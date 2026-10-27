from __future__ import absolute_import
from maya import cmds, mel
import json
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import os
import math
from pathlib import Path
from maya.api import OpenMaya as om

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()

#---------------------------------------------
TAB_FOLDER = '003_Facial'
PYBLOCK_NAME = 'exec_mouthgames'
CORNER_ORIENTS = False

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

MODULE_FILE = os.path.join(os.path.dirname(__file__),'003_MouthGames_v003.json')
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
    # rest position of the jaw rotation pivot (Mouth_JawPivot_Ctrl starts here)
    jawPivot = mt.create_joint_guide(name=name + '_JawPivot' + nc['guide'])
    cmds.move(0, 5, -10)
    cmds.parent(mouthCenter, jaw, lipUp, lipDown, jawPivot, block)

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
    jaw_pivot_guide = None  # blocks made before v003's pivot use the Jaw guide
    for child in children:
        if 'JawPivot' in child:
            jaw_pivot_guide = child

        elif 'Orient' in child:
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

    if cmds.attributeQuery('BindJoints', n=config, exists=True):
        bind_joints_mode = cmds.getAttr('{}.BindJoints'.format(config), asString=True)
    else:
        bind_joints_mode = 'PerVtx'

    upper_edge = cmds.getAttr('{}.SetUpperEdge'.format(config), asString=True).split(',')
    lower_edge = cmds.getAttr('{}.SetLowerEdge'.format(config), asString=True).split(',')
    attrs_position = cmds.getAttr('{}.SetAttrsPosition'.format(config), asString=True)

    def create_lips_system(name, edge, check_curve=True, color ='yellow'):

        num_joints = int(cmds.getAttr('{}.TweakCtrlsAmount'.format(config)))
        num_ctrls = int(cmds.getAttr('{}.MidCtrlsAmount'.format(config)))
        corner_follow_locs = []
        interior_end_locators = []

        #
        cmds.select(edge)
        linear_curve = cmds.polyToCurve(form=0,
                                        degree=1,
                                        conformToSmoothMeshPreview=1,
                                        n=name + '_Vtx' + nc['curve'],
                                        ch=False)[0]
        linear_curve_shape = cmds.listRelatives(linear_curve, s=True)[0]
        linear_curve_cvs = cmds.getAttr('{}.spans'.format(linear_curve_shape)) + 1

        # make sure curve is in correct orientation (cv[0] on the right side)
        if check_curve:
            first_cv = cmds.xform('{}.cv[0]'.format(linear_curve), q=True, ws=True, t=True)
            last_cv = cmds.xform('{}.cv[{}]'.format(linear_curve, linear_curve_cvs - 1), q=True, ws=True, t=True)
            if first_cv[0] > last_cv[0]:
                cmds.reverseCurve(linear_curve, ch=False, replaceOriginal=True)

        cmds.delete(linear_curve, ch=True)

        # v003: every point (joint or tweak) is placed by curve LENGTH, not by
        # parameter. v002 used POCI percentage on the linear vertex curve, which
        # follows the vertex index, so joints bunched up wherever the edge loop
        # had small edges (corners) and spread out in the middle.
        if bind_joints_mode == 'PerVtx':
            joint_params = vertex_params(linear_curve_shape)
        else:
            joint_params = params_by_length(linear_curve_shape, int(bind_joints_mode))
        tweak_params = params_by_length(linear_curve_shape, num_joints + 2)

        tweek_controllers = []
        locators_grp = cmds.group(em=True, n='{}_FollowLocators{}'.format(name, nc['group']))
        tweek_ctrl_grp = cmds.group(em=True, n='{}_Tweeks{}{}'.format(name, nc['ctrl'], nc['group']))
        main_ctrl_grp = cmds.group(em=True, n='{}{}{}'.format(name, nc['ctrl'], nc['group']))
        cmds.parent(tweek_ctrl_grp, main_ctrl_grp)

        # One curveInfo reads every CV of the (linear) lip curve. A
        # pointOnCurveInfo per point cost ~0.4ms each on a 30+ CV curve, more
        # than the whole rest of the mouth.
        curve_info = cmds.createNode('curveInfo', n=name + '_Vtx_CurveInfo')
        cmds.connectAttr(f'{linear_curve_shape}.worldSpace[0]', f'{curve_info}.inputCurve')

        def add_point(point_name, param):
            """Follow transform riding the lip curve at a fixed parameter."""
            carrier = cmds.createNode('transform', n=point_name + '_Follow' + nc['group'], p=locators_grp)
            position = linear_curve_point(curve_info, linear_curve_shape, param, point_name)
            cmds.connectAttr(position, f'{carrier}.translate')
            u = length_fraction(linear_curve_shape, param)
            is_corner = u < 1e-4 or u > 1 - 1e-4
            point = {'name': point_name, 'carrier': carrier, 'position': position,
                     'param': param, 'u': u, 'corner': is_corner}
            if is_corner:
                corner_follow_locs.append((nc['right'] if u < 0.5 else nc['left'], carrier))
            else:
                interior_end_locators.append(carrier)
            return point

        # --- Lip joints: one per point, child of its follow transform ---
        lip_points = []
        for jnt_name, param in zip(symmetric_names(name + '_Lip', joint_params, linear_curve_shape), joint_params):
            point = add_point(jnt_name, param)
            cmds.select(cl=True)
            jnt = cmds.joint(n=jnt_name + nc['joint'])
            cmds.parent(jnt, point['carrier'], r=True)
            point['joint'] = jnt
            lip_points.append(point)

        # --- Tweak controllers (same names / amount as v002) ---
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

        tweak_points = []
        for ctrl_name, param in zip(main_ctrl_names, tweak_params):
            point = add_point(f"{ctrl_name}{name}_Tweek", param)
            point['ctrl_name'] = f"{ctrl_name}{name}_Tweek{nc['ctrl']}"
            tweak_points.append(point)
        points_by_ctrl = {p['ctrl_name']: p for p in tweak_points}

        # Left and middle first, right side mirrors the left ones
        for point in tweak_points:
            if point['ctrl_name'].startswith(nc['right']):
                continue
            cmds.select(cl=True)
            ctrl = mt.curve(input=point['carrier'],
                            type='square',
                            rename=True,
                            custom_name=True,
                            name=point['ctrl_name'],
                            size=ctrl_size / 3)
            tweek_controllers.append(ctrl)
            mt.assign_color(color=color)
            ctrl_root = mt.root_grp()[0]
            cmds.xform(ctrl_root, ws=True, t=cmds.xform(point['carrier'], q=True, ws=True, t=True), ro=(0, 0, 0))
            cmds.parent(ctrl_root, tweek_ctrl_grp)
            cmds.parentConstraint(point['carrier'], ctrl_root, mo=True)
            point['ctrl'] = ctrl

        for point in tweak_points:
            if not point['ctrl_name'].startswith(nc['right']):
                continue
            left_point = points_by_ctrl[point['ctrl_name'].replace(nc['right'], nc['left'], 1)]
            cmds.select(cl=True)
            ctrl = mt.curve(input=left_point['carrier'],
                            type='square',
                            rename=True,
                            custom_name=True,
                            name=point['ctrl_name'],
                            size=ctrl_size / 3)
            tweek_controllers.append(ctrl)
            mt.assign_color(color=color)
            ctrl_root = mt.root_grp()[0]
            cmds.xform(ctrl_root, ws=True, t=cmds.xform(left_point['carrier'], q=True, ws=True, t=True), ro=(0, 0, 0))

            miror_grp = mt.mirror_group(ctrl_root, world=True)
            cmds.parent(miror_grp, tweek_ctrl_grp)
            cmds.parentConstraint(point['carrier'], ctrl_root, mo=True)
            point['ctrl'] = ctrl

        # Tweaks push the lip joints around them with a soft falloff
        # (ctrl local channels straight into the joint, like the reference
        # rig's bind_grp_b offsets -- no constraint on the joint, no cycle)
        tweak_us = [p['u'] for p in tweak_points]
        for point in lip_points:
            point['tweak_weights'] = [(tweak_points[k]['ctrl'], w)
                                      for k, w in cosine_weights(tweak_us, point['u'])]

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

            # no scaleConstraint: scaling a mid ctrl scales the lip joints
            # around it (weighted, see connect_lip_scale) instead of
            # stretching the driver curve
            cmds.parentConstraint(ctrl, jnt, mo=True)

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

            # no scaleConstraint: scaling a mid ctrl scales the lip joints
            # around it (weighted, see connect_lip_scale) instead of
            # stretching the driver curve
            cmds.parentConstraint(ctrl, jnt, mo=True)

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

        if not CORNER_ORIENTS:
            for side, puller in [(nc['right'], right_puller_loc), (nc['left'], left_puller_loc)]:
                follow_rotation(puller, [loc for s, loc in corner_follow_locs if s == side])

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
                'curve_shape': linear_curve_shape,
                'curve_info': curve_info,
                'smooth_curve' : five_curve,
                'wire_base' : wire_base,
                'follow_locs_grp' : locators_grp,
                'sec_joints': sec_jnts,
                'sec_joints_roots':sec_jnts_roots,
                'sec_joints_group': main_joint_grp,
                'main_locator':main_loc,
                'main_locator_root': main_loc_root,
                'interior_end_locators': interior_end_locators,
                'lip_points': lip_points,
                'tweak_points': tweak_points,
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
        # seals the lips from this corner to the middle (0 -> 10)
        mt.new_attr(input=side_main_ctrl, name='Zip', min=0, max=10, default=0)

        # Make pretty
        cmds.select('{}.cv[0:4]'.format(side_main_ctrl))
        cmds.rotate(90, 0, 0, r=True)
        # cmds.select('{}.cv[2:3]'.format(side_main_ctrl))
        # cmds.scale(0,ctrl_size/3,0,r=True)
        # cmds.move(ctrl_size/2,0,0,r=True)
        # v003: scale stays visible, it scales the corner of both lips

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

    # Dynamic pivot: Mouth_JawPivot_Ctrl moves jaw_ctrl.rotatePivot. Everything
    # that follows the jaw follows jaw_follow (a null under jaw_ctrl) instead
    # of jaw_ctrl itself, because constraints read the ctrl's rotatePivot and
    # would jump every time the pivot moves.
    jaw_follow = cmds.createNode('transform', n=name + '_JawFollow' + nc['null'], p=jaw_ctrl)

    cmds.select(cl=True)
    jaw_pivot_ctrl = mt.curve(input='',
                              type='sphere',
                              rename=True,
                              custom_name=True,
                              name=name + '_JawPivot' + nc['ctrl'],
                              size=ctrl_size / 3)
    mt.assign_color(color='yellow')
    jaw_pivot_root = mt.root_grp()[0]
    cmds.parent(jaw_pivot_root, jaw_ctrl_root)
    cmds.xform(jaw_pivot_root, os=True, t=(0, 0, 0), ro=(0, 0, 0))
    # rides the jaw translate (rotatePivot lives in jaw_ctrl's object space)
    jaw_pivot_follow = mt.root_grp(input=jaw_pivot_ctrl, custom=True, custom_name='JawTranslate',
                                   autoRoot=False, replace_nc=False)[0]
    cmds.connectAttr(jaw_ctrl + '.translate', jaw_pivot_follow + '.translate')
    pivot_source = jaw_pivot_guide or jaw_guide
    rest_pivot = cmds.xform(pivot_source, q=True, ws=True, t=True)
    cmds.xform(jaw_pivot_root, ws=True, t=rest_pivot)
    rest_local = cmds.getAttr(jaw_pivot_root + '.translate')[0]
    cmds.xform(jaw_pivot_root, os=True, t=(0, 0, 0))
    cmds.setAttr(jaw_pivot_ctrl + '.translate', 0, 0, 0)
    pivot_sum = cmds.createNode('plusMinusAverage', n=name + '_JawPivot_PMA')
    cmds.setAttr(pivot_sum + '.input3D[0]', *rest_local)
    cmds.connectAttr(jaw_pivot_ctrl + '.translate', pivot_sum + '.input3D[1]')
    cmds.connectAttr(pivot_sum + '.output3D', jaw_ctrl + '.rotatePivot')
    cmds.connectAttr(pivot_sum + '.output3D', jaw_ctrl + '.scalePivot')
    # pivot ctrl shape sits on the pivot: offset its CVs, not its transform
    cmds.move(rest_local[0], rest_local[1], rest_local[2], jaw_pivot_ctrl + '.cv[*]', r=True, os=True)
    mt.hide_attr(jaw_pivot_ctrl, r=True, s=True)

    #Automations time
    left_ctrl = side_controllers[0]
    right_ctrl = side_controllers[1]

    left_sub_ctrl = sub_side_controllers[0]
    right_sub_ctrl = sub_side_controllers[1]

    #jaw top to collide
    jaw_top_locator = cmds.spaceLocator(n=name + '_TopJaw' + nc['locator'])[0]
    cmds.parent(jaw_top_locator, clean_rig_grp)

    #Jaw to main lower and up jaw to main upper
    cmds.parentConstraint(jaw_follow, lower_system['main_ctrl_root'], mo=True)
    cmds.parentConstraint(jaw_top_locator, upper_system['main_ctrl_root'], mo=True)

    # Interior tweak locators no longer compute their own orient off the
    # curve -- every geometry-based attempt (fourByFourMatrix, motionPath,
    # aim-chain) eventually hit a point whose tangent went singular against
    # whatever reference it used. Force it instead: every interior locator
    # just takes the same rigid rotation as the jaw. Nothing left to flip.
    # v003: one shared rotation per driver instead of an orientConstraint
    # per locator (same result as orientConstraint mo=True)
    follow_rotation(jaw_follow, lower_system['interior_end_locators'])
    follow_rotation(jaw_top_locator, upper_system['interior_end_locators'])

    #Corner controllers stay between loc and jaw
    left_corner_pc=cmds.parentConstraint(jaw_follow, jaw_top_locator, side_controllers_root[0], mo=True)[0]
    cmds.setAttr(left_corner_pc + ".interpType", 2)
    right_corner_pc=cmds.parentConstraint(jaw_follow, jaw_top_locator, side_controllers_root[1], mo=True)[0]
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

    cmds.connectAttr(left_follow_attr, "{}.{}W0".format(left_corner_pc, jaw_follow), f=True)

    reverse_node = cmds.shadingNode('reverse', asUtility=True, name="{}_reverse".format(left_corner_pc))
    cmds.connectAttr(left_follow_attr, "{}.inputX".format(reverse_node), f=True)
    cmds.connectAttr("{}.output.outputX".format(reverse_node),
                     "{}.{}W1".format(left_corner_pc, jaw_top_locator), f=True)


    right_follow_attr = mt.new_attr(input=right_ctrl,
                                   name='Follow',
                                   min=-0, max=1, default=0.5)
    cmds.connectAttr(right_follow_attr, "{}.{}W0".format(right_corner_pc, jaw_follow), f=True)

    reverse_node = cmds.shadingNode('reverse', asUtility=True, name="{}_reverse".format(right_corner_pc))
    cmds.connectAttr(right_follow_attr, "{}.inputX".format(reverse_node), f=True)
    cmds.connectAttr("{}.output.outputX".format(reverse_node),
                     "{}.{}W1".format(right_corner_pc, jaw_top_locator), f=True)


    #Jaw up Logic
    up_main_auto = cmds.listRelatives(upper_system['main_ctrl'], p=True)[0]
    up_main_ctrl_root = upper_system['main_ctrl_root']
    pc = cmds.parentConstraint(
        jaw_follow,
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

    # LipCollision attr on jaw to blend collision on/off
    mt.line_attr(input=jaw_ctrl, name='Automation')
    lip_collision_attr = mt.new_attr(input=jaw_ctrl, name='LipCollision', min=0, max=1, default=1)
    pivot_vis_attr = mt.new_enum(input=jaw_ctrl, name='PivotCtrl', enums='Hide:Show', keyable=False)
    for shape in cmds.listRelatives(jaw_pivot_ctrl, s=True) or []:
        cmds.connectAttr(pivot_vis_attr, shape + '.v')

    collision_mult = cmds.createNode("multiplyDivide", name=name + "_jaw_collisionMult")
    cmds.connectAttr(bc + ".outputR", collision_mult + ".input1X", f=True)
    cmds.connectAttr(lip_collision_attr, collision_mult + ".input2X", f=True)

    collision_rev = cmds.createNode("reverse", name=name + "_jaw_collisionReverse")
    cmds.connectAttr(collision_mult + ".outputX", collision_rev + ".inputX", f=True)

    cmds.connectAttr(collision_mult + ".outputX", w0, f=True)
    cmds.connectAttr(collision_rev + ".outputX", w1, f=True)

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
    cmds.scaleConstraint(block_parent, jaw_top_locator, mo=True)

    # Clean a bit
    cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
    cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])

    for system in [upper_system, lower_system]:
        cmds.parent(system['linear_curve'], system['smooth_curve'],
                    system['wire_base'], system['follow_locs_grp'],
                    system['sec_joints_group'],
                    system['corner_pullers'],
                    # system['main_locator_root'],
                    clean_rig_grp)
        cmds.parent(system['main_controllers_grp'], center_ctrl)
        cmds.parent(system['main_locator_root'], center_lips_grp)

    cmds.parent(center_ctrl_root, clean_ctrl_grp)
    cmds.parent(center_root, clean_rig_grp)

    #*---------------------------------------------------
    # v003 lip joints: zip, tweak offsets, roll and weighted scale
    #*---------------------------------------------------
    systems = [upper_system, lower_system]

    # block scale on every follow transform, so the joint offsets and the
    # joint scale follow a scaled rig like the v002 constraints did
    parent_node = block_parent[0] if isinstance(block_parent, list) else block_parent
    parent_scale = cmds.createNode('decomposeMatrix', n=name + '_ParentScale_DM')
    cmds.connectAttr(parent_node + '.worldMatrix[0]', parent_scale + '.inputMatrix')
    for system in systems:
        for point in system['lip_points'] + system['tweak_points']:
            cmds.connectAttr(parent_scale + '.outputScale', point['carrier'] + '.scale')

    # Zip: each point slides to the middle of both lips, from the corners in
    zip_attrs = {nc['left']: left_ctrl + '.Zip', nc['right']: right_ctrl + '.Zip'}
    for system, other in [(upper_system, lower_system), (lower_system, upper_system)]:
        for point in system['lip_points'] + system['tweak_points']:
            connect_zip(point, other['curve_info'], other['curve_shape'], zip_attrs)

    # Roll: curls the lip out (positive) / in, strongest in the middle
    roll_attrs = {}
    for system, sign in [(upper_system, -1), (lower_system, 1)]:
        mt.line_attr(input=system['main_ctrl'], name='Lips')
        roll_attrs[system['main_ctrl']] = (mt.new_attr(input=system['main_ctrl'], name='Roll',
                                                       min=False, max=False, default=0), sign)

    # Scale weights = how much each ctrl moves each point (normalized), so
    # scale falls off over the lip exactly like translate does
    all_points = upper_system['lip_points'] + lower_system['lip_points']
    scale_ctrls = side_controllers + sub_side_controllers
    for system in systems:
        scale_ctrls += system['sec_controllers'] + [system['main_ctrl']]
    scale_weights = measure_point_weights(scale_ctrls, all_points)

    scale_minus = {}
    for ctrl in scale_ctrls + upper_system['tweek_ctrls'] + lower_system['tweek_ctrls']:
        minus = cmds.createNode('plusMinusAverage', n=ctrl + '_ScaleMinus_PMA')
        cmds.setAttr(minus + '.operation', 2)
        cmds.connectAttr(ctrl + '.scale', minus + '.input3D[0]')
        cmds.setAttr(minus + '.input3D[1]', 1, 1, 1)
        scale_minus[ctrl] = minus

    # tweak rotate read once as plain degrees, so the blendWeighted inputs
    # don't each get their own unitConversion
    tweak_degrees = {}
    for tweak in upper_system['tweek_ctrls'] + lower_system['tweek_ctrls']:
        degrees = cmds.createNode('multiplyDivide', n=tweak + '_RotateDegrees_MD')
        cmds.connectAttr(tweak + '.rotate', degrees + '.input1')
        tweak_degrees[tweak] = degrees

    for system in systems:
        roll_attr, roll_sign = roll_attrs[system['main_ctrl']]
        for point in system['lip_points']:
            jnt = point['joint']
            translate_terms = [[], [], []]
            rotate_terms = [[], [], []]
            scale_terms = [[], [], []]

            for tweak, weight in point['tweak_weights']:
                axes = axis_map(tweak, point['carrier'])
                for b in range(3):
                    for a in range(3):
                        m = axes['vector'][a][b]
                        if abs(m) > 1e-3:
                            translate_terms[b].append(('{}.t{}'.format(tweak, 'xyz'[a]), weight * m))
                            rotate_terms[b].append(('{}.output{}'.format(tweak_degrees[tweak], 'XYZ'[a]), weight * m * axes['det']))
                    scale_terms[b].append(('{}.output3D{}'.format(scale_minus[tweak], 'xyz'[axes['scale'][b]]), weight))

            rotate_terms[0].append((roll_attr, roll_sign * math.sin(math.pi * point['u'])))

            for ctrl, weight in scale_weights.get(jnt, []):
                axes = axis_map(ctrl, point['carrier'])
                for b in range(3):
                    scale_terms[b].append(('{}.output3D{}'.format(scale_minus[ctrl], 'xyz'[axes['scale'][b]]), weight))

            for b, axis in enumerate('XYZ'):
                out = weighted_sum('{}_Translate{}_BW'.format(jnt, axis), translate_terms[b])
                if out:
                    cmds.connectAttr(out, '{}.translate{}'.format(jnt, axis))
                out = weighted_sum('{}_Rotate{}_BW'.format(jnt, axis), rotate_terms[b])
                if out:
                    cmds.connectAttr(out, '{}.rotate{}'.format(jnt, axis))
                out = weighted_sum('{}_Scale{}_BW'.format(jnt, axis), scale_terms[b], constant=1.0)
                cmds.connectAttr(out, '{}.scale{}'.format(jnt, axis))

    # create bind joints
    bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])
    lip_joints = [p['joint'] for p in upper_system['lip_points'] + lower_system['lip_points']]
    for jnt in lip_joints:
        cmds.select(cl=True)
        bind_joint = cmds.joint(n=jnt.replace(nc['joint'], nc['joint_bind']))
        cmds.setAttr('{}.radius'.format(bind_joint), 1.5)
        cmds.parent(bind_joint, bind_jnt_grp)
        # matrix copy instead of parent + scale constraints (cheaper, same result)
        follow_matrix(jnt, bind_joint)

    # Create Jaw Bind Joint
    cmds.select(cl=True)
    bind_joint = cmds.joint(n=jaw_ctrl.replace(nc['ctrl'], nc['joint_bind']))
    cmds.parentConstraint(jaw_follow, bind_joint)
    cmds.scaleConstraint(jaw_follow, bind_joint)
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

#------------------------------------
#-----------v003 lip helpers---------
#------------------------------------

def _curve_fn(shape):
    sel = om.MSelectionList()
    sel.add(shape)
    return om.MFnNurbsCurve(sel.getDagPath(0))


def vertex_params(shape):
    """One parameter per CV of the linear vertex curve (PerVtx joints)."""
    return list(_curve_fn(shape).knots())


def params_by_length(shape, count):
    """count parameters evenly spaced by curve length, corners included."""
    fn = _curve_fn(shape)
    length = fn.length()
    start, end = fn.knotDomain
    count = max(int(count), 2)
    params = [fn.findParamFromLength(length * i / (count - 1)) for i in range(count - 1)]
    return params + [end]


def length_fraction(shape, param):
    fn = _curve_fn(shape)
    return fn.findLengthFromParam(param) / fn.length()


def param_from_fraction(shape, u):
    fn = _curve_fn(shape)
    if u >= 1 - 1e-6:
        return fn.knotDomain[1]
    return fn.findParamFromLength(fn.length() * max(u, 0.0))


def symmetric_names(base, params, shape, eps=1e-4):
    """Mid_<base> for the center point, R_/L_<base>_NN counting out from the middle."""
    us = [length_fraction(shape, p) for p in params]
    right = sorted([u for u in us if u < 0.5 - eps], reverse=True)
    left = sorted([u for u in us if u > 0.5 + eps])
    names = []
    for u in us:
        if u < 0.5 - eps:
            names.append('{}{}_{}'.format(nc['right'], base, str(right.index(u) + 1).zfill(2)))
        elif u > 0.5 + eps:
            names.append('{}{}_{}'.format(nc['left'], base, str(left.index(u) + 1).zfill(2)))
        else:
            names.append('Mid_{}'.format(base))
    return names


def cosine_weights(us, u):
    """(index, weight) of the two tweaks around u, smooth cosine falloff."""
    for k in range(len(us) - 1):
        if us[k] - 1e-6 <= u <= us[k + 1] + 1e-6:
            t = (u - us[k]) / max(us[k + 1] - us[k], 1e-9)
            w = 0.5 * (1 + math.cos(math.pi * min(max(t, 0.0), 1.0)))
            return [(i, x) for i, x in [(k, w), (k + 1, 1 - w)] if x > 1e-4]
    return [(0 if u < us[0] else len(us) - 1, 1.0)]


def axis_map(ctrl, carrier):
    """How the ctrl's local axes read in the carrier's frame at rest.

    vector[a][b]: local axis a -> carrier axis b (translate)
    det: -1 when the ctrl sits under a mirror group (rotations flip)
    scale[b]: local axis that scales carrier axis b
    """
    def rot(node):
        m = cmds.xform(node, q=True, ws=True, m=True)
        rows = [om.MVector(m[0:3]), om.MVector(m[4:7]), om.MVector(m[8:11])]
        return [r.normal() for r in rows]
    c = rot(ctrl)
    p = rot(carrier)
    vector = [[c[a] * p[b] for b in range(3)] for a in range(3)]
    det = ((c[0] ^ c[1]) * c[2]) * ((p[0] ^ p[1]) * p[2])
    scale = [max(range(3), key=lambda a: abs(vector[a][b])) for b in range(3)]
    return {'vector': vector, 'det': 1 if det > 0 else -1, 'scale': scale}


def weighted_sum(name, terms, constant=0.0):
    """blendWeighted output = constant + sum(plug * weight), None if empty."""
    if not terms and not constant:
        return None
    bw = cmds.createNode('blendWeighted', n=name)
    i = 0
    if constant:
        cmds.setAttr('{}.input[0]'.format(bw), constant)
        cmds.setAttr('{}.weight[0]'.format(bw), 1)
        i = 1
    for plug, weight in terms:
        cmds.connectAttr(plug, '{}.input[{}]'.format(bw, i))
        cmds.setAttr('{}.weight[{}]'.format(bw, i), weight)
        i += 1
    return bw + '.output'


def measure_point_weights(ctrls, points, threshold=0.02):
    """Move each ctrl 1 unit and record how far each point follows it.

    Returns {joint: [(ctrl, weight)]}, weight normalized so the point the
    ctrl moves most gets 1.0.
    """
    weights = {}
    rest = [cmds.xform(p['carrier'], q=True, ws=True, t=True) for p in points]
    for ctrl in ctrls:
        plug = ctrl + '.translateY'
        if not cmds.getAttr(plug, settable=True):
            continue
        value = cmds.getAttr(plug)
        cmds.setAttr(plug, value + 1)
        moved = [cmds.xform(p['carrier'], q=True, ws=True, t=True) for p in points]
        cmds.setAttr(plug, value)
        dist = [(om.MVector(m) - om.MVector(r)).length() for m, r in zip(moved, rest)]
        top = max(dist)
        if top < 1e-6:
            continue
        for p, d in zip(points, dist):
            if d / top > threshold:
                weights.setdefault(p['joint'], []).append((ctrl, d / top))
    return weights


def connect_zip(point, other_info, other_shape, zip_attrs):
    """Blend a point toward the middle of both lips with the corner Zip attrs.

    Each corner zips its own half, corner first (zip 0-3) to middle (7-10).
    """
    other = linear_curve_point(other_info, other_shape, param_from_fraction(other_shape, point['u']),
                               point['name'] + '_ZipOther')

    middle = cmds.createNode('plusMinusAverage', n=point['name'] + '_ZipMiddle_PMA')
    cmds.setAttr(middle + '.operation', 3)
    cmds.connectAttr(point['position'], middle + '.input3D[0]')
    cmds.connectAttr(other, middle + '.input3D[1]')

    blend = cmds.createNode('blendColors', n=point['name'] + '_Zip_BC')
    cmds.connectAttr(middle + '.output3D', blend + '.color1')
    cmds.connectAttr(point['position'], blend + '.color2')
    cmds.connectAttr(blend + '.output', point['carrier'] + '.translate', f=True)

    sides = []
    if point['u'] > 0.5 - 1e-4:
        sides.append((nc['left'], (1 - point['u']) * 2))
    if point['u'] < 0.5 + 1e-4:
        sides.append((nc['right'], point['u'] * 2))
    remaps = []
    for side, f in sides:
        remap = cmds.createNode('remapValue', n='{}_Zip{}Remap'.format(point['name'], side.replace('_', '')))
        cmds.connectAttr(zip_attrs[side], remap + '.inputValue')
        cmds.setAttr(remap + '.inputMin', f * 7)
        cmds.setAttr(remap + '.inputMax', f * 7 + 3)
        cmds.setAttr(remap + '.value[0].value_Interp', 2)
        cmds.setAttr(remap + '.value[1].value_Interp', 2)
        remaps.append(remap + '.outValue')
    if len(remaps) == 1:
        cmds.connectAttr(remaps[0], blend + '.blender')
    else:
        both = cmds.createNode('plusMinusAverage', n=point['name'] + '_Zip_PMA')
        for i, r in enumerate(remaps):
            cmds.connectAttr(r, '{}.input1D[{}]'.format(both, i))
        clamp = cmds.createNode('clamp', n=point['name'] + '_Zip_Clamp')
        cmds.setAttr(clamp + '.maxR', 1)
        cmds.connectAttr(both + '.output1D', clamp + '.inputR')
        cmds.connectAttr(clamp + '.outputR', blend + '.blender')


def linear_curve_point(curve_info, shape, param, name):
    """World position plug of a degree 1 curve at param, from its curveInfo.

    Exactly on a CV -> the CV itself; between two CVs -> a blendColors of both.
    """
    knots = list(_curve_fn(shape).knots())
    for k in range(len(knots) - 1):
        if knots[k] - 1e-6 <= param <= knots[k + 1] + 1e-6:
            t = (param - knots[k]) / max(knots[k + 1] - knots[k], 1e-9)
            if t < 1e-4:
                return '{}.controlPoints[{}]'.format(curve_info, k)
            if t > 1 - 1e-4:
                return '{}.controlPoints[{}]'.format(curve_info, k + 1)
            blend = cmds.createNode('blendColors', n=name + '_OnCurve_BC')
            cmds.connectAttr('{}.controlPoints[{}]'.format(curve_info, k + 1), blend + '.color1')
            cmds.connectAttr('{}.controlPoints[{}]'.format(curve_info, k), blend + '.color2')
            cmds.setAttr(blend + '.blender', t)
            return blend + '.output'
    return '{}.controlPoints[{}]'.format(curve_info, 0 if param < knots[0] else len(knots) - 1)


def follow_rotation(driver, nodes):
    """Same as orientConstraint(driver, node, mo=True) for nodes at rest
    identity under a still parent, with one multMatrix/decompose shared by all."""
    if not nodes:
        return
    rest = om.MMatrix(cmds.xform(driver, q=True, ws=True, m=True)).inverse()
    mult = cmds.createNode('multMatrix', n=driver + '_RestDelta_MM')
    cmds.setAttr(mult + '.matrixIn[0]', list(rest), type='matrix')
    cmds.connectAttr(driver + '.worldMatrix[0]', mult + '.matrixIn[1]')
    parent = cmds.listRelatives(nodes[0], p=True)
    if parent:
        cmds.connectAttr(parent[0] + '.worldInverseMatrix[0]', mult + '.matrixIn[2]')
    decompose = cmds.createNode('decomposeMatrix', n=driver + '_RestDelta_DM')
    cmds.connectAttr(mult + '.matrixSum', decompose + '.inputMatrix')
    for node in nodes:
        cmds.connectAttr(decompose + '.outputRotate', node + '.rotate')


def follow_matrix(source, target):
    """target copies source's world transform (target has no joint orient)."""
    mult = cmds.createNode('multMatrix', n=target + '_Follow_MM')
    cmds.connectAttr(source + '.worldMatrix[0]', mult + '.matrixIn[0]')
    parent = cmds.listRelatives(target, p=True)
    if parent:
        cmds.connectAttr(parent[0] + '.worldInverseMatrix[0]', mult + '.matrixIn[1]')
    decompose = cmds.createNode('decomposeMatrix', n=target + '_Follow_DM')
    cmds.connectAttr(mult + '.matrixSum', decompose + '.inputMatrix')
    cmds.connectAttr(decompose + '.outputTranslate', target + '.translate')
    cmds.connectAttr(decompose + '.outputRotate', target + '.rotate')
    cmds.connectAttr(decompose + '.outputScale', target + '.scale')
