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
            jaw_guide = child

        elif 'LipUp' in child:
            lip_up_guide = child

        elif 'LipDown' in child:
            lip_down_guide = child

    for g in [left_orient_lip, mouth_center, jaw_guide, lip_up_guide, lip_down_guide]:
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

        num_joints = int(cmds.getAttr('{}.TweakCtrlsAmount'.format(config)))
        num_ctrls = int(cmds.getAttr('{}.MidCtrlsAmount'.format(config)))

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

        # --- Create symmetrical names ---
        main_ctrl_names = []
        mid_index = num_joints // 2

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

        # --- Create joints, locators, and POCI setup ---
        for num, ctrl_name in enumerate(main_ctrl_names):

            # Place joint at pivot and on vertex
            cmds.select(cl=True)
            vtx_jnt = cmds.joint(n=f"{ctrl_name}{name}_Tweek{nc['joint']}")
            vtx_joints.append(vtx_jnt)

            # Locator
            end_locator = cmds.spaceLocator(n=f"{name}_{ctrl_name}{nc['locator'].replace('_','')}")[0]
            up_end_locator = cmds.spaceLocator(n=f"{name}_VectorUp_{ctrl_name}{nc['locator'].replace('_','')}")[0]

            vtx_locators.append(end_locator)
            cmds.parent(end_locator, locators_grp)
            cmds.parent(up_end_locator, locators_grp)

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


            four_by_four, decompose = create_tangent_orient_setup(
                base_name=f"{name}_{num}",
                poci=poci,
                loc=end_locator
            )

            if percentage not in (0, 0.5, 1):
                cmds.delete(cmds.parentConstraint(end_locator, vtx_jnt))
            else:
                cmds.delete(cmds.pointConstraint(end_locator, vtx_jnt))

            if percentage == 1:
                cmds.delete(cmds.orientConstraint(left_orient_lip, vtx_jnt))

            # Fix up vector
            # connect_tangent_system(
            #     param_node=poci,
            #     param_attr="parameter",
            #     input_curve=up_vector_curve,
            #     tangent_matrix_node=four_by_four
            # )

            # Do the same but for the up locator
            # pointOnCurveInfo setup
            poci = cmds.createNode('pointOnCurveInfo', n=f"{name}_UpVector_{ctrl_name}_POCI")
            cmds.connectAttr(f'{up_vector_curve}.worldSpace[0]', f'{poci}.inputCurve')
            cmds.connectAttr(f'{poci}.position', f'{up_end_locator}.translate')

            # Use percentage-based parameter (evenly distributed)
            if num_joints > 1:
                percentage = float(num) / (num_joints + 1)
            else:
                percentage = 0.0
            cmds.setAttr(f'{poci}.turnOnPercentage', True)
            cmds.setAttr(f'{poci}.parameter', percentage)

            # ----------------------------------------------
            # ----------------------------------------------

            four_by_four, decompose = create_tangent_orient_setup(
                base_name=f"{name}_UpVector_{num}",
                poci=poci,
                loc=up_end_locator
            )

            if percentage not in (0, 0.5, 1):
                cmds.delete(cmds.parentConstraint(end_locator, vtx_jnt))
            else:
                cmds.delete(cmds.pointConstraint(end_locator, vtx_jnt))

            if percentage == 1:
                cmds.delete(cmds.orientConstraint(left_orient_lip, vtx_jnt))


            #Do the dotproduct stuff




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
            'wire -n "{}_UpWire" -gw false -en 1.000000 -ce 0.000000 -li 0.000000 -w {} {};'.format(name+'_Up', five_curve,
                                                                                                  up_vector_curve))
        cmds.setAttr('{}.dropoffDistance[0]'.format(wire_up[0]), 999)
        wire_base_up = wire_up[1] + 'BaseWire1'

        cmds.move(0,1,0,up_vector_curve, r=True)


        #-------------------------------------
        #-------------------------------------
        #-------------------------------------

        # Dynamically create CV list
        cv_to_add_ctrl_to = ['{}.cv[{}]'.format(five_curve, i) for i in range(num_ctrls + 2)]
        print('cv_to_add_ctrl_to', cv_to_add_ctrl_to)

        mid_index = num_ctrls // 2
        main_ctrl_names = []

        for i in range(num_ctrls + 2):  # +2 for R_ and L_
            if i == 0:
                main_ctrl_names.append('R_')
            elif 0 < i <= mid_index:
                main_ctrl_names.append(f"R_Mid_{str(i).zfill(2)}_")
            elif i == mid_index + 1:
                main_ctrl_names.append('Mid_')
            elif mid_index + 1 < i < num_ctrls + 1:
                main_ctrl_names.append(f"L_Mid_{str(num_ctrls - i + 1).zfill(2)}_")
            else:
                main_ctrl_names.append('L_')

        print(main_ctrl_names)

        #-------------------------------------
        #-------------------------------------
        #-------------------------------------

        sec_ctrls = []
        sec_ctrls_roots = []
        left_sec_ctrls = []

        left_controllers = []
        left_controllers_roots = []

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
            if ctrl.startswith(nc['left']):
                left_controllers.append(ctrl)
                left_controllers_roots.append(ctrl_root)

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

            if ctrl.startswith(nc['left']):
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
        right_controllers = []
        right_controllers_roots = []

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
            right_controllers.append(ctrl)
            mt.assign_color(color=color)
            ctrl_root = mt.root_grp()[0]
            sec_ctrls_roots.append(ctrl_root)
            right_controllers_roots.append(ctrl)
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

            cmds.delete(temp_loc)

        cmds.skinCluster(sec_jnts, five_curve, sm=0, bm=1, tsb=True)


        mid_ctrl = False
        for ctrl in sec_ctrls:
            if ctrl.startswith('Mid_'):
                mid_ctrl = ctrl
        if not mid_ctrl:
            cmds.error('Naming error, sorry...')

        #-----------------------------
        #-----------------------------
        #-----------------------------

        #Create Main Controller
        main_loc = cmds.spaceLocator(n = name + '_Main' + nc['locator'])[0]
        main_loc_root, main_loc_auto = mt.root_grp(autoRoot=True)
        cmds.delete(cmds.parentConstraint(mid_ctrl, main_loc_root))
        cmds.select(main_loc_auto)
        cmds.select(main_loc)
        main_ctrl = mt.curve(input='',
                        type='rectangle',
                        rename=True,
                        custom_name=True,
                        name=name + '_Main' + nc['ctrl'],
                        size=ctrl_size)

        mt.assign_color(color=color)
        main_ctrl_root, main_ctrl_auto = mt.root_grp(main_ctrl, autoRoot=True)
        cmds.parent(main_ctrl_root, main_ctrl_grp)

        if '_Up' in name:
            cmds.delete(cmds.parentConstraint(lip_up_guide, main_ctrl_root))
        else:
            cmds.delete(cmds.parentConstraint(lip_down_guide, main_ctrl_root))

        #Corner Pullers
        left_puller_loc = cmds.spaceLocator(n=nc['left']+name + '_Puller' + nc['locator'])[0]
        right_puller_loc = cmds.spaceLocator(n=nc['right']+name + '_Puller' + nc['locator'])[0]

        mt.match(left_puller_loc, left_controllers[-1])
        mt.match(right_puller_loc, right_controllers[-1])

        print('*'*50)
        print('*'*50)
        print('*'*50)
        print('right_controllers', right_controllers)
        print('-'*50)
        print('left_controllers', left_controllers)
        print('*'*50)
        print('*'*50)
        print('*'*50)

        auto_cache = {}

        def get_auto(ctrl):
            """Return auto for ctrl, creating it only once."""
            if ctrl not in auto_cache:
                root = cmds.listRelatives(ctrl, p=True)[0]
                auto_cache[ctrl] = root
            return auto_cache[ctrl]

        def apply_linear_weights(side_ctrls, start_obj, end_obj):
            """
            Keeps the controller order untouched, but flips weight logic so:
            - last ctrl in list gets the strongest weight to start_obj (puller)
            - first ctrl in list gets weakest
            """

            forward = list(enumerate(side_ctrls))
            backward = list(reversed(forward))

            for num, ctrl in enumerate(side_ctrls):

                auto = get_auto(ctrl)

                pc = cmds.parentConstraint(
                    start_obj,  # puller
                    end_obj,  # mid
                    auto,
                    skipRotate=('x', 'y', 'z'),
                    mo=True
                )[0]

                cmds.setAttr(f"{pc}.{start_obj}W0", backward[num][0])
                cmds.setAttr(f"{pc}.{end_obj}W1", forward[num][0])
                cmds.setAttr(pc + ".interpType", 2)

        # LEFT
        apply_linear_weights(
            [mid_ctrl]+left_controllers,
            start_obj=main_ctrl,
            end_obj=left_puller_loc
        )

        # RIGHT
        apply_linear_weights(
            [mid_ctrl]+right_controllers,
            start_obj=main_ctrl,
            end_obj=right_puller_loc
        )

        #Mid controller
        # mid_root, mid_auto = mt.root_grp(mid_ctrl, autoRoot=True)
        # cmds.parentConstraint(main_ctrl, mid_auto, mo=True)


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
                'up_curve': up_vector_curve,
                'wire_base_up': wire_base_up,
                'follow_locs_grp' : locators_grp,
                'tweek_joints_groups' : vtx_joints_grp,
                'sec_joints': sec_jnts,
                'sec_joints_roots':sec_jnts_roots,
                'sec_joints_group': main_joint_grp,
                'main_locator':main_loc,
                'main_locator_root': main_loc_root,
                'aim_locators':vtx_locators,
                'tweek_joints': vtx_joints,
                'tweek_ctrls':tweek_controllers,
                'corner_pullers':[left_puller_loc, right_puller_loc]
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

    ######################################################
    ######################################################
    ######################################################

    # Clean Groups
    clean_ctrl_grp = cmds.group(em=True, name=name + nc['ctrl'] + nc['group'])
    clean_rig_grp = cmds.group(em=True, name=name + '_Rig' + nc['group'])

    # Main Mouth Controller
    center_grp = cmds.group(em=True, n=name + '_Center' + nc['group'])
    cmds.delete(cmds.parentConstraint(mouth_center, center_grp))
    center_root = mt.root_grp()[0]
    center_lips_grp = cmds.group(em=True, n=name + '_Centerlips' + nc['group'])
    cmds.delete(cmds.parentConstraint(center_grp, center_lips_grp))
    center_lips_root = mt.root_grp()[0]
    cmds.parent(center_lips_root, center_grp)

    center_ctrl = mt.curve(input=center_grp,
                           type='octagon',
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
    cmds.delete(cmds.parentConstraint(upper_system['main_ctrl'], center_cluster))
    cmds.delete(center_ctrl, ch=True)

    cmds.connectAttr('{}.translate'.format(center_ctrl), '{}.translate'.format(center_grp))
    cmds.connectAttr('{}.rotate'.format(center_ctrl), '{}.rotate'.format(center_grp))
    cmds.connectAttr('{}.scale'.format(center_ctrl), '{}.scale'.format(center_grp))

    center_lips_ctrl = mt.curve(input=center_grp,
                                type='octagon',
                                rename=True,
                                custom_name=True,
                                name=name + '_Centerlips' + nc['ctrl'],
                                size=ctrl_size * 0.75)
    mt.assign_color(color='lightBlue')
    center_lips_ctrl_root = mt.root_grp()[0]
    cmds.delete(cmds.parentConstraint(mouth_center, center_lips_ctrl_root))
    cmds.select(center_lips_ctrl + '.cv[0:8]')
    cmds.rotate(90, 0, 0)
    center_cluster = cmds.cluster()
    cmds.delete(cmds.parentConstraint(upper_system['main_ctrl'], center_cluster))
    cmds.delete(center_lips_ctrl, ch=True)

    cmds.connectAttr('{}.translate'.format(center_lips_ctrl), '{}.translate'.format(center_lips_grp))
    cmds.connectAttr('{}.rotate'.format(center_lips_ctrl), '{}.rotate'.format(center_lips_grp))
    cmds.connectAttr('{}.scale'.format(center_lips_ctrl), '{}.scale'.format(center_lips_grp))

    cmds.parent(center_lips_ctrl_root, center_ctrl)

    #--------------------------------------------------------
    #------------------------Main Sides----------------------
    #--------------------------------------------------------

    # Create Side Controllers
    # Create Main Controller
    side_controllers = []
    side_controllers_root = []
    side_locators = []
    sub_side_controllers = []

    for side in [nc['left'], nc['right']]:
        loc = cmds.spaceLocator(n=side + name + '_Main' + nc['locator'])[0]
        loc_root, loc_auto = mt.root_grp(autoRoot=True)
        cmds.delete(cmds.parentConstraint(left_orient_lip, loc_root))

        side_main_ctrl = mt.curve(input='',
                                  type='square',
                                  rename=True,
                                  custom_name=True,
                                  name=side + name + '_Main' + nc['ctrl'],
                                  size=ctrl_size)
        side_controllers.append(side_main_ctrl)

        if side == nc['right']:
            mt.assign_color(color='red')
        else:
            mt.assign_color(color='blue')
        left_main_ctrl_root, left_main_ctrl_auto = mt.root_grp(autoRoot=True)
        side_controllers_root.append(left_main_ctrl_root)

        # Attrs
        mt.line_attr(input=side_main_ctrl, name='Lips')
        mode_attr = mt.new_enum(input=side_main_ctrl, name='mode', enums='BSP:RIG')
        move_mult_attr = mt.new_attr(input=side_main_ctrl, name='MovementMult', min=0.1, max=10, default=1)
        sub_move_mult_attr = mt.new_attr(input=side_main_ctrl, name='SubMovementMult', min=0.1, max=10, default=1)

        # Make pretty
        cmds.select('{}.cv[0:4]'.format(side_main_ctrl))
        cmds.rotate(90, 0, 0, r=True)
        # cmds.select('{}.cv[2:3]'.format(side_main_ctrl))
        # cmds.scale(0,ctrl_size/3,0,r=True)
        # cmds.move(ctrl_size/2,0,0,r=True)
        mt.hide_attr(side_main_ctrl, s=True)

        side_locators.append(loc)

        # ----------SUB-----------------------------------------
        # create sub controller with modes in case we dont use BS
        sub_main_ctrl = mt.curve(input='',
                                 type='square',
                                 rename=True,
                                 custom_name=True,
                                 name=side + name + '_Sub' + nc['ctrl'],
                                 size=ctrl_size / 3)
        sub_side_controllers.append(sub_main_ctrl)
        if side == nc['right']:
            mt.assign_color(color='red')
        else:
            mt.assign_color(color='blue')
        left_sub_ctrl_root = mt.root_grp()[0]

        cmds.select('{}.cv[0:4]'.format(sub_main_ctrl))
        cmds.rotate(90, 0, 0, r=True)
        # cmds.select('{}.cv[2:3]'.format(sub_main_ctrl))
        # cmds.scale(0,ctrl_size/4,0,r=True)
        # cmds.move(ctrl_size/2,0,0,r=True)
        mt.hide_attr(sub_main_ctrl, s=True)
        # cmds.select('{}.cv[0:4]'.format(sub_main_ctrl))
        # cmds.scale(ctrl_size/4,ctrl_size/4,ctrl_size/4,r=True)

        cmds.parent(left_sub_ctrl_root, side_main_ctrl)

        # Flip
        if side == nc['right']:
            loc_root = mt.mirror_group(loc_root, world=True)
            left_main_ctrl_root = mt.mirror_group(left_main_ctrl_root, world=True)

        # cmds.parent(loc_root, clean_rig_grp)
        cmds.parent(loc_root, center_grp)
        # cmds.parent(left_main_ctrl_root, clean_ctrl_grp)
        cmds.parent(left_main_ctrl_root, center_ctrl)

    #--------------------------------------
    cmds.select(cl=True)
    jaw_ctrl = mt.curve(input='',
                      type='circleY',
                      rename=True,
                      custom_name=True,
                      name=name + '_Jaw' + nc['ctrl'],
                      size=ctrl_size*2)


    mt.assign_color(color='purple')
    jaw_ctrl_root = mt.root_grp()[0]
    cmds.parent(jaw_ctrl_root, clean_ctrl_grp)
    cmds.delete(cmds.parentConstraint(jaw_guide, jaw_ctrl_root))


    #aim to upr and lwr lip guides
    aim_temp_loc = cmds.spaceLocator()
    cmds.delete(cmds.parentConstraint(lip_up_guide, lip_down_guide, aim_temp_loc))
    cmds.delete(cmds.aimConstraint(aim_temp_loc,jaw_ctrl_root, aimVector=(0, 0, 1), upVector=(0, 1, 0),
                                   worldUpType='vector', mo=False))
    cmds.delete(aim_temp_loc)

    #Automations time
    left_ctrl = side_controllers[0]
    right_ctrl = side_controllers[1]

    left_sub_ctrl = sub_side_controllers[0]
    right_sub_ctrl = sub_side_controllers[1]

    #jaw top to collide
    jaw_top_locator = cmds.spaceLocator(n=name + '_TopJaw' + nc['locator'])[0]
    cmds.parent(jaw_top_locator, clean_rig_grp)

    #Jaw to main lower and up jaw to main upper
    cmds.parentConstraint(jaw_ctrl, lower_system['main_ctrl_root'], mo=True)
    cmds.parentConstraint(jaw_top_locator, upper_system['main_ctrl_root'], mo=True)

    #Corner controllers stay between loc and jaw
    left_corner_pc=cmds.parentConstraint(jaw_ctrl, jaw_top_locator, side_controllers_root[0], mo=True)[0]
    cmds.setAttr(left_corner_pc + ".interpType", 2)
    right_corner_pc=cmds.parentConstraint(jaw_ctrl, jaw_top_locator, side_controllers_root[1], mo=True)[0]
    cmds.setAttr(right_corner_pc + ".interpType", 2)

    #Corner controller move pullers
    cmds.parentConstraint(left_sub_ctrl, upper_system['corner_pullers'][0], mo=True)
    cmds.parentConstraint(right_sub_ctrl, upper_system['corner_pullers'][1], mo=True)
    cmds.parentConstraint(left_sub_ctrl, lower_system['corner_pullers'][0], mo=True)
    cmds.parentConstraint(right_sub_ctrl, lower_system['corner_pullers'][1], mo=True)

    # Automation for corner pc to move up or down
    left_follow_attr = mt.new_attr(input=left_ctrl,
                                   name='Follow',
                                   min=-0, max=1, default=0.5)

    cmds.connectAttr(left_follow_attr, "{}.{}W0".format(left_corner_pc, jaw_ctrl), f=True)

    reverse_node = cmds.shadingNode('reverse', asUtility=True, name="{}_reverse".format(left_corner_pc))
    cmds.connectAttr(left_follow_attr, "{}.inputX".format(reverse_node), f=True)
    cmds.connectAttr("{}.output.outputX".format(reverse_node),
                     "{}.{}W1".format(left_corner_pc, jaw_top_locator), f=True)


    right_follow_attr = mt.new_attr(input=right_ctrl,
                                   name='Follow',
                                   min=-0, max=1, default=0.5)
    cmds.connectAttr(right_follow_attr, "{}.{}W0".format(right_corner_pc, jaw_ctrl), f=True)

    reverse_node = cmds.shadingNode('reverse', asUtility=True, name="{}_reverse".format(right_corner_pc))
    cmds.connectAttr(right_follow_attr, "{}.inputX".format(reverse_node), f=True)
    cmds.connectAttr("{}.output.outputX".format(reverse_node),
                     "{}.{}W1".format(right_corner_pc, jaw_top_locator), f=True)


    #Jaw up Logic
    up_main_auto = cmds.listRelatives(upper_system['main_ctrl'], p=True)[0]
    up_main_ctrl_root = upper_system['main_ctrl_root']
    pc = cmds.parentConstraint(
        jaw_ctrl,
        up_main_ctrl_root,
        up_main_auto,
        mo=True,
        skipTranslate=['x', 'z'],
        skipRotate=['x', 'y', 'z']
    )[0]

    lt = cmds.createNode("lessThan", name=name+"_jaw_lessThan")
    bc = cmds.createNode("blendColors", name=name+"_jaw_blendColors")
    rev = cmds.createNode("reverse", name=name+"_jaw_reverse")
    cmds.setAttr(bc + ".color1R", 1)  # Been 1R = 1
    cmds.setAttr(bc + ".color2R", 0)  # 2R = 0

    cmds.connectAttr(jaw_ctrl + ".rotateX", lt + ".input1", force=True)
    cmds.connectAttr(lt + ".output", bc + ".blender", force=True)
    cmds.connectAttr(bc + ".output", rev + ".input", force=True)

    weights = cmds.parentConstraint(pc, q=True, wal=True)
    w0, w1 = [f"{pc}.{w}" for w in weights]

    cmds.connectAttr(bc + ".outputR", w0, f=True)
    cmds.connectAttr(rev + ".outputX", w1, f=True)

    #--------------------------------------------------
    #--Make the whole mouth and center mouth works-----
    #--------------------------------------------------

    cmds.parentConstraint(center_ctrl, jaw_top_locator, mo=True)

    #custom groups at center
    lwr_rotate_offset = mt.root_grp(input = lower_system['main_ctrl'], custom = True, custom_name = 'CenterRotateOffset', autoRoot = False, replace_nc = False)[0]
    lwr_rotate_grp = mt.root_grp(input = lower_system['main_ctrl'], custom = True, custom_name = 'CenterRotate', autoRoot = False, replace_nc = False)[0]

    lwr_rotate_lipsoffset = mt.root_grp(input = lower_system['main_ctrl'], custom = True, custom_name = 'CenterRotateLipsOffset', autoRoot = False, replace_nc = False)[0]
    lwr_rotate_lips_grp = mt.root_grp(input = lower_system['main_ctrl'], custom = True, custom_name = 'CenterRotateLips', autoRoot = False, replace_nc = False)[0]
    upr_rotate_lipsoffset = mt.root_grp(input = upper_system['main_ctrl'], custom = True, custom_name = 'CenterRotateLipsOffset', autoRoot = False, replace_nc = False)[0]
    upr_rotate_lipsgrp = mt.root_grp(input = upper_system['main_ctrl'], custom = True, custom_name = 'CenterRotateLips', autoRoot = False, replace_nc = False)[0]

    def match_pivot_to_mouth_center(mouth_center, *groups):
        pivot = cmds.xform(mouth_center, q=True, ws=True, rp=True)
        for grp in groups:
            cmds.xform(grp, ws=True, rp=pivot)
            cmds.xform(grp, ws=True, sp=pivot)

        print("Pivots matched to:", pivot)

    match_pivot_to_mouth_center(
        mouth_center,
        lwr_rotate_lipsoffset,
        upr_rotate_lipsoffset,
        lwr_rotate_offset
    )

    cmds.connectAttr(f"{center_ctrl}.rotate", f"{lwr_rotate_offset}.rotate")
    cmds.connectAttr(f"{center_ctrl}.translate", f"{lwr_rotate_offset}.translate")

    cmds.connectAttr(f"{center_lips_ctrl}.rotate", f"{lwr_rotate_lipsoffset}.rotate")
    cmds.connectAttr(f"{center_lips_ctrl}.rotate", f"{upr_rotate_lipsoffset}.rotate")

    cmds.connectAttr(f"{center_lips_ctrl}.translate", f"{lwr_rotate_lipsoffset}.translate")
    cmds.connectAttr(f"{center_lips_ctrl}.translate", f"{upr_rotate_lipsoffset}.translate")


    #*---------------------------------------------------
    #*---------------------------------------------------
    #Clean
    #*---------------------------------------------------
    #*---------------------------------------------------

    # Visibility switches
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
        for ctrl in [system['main_ctrl']] + [center_ctrl] + sub_side_controllers:
            shape = cmds.listRelatives(ctrl, s=True)[0]
            cmds.connectAttr(main_ctrl_attr, '{}.v'.format(shape), f=True)
        for ctrl in [center_ctrl, center_lips_ctrl]:
            shape = cmds.listRelatives(ctrl, s=True)[0]
            cmds.connectAttr(center_ctrl_attr, '{}.v'.format(shape), f=True)

    for ctrl in [left_ctrl, right_ctrl]:
        shape = cmds.listRelatives(ctrl, s=True)[0]
        cmds.connectAttr(main_ctrl_attr, '{}.v'.format(shape), f=True)

    # parent ctrls to block parent
    cmds.parentConstraint(block_parent, clean_ctrl_grp, mo=True)
    cmds.scaleConstraint(block_parent, clean_ctrl_grp, mo=True)

    # Clean a bit
    cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
    cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])

    for system in [upper_system, lower_system]:
        cmds.parent(system['linear_curve'], system['smooth_curve'], system['up_curve'],
                    system['wire_base'], system['wire_base_up'], system['follow_locs_grp'],
                    system['tweek_joints_groups'], system['sec_joints_group'],
                    system['corner_pullers'],
                    # system['main_locator_root'],
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

    # Create Jaw Bind Joint
    cmds.select(cl=True)
    bind_joint = cmds.joint(n=jaw_ctrl.replace(nc['ctrl'], nc['joint_bind']))
    cmds.parentConstraint(jaw_ctrl, bind_joint)
    cmds.scaleConstraint(jaw_ctrl, bind_joint)
    cmds.setAttr('{}.radius'.format(bind_joint), 1.5)
    cmds.parent(bind_joint, bind_jnt_grp)



    # build complete ----------------------------------------------------
    print ('Build {} Success'.format(block))

#build_mouthgames_block()

#------------------------------------
#------------------------------------
#------------------------------------
#-----------Extra Functions----------
#------------------------------------
#------------------------------------
#------------------------------------

#Fix Orients of Locators
def create_tangent_orient_setup(base_name, poci, loc):
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

def connect_tangent_system(param_node, param_attr, input_curve, tangent_matrix_node):
    """
    param_node: name of node that has .parameter and .position outputs (your *_POCI)
    param_attr: attribute name that stores the parameter (e.g. "parameter")
    input_curve: curve that drives the tangent (the up-vector curve)
    tangent_matrix_node: your existing matrix to plug into (like "Mouth_Dw_7_TangentMatrix")
    """

    # 1. Create pointOnCurveInfo
    poci = cmds.createNode("pointOnCurveInfo")

    # 2. Connect parameter node → POCI.parameter
    cmds.connectAttr(f"{param_node}.{param_attr}", f"{poci}.parameter", f=True)
    cmds.setAttr(f'{poci}.turnOnPercentage', True)

    # 3. Connect curveShape.worldSpace → POCI.inputCurve
    shape = cmds.listRelatives(input_curve, shapes=True)[0]
    cmds.connectAttr(f"{shape}.worldSpace[0]", f"{poci}.inputCurve", f=True)

    # 4. Create plusMinusAverage (subtract)
    pma = cmds.createNode("plusMinusAverage")
    cmds.setAttr(f"{pma}.operation", 2)  # 2 = subtract

    # 5. Connect parameterNode.position → pma.input3D[0]
    cmds.connectAttr(f"{param_node}.position", f"{pma}.input3D[0]", f=True)

    # 6. Connect pointOnCurveInfo.position → pma.input3D[1]
    cmds.connectAttr(f"{poci}.position", f"{pma}.input3D[1]", f=True)

    # 7. Connect pma.output3D → TangentMatrix in10/11/12
    cmds.connectAttr(f"{pma}.output3Dx", f"{tangent_matrix_node}.in10", f=True)
    cmds.connectAttr(f"{pma}.output3Dy", f"{tangent_matrix_node}.in11", f=True)
    cmds.connectAttr(f"{pma}.output3Dz", f"{tangent_matrix_node}.in12", f=True)

    print("Tangent system connected:")
    print(" POCI:", poci)
    print(" PMA:", pma)

    return poci, pma
