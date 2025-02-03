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
from Mutant_Tools.UI.MayaClose import load_maya_close
reload(load_maya_close)

try:cCloseUI.close()
except:pass
cCloseUI = load_maya_close.CloseUI()
cCloseUI.show()


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


# -------------------------------------------------------------------

# QT WIndow!
FOLDER_NAME = 'MayaClose'
Title = 'Please Click The Button'
UI_File = 'MayaClose.ui'

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


class CloseUI(QtMutantWindow.Qt_Mutant):

	def __init__(self):
		super(CloseUI, self).__init__()

		self.setWindowTitle(Title)

		self.designer_loader_child(path=os.path.join(FOLDER, 'UI', FOLDER_NAME), ui_file=UI_File)
		self.set_title(Title)

		self.create_layout()
		self.create_connections()

		self.setFixedSize(500, 500)

		self.close_sj = cmds.scriptJob(event=["SelectionChanged", self.close_script_job])

	# -------------------------------------------------------------------

	def create_layout(self):
		"""

		Returns:

		"""
		self.ui.red_button.setIcon(QtGui.QIcon(os.path.join(IconsPath ,'red.png')))


	def create_connections(self):
		"""

		Returns:

		"""

		self.ui.red_button.clicked.connect(self.close_cmd)

	def close_cmd(self):
		close_promp = cmds.confirmDialog(
			title='Do it at your own risk',
			message='Do You really want to do it?',
			button=['OK', 'Cancel'],
			defaultButton='OK',
			cancelButton='Cancel',
			dismissString='Cancel')

		if close_promp == 'OK':
			self.close()
			self.create_progress_bar()

	def create_progress_bar(self):
		import random
		cmds.progressWindow(title='Bye Bye...', progress=0, status='Progress (stepped by 1): 0%%',
							isInterruptable=True)
		limit = 10
		step = 1
		for i in range(limit):
			progress = 100.0 / limit * i
			if progress % step:
				continue
			cmds.progressWindow(e=1, progress=progress, status='Deleting everything...')
			# the following is to simulate some processing time
			import time
			time.sleep(0.25)
		cmds.progressWindow(endProgress=1)

		import webbrowser
		url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
		webbrowser.open(url, new=True, autoraise=True)


		cmds.quit(force=True)

	# -------------------------------------------------------------------

	def close_script_job(self):
		''
		self.show()
		try:
			import importlib;
			from importlib import reload
		except:
			import imp;
			from imp import reload

		import Mutant_Tools
		from Mutant_Tools.UI.MayaClose import load_maya_close
		reload(load_maya_close)

		try:
			cCloseUI.close()
		except:
			pass
		cCloseUI = load_maya_close.CloseUI()
		#cCloseUI.show()
		import random
		cCloseUI.move(random.randint(0, 1600), random.randint(0, 1600))


	# CLOSE EVENTS _________________________________
	def exit_ui(self):
		import random
		self.move(random.randint(0, 1600), random.randint(0, 1600))

# -------------------------------------------------------------------

if __name__ == "__main__":

	try:
		cCloseUI.close()  # pylint: disable=E0601
		cCloseUI.deleteLater()
	except:
		pass
	cCloseUI = CloseUI()
	cCloseUI.show()

# -------------------------------------------------------------------

'''
#Notes






'''