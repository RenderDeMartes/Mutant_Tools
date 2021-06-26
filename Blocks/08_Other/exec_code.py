from maya import cmds
from maya import mel
import json
import imp
import os

import Mutant_Tools
import Mutant_Tools.Utils
from Mutant_Tools.Utils import main_mutant
imp.reload(Mutant_Tools.Utils.main_mutant)

mt = main_mutant.Mutant()

#---------------------------------------------

TAB_FOLDER = '08_Other'
PYBLOCK_NAME = 'exec_code'

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

MODULE_FILE = (os.path.dirname(__file__) +'/04_Code.json')
with open(MODULE_FILE) as module_file:
	module = json.load(module_file)

#---------------------------------------------

def create_code_block(name = 'Code'):

    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name = name, icon = 'Code',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]

    loc = cmds.spaceLocator(n = name + nc['locator'])
    cmds.parent(loc,block)

    #cmds.getAttr('{}.AttrName'.format(config)) #get attrs from config
    #cmds.getAttr('{}.AttrName'.format(config), asString = True) #for enums
    #joint_one = mt.create_joint_guide(name = name) #guide base with shapes

    print('{} Created Successfully'.format(name))

#create_code_block()

#-------------------------

def build_code_block():

    #mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]

    #cmds.getAttr('{}.AttrName'.format(config))
    pl = cmds.getAttr('{}.Exec'.format(config), asString = True)
    code = cmds.getAttr('{}.Code'.format(config), asString = True)

    if pl != 'Python':
       mel.eval(code)
    else:
        exec(code)

    print ('Build {} Success'.format(block))



#build_code_block()
