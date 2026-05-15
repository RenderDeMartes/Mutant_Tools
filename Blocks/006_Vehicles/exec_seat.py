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

TAB_FOLDER = '006_Vehicles'
PYBLOCK_NAME = 'exec_seat'

#---------------------------------------------

def create_seat_block(name = 'Seat'):

    #---------------------------------------------------
    #---------------------------------------------------
    #---------------------------------------------------


    # Read name conventions as nc[''] and setup as seup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-2]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '05_Seat.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()

    #---------------------------------------------------
    #---------------------------------------------------
    #---------------------------------------------------

    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name = name, icon = 'Seat',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]
      
    joint_seat = mt.create_joint_guide(name=name+'_Seat')  # guide base with shapes
    joint_back = mt.create_joint_guide(name=name+'_Back')  # guide base with shapes
    cmds.move(0,0,-2)
    joint_back_top = mt.create_joint_guide(name=name+'_BackTop')  # guide base with shapes
    cmds.move(0,2,-2)

    cmds.parent(joint_back, joint_seat)
    cmds.parent(joint_back_top, joint_back)
    cmds.parent(joint_seat, block)
    cmds.select(block)

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_seat_block()

#-------------------------

def build_seat_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guide = cmds.listRelatives(block, c=True)[0]

    # orient the joints
    # mt.orient_joint(input=guide)
    new_guide = mt.duplicate_and_remove_guides(guide)
    print(new_guide)
    to_build = [new_guide]

    # use this group for later cleaning, just assign them when you create the top on hi
    clean_rig_grp = ''
    clean_ctrl_grp = ''

    if cmds.getAttr('{}.Mirror'.format(config), asString=True) == 'True':
        right_guide = mt.duplicate_change_names(input=new_guide, hi=True, search=nc['left'], replace=nc['right'])[0]
        to_build.append(right_guide)
        print(to_build)

    # build ------------------------------------------------------
    for side_guide in to_build:

        # use this locator in case parent is set to new locator
        if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
            block_parent = cmds.spaceLocator(
                n='{}'.format(str(side_guide).replace(nc['joint'], '_Parent' + nc['locator'])))
        else:
            block_parent = cmds.getAttr('{}.SetParent'.format(config))
            if side_guide.startswith(nc['right']):
                block_parent = block_parent.replace(nc['left'], nc['right'])

        # smart select the colors
        if str(side_guide).startswith(nc['left']):
            color = setup['left_color']
        elif str(side_guide).startswith(nc['right']):
            color = setup['right_color']
        else:
            color = setup['main_color']

        size = cmds.getAttr("{}.tx".format(side_guide))

        # main funcion
        cmds.select(side_guide, hierarchy=True)
        joints = cmds.ls(sl=True)
        fk_chain = mt.fk_chain(input='',
                               size=size,
                               color=color,
                               curve_type='cube'
                               )
        fk_parent = cmds.listRelatives(fk_chain[0], p=True)
        #mt.hide_attr(fk_chain[0], s=True)
        print(fk_chain)

        # check if the mirror attrs to Only_Right or mirror to True
        if cmds.getAttr('{}.Mirror'.format(config), asString=True) == 'True':
            if str(side_guide).startswith(nc['right']):
                miror_ctrl_grp = mt.mirror_group(fk_parent, world=True)
                miror_jnt_grp = mt.mirror_group(side_guide, world=True)
                cmds.parentConstraint(block_parent, fk_parent, mo=True)
                clean_rig_grp = miror_jnt_grp
                clean_ctrl_grp = miror_ctrl_grp
            else:
                cmds.parentConstraint(block_parent, fk_parent, mo=True)
                clean_rig_grp = side_guide
                clean_ctrl_grp = fk_parent
        else:
            cmds.parentConstraint(block_parent, fk_parent, mo=True)
            clean_rig_grp = side_guide
            clean_ctrl_grp = fk_parent

        # create bind Joints for the skin
        # create bind joints
        bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])
        for jnt in joints:
            cmds.setAttr("{}.segmentScaleCompensate".format(jnt), 0)
            cmds.select(cl=True)
            bind_joint = cmds.joint(n=jnt.replace(nc['joint'], nc['joint_bind']))
            cmds.setAttr('{}.radius'.format(bind_joint), 1.5)
            cmds.parent(bind_joint, bind_jnt_grp)
            cmds.parentConstraint(jnt, bind_joint)
            cmds.scaleConstraint(jnt, bind_joint)

        # Clean ----------------------------
        # clean ctrls
        cmds.parent(clean_ctrl_grp, 'Rig_Ctrl_Grp')

        # clean rig
        cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))

        # scale
        cmds.scaleConstraint('Global_Ctrl', clean_rig_grp, mo=True)

    print('Build {} Success'.format(block))
    print("___________________")
    print(joints)

#build_seat_block()
