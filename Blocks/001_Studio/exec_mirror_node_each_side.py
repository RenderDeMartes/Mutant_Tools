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
PYBLOCK_NAME = 'exec_mirror_node_each_side'

#---------------------------------------------

def create_mirror_node_each_side_block(name='MirrorNodeEachSide'):

    # Read name conventions as nc[''] and setup as setup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-2]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '09_MirrorNodeEachSide.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()

    #name checks and block creation
    name = 'MirrorNodeEachSide'
    if cmds.objExists('{}{}'.format(name, nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name=name, icon='Mirror', attrs=module['attrs'],
                            build_command=module['build_command'],
                            import_command=module['import'])
    config = block[1]
    block = block[0]

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_mirror_node_each_side_block()

#-------------------------

def build_mirror_node_each_side_block():
    """
    Sets a Maya optionVar flag so that all subsequent mirrored blocks
    will create a Mirror_Grp on BOTH sides (the unmirrored side gets
    identity/zeroed-out transforms for hierarchy consistency).
    """
    cmds.optionVar(iv=("mutant_ensure_mirror", 1))
    print('Mirror Node Each Side: Flag enabled. All mirrored blocks after this will include Mirror_Grp on both sides.')


#build_mirror_node_each_side_block()
