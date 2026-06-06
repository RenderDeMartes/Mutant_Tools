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

def create_vis_attrs_block(name='VisAttrs'):
    PATH = os.path.dirname(__file__)
    MODULE_FILE = os.path.join(PATH, '14_VisAttrs.json')
    if not os.path.exists(MODULE_FILE):
        cmds.warning('14_VisAttrs.json not found.')
        return ''
        
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()

    name = mt.ask_name(text=module['Name'])
    if not name:
        return
    if cmds.objExists('{}{}'.format(name, nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(
        name=name,
        icon=module['Icon'].replace('.png',''),
        attrs=module['attrs'],
        build_command=module['build_command'],
        import_command=module['import']
    )
    
    print('{} Created successfully'.format(name))

def build_vis_attrs_block():
    nc, curve_data, setup = mt.import_configs()
    block = cmds.ls(sl=True)
    if not block:
        cmds.warning("Please select the VisAttrs block to build.")
        return
        
    conns = cmds.listConnections(block, type='network') or []
    if not conns:
        conns = cmds.listConnections(block) or []
        if len(conns) < 2:
            cmds.warning("Could not find configuration network node for VisAttrs block {}.".format(block))
            return
        config = conns[1]
    else:
        config = conns[0]
        
    block = block[0]
    
    target_ctrl = cmds.getAttr('{}.SetTargetCtrl'.format(config), asString=True)
    vis_attrs_string = cmds.getAttr('{}.VisAttrsList'.format(config), asString=True)
    
    default_on = True
    if cmds.attributeQuery('DefaultOn', n=config, exists=True):
        default_on = cmds.getAttr('{}.DefaultOn'.format(config))

    if not target_ctrl:
        cmds.warning("No Target Control specified in SetTargetCtrl.")
        return
        
    if not cmds.objExists(target_ctrl):
        cmds.warning("Target Control '{}' does not exist in the scene. Skipping build.".format(target_ctrl))
        return

    if not vis_attrs_string:
        cmds.warning("No visibility attributes defined in VisAttrsList.")
        return

    # Parse mapping lines
    # Format: AttrName = Node1, Node2, ...
    lines = []
    for part in vis_attrs_string.replace('\r\n', '\n').split('\n'):
        for subpart in part.split(';'):
            if subpart.strip():
                lines.append(subpart.strip())

    success_count = 0
    for line in lines:
        if '=' not in line:
            cmds.warning("Invalid format (missing '='): {}".format(line))
            continue
            
        attr_part, nodes_part = line.split('=', 1)
        attr_name = attr_part.strip()
        
        # Format attribute name to be safe
        safe_attr_name = "".join([c if c.isalnum() or c == '_' else '_' for c in attr_name])
        if safe_attr_name != attr_name:
            cmds.warning("Attribute name '{}' had invalid characters. Renaming to '{}'.".format(attr_name, safe_attr_name))
            attr_name = safe_attr_name
            
        if not attr_name:
            cmds.warning("Empty attribute name in line: {}".format(line))
            continue
            
        nodes = [n.strip() for n in nodes_part.split(',') if n.strip()]
        if not nodes:
            cmds.warning("No nodes specified for attribute '{}'.".format(attr_name))
            continue

        # Add the attribute if it does not exist
        if not cmds.attributeQuery(attr_name, node=target_ctrl, exists=True):
            mt.new_enum(input=target_ctrl, name=attr_name, enums='Off:On', default=1 if default_on else 0)

        # Connect target attribute to the nodes' visibility
        for node in nodes:
            if not cmds.objExists(node):
                cmds.warning("Node '{}' does not exist. Skipping visibility connection.".format(node))
                continue
                
            vis_attr = '{}.visibility'.format(node)
            try:
                if cmds.isFreeToChangeState(vis_attr, checkLockAndConnections=True):
                    cmds.connectAttr('{}.{}'.format(target_ctrl, attr_name), vis_attr, f=True)
                    print("Connected {}.{} -> {}".format(target_ctrl, attr_name, vis_attr))
                else:
                    if cmds.getAttr(vis_attr, lock=True):
                        cmds.setAttr(vis_attr, lock=False)
                        cmds.connectAttr('{}.{}'.format(target_ctrl, attr_name), vis_attr, f=True)
                        print("Unlocked and connected {}.{} -> {}".format(target_ctrl, attr_name, vis_attr))
                    else:
                        cmds.warning("Could not connect to locked or connected visibility of '{}'.".format(node))
            except Exception as e:
                cmds.warning("Error connecting {}.{} to {}: {}".format(target_ctrl, attr_name, vis_attr, str(e)))
                
        success_count += 1
        
    print('Build VisAttrs on {} successfully completed ({} attributes created/connected)'.format(block, success_count))
