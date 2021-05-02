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

TAB_FOLDER = '02_Biped'
PYBLOCK_NAME = 'exec_clavicle'

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

MODULE_FILE = (os.path.dirname(__file__) +'/03_Clavicle.json')
with open(MODULE_FILE) as module_file:
	module = json.load(module_file)

#---------------------------------------------

def create_clavicle_block(name = 'Clavicle'):

    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name =  name, icon = 'Clavicle',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]

    cmds.select(cl=True)
    clav_guide = mt.create_joint_guide(name = name)
    cmds.move(5,0,0)
    clav_guideEnd = mt.create_joint_guide(name = name + '_End')
    cmds.move(15,0,0)
    cmds.parent(clav_guideEnd, clav_guide)
    cmds.parent(clav_guide, block)
    cmds.select(block)

    mt.orient_joint(input = clav_guide)

    print('{} Created Successfully'.format(name))

#create_clavicle_block()

#-------------------------

def build_clavicle_block():

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guide = cmds.listRelatives(block, c=True)[0]

    #cmds.getAttr('{}.AttrName'.format(config))
    #cmds.getAttr('{}.AttrName'.format(config), asString = True)

    #orient the joints
    mt.orient_joint(input = guide)
    new_guide = mt.duplciate_and_remove_guides(guide)
    print (new_guide)
    to_build = [new_guide]


    #if mirror is set only to right we need to build on left for mirror behavior then putt it back to righ side
    if cmds.getAttr('{}.Mirror'.format(config), asString = True) == 'Right_Only':
        miror_grp = mt.mirror_group(new_guide, world = True)
        cmds.makeIdentity(miror_grp, a=True, t=True, r=True, s=True)
        cmds.parent(new_guide, w = True)
        cmds.delete(miror_grp)
        mt.orient_joint(input = new_guide)

    elif cmds.getAttr('{}.Mirror'.format(config), asString = True) == 'True':
        right_guide = mt.duplicate_change_names(input = new_guide, hi = True, search=nc['left'], replace =nc['right'])[0]
        to_build.append(right_guide)
        print (to_build)

    #build ------------------------------------------------------
    for side_guide in to_build:

        #use this locator in case parent is set to new locator
        if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
            block_parent = cmds.spaceLocator( n = '{}'.format(str(side_guide).replace(nc['joint'],'_Parent' + nc['locator'])))
        else:
            block_parent = cmds.getAttr('{}.SetParent'.format(config))
            if side_guide.startswith(nc['right']):
                block_parent = block_parent.replace(nc['left'],nc['right'])

        #smart select the colors
        if str(side_guide).startswith(nc['left']):
            color = setup['left_color']
        elif str(side_guide).startswith(nc['right']):
            color = setup['right_color']       
        else:
            color = setup['main_color']       

        #main funcion
        cmds.select(side_guide)
        fk_chain = mt.fk_chain(input = '', 
                    size = cmds.getAttr('{}.CtrlSize'.format(config)), 
                    color = color, 
                    curve_type = cmds.getAttr('{}.CtrlType'.format(config), asString = True))

        for_parent = cmds.listRelatives(fk_chain[0], p=True)
        print (fk_chain)
            
        auto_grp = mt.root_grp(input = fk_chain[0], custom = True, custom_name = '_AutoFK', autoRoot = False, replace_nc = False)
        #check if the mirror attrs to Only_Right or mirror to True
        
        
        if cmds.getAttr('{}.Mirror'.format(config), asString = True) == 'Right_Only':
            miror_ctrl_grp = mt.mirror_group(cmds.listRelatives(auto_grp, p=True), world = True)
            miror_jnt_grp = mt.mirror_group( new_guide, world = True)
            cmds.parentConstraint(block_parent, miror_ctrl_grp , mo = True)     

        elif cmds.getAttr('{}.Mirror'.format(config), asString = True) == 'True':
            if str(side_guide).startswith(nc['right']) :
                miror_ctrl_grp = mt.mirror_group(cmds.listRelatives(auto_grp, p=True), world = True)
                miror_jnt_grp = mt.mirror_group(side_guide, world = True)
                cmds.parentConstraint(block_parent, miror_ctrl_grp , mo = True) 
            else:
                cmds.parentConstraint(block_parent, for_parent , mo = True) 
        
        
     
    print ('Build {} Success 07'.format(block))

    



#build_clavicle_block()
