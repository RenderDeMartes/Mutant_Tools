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

#---------------------------------------------

TAB_FOLDER = '002_Biped'
PYBLOCK_NAME = 'exec_head_v003'

#---------------------------------------------

def create_head_block(name = 'Head'):
    # Read name conventions as nc[''] and setup as seup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-3]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '005_Head_v003.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()

    #name checks and block creation
    name = mt.ask_name(text = module['Name'], ask_for = 'Neck and Head Names (Separete with a , )')

    if cmds.objExists('{}{}'.format(name.replace(',','_'),nc['module'])):
        cmds.warning('Name already exists.')
        return ''


    block = mt.create_block(name = name, icon = 'HeadNeck',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]

    neck_name = name.split(',')[0]
    head_name = name.split(',')[1]

    cmds.select(cl=True)
    neck_guide = mt.create_joint_guide(name = neck_name)
    cmds.move(0,0,0)
    head_guide = mt.create_joint_guide(name = head_name)
    cmds.move(0,5,1.5)
    head_guideEnd = mt.create_joint_guide(name = head_name + 'End')
    cmds.move(0,8.5,1.5)

    cmds.parent(head_guideEnd, head_guide)
    cmds.parent(head_guide, neck_guide)
    cmds.parent(neck_guide, block)
    cmds.select(block)

    # Orient head guides: Y aims at child joint, X aims at world X
    cmds.makeIdentity(neck_guide, apply=True, t=True, r=True, s=True, n=False, pn=1)
    cmds.joint(neck_guide, e=True, oj='yxz', ch=True, secondaryAxisOrient='xup')
    cmds.setAttr("{}.jointOrientX".format(head_guideEnd), 0)
    cmds.setAttr("{}.jointOrientY".format(head_guideEnd), 0)
    cmds.setAttr("{}.jointOrientZ".format(head_guideEnd), 0)

    print('{} Created Successfully'.format(name))

#create_head_block()

#-------------------------
# Matrix helpers: everything is driven with matrix nodes instead of constraints, follicles or skinned
# surfaces, they are cheaper to evaluate and keep the viewport fps up (same idea as Spine v002).

def _world(node):
    return om.MMatrix(cmds.xform(node, q=True, ws=True, m=True))


def _plug_matrix(plug):
    return om.MMatrix(cmds.getAttr(plug))


def _translate_matrix(point):
    matrix = om.MTransformationMatrix()
    matrix.setTranslation(om.MVector(point), om.MSpace.kWorld)
    return matrix.asMatrix()


def _mult_matrix(name, items):
    """multMatrix of plugs and constant MMatrix values, in order. Returns the output plug."""
    node = cmds.createNode('multMatrix', n=name)
    for i, item in enumerate(items):
        if isinstance(item, om.MMatrix):
            cmds.setAttr('{}.matrixIn[{}]'.format(node, i), list(item), type='matrix')
        else:
            cmds.connectAttr(item, '{}.matrixIn[{}]'.format(node, i))
    return node + '.matrixSum'


def _pick(name, plug, translate=False, rotate=False, scale=False):
    """Only the asked parts of a matrix."""
    node = cmds.createNode('pickMatrix', n=name)
    cmds.connectAttr(plug, node + '.inputMatrix')
    cmds.setAttr(node + '.useTranslate', translate)
    cmds.setAttr(node + '.useRotate', rotate)
    cmds.setAttr(node + '.useScale', scale)
    cmds.setAttr(node + '.useShear', 0)
    return node + '.outputMatrix'


def _weighted_sum(name, items):
    """wtAddMatrix of (plug, weight) pairs. Used on translate only matrices, so the result is the
    weighted sum of their positions."""
    node = cmds.createNode('wtAddMatrix', n=name)
    for i, (plug, weight) in enumerate(items):
        cmds.connectAttr(plug, '{}.wtMatrix[{}].matrixIn'.format(node, i))
        cmds.setAttr('{}.wtMatrix[{}].weightIn'.format(node, i), weight)
    return node + '.matrixSum'


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


def _zero_transform(node):
    cmds.xform(node, t=(0, 0, 0), ro=(0, 0, 0), s=(1, 1, 1), sh=(0, 0, 0))
    if cmds.nodeType(node) == 'joint':
        cmds.setAttr(node + '.jointOrient', 0, 0, 0)


def _drive_parent_space(node, world_plug, name):
    """Drive a node that lives under a parent from a world matrix, through offsetParentMatrix.
    Uses the parent worldInverseMatrix, never the node own parentInverseMatrix (that makes a cycle)."""
    parent = cmds.listRelatives(node, p=True)[0]
    local = _mult_matrix(name, [world_plug, parent + '.worldInverseMatrix[0]'])
    _zero_transform(node)
    cmds.connectAttr(local, node + '.offsetParentMatrix', f=True)


def _drive_bind_joint(joint, world_plug):
    """Bind joints keep their values on t/r/s for game export: world matrix decomposed, no inherit."""
    cmds.setAttr(joint + '.inheritsTransform', 0)
    cmds.setAttr(joint + '.segmentScaleCompensate', 0)
    cmds.setAttr(joint + '.jointOrient', 0, 0, 0)
    decompose = cmds.createNode('decomposeMatrix', n=joint + '_DecomposeMatrix')
    cmds.connectAttr(world_plug, decompose + '.inputMatrix')
    # constant rotate order, connecting the joint own rotateOrder makes an evaluation cycle per joint
    cmds.setAttr(decompose + '.inputRotateOrder', cmds.getAttr(joint + '.rotateOrder'))
    cmds.connectAttr(decompose + '.outputTranslate', joint + '.translate')
    cmds.connectAttr(decompose + '.outputRotate', joint + '.rotate')
    cmds.connectAttr(decompose + '.outputScale', joint + '.scale')


def _carry(name, rest_world, driver_plug):
    """Matrix that follows driver_plug keeping the current offset (like a parentConstraint with mo)."""
    offset = rest_world * _plug_matrix(driver_plug).inverse()
    return _mult_matrix(name, [offset, driver_plug])


def _plug_or_value(node_attr, value):
    if isinstance(value, str):
        cmds.connectAttr(value, node_attr, f=True)
    else:
        cmds.setAttr(node_attr, value)


def _mult(name, a, b):
    node = cmds.createNode('multDoubleLinear', n=name)
    _plug_or_value(node + '.input1', a)
    _plug_or_value(node + '.input2', b)
    return node + '.output'


def _orient_matrix(rest_matrix, orients):
    """Rest world matrix of a controller. SN: aligned to the world like the spine controllers,
    Default: same axes as rest_matrix (the neck joint)."""
    position = om.MTransformationMatrix(rest_matrix).translation(om.MSpace.kWorld)
    if orients == 'SN':
        return _translate_matrix(position)
    return rest_matrix


def _create_ctrl(joint, name, curve_type, size, color, rest_matrix):
    """Controller at rest_matrix with its Offset_Grp on top."""
    cmds.select(joint)
    ctrl = mt.curve(input=joint, type=curve_type, custom_name=True, name=name, size=size)
    cmds.xform(ctrl, ws=True, m=list(rest_matrix))
    mt.assign_color(ctrl, color)
    mt.hide_attr(ctrl, v=True)
    offset_grp = mt.root_grp(input=ctrl, replace_nc=False)[0]
    return ctrl, offset_grp


def _attr_spec(node, attr):
    plug = '{}.{}'.format(node, attr)
    spec = {'type': cmds.attributeQuery(attr, n=node, attributeType=True),
            'keyable': cmds.getAttr(plug, keyable=True), 'channel_box': cmds.getAttr(plug, channelBox=True),
            'lock': cmds.getAttr(plug, lock=True), 'value': cmds.getAttr(plug),
            'default': cmds.attributeQuery(attr, n=node, listDefault=True)[0],
            'outputs': cmds.listConnections(plug, s=False, d=True, p=True) or [],
            'inputs': cmds.listConnections(plug, s=True, d=False, p=True) or []}
    if spec['type'] == 'enum':
        spec['enum'] = cmds.attributeQuery(attr, n=node, listEnum=True)[0]
    for key in ['min', 'max']:
        if cmds.attributeQuery(attr, n=node, **{key + 'Exists': True}):
            spec[key] = cmds.attributeQuery(attr, n=node, **{key: True})[0]
    return spec


def attrs_on_ctrls(holder, attrs, shape_name, ctrls):
    """Attrs on every controller, like the Limb v002 switch shape: the real attrs go to a data node (not in
    the hierarchy, no evaluation cycle) and a locator shape instanced under every controller keeps proxies
    of them, in the same order. The holder gets the shape too, so the attrs stay where they were."""
    data_node = cmds.createNode('network', n=shape_name + '_Data')
    specs = []
    for attr in attrs:
        spec = _attr_spec(holder, attr)
        kwargs = {'ln': attr, 'at': spec['type']}
        if spec['type'] == 'enum':
            kwargs['en'] = spec['enum']
        else:
            kwargs['dv'] = spec['default']
        for key in ['min', 'max']:
            if key in spec:
                kwargs[key] = spec[key]
        cmds.addAttr(data_node, **kwargs)
        cmds.setAttr('{}.{}'.format(data_node, attr), spec['value'])
        specs.append((attr, spec))
    for attr, spec in specs:
        cmds.setAttr('{}.{}'.format(holder, attr), lock=False)
        cmds.deleteAttr(holder, at=attr)

    shape = cmds.createNode('locator', n=shape_name, p=holder, skipSelect=True)
    for attr in ['lpx', 'lpy', 'lpz', 'lsx', 'lsy', 'lsz']:
        cmds.setAttr('{}.{}'.format(shape, attr), lock=True, channelBox=False, keyable=False)
    cmds.setAttr(shape + '.visibility', 0)
    for attr, spec in specs:
        source = '{}.{}'.format(data_node, attr)
        cmds.addAttr(shape, ln=attr, proxy=source)
        for plug in spec['inputs']:
            cmds.connectAttr(plug, source, f=True)
        for plug in spec['outputs']:
            cmds.connectAttr(source, plug, f=True)
        cmds.setAttr('{}.{}'.format(shape, attr), keyable=spec['keyable'])
        if not spec['keyable']:
            cmds.setAttr('{}.{}'.format(shape, attr), channelBox=spec['channel_box'])
        if spec['lock']:
            cmds.setAttr(source, lock=True)
    for ctrl in ctrls:
        if ctrl != holder:
            cmds.parent(shape, ctrl, s=True, add=True)
    return shape, data_node

#-------------------------

def build_head_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guide = cmds.listRelatives(block, c=True)[0]

    def get_attr(attr, default, as_string=False):
        # older blocks do not have the newer attrs
        if not cmds.attributeQuery(attr, n=config, exists=True):
            return default
        return cmds.getAttr('{}.{}'.format(config, attr), asString=as_string)

    #orient the joints: Y aims at child joint, X aims at world X
    cmds.makeIdentity(guide, apply=True, t=True, r=True, s=True, n=False, pn=1)
    cmds.joint(guide, e=True, oj='yxz', ch=True, secondaryAxisOrient='xup')
    # Zero out end joint orient (leaf has no child to aim at)
    end_jnt = cmds.listRelatives(cmds.listRelatives(guide, c=True)[0], c=True)
    if end_jnt:
        for attr in ['jointOrientX', 'jointOrientY', 'jointOrientZ']:
            cmds.setAttr('{}.{}'.format(end_jnt[0], attr), 0)
    new_guide = mt.duplicate_and_remove_guides(guide)

    #use this locator in case parent is set to new locator
    if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
        block_parent = cmds.spaceLocator( n = '{}'.format(str(block).replace(nc['module'],'_Parent' + nc['locator'])))[0]
    else:
        block_parent = cmds.getAttr('{}.SetParent'.format(config))

    #config--------------------------

    joint_count = max(1, int(round(cmds.getAttr('{}.SecundaryRibbon'.format(config)))))
    ctrl_type = cmds.getAttr('{}.HeadCtrlType'.format(config), asString = True)
    ctrl_size = cmds.getAttr('{}.CtrlSize'.format(config))
    ctrl_color = cmds.getAttr('{}.CtrlColor'.format(config), asString = True)
    game_parent = cmds.getAttr('{}.SetGameParent'.format(config), asString = True)

    # Ribbon off: no sub controllers, the neck joints only follow the curve
    sub_ctrls = get_attr('Ribbon', True)
    squash_stretch = get_attr('SquashStretch', True)
    # Default: Mutant orients (Neck_Ctrl along the neck), SN: studio orients (world aligned like the spine)
    orients = get_attr('Orients', 'Default', as_string=True)

    neck_joint = new_guide
    head_joint = cmds.listRelatives(neck_joint, c=True, type='joint')[0]
    name = str(neck_joint).replace(nc['joint'], '')

    neck_rest = _world(neck_joint)
    head_rest = _world(head_joint)
    neck_pos = om.MVector(cmds.xform(neck_joint, q=True, ws=True, t=True))
    head_pos = om.MVector(cmds.xform(head_joint, q=True, ws=True, t=True))
    rest_length = (head_pos - neck_pos).length()

    #groups ----------------------------
    clean_rig_grp = cmds.group(em=True, n = '{}{}'.format(block.replace(nc['module'],'_Rig'), nc['group']))
    cmds.parent(clean_rig_grp, setup['rig_groups']['misc']+ nc['group'])
    cmds.parent(neck_joint, clean_rig_grp)

    #Controllers ------------------------
    # Neck and Head FK, same names and groups as v002 (Offset > Ofset > Root > Auto > Ctrl)
    neck_ctrl, neck_offset_grp = _create_ctrl(neck_joint, '{}{}'.format(name, nc['ctrl']), ctrl_type, ctrl_size,
                                              ctrl_color, _orient_matrix(neck_rest, orients))
    # the head controller is world aligned in both orients (like v002)
    head_ctrl, head_offset_grp = _create_ctrl(head_joint, str(head_joint).replace(nc['joint'], nc['ctrl']), ctrl_type,
                                              ctrl_size, ctrl_color, _orient_matrix(head_rest, 'SN'))
    cmds.parent(head_offset_grp, neck_ctrl)
    # where the neck enters the head: rides Head_Ctrl, moving it changes that point without moving the head
    neck_end_ctrl, neck_end_offset_grp = _create_ctrl(head_joint, '{}_End{}'.format(name, nc['ctrl']), 'circleY',
                                                      ctrl_size * 0.85, ctrl_color, _orient_matrix(head_rest, 'SN'))
    cmds.parent(neck_end_offset_grp, head_ctrl)

    #blends#changed name to offset since blends are now a dif block
    mt.root_grp(input=neck_ctrl, custom=True, custom_name='_Ofset', autoRoot=False, replace_nc=False)
    mt.root_grp(input=head_ctrl, custom=True, custom_name='_Ofset', autoRoot=False, replace_nc=False)
    mt.root_grp(input=neck_ctrl, autoRoot=True)
    mt.root_grp(input=head_ctrl, autoRoot=True)
    mt.root_grp(input=neck_end_ctrl, autoRoot=True)

    cmds.parent(neck_offset_grp, setup['base_groups']['control'] + nc['group'])

    # follow the block parent (translate/rotate) and the rig scale, was a parent + scale constraint in v002
    rig_scale = _pick(name + '_RigScale_PickMatrix', 'Rig_Ctrl_Grp.worldMatrix[0]', scale=True)
    parent_follow = _mult_matrix(name + '_Parent_Scaled_MultMatrix',
                                 [rig_scale, _pick(name + '_Parent_PickMatrix', block_parent + '.worldMatrix[0]',
                                                   translate=True, rotate=True)])
    parent_follow = _carry(name + '_Parent_World_MultMatrix', _world(neck_offset_grp), parent_follow)
    _drive_parent_space(neck_offset_grp, parent_follow, name + '_Parent_Local_MultMatrix')

    neck_world = neck_ctrl + '.worldMatrix[0]'
    head_world = head_ctrl + '.worldMatrix[0]'
    neck_end_world = neck_end_ctrl + '.worldMatrix[0]'
    neck_ctrl_rest = _world(neck_ctrl)
    head_ctrl_rest = _world(head_ctrl)
    neck_end_ctrl_rest = _world(neck_end_ctrl)

    #Attrs ------------------------------
    # attrs Neck_Ctrl already has are not neck attrs (they stay on it)
    holder_attrs = set(cmds.listAttr(neck_ctrl, ud=True) or [])
    mt.line_attr(neck_ctrl, 'Neck')
    # Stretch 0: the neck keeps its length, the head joint stays on the line to Head_Ctrl
    stretch_attr = mt.new_attr(input=neck_ctrl, name='Stretch', min=0, max=1, default=1)
    # Neck_End_Ctrl rotation multiplier for the neck curve
    curve_attr = mt.new_attr(input=neck_ctrl, name='CurveAmount', min=0, max=5, default=2)
    volume_attr = None
    if squash_stretch:
        volume_attr = mt.new_attr(input=neck_ctrl, name='Volume', min=0, max=1, default=1)

    # SN rotate orders (what the Custom_Biped_Rotate_Orders block does for the neck and head)
    if orients == 'SN':
        for ctrl in [neck_ctrl, head_ctrl]:
            cmds.setAttr(ctrl + '.RotateOrder', 3)

    #Neck line --------------------------
    # translate only matrices, so weighted sums of them are positions
    def point(label, rest_point, driver_plug, driver_rest):
        carried = _mult_matrix('{}_{}_MultMatrix'.format(name, label),
                               [_translate_matrix(rest_point) * driver_rest.inverse(), driver_plug])
        return _pick('{}_{}_PickMatrix'.format(name, label), carried, translate=True)

    start = point('Start', neck_pos, neck_world, neck_ctrl_rest)
    # the neck goes to Neck_End_Ctrl (Head_Ctrl carries it)
    head_point = point('Head', head_pos, neck_end_world, neck_end_ctrl_rest)

    # length of the neck against its rest length in the current scale of the neck controller (global included)
    distance = cmds.createNode('distanceBetween', n=name + '_Length_DistanceBetween')
    cmds.connectAttr(start, distance + '.inMatrix1')
    cmds.connectAttr(head_point, distance + '.inMatrix2')
    safe_distance = cmds.createNode('clamp', n=name + '_Length_Clamp')
    cmds.setAttr(safe_distance + '.minR', 0.0001)
    cmds.setAttr(safe_distance + '.maxR', 1e9)
    cmds.connectAttr(distance + '.distance', safe_distance + '.inputR')
    neck_decompose = cmds.createNode('decomposeMatrix', n=name + '_NeckScale_DecomposeMatrix')
    cmds.connectAttr(neck_world, neck_decompose + '.inputMatrix')
    scaled_length = _mult(name + '_RestLength_MultDoubleLinear', neck_decompose + '.outputScaleY', rest_length)
    keep_length = cmds.createNode('multiplyDivide', n=name + '_KeepLength_MultiplyDivide')
    cmds.setAttr(keep_length + '.operation', 2)
    cmds.connectAttr(scaled_length, keep_length + '.input1X')
    cmds.connectAttr(safe_distance + '.outputR', keep_length + '.input2X')
    # how far the head joint goes on the line to Head_Ctrl: 1 with Stretch on, rest length / length with it off
    head_reach = cmds.createNode('blendTwoAttr', n=name + '_HeadReach_BlendTwoAttr')
    cmds.connectAttr(keep_length + '.outputX', head_reach + '.input[0]')
    cmds.setAttr(head_reach + '.input[1]', 1)
    cmds.connectAttr(stretch_attr, head_reach + '.attributesBlender')
    reach = head_reach + '.output'
    reach_reverse = cmds.createNode('reverse', n=name + '_HeadReach_Reverse')
    cmds.connectAttr(reach, reach_reverse + '.inputX')
    end = cmds.createNode('wtAddMatrix', n=name + '_End_WtAddMatrix')
    cmds.connectAttr(start, end + '.wtMatrix[0].matrixIn')
    cmds.connectAttr(reach_reverse + '.outputX', end + '.wtMatrix[0].weightIn')
    cmds.connectAttr(head_point, end + '.wtMatrix[1].matrixIn')
    cmds.connectAttr(reach, end + '.wtMatrix[1].weightIn')
    end = end + '.matrixSum'

    # head joint: Head_Ctrl, moved by what Stretch 0 takes off the neck end (none with Stretch on), so
    # Neck_End_Ctrl moves the neck end only
    head_inverse = cmds.createNode('inverseMatrix', n=name + '_Head_InverseMatrix')
    cmds.connectAttr(head_point, head_inverse + '.inputMatrix')
    head_source = _mult_matrix(str(head_joint) + '_World_MultMatrix',
                               [head_rest * head_ctrl_rest.inverse(), head_world,
                                head_inverse + '.outputMatrix', end])

    # twist goes from the neck to the head along the neck: rotation since rest of both controllers
    neck_delta = _mult_matrix(name + '_NeckDelta_MultMatrix', [neck_ctrl_rest.inverse(), neck_world])
    head_delta = _mult_matrix(name + '_HeadDelta_MultMatrix', [neck_end_ctrl_rest.inverse(), neck_end_world])
    neck_scale = _pick(name + '_NeckScale_PickMatrix', neck_world, scale=True)

    #Squash and stretch -----------------
    squash_matrices = [None, None]
    if squash_stretch:
        # length / rest length, the length the head joint really gets (Stretch off keeps it at 1)
        ratio = cmds.createNode('multiplyDivide', n=name + '_Stretch_MultiplyDivide')
        cmds.setAttr(ratio + '.operation', 2)
        cmds.connectAttr(safe_distance + '.outputR', ratio + '.input1X')
        cmds.connectAttr(scaled_length, ratio + '.input2X')
        ratio = _mult(name + '_Stretch_MultDoubleLinear', ratio + '.outputX', reach)
        # thinner when it stretches, thicker when it squashes: stretch ^ (-0.5 * Volume)
        # the first joint sits on the Neck guide, it gets half so it does not pop against the chest
        for i, amount in enumerate([-0.25, -0.5]):
            exponent = _mult('{}_Volume{}_MultDoubleLinear'.format(name, i), volume_attr, amount)
            power = cmds.createNode('multiplyDivide', n='{}_Volume{}_MultiplyDivide'.format(name, i))
            cmds.setAttr(power + '.operation', 3)
            cmds.connectAttr(ratio, power + '.input1X')
            cmds.connectAttr(exponent, power + '.input2X')
            compose = cmds.createNode('composeMatrix', n='{}_Volume{}_ComposeMatrix'.format(name, i))
            cmds.connectAttr(power + '.outputX', compose + '.inputScaleX')
            cmds.connectAttr(power + '.outputX', compose + '.inputScaleZ')
            squash_matrices[i] = compose + '.outputMatrix'

    #Neck_End_Ctrl curve and scale ------
    # its own rotation (not the head one, a head nod does not bow the neck) turns the end tangent of a
    # Bezier from the neck to the head: P1 stays on the straight line, P2 turns around Neck_End_Ctrl.
    # Straight at rest, so the joints sit where they did without it.
    end_local = neck_end_ctrl + '.matrix'
    end_pivot = _mult_matrix(name + '_EndPivot_MultMatrix',
                             [_pick(name + '_EndPivot_PickMatrix', end_local, translate=True),
                              neck_end_ctrl + '.parentMatrix[0]'])
    end_pivot_inverse = cmds.createNode('inverseMatrix', n=name + '_EndPivot_InverseMatrix')
    cmds.connectAttr(end_pivot, end_pivot_inverse + '.inputMatrix')
    straight_p2 = _weighted_sum(name + '_StraightP2_WtAddMatrix', [(start, 1.0 / 3), (end, 2.0 / 3)])
    # CurveAmount multiplies the Neck_End_Ctrl rotation that turns P2
    end_rotate = cmds.createNode('multiplyDivide', n=name + '_CurveAmount_MultiplyDivide')
    cmds.connectAttr(neck_end_ctrl + '.rotate', end_rotate + '.input1')
    for axis in 'XYZ':
        cmds.connectAttr(curve_attr, end_rotate + '.input2' + axis)
    end_rotation = cmds.createNode('composeMatrix', n=name + '_EndRotate_ComposeMatrix')
    cmds.connectAttr(end_rotate + '.output', end_rotation + '.inputRotate')
    cmds.connectAttr(neck_end_ctrl + '.rotateOrder', end_rotation + '.inputRotateOrder')
    p2 = _mult_matrix(name + '_P2_MultMatrix', [straight_p2, end_pivot_inverse + '.outputMatrix',
                                                end_rotation + '.outputMatrix', end_pivot])
    p2 = _pick(name + '_P2_PickMatrix', p2, translate=True)
    # its own scale scales the neck joints with a falloff, none on the first joint, more near the head
    end_scale = _pick(name + '_EndScale_PickMatrix', end_local, scale=True)

    #Neck frames ------------------------
    # joints are spread evenly from the Neck guide (first joint on it) to the Head guide (Head_Bnd),
    # on the Bezier, Y aims at the next joint (the last one at the head)
    positions = []
    for j in range(joint_count):
        t = float(j) / joint_count
        label = '{}_{}'.format(name, j + 1)
        # cubic Bezier weights with P1 = 2/3 start + 1/3 end
        b0, b1, b2, b3 = (1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t ** 2, t ** 3
        positions.append(_weighted_sum(label + '_Position_WtAddMatrix',
                                       [(start, b0 + b1 * 2.0 / 3), (end, b3 + b1 / 3.0), (p2, b2)]))

    frames = []
    for j in range(joint_count):
        t = float(j) / joint_count
        label = '{}_{}'.format(name, j + 1)
        position = positions[j]
        twist = _blend_matrix(label + '_Twist_BlendMatrix', neck_delta, head_delta, t)

        aim = cmds.createNode('aimMatrix', n=label + '_AimMatrix')
        cmds.connectAttr(position, aim + '.inputMatrix')
        cmds.setAttr(aim + '.primaryInputAxis', 0, 1, 0)
        cmds.setAttr(aim + '.primaryMode', 1)
        cmds.connectAttr(positions[j + 1] if j + 1 < joint_count else end, aim + '.primaryTargetMatrix')
        # Z keeps the neck joint Z, turned by the blended twist
        cmds.setAttr(aim + '.secondaryInputAxis', 0, 0, 1)
        cmds.setAttr(aim + '.secondaryMode', 2)
        cmds.setAttr(aim + '.secondaryTargetVector', *[neck_rest[8], neck_rest[9], neck_rest[10]])
        cmds.connectAttr(twist, aim + '.secondaryTargetMatrix')
        frame = aim + '.outputMatrix'

        frame_items = [neck_scale, frame]
        if t > 0:
            falloff = cmds.createNode('blendMatrix', n=label + '_EndScale_BlendMatrix')
            cmds.connectAttr(end_scale, falloff + '.target[0].targetMatrix')
            cmds.setAttr(falloff + '.target[0].weight', t)
            frame_items.insert(0, falloff + '.outputMatrix')
        frames.append(_mult_matrix(label + '_Frame_MultMatrix', frame_items))

    #Sub controllers --------------------
    ctrl_grp = cmds.group(em=True, n='{}{}{}'.format(name, nc['ctrl'], nc['group']), p=neck_ctrl)
    cmds.xform(ctrl_grp, ws=True, m=list(neck_ctrl_rest))
    sub_ctrl_list = []
    bind_sources = []
    for j, frame in enumerate(frames):
        frame_rest = _plug_matrix(frame)
        label = '{}_{}'.format(name, j + 1)
        squash = squash_matrices[0 if j == 0 else 1]
        if not sub_ctrls:
            source = frame
        else:
            ctrl, offset_grp = _create_ctrl(neck_joint, label + nc['ctrl'], 'circleY', ctrl_size * 0.75, ctrl_color,
                                            _orient_matrix(frame_rest, orients))
            cmds.parent(offset_grp, ctrl_grp)
            mt.root_grp(input=ctrl, autoRoot=True)
            ctrl_rest = _world(ctrl)
            # the controller rides its joint on the neck, its own moves go on top (tweaker)
            _drive_parent_space(offset_grp, _mult_matrix(label + '_Ctrl_World_MultMatrix',
                                                         [ctrl_rest * frame_rest.inverse(), frame]),
                                label + '_Ctrl_Local_MultMatrix')
            source = _mult_matrix(label + '_Bind_World_MultMatrix',
                                  [frame_rest * ctrl_rest.inverse(), ctrl + '.worldMatrix[0]'])
            sub_ctrl_list.append(ctrl)
        if squash:
            source = _mult_matrix(label + '_Squash_MultMatrix', [squash, source])
        bind_sources.append(source)

    #Rig joints -------------------------
    # Neck_Jnt and Head_Jnt follow the controllers, other blocks can parent to them
    _drive_parent_space(neck_joint, _carry(name + '_Jnt_World_MultMatrix', neck_rest, neck_world),
                        name + '_Jnt_Local_MultMatrix')
    _drive_parent_space(head_joint, head_source, str(head_joint) + '_Local_MultMatrix')
    cmds.setAttr('{}.segmentScaleCompensate'.format(head_joint), 0)

    #bind joints ------------------------
    bind_jnt_grp = cmds.group(em=True, n='{}{}'.format(block.replace(nc['module'], '_Bind'), nc['group']))
    if cmds.objExists(game_parent):
        cmds.parent(bind_jnt_grp, game_parent)
    else:
        cmds.parent(bind_jnt_grp, '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group']))

    bind_joints = []
    bind_names = ['{}_{}{}'.format(name, j + 1, nc['joint_bind']) for j in range(joint_count)]
    bind_names.append(str(head_joint).replace(nc['joint'], nc['joint_bind']))
    for bind_name, source in zip(bind_names, bind_sources + [head_source]):
        parent = bind_joints[-1] if bind_joints else bind_jnt_grp
        bind_joint = cmds.createNode('joint', n=bind_name, p=parent)
        cmds.setAttr('{}.radius'.format(bind_joint), 1.5)
        _drive_bind_joint(bind_joint, source)
        bind_joints.append(bind_joint)

    #Hide the subs controllers
    mt.line_attr(neck_ctrl, 'Sub')
    vis_attr = mt.new_enum(input=neck_ctrl, name='Vis', enums='Hide:Show', keyable=False, default=0)
    for ctrl in sub_ctrl_list:
        for shape in cmds.listRelatives(ctrl, s=True) or []:
            cmds.connectAttr(vis_attr, shape + '.v')
    if not sub_ctrl_list:
        cmds.delete(ctrl_grp)
    neck_end_vis = mt.new_enum(input=neck_ctrl, name='NeckEndVis', enums='Hide:Show', keyable=False, default=0)
    for shape in cmds.listRelatives(neck_end_ctrl, s=True) or []:
        cmds.connectAttr(neck_end_vis, shape + '.v')

    # neck attrs on every neck controller (instanced shape with proxies, like the Limb)
    neck_attrs = [attr for attr in cmds.listAttr(neck_ctrl, ud=True) or [] if attr not in holder_attrs]
    attrs_on_ctrls(neck_ctrl, neck_attrs, '{}_Attrs{}'.format(name, nc['locator']),
                   [head_ctrl, neck_end_ctrl] + sub_ctrl_list)

    cmds.select(cl=True)

    #-------------------------------------------------------
    #done
    print ('Build {} Success'.format(block))


#build_head_block()
