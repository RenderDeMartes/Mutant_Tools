from __future__ import absolute_import, division
from maya import cmds, mel
import maya.api.OpenMaya as om
import json
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import os
from pathlib import Path

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant

reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()

# ---------------------------------------------

TAB_FOLDER = '002_Biped'
PYBLOCK_NAME = 'exec_spine_v002'

GUIDE_LABELS = ['Root', 'Base', 'Belly', 'Chest', 'End']
JOINT_COUNTS = [3, 5, 7, 9, 11]
DEFAULT_JOINT_COUNT = 5

# Squash amount per guide position (Root..End), interpolated for in-between joints.
SQUASH_PROFILE = [0, 1, 0.5, 0.25, 0]

# ---------------------------------------------

def create_spine_block(name='Spine'):

    # Read name conventions as nc[''] and setup as seup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-3]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '001_Spine_v002.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()

    name = mt.ask_name(text=module['Name'])
    if cmds.objExists('{}{}'.format(name, nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name=name, icon='Spine', attrs=module['attrs'], build_command=module['build_command'],
                            import_command=module['import'])
    config = block[1]
    block = block[0]

    # enums default to their first entry, start on 5 joints like v001
    if cmds.attributeQuery('JointCount', n=config, exists=True):
        cmds.setAttr('{}.JointCount'.format(config), JOINT_COUNTS.index(DEFAULT_JOINT_COUNT))

    cmds.select(cl=True)
    spineRoot_guide = mt.create_joint_guide(name=name + '_Root')
    cmds.parent(spineRoot_guide, block)
    spineBase_guide = mt.create_joint_guide(name=name + '_Base')
    cmds.move(0, 2, 0)
    spineBelly_guide = mt.create_joint_guide(name=name + '_Belly')
    cmds.move(0, 4, 0)
    spineChest_guide = mt.create_joint_guide(name=name + '_Chest')
    cmds.move(0, 6, 0)
    spineEnd_guide = mt.create_joint_guide(name=name + '_End')
    cmds.move(0, 8, 0)

    cmds.parent(spineBase_guide, spineRoot_guide)
    cmds.parent(spineBelly_guide, spineBase_guide)
    cmds.parent(spineChest_guide, spineBelly_guide)
    cmds.parent(spineEnd_guide, spineChest_guide)

    cmds.select(block)

    print('{} Created Successfully'.format(name))


# create_spine_block()

# -------------------------
# Matrix helpers: everything below is driven with matrix nodes instead of constraints,
# they are cheaper to evaluate and keep the viewport fps up.

def _world(node):
    return om.MMatrix(cmds.xform(node, q=True, ws=True, m=True))


def _plug_matrix(plug):
    return om.MMatrix(cmds.getAttr(plug))


def _mult_matrix(name, items):
    """multMatrix of plugs and constant MMatrix values, in order. Returns the output plug."""
    node = cmds.createNode('multMatrix', n=name)
    for i, item in enumerate(items):
        if isinstance(item, om.MMatrix):
            cmds.setAttr('{}.matrixIn[{}]'.format(node, i), list(item), type='matrix')
        else:
            cmds.connectAttr(item, '{}.matrixIn[{}]'.format(node, i))
    return node + '.matrixSum'


def _carry(name, rest_world, driver_plug):
    """Matrix that follows driver_plug keeping the current offset (like a parentConstraint with mo)."""
    offset = rest_world * _plug_matrix(driver_plug).inverse()
    return _mult_matrix(name, [offset, driver_plug])


def _blend_matrix(name, input_plug, target_plug, weight):
    """Blend from input_plug (weight 0) to target_plug (weight 1)."""
    node = cmds.createNode('blendMatrix', n=name)
    cmds.connectAttr(input_plug, node + '.inputMatrix')
    cmds.connectAttr(target_plug, node + '.target[0].targetMatrix')
    if isinstance(weight, str):
        cmds.connectAttr(weight, node + '.target[0].weight')
    else:
        cmds.setAttr(node + '.target[0].weight', weight)
    return node + '.outputMatrix'


def _no_scale(name, plug):
    node = cmds.createNode('pickMatrix', n=name)
    cmds.connectAttr(plug, node + '.inputMatrix')
    cmds.setAttr(node + '.useScale', 0)
    cmds.setAttr(node + '.useShear', 0)
    return node + '.outputMatrix'


def _compose_translate(name, translate_plug):
    node = cmds.createNode('composeMatrix', n=name)
    cmds.connectAttr(translate_plug, node + '.inputTranslate')
    return node + '.outputMatrix'


def _zero_transform(node):
    cmds.xform(node, t=(0, 0, 0), ro=(0, 0, 0), s=(1, 1, 1), sh=(0, 0, 0))
    if cmds.nodeType(node) == 'joint':
        cmds.setAttr(node + '.jointOrient', 0, 0, 0)


def _drive_parent_space(node, world_plug, name):
    """Drive a node that lives under a parent from a world matrix, through offsetParentMatrix."""
    parent = cmds.listRelatives(node, p=True)[0]
    local = _mult_matrix(name, [world_plug, parent + '.worldInverseMatrix[0]'])
    _zero_transform(node)
    cmds.connectAttr(local, node + '.offsetParentMatrix', f=True)


def _scale_matrix(ctrl):
    node = ctrl + '_Scale_ComposeMatrix'
    if not cmds.objExists(node):
        cmds.createNode('composeMatrix', n=node)
        cmds.connectAttr(ctrl + '.scale', node + '.inputScale')
    return node + '.outputMatrix'


def _inverse_scale_matrix(ctrl):
    node = ctrl + '_InverseScale_ComposeMatrix'
    if not cmds.objExists(node):
        # clamp so scaling a controller to 0 never divides by zero
        clamp = cmds.createNode('clamp', n=ctrl + '_InverseScale_Clamp')
        cmds.setAttr(clamp + '.min', 0.001, 0.001, 0.001)
        cmds.setAttr(clamp + '.max', 1e6, 1e6, 1e6)
        cmds.connectAttr(ctrl + '.scale', clamp + '.input')
        divide = cmds.createNode('multiplyDivide', n=ctrl + '_InverseScale_MultiplyDivide')
        cmds.setAttr(divide + '.operation', 2)
        cmds.setAttr(divide + '.input1', 1, 1, 1)
        cmds.connectAttr(clamp + '.output', divide + '.input2')
        cmds.createNode('composeMatrix', n=node)
        cmds.connectAttr(divide + '.output', node + '.inputScale')
    return node + '.outputMatrix'


def _unscaled_world(ctrl):
    """World matrix of a controller without its own scale (its parents scale is kept)."""
    node = ctrl + '_Unscaled_MultMatrix'
    if cmds.objExists(node):
        return node + '.matrixSum'
    return _mult_matrix(node, [_inverse_scale_matrix(ctrl), ctrl + '.worldMatrix[0]'])


def _compensate_parent_scale(root):
    """Children ignore the scale of their parent controller, that scale only feeds the joints."""
    parent = cmds.listRelatives(root, p=True)[0]
    cmds.connectAttr(_inverse_scale_matrix(parent), root + '.offsetParentMatrix', f=True)


def _axis_map(ctrl_matrix, joint_matrix):
    """For every joint axis, the controller axis that points the same way at rest."""
    ctrl_axes = [om.MVector(ctrl_matrix[i * 4], ctrl_matrix[i * 4 + 1], ctrl_matrix[i * 4 + 2]).normal() for i in range(3)]
    joint_axes = [om.MVector(joint_matrix[i * 4], joint_matrix[i * 4 + 1], joint_matrix[i * 4 + 2]).normal() for i in range(3)]
    return [max(range(3), key=lambda k: abs(axis * ctrl_axes[k])) for axis in joint_axes]


def _follow_blend(node, driver_a, driver_b, weight, name):
    """World matrix blending between following driver_a (weight 0) and driver_b (weight 1)."""
    rest = _world(node)
    carry_a = _carry(name + '_A_MultMatrix', rest, _unscaled_world(driver_a))
    carry_b = _carry(name + '_B_MultMatrix', rest, _unscaled_world(driver_b))
    return _blend_matrix(name + '_BlendMatrix', carry_a, carry_b, weight)


def _lerp_profile(profile, g):
    low = min(int(g), len(profile) - 2)
    return profile[low] + (profile[low + 1] - profile[low]) * (g - low)


def _get_joint_count(config):
    if not cmds.attributeQuery('JointCount', n=config, exists=True):
        return DEFAULT_JOINT_COUNT
    return int(cmds.getAttr('{}.JointCount'.format(config), asString=True))


def _joint_layout(joint_count):
    """Guide-space position (0=Root .. 4=End) and label for every joint.
    Joints that land on a guide keep its name, in-betweens are MidXX."""
    layout = []
    mid = 0
    for j in range(joint_count):
        g = 4.0 * j / (joint_count - 1)
        if abs(g - round(g)) < 1e-6:
            label = GUIDE_LABELS[int(round(g))]
            g = float(round(g))
        else:
            mid += 1
            label = 'Mid{:02d}'.format(mid)
        layout.append((g, label))
    return layout

# -------------------------

def build_spine_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guide = cmds.listRelatives(block, c=True)[0]
    name = block.replace(nc['module'], '')

    ctrl_size = cmds.getAttr('{}.CtrlSize'.format(config))
    joint_count = _get_joint_count(config)
    if cmds.attributeQuery('Tweakers', n=config, exists=True):
        do_tweakers = cmds.getAttr(config + '.Tweakers')
    else:
        do_tweakers = False

    global_ctrl = 'Global' + nc['ctrl']
    twist_axis = setup['twist_axis'].upper()
    squash_axes = [a for a in 'XYZ' if a != twist_axis]

    # groups for later cleaning
    clean_ctrl_grp = cmds.group(em=True, name=name + nc['ctrl'] + nc['group'])
    clean_rig_grp = cmds.group(em=True, name=name + '_Rig' + nc['group'])

    # orient the joints
    mt.orient_joint(input=guide)
    new_guide = mt.duplicate_and_remove_guides(guide)

    cmds.setAttr('{}_End{}.jointOrientX'.format(name, nc['joint']), 0)
    cmds.setAttr('{}_End{}.jointOrientY'.format(name, nc['joint']), 0)
    cmds.setAttr('{}_End{}.jointOrientZ'.format(name, nc['joint']), 0)

    # use this locator in case parent is set to new locator
    if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
        block_parent = cmds.spaceLocator(n='{}'.format(str(block).replace(nc['module'], '_Parent' + nc['locator'])))[0]
    else:
        block_parent = cmds.getAttr('{}.SetParent'.format(config))

    game_parent = cmds.getAttr('{}.SetGameParent'.format(config))

    # oriented guide chain, only used as rest reference and deleted after the controls are placed
    spine_joints = ['{}_{}{}'.format(name, label, nc['joint']) for label in GUIDE_LABELS]
    spine_joints[0] = new_guide

    back_distance = cmds.getAttr(spine_joints[2] + '.translate' + twist_axis)
    guide_rest = [_world(jnt) for jnt in spine_joints]
    guide_pos = [cmds.xform(jnt, q=True, ws=True, t=True) for jnt in spine_joints]

    # build
    # create curve
    spine_cv = cmds.curve(d=3, p=guide_pos, k=[0, 0, 0, 1, 2, 2, 2], n=name + '_Main' + nc['curve'])
    spine_cv = cmds.rebuildCurve(keepRange=0, ch=False, rebuildType=3, kcp=1, kep=1, kt=0, s=4, d=3, tol=0.01)[0]
    spine_cv_shape = cmds.listRelatives(spine_cv, s=True)[0]
    cmds.setAttr('{}.inheritsTransform'.format(spine_cv), 0)

    # ik controllers drive the curve cvs directly
    spine_ik_ctrls = []
    for num, jnt in enumerate(spine_joints):
        ctrl = mt.curve(input=jnt,
                        type='sphere',
                        rename=True,
                        custom_name=True, name=jnt.replace(nc['joint'], '_IK' + nc['ctrl']),
                        size=ctrl_size / 2,
                        )
        cmds.delete(cmds.pointConstraint(jnt, ctrl))
        cmds.move(0, 0, back_distance, '{}.cv[0:101]'.format(ctrl), r=True)

        mt.assign_color(ctrl, 'yellow')
        mt.root_grp(input=ctrl)
        cv_decompose = cmds.createNode('decomposeMatrix', n=ctrl + '_CV_DecomposeMatrix')
        cmds.connectAttr('{}.worldMatrix[0]'.format(ctrl), '{}.inputMatrix'.format(cv_decompose))
        cmds.connectAttr('{}.outputTranslate'.format(cv_decompose), '{}.controlPoints[{}]'.format(spine_cv_shape, num))
        spine_ik_ctrls.append(ctrl)

    # Belly is going to be purple
    mt.assign_color(spine_ik_ctrls[2], 'purple')


    # Create FK controllers
    base_ik_ctrl = mt.curve(input=spine_joints[0],
                            type='pringle',
                            rename=True,
                            custom_name=True, name=name + '_Bottom_Ik' + nc['ctrl'],
                            size=ctrl_size * 1.5
                            )
    cmds.rotate(0, 0, 0)
    base_ik_ctrl_root = mt.root_grp()
    mt.assign_color(base_ik_ctrl, 'purple')
    mt.match(base_ik_ctrl_root, spine_joints[1], r=False)

    base_ctrl = mt.curve(input=spine_joints[1],
                         type='square',
                         rename=True,
                         custom_name=True, name=spine_joints[1].replace(nc['joint'], '_FK' + nc['ctrl']),
                         size=ctrl_size * 1.5
                         )
    cmds.rotate(0, 0, 0)
    base_ctrl_root = mt.root_grp()
    mt.assign_color(base_ctrl, 'lightBlue')
    mt.match(base_ctrl_root, spine_joints[1], r=False)

    belly_ctrl = mt.curve(input=spine_joints[2],
                          type='square',
                          rename=True,
                          custom_name=True, name=spine_joints[2].replace(nc['joint'], '_FK' + nc['ctrl']),
                          size=ctrl_size * 1.5
                          )
    cmds.rotate(0, 0, 0)
    belly_ctrl_root = mt.root_grp()
    mt.assign_color(belly_ctrl, 'lightBlue')
    mt.match(belly_ctrl_root, spine_joints[2], r=False)

    chest_ctrl_fk = mt.curve(input=spine_joints[3],
                          type='square',
                          rename=True,
                          custom_name=True, name=spine_joints[3].replace(nc['joint'], '_FK' + nc['ctrl']),
                          size=ctrl_size * 1.5
                          )
    cmds.rotate(0, 0, 0)
    chest_fk_ctrl_root = mt.root_grp()
    mt.assign_color(chest_ctrl_fk, 'green')
    mt.match(chest_fk_ctrl_root, spine_joints[3], r=False)

    chest_ctrl = mt.curve(input=spine_joints[4],
                          type='pringle',
                          rename=True,
                          custom_name=True, name=spine_joints[3].replace(nc['joint'], '_Top_IK' + nc['ctrl']),
                          size=ctrl_size * 1.5
                          )
    cmds.rotate(0, 0, 0)
    chest_ctrl_root = mt.root_grp()
    mt.assign_color(chest_ctrl, 'purple')
    mt.match(chest_ctrl_root, spine_joints[3], r=False)

    # Game Attrs Compatibility
    if cmds.attributeQuery('OrientToWorld', n=config, exists=True):
        orient_to_world = cmds.getAttr(config + '.OrientToWorld')
    else:
        orient_to_world = True

    if not orient_to_world:
        #FIX ORIENTS ONLY WHEN NEEDED TO MATCH GUIDE
        cmds.delete(cmds.aimConstraint(belly_ctrl, base_ik_ctrl_root,
            aimVector=(0, 1, 0), upVector=(0, 0, -1), worldUpType="scene")[0])
        cmds.delete(cmds.aimConstraint(belly_ctrl, base_ctrl_root,
                                       aimVector=(0, 1, 0), upVector=(0, 0, -1), worldUpType="scene")[0])
        cmds.delete(cmds.aimConstraint(chest_fk_ctrl_root, belly_ctrl_root,
                                       aimVector=(0, 1, 0), upVector=(0, 0, -1), worldUpType="scene")[0])
        cmds.delete(cmds.aimConstraint(belly_ctrl_root, chest_fk_ctrl_root,
                                       aimVector=(0, -1, 0), upVector=(0, 0, -1), worldUpType="scene")[0])
        cmds.delete(cmds.aimConstraint(belly_ctrl_root, chest_ctrl_root,
                                       aimVector=(0, -1, 0), upVector=(0, 0, -1), worldUpType="scene")[0])

    #Back to normal Build

    # Create hierarchy
    cmds.parent(belly_ctrl_root, base_ctrl)
    cmds.parent(chest_fk_ctrl_root, belly_ctrl)
    cmds.parent(chest_ctrl_root, chest_ctrl_fk)

    cmds.parent(cmds.listRelatives(spine_ik_ctrls[0], p=True), base_ik_ctrl)
    cmds.parent(cmds.listRelatives(spine_ik_ctrls[1], p=True), base_ik_ctrl)
    cmds.parent(cmds.listRelatives(spine_ik_ctrls[2], p=True), base_ctrl)
    cmds.parent(cmds.listRelatives(spine_ik_ctrls[3], p=True), chest_ctrl)
    cmds.parent(cmds.listRelatives(spine_ik_ctrls[4], p=True), chest_ctrl)
    cmds.parent(base_ik_ctrl_root, base_ctrl_root, clean_ctrl_grp)

    # controllers scale is faked: children do not inherit it, it gets added to the joints scale instead
    for root in [cmds.listRelatives(spine_ik_ctrls[0], p=True)[0], belly_ctrl_root[0],
                 cmds.listRelatives(spine_ik_ctrls[2], p=True)[0], chest_fk_ctrl_root[0], chest_ctrl_root[0],
                 cmds.listRelatives(spine_ik_ctrls[4], p=True)[0]]:
        _compensate_parent_scale(root)
    # a zero scale can not be compensated on the children, stop parent controllers just above it
    for ctrl in [base_ik_ctrl, base_ctrl, belly_ctrl, chest_ctrl_fk, chest_ctrl]:
        cmds.transformLimits(ctrl, sx=(0.001, 1), sy=(0.001, 1), sz=(0.001, 1),
                             esx=(True, False), esy=(True, False), esz=(True, False))
    ctrls_rest = {ctrl: _world(ctrl) for ctrl in spine_ik_ctrls + [base_ik_ctrl, base_ctrl, belly_ctrl,
                                                                   chest_ctrl_fk, chest_ctrl]}

    # Share attrs locator
    all_controllers = [chest_ctrl_fk, chest_ctrl, belly_ctrl, base_ctrl, base_ik_ctrl] + spine_ik_ctrls
    for ctrl in all_controllers:
        cmds.select(ctrl)
        spine_attrs_loc = mt.shape_with_attr(input='', obj_name='{}_Attrs'.format(name), attr_name='Test').split('.')[0]
    try:
        cmds.deleteAttr('{}.Test'.format(spine_attrs_loc))
    except:
        pass
    # shape_with_attr adds a generic 'MT' line, label it for the visibility attrs below it
    for attr in cmds.listAttr(spine_attrs_loc, ud=True) or []:
        if cmds.getAttr('{}.{}'.format(spine_attrs_loc, attr), type=True) == 'enum' and \
                cmds.attributeQuery(attr, n=spine_attrs_loc, listEnum=True) == ['MT']:
            cmds.setAttr('{}.{}'.format(spine_attrs_loc, attr), lock=False)
            cmds.addAttr('{}.{}'.format(spine_attrs_loc, attr), e=True, enumName='Visibility:')
            cmds.setAttr('{}.{}'.format(spine_attrs_loc, attr), lock=True)
    show_ik_ctrls_attr = mt.new_enum(input=spine_attrs_loc, name='ikCtrls', enums='Hide:Show', keyable=False)
    show_extra_ik_ctrls_attr = mt.new_enum(input=spine_attrs_loc, name='ikCtrlsExtra', enums='Hide:Show', keyable=False)
    show_fk_ctrls_attr = mt.new_enum(input=spine_attrs_loc, name='fkCtrls', enums='Hide:Show', keyable=False)
    cmds.setAttr(show_ik_ctrls_attr, 1)
    cmds.setAttr(show_extra_ik_ctrls_attr, 0)
    cmds.setAttr(show_fk_ctrls_attr, 1)
    if do_tweakers:
        show_tweak_ctrls_attr = mt.new_enum(input=spine_attrs_loc, name='tweakCtrls', enums='Hide:Show', keyable=False)
        cmds.setAttr(show_tweak_ctrls_attr, 0)

    for ctrl in spine_ik_ctrls[2:-2] + [base_ik_ctrl, chest_ctrl]:
        shape = cmds.listRelatives(ctrl, s=True)[0]
        cmds.connectAttr(show_ik_ctrls_attr, '{}.v'.format(shape))
    for ctrl in [spine_ik_ctrls[0], spine_ik_ctrls[-1], spine_ik_ctrls[1], spine_ik_ctrls[-2]]:
        shape = cmds.listRelatives(ctrl, s=True)[0]
        cmds.connectAttr(show_extra_ik_ctrls_attr, '{}.v'.format(shape), f=True)
    for ctrl in [belly_ctrl, base_ctrl, chest_ctrl_fk]:
        shape = cmds.listRelatives(ctrl, s=True)[0]
        cmds.connectAttr(show_fk_ctrls_attr, '{}.v'.format(shape))

    # Belly IK Ctrl offsets other Iks
    mt.line_attr(input=spine_attrs_loc, name='MidOffsets')

    mid01_attr = mt.new_attr(input=spine_attrs_loc, name='Mid02Follow', min=0, max=1, default=0.5)
    mid02_attr = mt.new_attr(input=spine_attrs_loc, name='Mid01Follow', min=0, max=1, default=0.5)

    base_mid_root = cmds.listRelatives(spine_ik_ctrls[1], p=True)[0]
    _drive_parent_space(base_mid_root,
                        _follow_blend(base_mid_root, spine_ik_ctrls[2], spine_ik_ctrls[0], mid02_attr,
                                      spine_ik_ctrls[1] + '_Follow'),
                        spine_ik_ctrls[1] + '_Follow_OffsetMatrix')

    chest_mid_root = cmds.listRelatives(spine_ik_ctrls[3], p=True)[0]
    _drive_parent_space(chest_mid_root,
                        _follow_blend(chest_mid_root, spine_ik_ctrls[4], spine_ik_ctrls[2], mid01_attr,
                                      spine_ik_ctrls[3] + '_Follow'),
                        spine_ik_ctrls[3] + '_Follow_OffsetMatrix')

    # Mid twist: belly ik root takes its Y rotation from a blend between bottom and top iks
    mt.line_attr(input=spine_attrs_loc, name='Twist')
    mid_twist_attr = mt.new_attr(input=spine_attrs_loc, name='MidTwist', min=0, max=1, default=0.5)

    belly_ik_root = cmds.listRelatives(spine_ik_ctrls[2], p=True)[0]
    mid_twist_world = _follow_blend(belly_ik_root, base_ik_ctrl, chest_ctrl, mid_twist_attr,
                                    spine_ik_ctrls[2] + '_MidTwist')
    belly_ik_parent = cmds.listRelatives(belly_ik_root, p=True)[0]
    mid_twist_local = _mult_matrix(spine_ik_ctrls[2] + '_MidTwist_Local_MultMatrix',
                                   [mid_twist_world, belly_ik_parent + '.worldInverseMatrix[0]',
                                    _scale_matrix(belly_ik_parent)])
    mid_twist_decompose = cmds.createNode('decomposeMatrix', n=spine_ik_ctrls[2] + '_MidTwist_DecomposeMatrix')
    cmds.connectAttr(mid_twist_local, mid_twist_decompose + '.inputMatrix')
    cmds.connectAttr(mid_twist_decompose + '.outputRotateY', belly_ik_root + '.rotateY')

    # global scale matrix, shared by everything that lives in world space
    global_scale_node = cmds.createNode('composeMatrix', n=name + '_GlobalScale_ComposeMatrix')
    cmds.connectAttr(global_ctrl + '.scale', global_scale_node + '.inputScale')
    global_scale = global_scale_node + '.outputMatrix'

    # ---------------------------------------------------------------------------------
    # Joints along the curve

    layout = _joint_layout(joint_count)

    # curve parameters of the guides, in-between joints interpolate them
    near_point_node = cmds.createNode('nearestPointOnCurve')
    cmds.connectAttr('{}.worldSpace[0]'.format(spine_cv_shape), '{}.inputCurve'.format(near_point_node))
    guide_params = []
    for pos in guide_pos:
        cmds.setAttr('{}.inPosition'.format(near_point_node), *pos)
        guide_params.append(cmds.getAttr('{}.result.parameter'.format(near_point_node)))
    cmds.delete(near_point_node)

    # rest of the guide chain is not needed anymore, joints get rebuilt flat with the same names
    cmds.delete(new_guide)

    joints_grp = cmds.group(em=True, n=name + '_Joints' + nc['group'], p=clean_rig_grp)
    cmds.setAttr(joints_grp + '.inheritsTransform', 0)

    driver_joints = []
    curve_points = []
    rest_matrices = []
    for g, label in layout:
        jnt = cmds.createNode('joint', n='{}_{}{}'.format(name, label, nc['joint']), p=joints_grp)
        driver_joints.append(jnt)

        poci = cmds.createNode('pointOnCurveInfo', n=jnt.replace(nc['joint'], '_POCI'))
        cmds.connectAttr('{}.worldSpace[0]'.format(spine_cv_shape), '{}.inputCurve'.format(poci))
        cmds.setAttr('{}.parameter'.format(poci), _lerp_profile(guide_params, g))
        curve_points.append(_compose_translate(jnt.replace(nc['joint'], '_POCI_ComposeMatrix'),
                                               poci + '.result.position'))

        # rest orientation from the guide segment, joints on a guide sit on the guide, in-betweens on the curve
        rest = om.MTransformationMatrix(guide_rest[min(int(g), 4)])
        if g == int(g):
            position = guide_pos[int(g)]
        else:
            position = cmds.getAttr(poci + '.result.position')[0]
        rest.setTranslation(om.MVector(*position), om.MSpace.kWorld)
        rest_matrices.append(rest.asMatrix())

    # Up vectors come from the orientation of bottom ik, belly ik and top ik (not from positions),
    # so moving the iks around never adds twist, only rotating them does.
    twist_anchors = {}
    for g_anchor, anchor in {0: base_ik_ctrl, 2: spine_ik_ctrls[2], 4: chest_ctrl}.items():
        twist_anchors[g_anchor] = _no_scale(anchor + '_Twist_PickMatrix', anchor + '.worldMatrix[0]')

    for j, (g, label) in enumerate(layout):
        jnt = driver_joints[j]

        if j == 0 or j == len(layout) - 1:
            # Root and End take their orientation from their ik controllers, no aim, so they can not flip
            ik_ctrl = spine_ik_ctrls[0] if j == 0 else spine_ik_ctrls[-1]
            source = _no_scale(jnt + '_PickMatrix', ik_ctrl + '.worldMatrix[0]')
        else:
            # up frame is world aligned at rest, -Z (back) is the up direction
            up_rest = om.MMatrix()
            low = 0 if g < 2 else 2
            carry_low = _carry(jnt + '_Up_A_MultMatrix', up_rest, twist_anchors[low])
            if g == low:
                up_plug = carry_low
            else:
                carry_high = _carry(jnt + '_Up_B_MultMatrix', up_rest, twist_anchors[low + 2])
                up_plug = _blend_matrix(jnt + '_Up_BlendMatrix', carry_low, carry_high, (g - low) / 2.0)

            aim = cmds.createNode('aimMatrix', n=jnt + '_AimMatrix')
            cmds.connectAttr(curve_points[j], aim + '.inputMatrix')
            cmds.connectAttr(curve_points[j + 1], aim + '.primaryTargetMatrix')
            cmds.connectAttr(up_plug, aim + '.secondaryTargetMatrix')
            cmds.setAttr(aim + '.primaryInputAxis', 0, 1, 0)
            cmds.setAttr(aim + '.secondaryInputAxis', 0, 0, -1)
            cmds.setAttr(aim + '.secondaryTargetVector', 0, 0, -1)
            cmds.setAttr(aim + '.primaryMode', 1)
            cmds.setAttr(aim + '.secondaryMode', 2)
            source = aim + '.outputMatrix'

        scaled_source = _mult_matrix(jnt + '_Scaled_MultMatrix', [global_scale, source])
        offset = rest_matrices[j] * _plug_matrix(scaled_source).inverse()
        world = _mult_matrix(jnt + '_World_MultMatrix', [offset, scaled_source])
        cmds.connectAttr(world, jnt + '.offsetParentMatrix')
        cmds.setAttr(jnt + '.radius', 1)

    # ---------------------------------------------------------------------------------
    # Volumen Preservation
    curve_info_node = cmds.createNode('curveInfo', n=name + '_CurveInfo')
    cmds.connectAttr('{}.worldSpace[0]'.format(spine_cv_shape), '{}.inputCurve'.format(curve_info_node))
    curve_lenght = cmds.getAttr('{}.arcLength'.format(curve_info_node))

    # rest length / current length, normalized by the global scale
    normal_md = cmds.createNode('multiplyDivide', n=name + '_Normalize')
    cmds.setAttr(normal_md + '.operation', 2)
    cmds.connectAttr(curve_info_node + '.arcLength', normal_md + '.input1X')
    cmds.connectAttr(global_ctrl + '.scaleX', normal_md + '.input2X')
    squash_md = cmds.createNode('multiplyDivide', n=name + '_Squash_MultiplyDivide')
    cmds.setAttr(squash_md + '.operation', 2)
    cmds.setAttr(squash_md + '.input1X', curve_lenght)
    cmds.connectAttr(normal_md + '.outputX', squash_md + '.input2X')

    mt.line_attr(input=spine_attrs_loc, name='Squash')

    squash_remaps = {}

    for (g, label), jnt in reversed(list(zip(layout, driver_joints))):
        clean_name = jnt.replace(name, '').replace(nc['joint'], '') + 'Squash'
        squash_attr = mt.new_attr(input=spine_attrs_loc, name=clean_name, min=0, max=1, default=1)
        cmds.setAttr(squash_attr, _lerp_profile(SQUASH_PROFILE, g))

        remap_node = cmds.createNode('remapValue', name=jnt + '_RemapValue')
        cmds.setAttr(remap_node + '.outputMin', 1)
        cmds.connectAttr(squash_md + '.outputX', remap_node + '.outputMax')
        cmds.connectAttr(squash_attr, remap_node + '.inputValue')
        squash_remaps[jnt] = remap_node

    # Controllers scale: every fk and ik controller scales the joints around it (falloff of one guide),
    # works with uniform and non uniform scale, controller axes are matched to the joint axes at rest.
    def scale_influences(g):
        influences = [(ctrl, 1 - abs(g - k)) for k, ctrl in enumerate(spine_ik_ctrls)]
        influences += [(ctrl, 1 - abs(g - k)) for k, ctrl in [(1, base_ctrl), (2, belly_ctrl), (3, chest_ctrl_fk)]]
        influences += [(base_ik_ctrl, min(1, 2 - g)), (chest_ctrl, min(1, g - 2))]
        return [(ctrl, weight) for ctrl, weight in influences if weight > 1e-4]

    scale_mds = {}
    for j, ((g, label), jnt) in enumerate(zip(layout, driver_joints)):
        product = None
        for num, (ctrl, weight) in enumerate(scale_influences(g)):
            axis_map = _axis_map(ctrls_rest[ctrl], rest_matrices[j])
            blend = cmds.createNode('blendColors', n='{}_Scale{:02d}_BlendColors'.format(jnt, num))
            for channel, ctrl_axis in zip('RGB', axis_map):
                cmds.connectAttr('{}.scale{}'.format(ctrl, 'XYZ'[ctrl_axis]), '{}.color1{}'.format(blend, channel))
                cmds.setAttr('{}.color2{}'.format(blend, channel), 1)
            cmds.setAttr(blend + '.blender', weight)
            if product is None:
                product = blend + '.output'
            else:
                mult = cmds.createNode('multiplyDivide', n='{}_Scale{:02d}_MultiplyDivide'.format(jnt, num))
                cmds.connectAttr(product, mult + '.input1')
                cmds.connectAttr(blend + '.output', mult + '.input2')
                product = mult + '.output'

        # controllers scale * squash
        scale_md = cmds.createNode('multiplyDivide', n=jnt + '_Scale_MultiplyDivide')
        cmds.connectAttr(product, scale_md + '.input1')
        for axis in 'XYZ':
            if axis in squash_axes:
                cmds.connectAttr(squash_remaps[jnt] + '.outColor.outColorR', '{}.input2{}'.format(scale_md, axis))
            else:
                cmds.setAttr('{}.input2{}'.format(scale_md, axis), 1)
        cmds.connectAttr(scale_md + '.output', jnt + '.scale')
        scale_mds[jnt] = scale_md

    # Auto Breath
    # compatible with older versions without ribbons
    if cmds.attributeQuery('Breath', n=config, exists=True):
        do_breath = cmds.getAttr(config + '.Breath')
    else:
        do_breath = False

    if do_breath:
        mt.line_attr(input=spine_attrs_loc, name='Breath')
        breath_auto = mt.new_attr(input=spine_attrs_loc, name='BreathAuto', min=0, max=1, default=0)
        breath_frequency = mt.new_attr(input=spine_attrs_loc, name='BreathFrequency', min=0, max=10,
                                       default=2.5)
        breath_amount = mt.new_attr(input=spine_attrs_loc, name='BreathAmount', min=0.1, max=10, default=1)
        breath_chest = mt.new_attr(input=spine_attrs_loc, name='BreathChest', min=0, max=10, default=1)
        breath_belly = mt.new_attr(input=spine_attrs_loc, name='BreathBelly', min=0, max=10, default=0.5)
        chest_rotate = mt.new_attr(input=spine_attrs_loc, name='ChestRotate', min=0, max=10, default=2.5)

        chest_offset = \
        mt.root_grp(input=chest_ctrl, custom=True, custom_name='{}_Chest_Breath_{}'.format(name, nc['group']))[0]

        def replace_connection_with_doublelinear(input='', attr='', name='DoubleLinear'):
            double_linear = mt.create_add_double_linear(name=name)
            input1_attr, input2_attr, output_attr = mt.get_add_double_linear_attrs(double_linear)
            cmds.setAttr('{}.{}'.format(double_linear, input1_attr), 1)
            cmds.connectAttr('{}.{}'.format(double_linear, output_attr), '{}.{}'.format(input, attr), f=True)
            return double_linear

        # belly always exists with an odd joint count, chest is the closest joint between belly and end
        belly_jnt = driver_joints[[label for g, label in layout].index('Belly')]
        chest_candidates = [(abs(g - 3), jnt) for (g, label), jnt in zip(layout, driver_joints) if 2 < g < 4]
        chest_jnt = min(chest_candidates)[1] if chest_candidates else None

        breath_lines = []
        for jnt, amount_attr, prefix in [(belly_jnt, breath_belly, 'Belly'), (chest_jnt, breath_chest, 'Chest')]:
            if not jnt:
                continue
            add_x = replace_connection_with_doublelinear(input=scale_mds[jnt], attr='input2' + twist_axis,
                                                         name=prefix + '_Breath_Add_X')
            add_yz = mt.replace_connection_with_doublelinear(input=scale_mds[jnt], attr='input2' + squash_axes[0],
                                                             name=prefix + '_Breath_Add_YZ')
            add_yz_output = mt.get_add_double_linear_attrs(add_yz)[2]
            cmds.connectAttr('{}.{}'.format(add_yz, add_yz_output), '{}.input2{}'.format(scale_mds[jnt], squash_axes[1]), f=True)
            for node in [add_x, add_yz]:
                breath_lines.append('{}.{} = $breath * 0.07 *{};'.format(
                    node, mt.get_add_double_linear_attrs(node)[1], amount_attr))

        # breathing expression
        breath_exp = cmds.expression(n=name + '_breath' + nc['expression'],
                                     s="""//Breath_attrs
                                            $freq = {}/2;
                                            $amount = {} * {};
                                            $breath = sin(time*$freq)*$amount;
                                            //Apply_it_to_the_nodes
                                            {}
                                            {}.rotateX = -1 * sin(time*$freq*$amount)*$amount*{}-{}/2;
                                            """.format(breath_frequency,
                                                       breath_amount,
                                                       breath_auto,
                                                       '\n'.join(breath_lines),
                                                       chest_offset, chest_rotate, chest_rotate
                                                       ).replace(' ', '')
                                     )

    # ---------------------------------------------------------------------------------
    # Tweakers: one extra controller per joint between the driver joints and the bind joints,
    # they move, rotate and scale each bind joint on its own.
    bind_sources = []
    tweak_ctrls = []
    if do_tweakers:
        tweakers_grp = cmds.group(em=True, n=name + '_Tweakers' + nc['group'], p=clean_ctrl_grp)
        cmds.setAttr(tweakers_grp + '.inheritsTransform', 0)

        for jnt in driver_joints:
            ctrl = mt.curve(input=jnt,
                            type='circle' + twist_axis,
                            rename=True,
                            custom_name=True, name=jnt.replace(nc['joint'], '_Tweak' + nc['ctrl']),
                            size=ctrl_size * 1.1
                            )
            mt.assign_color(ctrl, 'pink')
            tweak_root = mt.root_grp(input=ctrl)[0]
            cmds.parent(tweak_root, tweakers_grp)
            _zero_transform(tweak_root)
            # follow the driver joint without its squash scale, squash gets added back on the bind joint
            cmds.connectAttr(jnt + '.offsetParentMatrix', tweak_root + '.offsetParentMatrix')
            tweak_ctrls.append(ctrl)

            squash_scale = cmds.createNode('composeMatrix', n=jnt + '_Squash_ComposeMatrix')
            cmds.connectAttr(jnt + '.scale', squash_scale + '.inputScale')
            bind_sources.append(_mult_matrix(ctrl + '_Bind_MultMatrix',
                                             [squash_scale + '.outputMatrix', ctrl + '.worldMatrix[0]']))

        # share the attrs shape, no attr_name so no extra line gets added
        for ctrl in tweak_ctrls:
            cmds.select(ctrl)
            mt.shape_with_attr(input='', obj_name='{}_Attrs'.format(name), attr_name='')

        cmds.connectAttr(show_tweak_ctrls_attr, tweakers_grp + '.v')
    else:
        bind_sources = [jnt + '.worldMatrix[0]' for jnt in driver_joints]

    # bind joints, driven by decomposed matrices so the values stay on t/r/s for game export
    bind_joints = []
    for jnt, source in zip(driver_joints, bind_sources):
        parent = bind_joints[-1] if bind_joints else None
        bind_joint = cmds.createNode('joint', n=jnt.replace(nc['joint'], nc['joint_bind']), p=parent) if parent \
            else cmds.createNode('joint', n=jnt.replace(nc['joint'], nc['joint_bind']))
        cmds.setAttr('{}.segmentScaleCompensate'.format(bind_joint), 0)
        cmds.setAttr('{}.inheritsTransform'.format(bind_joint), 0)
        cmds.setAttr('{}.radius'.format(bind_joint), 2)

        decompose = cmds.createNode('decomposeMatrix', n=bind_joint + '_DecomposeMatrix')
        cmds.connectAttr(source, decompose + '.inputMatrix')
        cmds.connectAttr(bind_joint + '.rotateOrder', decompose + '.inputRotateOrder')
        cmds.connectAttr(decompose + '.outputTranslate', bind_joint + '.translate')
        cmds.connectAttr(decompose + '.outputRotate', bind_joint + '.rotate')
        cmds.connectAttr(decompose + '.outputScale', bind_joint + '.scale')
        bind_joints.append(bind_joint)

    # game parents for bind joints
    if cmds.objExists(game_parent):
        cmds.parent(bind_joints[0], game_parent)

    else:
        bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])
        if cmds.objExists(bind_jnt_grp):
            cmds.parent(bind_joints[0], bind_jnt_grp)

    # parent system
    cmds.parent(spine_cv, clean_rig_grp)

    cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
    cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])

    # follow the block parent (translate/rotate) and the global scale
    parent_follow = _mult_matrix(name + '_Parent_Scaled_MultMatrix',
                                 [global_scale, _no_scale(name + '_Parent_PickMatrix',
                                                          block_parent + '.worldMatrix[0]')])
    parent_follow = _mult_matrix(name + '_Parent_World_MultMatrix',
                                 [_world(clean_ctrl_grp) * _plug_matrix(parent_follow).inverse(), parent_follow])
    _drive_parent_space(clean_ctrl_grp, parent_follow, name + '_Parent_Local_MultMatrix')

    cmds.select(cl=True)
