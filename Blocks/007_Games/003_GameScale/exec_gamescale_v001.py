from __future__ import absolute_import
from maya import cmds
import maya.api.OpenMaya as om
import json
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload
import os

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
from Mutant_Tools.Utils.Rigging import block_errors
reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()

#---------------------------------------------

TAB_FOLDER = '007_Games'
PYBLOCK_NAME = 'exec_gamescale'

BODY_ROOT = 'Root_Skl'
UNREAL_ROOT = 'root'
GLOBAL_SIZE = 'Global_Ctrl.size'

#---------------------------------------------

def create_gamescale_block(name = 'GameScale'):

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '003_GameScale.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()

    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name = name, icon = 'GameScale',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    block = block[0]

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#-------------------------

def build_gamescale_block():

    mt.import_configs()
    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]

    def option(attr):
        return bool(cmds.getAttr('{}.{}'.format(config, attr))) if cmds.attributeQuery(attr, n=config, exists=True) else True

    if option('FixBodySkeleton') and not cmds.objExists(BODY_ROOT):
        raise block_errors.BlockBuildError('No body skeleton', 'Move {} below ConvertBody, {} does not exist yet.'.format(block, BODY_ROOT), block=block)
    if option('FixUnrealSkeleton') and not cmds.objExists(UNREAL_ROOT):
        raise block_errors.BlockBuildError('No Unreal skeleton', 'Move {} below the Mannequin block, or turn FixUnrealSkeleton off.'.format(block), block=block)

    if option('FixMouthScale'):
        fix_mouth_scale()
    if option('FixPushScale'):
        fix_push_scale()

    # the face joints of the body skeleton can hang from the Unreal head (Mannequin block), so look in both skeletons
    no_own_scale = joints_without_own_scale((BODY_ROOT, UNREAL_ROOT)) if option('FixBodySkeleton') or option('FixUnrealSkeleton') else set()
    done = 0
    if option('FixBodySkeleton'):
        done += fix_skeleton(BODY_ROOT, no_own_scale)
    if option('FixUnrealSkeleton'):
        done += fix_skeleton(UNREAL_ROOT, no_own_scale)

    cmds.select(block)
    print('Build {} Success, {} joints now follow scale'.format(block, done))

#-------------------------
# Mouth

def fix_mouth_scale():
    """MouthGames lips drift when the rig scales, for two reasons:
    - the corner pullers stay at scale 1, so the mid ctrls constrained to them keep an unscaled offset.
    - the lip curve and its base wire stay at rest while the driver curve goes away with the head, so the wire
      has to bend them all that distance (this one also shows when the head only rotates).
    Pullers take the mouth parent scale, curve and base wire ride the mouth parent."""
    for config in cmds.ls('*_Config', type='network'):
        if not cmds.attributeQuery('Import_Command', n=config, exists=True):
            continue
        if 'exec_mouthgames' not in (cmds.getAttr(config + '.Import_Command') or ''):
            continue
        name = config[:-len('_Config')]
        parent = cmds.getAttr(config + '.SetParent')
        space = name + '_WireSpace_Grp'
        rig_grp = name + '_Rig_Grp'
        if cmds.objExists(space) or not cmds.objExists(parent) or not cmds.objExists(rig_grp):
            continue

        parent_scale = name + '_ParentScale_DM'
        if not cmds.objExists(parent_scale):
            parent_scale = cmds.createNode('decomposeMatrix', n=parent_scale)
            cmds.connectAttr(parent + '.worldMatrix[0]', parent_scale + '.inputMatrix')
        for puller in cmds.ls('*{}_*_Puller_Loc'.format(name), type='transform'):
            # right side pullers are born mirrored: keep their rest scale
            multiply = cmds.createNode('multiplyDivide', n=puller + '_GameScale_MD')
            cmds.connectAttr(parent_scale + '.outputScale', multiply + '.input1')
            cmds.setAttr(multiply + '.input2', *cmds.getAttr(puller + '.scale')[0])
            cmds.connectAttr(multiply + '.output', puller + '.scale', f=True)

        cmds.createNode('transform', n=space, p=rig_grp)
        cmds.setAttr(space + '.inheritsTransform', 0)
        rest = cmds.createNode('multMatrix', n=space + '_MM')
        cmds.setAttr(rest + '.matrixIn[0]', om.MMatrix(cmds.getAttr(parent + '.worldInverseMatrix[0]')), type='matrix')
        cmds.connectAttr(parent + '.worldMatrix[0]', rest + '.matrixIn[1]')
        follow = cmds.createNode('decomposeMatrix', n=space + '_DM')
        cmds.connectAttr(rest + '.matrixSum', follow + '.inputMatrix')
        for channel in ('Translate', 'Rotate', 'Scale'):
            cmds.connectAttr('{}.output{}'.format(follow, channel), '{}.{}'.format(space, channel.lower()))

        for side in ('Up', 'Dw'):
            wire = '{}_{}_Wire'.format(name, side)
            if not cmds.objExists(wire):
                continue
            base = cmds.listRelatives(cmds.listConnections(wire + '.baseWire[0]', s=True, d=False, shapes=True)[0], parent=True)[0]
            curve = cmds.listRelatives(cmds.deformer(wire, q=True, g=True)[0], parent=True)[0]
            cmds.parent(curve, base, space)

#-------------------------
# Push joints

def fix_push_scale():
    """Push joints (mt.create_push_joint) hang from two groups that only get a parentConstraint: the reader root
    and the ctrl root. Their local offsets and the push distances stayed at rest size. Nothing to do without them."""
    # reader roots first: the ctrl roots read the scale of the readers under them
    for root in cmds.ls('*_Reader_Loc_Root_Grp', type='transform') + cmds.ls('*_Push_*_Ctrl_Root_Grp', type='transform'):
        if cmds.listRelatives(root, type='scaleConstraint'):
            continue
        constraint = cmds.listRelatives(root, type='parentConstraint')
        if constraint:
            cmds.scaleConstraint(cmds.parentConstraint(constraint[0], q=True, tl=True)[0], root, mo=True)

#-------------------------
# Skeletons

def joints_without_own_scale(roots=(BODY_ROOT,)):
    """Joints whose bind joint ignores their parents' scale (brows only read their ctrl), found by testing global scale
    on the joints under roots. Unreal joints that follow other Unreal joints (sockets) have no bind joint to test."""
    if not cmds.objExists(GLOBAL_SIZE):
        return set()
    unreal = (set(cmds.listRelatives(UNREAL_ROOT, ad=True, type='joint') or []) | {UNREAL_ROOT}) if cmds.objExists(UNREAL_ROOT) else set()
    rest = cmds.getAttr(GLOBAL_SIZE)
    found = set()
    cmds.setAttr(GLOBAL_SIZE, rest * 2.0)
    try:
        for root in roots:
            if not cmds.objExists(root):
                continue
            for joint in cmds.listRelatives(root, ad=True, type='joint') or []:
                for target in _constraint_target(joint)[:1]:
                    if target in unreal:
                        continue
                    if _world_scale(target) < rest * 1.5:
                        found.add(joint)
    finally:
        cmds.setAttr(GLOBAL_SIZE, rest)
    return found


def fix_skeleton(root, multiply_by_parent=()):
    """Each joint copies its source joint (rest offset kept): position, rotation and world scale, no shear.

    Segment scale compensate is on, so a joint's world scale is its own scale attr and nothing leaks to the
    children. parentConstraint is replaced because it gets the rotation wrong under a non uniform parent.
    """
    joints = cmds.listRelatives(root, ad=True, type='joint') or []
    # rest offsets first: nothing has moved yet
    plans = {}
    for joint in joints:
        target = _constraint_target(joint)
        if target:
            world = om.MMatrix(cmds.getAttr(joint + '.worldMatrix[0]'))
            plans[joint] = (target[0], world * om.MMatrix(cmds.getAttr(target[0] + '.worldInverseMatrix[0]')), world)

    inverse_cache = {}
    done = 0
    for joint in joints:
        parent = (cmds.listRelatives(joint, parent=True, type='joint') or [None])[0]
        if not parent:
            continue
        cmds.setAttr(joint + '.segmentScaleCompensate', 1)
        if not cmds.listConnections(joint + '.inverseScale', s=True, d=False):
            cmds.connectAttr(parent + '.scale', joint + '.inverseScale')
        if joint not in plans:
            # no source (sockets roots, unused bones): rides its parent
            if not cmds.listConnections(joint + '.scale', s=True, d=False):
                cmds.connectAttr(parent + '.scale', joint + '.scale')
            done += 1
            continue
        target, offset, rest_world = plans[joint]
        for kind in ('parentConstraint', 'scaleConstraint'):
            old = cmds.listRelatives(joint, type=kind)
            if old:
                cmds.delete(old)
        _connect_joint(joint, parent, target, offset, rest_world, inverse_cache, joint in multiply_by_parent)
        done += 1
    return done


def _connect_joint(joint, parent, target, offset, rest_world, inverse_cache, multiply_by_parent):
    source = cmds.createNode('multMatrix', n=joint + '_GameScale_Source_MM')
    cmds.setAttr(source + '.matrixIn[0]', offset, type='matrix')
    cmds.connectAttr(target + '.worldMatrix[0]', source + '.matrixIn[1]')
    source_plug = source + '.matrixSum'

    # translate: the parent's scale still moves its children, read it through the full parent matrix
    translate_mm = cmds.createNode('multMatrix', n=joint + '_GameScale_T_MM')
    cmds.connectAttr(source_plug, translate_mm + '.matrixIn[0]')
    cmds.connectAttr(parent + '.worldInverseMatrix[0]', translate_mm + '.matrixIn[1]')
    translate_dm = cmds.createNode('decomposeMatrix', n=joint + '_GameScale_T_DM')
    cmds.connectAttr(translate_mm + '.matrixSum', translate_dm + '.inputMatrix')
    cmds.connectAttr(translate_dm + '.outputTranslate', joint + '.translate', f=True)

    # rotate: source and parent both without scale, so a non uniform scale can never turn the joint.
    # The parent's scale does not rotate a compensated child.
    pick = cmds.createNode('pickMatrix', n=joint + '_GameScale_R_PM')
    cmds.connectAttr(target + '.worldMatrix[0]', pick + '.inputMatrix')
    cmds.setAttr(pick + '.useScale', 0)
    cmds.setAttr(pick + '.useShear', 0)
    cmds.setAttr(pick + '.useTranslate', 0)
    rest_rotation = _rotation_only(rest_world) * om.MMatrix(cmds.getAttr(pick + '.outputMatrix')).inverse()
    orient = om.MEulerRotation([om.MAngle(a, om.MAngle.kDegrees).asRadians() for a in cmds.getAttr(joint + '.jointOrient')[0]]).asMatrix()
    rotate_mm = cmds.createNode('multMatrix', n=joint + '_GameScale_R_MM')
    cmds.setAttr(rotate_mm + '.matrixIn[0]', rest_rotation, type='matrix')
    cmds.connectAttr(pick + '.outputMatrix', rotate_mm + '.matrixIn[1]')
    cmds.connectAttr(_parent_inverse_rotation(parent, inverse_cache) + '.outputMatrix', rotate_mm + '.matrixIn[2]')
    cmds.setAttr(rotate_mm + '.matrixIn[3]', orient.inverse(), type='matrix')
    rotate_dm = cmds.createNode('decomposeMatrix', n=joint + '_GameScale_R_DM')
    cmds.connectAttr(rotate_mm + '.matrixSum', rotate_dm + '.inputMatrix')
    cmds.connectAttr(joint + '.rotateOrder', rotate_dm + '.inputRotateOrder')
    cmds.connectAttr(rotate_dm + '.outputRotate', joint + '.rotate', f=True)

    # scale: world scale along the joint's own axes
    scale_dm = cmds.createNode('decomposeMatrix', n=joint + '_GameScale_S_DM')
    cmds.connectAttr(source_plug, scale_dm + '.inputMatrix')
    scale_plug = scale_dm + '.outputScale'
    if multiply_by_parent:
        multiply = cmds.createNode('multiplyDivide', n=joint + '_GameScale_S_MD')
        cmds.connectAttr(scale_plug, multiply + '.input1')
        cmds.connectAttr(parent + '.scale', multiply + '.input2')
        scale_plug = multiply + '.output'
    cmds.connectAttr(scale_plug, joint + '.scale', f=True)


def _parent_inverse_rotation(parent, cache):
    """One pick + inverse per parent, shared by its children."""
    if parent not in cache:
        pick = cmds.createNode('pickMatrix', n=parent + '_GameScale_Parent_PM')
        cmds.connectAttr(parent + '.worldMatrix[0]', pick + '.inputMatrix')
        cmds.setAttr(pick + '.useScale', 0)
        cmds.setAttr(pick + '.useShear', 0)
        cmds.setAttr(pick + '.useTranslate', 0)
        inverse = cmds.createNode('inverseMatrix', n=parent + '_GameScale_Parent_IM')
        cmds.connectAttr(pick + '.outputMatrix', inverse + '.inputMatrix')
        cache[parent] = inverse
    return cache[parent]


def _rotation_only(matrix):
    return om.MMatrix([matrix[0], matrix[1], matrix[2], 0, matrix[4], matrix[5], matrix[6], 0,
                       matrix[8], matrix[9], matrix[10], 0, 0, 0, 0, 1])


def _constraint_target(joint):
    for constraint in cmds.listRelatives(joint, type='parentConstraint') or []:
        targets = cmds.parentConstraint(constraint, q=True, tl=True)
        if targets:
            return targets
    return []


def _world_scale(node):
    matrix = cmds.xform(node, q=True, ws=True, m=True)
    return om.MVector(matrix[0], matrix[1], matrix[2]).length()
