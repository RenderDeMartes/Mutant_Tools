'''
version: 1.0.0
date: 21/04/2020

#----------------
content: 

fk_chain(size = 1, color = 'lightBlue', curve_type = 'circleX') #works on selection only
pole_vector(bone_one = '', bone_two = '', bone_three = '') create locator in the correct pv pos
ik_chain(start = '', end = '', size = 1, color = 'lightBlue', curve_type = 'cube', pv = True)
joints_middle(start = '', end = '', axis = 'X', amount = 4)
twist(start = '', end = '', axis = 'X', amount = 4, mode = 'down'

NEEDS A UPDATE :)

#----------------
how to: 
	
import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import kinematics
imp.reload(Mutant_Tools.Utils.Rigging.kinematics)

kin = kinematics.Kinematics_class()
kin.FUNC_NAME(argument = '')

#----------------
dependencies:   
	
math
json
pymel
maya mel
maya.cmds
OpenMaya

tools.Tools_Class

#----------------
licence: https://www.eulatemplate.com/live.php?token=FGISW7ApRfgywum6murbBmLcusKONzkv
author:  Esteban Rodriguez <info@mutanttools.com>

'''
import math

import maya.mel as mel
from maya import cmds
#import pymel.core as pm
from maya import OpenMaya

import os
import imp
import json
from pathlib import Path

try: 
	import tools
	imp.reload(tools)

except:
	import Mutant_Tools
	import Mutant_Tools.Utils.Rigging
	from Mutant_Tools.Utils.Rigging import tools
	imp.reload(Mutant_Tools.Utils.Rigging.tools)

#----------------------------------------------------------------------------------------------------------------

#Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-2]
FOLDER=''
for f in PATH_PARTS:
	FOLDER = os.path.join(FOLDER, f)

JSON_FILE = os.path.join(FOLDER, 'config', 'name_conventions.json')
with open(JSON_FILE) as json_file:
	nc = json.load(json_file)
#setup File
SETUP_FILE = os.path.join(FOLDER, 'config', 'rig_setup.json')
with open(SETUP_FILE) as setup_file:
	setup = json.load(setup_file)

#----------------------------------------------------------------------------------------------------------------
#create base class for selection objects

class Kinematics_class(tools.Tools_class):
	
	def fk_chain(self, input = '', size = 1, color = setup['main_color'], curve_type = setup['fk_ctrl'], scale = True, twist_axis = setup['twist_axis']) :
		"""	Create a FK Chain with selected joints, settings can be change in the setup json file

		Args:
			input: if not specify it will use selection else specify string (Recommended using select and not the input names)
			size: int ctrl size
			color: string color of controlls
			curve_type: string curve tye based on config curves
			scale: bool add scale constraint
			twist_axis: aim axis of the joints for creating as bounding cubes

		Returns: list fk_controllers

		"""


		#Check input
		if input != '':
			self.input = [input]
			
		else:   
			self.input = input  
		
		self.check_input('fk_chain')    

		fk_controllers = []

		for bone in cmds.ls(sl =True) :
			
			#Create controller and groups to zero it
			#fk_controller = cmds.circle( n = '{}{}'.format(bone,nc['ctrl']) , nr = (1,0,0), r = size)[0]
			if curve_type == 'bounding_cube':
				fk_controller = self.bounding_cube(input = bone, size = size, name =  '{}{}'.format(bone,nc['ctrl']), axis = twist_axis)
			else:
				fk_controller = self.curve(type = curve_type, custom_name = True, name = '{}{}'.format(bone,nc['ctrl']), size = size)

			if nc['joint'] in str(fk_controller):
				fk_controller = cmds.rename(fk_controller, fk_controller.replace(nc['joint'],''))


			cmds.delete(cmds.parentConstraint(bone, fk_controller)) #put the controller in position

			#create Root Grp
			fk_auto_grp = self.root_grp(replace_nc = False)

			#add connections
			cmds.parentConstraint(fk_controller,bone) #parent Ctrl to Bone
			if scale == True:
				cmds.scaleConstraint(fk_controller,bone) #parent Ctrl to Bone

			#Organize a bit
			self.assign_color(fk_controller, color)
			self.hide_attr(fk_controller, s = 1 - scale, v = True)

			#try to parent it to create chain 
			if len(fk_controllers) > 0:cmds.parent(fk_auto_grp[0], fk_controllers[-1])
			else:pass 

			#Create Controller List
			fk_controllers.append(fk_controller)
		

		return fk_controllers

	#----------------------------------------------------------------------------------------------------------------

	def pole_vector_placement(self, bone_one = '', bone_two = '', bone_three = '',back_distance = 1):
		"""Get the perfect Polevector position

		Args:
			bone_one: string first joint in chain
			bone_two: string second joint in chain
			bone_three: string third joint in chain
			back_distance: distance to move it backwards so its better for animators

		Returns: string of temp locator

		"""


		#Thanks to >>> https://vimeo.com/66015036
		if bone_one == '':
				sel = cmds.ls(sl = 1)
				bone_one = sel[0]
				bone_two = sel[1]
				bone_three = sel[2]
		
		else:
			cmds.select(bone_one, bone_two, bone_three)
			sel = cmds.ls(sl = 1)

		start = cmds.xform(sel[0] ,q= 1 ,ws = 1,t =1 )
		mid = cmds.xform(sel[1] ,q= 1 ,ws = 1,t =1 )
		end = cmds.xform(sel[2] ,q= 1 ,ws = 1,t =1 )
		
		startV = OpenMaya.MVector(start[0] ,start[1],start[2])
		midV = OpenMaya.MVector(mid[0] ,mid[1],mid[2])
		endV = OpenMaya.MVector(end[0] ,end[1],end[2])
		
		startEnd = endV - startV
		startMid = midV - startV
		
		dotP = startMid * startEnd
		proj = float(dotP) / float(startEnd.length())
		startEndN = startEnd.normal()
		projV = startEndN * proj
		
		arrowV = startMid - projV
		arrowV*= 0.5
		finalV = arrowV + midV
		
		cross1 = startEnd ^ startMid
		cross1.normalize()
		
		cross2 = cross1 ^ arrowV
		cross2.normalize()
		arrowV.normalize()
		
		matrixV = [arrowV.x , arrowV.y , arrowV.z , 0 ,
		cross1.x ,cross1.y , cross1.z , 0 ,
		cross2.x , cross2.y , cross2.z , 0,
		0,0,0,1]
		
		matrixM = OpenMaya.MMatrix()
		
		OpenMaya.MScriptUtil.createMatrixFromList(matrixV , matrixM)
		
		matrixFn = OpenMaya.MTransformationMatrix(matrixM)
		
		rot = matrixFn.eulerRotation()
		
		loc = cmds.spaceLocator(n = '{}{}'.format(bone_two[0], nc['locator']))[0]
		cmds.xform(loc , ws =1 , t= (finalV.x , finalV.y ,finalV.z*back_distance))
		
		cmds.xform ( loc , ws = 1 , rotation = ((rot.x/math.pi*180.0),
		(rot.y/math.pi*180.0),
		(rot.z/math.pi*180.0)))
		
		return loc

	#----------------------------------------------------------------------------------------------------------------

	def streatchy_ik(self, ik = '', ik_ctrl= '', top_ctrl = '', pv_ctrl = '', attrs_location = '', name = '', axis = 'Y'):
		"""Generate all the nodes necessary to create a iK stretching system

		Args:
			ik:string name of the IK on the limb
			ik_ctrl: string name of the IK Ctrl
			top_ctrl: string name of the Top IK Ctrl
			pv_ctrl: string name of the PV Ctrl
			attrs_location: String where to put the attrs
			name: string name of the system
			axis: string name of the twist axis so it can get correct lengths

		Returns: ik_grp, normalize_loc, start_loc, end_loc, pv_loc, distance, top_distance, ik_distance

		"""


		if ik == '':
			ik = cmds.ls(sl=True)
		if name == '':
			name = ik
	
		#get components in the ik
		base_joint = cmds.listConnections (ik)
		effector = base_joint[1]
		end_joint = cmds.listConnections (effector)

		#joints in chain
		ik_joints = cmds.listRelatives (base_joint, ad = True, typ = 'joint')
		ik_joints.append (base_joint[0])  

		#find position of the base and end joints to create the distance tool
		first_pos = cmds.xform(ik_joints[0], q=True, t = True, ws=True)
		end_pos= cmds.xform(ik_joints[-1], q=True, t = True, ws=True) 
		pv_pos= cmds.xform(pv_ctrl, q=True, t = True, ws=True) 

		start_loc = cmds.spaceLocator(n = str(ik_joints[0]) + '_Stretchy' + nc['locator'])
		cmds.xform(start_loc, t = first_pos)
		cmds.setAttr(str(start_loc[0])+'.visibility', 0)
		end_loc = cmds.spaceLocator(n = str(ik_joints[-1])+ '_Stretchy'+ nc['locator'])
		cmds.xform(end_loc, t = end_pos)
		cmds.setAttr(str(end_loc[0])+'.visibility', 0)
		pv_loc = cmds.spaceLocator(n = str(ik_joints[1])+ '_Stretchy'+ nc['locator'])
		cmds.xform(pv_loc, t = pv_pos)
		cmds.setAttr(str(pv_loc[0])+'.visibility', 0)

		cmds.parentConstraint(top_ctrl, start_loc)
		cmds.parentConstraint(ik_ctrl, end_loc)
		cmds.parentConstraint(pv_ctrl, pv_loc)
				
		#distances nodes
		#main distance
		distance = cmds.distanceDimension(sp=first_pos, ep=end_pos)
		distance = cmds.rename(distance, ik_joints[-1] + '_' + ik_joints[0]+ nc['distance']+'_Shape')
		cmds.rename(cmds.listRelatives(distance, p =True), ik_joints[-1] + '_' + ik_joints[0]+ nc['distance'])
		cmds.setAttr('{}.visibility'.format(distance), 0)
		#top PV distance
		top_distance = cmds.distanceDimension(sp=first_pos, ep=pv_pos)
		top_distance = cmds.rename(top_distance, ik_joints[1] + '_' + ik_joints[0]+ nc['distance']+'_Shape')
		cmds.rename(cmds.listRelatives(top_distance, p =True), ik_joints[1] + '_' + ik_joints[0]+ nc['distance'])
		cmds.setAttr('{}.visibility'.format(top_distance), 0)		
		#IK PV distance
		ik_distance = cmds.distanceDimension(sp=end_pos, ep=pv_pos)
		ik_distance = cmds.rename(ik_distance, ik_joints[-1] + '_' + ik_joints[1]+ nc['distance']+'_Shape')
		cmds.rename(cmds.listRelatives(ik_distance, p =True), ik_joints[-1] + '_' + ik_joints[1]+ nc['distance'])	
		cmds.setAttr('{}.visibility'.format(ik_distance), 0)
				
		# stretchy math
		joints_for_distance = cmds.listRelatives (base_joint, ad = True, typ = 'joint')

		total_distance = 0
		
		for joint in joints_for_distance:
			current_distance = cmds.getAttr (joint + str ('.translate'+ axis))   
			total_distance = total_distance + current_distance  
		
		if total_distance < 0:
			total_distance = total_distance * -1  
			
		# New Attributes
		#Attr mult Stretchy
		print (attrs_location)

		for line in reversed(range(11)):
			try:
				self.line_attr(input = attrs_location, name = 'IK', lines = line)
				break
			except:pass
		
		stretch_Attr = self.new_attr(input= attrs_location, name = 'Stretch_On', min = 0 , max = 1, default = int(setup['stretch_default']))
		
		#IK Stretchy Nodes and Connections from RdM2 
		contidion_node = cmds.shadingNode('condition', asUtility=True, n= end_joint[0]+nc['condition'])
		cmds.setAttr(str(contidion_node)+".operation", 2)
		cmds.setAttr(str(contidion_node)+'.secondTerm', total_distance)

		#Connect To Distance
		md0 = self.connect_md_node(in_x1 = str(distance)+'.distance', in_x2 = total_distance, out_x = str(contidion_node)+'.colorIfTrueR', mode = 'divide', name = '')		
		
		#connect to joints
		md1 = self.connect_md_node(in_x1 = str(contidion_node)+'.outColorR', in_x2 = cmds.getAttr(str(ik_joints[1])+'.scale{}'.format(axis)), out_x = str(ik_joints[1])+'.scale{}'.format(axis), mode = 'mult', name = '{}_NewScale'.format(ik_joints[1]))
		md2 = self.connect_md_node(in_x1 = str(contidion_node)+'.outColorR', in_x2 = cmds.getAttr(str(ik_joints[2])+'.scale{}'.format(axis)), out_x = str(ik_joints[2])+'.scale{}'.format(axis), mode = 'mult', name = '{}_NewScale'.format(ik_joints[2]))
		
		md3 = self.connect_md_node(in_x1 = str(distance)+'.distance', in_x2 = stretch_Attr, out_x = str(contidion_node)+'.firstTerm', mode = 'mult', name = '{}_TotalDistance'.format(name))
		print (md0,md1,md2, md3)

		#normalize stretch
		normalize_loc = cmds.spaceLocator(n = name + '_NormalScale' + nc['locator'])[0]
		normal_md = self.connect_md_node( in_x1 = str(distance)+'.distance', in_x2 = str(normalize_loc) + '.scaleX', out_x = md0 + '.input1X', mode = 'divide', name = '{}_Normalize'.format(distance), force = True)
		#normalize pole vector lock
		cmds.connectAttr(str(normalize_loc) + '.scaleX', normal_md + '.input2Y')
		cmds.connectAttr(str(normalize_loc) + '.scaleX', normal_md + '.input2Z')

		cmds.connectAttr(normal_md + '.outputX', md3 + '.input1X', f=True)

		#manual change the sacles mult
		lower_attr = self.new_attr(input= attrs_location, name = 'Lower_Length', min = 0.25 , max = 2, default = 1)
		upper_attr = self.new_attr(input= attrs_location, name = 'Upper_Length', min = 0.25 , max = 2, default = 1)
		cmds.connectAttr(lower_attr, md2 + '.input2X', f=True)
		cmds.connectAttr(upper_attr, md1 + '.input2X', f=True)
		 		
		#elbow/knee lock #a bit hard coded bit it is what it is
		lock_attr = self.new_attr(input= attrs_location, name = 'Pole_Vector_Lock', min = 0 , max = 1, default = 0)

		upper_lock_blend = cmds.shadingNode('blendColors', asUtility=True, n = '{}_Lock{}'.format(ik_joints[1], nc['blend']))
		cmds.connectAttr(lock_attr, '{}.blender'.format(upper_lock_blend))
		cmds.connectAttr('{}.output.outputR'.format(upper_lock_blend), str(ik_joints[2])+'.scale{}'.format(axis), f=True)
		cmds.connectAttr('{}.outputX'.format(md1),'{}.color2.color2R'.format(upper_lock_blend), f=True)

		lower_lock_blend = cmds.shadingNode('blendColors', asUtility=True, n = '{}_Lock{}'.format(ik_joints[2], nc['blend']))
		cmds.connectAttr(lock_attr, '{}.blender'.format(lower_lock_blend))
		cmds.connectAttr('{}.output.outputR'.format(lower_lock_blend), str(ik_joints[1])+'.scale{}'.format(axis) , f=True)
		cmds.connectAttr('{}.outputX'.format(md2),'{}.color2.color2R'.format(lower_lock_blend), f=True)

		#connect lock pole vectors distance to normalize too
		cmds.connectAttr(str(top_distance)+'.distance', normal_md + '.input1Y')
		cmds.connectAttr(str(ik_distance)+'.distance', normal_md + '.input1Z')
		
		self.connect_md_node(in_x1 = normal_md + '.outputY', in_x2 = cmds.getAttr(str(ik_joints[0])+'.translate'+ axis), out_x = lower_lock_blend+ '.color1.color1R', mode = 'divide', name = '{}_DownLock_PV'.format(name))
		self.connect_md_node(in_x1 = normal_md + '.outputZ', in_x2 = cmds.getAttr(str(ik_joints[1])+'.translate'+ axis), out_x = upper_lock_blend + '.color1.color1R', mode = 'divide', name = '{}_UpLock_PV'.format(name))
		
		#volume preservation
		volume_attr = self.new_attr(input= attrs_location, name = 'Volume', min = 0 , max = 1, default = float(setup['volume_preservation']))

		upper_volume_blend = cmds.shadingNode('blendColors', asUtility=True, n = '{}_Volume{}'.format(ik_joints[2], nc['blend']))
		lower_volume_blend = cmds.shadingNode('blendColors', asUtility=True, n = '{}_Volume{}'.format(ik_joints[1], nc['blend']))
		cmds.setAttr('{}.color2.color2R'.format(upper_volume_blend), 1) 
		cmds.setAttr('{}.color2.color2R'.format(lower_volume_blend), 1) 

		cmds.connectAttr(volume_attr, '{}.blender'.format(upper_volume_blend))
		cmds.connectAttr(volume_attr, '{}.blender'.format(lower_volume_blend))

		self.connect_md_node(in_x1 = 1, in_x2 = upper_lock_blend+ '.output.outputR',out_x = upper_volume_blend+ '.color1.color1R', mode = 'divide', name = '{}_DownLock_PV'.format(name))
		self.connect_md_node(in_x1 = 1, in_x2 = lower_lock_blend+ '.output.outputR', out_x = lower_volume_blend+ '.color1.color1R', mode = 'divide', name = '{}_DownLock_PV'.format(name))

		volume_axis = ['X','Y','Z']
		volume_axis.remove(axis)
		#str(ik_joints[2])+'.scale{}'.format(axis)
		for scale_axis in volume_axis:
			cmds.connectAttr('{}.output.outputR'.format(upper_volume_blend), str(ik_joints[2])+'.scale{}'.format(scale_axis))
			cmds.connectAttr('{}.output.outputR'.format(upper_volume_blend), str(ik_joints[1])+'.scale{}'.format(scale_axis))

		#organize
		ik_grp = cmds.group(top_distance, ik_distance, distance,start_loc, end_loc, pv_loc ,normalize_loc , n = '{}_Stretchy{}'.format(ik, nc['group']))
		cmds.setAttr('{}.visibility'.format(ik_grp), 0)

		self.put_inside_rig_container([contidion_node,upper_lock_blend,upper_lock_blend, lower_lock_blend,upper_volume_blend, lower_volume_blend])

		return (ik_grp, normalize_loc, start_loc, end_loc, pv_loc, distance, top_distance, ik_distance)
		
	#----------------------------------------------------------------------------------------------------------------

	def simple_ik_chain(self, start = '', end = '', size = 1, color = setup['main_color'], ik_curve = setup['ik_ctrl'], pv_curve = setup['pv_ctrl'], pv = True, top_curve = setup['top_ik_ctrl']):
		"""This creates a simple IK chain between two joints with ctrls

		Args:
			start: string name of first joint
			end: string name of last joint
			size: string size of the controller
			color: string name of the color
			ik_curve: string type of controller based on curves.json
			pv_curve: string type of controller based on curves.json
			pv: bool true if pole vector
			top_curve: string type of controller based on curves.json

		Returns: ik_system

		"""

		if start == '':
			start = cmds.ls(sl =True)[0]
		if end == '':
			end = cmds.ls(sl =True)[-1]

		ik_system = []

		#create Ik Chain
		ik_handle = cmds.ikHandle (n = '{}{}'.format(end.replace(nc['joint'], ''), nc['ik_rp']), sj=start, ee= end, sol = 'ikRPsolver')
		cmds.rename(ik_handle[1],'{}{}'.format(end, nc['effector']))
		ik_handle = ik_handle[0]

		#create ik Controller with offset grp and clean attr
		ctrl = self.curve(type = ik_curve, rename = False, custom_name = True, name = '{}{}'.format(end, nc ['ctrl']), size = size)
		ctrl = cmds.rename(ctrl, ctrl.replace(nc['joint'],''))

		ik_system.append(ctrl)
		self.match(ctrl, end)
		cmds.rotate(0,0,0, a=True)

		#delete this below if want to maintain XYZ as axis
		cmds.delete(cmds.orientConstraint(end, ctrl,mo=False, skip = setup['twist_axis'].lower()))

		IK_grp = self.root_grp(replace_nc = True)
		self.hide_attr(ctrl, s = True, v = True)


		cmds.orientConstraint(ctrl, end ,mo =True)

		#parent ik to controller
		cmds.parentConstraint(ctrl, ik_handle, mo =True)
		cmds.group(ik_handle, n = ik_handle+ nc['group'])

		#create pole vector
		if (pv):

			#create pole vector in correct position
			pv_loc = self.pole_vector_placement(bone_one = start, bone_two = cmds.listRelatives(end, p = True), bone_three = end)

			#create controller in position with offset grp
			pv_ctrl = self.curve(type = pv_curve, rename = False, custom_name = True, name = '{}{}{}'.format(end,nc ['pole_vector'], nc ['ctrl']), size = size/2)
			pv_ctrl = cmds.rename(pv_ctrl, pv_ctrl.replace(nc['joint'],''))
			#cmds.rotate(0,0,0)
			ik_system.append(pv_ctrl)
			cmds.pointConstraint(pv_loc, pv_ctrl, mo=False)
			cmds.delete(pv_loc)
			pv_grp = self.root_grp(replace_nc = True)


			cmds.poleVectorConstraint(pv_ctrl, ik_handle)

			#clean controller
			self.hide_attr(pv_ctrl, r = True,  s = True, v = True)

			#connect with line
			line = self.connect_with_line(pv_ctrl, cmds.listRelatives(end, p=True)[0])
			print (line)
			
		#create top controler
		cmds.select(cl=True)
		top_ctrl = self.curve(type = top_curve, rename = False, custom_name = True, name = '{}{}'.format(start.replace(nc['joint'], ''), nc ['ctrl']), size = size*0.5)
		self.match(top_ctrl, start, r=False)
		top_grp = self.root_grp(replace_nc = True)

		self.hide_attr(top_ctrl,r = True,  s = True, v = True)
		ik_system.append(top_ctrl)

		cmds.parentConstraint(top_ctrl, start)

		#organize and add color

		#create IK Grp
		cmds.select(cl=True)
		ik_main_grp = cmds.group(n = start + nc['ctrl'] + nc ['group'], em =True)

		cmds.parent(pv_grp[0], ik_main_grp)
		cmds.parent(IK_grp[0], ik_main_grp)
		cmds.parent(top_grp[0], ik_main_grp)

		for c in ik_system:
			cmds.select(c)
			self.assign_color(color = color)

		#put the ik in the return list
		ik_system.append(ik_handle)		
		#add the line at the end
		ik_system.append(line[0])		

		#['L_Wrist_Ik_Ctrl', 'L_Wrist_Ik_PoleVector_Ctrl', 'L_Shoulder_Ik_Ctrl', 'L_Wrist_Ik_IKrp',
		#'L_Wrist_Ik_PoleVector_Ctrl_L_Elbow_Ik_Jnt_Connected_Crv']
		return ik_system


	#----------------------------------------------------------------------------------------------------------------

	def joints_middle(self, start = '', end = '', axis = setup['twist_axis'], amount = 4, name = 'Twist'):
		"""

		Args:
			start:
			end:
			axis:
			amount:
			name:

		Returns:

		"""
		'''
		create joints in between a joint chain
		'''
		if start == '':
			start = cmds.ls(sl =True)[0]
		if end == '':
			end = cmds.ls(sl =True)[-1]

		#create list for new joints
		middle_joints = []
		
		#create joints in between
		for i in range(amount):
			#duplicate joint and delete children
			middle_joint = cmds.duplicate(start, n = '{}_{}_{}{}'.format(start.replace(nc['joint'], ''),name,i, nc['joint']), rc = True)[0]
			cmds.delete(cmds.listRelatives(middle_joint, c = True))

			middle_joints.append(middle_joint)

			#if the new joint is not the first parent it to the last one
			if cmds.objExists('{}_{}_{}{}'.format(start.replace(nc['joint'], ''),name,i - 1, nc['joint'])):
				cmds.parent(middle_joint,'{}_{}_{}{}'.format(start.replace(nc['joint'], ''),name,i - 1, nc['joint']))
			
			else:
				try:cmds.parent(middle_joint, w=True)
				except:pass

		#Position joints in correct the spot... 
		
		for jnt in middle_joints:
			if jnt != middle_joints[0]:	
				cmds.setAttr('{}.translate{}'.format(jnt, axis), cmds.getAttr('{}.translate{}'.format(end, axis))/ (amount -1 ))

		#cmds.setAttr('{}.translate{}'.format(middle_joints[0], axis), 0)

	
		return middle_joints

	#----------------------------------------------------------------------------------------------------------------
	def joints_middle_no_chain(self, start = '', end='', axis = setup['twist_axis'], amount = 3, name = 'Mid'):
		"""

		Args:
			start:
			end:
			axis:
			amount:
			name:

		Returns:

		"""
		'''
		this will create joints in the middle of 2 selected objects but with out a Hy
		'''

		if start == '':
			start = cmds.ls(sl =True)[0]
		if end == '':
			end = cmds.ls(sl =True)[-1]

		if name == '':
			name = str(start).replace(nc['joint'],'') + '_Mid' + nc['joint']

		end_parent = cmds.listRelatives(end, p =True)			
		cmds.parent(end, start)

		mid_joints = self.joints_middle(start = start, end = end, axis = axis, amount = amount, name = name)
		cmds.parent(end, end_parent)

		for jnt in mid_joints:
			try:cmds.parent(jnt, w=True)
			except:pass
		
		return mid_joints

		#self.match(mid_joints[-1], end)

	#----------------------------------------------------------------------------------------------------------------

	def twist(self, start = '', end = '', axis = setup['twist_axis'], amount = 4, mode = 'down'):
		"""

		Args:
			start:
			end:
			axis:
			amount:
			mode:

		Returns:

		"""
		'''
		OLD
		old way of creating twist for limbs, i use this one on RdM Tools v2, recommend to use the advance one
		'''

		if start == '':
			start = cmds.ls(sl =True)[0]
		if end == '':
			end = cmds.ls(sl =True)[-1]

		twist_joints = self.joints_middle(start = start, end = end, axis = axis, amount = amount)
		
		#parent to upnode in hierarchy if possible
		try:cmds.parent(twist_joints[0], cmds.listRelatives(start, p = True))
		except:cmds.parent(twist_joints[0],w = True)

		#Ik Handle and pole vector set up
		ik_handle = cmds.ikHandle (n='{}_Twist{}'.format(start, nc['ik_rp']), sj=twist_joints[0], ee= twist_joints[1], sol = 'ikRPsolver')
		
		cmds.parent(ik_handle[0], start)
		
		cmds.setAttr('{}.poleVectorX'.format(ik_handle[0]), 0)
		cmds.setAttr('{}.poleVectorY'.format(ik_handle[0]), 0)
		cmds.setAttr('{}.poleVectorZ'.format(ik_handle[0]), 0)
		cmds.setAttr('{}.snapEnable'.format(ik_handle[0]), 0)
			   
		#Locator Setup
		aim_loc = cmds.spaceLocator(n ='{}_Twist{}'.format(start, nc ['locator']))
		
		#put the locator in correct pos
		if mode == 'up':

			cmds.xform(aim_loc, m = cmds.xform(twist_joints[0], q=1, m=1))
			cmds.parent(aim_loc,twist_joints[0])
			cmds.xform(aim_loc, t = (0,0,0), ra =(0,0,0))
			cmds.rotate( 0,0,0,aim_loc)
			cmds.orientConstraint(start, aim_loc, mo = True)

		elif mode == 'down':
			cmds.delete(cmds.parentConstraint(twist_joints[-1], aim_loc, mo =0))
			cmds.parent(aim_loc, twist_joints[0])
			cmds.xform(aim_loc, ra =(0,0,0))
			cmds.orientConstraint(end, aim_loc, mo = True)

		#connect twist to joints
		mult_node = cmds.shadingNode('multiplyDivide', asUtility=1, n  = '{}_Twist_Divide'.format(start))
		cmds.setAttr(str(mult_node)+'.operation', 2)
		cmds.setAttr(str(mult_node)+'.input2X', amount - 1 )
		cmds.connectAttr('{}.rotate{}'.format(aim_loc[0],axis), '{}.input1.input1X'.format(mult_node))

		#fix tranlation issue
		cmds.pointConstraint(start, twist_joints[0], mo = True)

		#connect joints to rotate
		return_joints = twist_joints
		twist_joints.remove(twist_joints[0])
		
		for twist_joint in twist_joints:
			cmds.connectAttr('{}.output.outputX'.format(mult_node), '{}.rotate{}'.format(twist_joint, axis))

		self.put_inside_rig_container([mult_node])

		return return_joints

	#----------------------------------------------------------------------------------------------------------------

	def twist_rotate_info(self, start = '', end = '', axis = setup['twist_axis'], driver = False):
		"""

		Args:
			start:
			end:
			axis:
			driver:

		Returns:

		"""
		'''
		create a system to correctly read the twist information for the desire joint, 
		it can be used from top to buttom or buttom to top
		'''

		if start == '':
			start = cmds.ls(sl =True)[0]
		if end == '':
			end = cmds.ls(sl =True)[-1]

		cmds.select(cl=True)
		print ('Twist axis is: '+ axis)

		#try to remove nameconventions
		try:
			name = start.replace(nc['joint'], '')
			name = start.replace(nc['joint_bind'], '')

		except: name = start

		#twist setup
		twist_root = cmds.joint(n=name + '_NoTwist{}'.format(nc['joint']), p =(0,0,0))
		twist_tip = cmds.joint(n=name + '_NoTwist_Tip{}'.format(nc['joint']), p = (1,0,0))
		
		twist_grp = cmds.group(twist_root, n= name + '_NoTwist{}'.format(nc['group']))
		cmds.xform(twist_grp, rp = (0,0,0), sp = (0,0,0))

		#locator reader
		loc = cmds.spaceLocator(n= name + '_Twist{}'.format(nc['locator']))[0]
		cmds.parent(loc, twist_root)

		#position in chain
		cmds.delete(cmds.parentConstraint(start, twist_grp, mo=False))
		cmds.delete(cmds.parentConstraint(end, twist_tip, mo=False))

		if driver:
			cmds.parentConstraint(driver, twist_grp, mo=True)

		#create IK for the locator to follor orientation
		ik_data = cmds.ikHandle(sj=twist_root, ee=twist_tip, sol='ikRPsolver')

		ik = cmds.rename(ik_data[0], name + '_NoTwist_IkHndl')
		cmds.rename(ik_data[1], name + "_" + nc['effector'])

		cmds.setAttr('{}.poleVectorX'.format(ik), 0)
		cmds.setAttr('{}.poleVectorY'.format(ik), 0)
		cmds.setAttr('{}.poleVectorZ'.format(ik), 0)
		cmds.pointConstraint(end, ik, mo=False)

		cmds.orientConstraint(start, loc, mo=True)
		cmds.pointConstraint(start, loc, mo=True)
		
		#cmds.setAttr(twist_root + '.ro', 3)
		# Offset Grps.
		offset_grp = self.root_grp(twist_root, replace_nc=True)[0]
		print (offset_grp)

		cmds.parent(loc, offset_grp)

		cmds.makeIdentity(twist_root, a=True, t=True, r=True, s=True)
		cmds.parent(loc, twist_root)
		
		return {'ik': ik, 'twist_grp': twist_grp, 'locator': loc, 'joint': twist_root, 'offset': offset_grp}		

	#----------------------------------------------------------------------------------------------------------------

	def advance_twist(self, start = '', end = '', axis = setup['twist_axis'], amount = 4, mode = 'up', driver = '', inverse =False):
		"""

		Args:
			start:
			end:
			axis:
			amount:
			mode:
			driver:
			inverse:

		Returns:

		"""
		'''
		create twist system for the chain, 
		this one can only be used by selecting from top to buttom joints but you can change the mode to up or down for desire effect
		
		OLD
		old way of creating twist for limbs, i use this one on RdM Tools v2, recommend to use the spline twist
		'''

		if start == '':
			start = cmds.ls(sl =True)[0]
		if end == '':
			end = cmds.ls(sl =True)[-1]


		if mode == 'up':
			twist_reader = self.twist_rotate_info(start=start, end=end)
		elif mode == 'down':
			twist_reader = self.twist_rotate_info(start=end, end=start)

		twist_locator = twist_reader['locator']
		twist_loc_grp = self.root_grp()

		#Create twist grps
		#create jnts in the middle
		twist_joints = self.joints_middle(start = start, end = end, axis = axis, amount = amount)
		if mode == 'down':
			cmds.parentConstraint(end, twist_joints[0], mo=True)
		else:
			cmds.parentConstraint(start, twist_joints[0], mo=True)
		#connect twist locator to joints using ik spline twist attr
		crv = self.curve_between(start=start, end=end)
		ik_spline = self.create_ik_spline_twist(start=twist_joints[0], end=twist_joints[-1], curve=crv)

		if inverse == True:
			mult = -1
		else:
			mult = 1
		twist_md = self.connect_md_node(in_x1 = '{}.rotate{}'.format(twist_locator,axis)
										, in_x2 = mult,
										out_x = '{}.twist'.format(ik_spline['ikHandle']),
										mode = 'mult',
										name = 'TwistMult')

		cmds.setAttr('{}.visibility'.format(twist_reader['twist_grp']), 0)
		twist_grp = cmds.group(twist_joints[0],crv, ik_spline['ikHandle'],twist_loc_grp, twist_reader['ik'] , n = '{}_{}_Twist{}'.format(start,end,nc['group']))
		
		#driver for twisting correctly
		if driver:
			##locator, joints y noTwist ik Handle = new grp
			driven_grp = cmds.group(twist_loc_grp, twist_reader['ik'], n = '{}_Twist_{}'.format(driver, nc['group']))
			cmds.parentConstraint(driver, driven_grp, mo=True)
			cmds.parent(twist_joints[0], driven_grp)

		cmds.setAttr('{}.inheritsTransform'.format(crv), 0)

		return {'twist_grp':twist_grp,'no_twist_grp': twist_reader['twist_grp'], 'joints':twist_joints, 'curve':crv}

	# ----------------------------------------------------------------------------------------------------------------

	def spline_twist(self, start = '', end = '', axis = setup['twist_axis'], amount = 4, mode = 'up', right_side = False):
		"""

		Args:
			start:
			end:
			axis:
			amount:
			mode:
			right_side: bool set Advance Attrs a bit different.

		Returns: {'twist_grp':twist_grp, 'joints':twist_joints, 'curve':spline_curve, 'ik_spline': ikSpline}

		"""

		if start == '':
			start = cmds.ls(sl=True)[0]
		if end == '':
			end = cmds.ls(sl=True)[-1]

		# Create twist grps
		# create jnts in the middle
		twist_joints = self.joints_middle(start=start, end=end, axis=axis, amount=amount)

		# twist setup
		cmds.select(d=True)
		twist_start = cmds.joint(n=start.replace(nc['joint'],'') + '_Twist{}'.format(nc['joint_ctrl']), ch = False)
		cmds.select(d=True)
		twist_end = cmds.joint(n=end.replace(nc['joint'],'') + '_Twist{}'.format(nc['joint_ctrl']), ch = False)

		# position in chain
		cmds.delete(cmds.parentConstraint(start,twist_start , mo=False))
		cmds.delete(cmds.parentConstraint(end, twist_end, mo=False))

		cmds.makeIdentity(twist_start,a=True, t=True, r=True, s=True)
		cmds.makeIdentity(twist_end,a=True, t=True, r=True, s=True)
		cmds.parentConstraint(start, twist_start, mo=False)
		cmds.parentConstraint(end, twist_end, mo=False)

		#create spline
		ikSpline = cmds.ikHandle(sj=twist_joints[0],
		                         ee=twist_joints[-1],
		                         sol='ikSplineSolver',
		                         n=twist_start.replace(nc['joint_ctrl'],nc['ik_spline']),
		                         ccv=True,
		                         pcv=False)

		spline_curve = ikSpline[2]
		spline_curve = cmds.rename(spline_curve, twist_start + nc['curve'])
		spline_curve = cmds.rebuildCurve(spline_curve, ch =  True,  rpo = True, rt = False, end =True, kr = False, kcp = False, kep = True , kt =False, s = 0, d = 1, tol = 0.01)[0]
		cmds.setAttr('{}.inheritsTransform'.format(spline_curve), 0)

		effector_spline = cmds.rename(ikSpline[1],
		                              start + nc['effector'])
		ikSpline = ikSpline[0]

		if mode == 'up':
			#no rotate joint
			cmds.select(d=True)
			no_rot_jnt = cmds.joint(n=end.replace(nc['joint'],'') + '_NoRotate{}'.format(nc['joint_ctrl']), ch=False)
			cmds.delete(cmds.parentConstraint(start, no_rot_jnt, mo=False))
			cmds.makeIdentity(no_rot_jnt, a=True, t=True, r=True, s=True)
			cmds.pointConstraint(start, no_rot_jnt, mo=False)
			cmds.skinCluster(no_rot_jnt, twist_end, spline_curve, tsb=True)

		else:
			cmds.skinCluster(twist_start, twist_end,spline_curve, tsb=True)

		# Enable twist
		cmds.setAttr("{}.dTwistControlEnable".format(ikSpline), 1)
		cmds.setAttr("{}.dWorldUpType".format(ikSpline), 4)
		if mode == 'up':
			cmds.connectAttr("{}.worldMatrix[0]".format(no_rot_jnt), "{}.dWorldUpMatrix".format(ikSpline), f=True)
		else:
			cmds.connectAttr("{}.worldMatrix[0]".format(twist_start), "{}.dWorldUpMatrix".format(ikSpline), f=True)

		cmds.connectAttr("{}.worldMatrix[0]".format(twist_end), "{}.dWorldUpMatrixEnd".format(ikSpline), f=True)

		twist_grp = cmds.group(twist_start, twist_end, twist_joints[0], ikSpline, spline_curve, n = '{}{}'.format(twist_start.replace(nc['joint_ctrl'], ''),nc['group']))

		cmds.setAttr("{}.dWorldUpAxis".format(ikSpline), 3)
		cmds.setAttr("{}.dWorldUpVectorY".format(ikSpline), 0)
		cmds.setAttr("{}.dWorldUpVectorEndY".format(ikSpline), 0)
		cmds.setAttr( "{}.dWorldUpVectorZ".format(ikSpline), 1)
		cmds.setAttr( "{}.dWorldUpVectorEndZ".format(ikSpline), 1)

		if mode == 'up':
			cmds.parent(no_rot_jnt, twist_grp)
			return {'twist_grp': twist_grp, 'joints': twist_joints, 'curve': spline_curve,'ik_spline': ikSpline ,'no_rotate': no_rot_jnt}

		else:
			return {'twist_grp':twist_grp, 'joints':twist_joints, 'curve':spline_curve, 'ik_spline': ikSpline}

	#----------------------------------------------------------------------------------------------------------------

	def simple_fk_ik(self, start = '', mid = '', end = '', size = 1, color = setup['main_color'], mode = setup['ik_fk_method'], twist_axis = setup['twist_axis']):
		"""

		Args:
			start:
			mid:
			end:
			size:
			color:
			mode:
			twist_axis:

		Returns:

		"""
		'''
		create a ik fk chain with a switch for 3 joints
		'''

		return_groups = []

		if start == '':
			start = cmds.ls(sl=True)[0]
			mid = cmds.ls(sl=True)[1]
			end = cmds.ls(sl=True)[2]

		print ('joints are: {} {} {}'.format(start,mid,end))

		#put name conventions to main chain
		if nc['joint'] in str(start):
			pass
		else: 
			start = cmds.rename(start, '{}{}'.format(start,nc['joint']))

		if nc['joint'] in str(mid):
			pass
		else: 
			mid = cmds.rename(mid, '{}{}'.format(mid,nc['joint']))

		if nc['joint'] in str(end):
			pass
		else: 
			end = cmds.rename(end, '{}{}'.format(end,nc['joint']))

		#manage errors if names exists
		if cmds.objExists(start):
			#cmds.error('we already have a system with theese names sorry')
			''
		main_joints = [start,mid,end]

		#duplicate chains to have the 3 of them
		cmds.select(start)
		ik_joints = self.duplicate_change_names( input = '', hi = True, search=nc['joint'], replace =nc['ik'])
		cmds.select(start)
		fk_joints = self.duplicate_change_names( input = start, hi = True, search=nc['joint'], replace =nc['fk'])
		
		#create FK System
		cmds.select(cl =True)

		for jnt in fk_joints:
			cmds.select(jnt, add = True)

		fk_system = self.fk_chain(size = size, color = color, curve_type = 'bounding_cube', scale = False)
		print ('FK = {}'.format(fk_system))
		#add fk group to retunr groups
		return_groups.append(cmds.listRelatives(fk_system[0], p =True)[0])

		#Create IK System
		print ('creating ik Chain for : {}'.format(start)),
		ik_system = self.simple_ik_chain(start = ik_joints[0], end = ik_joints[-1], size = size, color = color, pv = True)
		print ('IK = {}'.format(ik_system))

		#correct pv placement and connect with line
		pv_distance = cmds.getAttr('{}.translate{}'.format(mid, twist_axis))
		print (pv_distance)
		cmds.select(cmds.listRelatives(ik_system[1], p=True))
		'''
		if start.startswith(nc['right']):
			cmds.move(pv_distance*-1.5, 0, 0 , r=1, os=1, wd=1)
			#cmds.rotate(0,0,0)
		else:
			cmds.move(pv_distance*1.5, 0, 0 , r=1, os=1, wd=1)
			#cmds.rotate(0,0,0)
		'''
		cmds.move(pv_distance * 1.5, 0, 0, r=1, os=1, wd=1)
		#cmds.rotate(0,0,0)

		#add ik group to return groups
		return_groups.append(cmds.listRelatives(ik_system[0], p =True)[0])
		return_groups.append(cmds.listRelatives(ik_system[2], p =True)[0])
		return_groups.append(cmds.listRelatives(return_groups[1], p =True)[0])
		print (return_groups)
		print ('__________')

		#add swtich attr in all controllers
		ik_fk_controllers = fk_system + ik_system
		for ctrl in ik_fk_controllers :
			cmds.select(ctrl)
			if cmds.objectType(ctrl) ==  'transform':
				switch_attr = self.shape_with_attr(input = '', obj_name = '{}_Switch'.format(start), attr_name = 'Switch_IK_FK')

		#create switch ik fk
		print (switch_attr)

		for num, jnt in enumerate(main_joints):
			if mode == 'blend':
				self.switch_blend_colors(this = fk_joints[num], that = ik_joints[num], main = jnt, attr = switch_attr)
			else: 
				self.switch_constraints(this = fk_joints[num], that = ik_joints[num], main = jnt, attr = switch_attr)

		#connect visibility
		#FK Ctrl Grp					
		cmds.connectAttr(switch_attr, '{}.visibility'.format(return_groups[0]))

		#IK
		reverse_node = cmds.shadingNode('reverse', asUtility = True)
		cmds.connectAttr(switch_attr, '{}.input.inputX'.format(reverse_node))
		cmds.connectAttr('{}.output.outputX'.format(reverse_node), '{}.visibility'.format(return_groups[3]))
		cmds.connectAttr('{}.output.outputX'.format(reverse_node),
		                 '{}.visibility'.format(cmds.listRelatives(ik_system[0], p=True)[0]), f=True)
		cmds.connectAttr('{}.output.outputX'.format(reverse_node),
		                 '{}.visibility'.format(cmds.listRelatives(ik_system[1], p=True)[0]), f=True)
		cmds.connectAttr('{}.output.outputX'.format(reverse_node),
		                 '{}.visibility'.format(ik_system[4]), f=True)
		cmds.connectAttr('{}.output.outputX'.format(reverse_node),
		                 '{}.visibility'.format(cmds.listRelatives(ik_system[2], p=True)[0]), f=True)

		#create rotate order and line
		for main in main_joints:
			self.connect_rotate_order(input = main, object = '{}_Switch_Loc'.format(start))
	
		#create ik stretchy system
		ik_stretch = self.streatchy_ik(ik = ik_system[3], ik_ctrl= ik_system[0], top_ctrl = ik_system[2], pv_ctrl = ik_system[1], attrs_location = '{}_Switch_Loc'.format(start), name = '', axis = twist_axis)
		ik_system.append(ik_stretch)

		self.put_inside_rig_container([reverse_node])

		print (main_joints, ik_joints, fk_joints, fk_system, ik_system, return_groups)
		return main_joints, ik_joints, fk_joints, fk_system, ik_system, return_groups

	#----------------------------------------------------------------------------------------------------------------

	def twist_fk_ik(self, start = '', mid = '', end = '', size = 1, color = setup['main_color'], mode = setup['ik_fk_method'], twist_axis = setup['twist_axis'], twist_amount = 6):
		"""

		Args:
			start:
			mid:
			end:
			size:
			color:
			mode:
			twist_axis:
			twist_amount:

		Returns:

		"""
		'''
		create a ik fk chain with a switch for 3 joints, includes the twist information so is a full limb module
		'''

		#create basic ik fk system
		ik_fk = self.simple_fk_ik(start = start, mid = mid, end = end, size = size, color = color, mode = mode, twist_axis = twist_axis)

		#add the twists
		main_joints = ik_fk[0]

		if main_joints[0].startswith(nc['right']):
			right_inverse = True
		else:
			right_inverse = False

		upper_twist= self.spline_twist(start=main_joints[0], end=main_joints[1], axis=setup['twist_axis'], amount=twist_amount, mode='up')
		lower_twist= self.spline_twist(start=main_joints[1], end=main_joints[2], axis=setup['twist_axis'], amount=twist_amount, mode='down')

		print (upper_twist)
		print (lower_twist)

		#connect scale to twist joints
		for jnt in upper_twist['joints']:
			cmds.connectAttr('{}.scale'.format(main_joints[0]), '{}.scale'.format(jnt))
		for jnt in lower_twist['joints']:
			cmds.connectAttr('{}.scale'.format(main_joints[1]), '{}.scale'.format(jnt))

		return {'ik_fk':ik_fk,'upper_twist':upper_twist, 'lower_twist':lower_twist}

        #IKFK 
        #[0] ['L_Shoulder_Jnt', 'L_Elbow_Jnt', 'L_Wrist_Jnt'],
        #[1] ['L_Shoulder_Ik_Jnt', 'L_Elbow_Ik_Jnt', 'L_Wrist_Ik_Jnt'], 
        #[2] ['L_Shoulder_Fk_Jnt', 'L_Elbow_Fk_Jnt', 'L_Wrist_Fk_Jnt'], 
        #[3] ['L_Shoulder_Fk_Ctrl', 'L_Elbow_Fk_Ctrl', 'L_Wrist_Fk_Ctrl'], 
        #[4] ['L_Wrist_Ik_Ctrl', 'L_Wrist_Ik_PoleVector_Ctrl', 'L_Shoulder_Ik_Ctrl', 'L_Wrist_Ik_IKrp', 'L_Wrist_Ik_PoleVector_Ctrl_L_Elbow_Ik_Jnt_Connected_Crv', ('L_Wrist_Ik_IKrp_Stretchy_Grp', 'L_Wrist_Ik_IKrp_NormalScale_Loc', ['L_Wrist_Ik_Jnt_Stretchy_Loc'], ['L_Shoulder_Ik_Jnt_Stretchy_Loc'], ['L_Elbow_Ik_Jnt_Stretchy_Loc'], 'L_Shoulder_Ik_Jnt_L_Wrist_Ik_Jnt_Distance_Shape', 'L_Elbow_Ik_Jnt_L_Wrist_Ik_Jnt_Distance_Shape', 'L_Shoulder_Ik_Jnt_L_Elbow_Ik_Jnt_Distance_Shape')], ['L_Shoulder_Fk_Ctrl_Offset_Grp', 'L_Wrist_Ik_Ctrl_Offset_Grp', 'L_Shoulder_Ik_Ctrl_Offset_Grp', 'L_Shoulder_Ik_Jnt_Ctrl_Grp'])
        #[5] ['L_Shoulder_Fk_Ctrl_Offset_Grp', 'L_Wrist_Ik_Ctrl_Offset_Grp', 'L_Shoulder_Ik_Ctrl_Offset_Grp', 'L_Shoulder_Ik_Jnt_Ctrl_Grp'])


	#----------------------------------------------------------------------------------------------------------------

	def base_spline(self, start = '', end = '', size = 1, name = 'Spine', twist_axis = setup['twist_axis'], amount = 5):
		"""

		Args:
			start:
			end:
			size:
			name:
			twist_axis:
			amount:

		Returns:

		"""

		'''
		select start and end and create a ik fk spline like for a charatcer spine
		'''

		if start == '':
			start = cmds.ls(sl=True)[0]
			end = cmds.ls(sl=True)[-1]

		print ('joints are: {} to {}'.format(start,end))
		
		#put name conventions to main chain and manage errors
		if str(start).endswith(nc['joint']):
			pass
		else: 
			start = cmds.rename(start, '{}{}'.format(start,nc['joint']))

		if str(end).endswith(nc['joint']):
			pass
		else: 
			end = cmds.rename(end, '{}{}'.format(end,nc['joint']))


		main_joints = [start]
		for jnt in cmds.listRelatives(start, allDescendents=True):
			
			if str(jnt).endswith(nc['joint']):
				pass
			else:
				jnt = cmds.rename(jnt, '{}{}'.format(jnt,nc['joint']))	
			
			main_joints.append(jnt)


		#create ik handle
		ikSpline = cmds.ikHandle(sj=start,
								 ee=end,
								 sol='ikSplineSolver',
								 n= main_joints[0] + nc['ik_spline'],
								 ccv=True,
								 pcv = False)

		spline_curve =  ikSpline[2]
		spline_curve = cmds.rename(spline_curve, start + nc['curve'])
		spline_curve = cmds.rebuildCurve(spline_curve, ch =  True,  rpo = True, rt = False, end =True, kr = False, kcp = False, kep = True , kt =False, s = amount-1, d = 3, tol = 0.01)

		effector_spline = cmds.rename(ikSpline[1],
									 start + nc['effector'])
		ikSpline = ikSpline[0]

		#create joints for twisting the chain ik
		twist_ik_joints = self.joints_middle_no_chain(start = start, end=end, axis = twist_axis, amount = 2, name = 'Twist')

		#create joints for controlling the chain ik
		ik_joints = self.joints_middle_no_chain(start = start, end=end, axis = twist_axis, amount = amount, name = 'Ik')
		cmds.skinCluster(ik_joints,spline_curve, tsb=True)
		
		#create a ctrl for the iks
		ik_controllers=[]
		for num, jnt in enumerate(ik_joints):
			cmds.select(jnt)
			ik_controller = self.curve(type = setup['ik_ctrl'], size = size, custom_name = True, name = '{}_{}_IK{}'.format(name, num,nc['ctrl']))
			grp = self.root_grp()
			self.match(grp, jnt)
			cmds.parentConstraint(ik_controller, jnt, mo=True)
			ik_controllers.append(ik_controller)
		
		#create FK Controllers that will hold the Ik Controllers
		#this joints are placeholders
		temp_fk_joints = self.joints_middle_no_chain(start = start, end=end, axis = twist_axis, amount = amount, name = 'Fk_Temp')
		fk_controllers = []
		for num, joint in enumerate(temp_fk_joints):
			print (num, joint)
			cmds.select(cl=True)
			fk_controller = self.curve(type = setup['spine_fk_ctrl'], size = size, custom_name = True, name = '{}_{}_FK{}'.format(name, num,nc['ctrl']))
			fk_grp = self.root_grp(fk_controller)
			self.match(fk_grp, joint,r=False)
			if len(fk_controllers) > 0:cmds.parent(fk_grp[0], fk_controllers[-1])
			else:pass 

			#Create Controller List
			fk_controllers.append(fk_controller)


		cmds.delete(temp_fk_joints)

		#put the ik inside the fks
		for num, ik in enumerate(ik_controllers):
			cmds.parent(cmds.listRelatives(ik, p=True), fk_controllers[num])

		return fk_controllers, ik_controllers

	#----------------------------------------------------------------------------------------------------------------

	def mirror_group(self, input = '', world = True):
		"""

		Args:
			input: if not specify it will use selection else specify string
			world:

		Returns:

		"""

		if input == '':
			input = cmds.ls(sl=True)[0]

		mirror_grp =cmds.group(em=True, n = '{}Mirror{}'.format(input,nc['group']))
		if world == False:
			cmds.delete(cmds.parentConstraint(input, mirror_grp))
		cmds.parent(input, mirror_grp)
		
		if world == True:
			cmds.xform(mirror_grp, rp= (0,0,0), sp = (0,0,0))

		cmds.setAttr('{}.scaleX'.format(mirror_grp), -1)
		cmds.setAttr('{}.scaleY'.format(mirror_grp), -1)
		cmds.setAttr('{}.scaleZ'.format(mirror_grp), -1)

		cmds.setAttr('{}.rotateX'.format(mirror_grp), 180)

		return mirror_grp

	#----------------------------------------------------------------------------------------------------------------

	def basic_ribbon(self, start = '', end = '', divisions = 5, name = 'Ribbon', ctrl_type = 'circleY',size = 1):
		"""

		Args:
			start:
			end:
			divisions:
			name:
			ctrl_type:
			size:

		Returns:

		"""
		#this will create a plane between 2 objects and then create a ribbon rig for you

		if start ==  '':
			start = cmds.ls(sl=True)[0]
			end = cmds.ls(sl=True)[1]

		#create a nurbs etween and then create the follicles to it
		surface = self.nurbs_between(start=start,end=end)
		surface = cmds.rebuildSurface(surface, ch =False, dv=3,du=3, su=0,sv=divisions)
		surface = cmds.rename(surface, name + nc['joint'] +nc['nurb'])

		cmds.select(surface)
		mel.eval("createHair 1 {} 10 0 0 0 0 5 0 1 2 1".format(divisions))
		cmds.delete ('hairSystem1','pfxHair1','nucleus1')
		cmds.setAttr( surface +'.inheritsTransform', 0)
		
		fol_joints = []
		ctrl_joints = []
		for num in range (1, divisions+1):
			#delete crated curve and folicle rename
			fol = cmds.rename(cmds.listRelatives('curve' + str (num) , p=True), name + '_' +str(num) + nc['follicle'] )
			try:cmds.delete ('curve' + str (num) )
			except: pass
			#create joints for later bind
			cmds.select(fol)
			jnt = cmds.joint(n = fol + nc ['joint'])
			fol_joints.append(jnt)

			#joint to bind the ruibbon and add ctrls
			cmds.select(cl=True)
			cltr_joint = cmds.joint(n = fol.replace(nc ['follicle'],nc ['joint']))
			self.match(cltr_joint, jnt)
			cmds.setAttr('{}.radius'.format(cltr_joint), 1.25)
			ctrl_joints.append(cltr_joint)

		cmds.rename ('hairSystem1Follicles', name + nc['follicle']+nc['group'])
		
		follicles = cmds.ls(name + nc['follicle']+nc['group'], dag = True, type = 'follicle')

		#bind skin to nurbs
		cmds.select(ctrl_joints, surface)
		cmds.skinCluster(n = name.replace(nc['joint'], nc['skin_cluster']), toSelectedBones=True)
		cmds.select(surface)
		mel.eval('doPruneSkinClusterWeightsArgList 1 { "0.3" };')

		#controllers
		controllers =[]
		roots_grps = []
		for num, jnt in enumerate(ctrl_joints):
			cmds.select(jnt)
			ctrl = self.curve(type = ctrl_type, custom_name= True, name = str(jnt).replace(nc['joint'], nc['ctrl']), size = size * 0.75)
			grp = self.root_grp()[0]
			cmds.parentConstraint(ctrl , jnt, mo=True)
			#cmds.scaleConstraint(ctrl , jnt, mo=True)
			controllers.append(ctrl)
			roots_grps.append(grp)
			cmds.scaleConstraint(ctrl ,fol_joints[num], mo=True)

		main_ctrl_grp = cmds.group(roots_grps, n = name + nc['ctrl'] + nc['group'])
		cmds.group(ctrl_joints, n = name + nc['joint'] + nc['group'])

		return {'surface':surface, 
				'follicles':follicles,
				'fol_joints':fol_joints,
				'ctrl_joints':ctrl_joints,
				'controllers':controllers,
				'controllers_grp':main_ctrl_grp}

	
	#----------------------------------------------------------------------------------------------------------------

	def ribbon_between(self, start = '', end = '', divisions = 5, name = 'Ribbon', ctrl_type = 'circleY', size = 1):
		"""

		Args:
			start:
			end:
			divisions:
			name:
			ctrl_type:
			size:

		Returns:

		"""
		if start ==  '':
			start = cmds.ls(sl=True)[0]
			end = cmds.ls(sl=True)[1]
		
		#run main basic ribbon
		basic_ribbon = self.basic_ribbon(start = start, end = end, divisions = divisions, name = name, ctrl_type = ctrl_type, size = size)
		
		#create a new nursb to drive the ctrls
		ctrl_surface = cmds.duplicate(basic_ribbon['surface'], n = name + nc['ctrl'] +nc['nurb'])[0]
		ctrl_surface = cmds.rebuildSurface(ctrl_surface, ch =False, dv=1,du=1, su=1,sv=1)[0]

		cmds.select(ctrl_surface)
		mel.eval("createHair 1 {} 10 0 0 0 0 5 0 1 2 1".format(divisions))
		cmds.delete ('hairSystem1','pfxHair1','nucleus1')
		cmds.setAttr( ctrl_surface +'.inheritsTransform', 0)
		
		fol_joints = []
		for num in range (1, divisions+1):
			#delete crated curve and folicle rename
			fol = cmds.rename(cmds.listRelatives('curve' + str (num) , p=True), name + nc['ctrl'] + '_' +str(num) + nc['follicle'] )
			try:cmds.delete ('curve' + str (num) )
			except: pass

			#parent fol to ctrl offset grp
			cmds.parentConstraint(fol,cmds.listRelatives(basic_ribbon['controllers'][num-1], p=True))
		
		ctrl_fol_grp = cmds.rename ('hairSystem1Follicles', name + nc['follicle']+nc['ctrl']+nc['group'])
		
		#bind skin to nurbs
		cmds.select(start,end, ctrl_surface)
		skin = cmds.skinCluster(n = name.replace(nc['joint'], nc['skin_cluster']), toSelectedBones=True, dr = 10)[0]
		cmds.skinPercent(skin, '{}.cv[0:1][1]'.format(ctrl_surface), transformValue=[(end, 1)])
		cmds.skinPercent(skin, '{}.cv[0:1][0]'.format(ctrl_surface), transformValue=[(start, 1)])

		cmds.group(basic_ribbon['surface'], ctrl_surface , n = name + nc['nurb'] + nc['group'])

		return {'surface':[basic_ribbon['surface'],ctrl_surface], 
				'follicles':basic_ribbon['follicles'],
				'fol_joints':basic_ribbon['fol_joints'],
				'ctrl_joints':basic_ribbon['ctrl_joints'],
				'controllers':basic_ribbon['controllers'],
				'controllers_grp':basic_ribbon['controllers_grp'],
				'ctrl_fol_grp': ctrl_fol_grp}


	#----------------------------------------------------------------------------------------------------------------

	def blend_between(self, ctrl = None, blends = '', attr_position = 'ctrl', attr_name = 'Blends'):
		"""Create blends

		Args:
			ctrl: main ctrl name
			blends: string of blends separated by comas ,
			attr_position: where to put the attrs: default in same ctrl
			attr_name: attrs name, default is blends

		Returns:

		"""
		#inputs checks
		if not ctrl:
			cmds.error('No control assigned')

		if not blends:
			cmds.error('No blends assigned')

		if attr_position == 'ctrl':
			attr_position = ctrl

		#create main blends group for locators
		if not cmds.objExists('Blends' + nc['group']):
			blends_grp = cmds.group(n='Blends' + nc['group'], em=True)
		else:
			blends_grp = 'Blends' + nc['group']

		#get misc group and parent blends group in it
		misc_grp = setup['rig_groups']['misc'] + nc['group']
		if cmds.objExists(misc_grp):
			try:cmds.parent(blends_grp, misc_grp)
			except:pass

		#create blends gtroup for blends over main ctrl
		cmds.select(ctrl)
		if not cmds.objExists(ctrl + '_Blend' + nc['group']):
			blend_grp = self.root_grp(custom=True, custom_name='_Blend')
		else:
			blend_grp = ctrl + '_Blend' + nc['group']

		#blends stuffs
		blends = blends.split(',')
		blend_groups = []
		for blend in blends:
			print(blend)
			#creato locator in blends group for the parents
			blend_loc = cmds.spaceLocator(n = blend.replace(nc['joint'],nc['locator']).replace(nc['ctrl'],nc['locator']))
			self.match(blend_loc, blend)
			cmds.parentConstraint(blend, blend_loc, mo=False)
			cmds.parent(blend_loc, blends_grp)

			cmds.select(ctrl)

		cmds.select(ctrl)

	def parent_matrix(self, this=None, that=None, translate=True, rotate=True, scale=True, offset=True):
		# get data by selection if not assign
		if this == None:
			this = cmds.ls(sl=True)[0]
		if that == None:
			that = cmds.ls(sl=True)[1]

		# get offset values before connecting everything:
		if offset:
			from maya.api.OpenMaya import MMatrix
			offset = cmds.createNode('network', n=this + '_Offset')
			this_matrix = MMatrix(cmds.xform(this, ws=True, q=True, m=True))
			that_matrix = MMatrix(cmds.xform(that, ws=True, q=True, m=True))
			result = this_matrix * that_matrix

			cmds.addAttr(offset, ln='OffsetMatrix', at='matrix')
			cmds.setAttr(offset + '.OffsetMatrix', result, type="matrix")

		# create mult matrix to multiply the world matrix * the invert matrix so we got a new worl matrix for the target
		decompose = cmds.createNode('decomposeMatrix', n=this + '_DecomposeMatrix')
		mult_matrix = cmds.createNode('multMatrix', n=this + '_MultMatrix')

		cmds.connectAttr('{}.worldMatrix'.format(this), '{}.matrixIn[0]'.format(mult_matrix))
		cmds.connectAttr('{}.matrixSum'.format(mult_matrix), '{}.inputMatrix'.format(decompose))
		cmds.connectAttr('{}.parentInverseMatrix'.format(that), '{}.matrixIn[1]'.format(mult_matrix))

		# decide with one do we want to connect
		if translate:
			cmds.connectAttr('{}.outputTranslate'.format(decompose), '{}.translate'.format(that))
		if rotate:
			cmds.connectAttr('{}.outputRotate'.format(decompose), '{}.rotate'.format(that))
		if scale:
			cmds.connectAttr('{}.outputScale'.format(decompose), '{}.scale'.format(that))

		# connect extra offset matrix to the main one
		if offset:
			# shift one connections down becouse mult order is important in matrix
			cmds.connectAttr('{}.OffsetMatrix'.format(offset), '{}.matrixIn[0]'.format(mult_matrix), f=True)
			cmds.connectAttr('{}.worldMatrix'.format(this), '{}.matrixIn[1]'.format(mult_matrix), f=True)
			cmds.connectAttr('{}.parentInverseMatrix'.format(that), '{}.matrixIn[2]'.format(mult_matrix), f=True)

		self.put_inside_rig_container([offset,decompose,mult_matrix])

		return True