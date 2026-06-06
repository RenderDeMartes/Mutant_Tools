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

def create_hide_block(name='Hide'):
    PATH = os.path.dirname(__file__)
    MODULE_FILE = os.path.join(PATH, '10_Hide.json')
    if not os.path.exists(MODULE_FILE):
        cmds.warning('10_Hide.json not found.')
        return ''
        
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

def build_hide_block():
    nc, curve_data, setup = mt.import_configs()
    block = cmds.ls(sl=True)
    if not block:
        cmds.warning("Please select the Hide block to build.")
        return
        
    config = cmds.listConnections(block)[1]
    block = block[0]
    
    nodes_string = cmds.getAttr('{}.SetNodeList'.format(config), asString=True)

    if not nodes_string:
        cmds.warning("No nodes defined in SetNodeList.")
        return

    nodes = [n.strip() for n in nodes_string.split(',') if n.strip()]
    
    for node in nodes:
        if not cmds.objExists(node):
            cmds.warning("Node {} does not exist. Skipping.".format(node))
            continue
            
        try:
            cmds.setAttr('{}.visibility'.format(node), 0)
        except Exception as e:
            cmds.warning("Could not hide node {}: {}".format(node, str(e)))
                        
    print('Build Hide on nodes successful')
