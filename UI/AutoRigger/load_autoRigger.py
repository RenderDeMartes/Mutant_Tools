from __future__ import absolute_import, division
'''
version: 1.0.0
date: 21/04/2020

#----------------
content:

This will create a UI for the autorriger tool. Is dinamically created based on the .json files inside the folders

#----------------
how to:
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
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

import maya.OpenMayaUI as omui
from functools import partial
from maya import OpenMaya
import maya.cmds as cmds
import maya.mel as mel

import os
import time
import tempfile

try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import sys
import json
from collections import OrderedDict
from pathlib import Path
try:
	from rstar import convention
	convention.set_project()
except Exception as e:
	cmds.warning('Error loading rstar.convention on load_AutoRigger')

from Mutant_Tools.UI.AutoRigger import load_autoRiggerMenu
reload(load_autoRiggerMenu)

from Mutant_Tools.UI.CodeReader import load_codeReader
reload(load_codeReader)
log_ui = load_codeReader.Code_Reader(mode='view', code= '', config_attr = '')

import Mutant_Tools.UI
from Mutant_Tools.UI import QtMutantWindow
reload(QtMutantWindow)

import Mutant_Tools.UI.CustomWidgets.expandableWidget as expandableWidget
reload(expandableWidget)

from Mutant_Tools.Utils.Helpers import helpers
reload(Mutant_Tools.Utils.Helpers.helpers)
mh = helpers.Helpers()

import Mutant_Tools.Utils.IO
from Mutant_Tools.Utils.IO import EasySkin
reload(Mutant_Tools.Utils.IO.EasySkin)

from Mutant_Tools.Utils.IO import CtrlUtils
reload(Mutant_Tools.Utils.IO.CtrlUtils)
ctrls = CtrlUtils.Ctrls()

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
#Version File
VERSION_FILE = os.path.join(FOLDER, 'config', 'version.json')
with open(VERSION_FILE) as version_file:
	version = json.load(version_file)
#-------------------------------------------------------------------

#QT WIndow!
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-2]
FOLDER=''
for f in PATH_PARTS:
	FOLDER = os.path.join(FOLDER, f)
UI_File = 'autoRigger.ui'
IconsPath =  os.path.join(FOLDER, 'Icons')
Title = 'AutoRigger'

#-------------------------------------------------------------------

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()

import Mutant_Tools.UI.CustomWidgets.expandableWidget as expandableWidget
reload(expandableWidget)

#-------------------------------------------------------------------
def add_sys_folders_remove_compiled():
	#get all the paths for the blocks in the sys path
	file_path = (str(__file__))
	for folder in os.listdir(os.path.join(FOLDER , 'Blocks')):
		blocks_path = os.path.join(FOLDER, 'Blocks', folder)
		if blocks_path not in sys.path:
			sys.path.append(blocks_path)

	#Delete all pyc in the block folders so we dont need the imp.reload in the codes:
	path = os.path.join(FOLDER, 'Blocks')
	for path, subdirs, files in os.walk(path):
		for name in files:
			#print('Search: ' + os.path.join(path, name))
			if '.pyc' in str(name):
				#print (name + ': Have been deleted')
				os.remove(os.path.join(path, name))
			if '__pycache__' in str(name):
				#print (name + ': Have been deleted')
				os.remove(os.path.join(path, name))
			if 'DS_Store' in str(name):
				# print (name + ': Have been deleted')
				os.remove(os.path.join(path, name))

	# also remove pyc from UIs folder
	path = FOLDER
	for path, subdirs, files in os.walk(path):
		for name in files:
			if '.pyc' in str(name):
				#print (name + ': Have been deleted')
				os.remove(os.path.join(path, name))
			if '.DS_Store' in str(name):
				#print (name + ': Have been deleted')
				os.remove(os.path.join(path, name))
	print ('Cache removed...')

#-------------------------------------------------------------------

class AutoRigger(QtMutantWindow.Qt_Mutant):

	def __init__(self):
		super(AutoRigger, self).__init__()

		#UI Init
		self.setWindowTitle(Title)
		self.set_title(Title)

		self.create_menu()

		self.resize(605, 652)

		#load blocks folders to sys and remove all the compiled info in BLOCKS and UI Folder
		if mt.check_dev_mode():
			add_sys_folders_remove_compiled()
		self.reload_ready = False
		self.designer_loader_child(path=os.path.join(FOLDER,'UI','AutoRigger'), ui_file=UI_File)

		self.create_menus()
		self.create_layout()
		self.create_connections()
		self.reload_blocks_if_isnt_working()

		#009_Data init
		self.current_block = None
		self.current_block_folder = None

		#update icons
		mt.update_icons()

		#find tools updates:
		#mt.compare_versions()

		#load script job
		self.current_selected_block = False
		self.mutant_sj = cmds.scriptJob(event=["SelectionChanged", self.mutant_script_job])

		self.recipes_dict = {}

		self.studio_name = setup['studio']
		self.ui.tabs.setTabText(1, self.studio_name)

		try:OpenMaya.MGlobal.displayInfo('<3')
		except:pass

	#-------------------------------------------------------------------

	def force_load_of_dependency_plugins(self):
		plugins_windows = ['quatNodes.mll', 'objExport.mll','lookdevKit.mll', 'matrixNodes.mll']
		plugins_linux = plugins = ['quatNodes.so', 'objExport.so','lookdevKit.so', 'matrixNodes.so']
		for w_plugin, l_plugin in zip(plugins_windows, plugins_linux):
			try:cmds.loadPlugin(w_plugin)
			except:cmds.loadPlugin(l_plugin)

	def exit_ui(self):

		close_comfirm = cmds.confirmDialog(
						title='Close Mutant Autorigger',
						message='Are you sure?',
						button=['Close', 'Stay Open'],
						defaultButton='Stay Open',
						dismissString='Stay Open',
						cancelButton = 'Stay Open')

		if close_comfirm == 'Close':
			print('Mutant is closing')
			self.close()

	#-------------------------------------------------------------------

	def mutant_script_job(self):
		sel = cmds.ls(sl=True)
		if not sel:
			return
		if self.current_selected_block == sel[0]:
			return

		try:
			if str(sel[0]).endswith('_Block'):
				self.create_properties_layout(block = cmds.ls(sl=True)[0])
				self.current_selected_block = sel[0]
		except:
			pass


	#-------------------------------------------------------------------
	def reload_blocks_if_isnt_working(self):

		try:
			import exec_limb
		except:
			self.reload_all_blocks()

	#-------------------------------------------------------------------
	def create_menus(self):

		# self.menu = load_autoRiggerMenu.AutoRiggerMenu()
		# self.ui.menuLayout.addWidget(self.menu)
		# self.search_button = QPushButton()
		# #self.search_button.setFixedSize(20,20)
		# #self.ui.menuLayout.addWidget(self.search_button)

		#Relaod blocks connection in Menu
		self.menu.dev_reload.triggered.connect(self.reload_all_blocks)
		

	def create_layout(self):
		self.create_block_buttons()
		self.delete_side_buttons()

		try:self.create_all_side_buttons()
		except Exception as e:
			print(e)

		try:self.ui.layout().setContentsMargins(3, 3, 3, 3)
		except:pass
		self.ui.progressBar.setValue(0)
		self.ui.bar_label.setText('Mutant')

		#set Manual Icons
		self.ui.prebuild.setIcon(QtGui.QIcon(os.path.join(IconsPath ,'PRECODE.png')))
		self.ui.current_code.setIcon(QtGui.QIcon(os.path.join(IconsPath ,'CODE.png')))
		self.ui.postbuild.setIcon(QtGui.QIcon(os.path.join(IconsPath ,'POSTCODE.png')))
		self.ui.reload_ui.setIcon(QtGui.QIcon(os.path.join(IconsPath ,'RELOAD.png')))
		self.ui.log.setIcon(QtGui.QIcon(os.path.join(IconsPath ,'LOG.png')))


	def reload_ui(self):

		#Search delete
		self.ui.search_line.setText('')

		self.create_layout()
		#OpenMaya.MGlobal.displayInfo('<3')

		#rest propierties layout too
		for i in reversed(range(self.ui.properties_layout.count())):
			self.ui.properties_layout.itemAt(i).widget().setParent(None)
		self.ui.block_label.setText('Mutant Autorigger')

	def create_connections(self):

		self.ui.reload_ui.clicked.connect(self.reload_ui)
		self.ui.build_btn.clicked.connect(self.build_autorigger)

		self.ui.prebuild.clicked.connect(lambda : self.edit_prebuild_code(self.current_block))
		self.ui.current_code.clicked.connect(lambda : self.view_build_code(self.current_block))
		self.ui.postbuild.clicked.connect(lambda : self.edit_postbuild_code(self.current_block))
		self.ui.log.clicked.connect(lambda : self.view_log())

		self.ui.search_button.clicked.connect(self.search_command)

	#-------------------------------------------------------------------
	def reload_all_blocks(self):

		if self.reload_ready and not mt.check_dev_mode():
			return True

		add_sys_folders_remove_compiled()

		#'create all the buttons in the tabs blocks'
		blocks_folders = os.listdir(os.path.join(FOLDER, 'Blocks'))

		#Progress bar
		from Mutant_Tools.UI.ProgressBar import load_progress_bar
		reload(load_progress_bar)
		cProgressBarUI = load_progress_bar.ProgressBarUI(items=blocks_folders,
														 title='Loading Mutant...')
		cProgressBarUI.show()
		avoid_folders = ['.DS_Store']

		for num, block_folder in enumerate(blocks_folders):

			if block_folder in avoid_folders:
				continue
			cProgressBarUI.set_percent(num)

			print (block_folder)
			if block_folder not in sys.path:
				sys.path.append(block_folder)

			# clean_folder_name = block_folder.split('_')[1]
			# files = os.listdir(os.path.join(FOLDER, 'Blocks', block_folder))
			#
			# for num, block_file in enumerate(files):
			# 	#print(block_file)
			#
			# 	if not '.json' in str(block_file): #if the file != a json continue with the next one
			# 		continue
			#
			# 	#read the json file with block information
			# 	real_path =  os.path.join(FOLDER, 'Blocks', block_folder,  block_file)
			# 	sys.path.append(real_path)
			#
			# 	with open(real_path, "r") as block_info:
			# 		block = json.load(block_info)
			# 		#reaload with json files info if dev mode is on, off loads faster
			# 		try:
			# 			exec(block['import'])
			# 			exec(block['imp.reload'])
			# 		except Exception as e:
			# 			print('Importing error on {}'.format(block_file), e)

		cProgressBarUI.close()

	#-------------------------------------------------------------------
	def create_block_buttons(self):

		if mt.check_dev_mode():
			self.reload_all_blocks()

		#first we delete all the previews items on the layouts
		for i in reversed(range(self.ui.presets_layout.count())):
			self.ui.presets_layout.itemAt(i).widget().setParent(None)
		for i in reversed(range(self.ui.studio_layout.count())):
			self.ui.studio_layout.itemAt(i).widget().setParent(None)
		for i in reversed(range(self.ui.biped_layout.count())):
			self.ui.biped_layout.itemAt(i).widget().setParent(None)
		for i in reversed(range(self.ui.facial_layout.count())):
			self.ui.facial_layout.itemAt(i).widget().setParent(None)
		for i in reversed(range(self.ui.animals_layout.count())):
			self.ui.animals_layout.itemAt(i).widget().setParent(None)
		for i in reversed(range(self.ui.vehicles_layout.count())):
			self.ui.vehicles_layout.itemAt(i).widget().setParent(None)
		for i in reversed(range(self.ui.clothes_layout.count())):
			self.ui.clothes_layout.itemAt(i).widget().setParent(None)
		for i in reversed(range(self.ui.props_layout.count())):
			self.ui.props_layout.itemAt(i).widget().setParent(None)
		for i in reversed(range(self.ui.games_layout.count())):
			self.ui.games_layout.itemAt(i).widget().setParent(None)
		for i in reversed(range(self.ui.data_layout.count())):
			self.ui.data_layout.itemAt(i).widget().setParent(None)
		for i in reversed(range(self.ui.other_layout.count())):
			self.ui.other_layout.itemAt(i).widget().setParent(None)

		#'create all the buttons in the tabs blocks'
		blocks_folders = os.listdir(os.path.join(FOLDER, 'Blocks'))
		avoid_folders = ['.DS_Store', 'OldSystems']
		for block_folder in blocks_folders:
			if block_folder in avoid_folders:
				continue
			#print (block_folder)
			clean_folder_name = block_folder.split('_')[1]
			files = sorted(os.listdir(os.path.join(FOLDER, 'Blocks', block_folder)))
			have_order = False
			if 'order.json' in files:
				have_order = True

			if have_order:
				order_path = os.path.join(FOLDER, 'Blocks', block_folder, 'order.json')
				with open(order_path, "r") as order_path:
					order_data = json.load(order_path)

				files = []
				for tittle in order_data:
					files.append(tittle+'_Tittle.json')
					order_files = order_data[tittle]
					for f in order_files:
						files.append(f)

			for block_file in files:

				if not '.json' in str(block_file): #if the file != a json continue with the next one
					continue

				if 'Tittle' in block_file:
					button = QFrame()
					button.setFrameShape(QFrame.VLine)
					button.setFrameShadow(QFrame.Sunken)
					button.setToolTip(block_file.replace('_Tittle.json', ''))
					button.setFixedHeight(15)
					button.setContentsMargins(0, 0, 0, 0)

				else:
					#read the json file with block information
					real_path =  os.path.join(FOLDER, 'Blocks', block_folder,  block_file)

					with open(real_path, "r") as block_info:
						block = json.load(block_info)
						#reaload with json files info if dev mode is on, off loads faster

					#create button
					block_name = str(block_file).split('_')[1].replace('.json', '')
					button = QPushButton()#give a nicer name
					button.clicked.connect(partial (self.create_new_block, real_path))
					button.clicked.connect(self.create_layout)
					button.setToolTip(block['Description'])
					button.setFixedSize(40, 40)


					try:
						button.setIcon(QtGui.QIcon(os.path.join(IconsPath ,block['Icon'])))
						button.setIconSize((QtCore.QSize(35, 35)))
						button.setStyleSheet("text-align:right;")
						#button.setText(block_name)
					except:
						button.setText(block_name)

					if block['Enable'] == 'False':
						button.setEnabled(False)

				#parent to correct tab
				if block_folder == '000_Presets':
					self.ui.presets_layout.addWidget(button)
				elif block_folder == '001_Studio':
					self.ui.studio_layout.addWidget(button)
				elif block_folder == '002_Biped':
					self.ui.biped_layout.addWidget(button)
				elif block_folder == '003_Facial':
					self.ui.facial_layout.addWidget(button)
				elif block_folder == '004_Animals':
					self.ui.animals_layout.addWidget(button)
				elif block_folder == '005_Clothes':
					self.ui.clothes_layout.addWidget(button)
				elif block_folder == '006_Vehicles':
					self.ui.vehicles_layout.addWidget(button)
				elif block_folder == '007_Games':
					self.ui.games_layout.addWidget(button)
				elif block_folder == '008_Props':
					self.ui.props_layout.addWidget(button)
				elif block_folder == '009_Data':
					self.ui.data_layout.addWidget(button)
				else:
					self.ui.other_layout.addWidget(button)

				if not have_order:
					button.setFixedSize(42, 42)

	#-------------------------------------------------------------------
	def create_new_block(self,bock_path):

		#this will create a new block in maya based on the info on the json files
		#read json
		with open(bock_path, "r") as block_info:
			block = json.load(block_info)

		cmds.undoInfo(openChunk=True)

		exec (block['import'])
		if mt.check_dev_mode():
			try:exec (block['imp.reload'])
			except: print ('couldnt imp.reload {}'.format(bock_path))
		exec (block['exec_command'])
		mt.update_icons()
		self.create_properties_layout(block = cmds.ls(sl=True)[0])

		cmds.undoInfo(closeChunk=True)

	#-------------------------------------------------------------------
	def delete_side_buttons(self):

		# this will clear the side layout so we can move stuff around
		for i in reversed(range(self.ui.side_layout.count())):
			self.ui.side_layout.itemAt(i).widget().setParent(None)

		self.ui.side_scroll.setWidgetResizable(True)

	def options_side_buttonblock(self, block, layout):

		from Mutant_Tools.UI.AutoRigger import load_autoRiggerOptions
		reload(load_autoRiggerOptions)
		options = load_autoRiggerOptions.AutoRiggerOptions(autorigger_ui=self, block=block, layout=layout)
		options.show()


	#-------------------------------------------------------------------

	def create_all_side_buttons(self):

		#search_data
		search_text = self.ui.search_line.text()

		cmds.select('Mutant_Build')
		sel = cmds.ls(sl=True)
		if not sel:
			build_group = 'Mutant_Build'
		else:
			build_childs = cmds.listRelatives(sel[0], ad=True)
			for child in build_childs:
				if nc['module'] in str(child):
					build_group = sel[0]
					break
				else:
					build_group = 'Mutant_Build'

		if cmds.objExists(build_group):
			for num, child in enumerate(cmds.listRelatives(build_group, c=True)):
				if not child.endswith(nc['module']):
					colapsable_box = expandableWidget.expandableWidget(parent=self.ui.side_layout, title=child.replace('_Build', ''))
					grand_childs = cmds.listRelatives(child, c=True)
					#if not childs in group pass else parent sde button to group
					if grand_childs is None:
						continue
					else:
						for grand_child in grand_childs:
							if search_text:
								if search_text.lower() in grand_child.lower():
									self.create_side_button(pack_name=grand_child, index=num,
															block_parent=colapsable_box.layout)
							else:
								self.create_side_button(pack_name=grand_child, index=num, block_parent=colapsable_box.layout)
				else:
					if search_text:
						if search_text.lower() in grand_child.lower():
							self.create_side_button(pack_name=child, index=num, block_parent=None)
						else:
							continue
					else:
						self.create_side_button(pack_name=child, index=num, block_parent=None)

	#-------------------------------------------------------------------
	def create_side_button(self, pack_name = 'Mutant_Block', index = 0, block_parent = None):

		#This will create all the side buttons when the up buttons are clicked

		if block_parent == None:
			block_parent = self.ui.side_layout

		side_hbox = QGroupBox()
		block_parent.addWidget(side_hbox)

		#up down buttons
		up_button = QtWidgets.QPushButton()
		up_button.setIcon(QtGui.QIcon(os.path.join(IconsPath ,'Up.png')))
		down_button = QtWidgets.QPushButton()
		down_button.setIcon(QtGui.QIcon(os.path.join(IconsPath ,'Down.png')))
		up_button.setFixedSize(15,20)
		down_button.setFixedSize(15,20)

		#propierties button
		edit_button = QtWidgets.QPushButton(pack_name.replace(nc['module'],''))
		edit_button.setFixedSize(75,50)

		try:
			edit_button.setIcon(QtGui.QIcon(cmds.getAttr('{}.iconName'.format(pack_name))))
			edit_button.setIconSize((QtCore.QSize(30, 30)))
		except:
			edit_button.setText(pack_name)


		options_button = QtWidgets.QPushButton()
		options_button.setFixedSize(15,15)
		options_button.setIcon(QtGui.QIcon(os.path.join(IconsPath ,'Gear.png')))
		options_button.setToolTip('Options: {}'.format(pack_name))

		h_layout = QtWidgets.QHBoxLayout()
		v_layout = QtWidgets.QVBoxLayout()

		v_layout.addWidget(up_button)
		v_layout.addWidget(options_button)
		v_layout.addWidget(down_button)
		h_layout.addLayout(v_layout)
		h_layout.addWidget(edit_button)

		h_layout.addStretch()

		side_hbox.setLayout(h_layout)
		up_button.clicked.connect(partial (mt.move_outliner, pack_name, True, False))
		down_button.clicked.connect(partial (mt.move_outliner, pack_name, False, True))
		#down_button.clicked.connect(partial (self.create_properties_layout, cmds.ls(sl=True)[0]))
		#up_button.clicked.connect(partial (self.create_properties_layout, cmds.ls(sl=True)[0]))

		up_button.clicked.connect(self.create_layout)
		down_button.clicked.connect(self.create_layout)

		edit_button.clicked.connect(partial (self.create_properties_layout, pack_name))
		options_button.clicked.connect(partial (self.options_side_buttonblock, pack_name, side_hbox))

	#-------------------------------------------------------------------
	def create_properties_layout(self, block):
		#'Create All Properties Stuff'
		#self.create_layout()

		# this will clear the proprieties layout so we can recreate stuff
		for i in reversed(range(self.ui.properties_layout.count())):
			self.ui.properties_layout.itemAt(i).widget().setParent(None)

		#collect data for opening logs and codes
		self.current_block = block

		#print (block)
		cmds.select(self.current_block)
		config = cmds.listConnections(block)[1]
		attrs =  cmds.listAttr(config , ud=True)

		#create may q box to hold the widgets
		#side_hbox = QGroupBox(block)
		side_hbox = QGroupBox()
		self.ui.block_label.setText(block)

		self.ui.properties_layout.addWidget(side_hbox)
		v_layout = QtWidgets.QVBoxLayout()
		side_hbox.setLayout(v_layout)

		#get all attrs inf cofig node and get type so we can create UI depending of the type of attr

		self.check_precode(block)
		self.check_postcode(block)

		self.current_block = block

		#depending of the attr type create the UI
		for attr in attrs:

			edit_attr =  '{}.{}'.format(config, attr)

			#if the attrs is locked dont create anyting for it
			if cmds.getAttr(edit_attr,settable = True ) == False:
				continue
			#if attr is any of this continue
			skips = ['precode', 'postcode']
			if attr in skips: continue

			#main horizontal layout for each attr. they all have a label and the if is to add specific
			h_layout = QtWidgets.QHBoxLayout()
			h_layout.setContentsMargins(3, 5, 3, 5)
			#divisor
			layout_separator = QtWidgets.QLabel()
			layout_separator.setStyleSheet("border : 5px solid grey; ")
			layout_separator.setFixedHeight(1)
			v_layout.addWidget(layout_separator)
			#label
			label = QtWidgets.QLabel(attr + ': ')
			label.setFixedHeight(50)
			v_layout.addLayout(h_layout)
			h_layout.addWidget(label)

			#check Attrs type and create a layout diferente for each one
			attr_type = cmds.getAttr('{}.{}'.format(config,attr), type = True)


			#-----------------------------------------------------------------
			if attr_type == 'string':

				#Main strings attrs UI
				#print (attr + ': is string')
				line_edit = QtWidgets.QLineEdit(cmds.getAttr('{}.{}'.format(config, attr)))
				line_edit.textChanged.connect(partial(self.lineEdit_update_attr,line_edit, edit_attr))
				h_layout.addWidget(line_edit)

				if 'Set' in attr: #if set in name it will create a greab button
					set_button = QtWidgets.QPushButton('Set Selection')
					set_button.setFixedSize(80,30)
					set_button.clicked.connect(partial(self.lineEdit_get_selection,line_edit, edit_attr))

					select_button = QtWidgets.QPushButton()
					select_button.setFixedSize(20, 20)
					select_button.setIcon(QtGui.QIcon(os.path.join(IconsPath, 'Cursor.png')))
					select_button.clicked.connect(partial(self.lineEdit_sel_selection,line_edit, edit_attr))

					h_layout.addWidget(set_button)
					h_layout.addWidget(select_button)

				if 'File' in attr:
					file_button = QtWidgets.QPushButton('Browse')
					file_button.setFixedSize(80,35)
					file_button.clicked.connect(partial(self.lineEdit_get_file,line_edit, edit_attr))
					h_layout.addWidget(file_button)

				if 'Path' in attr:
					file_button = QtWidgets.QPushButton('Browse')
					file_button.setFixedSize(80,35)
					file_button.clicked.connect(partial(self.lineEdit_get_path,line_edit, edit_attr))
					h_layout.addWidget(file_button)

				if attr == 'Code':  # if code in name it will create a larger box
					line_edit.setParent(None)
					plainText_edit = QtWidgets.QPlainTextEdit(cmds.getAttr('{}.{}'.format(config, attr)))
					plainText_edit.textChanged.connect(partial(self.lineEdit_update_attr,plainText_edit, edit_attr))
					slider = QtWidgets.QSlider()
					h_layout.addWidget(plainText_edit)

				if attr == 'Help':  # if non string do a code box but non editable
					line_edit.setParent(None)
					plainText_edit = QtWidgets.QPlainTextEdit(cmds.getAttr('{}.{}'.format(config, attr)))
					plainText_edit.textChanged.connect(partial(self.lineEdit_update_attr,plainText_edit, edit_attr))
					slider = QtWidgets.QSlider()
					h_layout.addWidget(plainText_edit)
					plainText_edit.setReadOnly(True)

			#-----------------------------------------------------------------
			elif attr_type == 'enum':
				#get all the options in the config combo box and add them to a custom qt cumbo box
				#print (attr + ': is enum')
				enums = cmds.attributeQuery(attr, node=config, listEnum = True)[0]
				enums = str(enums).split(':')
				#print (enums)
				enum_box = QtWidgets.QComboBox()
				enum_box.addItems(enums)
				enum_box.setCurrentIndex(cmds.getAttr(edit_attr))
				enum_box.setStyleSheet('background-color: none;')
				enum_box.currentIndexChanged.connect(partial(self.enum_update_attr,enum_box,edit_attr))

				h_layout.addWidget(enum_box)

			#-----------------------------------------------------------------
			elif attr_type == 'long':
				#print (attr + ': is long')

				int_label = QtWidgets.QLabel(str(cmds.getAttr(edit_attr)))
				int_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
				int_slider.setValue(cmds.getAttr(edit_attr))
				if cmds.getAttr(edit_attr) > 20:
					int_slider.setMaximum(100)
				else:
					int_slider.setMaximum(20)
				int_slider.setStyleSheet('background-color: none;')
				int_slider.valueChanged.connect(partial(self.slider_update_attr, int_label, int_slider, edit_attr))

				h_layout.addWidget(int_label)
				h_layout.addWidget(int_slider)

			#-----------------------------------------------------------------
			elif attr_type == 'bool':
				#print (attr + ': is bool')
				checkbox = QtWidgets.QCheckBox(attr)
				checkbox.setChecked(cmds.getAttr('{}.{}'.format(config, attr)))
				checkbox.setStyleSheet('background-color: none;')
				h_layout.addWidget(checkbox)
				label.setParent(None)
				checkbox.stateChanged.connect(partial(self.checkBox_update_attr, checkbox, edit_attr))
			#-----------------------------------------------------------------


	#-------------------------------------------------------------------

	def delete_properties_layout(self):
		# this will clear the side layout so we can move stuff around
		for i in reversed(range(self.ui.properties_layout.count())):
			self.ui.properties_layout.itemAt(i).widget().setParent(None)
		#make UI Scrolable
		self.ui.properties_scroll.setWidgetResizable(True)

	#-------------------------------------------------------------------
	def lineEdit_update_attr(self, field, attr,*args):
		try:#simple line edits
			cmds.setAttr(attr, field.text(), type = 'string')
		except:#code plain Texts
			cmds.setAttr(attr, field.toPlainText(), type = 'string')

	def lineEdit_get_selection(self, field, attr,*args):
		sel = cmds.ls(sl=True)
		print(sel)
		#remove ugly lists keys
		nice_selection = str(sel)[1:-1]
		nice_selection = nice_selection.replace("u'", "'")
		nice_selection = nice_selection.replace("'", "")

		field.setText(nice_selection)
		cmds.setAttr(attr, nice_selection, type = 'string')

	def lineEdit_sel_selection(self, field, attr,*args):
		value = field.text()
		attr = cmds.getAttr(attr)

		if value == attr:
			print(attr)

		if ',' in value:
			value = value.split(',')

		try:
			cmds.select(value)
		except:
			cmds.warning('Selection doesnt exists')

	def lineEdit_get_file(self, field, attr, *args):
		path = mh.import_window(extension=".json")[0]
		field.setText(path)
		cmds.setAttr(attr, path, type='string')

	def lineEdit_get_path(self, field, attr, *args):
		path = mh.folder_window()
		field.setText(path)
		cmds.setAttr(attr, path, type='string')

	def slider_update_attr(self, label, slider,attr, *args):
		if slider.value() == 20:
			self.update_max_slider(slider, attr)
		cmds.setAttr(attr, slider.value())
		label.setText(str(slider.value()))

	def update_max_slider(self, slider, attr):
		print('updating value')
		cmds.addAttr(attr, edit=True, max=100)
		slider.setMaximum(100)


	def checkBox_update_attr(self, checkBox,attr, *args):
		cmds.setAttr(attr, checkBox.isChecked())

	def enum_update_attr(self, comboBox, attr, *args):
		cmds.setAttr(attr, comboBox.currentIndex())

	#-------------------------------------------------------------------

	def get_blocks_to_build(self, mode='Build Mutant Tools'):

		print(mode)

		to_build = []

		if mode == 'Build Mutant Tools':
			blocks = cmds.listRelatives('Mutant_Build', c=True)
		elif mode == 'Build Selected Group':
			grp = cmds.ls(sl=True)[0]
			blocks = cmds.listRelatives(grp, c=True)
		elif mode == 'Build Selected Block':
			blocks = cmds.ls(sl=True)

		for block in blocks:
			if not block.endswith(nc['module']):
				grand_childs = cmds.listRelatives(block, c=True)
				if not grand_childs:
					continue
				for grand_child in grand_childs:
					to_build.append(grand_child)
			else:
				to_build.append(block)

		return to_build

	#-------------------------------------------------------------------
	def build_autorigger(self, only_progressbar=False):

		self.ui.bar_label.resize(100, 200)
		self.ui.bar_label.setText('Starting the Build')

		#Load need plugins
		self.force_load_of_dependency_plugins()

		#Check rebuild
		rebuild = self.check_if_previous_build()
		if not rebuild:
			return False

		if rebuild == 'First Build':
			load_io = False
		elif rebuild == 'Just Rebuild':
			load_io = False
		else:
			load_io = True

		cmds.undoInfo(openChunk=True)

		#log
		try:
			cmds.scriptEditorInfo(ch=True)
			mt.Mutant_logger(mode = 'clear')
			mt.Mutant_logger(mode = 'stop')
		except:
			pass

		#build
		blocks = self.get_blocks_to_build(mode = self.ui.build_method.currentText())
		progress_max = len(blocks)
		self.ui.progressBar.setMaximum(progress_max)
		if only_progressbar:
			from Mutant_Tools.UI.ProgressBar import load_progress_bar
			reload(load_progress_bar)
			cProgressBarUI = load_progress_bar.ProgressBarUI(items=blocks,
															 title='Building Mutant...')
			cProgressBarUI.show()

		#select each block and run the build command and make progress bar move
		for num, block in enumerate(blocks):

			#just for fun
			cmds.refresh()

			#log
			mt.Mutant_logger(mode = 'create')
			print ('------------------------------------------------------------------------------------')
			print ('------------------------------------------------------------------------------------')
			print ('Building: {}'.format(block))
			print ('------------------------------------------------------------------------------------')
			print ('------------------------------------------------------------------------------------')

			self.ui.bar_label.setText('Building: {}'.format(block))
			self.ui.bar_label.setToolTip('Building: {}'.format(block))

			#building
			cmds.select(block)
			config = cmds.listConnections(block)[1]
			precode = cmds.getAttr('{}.precode'.format(config))
			import_command = cmds.getAttr('{}.Import_Command'.format(config))
			reload_command = import_command.replace('import', 'reload(')+')'.replace(' ', '')
			buid_command = cmds.getAttr('{}.Build_Command'.format(config))
			postcode = cmds.getAttr('{}.postcode'.format(config))

			self.ui.bar_label.setText(buid_command)
			self.ui.bar_label.setToolTip(buid_command)

			exec(import_command)
			exec(reload_command)
			print ('Import successfully {}'.format(import_command))
			pre_build_nodes = self.get_all_nodes()
			#if error in build show log and stop log writing
			try:
				if only_progressbar:
					cProgressBarUI.set_percent(num)
				# ----------------------
				# Precode---------------
				# ----------------------
				cmds.select(block)
				print('Precode {}'.format(block))
				if precode:
					try:
						exec(precode)
					except:
						mel.eval(precode)

				# ----------------------
				# BUILD-----------------
				# ----------------------
				cmds.select(block)
				#Build the blocks
				recipe_obj = None
				recipe_obj = eval(buid_command)
				recipe_name = block.replace(nc['module'],'')
				add_on = {recipe_name:recipe_obj}
				self.recipes_dict.update(add_on)

				print('Build successfully {}'.format(buid_command))
				# ----------------------
				# Postcode--------------
				# ----------------------
				cmds.select(block)
				print('Postcode {}'.format(block))
				if postcode:
					try:
						exec(postcode)
					except:
						mel.eval(postcode)

			#Errors
			except Exception:
				import traceback
				traceback.print_exc()
				mt.Mutant_logger(mode='stop')
				self.view_log()
				cmds.undoInfo(closeChunk=True)
				if not mt.check_dev_mode():
					cmds.undo()
				if only_progressbar:
					cProgressBarUI.close()
				return

			post_build_nodes = self.get_all_nodes()

			#succes message
			self.ui.bar_label.setText('{}'.format(block))
			self.ui.bar_label.setToolTip('Succesfull build: {}'.format(block))
			self.ui.progressBar.setValue((num + 1))

			#log
			mt.Mutant_logger(mode = 'stop')

			#Stop Block
			if block == 'Stop_Block':
				print ('User Stop')
				cmds.undoInfo(closeChunk=True)
				return

			#put build nodes only in notes
			if not cmds.attributeQuery("notes", n=block, ex=True):
				cmds.addAttr(block, ln="notes", sn="nts", dt="string")
			nodes_dif = self.get_diference_in_nodes(pre_build_nodes, post_build_nodes)
			cmds.setAttr("{}.notes".format(block), nodes_dif, type="string")

		if only_progressbar:
			cProgressBarUI.close()

		#all success message
		print('Mutant Build Complete')
		self.ui.bar_label.setText('Mutant Build Complete')
		self.ui.bar_label.setToolTip('Mutant Build Complete')

		cmds.setAttr('Mutant_Build.v', 0)
		if cmds.objExists('Mutant_Rig'):
			cmds.parent('Mutant_Rig', 'Miscellaneous_Grp')

		#IO
		if load_io:
			ctrls.load_all(path=os.path.join(tempfile.gettempdir(), 'RebuildTempCtrls', 'tempControllers.json'))
			EasySkin.load_all_skins_from(folder_path=os.path.join(tempfile.gettempdir(), 'RebuildTempSkin'))
			# Load parent hierarchy
			temp_folder = os.path.join(tempfile.gettempdir(), 'RebuildTemp')
			skeleton_file = os.path.join(temp_folder, 'skeleton_hierarchy.txt')
			if cmds.objExists('Skeleton'):
				self.load_joint_parents("Skeleton", skeleton_file)

		cmds.undoInfo(closeChunk=True)

	def save_joint_parents(self, group_name, file_path):
		"""
        Save the parent hierarchy of joints under the specified group to a file.
        :param group_name: Name of the group containing the joints.
        :param file_path: File path to save the parent hierarchy information.
        """
		joints = cmds.listRelatives(group_name, ad=True, type='joint') or []
		parent_dict = {}

		for joint in joints:
			parent = cmds.listRelatives(joint, parent=True)
			if parent:
				parent_dict[joint] = parent[0]

		with open(file_path, 'w') as file:
			for joint, parent in parent_dict.items():
				file.write(f"{joint},{parent}\n")

	def load_joint_parents(self, group_name, file_path):
		"""
        Load the parent hierarchy of joints from the provided file and apply to the joints under the specified group.
        :param group_name: Name of the group containing the joints.
        :param file_path: File path containing the parent hierarchy information.
        """
		with open(file_path, 'r') as file:
			parent_dict = {}
			for line in file:
				joint, parent = line.strip().split(',')
				parent_dict[joint] = parent

		for joint, parent in parent_dict.items():
			if cmds.objExists(joint) and cmds.objExists(parent):
				try:
					cmds.parent(joint, parent)
				except:
					pass

	#-------------------------------------------------------------------

	def get_all_nodes(self):
		return cmds.ls('*')

	def get_diference_in_nodes(self, new_list, old_list):
		dif = set(old_list).difference(set(new_list))
		return dif

	def check_if_previous_build(self):

		build_grp = 'Mutant_Tools_Grp'
		if cmds.objExists(build_grp):
			delete_comfirm = cmds.confirmDialog(
				title='Delete current build?',
				message='Are you sure you want to rebuild?',
				button=['Delete and Rebuild', 'Just Rebuild', 'Cancel'],
				defaultButton='Delete and Rebuild',
				dismissString='Cancel',
				cancelButton='Cancel')

			if delete_comfirm == 'Delete and Rebuild':

				if cmds.listRelatives('Mutant_Build', p=True):
					cmds.parent('Mutant_Build', w=True)

				#IO

				# Skeleton Hierarchy
				if cmds.objExists('Skeleton'):
					temp_folder = os.path.join(tempfile.gettempdir(), 'RebuildTemp')
					if not os.path.exists(temp_folder):
						os.mkdir(temp_folder)
					skeleton_file = os.path.join(temp_folder, 'skeleton_hierarchy.txt')
					# Save parent hierarchy to file
					self.save_joint_parents("Skeleton", skeleton_file)


				# Controllers
				temp_controllers_folder = os.path.join(tempfile.gettempdir(), 'RebuildTempCtrls')
				if not os.path.exists(temp_controllers_folder):
					os.mkdir(temp_controllers_folder)
				ctrls.save_all(folder_path=os.path.join(temp_controllers_folder, 'tempControllers.json'),
							   force_validate=True)

				#Skins
				temp_skin_folder = os.path.join(tempfile.gettempdir(), 'RebuildTempSkin')
				if not os.path.exists(temp_skin_folder):
					os.mkdir(temp_skin_folder)
				else:
					try:
						import shutil
						shutil.rmtree(temp_skin_folder)
						print('Deleted: ', temp_skin_folder)
					except:
						pass
				if not os.path.exists(temp_skin_folder):
					os.mkdir(temp_skin_folder)
				EasySkin.save_all_skins_to(folder_path=temp_skin_folder)

				#Delete
				cmds.delete(build_grp)
				if cmds.objExists('Mutant_Rig'):
					cmds.delete('Mutant_Rig')

				return temp_skin_folder, temp_controllers_folder

			elif delete_comfirm == 'Just Rebuild':
				return 'Just Rebuild'

			else:
				return False
		else:
			return 'First Build'


	#-------------------------------------------------------------------
	def check_precode(self, block):

		config = cmds.listConnections(block)[1]

		# Precode and Postcode attrs Code
		if cmds.getAttr('{}.precode'.format(config)) != '':
			self.ui.prebuild.setIcon(QtGui.QIcon(os.path.join(IconsPath ,'PRECODE_ON.png')))
		else:
			self.ui.prebuild.setIcon(QtGui.QIcon(os.path.join(IconsPath ,'PRECODE.png')))

	#-------------------------------------------------------------------
	def check_postcode(self, block):

		config = cmds.listConnections(block)[1]

		# Precode and Postcode attrs Code
		if cmds.getAttr('{}.postcode'.format(config)) != '':
			self.ui.postbuild.setIcon(QtGui.QIcon(os.path.join(IconsPath ,'POSTCODE_ON.png')))
		else:
			self.ui.postbuild.setIcon(QtGui.QIcon(os.path.join(IconsPath ,'POSTCODE.png')))

	#-------------------------------------------------------------------

	def edit_prebuild_code(self, block):

		config = cmds.listConnections(block)[1]

		#get past code
		pastcode_attr = cmds.getAttr('{}.precode'.format(config))

		try:
			codeUI.close()
		except:
			pass
		reload(load_codeReader)
		codeUI = load_codeReader.Code_Reader(mode='write', code= pastcode_attr, config_attr = '{}.precode'.format(config))
		codeUI.set_path_label(code_path = '{}.precode'.format(config))
		codeUI.show()

	#-------------------------------------------------------------------

	def view_build_code(self, block):

		config = cmds.listConnections(block)[1]

		import_command = cmds.getAttr('{}.Import_Command'.format(config))
		build_file = import_command.replace('import ', '')

		current_path = os.path.join(FOLDER, 'Blocks')
		script_name = build_file + '.py'

		# if we need find it first
		for root, dirs, files in os.walk(current_path):
			for name in files:
				if name == script_name:
					file_path = os.path.abspath(os.path.join(root, name))

		with open(file_path) as build_data:
			build_script = build_data.read()

		try:
			codeUI.close()
		except:
			pass
		reload(load_codeReader)
		codeUI = load_codeReader.Code_Reader(mode='view', code= build_script, config_attr = '')
		codeUI.set_path_label(code_path = file_path)
		codeUI.show()
	#-------------------------------------------------

	def edit_postbuild_code(self, block):
		config = cmds.listConnections(block)[1]

		#get past code
		postcode_attr = cmds.getAttr('{}.postcode'.format(config))

		try:
			codeUI.close()
		except:
			pass

		reload(load_codeReader)
		codeUI = load_codeReader.Code_Reader(mode='write', code= postcode_attr, config_attr = '{}.postcode'.format(config))
		codeUI.set_path_label(code_path = '{}.postcode'.format(config))
		codeUI.show()
	#-------------------------------------------------------------------

	def view_log(self):

		log_file = mt.Mutant_logger(mode = 'log')
		with open(log_file) as log_data:
			log = log_data.read()

		#log
		try:
			log_ui.close()
		except:
			pass

		print(log)

		reload(load_codeReader)
		log_ui = load_codeReader.Code_Reader(mode='view', code='', config_attr='')
		log_ui.previous_code = log
		log_ui.modify_ui_based_on_mode()
		log_ui.ui.code_text.verticalScrollBar().setValue(log_ui.ui.code_text.verticalScrollBar().maximum())
		log_ui.set_path_label(code_path = os.path.join(cmds.internalVar(usd=True),'Mutant_log.txt'))
		log_ui.show()

	#-------------------------------------------------------------------

	def search_command(self):
		self.delete_side_buttons()
		self.create_all_side_buttons()

	def show_bar_only(self):
		self.ui.menuLayout.setParent(None)
		self.ui.tabs.setParent(None)
		self.ui.side_scroll.setParent(None)
		self.ui.attrs_layout.setParent(None)
		self.ui.code_layout.setParent(None)
		self.ui.build_layout.setParent(None)
		self.ui.build_btn.setParent(None)
		self.ui.build_method.setParent(None)
		self.ui.search_layout.setParent(None)
		self.adjustSize()    
		self.show()

	#-------------------------------------------------------------------

	# CLOSE EVENTS _________________________________
	def closeEvent(self, event):

		#delete the script job created for the loading of the UI
		try:
			cmds.scriptJob(kill=self.mutant_sj)
			print ('ScripJob deleted')
			#cmds.scriptJob(ka=1)
		except:
			pass

		print ('Mutant_Tools Autorigger Closed')
#-------------------------------------------------------------------

if __name__ == "__main__":

	try:
		AutoRigger_ui.close() # pylint: disable=E0601
		AutoRigger_ui.deleteLater()
	except:
		pass
	AutoRigger_ui = AutoRigger()
	AutoRigger_ui.show()

#-------------------------------------------------------------------

print('''
#Import Menu
import Mutant_Tools
import Mutant_Tools.Utils
from Mutant_Tools.Utils import mt_menu
reload(Mutant_Tools.Utils.mt_menu)
mt_menu.create_mutant_menu()
mt_menu.put_in_userSetup()

#Import Main Mutant Tools
import imp
from imp import reload
import Mutant_Tools
import Mutant_Tools.Utils
from Mutant_Tools.Utils.Rigging import main_mutant
reload(Mutant_Tools.Utils.Rigging.main_mutant)
mt = main_mutant.Mutant()
''')

