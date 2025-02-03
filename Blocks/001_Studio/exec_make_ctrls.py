from __future__ import absolute_import
#

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
try:
    from rigSystem.assetTemplates import get_hierarchy, get_one_sid
except Exception as e:
    #cmds.warning('Error loading get_hierarchy, get_one_sid on exec_make_ctrls: {}'.format(e))
    ''

mt = main_mutant.Mutant()

#---------------------------------------------

TAB_FOLDER = '001_Studio'
PYBLOCK_NAME = 'exec_make_ctrls'

#---------------------------------------------

def create_make_ctrls_block(name = 'Make_Ctrls'):

    # Read name conventions as nc[''] and setup as seup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-2]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '01_Make_Ctrls.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()

    #name checks and block creation
    name = 'Tag_Ctrls'
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name = name, icon = 'Tag',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]
    
    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_make_ctrls_block(name = 'Tag_Ctrls')

#-------------------------

def build_make_ctrls_block():

    nc, curve_data, setup = mt.import_configs()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]

    rid = get_hierarchy(get_one_sid())
    rid.sid.tag_node().set_tag('animctrl', cmds.ls('*{}'.format(nc['ctrl'])))

    print('Block {} Success'.format(block))

#build_make_ctrls_block()
