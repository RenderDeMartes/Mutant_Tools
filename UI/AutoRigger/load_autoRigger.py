'''
version: 1.0.0
date: 21/04/2020

#----------------
content:

This will create a UI for the autorriger tool. Is dinamically created based on the .json files inside the folders

#----------------
how to:
import imp
import Mutant_Tools
from Mutant_Tools.UI.AutoRigger import load_autoRigger
imp.reload(load_autoRigger)

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
#import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel

import os
import imp
import sys
import json
from collections import OrderedDict

from Mutant_Tools.UI.AutoRigger import load_autoRiggerMenu
imp.reload(load_autoRiggerMenu)

from Mutant_Tools.UI.CodeReader import load_codeReader
imp.reload(load_codeReader)

import Mutant_Tools.UI
from Mutant_Tools.UI import QtMutantWindow
imp.reload(QtMutantWindow)

import Mutant_Tools.UI.CustomWidgets.expandableWidget as expandableWidget
imp.reload(expandableWidget)

from Mutant_Tools.Utils.Helpers import helpers
imp.reload(Mutant_Tools.Utils.Helpers.helpers)
mh = helpers.Helpers()

#-------------------------------------------------------------------

#Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = PATH.replace('\\UI\\AutoRigger', '//Config') #change this path depending of the folder

JSON_FILE = (PATH + '/name_conventions.json')
with open(JSON_FILE) as json_file:
	nc = json.load(json_file)
#Read curve shapes info
CURVE_FILE = (PATH + '/curves.json')
with open(CURVE_FILE) as curve_file:
	curve_data = json.load(curve_file)
#setup File
SETUP_FILE = (PATH+'/rig_setup.json')
with open(SETUP_FILE) as setup_file:
	setup = json.load(setup_file)
#version File
VERSION_FILE = (PATH+'/version.json')
with open(VERSION_FILE) as version_file:
	version = json.load(version_file)

#-------------------------------------------------------------------

#QT WIndow!
PATH = os.path.dirname(__file__)

Title = 'Auto_Rigger'
Folder = PATH.replace('\\UI\\AutoRigger', '')
UI_File = 'autoRigger.ui'
IconsPath =  Folder + '/Icons/'

#-------------------------------------------------------------------

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
imp.reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()

import Mutant_Tools.UI.CustomWidgets.expandableWidget as expandableWidget
imp.reload(expandableWidget)

#-------------------------------------------------------------------
def add_sys_folders_remove_compiled():
	#get all the paths for the blocks in the sys path
	file_path = (str(__file__))
	for folder in os.listdir(Folder + '/Blocks'):
		blocks_path = Folder + '/Blocks//{}'.format(folder)
		if blocks_path not in sys.path:
			sys.path.append(blocks_path)

	#Delete all pyc in the block folders so we dont need the imp.reload in the codes:
	path = Folder + '//Blocks'
	for path, subdirs, files in os.walk(path):
		for name in files:
			#print('Search: ' + os.path.join(path, name))
			if '.pyc' in str(name):
				#print (name + ': Have been deleted')
				os.remove(os.path.join(path, name))
			if '__pycache__' in str(name):
				#print (name + ': Have been deleted')
				os.remove(os.path.join(path, name))

	# also remove pyc from UIs folder
	path = Folder
	for path, subdirs, files in os.walk(path):
		for name in files:
			if '.pyc' in str(name):
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

		self.resize(605, 652)

		#load blocks folders to sys and remove all the compiled info in BLOCKS and UI Folder
		add_sys_folders_remove_compiled()

		self.designer_loader_child(path=Folder + '/UI/AutoRigger/', ui_file=UI_File)

		self.create_menus()
		self.create_layout()
		self.create_connections()
		try:OpenMaya.MGlobal.displayInfo('♥')
		except:pass

		#08_Data init
		self.current_block = None
		self.current_block_folder = None

		#update icons
		mt.update_icons()

	#-------------------------------------------------------------------
	def create_menus(self):

		self.menu = load_autoRiggerMenu.AutoRiggerMenu()
		self.ui.menuLayout.addWidget(self.menu)
		self.search_button = QPushButton()
		#self.search_button.setFixedSize(20,20)
		#self.ui.menuLayout.addWidget(self.search_button)

	def create_layout(self):
		self.create_block_buttons()
		self.delete_side_buttons()

		self.create_all_side_buttons()

		try:self.ui.layout().setContentsMargins(3, 3, 3, 3)
		except:pass
		self.ui.progressBar.setValue(0)
		self.ui.bar_label.setText('Mutant')

		#set Manual Icons
		self.ui.prebuild.setIcon(QtGui.QIcon(IconsPath + 'PRECODE.png'))
		self.ui.current_code.setIcon(QtGui.QIcon(IconsPath + 'CODE.png'))
		self.ui.postbuild.setIcon(QtGui.QIcon(IconsPath + 'POSTCODE.png'))
		self.ui.reload_ui.setIcon(QtGui.QIcon(IconsPath + 'RELOAD.png'))
		self.ui.log.setIcon(QtGui.QIcon(IconsPath + 'LOG.png'))


	def reload_ui(self):
		self.create_layout()
		OpenMaya.MGlobal.displayInfo('♥')

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


	#-------------------------------------------------------------------
	def create_block_buttons(self):

		#first we delete all the previews items on the layouts
		for i in reversed(range(self.ui.presets_layout.count())):
			self.ui.presets_layout.itemAt(i).widget().setParent(None)
		for i in reversed(range(self.ui.biped_layout.count())):
			self.ui.biped_layout.itemAt(i).widget().setParent(None)
		for i in reversed(range(self.ui.facial_layout.count())):
			self.ui.facial_layout.itemAt(i).widget().setParent(None)
		for i in reversed(range(self.ui.animals_layout.count())):
			self.ui.animals_layout.itemAt(i).widget().setParent(None)
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
		#print ('Relaod UI')
		#print (Folder)
		blocks_folders = os.listdir(Folder + '\\Blocks')
		#blocks_folders = ['01_Presets', '02_Biped']
		#print ('Block Folders : ' + str(blocks_folders))

		for block_folder in blocks_folders:

			clean_folder_name = block_folder.split('_')[1]
			files = os.listdir(Folder + '/Blocks/' + block_folder )

			for block_file in files:
				#print(block_file)

				if not '.json' in str(block_file): #if the file is not a json continue with the next one
					#print ('skiped' + block_file)
					continue
				#read the json file with block information
				real_path =  Folder + '/Blocks/' + block_folder + '/' + block_file
				#print (real_path)

				with open(real_path, "r") as block_info:
					block = json.load(block_info)
					#reaload with json files info if dev mode is on, off loads faster
					if version['dev_mode'] == 'On':
						exec(block['import'])
						exec(block['imp.reload'])
						#print ('reloading {}'.format(block_file))

				#create button
				block_name = str(block_file).split('_')[1].replace('.json', '')
				button = QPushButton()#give a nicer name
				button.clicked.connect(partial (self.create_new_block, real_path))
				button.clicked.connect(self.create_layout)
				button.setToolTip(block['Description'])
				try:
					button.setIcon(QtGui.QIcon(IconsPath + block['Icon']))
					button.setIconSize((QtCore.QSize(35, 35)))
					button.setStyleSheet("text-align:right;")
					#button.setText(block_name)
				except:
					button.setText(block_name)

				if block['Enable'] == 'False':
					button.setEnabled(False)

				#parent to correct tab
				if block_folder == '01_Presets':
					self.ui.presets_layout.addWidget(button)
				elif block_folder == '02_Biped':
					self.ui.biped_layout.addWidget(button)
				elif block_folder == '03_Facial':
					self.ui.facial_layout.addWidget(button)
				elif block_folder == '04_Animals':
					self.ui.animals_layout.addWidget(button)
				elif block_folder == '05_Clothes':
					self.ui.clothes_layout.addWidget(button)
				elif block_folder == '06_Props':
					self.ui.props_layout.addWidget(button)
				elif block_folder == '07_Games':
					self.ui.games_layout.addWidget(button)
				elif block_folder == '08_Data':
					self.ui.data_layout.addWidget(button)
				else:
					self.ui.other_layout.addWidget(button)

				button.setFixedSize(40, 40)

	#-------------------------------------------------------------------
	def create_new_block(self,bock_path):

		#this will create a new block in maya based on the info on the json files
		#read json
		with open(bock_path, "r") as block_info:
			block = json.load(block_info)

		cmds.undoInfo(openChunk=True)

		exec (block['import'])
		try:exec (block['imp.reload'])
		except: print ('couldnt imp.reload {}'.format(bock_path))
		exec (block['exec_command'])
		self.create_properties_layout(block = cmds.ls(sl=True)[0])

		cmds.undoInfo(closeChunk=True)

	#-------------------------------------------------------------------
	def delete_side_buttons(self):

		# this will clear the side layout so we can move stuff around
		for i in reversed(range(self.ui.side_layout.count())):
			self.ui.side_layout.itemAt(i).widget().setParent(None)

		self.ui.side_scroll.setWidgetResizable(True)

	def delete_side_buttonblock(self, block):

		delete_comfirm = cmds.confirmDialog(
						title='Name Block',
						message='Are you sure you want to delete: {}'.format(block),
						button=['Delete', 'Cancel'],
						defaultButton='Delete',
						dismissString='Cancel',
						cancelButton = 'Cancel')

		if delete_comfirm == 'Delete':
			cmds.delete(block)

		self.create_layout()

	#-------------------------------------------------------------------

	def create_all_side_buttons(self):
		if cmds.objExists('Mutant_Build'):
			for num, child in enumerate(cmds.listRelatives('Mutant_Build', c=True)):
				if not child.endswith(nc['module']):
					colapsable_box = expandableWidget.expandableWidget(parent=self.ui.side_layout, title=child.replace('_Build', ''))
					grand_childs = cmds.listRelatives(child, c=True)
					#if not childs in group pass else parent sde button to group
					if grand_childs is None:
						continue
					else:
						for grand_child in grand_childs:
							self.create_side_button(pack_name=grand_child, index=num, block_parent=colapsable_box.layout)
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
		#up_button = QtWidgets.QPushButton('↑')
		up_button = QtWidgets.QPushButton()
		up_button.setIcon(QtGui.QIcon(IconsPath + 'Up.png'))
		#down_button = QtWidgets.QPushButton('↓')
		down_button = QtWidgets.QPushButton()
		down_button.setIcon(QtGui.QIcon(IconsPath + 'Down.png'))
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


		delete_button = QtWidgets.QPushButton()
		delete_button.setFixedSize(15,15)
		delete_button.setIcon(QtGui.QIcon(IconsPath + 'delete.png'))
		delete_button.setToolTip('Delete: {}'.format(pack_name))

		h_layout = QtWidgets.QHBoxLayout()
		v_layout = QtWidgets.QVBoxLayout()

		v_layout.addWidget(up_button)
		v_layout.addWidget(delete_button)
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
		delete_button.clicked.connect(partial (self.delete_side_buttonblock, pack_name))

	#-------------------------------------------------------------------
	def create_properties_layout(self, block):
		#'Create All Properties Stuff'
		#self.create_layout()

		# this will clear the proprieties layout so we can recreate stuff
		for i in reversed(range(self.ui.properties_layout.count())):
			self.ui.properties_layout.itemAt(i).widget().setParent(None)

		#collect data for opening logs and codes
		self.current_block = block
		print (self.current_block)

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
					set_button.setFixedSize(80,35)
					set_button.clicked.connect(partial(self.lineEdit_get_selection,line_edit, edit_attr))
					h_layout.addWidget(set_button)

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
		#remove ugly lists keys
		nice_selection = str(sel).replace("[", "")
		nice_selection = str(nice_selection).replace("]", "")
		nice_selection = str(nice_selection).replace("'", "")

		field.setText(nice_selection)
		cmds.setAttr(attr, nice_selection, type = 'string')

	def lineEdit_get_file(self, field, attr, *args):
		path = mh.import_window(extension=".json")
		field.setText(path)
		cmds.setAttr(attr, path, type='string')

	def lineEdit_get_path(self, field, attr, *args):
		path = mh.folder_window()
		field.setText(path)
		cmds.setAttr(attr, path, type='string')

	def slider_update_attr(self, label, slider,attr, *args):
		cmds.setAttr(attr, slider.value())
		label.setText(str(slider.value()))

	def checkBox_update_attr(self, checkBox,attr, *args):
		cmds.setAttr(attr, checkBox.isChecked())

	def enum_update_attr(self, comboBox, attr, *args):
		cmds.setAttr(attr, comboBox.currentIndex())

	#-------------------------------------------------------------------

	def get_blocks_to_build(self):
		to_build = []
		blocks = cmds.listRelatives('Mutant_Build', c=True)
		for child in blocks:
			if not child.endswith(nc['module']):
				grand_childs = cmds.listRelatives(child, c=True)
				for grand_child in grand_childs:
					to_build.append(grand_child)
			else:
				to_build.append(child)

		return to_build

	#-------------------------------------------------------------------
	def build_autorigger(self):

		self.ui.bar_label.setText('Starting the Build')

		cmds.undoInfo(openChunk=True)

		#log
		try:
			cmds.scriptEditorInfo(ch=True)
			mt.Mutant_logger(mode = 'clear')
			mt.Mutant_logger(mode = 'stop')
		except:
			pass

		#build
		blocks = self.get_blocks_to_build()
		progress_max = len(blocks)
		self.ui.progressBar.setMaximum(progress_max)
		#select each block and run the build command and make progress bar move
		for num, block in enumerate(blocks):

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
			buid_command = cmds.getAttr('{}.Build_Command'.format(config))
			postcode = cmds.getAttr('{}.postcode'.format(config))

			self.ui.bar_label.setText(buid_command)
			self.ui.bar_label.setToolTip(buid_command)

			exec(import_command)
			print ('Import successfully {}'.format(import_command))
			#if error in build show log and stop log writing
			try:
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
				exec(buid_command)
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
				if version['dev_mode'] != 'On':
					cmds.undo()
				return

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

		#all success message
		print('Mutant Build Complete')
		self.ui.bar_label.setText('Mutant Build Complete')
		self.ui.bar_label.setToolTip('Mutant Build Complete')

		cmds.setAttr('Mutant_Build.v', 0)

		cmds.undoInfo(closeChunk=True)

	#-------------------------------------------------------------------
	def check_precode(self, block):

		config = cmds.listConnections(block)[1]

		# Precode and Postcode attrs Code
		if cmds.getAttr('{}.precode'.format(config)) != '':
			self.ui.prebuild.setIcon(QtGui.QIcon(IconsPath + 'PRECODE_ON.png'))
		else:
			self.ui.prebuild.setIcon(QtGui.QIcon(IconsPath + 'PRECODE.png'))

	#-------------------------------------------------------------------
	def check_postcode(self, block):

		config = cmds.listConnections(block)[1]

		# Precode and Postcode attrs Code
		if cmds.getAttr('{}.postcode'.format(config)) != '':
			self.ui.postbuild.setIcon(QtGui.QIcon(IconsPath + 'POSTCODE_ON.png'))
		else:
			self.ui.postbuild.setIcon(QtGui.QIcon(IconsPath + 'POSTCODE.png'))

	#-------------------------------------------------------------------

	def edit_prebuild_code(self, block):

		config = cmds.listConnections(block)[1]

		#get past code
		pastcode_attr = cmds.getAttr('{}.precode'.format(config))

		try:
			codeUI.close()
		except:
			pass

		codeUI = load_codeReader.Code_Reader(mode='write', code= pastcode_attr, config_attr = '{}.precode'.format(config))
		codeUI.set_path_label(code_path = '{}.precode'.format(config))
		codeUI.show()

	#-------------------------------------------------------------------

	def view_build_code(self, block):

		config = cmds.listConnections(block)[1]

		import_command = cmds.getAttr('{}.Import_Command'.format(config))
		build_file = import_command.replace('import ', '')

		current_path = Folder + '//Blocks'
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
			codeUI.close()
		except:
			pass

		codeUI = load_codeReader.Code_Reader(mode='view', code= log, config_attr = '')
		codeUI.ui.code_text.verticalScrollBar().setValue(codeUI.ui.code_text.verticalScrollBar().maximum())
		codeUI.set_path_label(code_path =  PATH.replace('\\UI', '/log.txt'))
		codeUI.show()

	#-------------------------------------------------------------------

	# CLOSE EVENTS _________________________________
	def closeEvent(self, event):

		#delete the script job created for the realding of the UI
		try:
			cmds.scriptJob(kill=Mutant_sj)
			print ('ScripJob deleted')
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


'''
#create script Job for laoding the UI
def Mutant_script_job():
	try:
		sel = cmds.ls(sl=True)[-1]
		if str(sel).endswith('_Block'):
			self.create_layout()
	except:pass
Mutant_sj = cmds.scriptJob(event=["SelectionChanged", Mutant_script_job])
	   

#cmds.scriptJob(kill=Mutant_sj)
#cmds.scriptJob(ka=1)


'''