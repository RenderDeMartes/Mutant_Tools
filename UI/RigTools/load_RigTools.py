'''
version: 1.0.0
date: 21/04/2020

#----------------
content:

#----------------
how to:

import imp
import Mutant_Tools
from Mutant_Tools.UI.RigTools import load_RigTools
imp.reload(load_RigTools)

try:cRigToolsUI.close()
except:pass
cRigToolsUI = load_RigTools.RigTools_UI()
cRigToolsUI.show()

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
import imp
import sys
import json
import glob
import pprint
from pathlib import Path


# -------------------------------------------------------------------

# QT WIndow!
FOLDER_NAME = 'RigTools'
PATH = os.path.dirname(__file__)
BLOCKS_PATH = PATH.replace('\\UI\\{}'.format(FOLDER_NAME), '//Blocks')  # get Blocks paths to write files

Title = 'RigTools'
Folder = PATH.replace('\\UI\\{}'.format(FOLDER_NAME), '')
UI_File = 'RigTools.ui'
IconsPath = Folder + '//Icons//'

# -------------------------------------------------------------------

# Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = PATH.replace('\\UI\\{}'.format(FOLDER_NAME), '//Config')  # change this path depending of the folder

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

import Mutant_Tools
import Mutant_Tools.Utils
from Mutant_Tools.Utils.Rigging import main_mutant

imp.reload(Mutant_Tools.Utils.Rigging.main_mutant)
mt = main_mutant.Mutant()

import Mutant_Tools.UI
from Mutant_Tools.UI import QtMutantWindow
imp.reload(QtMutantWindow)
Qt_Mutant = QtMutantWindow.Qt_Mutant()

import Mutant_Tools.Utils.Helpers
from Mutant_Tools.Utils.Helpers import helpers
imp.reload(Mutant_Tools.Utils.Helpers.helpers)
mh = helpers.Helpers()

# -------------------------------------------------------------------

rig_tab= {
	'0':{'code': 'CreateLocator',
		  'icon': 'locator.png',
		  'tooltip': 'Create Locator: Create a locator object on the grid',
		  'double_click' : 'None'},
	'1':{'code': 'JointTool',
		  'icon': 'kinJoint.png',
		  'tooltip': 'Create Joints: Click to place joint, click on existing joint to add to skeleton, click/drag to position joint',
		  'double_click' : 'JointToolOptions'},
	'2': {'code': 'IKHandleTool',
		  'icon': 'kinHandle.png',
		  'tooltip': 'Create IK Handle: Create IK handle on joint chain',
		   'double_click' : 'IKHandleToolOptions'},
	'3':{'code': 'SmoothBindSkin',
		  'icon': 'smoothSkin.png',
		  'tooltip': 'Bind Skin: Smooth bind skin',
		  'double_click' : 'SmoothBindSkinOptions'},
	'4':{'code': 'QuickRigEditor',
		  'icon': 'QR_QuickRigTool.png',
		  'tooltip': 'Quick Rig: Opens the Quick Rig tool, a quick character rigging tool which outputs an HIK rig',
		  'double_click' : 'None'},
	'5':{'code': 'HIKCharacterControlsTool',
		  'icon': 'humanIK_CharCtrl.png',
		  'tooltip': 'Human IK: Display the character controls window',
		  'double_click' : 'None'},
	'6':{'code': 'ArtPaintSkinWeightsTool',
		  'icon': 'paintSkinWeights.png',
		  'tooltip': 'Paint Skin Weights: Paint weights on smooth bound skins',
		  'double_click' : 'ArtPaintSkinWeightsToolOptions'},
	'7':{'code': 'CreateBlendShape',
		  'icon': 'blendShape.png',
		  'tooltip': 'Blend Shapes: Create a new Blend Shape on an object/group that can blend between other deformations / the original mesh shape.',
		  'double_click' : 'CreateBlendShapeOptions'},
	'8':{'code': 'CreateLattice',
		  'icon': 'lattice.png',
		  'tooltip': "Create Lattice: Surrounds geometry with a flexible grid that you can use to change the object's shape.",
		  'double_click' : 'CreateLatticeOptions'},
	'9':{'code': 'CreateCluster',
		  'icon': 'cluster.png',
		  'tooltip': 'Create Cluster: Creates a transform driven deformation for a set of points on an object (CVs, vertices, or lattice points).',
		  'double_click' : 'CreateClusterOptions'},
	'10': {'code': 'ParentConstraint',
		  'icon': 'parentConstraint.png',
		  'tooltip': 'Parent Constraint: Constrain one object to the position/orientation/scale of another.',
		  'double_click' : 'ParentConstraintOptions'},
	'11':{'code': 'PointConstraint',
		  'icon': 'posConstraint.png',
		  'tooltip': 'Point Constraint: Constrain one object to the position of another.',
		  'double_click' : 'PointConstraintOptions'},
	'12':{'code': 'OrientConstraint',
		  'icon': 'orientConstraint.png',
		  'tooltip': 'Orient Constraint: Constrain one object to the orientation of another.',
		  'double_click' : 'OrientConstraintOptions'},
	'13':{'code': 'ScaleConstraint',
		  'icon': 'scaleConstraint.png',
		  'tooltip': 'Scale Constraint: Constrain one object to the scale of another.',
		  'double_click' : 'ScaleConstraintOptions'},
	'14': {'code': 'AimConstraint',
		  'icon': 'aimConstraint.png',
		  'tooltip': 'Aim Constraint: Constrain one mesh to always point towards another.',
		  'double_click' : 'AimConstraintOptions'},
	'15': {'code': 'PoleVectorConstraint',
		  'icon': 'poleVectorConstraint.png',
		  'tooltip': 'Pole Vector Constraint: Constrain the end of an IK handle to follow the position of an object.',
		  'double_click' : 'PoleVectorConstraintOptions'},
	'16':{'code': 'SetKey',
		  'icon': 'setKeyframe.png',
		  'tooltip': 'Set Key: Sets a keyframe on all channels that are selected.',
		  'double_click' : 'SetKeyOptions'},
	'17':{'code': 'SetDrivenKey',
		  'icon': 'setDrivenKeyframe.png',
		  'tooltip': "Set Driven Key: Opens the Set Driven Key window; driven keys use one object's attribute(s) to drive the animation of other attribute(s)",
		  'double_click' : 'None'}
	}

sculpting_tab = {
	'0': {'code': 'SetMeshSculptTool',
		   'icon': 'Sculpt.png',
		   'tooltip': "Lift a surface",
		   'double_click': 'ShowMeshSculptToolOptions'},
	'1': {'code': 'SetMeshSmoothTool',
		   'icon': 'Smooth.png',
		   'tooltip': "Smooth the surface of a mesh.",
		   'double_click': 'ShowMeshSmoothToolOptions'},
	'2': {'code': 'SetMeshRelaxTool',
		   'icon': 'Relax.png',
		   'tooltip': "Smooth the surface of a mesh without changing its original shape.",
		   'double_click': 'ShowMeshRelaxToolOptions'},
	'3': {'code': 'SetMeshGrabTool',
		   'icon': 'Grab.png',
		   'tooltip': "Pull a single vertex along a surface in any direction",
		   'double_click': 'ShowMeshGrabToolOptions'},
	'4': {'code': 'SetMeshPinchTool',
		  'icon': 'Pinch.png',
		  'tooltip': "Sharpen soft edges",
		  'double_click': 'ShowMeshPinchToolOptions'},
	'5': {'code': 'SetMeshFlattenTool',
		  'icon': 'Flatten.png',
		  'tooltip': "Level a surface",
		  'double_click': 'ShowMeshFlattenToolOptions'},
	'6': {'code': 'SetMeshFoamyTool',
		  'icon': 'Foamy.png',
		  'tooltip': "Softly lift a surface.",
		  'double_click': 'ShowMeshFoamyToolOptions'},
	'7': {'code': 'SetMeshSprayTool',
		  'icon': 'Spray.png',
		  'tooltip': "Randomly spray a stamp imprint on a surface",
		  'double_click': 'ShowMeshSprayToolOptions'},
	'8': {'code': 'SetMeshRepeatTool',
		  'icon': 'Repeat.png',
		  'tooltip': "Stamp a pattern on a surface repeatedly.",
		  'double_click': 'ShowMeshRepeatToolOptions'},
	'9': {'code': 'SetMeshImprintTool',
		  'icon': 'Imprint.png',
		  'tooltip': "Imprint a single copy of a stamp on a surface",
		  'double_click': 'ShowMeshImprintToolOptions'},
	'10': {'code': 'SetMeshWaxTool',
		  'icon': 'Wax.png',
		  'tooltip': "Build up a surface",
		  'double_click': 'ShowMeshWaxToolOptions'},
	'11': {'code': 'SetMeshScrapeTool',
		  'icon': 'Scrape.png',
		  'tooltip': "Minimize or remove raised areas on a surface",
		  'double_click': 'ShowMeshScrapeToolOptions'},
	'12': {'code': 'SetMeshFillTool',
		  'icon': 'Fill.png',
		  'tooltip': "Fill in the valleys on a surface",
		  'double_click': 'ShowMeshFillToolOptions'},
	'13': {'code': 'SetMeshKnifeTool',
		  'icon': 'Knife.png',
		  'tooltip': "Cut fine strokes into a surface",
		  'double_click': 'ShowMeshKnifeToolOptions'},
	'14': {'code': 'SetMeshSmearTool',
		  'icon': 'Smear.png',
		  'tooltip': "Pull a surface in the direction of the stroke",
		  'double_click': 'ShowMeshSmearToolOptions'},
	'15': {'code': 'SetMeshBulgeTool',
		  'icon': 'Bulge.png',
		  'tooltip': "Inflate an area on a surface",
		  'double_click': 'ShowMeshBulgeToolOptions'},
	'16': {'code': 'SetMeshAmplifyTool',
		  'icon': 'Amplify.png',
		  'tooltip': "Accentuate surface detail",
		  'double_click': 'ShowMeshAmplifyToolOptions'},
	'17': {'code': 'SetMeshFreezeTool',
		  'icon': 'Freeze.png',
		  'tooltip': "Paint areas of a surface to prevent further modification",
		  'double_click': 'ShowMeshFreezeToolOptions'},
	'18': {'code': 'ConvertToFrozen',
		  'icon': 'freezeSelected.png',
		  'tooltip': "Convert To Frozen",
		  'double_click': 'None'},
	'19': {'code': 'OpenVisorForMeshes',
		  'icon': 'contentBrowserGeneric.png',
		  'tooltip': "Open Content Browser for Sculpting Base Meshes",
		  'double_click': 'None'},
	'20': {'code': 'ShapeEditor',
		  'icon': 'blendShapeEditor.png',
		  'tooltip': "Shape Editor: ",
		  'double_click': 'CreateBlendShapeOptions'},
	'21': {'code': 'PoseEditor',
		  'icon': 'poseEditor.png',
		  'tooltip': "Pose Editor: Create, edit and manage pose space deformations",
		  'double_click': 'None'},
	'22': {'code': 'SetMeshSmoothTargetTool',
		  'icon': 'SmoothTarget.png',
		  'tooltip': "Smooth Target Tool: Even out surface detail only for the current blend shape target in Edit mode",
		  'double_click': 'ShowMeshSmoothTargetToolOptions'},
	'23': {'code': 'SetMeshCloneTargetTool',
		  'icon': 'CloneTarget.png',
		  'tooltip': "Clone Target Tool: Copy edits from a blend shape target source to the current target in Edit mode",
		  'double_click': 'ShowMeshCloneTargetToolOptions'},
	'24': {'code': 'SetMeshMaskTool',
		  'icon': 'Mask.png',
		  'tooltip': "Mask Target Tool: Paint areas on a mesh to hide edits for the current blend shape target in Edit mode",
		  'double_click': 'ShowMeshMaskToolOptions'},
	'25': {'code': 'SetMeshEraseTool',
		  'icon': 'Erase.png',
		  'tooltip': "Erase Target Tool: Remove edits for the current blend shape target in Edit mode",
		  'double_click': 'ShowMeshEraseToolOptions'}
	}

separators_before = ['SetMeshSmoothTargetTool','ShapeEditor','ConvertToFrozen','ArtPaintSkinWeightsTool','ParentConstraint','SetKey']

#----------------------------------------------------------------------------------------------------
#icons missing: humanIK_CharCtrl.png
def get_icons():
	for item in cmds.resourceManager(nf='*png'):
		cmds.resourceManager(
			s=(item, "C:\\Users\\PC\\Documents\\maya\\2022\\scripts\\Mutant_Tools\\Icons\\MayaIcons\\{0}".format(item)))

	for num, i in enumerate(rig_tab):
		used_icons.append(rig_tab[str(num)]['icon'])
	for num, i in enumerate(sculpting_tab):
		used_icons.append(sculpting_tab[str(num)]['icon'])

	from shutil import copyfile
	for icon in used_icons:
		try:
			src = 'C:\\Users\\PC\\Documents\\maya\\2022\\scripts\\Mutant_Tools\\Icons\\MayaIcons\\' + icon
			dst = 'C:\\Users\\PC\\Documents\\maya\\2022\\scripts\\Mutant_Tools\\Icons\\MayaIcons\\used\\' + icon
			copyfile(src, dst)
			print(icon)
		except:
			print('error with:', icon)
			pass

# -------------------------------------------------------------------

class RigTools_UI(QtMutantWindow.Qt_Mutant):

	def __init__(self):
		super(RigTools_UI, self).__init__()

		self.setWindowTitle(Title)

		self.designer_loader_child(path=Folder + '/UI/{}/'.format(FOLDER_NAME), ui_file=UI_File)
		self.set_title(Title)

		self.resize(680,600)

		self.create_layout()
		self.create_connections()

	# -------------------------------------------------------------------

	def create_layout(self):
		"""

		Returns:

		"""
		self.ui.sculpt_frame.hide()
		self.ui.rig_frame.hide()
		self.populate_ui_shelf(rig_tab, self.ui.rig_shelf)
		self.populate_ui_shelf(sculpting_tab, self.ui.sculpt_shelf)


	def create_connections(self):
		"""

		Returns:

		"""

		self.ui.hide_shelfs.clicked.connect(self.toggle_shelfs_vis)
		self.ui.smallerGuideBtn.clicked.connect(lambda: self.resize_guides(0.75))
		self.ui.biggerGuideBtn.clicked.connect(lambda: self.resize_guides(1.25))
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


	def toggle_shelfs_vis(self):
		""" Show or hide fake rigging and sculting shelfs

		Returns:

		"""
		if self.ui.sculpt_frame.isVisible():
			self.ui.sculpt_frame.hide()
			self.ui.rig_frame.hide()
		else:
			self.ui.sculpt_frame.show()
			self.ui.rig_frame.show()

	def populate_ui_shelf(self, dict_data, layout):
		""" Populate shelfs that mimic riging and sculting of native maya

		Args:
			dict_data: dict data with icons, functions and names to put as butons
			layout: where to put the shelf in the qt ui from designer

		Returns: None

		"""
		for num in dict_data:
			button_data = dict_data[num]


			code = button_data['code']
			icon = button_data['icon']
			tooltip = button_data['tooltip']
			double_click = button_data['double_click']

			if code in separators_before:
				separator = self.create_vertical_separator()
				layout.addWidget(separator)

			button = QtWidgets.QPushButton()
			button.setMinimumSize(30,30)
			button.setIcon(QtGui.QIcon(IconsPath + 'MayaIcons//{}'.format(icon)))
			button.setIconSize(QtCore.QSize(30,30))
			button.setToolTip(tooltip)
			#connect button
			button.installEventFilter(self)
			button.clicked.connect(partial(self.shelf_click, code))
			button.setObjectName(double_click)

			#add to layout
			layout.addWidget(button)

	#stole event filler and add right click as obj name
	def eventFilter(self, obj, event):
		if event.type() == QtCore.QEvent.MouseButtonPress:
			if event.button() == QtCore.Qt.LeftButton:
				pass
			elif event.button() == QtCore.Qt.RightButton:
				try:mel.eval(obj.objectName())
				except:pass
		return QtCore.QObject.event(obj, event)

	def shelf_click(self, mel_code):
		mel.eval(mel_code)

	def resize_guides(self, size):
		""" Make guides bigger or smaller

		Args:
			size: amount to mult the guides to

		Returns: None

		"""

		guides= cmds.ls('*{}'.format(nc['guide']))

		for g in guides:
			cmds.select('{}_Ctrl_CtrlShape.cv[0:101]'.format(g),
						'{}_Ctrl_Ctrl_Ctrl_CtrlShape.cv[0:9]'.format(g),
						'{}_Ctrl_Ctrl_CtrlShape.cv[0:9]'.format(g),
						'{}_CtrlShape.cv[0:9]'.format(g))

			cmds.scale(size,size,size, r=True)

		cmds.select(cl=True)


	def toggle_axis(self, vis = True):
		""" Show or hide joints axis

		Args:
			vis: bool show or hide

		Returns: None

		"""
		#if no joints are selected, do it for all the joints in the scene
		if len(cmds.ls(sl=1, type="joint")) == 0:
			jointList = cmds.ls(type="joint")
		else:
			jointList = cmds.ls(sl=1, type="joint")

		#set the displayLocalAxis attribute to what the user specifies
		for jnt in jointList:
			cmds.setAttr(jnt + ".displayLocalAxis", vis)

	# -------------------------------------------------------------------

	def toogle_contrainers(self, lock=True):
		"""Remove nodes from rig container and add them back based on settings file

		Args:
			lock: bool

		Returns: None

		"""
		settings = mh.read_json(os.path.dirname(__file__) + '\\', 'RigTools.settings')

		if lock == True:
			container_data = settings['Mutant_Rig_Nodes']
			for node in container_data:
				if cmds.objExists(node):
					try:cmds.container('Mutant_Rig', edit=True, addNode=node)
					except:pass

		else:
			if not cmds.objExists('Mutant_Rig'):
				cmds.warning('No Mutant_Rig_Container in scene')
				return
			nodes = cmds.container('Mutant_Rig', query=True, nodeList=True)
			for node in nodes:
				cmds.container('Mutant_Rig', edit=True, removeNode=node)

			settings['Mutant_Rig_Nodes'] = nodes
			mh.write_json(os.path.dirname(__file__) + '\\', 'RigTools.settings', settings)

	# -------------------------------------------------------------------

	def hide_attrs(self):
		from Mutant_Tools.UI.RigTools.rdm2 import ShowHideAttr
		imp.reload(ShowHideAttr)
		ShowHideAttr.hideSelection(hideT=self.ui.HideTranslateCheckBox.isChecked(),
					  hideR=self.ui.HideRotateCheckBox.isChecked(),
					  hideS=self.ui.HideScaleCheckBox.isChecked(),
					  hideV=self.ui.HideVisibilityCheckBox.isChecked())

	def show_attrs(self):
		from Mutant_Tools.UI.RigTools.rdm2 import ShowHideAttr
		imp.reload(ShowHideAttr)
		ShowHideAttr.showAll()

	# -------------------------------------------------------------------



	# -------------------------------------------------------------------
	# -------------------------------------------------------------------
	# -------------------------------------------------------------------


	# CLOSE EVENTS _________________________________
	def closeEvent(self, event):
		''


# -------------------------------------------------------------------

if __name__ == "__main__":

	try:
		cRigToolsUI.close()  # pylint: disable=E0601
		cRigToolsUI.deleteLater()
	except:
		pass
	cRigToolsUI = RigTools_UI()
	cRigToolsUI.show()

# -------------------------------------------------------------------

'''
#Notes






'''