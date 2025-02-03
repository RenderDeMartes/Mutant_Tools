from __future__ import absolute_import, division
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
from Mutant_Tools.UI.Helpers import load_helpers
reload(load_helpers)

try:cHelperUI.close()
except:pass
cHelperUI = load_helpers.HelperUI()
cHelperUI.show()

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
	from star.entities import Project
except:
	pass
import pprint



# -------------------------------------------------------------------

# QT WIndow!
FOLDER_NAME = 'Helpers'
Title = 'Helpers'
UI_File = 'Helpers.ui'

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

import Mutant_Tools.Utils.Wrap
from Mutant_Tools.Utils.Wrap import wrap_utils
import imp
imp.reload(wrap_utils)
cWrap = wrap_utils.Wrap3D()

from Mutant_Tools.Utils.Wrap.Skeletor import Skeletor
reload(Skeletor)
cSkeletor = Skeletor.Skeletor()

import Mutant_Tools
import Mutant_Tools.Utils.Helpers
from Mutant_Tools.Utils.Helpers import helpers
reload(Mutant_Tools.Utils.Helpers.helpers)
mh = helpers.Helpers()

import Mutant_Tools.UI
from Mutant_Tools.UI import QtMutantWindow
reload(QtMutantWindow)
Qt_Mutant = QtMutantWindow.Qt_Mutant()


# -------------------------------------------------------------------


def maya_main_window():
	main_window_ptr = omui.MQtUtil.mainWindow()
	return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class HelperUI(QtMutantWindow.Qt_Mutant):

	def __init__(self):
		super(HelperUI, self).__init__()

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

		self.create_layout()
		self.create_connections()

		self.make_frameless()

		self.hierarchy_array = []
		self.block_order = []

		self.create_menu()



	# -------------------------------------------------------------------

	def create_layout(self):
		"""

		Returns:

		"""

		#self.ui.mutant_tools_button.setIcon(QtGui.QIcon(os.path.join(IconsPath, 'LogoWhite03.png')))
		#self.ui.mutant_tools_button.setIconSize(QtCore.QSize(25, 25))
		try:
			self.populate_shows()
			self.populate_assets()
		except:
			pass

		self.resize(300,650)

		self.add_icons_based_on_json(json_file = os.path.join(FOLDER, 'UI', FOLDER_NAME, 'helpers_icons.json'))
		self.ui.tabs.setCurrentIndex(0)

		self.load_resets()

	def create_connections(self):
		"""

		Returns:

		"""

		self.ui.shows_combo.currentIndexChanged.connect(self.populate_assets)
		self.ui.filter_text.textChanged.connect(self.populate_assets)

		self.ui.initialize_rig_button.clicked.connect(self.initialize_rig)
		#self.ui.mutant_tools_button.clicked.connect(self.open_autorig_ui)

		self.ui.wip.clicked.connect(self.activate_wip_mode)
		self.ui.complete.clicked.connect(self.activate_complete_mode)
		self.ui.lock_geo.clicked.connect(self.lock_geo)
		self.ui.unlock_geo.clicked.connect(self.unlock_geo)
		self.ui.shampooBtn.clicked.connect(self.shampoo)

		#Boday Tab

		self.ui.zeroX.clicked.connect(lambda: self.zero(axis='X'))
		self.ui.zeroY.clicked.connect(lambda: self.zero(axis='Y'))
		self.ui.zeroZ.clicked.connect(lambda: self.zero(axis='Z'))
		self.ui.line_up_finger.clicked.connect(self.line_up_finger)
		self.ui.unparent_guides.clicked.connect(self.unparent_guides)
		self.ui.parent_guides.clicked.connect(self.parent_guides)
		self.ui.ankle_to_ankle.clicked.connect(self.ankle_to_ankle)
		self.ui.wrist_to_writs.clicked.connect(self.wrist_to_writs)
		self.ui.neck_to_spine.clicked.connect(self.neck_to_spine)

		self.ui.fix_arms.clicked.connect(self.fix_arms)
		self.ui.fix_clav.clicked.connect(self.fix_clav)
		self.ui.fix_fingers_a.clicked.connect(self.fix_fingers_a)
		self.ui.fix_fingers_t.clicked.connect(self.fix_fingers_t)

		self.ui.pinky_reset.clicked.connect(self.zero_pinky)
		self.ui.ring_reset.clicked.connect(self.zero_ring)
		self.ui.middle_reset.clicked.connect(self.zero_middle)
		self.ui.index_reset.clicked.connect(self.zero_index)
		self.ui.thumb_reset.clicked.connect(self.zero_thumb)

  
		self.ui.fix_pelvis.clicked.connect(self.fix_pelvis)
		self.ui.fix_legs.clicked.connect(self.fix_legs)
		self.ui.fix_spine.clicked.connect(self.fix_spine)
		self.ui.fix_head.clicked.connect(self.fix_head)
		self.ui.fix_foot.clicked.connect(self.fix_foot)
		self.ui.fix_cog.clicked.connect(self.fix_cog)

		self.ui.shoe_to_guides.clicked.connect(self.shoe_to_guides)


		self.ui.remove_duplicate_names.clicked.connect(self.remove_dup_names)
		self.ui.studio_tag_ctrls.clicked.connect(self.tag_controllers)
		self.ui.remove_render_tag.clicked.connect(self.remove_render_tag)

		#Face Tab
		self.ui.skull.clicked.connect(self.show_skull)
		self.ui.eyes.clicked.connect(self.show_eyes)
		self.ui.lips.clicked.connect(self.show_lips)
		self.ui.brows.clicked.connect(self.show_brows)
		self.ui.cheecks.clicked.connect(self.show_cheecks)
		self.ui.jaw.clicked.connect(self.show_jaw)
		self.ui.nose.clicked.connect(self.show_nose)
		self.ui.mouth_up.clicked.connect(self.show_mouth_up)
		self.ui.mouth_down.clicked.connect(self.show_mouth_down)
		self.ui.mouth_wide.clicked.connect(self.show_mouth_wide)
		self.ui.mouth_narrow.clicked.connect(self.show_mouth_narrow)
		self.ui.add_extra_geos.clicked.connect(self.add_extra_geos)
		self.ui.l_add_to_eyes_wires.clicked.connect(self.l_add_to_eyes_wires)
		self.ui.r_add_to_eyes_wires.clicked.connect(self.r_add_to_eyes_wires)
		self.ui.auto_skin_lips.clicked.connect(self.auto_skin_lips)
		self.ui.auto_skin_eyes.clicked.connect(self.auto_skin_eyes)

		self.ui.upr_eyes_up.clicked.connect(lambda: self.eyes_up(mult=1))
		self.ui.upr_eyes_dw.clicked.connect(lambda: self.eyes_up(mult=-1))
		self.ui.lwr_eyes_up.clicked.connect(lambda: self.eyes_down(mult=-1))
		self.ui.lwr_eyes_dw.clicked.connect(lambda: self.eyes_down(mult=1))

		self.ui.upr_lips_up.clicked.connect(lambda: self.lips_up(mult=1))
		self.ui.upr_lips_dw.clicked.connect(lambda: self.lips_up(mult=-1))
		self.ui.lwr_lips_up.clicked.connect(lambda: self.lips_down(mult=-1))
		self.ui.lwr_lips_dw.clicked.connect(lambda: self.lips_down(mult=1))

		self.ui.reload_jaw_tester.clicked.connect(self.reload_jaw_tester)
		self.ui.delete_jaw_tester.clicked.connect(self.delete_jaw_tester)
		self.ui.jaw_tester_slider.valueChanged.connect(lambda: self.slider_movement(self.ui.jaw_tester_slider.value()))


		#Props Tab
		self.ui.tools_ui.clicked.connect(self.open_tools_ui)

		#Animals Tab
		self.ui.fix_quad_foot.clicked.connect(self.fix_quad_foot)

		#Other Tabs
		self.ui.reload_udims.clicked.connect(self.reload_udims)
		self.ui.label_joints.clicked.connect(self.label_joints)
		self.ui.proxy_maker.clicked.connect(self.proxy_maker)
		self.ui.reset_profile.clicked.connect(self.add_to_reset)

		self.ui.fari_deformersWeightsEditor.clicked.connect(self.fari_deformersWeightsEditor)
		self.ui.dont_press.clicked.connect(self.dont_press)
		self.ui.switch_ikfk.clicked.connect(self.switch_ikfk)


		#Clothes Tab
		self.ui.create_skirt_mirror_offsets.clicked.connect(self.create_skirt_mirror_offsets)
		self.ui.delete_skirt_mirror_offsets.clicked.connect(self.delete_skirt_mirror_offsets)
		self.ui.create_skirt_rigmeshes.clicked.connect(self.create_skirt_rigmeshes)
		self.ui.create_skirt_vis_toggle.clicked.connect(self.create_skirt_vis_toggle)

		#Crowds Tabs
		self.auto_connect_all_skin_buttons()
		self.ui.copy_selected_skin.clicked.connect(self.copy_selected_skin)
		self.ui.copy_ns_skin.clicked.connect(self.copy_ns_skin)



	# -------------------------------------------------------------------
	def open_autorig_ui(self):

		import Mutant_Tools
		from Mutant_Tools.UI.AutoRigger import load_autoRigger
		imp.reload(load_autoRigger)
		try:
			AutoRigger.close()
		except:
			pass
		AutoRigger = load_autoRigger.AutoRigger()
		AutoRigger.show()

	def populate_shows(self):
		projects = ['SP', 'AnythingGoes']
		self.ui.shows_combo.clear()
		self.ui.shows_combo.addItems(projects)

	def populate_assets(self):

		self.ui.assets_combo.clear()

		proj = Project.findby_name(self.ui.shows_combo.currentText())

		filter = self.ui.filter_text.text()

		assets = []

		for asset in proj.assets:
			if filter:
				if filter.lower() in asset.name.lower():
					assets.append(asset.name)
			else:
				assets.append(asset.name)

		self.ui.assets_combo.addItems(assets)

	@undo
	def reload_combos_ui(self):
		self.populate_shows()
		self.populate_assets()

	@undo
	def initialize_rig(self):

		proj = Project.findby_name(self.ui.shows_combo.currentText())
		asset = self.ui.assets_combo.currentText()
		for ass in proj.assets:
			if ass.name == asset:
				asset = ass
				break

		print(asset.name)

		#Open Latest Model

		pubs = asset.publishes
		if not pubs:
			return

		latest_version = False
		for pub in pubs:
			if pub.kind.name == 'geo-hi':
				versions = pub.versions
				if not versions:
					continue
				for version in versions:
					if version.is_latest:
						latest_version = version

		if not latest_version:
			return

		print(latest_version)
		print(latest_version.path)

		cmds.file(new=True, f=True)
		cmds.file(latest_version.path, i=True)

		#Create sid node

		from rigSystem.assetTemplates.core import get_one_sid, validate_sid
		sid = get_one_sid()
		sid = validate_sid(sid)
		sid.create_default_groups(kind='rig-hi')

		# get rigging task 

		rig_task = ''

		tasks = ['Rigging', 'Rig_Layout']
		for task in sid.entity.tasks:
			print(task)
			if str(task.name) in tasks:
				rig_task = task

		sid.tag(publish_kind='rig-hi', task=rig_task)

		#Open Rig UI
		import Mutant_Tools
		from Mutant_Tools.UI.AutoRigger import load_autoRigger
		reload(load_autoRigger)
		AutoRigger = load_autoRigger.AutoRigger()
		AutoRigger.show()

	@undo
	def activate_wip_mode(self):
		#studio groups
		try:
			cmds.setAttr('rig.v', 1)
			cmds.setAttr('bind.v', 1)
			cmds.setAttr('control.v', 1)
		except:
			pass

		self.unlock_geo()

		if cmds.objExists('Mutant_Build'):
			try:cmds.parent('Mutant_Build', w=True)
			except:pass
		if cmds.objExists('Mutant_Tools_Grp'):
			try:cmds.parent('Mutant_Tools_Grp', w=True)
			except:pass
			try:cmds.parent('Ctrl_Grp','Mutant_Tools_Grp')
			except:pass
			try:cmds.parent('Rig_Grp','Mutant_Tools_Grp')
			except:pass
			try:cmds.parent('Extra_Geo_Grp','Mutant_Tools_Grp')
			except:pass
			cmds.setAttr('Mutant_Tools_Grp.v', 1)
		if cmds.objExists('Rig_Grp'):
			try:cmds.parent('Bind_Joints_Grp','Rig_Grp')
			except:pass
			cmds.setAttr('Bind_Joints_Grp.v', 1)
			cmds.setAttr('Rig_Grp.v', 1)
		if cmds.objExists('Miscellaneous_Grp'):
			cmds.setAttr('Miscellaneous_Grp.v', 1)

		try:self.unreferece_geo()
		except:pass

	@undo
	def activate_complete_mode(self):
		if cmds.objExists('Mutant_Build'):
			try:cmds.parent('Mutant_Build', 'Template_Grp')
			except:pass
		if cmds.objExists('Mutant_Tools_Grp'):
			try:cmds.parent('Mutant_Tools_Grp', 'rig')
			except:pass
			try:cmds.parent('Ctrl_Grp','control')
			except:pass
			try:cmds.parent('Rig_Grp','Mutant_Tools_Grp')
			except:pass
			try:cmds.parent('Extra_Geo_Grp','Mutant_Tools_Grp')
			except:pass

			if cmds.objExists('rig'):
				cmds.setAttr('rig.v', 0)
				cmds.setAttr('Mutant_Tools_Grp.v', 0)

		if cmds.objExists('Rig_Grp'):
			try:cmds.parent('Bind_Joints_Grp','bind')
			except:pass
			cmds.setAttr('Bind_Joints_Grp.v', 0)
			if cmds.objExists('bind'):
				cmds.setAttr('bind.v', 0)
			cmds.setAttr('Rig_Grp.v', 0)
		if cmds.objExists('Miscellaneous_Grp'):
			cmds.setAttr('Miscellaneous_Grp.v', 0)

		if cmds.objExists('geo'):
			try:cmds.setAttr('geo.v', 1)
			except:cmds.setAttr('Global_Ctrl.GeoVis', 1)

		self.lock_geo()

		for ctrl in cmds.listRelatives('Ctrl_Grp', c=True):
			try:cmds.setAttr('{}.v'.format(ctrl), 1)
			except:pass

		self.turn_off_inherith_on_rig_childs()

		try:
			self.delete_jaw_tester()
		except:
			pass

		#Tag Controllers
		global_ctrl = 'Global_Ctrl'
		ctrls = cmds.ls('*_Ctrl') + cmds.ls('*_Connected_Crv')
		for ctrl in ctrls:
			if ctrl == global_ctrl:
				continue
			cmds.select(ctrl)
			mel.eval('TagAsController;')
			shapes = cmds.listRelatives(ctrl, shapes=True)
			if shapes:
				for shape in shapes:
					if cmds.attributeQuery('hideOnPlayback', node=shape, exists=True) and cmds.attributeQuery(
							'CtrlPlayback', node=global_ctrl, exists=True):
						cmds.connectAttr(global_ctrl + '.CtrlPlayback',
										 cmds.listRelatives(ctrl, shapes=True)[0] + '.hideOnPlayback', f=True)

		controllers = cmds.ls(type='controller')
		for tag in controllers:
			if cmds.objExists(global_ctrl):
				if cmds.attributeQuery('visibilityMode', node=tag, exists=True) and cmds.attributeQuery('CtrlVis', node=global_ctrl, exists=True):
					cmds.connectAttr(global_ctrl+'.CtrlVis', tag+'.visibilityMode', f=True)

	def turn_off_inherith_on_rig_childs(self):
		if not cmds.objExists('Mutant_Tools_Grp'):
			return
		mutant_grps = cmds.listRelatives('Mutant_Tools_Grp', c=True)
		for c in mutant_grps:
			cmds.setAttr('{}.inheritsTransform'.format(c), 0)

	@undo
	def lock_geo(self):
		cmds.setAttr("Global_Ctrl.Geo", 2)
		if not cmds.objExists('geo'):
			return
		try:
			geos = cmds.listRelatives("geo", ad=True)
			for each in geos:
				cmds.setAttr("{0}.overrideEnabled".format(each), 0)
		except:
			pass

	@undo
	def unlock_geo(self):
		cmds.setAttr("Global_Ctrl.Geo", 0)
		if not cmds.objExists('geo'):
			return
		try:
			geos = cmds.listRelatives("geo", ad=True)
			for each in geos:
				cmds.setAttr("{0}.overrideEnabled".format(each), 0)
		except:
			pass

	@undo
	def shampoo(self):
		from assetChecks import UI
		UI.open_ui()

	#-------------------------------------------------
	#-------------------------------------------------
	#----------------Body Tab-------------------------
	#-------------------------------------------------
	#-------------------------------------------------
	@undo
	def zero(self, axis=''):

		sel = cmds.ls(sl=True)

		self.unparent_guides()

		for s in sel:
			cmds.select(s)
			if axis == 'X':
				cmds.move(0, cmds.getAttr('{}.ty'.format(s)), cmds.getAttr('{}.tz'.format(s)))
			elif axis == 'Y':
				cmds.move(cmds.getAttr('{}.tx'.format(s)), 0, cmds.getAttr('{}.tz'.format(s)))
			else:
				cmds.move(cmds.getAttr('{}.tx'.format(s)), cmds.getAttr('{}.ty'.format(s)), 0)

		self.parent_guides()

	@undo
	def line_up_finger(self):
		sel = cmds.ls(sl=True)

		self.unparent_guides()

		main_z = cmds.getAttr('{}.translateZ'.format(sel[0]))
		print(main_z)
		print(sel)
		for s in sel:
			print(s)
			cmds.setAttr("{}.translateZ".format(s), main_z)

		self.parent_guides()

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
	def ankle_to_ankle(self):
		self.unparent_guides()
		cmds.delete(cmds.pointConstraint('L_Ankle_Guide', 'L_Foot_Ankle_Guide'))
		self.parent_guides()

	@undo
	def wrist_to_writs(self):
		self.unparent_guides()
		cmds.delete(cmds.pointConstraint('L_Wrist_Guide', 'L_Hand_Palm_Guide'))
		self.parent_guides()
	@undo
	def neck_to_spine(self):
		self.unparent_guides()
		cmds.delete(cmds.pointConstraint('Spine_End_Guide', 'Neck_Guide'))
		self.parent_guides()

	@undo
	def fix_arms(self):
		cWrap.fix_limb_arms_orientation()

	@undo
	def fix_clav(self):
		cWrap.fix_clav_orientation()

	@undo
	def fix_fingers_a(self):
		cWrap.fix_fingers_orientations(pose='A')

	@undo
	def fix_fingers_t(self):
		cWrap.fix_fingers_orientations(pose='T')

	@undo
	def zero_pinky(self):
		cWrap.zero_specific_finger('Pinky')
 
	@undo
	def zero_ring(self):
		cWrap.zero_specific_finger('Ring')
  
	@undo
	def zero_middle(self):
		cWrap.zero_specific_finger('Middle')
  
	@undo
	def zero_index(self):
		cWrap.zero_specific_finger('Index')
  
	@undo
	def zero_thumb(self):
		cWrap.zero_specific_finger('Thumb')
  
	@undo
	def fix_pelvis(self):
		cWrap.fix_pelvis_orientation()

	@undo
	def fix_legs(self):
		cWrap.fix_limb_legs_orientation()

	@undo
	def fix_spine(self):
		cWrap.fix_spine_orientation()

	@undo
	def fix_head(self):
		cWrap.fix_head_orientation()

	@undo
	def fix_foot(self):
		cWrap.fix_foot_orientation()

	@undo
	def fix_cog(self):
		cWrap.fix_cog_orientation()

	@undo
	def remove_dup_names(self):
		from mstar.nodes.sid import Sid
		from assetChecks.projectChecks.studio.checks import CheckUniqueNames
		import random
		import maya.mel as mel

		def fix_unique_names():

			sid = Sid.find()[0]  # getting the Sid node

			# Run check:
			check = CheckUniqueNames(sid)
			result = check.run()
			for item in result.items:
				item_name = item.item
				real_name = item_name.split('|')[-1]
				if item_name.endswith('_Ctrl'):
					continue
				else:
					try:
						print(item_name)
						cmds.select(item_name)
						to_rename = cmds.ls(sl=True)
						for i in to_rename:
							mel.eval('searchReplaceNames "{}" "{}" "selected";'.format(real_name, real_name + str(
								random.randint(0, 100))))
					except:
						pass

		fix_unique_names()
		fix_unique_names()
		fix_unique_names()

	@undo
	def tag_controllers(self):
		from rigSystem.assetTemplates import get_hierarchy, get_one_sid
		rid = get_hierarchy(get_one_sid())
		rid.sid.tag_node().set_tag('animctrl', cmds.ls('*{}'.format(nc['ctrl'])))

	@undo
	def remove_render_tag(self):
		sel = cmds.ls(sl=True)
		for geo in sel:
			geo = cmds.rename(geo, geo.replace('_hi', '_Geo'))
			connections = cmds.listConnections(geo + '.message', p=True)
			if not connections:
				continue
			else:
				for c in connections:
					cmds.disconnectAttr(geo + '.message', c)

	@undo
	def shoe_to_guides(self):
		shoe=cmds.ls(sl=True)
		cmds.select(cmds.duplicate(shoe))
		print(shoe)
		bb = cmds.geomToBBox(keepOriginal=False, ns='_BB')[0]
		bb = cmds.ls(sl=True)[0]
		print(bb)
		self.unparent_guides()

		#Create position clusters
		front_cluster = cmds.cluster('{}.e[2]'.format(bb))
		back_cluster = cmds.cluster('{}.e[0]'.format(bb))
		in_cluster = cmds.cluster('{}.e[3]'.format(bb))
		out_cluster = cmds.cluster('{}.e[1]'.format(bb))

		#place out boxe guides
		cmds.delete(cmds.pointConstraint(back_cluster, 'L_Foot_Heel_Guide',mo=False))
		cmds.delete(cmds.pointConstraint(front_cluster, 'L_Foot_Toes_Guide',mo=False))
		cmds.delete(cmds.pointConstraint(in_cluster, 'L_Foot_In_Guide',mo=False, skip=['y', 'z']))
		cmds.delete(cmds.pointConstraint(out_cluster, 'L_Foot_Out_Guide',mo=False, skip=['y', 'z']))

		#Place floor heel and ball
		ball_floor_pc = cmds.pointConstraint(front_cluster, back_cluster, 'L_Foot_BallFloor_Guide', mo=False)
		heel_floor_pc = cmds.pointConstraint(front_cluster, back_cluster, 'L_Foot_HeelMid_Guide', mo=False)
		cmds.setAttr("L_Foot_HeelMid_Guide_pointConstraint1.{}HandleW1".format(back_cluster[0]), 3)
		cmds.setAttr("L_Foot_BallFloor_Guide_pointConstraint1.{}HandleW0".format(front_cluster[0]), 3)
		cmds.delete(ball_floor_pc, heel_floor_pc)

		#Place ankle and ball
		cmds.delete(cmds.pointConstraint('L_Ankle_Guide', 'L_Foot_Ankle_Guide'))
		ball_pc = cmds.pointConstraint('L_Foot_Ankle_Guide', 'L_Foot_Toes_Guide', 'L_Foot_Ball_Guide', mo=False)
		cmds.setAttr("L_Foot_Ball_Guide_pointConstraint1.L_Foot_Toes_GuideW1", 2)
		cmds.delete(ball_pc)

		#Put in and out same as the ball flor
		cmds.delete(cmds.pointConstraint('L_Foot_BallFloor_Guide', 'L_Foot_In_Guide',mo=False, skip=['y', 'x']))
		cmds.delete(cmds.pointConstraint('L_Foot_BallFloor_Guide', 'L_Foot_Out_Guide',mo=False, skip=['y', 'x']))

		cmds.delete(front_cluster, back_cluster, in_cluster, out_cluster)

		self.parent_guides()

		#Reorient joints
		self.fix_foot()

	def unreferece_geo(self):
		for geo in cmds.listRelatives('geo',ad=True):
			cmds.setAttr('{}.overrideEnabled'.format(geo),1)
			cmds.connectAttr('Global_Ctrl.Geo','{}.overrideDisplayType'.format(geo),f=True)

	#-------------------------------------------------
	#-------------------------------------------------
	#----------------Face Tab-------------------------
	#-------------------------------------------------
	#-------------------------------------------------

	@undo
	def hide_face_componets(self):

		self.activate_wip_mode()

		misc_childs = cmds.listRelatives('Miscellaneous_Grp', c=True)
		bind_childs = cmds.listRelatives('Bind_Joints_Grp', c=True)
		ctrls_childs = cmds.listRelatives('Ctrl_Grp', c=True)
		locals_childs = cmds.listRelatives('BodySkull_Locals_Grp', c=True)

		skip = ['Vis_Ctrl']


		for c in misc_childs+bind_childs+ctrls_childs+locals_childs:
			if c in skip:
				continue
			cmds.setAttr('{}.v'.format(c) ,0)
		if cmds.objExists('geo'):
			try:cmds.setAttr('geo.v', 0)
			except:cmds.setAttr('Global_Ctrl.GeoVis', 0)


	@undo
	def hide_locals_except(self, exception):

		print(exception)
		locals_childs = cmds.listRelatives('BodySkull_Locals_Grp', c=True)
		for c in locals_childs:
			if str(c) == str(exception):
				print('Match')
				cmds.setAttr('{}.v'.format(exception) ,1)
			else:
				cmds.setAttr('{}.v'.format(c) ,0)

	@undo
	def show_this(self, show_list, local_grp=None):
		match_found = False
		for i in show_list:
			ad = cmds.listRelatives(i, ad=True)
			cmds.select(i)
			sel = cmds.ls(sl=True)
			for s in sel+ad:
				try:
					cmds.setAttr('{}.v'.format(s), 1)
				except:pass
			if not match_found:
				self.hide_locals_except(i)
				match_found=True

		if local_grp:
			if cmds.objExists('Local_Extra'):
				for i in cmds.listRelatives('Local_Extra', c=True):
					if i != local_grp:
						cmds.setAttr(i+'.v', 0)
					else:
						cmds.setAttr(i+'.v', 1)
						childs = cmds.listRelatives(i, c=True)
						for c in childs:
							cmds.setAttr(c + '.v', 1)

	@undo
	def show_skull(self):
		self.hide_face_componets()
		show_list = ['Skull_Ctrl_Grp', 'Skull_Rig_Grp', 'Skull_*_Bnd', 'SkullLocal_Rig_Grp']
		self.show_this(show_list=show_list)

	@undo
	def show_eyes(self):
		self.hide_face_componets()
		show_list = ['Locals_Rig_Grp', 'BodyEyes', 'L_Eyelids_Rig_Grp', '*_Eyelids_Up_*_Bnd', 'L_Eyelids_Ctrl_Grp', 'R_Eyelids_Ctrl_GrpMirror_Grp', 'R_Eyelids_Rig_GrpMirror_Grp', 'L_Orbicularis_Ctrl_Grp', 'R_Orbicularis_Ctrl_Grp']
		if cmds.attributeQuery('eyeMidCtrls', node='Vis_Ctrl', exists=True):
			cmds.setAttr('Vis_Ctrl.eyeMidCtrls', 1)
		self.show_this(show_list=show_list, local_grp='Local_Extra_BodyEyes')

	@undo
	def show_lips(self):
		self.hide_face_componets()
		show_list = ['Locals_Rig_Grp', 'Lips_Ctrl_Grp', 'Lips_Rig_Grp', 'BodyLips', '*Lips_*_Bnd']
		try:
			cmds.setAttr("Vis_Ctrl.lipsMainCtrls", 1)
			cmds.setAttr("Vis_Ctrl.lipsMidCtrls", 1)
		except:pass
		self.show_this(show_list=show_list, local_grp='Local_Extra_BodyLips')


	@undo
	def show_brows(self):
		self.hide_face_componets()
		show_list = ['Locals_Rig_Grp', 'BodyBrows', '*_Brow_*_Bnd', '*_Brow_Ctrl*', '*_Brow_Rig_Grp*', 'C_Brow_Bnd']
		self.show_this(show_list=show_list, local_grp='Local_Extra_BodyBrows')

	@undo
	def show_cheecks(self):
		self.hide_face_componets()
		show_list = ['Locals_Rig_Grp', 'BodyCheeks', '*_Cheecks_*_Bnd', '*_Cheecks_Ctrl*', '*_Cheecks_Rig_Grp*']
		self.show_this(show_list=show_list, local_grp='Local_Extra_BodyCheeks')

	@undo
	def show_jaw(self):
		self.hide_face_componets()
		show_list = ['Locals_Rig_Grp', 'BodyJaw', 'Jaw*Bnd', 'Jaw_Ctrl_Grp', 'Jaw_Rig_Grp']
		self.show_this(show_list=show_list, local_grp='Local_Extra_BodyJaw')

	@undo
	def show_nose(self):
		self.hide_face_componets()
		show_list = ['Locals_Rig_Grp', 'BodyNose', 'Nose*Bnd', 'Nose_Rig_Grp', 'Nose_Ctrl_Grp']
		self.show_this(show_list=show_list, local_grp='Local_Extra_BodyNose')
		if cmds.attributeQuery('noseMainCtrls', node='Vis_Ctrl', exists=True):
			cmds.setAttr("Vis_Ctrl.noseMainCtrls", 1)
		if cmds.attributeQuery('noseMidCtrls', node='Vis_Ctrl', exists=True):
			cmds.setAttr("Vis_Ctrl.noseMidCtrls", 1)


	@undo
	def show_mouth_up(self):
		self.hide_face_componets()
		show_list = ['Locals_Rig_Grp', 'BodyMouthUp', '*Commissures_Up*_Bnd',  'Commissures_Rig_Grp', 'Lips_Ctrl_Grp']
		self.show_this(show_list=show_list, local_grp='Local_Extra_BodyMouthUp')
		cmds.setAttr("Vis_Ctrl.lipsMidCtrls", 0)
		try:cmds.setAttr("Vis_Ctrl.lipsMainCtrls", 1)
		except:pass
	@undo
	def show_mouth_down(self):
		self.hide_face_componets()
		show_list = ['Locals_Rig_Grp', 'BodyMouthDown', '*Commissures_Down*_Bnd', 'Commissures_Rig_Grp', 'Lips_Ctrl_Grp']
		self.show_this(show_list=show_list, local_grp='Local_Extra_BodyMouthDown')
		cmds.setAttr("Vis_Ctrl.lipsMidCtrls", 0)
		try:cmds.setAttr("Vis_Ctrl.lipsMainCtrls", 1)
		except:pass

	@undo
	def show_mouth_wide(self):
		self.hide_face_componets()
		show_list = ['Locals_Rig_Grp', 'BodyMouthWide', '*Commissures_Wide*_Bnd',  'Commissures_Rig_Grp', 'Lips_Ctrl_Grp']
		self.show_this(show_list=show_list, local_grp='Local_Extra_BodyMouthWide')
		cmds.setAttr("Vis_Ctrl.lipsMidCtrls", 0)
		try:cmds.setAttr("Vis_Ctrl.lipsMainCtrls", 1)
		except:pass
	@undo
	def show_mouth_narrow(self):
		self.hide_face_componets()
		show_list = ['Locals_Rig_Grp', 'BodyMouthNarrow', '*Commissures_Narrow*_Bnd',  'Commissures_Rig_Grp', 'Lips_Ctrl_Grp']
		self.show_this(show_list=show_list, local_grp='Local_Extra_BodyMouthNarrow')
		cmds.setAttr("Vis_Ctrl.lipsMidCtrls", 0)
		cmds.setAttr("Vis_Ctrl.lipsMainCtrls", 1)

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

	@undo
	def l_add_to_eyes_wires(self):
		sel = cmds.ls(sl=True)
		if not sel:
			cmds.warning('We need a selection for this to work')
			return False
		for s in sel:
			mel.eval('deformer -e -g {} L_Eyelids_Dw_ClusterWire;'.format(s))
			mel.eval('deformer -e -g {} L_Eyelids_Up_ClusterWire;'.format(s))
			print('Added to:', s)
	@undo
	def r_add_to_eyes_wires(self):
		sel = cmds.ls(sl=True)
		if not sel:
			cmds.warning('We need a selection for this to work')
			return False
		for s in sel:
			mel.eval('deformer -e -g {} R_Eyelids_Dw_ClusterWire;'.format(s))
			mel.eval('deformer -e -g {} R_Eyelids_Up_ClusterWire;'.format(s))
			print('Added to:', s)
	@undo
	def auto_skin_lips(self):
		from Mutant_Tools.UI.Helpers.helpers_utils import auto_skin_helpers
		reload(auto_skin_helpers)
		upper_edge = cmds.getAttr('Lips_Config.SetUpperEdge')
		dot_index = upper_edge.index('.')
		src_mesh = upper_edge[0:dot_index]
		upper_edge = upper_edge.replace(src_mesh, 'BodyLips').replace(' ', '').split(',')
		lower_edge = cmds.getAttr('Lips_Config.SetLowerEdge').replace(src_mesh, 'BodyLips').replace(' ', '').split(',')

		upper_edge.extend(lower_edge)
		upper_edge = cmds.filterExpand(upper_edge, sm=32)
		loop_span = self.ui.auto_skin_range_value.value()
		auto_skin_helpers.skin_edge_loop_joints('BodyLips', upper_edge, loop_span)



	@undo
	def auto_skin_eyes(self):
		from Mutant_Tools.UI.Helpers.helpers_utils import auto_skin_helpers
		reload(auto_skin_helpers)
		upper_edge = cmds.getAttr('L_Eyelids_Config.SetUpperEdge')
		dot_index = upper_edge.index('.')
		src_mesh = upper_edge[0:dot_index]
		upper_edge = upper_edge.replace(src_mesh, 'BodyEyes').replace(' ', '').split(
			',')
		lower_edge = cmds.getAttr('L_Eyelids_Config.SetLowerEdge').replace(src_mesh, 'BodyEyes').replace(' ', '').split(
			',')

		upper_edge.extend(lower_edge)
		upper_edge = cmds.filterExpand(upper_edge, sm=32)
		loop_span = self.ui.auto_skin_range_value.value()
		auto_skin_helpers.skin_edge_loop_joints('BodyEyes', upper_edge, loop_span)


	@undo
	def lips_up(self, mult=1):
		cmds.setAttr('Vis_Ctrl.lipsMidCtrls', 1)
		ctrls = ['Lips_Up_Main_Ctrl','R_Lips_Up_Ctrl','R_Mid_02Lips_Up_Ctrl','R_Mid_01Lips_Up_Ctrl','_MidLips_Up_Ctrl','L_Mid_01Lips_Up_Ctrl', 'L_Mid_02Lips_Up_Ctrl', 'L_Lips_Up_Ctrl']
		for ctrl in ctrls:
			shapes = cmds.listRelatives(ctrl, s=True)
			if shapes:
				cmds.select('{}.cv[*]'.format(shapes[0]))
				cmds.move(0,0.15*mult,0, r=True)
		cmds.select(cl=True)

	@undo
	def lips_down(self, mult=1):
		cmds.setAttr('Vis_Ctrl.lipsMidCtrls', 1)
		ctrls = ['Lips_Dw_Main_Ctrl','R_Lips_Dw_Ctrl','R_Mid_02Lips_Dw_Ctrl','R_Mid_01Lips_Dw_Ctrl','_MidLips_Dw_Ctrl','L_Mid_01Lips_Dw_Ctrl', 'L_Mid_02Lips_Dw_Ctrl', 'L_Lips_Dw_Ctrl']
		for ctrl in ctrls:
			shapes = cmds.listRelatives(ctrl, s=True)
			if shapes:
				cmds.select('{}.cv[*]'.format(shapes[0]))
				cmds.move(0,-0.15*mult,0, r=True)
		cmds.select(cl=True)

	@undo
	def eyes_down(self, mult=1):
		if cmds.attributeQuery('eyeMidCtrls', node='Vis_Ctrl', exists=True):
			cmds.setAttr('Vis_Ctrl.eyeMidCtrls', 1)
		ctrls = ['L_Eyelids_DwStart_Ctrl','L_Eyelids_DwStartMid_Ctrl','L_Eyelids_DwMid_Ctrl','L_Eyelids_DwEndMid_Ctrl','L_Eyelids_DwEnd_Ctrl']
		for ctrl in ctrls:
			shapes = cmds.listRelatives(ctrl, s=True)
			if shapes:
				cmds.select('{}.cv[*]'.format(shapes[0]))
				cmds.move(0,-0.15*mult,0, r=True)
		cmds.select(cl=True)

	@undo
	def eyes_up(self, mult=1):
		if cmds.attributeQuery('eyeMidCtrls', node='Vis_Ctrl', exists=True):
			cmds.setAttr('Vis_Ctrl.eyeMidCtrls', 1)
		ctrls = ['L_Eyelids_UpStart_Ctrl','L_Eyelids_UpStartMid_Ctrl','L_Eyelids_UpMid_Ctrl','L_Eyelids_UpEndMid_Ctrl','L_Eyelids_UpEnd_Ctrl']
		for ctrl in ctrls:
			shapes = cmds.listRelatives(ctrl, s=True)
			if shapes:
				cmds.select('{}.cv[*]'.format(shapes[0]))
				cmds.move(0,0.15*mult,0, r=True)
		cmds.select(cl=True)

	@undo
	def slider_movement(self, value):
		mouth_geos = ["BodyMouthUp", "BodyMouthDown", "BodyMouthWide", "BodyMouthNarrow", "BodyLips"]

		for geo in mouth_geos:
			cmds.setAttr("{}_JawTester_Bsp.{}_JawTester".format(geo, geo), value/45)

	def reload_jaw_tester(self):

		try:
			self.delete_jaw_tester()
		except:
			pass

		cmds.setAttr("Jaw_Ctrl.rotateX", 45)

		mouth_geos = ["BodyMouthUp", "BodyMouthDown", "BodyMouthWide", "BodyMouthNarrow", "BodyLips"]

		for mouth_geo in mouth_geos:
			open_jaw_geo = cmds.duplicate("BodyJaw", name="{}_JawTester".format(mouth_geo))
			new_bsp = cmds.blendShape(open_jaw_geo, mouth_geo, name="{}_JawTester_Bsp".format(mouth_geo),
									  frontOfChain=True)
			cmds.blendShape(new_bsp, edit=True, w=[(0, 0)])

		cmds.setAttr("Jaw_Ctrl.rotateX", 0)

	def delete_jaw_tester(self):
		cmds.delete(cmds.ls("*JawTester*", type="blendShape"))
		cmds.delete(cmds.ls("*JawTester*"))


	#-------------------------------------------------
	#-------------------------------------------------
	#----------------Prop Tab-------------------------
	#-------------------------------------------------
	#-------------------------------------------------
	@undo
	def open_tools_ui(self):
		from Mutant_Tools.UI.RigTools import load_RigTools
		reload(load_RigTools)
		cRigToolsUI = load_RigTools.RigTools_UI()
		cRigToolsUI.show()

	#-------------------------------------------------
	#-------------------------------------------------
	#----------------Animals Tab----------------------
	#-------------------------------------------------
	#-------------------------------------------------
	@undo
	def fix_quad_foot(self):
		import Mutant_Tools.Utils.Wrap
		from Mutant_Tools.Utils.Wrap import wrap_utils
		reload(wrap_utils)
		cWrap = wrap_utils.Wrap3D()

		cWrap.fix_foot_quadruped_orientation(leg='Fr')
		cWrap.fix_foot_quadruped_orientation(leg='Bk')

	#-------------------------------------------------
	#-------------------------------------------------
	#----------------Clothes Tab-------------------------
	#-------------------------------------------------
	#-------------------------------------------------

	@undo
	def create_skirt_mirror_offsets(self):
		from Mutant_Tools.UI.Helpers.helpers_utils import skirt_helpers
		reload(skirt_helpers)
		skirt_helpers.create_mirror_skirt_groups(block_prefix=self.ui.skirt_name.text())

	@undo
	def delete_skirt_mirror_offsets(self):
		from Mutant_Tools.UI.Helpers.helpers_utils import skirt_helpers
		reload(skirt_helpers)
		skirt_helpers.delete_mirror_skirt_groups(block_prefix=self.ui.skirt_name.text())

	@undo
	def create_skirt_rigmeshes(self):
		from Mutant_Tools.UI.Helpers.helpers_utils import skirt_helpers
		reload(skirt_helpers)
		skirt_helpers.create_skirt_rigmeshes(prefix=self.ui.skirt_name.text(), dup_levels= self.ui.dup_number.value(), 
		skirt_bind_geos=[], open=self.ui.open_check.isChecked())

	@undo
	def create_skirt_vis_toggle(self):
		from Mutant_Tools.UI.Helpers.helpers_utils import skirt_helpers
		reload(skirt_helpers)
		skirt_helpers.add_skirt_vis_toggle(block_prefix=self.ui.skirt_name.text(), 
		attribute_location=self.ui.attribute_parent_box.text())

	# -------------------------------------------------
	# -------------------------------------------------
	# ----------------Crowds Tab-------------------------
	# -------------------------------------------------
	# -------------------------------------------------

	def auto_connect_all_skin_buttons(self):
		buttons_connection_plan = {
			'head': ['Head_Skl'],
			'left_eye': ['LeftEye_Skl'],
			'right_eye': ['RightEye_Skl'],
			'neck_head': ['Neck_Skl', 'Neck1_Skl', 'Head_Skl'],
			'spine': ['Hips_Skl', 'Spine_Skl', 'Spine1_Skl', 'Spine2_Skl', 'SpineHolder_Skl'],
			'neck_spine_head': ['Head_Skl', 'Neck_Skl', 'Neck1_Skl', 'Hips_Skl', 'Spine_Skl', 'Spine1_Skl', 'Spine2_Skl', 'SpineHolder_Skl'],
			'spine_clavs': ['Hips_Skl', 'Spine_Skl', 'Spine1_Skl', 'Spine2_Skl', 'SpineHolder_Skl', 'LeftShoulder_Skl', 'RightShoulder_Skl'],
			'neck_spine_head_clavs': ['Head_Skl', 'Neck_Skl', 'Neck1_Skl', 'Hips_Skl', 'Spine_Skl', 'Spine1_Skl', 'Spine2_Skl', 'SpineHolder_Skl','LeftShoulder_Skl', 'RightShoulder_Skl'],
			'left_arm': ['LeftArm_Skl', 'LeftArm_Roll_Skl', 'LeftForeArm_Skl', 'LeftForeArm_Roll_Skl', 'LeftArm_Roll_*_Skl', 'LeftForeArm_Roll_*_Skl'],
			'left_hand': ['LeftHand_Skl', 'LeftHandThumb*_Skl', 'LeftHandIndex*_Skl', 'LeftHandMiddle*_Skl', 'LeftHandRing*_Skl', 'LeftHandPinky*_Skl'],
			'left_arm_hand': ['LeftForeArm_Roll_*_Skl', 'LeftArm_Roll_*_Skl', 'LeftArm_Skl', 'LeftArm_Roll_Skl', 'LeftForeArm_Skl', 'LeftForeArm_Roll_Skl', 'LeftHand_Skl', 'LeftHandThumb*_Skl', 'LeftHandIndex*_Skl', 'LeftHandMiddle*_Skl', 'LeftHandRing*_Skl', 'LeftHandPinky*_Skl'],
			'rigth_arm': ['RightArm_Skl', 'RightArm_Roll_Skl', 'RightForeArm_Skl', 'RightForeArm_Roll_Skl', 'RightArm_Roll_*_Skl'],
			'right_hand': ['RightHand_Skl', 'RightHandThumb*_Skl', 'RightHandIndex*_Skl', 'RightHandMiddle*_Skl', 'RightHandRing*_Skl', 'RightHandPinky*_Skl', 'RightForeArm_Roll_*_Skl'],
			'right_arm_hand': ['RightArm_Roll_*_Skl', 'RightForeArm_Roll_*_Skl', 'RightArm_Skl', 'RightArm_Roll_Skl', 'RightForeArm_Skl', 'RightForeArm_Roll_Skl', 'RightHand_Skl', 'RightHandThumb*_Skl', 'RightHandIndex*_Skl', 'RightHandMiddle*_Skl', 'RightHandRing*_Skl', 'RightHandPinky*_Skl'],

			'left_leg': ['LeftUpLeg_Skl', 'LeftLeg_Skl', 'LeftUpLeg_Roll_*_Skl', 'LeftLeg_Roll_*_Skl'],
			'left_foot': ['LeftFoot_Skl', 'LeftToeBase_Skl'],
			'left_leg_foot': ['LeftUpLeg_Skl', 'LeftLeg_Skl', 'LeftFoot_Skl', 'LeftToeBase_Skl', 'LeftUpLeg_Roll_*_Skl', 'LeftLeg_Roll_*_Skl'],

			'right_leg': ['RightUpLeg_Skl', 'RightLeg_Skl', 'RightUpLeg_Roll_*_Skl', 'RightLeg_Roll_*_Skl'],
			'right_foot': ['RightFoot_Skl', 'RightToeBase_Skl'],
			'right_leg_foot': ['RightUpLeg_Skl', 'RightLeg_Skl', 'RightFoot_Skl', 'RightToeBase_Skl', 'RightUpLeg_Roll_*_Skl', 'RightLeg_Roll_*_Skl']
		}

		for b in buttons_connection_plan:
			button = self.findChild(QtWidgets.QPushButton, b)
			button.clicked.connect(partial (self.skin_this_to_selected, buttons_connection_plan[b]))

	def skin_this_to_selected(self, joints):
		geos = cmds.ls(sl=True)
		print(joints)

		if not geos:
			return
		for geo in geos:
			skin_joints = []
			for jnt in joints:
				if cmds.objExists(jnt):
					skin_joints.append(jnt)
			skin = cmds.skinCluster(geo, skin_joints, tsb=True)[0]


	def copy_selected_skin(self):

		mel.eval('copySkinWeights  -noMirror -surfaceAssociation closestComponent -influenceAssociation closestBone -influenceAssociation closestBone;')
		print(cmds.ls(sl=True))
	def copy_ns_skin(self):

		sel = cmds.ls(sl=True)
		if not sel:
			return False

		ns = self.get_namespace()

		for s in sel:
			cmds.select(s, s.replace(ns, ''))
			self.copy_selected_skin()
			print(s, s.replace(ns, ''))

		print('Skin copied')
		cmds.select(cl=True)

	def get_namespace(self):
		sel = cmds.ls(sl=True)
		if not sel:
			return str()

		if not ':' in sel[0]:
			return str()

		ns = sel[0].split(':')[0]
		return ns + ':'

	#-------------------------------------------------
	#-------------------------------------------------
	#----------------Other Tab-------------------------
	#-------------------------------------------------
	#-------------------------------------------------
	@undo
	def reload_udims(self):
		from maya import cmds, mel
		mel.eval("""
		ActivateViewport20;
		{  global string $gViewport2;   string $currentPanel = `getPanel -withFocus`;   string $panelType = `getPanel -to $currentPanel`;  if ($panelType ==  "modelPanel") {	  setRendererInModelPanel $gViewport2 $currentPanel;  } else if ($panelType ==  "scriptedPanel") {	 string $cmd = "setRendererInModelPanel $gViewport2 "; 
			scriptedPanelRunTimeCmd( $cmd, $currentPanel ); 
		  }};
		DisplayShadedAndTextured;
		generateAllUvTilePreviews;
		select -cl  ;
		"""
				 )

	@undo
	def label_joints(self):
		import Mutant_Tools
		from Mutant_Tools.Utils.Misc import label_joints
		reload(label_joints)

		label_joints.mass_label_joints()

	def proxy_maker(self):
		try:
			import importlib;
			from importlib import reload
		except:
			import imp;
			from imp import reload

		import Mutant_Tools
		from Mutant_Tools.UI.ProxyMaker import load_proxy_maker
		reload(load_proxy_maker)

		try:
			cProxyMakerUI.close()
		except:
			pass
		cProxyMakerUI = load_proxy_maker.ProxyMakerUI()
		cProxyMakerUI.show()

	def create_MouthIn(self):
		from Mutant_Tools.UI.Helpers.helpers_utils import mouth_helpers
		reload(mouth_helpers)
		mouth_helpers.create_MouthIn()

	def create_Mouth_RollPull(self):
		from Mutant_Tools.UI.Helpers.helpers_utils import mouth_helpers
		reload(mouth_helpers)
		mouth_helpers.create_Mouth_RollPull()

	def load_resets(self):

		try:
			import operator

			resets = mh.read_json(path='/job/anythinggoes/share/rigging/team/Esteban/', json_file='reset_profile.json')
			#print(resets)
			self.ui.resets_amount.setText(str(resets['reset_times']))

			#Create tool tip
			tooltip = 'Last Reset by: {} \n'.format(resets['last_user'])
			tooltip = tooltip+'\nLeaderboard:\n'
			leaderboard = resets['leaderboard']
			my_dict = leaderboard
			sorted_dict = sorted(my_dict.items(), key=operator.itemgetter(1))
			print(sorted_dict)

			for user, amount in reversed(sorted_dict):
				tooltip = tooltip + '{} : {}\n'.format(user, amount)
			tooltip = tooltip[:-1]
			pprint.pprint(tooltip)
			self.ui.reset_profile.setToolTip(tooltip)
		except Exception as e:
			print(e)
			pass

	def add_to_reset(self):
		try:
			from star.entities import User
			current_user = User.find_current_login()

			resets = mh.read_json(path='/job/anythinggoes/share/rigging/team/Esteban', json_file='reset_profile.json')
			resets['reset_times'] = resets['reset_times']+1
			resets['last_user'] = current_user
			if current_user in resets['leaderboard']:
				resets['leaderboard'][current_user] = resets['leaderboard'][current_user]+1
			else:
				resets['leaderboard'][current_user] = 1
			mh.write_json(path='/job/anythinggoes/share/rigging/team/Esteban/', json_file='reset_profile.json', data=resets)
			self.load_resets()
			pprint.pprint(resets)
		except Exception as e:
			print(e)
			pass

	def fari_deformersWeightsEditor(self):
		from Mutant_Tools.UI.Helpers.helpers_utils import fari_deformersWeightsEditor
		dwe_win = fari_deformersWeightsEditor.DeformersWeightsEditor.showUI()

	def dont_press(self):
		self.ui.setWindowOpacity(0.2)
		self.ui.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.setWindowOpacity(0.1)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

	def switch_ikfk(self):
		from Mutant_Tools.Utils.Animation import ikfk_match
		reload(ikfk_match)
		ikfk_match.ikfk_match_callback()

	# CLOSE EVENTS _________________________________
	def closeEvent(self, event):
		''


# -------------------------------------------------------------------

if __name__ == "__main__":

	try:
		cHelperUI.close()  # pylint: disable=E0601
		cHelperUI.deleteLater()
	except:
		pass
	cHelperUI = HelperUI()
	cHelperUI.show()

# -------------------------------------------------------------------

'''
#Notes






'''