from __future__ import absolute_import
from maya import cmds
import json
import os
from pathlib import Path

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload
reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()

#---------------------------------------------

def create_custom_finger_scales_block(name='Custom_Finger_Scales'):
    PATH = os.path.dirname(__file__)
    MODULE_FILE = os.path.join(PATH, 'custom_finger_scales.json')
    if not os.path.exists(MODULE_FILE):
        cmds.warning('custom_finger_scales.json not found.')
        return ''
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)
    nc, curve_data, setup = mt.import_configs()
    name = mt.ask_name(text=module['Name'])
    if cmds.objExists('{}{}'.format(name, nc['module'])):
        cmds.warning('Name already exists.')
        return ''
    block = mt.create_block(name=name, icon='FingersScale', attrs=module['attrs'], build_command=module['build_command'], import_command=module['import'])
    config = block[1]
    block = block[0]
    cmds.select(block)
    print('{} Created Successfully'.format(name))


def build_custom_finger_scales_block():

    nc, curve_data, setup = mt.import_configs()
    mt.check_is_there_is_base()
    block = cmds.ls(sl=True)
    if not block:
        cmds.warning('Select a block to build.')
        return
    config = cmds.listConnections(block)[1]
    block = block[0]
    name = block.replace(nc['module'], '')
    sides = ['L', 'R']
    fingers = ['Index', 'Middle', 'Ring', 'Pinky', 'Thumb']
    # Parent all finger joints to Palm_Jnt and delete scale constraints
    for side in sides:
        palm_jnt = '{}_Hand_Palm{}'.format(side, nc['joint'])
        for finger in fingers:
            for seg in range(0, 5):  # 0-4 for all phalanges
                jnt = '{}_Hand_{}_0{}_Jnt'.format(side, finger, seg)
                if not cmds.objExists(jnt):
                    continue
                # Parent to palm
                try:
                    cmds.parent(jnt, palm_jnt)
                except Exception as exc:
                    cmds.warning('Could not parent {} to {} ({})'.format(jnt, palm_jnt, exc))
                # Delete scale constraints
                constraints = cmds.listConnections(jnt, type='scaleConstraint', d=False, s=True) or []
                for c in constraints:
                    if cmds.objExists(c):
                        try:
                            cmds.delete(c)
                        except Exception as exc:
                            cmds.warning('Could not delete constraint {} ({})'.format(c, exc))
                # Connect control scale to joint with remap
                ctrl = '{}_Hand_{}_0{}_Ctrl'.format(side, finger, seg)
                if cmds.objExists(ctrl):
                    try:
                        cmds.connectAttr(ctrl+'.scaleX', jnt+'.scaleZ', f=True)
                        cmds.connectAttr(ctrl+'.scaleY', jnt+'.scaleX', f=True)
                        cmds.connectAttr(ctrl+'.scaleZ', jnt+'.scaleY', f=True)
                    except Exception as exc:
                        cmds.warning('Scale connect failed {} -> {} ({})'.format(ctrl, jnt, exc))

                    #Remove child finger from controller
                    cltr_child = cmds.listRelatives(ctrl, c=True, type='transform') or []
                    print("#"*20)
                    print("Checking cltr_child {} of {}".format(cltr_child, ctrl))
                    print("#"*20)
                    for child in cltr_child:
                        if cmds.objExists(child):
                            cmds.parent(child, '{}_Hand_Palm_Ctrl_Grp'.format(side))
                            cmds.parentConstraint(ctrl, child, mo=True)

    print('Custom Finger Scales block built. All finger joints parented to Palm_Jnt and scale constraints removed for both L_ and R_.')
