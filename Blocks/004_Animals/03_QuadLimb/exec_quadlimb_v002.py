from __future__ import absolute_import, division
from maya import cmds, mel
import maya.api.OpenMaya as om
import json
import math
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
PYBLOCK_NAME = 'exec_quadlimb'

#Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-3]
FOLDER=''
for f in PATH_PARTS:
    FOLDER = os.path.join(FOLDER, f)

JSON_FILE = os.path.join(FOLDER, 'config', 'name_conventions.json')
with open(JSON_FILE) as json_file:
	nc = json.load(json_file)
#Read curve shapes info
CURVE_FILE = os.path.join(FOLDER, 'config', 'curves.json')
with open(CURVE_FILE) as curve_file:
	curve_data = json.load(curve_file)
#setup File
SETUP_FILE = os.path.join(FOLDER, 'config', 'rig_setup.json')
with open(SETUP_FILE) as setup_file:
	setup = json.load(setup_file)

MODULE_FILE = os.path.join(os.path.dirname(__file__),'03_QuadLimb.json')
with open(MODULE_FILE) as module_file:
	module = json.load(module_file)

#---------------------------------------------
# v002 (same plan as Limb v002): same guides, joints, controllers and bind joint names as v001, so skins, saved
# controllers and the blocks that use the leg (Foot, Smart_RFL, Spaces, attrs) keep working. Faster playback:
# constraints swapped for matrix nodes, follicles for uvPins, the switch shape attrs moved to a data node (no
# evaluation cycles), the bendy tweakers ride the Limb v002 bendy path (BendyCurve attrs) instead of aim locators.
# Per leg GlobalScale controller (L_BkLeg_GlobalScale_Ctrl), the Foot v002 block finds it and scales the foot
# with the leg. Controllers scale the bind joints around them, the ball controllers (IK, SubIk, FK) scale the
# ball joint (L_BkBall_Jnt) so the Foot v002 foot scales with them.


def _limb():
    """Limb v002 node helpers (matrix swap, uvPins, switch data node, bendy path, controllers scale)."""
    limb_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                               '002_Biped', '004_Limb')
    if limb_folder not in sys.path:
        sys.path.append(limb_folder)
    import exec_limb_v002
    return exec_limb_v002


def create_quadlimb_block(name = 'QuadLimb'):

    nc, curve_data, setup = mt.import_configs()
    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    limb_name = name.split(',')
    if cmds.objExists('{}{}'.format(limb_name[0],nc['module'])):
        cmds.warning('Name already exists.')
        return

    block = mt.create_block(name = limb_name[0], icon = 'Quad_Limb',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]
    name = block.replace(nc['module'],'')


    cmds.select(cl=True)

    joint_one = mt.create_joint_guide(name=limb_name[0])
    cmds.move(5, 0, 0)
    joint_two = mt.create_joint_guide(name=limb_name[1])
    cmds.move(15, 0, -8)
    joint_three = mt.create_joint_guide(name=limb_name[2])
    cmds.move(25, 0, 5)
    joint_four = mt.create_joint_guide(name=limb_name[3])
    cmds.move(35, 0, -4)
    cmds.parent(joint_four, joint_three)
    cmds.parent(joint_three, joint_two)
    cmds.parent(joint_two, joint_one)

    cmds.rotate(180,0,-90, joint_one)
    cmds.move(5,30,0, joint_one)

    cmds.parent(joint_one, block)

    mt.orient_joint(input=joint_one)
    mt.orient_joint(input=joint_two)
    mt.orient_joint(input=joint_three)
    mt.orient_joint(input=joint_four)
    cmds.select(block)

    cmds.select(cl=True)
    pv_joint = mt.create_joint_guide(name=limb_name[0]+'_PV')
    cmds.parent(pv_joint, block)
    cmds.delete(cmds.pointConstraint(joint_four, pv_joint))
    cmds.setAttr(pv_joint + '.tz', cmds.getAttr(joint_two + '.translateX') * 2)
    cmds.setAttr(pv_joint + '.ty', 18)

    cmds.setAttr("{}.jointOrientX".format(joint_four), 0)
    cmds.setAttr("{}.jointOrientY".format(joint_four), 0)
    cmds.setAttr("{}.jointOrientZ".format(joint_four), 0)


    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_quadlimb_block()

#-------------------------

def _orient_chain_compat(root_joint):
    """Orient a joint chain in a Maya-version-safe way."""
    if not root_joint or not cmds.objExists(root_joint):
        return

    cmds.select(root_joint)
    try:
        mel.eval("joint -e -oj xzy -sao zup -aos -ch -zso;")
    except Exception:
        mel.eval("joint -e -oj xzy -sao zup -ch -zso;")


def pole_on_leg_plane(pv_loc, start, mid, end):
    """Move pv_loc onto the start / mid / end plane, on the side the mid joint bends to."""
    s, m, e = [om.MVector(cmds.xform(n, q=True, t=True, ws=True)) for n in (start, mid, end)]
    normal = (m - s) ^ (e - s)
    if normal.length() < 1e-6:
        return
    normal.normalize()
    p = om.MVector(cmds.xform(pv_loc, q=True, t=True, ws=True))
    p -= normal * ((p - s) * normal)
    line = (e - s).normal()
    foot = s + line * ((m - s) * line)
    bend = m - foot
    if bend.length() > 1e-6:
        bend.normalize()
        side = (p - foot) * bend
        if side < 0:
            p -= bend * (2 * side)
    cmds.xform(pv_loc, ws=True, t=list(p))

#-------------------------
# Ribbons: same nodes and names as the v001 (kinematics.create_mid_ribbons) ones, minus what the bendy path
# replaces (aim locators, blended tweaker constraints). Follicles become uvPins at the end of the build.

def create_mid_ribbons(name, first_joint, last_joint, twist_joints, twist_amount, ctrl_size, sec_color,
                       switch_locator, vis_attrs, limb_scale):
    """vis_attrs: (offsets, ends, tweaks) attrs. Returns the ribbon data for the bendy path."""
    offsets_vis, ends_vis, tweaks_vis = vis_attrs

    # twist ribbon, one follicle + joint per bind joint
    ribbon_limb_nurb = cmds.nurbsPlane(ch=1, d=1, v=1, p=(0, 0, 0), u=1, w=1, ax=(0, 0, 1), lr=1,
                                       n=name + 'Ribbon' + nc['nurb'])
    cluster01 = cmds.cluster(ribbon_limb_nurb[0] + '.cv[0][0:1]')
    cluster02 = cmds.cluster(ribbon_limb_nurb[0] + '.cv[1][0:1]')
    cmds.setAttr(str(ribbon_limb_nurb[0]) + '.visibility', 0)
    cmds.delete(cmds.parentConstraint(first_joint, cluster01, mo=False))
    cmds.delete(cmds.parentConstraint(last_joint, cluster02, mo=False))
    cmds.delete(ribbon_limb_nurb, ch=True)
    cmds.rebuildSurface(ribbon_limb_nurb[0], rt=0, kc=0, fr=0, end=1, sv=1, su=twist_amount, kr=0,
                        dir=2, kcp=0, tol=0.01, dv=1, du=3, rpo=1)

    cmds.select(ribbon_limb_nurb[0])
    mel.eval("createHair {} 1 10 0 0 0 0 5 0 1 2 1;".format(twist_amount))
    cmds.delete('hairSystem1', 'pfxHair1', 'nucleus1')
    cmds.setAttr(ribbon_limb_nurb[0] + '.inheritsTransform', 0)
    for C in range(1, twist_amount + 1):
        cmds.delete('curve' + str(C))
    fol_grp = cmds.rename('hairSystem1Follicles', name + nc['follicle'] + nc['group'])

    follicles = cmds.ls(fol_grp, dag=True, type='follicle')
    fol_joints = []
    cmds.setAttr(follicles[0] + '.parameterU', 0)
    for num, i in enumerate(follicles):
        cmds.select(i)
        fol_new_name = cmds.rename(cmds.listRelatives(i, p=True), name + '_' + str(num) + nc['follicle'])
        fol_jnt = cmds.joint(n=name + '_' + str(num) + nc['joint'])
        fol_joints.append(fol_jnt)
        # normalize follicles with the leg scale
        cmds.connectAttr(limb_scale, fol_new_name + '.scale')
    cmds.skinCluster(twist_joints[:-1], ribbon_limb_nurb[0], sm=0, bm=1, tsb=True)

    # tweakers: Root > Auto (bendy path) > ForwardAim > Ctrl
    tweks_ribbon_ctrl_grp = cmds.group(em=True, n=name + '_Ribbons' + nc['ctrl'] + nc['group'])
    ribbon_ctrls = []
    for fol_jnt in fol_joints:
        ctrl = mt.curve(input=fol_jnt, type='square', rename=True, custom_name=True,
                        name=fol_jnt.replace(nc['joint'], nc['ctrl']), size=ctrl_size / 3)
        mt.shape_with_attr(input='', obj_name=switch_locator.replace(nc['locator'], ''), attr_name='')
        mt.assign_color(ctrl, sec_color)
        root, auto = mt.root_grp(input=ctrl, autoRoot=True)
        cmds.parentConstraint(cmds.listRelatives(fol_jnt, p=True)[0], root, mo=False)
        cmds.parentConstraint(ctrl, fol_jnt)
        cmds.parent(root, tweks_ribbon_ctrl_grp)
        mt.root_grp(ctrl, custom=True, custom_name='_ForwardAim')
        cmds.connectAttr(tweaks_vis, '{}.v'.format(cmds.listRelatives(ctrl, shapes=True)[0]))
        ribbon_ctrls.append(ctrl)

    # bendy surface
    middle_limb_nurb = cmds.nurbsPlane(ch=1, d=1, v=1, p=(0, 0, 0), u=1, w=1, ax=(0, 0, 1), lr=1,
                                       n=name + 'Bendy' + nc['nurb'])
    cluster01 = cmds.cluster(middle_limb_nurb[0] + '.cv[0][0:1]')
    cluster02 = cmds.cluster(middle_limb_nurb[0] + '.cv[1][0:1]')
    cmds.delete(cmds.parentConstraint(first_joint, cluster01, mo=False))
    cmds.delete(cmds.parentConstraint(last_joint, cluster02, mo=False))
    cmds.delete(middle_limb_nurb, ch=True)
    cmds.rebuildSurface(middle_limb_nurb[0], rt=0, kc=0, fr=0, end=1, sv=1, su=len(twist_joints) + 1, kr=0,
                        dir=2, kcp=0, tol=0.01, dv=1, du=3, rpo=1)

    middle_joints = mt.joints_middle(start=first_joint, end=last_joint, axis=setup['twist_axis'], amount=4,
                                     name='BendyMid')
    for jnt in middle_joints:
        try:
            cmds.parent(jnt, w=True)
        except:
            pass
    cmds.parent(middle_joints[1], middle_joints[0])
    cmds.parent(middle_joints[2], middle_joints[3])
    cmds.delete(cmds.parentConstraint(first_joint, last_joint, middle_joints[1], mo=False))
    cmds.delete(cmds.parentConstraint(first_joint, last_joint, middle_joints[2], mo=False))
    ik_bendy_grp = cmds.group(middle_joints[0], middle_joints[3], n='{}_BendyIK{}'.format(name, nc['group']))

    # handles
    top_ik_bendy_ctrl = mt.curve(input=first_joint, type='pin_cube', rename=True, custom_name=True,
                                 name=name.replace(nc['joint'], '_Top_Handle' + nc['ctrl']), size=ctrl_size / 3)
    top_ik_bendy_root = mt.root_grp()
    mt.assign_color(top_ik_bendy_ctrl, sec_color)
    cmds.delete(cmds.parentConstraint(first_joint, top_ik_bendy_root))
    mt.shape_with_attr(input=top_ik_bendy_ctrl, obj_name=switch_locator.replace(nc['locator'], ''), attr_name='')
    mt.hide_attr(input=top_ik_bendy_ctrl, t=True, r=False, s=True, v=True)

    bottom_ik_bendy_ctrl = mt.curve(input=last_joint, type='pin_cube', rename=True, custom_name=True,
                                    name=name.replace(nc['joint'], '_Bottom_Handle' + nc['ctrl']), size=ctrl_size / 3)
    mt.assign_color(bottom_ik_bendy_ctrl, sec_color)
    bottom_ik_bendy_root = mt.root_grp()
    cmds.delete(cmds.parentConstraint(last_joint, bottom_ik_bendy_root))
    mt.shape_with_attr(input=bottom_ik_bendy_ctrl, obj_name=switch_locator.replace(nc['locator'], ''), attr_name='')
    mt.hide_attr(input=bottom_ik_bendy_ctrl, t=True, r=False, s=True, v=True)

    cmds.rotate(0, 0, 90 - cmds.getAttr('{}.jointOrientZ'.format(last_joint)),
                '{}.cv[0:22]'.format(bottom_ik_bendy_ctrl), r=True)
    cmds.rotate(0, 0, -90, '{}.cv[0:22]'.format(top_ik_bendy_ctrl), r=True)
    for handle in [top_ik_bendy_ctrl, bottom_ik_bendy_ctrl]:
        cmds.connectAttr(offsets_vis, '{}.v'.format(cmds.listRelatives(handle, shapes=True)[0]))

    # handles bend a local copy, blended onto the bendy surface; the twist only copy (pin) is what the
    # bendy path reads to know how much the handles bend
    local_geo_ik_geo = cmds.duplicate(middle_limb_nurb[0], n=name + 'Bendy_IK_Local' + nc['nurb'])
    cmds.skinCluster(middle_joints, local_geo_ik_geo, sm=0, bm=1, tsb=True)
    pin_surface = cmds.duplicate(middle_limb_nurb[0], n=name + 'Bendy_Pin' + nc['nurb'])[0]
    cmds.select(local_geo_ik_geo, middle_limb_nurb[0])
    cmds.blendShape(n='{}_Bendy{}'.format(name, '_BS'), w=[(0, 1)])
    cmds.skinCluster(twist_joints, middle_limb_nurb[0], sm=0, bm=1, tsb=True)
    cmds.skinCluster(twist_joints, pin_surface, sm=0, bm=1, tsb=True)
    cmds.setAttr(pin_surface + '.inheritsTransform', 0)
    cmds.setAttr(pin_surface + '.visibility', 0)
    local_grp = cmds.group(local_geo_ik_geo, ik_bendy_grp, n=name + '_Local' + nc['group'])

    cmds.connectAttr(top_ik_bendy_ctrl + '.rotate', middle_joints[0] + '.rotate')
    cmds.connectAttr(bottom_ik_bendy_ctrl + '.rotate', middle_joints[3] + '.rotate')

    # start / end bendy controllers on the bendy surface
    cmds.select(middle_limb_nurb[0])
    mel.eval("createHair {} 1 10 0 0 0 0 5 0 1 2 1;".format(3))
    cmds.delete('hairSystem1', 'pfxHair1', 'nucleus1')
    cmds.setAttr(middle_limb_nurb[0] + '.inheritsTransform', 0)
    for C in range(1, 4):
        cmds.delete('curve' + str(C))
    bendy_fol_grp = cmds.rename('hairSystem1Follicles', name + '_Bendy' + nc['follicle'] + nc['group'])
    bendy_follicles = cmds.ls(bendy_fol_grp, dag=True, type='follicle')
    # v002: start / end bendy controllers ride the twist only (pin) surface: on the bendy surface their own
    # handles bend what they sit on, an evaluation cycle (the leg evaluated serial, several times a frame)
    pin_shape = cmds.listRelatives(pin_surface, s=True, ni=True)[0]
    for fol in bendy_follicles:
        cmds.connectAttr(pin_shape + '.worldSpace[0]', fol + '.inputSurface', f=True)
        cmds.connectAttr(pin_shape + '.worldMatrix[0]', fol + '.inputWorldMatrix', f=True)
    cmds.setAttr(bendy_follicles[0] + '.parameterU', 0.05)
    cmds.setAttr(bendy_follicles[-1] + '.parameterU', 0.95)

    second_ctrls = []
    second_roots = []
    for num, fol in enumerate([bendy_follicles[0], bendy_follicles[-1]]):
        ribbon_ctrl = mt.curve(input=fol, type='sphere', rename=True, custom_name=True,
                               name=name.replace(nc['joint'], ['Start', 'End'][num] + '_Bendy' + nc['ctrl']),
                               size=ctrl_size / 1.5)
        mt.assign_color(ribbon_ctrl, sec_color)
        root, auto = mt.root_grp(input=ribbon_ctrl, autoRoot=True)
        cmds.parentConstraint(cmds.listRelatives(fol, p=True)[0], root, mo=False)
        cmds.connectAttr(ends_vis, '{}.v'.format(cmds.listRelatives(ribbon_ctrl, shapes=True)[0]))
        second_ctrls.append(ribbon_ctrl)
        second_roots.append(root)
        mt.shape_with_attr(input=ribbon_ctrl, obj_name=switch_locator.replace(nc['locator'], ''), attr_name='')
        cmds.connectAttr(limb_scale, cmds.listRelatives(fol, p=True)[0] + '.scale')
        # unused bendy follicle
    for fol in bendy_follicles[1:-1]:
        cmds.delete(cmds.listRelatives(fol, p=True)[0])

    cmds.parentConstraint(second_ctrls[0], top_ik_bendy_root, mo=True)
    cmds.parentConstraint(second_ctrls[1], bottom_ik_bendy_root, mo=True)

    ribbon_ctrl_grp = cmds.group(n=name.replace(nc["joint"], '_Ribbon' + nc['ctrl'] + nc['group']), em=True)
    cmds.parent(second_roots, tweks_ribbon_ctrl_grp, bottom_ik_bendy_root, top_ik_bendy_root, ribbon_ctrl_grp)
    ribbon_rig_group = cmds.group(n=name.replace(nc["joint"], '_Ribbon_Rig' + nc['group']), em=True)
    cmds.parent(local_grp, bendy_fol_grp, middle_limb_nurb[0], pin_surface, ribbon_rig_group)

    # the bind drivers get the main joint scale (ik stretch), the twist joints also carry the bone length
    for fol_jnt in fol_joints:
        cmds.connectAttr('{}.scale'.format(first_joint), '{}.scale'.format(fol_jnt))

    return {'ribbon_ctrl_grp': ribbon_ctrl_grp, 'ribbon_ctrls': ribbon_ctrls,
            'ribbon_plane': ribbon_limb_nurb[0], 'fol_ribbon_grp': fol_grp, 'fol_joints': fol_joints,
            'second_ctrls': second_ctrls, 'handle_controllers': [top_ik_bendy_ctrl, bottom_ik_bendy_ctrl],
            'handle_controllers_roots': [bottom_ik_bendy_root[0], top_ik_bendy_root[0]],
            'clean_rig_grp': ribbon_rig_group, 'clean_ctrl_grp': ribbon_ctrl_grp,
            'middle_joints': middle_joints, 'middle_surface': middle_limb_nurb[0], 'pin_surface': pin_surface}

#-------------------------
# The Limb v002 matrix swap reads the driven node own parentInverseMatrix / parentMatrix / rotateOrder, for the
# evaluation manager that is a cycle (node -> its driver -> node) per driven node. Same matrices from the parent
# (worldInverseMatrix / worldMatrix) and a constant rotate order, no cycle.

def break_self_cycles(nodes):
    fixed = 0
    for node in cmds.ls(list(nodes), type='multMatrix'):
        for index in cmds.getAttr(node + '.matrixIn', multiIndices=True) or []:
            plug = '{}.matrixIn[{}]'.format(node, index)
            source = (cmds.listConnections(plug, s=True, d=False, p=True) or [None])[0]
            if not source:
                continue
            owner, attr = source.split('.', 1)
            if not attr.startswith(('parentInverseMatrix', 'parentMatrix')):
                continue
            parent = (cmds.listRelatives(owner, p=True, f=True) or [None])[0]
            inverse = attr.startswith('parentInverseMatrix')
            if parent and cmds.getAttr(owner + '.inheritsTransform'):
                cmds.connectAttr('{}.{}[0]'.format(parent, 'worldInverseMatrix' if inverse else 'worldMatrix'), plug, f=True)
            else:
                # no parent or not inheriting it: the parent space is the world
                cmds.disconnectAttr(source, plug)
                cmds.setAttr(plug, list(om.MMatrix()), type='matrix')
            fixed += 1
    for node in cmds.ls(list(nodes), type='decomposeMatrix'):
        source = (cmds.listConnections(node + '.inputRotateOrder', s=True, d=False, p=True) or [None])[0]
        if source:
            value = cmds.getAttr(source)
            cmds.disconnectAttr(source, node + '.inputRotateOrder')
            cmds.setAttr(node + '.inputRotateOrder', value)
            fixed += 1
    return fixed


def twist_follow_length(segments, axis, ribbons):
    """Limb v002 twist_follow_length for any number of bones. segments: [(parent, child, twist joints)].
    The twist chains follow the bone length (FK scale makes the bones longer), the ik stretch (main joint
    scale) is not counted twice."""
    for parent, child, twist_joints in segments:
        rest = cmds.getAttr('{}.translate{}'.format(child, axis))
        if abs(rest) < 1e-6:
            continue
        ratio = cmds.createNode('multiplyDivide', n=child + '_BoneLength_MultiplyDivide')
        cmds.setAttr(ratio + '.operation', 2)
        cmds.connectAttr('{}.translate{}'.format(child, axis), ratio + '.input1X')
        cmds.setAttr(ratio + '.input2X', rest)
        if ribbons:
            for jnt in twist_joints:
                for source in cmds.listConnections(jnt + '.scale', s=True, d=False, p=True) or []:
                    cmds.disconnectAttr(source, jnt + '.scale')
                    for other in 'XYZ'.replace(axis, ''):
                        cmds.connectAttr('{}{}'.format(source, other), '{}.scale{}'.format(jnt, other))
                length = cmds.createNode('multDoubleLinear', n=jnt + '_BoneLength_MultDoubleLinear')
                cmds.connectAttr(ratio + '.outputX', length + '.input1')
                cmds.connectAttr('{}.scale{}'.format(parent, axis), length + '.input2')
                cmds.connectAttr(length + '.output', '{}.scale{}'.format(jnt, axis), f=True)
            continue
        for jnt in twist_joints[1:]:
            spacing = cmds.createNode('multDoubleLinear', n=jnt + '_BoneLength_MultDoubleLinear')
            cmds.connectAttr(ratio + '.outputX', spacing + '.input1')
            cmds.setAttr(spacing + '.input2', cmds.getAttr('{}.translate{}'.format(jnt, axis)))
            cmds.connectAttr(spacing + '.output', '{}.translate{}'.format(jnt, axis), f=True)


def bend_amount(limb, name, a, b, c):
    """0 straight, 1 at 90 degrees or more at b (1 - cos of the angle between a->b and b->c)."""
    directions = []
    for num, (start, end) in enumerate([(a, b), (b, c)]):
        unit = cmds.createNode('vectorProduct', n='{}_Bone{}_VectorProduct'.format(name, num))
        cmds.setAttr(unit + '.operation', 0)
        cmds.setAttr(unit + '.normalizeOutput', 1)
        cmds.connectAttr(limb._vector_op('{}_Bone{}_PlusMinusAverage'.format(name, num), limb._world_position(end),
                                         limb._world_position(start), 2), unit + '.input1')
        directions.append(unit + '.output')
    cosine = cmds.createNode('vectorProduct', n=name + '_Bend_VectorProduct')
    cmds.setAttr(cosine + '.operation', 1)
    cmds.connectAttr(directions[0], cosine + '.input1')
    cmds.connectAttr(directions[1], cosine + '.input2')
    bend = cmds.createNode('clamp', n=name + '_Bend_Clamp')
    cmds.setAttr(bend + '.maxR', 1)
    cmds.connectAttr(limb._add(name + '_Bend_AddDoubleLinear',
                               limb._mult(name + '_Bend_MultDoubleLinear', cosine + '.outputX', -1), 1), bend + '.inputR')
    return bend + '.outputR'


def build_bendy_paths(limb, data):
    """Bendy path per segment: Hip -> KneeMid, KneeMid -> AnkleMid, AnkleMid -> Ball. BendyCurve 0 straight
    lines through the mid bendy controllers, 10 the arc through the segment ends and the other point."""
    j = data['main_joints']
    hip, ball = [limb._world_position(x) for x in (j[0], j[3])]
    knee_mid, ankle_mid = [limb._world_position(c) for c in data['mid_ctrls']]
    attrs = data['curve_attrs']
    name = data['main_joints'][0].replace(nc['joint'], '_Bendy')
    knee_bend = bend_amount(limb, name + 'Knee', j[0], j[1], j[2])
    ankle_bend = bend_amount(limb, name + 'Ankle', j[1], j[2], j[3])

    def segment_curve(label, bend, offset):
        base = limb._add('{}_{}Base_AddDoubleLinear'.format(name, label), attrs['curve'],
                         limb._mult('{}_{}Auto_MultDoubleLinear'.format(name, label), attrs['auto'], bend))
        total = cmds.createNode('clamp', n='{}_{}Curve_Clamp'.format(name, label))
        cmds.setAttr(total + '.minR', -10)
        cmds.setAttr(total + '.maxR', 10)
        cmds.connectAttr(limb._add('{}_{}Curve_AddDoubleLinear'.format(name, label), base, offset), total + '.inputR')
        return limb._mult('{}_{}Curve_MultDoubleLinear'.format(name, label), total + '.outputR', 0.1)

    segments = [(data['ribbons'][0], (hip, knee_mid, ankle_mid), segment_curve('Upper', knee_bend, attrs['upper']),
                 limb._mult(name + '_StartEase_MultDoubleLinear', attrs['start_ease'], 0.1), True),
                (data['ribbons'][1], (knee_mid, ankle_mid, hip), segment_curve('Mid', knee_bend, attrs['mid']), None, True),
                (data['ribbons'][2], (ankle_mid, ball, knee_mid), segment_curve('Lower', ankle_bend, attrs['lower']),
                 limb._mult(name + '_EndEase_MultDoubleLinear', attrs['end_ease'], 0.1), False)]
    for ribbon, (seg_start, seg_end, other), curve, ease, ease_at_start in segments:
        offsets = [limb.bendy_move(ctrl, ctrl) for ctrl in ribbon['second_ctrls']]
        seg_name = ribbon['second_ctrls'][0].replace('Start_Bendy' + nc['ctrl'], '_BendyPath')
        limb.bendy_segment_path(seg_name, seg_start, seg_end, other, curve, ribbon['ribbon_ctrls'], offsets[0],
                                offsets[1], ribbon['middle_surface'], ribbon['pin_surface'], ease, ease_at_start)


SOFT_IK_RANGE = 0.02  # SoftIk 10 = soft zone of 20% of the hip -> ankle length


def soft_stretch_ik(limb, name, soft_grp, hip, soft_attr, stretch_attr, lengths, rig_scale, chain_joints, ankle_joint,
                    old_condition):
    """Stretch + soft IK on the hip -> ankle handle (same math as Limb v002 ArmsSoftIk / LegSoftIK), D hip -> ankle
    target and L hip -> knee -> ankle length, both without the leg scale, s = SoftIk * 2% of L (0 with no SoftIk):
        softD = D                                  if D <= L - s
                L - s * e^(-(D - (L - s)) / s)     if D >  L - s
    no stretch: soft_grp (the handle target) moves back D - softD towards the hip, the knee eases to straight.
    Stretch_On: the hip and knee bones scale by D / softD instead (from the soft threshold), the ankle stays on its
    target. The ankle -> ball bone does not stretch (it follows the ball controller)."""
    chain = sum(lengths)
    parent = cmds.listRelatives(soft_grp, p=True)[0]
    goal = limb._world_position(parent)
    length = cmds.createNode('distanceBetween', n=name + '_DistanceBetween')
    cmds.connectAttr(hip, length + '.point1')
    cmds.connectAttr(goal, length + '.point2')
    distance = limb._divide_scalar(name + '_Normalize_MultiplyDivide', length + '.distance', rig_scale)

    soft = limb._mult(name + '_Soft_MultDoubleLinear', soft_attr, SOFT_IK_RANGE * chain)
    safe_soft = limb._clamp(name + '_SafeSoft_Clamp', soft, 1e-4, 1e6)
    threshold = limb._add(name + '_Threshold_AddDoubleLinear', chain, limb._mult(name + '_NegSoft_MultDoubleLinear', soft, -1))
    over = limb._clamp(name + '_Over_Clamp', limb._add(name + '_Over_AddDoubleLinear', distance,
                                                        limb._mult(name + '_NegThreshold_MultDoubleLinear', threshold, -1)), 0, 1e6)
    exponent = limb._mult(name + '_Exponent_MultDoubleLinear', limb._divide_scalar(name + '_Exponent_MultiplyDivide', over, safe_soft), -1)
    power = cmds.createNode('multiplyDivide', n=name + '_Exp_MultiplyDivide')
    cmds.setAttr(power + '.operation', 3)
    cmds.setAttr(power + '.input1X', math.e)
    cmds.connectAttr(exponent, power + '.input2X')
    # pull = over - s * (1 - e^(-over / s)), 0 inside the threshold; with no soft (s tiny) it is D - L past full reach
    eased_over = limb._mult(name + '_EasedOver_MultDoubleLinear', safe_soft,
                            limb._add(name + '_OneMinusExp_AddDoubleLinear', limb._mult(name + '_NegExp_MultDoubleLinear', power + '.outputX', -1), 1))
    pull = limb._add(name + '_Pull_AddDoubleLinear', over, limb._mult(name + '_NegEasedOver_MultDoubleLinear', eased_over, -1))
    soft_dist = limb._add(name + '_SoftDist_AddDoubleLinear', distance, limb._mult(name + '_NegPull_MultDoubleLinear', pull, -1))

    # stretch: D / softD (1 inside the threshold), blended by Stretch_On
    factor = limb._divide_scalar(name + '_StretchFactor_MultiplyDivide', distance,
                                 limb._clamp(name + '_SafeSoftDist_Clamp', soft_dist, 1e-4, 1e6))
    stretch = limb._add(name + '_Stretch_AddDoubleLinear', 1, limb._mult(
        name + '_StretchOn_MultDoubleLinear', limb._add(name + '_StretchOver_AddDoubleLinear', factor, -1), stretch_attr))
    for jnt in chain_joints:
        cmds.connectAttr(stretch, jnt + '.scaleX', f=True)
    for plug in cmds.listConnections(ankle_joint + '.scaleX', s=True, d=False, p=True) or []:
        cmds.disconnectAttr(plug, ankle_joint + '.scaleX')
    cmds.setAttr(ankle_joint + '.scaleX', 1)

    # no stretch: pull the handle target back D - softD
    no_stretch = limb._add(name + '_NoStretch_AddDoubleLinear', limb._mult(name + '_NegStretch_MultDoubleLinear', stretch_attr, -1), 1)
    pull = limb._mult(name + '_PullWorld_MultDoubleLinear', limb._mult(name + '_PullOn_MultDoubleLinear', pull, no_stretch), rig_scale)
    direction = cmds.createNode('vectorProduct', n=name + '_Direction_VectorProduct')
    cmds.setAttr(direction + '.operation', 0)
    cmds.setAttr(direction + '.normalizeOutput', 1)
    cmds.connectAttr(limb._vector_op(name + '_Direction_PlusMinusAverage', goal, hip, 2), direction + '.input1')
    back = limb._vector_scale(name + '_Back_MultiplyDivide', direction + '.output', limb._mult(name + '_NegPullWorld_MultDoubleLinear', pull, -1))
    local = cmds.createNode('vectorProduct', n=name + '_Local_VectorProduct')
    cmds.setAttr(local + '.operation', 3)
    cmds.connectAttr(back, local + '.input1')
    cmds.connectAttr(parent + '.worldInverseMatrix[0]', local + '.matrix')
    cmds.connectAttr(local + '.output', soft_grp + '.translate')


def build_lean_paths(limb, data):
    """BendyCurve off: the bendy path at curve 0 with far less nodes. Tweakers on the straight lines
    hip -> knee mid -> ankle mid -> ball bendy controllers, the Start / End bendy moves fade along the segment,
    the handles bend added, aimed along the segment (the twist from the ribbon)."""
    j = data['main_joints']
    points = [limb._world_position(j[0])] + [limb._world_position(c) for c in data['mid_ctrls']] + [limb._world_position(j[3])]
    for seg, ribbon in enumerate(data['ribbons']):
        start, end = points[seg], points[seg + 1]
        name = ribbon['second_ctrls'][0].replace('Start_Bendy' + nc['ctrl'], '_BendyLean')
        start_off, end_off = [limb.bendy_move(ctrl, ctrl) for ctrl in ribbon['second_ctrls']]
        moved_start = limb._vector_op(name + '_Start_PlusMinusAverage', start, start_off, 1)
        moved_end = limb._vector_op(name + '_End_PlusMinusAverage', end, end_off, 1)
        tangent = limb._vector_op(name + '_Tangent_PlusMinusAverage', moved_end, moved_start, 2)

        rest_start = om.MVector(cmds.getAttr(start)[0])
        rest_chord = om.MVector(cmds.getAttr(end)[0]) - rest_start
        u_values = []
        for ctrl in ribbon['ribbon_ctrls']:
            rest = limb._world(ctrl)
            u = ((om.MVector(rest[12], rest[13], rest[14]) - rest_start) * rest_chord) / (rest_chord * rest_chord)
            u_values.append(min(1.0, max(0.0, u)))
        bends = limb._surface_bend(name, ribbon['middle_surface'], ribbon['pin_surface'], u_values)

        for num, ctrl in enumerate(ribbon['ribbon_ctrls']):
            point = '{}_{}'.format(name, num)
            forward_grp = cmds.listRelatives(ctrl, p=True)[0]
            auto_grp = cmds.listRelatives(forward_grp, p=True)[0]
            root_grp = cmds.listRelatives(auto_grp, p=True)[0]
            rest_ctrl = limb._world(ctrl)
            position = cmds.createNode('plusMinusAverage', n=point + '_Position_PlusMinusAverage')
            cmds.connectAttr(limb._vector_lerp(point + '_Line_BlendColors', moved_start, moved_end, u_values[num]),
                             position + '.input3D[0]')
            cmds.connectAttr(bends[num], position + '.input3D[1]')
            residual = om.MVector(rest_ctrl[12], rest_ctrl[13], rest_ctrl[14]) - om.MVector(cmds.getAttr(position + '.output3D')[0])
            cmds.setAttr(position + '.input3D[2]', *residual)
            compose = cmds.createNode('composeMatrix', n=point + '_Position_ComposeMatrix')
            cmds.connectAttr(position + '.output3D', compose + '.inputTranslate')

            # the root frame (ribbon twist) turned the shortest way onto the segment + the handles bend slope
            # (from the neighbour bend samples, so the tweakers turn with the bend)
            before, after = max(0, num - 1), min(len(u_values) - 1, num + 1)
            step = u_values[after] - u_values[before]
            point_tangent = tangent
            if step > 1e-6:
                slope = limb._vector_scale(point + '_BendSlope_MultiplyDivide',
                                           limb._vector_op(point + '_BendSlope_PlusMinusAverage', bends[after], bends[before], 2),
                                           1.0 / step)
                point_tangent = limb._vector_op(point + '_Tangent_PlusMinusAverage', tangent, slope, 1)
            primary_axis, _ = limb._closest_axis(limb._world(root_grp), rest_chord)
            aim = cmds.createNode('aimMatrix', n=point + '_AimMatrix')
            cmds.connectAttr(root_grp + '.worldMatrix[0]', aim + '.inputMatrix')
            cmds.setAttr(aim + '.primaryInputAxis', *primary_axis)
            cmds.setAttr(aim + '.primaryMode', 2)
            cmds.connectAttr(point_tangent, aim + '.primaryTargetVector')
            cmds.setAttr(aim + '.secondaryMode', 0)
            rotation = limb._pick_matrix(point + '_Rotation_PickMatrix', aim + '.outputMatrix', translate=False)
            offset = limb._only_rotate(rest_ctrl) * limb._only_rotate(limb._plug_matrix(rotation)).inverse()
            # auto group channels stay at rest, it moves through its offset parent matrix (one node):
            # ctrl world = inner * OPM * root world, inner = ctrl and forward group rest locals
            for attr in ['translate', 'rotate']:
                cmds.setAttr('{}.{}'.format(auto_grp, attr), 0, 0, 0)
            cmds.setAttr(forward_grp + '.rotate', 0, 0, 0)
            inner = limb._world(ctrl) * limb._world(auto_grp).inverse()
            cmds.connectAttr(limb._mult_matrix(point + '_MultMatrix', [inner.inverse() * offset, rotation,
                                                                       compose + '.outputMatrix',
                                                                       root_grp + '.worldInverseMatrix[0]']),
                             auto_grp + '.offsetParentMatrix', f=True)


def build_quadlimb_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()
    limb = _limb()
    limb._BUILD_CACHE.clear()
    # constraints / follicles made before this block (base rig, other blocks) are left alone
    old_constraints = set(cmds.ls(type='constraint'))
    old_follicles = set(cmds.ls(type='follicle'))
    old_matrix_nodes = set(cmds.ls(type=['multMatrix', 'decomposeMatrix']))
    keep_constraints = set()
    switch_shapes = []
    legs_data = []

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    children = cmds.listRelatives(block, c=True)
    guide = next((c for c in children if '_PV' not in c), None)
    aim_guide = next((c for c in children if '_PV' in c), None)

    new_guide = mt.duplicate_and_remove_guides(guide)
    print(new_guide)
    to_build = [new_guide]

    # compatible with older versions without AutoOrient
    if cmds.attributeQuery('AutoOrient', n=config, exists=True):
        auto_orient = cmds.getAttr(config + '.AutoOrient')
    else:
        auto_orient = True

    # orient the joints

    if auto_orient:
        mt.orient_joint(input=new_guide)
        _orient_chain_compat(new_guide)

    # force last joint to orient
    joint_four = cmds.listRelatives(new_guide, ad=True)[-3]
    cmds.setAttr("{}.jointOrientX".format(joint_four), 0)
    cmds.setAttr("{}.jointOrientY".format(joint_four), 0)
    cmds.setAttr("{}.jointOrientZ".format(joint_four), 0)

    #I have no idea why bt this doesnt work if we dont unparent and then parent them
    joint_one = new_guide
    joint_three = cmds.listRelatives(joint_four, p=True)[0]
    joint_two = cmds.listRelatives(joint_three, p=True)[0]
    cmds.parent(joint_four, w=True)
    cmds.parent(joint_three, w=True)
    cmds.parent(joint_two, w=True)
    cmds.parent(joint_two, new_guide)
    cmds.parent(joint_three, joint_two)
    cmds.parent(joint_four, joint_three)

    mirror_mode = cmds.getAttr('{}.Mirror'.format(config), asString=True)

    #prep work for right side ------------------------------------------------------

    #if mirror is set only to right we need to build on left for mirror behavior then putt it back to righ side
    if mirror_mode == 'Right_Only':
        miror_grp = mt.mirror_group(new_guide, world = True)
        cmds.makeIdentity(miror_grp, a=True, t=True, r=True, s=True)
        cmds.parent(new_guide, w = True)
        cmds.delete(miror_grp)
        if auto_orient:
            mt.orient_joint(input=new_guide)
            _orient_chain_compat(new_guide)

    elif mirror_mode == 'True':
        right_guide = mt.duplicate_change_names(input = new_guide, hi = True, search=nc['left'], replace =nc['right'])[0]
        to_build.append(right_guide)
        print (to_build)

    ctrl_size = cmds.getAttr('{}.CtrlSize'.format(config))
    twist_amount = int(cmds.getAttr('{}.TwistAmount'.format(config)))

    # compatible with older versions without DogMode
    if cmds.attributeQuery('DogMode', n=config, exists=True):
        dog_mode = cmds.getAttr(config + '.DogMode', asString=True)
    else:
        dog_mode = 'Back'

    # compatible with older versions without ForcePoleVectorDistance
    if cmds.attributeQuery('ForcePoleVectorDistance', n=config, exists=True):
        force_pv_distance = cmds.getAttr(config + '.ForcePoleVectorDistance', asString=True)
    else:
        force_pv_distance = 'Off'

    # compatible with older versions without ribbons
    if cmds.attributeQuery('CreateRibbons', n=config, exists=True):
        create_ribbons = cmds.getAttr(config + '.CreateRibbons')
    else:
        create_ribbons = True

    # BendyCurve: the Limb v002 bendy path (curve attrs, arcs), off: the same straight lines path with far less
    # nodes (faster playback)
    if cmds.attributeQuery('BendyCurve', n=config, exists=True):
        bendy_curve = cmds.getAttr(config + '.BendyCurve')
    else:
        bendy_curve = False

    # SoftIk: adds the SoftIk attr (0-10) to the leg attrs, the hip -> ankle ik eases to straight
    if cmds.attributeQuery('SoftIk', n=config, exists=True):
        use_soft_ik = cmds.getAttr(config + '.SoftIk')
    else:
        use_soft_ik = False

    # compatible with older versions without IkOrient
    if cmds.attributeQuery('IkOrient', n=config, exists=True):
        ik_orient = cmds.getAttr(config + '.IkOrient', asString=True)
    else:
        ik_orient = 'World'

    #build ------------------------------------------------------
    for side_guide in to_build:

        cmds.select(side_guide, hi=True)
        limb_a, limb_b, limb_c, limb_d = cmds.ls(sl=True)[:4]
        main_joints = [limb_a, limb_b, limb_c, limb_d]
        right = str(side_guide).startswith(nc['right'])

        #use this locator in case parent is set to new locator
        if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
            block_parent = cmds.spaceLocator( n = '{}'.format(str(side_guide).replace(nc['joint'],'_Parent' + nc['locator'])))[0]
        else:
            block_parent = cmds.getAttr('{}.SetParent'.format(config))
            if right:
                block_parent = block_parent.replace(nc['left'],nc['right'])

        # smart select the colors
        if str(side_guide).startswith(nc['left']):
            color = setup['left_color']
            sec_color = setup['left_secundary_color']
        elif right:
            color = setup['right_color']
            sec_color = setup['right_secundary_color']
        else:
            color = setup['main_color']
            sec_color = setup['main_color']

        # Leg global scale: one more level under the Global controller, scales the whole leg from the hip
        # (L_BkLeg_GlobalScale_Ctrl), what followed the Global scale follows this one
        side_prefix = str(side_guide).split('_')[0]
        token = str(limb_a).split('_')[1] if '_' in str(limb_a) else str(limb_a)
        limb_label = token.replace('Hip', '').replace('Shoulder', '') + 'Leg'
        limb_global_ctrl = mt.curve(input=limb_a, type='circleX', rename=True, custom_name=True,
                                    name='{}_{}_GlobalScale{}'.format(side_prefix, limb_label, nc['ctrl']),
                                    size=ctrl_size * 1.8)
        mt.assign_color(limb_global_ctrl, color)
        limb_global_root = mt.root_grp(input=limb_global_ctrl)[0]
        cmds.parent(limb_global_root, setup['base_groups']['control'] + nc['group'])
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

        #Create Blend Systems
        # duplicate chains to have the 3 of them
        ik_joints = mt.duplicate_change_names(input=side_guide, hi=True, search=nc['joint'], replace=nc['ik'])
        fk_joints = mt.duplicate_change_names(input=side_guide, hi=True, search=nc['joint'], replace=nc['fk'])
        cmds.select(cl=True)

        #Create FK System
        for jnt in fk_joints:
            cmds.select(jnt, add=True)

        fk_system = mt.fk_chain(size=ctrl_size, color=color, curve_type='bounding_cube', scale=False)
        print('FK = {}'.format(fk_system))


        #Ik System
        #Create 3 joints chain with correct distances
        cmds.select(cl=True)
        back_sys_joint_a = cmds.joint(n=ik_joints[0].replace(nc['joint'], 'Bk'+nc['joint']),
                                      p=[0,0,0])
        offset=1.5
        back_sys_joint_b = cmds.joint(n=ik_joints[1].replace(nc['joint'], 'Bk'+nc['joint']),
                                      p=[0,0,-1*offset*cmds.getAttr('{}.tx'.format(joint_two))])
        back_sys_joint_c = cmds.joint(n=ik_joints[3].replace(nc['joint'], 'Bk'+nc['joint']),
                                      p=[0,0,-1])
        cmds.setAttr('{}.rotateX'.format(back_sys_joint_b), -90)

        new_pos = cmds.getAttr('{}.tx'.format(joint_three))+cmds.getAttr('{}.tx'.format(joint_four))
        cmds.setAttr('{}.tx'.format(back_sys_joint_c), new_pos*-1)

        #Temp ik and placement
        temp_ik_data = cmds.ikHandle(sj=back_sys_joint_a, ee=back_sys_joint_c, sol='ikRPsolver')
        mt.match(this=back_sys_joint_a, that=ik_joints[0], r=False)
        mt.match(this=temp_ik_data[0], that=ik_joints[-1], r=False)

        temp_pv = cmds.poleVectorConstraint(ik_joints[0], temp_ik_data[0])

        #Check if twist needs backwards
        pos_ik = cmds.xform(ik_joints[0], q=True, t=True, ws=True)[2]
        pos_sys = cmds.xform(back_sys_joint_b, q=True, t=True, ws=True)[2]

        if dog_mode == 'Back':
            if pos_sys > pos_ik:
                cmds.setAttr('{}.twist'.format(temp_ik_data[0]), 180)
        else:
            if pos_sys < pos_ik:
                cmds.setAttr('{}.twist'.format(temp_ik_data[0]), 180)

        cmds.delete(temp_pv, temp_ik_data[1])

        #Create oficial system now
        backwards_ik = cmds.ikHandle(sj=back_sys_joint_a, ee=back_sys_joint_c,
                                     sol='ikRPsolver',
                                     n=ik_joints[-1].replace(nc['joint'], nc['ik_rp']))

        # pv_loc placed at mathematically correct pole vector position for the quad chain
        pv_loc = mt.pole_vector_placement(bone_one=[ik_joints[0]],
                                          bone_two=[ik_joints[1]],
                                          bone_three=[ik_joints[2]],
                                          back_distance=2)

        if force_pv_distance == 'Positive_1_5':
            cmds.setAttr('{}.tz'.format(pv_loc), 1.5)
        elif force_pv_distance != 'Off':
            leg_distance = mt.get_distance_between(ik_joints[0], ik_joints[1]) + mt.get_distance_between(ik_joints[1], ik_joints[2])
            pv_distance_scale = {
                'Leg_Distance': 1.0,
                'Half_Leg_Distance': 0.5,
                'Third_Leg_Distance': 1.0 / 3.0,
                'Double_Leg_Distance': 2.0,
            }[force_pv_distance]
            pv_magnitude = leg_distance * pv_distance_scale
            # Front pushes the loc to Z+, Back pushes it to Z- to keep the IK pole vector stable
            pv_signed_z = pv_magnitude if dog_mode == 'Front' else pv_magnitude * -1
            cmds.setAttr('{}.tz'.format(pv_loc), pv_signed_z)

        # v002: pole vector on the leg plane, knee side (v001 kept it off the plane for legs away from Z 0, the
        # back legs knee popped sideways at rest)
        pole_on_leg_plane(pv_loc, ik_joints[0], ik_joints[1], ik_joints[2])

        cmds.poleVectorConstraint(pv_loc, backwards_ik[0])

        pos_ik = cmds.xform(ik_joints[0], q=True, t=True, ws=True)[2]
        pos_sys = cmds.xform(back_sys_joint_b, q=True, t=True, ws=True)[2]
        if dog_mode == 'Back':
            if pos_sys > pos_ik:
                cmds.setAttr('{}.twist'.format(backwards_ik[0]), 180)
        else:
            if pos_sys < pos_ik:
                cmds.setAttr('{}.twist'.format(backwards_ik[0]), 180)

        backwards_ik = backwards_ik[0]

        #Create Controllers
        #Main IK
        main_ik_ctrl = mt.curve(input='',
                        type='cube',
                        rename=True,
                        custom_name=True,
                        name=ik_joints[-1].replace(nc['joint'], nc['ctrl']),
                        size=ctrl_size)

        cmds.rotate(0, 0, 0)
        mt.assign_color(color=color)
        main_ik_ctrl_root_grp = mt.root_grp()[0]
        cmds.delete(cmds.pointConstraint(ik_joints[-1], main_ik_ctrl_root_grp))
        # Mirror of ForceIkWorld logic from exec_limb.py
        if ik_orient == 'World':
            cmds.setAttr('{}.rotateX'.format(main_ik_ctrl_root_grp), 0)
            cmds.setAttr('{}.rotateY'.format(main_ik_ctrl_root_grp), 0)
            cmds.setAttr('{}.rotateZ'.format(main_ik_ctrl_root_grp), 0)
        else:  # FootY - aim -Z toward ankle so Z stays forward, giving correct Y rotation
            cmds.delete(cmds.aimConstraint(ik_joints[-2], main_ik_ctrl_root_grp,
                                           aimVector=(0, 0, -1), upVector=(0, 1, 0),
                                           worldUpType='vector', mo=False))
            cmds.setAttr('{}.rotateX'.format(main_ik_ctrl_root_grp), 0)
            cmds.setAttr('{}.rotateZ'.format(main_ik_ctrl_root_grp), 0)
        mt.hide_attr(main_ik_ctrl, t=False, r=False, s=True, rotate_order=False)

        #Ik Sub
        sub_ik_ctrl = mt.curve(input=ik_joints[-1],
                        type='cube',
                        rename=True,
                        custom_name=True,
                        name=ik_joints[-1].replace(nc['joint'],'_Sub'+nc['ctrl']),
                        size=ctrl_size*0.75)

        mt.assign_color(color=color)
        sub_ik_ctrl_root_grp = mt.root_grp()[0]
        mt.match(sub_ik_ctrl_root_grp, ik_joints[-1], r=True, t=True)
        mt.hide_attr(sub_ik_ctrl, t=False, r=False, s=True, rotate_order=False)

        #Ball Ctrl
        ball_ctrl = mt.curve(input=ik_joints[-1],
                        type='sphere',
                        rename=True,
                        custom_name=True,
                        name=ik_joints[-1].replace(nc['joint'],'_Ball'+nc['ctrl']),
                        size=ctrl_size*0.75)

        mt.assign_color(color=color)
        ball_ctrl_root_grp, ball_ctrl_auto_grp = mt.root_grp(autoRoot=True)
        mt.match(ball_ctrl_root_grp, ik_joints[-1], r=True, t=True)
        mt.hide_attr(ball_ctrl, t=True, r=False, s=True, rotate_order=False)

        #Top Ctrl
        top_ctrl = mt.curve(input=ik_joints[0],
                        type='pin_cube',
                        rename=True,
                        custom_name=True,
                        name=ik_joints[0].replace(nc['joint'], nc['ctrl']),
                        size=ctrl_size)

        mt.assign_color(color=color)
        top_ctrl_root_grp = mt.root_grp()[0]
        mt.match(top_ctrl_root_grp, ik_joints[0], r=True, t=True)
        mt.hide_attr(top_ctrl, t=False, r=True, s=True, rotate_order=False)

        #PV Ctrl
        pv_ctrl = mt.curve(input=aim_guide,
                            type='sphere',
                            rename=True,
                            custom_name=True,
                            name=ik_joints[1].replace(nc['joint'], 'PV'+nc['ctrl']),
                            size=ctrl_size)

        mt.assign_color(color=color)
        pv_ctrl_root_grp = mt.root_grp()[0]
        mt.match(pv_ctrl_root_grp, aim_guide, r=True, t=True)
        mt.hide_attr(pv_ctrl, t=False, r=True, s=True, rotate_order=True)


        #Hierarchy
        cmds.parent(sub_ik_ctrl_root_grp, main_ik_ctrl)
        cmds.parent(ball_ctrl_root_grp, sub_ik_ctrl)
        cmds.parentConstraint(pv_ctrl, pv_loc, mo=True)
        cmds.parentConstraint(top_ctrl, back_sys_joint_a, mo=True)
        cmds.parentConstraint(top_ctrl, ik_joints[0], mo=True)
        cmds.orientConstraint(sub_ik_ctrl, ik_joints[-1], mo=True)

        cmds.parent(backwards_ik, main_ik_ctrl)

        #Finish main ik system
        cmds.orientConstraint(back_sys_joint_b, ball_ctrl_auto_grp, mo=True)

        first_to_third_ik = cmds.ikHandle(sj=ik_joints[0], ee=ik_joints[2],
                                     sol='ikRPsolver',
                                     n=ik_joints[2].replace(nc['joint'], '_Up' + nc['ik_rp']))

        third_to_fourth_ik = cmds.ikHandle(sj=ik_joints[2], ee=ik_joints[3],
                                     sol='ikSCsolver',
                                     n=ik_joints[3].replace(nc['joint'], '_Dw' + nc['ik_rp']))

        cmds.parentConstraint(ball_ctrl, third_to_fourth_ik[0], mo=True)

        cmds.poleVectorConstraint(pv_loc, first_to_third_ik[0])

        #Stretchy Fix: Creating offset group for the IKRP to have it snap to ball control when stretched.
        stretch_ik_offset_grp = mt.root_grp(input=first_to_third_ik[0])
        cmds.parentConstraint(ball_ctrl, stretch_ik_offset_grp[0], mo=True)
        # v002: the handle follows a SoftIk group under the offset group (the soft ik moves it back to the hip)
        soft_ik_grp = cmds.group(em=True, n=first_to_third_ik[0].replace(nc['ik_rp'], '_SoftIk' + nc['group']))
        cmds.parent(soft_ik_grp, stretch_ik_offset_grp[0], r=True)
        stretch_ik_parentConstr = cmds.parentConstraint(ball_ctrl, soft_ik_grp, first_to_third_ik[0], mo=False)[0]
        cmds.setAttr("{}.{}W0".format(stretch_ik_parentConstr, ball_ctrl), 0)


        # v002: keep the twist that puts the knee where the guide has it (v001 guessed from the world Z)
        guide_knee = om.MVector(cmds.xform(fk_joints[1], q=True, t=True, ws=True))
        errors = []
        for twist in (0, 180):
            cmds.setAttr('{}.twist'.format(first_to_third_ik[0]), twist)
            errors.append((om.MVector(cmds.xform(ik_joints[1], q=True, t=True, ws=True)) - guide_knee).length())
        cmds.setAttr('{}.twist'.format(first_to_third_ik[0]), 0 if errors[0] <= errors[1] else 180)
        if min(errors) > 1e-2:
            cmds.warning('QuadLimb: {} IK knee is {:.3f} away from the guide at rest'.format(ik_joints[1], min(errors)))

        line = mt.connect_with_line(pv_ctrl, ik_joints[1])

        #Create ik fk system and switch
        ik_ctrls = [main_ik_ctrl, sub_ik_ctrl, ball_ctrl, top_ctrl, pv_ctrl]
        ik_fk_controllers = fk_system + ik_ctrls

        for ctrl in ik_fk_controllers:
            cmds.select(ctrl)
            if cmds.objectType(ctrl) == 'transform':
                switch_attr = mt.shape_with_attr(input='', obj_name='{}_Switch'.format(main_joints[0]),
                                                   attr_name='Switch_IK_FK')

        for num, jnt in enumerate(main_joints):
            mt.switch_blend_colors(this=fk_joints[num], that=ik_joints[num], main=jnt, attr=switch_attr)

        # IK extra attrs
        attrs_loc = switch_attr.split('.')[0]
        switch_shapes.append(attrs_loc)
        mt.line_attr(input=attrs_loc, name='IK')

        show_top_ctrl_attr = mt.new_enum(input=attrs_loc, name='TopIk', enums='Hide:Show', keyable=False)
        cmds.connectAttr(show_top_ctrl_attr, cmds.listRelatives(top_ctrl, s=True)[0] + '.v')
        # This is used in the build block for the limb
        show_gimbal = mt.new_enum(input=attrs_loc, name='SubIk', enums='Hide:Show', keyable=False)
        cmds.connectAttr(show_gimbal, cmds.listRelatives(sub_ik_ctrl, s=True)[0] + '.v')

        #Stretchy IK
        first_pos = cmds.xform(ik_joints[0], q=True, t=True, ws=True)
        end_pos = cmds.xform(ik_joints[-1], q=True, t=True, ws=True)

        distance = cmds.distanceDimension(sp=first_pos, ep=end_pos)
        distance = cmds.rename(distance, ik_joints[-1] + '_' + ik_joints[0] + nc['distance'] + '_Shape')

        cmds.rename(cmds.listRelatives(distance, p=True), ik_joints[-1] + '_' + ik_joints[0] + nc['distance'])
        cmds.setAttr('{}.visibility'.format(distance), 0)

        # world positions read without the controllers own scale (scaling a controller never stretches the leg)
        decompose1 = cmds.createNode('decomposeMatrix', name=ik_joints[0]+'_decomposeMatrix_joint')
        decompose2 = cmds.createNode('decomposeMatrix', name=ik_joints[-1]+'_decomposeMatrix_joint')

        cmds.connectAttr(top_ctrl + '.worldMatrix', decompose1 + '.inputMatrix', f=True)
        cmds.connectAttr(main_ik_ctrl + '.worldMatrix', decompose2 + '.inputMatrix', f=True)

        cmds.connectAttr(decompose1+'.outputTranslate ', distance + '.startPoint', f=True)
        cmds.connectAttr(decompose2+'.outputTranslate ', distance + '.endPoint', f=True)

        #Stretchy fix: Determine correct max length of leg when fully stretched before adding stretchy.
        total_distance = 0

        for num in range(1, 4):
            distance_node = cmds.distanceDimension(sp=cmds.xform(ik_joints[num - 1], q=True, t=True, ws=True),
                                                   ep=cmds.xform(ik_joints[num], q=True, t=True, ws=True))
            length_of_segment = cmds.getAttr("{}.distance".format(distance_node))
            total_distance = total_distance + length_of_segment
            cmds.delete(cmds.listRelatives(distance_node, parent=True))

        mt.line_attr(input=attrs_loc, name='IK')
        stretch_attr = mt.new_attr(input=attrs_loc, name='Stretch_On', min=0, max=1,
                                     default=int(setup['stretch_default']))

        normalize_loc = cmds.spaceLocator(n=ik_joints[0] + '_NormalScale' + nc['locator'])[0]

        # v002: the leg scale (GlobalScale ctrl, it has the Global scale too) normalizes the stretch
        cmds.connectAttr(limb_scale, normalize_loc + '.scale')

        # IK Stretchy Nodes and Connections from RdM2
        contidion_node = cmds.shadingNode('condition', asUtility=True, n=attrs_loc + nc['condition'])
        cmds.setAttr(str(contidion_node) + ".operation", 2)
        cmds.setAttr(str(contidion_node) + '.secondTerm', total_distance)

        # Connect To Distance
        md0 = mt.connect_md_node(in_x1=str(distance) + '.distance', in_x2=total_distance,
                                   out_x=str(contidion_node) + '.colorIfTrueR', mode='divide', name='')

        md3 = mt.connect_md_node(in_x1=str(distance) + '.distance', in_x2=stretch_attr,
                           out_x=str(contidion_node) + '.firstTerm', mode='mult',
                           name='{}_TotalDistance'.format(attrs_loc))

        for jnt in ik_joints[:-1]:
            cmds.connectAttr(contidion_node+'.outColorR', jnt+'.scaleX')

        normal_md = mt.connect_md_node(in_x1=str(distance) + '.distance', in_x2=str(normalize_loc) + '.scaleX',
                                         out_x=md0 + '.input1X', mode='divide', name='{}_Normalize'.format(distance),
                                         force=True)

        cmds.connectAttr(str(normalize_loc) + '.scaleX', normal_md + '.input2Y')
        cmds.connectAttr(str(normalize_loc) + '.scaleX', normal_md + '.input2Z')

        cmds.connectAttr(normal_md + '.outputX', md3 + '.input1X', f=True)

        #Stretchy fix: Connecting stretchy condition node to remap and reverse to control
        #the IKRP's parent constraint's parent influences.
        stretchy_IKRP_snap_remap = cmds.shadingNode("remapValue", au=True,
                                                    name="{}_StretchySnapFix_Remap".format(attrs_loc))
        cmds.setAttr("{}.inputMin".format(stretchy_IKRP_snap_remap), 1)
        cmds.setAttr("{}.inputMax".format(stretchy_IKRP_snap_remap), 1.05)
        cmds.setAttr("{}.outputMin".format(stretchy_IKRP_snap_remap), 0)
        cmds.setAttr("{}.outputMax".format(stretchy_IKRP_snap_remap), 1)

        cmds.connectAttr("{}.colorIfTrue.colorIfTrueR".format(contidion_node),
                         "{}.inputValue".format(stretchy_IKRP_snap_remap))

        stretchy_IKRP_snap_reverse = cmds.shadingNode("reverse", au=True,
                                                      name="{}_Reverse".format(stretchy_IKRP_snap_remap))
        # v002: the snap only with Stretch_On (v001 also snapped with no stretch: the knee popped straight at full
        # reach, the hip -> ankle target jumped from the ankle to the ball)
        snap = cmds.createNode('multDoubleLinear', n=stretchy_IKRP_snap_remap + '_StretchOn_MultDoubleLinear')
        cmds.connectAttr("{}.outValue".format(stretchy_IKRP_snap_remap), snap + '.input1')
        cmds.connectAttr(stretch_attr, snap + '.input2')
        cmds.connectAttr(snap + '.output', "{}.input.inputX".format(stretchy_IKRP_snap_reverse))

        cmds.connectAttr(snap + '.output', "{}.{}W0".format(stretch_ik_parentConstr,ball_ctrl))
        cmds.connectAttr("{}.output.outputX".format(stretchy_IKRP_snap_reverse),
                         "{}.{}W1".format(stretch_ik_parentConstr, soft_ik_grp))

        # v002: stretch and soft ik on the hip -> ankle chain (the knee chain is what straightens, v001 measured hip ->
        # ball: the leg stopped short of the controller, then the snap popped it), no snap needed anymore
        for attr in ['{}.{}W0'.format(stretch_ik_parentConstr, ball_ctrl), '{}.{}W1'.format(stretch_ik_parentConstr, soft_ik_grp)]:
            for plug in cmds.listConnections(attr, s=True, d=False, p=True) or []:
                cmds.disconnectAttr(plug, attr)
        cmds.setAttr('{}.{}W0'.format(stretch_ik_parentConstr, ball_ctrl), 0)
        cmds.setAttr('{}.{}W1'.format(stretch_ik_parentConstr, soft_ik_grp), 1)
        soft_attr = mt.new_attr(input=attrs_loc, name='SoftIk', min=0, max=10, default=0) if use_soft_ik else 0
        soft_stretch_ik(limb, first_to_third_ik[0].replace(nc['ik_rp'], '_SoftIk'), soft_ik_grp, decompose1 + '.outputTranslate',
                        soft_attr, stretch_attr, [abs(cmds.getAttr(j + '.translateX')) for j in ik_joints[1:3]],
                        limb_scale_node + '.outputScaleX', ik_joints[:2], ik_joints[2], contidion_node)

        #Vis
        cmds.connectAttr(switch_attr, '{}.visibility'.format(cmds.listRelatives(fk_system[0], p=True)[0]))

        reverse_node = cmds.shadingNode('reverse', asUtility=True)
        cmds.connectAttr(switch_attr, '{}.input.inputX'.format(reverse_node))

        cmds.connectAttr('{}.output.outputX'.format(reverse_node),
                         '{}.visibility'.format(main_ik_ctrl_root_grp), f=True)
        cmds.connectAttr('{}.output.outputX'.format(reverse_node),
                         '{}.visibility'.format(pv_ctrl_root_grp), f=True)
        cmds.connectAttr('{}.output.outputX'.format(reverse_node),
                         '{}.visibility'.format(top_ctrl_root_grp), f=True)
        cmds.connectAttr('{}.output.outputX'.format(reverse_node),
                         cmds.listRelatives(line[0], s=True)[0] + '.v', f=True)

        cmds.parent(line[0], main_ik_ctrl_root_grp)

        #Add the twist
        upper_upper_twist = mt.spline_twist(start=main_joints[0], end=main_joints[1], axis=setup['twist_axis'],
                                        amount=twist_amount, mode='up')
        upper_twist = mt.spline_twist(start=main_joints[1], end=main_joints[2], axis=setup['twist_axis'],
                                        amount=twist_amount, mode='up')
        lower_twist = mt.spline_twist(start=main_joints[2], end=main_joints[3], axis=setup['twist_axis'],
                                        amount=twist_amount, mode='down')
        twists = [upper_upper_twist, upper_twist, lower_twist]

        for num, twist in enumerate(twists):
            for jnt in twist['joints']:
                cmds.connectAttr('{}.scale'.format(main_joints[num]), '{}.scale'.format(jnt))

        #Order and clean
        clean_ctrl_grp = cmds.group(em=True, name=side_guide + nc['ctrl'] + nc['group'])
        clean_rig_grp = cmds.group(em=True, name=side_guide + '_Rig' + nc['group'])
        clean_ribbons_grp = cmds.group(em=True, name=side_guide + '_RigRibbons' + nc['group'])
        clean_main_system_grp = cmds.group(em=True, name=side_guide + '_RigSystem' + nc['group'])

        ribbons = []
        mid_ctrls = []
        curve_attrs = None
        if create_ribbons:
            mt.line_attr(input=attrs_loc, name='Bendy_Vis')
            ribbon_first_vis_attr = mt.new_enum(input=attrs_loc, name='BendyMain', enums='Hide:Show', keyable=False)
            vis_attrs = [mt.new_enum(input=attrs_loc, name=n, enums='Hide:Show', keyable=False)
                         for n in ('BendyOffsets', 'BendyEnds', 'BendyTweeks')]
            cmds.setAttr(ribbon_first_vis_attr, 1)

            curve_attr_names = []
        if create_ribbons and bendy_curve:
            # Bendy curve attrs (Limb v002): BendyCurve 0 straight lines through the mid bendy controllers,
            # 10 arcs, AutoCurve adds curve the more the knee / ankle bend, Upper/Mid/LowerCurve per segment
            # (negative bows the other way), Hip/BallEase keep the leg leaving the hip / ball straight
            mt.line_attr(input=attrs_loc, name='BendyCurve')
            curve_attrs = {
                'curve': mt.new_attr(input=attrs_loc, name='BendyCurve', min=0, max=10, default=0),
                'auto': mt.new_attr(input=attrs_loc, name='AutoCurve', min=0, max=10, default=0),
                'upper': mt.new_attr(input=attrs_loc, name='UpperCurve', min=-10, max=10, default=0),
                'mid': mt.new_attr(input=attrs_loc, name='MidCurve', min=-10, max=10, default=0),
                'lower': mt.new_attr(input=attrs_loc, name='LowerCurve', min=-10, max=10, default=0),
                'start_ease': mt.new_attr(input=attrs_loc, name='HipEase', min=0, max=10, default=0),
                'end_ease': mt.new_attr(input=attrs_loc, name='BallEase', min=0, max=10, default=0)}
            curve_attr_names = [plug.split('.')[-1] for plug in curve_attrs.values()]

        if create_ribbons:
            for num, twist in enumerate(twists):
                ribbons.append(create_mid_ribbons(main_joints[num], main_joints[num], main_joints[num + 1],
                                                  twist['joints'], twist_amount, ctrl_size, sec_color, attrs_loc,
                                                  vis_attrs, limb_scale))
            top_top_ribbon, top_ribbon, low_ribbon = ribbons

            # mid bendy controllers on the knee and the ankle
            for num, (jnt, before, after) in enumerate([(limb_b, top_top_ribbon, top_ribbon),
                                                        (limb_c, top_ribbon, low_ribbon)]):
                mid_ctrl = mt.curve(input=jnt, type='cubePlus', rename=True, custom_name=True,
                                    name=jnt.replace(nc['joint'], 'Mid_Bendy' + nc['ctrl']), size=ctrl_size / 2)
                mt.assign_color(mid_ctrl, sec_color)
                root_mid_ctrl = mt.root_grp(input=mid_ctrl)
                mt.shape_with_attr(input=mid_ctrl, obj_name=main_joints[0] + '_Switch', attr_name='')
                mt.match(root_mid_ctrl, jnt, r=True, t=True)
                cmds.parentConstraint(jnt, root_mid_ctrl, mo=True)
                cmds.pointConstraint(mid_ctrl, cmds.listRelatives(before['second_ctrls'][1], p=True), mo=True)
                cmds.pointConstraint(mid_ctrl, cmds.listRelatives(after['second_ctrls'][0], p=True), mo=True)
                cmds.connectAttr(ribbon_first_vis_attr, '{}.v'.format(cmds.listRelatives(mid_ctrl, shapes=True)[0]))
                cmds.parent(root_mid_ctrl, clean_ctrl_grp)
                mid_ctrls.append(mid_ctrl)

            for ribbon in ribbons:
                cmds.parent(ribbon['ribbon_plane'], ribbon['clean_rig_grp'], ribbon['fol_ribbon_grp'], clean_ribbons_grp)

        cmds.parent(distance, normalize_loc, clean_rig_grp)
        cmds.parent(clean_ribbons_grp, clean_rig_grp)
        cmds.parent(clean_main_system_grp, clean_rig_grp)

        cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
        cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])

        cmds.parent(main_ik_ctrl_root_grp,pv_ctrl_root_grp, top_ctrl_root_grp, cmds.listRelatives(fk_system, p=True)[0],
                    clean_ctrl_grp)

        main_joints_grp = cmds.group(em=True, name=side_guide + '_MainJoints' + nc['group'])
        cmds.parent(main_joints[0], ik_joints[0], fk_joints[0], main_joints_grp)

        cmds.parent(main_joints_grp, stretch_ik_offset_grp[0], third_to_fourth_ik[0],
                    back_sys_joint_a, pv_loc,
                    clean_main_system_grp)

        for twist in twists:
            cmds.parent(twist['twist_grp'], clean_ribbons_grp)

        to_bind = []
        if create_ribbons:
            for ribbon in ribbons:
                to_bind += ribbon['fol_joints']
        else:
            for twist in twists:
                to_bind += twist['joints']

        #Mirror
        #Parent Systems to parent Loc
        top_ctrl_grp = clean_ctrl_grp
        if mirror_mode == 'Right_Only' or (mirror_mode == 'True' and right):
            top_ctrl_grp = mt.mirror_group(clean_ctrl_grp, world=True)
            mirror_rig_grp = mt.mirror_group(clean_rig_grp, world=True)
            cmds.parent(mirror_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
            cmds.parent(top_ctrl_grp, setup['base_groups']['control'] + nc['group'])

        cmds.parentConstraint(block_parent, top_ctrl_root_grp, mo=True)
        cmds.parentConstraint(block_parent, main_joints_grp, mo=True)
        cmds.parentConstraint(block_parent, cmds.listRelatives(fk_system, p=True)[0], mo=True)
        # the leg joints scale with the leg scale controller, kept as a constraint: the Foot v002 block finds
        # the GlobalScale controller from it
        keep_constraints.add(cmds.scaleConstraint(limb_global_ctrl, clean_main_system_grp, mo=True)[0])

        # Fix issue with orient in the aims up vectors
        if create_ribbons:
            for ribbon in ribbons:
                cmds.parent(ribbon['ribbon_ctrl_grp'], clean_ctrl_grp)
            handle_grp = cmds.group([r for ribbon in ribbons for r in ribbon['handle_controllers_roots']],
                                    n=limb_a + '_Handle' + nc['ctrl'] + nc['group'])
            if right:
                cmds.setAttr('{}.rotateX'.format(handle_grp), 180)
                cmds.setAttr('{}.scaleX'.format(handle_grp), -1)
                cmds.setAttr('{}.scaleY'.format(handle_grp), -1)
                cmds.setAttr('{}.scaleZ'.format(handle_grp), -1)

        #Fix bad behaivior
        cmds.parent(clean_ribbons_grp, w=True)
        cmds.setAttr('{}.rx'.format(clean_ribbons_grp), 0)
        cmds.setAttr('{}.ry'.format(clean_ribbons_grp), 0)
        cmds.setAttr('{}.rz'.format(clean_ribbons_grp), 0)
        cmds.setAttr('{}.sx'.format(clean_ribbons_grp), 1)
        cmds.setAttr('{}.sy'.format(clean_ribbons_grp), 1)
        cmds.setAttr('{}.sz'.format(clean_ribbons_grp), 1)
        cmds.parent(clean_ribbons_grp, clean_rig_grp)

        for twist in twists:
            cmds.scaleConstraint(limb_global_ctrl, twist['twist_grp'], mo=True)

        # create bind Joints for the skin -------------------------
        bind_joints = []
        bind_joint = ''

        cmds.select(cl=True)
        bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])

        for jnt in to_bind:
            try:
                cmds.select(bind_joint)
            except:
                pass
            bind_joint = cmds.joint(n=jnt.replace(nc['joint'], nc['joint_bind']))
            cmds.delete(cmds.parentConstraint(jnt, bind_joint, mo=False))
            cmds.delete(cmds.scaleConstraint(jnt, bind_joint, mo=False))
            cmds.makeIdentity(a=True, t=True, s=True, r=True)
            cmds.parentConstraint(jnt, bind_joint, mo=False)
            cmds.scaleConstraint(jnt, bind_joint, mo=True)
            cmds.setAttr('{}.segmentScaleCompensate'.format(bind_joint), 0)
            cmds.setAttr('{}.inheritsTransform'.format(bind_joint), 0)
            bind_joints.append(bind_joint)
            cmds.setAttr('{}.radius'.format(bind_joint), 2)

        if cmds.objExists(bind_jnt_grp):
            cmds.parent(bind_joints[0], bind_jnt_grp)

        #Hot fix right side (the down twist reader is built on the left)
        if right:
            fix_group = lower_twist['twist_grp_to_mirror']
            parent = cmds.listRelatives(fix_group, p=True)[0]
            mirror_fix_grp = mt.mirror_group(fix_group)
            cmds.parent(mirror_fix_grp, parent)

        # Bendy attrs proxied on the mid bendy controllers
        if create_ribbons:
            for mid_ctrl in mid_ctrls:
                mt.proxy_this_attrs(attrs_from=attrs_loc, attrs_to=mid_ctrl,
                                    attrs_to_proxy=['BendyMain', 'BendyOffsets', 'BendyEnds', 'BendyTweeks'] + curve_attr_names)

        # the right side is built on the left and flipped, the global scale controller is placed now on the
        # final hip, it follows the block parent, the rig scale comes from the Global
        cmds.delete(cmds.parentConstraint(main_joints[0], limb_global_root, mo=False))
        cmds.parentConstraint(block_parent, limb_global_root, mo=True)
        cmds.scaleConstraint('Rig_Ctrl_Grp', limb_global_root, mo=True)
        # controllers keep following the rig, they only get scaled around the scale controller
        limb.scale_around(top_ctrl_grp, 'Rig_Ctrl_Grp', limb_global_ctrl)

        segment_binds = []
        start = 0
        for twist, ribbon in zip(twists, ribbons or [None] * 3):
            count = len(ribbon['fol_joints'] if ribbon else twist['joints'])
            segment_binds.append(bind_joints[start:start + count])
            start += count

        legs_data.append({'main_joints': main_joints, 'fk_ctrls': fk_system, 'ik_ctrl': main_ik_ctrl,
                          'sub_ik_ctrl': sub_ik_ctrl, 'top_ik_ctrl': top_ctrl, 'switch': switch_attr,
                          'segment_binds': segment_binds, 'ribbons': ribbons, 'mid_ctrls': mid_ctrls,
                          'curve_attrs': curve_attrs, 'twists': twists})

    # bendy path: straight or arcs through hip -> knee / ankle mid bendy controllers -> ball, no wobble
    for data in legs_data:
        if data['ribbons'] and data['curve_attrs']:
            build_bendy_paths(limb, data)
        elif data['ribbons']:
            build_lean_paths(limb, data)

    # controllers scale: fk controllers in fk, ik controllers in ik, bendy controllers fade along their segment
    scaled_ctrls = []
    for data in legs_data:
        fk_on = data['switch']
        ik_on = cmds.createNode('reverse', n=data['fk_ctrls'][0] + '_ScaleIk_Reverse')
        cmds.connectAttr(fk_on, ik_on + '.inputX')
        ik_on += '.outputX'

        influences = {}
        for seg, binds in enumerate(data['segment_binds']):
            for num, jnt in enumerate(binds):
                t = float(num) / (len(binds) - 1) if len(binds) > 1 else 1.0
                # fk is a normal hierarchy: the hip scales the whole leg, the knee from the knee down...
                items = [(fk_ctrl, fk_on) for fk_ctrl in data['fk_ctrls'][:seg + 1]]
                if seg == 0:
                    items.append((data['top_ik_ctrl'], ik_on))
                if data['ribbons']:
                    start_ctrl, end_ctrl = data['ribbons'][seg]['second_ctrls']
                    if 1 - t > 1e-4:
                        items.append((start_ctrl, 1 - t))
                    if t > 1e-4:
                        items.append((end_ctrl, t))
                    # mid bendy controllers: 1 on the knee / ankle, fading to the next joint
                    for mid_num, mid_ctrl in enumerate(data['mid_ctrls']):
                        weight = t if seg == mid_num else (1 - t if seg == mid_num + 1 else 0)
                        if weight > 1e-3:
                            items.append((mid_ctrl, weight))
                    items.append((data['ribbons'][seg]['ribbon_ctrls'][num], 1.0))
                influences[jnt] = items

        # ball controllers do not scale the leg, only the ball joint (the foot scales with it)
        ball = data['main_joints'][3]
        influences[ball] = [(ctrl, fk_on) for ctrl in data['fk_ctrls']] + \
                           [(ctrl, ik_on) for ctrl in [data['ik_ctrl'], data['sub_ik_ctrl']]]
        data['scale_influences'] = influences

        ctrls = data['fk_ctrls'] + [data['ik_ctrl'], data['sub_ik_ctrl'], data['top_ik_ctrl']] + data['mid_ctrls']
        for ribbon in data['ribbons']:
            ctrls += ribbon['second_ctrls'] + ribbon['ribbon_ctrls']
        # fk hip / knee / ankle scale is inherited by the fk controllers under them (the leg gets longer)
        limb.free_controller_scale(ctrls, inherit_scale=data['fk_ctrls'][:3])
        # the ik handle under the ik controller (the Foot block moves it to the foot) keeps no scale offset
        for handle in cmds.listRelatives(data['ik_ctrl'], c=True, type='ikHandle') or []:
            for plug in cmds.listConnections(handle + '.offsetParentMatrix', s=True, d=False, p=True) or []:
                cmds.disconnectAttr(plug, handle + '.offsetParentMatrix')
        scaled_ctrls += ctrls

    # follicles keep the leg out of parallel evaluation, swap them for uvPins
    limb.follicles_to_uv_pins([f for f in cmds.ls(type='follicle') if f not in old_follicles])

    # swap the constraints of this block for matrix nodes (faster playback)
    new_constraints = [c for c in cmds.ls(type='constraint') if c not in old_constraints and c not in keep_constraints]
    kept = limb.constraints_to_matrix(new_constraints, unscaled_targets=set(scaled_ctrls))
    replaced = len([c for c in new_constraints if not cmds.objExists(c)])
    print('QuadLimb matrix swap: {} constraints replaced, {} kept {}'.format(replaced, len(kept), kept))

    # bind joints get the controllers scale (after the swap, it multiplies into their scale channels)
    for data in legs_data:
        twist_follow_length([(data['main_joints'][n], data['main_joints'][n + 1], data['twists'][n]['joints'])
                             for n in range(3)], setup['twist_axis'].upper(), ribbons=bool(data['ribbons']))
        binds = [j for seg in data['segment_binds'] for j in seg]
        limb.scale_bind_joints(binds + [data['main_joints'][3]], data['scale_influences'])

    # break the switch shape cycle so the leg evaluates in parallel
    for switch_shape in switch_shapes:
        limb.switch_attrs_to_data_node(switch_shape)

    # and the matrix drivers reading their own node
    new_matrix_nodes = set(cmds.ls(type=['multMatrix', 'decomposeMatrix'])) - old_matrix_nodes
    print('QuadLimb: {} self cycles removed'.format(break_self_cycles(new_matrix_nodes)))

    print('Build {} Success'.format(block))
