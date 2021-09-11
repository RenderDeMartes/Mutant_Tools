'''
version: 1.0.0
date: 21/04/2020


#----------------
how to:

import Mutant_Tools
import Mutant_Tools.Utils.Helpers
from Mutant_Tools.Utils.Helpers import helpers
imp.reload(Mutant_Tools.Utils.Helpers.helpers)

mh = helpers.Helpers()
mh.FUNC(ARGUMENTS)

#----------------
dependencies:


#----------------
licence: https://www.eulatemplate.com/live.php?token=FGISW7ApRfgywum6murbBmLcusKONzkv
author:  Esteban Rodriguez <info@mutanttools.com>

'''

from maya import cmds

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

		write_json = path + json_file
		if not path.endswith('\\'):
			path = path +'\\'
		with open(write_json, 'w', encoding='utf-8') as f:
			json.dump(data, f, ensure_ascii=False, indent=4, t_keys = False)

		return write_json

	# ----------------------------------------------------------------------------------------------------------------

	def read_json(self, path, json_file):
		""" will read json file

		Args:
			path: path to where the json file is (rembember to use \\ to define the folders)
			json_file: json file name

		Returns: dictionary with data

		"""
		if not path.endswith('\\'):
			path = path +'\\'

		json_data = path + json_file
		json_data.replace('/', '\\')

		with open(json_data) as f:
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
		basicFilter = '*' + extension
		dialog = cmds.fileDialog2(fileFilter=basicFilter, fileMode=0, caption="Save As")
		return dialog

	# ----------------------------------------------------------------------------------------------------------------

	def import_window(self, extension = ".ma"):
		basicFilter = '*' + extension
		dialog = cmds.fileDialog2(fileFilter=basicFilter, fileMode=1, caption="Open")
		return dialog

	# ----------------------------------------------------------------------------------------------------------------
