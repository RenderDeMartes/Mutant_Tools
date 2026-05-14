from __future__ import absolute_import
from maya import cmds
import json
import os

try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()

def create_scale_isolate_block(name='ScaleIsolate'):
    PATH = os.path.dirname(__file__)
    MODULE_FILE = os.path.join(PATH, '07_Scale_Isolate.json')
    if not os.path.exists(MODULE_FILE):
        cmds.warning('07_Scale_Isolate.json not found.')
        return ''
        
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()

    name = mt.ask_name(text=module['Name'])
    if not name: return
    if cmds.objExists('{}{}'.format(name, nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name=name, icon=module['Icon'], attrs=module['attrs'], build_command=module['build_command'], import_command=module['import'])
    
    print('{} Created successfully'.format(name))

def build_scale_isolate_block():
    nc, curve_data, setup = mt.import_configs()
    block = cmds.ls(sl=True)
    if not block:
        cmds.warning("Please select the ScaleIsolate block to build.")
        return
        
    config = cmds.listConnections(block)[1]
    block = block[0]
    
    controls_string = cmds.getAttr('{}.SetControlsList'.format(config), asString=True)
    auto_parent = cmds.getAttr('{}.AutoParentChildren'.format(config))

    if not controls_string:
        cmds.warning("No controls defined in SetControlsList.")
        return

    controls = [c.strip() for c in controls_string.split(',') if c.strip()]
    
    for ctrl in controls:
        if not cmds.objExists(ctrl):
            cmds.warning("Control {} does not exist. Skipping.".format(ctrl))
            continue
            
        # extract name without suffix if possible
        name = ctrl
        for suffix in [nc['ctrl'], '_Ctrl', '_ctrl']:
            if name.endswith(suffix):
                name = name[:-len(suffix)]
                break
                
        driven_name = name + '_ScaleIsolated'
        
        if cmds.objExists(driven_name):
            cmds.warning("{} already has a scale isolate setup. Skipping recreation to avoid duplication.".format(ctrl))
            continue
            
        driven_node = cmds.group(em=True, name=driven_name)
        ctrl_parent = cmds.listRelatives(ctrl, parent=True)
        if ctrl_parent:
            cmds.parent(driven_node, ctrl_parent[0])
            
        # Match offsetParentMatrix if it exists
        if cmds.attributeQuery('offsetParentMatrix', node=ctrl, exists=True):
            cmds.connectAttr('{}.offsetParentMatrix'.format(ctrl), '{}.offsetParentMatrix'.format(driven_node))

        # Match rotateOrder before decomposition to avoid flipping
        cmds.connectAttr('{}.rotateOrder'.format(ctrl), '{}.rotateOrder'.format(driven_node))

        # Using decomposeMatrix to cleanly extract T, R, and Shear while ignoring Scale
        ctrl_dcmp = cmds.createNode('decomposeMatrix', name=name + '_Ctrl_Decomp')
        cmds.connectAttr('{}.matrix'.format(ctrl), '{}.imat'.format(ctrl_dcmp))
        cmds.connectAttr('{}.rotateOrder'.format(ctrl), '{}.inputRotateOrder'.format(ctrl_dcmp))
        
        cmds.connectAttr('{}.ot'.format(ctrl_dcmp), '{}.t'.format(driven_node))
        cmds.connectAttr('{}.or'.format(ctrl_dcmp), '{}.r'.format(driven_node))
        cmds.connectAttr('{}.osh'.format(ctrl_dcmp), '{}.sh'.format(driven_node))
        
        # Lock driven_node attributes
        for attr in ['tx','ty','tz','rx','ry','rz','sx','sy','sz']:
            cmds.setAttr('{}.{}'.format(driven_node, attr), lock=True)

        # Reparent existing children if auto_parent is True
        existing_children = cmds.listRelatives(ctrl, children=True, type='transform') or []
        shapes = cmds.listRelatives(ctrl, shapes=True) or []
        children_to_reparent = [c for c in existing_children if c not in shapes]

        if auto_parent and children_to_reparent:
            for child in children_to_reparent:
                cmds.parent(child, driven_node)

                        
    print('Build ScaleIsolate on controls sucessful')
