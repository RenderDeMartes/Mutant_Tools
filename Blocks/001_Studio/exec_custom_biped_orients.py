from __future__ import absolute_import
from maya import cmds
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

TAB_FOLDER = '001_Studio'
PYBLOCK_NAME = 'exec_custom_biped_orients'

#---------------------------------------------

def create_custom_biped_orients_block(name='Custom_Biped_Orients'):

    #---------------------------------------------------
    #---------------------------------------------------
    #---------------------------------------------------

    # Read name conventions as nc[''] and setup as seup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-2]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '04_Custom_Biped_Orients.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()

    #---------------------------------------------------
    #---------------------------------------------------
    #---------------------------------------------------

    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name = name, icon = 'Custom_Biped_Orients',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]

    #cmds.getAttr('{}.AttrName'.format(config)) #get attrs from config
    #cmds.getAttr('{}.AttrName'.format(config), asString = True) #for enums
    #joint_one = mt.create_joint_guide(name = name) #guide base with shapes

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_custom_biped_orients_block()

#-------------------------

def build_custom_biped_orients_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    name = block.replace(nc['module'],'')

    def _get_bool_attr(attr_name, default=True):
        if cmds.attributeQuery(attr_name, n=config, exists=True):
            return cmds.getAttr('{}.{}'.format(config, attr_name))
        return default

    fix_arms = _get_bool_attr('FixArms')
    fix_clavicles = _get_bool_attr('FixClavicles')
    fix_pelvis = _get_bool_attr('FixPelvis')
    fix_legs = _get_bool_attr('FixLegs')
    fix_toes = _get_bool_attr('FixToes')
    fix_fingers = _get_bool_attr('FixFingers')
    fix_misc = _get_bool_attr('FixMisc')

    def _get_constraints(ctrl):
        constraints = cmds.listConnections(
            ctrl,
            type='constraint',
            source=True,
            destination=True
        ) or []
        return list(set(constraints))

    def _get_constrained_joints(constraint):
        constrained = cmds.listConnections(
            constraint,
            source=False,
            destination=True,
            type='joint'
        ) or []
        return list(set(constrained))

    def _apply_orient_fix(ctrls, right_ctrls, default_rotate, section_name, custom_rotate_by_ctrl=None):
        if not ctrls:
            cmds.warning('Custom Biped Orients: no ctrls provided for {}.'.format(section_name))
            return

        constraints_data = []
        constraints_to_delete = []

        for ctrl in ctrls:
            if not cmds.objExists(ctrl):
                cmds.warning('Custom Biped Orients: ctrl not found: {}'.format(ctrl))
                continue

            constraints = _get_constraints(ctrl)
            for constraint in constraints:
                if not cmds.objExists(constraint):
                    continue

                constraint_type = cmds.nodeType(constraint)
                constrained_joints = _get_constrained_joints(constraint)
                if not constrained_joints:
                    continue

                for joint in constrained_joints:
                    constraints_data.append((ctrl, joint, constraint_type))

                constraints_to_delete.append(constraint)
                print('{} -> {} -> {}'.format(ctrl, constraint, constrained_joints))

        if constraints_to_delete:
            cmds.delete(list(set(constraints_to_delete)))

        for ctrl in ctrls:
            if not cmds.objExists(ctrl):
                continue

            children = cmds.listRelatives(ctrl, c=True, type='transform') or []
            world_children = []
            for child in children:
                if not cmds.objExists(child):
                    continue
                try:
                    cmds.parent(child, world=True)
                    world_children.append(child)
                except Exception as exc:
                    cmds.warning('Custom Biped Orients: could not unparent {} from {} ({})'.format(child, ctrl, exc))

            root_grp = mt.root_grp(input=ctrl, custom=True, custom_name='OrientChange')[0]
            rotate = default_rotate
            if custom_rotate_by_ctrl and ctrl in custom_rotate_by_ctrl:
                rotate = custom_rotate_by_ctrl[ctrl]
            cmds.rotate(rotate[0], rotate[1], rotate[2], root_grp, relative=True, objectSpace=True)

            if ctrl in right_ctrls:
                try:
                    cmds.setAttr('{}.translate'.format(root_grp), 0, 0, 0)
                    cmds.setAttr('{}.rotate'.format(root_grp), rotate[0], rotate[1], rotate[2])
                    cmds.setAttr('{}.scale'.format(root_grp), 1, 1, 1)

                    cmds.setAttr('{}.translate'.format(ctrl), 0, 0, 0)
                    cmds.setAttr('{}.rotate'.format(ctrl), 0, 0, 0)
                    try:
                        cmds.setAttr('{}.scale'.format(ctrl), 1, 1, 1)
                    except Exception as exc:
                        print
                except Exception as exc:
                    cmds.warning('Custom Biped Orients: could not force right-side attrs on {} ({})'.format(ctrl, exc))

            for child in world_children:
                if not cmds.objExists(child) or not cmds.objExists(ctrl):
                    continue
                try:
                    cmds.parent(child, ctrl)
                except Exception as exc:
                    cmds.warning('Custom Biped Orients: could not reparent {} to {} ({})'.format(child, ctrl, exc))

        for ctrl, joint, constraint_type in constraints_data:
            if not cmds.objExists(ctrl) or not cmds.objExists(joint):
                continue

            try:
                if constraint_type == 'orientConstraint':
                    cmds.orientConstraint(ctrl, joint, mo=True)
                elif constraint_type == 'parentConstraint':
                    cmds.parentConstraint(ctrl, joint, mo=True)
                elif constraint_type == 'pointConstraint':
                    cmds.pointConstraint(ctrl, joint, mo=True)
                elif constraint_type == 'scaleConstraint':
                    cmds.scaleConstraint(ctrl, joint, mo=True)
            except Exception as exc:
                cmds.warning(
                    'Custom Biped Orients: failed to recreate {} from {} to {} ({})'.format(
                        constraint_type, ctrl, joint, exc
                    )
                )

        print('Custom Biped Orients: {} orient fix applied.'.format(section_name))

    if fix_arms or fix_clavicles:

        # Clean old constraints
        for c in [
            'L_Hand_Middle_03_Smart_Ctrl_Root_Grp_parentConstraint1',
            'R_Hand_Middle_03_Smart_Ctrl_Root_Grp_parentConstraint1'
        ]:
            if cmds.objExists(c):
                try:
                    cmds.delete(c)
                except Exception as exc:
                    print(exc)

        # Rotations
        arm_rotate = [-90, -90, 0]
        clavicle_rotate = [-90, 0, 0]
        #clavicle_rotate = [0, -90, -90]
        wrist_rotate = [0, 0, -90]

        left_ctrls = []
        right_ctrls = []
        arm_ctrls = []
        clavicle_ctrls = []

        # Arms
        if fix_arms:
            left_arm_ctrls = [
                'L_Shoulder_Fk_Ctrl',
                'L_Elbow_Fk_Ctrl',
                'L_Wrist_Fk_Ctrl',
                'L_Hand_Wrist_Ctrl'
            ]
            right_arm_ctrls = [
                'R_Shoulder_Fk_Ctrl',
                'R_Elbow_Fk_Ctrl',
                'R_Wrist_Fk_Ctrl',
                'R_Hand_Wrist_Ctrl'
            ]

            left_ctrls.extend(left_arm_ctrls)
            right_ctrls.extend(right_arm_ctrls)
            arm_ctrls.extend(left_arm_ctrls + right_arm_ctrls)

        # Clavicles
        if fix_clavicles:
            left_clavicle_ctrl = 'L_Clavicle_Ctrl'
            right_clavicle_ctrl = 'R_Clavicle_Ctrl'

            left_ctrls.append(left_clavicle_ctrl)
            right_ctrls.append(right_clavicle_ctrl)
            clavicle_ctrls.extend([left_clavicle_ctrl, right_clavicle_ctrl])

        fk_arm_ctrls = left_ctrls + right_ctrls

        # --- Custom rotation overrides ---
        ctrl_rotates = {}

        # Clavicles
        for ctrl in clavicle_ctrls:
            ctrl_rotates[ctrl] = clavicle_rotate

        # Wrists (this is what you were missing)
        wrist_ctrls = [
            'L_Wrist_Fk_Ctrl', 'L_Hand_Wrist_Ctrl',
            'R_Wrist_Fk_Ctrl', 'R_Hand_Wrist_Ctrl'
        ]

        for ctrl in wrist_ctrls:
            if ctrl in fk_arm_ctrls:
                ctrl_rotates[ctrl] = wrist_rotate

        # Apply orient fix
        _apply_orient_fix(
            ctrls=fk_arm_ctrls,
            right_ctrls=right_ctrls,
            default_rotate=arm_rotate,
            section_name='FK arms/clavicles',
            custom_rotate_by_ctrl=ctrl_rotates
        )

        # Recreate constraints
        try:
            cmds.parentConstraint(
                "R_Hand_Wrist_Ctrl",
                "R_Hand_Middle_03_Smart_Ctrl_Root_Grp",
                mo=True
            )
            cmds.parentConstraint(
                "L_Hand_Wrist_Ctrl",
                "L_Hand_Middle_03_Smart_Ctrl_Root_Grp",
                mo=True
            )
        except Exception as exc:
            print(exc)
        
    if fix_legs:
        leg_rotate = [-90, -90, 0]

        left_leg_ctrls = ['L_Hip_Fk_Ctrl', 'L_Knee_Fk_Ctrl', 'L_Ankle_Fk_Ctrl']
        right_leg_ctrls = ['R_Hip_Fk_Ctrl', 'R_Knee_Fk_Ctrl', 'R_Ankle_Fk_Ctrl']
        fk_leg_ctrls = left_leg_ctrls + right_leg_ctrls

        _apply_orient_fix(
            ctrls=fk_leg_ctrls,
            right_ctrls=right_leg_ctrls,
            default_rotate=leg_rotate,
            section_name='FK legs'
        )

    if fix_pelvis:
        pelvis_rotate = [-90, -90, 0]

        left_pelvis_ctrls = ['L_Pelvis_Ctrl']
        right_pelvis_ctrls = ['R_Pelvis_Ctrl']
        fk_pelvis_ctrls = left_pelvis_ctrls + right_pelvis_ctrls

        _apply_orient_fix(
            ctrls=fk_pelvis_ctrls,
            right_ctrls=right_pelvis_ctrls,
            default_rotate=pelvis_rotate,
            section_name='FK pelvis'
        )

    if fix_toes:
        toes_rotate = [0, 90, 0]

        left_toes_ctrls = ['L_Foot_Toes_Ctrl']
        right_toes_ctrls = ['R_Foot_Toes_Ctrl']
        fk_toes_ctrls = left_toes_ctrls + right_toes_ctrls

        _apply_orient_fix(
            ctrls=fk_toes_ctrls,
            right_ctrls=right_toes_ctrls,
            default_rotate=toes_rotate,
            section_name='FK toes'
        )
    if fix_fingers:
        try:
            cmds.delete('L_Hand_Middle_03_Smart_Ctrl_Root_Grp_parentConstraint1')
            cmds.delete('R_Hand_Middle_03_Smart_Ctrl_Root_Grp_parentConstraint1')
        except Exception as exc:
            print(exc)

        four_fingers_rotate = [-90, 90, 0]
        thumb_rotate = [-90, 90, 0]
        hand_other_rotate = [-90, 90, 0]

        four_fingers_tokens = ['_Index_', '_Middle_', '_Ring_', '_Pinky_']

        hand_ctrls = []
        for side in ['L', 'R']:
            for finger in ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']:
                for segment in range(0, 4):
                    ctrl = '{}_Hand_{}_0{}_Ctrl'.format(side, finger, segment)
                    if cmds.objExists(ctrl):
                        hand_ctrls.append(ctrl)

        hand_ctrls = sorted(set(hand_ctrls))

        if hand_ctrls:
            right_hand_ctrls = [ctrl for ctrl in hand_ctrls if ctrl.startswith('R_')]

            thumb_ctrls = [ctrl for ctrl in hand_ctrls if '_Thumb_' in ctrl]
            four_fingers_ctrls = [
                ctrl for ctrl in hand_ctrls
                if any(token in ctrl for token in four_fingers_tokens)
            ]
            hand_other_ctrls = [
                ctrl for ctrl in hand_ctrls
                if ctrl not in thumb_ctrls and ctrl not in four_fingers_ctrls
            ]

            ctrl_rotates = {}
            for ctrl in thumb_ctrls:
                ctrl_rotates[ctrl] = thumb_rotate
            for ctrl in hand_other_ctrls:
                ctrl_rotates[ctrl] = hand_other_rotate

            _apply_orient_fix(
                ctrls=hand_ctrls,
                right_ctrls=right_hand_ctrls,
                default_rotate=four_fingers_rotate,
                section_name='FK fingers',
                custom_rotate_by_ctrl=ctrl_rotates
            )

        try:
            cmds.parentConstraint("R_Hand_Wrist_Ctrl","R_Hand_Middle_03_Smart_Ctrl_Root_Grp", mo=True)
            cmds.parentConstraint("L_Hand_Wrist_Ctrl","L_Hand_Middle_03_Smart_Ctrl_Root_Grp", mo=True)
        except Exception as exc:
            print(exc)

        else:
            cmds.warning('Custom Biped Orients: no hand ctrls found for fingers section.')
    if fix_misc:
        cmds.warning('Custom Biped Orients: misc changes not defined yet.')
    if not (fix_arms or fix_clavicles or fix_pelvis or fix_legs or fix_toes or fix_fingers or fix_misc):
        cmds.warning('Custom Biped Orients: no sections enabled.')

    


#build_custom_biped_orients_block()
