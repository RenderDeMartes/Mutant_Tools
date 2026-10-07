from __future__ import absolute_import, division
from maya import cmds
import maya.api.OpenMaya as om
import json
import math
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
PYBLOCK_NAME = 'exec_hand'

FINGERS = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
# default finger guides in palm space: phalanges, x, y, z, spacing (plus the thumb turned -50 in Y)
FINGER_GUIDES = {'Index': (5, 4, 0, 3, 3), 'Middle': (5, 4, 0, 0, 4.5), 'Ring': (5, 4, 0, -3, 4),
                 'Pinky': (5, 4, 0, -6, 3), 'Thumb': (4, 3, 0, 7, 3)}
THUMB_ROTATE_Y = -50
FINGER_CUPS = {'Thumb': 'InnerCup', 'Ring': 'OutterCup', 'Pinky': 'OutterCup'}

# Studio orients: same result as the Custom_Biped_Orients block (FixFingers and the hand part of FixArms)
SN_FINGERS_ROTATE = [-90, 90, 0]
SN_WRIST_ROTATE = [0, 0, -90]

#---------------------------------------------

def create_hand_block(name = 'Hand'):

    # Read name conventions as nc[''] and setup as seup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-3]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '006_Hand.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()

    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''
    fingers = mt.ask_name(text = 'Thumb_Index_Middle_Ring_Pinky', ask_for = 'Comfirm fingers (Delete if not needed)')

    block = mt.create_block(name = name, icon = 'Hand',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]

    # the finger attrs start as the fingers asked for, they add or remove the guides later (on_attr_changed)
    for finger in FINGERS:
        if cmds.attributeQuery(finger, n=config, exists=True):
            cmds.setAttr('{}.{}'.format(config, finger), finger in fingers)

    cmds.select (cl = True)
    palm = mt.create_joint_guide(name = name + '_Palm')

    def genericFinger (finger, phalanges,x,y,z,mult):
        cmds.select (palm)
        guides = []
        for f in range(phalanges):
            try:old_guide = guide
            except:pass
            guide = mt.create_joint_guide(name = (name + '_' + finger + '_0' + str (f)))
            cmds.move(f*mult,0,0)
            cmds.move (x,y,z, r = True)
            try: cmds.parent(guide, old_guide)
            except:pass
            guides.append(guide)
        return guides

    if 'Index' in fingers:
        indexs = genericFinger ('Index', *FINGER_GUIDES['Index'])
        cmds.parent(indexs[0], palm)

    if 'Middle' in fingers:
        middles = genericFinger ('Middle', *FINGER_GUIDES['Middle'])
        cmds.parent(middles[0], palm)

    if 'Ring' in fingers:
        rings = genericFinger ('Ring', *FINGER_GUIDES['Ring'])
        cmds.parent(rings[0], palm)

    if 'Pinky' in fingers:
        pinkys = genericFinger ('Pinky', *FINGER_GUIDES['Pinky'])
        cmds.parent(pinkys[0], palm)

    if 'Thumb' in fingers:
        thumbs = genericFinger ('Thumb', *FINGER_GUIDES['Thumb'])
        cmds.setAttr ('{}.rotateY'.format(thumbs[0]), THUMB_ROTATE_Y)

        inner_cup = mt.create_joint_guide(name = (name + '_' + 'InnerCup' ))
        cmds.delete(cmds.parentConstraint(palm, thumbs[0],inner_cup, mo=False))

        cmds.parent(thumbs[0], inner_cup)
        cmds.parent(inner_cup, palm)

    #create Outter Cup joints
    if 'Pinky' in fingers or 'Ring' in fingers:
        outter_cup = mt.create_joint_guide(name = (name + '_' + 'OutterCup' ))

        # Position the outter cup - prefer pinky, fallback to ring
        if 'Pinky' in fingers:
            cmds.delete(cmds.parentConstraint(palm, pinkys[0], outter_cup, mo=False))
        elif 'Ring' in fingers:
            cmds.delete(cmds.parentConstraint(palm, rings[0], outter_cup, mo=False))

        if 'Pinky' in fingers:
            cmds.parent(pinkys[0], outter_cup)

        if 'Ring' in fingers:
            cmds.parent(rings[0], outter_cup)

        cmds.parent(outter_cup, palm)

    cmds.parent(palm, block)

    cmds.move(2,0,0 , palm)

    cmds.select(block)
    print('{} Created Successfully'.format(name))

#create_hand_block()

#-------------------------
# Builder hook (Utils/Rigging/block_hooks.py): turning the Thumb / Index / Middle / Ring / Pinky attrs off
# deletes that finger guides, turning them on brings them back where they were (or at the default place).

def on_attr_changed(config, attr, value):
    if attr in FINGERS:
        set_finger_guides(config, attr, bool(value))


def _hand_palm_guide(config):
    """Block container and palm guide of a hand config."""
    nc = mt.import_configs()[0]
    for block in cmds.listConnections(config + '.nodeState', s=False, d=True) or []:
        for child in cmds.listRelatives(block, c=True, type='joint') or []:
            if child.endswith('_Palm' + nc['guide']):
                return block, child
    return None, None


def _finger_chain(root):
    chain = [root]
    while True:
        children = cmds.listRelatives(chain[-1], c=True, type='joint') or []
        if not children:
            return chain
        chain.append(children[0])


def _stored_attr(finger):
    return 'Stored{}Guides'.format(finger)


def _default_finger_matrices(finger):
    """Palm space matrices of a new finger, same place as create_hand_block."""
    phalanges, x, y, z, spacing = FINGER_GUIDES[finger]
    root = om.MTransformationMatrix()
    root.setTranslation(om.MVector(x, y, z), om.MSpace.kTransform)
    if finger == 'Thumb':
        root.setRotation(om.MEulerRotation(0, math.radians(THUMB_ROTATE_Y), 0))
    root = root.asMatrix()
    matrices = []
    for num in range(phalanges):
        offset = om.MTransformationMatrix()
        offset.setTranslation(om.MVector(num * spacing, 0, 0), om.MSpace.kTransform)
        matrices.append(offset.asMatrix() * root)
    return matrices


def set_finger_guides(config, finger, on):
    """Delete (on=False) or create (on=True) the guides of one finger. Deleted guides are stored in palm
    space on the block, so they come back in the same place. The cups are kept."""
    block, palm = _hand_palm_guide(config)
    if not palm:
        cmds.warning('{}: no palm guide found for {}'.format(config, finger))
        return
    root = palm.replace('Palm', finger + '_00')
    palm_world = om.MMatrix(cmds.getAttr(palm + '.worldMatrix[0]'))
    stored = '{}.{}'.format(block, _stored_attr(finger))

    if not on:
        if not cmds.objExists(root):
            return
        palm_inverse = palm_world.inverse()
        matrices = [list(om.MMatrix(cmds.getAttr(jnt + '.worldMatrix[0]')) * palm_inverse) for jnt in _finger_chain(root)]
        if not cmds.attributeQuery(_stored_attr(finger), n=block, exists=True):
            cmds.addAttr(block, ln=_stored_attr(finger), dt='string')
        cmds.setAttr(stored, json.dumps(matrices), type='string')
        cmds.delete(root)
        return

    if cmds.objExists(root):
        return
    matrices = None
    if cmds.attributeQuery(_stored_attr(finger), n=block, exists=True):
        try:
            matrices = [om.MMatrix(m) for m in json.loads(cmds.getAttr(stored) or '[]')]
        except (ValueError, TypeError):
            matrices = None
    matrices = matrices or _default_finger_matrices(finger)

    cup = palm.replace('Palm', FINGER_CUPS[finger]) if finger in FINGER_CUPS else None
    name = palm[:-len('_Palm' + mt.import_configs()[0]['guide'])]
    guides = []
    for num, matrix in enumerate(matrices):
        guide = mt.create_joint_guide(name='{}_{}_0{}'.format(name, finger, num))
        parent = guides[-1] if guides else palm
        cmds.parent(guide, parent)
        # local channels with setAttr (an xform -ws -m does not redo right)
        local = om.MTransformationMatrix(matrix * palm_world * om.MMatrix(cmds.getAttr(parent + '.worldInverseMatrix[0]')))
        cmds.setAttr(guide + '.translate', *local.translation(om.MSpace.kTransform))
        cmds.setAttr(guide + '.rotate', *[math.degrees(v) for v in local.rotation()])
        cmds.setAttr(guide + '.jointOrient', 0, 0, 0)
        cmds.setAttr(guide + '.scale', *local.scale(om.MSpace.kTransform))
        guides.append(guide)

    if cup:
        if not cmds.objExists(cup):
            # new cup between the palm and the finger, like create_hand_block
            cup = mt.create_joint_guide(name='{}_{}'.format(name, FINGER_CUPS[finger]))
            cmds.delete(cmds.parentConstraint(palm, guides[0], cup, mo=False))
            cmds.parent(cup, palm)
        cmds.parent(guides[0], cup)

#-------------------------
# Matrix helpers: v002 has no constraints, every joint reads its controller world matrix through
# multMatrix / decomposeMatrix nodes (cheaper to evaluate, the hand runs in parallel). Rest offsets are
# read at build time with the rig in rest pose.

AXES = 'XYZ'


def _world(node):
    return om.MMatrix(cmds.getAttr(node + '.worldMatrix[0]'))


def _position(node):
    return om.MVector(cmds.xform(node, q=True, ws=True, t=True))


def _mult_matrix(name, items):
    """multMatrix of plugs and constant MMatrix values, in order. Returns the output plug."""
    node = cmds.createNode('multMatrix', n=name)
    for i, item in enumerate(items):
        if isinstance(item, om.MMatrix):
            cmds.setAttr('{}.matrixIn[{}]'.format(node, i), list(item), type='matrix')
        else:
            cmds.connectAttr(item, '{}.matrixIn[{}]'.format(node, i))
    return node + '.matrixSum'


def _offset_world(driven, source):
    """[rest offset, source world]: driven keeps its rest place relative to source. The offset is always
    the first item, even when it is identity, so tools that re orient controllers later (Custom_Biped_Orients)
    can find it and keep the joints in place."""
    return [_world(driven) * _world(source).inverse(), source + '.worldMatrix[0]']


def _offset_world_plug(name, driven, source):
    return _mult_matrix(name, _offset_world(driven, source))


def drive(driven, world_items, channels=('translate', 'rotate', 'scale'), reparentable=False):
    """driven channels follow a world matrix (list of multMatrix items): local = world * parent inverse.
    The joint orient is taken out of the rotation.
    Nothing of the driven node goes back into its own nodes (its parentInverseMatrix / rotateOrder would be a
    cycle for the evaluation manager, every joint its own cluster): the parent worldInverseMatrix and a
    fixed rotate order. reparentable keeps the driven parentInverseMatrix, for nodes other tools re parent
    (the bind root under a game parent)."""
    parent = (cmds.listRelatives(driven, p=True) or [None])[0]
    if reparentable:
        parent_inverse = [driven + '.parentInverseMatrix[0]']
    else:
        parent_inverse = [parent + '.worldInverseMatrix[0]'] if parent else []
    local = _mult_matrix(driven + '_Local_MultMatrix', list(world_items) + parent_inverse)
    decompose = cmds.createNode('decomposeMatrix', n=driven + '_Local_DecomposeMatrix')
    cmds.connectAttr(local, decompose + '.inputMatrix')
    rotate_order = cmds.getAttr(driven + '.rotateOrder')
    cmds.setAttr(decompose + '.inputRotateOrder', rotate_order)
    if 'translate' in channels:
        cmds.connectAttr(decompose + '.outputTranslate', driven + '.translate', f=True)
    if 'scale' in channels:
        cmds.connectAttr(decompose + '.outputScale', driven + '.scale', f=True)
    if 'rotate' in channels:
        rotate = decompose + '.outputRotate'
        if cmds.nodeType(driven) == 'joint':
            joint_orient = cmds.getAttr(driven + '.jointOrient')[0]
            if any(abs(v) > 1e-6 for v in joint_orient):
                # local = S R JO T, the 3x3 of local * JO^-1 is S R (T only moves the translation)
                orient = om.MEulerRotation([om.MAngle(v, om.MAngle.kDegrees).asRadians() for v in joint_orient])
                rotate_local = _mult_matrix(driven + '_Rotate_MultMatrix', [local, orient.asMatrix().inverse()])
                rotate_decompose = cmds.createNode('decomposeMatrix', n=driven + '_Rotate_DecomposeMatrix')
                cmds.connectAttr(rotate_local, rotate_decompose + '.inputMatrix')
                cmds.setAttr(rotate_decompose + '.inputRotateOrder', rotate_order)
                rotate = rotate_decompose + '.outputRotate'
        cmds.connectAttr(rotate, driven + '.rotate', f=True)


def follow_target(jnt, ctrl, nc):
    """Hidden transform under the ctrl at the joint rest place, the joint follows it. Tools that re orient
    ctrls (Custom_Biped_Orients) keep the ctrl children where they are, so the joints stay right."""
    target = cmds.createNode('transform', n=jnt + '_Follow' + nc['null'], p=ctrl)
    cmds.xform(target, ws=True, m=list(_world(jnt)))
    return target


def _inverse_scale_matrix(name, scale_plug, rest_scale):
    """Matrix that undoes a scale change from its rest value (rest / current)."""
    divide = cmds.createNode('multiplyDivide', n=name + '_InverseScale_MultiplyDivide')
    cmds.setAttr(divide + '.operation', 2)
    cmds.setAttr(divide + '.input1', *rest_scale)
    if all(v > 0 for v in rest_scale):
        # clamp so scaling to 0 never divides by zero
        clamp = cmds.createNode('clamp', n=name + '_InverseScale_Clamp')
        cmds.setAttr(clamp + '.min', 0.001, 0.001, 0.001)
        cmds.setAttr(clamp + '.max', 1e6, 1e6, 1e6)
        cmds.connectAttr(scale_plug, clamp + '.input')
        cmds.connectAttr(clamp + '.output', divide + '.input2')
    else:
        cmds.connectAttr(scale_plug, divide + '.input2')
    compose = cmds.createNode('composeMatrix', n=name + '_InverseScale_ComposeMatrix')
    cmds.connectAttr(divide + '.output', compose + '.inputScale')
    return compose + '.outputMatrix'


def free_controller_scale(ctrls, skip=()):
    """Like Spine / Limb v002: a ctrl scale scales its own joint, the ctrls under it do not inherit it."""
    for ctrl in ctrls:
        for axis in [''] + list(AXES):
            cmds.setAttr('{}.scale{}'.format(ctrl, axis), lock=False)
        for axis in AXES:
            cmds.setAttr('{}.scale{}'.format(ctrl, axis), keyable=True)
        rest = cmds.getAttr(ctrl + '.scale')[0]
        if all(v > 0 for v in rest):
            cmds.transformLimits(ctrl, sx=(0.001, 1), sy=(0.001, 1), sz=(0.001, 1),
                                 esx=(True, False), esy=(True, False), esz=(True, False))
        inverse = None
        for child in cmds.listRelatives(ctrl, c=True, type='transform') or []:
            if child in skip or cmds.listConnections(child + '.offsetParentMatrix', s=True, d=False):
                continue
            inverse = inverse or _inverse_scale_matrix(ctrl, ctrl + '.scale', rest)
            cmds.connectAttr(inverse, child + '.offsetParentMatrix', f=True)


def _cup_matrix(pivot, aim, back):
    """X from the pivot to aim (the palm fold line), Y towards the back of the hand."""
    x_axis = (aim - pivot).normal()
    z_axis = (x_axis ^ back).normal()
    y_axis = (z_axis ^ x_axis).normal()
    return om.MMatrix([x_axis.x, x_axis.y, x_axis.z, 0, y_axis.x, y_axis.y, y_axis.z, 0,
                       z_axis.x, z_axis.y, z_axis.z, 0, pivot.x, pivot.y, pivot.z, 1])


def _place_joint(jnt, matrix):
    """Move and orient a joint without moving its children."""
    children = [cmds.parent(child, world=True)[0] for child in cmds.listRelatives(jnt, c=True, type='joint') or []]
    cmds.setAttr(jnt + '.jointOrient', 0, 0, 0)
    cmds.xform(jnt, ws=True, m=list(matrix))
    cmds.makeIdentity(jnt, apply=True, r=True, s=True)
    for child in children:
        cmds.parent(child, jnt)


def auto_cup_placement(palm):
    """Anatomical cup pivots. Each cup rolls around a palm fold line that starts near the wrist and runs
    along the fingers: the thenar fold (thumb side) between the thumb and index metacarpals, the
    hypothenar fold (pinky side) between the middle and ring metacarpals. Cup joints get X along that
    line, so rotating X folds that side of the palm."""
    normal = _palm_normal(palm)
    if normal is None:
        return
    back = -normal

    def positions(fingers, segment):
        return [_position(palm.replace('Palm', '{}_{}'.format(finger, segment))) for finger in fingers
                if cmds.objExists(palm.replace('Palm', '{}_{}'.format(finger, segment)))]

    def mean(points):
        return sum(points, om.MVector()) / len(points) if points else None

    wrist = _position(palm)
    fingers = ['Index', 'Middle', 'Ring', 'Pinky']
    forward = (mean(positions(fingers, '01')) - mean(positions(fingers, '00'))).normal()

    def fold(side_fingers, other_fingers):
        """Pivot between the two groups of metacarpals, pulled back towards the wrist."""
        base = mean(positions(side_fingers[:1], '00') + positions(other_fingers[:1], '00'))
        pivot = base - forward * (((base - wrist) * forward) * 0.65)
        return _cup_matrix(pivot, pivot + forward, back)

    inner_cup = palm.replace('Palm', 'InnerCup')
    index = [f for f in ['Index', 'Middle'] if positions([f], '00')]
    if cmds.objExists(inner_cup) and positions(['Thumb'], '00') and index:
        _place_joint(inner_cup, fold(['Thumb'], index))

    outter_cup = palm.replace('Palm', 'OutterCup')
    outer = [f for f in ['Ring', 'Pinky'] if positions([f], '00')]
    neighbour = [f for f in ['Middle', 'Index'] if positions([f], '00')]
    if cmds.objExists(outter_cup) and outer:
        _place_joint(outter_cup, fold(outer, neighbour))


def _close_sign(jnt, palm):
    """+1 when a positive rotateZ closes this joint towards the palm."""
    normal = _palm_normal(palm)
    child = (cmds.listRelatives(jnt, c=True, type='joint') or [None])[0]
    if normal is None or not child:
        return -1  # default guides: +Z opens the hand
    matrix = _world(jnt)
    z_axis = om.MVector(matrix[8], matrix[9], matrix[10])
    return 1 if (z_axis ^ (_position(child) - _position(jnt))) * normal > 0 else -1


# degrees per attr unit (100 = full pose) for the curl of each segment, positive closes the hand
HAND_POSES = {
    'Fist': {'fingers': [0.9, 1.0, 0.7], 'thumb': [0.4, 0.6]},
    'Point': {'fingers': [0.9, 1.0, 0.7], 'thumb': [0.4, 0.6], 'Index': [0, 0, 0]},
    'Claw': {'fingers': [-0.25, 0.8, 0.7], 'thumb': [0.2, 0.5]},
    'Flat': {'fingers': [-0.15, -0.1, -0.05], 'thumb': [-0.1, -0.1]},
}


def settle_rest_pose(side_guide, constraints, extra=()):
    """The rig joints get the same constraints v001 had (some without maintain offset), they are evaluated
    once and deleted, the matrix nodes take the joints from there. With mirrored guides (Right_Only) those
    constraints flip some joint axes, this keeps the result the same as v001."""
    joints = [side_guide] + (cmds.listRelatives(side_guide, ad=True, type='joint') or [])
    constraints = constraints + [c for jnt in joints for c in cmds.listRelatives(jnt, type='constraint') or []]
    # v001 made its constraints with segment scale compensate on and turned it off at the end
    for jnt in joints:
        cmds.setAttr(jnt + '.segmentScaleCompensate', 0)
    nodes = joints + list(extra)
    for node in nodes:
        cmds.getAttr(node + '.worldMatrix[0]')
    values = {}
    for node in nodes:
        values[node] = [cmds.getAttr('{}.{}'.format(node, attr))[0] for attr in ['translate', 'rotate', 'scale']]
    cmds.delete(list(set(constraints)))
    for jnt, (translate, rotate, scale) in values.items():
        cmds.setAttr(jnt + '.translate', *translate)
        cmds.setAttr(jnt + '.rotate', *rotate)
        cmds.setAttr(jnt + '.scale', *scale)


def v001_bind_offsets(binds, nc):
    """v001 drove every bind joint with a parent + scale constraint and no inherit transform. On mirrored
    sides that leaves some bind joints with a pair of axes flipped compared to their rig joint (the
    constraints split the negative scale differently). Same constraints here, evaluated once and deleted,
    so the bind skeleton (and anything exported or skinned to it) stays the same as v001.
    Returns {bind joint: offset from its rig joint world matrix}."""
    constraints = []
    for jnt in binds[1:] + binds[:1]:
        driver = jnt.replace(nc['joint_bind'], nc['joint'])
        constraints += [cmds.parentConstraint(driver, jnt)[0], cmds.scaleConstraint(driver, jnt)[0]]
        cmds.setAttr(jnt + '.inheritsTransform', 0)
    worlds = dict((jnt, _world(jnt)) for jnt in binds)
    cmds.delete(constraints)
    offsets = {}
    for jnt in binds:
        cmds.setAttr(jnt + '.inheritsTransform', 1)
        offsets[jnt] = worlds[jnt] * _world(jnt.replace(nc['joint_bind'], nc['joint'])).inverse()
    return offsets


def copy_local_channels(source, driven):
    """The bind joints are a copy of the rig joints hierarchy, their children only need the same local channels."""
    for attr in ['translate', 'rotate', 'scale']:
        cmds.connectAttr('{}.{}'.format(source, attr), '{}.{}'.format(driven, attr), f=True)


#-------------------------
# Controllers

def orient_ctrls(ctrls_rotates):
    """Put an OrientChange group above every ctrl rotated by its value (Orients = SN), the ctrl children
    and the joints stay where they are (the rest constraints are made again with maintain offset, like
    Custom_Biped_Orients does)."""
    remake = []
    for ctrl, rotate in ctrls_rotates:
        for constraint in set(cmds.listConnections(ctrl, type='constraint', s=True, d=True) or []):
            for jnt in set(cmds.listConnections(constraint, s=False, d=True, type='joint') or []):
                remake.append((ctrl, jnt, cmds.nodeType(constraint)))
            cmds.delete(constraint)
    for ctrl, rotate in ctrls_rotates:
        children = cmds.listRelatives(ctrl, c=True, type='transform') or []
        children = [cmds.parent(child, world=True)[0] for child in children]
        root = mt.root_grp(input=ctrl, custom=True, custom_name='OrientChange')[0]
        cmds.rotate(rotate[0], rotate[1], rotate[2], root, relative=True, objectSpace=True)
        for child in children:
            cmds.parent(child, ctrl)
    return [getattr(cmds, kind)(ctrl, jnt, mo=True)[0] for ctrl, jnt, kind in remake]


def _shapes(ctrl):
    return cmds.listRelatives(ctrl, s=True, f=True) or []


def _condition(name, plug, operation, value):
    """1 when plug <operation> value. operation: 2 greater than, 4 less than."""
    node = cmds.createNode('condition', n=name)
    cmds.connectAttr(plug, node + '.firstTerm')
    cmds.setAttr(node + '.secondTerm', value)
    cmds.setAttr(node + '.operation', operation)
    cmds.setAttr(node + '.colorIfTrueR', 1)
    cmds.setAttr(node + '.colorIfFalseR', 0)
    return node + '.outColorR'


def _palm_normal(side_guide):
    """Direction the palm faces, from the fingers direction and the pinky -> index side. Used to bend
    straight fingers the right way when the IK is created."""
    def first(names):
        for finger in names:
            jnt = side_guide.replace('Palm', finger + '_00')
            if cmds.objExists(jnt):
                return jnt
        return None
    front = first(['Index', 'Middle', 'Ring'])
    back = first(['Pinky', 'Ring', 'Middle'])
    finger = first(['Middle', 'Index', 'Ring', 'Pinky'])
    if not (front and back and finger) or front == back:
        return None
    tip = (cmds.listRelatives(finger, ad=True, type='joint') or [finger])[0]
    along = _position(tip) - _position(finger)
    side = _position(front) - _position(back)
    normal = along ^ side
    return normal.normal() if normal.length() > 1e-6 else None


def _rest_pole_vector(handle, ik_joints, rig_joints):
    """The RP solver can roll or flip the chain away from the rest pose (straight fingers, mirrored sides),
    that is a pop when switching to IK. Keep the pole vector that solves back to the rest pose: the one
    the handle was made with or one of the mid joint axes."""
    def error(pole_vector):
        # setting the pole vector dirties the handle, reading the joints solves it
        cmds.setAttr(handle + '.poleVector', *pole_vector)
        return max(max(abs(a - b) for a, b in zip(_world(ik), _world(jnt))) for ik, jnt in zip(ik_joints, rig_joints))
    candidates = [tuple(cmds.getAttr(handle + '.poleVector')[0])]
    mid = _world(ik_joints[1])
    parent_inverse = om.MMatrix(cmds.getAttr(ik_joints[0] + '.parentInverseMatrix[0]'))
    for row in range(3):
        axis = om.MVector(mid[row * 4], mid[row * 4 + 1], mid[row * 4 + 2]).normal()
        for direction in [axis, -axis]:
            local = direction * parent_inverse
            candidates.append((local.x, local.y, local.z))
    best = min(candidates, key=error)
    error(best)  # the joints keep this solved pose while the IK is off


def finger_ik(side_guide, finger, joints, tip, fk_ctrls, parent_ctrl, switch_plug, ctrl_size, color, nc):
    """IK for the last 3 bones of the finger (fingers 01 02 03, thumb 00 01 02). The IK ctrl sits on the
    finger tip with the last bone orientation: the last bone follows it and the RP IK solves the other two,
    so the finger tip stays planted where the ctrl is."""
    chain = joints[-3:] + [tip]
    name = side_guide.replace('Palm' + nc['joint'], finger)
    ik_joints = []
    duplicates = cmds.duplicate(chain[0], rc=True)
    # the rest constraints of the rig joints come with the duplicate
    cmds.delete([d for d in duplicates if cmds.nodeType(d) != 'joint'])
    for src, dup in zip(chain, [d for d in duplicates if cmds.objExists(d)]):
        ik_joints.append(cmds.rename(dup, src.replace(nc['joint'], nc['ik'])))
    for jnt in ik_joints:
        cmds.setAttr(jnt + '.segmentScaleCompensate', 0)
    cmds.setAttr(ik_joints[0] + '.visibility', 0)

    # straight fingers need a preferred angle, bend it towards the palm
    normal = _palm_normal(side_guide)
    mid = ik_joints[1]
    matrix = _world(mid)
    z_axis = om.MVector(matrix[8], matrix[9], matrix[10])
    bend = -10  # default guides: +Z opens the hand
    if normal is not None:
        bend = 10 if (z_axis ^ (_position(ik_joints[2]) - _position(mid))) * normal > 0 else -10
    # preferred angles start from the rest pose (the thumb rests rotated), plus the bend on the mid joint
    for jnt in ik_joints:
        cmds.setAttr(jnt + '.preferredAngle', *cmds.getAttr(jnt + '.rotate')[0])
    cmds.setAttr(mid + '.preferredAngleZ', cmds.getAttr(mid + '.rotateZ') + bend)

    ik_ctrl = mt.curve(input=tip, type='cube', rename=False, custom_name=True,
                       name=name + '_Ik' + nc['ctrl'], size=ctrl_size * 0.5)
    mt.assign_color(ik_ctrl, color)
    cmds.parent(ik_ctrl, parent_ctrl)
    cmds.xform(ik_ctrl, os=True, m=list(_world(joints[-1]) * _world(parent_ctrl).inverse()))
    cmds.xform(ik_ctrl, ws=True, t=list(_position(tip))[:3])
    cmds.setAttr(ik_ctrl + '.scale', 1, 1, 1)
    ik_root = mt.root_grp(input=ik_ctrl)[0]
    mt.hide_attr(input=ik_ctrl, s=True, v=True)
    mt.line_attr(input=ik_ctrl, name='IK', lines=10)
    twist = mt.new_attr(input=ik_ctrl, name='Twist', min=-360, max=360, default=0)
    stretch = mt.new_attr(input=ik_ctrl, name='Stretch', min=0, max=1, default=0)
    volume = mt.new_attr(input=ik_ctrl, name='Volume', min=0, max=1, default=0)

    handle, effector = cmds.ikHandle(sj=ik_joints[0], ee=ik_joints[2], sol='ikRPsolver', n=name + nc['ik_rp'])
    cmds.rename(effector, name + nc['effector'])
    cmds.parent(handle, ik_ctrl)
    # after the parent, parenting the handle resets its pole vector
    _rest_pole_vector(handle, ik_joints[:2], chain[:2])
    cmds.setAttr(handle + '.visibility', 0)
    cmds.connectAttr(twist, handle + '.twist')

    # stretch measures from the chain start (next to the IK, not under it, no cycle) to the handle
    stretch_start = cmds.createNode('transform', n=name + '_StretchStart' + nc['null'],
                                    p=cmds.listRelatives(ik_joints[0], p=True)[0])
    cmds.xform(stretch_start, ws=True, t=list(_position(ik_joints[0]))[:3])
    stretch_end = cmds.createNode('transform', n=name + '_StretchEnd' + nc['null'], p=ik_ctrl)
    cmds.xform(stretch_end, ws=True, t=list(_position(ik_joints[2]))[:3])

    # FK ctrls of the IK bones show in FK, the IK ctrl in IK
    fk_vis = _condition(name + '_Fk_Vis' + nc['condition'], switch_plug, 4, 1)
    ik_vis = _condition(name + '_Ik_Vis' + nc['condition'], switch_plug, 2, 0)
    for ctrl in fk_ctrls[-3:]:
        for shape in _shapes(ctrl):
            cmds.connectAttr(fk_vis, shape + '.visibility', f=True)
    for shape in _shapes(ik_ctrl):
        cmds.connectAttr(ik_vis, shape + '.visibility', f=True)

    return {'ctrl': ik_ctrl, 'joints': ik_joints, 'handle': handle, 'chain': chain, 'ik_on': ik_vis,
            'parent_ctrl': parent_ctrl, 'name': name, 'stretch': stretch, 'volume': volume,
            'stretch_start': stretch_start, 'stretch_end': stretch_end}


def ik_stretch(data):
    """Stretch: past the full length of the 2 solved bones they grow to reach the handle (0 off, 1 on).
    Volume: the stretched bones get thinner (1 / sqrt of the stretch). Returns the volume scale matrix
    plug per solved bone, local to the rig joint (the bone axis keeps 1)."""
    ik_joints, chain = data['joints'], data['chain']
    name = data['name']
    rest_translates = [cmds.getAttr(jnt + '.translate')[0] for jnt in ik_joints[1:3]]
    length = sum(om.MVector(t).length() for t in rest_translates)

    # handle place in the chain start space (the hand scale and the Global scale cancel out)
    local = _mult_matrix(name + '_Stretch_MultMatrix', [data['stretch_end'] + '.worldMatrix[0]',
                                                        data['stretch_start'] + '.worldInverseMatrix[0]'])
    decompose = cmds.createNode('decomposeMatrix', n=name + '_Stretch_DecomposeMatrix')
    cmds.connectAttr(local, decompose + '.inputMatrix')
    distance = cmds.createNode('distanceBetween', n=name + '_Stretch_DistanceBetween')
    cmds.connectAttr(decompose + '.outputTranslate', distance + '.point1')
    ratio = cmds.createNode('multiplyDivide', n=name + '_Stretch_MultiplyDivide')
    cmds.setAttr(ratio + '.operation', 2)
    cmds.connectAttr(distance + '.distance', ratio + '.input1X')
    cmds.setAttr(ratio + '.input2X', length)
    clamp = cmds.createNode('clamp', n=name + '_Stretch_Clamp')
    cmds.setAttr(clamp + '.minR', 1)
    cmds.setAttr(clamp + '.maxR', 1e6)
    cmds.connectAttr(ratio + '.outputX', clamp + '.inputR')
    factor = cmds.createNode('blendColors', n=name + '_Stretch_BlendColors')
    cmds.connectAttr(data['stretch'], factor + '.blender')
    cmds.connectAttr(clamp + '.outputR', factor + '.color1R')
    cmds.setAttr(factor + '.color2R', 1)
    for jnt, rest in zip(ik_joints[1:3], rest_translates):
        grow = cmds.createNode('multiplyDivide', n=jnt + '_Stretch_MultiplyDivide')
        cmds.setAttr(grow + '.input1', *rest)
        for axis in AXES:
            cmds.connectAttr(factor + '.outputR', grow + '.input2' + axis)
        cmds.connectAttr(grow + '.output', jnt + '.translate', f=True)

    power = cmds.createNode('multiplyDivide', n=name + '_Volume_MultiplyDivide')
    cmds.setAttr(power + '.operation', 3)
    cmds.connectAttr(factor + '.outputR', power + '.input1X')
    cmds.setAttr(power + '.input2X', -0.5)
    thin = cmds.createNode('blendColors', n=name + '_Volume_BlendColors')
    cmds.connectAttr(data['volume'], thin + '.blender')
    cmds.connectAttr(power + '.outputX', thin + '.color1R')
    cmds.setAttr(thin + '.color2R', 1)
    scales = []
    for jnt, child in zip(chain[:2], chain[1:3]):
        along = cmds.getAttr(child + '.translate')[0]
        bone_axis = AXES[max(range(3), key=lambda i: abs(along[i]))]
        compose = cmds.createNode('composeMatrix', n=jnt + '_Volume_ComposeMatrix')
        for axis in AXES:
            if axis != bone_axis:
                cmds.connectAttr(thin + '.outputR', compose + '.inputScale' + axis)
        scales.append(compose + '.outputMatrix')
    return scales


def ik_follow_space(data, space):
    """The IK ctrl stays in place when the hand moves, it only follows space (Rig_Ctrl_Grp: Mover / Global).
    It stays under the finger ctrl in the outliner, its top group offset parent matrix takes the hand out."""
    top = data['ctrl']
    while cmds.listRelatives(top, p=True)[0] != data['parent_ctrl']:
        top = cmds.listRelatives(top, p=True)[0]
    # world = local * offset * parent world, the offset keeps world = rest * space world
    # (the parent worldInverseMatrix, its own parentInverseMatrix does not update through the offset)
    local = om.MMatrix(cmds.xform(top, q=True, os=True, m=True))
    rest = local.inverse() * _world(top) * _world(space).inverse()
    parent = cmds.listRelatives(top, p=True)[0]
    follow = _mult_matrix(top + '_Space_MultMatrix', [rest, space + '.worldMatrix[0]', parent + '.worldInverseMatrix[0]'])
    cmds.connectAttr(follow, top + '.offsetParentMatrix', f=True)


def ik_rest_worlds(data):
    """IK joint world plugs for the blend. The mirror and the v001 rest settle can leave the solved IK
    joints rolled against the rig joints, a constant correction measured at rest keeps the switch pop free.
    Then the solver is turned off while the finger is in full FK (cheaper)."""
    worlds = []
    volume_scales = ik_stretch(data) + [None]
    for ik_jnt, jnt, volume in zip(data['joints'][:3], data['chain'][:3], volume_scales):
        correction = _world(jnt) * _world(ik_jnt).inverse()
        items = [ik_jnt + '.worldMatrix[0]']
        if not correction.isEquivalent(om.MMatrix(), 1e-3):
            items.insert(0, correction)
        if volume:
            items.insert(0, volume)
        worlds.append(items[0] if len(items) == 1 else _mult_matrix(ik_jnt + '_Rest_MultMatrix', items))
    cmds.connectAttr(data['ik_on'], data['handle'] + '.ikBlend', f=True)
    return worlds


#-------------------------

def build_hand_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guide = cmds.listRelatives(block, c=True)[0]
    name = str(block).replace(nc['module'], '')
    print (name)

    def get_attr(attr, default, as_string=False):
        if cmds.attributeQuery(attr, n=config, exists=True):
            return cmds.getAttr('{}.{}'.format(config, attr), asString=as_string) if as_string else cmds.getAttr('{}.{}'.format(config, attr))
        return default

    new_guide = mt.duplicate_and_remove_guides(guide)
    to_build = [new_guide]

    ctrl_size = cmds.getAttr('{}.CtrlSize'.format(config))
    ctrl_type = cmds.getAttr('{}.CtrlType'.format(config), asString = True)
    attrs_ctrl = cmds.getAttr('{}.SetAttrsCtrl'.format(config), asString = True)
    mirror = cmds.getAttr('{}.Mirror'.format(config), asString = True)
    curls_axis = 'Z'

    # compatible with older blocks without these attrs
    vis_attr = get_attr('SetVisAttr', False)
    create_fingers_attrs = get_attr('CreateFingersAttrs', True)
    fingers_ik = get_attr('FingersIk', True)
    orients = get_attr('Orients', 'Default', as_string=True)
    # Thumb / Index / ... (blocks made before keep their Build<Finger> attrs)
    build_fingers = [finger for finger in FINGERS if get_attr(finger, get_attr('Build' + finger, True))]
    # blocks made before this attr keep the v001 cups
    auto_cups = get_attr('AutoCupPlacement', False)
    hand_poses = get_attr('HandPoses', True)

    # duplicate_and_remove_guides drops every 1 of the duplicated names (Index_01 -> Index_0), put them back
    for jnt in cmds.listRelatives(new_guide, ad=True, type='joint') or []:
        if '_0_' in jnt:
            cmds.rename(jnt, jnt.replace('_0_', '_01_'))

    # fingers turned off are removed before anything is built (bind joints included)
    for finger in FINGERS:
        finger_root = new_guide.replace('Palm', finger + '_00')
        if finger not in build_fingers and cmds.objExists(finger_root):
            cmds.delete(finger_root)
    inner_cup_jnt = new_guide.replace('Palm', 'InnerCup')
    if cmds.objExists(inner_cup_jnt) and not cmds.listRelatives(inner_cup_jnt, c=True, type='joint'):
        cmds.delete(inner_cup_jnt)
    outter_cup_jnt = new_guide.replace('Palm', 'OutterCup')
    if cmds.objExists(outter_cup_jnt) and not cmds.listRelatives(outter_cup_jnt, c=True, type='joint'):
        cmds.delete(outter_cup_jnt)

    if auto_cups:
        auto_cup_placement(new_guide)

    #prep work for right side ------------------------------------------------------

    #if mirror is set only to right we need to build on left for mirror behavior then putt it back to righ side
    if mirror == 'Right_Only':
        miror_grp = mt.mirror_group(new_guide, world = True)
        cmds.parent(new_guide, w = True)
        cmds.delete(miror_grp)

    elif mirror == 'True':
        right_guide = mt.duplicate_change_names(input = new_guide, hi = True, search=nc['left'], replace =nc['right'])[0]
        to_build.append(right_guide)
        print (to_build)

    #build ------------------------------------------------------

    for side_guide in to_build:
        cmds.select(side_guide)
        is_right = str(side_guide).startswith(nc['right'])

        #smart select the colors
        if str(side_guide).startswith(nc['left']):
            color = setup['left_color']
            sec_color = setup['left_secundary_color']
        elif is_right:
            color = setup['right_color']
            sec_color = setup['right_secundary_color']
        else:
            color = setup['main_color']
            sec_color = setup['main_color']

        #ctrl list for the clean up
        main_ctrl_grps = []
        hand_grp = None
        ctrl_with_attrs = None

        # what drives every rig joint, wired at the end of the side: {joint: ctrl}
        joint_sources = {}
        rest_constraints = []
        finger_chains = []

        #create hand Ctrl if there is no ctrl for the Attrs
        if create_fingers_attrs:
            if attrs_ctrl == 'new_ctrl':
                ctrl_with_attrs = mt.curve(input = side_guide, type = 'hand',
                                                rename = False,
                                                custom_name = True,
                                                name = side_guide.replace(nc['joint'],nc['ctrl']),
                                                size = ctrl_size)

                mt.assign_color(ctrl_with_attrs, color)
                cmds.move(0,0,0)
                cmds.rotate(0,0,0)
                mt.match(ctrl_with_attrs, side_guide, t=True, r=False)
                hand_grp = mt.root_grp()[0]
                mt.hide_attr(input = ctrl_with_attrs, t=True, r=True, s=True, rotate_order=True)
                rest_constraints.append(cmds.parentConstraint(side_guide, hand_grp, mo=True)[0])

            else:
                ctrl_with_attrs = attrs_ctrl
                if is_right:
                    ctrl_with_attrs = ctrl_with_attrs.replace(nc['left'], nc['right'])

        #create ctrl attrs
        if create_fingers_attrs:
            mt.line_attr(input = ctrl_with_attrs, name='Curl', lines = 10)

        #--------------------------------

        #use this locator in case parent is set to new locator
        if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
            block_parent = cmds.spaceLocator( n = '{}'.format(str(side_guide).replace(nc['joint'],'_Parent' + nc['locator'])))[0]
        else:
            block_parent = cmds.getAttr('{}.SetParent'.format(config))
            if is_right:
                block_parent = block_parent.replace(nc['left'],nc['right'])

        #main funcion -------------------------------------------
        cmds.select(side_guide)

        #get phalange 0 for the main FK chain
        fingers_zero = []
        for finger in FINGERS:
            finger_zero = side_guide.replace('Palm', finger + '_00')
            if cmds.objExists(finger_zero):
                fingers_zero.append(finger_zero)
                #create curl attrs
                if create_fingers_attrs:
                    mt.new_attr(input= ctrl_with_attrs,
                                name = finger + 'Curl',
                                min = -100 ,
                                max = 100,
                                default = 0)

        #create bind joints for later
        bind_joints = mt.duplicate_change_names(input = side_guide, hi = True, search=nc['joint'], replace =nc['joint_bind'])

        #create main fk chains
        for finger_zero in fingers_zero:
            finger = finger_zero.split('_')[-3]
            cmds.select(finger_zero)
            fk_range = [0,1,2]
            if finger == 'Thumb': # do less if is the thumb
                fk_range = [0,1]

            #add to select for the fk chain in order
            for i in fk_range:
                cmds.select(cmds.listRelatives(cmds.ls(sl=True)[-1], c=True), add=True)
            sel = cmds.ls(sl=True)
            #create fk chain, its constraints only set the rest pose (see settle_rest_pose)
            fk_ctrls = mt.fk_chain(input = '', size = ctrl_size, color = color, curve_type = ctrl_type, scale = True, twist_axis = setup['twist_axis'])
            for jnt, ctrl in zip(sel, fk_ctrls):
                joint_sources[jnt] = ctrl

            main_ctrl_grps.append(cmds.listRelatives(fk_ctrls[0], p=True)[0])
            curl_grps = []
            for ctrl in fk_ctrls[1:]:
                #add auto curl
                curl_grp = mt.root_grp(input = ctrl, custom = True, custom_name = '_Curl', autoRoot = False, replace_nc = True)[0]
                curl_grps.append(curl_grp)
                #connect to attr
                if create_fingers_attrs:
                    cmds.connectAttr('{}.{}Curl'.format(ctrl_with_attrs, finger),'{}.rotate{}'.format(curl_grp,curls_axis), f=True)

            # the tip joint is a child of the last joint, it follows without anything
            tip = cmds.listRelatives(sel[-1], c=True, type='joint')[0]
            rest_constraints.append(cmds.parentConstraint(fk_ctrls[-1], tip, mo=True)[0])
            finger_chains.append({'finger': finger, 'joints': sel, 'ctrls': fk_ctrls, 'tip': tip, 'curls': curl_grps})

        #main ctrl grp
        ctrls_grp = cmds.group(main_ctrl_grps, n = '{}{}'.format(side_guide.replace(nc['joint'],nc['ctrl']), nc['group']))
        pivot = cmds.xform(side_guide ,rp =True, q=True, ws=True)
        cmds.move(pivot[0],pivot[1],pivot[2], "{}.scalePivot".format(ctrls_grp),"{}.rotatePivot".format(ctrls_grp), absolute=True)

        if hand_grp:
            cmds.parent(hand_grp, ctrls_grp)
        joint_sources[side_guide] = ctrls_grp
        rest_constraints.append(cmds.parentConstraint(ctrls_grp, side_guide, mo=True)[0])

        #create cup inner and outter stuff
        if create_fingers_attrs:
            mt.line_attr(input = ctrl_with_attrs, name='Hand', lines = 10)

        cup_ctrls = []
        inner_cup = side_guide.replace('Palm','InnerCup')
        thumb_zero = side_guide.replace('Palm', 'Thumb_00')
        if cmds.objExists(inner_cup) and thumb_zero in fingers_zero:
            print (side_guide + ':INNER CUP')
            inner_cup_group = mt.root_grp(input = thumb_zero.replace(nc['joint'], nc['ctrl']), custom=True,custom_name='_Inner_Cup{}'.format(nc['group']) ,replace_nc=True)[0]
            inner_cup_group = cmds.rename(inner_cup_group, inner_cup_group.replace('_Thumb_00_Ctrl',''))
            pivot = cmds.xform(inner_cup ,rp =True, q=True, ws=True)
            cmds.move(pivot[0],pivot[1],pivot[2], "{}.scalePivot".format(inner_cup_group),"{}.rotatePivot".format(inner_cup_group), absolute=True)

            inner_ctrl = mt.curve(input=inner_cup,
                            type=ctrl_type,
                            rename=True,
                            custom_name=True,
                            name=inner_cup.replace(nc['joint'], nc['ctrl']),
                            size=ctrl_size)

            mt.assign_color(color=color)
            inner_root, inner_auto = mt.root_grp(inner_ctrl, autoRoot=True)
            mt.match(inner_root, inner_cup, r=True, t=True)
            joint_sources[inner_cup] = inner_ctrl
            rest_constraints.append(cmds.parentConstraint(inner_ctrl, inner_cup)[0])
            cup_ctrls.append(inner_ctrl)
            if create_fingers_attrs:
                inner_cup_attr = mt.new_attr(input= ctrl_with_attrs,
                                            name = 'Inner_Cup',
                                            min = -100 ,
                                            max = 100,
                                            default = 0)
                cmds.connectAttr(inner_cup_attr, '{}.rotate{}'.format(inner_auto, 'X' if auto_cups else 'Y'))
            cmds.parent(inner_root, ctrls_grp)
            cmds.parent(cmds.listRelatives(inner_cup_group, p=True)[0], inner_ctrl)

        outter_cup = side_guide.replace('Palm','OutterCup')
        if cmds.objExists(outter_cup):
            print (side_guide + ': OUTTER CUP')
            if create_fingers_attrs:
                outter_cup_attr = mt.new_attr(input= ctrl_with_attrs,
                                            name = 'OutterCup',
                                            min = -100 ,
                                            max = 100,
                                            default = 0)

            outter_cup_group = cmds.group(n = '{}Outter{}'.format(side_guide.replace('Palm'+nc['joint'], ''),nc['group']), em=True)
            outter_offset = mt.root_grp(replace_nc=True)[0]
            cmds.delete(cmds.parentConstraint(outter_cup,outter_offset, mo=False))

            outter_ctrl = mt.curve(input=outter_cup,
                                  type=ctrl_type,
                                  rename=True,
                                  custom_name=True,
                                  name=outter_cup.replace(nc['joint'], nc['ctrl']),
                                  size=ctrl_size)

            mt.assign_color(color=color)
            outter_root, outter_auto = mt.root_grp(outter_ctrl, autoRoot=True)
            mt.match(outter_root, outter_cup, r=True, t=True)
            joint_sources[outter_cup] = outter_ctrl
            rest_constraints.append(cmds.parentConstraint(outter_ctrl, outter_cup)[0])
            cup_ctrls.append(outter_ctrl)

            for finger in ['Pinky', 'Ring']:
                finger_ctrl = side_guide.replace('Palm'+nc['joint'], finger + '_00'+nc['ctrl'])
                if cmds.objExists(finger_ctrl):
                    cmds.parent(cmds.listRelatives(finger_ctrl, p=True), outter_cup_group)

            cmds.parent(outter_offset, outter_ctrl)
            cmds.parent(outter_root, ctrls_grp)
            if create_fingers_attrs:
                if auto_cups:
                    # the pinky side is on -Z of the fold line
                    mt.connect_md_node(in_x1 = outter_cup_attr, in_x2 = -1, out_x = '{}.rotateX'.format(outter_auto), mode = 'mult', name = 'OutterCup', force = False)
                else:
                    cmds.connectAttr(outter_cup_attr, '{}.rotateX'.format(outter_auto))

        #spread stuff
        if create_fingers_attrs:
            def finger_poses(attr_name, multipliers, axis, grp_name=None):
                grp_name = grp_name or attr_name
                attr = mt.new_attr(input= ctrl_with_attrs, name = attr_name, min = -100 , max = 100, default = 0)
                for finger, mult in multipliers:
                    finger_ctrl = side_guide.replace('Palm'+nc['joint'], finger + nc['ctrl'])
                    if cmds.objExists(finger_ctrl):
                        pose_grp = mt.root_grp(input = finger_ctrl, custom = True, custom_name = '_' + grp_name, autoRoot = False, replace_nc = True)[0]
                        mt.connect_md_node(in_x1 = attr, in_x2 = mult, out_x = '{}.rotate{}'.format(pose_grp, axis), mode = 'mult', name = grp_name, force = False)

            finger_poses('Spread', [('Pinky_01', 2), ('Ring_01', 1), ('Middle_01', 0.5), ('Index_01', -0.5)], 'Y')
            finger_poses('Relax', [('Pinky_01', 3.5), ('Ring_01', 2.5), ('Middle_01', 1.5), ('Index_01', 1)], curls_axis)

            #thumb relax
            if cmds.objExists(side_guide.replace('Palm'+nc['joint'],'Thumb_00' + nc['ctrl'])):
                finger_poses('Thumb_Relax', [('Thumb_00', 1)], 'Z', grp_name='Relax')

            #Attrs for 3 fingers relax and spread
            mt.line_attr(input=ctrl_with_attrs, name='3 Fingers', lines=10)
            finger_poses('SpreadThree', [('Pinky_01', 2), ('Ring_01', 1), ('Middle_01', 0.5)], 'Y')
            finger_poses('RelaxThree', [('Pinky_01', 3.5), ('Ring_01', 2.5), ('Middle_01', 1.5)], curls_axis)

            # one attr hand poses, added to the curl of every segment (one blendWeighted per segment)
            if hand_poses:
                mt.line_attr(input=ctrl_with_attrs, name='Poses', lines=10)
                pose_attrs = [mt.new_attr(input=ctrl_with_attrs, name=pose, min=-100, max=100, default=0) for pose in HAND_POSES]
                for chain in finger_chains:
                    for num, (curl_grp, jnt) in enumerate(zip(chain['curls'], chain['joints'][1:])):
                        plug = '{}.rotate{}'.format(curl_grp, curls_axis)
                        curl_source = cmds.listConnections(plug, s=True, d=False, p=True, skipConversionNodes=True)
                        blend = cmds.createNode('blendWeighted', n=curl_grp + '_Poses_BlendWeighted')
                        if curl_source:
                            cmds.connectAttr(curl_source[0], blend + '.input[0]')
                            cmds.setAttr(blend + '.weight[0]', 1)
                        close = _close_sign(jnt, side_guide)
                        for index, (pose, attr) in enumerate(zip(HAND_POSES, pose_attrs)):
                            weights = HAND_POSES[pose].get(chain['finger']) or HAND_POSES[pose]['thumb' if chain['finger'] == 'Thumb' else 'fingers']
                            cmds.connectAttr(attr, '{}.input[{}]'.format(blend, index + 1))
                            cmds.setAttr('{}.weight[{}]'.format(blend, index + 1), close * weights[num])
                        cmds.connectAttr(blend + '.output', plug, f=True)

        #Create Main Hand Ctrl
        main_hand_ctrl = mt.curve(input=new_guide,
                                  type='sun',
                                  rename=True,
                                  custom_name=True,
                                  name=side_guide.replace('Palm','Wrist').replace(nc['joint'],nc['ctrl']),
                                  size=ctrl_size)
        mt.assign_color(color=sec_color)
        main_hand_root = mt.root_grp()[0]
        mt.match(main_hand_root, side_guide, r=True, t=True)
        cmds.parent(ctrls_grp, main_hand_ctrl)
        palm_ctrls_grp = ctrls_grp

        clean_ctrl_grp = cmds.group(em=True, name=side_guide + nc['ctrl'] + nc['group'])
        mt.match(clean_ctrl_grp, side_guide, r=True, t=True)
        cmds.parent(main_hand_root, clean_ctrl_grp)
        ctrls_grp = clean_ctrl_grp

        if vis_attr:
            if is_right:
                vis_attr = vis_attr.replace(nc['left'], nc['right'])
            mt.line_attr(input=vis_attr, name='FKHand')
            vis_attribute = mt.new_enum(input=vis_attr, name='FKHand', enums='Hide:Show', keyable=False, default=0)
            cmds.connectAttr(vis_attribute, cmds.listRelatives(main_hand_ctrl, s=True)[0]+'.v')

        rest_constraints.append(cmds.scaleConstraint(main_hand_ctrl, side_guide)[0])

        # IK FK per finger ------------------------------------
        ik_data = {}
        if fingers_ik:
            switch_node = ctrl_with_attrs if create_fingers_attrs else main_hand_ctrl
            mt.line_attr(input=switch_node, name='IKFK', lines=10)
            for chain in finger_chains:
                if len(chain['joints']) < 3:
                    continue
                finger = chain['finger']
                # the ctrl above the IK bones: the finger 00 ctrl, or the inner cup for the thumb
                first = chain['joints'][-3]
                parent_jnt = cmds.listRelatives(first, p=True)[0]
                parent_ctrl = joint_sources.get(parent_jnt, palm_ctrls_grp)
                switch_plug = mt.new_attr(input=switch_node, name=finger + 'IkFk', min=0, max=1, default=0)
                ik_data[finger] = finger_ik(side_guide, finger, chain['joints'], chain['tip'], chain['ctrls'],
                                            parent_ctrl, switch_plug, ctrl_size, color, nc)
                ik_data[finger]['switch'] = switch_plug

        # Orients (before the mirror, same as Custom_Biped_Orients on a v001 hand) -------------
        if orients == 'SN':
            to_orient = []
            for chain in finger_chains:
                to_orient += [(ctrl, SN_FINGERS_ROTATE) for ctrl in chain['ctrls']]
            to_orient += [(ctrl, SN_FINGERS_ROTATE) for ctrl in cup_ctrls]
            to_orient += [(data['ctrl'], SN_FINGERS_ROTATE) for data in ik_data.values()]
            to_orient.append((main_hand_ctrl, SN_WRIST_ROTATE))
            rest_constraints += orient_ctrls(to_orient)

        #flip right rig to right side -------------------------
        if mirror == 'Right_Only' or (mirror == 'True' and is_right):
            clean_ctrl_grp = mt.mirror_group(ctrls_grp, world = True)
            clean_rig_grp = mt.mirror_group(side_guide, world = True)
        else:
            clean_rig_grp = side_guide
            clean_ctrl_grp = ctrls_grp
        # follow the block parent like v001 (SmartHand looks for this constraint), 2 constraints per hand
        cmds.parentConstraint(block_parent, ctrls_grp, mo = True)

        #game parents for bind joints
        game_parent = cmds.getAttr('{}.SetGameParent'.format(config))
        if is_right:
            game_parent = game_parent.replace(nc['left'],nc['right'])

        if game_parent and cmds.objExists(game_parent):
            cmds.parent(bind_joints[0], game_parent)
        else:
            bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])
            if cmds.objExists(bind_jnt_grp):
                cmds.parent(bind_joints[0], bind_jnt_grp)

        #clean ctrls
        cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])
        # the block parent scales the hand (a parent under the Global brings the Global scale with it)
        cmds.scaleConstraint(block_parent, clean_ctrl_grp, mo=True)

        #parent rig
        cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))

        # v001 constraints evaluated once with the rig already mirrored, then gone
        settle_rest_pose(side_guide, rest_constraints, [hand_grp] if hand_grp else [])

        # IK finger ctrls do not move with the hand, only with the Mover / Global
        for data in ik_data.values():
            ik_follow_space(data, setup['main_ctrl_grp'] + nc['group'])


        # Wire everything with matrix nodes (rig in rest pose) ---------------------
        # the joints follow a hidden target under their ctrl (not the palm group)
        targets = {}
        for jnt, ctrl in joint_sources.items():
            targets[jnt] = ctrl if ctrl == palm_ctrls_grp else follow_target(jnt, ctrl, nc)

        # rig joints from top to bottom, IK fingers blend the FK ctrl and the IK joint
        blended = {}
        for finger, data in ik_data.items():
            chain = [c for c in finger_chains if c['finger'] == finger][0]
            for jnt, ik_world in zip(chain['joints'][-3:], ik_rest_worlds(data)):
                blended[jnt] = (ik_world, data['switch'])

        rig_joints = [side_guide] + (cmds.listRelatives(side_guide, ad=True, type='joint') or [])[::-1]
        for jnt in rig_joints:
            if jnt not in joint_sources:
                continue
            ctrl = targets[jnt]
            if jnt in blended:
                ik_world, switch_plug = blended[jnt]
                fk_world = _offset_world_plug(jnt + '_Fk_MultMatrix', jnt, ctrl)
                blend = cmds.createNode('blendMatrix', n=jnt + '_IkFk_BlendMatrix')
                cmds.connectAttr(fk_world, blend + '.inputMatrix')
                cmds.connectAttr(ik_world, blend + '.target[0].targetMatrix')
                cmds.connectAttr(switch_plug, blend + '.target[0].weight')
                drive(jnt, [blend + '.outputMatrix'])
            else:
                drive(jnt, _offset_world(jnt, ctrl))

        # the last IK bone follows the IK ctrl rotation
        for finger, data in ik_data.items():
            drive(data['joints'][2], _offset_world(data['joints'][2], data['ctrl']), channels=('rotate',))

        # controllers scale their own joint only, the IK chains do not take the scale of the joint above them
        scale_ctrls = [ctrl for chain in finger_chains for ctrl in chain['ctrls']] + cup_ctrls
        free_controller_scale(scale_ctrls, skip=set(targets.values()))
        for finger, data in ik_data.items():
            parent_jnt = cmds.listRelatives(data['joints'][0], p=True)[0]
            inverse = _inverse_scale_matrix(data['joints'][0], parent_jnt + '.scale', cmds.getAttr(parent_jnt + '.scale')[0])
            cmds.connectAttr(inverse, data['joints'][0] + '.offsetParentMatrix', f=True)
            cmds.connectAttr(inverse, data['stretch_start'] + '.offsetParentMatrix', f=True)

        # bind joints: the root follows the palm in world space, the rest copies the rig joints channels
        # (no nodes). The mirrored side keeps the v001 flipped axes, every bind joint follows its rig joint.
        all_binds = [bind_joints[0]] + (cmds.listRelatives(bind_joints[0], ad=True, type='joint') or [])[::-1]
        for jnt in all_binds:
            cmds.setAttr('{}.segmentScaleCompensate'.format(jnt), 0)
        offsets = sorted(v001_bind_offsets(all_binds, nc).items(), key=lambda item: all_binds.index(item[0]))
        if all(offset.isEquivalent(om.MMatrix(), 1e-4) for jnt, offset in offsets):
            drive(bind_joints[0], [side_guide + '.worldMatrix[0]'], reparentable=True)
            for jnt in all_binds[1:]:
                copy_local_channels(jnt.replace(nc['joint_bind'], nc['joint']), jnt)
        else:
            for jnt, offset in offsets:
                drive(jnt, [offset, jnt.replace(nc['joint_bind'], nc['joint']) + '.worldMatrix[0]'],
                      reparentable=jnt == bind_joints[0])

    # build complete ----------------------------------------------------
    print ('Build {} Success'.format(block))


#build_hand_block()
