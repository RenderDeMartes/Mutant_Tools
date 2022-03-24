from maya import cmds, OpenMaya
import maya.mel as mel
import json
import imp
import os
from pathlib import Path

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
imp.reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()

#---------------------------------------------

TAB_FOLDER = '03_Facial'
PYBLOCK_NAME = 'exec_mouth'

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

MODULE_FILE = os.path.join(os.path.dirname(__file__),'03_Mouth.json')
with open(MODULE_FILE) as module_file:
    module = json.load(module_file)


# ---------------------------------------------

def create_mouth_block(name='Mouth'):
    # name checks and block creation
    name = mt.ask_name(text=module['Name'])
    if cmds.objExists('{}{}'.format(name, nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name=name, icon='Lips', attrs=module['attrs'], build_command=module['build_command'],
                            import_command=module['import'])
    config = block[1]
    block = block[0]

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_mouth_block()

#-------------------------

def build_mouth_block():
    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    name = block.replace(nc['module'], '')

    # use this locator in case parent is set to new locator
    if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
        block_parent = cmds.spaceLocator(n='{}'.format(str(block).replace(nc['module'], '_Parent' + nc['locator'])))
    else:
        block_parent = cmds.getAttr('{}.SetParent'.format(config))

    ctrl_size = cmds.getAttr('{}.CtrlSize'.format(config)) / 2

    upper_edge = cmds.getAttr('{}.SetUpperEdge'.format(config), asString=True).split(',')
    lower_edge = cmds.getAttr('{}.SetLowerEdge'.format(config), asString=True).split(',')
    attrs_position = cmds.getAttr('{}.SetAttrsPosition'.format(config), asString=True)

    mirror_attr = cmds.getAttr('{}.Mirror'.format(config), asString=True)

    to_build = [name]
    if mirror_attr == 'True':
        to_build = [name, name.replace(nc['left'], nc['right'])]

    for name in to_build:

        # side settings
        if name.startswith(nc['right']):
            color = 'red'
        elif name.startswith(nc['left']):
            color = 'blue'
        else:
            color = 'yellow'

    def create_lips_system(name, edge, check_curve=True, color ='yellow'):

        #
        cmds.select(edge)
        linear_curve = cmds.polyToCurve(form=0,
                                        degree=1,
                                        conformToSmoothMeshPreview=1,
                                        n=name + '_Vtx' + nc['curve'],
                                        ch=False)[0]
        linear_curve_shape = cmds.listRelatives(linear_curve, s=True)[0]
        linear_curve_cvs = cmds.getAttr('{}.spans'.format(linear_curve_shape)) + 1

        # make sure curve is in correct orientation
        if check_curve:
            cmds.select('{}.cv[0]'.format(linear_curve))
            zero_cls = cmds.cluster()[1]
            cmds.select('{}.cv[1]'.format(linear_curve))
            one_cls = cmds.cluster()[1]
            if cmds.getAttr('{}.originX'.format(zero_cls)) > cmds.getAttr('{}.originX'.format(one_cls)):
                cmds.reverseCurve(linear_curve, ch=False, replaceOriginal=True)
            cmds.delete(zero_cls, one_cls)

        cmds.delete(linear_curve, ch=True)

        vtx_joints = []
        vtx_locators = []
        points_on_curve_infos = []
        tweek_controllers = []
        vtx_joints_grp = cmds.group(em=True, n='{}_VtxJnts{}'.format(name, nc['group']))
        locators_grp = cmds.group(em=True, n='{}_FollowLocators{}'.format(name, nc['group']))
        tweek_ctrl_grp = cmds.group(em=True, n='{}_Tweeks{}{}'.format(name, nc['ctrl'], nc['group']))
        main_ctrl_grp = cmds.group(em=True, n='{}{}{}'.format(name, nc['ctrl'], nc['group']))
        cmds.parent(tweek_ctrl_grp, main_ctrl_grp)

        for num in range(linear_curve_cvs):
            # Place joint at pivot and on vertex
            cmds.select(cl=True)
            vtx_jnt = cmds.joint(n='{}_{}{}'.format(name, num, nc['joint']))
            cmds.select('{}.cv[{}]'.format(linear_curve, num))
            temp_cls = cmds.cluster()
            cmds.delete(cmds.parentConstraint(temp_cls, vtx_jnt))
            cmds.delete(temp_cls)
            vtx_joints.append(vtx_jnt)

            end_locator = cmds.spaceLocator(n='{}_{}{}'.format(name, num, nc['locator']))[0]
            vtx_locators.append(end_locator)
            cmds.parent(end_locator, locators_grp)

            # point on curve info per cv
            poci = cmds.createNode('pointOnCurveInfo', n='{}_{}_POCI'.format(name, num))
            points_on_curve_infos.append(poci)
            cmds.connectAttr('{}.worldSpace[0]'.format(linear_curve_shape), '{}.inputCurve'.format(poci))
            cmds.connectAttr('{}.position'.format(poci), '{}.translate'.format(end_locator))
            cmds.setAttr('{}.parameter'.format(poci), num)

            # create controllers to control the curve
            ctrl = mt.curve(input=vtx_jnt,
                            type='square',
                            rename=True,
                            custom_name=True,
                            name=end_locator.replace(nc['locator'], nc['ctrl']),
                            size=ctrl_size / 3)
            tweek_controllers.append(ctrl)
            mt.assign_color(color=color)
            ctrl_root = mt.root_grp()[0]
            mt.match(ctrl_root, vtx_jnt, r=True, t=True)
            cmds.parent(ctrl_root, tweek_ctrl_grp)

            cmds.delete(cmds.parentConstraint(end_locator, vtx_jnt))
            vtx_root = mt.root_grp(input=vtx_jnt)
            cmds.parentConstraint(end_locator, vtx_root)

            #Connect directy to threat as local
            cmds.connectAttr('{}.rotate'.format(ctrl), '{}.rotate'.format(vtx_jnt))
            cmds.connectAttr('{}.translate'.format(ctrl), '{}.translate'.format(vtx_jnt))
            cmds.connectAttr('{}.scale'.format(ctrl), '{}.scale'.format(vtx_jnt))
            cmds.connectAttr('{}.rotate'.format(end_locator), '{}.rotate'.format(ctrl_root))
            cmds.connectAttr('{}.translate'.format(end_locator), '{}.translate'.format(ctrl_root))

            cmds.delete(cmds.parentConstraint(vtx_root, ctrl))
            cmds.parent(vtx_root, vtx_joints_grp)

        #Create controller for main controllers
        five_curve = cmds.duplicate(linear_curve, n=name + '_WireDriver' + nc['curve'])[0]
        mel.eval('rebuildCurve -ch 1 -rpo 1 -rt 0 -end 1 -kr 0'
                 ''
                 ''
                 ' -kcp 0 -kep 1 -kt 0 -s 4 -d 3 -tol 0.01 "{}";'.format(five_curve))
        five_curve_shape = cmds.listRelatives(five_curve, s=True)[0]

        wire = mel.eval(
            'wire -n "{}_Wire" -gw false -en 1.000000 -ce 0.000000 -li 0.000000 -w {} {};'.format(name, five_curve,
                                                                                                  linear_curve))
        cmds.setAttr('{}.dropoffDistance[0]'.format(wire[0]), 999)
        wire_base = wire[1] + 'BaseWire'

        # Create 5 controllers to manipulate main curve
        cv_to_add_ctrl_to = ['{}.cv[0]'.format(five_curve),
                             '{}.cv[1]'.format(five_curve),
                             '{}.cv[2]'.format(five_curve),
                             '{}.cv[3]'.format(five_curve),
                             '{}.cv[4]'.format(five_curve),
                             '{}.cv[5]'.format(five_curve),
                             '{}.cv[6]'.format(five_curve),
                             ]
        main_ctrl_names = [nc['right'],
                           nc['right']+'Mid_02',
                           nc['right']+'Mid_01',
                           '_Mid',
                           nc['left']+'Mid_01',
                           nc['left']+'Mid_02',
                           nc['left']
                           ]
        sec_ctrls = []
        sec_ctrls_roots = []

        sec_jnts = []
        sec_jnts_roots = []

        main_joint_grp = cmds.group(em=True, n='{}{}{}'.format(name, nc['joint'], nc['group']))

        for num, cv in enumerate(cv_to_add_ctrl_to):
            cmds.select(cv)
            temp_cls = cmds.cluster()
            ctrl = mt.curve(input=temp_cls,
                            type='circleZ',
                            rename=True,
                            custom_name=True,
                            name=main_ctrl_names[num]+name+nc['ctrl'],
                            size=ctrl_size / 2)
            sec_ctrls.append(ctrl)
            mt.assign_color(color=color)
            ctrl_root = mt.root_grp()[0]
            sec_ctrls_roots.append(ctrl_root)
            cmds.parent(ctrl_root, main_ctrl_grp)
            mt.match(ctrl_root, temp_cls, r=True, t=True)
            # cmds.delete(cmds.aimConstraint(eye_pivot, ctrl_root,
            #                    aimVector= (0, 0, -1), upVector =(0, 1, 0),
            #                    worldUpType="object", worldUpObject=eye_up_vector_locator))
            cmds.delete(temp_cls)

            cmds.select(cl=True)
            jnt = cmds.joint(n=name + main_ctrl_names[num] + nc['joint'])
            sec_jnts.append(jnt)
            mt.match(jnt, ctrl, r=True, t=True)
            jnt_root = mt.root_grp()[0]
            sec_jnts_roots.append(jnt_root)
            cmds.parent(jnt_root, main_joint_grp)
            cmds.connectAttr('{}.rotate'.format(ctrl), '{}.rotate'.format(jnt))
            cmds.connectAttr('{}.translate'.format(ctrl), '{}.translate'.format(jnt))
            cmds.connectAttr('{}.scale'.format(ctrl), '{}.scale'.format(jnt))

        cmds.delete(cmds.aimConstraint(sec_ctrls[3], sec_ctrls_roots[1], aimVector=(1, 0, 0), upVector=(0, 1, 0), worldUpType = 'vector', mo = False))
        cmds.delete(cmds.aimConstraint(sec_ctrls[3], sec_ctrls_roots[2], aimVector=(1, 0, 0), upVector=(0, 1, 0), worldUpType = 'vector', mo = False))
        cmds.delete(cmds.aimConstraint(sec_ctrls[3], sec_ctrls_roots[4], aimVector=(-1, 0, 0), upVector=(0, 1, 0), worldUpType = 'vector', mo = False))
        cmds.delete(cmds.aimConstraint(sec_ctrls[3], sec_ctrls_roots[5], aimVector=(-1, 0, 0), upVector=(0, 1, 0), worldUpType = 'vector', mo = False))

        cmds.delete(cmds.aimConstraint(sec_jnts[3], sec_jnts_roots[1], aimVector=(1, 0, 0), upVector=(0, 1, 0), worldUpType = 'vector', mo = False))
        cmds.delete(cmds.aimConstraint(sec_jnts[3], sec_jnts_roots[2], aimVector=(1, 0, 0), upVector=(0, 1, 0), worldUpType = 'vector', mo = False))
        cmds.delete(cmds.aimConstraint(sec_jnts[3], sec_jnts_roots[4], aimVector=(-1, 0, 0), upVector=(0, 1, 0), worldUpType = 'vector', mo = False))
        cmds.delete(cmds.aimConstraint(sec_jnts[3], sec_jnts_roots[5], aimVector=(-1, 0, 0), upVector=(0, 1, 0), worldUpType = 'vector', mo = False))

        cmds.skinCluster(sec_jnts, five_curve, sm=0, bm=1, tsb=True)

        cmds.parent(mt.mirror_group(sec_ctrls_roots[0], world = False),main_ctrl_grp)
        cmds.parent(mt.mirror_group(sec_ctrls_roots[1], world = False),main_ctrl_grp)
        cmds.parent(mt.mirror_group(sec_ctrls_roots[2], world = False),main_ctrl_grp)
        cmds.parent(mt.mirror_group(sec_jnts[0], world = False),main_joint_grp)
        cmds.parent(mt.mirror_group(sec_jnts[1], world = False),main_joint_grp)
        cmds.parent(mt.mirror_group(sec_jnts[2], world = False),main_joint_grp)

        #Create Main Controller
        main_loc = cmds.spaceLocator(n = name + '_Main' + nc['locator'])[0]
        main_loc_root = mt.root_grp()[0]
        cmds.delete(cmds.parentConstraint(sec_ctrls[3], main_loc_root))

        cmds.select(sec_ctrls[3])
        main_ctrl = mt.curve(input='',
                        type='square',
                        rename=True,
                        custom_name=True,
                        name=name + '_Main' + nc['ctrl'],
                        size=ctrl_size)

        mt.assign_color(color=color)
        main_ctrl_root = mt.root_grp()[0]
        cmds.parent(main_ctrl_root, main_ctrl_grp)

        cmds.connectAttr('{}.rotate'.format(end_locator), '{}.rotate'.format(ctrl_root))
        cmds.connectAttr('{}.translate'.format(end_locator), '{}.translate'.format(ctrl_root))

        cmds.select(
        '{}.cv[0:1]'.format(main_ctrl),
        '{}.cv[4]'.format(main_ctrl)
        )
        cmds.rotate(90,0,0,r=True)
        cmds.move(0,0,ctrl_size*1.5,r=True)
        temp_clusterB=cmds.cluster()
        cmds.delete(cmds.pointConstraint(sec_jnts[4],temp_clusterB))
        cmds.delete(main_ctrl, ch=True)

        cmds.select(
        '{}.cv[2:3]'.format(main_ctrl)
        )
        cmds.rotate(90,0,0,r=True)
        cmds.move(0,0,ctrl_size*1.5,r=True)
        temp_clusterB=cmds.cluster()
        cmds.delete(cmds.pointConstraint(sec_jnts[2],temp_clusterB))
        cmds.delete(main_ctrl, ch=True)

        return {
                'main_controllers_grp': main_ctrl_grp,
                'main_ctrl':main_ctrl,
                'main_ctrl_root' : main_ctrl_root,
                'sec_controllers' : sec_ctrls,
                'sec_ctrls_roots' : sec_ctrls_roots,
                'linear_curve' : linear_curve,
                'smooth_curve' : five_curve,
                'wire_base' : wire_base,
                'follow_locs_grp' : locators_grp,
                'tweek_joints_groups' : vtx_joints_grp,
                'sec_joints': sec_jnts,
                'sec_joints_roots':sec_jnts_roots,
                'sec_joints_group': main_joint_grp,
                'main_locator':main_loc,
                'main_locator_root': main_loc_root,
                'aim_locators':vtx_locators,
                'tweek_joints': vtx_joints,
                'tweek_ctrls':tweek_controllers
                }

    #---------------------------------------------------------------------
    #---------------------------------------------------------------------

    upper_system = create_lips_system(name=name + '_Up',
                                     edge=upper_edge,
                                     color = 'green'
                                     )

    lower_system = create_lips_system(name=name + '_Dw',
                                     edge=lower_edge,
                                     color = 'purple')

    #Clean Groups
    clean_ctrl_grp = cmds.group(em=True, name=name + nc['ctrl'] + nc['group'])
    clean_rig_grp = cmds.group(em=True, name=name + '_Rig' + nc['group'])


    #Create Side Controllers
    # Create Main Controller
    side_controllers = []
    side_locators=[]
    for side in [nc['left'], nc['right']]:
        loc = cmds.spaceLocator(n=side + name + '_Main' + nc['locator'])[0]
        loc_root = mt.root_grp()[0]
        cmds.delete(cmds.parentConstraint(upper_system['sec_controllers'][-1], loc_root))

        side_main_ctrl = mt.curve(input='',
                             type='square',
                             rename=True,
                             custom_name=True,
                             name=side + name + '_Main' + nc['ctrl'],
                             size=ctrl_size)
        if side == nc['right']:
            mt.assign_color(color='red')
        else:
            mt.assign_color(color='blue')
        left_main_ctrl_root = mt.root_grp()[0]

        cmds.connectAttr('{}.rotate'.format(side_main_ctrl), '{}.rotate'.format(loc))
        cmds.connectAttr('{}.translate'.format(side_main_ctrl), '{}.translate'.format(loc))
        cmds.select('{}.cv[0:4]'.format(side_main_ctrl))
        cmds.rotate(90,0,0,r=True)
        cmds.select('{}.cv[2:3]'.format(side_main_ctrl))
        cmds.scale(0,ctrl_size/3,0,r=True)
        cmds.move(ctrl_size/2,0,0,r=True)

        side_controllers.append(side_main_ctrl)
        side_locators.append(loc)

        if side == nc['right']:
            loc_root = mt.mirror_group(loc_root, world=True)
            left_main_ctrl_root = mt.mirror_group(left_main_ctrl_root, world=True)

        cmds.parent(loc_root, clean_rig_grp)
        cmds.parent(left_main_ctrl_root, clean_ctrl_grp)

    #for ctrl, loc in zip(upper_system['sec_joints'], upper_system['sec_controllers'] ):
    #    print(ctrl, loc)

    #Make them follow corners an tops
    for system in [upper_system, lower_system]:
        joints = system['sec_joints']
        joints_roots = system['sec_joints_roots']
        ctrls = system['sec_controllers']
        ctrls_roots = system['sec_ctrls_roots']

        main_ctrl = system['main_ctrl']
        main_loc = system['main_locator']

        left_ctrl = side_controllers[0]
        right_ctrl = side_controllers[1]

        left_locator = side_locators[0]
        right_locator = side_locators[1]

        #hardcoding stuff couse i didnt find a nice way sorry :)

        cmds.parentConstraint(left_ctrl, ctrls_roots[-1], mo=True)
        cmds.parentConstraint(left_locator, cmds.listRelatives(joints[-1], p=True)[0], mo=True)

        cmds.parentConstraint(right_ctrl, ctrls_roots[0], mo=True)
        cmds.parentConstraint(right_locator, cmds.listRelatives(joints[0], p=True)[0], mo=True)

        cmds.parentConstraint(main_ctrl, ctrls_roots[3], mo=True)
        cmds.parentConstraint(main_loc, cmds.listRelatives(joints[3], p=True)[0], mo=True)

        pc = cmds.parentConstraint(main_ctrl, left_ctrl, ctrls_roots[-2], mo=True)[0]
        cmds.setAttr('{}.interpType'.format(pc), 2)
        cmds.setAttr("{}.{}W1".format(pc, left_ctrl), 2)

        pc = cmds.parentConstraint(main_loc, left_locator, cmds.listRelatives(joints[-2], p=True)[0], mo=True)[0]
        cmds.setAttr('{}.interpType'.format(pc), 2)
        cmds.setAttr("{}.{}W1".format(pc, left_locator), 2)

        pc = cmds.parentConstraint(main_ctrl, left_ctrl, ctrls_roots[-3], mo=True)[0]
        cmds.setAttr('{}.interpType'.format(pc), 2)
        cmds.setAttr("{}.{}W0".format(pc, main_ctrl), 2)

        pc = cmds.parentConstraint(main_loc, left_locator, cmds.listRelatives(joints[-3], p=True)[0], mo=True)[0]
        cmds.setAttr('{}.interpType'.format(pc), 2)
        cmds.setAttr("{}.{}W0".format(pc, main_loc), 2)

        #--------------------------
        pc = cmds.parentConstraint(main_ctrl, right_ctrl, ctrls_roots[1], mo=True)[0]
        cmds.setAttr('{}.interpType'.format(pc), 2)
        cmds.setAttr("{}.{}W1".format(pc, right_ctrl), 2)

        pc = cmds.parentConstraint(main_loc, right_locator, cmds.listRelatives(joints[1], p=True)[0], mo=True)[0]
        cmds.setAttr('{}.interpType'.format(pc), 2)
        cmds.setAttr("{}.{}W1".format(pc, right_locator), 2)

        pc = cmds.parentConstraint(main_ctrl, right_ctrl, ctrls_roots[2], mo=True)[0]
        cmds.setAttr('{}.interpType'.format(pc), 2)
        cmds.setAttr("{}.{}W0".format(pc, main_ctrl), 2)

        pc = cmds.parentConstraint(main_loc, right_locator, cmds.listRelatives(joints[2], p=True)[0], mo=True)[0]
        cmds.setAttr('{}.interpType'.format(pc), 2)
        cmds.setAttr("{}.{}W0".format(pc, main_loc), 2)

    #Aim locators look to corners
    # right_up_vector_locator = cmds.spaceLocator(n=nc['right']+name + "_UpVector" + nc['locator'])[0]
    # cmds.delete(cmds.parentConstraint(right_locator,right_up_vector_locator))
    # cmds.move(0,ctrl_size*2,0,r=True)
    # cmds.parentConstraint(right_locator, right_up_vector_locator, mo=True)
    #
    # left_up_vector_locator = cmds.spaceLocator(n=nc['left']+name + "_UpVector" + nc['locator'])[0]
    # cmds.delete(cmds.parentConstraint(left_locator,left_up_vector_locator))
    # cmds.move(0,ctrl_size*2,0,r=True)
    # cmds.parentConstraint(left_locator, left_up_vector_locator, mo=True)
    #forward locators
    for system in [upper_system, lower_system]:
        aim_locators = system['aim_locators']
        for num, loc in enumerate(aim_locators):
            x_value = cmds.getAttr('{}.translateX'.format(loc))
            #Right Side
            if x_value < 0:
                if loc == aim_locators[0]:
                    cmds.orientConstraint(right_ctrl, loc, mo=True)
                    continue
                # cmds.aimConstraint(aim_locators[num-1], loc, aimVector=(1, 0, 0), upVector=(0, 1, 0), worldUpType="object", worldUpObject=right_up_vector_locator, mo=True)
                cmds.aimConstraint(aim_locators[num-1], loc, aimVector=(1, 0, 0), upVector=(0, 1, 0), worldUpType = 'vector', mo=True)

            #Left Side
            if x_value > 0:
                if loc == aim_locators[-1]:
                    cmds.orientConstraint(left_ctrl, loc, mo=True)
                    continue
                # cmds.aimConstraint(aim_locators[num-1], loc, aimVector=(1, 0, 0), upVector=(0, 1, 0), worldUpType="object", worldUpObject=left_up_vector_locator, mo=True)
                cmds.aimConstraint(aim_locators[num+1], loc, aimVector=(1, 0, 0), upVector=(0, 1, 0), worldUpType = 'vector', mo=True)


    #Visibility switches
    # hide ctrls
    if attrs_position == 'new_locator':
        guide_attrs_position = cmds.spaceLocator(n=name + '_Attrs' + nc['locator'])[0]

    mt.line_attr(input=guide_attrs_position, name='Mouth_Vis')
    main_ctrl_attr = mt.new_enum(input=guide_attrs_position, name='lipsMainCtrls', enums='Hide:Show')
    mid_ctrl_attr = mt.new_enum(input=guide_attrs_position, name='lipsMidCtrls', enums='Hide:Show')
    show_tweeks_attr = mt.new_enum(input=guide_attrs_position, name='lipsTweekCtrls', enums='Hide:Show')

    cmds.setAttr(main_ctrl_attr, 1)

    for system in [upper_system, lower_system]:
        for ctrl in system['sec_controllers']:
            shape = cmds.listRelatives(ctrl, s=True)[0]
            cmds.connectAttr(mid_ctrl_attr, '{}.v'.format(shape))
        for ctrl in system['tweek_ctrls']:
            shape = cmds.listRelatives(ctrl, s=True)[0]
            cmds.connectAttr(show_tweeks_attr, '{}.v'.format(shape))
        for ctrl in [system['main_ctrl']]:
            shape = cmds.listRelatives(ctrl, s=True)[0]
            cmds.connectAttr(main_ctrl_attr, '{}.v'.format(shape))

    for ctrl in [left_ctrl, right_ctrl]:
        shape = cmds.listRelatives(ctrl, s=True)[0]
        cmds.connectAttr(main_ctrl_attr, '{}.v'.format(shape))

    #Clean a bit
    cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
    cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])

    for system in [upper_system, lower_system]:
        cmds.parent(system['linear_curve'], system['smooth_curve'],
                    system['wire_base'], system['follow_locs_grp'],
                    system['tweek_joints_groups'], system['sec_joints_group'],
                    system['main_locator_root'],
                    #right_up_vector_locator, left_up_vector_locator,
                    clean_rig_grp)

        cmds.parent(system['main_controllers_grp'], clean_ctrl_grp)

    # create bind joints
    bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])
    for jnt in upper_system['tweek_joints'] + lower_system['tweek_joints']:
        cmds.select(cl=True)
        bind_joint = cmds.joint(n=jnt.replace(nc['joint'], nc['joint_bind']))
        cmds.parentConstraint(jnt, bind_joint)
        cmds.scaleConstraint(jnt, bind_joint)
        cmds.setAttr('{}.radius'.format(bind_joint), 1.5)
        cmds.parent(bind_joint, bind_jnt_grp)