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

		with open(write_json, 'w', encoding='utf-8') as f:
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

		json_data = path + '\\' + json_file
		json_data.replace('/', '\\')

		with open(json_data) as f:
			data = json.load(f)

		return data
