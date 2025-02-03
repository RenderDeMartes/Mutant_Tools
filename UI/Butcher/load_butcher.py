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
from Mutant_Tools.UI.Butcher import load_butcher
reload(load_butcher)

try:cButcherUI.close()
except:pass
cButcherUI = load_butcher.ButcherUI()
cButcherUI.show()

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
FOLDER_NAME = 'Butcher'
Title = 'Butcher'
UI_File = 'Butcher.ui'

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


class ButcherUI(QtMutantWindow.Qt_Mutant):

	def __init__(self):
		super(ButcherUI, self).__init__()

		self.setWindowTitle(Title)

		self.designer_loader_child(path=os.path.join(FOLDER, 'UI', FOLDER_NAME), ui_file=UI_File)
		self.set_title(Title)

		self.create_layout()
		self.create_connections()

		self.body_parts_path = os.path.join(FOLDER, 'UI', FOLDER_NAME, 'BodyParts')
		self.assets = []

	# -------------------------------------------------------------------

	def create_layout(self):
		"""

		Returns:

		"""
		self.populate_asset_box()

	def create_connections(self):
		"""

		Returns:

		"""

		self.ui.search_line.textChanged.connect(self.populate_asset_box)
		self.ui.load_button.clicked.connect(self.reference_asset)
		self.ui.remove_parts_button.clicked.connect(self.remove_all_references)

		self.ui.ref_all_button.clicked.connect(self.reference_all)

		self.ui.match_button.clicked.connect(self.match_guides)
		self.ui.match_sel_button.clicked.connect(self.match_selection)


	# -------------------------------------------------------------------

	def populate_asset_box(self):

		self.ui.pieces_box.clear()
		search_text = self.ui.search_line.text()

		assets = glob.glob(os.path.join(FOLDER, 'UI', FOLDER_NAME, 'BodyParts', '*'))
		clean_list=[]
		for a in assets:
			cPath = Path(a)
			asset = cPath.parts[-1]

			if search_text:
				if search_text.lower() in str(asset).lower():
					clean_list.append(asset)
			else:
				clean_list.append(asset)

		self.ui.pieces_box.addItems(clean_list)
		self.assets = clean_list

	def reference_asset(self, asset=None):
		if not asset:
			asset = self.ui.pieces_box.currentText()

		asset_path = os.path.join(self.body_parts_path, asset)
		cmds.file(asset_path, ignoreVersion=True, namespace='Butcher', mergeNamespacesOnClash=True, r=True)

		grp = self.create_temp_group()
		cmds.select('Butcher:*')
		butcher_parts = cmds.ls(sl=True)
		for p in butcher_parts:
			parent_grp = cmds.listRelatives(p, p=True)
			if not parent_grp:
				if 'Block' in p:
					print(p)
					cmds.select(p)
					cmds.parent(p, grp)

	def reference_all(self):

		self.assets = [self.ui.pieces_box.itemText(i) for i in range(self.ui.pieces_box.count())]
		print(self.assets)
		if self.assets:
			for asset in self.assets:
				self.reference_asset(asset=asset)

	def match_guides(self, asset=None):
		if not cmds.objExists('Butcher_Grp'):
			return False

		if not asset:
			asset=cmds.listRelatives('Butcher_Grp', c=True)[0]

		parents = []

		for i in cmds.listRelatives(asset, ad=True):
			print(i, i.replace('Butcher:', ''))
			try:
				pc=cmds.parentConstraint(i, i.replace('Butcher:', ''))
				parents.append(pc[0])
			except Exception as e:
				print(e)
		if parents:
			cmds.delete(parents)
		print(asset)

	def match_selection(self):
		sel = cmds.ls(sl=True)[0]
		if not 'Block' in sel:
			return False

		self.remove_all_references(exception=sel)

		self.match_guides(asset=sel)


	def create_temp_group(self):
		if cmds.objExists('Butcher_Grp'):
			return 'Butcher_Grp'

		grp = cmds.group(n = 'Butcher_Grp', em=True)
		return grp

	def remove_all_references(self, exception=None):
		if not cmds.objExists('Butcher_Grp'):
			return False

		guides = cmds.listRelatives('Butcher_Grp', c=True)
		if guides:
			for guide in guides:
				if exception:
					if guide == exception:
						continue
				ref = cmds.referenceQuery(guide, filename=True)
				cmds.file(ref, rr=True)
		cmds.delete('Butcher_Grp')

	def match_sel_guide(self, mult=1.1):
		''

	

	# -------------------------------------------------------------------

	# CLOSE EVENTS _________________________________
	def closeEvent(self, event):
		''


# -------------------------------------------------------------------

if __name__ == "__main__":

	try:
		cButcherUI.close()  # pylint: disable=E0601
		cButcherUI.deleteLater()
	except:
		pass
	cButcherUI = ButcherUI()
	cButcherUI.show()

# -------------------------------------------------------------------

'''
#Notes






'''