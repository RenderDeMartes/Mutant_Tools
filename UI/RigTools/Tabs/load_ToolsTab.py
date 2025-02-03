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
from Mutant_Tools.UI.RigTools.Tabs import load_ToolsTab
reload(load_ToolsTab)

try:cTools_ui.close()
except:pass
cTools_ui = load_ToolsTab.ToolsTab()
cTools_ui.show()

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

Title = 'Tools-Tab'
UI_File = 'Tools.ui'



# -------------------------------------------------------------------

def maya_main_window():
	main_window_ptr = omui.MQtUtil.mainWindow()
	return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class ToolsTab(QtWidgets.QDialog):

	def __init__(self, parent=maya_main_window()):
		super(ToolsTab, self).__init__(parent)

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
		try:
			from mstar.nodes.mayaNode import MayaNode
			self.ui.tongue_eyes_edit.setText("Face_C_Tongue_Geo,Face_C_GumsBottom_Geo,Face_C_GumsTop_Geo,Face_C_ToothTop_Geo,Face_C_ToothBottom_Geo")
		except Exception as e:
			print(e)
			pass

		
	# -------------------------------------------------------------------

	def create_connections(self):

		self.ui.smallerGuideBtn.clicked.connect(lambda: self.resize_guides(0.75))
		self.ui.biggerGuideBtn.clicked.connect(lambda: self.resize_guides(1.25))
		self.ui.smallerCtrlsBtn.clicked.connect(lambda: self.resize_Ctrls(0.75))
		self.ui.biggerCtrlsBtn.clicked.connect(lambda: self.resize_Ctrls(1.25))
		self.ui.JointSizeSlider.valueChanged.connect(lambda: cmds.jointDisplayScale(self.ui.JointSizeSlider.value() * 0.04))

		self.ui.HideAxisBtn.clicked.connect(lambda: self.toggle_axis(False))
		self.ui.ShowAxisBtn.clicked.connect(lambda: self.toggle_axis(True))
		self.ui.lockContainerBtn.clicked.connect(lambda: self.toogle_contrainers(True))
		self.ui.unlockContainerBtn.clicked.connect(lambda: self.toogle_contrainers(False))

		self.ui.HideBtn.clicked.connect(self.hide_attrs)
		self.ui.RevealBtn.clicked.connect(self.show_attrs)

		self.ui.SimpleFKBtn.clicked.connect(lambda: mt.fk_chain(size = self.ui.SimpleFKSizeSlider.value(),
																color = self.ui.SimpleFKColorBox.currentText(),
																curve_type = self.ui.SimpleFKShapeBox.currentText()))
		self.ui.TubeFKBtn.clicked.connect(self.tube_fk_chain)
		self.ui.auto_rotate_fk.clicked.connect(self.auto_rotate_fk)

		self.ui.keyVisemes.clicked.connect(self.key_visemes)
		self.ui.bakeVisemes.clicked.connect(self.bake_visemes)
		self.ui.splitVisemes.clicked.connect(self.split_visemes)
		self.ui.load_blendshapes.clicked.connect(self.load_blendshapes_from_sel)
		self.ui.connectVisemes.clicked.connect(self.connect_visemes)

		self.ui.help_button.clicked.connect(self.open_visemes_help)

		#self.ui.add_tongue_eyes.clicked.connect(self.pupulate_tongue_eyes)
		#self.ui.fix_shove.clicked.connect(self.fix_shove_issue)
		self.ui.dynamic_fk_btn.clicked.connect(self.create_dynamic_fk_ui)
		self.ui.connect_to_scale_reader.clicked.connect(self.connect_to_scale_reader)
		self.ui.scale_guides_button.clicked.connect(lambda: self.scale_mutant_template(float(self.ui.scale_guides_line.text()),
																				  float(self.ui.scale_guides_line.text()),
																				  float(self.ui.scale_guides_line.text())))
		self.ui.soft_cluster.clicked.connect(self.soft_cluster)
		self.ui.rivet_on_face.clicked.connect(self.rivet_on_face)

	# -------------------------------------------------------------------
	@undo
	def resize_guides(self, size):
		""" Make guides bigger or smaller

		Args:
			size: amount to mult the guides to

		Returns: None

		"""

		guides = cmds.ls('*{}'.format(nc['guide']))

		for g in guides:
			try:
				cmds.select('{}_Ctrl_CtrlShape.cv[0:101]'.format(g),
							'{}_Ctrl_Ctrl_Ctrl_CtrlShape.cv[0:9]'.format(g),
							'{}_Ctrl_Ctrl_CtrlShape.cv[0:9]'.format(g),
							'{}_CtrlShape.cv[0:9]'.format(g))

				cmds.scale(size, size, size, r=True)
			except:
				pass

		cmds.select(cl=True)

	def resize_Ctrls(self, size):
		""" Make ctrls bigger or smaller

		Args:
			size: amount to mult the guides to

		Returns: None

		"""

		ctrls = cmds.ls('*{}'.format(nc['ctrl']))

		for c in ctrls:
			try:
				shapes = cmds.listRelatives(c, s=True)
				for s in shapes:
					cmds.select('{}.cv[*]'.format(s))
					cmds.scale(size, size, size, r=True)
			except Exception as e:
				pass

		cmds.select(cl=True)

	@undo
	def toggle_axis(self, vis=True):
		""" Show or hide joints axis

		Args:
			vis: bool show or hide

		Returns: None

		"""
		# if no joints are selected, do it for all the joints in the scene
		if len(cmds.ls(sl=1, type="joint")) == 0:
			jointList = cmds.ls(type="joint")
		else:
			jointList = cmds.ls(sl=1, type="joint")

		# set the displayLocalAxis attribute to what the user specifies
		for jnt in jointList:
			cmds.setAttr(jnt + ".displayLocalAxis", vis)

	# -------------------------------------------------------------------
	@undo
	def toogle_contrainers(self, lock=True):
		"""Remove nodes from rig container and add them back based on settings file

		Args:
			lock: bool

		Returns: None

		"""
		try:settings = mh.read_json(path=os.path.join(cmds.internalVar(usd=True)), json_file='RigTools.settings')
		except: settings={}

		if lock == True:
			container_data = settings['Mutant_Rig_Nodes']
			for node in container_data:
				if cmds.objExists(node):
					try:
						cmds.container('Mutant_Rig', edit=True, addNode=node)
					except:
						pass
			print(os.path.join(cmds.internalVar(usd=True), 'RigTools.settings'))

		else:
			if not cmds.objExists('Mutant_Rig'):
				cmds.warning('No Mutant_Rig_Container in scene')
				return
			nodes = cmds.container('Mutant_Rig', query=True, nodeList=True)
			if nodes:
				for node in nodes:
					cmds.container('Mutant_Rig', edit=True, removeNode=node)
			else:
				nodes=[]

			settings['Mutant_Rig_Nodes'] = nodes
			mh.write_json(path=cmds.internalVar(usd=True), json_file='RigTools.settings', data=settings)

			print(os.path.join(cmds.internalVar(usd=True), 'RigTools.settings'))

	# -------------------------------------------------------------------
	@undo
	def hide_attrs(self):
		from Mutant_Tools.UI.RigTools.rdm2 import ShowHideAttr
		reload(ShowHideAttr)
		ShowHideAttr.hideSelection(hideT=self.ui.HideTranslateCheckBox.isChecked(),
								   hideR=self.ui.HideRotateCheckBox.isChecked(),
								   hideS=self.ui.HideScaleCheckBox.isChecked(),
								   hideV=self.ui.HideVisibilityCheckBox.isChecked())

	@undo
	def show_attrs(self):
		from Mutant_Tools.UI.RigTools.rdm2 import ShowHideAttr
		reload(ShowHideAttr)
		ShowHideAttr.showAll()

	# -------------------------------------------------------------------
	@undo
	def key_visemes(self):

		cmds.currentTime(0)

		#Remove Animation
		from Mutant_Tools.Utils.Animation import studio_library_utils
		reload(studio_library_utils)
		studio_library_utils.delete_keys()

		#Save as order dict
		from collections import OrderedDict
		animation = OrderedDict()

		#Set keys
		frame_dif = 10
		mult = self.ui.viseme_mult.value()

		animation['AEI'] =  {'L_Lips_Main_Ctrl' : [0.496, 0, 0.053, 0, 0, 0],
							'Lips_Up_Main_Ctrl': [0 ,0 ,0 ,0 ,0 ,0],
							'Lips_Dw_Main_Ctrl': [0, -0.528, 0, 0, 0, 0],
							'R_Lips_Main_Ctrl': [0.496, 0, 0.053, 0, 0, 0],
							}

		animation['OUW'] = {'L_Lips_Main_Ctrl': [-1.114, 0, -0.616, 0, 0, 0],
						   'Lips_Up_Main_Ctrl': [0, 0.291, 0, 0, 0, 0],
						   'Lips_Dw_Main_Ctrl': [0, -0.346, 0, 0, 0, 0],
						   'R_Lips_Main_Ctrl': [-1.114, 0, -0.616, 0, 0, 0],
						   }

		animation['FV'] = {'L_Lips_Main_Ctrl': [-0.128, 0, -0.071, 0, 0, 0],
						   'Lips_Up_Main_Ctrl': [0, 0.229, 0, 0, 0, 0],
						   'Lips_Dw_Main_Ctrl': [0, -0.028, -0.355, -24.053, 0, 0],
						   'R_Lips_Main_Ctrl': [-0.128, 0, -0.071, 0, 0, 0],
						   }

		animation['BMP'] = {'L_Lips_Main_Ctrl': [-0.168, 0, -0.093, 0, 0, 0],
						   'Lips_Up_Main_Ctrl': [-0.096, 0, -0.079, 96.061, 0, 0],
						   'Lips_Dw_Main_Ctrl': [-0.096, 0.038, -0.075, -69, 0, 0],
						   'R_Lips_Main_Ctrl': [-0.168, 0, -0.093, 0, 0, 0],
						   }

		animation['CDN'] = {'L_Lips_Main_Ctrl': [0.372, 0, 0.206, 0, 0, 0],
						   'Lips_Up_Main_Ctrl': [0, 0.102, 0, 0, 0, 0],
						   'Lips_Dw_Main_Ctrl': [0, -0.309, 0, 0, 0, 0],
						   'R_Lips_Main_Ctrl': [0.372, 0, 0.206, 0, 0, 0],
						   }


		for phoneme in animation:
			attrs_pos_dict = animation[phoneme]

			#Zero first
			for ctrl in attrs_pos_dict:
				cmds.select(ctrl)
				cmds.setAttr('{}.translateX'.format(ctrl), 0)
				cmds.setAttr('{}.translateY'.format(ctrl), 0)
				cmds.setAttr('{}.translateZ'.format(ctrl), 0)
				try:
					cmds.setAttr('{}.rotateX'.format(ctrl), 0)
					cmds.setAttr('{}.rotateY'.format(ctrl), 0)
					cmds.setAttr('{}.rotateZ'.format(ctrl), 0)
				except:
					pass

				cmds.select(ctrl)
				cmds.setKeyframe()

			current_time = cmds.currentTime(query=True)
			cmds.currentTime(current_time + frame_dif)

			#Animate it
			for ctrl in attrs_pos_dict:
				cmds.select(ctrl)
				tx, ty, tz, rx, ry, rz = attrs_pos_dict[ctrl]
				cmds.setAttr('{}.translateX'.format(ctrl), tx*mult)
				cmds.setAttr('{}.translateY'.format(ctrl), ty*mult)
				cmds.setAttr('{}.translateZ'.format(ctrl), tz*mult)
				try:
					cmds.setAttr('{}.rotateX'.format(ctrl), rx*mult)
					cmds.setAttr('{}.rotateY'.format(ctrl), ry*mult)
					cmds.setAttr('{}.rotateZ'.format(ctrl), rz*mult)
				except:
					pass
				cmds.select(ctrl)
				cmds.setKeyframe()

			current_time = cmds.currentTime(query=True)
			cmds.currentTime(current_time + frame_dif)

	@undo
	def bake_visemes(self):
		cmds.currentTime(0)

		selection = cmds.ls(sl=True)
		visemes_group = cmds.group(em=True, n='Visemes')

		if not selection:
			cmds.warning('Please select head geo')
			return

		for geo in selection:
			cmds.currentTime(10)
			AEI = cmds.duplicate(geo, n=geo+'_AEI')
			cmds.currentTime(30)
			OUW = cmds.duplicate(geo, n=geo+'_OUW')
			cmds.currentTime(50)
			FV = cmds.duplicate(geo, n=geo+'_FV')
			cmds.currentTime(70)
			BMP = cmds.duplicate(geo, n=geo+'_BMP')
			cmds.currentTime(90)
			CDN = cmds.duplicate(geo, n=geo+'_CDN')
			cmds.currentTime(0)

			cmds.parent(AEI,OUW,FV,BMP,CDN, visemes_group)

	def split_visemes(self):
		mel.eval('SHAPES;')

	@undo
	def load_blendshapes_from_sel(self):

		self.ui.shapes_combo.clear()

		selection = cmds.ls(sl=True)

		if not selection:
			cmds.warning('Please select head geo')
			return

		history_nodes = cmds.listHistory(selection[0])
		blendshape_nodes = cmds.ls(history_nodes, type = 'blendShape')

		self.ui.shapes_combo.addItems(blendshape_nodes)

	@undo
	def connect_visemes(self):
		selection = cmds.ls(sl=True)

		if not selection:
			cmds.warning('Please select head geo')
			return

		visemes = ['AEI','OUW','FV','BMP','CDN']

		bs_node = self.ui.shapes_combo.currentText()
		if not bs_node:
			cmds.warning('We need a blendshape node to connect')
			return

		for v in visemes:
			try:
				cmds.connectAttr('Mrg__{}_Ctrl.translateY'.format(v), '{}.{}_{}'.format(bs_node, selection[0], v), f=True)
				cmds.connectAttr('L__{}_Ctrl.translateX'.format(v), '{}.L_{}_{}'.format(bs_node, selection[0], v), f=True)
				cmds.connectAttr('R__{}_Ctrl.translateX'.format(v), '{}.R_{}_{}'.format(bs_node, selection[0], v), f=True)
			except:
				cmds.connectAttr('Mrg_{}_Ctrl.translateY'.format(v), '{}.{}_{}'.format(bs_node, selection[0], v), f=True)
				cmds.connectAttr('L_{}_Ctrl.translateX'.format(v), '{}.L_{}_{}'.format(bs_node, selection[0], v), f=True)
				cmds.connectAttr('R_{}_Ctrl.translateX'.format(v), '{}.R_{}_{}'.format(bs_node, selection[0], v), f=True)

		print('Finish Connecting Everything')

	def open_visemes_help(self):
		def open_website(website='http://mutanttools.com/', mode = 'view'):
			from Mutant_Tools.UI.WebsiteViewer import load_website_viewer
			reload(load_website_viewer)
			cWebsiteViewer = load_website_viewer.WebsiteViewerUI(website=website)
			if mode == 'view':
				cWebsiteViewer.show()
			else:
				cWebsiteViewer.open_link(website)

		open_website(website='https://stellarcreativelab.atlassian.net/wiki/spaces/WIKI/pages/2499772417/How+to+do+the+Rig+Visemes', mode='')

	@undo
	def tube_fk_chain(self):

		name = cmds.ls(sl=True)[0].split('.')[0]

		#mel.eval('SelectEdgeLoopSp')
		#mel.eval('SelectEdgeRingSp;')

		sel = cmds.ls(sl=True, fl=True)
		clusters = []
		for s in sel:
			cmds.select(s)
			clusters.append(cmds.cluster())

		if self.ui.flipJointCheckBox.isChecked():
			clusters = list(reversed(clusters))

		joints = []
		for num, c in enumerate(clusters):
			cmds.select(cl=True)
			j = cmds.joint()
			cmds.delete(cmds.parentConstraint(c, j))
			cmds.delete(c)
			joints.append(j)
			try:
				cmds.parent(j, joints[num - 1])
			except:
				pass

		cmds.select(joints)
		mel.eval('OrientJoint;')

		amount = self.ui.tubeAmountLabel.text()
		if amount == str(0):
			cmds.select(joints)
			mt.fk_chain(size=self.ui.SimpleFKSizeSlider.value(),
					color=self.ui.SimpleFKColorBox.currentText(),
					curve_type=self.ui.SimpleFKShapeBox.currentText())
		else:
			ik_spline = cmds.ikHandle(sj=joints[0],
									  ee=joints[-1],
									  sol='ikSplineSolver',
									  createCurve=True,
									  parentCurve=False
									  )
			curve=ik_spline[-1]
			new_curve = mel.eval('rebuildCurve -ch 1 -rpo 1 -rt 0 -end 1 -kr 0 -kcp 0 -kep 1 -kt 0 -s {} -d 1 -tol 0.0001 "{}";'.format(amount, curve))[0]
			cmds.delete(ik_spline[0], ik_spline[1])
			cmds.delete(joints)

			curveCVs = cmds.ls('%s.cv[:]' % new_curve, fl=True)
			new_joints = []
			if self.ui.flipJointCheckBox.isChecked():
				curveCVs = list(reversed(curveCVs))

			for num, cv in enumerate(curveCVs):
				[(x, y, z)] = cmds.getAttr(cv)
				j = cmds.joint(n=name+'_'+str(num)+nc['joint'])
				cmds.move(x, y, z, cmds.ls(sl=True))
				new_joints.append(j)

			cmds.select(new_joints)
			mel.eval('OrientJoint;')
			cmds.delete(curve)

			cmds.select(new_joints)
			mt.fk_chain(size=self.ui.SimpleFKSizeSlider.value(),
						color=self.ui.SimpleFKColorBox.currentText(),
						curve_type=self.ui.SimpleFKShapeBox.currentText())

	@undo
	def pupulate_tongue_eyes(self):
		self.ui.tongue_eyes_edit.setText(self.clean_selection(sel=cmds.ls(sl=True)))

	def clean_selection(self, sel):
		clean_sel = str(sel)[1:-1]
		clean_sel = clean_sel.replace("u'", "'")
		clean_sel = clean_sel.replace("'", "")
		return clean_sel

	@undo
	def fix_shove_issue(self):
		import maya.cmds as cmds
		import maya.mel as mel

		GEO_PARENT = 'geo'
		GLOBAL_CONTROL = 'Mover_Gimbal_Ctrl'

		def make_joints_matrix_local(skin_cluster):
			from mstar.nodes.mayaNode import MayaNode
			print(skin_cluster)
			global_ctrl = MayaNode(GLOBAL_CONTROL)
			skin_cluster = MayaNode(sc)
			# joint, connections list
			cons = iter(skin_cluster.listConnections('matrix', c=True, p=True))
			for attr, joint in zip(cons, cons):
				print(joint)
				joint = MayaNode(joint.split('.')[0])
				mult_matrix = MayaNode(cmds.createNode('multMatrix'))
				# cmds.connectAttr('{}.parentInverseMatrix[0]'.format(global_ctrl), '{}.matrixIn[0]'.format(mult_matrix), f=True)
				cmds.connectAttr('{}.worldMatrix[0]'.format(joint), '{}.matrixIn[0]'.format(mult_matrix), f=True)
				cmds.connectAttr('{}.worldInverseMatrix[0]'.format(global_ctrl), '{}.matrixIn[1]'.format(mult_matrix),
								 f=True)
				cmds.connectAttr('{}.matrixSum'.format(mult_matrix), attr, f=True)

		# get children geo group and extract their skin cluster name

		geo_children = cmds.listRelatives(GEO_PARENT, ad=1, type='transform')

		# hard coded names of tongue and teeth face geo
		tongue_eyes_text = self.ui.tongue_eyes_edit.text()
		if tongue_eyes_text:
			extra_geos = tongue_eyes_text.replace(' ','').split(',')
			for geo in extra_geos:
				if cmds.objExists(geo):
					geo_children.append(geo)
		# geo_children.extend([u'Face_C_Tongue_Geo', u'Face_C_GumsBottom_Geo', u'Face_C_GumsTop_Geo', u'Face_C_ToothTop_Geo', u'Face_C_ToothBottom_Geo'])


		skin_clusters = []
		for i in geo_children:
			sc = mel.eval('findRelatedSkinCluster {}'.format(i))
			if sc:
				skin_clusters.append(sc)

		for sc in skin_clusters:
			make_joints_matrix_local(sc)

		cmds.parentConstraint(GLOBAL_CONTROL, GEO_PARENT, mo=1)

	@undo
	def auto_rotate_fk(self):
		axis = 'Y'
		fk_system = mt.fk_chain(input='',
								size=self.ui.SimpleFKSizeSlider.value(),
								color=self.ui.SimpleFKColorBox.currentText(),
								curve_type=self.ui.SimpleFKShapeBox.currentText(),
								scale=True,
								twist_axis=axis,
								world_orient=False)
		ctrl_root = cmds.listRelatives(fk_system[0], p=1)[0]
		mt.create_auto_rotate_fk(fk_system[0], ctrl_root, self.ui.SimpleFKSizeSlider.value()*1.5)

	@undo
	def connect_to_scale_reader(self):
		type = cmds.objectType(cmds.ls(sl=True)[0])
		attrs = [".sx", ".sy", ".sz"]

		if type == "deltaMush":
			for attr in attrs:
				cmds.connectAttr("scale_reader{}".format(attr), "{}{}".format(cmds.ls(sl=True)[0], attr))

		else:
			sel = cmds.ls(sl=True)
			for num in range(0, len(sel)):
				cmds.scaleConstraint("scale_reader", sel[num], mo=True)

	@undo
	def scale_mutant_template(self, amountX, amountY, amountZ):

		# Getting all scalable objects from template grp
		mutant_build_grp = cmds.ls("Mutant_Build", l=True)
		if len(mutant_build_grp) < 1:
			cmds.error("No Mutant_Build_grp in scene to scale.")
		elif len(mutant_build_grp) > 1:
			cmds.error("More than one Mutant_Build_grp in scene.")

		# Getting all elements inside the build group.
		mutant_build_elements = cmds.listRelatives(mutant_build_grp, ad=True)
		mutant_build_elements.reverse()

		# separating elements into joint guides.
		mutant_joint_guides = cmds.ls(mutant_build_elements, type="joint")

		# separating elements into locator guides.
		mutant_locator_guides = []
		mutant_locator_shapes = cmds.ls(mutant_build_elements, type="locator")
		for shape in mutant_locator_shapes:  # Getting parent translate from locator shape.
			shape_parent = cmds.listRelatives(shape, parent=True)[0]
			mutant_locator_guides.append(shape_parent)

		# separating elements into nurb guides.
		mutant_nurb_guides = []
		for element in mutant_build_elements:
			if element.endswith("_Guide"):
				if cmds.nodeType(cmds.listRelatives(element, shapes=True)) == "nurbsSurface":  # Filtering non-nurbs
					mutant_nurb_guides.append(element)

		# Duplicates the guides with a different suffix and places the copies inside a new group to be scaled.
		def guide_to_scale(sel):
			if sel == []:
				pass

			else:
				if cmds.objExists("Scale_this_temp_grp"):
					grp = "Scale_this_temp_grp"
				else:
					grp = cmds.group(n="Scale_this_temp_grp", em=True)

				for each in sel:
					if cmds.objExists(each):
						loc = cmds.spaceLocator(n=each.replace("_Guide", "_Scale_Loc"))
						cmds.matchTransform(loc, each, pos=True, rot=True)
						cmds.parent(loc, grp)
					else:
						sel.remove(each)

		# Duplicates the locators with a different suffix and places the copies inside a new group to be scaled.
		def loc_to_scale(sel):
			if sel == []:
				pass

			else:
				if cmds.objExists("Scale_this_temp_grp"):
					grp = "Scale_this_temp_grp"
				else:
					grp = cmds.group(n="Scale_this_temp_grp", em=True)

				for each in sel:
					if cmds.objExists(each):
						loc = cmds.spaceLocator(n=each.replace("_Loc", "_Scale_Loc"))
						cmds.matchTransform(loc, each, pos=True, rot=True)
						cmds.parent(loc, grp)
					else:
						sel.remove(each)

		# Duplicates the nurbs with a different suffix and places the copies inside a new group to be scaled.
		def nurb_to_scale(sel):
			if sel == []:
				pass

			else:
				if cmds.objExists("Scale_this_temp_grp"):
					grp = "Scale_this_temp_grp"
				else:
					grp = cmds.group(n="Scale_this_temp_grp", em=True)

				for each in sel:
					if cmds.objExists(each):
						loc = cmds.spaceLocator(n=each.replace("_Guide", "_Scale_Loc"))
						cmds.matchTransform(loc, each, pos=True, rot=True, scl=True)
						cmds.parent(loc, grp)
					else:
						sel.remove(each)

		# Scales the group of the new guides.
		def scale_locs(numX, numY, numZ):
			cmds.setAttr("Scale_this_temp_grp.scaleZ", numX)
			cmds.setAttr("Scale_this_temp_grp.scaleX", numY)
			cmds.setAttr("Scale_this_temp_grp.scaleY", numZ)

		# Matches the position and rotation of the old guides with the new ones "scaling" them.
		def scale_but_not_quite_guide(sel):
			for each in sel:
				if cmds.objExists(each):
					cmds.matchTransform(each, each.replace("_Guide", "_Scale_Loc"), pos=True, rot=True)

				# Matches the position and rotation of the old locators with the new ones "scaling" them.

		def scale_but_not_quite_loc(sel):
			for each in sel:
				if cmds.objExists(each):
					cmds.matchTransform(each, each.replace("_Loc", "_Scale_Loc"), pos=True, rot=True)

				# Matches the position, scale and rotation of the old nurbs with the new ones.

		def scale_but_not_quite_nurb(sel):
			for each in sel:
				if cmds.objExists(each):
					cmds.matchTransform(each, each.replace("_Guide", "_Scale_Loc"), pos=True, rot=True, scl=True)

				# Trigger actions.

		guide_to_scale(mutant_joint_guides)
		loc_to_scale(mutant_locator_guides)
		nurb_to_scale(mutant_nurb_guides)

		scale_locs(amountX, amountY, amountZ)

		scale_but_not_quite_guide(mutant_joint_guides)
		scale_but_not_quite_loc(mutant_locator_guides)
		scale_but_not_quite_nurb(mutant_nurb_guides)

		cmds.delete("Scale_this_temp_grp")

		print("The mutant template has been scaled by [{}, {}, {}]. You're awesome!".format(amountX, amountY, amountZ))

	#

	@undo
	def soft_cluster(self):
		import maya.cmds as mc
		import maya.OpenMaya as om

		def softSelection():
			selection = om.MSelectionList()
			softSelection = om.MRichSelection()
			om.MGlobal.getRichSelection(softSelection)
			softSelection.getSelection(selection)

			dagPath = om.MDagPath()
			component = om.MObject()

			iter = om.MItSelectionList(selection, om.MFn.kMeshVertComponent)
			elements = []
			while not iter.isDone():
				iter.getDagPath(dagPath, component)
				dagPath.pop()
				node = dagPath.fullPathName()
				fnComp = om.MFnSingleIndexedComponent(component)

				for i in range(fnComp.elementCount()):
					elements.append([node, fnComp.element(i), fnComp.weight(i).influence()])
				next(iter)
			return elements

		def createSoftCluster():
			softElementData = softSelection()
			selection = ["%s.vtx[%d]" % (el[0], el[1]) for el in softElementData]

			mc.select(selection, r=True)
			cluster = mc.cluster(relative=True, bf=True)

			for i in range(len(softElementData)):
				mc.percent(cluster[0], selection[i], v=softElementData[i][2])
			mc.select(cluster[1], r=True)
			return cluster

		deformer, handle = createSoftCluster()


	@undo
	def rivet_on_face(self):
		sel = cmds.ls(sl=True)
		print(sel)
		pins = mt.rivet_constraint(sel)
		print(pins)


	@undo
	def create_dynamic_fk_ui(self):
		mt.create_dynamic_fk()

	# CLOSE EVENTS _________________________________
	def closeEvent(self, event):
		''


# -------------------------------------------------------------------

if __name__ == "__main__":

	try:
		ToolsTab.close()  # pylint: disable=E0601
		ToolsTab.deleteLater()
	except:
		pass
	cTools_ui = ToolsTab()
	cTools_ui.show()

# -------------------------------------------------------------------

