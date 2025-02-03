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
from Mutant_Tools.UI.FileCleaner import load_file_cleaner
reload(load_file_cleaner)

try:cCleanerUI.close()
except:pass
cCleanerUI = load_file_cleaner.CleanerUI()
cCleanerUI.show()

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
import subprocess
import tempfile

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
FOLDER_NAME = 'FileCleaner'
Title = 'File Cleaner'
UI_File = 'FileCleaner.ui'

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


class CleanerUI(QtMutantWindow.Qt_Mutant):

	def __init__(self):
		super(CleanerUI, self).__init__()

		self.setWindowTitle(Title)

		self.designer_loader_child(path=os.path.join(FOLDER, 'UI', FOLDER_NAME), ui_file=UI_File)
		self.set_title(Title)

		self.create_layout()
		self.create_connections()
		self.resize(800, 450)

	# -------------------------------------------------------------------

	def create_layout(self):
		"""

		Returns:

		"""


	def create_connections(self):
		"""

		Returns:

		"""

		self.ui.plugin_manager_button.clicked.connect(self.open_plugin_manager)
		self.ui.clean_arnold.clicked.connect(self.clean_arnold)
		self.ui.import_arnold_button.clicked.connect(self.import_cleaned_arnold_scene)



	# -------------------------------------------------------------------
	def open_plugin_manager(self):
		mel.eval('PluginManager;')

	def clean_arnold(self):
		temp_path = os.path.join(tempfile.gettempdir(), 'Arnold_Clean')
		dirt_temp_file = os.path.join(temp_path, 'dirty_scene.ma')
		clean_temp_file = os.path.join(temp_path, 'clean_scene.ma')
		if not os.path.exists(temp_path):
			os.makedirs(temp_path)
		cmds.file(rename=dirt_temp_file)
		cmds.file(save=True, type="mayaAscii")

		self.remove_line_from_ma(dirt_temp_file, 'mtoa', clean_temp_file)

		#command = "maya"
		#subprocess.Popen([command], stdout=subprocess.PIPE)

		cmds.quit(f=True)

	def remove_line_from_ma(self, file_path, word, output_path):
		# Open the input file for reading
		with open(file_path, 'r') as input_file:
			# Read all lines from the input file
			lines = input_file.readlines()

		# Open the output file for writing
		with open(output_path, 'w') as output_file:
			# Write lines to the output file, excluding those containing the specified word
			for line in lines:
				if word not in line:
					output_file.write(line)

		print(output_path)
		clipboard = QtWidgets.QApplication.clipboard()
		clipboard.setText(output_path)

		return output_path

	def import_cleaned_arnold_scene(self):
		temp_path = os.path.join(tempfile.gettempdir(), 'Arnold_Clean')
		clean_temp_file = os.path.join(temp_path, 'clean_scene.ma')
		print(clean_temp_file)

		cmds.file(clean_temp_file, open=True, f=True)

		self.deleteUnknownNodes()
		cmds.file(save=True, type="mayaAscii")

	def deleteUnknownNodes(self):
		# 2 things to take care of:
		#   1) you can't delete nodes from references.
		#   2) "delete" will delete all children nodes (hierarchy) in default.
		unknown = cmds.ls(type="unknown")
		unknown = [node for node in unknown if not cmds.referenceQuery(node, isNodeReferenced=True)]

		for node in unknown:
			if not cmds.objExists(node):
				continue
			cmds.delete(node)

	# CLOSE EVENTS _________________________________
	def closeEvent(self, event):
		''


# -------------------------------------------------------------------

if __name__ == "__main__":

	try:
		cCleanerUI.close()  # pylint: disable=E0601
		cCleanerUI.deleteLater()
	except:
		pass
	cCleanerUI = CleanerUI()
	cCleanerUI.show()

# -------------------------------------------------------------------

'''
#Notes






'''