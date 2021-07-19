'''
version: 1.0.0
date: 21/04/2020


#----------------
how to: 
	
import Mutant_Tools
import Mutant_Tools.Utils
from Mutant_Tools.Utils import modules
imp.reload(Mutant_Tools.Utils.modules)

modules = modules.RdM()
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
licence: https://www.eulatemplate.com/live.php?token=ySe25XC0bKARQymXaGQGR8i4gvXMJgVS
author:  Esteban Rodriguez <info@renderdemartes.com>

'''

import maya.mel
from maya import cmds
#import pymel.core as pm
from maya import OpenMaya

import os
import imp
import json

try: 
	import tools
	imp.reload(tools)
	import kinematics
	imp.reload(kinematics)
except:
	import Mutant_Tools
	import Mutant_Tools.Utils
	from Mutant_Tools.Utils import tools
	imp.reload(Mutant_Tools.Utils.tools)
	from Mutant_Tools.Utils import kinematics
	imp.reload(Mutant_Tools.Utils.kinematics)


#----------------------------------------------------------------------------------------------------------------

#Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = PATH.replace('\\Utils', '//Config')

JSON_FILE = (PATH +'/name_conventions.json')
with open(JSON_FILE) as json_file:
	nc = json.load(json_file)
SETUP_FILE = (PATH +'/rig_setup.json')
with open(SETUP_FILE) as setup_file:
	setup = json.load(setup_file)


#----------------------------------------------------------------------------------------------------------------

class Modules_class(kinematics.Kinematics_class):

	def __init__ (self):
		''

#----------------------------------------------------------------------------------------------------------------

	def create_block(self, name = 'Mutant', icon = 'Limb', attrs = {'attrs':'something'}, build_command = 'print("Test")', import_command = 'print("Test2")'):

		PATH = os.path.dirname(__file__)
		PATH = PATH.replace('\\Utils', '//Icons//') #change this path depending of the folder
		#print (PATH)
		icon = PATH + icon + '.png'

		cmds.select(cl=True)
		block = cmds.container(name = name + nc['module'],type='dagContainer')
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
		#-----------------------------------------------------------------------------------------

		return block,config
#----------------------------------------------------------------------------------------------------------------

	def move_outliner(self, input = '', up = False, down = False):
		
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
		
		cmds.select(cl=True)
		joint = cmds.joint(n = name + nc['guide'])
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

		if setup['axis_helper'] == 'True':
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
	
		if input =='':
			input = cmds.ls(sl=True)[0]

		cmds.makeIdentity(input, apply=True, t=True, r=True, s=True ,n=False, pn=1)
		try:
			if setup['twist_axis'] == 'Y':
				cmds.joint(input, e = True, oj = 'yxz' , ch=True, secondaryAxisOrient = '{}'.format(setup['secondaryAxisOrient']))
			elif setup['twist_axis'] == 'X':
				cmds.joint(input, e = True, oj = 'xyz' , ch=True, secondaryAxisOrient = '{}'.format(setup['secondaryAxisOrient']))
			else:
				cmds.joint(input, e = True, oj = 'zyx' , ch=True, secondaryAxisOrient = '{}'.format(setup['secondaryAxisOrient']))
		except:
			print ('Error while orienting joints, sorry')
			
#----------------------------------------------------------------------------------------------------------------

	def ask_name(self, text = '', ask_for = 'Name', check_split = False):
		ask_name = cmds.promptDialog(
						title='Name Block',
						message=ask_for,
						button=['OK', 'Cancel'],
						defaultButton='OK',
						cancelButton='Cancel',
						dismissString='Cancel',
						tx = text)

		if ask_name == 'OK':
			if cmds.objExists(cmds.promptDialog(query=True, text=True).replace(',','_')+nc['module']):
				print ('Name exists error')
				cmds.confirmDialog( title='Error', 
									message='Error: Block name already exists', 
									button=["Oh! ok!"])

			if check_split == True:
				if cmds.objExists(cmds.promptDialog(query=True, text=True).split(',')[0]+nc['module']):
					print ('Name exists error')
					cmds.confirmDialog( title='Error', 
										message='Error: Block name already exists', 
										button=["Oh! ok!"])

			return cmds.promptDialog(query=True, text=True)	

		else:
			cmds.error('We need a name :)')
			

#----------------------------------------------------------------------------------------------------------------

	def dual_ask_name(self, textA = 'Name 1', text_B = 'Name 2', command = ''):

		class dual_ask():

			def __init__(self):
				self.input1 = ''
				self.input2 = ''
				
				self.show_window()

			def show_window(self):

				windowID = 'Dual_Name'
			
				if cmds.window(windowID, exists = True):
					cmds.deleteUI(windowID)
			
				def close_UI(*args):
				
					windowID = 'Dual Name'
				
					self.input1 = cmds.textFieldGrp( 'textField_A', query = True, text = True)
					self.input2 = cmds.textFieldGrp( 'textField_B', query = True, text = True)
					return 
					cmds.deleteUI(window)

					exec(command)

				window = cmds.window(windowID)
				cmds.rowColumnLayout()
			
				cmds.textFieldGrp('textField_A', label = textA )
				cmds.textFieldGrp('textField_B', label = text_B )
			
				cmds.button(label = 'Create', command = close_UI)
			
				cmds.showWindow(window)

		#names = dual_ask()

#----------------------------------------------------------------------------------------------------------------

	def duplicate_and_remove_guides(self, input = ''):
		'this will ducplicate the top chain joint and change the _Guide for _Jnt and rename all the chils plus parent to the world'

		if input == '':
			input = cmds.ls(sl=True)[0]

		#duplicate the joints
		clean_joints = cmds.duplicate(input , to = True, n = input.replace(nc['guide'], nc['joint']), rc=True)
		for jnt in clean_joints:
			if nc['guide'] in str(jnt):
				jnt = cmds.rename(jnt, jnt.replace(nc['guide'], nc['joint']))

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

#----------------------------------------------------------------------------------------------------------------

	def build_baseA(self, name='Asset_Name', size = 1):
		'''
		This will crate the base structure for any kinf of rig with the same base sctructure
		'''

		#main grp
		main_grp = cmds.group(em=True, name = name +  nc['group'])

		#create base Groups
		base_groups = setup['base_groups'] 
		print (base_groups)

		for grp in base_groups:
			base_grp = cmds.group(em=True, n = base_groups[grp] + nc['group'])
			cmds.parent(base_grp, main_grp)
		
		geo_groups = setup['geo_groups']
		print (geo_groups)		
		for grp in geo_groups:
			geo_grp = cmds.group(em=True, n = geo_groups[grp] + nc['group'])
			cmds.parent(geo_grp, base_groups['geometry']+nc['group'])		
				
		rig_groups = setup['rig_groups']
		print (rig_groups)		
		for grp in rig_groups:
			rig_grp = cmds.group(em=True, n = rig_groups[grp] + nc['group'])
			cmds.parent(rig_grp, base_groups['rig']+nc['group'])	

		
		#create the base controllers

		global_ctrl = self.curve(type = 'root', custom_name=True, name = 'Global' + nc['ctrl'], size = size)
		global_offset = self.root_grp()
		mover_ctrl = self.curve(type = 'mover', custom_name=True, name = 'Mover'  + nc['ctrl'],size = size)
		mover_offset = self.root_grp()
		gimbal_ctrl = self.curve(type = 'mover', custom_name=True, name = 'Mover'  + nc['gimbal_ctrl'], size = size*0.9)

		cmds.parent(gimbal_ctrl, mover_ctrl)
		cmds.parent(mover_offset, global_ctrl)
		cmds.parent(global_offset, 'Ctrl_Grp')

		vis_Attr = self.new_attr(input= mover_ctrl, name = 'Gimbal', min = 0 , max = 1, default = 0) 
		cmds.connectAttr(vis_Attr, cmds.listRelatives(gimbal_ctrl,s=True)[0]+'.v')

		#group for ctrls inside the gimal
		main_ctrl_grp = cmds.group(em = True, name = setup['main_ctrl_grp'] + nc['group'])
		cmds.parent(main_ctrl_grp, gimbal_ctrl)

		#clean
		self.hide_attr(input = mover_ctrl , s = True)
		self.hide_attr(input = gimbal_ctrl , s = True)

		return(global_ctrl, mover_ctrl, gimbal_ctrl)

#----------------------------------------------------------------------------------------------------------------

	def check_is_there_is_base(self, base = 'BaseA'):

		'this one is ment to be in the start of all the modules so if there is no base it will create one for you'

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

		log_file = PATH.replace('/Config', '/log.txt')

		if mode == 'create': 
			print (log_file)
			cmds.scriptEditorInfo(historyFilename=log_file, writeHistory=True)
		elif mode == 'stop':
			cmds.scriptEditorInfo(writeHistory=False)
		elif mode == 'clear':
			open(log_file, 'w').close()
		else:
			return log_file


