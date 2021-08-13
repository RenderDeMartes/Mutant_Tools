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

TAB_FOLDER = 'TAB'
PYBLOCK_NAME = 'exec_NAME'

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

MODULE_FILE = (os.path.dirname(__file__) +'/num_name.json')
with open(MODULE_FILE) as module_file:
	module = json.load(module_file)

#---------------------------------------------

def create_NAME_block(name = 'NAME'):

    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name = name, icon = 'ICON_NAME',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]
      
    #cmds.getAttr('{}.AttrName'.format(config)) #get attrs from config
    #cmds.getAttr('{}.AttrName'.format(config), asString = True) #for enums
    #joint_one = mt.create_joint_guide(name = name) #guide base with shapes

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_NAME_block()

#-------------------------

def build_NAME_block():

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


        #create bind Joints for the skin ------------------------- 
        '''
        bind_joint = cmds.duplicate(side_guide, po=True, n = side_guide.replace(nc['joint'], nc['joint_bind']))[0] 
        cmds.parentConstraint(side_guide, bind_joint, mo = False)
        try: cmds.parent(bind_joint, w=True)
        except:pass
        cmds.setAttr('{}.radius'.format(bind_joint), 1.5)
        '''

        #flip right rig  to right side ------------------------- 
        '''
        #check if the mirror attrs to Only_Right or mirror to True
        if cmds.getAttr('{}.Mirror'.format(config), asString = True) == 'Right_Only':
            miror_ctrl_grp = mt.mirror_group(cmds.listRelatives(auto_grp, p=True)[0], world = True)
            miror_jnt_grp = mt.mirror_group(new_guide, world = True)
            cmds.parentConstraint(block_parent, miror_ctrl_grp , mo = True)     
            clean_rig_grp = miror_jnt_grp
            clean_ctrl_grp = miror_ctrl_grp

        elif cmds.getAttr('{}.Mirror'.format(config), asString = True) == 'True':
            if str(side_guide).startswith(nc['right']) :
                miror_ctrl_grp = mt.mirror_group(cmds.listRelatives(auto_grp, p=True)[0], world = True)
                miror_jnt_grp = mt.mirror_group(side_guide, world = True)
                cmds.parentConstraint(block_parent, miror_ctrl_grp , mo = True) 
                clean_rig_grp = miror_jnt_grp
                clean_ctrl_grp = miror_ctrl_grp
            else:
                cmds.parentConstraint(block_parent, for_parent , mo = True) 
                clean_rig_grp = side_guide
                clean_ctrl_grp = for_parent        
        
        else: #only left side
            cmds.parentConstraint(block_parent, for_parent , mo = True) 
        '''

        #blends
        '''
        blends_grp = mt.root_grp(input = '', custom = True, custom_name = 'Blends', autoRoot = False, replace_nc = False)[0]
        blends_grp = blends_grp.replace('_AutoFK','')
        bends = cmds.getAttr('{}.Blends'.format(config).split(':'))
        for blend in bends:
            ''
            #cmds.orientConstraint()
        '''

        #Finish -------------------------------------------
        '''
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

        #parent rig
        cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))

        '''  

    #clean a bit
    clean_rig_grp = cmds.group(em=True, n = '{}{}'.format(block.replace(nc['module'],'_Rig'), nc['group']))

    

    # build complete ----------------------------------------------------    
    print ('Build {} Success'.format(block))


#build_NAME_block()
