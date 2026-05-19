from __future__ import absolute_import
from maya import cmds
import json
import os
from pathlib import Path

try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()

def create_orient_offset_block(name='OrientOffset'):
    PATH = os.path.dirname(__file__)
    MODULE_FILE = os.path.join(PATH, '06_Orient_Offset.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()

    name = mt.ask_name(text=module['Name'])
    if not name: return
    if cmds.objExists('{}{}'.format(name, nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name=name, icon=module['Icon'].replace('.png',''), attrs=module['attrs'], build_command=module['build_command'], import_command=module['import'])
    
    print('{} Created successfully'.format(name))

def build_orient_offset_block():
    nc, curve_data, setup = mt.import_configs()
    block = cmds.ls(sl=True)
    if not block:
        cmds.warning("Please select the OrientOffset block to build.")
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
                
        orient_name = name + '_Orient'
        
        # Capture existing orient values from the Block itself
        saved_orient = None
        safe_ctrl_name = ctrl.replace(':', '_').replace('|', '_')
        
        # Check if the block has the orient values saved
        if cmds.attributeQuery('{}_tx'.format(safe_ctrl_name), node=block, exists=True):
            saved_orient = {
                't': [cmds.getAttr('{}.{}_tx'.format(block, safe_ctrl_name)),
                      cmds.getAttr('{}.{}_ty'.format(block, safe_ctrl_name)),
                      cmds.getAttr('{}.{}_tz'.format(block, safe_ctrl_name))],
                'r': [cmds.getAttr('{}.{}_rx'.format(block, safe_ctrl_name)),
                      cmds.getAttr('{}.{}_ry'.format(block, safe_ctrl_name)),
                      cmds.getAttr('{}.{}_rz'.format(block, safe_ctrl_name))],
                's': [cmds.getAttr('{}.{}_sx'.format(block, safe_ctrl_name)),
                      cmds.getAttr('{}.{}_sy'.format(block, safe_ctrl_name)),
                      cmds.getAttr('{}.{}_sz'.format(block, safe_ctrl_name))]
            }
            cmds.warning('ORIENT SAVE: loaded values from block node for {}'.format(ctrl))
        else:
            # Create the hidden attributes on the block to store values
            for attr in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']:
                cmds.addAttr(block, longName='{}_{}'.format(safe_ctrl_name, attr), attributeType='double', defaultValue=0.0)
            for attr in ['sx', 'sy', 'sz']:
                cmds.addAttr(block, longName='{}_{}'.format(safe_ctrl_name, attr), attributeType='double', defaultValue=1.0)
            
        # If orient already exists in the scene, warn and skip to avoid duplicate hierarchy
        if cmds.objExists(orient_name):
            cmds.warning("{} already has an orient setup. Skipping recreation to avoid duplication.".format(ctrl))
            continue
            
        orient_root = cmds.group(em=True, name=name + '_Orient_Root')
        ctrl_parent = cmds.listRelatives(ctrl, parent=True)
        if ctrl_parent:
            cmds.parent(orient_root, ctrl_parent[0])
            
        # Match orient root to control's world position before reparenting
        cmds.matchTransform(orient_root, ctrl, pos=True, rot=True, scl=False)
        
        orient_node = cmds.group(em=True, name=orient_name)
        cmds.parent(orient_node, orient_root)
            
        for attr in ['tx','ty','tz','rx','ry','rz']:
            cmds.setAttr('{}.{}'.format(orient_node, attr), 0)
        for attr in ['sx','sy','sz']:
            cmds.setAttr('{}.{}'.format(orient_node, attr), 1)
            
        for attr in ['tx','ty','tz','rx','ry','rz','sx','sy','sz']:
            cmds.setAttr('{}.{}'.format(orient_node, attr), keyable=False, channelBox=True)

        # Reparent existing children if auto_parent is True
        existing_children = cmds.listRelatives(ctrl, children=True, type='transform') or []
        # exclude shapes
        shapes = cmds.listRelatives(ctrl, shapes=True) or []
        children_to_reparent = [c for c in existing_children if c not in shapes]

        cmds.parent(ctrl, orient_node)
        cmds.addAttr(ctrl, longName='ctrlOrient', niceName='_________',
                     attributeType='enum', enumName='Ctrl Orient', keyable=True)
        cmds.setAttr('{}.ctrlOrient'.format(ctrl), lock=True)

        for axis in ['X', 'Y', 'Z']:
            attr_name = 'orientTranslate{}'.format(axis)
            cmds.addAttr(ctrl, longName=attr_name, attributeType='doubleLinear',
                         usedAsProxy=True)
            cmds.setAttr('{}.{}'.format(ctrl, attr_name), channelBox=True)
            cmds.connectAttr('{}.t{}'.format(orient_node, axis.lower()),
                             '{}.{}'.format(ctrl, attr_name))

        for axis in ['X', 'Y', 'Z']:
            attr_name = 'orientRotate{}'.format(axis)
            cmds.addAttr(ctrl, longName=attr_name, attributeType='doubleAngle',
                         usedAsProxy=True)
            cmds.setAttr('{}.{}'.format(ctrl, attr_name), channelBox=True)
            cmds.connectAttr('{}.r{}'.format(orient_node, axis.lower()),
                             '{}.{}'.format(ctrl, attr_name))

        for axis in ['X', 'Y', 'Z']:
            attr_name = 'orientScale{}'.format(axis)
            cmds.addAttr(ctrl, longName=attr_name, attributeType='double',
                         defaultValue=1.0, usedAsProxy=True)
            cmds.setAttr('{}.{}'.format(ctrl, attr_name), channelBox=True)
            cmds.connectAttr('{}.s{}'.format(orient_node, axis.lower()),
                             '{}.{}'.format(ctrl, attr_name))

        driven_node = cmds.group(em=True, name=name + '_Driven')
        cmds.parent(driven_node, orient_root)
        cmds.setAttr('{}.tx'.format(driven_node), 0)
        cmds.setAttr('{}.ty'.format(driven_node), 0)
        cmds.setAttr('{}.tz'.format(driven_node), 0)

        ctrl_dcmp = cmds.createNode('decomposeMatrix', name=name + '_Ctrl_Decomp')
        ctrl_comp_tr = cmds.createNode('composeMatrix', name=name + '_Ctrl_TR_Comp')
        
        cmds.connectAttr('{}.m'.format(ctrl), '{}.imat'.format(ctrl_dcmp))
        cmds.connectAttr('{}.ot'.format(ctrl_dcmp), '{}.it'.format(ctrl_comp_tr))
        cmds.connectAttr('{}.or'.format(ctrl_dcmp), '{}.ir'.format(ctrl_comp_tr))
        cmds.connectAttr('{}.osh'.format(ctrl_dcmp), '{}.ish'.format(ctrl_comp_tr))
        
        ctrl_comp_s = cmds.createNode('composeMatrix', name=name + '_Ctrl_S_Comp')
        cmds.connectAttr('{}.os'.format(ctrl_dcmp), '{}.is'.format(ctrl_comp_s))
        
        orient_dcmp = cmds.createNode('decomposeMatrix', name=name + '_Orient_Decomp')
        orient_comp_r = cmds.createNode('composeMatrix', name=name + '_Orient_R_Comp')
        cmds.connectAttr('{}.m'.format(orient_node), '{}.imat'.format(orient_dcmp))
        cmds.connectAttr('{}.or'.format(orient_dcmp), '{}.ir'.format(orient_comp_r))
        
        orient_comp_r_inv = cmds.createNode('inverseMatrix', name=name + '_Orient_R_Inv')
        cmds.connectAttr('{}.outputMatrix'.format(orient_comp_r), '{}.inputMatrix'.format(orient_comp_r_inv))
        
        m1 = cmds.createNode('multMatrix', name=name + '_M1')
        cmds.connectAttr('{}.im'.format(orient_node), '{}.i[0]'.format(m1))
        cmds.connectAttr('{}.outputMatrix'.format(ctrl_comp_tr), '{}.i[1]'.format(m1))
        cmds.connectAttr('{}.m'.format(orient_node), '{}.i[2]'.format(m1))
        
        m2 = cmds.createNode('multMatrix', name=name + '_M2')
        cmds.connectAttr('{}.outputMatrix'.format(orient_comp_r_inv), '{}.i[0]'.format(m2))
        cmds.connectAttr('{}.outputMatrix'.format(ctrl_comp_s), '{}.i[1]'.format(m2))
        cmds.connectAttr('{}.outputMatrix'.format(orient_comp_r), '{}.i[2]'.format(m2))
        
        m_final = cmds.createNode('multMatrix', name=name + '_M_Final')
        cmds.connectAttr('{}.matrixSum'.format(m2), '{}.i[0]'.format(m_final))
        cmds.connectAttr('{}.matrixSum'.format(m1), '{}.i[1]'.format(m_final))

        final_dcmp = cmds.createNode('decomposeMatrix', name=name + '_Final_Decomp')
        cmds.connectAttr('{}.matrixSum'.format(m_final), '{}.imat'.format(final_dcmp))

        cmds.connectAttr('{}.ot'.format(final_dcmp), '{}.t'.format(driven_node))
        cmds.connectAttr('{}.or'.format(final_dcmp), '{}.r'.format(driven_node))
        cmds.connectAttr('{}.os'.format(final_dcmp), '{}.s'.format(driven_node))
        cmds.connectAttr('{}.osh'.format(final_dcmp), '{}.sh'.format(driven_node))

        for attr in ['tx','ty','tz','rx','ry','rz','sx','sy','sz']:
            cmds.setAttr('{}.{}'.format(driven_node, attr), lock=True)
            
        if auto_parent and children_to_reparent:
            for child in children_to_reparent:
                cmds.parent(child, driven_node)

        # Rewire constraints from ctrl to driven_node if auto_parent is True
        if auto_parent:
            constraints = list(set(cmds.listConnections(ctrl, source=False, destination=True, type='constraint') or []))
            for cns in constraints:
                cns_type = cmds.nodeType(cns)
                driven_objs = list(set(cmds.listConnections(cns, source=False, destination=True, type='transform') or []))
                for obj in driven_objs:
                    if obj in [orient_node, driven_node, ctrl, orient_root]: continue
                    try:
                        if cns_type == 'parentConstraint':
                            cmds.parentConstraint(driven_node, obj, mo=True)
                            cmds.parentConstraint(ctrl, obj, rm=True)
                        elif cns_type == 'scaleConstraint':
                            cmds.scaleConstraint(driven_node, obj, mo=True)
                            cmds.scaleConstraint(ctrl, obj, rm=True)
                        elif cns_type == 'pointConstraint':
                            cmds.pointConstraint(driven_node, obj, mo=True)
                            cmds.pointConstraint(ctrl, obj, rm=True)
                        elif cns_type == 'orientConstraint':
                            cmds.orientConstraint(driven_node, obj, mo=True)
                            cmds.orientConstraint(ctrl, obj, rm=True)
                    except Exception as e:
                        cmds.warning("Failed to rewire {} to {}: {}".format(cns_type, obj, e))

        if saved_orient:
            cmds.setAttr('{}.tx'.format(orient_node), saved_orient['t'][0])
            cmds.setAttr('{}.ty'.format(orient_node), saved_orient['t'][1])
            cmds.setAttr('{}.tz'.format(orient_node), saved_orient['t'][2])
            cmds.setAttr('{}.rx'.format(orient_node), saved_orient['r'][0])
            cmds.setAttr('{}.ry'.format(orient_node), saved_orient['r'][1])
            cmds.setAttr('{}.rz'.format(orient_node), saved_orient['r'][2])
            cmds.setAttr('{}.sx'.format(orient_node), saved_orient['s'][0])
            cmds.setAttr('{}.sy'.format(orient_node), saved_orient['s'][1])
            cmds.setAttr('{}.sz'.format(orient_node), saved_orient['s'][2])
                
        # Connect the _Orient node directly to the block's storage attributes
        # This guarantees that the block always stores the latest values and retains them on deletion.
        for attr in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']:
            cmds.connectAttr('{}.{}'.format(orient_node, attr), '{}.{}_{}'.format(block, safe_ctrl_name, attr), force=True)
                
    print('Build OrientOffset on controls sucessful')
