from __future__ import absolute_import
'''
version: 1.0.0
date: 21/04/2020

#----------------
content:

#----------------
how to:

try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import Mutant_Tools
from Mutant_Tools.UI.GuidePlacements import load_guide_placements
reload(load_guide_placements)

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
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import sys
import json
import glob
import pprint
from pathlib import Path

from functools import partial

# -------------------------------------------------------------------

# QT WIndow!
FOLDER_NAME = 'GuidePlacements'
#Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-2]
FOLDER=''
for f in PATH_PARTS:
	FOLDER = os.path.join(FOLDER, f)

Title = 'Guide Placements'
UI_File = 'GuidePlacement.ui'
IconsPath = os.path.join(FOLDER, 'Icons')



# -------------------------------------------------------------------

JSON_FILE = os.path.join(FOLDER, 'config', 'name_conventions.json')
with open(JSON_FILE) as json_file:
	nc = json.load(json_file)
#Read curve shapes info
CURVE_FILE = os.path.join(FOLDER, 'config', 'curves.json')
with open(CURVE_FILE) as curve_file:
	curve_data = json.load(curve_file)
#setup File
SETUP_FILE = os.path.join(FOLDER, 'config', 'rig_setup.json')
with open(SETUP_FILE) as setup_file:
	setup = json.load(setup_file)
#Version File
VERSION_FILE = os.path.join(FOLDER, 'config', 'version.json')
with open(VERSION_FILE) as version_file:
	version = json.load(version_file)


# -------------------------------------------------------------------

import Mutant_Tools
import Mutant_Tools.Utils
from Mutant_Tools.Utils.Rigging import main_mutant

reload(Mutant_Tools.Utils.Rigging.main_mutant)
mt = main_mutant.Mutant()

from Mutant_Tools.UI import QtMutantWindow
reload(QtMutantWindow)
Qt_Mutant = QtMutantWindow.Qt_Mutant()

from Mutant_Tools.Utils.Helpers import helpers
reload(Mutant_Tools.Utils.Helpers.helpers)
mh = helpers.Helpers()

# -------------------------------------------------------------------


def maya_main_window():
	main_window_ptr = omui.MQtUtil.mainWindow()
	return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class GuidePlacements(QtMutantWindow.Qt_Mutant):

	def __init__(self):
		super(GuidePlacements, self).__init__()

		self.setWindowTitle(Title)
		self.designer_loader_child(path=os.path.join(FOLDER, 'UI', FOLDER_NAME), ui_file=UI_File)
		self.set_title(Title)

		self.create_layout()
		self.create_connections()
		self.resize(800,900)

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


		self.load_biped_frank = self.guideMenu.addAction("Load Frank Biped")
		self.load_biped_frank.triggered.connect(lambda: self.load_frankBiped_data())
		self.load_biped_ag = self.guideMenu.addAction("Load Mutant Avenger")
		self.load_biped_ag.triggered.connect(lambda: self.load_agBiped_data())
		self.load_stellarMale = self.guideMenu.addAction("Load Stellar Male")
		self.load_stellarMale.triggered.connect(lambda: self.load_stellarMale_data())
		self.load_stellarFemale = self.guideMenu.addAction("Load Stellar Female")
		self.load_stellarFemale.triggered.connect(lambda: self.load_stellarFemale_data())

		self.guideMenu.addSeparator()



		self.menuBar.addMenu(self.guideMenu)

		self.ui.menuLayout.insertWidget(0, self.menuBar)

	# -------------------------------------------------------------------
	# -------------------------------------------------------------------
	# -------------------------------------------------------------------
	#Guides

	def create_place_guide_widget(self, guide_text = '', position_text='', aim_text='', aim_axis='', up_axis=''):

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
		guide_button.setIcon(QtGui.QIcon(os.path.join(IconsPath, 'DLeft.png')))
		guide_button.clicked.connect(partial(self.selection_to_line_edit, guide_edit))
		sel_guide_button = QPushButton()
		sel_guide_button.setIcon(QtGui.QIcon(os.path.join(IconsPath, 'Cursor.png')))
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
		position_button.setIcon(QtGui.QIcon(os.path.join(IconsPath, 'DLeft.png')))
		position_button.clicked.connect(partial(self.selection_to_line_edit, position_edit))
		sel_position_button = QPushButton()
		sel_position_button.setIcon(QtGui.QIcon(os.path.join(IconsPath, 'Cursor.png')))
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
		aim_button.setIcon(QtGui.QIcon(os.path.join(IconsPath, 'DLeft.png')))
		aim_button.clicked.connect(partial(self.selection_to_line_edit, aim_edit))
		sel_aim_button = QPushButton()
		sel_aim_button.setIcon(QtGui.QIcon(os.path.join(IconsPath, 'Cursor.png')))
		sel_aim_button.clicked.connect(partial(self.select_text, aim_edit))

		main_layout.addWidget(aim_edit)
		main_layout.addWidget(aim_button)
		main_layout.addWidget(sel_aim_button)

		#Aim axis and up
		#aim_axis = '', up_axis = ''
		aim_axis_line = QLineEdit()
		aim_axis_line.setFixedSize(60,20)
		aim_axis_line.setToolTip('Aim Axis')
		if not aim_axis:
			aim_axis_line.setText('1,0,0')
		else:
			aim_axis_line.setText(aim_axis)
		aim_up_line = QLineEdit()
		aim_up_line.setFixedSize(50,20)
		aim_up_line.setToolTip('Up Axis')
		if not up_axis:
			aim_up_line.setText('0,1,0')
		else:
			aim_up_line.setText(up_axis)

		main_layout.addWidget(aim_axis_line)
		main_layout.addWidget(aim_up_line)

		build_button = QPushButton('Build')
		for_build = []
		for_build.append([guide_edit, position_edit, aim_edit, aim_axis_line, aim_up_line])
		build_button.clicked.connect(partial(self.place_guides, 'selection', for_build))
		main_layout.addWidget(build_button)


		self.place_widgets.append([guide_edit, position_edit, aim_edit, aim_axis_line, aim_up_line])

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
		clean_sel = clean_sel.replace("u'", "'")
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

			aim_axis = guide_pairs[3].text().split(',')
			aim_axis = (float(aim_axis[0]),float(aim_axis[1]),float(aim_axis[2]))

			aim_up = guide_pairs[4].text().split(',')
			aim_up = (float(aim_up[0]),float(aim_up[1]),float(aim_up[2]))

			if guide and position:
				print (guide, '>>>' ,position, '>>>', aim)

				if aim:
					temp_loc = cmds.spaceLocator()
					cmds.delete(cmds.parentConstraint(aim, temp_loc, mo=False))

				cmds.select(position)
				temp_cls = cmds.cluster()[1]
				cmds.delete(cmds.pointConstraint(temp_cls, guide, mo=False))
				cmds.delete(temp_cls)
				cmds.select(guide)


			if guide and aim:
				cmds.select(aim)
				temp_contraint = cmds.aimConstraint(temp_loc, guide, mo=False, worldUpType='vector', upVector=(aim_up), aimVector=aim_axis)[0]
				cmds.delete(cmds.parentConstraint(temp_loc,aim, mo=False))

				cmds.delete(temp_loc,temp_contraint)
				cmds.select(guide)

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
		start_button.setIcon(QtGui.QIcon(os.path.join(IconsPath, 'DLeft.png')))
		start_button.clicked.connect(partial(self.selection_to_line_edit, start_edit))

		main_layout.addWidget(start_edit)
		main_layout.addWidget(start_button)

		mid_edit = QLineEdit()
		mid_edit.setText(mid_text)
		mid_button = QPushButton()
		mid_button.setIcon(QtGui.QIcon(os.path.join(IconsPath, 'DLeft.png')))
		mid_button.clicked.connect(partial(self.selection_to_line_edit, mid_edit))

		main_layout.addWidget(mid_edit)
		main_layout.addWidget(mid_button)

		end_edit = QLineEdit()
		end_edit.setText(end_text)
		end_button = QPushButton()
		end_button.setIcon(QtGui.QIcon(os.path.join(IconsPath, 'DLeft.png')))
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
			aim_axis = guide_pairs[3].text()
			aim_up = guide_pairs[4].text()
			guide_data[str(num)] = {guide : [position, aim, aim_axis, aim_up]}


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

		with open(path, 'w') as f:
			json.dump(preset_data, f, ensure_ascii=False, indent=4)

		print(path)

		return preset_data

	# -------------------------------------------------------------------

	def load_preset(self, path = None, json_file=None):

		if path == None:
			read_path = mh.import_window(extension = ".json")[0]
			with open(read_path) as f:
				data = json.load(f)

		else:
			read_path=path
			json_file = json_file
			data = mh.read_json(path=read_path, json_file=json_file)

		if not read_path:
			return False

		for i in reversed(range(self.ui.place_layout.count())):
			self.ui.place_layout.itemAt(i).widget().setParent(None)
		for i in reversed(range(self.ui.ref_layout.count())):
			self.ui.ref_layout.itemAt(i).widget().setParent(None)

		guides = data['guides']
		refs = data['refs']
		code = data['code']

		#Guides---------------------
		for num, guide in enumerate(guides):
			guide_data = guides[str(num)]
			for guide_name in guide_data:
				try:
					self.create_place_guide_widget(guide_text=guide_name, position_text=guide_data[guide_name][0],
											   aim_text=guide_data[guide_name][1], aim_axis=guide_data[guide_name][2], up_axis=guide_data[guide_name][3])
				except:
					self.create_place_guide_widget(guide_text=guide_name, position_text=guide_data[guide_name][0],
											   aim_text=guide_data[guide_name][1])

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
		json_file = os.path.join(os.path.dirname(__file__),'Guides')
		self.load_preset(path = json_file, json_file='BipedWrap.json')
		print(json_file)

	def load_biped_data(self):
		json_file = os.path.join(os.path.dirname(__file__),'Guides')
		print(json_file)
		self.load_preset(path=json_file, json_file='Biped.json')

	def load_frankBiped_data(self):
		json_file = os.path.join(os.path.dirname(__file__),'Guides')
		print(json_file)
		self.load_preset(path=json_file, json_file='frankBody.json')

	def load_agBiped_data(self):
		json_file = os.path.join(os.path.dirname(__file__),'Guides')
		print(json_file)
		self.load_preset(path=json_file, json_file='avengerBody.json')


	def load_stellarMale_data(self):
		json_file = os.path.join(os.path.dirname(__file__),'Guides')
		print(json_file)
		self.load_preset(path=json_file, json_file='StellarMale.json')

	def load_stellarFemale_data(self):
		json_file = os.path.join(os.path.dirname(__file__),'Guides')
		print(json_file)
		self.load_preset(path=json_file, json_file='StellarFemale.json')



	# -------------------------------------------------------------------
	# -------------------------------------------------------------------
	# -------------------------------------------------------------------

	def exit_ui(self):

		close_comfirm = cmds.confirmDialog(
						title='Close Mutant Autorigger',
						message='Are you sure?',
						button=['Close', 'Stay Open'],
						defaultButton='Stay Open',
						dismissString='Stay Open',
						cancelButton = 'Stay Open')

		if close_comfirm == 'Close':
			print('Mutant is closing')
			self.close()


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