from __future__ import absolute_import
'''
version: 1.0.0
date: 21/04/2020


#----------------
how to: 
	
import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()
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


import time
from maya import cmds
try:import urllib.request
except:pass

'''
cmds.progressWindow(title='Loading RdM Tools V3', progress=0, status='Starting', isInterruptable=True,maxValue=3)
time.sleep(2)
cmds.progressWindow(edit=True, progress=1, status='Hello!'.format(version))
time.sleep(1)
cmds.progressWindow(edit=True, progress=2, status='Loading RdM Tools V{}'.format(version))
'''

import maya.mel as mel
from maya import OpenMaya

import os
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import json
import math
from pathlib import Path

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
	import Mutant_Tools
	import Mutant_Tools.Utils.Rigging
	from Mutant_Tools.Utils.Rigging import tools
	reload(Mutant_Tools.Utils.Rigging.tools)
	from Mutant_Tools.Utils.Rigging import kinematics
	reload(Mutant_Tools.Utils.Rigging.kinematics)
	from Mutant_Tools.Utils.Rigging import modules
	reload(Mutant_Tools.Utils.Rigging.modules)

#---------------------------------------------------
#Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-2]
FOLDER=''
for f in PATH_PARTS:
	FOLDER = os.path.join(FOLDER, f)

#nc, curve_data, setup = tools.import_configs()


class Mutant(modules.Modules_class):

	def __init__(self):
		super(Mutant, self).__init__()

		version = self.get_local_version()

		if cmds.objExists('Mutant_Tools'):
			#print ('Mutant node created on:{} with version {}'.format(cmds.getAttr('Mutant_Tools.Date'),cmds.getAttr('Mutant_Tools.Version')))
			''

		else:
			Mutant_node = cmds.createNode('network',n='Mutant_Tools')
			date_attr = self.string_attr(Mutant_node, 'Date', time.ctime())
			cmds.setAttr(date_attr, l=True)
			version_attr = self.string_attr(Mutant_node, 'Version', version)
			cmds.setAttr(version_attr, l=True)

		#OpenMaya.MGlobal.displayInfo('Mutant_Tools {}'.format(version))


	#---------------------------------------------------

	def get_online_version(self):
		"""
		Retrieves the online version of a tool from a specified URL.

		Returns:
		    str or None: The online version of the tool if available, None otherwise.

		Raises:
		    None

		This function retrieves the online version of a tool by scraping a specific URL. It starts by defining the URL where the version information is
		located. The 'urlopen' function from the 'urllib.request' module is used to open the URL and read its contents.

		The function iterates over the lines read from the URL and searches for a line containing the keyword 'Version'. Once found, it extracts the version
		information from the line.

		The extracted online version is then processed to remove any unwanted characters or formatting. If the online version is empty or cannot be
		determined, the function returns None. Otherwise, it returns the online version.

		Note:
		    This function relies on the 'urllib.request' module, so make sure it is imported before using this function.
		"""

		version_line = str()
		url = 'https://mutanttools.com/current_version/'
		oURL = urllib.request.urlopen(url)

		url_lines = oURL.readlines()
		for line in url_lines:
			if 'Version' in str(line):
				version_line = str(line)

		online_version = version_line.replace("b'<p>Version=", '')
		online_version = online_version.replace("</p>\\n'", '')

		if online_version == []:
			return None
		elif online_version == '':
			return None
		else:
			return online_version

	# ---------------------------------------------------

	def get_local_version(self):
		"""
		Retrieves the local version of the tool.

		Returns:
		    str or None: The local version of the tool if available, None otherwise.

		Raises:
		    None

		This function reads the local version of the tool from a JSON file. It starts by specifying the path to the JSON file containing the version
		information. The 'read_json' method is then used to read the contents of the file.

		The function retrieves the version value from the JSON data and returns it. If the local version != available or cannot be determined, the
		function returns None.

		Note:
		    This function assumes that the 'read_json' method is implemented and correctly reads the version information from the JSON file.
		"""
		local_version = self.read_json(path = os.path.join(FOLDER, 'config'), json_file = 'version.json')
		return local_version['version']

	# ---------------------------------------------------

	def compare_versions(self):
		"""
		Compares the local version with the online version and displays a warning if an update is available.

		Returns:
		    None

		Raises:
		    None

		This function compares the local version of the tool with the online version retrieved from the website. It first checks if the tool is in
		development mode based on the 'dev_mode' flag in the version data. If the tool is in development mode, the function prints a message and
		returns without further checks.

		If the tool != in development mode, the function retrieves the local version using the 'get_local_version' method and the online version
		using the 'get_online_version' method. It then compares the two versions and displays a warning message if they are different.

		Note:
		    This function assumes that the 'get_online_version' and 'get_local_version' methods are implemented and correctly retrieve the online
		    and local versions, respectively.
		"""

		#if dev dont look for versions
		version_data = self.read_json(path = os.path.join(FOLDER, 'config'), json_file = 'version.json')

		if version_data['dev_mode']:
			print('Mutant != searching for updates...')
			return
		try:
			print('Searching for updates..')
			online = self.get_online_version()
			offline = self.get_local_version()
			if online != offline:
				print('Update Available', offline, online)
				OpenMaya.MGlobal.displayWarning('New Version Available... Go to mutanttools.com to download it!')

		except:
			pass

