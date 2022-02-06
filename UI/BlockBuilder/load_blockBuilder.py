'''
version: 1.0.0

#----------------
content:

#----------------
how to:

import imp
import Mutant_Tools
from Mutant_Tools.UI.BlockBuilder import load_blockBuilder
import imp
imp.reload(load_blockBuilder)

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
import imp
import sys
import json
import glob
import pprint
from pathlib import Path

from collections import OrderedDict

#-------------------------------------------------------------------

#Read name conventions as nc[''] and setup as setup['']
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
FOLDER = os.path.join(*PATH.parts[:-2], 'Config')

JSON_FILE = os.path.join(PATH, 'name_conventions.json')
with open(JSON_FILE) as json_file:
	nc = json.load(json_file)
#Read curve shapes info
CURVE_FILE = os.path.join(PATH, 'curves.json')
with open(CURVE_FILE) as curve_file:
	curve_data = json.load(curve_file)
#setup File
SETUP_FILE = os.path.join(PATH, 'rig_setup.json')
with open(SETUP_FILE) as setup_file:
	setup = json.load(setup_file)



#-------------------------------------------------------------------

#QT WIndow!
PATH = os.path.dirname(__file__)
OTHERS_PATH = PATH.replace('\\UI\\BlockBuilder', '//Others') #get presets path to read files
BLOCKS_PATH = PATH.replace('\\UI\\BlockBuilder', '//Blocks') #get Blocks paths to write files

Title = 'Mutant // Block Builder'
Folder = PATH.replace('\\UI\\BlockBuilder', '')
UI_File = 'blockBuilder.ui'
IconsPath =  Folder + '//Icons//'
#-------------------------------------------------------------------

import Mutant_Tools
import Mutant_Tools.Utils
from Mutant_Tools.Utils.Rigging import main_mutant
imp.reload(Mutant_Tools.Utils.Rigging.main_mutant)
mt = main_mutant.Mutant()

import Mutant_Tools.UI
from Mutant_Tools.UI import QtMutantWindow
imp.reload(QtMutantWindow)
Qt_Mutant = QtMutantWindow.Qt_Mutant()

#-------------------------------------------------------------------


def maya_main_window(dockable=True):

	main_window_ptr = omui.MQtUtil.mainWindow()
	return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class BlockBuilder(QtMutantWindow.Qt_Mutant):

	def __init__(self):
		super(BlockBuilder, self).__init__()

		self.setWindowTitle(Title)

		self.designer_loader_child(path = Folder + '/UI/BlockBuilder/', ui_file = UI_File)
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
		self.close()

	def create_config(self):

		#grab the main info
		name = self.ui.name_line.text()
		description = self.ui.description_line.text()
		icon = self.ui.icon_line.text()

		if self.ui.presets_radio.isChecked():
			tab = '01_Presets'
		elif self.ui.biped_radio.isChecked():
			tab = '02_Biped'
		elif self.ui.facial_radio.isChecked():
			tab = '03_Facial'
		elif self.ui.animals_radio.isChecked():
			tab = '04_Animals'
		elif self.ui.clothes_radio.isChecked():
			tab = '05_Clothes'
		elif self.ui.props_radio.isChecked():
			tab = '06_Props'
		elif self.ui.games_radio.isChecked():
			tab = '07_Games'
		elif self.ui.data_radio.isChecked():
			tab = '08_Data'
		else :
			tab = '09_Other'


		#create the config dic with ordered dict so it can mantain the order we desire
		block_data = OrderedDict()

		block_data['Name'] =         name
		block_data['Description'] =  description
		block_data['Icon'] =         icon + '.png'

		block_data['Enable'] =       'True'

		block_data['python_file'] =  'exec_{}.py'.format(name.lower())
		block_data['import'] =       'import exec_{}'.format(name.lower())
		block_data['imp.reload'] =   'imp.reload(exec_{})'.format(name.lower())
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
		all_blocks = glob.glob('{}//{}//*json'.format(BLOCKS_PATH, tab))
		pprint.pprint(all_blocks)

		if all_blocks:
			last_block = all_blocks[-1]
			last_num = last_block.split('\\')[-1].split('_')[0]
			print (last_num)
			new_num = '0' + str(int(last_num[1]) + 1)
		else:
			new_num=0

		#write json file
		with open('{}//{}//{}_{}.json'.format(BLOCKS_PATH, tab, new_num, name), 'w') as new_config:
			json.dump(block_data, new_config, indent=4, sort_keys = False)

		pprint.pprint(block_data)

		#open exec python file and change it to fit new one

		if self.ui.simple_block.isChecked():
			base_python_preset = OTHERS_PATH + '//exec_block.py'
		else:
			base_python_preset = OTHERS_PATH + '//exec_block_sides.py'

		with open(base_python_preset) as exec_block:
			exec_code = exec_block.read()

		new_exec_code = exec_code.replace("TAB_FOLDER = 'TAB'", "TAB_FOLDER = '{}'".format(tab))
		new_exec_code = new_exec_code.replace("PYBLOCK_NAME = 'exec_NAME'", "PYBLOCK_NAME = 'exec_{}'".format(name.lower()))
		new_exec_code = new_exec_code.replace("create_NAME_block(name = 'NAME')", "create_{}_block(name = '{}')".format(name.lower(),name))
		new_exec_code = new_exec_code.replace("#create_NAME_block()", "#create_{}_block()".format(name.lower()))
		new_exec_code = new_exec_code.replace("def build_NAME_block():", "def build_{}_block():".format(name.lower()))
		new_exec_code = new_exec_code.replace("#build_NAME_block()", "#build_{}_block()".format(name.lower()))

		new_exec_code = new_exec_code.replace("/num_name.json", "/{}_{}.json".format(new_num, name))
		new_exec_code = new_exec_code.replace("icon = 'ICON_NAME'", "icon = '{}'".format(icon))

		print (new_exec_code)

		#write .py file

		with open('{}//{}//exec_{}.py'.format(BLOCKS_PATH, tab, name.lower()), 'w') as new_py:
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