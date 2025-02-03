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
from Mutant_Tools.UI.AssetsRigger import load_AssetsRigger
reload(load_AssetsRigger)

try:cAssetsRiggerUI.close()
except:pass
cAssetsRiggerUI = load_AssetsRigger.AssetsRiggerUI()
cAssetsRiggerUI.show()

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

from autoRig import core02
reload(core02)



# -------------------------------------------------------------------

# QT WIndow!
FOLDER_NAME = 'AssetsRigger'
Title = 'Assets Rigger'
UI_File = 'AssetsRigger.ui'

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


class AssetsRiggerUI(QtMutantWindow.Qt_Mutant):

	def __init__(self):
		super(AssetsRiggerUI, self).__init__()

		self.setWindowTitle(Title)

		self.designer_loader_child(path=os.path.join(FOLDER, 'UI', FOLDER_NAME), ui_file=UI_File)
		self.set_title(Title)

		self.create_layout()
		self.create_connections()

		self.user = ''

	# -------------------------------------------------------------------

	def create_layout(self):
		"""

		Returns:

		"""
		self.get_user_name()
		self.get_shows_from_user()
		self.populate_combo_box()


	def create_connections(self):
		"""

		Returns:

		"""
		self.ui.load_current_user.clicked.connect(self.get_user_name)
		self.ui.search_line.returnPressed.connect(self.populate_combo_box)
		self.ui.user_line.textChanged.connect(self.populate_combo_box)
		self.ui.load_current_user.clicked.connect(self.populate_user_field)
		self.ui.show_combo.currentIndexChanged.connect(self.populate_combo_box)
		self.ui.autorig_button.clicked.connect(self.autorig_asset)

		self.ui.autorig_current_button.clicked.connect(self.autorig_current)
		self.ui.create_rig_sid.clicked.connect(self.create_rig_sid)
		self.ui.create_base_only.clicked.connect(self.create_base_only)

	# -------------------------------------------------------------------

	def get_user_name(self):

		try:
			from star.entities import Asset, Task, User
			self.user = User.find_current()
		except:
			self.user=None

	def get_shows_from_user(self):
		self.get_user_name()
		if self.user:
			projects = self.user.projects
			prjs = []
			for p in projects:
				prjs.append(p.name)
			self.ui.show_combo.addItems(prjs)
			try:self.ui.show_combo.setCurrentIndex(1)
			except:pass

	def populate_user_field(self):
		if self.user:
			user = self.user.login
		else:
			user = '*'
		self.ui.user_line.setText(user)

	def get_assets_by_user(self, user):
		if self.user:
			tasks = self.user.tasks
			task_names = []
			for t in tasks:
				task_names.append(t.asset.name)
			return task_names

	def get_all_assets(self):

		try:
			from star.entities import Project
			proj_name = self.ui.show_combo.currentText()
			print(proj_name)
			proj = Project.findby_name(proj_name)
			assets = []
			for ass in proj.assets:
				assets.append(ass.name)
			return assets
		except Exception as e:
			print(e)
			pass

	def populate_combo_box(self):

		self.ui.assets_combo.clear()

		search = self.ui.search_line.text()

		user_input = self.ui.user_line.text()
		if user_input == '*' or not user_input:
			assets = self.get_all_assets()
		else:
			assets = self.get_assets_by_user(user=user_input)
		if not assets:
			return

		assets = sorted(assets)

		#filter search
		filter_assets = []
		for a in assets:
			if search.lower() in a.lower():
				filter_assets.append(a)
		assets=filter_assets

		#remove duplicates
		clean_assets = []
		for a in assets:
			if a not in clean_assets:
				clean_assets.append(a)
		assets=clean_assets

		self.ui.assets_combo.addItems(assets)

	@undo
	def autorig_asset(self, asset=None, show=None):
		cmds.file(new=True, force=True)
		if not asset:
			asset = self.ui.assets_combo.currentText()
		if not show:
			show = self.ui.show_combo.currentText()

		scale_check = self.ui.scales_combo_users.isChecked()
		core02.build_auto_rig(asset, skin=False, show_name=show, scale_multiply=0.75, extra_scales=scale_check)

	@undo
	def autorig_current(self):
		scale_check = self.ui.scales_combo.isChecked()
		core02.build_auto_rig(skin=False, scale_multiply=0.75, rig_current_scene=True, extra_scales=scale_check)

	# -------------------------------------------------------------------

	def create_rig_sid(self):
		core02.create_sid_node()

	def create_base_only(self):
		mt.check_is_there_is_base()

	# CLOSE EVENTS _________________________________
	def closeEvent(self, event):
		''


# -------------------------------------------------------------------

if __name__ == "__main__":

	try:
		cAssetsRiggerUI.close()  # pylint: disable=E0601
		cAssetsRiggerUI.deleteLater()
	except:
		pass
	cAssetsRiggerUI = AssetsRiggerUI()
	cAssetsRiggerUI.show()

# -------------------------------------------------------------------

'''
#Notes






'''