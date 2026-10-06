from __future__ import absolute_import, division
from maya import cmds
import maya.mel as mel
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

# ---------------------------------------------

TAB_FOLDER = '002_Biped'
PYBLOCK_NAME = 'exec_head'


def create_limb_block(name='Limb'):

    nc, curve_data, setup = mt.import_configs()

    # Read name conventions as nc[''] and setup as seup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-3]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '004_Limb.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    # name checks and block creation
    name = mt.ask_name(text=module['Name'],
                       ask_for='Limb Names (Separete with a , ), Needs to start with L_ or R_ ',
                       check_split=True)

    if cmds.objExists('{}{}'.format(name.split(',')[0], nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    limb_block = mt.create_block(name=name.split(',')[0], icon='Limb', attrs=module['attrs'],
                                 build_command=module['build_command'], import_command=module['import'])
    limb_config = limb_block[1]
    limb_block = limb_block[0]

    name = name.split(',')
    # limb base create
    cmds.select(cl=True)
    joint_one = mt.create_joint_guide(name=name[0])
    cmds.move(5, 0, 0)
    joint_two = mt.create_joint_guide(name=name[1])
    cmds.move(15, 0, -1)
    joint_three = mt.create_joint_guide(name=name[2])
    cmds.move(25, 0, 0)
    cmds.parent(joint_three, joint_two)
    cmds.parent(joint_two, joint_one)

    cmds.parent(joint_one, limb_block)

    cmds.select()
    mt.orient_joint(input=joint_one)
    mt.orient_joint(input=joint_two)
    mt.orient_joint(input=joint_three)

    cmds.select(limb_block)

    cmds.setAttr("{}.jointOrientX".format(joint_three), 0)
    cmds.setAttr("{}.jointOrientY".format(joint_three), 0)
    cmds.setAttr("{}.jointOrientZ".format(joint_three), 0)

    print('Limb Base Created Successfully'),


# create_limb_base()

# -------------------------
# Matrix helpers: the limb is built with the shared kinematics tools (constraints), then every
# constraint the block made is swapped for matrix nodes, they are cheaper to evaluate and keep the
# viewport fps up. The swap keeps the result on the same translate/rotate/scale channels, so
# anything reading them (ik fk blend, twist readers, aim locators) keeps working.

CONSTRAINT_TYPES = ['parentConstraint', 'pointConstraint', 'orientConstraint', 'scaleConstraint', 'aimConstraint']
AXES = 'XYZ'


def _world(node):
    return om.MMatrix(cmds.getAttr(node + '.worldMatrix[0]'))


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


def _pick_matrix(name, plug, translate=True, rotate=True):
    node = cmds.createNode('pickMatrix', n=name)
    cmds.connectAttr(plug, node + '.inputMatrix')
    cmds.setAttr(node + '.useTranslate', translate)
    cmds.setAttr(node + '.useRotate', rotate)
    cmds.setAttr(node + '.useScale', 0)
    cmds.setAttr(node + '.useShear', 0)
    return node + '.outputMatrix'


def _only_translate(matrix):
    return om.MMatrix(om.MTransformationMatrix().setTranslation(
        om.MTransformationMatrix(matrix).translation(om.MSpace.kWorld), om.MSpace.kWorld).asMatrix())


def _only_rotate(matrix):
    return om.MTransformationMatrix().setRotation(om.MTransformationMatrix(matrix).rotation(asQuaternion=True)).asMatrix()


def _has_offsets(node):
    """Pivots or rotate axis change how channels map to the matrix, those nodes keep their constraint."""
    for attr in ['rotatePivot', 'rotatePivotTranslate', 'scalePivot', 'scalePivotTranslate', 'rotateAxis']:
        if any(abs(v) > 1e-6 for v in cmds.getAttr('{}.{}'.format(node, attr))[0]):
            return True
    return False


def _constraint_info(con):
    con_type = cmds.nodeType(con)
    query = getattr(cmds, con_type)
    targets = query(con, q=True, targetList=True) or []
    aliases = query(con, q=True, weightAliasList=True) or []
    if any(cmds.listConnections('{}.{}'.format(con, a), s=True, d=False) for a in aliases):
        return None  # animated weights (switches) stay as constraints
    weights = [cmds.getAttr('{}.{}'.format(con, a)) for a in aliases]

    driven = None
    channels = []
    outputs = cmds.listConnections(con, s=False, d=True, p=True, c=True) or []
    for src, dst in zip(outputs[::2], outputs[1::2]):
        node = dst.split('.')[0]
        if node == con or not src.split('.')[-1].startswith('constraint'):
            continue
        driven = node
        channels.append(cmds.attributeName(dst, l=True))
    if not driven or not targets:
        return None

    active = [(t, w) for t, w in zip(targets, weights) if w > 1e-6]
    if not active or _has_offsets(driven):
        return None
    if any(any(abs(v) > 1e-6 for v in cmds.getAttr(t + '.rotatePivot')[0]) for t, w in active):
        return None
    if len(active) > 2 or (len(active) > 1 and (con_type != 'parentConstraint' or
                                                 any(c.startswith('rotate') for c in channels))):
        return None

    return {'con': con, 'type': con_type, 'driven': driven, 'channels': channels, 'targets': active}


def _parent_space_for_rotate(driven):
    """Joints under a joint with segmentScaleCompensate ignore the parent scale (world = S R JO IS T P),
    so their rotation is read with the parent scale added back."""
    items = [driven + '.parentInverseMatrix[0]']
    parent = (cmds.listRelatives(driven, p=True) or [None])[0]
    if (cmds.nodeType(driven) == 'joint' and parent and cmds.nodeType(parent) == 'joint'
            and cmds.getAttr(driven + '.segmentScaleCompensate')):
        node = parent + '_Scale_ComposeMatrix'
        if not cmds.objExists(node):
            cmds.createNode('composeMatrix', n=node)
            cmds.connectAttr(parent + '.scale', node + '.inputScale')
        items.append(node + '.outputMatrix')
    return items


def _connect_channels(name, driven, world_plug, channels, kind, post=None):
    """Decompose a world matrix onto the driven channels of one kind (translate / rotate)."""
    wanted = [c for c in channels if c.startswith(kind)]
    if not wanted:
        return
    if kind == 'rotate':
        items = [world_plug] + _parent_space_for_rotate(driven)
        # mirrored nodes (negative scale) would get the flip as a 180 rotation, take their own scale out first
        scale = cmds.getAttr(driven + '.scale')[0]
        if any(v < 0 for v in scale):
            own_scale = om.MTransformationMatrix()
            own_scale.setScale(scale, om.MSpace.kTransform)
            items.insert(0, own_scale.asMatrix().inverse())
        if cmds.nodeType(driven) == 'joint':
            joint_orient = cmds.getAttr(driven + '.jointOrient')[0]
            if any(abs(v) > 1e-6 for v in joint_orient):
                orient = om.MEulerRotation([om.MAngle(v, om.MAngle.kDegrees).asRadians() for v in joint_orient])
                items.append(orient.asMatrix().inverse())
    else:
        items = [world_plug, driven + '.parentInverseMatrix[0]']
    if post is not None:
        items.append(post)
    local_plug = _mult_matrix('{}_{}_MultMatrix'.format(name, kind.capitalize()), items)
    decompose = cmds.createNode('decomposeMatrix', n='{}_{}_DecomposeMatrix'.format(name, kind.capitalize()))
    cmds.connectAttr(local_plug, decompose + '.inputMatrix')
    cmds.connectAttr(driven + '.rotateOrder', decompose + '.inputRotateOrder')
    out = {'translate': 'outputTranslate', 'rotate': 'outputRotate'}[kind]
    for channel in wanted:
        axis = channel[-1]
        cmds.connectAttr('{}.{}{}'.format(decompose, out, axis), '{}.{}'.format(driven, channel), f=True)


def _build_matrix_network(info, unscaled_targets=()):
    """Rest offsets are read now (the rig is in rest pose), so call this before deleting the constraint."""
    con_type, driven, channels = info['type'], info['driven'], info['channels']
    name = info['con']
    rest_world = _world(driven)
    rest_pim = _plug_matrix(driven + '.parentInverseMatrix[0]')
    pim = driven + '.parentInverseMatrix[0]'

    if con_type == 'parentConstraint':
        carries = []
        for num, (target, weight) in enumerate(info['targets']):
            offset = rest_world * _world(target).inverse()
            # scaled controllers only pass their scale to the joints, not to what follows them
            target_plug = _unscaled_world(target) if target in unscaled_targets else target + '.worldMatrix[0]'
            carries.append(_mult_matrix('{}_{}_MultMatrix'.format(name, num), [offset, target_plug]))
        world = carries[0]
        if len(carries) == 2:
            w0, w1 = info['targets'][0][1], info['targets'][1][1]
            blend = cmds.createNode('blendMatrix', n=name + '_BlendMatrix')
            cmds.connectAttr(carries[0], blend + '.inputMatrix')
            cmds.connectAttr(carries[1], blend + '.target[0].targetMatrix')
            cmds.setAttr(blend + '.target[0].weight', w1 / (w0 + w1))
            world = blend + '.outputMatrix'
        jobs = [(world, 'translate', None), (world, 'rotate', None)]

    elif con_type == 'pointConstraint':
        target = info['targets'][0][0]
        position = _pick_matrix(name + '_PickMatrix', target + '.worldMatrix[0]', rotate=False)
        rest_local = om.MTransformationMatrix(_only_translate(_world(target)) * rest_pim).translation(om.MSpace.kWorld)
        current = om.MVector(cmds.getAttr(driven + '.translate')[0])
        offset = om.MTransformationMatrix().setTranslation(current - rest_local, om.MSpace.kWorld).asMatrix()
        jobs = [(position, 'translate', offset)]

    elif con_type == 'orientConstraint':
        target = info['targets'][0][0]
        offset = _only_rotate(rest_world) * _only_rotate(_world(target)).inverse()
        rotation = _pick_matrix(name + '_PickMatrix', target + '.worldMatrix[0]', translate=False)
        world = _mult_matrix(name + '_World_MultMatrix', [offset, rotation])
        jobs = [(world, 'rotate', None)]

    elif con_type == 'scaleConstraint':
        target = info['targets'][0][0]
        local = _mult_matrix(name + '_Local_MultMatrix', [target + '.worldMatrix[0]', pim])
        decompose = cmds.createNode('decomposeMatrix', n=name + '_Scale_DecomposeMatrix')
        cmds.connectAttr(local, decompose + '.inputMatrix')
        rest_scale = om.MTransformationMatrix(_world(target) * rest_pim).scale(om.MSpace.kWorld)
        current = cmds.getAttr(driven + '.scale')[0]
        offset = cmds.createNode('multiplyDivide', n=name + '_Offset_MultiplyDivide')
        cmds.connectAttr(decompose + '.outputScale', offset + '.input1')
        cmds.setAttr(offset + '.input2', *[c / r if abs(r) > 1e-9 else 1.0 for c, r in zip(current, rest_scale)])
        return [(offset, 'scale', None)]

    elif con_type == 'aimConstraint':
        target = info['targets'][0][0]
        con = info['con']
        aim = cmds.createNode('aimMatrix', n=name + '_AimMatrix')
        compose = cmds.createNode('composeMatrix', n=name + '_Position_ComposeMatrix')
        cmds.connectAttr(driven + '.translate', compose + '.inputTranslate')
        _mult_matrix(name + '_Position_MultMatrix', [compose + '.outputMatrix', driven + '.parentMatrix[0]'])
        cmds.connectAttr(name + '_Position_MultMatrix.matrixSum', aim + '.inputMatrix')
        cmds.setAttr(aim + '.primaryInputAxis', *cmds.aimConstraint(con, q=True, aimVector=True))
        cmds.setAttr(aim + '.primaryMode', 1)
        cmds.connectAttr(target + '.worldMatrix[0]', aim + '.primaryTargetMatrix')
        cmds.setAttr(aim + '.secondaryInputAxis', *cmds.aimConstraint(con, q=True, upVector=True))
        up_type = cmds.aimConstraint(con, q=True, worldUpType=True)
        up_object = (cmds.aimConstraint(con, q=True, worldUpObject=True) or [None])[0]
        if up_type == 'object' and up_object:
            cmds.setAttr(aim + '.secondaryMode', 1)
            cmds.connectAttr(up_object + '.worldMatrix[0]', aim + '.secondaryTargetMatrix')
        elif up_type == 'objectrotation' and up_object:
            cmds.setAttr(aim + '.secondaryMode', 2)
            cmds.setAttr(aim + '.secondaryTargetVector', *cmds.aimConstraint(con, q=True, worldUpVector=True))
            cmds.connectAttr(up_object + '.worldMatrix[0]', aim + '.secondaryTargetMatrix')
        elif up_type in ('vector', 'scene'):
            cmds.setAttr(aim + '.secondaryMode', 2)
            vector = cmds.aimConstraint(con, q=True, worldUpVector=True) if up_type == 'vector' else (0, 1, 0)
            cmds.setAttr(aim + '.secondaryTargetVector', *vector)
        else:
            cmds.setAttr(aim + '.secondaryMode', 0)
        offset = _only_rotate(rest_world) * _only_rotate(_plug_matrix(aim + '.outputMatrix')).inverse()
        world = _mult_matrix(name + '_World_MultMatrix', [offset, aim + '.outputMatrix'])
        jobs = [(world, 'rotate', None)]

    return jobs


def follicles_to_uv_pins(follicles):
    """Swap hair follicles for one uvPin per surface. Follicles are dynamics nodes, Maya evaluates
    everything around them in the dynamics evaluator (serial), so a limb with follicles never runs
    in parallel. The follicle transforms stay (same names and rest pose), driven by the uvPin."""
    by_surface = {}
    for follicle in follicles:
        surface = (cmds.listConnections(follicle + '.inputSurface', s=True, d=False, shapes=True) or [None])[0]
        if surface:
            by_surface.setdefault(surface, []).append(follicle)

    for surface, shapes in by_surface.items():
        uv_pin = cmds.createNode('uvPin', n=surface.replace('Shape', '') + '_UvPin')
        cmds.connectAttr(surface + '.worldSpace[0]', uv_pin + '.deformedGeometry')
        cmds.setAttr(uv_pin + '.normalizedIsoParms', 1)
        index = 0
        for follicle in shapes:
            transform = cmds.listRelatives(follicle, p=True)[0]
            used = [c for c in cmds.listRelatives(transform, c=True) or [] if c != follicle]
            used += cmds.listConnections(transform, s=False, d=True) or []
            if not used:
                cmds.delete(transform)
                continue
            cmds.setAttr('{}.coordinate[{}].coordinateU'.format(uv_pin, index), cmds.getAttr(follicle + '.parameterU'))
            cmds.setAttr('{}.coordinate[{}].coordinateV'.format(uv_pin, index), cmds.getAttr(follicle + '.parameterV'))
            pin_plug = '{}.outputMatrix[{}]'.format(uv_pin, index)
            offset = _world(transform) * _plug_matrix(pin_plug).inverse()
            cmds.delete(follicle)
            for attr in ['translate', 'rotate']:
                for axis in [''] + list(AXES):
                    cmds.setAttr('{}.{}{}'.format(transform, attr, axis), lock=False)
            world =_mult_matrix(transform + '_UvPin_MultMatrix', [offset, pin_plug])
            _connect_channels(transform, transform, world, ['translateX', 'translateY', 'translateZ'], 'translate')
            _connect_channels(transform, transform, world, ['rotateX', 'rotateY', 'rotateZ'], 'rotate')
            index += 1


# -------------------------
# Bendy path: the tweak controllers ride an exact path through limb start -> mid bendy controller -> limb end,
# BendyCurve 0 = two straight lines, 10 = the circle arc through the three points. Bendy handles, AutoBend
# and the Start/End bendy controllers are added on top as offsets.

def _world_position(node):
    plug = node + '_WorldPosition_DecomposeMatrix'
    if not cmds.objExists(plug):
        cmds.createNode('decomposeMatrix', n=plug)
        cmds.connectAttr(node + '.worldMatrix[0]', plug + '.inputMatrix')
    return plug + '.outputTranslate'


def _vector_op(name, a, b, operation):
    """plusMinusAverage on two vector plugs, operation 1 sum, 2 subtract."""
    node = cmds.createNode('plusMinusAverage', n=name)
    cmds.setAttr(node + '.operation', operation)
    cmds.connectAttr(a, node + '.input3D[0]')
    cmds.connectAttr(b, node + '.input3D[1]')
    return node + '.output3D'


def _vector_scale(name, vector, value):
    node = cmds.createNode('multiplyDivide', n=name)
    cmds.connectAttr(vector, node + '.input1')
    for axis in AXES:
        _plug_or_value('{}.input2{}'.format(node, axis), value)
    return node + '.output'


def _vector_lerp(name, a, b, weight):
    """a when weight is 0, b when weight is 1 (vector plugs, weight plug or number)."""
    node = cmds.createNode('blendColors', n=name)
    for value, attr in [(b, '.color1'), (a, '.color2')]:
        if isinstance(value, str):
            cmds.connectAttr(value, node + attr)
        else:
            cmds.setAttr(node + attr, *value)
    _plug_or_value(node + '.blender', weight)
    return node + '.output'


def _vector_mix(name, a, b, weight):
    """a + (b - a) * weight, the weight can go negative or past 1."""
    difference = _vector_op(name + '_Difference_PlusMinusAverage', b, a, 2)
    return _vector_op(name + '_PlusMinusAverage', a, _vector_scale(name + '_MultiplyDivide', difference, weight), 1)


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


def _plug_or_value(node_attr, value):
    if isinstance(value, str):
        cmds.connectAttr(value, node_attr, f=True)
    else:
        cmds.setAttr(node_attr, value)


def _scaled_angle(name, angle, weight):
    """angle * weight, stays an angle (no unit conversion)."""
    node = cmds.createNode('animBlendNodeAdditiveDA', n=name)
    cmds.connectAttr(angle, node + '.inputA')
    cmds.setAttr(node + '.weightA', weight)
    cmds.setAttr(node + '.inputB', 0)
    return node + '.output'


def _sin(name, angle):
    """sin(angle): x of the quaternion of a rotation of 2 * angle."""
    node = cmds.createNode('axisAngleToQuat', n=name)
    cmds.setAttr(node + '.inputAxis', 1, 0, 0)
    cmds.connectAttr(_scaled_angle(name + '_Double', angle, 2), node + '.inputAngle')
    return node + '.outputQuatX'


def _rotate_vector(name, vector, axis, angle):
    quat = cmds.createNode('axisAngleToQuat', n=name + '_AxisAngleToQuat')
    cmds.connectAttr(axis, quat + '.inputAxis')
    cmds.connectAttr(angle, quat + '.inputAngle')
    compose = cmds.createNode('composeMatrix', n=name + '_ComposeMatrix')
    cmds.setAttr(compose + '.useEulerRotation', 0)
    cmds.connectAttr(quat + '.outputQuat', compose + '.inputQuat')
    product = cmds.createNode('vectorProduct', n=name + '_VectorProduct')
    cmds.setAttr(product + '.operation', 3)
    cmds.connectAttr(vector, product + '.input1')
    cmds.connectAttr(compose + '.outputMatrix', product + '.matrix')
    return product + '.output'


def _closest_axis(matrix, direction):
    """Local axis (vector, as a tuple) of a matrix that points the most along a world direction."""
    direction = direction.normal()
    axes = [om.MVector(matrix[i * 4], matrix[i * 4 + 1], matrix[i * 4 + 2]).normal() for i in range(3)]
    best = max(range(3), key=lambda k: abs(axes[k] * direction))
    sign = 1 if axes[best] * direction > 0 else -1
    return tuple(sign if k == best else 0 for k in range(3)), axes[best] * sign


def _surface_bend(name, full_surface, pin_surface, u_values):
    """Per u (v = 0.5): what the handles and AutoBend bend the bendy surface, full surface - twist only copy."""
    samples = []
    for surface in [full_surface, pin_surface]:
        shape = cmds.listRelatives(surface, s=True, ni=True)[0]
        uv_pin = cmds.createNode('uvPin', n='{}_{}_UvPin'.format(name, surface))
        cmds.connectAttr(shape + '.worldSpace[0]', uv_pin + '.deformedGeometry')
        cmds.setAttr(uv_pin + '.normalizedIsoParms', 1)
        plugs = []
        for index, u_value in enumerate(u_values):
            cmds.setAttr('{}.coordinate[{}].coordinateU'.format(uv_pin, index), u_value)
            cmds.setAttr('{}.coordinate[{}].coordinateV'.format(uv_pin, index), 0.5)
            decompose = cmds.createNode('decomposeMatrix', n='{}_{}_{}_DecomposeMatrix'.format(name, surface, index))
            cmds.connectAttr('{}.outputMatrix[{}]'.format(uv_pin, index), decompose + '.inputMatrix')
            plugs.append(decompose + '.outputTranslate')
        samples.append(plugs)
    return [_vector_op('{}_{}_Bend_PlusMinusAverage'.format(name, index), full, pin, 2)
            for index, (full, pin) in enumerate(zip(*samples))]


BEND_SLOPE_STEP = 0.02


def bendy_segment_path(name, start, end, other, curve, tweak_ctrls, start_offset, end_offset, full_surface, pin_surface,
                       ease=None, ease_at_start=True):
    """Drive the tweak controllers (their Auto group) along start -> end. start/end/other are world position
    plugs, curve (plug, -1 to 1) blends straight line -> arc through the 3 points, negative bows the other way,
    ease (plug 0-1) fades the curve out towards the start (or end) so the limb leaves that joint straight. Offsets (Start/End bendy controllers
    move) are world vectors added with a falloff, the handles / AutoBend bend of the bendy surface is added
    where each controller sits."""
    chord = _vector_op(name + '_Chord_PlusMinusAverage', end, start, 2)
    to_other = _vector_op(name + '_ToOther_PlusMinusAverage', other, start, 2)
    normal = cmds.createNode('vectorProduct', n=name + '_Normal_VectorProduct')
    cmds.setAttr(normal + '.operation', 2)
    cmds.setAttr(normal + '.normalizeOutput', 1)
    cmds.connectAttr(chord, normal + '.input1')
    cmds.connectAttr(to_other, normal + '.input2')
    normal += '.output'

    # inscribed angle at the other point: the arc start -> end turns twice this
    angle = cmds.createNode('angleBetween', n=name + '_Inscribed_AngleBetween')
    cmds.connectAttr(_vector_op(name + '_OtherStart_PlusMinusAverage', start, other, 2), angle + '.vector1')
    cmds.connectAttr(_vector_op(name + '_OtherEnd_PlusMinusAverage', end, other, 2), angle + '.vector2')
    angle += '.angle'
    sin_angle = _sin(name + '_Sin', angle)
    offsets_slope = _vector_op(name + '_OffsetSlope_PlusMinusAverage', end_offset, start_offset, 2)

    rest_start = om.MVector(cmds.getAttr(start)[0])
    rest_chord = om.MVector(cmds.getAttr(chord)[0])
    u_values = []
    for ctrl in tweak_ctrls:
        rest_ctrl = _world(ctrl)
        rest_position = om.MVector(rest_ctrl[12], rest_ctrl[13], rest_ctrl[14])
        u = ((rest_position - rest_start) * rest_chord) / (rest_chord * rest_chord)
        u_values.append(min(1.0, max(0.0, u)))  # the rest residual below takes the tiny leftover
    # bend at each controller and a bit ahead (for the slope, so the orientation follows the bend)
    bends = _surface_bend(name, full_surface, pin_surface,
                          [v for u in u_values for v in (u, min(1.0, u + BEND_SLOPE_STEP))])

    for num, ctrl in enumerate(tweak_ctrls):
        point = '{}_{}'.format(name, num)
        forward_grp = cmds.listRelatives(ctrl, p=True)[0]
        auto_grp = cmds.listRelatives(forward_grp, p=True)[0]
        root_grp = cmds.listRelatives(auto_grp, p=True)[0]
        rest_ctrl = _world(ctrl)
        rest_position = om.MVector(rest_ctrl[12], rest_ctrl[13], rest_ctrl[14])
        u = u_values[num]
        bend, bend_ahead = bends[num * 2], bends[num * 2 + 1]

        # position: straight / arc blend + offsets
        straight = _vector_lerp(point + '_Straight_BlendColors', start, end, u)
        chord_dir = _rotate_vector(point + '_ArcChord', chord, normal, _scaled_angle(point + '_ArcChord_Angle', angle, -(1 - u)))
        ratio = cmds.createNode('multiplyDivide', n=point + '_ArcRatio_MultiplyDivide')
        cmds.setAttr(ratio + '.operation', 2)
        cmds.connectAttr(_sin(point + '_SinU', _scaled_angle(point + '_U_Angle', angle, u)), ratio + '.input1X')
        cmds.connectAttr(sin_angle, ratio + '.input2X')
        # straight limb: sin is 0, the arc is the straight line
        safe_ratio = cmds.createNode('condition', n=point + '_ArcRatio_Condition')
        cmds.setAttr(safe_ratio + '.operation', 2)
        cmds.connectAttr(sin_angle, safe_ratio + '.firstTerm')
        cmds.setAttr(safe_ratio + '.secondTerm', 1e-5)
        cmds.connectAttr(ratio + '.outputX', safe_ratio + '.colorIfTrueR')
        cmds.setAttr(safe_ratio + '.colorIfFalseR', u)
        arc = _vector_op(point + '_Arc_PlusMinusAverage', start,
                         _vector_scale(point + '_ArcChord_MultiplyDivide', chord_dir, safe_ratio + '.outColorR'), 1)
        # curve at this point, the ease fades it towards the eased end: curve * (1 - ease * distance^2)
        point_curve = curve
        if ease:
            distance = (1 - u) if ease_at_start else u
            fade = _add(point + '_Ease_AddDoubleLinear', _mult(point + '_Ease_MultDoubleLinear', ease, -distance * distance), 1)
            point_curve = _mult(point + '_Curve_MultDoubleLinear', curve, fade)
        position = _vector_mix(point + '_Curve', straight, arc, point_curve)
        sum_node = cmds.createNode('plusMinusAverage', n=point + '_Position_PlusMinusAverage')
        cmds.connectAttr(position, sum_node + '.input3D[0]')
        cmds.connectAttr(_vector_lerp(point + '_StartOffset_BlendColors', start_offset, (0, 0, 0), u), sum_node + '.input3D[1]')
        cmds.connectAttr(_vector_lerp(point + '_EndOffset_BlendColors', (0, 0, 0), end_offset, u), sum_node + '.input3D[2]')
        cmds.connectAttr(bend, sum_node + '.input3D[3]')
        # keep the exact rest position
        residual = rest_position - om.MVector(cmds.getAttr(sum_node + '.output3D')[0])
        cmds.setAttr(sum_node + '.input3D[4]', *residual)
        compose = cmds.createNode('composeMatrix', n=point + '_Position_ComposeMatrix')
        cmds.connectAttr(sum_node + '.output3D', compose + '.inputTranslate')

        # orientation: along the path (tangent), twist from the ribbon (root group)
        tangent_arc = _rotate_vector(point + '_ArcTangent', chord, normal, _scaled_angle(point + '_ArcTangent_Angle', angle, -(1 - 2 * u)))
        step = min(1.0, u + BEND_SLOPE_STEP) - u
        bend_slope = _vector_scale(point + '_BendSlope_MultiplyDivide',
                                   _vector_op(point + '_BendSlope_PlusMinusAverage', bend_ahead, bend, 2),
                                   1.0 / step if step > 1e-6 else 0.0)
        tangent = cmds.createNode('plusMinusAverage', n=point + '_Tangent_PlusMinusAverage')
        cmds.connectAttr(_vector_mix(point + '_Tangent', chord, tangent_arc, point_curve), tangent + '.input3D[0]')
        cmds.connectAttr(offsets_slope, tangent + '.input3D[1]')
        cmds.connectAttr(bend_slope, tangent + '.input3D[2]')
        tangent += '.output3D'
        root_matrix = _world(root_grp)
        primary_axis, along = _closest_axis(rest_ctrl, rest_chord)
        root_axes = [om.MVector(root_matrix[i * 4], root_matrix[i * 4 + 1], root_matrix[i * 4 + 2]).normal() for i in range(3)]
        root_up = min(range(3), key=lambda k: abs(root_axes[k] * along))
        secondary_axis, _ = _closest_axis(rest_ctrl, root_axes[root_up])
        aim = cmds.createNode('aimMatrix', n=point + '_AimMatrix')
        cmds.setAttr(aim + '.primaryInputAxis', *primary_axis)
        cmds.setAttr(aim + '.primaryMode', 2)
        cmds.connectAttr(tangent, aim + '.primaryTargetVector')
        cmds.setAttr(aim + '.secondaryInputAxis', *secondary_axis)
        cmds.setAttr(aim + '.secondaryMode', 2)
        cmds.setAttr(aim + '.secondaryTargetVector', *[1 if k == root_up else 0 for k in range(3)])
        cmds.connectAttr(root_grp + '.worldMatrix[0]', aim + '.secondaryTargetMatrix')

        # old drivers out: blended parent constraint, aim constraint and the forward aim
        for constraint in set(cmds.listConnections(auto_grp, type='constraint', s=True, d=False) or []):
            cmds.delete(constraint)
        for attr in ['rotate'] + ['rotate' + a for a in AXES]:
            for plug in cmds.listConnections('{}.{}'.format(forward_grp, attr), s=True, d=False, p=True) or []:
                cmds.disconnectAttr(plug, '{}.{}'.format(forward_grp, attr))
        cmds.setAttr(forward_grp + '.rotate', 0, 0, 0)

        # the auto group takes the whole rest orientation of the controller
        offset = _only_rotate(rest_ctrl) * _only_rotate(_plug_matrix(aim + '.outputMatrix')).inverse()
        rotation = _mult_matrix(point + '_Rotation_MultMatrix', [offset, aim + '.outputMatrix'])
        _connect_channels(point, auto_grp, compose + '.outputMatrix', ['translateX', 'translateY', 'translateZ'], 'translate')
        _connect_channels(point, auto_grp, rotation, ['rotateX', 'rotateY', 'rotateZ'], 'rotate')


def bendy_move(name, ctrl):
    """How far a Start/End bendy controller was moved by the animator (world vector)."""
    parent = cmds.listRelatives(ctrl, p=True)[0]
    return _vector_op(name + '_Move_PlusMinusAverage', _world_position(ctrl), _world_position(parent), 2)


# -------------------------
# Studio orients: same result as the Custom_Biped_Orients block (FixArms / FixLegs), so limbs do not need it.

SN_ORIENTS = {'Arms': [[-90, -90, 0], [-90, -90, 0], [0, 0, -90]],
              'Legs': [[-90, -90, 0], [-90, -90, 0], [-90, -90, 0]]}


def apply_custom_orients(ctrls, rotates, right_ctrls):
    """Put an OrientChange group above every ctrl rotated by its value, the ctrl children and the joints
    it drives stay where they are."""
    constraints_data = []
    to_delete = []
    for ctrl in ctrls:
        for constraint in set(cmds.listConnections(ctrl, type='constraint', s=True, d=True) or []):
            joints = set(cmds.listConnections(constraint, s=False, d=True, type='joint') or [])
            if not joints:
                continue
            for joint in joints:
                constraints_data.append((ctrl, joint, cmds.nodeType(constraint)))
            to_delete.append(constraint)
    if to_delete:
        cmds.delete(list(set(to_delete)))

    for ctrl, rotate in zip(ctrls, rotates):
        children = cmds.listRelatives(ctrl, c=True, type='transform') or []
        for child in children:
            cmds.parent(child, world=True)
        root = mt.root_grp(input=ctrl, custom=True, custom_name='OrientChange')[0]
        cmds.rotate(rotate[0], rotate[1], rotate[2], root, relative=True, objectSpace=True)
        if ctrl in right_ctrls:
            cmds.setAttr(root + '.translate', 0, 0, 0)
            cmds.setAttr(root + '.rotate', *rotate)
            cmds.setAttr(root + '.scale', 1, 1, 1)
            cmds.setAttr(ctrl + '.translate', 0, 0, 0)
            cmds.setAttr(ctrl + '.rotate', 0, 0, 0)
        for child in children:
            cmds.parent(child, ctrl)

    for ctrl, joint, constraint_type in constraints_data:
        getattr(cmds, constraint_type)(ctrl, joint, mo=True)


# -------------------------
# Controllers scale (like Spine v002): a controller scale is not inherited by the controllers under it,
# it scales the bind joints around it instead, uniform or non uniform, axes matched to the joints at rest.

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


def _axis_map(ctrl_matrix, joint_matrix):
    """For every joint axis, the controller axis that points the same way at rest."""
    ctrl_axes = [om.MVector(ctrl_matrix[i * 4], ctrl_matrix[i * 4 + 1], ctrl_matrix[i * 4 + 2]).normal() for i in range(3)]
    joint_axes = [om.MVector(joint_matrix[i * 4], joint_matrix[i * 4 + 1], joint_matrix[i * 4 + 2]).normal() for i in range(3)]
    return [max(range(3), key=lambda k: abs(axis * ctrl_axes[k])) for axis in joint_axes]


def free_controller_scale(ctrls):
    """Unlock the scale and stop the children from inheriting it."""
    for ctrl in ctrls:
        for axis in [''] + list(AXES):
            cmds.setAttr('{}.scale{}'.format(ctrl, axis), lock=False)
        for axis in AXES:
            cmds.setAttr('{}.scale{}'.format(ctrl, axis), keyable=True)
        # a zero scale can not be compensated on the children
        cmds.transformLimits(ctrl, sx=(0.001, 1), sy=(0.001, 1), sz=(0.001, 1),
                             esx=(True, False), esy=(True, False), esz=(True, False))
        for child in cmds.listRelatives(ctrl, c=True, type='transform') or []:
            if cmds.listConnections(child + '.offsetParentMatrix', s=True, d=False):
                continue
            cmds.connectAttr(_inverse_scale_matrix(ctrl), child + '.offsetParentMatrix', f=True)


def scale_bind_joints(bind_joints, influences):
    """influences: {bind joint: [(ctrl, weight number or plug), ...]}. Multiplies the weighted controllers
    scale into the bind joints scale."""
    for jnt in bind_joints:
        rest = _world(jnt)
        product = None
        for num, (ctrl, weight) in enumerate(influences.get(jnt, [])):
            axis_map = _axis_map(_world(ctrl), rest)
            blend = cmds.createNode('blendColors', n='{}_Scale{:02d}_BlendColors'.format(jnt, num))
            for channel, ctrl_axis in zip('RGB', axis_map):
                cmds.connectAttr('{}.scale{}'.format(ctrl, AXES[ctrl_axis]), '{}.color1{}'.format(blend, channel))
                cmds.setAttr('{}.color2{}'.format(blend, channel), 1)
            if isinstance(weight, str):
                cmds.connectAttr(weight, blend + '.blender')
            else:
                cmds.setAttr(blend + '.blender', weight)
            if product is None:
                product = blend + '.output'
            else:
                mult = cmds.createNode('multiplyDivide', n='{}_Scale{:02d}_MultiplyDivide'.format(jnt, num))
                cmds.connectAttr(product, mult + '.input1')
                cmds.connectAttr(blend + '.output', mult + '.input2')
                product = mult + '.output'
        if product is None:
            continue
        scale_md = cmds.createNode('multiplyDivide', n=jnt + '_CtrlsScale_MultiplyDivide')
        cmds.connectAttr(product, scale_md + '.input2')
        for axis in AXES:
            source = cmds.listConnections('{}.scale{}'.format(jnt, axis), s=True, d=False, p=True, skipConversionNodes=True)
            if source:
                cmds.connectAttr(source[0], '{}.input1{}'.format(scale_md, axis))
            else:
                cmds.setAttr('{}.input1{}'.format(scale_md, axis), cmds.getAttr('{}.scale{}'.format(jnt, axis)))
            cmds.connectAttr('{}.output{}'.format(scale_md, axis), '{}.scale{}'.format(jnt, axis), f=True)


def _weight_plug(name, weight, switch_plug):
    """weight * switch (switch can be the reverse of the ik fk switch)."""
    node = cmds.createNode('multDoubleLinear', n=name)
    cmds.setAttr(node + '.input1', weight)
    cmds.connectAttr(switch_plug, node + '.input2')
    return node + '.output'


def _attr_spec(node, attr):
    plug = '{}.{}'.format(node, attr)
    spec = {'type': cmds.attributeQuery(attr, n=node, attributeType=True),
            'keyable': cmds.getAttr(plug, keyable=True), 'channel_box': cmds.getAttr(plug, channelBox=True),
            'lock': cmds.getAttr(plug, lock=True), 'value': cmds.getAttr(plug),
            'default': cmds.attributeQuery(attr, n=node, listDefault=True)[0]}
    if spec['type'] == 'enum':
        spec['enum'] = cmds.attributeQuery(attr, n=node, listEnum=True)[0]
    if cmds.attributeQuery(attr, n=node, minExists=True):
        spec['min'] = cmds.attributeQuery(attr, n=node, min=True)[0]
    if cmds.attributeQuery(attr, n=node, maxExists=True):
        spec['max'] = cmds.attributeQuery(attr, n=node, max=True)[0]
    return spec


def switch_attrs_to_data_node(switch_shape):
    """The switch shape is instanced under every limb controller and its attrs drive the limb, so for
    the evaluation manager the limb depends on itself (a cycle) and runs serial, several times per frame.
    The real attrs move to a data node (not in the hierarchy) and the shape keeps proxies of them,
    animators still see and key them on every controller."""
    shape = cmds.ls(switch_shape, type='locator')[0]
    data_node = cmds.createNode('network', n=shape.split('|')[-1] + '_Data')
    specs = []
    for attr in cmds.listAttr(shape, ud=True) or []:
        spec = _attr_spec(shape, attr)
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
        plug = '{}.{}'.format(shape, attr)
        spec['outputs'] = cmds.listConnections(plug, s=False, d=True, p=True) or []
        spec['inputs'] = cmds.listConnections(plug, s=True, d=False, p=True) or []
        specs.append((attr, spec))

    for attr, spec in specs:
        cmds.setAttr('{}.{}'.format(shape, attr), lock=False)
        cmds.deleteAttr(shape, at=attr)

    # same order as before so the channel box looks the same
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
    return data_node


def constraints_to_matrix(constraints, unscaled_targets=()):
    """Swap constraints for matrix nodes. Returns the constraints that could not be swapped."""
    infos = []
    kept = []
    for con in constraints:
        if not cmds.objExists(con) or cmds.nodeType(con) not in CONSTRAINT_TYPES:
            continue
        info = _constraint_info(con)
        if info:
            infos.append(info)
        else:
            kept.append(con)

    # read every rest offset first, then remove the constraints and hook the channels
    built = [(info, _build_matrix_network(info, unscaled_targets)) for info in infos]
    for info, jobs in built:
        cmds.delete(info['con'])
    for info, jobs in built:
        for plug, kind, post in jobs:
            if kind == 'scale':
                for axis in AXES:
                    if 'scale' + axis in info['channels']:
                        cmds.connectAttr('{}.output{}'.format(plug, axis), '{}.scale{}'.format(info['driven'], axis), f=True)
            else:
                _connect_channels(info['con'], info['driven'], plug, info['channels'], kind, post)
    return kept

# -------------------------

def build_limb_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()
    # constraints made before this block (base rig, other blocks) are left alone
    old_constraints = set(cmds.ls(type='constraint'))
    old_follicles = set(cmds.ls(type='follicle'))
    switch_shapes = []
    limbs_data = []

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guide = cmds.listRelatives(block, c=True)[0]

    new_guide = mt.duplicate_and_remove_guides(guide)
    print(new_guide)
    to_build = [new_guide]

    # orient the joints

    mt.orient_joint(input=new_guide)
    # force last joint to orient
    joint_three = cmds.listRelatives(new_guide, ad=True)[-2]
    cmds.setAttr("{}.jointOrientX".format(joint_three), 0)
    cmds.setAttr("{}.jointOrientY".format(joint_three), 0)
    cmds.setAttr("{}.jointOrientZ".format(joint_three), 0)

    # i have no idea why bt this shit doesnt work if we dont unparent and then aprent them

    joint_two = cmds.listRelatives(joint_three, p=True)
    cmds.parent(joint_three, w=True)
    cmds.parent(joint_two, w=True)
    cmds.parent(joint_two, new_guide)
    cmds.parent(joint_three, joint_two)

    # ctrl attrs
    ctrl_size = cmds.getAttr('{}.CtrlSize'.format(config))
    game_parent = cmds.getAttr('{}.SetGameParent'.format(config), asString=True)
    twist_amount = cmds.getAttr('{}.TwistAmount'.format(config))

    # compatible with older versions without world ik option
    if cmds.attributeQuery('ForceIkWorld', n=config, exists=True):
        force_ik_world = cmds.getAttr('{}.ForceIkWorld'.format(config))
    else:
        force_ik_world = False

    # compatible with older versions without ribbons
    if cmds.attributeQuery('Ribbons', n=config, exists=True):
        create_ribbons = cmds.getAttr(config + '.Ribbons')
    else:
        create_ribbons = True

    # compatible with older versions without ScaleTweakCtrls option
    if cmds.attributeQuery('ScaleTweakCtrls', n=config, exists=True):
        scale_tweak_ctrls = cmds.getAttr('{}.ScaleTweakCtrls'.format(config))
    else:
        scale_tweak_ctrls = False

    # Default: Mutant orients, SN: studio orients (what the Custom_Biped_Orients block did for limbs)
    if cmds.attributeQuery('Orients', n=config, exists=True):
        orients = cmds.getAttr('{}.Orients'.format(config), asString=True)
    else:
        orients = 'Default'

    # use this group for later cleaning, just assign them when you create the top on hierarchy
    clean_rig_grp = ''
    clean_ctrl_grp = ''

    # prep work for right side ------------------------------------------------------

    # if mirror is set only to right we need to build on left for mirror behavior then putt it back to righ side
    if cmds.getAttr('{}.Mirror'.format(config), asString=True) == 'Right_Only':
        right_guide = mirror = \
        cmds.mirrorJoint(new_guide, mirrorYZ=True, mirrorBehavior=True, searchReplace=(nc['left'], nc['right']))[0]
        mt.orient_joint(input=right_guide)
        to_build.append(right_guide)
        cmds.delete(new_guide)
        to_build.remove(new_guide)

    elif cmds.getAttr('{}.Mirror'.format(config), asString=True) == 'True':
        # right_guide = cmds.mirrorJoint(new_guide, mirrorYZ = True, mirrorBehavior=True, searchReplace = (nc['left'],nc['right']))[0]
        right_guide = mt.duplicate_change_names(input=new_guide, hi=True, search=nc['left'], replace=nc['right'])[0]
        mt.orient_joint(input=right_guide)
        to_build.append(right_guide)

        print(to_build)

    # build ------------------------------------------------------
    for side_guide in to_build:

        # use this locator in case parent is set to new locator
        if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
            block_parent = cmds.spaceLocator(
                n='{}'.format(str(side_guide).replace(nc['joint'], '_Parent' + nc['locator'])))[0]
        else:
            block_parent = cmds.getAttr('{}.SetParent'.format(config))
            if side_guide.startswith(nc['right']):
                block_parent = block_parent.replace(nc['left'], nc['right'])

        # smart select the colors
        if str(side_guide).startswith(nc['left']):
            color = setup['left_color']
            sec_color = setup['left_secundary_color']
        elif str(side_guide).startswith(nc['right']):
            color = setup['right_color']
            sec_color = setup['right_secundary_color']
        else:
            color = setup['main_color']
            sec_color = setup['main_color']


        # main funcion -------------------------------------------
        cmds.select(side_guide, hi=True)
        limb_a = cmds.ls(sl=True)[0]
        limb_b = cmds.ls(sl=True)[1]
        limb_c = cmds.ls(sl=True)[2]

        amrs_keyworkds = ['Shoulder', 'Elbow', 'Wrist', 'Arm','Clav']
        legs_keyworkds = ['Hip', 'Kne', 'Ankle', 'Leg', 'Pelvis']

        limbs = [limb_a, limb_b, limb_c]

        mode = 'None'
        for keyword in amrs_keyworkds:
            for limb in limbs:
                if keyword.lower() in limb.lower():
                    mode = 'Arms'

        for keyword in legs_keyworkds:
            for limb in limbs:
                if keyword.lower() in limb.lower():
                    mode = 'Legs'

        ikfk = mt.twist_fk_ik(start='', mid='', end='', size=ctrl_size, color=color, twist_amount=twist_amount)

        print('----------------IK FK------------------')

        # Limb global scale: one more level under the Global controller, scales the whole limb from its start
        # (L_Arm_GlobalScale_Ctrl / L_Leg_GlobalScale_Ctrl), everything that followed the Global scale follows this
        side_prefix = str(side_guide).split('_')[0]
        limb_label = {'Arms': 'Arm', 'Legs': 'Leg'}.get(mode, str(limb_a).split('_')[1] if '_' in str(limb_a) else 'Limb')
        limb_global_ctrl = mt.curve(input=ikfk['ik_fk'][0][0], type='circleX', rename=True, custom_name=True,
                                    name='{}_{}_GlobalScale{}'.format(side_prefix, limb_label, nc['ctrl']),
                                    size=ctrl_size * 1.8)
        mt.assign_color(limb_global_ctrl, color)
        limb_global_root = mt.root_grp(input=limb_global_ctrl)[0]
        cmds.delete(cmds.parentConstraint(ikfk['ik_fk'][0][0], limb_global_root, mo=False))
        cmds.parent(limb_global_root, setup['base_groups']['control'] + nc['group'])
        # uniform: scale X drives Y and Z, so any scale manipulator works
        for axis in 'YZ':
            cmds.connectAttr(limb_global_ctrl + '.scaleX', '{}.scale{}'.format(limb_global_ctrl, axis))
            cmds.setAttr('{}.scale{}'.format(limb_global_ctrl, axis), keyable=False, channelBox=False)
        for attr in ['translate', 'rotate']:
            for axis in 'XYZ':
                cmds.setAttr('{}.{}{}'.format(limb_global_ctrl, attr, axis), lock=True, keyable=False, channelBox=False)
        cmds.setAttr(limb_global_ctrl + '.visibility', keyable=False, channelBox=False)
        limb_scale_node = cmds.createNode('decomposeMatrix', n=limb_global_ctrl + '_WorldScale_DecomposeMatrix')
        cmds.connectAttr(limb_global_ctrl + '.worldMatrix[0]', limb_scale_node + '.inputMatrix')
        limb_scale = limb_scale_node + '.outputScale'

        # clean a bit
        print(ikfk['ik_fk'])
        cmds.connectAttr(limb_scale, '{}.scale'.format(ikfk['ik_fk'][4][5][1]))

        # ikfk['ik_fk'[#]]
        # [0] ['L_Shoulder_Jnt', 'L_Elbow_Jnt', 'L_Wrist_Jnt'],
        # [1] ['L_Shoulder_Ik_Jnt', 'L_Elbow_Ik_Jnt', 'L_Wrist_Ik_Jnt'],
        # [2] ['L_Shoulder_Fk_Jnt', 'L_Elbow_Fk_Jnt', 'L_Wrist_Fk_Jnt'],
        # [3] ['L_Shoulder_Fk_Ctrl', 'L_Elbow_Fk_Ctrl', 'L_Wrist_Fk_Ctrl'],
        # [4] ['L_Wrist_Ik_Ctrl', 'L_Wrist_Ik_PoleVector_Ctrl', 'L_Shoulder_Ik_Ctrl', 'L_Wrist_Ik_IKrp', 'L_Wrist_Ik_PoleVector_Ctrl_L_Elbow_Ik_Jnt_Connected_Crv', ('L_Wrist_Ik_IKrp_Stretchy_Grp', 'L_Wrist_Ik_IKrp_NormalScale_Loc', ['L_Wrist_Ik_Jnt_Stretchy_Loc'], ['L_Shoulder_Ik_Jnt_Stretchy_Loc'], ['L_Elbow_Ik_Jnt_Stretchy_Loc'], 'L_Shoulder_Ik_Jnt_L_Wrist_Ik_Jnt_Distance_Shape', 'L_Elbow_Ik_Jnt_L_Wrist_Ik_Jnt_Distance_Shape', 'L_Shoulder_Ik_Jnt_L_Elbow_Ik_Jnt_Distance_Shape')], ['L_Shoulder_Fk_Ctrl_Offset_Grp', 'L_Wrist_Ik_Ctrl_Offset_Grp', 'L_Shoulder_Ik_Ctrl_Offset_Grp', 'L_Shoulder_Ik_Jnt_Ctrl_Grp'])
        # [5] ['L_Shoulder_Fk_Ctrl_Offset_Grp', 'L_Wrist_Ik_Ctrl_Offset_Grp', 'L_Shoulder_Ik_Ctrl_Offset_Grp', 'L_Shoulder_Ik_Jnt_Ctrl_Grp'])

        print(ikfk['upper_twist'])
        print(ikfk['lower_twist'])
        # ------------------------------------------------------------------------------------------------
        #Space switches
        #Pole vector space switch
        print('---------------------------------------')
        print(ikfk)
        world = 'Global_Ctrl'
        ctrl = ikfk['ik_fk'][4][0]
        pv = ikfk['ik_fk'][4][1]
        switch_locator = ikfk['ik_fk'][0][0] + '_Switch' + nc['locator']
        switch_shapes.append(switch_locator)

        fk_ctrl = ikfk['ik_fk'][3][0]
        fk_offset = ikfk['ik_fk'][5][0]
        fk_root, fk_auto = mt.root_grp(input=ikfk['ik_fk'][3][0], autoRoot=True)


        # ------------------------------------------------------------------------------------------------

        # Add Ribbons
        if create_ribbons:

            # Ribbon stuff from BendyRibbons RdM ToolsV2

            name = '{}'.format(str(side_guide).replace(nc['joint'], ''))

            start = ikfk['ik_fk'][0][0]
            mid = ikfk['ik_fk'][0][1]
            end = ikfk['ik_fk'][0][2]

            # -----------------------------------
            # Ribbon Middle Controllers

            mt.line_attr(input=switch_locator, name='Bendy_Vis')
            ribbon_first_vis_attr = mt.new_enum(input=switch_locator, name='BendyMain', enums='Hide:Show', keyable=False)
            ribbon_second_vis_attr = mt.new_enum(input=switch_locator, name='BendyOffsets', enums='Hide:Show', keyable=False)
            ribbon_ends_vis_attr = mt.new_enum(input=switch_locator, name='BendyEnds', enums='Hide:Show', keyable=False)
            ribbon_third_vis_attr = mt.new_enum(input=switch_locator, name='BendyTweeks', enums='Hide:Show', keyable=False)

            # for dev set to 0 at the end
            cmds.setAttr(ribbon_first_vis_attr, 1)
            cmds.setAttr(ribbon_second_vis_attr, 0)
            cmds.setAttr(ribbon_third_vis_attr, 0)
            cmds.setAttr(ribbon_ends_vis_attr, 0)

            # Bendy curve attrs (v002, replace the old AutoBend handle automation)
            # BendyCurve: 0 straight lines through the mid bendy controller, 10 a perfect arc
            # AutoCurve: extra curve the more the limb bends (all of it at 90 degrees)
            # Upper/LowerCurve: per segment offset, negative bows the other way (S shapes)
            # Start/End Ease: keeps the limb leaving the shoulder / wrist straight
            mt.line_attr(input=switch_locator, name='BendyCurve')
            ease_names = {'Arms': ['ShoulderEase', 'WristEase'], 'Legs': ['HipEase', 'AnkleEase']}.get(mode, ['StartEase', 'EndEase'])
            curve_attrs = {
                'curve': mt.new_attr(input=switch_locator, name='BendyCurve', min=0, max=10, default=0),
                'auto': mt.new_attr(input=switch_locator, name='AutoCurve', min=0, max=10, default=0),
                'upper': mt.new_attr(input=switch_locator, name='UpperCurve', min=-10, max=10, default=0),
                'lower': mt.new_attr(input=switch_locator, name='LowerCurve', min=-10, max=10, default=0),
                'start_ease': mt.new_attr(input=switch_locator, name=ease_names[0], min=0, max=10, default=0),
                'end_ease': mt.new_attr(input=switch_locator, name=ease_names[1], min=0, max=10, default=0)}
            curve_attr_names = [plug.split('.')[-1] for plug in curve_attrs.values()]

            # cmds.setAttr(bendy_shoulder_attr, 5)
            # cmds.setAttr(bendy_elbow_shoulder_attr, -2)
            # cmds.setAttr(bendy_elbow_wrist_attr, 2)
            # cmds.setAttr(bendy_wrist_attr, -5)

            def create_mid_ribbons(name, first_joint, last_joint, twist_joints, aim):

                # main tweek Ribbons
                ribbon_limb_nurb = cmds.nurbsPlane(ch=1, d=1, v=1, p=(0, 0, 0), u=1, w=1, ax=(0, 0, 1), lr=1,
                                                   n=name + 'Ribbon' + nc['nurb'])
                cluster01 = cmds.cluster(ribbon_limb_nurb[0] + '.cv[0][0:1]')
                cluster02 = cmds.cluster(ribbon_limb_nurb[0] + '.cv[1][0:1]')
                cmds.setAttr(str(ribbon_limb_nurb[0]) + '.visibility', 0)
                cmds.delete(cmds.parentConstraint(first_joint, cluster01, mo=False))
                cmds.delete(cmds.parentConstraint(last_joint, cluster02, mo=False))
                cmds.delete(ribbon_limb_nurb, ch=True)
                cmds.rebuildSurface(ribbon_limb_nurb[0], rt=0, kc=0, fr=0, end=1, sv=1, su=twist_amount, kr=0,
                                    dir=2, kcp=0,
                                    tol=0.01, dv=1, du=3, rpo=1)

                # Create follicles
                cmds.select(ribbon_limb_nurb[0])
                mel.eval("createHair {} 1 10 0 0 0 0 5 0 1 2 1;".format(twist_amount))

                cmds.delete('hairSystem1', 'pfxHair1', 'nucleus1')
                cmds.setAttr(ribbon_limb_nurb[0] + '.inheritsTransform', 0)

                for C in range(1, twist_amount + 1):
                    cmds.delete('curve' + str(C))
                fol_grp = cmds.rename('hairSystem1Follicles', name + nc['follicle'] + nc['group'])

                follicles = cmds.ls(name + nc['follicle'] + nc['group'], dag=True, type='follicle')
                fol_joints = []
                cmds.setAttr(follicles[0] + '.parameterU', 0)

                for num, i in enumerate(follicles):
                    cmds.select(i)
                    fol_new_name = cmds.rename(cmds.listRelatives(i, p=True), name + '_' + str(num) + nc['follicle'])
                    fol_jnt = cmds.joint(n=name + '_' + str(num) + nc['joint'])
                    fol_joints.append(fol_jnt)
                    #Normalize Follicles
                    cmds.connectAttr(limb_scale, fol_new_name+'.scale')
                # Bind twist to bendy surfaces
                cmds.skinCluster(twist_joints[:-1], ribbon_limb_nurb[0], sm=0, bm=1, tsb=True)

                tweks_ribbon_ctrl_grp = cmds.group(em=True, n=name + '_Ribbons' + nc['ctrl'] + nc['group'])
                ribbon_ctrls = []
                for fol_jnt in fol_joints:
                    ctrl = mt.curve(input=fol_jnt, type='square',
                                    rename=True,
                                    custom_name=True, name=fol_jnt.replace(nc['joint'], nc['ctrl']),
                                    size=ctrl_size / 3,
                                    )
                    mt.shape_with_attr(input='', obj_name=start + '_Switch', attr_name='')
                    mt.assign_color(ctrl, sec_color)
                    root, auto = mt.root_grp(input=ctrl, autoRoot=True)
                    cmds.parentConstraint(cmds.listRelatives(fol_jnt, p=True)[0], root, mo=False)
                    cmds.parentConstraint(ctrl, fol_jnt)
                    cmds.parent(root, tweks_ribbon_ctrl_grp)

                    cmds.connectAttr(ribbon_third_vis_attr, '{}.v'.format(cmds.listRelatives(ctrl, shapes=True)[0]))
                    ribbon_ctrls.append(ctrl)
                # --------------------------------------------------------------------------------
                # --------------------------------------------------------------------------------
                # --------------------------------------------------------------------------------

                # Bendy Ribbons
                # create ribbon Plane
                middle_limb_nurb = cmds.nurbsPlane(ch=1, d=1, v=1, p=(0, 0, 0), u=1, w=1, ax=(0, 0, 1), lr=1,
                                                   n=name + 'Bendy' + nc['nurb'])
                cluster01 = cmds.cluster(middle_limb_nurb[0] + '.cv[0][0:1]')
                cluster02 = cmds.cluster(middle_limb_nurb[0] + '.cv[1][0:1]')
                # cmds.setAttr(str(middle_limb_nurb[0]) + '.visibility', 0)
                cmds.delete(cmds.parentConstraint(first_joint, cluster01, mo=False))
                cmds.delete(cmds.parentConstraint(last_joint, cluster02, mo=False))
                cmds.delete(middle_limb_nurb, ch=True)
                # cmds.rebuildSurface(middle_limb_nurb[0], rt=0, kc=0, fr=0, end=1, sv=1, su=2, kr=0,
                cmds.rebuildSurface(middle_limb_nurb[0], rt=0, kc=0, fr=0, end=1, sv=1, su=len(twist_joints) + 1, kr=0,
                                    dir=2, kcp=0,
                                    tol=0.01, dv=1, du=3, rpo=1)
                # cmds.skinCluster(first_joint, middle_limb_nurb[0], sm=0, bm=1, tsb=True)

                # create joints for iks
                middle_joints = mt.joints_middle(start=first_joint, end=last_joint, axis=setup['twist_axis'], amount=4,
                                                 name='BendyMid')
                for jnt in middle_joints:
                    try:
                        cmds.parent(jnt, w=True)
                    except:
                        pass

                cmds.parent(middle_joints[1], middle_joints[0])
                cmds.parent(middle_joints[2], middle_joints[3])

                # put middle joints in middle
                cmds.delete(cmds.parentConstraint(first_joint, last_joint, middle_joints[1], mo=False))
                cmds.delete(cmds.parentConstraint(first_joint, last_joint, middle_joints[2], mo=False))

                # create iks (now they are not IK anymore)
                ik_bendy_grp = cmds.group(middle_joints[0], middle_joints[3],
                                          n='{}_BendyIK{}'.format(name, nc['group']))

                # cmds.skinCluster(middle_joints, middle_limb_nurb[0], sm=0, bm=1, tsb=True)
                # cmds.skinCluster(twist_joints, middle_limb_nurb[0], sm=0, bm=1, tsb=True)
                # put this under bs

                # Pin IK Bendys
                top_ik_bendy_ctrl = mt.curve(input=first_joint,
                                             type='pin_cube',
                                             rename=True,
                                             custom_name=True,
                                             name=name.replace(nc['joint'], '_Top_Handle' + nc['ctrl']),
                                             size=ctrl_size / 3,
                                             )
                top_ik_bendy_root = mt.root_grp()
                mt.assign_color(top_ik_bendy_ctrl, sec_color)
                cmds.delete(cmds.parentConstraint(first_joint, top_ik_bendy_root))
                mt.shape_with_attr(input=top_ik_bendy_ctrl, obj_name=start + '_Switch', attr_name='')
                mt.hide_attr(input=top_ik_bendy_ctrl ,t=True, r=False, s=True,v=True)

                bottom_ik_bendy_ctrl = mt.curve(input=last_joint,
                                                type='pin_cube',
                                                rename=True,
                                                custom_name=True,
                                                name=name.replace(nc['joint'], '_Bottom_Handle' + nc['ctrl']),
                                                size=ctrl_size / 3,
                                                )
                mt.assign_color(bottom_ik_bendy_ctrl, sec_color)
                bottom_ik_bendy_root = mt.root_grp()
                cmds.delete(cmds.parentConstraint(last_joint, bottom_ik_bendy_root))
                mt.shape_with_attr(input=bottom_ik_bendy_ctrl, obj_name=start + '_Switch', attr_name='')
                mt.hide_attr(input=bottom_ik_bendy_ctrl, t=True, r=False, s=True, v=True)

                # Aim to each other
                # cmds.delete(cmds.aimConstraint(top_ik_bendy_ctrl, bottom_ik_bendy_root, aimVector =(0, 1, 0), upVector = (0,0,-1)))
                # cmds.delete(cmds.aimConstraint(bottom_ik_bendy_ctrl, top_ik_bendy_root, aimVector =(0, 1, 0), upVector = (0,0,-1)))
                cmds.rotate(0, 0, 90 - cmds.getAttr('{}.jointOrientZ'.format(last_joint)),
                            '{}.cv[0:22]'.format(bottom_ik_bendy_ctrl), r=True)
                cmds.rotate(0, 0, -90, '{}.cv[0:22]'.format(top_ik_bendy_ctrl), r=True)

                # cmds.parentConstraint(first_joint, ik_bendy_grp,mo=True)
                # cmds.parentConstraint(top_ik_bendy_ctrl, start_handle,mo=True)
                # cmds.parentConstraint(bottom_ik_bendy_ctrl, end_handle, mo=True)
                # cmds.parentConstraint(first_joint, middle_joints[0])
                # cmds.parentConstraint(last_joint, middle_joints[3])

                cmds.connectAttr(ribbon_second_vis_attr,
                                 '{}.v'.format(cmds.listRelatives(top_ik_bendy_ctrl, shapes=True)[0]))
                cmds.connectAttr(ribbon_second_vis_attr,
                                 '{}.v'.format(cmds.listRelatives(bottom_ik_bendy_ctrl, shapes=True)[0]))

                handle_controllers = [top_ik_bendy_ctrl, bottom_ik_bendy_ctrl]
                handle_controllers_roots = [bottom_ik_bendy_root[0], top_ik_bendy_root[0]]
                # local system for handles
                # local system for handles
                local_geo_ik_geo = cmds.duplicate(middle_limb_nurb[0], n=name + 'Bendy_IK_Local' + nc['nurb'])
                cmds.skinCluster(middle_joints, local_geo_ik_geo, sm=0, bm=1, tsb=True)

                # v001 also had an unused static copy (Bendy_Other_Local) as a second target, it added nothing
                # twist only copy of the bendy surface: full surface - this copy = what handles and AutoBend bend
                pin_surface = cmds.duplicate(middle_limb_nurb[0], n=name + 'Bendy_Pin' + nc['nurb'])[0]

                cmds.select(local_geo_ik_geo, middle_limb_nurb[0])
                bs = cmds.blendShape(n='{}_Bendy{}'.format(name, '_BS'), w=[(0, 1)], )
                cmds.skinCluster(twist_joints, middle_limb_nurb[0], sm=0, bm=1, tsb=True)
                cmds.skinCluster(twist_joints, pin_surface, sm=0, bm=1, tsb=True)
                cmds.setAttr(pin_surface + '.inheritsTransform', 0)
                cmds.setAttr(pin_surface + '.visibility', 0)

                local_grp = cmds.group(local_geo_ik_geo, ik_bendy_grp, n=name + '_Local' + nc['group'])

                cmds.connectAttr(top_ik_bendy_ctrl + '.rotate', middle_joints[0] + '.rotate')
                cmds.connectAttr(bottom_ik_bendy_ctrl + '.rotate', middle_joints[3] + '.rotate')

                # Bendys
                # Create follicles
                cmds.select(middle_limb_nurb[0])
                mel.eval("createHair {} 1 10 0 0 0 0 5 0 1 2 1;".format(3))

                cmds.delete('hairSystem1', 'pfxHair1', 'nucleus1')
                cmds.setAttr(middle_limb_nurb[0] + '.inheritsTransform', 0)

                for C in range(1, 4):
                    cmds.delete('curve' + str(C))
                bendy_fol_grp = cmds.rename('hairSystem1Follicles', name + '_Bendy' + nc['follicle'] + nc['group'])

                bendy_follicles = cmds.ls(bendy_fol_grp, dag=True, type='follicle')
                cmds.setAttr(bendy_follicles[0] + '.parameterU', 0.05)
                cmds.setAttr(bendy_follicles[-1] + '.parameterU', 0.95)

                custom_name = ['Start', 'End']
                second_ctrls = []
                second_roots = []
                for num, fol in enumerate([bendy_follicles[0], bendy_follicles[-1]]):
                    ribbon_ctrl = mt.curve(input=fol, type='sphere',
                                           rename=True,
                                           custom_name=True,
                                           name=name.replace(nc['joint'], custom_name[num] + '_Bendy' + nc['ctrl']),
                                           size=ctrl_size / 1.5,
                                           )
                    mt.assign_color(ribbon_ctrl, sec_color)
                    root, auto = mt.root_grp(input=ribbon_ctrl, autoRoot=True)
                    cmds.parentConstraint(cmds.listRelatives(fol, p=True)[0], root, mo=False)
                    cmds.connectAttr(ribbon_ends_vis_attr,
                                     '{}.v'.format(cmds.listRelatives(ribbon_ctrl, shapes=True)[0]))
                    second_ctrls.append(ribbon_ctrl)
                    second_roots.append(root)
                    mt.shape_with_attr(input=ribbon_ctrl, obj_name=start + '_Switch', attr_name='')
                    #Normalize Follicles
                    cmds.connectAttr(limb_scale, cmds.listRelatives(fol, p=True)[0]+'.scale')

                forward = list(enumerate(ribbon_ctrls))
                backward = list(reversed(forward))

                extra_aim_forward_grp = cmds.group(em=True, n=name + '_ForwardAim' + nc['group'])
                cmds.scaleConstraint(limb_global_ctrl, extra_aim_forward_grp)

                for num, ctrl in enumerate(ribbon_ctrls):
                    auto = cmds.listRelatives(ctrl, p=True)
                    pc = \
                    cmds.parentConstraint(second_ctrls[0], second_ctrls[1], auto, skipRotate=('x', 'y', 'z'), mo=True)[
                        0]
                    cmds.setAttr(pc + '.' + second_ctrls[0] + 'W0', backward[num][0])
                    cmds.setAttr(pc + '.' + second_ctrls[1] + 'W1', forward[num][0])
                    cmds.setAttr(pc + '.interpType', 2)  # shortest

                    # aim to ctrl
                    # cmds.aimConstraint(second_ctrls[1], auto, aimVector =(aim, 0, 0), upVector = (0,0,-1)), worldUpType='vector', mo=True)#, worldUpObject=up_vector_loc, mo=True)
                    cmds.aimConstraint(second_ctrls[1], auto, aimVector=(1, 0, 0), upVector=(0, 1, 0),
                                       worldUpType='object', worldUpObject=second_ctrls[1], mo=True)

                    # add extra aim to next controller
                    aim_loc = cmds.spaceLocator(n=ctrl.replace(nc['ctrl'], '_Aim' + nc['locator']))[0]
                    aim_loc_root = mt.root_grp()
                    cmds.parent(aim_loc_root, extra_aim_forward_grp)
                    cmds.delete(cmds.parentConstraint(ribbon_ctrls[num], aim_loc_root, mo=False))
                    cmds.parentConstraint(cmds.listRelatives(ribbon_ctrls[num], p=True)[0], aim_loc_root, mo=True)

                    # Create upVector
                    up_aim_loc = cmds.spaceLocator(n=ctrl.replace(nc['ctrl'], '_UpVector' + nc['locator']))[0]
                    cmds.parent(up_aim_loc, aim_loc_root)
                    cmds.delete(cmds.parentConstraint(aim_loc, up_aim_loc, mo=False))
                    cmds.setAttr(up_aim_loc + '.translateZ', ctrl_size * -1)
                    # Create Aim
                    # aimConstraint -mo -weight 1 -aimVector 1 0 0 -upVector 0 0 -1 -worldUpType "object" -worldUpObject L_Shoulder_UpVector_Loc_2_UpVector_Loc;
                    try:
                        cmds.aimConstraint(cmds.listRelatives(ribbon_ctrls[num + 1], p=True)[0], aim_loc,
                                           aimVector=(1, 0, 0), upVector=(0, 0, -1), worldUpType='object',
                                           worldUpObject=up_aim_loc, mo=True)
                    except:
                        pass
                    aim_grp = mt.root_grp(ribbon_ctrls[num], custom=True, custom_name='_ForwardAim')[0]
                    cmds.connectAttr(aim_loc + '.rotate', aim_grp + '.rotate')

                # Connect Handles local to 2nd controllers
                cmds.parentConstraint(second_ctrls[0], top_ik_bendy_root, mo=True)
                cmds.parentConstraint(second_ctrls[1], bottom_ik_bendy_root, mo=True)
                # cmds.aimConstraint(second_ctrls[1], top_ik_bendy_root, mo=True)
                # cmds.aimConstraint(second_ctrls[0], bottom_ik_bendy_root, mo=True)

                # clean the ribbon a bit
                ribbon_ctrl_grp = cmds.group(n=name.replace(nc["joint"], '_Ribbon' + nc['ctrl'] + nc['group']), em=True)
                cmds.parent(second_roots, tweks_ribbon_ctrl_grp, bottom_ik_bendy_root, top_ik_bendy_root,
                            ribbon_ctrl_grp)

                ribbon_rig_group = cmds.group(n=name.replace(nc["joint"], '_Ribbon_Rig' + nc['group']), em=True)
                cmds.parent(local_grp, bendy_fol_grp, extra_aim_forward_grp, middle_limb_nurb[0], pin_surface, ribbon_rig_group)

                # transfer scale from twist to ibbon jnts
                for num, jnt in enumerate(twist_joints):
                    # v002: the tweak controller scale is added on the bind joint with the other controllers
                    # (axis matched, non uniform), always on, ScaleTweakCtrls is not used anymore
                    cmds.connectAttr('{}.scale'.format(jnt), '{}.scale'.format(fol_joints[num]))

                return {'ribbon_ctrl_grp': ribbon_ctrl_grp, 'ribbon_ctrls': ribbon_ctrls,
                        'ribbon_plane': ribbon_limb_nurb[0], 'fol_ribbon_grp': fol_grp, 'fol_joints': fol_joints,
                        'second_ctrls': second_ctrls, 'handle_controllers': handle_controllers, 'handle_controllers_roots' : handle_controllers_roots,
                        'clean_rig_grp': ribbon_rig_group, 'clean_ctrl_grp': ribbon_ctrl_grp,
                        'middle_joints' : middle_joints, 'middle_surface': middle_limb_nurb[0],
                        'pin_surface': pin_surface, 'forward_aim_grp': extra_aim_forward_grp
                        }

            # ---------------------------------------------------------------------------------------------------------------------------------------
            top_ribbon = create_mid_ribbons(name=start, first_joint=start, last_joint=mid,
                                            twist_joints=ikfk['upper_twist']['joints'], aim=1)
            low_ribbon = create_mid_ribbons(name=mid, first_joint=mid, last_joint=end,
                                            twist_joints=ikfk['lower_twist']['joints'], aim=-1)
            # ---------------------------------------------------------------------------------------------------------------------------------------

            # Main mid controller
            main_mid_ctrl = mt.curve(input=mid,
                                     type='cubePlus',
                                     rename=True,
                                     custom_name=True,
                                     name=mid.replace(nc['joint'], 'Mid_Bendy' + nc['ctrl']),
                                     size=ctrl_size/2,
                                     )
            mt.assign_color(main_mid_ctrl, sec_color)
            root_mid_ctrl = mt.root_grp(input=main_mid_ctrl)
            mt.shape_with_attr(input=main_mid_ctrl, obj_name=start + '_Switch', attr_name='')

            cmds.parentConstraint(mid, root_mid_ctrl, mo=False)

            cmds.pointConstraint(main_mid_ctrl, cmds.listRelatives(top_ribbon['second_ctrls'][1], p=True), mo=True)
            cmds.pointConstraint(main_mid_ctrl, cmds.listRelatives(low_ribbon['second_ctrls'][0], p=True), mo=True)
            cmds.connectAttr(ribbon_first_vis_attr, '{}.v'.format(cmds.listRelatives(main_mid_ctrl, shapes=True)[0]))

            # --- Mid Bendy Scale Falloff ---
            # Connect main_mid_ctrl scale to ribbon fol_joints with weighted falloff
            # Weight is 1.0 at elbow, fading to 0.0 at shoulder/wrist
            for ribbon_data, is_upper in [(top_ribbon, True), (low_ribbon, False)]:
                fol_joints_list = ribbon_data['fol_joints']
                n = len(fol_joints_list)

                for idx, fol_jnt in enumerate(fol_joints_list):
                    # Upper ribbon ramps up toward elbow, lower ramps down from elbow
                    if n > 1:
                        t = float(idx) / float(n - 1)
                        weight = t if is_upper else (1.0 - t)
                    else:
                        weight = 1.0

                    if weight < 0.001:
                        continue  # Skip joints with negligible weight

                    # BlendColors: lerp between (1,1,1) and mid_ctrl.scale by weight
                    blend_node = cmds.createNode('blendColors', n='{}_MidBendyScale_Blend'.format(fol_jnt))
                    cmds.connectAttr('{}.scaleX'.format(main_mid_ctrl), '{}.color1R'.format(blend_node))
                    cmds.connectAttr('{}.scaleY'.format(main_mid_ctrl), '{}.color1G'.format(blend_node))
                    cmds.connectAttr('{}.scaleZ'.format(main_mid_ctrl), '{}.color1B'.format(blend_node))
                    cmds.setAttr('{}.color2'.format(blend_node), 1, 1, 1, type='double3')
                    cmds.setAttr('{}.blender'.format(blend_node), weight)

                    # Insert multiply into existing scale chain
                    md_mid = cmds.createNode('multiplyDivide', n='{}_MidBendyScale_MD'.format(fol_jnt))

                    # Find and reroute existing scale source (compound or per-axis)
                    scale_src = cmds.listConnections('{}.scale'.format(fol_jnt), source=True, destination=False, plugs=True, skipConversionNodes=True)
                    if scale_src:
                        src_plug = scale_src[0]
                        cmds.disconnectAttr(src_plug, '{}.scale'.format(fol_jnt))
                        src_node, src_attr = src_plug.split('.', 1)
                        for ax, color_ax in [('X', 'R'), ('Y', 'G'), ('Z', 'B')]:
                            cmds.connectAttr('{}.{}{}'.format(src_node, src_attr, ax), '{}.input1{}'.format(md_mid, ax))
                            cmds.connectAttr('{}.output{}'.format(blend_node, color_ax), '{}.input2{}'.format(md_mid, ax))
                            cmds.connectAttr('{}.output{}'.format(md_mid, ax), '{}.scale{}'.format(fol_jnt, ax))
                    else:
                        # Fallback: try per-axis connections
                        for ax, color_ax in [('X', 'R'), ('Y', 'G'), ('Z', 'B')]:
                            ax_src = cmds.listConnections('{}.scale{}'.format(fol_jnt, ax), source=True, destination=False, plugs=True, skipConversionNodes=True)
                            if ax_src:
                                cmds.disconnectAttr(ax_src[0], '{}.scale{}'.format(fol_jnt, ax))
                                cmds.connectAttr(ax_src[0], '{}.input1{}'.format(md_mid, ax))
                            else:
                                cmds.setAttr('{}.input1{}'.format(md_mid, ax), cmds.getAttr('{}.scale{}'.format(fol_jnt, ax)))
                            cmds.connectAttr('{}.output{}'.format(blend_node, color_ax), '{}.input2{}'.format(md_mid, ax))
                            cmds.connectAttr('{}.output{}'.format(md_mid, ax), '{}.scale{}'.format(fol_jnt, ax))

            # cmds.pointConstraint(start, cmds.listRelatives(top_ribbon['second_ctrls'][0], p=True), mo=True)
            # cmds.pointConstraint(end, cmds.listRelatives(low_ribbon['second_ctrls'][1], p=True), mo=True)



        # ----------------------------------------------------------

        #Add Super Ctrl for Limb (Rename main Ik to SubIk) Orient to world based on limb position
        old_main_ik = ikfk['ik_fk'][4][0]
        correct_name = old_main_ik
        old_main_root = cmds.listRelatives(old_main_ik, p=True)[0]
        grandfather = cmds.listRelatives(cmds.listRelatives(old_main_ik, p=True)[0], p=True)

        cmds.rename(old_main_root, old_main_root.replace('_Ik', '_SubIk'))
        old_main_ik=cmds.rename(old_main_ik, old_main_ik.replace('_Ik', '_SubIk'))

        main_ik_ctrl = mt.curve(input='',
                              type=setup['ik_ctrl'],
                              rename=True,
                              custom_name=True,
                              name=correct_name,
                              size=ctrl_size*1.25)
        cmds.rotate(0,0,0)
        mt.assign_color(color=color)
        main_ik_root, main_ik_auto = mt.root_grp(autoRoot=True)
        cmds.delete(cmds.pointConstraint(old_main_ik, main_ik_root))

        # Fix Aim in pose A. Optional override keeps IK aligned to world.
        if force_ik_world:
            cmds.setAttr('{}.rotateX'.format(main_ik_root), 0)
            cmds.setAttr('{}.rotateY'.format(main_ik_root), 0)
            cmds.setAttr('{}.rotateZ'.format(main_ik_root), 0)
        else:
            if mode == 'Arms':
                #Make sure ik and fk are the same orientation
                dummy_up = cmds.duplicate(ikfk['ik_fk'][3][2])[0]
                cmds.setAttr(dummy_up+'.translateZ', -5)
                cmds.delete(cmds.aimConstraint(limb_b, main_ik_root,
                                               aimVector=(-1, 0, 0), upVector=(0, 1, 0),
                                               worldUpType='object', worldUpObject=dummy_up, mo=False), dummy_up)
            if mode == 'Legs':
                cmds.delete(cmds.aimConstraint(limb_b, main_ik_root,
                                               aimVector=(0, 1, 0), upVector=(0, 1, 0),
                                               worldUpType='vector', mo=False))
                cmds.setAttr('{}.rotateX'.format(main_ik_root), 0)
        cmds.parent(main_ik_root, grandfather)
        cmds.parent(cmds.listRelatives(old_main_ik, p=True)[0], main_ik_ctrl)

        if force_ik_world:
            cmds.setAttr('{}.rotateX'.format(main_ik_auto), 0)
            cmds.setAttr('{}.rotateY'.format(main_ik_auto), 0)
            cmds.setAttr('{}.rotateZ'.format(main_ik_auto), 0)
            cmds.setAttr('{}.rotateX'.format(main_ik_ctrl), 0)
            cmds.setAttr('{}.rotateY'.format(main_ik_ctrl), 0)
            cmds.setAttr('{}.rotateZ'.format(main_ik_ctrl), 0)

        #Vis
        #cmds.connectAttr(switch_locator + '.Switch_IK_FK', cmds.listRelatives(main_ik_ctrl, s=True)[0]+'.v')
        cmds.connectAttr(switch_locator + '.SubIk', cmds.listRelatives(old_main_ik, s=True)[0]+'.v')
        main_ikreverse_node = cmds.createNode('reverse', n=main_ik_ctrl + 'Main_Reverse')
        cmds.connectAttr(switch_locator + '.Switch_IK_FK', '{}.input.inputX'.format(main_ikreverse_node))
        cmds.connectAttr('{}.output.outputX'.format(main_ikreverse_node), cmds.listRelatives(main_ik_ctrl, s=True)[0]+'.v')

        mt.shape_with_attr(input=main_ik_ctrl, obj_name=switch_locator.replace(nc['locator'], ''), attr_name='')




        # ----------------------------------------------------------

        clean_rig_grp = cmds.group(em=True, n=side_guide.replace(nc['joint'], '_Rig' + nc['group']))
        clean_ctrl_grp = cmds.group(em=True, n=side_guide.replace(nc['joint'], nc['ctrl']) + nc['group'])

        # clean ribbons
        if create_ribbons:
            cmds.parent(top_ribbon['ribbon_plane'], top_ribbon['clean_rig_grp'], top_ribbon['fol_ribbon_grp'],
                        clean_rig_grp)
            cmds.parent(low_ribbon['ribbon_plane'], low_ribbon['clean_rig_grp'], low_ribbon['fol_ribbon_grp'],
                        clean_rig_grp)

            cmds.parent(root_mid_ctrl, clean_ctrl_grp)

            # # fix righ side
            # if str(side_guide).startswith(nc['right']):
            #     for handle in top_ribbon['handle_controllers'] + low_ribbon['handle_controllers']:
            #         cmds.setAttr('{}.scaleX'.format(cmds.listRelatives(handle, p=True)[0]), -1)
            #         cmds.rotate(0, 0, 180, '{}.cv[0:22]'.format(handle), r=True)

        # Flip Right Sides
        if str(side_guide).startswith(nc['right']):
            flip_twist_grp = cmds.group(em=True, n=side_guide.replace(nc['joint'], '_Flip' + nc['group']))
            cmds.parent(ikfk['upper_twist']['twist_grp'], ikfk['lower_twist']['twist_grp'], flip_twist_grp)
            cmds.parent(flip_twist_grp, clean_rig_grp)
            cmds.setAttr('{}.rotateX'.format(flip_twist_grp), 180)
            cmds.setAttr('{}.scaleX'.format(flip_twist_grp), -1)
            cmds.setAttr('{}.scaleY'.format(flip_twist_grp), -1)
            cmds.setAttr('{}.scaleZ'.format(flip_twist_grp), -1)

        else:
            cmds.parent(ikfk['upper_twist']['twist_grp'], clean_rig_grp)
            cmds.parent(ikfk['lower_twist']['twist_grp'], clean_rig_grp)

        cmds.parent(ikfk['ik_fk'][0][0], clean_rig_grp)
        cmds.parent(ikfk['ik_fk'][1][0], clean_rig_grp)
        cmds.parent(ikfk['ik_fk'][2][0], clean_rig_grp)

        cmds.parent(ikfk['ik_fk'][4][5][0], clean_rig_grp)
        cmds.parent(cmds.listRelatives(ikfk['ik_fk'][4][3], p=True), clean_rig_grp)

        cmds.scaleConstraint(limb_global_ctrl, ikfk['upper_twist']['twist_grp'], mo=True)
        cmds.scaleConstraint(limb_global_ctrl, ikfk['lower_twist']['twist_grp'], mo=True)

        cmds.parent(ikfk['ik_fk'][5][0], clean_ctrl_grp)
        cmds.parent(cmds.listRelatives(ikfk['ik_fk'][4][0], p=True), clean_ctrl_grp)
        cmds.parent(cmds.listRelatives(cmds.listRelatives(ikfk['ik_fk'][4][1], p=True), p=True), clean_ctrl_grp)

        # flip right rig  to right side -------------------------
        # check if the mirror attrs to Only_Right or mirror to True
        if cmds.getAttr('{}.Mirror'.format(config), asString=True) == 'Right_Only':

            mirror_ctrl_grp = mt.mirror_group(clean_ctrl_grp, world=True)
            cmds.parentConstraint(block_parent, ikfk['ik_fk'][5][0], mo=True)
            cmds.parentConstraint(block_parent, cmds.listRelatives(ikfk['ik_fk'][4][2], p=True), mo=True)
            clean_ctrl_grp = mirror_ctrl_grp

        elif cmds.getAttr('{}.Mirror'.format(config), asString=True) == 'True':
            ''
            if str(side_guide).startswith(nc['right']):
                mirror_ctrl_grp = mt.mirror_group(clean_ctrl_grp, world=True)

                cmds.parentConstraint(block_parent, ikfk['ik_fk'][5][0], mo=True)
                cmds.parentConstraint(block_parent, cmds.listRelatives(ikfk['ik_fk'][4][2], p=True), mo=True)
                #cmds.orientConstraint(block_parent, cmds.listRelatives(ikfk['upper_twist']['no_rotate'], p=True)[0], mo=True)

                clean_ctrl_grp = mirror_ctrl_grp
            else:
                cmds.parentConstraint(block_parent, ikfk['ik_fk'][5][0], mo=True)
                cmds.parentConstraint(block_parent, cmds.listRelatives(ikfk['ik_fk'][4][2], p=True), mo=True)
                #cmds.orientConstraint(block_parent, cmds.listRelatives(ikfk['upper_twist']['no_rotate'], p=True)[0], mo=True)

                clean_ctrl_grp = clean_ctrl_grp

        else:  # only left side

            cmds.parentConstraint(block_parent, ikfk['ik_fk'][5][0], mo=True)
            cmds.parentConstraint(block_parent, cmds.listRelatives(ikfk['ik_fk'][4][2], p=True), mo=True)
            #cmds.orientConstraint(block_parent, cmds.listRelatives(ikfk['upper_twist']['no_rotate'], p=True)[0], mo=True)


        # blends
        '''
        blends_grp = mt.root_grp(input = '', custom = True, custom_name = 'Blends', autoRoot = False, replace_nc = False)[0]
        blends_grp = blends_grp.replace('_AutoFK','')
        bends = cmds.getAttr('{}.Blends'.format(config).split(':'))
        for blend in bends:
            ''
            #cmds.orientConstraint()
        '''
        # clean ctrls
        cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])

        # parent rig
        cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))

        # connected
        cmds.parent(ikfk['ik_fk'][4][4], clean_ctrl_grp)

        # stretchy fixes to make it scalable
        main_jnt_grp = cmds.group(em=True, n=side_guide + '_Main' + nc['group'])
        cmds.parent(main_jnt_grp, cmds.listRelatives(ikfk['ik_fk'][0][0], p=True))
        cmds.parent(ikfk['ik_fk'][0][0], ikfk['ik_fk'][1][0], ikfk['ik_fk'][2][0], main_jnt_grp)


        # Fix Switch IKFK
        if str(side_guide).startswith(nc['right']):
            cmds.setAttr('{}.rotateX'.format(main_jnt_grp), 180)
            cmds.setAttr('{}.scaleX'.format(main_jnt_grp), -1)
            cmds.setAttr('{}.scaleY'.format(main_jnt_grp), -1)
            cmds.setAttr('{}.scaleZ'.format(main_jnt_grp), -1)

        cmds.scaleConstraint(limb_global_ctrl, main_jnt_grp, mo=True)

        temp_locator = cmds.spaceLocator()[0]
        cmds.delete(cmds.parentConstraint(ikfk['ik_fk'][0][0], temp_locator))
        piv_position = cmds.objectCenter(temp_locator, gl=True)
        cmds.xform(main_jnt_grp, pivots=piv_position)
        cmds.parentConstraint(block_parent, main_jnt_grp, mo=True)
        cmds.delete(temp_locator)

        # create bind Joints for the skin -------------------------
        # bind joints
        bind_joints = []
        bind_joint = ''

        if create_ribbons:
            to_bind = top_ribbon['fol_joints'] + low_ribbon['fol_joints']
            # Fix issue with orient in the aims up vectors
            cmds.parent(top_ribbon['ribbon_ctrl_grp'], top_ribbon['clean_ctrl_grp'], clean_ctrl_grp)
            cmds.parent(low_ribbon['ribbon_ctrl_grp'], low_ribbon['clean_ctrl_grp'], clean_ctrl_grp)
            handle_grp = cmds.group(low_ribbon['handle_controllers_roots'], top_ribbon['handle_controllers_roots'], n=name+'_Handle'+nc['ctrl']+nc['group'])
            if side_guide.startswith(nc['right']):
                cmds.setAttr('{}.rotateX'.format(handle_grp), 180)
                cmds.setAttr('{}.scaleX'.format(handle_grp), -1)
                cmds.setAttr('{}.scaleY'.format(handle_grp), -1)
                cmds.setAttr('{}.scaleZ'.format(handle_grp), -1)
        else:
            to_bind = ikfk['upper_twist']['joints'] + ikfk['lower_twist']['joints']

        cmds.select(cl=True)

        for jnt in to_bind:
            try:
                cmds.select(bind_joint)
            except:
                pass
            # bind_joint = mt.duplicate_change_names( input = jnt, hi = False, search=nc['joint'], replace = nc['joint_bind'])[0]
            # cmds.delete(cmds.pickWalk(bind_joints, d='down'))#clean the dirty constraint
            # cmds.delete(cmds.listRelatives(bind_joint, ad=True))
            bind_joint = cmds.joint(n=jnt.replace(nc['joint'], nc['joint_bind']))
            # mt.orient_joint(input=bind_joint)
            cmds.delete(cmds.parentConstraint(jnt, bind_joint, mo=False))
            cmds.delete(cmds.scaleConstraint(jnt, bind_joint, mo=False))
            cmds.makeIdentity(a=True, t=True, s=True, r=True)
            cmds.parentConstraint(jnt, bind_joint, mo=False)
            cmds.scaleConstraint(jnt, bind_joint, mo=True)
            cmds.setAttr('{}.segmentScaleCompensate'.format(bind_joint), 0)
            cmds.setAttr('{}.inheritsTransform'.format(bind_joint), 0)

            # cmds.connectAttr('{}.scaleX'.format(jnt),'{}.scaleX'.format(bind_joint) )
            # cmds.connectAttr('{}.scaleY'.format(jnt),'{}.scaleY'.format(bind_joint) )
            # cmds.connectAttr('{}.scaleZ'.format(jnt),'{}.scaleX'.format(bind_joint) )

            # clean bind joints and radius to 1.5
            print(bind_joint)

            bind_joints.append(bind_joint)
            cmds.setAttr('{}.radius'.format(bind_joint), 2)


        # Finish -------------------------------------------

        # game parents for bind joints
        game_parent = cmds.getAttr('{}.SetGameParent'.format(config))
        if side_guide.startswith(nc['right']):
            game_parent = game_parent.replace(nc['left'], nc['right'])

        if cmds.objExists(game_parent):
            cmds.parent(bind_joints[0], game_parent)

        else:
            bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])
            if cmds.objExists(bind_jnt_grp):
                cmds.parent(bind_joints[0], bind_jnt_grp)


        #Turn Fk As Default if arms
        if mode == 'Arms':
            cmds.setAttr(switch_locator+'.Switch_IK_FK', 1)
            cmds.setAttr(ikfk['ik_fk'][3][0]+'.RotateOrder', 3)

        # Twist offset attrs on switch locator
        mt.line_attr(input=switch_locator, name='Twist')

        # Main Twist attr
        main_twist_attr = mt.new_attr(input=switch_locator, name='MainTwist', min=False, max=False, default=0)
        cmds.connectAttr(main_twist_attr, '{}.twist'.format(ikfk['ik_fk'][4][3]))

        upper_twist_attr = mt.new_attr(input=switch_locator, name='UpperTwist', min=False, max=False, default=0)
        lower_twist_attr = mt.new_attr(input=switch_locator, name='LowerTwist', min=False, max=False, default=0)
        cmds.connectAttr(upper_twist_attr, '{}.twist'.format(ikfk['upper_twist']['ik_spline']))
        cmds.connectAttr(lower_twist_attr, '{}.twist'.format(ikfk['lower_twist']['ik_spline']))

        # Roll offset attrs on switch locator
        upper_roll_attr = mt.new_attr(input=switch_locator, name='UpperRoll', min=False, max=False, default=0)
        lower_roll_attr = mt.new_attr(input=switch_locator, name='LowerRoll', min=False, max=False, default=0)
        cmds.connectAttr(upper_roll_attr, '{}.roll'.format(ikfk['upper_twist']['ik_spline']))
        cmds.connectAttr(lower_roll_attr, '{}.roll'.format(ikfk['lower_twist']['ik_spline']))

        #mt.line_attr(input=switch_locator, name='MT')

        # #Add proxy attrs to main controllers
        # #Fk Attrs
        # mt.proxy_this_attrs(attrs_from=switch_locator, attrs_to=ikfk['ik_fk'][3][0],
        #                     attrs_to_proxy=['_________'])
        #
        # #Ik Attrs
        # mt.proxy_this_attrs(attrs_from=switch_locator, attrs_to=main_ik_ctrl,
        #                     attrs_to_proxy=['_________', 'TopIk', 'SubIk', 'Stretch_On','Lower_Length','Upper_Length','Pole_Vector_Lock','Volume'])
        #
        # #Bendy
        # mt.proxy_this_attrs(attrs_from=switch_locator, attrs_to=main_mid_ctrl,
        #                     attrs_to_proxy=['_________', 'BendyMain', 'BendyOffsets', 'BendyEnds', 'BendyTweeks'])

        # Bendy Vis Attrs -> Mid Bendy Ctrl (R_KneeMidBendy / L_ElbowMidBendy)
        if create_ribbons:
            mt.proxy_this_attrs(attrs_from=switch_locator, attrs_to=main_mid_ctrl,
                                attrs_to_proxy=['BendyMain', 'BendyOffsets', 'BendyEnds', 'BendyTweeks'] + curve_attr_names)

        # the right side is built on the left and flipped, so the global scale controller is placed now, on the
        # final limb start, and the controllers follow it from here
        cmds.delete(cmds.parentConstraint(ikfk['ik_fk'][0][0], limb_global_root, mo=False))
        cmds.parentConstraint('Rig_Ctrl_Grp', limb_global_root, mo=True)
        cmds.scaleConstraint('Rig_Ctrl_Grp', limb_global_root, mo=True)
        cmds.parentConstraint(limb_global_ctrl, clean_ctrl_grp, mo=True)
        cmds.scaleConstraint(limb_global_ctrl, clean_ctrl_grp, mo=True)

        upper_count = len(top_ribbon['fol_joints'] if create_ribbons else ikfk['upper_twist']['joints'])
        limbs_data.append({'mode': mode, 'right': side_guide.startswith(nc['right']),
                           'fk_ctrls': ikfk['ik_fk'][3], 'ik_ctrl': main_ik_ctrl, 'sub_ik_ctrl': old_main_ik,
                           'top_ik_ctrl': ikfk['ik_fk'][4][2], 'switch': switch_locator + '.Switch_IK_FK',
                           'upper_binds': bind_joints[:upper_count], 'lower_binds': bind_joints[upper_count:],
                           'bendy_ctrls': [top_ribbon['second_ctrls'], low_ribbon['second_ctrls']] if create_ribbons else None,
                           'ribbons': [top_ribbon, low_ribbon] if create_ribbons else None,
                           'tweak_ctrls': top_ribbon['ribbon_ctrls'] + low_ribbon['ribbon_ctrls'] if create_ribbons else [],
                           'main_joints': ikfk['ik_fk'][0], 'mid_ctrl': main_mid_ctrl if create_ribbons else None,
                           'curve_attrs': curve_attrs if create_ribbons else None})

    # studio orients for the fk controllers
    if orients == 'SN':
        for data in limbs_data:
            if data['mode'] not in SN_ORIENTS:
                cmds.warning('Limb: SN orients only know arms and legs, {} keeps the default'.format(data['fk_ctrls'][0]))
                continue
            right_ctrls = data['fk_ctrls'] if data['right'] else []
            apply_custom_orients(data['fk_ctrls'], SN_ORIENTS[data['mode']], right_ctrls)

    # bendy path: straight or arc through start -> mid bendy controller -> end, no wobble
    for data in limbs_data:
        if not data['ribbons']:
            continue
        top, low = data['ribbons']
        start, end = [_world_position(j) for j in (data['main_joints'][0], data['main_joints'][2])]
        mid = _world_position(data['mid_ctrl'])
        attrs = data['curve_attrs']
        name = data['mid_ctrl'].replace(nc['ctrl'], '')

        # how bent the limb is: 0 straight, 1 at 90 degrees or more (1 - cos of the elbow angle)
        directions = []
        for num, (a, b) in enumerate([(data['main_joints'][0], data['main_joints'][1]),
                                      (data['main_joints'][1], data['main_joints'][2])]):
            unit = cmds.createNode('vectorProduct', n='{}_Bone{}_VectorProduct'.format(name, num))
            cmds.setAttr(unit + '.operation', 0)
            cmds.setAttr(unit + '.normalizeOutput', 1)
            cmds.connectAttr(_vector_op('{}_Bone{}_PlusMinusAverage'.format(name, num), _world_position(b), _world_position(a), 2),
                             unit + '.input1')
            directions.append(unit + '.output')
        cosine = cmds.createNode('vectorProduct', n=name + '_Bend_VectorProduct')
        cmds.setAttr(cosine + '.operation', 1)
        cmds.connectAttr(directions[0], cosine + '.input1')
        cmds.connectAttr(directions[1], cosine + '.input2')
        bend = cmds.createNode('clamp', n=name + '_Bend_Clamp')
        cmds.setAttr(bend + '.maxR', 1)
        cmds.connectAttr(_add(name + '_Bend_AddDoubleLinear', _mult(name + '_Bend_MultDoubleLinear', cosine + '.outputX', -1), 1),
                         bend + '.inputR')
        auto_curve = _mult(name + '_AutoCurve_MultDoubleLinear', attrs['auto'], bend + '.outputR')
        base_curve = _add(name + '_Curve_AddDoubleLinear', attrs['curve'], auto_curve)

        def segment_curve(label, offset):
            total = cmds.createNode('clamp', n='{}_{}Curve_Clamp'.format(name, label))
            cmds.setAttr(total + '.minR', -10)
            cmds.setAttr(total + '.maxR', 10)
            cmds.connectAttr(_add('{}_{}Curve_AddDoubleLinear'.format(name, label), base_curve, offset), total + '.inputR')
            return _mult('{}_{}Curve_MultDoubleLinear'.format(name, label), total + '.outputR', 0.1)

        segments = [(top, (start, mid, end), segment_curve('Upper', attrs['upper']),
                     _mult(name + '_StartEase_MultDoubleLinear', attrs['start_ease'], 0.1), True),
                    (low, (mid, end, start), segment_curve('Lower', attrs['lower']),
                     _mult(name + '_EndEase_MultDoubleLinear', attrs['end_ease'], 0.1), False)]
        for ribbon, (seg_start, seg_end, other), curve, ease, ease_at_start in segments:
            offsets = [bendy_move(ctrl, ctrl) for ctrl in ribbon['second_ctrls']]
            seg_name = ribbon['second_ctrls'][0].replace('Start_Bendy' + nc['ctrl'], '_BendyPath')
            bendy_segment_path(seg_name, seg_start, seg_end, other, curve, ribbon['ribbon_ctrls'],
                               offsets[0], offsets[1], ribbon['middle_surface'], ribbon['pin_surface'], ease, ease_at_start)
            # the old aim locators are not needed anymore
            cmds.delete(ribbon['forward_aim_grp'])

    # controllers scale: fk controllers in fk, ik controllers in ik, bendy controllers fade along their segment
    scaled_ctrls = []
    for data in limbs_data:
        fk_on = data['switch']
        ik_on = cmds.createNode('reverse', n=data['fk_ctrls'][0] + '_ScaleIk_Reverse')
        cmds.connectAttr(fk_on, ik_on + '.inputX')
        ik_on += '.outputX'

        influences = {}
        segments = [(data['upper_binds'], True), (data['lower_binds'], False)]
        for binds, is_upper in segments:
            for num, jnt in enumerate(binds):
                t = float(num) / (len(binds) - 1) if len(binds) > 1 else 1.0
                fk_ctrl = data['fk_ctrls'][0] if is_upper else data['fk_ctrls'][1]
                items = [(fk_ctrl, fk_on)]
                if is_upper:
                    items.append((data['top_ik_ctrl'], ik_on))
                elif t > 1e-4:
                    items.append((data['fk_ctrls'][2], _weight_plug(jnt + '_WristFkScale_MultDoubleLinear', t, fk_on)))
                    for ctrl in [data['ik_ctrl'], data['sub_ik_ctrl']]:
                        items.append((ctrl, _weight_plug('{}_{}Scale_MultDoubleLinear'.format(jnt, ctrl), t, ik_on)))
                if data['bendy_ctrls']:
                    start_ctrl, end_ctrl = data['bendy_ctrls'][0 if is_upper else 1]
                    if 1 - t > 1e-4:
                        items.append((start_ctrl, 1 - t))
                    if t > 1e-4:
                        items.append((end_ctrl, t))
                influences[jnt] = items

        # bendy tweakers: each one scales its own bind joint
        for tweak_ctrl, jnt in zip(data['tweak_ctrls'], data['upper_binds'] + data['lower_binds']):
            influences[jnt].append((tweak_ctrl, 1.0))

        ctrls = data['fk_ctrls'] + [data['ik_ctrl'], data['sub_ik_ctrl'], data['top_ik_ctrl']]
        if data['bendy_ctrls']:
            ctrls += data['bendy_ctrls'][0] + data['bendy_ctrls'][1]
        ctrls += data['tweak_ctrls']
        free_controller_scale(ctrls)
        scaled_ctrls += ctrls
        data['scale_influences'] = influences

    # follicles keep the limb out of parallel evaluation, swap them for uvPins
    follicles_to_uv_pins([f for f in cmds.ls(type='follicle') if f not in old_follicles])

    # swap the constraints of this block for matrix nodes (faster playback)
    new_constraints = [c for c in cmds.ls(type='constraint') if c not in old_constraints]
    kept = constraints_to_matrix(new_constraints, unscaled_targets=set(scaled_ctrls))
    replaced = len([c for c in new_constraints if not cmds.objExists(c)])
    print('Limb matrix swap: {} constraints replaced, {} kept {}'.format(replaced, len(kept), kept))

    # bind joints get the controllers scale (after the swap, it multiplies into their scale channels)
    for data in limbs_data:
        scale_bind_joints(data['upper_binds'] + data['lower_binds'], data['scale_influences'])

    # break the switch shape cycle so the limb evaluates in parallel
    for switch_shape in switch_shapes:
        switch_attrs_to_data_node(switch_shape)
