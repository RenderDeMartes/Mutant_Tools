from __future__ import absolute_import
'''
version: 1.0.0
date: 21/04/2020

#----------------

how to:

try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import Mutant_Tools
import Mutant_Tools.Utils.Wrap
from Mutant_Tools.Utils.Wrap import wrap_utils
reload(wrap_utils)
cWrap = wrap_utils.Wrap3D()

cmds.select('transf0')
sel=cmds.ls(sl=True)[0]
cWrap.place_mutant_on_wrap_geo(geo=sel)
cWrap.fix_all_body_orientations(hand_pose='A')
cWrap.load_mutant_wrap_skinning(geo=sel, skin='WrapBaseMesh')

#----------------
dependencies:

Wrap3D
maya cmds
maya mel
pymel


#----------------
licence: https://www.eulatemplate.com/live.php?token=FGISW7ApRfgywum6murbBmLcusKONzkv
author:  Esteban Rodriguez <info@mutanttools.com>

'''

import os
import json
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

from pathlib import Path

from maya import cmds as cmds, mel
from maya import OpenMaya as om

import Mutant_Tools
from Mutant_Tools.Utils.Helpers import helpers
reload(Mutant_Tools.Utils.Helpers.helpers)
mh = helpers.Helpers()

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()
nc, curve_data, setup = mt.import_configs()

PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-2]
FOLDER = ''
for f in PATH_PARTS:
	FOLDER = os.path.join(FOLDER, f)

from Mutant_Tools.Utils.Wrap.Skeletor import Skeletor
reload(Skeletor)
cSkeletor = Skeletor.Skeletor()


from Mutant_Tools.Utils.IO import SkinUtils
reload(Mutant_Tools.Utils.IO.SkinUtils)
cSkin = SkinUtils.Skinning()

#------------------------------------------------------

class Wrap3D(object):

    def __init__(self):

        #Base Meshes
        self.wrap_body_geo = os.path.join(FOLDER, 'Utils', 'Wrap', 'BaseMesh', 'WrapBaseMesh', 'Alembic', 'Body.abc')
        self.wrap_face_geo = os.path.join(FOLDER, 'Utils', 'Wrap', 'BaseMesh', 'WrapBaseMesh', 'Alembic', 'Face.abc')

        #Skeletor
        cSkeletor.dirpath = os.path.join(FOLDER, 'Utils', 'Wrap', 'BaseMesh', 'WrapBaseMesh', 'Skeletor')
        self.wrap_body_node_array = cSkeletor.load_data(mesh='WrapBaseMesh', dirpath=cSkeletor.dirpath)
        self.node_array = self.wrap_body_node_array

        #Skinning
        self.wrap_skin_file = os.path.join(FOLDER, 'Utils', 'Wrap', 'Skins', 'WrapBaseMesh.json')
        self.skin_file = self.wrap_skin_file

        self.block_order = self.get_order_of_blocks()

    #-----------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------

    def create_new_scene(self):
        cmds.file(new=True, f=True)

    #-----------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------

    def import_wrap_body(self, new_scene=False):
        if new_scene:
            self.create_new_scene()
        cmds.file(self.wrap_body_geo, i=True, type="Alembic")

    def import_wrap_face(self, new_scene=False):
        if new_scene:
            self.create_new_scene()
        cmds.file(self.wrap_face_geo, i=True, type="Alembic")

    def place_mutant_on_wrap_geo(self, geo=None, base_mesh='WrapBaseMesh', topology=None):
        print(geo, topology)
        if not geo:
            geo = cmds.ls(sl=True)[0]
        if topology:
            cSkeletor.dirpath = os.path.join(FOLDER, 'Utils','Wrap','BaseMesh', base_mesh, 'Skeletor')
            node_array = cSkeletor.load_data(mesh=topology, dirpath=cSkeletor.dirpath)
        else:
            node_array = self.node_array
        cSkeletor.place_all(mesh=geo, node_Array=node_array)

    #-----------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------

    def create_aim_locators(self, guide):

        up_locator = cmds.spaceLocator(n=guide+'_Temp_Up'+nc['locator'])[0]
        side_locator = cmds.spaceLocator(n=guide+'_Temp_Side'+nc['locator'])[0]
        front_locator = cmds.spaceLocator(n=guide+'_Temp_Front'+nc['locator'])[0]

        mt.match(up_locator, guide, r=False)
        mt.match(side_locator, guide, r=False)
        mt.match(front_locator, guide, r=False)

        cmds.move(0,10,0, up_locator, r=True)
        cmds.move(10,0,0, side_locator, r=True)
        cmds.move(0,0,10, front_locator, r=True)

        return up_locator, side_locator, front_locator

    def fix_guides_orientation(self, guides=[], aim_axis=(1,0,0), up_axis=(0,1,0) , target_locator='up_locator', fix_last=True, node_array=None):

        self.block_order = self.get_order_of_blocks()

        # Skeletor.rotate_planar(array)
        if not node_array:
            node_array = self.node_array
        if not node_array:
            return False
        hierarchy_array = Skeletor.unparent_hierarchy(node_array)

        for num, guide in enumerate(guides):

            #Decide the up vector
            up_locator, side_locator, front_locator = self.create_aim_locators(guide)

            if target_locator == 'Up':
                aim_loc = up_locator
            elif target_locator == 'Front':
                aim_loc = front_locator
            elif target_locator == 'Side':
                aim_loc = side_locator
            else:
                aim_loc = up_locator

            #Aim constriant to lower guide in guides array
            if guide == guides[-1]:
                #Do stuff on last guide
                if fix_last:
                    constraint = cmds.orientConstraint(guides[num-1], guide)
                    cmds.delete(constraint)
            else:
                #aim to next guide
                print(guide, guides[num+1])
                constraint = cmds.aimConstraint(guides[num+1], guide, aimVector=aim_axis, upVector=up_axis,
                                   worldUpType="object", worldUpObject=aim_loc)
                cmds.delete(constraint)

            #Delete stuff
            cmds.delete(up_locator, side_locator, front_locator)

        #Reaprent the hierarchy
        Skeletor.parent_hierarchy(hierarchy_array)

        self.reorder_block_guides(self.block_order)

    #-----------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------

    def fix_limb_arms_orientation(self):
        #Skeletor.rotate_planar(["L_Shoulder_Guide", "L_Elbow_Guide", "L_Wrist_Guide"])

        self.fix_guides_orientation(guides=["L_Shoulder_Guide", "L_Elbow_Guide", "L_Wrist_Guide"],
                                    aim_axis = (1, 0, 0), up_axis = (0, 0, -1), target_locator = 'Up',
                                    fix_last=True)
        ref = self.create_ref_planes('L_Shoulder_Guide', 'L_Wrist_Guide')
        x_value = cmds.getAttr('L_Elbow_Guide.tx')

        hierarchy_array = Skeletor.unparent_hierarchy(self.node_array)
        cmds.delete(cmds.pointConstraint('L_Shoulder_Guide','L_Wrist_Guide','L_Elbow_Guide'))
        Skeletor.parent_hierarchy(hierarchy_array)

        self.fix_guides_orientation(guides=["L_Shoulder_Guide", "L_Elbow_Guide", "L_Wrist_Guide"],
                                    aim_axis = (1, 0, 0), up_axis = (0, 0, -1), target_locator = 'Up',
                                    fix_last=True)

        end_matrix = cmds.xform('L_Wrist_Guide', q=True, m=True)

        cmds.setAttr('L_Elbow_Guide.tx', x_value)
        cmds.setAttr('L_Elbow_Guide.ty', -0.5)

        cmds.xform('L_Wrist_Guide', m=end_matrix)


    def fix_clav_orientation(self):
        self.fix_guides_orientation(guides=["L_Clavicle_Guide", "L_Shoulder_Guide"],
                                    aim_axis = (1, 0, 0), up_axis = (0, 0, -1), target_locator = 'Up',
                                    fix_last=False)
        cmds.delete(cmds.pointConstraint("L_Shoulder_Guide", 'L_ClavicleEnd_Guide', mo=False))

    def zero_specific_finger(self, finger):
        for num in range(1,5):
            finger_guide = 'L_Hand_{}_0{}_Guide'.format(finger, num)
            if cmds.objExists(finger_guide):
                print(finger_guide)
                cmds.setAttr('{}.jointOrientY'.format(finger_guide), 0)
                cmds.setAttr('{}.jointOrientZ'.format(finger_guide), 0)
                if num != 1:
                    cmds.setAttr('{}.jointOrientX'.format(finger_guide), 0)
                    cmds.setAttr('{}.rotateX'.format(finger_guide), 0)
                cmds.setAttr('{}.rotateY'.format(finger_guide), 0)
                cmds.setAttr('{}.rotateZ'.format(finger_guide), 0)
                
    def fix_fingers_orientations(self, pose='A'):

        fingers_guides = ['L_Hand_Pinky_NUM_Guide', 'L_Hand_Ring_NUM_Guide', 'L_Hand_Middle_NUM_Guide',
                          'L_Hand_Index_NUM_Guide', 'L_Hand_Thumb_NUM_Guide']

        if cmds.objExists('L_Hand_Middle_01_Guide'):
            self.fix_guides_orientation(guides=["L_Hand_Palm_Guide", "L_Hand_Middle_01_Guide"],
                                    aim_axis = (1, 0, 0), up_axis = (0, 1, 0), target_locator = 'Up',
                                    fix_last=False)

        for finger in fingers_guides:
            fingers = []
            for num in range(5):
                fingers.append(finger.replace('NUM', '0{}'.format(num)))
            if 'Thumb' in finger:
                fingers.pop(-1)
                if pose == 'A':
                    self.fix_guides_orientation(guides=fingers,
                                                aim_axis=(1, 0, 0), up_axis=(0, 1, 0), target_locator='Front',
                                                fix_last=True)
                else:
                    #Skeletor.rotate_planar(fingers)
                    self.fix_guides_orientation(guides=fingers,
                                                aim_axis=(1, 0, 0), up_axis=(0, 1, 0), target_locator='Up',
                                                fix_last=True)

            else:
                if pose == 'A':
                    #Skeletor.rotate_planar(fingers[1:-1])
                    self.fix_guides_orientation(guides=fingers,
                                                aim_axis=(1, 0, 0), up_axis=(0, 1, 0), target_locator='Side',
                                                fix_last=True)
                else:
                    #Skeletor.rotate_planar(fingers[1:-1])
                    self.fix_guides_orientation(guides=fingers,
                                                aim_axis=(1, 0, 0), up_axis=(0, 1, 0), target_locator='Up',
                                                fix_last=True)

            #Fix Cups
            #L_Hand_InnerCup_Guide, L_Hand_OutterCup_Guide
            if pose == 'A':
                self.fix_guides_orientation(guides=['L_Hand_InnerCup_Guide', 'L_Hand_Thumb_00_Guide'],
                                            aim_axis=(1, 0, 0), up_axis=(0, 1, 0), target_locator='Front',
                                            fix_last=False)
                self.fix_guides_orientation(guides=['L_Hand_OutterCup_Guide', 'L_Hand_Pinky_00_Guide'],
                                            aim_axis=(1, 0, 0), up_axis=(0, 1, 0), target_locator='Side',
                                            fix_last=False)
            else:
                self.fix_guides_orientation(guides=fingers,
                                            aim_axis=(1, 0, 0), up_axis=(0, 1, 0), target_locator='Up',
                                            fix_last=False)
                self.fix_guides_orientation(guides=fingers,
                                            aim_axis=(1, 0, 0), up_axis=(0, 1, 0), target_locator='Up',
                                            fix_last=False)


    def fix_pelvis_orientation(self):
        cmds.rotate(0,0,0, "L_Pelvis_Guide")
        cmds.delete(cmds.pointConstraint("L_Hip_Guide", 'L_PelvisEnd_Guide',mo=False))

    def fix_limb_legs_orientation(self):
        #Skeletor.rotate_planar(["L_Hip_Guide", "L_Knee_Guide", "L_Ankle_Guide"])

        self.fix_guides_orientation(guides=["L_Hip_Guide", "L_Knee_Guide", "L_Ankle_Guide"],
                                    aim_axis=(1, 0, 0), up_axis=(0, -1, 0), target_locator='Front',
                                    fix_last=True)
        ref = self.create_ref_planes('L_Hip_Guide', 'L_Ankle_Guide')

        x_value = cmds.getAttr('L_Knee_Guide.tx')

        hierarchy_array = Skeletor.unparent_hierarchy(self.node_array)
        cmds.delete(cmds.pointConstraint('L_Hip_Guide','L_Ankle_Guide','L_Knee_Guide'))
        Skeletor.parent_hierarchy(hierarchy_array)

        self.fix_guides_orientation(guides=["L_Hip_Guide", "L_Knee_Guide", "L_Ankle_Guide"],
                                    aim_axis = (1, 0, 0), up_axis = (0, 0, -1), target_locator = 'Up',
                                    fix_last=True)

        end_matrix = cmds.xform('L_Ankle_Guide', q=True, m=True, ws=True)

        cmds.setAttr('L_Knee_Guide.tx', x_value)
        cmds.setAttr('L_Knee_Guide.tz', 0.5)

        cmds.xform('L_Ankle_Guide', m=end_matrix, ws=True)

    def fix_spine_orientation(self):
        #Skeletor.rotate_planar(["Spine_Root_Guide", "Spine_Base_Guide", "Spine_Belly_Guide","Spine_Chest_Guide","Spine_End_Guide"])
        self.fix_guides_orientation(guides=["Spine_Root_Guide", "Spine_Base_Guide", "Spine_Belly_Guide","Spine_Chest_Guide","Spine_End_Guide"],
                                    aim_axis=(1, 0, 0), up_axis=(0, 1, 0), target_locator='Front',
                                    fix_last=True)
        cmds.select("Spine_Root_Guide", "Spine_Base_Guide", "Spine_Belly_Guide","Spine_Chest_Guide","Spine_End_Guide")
        self.zero(axis='X')

    def fix_head_orientation(self):
        self.fix_guides_orientation(
            guides=["Neck_Guide", "Head_Guide", "HeadEnd_Guide"],
            aim_axis=(1, 0, 0), up_axis=(0, 1, 0), target_locator='Front',
            fix_last=True)
        cmds.select("Neck_Guide", "Head_Guide", "HeadEnd_Guide")
        self.zero(axis='X')

    def fix_foot_orientation(self):

        hierarchy_array = Skeletor.unparent_hierarchy(self.node_array)
        cmds.delete(cmds.pointConstraint('L_Ankle_Guide', 'L_Foot_Ankle_Guide', mo=False))
        Skeletor.parent_hierarchy(hierarchy_array)

        self.fix_guides_orientation(
            guides=["L_Foot_Ankle_Guide", "L_Foot_Ball_Guide"],
            aim_axis=(0, 1, 0), up_axis=(-1, 0, 0), target_locator='Up',
            fix_last=False)
        self.fix_guides_orientation(
            guides=["L_Foot_Ball_Guide", "L_Foot_Toes_Guide"],
            aim_axis=(1, 0, 0), up_axis=(0, 1, 0), target_locator='Up',
            fix_last=False)
        self.fix_guides_orientation(
            guides=["L_Foot_Heel_Guide", "L_Foot_Toes_Guide"],
            aim_axis=(0, 0, 1), up_axis=(0, 1, 0), target_locator='Up',
            fix_last=False)
        self.fix_guides_orientation(
            guides=["L_Foot_HeelMid_Guide", "L_Foot_Toes_Guide"],
            aim_axis=(0, 0, 1), up_axis=(0, 1, 0), target_locator='Up',
            fix_last=False)
        self.fix_guides_orientation(
            guides=["L_Foot_Out_Guide", "L_Foot_BallFloor_Guide"],
            aim_axis=(-1, 0, 0), up_axis=(0, 1, 0), target_locator='Up',
            fix_last=False)
        self.fix_guides_orientation(
            guides=["L_Foot_In_Guide", "L_Foot_BallFloor_Guide"],
            aim_axis=(1, 0, 0), up_axis=(0, 1, 0), target_locator='Up',
            fix_last=False)
        self.fix_guides_orientation(
            guides=["L_Foot_BallFloor_Guide", "L_Foot_Toes_Guide"],
            aim_axis=(0, 1, 0), up_axis=(0, 0, 1), target_locator='Up',
            fix_last=False)

        cmds.delete(cmds.orientConstraint('L_Foot_HeelMid_Guide','L_Foot_Toes_Guide', mo=False))

        cmds.select("L_Foot_Heel_Guide", "L_Foot_HeelMid_Guide", "L_Foot_BallFloor_Guide",
                    "L_Foot_In_Guide","L_Foot_Out_Guide","L_Foot_Toes_Guide")
        self.zero(axis='Y')

    def fix_cog_orientation(self):
        cog = 'COG_Loc'
        cmds.delete(cmds.pointConstraint('Spine_Base_Guide', 'Spine_Root_Guide', cog))

    def fix_all_body_orientations(self, hand_pose='A'):
        self.fix_limb_arms_orientation()
        self.fix_clav_orientation()
        self.fix_fingers_orientations(hand_pose)
        self.fix_pelvis_orientation()
        self.fix_limb_legs_orientation()
        self.fix_spine_orientation()
        self.fix_head_orientation()
        self.fix_foot_orientation()
        self.fix_cog_orientation()

    def zero(self, axis=''):


        sel = cmds.ls(sl=True)
        hierarchy_array = Skeletor.unparent_hierarchy(self.node_array)

        for s in sel:
            cmds.select(s)
            if axis == 'X':
                cmds.move(0, cmds.getAttr('{}.ty'.format(s)), cmds.getAttr('{}.tz'.format(s)))
            elif axis == 'Y':
                cmds.move(cmds.getAttr('{}.tx'.format(s)), 0, cmds.getAttr('{}.tz'.format(s)))
            else:
                cmds.move(cmds.getAttr('{}.tx'.format(s)), cmds.getAttr('{}.ty'.format(s)), 0)

        Skeletor.parent_hierarchy(hierarchy_array)

    def load_mutant_wrap_skinning(self, geo=None, skin='WrapBaseMesh', rename=False):
        if not geo:
            cmds.error('We need a geo to assign skin to')
        if rename:
            if cmds.objExists(skin):
                cmds.rename(skin, skin+'TempName')
            geo_needed_name = cmds.rename(geo, skin)
        else:
            geo_needed_name=geo

        try:
            print('loading from', self.skin_file)
            data = cSkin.load_data(path=self.skin_file)
            cSkin.set_weights(all_data=data, geometry=skin, remove_unused=True)
        except Exception as e:
            if rename:
                cmds.rename(geo_needed_name, geo)
                if cmds.objExists(skin + 'TempName'):
                    cmds.rename(skin + 'TempName', skin)
            cmds.error('Error while loading the skinning: {}'.format(e))

        if rename:
            cmds.rename(geo_needed_name, geo)
            if cmds.objExists(skin+'TempName'):
                cmds.rename(skin+'TempName', skin)

        print(geo, 'Skin')

    #-----------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------

    def create_ref_planes(self, start, end):
        from Mutant_Tools.UI.GuidePlacements import load_guide_placements
        reload(load_guide_placements)
        cGuidePlacements = load_guide_placements.GuidePlacements()

        name = str(start) + '_Ref'
        if cmds.objExists(name):
            cmds.delete(name)
        cGuidePlacements.create_ref_plane(start, end)

        return name

    #-----------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------


    def get_order_of_blocks(self, use_selection=False):
        if use_selection:
            blocks = cmds.ls(sl=True)
        else:
            blocks = cmds.ls('*_Block')

        if not blocks:
            return False

        blocks_order = {}

        for block in blocks:
            outliner_order = {}
            guides = cmds.listRelatives(block, c=True, type='transform')
            outliner_order[block] = guides
            if guides:
                for guide in guides:
                    child_guides = cmds.listRelatives(guide, c=True, type='transform')
                    outliner_order[guide] = child_guides
                    if child_guides:
                        for child_guide in child_guides:
                            grand_child_guides = cmds.listRelatives(child_guide, c=True, type='transform')
                            outliner_order[child_guide] = grand_child_guides
                            if grand_child_guides:
                                for ggc in grand_child_guides:
                                    ggc_guides = cmds.listRelatives(ggc, c=True, type='transform')
                                    outliner_order[ggc] = ggc_guides
            blocks_order[block] = outliner_order

        return blocks_order

    def reorder_block_guides(self, block_order):
        blocks = cmds.ls('*_Block')
        if not blocks:
            return False

        for block in blocks:
            if block in block_order:
                order_data = block_order[block]
                if order_data:
                    for child_data in order_data:
                        father = child_data
                        childs = order_data[child_data]
                        if childs:
                            cmds.parent(childs, w=True)
                            cmds.parent(childs, father)

    #-----------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------


    def fix_all_face_orientations(self, eyeball=None,face_geo=None):
        self.fix_skull_orientation()
        self.fix_eyelids_block(eyeball=eyeball)
        self.fix_oblicular_orientation()
        self.fix_lips_orientation()
        self.fix_brows_orientation()
        self.fix_cheecks_orientation()
        self.fix_jaw_orientation()
        self.fix_commisures_orientation()
        self.fix_nose_orientation()
        self.assign_eyelids_edges(mesh=face_geo)
        self.assign_lips_edges(mesh=face_geo)
        self.set_locals_face_geo(face_geo=face_geo)

        self.wrap_geo_to_brows_guide(mesh=face_geo)
        self.wrap_geo_to_cheecks_guide(mesh=face_geo)
        self.wrap_geo_to_oblicularis_guide(mesh=face_geo)
        self.wrap_geo_to_commisures_guides(mesh=face_geo)

    def fix_skull_orientation(self):

        for guide in ['Skull_Lwr_Guide','Skull_Upr_Guide']:
            cmds.setAttr('{}.rotateX'.format(guide), 0)
            cmds.setAttr('{}.rotateY'.format(guide), 0)
            cmds.setAttr('{}.rotateZ'.format(guide), 0)

    def fix_eyelids_block(self, eyeball=None):

        cmds.setAttr('{}.rotateX'.format('Eye_Pivot'), 0)
        cmds.setAttr('{}.rotateY'.format('Eye_Pivot'), 0)
        cmds.setAttr('{}.rotateZ'.format('Eye_Pivot'), 0)

        if not eyeball:
            return

        try:
            temp_cls = cmds.cluster(eyeball)
            cmds.delete(cmds.parentConstraint(temp_cls, 'Eye_Pivot'), temp_cls)
        except:
            pass

    def fix_oblicular_orientation(self):
        if cmds.objExists('L_Orbicularis_Guide'):
            cmds.delete(cmds.parentConstraint('Eye_Pivot', 'L_Orbicularis_Guide'))
            cmds.move(0,0,1, 'L_Orbicularis_Guide', r=True)

    def fix_lips_orientation(self):
        cmds.setAttr('{}.rotateX'.format('Lips_SlideCenter_Guide_Guide'), 0)
        cmds.setAttr('{}.rotateY'.format('Lips_SlideCenter_Guide_Guide'), 0)
        cmds.setAttr('{}.rotateZ'.format('Lips_SlideCenter_Guide_Guide'), 0)

        self.fix_guides_orientation(
            guides=["L_Lips_Orient_Guide_Guide", "Lips_SlideCenter_Guide_Guide"],
            aim_axis=(0, 0, -1), up_axis=(0, 1, 0), target_locator='Up',
            fix_last=False)

    def fix_brows_orientation(self):
        cmds.setAttr('{}.rotateX'.format('L_Brow_Guide'), 0)
        cmds.setAttr('{}.rotateY'.format('L_Brow_Guide'), 0)
        cmds.setAttr('{}.rotateZ'.format('L_Brow_Guide'), 0)

    def fix_cheecks_orientation(self):
        cmds.delete(cmds.parentConstraint('L_Lips_Orient_Guide_Guide', 'L_Cheecks_Border_Guide'))
        cmds.setAttr('{}.rotateX'.format('L_Cheecks_Guide'), 0)
        cmds.setAttr('{}.rotateY'.format('L_Cheecks_Guide'), 0)
        cmds.setAttr('{}.rotateZ'.format('L_Cheecks_Guide'), 0)

        cmds.move(0,0,1, 'L_Cheecks_Border_Guide', r=True)

    def fix_jaw_orientation(self):

        self.block_order = self.get_order_of_blocks()
        hierarchy_array = Skeletor.unparent_hierarchy(self.node_array)

        cmds.setAttr('{}.rotateX'.format('Jaw_Guide'), 0)
        cmds.setAttr('{}.rotateY'.format('Jaw_Guide'), 0)
        cmds.setAttr('{}.rotateZ'.format('Jaw_Guide'), 0)

        cmds.setAttr('{}.rotateX'.format('JawUpperLip_Guide'), 0)
        cmds.setAttr('{}.rotateY'.format('JawUpperLip_Guide'), 0)
        cmds.setAttr('{}.rotateZ'.format('JawUpperLip_Guide'), 0)

        cmds.setAttr('{}.rotateX'.format('JawLowerLip_Guide'), 0)
        cmds.setAttr('{}.rotateY'.format('JawLowerLip_Guide'), 0)
        cmds.setAttr('{}.rotateZ'.format('JawLowerLip_Guide'), 0)

        Skeletor.parent_hierarchy(hierarchy_array)
        self.reorder_block_guides(self.block_order)

    def fix_commisures_orientation(self):
        cmds.delete(cmds.parentConstraint('L_Lips_Orient_Guide_Guide', 'L_Commissures_Wide_Guide'))
        cmds.delete(cmds.parentConstraint('L_Lips_Orient_Guide_Guide', 'L_Commissures_Narrow_Guide'))
        cmds.delete(cmds.parentConstraint('L_Lips_Orient_Guide_Guide', 'L_Commissures_Up_Guide'))
        cmds.delete(cmds.parentConstraint('L_Lips_Orient_Guide_Guide', 'L_Commissures_Down_Guide'))

    def fix_nose_orientation(self):
        self.fix_guides_orientation(
            guides=["L_NoseNostril_Guide", "L_NoseNostrilEnd_Guide"],
            aim_axis=(1, 0, 0), up_axis=(0, 1, 0), target_locator='Up',
            fix_last=True)

        self.fix_guides_orientation(
            guides=["R_NoseNostril_Guide", "R_NoseNostrilEnd_Guide"],
            aim_axis=(-1, 0, 0), up_axis=(0, 1, 0), target_locator='Up',
            fix_last=True)

    #-----------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------

    def assign_eyelids_edges(self, mesh='transf0'):

        lower_edges = ['{}.e[30271]'.format(mesh), '{}.e[30273]'.format(mesh), '{}.e[30275]'.format(mesh),
                       '{}.e[30277]'.format(mesh), '{}.e[30280]'.format(mesh), '{}.e[30282:30283]'.format(mesh),
                       '{}.e[30285]'.format(mesh), '{}.e[30288]'.format(mesh), '{}.e[30290]'.format(mesh),
                       '{}.e[30292]'.format(mesh), '{}.e[30294]'.format(mesh), '{}.e[30296]'.format(mesh),
                       '{}.e[30298]'.format(mesh), '{}.e[30300]'.format(mesh), '{}.e[30302]'.format(mesh),
                       '{}.e[30304]'.format(mesh), '{}.e[30306:30307]'.format(mesh)]

        upper_edges = ['{}.e[30250]'.format(mesh), '{}.e[30254]'.format(mesh), '{}.e[30256]'.format(mesh),
                       '{}.e[30258]'.format(mesh), '{}.e[30260]'.format(mesh), '{}.e[30262]'.format(mesh),
                       '{}.e[30264]'.format(mesh), '{}.e[30266]'.format(mesh), '{}.e[30268]'.format(mesh),
                       '{}.e[30270]'.format(mesh), '{}.e[30309]'.format(mesh), '{}.e[30311]'.format(mesh),
                       '{}.e[30313]'.format(mesh), '{}.e[30315]'.format(mesh), '{}.e[30317]'.format(mesh),
                       '{}.e[30319]'.format(mesh), '{}.e[30321]'.format(mesh), '{}.e[30323]'.format(mesh),
                       '{}.e[30325]'.format(mesh)]

        cmds.setAttr('L_Eyelids_Config.SetLowerEdge', str(lower_edges)[1:-1].replace("'", ''),  type="string")
        cmds.setAttr('L_Eyelids_Config.SetUpperEdge', str(upper_edges)[1:-1].replace("'", ''), type="string")


    def assign_lips_edges(self, mesh='transf0'):

        lower_edges = [ '{}.e[31943]'.format(mesh), '{}.e[31947]'.format(mesh), '{}.e[31950]'.format(mesh),
                        '{}.e[31954]'.format(mesh), '{}.e[31967]'.format(mesh), '{}.e[31972]'.format(mesh),
                        '{}.e[31976]'.format(mesh), '{}.e[32113]'.format(mesh), '{}.e[32131]'.format(mesh),
                        '{}.e[32146]'.format(mesh), '{}.e[37565]'.format(mesh), '{}.e[37569]'.format(mesh),
                        '{}.e[37574]'.format(mesh), '{}.e[37577]'.format(mesh), '{}.e[37590]'.format(mesh),
                        '{}.e[37595]'.format(mesh), '{}.e[37600]'.format(mesh), '{}.e[37736]'.format(mesh),
                        '{}.e[37754]'.format(mesh), '{}.e[37764]'.format(mesh)]

        upper_edges = ['{}.e[2747]'.format(mesh), '{}.e[2751]'.format(mesh), '{}.e[2754]'.format(mesh),
                       '{}.e[2759]'.format(mesh), '{}.e[2762]'.format(mesh), '{}.e[2765]'.format(mesh),
                       '{}.e[2768]'.format(mesh), '{}.e[2783]'.format(mesh), '{}.e[2799]'.format(mesh),
                       '{}.e[2845]'.format(mesh), '{}.e[34495]'.format(mesh), '{}.e[34498]'.format(mesh),
                       '{}.e[34501]'.format(mesh), '{}.e[34505]'.format(mesh), '{}.e[34508]'.format(mesh),
                       '{}.e[34511]'.format(mesh), '{}.e[34515]'.format(mesh), '{}.e[34530]'.format(mesh),
                       '{}.e[34544]'.format(mesh), '{}.e[34589]'.format(mesh)]

        cmds.setAttr('Lips_Config.SetLowerEdge', str(lower_edges)[1:-1].replace("'", ''),  type="string")
        cmds.setAttr('Lips_Config.SetUpperEdge', str(upper_edges)[1:-1].replace("'", ''), type="string")

    def set_locals_face_geo(self, face_geo=''):

        if not face_geo:
            face_geo='transf0'
        if cmds.objExists('SkullLocal_Config'):
            cmds.setAttr('SkullLocal_Config.SetGeo', face_geo, type="string")


    def wrap_geo_to_brows_guide(self, mesh='transf0'):

        top_edges = ['transf0.e[30461]', 'transf0.e[30466]', 'transf0.e[30470]', 'transf0.e[30474]',
                     'transf0.e[30481]', 'transf0.e[30492]', 'transf0.e[30603]', 'transf0.e[30674]',
                     'transf0.e[30694]', 'transf0.e[32218]']
        low_edges = ['transf0.e[29409]', 'transf0.e[29463]', 'transf0.e[29466]', 'transf0.e[29477]',
                     'transf0.e[29482]', 'transf0.e[29489]', 'transf0.e[29820:29821]', 'transf0.e[29827]',
                     'transf0.e[29831]']

        top_edges_mesh = []
        for top_edge in top_edges:
            top_edges_mesh.append(top_edge.replace('transf0', mesh))
        cmds.select(top_edges_mesh)
        top_crv = cmds.polyToCurve(form=0,
                                    degree=3,
                                    conformToSmoothMeshPreview=1,
                                    n='BrowTop_Vtx' + nc['curve'],
                                    ch=False)[0]
        low_edges_mesh = []
        for low_edge in low_edges:
            low_edges_mesh.append(low_edge.replace('transf0', mesh))
        cmds.select(low_edges_mesh)
        btm_curve = cmds.polyToCurve(form=0,
                                        degree=3,
                                        conformToSmoothMeshPreview=1,
                                        n='BrowBtm_Vtx' + nc['curve'],
                                        ch=False)[0]

        top_crv = cmds.rebuildCurve(top_crv, ch=False, rpo=1 , kt=0 , s=5, d=3, kcp=0, kep=1, n='L_Brow_Guide')[0]
        btm_curve = cmds.rebuildCurve(btm_curve, ch=False, rpo=1 , kt=0 , s=5, d=3, kcp=0, kep=1, n='L_Brow_Guide')[0]

        new_surface = mel.eval('loft -ch 1 -u 1 -c 0 -ar 1 -d 3 -ss 1 -rn 0 -po 0 -rsn true "{}" "{}";'.format(top_crv, btm_curve))[0]
        cmds.delete(top_crv, btm_curve, 'L_Brow_Guide')
        new_surface=cmds.rename(new_surface, 'L_Brow_Guide')
        cmds.parent(new_surface, 'L_Brow_Block')

    def wrap_geo_to_cheecks_guide(self, mesh='transf0'):

        first_matrix = cmds.pointPosition('{}.vtx[14414]'.format(mesh))
        second_matrix = cmds.pointPosition('{}.vtx[14288]'.format(mesh))
        third_matrix = cmds.pointPosition('{}.vtx[14283]'.format(mesh))
        fourth_matrix = cmds.pointPosition('{}.vtx[15952]'.format(mesh))
        fifth_matrix = cmds.pointPosition('{}.vtx[15850]'.format(mesh))
        sixth_matrix = cmds.pointPosition('{}.vtx[15840]'.format(mesh))

        cmds.xform('L_Cheecks_Border_Guide.cv[0]', t=first_matrix, ws=True)
        cmds.xform('L_Cheecks_Border_Guide.cv[1]', t=second_matrix, ws=True)
        cmds.xform('L_Cheecks_Border_Guide.cv[2]', t=third_matrix, ws=True)
        cmds.xform('L_Cheecks_Border_Guide.cv[3]', t=fourth_matrix, ws=True)
        cmds.xform('L_Cheecks_Border_Guide.cv[4]', t=fifth_matrix, ws=True)
        cmds.xform('L_Cheecks_Border_Guide.cv[5]', t=sixth_matrix, ws=True)


        #Cheeck bone if exists
        if cmds.objExists('L_Cheecks_Bone_Guide'):
            first_matrix = cmds.pointPosition('{}.vtx[14639]'.format(mesh))
            second_matrix = cmds.pointPosition('{}.vtx[14645]'.format(mesh))
            third_matrix = cmds.pointPosition('{}.vtx[14652]'.format(mesh))
            fourth_matrix = cmds.pointPosition('{}.vtx[14812]'.format(mesh))

            cmds.xform('L_Cheecks_Bone_Guide.cv[0]', t=first_matrix, ws=True)
            cmds.xform('L_Cheecks_Bone_Guide.cv[1]', t=second_matrix, ws=True)
            cmds.xform('L_Cheecks_Bone_Guide.cv[2]', t=third_matrix, ws=True)
            cmds.xform('L_Cheecks_Bone_Guide.cv[3]', t=fourth_matrix, ws=True)

    def wrap_geo_to_oblicularis_guide(self, mesh='transf0'):

        if not cmds.objExists('L_Orbicularis_Guide'):
            return False

        edges = ['{}.e[29334]'.format(mesh), '{}.e[29337]'.format(mesh), '{}.e[29357]'.format(mesh), '{}.e[29360]'.format(mesh),
                 '{}.e[29369]'.format(mesh), '{}.e[29372]'.format(mesh), '{}.e[29375]'.format(mesh), '{}.e[29378]'.format(mesh),
                 '{}.e[29387]'.format(mesh), '{}.e[29391]'.format(mesh), '{}.e[29398]'.format(mesh), '{}.e[29415]'.format(mesh),
                 '{}.e[29454]'.format(mesh), '{}.e[29485]'.format(mesh), '{}.e[29495]'.format(mesh), '{}.e[29499]'.format(mesh),
                 '{}.e[29516]'.format(mesh), '{}.e[29519:29520]'.format(mesh), '{}.e[29523]'.format(mesh), '{}.e[29547]'.format(mesh),
                 '{}.e[29553]'.format(mesh), '{}.e[29558]'.format(mesh), '{}.e[29561]'.format(mesh), '{}.e[29565]'.format(mesh),
                 '{}.e[29592]'.format(mesh), '{}.e[29636]'.format(mesh), '{}.e[29639]'.format(mesh), '{}.e[29643]'.format(mesh),
                 '{}.e[29647]'.format(mesh), '{}.e[29652]'.format(mesh), '{}.e[29660]'.format(mesh), '{}.e[29662]'.format(mesh),
                 '{}.e[29664]'.format(mesh), '{}.e[29716]'.format(mesh), '{}.e[29774]'.format(mesh), '{}.e[29839]'.format(mesh),
                 '{}.e[29851]'.format(mesh)]

        match_mapping ={
            'L_Orbicularis_Guide.cv[3]':'{}.vtx[14884]'.format(mesh),
            'L_Orbicularis_Guide.cv[2]': '{}.vtx[14887]'.format(mesh),
            'L_Orbicularis_Guide.cv[1]': '{}.vtx[14890]'.format(mesh),
            'L_Orbicularis_Guide.cv[0]': '{}.vtx[14876] '.format(mesh),
            'L_Orbicularis_Guide.cv[7]': '{}.vtx[14902]'.format(mesh),
            'L_Orbicularis_Guide.cv[6]': '{}.vtx[14866]'.format(mesh),
            'L_Orbicularis_Guide.cv[5]': '{}.vtx[14870]'.format(mesh),
            'L_Orbicularis_Guide.cv[4]': '{}.vtx[14888]'.format(mesh)
        }

        for cv in match_mapping:
            vtx = match_mapping[cv]
            position = cmds.pointPosition(vtx)
            cmds.xform(cv, t=position, ws=True)

        cmds.ogs(pause=1)
        cmds.ogs(pause=1)


    def wrap_geo_to_commisures_guides(self, mesh='transf0'):
        ''

    #-----------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------

    def fix_foot_quadruped_orientation(self, leg='Fr' ):

        cmds.select('L_{}Foot_Heel_Guide'.format(leg), 'L_{}Foot_HeelMid_Guide'.format(leg),
                    'L_{}Foot_BallFloor_Guide'.format(leg),
                    "L_{}Foot_In_Guide".format(leg),"L_{}Foot_Out_Guide".format(leg),'L_{}Foot_Toes_Guide'.format(leg), 'L_{}Foot_Ball_Guide'.format(leg))
        node_array = cmds.ls(sl=True)
        hierarchy_array = Skeletor.unparent_hierarchy(node_array)
        cmds.delete(cmds.pointConstraint('L_{}Ball_Guide'.format(leg), 'L_{}Foot_Ankle_Guide'.format(leg), mo=False))
        Skeletor.parent_hierarchy(hierarchy_array)

        self.fix_guides_orientation(
            guides=['L_{}Foot_Ankle_Guide'.format(leg), 'L_{}Foot_Ball_Guide'.format(leg)],
            aim_axis=(0, 1, 0), up_axis=(-1, 0, 0), target_locator='Up',
            fix_last=False,
            node_array=node_array)
        self.fix_guides_orientation(
            guides=['L_{}Foot_Ball_Guide'.format(leg), 'L_{}Foot_Toes_Guide'.format(leg)],
            aim_axis=(1, 0, 0), up_axis=(0, 1, 0), target_locator='Up',
            fix_last=False,
            node_array=node_array)
        self.fix_guides_orientation(
            guides=['L_{}Foot_Heel_Guide'.format(leg), 'L_{}Foot_Toes_Guide'.format(leg)],
            aim_axis=(0, 0, 1), up_axis=(0, 1, 0), target_locator='Up',
            fix_last=False,
            node_array=node_array)
        self.fix_guides_orientation(
            guides=['L_{}Foot_HeelMid_Guide'.format(leg), 'L_{}Foot_Toes_Guide'.format(leg)],
            aim_axis=(0, 0, 1), up_axis=(0, 1, 0), target_locator='Up',
            fix_last=False,
            node_array=node_array)
        self.fix_guides_orientation(
            guides=["L_{}Foot_Out_Guide".format(leg), 'L_{}Foot_BallFloor_Guide'.format(leg)],
            aim_axis=(-1, 0, 0), up_axis=(0, 1, 0), target_locator='Up',
            fix_last=False,
            node_array=node_array)
        self.fix_guides_orientation(
            guides=["L_{}Foot_In_Guide".format(leg), 'L_{}Foot_BallFloor_Guide'.format(leg)],
            aim_axis=(1, 0, 0), up_axis=(0, 1, 0), target_locator='Up',
            fix_last=False,
            node_array=node_array)
        self.fix_guides_orientation(
            guides=['L_{}Foot_BallFloor_Guide'.format(leg), 'L_{}Foot_Toes_Guide'.format(leg)],
            aim_axis=(0, 1, 0), up_axis=(0, 0, 1), target_locator='Up',
            fix_last=False,
            node_array=node_array)

        cmds.delete(cmds.orientConstraint('L_{}Foot_HeelMid_Guide'.format(leg),'L_{}Foot_Toes_Guide'.format(leg), mo=False))

        # cmds.select('L_{}Foot_Heel_Guide'.format(leg), 'L_{}Foot_HeelMid_Guide'.format(leg), 'L_{}Foot_BallFloor_Guide'.format(leg),
        #             "L_{}Foot_In_Guide".format(leg),"L_{}Foot_Out_Guide".format(leg),'L_{}Foot_Toes_Guide'.format(leg))
        # self.zero(axis='Y')