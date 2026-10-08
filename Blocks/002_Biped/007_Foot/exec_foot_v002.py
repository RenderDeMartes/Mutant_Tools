from __future__ import absolute_import
from maya import cmds
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
PYBLOCK_NAME = 'exec_foot'

#---------------------------------------------

#---------------------------------------------

def create_foot_block(name = 'Foot'):

    nc, curve_data, setup = mt.import_configs()

    # Read name conventions as nc[''] and setup as seup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-3]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '007_Foot.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name = name, icon = 'Foot',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]

    ankle = mt.create_joint_guide(name = name + '_Ankle')
    #cmds.setAttr('{}.Helper'.format(ankle), 0)
    cmds.move(2,1.5,-1.5)

    ball = mt.create_joint_guide(name = name + '_Ball')
    cmds.setAttr('{}.Helper'.format(ball), 0)
    cmds.move(2,0.5,0)

    ball_floor = mt.create_joint_guide(name = name + '_BallFloor')
    cmds.setAttr('{}.Helper'.format(ball_floor), 0)
    cmds.move(2,0,0)

    in_floor = mt.create_joint_guide(name = name + '_In')
    cmds.setAttr('{}.Helper'.format(in_floor), 0)
    cmds.move(1,0,0)

    out_floor = mt.create_joint_guide(name = name + '_Out')
    cmds.setAttr('{}.Helper'.format(out_floor), 0)
    cmds.move(3,0,0)

    toes = mt.create_joint_guide(name = name + '_Toes')
    cmds.setAttr('{}.Helper'.format(toes), 0)
    cmds.move(2,0,1.5)

    heel_mid = mt.create_joint_guide(name = name + '_HeelMid')
    cmds.setAttr('{}.Helper'.format(heel_mid), 0)
    cmds.move(2,0,-1.5)

    heel = mt.create_joint_guide(name = name + '_Heel')
    cmds.setAttr('{}.Helper'.format(heel), 0)
    cmds.move(2,0,-2)


    cmds.parent(heel, ankle)
    cmds.parent(toes, ball)
    cmds.parent(ball_floor, ball)
    cmds.parent(in_floor, ball_floor)
    cmds.parent(out_floor, ball_floor)
    cmds.parent(ball, ankle)
    cmds.parent(heel_mid, ankle)
    cmds.parent(ankle, block)

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_foot_block()

#-------------------------
# Limb v002 swaps its constraints for matrix nodes (named <constraint>_*), deleting the parentConstraint
# is not enough there: the IK handle and the stretch locator keep following the IK ctrl, not the RFL.

def remove_matrix_driver(node):
    """Delete the matrix nodes a Limb v002 constraint swap left driving node translate / rotate."""
    prefixes = set()
    for attr in ['translate', 'rotate']:
        for axis in 'XYZ':
            for source in cmds.listConnections('{}.{}{}'.format(node, attr, axis), s=True, d=False) or []:
                for suffix in ('_Translate_DecomposeMatrix', '_Rotate_DecomposeMatrix'):
                    if source.endswith(suffix):
                        prefixes.add(source[:-len(suffix)])
    for prefix in prefixes:
        nodes = [n for n in cmds.ls(prefix + '_*') if cmds.nodeType(n) in
                 ('multMatrix', 'decomposeMatrix', 'blendMatrix', 'pickMatrix', 'aimMatrix', 'composeMatrix')]
        if nodes:
            cmds.delete(nodes)

#-------------------------
# Faster playback: the single target parent (+ scale) constraints of the block become one multMatrix ->
# decomposeMatrix per node. Kept as constraints: the IK / FK switch blends (animated weights), scale only
# constraints (rig groups to Global_Ctrl, mirror groups) and *_BallToes_Jnt_parentConstraint1, the
# Custom_Biped_Orients block deletes / recreates it by name.
# The driven node reads its parent worldInverseMatrix, never its own parentInverseMatrix (that makes an
# evaluation manager cycle cluster per node).

def _world_matrix(node):
    return om.MMatrix(cmds.getAttr(node + '.worldMatrix[0]'))


def _single_target(con):
    con_type = cmds.nodeType(con)
    query = getattr(cmds, con_type)
    targets = query(con, q=True, targetList=True) or []
    aliases = query(con, q=True, weightAliasList=True) or []
    if len(targets) != 1 or any(cmds.listConnections('{}.{}'.format(con, a), s=True, d=False) for a in aliases):
        return None
    return targets[0]


def _constrained_node(con):
    for plug in ('constraintTranslateX', 'constraintRotateX', 'constraintScaleX'):
        if cmds.attributeQuery(plug, n=con, exists=True):
            nodes = cmds.listConnections('{}.{}'.format(con, plug), s=False, d=True) or []
            if nodes:
                return nodes[0]
    return None


def chain_by_name(joints):
    """Ankle, Ball, Toes joints of a foot chain in that order."""
    order = ['Ankle', 'Ball', 'Toes']
    return sorted(joints, key=lambda j: [order.index(t) for t in j.split('|')[-1].split('_') if t in order][0])


def drive_with_matrix(node, target, scale=False, world=None):
    """node follows target like a parent (+ scale) constraint with maintain offset, as matrix nodes.
    world: node rest world matrix (read it before deleting the constraint that held it)."""
    if world is None:
        world = _world_matrix(node)
    parent = (cmds.listRelatives(node, p=True) or [None])[0]
    inherits = bool(parent and cmds.getAttr(node + '.inheritsTransform'))
    # rest pose back on the channels, joint orient moved into the rotation
    local = world * _world_matrix(parent).inverse() if inherits else world
    if cmds.nodeType(node) == 'joint':
        cmds.setAttr(node + '.jointOrient', 0, 0, 0)
    for attr in ['translate', 'rotate', 'scale']:
        for axis in 'XYZ':
            cmds.setAttr('{}.{}{}'.format(node, attr, axis), lock=False)
    cmds.xform(node, os=True, m=list(local))
    offset = world * _world_matrix(target).inverse()
    mult = cmds.createNode('multMatrix', n=node + '_Follow_MultMatrix')
    cmds.setAttr(mult + '.matrixIn[0]', list(offset), type='matrix')
    cmds.connectAttr(target + '.worldMatrix[0]', mult + '.matrixIn[1]')
    if inherits:
        cmds.connectAttr(parent + '.worldInverseMatrix[0]', mult + '.matrixIn[2]')
    decompose = cmds.createNode('decomposeMatrix', n=node + '_Follow_DecomposeMatrix')
    cmds.connectAttr(mult + '.matrixSum', decompose + '.inputMatrix')
    cmds.setAttr(decompose + '.inputRotateOrder', cmds.getAttr(node + '.rotateOrder'))
    channels = [('outputTranslate', 'translate'), ('outputRotate', 'rotate')]
    if scale:
        channels.append(('outputScale', 'scale'))
    for out, attr in channels:
        for axis in 'XYZ':
            cmds.connectAttr('{}.{}{}'.format(decompose, out, axis), '{}.{}{}'.format(node, attr, axis), f=True)


def constraints_to_matrix(constraints):
    """Swap what can be swapped, returns the constraints that stay."""
    by_node = {}
    for con in constraints:
        if not cmds.objExists(con) or cmds.nodeType(con) not in ('parentConstraint', 'scaleConstraint'):
            continue
        if con.endswith('_BallToes_Jnt_parentConstraint1'):
            continue
        target = _single_target(con)
        node = _constrained_node(con)
        if target and node:
            by_node.setdefault(node, {})[cmds.nodeType(con)] = (con, target)
    for node, cons in by_node.items():
        if 'parentConstraint' not in cons:
            continue
        parent_con, target = cons['parentConstraint']
        scale_con = cons.get('scaleConstraint')
        with_scale = bool(scale_con and scale_con[1] == target and all(v > 0 for v in cmds.getAttr(node + '.scale')[0]))
        world = _world_matrix(node)
        cmds.delete([parent_con] + ([scale_con[0]] if with_scale else []))
        drive_with_matrix(node, target, scale=with_scale, world=world)
    return [c for c in constraints if cmds.objExists(c)]

#-------------------------
# Controllers scale (like Limb / Hand v002): Limb v002 puts the IK, SubIk and FK ankle controllers scale
# (blended by the switch, in the ankle joint axes) on the limb ankle joint scale. The foot bind joints get
# it around the limb ankle, so the whole foot scales (non uniform too), and the toes bind joint gets the
# toes controller scale on top (its axes are the toes controller axes).

def _bind_follow(bind):
    """multMatrix -> decomposeMatrix that drives a bind joint after the matrix swap."""
    decompose = (cmds.listConnections(bind + '.translateX', s=True, d=False, type='decomposeMatrix') or [None])[0]
    if not decompose:
        return None, None
    return decompose, cmds.listConnections(decompose + '.inputMatrix', s=True, d=False, p=True)[0]


def limb_scale_ctrl(limb_ankle):
    """Limb v002 GlobalScale controller (L_Leg_GlobalScale_Ctrl) that scale constrains the limb joints group,
    so the foot scales with the leg. Global_Ctrl when the limb has none."""
    node = limb_ankle if cmds.objExists(limb_ankle) else None
    while node:
        for con in set(cmds.listConnections(node + '.scaleX', s=True, d=False, type='scaleConstraint') or []):
            for target in cmds.scaleConstraint(con, q=True, targetList=True) or []:
                if 'GlobalScale' in target:
                    return target
        node = (cmds.listRelatives(node, p=True) or [None])[0]
    return 'Global_Ctrl'


def add_foot_scale(limb_ankle, toes_ctrl, ankle_bind, ball_bind):
    if not cmds.objExists(limb_ankle):
        cmds.warning('Foot: {} not found, the ankle controllers do not scale the foot'.format(limb_ankle))
        limb_ankle = None

    around_ankle = None
    if limb_ankle:
        # limb ankle without scale, its scale channels in its own axes: rigid^-1 * scale * rigid
        decompose = cmds.createNode('decomposeMatrix', n=limb_ankle + '_FootScale_DecomposeMatrix')
        cmds.connectAttr(limb_ankle + '.worldMatrix[0]', decompose + '.inputMatrix')
        rigid = cmds.createNode('composeMatrix', n=limb_ankle + '_FootScale_Rigid_ComposeMatrix')
        cmds.connectAttr(decompose + '.outputTranslate', rigid + '.inputTranslate')
        cmds.connectAttr(decompose + '.outputQuat', rigid + '.inputQuat')
        cmds.setAttr(rigid + '.useEulerRotation', 0)
        inverse = cmds.createNode('inverseMatrix', n=limb_ankle + '_FootScale_InverseMatrix')
        cmds.connectAttr(rigid + '.outputMatrix', inverse + '.inputMatrix')
        scale = cmds.createNode('composeMatrix', n=limb_ankle + '_FootScale_ComposeMatrix')
        cmds.connectAttr(limb_ankle + '.scale', scale + '.inputScale')
        around_ankle = cmds.createNode('multMatrix', n=limb_ankle + '_FootScale_MultMatrix')
        cmds.connectAttr(inverse + '.outputMatrix', around_ankle + '.matrixIn[0]')
        cmds.connectAttr(scale + '.outputMatrix', around_ankle + '.matrixIn[1]')
        cmds.connectAttr(rigid + '.outputMatrix', around_ankle + '.matrixIn[2]')
        around_ankle += '.matrixSum'

    for bind, own_scale in ((ankle_bind, None), (ball_bind, toes_ctrl)):
        decompose, follow = _bind_follow(bind)
        if not decompose:
            cmds.warning('Foot: {} is not matrix driven, controllers scale skipped'.format(bind))
            continue
        items = []
        if own_scale:
            toes_scale = cmds.createNode('composeMatrix', n=bind + '_CtrlScale_ComposeMatrix')
            cmds.connectAttr(own_scale + '.scale', toes_scale + '.inputScale')
            items.append(toes_scale + '.outputMatrix')
        items.append(follow)
        if around_ankle:
            items.append(around_ankle)
        mult = cmds.createNode('multMatrix', n=bind + '_CtrlScale_MultMatrix')
        for i, item in enumerate(items):
            cmds.connectAttr(item, '{}.matrixIn[{}]'.format(mult, i))
        cmds.connectAttr(mult + '.matrixSum', decompose + '.inputMatrix', f=True)
        for axis in 'XYZ':
            for plug in cmds.listConnections('{}.scale{}'.format(bind, axis), s=True, d=False, p=True) or []:
                cmds.disconnectAttr(plug, '{}.scale{}'.format(bind, axis))
            cmds.connectAttr('{}.outputScale{}'.format(decompose, axis), '{}.scale{}'.format(bind, axis), f=True)

#-------------------------
# Studio orients: same result as the Custom_Biped_Orients block (FixToes), so feet do not need it.

SN_TOES_ORIENT = [0, 90, 0]


def apply_custom_orients(ctrl, rotate, right):
    """Put an OrientChange group above the ctrl rotated by rotate, the ctrl children stay where they are."""
    children = cmds.listRelatives(ctrl, c=True, type='transform') or []
    for child in children:
        cmds.parent(child, world=True)
    root = mt.root_grp(input=ctrl, custom=True, custom_name='OrientChange')[0]
    cmds.rotate(rotate[0], rotate[1], rotate[2], root, relative=True, objectSpace=True)
    if right:
        cmds.setAttr(root + '.translate', 0, 0, 0)
        cmds.setAttr(root + '.rotate', *rotate)
        cmds.setAttr(root + '.scale', 1, 1, 1)
        cmds.setAttr(ctrl + '.translate', 0, 0, 0)
        cmds.setAttr(ctrl + '.rotate', 0, 0, 0)
    for child in children:
        cmds.parent(child, ctrl)

#-------------------------

def build_foot_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guide = cmds.listRelatives(block, c=True)[0]

    #orient the joints
    #mt.orient_joint(input = guide)
    for jnt in cmds.listRelatives(guide, ad=True):
        try:
            cmds.makeIdentity(apply=True, t=True, r=True, s=True ,n=False, pn=1)
        except:
            pass
    new_guide = mt.duplicate_and_remove_guides(guide)
    print (new_guide)
    to_build = [new_guide]
    old_constraints = set(cmds.ls(type='constraint'))

    #use this group for later cleaning, just assign them when you create the top on hierarchy
    clean_rig_grp = ''
    clean_ctrl_grp = ''

    #get attrs
    ikfk_switch_attr = cmds.getAttr('{}.SwitchIKFKAttr'.format(config), asString=True)
    rfl_attr = cmds.getAttr('{}.IkAttrsPosition'.format(config), asString=True)
    block_parent_ik = cmds.getAttr('{}.SetIKCtrl'.format(config), asString=True)
    block_parent_fk = cmds.getAttr('{}.SetFKCtrl'.format(config), asString=True)
    main_ik = cmds.getAttr('{}.IKLeg'.format(config), asString=True)
    size = cmds.getAttr('{}.CtrlSize'.format(config), asString=True)

    # Check for ParallelToFloor attribute (compatibility safe)
    parallel_to_floor = False
    if cmds.attributeQuery('ParallelToFloor', node=config, exists=True):
        try:
            parallel_to_floor = cmds.getAttr('{}.ParallelToFloor'.format(config))
        except Exception:
            parallel_to_floor = False

    # Default: Mutant orients, SN: studio orients (what the Custom_Biped_Orients block FixToes did)
    if cmds.attributeQuery('Orients', n=config, exists=True):
        orients = cmds.getAttr('{}.Orients'.format(config), asString=True)
    else:
        orients = 'Default'
    toes_data = []
    scale_data = []

    #prep work for right side ------------------------------------------------------

    #if mirror is set only to right we need to build on left for mirror behavior then putt it back to righ side
    if cmds.getAttr('{}.Mirror'.format(config), asString = True) == 'Right_Only':
        miror_grp = mt.mirror_group(new_guide, world = True)
        cmds.makeIdentity(miror_grp, a=True, t=True, r=True, s=True)
        cmds.parent(new_guide, w = True)
        cmds.delete(miror_grp)
        mt.orient_joint(input = new_guide)

    elif cmds.getAttr('{}.Mirror'.format(config), asString = True) == 'True':
        right_guide = mt.duplicate_change_names(input = new_guide, hi = True, search=nc['left'], replace =nc['right'])[0]
        to_build.append(right_guide)
        print (to_build)


    #build ------------------------------------------------------
    for side_guide in to_build:

        #smart select the colors
        if str(side_guide).startswith(nc['left']):
            color = setup['left_color']
        elif str(side_guide).startswith(nc['right']):
            color = setup['right_color']
        else:
            color = setup['main_color']


        #main funcion -------------------------------------------
        #change joints order
        all_joints = cmds.listRelatives(side_guide, c=True, ad=True)
        all_joints.insert(0,side_guide)
        print (all_joints)
        #Reorder to match desire order
        order_keys = {0:'Ankle'+nc['joint'],
                      1: 'Heel'+nc['joint'],
                      2: 'Toes'+nc['joint'],
                      3: 'In'+nc['joint'],
                      4: 'Out'+nc['joint'],
                      5: 'BallFloor'+nc['joint'],
                      6: 'Ball'+nc['joint'],
                      7: 'HeelMid'+nc['joint']
                      }
        ordered_joints = []
        for key in order_keys:
            for jnt in all_joints:
                if order_keys[key] in jnt:
                    ordered_joints.append(jnt)

        print(ordered_joints)

        all_joints=ordered_joints
        #hardcoded parents

        rbl_jnts = [all_joints[1], all_joints[3],all_joints[4],all_joints[5],all_joints[7]]

        #all_joints : ['L_Foot_Ankle_Jnt', 'L_Foot_Heel_Jnt', 'L_Foot_Toes_Jnt', 'L_Foot_In_Jnt',
        #              'L_Foot_Out_Jnt', 'L_Foot_BallFloor_Jnt', 'L_Foot_Ball_Jnt', 'L_Foot_HeelMid_Jnt']
        for jnt in all_joints:
            try:cmds.parent(jnt, w=True)
            except:pass

        cmds.parent(all_joints[6],all_joints[0])
        cmds.parent(all_joints[2],all_joints[6])
        cmds.parent(all_joints[7],all_joints[1])
        cmds.parent(all_joints[5],all_joints[7])
        cmds.parent(all_joints[1],all_joints[3])
        cmds.parent(all_joints[3],all_joints[4])

        #create missing rfl joints

        #create groups for RFL in correct order
        rfl_main_grps = []
        for jnt in rbl_jnts:
            main_grp = cmds.group(em=True, n = jnt.replace(nc['joint'], '_RFL' + nc['group']))
            cmds.delete(cmds.parentConstraint(jnt,main_grp,mo=False))
            rfl_main_grps.append(main_grp)

        for jnt in all_joints[0],all_joints[2],all_joints[6]:
            main_grp = cmds.group(em=True, n = jnt.replace(nc['joint'], '_RFL' + nc['group']))
            cmds.delete(cmds.parentConstraint(jnt,main_grp,mo=False))
            rfl_main_grps.append(main_grp)

        print (rfl_main_grps)

        #hardcoded parents... again
        #['L_Foot_Heel_RFL_Grp' 0 , 'L_Foot_In_RFL_Grp' 1 , 'L_Foot_Out_RFL_Grp' 2 , 'L_Foot_BallFloor_RFL_Grp' 3,
        # 'L_Foot_HeelMid_RFL_Grp' 4 , 'L_Foot_Ankle_RFL_Grp' 5 , 'L_Foot_Toes_RFL_Grp' 6 , 'L_Foot_Ball_RFL_Grp' 7 ]

        cmds.parent(rfl_main_grps[5],rfl_main_grps[7])
        cmds.parent(rfl_main_grps[7],rfl_main_grps[6])
        cmds.parent(rfl_main_grps[6],rfl_main_grps[3])
        cmds.parent(rfl_main_grps[3],rfl_main_grps[4])
        cmds.parent(rfl_main_grps[4],rfl_main_grps[0])
        cmds.parent(rfl_main_grps[0],rfl_main_grps[1])
        cmds.parent(rfl_main_grps[1],rfl_main_grps[2])


        for grp in rfl_main_grps:
            cmds.select(grp)
            autoA = mt.root_grp(autoRoot=True)
            autoB = mt.root_grp()


        #FK IK JOINTS
        cmds.delete(rbl_jnts)

        cmds.select(side_guide)
        ik_joints = mt.duplicate_change_names(input=side_guide, hi=True, search=nc['joint'], replace=nc['ik'])
        cmds.select(side_guide)
        fk_joints = mt.duplicate_change_names(input=side_guide, hi=True, search=nc['joint'], replace=nc['fk'])
        print (ik_joints)#['R_Foot_Ankle_Ik_Jnt', 'R_Foot_Ball_Ik_Jnt', 'R_Foot_Toes_Ik_Jnt']
        print (fk_joints)#['R_Foot_Ankle_Fk_Jnt', 'R_Foot_Ball_Fk_Jnt', 'R_Foot_Toes_Fk_Jnt']


        #fk
        parent_fk = block_parent_fk
        if parent_fk == 'new_locator':
            parent_fk = cmds.spaceLocator(n='{}_ParentFK{}'.format(fk_joints[0], nc['locator']))[0]
        else:
            if parent_fk.startswith(nc['left']) and side_guide.startswith(nc['right']):
                parent_fk = parent_fk.replace(nc['left'], nc['right'])


        #IK
        # create ik handle
        ankle_ikSpline = cmds.ikHandle(sj=ik_joints[0],
                                         ee=ik_joints[1],
                                         sol='ikSCsolver',
                                         n=ik_joints[0].replace(nc['joint'], nc['ik_sc']),
                                         ccv=False,
                                         pcv=False)

        ball_ikSpline = cmds.ikHandle(sj=ik_joints[1],
                                       ee=ik_joints[2],
                                       sol='ikSCsolver',
                                       n= ik_joints[1].replace(nc['joint'], nc['ik_sc']),
                                       ccv=False,
                                       pcv=False)

        cmds.parent(ankle_ikSpline[0], rfl_main_grps[7])
        cmds.parent(ball_ikSpline[0], rfl_main_grps[6])


        #create share controller in case we dont have a switch attr to put it in there
        share_ctrl = mt.curve(input= '',
                              type='circleX',
                              rename=True,
                              custom_name=True,
                              name=side_guide.replace('_Ankle'+nc['joint'], '_Toes'+nc['ctrl']),
                              size=size)
        mt.assign_color(color=color)
        share_grp = mt.root_grp()[0]
        cmds.select(share_ctrl)
        root_grp, auto_grp = mt.root_grp(autoRoot=True)
        mt.match(share_grp, all_joints[6], r=True,t=True)

        if parallel_to_floor:
            # Create a temp locator in front of the foot (Z+ world position)
            temp_locator = cmds.spaceLocator(n=side_guide + '_TempParallelLocator')[0]
            cmds.xform(temp_locator, ws=True, t=[0, 0, 10])
            # Aim constraint auto group to locator, only rotate Z
            cmds.select(auto_grp)
            aim_constraint = cmds.aimConstraint(
            temp_locator,
            auto_grp,
            aimVector=[0, 0, 1],
            upVector=[0, 1, 0],
            worldUpType="vector",
            worldUpVector=[0, 1, 0],
            skip=["x", "y"]
            )[0]
            # Delete constraint and locator after
            cmds.delete(aim_constraint)
            cmds.delete(temp_locator)

        cmds.parentConstraint(all_joints[6], share_grp)

        #new toes joint
        cmds.select(cl=True)
        shared_toes_jnt = cmds.joint( n = all_joints[6].replace('_Ball', '_BallToes'))
        cmds.parentConstraint(share_ctrl, shared_toes_jnt, mo=False)

        #parent rfl groups to ik parent
        parent_ik = block_parent_ik
        if parent_ik == 'new_locator':
            parent_ik = cmds.spaceLocator(n = '{}_ParentIK{}'.format(fk_joints[0], nc['locator']))[0]
        else:
            if parent_ik.startswith(nc['left']) and side_guide.startswith(nc['right']):
                parent_ik = parent_ik.replace(nc['left'], nc['right'])

        #cmds.parentConstraint(parent_ik, rfl_main_grps[0], mo=True)
        p = cmds.listRelatives(rfl_main_grps[2], p=True)[0]
        pp = cmds.listRelatives(p, p=True)[0]
        ppp = cmds.listRelatives(pp, p=True)[0]

        #add ik fk ctrl shape
        if ikfk_switch_attr == 'new_attr':
            cmds.select(share_ctrl)
            switch_attr = mt.shape_with_attr(input='', obj_name='{}_Switch'.format(share_ctrl),
                                                   attr_name='Switch_IK_FK')
        else:
            switch_attr = ikfk_switch_attr

        if side_guide.startswith(nc['right']):
            switch_attr = switch_attr.replace(nc['left'],nc['right'])


        main_joints = cmds.listRelatives(side_guide, c=True, ad=True)
        main_joints.insert(0,side_guide)
        # v002: match the chains by name, listRelatives order is not the same on the mirrored guide
        # (v001 switched R_Foot_Ball_Jnt to the toes ik / fk joints)
        main_joints, ik_joints, fk_joints = [chain_by_name(c) for c in (main_joints, ik_joints, fk_joints)]
        mt.switch_constraints(this=ik_joints[0], that=fk_joints[0], main=main_joints[0], attr=switch_attr)
        mt.switch_constraints(this=ik_joints[1], that=fk_joints[1], main=main_joints[1], attr=switch_attr)
        mt.switch_constraints(this=ik_joints[2], that=fk_joints[2], main=main_joints[2], attr=switch_attr)
        # v002: no scale switch, the ik / fk foot joints only get the rig scale (the main joints inherit it).
        # On the mirrored side it decomposed the -1 scale on a different axis every pose and twisted the ball.
        for jnt in main_joints:
            scale_cons = cmds.listRelatives(jnt, type='scaleConstraint') or []
            if scale_cons:
                cmds.delete(scale_cons)
                cmds.setAttr(jnt + '.scale', 1, 1, 1)

        #switch ik fk in the shared ctrl
        #mt.switch_constraints(this=parent_ik, that=parent_fk, main=share_grp, attr=switch_attr)


        #IK RFL Attrs
        if rfl_attr == 'new_locator':
            ik_attrs_shape = cmds.spaceLocator(n = side_guide + '_FootAttrs' + nc['locator'])[0]
        else:
            if rfl_attr.startswith(nc['left']) and side_guide.startswith(nc['right']):
                ik_attrs_shape = rfl_attr.replace(nc['left'], nc['right'])
            else:
                ik_attrs_shape = rfl_attr

        # ['L_Foot_Heel_RFL_Grp' 0 , 'L_Foot_In_RFL_Grp' 1 , 'L_Foot_Out_RFL_Grp' 2 , 'L_Foot_BallFloor_RFL_Grp' 3,
        # 'L_Foot_HeelMid_RFL_Grp' 4 , 'L_Foot_Ankle_RFL_Grp' 5 , 'L_Foot_Toes_RFL_Grp' 6 , 'L_Foot_Ball_RFL_Grp' 7 ]
        rfl_attrs = {'RollToes':'{}.rotateX'.format(cmds.listRelatives(rfl_main_grps[6],p=True)[0]),
                     'PivotToes':'{}.rotateY'.format(cmds.listRelatives(rfl_main_grps[6],p=True)[0]),
                     'PivotBallFloor':'{}.rotateZ'.format(cmds.listRelatives(rfl_main_grps[3],p=True)[0]),
                     'RollBall':'{}.rotateZ'.format(cmds.listRelatives(rfl_main_grps[7],p=True)[0]),
                     'BallTwist':'{}.rotateX'.format(cmds.listRelatives(cmds.listRelatives(rfl_main_grps[7],p=True)[0], p=True)[0]),
                     'PivotBall':'{}.rotateY'.format(cmds.listRelatives(rfl_main_grps[7],p=True)[0]),
                     'PivotHeelMid':'{}.rotateY'.format(cmds.listRelatives(rfl_main_grps[4],p=True)[0]),
                     'RollHeel':'{}.rotateX'.format(cmds.listRelatives(rfl_main_grps[0],p=True)[0]),
                     'PivotHeel':'{}.rotateY'.format(cmds.listRelatives(rfl_main_grps[0],p=True)[0]),
                     'RollOut':'{}.rotateZ'.format(cmds.listRelatives(rfl_main_grps[2],p=True)[0]),
                     'PivotOut':'{}.rotateY'.format(cmds.listRelatives(rfl_main_grps[2],p=True)[0]),
                     'RollIn':'{}.rotateZ'.format(cmds.listRelatives(rfl_main_grps[1],p=True)[0]),
                     'PivotIn':'{}.rotateY'.format(cmds.listRelatives(rfl_main_grps[1],p=True)[0])
                     }

        #Foot Roll
        mt.line_attr(input = ik_attrs_shape, name = 'FootRoll', lines = 10)
        break_limit_attr = mt.new_attr(input=ik_attrs_shape, name='BreakRoll', min=-0, max=180, default=45)
        extend_attr = mt.new_attr(input=ik_attrs_shape, name='ExtendRoll', min=-0, max=180, default=90)
        foot_roll_attr = mt.new_attr(input=ik_attrs_shape, name='FootRoll', min=-180, max=180, default=0)
        mt.line_attr(input = ik_attrs_shape, name = 'RFL', lines = 10)

        for attr in rfl_attrs:
            rfl_temp_attr = mt.new_attr(input= ik_attrs_shape, name = attr, min = -100 , max = 100, default = 0)
            if attr == 'RollBall':
                # v002: positive RollBall lifts the heel like FootRoll / RollToes / RollHeel (v001 rolled back)
                flip = cmds.createNode('multDL', n=side_guide + '_RollBall_Flip_MultDoubleLinear')
                cmds.setAttr(flip + '.input2', -1)
                cmds.connectAttr(rfl_temp_attr, flip + '.input1')
                rfl_temp_attr = flip + '.output'
            cmds.connectAttr(rfl_temp_attr, rfl_attrs[attr])



        #Ball
        roll_contidion_node = cmds.shadingNode('condition', asUtility=True, n=side_guide + '_Ball_Limit' + nc['condition'])
        cmds.setAttr(str(roll_contidion_node) + ".operation", 3) #grather equal than
        cmds.connectAttr(break_limit_attr, str(roll_contidion_node) + '.firstTerm')
        cmds.connectAttr(foot_roll_attr, str(roll_contidion_node) + '.secondTerm')
        cmds.connectAttr(foot_roll_attr, str(roll_contidion_node) + '.colorIfTrue.colorIfTrueR')
        cmds.connectAttr(break_limit_attr, str(roll_contidion_node) + '.colorIfFalse.colorIfFalseR')


        #ball negative turn off
        rollneg_contidion_node = cmds.shadingNode('condition', asUtility=True, n=side_guide + '_BallNegative_Limit' + nc['condition'])
        cmds.setAttr(str(rollneg_contidion_node) + ".operation", 2) #grather than
        cmds.setAttr(str(rollneg_contidion_node) + '.secondTerm', 0)
        cmds.setAttr(str(rollneg_contidion_node) + '.outColor.outColorR', 0)

        #reverse ball
        ball_group_attr = '{}.rotateZ'.format(cmds.listRelatives(cmds.listRelatives(rfl_main_grps[7],p=True)[0], p=True)[0])
        mt.connect_md_node(in_x1=str(roll_contidion_node) + '.outColor.outColorR',
                           in_x2=-1.0,
                           out_x=rollneg_contidion_node + '.colorIfTrue.colorIfTrueR'
                           ,mode='mult', name='', force=True)

        cmds.connectAttr(rollneg_contidion_node+'.outColor.outColorR', ball_group_attr)
        cmds.connectAttr(roll_contidion_node+'.outColor.outColorR', rollneg_contidion_node+'.firstTerm')

        #L_Foot_Ball_RFL_Grp_Auto_Grp_Offset_Grp

        #toes
        toes_contidion_node = cmds.shadingNode('condition', asUtility=True, n=side_guide + '_Toes_Limit' + nc['condition'])
        cmds.setAttr(str(toes_contidion_node) + ".operation", 3) #grather equal than
        cmds.connectAttr(break_limit_attr, str(toes_contidion_node) + '.firstTerm')
        cmds.connectAttr(foot_roll_attr, str(toes_contidion_node) + '.secondTerm')

        cmds.setAttr(str(toes_contidion_node) + '.colorIfTrue.colorIfTrueR', 0)

        toes_substract_node = cmds.shadingNode('plusMinusAverage', asUtility=True, n=side_guide + '_Toes_Substract' + nc['plus_minus_average'])
        cmds.setAttr(str(toes_substract_node) + ".operation", 2) #substract
        cmds.setAttr(str(toes_contidion_node) + '.colorIfTrue.colorIfTrueR', 0)

        cmds.connectAttr(toes_substract_node + '.output1D', str(toes_contidion_node) + '.colorIfFalse.colorIfFalseR')
        cmds.connectAttr(break_limit_attr, str(toes_substract_node) + '.input1D[1]')
        cmds.connectAttr(foot_roll_attr, str(toes_substract_node) + '.input1D[0]')

        cmds.connectAttr(str(toes_contidion_node) + '.outColor.outColorR',
         '{}.rotateX'.format(cmds.listRelatives(cmds.listRelatives(rfl_main_grps[6],p=True)[0], p=True)[0]))

        #heel back
        #Heel
        back_heel_contidion_node = cmds.shadingNode('condition', asUtility=True, n=side_guide + '_Toes_Limit' + nc['condition'])
        cmds.setAttr(str(back_heel_contidion_node) + ".operation", 5) #less equal than

        cmds.setAttr(str(back_heel_contidion_node) + '.firstTerm', 0)
        cmds.connectAttr(foot_roll_attr, str(back_heel_contidion_node) + '.secondTerm')
        cmds.setAttr(str(back_heel_contidion_node) + '.colorIfTrue.colorIfTrueR', 0)
        cmds.connectAttr(foot_roll_attr ,str(back_heel_contidion_node) + '.colorIfFalse.colorIfFalseR')

        cmds.connectAttr(str(back_heel_contidion_node) + '.outColor.outColorR',
         '{}.rotateX'.format(cmds.listRelatives(cmds.listRelatives(rfl_main_grps[0],p=True)[0], p=True)[0]))

        #roll reverse
        roll_reverse_contidion_node = cmds.shadingNode('condition', asUtility=True, n=side_guide + '_Toes_Limit' + nc['condition'])
        cmds.setAttr(str(roll_reverse_contidion_node) + ".operation", 3) #grather equal than

        cmds.connectAttr('{}.rotateX'.format(cmds.listRelatives(cmds.listRelatives(rfl_main_grps[6],p=True)[0], p=True)[0]),
                         str(roll_reverse_contidion_node) + '.firstTerm')

        toes_substract_node = cmds.shadingNode('plusMinusAverage', asUtility=True,
                                               n=side_guide + '_Toes_Substract' + nc['plus_minus_average'])
        cmds.setAttr(str(toes_substract_node) + ".operation", 2)  # substract
        cmds.connectAttr(break_limit_attr, str(toes_substract_node) + '.input1D[1]')
        cmds.connectAttr(extend_attr, str(toes_substract_node) + '.input1D[0]')

        cmds.connectAttr(toes_substract_node+'.output1D', str(roll_reverse_contidion_node) + '.secondTerm')

        cmds.connectAttr(toes_substract_node+'.output1D', str(roll_reverse_contidion_node) + '.colorIfTrue.colorIfTrueR')
        cmds.connectAttr('{}.rotateX'.format(cmds.listRelatives(cmds.listRelatives(rfl_main_grps[6],p=True)[0], p=True)[0]),
                        str(roll_reverse_contidion_node) + '.colorIfFalse.colorIfFalseR')


        cmds.connectAttr(roll_reverse_contidion_node + '.outColor.outColorR',
                         '{}.rotateZ'.format(rfl_main_grps[7]))


        # clean a bit
        clean_rig_grp = cmds.group(em=True, n='{}'.format(side_guide.replace(nc['joint'], nc['group'])))
        cmds.parent(all_joints[0],clean_rig_grp)
        cmds.parent(rfl_main_grps[2] +'_Root_Grp',clean_rig_grp)
        cmds.parent(ik_joints[0],clean_rig_grp)
        cmds.parent(fk_joints[0],clean_rig_grp)
        cmds.parent(shared_toes_jnt ,clean_rig_grp)

        clean_ctrl_grp = share_grp

        #flip right rig  to right side -------------------------

        #check if the mirror attrs to Only_Right or mirror to True
        if cmds.getAttr('{}.Mirror'.format(config), asString = True) == 'Right_Only':
            miror_grp = mt.mirror_group(clean_rig_grp, world = True)
            clean_rig_grp = miror_grp

        elif cmds.getAttr('{}.Mirror'.format(config), asString = True) == 'True':
            if str(side_guide).startswith(nc['right']) :
                miror_grp = mt.mirror_group(clean_rig_grp, world=True)
                clean_rig_grp = miror_grp

            else:
                pass

        else: #only left side
            pass


        #create bind Joints for the skin -------------------------
        cmds.select(cl=True)
        ankle_bind_joint = cmds.joint(n = main_joints[0].replace(nc['joint'], nc['joint_bind']))
        cmds.parentConstraint(main_joints[0], ankle_bind_joint, mo = False)
        cmds.scaleConstraint(main_joints[0], ankle_bind_joint, mo = True)
        try: cmds.parent(ankle_bind_joint, w=True)
        except:pass
        cmds.setAttr('{}.radius'.format(ankle_bind_joint), 1.5)
        cmds.setAttr('{}.segmentScaleCompensate'.format(ankle_bind_joint), 0)
        cmds.setAttr('{}.inheritsTransform'.format(ankle_bind_joint), 0)

        ball_bind_joint = cmds.joint(n = shared_toes_jnt.replace(nc['joint'], nc['joint_bind']))
        cmds.parentConstraint(shared_toes_jnt, ball_bind_joint, mo = False)
        cmds.scaleConstraint(shared_toes_jnt, ball_bind_joint, mo = True)
        cmds.setAttr('{}.radius'.format(ball_bind_joint), 1.5)
        cmds.setAttr('{}.segmentScaleCompensate'.format(ball_bind_joint), 0)
        cmds.setAttr('{}.inheritsTransform'.format(ball_bind_joint), 0)

        #Finish -------------------------------------------

        #game parents for bind joints
        game_parent = cmds.getAttr('{}.SetGameParent'.format(config))
        if side_guide.startswith(nc['right']):
            game_parent = game_parent.replace(nc['left'],nc['right'])

        if cmds.objExists(game_parent):
            cmds.parent(ankle_bind_joint, game_parent)
        else:
            bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])
            if cmds.objExists(bind_jnt_grp):
                cmds.parent(ankle_bind_joint, bind_jnt_grp)


        #parents at the end

        if main_ik == 'new_locator':
            cmds.parent(cmds.spaceLocator(n = ik_joints[0].replace(nc['joint'],'_Here')), rfl_main_grps[5])
        else:
            if main_ik.startswith(nc['left']) and side_guide.startswith(nc['right']):
                pc_ik = cmds.listRelatives(main_ik.replace(nc['left'], nc['right']), type='parentConstraint',c=True)
                if pc_ik:
                    pc_ik=pc_ik[0]
                    cmds.delete(pc_ik)
                remove_matrix_driver(main_ik.replace(nc['left'], nc['right']))
                cmds.parent(main_ik.replace(nc['left'], nc['right']), rfl_main_grps[5])
            else:
                pc_ik = cmds.listRelatives(main_ik, c=True, type='parentConstraint')
                if pc_ik:
                    pc_ik=pc_ik[0]
                    cmds.delete(pc_ik)
                remove_matrix_driver(main_ik)
                cmds.parent(main_ik, rfl_main_grps[5])
        

        #For Quad Build
        ball_ball_ctrl = parent_ik.replace(nc['ctrl'], '_Ball'+nc['ctrl']).replace('_Sub', '').replace('Sub', '').replace('Paw', '')
        if cmds.objExists(ball_ball_ctrl): #is quad
            cmds.pointConstraint(rfl_main_grps[5], cmds.listRelatives(ball_ball_ctrl, p=True)[0], mo=True)
            cmds.parentConstraint(
                parent_ik.replace(nc['ctrl'], nc['joint']).replace('_Sub', '').replace('Sub', '').replace('Paw', ''),
                ik_joints[0], mo=True)
            cmds.parentConstraint(parent_ik, ppp, mo=True)
            cmds.parentConstraint(parent_fk, fk_joints[0], mo=True)
        else: #no quad
            cmds.parentConstraint(
                parent_ik.replace(nc['ctrl'], nc['joint']).replace('Sub', '').replace('Paw', ''),
                ik_joints[0], mo=True)
            cmds.parentConstraint(parent_ik, ppp, mo=True)
            cmds.parentConstraint(parent_fk, fk_joints[0], mo=True)


        #Fix stretchy
        #L_Ankle_Ik_IKrp
        #'L_Hip_Ik_Jnt_Stretchy_Loc'
        stretchy_loc = main_ik.replace('Ankle_Ik_IKrp', 'Hip_Ik_Jnt_Stretchy_Loc')
        if side_guide.startswith(nc['right']):
            stretchy_loc=stretchy_loc.replace(nc['left'], nc['right'])
        if cmds.objExists(stretchy_loc):
            constraint= cmds.listRelatives(stretchy_loc, ad=True, type='parentConstraint')
            if constraint:
                cmds.delete(constraint)
            remove_matrix_driver(stretchy_loc)
            if side_guide.startswith(nc['right']):
                cmds.parentConstraint(cmds.listRelatives(main_ik.replace(nc['left'], nc['right']), p=True)[0], stretchy_loc, mo=True)
            else:
                cmds.parentConstraint(cmds.listRelatives(main_ik, p=True)[0], stretchy_loc, mo=True)

        #clean ctrls
        cmds.parent(clean_ctrl_grp, 'Rig_Ctrl_Grp')

        #parent rig
        cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))

        # limb ankle joint (Limb v002 puts the IK / SubIk / FK ankle controllers scale on it)
        limb_ankle = parent_fk.replace(nc['fk'].replace(nc['joint'], '') + nc['ctrl'], nc['joint'])

        #scale: the limb GlobalScale ctrl (it has the Global scale too), so the RFL pivots / ik goal and the
        #foot joints scale with the leg and the ik does not stretch when the leg is scaled
        scale_ctrl = limb_scale_ctrl(limb_ankle)
        cmds.scaleConstraint(scale_ctrl, clean_rig_grp, mo=True)
        cmds.scaleConstraint(scale_ctrl, clean_ctrl_grp, mo=True)

        #put everything in the asset container
        mt.put_inside_rig_container([toes_contidion_node, roll_contidion_node, roll_reverse_contidion_node, rollneg_contidion_node, toes_substract_node, back_heel_contidion_node])

        toes_data.append((share_ctrl, shared_toes_jnt, str(side_guide).startswith(nc['right'])))
        scale_data.append((limb_ankle, share_ctrl, ankle_bind_joint, ball_bind_joint))

    # studio orients for the toes controllers
    if orients == 'SN':
        for toes_ctrl, toes_jnt, right in toes_data:
            apply_custom_orients(toes_ctrl, SN_TOES_ORIENT, right)
            # the toes joint follows the reoriented ctrl, no offset
            for constraint in cmds.listRelatives(toes_jnt, type='parentConstraint') or []:
                cmds.delete(constraint)
            cmds.parentConstraint(toes_ctrl, toes_jnt, mo=False)

    # constraints -> matrix nodes (faster playback)
    new_constraints = [c for c in cmds.ls(type='constraint') if c not in old_constraints]
    kept = constraints_to_matrix(new_constraints)
    print('Foot matrix swap: {} constraints replaced, {} kept'.format(len(new_constraints) - len(kept), len(kept)))

    # controllers scale: the ankle controllers scale the whole foot, the toes controller its own joint
    for limb_ankle, toes_ctrl, ankle_bind, ball_bind in scale_data:
        add_foot_scale(limb_ankle, toes_ctrl, ankle_bind, ball_bind)

    # build complete ----------------------------------------------------
    print ('Build {} Success'.format(block))


#build_foot_block()
