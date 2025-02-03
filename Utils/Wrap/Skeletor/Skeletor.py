from __future__ import absolute_import, division
from builtins import round
"""
#Title: Skeletor.py
#Author: Noah Schnapp
#LinkedIn: https://www.linkedin.com/in/wnschnapp/
#Youtube: http://www.youtube.com/WilliamNoahSchnapp

import Mutant_Tools

from Mutant_Tools.Utils.Wrap.Skeletor import Skeletor
import imp
imp.reload(Skeletor)
Skeletor.openUI()

"""

####################
####################
#...Import Commands
####################
####################

import maya.cmds as cmds
import maya.mel as mel
import math, os, json
from pathlib import Path
from collections import OrderedDict

PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-3]
FOLDER=''
for f in PATH_PARTS:
	FOLDER = os.path.join(FOLDER, f)

####################
####################

#...SCRIPT EDITOR USE
dirpath = os.path.join(FOLDER, 'Utils','Wrap','Skeletor')

# dirpath = r'F:\schnapp_projects_ARCHIVE\_myProjects\sandbox\automaticallyPlaceJointsTutorial\02-files'
# import sys, imp 
# sys.path.insert(0, dirpath) 
# import automaticJointPlacement_complete 
# imp.reload(automaticJointPlacement_complete)
# automaticJointPlacement_complete.run_dev()

####################
####################

# def run_dev():
# 	#...args
# 	mode = 'body'
# 	#...name file
# 	filepath = '%s/00_example_%s.mb'%(dirpath, mode)
# 	#...open scene
# 	#cmds.file(filepath, o=True, f=True)
# 	#...setLayout
# 	#mel.eval('setNamedPanelLayout "layout_user";')
# 	#...rename scene for testing
# 	cmds.file(rename='untitled')
# 	#...openUI
# 	openUI(dirpath)
#
# 	#...dev code
# 	cSkeletor = Skeletor()
# 	# cSkeletor.sample_one(sample_Array=cmds.ls(sl=1,fl=True)[:-1], node=cmds.ls(sl=1)[-1], auto=False)
# 	cSkeletor.dirpath = dirpath
# 	# cSkeletor.mirror_records()
# 	# cSkeletor.select_nodeSamples()
# 	# cSkeletor.select_nodesInAutoMode()
#
# 	# cSkeletor.update_positionRecords()
# 	# cSkeletor.record_one()
# 	# cSkeletor.record_all()
#
# 	# cSkeletor.reconform_all()
#
#
# 	# cSkeletor.sample_all('base_body', cmds.ls(sl=True))
# 	# print cSkeletor.data
#
#
# 	return True

#Fix for python 3
xrange=range


def dev_rotatePlanar(array = ["L_Shoulder_Guide", "L_Elbow_Guide", "L_Wrist_Guide"]):
	#...example rotate_planar
	rotate_planar(array)

	return True

def openUI(dirpath=dirpath):
	cSkeletorUI = SkeletorUI()
	cSkeletorUI.create_mainWindow(dirpath)
	return True

class SkeletorUI(object):

	def __init__(self):

		#...classes
		self.cSkeletor = Skeletor()

		#...vars
		self.windowName = 'SkeletorUI'
		self.windowWidth = 300
		self.textFieldWidth = 300
		self.buttonWidth = 300
		self.buttonHeight = 25
		pass

	def create_mainWindow(self, dirpath=None):

		#...set dirpath
		if dirpath == None:
			dirpath = self.cSkeletor.dirpath
		else:
			self.cSkeletor.dirpath = dirpath

		# Make a new window
		if (cmds.window(self.windowName, exists=True)):
			cmds.deleteUI(self.windowName)
			
		#...title
		self.window = cmds.window(self.windowName, title=self.windowName, sizeable = True, resizeToFitChildren = True)
		self.columnLayout__ui = cmds.columnLayout(adjustableColumn=True,width=self.windowWidth)
		cmds.text('Directory')

		#...dirpath
		self.columnLayout__ioA = cmds.rowColumnLayout('columnLayout__ioA', parent = self.columnLayout__ui, numberOfColumns=2, width = self.windowWidth)
		self.textField__dirpath = cmds.textField('textField__dirpath', text=dirpath, editable=0, width = 270, parent = self.columnLayout__ioA) 
		cmds.button(label='Set', width = 30,  height = self.buttonHeight, command = self.btnCmd_setDirpath, parent = self.columnLayout__ioA)
		cmds.text('-'*50)
		cmds.setParent('..')

		#...buttons
		self.columnLayout__ioBBB = cmds.rowColumnLayout('columnLayout__ioBBB', parent = self.columnLayout__ui, numberOfColumns=1, width = self.windowWidth)
		cmds.button(label='Record All', width = self.buttonWidth,  height = self.buttonHeight, command =  self.btnCmd_recordAll, parent = self.columnLayout__ioBBB)
		cmds.text(' '*50)
		cmds.button(label='Record One', width = self.buttonWidth,  height = self.buttonHeight, command = self.btnCmd_recordOne, parent = self.columnLayout__ioBBB)
		cmds.text('-'*50)
		cmds.button(label='Select Node Samples', width = self.buttonWidth,  height = self.buttonHeight, command = self.btnCmd_selectNodeSamples, parent = self.columnLayout__ioBBB)
		cmds.button(label='Select Nodes in Auto Mode', width = self.buttonWidth,  height = self.buttonHeight, command = self.btnCmd_selectNodesInAutoMode, parent = self.columnLayout__ioBBB)
		cmds.text(' '*50)
		cmds.button(label='Mirror Records', width = self.buttonWidth,  height = self.buttonHeight, command = self.btnCmd_mirrorRecords, parent = self.columnLayout__ioBBB)
		cmds.button(label='Update Position Records', width = self.buttonWidth,  height = self.buttonHeight, command = self.btnCmd_updatePositionRecords, parent = self.columnLayout__ioBBB)
		cmds.text('-'*50)
		cmds.button(label='Reconform Nodes To Selected Mesh', width = self.buttonWidth,  height = self.buttonHeight, command = self.btnCmd_reconformNodesToSelectedMesh, parent = self.columnLayout__ioBBB)
		cmds.setParent('..')

		cmds.showWindow(self.window)

		return True

	#...UI
	def btnCmd_setDirpath(self, *args, **kwargs):
		#...get dirpath
		self.cSkeletor.dirpath = cmds.fileDialog2(caption='Select Data Directory', 
										dialogStyle=2, 
										fileMode=3, 
										startingDirectory=cmds.workspace(q=True, rootDirectory=True), 
										fileFilter='*.%s'%self.cSkeletor.filenameExtension, 
										okCaption = "Select")[0]

		#...update textfield
		cmds.textField(self.textField__dirpath, e=True, text=self.cSkeletor.dirpath)

		return True

	def btnCmd_recordAll(self, *args, **kwargs):
		#...parse_selection
		node_Array, mesh, sample_Array = self.cSkeletor.parse_selection()
		#...update vars
		self.cSkeletor.filepath = '%s/%s.%s'%(self.cSkeletor.dirpath, mesh, self.cSkeletor.filenameExtension)
		#...if confirm
		if os.path.exists(self.cSkeletor.filepath):
			result = cmds.confirmDialog(
					title='Skeletor Data Exists!',
					message='Overwrite existing Data for: "%s"?'%mesh,
					button=['Overwrite', 'Cancel'],
					defaultButton='Cancel',
					cancelButton='Cancel',
					dismissString='Cancel')
			#...Overwrite
			if result == 'Cancel':
				return False
		#...record_all
		self.cSkeletor.record_all()

		return True

	def btnCmd_recordOne(self, *args, **kwargs):
		#...record_one
		self.cSkeletor.record_one()
		return True

	def btnCmd_mirrorRecords(self, *args, **kwargs):
		#...mirror_records
		self.cSkeletor.mirror_records()
		return True

	def btnCmd_updatePositionRecords(self, *args, **kwargs):
		#...update_positionRecords
		self.cSkeletor.update_positionRecords()
		return True

	def btnCmd_selectNodeSamples(self, *args, **kwargs):
		#...select_nodeSamples
		self.cSkeletor.select_nodeSamples()
		return True

	def btnCmd_selectNodesInAutoMode(self, *args, **kwargs):
		#...select autoNodes
		self.cSkeletor.select_nodesInAutoMode()
		return True

	def btnCmd_reconformNodesToSelectedMesh(self, *args, **kwargs):
		#...reconform_all
		self.cSkeletor.reconform_all()
		return True

class Skeletor(object):

	def __init__(self):

		self.dirpath = os.path.join(FOLDER, 'Utils','Wrap','Skeletor')
		self.mesh = None
		self.data = {}
		self.sampleCount = 120
		self.filenameExtension = 'skeletor'
		self.vtxPosition_Array = []

		pass

	#...record
	def record_all(self, sel_Array=None):
		#...parse_selection
		node_Array, mesh, sample_Array = self.parse_selection(sel_Array)
		if mesh == None:
			print('ERROR: Select a mesh and node_Array to record Auto Node Samples!')
			return False
		#...load_data
		self.load_data(mesh, self.dirpath)
		#...analyze mesh
		self.sample_all(mesh, node_Array)
		#...save_data
		self.save_data(mesh, self.dirpath)
		#...debug
		print('SUCCESS: Recorded nodes on mesh: "%s"'%mesh)
		for n in node_Array:
			print(n)
		return True

	def record_one(self, sel_Array=None):
		#...parse_selection
		node_Array, mesh, sample_Array = self.parse_selection(sel_Array)
		if sample_Array == []:
			print('ERROR: Select a mesh and sample_Array to record Node Samples!')
			return False
		#...load_data
		self.load_data(mesh, self.dirpath)
		#...analyze mesh
		self.sample_one(sample_Array, node_Array[0])
		#...save_data
		self.save_data(mesh, self.dirpath)
		#...debug
		print('SUCCESS: Recorded nodes on mesh: "%s"'%mesh)
		print(node_Array[0])
		return True

	def mirror_records(self, sel_Array=None):
		#...parse_selection
		node_Array, mesh, sample_Array = self.parse_selection(sel_Array)
		#...debug
		if mesh == None:
			print('ERROR: Select a mesh to Mirror Records!')
			return False
		#...load_data
		self.load_data(mesh, self.dirpath)
		#...mirror_all
		keys=[]
		mirror_keys=[]
		for i in self.data:
			mirror_keys.append(i)
		self.mirror_all(mesh, mirror_keys)
		#...save_data
		self.save_data(mesh, self.dirpath)
		#...debug
		print('SUCCESS: Recorded all Mirror samples on mesh: "%s"'%mesh)
		for node in self.data.keys():
			print(node)
		return True

	def update_positionRecords(self, sel_Array=None):
		#...parse_selection
		node_Array, mesh, sample_Array = self.parse_selection(sel_Array)
		#...debug
		if mesh == None:
			print('ERROR: Select a mesh to Update Node Records!')
			return False
		#...load_data
		self.load_data(mesh, self.dirpath)
		#...updateRecords
		for node in self.data.keys():
			self.sample_one(sample_Array=None, node=node, auto=None)
		#...save_data
		self.save_data(mesh, self.dirpath)
		#...debug
		print('SUCCESS: Updated all Node Position Vectors on mesh: "%s"'%mesh)
		for node in self.data.keys():
			print(node)
		return True

	def select_nodeSamples(self, sel_Array=None):
		#...parse_selection
		node_Array, mesh, sample_Array = self.parse_selection(sel_Array)
		#...debug
		if mesh == None or len(node_Array) != 1:
			print('ERROR: Select both a Mesh and Node to show Node Samples!')
			return False
		node = node_Array[0]
		#...load_data
		self.load_data(mesh, self.dirpath)
		#...select sample
		vertID_Array = []
		if node in self.data.keys():
			vertID_Array.extend(self.data[node][0])
		#...construct meshVtx_Array
		meshVtx_Array = ['%s.vtx[%s]'%(mesh, v) for v in vertID_Array]
		#...select components
		cmds.select(meshVtx_Array, r=True)
		return True
	
	def select_nodesInAutoMode(self, sel_Array=None):
		#...parse_selection
		node_Array, mesh, sample_Array = self.parse_selection(sel_Array)
		#...debug
		if mesh == None:
			print('ERROR: Select a mesh to list autoNodes for!')
			return False
		#...load_data
		self.load_data(mesh, self.dirpath)
		#...select auto_Array
		auto_Array = []
		print('---')
		for node in self.data.keys():
			if cmds.objExists(node):
				if self.data[node][3] == True:
					auto_Array.append(node)
		#...select
		cmds.select(auto_Array, r=True)
		return True
	
	def reconform_all(self, sel_Array=None, use_self_path=False):
		#...parse_selection
		if sel_Array == None:
			sel_Array = cmds.ls(sl=1)
		#...debug
		if len(sel_Array) != 2:
			print('ERROR: Select a Source and Destination mesh to reconform nodes too!')
			return False
		#...filepath exists?
		if use_self_path:
			filepath = '%s/%s.%s'%(self.dirpath, sel_Array[0], self.filenameExtension)
		else:
			filepath = '%s/%s.%s'%(dirpath, sel_Array[0], self.filenameExtension)

		if not os.path.exists(filepath):
			print('ERROR: Cannot find Skeletor Data file for "%s" at path: %s'%(sel_Array[0], filepath))
			return False
		#...load_data
		self.load_data(sel_Array[0], self.dirpath)
		#...place_all
		self.place_all(sel_Array[1])
		#...debug
		print('SUCCESS: Reconform nodes to mesh: "%s"'%sel_Array[1])
		for node in self.data.keys():
			print(node)
		return True

	#...analyze
	def get_vtxPositions(self, mesh):
		posFlatten_Array = [round(x, 6) for x in cmds.xform('%s.vtx[*]'%mesh, q=True, ws=True, t=True)]
		self.vtxPosition_Array = list(zip(posFlatten_Array[0::3], posFlatten_Array[1::3], posFlatten_Array[2::3]))
		return self.vtxPosition_Array
	
	def get_sampleArray(self, mesh, node, sampleCount = 30):
		#...need to reanalyze mesh?
		if self.mesh != mesh:
			self.vtxPosition_Array = self.get_vtxPositions(mesh)
		if self.vtxPosition_Array == []:
			self.vtxPosition_Array = self.get_vtxPositions(mesh)

		#...get node position
		xform_node = cmds.xform(node, q=True, t=True,ws=True)
		#...get distance
		distance_Array = [[distance(xform_vtx, xform_node), i] for i, xform_vtx in enumerate(self.vtxPosition_Array)]
		#...sort array
		distance_Array.sort()
		#...construct meshVtx_Array
		meshVtx_Array = ['%s.vtx[%s]'%(mesh, d[1]) for d in distance_Array[:sampleCount]]

		return meshVtx_Array

	def parse_selection(self, sel_Array=None):

		node_Array = []
		mesh = None
		sample_Array = []
		#...get sel_Array
		if sel_Array == None:
			sel_Array = cmds.ls(sl=1)
		if sel_Array == []:
			print("ERROR: Can't parse Selection! Nothing Selected!")
			return node_Array, mesh, sample_Array
		#...get sample_Array from selection
		sample_Array = cmds.ls([v for v in sel_Array if '.vtx[' in v], flatten=True)
		#...get node/mesh from sel_Array
		node_Array = []
		mesh = None
		for s in sel_Array:
			if '.vtx[' in s:
				mesh = s.split('.vtx')[0]
			else:
				#...determine mesh from nodes
				if cmds.objectType(s) == 'joint':
					node_Array.append(s)
				else:
					mesh = s

		return node_Array, mesh, sample_Array
	
	#...sample mesh and node relationship
	def sample_all(self, mesh, node_Array):
		#...add node position entries
		[self.sample_one(self.get_sampleArray(mesh, node, sampleCount=self.sampleCount), node, auto=True) for node in node_Array]
		return True

	def sample_one(self, sample_Array=None, node=None, auto=False):
		#...use existing sample_Array?
		if sample_Array == None:
			sample_Array = ['%s.vtx[%s]'%(self.mesh, d) for d in self.data[node][0]]
		#...check for node
		if node == None:
			return False
		#...use existing auto setting?
		if auto == None:
			auto = self.data[node][3]
		#...get position of centroid of sel_Array
		pos_centroid = get_centroid(sample_Array)
		#...get position of node
		pos_node = cmds.xform(node, q=1,t=1,ws=1)
		#...get vector of centroid to node
		vector = get_vector(pos_centroid, pos_node)
		#...convert sample_Array to number_Array only 
		vertID_Array = [int((i.split('.vtx[')[1].split(']')[0])) for i in cmds.ls(sample_Array, fl=True)]
		#...get scaleFactor
		scaleFactor = get_scaleFactor(sample_Array)
		#...store in data ram
		self.data[node] = [vertID_Array, vector, scaleFactor, auto]
		return True

	def mirror_all(self, mesh, node_Array):
		#...mirror list
		for node in node_Array:
			if not node.startswith('r_'):
				print(node)
				self.mirror_one(mesh, node)

		return True
	
	def mirror_one(self, mesh, node):
		if not cmds.objExists(node):
			return False
		#...get data info
		[vtxID_Array, vector, scaleFactorOld, auto] = self.data[node]
		#...create sample_Array
		sample_Array = ['%s.vtx[%s]'%(mesh, v) for v in vtxID_Array]
		#...mirror
		mirror_ArrayTemp = get_mirrorVerts(sample_Array)
		#...remove l side if l in nodeMirror:
		mirror_Array = []
		if node.startswith('l_'):
			for m in mirror_ArrayTemp:
				if m not in sample_Array:
					mirror_Array.append(m)
		else:
			mirror_Array = mirror_ArrayTemp[::]
		#...get mirror node, l => r, m => m
		nodeMirror = node.replace('l_','r_')
		#...sample one
		self.sample_one(mirror_Array, nodeMirror, auto=auto)
		return True

	#...reconform nodes to new mesh
	def place_all(self, mesh, node_Array = None):
		#...node_Array == None, reconform nodes in self.data
		if node_Array == None:
			node_Array = [n for n in self.data.keys() if cmds.objExists(n)]
		#...store parent_Array
		hierarchy_Array = unparent_hierarchy(node_Array)
		for node in node_Array:
			if cmds.objExists(node):
				self.place_one(mesh, node)
		#...reparent hiearchy
		parent_hierarchy(hierarchy_Array)
		return True

	def place_one(self, mesh, node):
		#...get data info
		[vtxID_Array, vector, scaleFactorOld, auto] = self.data[node]
		#...create sample_Array
		sample_Array = ['%s.vtx[%s]'%(mesh, v) for v in vtxID_Array]
		#...get position of centroid of sel_Array
		pos_centroid = get_centroid(sample_Array)
		#...get new scaleFactor
		scaleFactorNew = get_scaleFactor(sample_Array)
		#...get new position from centroid + vector
		scaleFactorNew = get_scaleFactor(sample_Array)
		scaleFactorMult = [0,0,0]
		if scaleFactorOld[0] == 0:
			scaleFactorMult[0] = 0
		else:
			scaleFactorMult[0] = scaleFactorNew[0]/scaleFactorOld[0]
		if scaleFactorOld[1] == 0:
			scaleFactorMult[1] = 0
		else:
			scaleFactorMult[1] = scaleFactorNew[1]/scaleFactorOld[1]
		if scaleFactorOld[2] == 0:
			scaleFactorMult[2] = 0
		else:
			scaleFactorMult[2] = scaleFactorNew[2]/scaleFactorOld[2]
		#...get new position from centroid + vector
		pos_nodeNew = [0,0,0]
		pos_nodeNew[0] = pos_centroid[0] + (vector[0] * scaleFactorMult[0])
		pos_nodeNew[1] = pos_centroid[1] + (vector[1] * scaleFactorMult[1])
		pos_nodeNew[2] = pos_centroid[2] + (vector[2] * scaleFactorMult[2])
		#...move node to reconform position
		cmds.select(cl=1)
		cmds.xform(node, t=pos_nodeNew, ws=1)
		return True

	#...save/load
	def save_data(self, mesh, dirpath=None):
		#...get dirpath
		if dirpath == None:
			dirpath = self.dirpath
		#...get filepath
		self.filepath = '%s/%s.%s'%(dirpath, mesh, self.filenameExtension)
		#...save data
		fh = open(self.filepath, 'w')
		json.dump(self.data, fh, ensure_ascii=False, indent=4)
		fh.close()
		#...debug
		print('SUCCESS: Saved Skeletor Data to: "%s"'%self.filepath)
		print('')
		return True

	def load_data(self, mesh, dirpath=None):
		#...define mesh
		self.mesh = mesh
		#...get dirpath
		if dirpath == None:
			dirpath = self.dirpath
		#...get filepath
		self.filepath = '%s/%s.%s'%(dirpath, self.mesh, self.filenameExtension)
		#...file exist?
		if not os.path.exists(self.filepath):
			print('ERROR: Skeletor Data Not Found! "%s"'%self.filepath)
			return False
		#...load data
		fh = open(self.filepath, 'r')
		self.data = json.load(fh)
		fh.close()
		#...debug
		print('SUCCESS: Loaded Skeletor Data from: "%s"'%self.filepath)
		print('')
		return self.data

#####################################################################
#####################################################################

#############################################
#...other funcs
#############################################
def unparent_hierarchy(node_Array):
	hierarchy_Array = []
	#...get child/parent
	for n in node_Array:
		if cmds.objExists(n):
			hierarchy_Array.append([n, cmds.listRelatives(n, p=True)])
			if cmds.listRelatives(n, parent=True) != None:
				cmds.parent(n, w=True)
	return hierarchy_Array

def parent_hierarchy(hierarchy_Array):
	#...parent
	for node, parent in hierarchy_Array:
		if parent == None:
			if cmds.listRelatives(node, parent=True) != None:
				cmds.parent(node, w=True)
		else:
			cmds.parent(node, parent)

	return True

def get_mirrorVerts(meshVtx_Array=None, select=False):
	#...get sel_Array
	if meshVtx_Array == None:
		meshVtx_Array = cmds.ls(sl=1)
	#...turn on sym sel
	mel.eval('reflectionSetMode objectx;')
	main_Array = cmds.ls(meshVtx_Array, flatten=True)
	cmds.select(main_Array, r=True, sym=True)
	#...get mirror
	mirror_Array = []
	for v in cmds.ls(sl=True, flatten=True):
		mirror_Array.append(v)
	#...remove duplicates
	mirror_Array = list(set(mirror_Array))
	#...turn off sym sel
	mel.eval('reflectionSetMode none;')
	#...clear selection
	cmds.select(cl=True)
	#...select mirror_Array
	if select == True:
		cmds.select(mirror_Array, r=True)
	return mirror_Array

#############################################
#...math funcs
#############################################
def get_scaleFactor(node_Array):
	bb = cmds.exactWorldBoundingBox(node_Array, ignoreInvisible=True)
	scaleFactor = [0,0,0]
	scaleFactor[0] = abs(bb[3]-bb[0])
	scaleFactor[1] = abs(bb[4]-bb[1])
	scaleFactor[2] = abs(bb[5]-bb[2])


	return scaleFactor

def get_vector(pt0 = None, pt1 = None):
	dx = pt1[0] - pt0[0]
	dy = pt1[1] - pt0[1]
	dz = pt1[2] - pt0[2]
	return [dx, dy, dz]

def get_centroid(node_Array):
	#...get centroid of nodes
	posX = 0
	posY = 0
	posZ = 0
	for node in node_Array:
		position = cmds.xform(node, query = True, translation = True, worldSpace = True)
		posX = posX + position[0]
		posY = posY + position[1]
		posZ = posZ + position[2]
	nodeCount = len(node_Array)
	centroid = [posX/nodeCount, posY/nodeCount, posZ/nodeCount]
	return centroid

def distance(pt0 = None, pt1 = None):
	dx = pt1[0] - pt0[0]
	dy = pt1[1] - pt0[1]
	dz = pt1[2] - pt0[2]
	distance = float(math.sqrt(dx*dx + dy*dy + dz*dz))
	return distance

def crossProduct(a, b):
	cp = [a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0]]
	return cp

def normalize_Array(val_Array):
	total = 0
	for i in xrange (0, len(val_Array)):
		val = val_Array[i]*val_Array[i]
		total = total + val
	divideVal = math.sqrt(total)
	for i in xrange (0, len(val_Array)):
		val_Array[i] /= divideVal
	return val_Array

def create_matrix(vectAx = None, vectAy = None, vectAz = None, shear_Array = None, position = None):

	if vectAx == None:
		vectAx = [1,0,0]
	if vectAy == None:
		vectAy = [0,1,0]
	if vectAz == None:
		vectAz = [0,0,1]
	if shear_Array == None:
		shear_Array = [0,0,0,1]
	if position == None:
		position = [0,0,0]

	matrix = []
	matrix.append(vectAx[0])
	matrix.append(vectAx[1])
	matrix.append(vectAx[2])
	matrix.append(float(shear_Array[0]))
	matrix.append(vectAy[0])
	matrix.append(vectAy[1])
	matrix.append(vectAy[2])
	matrix.append(float(shear_Array[1]))
	matrix.append(vectAz[0])
	matrix.append(vectAz[1])
	matrix.append(vectAz[2])
	matrix.append(float(shear_Array[2]))
	matrix.append(position[0])
	matrix.append(position[1])
	matrix.append(position[2])
	matrix.append(float(shear_Array[3]))

	return matrix

def rotate_planar(node_Array = None, freeze_translate=False, freeze_rotate=False, freeze_scale=False):
	#...Get Args from Selection
	if node_Array == None:
		node_Array = cmds.ls(sl=True)
	#...store parent_Array
	hierarchy_Array = unparent_hierarchy(node_Array)
	#...get positions
	nodeA = node_Array[0]
	nodeB = node_Array[1]
	nodeC = node_Array[2]
	vectA_pos = cmds.xform(nodeA, scalePivot = True, query = True, worldSpace = True)
	vectB_pos = cmds.xform(nodeB, scalePivot = True, query = True, worldSpace = True)
	vectC_pos = cmds.xform(nodeC, scalePivot = True, query = True, worldSpace = True)
	#...get vectors and matricies
	vectAx = get_vector(vectA_pos, vectB_pos)
	vectBx = get_vector(vectB_pos, vectC_pos)

	vectAy = crossProduct(vectAx,vectBx)
	vectAz = crossProduct(vectAy,vectAx)

	vectBy = crossProduct(vectAx,vectBx)
	vectBz = crossProduct(vectBy,vectBx)

	vectAx = normalize_Array(vectAx)
	vectAy = normalize_Array(vectAy)
	vectAz = normalize_Array(vectAz)

	nodeA_matrix = create_matrix(vectAx = vectAx, vectAy = vectAy, vectAz = vectAz, position = vectA_pos)
	nodeB_matrix = create_matrix(vectAx = vectBx, vectAy = vectBy, vectAz = vectBz, position = vectB_pos)

	#...orient nodes
	cmds.xform(nodeA, m = nodeA_matrix, worldSpace = True)
	cmds.xform(nodeB, m = nodeB_matrix, worldSpace = True)

	cmds.makeIdentity(nodeA, t=freeze_translate,r=freeze_rotate,s=freeze_scale,apply=True,n=0)
	cmds.makeIdentity(nodeB, t=freeze_translate,r=freeze_rotate,s=freeze_scale,apply=True,n=0)

	#...reparent hiearchy
	parent_hierarchy(hierarchy_Array)
	return True

