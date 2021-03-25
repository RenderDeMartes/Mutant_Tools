'''
version: 1.0.0
date: 21/04/2020


#----------------
how to: 
	
import RdM_ScriptTools
from RdM_ScriptTools import main_rdm
reload(RdM_ScriptTools.main_rdm)

rdm = main_rdm.RdM()
rdm.FUNC(ARGUMENTS)

#----------------
dependencies:   
	
math
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
version = '3.0.0'

#loading screen so it looks nicer
import time
from maya import cmds
'''
cmds.progressWindow(title='Loading RdM Tools V3', progress=0, status='Starting', isInterruptable=True,maxValue=3)
time.sleep(2)
cmds.progressWindow(edit=True, progress=1, status='Hello!'.format(version))
time.sleep(1)
cmds.progressWindow(edit=True, progress=2, status='Loading RdM Tools V{}'.format(version))
'''
import maya.mel
import pymel.core as pm
from maya import OpenMaya

import os
import json
import math

try: 
	import tools
	reload(tools)
	import kinematics
	reload(kinematics)
	import modules
	reload(modules)
	import blocks
	reload(blocks)
except:
	import RdM_ScriptTools
	from RdM_ScriptTools import tools
	reload(RdM_ScriptTools.tools)
	from RdM_ScriptTools import kinematics
	reload(RdM_ScriptTools.kinematics)
	from RdM_ScriptTools import modules
	reload(RdM_ScriptTools.modules)
#----------------

class RdM(modules.Modules_class):

	def __init__ (self):
		
		if cmds.objExists('RdM_Tools_V3'):
			print ('RdM_Tools V3 node created on:{} with version {}'.format(cmds.getAttr('RdM_Tools_V3.Date'),cmds.getAttr('RdM_Tools_V3.Version')))

		else:
			rdm_node = cmds.createNode('network',n='RdM_Tools V3')
			date_attr = self.string_attr(rdm_node, 'Date', time.ctime())
			cmds.setAttr(date_attr, l=True)
			version_attr = self.string_attr(rdm_node, 'Version', version)
			cmds.setAttr(version_attr, l=True)

		OpenMaya.MGlobal.displayInfo('RdM Tools Verion {}'.format(version))

	

'''
cmds.progressWindow(edit=True, progress=3, status='Enjoy :)')
cmds.progressWindow(endProgress=1)
'''