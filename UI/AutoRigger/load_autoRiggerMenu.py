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
from Mutant_Tools.UI.AutoRigger import load_autoRiggerMenu
reload(load_autoRiggerMenu)

try:AutoRiggerMenu.close()
except:pass
menu = load_autoRiggerMenu.AutoRiggerMenu()
menu.show()

#----------------
dependencies:

QT FILE
ICONS
JSON FILES
Main Mutant

#----------------
www.mutanttools.com
author:  Esteban Rodriguez <info@renderdemartes.com>

'''
# -------------------------------------------------------------------
try:
    from shiboken6 import wrapInstance
    from PySide6 import QtGui, QtCore
    from PySide6 import QtUiTools
    from PySide6 import QtWidgets
    from PySide6.QtWidgets import *
except: 
    from shiboken2 import wrapInstance #Compatibility pre 2026
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

from Mutant_Tools.Utils.Rigging import main_mutant
reload(Mutant_Tools.Utils.Rigging.main_mutant)
mt = main_mutant.Mutant()

import Mutant_Tools.Utils.IO
from Mutant_Tools.Utils.IO import EasySkin
reload(Mutant_Tools.Utils.IO.EasySkin)

# -------------------------------------------------------------------

#Read name conventions as nc[''] and setup as setup['']
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

# -------------------------------------------------------------------

#QT WIndow!
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-2]
FOLDER=''
for p in PATH_PARTS:
	FOLDER = os.path.join(FOLDER, p)
PATH = os.path.join(FOLDER, 'UI')

ICONS_FOLDER = os.path.join(FOLDER,'Icons')

Title = 'Menu'
UI_File = 'autoRiggerMenu.ui'



# -------------------------------------------------------------------

def maya_main_window():
	main_window_ptr = omui.MQtUtil.mainWindow()
	return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class AutoRiggerMenu(QtWidgets.QDialog):

	def __init__(self, parent=maya_main_window()):
		super(AutoRiggerMenu, self).__init__(parent)

		self.open_viewer=True
		self.cWebsiteViewer = self.load_viewer()

		self.setWindowTitle(Title)
		self.setFixedHeight(20)

		self.init_ui()
		self.create_layout()
		self.create_connections()

	def load_viewer(self):
		from Mutant_Tools.UI.WebsiteViewer import load_website_viewer
		reload(load_website_viewer)
		viewer = load_website_viewer.WebsiteViewerUI()
		return viewer

	def init_ui(self):
		UIPath = os.path.join(FOLDER,'UI','AutoRigger')
		f = QtCore.QFile(os.path.join(UIPath, UI_File))
		f.open(QtCore.QFile.ReadOnly)

		loader = QtUiTools.QUiLoader()
		self.ui = loader.load(f, parentWidget=self)

		f.close()

	# -------------------------------------------------------------------

	def create_layout(self):

		#create menu bar
		self.menuBar = QtWidgets.QMenuBar()  # requires parent

		# -------------------------------------------------------------------

		#File Menu

		self.fileMenu = QtWidgets.QMenu(self)
		self.fileMenu.setTitle("File")

		self.kanban_board = self.fileMenu.addAction("Kanban Board")
		self.fileMenu.addSeparator()

		# Guides submenu
		self.guidesMenu = QtWidgets.QMenu("Guides", self)
		self.fileMenu.addMenu(self.guidesMenu)

		self.save_guide = self.guidesMenu.addAction("Save Guide")
		self.load_guide = self.guidesMenu.addAction("Load Guide")
		self.guidesMenu.addSeparator()
		self.place_guide = self.guidesMenu.addAction("Guide Placement")
		self.butcher = self.guidesMenu.addAction("Butcher")
		self.fileMenu.addSeparator()

		self.bind_selected = self.fileMenu.addAction("Bind Selected Geo")
		self.download_ng = self.fileMenu.addAction("Download NgSkinToolsV2")
		self.fileMenu.addSeparator()

		# Skins submenu
		self.skinsMenu = QtWidgets.QMenu("Skins", self)
		self.fileMenu.addMenu(self.skinsMenu)

		self.save_skin = self.skinsMenu.addAction("Save All Skins")
		self.load_skin = self.skinsMenu.addAction("Load All Skins")
		self.fast_save_skin = self.skinsMenu.addAction("Fast Save Skin Pack")
		self.fast_load_skin = self.skinsMenu.addAction("Fast Load Skin Pack")
		self.save_sel_skin = self.skinsMenu.addAction("Save Selected Skins")
		self.load_sel_skin = self.skinsMenu.addAction("Load Selected Skins")
		self.skinsMenu.addSeparator()
		self.use_fast_skin = self.skinsMenu.addAction("Use Fast Skin (Rebuild)")
		self.use_fast_skin.setCheckable(True)
		fast_skin_state = cmds.optionVar(q="mutant_use_fast_skin") if cmds.optionVar(ex="mutant_use_fast_skin") else True
		self.use_fast_skin.setChecked(fast_skin_state)

		# Controllers submenu
		self.ctrlsMenu = QtWidgets.QMenu("Controllers", self)
		self.fileMenu.addMenu(self.ctrlsMenu)

		self.save_ctrls = self.ctrlsMenu.addAction("Save Ctrls")
		self.load_ctrls = self.ctrlsMenu.addAction("Load Ctrls")
		self.save_world_ctrls = self.ctrlsMenu.addAction("Save Ctrls World Position")
		self.load_world_ctrls = self.ctrlsMenu.addAction("Load Ctrls World Position")
		self.save_selected_ctrls = self.ctrlsMenu.addAction("Save Selected Ctrls")
		self.load_selected_ctrls = self.ctrlsMenu.addAction("Load Selected Ctrls")
		self.mirror_ctrls = self.ctrlsMenu.addAction("Mirror Ctrls")
		self.mirror_selected_ctrls = self.ctrlsMenu.addAction("Mirror Selected Ctrls")
		self.fileMenu.addSeparator()

		self.dev_reload = self.fileMenu.addAction("Reload Blocks")
		self.update_all_blocks = self.fileMenu.addAction("Update All Blocks")

		self.settingsMenu = QtWidgets.QMenu("Settings", self)
		self.fileMenu.addMenu(self.settingsMenu)

		self.toggle_dev = self.settingsMenu.addAction("Toggle Dev Mode")

		self.settingsMenu.addSeparator()

		self.visual_build = self.settingsMenu.addAction("Visual Build")
		self.visual_build.setCheckable(True)
		visual_build_state = cmds.optionVar(q="mutant_visual_build") if cmds.optionVar(ex="mutant_visual_build") else True
		self.visual_build.setChecked(visual_build_state)

		self.wrap_icons = self.settingsMenu.addAction("Wrap Block Icons")
		self.wrap_icons.setCheckable(True)
		wrap_icons_state = cmds.optionVar(q="mutant_wrap_icons") if cmds.optionVar(ex="mutant_wrap_icons") else True
		self.wrap_icons.setChecked(wrap_icons_state)


		self.clear_script_editor = self.settingsMenu.addAction("Clear Script Editor on Build")
		self.clear_script_editor.setCheckable(True)
		clear_se_state = cmds.optionVar(q="mutant_clear_script_editor") if cmds.optionVar(ex="mutant_clear_script_editor") else True
		self.clear_script_editor.setChecked(clear_se_state)

		self.revert_on_fail = self.settingsMenu.addAction("Revert on Fail")
		self.revert_on_fail.setCheckable(True)
		revert_state = cmds.optionVar(q="mutant_revert_on_fail") if cmds.optionVar(ex="mutant_revert_on_fail") else True
		self.revert_on_fail.setChecked(revert_state)

		self.show_block_tooltips = self.settingsMenu.addAction("Show Block Tooltips")
		self.show_block_tooltips.setCheckable(True)
		tooltips_state = cmds.optionVar(q="mutant_show_block_tooltips") if cmds.optionVar(ex="mutant_show_block_tooltips") else False
		self.show_block_tooltips.setChecked(tooltips_state)

		self.settingsMenu.addSeparator()

		self.standard_window = self.settingsMenu.addAction("Use Standard Window")
		self.standard_window.setCheckable(True)
		std_win_state = cmds.optionVar(q="mutant_standard_window") if cmds.optionVar(ex="mutant_standard_window") else False
		self.standard_window.setChecked(std_win_state)

		self.menuBar.addMenu(self.fileMenu)

		# -------------------------------------------------------------------

		#Help Menu
		self.tutorialMenu = QtWidgets.QMenu()
		self.tutorialMenu.setTitle("Help")

		self.discord = self.main_page = self.tutorialMenu.addAction("Join Discord")
		self.report_bug = self.main_page = self.tutorialMenu.addAction("Report Bug")
		self.request_feature = self.main_page = self.tutorialMenu.addAction("Request Feature")

		self.tutorialMenu.addSeparator()

		self.riggers = self.tutorialMenu.addAction("Riggers")
		self.developers = self.tutorialMenu.addAction("Developers")
		self.tutorialMenu.addSeparator()

		self.main_page = self.tutorialMenu.addAction("Main Page")
		self.menuBar.addMenu(self.tutorialMenu)
		self.tutorialMenu.addSeparator()

		self.open_in_maya = self.tutorialMenu.addAction('Use Website Viewer')
		self.open_in_maya.setCheckable(True)
		self.open_in_maya.setChecked(True)

		self.tutorialMenu.addSeparator()
		self.use_mutant_hotkeys = self.tutorialMenu.addAction('Set Mutant Hotkeys')

		# -------------------------------------------------------------------

		#Donate
		self.donateMenu = QtWidgets.QMenu(self)
		self.donateMenu.setTitle("Donate")
		self.paypal = self.donateMenu.addAction("Paypal")
		self.crypto = self.donateMenu.addAction("Crypto")
		self.menuBar.addMenu(self.donateMenu)

		#add menu bar to layout
		self.ui.menuLayout.insertWidget(0, self.menuBar)

	# -------------------------------------------------------------------

	def create_connections(self):
		#FILE MENU
		self.save_guide.triggered.connect(lambda: guides.export_ma_guide())
		self.load_guide.triggered.connect(lambda: guides.import_ma_guide())
		self.place_guide.triggered.connect(lambda: self.load_guide_placement())
		self.butcher.triggered.connect(lambda: self.load_butcher())

		self.bind_selected.triggered.connect(lambda: skin.bind_to_bnd())
		self.save_skin.triggered.connect(self.save_skins)
		self.load_skin.triggered.connect(self.load_skins)
		self.fast_save_skin.triggered.connect(self.fast_save_skins)
		self.fast_load_skin.triggered.connect(self.fast_load_skins)
		self.save_sel_skin.triggered.connect(self.save_sel_skins)
		self.load_sel_skin.triggered.connect(self.load_sel_skins)

		self.save_ctrls.triggered.connect(lambda: ctrls.save_all())
		self.load_ctrls.triggered.connect(lambda: ctrls.load_all())
		self.save_world_ctrls.triggered.connect(lambda: ctrls.save_world_ctrls())
		self.load_world_ctrls.triggered.connect(lambda: ctrls.load_world_ctrls())
		self.save_selected_ctrls.triggered.connect(lambda: ctrls.save_all(ctrls='Selected'))
		self.load_selected_ctrls.triggered.connect(lambda: ctrls.load_selected())
		self.mirror_ctrls.triggered.connect(lambda: ctrls.mirror_all_ctrl_shapes())
		self.mirror_selected_ctrls.triggered.connect(lambda: ctrls.mirror_all_ctrl_shapes(ctrls='Selected'))

		#HELP MENU
		self.discord.triggered.connect(lambda: self.cWebsiteViewer.open_link('https://discord.gg/pqGeYhUcAW'))
		self.report_bug.triggered.connect(lambda: self.send_bugs())
		self.request_feature.triggered.connect(lambda: self.send_requests())

		self.riggers.triggered.connect(lambda: self.open_website('https://mutanttools.com/riggers/'))
		self.developers.triggered.connect(lambda: self.open_website('https://mutanttools.com/mt_commands/'))
		self.main_page.triggered.connect(lambda: self.open_website('https://mutanttools.com/'))
		self.use_mutant_hotkeys.triggered.connect(self.set_mutant_hotkeys)

		#DONATE MENU
		self.paypal.triggered.connect(lambda: self.open_website('https://www.paypal.com/paypalme/renderdemartes'))
		self.crypto.triggered.connect(lambda: self.open_website('https://mutanttools.com/donate/'))

		#Dev Mode
		self.toggle_dev.triggered.connect(lambda: mt.toggle_dev_mode())

		#Kanban Board
		self.kanban_board.triggered.connect(self._open_kanban)


		#Visual Build
		self.visual_build.toggled.connect(lambda state: cmds.optionVar(intValue=("mutant_visual_build", state)))

		#Wrap Block Icons
		self.wrap_icons.toggled.connect(lambda state: cmds.optionVar(intValue=("mutant_wrap_icons", state)))

		#Clear Script Editor
		self.clear_script_editor.toggled.connect(lambda state: cmds.optionVar(intValue=("mutant_clear_script_editor", state)))

		#Revert on Fail
		self.revert_on_fail.toggled.connect(lambda state: cmds.optionVar(intValue=("mutant_revert_on_fail", state)))

		#Show Block Tooltips
		self.show_block_tooltips.toggled.connect(lambda state: cmds.optionVar(intValue=("mutant_show_block_tooltips", state)))

		#Use Fast Skin (Rebuild)
		self.use_fast_skin.toggled.connect(lambda state: cmds.optionVar(intValue=("mutant_use_fast_skin", state)))

		#Standard Window
		self.standard_window.toggled.connect(self._toggle_standard_window)

	# -------------------------------------------------------------------
	def _toggle_standard_window(self, state):
		"""Find the parent Qt_Mutant window and toggle its window mode."""
		parent = self.parent()
		while parent:
			if hasattr(parent, 'toggle_standard_window'):
				parent.toggle_standard_window(standard=state)
				return
			parent = parent.parent()
		cmds.warning('Could not find Mutant main window to toggle window mode.')

	# -------------------------------------------------------------------
	def _open_kanban(self, *args):
		try:
			import importlib;from importlib import reload
		except:
			import imp;from imp import reload
		from Mutant_Tools.UI.Kanban import load_kanban
		reload(load_kanban)
		try:
			self._cKanbanUI.close()
		except:
			pass
		self._cKanbanUI = load_kanban.KanbanUI()
		self._cKanbanUI.show()

	# -------------------------------------------------------------------
	def set_mutant_hotkeys(self, *args):
		try:
			import Mutant_Tools.UI.QtMutantWindow as QtMutantWindow
			reload(QtMutantWindow)
			success = QtMutantWindow.set_mutant_hotkeys_enabled(True)
			if not success:
				cmds.warning('Could not set Mutant hotkeys.')
				return
		except Exception as e:
			cmds.warning('Could not set Mutant hotkeys: {}'.format(e))
			return

		print('Mutant hotkeys set.')

	# -------------------------------------------------------------------
	def save_skins(self):
		EasySkin.save_all_skins_to()

	def load_skins(self):
		EasySkin.load_all_skins_from()

	def fast_save_skins(self):
		try:
			from Mutant_Tools.Utils.IO import IOSkin
			reload(Mutant_Tools.Utils.IO.IOSkin)

			folder_path = mh.folder_window()
			if not folder_path:
				cmds.warning('Fast Save Skin Pack cancelled (no folder selected).')
				return

			skinned_geos = IOSkin.getSkinnedSceneObjects()
			if not skinned_geos:
				cmds.warning('No skinned geometries found in scene for Fast Save Skin Pack.')
				return

			pack_path = os.path.join(folder_path, 'FastSkinPack.bSkinPack')
			IOSkin.exportSkinPack(packPath=pack_path, objs=skinned_geos)
			print('Fast Save Skin Pack exported: {}'.format(pack_path))
		except Exception as e:
			cmds.warning('Fast Save Skin Pack unavailable ({}). Falling back to Save All Skins.'.format(e))
			EasySkin.save_all_skins_to()

	def fast_load_skins(self):
		try:
			from Mutant_Tools.Utils.IO import IOSkin
			reload(Mutant_Tools.Utils.IO.IOSkin)
			IOSkin.importSkinPack()
		except Exception as e:
			cmds.warning('Fast Load Skin Pack unavailable ({}). Falling back to Load All Skins.'.format(e))
			EasySkin.load_all_skins_from()

	def save_sel_skins(self):
		EasySkin.save_selected_geos()

	def load_sel_skins(self):
		EasySkin.load_selected_geos()

	# -------------------------------------------------------------------

	def open_website(self, website = 'http://mutanttools.com/'):

		self.get_web_viewer_state()

		cWebsiteViewer = load_website_viewer.WebsiteViewerUI(website = website)

		if self.open_viewer == True:
			cWebsiteViewer.show()
		else:
			cWebsiteViewer.open_link(website)

	# -------------------------------------------------------------------

	def get_web_viewer_state(self):
		if self.open_in_maya.isChecked():
			self.open_viewer = True
		else:
			self.open_viewer = False

	# -------------------------------------------------------------------

	def send_webhook_message(self, webhook, message):

		# Provide the webhook URL that Discord generated


		# Post the message to the slack webhook
		message = {"content": message}
		req = Request(webhook, json.dumps(message).encode('utf-8'))

		# specifying headers for the request, discord appears to block the  default urllib user-agent
		req.add_header('Content-Type', 'application/json')
		req.add_header('User-Agent', 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11')

		response = urlopen(req)
		response.read()

		#try:OpenMaya.MGlobal.displayInfo('Message Sent')
		#except:pass

	# -------------------------------------------------------------------

	def send_bugs(self):
		from Mutant_Tools.Utils.Helpers import discord
		reload(discord)
		discord.send_bugs()

	# -------------------------------------------------------------------

	def send_requests(self):
		from Mutant_Tools.Utils.Helpers import discord
		reload(discord)
		discord.send_requests()

	# -------------------------------------------------------------------
	def load_guide_placement(self):
		from Mutant_Tools.UI.GuidePlacements import load_guide_placements
		reload(load_guide_placements)

		try:cGuidePlacements.close()
		except:pass
		cGuidePlacements = load_guide_placements.GuidePlacements()
		cGuidePlacements.show()

	# -------------------------------------------------------------------

	def load_butcher(self):
		import Mutant_Tools
		from Mutant_Tools.UI.Butcher import load_butcher
		reload(load_butcher)

		try:
			cButcherUI.close()
		except:
			pass
		cButcherUI = load_butcher.ButcherUI()
		cButcherUI.show()

	# -------------------------------------------------------------------


	# CLOSE EVENTS _________________________________
	def closeEvent(self, event):
		''


# -------------------------------------------------------------------

if __name__ == "__main__":

	try:
		AutoRiggerMenu.close()  # pylint: disable=E0601
		AutoRiggerMenu.deleteLater()
	except:
		pass
	menu_ui = AutoRiggerMenu()
	menu_ui.show()

# -------------------------------------------------------------------

