'''
version: 1.0.0
date: 21/04/2020

#----------------
content:

#----------------
how to:

import imp
import Mutant_Tools
from Mutant_Tools.UI.FolderName import load_pyname
import imp
imp.reload(load_pyname)

try:cMutantUI.close()
except:pass
cMutantUI = load_pyname.MutantUI()
cMutantUI.show()

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
# -------------------------------------------------------------------
from shiboken2 import wrapInstance
from PySide2 import QtGui, QtCore
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


# -------------------------------------------------------------------

# Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = PATH.replace('\\UI\\FolderName', '//Config')  # change this path depending of the folder

JSON_FILE = (PATH + '/name_conventions.json')
with open(JSON_FILE) as json_file:
	nc = json.load(json_file)
# Read curve shapes info
CURVE_FILE = (PATH + '/curves.json')
with open(CURVE_FILE) as curve_file:
	curve_data = json.load(curve_file)
# setup File
SETUP_FILE = (PATH + '/rig_setup.json')
with open(SETUP_FILE) as setup_file:
	setup = json.load(setup_file)

# -------------------------------------------------------------------

# QT WIndow!
PATH = os.path.dirname(__file__)
OTHERS_PATH = PATH.replace('\\UI\\FolderName', '//Others')  # get presets path to read files
BLOCKS_PATH = PATH.replace('\\UI\\FolderName', '//Blocks')  # get Blocks paths to write files

Title = 'Mutant || Mutant'
Folder = PATH.replace('\\UI\\FolderName', '')
UI_File = 'blockBuilder.ui'
IconsPath = Folder + '//Icons//'
# -------------------------------------------------------------------

import Mutant_Tools
import Mutant_Tools.Utils
from Mutant_Tools.Utils.Rigging import main_mutant

imp.reload(Mutant_Tools.Utils.Rigging.main_mutant)
mt = main_mutant.Mutant()

import Mutant_Tools.UI
from Mutant_Tools.UI import QtMutantWindow
imp.reload(QtMutantWindow)
Qt_Mutant = QtMutantWindow.Qt_Mutant()


# -------------------------------------------------------------------


def maya_main_window():
	main_window_ptr = omui.MQtUtil.mainWindow()
	return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class MutantUI(QtMutantWindow.Qt_Mutant):

	def __init__(self):
		super(MutantUI, self).__init__()

		self.setWindowTitle(Title)

		self.designer_loader_child(path=Folder + '/UI/FolderName/', ui_file=UI_File)
		self.set_title('Block Builder')

		self.create_layout()
		self.create_connections()

	# -------------------------------------------------------------------

	def create_layout(self):
		"""

		Returns:

		"""


	def create_connections(self):
		"""

		Returns:

		"""

		#self.ui.button.clicked.connect(self.create_block)

	# -------------------------------------------------------------------

	# CLOSE EVENTS _________________________________
	def closeEvent(self, event):
		''


# -------------------------------------------------------------------

if __name__ == "__main__":

	try:
		cMutantUI.close()  # pylint: disable=E0601
		cMutantUI.deleteLater()
	except:
		pass
	cMutantUI = MutantUI()
	cMutantUI.show()

# -------------------------------------------------------------------

'''
#Notes






'''