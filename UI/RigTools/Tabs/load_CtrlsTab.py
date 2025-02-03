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
from Mutant_Tools.UI.RigTools.Tabs import load_CtrlsTab
reload(load_CtrlsTab)

try:cCtrls_ui.close()
except:pass
cCtrls_ui = load_CtrlsTab.CtrlsTab()
cCtrls_ui.show()

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

reload(Mutant_Tools.Utils.Rigging.main_mutant)
mt = main_mutant.Mutant()

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

Title = 'Ctrls-Tab'
UI_File = 'Ctrls.ui'



# -------------------------------------------------------------------

def maya_main_window():
	main_window_ptr = omui.MQtUtil.mainWindow()
	return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class CtrlsTab(QtWidgets.QDialog):

	def __init__(self, parent=maya_main_window()):
		super(CtrlsTab, self).__init__(parent)

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
		self.populate_ctrls_layout()

		
	# -------------------------------------------------------------------

	def create_connections(self):
		self.ui.mutant_controller.clicked.connect(self.tag_mutant_controller)
		self.ui.mirror_behavior.clicked.connect(self.mirror_behavior)
		self.ui.world_mirror.clicked.connect(self.mirror_world)
		self.ui.root_auto.clicked.connect(self.root_auto)
		self.ui.offset.clicked.connect(self.offset_grp)
		self.ui.match.clicked.connect(self.match_transform)
		self.ui.red.clicked.connect(lambda: self.assign_color(color='red'))
		self.ui.blue.clicked.connect(lambda: self.assign_color(color='blue'))
		self.ui.green.clicked.connect(lambda: self.assign_color(color='green'))
		self.ui.white.clicked.connect(lambda: self.assign_color(color='white'))
		self.ui.purple.clicked.connect(lambda: self.assign_color(color='purple'))
		self.ui.yellow.clicked.connect(lambda: self.assign_color(color='yellow'))
		self.ui.light_blue.clicked.connect(lambda: self.assign_color(color='lightBlue'))
		self.ui.black.clicked.connect(lambda: self.assign_color(color='grey'))

		self.ui.rgb1.clicked.connect(lambda: self.rgb_color(color=[230, 176, 170]))
		self.ui.rgb2.clicked.connect(lambda: self.rgb_color(color=[195, 155, 211]))
		self.ui.rgb3.clicked.connect(lambda: self.rgb_color(color=[127, 179, 213]))
		self.ui.rgb4.clicked.connect(lambda: self.rgb_color(color=[155, 198, 182]))
		self.ui.rgb5.clicked.connect(lambda: self.rgb_color(color=[130, 224, 170]))
		self.ui.rgb6.clicked.connect(lambda: self.rgb_color(color=[245, 176, 65]))
		self.ui.rgb7.clicked.connect(lambda: self.rgb_color(color=[229, 152, 102]))
		self.ui.rgb8.clicked.connect(lambda: self.rgb_color(color=[133, 146, 158]))
		self.ui.rgb9.clicked.connect(lambda: self.rgb_color(color=[146, 43, 33]))
		self.ui.rgb10.clicked.connect(lambda: self.rgb_color(color=[14, 102, 85]))
		self.ui.rgb11.clicked.connect(lambda: self.rgb_color(color=[118, 68, 138]))
		self.ui.rgb12.clicked.connect(lambda: self.rgb_color(color=[31, 97, 141]))
		self.ui.rgb13.clicked.connect(lambda: self.rgb_color(color=[34, 153, 84]))
		self.ui.rgb14.clicked.connect(lambda: self.rgb_color(color=[110, 44, 0]))
		self.ui.rgb15.clicked.connect(lambda: self.rgb_color(color=[46, 64, 83]))

		self.ui.rgb_random.clicked.connect(self.random_color)
		self.ui.rgb_random_each.clicked.connect(self.random_color_each)

		#self.ui.create_ctrl.clicked.connect(self.create_ctrl)
		self.ui.translate.clicked.connect(self.connect_translate)
		self.ui.rotate.clicked.connect(self.connect_rotate)
		self.ui.scale.clicked.connect(self.connect_scale)

		self.ui.color_wheel.clicked.connect(self.rgb_pick_color)


	# -------------------------------------------------------------------
	def random_color(self):
		r = randrange(255)
		g = randrange(255)
		b = randrange(255)
		rand_color = [r, g, b]

		sel = cmds.ls(sl=True)
		if not sel:
			return False
		for i in sel:
			cmds.select(i)
			mt.assign_color_rgb(color=[rand_color[0] / 255, rand_color[1] / 255, rand_color[2] / 255])
		cmds.select(sel)

	def random_color_each(self):

		sel = cmds.ls(sl=True)
		if not sel:
			return False
		for i in sel:
			r = randrange(255)
			g = randrange(255)
			b = randrange(255)
			rand_color = [r, g, b]
			cmds.select(i)
			mt.assign_color_rgb(color=[rand_color[0] / 255, rand_color[1] / 255, rand_color[2] / 255])
		cmds.select(sel)



	def rgb_pick_color(self):
		result = cmds.colorEditor()
		buffer = result.split()
		if '1' == buffer[3]:
			values = cmds.colorEditor(query=True, rgb=True)
			print('RGB = ' + str(values))
			alpha = cmds.colorEditor(query=True, alpha=True)
			print('Alpha = ' + str(alpha))
		else:
			print('Editor was dismissed')

		sel = cmds.ls(sl=True)
		if not sel:
			return False
		for i in sel:
			cmds.select(i)
			mt.assign_color_rgb(color = values)
		cmds.select(sel)

	def rgb_color(self, color = [0,0,0]):
		sel = cmds.ls(sl=True)
		if not sel:
			return False
		for i in sel:
			cmds.select(i)
			mt.assign_color_rgb(color = [color[0]/255, color[1]/255, color[2]/255])
		cmds.select(sel)

	def populate_ctrls_layout(self):

		curves = []
		for c in curve_data:
			curves.append(c)

		curves=sorted(curves)
		curves_groups = list(self.divide_chunks(curves, 5))

		for grp in curves_groups:
			side_hbox = QtWidgets.QGroupBox()
			self.ui.curves_layout.addWidget(side_hbox)
			h_layout = QtWidgets.QHBoxLayout()
			side_hbox.setLayout(h_layout)
			h_layout.setContentsMargins(1, 1, 1, 1)
			side_hbox.setContentsMargins(1, 1, 1, 1)
			side_hbox.setStyleSheet("border : 0px solid grey; ")

			for cv in grp:
				cv_button = QtWidgets.QPushButton()
				cv_button.setStyleSheet("""
										QPushButton {
											background-color: none; 
											border: 0px solid black;
										}
										QPushButton:hover {
										background-color: grey;
            							}
										}
									""")
				cv_button.setFixedSize(70,70)
				h_layout.addWidget(cv_button)
				cv_button.setToolTip(cv)
				cv_button.clicked.connect(partial(self.create_curve, cv))
				icon_path = os.path.join(FOLDER, 'config', 'Curves', '{}.png'.format(cv))
				if os.path.isfile(icon_path):
					cv_button.setIcon(QtGui.QIcon(icon_path))
					cv_button.setIconSize((QtCore.QSize(70, 70)))
				else:
					cv_button.setText(cv)
	def divide_chunks(self, l, n):
		# looping till length l
		for i in range(0, len(l), n):
			yield l[i:i + n]

	@undo
	def create_curve(self, cv):

		custom_name = self.ui.custom_name_line.text()
		size = self.ui.size_slider.value()

		sel = cmds.ls(sl=True)
		for num, s in enumerate(sel):
			cmds.select(s)
			if s.endswith(nc['ctrl']):
				mt.change_curve_shape(input=s, new_shape=cv, size = size)
				continue
			if custom_name:
				ctrl = mt.curve(input='',
								type=cv,
								rename=True,
								custom_name=True,
								name=custom_name+'_'+str(num)+nc['ctrl'],
								size=1)
			else:
				ctrl= mt.curve(input='',
						 type=cv,
						 rename=True,
						 custom_name=False,
						 name='',
						 size=1)
			mt.root_grp()
			if self.ui.pc.isChecked():
				cmds.parentConstraint(ctrl, s, mo=True)
				cmds.scaleConstraint(ctrl, s, mo=True)

			if self.ui.trs.isChecked() and not self.ui.pc.isChecked():
				cmds.select(ctrl, s)
				self.connect_translate()
				cmds.select(ctrl, s)
				self.connect_rotate()
				cmds.select(ctrl, s)
				self.connect_scale()

		if not sel:
			if custom_name:
				ctrl = mt.curve(input='',
								type=cv,
								rename=True,
								custom_name=True,
								name=custom_name+nc['ctrl'],
								size=1)
			else:
				ctrl= mt.curve(input='',
						 type=cv,
						 rename=True,
						 custom_name=False,
						 name='',
						 size=1)

			mt.root_grp()


	# -------------------------------------------------------------------

	@undo
	def tag_mutant_controller(self):
		# define variables
		global_ctrl = 'Global_Ctrl'
		sel = cmds.ls(sl=True)
		# Determining ctrls for script to be applied to.
		if not sel:
			sel = cmds.ls('*_Ctrl')
		# Create rotate order attr and connect it
		for ctrl in sel:
			cmds.select(ctrl)
			self.curve_thickness(num=2)

			if cmds.attributeQuery("RotateOrder", node=ctrl, exists=True) == False:
				mt.connect_rotate_order(input=ctrl, object=ctrl)
			# tag as controller
			mel.eval('TagAsController;')
			# connect controller visibility type.
			if cmds.objExists(global_ctrl):
				cmds.connectAttr("{}.CtrlVis".format(global_ctrl), "{}_tag.visibilityMode".format(ctrl))

			#Missing the line width change, none working code:
			cmds.setAttr('{}.lineWidth'.format(cmds.listRelatives(ctrl, shapes=True)[0]), 2)

			#rename to desire name
			cmds.rename(ctrl, ctrl.replace('_ctrl', '_Ctrl'))

	def curve_thickness(self, num=2):
		"""
        Set the thickness of all shapes in all selected curves to a desired value.

        Args:
        num (int, optional): The line width value to set. Defaults to 2.

        Returns:
        None
        """
		ctrl_sel = cmds.ls(sl=True, type="transform")

		for ctrl in ctrl_sel:
			shape_list = cmds.listRelatives(ctrl, shapes=True)
			for shape in shape_list:
				cmds.setAttr("{}.lineWidth".format(shape), num)

	@undo
	def assign_color(self, color):
		mt.assign_color(color=color)

	def mirror_behavior(self):
		mt.mirror_group(input=cmds.ls(sl=True), world=False)

	def mirror_world(self):
		mt.mirror_group(input=cmds.ls(sl=True), world=True)

	def root_auto(self):
		mt.root_grp(autoRoot=True)

	def offset_grp(self):
		mt.root_grp()

	def match_transform(self):
		sel = cmds.ls(sl=True)
		for s in sel:
			if s == sel[-1]:
				continue
			cmds.delete(cmds.parentConstraint(sel[-1], s))

	@undo
	def create_ctrl(self):

		custom_name = self.ui.custom_name_line.text()

		sel = cmds.ls(sl=True)
		for num, s in enumerate(sel):
			cmds.select(s)
			if custom_name:
				ctrl = mt.curve(input='',
								type=self.ui.curves.currentText(),
								rename=True,
								custom_name=True,
								name=custom_name+'_'+str(num)+nc['ctrl'],
								size=1)
			else:
				ctrl= mt.curve(input='',
						 type=self.ui.curves.currentText(),
						 rename=True,
						 custom_name=False,
						 name='',
						 size=1)
			mt.root_grp()
			if self.ui.pc.isChecked():
				cmds.parentConstraint(ctrl, s, mo=True)
				cmds.scaleConstraint(ctrl, s, mo=True)

			if self.ui.trs.isChecked() and not self.ui.pc.isChecked():
				cmds.select(ctrl, s)
				self.connect_translate()
				cmds.select(ctrl, s)
				self.connect_rotate()
				cmds.select(ctrl, s)
				self.connect_scale()

		if not sel:
			if custom_name:
				ctrl = mt.curve(input='',
								type=self.ui.curves.currentText(),
								rename=True,
								custom_name=True,
								name=custom_name+nc['ctrl'],
								size=1)
			else:
				ctrl= mt.curve(input='',
						 type=self.ui.curves.currentText(),
						 rename=True,
						 custom_name=False,
						 name='',
						 size=1)

			mt.root_grp()

	@undo
	def connect_translate(self):
		sel = cmds.ls(sl=True)
		if self.ui.tx.isChecked():
			cmds.connectAttr('{}.tx'.format(sel[0]),'{}.tx'.format(sel[-1]))
		if self.ui.ty.isChecked():
			cmds.connectAttr('{}.ty'.format(sel[0]),'{}.ty'.format(sel[-1]))
		if self.ui.tz.isChecked():
			cmds.connectAttr('{}.tz'.format(sel[0]),'{}.tz'.format(sel[-1]))

	@undo
	def connect_rotate(self):
		sel = cmds.ls(sl=True)
		if self.ui.rx.isChecked():
			cmds.connectAttr('{}.rx'.format(sel[0]),'{}.rx'.format(sel[-1]))
		if self.ui.ry.isChecked():
			cmds.connectAttr('{}.ry'.format(sel[0]),'{}.ry'.format(sel[-1]))
		if self.ui.rz.isChecked():
			cmds.connectAttr('{}.rz'.format(sel[0]),'{}.rz'.format(sel[-1]))

	@undo
	def connect_scale(self):
		sel = cmds.ls(sl=True)
		if self.ui.sx.isChecked():
			cmds.connectAttr('{}.sx'.format(sel[0]),'{}.sx'.format(sel[-1]))
		if self.ui.sy.isChecked():
			cmds.connectAttr('{}.sy'.format(sel[0]),'{}.sy'.format(sel[-1]))
		if self.ui.sz.isChecked():
			cmds.connectAttr('{}.sz'.format(sel[0]),'{}.sz'.format(sel[-1]))

	# -------------------------------------------------------------------



	# CLOSE EVENTS _________________________________
	def closeEvent(self, event):
		''


# -------------------------------------------------------------------

if __name__ == "__main__":

	try:
		CtrlsTab.close()  # pylint: disable=E0601
		CtrlsTab.deleteLater()
	except:
		pass
	cCtrls_ui = CtrlsTab()
	cCtrls_ui.show()

# -------------------------------------------------------------------

