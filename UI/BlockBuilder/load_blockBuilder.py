from __future__ import absolute_import
'''
version: 1.0.0

#----------------
content:

#----------------
how to:

try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import Mutant_Tools
from Mutant_Tools.UI.BlockBuilder import load_blockBuilder
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

reload(load_blockBuilder)

try:BlockBuilder.close()
except:pass
BlockBuilder = load_blockBuilder.BlockBuilder()
BlockBuilder.show()

#----------------
dependencies:

QT FILE
ICONS
JSON FILES
Main Mutant

#----------------
licence: https://www.eulatemplate.com/live.php?token=FGISW7ApRfgywum6murbBmLcusKONzkv
author:  Esteban Rodriguez <info@renderdemartes.com>

'''
#-------------------------------------------------------------------
from shiboken2 import wrapInstance
from PySide2 import QtGui,QtCore
from PySide2 import QtUiTools
from PySide2 import QtWidgets
from PySide2.QtWidgets import *

import maya.OpenMayaUI as omui
from functools import partial
from maya import OpenMaya
import maya.cmds as cmds
import maya.mel as mel

import os
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import sys
import json
import glob
import pprint
from pathlib import Path

from collections import OrderedDict

#-------------------------------------------------------------------



#Read name conventions as nc[''] and setup as seup['']
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

#-------------------------------------------------------------------
    
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import Mutant_Tools
from Mutant_Tools.UI.AutoRigger import load_autoRigger
reload(load_autoRigger)

try:AutoRigger.close()
except:pass
AutoRigger = load_autoRigger.AutoRigger()
AutoRigger.show()

BLOCKS_PATH = os.path.join(FOLDER, 'Blocks')
OTHERS_PATH = os.path.join(FOLDER, 'Others')
#-------------------------------------------------------------------

import Mutant_Tools
import Mutant_Tools.Utils
from Mutant_Tools.Utils.Rigging import main_mutant
reload(Mutant_Tools.Utils.Rigging.main_mutant)
mt = main_mutant.Mutant()

import Mutant_Tools.UI
from Mutant_Tools.UI import QtMutantWindow
reload(QtMutantWindow)
Qt_Mutant = QtMutantWindow.Qt_Mutant()

#-------------------------------------------------------------------


def maya_main_window(dockable=True):

	main_window_ptr = omui.MQtUtil.mainWindow()
	return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class BlockBuilder(QtMutantWindow.Qt_Mutant):

	def __init__(self):
		super(BlockBuilder, self).__init__()

		self.setWindowTitle('Block Builder')

		self.designer_loader_child(path=os.path.join(FOLDER, 'UI','BlockBuilder'), ui_file='blockBuilder.ui')
		self.set_title('Block Builder')

		self.create_layout()
		self.create_connections()

	#-------------------------------------------------------------------

	def create_layout(self):
		''
		
	def create_connections(self):
		self.ui.create_button.clicked.connect(self.create_block)

	#-------------------------------------------------------------------
	def create_block(self):
		self.create_config()
		OpenMaya.MGlobal.displayInfo('Block Created Succesfully')
		if self.ui.close_after.isChecked():
			self.close()

	def create_config(self):

		#grab the main info
		name = self.ui.name_line.text()
		description = self.ui.description_line.text()
		icon = self.ui.icon_line.text()

		if self.ui.presets_radio.isChecked():
			tab = '000_Presets'
		elif self.ui.studio_radio.isChecked():
			tab = '001_Studio'
		elif self.ui.biped_radio.isChecked():
			tab = '002_Biped'
		elif self.ui.facial_radio.isChecked():
			tab = '003_Facial'
		elif self.ui.animals_radio.isChecked():
			tab = '004_Animals'
		elif self.ui.clothes_radio.isChecked():
			tab = '005_Clothes'
		elif self.ui.vehicles_radio.isChecked():
			tab = '006_Vehicles'
		elif self.ui.props_radio.isChecked():
			tab = '008_Props'
		elif self.ui.games_radio.isChecked():
			tab = '007_Games'
		elif self.ui.data_radio.isChecked():
			tab = '009_Data'
		else :
			tab = '010_Other'


		#create the config dic with ordered dict so it can mantain the order we desire
		block_data = OrderedDict()

		block_data['Name'] =         name
		block_data['Description'] =  description
		block_data['Icon'] =         icon + '.png'

		block_data['Enable'] =       'True'

		block_data['python_file'] =  'exec_{}.py'.format(name.lower())
		block_data['import'] =       'import exec_{}'.format(name.lower())
		block_data['imp.reload'] =   'reload(exec_{})'.format(name.lower())
		block_data['exec_command'] = 'exec_{}.create_{}_block()'.format(name.lower(), name.lower())
		block_data['build_command'] ='exec_{}.build_{}_block()'.format(name.lower(), name.lower())

		attrs_data = OrderedDict()
		attrs_data[self.ui.attr_name_1.text()] = self.ui.attr_settings_1.text()
		attrs_data[self.ui.attr_name_2.text()] = self.ui.attr_settings_2.text()
		attrs_data[self.ui.attr_name_3.text()] = self.ui.attr_settings_3.text()
		attrs_data[self.ui.attr_name_4.text()] = self.ui.attr_settings_4.text()
		attrs_data[self.ui.attr_name_5.text()] = self.ui.attr_settings_5.text()
		attrs_data[self.ui.attr_name_6.text()] = self.ui.attr_settings_6.text()
		attrs_data[self.ui.attr_name_7.text()] = self.ui.attr_settings_7.text()
		attrs_data[self.ui.attr_name_8.text()] = self.ui.attr_settings_8.text()
		attrs_data[self.ui.attr_name_9.text()] = self.ui.attr_settings_9.text()
		attrs_data[self.ui.attr_name_10.text()] = self.ui.attr_settings_10.text()

		try:attrs_data.pop('') #remove empty keys if the line edit werent used
		except:pass

		block_data['attrs'] = attrs_data

		#find next number for the json file
		all_blocks = glob.glob(os.path.join(BLOCKS_PATH, tab, '*json'))
		pprint.pprint(all_blocks)

		if all_blocks:
			last_block = all_blocks[-1]
			last_block = last_block.split('\\')[-1]
			last_num = last_block.split('/')[-1].split('_')[0]
			print (last_num)
			new_num = '0' + str(int(last_num[1]) + 1)
		else:
			new_num=0

		#write json file
		new_json_file = os.path.join(BLOCKS_PATH, tab, '{}_{}.json'.format(new_num, name))
		with open(new_json_file, 'w') as new_config:
			json.dump(block_data, new_config, indent=4, sort_keys = False)

		pprint.pprint(block_data)

		#open exec python file and change it to fit new one

		if self.ui.simple_block.isChecked():
			base_python_preset = os.path.join(OTHERS_PATH,'Exec_Block.py')
		else:
			base_python_preset = os.path.join(OTHERS_PATH,'exec_block_sides.py')

		with open(base_python_preset) as exec_block:
			exec_code = exec_block.read()

		new_exec_code = exec_code.replace("TAB_FOLDER = 'TAB'", "TAB_FOLDER = '{}'".format(tab))
		new_exec_code = new_exec_code.replace("PYBLOCK_NAME = 'exec_NAME'", "PYBLOCK_NAME = 'exec_{}'".format(name.lower()))
		new_exec_code = new_exec_code.replace("create_NAME_block(name = 'NAME')", "create_{}_block(name = '{}')".format(name.lower(),name))
		new_exec_code = new_exec_code.replace("#create_NAME_block()", "#create_{}_block()".format(name.lower()))
		new_exec_code = new_exec_code.replace("def build_NAME_block():", "def build_{}_block():".format(name.lower()))
		new_exec_code = new_exec_code.replace("#build_NAME_block()", "#build_{}_block()".format(name.lower()))

		new_exec_code = new_exec_code.replace("num_name.json", "{}_{}.json".format(new_num, name))
		new_exec_code = new_exec_code.replace("icon = 'ICON_NAME'", "icon = '{}'".format(icon))

		print (new_exec_code)

		#write .py file
		new_file = os.path.join(BLOCKS_PATH, tab, 'exec_{}.py'.format(name.lower()))
		with open(new_file, 'w') as new_py:
				new_py.write(new_exec_code)

	#-------------------------------------------------------------------

	# CLOSE EVENTS _________________________________
	def closeEvent(self, event):
		''

#-------------------------------------------------------------------

if __name__ == "__main__":

	try:
		BlockBuilder_ui.close() # pylint: disable=E0601
		BlockBuilder_ui.deleteLater()
	except:
		pass
	BlockBuilder_ui = BlockBuilder()
	BlockBuilder_ui.show()

#-------------------------------------------------------------------

'''
#Notes






'''