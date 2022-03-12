'''
version: 1.0.0
date: 21/04/2020

#----------------

how to:
	
import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import tools
imp.reload(Mutant_Tools.Utils.Rigging.tools)

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
import imp
import json
from pathlib import Path

from  maya import mel
from maya import cmds


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
#Read curve shapes info
CURVE_FILE = os.path.join(FOLDER, 'config', 'curves.json')
with open(CURVE_FILE) as curve_file:
	curve_data = json.load(curve_file)
#setup File
SETUP_FILE = os.path.join(FOLDER, 'config', 'rig_setup.json')
with open(SETUP_FILE) as setup_file:
	setup = json.load(setup_file)


#----------------------------------------------------------------------------------------------------------------
#create base class for selection objects

class Tools_class(object):
	
	def __init__(self, input = ''):

		self.input = input

	#----------------------------------------------------------------------------------------------------------------			

	def check_input(self, func = '', print_input = False):
		"""	if input is empty uses selection instead, i used to use this but stop becouse is not usefull... sorry :)


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
		"""This create groups

		Args:
			input: if not specify it will use selection else specify string
			custom: bool: specify if new grp have a custom name
			custom_name: string: name of custom group (needs custom to be True)
			autoRoot: bool: will create 2 groups intead of 1: Root Grp and Auto Grp
			replace_nc:bool: will try to replace the name space to be the groups one.

		Returns: list with string of new groups

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
				group_names = [nc['root'], nc['auto']]
			else:
				group_names = [nc['offset']]				

			if custom == True:
				group_names = [custom_name]      

			if custom and autoRoot:
				group_names = [nc['root'], nc['auto'],custom_name]
				
			for name in group_names:
				
				cmds.select(i)
				father = cmds.listRelatives(i, p =1)
				
				#Null group as parent in same xform
				group_zero = cmds.group(em=1, n = '{}{}'.format(i,name) + nc['group'])
				cmds.delete(cmds.parentConstraint(i,group_zero, mo =0))
			  
				cmds.parent(i,group_zero)
				
				#if they have upper nodes, put them inside
				if father :cmds.parent(group_zero, father) 
				cmds.select(group_zero)
				
				#Remove Nameconventions		
				if (replace_nc):
					try:group_zero = self.replace_name(input = '', search = nc['ctrl'], replace = '', hi = False)
					except:pass
					
					try:group_zero = self.replace_name(input = '', search = nc['joint'], replace = '', hi = False)
					except:pass	
				
				#return this groups				
				groups.append(group_zero)     
				
		return groups    

	#----------------------------------------------------------------------------------------------------------------		
	
	def replace_name(self, input = '', search = '', replace = '', hi = False):
		""" will replace names in selection. Works nice to change names i hierarchys

		Args:
			input: if not specify it will use selection else specify string
			search: string to search
			replace: string to replace with
			hi: bool: true if do the change to all the hierarchy.

		Returns: list with new names

		"""

		if hi ==True:

			mel.eval( 'searchReplaceNames {} {} "hierarchy"'.format(search, replace))
			cmds.select(hi = True)
	
		else:
			mel.eval( 'searchReplaceNames {} {} "selected"'.format(search, replace))
	
	
		return cmds.ls(sl = True)

	#----------------------------------------------------------------------------------------------------------------
	
	def assign_color(self, input = '', color = 'lightBlue'):
		"""	assing color to desire transform

		available_colors = {    'red':       13,
								'blue':       6,
								'white':     16,
								'purple':     9,
								'green':     14,
								'lightBlue': 18,
								'yellow':    17,
								'grey':       1  }

		Args:
			input: if not specify it will use selection else specify string
			color: string of name (dont accept intergers)

		Returns: None

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
					'grey':      1 }

		color_num = colors[color]
		
		for obj in self.input:
			cmds.setAttr ('{}.overrideEnabled'.format(obj), 1)
			cmds.setAttr ('{}.overrideColor'.format(obj), color_num)
			
	#----------------------------------------------------------------------------------------------------------------					
	def hide_attr(self, input = '', t= False, r = False, s = False, v = False, rotate_order = False, show = False):
		"""Will hide selected attrs or display them all if show

		Args:
			input: if not specify it will use selection else specify string
			t: bool hide translate
			r: bool hide rotate
			s: bool hide scale
			v: bool hide visibility
			rotate_order: bool hide rotate order
			show: bool show all

		Returns: None

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

	def curve(self,input = '', type = 'cube', rename = True, custom_name = False, name = '', size = 1):
		"""For Controllers this is legacy, use mt.controller// Will create a curve on position of selected input.
		(see curves.json in config for more details of avilable shapes)

		Args:
			input: if not specify it will use selection else specify string
			type: string name of shape
			rename: bool to replace namespaces at the end
			custom_name: true if want to assigne new name, false if want the same as selection
			name: string custom name
			size: int  size

		Returns: string ctrl

		"""

		try:sel = cmds.ls(sl = True)[0]
		except: sel = 'RdM'

		#create curve from mel cmds in json file
		ctrl = mel.eval(curve_data[type])
			
		#set name of the curve
		if (rename): 
			ctrl = cmds.rename(ctrl, '{}{}'.format(sel,nc['ctrl']))
		
		else:      
			ctrl = cmds.rename(ctrl, '{}{}'.format(type,nc['ctrl']))

		if (custom_name):
			ctrl = cmds.rename(ctrl, name)

		if (size):
			curve_cvs = cmds.ls(cmds.ls(sl = True)[0] + ".cv[0:]",fl=True)
			cmds.scale(size,size,size, curve_cvs)	

		#match to selection and assing color if possible
		try:self.match(ctrl, sel)
		except:pass
		self.assign_color(color = setup['main_color'])

		#connect rotate order to itself
		self.connect_rotate_order(input = ctrl, object = ctrl)

		#change ctrl line width
		cmds.setAttr('{}.lineWidth'.format(cmds.listRelatives(ctrl, shapes=True)[0]), int(setup['line_width']))

		try:self.hide_attr(input = ctrl, v=True)
		except:pass
		
		#return last ctrl created
		return ctrl	

	#----------------------------------------------------------------------------------------------------------------
	def controller(self, input='', name='', shape='cube', color = setup['main_color'], size = 1, gimbal=True, world=True):
		""" Create controller in input

		Args:
			input: string name of input if None creates on world
			name: string desire name, if None uses input
			shape: string desire shape (see curves.json in config for more details of avilable shapes)
			color: string desire color
			size: int desire size
			gimbal: bool creates gimbal ctrl under main ctrl
			world: bool creates world control oriented to the world

		Returns: {'ctrl':ctrl,
				'root':root,
				'world':world,
				'gimbal':gimbal}

		"""

		if not input:
			input = 'Mt'

		if not name:
			cmds.warning('No name in mt.controller(), using input')
			name = input

		ctrl = mel.eval(curve_data[shape])

		try:self.match(ctrl, input)
		except:pass

		ctrl = cmds.rename(ctrl, '{}{}'.format(name, nc['ctrl']))
		root = self.root_grp()
		controllers = [ctrl]

		#Add gimbal sub controller
		if world:
			world = mel.eval(curve_data[shape])
			world = cmds.rename(world, '{}{}'.format(name, nc['world_ctrl']))
			controllers.append(world)
			world_root = self.root_grp()
			show_world_attr = self.new_enum(input=ctrl, name='World', enums='Hide:Show')
			cmds.connectAttr(show_world_attr, '{}.v'.format(cmds.listRelatives(world, shapes=True)[0]))
			self.match(world_root, ctrl, r=False)
			cmds.parent(root, world)


		if gimbal:
			gimbal = mel.eval(curve_data[shape])
			gimbal = cmds.rename(gimbal, '{}{}'.format(name, nc['gimbal_ctrl']))
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
		""" Match 2 transforms with the desire transform, rotate or scale

		Args:
			this: string item to move
			that: string item with desire position
			t: bool match translate
			r: bool match rotate
			s: bool match scale

		Returns: None

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
		"""Create a switch between 3 chains (for ikfk setups) There is a blend colors alternative to this one.

		Args:
			this:string ik joint(can be any transform)
			that:string fk joint(can be any transform)
			main:ik main joint that swtich between
			attr: string what to use as a switch parent

		Returns: None

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
		"""Create a switch between 3 chains (for ikfk setups) There is a constraint alternative to this one.

		Args:
			this:string ik joint(can be any transform)
			that:string fk joint(can be any transform)
			main:ik main joint that swtich between
			attr: string what to use as a switch parent

		Returns: None
		"""

		attrs = ['translate', 'rotate', 'scale']

		for a in attrs:
		#create blend node
			blend_node = cmds.shadingNode('blendColors' , asUtility = True, n = '{}_{}{}'.format(this, a, nc['blend']))

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
		"""Will create new double attr on transform

		Args:
			input: if not specify it will use selection else specify string
			name: string name of new attr
			min: interger min (need it)
			max: interget max (need it)
			default: interger deafult value

		Returns: string attr name

		"""

		#add new attr as float
		cmds.addAttr(input, ln = name, at = 'double', min = min, max = max, dv = default)
		cmds.setAttr('{}.{}'.format(input, name), e = True, keyable = True)

		return '{}.{}'.format(input, name)

	#----------------------------------------------------------------------------------------------------------------
	def new_attr_interger(self, input= '', name = 'switch', min = 0 , max = 1, default = 0):
		"""Will create new long attr on transform

		Args:
			input: if not specify it will use selection else specify string
			name: string name of new attr
			min: interger min (need it)
			max: interget max (need it)
			default: interger deafult value

		Returns: string attr name

		"""
	
		#add new attr as float
		cmds.addAttr(input, ln = name, at = 'long', min = min, max = max, dv = default)
		cmds.setAttr('{}.{}'.format(input, name), e = True, keyable = True)

		return '{}.{}'.format(input, name)

	#----------------------------------------------------------------------------------------------------------------
	
	def new_enum(self, input= '', name = 'switch', enums = 'Hide:Show'):
		"""Will create new enum attr on transform

		Args:
			input: if not specify it will use selection else specify string
			name: string attr name
			enums: strings separated by :

		Returns: string attr name
		"""
		
		#add new attr as float
		cmds.addAttr(input, ln = name, at = 'enum', en = enums)
		cmds.setAttr('{}.{}'.format(input, name), e = True, channelBox = True)

		return '{}.{}'.format(input, name)

	#----------------------------------------------------------------------------------------------------------------
	
	def new_boolean(self, input= '', name = 'bool', dv = 'True'):
		"""Will create new boolean attr on transform

		Args:
			input: if not specify it will use selection else specify string
			name: string attr name
			dv: bool default value

		Returns: string attr name

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
		""" Will create a line Attr ---------------[NAME]

		Args:
			input: if not specify it will use selection else specify string
			name:Attrs name
			lines: int amount of lines, iff amount exists will -1 until possible

		Returns: String Attr name
		"""

		for num in reversed(range(lines)):
			try:
				line_attr = self.new_enum(input= input, name = '_'*num, enums = '{}:'.format(name))
				cmds.setAttr(line_attr,e=True, lock = True)
			except:
				continue

			return line_attr

	#----------------------------------------------------------------------------------------------------------------

	def string_attr(self, input = '', name = 'name', string = 'string'):
		""" Will create a string attr. Usefull to store information

		Args:
			input: if not specify it will use selection else specify string
			name: string name
			string: string value

		Returns: string attr name

		"""

		cmds.addAttr(input, ln=name, dt="string")
		cmds.setAttr('{}.{}'.format(input,name), string, type="string")

		return '{}.{}'.format(input,name)

	#----------------------------------------------------------------------------------------------------------------

	def connect_rotate_order(self, input = '', object = 'controller'):
		"""Will connect inputs RO to attr in controller object

		Args:
			input: if not specify it will use selection else specify string
			object: String where to put the attr

		Returns: string attr

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
			pass
		else:
			self.new_enum(input= object, name = 'RotateOrder', enums = 'xyz:yzx:zxy:xzy:yxz:zyx')
			cmds.setAttr('{}.RotateOrder'.format(object), e = True, channelBox = True)

		#connect attr	
		for input in self.input:
			cmds.connectAttr('{}.RotateOrder'.format(object), '{}.rotateOrder'.format(input), f = True)

		return '{}.RotateOrder'.format(object)

	#----------------------------------------------------------------------------------------------------------------

	def duplicate_change_names(self, input = '', hi = True, search='_Jnt', replace ='_dup'):
		""" duplicate any hierarchy with no duplicated names but with clean ones


		Args:
			input: if not specify it will use selection else specify string
			hi: bool if do it in all the hierarchy
			search: string to seacrh
			replace: string to replace

		Returns: string duplicated[0] transform

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
		"""	create a ctrl cube with coverage for the full limb, so its like a bounding box in lenght


		Args:
			input: if not specify it will use selection else specify string
			size: ctrl size
			name: string name of cube
			axis: X Y o Z for the aim axis. By default will read the setup file

		Returns: string ctrl

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
		"""create a shape with an attr to put inside all the input ransform (to have a ik fk switch on all the ctrls)

		Args:
			input: if not specify it will use selection else specify string
			obj_name: string transform name to put the shape in
			attr_name: string attr name

		Returns: string attr

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
		if cmds.objExists(obj_name + nc['locator']):
			loc_shape = obj_name + nc['locator']
		else:
			loc = cmds.spaceLocator(n = obj_name + nc['locator'])
			loc_shape = cmds.pickWalk(d ='down')[0]
			loc = loc[0]

		#hide unwanted attrs
		hide_this_attrs = ['lpx','lpy','lpz','lsx','lsy','lsz']
		for attr in hide_this_attrs:
			try: cmds.setAttr("{}.{}".format(loc_shape, attr), lock=True, channelBox=False, keyable=False)
			except: print ('shape_with_attr info: no rotate order atttr found')

		cmds.setAttr("{}.visibility".format(loc_shape), 0)

		#add new attr to the shape if it doesnt exists
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

		loc_shape = cmds.rename(loc_shape, obj_name + nc['locator'])

		return obj_name + nc['locator'] + '.' + attr_name


	#----------------------------------------------------------------------------------------------------------------				
	def text_curves(self, name_text = 'Name', font = 'Arial', color = setup['main_color']):
		"""Create text curves

		Args:
			name_text: string text to curve
			font:string desire font
			color: string color

		Returns: string curve

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
			cmds.setAttr (dl+'.overrideEnabled', 1)
			cmds.setAttr (dl+'.overrideColor', Color)

		#Organizing
		cmds.parent (Shape, w = True)
		cmds.rename (Shape, Texto + str(nc['ctrl']))
		cmds.delete(Text[0])
		cmds.delete (Texto + str(nc['ctrl']+'Shape'))
		cmds.move (-0.5,0,0, r = True)
		cmds.xform(cp= True)
		cmds.rename(name_text + nc['curve'])

		return name_text + nc['curve']
			
	#----------------------------------------------------------------------------------------------------------------		

	def swap_connections(self, old_node = '', new_node= 'new_node_here', inputs= 'False', outputd='False'):
		""" Nothing Yet sorry.

		Args:
			old_node:
			new_node:
			inputs:
			outputd:

		Returns:

		"""

		'''
		#this tool will try to swap all the output or input onenctios to the node
		wanted_attr = ['translate','rotate','scale']

		source_attrs = cmds.listConnections(old_node, c = True, d=False)
		destination_attrs = cmds.listConnections(old_node, c = True, s=False)

		print (str(source_attrs) + ':' + str(destination_attrs))
		'''
		
		''

	#----------------------------------------------------------------------------------------------------------------		

	def curve_between(self, start, end):
		""" Will create a 1d curve between to transforms
		
		Args:
			start: string transform 1
			end: string transform 2

		Returns: curve

		"""
		#create a simple linear curve between 2 joints 
	   
		pos_a = cmds.xform(start, q=True,t=True, ws=True)
		pos_b = cmds.xform(end, q=True,t=True, ws=True) 
	   
		crv = cmds.curve(d=1, p=[pos_a,pos_b], k=[0,1], n = '{}{}'.format(start, nc['curve']))
	   
		return crv

	#----------------------------------------------------------------------------------------------------------------		
	
	def nurbs_between(self, start, end):
		""" Will create a nurbs plane between 2 transforms

		Args:
			start: string start transform
			end: string end transform

		Returns: nurbs plane

		"""
		#creates a nurbs plane between 2 transforms
		
		name = start.replace(nc['joint'], '') +'_'+ end.replace(nc['joint'], '')+ nc['nurb']  
		surface = cmds.nurbsPlane(d = 1, ch = False, n = name)[0]
		temp_cluster1 = cmds.cluster('{}.cv[0:1][0]'.format(surface))
		temp_cluster2 = cmds.cluster('{}.cv[0:1][1]'.format(surface))

		cmds.delete(cmds.parentConstraint(start,temp_cluster1, mo =False))
		cmds.delete(cmds.parentConstraint(end,temp_cluster2, mo =False))
		cmds.delete(surface, constructionHistory = True)
		
		return surface
		

	#----------------------------------------------------------------------------------------------------------------		

	def nurbs_between_trio(self, start, mid, end):
		def nurbs_between(self, start, end):
			""" Will create a nurbs plane between 2 transforms

			Args:
				start: string start transform
				mid: string mid transform
				end: string end transform

			Returns: nurbs plane

			"""
		#creates a nurbs plane between 3 transforms

		name = start.replace(nc['joint'], '') +'_'+ end.replace(nc['joint'], '')+ nc['nurb']  
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
		"""create ik spline based on 2 joints and one curve

		Args:
			start:string first joint
			end: string last joint
			curve: string curve (can use curve between to create it)

		Returns: {'ikHandle': ikSpline, 'effector': effector_spline, 'curve': spline_curve}

		"""

		# ik spline solver
		ikSpline = cmds.ikHandle(sj=start,
								 ee=end,
								 sol='ikSplineSolver',
								 n=start + '_Twist' + nc['ik_spline'],
								 c = curve,
								 ccv=False,
								 pcv = False)

		effector_spline = cmds.rename(ikSpline[1], start + '_Twist' + nc['effector'])
		ikSpline = ikSpline[0]
		spline_curve = ikSpline[2]

		return {'ikHandle': ikSpline, 'effector': effector_spline, 'curve': spline_curve}

	#----------------------------------------------------------------------------------------------------------------		

	def connect_md_node(self, in_x1 = '', in_x2 = 1.0, out_x = '', mode = 'mult', name = '', force = False):
		"""	this wil create a md node for you to connect something in the input 1x, to output 1x and a value


		Args:
			in_x1: string attr to connect to input 1 or int value
			in_x2: string attr to connect to input 1 or int value
			out_x: atrr to connect the multiply devide output
			mode: string mult or devide
			name: name of node
			force: force the connection if needed. False by default so we can debug easy

		Returns: string node name

		"""

		if name == '':
			try:
				name = in_x1.split('.')[0]
			except:
				name = in_x2.split('.')[0]

		#create md node with correct value and mode
		md_node = cmds.shadingNode('multiplyDivide', asUtility=1, n  = '{}{}'.format(name, nc['multiplyDivide']))

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
			cmds.connectAttr(in_x1, '{}.input1.input1X'.format(md_node), f=True)

		#check input 2x
		if isinstance(in_x2, int) == True:
			cmds.setAttr(str(md_node)+'.input2X', in_x2)
		elif isinstance(in_x2, float) == True:
			cmds.setAttr(str(md_node)+'.input2X', in_x2)
		else: 
			cmds.connectAttr(in_x2, '{}.input2.input2X'.format(md_node), f=True)

		#connect output
		if out_x == '':
			return md_node

		if force: 
			cmds.connectAttr('{}.output.outputX'.format(md_node), out_x, f=True)
		else:
			cmds.connectAttr('{}.output.outputX'.format(md_node), out_x)

		self.put_inside_rig_container([md_node])

		#return node
		return md_node

	#----------------------------------------------------------------------------------------------------------------

	def trasform_on_sel(self, transform='', name='Temp'):
		"""	position a transform node in desire selection, if there is no trasnform it will create a joint for you (Not sure why we needed this one)

		Args:
			transform: where to put the new transform
			name: string name

		Returns: None

		"""

		
		cluster = cmds.cluster(n='temp'+nc['cluster'])
		print (cluster)
		#cluster = cmds.rename(cluster,str(cluster[1]).replace('Handle', nc['cluster_handle']))

		#create if no input
		if transform == '':
			cmds.select(cl=True)
			transform = cmds.joint(n=name+nc['joint'])
		
		#put input in desire location
		cmds.delete(cmds.parentConstraint(cluster[1], transform, mo=False))

	#----------------------------------------------------------------------------------------------------------------
	def connect_with_line(self, start='', end=''):
		""" Create a non selectable curve between to objects (Pole Vectors Lines)

		Args:
			start: string start transform
			end: string end transform

		Returns:

		"""

		if start=='':
			sel = cmds.ls(sl=True)
			start = sel[0]
			end = sel[1]

		#create line 
		cv = self.curve_between(start=start, end=end)
		cv = cmds.rename(cv, '{}_{}{}{}'.format(start,end,nc['connected'], nc['curve']))

		#create clusters on cvs 0 and 1
		cmds.select('{}.cv[0]'.format(cv))
		cluster_start = cmds.cluster(n='{}{}'.format(start,nc['cluster']))
		cmds.select('{}.cv[1]'.format(cv))
		cluster_end = cmds.cluster(n='{}{}'.format(end,nc['cluster']))

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
		"""

		Args:
			input: if not specify it will use selection else specify string
			unlock: bool: True Unlocks and False locks

		Returns:

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
		""" Add a double linear between 2 nodes

		Args:
			input: if not specify it will use selection else specify string
			attr: attr to connect the double linear result
			name: string node name

		Returns: string node

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
		""" Will write json file with data

		Args:
			path: path to put the json file in (rembember to use \\ to define the folders)
			json_file: json file name
			data: dictionary to sabe

		Returns: string json file full path

		"""
		write_json = os.path.join(path, json_file)

		with open(write_json, 'w', encoding='utf-8') as f:
			json.dump(data, f, ensure_ascii=False, indent=4, sort_keys = False)

		print(write_json)
		return write_json

	#----------------------------------------------------------------------------------------------------------------

	def read_json(self, path, json_file):
		""" will read json file

		Args:
			path: path to where the json file is (rembember to use \\ to define the folders)
			json_file: json file name

		Returns: dictionary with data

		"""

		json_data = os.path.join(path, json_file)

		with open(json_data) as f:
			data = json.load(f)

		return data

	#----------------------------------------------------------------------------------------------------------------

	def change_default(self, atrr, default):

		cmds.addAttr('{}'.format(atrr), e=1, dv=default)

	#----------------------------------------------------------------------------------------------------------------

	def put_inside_rig_container(self, inputs = []):
		if not inputs:
			return False

		if not cmds.objExists('Mutant_Rig'):
			mutant_rig = cmds.container(name='Mutant_Rig', type='dagContainer')
		else:
			mutant_rig = 'Mutant_Rig'


		for input in inputs:
			cmds.container('Mutant_Rig', e=True, addNode=input)





#tool = Tools_class()


