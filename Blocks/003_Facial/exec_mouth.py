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

from Mutant_Tools.UI.FaceInstall.faceinstall_utils import postbuilds_faceinstall
reload(postbuilds_faceinstall) 

#---------------------------------------------

TAB_FOLDER = '003_Facial'
PYBLOCK_NAME = 'exec_mouth'

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

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '003_Mouth.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()

    # name checks and block creation
    name = mt.ask_name(text=module['Name'])
    if cmds.objExists('{}{}'.format(name, nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name=name, icon='Lips', attrs=module['attrs'], build_command=module['build_command'],
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
            cmds.select('{}.cv[{}]'.format(linear_curve, linear_curve_cvs))
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
            #cmds.connectAttr('{}.translate'.format(end_locator), '{}.translate'.format(ctrl_root))

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

        cmds.delete(cmds.aimConstraint(sec_ctrls[3], sec_ctrls_roots[1], aimVector=(1, 0, 0), upVector=(0, 1, 0), worldUpType = 'vector', mo = False, skip=['z']))
        cmds.delete(cmds.aimConstraint(sec_ctrls[3], sec_ctrls_roots[2], aimVector=(1, 0, 0), upVector=(0, 1, 0), worldUpType = 'vector', mo = False, skip=['z']))
        cmds.delete(cmds.aimConstraint(sec_ctrls[3], sec_ctrls_roots[4], aimVector=(-1, 0, 0), upVector=(0, 1, 0), worldUpType = 'vector', mo = False, skip=['z']))
        cmds.delete(cmds.aimConstraint(sec_ctrls[3], sec_ctrls_roots[5], aimVector=(-1, 0, 0), upVector=(0, 1, 0), worldUpType = 'vector', mo = False, skip=['z']))

        cmds.delete(cmds.aimConstraint(sec_jnts[3], sec_jnts_roots[1], aimVector=(1, 0, 0), upVector=(0, 1, 0), worldUpType = 'vector', mo = False, skip=['z']))
        cmds.delete(cmds.aimConstraint(sec_jnts[3], sec_jnts_roots[2], aimVector=(1, 0, 0), upVector=(0, 1, 0), worldUpType = 'vector', mo = False, skip=['z']))
        cmds.delete(cmds.aimConstraint(sec_jnts[3], sec_jnts_roots[4], aimVector=(-1, 0, 0), upVector=(0, 1, 0), worldUpType = 'vector', mo = False, skip=['z']))
        cmds.delete(cmds.aimConstraint(sec_jnts[3], sec_jnts_roots[5], aimVector=(-1, 0, 0), upVector=(0, 1, 0), worldUpType = 'vector', mo = False, skip=['z']))

        cmds.skinCluster(sec_jnts, five_curve, sm=0, bm=1, tsb=True)
        # sm = 0 - classical linear skinning (default). 1 - dual quaternion (volume preserving), 2 - a weighted blend between the two
        # bm = 1 - Closest distance between a joint, considering the skeleton hierarchy, and a point of the geometry. 2 - Surface heat map diffusion. 3 - Geodesic voxel binding. geomBind

        cmds.parent(mt.mirror_group(sec_ctrls_roots[0], world = False),main_ctrl_grp)
        cmds.parent(mt.mirror_group(sec_ctrls_roots[1], world = False),main_ctrl_grp)
        cmds.parent(mt.mirror_group(sec_ctrls_roots[2], world = False),main_ctrl_grp)
        cmds.parent(mt.mirror_group(sec_jnts[0], world = False),main_joint_grp)
        cmds.parent(mt.mirror_group(sec_jnts[1], world = False),main_joint_grp)
        cmds.parent(mt.mirror_group(sec_jnts[2], world = False),main_joint_grp)

        #Create Main Controller
        main_loc = cmds.spaceLocator(n = name + '_Main' + nc['locator'])[0]
        main_loc_root, main_loc_auto = mt.root_grp(autoRoot=True)
        cmds.delete(cmds.parentConstraint(sec_ctrls[3], main_loc_root))
        cmds.select(main_loc_auto)
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

        cmds.connectAttr('{}.rotate'.format(main_ctrl), '{}.rotate'.format(main_loc))
        cmds.connectAttr('{}.translate'.format(main_ctrl), '{}.translate'.format(main_loc))
        cmds.connectAttr('{}.scale'.format(main_ctrl), '{}.scale'.format(main_loc))

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

        #----------------------------
        #----------------------------
        #----------------------------
        #Create lip rolls
        def findMiddle(input_list):
            middle = float(len(input_list)) / 2
            if middle % 2 != 0:
                return input_list[int(middle - .5)]
            else:
                return (input_list[int(middle)], input_list[int(middle - 1)])

        middle_joint = findMiddle(vtx_locators)

        def split(a, n):
            k, m = divmod(len(a), n)
            return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))

        right_side_list, left_side_list = list(split(vtx_locators, 2))

        if not type(middle_joint) == type(()):
            left_side_list.insert(0, middle_joint)
        print(middle_joint, right_side_list, left_side_list)


        for num, loc in enumerate(reversed(left_side_list)):
            lip_grp = cmds.group(loc, name = loc.replace(nc['locator'],'_Roll'+nc['group']))
            md = mt.connect_md_node(in_x1=main_ctrl+'.rotateX', in_x2=num*0.1, out_x= lip_grp+'.rotateX', mode='multiply')
            cmds.connectAttr("{}.rotatePivot".format(main_ctrl), "{}.rotatePivot".format(lip_grp), f=True)
            cmds.connectAttr("{}.scalePivot".format(main_ctrl), "{}.scalePivot".format(lip_grp), f=True)
            cmds.connectAttr('{}.translate'.format(loc), "{}.rotatePivot".format(lip_grp), f=True)
            cmds.connectAttr('{}.translate'.format(loc), "{}.scalePivot".format(lip_grp), f=True)

        for num, loc in enumerate(right_side_list):
            if cmds.objExists(loc.replace(nc['locator'], '_Roll' + nc['group'])):
                continue
            lip_grp = cmds.group(loc, name=loc.replace(nc['locator'], '_Roll' + nc['group']))
            # Lips_Dw_0_Locq
            md = mt.connect_md_node(in_x1=main_ctrl+'.rotateX', in_x2=num*0.1, out_x= lip_grp+'.rotateX', mode='multiply')

            cmds.connectAttr('{}.translate'.format(loc), "{}.rotatePivot".format(lip_grp), f=True)
            cmds.connectAttr('{}.translate'.format(loc), "{}.scalePivot".format(lip_grp), f=True)

        #----------------------------
        #----------------------------
        #----------------------------
        search_amount = (len(vtx_locators) // len(sec_ctrls)) + 2

        def get_closest(ctrl, locators, amount):

            distances=[]
            for loc in locators:
                distance = mt.get_distance_between(ctrl, loc)
                distances.append(distance)

            distances.sort()

            distances = distances[:amount]
            return_list = []
            for d in distances:
                for loc in locators:
                    distance = mt.get_distance_between(ctrl, loc)
                    if d == distance:
                        return_list.append(loc)

            return return_list


        print('#'*50)
        for ctrl in sec_ctrls[1:-1]:
            closest = get_closest(ctrl, vtx_locators, search_amount)
            print(ctrl, closest)
            for loc in closest:
                lip_grp = cmds.group(loc, name=loc.replace(nc['locator'], '_Roll_{}'.format(ctrl) + nc['group']))
                # Lips_Dw_0_Loc
                md = mt.connect_md_node(in_x1=ctrl + '.rotateX', in_x2=mt.get_distance_between(ctrl, loc)+0.01, out_x=lip_grp+'.rotateX',
                                        mode='divide')
                md = mt.connect_md_node(in_x1=ctrl + '.rotateY', in_x2=mt.get_distance_between(ctrl, loc)+0.01, out_x=lip_grp+'.rotateY',
                                        mode='divide')
                md = mt.connect_md_node(in_x1=ctrl + '.rotateZ', in_x2=mt.get_distance_between(ctrl, loc)+0.01, out_x=lip_grp+'.rotateZ',
                                        mode='divide')
                #relocate the pivotrs
                cmds.connectAttr('{}.translate'.format(loc), "{}.rotatePivot".format(lip_grp), f=True)
                cmds.connectAttr('{}.translate'.format(loc), "{}.scalePivot".format(lip_grp), f=True)

        #----------------------------
        #----------------------------
        #----------------------------

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
                                     color = 'yellow'
                                     )

    lower_system = create_lips_system(name=name + '_Dw',
                                     edge=lower_edge,
                                     color = 'purple')

    #Clean Groups
    clean_ctrl_grp = cmds.group(em=True, name=name + nc['ctrl'] + nc['group'])
    clean_rig_grp = cmds.group(em=True, name=name + '_Rig' + nc['group'])

    #Main Mouth Controller
    center_grp = cmds.group(em=True, n=name+'_Center'+nc['group'])
    cmds.delete(cmds.parentConstraint(mouth_center, center_grp))
    center_root = mt.root_grp()[0]
    center_lips_grp = cmds.group(em=True, n=name+'_Centerlips'+nc['group'])
    cmds.delete(cmds.parentConstraint(center_grp, center_lips_grp))
    center_lips_root = mt.root_grp()[0]
    cmds.parent(center_lips_root, center_grp)

    center_ctrl =  mt.curve(input=center_grp,
                            type='octagon',
                            rename=True,
                            custom_name=True,
                            name=name+'_Center'+nc['ctrl'],
                            size=ctrl_size)
    mt.assign_color(color='lightBlue')
    center_ctrl_root = mt.root_grp()[0]
    cmds.delete(cmds.parentConstraint(mouth_center, center_ctrl_root))
    cmds.select(center_ctrl + '.cv[0:8]')
    cmds.rotate(90,0,0)
    center_cluster = cmds.cluster()
    cmds.delete(cmds.parentConstraint(upper_system['main_ctrl'], center_cluster))
    cmds.delete(center_ctrl, ch=True)

    cmds.connectAttr('{}.translate'.format(center_ctrl), '{}.translate'.format(center_grp))
    cmds.connectAttr('{}.rotate'.format(center_ctrl), '{}.rotate'.format(center_grp))
    cmds.connectAttr('{}.scale'.format(center_ctrl), '{}.scale'.format(center_grp))

    center_lips_ctrl =  mt.curve(input=center_grp,
                            type='octagon',
                            rename=True,
                            custom_name=True,
                            name=name+'_Centerlips'+nc['ctrl'],
                            size=ctrl_size*0.75)
    mt.assign_color(color='lightBlue')
    center_lips_ctrl_root = mt.root_grp()[0]
    cmds.delete(cmds.parentConstraint(mouth_center, center_lips_ctrl_root))
    cmds.select(center_lips_ctrl + '.cv[0:8]')
    cmds.rotate(90,0,0)
    center_cluster = cmds.cluster()
    cmds.delete(cmds.parentConstraint(upper_system['main_ctrl'], center_cluster))
    cmds.delete(center_lips_ctrl, ch=True)

    cmds.connectAttr('{}.translate'.format(center_lips_ctrl), '{}.translate'.format(center_lips_grp))
    cmds.connectAttr('{}.rotate'.format(center_lips_ctrl), '{}.rotate'.format(center_lips_grp))
    cmds.connectAttr('{}.scale'.format(center_lips_ctrl), '{}.scale'.format(center_lips_grp))

    cmds.parent(center_lips_ctrl_root, center_ctrl)


    #Create Side Controllers
    # Create Main Controller
    side_controllers = []
    side_locators = []
    sub_side_controllers = []

    for side in [nc['left'], nc['right']]:
        loc = cmds.spaceLocator(n=side + name + '_Main' + nc['locator'])[0]
        loc_root, loc_auto = mt.root_grp(autoRoot=True)
        cmds.delete(cmds.parentConstraint(upper_system['sec_controllers'][-1], loc_root))
        cmds.delete(cmds.orientConstraint(orient_guide, loc_root))

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

        #Attrs
        mt.line_attr(input=side_main_ctrl, name='Lips')
        mode_attr = mt.new_enum(input=side_main_ctrl, name='mode', enums='BSP:RIG')
        move_mult_attr = mt.new_attr(input=side_main_ctrl, name='MovementMult', min=0.1, max=10, default=1)
        sub_move_mult_attr = mt.new_attr(input=side_main_ctrl, name='SubMovementMult', min=0.1, max=10, default=1)

        #Make pretty
        cmds.select('{}.cv[0:4]'.format(side_main_ctrl))
        cmds.rotate(90,0,0,r=True)
        #cmds.select('{}.cv[2:3]'.format(side_main_ctrl))
        #cmds.scale(0,ctrl_size/3,0,r=True)
        #cmds.move(ctrl_size/2,0,0,r=True)
        mt.hide_attr(side_main_ctrl, s=True)

        side_controllers.append(side_main_ctrl)
        side_locators.append(loc)


        #----------SUB-----------------------------------------
        #create sub controller with modes in case we dont use BS
        sub_main_ctrl = mt.curve(input='',
                             type='square',
                             rename=True,
                             custom_name=True,
                             name=side + name + '_Sub' + nc['ctrl'],
                             size=ctrl_size/3)
        sub_side_controllers.append(sub_main_ctrl)
        if side == nc['right']:
            mt.assign_color(color='red')
        else:
            mt.assign_color(color='blue')
        left_sub_ctrl_root = mt.root_grp()[0]

        cmds.select('{}.cv[0:4]'.format(sub_main_ctrl))
        cmds.rotate(90,0,0,r=True)
        # cmds.select('{}.cv[2:3]'.format(sub_main_ctrl))
        # cmds.scale(0,ctrl_size/4,0,r=True)
        # cmds.move(ctrl_size/2,0,0,r=True)
        mt.hide_attr(sub_main_ctrl, s=True)
        # cmds.select('{}.cv[0:4]'.format(sub_main_ctrl))
        # cmds.scale(ctrl_size/4,ctrl_size/4,ctrl_size/4,r=True)

        cmds.parent(left_sub_ctrl_root, side_main_ctrl)

        #direct connect with mult
        mt.connect_md_node(in_x1=sub_move_mult_attr, in_x2='{}.rotate'.format(sub_main_ctrl), out_x= '{}.rotate'.format(loc), mode='multiply', vector=True)
        mt.connect_md_node(in_x1=sub_move_mult_attr, in_x2='{}.translate'.format(sub_main_ctrl), out_x= '{}.translate'.format(loc), mode='multiply', vector=True)
        #mt.connect_md_node(in_x1=sub_move_mult_attr, in_x2='{}.scale'.format(sub_main_ctrl), out_x= '{}.scale'.format(loc), mode='multiply', vector=True )

        #-----------------------------------------------------
        #Connect main siude ctrl
        md_rotate = mt.connect_md_node(in_x1=move_mult_attr, in_x2='{}.rotate'.format(side_main_ctrl), out_x= '{}.rotate'.format(loc_auto), mode='multiply', vector=True)
        md_translate = mt.connect_md_node(in_x1=move_mult_attr, in_x2='{}.translate'.format(side_main_ctrl), out_x= '{}.translate'.format(loc_auto), mode='multiply', vector=True)
        #md_scale = mt.connect_md_node(in_x1=move_mult_attr, in_x2='{}.scale'.format(side_main_ctrl), out_x= '{}.scale'.format(loc_auto), mode='multiply', vector=True )

        mt.connect_md_node(in_x1=mode_attr, in_x2='{}.output'.format(md_rotate), out_x= '{}.rotate'.format(loc_auto), mode='multiply', vector=True, force=True)
        mt.connect_md_node(in_x1=mode_attr, in_x2='{}.output'.format(md_translate), out_x= '{}.translate'.format(loc_auto), mode='multiply', vector=True, force=True)
        #mt.connect_md_node(in_x1=mode_attr, in_x2='{}.output'.format(md_scale), out_x= '{}.scale'.format(loc_auto), mode='multiply', vector=True, force=True)


        #Flip
        if side == nc['right']:
            loc_root = mt.mirror_group(loc_root, world=True)
            left_main_ctrl_root = mt.mirror_group(left_main_ctrl_root, world=True)

        #cmds.parent(loc_root, clean_rig_grp)
        cmds.parent(loc_root, center_grp)
        #cmds.parent(left_main_ctrl_root, clean_ctrl_grp)
        cmds.parent(left_main_ctrl_root, center_ctrl)

    #--------------------------------------------------------------------------

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

        left_sub_ctrl = sub_side_controllers[0]
        right_sub_ctrl = sub_side_controllers[1]

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
        cmds.setAttr("{}.{}W1".format(pc, left_ctrl), 3)

        pc = cmds.parentConstraint(main_loc, left_locator, cmds.listRelatives(joints[-2], p=True)[0], mo=True)[0]
        cmds.setAttr('{}.interpType'.format(pc), 2)
        cmds.setAttr("{}.{}W1".format(pc, left_locator), 3)

        pc = cmds.parentConstraint(main_ctrl, left_ctrl, ctrls_roots[-3], mo=True)[0]
        cmds.setAttr('{}.interpType'.format(pc), 2)
        cmds.setAttr("{}.{}W0".format(pc, main_ctrl), 3)

        pc = cmds.parentConstraint(main_loc, left_locator, cmds.listRelatives(joints[-3], p=True)[0], mo=True)[0]
        cmds.setAttr('{}.interpType'.format(pc), 2)
        cmds.setAttr("{}.{}W0".format(pc, main_loc), 3)

        #--------------------------
        pc = cmds.parentConstraint(main_ctrl, right_ctrl, ctrls_roots[1], mo=True)[0]
        cmds.setAttr('{}.interpType'.format(pc), 2)
        cmds.setAttr("{}.{}W1".format(pc, right_ctrl), 3)

        pc = cmds.parentConstraint(main_loc, right_locator, cmds.listRelatives(joints[1], p=True)[0], mo=True)[0]
        cmds.setAttr('{}.interpType'.format(pc), 2)
        cmds.setAttr("{}.{}W1".format(pc, right_locator), 3)

        pc = cmds.parentConstraint(main_ctrl, right_ctrl, ctrls_roots[2], mo=True)[0]
        cmds.setAttr('{}.interpType'.format(pc), 2)
        cmds.setAttr("{}.{}W0".format(pc, main_ctrl), 3)

        pc = cmds.parentConstraint(main_loc, right_locator, cmds.listRelatives(joints[2], p=True)[0], mo=True)[0]
        cmds.setAttr('{}.interpType'.format(pc), 2)
        cmds.setAttr("{}.{}W0".format(pc, main_loc), 3)

    #Aim locators look to corners
    right_up_vector_locator = cmds.spaceLocator(n=nc['right']+name + "_UpVector" + nc['locator'])[0]
    cmds.delete(cmds.parentConstraint(right_locator,right_up_vector_locator))
    cmds.move(0,ctrl_size*2,0,r=True)
    cmds.parentConstraint(right_locator, main_loc, right_up_vector_locator, mo=True)

    left_up_vector_locator = cmds.spaceLocator(n=nc['left']+name + "_UpVector" + nc['locator'])[0]
    cmds.delete(cmds.parentConstraint(left_locator,left_up_vector_locator))
    cmds.move(0,ctrl_size*2,0,r=True)
    cmds.parentConstraint(left_locator, main_loc, left_up_vector_locator, mo=True)

    #forward locators
    left_rotation_mul_attr = mt.new_attr(input=side_controllers[0], name='SubAutoRotation', min=0, max=1, default=0.25)
    right_rotation_mul_attr = mt.new_attr(input=side_controllers[1], name='SubAutoRotation', min=0, max=1, default=0.25)

    for system in [upper_system, lower_system]:
        aim_locators = system['aim_locators']
        for num, loc in enumerate(aim_locators):
            print(loc)
            x_value = cmds.getAttr('{}.translateX'.format(loc))
            #Right Side
            if x_value < 0:
                #cmds.aimConstraint(aim_locators[num-1], loc, aimVector=(1, 0, 0), upVector=(0, 1, 0), worldUpType="object", worldUpObject=right_up_vector_locator, mo=True)
                #cmds.aimConstraint(aim_locators[num-1], loc, aimVector=(1, 0, 0), upVector=(0, 1, 0), worldUpType = 'vector', mo=True)
                md = mt.connect_md_node(in_x1=right_sub_ctrl+'.rotateZ', in_x2=x_value, out_x= loc+'.rotateZ', mode='multiply')
                mt.connect_md_node(in_x1=x_value, in_x2=right_rotation_mul_attr, out_x= md+'.input2X', mode='multiply')

        for num, loc in reversed(list(enumerate(aim_locators))):
            print(loc)
            x_value = cmds.getAttr('{}.translateX'.format(loc))
            #Left Sideq
            if x_value > 0:
                #cmds.aimConstraint(aim_locators[num+1], loc, aimVector=(1, 0, 0), upVector=(0, 1, 0), worldUpType="object", worldUpObject=left_up_vector_locator, mo=True)
                #cmds.aimConstraint(aim_locators[num+1], loc, aimVector=(1, 0, 0), upVector=(0, 1, 0), worldUpType = 'vector', mo=True)
                md = mt.connect_md_node(in_x1=left_sub_ctrl+'.rotateZ', in_x2=x_value, out_x= loc+'.rotateZ', mode='multiply')
                mt.connect_md_node(in_x1=x_value, in_x2=left_rotation_mul_attr, out_x= md+'.input2X', mode='multiply')

    #Visibility switches
    # hide ctrls
    if attrs_position == 'new_locator':
        guide_attrs_position = cmds.spaceLocator(n=name + '_Attrs' + nc['locator'])[0]
    else:
        guide_attrs_position = attrs_position
    mt.line_attr(input=guide_attrs_position, name='Mouth_Vis')
    main_ctrl_attr = mt.new_enum(input=guide_attrs_position, name='lipsMainCtrls', enums='Hide:Show', keyable=False)
    center_ctrl_attr = mt.new_enum(input=guide_attrs_position, name='lipsCenterCtrls', enums='Hide:Show', keyable=False)
    mid_ctrl_attr = mt.new_enum(input=guide_attrs_position, name='lipsMidCtrls', enums='Hide:Show', keyable=False)
    show_tweeks_attr = mt.new_enum(input=guide_attrs_position, name='lipsTweekCtrls', enums='Hide:Show', keyable=False)

    cmds.setAttr(main_ctrl_attr, 1)

    for system in [upper_system, lower_system]:
        for ctrl in system['sec_controllers']:
            shape = cmds.listRelatives(ctrl, s=True)[0]
            cmds.connectAttr(mid_ctrl_attr, '{}.v'.format(shape))
        for ctrl in system['tweek_ctrls']:
            shape = cmds.listRelatives(ctrl, s=True)[0]
            cmds.connectAttr(show_tweeks_attr, '{}.v'.format(shape))
        for ctrl in [system['main_ctrl']]+[center_ctrl]+sub_side_controllers:
            shape = cmds.listRelatives(ctrl, s=True)[0]
            cmds.connectAttr(main_ctrl_attr, '{}.v'.format(shape), f=True)
        for ctrl in [center_ctrl, center_lips_ctrl]:
            shape = cmds.listRelatives(ctrl, s=True)[0]
            cmds.connectAttr(center_ctrl_attr, '{}.v'.format(shape), f=True)


    for ctrl in [left_ctrl, right_ctrl]:
        shape = cmds.listRelatives(ctrl, s=True)[0]
        cmds.connectAttr(main_ctrl_attr, '{}.v'.format(shape))

    #parent ctrls to block parent
    cmds.parentConstraint(block_parent, clean_ctrl_grp, mo=True)

    #Clean a bit
    cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
    cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])

    for system in [upper_system, lower_system]:
        cmds.parent(system['linear_curve'], system['smooth_curve'],
                    system['wire_base'], system['follow_locs_grp'],
                    system['tweek_joints_groups'], system['sec_joints_group'],
                    #system['main_locator_root'],
                    right_up_vector_locator, left_up_vector_locator,
                    clean_rig_grp)
        cmds.parent(system['main_controllers_grp'], center_ctrl)
        cmds.parent(system['main_locator_root'], center_lips_grp)

    cmds.parent(center_ctrl_root, clean_ctrl_grp)
    cmds.parent(center_root, clean_rig_grp)

    # create bind joints
    bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])
    for jnt in upper_system['tweek_joints'] + lower_system['tweek_joints']:
        cmds.select(cl=True)
        bind_joint = cmds.joint(n=jnt.replace(nc['joint'], nc['joint_bind']))
        cmds.parentConstraint(jnt, bind_joint)
        cmds.scaleConstraint(jnt, bind_joint)
        cmds.setAttr('{}.radius'.format(bind_joint), 1.5)
        cmds.parent(bind_joint, bind_jnt_grp)

    if cmds.attributeQuery('SetupOption', n=config, exists=True):
        if cmds.getAttr('{}.SetupOption'.format(config)) == 'Bezier':
            postbuilds_faceinstall.lip_postbuilds()
 