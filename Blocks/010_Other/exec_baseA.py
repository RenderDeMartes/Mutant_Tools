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

#---------------------------------------------

def create_BaseA(name = 'BaseA'):

    # Read name conventions as nc[''] and setup as setup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-2]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)
    MODULE_FILE = os.path.join(os.path.dirname(__file__), '001_BaseA.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()

    name = mt.ask_name(text = name)
    if cmds.objExists('{}{}'.format(name, nc['module'])):
        cmds.warning('Name already exists.')
        return None

    # only one base at a time sorry
    if cmds.objExists('{}{}'.format(name, nc['module'])):
        cmds.warning('Build already have a base, we can only have 1 base at a time')
        return ''

    base = mt.create_block(name = name, icon = 'BaseA',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    base = base[1]
    base = base[0]

    print('BaseA Block added Successfully')


#-------------------------

def build_baseA_block():

    nc, curve_data, setup = mt.import_configs()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]    
    
    base = mt.build_baseA(size = cmds.getAttr('{}.CtrlScale'.format(config)), name = cmds.getAttr('{}.Name'.format(config)))
    print (base)
    mt.assign_color(input = base[0], color = cmds.getAttr('{}.CtrlColor'.format(config), asString = True))
    mt.assign_color(input = base[1], color = cmds.getAttr('{}.CtrlColor'.format(config), asString = True))
    mt.assign_color(input = base[2], color = cmds.getAttr('{}.CtrlColor'.format(config), asString = True))

    if cmds.objExists('geo'):
        cmds.connectAttr('{}.GeoVis'.format(base[0]), 'geo.v')

    print('BaseA Created Successfully')