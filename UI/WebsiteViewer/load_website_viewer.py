'''
version: 1.0.0
date: 21/04/2020

#----------------
content:

#----------------
how to:

import imp
import Mutant_Tools
from Mutant_Tools.UI.WebsiteViewer import load_website_viewer
import imp
imp.reload(load_website_viewer)

try:cWebsiteViewer.close()
except:pass
cWebsiteViewer = load_website_viewer.WebsiteViewerUI()
cWebsiteViewer.show()

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
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtUiTools import *
from PySide2.QtWebEngineWidgets import *
from PySide2.QtCore import QUrl


import maya.OpenMayaUI as omui
from functools import partial
from maya import OpenMaya
import maya.cmds as cmds
import maya.mel as mel

import os
import imp
import sys
import json
import glob
import pprint


# -------------------------------------------------------------------

# Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = PATH.replace('\\UI\\WebsiteViewer', '//Config')  # change this path depending of the folder

JSON_FILE = (PATH + '/name_conventions.json')
with open(JSON_FILE) as json_file:
	nc = json.load(json_file)
# Read curve shapes info
CURVE_FILE = (PATH + '/curves.json')
with open(CURVE_FILE) as curve_file:
	curve_data = json.load(curve_file)
# setup File
SETUP_FILE = (PATH + '/rig_setup.json')
with open(SETUP_FILE) as setup_file:
	setup = json.load(setup_file)

# -------------------------------------------------------------------

# QT WIndow!
PATH = os.path.dirname(__file__)
OTHERS_PATH = PATH.replace('\\UI\\WebsiteViewer', '//Others')  # get presets path to read files
BLOCKS_PATH = PATH.replace('\\UI\\WebsiteViewer', '//Blocks')  # get Blocks paths to write files

Title = 'Mutant || WebsiteViewer'
Folder = PATH.replace('\\UI\\WebsiteViewer', '')
UI_File = 'WebsiteViewer.ui'
IconsPath = Folder + '//Icons//'

# -------------------------------------------------------------------

import Mutant_Tools
import Mutant_Tools.Utils
from Mutant_Tools.Utils.Rigging import main_mutant

imp.reload(Mutant_Tools.Utils.Rigging.main_mutant)
mt = main_mutant.Mutant()

import Mutant_Tools.UI
from Mutant_Tools.UI import QtMutantWindow
imp.reload(QtMutantWindow)
Qt_Mutant = QtMutantWindow.Qt_Mutant()


# -------------------------------------------------------------------


def maya_main_window():
	main_window_ptr = omui.MQtUtil.mainWindow()
	return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class WebsiteViewerUI(QtMutantWindow.Qt_Mutant):

	def __init__(self, website = 'http://mutanttools.com/'):
		super(WebsiteViewerUI, self).__init__()

		self.website = website

		self.setWindowTitle(Title)
		self.resize(500,600)

		self.designer_loader_child(path=Folder + '/UI/WebsiteViewer/', ui_file=UI_File)
		self.set_title('Website Viewer')

		self.create_layout()
		self.create_connections()

	# -------------------------------------------------------------------

	def create_layout(self):
		view = QWebEngineView()
		view.load(QUrl(self.website))
		self.ui.website_layout.addWidget(view)

	def create_connections(self):
		self.ui.explorer_btn.clicked.connect(lambda: self.open_link(self.website))


	def open_link(self, linkStr):
		QDesktopServices.openUrl(QUrl(linkStr))

	# -------------------------------------------------------------------

	# CLOSE EVENTS _________________________________
	def closeEvent(self, event):
		''


# -------------------------------------------------------------------

if __name__ == "__main__":

	try:
		cWebsiteViewer.close()  # pylint: disable=E0601
		cWebsiteViewer.deleteLater()
	except:
		pass
	cWebsiteViewer = WebsiteViewerUI()
	cWebsiteViewer.show()

# -------------------------------------------------------------------

'''
#Notes






'''