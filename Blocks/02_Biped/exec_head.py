from maya import cmds
from maya import OpenMaya

import json
import imp
import os

import Mosaic_Tools
import Mosaic_Tools.Utils
from Mosaic_Tools.Utils import main_mosaic
imp.reload(Mosaic_Tools.Utils.main_mosaic)

mt = main_mosaic.Mosaic()

#---------------------------------------------

TAB_FOLDER = '02_Biped'
PYBLOCK_NAME = 'exec_head'

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

MODULE_FILE = (os.path.dirname(__file__) +'/05_Head.json')
with open(MODULE_FILE) as module_file:
	module = json.load(module_file)

#---------------------------------------------

def create_head_block(name = 'Head'):

    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''
    names = name.split('_')
    neck_name = names[0]
    head_name = names[1]

    block = mt.create_block(name = name, icon = 'HeadNeck',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]
      
    cmds.select(cl=True)
    neck_guide = mt.create_joint_guide(name = neck_name)
    cmds.move(0,0,0)
    head_guide = mt.create_joint_guide(name = head_name)
    cmds.move(0,5,1.5)
    head_guideEnd = mt.create_joint_guide(name = head_name + 'End')
    cmds.move(0,8.5,1.5)

    cmds.parent(head_guideEnd, head_guide)
    cmds.parent(head_guide, neck_guide)
    cmds.parent(neck_guide, block)
    cmds.select(block)

    mt.orient_joint(input = neck_guide)
    cmds.setAttr("{}.jointOrientX".format(head_guideEnd), 0)
    cmds.setAttr("{}.jointOrientY".format(head_guideEnd), 0)
    cmds.setAttr("{}.jointOrientZ".format(head_guideEnd), 0)

    print('{} Created Successfully'.format(name))

#create_head_block()

#-------------------------

def build_head_block():

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
    new_guide = mt.duplciate_and_remove_guides(guide)

    #use this locator in case parent is set to new locator
    if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
        block_parent = cmds.spaceLocator( n = '{}'.format(str(block).replace(nc['module'],'_Parent' + nc['locator'])))
    else:
        block_parent = cmds.getAttr('{}.SetParent'.format(config))

    #config--------------------------

    ribbon_amount = cmds.getAttr('{}.SecundaryRibbon'.format(config))
    ctrl_type = cmds.getAttr('{}.HeadCtrlType'.format(config), asString = True)
    ctrl_size = cmds.getAttr('{}.CtrlSize'.format(config))
    ctrl_color = cmds.getAttr('{}.CtrlColor'.format(config))

    neck_joint = new_guide
    head_joint = cmds.listRelatives(new_guide, c=True)[0]

    #Build--------------------------

    ribbon = mt.basic_ribbon_between(neck_joint, head_joint, ribbon_amount , str(neck_joint).replace(nc['joint'], ''))
    
    #mid joint
    mid_neck_joint = mt.joints_middle_no_chain( start = neck_joint, end=head_joint, axis = setup['twist_axis'], amount =6, name = 'Mid')
    cmds.delete(cmds.parentConstraint(neck_joint, head_joint, mid_neck_joint, mo=False))
    
     #create controllers



    print ('Build {} Success'.format(block))



#build_head_block()
