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
from Mutant_Tools.UI.Shelves import load_shelves
reload(load_shelves)

try:cShelvesUI.close()
except:pass
cShelvesUI = load_shelves.ShelvesUI()
cShelvesUI.show()

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
import Mutant_Tools

from pathlib import Path
from Mutant_Tools.Utils.Helpers.decorators import undo

from Mutant_Tools.UI.Shelves import shelves_utils
reload(shelves_utils)
cShelves = shelves_utils.Shelves()

# -------------------------------------------------------------------

# QT WIndow!
FOLDER_NAME = 'Shelves'
Title = 'Shelves'
UI_File = 'Shelves.ui'

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


class ShelvesUI(QtMutantWindow.Qt_Mutant):

	def __init__(self):
		super(ShelvesUI, self).__init__()

		self.new_layouts = []

		self.setWindowTitle(Title)

		self.designer_loader_child(path=os.path.join(FOLDER, 'UI', FOLDER_NAME), ui_file=UI_File)
		self.set_title(Title)

		self.create_layout()
		self.create_connections()



	# -------------------------------------------------------------------

	def create_layout(self):
		"""

		Returns:

		"""
		self.create_files_layout()
		self.ui.explorer_button.setIcon(QtGui.QIcon(os.path.join(IconsPath, 'explorer.png')))

	def create_connections(self):
		"""

		Returns:

		"""

		self.ui.save_button.clicked.connect(self.save)
		self.ui.export_sel_button.clicked.connect(self.export_sel)
		self.ui.open_button.clicked.connect(self.open)
		self.ui.import_button.clicked.connect(self.import_file)
		self.ui.reference_button.clicked.connect(self.reference)
		self.ui.explorer_button.clicked.connect(self.open_explorer)

	# -------------------------------------------------------------------

	def open_explorer(self):
		cShelves.open_shelves_in_explorer()

	def save(self):
		name = self.ui.name_line.text()
		cShelves.save_file(name=name)
		cShelves.create_image()

		self.create_files_layout()

	def export_sel(self):
		name = self.ui.name_line.text()
		cShelves.export_sel(name=name)
		cShelves.create_image()

		self.create_files_layout()

	def create_files_layout(self):

		self.clean_layout()
		self.new_layouts = []

		files = cShelves.list_shelved_files()
		files = sorted(files)
		files_chunks = list(self.divide_chunks(files, 4))

		for chunk in files_chunks:
			side_hbox = QtWidgets.QGroupBox()
			self.ui.files_layout.addWidget(side_hbox)
			h_layout = QtWidgets.QHBoxLayout()
			side_hbox.setLayout(h_layout)
			h_layout.setContentsMargins(1, 1, 1, 1)
			side_hbox.setContentsMargins(1, 1, 1, 1)
			side_hbox.setStyleSheet("border : 0px solid grey; ")

			self.new_layouts.append(side_hbox)

			for file in chunk:

				file_name = self.get_file_name(file)

				file_button = QtWidgets.QPushButton()
				file_button.setStyleSheet("""
										QPushButton {
											background-color: none; 
											border: 0px solid black;
										}
										QPushButton:hover {
										background-color: grey;
										}
										}
										""")
				file_button.setFixedSize(90, 90)
				h_layout.addWidget(file_button)
				file_button.setToolTip(file_name)

				file_button.clicked.connect(partial(self.put_path_in_line, file))

				icon_path = os.path.join(cShelves.folder, file_name.replace('ma', '1.jpg'))
				print(icon_path)
				if os.path.isfile(icon_path):
					file_button.setIcon(QtGui.QIcon(icon_path))
					file_button.setIconSize((QtCore.QSize(70, 70)))
					file_button.setText(file_name)
				else:
					file_button.setText(file_name)

	def clean_layout(self):

		if self.new_layouts:
			for l in self.new_layouts:
				l.setParent(None)

	def divide_chunks(self, l, n):
		# looping till length l
		for i in range(0, len(l), n):
			yield l[i:i + n]

	def put_path_in_line(self, file):
		self.ui.path_line.setText(file)
		print(file)

	def get_file_name(self, path):
		return os.path.basename(path)

	def open(self):
		file_path = self.ui.path_line.text()
		cShelves.open_file(file_path)

	def import_file(self):
		file_path = self.ui.path_line.text()
		cShelves.import_file(file_path)


	def reference(self):
		file_path = self.ui.path_line.text()
		cShelves.reference_file(file_path)

	# CLOSE EVENTS _________________________________
	def closeEvent(self, event):
		''


# -------------------------------------------------------------------

if __name__ == "__main__":

	try:
		cShelvesUI.close()  # pylint: disable=E0601
		cShelvesUI.deleteLater()
	except:
		pass
	cShelvesUI = ShelvesUI()
	cShelvesUI.show()

# -------------------------------------------------------------------

'''
#Notes






'''