from __future__ import absolute_import, division
'''

from Mutant_Tools.Utils.Unreal import mannequin_utils
mannequin_utils.import_mannequin_fancy_skeleton()

mannequin_utils.parent_to_superhero_template()


'''
import os
from maya import cmds, mel
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload
import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
reload(Mutant_Tools.Utils.Rigging.main_mutant)
mt = main_mutant.Mutant()
nc, curves, setup = mt.import_configs()

from Mutant_Tools.Utils.Wrap.Skeletor import Skeletor
cSkeletor = Skeletor.Skeletor()

def import_mannequin_skeleton():
    skeleton = os.path.join(os.path.dirname(__file__), 'MannequinFBX', 'SKM_Manny_BaseSkeleton.FBX')
    print(skeleton)
    cmds.file(skeleton, i=True)

def import_mannequin_fancy_skeleton():
    skeleton = os.path.join(os.path.dirname(__file__), 'MannequinFBX', 'SKM_Manny_Skeleton.FBX')
    print(skeleton)
    cmds.file(skeleton, i=True)
def parent_to_superhero_template():
    #Unparent all joints
    rig_joints = cmds.listRelatives('root', ad=True, type='joint')
    hierarchy_array = Skeletor.unparent_hierarchy(rig_joints)

    #Do some reparents to make it work
    parent_push_joints()

    #Put in Correct Position
    for jnt in rig_map:
        cmds.delete(cmds.pointConstraint(rig_map[jnt], jnt))
        if jnt.endswith('_l'):
            cmds.delete(cmds.pointConstraint(rig_map[jnt].replace('L_', 'R_'), replace_last_l_with_r(jnt)))


    #We need joints in world back to make skeletor work later
    for jnt in parent_map:
        cmds.parent(jnt, w=True)
        if jnt.endswith('_l'):
            cmds.parent(replace_last_l_with_r(jnt), w=True)

    #Reparent everything
    Skeletor.parent_hierarchy(hierarchy_array)

    #Fix Aims
    fix_spine_head(rig_joints)
    fix_clav_arms(rig_joints)
    fix_fingers(rig_joints)
    fix_legs_feet(rig_joints)

    #Frezze transforms? Not sure if needed, and some extra hardcoded stuff
    for joint in rig_joints:
        cmds.makeIdentity(joint, rotate=True, apply=True)

    cmds.parent('neck_02', 'clavicle_r', 'clavicle_l', 'clavicle_pec_r', 'clavicle_pec_l', 'spine_04_latissimus_l', 'spine_04_latissimus_r', w=True)

    cmds.select('spine_02','spine_03','spine_04', 'spine_05', 'neck_01')
    mel.eval("joint -e  -oj xyz -secondaryAxisOrient ydown -ch -zso;")

    cmds.parent('neck_02', 'neck_01')
    cmds.parent('clavicle_r', 'spine_05')
    cmds.parent('clavicle_l', 'spine_05')
    cmds.parent('clavicle_pec_r', 'spine_05')
    cmds.parent('clavicle_pec_l', 'spine_05')
    cmds.parent('spine_04_latissimus_l', 'spine_05')
    cmds.parent('spine_04_latissimus_r', 'spine_05')

    # cmds.setAttr('head.jointOrientX', 0)
    # cmds.setAttr('head.jointOrientY', 0)
    # cmds.setAttr('head.jointOrientZ', 0)

    # Official Parents with Scale Fix
    for jnt in rig_map:
        # Parent and scale connections for the left side
        cmds.parentConstraint(rig_map[jnt], jnt, mo=True)
        #cmds.connectAttr(f"{rig_map[jnt]}.scale", f"{jnt}.scale", f=True)

        if jnt.endswith('_l'):
            cmds.parentConstraint(rig_map[jnt].replace('L_', 'R_'), replace_last_l_with_r(jnt), mo=True)
            #cmds.scaleConstraint(rig_map[jnt].replace('L_', 'R_'), replace_last_l_with_r(jnt), mo=True)
            #ensure_positive_scale(f"{rig_map[jnt].replace('L_', 'R_')}.scale", f"{replace_last_l_with_r(jnt)}.scale")


    #Place Ik and weapon sockets
    cmds.parentConstraint('hand_r', 'ik_hand_gun')
    cmds.parentConstraint('hand_l', 'ik_hand_l')
    cmds.parentConstraint('hand_r', 'ik_hand_r')
    cmds.parentConstraint('foot_l', 'ik_foot_l')
    cmds.parentConstraint('foot_r', 'ik_foot_r')
    cmds.parentConstraint('hand_l', 'weapon_l')
    cmds.parentConstraint('hand_r', 'weapon_r')


    if cmds.objExists('scale_reader'):
        cmds.scaleConstraint('scale_reader', 'root')

    #Done
    print('Done Placing Mannequin Skeleton')


def ensure_positive_scale(source_attr, target_attr):
    # Create a multiplyDivide node
    md_node = cmds.createNode('multiplyDivide', name=f"{target_attr}_scale_md")

    # Connect the source scale attribute to the input of the multiplyDivide node
    cmds.connectAttr(source_attr, f"{md_node}.input1")

    # Set the second input of the multiplyDivide node to -1 for any negative scale
    for axis in ['X', 'Y', 'Z']:
        scale_value = cmds.getAttr(f"{source_attr}{axis}")
        if scale_value < 0:
            cmds.setAttr(f"{md_node}.input2{axis}", -1)
        else:
            cmds.setAttr(f"{md_node}.input2{axis}", 1)

    # Connect the output of the multiplyDivide node to the target's scale
    cmds.connectAttr(f"{md_node}.output", target_attr, f=True)

def remove_constriants_in_main_skeleton():
    root = 'root'

    pr_constriants = cmds.listRelatives(root, ad=True, type='parentConstraint')
    p_constriants = cmds.listRelatives(root, ad=True, type='pointConstraint')
    o_constriants = cmds.listRelatives(root, ad=True, type='orientConstraint')
    s_constriants = cmds.listRelatives(root, ad=True, type='scaleConstraint')

    cmds.delete(pr_constriants, p_constriants, o_constriants, s_constriants)

def replace_last_l_with_r(name):
    if name.endswith('_l'):
        return name[:-2] + '_r'
    return name

def parent_push_joints():
    for jnt in parent_map:
        cmds.parent(jnt, parent_map[jnt])
        if jnt.endswith('_l'):
            cmds.parent(replace_last_l_with_r(jnt), replace_last_l_with_r(parent_map[jnt]))


def create_aim_locators(guide):

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

def fix_guides_orientation(guides=[], aim_axis=(1,0,0), up_axis=(0,1,0) , target_locator='up_locator', fix_last=True, node_array=None, do_push_parents=False, last_rotations=[0,0,0]):


    # Skeletor.rotate_planar(array)
    if not node_array:
        return False
    hierarchy_array = Skeletor.unparent_hierarchy(node_array)
    if do_push_parents:
        parent_push_joints()

    for num, guide in enumerate(guides):

        #Decide the up vector
        up_locator, side_locator, front_locator = create_aim_locators(guide)

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
                cmds.rotate(last_rotations[0], last_rotations[1], last_rotations[2], guide, r=True, os=True, fo=True)
        else:
            #aim to next guide
            print(guide, guides[num+1])
            constraint = cmds.aimConstraint(guides[num+1], guide, aimVector=aim_axis, upVector=up_axis,
                               worldUpType="object", worldUpObject=aim_loc)
            cmds.delete(constraint)

        #Delete stuff
        cmds.delete(up_locator, side_locator, front_locator)


    # We need joints in world back to make skeletor work later
    for jnt in parent_map:
        try:
            cmds.parent(jnt, w=True)
        except:
            pass
        if jnt.endswith('_l'):
            try:
                cmds.parent(replace_last_l_with_r(jnt), w=True)
            except:
                pass

    #Reaprent the hierarchy
    Skeletor.parent_hierarchy(hierarchy_array)

def zero(axis=''):


    sel = cmds.ls(sl=True)
    hierarchy_array = Skeletor.unparent_hierarchy(sel)

    for s in sel:
        cmds.select(s)
        if axis == 'X':
            cmds.move(0, cmds.getAttr('{}.ty'.format(s)), cmds.getAttr('{}.tz'.format(s)))
        elif axis == 'Y':
            cmds.move(cmds.getAttr('{}.tx'.format(s)), 0, cmds.getAttr('{}.tz'.format(s)))
        else:
            cmds.move(cmds.getAttr('{}.tx'.format(s)), cmds.getAttr('{}.ty'.format(s)), 0)

    Skeletor.parent_hierarchy(hierarchy_array)

def fix_spine_head(node_array):

    cmds.parent('spine_04', w=True)
    cmds.delete(cmds.parentConstraint('spine_04', 'spine_02', 'spine_03'))
    cmds.parent('spine_04', 'spine_03')

    #Skeletor.rotate_planar(["Spine_Root_Guide", "Spine_Base_Guide", "Spine_Belly_Guide","Spine_Chest_Guide","Spine_End_Guide"])
    fix_guides_orientation(guides=["pelvis","spine_01","spine_02","spine_03","spine_04","spine_05", "neck_01", "neck_02", "head"],
                                aim_axis=(1, 0, 0), up_axis=(0, 1, 0), target_locator='Back',
                                fix_last=False, node_array=node_array)
    #Force This spine ones
    fix_guides_orientation(
        guides=["spine_02", "spine_03", "spine_04", "spine_05"],
        aim_axis=(1, 0, 0), up_axis=(0, 1, 0), target_locator='Back',
        fix_last=False, node_array=node_array)
    cmds.select("pelvis","spine_01","spine_02","spine_03","spine_04","spine_05")
    zero(axis='X')

def fix_clav_arms(node_array):

    #Blue Up, Green Back
    #Hand is Blue Back, Green Down
    fix_guides_orientation(
        guides=["clavicle_l", "upperarm_l", 'upperarm_twist_01_l', 'upperarm_twist_02_l', "lowerarm_l", 'lowerarm_twist_02_l', 'lowerarm_twist_01_l' , 'hand_l'],
        aim_axis=(1, 0, 0), up_axis=(0, -1, 0), target_locator='Front',
        fix_last=True, node_array=node_array,
        do_push_parents=True, last_rotations=[-90,0,0])

    #Right Side
    # Green Front Blue Down, Red Back
    # Hand is RedBack, Green Up, Blue Front
    fix_guides_orientation(
        guides=["clavicle_r", "upperarm_r", 'upperarm_twist_01_r', 'upperarm_twist_02_r', "lowerarm_r", 'lowerarm_twist_02_r', 'lowerarm_twist_01_r' , 'hand_r'],
        aim_axis=(-1, 0, 0), up_axis=(0, 1, 0), target_locator='Front',
        fix_last=True, node_array=node_array,
        do_push_parents=True, last_rotations=[-90, 0, 0])

def fix_fingers(node_array):
    fix_guides_orientation(
        guides=["index_metacarpal_l", "index_01_l", "index_02_l", 'index_03_l'],
        aim_axis=(1, 0, 0), up_axis=(0, -1, 0), target_locator='Up',
        fix_last=True, node_array=node_array,
        do_push_parents=True, last_rotations=[0, 0, 0])
    fix_guides_orientation(
        guides=["ring_metacarpal_l", "ring_01_l", "ring_02_l", 'ring_03_l'],
        aim_axis=(1, 0, 0), up_axis=(0, -1, 0), target_locator='Up',
        fix_last=True, node_array=node_array,
        do_push_parents=True, last_rotations=[0, 0, 0])
    fix_guides_orientation(
        guides=["pinky_metacarpal_l", "pinky_01_l", "pinky_02_l", 'pinky_03_l'],
        aim_axis=(1, 0, 0), up_axis=(0, -1, 0), target_locator='Up',
        fix_last=True, node_array=node_array,
        do_push_parents=True, last_rotations=[0, 0, 0])
    fix_guides_orientation(
        guides=["middle_metacarpal_l", "middle_01_l", "middle_02_l", 'middle_03_l'],
        aim_axis=(1, 0, 0), up_axis=(0, -1, 0), target_locator='Up',
        fix_last=True, node_array=node_array,
        do_push_parents=True, last_rotations=[0, 0, 0])
    fix_guides_orientation(
        guides=["thumb_01_l", "thumb_02_l", "thumb_03_l"],
        aim_axis=(1, 0, 0), up_axis=(0, -1, 0), target_locator='Up',
        fix_last=True, node_array=node_array,
        do_push_parents=True, last_rotations=[0, 0, 0])

    #Blue Front, Green Up, Red Back
    fix_guides_orientation(
        guides=["index_metacarpal_r", "index_01_r", "index_02_r", 'index_03_r'],
        aim_axis=(-1, 0, 0), up_axis=(0, 1, 0), target_locator='Up',
        fix_last=True, node_array=node_array,
        do_push_parents=True, last_rotations=[0, 0, 0])
    fix_guides_orientation(
        guides=["ring_metacarpal_r", "ring_01_r", "ring_02_r", 'ring_03_r'],
        aim_axis=(-1, 0, 0), up_axis=(0, 1, 0), target_locator='Up',
        fix_last=True, node_array=node_array,
        do_push_parents=True, last_rotations=[0, 0, 0])
    fix_guides_orientation(
        guides=["pinky_metacarpal_r", "pinky_01_r", "pinky_02_r", 'pinky_03_r'],
        aim_axis=(-1, 0, 0), up_axis=(0, 1, 0), target_locator='Up',
        fix_last=True, node_array=node_array,
        do_push_parents=True, last_rotations=[0, 0, 0])
    fix_guides_orientation(
        guides=["middle_metacarpal_r", "middle_01_r", "middle_02_r", 'middle_03_r'],
        aim_axis=(-1, 0, 0), up_axis=(0, 1, 0), target_locator='Up',
        fix_last=True, node_array=node_array,
        do_push_parents=True, last_rotations=[0, 0, 0])
    fix_guides_orientation(
        guides=["thumb_01_r", "thumb_02_r", "thumb_03_r"],
        aim_axis=(-1, 0, 0), up_axis=(0, 1, 0), target_locator='Up',
        fix_last=True, node_array=node_array,
        do_push_parents=True, last_rotations=[0, 0, 0])

def fix_legs_feet(node_array):

    #Red up, Blue In, Green Back
    fix_guides_orientation(
        guides=["thigh_l", "thigh_twist_01_l", "thigh_twist_02_l", "calf_l", "calf_twist_02_l", 'calf_twist_01_l', 'foot_l'],
        aim_axis=(-1, 0, 0), up_axis=(0, -1, 0), target_locator='Front',
        fix_last=True, node_array=node_array,
        do_push_parents=True, last_rotations=[0, 0, 0])
    fix_guides_orientation(
        guides=["ball_l", "foot_l"],
        aim_axis=(-1, 0, 0), up_axis=(0, 1, 0), target_locator='Up',
        fix_last=False, node_array=node_array,
        do_push_parents=True, last_rotations=[0, 0, 0])
    cmds.setAttr('ball_l.rotateZ', -90)



#---------------------------------------------------------------------

rig_map = {
    'pelvis': 'Spine_Root_Bnd',

    'spine_01': 'Spine_Base_Bnd',
    'spine_02': 'Spine_Belly_Bnd',
    #'spine_03': '',
    'spine_04': 'Spine_Chest_Bnd',
    'spine_05': 'Spine_End_Bnd',

    'neck_01': 'Neck_1_Bnd',
    'neck_02': 'Neck_2_Bnd',
    'head': 'Head_Bnd',

    'clavicle_l': 'L_Clavicle_Bnd',
    'upperarm_l': 'L_Shoulder_Bnd_0_Bnd',
    'lowerarm_l': 'L_Elbow_Bnd_0_Bnd',
    'lowerarm_twist_02_l': 'L_Elbow_Bnd_1_Bnd',
    'lowerarm_twist_01_l': 'L_Elbow_Bnd_2_Bnd',
    'hand_l': 'L_Hand_Palm_Bnd',

    'index_metacarpal_l': 'L_Hand_Index_00_Bnd',
    'index_01_l': 'L_Hand_Index_01_Bnd',
    'index_02_l': 'L_Hand_Index_02_Bnd',
    'index_03_l': 'L_Hand_Index_03_Bnd',

    'middle_metacarpal_l': 'L_Hand_Middle_00_Bnd',
    'middle_01_l': 'L_Hand_Middle_01_Bnd',
    'middle_02_l': 'L_Hand_Middle_02_Bnd',
    'middle_03_l': 'L_Hand_Middle_03_Bnd',

    'thumb_01_l': 'L_Hand_Thumb_00_Bnd',
    'thumb_02_l': 'L_Hand_Thumb_01_Bnd',
    'thumb_03_l': 'L_Hand_Thumb_02_Bnd',

    'pinky_metacarpal_l': 'L_Hand_Pinky_00_Bnd',
    'pinky_01_l': 'L_Hand_Pinky_01_Bnd',
    'pinky_02_l': 'L_Hand_Pinky_02_Bnd',
    'pinky_03_l': 'L_Hand_Pinky_03_Bnd',

    'ring_metacarpal_l': 'L_Hand_Ring_00_Bnd',
    'ring_01_l': 'L_Hand_Ring_01_Bnd',
    'ring_02_l': 'L_Hand_Ring_02_Bnd',
    'ring_03_l': 'L_Hand_Ring_03_Bnd',

    'upperarm_twist_01_l': 'L_Shoulder_Bnd_1_Bnd',
    'upperarm_twist_02_l': 'L_Shoulder_Bnd_2_Bnd',

    'thigh_l': 'L_Hip_Bnd_0_Bnd',
    'calf_l': 'L_Knee_Bnd_0_Bnd',
    'foot_l': 'L_Foot_Ankle_Bnd',
    'ball_l': 'L_Foot_BallToes_Bnd',

    'calf_twist_02_l': 'L_Knee_Bnd_1_Bnd',
    'calf_twist_01_l': 'L_Knee_Bnd_2_Bnd',

    'thigh_twist_01_l': 'L_Hip_Bnd_1_Bnd',
    'thigh_twist_02_l': 'L_Hip_Bnd_2_Bnd'

}

parent_map = {

    'thigh_correctiveRoot_l' : 'thigh_l',
    'thigh_twistCor_01_l': 'thigh_twist_01_l',
    'thigh_twistCor_02_l': 'thigh_correctiveRoot_l',

    'thigh_bck_l': 'thigh_correctiveRoot_l',
    'thigh_fwd_l': 'thigh_correctiveRoot_l',
    'thigh_out_l': 'thigh_correctiveRoot_l',
    'thigh_bck_lwr_l': 'thigh_correctiveRoot_l',
    'thigh_in_l': 'thigh_correctiveRoot_l',
    'thigh_fwd_lwr_l': 'thigh_correctiveRoot_l',

    'calf_correctiveRoot_l': 'calf_l',
    'calf_kneeBack_l': 'thigh_correctiveRoot_l',
    'calf_knee_l': 'thigh_correctiveRoot_l',

    'ankle_bck_l': 'foot_l',
    'ankle_fwd_l': 'foot_l',

    'spine_04_latissimus_l': 'spine_05',
    'clavicle_pec_l': 'spine_05',

    'clavicle_scap_l': 'clavicle_l',
    'clavicle_out_l': 'clavicle_l',

    'upperarm_bck_l': 'upperarm_correctiveRoot_l',
    'upperarm_fwd_l': 'upperarm_correctiveRoot_l',
    'upperarm_in_l': 'upperarm_correctiveRoot_l',
    'upperarm_out_l': 'upperarm_correctiveRoot_l',

    'upperarm_correctiveRoot_l': 'upperarm_l',
    'lowerarm_correctiveRoot_l': 'lowerarm_l',

    'upperarm_tricep_l': 'upperarm_twist_02_l',
    'upperarm_bicep_l': 'upperarm_twist_02_l',
    'upperarm_twistCor_02_l': 'upperarm_twist_02_l',

    'lowerarm_in_l': 'lowerarm_correctiveRoot_l',
    'lowerarm_out_l': 'lowerarm_correctiveRoot_l',
    'lowerarm_fwd_l': 'lowerarm_correctiveRoot_l',
    'lowerarm_bck_l': 'lowerarm_correctiveRoot_l',

    'wrist_inner_l' : 'hand_l',
    'wrist_outer_l' : 'hand_l',

    'calf_twistCor_02_l': 'calf_twist_02_l',
    'upperarm_twistCor_01_l':'upperarm_twist_01_l'
}

base_bind_joints = [
'pelvis', 'spine_01', 'spine_02', 'spine_03', 'spine_04', 'spine_05', 'neck_01', 'neck_02', 'head', 'clavicle_l',
'upperarm_l', 'lowerarm_l', 'lowerarm_twist_01_l', 'lowerarm_twist_02_l', 'hand_l', 'wrist_inner_l', 'wrist_outer_l',
'index_metacarpal_l', 'index_01_l', 'index_02_l', 'index_03_l', 'middle_metacarpal_l', 'middle_01_l', 'middle_02_l',
'middle_03_l', 'thumb_01_l', 'thumb_02_l', 'thumb_03_l', 'pinky_metacarpal_l', 'pinky_01_l', 'pinky_02_l', 'pinky_03_l',
'ring_metacarpal_l', 'ring_01_l', 'ring_02_l', 'ring_03_l', 'upperarm_twist_01_l', 'upperarm_twist_02_l', 'clavicle_r',
'upperarm_r', 'lowerarm_r', 'lowerarm_twist_02_r', 'lowerarm_twist_01_r', 'hand_r', 'wrist_inner_r', 'wrist_outer_r',
'pinky_metacarpal_r', 'pinky_01_r', 'pinky_02_r', 'pinky_03_r', 'ring_metacarpal_r', 'ring_01_r', 'ring_02_r',
'ring_03_r', 'middle_metacarpal_r', 'middle_01_r', 'middle_03_r', 'middle_02_r', 'index_metacarpal_r', 'index_01_r',
'index_02_r', 'index_03_r', 'thumb_01_r', 'thumb_02_r', 'thumb_03_r', 'upperarm_twist_01_r', 'upperarm_twist_02_r',
'thigh_r', 'calf_r', 'foot_r', 'ball_r', 'calf_twist_02_r', 'calf_twist_01_r', 'thigh_twist_01_r', 'thigh_twist_02_r',
'thigh_l', 'calf_l', 'foot_l', 'ball_l', 'calf_twist_02_l', 'calf_twist_01_l', 'thigh_twist_01_l', 'thigh_twist_02_l']


#'thigh_twistCor_02_r'
