from maya import cmds
import json
import imp
import os

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
imp.reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()

#---------------------------------------------

TAB_FOLDER = '09_Other'
PYBLOCK_NAME = 'exec_bs_bind'

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

MODULE_FILE = (os.path.dirname(__file__) +'/06_BS_Bind.json')
with open(MODULE_FILE) as module_file:
	module = json.load(module_file)

#---------------------------------------------

def create_bs_bind_block(name = 'BS_Bind'):

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

#create_bs_bind_block()

#-------------------------

def build_bs_bind_block():

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]

    #cmds.getAttr('{}.AttrName'.format(config))
    geo_grp = cmds.getAttr('{}.SetGeoGrp'.format(config), asString = True)

    if not cmds.objExists(geo_grp):
        cmds.warning('there is no group called {}'.format(geo_grp))
        return False

    new_geo = mt.duplicate_change_names(input = geo_grp, hi = True, search=nc['geo'], replace =nc['bind_geo'])[0]
    cmds.parent(new_geo, 'Bind_Geo_Grp')

    cmds.select(new_geo, geo_grp)
    bs=cmds.blendShape(n='BS_{}_Render'.format(new_geo), w=[(0, 1)])


    print ('Build {} Success'.format(block))



#build_bs_bind_block()
