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
PYBLOCK_NAME = 'exec_setter'

#---------------------------------------------

def create_setter_block(name = 'Setter'):

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

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '008_Setter.json')
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

    block = mt.create_block(name = name, icon = 'Pose',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]
      
    #cmds.getAttr('{}.AttrName'.format(config)) #get attrs from config
    #cmds.getAttr('{}.AttrName'.format(config), asString = True) #for enums
    #joint_one = mt.create_joint_guide(name = name) #guide base with shapes

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_setter_block()

#-------------------------

def build_setter_block():

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]

    for num in range(8):
        values = cmds.getAttr('{}.Pose{}'.format(config, num))
        if not values:
            continue
        values=values.replace(' ', '').split(',')
        print(values)
        node = values[0]
        pose =  {'translateX' : values[1],
                'translateY' : values[2],
                'translateZ' : values[3],
                'rotateX' : values[4],
                'rotateY' : values[5],
                'rotateZ' : values[6],
                'scaleX' : values[7],
                'scaleY' : values[8],
                'scaleZ' : values[9]
                }

        for attr in pose:
            try:
                print('{}.{}'.format(node, attr), float(pose[attr]))
                cmds.setAttr('{}.{}'.format(node, attr), float(pose[attr]))
            except Exception as e:
                print(e)








    print ('Build {} Success'.format(block))



#build_setter_block()
