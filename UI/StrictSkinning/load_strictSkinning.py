from __future__ import absolute_import
'''
version: 1.0.0
date: 21/04/2020

#----------------
content:

#----------------
how to:

try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import Mutant_Tools
from Mutant_Tools.UI.StrictSkinning import load_strictSkinning
reload(load_strictSkinning)

try:cStrictSkinning.close()
except:pass
cStrictSkinning = load_strictSkinning.StrictSkinning()
cStrictSkinning.show()

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
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import sys
import json
import glob
import pprint
from pathlib import Path
from Mutant_Tools.Utils.Helpers.decorators import undo


# -------------------------------------------------------------------

# QT WIndow!
FOLDER_NAME = 'StrictSkinning'
Title = 'Strict Skinning'
UI_File = 'strictSkinning.ui'

# QT WIndow!
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-2]
FOLDER=''
for f in PATH_PARTS:
	FOLDER = os.path.join(FOLDER, f)

IconsPath = os.path.join(FOLDER, 'Icons')



# -------------------------------------------------------------------

import Mutant_Tools
import Mutant_Tools.Utils
from Mutant_Tools.Utils.Rigging import main_mutant

reload(Mutant_Tools.Utils.Rigging.main_mutant)
mt = main_mutant.Mutant()

import Mutant_Tools.UI
from Mutant_Tools.UI import QtMutantWindow
reload(QtMutantWindow)
Qt_Mutant = QtMutantWindow.Qt_Mutant()

# -------------------------------------------------------------------


def maya_main_window():
	main_window_ptr = omui.MQtUtil.mainWindow()
	return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class StrictSkinning(QtMutantWindow.Qt_Mutant):

	def __init__(self):
		super(StrictSkinning, self).__init__()

		self.setWindowTitle(Title)

		self.designer_loader_child(path=os.path.join(FOLDER, 'UI', FOLDER_NAME), ui_file=UI_File)
		self.set_title(Title)

		self.create_layout()
		self.create_connections()

		self.bind_joints = []

	# -------------------------------------------------------------------

	def reload(self):
		self.populate_combos()
		self.populate_layout()

	def create_layout(self):
		"""

		Returns:

		"""
		self.populate_layout()
		self.populate_combos()


	def create_connections(self):
		"""

		Returns:

		"""

		self.ui.reload_button.clicked.connect(self.reload)

	def populate_layout(self):
		layout = self.ui.buttons_layout

	def populate_combos(self):
		left_combo = self.ui.left_combo
		right_combo = self.ui.right_combo

	# -------------------------------------------------------------------

	# CLOSE EVENTS _________________________________
	def closeEvent(self, event):
		''


# -------------------------------------------------------------------

if __name__ == "__main__":

	try:
		cStrictSkinning.close()  # pylint: disable=E0601
		cStrictSkinning.deleteLater()
	except:
		pass
	cStrictSkinning = StrictSkinning()
	cStrictSkinning.show()

# -------------------------------------------------------------------

'''
#Notes






'''