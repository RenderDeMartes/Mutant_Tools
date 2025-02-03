from __future__ import absolute_import, division
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
reload(Mutant_Tools.Utils.Rigging.kinematics)

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
import maya.api.OpenMaya as om

import os
try:
	import importlib;from importlib import reload
except:
	import imp;from imp import reload

import json
from pathlib import Path

try: 
	import tools
	reload(tools)

except:
	import Mutant_Tools
	import Mutant_Tools.Utils.Rigging
	from Mutant_Tools.Utils.Rigging import tools
	reload(Mutant_Tools.Utils.Rigging.tools)

#----------------------------------------------------------------------------------------------------------------

#Read name conventions as self.nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-2]
FOLDER=''
for f in PATH_PARTS:
	FOLDER = os.path.join(FOLDER, f)


nc, curve_data, setup = tools.nc, tools.curve_data, tools.setup


#----------------------------------------------------------------------------------------------------------------
#create base class for selection objects

class Kinematics_class(tools.Tools_class):
	def __init__(self):
		super(Kinematics_class, self).__init__()
	
	def fk_chain(self, input = '', size = 1, color = setup['main_color'], curve_type = setup['fk_ctrl'], scale = True, twist_axis = setup['twist_axis'], world_orient=False, direct_connect = False) :
		"""
		Create a FK Chain with selected joints.

		Args:
			input (str): The input joint or a string representing the selection. If not specified, it will use the selected joints.
			size (int): The size of the FK controllers.
			color (str): The color of the controllers.
			curve_type (str): The type of curve used for the controllers.
			scale (bool): Whether to add a scale constraint to the controllers.
			twist_axis (str): The aim axis of the joints for creating bounding cubes.
			world_orient (bool): Whether to perform world orientation on the controllers.
			direct_connect (bool): Whether to directly connect the controllers to the joints.

		Returns:
			list: A list of FK controllers.

		Raises:
			None

		This function creates a FK (Forward Kinematics) chain with the selected joints. The settings for the chain can be customized in the setup
		JSON file.

		The `input` parameter allows specifying the input joint or using the selected joints by leaving it empty. The `size` parameter determines
		the size of the FK controllers. The `color` parameter sets the color of the controllers. The `curve_type` parameter determines the type of
		curve used for the controllers, which can be customized in the setup JSON file.

		The `scale` parameter controls whether a scale constraint is added to the controllers. The `twist_axis` parameter specifies the aim axis
		of the joints when creating bounding cubes. The `world_orient` parameter determines whether to perform world orientation on the
		controllers.

		If `direct_connect` is set to `True`, the controllers will be directly connected to the joints. Otherwise, they will be parented using
		constraints.

		The function returns a list of FK controllers created.

		Note:
			This function assumes the existence of other helper methods such as `check_input`, `bounding_cube`, `curve`, `root_grp`, `assign_color`,
			and `hide_attr`. Please ensure that these methods are implemented and correctly handle their respective functionalities.
		"""


		#Check input
		if input != '':
			self.input = [input]
			
		else:   
			self.input = input  
		
		self.check_input('fk_chain')	

		fk_controllers = []
		selected_joints = cmds.ls(sl =True)
		for num, bone in enumerate(selected_joints):
			
			#Create controller and groups to zero it
			#fk_controller = cmds.circle( n = '{}{}'.format(bone,self.nc['ctrl']) , nr = (1,0,0), r = size)[0]
			if curve_type == 'bounding_cube':
				fk_controller = self.bounding_cube(input = bone, size = size, name =  '{}{}'.format(bone,self.nc['ctrl']), axis = twist_axis)
			else:
				fk_controller = self.curve(input = bone, type = curve_type, custom_name = True, name = '{}{}'.format(bone,self.nc['ctrl']), size = size)

			if self.nc['joint'] in str(fk_controller):
				fk_controller = cmds.rename(fk_controller, fk_controller.replace(self.nc['joint'],''))

			if world_orient:
				cmds.setAttr('{}.rotateX'.format(fk_controller), 0)
				cmds.setAttr('{}.rotateY'.format(fk_controller), 0)
				cmds.setAttr('{}.rotateZ'.format(fk_controller), 0)
				cmds.delete(cmds.pointConstraint(bone, fk_controller))
				try:
					cmds.delete(cmds.aimConstraint(selected_joints[num+1], fk_controller, aimVector=(0, 1, 0), upVector=(0, 1, 0),
											   worldUpType='vector', mo=False))
				except:
					pass

				print('World Orient in FK Chain')
			else:
				cmds.delete(cmds.parentConstraint(bone, fk_controller)) #put the controller in position

			#create Root Grp
			fk_auto_grp = self.root_grp(replace_nc = False)

			#add connections
			if direct_connect:
				root, auto = self.root_grp(input = bone, autoRoot=True)
				cmds.connectAttr('{}.translate'.format(fk_controller), '{}.translate'.format(auto))
				cmds.connectAttr('{}.rotate'.format(fk_controller), '{}.rotate'.format(auto))
				if scale == True:
					cmds.connectAttr('{}.scale'.format(fk_controller), '{}.scale'.format(auto))
			else:
				cmds.parentConstraint(fk_controller,bone, mo=True) #parent Ctrl to Bone
				if scale == True:
					cmds.scaleConstraint(fk_controller,bone, mo=True) #parent Ctrl to Bone

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
		"""
		Get the perfect Polevector position.

		Args:
			bone_one (str): The first joint in the chain.
			bone_two (str): The second joint in the chain.
			bone_three (str): The third joint in the chain.
			back_distance (float): The distance to move the pole vector position backward.

		Returns:
			str: The name of the temporary locator.

		Raises:
			None

		This function calculates and returns the perfect position for the Polevector in a joint chain. The positions of the three joints are
		specified using the `bone_one`, `bone_two`, and `bone_three` parameters. Alternatively, if no parameters are provided, the function will
		use the currently selected joints.

		The function calculates the Polevector position based on the positions of the three joints. It uses vector math and algorithms to find
		the most suitable position. The calculated position is then used to create a temporary locator that can be used for visual reference.

		The `back_distance` parameter allows adjusting the position backward, which can be useful for animators.

		The function returns the name of the temporary locator created.

		Note:
			This function relies on the OpenMaya module for vector calculations and transformations. Please ensure that the module is available and
			properly imported before using this function.
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
		
		loc = cmds.spaceLocator(n = '{}{}'.format(bone_two[0], self.nc['locator']))[0]
		cmds.xform(loc , ws =1 , t= (finalV.x , finalV.y ,finalV.z*back_distance))
		
		cmds.xform ( loc , ws = 1 , rotation = ((rot.x/math.pi*180.0),
		(rot.y/math.pi*180.0),
		(rot.z/math.pi*180.0)))
		
		return loc

	#----------------------------------------------------------------------------------------------------------------

	def streatchy_ik(self, ik = '', ik_ctrl= '', top_ctrl = '', pv_ctrl = '', attrs_location = '', name = '', axis = 'Y'):
		"""
		Generate all the nodes necessary to create an IK stretching system.

		Args:
			ik (string): Name of the IK on the limb.
			ik_ctrl (string): Name of the IK Ctrl.
			top_ctrl (string): Name of the Top IK Ctrl.
			pv_ctrl (string): Name of the PV Ctrl.
			attrs_location (string): Location where to put the attributes.
			name (string): Name of the system.
			axis (string): Name of the twist axis to obtain correct lengths.

		Returns:
			tuple: A tuple containing the following nodes and locators:
				- ik_grp: The top-level group node that contains all the created nodes.
				- normalize_loc: The locator used for normalizing the stretch.
				- start_loc: Locator positioned at the base joint of the IK chain.
				- end_loc: Locator positioned at the end joint of the IK chain.
				- pv_loc: Locator positioned at the pole vector control.
				- distance: Distance dimension node representing the length of the IK chain.
				- top_distance: Distance dimension node representing the length between the base joint and the pole vector.
				- ik_distance: Distance dimension node representing the length between the end joint and the pole vector.

		Notes:
			- This function generates nodes and connections for a stretchy IK system.
			- The function assumes that the IK chain is already set up and the necessary controls and joints are passed as arguments.
			- The function creates locators to represent the start, end, and pole vector positions of the IK chain.
			- It also creates distance dimension nodes to measure the lengths of different segments.
			- The stretchy math is calculated based on the distances and joint scales.
			- Additional attributes for controlling the system, such as stretchiness, pole vector lock, and volume preservation, are created.
			- The function organizes all the nodes under a top-level group node and returns the necessary nodes and locators.

		Usage:
			# Example usage with default arguments
			ik_grp, normalize_loc, start_loc, end_loc, pv_loc, distance, top_distance, ik_distance = streatchy_ik()

			# Example usage with custom arguments
			ik_grp, normalize_loc, start_loc, end_loc, pv_loc, distance, top_distance, ik_distance = streatchy_ik(
				ik='left_arm_ik',
				ik_ctrl='left_arm_ik_ctrl',
				top_ctrl='left_arm_top_ctrl',
				pv_ctrl='left_arm_pv_ctrl',
				attrs_location='left_arm_attrs',
				name='left_arm_stretchy',
				axis='Y'
			)
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

		start_loc = cmds.spaceLocator(n = str(ik_joints[0]) + '_Stretchy' + self.nc['locator'])
		cmds.xform(start_loc, t = first_pos)
		cmds.setAttr(str(start_loc[0])+'.visibility', 0)
		end_loc = cmds.spaceLocator(n = str(ik_joints[-1])+ '_Stretchy'+ self.nc['locator'])
		cmds.xform(end_loc, t = end_pos)
		cmds.setAttr(str(end_loc[0])+'.visibility', 0)
		pv_loc = cmds.spaceLocator(n = str(ik_joints[1])+ '_Stretchy'+ self.nc['locator'])
		cmds.xform(pv_loc, t = pv_pos)
		cmds.setAttr(str(pv_loc[0])+'.visibility', 0)

		cmds.parentConstraint(top_ctrl, start_loc)
		cmds.parentConstraint(ik_ctrl, end_loc)
		cmds.parentConstraint(pv_ctrl, pv_loc)
				
		#distances nodes
		#main distance
		distance = cmds.distanceDimension(sp=first_pos, ep=end_pos)
		distance = cmds.rename(distance, ik_joints[-1] + '_' + ik_joints[0]+ self.nc['distance']+'_Shape')
		cmds.rename(cmds.listRelatives(distance, p =True), ik_joints[-1] + '_' + ik_joints[0]+ self.nc['distance'])
		cmds.setAttr('{}.visibility'.format(distance), 0)
		#top PV distance
		top_distance = cmds.distanceDimension(sp=first_pos, ep=pv_pos)
		top_distance = cmds.rename(top_distance, ik_joints[1] + '_' + ik_joints[0]+ self.nc['distance']+'_Shape')
		cmds.rename(cmds.listRelatives(top_distance, p =True), ik_joints[1] + '_' + ik_joints[0]+ self.nc['distance'])
		cmds.setAttr('{}.visibility'.format(top_distance), 0)		
		#IK PV distance
		ik_distance = cmds.distanceDimension(sp=end_pos, ep=pv_pos)
		ik_distance = cmds.rename(ik_distance, ik_joints[-1] + '_' + ik_joints[1]+ self.nc['distance']+'_Shape')
		cmds.rename(cmds.listRelatives(ik_distance, p =True), ik_joints[-1] + '_' + ik_joints[1]+ self.nc['distance'])	
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

		show_top_ctrl_attr = self.new_enum(input=attrs_location, name='TopIk', enums='Hide:Show', keyable=False)
		cmds.connectAttr(show_top_ctrl_attr, cmds.listRelatives(top_ctrl, s=True)[0]+'.v')
		#This is used in the build block for the limb
		show_gimbal = self.new_enum(input=attrs_location, name='SubIk', enums='Hide:Show', keyable=False)

		stretch_Attr = self.new_attr(input= attrs_location, name = 'Stretch_On', min = 0 , max = 1, default = int(self.setup['stretch_default']))

		#IK Stretchy Nodes and Connections from RdM2 
		contidion_node = cmds.shadingNode('condition', asUtility=True, n= end_joint[0]+self.nc['condition'])
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
		normalize_loc = cmds.spaceLocator(n = name + '_NormalScale' + self.nc['locator'])[0]
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

		upper_lock_blend = cmds.shadingNode('blendColors', asUtility=True, n = '{}_Lock{}'.format(ik_joints[1], self.nc['blend']))
		cmds.connectAttr(lock_attr, '{}.blender'.format(upper_lock_blend))
		cmds.connectAttr('{}.output.outputR'.format(upper_lock_blend), str(ik_joints[2])+'.scale{}'.format(axis), f=True)
		cmds.connectAttr('{}.outputX'.format(md1),'{}.color2.color2R'.format(upper_lock_blend), f=True)

		lower_lock_blend = cmds.shadingNode('blendColors', asUtility=True, n = '{}_Lock{}'.format(ik_joints[2], self.nc['blend']))
		cmds.connectAttr(lock_attr, '{}.blender'.format(lower_lock_blend))
		cmds.connectAttr('{}.output.outputR'.format(lower_lock_blend), str(ik_joints[1])+'.scale{}'.format(axis) , f=True)
		cmds.connectAttr('{}.outputX'.format(md2),'{}.color2.color2R'.format(lower_lock_blend), f=True)

		#connect lock pole vectors distance to normalize too
		cmds.connectAttr(str(top_distance)+'.distance', normal_md + '.input1Y')
		cmds.connectAttr(str(ik_distance)+'.distance', normal_md + '.input1Z')
		
		self.connect_md_node(in_x1 = normal_md + '.outputY', in_x2 = cmds.getAttr(str(ik_joints[0])+'.translate'+ axis), out_x = lower_lock_blend+ '.color1.color1R', mode = 'divide', name = '{}_DownLock_PV'.format(name))
		self.connect_md_node(in_x1 = normal_md + '.outputZ', in_x2 = cmds.getAttr(str(ik_joints[1])+'.translate'+ axis), out_x = upper_lock_blend + '.color1.color1R', mode = 'divide', name = '{}_UpLock_PV'.format(name))
		
		#volume preservation
		volume_attr = self.new_attr(input= attrs_location, name = 'Volume', min = 0 , max = 1, default = float(self.setup['volume_preservation']))

		upper_volume_blend = cmds.shadingNode('blendColors', asUtility=True, n = '{}_Volume{}'.format(ik_joints[2], self.nc['blend']))
		lower_volume_blend = cmds.shadingNode('blendColors', asUtility=True, n = '{}_Volume{}'.format(ik_joints[1], self.nc['blend']))
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
		ik_grp = cmds.group(top_distance, ik_distance, distance,start_loc, end_loc, pv_loc ,normalize_loc , n = '{}_Stretchy{}'.format(ik, self.nc['group']))
		cmds.setAttr('{}.visibility'.format(ik_grp), 0)

		self.put_inside_rig_container([contidion_node,upper_lock_blend,upper_lock_blend, lower_lock_blend,upper_volume_blend, lower_volume_blend])

		return (ik_grp, normalize_loc, start_loc, end_loc, pv_loc, distance, top_distance, ik_distance)
		
	#----------------------------------------------------------------------------------------------------------------

	def simple_ik_chain(self, start = '', end = '', size = 1, color = setup['main_color'], ik_curve = setup['ik_ctrl'], pv_curve = setup['pv_ctrl'], pv = True, top_curve = setup['top_ik_ctrl']):
		"""
		Create a simple IK chain between two joints with controllers.

		Args:
			start (string): Name of the first joint. If empty, the currently selected joint will be used.
			end (string): Name of the last joint. If empty, the last selected joint will be used.
			size (string): Size of the controller.
			color (string): Name of the color for the controllers.
			ik_curve (string): Type of controller based on curves.json.
			pv_curve (string): Type of pole vector controller based on curves.json.
			pv (bool): True if pole vector controller should be created.
			top_curve (string): Type of top controller based on curves.json.

		Returns:
			list: A list containing the following elements:
				- ik_ctrl: Name of the IK controller.
				- pv_ctrl: Name of the pole vector controller (if created).
				- top_ctrl: Name of the top controller.
				- ik_handle: Name of the IK handle.
				- line: Name of the line connecting the pole vector controller to the end joint.

		Notes:
			- This function creates an IK chain between two joints and generates controllers for IK, pole vector, and top control.
			- The function assumes that the necessary arguments for joints, sizes, colors, and curve types are provided.
			- If the 'start' and 'end' arguments are empty, the function will use the currently selected joints.
			- The function creates an IK handle and renames it accordingly.
			- It creates an IK controller with an offset group and clean attributes.
			- The IK controller is aligned with the end joint and can be oriented based on the twist axis.
			- The function creates an IK group and orients the end joint to the IK controller.
			- The IK handle is parent-constrained to the IK controller.
			- If the 'pv' argument is True, a pole vector controller is created.
			- The pole vector controller is positioned correctly and connected to the IK handle.
			- The pole vector controller is cleaned up, and a line is created to connect it to the end joint.
			- A top controller is created and parent-constrained to the start joint.
			- The function organizes all the nodes and controllers under an IK group and assigns colors to the controllers.
			- The function returns a list of the IK system components.

		Usage:
			# Example usage with default arguments
			ik_system = simple_ik_chain()

			# Example usage with custom arguments
			ik_system = simple_ik_chain(
				start='joint1',
				end='joint2',
				size='small',
				color='blue',
				ik_curve='curve_type1',
				pv_curve='curve_type2',
				pv=True,
				top_curve='curve_type3'
			)
		"""

		if start == '':
			start = cmds.ls(sl =True)[0]
		if end == '':
			end = cmds.ls(sl =True)[-1]

		ik_system = []

		#create Ik Chain
		ik_handle = cmds.ikHandle (n = '{}{}'.format(end.replace(self.nc['joint'], ''), self.nc['ik_rp']), sj=start, ee= end, sol = 'ikRPsolver')
		cmds.rename(ik_handle[1],'{}{}'.format(end, self.nc['effector']))
		ik_handle = ik_handle[0]

		#create ik Controller with offset grp and clean attr
		ctrl = self.curve(type = ik_curve, rename = False, custom_name = True, name = '{}{}'.format(end, nc ['ctrl']), size = size)
		ctrl = cmds.rename(ctrl, ctrl.replace(self.nc['joint'],''))

		ik_system.append(ctrl)
		self.match(ctrl, end)
		cmds.rotate(0,0,0, a=True)

		#delete this below if want to maintain XYZ as axis
		cmds.delete(cmds.orientConstraint(end, ctrl,mo=False, skip = self.setup['twist_axis'].lower()))

		IK_grp = self.root_grp(replace_nc = True)
		self.hide_attr(ctrl, s = True, v = True)


		cmds.orientConstraint(ctrl, end ,mo =True)

		#parent ik to controller
		cmds.parentConstraint(ctrl, ik_handle, mo =True)
		cmds.group(ik_handle, n = ik_handle+ self.nc['group'])

		#create pole vector
		if (pv):

			#create pole vector in correct position
			pv_loc = self.pole_vector_placement(bone_one = start, bone_two = cmds.listRelatives(end, p = True), bone_three = end)

			#create controller in position with offset grp
			pv_ctrl = self.curve(type = pv_curve, rename = False, custom_name = True, name = '{}{}{}'.format(end,nc ['pole_vector'], nc ['ctrl']), size = size/2)
			pv_ctrl = cmds.rename(pv_ctrl, pv_ctrl.replace(self.nc['joint'],''))
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
		top_ctrl = self.curve(type = top_curve, rename = False, custom_name = True, name = '{}{}'.format(start.replace(self.nc['joint'], ''), nc ['ctrl']), size = size*0.5)
		self.match(top_ctrl, start, r=False)
		top_grp = self.root_grp(replace_nc = True)

		self.hide_attr(top_ctrl,r = True,  s = True, v = True)
		ik_system.append(top_ctrl)

		cmds.parentConstraint(top_ctrl, start)

		#organize and add color

		#create IK Grp
		cmds.select(cl=True)
		ik_main_grp = cmds.group(n = start + self.nc['ctrl'] + nc ['group'], em =True)

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
		Create joints in between a joint chain.

		Args:
			start (str): Name of the first joint. If empty, the currently selected joint will be used.
			end (str): Name of the last joint. If empty, the last selected joint will be used.
			axis (str): Twist axis.
			amount (int): Number of joints to create in between.
			name (str): Name prefix for the created joints.

		Returns:
			list: A list containing the names of the newly created joints.

		Notes:
			- This function creates a series of joints in between a joint chain.
			- The function assumes that the necessary arguments for the start and end joints, twist axis, amount, and name are provided.
			- If the 'start' and 'end' arguments are empty, the function will use the currently selected joints.
			- The function duplicates the start joint and deletes its children to create the middle joints.
			- The names of the middle joints follow the pattern: "startName_nameIndex_joint".
			- The middle joints are parented to each other in order.
			- The function positions the middle joints in the correct spot along the twist axis.
			- The function returns a list of the names of the newly created middle joints.

		Usage:
			# Example usage with default arguments
			middle_joints = joints_middle()

			# Example usage with custom arguments
			middle_joints = joints_middle(
				start='joint1',
				end='joint2',
				axis='x',
				amount=3,
				name='TwistChain'
			)
		"""
		if start == '':
			start = cmds.ls(sl =True)[0]
		if end == '':
			end = cmds.ls(sl =True)[-1]

		#create list for new joints
		middle_joints = []
		
		#create joints in between
		for i in range(amount):
			#duplicate joint and delete children
			middle_joint = cmds.duplicate(start, n = '{}_{}_{}{}'.format(start.replace(self.nc['joint'], ''),name,i, self.nc['joint']), rc = True)[0]
			cmds.delete(cmds.listRelatives(middle_joint, c = True))

			middle_joints.append(middle_joint)

			#if the new joint != the first parent it to the last one
			if cmds.objExists('{}_{}_{}{}'.format(start.replace(self.nc['joint'], ''),name,i - 1, self.nc['joint'])):
				cmds.parent(middle_joint,'{}_{}_{}{}'.format(start.replace(self.nc['joint'], ''),name,i - 1, self.nc['joint']))
			
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
		Create joints in the middle of two selected objects but without a hierarchy.

		Args:
			start (str): Name of the first object. If empty, the first selected object will be used.
			end (str): Name of the second object. If empty, the last selected object will be used.
			axis (str): Twist axis.
			amount (int): Number of joints to create in between.
			name (str): Name prefix for the created joints.

		Returns:
			list: A list containing the names of the newly created joints.

		Notes:
			- This function creates a series of joints in between two selected objects without creating a hierarchy.
			- The function assumes that the necessary arguments for the start and end objects, twist axis, amount, and name are provided.
			- If the 'start' and 'end' arguments are empty, the function will use the first and last selected objects, respectively.
			- The function temporarily parents the end object under the start object to create the middle joints.
			- The names of the middle joints follow the pattern: "startName_MidIndex_joint".
			- The middle joints are created using the 'joints_middle' function.
			- After creating the middle joints, the end object is restored to its original parent.
			- The function returns a list of the names of the newly created middle joints.

		Usage:
			# Example usage with default arguments
			middle_joints = joints_middle_no_chain()

			# Example usage with custom arguments
			middle_joints = joints_middle_no_chain(
				start='object1',
				end='object2',
				axis='x',
				amount=3,
				name='MidJoints'
			)
		"""

		if start == '':
			start = cmds.ls(sl =True)[0]
		if end == '':
			end = cmds.ls(sl =True)[-1]

		if name == '':
			name = str(start).replace(self.nc['joint'],'') + '_Mid' + self.nc['joint']

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
		Create a twist setup for limbs using an old method.
		Old way of creating twist for limbs, i use this one on RdM Tools v2, recommend to use the new advance one

		Args:
			start (str): Name of the first joint in the limb. If empty, the first selected joint will be used.
			end (str): Name of the last joint in the limb. If empty, the last selected joint will be used.
			axis (str): Twist axis.
			amount (int): Number of twist joints to create in between the start and end joints.
			mode (str): Twist mode. Possible values: 'up' or 'down'.

		Returns:
			list: A list containing the names of the twist joints.

		Notes:
			- This function creates a twist setup for limbs using an old method.
			- The function assumes that the necessary arguments for the start and end joints, twist axis, amount, and mode are provided.
			- If the 'start' and 'end' arguments are empty, the function will use the first and last selected joints, respectively.
			- The twist joints are created using the 'joints_middle' function.
			- The function parents the twist joints to the upnode in the hierarchy if possible.
			- It sets up an IK handle and a pole vector constraint.
			- It creates a locator and positions it based on the specified mode ('up' or 'down').
			- The twist rotation is connected to the twist joints using a multiplyDivide node.
			- The function returns a list of the names of the twist joints.

		Usage:
			# Example usage with default arguments
			twist_joints = twist()

			# Example usage with custom arguments
			twist_joints = twist(
				start='joint1',
				end='joint2',
				axis='x',
				amount=4,
				mode='up'
			)
		"""


		if start == '':
			start = cmds.ls(sl =True)[0]
		if end == '':
			end = cmds.ls(sl =True)[-1]

		twist_joints = self.joints_middle(start = start, end = end, axis = axis, amount = amount)
		
		#parent to upnode in hierarchy if possible
		try:cmds.parent(twist_joints[0], cmds.listRelatives(start, p = True))
		except:cmds.parent(twist_joints[0],w = True)

		#Ik Handle and pole vector set up
		ik_handle = cmds.ikHandle (n='{}_Twist{}'.format(start, self.nc['ik_rp']), sj=twist_joints[0], ee= twist_joints[1], sol = 'ikRPsolver')
		
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
		Create a system to correctly read the twist information for the desired joint.

		Args:
			start (str): Name of the first joint in the chain. If empty, the first selected joint will be used.
			end (str): Name of the last joint in the chain. If empty, the last selected joint will be used.
			axis (str): Twist axis.
			driver (bool): Flag indicating whether to use a driver joint as the parent of the twist group.

		Returns:
			dict: A dictionary containing information about the created twist setup:
				- 'ik': Name of the IK handle.
				- 'twist_grp': Name of the twist group.
				- 'locator': Name of the locator.
				- 'joint': Name of the twist root joint.
				- 'offset': Name of the offset group.

		Notes:
			- This function creates a system to correctly read the twist information for the desired joint.
			- The function assumes that the necessary arguments for the start and end joints, twist axis, and driver are provided.
			- If the 'start' and 'end' arguments are empty, the function will use the first and last selected joints, respectively.
			- It creates a twist setup by adding a root joint, tip joint, twist group, and a locator.
			- The twist group and locator are positioned along the chain using parent constraints.
			- If the 'driver' flag is set to True, a parent constraint is applied between the driver joint and the twist group.
			- An IK handle is created to make the locator follow the orientation of the twist chain.
			- Offset groups are created using the 'root_grp' method.
			- The function returns a dictionary containing information about the created twist setup.

		Usage:
			# Example usage with default arguments
			twist_info = twist_rotate_info()

			# Example usage with custom arguments
			twist_info = twist_rotate_info(
				start='joint1',
				end='joint2',
				axis='x',
				driver=True
			)
		"""

		if start == '':
			start = cmds.ls(sl =True)[0]
		if end == '':
			end = cmds.ls(sl =True)[-1]

		cmds.select(cl=True)
		print ('Twist axis is: '+ axis)

		#try to remove nameconventions
		try:
			name = start.replace(self.nc['joint'], '')
			name = start.replace(self.nc['joint_bind'], '')

		except: name = start

		#twist setup
		twist_root = cmds.joint(n=name + '_NoTwist{}'.format(self.nc['joint']), p =(0,0,0))
		twist_tip = cmds.joint(n=name + '_NoTwist_Tip{}'.format(self.nc['joint']), p = (1,0,0))
		
		twist_grp = cmds.group(twist_root, n= name + '_NoTwist{}'.format(self.nc['group']))
		cmds.xform(twist_grp, rp = (0,0,0), sp = (0,0,0))

		#locator reader
		loc = cmds.spaceLocator(n= name + '_Twist{}'.format(self.nc['locator']))[0]
		cmds.parent(loc, twist_root)

		#position in chain
		cmds.delete(cmds.parentConstraint(start, twist_grp, mo=False))
		cmds.delete(cmds.parentConstraint(end, twist_tip, mo=False))

		if driver:
			cmds.parentConstraint(driver, twist_grp, mo=True)

		#create IK for the locator to follor orientation
		ik_data = cmds.ikHandle(sj=twist_root, ee=twist_tip, sol='ikRPsolver')

		ik = cmds.rename(ik_data[0], name + '_NoTwist_IkHndl')
		cmds.rename(ik_data[1], name + "_" + self.nc['effector'])

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
		Create a twist system for the chain.

		Args:
			start (str): Name of the first joint in the chain. If empty, the first selected joint will be used.
			end (str): Name of the last joint in the chain. If empty, the last selected joint will be used.
			axis (str): Twist axis.
			amount (int): Number of twist joints to create.
			mode (str): Twist mode. Options: 'up' (default), 'down'.
			driver (str): Name of the driver joint for twisting correctly. If empty, no driver will be used.
			inverse (bool): Flag indicating whether to invert the twist direction.

		Returns:
			dict: A dictionary containing information about the created twist system:
				- 'twist_grp': Name of the twist group.
				- 'no_twist_grp': Name of the no_twist group.
				- 'joints': List of twist joints.
				- 'curve': Name of the created curve.

		Notes:
			- This function creates a twist system for a joint chain.
			- The function assumes that the necessary arguments for the start and end joints, twist axis, and mode are provided.
			- If the 'start' and 'end' arguments are empty, the function will use the first and last selected joints, respectively.
			- The 'amount' argument determines the number of twist joints to create between the start and end joints.
			- The 'mode' argument determines the direction of the twist system. Options: 'up' (default), 'down'.
			- The 'driver' argument specifies the name of the driver joint for twisting correctly. If empty, no driver will be used.
			- The 'inverse' flag can be set to True to invert the twist direction.
			- The function creates twist joints in the middle of the chain using the 'joints_middle' method.
			- It connects the twist locator to the joints using the IK spline twist attribute.
			- A curve is created between the start and end joints using the 'curve_between' method.
			- An IK spline twist setup is created using the 'create_ik_spline_twist' method.
			- The twist rotation is controlled by a multiply-divide node connected to the twist locator's rotation attribute.
			- The twist group's visibility is set to 0.
			- The function returns a dictionary containing information about the created twist system.

		Usage:
			# Example usage with default arguments
			twist_system = advance_twist()

			# Example usage with custom arguments
			twist_system = advance_twist(
				start='joint1',
				end='joint2',
				axis='x',
				amount=4,
				mode='up',
				driver='driver_joint',
				inverse=False
			)
		"""

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
		twist_grp = cmds.group(twist_joints[0],crv, ik_spline['ikHandle'],twist_loc_grp, twist_reader['ik'] , n = '{}_{}_Twist{}'.format(start,end,self.nc['group']))
		
		#driver for twisting correctly
		if driver:
			##locator, joints y noTwist ik Handle = new grp
			driven_grp = cmds.group(twist_loc_grp, twist_reader['ik'], n = '{}_Twist_{}'.format(driver, self.nc['group']))
			cmds.parentConstraint(driver, driven_grp, mo=True)
			cmds.parent(twist_joints[0], driven_grp)

		cmds.setAttr('{}.inheritsTransform'.format(crv), 0)

		return {'twist_grp':twist_grp,'no_twist_grp': twist_reader['twist_grp'], 'joints':twist_joints, 'curve':crv}

	# ----------------------------------------------------------------------------------------------------------------

	def spline_twist(self, start = '', end = '', axis = setup['twist_axis'], amount = 4, mode = 'up', right_side = False):
		"""
		Create a spline twist system for the chain.

		Args:
			start (str): Name of the first joint in the chain. If empty, the first selected joint will be used.
			end (str): Name of the last joint in the chain. If empty, the last selected joint will be used.
			axis (str): Twist axis.
			amount (int): Number of twist joints to create.
			mode (str): Twist mode. Options: 'up' (default), 'down'.
			right_side (bool): Flag indicating whether to set Advance Attrs differently.

		Returns:
			dict: A dictionary containing information about the created spline twist system:
				- 'twist_grp': Name of the twist group.
				- 'joints': List of twist joints.
				- 'curve': Name of the created spline curve.
				- 'ik_spline': Name of the IK spline handle.

		Notes:
			- This function creates a spline twist system for a joint chain.
			- The function assumes that the necessary arguments for the start and end joints, twist axis, and mode are provided.
			- If the 'start' and 'end' arguments are empty, the function will use the first and last selected joints, respectively.
			- The 'amount' argument determines the number of twist joints to create between the start and end joints.
			- The 'mode' argument determines the direction of the twist system. Options: 'up' (default), 'down'.
			- The 'right_side' flag can be set to True to indicate a right-side setup with different attributes.
			- The function creates twist joints in the middle of the chain using the 'joints_middle' method.
			- It creates twist start and end joints for the twist setup.
			- The twist start joint is positioned at the start joint using a parent constraint.
			- The twist end joint is positioned at the end joint using a parent constraint.
			- A spline curve is created between the twist start and end joints using the 'ikHandle' command.
			- The spline curve is rebuilt using the 'rebuildCurve' command.
			- The twist setup is skinned to the spline curve using the 'skinCluster' command.
			- The twist rotation is controlled by enabling twist control and setting up the world up vectors.
			- The twist group is created and all relevant nodes are grouped under it.
			- The function returns a dictionary containing information about the created spline twist system.

		Usage:
			# Example usage with default arguments
			twist_system = spline_twist()

			# Example usage with custom arguments
			twist_system = spline_twist(
				start='joint1',
				end='joint2',
				axis='x',
				amount=4,
				mode='up',
				right_side=False
			)
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
		twist_start = cmds.joint(n=start.replace(self.nc['joint'],'') + '_TwistStart{}'.format(self.nc['joint_ctrl']), ch = False)
		cmds.select(d=True)
		twist_end = cmds.joint(n=end.replace(self.nc['joint'],'') + '_TwistEnd{}'.format(self.nc['joint_ctrl']), ch = False)

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
								 n=twist_start.replace(self.nc['joint_ctrl'],self.nc['ik_spline']),
								 ccv=True,
								 pcv=False)

		spline_curve = ikSpline[2]
		spline_curve = cmds.rename(spline_curve, twist_start + self.nc['curve'])
		spline_curve = cmds.rebuildCurve(spline_curve, ch =  True,  rpo = True, rt = False, end =True, kr = False, kcp = False, kep = True , kt =False, s = 0, d = 1, tol = 0.01)[0]
		cmds.setAttr('{}.inheritsTransform'.format(spline_curve), 0)

		effector_spline = cmds.rename(ikSpline[1],
									  start + self.nc['effector'])
		ikSpline = ikSpline[0]

		if mode == 'up':
			#no rotate joint
			cmds.select(d=True)
			no_rot_jnt = cmds.joint(n=end.replace(self.nc['joint'],'') + '_NoRotate{}'.format(self.nc['joint_ctrl']), ch=False)
			no_rot_jnt_root = self.root_grp()
			cmds.delete(cmds.parentConstraint(start, no_rot_jnt_root, mo=False))
			cmds.makeIdentity(no_rot_jnt, a=True, t=True, r=True, s=True)
			cmds.skinCluster(no_rot_jnt, twist_end, spline_curve, tsb=True)
			cmds.parentConstraint(start, no_rot_jnt_root, mo=True)
			#no ratote inv rotation euler
			euler_to_quad_node = cmds.createNode('eulerToQuat', n = start + '_UTQ')
			quad_to_euler_node = cmds.createNode('quatToEuler', n = start + '_QTE')

			cmds.connectAttr('{}.rotate'.format(start), '{}.inputRotate'.format(euler_to_quad_node))
			cmds.connectAttr('{}.outputQuat.outputQuatW'.format(euler_to_quad_node), '{}.inputQuat.inputQuatW'.format(quad_to_euler_node))
			cmds.connectAttr('{}.outputQuat.outputQuatX'.format(euler_to_quad_node), '{}.inputQuat.inputQuatX'.format(quad_to_euler_node))

			self.connect_md_node(in_x1='{}.outputRotate.outputRotateX'.format(quad_to_euler_node),
								 in_x2=-1,
								 out_x = '{}.rotateX'.format(no_rot_jnt),
								 mode = 'mult')

		else:
			cmds.skinCluster(twist_start, twist_end,spline_curve, tsb=True)

		twist_grp = cmds.group(twist_start, twist_end, twist_joints[0], ikSpline, spline_curve, n = '{}{}'.format(twist_start.replace(self.nc['joint_ctrl'], ''),self.nc['group']))

		# Enable twist
		cmds.setAttr("{}.dTwistControlEnable".format(ikSpline), 1)
		cmds.setAttr("{}.dWorldUpType".format(ikSpline), 4)
		if mode == 'up':
			cmds.connectAttr("{}.worldMatrix[0]".format(no_rot_jnt), "{}.dWorldUpMatrix".format(ikSpline), f=True)
			cmds.connectAttr("{}.worldMatrix[0]".format(twist_end), "{}.dWorldUpMatrixEnd".format(ikSpline), f=True)

		else:
			### L_Elbow_TwistStart_Grp
			### L_Wrist_TwistReader_JntCtrl_Offset_GrpL_Wrist_Jnt_Twist_Reader_Grp_Grp

			#Create new driver system
			cmds.select(cl=True)
			twist_reader = cmds.joint(n=end.replace(self.nc['joint'],'') + '_TwistReader{}'.format(self.nc['joint_ctrl']))
			self.match(twist_reader, twist_end)
			cmds.makeIdentity(twist_reader, a=True, t=True, r=True, s=True)

			root_grp = self.root_grp()[0]
			self.match(root_grp, twist_end)
			root_of_root = self.root_grp(input=root_grp, custom=True, custom_name=end+'_Twist_Reader'+nc['group'])
			self.match(root_of_root, twist_end)


			cmds.parentConstraint(twist_start, root_grp, mo=True)
			cmds.scaleConstraint(twist_start, root_grp, mo=True)

			#Complex setup for twist reader
			mult = cmds.shadingNode('multMatrix', asUtility=True, n=twist_reader+'_multMatrix')
			decompose = cmds.createNode("decomposeMatrix", n=twist_reader+'_decomposeMatrix')
			quat = cmds.shadingNode('quatToEuler', asUtility=True, n=twist_reader+'_quatToEuler')

			cmds.connectAttr('{}.worldMatrix[0]'.format(end), '{}.matrixIn[0]'.format(mult))
			cmds.connectAttr('{}.worldInverseMatrix[0]'.format(root_grp), '{}.matrixIn[1]'.format(mult))

			cmds.connectAttr('{}.matrixSum'.format(mult), '{}.inputMatrix'.format(decompose))

			cmds.connectAttr('{}.outputQuatX'.format(decompose), '{}.inputQuatX'.format(quat))
			cmds.connectAttr('{}.outputQuatW'.format(decompose), '{}.inputQuatW'.format(quat))

			cmds.connectAttr('{}.outputRotateX'.format(quat), '{}.rotateX'.format(twist_reader))

			cmds.connectAttr("{}.worldMatrix[0]".format(twist_start), "{}.dWorldUpMatrix".format(ikSpline), f=True)
			cmds.connectAttr("{}.worldMatrix[0]".format(twist_reader), "{}.dWorldUpMatrixEnd".format(ikSpline), f=True)

			cmds.parent(root_of_root, twist_grp)

		cmds.setAttr("{}.dWorldUpAxis".format(ikSpline), 3)
		cmds.setAttr("{}.dWorldUpVectorY".format(ikSpline), 0)
		cmds.setAttr("{}.dWorldUpVectorEndY".format(ikSpline), 0)
		cmds.setAttr( "{}.dWorldUpVectorZ".format(ikSpline), 1)
		cmds.setAttr( "{}.dWorldUpVectorEndZ".format(ikSpline), 1)

		if mode == 'up':
			cmds.parent(no_rot_jnt_root, twist_grp)
			return {'twist_grp': twist_grp, 'joints': twist_joints, 'curve': spline_curve,'ik_spline': ikSpline ,'no_rotate': no_rot_jnt}

		else:
			return {'twist_grp':twist_grp, 'joints':twist_joints, 'curve':spline_curve, 'ik_spline': ikSpline, 'twist_reader' : twist_reader, 'twist_grp_to_mirror' : root_of_root}

	#----------------------------------------------------------------------------------------------------------------

	def simple_fk_ik(self, start = '', mid = '', end = '', size = 1, color = setup['main_color'], mode = setup['ik_fk_method'], twist_axis = setup['twist_axis'], use_shared_loc=True):
		"""
		Create an FK/IK chain with a switch for 3 joints.

		Args:
			start (str): Name of the start joint. If not provided, the first selected joint will be used.
			mid (str): Name of the middle joint. If not provided, the second selected joint will be used.
			end (str): Name of the end joint. If not provided, the third selected joint will be used.
			size (float): Size of the controls.
			color (tuple): Color of the controls in RGB format.
			mode (str): IK/FK blending mode. Can be 'blend' or 'constraints'.
			twist_axis (str): Twist axis for the IK chain. Can be 'X', 'Y', or 'Z'.

		Returns:
			tuple: A tuple containing the main joints, IK joints, FK joints, FK system, IK system, and return groups.

		Notes:
			- This function creates an FK/IK chain with controls and a switch to blend between the two.
			- The FK controls drive the joints directly, while the IK controls use an IK solver.
			- The switch attribute determines the influence of the IK and FK controls on the joints.
			- The visibility of the FK and IK controls is controlled by the switch attribute.

		Examples:
			# Example 1: Create an FK/IK chain with default settings
			main_joints, ik_joints, fk_joints, fk_system, ik_system, return_groups = simple_fk_ik()

			# Example 2: Create an FK/IK chain with custom joint names and size
			main_joints, ik_joints, fk_joints, fk_system, ik_system, return_groups = simple_fk_ik(start='arm_01_joint', mid='arm_02_joint', end='arm_03_joint', size=0.5)

			# Example 3: Create an FK/IK chain with custom color and IK/FK blending mode
			main_joints, ik_joints, fk_joints, fk_system, ik_system, return_groups = simple_fk_ik(color=(1, 0.5, 0), mode='constraints')
		"""

		return_groups = []

		if start == '':
			start = cmds.ls(sl=True)[0]
			mid = cmds.ls(sl=True)[1]
			end = cmds.ls(sl=True)[2]

		print ('joints are: {} {} {}'.format(start,mid,end))

		#put name conventions to main chain
		if self.nc['joint'] in str(start):
			pass
		else: 
			start = cmds.rename(start, '{}{}'.format(start,self.nc['joint']))

		if self.nc['joint'] in str(mid):
			pass
		else: 
			mid = cmds.rename(mid, '{}{}'.format(mid,self.nc['joint']))

		if self.nc['joint'] in str(end):
			pass
		else: 
			end = cmds.rename(end, '{}{}'.format(end,self.nc['joint']))

		#manage errors if names exists
		if cmds.objExists(start):
			#cmds.error('we already have a system with theese names sorry')
			''
		main_joints = [start,mid,end]

		#duplicate chains to have the 3 of them
		cmds.select(start)
		ik_joints = self.duplicate_change_names( input = '', hi = True, search=self.nc['joint'], replace =self.nc['ik'])
		cmds.select(start)
		fk_joints = self.duplicate_change_names( input = start, hi = True, search=self.nc['joint'], replace =self.nc['fk'])
		
		#create FK System
		cmds.select(cl =True)

		for jnt in fk_joints:
			cmds.select(jnt, add = True)

		fk_system = self.fk_chain(size = size, color = color, curve_type = setup['fk_ctrl'], scale = False)
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
		if start.startswith(self.nc['right']):
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
		if use_shared_loc:
			for ctrl in ik_fk_controllers :
				cmds.select(ctrl)
				if cmds.objectType(ctrl) == 'transform':
					switch_attr = self.shape_with_attr(input='', obj_name='{}_Switch'.format(start), attr_name='Switch_IK_FK')
		else:
			share_ctrl = self.curve(input=end,
							type='gear',
							rename=True,
							custom_name=True,
							name=start.replace(nc['joint'], '_Attrs'+nc['ctrl']),
							size=size)

			self.assign_color(color=color)
			root_grp = self.root_grp()[0]
			self.match(root_grp, end, r=True, t=True)
			cmds.parentConstraint(end, root_grp)
			self.hide_attr(share_ctrl, t=True, r=True, s=True)
			self.line_attr(input=share_ctrl, name='MT')
			switch_attr = self.new_attr(input=share_ctrl, name='Switch_IK_FK', min=0 , max=1, default=0)
			cmds.setAttr(switch_attr, e=1, keyable=True)


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
		if use_shared_loc:
			for main in main_joints:
				self.connect_rotate_order(input = main, object = '{}_Switch_Loc'.format(start))
	
		#create ik stretchy system
		if use_shared_loc:
			attrs_location = '{}_Switch_Loc'.format(start)
		else:
			attrs_location = share_ctrl
		ik_stretch = self.streatchy_ik(ik = ik_system[3], ik_ctrl= ik_system[0], top_ctrl = ik_system[2], pv_ctrl = ik_system[1], attrs_location=attrs_location, name = '', axis = twist_axis)
		ik_system.append(ik_stretch)

		self.put_inside_rig_container([reverse_node])

		print (main_joints, ik_joints, fk_joints, fk_system, ik_system, return_groups)
		return main_joints, ik_joints, fk_joints, fk_system, ik_system, return_groups

	#----------------------------------------------------------------------------------------------------------------

	def twist_fk_ik(self, start = '', mid = '', end = '', size = 1, color = setup['main_color'], mode = setup['ik_fk_method'], twist_axis = setup['twist_axis'], twist_amount = 6, use_shared_loc=True):
		"""
		Create an FK/IK chain with a switch for 3 joints and add twist functionality for a full limb module.

		Args:
			start (str): Name of the start joint. If not provided, the first selected joint will be used.
			mid (str): Name of the middle joint. If not provided, the second selected joint will be used.
			end (str): Name of the end joint. If not provided, the third selected joint will be used.
			size (float): Size of the controls.
			color (tuple): Color of the controls in RGB format.
			mode (str): IK/FK blending mode. Can be 'blend' or 'constraints'.
			twist_axis (str): Twist axis for the IK chain. Can be 'X', 'Y', or 'Z'.
			twist_amount (int): Number of twist joints to create for each section of the limb.

		Returns:
			dict: A dictionary containing the IK/FK system and the upper and lower twist information.

		Notes:
			- This function extends the functionality of the simple_fk_ik function by adding twist joints to the limb.
			- The twist joints allow for smoother deformation during twisting motions.
			- The upper_twist and lower_twist dictionaries contain information about the twist joints created.
			- The scale of the twist joints is connected to the scale of the corresponding main joints.

		Examples:
			# Example 1: Create a twist FK/IK chain with default settings
			result = twist_fk_ik()

			# Example 2: Create a twist FK/IK chain with custom joint names and size
			result = twist_fk_ik(start='arm_01_joint', mid='arm_02_joint', end='arm_03_joint', size=0.5)

			# Example 3: Create a twist FK/IK chain with custom color and twist axis
			result = twist_fk_ik(color=(1, 0.5, 0), twist_axis='Y', twist_amount=8)
		"""

		#create basic ik fk system
		ik_fk = self.simple_fk_ik(start = start, mid = mid, end = end, size = size, color = color, mode = mode, twist_axis = twist_axis, use_shared_loc=use_shared_loc)

		#add the twists
		main_joints = ik_fk[0]

		if main_joints[0].startswith(self.nc['right']):
			right_inverse = True
		else:
			right_inverse = False

		upper_twist= self.spline_twist(start=main_joints[0], end=main_joints[1], axis=self.setup['twist_axis'], amount=twist_amount, mode='up')
		lower_twist= self.spline_twist(start=main_joints[1], end=main_joints[2], axis=self.setup['twist_axis'], amount=twist_amount, mode='down')

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
		Select the start and end joints and create an IK/FK spline for a character's spine.

		Args:
			start (str): Name of the start joint. If not provided, the first selected joint will be used.
			end (str): Name of the end joint. If not provided, the last selected joint will be used.
			size (float): Size of the controls.
			name (str): Name prefix for the spline controls.
			twist_axis (str): Twist axis for the spline. Can be 'X', 'Y', or 'Z'.
			amount (int): Number of joints to create for the spline.

		Returns:
			tuple: A tuple containing lists of FK and IK controllers created for the spline.

		Notes:
			- If no start and end joint names are provided, the function assumes that the first and last selected joints are the start and end joints, respectively.
			- The main_joints list contains all the joints in the spline chain.
			- The spline_curve variable represents the spline curve created for the IK handle.
			- The effector_spline variable represents the IK spline effector.
			- The twist_ik_joints list contains the joints used for twisting the IK chain.
			- The ik_joints list contains the joints used for controlling the IK chain.
			- The ik_controllers list contains the IK controllers created.
			- The fk_controllers list contains the FK controllers created.
			- The skinCluster function is used to bind the IK joints to the spline curve.

		Examples:
			# Example 1: Create a spine IK/FK spline with default settings
			fk_controllers, ik_controllers = base_spline()

			# Example 2: Create a spine IK/FK spline with custom joint names and size
			fk_controllers, ik_controllers = base_spline(start='spine1_joint', end='spine3_joint', size=0.5)

			# Example 3: Create a spine IK/FK spline with a custom name prefix and twist axis
			fk_controllers, ik_controllers = base_spline(name='Character_Spine', twist_axis='Y', amount=8)
		"""

		if start == '':
			start = cmds.ls(sl=True)[0]
			end = cmds.ls(sl=True)[-1]

		print ('joints are: {} to {}'.format(start,end))
		
		#put name conventions to main chain and manage errors
		if str(start).endswith(self.nc['joint']):
			pass
		else: 
			start = cmds.rename(start, '{}{}'.format(start,self.nc['joint']))

		if str(end).endswith(self.nc['joint']):
			pass
		else: 
			end = cmds.rename(end, '{}{}'.format(end,self.nc['joint']))


		main_joints = [start]
		for jnt in cmds.listRelatives(start, allDescendents=True):
			
			if str(jnt).endswith(self.nc['joint']):
				pass
			else:
				jnt = cmds.rename(jnt, '{}{}'.format(jnt,self.nc['joint']))	
			
			main_joints.append(jnt)


		#create ik handle
		ikSpline = cmds.ikHandle(sj=start,
								 ee=end,
								 sol='ikSplineSolver',
								 n= main_joints[0] + self.nc['ik_spline'],
								 ccv=True,
								 pcv = False)

		spline_curve =  ikSpline[2]
		spline_curve = cmds.rename(spline_curve, start + self.nc['curve'])
		spline_curve = cmds.rebuildCurve(spline_curve, ch =  True,  rpo = True, rt = False, end =True, kr = False, kcp = False, kep = True , kt =False, s = amount-1, d = 3, tol = 0.01)

		effector_spline = cmds.rename(ikSpline[1],
									 start + self.nc['effector'])
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
			ik_controller = self.curve(type = self.setup['ik_ctrl'], size = size, custom_name = True, name = '{}_{}_IK{}'.format(name, num,self.nc['ctrl']))
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
			fk_controller = self.curve(type = self.setup['spine_fk_ctrl'], size = size, custom_name = True, name = '{}_{}_FK{}'.format(name, num,self.nc['ctrl']))
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
		   Create a mirrored group for a specified object or the currently selected object.

		   Args:
			   input (str): Name of the object to mirror. If not provided, the first selected object will be used.
			   world (bool): Specifies whether to mirror the group in world space or maintain the original position.

		   Returns:
			   str: Name of the mirrored group.

		   Notes:
			   - If no input object name is provided, the function assumes that the first selected object is the input.
			   - The mirror_grp variable represents the created mirrored group.
			   - If world is set to False, the original position of the input object is maintained.
			   - If world is set to True, the mirrored group is aligned to the world origin.
			   - The scaleX, scaleY, and scaleZ attributes of the mirror_grp are set to -1 to mirror the object.
			   - The rotateX attribute of the mirror_grp is set to 180 to rotate the mirrored object.

		   Examples:
			   # Example 1: Create a mirrored group for the selected object using the default settings
			   mirrored_group = mirror_group()

			   # Example 2: Create a mirrored group for a specific object with world mirroring disabled
			   mirrored_group = mirror_group(input='object1', world=False)

			   # Example 3: Create a mirrored group for the selected object with world mirroring enabled
			   mirrored_group = mirror_group(world=True)
		   """

		if input == '':
			input = cmds.ls(sl=True)[0]

		mirror_grp =cmds.group(em=True, n = '{}Mirror{}'.format(input,self.nc['group']))
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

	def basic_ribbon(self, start = '', end = '', divisions = 5, name = 'Ribbon', ctrl_type = 'circleY',size = 1, world_orient=False, start_end_joints=False):
		"""
		Create a basic ribbon rig between two objects using a plane and follicles.

		Args:
			start (str): Name of the start object. If not provided, the first selected object will be used.
			end (str): Name of the end object. If not provided, the second selected object will be used.
			divisions (int): Number of divisions or follicles along the ribbon.
			name (str): Name prefix for the ribbon elements.
			ctrl_type (str): Type of control shapes to create for the controllers.
			size (float): Size scale factor for the control shapes.
			world_orient (bool): Specifies whether to set the controllers' rotation to world orientation.

		Returns:
			dict: A dictionary containing the created ribbon elements.

		Notes:
			- If no start and end object names are provided, the function assumes that the first and second selected
			  objects are the start and end objects, respectively.
			- The surface variable represents the created NURBS plane between the start and end objects.
			- The follicles variable contains a list of the created follicles along the ribbon.
			- The fol_joints variable contains a list of joints created for binding to the follicles.
			- The ctrl_joints variable contains a list of joints created as control joints.
			- The controllers variable contains a list of created control shapes.
			- The controllers_grp variable represents the group containing the control shapes.
			- The created ribbon rig includes skinning the surface to the control joints and positioning the controllers.
			- If world_orient is set to True, the controllers' rotation is set to world orientation.
			- The function returns a dictionary with the created ribbon elements.

		Examples:
			# Example 1: Create a basic ribbon rig between the first and second selected objects using default settings
			ribbon_elements = basic_ribbon()

			# Example 2: Create a basic ribbon rig with custom settings
			ribbon_elements = basic_ribbon(start='object1', end='object2', divisions=7, name='MyRibbon',
										   ctrl_type='cube', size=2.0, world_orient=True)
		"""
		#this will create a plane between 2 objects and then create a ribbon rig for you

		if start ==  '':
			start = cmds.ls(sl=True)[0]
			end = cmds.ls(sl=True)[1]

		#create a nurbs etween and then create the follicles to it
		surface = self.nurbs_between(start=start,end=end)
		surface = cmds.rebuildSurface(surface, ch =False, dv=3,du=3, su=0,sv=divisions)
		surface = cmds.rename(surface, name + self.nc['joint'] +self.nc['nurb'])

		cmds.select(surface)
		mel.eval("createHair 1 {} 10 0 0 0 0 5 0 1 2 1".format(divisions))
		cmds.delete ('hairSystem1','pfxHair1','nucleus1')
		cmds.setAttr( surface +'.inheritsTransform', 0)
		
		fol_joints = []
		ctrl_joints = []
		for num in range (1, divisions+1):
			#delete crated curve and folicle rename
			fol = cmds.rename(cmds.listRelatives('curve' + str (num) , p=True), name + '_' +str(num) + self.nc['follicle'] )
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

		cmds.rename ('hairSystem1Follicles', name + self.nc['follicle']+self.nc['group'])
		
		follicles = cmds.ls(name + self.nc['follicle']+self.nc['group'], dag = True, type = 'follicle')

		#bind skin to nurbs
		cmds.select(ctrl_joints, surface)
		cmds.skinCluster(n = name.replace(self.nc['joint'], self.nc['skin_cluster']), toSelectedBones=True)
		cmds.select(surface)
		mel.eval('doPruneSkinClusterWeightsArgList 1 { "0.3" };')

		#controllers
		controllers =[]
		roots_grps = []
		for num, jnt in enumerate(ctrl_joints):
			cmds.select(jnt)
			ctrl = self.curve(type = ctrl_type, custom_name= True, name = str(jnt).replace(self.nc['joint'], self.nc['ctrl']), size = size * 0.75)
			if world_orient:
				print('World Orient in Simple Ribbon')
				cmds.setAttr('{}.rotateX'.format(ctrl),0)
				cmds.setAttr('{}.rotateY'.format(ctrl),0)
				cmds.setAttr('{}.rotateZ'.format(ctrl),0)
			grp = self.root_grp()[0]
			cmds.parentConstraint(ctrl , jnt, mo=True)
			#cmds.scaleConstraint(ctrl , jnt, mo=True)
			controllers.append(ctrl)
			roots_grps.append(grp)
			cmds.scaleConstraint(ctrl ,fol_joints[num], mo=True)
			if world_orient:
				cmds.delete(cmds.aimConstraint(start, grp, aimVector=(0, -1, 0), upVector=(0, 1, 0),
												   worldUpType='vector', mo=False))


		main_ctrl_grp = cmds.group(roots_grps, n = name + self.nc['ctrl'] + self.nc['group'])
		cmds.group(ctrl_joints, n = name + self.nc['joint'] + self.nc['group'])

		if start_end_joints:
			''

		return {'surface':surface, 
				'follicles':follicles,
				'fol_joints':fol_joints,
				'ctrl_joints':ctrl_joints,
				'controllers':controllers,
				'controllers_grp':main_ctrl_grp}

	
	#----------------------------------------------------------------------------------------------------------------

	def ribbon_between(self, start = '', end = '', divisions = 5, name = 'Ribbon', ctrl_type = 'circleY', size = 1, world_orient=False):
		"""
		Create a ribbon rig between two objects using a NURBS plane and follicles.

		Args:
			start (str): Name of the start object. If not provided, the first selected object will be used.
			end (str): Name of the end object. If not provided, the second selected object will be used.
			divisions (int): Number of divisions or follicles along the ribbon.
			name (str): Name prefix for the ribbon elements.
			ctrl_type (str): Type of control shapes to create for the controllers.
			size (float): Size scale factor for the control shapes.
			world_orient (bool): Specifies whether to set the controllers' rotation to world orientation.

		Returns:
			dict: A dictionary containing the created ribbon elements.

		Notes:
			- If no start and end object names are provided, the function assumes that the first and second selected
			  objects are the start and end objects, respectively.
			- The basic_ribbon function is used to create the initial ribbon rig.
			- The ctrl_surface variable represents a duplicate of the original surface to drive the control joints.
			- The function creates follicles on the ctrl_surface and parents them to the control joints.
			- The ctrl_fol_grp variable represents the group containing the follicles and control joints.
			- The ribbon rig is bound to the ctrl_surface using skinning.
			- The function returns a dictionary with the created ribbon elements, including the surface, follicles,
			  control joints, controllers, and their respective groups.

		Examples:
			# Example 1: Create a ribbon rig between the first and second selected objects using default settings
			ribbon_elements = ribbon_between()

			# Example 2: Create a ribbon rig with custom settings
			ribbon_elements = ribbon_between(start='object1', end='object2', divisions=7, name='MyRibbon',
											 ctrl_type='cube', size=2.0, world_orient=True)
		"""
		if start ==  '':
			start = cmds.ls(sl=True)[0]
			end = cmds.ls(sl=True)[1]
		
		#run main basic ribbon
		basic_ribbon = self.basic_ribbon(start = start, end = end, divisions = divisions, name = name, ctrl_type = ctrl_type, size = size, world_orient=world_orient)
		
		#create a new nursb to drive the ctrls
		ctrl_surface = cmds.duplicate(basic_ribbon['surface'], n = name + self.nc['ctrl'] +self.nc['nurb'])[0]
		ctrl_surface = cmds.rebuildSurface(ctrl_surface, ch =False, dv=1,du=1, su=1,sv=1)[0]

		cmds.select(ctrl_surface)
		mel.eval("createHair 1 {} 10 0 0 0 0 5 0 1 2 1".format(divisions))
		cmds.delete ('hairSystem1','pfxHair1','nucleus1')
		cmds.setAttr( ctrl_surface +'.inheritsTransform', 0)

		fol_joints = []
		for num in range (1, divisions+1):
			#delete crated curve and folicle rename
			fol = cmds.rename(cmds.listRelatives('curve' + str (num) , p=True), name + self.nc['ctrl'] + '_' +str(num) + self.nc['follicle'] )
			try:cmds.delete ('curve' + str (num) )
			except: pass

			#parent fol to ctrl offset grp
			cmds.parentConstraint(fol,cmds.listRelatives(basic_ribbon['controllers'][num-1], p=True), mo=True)
		
		ctrl_fol_grp = cmds.rename ('hairSystem1Follicles', name + self.nc['follicle']+self.nc['ctrl']+self.nc['group'])
		
		#bind skin to nurbs
		cmds.select(start,end, ctrl_surface)
		skin = cmds.skinCluster(n = name.replace(self.nc['joint'], self.nc['skin_cluster']), toSelectedBones=True, dr = 10)[0]
		cmds.skinPercent(skin, '{}.cv[0:1][1]'.format(ctrl_surface), transformValue=[(end, 1)])
		cmds.skinPercent(skin, '{}.cv[0:1][0]'.format(ctrl_surface), transformValue=[(start, 1)])

		cmds.group(basic_ribbon['surface'], ctrl_surface , n = name + self.nc['nurb'] + self.nc['group'])

		return {'surface':[basic_ribbon['surface'],ctrl_surface], 
				'follicles':basic_ribbon['follicles'],
				'fol_joints':basic_ribbon['fol_joints'],
				'ctrl_joints':basic_ribbon['ctrl_joints'],
				'controllers':basic_ribbon['controllers'],
				'controllers_grp':basic_ribbon['controllers_grp'],
				'ctrl_fol_grp': ctrl_fol_grp}


	#----------------------------------------------------------------------------------------------------------------

	def blend_between(self, ctrl = None, blends = '', attr_position = 'ctrl', attr_name = 'Blends'):
		"""
		Create blend groups and locators for controlling blends.

		Args:
			ctrl (str): Name of the main control.
			blends (str): Comma-separated string of blend names.
			attr_position (str): Position to create the blend attributes. Default is 'ctrl'.
			attr_name (str): Name of the blend attributes. Default is 'Blends'.

		Returns:
			None

		Notes:
			- The function creates a blend group and locators for each blend.
			- The blends are specified as a comma-separated string.
			- The blend group and locators are parented under a 'Blends' group in the 'misc' rig group.
			- If the blend group or 'Blends' group already exists, the function uses the existing groups.
			- The blend group is created as a child of the main control's blend group.
			- Locators are created for each blend and parent-constrained to the respective blend.
			- The blend attributes are created on the specified position (either the main control or a separate group).
			- The blend attributes are named based on the specified attribute name.
			- If no control or blends are provided, an error is raised.

		Examples:
			# Example 1: Create blend groups and locators for blends on the main control
			blend_between(ctrl='MainCtrl', blends='Blend1,Blend2,Blend3')

			# Example 2: Create blend groups and locators for blends on a separate group
			blend_between(ctrl='MainCtrl', blends='Blend1,Blend2,Blend3', attr_position='BlendsGroup')

			# Example 3: Create blend groups and locators with custom attribute name
			blend_between(ctrl='MainCtrl', blends='Blend1,Blend2,Blend3', attr_name='MyBlends')
		"""

		#inputs checks
		if not ctrl:
			cmds.error('No control assigned')

		if not blends:
			cmds.error('No blends assigned')

		if attr_position == 'ctrl':
			attr_position = ctrl

		#create main blends group for locators
		if not cmds.objExists('Blends' + self.nc['group']):
			blends_grp = cmds.group(n='Blends' + self.nc['group'], em=True)
		else:
			blends_grp = 'Blends' + self.nc['group']

		#get misc group and parent blends group in it
		misc_grp = self.setup['rig_groups']['misc'] + self.nc['group']
		if cmds.objExists(misc_grp):
			try:cmds.parent(blends_grp, misc_grp)
			except:pass

		#create blends gtroup for blends over main ctrl
		cmds.select(ctrl)
		if not cmds.objExists(ctrl + '_Blend' + self.nc['group']):
			blend_grp = self.root_grp(custom=True, custom_name='_Blend')
		else:
			blend_grp = ctrl + '_Blend' + self.nc['group']

		#blends stuffs
		blends = blends.split(',')
		blend_groups = []
		for blend in blends:
			print(blend)
			#creato locator in blends group for the parents
			blend_loc = cmds.spaceLocator(n = blend.replace(self.nc['joint'],self.nc['locator']).replace(self.nc['ctrl'],self.nc['locator']))
			self.match(blend_loc, blend)
			cmds.parentConstraint(blend, blend_loc, mo=False)
			cmds.parent(blend_loc, blends_grp)

			cmds.select(ctrl)

		cmds.select(ctrl)

	#----------------------------------------------------------------------------------------------------------------

	def parent_matrix(self, this=None, that=None, translate=True, rotate=True, scale=True, offset=True):
		"""
		Parent matrix between two objects, allowing control over translation, rotation, and scale.

		Args:
			this (str): Name of the source object.
			that (str): Name of the target object.
			translate (bool): Whether to connect translation. Default is True.
			rotate (bool): Whether to connect rotation. Default is True.
			scale (bool): Whether to connect scale. Default is True.
			offset (bool): Whether to create an offset matrix for the connection. Default is True.

		Returns:
			bool: True if successful.

		Notes:
			- If the 'this' and 'that' arguments are not provided, the function will use the selected objects.
			- If 'offset' is True, an offset matrix is created to preserve the relative transform between the objects.
			- The offset matrix is calculated by multiplying the world matrices of 'this' and 'that'.
			- The resulting matrix is stored in a network node and connected to the 'matrixIn' attribute of the multMatrix node.
			- The multMatrix node combines the world matrix of 'this' with the inverse of the parent matrix of 'that',
			  resulting in a new world matrix for 'that'.
			- The 'translate', 'rotate', and 'scale' arguments determine which attributes are connected.
			- The decomposeMatrix node extracts the translation, rotation, and scale values from the new world matrix.
			- If the 'offset' argument is True, the offset matrix is connected to the main multMatrix node.
			- The function also puts the created nodes inside the rig container.

		Examples:
			# Example 1: Parent matrix with translation, rotation, and scale
			parent_matrix(this='Source', that='Target', translate=True, rotate=True, scale=True, offset=True)

			# Example 2: Parent matrix with translation only
			parent_matrix(this='Source', that='Target', translate=True, rotate=False, scale=False, offset=False)
		"""
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

	#----------------------------------------------------------------------------------------------------------------

	def rivets_ctrls(self, geometry=None, selection_ctrls=None):
		"""
		Create a rivet system for the controllers to follow geometry on the rigs.

		Args:
			geometry (str): Name of the geometry to attach the controllers to.
			selection_ctrls (list): List of names of the controllers.

		Returns:
			None

		Example:
			import Mutant_Tools
			from Mutant_Tools.Utils.Rigging import main_mutant
			import imp
			imp.reload(Mutant_Tools.Utils.Rigging.main_mutant)
			mt = main_mutant.Mutant()
			# Select the controllers, then the geometry
			mt.rivets_ctrls()
		"""

		if not geometry and not selection_ctrls:
			sel = cmds.ls(sl=True)
			geometry = sel[-1]
			selection_ctrls = sel[:-1]
			print('Using Selection:', geometry, selection_ctrls)

		grp_rivets = cmds.group(n='{}_Rivets_Grp'.format(geometry), em=True)

		for ctrl in selection_ctrls:
			# create rivet #
			uvpin_node = cmds.createNode('uvPin', n='Rivet_{}_node'.format(ctrl))
			locator = cmds.spaceLocator(n='Rivet_{}_Loc'.format(ctrl))[0]
			cmds.parent(locator, grp_rivets)
			cmds.connectAttr('{}.worldMesh'.format(geometry), '{}.deformedGeometry'.format(uvpin_node), f=True)
			cmds.connectAttr('{}.outputMatrix[0]'.format(uvpin_node), '{}.offsetParentMatrix'.format(locator), f=True)

			# get position ctrl#
			closest_node = cmds.createNode('closestPointOnMesh', n='CPOM_{}'.format(ctrl))
			cmds.connectAttr('{}.worldMesh'.format(geometry), '{}.inMesh'.format(closest_node), f=True)
			pos_ctrl = cmds.xform(ctrl, ws=True, q=True, t=True)
			rot_ctrl = cmds.xform(ctrl, ws=True, q=True, ro=True)
			scale_ctrl = cmds.xform(ctrl, ws=True, q=True, s=True)

			cmds.setAttr('{}.inPositionX'.format(closest_node), pos_ctrl[0])
			cmds.setAttr('{}.inPositionY'.format(closest_node), pos_ctrl[1])
			cmds.setAttr('{}.inPositionZ'.format(closest_node), pos_ctrl[2])
			parameter_u = cmds.getAttr('{}.parameterU'.format(closest_node))
			parameter_v = cmds.getAttr('{}.parameterV'.format(closest_node))

			# set parameters uv to coordinate uvpin#
			cmds.setAttr('{}.coordinate[0].coordinateU'.format(uvpin_node), parameter_u)
			cmds.setAttr('{}.coordinate[0].coordinateV'.format(uvpin_node), parameter_v)
			cmds.delete(closest_node)

			# create grps offset#
			offset_ctrl = cmds.listRelatives(ctrl, p=True)[0]
			inverse_grp = cmds.group(n='{}_Inverse_Grp'.format(ctrl), em=True)
			point_grp = cmds.group(n='{}_Point_Grp'.format(ctrl))
			cmds.xform(point_grp, ws=True, t=pos_ctrl)
			cmds.xform(point_grp, ws=True, ro=rot_ctrl)
			cmds.xform(point_grp, ws=True, s=scale_ctrl)
			cmds.parent(point_grp, offset_ctrl)
			cmds.parent(ctrl, inverse_grp)

			# offset
			offset_value = cmds.createNode('transposeMatrix', n='{}_offset_tm'.format(ctrl))
			offset_mm = cmds.createNode('multMatrix', n='{}_Offset_Mm'.format(ctrl))
			cmds.connectAttr('{}.worldMatrix'.format(point_grp), '{}.matrixIn[0]'.format(offset_mm))
			cmds.connectAttr('{}.worldInverseMatrix'.format(locator), '{}.matrixIn[1]'.format(offset_mm))
			cmds.connectAttr('{}.matrixSum'.format(offset_mm), '{}.inputMatrix'.format(offset_value))
			cmds.disconnectAttr('{}.matrixSum'.format(offset_mm), '{}.inputMatrix'.format(offset_value))
			cmds.delete(offset_mm)

			# point constraint rivet to point_grp#
			point_mm = cmds.createNode('multMatrix', n='{}_PointConstraint_Mm'.format(ctrl))
			point_dcm = cmds.createNode('decomposeMatrix', n='{}_PointConstraint_Dcm'.format(ctrl))
			cmds.connectAttr('{}.inputMatrix'.format(offset_value), '{}.matrixIn[0]'.format(point_mm), f=True)
			cmds.connectAttr('{}.worldMatrix[0]'.format(locator), '{}.matrixIn[1]'.format(point_mm), f=True)
			cmds.connectAttr('{}.worldInverseMatrix[0]'.format(offset_ctrl), '{}.matrixIn[2]'.format(point_mm), f=True)
			cmds.connectAttr('{}.matrixSum'.format(point_mm), '{}.inputMatrix'.format(point_dcm), f=True)
			cmds.connectAttr('{}.outputTranslate'.format(point_dcm), '{}.translate'.format(point_grp), f=True)

			# cmds.pointConstraint(locator,point_grp,mo=True)

			inverse_dcm = cmds.createNode('decomposeMatrix', n='{}_Inverse_Dcm'.format(ctrl))
			cmds.connectAttr('{}.inverseMatrix'.format(ctrl), '{}.inputMatrix'.format(inverse_dcm))
			cmds.connectAttr('{}.outputTranslate'.format(inverse_dcm), '{}.translate'.format(inverse_grp))
			cmds.connectAttr('{}.outputRotate'.format(inverse_dcm), '{}.rotate'.format(inverse_grp))

			#disable and enable it
			self.put_inside_lod(nodes=[inverse_dcm, uvpin_node],  lod='High')


	def remove_rivets_ctrls(self, selection_ctrls=None):
		"""
		Remove the rivet system from the specified controllers.

		Args:
			selection_ctrls (list): List of names of the controllers.

		Returns:
			None

		Notes:
			If no controllers are specified, the function searches for controllers
			with names ending in "Ctrl_Inverse_Grp" and removes the rivet system
			from them.

		Examples:
			# Remove rivet system from selected controllers
			remove_rivets_ctrls()

			# Remove rivet system from specific controllers
			remove_rivets_ctrls(['Ctrl1', 'Ctrl2', 'Ctrl3'])
		"""
		if not selection_ctrls:
			sel = cmds.ls('*Ctrl_Inverse_Grp')
			selection_ctrls = []
			for ctrl in sel:
				print(ctrl)
				selection_ctrls.append(ctrl.replace('_Inverse_Grp', ''))
			print('Using Selection:', selection_ctrls)
		for ctrl in selection_ctrls:
			original_grp = ctrl.replace('Ctrl', 'Ctrl_Offset_Grp')
			inv_grp = ctrl.replace('Ctrl', 'Ctrl_Point_Grp')
			point_grp = ctrl.replace('Ctrl', 'Ctrl_Inverse_Grp')
			cmds.parent(ctrl, original_grp)
			cmds.delete(point_grp)

			rivet_loc = 'Rivet_{}_Loc'.format(ctrl)
			cmds.delete(rivet_loc)

			print('Removed rivet connection from {}'.format(ctrl))

	#----------------------------------------------------------------------------------------------------------------

	def curve_to_ribbon(self, curve, amount = 5, direction='V', size=1, color='lightBlue'):
		"""
		Create a ribbon system along the given curve.

		Args:
			curve (str): Name of the curve to create the ribbon on.
			amount (int): Number of follicles/hairs to generate along the curve.
			direction (str): Direction of the ribbon ('U' or 'V').
			size (float): Size of the main and tweak controls.
			color (str): Color of the controls.

		Returns:
			None

		Notes:
			- This function creates a ribbon system along the specified curve using follicles and joints.
			- The ribbon surface is created by converting the curve to a NURBS surface using the `bevel` command.
			- Follicles are then created on the ribbon surface, and joints and controls are attached to them.
			- The main controls are placed at the start, middle, and end of the ribbon.
			- The tweak controls are placed on each follicle.

		Examples:
			# Create a ribbon system on the selected curve with default settings
			curve_to_ribbon('curve1')

			# Create a ribbon system on a specific curve with custom settings
			curve_to_ribbon('curve2', amount=8, direction='U', size=1.5, color='red')
		"""

		joints_grp = cmds.group(em=True, n=curve + self.nc['joint'] + self.nc['group'])
		main_ctrls_grp = cmds.group(em=True, n=curve + self.nc['ctrl'] + '_Main' + self.nc['group'])
		tweeks_ctrls_grp = cmds.group(em=True, n=curve + self.nc['ctrl'] + '_Tweeks' + self.nc['group'])
		ctrls_grp = cmds.group(em=True, n=curve + self.nc['ctrl'] + self.nc['group'])
		cmds.parent(tweeks_ctrls_grp, ctrls_grp)
		cmds.parent(main_ctrls_grp, ctrls_grp)
		misc_group = cmds.group(em=True, n=curve + '_Misc' + self.nc['group'])

		# duplciate curve to convert to nurbs to add folls
		ribbon_surface = cmds.bevel(curve, ch=False, w=0, d=0.01, ed=0, ct=2, bst=1, n=curve + self.nc['nurb'], js=True)[
			0]
		ribbon_surface = cmds.rebuildSurface(ribbon_surface, ch=False, dv=3, du=3, su=0, sv=amount - 1)[0]

		cmds.parent(ribbon_surface, misc_group)
		cmds.parent(curve, misc_group)

		# Create follicles
		cmds.select(ribbon_surface)
		if direction == 'U':
			mel.eval("createHair {} 1 10 0 0 1 0 5 0 1 2 1;".format(amount))
		else:
			mel.eval("createHair 1 {} 10 0 0 1 0 5 0 1 2 1;".format(amount))

		cmds.delete('hairSystem1', 'pfxHair1', 'nucleus1')
		cmds.setAttr(ribbon_surface + '.inheritsTransform', 0)

		fol_grp = cmds.rename('hairSystem1Follicles', curve + self.nc['follicle'] + self.nc['group'])
		cmds.parent(fol_grp, misc_group)
		follicles = []
		for num, fol in enumerate(cmds.listRelatives(fol_grp, c=True)):
			gc = cmds.listRelatives(fol, c=True)
			cmds.delete(gc[-1])
			fol = cmds.rename(fol, curve + self.nc['follicle'] + '_' + str(num))
			follicles.append(fol)

		# add joints to follicles
		fol_joints = []
		tweek_ctrls = []

		for num, fol in enumerate(follicles):
			cmds.select(cl=True)
			fol_joint = cmds.joint(n='{}{}_{}{}'.format(curve, self.nc['follicle'], num, self.nc['joint']))
			fol_joints.append(fol_joint)
			cmds.delete(cmds.parentConstraint(fol, fol_joint))
			cmds.parent(fol_joint, fol)
			if direction == 'U':
				cmds.setAttr('{}.parameterV'.format(fol), 0)
			else:
				cmds.setAttr('{}.parameterU'.format(fol), 0)

			# ctrls
			ctrl = self.curve(input=fol_joint,
							type='sphere',
							rename=True,
							custom_name=True,
							name=fol_joint.replace(self.nc['joint'], '_Tweek' + self.nc['ctrl']),
							size=size)

			self.assign_color(color=color)
			root_grp = self.root_grp()[0]
			self.match(root_grp, fol_joint, r=True, t=True)
			cmds.parentConstraint(ctrl, fol_joint)
			cmds.scaleConstraint(ctrl, fol_joint)
			tweek_ctrls.append(ctrl)

			cmds.parentConstraint(fol, root_grp, mo=True)

			cmds.parent(root_grp, tweeks_ctrls_grp)

		# skin tweeks joints to curve
		cmds.skinCluster(fol_joints, curve, tsb=True)

		# Main ctrls
		ctrl_joints = []
		main_ctrls = []

		for num, fol in enumerate([follicles[0], follicles[len(follicles) // 2], follicles[-1]]):
			cmds.select(cl=True)
			ctrl_joint = cmds.joint(n='{}{}_{}{}'.format(curve, self.nc['follicle'], num, self.nc['joint_ctrl']))
			self.match(ctrl_joint, fol)
			ctrl_joints.append(ctrl_joint)

			# ctrls
			ctrl = self.curve(input=ctrl_joint,
							type='cube',
							rename=True,
							custom_name=True,
							name=ctrl_joint.replace(self.nc['joint_ctrl'], self.nc['ctrl']),
							size=size * 1.5)

			self.assign_color(color=color)
			root_grp = self.root_grp()[0]
			self.match(root_grp, ctrl_joint, r=True, t=True)
			cmds.parentConstraint(ctrl, ctrl_joint)
			cmds.scaleConstraint(ctrl, ctrl_joint)
			main_ctrls.append(ctrl)

			cmds.parent(root_grp, main_ctrls_grp)
			cmds.parent(ctrl_joint, joints_grp)

		cmds.skinCluster(ctrl_joints, ribbon_surface, tsb=True)

	#----------------------------------------------------------------------------------------------------------------


	def bend_and_squash_head(self, geo, parent_grp):
		"""
		Add squash and bend deformers to the specified geometry.

		Args:
		   geo (str): Name of the geometry to apply the deformers on.
		   parent_grp (str): Name of the parent group for the deformers.

		Returns:
		   None

		Notes:
		   - This function adds squash and bend deformers to the specified geometry.
		   - It creates control objects for controlling the deformers.
		   - The deformers are applied to the geometry using non-linear deformers.
		   - The control objects are parented to the specified parent group.
		   - The deformers are connected to the control objects to control their attributes.

		Examples:
		   # Apply bend and squash deformers to the geometry with default settings
		   bend_and_squash_head('head_geo', 'head_grp')

		   # Apply bend and squash deformers to the geometry with custom settings
		   bend_and_squash_head('head_geo', 'head_grp')
		"""

		nolinear_rot = [-90, 0, 0]
		nolinear_types = ["bend", "bend", "squash"]
		nolinear_hdls = ["SS_Head_Bend_Front_Back", "SS_Head_Bend_Side", "SS_Head"]
		nolinear_trans = ["z", "x", "y"]
		nolinear_fac = ["curvature", "curvature", "factor"]
		nolinear_mult = [15, 15, 0.15]

		def_grp = cmds.group(n="Pivot_Head_SS_Grp", em=True)
		off_def_grp = cmds.group(n="Pivot_Head_SS_Grp_Offset")

		ctrl_grp = cmds.group(n="SS_Head_Ctrl_Offset", em=True)

		ctrl = self.curve(type='sphere', name="SS_Head_Ctrl")

		cmds.parent(ctrl, ctrl_grp)
		cmds.matchTransform(ctrl_grp, parent_grp)

		for n_hdl, n_type, n_rot, n_trans, n_fac, n_mult in zip(nolinear_hdls, nolinear_types, nolinear_rot, nolinear_trans,
																nolinear_fac, nolinear_mult):
			cmds.select(geo)

			dag, hdl = cmds.nonLinear(type=n_type, lowBound=0)

			hdl = cmds.rename(hdl, n_hdl)
			dag = cmds.rename(dag, "{0}_Deformer".format(n_hdl))
			cmds.setAttr("{0}.ry".format(hdl), n_rot)

			cmds.parent(hdl, def_grp)

			cmds.matchTransform(hdl, def_grp, pos=True, rot=False)

			nolinear_mdl = cmds.createNode("multDoubleLinear", n="{0}_multD".format(hdl))
			cmds.setAttr("{0}.input2".format(nolinear_mdl), n_mult)

			cmds.connectAttr("{0}.t{1}".format(ctrl, n_trans), "{0}.input1".format(nolinear_mdl))
			cmds.connectAttr("{0}.output".format(nolinear_mdl), "{0}.{1}".format(dag, n_fac))

		cmds.parentConstraint(parent_grp, off_def_grp, mo=False)
		cmds.parent(ctrl_grp, parent_grp)
		cmds.setAttr("{0}.ty".format(ctrl_grp), 7)

		self.hide_attr(input=ctrl,r=True, s=True, rotate_order=True)

		cmds.scaleConstraint('Skull_Upr_Ctrl', 'Pivot_Head_SS_Grp_Offset', mo=True)

	#----------------------------------------------------------------------------------------------------------------

	def bend_and_squash(self, name = 'SnS', geo=None, parent_grp=None):
		"""
		Add squash and bend deformations to objects.

		Args:
			name (str): Name prefix for the deformers and controls.
			geo (str): Name of the geometry to apply the deformations to. If None, the currently selected object will be used.
			parent_grp (str): Name of the parent group. If None, a new locator will be created as the parent group.

		Returns:
			tuple: Tuple containing the names of the offset deformation group and control group.

		Notes:
			- This function adds squash and bend deformations to the specified geometry.
			- It creates control handles and deformers for each type of deformation.
			- The control handles are connected to the deformers, and the deformers are connected to the geometry.
			- The function sets up constraints and parenting for the control handles and deformers.
			- The function returns the names of the offset deformation group and control group.

		Example:
			# Apply squash and bend deformations to the 'head_geo' with a parent group 'head_grp'
			off_def_grp, ctrl_grp = bend_and_squash('head', 'head_geo', 'head_grp')
		"""

		if not geo:
			geo = cmds.ls(sl=True)[0]
		if not parent_grp:
			parent_grp = cmds.spaceLocator(n=geo+'_SnS_Parent'+self.nc['locator'])[0]

		nolinear_rot = [-90, 0, 0]
		nolinear_types = ["bend", "bend", "squash"]
		nolinear_hdls = ["{}_Bend_Front_Back".format(name), "{}_Bend_Side".format(name), "SS_{}".format(name)]
		nolinear_trans = ["z", "x", "y"]
		nolinear_fac = ["curvature", "curvature", "factor"]
		nolinear_mult = [15, 15, 0.15]

		def_grp = cmds.group(n="Pivot_{}_Grp".format(name), em=True)
		off_def_grp = cmds.group(n="Pivot_{}_Grp_Offset".format(name))

		ctrl_grp = cmds.group(n="{}_Ctrl_Offset".format(name), em=True)

		ctrl = self.curve(type='sphere', name="{}_Ctrl".format(name))

		cmds.parent(ctrl, ctrl_grp)
		cmds.matchTransform(ctrl_grp, parent_grp)

		for n_hdl, n_type, n_rot, n_trans, n_fac, n_mult in zip(nolinear_hdls, nolinear_types, nolinear_rot, nolinear_trans,
																nolinear_fac, nolinear_mult):
			cmds.select(geo)

			dag, hdl = cmds.nonLinear(type=n_type, lowBound=0)

			hdl = cmds.rename(hdl, n_hdl)
			dag = cmds.rename(dag, "{0}_Deformer".format(n_hdl))
			cmds.setAttr("{0}.ry".format(hdl), n_rot)

			cmds.parent(hdl, def_grp)

			cmds.matchTransform(hdl, def_grp, pos=True, rot=False)

			nolinear_mdl = cmds.createNode("multDoubleLinear", n="{0}_multD".format(hdl))
			cmds.setAttr("{0}.input2".format(nolinear_mdl), n_mult)

			cmds.connectAttr("{0}.t{1}".format(ctrl, n_trans), "{0}.input1".format(nolinear_mdl))
			cmds.connectAttr("{0}.output".format(nolinear_mdl), "{0}.{1}".format(dag, n_fac))

		cmds.parentConstraint(parent_grp, off_def_grp, mo=False)
		cmds.delete(cmds.parentConstraint(parent_grp, ctrl_grp, mo=False))
		cmds.setAttr("{0}.ty".format(ctrl_grp), 7)
		cmds.parentConstraint(parent_grp, ctrl_grp, mo=True)

		self.hide_attr(input=ctrl,r=True, s=True, rotate_order=True)

		return off_def_grp, ctrl_grp

	#----------------------------------------------------------------------------------------------------------------

	def create_lods_containers(self, lods = ['High']):
		"""
		Create LOD (Level of Detail) containers.

		Args:
			lods (list): List of LOD names.

		Returns:
			list: List of LOD nodes.

		Notes:
			- This function creates LOD containers for the specified LODs.
			- Each container is named 'Mutant_{lod}'.
			- The function checks if the container already exists before creating it.
			- The function sets the 'iconName' attribute of each container to a specified icon path.
			- If a 'Miscellaneous_Grp' exists, the containers are parented under it.
			- The function returns a list of the created LOD nodes.

		Example:
			# Create LOD containers for 'High' and 'Medium' LODs
			lods_created = create_lods_containers(['High', 'Medium'])
		"""

		lods_created = []

		for lod in lods:
			cmds.select(cl=True)
			if not cmds.objExists('Mutant_{}'.format(lod)):
				mutant_lod = cmds.container(name='Mutant_{}'.format(lod), type='dagContainer')
				print('LOD Created', lod)
			else:
				mutant_lod = 'Mutant_{}'.format(lod)
				print('LOD Exists', lod)

			lods_created.append(mutant_lod)

			icon_path = os.path.join(FOLDER, 'Icons', 'LogoBlack03')
			cmds.setAttr('{}.iconName'.format(mutant_lod), icon_path, type='string')

			if cmds.objExists('Miscellaneous_Grp'):
				cmds.parent(mutant_lod, 'Miscellaneous_Grp')

		return lods_created

	#----------------------------------------------------------------------------------------------------------------

	def put_inside_lod(self,nodes=[],  lod='High'):
		"""
		Put nodes inside an LOD (Level of Detail) container.

		Args:
			nodes (list): List of nodes to put inside the container.
			lod (str): LOD name.

		Returns:
			str: LOD container name.

		Notes:
			- This function puts the specified nodes inside the LOD container.
			- If the LOD container doesn't exist, it creates it using the 'create_lods_containers' function.
			- The function expects a list of nodes to be provided.
			- If 'nodes' != a list, it converts it to a list.
			- The function adds each node to the LOD container using the 'container' command.
			- The function returns the name of the LOD container.

		Example:
			# Put selected nodes inside the 'High' LOD container
			lod_container = put_inside_lod(cmds.ls(sl=True), 'High')
		"""

		if not nodes:
			cmds.error('We need nodes to put inside the container')

		lod_container = 'Mutant_{}'.format(lod)

		if not cmds.objExists(lod_container):
			self.create_lods_containers(lods=[lod])

		if type(nodes) != 'list':
			nodes = [nodes]

		for node in nodes:
			cmds.container(lod_container, edit=True, addNode=node)

		return lod_container

	#----------------------------------------------------------------------------------------------------------------

	def create_wire_system(self, geo, curve, name='Wire', dropoff=100, axis='Y', scale=1):
		"""
		Creates a wire system that can be used to control the shape of a mesh.

		Args:
			geo (str): The name of the mesh that the wire system will be applied to.
			curve (str): The name of the curve that will be used to control the wire system.
			name (str): The prefix for the names of the created objects. Defaults to 'Wire'.
			dropoff (int): The distance from the curve that the wire system will affect the mesh. Defaults to 100.
			axis (str): The axis that the wire system will be aligned to. Defaults to 'Y'.
			scale (float): The scale of the created objects. Defaults to 1.

		Returns:
			dict: A dictionary containing the created objects. The keys are:
				'main_ctrl': The main control object for the wire system.
				'ctrls': A list of control objects for the wire system.
				'ctrsl_grp': The group containing the control objects for the wire system.
				'joints': A list of joints that are used to control the wire system.
				'joints_grp': The group containing the joints for the wire system.
				'wireBase': The base object for the wire system.

		Notes:
			- The function creates a wire deformer using the specified geometry and curve.
			- It sets the dropoff distance for the wire deformer.
			- It creates control objects for each CV (control vertex) of the curve and assigns them to joints.
			- The control objects are parented under a main control object that acts as the root of the wire system.
			- The function creates a skin cluster to bind the joints to the curve.
			- It returns a dictionary containing the created objects for further manipulation.

		Example:
			# Create a wire system with a mesh and a curve
			wire_system = create_wire_system('mesh1', 'curve1')
		"""

		cmds.makeIdentity(curve, apply=True, t=1, r=1, s=1, n=0, pn=1)

		wireDef = cmds.wire(geo, w=curve, foc=True)
		wireDef = wireDef[0]
		cmds.setAttr('{}.dropoffDistance[0]'.format(wireDef), dropoff)

		bindJnt = []
		crvCVs = cmds.ls(curve + '.cv[0:]', fl=1)

		crls_grp = cmds.group(n=name + self.nc['ctrl'] + '_Wire' + self.nc['group'], em=True)
		joints_mover_grp = cmds.group(n=name + self.nc['joint'] + '_MoverWire' + self.nc['group'], em=True)
		joints_grp = cmds.group(n=name + self.nc['joint'] + '_Wire' + self.nc['group'])
		self.match(joints_grp, curve)

		#Main Ctrl
		cmds.select(joints_mover_grp)
		main_ctrl = ctrl = self.curve(input=joints_mover_grp,
							type='circle{}'.format(axis),
							rename=True,
							custom_name=True,
							name=name + '_Main_' + self.nc['ctrl'],
							size=scale*4)
		main_root_grp = self.root_grp()[0]
		self.assign_color(color='lightBlue')
		cmds.connectAttr(main_ctrl + '.translate', joints_mover_grp + '.translate')
		cmds.connectAttr(main_ctrl + '.rotate', joints_mover_grp + '.rotate')
		cmds.connectAttr(main_ctrl + '.scale', joints_mover_grp + '.scale')
		cmds.parent(main_root_grp, crls_grp)

		#Create System
		ctrls = []
		rot=45
		for i, cv in enumerate(crvCVs):
			cmds.select(cl=True)
			joint = cmds.joint(n=name + '_' + str(i) + self.nc['joint'])
			cmds.setAttr('{}.rotate{}'.format(joint, axis), rot)
			offset_joint = self.root_grp()[0]

			pos = cmds.xform(cv, q=1, ws=1, t=1)
			cmds.xform(offset_joint, ws=1, t=pos)

			ctrl = self.curve(input=joint,
							type='sphere',
							rename=True,
							custom_name=True,
							name=name + '_' + str(i) + self.nc['ctrl'],
							size=scale*2)
			cmds.setAttr('{}.rotate{}'.format(ctrl, axis), rot)
			ctrls.append(ctrl)
			self.assign_color(color='lightBlue')
			root_grp = self.root_grp()[0]
			cmds.parent(root_grp, main_ctrl)
			self.match(root_grp, joint, r=True, t=True)
			self.hide_attr(input=ctrl, t=False, r=True, s=True, v=False, rotate_order=True)
			cmds.connectAttr(ctrl + '.translate', joint + '.translate')
			cmds.connectAttr(ctrl + '.rotate', joint + '.rotate')
			cmds.connectAttr(ctrl + '.scale', joint + '.scale')
			bindJnt.append(joint)
			cmds.parent(offset_joint, joints_mover_grp)

			rot=rot+45

		cmds.skinCluster(bindJnt, curve)


		return {'main_ctrl' : main_ctrl, 'ctrls': ctrls, 'ctrsl_grp': crls_grp, 'joints': bindJnt, 'joints_grp': joints_grp,
				'wireBase': curve + 'BaseWire'}

	#----------------------------------------------------------------------------------------------------------------

	def get_distance_between(self, start_node, end_node):
		"""
		Calculates the distance between two nodes in 3D space.

		Args:
			start_node (str): The name of the starting node.
			end_node (str): The name of the ending node.

		Returns:
			float: The distance between the two nodes.

		Notes:
			- The function uses the xform command to get the world space translation values of the nodes.
			- It creates MVector objects from the translation values.
			- It subtracts the vectors to get the vector between the two nodes.
			- The length of the vector represents the distance between the nodes.
			- The function returns the distance as a float value.

		Example:
			# Calculate the distance between two nodes
			distance = get_distance_between('node1', 'node2')
		"""

		t1, t2 = cmds.xform(start_node, t=1, q=1, ws=True), cmds.xform(end_node, t=1, q=1, ws=True)
		v1, v2 = om.MVector(t1), om.MVector(t2)
		v = v2 - v1

		return om.MVector(v2 - v1).length()

	#----------------------------------------------------------------------------------------------------------------

	def proxy_this_attrs(self,attrs_from=None, attrs_to=None, attrs_to_proxy=[], line_at_end=True, line_at_start=True):
		"""
		Proxies attributes from one object to another.

		Args:
			attrs_from (str): The source object from which to copy attributes.
			attrs_to (str): The destination object to which the attributes will be copied.
			attrs_to_proxy (list): A list of attributes to proxy from the source object to the destination object.
			line_at_end (bool): Whether to add a separator line attribute at the end. Defaults to True.
			line_at_start (bool): Whether to add a separator line attribute at the start. Defaults to True.

		Notes:
			- The function checks if the necessary arguments are provided.
			- It retrieves the user-defined attributes (UDAs) from the source object.
			- For each attribute, it checks if it is in the list of attributes to proxy.
			- If the attribute != in the list, it skips to the next attribute.
			- It gets the attribute type using `cmds.getAttr`.
			- If the attribute type is 'double', it adds a double attribute to the destination object and proxies the attribute value.
			- If the attribute type is 'enum', it adds an enum attribute to the destination object and proxies the attribute value.
			- The minimum and maximum values are also copied for double attributes.
			- If `line_at_end` is True, a separator line attribute is added at the end.

		Example:
			# Proxy selected attributes from one object to another
			mt.proxy_this_attrs(attrs_from='|L_Hip_Jnt_Switch_Loc', attrs_to='L_Ankle_Ik_Ctrl', attrs_to_proxy=['HipBend', 'Switch_IK_FK'])
		"""

		if not attrs_to_proxy:
			cmds.error('We need a list of attrs to copy to')

		if not attrs_from:
			cmds.error('We need a source object')

		if not attrs_to:
			cmds.error('We need a destination object')

		# Get aatrs from and apply to new
		attrs = cmds.listAttr(attrs_from, ud=True)
		print('Attrs: {}'.format(attrs))
		if line_at_start:
			self.line_attr(input=attrs_to, name='Proxy')
		for attr in attrs:

			if attr not in attrs_to_proxy:
				continue

			cmds.select(attrs_from)
			print(attrs_from, attr)
			if '___' in attr:
				continue

			print('{}.{}'.format(attrs_from, attr))

			try:
				attr_type = cmds.getAttr('{}.{}'.format(attrs_from, attr), type=True)
			except:
				attr_type = None

			if not attr_type:
				continue

			if attr_type == 'double':
				cmds.addAttr(attrs_to, ln=attr, proxy="{}.{}".format(attrs_from, attr), at="double",
							 min=cmds.attributeQuery(attr, node=attrs_from, min=True)[0],
							 max=cmds.attributeQuery(attr, node=attrs_from, max=True)[0],
							 )

			elif attr_type == 'double':
				cmds.addAttr(attrs_to, ln=attr, proxy="{}.{}".format(attrs_from, attr), at="double",
							 min=cmds.attributeQuery(attr, node=attrs_from, min=True)[0],
							 max=cmds.attributeQuery(attr, node=attrs_from, max=True)[0],
							 )

			elif attr_type == 'enum':
				if 'RotateOrder' in attr:
					continue
				cmds.addAttr(attrs_to, ln=attr, proxy="{}.{}".format(attrs_from, attr), at="enum",
							 en=cmds.attributeQuery(attr, node=attrs_from, listEnum=True)[0],
							 )

		if line_at_end:
			self.line_attr(input=attrs_to, name='Attrs')

	#----------------------------------------------------------------------------------------------------------------

	def dinamic_pivot(self, input, size=1):
		"""
		Creates a dynamic pivot point for an object in Maya.

		Parameters:
			input (str): The name of the object that the rotate pivot will be connected to.
			size (float): The size of the created cube curve. Defaults to 1.

		Returns:
			str: The name of the created cube curve.

		Notes:
			- This function creates a cube curve and renames it with a specific naming convention.
			- It creates a group object and moves/orientates the group object to match the position and orientation of the curve.
			- The curve is parented to the group object.
			- It connects the translate attribute of the curve to the rotate pivot of the input object.

		Example:
			dinamic_pivot("pCube1")
		"""

		ctrl = self.curve(input='', type='cube', rename=True, custom_name=True, name='Dinamic_Pivot_{}'.format(input),
						size=size)
		cmds.select(cl=True)
		grp_ctrl = cmds.group(n='{}{}'.format(ctrl, self.nc['group']), em=True)
		get_position = cmds.xform(ctrl, ws=True, q=True, t=True)
		get_orient = cmds.xform(ctrl, ws=True, q=True, ro=True)
		cmds.xform(grp_ctrl, ws=True, t=get_position)
		cmds.xform(grp_ctrl, ws=True, ro=get_orient)
		cmds.parent(ctrl, grp_ctrl)

		cmds.connectAttr('{}.translate'.format(ctrl), '{}.rotatePivot'.format(input))

		return ctrl

	#----------------------------------------------------------------------------------------------------------------

	def create_auto_rotate_fk(self, fk_root_ctrl=None, fk_root_ctrl_offset=None, size=1):
		"""
		Creates an auto-rotate FK setup for a chain of controls in Maya.

		Parameters:
			fk_root_ctrl (str): The name of the root FK control.
			fk_root_ctrl_offset (str): The name of the offset group for the root FK control.

		Returns:
			None

		Notes:
			- This function assumes that the chain of controls is connected through parent relationships.
			- It creates a sphere curve as the rotator control.
			- It positions and orients the rotator control's offset group to match the last control in the chain.
			- It parents the rotator control's offset group under the root FK control's offset group.
			- It creates a group for each control in the chain and positions/orients it to match the control.
			- It parents each control under its corresponding group.
			- It connects the rotation attributes of the rotator control to the rotation attributes of each group in the chain.

		Example:
			# Without attributes
			create_auto_rotate_fk("FK_Root_Ctrl", "FK_Root_Ctrl_Offset")

			# With attributes
			create_auto_rotate_fk("FK_Root_Ctrl", "FK_Root_Ctrl_Offset")
		"""
		
		chain_ctrls = [cmds.listRelatives(ctrl, p=1)[0] for ctrl in cmds.listRelatives(fk_root_ctrl_offset, ad=1, type='nurbsCurve')]
		
		ctrl_autorotate = self.curve(input = '', type = 'sphere', rename=True, custom_name = True, name = '{}{}'.format(fk_root_ctrl.replace(nc['ctrl'], '_Rotator'), nc['ctrl']), size=4)
		ctrl_autorotate_offset = self.root_grp(ctrl_autorotate, autoRoot=True)[0]

		cmds.parent(ctrl_autorotate_offset, fk_root_ctrl_offset)

		for ctrl in chain_ctrls:
			grp = self.root_grp(ctrl, custom=True, custom_name='AutoRotate', autoRoot=True)[-1]
			cmds.connectAttr('{}.r'.format(ctrl_autorotate),'{}.r'.format(grp),f=True)

	#----------------------------------------------------------------------------------------------------------------

	def create_mid_ribbons(self, name, first_joint, last_joint, twist_joints, aim, twist_amount, ctrl_size, sec_color, switch_locator):
		"""
		Creates mid ribbons with bendy functionality.

		Args:
			name (str): Name prefix for the ribbons and controls.
			first_joint (str): Name of the first joint in the chain.
			last_joint (str): Name of the last joint in the chain.
			twist_joints (list): List of joint names to be included in the twist deformation.
			aim (str): Aim direction for the ribbon controls ('X', 'Y', or 'Z').
			twist_amount (int): Number of subdivisions/twist joints on the ribbon.
			ctrl_size (float): Size of the control objects.
			sec_color (str): Secondary color for the control objects.
			switch_locator (str): Name of the switch locator object.

		Notes:
			- This method creates mid ribbons with bendy functionality by creating NURBS planes and follicles.
			- The ribbons are controlled by twist joints and IK handles.
			- The method also creates control objects for tweaking the ribbons and handles for pinning the ribbons.

		Examples:
			# Create mid ribbons with bendy functionality
			create_mid_ribbons('arm', 'shoulder', 'wrist', ['elbow1', 'elbow2', 'elbow3'], 'X', 5, 1.0, 'blue', 'switch_locator')
		"""

		if not cmds.attributeQuery('BendyMain', n=switch_locator, exists=True):
			self.line_attr(input=switch_locator, name='Bendy_Vis')
			ribbon_first_vis_attr = self.new_enum(input=switch_locator, name='BendyMain', enums='Hide:Show', keyable=False)
			ribbon_second_vis_attr = self.new_enum(input=switch_locator, name='BendyOffsets', enums='Hide:Show',
												 keyable=False)
			ribbon_ends_vis_attr = self.new_enum(input=switch_locator, name='BendyEnds', enums='Hide:Show', keyable=False)
			ribbon_third_vis_attr = self.new_enum(input=switch_locator, name='BendyTweeks', enums='Hide:Show', keyable=False)

		else:
			ribbon_first_vis_attr = switch_locator+'.BendyMain'
			ribbon_second_vis_attr = switch_locator + '.BendyOffsets'
			ribbon_ends_vis_attr = switch_locator + '.BendyEnds'
			ribbon_third_vis_attr = switch_locator + '.BendyTweeks'

		# for dev set to 0 at the end
		cmds.setAttr(ribbon_first_vis_attr, 1)
		cmds.setAttr(ribbon_second_vis_attr, 0)
		cmds.setAttr(ribbon_third_vis_attr, 0)
		cmds.setAttr(ribbon_ends_vis_attr, 0)

		# main tweek Ribbons
		ribbon_limb_nurb = cmds.nurbsPlane(ch=1, d=1, v=1, p=(0, 0, 0), u=1, w=1, ax=(0, 0, 1), lr=1,
										   n=name + 'Ribbon' + self.nc['nurb'])
		cluster01 = cmds.cluster(ribbon_limb_nurb[0] + '.cv[0][0:1]')
		cluster02 = cmds.cluster(ribbon_limb_nurb[0] + '.cv[1][0:1]')
		cmds.setAttr(str(ribbon_limb_nurb[0]) + '.visibility', 0)
		cmds.delete(cmds.parentConstraint(first_joint, cluster01, mo=False))
		cmds.delete(cmds.parentConstraint(last_joint, cluster02, mo=False))
		cmds.delete(ribbon_limb_nurb, ch=True)
		cmds.rebuildSurface(ribbon_limb_nurb[0], rt=0, kc=0, fr=0, end=1, sv=1, su=twist_amount, kr=0,
							dir=2, kcp=0,
							tol=0.01, dv=1, du=3, rpo=1)

		# Create follicles
		cmds.select(ribbon_limb_nurb[0])
		mel.eval("createHair {} 1 10 0 0 0 0 5 0 1 2 1;".format(twist_amount))

		cmds.delete('hairSystem1', 'pfxHair1', 'nucleus1')
		cmds.setAttr(ribbon_limb_nurb[0] + '.inheritsTransform', 0)

		for C in range(1, twist_amount + 1):
			cmds.delete('curve' + str(C))
		fol_grp = cmds.rename('hairSystem1Follicles', name + self.nc['follicle'] + self.nc['group'])

		follicles = cmds.ls(name + self.nc['follicle'] + self.nc['group'], dag=True, type='follicle')
		fol_joints = []
		cmds.setAttr(follicles[0] + '.parameterU', 0)

		for num, i in enumerate(follicles):
			cmds.select(i)
			fol_new_name = cmds.rename(cmds.listRelatives(i, p=True), name + '_' + str(num) + self.nc['follicle'])
			fol_jnt = cmds.joint(n=name + '_' + str(num) + self.nc['joint'])
			fol_joints.append(fol_jnt)
			# Normalize Follicles
			cmds.connectAttr('Global_Ctrl.scale', fol_new_name + '.scale')
		# Bind twist to bendy surfaces
		cmds.skinCluster(twist_joints[:-1], ribbon_limb_nurb[0], sm=0, bm=1, tsb=True)

		tweks_ribbon_ctrl_grp = cmds.group(em=True, n=name + '_Ribbons' + self.nc['ctrl'] + self.nc['group'])
		ribbon_ctrls = []
		for fol_jnt in fol_joints:
			ctrl = self.curve(input=fol_jnt, type='square',
							rename=True,
							custom_name=True, name=fol_jnt.replace(self.nc['joint'], self.nc['ctrl']),
							size=ctrl_size / 3,
							)
			self.shape_with_attr(input='', obj_name=name + '_Switch', attr_name='')
			self.assign_color(ctrl, sec_color)
			root, auto = self.root_grp(input=ctrl, autoRoot=True)
			cmds.parentConstraint(cmds.listRelatives(fol_jnt, p=True)[0], root, mo=False)
			cmds.parentConstraint(ctrl, fol_jnt)
			cmds.parent(root, tweks_ribbon_ctrl_grp)

			cmds.connectAttr(ribbon_third_vis_attr, '{}.v'.format(cmds.listRelatives(ctrl, shapes=True)[0]))
			ribbon_ctrls.append(ctrl)
		# --------------------------------------------------------------------------------
		# --------------------------------------------------------------------------------
		# --------------------------------------------------------------------------------

		# Bendy Ribbons
		# create ribbon Plane
		middle_limb_nurb = cmds.nurbsPlane(ch=1, d=1, v=1, p=(0, 0, 0), u=1, w=1, ax=(0, 0, 1), lr=1,
										   n=name + 'Bendy' + self.nc['nurb'])
		cluster01 = cmds.cluster(middle_limb_nurb[0] + '.cv[0][0:1]')
		cluster02 = cmds.cluster(middle_limb_nurb[0] + '.cv[1][0:1]')
		# cmds.setAttr(str(middle_limb_nurb[0]) + '.visibility', 0)
		cmds.delete(cmds.parentConstraint(first_joint, cluster01, mo=False))
		cmds.delete(cmds.parentConstraint(last_joint, cluster02, mo=False))
		cmds.delete(middle_limb_nurb, ch=True)
		# cmds.rebuildSurface(middle_limb_nurb[0], rt=0, kc=0, fr=0, end=1, sv=1, su=2, kr=0,
		cmds.rebuildSurface(middle_limb_nurb[0], rt=0, kc=0, fr=0, end=1, sv=1, su=len(twist_joints) + 1, kr=0,
							dir=2, kcp=0,
							tol=0.01, dv=1, du=3, rpo=1)
		# cmds.skinCluster(first_joint, middle_limb_nurb[0], sm=0, bm=1, tsb=True)

		# create joints for iks
		middle_joints = self.joints_middle(start=first_joint, end=last_joint, axis=self.setup['twist_axis'], amount=4,
										 name='BendyMid')
		for jnt in middle_joints:
			try:
				cmds.parent(jnt, w=True)
			except:
				pass

		cmds.parent(middle_joints[1], middle_joints[0])
		cmds.parent(middle_joints[2], middle_joints[3])

		# put middle joints in middle
		cmds.delete(cmds.parentConstraint(first_joint, last_joint, middle_joints[1], mo=False))
		cmds.delete(cmds.parentConstraint(first_joint, last_joint, middle_joints[2], mo=False))

		# create iks (now they are not IK anymore)
		ik_bendy_grp = cmds.group(middle_joints[0], middle_joints[3],
								  n='{}_BendyIK{}'.format(name, self.nc['group']))

		# cmds.skinCluster(middle_joints, middle_limb_nurb[0], sm=0, bm=1, tsb=True)
		# cmds.skinCluster(twist_joints, middle_limb_nurb[0], sm=0, bm=1, tsb=True)
		# put this under bs

		# Pin IK Bendys
		top_ik_bendy_ctrl = self.curve(input=first_joint,
									 type='pin_cube',
									 rename=True,
									 custom_name=True,
									 name=name.replace(self.nc['joint'], '_Top_Handle' + self.nc['ctrl']),
									 size=ctrl_size / 3,
									 )
		top_ik_bendy_root = self.root_grp()
		self.assign_color(top_ik_bendy_ctrl, sec_color)
		cmds.delete(cmds.parentConstraint(first_joint, top_ik_bendy_root))
		self.shape_with_attr(input=top_ik_bendy_ctrl, obj_name=name + '_Switch', attr_name='')
		self.hide_attr(input=top_ik_bendy_ctrl, t=True, r=False, s=True, v=True)

		bottom_ik_bendy_ctrl = self.curve(input=last_joint,
										type='pin_cube',
										rename=True,
										custom_name=True,
										name=name.replace(self.nc['joint'], '_Bottom_Handle' + self.nc['ctrl']),
										size=ctrl_size / 3,
										)
		self.assign_color(bottom_ik_bendy_ctrl, sec_color)
		bottom_ik_bendy_root = self.root_grp()
		cmds.delete(cmds.parentConstraint(last_joint, bottom_ik_bendy_root))
		self.shape_with_attr(input=bottom_ik_bendy_ctrl, obj_name=name + '_Switch', attr_name='')
		self.hide_attr(input=bottom_ik_bendy_ctrl, t=True, r=False, s=True, v=True)

		# Aim to each other
		# cmds.delete(cmds.aimConstraint(top_ik_bendy_ctrl, bottom_ik_bendy_root, aimVector =(0, 1, 0), upVector = (0,0,-1)))
		# cmds.delete(cmds.aimConstraint(bottom_ik_bendy_ctrl, top_ik_bendy_root, aimVector =(0, 1, 0), upVector = (0,0,-1)))
		cmds.rotate(0, 0, 90 - cmds.getAttr('{}.jointOrientZ'.format(last_joint)),
					'{}.cv[0:22]'.format(bottom_ik_bendy_ctrl), r=True)
		cmds.rotate(0, 0, -90, '{}.cv[0:22]'.format(top_ik_bendy_ctrl), r=True)

		# cmds.parentConstraint(first_joint, ik_bendy_grp,mo=True)
		# cmds.parentConstraint(top_ik_bendy_ctrl, start_handle,mo=True)
		# cmds.parentConstraint(bottom_ik_bendy_ctrl, end_handle, mo=True)
		# cmds.parentConstraint(first_joint, middle_joints[0])
		# cmds.parentConstraint(last_joint, middle_joints[3])

		cmds.connectAttr(ribbon_second_vis_attr,
						 '{}.v'.format(cmds.listRelatives(top_ik_bendy_ctrl, shapes=True)[0]))
		cmds.connectAttr(ribbon_second_vis_attr,
						 '{}.v'.format(cmds.listRelatives(bottom_ik_bendy_ctrl, shapes=True)[0]))

		handle_controllers = [top_ik_bendy_ctrl, bottom_ik_bendy_ctrl]
		handle_controllers_roots = [bottom_ik_bendy_root[0], top_ik_bendy_root[0]]
		# local system for handles
		# local system for handles
		local_geo_ik_geo = cmds.duplicate(middle_limb_nurb[0], n=name + 'Bendy_IK_Local' + self.nc['nurb'])
		cmds.skinCluster(middle_joints, local_geo_ik_geo, sm=0, bm=1, tsb=True)

		local_geo = cmds.duplicate(middle_limb_nurb[0], n=name + 'Bendy_Other_Local' + self.nc['nurb'])
		# cmds.skinCluster(middle_joints, local_geo, sm=0, bm=1, tsb=True)

		cmds.select(local_geo_ik_geo, local_geo, middle_limb_nurb[0])
		bs = cmds.blendShape(n='{}_Bendy{}'.format(name, '_BS'), w=[(0, 1), (1, 1)], )
		cmds.skinCluster(twist_joints, middle_limb_nurb[0], sm=0, bm=1, tsb=True)

		local_grp = cmds.group(local_geo_ik_geo, local_geo, ik_bendy_grp, n=name + '_Local' + self.nc['group'])

		cmds.connectAttr(top_ik_bendy_ctrl + '.rotate', middle_joints[0] + '.rotate')
		cmds.connectAttr(bottom_ik_bendy_ctrl + '.rotate', middle_joints[3] + '.rotate')

		# Bendys
		# Create follicles
		cmds.select(middle_limb_nurb[0])
		mel.eval("createHair {} 1 10 0 0 0 0 5 0 1 2 1;".format(3))

		cmds.delete('hairSystem1', 'pfxHair1', 'nucleus1')
		cmds.setAttr(middle_limb_nurb[0] + '.inheritsTransform', 0)

		for C in range(1, 4):
			cmds.delete('curve' + str(C))
		bendy_fol_grp = cmds.rename('hairSystem1Follicles', name + '_Bendy' + self.nc['follicle'] + self.nc['group'])

		bendy_follicles = cmds.ls(bendy_fol_grp, dag=True, type='follicle')
		cmds.setAttr(bendy_follicles[0] + '.parameterU', 0.05)
		cmds.setAttr(bendy_follicles[-1] + '.parameterU', 0.95)

		custom_name = ['Start', 'End']
		second_ctrls = []
		second_roots = []
		for num, fol in enumerate([bendy_follicles[0], bendy_follicles[-1]]):
			ribbon_ctrl = self.curve(input=fol, type='sphere',
								   rename=True,
								   custom_name=True,
								   name=name.replace(self.nc['joint'], custom_name[num] + '_Bendy' + self.nc['ctrl']),
								   size=ctrl_size / 1.5,
								   )
			self.assign_color(ribbon_ctrl, sec_color)
			root, auto = self.root_grp(input=ribbon_ctrl, autoRoot=True)
			cmds.parentConstraint(cmds.listRelatives(fol, p=True)[0], root, mo=False)
			cmds.connectAttr(ribbon_ends_vis_attr,
							 '{}.v'.format(cmds.listRelatives(ribbon_ctrl, shapes=True)[0]))
			second_ctrls.append(ribbon_ctrl)
			second_roots.append(root)
			self.shape_with_attr(input=ribbon_ctrl, obj_name=name + '_Switch', attr_name='')
			# Normalize Follicles
			cmds.connectAttr('Global_Ctrl.scale', cmds.listRelatives(fol, p=True)[0] + '.scale')

		forward = list(enumerate(ribbon_ctrls))
		backward = list(reversed(forward))

		extra_aim_forward_grp = cmds.group(em=True, n=name + '_ForwardAim' + self.nc['group'])
		cmds.scaleConstraint('Global_Ctrl', extra_aim_forward_grp)

		for num, ctrl in enumerate(ribbon_ctrls):
			auto = cmds.listRelatives(ctrl, p=True)
			pc = \
				cmds.parentConstraint(second_ctrls[0], second_ctrls[1], auto, skipRotate=('x', 'y', 'z'), mo=True)[
					0]
			cmds.setAttr(pc + '.' + second_ctrls[0] + 'W0', backward[num][0])
			cmds.setAttr(pc + '.' + second_ctrls[1] + 'W1', forward[num][0])
			cmds.setAttr(pc + '.interpType', 2)  # shortest

			# aim to ctrl
			# cmds.aimConstraint(second_ctrls[1], auto, aimVector =(aim, 0, 0), upVector = (0,0,-1)), worldUpType='vector', mo=True)#, worldUpObject=up_vector_loc, mo=True)
			cmds.aimConstraint(second_ctrls[1], auto, aimVector=(1, 0, 0), upVector=(0, 1, 0),
							   worldUpType='object', worldUpObject=second_ctrls[1], mo=True)

			# add extra aim to next controller
			aim_loc = cmds.spaceLocator(n=ctrl.replace(self.nc['ctrl'], '_Aim' + self.nc['locator']))[0]
			aim_loc_root = self.root_grp()
			cmds.parent(aim_loc_root, extra_aim_forward_grp)
			cmds.delete(cmds.parentConstraint(ribbon_ctrls[num], aim_loc_root, mo=False))
			cmds.parentConstraint(cmds.listRelatives(ribbon_ctrls[num], p=True)[0], aim_loc_root, mo=True)

			# Create upVector
			up_aim_loc = cmds.spaceLocator(n=ctrl.replace(self.nc['ctrl'], '_UpVector' + self.nc['locator']))[0]
			cmds.parent(up_aim_loc, aim_loc_root)
			cmds.delete(cmds.parentConstraint(aim_loc, up_aim_loc, mo=False))
			cmds.setAttr(up_aim_loc + '.translateZ', ctrl_size * -1)
			# Create Aim
			# aimConstraint -mo -weight 1 -aimVector 1 0 0 -upVector 0 0 -1 -worldUpType "object" -worldUpObject L_Shoulder_UpVector_Loc_2_UpVector_Loc;
			try:
				cmds.aimConstraint(cmds.listRelatives(ribbon_ctrls[num + 1], p=True)[0], aim_loc,
								   aimVector=(1, 0, 0), upVector=(0, 0, -1), worldUpType='object',
								   worldUpObject=up_aim_loc, mo=True)
			except:
				pass
			aim_grp = self.root_grp(ribbon_ctrls[num], custom=True, custom_name='_ForwardAim')[0]
			cmds.connectAttr(aim_loc + '.rotate', aim_grp + '.rotate')

		# Connect Handles local to 2nd controllers
		cmds.parentConstraint(second_ctrls[0], top_ik_bendy_root, mo=True)
		cmds.parentConstraint(second_ctrls[1], bottom_ik_bendy_root, mo=True)
		# cmds.aimConstraint(second_ctrls[1], top_ik_bendy_root, mo=True)
		# cmds.aimConstraint(second_ctrls[0], bottom_ik_bendy_root, mo=True)

		# clean the ribbon a bit
		ribbon_ctrl_grp = cmds.group(n=name.replace(self.nc["joint"], '_Ribbon' + self.nc['ctrl'] + self.nc['group']), em=True)
		cmds.parent(second_roots, tweks_ribbon_ctrl_grp, bottom_ik_bendy_root, top_ik_bendy_root,
					ribbon_ctrl_grp)

		ribbon_rig_group = cmds.group(n=name.replace(self.nc["joint"], '_Ribbon_Rig' + self.nc['group']), em=True)
		#cmds.setAttr('{}.inheritsTransform'.format(ribbon_rig_group), 0)
		cmds.parent(local_grp, bendy_fol_grp, extra_aim_forward_grp, middle_limb_nurb[0], ribbon_rig_group)

		# transfer scale from twist to ibbon jnts
		for num, jnt in enumerate(twist_joints):
			cmds.connectAttr('{}.scale'.format(jnt), '{}.scale'.format(fol_joints[num]))

		return {'ribbon_ctrl_grp': ribbon_ctrl_grp, 'ribbon_ctrls': ribbon_ctrls,
				'ribbon_plane': ribbon_limb_nurb[0], 'fol_ribbon_grp': fol_grp, 'fol_joints': fol_joints,
				'second_ctrls': second_ctrls, 'handle_controllers': handle_controllers,
				'handle_controllers_roots': handle_controllers_roots,
				'clean_rig_grp': ribbon_rig_group, 'clean_ctrl_grp': ribbon_ctrl_grp,
				'middle_joints': middle_joints
				}

	#----------------------------------------------------------------------------------------------------------------

	def copy_skin_values(self, vertex_selection):
		"""to be used with: self.create_rivet_skin_constraint
		Copy skinning values from a selected vertex.

		Args:
			vertex_selection (list): A list containing the name of a single vertex to copy skinning from.

		Returns:
			tuple: A tuple containing two lists - relevant_values and relevant_joints.

		Notes:
		- This function takes a list with a single vertex name as input.
		- It retrieves the skinCluster associated with the vertex and collects skinning information.
		- The skinning information is filtered to include only joints with significant influence (value > 0.01).

		Usage:
		relevant_values, relevant_joints = copy_skin_values(["pSphere1.vtx[10]"])
		"""
		if len(vertex_selection) != 1:
			cmds.error("Please select 1 and only 1 vertex to copy skinning from.")

		obj = vertex_selection[0].split(".")[0]

		vertex_skincluster = cmds.ls(cmds.listHistory(obj), type="skinCluster")[0]

		relevant_values = []
		relevant_joints = []

		# Get weight values
		skinVals = cmds.skinPercent(vertex_skincluster, vertex_selection, query=True, value=True)
		# Get joints list which affect the vertex
		jointVals = cmds.skinPercent(vertex_skincluster, vertex_selection, query=True, transform=None)

		for value, jnt in zip(skinVals, jointVals):
			if value > 0.01:
				relevant_values.append(value)
				relevant_joints.append(jnt)

		return relevant_values, relevant_joints

	def create_rivet_skin_constraint(self):
		"""
		Create a parent constraint to skinning for selected elements.

		Notes:
		- This function is designed to be used in Autodesk Maya.
		- It assumes you have selected mesh elements (vertices or other components).
		- It creates joints at the selected elements' positions and applies a parent constraint with relevant skinning weights.

		Usage:
		- Select the mesh elements you want to create constraints for.
		- Run create_rivet_skin_constraint().

		Example:
		create_rivet_skin_constraint()
		"""
		sel = cmds.ls(sl=True, flatten=True)

		for s in sel:
			cmds.select(cl=True)
			pos = cmds.pointPosition(s)
			element = cmds.joint(n=s + nc['joint'])
			cmds.xform(element, t=pos)

			relevant_values, relevant_joints = self.copy_skin_values(vertex_selection=[s])

			element_selection = element

			new_constraint = cmds.parentConstraint(relevant_joints, element, mo=True)[0]
			num = 0
			for jnt, val in zip(relevant_joints, relevant_values):
				cmds.setAttr("{}.{}W{}".format(new_constraint, jnt, num), val)
				num = num + 1
			cmds.setAttr("{}.interpType".format(new_constraint), 2)


	#----------------------------------------------------------------------------------------------------------------

	def create_dynamic_fk(self, joints=[]):

		if not joints:
			joints = cmds.ls(sl=True)

		for jnt in joints:
			if not jnt.endswith(self.nc['joint']):
				cmds.error('Joints must end with {}'.format(self.nc['joint']))

		dyn_joints = self.duplicate_change_names(input=joints[0], hi=True, search=self.nc['joint'], replace='_Dyn')
		fk_joints = self.duplicate_change_names(input=joints[0], hi=True, search=self.nc['joint'], replace=self.nc['fk'])

		cmds.select(cl=True)

		for jnt in fk_joints:
			cmds.select(jnt, add = True)

		#Create Fk System
		fk_system_ctrls = self.fk_chain(size=1, color='green', curve_type=setup['fk_ctrl'], scale=False)
		print('FK = {}'.format(fk_system_ctrls))

		#Switch Dyn Fk
		switches = []
		for num, ctrl in enumerate(fk_system_ctrls):
			cmds.select(ctrl)
			print(ctrl, joints[num])
			switch_attr = self.shape_with_attr(input='', obj_name='{}_Switch'.format(joints[num]),
												   attr_name='Switch_Dyn_FK')
			print(switch_attr)
			switches.append(switch_attr)


		for num, jnt in enumerate(joints):
			self.switch_constraints(this = fk_joints[num], that = dyn_joints[num], main = jnt, attr = switches[num])

		#Continue manual
		# Create Dynamic System
		cmds.select(dyn_joints[0], dyn_joints[-1])
		mel.eval('bt_makeJointsDynamicUI')

		cmds.warning('Just click create')