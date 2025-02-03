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
from Mutant_Tools.UI.Zombinator import load_zombinator
reload(load_zombinator)

try:cZombinator.close()
except:pass
cZombinator = load_zombinator.Zombinator()
cZombinator.show()

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
from Mutant_Tools.Utils.Helpers.decorators import undo

import os
import platform
import subprocess

try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import sys
import json
import glob
import pprint
from pathlib import Path

try:
	import exec_humanBodyTemplate
except:
	from Mutant_Tools.UI.AutoRigger import load_autoRigger
	reload(load_autoRigger)
	AutoRigger = load_autoRigger.AutoRigger()

import Mutant_Tools.UI.CustomWidgets.expandableWidget as expandableWidget
reload(expandableWidget)

# -------------------------------------------------------------------

# QT WIndow!
FOLDER_NAME = 'Zombinator'
Title = 'Zombinator'
UI_File = 'Zombinator.ui'

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
nc, curve_data, setup = mt.import_configs()

import Mutant_Tools.Utils.Wrap
from Mutant_Tools.Utils.Wrap import wrap_utils
reload(wrap_utils)
cWrap = wrap_utils.Wrap3D()

from Mutant_Tools.Utils.Wrap.Skeletor import Skeletor
reload(Skeletor)
cSkeletor = Skeletor.Skeletor()

import Mutant_Tools.UI
from Mutant_Tools.UI import QtMutantWindow
reload(QtMutantWindow)
Qt_Mutant = QtMutantWindow.Qt_Mutant()

# -------------------------------------------------------------------


def maya_main_window():
	main_window_ptr = omui.MQtUtil.mainWindow()
	return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class Zombinator(QtMutantWindow.Qt_Mutant):

	def __init__(self):
		super(Zombinator, self).__init__()

		self.setWindowTitle(Title)

		self.designer_loader_child(path=os.path.join(FOLDER, 'UI', FOLDER_NAME), ui_file=UI_File)
		self.set_title(Title)

		self.skin_mapping = {'BodySkull': 'BindSkull',
						'BodyEyes': 'BindEyelids',
						'BodyLips': 'BindLips',
						'BodyBrows': 'BindBrows',
						'BodyCheeks': 'BindCheeks',
						'BodyJaw': 'BindJaw',
						'BodyNose': 'BindNose',
						'BodyMouthUp': 'BindMouthUp',
						'BodyMouthDown': 'BindMouthDown',
						'BodyMouthWide': 'BindMouthWide',
						'BodyMouthNarrow': 'BindMouthNarrow',
						'BodySquash': ''
						}

		self.base_mesh = 'WrapBaseMesh'
		self.skinning_boxes={}
		self.body_skinning_versions = []
		self.face_skinning_versions = []

		self.hierarchy_array = []
		self.block_order = []

		self.force_load_of_dependency_plugins()
		self.rename_transf_shapes()

		self.create_layout()
		self.create_connections()

		self.create_menu()


	# -------------------------------------------------------------------

	def create_layout(self):
		"""

		Returns:

		"""
		self.add_icons_based_on_json(json_file=os.path.join(FOLDER, 'UI', FOLDER_NAME, 'zombinator_icons.json'))
		self.preload_guides()
		cmds.select(cl=True)

		self.create_version_skinning_boxes()

		self.populate_base_meshes()
		self.get_ui_data()

	def create_connections(self):
		"""

		Returns:

		"""
		#Wrap Tab
		self.ui.export_geo_for_wrap.clicked.connect(self.export_geo_for_wrap)
		self.ui.export_geo_for_wrap_face.clicked.connect(self.export_geo_for_wrap_face)
		self.ui.open_wrap_3d.clicked.connect(self.open_wrap_3d)
		self.ui.wrap_help.clicked.connect(self.wrap_help)
		self.ui.open_folder_with_wrapped_geos.clicked.connect(self.open_folder_with_wrapped_geos)
		self.ui.import_wrapped_geo.clicked.connect(self.import_wrapped_geo)

		#BodyTab
		self.ui.auto_zombify.clicked.connect(self.run_zombify)
		self.ui.import_biped_guide.clicked.connect(self.import_biped_guide)
		self.ui.auto_place_guides.clicked.connect(self.auto_place_guides)
		self.ui.unparent_guides.clicked.connect(self.unparent_guides)
		self.ui.parent_guides.clicked.connect(self.parent_guides)
		self.ui.reset_arms.clicked.connect(self.reset_arms)
		self.ui.reset_legs.clicked.connect(self.reset_legs)
		self.ui.build_rig.clicked.connect(self.build_rig)
		self.ui.load_skinning.clicked.connect(self.load_skinning)
		self.ui.copy_skinning_to_sel.clicked.connect(self.copy_skinning_to_sel)
		self.ui.load_roms.clicked.connect(self.load_rom)
		self.ui.open_helpers.clicked.connect(self.open_helpers)

		#FaceTab
		self.ui.auto_zombify_face.clicked.connect(self.zombinator_face)
		self.ui.import_face_guide.clicked.connect(self.import_face_guide)
		self.ui.auto_place_guides_face.clicked.connect(self.auto_place_guides_face)
		self.ui.build_rig_face.clicked.connect(self.build_rig_face)
		self.ui.load_skinning_face.clicked.connect(self.load_skinning_face)
		self.ui.create_face_geos.clicked.connect(self.create_face_geos)
		self.ui.copy_skinning_to_sel_face.clicked.connect(self.copy_skinning_to_sel_face)
		self.ui.open_helpers_face.clicked.connect(self.open_helpers_face)

		self.ui.load_eyeball_geo.clicked.connect(lambda: self.put_selection_on_field(field=self.ui.eyeball_line))
		self.ui.load_face_geo.clicked.connect(lambda: self.put_selection_on_field(field=self.ui.face_geo_line))
		self.ui.create_real_head_based_on_sel.clicked.connect(lambda: self.put_selection_on_field(field=self.ui.real_face_line))
		#self.ui.load_face_geo_extras.clicked.connect(lambda: self.put_selection_on_field(field=self.ui.extra_face_geo_line))

		self.ui.add_extra_geos.clicked.connect(self.add_extra_geos)
		self.ui.add_to_extra_geos_line.clicked.connect(lambda: self.put_selection_on_field(field=self.ui.extra_geos_line))

		self.ui.load_guides.clicked.connect(self.load_guides)
		self.ui.update_geo.clicked.connect(self.update_geo)
		self.ui.f_help.clicked.connect(self.open_online_help)

		self.ui.base_mesh_combo.currentTextChanged.connect(self.basemesh_combo_changed)
		self.ui.base_mesh_combo.setCurrentText('WrapBaseMesh')

	# -------------------------------------------------------------------
	# -------------------------------------------------------------------
	# ------------------------  Common  ---------------------------------
	# -------------------------------------------------------------------
	# -------------------------------------------------------------------

	def basemesh_combo_changed(self):
		self.base_mesh = self.ui.base_mesh_combo.currentText()
		print(self.base_mesh)

		self.get_ui_data()

	def populate_base_meshes(self):

		path = os.path.join(FOLDER, 'Utils', 'Wrap', 'BaseMesh', '*')
		folders = glob.glob(path)

		clean_names = []
		omit = ['Template', 'Instructions.txt']
		for folder in folders:
			name = os.path.basename(folder)
			if name in omit:
				continue
			clean_names.append(name)

		self.ui.base_mesh_combo.clear()
		self.ui.base_mesh_combo.addItems(clean_names)
		self.ui.base_mesh_combo.setCurrentIndex(0)


	def get_ui_data(self):
		# names = ['Wrap', 'Biped', 'Face']
		# for i in range(3):
		# 	self.ui.steps_tabs.setTabEnabled(i, True)
		# 	self.ui.steps_tabs.setTabText(i, names[i])

		#base_meshes = [self.ui.base_mesh_combo.itemText(i) for i in range(self.ui.base_mesh_combo.count())]


		base_path = os.path.join(FOLDER, 'Utils', 'Wrap', 'BaseMesh', self.base_mesh)
		body_skins = glob.glob(os.path.join(base_path, 'Skins' ,'Body*'))
		face_skins = glob.glob(os.path.join(base_path, 'Skins' ,'Face*'))
		wrap_files = glob.glob(os.path.join(base_path, 'WrapFiles' ,'*preset'))
		skeletor_files = glob.glob(os.path.join(base_path, 'Skeletor' ,'*.skeletor'))

		self.body_skinning_versions = self.paths_to_basename(body_skins)
		self.face_skinning_versions = self.paths_to_basename(face_skins)

		self.ui.body_skinning_combo.clear()
		self.ui.body_skinning_combo.addItems(self.body_skinning_versions)

		self.ui.face_skinning_combo.clear()
		self.ui.face_skinning_combo.addItems(self.face_skinning_versions)
		#self.ui.face_skinning_combo.setCurrentIndex(int(self.face_skinning_versions[-1])-1)

		for num, face in enumerate(self.skinning_boxes):
			self.skinning_boxes[face].clear()
			self.skinning_boxes[face].addItems(self.face_skinning_versions)
			#self.skinning_boxes[face].setCurrentIndex(int(self.face_skinning_versions[-1]) - 1)

	def list_to_amount(self, ls_amount):
		new_ls = []
		if not ls_amount:
			return []
		for num in range(ls_amount):
			new_ls.append(str(num+1))

		return new_ls

	def paths_to_basename(self, paths):
		clean_paths = []
		for path in paths:
			cleam_path = os.path.basename(path)
			clean_paths.append(cleam_path)

		return clean_paths


	# -------------------------------------------------------------------
	# -------------------------------------------------------------------
	# ------------------------Wrap Tab-----------------------------------
	# -------------------------------------------------------------------
	# -------------------------------------------------------------------

	def open_online_help(self):
		cmds.warning('www.mutanttools.com')

	def put_selection_on_field(self, field):
		sel = cmds.ls(sl=True)
		print(sel)
		# remove ugly lists keys
		nice_selection = str(sel)[1:-1]
		nice_selection = nice_selection.replace("u'", "'")
		nice_selection = nice_selection.replace("'", "")
		field.setText(nice_selection)

	def export_geo_for_wrap(self, mode='Body'):
		import os
		try:
			from rigSystem.utils.io.core import IO
			from rigSystem.assetTemplates.core import (get_one_sid, validate_sid)
			sid = get_one_sid()
			sid = validate_sid(sid)
			version = sid.version
			name = str(sid) + '_ForWrapGeo'
		except:
			version = 0
			name = 'Model_ForWrapGeo'

		path = os.path.join(cmds.workspace(rd=True, q=True), 'data', '{}_{}.abc'.format(name, version))

		while os.path.exists(path):
			version = version + 1
			path = os.path.join(cmds.workspace(rd=True, q=True), 'data', '{}_{}.abc'.format(name, version))

		if 'modeling' in path:
			path = path.replace('modeling', 'rigging')

		#Stupid windows fix
		o_system = platform.platform()
		if 'Windows' in o_system:
			path = path.replace("\\","/")

		if not os.path.exists(os.path.dirname(path)):
			os.makedirs(os.path.dirname(path))
  
		#Create new export geo
		sel = cmds.ls(sl=True)

		export_grp = cmds.group(em=True, n='Zombinator_Export_Grp')
		dups = cmds.duplicate(sel, rc=True)
		cmds.parent(dups, export_grp)

		cmds.select(export_grp)
		if len(sel) != 1:
			geo = cmds.polyUnite()[0]
			mel.eval('AbcExport -j "-frameRange 1 1 -dataFormat ogawa -root |{} -file {}";'.format(geo, path))
		else:
			geo = dups[0]
			cmds.select(geo)
			mel.eval('AbcExport -j "-frameRange 1 1 -dataFormat ogawa -root {} -file {}";'.format(geo, path))

		print(geo)
		cmds.delete(export_grp, geo)
		print(path)

		if isinstance(path, list):
			path=path[0]

		if mode == 'Face':
			self.create_wrap_file(path, mode='Face')
		else:
			self.create_wrap_file(path, mode='Body')

		self.open_folder_with_wrapped_geos()

		print('Done')

	def export_geo_for_wrap_face(self):
		self.export_geo_for_wrap(mode='Face')


	def create_wrap_file(self, obj_path, mode='Body'):

		print('#'*30)
		print('#'*30)
		print(mode)
		print('#'*30)
		print('#'*30)

		if isinstance(obj_path, list):
			obj_path=obj_path[0]

		if mode == 'Body':
			wrap_template_file = os.path.join(FOLDER, 'Utils', 'Wrap', 'BaseMesh', self.base_mesh,  "WrapFiles", 'body_preset.wrap')
		else:
			wrap_template_file = os.path.join(FOLDER, 'Utils', 'Wrap', 'BaseMesh',  self.base_mesh, "WrapFiles", 'face_preset.wrap')
		print(wrap_template_file)

		f = open(wrap_template_file, 'r')
		wrap_data = json.loads(f.read())
		# project['nodes']['Load']['params']['fileNames']['value'] = ['C:/Models/John.obj']
		f.close()

		edited_data = wrap_data

		edited_data['nodes']['PUT_YOUR_GEO_HERE']['params']['fileName']['value'] = obj_path
		edited_data['nodes']['SaveAlembic']['params']['fileName']['value'] = obj_path.replace('.obj', '')+'_{}_Wrapped.abc'.format(mode)

		new_wrap_file = obj_path.replace('.obj', '')+'_{}_WRAP.wrap'.format(mode)

		with open(new_wrap_file, 'w+') as fp:
			json.dump(edited_data, fp, indent=4, sort_keys=True)

		print(new_wrap_file)

		import pprint
		pprint.pprint(edited_data)

		clipboard = QtWidgets.QApplication.clipboard()
		clipboard.setText(new_wrap_file)

	def open_wrap_3d(self):
		centos_command = "r3ds_wrap"
		roky_command = "sclenv r3ds_wrap"

		try:
			subprocess.Popen([centos_command], stdout = subprocess.PIPE)
		except:
			os.system('{}'.format(roky_command))


	def wrap_help(self):
		''

	def open_folder_with_wrapped_geos(self):

		o_system = platform.platform()
		path = os.path.join(cmds.workspace(rd=True, q=True), 'data').replace('modeling', 'rigging')
		print(path)
		if 'Windows' in o_system:
			subprocess.call('explorer "{}"'.format(path.replace('/', '\\')), shell=True)
		else:
			os.system('xdg-open "{}"'.format(os.path.join(cmds.workspace(rd=True, q=True), 'data').replace('modeling', 'rigging')))

	def import_wrapped_geo(self):

		path = os.path.join(cmds.workspace(rd=True, q=True), 'data')
		if 'modeling' in path:
			path = path.replace('modeling', 'rigging')

		abc_files = glob.glob(os.path.join(path, '*.abc'))
		abc_files.sort(key=os.path.getmtime)
		last_abc_file = abc_files[-1]

		# Stupid windows fix
		o_system = platform.platform()
		if 'Windows' in o_system:
			last_abc_file = last_abc_file.replace("\\", "/")

		mel.eval('AbcImport -mode import "{}";'.format(last_abc_file))
		print(last_abc_file)

		if cmds.objExists('Body'):
			bodys = cmds.ls('Body')
			if bodys:
				for b in bodys:
					father = cmds.listRelatives(b, p=True)
					if father:
						if not father[0] == 'Mutant_Build':
							cmds.rename('Body', 'Body_node')


		self.rename_transf_shapes()

	def rename_transf_shapes(self):
		if not cmds.objExists('transf0'):
			return False
		try:
			transf_shapes = cmds.listRelatives('transf0', s=True)
			for s in transf_shapes:
				cmds.rename(s, 'transf0' + 'Shape')
		except:
			pass
		return True

	# -------------------------------------------------------------------
	# -------------------------------------------------------------------
	# ---------------------------Body Tab--------------------------------
	# -------------------------------------------------------------------
	# -------------------------------------------------------------------

	@undo
	def run_zombify(self):
		self.import_biped_guide()
		self.auto_place_guides()
		self.build_rig()
		self.load_skinning()
		self.load_rom()

	@undo
	def import_biped_guide(self):
		try:
			import exec_humanBodyTemplate
			reload(exec_humanBodyTemplate)
			exec_humanBodyTemplate.create_humanBodyTemplate_block()
		except:
			import Mutant_Tools
			from Mutant_Tools.UI.AutoRigger import load_autoRigger
			reload(load_autoRigger)
			AutoRigger = load_autoRigger.AutoRigger()
			AutoRigger.show()
			AutoRigger.close()
			import exec_humanBodyTemplate
			reload(exec_humanBodyTemplate)
			exec_humanBodyTemplate.create_humanBodyTemplate_block()

	@undo
	def auto_place_guides(self, pose='', node = 'transf0'):
		if not cmds.objExists(node) and not cmds.objExists(self.base_mesh):
			cmds.warning('{} or {}:Doesnt Exists'.format(node, self.base_mesh))
			return False
		if not pose:
			if self.ui.t_radio.isChecked():
				pose = 'T'
			else:
				pose = 'A'
		if cmds.objExists('transf0'):
			geo = 'transf0'
		else:
			geo = self.base_mesh
		cWrap.place_mutant_on_wrap_geo(geo=geo, base_mesh=self.base_mesh, topology=self.base_mesh)
		cWrap.fix_all_body_orientations(hand_pose=pose)

	@undo
	def unparent_guides(self):

		self.block_order = cWrap.get_order_of_blocks()
		blocks = cmds.ls('*_Block')
		childs = []
		omit_blocks = ['PhonemesUI_Block']
		for block in blocks:
			if block in omit_blocks:
				blocks.remove(block)
		for child in blocks:
			nodes = cmds.listRelatives(child, ad=True, type='transform')
			print(nodes)
			if not nodes:
				continue
			childs = childs + nodes
		print(childs)
		self.hierarchy_array = Skeletor.unparent_hierarchy(childs)

	@undo
	def parent_guides(self):
		Skeletor.parent_hierarchy(self.hierarchy_array)
		cWrap.reorder_block_guides(self.block_order)

	@undo
	def build_rig(self):
		from Mutant_Tools.UI.AutoRigger import load_autoRigger
		reload(load_autoRigger)
		try:
			AutoRigger.close()
		except:
			pass
		AutoRigger = load_autoRigger.AutoRigger()
		# AutoRigger.reload_all_blocks()
		AutoRigger.build_autorigger(only_progressbar=True)



	@undo
	def load_skinning(self):

		skin_version = self.ui.body_skinning_combo.currentText()

		skin_path = os.path.join(FOLDER, 'Utils', 'Wrap', 'BaseMesh', self.base_mesh, 'Skins')
		cWrap.skin_file = os.path.join(skin_path, '{}'.format(skin_version), '{}.json'.format(self.base_mesh))

		if cmds.objExists('transf0'):
			geo = 'transf0'
			rename=True
		else:
			geo = self.base_mesh
			rename = False
		cWrap.load_mutant_wrap_skinning(geo=geo, skin=self.base_mesh, rename=rename)

	@undo
	def copy_skinning_to_sel(self):

		geo = cmds.ls(sl=True)
		for g in geo:
			print(g)
			cmds.select('transf0',g)
			try:
				mel.eval('performCopySkinWeights false;')
			except:
				cmds.select(g, '*_Bnd')
				cmds.skinCluster(tsb=True)
				cmds.select('transf0', g)
				mel.eval('performCopySkinWeights false;')

	@undo
	def load_rom(self):
		# import Mutant_Tools.Utils.Mocap.Retarget
		# from Mutant_Tools.Utils.Mocap.Retarget import retarget
		# reload(Mutant_Tools.Utils.Mocap.Retarget.retarget)
		#
		# cRetarget = retarget.Retarget()
		#
		# anim_path = os.path.join(FOLDER, 'Utils','Mocap','MocapFiles','Mixamo', 'zombie_attack')
		# cRetarget.load_mixamo_animation(anim_file=anim_path)

		import Mutant_Tools
		from Mutant_Tools.UI.AnimLoader import load_anim_loader
		reload(load_anim_loader)
		try:
			cAnimLoaderUI.close()
		except:
			pass
		cAnimLoaderUI = load_anim_loader.AnimLoaderUI()
		cAnimLoaderUI.show()


	@undo
	def open_helpers(self):
		from Mutant_Tools.UI.Helpers import load_helpers
		reload(load_helpers)
		cHelperUI = load_helpers.HelperUI()
		cHelperUI.show()

	@undo
	def reset_arms(self):
		arms_pos = {
			'L_Shoulder_Guide' : [15.673, 141.79, -3.056, 3.983, -41.351, 0],
			'L_Elbow_Guide' : [21.794, 0.384, -0, 0, 0, 10.209],
			'L_Wrist_Guide' : [25.642, -0.262, -0, 0, 0, 0]
		}

		ref_plane = 'L_Shoulder_Guide_Ref'

		for guide in arms_pos:
			cmds.setAttr('{}.translateX'.format(guide), arms_pos[guide][0])
			cmds.setAttr('{}.translateY'.format(guide), arms_pos[guide][1])
			cmds.setAttr('{}.translateZ'.format(guide), arms_pos[guide][2])
			cmds.setAttr('{}.rotateX'.format(guide), arms_pos[guide][3])
			cmds.setAttr('{}.rotateY'.format(guide), arms_pos[guide][4])
			cmds.setAttr('{}.rotateZ'.format(guide), arms_pos[guide][5])

		cmds.delete(cmds.pointConstraint(ref_plane, 'L_Shoulder_Guide'))

	@undo
	def reset_legs(self, template='Human'):

		if template == 'Human':
			hip_matrix = [0.013746933661306526, -0.9904106235830035, 0.13746933661307106, 0.0, -0.09854954040441069,
						  -0.13815497346793637, -0.9854954040441555, 0.0, 0.9950371902099897, 5.5511151231257815e-17,
						  -0.09950371902099397, 0.0, 8.897879600524902, 93.12921142578125, -0.46075183153152466, 1.0]
			knee_matrix = [-0.01369176025564372, -0.9904878120458103, -0.13691760255644486, 0.0, -0.09855722094352554,
						   0.13760048760343344, -0.9855722094353037, 0.0, 0.9950371902099894, 5.5511151231257796e-17,
						   -0.09950371902099395, 0.0, 8.752433915230041, 54.822620709875224, -1.9152086844802474, 1.0]
			ankle_matrix = [-0.01369176025564373, -0.9904878120458109, -0.13691760255644495, 0.0, -0.09855722094352558,
							0.1376004876034335, -0.9855722094353041, 0.0, 0.99503719020999, 5.551115123125783e-17,
							-0.09950371902099402, 0.0, 8.195169516284642, 9.931680646559656, -7.487852673934562, 1.0]

		elif template == 'Toon':
			hip_matrix = [0.013746933661306526, -0.9904106235830035, 0.13746933661307106, 0.0, -0.09854954040441069,
						  -0.13815497346793637, -0.9854954040441555, 0.0, 0.9950371902099897, 5.5511151231257815e-17,
						  -0.09950371902099397, 0.0, 8.897879600524902, 93.12921142578125, -0.46075183153152466, 1.0]
			knee_matrix = [-0.01369176025564372, -0.9904878120458103, -0.13691760255644486, 0.0, -0.09855722094352554,
						   0.13760048760343344, -0.9855722094353037, 0.0, 0.9950371902099894, 5.5511151231257796e-17,
						   -0.09950371902099395, 0.0, 8.752433915230041, 54.822620709875224, -1.9152086844802474, 1.0]
			ankle_matrix = [-0.01369176025564373, -0.9904878120458109, -0.13691760255644495, 0.0, -0.09855722094352558,
							0.1376004876034335, -0.9855722094353041, 0.0, 0.99503719020999, 5.551115123125783e-17,
							-0.09950371902099402, 0.0, 8.195169516284642, 9.931680646559656, -7.487852673934562, 1.0]

			cmds.error('We need to get matrix data, i just copy paste from here to do later')

		cmds.xform('L_Hip_Guide', m=hip_matrix, ws=True)
		cmds.xform('L_Knee_Guide', m=knee_matrix, ws=True)
		cmds.xform('L_Ankle_Guide', m=ankle_matrix, ws=True)

		cmds.delete(cmds.pointConstraint('L_PelvisEnd_Guide', 'L_Hip_Guide'))

	# -------------------------------------------------------------------
	# -------------------------------------------------------------------
	# ---------------------------Face Tab--------------------------------
	# -------------------------------------------------------------------
	# -------------------------------------------------------------------

	def zombinator_face(self):
		''

	@undo
	def import_face_guide(self):
		import exec_humanFaceTemplate
		reload(exec_humanFaceTemplate)
		exec_humanFaceTemplate.create_humanFaceTemplate_block()

	@undo
	def auto_place_guides_face(self):
		if cmds.objExists('transf0'):
			geo = 'transf0'
		else:
			geo = self.base_mesh
		cWrap.place_mutant_on_wrap_geo(geo=geo, base_mesh=self.base_mesh, topology=self.base_mesh)
		cWrap.fix_all_face_orientations(eyeball=self.ui.eyeball_line.text(), face_geo=self.ui.face_geo_line.text())

	@undo
	def build_rig_face(self):
		from Mutant_Tools.UI.AutoRigger import load_autoRigger
		reload(load_autoRigger)
		try:
			AutoRigger.close()
		except:
			pass
		AutoRigger = load_autoRigger.AutoRigger()
		# AutoRigger.reload_all_blocks()
		AutoRigger.show_bar_only()
		AutoRigger.build_autorigger(only_progressbar=True)


	def create_version_skinning_boxes(self):
		colapsable_box = expandableWidget.expandableWidget(parent=self.ui.face_skinning_layout, title='Skins')
		colapsable_box.collapse()

		skinning_boxes = {}
		for geo in self.skin_mapping:
			placement_box = QGroupBox()
			colapsable_box.layout.addWidget(placement_box)

			main_layout = QtWidgets.QHBoxLayout()
			placement_box.setLayout(main_layout)

			label = QLabel(geo)
			combo_box = QComboBox()

			button = QPushButton('Skin')

			main_layout.addWidget(label)
			main_layout.addWidget(combo_box)
			main_layout.addWidget(button)

			button.clicked.connect(partial(self.skin_individual_face,combo_box, geo))

			skinning_boxes[geo] =combo_box

		self.skinning_boxes = skinning_boxes

	def skin_individual_face(self, combo, face):
		skin_path = os.path.join(FOLDER, 'Utils', 'Wrap', 'BaseMesh', self.base_mesh, 'Skins')
		value = combo.currentText()
		cWrap.skin_file = os.path.join(skin_path, value, '{}.json'.format(face))
		cWrap.load_mutant_wrap_skinning(geo=face, skin=face, rename=False)

	@undo
	def load_skinning_face(self):

		skin_path = os.path.join(FOLDER, 'Utils', 'Wrap', 'BaseMesh', self.base_mesh, 'Skins')
		skin_version = self.ui.face_skinning_combo.currentText()

		cWrap.skin_file = os.path.join(skin_path, skin_version, 'BodyEyes.json')
		cWrap.load_mutant_wrap_skinning(geo='BodyEyes', skin='BodyEyes', rename=False)

		cWrap.skin_file = os.path.join(skin_path, skin_version, 'BodyLips.json')
		cWrap.load_mutant_wrap_skinning(geo='BodyLips', skin='BodyLips', rename=False)

		cWrap.skin_file = os.path.join(skin_path, skin_version, 'BodyBrows.json')
		cWrap.load_mutant_wrap_skinning(geo='BodyBrows', skin='BodyBrows', rename=False)

		cWrap.skin_file = os.path.join(skin_path, skin_version, 'BodyCheeks.json')
		cWrap.load_mutant_wrap_skinning(geo='BodyCheeks', skin='BodyCheeks', rename=False)

		cWrap.skin_file = os.path.join(skin_path, skin_version, 'BodyJaw.json')
		cWrap.load_mutant_wrap_skinning(geo='BodyJaw', skin='BodyJaw', rename=False)

		cWrap.skin_file = os.path.join(skin_path, skin_version, 'BodyNose.json')
		cWrap.load_mutant_wrap_skinning(geo='BodyNose', skin='BodyNose', rename=False)

		cWrap.skin_file = os.path.join(skin_path, skin_version, 'BodyMouthUp.json')
		cWrap.load_mutant_wrap_skinning(geo='BodyMouthUp', skin='BodyMouthUp', rename=False)

		cWrap.skin_file = os.path.join(skin_path, skin_version, 'BodyMouthDown.json')
		cWrap.load_mutant_wrap_skinning(geo='BodyMouthDown', skin='BodyMouthDown', rename=False)

		cWrap.skin_file = os.path.join(skin_path, skin_version, 'BodyMouthWide.json')
		cWrap.load_mutant_wrap_skinning(geo='BodyMouthWide', skin='BodyMouthWide', rename=False)

		cWrap.skin_file = os.path.join(skin_path, skin_version, 'BodyMouthNarrow.json')
		cWrap.load_mutant_wrap_skinning(geo='BodyMouthNarrow', skin='BodyMouthNarrow', rename=False)

		cWrap.skin_file = os.path.join(skin_path, skin_version, 'BodySkull.json')
		cWrap.load_mutant_wrap_skinning(geo='BodyMouthNarrow', skin='BodySkull', rename=False)

	@undo
	def create_face_geos(self, real_face=None):
		if not real_face:
			real_face=self.ui.real_face_line.text()

		rig_heads = ['BodySkull', 'BodyEyes', 'BodyLips', 'BodyBrows',
					 'BodyCheeks', 'BodyJaw', 'BodyNose', 'BodyMouthUp',
					 'BodyMouthDown', 'BodyMouthWide', 'BodyMouthNarrow',
					 'BodySquash']

		rig_heads = cmds.listRelatives('BodySkull_Locals_Grp', c=True) + ['BodySkull']

		wrap_heads = []
		wrap_group = cmds.group(em=True, n='LocalWrap_Heads_Grp')
		for geo in rig_heads:
			new_geo = cmds.rename(geo, 'Wrap_{}'.format(geo))
			wrap_heads.append(new_geo)

			real_face_geo = cmds.duplicate(real_face, n=geo)
			cmds.parent(real_face_geo, cmds.listRelatives(new_geo, p=True)[0])

			cmds.parent(new_geo, wrap_group)

		cmds.parent(wrap_group, 'Miscellaneous_Grp')

		#create blendshape
		cmds.select(rig_heads, 'BodySkull')
		bs = cmds.blendShape(n='ZombinatorSkull', w=[(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (10, 1)])
		cmds.select('BodySkull', real_face)
		bs = cmds.blendShape(n='ZombinatorMain', w=[(0, 1)])

		#transfer oblicularis deformer to real face
		if cmds.objExists('BodyEyes') and cmds.objExists('Wrap_BodyEyes'):
			mel.eval('deformer -e -g BodyEyes R_Orbicularis_Crv_Wire;')
			mel.eval('deformer -e -g BodyEyes L_Orbicularis_Crv_Wire;')

		if cmds.objExists('BodyEyes') and cmds.objExists('Wrap_BodyEyes'):
			mel.eval('deformer -e -g BodyEyes R_Eyelids_Dw_ClusterWire;')
			mel.eval('deformer -e -g BodyEyes L_Eyelids_Dw_ClusterWire;')
			mel.eval('deformer -e -g BodyEyes R_Eyelids_Up_ClusterWire;')
			mel.eval('deformer -e -g BodyEyes L_Eyelids_Up_ClusterWire;')

	@undo
	def copy_skinning_to_sel_face(self):
		skin_mapping = self.skin_mapping

		for geo in skin_mapping:
			bind_set = skin_mapping[geo]
			if cmds.objExists(geo) and cmds.objExists(bind_set):
				try:
					cmds.select(bind_set, geo)
					cmds.skinCluster(tsb=True)
				except:
					pass

				wrap_geo = 'Wrap_{}'.format(geo)
				if cmds.objExists(wrap_geo):
					cmds.select(wrap_geo, geo)
					mel.eval('copySkinWeights  -noMirror -surfaceAssociation closestPoint -influenceAssociation oneToOne -influenceAssociation label -normalize;')

	@undo
	def add_extra_geos(self, geos=None):
		""" Select desire geos and make the local system for them

		Returns:

		"""

		if not geos:
			geos = cmds.ls(sl=True)

		if cmds.objExists("Local_Extra"):
			cmds.delete('Local_Extra')

		if cmds.objExists("Skull_Local_Extra"):
			cmds.delete('Skull_Local_Extra')

		grp_local_skull = cmds.group(n="Skull_Local_Extra", em=True, p="SkullLocal_Rig_Grp")
		grp_local = cmds.group(n="Local_Extra", em=True, p="Locals_Rig_Grp")

		#Create Loccal skull
		skull_geos = []
		for geo in geos:
			#Duplicate
			skull_extra = cmds.duplicate(geo, n=geo.replace("_hi", "_Skull_Local"))
			cmds.parent(skull_extra, grp_local_skull)
			skull_geos.append(skull_extra[0])
			#Bsp
			cmds.select(skull_extra, geo)
			local_bs = cmds.blendShape(n=geo.replace("_hi", "_BS"), en=1)[0]
			cmds.setAttr("{0}.{1}".format(local_bs, skull_extra[0]), 1)

			#Copy skin
			cmds.select('BindSkull', skull_extra)
			cmds.skinCluster(tsb=True)
			cmds.select('BodySkull', skull_extra)
			mel.eval(
				'copySkinWeights  -noMirror -surfaceAssociation closestPoint -influenceAssociation oneToOne -influenceAssociation label -normalize;')

		#Create locals
		local_systems = cmds.listRelatives('BodySkull_Locals_Grp', c=True)
		skin_mapping = self.skin_mapping
		locals_grps = []
		for s in local_systems:
			local_system_grp = cmds.group(n="Local_Extra_{}".format(s), em=True, p=grp_local)
			locals_grps.append(local_system_grp)
			for geo in geos:
				# Duplicate
				extra_geo = cmds.duplicate(geo, n=geo.replace("_hi", "_{}_Local".format(s)))
				cmds.parent(extra_geo, local_system_grp)

				# Copy skin
				if not skin_mapping[s]:
					continue
				cmds.select(skin_mapping[s], extra_geo)
				cmds.skinCluster(tsb=True)
				cmds.select(s, extra_geo)
				mel.eval(
					'copySkinWeights  -noMirror -surfaceAssociation closestPoint -influenceAssociation oneToOne -influenceAssociation label -normalize;')


		#BSP from Locals To Skull
		total_geos = len(cmds.listRelatives(locals_grps[0], c=True))
		for num in range(total_geos):
			current_geos = []
			for grp in locals_grps:
				geos = cmds.listRelatives(grp, c=True)
				current_geos.append(geos[num])
			cmds.select(current_geos, skull_geos[num])
			print('#'*50)
			print(skull_geos[num])
			print(current_geos)
			local_bs = cmds.blendShape(n=skull_geos[num].replace("_Local", "_BS"), en=1)[0]
			#cmds.setAttr("{0}.{1}".format(local_bs, skull_extra[0]), 1)


	def open_helpers_face(self):
		from Mutant_Tools.UI.Helpers import load_helpers
		reload(load_helpers)
		cHelperUI = load_helpers.HelperUI()
		cHelperUI.show()



	# -------------------------------------------------------------------
	# -------------------------------------------------------------------
	# --------------------------Misc Tab---------------------------------
	# -------------------------------------------------------------------
	# -------------------------------------------------------------------

	def force_load_of_dependency_plugins(self):
		plugins_windows = ['quatNodes.mll', 'objExport.mll','lookdevKit.mll', 'matrixNodes.mll', 'AbcExport.mll', 'AbcImport.mll']
		plugins_linux = plugins = ['quatNodes.so', 'objExport.so','lookdevKit.so', 'matrixNodes.so', 'AbcExport.so', 'AbcImport.so']
		for w_plugin, l_plugin in zip(plugins_windows, plugins_linux):
			try:cmds.loadPlugin(w_plugin)
			except:cmds.loadPlugin(l_plugin)

	def preload_guides(self):
		guides = cmds.ls('*{}'.format(nc['guide']))
		if guides:
			cmds.select(guides)
			self.load_guides()

	def load_guides(self):
		line_Edit = self.ui.guides_line

		#sel=cmds.ls(sl=True, type='joint')
		sel=cmds.ls(sl=True)
		clean_sel = str(sel)[1:-1]
		clean_sel = clean_sel.replace("u'", "'")
		clean_sel = clean_sel.replace("'", "")
		line_Edit.setText(clean_sel)

	@undo
	def update_geo(self):

		#Setup Skeletor Class Paths
		import tempfile
		temp_folder = os.path.join(tempfile.gettempdir(), 'ZombinatorTemp')
		if not os.path.exists(temp_folder):
			os.mkdir(temp_folder)
		cSkeletor.dirpath = temp_folder

		#Get guides in scene
		sel= cmds.ls(sl=True)
		if not sel:
			return False

		#guides = cmds.ls('*{}'.format(nc['guide']))
		guides = self.ui.guides_line.text()
		if not guides:
			print('Using all guides')
			#print('AA'*80)
			guides = cmds.ls('*{}'.format(nc['guide']))
		else:
			guides = guides.replace(' ', '').split(',')
		cmds.select(sel[0], guides)

		# Get Data
		cSkeletor.record_all()
		data = cSkeletor.data
		print(cSkeletor.filepath)

		cmds.select(sel)
		cSkeletor.reconform_all(use_self_path=True)

		#Clean file afterwards
		cSkeletor.data = {}
		fh = open(cSkeletor.filepath, 'w')
		json.dump(cSkeletor.data, fh, ensure_ascii=False, indent=4)
		fh.close()

	# CLOSE EVENTS _________________________________
	def closeEvent(self, event):
		''


# -------------------------------------------------------------------

if __name__ == "__main__":

	try:
		cZombinator.close()  # pylint: disable=E0601
		cZombinator.deleteLater()
	except:
		pass
	cZombinator = Zombinator()
	cZombinator.show()

# -------------------------------------------------------------------

'''
#Notes






'''