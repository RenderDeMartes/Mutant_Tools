'''
version: 1.0.0
date: 21/04/2020

#----------------
content:

#----------------
how to:

import imp
import Mutant_Tools
from Mutant_Tools.UI.GuidePlacements import load_guide_placements
imp.reload(load_guide_placements)

try:cGuidePlacements.close()
except:pass
cGuidePlacements = load_guide_placements.GuidePlacements()
cGuidePlacements.show()

#----------------
dependencies:

QT FILE
ICONS
JSON FILES
Main Mutant

#----------------
licence: https://www.eulatemplate.com/live.php?token=FGISW7ApRfgywum6murbBmLcusKONzkv
author:  Esteban Rodriguez <info@renderdemartes.com>

'''
# -------------------------------------------------------------------
from shiboken2 import wrapInstance
from PySide2 import QtGui, QtCore
from PySide2 import QtUiTools
from PySide2 import QtWidgets
from PySide2.QtWidgets import *

import maya.OpenMayaUI as omui
from functools import partial
from maya import OpenMaya
import maya.cmds as cmds
import maya.mel as mel

import os
import imp
import sys
import json
import glob
import pprint
from pathlib import Path

from functools import partial

# -------------------------------------------------------------------

# QT WIndow!
FOLDER_NAME = 'GuidePlacements'
PATH = os.path.dirname(__file__)
BLOCKS_PATH = PATH.replace('\\UI\\{}'.format(FOLDER_NAME), '//Blocks')  # get Blocks paths to write files

Title = 'Guide Placements'
Folder = PATH.replace('\\UI\\{}'.format(FOLDER_NAME), '')
UI_File = 'GuidePlacement.ui'
IconsPath = Folder + '//Icons//'

# -------------------------------------------------------------------

# Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = PATH.replace('\\UI\\{}'.format(FOLDER_NAME), '//Config')  # change this path depending of the folder

JSON_FILE = (PATH + '/name_conventions.json')
with open(JSON_FILE) as json_file:
	nc = json.load(json_file)
# Read curve shapes info
CURVE_FILE = (PATH + '/curves.json')
with open(CURVE_FILE) as curve_file:
	curve_data = json.load(curve_file)
# setup File
SETUP_FILE = (PATH + '/rig_setup.json')
with open(SETUP_FILE) as setup_file:
	setup = json.load(setup_file)


# -------------------------------------------------------------------

import Mutant_Tools
import Mutant_Tools.Utils
from Mutant_Tools.Utils.Rigging import main_mutant

imp.reload(Mutant_Tools.Utils.Rigging.main_mutant)
mt = main_mutant.Mutant()

from Mutant_Tools.UI import QtMutantWindow
imp.reload(QtMutantWindow)
Qt_Mutant = QtMutantWindow.Qt_Mutant()

from Mutant_Tools.Utils.Helpers import helpers
imp.reload(Mutant_Tools.Utils.Helpers.helpers)
mh = helpers.Helpers()

# -------------------------------------------------------------------


def maya_main_window():
	main_window_ptr = omui.MQtUtil.mainWindow()
	return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class GuidePlacements(QtMutantWindow.Qt_Mutant):

	def __init__(self):
		super(GuidePlacements, self).__init__()

		self.setWindowTitle(Title)
		self.designer_loader_child(path=Folder + '/UI/{}/'.format(FOLDER_NAME), ui_file=UI_File)
		self.set_title(Title)

		self.create_layout()
		self.create_connections()
		self.resize(500,750)

		self.place_widgets=[]
		self.ik_ref_widgets=[]
		self.code_mode = 'python'
		self.code = ''

	# -------------------------------------------------------------------

	def create_layout(self):
		"""

		Returns:

		"""

		self.create_menu()

	def create_connections(self):
		"""

		Returns:

		"""

		self.ui.add_btn.clicked.connect(self.create_place_guide_widget)
		self.ui.place_guide_btn.clicked.connect(self.place_guides)
		self.ui.add_ref_btn.clicked.connect(self.create_ik_ref_widget)
		self.ui.create_ik_refs_btn.clicked.connect(self.create_ref_planes)

		self.ui.run_btn.clicked.connect(self.exec_code_field)

	def create_menu(self):
		self.menuBar = QtWidgets.QMenuBar()  # requires parent

		# -------------------------------------------------------------------

		# File Menu

		self.guideMenu = QtWidgets.QMenu(self)
		self.guideMenu.setTitle("Guides")

		self.save_custom = self.guideMenu.addAction("Save Custom")
		self.save_custom.triggered.connect(lambda: self.save_preset())
		self.load_custom = self.guideMenu.addAction("Load Custom")
		self.load_custom.triggered.connect(lambda: self.load_preset())
		self.guideMenu.addSeparator()

		self.load_biped = self.guideMenu.addAction("Load Biped")
		self.load_biped.triggered.connect(lambda: self.load_biped_data())
		self.load_biped_wrap = self.guideMenu.addAction("Load Wrap3 Biped")
		self.load_biped_wrap.triggered.connect(lambda: self.load_biped_wrap_data())
		self.guideMenu.addSeparator()

		self.menuBar.addMenu(self.guideMenu)

		self.ui.menuLayout.insertWidget(0, self.menuBar)

	# -------------------------------------------------------------------
	# -------------------------------------------------------------------
	# -------------------------------------------------------------------
	#Guides

	def create_place_guide_widget(self, guide_text = '', position_text='', aim_text=''):

		placement_box = QGroupBox()
		self.ui.place_layout.addWidget(placement_box)

		main_layout = QtWidgets.QHBoxLayout()
		placement_box.setLayout(main_layout)

		guide_edit = QLineEdit()
		if not guide_text:
			guide_edit.setPlaceholderText('Guide')
		else:
			guide_edit.setText(guide_text)
		guide_button = QPushButton()
		guide_button.setIcon(QtGui.QIcon(IconsPath + 'DLeft.png'))
		guide_button.clicked.connect(partial(self.selection_to_line_edit, guide_edit))
		sel_guide_button = QPushButton()
		sel_guide_button.setIcon(QtGui.QIcon(IconsPath + 'Cursor.png'))
		sel_guide_button.clicked.connect(partial(self.select_text, guide_edit))

		main_layout.addWidget(guide_edit)
		main_layout.addWidget(guide_button)
		main_layout.addWidget(sel_guide_button)

		position_edit = QLineEdit()
		if not position_text:
			position_edit.setPlaceholderText('Position')
		else:
			position_edit.setText(position_text)
		position_button = QPushButton()
		position_button.setIcon(QtGui.QIcon(IconsPath + 'DLeft.png'))
		position_button.clicked.connect(partial(self.selection_to_line_edit, position_edit))
		sel_position_button = QPushButton()
		sel_position_button.setIcon(QtGui.QIcon(IconsPath + 'Cursor.png'))
		sel_position_button.clicked.connect(partial(self.select_text, position_edit))

		main_layout.addWidget(position_edit)
		main_layout.addWidget(position_button)
		main_layout.addWidget(sel_position_button)

		aim_edit = QLineEdit()
		if not aim_text:
			aim_edit.setPlaceholderText('Aim')
		else:
			aim_edit.setText(aim_text)
		aim_button = QPushButton()
		aim_button.setIcon(QtGui.QIcon(IconsPath + 'DLeft.png'))
		aim_button.clicked.connect(partial(self.selection_to_line_edit, aim_edit))
		sel_aim_button = QPushButton()
		sel_aim_button.setIcon(QtGui.QIcon(IconsPath + 'Cursor.png'))
		sel_aim_button.clicked.connect(partial(self.select_text, aim_edit))

		main_layout.addWidget(aim_edit)
		main_layout.addWidget(aim_button)
		main_layout.addWidget(sel_aim_button)

		build_button = aim_button = QPushButton('Build')
		for_build = []
		for_build.append([guide_edit, position_edit, aim_edit])
		build_button.clicked.connect(partial(self.place_guides, 'selection', for_build))
		main_layout.addWidget(build_button)


		self.place_widgets.append([guide_edit, position_edit, aim_edit])

	# -------------------------------------------------------------------

	def selection_to_line_edit(self, line_edit):
		sel=cmds.ls(sl=True)
		clean_sel = self.clean_selection(sel)
		if sel:
			if line_edit.text():
				result = cmds.confirmDialog( title='Replace?', message='Replace {}?'.format(line_edit.text()), button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
				if result != 'Yes':
					return None
			line_edit.setText(clean_sel)

	def select_text(self, line_edit):
		objs = line_edit.text()
		if objs:
			cmds.select(cl=True)
			for i in objs.split(','):
				cmds.select(i, add=True)

	# -------------------------------------------------------------------

	def clean_selection(self, sel):
		clean_sel = str(sel)[1:-1]
		clean_sel = clean_sel.replace("'", "")
		return clean_sel

	# -------------------------------------------------------------------

	def place_guides(self, mode = 'all', selection = []):

		print(mode)

		if not self.place_widgets:
			return False

		cmds.undoInfo(openChunk=True)

		if mode == 'all':
			build = self.place_widgets
		else:
			build = selection

		clusters = []
		for guide_pairs in build:
			guide = guide_pairs[0].text()
			position = guide_pairs[1].text()
			position = position.split(',')
			aim = guide_pairs[2].text()
			if guide and position:
				print (guide, '>>>' ,position, '>>>', aim)

				if aim:
					temp_loc = cmds.spaceLocator()
					cmds.delete(cmds.parentConstraint(aim, temp_loc, mo=False))

				cmds.select(position)
				temp_cls = cmds.cluster()[1]
				cmds.delete(cmds.pointConstraint(temp_cls, guide, mo=False))
				cmds.delete(temp_cls)


			aim_delete = []
			if guide and aim:
				cmds.select(aim)
				temp_contraint2 = cmds.aimConstraint(temp_loc, guide, mo=False)[0]
				cmds.delete(cmds.parentConstraint(temp_loc,aim, mo=False))

				cmds.delete(temp_loc,temp_contraint2)


		cmds.undoInfo(closeChunk=True)

	# -------------------------------------------------------------------
	# -------------------------------------------------------------------
	# -------------------------------------------------------------------

	#IK REF
	def create_ik_ref_widget(self, start_text='', mid_text='', end_text=''):

		placement_box = QGroupBox()
		self.ui.ref_layout.addWidget(placement_box)

		main_layout = QtWidgets.QHBoxLayout()
		placement_box.setLayout(main_layout)

		start_edit = QLineEdit()
		start_edit.setText(start_text)
		start_button = QPushButton()
		start_button.setIcon(QtGui.QIcon(IconsPath + 'DLeft.png'))
		start_button.clicked.connect(partial(self.selection_to_line_edit, start_edit))

		main_layout.addWidget(start_edit)
		main_layout.addWidget(start_button)

		mid_edit = QLineEdit()
		mid_edit.setText(mid_text)
		mid_button = QPushButton()
		mid_button.setIcon(QtGui.QIcon(IconsPath + 'DLeft.png'))
		mid_button.clicked.connect(partial(self.selection_to_line_edit, mid_edit))

		main_layout.addWidget(mid_edit)
		main_layout.addWidget(mid_button)

		end_edit = QLineEdit()
		end_edit.setText(end_text)
		end_button = QPushButton()
		end_button.setIcon(QtGui.QIcon(IconsPath + 'DLeft.png'))
		end_button.clicked.connect(partial(self.selection_to_line_edit, end_edit))

		main_layout.addWidget(end_edit)
		main_layout.addWidget(end_button)

		self.ik_ref_widgets.append([start_edit, mid_edit, end_edit])

	# -------------------------------------------------------------------

	def create_ref_planes(self):


		if not self.ik_ref_widgets:
			return False
		cmds.undoInfo(openChunk=True)

		parent_constraints = []
		for ref_pairs in self.ik_ref_widgets:
			start = ref_pairs[0].text()
			mid = ref_pairs[1].text()
			end = ref_pairs[2].text()

			start = start.split(',')
			mid = mid.split(',')
			end = end.split(',')

			if start and end:
				print (start, '>>>' , end)
				self.create_ref_plane(start, end)
				if mid:
					print(start, '>>>', mid ,'>>>' ,end)

		cmds.undoInfo(closeChunk=True)

	# -------------------------------------------------------------------

	def create_ref_plane(self, start,end):
		cmds.undoInfo(openChunk=True)

		cmds.select(start,end)
		sel = cmds.ls(sl=True)
		refPlane = cmds.polyPlane(n=str(sel[0]) + '_Ref', sh=1, sw=1)[0]

		cmds.move(-0.5, 0, 0, str(refPlane) + '.scalePivot', str(refPlane) + '.rotatePivot')
		cmds.manipPivot(o=(-90, 0, 90))

		cmds.matchTransform(refPlane, sel[0])
		edge = cmds.select(str(refPlane) + '.e[2]')

		Cluster = cmds.cluster(n=str(sel[1]) + '_cluster')
		cmds.delete(cmds.pointConstraint(sel[1], Cluster, mo=False))
		cmds.delete(refPlane, ch=True)

		cmds.undoInfo(closeChunk=True)


	# -------------------------------------------------------------------
	# -------------------------------------------------------------------
	# -------------------------------------------------------------------
	#CODE

	def exec_code_field(self):
		cmds.undoInfo(openChunk=True)

		self.code_mode = 'python' if self.ui.python_radio.isChecked() else 'mel'
		self.code = self.ui.code_text.toPlainText()

		print(self.code_mode)
		print(self.code)
		if self.code_mode == 'python':
			exec(self.code)
		else:
			mel.eval(self.code)

		cmds.undoInfo(closeChunk=True)

	# -------------------------------------------------------------------
	# -------------------------------------------------------------------
	# -------------------------------------------------------------------
	#Presets

	def save_preset(self):

		self.code_mode = 'python' if self.ui.python_radio.isChecked() else 'mel'
		self.code = self.ui.code_text.toPlainText()

		guide_data = {}
		for num, guide_pairs in enumerate(self.place_widgets):
			guide = guide_pairs[0].text()
			position = guide_pairs[1].text()
			aim = guide_pairs[2].text()
			guide_data[str(num)] = {guide : [position, aim]}


		ref_data={}
		for num, ref_pairs in enumerate(self.ik_ref_widgets):
			start = ref_pairs[0].text()
			mid = ref_pairs[1].text()
			end = ref_pairs[2].text()
			ref_data[str(num)] = {'start':start, 'mid':mid, 'end':end}

		preset_data = {
						'guides' : guide_data,
						'refs' : ref_data,
						'code' : {'mode' : self.code_mode, 'code': self.code}
						}

		pprint.pprint(preset_data)

		path = mh.export_window(extension=".json")[0]
		if path:
			new_file = mh.write_json(path=path,
							json_file='',
							data=preset_data)
		print(new_file)
		return preset_data

	# -------------------------------------------------------------------

	def load_preset(self, path = None):
		if path == None:
			read_path = mh.import_window(extension = ".json")[0]
		else:
			read_path=path

		if not read_path:
			return False

		for i in reversed(range(self.ui.place_layout.count())):
			self.ui.place_layout.itemAt(i).widget().setParent(None)
		for i in reversed(range(self.ui.ref_layout.count())):
			self.ui.ref_layout.itemAt(i).widget().setParent(None)

		data = mh.read_json(path = read_path, json_file = '')
		guides = data['guides']
		refs = data['refs']
		code = data['code']

		#Guides---------------------
		for num, guide in enumerate(guides):
			guide_data = guides[str(num)]
			for guide_name in guide_data:
				self.create_place_guide_widget(guide_text=guide_name, position_text=guide_data[guide_name][0], aim_text=guide_data[guide_name][1])

		#Refs---------------------
		for num, ref in enumerate(refs):
			ref_data = refs[str(num)]
			start = ref_data['start']
			mid = ref_data['mid']
			end = ref_data['end']
			self.create_ik_ref_widget(start_text=start, mid_text=mid, end_text=end)

		#Code---------------------
		if code['mode'] == 'python':
			self.ui.python_radio.setChecked(True)
		else:
			self.ui.mel_radio.setChecked(True)

		self.ui.code_text.setPlainText(code['code'])

		pprint.pprint(data)

	# -------------------------------------------------------------------
	def load_biped_wrap_data(self):
		json_file = os.path.dirname(__file__) + '\\Guides\\BipedWrap.json'
		self.load_preset(path = json_file)

	def load_biped_data(self):
		json_file = os.path.dirname(__file__) + '\\Guides\\Biped.json'
		self.load_preset(path=json_file)


# -------------------------------------------------------------------

if __name__ == "__main__":

	try:
		cGuidePlacements.close()  # pylint: disable=E0601
		cGuidePlacements.deleteLater()
	except:
		pass
	cGuidePlacements = GuidePlacements()
	cGuidePlacements.show()

# -------------------------------------------------------------------

'''
#Notes






'''