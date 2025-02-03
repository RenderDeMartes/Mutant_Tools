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

from Mutant_Tools.Utils.Correctives import PushCorrectives
reload(PushCorrectives)

#---------------------------------------------

TAB_FOLDER = '007_Games'
PYBLOCK_NAME = 'exec_pushcorrectives'

#---------------------------------------------

def create_pushcorrectives_block(name = 'PushCorrectives'):
    """
    Create a push correctives block with the specified name.

    Args:
        name (str): The base name for the push correctives block.

    Returns:
        str: The name of the created push correctives block.

    Raises:
        RuntimeError: If the specified name or direction already exists.

    Example:
        >>> create_pushcorrectives_block(name='MyPushCorrectivesBlock')
        'MyPushCorrectivesBlock'
    """
    # Read name conventions as nc[''] and setup as seup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-2]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '01_PushCorrectives.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()

    #---------------------------------------------------
    #---------------------------------------------------
    #---------------------------------------------------

    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    #name checks and block creation
    axis_names = mt.ask_name(text = module['attrs']['Direction_string'])
    if cmds.objExists('{}{}'.format(axis_names,nc['module'])):
        cmds.warning('Directions already defined.')
        return ''

    block = mt.create_block(name = name, icon = 'PushCorrectives',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = cmds.listConnections(block)[1]
    #cmds.getAttr('{}.AttrName'.format(config)) #get attrs from config
    #cmds.getAttr('{}.AttrName'.format(config), asString = True) #for enums
    #joint_one = mt.create_joint_guide(name = name) #guide base with shapes

    #for processing sides
    #direction = cmds.getAttr('{}.SetDirection'.format(config), asString=True)
    direction = axis_names.replace(" ", "")
    cmds.setAttr('{}.Direction'.format(config), direction, type="string")
    direction_list = direction.split(',')

    for direction in direction_list:
        PushSystemObject = PushCorrectives.PushSystem()
        #PushSystemObject.create_push_joints(sources=cmds.ls(sl=True))
        print("Directions received"+direction)
        a_joint = PushSystemObject.create_push_joints(section=name, side=[direction])
        cmds.parent(a_joint, block)
    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_pushcorrectives_block()

#-------------------------

def build_pushcorrectives_block():
    """
    Build the push correctives block based on the selected block.

    Raises:
        RuntimeError: If the block does not have a valid configuration.

    Example:
        >>> build_pushcorrectives_block()
        Build PushCorrectivesBlock Success
    """
    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guide = cmds.listRelatives(block, c=True)
    print(guide)
    name = block.replace(nc['module'],'')

    #for processing sides
    direction = cmds.getAttr('{}.Direction'.format(config), asString=True)
    direction = direction.replace(" ", "")
    direction_list = direction.split(',')

    source = cmds.getAttr('{}.SetParent'.format(config), asString=True)

    chains_list = cmds.listRelatives(block, children=True)

    for guide_chain in guide:
        mt.duplicate_and_remove_guides(guide_chain)

    limb_push_systems = []
    for direction in direction_list: 
        PushSystemObject = PushCorrectives.PushSystem()
        PushSystemObject.identify_push_joints(section=name, source=source, side=[direction])
        limb_push_systems.append(PushSystemObject)

    for limb_push_system in limb_push_systems:
        limb_push_system.create_push_system()

    print ('Build {} Success'.format(block))

#build_pushcorrectives_block()
