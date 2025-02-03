from __future__ import absolute_import
'''
version: 1.0.0
date: 21/04/2020

#----------------

how to:
	
import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import tools
reload(Mutant_Tools.Utils.Rigging.tools)

tool = tools.Tools_class()
tool.FUNC_NAME(argument = '')

#----------------
dependencies:   

json
pymel
maya mel
maya.cmds

#----------------
licence: https://www.eulatemplate.com/live.php?token=FGISW7ApRfgywum6murbBmLcusKONzkv
author:  Esteban Rodriguez <info@mutanttools.com>

'''
import os
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import json
from pathlib import Path

from  maya import mel
from maya import cmds
from maya.api import OpenMaya as om2
import operator

PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-2]
FOLDER = ''
for f in PATH_PARTS:
	FOLDER = os.path.join(FOLDER, f)

#----------------------------------------------------------------------------------------------------------------

def import_configs(nc=True, curves=True, setup=True):
	PATH = os.path.dirname(__file__)
	PATH = Path(PATH)
	PATH_PARTS = PATH.parts[:-2]
	FOLDER = ''
	for f in PATH_PARTS:
		FOLDER = os.path.join(FOLDER, f)

	if nc:
		JSON_FILE = os.path.join(FOLDER, 'config', 'name_conventions.json')
		with open(JSON_FILE) as json_file:
			nc = json.load(json_file)
	else:
		nc = None

	if curves:
		# Read curve shapes info
		CURVE_FILE = os.path.join(FOLDER, 'config', 'curves.json')
		with open(CURVE_FILE) as curve_file:
			curve_data = json.load(curve_file)
	else:
		curve_data = None

	if setup:
		# setup File
		SETUP_FILE = os.path.join(FOLDER, 'config', 'rig_setup.json')
		with open(SETUP_FILE) as setup_file:
			setup = json.load(setup_file)
	else:
		setup = None


	return nc, curve_data, setup

nc, curve_data, setup = import_configs()

#----------------------------------------------------------------------------------------------------------------
#create base class for selection objects

class Tools_class(object):

	def __init__(self):
		super(Tools_class, self).__init__()

		self.input = ''
		self.nc, self.curve_data, self.setup = nc, curve_data, setup

	#----------------------------------------------------------------------------------------------------------------
	def import_configs(self):
		return import_configs(nc=True, curves=True, setup=True)

	#----------------------------------------------------------------------------------------------------------------			

	def check_input(self, func = '', print_input = False):
		"""	if input is empty uses selection instead, i used to use this but stop becouse != usefull... sorry :)


		Args:
			func: string: name of the function
			print_input: bool

		Returns: None

		"""

		if self.input == '':
						
			self.input = cmds.ls(sl = True)
			if (print_input):
				print ('{} input is selection: {}'.format(func, self.input))
			
		else:
			if (print_input):
				print ('{} input is argument: {}'.format(func, self.input))

		return None
	
	#----------------------------------------------------------------------------------------------------------------			
	def root_grp(self, input = '', custom = False, custom_name = 'customName', autoRoot = False, replace_nc = False):
		"""
		Create groups.

		Args:
		    input (str): Input string representing the selection. If not specified, the current selection will be used.
		    custom (bool): Specify if the new group should have a custom name.
		    custom_name (str): Name of the custom group (requires `custom` to be True).
		    autoRoot (bool): If True, create two groups instead of one: Root Grp and Auto Grp.
		    replace_nc (bool): Try to replace the namespace to match the groups' namespace.

		Returns:
		    list: List of strings representing the new groups.

		Notes:
		    - This method creates groups based on the specified arguments.
		    - It can create either one group or two groups (Root Grp and Auto Grp).
		    - If `custom` is True, the group(s) will have a custom name specified by `custom_name`.
		    - The method handles parenting and constraints to create the groups.
		    - If `replace_nc` is True, it will attempt to replace the namespace with the groups' namespace.

		Examples:
		    # Create a single group using the current selection
		    root_grp()

		    # Create a single group with a custom name
		    root_grp(custom=True, custom_name='MyGroup')

		    # Create two groups (Root Grp and Auto Grp) using the current selection
		    root_grp(autoRoot=True)

		    # Create two groups with a custom name
		    root_grp(custom=True, custom_name='MyGroup', autoRoot=True)

		    # Create groups and replace the namespace
		    root_grp(replace_nc=True)
		"""

		#Check input
		if input != '':
			self.input = [input]
			
		else:	
			self.input = input

		self.check_input('root_grp')

		#Group to have something to work after the command
		groups = []
		
		for i in self.input:
			
			if autoRoot == True:           
				group_names = [self.nc['root'], self.nc['auto']]
			else:
				group_names = [self.nc['offset']]				

			if custom == True:
				group_names = [custom_name]      

			if custom and autoRoot:
				group_names = [self.nc['root'], self.nc['auto'],custom_name]
				
			for name in group_names:
				
				cmds.select(i)
				father = cmds.listRelatives(i, p =1)
				
				#Null group as parent in same xform
				group_zero = cmds.group(em=1, n = '{}{}'.format(i,name) + self.nc['group'])
				cmds.delete(cmds.parentConstraint(i,group_zero, mo =0))
			  
				cmds.parent(i,group_zero)
				
				#if they have upper nodes, put them inside
				if father :cmds.parent(group_zero, father) 
				cmds.select(group_zero)
				
				#Remove Nameconventions		
				if (replace_nc):
					try:group_zero = self.replace_name(input = '', search = self.nc['ctrl'], replace = '', hi = False)
					except:pass
					
					try:group_zero = self.replace_name(input = '', search = self.nc['joint'], replace = '', hi = False)
					except:pass	
				
				#return this groups				
				groups.append(group_zero)     
				
		return groups    

	#----------------------------------------------------------------------------------------------------------------		
	
	def replace_name(self, input = '', search = '', replace = '', hi = False):
		"""
		Replace names in the selection. Works nicely to change names in hierarchies.

		Args:
		    input (str): Input string representing the selection. If not specified, the current selection will be used.
		    search (str): String to search for in the names.
		    replace (str): String to replace the matched search string with.
		    hi (bool): True if the change should be applied to the entire hierarchy.

		Returns:
		    list: List of new names.

		Notes:
		    - This function replaces occurrences of the `search` string with the `replace` string in the selection.
		    - If `input` != specified, it will use the current selection.
		    - If `hi` is True, the replacement will be applied to the entire hierarchy under each selected item.

		Examples:
		    # Replace 'old' with 'new' in the current selection
		    replace_name(search='old', replace='new')

		    # Replace 'old' with 'new' in a specific item
		    replace_name(input='item1', search='old', replace='new')

		    # Replace 'old' with 'new' in the entire hierarchy under each selected item
		    replace_name(search='old', replace='new', hi=True)
		"""

		if hi ==True:

			mel.eval( 'searchReplaceNames {} {} "hierarchy"'.format(search, replace))
			cmds.select(hi = True)
	
		else:
			mel.eval( 'searchReplaceNames {} {} "selected"'.format(search, replace))
	
	
		return cmds.ls(sl = True)

	#----------------------------------------------------------------------------------------------------------------
	
	def assign_color(self, input = '', color = 'lightBlue'):
		"""
		Assign a color to the desired transform.

		Args:
			input (str): Input string representing the selection. If not specified, the current selection will be used.
			color (str): Name of the color to assign. Available colors are: 'red', 'blue', 'white', 'purple', 'green',
						 'lightBlue', 'yellow', 'pink', 'grey', and 'orange'.

		Returns:
			None

		Notes:
			- This function assigns a color to the transform(s) specified in the input.
			- If `input` != specified, it will use the current selection.
			- The `color` parameter should be a string representing the color name.
			- The available colors and their corresponding values are defined in the `colors` dictionary.

		Examples:
			# Example 1: Assign the color 'red' to the current selection
			assign_color()

			# Example 2: Assign the color 'green' to a specific transform
			assign_color(input='transform1', color='green')

			# Example 3: Assign the color 'lightBlue' to multiple transforms
			assign_color(input=['transform1', 'transform2'], color='lightBlue')
		"""

		if input != '':
			self.input = [input]
			
		else:	
			self.input = input	
			
		self.check_input('assing_color')		
		
		colors = {  'red':       13,
					'blue':       6,
					'white':     16,
					'purple':     9,
					'green':     14, 
					'lightBlue': 18,
					'yellow':    17,
					'pink':      20,
					'grey':      1,
					'orange':    21 }

		color_num = colors[color]
		
		for obj in self.input:
			cmds.setAttr ('{}.overrideEnabled'.format(obj), 1)
			cmds.setAttr('{}.overrideRGBColors'.format(obj), 0)
			cmds.setAttr ('{}.overrideColor'.format(obj), color_num)


	def assign_color_rgb(self, input = '', color = [1,1,1], hsv=False):
		"""
		Assign an RGB color or HSV color to the desired transform(s).

		Args:
		    input (str or list): Input string or list representing the selection. If not specified, the current selection
		                         will be used.
		    color (list): List of RGB or HSV values representing the color to assign.
		    hsv (bool): True if the color values are in HSV format, False if they are in RGB format.

		Returns:
		    None

		Notes:
		    - This function assigns an RGB or HSV color to the transform(s) specified in the input.
		    - If `input` != specified, it will use the current selection.
		    - The `color` parameter should be a list of three values representing the color channels (R, G, B or H, S, V).
		    - If `hsv` is True, the `color` parameter is interpreted as HSV values. Otherwise, it is interpreted as RGB values.

		Examples:
		    # Example 1: Assign an RGB color to the current selection
		    assign_color(color=[1, 0, 0])

		    # Example 2: Assign an HSV color to a specific transform
		    assign_color(input='transform1', color=[0.5, 1, 1], hsv=True)

		    # Example 3: Assign an RGB color to multiple transforms
		    assign_color(input=['transform1', 'transform2'], color=[0, 1, 0.5])
		"""

		if not input:
			input = cmds.ls(sl=True)

		if not isinstance(input, list):
			input = [input]

		rgb = ("R", "G", "B")
		if hsv:
			import colorsys
			print(color)
			color[0], color[1], color[2] = colorsys.rgb_to_hsv(color[0], color[1], color[2])
			print(color)
		for ctrl in input:
			cmds.setAttr('{}.overrideEnabled'.format(ctrl), 1)
			cmds.setAttr('{}.overrideRGBColors'.format(ctrl), 1)
			for channel, color in zip(rgb, color):
				cmds.setAttr(ctrl + ".overrideColor%s" % channel, color)

	def smart_assign_color(self, input=''):
		"""
        Smartly assign predefined colors based on the input.

        Args:
            input (str or list): Input string or list representing the selection. If not specified, the current selection
                                 will be used.

        Returns:
            None

        Notes:
            - This function automatically assigns predefined colors based on the input string.
            - If `input` != specified, it will use the current selection.
            - The color assignment is determined based on the prefix of the input string.
            - If the input starts with the left prefix, it will assign the left color.
            - If the input starts with the right prefix, it will assign the right color.
            - Otherwise, it will assign the main color.

        Examples:
            # Example 1: Smartly assign color to the current selection
            smart_assign_color()

            # Example 2: Smartly assign color to a specific transform
            smart_assign_color(input='transform1')

        """
		if not input:
			input = cmds.ls(sl=True)

		if str(input).startswith(nc['left']):
			color = setup['left_color']
		elif str(input).startswith(nc['right']):
			color = setup['right_color']
		else:
			color = setup['center_color']

		self.assign_color(input, color)

	#----------------------------------------------------------------------------------------------------------------					
	def hide_attr(self, input = '', t= False, r = False, s = False, v = False, rotate_order = False, show = False):
		"""
		Hide selected attributes or display all attributes if show is True.

		Args:
			input (str): Input string representing the selection. If not specified, the current selection will be used.
			t (bool): True to hide translate attributes.
			r (bool): True to hide rotate attributes.
			s (bool): True to hide scale attributes.
			v (bool): True to hide visibility attribute.
			rotate_order (bool): True to hide rotate order attribute.
			show (bool): True to show all attributes.

		Returns:
			None

		Notes:
			- This function hides or displays selected attributes for the specified transform(s).
			- If `input` != specified, it will use the current selection.
			- Set the corresponding flag to True for each attribute you want to hide.
			- If `show` is True, all attributes will be shown and unlocked.

		Examples:
			# Example 1: Hide translate and scale attributes for the current selection
			hide_attr(t=True, s=True)

			# Example 2: Hide rotate order attribute for a specific transform
			hide_attr(input='transform1', rotate_order=True)

			# Example 3: Show all attributes for multiple transforms
			hide_attr(input=['transform1', 'transform2'], show=True)
		"""


		if input != '':
			self.input = [input]
			
		else:	
			self.input = input

		self.check_input('hide_attr')
		
		#Axis to hide in selection input
		axis_to_hide = ['X','Y','Z']
		
		#hide selected attrs
		for i in self.input:
			cmds.select(i)
			if (t):
				for T in self.input:
					for axis in axis_to_hide:
						cmds.setAttr('{}.translate{}'.format(T, axis),lock = True, keyable = False, channelBox = False)
		
			if (r):
				for R in self.input:
					for axis in axis_to_hide:
						cmds.setAttr('{}.rotate{}'.format(R, axis),lock = True, keyable = False, channelBox = False)
					try:cmds.setAttr('{}.RotateOrder'.format(R),lock = True, keyable = False, channelBox = False)
					except: print ('rdm.hide_attr: no rotate order found')

			if (s):
				for S in self.input:
					for axis in axis_to_hide:
						cmds.setAttr('{}.scale{}'.format(S, axis),lock = True, keyable = False, channelBox = False)
		
				
			if (v):
				for V in self.input:
					cmds.setAttr('{}.visibility'.format(V),lock = True, keyable = False, channelBox = False)        
			if (rotate_order):
				for ro in self.input:
					cmds.setAttr('{}.RotateOrder'.format(ro),lock = True, keyable = False, channelBox = False)        
								
			
			#show and unlock everything
			if (show):
				sel=cmds.ls(long=1, sl=1)
				attrs = ['.tx','.ty','.tz','.rx','.ry','.rz','.sx','.sy','.sz','.v']
				
				for eachObj in sel:
					for attr in attrs:	        
						cmds.listAttr(eachObj, ud=1)
						cmds.setAttr('{}{}'.format(eachObj, attr), k=True)
						cmds.setAttr('{}{}'.format(eachObj,attr), l=False)

	#----------------------------------------------------------------------------------------------------------------					

	def curve(self, input = '', type = 'cube', rename = True, custom_name = False, name = '', size = 1, tag=True, playback=True):
		"""
		For Controllers this is legacy, use mt.controller
		Will create a curve on the position of the selected input.
		(see curves.json in config for more details of available shapes)

		Args:
			input: if not specified, it will use the selection; otherwise, specify the string
			type: string name of the shape (default: 'cube')
			rename: bool to replace namespaces at the end (default: True)
			custom_name: True if you want to assign a new name, False if you want to use the same as the selection (default: False)
			name: string custom name (default: '')
			size: int size (default: 1)
			tag: bool to tag the curve as a controller (default: True)
			playback: bool to hide the curve during playback (default: True)

		Returns:
			string ctrl

		Examples:
			# Example 1: Create a curve using the default shape type ('cube') and rename it using the namespace of the selected input
			curve()

			# Example 2: Create a curve using the shape type 'circle' and assign a custom name
			curve(type='circle', custom_name=True, name='myCurve')

			# Example 3: Create a curve with a larger size (scale) of 2
			curve(size=2)

			# Example 4: Create a curve and tag it as a controller
			curve(tag=True)

			# Example 5: Create a curve and hide it during playback
			curve(playback=True)

		Types:
		"""

		try:sel = cmds.ls(sl = True)[0]
		except: sel = 'RdM'

		#create curve from mel cmds in json file
		curves_mel = self.curve_data[type]
		if not isinstance(curves_mel, list):
			curves_mel=[curves_mel]

		all_curves=[]
		for mel_curve in curves_mel:
			ctrl = mel.eval(mel_curve)
			all_curves.append(ctrl)

		#combine shapes into one
		dumb_transform = cmds.group(em=True)
		for c in all_curves:
			shape = cmds.listRelatives(c, s=True)
			if not shape:
				continue
			shape=shape[0]
			if cmds.attributeQuery('lineWidth', node=shape, exists=True):
				cmds.setAttr('{}.lineWidth'.format(shape), int(setup['line_width']))
			cmds.parent(shape, dumb_transform, s=True, r=True)
			cmds.delete(c)

		cmds.select(dumb_transform)
		ctrl = cmds.ls(sl=True)[0]
		#set name of the curve
		if (rename): 
			ctrl = cmds.rename(ctrl, '{}{}'.format(sel,self.nc['ctrl']))
		
		else:      
			ctrl = cmds.rename(ctrl, '{}{}'.format(type,self.nc['ctrl']))

		if (custom_name):
			ctrl = cmds.rename(ctrl, name)

		if (size):
			curve_cvs = cmds.ls(cmds.ls(sl = True)[0] + ".cv[0:]",fl=True)
			cmds.scale(size,size,size, curve_cvs)

		#rename the shape
		shapes = cmds.listRelatives(ctrl, s=True)
		if shapes:
			for shape in shapes:
				cmds.rename(shape, '{}Shape'.format(ctrl))

		#match to selection and assing color if possible
		try:self.match(ctrl, sel)
		except:pass
		self.assign_color(color = setup['main_color'])

		#connect rotate order to itself
		self.connect_rotate_order(input = ctrl, object = ctrl)

		try:self.hide_attr(input = ctrl, v=True)
		except:pass

		global_ctrl = 'Global{}'.format(self.nc['ctrl'])

		#Tag as controller
		if tag and cmds.nodeType(ctrl) != 'joint':
			if cmds.objExists(ctrl+'_tag'):
				cmds.delete(ctrl+'_tag')
			cmds.select(ctrl)
			mel.eval('TagAsController;')
			if cmds.objExists(global_ctrl):
				if cmds.attributeQuery('visibilityMode', node=ctrl+'_tag', exists=True) and cmds.attributeQuery('CtrlVis', node=global_ctrl, exists=True):
					cmds.connectAttr(global_ctrl+'.CtrlVis', ctrl+'_tag.visibilityMode')

		#hide on playback
		if playback:
			if cmds.objExists(global_ctrl):
				shapes = cmds.listRelatives(ctrl, shapes=True)
				if shapes:
					for shape in shapes:
						if cmds.attributeQuery('hideOnPlayback', node=shape, exists=True) and cmds.attributeQuery('CtrlPlayback', node=global_ctrl, exists=True):
							cmds.connectAttr(global_ctrl + '.CtrlPlayback',
						 					cmds.listRelatives(ctrl, shapes=True)[0] + '.hideOnPlayback')


		return ctrl

	def build_all_curves(self):
		"""
		Create all curves to generate icons or images quickly.

		Args:
		    None

		Returns:
		    None

		Notes:
		    - This function iterates over the `curve_data` list to create all the curves.
		    - Each curve is created using the `curve` function with the specified type.
		    - The curve is then renamed to match its type.

		Examples:
		    # Creates all the curves specified in the `curve_data` list.
		    build_all_curves()
		"""

		for curve in curve_data:
			cmds.select(cl=True)
			print()
			cv = self.curve(type=curve, custom_name=False, name=curve)
			cmds.rename(cv, curve)

	def change_curve_shape(self, input='', new_shape='', size = 1):
		"""Change the shape of a curve.

		Args:
		    input (str): Name of the curve object to modify. If not provided, the currently selected object will be used.
		    new_shape (str): The new shape type to be applied to the curve.
		    size (float): Size of the new shape.

		Returns:
		    bool: False if the new shape or input != specified or if the shapes cannot be retrieved.
		    bool: True if the curve shape is successfully changed.

		Raises:
		    None

		Notes:
		    - This function changes the shape of a curve by creating a new curve with the specified `new_shape` and `size`.
		    - The original curve's shape is replaced with the new shape.
		    - The `input` parameter specifies the name of the curve object to modify. If not provided, the currently selected object is used.
		    - The `new_shape` parameter specifies the type of shape to be applied to the curve.
		    - The `size` parameter specifies the size of the new shape.

		Examples:
		    # Change the shape of the selected curve to a cube shape with a size of 1.
		    change_curve_shape(new_shape='cube', size=1)

		    # Change the shape of the curve named 'curve1' to a circle shape with a size of 0.5.
		    change_curve_shape(input='curve1', new_shape='circle', size=0.5)
		"""

		if not input:
			input = cmds.ls(sl=True)[0]
			if not input:
				cmds.warning('We need an imput')
				return False

		if not new_shape:
			cmds.warning('Need new shape specified')
			return False

		print(input, new_shape)

		cmds.select(cl=True)
		new_cv = self.curve(type=new_shape, size=size)

		shapes = cmds.listRelatives(new_cv, s=True, f=True)
		og_shapes = cmds.listRelatives(input, s=True, type='nurbsCurve', f=True)

		if not shapes or not og_shapes:
			cmds.delete(new_cv)
			return False

		cmds.delete(og_shapes)
		for shape in shapes:
			new_named_shape = cmds.rename(shape, input+'Shape')
			cmds.parent(new_named_shape, input, r=True, s=True)
		cmds.delete(new_cv)

		cmds.select(input)
		return True

	#----------------------------------------------------------------------------------------------------------------
	def controller(self, input='', name='', shape='cube', color = setup['main_color'], size = 1, gimbal=True, world=True):
		"""Create a controller.

		Args:
		    input (str): Name of the input object. If None, the controller will be created in the world.
		    name (str): Desired name for the controller. If None, the input name will be used.
		    shape (str): Desired shape of the controller. See curves.json in the config for available shapes.
		    color (str): Desired color of the controller.
		    size (int): Desired size of the controller.
		    gimbal (bool): If True, creates a gimbal controller under the main controller.
		    world (bool): If True, creates a world control oriented to the world.

		Returns:
		    dict: Dictionary containing the created controllers:
		        - 'ctrl': Main controller
		        - 'root': Root group
		        - 'world': World controller (if world is True)
		        - 'gimbal': Gimbal controller (if gimbal is True)

		Notes:
		    - This function creates a controller with the specified parameters.
		    - The 'input' parameter specifies the name of the object where the controller will be created. If None, it will be created in the world.
		    - The 'name' parameter specifies the desired name for the controller. If None, the input name will be used.
		    - The 'shape' parameter specifies the desired shape of the controller.
		    - The 'color' parameter specifies the desired color of the controller.
		    - The 'size' parameter specifies the desired size of the controller.
		    - The 'gimbal' parameter determines whether a gimbal controller should be created under the main controller.
		    - The 'world' parameter determines whether a world controller should be created oriented to the world.

		Examples:
		    # Create a cube-shaped controller named 'ctrl1' with the default color, size of 1, and gimbal and world controllers.
		    controller(input='object1', name='ctrl1', shape='cube', color=setup['main_color'], size=1, gimbal=True, world=True)

		    # Create a sphere-shaped controller in the world with the default color, size of 2, and no gimbal or world controllers.
		    controller(shape='sphere', color=setup['main_color'], size=2, gimbal=False, world=False)
		"""

		if not input:
			input = 'Mt'

		if not name:
			cmds.warning('No name in mt.controller(), using input')
			name = input

		ctrl = mel.eval(self.curve_data[shape])

		try:self.match(ctrl, input)
		except:pass

		ctrl = cmds.rename(ctrl, '{}{}'.format(name, self.nc['ctrl']))
		root = self.root_grp()
		controllers = [ctrl]

		#Add gimbal sub controller
		if world:
			world = mel.eval(self.curve_data[shape])
			world = cmds.rename(world, '{}{}'.format(name, self.nc['world_ctrl']))
			controllers.append(world)
			world_root = self.root_grp()
			show_world_attr = self.new_enum(input=ctrl, name='World', enums='Hide:Show')
			cmds.connectAttr(show_world_attr, '{}.v'.format(cmds.listRelatives(world, shapes=True)[0]))
			self.match(world_root, ctrl, r=False)
			cmds.parent(root, world)


		if gimbal:
			gimbal = mel.eval(self.curve_data[shape])
			gimbal = cmds.rename(gimbal, '{}{}'.format(name, self.nc['gimbal_ctrl']))
			controllers.append(gimbal)
			show_gimbal_attr = self.new_enum(input=ctrl, name='Gimbal', enums='Hide:Show')
			cmds.connectAttr(show_gimbal_attr, '{}.v'.format(cmds.listRelatives(gimbal, shapes=True)[0]))
			self.match(gimbal, ctrl)
			cmds.parent(gimbal, ctrl)


		# make it pretty and clean
		for c in controllers:
			cmds.select(c)
			if size:
				curve_cvs = cmds.ls(cmds.ls(sl=True)[0] + ".cv[0:]", fl=True)
				cmds.scale(size, size, size, curve_cvs)
			self.assign_color(color=color)
			self.connect_rotate_order(input=c, object=c)
			cmds.setAttr('{}.lineWidth'.format(cmds.listRelatives(c, shapes=True)[0]), int(setup['line_width']))
			try:
				self.hide_attr(input=c, v=True)
			except:
				pass

		#change gimbal and world ctrl size
		if world:
			cmds.select(world)
			curve_cvs = cmds.ls(cmds.ls(sl=True)[0] + ".cv[0:]", fl=True)
			cmds.scale(size*1.25, size*1.25, size*1.25, curve_cvs)
		if gimbal:
			cmds.select(gimbal)
			curve_cvs = cmds.ls(cmds.ls(sl=True)[0] + ".cv[0:]", fl=True)
			cmds.scale(size*0.75, size*0.75, size*0.75, curve_cvs)

		return {'ctrl':ctrl,
				'root':root,
				'world':world,
				'gimbal':gimbal}

	#----------------------------------------------------------------------------------------------------------------

	def match(self, this = '', that = '' ,t = True, r = True, s = True):
		"""Match two transforms with desired transform, rotate, or scale.

		Args:
			this (str): Item to move.
			that (str): Item with desired position.
			t (bool): Match translate if True.
			r (bool): Match rotate if True.
			s (bool): Match scale if True.

		Returns:
			None

		Notes:
			- This function moves the 'this' transform to match the position, rotation, and scale of the 'that' transform.
			- The 't' parameter controls whether translation is matched.
			- The 'r' parameter controls whether rotation is matched.
			- The 's' parameter controls whether scale is matched.

		Examples:
			# Match the position and rotation of transform 'obj2' to transform 'obj1'.
			match(this='obj1', that='obj2', t=True, r=True, s=False)

			# Match the scale of transform 'obj3' to transform 'obj4'.
			match(this='obj4', that='obj3', t=False, r=False, s=True)
		"""

		if (t):
			cmds.delete(cmds.pointConstraint(that, this, mo =False))
		if (r):
			cmds.delete(cmds.orientConstraint(that, this, mo =False))
		if (s):
			cmds.delete(cmds.scaleConstraint(that, this, mo =False))

		return None

	#----------------------------------------------------------------------------------------------------------------
	def switch_constraints(self, this = '', that = '', main = '', attr = ''):
		"""Create a switch between 3 chains for IK/FK setups.

		Args:
		    this (str): IK joint (can be any transform).
		    that (str): FK joint (can be any transform).
		    main (str): Main joint that switches between.
		    attr (str): Attribute to use as a switch parent.

		Returns:
		    None

		Notes:
		    - This function creates a switch between IK and FK chains in an IK/FK setup.
		    - The 'this' parameter represents the IK joint.
		    - The 'that' parameter represents the FK joint.
		    - The 'main' parameter represents the IK main joint that switches between IK and FK.
		    - The 'attr' parameter specifies the attribute to use as a switch parent.
		    - The function creates a parent constraint and a scale constraint for the 'main' joint, and connects them to the switch attribute.
		    - It also creates a reverse node to invert the switch attribute's value for the parent constraint.
		    - The resulting setup allows switching between IK and FK by controlling the 'attr' attribute.

		Examples:
		    # Create a switch between IK and FK chains using 'switchAttr' as the switch parent attribute.
		    switch_constraints(this='ikJoint', that='fkJoint', main='ikMainJoint', attr='switchAttr')
		"""


		#create shortest parentContraint
		contraint = cmds.parentConstraint(this,that, main, mo =True)[0]
		cmds.setAttr('{}.interpType'.format(contraint), 2)
		
		#Create nodes and connect to switch
		reverse= cmds.shadingNode('reverse', asUtility = True, n = '{}_Reverse'.format(this))

		cmds.connectAttr('{}'.format(attr), '{}_parentConstraint1.{}W1'.format(main,that), f =True)
		cmds.connectAttr('{}'.format(attr), '{}.inputX'.format(reverse), f = True)
		cmds.connectAttr('{}.outputX'.format(reverse), '{}_parentConstraint1.{}W0'.format(main,this), f =True)


		#connect scale
		cmds.scaleConstraint(this,that, main, mo =True)[0]
		
		#Create nodes and connect to switch
		reverse2 = cmds.shadingNode('reverse', asUtility = True, n = '{}_Reverse'.format(this))

		cmds.connectAttr('{}'.format(attr), '{}_scaleConstraint1.{}W1'.format(main,that), f =True)
		cmds.connectAttr('{}'.format(attr), '{}.inputX'.format(reverse2), f = True)
		cmds.connectAttr('{}.outputX'.format(reverse2), '{}_parentConstraint1.{}W0'.format(main,this), f =True)

		self.put_inside_rig_container([reverse, reverse2])

	#----------------------------------------------------------------------------------------------------------------
	def switch_blend_colors(self, this = '', that = '', main = '', attr = ''):
		"""Create a switch between 3 chains for IK/FK setups using color blending.

		Args:
		    this (str): IK joint (can be any transform).
		    that (str): FK joint (can be any transform).
		    main (str): Main joint that switches between.
		    attr (str): Attribute to use as a switch parent.

		Returns:
		    None

		Notes:
		    - This function creates a switch between IK and FK chains in an IK/FK setup using color blending.
		    - The 'this' parameter represents the IK joint.
		    - The 'that' parameter represents the FK joint.
		    - The 'main' parameter represents the IK main joint that switches between IK and FK.
		    - The 'attr' parameter specifies the attribute to use as a switch parent.
		    - The function creates blendColors nodes to blend the transform attributes of 'this' and 'that' based on the switch attribute.
		    - It connects the blended color outputs to the corresponding transform attributes of the 'main' joint.
		    - The resulting setup allows switching between IK and FK by controlling the 'attr' attribute.

		Examples:
		    # Create a switch between IK and FK chains using 'switchAttr' as the switch parent attribute.
		    switch_blend_colors(this='ikJoint', that='fkJoint', main='MainJoint', attr='switchAttr')
		"""

		attrs = ['translate', 'rotate', 'scale']

		for a in attrs:
		#create blend node
			blend_node = cmds.shadingNode('blendColors' , asUtility = True, n = '{}_{}{}'.format(this, a, self.nc['blend']))

			#connect to blend node
			cmds.connectAttr('{}.{}.{}X'.format(this, a, a), '{}.color1.color1R'.format(blend_node), f=1)
			cmds.connectAttr('{}.{}.{}Y'.format(this, a, a), '{}.color1.color1G'.format(blend_node), f=1)
			cmds.connectAttr('{}.{}.{}Z'.format(this, a, a), '{}.color1.color1B'.format(blend_node), f=1)

			cmds.connectAttr('{}.{}.{}X'.format(that, a, a), '{}.color2.color2R'.format(blend_node), f=1)
			cmds.connectAttr('{}.{}.{}Y'.format(that, a, a), '{}.color2.color2G'.format(blend_node), f=1)
			cmds.connectAttr('{}.{}.{}Z'.format(that, a, a), '{}.color2.color2B'.format(blend_node), f=1)

			cmds.connectAttr('{}'. format(attr), '{}.blender'.format(blend_node), f=1)

			#connect to main
			cmds.connectAttr('{}.output.outputR'.format(blend_node), '{}.{}.{}X'.format(main, a, a), f=1)
			cmds.connectAttr('{}.output.outputG'.format(blend_node), '{}.{}.{}Y'.format(main, a, a), f=1)
			cmds.connectAttr('{}.output.outputB'.format(blend_node), '{}.{}.{}Z'.format(main, a, a), f=1)

			self.put_inside_rig_container([blend_node])

	#----------------------------------------------------------------------------------------------------------------
	def new_attr(self, input= '', name = 'switch', min = 0 , max = 1, default = 0):
		"""Create a new double attribute on a transform.

		Args:
			input (str): Name of the transform to add the attribute to. If not specified, it will use the currently selected object.
			name (str): Name of the new attribute.
			min (int): Minimum value for the attribute (inclusive).
			max (int): Maximum value for the attribute (inclusive).
			default (int): Default value for the attribute.

		Returns:
			str: Name of the created attribute.

		Notes:
			- This function adds a new double attribute to the specified transform.
			- If 'input' != specified, the function will use the currently selected object.
			- The 'name' parameter specifies the name of the new attribute.
			- The 'min' and 'max' parameters define the range of values for the attribute.
			- The 'default' parameter sets the default value of the attribute.
			- The function sets the added attribute as keyable.

		Examples:
			# Create a new double attribute named 'switch' with a range of 0 to 1 and a default value of 0.
			new_attr(input='myObject', name='switch', min=0, max=1, default=0)
		"""

		#add new attr as float
		cmds.addAttr(input, ln = name, at = 'double', min = min, max = max, dv = default)
		cmds.setAttr('{}.{}'.format(input, name), e = True, keyable = True)

		return '{}.{}'.format(input, name)

	#----------------------------------------------------------------------------------------------------------------
	def new_attr_interger(self, input= '', name = 'switch', min = 0 , max = 1, default = 0):
		"""Create a new integer attribute on a transform.

		Args:
			input (str): Name of the transform to add the attribute to. If not specified, it will use the currently selected object.
			name (str): Name of the new attribute.
			min (int): Minimum value for the attribute (inclusive).
			max (int): Maximum value for the attribute (inclusive).
			default (int): Default value for the attribute.

		Returns:
			str: Name of the created attribute.

		Notes:
			- This function adds a new long (integer) attribute to the specified transform.
			- If 'input' != specified, the function will use the currently selected object.
			- The 'name' parameter specifies the name of the new attribute.
			- The 'min' and 'max' parameters define the range of values for the attribute.
			- The 'default' parameter sets the default value of the attribute.
			- The function sets the added attribute as keyable.

		Examples:
			# Create a new integer attribute named 'switch' with a range of 0 to 1 and a default value of 0.
			new_attr_interger(input='myObject', name='switch', min=0, max=1, default=0)
		"""

		#add new attr as float
		cmds.addAttr(input, ln = name, at = 'long', min = min, max = max, dv = default)
		cmds.setAttr('{}.{}'.format(input, name), e = True, keyable = True)

		return '{}.{}'.format(input, name)

	#----------------------------------------------------------------------------------------------------------------
	
	def new_enum(self, input= '', name = 'switch', enums = 'Hide:Show', keyable=True, long_name=False, default=0):
		"""Create a new enum attribute on a transform.

		Args:
		    input (str): Name of the transform to add the attribute to. If not specified, it will use the currently selected object.
		    name (str): Name of the new attribute.
		    enums (str): Enumerated values separated by a colon (':').
		    keyable (bool): Specifies if the attribute should be keyable (True by default).
		    long_name (bool): Specifies if the attribute name should include the full path (False by default).
		    default: Default value for the attribute.

		Returns:
		    str: Name of the created attribute.

		Notes:
		    - This function adds a new enum attribute to the specified transform.
		    - If 'input' != specified, the function will use the currently selected object.
		    - The 'name' parameter specifies the name of the new attribute.
		    - The 'enums' parameter defines the enumerated values for the attribute, separated by a colon (':').
		    - The 'keyable' parameter determines if the attribute is keyable or not.
		    - The 'long_name' parameter specifies if the attribute name should include the full path or not.
		    - The 'default' parameter sets the default value of the attribute.
		    - The function sets the added attribute as a channel box attribute.
		    - If 'keyable' is set to True, the attribute is also set as keyable.

		Examples:
		    # Create a new enum attribute named 'switch' with values 'Hide' and 'Show'.
		    new_enum(input='myObject', name='switch', enums='Hide:Show')

		    # Create a new enum attribute named 'status' with values 'Pending', 'Processing', and 'Completed',
		    # and make it keyable and a long name attribute.
		    new_enum(input='myObject', name='status', enums='Pending:Processing:Completed', keyable=True, long_name=True)
		"""
		
		#add new attr as float
		cmds.select(input)
		cmds.addAttr(input, ln = name, at = 'enum', en = enums, dv=default)
		cmds.setAttr('{}.{}'.format(input, name), default)
		if keyable:
			cmds.setAttr('{}.{}'.format(cmds.ls(sl=True, l=True)[0], name), e=True, channelBox=True, k=True)
		else:
			cmds.setAttr('{}.{}'.format(input, name), e=True, channelBox=True, k=False)

		if long_name:
			cmds.select(input)
			return '{}.{}'.format(cmds.ls(sl=True, l=True)[0], name)


		return '{}.{}'.format(input, name)

	#----------------------------------------------------------------------------------------------------------------
	
	def new_boolean(self, input= '', name = 'bool', dv = 'True'):
		"""Create a new boolean attribute on a transform.

		Args:
			input (str): Name of the transform to add the attribute to. If not specified, it will use the currently selected object.
			name (str): Name of the new attribute.
			dv (bool): Default value for the attribute (True by default).

		Returns:
			str: Name of the created attribute.

		Notes:
			- This function adds a new boolean attribute to the specified transform.
			- If 'input' != specified, the function will use the currently selected object.
			- The 'name' parameter specifies the name of the new attribute.
			- The 'dv' parameter sets the default value of the attribute.
			- The function sets the added attribute as a channel box attribute.

		Examples:
			# Create a new boolean attribute named 'bool' with a default value of True.
			new_boolean(input='myObject', name='bool', dv=True)

			# Create a new boolean attribute named 'visibility' with a default value of False.
			new_boolean(input='myObject', name='visibility', dv=False)
		"""

		#add new attr as float
		cmds.addAttr(input, ln = name, at = 'bool')
		cmds.setAttr('{}.{}'.format(input, name), e = True, channelBox = True)
		if dv == 'True':
			cmds.setAttr('{}.{}'.format(input, name), 1)
		print (dv)

		return '{}.{}'.format(input, name)

	#----------------------------------------------------------------------------------------------------------------

	def line_attr(self, input = '', name = 'name', lines = 10):
		"""Create a line attribute with a header. _____________ [Name]

		Args:
			input (str): Name of the transform to add the attribute to. If not specified, it will use the currently selected object.
			name (str): Name of the attribute.
			lines (int): Number of lines to create in the attribute's header.

		Returns:
			str: Name of the created attribute.

		Notes:
			- This function creates a line attribute with a header that consists of a series of dashes followed by the attribute name in brackets.
			- If 'input' != specified, the function will use the currently selected object.
			- The 'name' parameter specifies the name of the attribute.
			- The 'lines' parameter determines the number of lines in the header. If the specified number of lines exceeds the maximum available space, the function will reduce it to fit.
			- The function returns the name of the created attribute.

		Examples:
			# Create a line attribute named 'name' with a header of 10 lines.
			line_attr(input='myObject', name='name', lines=10)

			# Create a line attribute named 'description' with a header of 5 lines.
			line_attr(input='myObject', name='description', lines=5)
		"""

		for num in reversed(range(lines)):
			try:
				line_attr = self.new_enum(input= input, name = '_'*num, enums = '{}:'.format(name))
				cmds.setAttr(line_attr,e=True, lock = True)
			except:
				continue

			return line_attr

	#----------------------------------------------------------------------------------------------------------------

	def string_attr(self, input='', name='name', string='string'):
		"""Create a string attribute to store information.

		Args:
		    input (str): Name of the transform to add the attribute to. If not specified, it will use the currently selected object.
		    name (str): Name of the attribute.
		    string (str): Initial string value for the attribute.

		Returns:
		    str: Name of the created attribute.

		Notes:
		    - This function creates a string attribute that can be used to store information.
		    - If 'input' != specified, the function will use the currently selected object.
		    - The 'name' parameter specifies the name of the attribute.
		    - The 'string' parameter sets the initial string value for the attribute.
		    - The function returns the name of the created attribute.

		Examples:
		    # Create a string attribute named 'name' with the initial value 'John'.
		    string_attr(input='myObject', name='name', string='John')

		    # Create a string attribute named 'description' with the initial value 'Object description'.
		    string_attr(input='myObject', name='description', string='Object description')
		"""

		cmds.addAttr(input, ln=name, dt="string")
		cmds.setAttr('{}.{}'.format(input,name), string, type="string")

		return '{}.{}'.format(input,name)


	#----------------------------------------------------------------------------------------------------------------
	def connect_rotate_order(self, input='', object='controller'):
		"""Connect the rotate order attribute of the input object(s) to an attribute in the controller object.

		Args:
		    input (str or list): Name of the transform(s) to connect the rotate order attribute. If not specified, it will use the currently selected object(s).
		    object (str): Name of the controller object where the rotate order attribute will be connected.

		Returns:
		    str: Name of the rotate order attribute in the controller object.

		Notes:
		    - This function connects the rotate order attribute of the input object(s) to an attribute in the controller object.
		    - If 'input' != specified, the function will use the currently selected object(s).
		    - The 'object' parameter specifies the name of the controller object where the rotate order attribute will be connected.
		    - If the rotate order attribute already exists in the controller object, it will be made keyable.
		    - If the rotate order attribute doesn't exist in the controller object, it will be created as an enum attribute with the rotate order values.
		    - The function returns the name of the rotate order attribute in the controller object.

		Examples:
		    # Connect the rotate order attribute of 'object1' to the 'RotateOrder' attribute of 'controller'.
		    connect_rotate_order(input='object1', object='controller')

		    # Connect the rotate order attribute of multiple objects to the 'RotationOrder' attribute of 'controller'.
		    connect_rotate_order(input=['object1', 'object2', 'object3'], object='controller')
		"""


		if input != '':
			self.input = [input]
			
		else:	
			self.input = input

		self.check_input('connect_rotate_order')	

		#create the attr if it doesnt exists
		'''
		try:
			self.new_enum(input= object, name = 'RotateOrder', enums = 'xyz:yzx:zxy:xzy:yxz:zyx')
		except:
			cmds.setAttr('{}.RotateOrder'.format(object), e = True, channelBox = True)
		'''
		if cmds.attributeQuery('RotateOrder', node=object, exists=True):
			cmds.setAttr('{}.RotateOrder'.format(object), k=True)
		else:
			self.new_enum(input= object, name = 'RotateOrder', enums='xyz:yzx:zxy:xzy:yxz:zyx')
			cmds.setAttr('{}.RotateOrder'.format(object), e=True, channelBox=True)
			cmds.setAttr('{}.RotateOrder'.format(object), k=True)
		#connect attr
		for input in self.input:
			cmds.connectAttr('{}.RotateOrder'.format(object), '{}.rotateOrder'.format(input), f = True)

		return '{}.RotateOrder'.format(object)

	#----------------------------------------------------------------------------------------------------------------

	def duplicate_change_names(self, input = '', hi = True, search='_Jnt', replace ='_dup', remove_end_number=True):
		"""Duplicate the hierarchy with clean names, ensuring no duplicated names in the duplicated hierarchy.

		Args:
		    input (str or list): Name of the transform(s) to duplicate. If not specified, it will use the currently selected object(s).
		    hi (bool): If True, duplicate the entire hierarchy. If False, duplicate only the selected object(s).
		    search (str): String to search for in the names of the duplicated objects.
		    replace (str): String to replace the search string with in the names of the duplicated objects.

		Returns:
		    str: Name of the duplicated[0] transform.

		Notes:
		    - This function duplicates the specified hierarchy or selected objects.
		    - The duplicated objects have their names cleaned to ensure no duplicated names in the duplicated hierarchy.
		    - The 'input' parameter specifies the name of the transform(s) to duplicate. If not specified, it will use the currently selected object(s).
		    - The 'hi' parameter controls whether to duplicate the entire hierarchy (hi=True) or only the selected objects (hi=False).
		    - The 'search' parameter is used to find the string to be replaced in the names of the duplicated objects.
		    - The 'replace' parameter is the string that will replace the search string in the names of the duplicated objects.
		    - The function returns the name of the duplicated[0] transform.

		Examples:
		    # Duplicate the hierarchy with clean names, replacing '_Jnt' with '_dup'.
		    duplicate_change_names(input='rootJoint', hi=True, search='_Jnt', replace='_dup')

		    # Duplicate the selected objects with clean names, replacing '_Ctrl' with '_Copy'.
		    duplicate_change_names(input=['ctrl1', 'ctrl2', 'ctrl3'], hi=False, search='_Ctrl', replace='_Copy')
		"""
		
		if input == '':
			self.input = cmds.ls(sl=True)
		
		else:
			self.input = input

		#error if search dont exists
		#duplicate and search and replace names
		if hi == True:
			cmds.select(self.input, hi =True)
		else:
			cmds.select(self.input, hi =False)

		new_transforms = cmds.duplicate()

		return_list = []
		
		new_name = self.replace_name(new_transforms,search, replace, hi)
		return_list.append(new_name)

		#remove 1 from firt duplicated joint
		if remove_end_number:
			for name in  return_list[-1]:
				if '{}'.format(name)[-1] == str(1):
					cmds.rename('{}'.format(name),'{}'.format(name[:-1]) )
					return_list[-1][0] = '{}'.format(name[:-1])
		'''
		for jnt in cmds.listRelatives(return_list[-1], ad=True):
			try:
				if cmds.nodeType(jnt) == 'joint':
					parent = cmds.listRelatives(jnt, p=True)
					if parent:
						cmds.parent(jnt, w=True)
						cmds.parent(jnt, parent[0])
			except:
				pass
		'''

		#return list
		return return_list[-1]

	#----------------------------------------------------------------------------------------------------------------

	def bounding_cube(self, input = '', size = 1, name = '', axis = setup['twist_axis']):
		"""Create a control cube with coverage for the full limb, resembling a bounding box in length.

	   Args:
		   input (str or list): Name of the transform(s) to use as input. If not specified, it will use the currently selected object(s).
		   size (float): Size of the control cube.
		   name (str): Name of the cube. If not specified, a default name will be used.
		   axis (str): Axis to aim the control cube towards. Valid values are 'X', 'Y', or 'Z'. By default, it reads the value from the setup dictionary.

	   Returns:
		   str: Name of the created control cube.

	   Notes:
		   - This function creates a control cube that covers the full limb.
		   - The 'input' parameter specifies the name of the transform(s) to use as input. If not specified, it will use the currently selected object(s).
		   - The 'size' parameter controls the size of the control cube.
		   - The 'name' parameter allows specifying a custom name for the control cube. If not specified, a default name will be used.
		   - The 'axis' parameter determines the axis to aim the control cube towards. Valid values are 'X', 'Y', or 'Z'. By default, it reads the value from the setup dictionary.
		   - The function returns the name of the created control cube.

	   Examples:
		   # Create a control cube with a size of 2, aiming towards the Y axis.
		   bounding_cube(input='limb_1', size=2, axis='Y')

		   # Create a control cube with the default size, aiming towards the Z axis.
		   bounding_cube(input='limb_2', axis='Z')
	   """

		#turn off soft selection
		cmds.softSelect(e=True, softSelectEnabled = False)

		#get correct input
		if input != '':
			self.input = [input]
			
		else:	
			self.input = input

		self.check_input('bounding_cube')	

		# get children of input
		original = self.input[0]
		children = cmds.listRelatives(self.input, c = True)
		print (children)
		#create a cube
		cmds.select(self.input)
		if name == '':
			cube = self.curve(type = 'cube',  size = size, gimbal = False)
		else:
			cube = self.curve(type = 'cube', custom_name = True, name = name, size = size)

		#move vertex to start and move vertex to finish
		#input_position = cmds.xform(original, q = True, m= True, ws = True)
		#input_child_position = cmds.xform(children, q = True, m= True, ws = True)
		
		#createl cluster per side to locate them
		#make sure it works on any axis
		if axis == 'X':
			cmds.select('{}.cv[0]'.format(cube),'{}.cv[3:5]'.format(cube),'{}.cv[11:12]'.format(cube), '{}.cv[14:15]'.format(cube))
			up_side = cmds.cluster()
			cmds.select('{}.cv[1:2]'.format(cube),'{}.cv[6:10]'.format(cube),'{}.cv[13]'.format(cube))
			down_side = cmds.cluster()
		elif axis == 'Y':
			cmds.select('{}.cv[5:6]'.format(cube),'{}.cv[9:14]'.format(cube))
			up_side = cmds.cluster()
			cmds.select('{}.cv[0:4]'.format(cube),'{}.cv[7:8]'.format(cube),'{}.cv[15]'.format(cube))
			down_side = cmds.cluster()			
		else: 
			cmds.select('{}.cv[2:3]'.format(cube),'{}.cv[8:9]'.format(cube),'{}.cv[11:12]'.format(cube), '{}.cv[12:15]'.format(cube))
			up_side = cmds.cluster()
			cmds.select('{}.cv[0:1]'.format(cube),'{}.cv[4:7]'.format(cube),'{}.cv[10:11]'.format(cube))
			down_side = cmds.cluster()	

		#move locator to correct pos
		self.match(up_side, original, r = False)
		if children == None:
			pass
		else:
			self.match(down_side, children, r = False)

		#delete history
		cmds.delete(cube, ch = True)

		#return the cube
		cmds.select(cube)
		return cube

	#----------------------------------------------------------------------------------------------------------------
	def shape_with_attr(self, input = '', obj_name = 'Switch', attr_name = 'Switch'):
		"""Create a shape with an attribute and place it inside all the input transforms.

		This function is used to have an IK/FK switch on all the controls by adding a shape with the specified attribute.

		Args:
			input (str or list): Name of the transform(s) to use as input. If not specified, it will use the currently selected object(s).
			obj_name (str): Name of the transform to put the shape in.
			attr_name (str): Name of the attribute.

		Returns:
			str: Name of the created attribute.

		Notes:
			- This function creates a shape with the specified attribute and places it inside all the input transforms.
			- The 'input' parameter specifies the name of the transform(s) to use as input. If not specified, it will use the currently selected object(s).
			- The 'obj_name' parameter determines the name of the transform to put the shape in.
			- The 'attr_name' parameter specifies the name of the attribute to create.
			- If the shape already has the attribute, it will not be created again.
			- The function returns the name of the created attribute.

		Examples:
			# Create a shape with the 'Switch' attribute and place it inside the 'ctrl' transform.
			shape_with_attr(input='limb_1', obj_name='ctrl', attr_name='Switch')

			# Create a shape with the default attribute name and place it inside the selected transforms.
			shape_with_attr()
		"""

		#get correct input as list
		if input != '':
			self.input = [input]
			
		else:	
			self.input = input

		self.check_input('shape_with_attr')	

		#print initial statement
		print ('adding loc to {}'.format(self.input))

		#create a dummy loc
		if cmds.objExists(obj_name + self.nc['locator']):
			loc_shape = obj_name + self.nc['locator']
		else:
			loc = cmds.spaceLocator(n = obj_name + self.nc['locator'])
			loc_shape = cmds.pickWalk(d ='down')[0]
			loc = loc[0]

		#hide unwanted attrs
		hide_this_attrs = ['lpx','lpy','lpz','lsx','lsy','lsz']
		for attr in hide_this_attrs:
			try: cmds.setAttr("{}.{}".format(loc_shape, attr), lock=True, channelBox=False, keyable=False)
			except: print ('shape_with_attr info: no rotate order atttr found')

		cmds.setAttr("{}.visibility".format(loc_shape), 0)

		#add new attr to the shape if it doesnt exists
		if attr_name:
			try:
				if cmds.attributeQuery(attr_name, node=loc_shape, exists=True):
					pass
				else:
					self.line_attr(input= loc_shape, name = 'MT')
					cmds.addAttr(loc_shape, ln= attr_name, max=1, dv=0, at='double', min=0)
					cmds.setAttr('{}.{}'.format(loc_shape, attr_name), e=1, keyable=True)
			except:
				pass

		#put the shape in all the transforms inputs
		for transform in self.input:
			cmds.parent(loc_shape, transform, s = True, add = True)

		#try to delete the loc transform if it still exists
		try:cmds.delete(loc)
		except:pass

		loc_shape = cmds.rename(loc_shape, obj_name + self.nc['locator'])

		return obj_name + self.nc['locator'] + '.' + attr_name


	#----------------------------------------------------------------------------------------------------------------				
	def text_curves(self, name_text = 'Name', font = 'Arial', color = setup['main_color']):
		"""Create text curves.

		This function creates text curves based on the specified parameters.

		Args:
		    name_text (str): Text to be curved.
		    font (str): Desired font.
		    color (str): Color of the curves.

		Returns:
		    str: Name of the created curve.

		Notes:
		    - The 'name_text' parameter specifies the text to be curved.
		    - The 'font' parameter determines the desired font.
		    - The 'color' parameter specifies the color of the curves.
		    - The function returns the name of the created curve.

		Examples:
		    # Create text curves with the specified name, font, and color.
		    text_curves(name_text='Hello', font='Arial', color='red')

		    # Create text curves with default parameters.
		    text_curves()
		"""

		#BASED ON OLD ONE in RDM Tools V1 (Sorry for the spanish i just copy paste it)

		#Im deleting one node so if theres one already in the scene i dont want to delete it
		if cmds.objExists('makeTextCurves1'):
			cmds.rename ('makeTextCurves1','makeTextCurves1LOL')

		#Lets Create some curves
		Texto = '_'+ name_text
		Color = color

		LetrasDobles = []

		Text = cmds.textCurves (n= Texto, t = Texto, o = True, f = font)
		Lista= cmds.listRelatives (Text, ad = True)

		#print Lista
		Shape = Lista[1]
		#print Shape
		cmds.delete ('makeTextCurves1')
		for Curva in Lista:
			if cmds.objectType(str(Curva), isType='nurbsCurve'):
				#print Curva
				#Get Parents
				curvaPapa = cmds.listRelatives(Curva, p = True)
				#print 'Curva papa ' + str(curvaPapa)
				curvaAbuelo = cmds.listRelatives(curvaPapa, p = True)
				#print 'curva Abuelo '+(curvaAbuelo[0])

				#letters like e and o have 2 curves instead of 1
				DobleCurva = cmds.listRelatives(curvaAbuelo)

				if len(DobleCurva)==2:

					#print 'DobleCurva ' + str(DobleCurva)
					LetrasDobles.append (Curva)

				else:
					#parent to first shape
					if not Shape == curvaPapa[0]:
						cmds.makeIdentity (curvaAbuelo, a = True, t = True , r = True)
						cmds.parent (Curva, Shape, r = True, s = True)

					#Colores
					cmds.setAttr (Curva+'.overrideEnabled', 1)
					self.assign_color(Curva, color = color)
					cmds.setAttr('{}.lineWidth'.format(Curva), int(setup['line_width']))


		#Do stuff for the Double Letters
			#print LetrasDobles
		for dl in LetrasDobles:
			dlPapa = cmds.listRelatives (dl, p = True)
			dlAbuelo = cmds.listRelatives (dlPapa, p = True)
			cmds.makeIdentity (dlAbuelo, a = True, t = True , r = True)
			cmds.parent(dl, Shape, r = True, s = True)
			self.assign_color(dl, color = color)
			cmds.setAttr('{}.lineWidth'.format(dl), int(setup['line_width']))

		#Organizing
		cmds.parent (Shape, w = True)
		cmds.rename (Shape, Texto + str(self.nc['ctrl']))
		cmds.delete(Text[0])
		cmds.delete (Texto + str(self.nc['ctrl']+'Shape'))
		cmds.move (-0.5,0,0, r = True)
		cmds.xform(cp= True)
		#cmds.rename(name_text + self.nc['curve'])

		return name_text + self.nc['curve']
			

	#----------------------------------------------------------------------------------------------------------------		

	def curve_between(self, start, end):
		"""Create a 1D curve between two transforms.

		This function creates a linear curve between two transforms.

		Args:
			start (str): Name of the first transform.
			end (str): Name of the second transform.

		Returns:
			str: Name of the created curve.

		Notes:
			- The created curve is a linear curve with two control points.
			- The curve is created in world space.

		Examples:
			# Create a curve between two transforms.
			curve_between('joint1', 'joint2')
		"""

		#create a simple linear curve between 2 joints 
	   
		pos_a = cmds.xform(start, q=True,t=True, ws=True)
		pos_b = cmds.xform(end, q=True,t=True, ws=True) 
	   
		crv = cmds.curve(d=1, p=[pos_a,pos_b], k=[0,1], n = '{}{}'.format(start, self.nc['curve']))
	   
		return crv

	#----------------------------------------------------------------------------------------------------------------		
	
	def nurbs_between(self, start, end):
		"""Create a NURBS plane between two transforms.

		This function creates a NURBS plane between two transforms.

		Args:
		    start (str): Name of the start transform.
		    end (str): Name of the end transform.

		Returns:
		    str: Name of the created NURBS plane.

		Notes:
		    - The created NURBS plane is a single-span surface.
		    - The NURBS plane is created with a degree of 1 (linear).
		    - The surface is created without construction history.
		    - Two clusters are created to control the surface CVs and are positioned on the start and end transforms.

		Examples:
		    # Create a NURBS plane between two transforms.
		    nurbs_between('joint1', 'joint2')
		"""

		#creates a nurbs plane between 2 transforms
		
		name = start.replace(self.nc['joint'], '') +'_'+ end.replace(self.nc['joint'], '')+ self.nc['nurb']  
		surface = cmds.nurbsPlane(d = 1, ch = False, n = name)[0]
		temp_cluster1 = cmds.cluster('{}.cv[0:1][0]'.format(surface))
		temp_cluster2 = cmds.cluster('{}.cv[0:1][1]'.format(surface))

		cmds.delete(cmds.parentConstraint(start,temp_cluster1, mo =False))
		cmds.delete(cmds.parentConstraint(end,temp_cluster2, mo =False))
		cmds.delete(surface, constructionHistory = True)
		
		return surface
		

	#----------------------------------------------------------------------------------------------------------------		

	def nurbs_between_trio(self, start, mid, end):
		"""Create a NURBS plane between three transforms.

		This function creates a NURBS plane between three transforms.

		Args:
		    start (str): Name of the start transform.
		    mid (str): Name of the mid transform.
		    end (str): Name of the end transform.

		Returns:
		    str: Name of the created NURBS plane.

		Notes:
		    - The created NURBS plane is a single-span surface.
		    - The NURBS plane is created with a degree of 1 (linear).
		    - The surface is created without construction history.
		    - Three clusters are created to control the surface CVs, positioned on the start, mid, and end transforms.

		Examples:
		    # Create a NURBS plane between three transforms.
		    nurbs_between_trio('joint1', 'joint2', 'joint3')
		"""
		#creates a nurbs plane between 3 transforms

		name = start.replace(self.nc['joint'], '') +'_'+ end.replace(self.nc['joint'], '')+ self.nc['nurb']
		surface = cmds.nurbsPlane(d = 1, ch = False, n = name)[0]
		temp_cluster1 = cmds.cluster('{}.cv[0][0:1]'.format(surface))
		temp_cluster2 = cmds.cluster('{}.cv[1][0:1]'.format(surface))
		temp_cluster3 = cmds.cluster('{}.cv[2][0:1]'.format(surface))

		cmds.delete(cmds.parentConstraint(start,temp_cluster1, mo =False))
		cmds.delete(cmds.parentConstraint(mid,temp_cluster2, mo =False))
		cmds.delete(cmds.parentConstraint(end,temp_cluster2, mo =False))
		cmds.delete(surface, constructionHistory = True)

		return surface

	#----------------------------------------------------------------------------------------------------------------		

	def create_ik_spline_twist(self, start, end, curve):
		"""Create an IK spline based on two joints and one curve.

		This function creates an IK spline handle using the specified start and end joints
		and a curve as the spline shape.

		Args:
		    start (str): Name of the first joint.
		    end (str): Name of the last joint.
		    curve (str): Name of the curve to be used as the spline shape.

		Returns:
		    dict: A dictionary containing the names of the IK handle, effector, and curve.

		Notes:
		    - The IK handle is created using the 'ikSplineSolver' solver type.
		    - The created IK handle, effector, and curve are renamed using the specified naming conventions.

		Examples:
		    # Create an IK spline handle between two joints using a curve.
		    create_ik_spline_twist('joint1', 'joint2', 'curve1')
		"""

		# ik spline solver
		ikSpline = cmds.ikHandle(sj=start,
								 ee=end,
								 sol='ikSplineSolver',
								 n=start + '_Twist' + self.nc['ik_spline'],
								 c = curve,
								 ccv=False,
								 pcv = False)

		effector_spline = cmds.rename(ikSpline[1], start + '_Twist' + self.nc['effector'])
		ikSpline = ikSpline[0]
		spline_curve = ikSpline[2]

		return {'ikHandle': ikSpline, 'effector': effector_spline, 'curve': spline_curve}

	#----------------------------------------------------------------------------------------------------------------		

	def connect_md_node(self, in_x1 = '', in_x2 = 1.0, out_x = '', mode = 'mult', name = '', force = False, vector = False):
		"""Create a multiplyDivide node to connect inputs and outputs.

		This function creates a multiplyDivide node and connects the specified input attributes
		to the input1 and input2 of the node. It also connects the output of the node to the
		specified output attribute.

		Args:
			in_x1 (str or int or float): Attribute or value to connect to input1X.
			in_x2 (str or int or float): Attribute or value to connect to input2X.
			out_x (str): Attribute to connect the multiplyDivide output.
			mode (str): Operation mode of the multiplyDivide node ('mult', 'divide', or 'power').
			name (str): Name of the node (optional).
			force (bool): Force the connection if needed (default: False).
			vector (bool): Connect input and output attributes as vector (default: False).

		Returns:
			str: Name of the created multiplyDivide node.

		Notes:
			- The created multiplyDivide node can perform multiplication, division, or power operations.
			- The input and output connections can be forced if specified.
			- If `vector` is True, the input and output connections will be treated as vector attributes.

		Examples:
			# Create a multiplyDivide node and connect attributes.
			connect_md_node('attr1.attr', 'attr2.attr', 'result.attr', 'mult')

			# Create a multiplyDivide node with constant values and connect attributes.
			connect_md_node(2.0, 0.5, 'result.attr', 'mult')

			# Create a multiplyDivide node with a vector attribute and connect attributes.
			connect_md_node('vector1.attr', 'vector2.attr', 'result.attr', 'mult', vector=True)
		"""

		if name == '':
			try:
				name = in_x1.split('.')[0]
			except:
				name = in_x2.split('.')[0]

		#create md node with correct value and mode
		md_node = cmds.shadingNode('multiplyDivide', asUtility=1, n  = '{}{}'.format(name, self.nc['multiplyDivide']))

		if mode == 'divide':
			cmds.setAttr(str(md_node)+'.operation', 2)
		elif mode == 'power':
			cmds.setAttr(str(md_node) + '.operation', 3)
		else:
			cmds.setAttr(str(md_node)+'.operation', 1)

		#connect md node
		#check input 1x
		if isinstance(in_x1, int) == True:
			cmds.setAttr(str(md_node)+'.input1X', in_x1)
		elif isinstance(in_x1, float) == True:
			cmds.setAttr(str(md_node)+'.input1X', in_x1)
		else:
			if vector:
				try:
					cmds.connectAttr(in_x1, '{}.input1'.format(md_node), f=True)
				except:
					cmds.connectAttr(in_x1, '{}.input1X'.format(md_node), f=True)
					cmds.connectAttr(in_x1, '{}.input1Y'.format(md_node), f=True)
					cmds.connectAttr(in_x1, '{}.input1Z'.format(md_node), f=True)

			else:
				cmds.connectAttr(in_x1, '{}.input1.input1X'.format(md_node), f=True)

		#check input 2x
		if isinstance(in_x2, int) == True:
			cmds.setAttr(str(md_node)+'.input2X', in_x2)
		elif isinstance(in_x2, float) == True:
			cmds.setAttr(str(md_node)+'.input2X', in_x2)
		else:
			if vector:
				try:
					cmds.connectAttr(in_x2, '{}.input2'.format(md_node), f=True)
				except:
					cmds.connectAttr(in_x2, '{}.input2.input2X'.format(md_node), f=True)
					cmds.connectAttr(in_x2, '{}.input2.input2Y'.format(md_node), f=True)
					cmds.connectAttr(in_x2, '{}.input2.input2Z'.format(md_node), f=True)

			else:
				cmds.connectAttr(in_x2, '{}.input2.input2X'.format(md_node), f=True)

		#connect output
		if out_x == '':
			return md_node

		if force:
			if vector:
				cmds.connectAttr('{}.output'.format(md_node), out_x, f=True)
			else:
				cmds.connectAttr('{}.output.outputX'.format(md_node), out_x, f=True)

		else:
			if vector:
				cmds.connectAttr('{}.output'.format(md_node), out_x)
			else:
				cmds.connectAttr('{}.output.outputX'.format(md_node), out_x)

		self.put_inside_rig_container([md_node])

		#return node
		return md_node

	#----------------------------------------------------------------------------------------------------------------

	def transform_on_sel(self, transform='', name='Temp'):
		"""Position a transform node based on the selection.

		This function positions a transform node based on the selected objects.
		If no transform node is specified, it will create a joint.

		Args:
		    transform (str): Name of the transform node to position (optional).
		    name (str): Name of the transform node or joint (default: 'Temp').

		Returns:
		    None

		Notes:
		    - If no transform node is specified, it will create a joint with the given name.
		    - The transform node will be positioned based on the selected objects.
		"""

		
		cluster = cmds.cluster(n='temp'+self.nc['cluster'])
		print (cluster)
		#cluster = cmds.rename(cluster,str(cluster[1]).replace('Handle', self.nc['cluster_handle']))

		#create if no input
		if transform == '':
			cmds.select(cl=True)
			transform = cmds.joint(n=name+self.nc['joint'])
		
		#put input in desire location
		cmds.delete(cmds.parentConstraint(cluster[1], transform, mo=False))

	#----------------------------------------------------------------------------------------------------------------
	def connect_with_line(self, start='', end=''):
		"""Create a non-selectable curve between two objects (Pole Vectors Lines).

		This function creates a curve between two objects, commonly used for pole vectors lines.
		If no start and end transforms are provided, it will use the currently selected objects.

		Args:
			start (str): Name of the start transform (optional).
			end (str): Name of the end transform (optional).

		Returns:
			List[str]: List of created assets (curve and clusters).

		Notes:
			- If no start and end transforms are provided, it will use the currently selected objects.
			- The curve is created using the `curve_between` function.
			- Clusters are created on CVs 0 and 1 of the curve.
			- Parent constraints are applied to the clusters to attach them to the start and end transforms.
			- The CVs and clusters are cleaned and hidden for a cleaner display.

		Example:
			# Create a curve between two transforms
			connect_with_line('joint1', 'joint2')
		"""

		if start=='':
			sel = cmds.ls(sl=True)
			start = sel[0]
			end = sel[1]

		#create line 
		cv = self.curve_between(start=start, end=end)
		cv = cmds.rename(cv, '{}_{}{}{}'.format(start,end,self.nc['connected'], self.nc['curve']))

		#create clusters on cvs 0 and 1
		cmds.select('{}.cv[0]'.format(cv))
		cluster_start = cmds.cluster(n='{}{}'.format(start,self.nc['cluster']))
		cmds.select('{}.cv[1]'.format(cv))
		cluster_end = cmds.cluster(n='{}{}'.format(end,self.nc['cluster']))

		#create aprents constrains to clusters
		cmds.parentConstraint(start, cluster_start)
		cmds.parentConstraint(end, cluster_end)

		#clean and hide cv and clusters
		cmds.setAttr("{}.inheritsTransform".format(cv), 0)

		cmds.setAttr("{}.overrideEnabled".format(cv), 1)
		cmds.setAttr("{}.overrideDisplayType".format(cv), 2)

		cmds.setAttr('{}.v'.format(cluster_start[1]), 0)
		cmds.setAttr('{}.v'.format(cluster_end[1]), 0)

		connect_with_line_assets = [cv, cluster_start[1], cluster_end[1]]

		cmds.parent(cluster_start[1], cluster_end[1],cv)

		return connect_with_line_assets

	#----------------------------------------------------------------------------------------------------------------
	def lock_node(self, input = '', unlock=False):
		"""Lock or unlock nodes.

		This function allows you to lock or unlock nodes. If no input is specified, it will use the currently selected nodes.

		Args:
		    input (str or List[str]): Node or list of nodes to lock or unlock (optional).
		    unlock (bool): True to unlock nodes, False to lock nodes.

		Returns:
		    None

		Notes:
		    - If no input is specified, it will use the currently selected nodes.
		    - When unlocking nodes, the `lockNode` command is called with `lock=False`.
		    - When locking nodes, the `lockNode` command is called with `lock=True`.

		Example:
		    # Lock selected nodes
		    lock_node()

		    # Unlock specified nodes
		    lock_node(['node1', 'node2'], unlock=True)
		"""

		if input == '':
			input = cmds.ls(sl=True)
		
		for node in input:
			if unlock ==True:
				cmds.lockNode(node, lock=False)
			else:
				cmds.lockNode(node, lock=True)


	#----------------------------------------------------------------------------------------------------------------

	def replace_connection_with_doublelinear(self, input = '', attr = '', name = 'DoubleLinear'):
		"""Add a double linear node between two nodes.

		This function adds a double linear node between two nodes to replace an existing connection.

		Args:
		    input (str): Node or attribute to replace the connection (optional).
		    attr (str): Attribute to connect the double linear node (optional).
		    name (str): Name of the double linear node (optional).

		Returns:
		    str: Name of the double linear node.

		Notes:
		    - If no input is specified, it will use the selection.
		    - The function creates a double linear node using the 'addDoubleLinear' shading node.
		    - It retrieves the connection to replace based on the input node and attribute.
		    - The connection is established between the retrieved connection and the input of the double linear node.
		    - The output of the double linear node is connected to the specified attribute of the input node.
		    - The double linear node is added to the rig container.

		Example:
		    # Replace connection with a double linear node
		    replace_connection_with_doublelinear()

		    # Replace connection with a double linear node on a specific attribute
		    replace_connection_with_doublelinear(input='node1', attr='translateX', name='DLNode')
		"""

		double_linear = cmds.shadingNode('addDoubleLinear', asUtility=True, name = name)
		connection_to_replace = cmds.listConnections('{}.{}'.format(input,attr), p=True)[0]
		print (connection_to_replace)
		cmds.connectAttr('{}'.format(connection_to_replace), '{}.input1'.format(double_linear), f=True)
		cmds.connectAttr('{}.output'.format(double_linear), '{}.{}'.format(input,attr), f=True)
		self.put_inside_rig_container([double_linear])

		return double_linear

	#----------------------------------------------------------------------------------------------------------------

	def write_json(self, path, json_file, data):
		"""Write data to a JSON file.

		This function writes the specified data to a JSON file.

		Args:
		    path (str): Path to the folder where the JSON file will be located (use '\\' to define folders).
		    json_file (str): Name of the JSON file.
		    data (dict): Data to be saved in the JSON file.

		Returns:
		    str: Full path of the JSON file.

		Notes:
		    - The function uses the `os.path.join()` function to construct the full path of the JSON file.
		    - The data is written to the file using the `json.dump()` function.
		    - The `ensure_ascii`, `indent`, and `sort_keys` parameters are set to `False`, `4`, and `False` respectively
		      for better formatting and readability of the JSON file.
		    - The full path of the JSON file is returned.

		Example:
		    # Write data to a JSON file
		    write_json("C:\\data", "output.json", {"name": "John", "age": 30})
		"""
		write_json = os.path.join(path, json_file)

		with open(write_json, 'w', encoding='utf-8') as f:
			json.dump(data, f, ensure_ascii=False, indent=4, sort_keys = False)

		print(write_json)
		return write_json

	#----------------------------------------------------------------------------------------------------------------

	def read_json(self, path, json_file):
		"""Read data from a JSON file.

		This function reads the data from the specified JSON file and returns it as a dictionary.

		Args:
			path (str): Path to the folder where the JSON file is located (use '\\' to define folders).
			json_file (str): Name of the JSON file.

		Returns:
			dict: Dictionary with the data from the JSON file.

		Notes:
			- The function uses the `os.path.join()` function to construct the full path of the JSON file.
			- The data is read from the file using the `json.load()` function.
			- The dictionary with the data is returned.

		Example:
			# Read data from a JSON file
			data = read_json("C:\\data", "input.json")
		"""

		json_data = os.path.join(path, json_file)

		with open(json_data) as f:
			data = json.load(f)

		return data

	#----------------------------------------------------------------------------------------------------------------

	def change_default(self, atrr, default):
		"""Change the default value of an attribute.

		This function changes the default value of the specified attribute to the given value.

		Args:
			attr (str): Name of the attribute to change.
			default: New default value for the attribute.

		Returns:
			None

		Notes:
			- The function uses the `cmds.addAttr()` command with the `e` flag to modify the attribute.
			- The `dv` flag is used to set the new default value for the attribute.

		Example:
			# Change the default value of an attribute
			change_default('myNode.myAttribute', 10.0)
		"""
		cmds.addAttr('{}'.format(atrr), e=1, dv=default)

	#----------------------------------------------------------------------------------------------------------------

	def put_inside_rig_container(self, inputs = []):
		"""Put nodes inside a rig container.

		This function adds the specified nodes to a rig container called "Mutant_Rig". If the container does not exist, it will be created.

		Args:
			inputs (list): List of nodes to add to the rig container.

		Returns:
			None

		Notes:
			- The function checks if the "Mutant_Rig" container exists. If it doesn't, a new container is created using the `cmds.container()` command with the "dagContainer" type.
			- The `addNode` flag of the `cmds.container()` command is used to add the specified nodes to the container.
			- The `iconName` attribute of the container is set to a specific icon path.

		Example:
			# Put nodes inside a rig container
			put_inside_rig_container(['node1', 'node2', 'node3'])
		"""
		if not inputs:
			return False

		if not cmds.objExists('Mutant_Rig'):
			mutant_rig = cmds.container(name='Mutant_Rig', type='dagContainer')
		else:
			mutant_rig = 'Mutant_Rig'

		icon_path = os.path.join(FOLDER, 'Icons', 'LogoWhite03')
		cmds.setAttr('{}.iconName'.format(mutant_rig), icon_path, type='string')

		for input in inputs:
			cmds.container('Mutant_Rig', e=True, addNode=input)

	#----------------------------------------------------------------------------------------------------------------

	def connect_remap_value(self, input_value, output_value, value=0):
		"""Connect a remapValue node to remap an input value to an output value.

		This function creates a remapValue node and connects it between the input value and output value. It allows you to remap the input value to a desired output value range.

		Args:
			input_value (str): Input value attribute to connect.
			output_value (str): Output value attribute to connect.
			value (float): Default output value.

		Returns:
			str: Name of the remapValue node.

		Example:
			# Connect remapValue node
			remap_node = connect_remap_value('input.value', 'output.value', value=0)
		"""
		remap = cmds.shadingNode('remapValue', asUtility=True)
		cmds.connectAttr(input_value, '{}.inputValue'.format(remap), f=True)
		cmds.connectAttr('{}.outValue'.format(remap), output_value, f=True)
		cmds.setAttr('{}.outputMin'.format(remap), value)
		cmds.setAttr('{}.outputMax'.format(remap), value)
		return remap

	#----------------------------------------------------------------------------------------------------------------

	def create_proxy_attr(self, original_attr, output_node, line_on_top=False, line_name = '', new_name=False, name=''):
		"""Create a proxy attribute from a source node to a target node.

		This function copies an attribute from a source node to a target node and creates a proxy attribute that mirrors the source attribute's behavior.

		Args:
			original_attr (str): Original attribute to copy.
			output_node (str): Node where the new attribute will be created.
			line_on_top (bool, optional): Add a line before the new attribute. Defaults to False.
			line_name (str, optional): Name of the line attribute. Defaults to ''.
			new_name (bool, optional): Rename the new attribute. Defaults to False.
			name (str, optional): Name for the new attribute. Defaults to ''.

		Returns:
			str: Name of the new attribute.

		Notes:
			- The function creates a proxy attribute by copying the attribute from the source node to the output node.
			- If line_on_top is set to True, a line attribute will be added before the new attribute.
			- If new_name is set to True, the new attribute will be renamed using the specified name. Otherwise, it will retain the original attribute name.
			- The attribute type, minimum and maximum values, and enumeration options (if applicable) will be preserved in the proxy attribute.

		Examples:
			1. Copying an attribute without renaming:
				create_proxy_attr(original_attr='L_Shoulder_Jnt_Switch_Loc.FK_Arms', output_node='L_Shoulder_Fk_Ctrl')

			2. Copying an attribute and renaming:
				create_proxy_attr(original_attr='L_Shoulder_Jnt_Switch_Loc.FK_Arms', output_node='L_Shoulder_Fk_Ctrl', new_name=True, name='Follow')

			3. Copying an attribute with a line attribute on top:
				create_proxy_attr(original_attr='L_Shoulder_Jnt_Switch_Loc.FK_Arms', output_node='L_Shoulder_Fk_Ctrl', line_on_top=True, line_name='LineAttr')
		"""

		attr = original_attr.split('.')[-1]
		attrs_from = original_attr.split('.')[0]
		ctrl = output_node

		if new_name:
			if not name:
				attr_name = attr
			else:
				attr_name = name
		else:
			attr_name = attr

		if line_on_top:
			self.line_attr(input=output_node, name=line_name)

		cmds.select(attrs_from)
		print(attrs_from, attr)
		if '___' in attr:
			mt.line_attr(input=ctrl, name=cmds.getAttr("{}.{}".format(attrs_from, attr_name), asString=True))
			return

		print('{}.{}'.format(attrs_from, attr))

		try:
			attr_type = cmds.getAttr('{}.{}'.format(attrs_from, attr), type=True)
		except:
			attr_type = None

		if not attr_type:
			return

		if attr_type == 'double':
			cmds.addAttr(ctrl, ln=attr_name, proxy="{}.{}".format(attrs_from, attr), at="double",
						 min=cmds.attributeQuery(attr, node=attrs_from, min=True)[0],
						 max=cmds.attributeQuery(attr, node=attrs_from, max=True)[0],
						 )

		elif attr_type == 'double':
			cmds.addAttr(ctrl, ln=attr_name, proxy="{}.{}".format(attrs_from, attr), at="double",
						 min=cmds.attributeQuery(attr, node=attrs_from, min=True)[0],
						 max=cmds.attributeQuery(attr, node=attrs_from, max=True)[0],
						 )

		elif attr_type == 'enum':
			if 'RotateOrder' in attr:
				return
			print(cmds.attributeQuery(attr, node=attrs_from, listEnum=True)[0])
			cmds.addAttr(ctrl, ln=attr_name, proxy="{}.{}".format(attrs_from, attr), at="enum",
						 en=cmds.attributeQuery(attr, node=attrs_from, listEnum=True)[0],
						 )
	
	def create_softmod(self, vertex, name='soft_mod'):

		"""Creates a softMod deformer and adds a custom control structure for controlling the strength, radius, and falloff directions.

		    Args:
		        vertex (str): Vertex that the softMod will be created on.
		        name (str, optional): Name for the softMod. Defaults to 'soft_mod'.

		    Returns:
		        list: SoftMod, SoftMod handle, control, pivot control offset.

		    Notes:
		        - The softMod deformer is created on the specified vertex.
		        - A custom control structure is added to control the softMod's attributes.
		        - The control structure includes a main control, a pivot control, and a locator.
		        - Additional attributes are added to the main control to control the strength, radius, and falloff directions.

		    Examples:
		        1. Create a basic softMod:
		            soft_mod, soft_mod_handle, ctrl, pivot_ctrl_offset = create_softmod("pSphere1.vtx[0]", name="sphere_softMod")

		        2. Create a softMod with custom attributes:
		            soft_mod, soft_mod_handle, ctrl, pivot_ctrl_offset = create_softmod("pSphere1.vtx[0]", name="sphere_softMod")
		            # Add custom attributes
		            self.new_attr(ctrl, 'customAttr1', 0, 1, 1)
		            self.new_attr(ctrl, 'customAttr2', -10, 10, 0)
		            self.new_boolean(ctrl, 'customAttr3', 'True')
		    """
		

		cmds.select(vertex)
		soft_mod, soft_mod_handle = cmds.softMod(vertex, n=name+self.nc['softMod'], falloffMasking=0, falloffAroundSelection=0)
		cmds.setAttr('{}.origin'.format(soft_mod_handle), 0, 0, 0, type='double3')
		cmds.setAttr('{}.visibility'.format(soft_mod_handle), 0)

		# prepare controller structure
		
		ctrl = self.controller(soft_mod_handle, name, 'cube', world=False, gimbal=False)
		offset = ctrl['root'][0]
		ctrl = ctrl['ctrl']
		cmds.parent(soft_mod_handle, offset)

		pivot_ctrl = self.controller(ctrl, name+'_Pivot', 'cube', 'green', 1.33, False, False)
		pivot_ctrl_offset = pivot_ctrl['root']
		pivot_ctrl = pivot_ctrl['ctrl']
		cmds.parent(offset, pivot_ctrl)

		loc = cmds.spaceLocator(n='Loc_'+ctrl)[0]
		cmds.setAttr('{}.visibility'.format(loc), 0)
		self.match(loc, ctrl)
		cmds.parent(loc, offset)

		# add attrs to soft mod ctrl

		self.new_attr(ctrl, 'strength', 0, 1, 1)
		self.new_attr(ctrl, 'radius', 0, 100, 1)
		self.new_boolean(ctrl, 'falloffX', 'True')
		self.new_boolean(ctrl, 'falloffY', 'True')
		self.new_boolean(ctrl, 'falloffZ', 'True')

		# make connections

		cmds.connectAttr('{}.worldInverseMatrix[0]'.format(offset), '{}.bindPreMatrix'.format(soft_mod))
		cmds.connectAttr('{}.worldPosition'.format(loc), '{}.falloffCenter'.format(soft_mod))

		cmds.connectAttr('{}.strength'.format(ctrl), '{}.envelope'.format(soft_mod))
		cmds.connectAttr('{}.radius'.format(ctrl), '{}.falloffRadius'.format(soft_mod))
		cmds.connectAttr('{}.falloffX'.format(ctrl), '{}.falloffInX'.format(soft_mod))
		cmds.connectAttr('{}.falloffY'.format(ctrl), '{}.falloffInY'.format(soft_mod))
		cmds.connectAttr('{}.falloffZ'.format(ctrl), '{}.falloffInZ'.format(soft_mod))

		cmds.connectAttr('{}.t'.format(ctrl), '{}.t'.format(soft_mod_handle))
		cmds.connectAttr('{}.r'.format(ctrl), '{}.r'.format(soft_mod_handle))
		cmds.connectAttr('{}.s'.format(ctrl), '{}.s'.format(soft_mod_handle))

		#center pivot of soft mod
		piv = cmds.xform(loc, q=True, ws=True, t=True)
		cmds.xform(soft_mod_handle, ws=True, piv=piv)

		return soft_mod, soft_mod_handle, ctrl, pivot_ctrl_offset

	def get_dag_path(self, obj):
		"""Returns the DAG path of the specified object.

		Args:
			obj (str): Name of the object.

		Returns:
			om2.MDagPath or None: The DAG path of the object if it exists, None otherwise.

		Example:
			dag_path = get_dag_path('pSphere1')
		"""
		if cmds.objExists(obj):
			sel_list = om2.MSelectionList()
			sel_list.add(obj)
			return sel_list.getDagPath(0)
		else:
			print('{} does not exist'.format(obj))
			return None

	def get_closest_vertex(self, mesh_fn, point):
		"""Returns the closest vertex index on the given mesh to the specified point.

		Args:
			mesh_fn (om2.MFnMesh): Mesh function set.
			point (om2.MPoint): Point in world space.

		Returns:
			int: Index of the closest vertex.

		Example:
			# Get closest vertex on a mesh
			mesh_fn = om2.MFnMesh(get_dag_path('pSphere1'))
			point = om2.MPoint(1, 2, 3)
			closest_vertex = get_closest_vertex(mesh_fn, point)
		"""
		face_id = mesh_fn.getClosestPoint(point)[1]
		vertices = mesh_fn.getPolygonVertices(face_id)

		distances = ((vtx, mesh_fn.getPoint(vtx, om2.MSpace.kWorld).distanceTo(point)) for vtx in vertices)

		return min(distances, key=operator.itemgetter(1))[0]

	def get_position(self, obj):
		"""Returns the world space position of the specified object.

		Args:
			obj (str): Name of the object.

		Returns:
			list: List of three float values representing the x, y, and z coordinates.

		Example:
			position = get_position('pSphere1')
		"""
		return cmds.xform(obj,ws=True,q=True,t=True)
	
	def get_orient(self, obj):
		"""Returns the world space orientation of the specified object.

		Args:
			obj (str): Name of the object.

		Returns:
			list: List of three float values representing the x, y, and z rotation angles in degrees.

		Example:
			orientation = get_orient('pSphere1')
		"""
		return cmds.xform(obj,ws=True,q=True,ro=True)

	def get_scale(self, obj):
		"""Returns the world space scale of the specified object.

		Args:
			obj (str): Name of the object.

		Returns:
			list: List of three float values representing the x, y, and z scale values.

		Example:
			scale = get_scale('pSphere1')
		"""
		return cmds.xform(obj, ws=1, q=1, s=1)

	def rotate_shape(self, input=None, x=0, y=0, z=0):
		"""Rotates the control vertices of the shape nodes of the specified object.

		Args:
			input (str): Name of the object.
			x (float): Rotation angle in degrees around the X-axis.
			y (float): Rotation angle in degrees around the Y-axis.
			z (float): Rotation angle in degrees around the Z-axis.

		Returns:
			bool: True if successful, False otherwise.

		Example:
			# Rotate the shape of a sphere
			rotate_shape('pSphere1', x=45, y=0, z=0)
		"""
		if not input:
			cmds.warning('We need an input')
			return False

		shapes = cmds.listRelatives(input, s=True)
		if not shapes:
			return False
		for s in shapes:
			cmds.select('{}.cv[*]'.format(s))
			cmds.rotate(x,y,z, r=True)

		cmds.select(input)

	def scale_shape(self, input=None, x=1, y=1, z=1):
		"""Scales the control vertices of the shape nodes of the specified object.

		Args:
			input (str): Name of the object.
			x (float): Scale factor along the X-axis.
			y (float): Scale factor along the Y-axis.
			z (float): Scale factor along the Z-axis.

		Returns:
			bool: True if successful, False otherwise.

		Example:
			# Scale the shape of a sphere
			scale_shape('pSphere1', x=2, y=1, z=1)
		"""
		if not input:
			cmds.warning('We need an input')
			return False

		shapes = cmds.listRelatives(input, s=True)
		if not shapes:
			return False
		for s in shapes:
			cmds.select('{}.cv[*]'.format(s))
			cmds.scale(x,y,z, r=True, ocp=True)

		cmds.select(input)

	def translate_shape(self, input=None, x=0, y=0, z=0):
		"""Translates the control vertices of the shape nodes of the specified object.

		Args:
			input (str): Name of the object.
			x (float): Translation distance along the X-axis.
			y (float): Translation distance along the Y-axis.
			z (float): Translation distance along the Z-axis.

		Returns:
			bool: True if successful, False otherwise.

		Example:
			# Translate the shape of a sphere
			translate_shape('pSphere1', x=1, y=0, z=0)
		"""
		if not input:
			cmds.warning('We need an input')
			return False

		shapes = cmds.listRelatives(input, s=True)
		if not shapes:
			return False
		for s in shapes:
			cmds.select('{}.cv[*]'.format(s))
			cmds.move(x,y,z, r=True)

		cmds.select(input)

	def calculate_bounding_box_diagonal(self, geo):
		"""Calculates the diagonal length of the bounding box of the specified geometry.

		Args:
			geo (str): Name of the geometry.

		Returns:
			tuple: A tuple containing the name of the bounding box and the diagonal length.

		Example:
			bbox, diagonal_length = calculate_bounding_box_diagonal('pSphere1')
		"""
		bbox = cmds.geomToBBox(geo, nameSuffix='_BBox', single=1, keepOriginal=1)[0]

		vertexA = cmds.pointPosition('{}.vtx[0]'.format(bbox))
		vertexB = cmds.pointPosition('{}.vtx[6]'.format(bbox))
		vertexA = om2.MVector(vertexA)
		vertexB = om2.MVector(vertexB)
		displacement = vertexB - vertexA
		bbox_diagonal_length = displacement.length()

		return bbox, bbox_diagonal_length

	def rivet_constraint(self, faces=None):
		"""Applies a rivet constraint to the specified faces.

		Args:
		    faces (list[str]): Optional. The faces to which the rivet constraint should be applied.
		        If not specified, an error is raised.

		Returns:
		    list[str]: A list of the rivets objects after applying the rivet constraint.

		Raises:
		    RuntimeError: If no faces are provided.

		Notes:
		    This function applies a rivet constraint to the specified faces in Maya. It uses the
		    Maya internal nodes and the uvpin.node_interface module to create the rivet.

		Example:
		    >>> rivet_constraint(['pCube1.f[0]', 'pCube1.f[1]'])
		    ['pCube1.f[0]', 'pCube1.f[1]']

		"""
		if not faces:
			cmds.error('We need faces selection to work')
		cmds.select(faces)
		import maya.internal.nodes.uvpin.node_interface
		pin = maya.internal.nodes.uvpin.node_interface.createRivet()

		return cmds.ls(sl=True)

	def find_closest_joint(self, joint, target_list):
		"""
		Find the closest joint in the target_list to the given joint.

		Args:
			joint (str): The name of the joint to which distances are measured.
			target_list (list[str]): List of joint names to compare distances with.

		Returns:
			str: The name of the closest joint from the target_list.

		Notes:
			This function calculates the distance between the specified joint and a list of target joints.
			It returns the name of the joint in the target_list that is closest to the given joint.

		Example:
			mt.find_closest_joint('joint1', ['joint2', 'joint3', 'joint4'])
			'joint2'

		"""

		closest_distance = float("inf")
		closest_joint = None

		for target_joint in target_list:
			if target_joint == joint:
				continue

			joint_pos = cmds.xform(joint, query=True, translation=True, worldSpace=True)
			target_joint_pos = cmds.xform(target_joint, query=True, translation=True, worldSpace=True)

			distance = ((joint_pos[0] - target_joint_pos[0]) ** 2 +
						(joint_pos[1] - target_joint_pos[1]) ** 2 +
						(joint_pos[2] - target_joint_pos[2]) ** 2) ** 0.5

			if distance < closest_distance:
				closest_distance = distance
				closest_joint = target_joint

		return closest_joint

	def connect_object_to_offsets(self, driver_ctrl='', driven_ctrls=[], offset_name='', auto_root=True, rotation=True, translation=False, scaling=False):
		"""
		Description:
		Connect the transformations (rotation, translation, scaling) of a driver controller to multiple driven controllers.

		Args:
			driver_ctrl (str): The controller whose transformations will be used as the source.
			driven_ctrls (list): List of controllers to connect to the driver controller.
			offset_name (str): Custom name for the offset groups created for each driven controller.
			rotation (bool): Flag to determine whether to connect rotation attributes.
			translation (bool): Flag to determine whether to connect translation attributes.
			scaling (bool): Flag to determine whether to connect scaling attributes.

		Returns:
			list: A list of offset groups created for each driven controller.

		Example:
			connect_object_to_offsets(driver_ctrl="source_ctrl", driven_ctrls=["driven_ctrl_1", "driven_ctrl_2"], offset_name="offset_grp", rotation=True, translation=True, scaling=False)
		"""
		offset_grps = []

		for ctrl in driven_ctrls:
			grps = self.root_grp(ctrl, custom=True, custom_name=offset_name, autoRoot=auto_root)
			grp = grps[-1]
			"""
			if len(grps)>1:
				grp = grps[-1]
			else:
				grp = grps
			"""

			#Connecting selected parameters. 
			if rotation:
				cmds.connectAttr('{}.r'.format(driver_ctrl),'{}.r'.format(grp),f=True)
			if translation:
				cmds.connectAttr('{}.t'.format(driver_ctrl),'{}.t'.format(grp),f=True)
			if scaling:
				cmds.connectAttr('{}.s'.format(driver_ctrl),'{}.s'.format(grp),f=True)
			
			offset_grps.append(grps)
		
		return offset_grps

#tool = Tools_class()


