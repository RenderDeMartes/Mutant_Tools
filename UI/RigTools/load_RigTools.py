'''
version: 1.0.0
date: 21/04/2020

#----------------
content:

#----------------
how to:

import imp
import Mutant_Tools
from Mutant_Tools.UI.FolderName import load_pyname
imp.reload(load_pyname)

try:cMutantUI.close()
except:pass
cMutantUI = load_pyname.MutantUI()
cMutantUI.show()

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


# -------------------------------------------------------------------

# QT WIndow!
FOLDER_NAME = 'folder_name_here'
PATH = os.path.dirname(__file__)
BLOCKS_PATH = PATH.replace('\\UI\\{}'.format(FOLDER_NAME), '//Blocks')  # get Blocks paths to write files

Title = 'Mutant || Mutant'
Folder = PATH.replace('\\UI\\{}'.format(FOLDER_NAME), '')
UI_File = 'FILE_NAME_HERE.ui'
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



# -------------------------------------------------------------------

rig_tab= {
	'00':{'code': 'CreateLocator',
		  'icon': 'locator.png',
		  'tooltip': 'Create Locator: Create a locator object on the grid',
		  'double_click' : 'None'},
	'01':{'code': 'JointTool',
		  'icon': 'kinJoint.png',
		  'tooltip': 'Create Joints: Click to place joint, click on existing joint to add to skeleton, click/drag to position joint',
		  'double_click' : 'JointToolOptions'},
	'02': {'code': 'IKHandleTool',
		  'icon': 'kinHandle.png',
		  'tooltip': 'Create IK Handle: Create IK handle on joint chain',
		   'double_click' : 'IKHandleToolOptions'},
	'03':{'code': 'SmoothBindSkin',
		  'icon': 'smoothSkin.png',
		  'tooltip': 'Bind Skin: Smooth bind skin',
		  'double_click' : 'SmoothBindSkinOptions'},
	'04':{'code': 'QuickRigEditor',
		  'icon': 'QR_QuickRigTool.png',
		  'tooltip': 'Quick Rig: Opens the Quick Rig tool, a quick character rigging tool which outputs an HIK rig',
		  'double_click' : 'None'},
	'05':{'code': 'HIKCharacterControlsTool',
		  'icon': 'humanIK_CharCtrl.png',
		  'tooltip': 'Human IK: Display the character controls window',
		  'double_click' : 'None'},
	'06':{'code': 'ArtPaintSkinWeightsTool',
		  'icon': 'paintSkinWeights.png',
		  'tooltip': 'Paint Skin Weights: Paint weights on smooth bound skins',
		  'double_click' : 'ArtPaintSkinWeightsToolOptions'},
	'07':{'code': 'CreateBlendShape',
		  'icon': 'blendShape.png',
		  'tooltip': 'Blend Shapes: Create a new Blend Shape on an object/group that can blend between other deformations / the original mesh shape.',
		  'double_click' : 'CreateBlendShapeOptions'},
	'08':{'code': 'CreateLattice',
		  'icon': 'lattice.png',
		  'tooltip': "Create Lattice: Surrounds geometry with a flexible grid that you can use to change the object's shape.",
		  'double_click' : 'CreateLatticeOptions'},
	'09':{'code': 'CreateCluster',
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
	'01': {'code': 'SetMeshSculptTool',
		   'icon': 'Sculpt.png',
		   'tooltip': "Lift a surface",
		   'double_click': 'ShowMeshSculptToolOptions'},
	'02': {'code': 'SetMeshSmoothTool',
		   'icon': 'Smooth.png',
		   'tooltip': "Smooth the surface of a mesh.",
		   'double_click': 'ShowMeshSmoothToolOptions'},
	'03': {'code': 'SetMeshRelaxTool',
		   'icon': 'Relax.png',
		   'tooltip': "Smooth the surface of a mesh without changing its original shape.",
		   'double_click': 'ShowMeshRelaxToolOptions'},
	'04': {'code': 'SetMeshGrabTool',
		   'icon': 'Grab.png',
		   'tooltip': "Pull a single vertex along a surface in any direction",
		   'double_click': 'ShowMeshGrabToolOptions'},
	'05': {'code': 'SetMeshPinchTool',
		  'icon': 'Pinch.png',
		  'tooltip': "Sharpen soft edges",
		  'double_click': 'ShowMeshPinchToolOptions'},
	'06': {'code': 'SetMeshFlattenTool',
		  'icon': 'Flatten.png',
		  'tooltip': "Level a surface",
		  'double_click': 'ShowMeshFlattenToolOptions'},
	'07': {'code': 'SetMeshFoamyTool',
		  'icon': 'Foamy.png',
		  'tooltip': "Softly lift a surface.",
		  'double_click': 'ShowMeshFoamyToolOptions'},
	'08': {'code': 'SetMeshSprayTool',
		  'icon': 'Spray.png',
		  'tooltip': "Randomly spray a stamp imprint on a surface",
		  'double_click': 'ShowMeshSprayToolOptions'},
	'09': {'code': 'SetMeshRepeatTool',
		  'icon': 'Repeat.png',
		  'tooltip': "Stamp a pattern on a surface repeatedly.",
		  'double_click': 'ShowMeshRepeatToolOptions'},
	'10': {'code': 'SetMeshImprintTool',
		  'icon': 'Imprint.png',
		  'tooltip': "Imprint a single copy of a stamp on a surface",
		  'double_click': 'ShowMeshImprintToolOptions'},
	'11': {'code': 'SetMeshWaxTool',
		  'icon': 'Wax.png',
		  'tooltip': "Build up a surface",
		  'double_click': 'ShowMeshWaxToolOptions'},
	'12': {'code': 'SetMeshScrapeTool',
		  'icon': 'Scrape.png',
		  'tooltip': "Minimize or remove raised areas on a surface",
		  'double_click': 'ShowMeshScrapeToolOptions'},
	'13': {'code': 'SetMeshFillTool',
		  'icon': 'Fill.png',
		  'tooltip': "Fill in the valleys on a surface",
		  'double_click': 'ShowMeshFillToolOptions'},
	'14': {'code': 'SetMeshKnifeTool',
		  'icon': 'Knife.png',
		  'tooltip': "Cut fine strokes into a surface",
		  'double_click': 'ShowMeshKnifeToolOptions'},
	'15': {'code': 'SetMeshSmearTool',
		  'icon': 'Smear.png',
		  'tooltip': "Pull a surface in the direction of the stroke",
		  'double_click': 'ShowMeshSmearToolOptions'},
	'16': {'code': 'SetMeshBulgeTool',
		  'icon': 'Bulge.png',
		  'tooltip': "Inflate an area on a surface",
		  'double_click': 'ShowMeshBulgeToolOptions'},
	'17': {'code': 'SetMeshAmplifyTool',
		  'icon': 'Amplify.png',
		  'tooltip': "Accentuate surface detail",
		  'double_click': 'ShowMeshAmplifyToolOptions'},
	'18': {'code': 'SetMeshFreezeTool',
		  'icon': 'Freeze.png',
		  'tooltip': "Paint areas of a surface to prevent further modification",
		  'double_click': 'ShowMeshFreezeToolOptions'},
	'19': {'code': 'ConvertToFrozen',
		  'icon': 'freezeSelected.png',
		  'tooltip': "Convert To Frozen",
		  'double_click': 'None'},
	'20': {'code': 'OpenVisorForMeshes',
		  'icon': 'contentBrowserGeneric.png',
		  'tooltip': "Open Content Browser for Sculpting Base Meshes",
		  'double_click': 'None'},
	'21': {'code': 'ShapeEditor',
		  'icon': 'blendShapeEditor.png',
		  'tooltip': "Shape Editor: ",
		  'double_click': 'CreateBlendShapeOptions'},
	'22': {'code': 'PoseEditor',
		  'icon': 'poseEditor.png',
		  'tooltip': "Pose Editor: Create, edit and manage pose space deformations",
		  'double_click': 'None'},
	'23': {'code': 'SetMeshSmoothTargetTool',
		  'icon': 'SmoothTarget.png',
		  'tooltip': "Smooth Target Tool: Even out surface detail only for the current blend shape target in Edit mode",
		  'double_click': 'ShowMeshSmoothTargetToolOptions'},
	'24': {'code': 'SetMeshCloneTargetTool',
		  'icon': 'CloneTarget.png',
		  'tooltip': "Clone Target Tool: Copy edits from a blend shape target source to the current target in Edit mode",
		  'double_click': 'ShowMeshCloneTargetToolOptions'},
	'25': {'code': 'SetMeshMaskTool',
		  'icon': 'Mask.png',
		  'tooltip': "Mask Target Tool: Paint areas on a mesh to hide edits for the current blend shape target in Edit mode",
		  'double_click': 'ShowMeshMaskToolOptions'},
	'26': {'code': 'SetMeshEraseTool',
		  'icon': 'Erase.png',
		  'tooltip': "Erase Target Tool: Remove edits for the current blend shape target in Edit mode",
		  'double_click': 'ShowMeshEraseToolOptions'}
	}

separators_before = ['SetMeshSmoothTargetTool','ShapeEditor','ConvertToFrozen','ArtPaintSkinWeightsTool','ParentConstraint','SetKey']

# -------------------------------------------------------------------


class MutantUI(QtMutantWindow.Qt_Mutant):

	def __init__(self):
		super(MutantUI, self).__init__()

		self.setWindowTitle(Title)

		self.designer_loader_child(path=Folder + '/UI/{}/'.format(FOLDER_NAME), ui_file=UI_File)
		self.set_title(Title)

		self.create_layout()
		self.create_connections()

	# -------------------------------------------------------------------

	def create_layout(self):
		"""

		Returns:

		"""


	def create_connections(self):
		"""

		Returns:

		"""

		#self.ui.button.clicked.connect(self.create_block)

	# -------------------------------------------------------------------

	# CLOSE EVENTS _________________________________
	def closeEvent(self, event):
		''


# -------------------------------------------------------------------

if __name__ == "__main__":

	try:
		cMutantUI.close()  # pylint: disable=E0601
		cMutantUI.deleteLater()
	except:
		pass
	cMutantUI = MutantUI()
	cMutantUI.show()

# -------------------------------------------------------------------

'''
#Notes






'''