from __future__ import absolute_import
'''
version: 1.0.0
date: 21/04/2020

#----------------
content:

This will create a UI for the autorriger menu tool.

#----------------
how to:

import Mutant_Tools
from Mutant_Tools.UI.RigTools.Tabs import load_RenameTab
reload(load_RenameTab)

try:cRename_ui.close()
except:pass
cRename_ui = load_RenameTab.RenameTab()
cRename_ui.show()

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
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as omui
from functools import partial
# import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel
from pathlib import Path

import os
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import sys
import json

try:from urllib.request import Request, urlopen
except:pass

import Mutant_Tools
from Mutant_Tools.UI.WebsiteViewer import load_website_viewer
reload(load_website_viewer)
viewer = load_website_viewer.WebsiteViewerUI()

from Mutant_Tools.Utils.Helpers import helpers
reload(Mutant_Tools.Utils.Helpers.helpers)
mh = helpers.Helpers()

from Mutant_Tools.Utils.IO import SkinUtils
reload(Mutant_Tools.Utils.IO.SkinUtils)
skin = SkinUtils.Skinning()

from Mutant_Tools.Utils.IO import NgSkinUtils
reload(Mutant_Tools.Utils.IO.NgSkinUtils)
ngmt = NgSkinUtils.NG_Mutant()

from Mutant_Tools.Utils.IO import CtrlUtils
reload(Mutant_Tools.Utils.IO.CtrlUtils)
ctrls = CtrlUtils.Ctrls()

from Mutant_Tools.Utils.IO import Guides
reload(Mutant_Tools.Utils.IO.Guides)
guides = Guides.Guides()

import Mutant_Tools.Utils.Helpers
from Mutant_Tools.Utils.Helpers import helpers
reload(Mutant_Tools.Utils.Helpers.helpers)
mh = helpers.Helpers()

from Mutant_Tools.Utils.IO import SkinUtils
reload(SkinUtils)
ms = SkinUtils.Skinning()

import Mutant_Tools
import Mutant_Tools.Utils
from Mutant_Tools.Utils.Rigging import main_mutant

reload(Mutant_Tools.Utils.Rigging.main_mutant)
mt = main_mutant.Mutant()

# -------------------------------------------------------------------

#Read name conventions as nc[''] and setup as setup['']
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-3]
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

# -------------------------------------------------------------------

#QT WIndow!
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-3]
FOLDER=''
for p in PATH_PARTS:
	FOLDER = os.path.join(FOLDER, p)
PATH = os.path.join(FOLDER, 'UI')

ICONS_FOLDER = os.path.join(FOLDER,'Icons')

Title = 'Rename-Tab'
UI_File = 'Rename.ui'



# -------------------------------------------------------------------

def maya_main_window():
	main_window_ptr = omui.MQtUtil.mainWindow()
	return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class RenameTab(QtWidgets.QDialog):

	def __init__(self, parent=maya_main_window()):
		super(RenameTab, self).__init__(parent)

		self.setWindowTitle(Title)

		self.init_ui()
		self.create_layout()
		self.create_connections()

	def init_ui(self):
		UIPath = os.path.join(FOLDER,'UI','RigTools','Tabs',UI_File)
		f = QtCore.QFile(os.path.join(UIPath))
		f.open(QtCore.QFile.ReadOnly)

		loader = QtUiTools.QUiLoader()
		self.ui = loader.load(f, parentWidget=self)

		f.close()

	# -------------------------------------------------------------------

	def create_layout(self):
		self.populate_all_combos()

		
	# -------------------------------------------------------------------

	def create_connections(self):
		self.ui.RenameBtn.clicked.connect(self.rename)
		self.ui.prefixBtn.clicked.connect(self.add_prefix)
		self.ui.sufixBtn.clicked.connect(self.add_sufix)
		self.ui.ChangeNameBtn.clicked.connect(lambda: self.search_replace(hierarchy=False))
		self.ui.ChangeNameBtn2.clicked.connect(lambda: self.search_replace(hierarchy=True))

		self.ui.right.clicked.connect(lambda: self.quick_prefix(text=nc['right']))
		self.ui.left.clicked.connect(lambda: self.quick_prefix(text=nc['left']))

		self.ui.ctrl.clicked.connect(lambda: self.quick_sufix(text=nc['ctrl']))
		self.ui.joint.clicked.connect(lambda: self.quick_sufix(text=nc['joint']))

		self.ui.prefix_combo.currentTextChanged.connect(lambda: self.ui.prefix_line.setText(nc[self.ui.prefix_combo.currentText()]))
		self.ui.sufix_combo.currentTextChanged.connect(lambda: self.ui.sufix_line.setText(nc[self.ui.sufix_combo.currentText()]))

	def populate_all_combos(self):

		to_add =[]
		for name in nc:
			to_add.append(name)

		self.ui.prefix_combo.addItems(to_add)
		self.ui.sufix_combo.addItems(to_add)

	def assing_temp_name(self, node):
		if not node:
			return
		import random
		cmds.select(node)
		new_name = cmds.rename(cmds.ls(sl=True)[0], 'aa'+str(random.randint(0,999)))
		return new_name

	def rename(self, nodes=[]):

		cmds.undoInfo(openChunk=True)
		if not nodes:
			nodes=cmds.ls(sl=True)
		new_sel = []
		for num, node in enumerate(nodes):
			search = self.assing_temp_name(node)
			replace = self.ui.NewNameLineEdit.text()
			if self.ui.RenameNumCheckBox.isChecked():
				replace = replace + '_' + str(num)
			mel.eval('searchReplaceNames {} {} "selected"'.format(search, replace))
			new_sel.append(replace)
		cmds.select(new_sel)
		cmds.undoInfo(closeChunk=True)

	def add_sufix(self, nodes=[]):

		cmds.undoInfo(openChunk=True)
		if not nodes:
			nodes=cmds.ls(sl=True)
		new_sel = []
		for num, node in enumerate(nodes):
			search = node
			replace = search + '_' + self.ui.sufix_line.text()
			cmds.rename(search, replace)
			new_sel.append(replace)
		cmds.select(new_sel)
		cmds.undoInfo(closeChunk=True)

	def add_prefix(self, nodes=[]):

		cmds.undoInfo(openChunk=True)
		if not nodes:
			nodes=cmds.ls(sl=True)
		new_sel = []
		for num, node in enumerate(nodes):
			search = node
			replace = self.ui.prefix_line.text() + '_' +search
			cmds.rename(search, replace)
			new_sel.append(replace)
		cmds.select(new_sel)
		cmds.undoInfo(closeChunk=True)

	def search_replace(self, hierarchy=False):

		cmds.undoInfo(openChunk=True)
		for num, node in enumerate(cmds.ls(sl=True)):
			cmds.select(node)
			search = self.ui.SearchLineEdit.text()
			replace = self.ui.ReplaceLineEdit.text()
			if hierarchy:
				mel.eval('searchReplaceNames {} {} "hierarchy"'.format(search, replace)) #hierarchy
			else:
				mel.eval('searchReplaceNames {} {} "selected"'.format(search, replace)) #hierarchy
		cmds.undoInfo(closeChunk=True)

	def quick_prefix(self, text=''):
		if not text:
			return

		self.ui.prefix_line.setText(text)
		self.add_prefix()

	def quick_sufix(self, text=''):
		if not text:
			return

		self.ui.sufix_line.setText(text)
		self.add_sufix()


	# CLOSE EVENTS _________________________________
	def closeEvent(self, event):
		''


# -------------------------------------------------------------------

if __name__ == "__main__":

	try:
		RenameTab.close()  # pylint: disable=E0601
		RenameTab.deleteLater()
	except:
		pass
	cRename_ui = RenameTab()
	cRename_ui.show()

# -------------------------------------------------------------------

