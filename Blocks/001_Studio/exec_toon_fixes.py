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
PYBLOCK_NAME = 'exec_toon_fixes'

#---------------------------------------------

def create_toon_fixes_block(name='Toon_Fixes'):

    #---------------------------------------------------
    #---------------------------------------------------
    #---------------------------------------------------


    # Read name conventions as nc[''] and setup as seup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-2]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '03_Toon_Fixes.json')
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

    block = mt.create_block(name = name, icon = 'letter-b',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]
      
    #cmds.getAttr('{}.AttrName'.format(config)) #get attrs from config
    #cmds.getAttr('{}.AttrName'.format(config), asString = True) #for enums
    #joint_one = mt.create_joint_guide(name = name) #guide base with shapes

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_toon_fixes_block()

#-------------------------

def build_toon_fixes_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    name = block.replace(nc['module'],'')

    # if cmds.objExists('Light_Loc_Grp'):
    #     cmds.delete('Light_Loc_Grp')
    #
    # light_grp = cmds.group(em=True, n='Light_Loc_Grp')
    # if cmds.objExists('geo'):
    #     cmds.parent(light_grp, 'geo')
    #     cmds.setAttr('{}.v'.format(light_grp), 0)
    #
    # # # Add Light Locators
    # if not cmds.objExists('Mover_Light_Loc'):
    #     mover_loc = cmds.spaceLocator(n='Mover_Light_Loc')[0]
    #     cmds.setAttr('{}.v'.format(mover_loc), 0)
    #     cmds.parentConstraint('Mover_Gimbal_Ctrl', mover_loc, mo=False)
    #     cmds.scaleConstraint('Mover_Gimbal_Ctrl', mover_loc, mo=False)
    #     cmds.parent(mover_loc, light_grp)
    # if not cmds.objExists('World_Light_Loc'):
    #     world_loc = cmds.spaceLocator(n='World_Light_Loc')[0]
    #     cmds.setAttr('{}.v'.format(world_loc), 0)
    #     cmds.parentConstraint('Global_Ctrl', world_loc, mo=False)
    #     cmds.scaleConstraint('Global_Ctrl', world_loc, mo=False)
    #     cmds.parent(world_loc, light_grp)
    # if not cmds.objExists('COG_Light_Loc'):
    #     cog_loc = cmds.spaceLocator(n='COG_Light_Loc')[0]
    #     cmds.setAttr('{}.v'.format(cog_loc), 0)
    #     cmds.parentConstraint('COG_Gimbal_Ctrl', cog_loc, mo=False)
    #     cmds.scaleConstraint('COG_Gimbal_Ctrl', cog_loc, mo=False)
    #     cmds.parent(cog_loc, light_grp)
    # try:
    #     from rigSystem.assetTemplates import get_hierarchy, get_one_sid
    #     locators = ['Mover_Light_Loc', 'World_Light_Loc', 'COG_Light_Loc']
    #     rid = get_hierarchy(get_one_sid())
    #     rid.sid.tag_node().set_tag('rendergeo', locators)
    # except:
    #     pass


    #remove chest ctrl
    if cmds.objExists('Spine_Chest_FK_CtrlShape'):
        cmds.setAttr('Spine_Chest_FK_CtrlShape.v', 0)

#build_toon_fixes_block()
