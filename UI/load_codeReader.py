'''
version: 1.0.0
date: 21/04/2020

#----------------
content: 

This will create a UI for the autorriger tool. Is dinamically created based on the .json files inside the folders

#----------------
how to: 

import Mutant_Tools
from Mutant_Tools.UI import load_codeReader
import imp
imp.reload(load_codeReader)

try:codeUI.close()
except:pass
codeUI = load_codeReader.Code_Reader(mode = 'view', code = 'Test')
codeUI.show()
codeUI.get_code
codeUI.close()

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
#import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel

import os
import imp
import sys
import json
import subprocess

#-------------------------------------------------------------------

#Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = PATH.replace('\\UI', '//Config') #change this path depending of the folder

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


#-------------------------------------------------------------------

#QT WIndow!
PATH = os.path.dirname(__file__)

Title = 'Code Reader'
Folder = PATH.replace('\\UI', '') #where the qt designer file is
UI_File = 'codeReader.ui'
IconsPath =  Folder + '/Icons/' #icons path

#-------------------------------------------------------------------


def maya_main_window(dockable=True):

	main_window_ptr = omui.MQtUtil.mainWindow()
	return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class Code_Reader(QtWidgets.QMainWindow):

	def __init__(self, parent=maya_main_window(), mode = 'view', code = '', config_attr = ''):
		super(Code_Reader, self).__init__(parent)

		#self.setWindowTitle(Title)
		self.resize(680,475)

		self.init_ui()
		self.create_layout()
		self.create_connections()

		self.previous_code = code
		self.mode = mode
		self.config_attr = config_attr

		self.modify_ui_based_on_mode()
		self.code_path = 'local'

		#self.move_top_right()

	def init_ui(self):

		UIPath  = Folder + '/UI/'
		f = QtCore.QFile(UIPath + UI_File)
		f.open(QtCore.QFile.ReadOnly)

		loader = QtUiTools.QUiLoader()
		self.ui = loader.load(f, parentWidget=self)

		f.close()
	#-------------------------------------------------------------------

	def move_top_right(self):

		top_right = QApplication.desktop().availableGeometry().topRight()
		self.move(top_right)

	def create_layout(self):

		self.ui.layout().setContentsMargins(3, 3, 3, 3)

	def create_connections(self):

		self.ui.close_btn.clicked.connect(self.close)
		self.ui.sizeSlider.valueChanged.connect(lambda: self.change_font_size(self.ui.sizeSlider.value()))

	#-------------------------------------------------------------------

	def modify_ui_based_on_mode(self):

		print(self.mode)
		if self.mode == 'view':
			self.ui.python_radio.setParent(None)
			self.ui.mel_radio.setParent(None)
			self.ui.code_text.setPlainText(self.previous_code)
		else:
			self.ui.code_text.setPlainText(self.previous_code)

	@property
	def get_code (self):
		return self.ui.code_text.toPlainText()

	def change_font_size(self, size):
		self.ui.code_text.setFont(QtGui.QFont('Arial', size))

	def set_path_label(self, code_path):
		self.ui.path_ui.setText(code_path)
		self.ui.explorer.setIcon(QtGui.QIcon(IconsPath + 'explorer.png'))
		print (code_path)
		if '/' in code_path or '\\' in code_path:
			self.ui.explorer.clicked.connect(lambda: subprocess.call('explorer /select, {}'.format(code_path.replace('/', '\\'), shell=True)))
		else:
			self.ui.path_ui.setParent(None)
			self.ui.explorer.setParent(None)

	# CLOSE EVENTS _________________________________
	def closeEvent(self, event):
		if self.mode == 'view':
			return None
		else:
			cmds.setAttr('{}'.format(self.config_attr), self.get_code, type = 'string')
			print (self.config_attr)

#-------------------------------------------------------------------

if __name__ == "__main__":

	try:
		Code_Reader.close() # pylint: disable=E0601
		Code_Reader.deleteLater()
	except:
		pass
	Code_Reader = name()
	Code_Reader.show()

#-------------------------------------------------------------------

