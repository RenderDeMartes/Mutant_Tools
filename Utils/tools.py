'''
version: 1.0.0
date: 21/04/2020

#----------------
content: 

self.check_input() #print input infomation
self.input_unit() #convert input list in a string

root_grp(input = '', repalce_np = False) #Create a group over the input		
asign_color(input = '', color = '') #asign color to the input
replace_name(input = '', custom = False, custom_name = 'customName', autoRoot = True, replace_nc = False) #Change names with or without Hierarchy
hide_attr(input = '',t= False, r = False, s = False, v = False, show = False) #Hide attrs in channel box o show them all
curve(type = 'cube', rename = True, custom_name = False, name = '',  size = 1) #based on curves.json file
match(this = '', that = '' ,t = True, r = True, s = True)
switch(this = '', that = '', main = '', attr = '')#create a switch with a parent contraint 
new_attr(input= '', name = 'switch', min = 0 , max = 1, default = 0) # create a new float attr with min, max and feault value

NEEDS A UPDATE :)
#----------------
how to: 
	
import Mosaic_Tools
import Mosaic_Tools.Utils
from Mosaic_Tools.Utils import tools
imp.reload(Mosaic_Tools.Utils.tools)

tool = tools.Tools_class()
tool.FUNC_NAME(argument = '')

#----------------
dependencies:   

json
pymel
maya mel
maya.cmds

#----------------
licence: https://www.eulatemplate.com/live.php?token=ySe25XC0bKARQymXaGQGR8i4gvXMJgVS
author:  Esteban Rodriguez <info@renderdemartes.com>

'''
import os
import imp
import json

from  maya import mel
from maya import cmds
import pymel.core as pm


#----------------------------------------------------------------------------------------------------------------

#Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = PATH.replace('\\Utils', '//Config')

JSON_FILE = (PATH + '/name_conventions.json')
with open(JSON_FILE) as json_file:
	nc = json.load(json_file)
#Read curve shapes info
CURVE_FILE = (PATH + '/curves.json')
with open(CURVE_FILE) as curve_file:
	curve_data = json.load(curve_file)
#setup File
SETUP_FILE = (PATH+'/rig_setup.json')
with open(SETUP_FILE) as setup_file:
	setup = json.load(setup_file)	

#----------------------------------------------------------------------------------------------------------------
#create base class for selection objects

class Tools_class:
	
	def __init__(self, input = ''):
		
		self.input = input

	#----------------------------------------------------------------------------------------------------------------			
	#input can be an argument or a selection

	def check_input(self, func = '', print_input = False):
		'''
		if input is empty uses selection instead, i used to use this but stop becouse is not usefull... sorry :)
		'''
		
		if self.input == '':
						
			self.input = cmds.ls(sl = True)
			if (print_input):
				print ('{} input is selection: {}'.format(func, self.input))
			
		else:
			if (print_input):
				print ('{} input is argument: {}'.format(func, self.input))
	
	
	#----------------------------------------------------------------------------------------------------------------			
	#create a group over the 
	def	root_grp(self, input = '', custom = False, custom_name = 'customName', autoRoot = False, replace_nc = False):
		'''
		create offsete groups for desire transforms
		'''

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
	#Search and Replace names
	
	def replace_name(self, input = '', search = '', replace = '', hi = False):
		'''
		replaces names of obj or obj hierarchy
		'''
			
		if hi ==True:

			pm.mel.searchReplaceNames(search, replace, "hierarchy")
			cmds.select(hi = True)
	
		else:
			pm.mel.searchReplaceNames(search, replace, "selected")
	
	
		return cmds.ls(sl = True)


	#----------------------------------------------------------------------------------------------------------------		
	#Asign Color
	
	def asign_color(self, input = '', color = 'lightBlue'):
		'''
		assing color to desire transform
		'''
		
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
	def hide_attr(self, input = '', t= False, r = False, s = False, v = False, show = False):
		'''
		hide translate, rotate, scale and visivility from attrs channel box
		'''

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
				
			#show and unlock everything
			if (show):
				sel=pm.ls(long=1, sl=1)
				attrs = ['.tx','.ty','.tz','.rx','.ry','.rz','.sx','.sy','.sz','.v']
				
				for eachObj in sel:
					for attr in attrs:	        
						pm.listAttr(eachObj, ud=1)
						pm.setAttr('{}{}'.format(eachObj, attr), k=True)
						pm.setAttr('{}{}'.format(eachObj,attr), l=False)

	#----------------------------------------------------------------------------------------------------------------					

	# meter size
	def curve(self,input = '', type = 'cube', rename = True, custom_name = False, name = '', size = 1):
		'''
		create curves shapes based on the curve json file
		'''

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
		self.asign_color(color = setup['main_color'])

		#connect rotate order to itself
		self.connect_rotate_order(input = ctrl, object = ctrl)

		#change ctrl line width
		cmds.setAttr('{}.lineWidth'.format(cmds.listRelatives(ctrl, shapes=True)[0]), int(setup['line_width']))

		try:self.hide_attr(input = ctrl, v=True)
		except:pass
		
		#return last ctrl created
		return ctrl	

	#----------------------------------------------------------------------------------------------------------------

	def match(self, this = '', that = '' ,t = True, r = True, s = True):
		'''
		match desire transforms
		'''
		if (t):
			cmds.delete(cmds.pointConstraint(that, this, mo =False))
		if (r):
			cmds.delete(cmds.orientConstraint(that, this, mo =False))
		if (s):
			cmds.delete(cmds.scaleConstraint(that, this, mo =False))

	#----------------------------------------------------------------------------------------------------------------
	def switch_constraints(self, this = '', that = '', main = '', attr = ''):
		'''
		create a switch between 3 joints chains and it used a parent constraint instead of blend colors
		'''

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

	#----------------------------------------------------------------------------------------------------------------
	def switch_blend_colors(self, this = '', that = '', main = '', attr = ''):
		'''
		create a swhitch between 3 joints chains and it used a blend colors instead of parent constraints
		'''

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

	#----------------------------------------------------------------------------------------------------------------
	def new_attr(self, input= '', name = 'switch', min = 0 , max = 1, default = 0):
		'''
		create a double attr default is 0 to 1 and deafault value as 0
		'''
	
		#add new attr as float
		cmds.addAttr(input, ln = name, at = 'double', min = min, max = max, dv = default)
		cmds.setAttr('{}.{}'.format(input, name), e = True, keyable = True)

		return '{}.{}'.format(input, name)

	#----------------------------------------------------------------------------------------------------------------
	def new_attr_interger(self, input= '', name = 'switch', min = 0 , max = 1, default = 0):
		'''
		create a int attr default is 0 to 1 and deafault value as 0
		'''
	
		#add new attr as float
		cmds.addAttr(input, ln = name, at = 'long', min = min, max = max, dv = default)
		cmds.setAttr('{}.{}'.format(input, name), e = True, keyable = True)

		return '{}.{}'.format(input, name)

	#----------------------------------------------------------------------------------------------------------------
	
	def new_enum(self, input= '', name = 'switch', enums = 'Hide:Show'):
		'''
		create an enum attr in the attr lists for the input, default is going to be Hide and Show
		'''
		
		#add new attr as float
		cmds.addAttr(input, ln = name, at = 'enum', en = enums)
		cmds.setAttr('{}.{}'.format(input, name), e = True, channelBox = True)

		return '{}.{}'.format(input, name)

	#----------------------------------------------------------------------------------------------------------------
	
	def new_boolean(self, input= '', name = 'bool', dv = 'True'):
		'''
		create an boolean attr in the attr lists for the input, default is going to be Hide and Show
		'''
		
		#add new attr as float
		cmds.addAttr(input, ln = name, at = 'bool')
		cmds.setAttr('{}.{}'.format(input, name), e = True, channelBox = True)
		if dv == 'True':
			cmds.setAttr('{}.{}'.format(input, name), 1)
		print (dv)

		return '{}.{}'.format(input, name)
	#----------------------------------------------------------------------------------------------------------------

	def line_attr(self, input = '', name = 'name', lines = 10):
		'''
		create this attr in the attr lists __________
		'''
		line_attr = self.new_enum(input= input, name = '_'*lines, enums = '{}:'.format(name))
		cmds.setAttr(line_attr,e=True, lock = True)

		return line_attr

	#----------------------------------------------------------------------------------------------------------------

	def string_attr(self, input = '', name = 'name', string = 'string'):
		'''
		create a string attr in selected node
		'''
		cmds.addAttr(input, ln=name, dt="string")
		cmds.setAttr('{}.{}'.format(input,name), string, type="string")

		return '{}.{}'.format(input,name)
	#----------------------------------------------------------------------------------------------------------------

	def connect_rotate_order(self, input = '', object = 'controller'):
		'''
		create a rotate order attr and connects it to the desire ogject
		'''

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
		'''
		duplicate any herachy with no duplicated names but with clean ones
		'''
		if input != '':
			self.input = [input]
			
		else:	
			self.input = input

		self.check_input('duplicate_change_names')	

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

		#return list
		return return_list[-1]
	#----------------------------------------------------------------------------------------------------------------

	def bounding_cube(self, input = '', size = 1, name = '', axis = setup['twist_axis']):
		'''
		create a ctrl cube with coverage for the full limb, so its like a bounding box in lenght
		'''

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
		'''
		create a shape with an attr to put inside all the ctrls, 
		if the initial shape doesnt exists it create it, else it just put it inside
		input = a list
		
		'''

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
	                self.asign_color(Curva, color = color)
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
		#create a simple linear curve between 2 joints 
	   
	   pos_a = cmds.xform(start, q=True,t=True, ws=True)
	   pos_b = cmds.xform(end, q=True,t=True, ws=True) 
	   
	   crv = cmds.curve(d=1, p=[pos_a,pos_b], k=[0,1], n = '{}{}'.format(start, nc['curve']))
	   
	   return crv

	#----------------------------------------------------------------------------------------------------------------		

	def create_ik_spline_twist(self, start, end, curve):
		#create ik spline based on 2 joints and one curve

	    # ik spline solver
	    ikSpline = cmds.ikHandle(sj=start,
	                             ee=end,
	                             sol='ikSplineSolver',
	                             n=start + '_Twist' + nc['ik_spline'],
	                             c = curve,
	                             ccv=False,
	                             pcv = False)

	    effector_spline = cmds.rename(ikSpline[1],
	                                 start + '_Twist' + nc['effector'])
	    ikSpline = ikSpline[0]
	        
	    return {'ikHandle': ikSpline, 'effector': effector_spline}

	#----------------------------------------------------------------------------------------------------------------		

	def connect_md_node(self, in_x1 = '', in_x2 = 1.0, out_x = '', mode = 'mult', name = '', force = False):
		'''
		this wil create a md node for you to connect something in the input 1x, to output 1x and a value
		mode = mult or devide
		'''
		if name == '':
			try:
				name = in_x1.split('.')[0]
			except:
				name = in_x2.split('.')[0]

		#create md node with correct value and mode
		md_node = cmds.shadingNode('multiplyDivide', asUtility=1, n  = '{}{}'.format(name, nc['multiplyDivide']))

		if mode == 'divide':
			cmds.setAttr(str(md_node)+'.operation', 2)
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
		if force: 
				cmds.connectAttr('{}.output.outputX'.format(md_node), out_x, f=True)
		else:
			cmds.connectAttr('{}.output.outputX'.format(md_node), out_x)

		#return node
		return md_node

	#----------------------------------------------------------------------------------------------------------------

	def trasform_on_sel(self, transform='', name='Temp'):
		'''
		position a transform node in desire selection, if there is no trasnform it will create a joint for you
		'''
		
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
	#connect two transforms with a line
	def connect_with_line(self, start='', end=''):
		'''
		create a line in between 2 transforms (start and end)
		'''
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
		cmds.setAttr("{}.overrideEnabled".format(cv), 1)
		cmds.setAttr("{}.overrideDisplayType".format(cv), 2)

		cmds.setAttr('{}.v'.format(cluster_start[1]), 0)
		cmds.setAttr('{}.v'.format(cluster_end[1]), 0)

		connect_with_line_assets = [cv, cluster_start[1], cluster_end[1]]

		return connect_with_line_assets

	#----------------------------------------------------------------------------------------------------------------
	#lock and unlock nodes
	def lock_node(self, input = '', unlock=False):
		'''
		this will lock and unlock (with the attr True) any input node
		'''			
		if input == '':
			input = cmds.ls(sl=True)
		
		for node in input:
			if unlock ==True:
				cmds.lockNode(node, lock=False)
			else:
				cmds.lockNode(node, lock=True)


	#----------------------------------------------------------------------------------------------------------------

	#tail/ finger, curl FK pero en kinnematics
	#world mirror para sistemas completos
	#Sliders
	#skinning pero puede ser una clase nueva: bind skin, transfer skin, select from, copy, add, remove, remove unused, copy weight, paste weight, Mirror, joints edit on, joints edit off, import y export
	#controles con forma de base, root, cog, orient templates
	#show/hide by type

	#revisar bounding cubes en setup
	#REVISAR NOMBRES DE CLUSTERS


#tool = Tools_class()

