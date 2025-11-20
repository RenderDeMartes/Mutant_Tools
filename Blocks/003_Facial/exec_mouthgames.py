from __future__ import absolute_import
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
TAB_FOLDER = '003_Facial'
PYBLOCK_NAME = 'exec_mouthgames'

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

MODULE_FILE = os.path.join(os.path.dirname(__file__),'003_MouthGames.json')
with open(MODULE_FILE) as module_file:
	module = json.load(module_file)

#---------------------------------------------

def create_mouthgames_block(name = 'MouthGames'):

    nc, curve_data, setup = mt.import_configs()
    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name = name, icon = 'MouthGames',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]
    name = block.replace(nc['module'],'')

    left_orient_lip = mt.create_joint_guide(name=nc['left'] + name + '_Orient' + nc['guide'])
    cmds.move(3, 0, 0)
    cmds.parent(left_orient_lip, block)
    mouthCenter = mt.create_joint_guide(name=name + '_SlideCenter' + nc['guide'])
    cmds.move(0, 0, -3)
    jaw = mt.create_joint_guide(name=name + '_Jaw' + nc['guide'])
    cmds.move(0, 5, -10)
    lipUp = mt.create_joint_guide(name=name + '_LipUp' + nc['guide'])
    cmds.move(0, 0.5, 2.5)
    lipDown = mt.create_joint_guide(name=name + '_LipDown' + nc['guide'])
    cmds.move(0, -0.5, 2.5)
    cmds.parent(mouthCenter, jaw, lipUp, lipDown, block)

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_mouthgames_block()

#-------------------------

def build_mouthgames_block():
    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    name = block.replace(nc['module'], '')

    # Get all direct children of the block
    children = cmds.listRelatives(block, c=True, f=False) or []

    # Loop through children and find guides by name
    for child in children:
        if 'Orient' in child:
            left_orient_lip = child

        elif 'SlideCenter' in child:
            mouth_center = child

        elif 'Jaw' in child:
            jaw = child

        elif 'LipUp' in child:
            lip_up = child

        elif 'LipDown' in child:
            lip_down = child

    for g in [left_orient_lip, mouth_center, jaw, lip_up, lip_down]:
        print("  -", g)

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

        #Create up vector
        up_vector_curve = cmds.duplicate(linear_curve, n=name + '_UpVector' + nc['curve'])[0]

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

        num_joints = 7

        # --- Create symmetrical names ---
        main_ctrl_names = []
        mid_index = num_joints // 2

        for i in range(num_joints + 2):  # +2 for R_ and L_
            if i == 0:
                main_ctrl_names.append('R_')
            elif 0 < i <= mid_index:
                main_ctrl_names.append(f"R_Mid_{str(i).zfill(2)}_")
            elif i == mid_index + 1:
                main_ctrl_names.append('Mid')
            elif mid_index + 1 < i < num_joints + 1:
                main_ctrl_names.append(f"L_Mid_{str(num_joints - i + 1).zfill(2)}_")
            else:
                main_ctrl_names.append('L_')

        # --- Create joints, locators, and POCI setup ---
        for num, ctrl_name in enumerate(main_ctrl_names):

            # Place joint at pivot and on vertex
            cmds.select(cl=True)
            vtx_jnt = cmds.joint(n=f"{ctrl_name}{name}_Tweek_{nc['joint']}")
            vtx_joints.append(vtx_jnt)

            # Locator
            end_locator = cmds.spaceLocator(n=f"{name}_{ctrl_name}{nc['locator']}")[0]
            vtx_locators.append(end_locator)
            cmds.parent(end_locator, locators_grp)

            # pointOnCurveInfo setup
            poci = cmds.createNode('pointOnCurveInfo', n=f"{name}_{ctrl_name}_POCI")
            points_on_curve_infos.append(poci)
            cmds.connectAttr(f'{linear_curve_shape}.worldSpace[0]', f'{poci}.inputCurve')
            cmds.connectAttr(f'{poci}.position', f'{end_locator}.translate')

            # Use percentage-based parameter (evenly distributed)
            if num_joints > 1:
                percentage = float(num) / (num_joints + 1)
            else:
                percentage = 0.0
            cmds.setAttr(f'{poci}.turnOnPercentage', True)
            cmds.setAttr(f'{poci}.parameter', percentage)

            #----------------------------------------------
            #----------------------------------------------


            create_tangent_orient_setup(
                base_name=f"{name}_{num}",
                poci=poci,
                loc=end_locator,
                up_vector_curve=up_vector_curve,
                linear_curve=linear_curve
            )

            if percentage not in (0, 0.5, 1):
                cmds.delete(cmds.parentConstraint(end_locator, vtx_jnt))
            else:
                cmds.delete(cmds.pointConstraint(end_locator, vtx_jnt))


        #do only left and middle
        for num, vtx_jnt in enumerate(vtx_joints):

            #----------------------------------------------
            #----------------------------------------------

            if vtx_jnt.startswith(nc['right']):
                continue

            # create controllers to control the curve
            ctrl = mt.curve(input=vtx_jnt,
                            type='square',
                            rename=True,
                            custom_name=True,
                            name=vtx_jnt.replace(nc['joint'],nc['ctrl']),
                            size=ctrl_size / 3)
            tweek_controllers.append(ctrl)
            mt.assign_color(color=color)
            ctrl_root = mt.root_grp()[0]
            mt.match(ctrl_root, vtx_jnt, r=True, t=True)
            cmds.parent(ctrl_root, tweek_ctrl_grp)

            vtx_root = mt.root_grp(input=vtx_jnt)

            #Constraints for game rigs
            cmds.parentConstraint(ctrl, vtx_jnt, mo=True)
            cmds.scaleConstraint(ctrl, vtx_jnt, mo=True)
            cmds.parentConstraint(vtx_locators[num], ctrl_root, mo=True)
            cmds.parent(vtx_root, vtx_joints_grp)

        #Do Right Side using left controllers and mirror
        for num, vtx_jnt in enumerate(vtx_joints):

            #----------------------------------------------
            #----------------------------------------------

            if not vtx_jnt.startswith(nc['right']):
                continue

            # create controllers to control the curve
            ctrl = mt.curve(input=vtx_jnt.replace(nc['right'], nc['left']),
                            type='square',
                            rename=True,
                            custom_name=True,
                            name=vtx_jnt.replace(nc['joint'],nc['ctrl']),
                            size=ctrl_size / 3)
            tweek_controllers.append(ctrl)
            mt.assign_color(color=color)
            ctrl_root = mt.root_grp()[0]
            mt.match(ctrl_root, vtx_jnt.replace(nc['right'], nc['left']), r=True, t=True)

            miror_grp = mt.mirror_group(ctrl_root, world=True)
            cmds.parent(miror_grp, tweek_ctrl_grp)

            vtx_root = mt.root_grp(input=vtx_jnt)

            #Constraints for game rigs
            cmds.parentConstraint(ctrl, vtx_jnt, mo=False)
            cmds.scaleConstraint(ctrl, vtx_jnt, mo=False)
            cmds.parentConstraint(vtx_locators[num], ctrl_root, mo=True)
            cmds.parent(vtx_root, vtx_joints_grp)

        #--------------------------------
        #--------------------------------
        #--------------------------------

        #Create controller for main controllers
        #7 is default
        num_ctrls = 5
        if num_ctrls % 2 == 0:
            num_ctrls += 1
        spans = num_ctrls - 1
        degree = 3

        five_curve = cmds.duplicate(linear_curve, n=name + '_WireDriver' + nc['curve'])[0]
        mel.eval('rebuildCurve -ch 1 -rpo 1 -rt 0 -end 1 -kr 0'
                 ''
                 ''
                 ' -kcp 0 -kep 1 -kt 0 -s {} -d {} -tol 0.01 "{}";'.format(spans, degree, five_curve))
        five_curve_shape = cmds.listRelatives(five_curve, s=True)[0]

        wire = mel.eval(
            'wire -n "{}_Wire" -gw false -en 1.000000 -ce 0.000000 -li 0.000000 -w {} {};'.format(name, five_curve,
                                                                                                  linear_curve))
        cmds.setAttr('{}.dropoffDistance[0]'.format(wire[0]), 999)
        wire_base = wire[1] + 'BaseWire'

        #Wire up vector curve and move up
        wire_up = mel.eval(
            'wire -n "{}_UpWire" -gw false -en 1.000000 -ce 0.000000 -li 0.000000 -w {} {};'.format(name, five_curve,
                                                                                                  up_vector_curve))
        cmds.setAttr('{}.dropoffDistance[0]'.format(wire_up[0]), 999)
        wire_base_up = wire_up[1] + 'BaseWire'

        cmds.move(0,1,0,up_vector_curve, r=True)


        #-------------------------------------
        #-------------------------------------
        #-------------------------------------

        # Dynamically create CV list
        cv_to_add_ctrl_to = ['{}.cv[{}]'.format(five_curve, i) for i in range(num_ctrls + 2)]
        print('cv_to_add_ctrl_to', cv_to_add_ctrl_to)

        mid_index = num_ctrls // 2
        main_ctrl_names = []

        for i in range(num_joints + 2):  # +2 for R_ and L_
            if i == 0:
                main_ctrl_names.append('R_')
            elif 0 < i <= mid_index:
                main_ctrl_names.append(f"R_Mid_{str(i).zfill(2)}_")
            elif i == mid_index + 1:
                main_ctrl_names.append('Mid_')
            elif mid_index + 1 < i < num_joints + 1:
                main_ctrl_names.append(f"L_Mid_{str(num_joints - i + 1).zfill(2)}_")
            else:
                main_ctrl_names.append('L_')

        print(main_ctrl_names)

        #-------------------------------------
        #-------------------------------------
        #-------------------------------------

        sec_ctrls = []
        sec_ctrls_roots = []
        left_sec_ctrls = []


        sec_jnts = []
        sec_jnts_roots = []

        main_joint_grp = cmds.group(em=True, n='{}{}{}'.format(name, nc['joint'], nc['group']))

        #Left side first
        for num, cv in enumerate(cv_to_add_ctrl_to):

            if main_ctrl_names[num].startswith(nc['right']):
                continue

            cmds.select(cv)
            temp_cls = cmds.cluster()

            # Create controller at that position
            ctrl = mt.curve(
                type='circleZ',
                rename=True,
                custom_name=True,
                name=main_ctrl_names[num] + name + nc['ctrl'],
                size=ctrl_size / 2
            )
            sec_ctrls.append(ctrl)

            mt.assign_color(color=color)
            ctrl_root = mt.root_grp()[0]
            sec_ctrls_roots.append(ctrl_root)
            cmds.parent(ctrl_root, main_ctrl_grp)
            mt.match(ctrl_root, temp_cls, r=True, t=True)

            cmds.delete(temp_cls)

            cmds.select(cl=True)
            jnt = cmds.joint(n=ctrl.replace(nc['ctrl'], nc['joint']))
            sec_jnts.append(jnt)
            mt.match(jnt, ctrl, r=True, t=True)
            jnt_root = mt.root_grp()[0]
            sec_jnts_roots.append(jnt_root)
            cmds.parent(jnt_root, main_joint_grp)

            cmds.parentConstraint(ctrl, jnt, mo=True)
            cmds.scaleConstraint(ctrl, jnt, mo=True)

            # *--------- Aims or Orients -------------
            # *----------------------------

            if 'L_' in ctrl:
                left_sec_ctrls.append(ctrl)

                #Near to curve to move on top of curve
                temp_loc = cmds.spaceLocator()[0]
                temp_loc2 = cmds.spaceLocator()[0]

                npoc = cmds.createNode("nearestPointOnCurve")
                poci = cmds.createNode('pointOnCurveInfo')
                four_by_four = cmds.shadingNode('fourByFourMatrix', asUtility=True)
                decompose = cmds.createNode('decomposeMatrix')


                mt.match(temp_loc, ctrl, t=True)
                cmds.connectAttr(f'{temp_loc}.translate', f"{npoc}.inPosition")
                cmds.connectAttr(f'{linear_curve_shape}.worldSpace', f"{npoc}.inputCurve")

                cmds.connectAttr(f'{npoc}.position', f"{temp_loc2}.translate")

                cmds.connectAttr(f'{linear_curve_shape}.worldSpace[0]', f'{poci}.inputCurve')
                cmds.connectAttr(f'{npoc}.parameter', f'{poci}.parameter')

                # Connect normalized tangent to matrix
                cmds.connectAttr(f"{poci}.normalizedTangentX", f"{four_by_four}.in00", f=True)
                cmds.connectAttr(f"{poci}.normalizedTangentY", f"{four_by_four}.in01", f=True)
                cmds.connectAttr(f"{poci}.normalizedTangentZ", f"{four_by_four}.in02", f=True)

                cmds.connectAttr(f"{poci}.positionX", f"{four_by_four}.in30", f=True)
                cmds.connectAttr(f"{poci}.positionY", f"{four_by_four}.in31", f=True)
                cmds.connectAttr(f"{poci}.positionZ", f"{four_by_four}.in32", f=True)

                # Connect matrix to decomposeMatrix
                cmds.connectAttr(f"{four_by_four}.output", f"{decompose}.inputMatrix", f=True)

                # Connect rotation output to locator
                cmds.connectAttr(f"{decompose}.outputRotateX", f"{temp_loc2}.rotateX", f=True)
                cmds.connectAttr(f"{decompose}.outputRotateY", f"{temp_loc2}.rotateY", f=True)
                cmds.connectAttr(f"{decompose}.outputRotateZ", f"{temp_loc2}.rotateZ", f=True)
                cmds.connectAttr(f"{decompose}.outputTranslateX", f"{temp_loc2}.translateX", f=True)
                cmds.connectAttr(f"{decompose}.outputTranslateY", f"{temp_loc2}.translateY", f=True)
                cmds.connectAttr(f"{decompose}.outputTranslateZ", f"{temp_loc2}.translateZ", f=True)

                #Orient to Follow the Curve
                mt.match(ctrl_root, temp_loc2, r=True, t=True)

                cmds.delete(temp_loc, temp_loc2)
                cmds.delete(npoc, poci, four_by_four)


            # ----------------------------------------------
            # ----------------------------------------------

        #Fix latest controller
        cmds.delete(cmds.parentConstraint(left_orient_lip,ctrl_root))

        #Do Right side now...
        for left_ctrl in left_sec_ctrls:
            temp_loc = cmds.spaceLocator()
            cmds.delete(cmds.parentConstraint(left_ctrl, temp_loc))

            # Create controller at that position
            ctrl = mt.curve(
                type='circleZ',
                rename=True,
                custom_name=True,
                name=left_ctrl.replace(nc['left'], nc['right']),
                size=ctrl_size / 2
            )
            sec_ctrls.append(ctrl)

            mt.assign_color(color=color)
            ctrl_root = mt.root_grp()[0]
            sec_ctrls_roots.append(ctrl_root)
            cmds.parent(ctrl_root, main_ctrl_grp)
            mt.match(ctrl_root, left_ctrl, r=True, t=True)

            cmds.select(cl=True)
            jnt = cmds.joint(n=ctrl.replace(nc['ctrl'], nc['joint']))
            sec_jnts.append(jnt)
            mt.match(jnt, ctrl, r=True, t=True)
            jnt_root = mt.root_grp()[0]
            sec_jnts_roots.append(jnt_root)
            cmds.parent(jnt_root, main_joint_grp)

            cmds.parentConstraint(ctrl, jnt, mo=True)
            cmds.scaleConstraint(ctrl, jnt, mo=True)

            #Mirror and reparent
            miror_ctrl_grp = mt.mirror_group(ctrl_root, world=True)
            cmds.parent(miror_ctrl_grp, main_ctrl_grp)


        cmds.skinCluster(sec_jnts, five_curve, sm=0, bm=1, tsb=True)


        #-----------------------------
        #-----------------------------
        #-----------------------------

        #Create Main Controller
        main_loc = cmds.spaceLocator(n = name + '_Main' + nc['locator'])[0]
        main_loc_root, main_loc_auto = mt.root_grp(autoRoot=True)
        cmds.delete(cmds.parentConstraint(sec_ctrls, main_loc_root))
        cmds.select(main_loc_auto)
        cmds.select(main_loc)
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

        aa

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



    # build complete ----------------------------------------------------
    print ('Build {} Success'.format(block))


#build_mouthgames_block()

#Fix Orients of Locators
def create_tangent_orient_setup(base_name, poci, loc, up_vector_curve, linear_curve):
    """
    Creates a fourByFourMatrix + decomposeMatrix setup that drives
    the rotation of a locator based on a POCI's tangent.

    Args:
        base_name (str): Base name for the created nodes (e.g. 'Mouth_Up_20')
        poci (str): Name of the pointOnCurveInfo node
        loc (str): Name of the locator to receive rotation
    """

    # Create nodes
    four_by_four = cmds.shadingNode('fourByFourMatrix', asUtility=True, name=f"{base_name}_TangentMatrix")
    decompose = cmds.createNode('decomposeMatrix', name=f"{base_name}_DecomposeMatrix")

    # Connect normalized tangent to matrix
    cmds.connectAttr(f"{poci}.normalizedTangentX", f"{four_by_four}.in00", f=True)
    cmds.connectAttr(f"{poci}.normalizedTangentY", f"{four_by_four}.in01", f=True)
    cmds.connectAttr(f"{poci}.normalizedTangentZ", f"{four_by_four}.in02", f=True)

    # Connect matrix to decomposeMatrix
    cmds.connectAttr(f"{four_by_four}.output", f"{decompose}.inputMatrix", f=True)

    # Connect rotation output to locator
    cmds.connectAttr(f"{decompose}.outputRotateX", f"{loc}.rotateX", f=True)
    cmds.connectAttr(f"{decompose}.outputRotateY", f"{loc}.rotateY", f=True)
    cmds.connectAttr(f"{decompose}.outputRotateZ", f"{loc}.rotateZ", f=True)

    print(f"✅ Created tangent orientation setup for {base_name}")
    return four_by_four, decompose