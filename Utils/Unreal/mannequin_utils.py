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
    rig_joints = cmds.listRelatives('root', ad=True, type='joint') or []
    hierarchy_array = Skeletor.unparent_hierarchy(rig_joints)
    hierarchy_restored = False

    try:
        #Do some reparents to make it work
        parent_push_joints()

        #Put in Correct Position
        for jnt in rig_map:
            source_jnt = rig_map[jnt]
            if cmds.objExists(source_jnt) and cmds.objExists(jnt):
                cmds.delete(cmds.pointConstraint(source_jnt, jnt))
            else:
                cmds.warning('Skipping point snap {} -> {}'.format(source_jnt, jnt))
            if jnt.endswith('_l'):
                mirror_source = source_jnt.replace('L_', 'R_')
                mirror_target = replace_last_l_with_r(jnt)
                if cmds.objExists(mirror_source) and cmds.objExists(mirror_target):
                    cmds.delete(cmds.pointConstraint(mirror_source, mirror_target))
                else:
                    cmds.warning('Skipping point snap {} -> {}'.format(mirror_source, mirror_target))

        # spine_05 should sit between spine_04 (chest) and neck_01, not at Spine_End_Bnd
        if cmds.objExists('spine_05') and cmds.objExists('spine_04') and cmds.objExists('neck_01'):
            sp = cmds.xform('spine_04', q=True, ws=True, t=True)
            ep = cmds.xform('neck_01',  q=True, ws=True, t=True)
            cmds.xform('spine_05', ws=True, t=[
                (sp[0] + ep[0]) * 0.5,
                (sp[1] + ep[1]) * 0.5,
                (sp[2] + ep[2]) * 0.5,
            ])
            print('Placed spine_05 at midpoint between spine_04 and neck_01')

        #We need joints in world back to make skeletor work later
        for jnt in parent_map:
            if cmds.objExists(jnt):
                cmds.parent(jnt, w=True)
            else:
                cmds.warning('Skipping missing joint: {}'.format(jnt))
            if jnt.endswith('_l'):
                mirror_jnt = replace_last_l_with_r(jnt)
                if cmds.objExists(mirror_jnt):
                    cmds.parent(mirror_jnt, w=True)
                else:
                    cmds.warning('Skipping missing joint: {}'.format(mirror_jnt))

        #Reparent everything
        Skeletor.parent_hierarchy(hierarchy_array)
        hierarchy_restored = True

        #Fix Aims
        fix_spine_head(rig_joints)
        fix_clav_arms(rig_joints)
        fix_fingers(rig_joints)
        fix_legs_feet(rig_joints)

        #Place twist joints at evenly spaced intervals along their limb segment
        place_twist_joints()

        #Frezze transforms? Not sure if needed, and some extra hardcoded stuff
        for joint in rig_joints:
            if not cmds.objExists(joint):
                continue
            if cmds.listConnections(joint, type='skinCluster'):
                cmds.warning('Skipping freeze on skinned joint: {}'.format(joint))
                continue
            try:
                cmds.makeIdentity(joint, rotate=True, apply=True)
            except Exception as error:
                cmds.warning('Skipping freeze on {}: {}'.format(joint, error))

        temp_world_nodes = ['neck_02', 'clavicle_r', 'clavicle_l', 'clavicle_pec_r', 'clavicle_pec_l', 'spine_04_latissimus_l', 'spine_04_latissimus_r']
        for node in temp_world_nodes:
            if cmds.objExists(node):
                cmds.parent(node, w=True)
            else:
                cmds.warning('Skipping world parent for missing node: {}'.format(node))

        # Spine/neck orientations are set by fix_spine_head; no MEL override needed here.

        parent_pairs = [
            ('neck_02', 'neck_01'),
            ('clavicle_r', 'spine_05'),
            ('clavicle_l', 'spine_05'),
            ('clavicle_pec_r', 'spine_05'),
            ('clavicle_pec_l', 'spine_05'),
            ('spine_04_latissimus_l', 'spine_05'),
            ('spine_04_latissimus_r', 'spine_05')
        ]
        for child, parent in parent_pairs:
            if cmds.objExists(child) and cmds.objExists(parent):
                cmds.parent(child, parent)
            else:
                cmds.warning('Skipping parent {} -> {}'.format(child, parent))

        # cmds.setAttr('head.jointOrientX', 0)
        # cmds.setAttr('head.jointOrientY', 0)
        # cmds.setAttr('head.jointOrientZ', 0)

        # Official Parents with Scale Fix
        for jnt in rig_map:
            source_jnt = rig_map[jnt]

            # Parent and scale connections for the left side
            if cmds.objExists(source_jnt) and cmds.objExists(jnt):
                cmds.parentConstraint(source_jnt, jnt, mo=True)
            else:
                cmds.warning('Skipping parent constraint {} -> {}'.format(source_jnt, jnt))
            #cmds.connectAttr(f"{source_jnt}.scale", f"{jnt}.scale", f=True)

            if jnt.endswith('_l'):
                mirror_source = source_jnt.replace('L_', 'R_')
                mirror_target = replace_last_l_with_r(jnt)
                if cmds.objExists(mirror_source) and cmds.objExists(mirror_target):
                    cmds.parentConstraint(mirror_source, mirror_target, mo=True)
                else:
                    cmds.warning('Skipping parent constraint {} -> {}'.format(mirror_source, mirror_target))
                #cmds.scaleConstraint(mirror_source, mirror_target, mo=True)
                #ensure_positive_scale(f"{mirror_source}.scale", f"{mirror_target}.scale")


        #Place Ik and weapon sockets
        socket_pairs = [
            ('hand_r', 'ik_hand_gun'),
            ('hand_l', 'ik_hand_l'),
            ('hand_r', 'ik_hand_r'),
            ('foot_l', 'ik_foot_l'),
            ('foot_r', 'ik_foot_r'),
            ('hand_l', 'weapon_l'),
            ('hand_r', 'weapon_r')
        ]
        for source, target in socket_pairs:
            if cmds.objExists(source) and cmds.objExists(target):
                cmds.parentConstraint(source, target)
            else:
                cmds.warning('Skipping socket parent constraint {} -> {}'.format(source, target))


        if cmds.objExists('scale_reader') and cmds.objExists('root'):
            cmds.scaleConstraint('scale_reader', 'root')

        #Done
        print('Done Placing Mannequin Skeleton')
    finally:
        if not hierarchy_restored:
            try:
                Skeletor.parent_hierarchy(hierarchy_array)
            except Exception as error:
                cmds.warning('Failed to restore hierarchy after error: {}'.format(error))


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
        parent_jnt = parent_map[jnt]
        if cmds.objExists(jnt) and cmds.objExists(parent_jnt):
            cmds.parent(jnt, parent_jnt)
        else:
            cmds.warning('Skipping parent push {} -> {}'.format(jnt, parent_jnt))
        if jnt.endswith('_l'):
            mirror_jnt = replace_last_l_with_r(jnt)
            mirror_parent_jnt = replace_last_l_with_r(parent_jnt)
            if cmds.objExists(mirror_jnt) and cmds.objExists(mirror_parent_jnt):
                cmds.parent(mirror_jnt, mirror_parent_jnt)
            else:
                cmds.warning('Skipping parent push {} -> {}'.format(mirror_jnt, mirror_parent_jnt))


def create_aim_locators(guide):

    up_locator    = cmds.spaceLocator(n=guide+'_Temp_Up'+nc['locator'])[0]
    side_locator  = cmds.spaceLocator(n=guide+'_Temp_Side'+nc['locator'])[0]
    front_locator = cmds.spaceLocator(n=guide+'_Temp_Front'+nc['locator'])[0]
    back_locator  = cmds.spaceLocator(n=guide+'_Temp_Back'+nc['locator'])[0]

    mt.match(up_locator,    guide, r=False)
    mt.match(side_locator,  guide, r=False)
    mt.match(front_locator, guide, r=False)
    mt.match(back_locator,  guide, r=False)

    cmds.move(0,  10, 0,   up_locator,    r=True)  # world Y+
    cmds.move(10,  0, 0,   side_locator,  r=True)  # world X+
    cmds.move(0,   0, 10,  front_locator, r=True)  # world Z+
    cmds.move(0,   0, -10, back_locator,  r=True)  # world Z- (backwards)

    return up_locator, side_locator, front_locator, back_locator

def fix_guides_orientation(guides=[], aim_axis=(1,0,0), up_axis=(0,1,0) , target_locator='up_locator', fix_last=True, node_array=None, do_push_parents=False, last_rotations=[0,0,0]):


    # Skeletor.rotate_planar(array)
    if not node_array:
        return False
    existing_guides = [guide for guide in guides if cmds.objExists(guide)]
    for guide in guides:
        if not cmds.objExists(guide):
            cmds.warning('Skipping missing guide: {}'.format(guide))

    if not existing_guides:
        cmds.warning('No valid guides found for orientation fix.')
        return False

    hierarchy_array = Skeletor.unparent_hierarchy(node_array)
    hierarchy_restored = False

    try:
        if do_push_parents:
            parent_push_joints()

        for num, guide in enumerate(existing_guides):

            #Decide the up vector
            up_locator, side_locator, front_locator, back_locator = create_aim_locators(guide)

            if target_locator == 'Up':
                aim_loc = up_locator
            elif target_locator == 'Front':
                aim_loc = front_locator
            elif target_locator == 'Side':
                aim_loc = side_locator
            elif target_locator == 'Back':
                aim_loc = back_locator
            else:
                aim_loc = up_locator

            #Aim constriant to lower guide in guides array
            if guide == existing_guides[-1]:
                #Do stuff on last guide
                if fix_last:
                    if num > 0:
                        constraint = cmds.orientConstraint(existing_guides[num-1], guide)
                        cmds.delete(constraint)
                    cmds.rotate(last_rotations[0], last_rotations[1], last_rotations[2], guide, r=True, os=True, fo=True)
            else:
                #aim to next guide
                print(guide, existing_guides[num+1])
                constraint = cmds.aimConstraint(existing_guides[num+1], guide, aimVector=aim_axis, upVector=up_axis,
                                   worldUpType="object", worldUpObject=aim_loc)
                cmds.delete(constraint)

            #Delete stuff
            cmds.delete(up_locator, side_locator, front_locator, back_locator)


        # We need joints in world back to make skeletor work later
        for jnt in parent_map:
            if cmds.objExists(jnt):
                cmds.parent(jnt, w=True)
            if jnt.endswith('_l'):
                mirror_jnt = replace_last_l_with_r(jnt)
                if cmds.objExists(mirror_jnt):
                    cmds.parent(mirror_jnt, w=True)

        #Reaprent the hierarchy
        Skeletor.parent_hierarchy(hierarchy_array)
        hierarchy_restored = True
    finally:
        if not hierarchy_restored:
            try:
                Skeletor.parent_hierarchy(hierarchy_array)
            except Exception as error:
                cmds.warning('Failed to restore hierarchy in fix_guides_orientation: {}'.format(error))

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
    # Temporarily detach spine_04 so the parentConstraint-snap works cleanly
    if cmds.objExists('spine_04'):
        cmds.parent('spine_04', w=True)
        snap_targets = [j for j in ['spine_02', 'spine_03'] if cmds.objExists(j)]
        if snap_targets:
            cmds.delete(cmds.parentConstraint('spine_04', *snap_targets))
        if cmds.objExists('spine_03'):
            cmds.parent('spine_04', 'spine_03')

    # Orient pelvis → spine chain → neck chain so that:
    #   local X+ aims toward the next joint (up the chain)
    #   local Y+ points toward world Z- (backwards)
    # head is last with fix_last=False so it is handled separately below
    fix_guides_orientation(
        guides=["pelvis", "spine_01", "spine_02", "spine_03", "spine_04", "spine_05",
                "neck_01", "neck_02", "head"],
        aim_axis=(1, 0, 0), up_axis=(0, 1, 0), target_locator='Back',
        fix_last=False, node_array=node_array)

    # Head: X+ aims toward world Y+ (straight up); Y+ toward world Z- (backwards)
    if cmds.objExists('head'):
        head_pos = cmds.xform('head', q=True, ws=True, t=True)
        aim_target = cmds.spaceLocator(n='head_AimTarget_TMP_LOC')[0]
        up_ref     = cmds.spaceLocator(n='head_UpRef_TMP_LOC')[0]
        cmds.xform(aim_target, ws=True, t=[head_pos[0],      head_pos[1] + 20, head_pos[2]])
        cmds.xform(up_ref,     ws=True, t=[head_pos[0],      head_pos[1],      head_pos[2] - 10])
        c = cmds.aimConstraint(aim_target, 'head',
                               aimVector=(1, 0, 0), upVector=(0, 1, 0),
                               worldUpType='object', worldUpObject=up_ref)
        cmds.delete(c, aim_target, up_ref)

    # Center spine joints onto world X=0 plane
    existing_spine = [j for j in ["pelvis","spine_01","spine_02","spine_03","spine_04","spine_05"] if cmds.objExists(j)]
    if existing_spine:
        cmds.select(existing_spine)
        zero(axis='X')

def fix_clav_arms(node_array):

    # ---- Left arm: X+ aims toward next joint, Y toward world Z- (Back) ----

    # Main chain: clavicle -> upperarm -> lowerarm -> hand
    fix_guides_orientation(
        guides=["clavicle_l", "upperarm_l", "lowerarm_l", "hand_l"],
        aim_axis=(1, 0, 0), up_axis=(0, 1, 0), target_locator='Back',
        fix_last=True, node_array=node_array,
        do_push_parents=True, last_rotations=[-90, 0, 0])

    # Upper arm twists: twist_01 -> twist_02 -> lowerarm (lowerarm is target only, fix_last=False)
    fix_guides_orientation(
        guides=["upperarm_twist_01_l", "upperarm_twist_02_l", "lowerarm_l"],
        aim_axis=(1, 0, 0), up_axis=(0, 1, 0), target_locator='Back',
        fix_last=False, node_array=node_array,
        do_push_parents=True, last_rotations=[0, 0, 0])

    # Lower arm twists: twist_01 -> twist_02 -> hand (hand is target only, fix_last=False)
    fix_guides_orientation(
        guides=["lowerarm_twist_01_l", "lowerarm_twist_02_l", "hand_l"],
        aim_axis=(1, 0, 0), up_axis=(0, 1, 0), target_locator='Back',
        fix_last=False, node_array=node_array,
        do_push_parents=True, last_rotations=[0, 0, 0])

    # ---- Right arm: X- aims toward next joint, Y toward world Z+ (Front) ----

    # Main chain
    fix_guides_orientation(
        guides=["clavicle_r", "upperarm_r", "lowerarm_r", "hand_r"],
        aim_axis=(-1, 0, 0), up_axis=(0, 1, 0), target_locator='Front',
        fix_last=True, node_array=node_array,
        do_push_parents=True, last_rotations=[-90, 0, 0])

    # Upper arm twists
    fix_guides_orientation(
        guides=["upperarm_twist_01_r", "upperarm_twist_02_r", "lowerarm_r"],
        aim_axis=(-1, 0, 0), up_axis=(0, 1, 0), target_locator='Front',
        fix_last=False, node_array=node_array,
        do_push_parents=True, last_rotations=[0, 0, 0])

    # Lower arm twists
    fix_guides_orientation(
        guides=["lowerarm_twist_01_r", "lowerarm_twist_02_r", "hand_r"],
        aim_axis=(-1, 0, 0), up_axis=(0, 1, 0), target_locator='Front',
        fix_last=False, node_array=node_array,
        do_push_parents=True, last_rotations=[0, 0, 0])

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

def place_twist_joints():
    """
    Distribute twist joints evenly along their parent limb segment.
    For N twists in a segment the positions are at t = i/(N+1) (i=1..N)
    between the segment start and end joints in world space.
    Works on both sides automatically.

    Also repositions spine_05 to the midpoint between spine_04 and neck_01.

    Can also be called standalone after parent_to_superhero_template:
        mannequin_utils.place_twist_joints()
    """
    # spine_05: midpoint between chest (spine_04) and neck_01
    if cmds.objExists('spine_05') and cmds.objExists('spine_04') and cmds.objExists('neck_01'):
        sp = cmds.xform('spine_04', q=True, ws=True, t=True)
        ep = cmds.xform('neck_01',  q=True, ws=True, t=True)
        cmds.xform('spine_05', ws=True, t=[
            (sp[0] + ep[0]) * 0.5,
            (sp[1] + ep[1]) * 0.5,
            (sp[2] + ep[2]) * 0.5,
        ])
        print('Placed spine_05 at midpoint between spine_04 and neck_01')

    # (segment_start, segment_end, [twist_joints_ordered_01_first])
    segments = [
        ('upperarm_l', 'lowerarm_l', ['upperarm_twist_01_l', 'upperarm_twist_02_l']),
        ('lowerarm_l', 'hand_l',     ['lowerarm_twist_01_l', 'lowerarm_twist_02_l']),
        ('thigh_l',    'calf_l',     ['thigh_twist_01_l',    'thigh_twist_02_l']),
        ('calf_l',     'foot_l',     ['calf_twist_01_l',     'calf_twist_02_l']),
        ('upperarm_r', 'lowerarm_r', ['upperarm_twist_01_r', 'upperarm_twist_02_r']),
        ('lowerarm_r', 'hand_r',     ['lowerarm_twist_01_r', 'lowerarm_twist_02_r']),
        ('thigh_r',    'calf_r',     ['thigh_twist_01_r',    'thigh_twist_02_r']),
        ('calf_r',     'foot_r',     ['calf_twist_01_r',     'calf_twist_02_r']),
    ]

    for start_jnt, end_jnt, twist_jnts in segments:
        if not cmds.objExists(start_jnt) or not cmds.objExists(end_jnt):
            cmds.warning('place_twist_joints: skipping segment {} -> {} (missing)'.format(start_jnt, end_jnt))
            continue

        existing = [j for j in twist_jnts if cmds.objExists(j)]
        if not existing:
            continue

        sp = cmds.xform(start_jnt, q=True, ws=True, t=True)
        ep = cmds.xform(end_jnt,   q=True, ws=True, t=True)
        n  = len(existing)

        for i, twist in enumerate(existing):
            t = float(i + 1) / float(n + 1)
            pos = [
                sp[0] + (ep[0] - sp[0]) * t,
                sp[1] + (ep[1] - sp[1]) * t,
                sp[2] + (ep[2] - sp[2]) * t,
            ]
            cmds.xform(twist, ws=True, t=pos)
            print('Placed {} at {:.0f}% between {} and {}'.format(twist, t * 100, start_jnt, end_jnt))


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


mannequin_capture_joints = [
    'root', 'attach', 'pelvis', 'spine_01', 'spine_02', 'spine_03', 'spine_04', 'spine_05',
    'clavicle_l', 'upperarm_l', 'lowerarm_l', 'hand_l', 'index_metacarpal_l', 'index_01_l',
    'index_02_l', 'index_03_l', 'middle_metacarpal_l', 'middle_01_l', 'middle_02_l', 'middle_03_l',
    'pinky_metacarpal_l', 'pinky_01_l', 'pinky_02_l', 'pinky_03_l', 'ring_metacarpal_l', 'ring_01_l',
    'ring_02_l', 'ring_03_l', 'thumb_01_l', 'thumb_02_l', 'thumb_03_l', 'weapon_l',
    'lowerarm_twist_01_l', 'lowerarm_twist_02_l', 'upperarm_twist_01_l', 'upperarm_twist_02_l',
    'clavicle_r', 'upperarm_r', 'lowerarm_r', 'hand_r', 'index_metacarpal_r', 'index_01_r',
    'index_02_r', 'index_03_r', 'middle_metacarpal_r', 'middle_01_r', 'middle_02_r', 'middle_03_r',
    'pinky_metacarpal_r', 'pinky_01_r', 'pinky_02_r', 'pinky_03_r', 'ring_metacarpal_r', 'ring_01_r',
    'ring_02_r', 'ring_03_r', 'thumb_01_r', 'thumb_02_r', 'thumb_03_r', 'weapon_r',
    'lowerarm_twist_01_r', 'lowerarm_twist_02_r', 'upperarm_twist_01_r', 'upperarm_twist_02_r',
    'neck_01', 'neck_02', 'head', 'thigh_l', 'calf_l', 'calf_twist_01_l', 'calf_twist_02_l',
    'foot_l', 'ball_l', 'thigh_twist_01_l', 'thigh_r', 'calf_r', 'calf_twist_01_r', 'calf_twist_02_r',
    'foot_r', 'ball_r', 'thigh_twist_01_r', 'ik_foot_root', 'ik_foot_l', 'ik_foot_r', 'ik_hand_root',
    'ik_hand_gun', 'ik_hand_l', 'ik_hand_r'
]


def _get_attr_vector(node, attrs, default=0.0):
    values = []
    for attr in attrs:
        if cmds.attributeQuery(attr, n=node, ex=True):
            values.append(cmds.getAttr('{}.{}'.format(node, attr)))
        else:
            values.append(default)
    return values


def _set_attr_vector(node, attrs, values):
    if not values:
        return
    for attr, value in zip(attrs, values):
        if cmds.attributeQuery(attr, n=node, ex=True):
            try:
                cmds.setAttr('{}.{}'.format(node, attr), value)
            except Exception as error:
                cmds.warning('Could not set {}.{}: {}'.format(node, attr, error))


def capture_mannequin_skeleton_data(joints=None, file_path=None, print_json=True):
    """
    Capture transform + hierarchy data for mannequin joints.

    Args:
        joints: list of joint names. Defaults to mannequin_capture_joints.
        file_path: optional JSON path to write.
        print_json: print the JSON payload to Script Editor.

    Returns:
        dict payload with metadata, joint_order, and joints info.

    Example:
        data = capture_mannequin_skeleton_data()
        capture_mannequin_skeleton_data(file_path=r'C:/temp/mannequin_skeleton_capture.json')
    """
    import json

    if joints is None:
        joints = mannequin_capture_joints

    payload = {
        'meta': {
            'version': 1,
            'description': 'Captured from mannequin_utils.capture_mannequin_skeleton_data'
        },
        'joint_order': [],
        'joints': {}
    }

    for joint in joints:
        if not cmds.objExists(joint):
            cmds.warning('capture_mannequin_skeleton_data: missing joint {}'.format(joint))
            continue

        parent = cmds.listRelatives(joint, p=True)
        parent_name = parent[0] if parent else None

        payload['joint_order'].append(joint)
        payload['joints'][joint] = {
            'parent': parent_name,
            'world_translate': cmds.xform(joint, q=True, ws=True, t=True),
            'world_rotate': cmds.xform(joint, q=True, ws=True, ro=True),
            'local_translate': _get_attr_vector(joint, ['translateX', 'translateY', 'translateZ'], 0.0),
            'local_rotate': _get_attr_vector(joint, ['rotateX', 'rotateY', 'rotateZ'], 0.0),
            'local_scale': _get_attr_vector(joint, ['scaleX', 'scaleY', 'scaleZ'], 1.0),
            'joint_orient': _get_attr_vector(joint, ['jointOrientX', 'jointOrientY', 'jointOrientZ'], 0.0),
            'rotate_order': cmds.getAttr('{}.rotateOrder'.format(joint)) if cmds.attributeQuery('rotateOrder', n=joint, ex=True) else 0,
            'radius': cmds.getAttr('{}.radius'.format(joint)) if cmds.attributeQuery('radius', n=joint, ex=True) else 1.0,
            'segment_scale_compensate': cmds.getAttr('{}.segmentScaleCompensate'.format(joint)) if cmds.attributeQuery('segmentScaleCompensate', n=joint, ex=True) else 1,
        }

    json_text = json.dumps(payload, indent=4)

    if print_json:
        print(json_text)

    if file_path:
        with open(file_path, 'w') as out_file:
            out_file.write(json_text)
        print('capture_mannequin_skeleton_data: saved {}'.format(file_path))

    return payload


def recreate_mannequin_from_json(source=None):
    """
    Recreate/reposition mannequin joints from JSON payload.

    Args:
        source: dict payload OR path to JSON file.
                If None, defaults to mannequin_skeleton_capture.json in this folder.
    """
    import json

    if source is None:
        source = os.path.join(os.path.dirname(__file__), 'mannequin_skeleton_capture.json')

    if isinstance(source, dict):
        payload = source
    else:
        if not os.path.isfile(source):
            cmds.error('recreate_mannequin_from_json: file not found {}'.format(source))
            return
        with open(source, 'r') as in_file:
            payload = json.load(in_file)

    joints_data = payload.get('joints', {})
    joint_order = payload.get('joint_order', list(joints_data.keys()))

    # Create missing joints first
    created = []
    for joint in joint_order:
        if not joint:
            continue
        if not cmds.objExists(joint):
            cmds.select(cl=True)
            cmds.joint(n=joint)
            created.append(joint)

    # Unparent to world before rebuilding hierarchy
    for joint in joint_order:
        if cmds.objExists(joint):
            try:
                cmds.parent(joint, w=True)
            except Exception:
                pass

    # Rebuild parent relationships
    for joint in joint_order:
        if not cmds.objExists(joint):
            continue
        info = joints_data.get(joint, {})
        parent = info.get('parent')
        if parent and cmds.objExists(parent):
            try:
                cmds.parent(joint, parent)
            except Exception as error:
                cmds.warning('recreate_mannequin_from_json: could not parent {} -> {} ({})'.format(joint, parent, error))

    # Reapply joint values in final hierarchy
    for joint in joint_order:
        if not cmds.objExists(joint):
            continue
        info = joints_data.get(joint, {})

        if 'rotate_order' in info and cmds.attributeQuery('rotateOrder', n=joint, ex=True):
            cmds.setAttr('{}.rotateOrder'.format(joint), int(info.get('rotate_order', 0)))

        _set_attr_vector(joint, ['jointOrientX', 'jointOrientY', 'jointOrientZ'], info.get('joint_orient'))
        _set_attr_vector(joint, ['translateX', 'translateY', 'translateZ'], info.get('local_translate'))
        _set_attr_vector(joint, ['rotateX', 'rotateY', 'rotateZ'], info.get('local_rotate'))
        _set_attr_vector(joint, ['scaleX', 'scaleY', 'scaleZ'], info.get('local_scale'))

        if 'radius' in info and cmds.attributeQuery('radius', n=joint, ex=True):
            cmds.setAttr('{}.radius'.format(joint), info.get('radius', 1.0))
        if 'segment_scale_compensate' in info and cmds.attributeQuery('segmentScaleCompensate', n=joint, ex=True):
            cmds.setAttr('{}.segmentScaleCompensate'.format(joint), int(info.get('segment_scale_compensate', 1)))

    print('recreate_mannequin_from_json: processed {} joints (created {}).'.format(len(joint_order), len(created)))
