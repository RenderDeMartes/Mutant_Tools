from __future__ import absolute_import
from maya import cmds, mel
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

TAB_FOLDER = '008_Props'
PYBLOCK_NAME = 'exec_blendshape'

#---------------------------------------------

def create_blendshape_block(name = 'BlendShape'):

    # Read name conventions as nc[''] and setup as seup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-2]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '04_Blendshape.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()
    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name = name, icon = 'Blendshape',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]
      
    #cmds.getAttr('{}.AttrName'.format(config)) #get attrs from config
    #cmds.getAttr('{}.AttrName'.format(config), asString = True) #for enums
    #joint_one = mt.create_joint_guide(name = name) #guide base with shapes

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_blendshape_block()

#-------------------------

def build_blendshape_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    name=block.replace(nc['module'],'')

    geo = cmds.getAttr('{}.SetGeo'.format(config))
    names = cmds.getAttr('{}.NewNames'.format(config)).replace(' ', '').split(',')

    local_geos = []
    for n in names:
        print(n)
        duplicated = cmds.duplicate(geo, name=n)[0]
        print(duplicated)
        local_geos.append(duplicated)

    cmds.select(local_geos, geo)
    if cmds.objExists(name+'_BSP'):
        cmds.delete(name+'_BSP')
    bs = mel.eval("blendShape -automatic -before;")[0]
    bs=cmds.rename(bs, name+'_BSP')
    print(bs)
    cmds.delete(local_geos)

    print ('Build {} Success'.format(block))



#build_blendshape_block()
