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
    name = mt.ask_name(text = name)
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    NAME_block = mt.create_block(name = name, icon = 'ICON_NAME',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    NAME_config = NAME_block[1]
    NAME_block = NAME_block[0]

    print('Base Created Successfully'),

#create_NAME_block()

#-------------------------

def build_NAME_block():

    block = cmds.ls(sl=True)
    config = ''

    print ('Hi :), this is working')



#build_NAME_block()
