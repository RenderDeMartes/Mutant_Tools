from maya import cmds
import json
import imp
import os

import Mosaic_Tools
import Mosaic_Tools.Utils
from Mosaic_Tools.Utils import main_mosaic
imp.reload(Mosaic_Tools.Utils.main_mosaic)

mt = main_mosaic.Mosaic()

#---------------------------------------------

TAB_FOLDER = 'TAB'
PYBLOCK_NAME = 'exec_NAME'

#Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = PATH.replace('\Blocks//{}'.format(TAB_FOLDER), '//Config') #change this path depending of the folder

JSON_FILE = (PATH + '/name_conventions.json')
with open(JSON_FILE) as json_file:
	nc = json.load(json_file)
#Read curve shapes info
CURVE_FILE = (PATH + '/curves.json')
with open(CURVE_FILE) as curve_file:
	curve_data = json.load(curve_file)
#setup File
SETUP_FILE = (PATH+'/rig_setup.json')
with open(SETUP_FILE) as setup_file:
	setup = json.load(setup_file)	

MODULE_FILE = (os.path.dirname(__file__) +'/num_name.json')
with open(MODULE_FILE) as module_file:
	module = json.load(module_file)

#---------------------------------------------

def create_NAME_block(name = 'NAME'):

    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name = name, icon = 'ICON_NAME',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]
      
    #cmds.getAttr('{}.AttrName'.format(config)) #get attrs from config
    #cmds.getAttr('{}.AttrName'.format(config), asString = True) #for enums
    #joint_one = mt.create_joint_guide(name = name) #guide base with shapes

    print('{} Created Successfully'.format(name))

#create_NAME_block()

#-------------------------

def build_NAME_block():

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guide = cmds.listRelatives(block, c=True)[0]

    #groups for later cleaning
    main_ctrl_group = []
    main_rig_group = []

    #cmds.getAttr('{}.AttrName'.format(config))
    #cmds.getAttr('{}.AttrName'.format(config), asString = True)

    #orient the joints
    mt.orient_joint(input = guide)
    new_guide = mt.duplciate_and_remove_guides(guide)
    print (new_guide)
    to_build = [new_guide]

    #use this locator in case parent is set to new locator
    if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
        block_parent = cmds.spaceLocator( n = '{}'.format(str(block).replace(nc['module'],nc['locator'])))
    else:
        block_parent = cmds.getAttr('{}.SetParent'.format(config))

    print ('Build {} Success'.format(block))



#build_NAME_block()
