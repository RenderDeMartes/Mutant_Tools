from __future__ import absolute_import, division
'''
version: 1.0.0
date: 21/04/2020

#----------------
content:

This will create a UI for the autorriger menu tool.

#----------------
how to:

import Mutant_Tools
from Mutant_Tools.UI.RigTools.Tabs import load_CorrectivesTab
reload(load_CorrectivesTab)


cCorrectives_ui = load_CorrectivesTab.CorrectivesTab()
cCorrectives_ui.show()

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
import random
from random import randrange

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

from Mutant_Tools.Utils.Rigging import main_mutant
reload(Mutant_Tools.Utils.Rigging.main_mutant)
mt = main_mutant.Mutant()

from Mutant_Tools.Utils.Correctives import PushCorrectives
reload(PushCorrectives)

from Mutant_Tools.Utils.Correctives import blendshapes_correctives
reload(blendshapes_correctives)

from Mutant_Tools.Utils.Helpers.decorators import undo

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

Title = 'Correctives'
UI_File = 'Correctives.ui'



# -------------------------------------------------------------------

def maya_main_window():
	main_window_ptr = omui.MQtUtil.mainWindow()
	return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class CorrectivesTab(QtWidgets.QDialog):

	def __init__(self, parent=maya_main_window()):
		super(CorrectivesTab, self).__init__(parent)

		self.setWindowTitle(Title)

		self.init_ui()
		self.create_layout()
		self.create_connections()

		self.limb_push_systems=None

		self.resize(650, 690)

	def init_ui(self):
		UIPath = os.path.join(FOLDER,'UI','RigTools','Tabs',UI_File)
		f = QtCore.QFile(os.path.join(UIPath))
		f.open(QtCore.QFile.ReadOnly)

		loader = QtUiTools.QUiLoader()
		self.ui = loader.load(f, parentWidget=self)

		f.close()

	# -------------------------------------------------------------------

	def create_layout(self):
		self.populate_correctives_text()

	# -------------------------------------------------------------------

	def create_connections(self):
		self.ui.load_joint_Btn.clicked.connect(lambda:self.fill_push_object(
												sides=[self.ui.FrontCheckBox,
												self.ui.BackCheckBox,
												self.ui.InCheckBox,
												self.ui.OutCheckBox
												]))
		self.ui.push_guides_Btn.clicked.connect(lambda:self.create_push_guides(source=self.ui.load_joint_edit.text(),
												sides=[self.ui.FrontCheckBox,
												self.ui.BackCheckBox,
												self.ui.InCheckBox,
												self.ui.OutCheckBox
												]))
		self.ui.push_build_Btn.clicked.connect(lambda:self.build_push_correctives())

		self.ui.template_combo.currentIndexChanged.connect(self.populate_correctives_text)
		self.ui.geo_line_button.clicked.connect(self.put_geo_in_line)
		self.ui.create_correctives_button.clicked.connect(self.create_blendshapes)
		self.ui.connect_button.clicked.connect(self.connect_controllers)
		self.ui.connect_mirror_button.clicked.connect(self.mirror_blendshapes)

	# -------------------------------------------------------------------

	@undo
	def create_push_guides(self, source=None, sides=None):
		self.limb_push_systems = []
		#ZIP the comparative side and checkbox sides to see if it should pass it
		for side in sides:
			if side.isChecked():
				PushSystemObject = PushCorrectives.PushSystem()
				#PushSystemObject.create_push_joints(sources=cmds.ls(sl=True))
				PushSystemObject.create_push_joints(source=source, side=[side.text()])
				self.limb_push_systems.append(PushSystemObject)

	def fill_push_object(self, sides=None):
		self.limb_push_systems = []
		source = str(cmds.ls(sl=True)[0])
		self.ui.load_joint_edit.setText(source)
		for side in sides:
			if side.isChecked():
				try:
					print('{} added to buildable push Objects'.format(side.text()))
					PushSystemObject = PushCorrectives.PushSystem()
					PushSystemObject.identify_push_joints(source=source, side=[side.text()])
					self.limb_push_systems.append(PushSystemObject)
					print('Found the joints asssociated with {}_{}'.format(source, [side.text()]))
				except:
					cmds.warning('Could not find the joints asssociated with {}_{}'.format(source, [side.text()]))

	@undo
	def build_push_correctives(self):
		for limb_push_system in self.limb_push_systems:
			limb_push_system.create_push_system()

	# -------------------------------------------------------------------

	def populate_correctives_text(self):
		current_template = self.ui.template_combo.currentText()

		details = blendshapes_correctives.correctives_templates[current_template]

		#html code using  textEdit instead of plain text
		fancy_text = '<p>Shapes:</p>'

		for s in details['shapes']:
			shape_name = '<span style="color: orange;">BSP.GEO_' + s + '</span><br>'
			fancy_text += shape_name

		fancy_text += '<p>Drivers:</p>'
		for d, v in zip(details['driver_sdk'], details['values']):
			driver_text = '<span style="color: lightblue;">' + d + ' : ' + str(v) + '</span><br>'
			fancy_text += driver_text

		self.ui.text_shapes.setHtml(fancy_text)

	def put_geo_in_line(self):
		sel = cmds.ls(sl=True)
		self.ui.geo_line.setText(sel[0])

	@undo
	def create_blendshapes(self):
		geo = self.ui.geo_line.text()
		template = self.ui.template_combo.currentText()
		print(geo, template)

		cBSPCorrectives = blendshapes_correctives.BSP_Correctives(geo, template)
		cBSPCorrectives.create_correctives()

	@undo
	def connect_controllers(self):
		geo = self.ui.geo_line.text()
		template = self.ui.template_combo.currentText()
		blendshape_name = self.ui.blendshape_name_line.text()

		cBSPCorrectives = blendshapes_correctives.BSP_Correctives(geo, template)
		cBSPCorrectives.connect_correctives(geo, blendshape_name, template)

	@undo
	def mirror_blendshapes(self):
		geo = self.ui.geo_line.text()
		template = self.ui.template_combo.currentText()
		blendshape_name = self.ui.blendshape_name_line.text()

		cBSPCorrectives = blendshapes_correctives.BSP_Correctives(geo, template)
		cBSPCorrectives.connect_correctives(geo, blendshape_name, template, mirror=True)

	# -------------------------------------------------------------------


	# CLOSE EVENTS _________________________________
	def closeEvent(self, event):
		''


# -------------------------------------------------------------------

if __name__ == "__main__":

	try:
		cCorrectivesTab.close()  # pylint: disable=E0601
		cCorrectivesTab.deleteLater()
	except:
		pass
	cCorrectivesTab = CorrectivesTab()
	cCorrectivesTab.show()

# -------------------------------------------------------------------

