from maya import cmds
from maya import OpenMaya

import json
import imp
import os

import Mutant_Tools
import Mutant_Tools.Utils
from Mutant_Tools.Utils import main_mutant
imp.reload(Mutant_Tools.Utils.main_mutant)

mt = main_mutant.Mutant()

#----------------------------------------------------------------

#install packages if they cant import
try:
	import mediapipe as mp #ai
	import cv2 #ui

except:
	try:
		# run maya as admin
		from setuptools.command import easy_install
		easy_install.main(['mediapipe'])
	except:
		OpenMaya.MGlobal.displayInfo(
			'We need to install some packages, please open maya as Admin :)\n'
			' (Right click open as Administrator)')


#----------------------------------------------------------------

class Mutant_AI(object):

	def __init__(self):

		#image
		self.image = None

		#body
		self.body_coordinates = {}

		#hands
		self.hands = 1
		self.fingers = 5
		self.hand_coordinates = {}

		#utils
		self.mp_drawing = mp.solutions.drawing_utils

	#--------------------------------------------------

	def init_hands(self):

		self.mp_hands = mp.solutions.hands



