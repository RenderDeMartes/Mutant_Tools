from __future__ import absolute_import, division
'''
version: 1.0.0
date: 21/04/2020

#----------------

how to:

try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import Mutant_Tools
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload


from Mutant_Tools.Utils.Animation import ikfk_match
reload(ikfk_match)
ikfk_match.ikfk_match_callback()

#----------------
dependencies:

maya cmds
maya mel
pymel


#----------------
licence: https://www.eulatemplate.com/live.php?token=FGISW7ApRfgywum6murbBmLcusKONzkv
author:  Esteban Rodriguez <info@mutanttools.com>

'''
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

#------------------------------------------------------------------------------------

import maya.cmds as cmds
from maya.api import OpenMaya as om2
from math import pi
from functools import wraps

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
reload(Mutant_Tools.Utils.Rigging.main_mutant)

try:
    from rigTools.IkFkMatch import Bardel_IkFkMatch as matcher
    reload(matcher)
except:
    pass

mt = main_mutant.Mutant()

nc, curve_data, setup = mt.import_configs()

def undo(func):
    """ Puts the wrapped `func` into a single Maya Undo action, then
        undoes it when the function enters the finally: block """
    @wraps(func)
    def _undofunc(*args, **kwargs):
        try:
            # start an undo chunk
            cmds.undoInfo(ock=True)
            return func(*args, **kwargs)
        except Exception as e:
            print(e)
        finally:
            print("entering finally block")
            # after calling the func, end the undo chunk and undo
            cmds.undoInfo(cck=True)
            #cmds.undo()

    return _undofunc

def get_dag_path(name):
    sel = om2.MSelectionList()
    sel.add(name)
    dag = sel.getDagPath(0)
    return dag

def place_pole_vector(pole_vector, joint_a, joint_b, joint_c, force_fk):
    if force_fk:
        cmds.delete(cmds.pointConstraint(joint_b, pole_vector))
        print('Forcing')
    else:
        OA = om2.MVector(*cmds.xform(joint_a, t=True, q=True, ws=True))
        OB = om2.MVector(*cmds.xform(joint_b, t=True, q=True, ws=True))
        OC = om2.MVector(*cmds.xform(joint_c, t=True, q=True, ws=True))

        AC = OC - OA
        AB = OB - OA
        BC = OC - OB

        multiplier = (AC * AB) / (AC * AC)
        projection = AC * multiplier + OA
        direction = (OB - projection).normal()

        length = AB.length() + BC.length()
        pv_pos = OB + direction * length

        cmds.xform(pole_vector, t=[pv_pos.x, pv_pos.y, pv_pos.z], ws=True)


@undo
def ikFKSwitch(ikFk_attr, ik_ctrls, ik_chain, fk_ctrls, side, isLeg, namespace, offset, attr_at_fk=1):
    # add side prefix
    ik_ctrls = [namespace + side + i for i in ik_ctrls]
    ik_chain = [namespace + side + i for i in ik_chain]
    fk_ctrls = [namespace + side + i for i in fk_ctrls]
    ikFk_attr = namespace + side + ikFk_attr

    # check ikfk value

    if cmds.getAttr(ikFk_attr) == attr_at_fk:

        cmds.setAttr(ikFk_attr, 1 - attr_at_fk)
        place_pole_vector(ik_ctrls[1], fk_ctrls[0], fk_ctrls[1], fk_ctrls[2], True)
        fk_wrist_ws_m = cmds.xform(fk_ctrls[2], q=1, ws=1, m=1)
        cmds.xform(ik_ctrls[0], ws=1, m=fk_wrist_ws_m)
        #debug_loc = cmds.spaceLocator(n='DEBUG_FK_Wrist')
        #cmds.xform(debug_loc, ws=1, m=fk_wrist_ws_m)
        #cmds.xform(ik_ctrls[0], p=1, roo='zyx')
        #cmds.rotate(offset[0], offset[1], offset[2], ik_ctrls[0], r=1, os=1)
        
        cmds.rotate(offset[0], 0, 0, ik_ctrls[0], r=1, os=1)
        cmds.rotate(0, offset[1], 0, ik_ctrls[0], r=1, os=1)
        cmds.rotate(0, 0, offset[2], ik_ctrls[0], r=1, os=1)

        #force pole vector
        cmds.matchTransform(ik_ctrls[1], fk_ctrls[1], pos=True)


        if not isLeg:
            print(ik_ctrls[0])
            if 'R_' in ik_ctrls[0]:
                print('R')
                dif = get_wrist_diference(ik_ctrls[0])
                if dif:
                    print('dif', dif)
                    cmds.setAttr('{}.rotateX'.format(ik_ctrls[0]), cmds.getAttr('{}.rotateX'.format(ik_ctrls[0]))+dif)


    else:
        for i, ik_joint in enumerate(ik_chain):
            ik_joint_ws_matrix = cmds.xform(ik_joint, q=1, ws=1, m=1)
            cmds.xform(fk_ctrls[i], ws=1, m=ik_joint_ws_matrix)

        cmds.setAttr(ikFk_attr, attr_at_fk)

def force_last(ik_ctrl, fk_ctrl):
    print(ik_ctrl, fk_ctrl)
    up_locator, side_locator, front_locator, dummy_guide = create_aim_locators(fk_ctrl)

    dummy_ik = cmds.spaceLocator(n=ik_ctrl+'_Temp'+nc['locator'])
    cmds.xform(dummy_ik, ws=True, m=cmds.xform(ik_ctrl, ws=True, q=True, m=True))

    constraint = cmds.aimConstraint(side_locator, dummy_ik, aimVector=[1,0,0], upVector=[0,-1,0],
                                      worldUpType="object", worldUpObject=front_locator)


    cmds.xform(ik_ctrl, ws=True, t=cmds.xform(dummy_ik, ws=True, q=True, t=True))

    cmds.delete(constraint, up_locator, side_locator, front_locator, dummy_guide, dummy_ik)

def create_aim_locators(guide):
    up_locator = cmds.spaceLocator(n=guide + '_Temp_Up' + nc['locator'])[0]
    side_locator = cmds.spaceLocator(n=guide + '_Temp_Side' + nc['locator'])[0]
    front_locator = cmds.spaceLocator(n=guide + '_Temp_Front' + nc['locator'])[0]

    dummy_guide = cmds.spaceLocator(n=guide + '_Temp' + nc['locator'])
    cmds.xform(dummy_guide, ws=True, m=cmds.xform(guide, ws=True, q=True, m=True))

    cmds.parent(up_locator, side_locator, front_locator, dummy_guide)

    mt.match(up_locator, guide, r=False)
    mt.match(side_locator, guide, r=False)
    mt.match(front_locator, guide, r=False)

    # cmds.move(0, 10, 0, up_locator, r=True)
    # cmds.move(10, 0, 0, side_locator, r=True)
    # cmds.move(0, 0, 10, front_locator, r=True)

    cmds.setAttr(up_locator+'.ty', 10)
    cmds.setAttr(side_locator+'.tx', 10)
    cmds.setAttr(front_locator+'.tz', 10)

    return up_locator, side_locator, front_locator, dummy_guide

# list of ctrls and joints names

arm_ik_ctrls = ['Wrist_Ik_Ctrl', 'Wrist_Ik_PoleVector_Ctrl', 'Shoulder_Ik_Ctrl']
arm_fk_ctrls = ['Shoulder_Fk_Ctrl', 'Elbow_Fk_Ctrl', 'Wrist_Fk_Ctrl']
arm_ik_joints = ['Shoulder_Ik_Jnt', 'Elbow_Ik_Jnt', 'Wrist_Ik_Jnt']
arm_ikFk_attr = 'Shoulder_Jnt_Switch_Loc.Switch_IK_FK'
leg_ik_ctrls = ['Ankle_Ik_Ctrl', 'Ankle_Ik_PoleVector_Ctrl', 'Hip_Ik_Ctrl']
leg_fk_ctrls = ['Hip_Fk_Ctrl', 'Knee_Fk_Ctrl', 'Ankle_Fk_Ctrl']
leg_ik_joints = ['Hip_Ik_Jnt', 'Knee_Ik_Jnt', 'Ankle_Ik_Jnt']
leg_ikFk_attr = 'Hip_Jnt_Switch_Loc.Switch_IK_FK'

bd_arm_ik_ctrls = ['Ik_Wrist_01_Ctrl', 'Ik_Elbow_01_Ctrl', 'Ik_Shoulder_01_Ctrl']
bd_arm_fk_ctrls = ['Fk_Shoulder_01_Ctrl', 'Fk_Elbow_01_Ctrl', 'Fk_Wrist_01_Ctrl']
bd_arm_ik_joints = ['setup_shoulder_01_Jnt', 'setup_elbow_01_Jnt', 'setup_wrist_01_Jnt']
bd_arm_ikFk_attr = 'Palm_01_Ctrl.fkik'
bd_leg_ik_ctrls = ['Ik_Base_01_Ctrl', 'Ik_Knee_01_Ctrl', 'Ik_Hip_01_Ctrl']
bd_leg_fk_ctrls = ['Fk_Hip_01_Ctrl', 'Fk_Knee_01_Ctrl', 'Fk_Ankle_01_Ctrl']
bd_leg_ik_joints = ['setup_hip_01_Jnt', 'setup_knee_01_Jnt', 'setup_ankle_01_Jnt']
bd_leg_ikFk_attr = 'Heel_01_Ctrl.fkik'

# offsets stored as euler rotations

ikFkRotationOffsets = [
    (-90, 0, 0),
    (-90, -1.045, 90),
    (0, 0, 0),
    (-180, 0, 0),
    (-90, -1.29, 90),
    (0, 0, 90),
    (180, 0, -90)
    ]

def ikfk_match_callback():
    sel = cmds.ls(sl=1)[-1]
    ns = ''
    if ':' in sel:
        ns, sel = sel.split(':')
        ns += ':'

    side = sel[:2]
    sel = sel[2:]
    if sel in arm_ik_ctrls or sel in arm_fk_ctrls:
        ikFKSwitch(arm_ikFk_attr, arm_ik_ctrls, arm_ik_joints, arm_fk_ctrls, side, False, ns, ikFkRotationOffsets[0])
    elif sel in leg_ik_ctrls or sel in leg_fk_ctrls:
        #print('rot offset = {}'.format(ikFkRotationOffsets[4]) )
        ikFKSwitch(leg_ikFk_attr, leg_ik_ctrls, leg_ik_joints, leg_fk_ctrls, side, True, ns, ikFkRotationOffsets[4])
    elif sel in bd_arm_ik_ctrls or sel in bd_arm_fk_ctrls:
        offset_index = 3 if side == 'R_' else 2
        ikFKSwitch(bd_arm_ikFk_attr, bd_arm_ik_ctrls, bd_arm_ik_joints, bd_arm_fk_ctrls, side, False, ns, ikFkRotationOffsets[offset_index], 0)
    elif sel in bd_leg_ik_ctrls or sel in bd_leg_fk_ctrls:
        offset_index = 6 if side == 'R_' else 5
        ikFKSwitch(bd_leg_ikFk_attr, bd_leg_ik_ctrls, bd_leg_ik_joints, bd_leg_fk_ctrls, side, False, ns, ikFkRotationOffsets[offset_index], 0)

def left_arm_match():
    sel = cmds.ls(sl=1)[-1]
    ns = ''
    if ':' in sel:
        ns, sel = sel.split(':')
        ns += ':'

    side = sel[:2]
    if sel[2:] in arm_ik_ctrls or sel[2:] in arm_fk_ctrls and side =='L_':
        ikFKSwitch(arm_ikFk_attr, arm_ik_ctrls, arm_ik_joints, arm_fk_ctrls, side, False, ns)

def right_arm_match():
    sel = cmds.ls(sl=1)[-1]
    ns = ''
    if ':' in sel:
        ns, sel = sel.split(':')
        ns += ':'

    side = sel[:2]
    if sel[2:] in arm_ik_ctrls or sel[2:] in arm_fk_ctrls and side =='R_':
        ikFKSwitch(arm_ikFk_attr, arm_ik_ctrls, arm_ik_joints, arm_fk_ctrls, side, False, ns)
def left_leg_match():
    sel = cmds.ls(sl=1)[-1]
    ns = ''
    if ':' in sel:
        ns, sel = sel.split(':')
        ns += ':'

    side = sel[:2]
    if sel[2:] in arm_ik_ctrls or sel[2:] in arm_fk_ctrls and side =='L_':
        ikFKSwitch(leg_ikFk_attr, leg_ik_ctrls, leg_ik_joints, leg_fk_ctrls, side, True, ns)
def right_leg_match():
    sel = cmds.ls(sl=1)[-1]
    ns = ''
    if ':' in sel:
        ns, sel = sel.split(':')
        ns += ':'

    side = sel[:2]
    if sel[2:] in arm_ik_ctrls or sel[2:] in arm_fk_ctrls and side =='R_':
        ikFKSwitch(leg_ikFk_attr, leg_ik_ctrls, leg_ik_joints, leg_fk_ctrls, side, True, ns)

def get_wrist_diference(ik_ctrl):

    right_rotate_compansate_ctrl = ik_ctrl+'_RotationCorrection_Grp'

    custom_attr = 'IkCorrectionX'
    attr_exists= cmds.attributeQuery(custom_attr,  node=ik_ctrl,  exists=True)

    if not cmds.objExists(right_rotate_compansate_ctrl) and not attr_exists:
        return False

    if attr_exists:
        return float(cmds.getAttr(ik_ctrl+'.'+custom_attr, asString=True))*-1

    else:
        left_rotate_compansate_ctrl = right_rotate_compansate_ctrl.replace('R_', 'L_')
        r_rotx = cmds.getAttr(right_rotate_compansate_ctrl+'.rx')
        l_rotx = cmds.getAttr(left_rotate_compansate_ctrl+'.rx')

        dif = r_rotx-l_rotx
        return dif
