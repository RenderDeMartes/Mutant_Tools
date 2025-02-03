from __future__ import absolute_import, division
from maya import cmds, OpenMaya
import maya.mel as mel
import re
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

TAB_FOLDER = '003_Facial'
PYBLOCK_NAME = 'exec_ribbon_mouth'

#Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-2]
FOLDER=''
for f in PATH_PARTS:
    FOLDER = os.path.join(FOLDER, f)



# ---------------------------------------------

def create_mouth_block(name='Mouth'):

    # Read name conventions as nc[''] and setup as seup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-2]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '003_RibbonMouth.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()

    # name checks and block creation
    name = mt.ask_name(text=module['Name'])
    if cmds.objExists('{}{}'.format(name, nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name=name, icon='RibbonLips', attrs=module['attrs'], build_command=module['build_command'],
                            import_command=module['import'])
    config = block[1]
    block = block[0]

    left_orient_lip = mt.create_joint_guide(name = nc['left']+name + '_Orient'+nc['guide'])
    cmds.move(3,0,0)
    cmds.parent(left_orient_lip, block)
    mouthCenter = mt.create_joint_guide(name = name +'_SlideCenter'+nc['guide'])
    cmds.move(0,0,-3)
    cmds.parent(mouthCenter, block)


    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_mouth_block()

#-------------------------

def reverse_surface(input_surface):
    # Duplicate the input surface
    duplicated_surface = cmds.duplicate(input_surface, returnRootsOnly=True)[0]

    # Reverse the surface
    cmds.reverseSurface(duplicated_surface, direction=2, replaceOriginal=True)

    return duplicated_surface

def build_mouth_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    name = block.replace(nc['module'], '')
    orient_guide = cmds.listRelatives(block, c=True)[0]
    mouth_center = cmds.listRelatives(block, c=True)[1]

    # use this locator in case parent is set to new locator
    if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
        block_parent = cmds.spaceLocator(n='{}'.format(str(block).replace(nc['module'], '_Parent' + nc['locator'])))
    else:
        block_parent = cmds.getAttr('{}.SetParent'.format(config))

    ctrl_size = cmds.getAttr('{}.CtrlSize'.format(config))

    upper_edge = cmds.getAttr('{}.SetUpperEdge'.format(config), asString=True).split(',')
    lower_edge = cmds.getAttr('{}.SetLowerEdge'.format(config), asString=True).split(',')
    attrs_position = cmds.getAttr('{}.SetAttrsPosition'.format(config), asString=True)

    amount = 10 #cmds.getAttr('{}.RigAmount'.format(config), asString=True)
    #we need odd numbers
    if (amount % 2) == 0:
        amount=amount+1
    attrs_position = cmds.getAttr('{}.SetAttrsPosition'.format(config), asString=True)

    # Parent and Clean a bit
    # Clean Groups
    clean_ctrl_grp = cmds.group(em=True, name=name + nc['ctrl'] + nc['group'])
    clean_rig_grp = cmds.group(em=True, name=name + '_Rig' + nc['group'])

    #create base surface for ribbons
    edges = [upper_edge, lower_edge]
    names = ['_Upr', '_Lwr']
    colors = ['yellow', 'purple']

    lips_surfaces = []

    left_local_locs = []
    right_local_locs = []
    center_local_locs = []

    up_or_down_ctrls = []

    to_main_vis = []
    to_mid_vis = []
    to_corner_vis = []

    for num, edge in enumerate(edges):
        cmds.select(edge)
        linear_curve = cmds.polyToCurve(form=0,
                                        degree=1,
                                        conformToSmoothMeshPreview=1,
                                        n=name + '_Vtx' + nc['curve'],
                                        ch=False)[0]
        linear_curve_shape = cmds.listRelatives(linear_curve, s=True)[0]
        linear_curve_cvs = cmds.getAttr('{}.spans'.format(linear_curve_shape)) + 1

        # make sure curve is in correct orientation
        cmds.select('{}.cv[0]'.format(linear_curve))
        zero_cls = cmds.cluster()[1]
        cmds.select('{}.cv[{}]'.format(linear_curve, linear_curve_cvs))
        one_cls = cmds.cluster()[1]
        if cmds.getAttr('{}.originX'.format(zero_cls)) > cmds.getAttr('{}.originX'.format(one_cls)):
            cmds.reverseCurve(linear_curve, ch=False, replaceOriginal=True)
        cmds.delete(zero_cls, one_cls)

        cmds.delete(linear_curve, ch=True)

        start_five_curve = cmds.duplicate(linear_curve, n=name + names[num] + nc['curve'])[0]
        mel.eval('rebuildCurve -ch 1 -rpo 1 -rt 0 -end 1 -kr 0'
                 ''
                 ''
                 ' -kcp 0 -kep 1 -kt 0 -s {} -d 3 -tol 0.01 "{}";'.format(amount, start_five_curve))

        end_five_curve = cmds.duplicate(start_five_curve)[0]
        cmds.move(0,0, 0.5, start_five_curve, r=True)
        cmds.move(0,0, -0.5, end_five_curve, r=True)

        # Create nurb
        pivot = cmds.xform(mouth_center, rp=True, q=True, ws=True)
        cmds.move(pivot[0], pivot[1], pivot[2], "{}.scalePivot".format(start_five_curve),
                  "{}.rotatePivot".format(start_five_curve),
                  absolute=True)
        cmds.scale(1.01, 1.01, 1.01, start_five_curve, r=True)

        cmds.move(pivot[0], pivot[1], pivot[2], "{}.scalePivot".format(end_five_curve),
                  "{}.rotatePivot".format(end_five_curve),
                  absolute=True)
        cmds.scale(0.99, 0.99, 0.99, end_five_curve, r=True)

        surface = mel.eval('loft -ch 1 -u 1 -c 0 -ar 1 -d 3 -ss 1 -rn 0 -po 0 -rsn true "{}" "{}";'.format(start_five_curve, end_five_curve))[0]
        surface = cmds.rename(surface, name + names[num] + nc['nurb'])
        cmds.delete(linear_curve, start_five_curve, end_five_curve)

        lips_surfaces.append(surface)

    center_locs_grp = []
    to_md_rotators = []
    cmds.parent(lips_surfaces, clean_rig_grp)
    all_foll_joints = []
    for num, surface in enumerate(lips_surfaces):

        color = colors[num]
        part_name = name + names[num]
        follicles = []
        fol_joints = []

        print(surface)
        cmds.select(surface)
        fol_amount = 5
        mel.eval("createHair {} 1 10 0 0 0 0 5 0 1 2 1;".format(fol_amount))

        cmds.delete('hairSystem1', 'pfxHair1', 'nucleus1')
        cmds.setAttr(surface + '.inheritsTransform', 0)

        fol_grp = cmds.rename('hairSystem1Follicles', part_name + nc['follicle'] + nc['group'])
        cmds.parent(fol_grp, clean_rig_grp)

        fol_names = ['{}{}_01'.format(nc['right'], part_name), '{}{}_02'.format(nc['right'], part_name),
                     'C_{}'.format(part_name),
                     '{}{}_01'.format(nc['left'], part_name), '{}{}_02'.format(nc['left'], part_name)]


        for num, fol in enumerate(cmds.listRelatives(fol_grp, c=True)):
            gc = cmds.listRelatives(fol, c=True)
            cmds.delete(gc[-1])

            fol = cmds.rename(fol,  fol_names[num] + nc['follicle'])

            follicles.append(fol)
            cmds.select(fol)
            jnt = cmds.joint(n=fol_names[num]+ nc['follicle'] + nc['joint'])
            fol_joints.append(jnt)
            all_foll_joints.append(jnt)
            # Disconnect incoming connections
            print(fol)
            #mel.eval('CBunlockAttr "{}.r"'.format(fol))
            cmds.setAttr("{}.r".format(fol), lock=False)

            #rotation connectAttr disconnect fix
            #cmds.disconnectAttr(cmds.listConnections("{}.r".format(fol), plugs=True)[0], "{}.r".format(fol))
            to_md_rotators.append(fol)

        #Create null folicles to place the ctrls and joint ctrls
        #duplicate joints for ctrl joints
        left_joints = []
        center_joints = []
        right_joints = []

        left_joints_root = []
        center_joints_root = []
        right_joints_root = []

        left_ctrls = []
        center_ctrls = []
        right_ctrls = []

        left_ctrls_root = []
        center_ctrls_root = []
        right_ctrls_root = []

        ctrl_joints = []

        central_rotators = []

        ctrl_jnt_grp = cmds.group(n=part_name + nc['joint'] + nc['ctrl'] + nc['group'], em=True)
        ctrl_grp = cmds.group(n=part_name + nc['ctrl'] + nc['group'], em=True)

        cmds.parent(ctrl_jnt_grp, clean_rig_grp)
        cmds.parent(ctrl_grp, clean_ctrl_grp)


        for jnt in fol_joints:
            cmds.select(cl=True)
            ctrl_joint = cmds.joint(n=jnt.replace(nc['follicle'] + nc['joint'], nc['ctrl'] + nc['joint']))
            joint_root_grp, joint_auto_grp = mt.root_grp(autoRoot=True)
            cmds.delete(cmds.pointConstraint(jnt, joint_root_grp))

            cmds.parent(joint_root_grp, ctrl_jnt_grp)

            ctrl = mt.curve(input=ctrl_joint,
                            type='halfCircle',
                            rename=True,
                            custom_name=True,
                            name=ctrl_joint.replace(nc['ctrl'] + nc['joint'], nc['ctrl']),
                            size=ctrl_size)
            to_mid_vis.append(cmds.listRelatives(ctrl, s=True)[0])
            if 'Lwr' in ctrl:
                mt.rotate_shape(input=ctrl, x=0, y=0, z=180)

            mt.assign_color(color=color)
            root_grp = mt.root_grp()[0]
            mt.match(root_grp, ctrl_joint, r=True, t=True)
            cmds.parent(root_grp, ctrl_grp)

            #ConnectAttr
            cmds.connectAttr('{}.translate'.format(ctrl), '{}.translate'.format(ctrl_joint), f=True)
            cmds.connectAttr('{}.rotate'.format(ctrl), '{}.rotate'.format(ctrl_joint), f=True)
            cmds.connectAttr('{}.scale'.format(ctrl), '{}.scale'.format(jnt), f=True)

            trans_attr = mt.new_attr(root_grp, name='ConnectMult', min=0.1, max=9999, default=1.5)

            mt.connect_md_node(in_x1='{}.translateX'.format(ctrl), in_x2=trans_attr, out_x='{}.translateX'.format(ctrl_joint), mode='multiply')
            mt.connect_md_node(in_x1='{}.translateY'.format(ctrl), in_x2=trans_attr, out_x='{}.translateY'.format(ctrl_joint), mode='multiply')
            mt.connect_md_node(in_x1='{}.translateZ'.format(ctrl), in_x2=trans_attr, out_x='{}.translateZ'.format(ctrl_joint), mode='multiply')

            if jnt.startswith(nc['left']):
                left_joints.append(ctrl_joint)
                left_ctrls.append(ctrl)
                left_joints_root.append(joint_root_grp)
                left_ctrls_root.append(root_grp)
            elif jnt.startswith(nc['right']):
                right_joints.append(ctrl_joint)
                right_ctrls.append(ctrl)
                right_joints_root.append(joint_root_grp)
                right_ctrls_root.append(root_grp)
            else:
                center_joints.append(ctrl_joint)
                center_ctrls.append(ctrl)
                center_joints_root.append(joint_root_grp)
                center_ctrls_root.append(root_grp)

            ctrl_joints.append(ctrl_joint)

        print(left_joints)
        print(center_joints)
        print(right_joints)

        print(ctrl_joints)

        #connect corners
        to_corner_vis.append(cmds.listRelatives(right_ctrls[-1], s=True)[0])
        to_corner_vis.append(cmds.listRelatives(left_ctrls[-1], s=True)[0])

        #Improve orient of joints and ctrls
        #Hardcoded because its a few joints

        #Coner left Joints
        cmds.delete(cmds.orientConstraint(orient_guide, left_ctrls_root[-1], mo=False))
        cmds.delete(cmds.orientConstraint(orient_guide, left_joints_root[-1], mo=False))

        #Second Joint Left
        cmds.delete(cmds.aimConstraint(center_joints[0],  left_ctrls_root[0], aimVector=(-1, 0, 0), upVector=(0, 1, 0), worldUpType='vector',  skip=['x', 'z'], mo=False))
        cmds.delete(cmds.aimConstraint(center_joints[0],  left_joints_root[0], aimVector=(-1, 0, 0), upVector=(0, 1, 0), worldUpType='vector',  skip=['x', 'z'], mo=False))

        #First Joint Left
        cmds.delete(cmds.aimConstraint(left_joints[0],  left_ctrls_root[1], aimVector=(-1, 0, 0), upVector=(0, 1, 0), worldUpType='vector',  skip=['x', 'z'], mo=False))
        cmds.delete(cmds.aimConstraint(left_joints[0],  left_joints_root[1], aimVector=(-1, 0, 0), upVector=(0, 1, 0), worldUpType='vector',  skip=['x', 'z'], mo=False))

        #Right ones match and then mirror to pos
        for r, l in zip(right_ctrls_root, left_ctrls_root):
            mt.match(r, l, t=True,r=True,s=True)
            mirror_grp = mt.mirror_group(r, world=True)
            cmds.parent(mirror_grp, ctrl_grp)

        for r, l in zip(right_joints_root, left_joints_root):
            mt.match(r, l, t=True,r=True,s=True)
            mirror_grp = mt.mirror_group(r, world=True)
            cmds.parent(mirror_grp, ctrl_jnt_grp)

        #Skin ctrl joints to surface
        skin = cmds.skinCluster(ctrl_joints, surface, sm=0, bm=1, tsb=True)[0]
        #['R_Lips_Lwr_01_Ctrl_Jnt', 'R_Lips_Lwr_02_Ctrl_Jnt', 'C_Lips_Lwr_Ctrl_Jnt', 'L_Lips_Lwr_02_Ctrl_Jnt', 'L_Lips_Lwr_01_Ctrl_Jnt']
        cmds.skinPercent(skin, '{}.cv[0][0:3]'.format(surface), tv=[ctrl_joints[1], 1])
        cmds.skinPercent(skin, '{}.cv[1][0:3]'.format(surface), tv=[ctrl_joints[1], 1])
        cmds.skinPercent(skin, '{}.cv[2][0:3]'.format(surface), tv=[ctrl_joints[1], 1])

        cmds.skinPercent(skin, '{}.cv[3][0:3]'.format(surface), tv=[ctrl_joints[1], 0.6])
        cmds.skinPercent(skin, '{}.cv[3][0:3]'.format(surface), tv=[ctrl_joints[0], 0.4])

        cmds.skinPercent(skin, '{}.cv[4][0:3]'.format(surface), tv=[ctrl_joints[0], 1])

        cmds.skinPercent(skin, '{}.cv[5][0:3]'.format(surface), tv=[ctrl_joints[0], 0.4])
        cmds.skinPercent(skin, '{}.cv[5][0:3]'.format(surface), tv=[ctrl_joints[2], 0.6])

        cmds.skinPercent(skin, '{}.cv[6][0:3]'.format(surface), tv=[ctrl_joints[2], 1])
        cmds.skinPercent(skin, '{}.cv[7][0:3]'.format(surface), tv=[ctrl_joints[2], 1])

        cmds.skinPercent(skin, '{}.cv[8][0:3]'.format(surface), tv=[ctrl_joints[2], 0.6])
        cmds.skinPercent(skin, '{}.cv[8][0:3]'.format(surface), tv=[ctrl_joints[3], 0.4])

        cmds.skinPercent(skin, '{}.cv[9][0:3]'.format(surface), tv=[ctrl_joints[3], 1])

        cmds.skinPercent(skin, '{}.cv[10][0:3]'.format(surface), tv=[ctrl_joints[3], 0.4])
        cmds.skinPercent(skin, '{}.cv[10][0:3]'.format(surface), tv=[ctrl_joints[4], 0.6])

        cmds.skinPercent(skin, '{}.cv[11][0:3]'.format(surface), tv=[ctrl_joints[4], 1])
        cmds.skinPercent(skin, '{}.cv[12][0:3]'.format(surface), tv=[ctrl_joints[4], 1])
        cmds.skinPercent(skin, '{}.cv[13][0:3]'.format(surface), tv=[ctrl_joints[4], 1])

        #create LOCAL and GLobal Locs to follow systems
        l_local_loc = cmds.spaceLocator(n=nc['left'] + part_name + '_Local' + nc['locator'])[0]
        r_local_loc = cmds.spaceLocator(n=nc['right'] + part_name + '_Local' + nc['locator'])[0]
        c_local_loc = cmds.spaceLocator(n=nc['center']+part_name+'_Local'+nc['locator'])[0]

        left_local_locs.append(l_local_loc)
        right_local_locs.append(r_local_loc)
        center_local_locs.append(c_local_loc)

        #Position de locators
        mt.match(r_local_loc, orient_guide)
        mt.match(l_local_loc, orient_guide)
        mt.match(c_local_loc, center_ctrls[0])

        #Clean the locators
        local_loc_grp = cmds.group(em=True, n=part_name+'_Local'+nc['locator']+nc['group'])
        cmds.parent(l_local_loc, l_local_loc, c_local_loc, local_loc_grp)

        for loc in [r_local_loc, c_local_loc, l_local_loc]:
            mt.root_grp(loc)
            central_grp = mt.root_grp(input=loc, custom=True, custom_name='CentralRotator')[0]
            pivot = cmds.xform(mouth_center, rp=True, q=True, ws=True)
            cmds.move(pivot[0], pivot[1], pivot[2], "{}.scalePivot".format(central_grp), "{}.rotatePivot".format(central_grp), absolute=True)
            central_rotators.append(central_grp)

        to_mirror_grp = cmds.listRelatives(r_local_loc,p=True)[0]
        to_mirror_parent = cmds.listRelatives(to_mirror_grp,p=True)[0]
        r_local_loc_grp = mt.mirror_group(to_mirror_grp, world=True)
        cmds.parent(r_local_loc_grp, to_mirror_parent)
        cmds.parent(to_mirror_parent, local_loc_grp)

        center_locs_grp.append(local_loc_grp)

        # Constraints to joints
        pc1 = cmds.parentConstraint(l_local_loc, left_joints_root[1], mo=True)
        pc2 = cmds.parentConstraint(l_local_loc, c_local_loc, left_joints_root[0], mo=True)
        pc3 = cmds.parentConstraint(c_local_loc, center_joints_root[0], mo=True)
        pc4 = cmds.parentConstraint(r_local_loc, c_local_loc, right_joints_root[0], mo=True)
        pc5 = cmds.parentConstraint(r_local_loc, right_joints_root[1], mo=True)

        # # Aims
        # cmds.aimConstraint(l_local_loc, cmds.listRelatives(left_joints[0], p=True)[0], aimVector=(1, 0, 0),
        #                    upVector=(0, 1, 0), worldUpType='vector', mo=True)
        # cmds.aimConstraint(r_local_loc, cmds.listRelatives(right_joints[0], p=True)[0], aimVector=(-1, 0, 0),
        #                    upVector=(0, 1, 0), worldUpType='vector', mo=True)

        #Create Up or Down Main Ctrl
        up_or_dw_ctrl = mt.curve(input=ctrl_joints[2],
                        type='square',
                        rename=True,
                        custom_name=True,
                        name=ctrl_joints[2].replace(nc['ctrl'] + nc['joint'], '_Main' + nc['ctrl']),
                        size=ctrl_size*1.5)
        to_main_vis.append(cmds.listRelatives(up_or_dw_ctrl, s=True)[0])
        mt.translate_shape(up_or_dw_ctrl, z=ctrl_size)
        if 'Upr' in ctrl:
            mt.rotate_shape(input=up_or_dw_ctrl, x=90, y=0, z=180)
        else:
            mt.rotate_shape(up_or_dw_ctrl, x=90)
        mt.scale_shape(up_or_dw_ctrl, y=0.5, x=2)

        mt.assign_color(color=color)
        mt.match(up_or_dw_ctrl, ctrl_joints[2], r=True, t=True)
        root_grp = mt.root_grp()[0]

        up_or_down_ctrls.append(up_or_dw_ctrl)

        cmds.connectAttr('{}.translate'.format(up_or_dw_ctrl), '{}.translate'.format(c_local_loc), f=True)
        cmds.connectAttr('{}.rotate'.format(up_or_dw_ctrl), '{}.rotate'.format(c_local_loc), f=True)

        mt.hide_attr(up_or_dw_ctrl, s=True)
        cmds.parent(root_grp, clean_ctrl_grp)


    #Create side ctrls
    side_crls = []
    side_crls_root = []
    sub_side_crls = []
    sub_side_crls_root = []

    side_locs = []

    for side in [nc['left'], nc['right']]:
        cmds.select(cl=True)
        ctrl = mt.curve(input='',
                        type='triangle',
                        rename=True,
                        custom_name=True,
                        name=side + name + '_Main' + nc['ctrl'],
                        size=ctrl_size)

        mt.smart_assign_color(ctrl)
        root_grp = mt.root_grp()[0]
        side_crls.append(ctrl)
        side_crls_root.append(root_grp)
        mt.hide_attr(ctrl, s=True)

        mt.line_attr(input=ctrl, name='Lips')
        mode_attr = mt.new_enum(input=ctrl, name='mode', enums='BSP:RIG')
        sub_vis_attr = mt.new_enum(input=ctrl, name='SubCtrl', enums='Hide:Show', keyable=False)

        sub_ctrl = mt.curve(input='',
                                 type='triangle',
                                 rename=True,
                                 custom_name=True,
                                 name=side + name + '_Sub' + nc['ctrl'],
                                 size=ctrl_size*0.75)


        mt.smart_assign_color(sub_ctrl)
        sub_root_grp = mt.root_grp()[0]
        mt.hide_attr(sub_ctrl, s=True)
        sub_side_crls.append(sub_ctrl)
        sub_side_crls_root.append(sub_root_grp)

        cmds.connectAttr(sub_vis_attr, sub_root_grp+'.v')

        cmds.parent(sub_root_grp, ctrl)
        mt.match(root_grp, orient_guide)

        mt.rotate_shape(ctrl, x=90, z=-90)
        mt.rotate_shape(sub_ctrl, x=90, z=-90)

        #local loc
        side_loc = cmds.spaceLocator(n=side + name + '_Sub' + nc['locator'])[0]
        mt.match(side_loc, orient_guide)
        side_locs.append(side_loc)
        loc_root_grp, loc_auto_grp = mt.root_grp(autoRoot=True)

        # ConnectAttr

        for axis in ['X', 'Y', 'Z']:
            #---------Translate--------

            double_linear = cmds.shadingNode('addDoubleLinear', asUtility=True, name=ctrl + '_DLOut')

            cmds.connectAttr('{}.translate{}'.format(sub_ctrl, axis), '{}.input1'.format(double_linear), f=True)
            mt.connect_md_node(in_x1=mode_attr, in_x2='{}.translate{}'.format(ctrl, axis),
                               out_x='{}.input2'.format(double_linear), mode='multiply', vector=False)
            cmds.connectAttr('{}.output'.format(double_linear), '{}.translate{}'.format(side_loc, axis), f=True)

            #---------Rotate--------

            double_linear = cmds.shadingNode('addDoubleLinear', asUtility=True, name=ctrl + '_DLOut')

            cmds.connectAttr('{}.rotate{}'.format(sub_ctrl, axis), '{}.input1'.format(double_linear), f=True)
            mt.connect_md_node(in_x1=mode_attr, in_x2='{}.rotate{}'.format(ctrl, axis),
                               out_x='{}.input2'.format(double_linear), mode='multiply', vector=False)
            cmds.connectAttr('{}.output'.format(double_linear), '{}.rotate{}'.format(side_loc, axis), f=True)


        #mirror right
        print(left_local_locs)
        print(right_local_locs)
        # ['L_Lips_Upr_Local_Loc', 'L_Lips_Lwr_Local_Loc']
        # ['R_Lips_Upr_Local_Loc', 'R_Lips_Lwr_Local_Loc']
        if side == nc['right']:
            root_grp = mt.mirror_group(input=root_grp, world=True)
            mirror_loc_grp = mt.mirror_group(input=loc_root_grp, world=True)
            cmds.parent(root_grp, clean_ctrl_grp)
            cmds.parent(mirror_loc_grp, clean_rig_grp)

            #Contraints
            cmds.connectAttr('{}.translate'.format(side_loc), '{}.translate'.format(right_local_locs[0]))
            cmds.connectAttr('{}.rotate'.format(side_loc), '{}.rotate'.format(right_local_locs[0]))
            cmds.connectAttr('{}.translate'.format(side_loc), '{}.translate'.format(right_local_locs[1]))
            cmds.connectAttr('{}.rotate'.format(side_loc), '{}.rotate'.format(right_local_locs[1]))
        else:
            cmds.parent(root_grp, clean_ctrl_grp)
            cmds.parent(loc_root_grp, clean_rig_grp)
            cmds.connectAttr('{}.translate'.format(side_loc), '{}.translate'.format(left_local_locs[0]))
            cmds.connectAttr('{}.rotate'.format(side_loc), '{}.rotate'.format(left_local_locs[0]))
            cmds.connectAttr('{}.translate'.format(side_loc), '{}.translate'.format(left_local_locs[1]))
            cmds.connectAttr('{}.rotate'.format(side_loc), '{}.rotate'.format(left_local_locs[1]))

    #Center Ctrls
    # Main Mouth Controller
    center_grp = cmds.group(em=True, n=name + '_Center' + nc['group'])
    cmds.delete(cmds.parentConstraint(mouth_center, center_grp))
    center_root = mt.root_grp()[0]
    center_lips_grp = cmds.group(em=True, n=name + '_Centerlips' + nc['group'])
    cmds.delete(cmds.parentConstraint(center_grp, center_lips_grp))
    center_lips_root = mt.root_grp()[0]
    cmds.parent(center_lips_root, center_grp)

    center_ctrl = mt.curve(input=center_grp,
                           type='square',
                           rename=True,
                           custom_name=True,
                           name=name + '_Center' + nc['ctrl'],
                           size=ctrl_size)
    mt.assign_color(color='lightBlue')
    center_ctrl_root = mt.root_grp()[0]
    cmds.delete(cmds.parentConstraint(mouth_center, center_ctrl_root))
    cmds.select(center_ctrl + '.cv[0:8]')
    cmds.rotate(90, 0, 0)
    center_cluster = cmds.cluster()
    cmds.delete(cmds.parentConstraint(up_or_dw_ctrl, center_cluster))
    cmds.delete(center_ctrl, ch=True)

    cmds.connectAttr('{}.translate'.format(center_ctrl), '{}.translate'.format(center_grp))
    cmds.connectAttr('{}.rotate'.format(center_ctrl), '{}.rotate'.format(center_grp))
    cmds.connectAttr('{}.scale'.format(center_ctrl), '{}.scale'.format(center_grp))

    cmds.parent(center_locs_grp, center_lips_grp)

    cmds.parent(center_root, clean_rig_grp)
    cmds.parent(center_ctrl_root, ctrl_grp, clean_ctrl_grp)

    cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
    cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])

    # Visibility switches
    # hide ctrls
    if attrs_position == 'new_locator':
        guide_attrs_position = cmds.spaceLocator(n=name + '_Attrs' + nc['locator'])[0]
    else:
        guide_attrs_position = attrs_position
    mt.line_attr(input=guide_attrs_position, name='Mouth_Vis')

    main_ctrl_attr = mt.new_enum(input=guide_attrs_position, name='lipsMainCtrls', enums='Hide:Show', keyable=False)

    if guide_attrs_position != center_ctrl:
        center_ctrl_attr = mt.new_enum(input=guide_attrs_position, name='lipsCenterCtrls', enums='Hide:Show', keyable=False)
        cmds.setAttr(center_ctrl_attr, 0)

    mid_ctrl_attr = mt.new_enum(input=guide_attrs_position, name='lipsMidCtrls', enums='Hide:Show', keyable=False)
    corner_ctrl_attr = mt.new_enum(input=guide_attrs_position, name='lipsCornerCtrls', enums='Hide:Show', keyable=False)

    cmds.setAttr(main_ctrl_attr, 1)
    cmds.setAttr(mid_ctrl_attr, 1)
    cmds.setAttr(corner_ctrl_attr, 0)

    if guide_attrs_position != center_ctrl:
        cmds.connectAttr(center_ctrl_attr, '{}.v'.format(cmds.listRelatives(center_ctrl, s=True)[0]), f=True)

    for ctrl in to_main_vis:
        cmds.connectAttr(main_ctrl_attr, ctrl+'.v')
    for ctrl in to_mid_vis:
        cmds.connectAttr(mid_ctrl_attr, ctrl+'.v')
    for ctrl in to_corner_vis:
        cmds.connectAttr(corner_ctrl_attr, ctrl+'.v', f=True)

    # create bind joints
    bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])
    for jnt in all_foll_joints:
        cmds.select(cl=True)
        bind_joint = cmds.joint(n=jnt.replace(nc['follicle']+nc['joint'], nc['joint_bind']))
        cmds.parentConstraint(jnt, bind_joint)
        cmds.scaleConstraint(jnt, bind_joint)
        cmds.setAttr('{}.radius'.format(bind_joint), 1.5)
        cmds.parent(bind_joint, bind_jnt_grp)

    #use this locator in case parent is set to new locator
    if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
        block_parent = cmds.spaceLocator( n = '{}'.format(str(block).replace(nc['module'],'_Parent' + nc['locator'])))[0]
    else:
        block_parent = cmds.getAttr('{}.SetParent'.format(config))

    cmds.parentConstraint(block_parent, clean_ctrl_grp, mo=True)
    cmds.scaleConstraint(block_parent, clean_ctrl_grp, mo=True)

    #hot fixes
    cmds.setAttr(corner_ctrl_attr,l=True, cb=False)
    # for fol in ['L_Lips_Upr_02_Fol','R_Lips_Upr_01_Fol','R_Lips_Lwr_01_Fol','L_Lips_Lwr_02_Fol']:
    #     cmds.disconnectAttr(cmds.listConnections("{}.r".format(fol), plugs=True)[0], "{}.r".format(fol))
    for fol in to_md_rotators:
        md = mt.connect_md_node(in_x2=cmds.listConnections("{}.r".format(fol), plugs=True)[0], in_x1=1.0,
                                out_x="{}.r".format(fol), mode='mult', name='', force=True, vector=True)
        cmds.setAttr(md + '.input1.input1Z', 0.25)
