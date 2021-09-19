from maya import cmds
import json
import imp
import os

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
imp.reload(Mutant_Tools.Utils.Rigging.main_mutant)
mt = main_mutant.Mutant()

from Mutant_Tools.Utils.IO import CtrlUtils
imp.reload(Mutant_Tools.Utils.IO.CtrlUtils)
ctrls = CtrlUtils.Ctrls()
#---------------------------------------------

TAB_FOLDER = '08_Data'
PYBLOCK_NAME = 'exec_load_ctrls'

#Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = PATH.replace('/Blocks//{}'.format(TAB_FOLDER), '//Config') #change this path depending of the folder

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

MODULE_FILE = (os.path.dirname(__file__) +'/02_Load_Ctrls.json')
with open(MODULE_FILE) as module_file:
	module = json.load(module_file)

#---------------------------------------------

def create_load_ctrls_block(name = 'Load_Ctrls'):

    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name = name, icon = 'Controller',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_load_ctrls_block()

#-------------------------

def build_load_ctrls_block():

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    file = cmds.getAttr('{}.File'.format(config), asString = True)
    if not file:
        return False

    ctrls.load_all(path = file)

    print('Getting ctrls data from: ', file)


    print ('Build {} Success'.format(block))


#build_load_ctrls_block()
