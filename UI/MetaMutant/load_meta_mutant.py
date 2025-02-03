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
from Mutant_Tools.UI.MetaMutant import load_meta_mutant
reload(load_meta_mutant)

try:cMetaMutantUI.close()
except:pass
cMetaMutantUI = load_meta_mutant.MetaMutantUI()
cMetaMutantUI.show()

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
import platform
import subprocess
from pathlib import Path
from Mutant_Tools.Utils.Helpers.decorators import undo


import Mutant_Tools
from Mutant_Tools.Utils.Unreal.MetaHuman import meta_mutant
reload(meta_mutant)
cMeta_Mutant = meta_mutant.Meta_Mutant()


# -------------------------------------------------------------------

# QT WIndow!
FOLDER_NAME = 'MetaMutant'
Title = 'Meta-Mutant'
UI_File = 'meta_mutant.ui'

# QT WIndow!
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-2]
FOLDER=''
for f in PATH_PARTS:
	FOLDER = os.path.join(FOLDER, f)

IconsPath = os.path.join(FOLDER, 'Icons')



# -------------------------------------------------------------------

import Mutant_Tools
import Mutant_Tools.Utils
from Mutant_Tools.Utils.Rigging import main_mutant

reload(Mutant_Tools.Utils.Rigging.main_mutant)
mt = main_mutant.Mutant()

from Mutant_Tools.Utils.Helpers import helpers
reload(Mutant_Tools.Utils.Helpers.helpers)
mh = helpers.Helpers()

import Mutant_Tools.UI.CustomWidgets.expandableWidget as expandableWidget
reload(expandableWidget)

import Mutant_Tools.UI
from Mutant_Tools.UI import QtMutantWindow
reload(QtMutantWindow)
Qt_Mutant = QtMutantWindow.Qt_Mutant()

# -------------------------------------------------------------------


def maya_main_window():
	main_window_ptr = omui.MQtUtil.mainWindow()
	return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class MetaMutantUI(QtMutantWindow.Qt_Mutant):

	def __init__(self):
		super(MetaMutantUI, self).__init__()

		self.setWindowTitle(Title)

		self.meta_mutant_folder = cMeta_Mutant.meta_mutant_folder

		self.designer_loader_child(path=os.path.join(FOLDER, 'UI', FOLDER_NAME), ui_file=UI_File)
		self.set_title(Title)

		self.advance_layouts = [self.ui.l_eye_pivot_layout, self.ui.r_eye_pivot_layout,
								self.ui.tongue_start_end_layout, self.ui.tongue_left_right_layout,
								self.ui.tongue_up_dw_layout, self.ui.uppr_teeth_layout,
								self.ui.lwr_teeth_layout]

		self.create_layout()
		self.create_connections()
		self.create_menu()

	# -------------------------------------------------------------------

	def create_layout(self):
		"""

		Returns:

		"""

		self.populate_dna_files()
		self.put_lines_to_drop_menu()

	def create_connections(self):
		"""

		Returns:

		"""

		self.ui.build_template_btn.clicked.connect(self.build_template)
		self.ui.load_dna_builder_button.clicked.connect(self.get_builder_dna_into_line)
		self.ui.build_dna_button.clicked.connect(self.template_build)

		self.ui.export_face_sel.clicked.connect(self.export_geo_for_wrap_face)
		self.ui.open_wrap_btn.clicked.connect(self.open_wrap_3d)
		self.ui.open_meta_mutant_btn.clicked.connect(self.open_meta_mutant_folder)

		self.ui.wrapped_head_btn.clicked.connect(self.put_wrapped_head_in_line)
		self.ui.import_wrapped_head_btn.clicked.connect(self.import_wrapped_head)
		self.ui.save_btn.clicked.connect(self.save_settings)
		self.ui.load_btn.clicked.connect(self.load_settings)

		self.ui.l_eye_pivot_btn.clicked.connect(
			lambda: self.selection_to_line_edit(self.ui.l_eye_pivot_line))
		self.ui.r_eye_pivot_btn.clicked.connect(
			lambda: self.selection_to_line_edit(self.ui.r_eye_pivot_line))
		self.ui.tongue_end_btn.clicked.connect(
			lambda: self.selection_to_line_edit(self.ui.tongue_end_line))
		self.ui.tongue_start_btn.clicked.connect(
			lambda: self.selection_to_line_edit(self.ui.tongue_start_line))
		self.ui.tongue_right_btn.clicked.connect(
			lambda: self.selection_to_line_edit(self.ui.tongue_right_line))
		self.ui.tongue_left_btn.clicked.connect(
			lambda: self.selection_to_line_edit(self.ui.tongue_left_line))
		self.ui.tongue_up_btn.clicked.connect(
			lambda: self.selection_to_line_edit(self.ui.tongue_up_line))
		self.ui.jaw_btn.clicked.connect(
			lambda: self.selection_to_line_edit(self.ui.jaw_line))
		self.ui.uppr_teeth_btn.clicked.connect(
			lambda: self.selection_to_line_edit(self.ui.uppr_teeth_line))
		self.ui.lwr_teeth_btn.clicked.connect(
			lambda: self.selection_to_line_edit(self.ui.lwr_teeth_line))
		self.ui.create_position_locators_btn.clicked.connect(self.create_position_locators)


		self.ui.build_custom_btn.clicked.connect(self.build_custom_metahuman)
		self.ui.save_temp_btn.clicked.connect(self.save_as_temp_file)
		self.ui.load_temp_btn.clicked.connect(self.import_temp_file)
		#self.ui.transform_back_btn.clicked.connect(self.transform_back)

		self.ui.trasnfer_to_sel_btn.clicked.connect(self.trasnfer_to_sel)
		self.ui.skin_l_eye_btn.clicked.connect(self.skin_l_eye)
		self.ui.skin_r_eye_btn.clicked.connect(self.skin_r_eye)
		self.ui.skin_upper_teeth_btn.clicked.connect(self.skin_upper_teeth)
		self.ui.skin_lower_teeth_btn.clicked.connect(self.skin_lower_teeth)
		self.ui.skin_tongue_btn.clicked.connect(self.skin_tongue)

		#Blendshapes
		self.ui.animate_btn.clicked.connect(self.animate)
		self.ui.main_geo_load_btn.clicked.connect(
			lambda: self.selection_to_line_edit(self.ui.main_geo_line))

		self.ui.extract_shapes_btn.clicked.connect(self.extract_shapes)
		self.ui.save_as_temp_btn.clicked.connect(self.save_extracted_shapes_as_temp)
		self.ui.load_as_temp_btn.clicked.connect(self.load_extracted_shapes_as_temp)
		self.ui.split_shapes_btn.clicked.connect(self.split_shapes)
		self.ui.connect_shapes_btn.clicked.connect(self.connect_shapes)

	# -------------------------------------------------------------------
	# -------------------------------------------------------------------
	# -------------------------Layout UI---------------------------------
	# -------------------------------------------------------------------
	# -------------------------------------------------------------------

	def populate_dna_files(self):
		self.ui.metahuman_templates_combo.clear()
		dna_files = glob.glob(os.path.join(cMeta_Mutant.ROOT_DIR, 'data', 'dna_files', '*.dna'))
		nice_names = []
		for path in dna_files:
			filename_without_ext = os.path.splitext(os.path.basename(path))[0]
			nice_names.append(filename_without_ext)
		self.ui.metahuman_templates_combo.addItems(nice_names)

	def put_lines_to_drop_menu(self):
		colapsable_box = expandableWidget.expandableWidget(
			parent=self.ui.pop_down_layout, title='Advance Setup')
		colapsable_box.collapse()

		self.ui.advance_scroll.setParent(None)
		colapsable_box.layout.addWidget(self.ui.advance_scroll)

	# -------------------------------------------------------------------
	# -------------------------------------------------------------------
	# -----------------------DNA Builder---------------------------------
	# -------------------------------------------------------------------
	# -------------------------------------------------------------------

	def build_template(self):
		cMeta_Mutant.create_simple_metahuman(self.ui.metahuman_templates_combo.currentText())

	def get_builder_dna_into_line(self):
		file = mh.import_window(extension=".dna")
		self.ui.builder_dna_file_line.setText(file[0])

	def template_build(self):
		cMeta_Mutant.create_simple_metahuman(dna_path=self.ui.builder_dna_file_line.text())

	# -------------------------------------------------------------------
	# -------------------------------------------------------------------
	# -----------------------------WRAP----------------------------------
	# -------------------------------------------------------------------
	# -------------------------------------------------------------------
	def open_wrap_3d(self):
		centos_command = "r3ds_wrap"
		roky_command = "sclenv r3ds_wrap"

		try:
			subprocess.Popen([centos_command], stdout = subprocess.PIPE)
		except:
			os.system('{}'.format(roky_command))

	def export_geo_for_wrap(self, mode='Body'):
		version = 0
		name = 'Model_ForWrapGeo'

		path = os.path.join(self.meta_mutant_folder, '{}_{}.obj'.format(name, version))

		while os.path.exists(path):
			version = version + 1
			path = os.path.join(self.meta_mutant_folder, '{}_{}.obj'.format(name, version))

		# Stupid windows fix
		o_system = platform.platform()
		if 'Windows' in o_system:
			path = path.replace("\\", "/")

		if not os.path.exists(os.path.dirname(path)):
			os.makedirs(os.path.dirname(path))

		# Create new export geo
		sel = cmds.ls(sl=True)

		export_grp = cmds.group(em=True, n='Zombinator_Export_Grp')
		dups = cmds.duplicate(sel, rc=True)
		cmds.parent(dups, export_grp)

		cmds.select(export_grp)
		if len(sel) != 1:
			geo = cmds.polyUnite()[0]
			mel.eval('file -force -options "groups=1;ptgroups=1;materials=1;smoothing=1;normals=1" -typ "OBJexport" -pr -es "{}";'.format(path))
		else:
			geo = dups[0]
			cmds.select(geo)
			mel.eval('file -force -options "groups=1;ptgroups=1;materials=1;smoothing=1;normals=1" -typ "OBJexport" -pr -es "{}";'.format(path))

		print(geo)
		cmds.delete(export_grp, geo)
		print(path)

		if isinstance(path, list):
			path = path[0]

		if mode == 'Face':
			self.create_wrap_file(path, mode='Face')
		else:
			self.create_wrap_file(path, mode='Body')

		self.open_folder_with_wrapped_geos()

		print('Done')

	def create_wrap_file(self, obj_path, mode='Body'):

		print('#'*30)
		print('#'*30)
		print(mode)
		print('#'*30)
		print('#'*30)

		if isinstance(obj_path, list):
			obj_path=obj_path[0]

		if mode == 'Body':
			wrap_template_file = os.path.join(FOLDER, 'Utils','Unreal', 'MetaHuman', 'meta_components', 'meta_face_preset_project.wrap')
		else:
			wrap_template_file = os.path.join(FOLDER, 'Utils','Unreal', 'MetaHuman', 'meta_components', 'meta_face_preset_project.wrap')

		f = open(wrap_template_file, 'r')
		wrap_data = json.loads(f.read())
		# project['nodes']['Load']['params']['fileNames']['value'] = ['C:/Models/John.obj']
		f.close()

		edited_data = wrap_data

		edited_data['nodes']['PUT_YOUR_GEO_HERE']['params']['fileName']['value'] = obj_path
		edited_data['nodes']['SaveAlembic']['params']['fileName']['value'] = obj_path.replace('.obj', '')+'_{}_Wrapped.abc'.format(mode)
		base_mesh_head = wrap_template_file = os.path.join(FOLDER, 'Utils', 'Unreal', 'MetaHuman', 'meta_components', 'base_head.obj')
		edited_data['nodes']['DESIRE_TOPOLOGY']['params']['fileName']['value'] = base_mesh_head

		new_wrap_file = obj_path.replace('.obj', '')+'_{}_WRAP.wrap'.format(mode)

		with open(new_wrap_file, 'w+') as fp:
			json.dump(edited_data, fp, indent=4, sort_keys=True)

		#print(new_wrap_file)

		import pprint
		pprint.pprint(edited_data)

		clipboard = QtWidgets.QApplication.clipboard()
		clipboard.setText(new_wrap_file)

	def export_geo_for_wrap_face(self):
		self.export_geo_for_wrap(mode='Face')

	def open_meta_mutant_folder(self):
		self.open_folder_with_wrapped_geos()

	def open_folder_with_wrapped_geos(self):

		o_system = platform.platform()
		path = self.meta_mutant_folder
		print(path)
		if 'Windows' in o_system:
			subprocess.call('explorer "{}"'.format(path.replace('/', '\\')), shell=True)
		else:
			os.system('xdg-open "{}"'.format(
				os.path.join(cmds.workspace(rd=True, q=True), 'data').replace('modeling', 'rigging')))

	# -------------------------------------------------------------------
	# -------------------------------------------------------------------
	# -------------------------Custom Build------------------------------
	# -------------------------------------------------------------------
	# -------------------------------------------------------------------

	def put_wrapped_head_in_line(self):
		file = mh.import_window(extension=".abc")
		self.ui.wrapped_line.setText(file[0])

	def import_wrapped_head(self):
		mel.eval('AbcImport -mode import "{}";'.format(self.ui.wrapped_line.text()))

	def save_settings(self):

		data = {'L_Eye' : self.ui.l_eye_pivot_line.text(),
				'R_Eye' : self.ui.r_eye_pivot_line.text(),
				'TongueStart' : self.ui.tongue_start_line.text(),
				'TongueEnd' : self.ui.tongue_end_line.text(),
				'TongueRight' : self.ui.tongue_right_line.text(),
				'TongueLeft' : self.ui.tongue_left_line.text(),
				'TongueUp' : self.ui.tongue_up_line.text(),
				'Jaw' : self.ui.jaw_line.text(),
				'UpTeeth' : self.ui.uppr_teeth_line.text(),
				'DwTeeth' : self.ui.lwr_teeth_line.text()
				}

		save_path = mh.export_window(extension = ".json")
		save_path = save_path[0]
		if not save_path:
			return

		f = open(save_path, "w")
		f.write(json.dumps(data, sort_keys=1, indent=4, separators=(",", ":")))
		f.close()

		print(save_path)

	def load_settings(self):

		path = mh.import_window(extension = ".json")
		path = path[0]
		if not path:
			return False

		if not os.path.isfile(path):
			cmds.warning('Path doesnt exists', path)
			return False

		f = open(path, "r")
		data = json.loads(f.read())
		f.close()

		self.ui.l_eye_pivot_line.setText(data['L_Eye'])
		self.ui.r_eye_pivot_line.setText(data['R_Eye'])
		self.ui.tongue_start_line.setText(data['TongueStart'])
		self.ui.tongue_end_line.setText(data['TongueEnd'])
		self.ui.tongue_right_line.setText(data['TongueRight'])
		self.ui.tongue_left_line.setText(data['TongueLeft'])
		self.ui.tongue_up_line.setText(data['TongueUp'])
		self.ui.jaw_line.setText(data['Jaw'])
		self.ui.uppr_teeth_line.setText(data['UpTeeth'])
		self.ui.lwr_teeth_line.setText(data['DwTeeth'])



	def selection_to_line_edit(self, line_edit):
		sel=cmds.ls(sl=True)
		clean_sel = self.clean_selection(sel)
		if sel:
			if line_edit.text():
				result = cmds.confirmDialog( title='Replace?', message='Replace {}?'.format(line_edit.text()), button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
				if result != 'Yes':
					return None
			line_edit.setText(clean_sel)

	def clean_selection(self, sel):
		clean_sel = str(sel)[1:-1]
		clean_sel = clean_sel.replace("u'", "'")
		clean_sel = clean_sel.replace("'", "")
		return clean_sel

	def build_custom_metahuman(self):

		custom_data = self.get_custom_data()
		custom_data_positions = self.get_custom_data_positions(custom_data)


		cMeta_Mutant = meta_mutant.Meta_Mutant()
		cMeta_Mutant.create_custom_metahuman(
			new_geo=self.ui.wrapped_line.text(), custom_data=custom_data,
			custom_data_positions=custom_data_positions)

		self.save_as_temp_file()

	def save_as_temp_file(self):
		import tempfile

		temp_path = os.path.join(tempfile.gettempdir(), 'MetaMutant')
		dirt_temp_file = os.path.join(temp_path, 'MetaMutant_Build.ma')
		if not os.path.exists(temp_path):
			os.makedirs(temp_path)
		cmds.file(rename=dirt_temp_file)
		cmds.file(save=True, type="mayaAscii")

	def import_temp_file(self):
		import tempfile
		temp_path = os.path.join(tempfile.gettempdir(), 'MetaMutant')
		clean_temp_file = os.path.join(temp_path, 'MetaMutant_Build.ma')

		cmds.file(clean_temp_file, i=True)

	def transform_back(self):
		x_value = self.ui.x_line.text()
		y_value = self.ui.y_line.text()
		z_value = self.ui.z_line.text()

		cmds.select('headGui_grp', 'spine_04')
		cmds.move(x_value, y_value, z_value, r=True)

	def create_position_locators(self):
		data =self.get_custom_data()
		cMeta_Mutant.create_position_locators(data)

	def get_custom_data(self):
		data = {'L_Eye': self.ui.l_eye_pivot_line.text(),
				'R_Eye': self.ui.r_eye_pivot_line.text(),
				'TongueStart': self.ui.tongue_start_line.text(),
				'TongueEnd': self.ui.tongue_end_line.text(),
				'TongueRight': self.ui.tongue_right_line.text(),
				'TongueLeft': self.ui.tongue_left_line.text(),
				'TongueUp': self.ui.tongue_up_line.text(),
				'Jaw': self.ui.jaw_line.text(),
				'UpTeeth': self.ui.uppr_teeth_line.text(),
				'DwTeeth': self.ui.lwr_teeth_line.text()}

		return data

	def get_custom_data_positions(self, data):
		positions = {}
		for i in data:
			if cmds.objExists(i+'_Loc'):
				print(i)
				positions[i] = cmds.xform(i+'_Loc', q=True, ws=True, t=True)

		return positions

	# -------------------------------------------------------------------
	# -------------------------------------------------------------------
	# -----------------------------Skin----------------------------------
	# -------------------------------------------------------------------
	# -------------------------------------------------------------------

	def trasnfer_to_sel(self):
		sel = cmds.ls(sl=True)
		if not sel:
			cmds.warning('We need a selection')
			return
		sel=sel[0]

		meta_head = 'head_lod0_mesh'
		joints = cmds.listRelatives('spine_04', ad=True, type='joint')

		cmds.skinCluster(sel, joints, sm=0, bm=1, tsb=True)
		cmds.select(meta_head, sel)
		mel.eval('copySkinWeights  -noMirror -surfaceAssociation closestPoint -influenceAssociation oneToOne -influenceAssociation label -normalize;')

	def skin_l_eye(self):
		self.skin_this_joint_to_sel('FACIAL_L_Eye')


	def skin_r_eye(self):
		self.skin_this_joint_to_sel('FACIAL_R_Eye')


	def skin_tongue(self):
		self.skin_this_joint_to_sel(['FACIAL_C_Tongue1', 'FACIAL_C_Tongue2', 'FACIAL_C_TongueUpper2', 'FACIAL_L_TongueSide2',
		 'FACIAL_R_TongueSide2', 'FACIAL_C_Tongue3', 'FACIAL_C_TongueUpper3', 'FACIAL_C_TongueLower3', 'FACIAL_L_TongueSide3',
		 'FACIAL_R_TongueSide3', 'FACIAL_C_Tongue4'])


	def skin_upper_teeth(self):
		self.skin_this_joint_to_sel('FACIAL_C_TeethUpper')

	def skin_lower_teeth(self):
		self.skin_this_joint_to_sel('FACIAL_C_TeethLower')

	def skin_this_joint_to_sel(self, joint):
		cmds.select(joint, add=True)
		cmds.skinCluster(cmds.ls(sl=True), sm=0, bm=1, tsb=True)

	# -------------------------------------------------------------------
	# -------------------------------------------------------------------
	# ------------------------ Blendshapes-------------------------------
	# -------------------------------------------------------------------
	# -------------------------------------------------------------------

	@undo
	def animate(self):
		cMeta_Mutant.animate()

	@undo
	def extract_shapes(self):
		cMeta_Mutant.extract_shapes(main_geo = self.ui.main_geo_line.text())

	def save_extracted_shapes_as_temp(self):
		cMeta_Mutant.save_extracted_shapes_as_temp()

	def load_extracted_shapes_as_temp(self):
		cMeta_Mutant.load_extracted_shapes_as_temp()

	def split_shapes(self):
		cMeta_Mutant.open_shapes()

	def connect_shapes(self):
		cMeta_Mutant.connect_shapes_to_mutant_face()

	# -------------------------------------------------------------------
	# -------------------------------------------------------------------

	# CLOSE EVENTS _________________________________
	def closeEvent(self, event):
		''


# -------------------------------------------------------------------

if __name__ == "__main__":

	try:
		cMetaMutantUI.close()  # pylint: disable=E0601
		cMetaMutantUI.deleteLater()
	except:
		pass
	cMetaMutantUI = MetaMutantUI()
	cMetaMutantUI.show()

# -------------------------------------------------------------------

'''
#Notes






'''