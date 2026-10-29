from __future__ import absolute_import, division
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
reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()

#---------------------------------------------

TAB_FOLDER = '008_Props'
PYBLOCK_NAME = 'exec_squash_v002'

# lattice padding around the geo (width / depth)
PADDING = 1.1

#---------------------------------------------

def _geo_bounding_box(geos):
    """World bounding box of the geos (xmin, ymin, zmin, xmax, ymax, zmax), None without geos."""
    geos = [geo for geo in geos if cmds.objExists(geo)]
    if not geos:
        return None
    return cmds.exactWorldBoundingBox(geos)


def create_squash_block(name = 'Squash'):

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '06_Squash_v002.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()

    # the geo selected when the block is made goes to SetGeo, the guides fit it
    selected = cmds.ls(sl=True, type='transform') or []

    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name = name, icon = 'Squash',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]

    base_guide = cmds.spaceLocator(n = name + '_Base_Guide' + nc['locator'])[0]
    cmds.parent(base_guide, block)
    top_guide = cmds.spaceLocator(n = name + '_Top_Guide' + nc['locator'])[0]
    cmds.parent(top_guide, block)
    cmds.setAttr(top_guide + '.ty', 4)
    # custom pivot: where Squash_Ctrl sits (only the controller, the deformation keeps the base / top guides)
    ctrl_guide = cmds.spaceLocator(n = name + '_Ctrl_Guide' + nc['locator'])[0]
    cmds.parent(ctrl_guide, top_guide)
    cmds.setAttr(ctrl_guide + '.t', 0, 0, 0)
    cmds.connectAttr(config + '.UseCustomPivots', ctrl_guide + '.v')

    box = _geo_bounding_box(selected)
    if box:
        cmds.setAttr(config + '.SetGeo', ','.join(selected), type='string')
        center_x, center_z = (box[0] + box[3]) / 2.0, (box[2] + box[5]) / 2.0
        cmds.xform(base_guide, ws=True, t=(center_x, box[1], center_z))
        cmds.xform(top_guide, ws=True, t=(center_x, box[4], center_z))

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_squash_block()

#-------------------------
# Matrix helpers (same as Head v003): matrix nodes instead of constraints

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
    if input_plug:
        cmds.connectAttr(input_plug, node + '.inputMatrix')
    cmds.connectAttr(target_plug, node + '.target[0].targetMatrix')
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


def _carry(name, rest_world, driver_plug):
    """Matrix that follows driver_plug keeping the current offset (like a parentConstraint with mo)."""
    offset = rest_world * _plug_matrix(driver_plug).inverse()
    return _mult_matrix(name, [offset, driver_plug])


def _mult(name, a, b):
    # multiplyDivide / plusMinusAverage, not multDoubleLinear / addDoubleLinear: Maya 2026 turns those into multDL / addDL, which Maya 2024 can not open
    node = cmds.createNode('multiplyDivide', n=name)
    for attr, value in [('input1X', a), ('input2X', b)]:
        if isinstance(value, str):
            cmds.connectAttr(value, '{}.{}'.format(node, attr), f=True)
        else:
            cmds.setAttr('{}.{}'.format(node, attr), value)
    return node + '.outputX'


def _create_ctrl(name, curve_type, size, color, rest_matrix):
    """Controller at rest_matrix with its Offset_Grp on top."""
    cmds.select(cl=True)
    ctrl = mt.curve(type=curve_type, custom_name=True, name=name, size=size)
    cmds.xform(ctrl, ws=True, m=list(rest_matrix))
    mt.assign_color(ctrl, color)
    mt.hide_attr(ctrl, v=True)
    offset_grp = mt.root_grp(input=ctrl, replace_nc=False)[0]
    return ctrl, offset_grp


def _fit_shape(ctrl, width, depth, size):
    """Scale the ctrl curves to a width x depth section (the curves are made size wide)."""
    for shape in cmds.listRelatives(ctrl, s=True, f=True) or []:
        cmds.scale(width / size, 1, depth / size, shape + '.cv[*]', r=True, ocp=False, p=cmds.xform(ctrl, q=True, ws=True, t=True))


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

# v001 config values -> attrs on Squash_Ctrl made by mt.bend_and_squash
def _param_map(name):
    return {
        'SquashMult':         'SS_{}_mult'.format(name),
        'SquashFactor':       'SS_{}_factor'.format(name),
        'SquashLowBound':     'SS_{}_lowBound'.format(name),
        'SquashHighBound':    'SS_{}_highBound'.format(name),
        'BendFrontMult':      '{}_Bend_Front_Back_mult'.format(name),
        'BendFrontCurvature': '{}_Bend_Front_Back_curvature'.format(name),
        'BendFrontLowBound':  '{}_Bend_Front_Back_lowBound'.format(name),
        'BendFrontHighBound': '{}_Bend_Front_Back_highBound'.format(name),
        'BendSideMult':       '{}_Bend_Side_mult'.format(name),
        'BendSideCurvature':  '{}_Bend_Side_curvature'.format(name),
        'BendSideLowBound':   '{}_Bend_Side_lowBound'.format(name),
        'BendSideHighBound':  '{}_Bend_Side_highBound'.format(name),
    }


def reorder_deformers(geo, ffd):
    """Evaluation order: (skinCluster) -> lattice -> bend front -> bend side -> squash (last, top of the
    inputs list). reorderDeformers(a, b) moves b right before a, so it goes from the last one down."""
    nonlinears = [node for node in cmds.listHistory(geo, pruneDagObjects=True) or [] if cmds.nodeType(node) == 'nonLinear']
    squash = next((n for n in nonlinears if 'SS_' in n), None)
    bend_side = next((n for n in nonlinears if 'Side' in n), None)
    bend_front = next((n for n in nonlinears if 'Front_Back' in n), None)
    order = [node for node in [ffd, bend_front, bend_side, squash] if node]
    try:
        for before, after in reversed(list(zip(order, order[1:]))):
            cmds.reorderDeformers(after, before, geo)
    except Exception as e:
        print("[Reorder Warning] {}: {}".format(geo, e))


def build_squash_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    name = block.replace(nc['module'],'')

    def get_attr(attr, default, as_string=False):
        if not cmds.attributeQuery(attr, n=config, exists=True):
            return default
        return cmds.getAttr('{}.{}'.format(config, attr), asString=as_string)

    joint_count = max(2, int(get_attr('Joints', 5)))
    sides = max(2, int(get_attr('LatticeSides', 2)))
    ctrl_size = get_attr('CtrlSize', 2)
    ctrl_color = get_attr('CtrlColor', 'yellow', as_string=True)

    base_guide = name + '_Base_Guide' + nc['locator']
    top_guide = name + '_Top_Guide' + nc['locator']
    base_pos = om.MVector(cmds.xform(base_guide, q=True, ws=True, t=True))
    top_pos = om.MVector(cmds.xform(top_guide, q=True, ws=True, t=True))
    rest_length = (top_pos - base_pos).length()
    # custom pivot: only where Squash_Ctrl sits, the deformers stay on the geo / guides
    ctrl_guide = name + '_Ctrl_Guide' + nc['locator']
    if not (get_attr('UseCustomPivots', False) and cmds.objExists(ctrl_guide)):
        ctrl_guide = top_guide

    #use this locator in case parent is set to new locator
    if get_attr('SetParent', 'new_locator') == 'new_locator':
        block_parent = cmds.spaceLocator(n=str(block).replace(nc['module'], '_Parent' + nc['locator']))[0]
    else:
        block_parent = get_attr('SetParent', '')

    geos_attr = get_attr('SetGeo', '', as_string=True)
    geos = [g.strip() for g in geos_attr.split(',') if g.strip()]
    dummy_geo = None
    if not geos:
        dummy_geo = cmds.polyCube(n=name + '_Squash_Dummy_Geo', h=rest_length)[0]
        cmds.xform(dummy_geo, ws=True, t=list((base_pos + top_pos) / 2.0))
        cmds.setAttr(dummy_geo + '.v', 0)
        geos = [dummy_geo]

    # Frame of the block: Y from the base to the top guide, X close to the world X
    up = (top_pos - base_pos).normal()
    side = om.MVector(1, 0, 0) if abs(up * om.MVector(1, 0, 0)) < 0.99 else om.MVector(0, 0, 1)
    front = (side ^ up).normal()
    side = (up ^ front).normal()

    def frame_matrix(position, sx=1.0, sy=1.0, sz=1.0):
        return om.MMatrix([side.x * sx, side.y * sx, side.z * sx, 0,
                           up.x * sy, up.y * sy, up.z * sy, 0,
                           front.x * sz, front.y * sz, front.z * sz, 0,
                           position.x, position.y, position.z, 1])

    # width / depth of the geo in that frame
    box = cmds.exactWorldBoundingBox(geos)
    corners = [om.MVector(x, y, z) for x in (box[0], box[3]) for y in (box[1], box[4]) for z in (box[2], box[5])]
    width = max(abs((c - base_pos) * side) for c in corners) * 2 * PADDING or 1.0
    depth = max(abs((c - base_pos) * front) for c in corners) * 2 * PADDING or 1.0

    #Bend and Squash deformers (v001), Squash_Ctrl translate drives them -----
    cmds.select(geos)
    rig_grp, ctrl_group = mt.bend_and_squash(name=name, geo=geos, parent_grp=block_parent,
                                             squash_enabled=get_attr('Squash', True),
                                             bend_enabled=get_attr('Bend', True), ctrl_guide=ctrl_guide)
    # mt.bend_and_squash names it <name>_Ctrl_Offset_Ctrl
    top_ctrl = cmds.rename('{}_Ctrl_Offset_Ctrl'.format(name), '{}{}'.format(name, nc['ctrl']))
    for config_attr, ctrl_attr in _param_map(name).items():
        if cmds.attributeQuery(config_attr, node=config, exists=True) and cmds.attributeQuery(ctrl_attr, node=top_ctrl, exists=True):
            cmds.setAttr('{}.{}'.format(top_ctrl, ctrl_attr), float(get_attr(config_attr, 0, as_string=True)))
    if get_attr('LockSecondaryAttrs', False):
        for config_attr, ctrl_attr in _param_map(name).items():
            if 'Mult' not in config_attr and cmds.attributeQuery(ctrl_attr, node=top_ctrl, exists=True):
                cmds.setAttr('{}.{}'.format(top_ctrl, ctrl_attr), lock=True, keyable=False, channelBox=False)
    # rotate and scale are for the lattice
    for attr in ['rx', 'ry', 'rz', 'sx', 'sy', 'sz']:
        cmds.setAttr('{}.{}'.format(top_ctrl, attr), lock=False, keyable=True)

    #groups ----------------------------
    clean_ctrl_grp = cmds.group(em=True, n=name + nc['ctrl'] + nc['group'], p=setup['base_groups']['control'] + nc['group'])
    clean_rig_grp = cmds.group(em=True, n=name + '_Rig' + nc['group'], p=setup['rig_groups']['misc'] + nc['group'])
    cmds.parent(rig_grp, clean_rig_grp)
    cmds.parent(ctrl_group, clean_ctrl_grp)
    # the lattice base follows the block parent
    parent_rest = _world(block_parent)
    rig_follow_grp = cmds.createNode('transform', n=name + '_Rig_Parent_Follow' + nc['group'], p=clean_rig_grp)
    cmds.connectAttr(_mult_matrix(name + '_Rig_Parent_Follow_MultMatrix',
                                  [parent_rest.inverse(), block_parent + '.worldMatrix[0]',
                                   clean_rig_grp + '.worldInverseMatrix[0]']), rig_follow_grp + '.offsetParentMatrix')
    if dummy_geo:
        cmds.parent(dummy_geo, rig_follow_grp)

    parent_world = block_parent + '.worldMatrix[0]'
    top_rest = _world(top_ctrl)
    holder_attrs = {'RotateOrder', 'MutantController'}

    #Attrs ------------------------------
    mt.line_attr(top_ctrl, 'Lattice')
    curve_attr = mt.new_attr(input=top_ctrl, name='RotationAmount', min=0, max=5, default=1)

    #FK rows ----------------------------
    # Squash_Ctrl translate is for the bend / squash deformers, the lattice takes its rotate and scale.
    # The rows are an FK chain from the base: every row after the base turns by the same Squash_Ctrl
    # rotation (times RotationAmount), so they add up to an extra curl. The base row stays with the parent.
    top_local = top_ctrl + '.matrix'
    top_rotate = cmds.createNode('multiplyDivide', n=name + '_RotationAmount_MultiplyDivide')
    cmds.connectAttr(top_ctrl + '.rotate', top_rotate + '.input1')
    for axis in 'XYZ':
        cmds.connectAttr(curve_attr, top_rotate + '.input2' + axis)
    top_rotation = cmds.createNode('composeMatrix', n=name + '_TopRotate_ComposeMatrix')
    cmds.connectAttr(top_rotate + '.output', top_rotation + '.inputRotate')
    cmds.connectAttr(top_ctrl + '.rotateOrder', top_rotation + '.inputRotateOrder')
    # the rotation is in the Squash_Ctrl parent axes, the rows turn in the block frame axes
    frame_rotation = frame_matrix(om.MVector())
    ctrl_parent_rotation = om.MTransformationMatrix(_plug_matrix(top_ctrl + '.parentMatrix[0]')).asRotateMatrix()
    row_rotation = _mult_matrix(name + '_RowRotate_MultMatrix',
                                [frame_rotation * ctrl_parent_rotation.inverse(), top_rotation + '.outputMatrix',
                                 ctrl_parent_rotation * frame_rotation.inverse()])
    # Squash_Ctrl scale goes down with a falloff (all on the top row, none on the base)
    top_scale = _pick(name + '_TopScale_PickMatrix', top_local, scale=True)

    segment = _translate_matrix(om.MVector(0, rest_length / (joint_count - 1), 0))
    base_rest = frame_matrix(base_pos)
    chain = [_mult_matrix(name + '_1_Chain_MultMatrix', [base_rest * parent_rest.inverse(), parent_world])]
    for j in range(1, joint_count):
        label = '{}_{}'.format(name, j + 1)
        chain.append(_mult_matrix(label + '_Chain_MultMatrix', [row_rotation, segment, chain[-1]]))

    ts = [float(j) / (joint_count - 1) for j in range(joint_count)]
    frames = []
    for j, t in enumerate(ts):
        label = '{}_{}'.format(name, j + 1)
        if t > 0:
            frames.append(_mult_matrix(label + '_Frame_MultMatrix',
                                       [_blend_matrix(label + '_TopScale_BlendMatrix', None, top_scale, t), chain[j]]))
        else:
            frames.append(chain[j])

    #Secondary controllers and joints ---
    sub_grp = cmds.group(em=True, n=name + '_Sub' + nc['ctrl'] + nc['group'], p=clean_ctrl_grp)
    joints_grp = cmds.group(em=True, n=name + '_Joints' + nc['group'], p=clean_rig_grp)
    sub_ctrls = []
    joints = []
    for j, frame in enumerate(frames):
        label = '{}_{}'.format(name, j + 1)
        frame_rest = _plug_matrix(frame)
        ctrl, offset_grp = _create_ctrl(label + nc['ctrl'], 'square', ctrl_size, ctrl_color, frame_rest)
        _fit_shape(ctrl, width * 1.05, depth * 1.05, ctrl_size)
        cmds.parent(offset_grp, sub_grp)
        mt.root_grp(input=ctrl, autoRoot=True)
        # the secondary rides its row, its own moves go on top (scale the row for a bulge)
        _drive_parent_space(offset_grp, _carry(label + '_Ctrl_World_MultMatrix', _world(offset_grp), frame),
                            label + '_Ctrl_Local_MultMatrix')
        sub_ctrls.append(ctrl)

        jnt = cmds.createNode('joint', n=label + nc['joint'], p=joints_grp)
        cmds.setAttr(jnt + '.segmentScaleCompensate', 0)
        cmds.xform(jnt, ws=True, m=list(_world(ctrl)))
        _drive_parent_space(jnt, _carry(label + '_Jnt_World_MultMatrix', _world(jnt), ctrl + '.worldMatrix[0]'),
                            label + '_Jnt_Local_MultMatrix')
        joints.append(jnt)

    #Lattice (first, before the bend / squash deformers) ---
    cmds.select(geos)
    ffd, lattice, lattice_base = cmds.lattice(geos, divisions=(sides, joint_count, sides), objectCentered=True,
                                              ldv=(2, 2, 2), n=name + '_Ffd')
    for geo in geos:
        reorder_deformers(geo, ffd)
    lattice = cmds.rename(lattice, name + '_Lattice')
    lattice_base = cmds.rename(lattice_base, name + '_Lattice_Base')
    # a bit taller than the guides, geo right on the lattice border would not deform (the rows still go
    # with their joints, the skin keeps the offset)
    lattice_matrix = frame_matrix((base_pos + top_pos) / 2.0, width, rest_length * 1.02, depth)
    for node in [lattice, lattice_base]:
        cmds.xform(node, ws=True, m=list(lattice_matrix))
    # the skinned lattice stays still (the joints move its points), the base follows the block parent
    cmds.parent(lattice, clean_rig_grp)
    cmds.setAttr(lattice + '.inheritsTransform', 0)
    cmds.parent(lattice_base, rig_follow_grp)
    for node in [lattice, lattice_base]:
        cmds.setAttr(node + '.v', 0)

    # the geo outside the lattice deforms too
    cmds.setAttr(ffd + '.outsideLattice', 1)

    # every lattice row goes to its joint
    skin = cmds.skinCluster(joints, lattice, tsb=True, mi=1, n=name + '_Lattice_SkinCluster')[0]
    for row, jnt in enumerate(joints):
        cmds.skinPercent(skin, '{}.pt[*][{}][*]'.format(lattice, row), transformValue=[(jnt, 1.0)])

    #Top / Bottom / Left / Right controllers ---
    # spheres riding a row, each one moves its part of the lattice (a cluster after the skin, only their own
    # moves): Top and Bottom their row with a falloff to the other end, Left and Right their whole side
    # column (every row) with a falloff to the other side
    mid = joint_count // 2
    edge_specs = [('Top', joint_count - 1, om.MVector(0, 0, 0), lambda s, t: t ** 2),
                  ('Bottom', 0, om.MVector(0, 0, 0), lambda s, t: (1 - t) ** 2),
                  ('Left', mid, om.MVector(-width / 2.0, 0, 0), lambda s, t: (1 - float(s) / (sides - 1)) ** 2),
                  ('Right', mid, om.MVector(width / 2.0, 0, 0), lambda s, t: (float(s) / (sides - 1)) ** 2),
                  # corners: their side column, their row with a falloff to the other end
                  ('TopLeft', joint_count - 1, om.MVector(-width / 2.0, 0, 0), lambda s, t: t ** 2 if s == 0 else 0),
                  ('TopRight', joint_count - 1, om.MVector(width / 2.0, 0, 0), lambda s, t: t ** 2 if s == sides - 1 else 0),
                  ('BottomLeft', 0, om.MVector(-width / 2.0, 0, 0), lambda s, t: (1 - t) ** 2 if s == 0 else 0),
                  ('BottomRight', 0, om.MVector(width / 2.0, 0, 0), lambda s, t: (1 - t) ** 2 if s == sides - 1 else 0)]
    edge_ctrls = []
    for label, row, offset, weight in edge_specs:
        ctrl_name = '{}_{}{}'.format(name, label, nc['ctrl'])
        row_rest = _plug_matrix(frames[row])
        ctrl, offset_grp = _create_ctrl(ctrl_name, 'sphere', ctrl_size * 0.35, ctrl_color,
                                        _translate_matrix(offset) * row_rest)
        cmds.parent(offset_grp, sub_grp)
        mt.root_grp(input=ctrl, autoRoot=True)
        _drive_parent_space(offset_grp, _carry(ctrl_name + '_World_MultMatrix', _world(offset_grp), frames[row]),
                            ctrl_name + '_Local_MultMatrix')
        points = [('{}.pt[{}][{}][{}]'.format(lattice, s, r, u), weight(s, ts[r]))
                  for s in range(sides) for r in range(joint_count) for u in range(sides)]
        points = [(point, value) for point, value in points if value > 1e-4]
        cluster, handle = cmds.cluster([point for point, value in points], n=ctrl_name + '_Cluster')
        # the handle stays hidden in the rig group (no clusterHandleShape under the ctrl): it sits under a
        # null that follows the ctrl parent and copies the ctrl channels, the bind is that null so only the
        # ctrl own moves deform (it rides the rows), around the ctrl
        handle = cmds.rename(handle, ctrl_name + '_ClusterHandle')
        handle_space = cmds.createNode('transform', n=ctrl_name + '_ClusterSpace' + nc['null'], p=clean_rig_grp)
        cmds.setAttr(handle_space + '.inheritsTransform', 0)
        cmds.connectAttr(cmds.listRelatives(ctrl, p=True)[0] + '.worldMatrix[0]', handle_space + '.offsetParentMatrix')
        cmds.parent(handle, handle_space)
        for attr in ['rotatePivot', 'scalePivot']:
            cmds.setAttr('{}.{}'.format(handle, attr), 0, 0, 0)
        cmds.setAttr(handle + 'Shape.origin', 0, 0, 0)
        for attr in ['translate', 'rotate', 'scale', 'rotateOrder']:
            cmds.connectAttr('{}.{}'.format(ctrl, attr), '{}.{}'.format(handle, attr), f=True)
        cmds.connectAttr(handle_space + '.worldInverseMatrix[0]', cluster + '.bindPreMatrix', f=True)
        cmds.setAttr(handle + '.v', 0)
        for point, value in points:
            cmds.percent(cluster, point, v=value)
        edge_ctrls.append(ctrl)

    #Vis and attrs on every controller --
    mt.line_attr(top_ctrl, 'Vis')
    sub_vis = mt.new_enum(input=top_ctrl, name='SubCtrls', enums='Hide:Show', keyable=False, default=0)
    for ctrl in sub_ctrls:
        for shape in cmds.listRelatives(ctrl, s=True) or []:
            cmds.connectAttr(sub_vis, shape + '.v')
    edge_vis = mt.new_enum(input=top_ctrl, name='EdgeCtrls', enums='Hide:Show', keyable=False, default=0)
    corner_vis = mt.new_enum(input=top_ctrl, name='CornerCtrls', enums='Hide:Show', keyable=False, default=0)
    for ctrl, (label, row, offset, weight) in zip(edge_ctrls, edge_specs):
        vis = corner_vis if label.startswith(('TopLeft', 'TopRight', 'BottomLeft', 'BottomRight')) else edge_vis
        # the clusters add a clusterHandleShape under them
        for shape in cmds.listRelatives(ctrl, s=True, f=True, type='nurbsCurve') or []:
            cmds.connectAttr(vis, shape + '.v')
    squash_attrs = [attr for attr in cmds.listAttr(top_ctrl, ud=True) or [] if attr not in holder_attrs]
    attrs_on_ctrls(top_ctrl, squash_attrs, name + '_Attrs' + nc['locator'], sub_ctrls + edge_ctrls)

    cmds.select(cl=True)
    print ('Build {} Success'.format(block))


#build_squash_block()
