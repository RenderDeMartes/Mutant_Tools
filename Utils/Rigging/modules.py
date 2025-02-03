from __future__ import absolute_import
'''
version: 1.0.0
date: 21/04/2020


#----------------
how to: 
	
import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import modules
reload(Mutant_Tools.Utils.Rigging.modules)

modules = modules.Modules_class()
modules.FUNC(ARGUMENTS)

#----------------
dependencies:   
	
json
pymel
maya mel
maya.cmds
OpenMaya

tools.Tools_Class
kinematics.Kinematics_class


#----------------
licence: https://www.eulatemplate.com/live.php?token=FGISW7ApRfgywum6murbBmLcusKONzkv
author:  Esteban Rodriguez <info@mutanttools.com>

'''

import maya.mel
from maya import cmds
#import pymel.core as pm
from maya import OpenMaya

import os
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import json
from collections import OrderedDict
from pathlib import Path

try: 
	import tools
	reload(tools)
	import kinematics
	reload(kinematics)
except:
	import Mutant_Tools
	import Mutant_Tools.Utils.Rigging
	from Mutant_Tools.Utils.Rigging import tools
	reload(Mutant_Tools.Utils.Rigging.tools)
	from Mutant_Tools.Utils.Rigging import kinematics
	reload(Mutant_Tools.Utils.Rigging.kinematics)
try:
	from rstar.naming import NameInfo
	from rstar.nodes.joint import Joint
	stellar_guide= NameInfo(base='Guide')
except:
	stellar_guide = 'Guide'

#----------------------------------------------------------------------------------------------------------------

#Read name conventions as self.nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-2]
FOLDER=''
for f in PATH_PARTS:
	FOLDER = os.path.join(FOLDER, f)

#nc, curve_data, setup = tools.import_configs()

#----------------------------------------------------------------------------------------------------------------

class Modules_class(kinematics.Kinematics_class):

	def __init__(self):
		super(Modules_class, self).__init__()

	#----------------------------------------------------------------------------------------------------------------

	def create_block(self, name = 'Mutant', icon = 'Limb', attrs = {'attrs':'something'}, build_command = 'print("Test")', import_command = 'print("Test2")'):
		"""
		Creates a block with specified attributes and commands.

		Args:
		    name (str): The name of the block to create. Defaults to 'Mutant'.
		    icon (str): The name of the icon to use for the block. Defaults to 'Limb'.
		    attrs (dict): A dictionary containing the attributes to add to the block. Defaults to {'attrs': 'something'}.
		    build_command (str): The build command associated with the block. Defaults to 'print("Test")'.
		    import_command (str): The import command associated with the block. Defaults to 'print("Test2")'.

		Returns:
		    tuple: A tuple containing the block and the configuration network node.

		Raises:
		    None

		This function creates a block with the specified name and icon. It also adds attributes to the block based on the provided 'attrs' dictionary.
		The build and import commands are associated with the block as well.

		The function starts by constructing the path to the icon file using the 'os.path.join' function and the provided 'icon' name.

		It then creates an empty container object using the 'container' command and assigns it the specified name with the appropriate naming
		convention. The icon for the container is set using the 'setAttr' command.

		The function calls 'hide_attr' to hide transformation attributes of the block.

		If the 'Mutant_Build' group does not exist, the function creates it using the 'group' command.

		A network node is created using the 'createNode' command, and the necessary connections between the network node and the container are
		established using the 'connectAttr' command.

		Next, the function creates various attributes based on the provided 'attrs' dictionary. String attributes are created using the 'string_attr'
		function, enum attributes using the 'new_enum' function, float attributes using the 'new_attr_interger' function, and boolean attributes
		using the 'new_boolean' function.

		Finally, the function creates a 'precode' and 'postcode' attribute using the 'string_attr' function and returns the block and configuration
		network node as a tuple.

		Note:
		    This function assumes the use of the 'cmds' module from Autodesk Maya or a similar 3D software.
		"""

		icon = os.path.join(FOLDER.replace('Utils', ''), 'Icons', icon+'.png')

		cmds.select(cl=True)
		block = cmds.container(name = name + self.nc['module'],type='dagContainer')
		cmds.setAttr('{}.iconName'.format(block), icon, type="string")
		self.hide_attr(t=True, r=True, s=True,v=True)

		if cmds.objExists('Mutant_Build'):
			pass
		else:
			cmds.group(n = 'Mutant_Build', em=True)
		print (block)
		cmds.parent(block,'Mutant_Build')

		#create network node with all the attrs
		config = cmds.createNode('network', n = '{}_Config'.format(name))
		cmds.connectAttr('{}.nodeState'.format(config), '{}.nodeState'.format(block))

		#-----------------------------------------------------------------------------------------
		precode = self.string_attr(input = config, name = 'precode', string = '')

		build_command = self.string_attr(input = config, name = 'Build_Command', string = build_command)
		cmds.setAttr(build_command, lock=True)
		import_command = self.string_attr(input = config, name = 'Import_Command', string = import_command)
		cmds.setAttr(import_command, lock=True)

		#main block attrs
		for attr in attrs:
			if 'string' in attr:
				self.string_attr(input = config, name = attr.split('_')[0], string = attrs[attr])
			elif 'enum' in attr:
				self.new_enum(input= config, name = attr.split('_')[0], enums = attrs[attr])
			elif 'float' in attr:
				self.new_attr_interger(input= config, name = attr.split('_')[0], min = 1 , max = 20, default = int(attrs[attr]))
			elif 'bool' in attr:
				self.new_boolean(input= config, name = attr.split('_')[0], dv = attrs[attr])

		postcode = self.string_attr(input = config, name = 'postcode', string = '')

		return block,config

	#----------------------------------------------------------------------------------------------------------------

	def move_outliner(self, input = '', up = False, down = False):
		"""
		Moves the specified object or objects in the outliner hierarchy.

		Args:
		    input (str or list): The name or list of names of the object(s) to move in the outliner hierarchy. Defaults to an empty string, which
		                         selects the currently selected objects in the scene.
		    up (bool): Specifies whether to move the object(s) up in the outliner hierarchy. Defaults to False.
		    down (bool): Specifies whether to move the object(s) down in the outliner hierarchy. Defaults to False.

		Returns:
		    None

		Raises:
		    None

		This function allows moving an object or a list of objects in the outliner hierarchy. The objects to move can be specified by name or by using
		the currently selected objects in the scene.

		The function first checks if the 'input' argument is empty. If it is empty, it selects the currently selected objects in the scene.

		The function then retrieves the parent of the input object(s) using the 'listRelatives' command and stores it in the 'parent' variable. It also
		retrieves the list of children of the parent object using the 'listRelatives' command and stores it in the 'brothers' variable.

		If the 'up' argument is True, the function checks if the input object(s) is the first child in the 'brothers' list. If it is, it prints a
		message indicating that the object(s) is already at the top. Otherwise, it uses the 'reorder' command to move the object(s) up by one
		position in the outliner hierarchy.

		If the 'down' argument is True, the function checks if the input object(s) is the last child in the 'brothers' list. If it is, it prints a
		message indicating that the object(s) is already at the bottom. Otherwise, it uses the 'reorder' command to move the object(s) down by one
		position in the outliner hierarchy.

		If both 'up' and 'down' arguments are False, the function does nothing.

		Note:
		    This function assumes the use of the 'cmds' module from Autodesk Maya or a similar 3D software.
		"""
		if input ==  '':
			input = cmds.ls(sl=True)

		try:
			parent = cmds.listRelatives(input, p =True)
			brothers = cmds.listRelatives(parent, c = True)
			#print (brothers)

			if up == True:
				if brothers[0] == input:
					print ('{} is top'.format(input))
				else:
					cmds.reorder(input, r= -1 )
					print ('{} moved up'.format(input))

			if down == True:
				if brothers[-1] == input:
					print ('{} is bottom'.format(input))
				else:
					cmds.reorder(input, r= 1 )		
					print ('{} moved down'.format(input))

		except:
			if up == True:
				cmds.reorder( input, r= -1 )
			if down == True:
				cmds.reorder( input, r= 1 )


	#----------------------------------------------------------------------------------------------------------------

	def create_joint_guide(self, name = 'Guide'):
		"""
		Creates a joint guide with the specified name.

		Args:
			name (str): The name of the joint guide. Defaults to 'Guide'.

		Returns:
			str: The name of the created joint guide.

		Raises:
			None

		This function creates a joint guide consisting of a joint, a 2D arrow, a sphere, an arrow axis, and an arrow front. The joint guide is
		named using the specified name and the naming convention for guides.

		The function uses the 'cmds.joint' command to create the joint. It then creates the 2D arrow, sphere, arrow axis, and arrow front using the
		'curve' function with the respective types.

		The function assigns colors to the components of the joint guide using the 'assign_color' function.

		An enumeration attribute called 'Helper' is created on the joint, which can be used to turn on or off the visibility of the joint guide
		components. The visibility of each component is connected to this enumeration attribute using the 'connectAttr' function.

		The visibility of the joint guide components is controlled based on the value of the 'axis_helper' setup attribute. If 'axis_helper' is set
		to 'True', the visibility of the joint guide components is turned on. Otherwise, it is turned off.

		The joint guide components are parented under the joint using the 'parent' command.

		The sphere, arrow, arrow axis, and arrow front components are deleted after parenting.

		Finally, the created joint is selected, and its name is returned.

		Note:
			This function assumes the use of the 'cmds' module from Autodesk Maya or a similar 3D software.
		"""
		cmds.select(cl=True)
		joint = cmds.joint(n = name + self.nc['guide'])
		arrow = self.curve(type = '2dArrow')
		sphere = self.curve(type = 'sphere')

		arrowAxis = self.curve(type = '2dArrow')
		cmds.rotate(90,90,0,cmds.listRelatives(arrowAxis, s=True)[0] + '.cv[0:9]')
		arrowFront = self.curve(type = '2dArrow')
		cmds.rotate(90,0,90,cmds.listRelatives(arrowFront, s=True)[0] + '.cv[0:9]')

		self.assign_color(input = cmds.listRelatives(arrow, s=True)[0], color = 'green')
		self.assign_color(input = cmds.listRelatives(sphere, s=True)[0])
		self.assign_color(input = cmds.listRelatives(arrowAxis, s=True)[0], color = 'red')
		self.assign_color(input = cmds.listRelatives(arrowFront, s=True)[0], color = 'blue')

		#create turn off and on attr
		hide_attr = self.new_enum(input = joint, name = 'Helper')
		print (hide_attr)
		print (joint)
		cmds.connectAttr(hide_attr, cmds.listRelatives(arrow, s=True)[0] + '.v', f=True)
		cmds.connectAttr(hide_attr, cmds.listRelatives(sphere, s=True)[0] + '.v', f=True)
		cmds.connectAttr(hide_attr, cmds.listRelatives(arrowAxis, s=True)[0] + '.v', f=True)
		cmds.connectAttr(hide_attr, cmds.listRelatives(arrowFront, s=True)[0] + '.v', f=True)

		if self.setup['axis_helper'] == 'True':
			cmds.setAttr(hide_attr, 1)
		else:
			cmds.setAttr(hide_attr, 0)

		cmds.parent(cmds.listRelatives(arrow, s=True),joint,r=True, s=True)
		cmds.parent(cmds.listRelatives(sphere, s=True),joint,r=True, s=True)
		cmds.parent(cmds.listRelatives(arrowAxis, s=True),joint,r=True, s=True)
		cmds.parent(cmds.listRelatives(arrowFront, s=True),joint,r=True, s=True)

		cmds.delete(sphere, arrow, arrowAxis,arrowFront)
		cmds.select(joint)

		return joint
	
	def create_stellar_joint_guide(self, name = stellar_guide):
		"""
		Creates a stellar joint guide with the specified name.

		Args:
		    name (str): The name of the stellar joint guide. Defaults to 'stellar_guide'.

		Returns:
		    str: The name of the created joint guide.

		Raises:
		    None

		This function creates a stellar joint guide consisting of a joint, a 2D arrow, a sphere, an arrow axis, and an arrow front. The joint guide is
		named using the specified name and the naming convention for guides.

		The function uses the 'Joint.create' method (assuming it exists) or the 'cmds.joint' command to create the joint. It then creates the 2D arrow,
		sphere, arrow axis, and arrow front using the 'curve' function with the respective types.

		The function assigns colors to the components of the joint guide using the 'assign_color' function.

		An enumeration attribute called 'Helper' is created on the joint, which can be used to turn on or off the visibility of the joint guide
		components. The visibility of each component is connected to this enumeration attribute using the 'connectAttr' function.

		The visibility of the joint guide components is controlled based on the value of the 'axis_helper' setup attribute. If 'axis_helper' is set
		to 'True', the visibility of the joint guide components is turned on. Otherwise, it is turned off.

		The joint guide components are parented under the joint using the 'parent' command.

		The sphere, arrow, arrow axis, and arrow front components are deleted after parenting.

		Finally, the created joint is selected, and its name is returned.

		Note:
		    This function assumes the use of the 'cmds' module from Autodesk Maya or a similar 3D software.
		"""
		#name = str(name)

		cmds.select(cl=True)
		joint = Joint.create(name.copy(), sself.nc['guide'])
		#joint = cmds.joint(n = name + self.nc['guide'])
		arrow = self.curve(type = '2dArrow')
		sphere = self.curve(type = 'sphere')

		arrowAxis = self.curve(type = '2dArrow')
		cmds.rotate(90,90,0,cmds.listRelatives(arrowAxis, s=True)[0] + '.cv[0:9]')
		arrowFront = self.curve(type = '2dArrow')
		cmds.rotate(90,0,90,cmds.listRelatives(arrowFront, s=True)[0] + '.cv[0:9]')

		self.assign_color(input = cmds.listRelatives(arrow, s=True)[0], color = 'green')
		self.assign_color(input = cmds.listRelatives(sphere, s=True)[0])
		self.assign_color(input = cmds.listRelatives(arrowAxis, s=True)[0], color = 'red')
		self.assign_color(input = cmds.listRelatives(arrowFront, s=True)[0], color = 'blue')

		#create turn off and on attr
		hide_attr = self.new_enum(input = joint, name = 'Helper')
		print (hide_attr)
		print (joint)
		cmds.connectAttr(hide_attr, cmds.listRelatives(arrow, s=True)[0] + '.v', f=True)
		cmds.connectAttr(hide_attr, cmds.listRelatives(sphere, s=True)[0] + '.v', f=True)
		cmds.connectAttr(hide_attr, cmds.listRelatives(arrowAxis, s=True)[0] + '.v', f=True)
		cmds.connectAttr(hide_attr, cmds.listRelatives(arrowFront, s=True)[0] + '.v', f=True)

		if self.setup['axis_helper'] == 'True':
			cmds.setAttr(hide_attr, 1)
		else:
			cmds.setAttr(hide_attr, 0)

		cmds.parent(cmds.listRelatives(arrow, s=True),joint,r=True, s=True)
		cmds.parent(cmds.listRelatives(sphere, s=True),joint,r=True, s=True)
		cmds.parent(cmds.listRelatives(arrowAxis, s=True),joint,r=True, s=True)
		cmds.parent(cmds.listRelatives(arrowFront, s=True),joint,r=True, s=True)

		cmds.delete(sphere, arrow, arrowAxis,arrowFront)
		cmds.select(joint)

		return joint
	#----------------------------------------------------------------------------------------------------------------

	def orient_joint(self, input = ''):
		"""
		Orients a joint based on the specified input.

		Args:
		    input (str): The name of the joint to orient. If not provided, the currently selected joint is used. Defaults to an empty string.

		Returns:
		    None

		Raises:
		    None

		This function orients a joint by applying identity transformation, including translation, rotation, and scale. It then adjusts the joint's
		orientation based on the specified twist axis and secondary axis orientation.

		If the 'input' parameter != provided, the function uses the currently selected joint as the input.

		The function uses the 'makeIdentity' function to reset the joint's transformations. It then uses the 'joint' function with the appropriate
		'oj' (orient joint) flag and 'secondaryAxisOrient' parameter to orient the joint based on the specified twist axis and secondary axis orientation.

		If an error occurs during the joint orientation process, an error message is printed.

		Note:
		    This function assumes the use of the 'cmds' module from Autodesk Maya or a similar 3D software.

		Example:
		    orient_joint(input='joint1')
		"""
		if input =='':
			input = cmds.ls(sl=True)[0]

		cmds.makeIdentity(input, apply=True, t=True, r=True, s=True ,n=False, pn=1)
		try:
			if self.setup['twist_axis'] == 'Y':
				cmds.joint(input, e = True, oj = 'yxz' , ch=True, secondaryAxisOrient = '{}'.format(self.setup['secondaryAxisOrient']))
			elif self.setup['twist_axis'] == 'X':
				cmds.joint(input, e = True, oj = 'xyz' , ch=True, secondaryAxisOrient = '{}'.format(self.setup['secondaryAxisOrient']))
			else:
				cmds.joint(input, e = True, oj = 'zyx' , ch=True, secondaryAxisOrient = '{}'.format(self.setup['secondaryAxisOrient']))
		except:
			print ('Error while orienting joints, sorry')
			
	#----------------------------------------------------------------------------------------------------------------

	def ask_name(self, text = '', ask_for = 'Name', check_split = False, popup=True, allow_name_exists=False):
		"""
		Asks the user for a block name.

		Args:
		    text (str): The initial text displayed in the prompt dialog. Defaults to an empty string.
		    ask_for (str): The message displayed in the prompt dialog, specifying what the name is asked for. Defaults to 'Name'.
		    check_split (bool): Specifies whether to check for name existence after splitting the input at a comma. Defaults to False.
		    popup (bool): Specifies whether to display a popup dialog for errors and warnings. Defaults to True.
			allow_name_exists (bool) : Allow names in case is used not for a block creation

		Returns:
		    str or None: The entered block name if the user clicked 'OK' and the name doesn't exist, or None if the user clicked 'Cancel'
		                or didn't enter a name.

		Raises:
		    None

		This function displays a prompt dialog with a given title and message, allowing the user to enter a block name. The dialog
		has 'OK' and 'Cancel' buttons. If the user clicks 'OK', the function checks if the entered name already exists as an object
		in the scene. If the name already exists, an error message is printed and a confirmation dialog is displayed indicating the
		name already exists.

		If the 'check_split' parameter is set to True, the function also checks for name existence after splitting the entered name
		at a comma (','). If the split name already exists, an error message is printed and a confirmation dialog is displayed.

		The function returns the entered block name if the user clicked 'OK' and the name doesn't exist. If the user clicked 'Cancel'
		or didn't enter a name, None is returned.

		If the 'popup' parameter is set to True, warning messages are displayed using the 'cmds.warning' function. Otherwise, the
		warning messages are printed to the console.

		Note:
		    This function assumes the use of the 'cmds' module from Autodesk Maya or a similar 3D software.

		Example:
		    name = ask_name(text='Enter block name:', ask_for='Block Name', check_split=True, popup=True)
		    if name != None:
		        print(f"Entered block name: {name}")
		"""

		ask_name = cmds.promptDialog(
						title='Name Block',
						message=ask_for,
						button=['OK', 'Cancel'],
						defaultButton='OK',
						cancelButton='Cancel',
						dismissString='Cancel',
						tx = text)

		if ask_name == 'OK':
			if cmds.objExists(cmds.promptDialog(query=True, text=True).replace(',','_')+self.nc['module']):
				if not allow_name_exists:
					print ('Name exists error')
					cmds.confirmDialog( title='Error',
										message='Error "{}": Block name already exists.'.format(
											cmds.promptDialog(query=True, text=True).replace(',','_')+self.nc['module']),
										button=["Oh! ok!"])

			if check_split == True:
				if cmds.objExists(cmds.promptDialog(query=True, text=True).split(',')[0]+self.nc['module']):
					if not allow_name_exists:
						print ('Name exists error')
						cmds.confirmDialog( title='Error',
											message='Error: Block name already exists',
											button=["Oh! ok!"])

			return cmds.promptDialog(query=True, text=True)	

		else:
			cmds.warning('We need a name :)')
			

	#----------------------------------------------------------------------------------------------------------------

	def duplicate_and_remove_guides(self, input = ''):
		"""
		Duplicates the top chain joint and changes '_Guide' to '_Jnt' in the name.
		Renames all children and parent to the world.

		Args:
			input (str): The input joint(s) to duplicate. If empty, selects the first item from the current selection.

		Returns:
			str: The name of the duplicated joint.

		Raises:
			None

		This function duplicates the specified joint(s) and modifies the name of the duplicated joint(s) by replacing the '_Guide'
		suffix with '_Jnt'. It also removes specific attributes and re-parents the joints to the world space.

		Note:
			This function assumes the use of the 'cmds' module from Autodesk Maya or a similar 3D software.

		Example:
			duplicate_and_remove_guides(input='joint_01_Guide')
		"""
		if input == '':
			input = cmds.ls(sl=True)[0]

		#duplicate the joints
		clean_joints = cmds.duplicate(input , to = True, n = input.replace(self.nc['guide'], self.nc['joint']), rc=True)
		for jnt in clean_joints:
			if self.nc['guide'] in str(jnt):
				jnt = cmds.rename(jnt, jnt.replace(self.nc['guide'], self.nc['joint']))

				try:cmds.deleteAttr( '{}.Helper'.format(jnt) )
				except:pass

			if jnt.endswith('1'):
				jnt =cmds.rename(jnt, jnt.replace('1', ''))

			try:
				parent = cmds.listRelatives(jnt, p=True)
				cmds.parent(jnt,w=True)
				cmds.parent( jnt, parent)
			except:pass


		cmds.parent(clean_joints[0], w=True)

		return clean_joints[0]

	def duplicate_and_remove_stellar_guides(self, input = ''):
		"""
		Duplicates the top chain joint, changes '_Guide' to '_Jnt' in the name, and renames all children plus parent to the world.

		Args:
			input (str): The input joint(s) to duplicate. If empty, selects the first item from the current selection.

		Returns:
			list: A list of duplicated joint objects.

		Raises:
			None

		This function duplicates the specified joint(s) and modifies the name of the duplicated joint(s) by replacing the '_Guide'
		suffix with '_Jnt'. It also removes specific attributes and re-parents the joints to the world space.

		Note:
			This function assumes the use of the 'cmds' module from Autodesk Maya or a similar 3D software.

		Example:
			duplicate_and_remove_stellar_guides(input='joint_01_Guide')
		"""
		if input == '':
			input = cmds.ls(sl=True)[0]

		#duplicate the joints
		#clean_joints = cmds.duplicate(input , to = True, n = input.replace(self.nc['guide'], self.nc['joint']), rc=True)
		clean_joints=[]
		dirt_jnts = cmds.duplicate(input , to = True, rc=True)
		for clean_joint in dirt_jnts:
			jnt = Joint(clean_joint)
			jnt_ni = jnt.name_info.copy(node_type = sself.nc['joint'])
			jnt.rename(jnt_ni)

			if sself.nc['guide'] in str(jnt):
				jnt = cmds.rename(jnt, jnt.name_info.copy(node_type=sself.nc['joint']))

				try:cmds.deleteAttr( '{}.Helper'.format(jnt) )
				except:pass

			#REMOVED THIS IF.
			#if jnt.endswith('1'):
			#	jnt =cmds.rename(jnt, jnt.replace('1', ''))

			try:
				parent = cmds.listRelatives(jnt, p=True)
				cmds.parent(jnt,w=True)
				cmds.parent( jnt, parent)
			except:pass

			clean_joints.append(jnt)

		cmds.parent(clean_joints[0], w=True)

		return clean_joints

	#----------------------------------------------------------------------------------------------------------------

	def build_baseA(self, name='Asset_Name', size = 1):
		"""
		Creates the base structure for any kind of rig with the same base structure.

		Args:
			name (str): The name of the asset. Default is 'Asset_Name'.
			size (float): The size of the base controllers. Default is 1.

		Returns:
			tuple: A tuple containing the global controller, mover controller, and gimbal controller.

		Raises:
			None

		This function creates the base structure for a rig, including main groups, base groups, geometry groups, and rig groups.
		It also creates base controllers such as the global controller, mover controller, and gimbal controller. Various attributes
		are added to the controllers for control visibility, playback, and geometry visibility.

		Note:
			This function relies on other methods such as 'curve', 'root_grp', 'new_enum', 'new_attr', 'hide_attr', and specific
			attributes and naming conventions defined in the 'setup' attribute.

		Example:
			build_baseA(name='MyCharacter', size=1.5)
		"""
		#main grp
		main_grp = cmds.group(em=True, name = name +  self.nc['group'])

		#create base Groups
		base_groups = self.setup['base_groups'] 
		print (base_groups)

		for grp in base_groups:
			base_grp = cmds.group(em=True, n = base_groups[grp] + self.nc['group'])
			cmds.parent(base_grp, main_grp)
		
		geo_groups = self.setup['geo_groups']
		print (geo_groups)		
		for grp in geo_groups:
			geo_grp = cmds.group(em=True, n = geo_groups[grp] + self.nc['group'])
			cmds.parent(geo_grp, base_groups['geometry']+self.nc['group'])		
				
		rig_groups = self.setup['rig_groups']
		print (rig_groups)		
		for grp in rig_groups:
			rig_grp = cmds.group(em=True, n = rig_groups[grp] + self.nc['group'])
			cmds.parent(rig_grp, base_groups['rig']+self.nc['group'])	

		
		#create the base controllers

		global_ctrl = self.curve(type = 'root', custom_name=True, name = 'Global' + self.nc['ctrl'], size = size, tag=False, playback=False)
		global_offset = self.root_grp()

		#Add Attrs
		ctrls_vis = self.new_enum(input=global_ctrl, name = 'CtrlVis', enums = 'Default:Inherit:Proximity')
		hide_on_vis_attr = self.new_enum(input=global_ctrl, name='CtrlPlayback', enums='Show:Hide')
		geo_vis = self.new_enum(input=global_ctrl, name = 'Geo', enums = 'Normal:Template:Reference')
		geo_vis_toggle = self.new_enum(input=global_ctrl, name = 'GeoVis', enums = 'Hide:Show', default=1, keyable=True)
		cmds.setAttr(geo_vis_toggle, e=True, k=True)

		cmds.setAttr(hide_on_vis_attr, 1)
		cmds.connectAttr(hide_on_vis_attr, cmds.listRelatives(global_ctrl, shapes=True)[0] + '.hideOnPlayback')

		mover_ctrl = self.curve(type = 'mover', custom_name=True, name = 'Mover'  + self.nc['ctrl'],size = size)
		mover_offset = self.root_grp()
		gimbal_ctrl = self.curve(type = 'mover', custom_name=True, name = 'Mover'  + self.nc['gimbal_ctrl'], size = size*0.9)

		cmds.parent(gimbal_ctrl, mover_ctrl)
		cmds.parent(mover_offset, global_ctrl)
		cmds.parent(global_offset, 'Ctrl_Grp')

		vis_Attr = self.new_attr(input= mover_ctrl, name = 'Gimbal', min = 0 , max = 1, default = 0) 
		cmds.connectAttr(vis_Attr, cmds.listRelatives(gimbal_ctrl,s=True)[0]+'.v')

		#group for ctrls inside the gimal
		main_ctrl_grp = cmds.group(em = True, name = self.setup['main_ctrl_grp'] + self.nc['group'])
		cmds.parent(main_ctrl_grp, gimbal_ctrl)

		#clean
		self.hide_attr(input = mover_ctrl , s = True)
		self.hide_attr(input = gimbal_ctrl , s = True)

		return(global_ctrl, mover_ctrl, gimbal_ctrl)

	#----------------------------------------------------------------------------------------------------------------

	def check_is_there_is_base(self, base = 'BaseA'):
		"""
		Checks if the base structure exists and creates it if not.

		Args:
			base (str): The name of the base structure. Default is 'BaseA'.

		Returns:
			None

		Raises:
			None

		This function is intended to be placed at the start of all the modules. It checks if the specified base structure exists,
		and if not, it creates one. It also remembers the previous selection and restores it after the build.

		Note:
			This function relies on the 'cmds' module from Autodesk Maya or a similar 3D software.

		Example:
			check_is_there_is_base(base='BaseA')
		"""
		sel = cmds.ls(sl=True)#this will remember previews selection so it wont affect any build

		if base == 'BaseA':
			if cmds.objExists('Rig_Grp'):
				pass
			else:
				base = self.build_baseA(name = 'Mutant_Tools')
				print('BaseA Created Successfully')

		cmds.select(sel)#return to previews selection after the build

	#----------------------------------------------------------------------------------------------------------------

	def Mutant_logger(self, mode = 'create'):
		"""
		Manages the Mutant logger for scriptEditor history.

		Args:
			mode (str): The mode of operation for the logger. Default is 'create'.

		Returns:
			str or None: The path to the Mutant log file if mode != 'create', otherwise None.

		Raises:
			None

		This function manages the Mutant logger, which controls the scriptEditor history. It can be used to create, stop, or clear
		the logger. When mode is set to 'create', it creates the log file and enables scriptEditor history logging. When mode is
		set to 'stop', it disables scriptEditor history logging. When mode is set to 'clear', it clears the contents of the log
		file. If mode != one of the specified options, it returns the path to the Mutant log file.

		Note:
			This function assumes the use of the 'cmds' module from Autodesk Maya or a similar 3D software.

		Example:
			Mutant_logger(mode='create')
		"""

		log_file = os.path.join(cmds.internalVar(usd=True), 'Mutant_log.txt')

		if mode == 'create': 
			print (log_file)
			cmds.scriptEditorInfo(historyFilename=log_file, writeHistory=True)
		elif mode == 'stop':
			cmds.scriptEditorInfo(writeHistory=False)
		elif mode == 'clear':
			open(log_file, 'w').close()
		else:
			return log_file

	#----------------------------------------------------------------------------------------------------------------

	def update_icons(self):
		"""
	   Updates the icons of Mutant build blocks.

	   Args:
		   None

	   Returns:
		   None

	   Raises:
		   None

	   This function updates the icons of Mutant build blocks. It assumes the existence of a folder named 'Icons' within the
	   project directory. If the 'Mutant_Build' object does not exist, the function returns without performing any changes.
	   It retrieves the current icon of each block, extracts the filename, and constructs the path to the corresponding icon
	   file within the 'Icons' folder. Finally, it sets the 'iconName' attribute of each block to the new icon path.

	   Note:
		   This function assumes the use of the 'cmds' module from Autodesk Maya or a similar 3D software.

	   Example:
		   update_icons()
		   """

		ICON_FOLDER = os.path.join(FOLDER, 'Icons')

		if not cmds.objExists('Mutant_Build'):
			return

		blocks = cmds.listRelatives('Mutant_Build', ad=True)
		if blocks:
			for block in blocks:
				try:
					current_icon = cmds.getAttr('{}.iconName'.format(block), asString = True)
					current_icon = current_icon.split('/')[-1]
					icon = os.path.join(FOLDER.replace('Utils', ''), 'Icons', current_icon)
					cmds.setAttr('{}.iconName'.format(block), os.path.join(ICON_FOLDER, icon), type="string")
				except:pass


	#----------------------------------------------------------------------------------------------------------------

	def check_dev_mode(self):
		"""
		Checks if the Mutant Tools is in development mode.

		Args:
			None

		Returns:
			bool: True if the Mutant Tools is in development mode, False otherwise.

		Raises:
			None

		This function checks if the Mutant Tools is in development mode. It reads the 'version.json' file located in the 'config'
		folder within the project directory to retrieve the current version information. If the 'dev_mode' key in the version file
		is set to 'On', the function returns True indicating that the Mutant Tools is in development mode.

		If the 'dev_mode' key != set to 'On', the function attempts to import the 'Mutant_Tools' module and reloads the 'helpers'
		module from the 'Mutant_Tools.Utils.Helpers' package. It then creates an instance of the 'Helpers' class and checks for the
		'dev_mode' key in the 'MutantTools.settings' JSON file. If the 'dev_mode' key is present and set to True, the function returns
		True indicating that the Mutant Tools is in development mode.

		If any exceptions occur during the process, the function returns False indicating that the Mutant Tools != in development mode.

		Note:
			This function assumes the use of the 'cmds' module from Autodesk Maya or a similar 3D software, as well as the 'json'
			module for JSON file handling.

		Example:
			check_dev_mode()
		"""
		VERSION_FILE = os.path.join(FOLDER, 'config', 'version.json')
		with open(VERSION_FILE) as version_file:
			version = json.load(version_file)

		if version['dev_mode'] == 'On':
			return True

		#------------------------------------------------------------------------
		import Mutant_Tools
		from Mutant_Tools.Utils.Helpers import helpers
		reload(Mutant_Tools.Utils.Helpers.helpers)
		mh = helpers.Helpers()

		settings = {}
		settings['dev_mode']=True
		try:
			settings = mh.read_json(path=os.path.join(cmds.internalVar(usd=True)),json_file='MutantTools.settings')
		except:
			mh.write_json(path=os.path.join(cmds.internalVar(usd=True)),json_file='MutantTools.settings', data = settings)

		try:
			if settings['dev_mode']:
				return True
		except:
			return False

		return False

	#----------------------------------------------------------------------------------------------------------------

	def toggle_dev_mode(self):
		"""
		Toggles the Mutant Tools development mode.

		Args:
		    None

		Returns:
		    None

		Raises:
		    None

		This function toggles the Mutant Tools development mode. It attempts to import the 'Mutant_Tools' module and reloads the
		'helpers' module from the 'Mutant_Tools.Utils.Helpers' package. It then creates an instance of the 'Helpers' class and
		reads the 'MutantTools.settings' JSON file located in the 'cmds.internalVar(usd=True)' path. If the file does not exist,
		it creates the file with a default 'dev_mode' value of False.

		If the 'dev_mode' key in the JSON file is currently set to True, the function updates the value to False and displays a
		confirmation dialog indicating that the development mode is now turned off. If the 'dev_mode' key is currently set to
		False, the function updates the value to True and displays a confirmation dialog indicating that the development mode is
		now turned on.

		Note:
		    This function assumes the use of the 'cmds' module from Autodesk Maya or a similar 3D software, as well as the 'json'
		    module for JSON file handling.

		Example:
		    toggle_dev_mode()
		"""
		import Mutant_Tools
		from Mutant_Tools.Utils.Helpers import helpers
		reload(Mutant_Tools.Utils.Helpers.helpers)
		mh = helpers.Helpers()

		try:
			settings = mh.read_json(path=os.path.join(cmds.internalVar(usd=True)),json_file='MutantTools.settings')
		except:
			mh.write_json(path=os.path.join(cmds.internalVar(usd=True)),json_file='MutantTools.settings', data = {'dev_mode': False})
			settings = mh.read_json(path=os.path.join(cmds.internalVar(usd=True)),json_file='MutantTools.settings')

		if settings['dev_mode']:
			mh.write_json(path=os.path.join(cmds.internalVar(usd=True)), json_file='MutantTools.settings',
						  data={'dev_mode': False})
			cmds.confirmDialog(m='Dev Mode is now Off')
		else:
			mh.write_json(path=os.path.join(cmds.internalVar(usd=True)), json_file='MutantTools.settings',
						  data={'dev_mode': True})
			cmds.confirmDialog(m='Dev Mode is now On')

	#----------------------------------------------------------------------------------------------------------------


