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

TAB_FOLDER = '010_Other'
PYBLOCK_NAME = 'exec_changecolors'

#---------------------------------------------

def create_change_colors_block(name = 'ChangeColors'):

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

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '010_Change_Colors.json')
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

    block = mt.create_block(name = name, icon = 'ChangeColors',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]
      
    #cmds.getAttr('{}.AttrName'.format(config)) #get attrs from config
    #cmds.getAttr('{}.AttrName'.format(config), asString = True) #for enums
    #joint_one = mt.create_joint_guide(name = name) #guide base with shapes

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_changecolors_block()

#-------------------------

def build_change_colors_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    name = block.replace(nc['module'],'')

    colors_a = cmds.getAttr('{}.ChangeColors1'.format(config), asString = True)
    colors_b = cmds.getAttr('{}.ChangeColors2'.format(config), asString = True)
    colors_c = cmds.getAttr('{}.ChangeColors3'.format(config), asString = True)
    colors_d = cmds.getAttr('{}.ChangeColors4'.format(config), asString = True)
    colors_e = cmds.getAttr('{}.ChangeColors5'.format(config), asString = True)
    colors_f = cmds.getAttr('{}.ChangeColors6'.format(config), asString = True)
    colors_g = cmds.getAttr('{}.ChangeColors7'.format(config), asString = True)
    colors_h = cmds.getAttr('{}.ChangeColors8'.format(config), asString = True)
    colors_i = cmds.getAttr('{}.ChangeColors9'.format(config), asString = True)

    colors_attrs = [colors_a, colors_b, colors_c, colors_d, colors_e, colors_f, colors_g, colors_h, colors_i]

    for color in colors_attrs:
        if not color:
            continue
        print(color)
        color_split = color.split(':')
        print(color_split)
        ctrl = color_split[0]
        color = color_split[1]

        mt.assign_color(input=ctrl,color=color)


    print ('Build {} Success'.format(block))

#build_changecolors_block()
