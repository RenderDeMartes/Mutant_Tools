from __future__ import absolute_import, division
from maya import cmds
import maya.mel as mel
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
    PATH_PARTS = PATH.parts[:-2]
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

def build_limb_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

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

    # compatible with older versions without ribbons
    if cmds.attributeQuery('Ribbons', n=config, exists=True):
        create_ribbons = cmds.getAttr(config + '.Ribbons')
    else:
        create_ribbons = True

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

        # clean a bit
        print(ikfk['ik_fk'])
        cmds.connectAttr('Global_Ctrl.scale', '{}.scale'.format(ikfk['ik_fk'][4][5][1]))

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

            #Ribbon attrs for auto bendy
            mt.line_attr(input=switch_locator, name='AutoBend')
            if mode == 'Arms':
                attrs_names = ['ShoulderBend','ElbowShoulderBend','ElbowWristBend','WristBend']
            elif mode == 'Legs':
                attrs_names = ['HipBend','KneeHipBend','KneeAnkleBend','AnkkleBend']
            else:
                attrs_names = ['FirstBend', 'SecondFirstBend', 'SecondThirdBend', 'ThirdBend']

            bendy_shoulder_attr = mt.new_attr(input=switch_locator, name=attrs_names[0], min=-20, max=20, default=0)
            bendy_elbow_shoulder_attr = mt.new_attr(input=switch_locator, name=attrs_names[1], min=-20, max=20, default=0)
            bendy_elbow_wrist_attr = mt.new_attr(input=switch_locator, name=attrs_names[2], min=-20, max=20, default=0)
            bendy_wrist_attr = mt.new_attr(input=switch_locator, name=attrs_names[3], min=-20, max=20, default=0)
            auto_bendy_attrs = [bendy_shoulder_attr, bendy_elbow_shoulder_attr, bendy_elbow_wrist_attr, bendy_wrist_attr]

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
                    cmds.connectAttr('Global_Ctrl.scale', fol_new_name+'.scale')
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

                local_geo = cmds.duplicate(middle_limb_nurb[0], n=name + 'Bendy_Other_Local' + nc['nurb'])
                # cmds.skinCluster(middle_joints, local_geo, sm=0, bm=1, tsb=True)

                cmds.select(local_geo_ik_geo, local_geo, middle_limb_nurb[0])
                bs = cmds.blendShape(n='{}_Bendy{}'.format(name, '_BS'), w=[(0, 1), (1, 1)], )
                cmds.skinCluster(twist_joints, middle_limb_nurb[0], sm=0, bm=1, tsb=True)

                local_grp = cmds.group(local_geo_ik_geo, local_geo, ik_bendy_grp, n=name + '_Local' + nc['group'])

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
                    cmds.connectAttr('Global_Ctrl.scale', cmds.listRelatives(fol, p=True)[0]+'.scale')

                forward = list(enumerate(ribbon_ctrls))
                backward = list(reversed(forward))

                extra_aim_forward_grp = cmds.group(em=True, n=name + '_ForwardAim' + nc['group'])
                cmds.scaleConstraint('Global_Ctrl', extra_aim_forward_grp)

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
                cmds.parent(local_grp, bendy_fol_grp, extra_aim_forward_grp, middle_limb_nurb[0], ribbon_rig_group)

                # transfer scale from twist to ibbon jnts
                for num, jnt in enumerate(twist_joints):
                    cmds.connectAttr('{}.scale'.format(jnt), '{}.scale'.format(fol_joints[num]))

                return {'ribbon_ctrl_grp': ribbon_ctrl_grp, 'ribbon_ctrls': ribbon_ctrls,
                        'ribbon_plane': ribbon_limb_nurb[0], 'fol_ribbon_grp': fol_grp, 'fol_joints': fol_joints,
                        'second_ctrls': second_ctrls, 'handle_controllers': handle_controllers, 'handle_controllers_roots' : handle_controllers_roots,
                        'clean_rig_grp': ribbon_rig_group, 'clean_ctrl_grp': ribbon_ctrl_grp,
                        'middle_joints' : middle_joints
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

            # cmds.pointConstraint(start, cmds.listRelatives(top_ribbon['second_ctrls'][0], p=True), mo=True)
            # cmds.pointConstraint(end, cmds.listRelatives(low_ribbon['second_ctrls'][1], p=True), mo=True)

            # Handle Pin cubes automate rotations middle_joints[0] middle_joints[3]
            automate_bendy_grps = []
            for jnt in [top_ribbon['middle_joints'][0], top_ribbon['middle_joints'][3],low_ribbon['middle_joints'][0], low_ribbon['middle_joints'][3]]:
                cmds.select(jnt)
                auto_grp = mt.root_grp(input='', custom = True, custom_name = '_AutoBend', autoRoot=True)[-1]
                automate_bendy_grps.append(auto_grp)
            #L_Elbow_BendyMid_0_Jnt_Auto_Grp
            for attr, grp in zip(auto_bendy_attrs, automate_bendy_grps):
                mt.connect_md_node(in_x1='{}.translateY'.format(main_mid_ctrl), in_x2=attr, out_x='{}.rotateZ'.format(grp), mode='multiply')


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

        #Fix Aim in pose A
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

        cmds.scaleConstraint('Rig_Ctrl_Grp', ikfk['upper_twist']['twist_grp'], mo=True)
        cmds.scaleConstraint('Rig_Ctrl_Grp', ikfk['lower_twist']['twist_grp'], mo=True)

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
        cmds.parentConstraint('Rig_Ctrl_Grp', clean_ctrl_grp, mo=True)
        cmds.scaleConstraint('Rig_Ctrl_Grp', clean_ctrl_grp, mo=True)

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

        cmds.scaleConstraint('Global_Ctrl', main_jnt_grp, mo=True)

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
