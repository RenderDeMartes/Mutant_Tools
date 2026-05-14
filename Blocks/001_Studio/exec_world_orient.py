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

def create_world_orient_block(name='WorldOrient'):
    PATH = os.path.dirname(__file__)
    MODULE_FILE = os.path.join(PATH, '08_World_Orient.json')
    if not os.path.exists(MODULE_FILE):
        cmds.warning('08_World_Orient.json not found.')
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

def build_world_orient_block():
    nc, curve_data, setup = mt.import_configs()
    block = cmds.ls(sl=True)
    if not block:
        cmds.warning("Please select the WorldOrient block to build.")
        return
        
    config = cmds.listConnections(block)[1]
    block = block[0]
    
    controls_string = cmds.getAttr('{}.SetControlsList'.format(config), asString=True)

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
                
        driven_name = name + '_WorldOriented'
        
        if cmds.objExists(driven_name):
            cmds.warning("{} already has a WorldOrient setup. Skipping recreation to avoid duplication.".format(ctrl))
            continue
            
        ctrl_parent = cmds.listRelatives(ctrl, parent=True)
        if not ctrl_parent:
            cmds.warning("{} has no parent. It is already world oriented. Skipping.".format(ctrl))
            continue

        parent_node = ctrl_parent[0]

        # Create the isolating node
        driven_node = cmds.group(em=True, name=driven_name)
        cmds.parent(driven_node, parent_node)
        
        # Match driven node's position to control so the control doesn't move when reparented
        cmds.matchTransform(driven_node, ctrl, pos=True, rot=False, scl=False)
            
        # Create inverse matrix setup to cancel out the parent's rotation
        parent_dcmp = cmds.createNode('decomposeMatrix', name=name + '_ParentInv_Decomp')
        cmds.connectAttr('{}.worldInverseMatrix[0]'.format(parent_node), '{}.imat'.format(parent_dcmp))
        
        # Connect inverse rotation to driven node
        cmds.connectAttr('{}.outputRotate'.format(parent_dcmp), '{}.rotate'.format(driven_node))
        
        # --- PRESERVE CONSTRAINTS ---
        # Before moving and rotating ctrl, record any constraints it drives
        constraints = list(set(cmds.listConnections(ctrl, source=False, destination=True, type='constraint') or []))
        cns_data = []
        for cns in constraints:
            cns_type = cmds.nodeType(cns)
            driven_objs = list(set(cmds.listConnections(cns, source=False, destination=True, type='transform') or []))
            for obj in driven_objs:
                if obj == ctrl: continue
                # To be absolutely sure ctrl is a target, we just assume it is if it's connected
                cns_data.append((cns, cns_type, obj))
                
        # Temporarily create locators to hold the constraints
        temp_locs = []
        for cns, cns_type, obj in cns_data:
            # Create a locator at the exact same position as obj
            loc = cmds.spaceLocator(name=obj + "_temp_cns_loc")[0]
            cmds.matchTransform(loc, obj)
            temp_locs.append(loc)
            
            # Add loc to the constraint and remove ctrl
            try:
                if cns_type == 'parentConstraint':
                    cmds.parentConstraint(loc, obj, mo=True)
                    cmds.parentConstraint(ctrl, obj, rm=True)
                elif cns_type == 'scaleConstraint':
                    cmds.scaleConstraint(loc, obj, mo=True)
                    cmds.scaleConstraint(ctrl, obj, rm=True)
                elif cns_type == 'pointConstraint':
                    cmds.pointConstraint(loc, obj, mo=True)
                    cmds.pointConstraint(ctrl, obj, rm=True)
                elif cns_type == 'orientConstraint':
                    cmds.orientConstraint(loc, obj, mo=True)
                    cmds.orientConstraint(ctrl, obj, rm=True)
            except Exception as e:
                cmds.warning("Could not preserve {} on {}: {}".format(cns_type, obj, e))

        # --- ROTATE CONTROL ---
        # Reparent control under driven node
        cmds.parent(ctrl, driven_node)

        # Zero out local rotation on the control to match the driven node (which is perfectly world aligned)
        for attr in ['rotateX', 'rotateY', 'rotateZ', 'jointOrientX', 'jointOrientY', 'jointOrientZ']:
            if cmds.attributeQuery(attr, node=ctrl, exists=True):
                # Ensure it's not locked before setting
                is_locked = cmds.getAttr('{}.{}'.format(ctrl, attr), lock=True)
                if is_locked:
                    cmds.setAttr('{}.{}'.format(ctrl, attr), lock=False)
                
                try:
                    cmds.setAttr('{}.{}'.format(ctrl, attr), 0)
                except Exception as e:
                    print("Could not set {}.{}: {}".format(ctrl, attr, e))

                if is_locked:
                    cmds.setAttr('{}.{}'.format(ctrl, attr), lock=True)

        # --- RESTORE CONSTRAINTS ---
        # Now that ctrl is rotated, add it back with mo=True to calculate the new offset
        for (cns, cns_type, obj), loc in zip(cns_data, temp_locs):
            try:
                if cns_type == 'parentConstraint':
                    cmds.parentConstraint(ctrl, obj, mo=True)
                    cmds.parentConstraint(loc, obj, rm=True)
                elif cns_type == 'scaleConstraint':
                    cmds.scaleConstraint(ctrl, obj, mo=True)
                    cmds.scaleConstraint(loc, obj, rm=True)
                elif cns_type == 'pointConstraint':
                    cmds.pointConstraint(ctrl, obj, mo=True)
                    cmds.pointConstraint(loc, obj, rm=True)
                elif cns_type == 'orientConstraint':
                    cmds.orientConstraint(ctrl, obj, mo=True)
                    cmds.orientConstraint(loc, obj, rm=True)
            except Exception as e:
                cmds.warning("Could not restore {} on {}: {}".format(cns_type, obj, e))
            
            # Clean up the temporary locator
            cmds.delete(loc)
                        
    print('Build WorldOrient on controls successful')
