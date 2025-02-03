from __future__ import absolute_import
"""
version: 1.0.0
date: 19/07/2022

modified: 25/05/2023

#----------------

how to:

import Mutant_Tools
try:
	import importlib;from importlib import reload
except:
	import imp;from imp import reload

import Mutant_Tools.Utils.Games.games_utils as games_utils
reload(games_utils)

cGames = games_utils.Games()

#----------------
dependencies:

json
pymel
maya mel
maya.cmds

#----------------
licence: https://www.eulatemplate.com/live.php?token=FGISW7ApRfgywum6murbBmLcusKONzkv
author:  Esteban Rodriguez <info@mutanttools.com>

"""
from maya import cmds, mel
import os
import glob
import json
import pprint
from pathlib import Path
import tempfile

try:
	import importlib;from importlib import reload
except:
	import imp;from imp import reload


import Mutant_Tools
import Mutant_Tools.Utils
from Mutant_Tools.Utils.Rigging import main_mutant
reload(Mutant_Tools.Utils.Rigging.main_mutant)
mt = main_mutant.Mutant()

from Mutant_Tools.Utils.Helpers.decorators import undo

import Mutant_Tools.Utils.Helpers
from Mutant_Tools.Utils.Helpers import helpers
reload(Mutant_Tools.Utils.Helpers.helpers)
mh = helpers.Helpers()

from Mutant_Tools.Utils.IO import EasySkin
reload(Mutant_Tools.Utils.IO.EasySkin)

from Mutant_Tools.Utils.IO import SkinUtils
reload(Mutant_Tools.Utils.IO.SkinUtils)
cSkin = SkinUtils.Skinning()

import Mutant_Tools.Utils.Crowds.Facial.eyelids_local2crowd as eye2crowd
reload(eye2crowd)

nc, curve_data, setup = mt.import_configs()

from Mutant_Tools.Utils.Wrap.Skeletor import Skeletor
reload(Skeletor)

# -------------------------------------------------------------------

import Mutant_Tools
from Mutant_Tools.Utils.Misc import label_joints
reload(label_joints)

# -------------------------------------------------------------------

# Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-2]
FOLDER=''
for f in PATH_PARTS:
	FOLDER = os.path.join(FOLDER, f)


# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------

class Games(object):

	def __init__(self):
		""" Games Class to convert rigs to Games  rigs
		"""
		super(Games, self).__init__()


		self.root = 'Root_Skl'

	#-------------------------------------------------------------------


	def reparent_bnd(self, map='reparent_bnd_map.json'):
		reparent_map =  mh.read_json(path=os.path.join(FOLDER, 'Utils', 'Games', 'maps'), json_file=map)

		if not cmds.objExists('Bind_Joints_Grp'):
			cmds.warning('No Bnd Joints in this scene')
			return False

		bnd_childs = cmds.listRelatives('Bind_Joints_Grp', c=True)
		if not bnd_childs:
			cmds.warning('No Bnd Joints in this scene')
			return False

		# for jnt in bnd_childs:
		# 	cmds.parent(jnt, w=True)
		# 	cmds.setAttr('{}.v'.format(jnt), 1)

		for jnt in reparent_map:
			parent_jnt = reparent_map[jnt]
			if '?' in parent_jnt:
				for num in reversed(range(10)):
					if cmds.objExists(parent_jnt.replace('?', str(num))):
						parent_jnt = parent_jnt.replace('?', str(num))
						break
			if cmds.objExists(jnt) and cmds.objExists(parent_jnt):
				print(jnt, parent_jnt)
				try:cmds.parent(jnt, parent_jnt)
				except:pass
				# cmds.setAttr('{}.v'.format(jnt), 1)
				# cmds.setAttr('{}.inheritsTransform'.format(jnt), 1)
				# cmds.setAttr('{}.segmentScaleCompensate'.format(jnt), 1)


	# -------------------------------------------------------------------

	@undo
	def remove_constriants_in_main_skeleton(self):
		root = self.root

		pr_constriants = cmds.listRelatives(root, ad=True, type='parentConstraint')
		p_constriants = cmds.listRelatives(root, ad=True, type='pointConstraint')
		o_constriants = cmds.listRelatives(root, ad=True, type='orientConstraint')
		s_constriants = cmds.listRelatives(root, ad=True, type='scaleConstraint')

		cmds.delete(pr_constriants, p_constriants, o_constriants, s_constriants)

	def rename_bnd_joints_in_root(self, bind_to_game=False, game_to_bind=False):

		if bind_to_game:
			bnd_joints = cmds.ls('*_Bnd')
			for jnt in bnd_joints:
				cmds.rename(jnt, jnt.replace('_Bnd', '_Skl'))
				new_joints = cmds.ls('*_Skl')

		if game_to_bind:
			bnd_joints = cmds.ls('*_Skl')
			for jnt in bnd_joints:
				cmds.rename(jnt, jnt.replace('_Skl', '_Bnd'))
				new_joints = cmds.ls('*_Bnd')

		return new_joints

	def create_biped_game_joints(self, do_skins=True, map='reparent_bnd_map.json'):

		map = mh.read_json(path=os.path.join(FOLDER, 'Utils', 'Games', 'maps'), json_file=map)
		joints_in_map = []
		for j in map:
			joints_in_map.append(j)

		hierarchy_array = Skeletor.unparent_hierarchy(joints_in_map)

		self.reparent_bnd()
		self.rename_root()

		# Save Skins as Game
		if do_skins:
			game_joints = self.rename_bnd_joints_in_root(bind_to_game=True)

			temp_skin_folder = os.path.join(tempfile.gettempdir(), 'game_utils')
			if not os.path.exists(temp_skin_folder):
				os.mkdir(temp_skin_folder)

			EasySkin.save_all_skins_to(folder_path=temp_skin_folder)

			self.rename_bnd_joints_in_root(game_to_bind=True)

			#clean the geo
			if not cmds.objExists('geo'):
				cmds.error('No geo Grp')
			geos = cmds.listRelatives('geo', ad=True, type='transform')
			for geo in geos:
				cmds.delete(geo, constructionHistory=True)

		#Create game joints
		bnd_joints = cmds.ls('*_Bnd')
		game_joints = []
		for jnt in bnd_joints:
			#filter facial rig
			long_path = cmds.ls(jnt, l=True)[0]
			if 'Face_Bind_Joints_Grp' in long_path:
				continue
			cmds.select(cl=True)
			game_joint = self.create_game_joint_based_on_bnd(bnd_joint=jnt, do_scale=False, scale_constraint=False, segmentScaleCompensate=False)
			game_joints.append(game_joint)

		#reparent
		print(game_joints)
		for jnt in game_joints:
			print(jnt)
			bnd_joint = jnt.replace('_Skl', '_Bnd')
			if not bnd_joint:
				continue
			bnd_parent = cmds.listRelatives(bnd_joint, p=True)
			if not bnd_parent:
				continue
			bnd_parent = bnd_parent[0]
			if 'transform' in bnd_parent:
				print(jnt, bnd_parent)
				bnd_parent = cmds.listRelatives(bnd_parent, p=True)[0]
			if not bnd_parent.endswith('_Bnd'):
				continue
			if cmds.objExists(bnd_parent.replace('_Bnd', '_Skl')):
				cmds.parent(jnt, bnd_parent.replace('_Bnd', '_Skl'))

		#cmds.parent('Root_Skl', w=True)

		#Load skin to real game joints
		if do_skins:
			# if cmds.objExists('geo'):
			# 	cmds.select('geo')
			# 	mel.eval('doDetachSkin "2" { "1","1" };')

			print('Loading Skin')
			EasySkin.load_all_skins_from(folder_path=os.path.join(tempfile.gettempdir(), 'game_utils'))

		#check if any skl still without parent
		skl_joints = cmds.ls('*_Skl')
		for skl in skl_joints:
			if skl == 'Root_Skl':
				continue
			p = cmds.listRelatives(skl, p=True)
			if not p:
				cmds.parent(skl, 'Root_Skl')


		Skeletor.parent_hierarchy(hierarchy_array)

		#Create skeleton grp
		self.create_skeleton_grp()

		cmds.parentConstraint('Global_Ctrl', 'Root_Bnd', mo=True)
		cmds.scaleConstraint('Global_Ctrl', 'Root_Skl', mo=True)

		print('Finish Creating Base Game Skeleton')

	def create_skeleton_grp(self):
		skeleton_grp = cmds.group(em=True, n='Skeleton')
		cmds.parent('Root_Skl', skeleton_grp)
		cmds.parent(skeleton_grp, 'Mutant_Tools_Grp')


	def create_game_joint_based_on_bnd(self, bnd_joint, do_scale=True, scale_constraint=True, segmentScaleCompensate=False):
		return create_game_joint_based_on_bnd(bnd_joint, do_scale, scale_constraint, segmentScaleCompensate)

	def rename_root(self):
		if cmds.objExists('Root'):
			cmds.rename('Root', 'Root_Bnd')

	def set_max_inf(self, inf=4):

		skins = cmds.ls(typ='skinCluster')
		for skin in skins:
			cmds.setAttr('{}.maxInfluences'.format(skin), 4)
			cmds.setAttr('{}.maintainMaxInfluences'.format(skin), True)
			cmds.setAttr('{}.maxInfluences'.format(skin), 4)

	def classic_linear_skin(self):
		skins = cmds.ls(typ='skinCluster')
		for skin in skins:
			cmds.setAttr('{}.skinningMethod'.format(skin), 0)

	def convert_eyes(self):
		eye_joints = cmds.ls("*Eyelids*Bnd")
		eye2crowd.dup_joints(eye_joints, 'Head_Skl')
		eye2crowd.eyelids_crowd()

	def convert_eyebrows(self):
		convert_brows_to_global(prefix_name="Brow")

	def import_face_skeleton(self):
		filepath = os.path.join(FOLDER, 'Utils', 'Games', 'skeletons', 'face_joints.ma')
		print('Loading: {}...'.format(filepath))
		cmds.file(filepath, i=True, type="mayaAscii")

	def create_face_skeleton(self):

		#find mode:
		if cmds.objExists('R_Lips_Upr_01_Bnd'):
			mode = 'simple'
		else:
			mode = 'normal'

		face_grp = cmds.group(em=True, n='Face_Skeleton')
		joints = ['Jaw_Skl', 'L_Eyelids_UpStart_Skl', 'L_Eyelids_DwMid_Skl', 'L_Eyelids_DwEnd_Skl',
 					'L_Eyelids_UpMid_Skl', 'L_Eyelids_DwStart_Skl', 'L_Eyelids_DwEndMid_Skl', 'L_Eyelids_UpEndMid_Skl', 'L_Eyelids_DwStartMid_Skl',
 					'L_Eyelids_UpStartMid_Skl', 'L_Eyelids_UpEnd_Skl', 'R_Eyelids_DwStart_Skl', 'R_Eyelids_UpMid_Skl', 'R_Eyelids_DwEnd_Skl', 'R_Eyelids_DwMid_Skl',
 					'R_Eyelids_UpEnd_Skl', 'R_Eyelids_DwEndMid_Skl', 'R_Eyelids_UpEndMid_Skl', 'R_Eyelids_UpStartMid_Skl', 'R_Eyelids_UpStart_Skl',
 					'R_Eyelids_DwStartMid_Skl', 'Lips_Up_Mid_Skl', 'Lips_DwR_Mid_01_Skl', 'Lips_DwR_Mid_02_Skl', 'Lips_DwL_Mid_02_Skl', 'Lips_UpR__Skl', 'Lips_DwL__Skl',
 					'Lips_UpR_Mid_01_Skl', 'Lips_UpL_Mid_02_Skl', 'Lips_Dw_Mid_Skl', 'Lips_UpL_Mid_01_Skl', 'Lips_UpL__Skl', 'Lips_DwL_Mid_01_Skl', 'Lips_UpR_Mid_02_Skl',
 					'Lips_DwR__Skl', 'L_Brow_2_Skl', 'L_Brow_4_Skl', 'L_Brow_1_Skl', 'L_Brow_0_Skl', 'L_Brow_3_Skl', 'R_Brow_4_Skl', 'R_Brow_1_Skl', 'R_Brow_0_Skl',
 					'R_Brow_2_Skl', 'R_Brow_3_Skl', 'L_Cheecks_0_Skl', 'L_Cheecks_4_Skl', 'L_Cheecks_Bone_3_Skl', 'L_Cheecks_2_Skl', 'L_Cheecks_3_Skl',
 					'L_Cheecks_Bone_2_Skl', 'L_Cheecks_Bone_0_Skl', 'L_Cheecks_5_Skl', 'L_Cheecks_Bone_1_Skl', 'L_Cheecks_1_Skl', 'R_Cheecks_4_Skl', 'R_Cheecks_Bone_2_Skl',
 					'R_Cheecks_Bone_0_Skl', 'R_Cheecks_Bone_1_Skl', 'R_Cheecks_1_Skl', 'R_Cheecks_Bone_3_Skl', 'R_Cheecks_3_Skl', 'R_Cheecks_0_Skl', 'R_Cheecks_5_Skl',
 					'R_Cheecks_2_Skl', 'Nose_Origin_Skl', 'Nose_Bridge_Skl', 'Nose_Base_Skl', 'Nose_Top_Skl', 'Nose_Tip_Skl', 'L_NoseNostril_Skl', 'L_NoseNostrilEnd_Skl',
 					'R_NoseNostril_Skl', 'R_NoseNostrilEnd_Skl', 'Tongue_01_Skl', 'Tongue_02_Skl', 'Tongue_03_Skl', 'Tongue_04_Skl', 'Tongue_05_Skl', 'Teeth_Lwr_Skl',
 					'Teeth_Upr_Skl', 'R_Cheecks_Main_Skl', 'L_Cheecks_Main_Skl']

		simple_joints = ['Jaw_Skl', 'L_Eyelids_UpStart_Skl', 'L_Eyelids_DwMid_Skl', 'L_Eyelids_DwEnd_Skl',
 					'L_Eyelids_UpMid_Skl', 'L_Eyelids_DwStart_Skl', 'L_Eyelids_DwEndMid_Skl', 'L_Eyelids_UpEndMid_Skl', 'L_Eyelids_DwStartMid_Skl',
 					'L_Eyelids_UpStartMid_Skl', 'L_Eyelids_UpEnd_Skl', 'R_Eyelids_DwStart_Skl', 'R_Eyelids_UpMid_Skl', 'R_Eyelids_DwEnd_Skl', 'R_Eyelids_DwMid_Skl',
 					'R_Eyelids_UpEnd_Skl', 'R_Eyelids_DwEndMid_Skl', 'R_Eyelids_UpEndMid_Skl', 'R_Eyelids_UpStartMid_Skl', 'R_Eyelids_UpStart_Skl', 'R_Eyelids_DwStartMid_Skl',
 					'R_Lips_Upr_01_Skl', 'R_Lips_Upr_02_Skl', 'C_Lips_Upr_Skl', 'L_Lips_Upr_02_Skl', 'L_Lips_Upr_01_Skl',
 					'R_Lips_Lwr_01_Skl', 'R_Lips_Lwr_02_Skl', 'C_Lips_Lwr_Skl', 'L_Lips_Lwr_02_Skl', 'L_Lips_Lwr_01_Skl',
 					'L_Brow_2_Skl', 'L_Brow_4_Skl', 'L_Brow_1_Skl', 'L_Brow_0_Skl', 'L_Brow_3_Skl', 'R_Brow_4_Skl', 'R_Brow_1_Skl', 'R_Brow_0_Skl',
 					'R_Brow_2_Skl', 'R_Brow_3_Skl', 'L_Cheecks_0_Skl', 'L_Cheecks_4_Skl', 'L_Cheecks_Bone_3_Skl', 'L_Cheecks_2_Skl', 'L_Cheecks_3_Skl',
 					'L_Cheecks_Bone_2_Skl', 'L_Cheecks_Bone_0_Skl', 'L_Cheecks_5_Skl', 'L_Cheecks_Bone_1_Skl', 'L_Cheecks_1_Skl', 'R_Cheecks_4_Skl', 'R_Cheecks_Bone_2_Skl',
 					'R_Cheecks_Bone_0_Skl', 'R_Cheecks_Bone_1_Skl', 'R_Cheecks_1_Skl', 'R_Cheecks_Bone_3_Skl', 'R_Cheecks_3_Skl', 'R_Cheecks_0_Skl', 'R_Cheecks_5_Skl',
 					'R_Cheecks_2_Skl', 'Nose_Origin_Skl', 'Nose_Bridge_Skl', 'Nose_Base_Skl', 'Nose_Top_Skl', 'Nose_Tip_Skl', 'L_NoseNostril_Skl', 'L_NoseNostrilEnd_Skl',
 					'R_NoseNostril_Skl', 'R_NoseNostrilEnd_Skl', 'Tongue_01_Skl', 'Tongue_02_Skl', 'Tongue_03_Skl', 'Tongue_04_Skl', 'Tongue_05_Skl', 'Teeth_Lwr_Skl',
 					'Teeth_Upr_Skl', 'R_Cheecks_Main_Skl', 'L_Cheecks_Main_Skl']

		if mode == 'simple':
			joints = simple_joints

		for j in joints:
			cmds.select(cl=True)
			jnt = cmds.joint(n=j)
			cmds.parent(jnt, face_grp)

		#create needed hier
		cmds.parent('R_NoseNostrilEnd_Skl', 'R_NoseNostril_Skl')
		cmds.parent('L_NoseNostrilEnd_Skl', 'L_NoseNostril_Skl')
		cmds.parent('Nose_Tip_Skl', 'Nose_Top_Skl')
		cmds.parent('Nose_Top_Skl', 'Nose_Base_Skl')
		cmds.parent('Nose_Base_Skl', 'Nose_Bridge_Skl')
		cmds.parent('Nose_Bridge_Skl', 'Nose_Origin_Skl')
		cmds.parent('Tongue_05_Skl', 'Tongue_04_Skl')
		cmds.parent('Tongue_04_Skl', 'Tongue_03_Skl')
		cmds.parent('Tongue_03_Skl', 'Tongue_02_Skl')
		cmds.parent('Tongue_02_Skl', 'Tongue_01_Skl')


	def setup_face_skeleton(self):
		"""

		Args:

		Returns:

		"""
		#Position Face
		constraints = []
		for jnt in cmds.listRelatives('Face_Skeleton', ad=True):
			if cmds.objExists(jnt.replace('_Skl', '_Jnt')):
				c = cmds.pointConstraint(jnt.replace('_Skl', '_Jnt'), jnt)[0]
			else:
				c = cmds.pointConstraint(jnt.replace('_Skl', '_Bnd'), jnt)[0]
			constraints.append(c)

		cmds.delete(constraints)

		#force Brows
		convert_brows_to_global()
		brow_skel_joints = ['L_Brow_0_Skl','L_Brow_1_Skl','L_Brow_2_Skl','L_Brow_3_Skl','L_Brow_4_Skl',
							'R_Brow_0_Skl', 'R_Brow_1_Skl', 'R_Brow_2_Skl', 'R_Brow_3_Skl', 'R_Brow_4_Skl']
		for jnt in brow_skel_joints:
			normal_jnt = jnt.replace('_Skl', '_Jnt')
			cmds.parentConstraint(normal_jnt, jnt, mo=True)
			cmds.scaleConstraint(normal_jnt, jnt, mo=True)

		#Force Cheecks
		convert_cheeks_to_global(prefix_name="Cheecks")
		cheecks_skel_joints = ['L_Cheecks_Bone_0_Skl', 'L_Cheecks_Bone_1_Skl', 'L_Cheecks_Bone_2_Skl', 'L_Cheecks_Bone_3_Skl',
							   'L_Cheecks_0_Skl','L_Cheecks_1_Skl', 'L_Cheecks_2_Skl','L_Cheecks_3_Skl','L_Cheecks_4_Skl','L_Cheecks_5_Skl',
							   'R_Cheecks_Bone_0_Skl', 'R_Cheecks_Bone_1_Skl', 'R_Cheecks_Bone_2_Skl', 'R_Cheecks_Bone_3_Skl',
							   'R_Cheecks_0_Skl','R_Cheecks_1_Skl', 'R_Cheecks_2_Skl','R_Cheecks_3_Skl','R_Cheecks_4_Skl', 'R_Cheecks_5_Skl',
							   'R_Cheecks_Main_Skl', 'L_Cheecks_Main_Skl']

		for jnt in cheecks_skel_joints:
			normal_jnt = jnt.replace('_Skl', '_Jnt')
			cmds.parentConstraint(normal_jnt, jnt, mo=True)
			cmds.scaleConstraint(normal_jnt, jnt, mo=True)

		cmds.parentConstraint('Jaw_Ctrl','L_Cheecks_Btm_Ctrl_Offset_Grp', mo=True)
		cmds.parentConstraint('Jaw_Ctrl','R_Cheecks_Btm_Ctrl_Offset_Grp', mo=True)
		cmds.parentConstraint('L_Lips_Main_Ctrl','L_Cheecks_Mid_Ctrl_Offset_Grp', mo=True)
		cmds.parentConstraint('R_Lips_Main_Ctrl','R_Cheecks_Mid_Ctrl_Offset_Grp', mo=True)

		#Force Jaw
		convert_jaw_to_global()
		jaw_skl_joints = ['Jaw_Skl']
		for jnt in jaw_skl_joints:
			normal_jnt = jnt.replace('_Skl', '_Jnt')
			cmds.parentConstraint(normal_jnt, jnt, mo=True)
			cmds.scaleConstraint(normal_jnt, jnt, mo=True)


		#Fix eyes
		eye2crowd.eyelids_crowd()

		eyes_skl_joints = ['L_Eyelids_UpStart_Skl', 'L_Eyelids_UpStartMid_Skl', 'L_Eyelids_UpMid_Skl', 'L_Eyelids_UpEndMid_Skl', 'L_Eyelids_UpEnd_Skl',
						   'L_Eyelids_DwStart_Skl', 'L_Eyelids_DwStartMid_Skl', 'L_Eyelids_DwMid_Skl', 'L_Eyelids_DwEndMid_Skl', 'L_Eyelids_DwEnd_Skl',
						   'R_Eyelids_UpStart_Skl', 'R_Eyelids_UpStartMid_Skl', 'R_Eyelids_UpMid_Skl', 'R_Eyelids_UpEndMid_Skl', 'R_Eyelids_UpEnd_Skl',
						   'R_Eyelids_DwStart_Skl', 'R_Eyelids_DwStartMid_Skl', 'R_Eyelids_DwMid_Skl', 'R_Eyelids_DwEndMid_Skl', 'R_Eyelids_DwEnd_Skl']
		eyes_corner_skls = ['L_Eyelids_UpStart_Skl','L_Eyelids_DwStart_Skl','L_Eyelids_UpEnd_Skl','L_Eyelids_DwEnd_Skl',
							'R_Eyelids_UpStart_Skl','R_Eyelids_DwStart_Skl','R_Eyelids_UpEnd_Skl','R_Eyelids_DwEnd_Skl']
		eyes_corner_jnts = ['L_Eyelids_Up_0_Bnd','L_Eyelids_Dw_0_Bnd','L_Eyelids_Up_?_Bnd','L_Eyelids_Dw_?_Bnd',
							'R_Eyelids_Up_0_Bnd','R_Eyelids_Dw_0_Bnd','R_Eyelids_Up_?_Bnd','R_Eyelids_Dw_?_Bnd']

		eye_lids_joints = cmds.ls("*Eyelids*Bnd")
		for jnt in eyes_skl_joints:
			if jnt in eyes_corner_skls:
				continue
			normal_jnt = jnt.replace('_Skl', '_Jnt')
			closest_joint = mt.find_closest_joint(joint=jnt, target_list=eye_lids_joints)
			#print("Closest joint to", jnt, "is", closest_joint)
			cmds.parentConstraint(closest_joint, jnt, mo=True)
			cmds.scaleConstraint(closest_joint, jnt, mo=True)

		for skl, jnt in list(zip(eyes_corner_skls, eyes_corner_jnts)):
			if '?' in jnt:
				for num in reversed(range(99)):
					if cmds.objExists(jnt.replace('?', str(num))):
						jnt = jnt.replace('?', str(num))
						break
			cmds.parentConstraint(jnt, skl, mo=True)
			cmds.scaleConstraint(normal_jnt, jnt, mo=True)

		if cmds.attributeQuery('Eyelids_UpSlide', node='L_Eyelids_BlinkAttrs_Ctrl', exists=True):
			cmds.setAttr("L_Eyelids_BlinkAttrs_Ctrl.Eyelids_UpSlide", 1, l=True)
			cmds.setAttr("L_Eyelids_BlinkAttrs_Ctrl.Eyelids_DwSlide", 1, l=True)
			cmds.setAttr("R_Eyelids_BlinkAttrs_Ctrl.Eyelids_UpSlide", 1, l=True)
			cmds.setAttr("R_Eyelids_BlinkAttrs_Ctrl.Eyelids_DwSlide", 1, l=True)

		#make theeth and tonge global
		theet_tongue_skl_joints = ['Teeth_Lwr_Skl', 'Teeth_Upr_Skl',
								   'Tongue_01_Skl','Tongue_02_Skl','Tongue_03_Skl','Tongue_04_Skl','Tongue_05_Skl',]
		for jnt in theet_tongue_skl_joints:
			normal_jnt = jnt.replace('_Skl', '_Jnt')
			cmds.parentConstraint(normal_jnt, jnt, mo=True)
			cmds.scaleConstraint(normal_jnt, jnt, mo=True)

		#make nose global
		convert_nose_to_global()

		nose_joints = ['Nose_Origin_Skl', 'Nose_Bridge_Skl',
					   'Nose_Base_Skl', 'Nose_Top_Skl', 'Nose_Tip_Skl',
					   'L_NoseNostril_Skl', 'L_NoseNostrilEnd_Skl',
					   'R_NoseNostril_Skl', 'R_NoseNostrilEnd_Skl']

		for jnt in nose_joints:
			normal_jnt = jnt.replace('_Skl', '_Jnt')
			cmds.parentConstraint(normal_jnt, jnt, mo=True)
			cmds.scaleConstraint(normal_jnt, jnt, mo=True)

		#Make Lips System
		cmds.setAttr("L_Lips_Main_Ctrl.mode", 1, l=True)
		cmds.setAttr("R_Lips_Main_Ctrl.mode", 1, l=True)
		if cmds.objExists('R_Lips_Upr_01_Bnd'):
			convert_ribbon_lips_to_global(head_parent_target="Head_Bnd")
			connect_jaw_with_ribbon_mouth()
			#cmds.parentConstraint('Jaw_Ctrl', 'C_Lips_Lwr_Main_Ctrl_Offset_Grp', mo=True)
			#cmds.parentConstraint('Jaw_Ctrl', 'JawUpperLipPivot_Jnt','L_Lips_Main_Ctrl_Offset_Grp', mo=True)
			#cmds.parentConstraint('Jaw_Ctrl', 'JawUpperLipPivot_Jnt', 'R_Lips_Main_Ctrl_Offset_Grp', mo=True)

		else:
			convert_lips_to_global(head_parent_target="Head_Bnd")

		#parent joints to head
		joints = cmds.listRelatives('Face_Skeleton', c=True)
		for j in joints:
			cmds.parent(j, 'Head_Skl')
		cmds.delete('Face_Skeleton')

		cmds.parentConstraint('Head_Ctrl', 'Vis_Ctrl', mo=True)
		cmds.scaleConstraint('Head_Ctrl', 'Vis_Ctrl', mo=True)

		cmds.scaleConstraint('Head_Ctrl', 'Skull_Ctrl_Grp', mo=True)
		cmds.scaleConstraint('Head_Ctrl', 'Jaw_Ctrl_Offset_Grp', mo=True)

	def set_scale_compensate_on_skl(self, value=0):
		sel = cmds.ls("*_Skl")
		#print(sel)
		for jnt in sel:
			cmds.setAttr('{}.segmentScaleCompensate'.format(jnt), value)


	def convert_hero_template_skl_to_simple_skl(self):
		reparent_map = {
			"L_Foot_Ankle_Skl":"L_Knee_Skl_2_Skl",
			"L_Knee_Skl_2_Skl": "L_Knee_Skl_0_Skl",
			"L_Knee_Skl_0_Skl": "L_Hip_Skl_2_Skl",
			"L_Hip_Skl_2_Skl": "L_Hip_Skl_0_Skl",

			"L_Hip_Skl_0_Skl": "Spine_Root_Skl",

			"Head_Skl": "Neck_1_Skl",

			"L_Hand_Palm_Skl": "L_Elbow_Skl_2_Skl",
			"L_Elbow_Skl_2_Skl": "L_Elbow_Skl_0_Skl",
			"L_Elbow_Skl_0_Skl": "L_Shoulder_Skl_2_Skl",
			"L_Shoulder_Skl_2_Skl": "L_Shoulder_Skl_0_Skl",

			"L_Hand_Pinky_01_Skl": "L_Hand_OutterCup_Skl",
			"L_Hand_Ring_01_Skl": "L_Hand_OutterCup_Skl",
			"L_Hand_Middle_01_Skl": "L_Hand_Palm_Skl",
			"L_Hand_Index_01_Skl": "L_Hand_Palm_Skl",

			"Spine_Root_Skl":"Root_Skl"
		}

		delete_joints = ['L_Hand_Pinky_04_Skl','L_Hand_Ring_04_Skl', 'L_Hand_Middle_04_Skl','L_Hand_Index_04_Skl',
					 'L_Hand_Thumb_03_Skl','L_Elbow_Skl_1_Skl','L_Elbow_Skl_3_Skl','L_Shoulder_Skl_1_Skl','L_Shoulder_Skl_3_Skl','L_Pelvis_Skl',
					 'Neck_2_Skl','L_Knee_Skl_3_Skl','L_Knee_Skl_1_Skl','L_Hip_Skl_3_Skl','L_Hip_Skl_1_Skl', 'L_Hand_Pinky_00_Skl',
						 'L_Hand_Ring_00_Skl', 'L_Hand_Middle_00_Skl', 'L_Hand_Index_00_Skl', 'COG_Skl']

		for jnt in reparent_map:
			print(jnt, reparent_map[jnt])
			cmds.parent(jnt, reparent_map[jnt])
			if jnt.startswith(('L_')):
				cmds.parent(jnt.replace('L_', 'R_'), reparent_map[jnt].replace('L_', 'R_'))

		for jnt in delete_joints:
			cmds.delete(jnt)
			if jnt.startswith(('L_')):
				cmds.delete(jnt.replace('L_', 'R_'))

		#rename some joints
		cmds.rename('L_Knee_Skl_2_Skl','L_Knee_Skl_1_Skl')
		cmds.rename('R_Knee_Skl_2_Skl','R_Knee_Skl_1_Skl')
		cmds.rename('L_Hip_Skl_2_Skl','L_Hip_Skl_1_Skl')
		cmds.rename('R_Hip_Skl_2_Skl','R_Hip_Skl_1_Skl')

		cmds.rename('L_Shoulder_Skl_2_Skl','L_Shoulder_Skl_1_Skl')
		cmds.rename('R_Shoulder_Skl_2_Skl','R_Shoulder_Skl_1_Skl')
		cmds.rename('L_Elbow_Skl_2_Skl','L_Elbow_Skl_1_Skl')
		cmds.rename('R_Elbow_Skl_2_Skl','R_Elbow_Skl_1_Skl')


#------------------------------------------------------
#------------------------------------------------------
#------------------------------------------------------
#------------------------------------------------------
#------------------------------------------------------

def convert_brows_to_global(prefix_name="Brow"):
	"""
	Run to convert the local brow setup into a global brow setup. Just remember to reparent the bnd joints to whichever the parent joints should be
	"""

	mel.eval("source channelBoxCommand;")
	mel.eval('source generateChannelMenu.mel;')

	transform_attrs = ["tx", "ty", "tz", "rx", "ry", "rz"]
	scale_attrs = ["scaleX", "scaleY", "scaleZ", ]

	for side in ["L", "R"]:
		master_ctrl_grp = "{}_{}_Ctrl_Grp".format(side, prefix_name)
		if cmds.objExists(master_ctrl_grp):
			block_parent_constraint = cmds.listConnections("{}.translateX".format(master_ctrl_grp))[0]
			block_parent = cmds.listConnections("{}.target[0].targetParentMatrix".format(block_parent_constraint))

			if side == "R":
				mirror_ctrl_grp = cmds.listRelatives(master_ctrl_grp, parent=True)

			if side == "L":
				cmds.scaleConstraint(block_parent, master_ctrl_grp, mo=True)
			else:
				cmds.scaleConstraint(block_parent, mirror_ctrl_grp, mo=True)

			for attr in transform_attrs:
				mel_script = 'CBdeleteConnection "{}_{}_DriverJnts_Grp.{}";'.format(side, prefix_name, attr)
				mel.eval(mel_script)

			for attr in scale_attrs:
				mel_script = 'CBdeleteConnection "{}_{}_DriverJnts_Grp.{}";'.format(side, prefix_name, attr)
				mel.eval(mel_script)

			for num in range(0, 5):

				for attr in transform_attrs:
					mel_script = 'CBdeleteConnection "{}_{}_Driver{}_Jnt.{}";'.format(side, prefix_name, num, attr)
					mel.eval(mel_script)

				for attr in scale_attrs:
					mel_script = 'CBdeleteConnection "{}_{}_Driver{}_Jnt.{}";'.format(side, prefix_name, num, attr)
					mel.eval(mel_script)

				ctrl = "{}_{}_Driver{}_Main_Ctrl".format(side, prefix_name, num)
				if num in [1, 3]:
					ctrl = ctrl.replace("Main", "Sec")

				cmds.parentConstraint(ctrl, "{}_{}_Driver{}_Jnt".format(side, prefix_name, num), mo=True)
				cmds.scaleConstraint(ctrl, "{}_{}_Driver{}_Jnt".format(side, prefix_name, num), mo=True)

				locator_grp = "{}_{}_{}_Loc_Offset_Grp".format(side, prefix_name, num)
				follicle = cmds.listConnections(locator_grp, destination=False)[0]

				cmds.scaleConstraint(block_parent, follicle, mo=True)

				cmds.scaleConstraint("{}_{}_{}_Loc".format(side, prefix_name, num),
									 "{}_{}_{}_Jnt".format(side, prefix_name, num), mo=True)

				for attr in transform_attrs:
					mel_script = 'CBdeleteConnection "{}.{}";'.format(locator_grp, attr)
					mel.eval(mel_script)

				for attr in scale_attrs:
					mel_script = 'CBdeleteConnection "{}.{}";'.format(locator_grp, attr)
					mel.eval(mel_script)

				cmds.parentConstraint(follicle, locator_grp, mo=True)
				cmds.scaleConstraint(follicle, locator_grp, mo=True)

				tweak_offset_grp = "{}_{}_{}_Ctrl_Offset_Grp".format(side, prefix_name, num)

				for attr in transform_attrs:
					mel_script = 'CBdeleteConnection "{}.{}";'.format(tweak_offset_grp, attr)
					mel.eval(mel_script)

				cmds.parentConstraint(locator_grp, tweak_offset_grp, mo=True)
				cmds.scaleConstraint(locator_grp, tweak_offset_grp, mo=True)
	#
	# #create bind joints
	# brow_joints = cmds.ls('*Brow_*_Bnd')
	# for bnd in brow_joints:
	# 	game_joint = create_game_joint_based_on_bnd(bnd)
	# 	cmds.parent(game_joint, 'Head_Skl')

def convert_jaw_to_global(head_parent_target="Head_Bnd"):
	cmds.parentConstraint(head_parent_target, 'Jaw_Rig_Grp', mo=True)
	cmds.scaleConstraint(head_parent_target, 'Jaw_Rig_Grp', mo=True)
	cmds.parent('JawUpperLipPivot_Bnd', head_parent_target)
	cmds.parent('Jaw_Bnd', head_parent_target)

	# if cmds.objExists('Lips_Up_Main_Ctrl_Offset_Grp'):
	# 	cmds.parentConstraint('JawUpperLipPivot_Jnt', 'Lips_Up_Main_Ctrl_Offset_Grp', mo=True)
	# if cmds.objExists('C_Lips_Lwr_Main_Ctrl_Offset_Grp'):
	# 	cmds.parentConstraint('JawUpperLipPivot_Jnt', 'C_Lips_Upr_Main_Ctrl_Offset_Grp', mo=True)

def connect_jaw_with_ribbon_mouth():

	from Mutant_Tools.Utils.IO import SkinUtils
	reload(Mutant_Tools.Utils.IO.SkinUtils)
	cSkin = SkinUtils.Skinning()

	# create_local_jaw
	jaw = 'Jaw_Skl'
	cmds.select(cl=True)
	fake_jaw = cmds.joint(n='Fake_Local_Jaw_Jnt')
	cmds.select(cl=True)
	fake_head = cmds.joint(n='Fake_Local_Head_Jnt')

	fake_grp = cmds.group(fake_head, fake_jaw, n='Game_Local_Lips')

	cmds.delete(cmds.parentConstraint('Jaw_Ctrl', fake_jaw))
	mt.root_grp(fake_jaw)
	cmds.connectAttr('Jaw_Ctrl.t', '{}.t'.format(fake_jaw))
	cmds.connectAttr('Jaw_Ctrl.r', '{}.r'.format(fake_jaw))
	cmds.connectAttr('Jaw_Ctrl.s', '{}.s'.format(fake_jaw))

	cmds.parent(fake_grp, 'Miscellaneous_Grp')

	#Create blendshapes
	nurbs = ['Lips_Upr_Nurb', 'Lips_Lwr_Nurb']
	for nurb in nurbs:
		new_nurb = cmds.duplicate(nurb, n=nurb.replace('Lips_', 'Lips_Local_'))[0]
		cmds.select(new_nurb, nurb)
		skin = cSkin.get_skin_from_geo(nurb)
		bs = cmds.blendShape(n='{}_Game{}'.format(nurb, '_BS'), w=[(0, 1)], before=True)[0]
		cmds.reorderDeformers(skin, bs)

		cmds.skinCluster([fake_head, fake_jaw], new_nurb, sm=0, bm=1, tsb=True)


	#Skin the Shapes
	skin = cSkin.get_skin_from_geo('Lips_Local_Upr_Nurb')

	cmds.skinPercent(skin, 'Lips_Local_Upr_Nurb.cv[12:13][0:3]', tv=[fake_jaw, 0.5])
	cmds.skinPercent(skin, 'Lips_Local_Upr_Nurb.cv[12:13][0:3]', tv=[fake_head, 0.5])

	cmds.skinPercent(skin, 'Lips_Local_Upr_Nurb.cv[11][0:3]', tv=[fake_jaw, 0.3])
	cmds.skinPercent(skin, 'Lips_Local_Upr_Nurb.cv[11][0:3]', tv=[fake_head, 0.7])

	cmds.skinPercent(skin, 'Lips_Local_Upr_Nurb.cv[10][0:3]', tv=[fake_jaw, 0.2])
	cmds.skinPercent(skin, 'Lips_Local_Upr_Nurb.cv[10][0:3]', tv=[fake_head, 0.8])

	cmds.skinPercent(skin, 'Lips_Local_Upr_Nurb.cv[9][0:3]', tv=[fake_jaw, 0.1])
	cmds.skinPercent(skin, 'Lips_Local_Upr_Nurb.cv[9][0:3]', tv=[fake_head, 0.9])

	cmds.skinPercent(skin, 'Lips_Local_Upr_Nurb.cv[5:8][0:3]', tv=[fake_head, 1])

	cmds.skinPercent(skin, 'Lips_Local_Upr_Nurb.cv[4][0:3]', tv=[fake_jaw, 0.1])
	cmds.skinPercent(skin, 'Lips_Local_Upr_Nurb.cv[4][0:3]', tv=[fake_head, 0.9])

	cmds.skinPercent(skin, 'Lips_Local_Upr_Nurb.cv[3][0:3]', tv=[fake_jaw, 0.2])
	cmds.skinPercent(skin, 'Lips_Local_Upr_Nurb.cv[3][0:3]', tv=[fake_head, 0.8])

	cmds.skinPercent(skin, 'Lips_Local_Upr_Nurb.cv[2][0:3]', tv=[fake_jaw, 0.3])
	cmds.skinPercent(skin, 'Lips_Local_Upr_Nurb.cv[2][0:3]', tv=[fake_head, 0.7])

	cmds.skinPercent(skin, 'Lips_Local_Upr_Nurb.cv[0:1][0:3]', tv=[fake_jaw, 0.5])
	cmds.skinPercent(skin, 'Lips_Local_Upr_Nurb.cv[0:1][0:3]', tv=[fake_head, 0.5])

	#----------------------------------------------------------------------------------

	skin = cSkin.get_skin_from_geo('Lips_Local_Lwr_Nurb')

	cmds.skinPercent(skin, 'Lips_Local_Lwr_Nurb.cv[13][0:3]', tv=[fake_jaw, 0.6])
	cmds.skinPercent(skin, 'Lips_Local_Lwr_Nurb.cv[13][0:3]', tv=[fake_head, 0.4])

	cmds.skinPercent(skin, 'Lips_Local_Lwr_Nurb.cv[12][0:3]', tv=[fake_jaw, 0.75])
	cmds.skinPercent(skin, 'Lips_Local_Lwr_Nurb.cv[12][0:3]', tv=[fake_head, 0.25])

	cmds.skinPercent(skin, 'Lips_Local_Lwr_Nurb.cv[11][0:3]', tv=[fake_jaw, 0.9])
	cmds.skinPercent(skin, 'Lips_Local_Lwr_Nurb.cv[11][0:3]', tv=[fake_head, 0.1])

	cmds.skinPercent(skin, 'Lips_Local_Lwr_Nurb.cv[10][0:3]', tv=[fake_jaw, 0.95])
	cmds.skinPercent(skin, 'Lips_Local_Lwr_Nurb.cv[10][0:3]', tv=[fake_head, 0.05])

	cmds.skinPercent(skin, 'Lips_Local_Lwr_Nurb.cv[4:9][0:3]', tv=[fake_jaw, 1])

	cmds.skinPercent(skin, 'Lips_Local_Lwr_Nurb.cv[3][0:3]', tv=[fake_jaw, 0.95])
	cmds.skinPercent(skin, 'Lips_Local_Lwr_Nurb.cv[3][0:3]', tv=[fake_head, 0.05])

	cmds.skinPercent(skin, 'Lips_Local_Lwr_Nurb.cv[2][0:3]', tv=[fake_jaw, 0.9])
	cmds.skinPercent(skin, 'Lips_Local_Lwr_Nurb.cv[2][0:3]', tv=[fake_head, 0.1])

	cmds.skinPercent(skin, 'Lips_Local_Lwr_Nurb.cv[1][0:3]', tv=[fake_jaw, 0.75])
	cmds.skinPercent(skin, 'Lips_Local_Lwr_Nurb.cv[1][0:3]', tv=[fake_head, 0.25])

	cmds.skinPercent(skin, 'Lips_Local_Lwr_Nurb.cv[0][0:3]', tv=[fake_jaw, 0.6])
	cmds.skinPercent(skin, 'Lips_Local_Lwr_Nurb.cv[0][0:3]', tv=[fake_head, 0.4])

	#Connect Follciles to Head Rotation
	upr_fols = cmds.listRelatives('Lips_Upr_Fol_Grp', c=True)
	lwr_fols = cmds.listRelatives('Lips_Lwr_Fol_Grp', c=True)

	for fol in upr_fols + lwr_fols:
		cmds.orientConstraint('Head_Skl', fol, mo=True)
		cmds.scaleConstraint('Head_Skl', fol, mo=True)

	cmds.setAttr('Lips_Center_Ctrl_Offset_Grp.v', 0)

def convert_nose_to_global(head_parent_target="Head_Bnd"):
	if cmds.objExists('Nose_Origin_Rig_Grp'):
		nose_rig = 'Nose_Origin_Rig_Grp'
	else:
		nose_rig = 'Nose_Rig_Grp'
	cmds.parentConstraint(head_parent_target, nose_rig, mo=True)
	cmds.scaleConstraint(head_parent_target, nose_rig, mo=True)

def convert_ribbon_lips_to_global(head_parent_target="Head_Bnd"):
	locs = ['L_Lips_Sub_Loc','R_Lips_Sub_Loc','C_Lips_Upr_Local_Loc','C_Lips_Lwr_Local_Loc']
	ctrls = ['L_Lips_Sub_Ctrl','R_Lips_Sub_Ctrl','C_Lips_Upr_Main_Ctrl','C_Lips_Lwr_Main_Ctrl']

	for loc, ctrl in zip(locs, ctrls):
		disconnect_attrs(loc)
		cmds.parentConstraint(ctrl, loc, mo=True)
		#cmds.scaleConstraint(ctrl, loc, mo=True)

	lips_skel_joints = ['R_Lips_Upr_01_Skl', 'R_Lips_Upr_02_Skl', 'C_Lips_Upr_Skl', 'L_Lips_Upr_02_Skl', 'L_Lips_Upr_01_Skl',
 						'R_Lips_Lwr_01_Skl', 'R_Lips_Lwr_02_Skl', 'C_Lips_Lwr_Skl', 'L_Lips_Lwr_02_Skl', 'L_Lips_Lwr_01_Skl',]
	for jnt in lips_skel_joints:
		normal_jnt = jnt.replace('_Skl', '_Bnd')
		cmds.parentConstraint(normal_jnt, jnt, mo=True)
		#cmds.scaleConstraint(normal_jnt, jnt, mo=True)

	# from Mutant_Tools.Utils.IO import SkinUtils
	# reload(Mutant_Tools.Utils.IO.SkinUtils)
	# cSkin = SkinUtils.Skinning()

	# #change skin a bit
	# for side in ['Lwr', 'Upr']:
	# 	skin = cSkin.get_skin_from_geo('Lips_{}_Nurb'.format(side))
	# 	cmds.skinPercent(skin, 'Lips_{}_Nurb.cv[12:13][0:3]'.format(side), tv=['L_Lips_{}_02_Ctrl_Jnt'.format(side), 1])
	#
	# 	cmds.skinPercent(skin, 'Lips_{}_Nurb.cv[11][0:3]'.format(side), tv=['L_Lips_{}_01_Ctrl_Jnt'.format(side), 0.5])
	# 	cmds.skinPercent(skin, 'Lips_{}_Nurb.cv[11][0:3]'.format(side), tv=['L_Lips_{}_02_Ctrl_Jnt'.format(side), 0.5])
	# 	cmds.skinPercent(skin, 'Lips_{}_Nurb.cv[11][0:3]'.format(side), tv=['C_Lips_{}_Ctrl_Jnt'.format(side), 0])
	#
	# 	cmds.skinPercent(skin, 'Lips_{}_Nurb.cv[10][0:3]'.format(side), tv=['L_Lips_{}_01_Ctrl_Jnt'.format(side), 0.75])
	# 	cmds.skinPercent(skin, 'Lips_{}_Nurb.cv[10][0:3]'.format(side), tv=['L_Lips_{}_02_Ctrl_Jnt'.format(side), 0.25])
	#
	# 	cmds.skinPercent(skin, 'Lips_{}_Nurb.cv[9][0:3]'.format(side), tv=['L_Lips_{}_01_Ctrl_Jnt'.format(side), 1])
	#
	# 	cmds.skinPercent(skin, 'Lips_{}_Nurb.cv[8][0:3]'.format(side), tv=['L_Lips_{}_01_Ctrl_Jnt'.format(side), 0.5])
	# 	cmds.skinPercent(skin, 'Lips_{}_Nurb.cv[8][0:3]'.format(side), tv=['C_Lips_{}_Ctrl_Jnt'.format(side), 0.5])
	#
	# 	cmds.skinPercent(skin, 'Lips_{}_Nurb.cv[6:7][0:3]'.format(side), tv=['C_Lips_{}_Ctrl_Jnt'.format(side), 1])
	#
	# 	cmds.skinPercent(skin, 'Lips_{}_Nurb.cv[5][0:3]'.format(side), tv=['R_Lips_{}_01_Ctrl_Jnt'.format(side), 0.5])
	# 	cmds.skinPercent(skin, 'Lips_{}_Nurb.cv[5][0:3]'.format(side), tv=['C_Lips_{}_Ctrl_Jnt'.format(side), 0.5])
	#
	# 	cmds.skinPercent(skin, 'Lips_{}_Nurb.cv[4][0:3]'.format(side), tv=['R_Lips_{}_01_Ctrl_Jnt'.format(side), 1])
	#
	# 	cmds.skinPercent(skin, 'Lips_{}_Nurb.cv[3][0:3]'.format(side), tv=['R_Lips_{}_01_Ctrl_Jnt'.format(side), 0.75])
	# 	cmds.skinPercent(skin, 'Lips_{}_Nurb.cv[3][0:3]'.format(side), tv=['R_Lips_{}_02_Ctrl_Jnt'.format(side), 0.25])
	#
	# 	cmds.skinPercent(skin, 'Lips_{}_Nurb.cv[2][0:3]'.format(side), tv=['R_Lips_{}_01_Ctrl_Jnt'.format(side), 0.5])
	# 	cmds.skinPercent(skin, 'Lips_{}_Nurb.cv[2][0:3]'.format(side), tv=['R_Lips_{}_02_Ctrl_Jnt'.format(side), 0.5])
	#
	# 	cmds.skinPercent(skin, 'Lips_{}_Nurb.cv[0:1][0:3]'.format(side), tv=['R_Lips_{}_02_Ctrl_Jnt'.format(side), 1])

	scale_connect_list = ['Lips_Upr_Jnt_Ctrl_Grp',
						  'Lips_Lwr_Jnt_Ctrl_Grp',
						  'L_Lips_Lwr_Local_Loc',
						  'R_Lips_Lwr_Local_Loc',
						  'C_Lips_Upr_Local_Loc',
						  'C_Lips_Lwr_Local_Loc',
						  'R_Lips_Upr_Local_Loc',
						  'L_Lips_Upr_Local_Loc']

	for sc_element in scale_connect_list:
		cmds.connectAttr('Global_Ctrl.sx', "{}.sx".format(sc_element))
		cmds.connectAttr('Global_Ctrl.sy', "{}.sy".format(sc_element))
		cmds.connectAttr('Global_Ctrl.sz', "{}.sz".format(sc_element))


def convert_lips_to_global(head_parent_target="Head_Bnd"):

	#CHANGE CTRL CONSTRAINTS
	mouth_mid_ctrs = ['L_Mid_01Lips_Up_Ctrl', 'R_Lips_Mid_Ctrl', 'L_Mid_02Lips_Up_Ctrl',
					  'L_Lips_Dw_Ctrl', 'L_Mid_01Lips_Dw_Ctrl', 'R_Lips_Up_Ctrl', 'R_Mid_02Lips_Dw_Ctrl',
					  '_MidLips_Up_Ctrl', 'R_Mid_02Lips_Up_Ctrl', 'L_Mid_02Lips_Dw_Ctrl', 'R_Mid_01Lips_Up_Ctrl',
					  '_MidLips_Dw_Ctrl', 'L_Lips_Mid_Ctrl', 'L_Lips_Up_Ctrl', 'R_Lips_Dw_Ctrl', 'R_Mid_01Lips_Dw_Ctrl',
					  ]
	constraints_map = {}

	for c in mouth_mid_ctrs:
		print(c)
		father = cmds.listRelatives(c, p=True)[0]
		constraint = cmds.listRelatives(father, c=True, type='parentConstraint')[0]
		attrs = cmds.listAttr(constraint, ud=True)
		constraint_data = {}
		for attr in attrs:
			ctrl = attr.replace('W0', '').replace('W1', '')
			value = cmds.getAttr(constraint + '.' + attr)
			constraint_data[ctrl] = value
		cmds.delete(constraint)
		print(constraint_data)
		constraints_map[c] = constraint_data

	print(constraints_map)

	for c in constraints_map:
		father = cmds.listRelatives(c, p=True)[0]
		data = constraints_map[c]
		cmds.select(cl=True)
		c_parents = []
		for c in data:
			if c == 'R_Lips_Main_Ctrl':
				c = 'R_Lips_Sub_Ctrl'
			if c == 'L_Lips_Main_Ctrl':
				c = 'L_Lips_Sub_Ctrl'
			c_parents.append(c)
		c = cmds.parentConstraint(c_parents, father, mo=True)[0]
		for ctrl in data:
			value = data[ctrl]
			if ctrl == 'R_Lips_Main_Ctrl':
				ctrl = 'R_Lips_Sub_Ctrl'
			if ctrl == 'L_Lips_Main_Ctrl':
				ctrl = 'L_Lips_Sub_Ctrl'
			try:
				cmds.setAttr('{}.{}W0'.format(c, ctrl), value)
			except:
				cmds.setAttr('{}.{}W1'.format(c, ctrl), value)

	from Mutant_Tools.Utils.External import Ribbonizer
	upr_nurb = cmds.nurbsPlane(ax=(0, 0, 1), d=3, v=7, lr=5)[0]
	cmds.rotate(0, 0, 90)
	cmds.move(0, 2, 0)

	upr_ctrl_grp, upr_rig_grp, upr_bnd_grp = Ribbonizer.ribbonize(surf_tr=upr_nurb,
																  equal=True,
																  num_of_Ctrls=7,
																  num_of_Jnts=7,
																  prefix='UprLip',
																  constrain=True,
																  add_fk=False,
																  wire=False,
																  middle_ctrl_pos='Middle')

	lwr_nurb = cmds.nurbsPlane(ax=(0, 0, 1), d=3, v=7, lr=5)[0]
	cmds.rotate(0, 0, 90)
	cmds.move(0, 0, 0)

	lwr_ctrl_grp, lwr_rig_grp, lwr_bnd_grp = Ribbonizer.ribbonize(surf_tr=lwr_nurb,
																  equal=True,
																  num_of_Ctrls=7,
																  num_of_Jnts=7,
																  prefix='LwrLip',
																  constrain=True,
																  add_fk=False,
																  wire=False,
																  middle_ctrl_pos='Middle')

	#remove ctrl in names
	print(lwr_ctrl_grp)
	for ctrl in cmds.listRelatives(lwr_ctrl_grp, ad=True)+cmds.listRelatives(upr_ctrl_grp, ad=True):
		print(ctrl)
		if ctrl.endswith('_Ctrl'):
			cmds.rename(ctrl, ctrl.replace('_Ctrl', '_FakeCtrl'))

	#Postion new ribbon on correct_place
	pos_map = {

		'UprLip_00_FakeCtrl' : 'R_Lips_Up_Ctrl',
		'UprLip_01_FakeCtrl': 'R_Mid_02Lips_Up_Ctrl',
		'UprLip_02_FakeCtrl': 'R_Mid_01Lips_Up_Ctrl',
		'UprLip_03_FakeCtrl': '_MidLips_Up_Ctrl',
		'UprLip_04_FakeCtrl': 'L_Mid_01Lips_Up_Ctrl',
		'UprLip_05_FakeCtrl': 'L_Mid_02Lips_Up_Ctrl',
		'UprLip_06_FakeCtrl': 'L_Lips_Up_Ctrl',

		'LwrLip_00_FakeCtrl': 'R_Lips_Dw_Ctrl',
		'LwrLip_01_FakeCtrl': 'R_Mid_02Lips_Dw_Ctrl',
		'LwrLip_02_FakeCtrl': 'R_Mid_01Lips_Dw_Ctrl',
		'LwrLip_03_FakeCtrl': '_MidLips_Dw_Ctrl',
		'LwrLip_04_FakeCtrl': 'L_Mid_01Lips_Dw_Ctrl',
		'LwrLip_05_FakeCtrl': 'L_Mid_02Lips_Dw_Ctrl',
		'LwrLip_06_FakeCtrl': 'L_Lips_Dw_Ctrl',
	}

	for fake_ctrl in pos_map:
		offset=cmds.listRelatives(fake_ctrl, p=True)[0]
		cmds.delete(cmds.pointConstraint(pos_map[fake_ctrl], offset))
		cmds.parentConstraint(pos_map[fake_ctrl], offset, mo=True)

	skl_map = {

		'UprLip_Bind_01_Bnd' : 'Lips_UpR__Skl',
		'UprLip_Bind_02_Bnd': 'Lips_UpR_Mid_02_Skl',
		'UprLip_Bind_03_Bnd': 'Lips_UpR_Mid_01_Skl',
		'UprLip_Bind_04_Bnd': 'Lips_Up_Mid_Skl',
		'UprLip_Bind_05_Bnd': 'Lips_UpL_Mid_01_Skl',
		'UprLip_Bind_06_Bnd': 'Lips_UpL_Mid_02_Skl',
		'UprLip_Bind_07_Bnd': 'Lips_UpL__Skl',

		'LwrLip_Bind_01_Bnd': 'Lips_DwR__Skl',
		'LwrLip_Bind_02_Bnd': 'Lips_DwR_Mid_02_Skl',
		'LwrLip_Bind_03_Bnd': 'Lips_DwR_Mid_01_Skl',
		'LwrLip_Bind_04_Bnd': 'Lips_Dw_Mid_Skl',
		'LwrLip_Bind_05_Bnd': 'Lips_DwL_Mid_01_Skl',
		'LwrLip_Bind_06_Bnd': 'Lips_DwL_Mid_02_Skl',
		'LwrLip_Bind_07_Bnd': 'Lips_DwL__Skl',
	}

	for bnd in skl_map:
		skl = skl_map[bnd]
		cmds.delete(cmds.pointConstraint(bnd, skl))
		cmds.parentConstraint(bnd, skl, mo=True)
		cmds.scaleConstraint(bnd, skl)

	cmds.parentConstraint(head_parent_target, lwr_ctrl_grp, mo=True)
	cmds.parentConstraint(head_parent_target, upr_ctrl_grp, mo=True)
	cmds.scaleConstraint(head_parent_target, lwr_ctrl_grp, mo=True)
	cmds.scaleConstraint(head_parent_target, upr_ctrl_grp, mo=True)

	cmds.parent(lwr_ctrl_grp, lwr_rig_grp, lwr_bnd_grp, 'Rig_Grp')
	cmds.parent(upr_ctrl_grp, upr_rig_grp, upr_bnd_grp, 'Rig_Grp')

	#force nurb skin
	# Select your NURBS surface
	nurbs_surface = 'LwrLip_ribbon_surface'
	cmds.select(nurbs_surface)

	# Get the skinCluster node
	skin_cluster = cmds.ls(cmds.listHistory(nurbs_surface), type='skinCluster')[0]
	influence_objects = cmds.skinCluster(skin_cluster, q=True, inf=True)
	cmds.skinPercent(skin_cluster, 'LwrLip_ribbon_surface.cv[8:9][0:3]', transformValue=[('LwrLip_Ctrl_07_Jnt', 1.0)])
	cmds.skinPercent(skin_cluster, 'LwrLip_ribbon_surface.cv[7][0:3]', transformValue=[('LwrLip_Ctrl_06_Jnt', 1.0)])
	cmds.skinPercent(skin_cluster, 'LwrLip_ribbon_surface.cv[6][0:3]', transformValue=[('LwrLip_Ctrl_05_Jnt', 1.0)])
	cmds.skinPercent(skin_cluster, 'LwrLip_ribbon_surface.cv[4:5][0:3]', transformValue=[('LwrLip_Ctrl_04_Jnt', 1.0)])
	cmds.skinPercent(skin_cluster, 'LwrLip_ribbon_surface.cv[3][0:3]', transformValue=[('LwrLip_Ctrl_03_Jnt', 1.0)])
	cmds.skinPercent(skin_cluster, 'LwrLip_ribbon_surface.cv[2][0:3]', transformValue=[('LwrLip_Ctrl_02_Jnt', 1.0)])
	cmds.skinPercent(skin_cluster, 'LwrLip_ribbon_surface.cv[0:1][0:3]', transformValue=[('LwrLip_Ctrl_01_Jnt', 1.0)])


	nurbs_surface = 'UprLip_ribbon_surface'
	cmds.select(nurbs_surface)
	skin_cluster = cmds.ls(cmds.listHistory(nurbs_surface), type='skinCluster')[0]
	influence_objects = cmds.skinCluster(skin_cluster, q=True, inf=True)
	cmds.skinPercent(skin_cluster, 'UprLip_ribbon_surface.cv[8:9][0:3]', transformValue=[('UprLip_Ctrl_07_Jnt', 1.0)])
	cmds.skinPercent(skin_cluster, 'UprLip_ribbon_surface.cv[7][0:3]', transformValue=[('UprLip_Ctrl_06_Jnt', 1.0)])
	cmds.skinPercent(skin_cluster, 'UprLip_ribbon_surface.cv[6][0:3]', transformValue=[('UprLip_Ctrl_05_Jnt', 1.0)])
	cmds.skinPercent(skin_cluster, 'UprLip_ribbon_surface.cv[4:5][0:3]', transformValue=[('UprLip_Ctrl_04_Jnt', 1.0)])
	cmds.skinPercent(skin_cluster, 'UprLip_ribbon_surface.cv[3][0:3]', transformValue=[('UprLip_Ctrl_03_Jnt', 1.0)])
	cmds.skinPercent(skin_cluster, 'UprLip_ribbon_surface.cv[2][0:3]', transformValue=[('UprLip_Ctrl_02_Jnt', 1.0)])
	cmds.skinPercent(skin_cluster, 'UprLip_ribbon_surface.cv[0:1][0:3]', transformValue=[('UprLip_Ctrl_01_Jnt', 1.0)])


def create_game_joint_based_on_bnd(bnd_joint, do_scale, scale_constraint=True, segmentScaleCompensate=False):
	game_joint = cmds.joint(
		n=bnd_joint.replace('_Bnd', '_Skl'))
	mt.match(game_joint, bnd_joint, t=True, r=True, s=False)

	cmds.parentConstraint(bnd_joint, game_joint)

	cmds.setAttr('{}.segmentScaleCompensate'.format(game_joint), segmentScaleCompensate)

	if not do_scale:
		return game_joint

	if scale_constraint:
		cmds.scaleConstraint(bnd_joint, game_joint, mo=True)

	else:
		source2parentSpace_mmult = cmds.createNode('multMatrix', n=bnd_joint + '_src2parentSpace')
		cmds.connectAttr('{}.worldMatrix[0]'.format(bnd_joint), '{}.matrixIn[0]'.format(source2parentSpace_mmult), f=True)
		cmds.connectAttr('{}.parentInverseMatrix'.format(game_joint), '{}.matrixIn[1]'.format(source2parentSpace_mmult), f=True)

		source2parentSpace_srt = cmds.createNode('decomposeMatrix', n=source2parentSpace_mmult+'_srt')

		cmds.connectAttr('{}.matrixSum'.format(source2parentSpace_mmult), '{}.inputMatrix'.format(source2parentSpace_srt), f=True)
		cmds.connectAttr('{}.outputScale'.format(source2parentSpace_srt), '{}.scale'.format(game_joint), f=True)


	return game_joint


def disconnect_attrs(obj=""):
	transform_attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "translate", "rotate", "scale"]

	for attr in transform_attrs:
		incoming_connections = cmds.listConnections("{}.{}".format(obj, attr), d=False, s=True, plugs=True)
		if incoming_connections:
			cmds.disconnectAttr(incoming_connections[0], "{}.{}".format(obj, attr))


def convert_cheeks_to_global(prefix_name="Cheecks"):
	transform_attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]
	# scale_attrs = ["scaleX", "scaleY", "scaleZ",]

	comissure_mouth_ctrls = ["Top", "Mid", "Btm"]

	for side in ["L", "R"]:

		master_ctrl_grp = "{}_{}_Ctrl_Grp".format(side, prefix_name)

		if cmds.objExists(master_ctrl_grp):
			block_parent_constraint = cmds.listConnections("{}.translateX".format(master_ctrl_grp))[0]
			block_parent = cmds.listConnections("{}.target[0].targetParentMatrix".format(block_parent_constraint))

			# Determining where to place the parent and scale constraints based on side.
			if side == "R":
				mirror_ctrl_grp = cmds.listRelatives(master_ctrl_grp, parent=True)
				cmds.scaleConstraint(block_parent, mirror_ctrl_grp, mo=True)

			elif side == "L":
				cmds.scaleConstraint(block_parent, master_ctrl_grp, mo=True)

			#####################
			###Comissure Ctrls###
			#####################

			# For every main comissure ctrl:
			for comissure_mouth_ctrl in comissure_mouth_ctrls:
				# Remove direct connections in all attributes of the curve's driving joints.
				disconnect_attrs(obj="{}_{}_{}_Jnt".format(side, prefix_name, comissure_mouth_ctrl))

				# Connect the controls to the driving joints through constraints instead.
				cmds.parentConstraint("{}_{}_{}_Ctrl".format(side, prefix_name, comissure_mouth_ctrl),
									  "{}_{}_{}_Jnt".format(side, prefix_name, comissure_mouth_ctrl))
				cmds.scaleConstraint("{}_{}_{}_Ctrl".format(side, prefix_name, comissure_mouth_ctrl),
									 "{}_{}_{}_Jnt".format(side, prefix_name, comissure_mouth_ctrl))

			# In order to eliminate the tweak ctrl's double transform, inherit transforms must be off.
			cmds.setAttr("{}_{}_Tweeks_Ctrl_Grp.inheritsTransform".format(side, prefix_name), 0)

			# Right side flips if inherit transforms are off, the need to redo the flipping in that group.
			if side == "R":
				cmds.setAttr("{}_{}_Tweeks_Ctrl_Grp.scaleX".format(side, prefix_name), -1)

			# To have the joints orient to the head after turning off inherit transforms, some extra constraints are needed.
			# Eliminating direct connections between tweak driver joints and their offset groups.
			for num in range(0, 6):
				for suffix in ["Jnt", "Ctrl_Offset_Grp"]:
					disconnect_attrs(obj="{}_{}_{}_{}".format(side, prefix_name, num, suffix))

				# Creating constraints from ctrls to joints.
				cmds.parentConstraint("{}_{}_{}_Ctrl".format(side, prefix_name, num),
									  "{}_{}_{}_Jnt".format(side, prefix_name, num))
				cmds.scaleConstraint("{}_{}_{}_Ctrl".format(side, prefix_name, num),
									 "{}_{}_{}_Jnt".format(side, prefix_name, num))

				# Creating constraints from block parent to offset groups.
				cmds.orientConstraint(block_parent, "{}_{}_{}_Jnt_Offset_Grp".format(side, prefix_name, num), mo=True)
				cmds.scaleConstraint(block_parent, "{}_{}_{}_Jnt_Offset_Grp".format(side, prefix_name, num), mo=True)

				# Creating remaining constraints.
				cmds.parentConstraint("{}_{}_{}_Jnt_Offset_Grp".format(side, prefix_name, num),
									  "{}_{}_{}_Ctrl_Offset_Grp".format(side, prefix_name, num), mo=True)
				cmds.scaleConstraint("{}_{}_{}_Jnt_Offset_Grp".format(side, prefix_name, num),
									 "{}_{}_{}_Ctrl_Offset_Grp".format(side, prefix_name, num), mo=True)

			#####################
			##### Main Ctrls ####
			#####################

			# Deleting conections from the "Main" cheek joint.
			disconnect_attrs(obj="{}_{}_Main_Jnt".format(side, prefix_name))

			# Creating constraint connections instead:
			cmds.parentConstraint("{}_{}_Main_Ctrl".format(side, prefix_name),
								  "{}_{}_Main_Jnt".format(side, prefix_name))
			cmds.scaleConstraint("{}_{}_Main_Ctrl".format(side, prefix_name),
								 "{}_{}_Main_Jnt".format(side, prefix_name))

			#####################
			##### Bone Ctrls ####
			#####################

			for num in range(0, 4):
				# Disconnecting all direct connection attributes from the driving joints and their offset groups.
				for suffix in ["Jnt_Auto_Grp", "Jnt"]:
					if cmds.objExists("{}_{}_Bone_{}_{}".format(side, prefix_name, num, suffix)):
						disconnect_attrs(obj="{}_{}_Bone_{}_{}".format(side, prefix_name, num, suffix))

				# Creating constraint connections instead.
				cmds.parentConstraint("{}_{}_Bone_{}_Ctrl".format(side, prefix_name, num),
									  "{}_{}_Bone_{}_Jnt".format(side, prefix_name, num))
				cmds.scaleConstraint("{}_{}_Bone_{}_Ctrl".format(side, prefix_name, num),
									 "{}_{}_Bone_{}_Jnt".format(side, prefix_name, num))

				# Connecting Bone 3 Control because it is inside the tweaks ctrl grp.
				cmds.parentConstraint(block_parent, "{}_{}_Bone_3_Ctrl_Offset_Grp".format(side, prefix_name), mo=True)
				cmds.scaleConstraint(block_parent, "{}_{}_Bone_3_Ctrl_Offset_Grp".format(side, prefix_name), mo=True)


