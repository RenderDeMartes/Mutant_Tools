from __future__ import absolute_import, division
from maya import cmds
import maya.api.OpenMaya as om
import json
import math

try:
    import importlib; from importlib import reload
except Exception:
    import imp; from imp import reload

import os
import sys

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()

TAB_FOLDER = '002_Biped'
PYBLOCK_NAME = 'exec_leg_softik'

# -------------------------
# Leg Soft IK for Limb v002 legs (with the Foot block on top). Same math as the Limb v002 ArmsSoftIk:
#   softD = D                                  if D <= L - s
#           L - s * e^(-(D - (L - s)) / s)     if D >  L - s
#   no stretch: the IK handle is pulled back D - softD towards the hip, the leg eases to straight
#   stretch:    stretch starts at L - s with a D / softD factor, the foot stays on the controller
# D and L in the stretch units (the stretch Normalize node), L uses Upper/Lower_Length,
# s = SoftIk * 2% of L. Everything is found from the IK handle, nothing is hard coded.

SOFT_IK_RANGE = 0.02  # SoftIk 10 = soft zone of 20% of the leg length


def _limb():
    """Limb v002 node helpers (the soft IK uses the same small node builders)."""
    limb_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '004_Limb')
    if limb_folder not in sys.path:
        sys.path.append(limb_folder)
    import exec_limb_v002
    return exec_limb_v002


def _load_module_data():
    module_file = os.path.join(os.path.dirname(__file__), '013_LegSoftIK.json')
    with open(module_file) as module_handle:
        return json.load(module_handle)


def _stretch_data(ik_handle):
    """IK joints, distance shape, root / goal locators and stretch condition of a streatchy_ik leg."""
    start, mid = cmds.ikHandle(ik_handle, q=True, jointList=True)[:2]
    effector = cmds.ikHandle(ik_handle, q=True, endEffector=True)
    end = cmds.listConnections(effector + '.translateX', s=True, d=False)[0]
    ik_joints = [start, mid, end]

    distance = '{}_{}_Distance_Shape'.format(start, end)
    if not cmds.objExists(distance):
        return None
    locs = [cmds.listConnections('{}.{}'.format(distance, p), s=True, d=False)[0] for p in ('startPoint', 'endPoint')]
    # the goal locator is the one sitting on the ankle, the root one on the hip
    handle_pos = om.MVector(cmds.xform(ik_handle, q=True, ws=True, t=True))
    locs.sort(key=lambda loc: (om.MVector(cmds.xform(loc, q=True, ws=True, t=True)) - handle_pos).length())
    goal_loc, root_loc = locs

    normalize_md = [n for n in cmds.listConnections(distance + '.distance', s=False, d=True, type='multiplyDivide') or []
                    if 'Normalize' in n][0]
    condition = None
    for node in cmds.listConnections(normalize_md + '.outputX', s=False, d=True, type='multiplyDivide') or []:
        condition = (cmds.listConnections(node + '.outputX', s=False, d=True, type='condition') or [None])[0] or condition
    # stretch units -> world: the normalize divisor
    unit = (cmds.listConnections(normalize_md + '.input2X', s=True, d=False, p=True) or [None])[0]
    if unit is None:
        unit = cmds.getAttr(normalize_md + '.input2X')

    return {'ik_joints': ik_joints, 'distance': distance, 'root_loc': root_loc, 'goal_loc': goal_loc,
            'normalized': normalize_md + '.outputX', 'condition': condition, 'unit': unit}


def leg_soft_ik(name, ik_handle, data, soft_attr, upper_length, lower_length):
    limb = _limb()
    normalized, condition = data['normalized'], data['condition']

    # chain length with the length multipliers
    rest = [abs(cmds.getAttr(j + '.translateX')) for j in data['ik_joints'][1:]]
    chain = limb._add(name + '_Chain_AddDoubleLinear', limb._mult(name + '_Upper_MultDoubleLinear', upper_length, rest[0]),
                      limb._mult(name + '_Lower_MultDoubleLinear', lower_length, rest[1]))
    soft = limb._mult(name + '_Soft_MultDoubleLinear',
                      limb._mult(name + '_SoftRange_MultDoubleLinear', soft_attr, SOFT_IK_RANGE), chain)
    safe_soft = limb._clamp(name + '_SafeSoft_Clamp', soft, 1e-4, 1e6)
    threshold = limb._add(name + '_Threshold_AddDoubleLinear', chain, limb._mult(name + '_NegSoft_MultDoubleLinear', soft, -1))

    # chain - s * e^(-max(0, D - threshold) / s)
    over = limb._clamp(name + '_Over_Clamp', limb._add(name + '_Over_AddDoubleLinear', normalized,
                                                       limb._mult(name + '_NegThreshold_MultDoubleLinear', threshold, -1)), 0, 1e6)
    exponent = limb._mult(name + '_Exponent_MultDoubleLinear', limb._divide_scalar(name + '_Exponent_MultiplyDivide', over, safe_soft), -1)
    power = cmds.createNode('multiplyDivide', n=name + '_Exp_MultiplyDivide')
    cmds.setAttr(power + '.operation', 3)
    cmds.setAttr(power + '.input1X', math.e)
    cmds.connectAttr(exponent, power + '.input2X')
    soft_exp = limb._mult(name + '_SoftExp_MultDoubleLinear', soft, power + '.outputX')
    eased = limb._add(name + '_Eased_AddDoubleLinear', chain, limb._mult(name + '_NegSoftExp_MultDoubleLinear', soft_exp, -1))
    soft_on = cmds.createNode('condition', n=name + '_SoftOn_Condition')
    cmds.setAttr(soft_on + '.operation', 2)
    cmds.connectAttr(soft, soft_on + '.firstTerm')
    cmds.setAttr(soft_on + '.secondTerm', 1e-4)
    cmds.connectAttr(eased, soft_on + '.colorIfTrueR')
    cmds.connectAttr(chain, soft_on + '.colorIfFalseR')
    soft_dist = cmds.createNode('condition', n=name + '_SoftDist_Condition')
    cmds.setAttr(soft_dist + '.operation', 2)
    cmds.connectAttr(normalized, soft_dist + '.firstTerm')
    cmds.connectAttr(threshold, soft_dist + '.secondTerm')
    cmds.connectAttr(soft_on + '.outColorR', soft_dist + '.colorIfTrueR')
    cmds.connectAttr(normalized, soft_dist + '.colorIfFalseR')
    soft_dist += '.outColorR'

    # stretch: starts at the soft threshold, factor D / softD (with no soft it is the old D / L)
    cmds.connectAttr(threshold, condition + '.secondTerm', f=True)
    cmds.connectAttr(limb._divide_scalar(name + '_StretchFactor_MultiplyDivide', normalized, soft_dist),
                     condition + '.colorIfTrueR', f=True)
    # no stretch: pull the handle back D - softD towards the hip (the stretch condition picks it)
    cmds.connectAttr(limb._add(name + '_Pull_AddDoubleLinear', normalized,
                               limb._mult(name + '_NegSoftDist_MultDoubleLinear', soft_dist, -1)),
                     condition + '.colorIfFalseG', f=True)
    cmds.setAttr(condition + '.colorIfTrueG', 0)
    pull = limb._mult(name + '_PullWorld_MultDoubleLinear', condition + '.outColorG', data['unit'])

    # goal: where the handle sits under its parent (the foot RFL), moved back along hip -> goal
    parent = cmds.listRelatives(ik_handle, p=True)[0]
    rest_local = om.MTransformationMatrix()
    rest_local.setTranslation(om.MVector(cmds.getAttr(ik_handle + '.translate')[0]), om.MSpace.kTransform)
    goal = cmds.createNode('decomposeMatrix', n=name + '_Goal_DecomposeMatrix')
    cmds.connectAttr(limb._mult_matrix(name + '_Goal_MultMatrix', [rest_local.asMatrix(), parent + '.worldMatrix[0]']),
                     goal + '.inputMatrix')
    direction = cmds.createNode('vectorProduct', n=name + '_Direction_VectorProduct')
    cmds.setAttr(direction + '.operation', 0)
    cmds.setAttr(direction + '.normalizeOutput', 1)
    cmds.connectAttr(limb._vector_op(name + '_Direction_PlusMinusAverage', limb._world_position(data['goal_loc']),
                                     limb._world_position(data['root_loc']), 2), direction + '.input1')
    soft_goal = limb._vector_op(name + '_SoftGoal_PlusMinusAverage', goal + '.outputTranslate',
                                limb._vector_scale(name + '_Pull_MultiplyDivide', direction + '.output', pull), 2)
    compose = cmds.createNode('composeMatrix', n=name + '_SoftGoal_ComposeMatrix')
    cmds.connectAttr(soft_goal, compose + '.inputTranslate')
    limb._connect_channels(name, ik_handle, compose + '.outputMatrix', ['translateX', 'translateY', 'translateZ'], 'translate')


def create_leg_softik_block(name='LegSoftIK'):

    nc, curve_data, setup = mt.import_configs()
    module = _load_module_data()

    name = mt.ask_name(text=module['Name'])
    if not name:
        cmds.warning('Block creation cancelled: no name provided.')
        return ''

    if cmds.objExists('{}{}'.format(name, nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name=name,
                            icon='softIkLeg',
                            attrs=module['attrs'],
                            build_command=module['build_command'],
                            import_command=module['import'])

    cmds.select(block[0])
    print('{} Created Successfully'.format(name))
    return block[0]


def build_leg_softik_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    if not block:
        cmds.warning('Select a Leg Soft IK block to build.')
        return

    config = cmds.listConnections(block)[1]
    block = block[0]

    mirror = cmds.getAttr('{}.Mirror'.format(config), asString=True)
    ik_handle = cmds.getAttr('{}.LeftIKHandle'.format(config))
    holder = cmds.getAttr('{}.LeftSoftIkAttrHolder'.format(config))
    default = cmds.getAttr('{}.SoftIkDefault'.format(config)) if cmds.attributeQuery('SoftIkDefault', n=config, exists=True) else 0.5

    sides = {'True': [nc['left'], nc['right']], 'False': [nc['left']], 'Right_Only': [nc['right']]}.get(mirror, [nc['left']])
    for side in sides:
        side_handle, side_holder = ik_handle, holder
        if side == nc['right']:
            side_handle = ik_handle.replace(nc['left'], nc['right'], 1)
            side_holder = holder.replace(nc['left'], nc['right'], 1)

        missing = [n for n in (side_handle, side_holder) if not cmds.objExists(n)]
        if missing:
            cmds.warning('Leg Soft IK: skipping {}, missing {}'.format(side, missing))
            continue
        if cmds.listConnections(side_handle + '.translateX', s=True, d=False):
            cmds.warning('Leg Soft IK: {} translate is already driven (soft IK built, or the Foot block did not take '
                         'the handle from Limb v002), skipped'.format(side_handle))
            continue
        data = _stretch_data(side_handle)
        if not data or not data['condition']:
            cmds.warning('Leg Soft IK: {} has no Limb stretch setup, skipped'.format(side_handle))
            continue

        if cmds.attributeQuery('SoftIk', n=side_holder, exists=True):
            soft_attr = side_holder + '.SoftIk'
        else:
            mt.line_attr(input=side_holder, name='SoftIk')
            soft_attr = mt.new_attr(input=side_holder, name='SoftIk', min=0, max=10, default=default)

        name = side_handle.replace(nc['ik_rp'], '_SoftIk') if nc['ik_rp'] in side_handle else side_handle + '_SoftIk'
        leg_soft_ik(name, side_handle, data, soft_attr, side_holder + '.Upper_Length', side_holder + '.Lower_Length')
        print('Leg Soft IK built on {}'.format(side_handle))

    cmds.select(block)
