from __future__ import absolute_import
'''
version: 1.0.0
date: 21/04/2020

#----------------
content:

This will create a UI for the autorriger Options tool.

#----------------
how to:

import Mutant_Tools
from Mutant_Tools.UI.AutoRigger import load_autoRiggerOptions
reload(load_autoRiggerOptions)

try:AutoRiggerMenu.close()
except:pass
options = load_autoRiggerOptions.AutoRiggerOptions()
options.show()

#----------------
dependencies:

QT FILE
ICONS
JSON FILES
Main Mutant

#----------------
www.mutanttools.com
author:  Esteban Rodriguez <info@renderdemartes.com>

'''
# -------------------------------------------------------------------
try:
    from shiboken6 import wrapInstance
    from PySide6 import QtGui, QtCore
    from PySide6 import QtUiTools
    from PySide6 import QtWidgets
    from PySide6.QtWidgets import *
except: 
    from shiboken2 import wrapInstance #Compatibility pre 2026
    from PySide2 import QtGui, QtCore
    from PySide2 import QtUiTools
    from PySide2 import QtWidgets
    from PySide2.QtWidgets import *
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as omui
from functools import partial
# import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel
from pathlib import Path

import os
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import sys
import json
import Mutant_Tools
import Mutant_Tools.UI
from Mutant_Tools.UI import QtMutantWindow
reload(QtMutantWindow)
from Mutant_Tools.Utils.Helpers.decorators import undo

from Mutant_Tools.Utils.Rigging import main_mutant
reload(Mutant_Tools.Utils.Rigging.main_mutant)
mt = main_mutant.Mutant()


# -------------------------------------------------------------------

#Read name conventions as nc[''] and setup as setup['']
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-2]
FOLDER=''
for f in PATH_PARTS:
	FOLDER = os.path.join(FOLDER, f)

JSON_FILE = os.path.join(FOLDER, 'config', 'name_conventions.json')
with open(JSON_FILE) as json_file:
	nc = json.load(json_file)
#Read curve shapes info
CURVE_FILE = os.path.join(FOLDER, 'config', 'curves.json')
with open(CURVE_FILE) as curve_file:
	curve_data = json.load(curve_file)
#setup File
SETUP_FILE = os.path.join(FOLDER, 'config', 'rig_setup.json')
with open(SETUP_FILE) as setup_file:
	setup = json.load(setup_file)

# -------------------------------------------------------------------

#QT WIndow!
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-2]
FOLDER=''
for p in PATH_PARTS:
	FOLDER = os.path.join(FOLDER, p)
PATH = os.path.join(FOLDER, 'UI')

ICONS_FOLDER = os.path.join(FOLDER,'Icons')

Title = 'Options'
UI_File = 'autoRiggerOptions.ui'



# -------------------------------------------------------------------

def maya_main_window():
	main_window_ptr = omui.MQtUtil.mainWindow()
	return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class AutoRiggerOptions(QtMutantWindow.Qt_Mutant):

	def __init__(self, parent=maya_main_window(), autorigger_ui = '', block='', layout=''):
		super(AutoRiggerOptions, self).__init__(parent)


		self.designer_loader_child(path=os.path.join(FOLDER,'UI','AutoRigger'), ui_file=UI_File)


		self.create_layout()
		self.create_connections()

		self.setWindowTitle(Title+' | '+block)
		self.set_title(Title+' | '+block)

		self.open_over_mouse()
		self.enable_popup_mode()

		self.block = block
		self.layout = layout
		self.autorigger_ui = autorigger_ui

		self.set_margins(top=2, buttom=2, right=2, left=2)

	# -------------------------------------------------------------------

	def create_layout(self):

		''


	# -------------------------------------------------------------------

	def create_connections(self):

		self.ui.duplicate_button.clicked.connect(self.duplicate_cmd)
		self.ui.delete_button.clicked.connect(self.delete_cmd)
		self.ui.delete_build_button.clicked.connect(self.delete_build_cmd)
		self.ui.change_name_button.clicked.connect(self.change_name_cmd)
		self.ui.update_button.clicked.connect(self.update_cmd)

	# -------------------------------------------------------------------
	@undo
	def duplicate_cmd(self, block=None):
		print(self.block,'Duplicate')
		if not block:
			block = self.block
		name = block.replace(nc['module'], '')
		og_guides = cmds.listRelatives(block, c=True)
		if og_guides:
			cmds.parent(og_guides, w=True)

		#Dup block
		new_name = mt.ask_name(text='',
							   ask_for='New Name',
							   check_split=True)

		new_block = cmds.duplicate(block, name=new_name+nc['module'], un=True)
		config = new_block[-1]
		new_block = new_block[0]
		config = cmds.listConnections(new_block)[1]
		cmds.rename(config, new_name+'_Config')

		#Dup guides
		if og_guides:
			for guide in og_guides:
				print(guide)
				if guide.endswith("_Loc"):
					new_guide = cmds.duplicate(guide, name=new_name + "_Loc")[0]
				else:
					new_guide = cmds.duplicate(guide, name=new_name + nc['guide'])[0]

				print(new_guide)
				cmds.parent(new_guide, new_block)

				#rename all guides:
				new_guide_childs = cmds.listRelatives(new_guide, ad=True)
				new_guide_childs_full_name = cmds.listRelatives(new_guide, ad=True, f=True)
				if new_guide_childs:
					for g, full_g in zip(new_guide_childs, new_guide_childs_full_name):
						cmds.rename(full_g, g.replace(name, new_name))

		#Restore
		if og_guides:
			cmds.parent(og_guides, block)

		#Make the new block pretty on shapes
		if og_guides:
			shapes = cmds.listRelatives(new_guide, ad=True, type='shape')
			if shapes:
				for s in shapes:
					if cmds.objectType(s)=="nurbsCurve":
						cmds.setAttr("{}.lineWidth".format(s), int(setup['line_width']))

		try:
			self.autorigger_ui.create_layout()
			mt.update_icons()
		except Exception as e:
			print('Duplicate refresh error: {}'.format(e))

		cmds.select(new_block)
		self.close()

	@undo
	def delete_cmd(self):
		print(self.block, 'Delete Block')
		cmds.delete(self.block)
		self.layout.setParent(None)
		self.close()

	@undo
	def delete_build_cmd(self):
		print(self.block, 'Delete Data')
		if cmds.attributeQuery("notes", n=self.block, ex=True):
			notes = cmds.getAttr("{}.notes".format(self.block))
			nodes_list = str(notes)[1:-1]
			nodes_list = nodes_list.replace("u'", "'")
			nodes_list = nodes_list.replace("'", "")
			for i in nodes_list.split(', '):
				if cmds.objExists(i):
					if cmds.nodeType(i) == 'skinCluster':
						print('Skipped', i)
						continue
					cmds.delete(i)
		print('Done Deleting:', self.block)

	@undo
	def change_name_cmd(self, block=None):
		if not block:
			block = self.block

		print(block, 'Rename')
		config = cmds.listConnections(block)[1]
		name = block.replace(nc['module'], '')
		guides = cmds.listRelatives(block, ad=True)

		new_name = mt.ask_name( text=name,
								ask_for='New Name',
                       			check_split=True)
		new_block = cmds.rename(block, block.replace(name, new_name))
		cmds.rename(config, config.replace(name, new_name))
		if guides:
			for g in guides:
				cmds.rename(g, g.replace(name, new_name))

		try:
			self.autorigger_ui.create_layout()
			cmds.select(new_block)
		except:
			pass


	@undo
	def update_cmd(self, block=None, auto_match_only=False):
		if not block:
			block = self.block

		config = cmds.listConnections(block)[1]
		import_cmds = cmds.getAttr('{}.Import_Command'.format(config))
		desire_json = ''

		#get all block jsons
		jsons = self.get_all_jsons()
		for j in jsons:
			with open(j) as block_data:
				block_data = json.load(block_data)
			if block_data.get('import') == import_cmds:
				desire_json = os.path.basename(j)
				desire_json = desire_json.replace('.json', '')
				break

		if auto_match_only:
			for file in jsons:
				if desire_json and desire_json.lower() in file.lower():
					desire_json = file
					break
		else:
			json_name = mt.ask_name(text=desire_json,
									ask_for='Block Name, Example: 04_Limb',
									check_split=False, allow_name_exists=True)
			if not json_name:
				return False

			#Find the correct json
			desire_json = None
			for file in jsons:
				if json_name.lower() in file.lower():
					desire_json = file
		print(desire_json)
		if not desire_json:
			cmds.error('No json found with that name')

		#Get json data
		with open(desire_json) as module_file:
			module = json.load(module_file)

		import pprint
		pprint.pprint(module)

		#update the config
		self.update_config(block, config, module)

	def update_config(self, block, config, module):
		print(config)
		attrs_in_json = module.get('attrs', {})
		attrs_in_config = cmds.listAttr(config , ud=True) or []

		print(attrs_in_config)
		print(attrs_in_json)

		skips = ['precode', 'postcode', 'Build_Command', 'Import_Command']
		attrs_to_recreate = []
		existing_values = {}

		#if not in json delete
		for attr in attrs_in_config:
			if attr in skips:
				continue
			clean_attr = self.get_mutant_config_attr(attr, config)
			if clean_attr not in attrs_in_json:
				if cmds.attributeQuery(attr, node=config, exists=True):
					cmds.deleteAttr('{}.{}'.format(config, attr))
			else:
				attrs_to_recreate.append(attr)
				existing_values[clean_attr] = self.get_config_attr_value(config=config, attr=attr, attr_key=clean_attr)

		# Recreate custom attrs in JSON order so the UI/channel order matches the json file
		for attr in attrs_to_recreate:
			if cmds.attributeQuery(attr, node=config, exists=True):
				cmds.deleteAttr('{}.{}'.format(config, attr))

		for attr in attrs_in_json:
			attr_name = attr.split('_')[0]
			if 'string' in attr:
				mt.string_attr(input=config, name=attr_name, string=module['attrs'][attr])
			elif 'enum' in attr:
				mt.new_enum(input=config, name=attr_name, enums=module['attrs'][attr])
			elif 'float' in attr:
				mt.new_attr_interger(input=config, name=attr_name, min=1, max=20, default=int(module['attrs'][attr]))
			elif 'bool' in attr:
				mt.new_boolean(input=config, name=attr_name, dv=module['attrs'][attr])

			value_to_set = module['attrs'][attr]
			if attr in existing_values:
				value_to_set = existing_values[attr]

			self.set_config_attr_value(config=config, attr=attr_name, attr_key=attr, value=value_to_set)

	def set_config_attr_value(self, config, attr, attr_key, value):
		attr_path = '{}.{}'.format(config, attr)
		if not cmds.attributeQuery(attr, node=config, exists=True):
			return

		try:
			if 'string' in attr_key:
				cmds.setAttr(attr_path, str(value), type='string')
			elif 'enum' in attr_key:
				enums = cmds.attributeQuery(attr, node=config, listEnum=True)
				if enums:
					enum_values = enums[0].split(':')
					if isinstance(value, str) and value in enum_values:
						cmds.setAttr(attr_path, enum_values.index(value))
					elif isinstance(value, int):
						cmds.setAttr(attr_path, value)
			elif 'float' in attr_key:
				cmds.setAttr(attr_path, int(value))
			elif 'bool' in attr_key:
				cmds.setAttr(attr_path, bool(value))
		except Exception as e:
			print('Could not set {}: {}'.format(attr_path, e))

	def get_config_attr_value(self, config, attr, attr_key):
		attr_path = '{}.{}'.format(config, attr)
		if not cmds.attributeQuery(attr, node=config, exists=True):
			return None

		try:
			if 'enum' in attr_key:
				current_index = cmds.getAttr(attr_path)
				enums = cmds.attributeQuery(attr, node=config, listEnum=True)
				if enums:
					enum_values = enums[0].split(':')
					if 0 <= int(current_index) < len(enum_values):
						return enum_values[int(current_index)]
				return current_index
			return cmds.getAttr(attr_path)
		except Exception as e:
			print('Could not read {}: {}'.format(attr_path, e))
			return None


	def get_mutant_config_attr(self, attr, config):
		attr_type = cmds.getAttr('{}.{}'.format(config, attr), type=True)

		if attr_type == 'string':
			attr = attr + '_string'
		elif attr_type == 'enum':
			attr = attr + '_enum'
		elif attr_type == 'long':
			attr = attr + '_float'
		elif attr_type == 'bool':
			attr = attr + '_bool'

		return attr

	def get_all_jsons(self):
		import glob
		main_path = os.path.join(FOLDER, 'Blocks')
		json_paths = os.path.join(main_path, '*', '*.json')

		jsons = glob.glob(json_paths)

		return jsons


	# CLOSE EVENTS _________________________________
	def closeEvent(self, event):
		''


# -------------------------------------------------------------------

if __name__ == "__main__":

	try:
		AutoRiggerMenu.close()  # pylint: disable=E0601
		AutoRiggerMenu.deleteLater()
	except:
		pass
	menu_ui = AutoRiggerOptions()
	menu_ui.show()

# -------------------------------------------------------------------

