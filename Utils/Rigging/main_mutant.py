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
www.mutanttools.com
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

	# ---------------------------------------------------

	def get_github_latest_release(self):
		"""
		Retrieves the latest release info from the Mutant_Tools GitHub repo's public API.
		Works without any authentication (public repo), so it works on machines that
		are not logged into GitHub.

		Returns:
			dict: The decoded JSON of the latest release (tag_name, zipball_url, html_url, etc.)
		"""
		url = 'https://api.github.com/repos/RenderDeMartes/Mutant_Tools/releases/latest'
		request = urllib.request.Request(url, headers={'Accept': 'application/vnd.github+json',
														'User-Agent': 'Mutant_Tools-Updater'})
		response = urllib.request.urlopen(request, timeout=10)
		return json.loads(response.read().decode('utf-8'))

	# ---------------------------------------------------

	def check_for_updates(self, silent=True):
		"""
		Compares the local version against the latest GitHub release. If a newer release
		is available, asks the user if they want to download and install it automatically.

		Args:
			silent (bool): If False, also informs the user when no update is needed or the
				check failed. If True (default, used on startup), stays quiet unless an
				update is found.
		"""
		version_data = self.read_json(path=os.path.join(FOLDER, 'config'), json_file='version.json')

		if version_data.get('dev_mode') not in (False, 'Off', 'off', 0, None):
			if not silent:
				cmds.confirmDialog(title='Mutant Tools', message='Dev mode is on, update check skipped.', button=['OK'])
			return

		try:
			release = self.get_github_latest_release()
		except Exception:
			if not silent:
				cmds.confirmDialog(title='Mutant Tools', message='Could not reach GitHub to check for updates.', button=['OK'])
			return

		latest_version = release.get('tag_name', '').lstrip('vV')
		local_version = self.get_local_version()

		if latest_version and latest_version != local_version:
			answer = cmds.confirmDialog(
				title='Update Available',
				message='A new version of Mutant Tools is available ({} -> {}).\n\nDownload and install it now?'.format(local_version, latest_version),
				button=['Update', 'Later'],
				defaultButton='Update',
				cancelButton='Later',
				dismissString='Later')
			if answer == 'Update':
				self.install_github_release(release)
		elif not silent:
			cmds.confirmDialog(title='Mutant Tools', message='You are running the latest version ({}).'.format(local_version), button=['OK'])

	# ---------------------------------------------------

	def install_github_release(self, release):
		"""
		Downloads a GitHub release's source zip and installs it over the current
		Mutant_Tools folder, mirroring the copy done by easy_install.py.

		Args:
			release (dict): A release dict as returned by get_github_latest_release().
		"""
		import zipfile
		import tempfile
		import shutil
		from distutils.dir_util import copy_tree

		zip_url = release.get('zipball_url')
		if not zip_url:
			OpenMaya.MGlobal.displayWarning('Mutant Tools: update download link not found.')
			return

		tmp_dir = tempfile.mkdtemp(prefix='mutant_tools_update_')
		zip_path = os.path.join(tmp_dir, 'update.zip')

		try:
			request = urllib.request.Request(zip_url, headers={'User-Agent': 'Mutant_Tools-Updater'})
			response = urllib.request.urlopen(request, timeout=120)
			with open(zip_path, 'wb') as out_file:
				shutil.copyfileobj(response, out_file)

			with zipfile.ZipFile(zip_path, 'r') as zip_file:
				zip_file.extractall(tmp_dir)

			#GitHub zipballs are wrapped in a single top-level folder, eg RenderDeMartes-Mutant_Tools-<sha>
			extracted_root = None
			for entry in os.listdir(tmp_dir):
				entry_path = os.path.join(tmp_dir, entry)
				if os.path.isdir(entry_path):
					extracted_root = entry_path
					break

			if not extracted_root:
				OpenMaya.MGlobal.displayWarning('Mutant Tools: could not find extracted update files.')
				return

			copy_tree(extracted_root, FOLDER)
			OpenMaya.MGlobal.displayInfo('Mutant Tools updated. Restart Maya to load the new version.')
			cmds.confirmDialog(title='Mutant Tools', message='Update installed.\n\nPlease restart Maya to load the new version.', button=['OK'])

		except Exception as e:
			OpenMaya.MGlobal.displayWarning('Mutant Tools: update failed - {}'.format(e))
		finally:
			shutil.rmtree(tmp_dir, ignore_errors=True)

