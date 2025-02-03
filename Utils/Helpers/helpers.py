from __future__ import absolute_import
'''
version: 1.0.0
date: 21/04/2020


#----------------
how to:

import Mutant_Tools
import Mutant_Tools.Utils.Helpers
from Mutant_Tools.Utils.Helpers import helpers
reload(Mutant_Tools.Utils.Helpers.helpers)

mh = helpers.Helpers()
mh.FUNC(ARGUMENTS)

#----------------
dependencies:


#----------------
licence: https://www.eulatemplate.com/live.php?token=FGISW7ApRfgywum6murbBmLcusKONzkv
author:  Esteban Rodriguez <info@mutanttools.com>

'''

from maya import cmds
import json
from pathlib import Path
import os

PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-2]
FOLDER=''
for f in PATH_PARTS:
	FOLDER = os.path.join(FOLDER, f)

class Helpers(object):

	def __init__(self):
		''

	# ----------------------------------------------------------------------------------------------------------------

	def capture_viewport(self, image_name=None,
							   path= None,
							   width=1920,
							   height=1080,
							   ornaments=False):
		"""

		Args:
			image_name:
			path:
			width:
			height:
			ornaments:

		Returns:

		"""
		image_file = path + image_name
		exported_image = cmds.playblast(orn=ornaments, c='jpg', st=cmds.currentTime(query=True),
										et=cmds.currentTime(query=True), w=width, h=height, p=75, v=False, fo=True,
										fmt='image', f=image_file, cc=True, os=True, fp=1)
		time_slider = int(cmds.currentTime(query=True))
		exported_image = exported_image.replace('.####', '.{}'.format(time_slider))

		return exported_image

	# ----------------------------------------------------------------------------------------------------------------

	def write_json(self, path, json_file, data):
		""" Will write json file with data

		Args:
			path: path to put the json file in (rembember to use \\ to define the folders)
			json_file: json file name
			data: dictionary to sabe

		Returns: string json file full path

		"""

		write_json = os.path.join(path, json_file)

		with open(write_json, 'w') as f:
			json.dump(data, f, ensure_ascii=False, indent=4)

		return write_json

	# ----------------------------------------------------------------------------------------------------------------

	def read_json(self, path, json_file):
		""" will read json file

		Args:
			path: path to where the json file is (rembember to use \\ to define the folders)
			json_file: json file name

		Returns: dictionary with data

		"""
		#Force to allow only path and not json file
		try:
			json_data = os.path.join(path, json_file)

			with open(json_data) as f:
				data = json.load(f)
		except:
			with open(path) as f:
				data = json.load(f)

		return data

	# ----------------------------------------------------------------------------------------------------------------

	def reset_to_default(self):
		"""
		--------------------------------------------------------------------------------------------------------------------
		resetControllers.py - Python Script
		--------------------------------------------------------------------------------------------------------------------
		Copyright 2012 Carlos Chacon L. All rights reserved.

		DESCRIPTION:
		Resets the selected controllers to their default value.

		USAGE:
		*Select the controllers to be reset.
		*Run the script.

		AUTHOR:
		Carlos Chacon L. (caedo.00 at gmail dot com)
		--------------------------------------------------------------------------------------------------------------------
		"""

		def isSingleAttribute(attr, obj):
			"""
				Checks if the attr is single or multiple value.
				"""
			return True if (cmds.attributeQuery(attr, node=obj, nc=True) is None) else False

		def resetController(controller):
			"""
			Resets to zero all the non-locked attributes from a controller
			"""
			controller_attrs = cmds.listAttr(controller, k=True)
			for attr in controller_attrs:
				if (isSingleAttribute(attr, controller)):
					default_value = cmds.attributeQuery(attr, ld=True, node=controller)[0]
					try:
						cmds.setAttr(controller + "." + attr, default_value)
					except:
						pass

		def resetControllers(controllers):
			"""
			Resets multiple controllers.
			"""
			if (len(controllers) > 0):
				for controller in controllers:
					resetController(controller)
				print("Controllers reset successfully")
			else:
				print("No Controllers selected")

		resetControllers(cmds.ls(sl=True))

	# ----------------------------------------------------------------------------------------------------------------

	def read_setup_file(self):
		''

	def write_setup_file(self, old_data):
		''

	def get_inbetween_text(self, start, finish):
		''

	# ----------------------------------------------------------------------------------------------------------------

	def export_window(self, extension = ".ma"):
		if extension == 'maya_file':
			basicFilter="Maya Files (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb)"
		else:
			basicFilter = '*' + extension
		dialog = cmds.fileDialog2(fileFilter=basicFilter, fileMode=0, caption="Save As")
		return dialog

	# ----------------------------------------------------------------------------------------------------------------

	def import_window(self, extension = ".ma"):
		if extension == 'maya_file':
			basicFilter="Maya Files (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb)"
		else:
			basicFilter = '*' + extension
		dialog = cmds.fileDialog2(fileFilter=basicFilter, fileMode=1, caption="Open")
		return dialog

	# ----------------------------------------------------------------------------------------------------------------

	def folder_window(self):
		dialog = cmds.fileDialog2(dialogStyle=1, fileMode=3, caption="Open")
		return dialog[0]

	# ----------------------------------------------------------------------------------------------------------------
	def find_user_show(self):

		try:
			settings = self.read_json(path=os.path.join(cmds.internalVar(usd=True)),json_file='MutantTools.settings')
		except:
			self.write_json(path=os.path.join(cmds.internalVar(usd=True)),json_file='MutantTools.settings', data = {'user': False})
			settings = self.read_json(path=os.path.join(cmds.internalVar(usd=True)),json_file='MutantTools.settings')

		if 'user' in settings:
			user = settings['user']
		else:
			user = cmds.promptDialog(t='Ask User', m='Whats you user name?')
			user = cmds.promptDialog(query=True, text=True)
			settings['user'] = user
			self.write_json(path=os.path.join(cmds.internalVar(usd=True)), json_file='MutantTools.settings',
							data=settings)
		print(user)

		#Compare user with config file to find show
		studio_config = self.read_json(os.path.join(FOLDER, 'config'), 'studio.json')


		for show in studio_config['shows']:
			for u in studio_config['shows'][show]:
				if u in user:
					print(show)
					return show

		return False

# ----------------------------------------------------------------------------------------------------------------
