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
PYBLOCK_NAME = 'exec_human_fixes'

#---------------------------------------------

def create_human_fixes_block(name='Human_Fixes'):

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

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '02_Human_Fixes.json')
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

    block = mt.create_block(name = name, icon = 'letter-a',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]
      
    #cmds.getAttr('{}.AttrName'.format(config)) #get attrs from config
    #cmds.getAttr('{}.AttrName'.format(config), asString = True) #for enums
    #joint_one = mt.create_joint_guide(name = name) #guide base with shapes

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_human_fixes_block()

#-------------------------

def build_human_fixes_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    name = block.replace(nc['module'],'')


    #cmds.getAttr('{}.AttrName'.format(config))
    #cmds.getAttr('{}.AttrName'.format(config), asString = True)


    #Spine
    if cmds.objExists('Spine_Root_Parent_Loc_aimConstraint1') and cmds.objExists('Spine_Bottom_Ik_Ctrl') and cmds.objExists('Spine_Root_Parent_Loc'):
            cmds.delete('Spine_Root_Parent_Loc_aimConstraint1')
            cmds.orientConstraint('Spine_Bottom_Ik_Ctrl', 'Spine_Root_Parent_Loc', mo=True)


    #Spine values
    values = [0, 0, 0.2, 0, 0]
    attrs = ['_EndSquash','_ChestSquash','_BellySquash','_BaseSquash','_RootSquash']
    if cmds.objExists('Spine_Attrs_Loc'):
        for attr, value in zip(attrs, values):
            if cmds.attributeQuery(attr, n='Spine_Attrs_Loc', exists=True):
                cmds.setAttr('Spine_Attrs_Loc.{}'.format(attr), value)
        if cmds.attributeQuery('MidTwist', n='Spine_Attrs_Loc', exists=True):
            cmds.setAttr("Spine_Root_IK_Ctrl|Spine_Attrs_Loc.MidTwist", 1)


    #Scale Head
    if cmds.objExists('L_Eyes_Jnt_scaleConstraint1') and cmds.objExists('L_Eyes_Jnt') and cmds.objExists('Head_Jnt'):
            cmds.delete('L_Eyes_Jnt_scaleConstraint1')
            cmds.scaleConstraint('Head_Jnt', 'L_Eyes_Jnt', mo=True)
            cmds.delete("R_Eyes_Jnt_scaleConstraint1")
            cmds.scaleConstraint("Head_Jnt", "R_Eyes_Jnt", mo=True)
    if cmds.objExists('Head_Ctrl') and cmds.objExists('Head_Jnt_Eyes_Switches_Loc'):
        cmds.scaleConstraint("Head_Ctrl", "Head_Jnt_Eyes_Switches_Loc", mo=True)



#build_human_fixes_block()
