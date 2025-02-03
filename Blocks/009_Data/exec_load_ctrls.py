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

from Mutant_Tools.Utils.IO import CtrlUtils
reload(Mutant_Tools.Utils.IO.CtrlUtils)
ctrls = CtrlUtils.Ctrls()
#---------------------------------------------

TAB_FOLDER = '009_Data'
PYBLOCK_NAME = 'exec_load_ctrls'

#Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-2]
FOLDER=''
for f in PATH_PARTS:
	FOLDER = os.path.join(FOLDER, f)

JSON_FILE = os.path.join(FOLDER, 'config', 'name_conventions.json')
with open(JSON_FILE) as json_file:
	nc = json.load(json_file)
#Read curve shapes info
CURVE_FILE = os.path.join(FOLDER, 'config', 'curves.json')
with open(CURVE_FILE) as curve_file:
	curve_data = json.load(curve_file)
#setup File
SETUP_FILE = os.path.join(FOLDER, 'config', 'rig_setup.json')
with open(SETUP_FILE) as setup_file:
	setup = json.load(setup_file)

MODULE_FILE = os.path.join(os.path.dirname(__file__),'02_Load_Ctrls.json')
with open(MODULE_FILE) as module_file:
	module = json.load(module_file)


#---------------------------------------------

def create_load_ctrls_block(name = 'Load_Ctrls'):

    nc, curve_data, setup = mt.import_configs()
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

    # Read name conventions as nc[''] and setup as seup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-2]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '02_Load_Ctrls.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    file = cmds.getAttr('{}.File'.format(config), asString = True)
    if not file:
        return False
    try:
        if file == 'AG':
            print('Loading From:', os.path.join(FOLDER,'Utils', 'IO', 'Ctrl_Data', 'AG.json'))
            ctrls.load_all(path = os.path.join(FOLDER,'Utils', 'IO', 'Ctrl_Data', 'AG.json'))
        elif file == 'SP':
            print('Loading From:', os.path.join(FOLDER,'Utils', 'IO', 'Ctrl_Data', 'SP.json'))
            ctrls.load_all(path = os.path.join(FOLDER,'Utils', 'IO', 'Ctrl_Data', 'SP.json'))
        elif file == 'Quad':
            print('Loading From:', os.path.join(FOLDER,'Utils', 'IO', 'Ctrl_Data', 'Quad.json'))
            ctrls.load_all(path = os.path.join(FOLDER,'Utils', 'IO', 'Ctrl_Data', 'Quad.json'))
        elif file == 'Simple':
            print('Loading From:', os.path.join(FOLDER,'Utils', 'IO', 'Ctrl_Data', 'Simple.json'))
            ctrls.load_all(path = os.path.join(FOLDER,'Utils', 'IO', 'Ctrl_Data', 'Simple.json'))
        else:
            print('Loading From:', file)
            ctrls.load_all(path = file)
    except:
        pass


    print ('Build {} Success'.format(block))


#build_load_ctrls_block()
