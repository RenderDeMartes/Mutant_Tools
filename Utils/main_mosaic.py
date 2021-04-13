'''
version: 1.0.0
date: 21/04/2020


#----------------
how to: 
	
import Mosaic_Tools
import Mosaic_Tools.Utils
from Mosaic_Tools.Utils import main_mosaic
imp.reload(Mosaic_Tools.Utils.main_mosaic)

mosaic = main_mosaic.Mosaic()
mosaic.FUNC(ARGUMENTS)

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
modules.Modules_class


#----------------
licence: https://www.eulatemplate.com/live.php?token=ySe25XC0bKARQymXaGQGR8i4gvXMJgVS
author:  Esteban Rodriguez <info@renderdemartes.com>

'''
version = '1.0.0'

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
import imp
import json
import math


try: 
	import tools
	imp.reload(tools)
	import kinematics
	imp.reload(kinematics)
	import modules
	imp.reload(modules)
	import blocks
	imp.reload(blocks)
except:
	import Mosaic_Tools
	import Mosaic_Tools.Utils
	from Mosaic_Tools.Utils import tools
	imp.reload(Mosaic_Tools.Utils.tools)
	from Mosaic_Tools.Utils import kinematics
	imp.reload(Mosaic_Tools.Utils.kinematics)
	from Mosaic_Tools.Utils import modules
	imp.reload(Mosaic_Tools.Utils.modules)
#----------------

class Mosaic(modules.Modules_class):

	def __init__ (self):
		
		if cmds.objExists('Mosaic_Tools'):
			print ('Mosaic node created on:{} with version {}'.format(cmds.getAttr('Mosaic_Tools.Date'),cmds.getAttr('Mosaic_Tools.Version')))

		else:
			mosaic_node = cmds.createNode('network',n='Mosaic_Tools')
			date_attr = self.string_attr(mosaic_node, 'Date', time.ctime())
			cmds.setAttr(date_attr, l=True)
			version_attr = self.string_attr(mosaic_node, 'Version', version)
			cmds.setAttr(version_attr, l=True)

		OpenMaya.MGlobal.displayInfo('Mosaic_Tools {}'.format(version))

	

'''
cmds.progressWindow(edit=True, progress=3, status='Enjoy :)')
cmds.progressWindow(endProgress=1)
'''