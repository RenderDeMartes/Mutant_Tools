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

TAB_FOLDER = '02_Biped'
PYBLOCK_NAME = 'exec_head'

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

MODULE_FILE = (os.path.dirname(__file__) +'/03_Pelvis.json')
with open(MODULE_FILE) as module_file:
	module = json.load(module_file)


#---------------------------------------------

def create_pelvis_block(name = 'Pelvis'):

    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name = name, icon = 'Pelvis',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]

    cmds.select(cl=True)
    clav_guide = mt.create_joint_guide(name = name)
    cmds.move(3,0,0)
    clav_guideEnd = mt.create_joint_guide(name = name + 'End')
    cmds.move(9,0,0)
    cmds.parent(clav_guideEnd, clav_guide)
    cmds.parent(clav_guide, block)
    cmds.select(block)

    mt.orient_joint(input = clav_guide)


    print('{} Created Successfully'.format(name))

#create_hip_block()

#-------------------------

def build_pelvis_block():

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guide = cmds.listRelatives(block, c=True)[0]

    #orient the joints
    mt.orient_joint(input = guide)
    new_guide = mt.duplicate_and_remove_guides(guide)
    print (new_guide)
    to_build = [new_guide]

    #use this group for later cleaning, just assign them when you create the top on hierarchy
    clean_rig_grp = ''
    clean_ctrl_grp = ''


    #prep work for right side ------------------------------------------------------

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


        #main funcion -------------------------------------------
        cmds.select(side_guide)
        fk_chain = mt.fk_chain(input = '', 
                    size = cmds.getAttr('{}.CtrlSize'.format(config)), 
                    color = color, 
                    curve_type = cmds.getAttr('{}.CtrlType'.format(config), asString = True))

        for_parent = cmds.listRelatives(fk_chain[0], p=True)
        mt.hide_attr(fk_chain[0], s=True)
        print (fk_chain)
            

        #blends groups

        #flip right rig  to right side ------------------------- 
        #check if the mirror attrs to Only_Right or mirror to True
        if cmds.getAttr('{}.Mirror'.format(config), asString = True) == 'Right_Only':
            miror_ctrl_grp = mt.mirror_group(cmds.listRelatives(fk_chain[0], p=True)[0], world = True)
            miror_jnt_grp = mt.mirror_group(new_guide, world = True)
            cmds.parentConstraint(block_parent, cmds.listRelatives(fk_chain[0],p=True)[0], mo = True)
            clean_rig_grp = miror_jnt_grp
            clean_ctrl_grp = miror_ctrl_grp

        elif cmds.getAttr('{}.Mirror'.format(config), asString = True) == 'True':
            if str(side_guide).startswith(nc['right']) :
                miror_ctrl_grp = mt.mirror_group(cmds.listRelatives(fk_chain[0], p=True)[0], world = True)
                miror_jnt_grp = mt.mirror_group(side_guide, world = True)
                cmds.parentConstraint(block_parent, cmds.listRelatives(fk_chain[0],p=True)[0] , mo = True)
                clean_rig_grp = miror_jnt_grp
                clean_ctrl_grp = miror_ctrl_grp
            else:
                cmds.parentConstraint(block_parent, for_parent , mo = True) 
                clean_rig_grp = side_guide
                clean_ctrl_grp = for_parent        
        
        else: #only left side
            cmds.parentConstraint(block_parent, for_parent , mo = True) 
            clean_rig_grp = side_guide
            clean_ctrl_grp = for_parent   

        #create bind Joints for the skin
        cmds.select(cl=True)
        bind_joint = cmds.joint(n = side_guide.replace(nc['joint'], nc['joint_bind']))
        cmds.makeIdentity(bind_joint, a=True, t=True, r=True, s=True)
        cmds.parentConstraint(side_guide, bind_joint, mo = False)
        cmds.scaleConstraint(side_guide, bind_joint, mo = True)
        cmds.setAttr('{}.segmentScaleCompensate'.format(bind_joint), 0)
        cmds.setAttr('{}.inheritsTransform'.format(bind_joint), 0)

        try: cmds.parent(bind_joint, w=True)
        except:pass
        cmds.setAttr('{}.radius'.format(bind_joint), 1.5)

        #Clean -------------------------------------------
        #game parents for bind joints
        game_parent = cmds.getAttr('{}.SetGameParent'.format(config))
        if side_guide.startswith(nc['right']):
            game_parent = game_parent.replace(nc['left'],nc['right'])

        if cmds.objExists(game_parent):
            cmds.parent(bind_joint, game_parent) 
        else: 
            bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])
            if cmds.objExists(bind_jnt_grp):
                cmds.parent(bind_joint, bind_jnt_grp) 
           
        #clean ctrls
        cmds.parent(clean_ctrl_grp, 'Rig_Ctrl_Grp')

        #clean rig
        cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))

          
        

    # build complete ----------------------------------------------------    
    print ('Build {} Success'.format(block))


#build_hip_block()