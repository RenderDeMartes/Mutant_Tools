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


def _plug_or_value(node_attr, value):
    if isinstance(value, str):
        cmds.connectAttr(value, node_attr, f=True)
    else:
        cmds.setAttr(node_attr, value)


def _mult(name, a, b):
    """a * b, plugs or numbers. Returns the output plug."""
    node = cmds.createNode('multDoubleLinear', n=name)
    _plug_or_value(node + '.input1', a)
    _plug_or_value(node + '.input2', b)
    return node + '.output'


def _add(name, a, b):
    node = cmds.createNode('addDoubleLinear', n=name)
    _plug_or_value(node + '.input1', a)
    _plug_or_value(node + '.input2', b)
    return node + '.output'


def _divide(name, a, b):
    node = cmds.createNode('multiplyDivide', n=name)
    cmds.setAttr(node + '.operation', 2)
    _plug_or_value(node + '.input1X', a)
    _plug_or_value(node + '.input2X', b)
    return node + '.outputX'


def _lerp(name, a, b, weight):
    """a when weight is 0, b when weight is 1 (plugs or numbers)."""
    node = cmds.createNode('blendTwoAttr', n=name)
    _plug_or_value(node + '.input[0]', a)
    _plug_or_value(node + '.input[1]', b)
    _plug_or_value(node + '.attributesBlender', weight)
    return node + '.output'


def _greater_pick(name, first, second, if_true, if_false):
    """if_true when first > second, else if_false (plugs or numbers)."""
    node = cmds.createNode('condition', n=name)
    cmds.setAttr(node + '.operation', 2)
    _plug_or_value(node + '.firstTerm', first)
    _plug_or_value(node + '.secondTerm', second)
    _plug_or_value(node + '.colorIfTrueR', if_true)
    _plug_or_value(node + '.colorIfFalseR', if_false)
    return node + '.outColorR'


def _no_twist_frame(ctrl, name, parent_plug=None):
    """Orientation of a controller without its own rotateY (twist), so twist can be read from the channel
    instead, which keeps going past 180 degrees."""
    compose = cmds.createNode('composeMatrix', n=name + '_NoTwist_ComposeMatrix')
    cmds.connectAttr(ctrl + '.rotateX', compose + '.inputRotateX')
    cmds.connectAttr(ctrl + '.rotateZ', compose + '.inputRotateZ')
    cmds.connectAttr(ctrl + '.rotateOrder', compose + '.inputRotateOrder')
    return _mult_matrix(name + '_NoTwist_MultMatrix',
                        [compose + '.outputMatrix', parent_plug or ctrl + '.parentMatrix[0]'])


def _dag_path(node):
    selection = om.MSelectionList()
    selection.add(node)
    return selection.getDagPath(0)


def _path_point(name, curve_shape, u_value):
    """World position at a fraction of the curve arc length (motionPath in fraction mode)."""
    motion_path = cmds.createNode('motionPath', n=name + '_MotionPath')
    cmds.connectAttr(curve_shape + '.worldSpace[0]', motion_path + '.geometryPath')
    cmds.setAttr(motion_path + '.fractionMode', 1)
    _plug_or_value(motion_path + '.uValue', u_value)
    return _compose_translate(name + '_Path_ComposeMatrix', motion_path + '.allCoordinates')


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

    # Pivot slide: moves the bottom/top ik rotate pivot towards the belly (1 = at the belly)
    for ctrl in [base_ik_ctrl, chest_ctrl]:
        pivot_attr = mt.new_attr(input=ctrl, name='PivotSlide', min=-1, max=1, default=0)
        to_belly = om.MPoint(*guide_pos[2]) * ctrls_rest[ctrl].inverse()
        pivot_md = cmds.createNode('multiplyDivide', n=ctrl + '_PivotSlide_MultiplyDivide')
        cmds.setAttr(pivot_md + '.input1', to_belly.x, to_belly.y, to_belly.z)
        for axis in 'XYZ':
            cmds.connectAttr(pivot_attr, '{}.input2{}'.format(pivot_md, axis))
        cmds.connectAttr(pivot_md + '.output', ctrl + '.rotatePivot')

    # Twist is read from the bottom/top ik rotateY channels so it keeps going past 180 degrees,
    # the belly ik gets a twist group driven by a blend of both channels.
    mt.line_attr(input=spine_attrs_loc, name='Twist')
    mid_twist_attr = mt.new_attr(input=spine_attrs_loc, name='MidTwist', min=0, max=1, default=0.5)

    belly_twist_grp = mt.root_grp(input=spine_ik_ctrls[2], custom=True,
                                  custom_name='{}_Belly_IK_Twist{}'.format(name, nc['group']))[0]
    cmds.connectAttr(_lerp(name + '_MidTwist_BlendTwoAttr', base_ik_ctrl + '.rotateY', chest_ctrl + '.rotateY',
                           mid_twist_attr), belly_twist_grp + '.rotateY')

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

    # rest of the guide chain is not needed anymore
    cmds.delete(new_guide)

    joints_grp = cmds.group(em=True, n=name + '_Joints' + nc['group'], p=clean_rig_grp)
    cmds.setAttr(joints_grp + '.inheritsTransform', 0)

    # Stretch and squash: SSMultiplier 0 keeps the spine length and volume, 1 is the normal effect and
    # higher values push the volume change further (length can not go past the curve). Joints sit at arc
    # length fractions of the curve, so when they do not stretch they slide along it.
    # one section for stretch and squash
    mt.line_attr(input=spine_attrs_loc, name='StretchSquash')
    ss_multiplier_attr = mt.new_attr(input=spine_attrs_loc, name='SSMultiplier', min=0, max=10, default=1)
    stretch_clamp = cmds.createNode('clamp', n=name + '_Stretch_Clamp')
    cmds.setAttr(stretch_clamp + '.maxR', 1)
    cmds.connectAttr(ss_multiplier_attr, stretch_clamp + '.inputR')
    stretch_attr = stretch_clamp + '.outputR'

    curve_info_node = cmds.createNode('curveInfo', n=name + '_CurveInfo')
    cmds.connectAttr('{}.worldSpace[0]'.format(spine_cv_shape), '{}.inputCurve'.format(curve_info_node))
    current_length = _divide(name + '_Normalize', curve_info_node + '.arcLength', global_ctrl + '.scaleX')
    rest_length = cmds.getAttr(current_length)

    stretched_length = _add(name + '_Stretch_Add', rest_length,
                            _mult(name + '_Stretch_Mult', _add(name + '_Excess_Add', current_length, -rest_length),
                                  stretch_attr))
    spine_length = _greater_pick(name + '_Stretch_Condition', current_length, rest_length,
                                 stretched_length, current_length)
    length_ratio = _divide(name + '_LengthRatio', spine_length, current_length)

    curve_fn = om.MFnNurbsCurve(_dag_path(spine_cv_shape))
    total_length = curve_fn.length()
    fractions = [curve_fn.findLengthFromParam(_lerp_profile(guide_params, g)) / total_length for g, label in layout]

    # driver joints (internal), the Spine_*_Jnt names are the output joints built at the end
    driver_joints = []
    curve_points = []
    ahead_points = []
    rest_matrices = []
    last = len(layout) - 1
    for j, (g, label) in enumerate(layout):
        jnt = cmds.createNode('joint', n='{}_{}_Drv{}'.format(name, label, nc['joint']), p=joints_grp)
        cmds.setAttr(jnt + '.drawStyle', 2)
        driver_joints.append(jnt)

        point = ahead = None
        if j > 0:
            u_value = _mult(jnt + '_U_Mult', length_ratio, fractions[j])
            point = _path_point(jnt, spine_cv_shape, u_value)
            if j < last:
                # a point a bit further along the curve gives the tangent, it keeps turning smoothly
                # even when the spine curls over itself
                ahead = _path_point(jnt + '_Ahead', spine_cv_shape, _add(jnt + '_Ahead_Add', u_value, 0.01))
        curve_points.append(point)
        ahead_points.append(ahead)

        # rest orientation from the guide segment, joints on a guide sit on the guide, in-betweens on the curve
        rest = om.MTransformationMatrix(guide_rest[min(int(g), 4)])
        if g == int(g):
            position = guide_pos[int(g)]
        else:
            position = cmds.getAttr(point.split('.')[0] + '.inputTranslate')[0]
        rest.setTranslation(om.MVector(*position), om.MSpace.kWorld)
        rest_matrices.append(rest.asMatrix())

    # Up vectors come from the orientation of bottom ik, belly ik and top ik without their own twist
    # (moving the iks never adds twist), the twist is added from their rotateY channels.
    twist_anchors = {0: _no_twist_frame(base_ik_ctrl, base_ik_ctrl),
                     2: _no_twist_frame(spine_ik_ctrls[2], spine_ik_ctrls[2], belly_twist_grp + '.parentMatrix[0]'),
                     4: _no_twist_frame(chest_ctrl, chest_ctrl)}
    twist_values = {0: base_ik_ctrl + '.rotateY',
                    2: _add(name + '_BellyTwist_Add', belly_twist_grp + '.rotateY', spine_ik_ctrls[2] + '.rotateY'),
                    4: chest_ctrl + '.rotateY'}

    for j, (g, label) in enumerate(layout):
        jnt = driver_joints[j]

        if j == 0:
            # Root takes its orientation from its ik controller, no aim, so it can not flip
            source = _no_scale(jnt + '_PickMatrix', spine_ik_ctrls[0] + '.worldMatrix[0]')
        elif j == last:
            # End: position along the curve (it respects Stretch), orientation from its ik controller
            rotation = cmds.createNode('pickMatrix', n=jnt + '_Rotate_PickMatrix')
            cmds.connectAttr(spine_ik_ctrls[-1] + '.worldMatrix[0]', rotation + '.inputMatrix')
            for flag in ['useTranslate', 'useScale', 'useShear']:
                cmds.setAttr('{}.{}'.format(rotation, flag), 0)
            source = _mult_matrix(jnt + '_End_MultMatrix', [rotation + '.outputMatrix', curve_points[j]])
        else:
            # up frame is world aligned at rest, -Z (back) is the up direction
            up_rest = om.MMatrix()
            low = 0 if g < 2 else 2
            carry_low = _carry(jnt + '_Up_A_MultMatrix', up_rest, twist_anchors[low])
            if g == low:
                up_plug = carry_low
                twist = twist_values[low]
            else:
                carry_high = _carry(jnt + '_Up_B_MultMatrix', up_rest, twist_anchors[low + 2])
                up_plug = _blend_matrix(jnt + '_Up_BlendMatrix', carry_low, carry_high, (g - low) / 2.0)
                twist = _lerp(jnt + '_Twist_BlendTwoAttr', twist_values[low], twist_values[low + 2], (g - low) / 2.0)

            aim = cmds.createNode('aimMatrix', n=jnt + '_AimMatrix')
            cmds.connectAttr(curve_points[j], aim + '.inputMatrix')
            cmds.connectAttr(ahead_points[j], aim + '.primaryTargetMatrix')
            cmds.connectAttr(up_plug, aim + '.secondaryTargetMatrix')
            cmds.setAttr(aim + '.primaryInputAxis', 0, 1, 0)
            cmds.setAttr(aim + '.secondaryInputAxis', 0, 0, -1)
            cmds.setAttr(aim + '.secondaryTargetVector', 0, 0, -1)
            cmds.setAttr(aim + '.primaryMode', 1)
            cmds.setAttr(aim + '.secondaryMode', 2)

            # twist around the aim axis
            twist_compose = cmds.createNode('composeMatrix', n=jnt + '_Twist_ComposeMatrix')
            cmds.connectAttr(twist, twist_compose + '.inputRotateY')
            source = _mult_matrix(jnt + '_Twist_MultMatrix', [twist_compose + '.outputMatrix', aim + '.outputMatrix'])

        scaled_source = _mult_matrix(jnt + '_Scaled_MultMatrix', [global_scale, source])
        offset = rest_matrices[j] * _plug_matrix(scaled_source).inverse()
        world = _mult_matrix(jnt + '_World_MultMatrix', [offset, scaled_source])
        cmds.connectAttr(world, jnt + '.offsetParentMatrix')
        cmds.setAttr(jnt + '.radius', 1)

    # ---------------------------------------------------------------------------------
    # Volumen Preservation: scale = (rest length / length) ^ (joint squash * SSMultiplier)
    squash_ratio = _divide(name + '_Squash_Ratio', rest_length, spine_length)


    squash_powers = {}
    for (g, label), jnt in reversed(list(zip(layout, driver_joints))):
        squash_attr = mt.new_attr(input=spine_attrs_loc, name='_{}Squash'.format(label), min=0, max=1, default=1)
        cmds.setAttr(squash_attr, _lerp_profile(SQUASH_PROFILE, g))

        power = cmds.createNode('multiplyDivide', n='{}_{}_Squash_Power'.format(name, label))
        cmds.setAttr(power + '.operation', 3)
        cmds.connectAttr(squash_ratio, power + '.input1X')
        cmds.connectAttr(_mult('{}_{}_Squash_Mult'.format(name, label), squash_attr, ss_multiplier_attr),
                         power + '.input2X')
        squash_powers[jnt] = power + '.outputX'

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
                cmds.connectAttr(squash_powers[jnt], '{}.input2{}'.format(scale_md, axis))
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

        breath_targets = []
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
                breath_targets.append(('{}.{}'.format(node, mt.get_add_double_linear_attrs(node)[1]), amount_attr))

        # breathing with math nodes, an expression would slow down and break parallel evaluation
        try:
            sin_test = cmds.createNode('sin')
            cmds.delete(sin_test)
            has_sin_node = True
        except RuntimeError:
            has_sin_node = False

        if has_sin_node:
            def sin_degrees(node_name, degrees_plug):
                node = cmds.createNode('sin', n=node_name)
                cmds.connectAttr(degrees_plug, node + '.input')
                return node + '.output'

            # time1 comes in frames, the breath is tuned in seconds
            seconds = _divide(name + '_Breath_Seconds', 'time1.outTime', mel.eval('currentTimeUnitToFPS()'))
            frequency = _mult(name + '_Breath_Frequency', breath_frequency, 0.5)
            amount = _mult(name + '_Breath_Amount', breath_amount, breath_auto)
            # the sin node works in degrees
            phase = _mult(name + '_Breath_Phase_Degrees',
                          _mult(name + '_Breath_Phase', seconds, frequency), 57.2957795)
            breath_value = _mult(name + '_Breath_Value', sin_degrees(name + '_Breath_Sin', phase), amount)
            breath_value = _mult(name + '_Breath_Scaled', breath_value, 0.07)
            for num, (target, amount_attr) in enumerate(breath_targets):
                cmds.connectAttr(_mult('{}_Breath_Target{:02d}_Mult'.format(name, num), breath_value, amount_attr),
                                 target, f=True)

            chest_sin = sin_degrees(name + '_ChestBreath_Sin', _mult(name + '_ChestBreath_Phase', phase, amount))
            chest_rotation = _mult(name + '_ChestBreath_Rotate',
                                   _mult(name + '_ChestBreath_Amount', chest_sin, amount), chest_rotate)
            cmds.connectAttr(_mult(name + '_ChestBreath_Negate', chest_rotation, -1), chest_offset + '.rotateX')
        else:
            breath_lines = ['{} = $breath * 0.07 *{};'.format(target, amount_attr)
                            for target, amount_attr in breath_targets]
            breath_exp = cmds.expression(n=name + '_breath' + nc['expression'],
                                         s="""//Breath_attrs
                                                $freq = {}/2;
                                                $amount = {} * {};
                                                $breath = sin(time*$freq)*$amount;
                                                //Apply_it_to_the_nodes
                                                {}
                                                {}.rotateX = -1 * sin(time*$freq*$amount)*$amount*{};
                                                """.format(breath_frequency,
                                                           breath_amount,
                                                           breath_auto,
                                                           '\n'.join(breath_lines),
                                                           chest_offset, chest_rotate
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

        for (g, label), jnt in zip(layout, driver_joints):
            ctrl = mt.curve(input=jnt,
                            type='circle' + twist_axis,
                            rename=True,
                            custom_name=True, name='{}_{}_Tweak{}'.format(name, label, nc['ctrl']),
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
    for (g, label), source in zip(layout, bind_sources):
        parent = bind_joints[-1] if bind_joints else None
        bind_name = '{}_{}{}'.format(name, label, nc['joint_bind'])
        bind_joint = cmds.createNode('joint', n=bind_name, p=parent) if parent else cmds.createNode('joint', n=bind_name)
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

    # output joints: same result as the bind joints (tweakers and controllers scale included),
    # other blocks parent to these (Spine_End_Jnt...) so they follow everything the spine does
    output_joints = []
    for (g, label), source in zip(layout, bind_sources):
        output_joint = cmds.createNode('joint', n='{}_{}{}'.format(name, label, nc['joint']), p=joints_grp)
        cmds.connectAttr(source, output_joint + '.offsetParentMatrix')
        cmds.setAttr(output_joint + '.radius', 1)
        output_joints.append(output_joint)

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
