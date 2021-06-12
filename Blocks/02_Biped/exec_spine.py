from maya import cmds
import json
import imp
import os

import Mutant_Tools
import Mutant_Tools.Utils
from Mutant_Tools.Utils import main_mutant
imp.reload(Mutant_Tools.Utils.main_mutant)

mt = main_mutant.Mutant()

#---------------------------------------------

TAB_FOLDER = '02_Biped'
PYBLOCK_NAME = 'exec_spine'

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

MODULE_FILE = (os.path.dirname(__file__) +'/01_Spine.json')
with open(MODULE_FILE) as module_file:
	module = json.load(module_file)

#---------------------------------------------

def create_spine_block(name = 'Spine'):

    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name = name, icon = 'Spine',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]
    
    cmds.select(cl=True)
    spineBase_guide = mt.create_joint_guide(name = name + '_Base')
    cmds.parent(spineBase_guide, block)
    spineInv_guide = mt.create_joint_guide(name = name + '_Inv')
    cmds.move(0,-1,0)
    spineBelly_guide = mt.create_joint_guide(name = name + '_Belly')
    cmds.move(0,2,0)
    spineChest_guide = mt.create_joint_guide(name = name + '_Chest')
    cmds.move(0,4,0)
    spineEnd_guide = mt.create_joint_guide(name = name + '_End')
    cmds.move(0,6,0)

    cmds.parent(spineBelly_guide,spineBase_guide)
    cmds.parent(spineChest_guide,spineBelly_guide)
    cmds.parent(spineEnd_guide,spineChest_guide)
    cmds.parent(spineInv_guide,spineBase_guide)


    #mt.orient_joint(input = spineBase_guide)
    #cmds.setAttr("{}.jointOrientX".format(spineInv_guide), 0)
    #cmds.setAttr("{}.jointOrientY".format(spineInv_guide), 0)
    #cmds.setAttr("{}.jointOrientZ".format(spineInv_guide), 0)

    print('{} Created Successfully'.format(name))

#create_spine_block()

#-------------------------

def build_spine_block():

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guide = cmds.listRelatives(block, c=True)[0]

    #groups for later cleaning
    clean_rig_grp = ''
    clean_ctrl_grp = ''
    
    #cmds.getAttr('{}.AttrName'.format(config))
    #cmds.getAttr('{}.AttrName'.format(config), asString = True)

    #orient the joints
    mt.orient_joint(input = guide)
    new_guide = mt.duplicate_and_remove_guides(guide)
    print (new_guide)
    to_build = [new_guide]

    #use this locator in case parent is set to new locator
    if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
        block_parent = cmds.spaceLocator( n = '{}'.format(str(block).replace(nc['module'],'_Parent' + nc['locator'])))
    else:
        block_parent = cmds.getAttr('{}.SetParent'.format(config))

    #build
    


    #clean a bit
    clean_rig_grp = cmds.group(em=True, n = '{}{}'.format(block.replace(nc['module'],'_Rig'), nc['group']))


    print ('Build {} Success'.format(block))



#build_spine_block()
