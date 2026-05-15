from __future__ import absolute_import, division
from maya import cmds, mel
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
TAB_FOLDER = '004_Animals'
PYBLOCK_NAME = 'exec_quadlimb'

#Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-2]
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

def create_quadlimb_block(name = 'QuadLimb'):

    nc, curve_data, setup = mt.import_configs()
    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    limb_name = name.split(',')
    if cmds.objExists('{}{}'.format(name[0],nc['module'])):
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

def build_quadlimb_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guide = cmds.listRelatives(block, c=True)[0]
    aim_guide = cmds.listRelatives(block, c=True)[1]

    if 'Aim' in guide:
        guide = cmds.listRelatives(block, c=True)[1]
        aim_guide = cmds.listRelatives(block, c=True)[0]

    new_guide = mt.duplicate_and_remove_guides(guide)
    print(new_guide)
    to_build = [new_guide]

    # orient the joints

    mt.orient_joint(input=new_guide)
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

        main_joints = [side_guide] + cmds.listRelatives(side_guide, ad=True)
        print(main_joints)

        cmds.select(side_guide, hi=True)
        limb_a = cmds.ls(sl=True)[0]
        limb_b = cmds.ls(sl=True)[1]
        limb_c = cmds.ls(sl=True)[2]
        limb_d = cmds.ls(sl=True)[3]

        main_joints = [limb_a, limb_b, limb_c, limb_d]

        for jnt in main_joints:
            print(jnt)


        #use this locator in case parent is set to new locator
        if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
            block_parent = cmds.spaceLocator( n = '{}'.format(str(side_guide).replace(nc['joint'],'_Parent' + nc['locator'])))[0]
        else:
            block_parent = cmds.getAttr('{}.SetParent'.format(config))
            if side_guide.startswith(nc['right']):
                block_parent = block_parent.replace(nc['left'],nc['right'])

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

        ctrl_size = cmds.getAttr('{}.CtrlSize'.format(config))
        twist_amount = cmds.getAttr('{}.TwistAmount'.format(config))

        # compatible with older versions without DogMode
        if cmds.attributeQuery('DogMode', n=config, exists=True):
            dog_mode = cmds.getAttr(config + '.DogMode', asString=True)
        else:
            dog_mode = 'Back'

        # compatible with older versions without ribbons
        if cmds.attributeQuery('CreateRibbons', n=config, exists=True):
            create_ribbons = cmds.getAttr(config + '.CreateRibbons')
        else:
            create_ribbons = True

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
        print('Setting 90 down', back_sys_joint_b)
        cmds.setAttr('{}.rotateX'.format(back_sys_joint_b), -90)

        mt.orient_joint(back_sys_joint_a)

        new_pos = cmds.getAttr('{}.tx'.format(joint_three))+cmds.getAttr('{}.tx'.format(joint_four))
        cmds.setAttr('{}.tx'.format(back_sys_joint_c), new_pos*-1)

        mt.orient_joint(back_sys_joint_a)

        #Temp ik and placement
        temp_ik_data = cmds.ikHandle(sj=back_sys_joint_a, ee=back_sys_joint_c, sol='ikRPsolver')
        mt.match(this=back_sys_joint_a, that=ik_joints[0], r=False)
        mt.match(this=temp_ik_data[0], that=ik_joints[-1], r=False)

        temp_pv = cmds.poleVectorConstraint(ik_joints[0], temp_ik_data[0])

        #Check if twist needs backwards
        pos_ik = cmds.xform(ik_joints[0], q=True, t=True, ws=True)[2]
        pos_sys = cmds.xform(back_sys_joint_b, q=True, t=True, ws=True)[2]

        print('Temp', 'Pos IK', pos_ik, 'Pos Sys', pos_sys)
        if dog_mode == 'Back':
            if pos_sys > pos_ik:
                print('Temp Flipping')
                cmds.setAttr('{}.twist'.format(temp_ik_data[0]), 180)
        else:
            if pos_sys < pos_ik:
                print('Temp Flipping')
                cmds.setAttr('{}.twist'.format(temp_ik_data[0]), 180)

        cmds.delete(temp_pv, temp_ik_data[1])
        mt.orient_joint(back_sys_joint_a)

        #Create oficial system now
        backwards_ik = cmds.ikHandle(sj=back_sys_joint_a, ee=back_sys_joint_c,
                                     sol='ikRPsolver',
                                     n=ik_joints[-1].replace(nc['joint'], nc['ik_rp']))

        distance = mt.get_distance_between(ik_joints[1], aim_guide)

        pv_loc=mt.pole_vector_placement(bone_one=[ik_joints[0]],
                                         bone_two=[ik_joints[1]],
                                         bone_three=[ik_joints[2]],
                                         back_distance=distance)

        #aim_guide
        constraint = cmds.pointConstraint(aim_guide, pv_loc, skip=['x', 'y'], mo=False)[0]
        cmds.delete(constraint)
        pv_constraint = cmds.poleVectorConstraint(pv_loc, backwards_ik[0])

        pos_ik = cmds.xform(ik_joints[0], q=True, t=True, ws=True)[2]
        pos_sys = cmds.xform(back_sys_joint_b, q=True, t=True, ws=True)[2]
        print('Pos IK', pos_ik, 'Pos Sys', pos_sys)
        if dog_mode == 'Back':
            if pos_sys > pos_ik:
                print('Flipping')
                cmds.setAttr('{}.twist'.format(backwards_ik[0]), 180)
        else:
            if pos_sys < pos_ik:
                print('Flipping')
                cmds.setAttr('{}.twist'.format(backwards_ik[0]), 180)

        backwards_ik_efector = backwards_ik[1]
        backwards_ik = backwards_ik[0]

        #This is for the RFL
        #cmds.parent(backwards_ik, joint_four)

        #Create Controllers
        #Main IK
        main_ik_ctrl = mt.curve(input='',
                        type='cube',
                        rename=True,
                        custom_name=True,
                        name=ik_joints[-1].replace(nc['joint'], nc['ctrl']),
                        size=ctrl_size)

        mt.assign_color(color=color)
        main_ik_ctrl_root_grp = mt.root_grp()[0]
        mt.match(main_ik_ctrl_root_grp, ik_joints[-1], r=False, t=True)
        cmds.rotate(0,0,0, main_ik_ctrl_root_grp)
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

        #Ankle Ctrl
        #Ik Sub
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
        stretch_ik_parentConstr = cmds.parentConstraint(ball_ctrl, stretch_ik_offset_grp[0], first_to_third_ik[0], mo=False)[0]
        cmds.setAttr("{}.{}W0".format(stretch_ik_parentConstr, ball_ctrl), 0)


        pos_ik = cmds.xform(ik_joints[0], q=True, t=True, ws=True)[2]
        pos_sec_jnt = cmds.xform(ik_joints[1], q=True, t=True, ws=True)[2]
        print('Pos IK', pos_ik, 'Pos Sec jnt', pos_sec_jnt)
        if dog_mode == 'Back':
            if pos_ik > pos_sec_jnt:
                print('Flipping')
                cmds.setAttr('{}.twist'.format(first_to_third_ik[0]), 180)
        else:
            if pos_ik < pos_sec_jnt:
                print('Flipping')
                cmds.setAttr('{}.twist'.format(first_to_third_ik[0]), 180)

        #This pole vector is needed for the system but its breaking the twist
        #cmds.poleVectorConstraint(pv_loc, third_to_fourth_ik[0])

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
            print(fk_joints[num], ik_joints[num], jnt)
            mt.switch_blend_colors(this=fk_joints[num], that=ik_joints[num], main=jnt, attr=switch_attr)

        # IK extra attrs
        attrs_loc = switch_attr.split('.')[0]
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

        cmds.connectAttr('Global_Ctrl.scale', normalize_loc + '.scale')

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

        #Creating remap
        stretchy_IKRP_snap_remap = cmds.shadingNode("remapValue", au=True,
                                                    name="{}_StretchySnapFix_Remap".format(attrs_loc))
        cmds.setAttr("{}.inputMin".format(stretchy_IKRP_snap_remap), 1)
        cmds.setAttr("{}.inputMax".format(stretchy_IKRP_snap_remap), 1.05)
        cmds.setAttr("{}.outputMin".format(stretchy_IKRP_snap_remap), 0)
        cmds.setAttr("{}.outputMax".format(stretchy_IKRP_snap_remap), 1)

        #connecting condition to remap
        cmds.connectAttr("{}.colorIfTrue.colorIfTrueR".format(contidion_node),
                         "{}.inputValue".format(stretchy_IKRP_snap_remap))

        #connecting remap to reverse and to first_to_third_ikrp parent constraint.
        stretchy_IKRP_snap_reverse = cmds.shadingNode("reverse", au=True,
                                                      name="{}_Reverse".format(stretchy_IKRP_snap_remap))
        cmds.connectAttr("{}.outValue".format(stretchy_IKRP_snap_remap), "{}.input.inputX".format(stretchy_IKRP_snap_reverse))

        cmds.connectAttr("{}.outValue".format(stretchy_IKRP_snap_remap), "{}.{}W0".format(stretch_ik_parentConstr,ball_ctrl))
        cmds.connectAttr("{}.output.outputX".format(stretchy_IKRP_snap_reverse),
                         "{}.{}W1".format(stretch_ik_parentConstr, stretch_ik_offset_grp[0]))




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

        for jnt in upper_upper_twist['joints']:
            cmds.connectAttr('{}.scale'.format(ik_joints[0]), '{}.scale'.format(jnt))
        for jnt in upper_twist['joints']:
            cmds.connectAttr('{}.scale'.format(ik_joints[1]), '{}.scale'.format(jnt))
        for jnt in lower_twist['joints']:
            cmds.connectAttr('{}.scale'.format(ik_joints[2]), '{}.scale'.format(jnt))

        #add ribbon
        top_top_ribbon = mt.create_mid_ribbons(name=limb_a, first_joint=limb_a, last_joint=limb_b,
                                        twist_joints=upper_upper_twist['joints'], aim=1,
                                        twist_amount=twist_amount, ctrl_size=ctrl_size, sec_color=sec_color,
                                        switch_locator=attrs_loc)

        top_ribbon = mt.create_mid_ribbons(name=limb_b, first_joint=limb_b, last_joint=limb_c,
                                        twist_joints=upper_twist['joints'], aim=1,
                                        twist_amount=twist_amount, ctrl_size=ctrl_size, sec_color=sec_color,
                                        switch_locator=attrs_loc)

        low_ribbon = mt.create_mid_ribbons(name=limb_c, first_joint=limb_c, last_joint=limb_d,
                                        twist_joints=lower_twist['joints'], aim=-1,
                                        twist_amount=twist_amount, ctrl_size=ctrl_size, sec_color=sec_color,
                                        switch_locator = attrs_loc)

        ribbon_first_vis_attr = attrs_loc + '.BendyMain'

        # Main mid controller
        main_mid_ctrl = mt.curve(input=limb_b,
                                 type='cubePlus',
                                 rename=True,
                                 custom_name=True,
                                 name=limb_b.replace(nc['joint'], 'Mid_Bendy' + nc['ctrl']),
                                 size=ctrl_size / 2,
                                 )
        mt.assign_color(main_mid_ctrl, sec_color)
        root_mid_ctrl = mt.root_grp(input=main_mid_ctrl)
        mt.shape_with_attr(input=main_mid_ctrl, obj_name=main_joints[0] + '_Switch', attr_name='')

        cmds.parentConstraint(limb_b, root_mid_ctrl, mo=False)

        cmds.pointConstraint(main_mid_ctrl, cmds.listRelatives(top_top_ribbon['second_ctrls'][1], p=True), mo=True)
        cmds.pointConstraint(main_mid_ctrl, cmds.listRelatives(top_ribbon['second_ctrls'][0], p=True), mo=True)
        cmds.connectAttr(ribbon_first_vis_attr, '{}.v'.format(cmds.listRelatives(main_mid_ctrl, shapes=True)[0]))

        # Main mid controller
        sec_mid_ctrl = mt.curve(input=limb_c,
                                 type='cubePlus',
                                 rename=True,
                                 custom_name=True,
                                 name=limb_c.replace(nc['joint'], 'Mid_Bendy' + nc['ctrl']),
                                 size=ctrl_size / 2,
                                 )
        mt.assign_color(sec_mid_ctrl, sec_color)
        root_sec_mid_ctrl = mt.root_grp(input=sec_mid_ctrl)
        mt.shape_with_attr(input=sec_mid_ctrl, obj_name=main_joints[0] + '_Switch', attr_name='')

        cmds.parentConstraint(limb_c, root_sec_mid_ctrl, mo=False)

        cmds.pointConstraint(sec_mid_ctrl, cmds.listRelatives(top_ribbon['second_ctrls'][1], p=True), mo=True)
        cmds.pointConstraint(sec_mid_ctrl, cmds.listRelatives(low_ribbon['second_ctrls'][0], p=True), mo=True)
        cmds.connectAttr(ribbon_first_vis_attr, '{}.v'.format(cmds.listRelatives(sec_mid_ctrl, shapes=True)[0]))

        # #The rotate of the cubes for Toon Smooths
        # # Handle Pin cubes automate rotations middle_joints[0] middle_joints[3]
        # automate_bendy_grps = []
        # for jnt in [top_top_ribbon['middle_joints'][0], top_top_ribbon['middle_joints'][3],
        #             top_ribbon['middle_joints'][0], top_ribbon['middle_joints'][3],
        #             low_ribbon['middle_joints'][0], low_ribbon['middle_joints'][3]]:
        #     cmds.select(jnt)
        #     auto_grp = mt.root_grp(input='', custom=True, custom_name='_AutoBend', autoRoot=True)[-1]
        #     automate_bendy_grps.append(auto_grp)
        #
        # # L_Elbow_BendyMid_0_Jnt_Auto_Grp
        # mt.line_attr(input=attrs_loc, name='AutoBend')
        # attrs_names = ['HipBend', 'HipKneeBend', 'KneeAnkletBend', 'AnkleBallBend','BallBend']
        #
        # bendy_hip_attr = mt.new_attr(input=attrs_loc, name=attrs_names[0], min=-20, max=20, default=0)
        # bendy_hip_knee_attr = mt.new_attr(input=attrs_loc, name=attrs_names[1], min=-20, max=20, default=0)
        # bendy_knee_ankle_attr = mt.new_attr(input=attrs_loc, name=attrs_names[2], min=-20, max=20, default=0)
        # bendy_ankle_ball_attr = mt.new_attr(input=attrs_loc, name=attrs_names[3], min=-20, max=20, default=0)
        # bendy_ball_attr = mt.new_attr(input=attrs_loc, name=attrs_names[4], min=-20, max=20, default=0)
        #
        # auto_bendy_attrs = [bendy_hip_attr, bendy_hip_knee_attr,
        #                     bendy_knee_ankle_attr, bendy_ankle_ball_attr,
        #                     bendy_ball_attr]
        #
        # for attr, grp in zip(auto_bendy_attrs, automate_bendy_grps):
        #     mt.connect_md_node(in_x1='{}.translateY'.format(main_mid_ctrl), in_x2=attr, out_x='{}.rotateZ'.format(grp),
        #                        mode='multiply')

        #Order and clean
        clean_ctrl_grp = cmds.group(em=True, name=side_guide + nc['ctrl'] + nc['group'])
        clean_rig_grp = cmds.group(em=True, name=side_guide + '_Rig' + nc['group'])
        clean_ribbons_grp = cmds.group(em=True, name=side_guide + '_RigRibbons' + nc['group'])
        clean_main_system_grp = cmds.group(em=True, name=side_guide + '_RigSystem' + nc['group'])

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

        cmds.parent(upper_upper_twist['twist_grp'], clean_ribbons_grp)
        cmds.parent(upper_twist['twist_grp'], clean_ribbons_grp)
        cmds.parent(lower_twist['twist_grp'], clean_ribbons_grp)

        #Clean ribbons
        cmds.parent(top_ribbon['ribbon_plane'], top_ribbon['clean_rig_grp'], top_ribbon['fol_ribbon_grp'],
                    clean_ribbons_grp)
        cmds.parent(low_ribbon['ribbon_plane'], low_ribbon['clean_rig_grp'], low_ribbon['fol_ribbon_grp'],
                    clean_ribbons_grp)
        cmds.parent(top_top_ribbon['ribbon_plane'], top_top_ribbon['clean_rig_grp'], top_top_ribbon['fol_ribbon_grp'],
                    clean_ribbons_grp)
        cmds.parent(root_mid_ctrl, root_sec_mid_ctrl, clean_ctrl_grp)

        to_bind = top_top_ribbon['fol_joints'] + top_ribbon['fol_joints'] + low_ribbon['fol_joints']

        #Mirror
        #Parent Systems to parent Loc
        if cmds.getAttr('{}.Mirror'.format(config), asString=True) == 'Right_Only':
            mirror_ctrl_grp = mt.mirror_group(clean_ctrl_grp, world=True)
            mirror_rig_grp = mt.mirror_group(clean_rig_grp, world=True)

            cmds.parentConstraint(block_parent, mirror_ctrl_grp, mo=True)
            cmds.parentConstraint(block_parent, top_ctrl_root_grp, mo=True)
            cmds.parentConstraint('Rig_Ctrl_Grp', mirror_ctrl_grp, mo=True)
            cmds.scaleConstraint('Rig_Ctrl_Grp', mirror_ctrl_grp, mo=True)
            cmds.scaleConstraint('Rig_Ctrl_Grp', clean_main_system_grp, mo=True)
            cmds.parent(mirror_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
            cmds.parent(mirror_ctrl_grp, setup['base_groups']['control'] + nc['group'])
            cmds.parentConstraint(block_parent, main_joints_grp, mo=True)

            cmds.parentConstraint(block_parent, cmds.listRelatives(fk_system, p=True)[0], mo=True)

        elif cmds.getAttr('{}.Mirror'.format(config), asString=True) == 'True':

            if str(side_guide).startswith(nc['right']):
                mirror_ctrl_grp = mt.mirror_group(clean_ctrl_grp, world=True)
                mirror_rig_grp = mt.mirror_group(clean_rig_grp, world=True)

                cmds.parentConstraint(block_parent, top_ctrl_root_grp, mo=True)
                cmds.parentConstraint('Rig_Ctrl_Grp', mirror_ctrl_grp, mo=True)
                cmds.scaleConstraint('Rig_Ctrl_Grp', mirror_ctrl_grp, mo=True)
                cmds.scaleConstraint('Rig_Ctrl_Grp', clean_main_system_grp, mo=True)
                cmds.parent(mirror_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
                cmds.parent(mirror_ctrl_grp, setup['base_groups']['control'] + nc['group'])
                cmds.parentConstraint(block_parent, main_joints_grp, mo=True)
                cmds.parentConstraint(block_parent, cmds.listRelatives(fk_system, p=True)[0], mo=True)


            else:
                cmds.parentConstraint(block_parent, top_ctrl_root_grp, mo=True)
                cmds.parentConstraint('Rig_Ctrl_Grp', clean_ctrl_grp, mo=True)
                cmds.scaleConstraint('Rig_Ctrl_Grp', clean_ctrl_grp, mo=True)
                cmds.scaleConstraint('Rig_Ctrl_Grp', clean_main_system_grp, mo=True)
                cmds.parentConstraint(block_parent, main_joints_grp, mo=True)
                cmds.parentConstraint(block_parent, cmds.listRelatives(fk_system, p=True)[0], mo=True)


        else:  # only left side
            cmds.parentConstraint(block_parent, top_ctrl_root_grp, mo=True)
            cmds.parentConstraint('Rig_Ctrl_Grp', clean_ctrl_grp, mo=True)
            cmds.scaleConstraint('Rig_Ctrl_Grp', clean_ctrl_grp, mo=True)
            cmds.scaleConstraint('Rig_Ctrl_Grp', clean_main_system_grp, mo=True)
            cmds.parentConstraint(block_parent, main_joints_grp, mo=True)
            cmds.orienttConstraint(block_parent, clean_main_system_grp, mo=True)
            cmds.parentConstraint(block_parent, cmds.listRelatives(fk_system, p=True)[0], mo=True)


        # Fix issue with orient in the aims up vectors
        cmds.parent(top_top_ribbon['ribbon_ctrl_grp'], top_top_ribbon['clean_ctrl_grp'], clean_ctrl_grp)
        cmds.parent(top_ribbon['ribbon_ctrl_grp'], top_ribbon['clean_ctrl_grp'], clean_ctrl_grp)
        cmds.parent(low_ribbon['ribbon_ctrl_grp'], low_ribbon['clean_ctrl_grp'], clean_ctrl_grp)

        handle_grp = cmds.group(low_ribbon['handle_controllers_roots'], top_ribbon['handle_controllers_roots'],
                                n=limb_a + '_Handle' + nc['ctrl'] + nc['group'])
        if side_guide.startswith(nc['right']):
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


        cmds.scaleConstraint('Rig_Ctrl_Grp', upper_upper_twist['twist_grp'], mo=True)
        cmds.scaleConstraint('Rig_Ctrl_Grp', upper_twist['twist_grp'], mo=True)
        cmds.scaleConstraint('Rig_Ctrl_Grp', lower_twist['twist_grp'], mo=True)

        # create bind Joints for the skin -------------------------
        # bind joints
        bind_joints = []
        bind_joint = ''

        cmds.select(cl=True)
        bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])

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

        if cmds.objExists(bind_jnt_grp):
            cmds.parent(bind_joints[0], bind_jnt_grp)

        #mt.line_attr(input=attrs_loc, name='MT')


    #------------------------------------
    #Hot fix right side
    if bind_joints[0].startswith(nc['right']):
        fix_group = lower_twist['twist_grp_to_mirror']
        parent = cmds.listRelatives(fix_group, p=True)[0]
        print(fix_group)
        mirror_fix_grp = mt.mirror_group(fix_group)
        cmds.parent(mirror_fix_grp, parent)
