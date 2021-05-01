'''
version: 1.0.0
date: 21/04/2020


#----------------
how to: 
	
import Mosaic_Tools
import Mosaic_Tools.Utils
from Mosaic_Tools.Utils import modules
imp.reload(Mosaic_Tools.Utils.modules)

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
import pymel.core as pm
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
	import Mosaic_Tools
	import Mosaic_Tools.Utils
	from Mosaic_Tools.Utils import tools
	imp.reload(Mosaic_Tools.Utils.tools)
	from Mosaic_Tools.Utils import kinematics
	imp.reload(Mosaic_Tools.Utils.kinematics)


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

	def create_block(self, name = 'Mosaic', icon = 'Limb', attrs = {'attrs':'something'}, build_command = 'print("Test")', import_command = 'print("Test2")'):

		PATH = os.path.dirname(__file__)
		PATH = PATH.replace('\\Utils', '//Icons//') #change this path depending of the folder
		#print (PATH)
		icon = PATH + icon + '.png'

		cmds.select(cl=True)
		block = cmds.container(name = name + nc['module'],type='dagContainer')
		cmds.setAttr('{}.iconName'.format(block), icon, type="string")
		self.hide_attr(t=True, r=True, s=True,v=True)

		if cmds.objExists('Mosaic_Build'):
			pass
		else:
			cmds.group(n = 'Mosaic_Build', em=True)
		print (block)
		cmds.parent(block,'Mosaic_Build')

		#create network node with all the attrs
		config = cmds.createNode('network', n = '{}_Config'.format(name))
		cmds.connectAttr('{}.nodeState'.format(config), '{}.nodeState'.format(block))
		
		build_command = self.string_attr(input = config, name = 'Build_Command', string = build_command)
		cmds.setAttr(build_command, lock=True)
		import_command = self.string_attr(input = config, name = 'Import_Command', string = import_command)
		cmds.setAttr(import_command, lock=True)
		
		for attr in attrs:
			if 'string' in attr:
				self.string_attr(input = config, name = attr.split('_')[0], string = attrs[attr])
			elif 'enum' in attr:
				self.new_enum(input= config, name = attr.split('_')[0], enums = attrs[attr])
			elif 'float' in attr:
				self.new_attr_interger(input= config, name = attr.split('_')[0], min = 1 , max = 20, default = int(attrs[attr]))
			elif 'bool' in attr:
				self.new_boolean(input= config, name = attr.split('_')[0], dv = attrs[attr])
			
			
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
		joint = cmds.joint(n = name + nc['joint'])
		arrow = self.curve(type = '2dArrow')
		sphere = self.curve(type = 'sphere')

		arrowAxis = self.curve(type = '2dArrow')
		cmds.rotate(90,90,0,cmds.listRelatives(arrowAxis, s=True)[0] + '.cv[0:9]')
		arrowFront = self.curve(type = '2dArrow')
		cmds.rotate(90,0,90,cmds.listRelatives(arrowFront, s=True)[0] + '.cv[0:9]')

		self.asign_color(input = cmds.listRelatives(arrow, s=True)[0], color = 'green')
		self.asign_color(input = cmds.listRelatives(sphere, s=True)[0])
		self.asign_color(input = cmds.listRelatives(arrowAxis, s=True)[0], color = 'red')
		self.asign_color(input = cmds.listRelatives(arrowFront, s=True)[0], color = 'blue')

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

	def ask_name(self, text = ''):
		ask_name = cmds.promptDialog(
						title='Name Block',
						message='Name:',
						button=['OK', 'Cancel'],
						defaultButton='OK',
						cancelButton='Cancel',
						dismissString='Cancel',
						tx = text)

		if ask_name == 'OK':
				return cmds.promptDialog(query=True, text=True)	
		else:
			cmds.error('We need a name :)')

#----------------------------------------------------------------------------------------------------------------

	def build_base(self, name='Asset_Name', size = 1):
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
		self.hide_attr(input =mover_ctrl , s = True)
		self.hide_attr(input =gimbal_ctrl , s = True)

#----------------------------------------------------------------------------------------------------------------



		

