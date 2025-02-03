from __future__ import absolute_import, division
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
from Mutant_Tools.UI.ProgressBar import load_progress_bar
reload(load_progress_bar)

try:cProgressBarUI.close()
except:pass
cProgressBarUI = load_progress_bar.ProgressBarUI(items=['a', 'b', 'c'], title='Barrita')
cProgressBarUI.show()

cProgressBarUI.set_percent(2)

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
FOLDER_NAME = 'ProgressBar'
Title = 'Progress Bar'
UI_File = 'ProgressBar.ui'

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


class ProgressBarUI(QtMutantWindow.Qt_Mutant):

	def __init__(self, items=[], title=Title):
		super(ProgressBarUI, self).__init__()

		self.setWindowTitle(title)

		self.designer_loader_child(path=os.path.join(FOLDER, 'UI', FOLDER_NAME), ui_file=UI_File)
		self.set_title(title)

		self.create_layout()
		self.create_connections()

		self.items = items
		self.max_value = self.max_value = len(items)
		self.set_max_value()

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


	def set_percent(self, value):

		if value+1 > self.max_value:
			self.end_progress()
			return True

		self.ui.bar.setValue(value)
		percent = (float(value)/float(self.max_value))*100
		percent = "{:.2f}".format(percent)
		self.ui.percent.setText(str(percent)+'%')
		self.set_text(value)
		cmds.refresh()
		return True

	def set_text(self, value):
		text = self.items[value]
		self.ui.text.setText(str(text))

	def end_progress(self):
		self.close()

	def set_max_value(self):
		self.ui.bar.setMaximum(self.max_value)


	# -------------------------------------------------------------------

	# CLOSE EVENTS _________________________________
	def closeEvent(self, event):
		''


# -------------------------------------------------------------------

if __name__ == "__main__":

	try:
		cProgressBarUI.close()  # pylint: disable=E0601
		cProgressBarUI.deleteLater()
	except:
		pass
	cProgressBarUI = ProgressBarUI()
	cProgressBarUI.show()

# -------------------------------------------------------------------

'''
#Notes

cmds.progressWindow(title='Mutant Tools', progress=0, status='Loading Mutant...',
					isInterruptable=True, maxValue=len(blocks_folders))

for num, block_folder in enumerate(blocks_folders):

	if block_folder in avoid_folders:
		continue
	cmds.progressWindow(e=1, progress=num, status=block_folder)

cmds.progressWindow(endProgress=1)


'''