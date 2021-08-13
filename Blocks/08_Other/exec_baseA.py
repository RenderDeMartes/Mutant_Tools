from maya import cmds
import json
import os

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
import imp
imp.reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()

#---------------------------------------------

#Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = PATH.replace('/Blocks//08_Other', '//Config') #change this path depending of the folder

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

MODULE_FILE = (os.path.dirname(__file__) +'/01_BaseA.json')
with open(MODULE_FILE) as module_file:
	module = json.load(module_file)

#---------------------------------------------

def create_BaseA(name = 'BaseA'):

    name = mt.ask_name(text = name)
    if cmds.objExists('{}{}'.format(name, nc['module'])):
        cmds.warning('Name already exists.')
        return None

    # only one base at a time sorry
    if cmds.objExists('{}{}'.format(name, nc['module'])):
        cmds.warning('Build already have a base, we can only have 1 base at a time')
        return ''

    base = mt.create_block(name = name, icon = 'BaseA',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    base = base[1]
    base = base[0]

    print('BaseA Block added Successfully')


#-------------------------

def build_baseA_block():

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]    
    
    base = mt.build_baseA(size = cmds.getAttr('{}.CtrlScale'.format(config)), name = cmds.getAttr('{}.Name'.format(config)))
    print (base)
    mt.assign_color(input = base[0], color = cmds.getAttr('{}.CtrlColor'.format(config), asString = True))
    mt.assign_color(input = base[1], color = cmds.getAttr('{}.CtrlColor'.format(config), asString = True))
    mt.assign_color(input = base[2], color = cmds.getAttr('{}.CtrlColor'.format(config), asString = True))


    print('BaseA Created Successfully')