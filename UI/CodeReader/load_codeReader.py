from __future__ import absolute_import
'''
version: 1.0.0

#----------------
content: 

#----------------
how to: 

import Mutant_Tools
from Mutant_Tools.UI.CodeReader import load_codeReader
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

reload(load_codeReader)

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
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import sys
import json
import subprocess
from pathlib import Path

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

import Mutant_Tools.UI
from Mutant_Tools.UI import QtMutantWindow

reload(QtMutantWindow)
Qt_Mutant = QtMutantWindow.Qt_Mutant()

#-------------------------------------------------------------------

#QT WIndow!
UI_File = 'codeReader.ui'
IconsPath =  os.path.join(FOLDER, 'Icons')
Title = 'Code Reader'
#-------------------------------------------------------------------



class Code_Reader(QtMutantWindow.Qt_Mutant):

	def __init__(self, mode = 'view', code = '', config_attr = ''):
		super(Code_Reader, self).__init__()

		#self.setWindowTitle(Title)
		self.resize(680,475)

		self.designer_loader_child(path=os.path.join(FOLDER, 'UI','CodeReader'), ui_file=UI_File)
		self.set_title('Title')

		self.create_layout()
		self.create_connections()

		self.previous_code = code
		self.mode = mode
		self.config_attr = config_attr

		self.modify_ui_based_on_mode()
		self.code_path = 'local'

	#-------------------------------------------------------------------

	def create_layout(self):

		self.ui.layout().setContentsMargins(3, 3, 3, 3)

	def create_connections(self):

		self.ui.close_btn.clicked.connect(self.close)
		self.ui.sizeSlider.valueChanged.connect(lambda: self.change_font_size(self.ui.sizeSlider.value()))
		#self.ui.code_text.textChanged.connect(self.slider_changed)
		self.ui.down_button.clicked.connect(self.slider_changed)

	#-------------------------------------------------------------------

	def modify_ui_based_on_mode(self):

		#print(self.mode)
		if self.mode == 'view':
			self.ui.python_radio.setParent(None)
			self.ui.mel_radio.setParent(None)
			self.ui.code_text.setPlainText(self.previous_code)
		else:
			self.ui.code_text.setPlainText(self.previous_code)

		try:
			self.ui.code_text.verticalScrollBar().maximum()
		except:
			pass

	def slider_changed(self):
		self.ui.code_text.verticalScrollBar().setValue(self.ui.code_text.verticalScrollBar().maximum())

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

