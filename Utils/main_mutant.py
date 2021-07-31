'''
version: 1.0.0
date: 21/04/2020


#----------------
how to: 
	
import Mutant_Tools
import Mutant_Tools.Utils
from Mutant_Tools.Utils import main_mutant
imp.reload(Mutant_Tools.Utils.main_mutant)

Mutant = main_mutant.Mutant()
Mutant.FUNC(ARGUMENTS)

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
licence: https://www.eulatemplate.com/live.php?token=FGISW7ApRfgywum6murbBmLcusKONzkv
author:  Esteban Rodriguez <info@mutanttools.com>

'''

version = '0.01'

#loading screen so it looks nicer
import time
from maya import cmds
import urllib.request

'''
cmds.progressWindow(title='Loading RdM Tools V3', progress=0, status='Starting', isInterruptable=True,maxValue=3)
time.sleep(2)
cmds.progressWindow(edit=True, progress=1, status='Hello!'.format(version))
time.sleep(1)
cmds.progressWindow(edit=True, progress=2, status='Loading RdM Tools V{}'.format(version))
'''
import maya.mel
#import pymel.core as pm
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
	import Mutant_Tools
	import Mutant_Tools.Utils
	from Mutant_Tools.Utils import tools
	imp.reload(Mutant_Tools.Utils.tools)
	from Mutant_Tools.Utils import kinematics
	imp.reload(Mutant_Tools.Utils.kinematics)
	from Mutant_Tools.Utils import modules
	imp.reload(Mutant_Tools.Utils.modules)
#----------------

class Mutant(modules.Modules_class):

	def __init__ (self):
		
		if cmds.objExists('Mutant_Tools'):
			print ('Mutant node created on:{} with version {}'.format(cmds.getAttr('Mutant_Tools.Date'),cmds.getAttr('Mutant_Tools.Version')))

		else:
			Mutant_node = cmds.createNode('network',n='Mutant_Tools')
			date_attr = self.string_attr(Mutant_node, 'Date', time.ctime())
			cmds.setAttr(date_attr, l=True)
			version_attr = self.string_attr(Mutant_node, 'Version', version)
			cmds.setAttr(version_attr, l=True)

		OpenMaya.MGlobal.displayInfo('Mutant_Tools {}'.format(version))

		#self.check_update()

	def check_update(self):

		version_line = ''
		url = 'https://mutanttools.com/current_version/'
		oURL = urllib.request.urlopen(url)

		url_lines = oURL.readlines()
		for line in url_lines:
			if 'Version' in str(line):
				version_line = str(line)

		current_version = version_line.replace("b'<p>Version=", '')
		current_version = current_version.replace("</p>\\n'", '')

		if current_version == []:
			pass
		elif current_version == '':
			pass
		else:
			if current_version == version:
				pass
			else:
				OpenMaya.MGlobal.displayInfo('Mutant_Tools: There is a new version available: Installed: {}, Available: {}'.format(version, current_version))

		return current_version

'''
cmds.progressWindow(edit=True, progress=3, status='Enjoy :)')
cmds.progressWindow(endProgress=1)
'''