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
PYBLOCK_NAME = 'exec_custom_biped_rotate_orders'

ROTATE_ORDER_INDEX = {
    'xyz': 0,
    'yzx': 1,
    'zxy': 2,
    'xzy': 3,
    'yxz': 4,
    'zyx': 5
}

ROTATE_ORDER_DICT = {
    'xzy': [
        'Head_Ctrl',
        'Neck_Ctrl',
        'COG_Ctrl',
        'Spine_Bottom_Ik_Ctrl',
        'Spine_Base_FK_Ctrl',
        'Spine_Belly_FK_Ctrl',
        'Spine_Chest_FK_Ctrl',
        'Spine_Chest_Top_IK_Ctrl',
        'Spine_Belly_IK_Ctrl',
        'L_Hip_Fk_Ctrl',
        'L_Knee_Fk_Ctrl',
        'L_Ankle_Fk_Ctrl',
        'L_Ankle_Ik_Ctrl'
    ],
    'xyz': [
        'L_Clavicle_Ctrl',
        'L_Shoulder_Fk_Ctrl',
        'L_Elbow_Fk_Ctrl',
        'L_Wrist_Fk_Ctrl',
        'L_Wrist_Ik_Ctrl',
        'L_Hand_Ring_01_Ctrl', 'L_Hand_Wrist_Ctrl', 'L_Hand_Ring_03_Ctrl',
        'L_Hand_Pinky_03_Ctrl', 'L_Hand_Pinky_02_Ctrl', 'L_Hand_Ring_02_Ctrl',
        'L_Hand_Palm_Ctrl', 'L_Hand_Middle_02_Ctrl', 'L_Hand_Pinky_01_Ctrl',
        'L_Hand_Thumb_01_Ctrl', 'L_Hand_Middle_01_Ctrl', 'L_Hand_Thumb_02_Ctrl',
        'L_Hand_OutterCup_Ctrl', 'L_Hand_Thumb_00_Ctrl', 'L_Hand_Middle_03_Ctrl',
        'L_Hand_Pinky_00_Ctrl', 'L_Hand_Ring_00_Ctrl', 'L_Hand_Middle_00_Ctrl',
        'L_Hand_Index_00_Ctrl', 'L_Hand_Index_01_Ctrl', 'L_Hand_InnerCup_Ctrl',
        'L_Hand_Index_02_Ctrl', 'L_Hand_Index_03_Ctrl'
    ]
}

#---------------------------------------------

def create_custom_biped_rotate_orders_block(name='Custom_Biped_Rotate_Orders'):

    #---------------------------------------------------
    #---------------------------------------------------
    #---------------------------------------------------

    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-2]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '05_Custom_Biped_Rotate_Orders.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()

    #---------------------------------------------------
    #---------------------------------------------------
    #---------------------------------------------------

    name = mt.ask_name(text=module['Name'])
    if cmds.objExists('{}{}'.format(name, nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(
        name=name,
        icon='Custom_Biped_Rotate_Orders',
        attrs=module['attrs'],
        build_command=module['build_command'],
        import_command=module['import']
    )
    config = block[1]
    block = block[0]

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_custom_biped_rotate_orders_block()

#-------------------------

def build_custom_biped_rotate_orders_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    name = block.replace(nc['module'], '')

    processed = set()

    for order_name, ctrl_list in ROTATE_ORDER_DICT.items():
        order_name = order_name.lower()
        if order_name not in ROTATE_ORDER_INDEX:
            cmds.warning('Custom Biped Rotate Orders: invalid rotate order {}.'.format(order_name))
            continue

        order_index = ROTATE_ORDER_INDEX[order_name]


        for ctrl in ctrl_list:
            candidate_ctrls = [ctrl]
            if ctrl.startswith('L_'):
                candidate_ctrls.append(ctrl.replace('L_', 'R_', 1))

            for candidate in candidate_ctrls:
                if candidate in processed:
                    continue
                processed.add(candidate)

                if not cmds.objExists(candidate):
                    continue

                # Try both attribute names, set if exists, ignore errors for locked/connected
                for rotate_attr in ['rotateOrder', 'RotateOrder']:
                    if cmds.attributeQuery(rotate_attr, node=candidate, exists=True):
                        try:
                            cmds.setAttr('{}.{}'.format(candidate, rotate_attr), order_index)
                        except Exception as exc:
                            # Only warn if both failb
                            pass

    print('Custom Biped Rotate Orders: rotate orders updated successfully.')

#build_custom_biped_rotate_orders_block()
