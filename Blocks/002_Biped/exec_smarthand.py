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

#---------------------------------------------
TAB_FOLDER = '002_Biped'
PYBLOCK_NAME = 'exec_smarthand'

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

MODULE_FILE = os.path.join(os.path.dirname(__file__),'01_SmartHand.json')
with open(MODULE_FILE) as module_file:
	module = json.load(module_file)

#---------------------------------------------

def create_smarthand_block(name = 'SmartHand'):

    nc, curve_data, setup = mt.import_configs()
    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name = name, icon = 'SmartHand',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]
    name = block.replace(nc['module'],'')

    #cmds.getAttr('{}.AttrName'.format(config)) #get attrs from config
    #cmds.getAttr('{}.AttrName'.format(config), asString = True) #for enums
    #joint_one = mt.create_joint_guide(name = name) #guide base with shapes

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_smarthand_block()

#-------------------------

def build_smarthand_block():

    mt.check_is_there_is_base()


    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]

    hand_block = cmds.getAttr('{}.HandBlock'.format(config), asString=True)

    if cmds.objExists(hand_block+'_Wrist_Ctrl'):
        to_build = [hand_block, hand_block.replace(nc['left'], nc['right'])]
    else:
        to_build = [hand_block]

    #build ------------------------------------------------------
    for side_guide in to_build:

        #smart select the colors
        if str(side_guide).startswith(nc['left']):
            color = setup['left_color']
        elif str(side_guide).startswith(nc['right']):
            color = setup['right_color']       
        else:
            color = setup['main_color']       

        fingers = ['Pinky','Ring','Middle','Index']
        thumb = ['Thumb']

        size = mt.get_distance_between('{}_Middle_03_Ctrl'.format(side_guide), '{}_Middle_02_Ctrl'.format(side_guide))

        cmds.select(cl=True)
        main_ctrl = mt.curve(input='{}_Middle_03_Ctrl'.format(side_guide),
                        type='sphere',
                        rename=True,
                        custom_name=True,
                        name=side_guide+'_Middle_03_Ctrl'.replace(nc['ctrl'], '_Smart'+nc['ctrl']),
                        size=size)
        mt.assign_color(color=color)
        root_grp, auto_grp = mt.root_grp(autoRoot=True)
        mt.match(root_grp, '{}_Middle_03_Ctrl'.format(side_guide), r=True, t=True)
        cmds.parent(root_grp, setup['base_groups']['control'] + nc['group'])
        if side_guide.startswith(nc['right']):
            cmds.move(-5,0,0, auto_grp, r=True)
        else:
            cmds.move(5,0,0, auto_grp, r=True)


        mt.hide_attr(main_ctrl, t=True, s=True, rotate_order=True)
        cmds.parentConstraint('{}_Wrist_Ctrl'.format(side_guide), root_grp, mo=True)

        for finger in fingers:
            for num in range(1, 4):
                ctrl = '{}_{}_0{}_Ctrl'.format(side_guide, finger, num)
                if not cmds.objExists(ctrl):
                    continue
                cmds.select(cl=True)
                curl_root = mt.root_grp(ctrl, custom=True, custom_name=ctrl.replace('_Ctrl', '_SmartCurl_RootGrp'))[0]
                curl = mt.root_grp(ctrl, custom=True, custom_name=ctrl.replace('_Ctrl', '_SmartCurl_Grp'))[0]
                cmds.select(cl=True)
                side_to_side_root = mt.root_grp(ctrl, custom=True, custom_name=ctrl.replace('_Ctrl', '_Sides_RootGrp'))[0]
                side_to_side = mt.root_grp(ctrl, custom=True, custom_name=ctrl.replace('_Ctrl', '_Sides_Grp'))[0]
                cmds.select(cl=True)
                spread_root = mt.root_grp(ctrl, custom=True, custom_name=ctrl.replace('_Ctrl', '_SmartSpread_RootGrp'))[0]
                spread = mt.root_grp(ctrl, custom=True, custom_name=ctrl.replace('_Ctrl', '_SmartSpread_Grp'))[0]

                mt.connect_md_node(in_x1=main_ctrl+'.rotateZ',
                                   in_x2=1.0,
                                   out_x=curl+'.rotateZ'
                                   , mode='mult', name='', force=True)

                if num > 1:
                    continue

                mt.connect_md_node(in_x1=main_ctrl+'.rotateY',
                                   in_x2=1.0,
                                   out_x=side_to_side+'.rotateY'
                                   , mode='mult', name='', force=True)

                if finger == 'Middle':
                    value = -0.15
                elif finger == 'Pinky':
                    value = 0.6
                elif finger == 'Ring':
                    value = 0.15
                elif finger == 'Index':
                    value = -0.6

                mt.connect_md_node(in_x1=main_ctrl + '.rotateX',
                                   in_x2=value,
                                   out_x=spread + '.rotateZ'
                                   , mode='mult', name='', force=True)

                #Reset Right Roots
                for grp in [curl_root, spread_root, side_to_side_root]:
                    if grp.startswith(nc['right']):
                        cmds.setAttr('{}.rx'.format(grp), 0)
                        cmds.setAttr('{}.ry'.format(grp), 0)
                        cmds.setAttr('{}.rz'.format(grp), 0)
                        cmds.setAttr('{}.sx'.format(grp), 1)

    # build complete ----------------------------------------------------    
    print ('Build {} Success'.format(block))


#build_smarthand_block()
