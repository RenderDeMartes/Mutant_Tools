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
imp.reload(load_autoRiggerMenu)

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
import imp
import sys
import json

try:from urllib.request import Request, urlopen
except:pass

import Mutant_Tools
from Mutant_Tools.UI.WebsiteViewer import load_website_viewer
imp.reload(load_website_viewer)
viewer = load_website_viewer.WebsiteViewerUI()

from Mutant_Tools.Utils.Helpers import helpers
imp.reload(Mutant_Tools.Utils.Helpers.helpers)
mh = helpers.Helpers()

from Mutant_Tools.Utils.IO import SkinUtils
imp.reload(Mutant_Tools.Utils.IO.SkinUtils)
skin = SkinUtils.Skinning()

from Mutant_Tools.Utils.IO import NgSkinUtils
imp.reload(Mutant_Tools.Utils.IO.NgSkinUtils)
ngmt = NgSkinUtils.NG_Mutant()

from Mutant_Tools.Utils.IO import CtrlUtils
imp.reload(Mutant_Tools.Utils.IO.CtrlUtils)
ctrls = CtrlUtils.Ctrls()

from Mutant_Tools.Utils.IO import Guides
imp.reload(Mutant_Tools.Utils.IO.Guides)
guides = Guides.Guides()

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
		self.cWebsiteViewer = viewer

		self.setWindowTitle(Title)
		self.setFixedHeight(20)

		self.init_ui()
		self.create_layout()
		self.create_connections()

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

		self.save_guide = self.fileMenu.addAction("Save Guide")
		self.load_guide = self.fileMenu.addAction("Load Guide")
		self.place_guide = self.fileMenu.addAction("Guide Placement")
		self.fileMenu.addSeparator()

		self.bind_selected = self.fileMenu.addAction("Bind Selected Geo")
		self.download_ng = self.fileMenu.addAction("Download NgSkinToolsV2")
		self.save_skin = self.fileMenu.addAction("Save All Skins")
		self.load_skin = self.fileMenu.addAction("Load All Skins")
		self.save_sel_skin = self.fileMenu.addAction("Save Selected Skins")
		self.load_sel_skin = self.fileMenu.addAction("Load Selected Skins")
		self.fileMenu.addSeparator()

		self.save_ctrls = self.fileMenu.addAction("Save Ctrls")
		self.load_ctrls = self.fileMenu.addAction("Load Ctrls")
		self.mirror_ctrls = self.fileMenu.addAction("Mirror Ctrls")
		self.fileMenu.addSeparator()

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

		self.bind_selected.triggered.connect(lambda: skin.bind_to_bnd())
		self.save_skin.triggered.connect(self.save_skins)
		self.load_skin.triggered.connect(self.load_skins)
		self.save_sel_skin.triggered.connect(self.save_sel_skins)
		self.load_sel_skin.triggered.connect(self.load_sel_skins)

		self.save_ctrls.triggered.connect(lambda: ctrls.save_all())
		self.load_ctrls.triggered.connect(lambda: ctrls.load_all())
		self.mirror_ctrls.triggered.connect(lambda: ctrls.mirror_all())

		#HELP MENU
		self.discord.triggered.connect(lambda: self.cWebsiteViewer.open_link('https://discord.gg/pqGeYhUcAW'))
		self.report_bug.triggered.connect(lambda: self.send_bugs())
		self.request_feature.triggered.connect(lambda: self.send_requests())

		self.riggers.triggered.connect(lambda: self.open_website('https://mutanttools.com/riggers/'))
		self.developers.triggered.connect(lambda: self.open_website('https://mutanttools.com/mt_commands/'))
		self.main_page.triggered.connect(lambda: self.open_website('https://mutanttools.com/'))

		#DONATE MENU
		self.paypal.triggered.connect(lambda: self.open_website('https://www.paypal.com/paypalme/renderdemartes'))
		self.crypto.triggered.connect(lambda: self.open_website('https://mutanttools.com/donate/'))

	# -------------------------------------------------------------------
	def save_skins(self):
		try:
			ngmt.export_all_skins()
		except:
			import ngSkinTools2
			ngSkinTools2.open_ui()
			ngmt.export_all_skins()

	def load_skins(self):
		try:
			ngmt.import_all_skins()
		except:
			import ngSkinTools2
			ngSkinTools2.open_ui()
			ngmt.import_all_skins()

	def save_sel_skins(self):
		try:
			ngmt.export_selected_skin()
		except:
			import ngSkinTools2
			ngSkinTools2.open_ui()
			ngmt.export_selected_skin()

	def load_sel_skins(self):
		try:
			ngmt.import_selected_skins()
		except:
			import ngSkinTools2
			ngSkinTools2.open_ui()
			ngmt.import_selected_skins()

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

		try:OpenMaya.MGlobal.displayInfo('Message Sent')
		except:pass

	# -------------------------------------------------------------------

	def send_bugs(self):
		from Mutant_Tools.Utils.Helpers import discord
		imp.reload(discord)
		discord.send_bugs()

	# -------------------------------------------------------------------

	def send_requests(self):
		from Mutant_Tools.Utils.Helpers import discord
		imp.reload(discord)
		discord.send_requests()

	# -------------------------------------------------------------------
	def load_guide_placement(self):
		from Mutant_Tools.UI.GuidePlacements import load_guide_placements
		imp.reload(load_guide_placements)

		try:cGuidePlacements.close()
		except:pass
		cGuidePlacements = load_guide_placements.GuidePlacements()
		cGuidePlacements.show()

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

