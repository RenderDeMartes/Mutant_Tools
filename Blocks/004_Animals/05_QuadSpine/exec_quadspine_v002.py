from __future__ import absolute_import
from __future__ import division
from maya import cmds
import maya.api.OpenMaya as om
import json
import math
import string
import sys
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

TAB_FOLDER = '004_Animals'
PYBLOCK_NAME = 'exec_quadspine'

#---------------------------------------------
# v002: same guides, joints (Spine_A_Jnt...), controllers (Spine_N_Ik / Frw / Bkw_Ctrl), attrs and bind joints as
# v001, so the neck, tail, pelvis, clavicles, spaces and skin keep working.
# - The hip and chest IK controllers drive the first / last joint orientation fully (v001: 12 of 30 degrees).
# - The joints ride the curve by arc length, the chain always ends on the chest controller, every segment
#   stretches the same (v001 left the first and last segments out). Stretch 0 keeps the length, Squash keeps
#   the volume.
# - No ik spline, clusters or constraints on the joints: the curve CVs come from the controllers matrices and
#   every joint is a matrix network (faster playback, no evaluation cycles).
# - Bind joints in a chain (Spine_A_Bnd > Spine_B_Bnd ...) under SetGameParent (or the bind joints group),
#   so the game skeleton gets the spine hierarchy without post build code.
# - Tweakers (one controller per joint), controllers scale the bind joints around them, DefaultCtrls,
#   JointCount (resample the spine to 5 / 7 / 9 / 11 joints, Guides = one joint per guide).

ALPHABET = string.ascii_uppercase


def _limb():
    """Limb v002 node helpers (matrix swap, switch data node, controllers scale)."""
    limb_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                               '002_Biped', '004_Limb')
    if limb_folder not in sys.path:
        sys.path.append(limb_folder)
    import exec_limb_v002
    return exec_limb_v002


def create_quadspine_block(name = 'QuadSpine'):

    # Read name conventions as nc[''] and setup as seup['']
    MODULE_FILE = os.path.join(os.path.dirname(__file__), '05_QuadSpine.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()

    name = mt.ask_name(text=module['Name'])
    if cmds.objExists('{}{}'.format(name, nc['module'])):
        cmds.warning('Name already exists.')
        return ''
    amount = 7

    block = mt.create_block(name=name, icon='QuadSpine', attrs=module['attrs'], build_command=module['build_command'],
                            import_command=module['import'])
    config = block[1]
    block = block[0]

    past_guide = None
    x_pos = 0
    for num in range(int(amount)):
        cmds.select(cl=True)
        guide = mt.create_joint_guide(name=name+'_'+ALPHABET[num])
        cmds.move(0,0,x_pos)
        if not past_guide:
            cmds.parent(guide,block)
        else:
            cmds.parent(guide,past_guide)
        past_guide=guide
        x_pos = x_pos+2

    cmds.select(block)
    print('{} Created Successfully'.format(name))

#-------------------------


def _world(node):
    return om.MMatrix(cmds.getAttr(node + '.worldMatrix[0]'))


def _position(node):
    return om.MVector(cmds.xform(node, q=True, ws=True, t=True))


def _translation_matrix(vector):
    return om.MTransformationMatrix().setTranslation(om.MVector(vector), om.MSpace.kWorld).asMatrix()


def _rotation_only(matrix):
    return om.MTransformationMatrix().setRotation(om.MTransformationMatrix(matrix).rotation(asQuaternion=True)).asMatrix()


def _attr(config, attr, default, as_string=False):
    if cmds.attributeQuery(attr, n=config, exists=True):
        return cmds.getAttr('{}.{}'.format(config, attr), asString=as_string)
    return default


def _drive(node, world_plug, name):
    """Joint / transform channels from a world matrix (the node does not inherit its parent)."""
    cmds.setAttr(node + '.inheritsTransform', 0)
    if cmds.nodeType(node) == 'joint':
        cmds.setAttr(node + '.jointOrient', 0, 0, 0)
    decompose = cmds.createNode('decomposeMatrix', n=name + '_DecomposeMatrix')
    cmds.connectAttr(world_plug, decompose + '.inputMatrix')
    for attr in ['Translate', 'Rotate', 'Scale']:
        cmds.connectAttr('{}.output{}'.format(decompose, attr), '{}.{}'.format(node, attr.lower()), f=True)


def _drive_local(node, world_plug, parent_world_inverse, name):
    """Joint channels from a world matrix, inside its parent (bind joints keep their hierarchy)."""
    if cmds.nodeType(node) == 'joint':
        cmds.setAttr(node + '.jointOrient', 0, 0, 0)
        cmds.setAttr(node + '.segmentScaleCompensate', 0)
    local = cmds.createNode('multMatrix', n=name + '_Local_MultMatrix')
    cmds.connectAttr(world_plug, local + '.matrixIn[0]')
    cmds.connectAttr(parent_world_inverse, local + '.matrixIn[1]')
    decompose = cmds.createNode('decomposeMatrix', n=name + '_Local_DecomposeMatrix')
    cmds.connectAttr(local + '.matrixSum', decompose + '.inputMatrix')
    for attr in ['Translate', 'Rotate', 'Scale']:
        cmds.connectAttr('{}.output{}'.format(decompose, attr), '{}.{}'.format(node, attr.lower()), f=True)


def _resample(points, count):
    """count points along the polyline through points, evenly spaced by length."""
    lengths = [0.0]
    for a, b in zip(points[:-1], points[1:]):
        lengths.append(lengths[-1] + (b - a).length())
    total = lengths[-1]
    result = []
    for i in range(count):
        target = total * i / (count - 1)
        seg = max(k for k in range(len(points) - 1) if lengths[k] <= target + 1e-9) if i < count - 1 else len(points) - 2
        span = lengths[seg + 1] - lengths[seg]
        t = (target - lengths[seg]) / span if span > 1e-9 else 0.0
        result.append(points[seg] + (points[seg + 1] - points[seg]) * t)
    return result


def _ctrl_scale_matrix(limb, name, influences, rest_matrix):
    """Weighted product of controllers scale (axes matched to the joint at rest) as a scale matrix plug."""
    product = None
    for num, (ctrl, weight) in enumerate(influences):
        axis_map = limb._axis_map(_world(ctrl), rest_matrix)
        blend = cmds.createNode('blendColors', n='{}_Scale{:02d}_BlendColors'.format(name, num))
        for channel, ctrl_axis in zip('RGB', axis_map):
            cmds.connectAttr('{}.scale{}'.format(ctrl, 'XYZ'[ctrl_axis]), '{}.color1{}'.format(blend, channel))
            cmds.setAttr('{}.color2{}'.format(blend, channel), 1)
        cmds.setAttr(blend + '.blender', weight)
        if product is None:
            product = blend + '.output'
        else:
            mult = cmds.createNode('multiplyDivide', n='{}_Scale{:02d}_MultiplyDivide'.format(name, num))
            cmds.connectAttr(product, mult + '.input1')
            cmds.connectAttr(blend + '.output', mult + '.input2')
            product = mult + '.output'
    if product is None:
        return None
    compose = cmds.createNode('composeMatrix', n=name + '_CtrlsScale_ComposeMatrix')
    cmds.connectAttr(product, compose + '.inputScale')
    return compose + '.outputMatrix'


def build_quadspine_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()
    limb = _limb()
    limb._BUILD_CACHE.clear()
    old_constraints = set(cmds.ls(type='constraint'))

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guide = cmds.listRelatives(block, c=True)[0]
    name = block.replace(nc['module'],'')

    # orient the joints
    new_guide = mt.duplicate_and_remove_guides(guide)
    mt.orient_joint(input = new_guide)

    #use this locator in case parent is set to new locator
    if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
        block_parent = cmds.spaceLocator(n='{}'.format(str(block).replace(nc['module'], '_Parent' + nc['locator'])))[0]
    else:
        block_parent = cmds.getAttr('{}.SetParent'.format(config))

    ctrl_size = cmds.getAttr('{}.CtrlSize'.format(config))
    game_parent = _attr(config, 'SetGameParent', '') or ''
    do_tweakers = _attr(config, 'Tweakers', True)
    default_ctrls = _attr(config, 'DefaultCtrls', 'Both', as_string=True)
    joint_count = _attr(config, 'JointCount', 'Guides', as_string=True)

    forward_color = 'green'
    backward_color = 'purple'
    ik_color = 'lightBlue'

    # guide chain (controllers are placed on it, like v001)
    guide_joints = []
    num = 0
    while cmds.objExists(name + '_' + ALPHABET[num] + nc['joint']):
        guide_joints.append(name + '_' + ALPHABET[num] + nc['joint'])
        num += 1
    if len(guide_joints) < 3 or len(guide_joints) % 2 == 0:
        cmds.error('QuadSpine: needs an odd number of guides (3, 5, 7...), found {}'.format(len(guide_joints)))
    for jnt in guide_joints:
        cmds.makeIdentity(jnt, a=True, t=True, r=True, s=True)
    cmds.setAttr("{}.jointOrient".format(guide_joints[-1]), 0, 0, 0)
    guide_positions = [_position(j) for j in guide_joints]

    # spine joints: one per guide or resampled
    if joint_count != 'Guides' and int(joint_count) != len(guide_joints):
        place_grp = cmds.group(em=True, n=name + '_GuidePlacement' + nc['group'])
        cmds.parent(guide_joints[0], place_grp)
        for num, jnt in enumerate(guide_joints):
            guide_joints[num] = cmds.rename(jnt, '{}_Guide{}{}'.format(name, ALPHABET[num], nc['joint']))
        spine_joints = []
        cmds.select(cl=True)
        for num, position in enumerate(_resample(guide_positions, int(joint_count))):
            spine_joints.append(cmds.joint(n=name + '_' + ALPHABET[num] + nc['joint'], p=list(position)))
        mt.orient_joint(input=spine_joints[0])
        cmds.setAttr("{}.jointOrient".format(spine_joints[-1]), 0, 0, 0)
    else:
        place_grp = None
        spine_joints = guide_joints
    print('Spine Joints:', spine_joints)

    ik_nums = list(range(0, len(guide_joints), 2))
    fk_nums = list(range(1, len(guide_joints), 2))
    cv_positions = [guide_positions[n] for n in ik_nums]

    #Create Ctrls ---------------------------------------------------------------
    ik_ctrls = []
    ik_roots = []
    for num, guide_num in enumerate(ik_nums):
        end = num == 0 or num + 1 == len(ik_nums)
        cmds.select(cl=True)
        ctrl = mt.curve(input='', type='cube' if end else 'sphere', rename=True, custom_name=True,
                        name='{}_{}_Ik{}'.format(name, num, nc['ctrl']), size=ctrl_size if end else ctrl_size * 0.75)
        mt.assign_color(color=ik_color)
        root_grp = mt.root_grp()[0]
        if num == 0:
            mt.match(root_grp, guide_joints[1], r=True, t=True)
        elif num + 1 == len(ik_nums):
            mt.match(root_grp, guide_joints[-2], r=True, t=True)
        else:
            cmds.xform(root_grp, ws=True, t=list(cv_positions[num]), ro=(0, 0, 0))
        ik_ctrls.append(ctrl)
        ik_roots.append(root_grp)
        if end:
            mt.hide_attr(ctrl, s=True)
        else:
            mt.hide_attr(ctrl, s=True, r=True, rotate_order=True)

    fk_joints = [guide_joints[n] for n in fk_nums]
    forward_ctrls = []
    for num, joint in enumerate(fk_joints):
        ctrl = mt.curve(input=joint, type='cylinder', rename=True, custom_name=True,
                        name=name+'_'+str(num)+'_Frw'+nc['ctrl'], size=ctrl_size*0.90)
        mt.rotate_shape(input=ctrl, z=90)
        mt.scale_shape(input=ctrl, x=0.5)
        mt.assign_color(color=forward_color)
        root_grp = mt.root_grp()[0]
        mt.hide_attr(ctrl, s=True)
        if forward_ctrls:
            cmds.parent(root_grp, forward_ctrls[-1])
        forward_ctrls.append(ctrl)
        mt.match(root_grp, joint, r=True, t=True)

    backwards_ctrls = []
    for num, joint in enumerate(reversed(fk_joints)):
        ctrl = mt.curve(input=joint, type='cylinder', rename=True, custom_name=True,
                        name=name+'_'+str(num)+'_Bkw'+nc['ctrl'], size=ctrl_size*0.80)
        mt.rotate_shape(input=ctrl, z=90)
        mt.scale_shape(input=ctrl, x=0.5)
        mt.assign_color(color=backward_color)
        root_grp = mt.root_grp()[0]
        mt.hide_attr(ctrl, s=True)
        if backwards_ctrls:
            cmds.parent(root_grp, backwards_ctrls[-1])
        backwards_ctrls.append(ctrl)
        mt.match(root_grp, joint, r=True, t=True)

    cmds.parent(ik_roots[0], backwards_ctrls[-1])
    cmds.parent(ik_roots[-1], forward_ctrls[-1])

    # mid ik controllers between the forward and backward fk controllers (animated weights, kept constraints)
    reversed_backwards_ctrls = list(reversed(backwards_ctrls))
    mid_constraints = []
    for num, root in enumerate(ik_roots[1:-1]):
        pc = cmds.parentConstraint(forward_ctrls[num], reversed_backwards_ctrls[num + 1], root, mo=True)[0]
        cmds.setAttr('{}.interpType'.format(pc), 2)
        mid_constraints.append((pc, forward_ctrls[num], reversed_backwards_ctrls[num + 1]))

    for ctrl in forward_ctrls + backwards_ctrls + ik_ctrls:
        cmds.select(ctrl)
        share_loc = mt.shape_with_attr(input='', obj_name='{}_Switch'.format(name), attr_name='').split('.')[0]

    mt.line_attr(input=share_loc, name='Visibility')
    show_main_iks_attr = mt.new_enum(input=share_loc, name='IkMain')
    show_mid_iks_attr = mt.new_enum(input=share_loc, name='IkMid')
    show_backwards_attr = mt.new_enum(input=share_loc, name='FkBackwards')
    show_fordward_attr = mt.new_enum(input=share_loc, name='FkForwards')
    show_ik = default_ctrls in ('Both', 'IK')
    show_fk = default_ctrls in ('Both', 'FK')
    cmds.setAttr(show_main_iks_attr, show_ik)
    cmds.setAttr(show_mid_iks_attr, show_ik)
    cmds.setAttr(show_backwards_attr, show_fk)
    cmds.setAttr(show_fordward_attr, show_fk)
    if do_tweakers:
        show_tweak_attr = mt.new_enum(input=share_loc, name='tweakCtrls', enums='Hide:Show', keyable=False)
        cmds.setAttr(show_tweak_attr, 0)

    mt.line_attr(input=share_loc, name='Motion')
    forward_attr = mt.new_attr(input=share_loc, name='FkForward', min=0, max=2, default=1)
    backward_attr = mt.new_attr(input=share_loc, name='FkBackward', min=0, max=2, default=1)

    for ctrl in ik_ctrls[1:-1]:
        cmds.connectAttr(show_mid_iks_attr, '{}.v'.format(cmds.listRelatives(ctrl, s=True)[0]))
    for ctrl in [ik_ctrls[0], ik_ctrls[-1]]:
        cmds.connectAttr(show_main_iks_attr, '{}.v'.format(cmds.listRelatives(ctrl, s=True)[0]))
    for ctrl in forward_ctrls:
        cmds.connectAttr(show_fordward_attr, '{}.v'.format(cmds.listRelatives(ctrl, s=True)[0]))
    for ctrl in backwards_ctrls:
        cmds.connectAttr(show_backwards_attr, '{}.v'.format(cmds.listRelatives(ctrl, s=True)[0]))
    for pc, forward, backward in mid_constraints:
        cmds.connectAttr(forward_attr, '{}.{}W0'.format(pc, forward))
        cmds.connectAttr(backward_attr, '{}.{}W1'.format(pc, backward))

    mt.line_attr(input=share_loc, name='SnS')
    stretch_attr = mt.new_attr(input=share_loc, name='Stretch', min=0, max=1, default=1)
    squash_attr = mt.new_attr(input=share_loc, name='Squash', min=0, max=1, default=1)

    # clean a bit
    clean_ctrl_grp = cmds.group(em=True, name=name + nc['ctrl'] + nc['group'])
    clean_rig_grp = cmds.group(em=True, name=name + '_Rig' + nc['group'])
    cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
    cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])
    cmds.parent(ik_roots[1:-1], cmds.listRelatives(forward_ctrls[0], p=True)[0],
                cmds.listRelatives(backwards_ctrls[0], p=True)[0], clean_ctrl_grp)
    cmds.parentConstraint(block_parent, clean_ctrl_grp, mo=True)
    cmds.scaleConstraint(block_parent, clean_ctrl_grp, mo=True)

    # spine scale (the block parent scale normalizes the stretch)
    scale_node = cmds.createNode('decomposeMatrix', n=name + '_SpineScale_DecomposeMatrix')
    cmds.connectAttr(block_parent + '.worldMatrix[0]', scale_node + '.inputMatrix')
    spine_scale = scale_node + '.outputScaleX'
    rest_scale = cmds.getAttr(spine_scale)

    # controllers scale: the ik / fk controllers do not pass their scale to the controllers under them
    scaled_ctrls = ik_ctrls + forward_ctrls + backwards_ctrls
    limb.free_controller_scale(scaled_ctrls)

    # curve from the ik controllers (no clusters): CV = rest offset * controller world without its scale ------
    degree = min(3, len(cv_positions) - 1)
    spine_cv = cmds.curve(d=degree, p=[list(p) for p in cv_positions], n=name + '_Main' + nc['curve'])
    spine_cv_shape = cmds.listRelatives(spine_cv, s=True)[0]
    cmds.setAttr(spine_cv + '.inheritsTransform', 0)
    cmds.setAttr(spine_cv + '.visibility', 0)
    cmds.parent(spine_cv, clean_rig_grp)
    # HipBend / ChestBend: the CV next to the hip / chest also turns with that controller rotation, so rotating
    # them bends the spine instead of only the end joint
    mt.line_attr(input=share_loc, name='Bend')
    bend_attrs = {1: mt.new_attr(input=share_loc, name='HipBend', min=0, max=1, default=1),
                  len(ik_ctrls) - 2: mt.new_attr(input=share_loc, name='ChestBend', min=0, max=1, default=1)}
    for num, (ctrl, position) in enumerate(zip(ik_ctrls, cv_positions)):
        offset = _translation_matrix(position) * _world(ctrl).inverse()
        world = limb._mult_matrix('{}_CV{}_MultMatrix'.format(name, num), [offset, limb._unscaled_world(ctrl)])
        decompose = cmds.createNode('decomposeMatrix', n='{}_CV{}_DecomposeMatrix'.format(name, num))
        cmds.connectAttr(world, decompose + '.inputMatrix')
        point = decompose + '.outputTranslate'
        for end_num, bend_attr in bend_attrs.items():
            if num != end_num or num in (0, len(ik_ctrls) - 1):
                continue
            end_ctrl = ik_ctrls[0] if bend_attr.endswith('HipBend') else ik_ctrls[-1]
            label = '{}_CV{}_{}'.format(name, num, bend_attr.split('.')[-1])
            # rest vector end controller -> this CV, turned by the end controller rotation since rest
            rest_vector = om.MVector(position) - _position(end_ctrl)
            turn = limb._mult_matrix(label + '_Turn_MultMatrix', [_rotation_only(_world(end_ctrl)).inverse(),
                                                                  limb._pick_matrix(label + '_PickMatrix', limb._unscaled_world(end_ctrl), translate=False)])
            turned = cmds.createNode('vectorProduct', n=label + '_VectorProduct')
            cmds.setAttr(turned + '.operation', 3)
            cmds.setAttr(turned + '.input1', *rest_vector)
            cmds.connectAttr(turn, turned + '.matrix')
            delta = cmds.createNode('plusMinusAverage', n=label + '_Delta_PlusMinusAverage')
            cmds.setAttr(delta + '.operation', 2)
            cmds.connectAttr(turned + '.output', delta + '.input3D[0]')
            cmds.setAttr(delta + '.input3D[1]', *rest_vector)
            point = limb._vector_op(label + '_PlusMinusAverage', point,
                                    limb._vector_scale(label + '_Weight_MultiplyDivide', delta + '.output3D', bend_attr), 1)
        cmds.connectAttr(point, '{}.controlPoints[{}]'.format(spine_cv_shape, num), f=True)

    curve_info = cmds.createNode('curveInfo', n=name + '_CurveInfoSpine')
    cmds.connectAttr(spine_cv_shape + '.worldSpace[0]', curve_info + '.inputCurve')
    rest_length = cmds.getAttr(curve_info + '.arcLength') / rest_scale
    # ratio: curve length / rest length, without the spine scale
    ratio = limb._divide_scalar(name + '_Ratio_MultiplyDivide', limb._divide_scalar(
        name + '_Normalize_MultiplyDivide', curve_info + '.arcLength', spine_scale), rest_length)
    # Stretch 1: the joints spread on the whole curve, 0: they keep the rest length (fraction / ratio)
    effective = limb._add(name + '_Stretch_AddDoubleLinear', 1, limb._mult(
        name + '_StretchOn_MultDoubleLinear', limb._add(name + '_RatioOver_AddDoubleLinear', ratio, -1), stretch_attr))
    # squash: 1 / sqrt(stretch), blended by Squash
    volume = cmds.createNode('multiplyDivide', n=name + '_Volume_MultiplyDivide')
    cmds.setAttr(volume + '.operation', 3)
    cmds.connectAttr(effective, volume + '.input1X')
    cmds.setAttr(volume + '.input2X', -0.5)
    squash = limb._add(name + '_Squash_AddDoubleLinear', 1, limb._mult(
        name + '_SquashOn_MultDoubleLinear', limb._add(name + '_VolumeOver_AddDoubleLinear', volume + '.outputX', -1), squash_attr))

    # joints -------------------------------------------------------------------
    rest = [_world(j) for j in spine_joints]
    lengths = [0.0]
    for a, b in zip(spine_joints[:-1], spine_joints[1:]):
        lengths.append(lengths[-1] + (_position(b) - _position(a)).length())
    fractions = [l / lengths[-1] for l in lengths]
    hip_ctrl, chest_ctrl = ik_ctrls[0], ik_ctrls[-1]
    hip_world, chest_world = limb._unscaled_world(hip_ctrl), limb._unscaled_world(chest_ctrl)

    points = []
    for num, fraction in enumerate(fractions):
        label = '{}_{}'.format(name, ALPHABET[num])
        keep = limb._clamp(label + '_Keep_Clamp', limb._divide_scalar(label + '_Keep_MultiplyDivide', fraction, ratio), 0, 1)
        u = cmds.createNode('blendTwoAttr', n=label + '_U_BlendTwoAttr')
        cmds.connectAttr(stretch_attr, u + '.attributesBlender')
        cmds.connectAttr(keep, u + '.input[0]')
        cmds.setAttr(u + '.input[1]', fraction)
        motion_path = cmds.createNode('motionPath', n=label + '_MotionPath')
        cmds.connectAttr(spine_cv_shape + '.worldSpace[0]', motion_path + '.geometryPath')
        cmds.setAttr(motion_path + '.fractionMode', 1)
        cmds.connectAttr(u + '.output', motion_path + '.uValue')
        points.append(motion_path + '.allCoordinates')

    joint_worlds = []
    for num, jnt in enumerate(spine_joints):
        label = '{}_{}'.format(name, ALPHABET[num])
        position = cmds.createNode('composeMatrix', n=label + '_Position_ComposeMatrix')
        cmds.connectAttr(points[num], position + '.inputTranslate')
        if num in (0, len(spine_joints) - 1):
            # hip / chest joints: the controller orientation, fully
            ctrl_world = hip_world if num == 0 else chest_world
            ctrl_rest = _world(hip_ctrl if num == 0 else chest_ctrl)
            rotation = limb._pick_matrix(label + '_Rotation_PickMatrix', ctrl_world, translate=False)
            offset = _rotation_only(rest[num]) * _rotation_only(ctrl_rest).inverse()
        else:
            # mid joints: aim at the next joint, the up axis blended from the hip to the chest controller
            frame = cmds.createNode('blendMatrix', n=label + '_Up_BlendMatrix')
            cmds.connectAttr(limb._mult_matrix(label + '_HipUp_MultMatrix', [_rotation_only(rest[num]) * _rotation_only(_world(hip_ctrl)).inverse(),
                                                                              limb._pick_matrix(label + '_HipUp_PickMatrix', hip_world, translate=False)]),
                             frame + '.inputMatrix')
            cmds.connectAttr(limb._mult_matrix(label + '_ChestUp_MultMatrix', [_rotation_only(rest[num]) * _rotation_only(_world(chest_ctrl)).inverse(),
                                                                                limb._pick_matrix(label + '_ChestUp_PickMatrix', chest_world, translate=False)]),
                             frame + '.target[0].targetMatrix')
            cmds.setAttr(frame + '.target[0].weight', fractions[num])
            aim = cmds.createNode('aimMatrix', n=label + '_AimMatrix')
            cmds.connectAttr(position + '.outputMatrix', aim + '.inputMatrix')
            cmds.setAttr(aim + '.primaryInputAxis', 1, 0, 0)
            cmds.setAttr(aim + '.primaryMode', 2)
            cmds.connectAttr(limb._vector_op(label + '_Aim_PlusMinusAverage', points[num + 1], points[num], 2),
                             aim + '.primaryTargetVector')
            cmds.setAttr(aim + '.secondaryInputAxis', 0, 1, 0)
            cmds.setAttr(aim + '.secondaryMode', 2)
            cmds.setAttr(aim + '.secondaryTargetVector', 0, 1, 0)
            cmds.connectAttr(frame + '.outputMatrix', aim + '.secondaryTargetMatrix')
            rotation = limb._pick_matrix(label + '_Rotation_PickMatrix', aim + '.outputMatrix', translate=False)
            offset = _rotation_only(rest[num]) * _rotation_only(limb._plug_matrix(rotation)).inverse()
        # scale: the spine scale, squash on the mid joints
        scale = cmds.createNode('composeMatrix', n=label + '_Scale_ComposeMatrix')
        cmds.connectAttr(spine_scale, scale + '.inputScaleX')
        if 0 < num < len(spine_joints) - 1:
            side = limb._mult(label + '_Squash_MultDoubleLinear', spine_scale, squash)
        else:
            side = spine_scale
        cmds.connectAttr(side, scale + '.inputScaleY')
        cmds.connectAttr(side, scale + '.inputScaleZ')
        world = limb._mult_matrix(label + '_World_MultMatrix', [scale + '.outputMatrix', offset, rotation, position + '.outputMatrix'])
        _drive(jnt, world, label)
        joint_worlds.append(world)

    spine_root_main_chain = mt.root_grp(input=spine_joints[0])[0]
    cmds.parent(spine_root_main_chain, clean_rig_grp)
    if place_grp:
        cmds.delete(place_grp)

    # tweakers: one controller per joint, the bind joint follows it ---------------------------------------
    tweak_ctrls = []
    if do_tweakers:
        tweakers_grp = cmds.group(em=True, n=name + '_Tweakers' + nc['group'], p=clean_ctrl_grp)
        cmds.setAttr(tweakers_grp + '.inheritsTransform', 0)
        cmds.connectAttr(show_tweak_attr, tweakers_grp + '.v')
        for num, jnt in enumerate(spine_joints):
            cmds.select(cl=True)
            ctrl = mt.curve(input='', type='circleX', rename=True, custom_name=True,
                            name='{}_{}_Tweak{}'.format(name, ALPHABET[num], nc['ctrl']), size=ctrl_size * 0.6)
            mt.assign_color(color='yellow')
            tweak_root = mt.root_grp(input=ctrl)[0]
            cmds.parent(tweak_root, tweakers_grp)
            for attr in ['translate', 'rotate']:
                cmds.setAttr(tweak_root + '.' + attr, 0, 0, 0)
            cmds.setAttr(tweak_root + '.scale', 1, 1, 1)
            # the joint world without its squash (the tweaker shape keeps its size)
            no_scale = limb._pick_matrix('{}_{}_Tweak_PickMatrix'.format(name, ALPHABET[num]), joint_worlds[num], translate=True, rotate=True)
            cmds.connectAttr(no_scale, tweak_root + '.offsetParentMatrix')
            cmds.select(ctrl)
            mt.shape_with_attr(input='', obj_name='{}_Switch'.format(name), attr_name='')
            tweak_ctrls.append(ctrl)

    # bind joints in a chain -------------------------------------------------------------------------------
    bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])
    bind_parent = game_parent if game_parent and cmds.objExists(game_parent) else (bind_jnt_grp if cmds.objExists(bind_jnt_grp) else None)
    if game_parent and not cmds.objExists(game_parent):
        cmds.warning('QuadSpine: SetGameParent {} not found, bind joints go to {}'.format(game_parent, bind_parent))

    # controllers scale: ik controllers fade to their neighbours, fk controllers on their joint, tweakers on
    # their own joint
    ik_fractions = []
    for ctrl in ik_ctrls:
        ik_fractions.append(min(range(len(spine_joints)), key=lambda n: (_position(spine_joints[n]) - _position(ctrl)).length()))
    ik_fractions = [fractions[n] for n in ik_fractions]
    fk_items = []
    for ctrl_list in (forward_ctrls, backwards_ctrls):
        for ctrl in ctrl_list:
            closest = min(range(len(spine_joints)), key=lambda n: (_position(spine_joints[n]) - _position(ctrl)).length())
            fk_items.append((ctrl, closest))

    bind_joints = []
    previous_world = None
    for num, jnt in enumerate(spine_joints):
        label = '{}_{}'.format(name, ALPHABET[num])
        cmds.select(cl=True)
        bind_joint = cmds.joint(n=jnt.replace(nc['joint'], nc['joint_bind']))
        cmds.setAttr(bind_joint + '.radius', 1.5)
        if bind_joints:
            cmds.parent(bind_joint, bind_joints[-1])
        elif bind_parent:
            cmds.parent(bind_joint, bind_parent)
        influences = []
        for k, ctrl in enumerate(ik_ctrls):
            left = ik_fractions[k - 1] if k > 0 else None
            right = ik_fractions[k + 1] if k + 1 < len(ik_ctrls) else None
            f = fractions[num]
            if f <= ik_fractions[k]:
                weight = 1.0 if left is None else max(0.0, (f - left) / (ik_fractions[k] - left))
            else:
                weight = 1.0 if right is None else max(0.0, (right - f) / (right - ik_fractions[k]))
            if weight > 1e-3:
                influences.append((ctrl, weight))
        influences += [(ctrl, 1.0) for ctrl, closest in fk_items if closest == num]
        source = tweak_ctrls[num] + '.worldMatrix[0]' if tweak_ctrls else joint_worlds[num]
        scale_matrix = _ctrl_scale_matrix(limb, label + '_Bind', influences, rest[num])
        world = limb._mult_matrix(label + '_Bind_MultMatrix', [scale_matrix, source]) if scale_matrix else source
        if tweak_ctrls:
            # the joint squash under the tweaker
            squash_scale = cmds.createNode('pickMatrix', n=label + '_BindSquash_PickMatrix')
            cmds.connectAttr(joint_worlds[num], squash_scale + '.inputMatrix')
            for attr, value in (('useTranslate', 0), ('useRotate', 0), ('useScale', 1), ('useShear', 0)):
                cmds.setAttr(squash_scale + '.' + attr, value)
            world = limb._mult_matrix(label + '_BindSquash_MultMatrix', [squash_scale + '.outputMatrix', world])
        if previous_world:
            inverse = cmds.createNode('inverseMatrix', n=label + '_ParentBind_InverseMatrix')
            cmds.connectAttr(previous_world, inverse + '.inputMatrix')
            _drive_local(bind_joint, world, inverse + '.outputMatrix', label + '_Bind')
        elif bind_parent:
            _drive_local(bind_joint, world, bind_parent + '.worldInverseMatrix[0]', label + '_Bind')
        else:
            _drive(bind_joint, world, label + '_Bind')
        previous_world = world
        bind_joints.append(bind_joint)

    if do_tweakers:
        limb.free_controller_scale(tweak_ctrls)

    # constraints -> matrix nodes (the mid ik blends keep their constraints, animated weights)
    new_constraints = [c for c in cmds.ls(type='constraint') if c not in old_constraints]
    kept = limb.constraints_to_matrix(new_constraints, unscaled_targets=set(scaled_ctrls))
    print('QuadSpine matrix swap: {} constraints replaced, {} kept'.format(len(new_constraints) - len(kept), len(kept)))

    # the switch shape is instanced under every spine controller, its attrs move to a data node (no cycle)
    limb.switch_attrs_to_data_node(share_loc)

    print ('Build {} Success'.format(block))
