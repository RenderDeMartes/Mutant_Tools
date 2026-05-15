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
PYBLOCK_NAME = 'exec_wheel'

#---------------------------------------------

def create_wheel_block(name = 'Wheel'):

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

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '03_Wheel.json')
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

    block = mt.create_block(name = name, icon = 'Wheel',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]
      
    #cmds.getAttr('{}.AttrName'.format(config)) #get attrs from config
    #cmds.getAttr('{}.AttrName'.format(config), asString = True) #for enums
    joint_one = mt.create_joint_guide(name = name) #guide base with shapes
    cmds.parent(joint_one, block)
    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_wheel_block()

#-------------------------

def build_wheel_block():
    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guide = cmds.listRelatives(block, c=True)[0]
    name = block.replace(nc['module'], '')

    # orient the joints
    #mt.orient_joint(input=guide)
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

    # Manual Rotation
    attrs_pos = cmds.getAttr('{}.SetManualRotationAttPos'.format(config))
    wheel_rotation_attr = mt.new_attr(input=attrs_pos, name='{}Rotation'.format(name.replace(nc['left'], '').replace(nc['right'], '')), min=-9999, max=9999, default=0)
    wheel_steeering_attr = mt.new_attr(input=attrs_pos, name='{}Steering'.format(name.replace(nc['left'], '').replace(nc['right'], '')), min=-9999, max=9999, default=0)



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
        root, auto = mt.root_grp(input=side_guide, autoRoot=True)
        cmds.select(auto)
        fk_chain = mt.fk_chain(input='',
                               size=size,
                               color=color,
                               curve_type='wheel')
        fk_chain = cmds.rename(fk_chain[0], fk_chain[0].replace('_Auto'+nc['group'], ''))
        fk_parent = cmds.listRelatives(fk_chain, p=True)
        mt.hide_attr(fk_chain, s=True, t=1)
        print(fk_chain)

        #manual rotate
        manual_grp = mt.root_grp(input=side_guide, custom=True, custom_name ='_ManualRotate')[0]
        cmds.connectAttr(wheel_rotation_attr, '{}.rotateX'.format(manual_grp))

        #Steering
        auto_steer_grp = mt.root_grp(fk_chain, custom=True, custom_name='_Steering')[0]
        cmds.connectAttr(wheel_steeering_attr, '{}.rotateY'.format(auto_steer_grp))

        # Create Dummy Ctrl
        cmds.select(cl=True)
        vis_ctrl = mt.curve(input='',
                        type='wheel',
                        rename=True,
                        custom_name=True,
                        name=side_guide.replace(nc['joint'], '_Vis'+nc['ctrl']),
                        size=size*0.5)
        mt.assign_color(vis_ctrl, color='grey')
        vis_root, vis_auto = mt.root_grp(input=vis_ctrl, autoRoot=True)
        mt.assign_color(color=color)
        cmds.parentConstraint(side_guide, vis_root, mo=False)
        cmds.scaleConstraint(side_guide, vis_root, mo=False)
        mt.hide_attr(vis_ctrl, s=True, t=True, r=True)

        # check if the mirror attrs to Only_Right or mirror to True
        if cmds.getAttr('{}.Mirror'.format(config), asString=True) == 'True':
            if str(side_guide).startswith(nc['right']):

                #Mirror a bit diferent to keep the same orient
                temp_loc = cmds.spaceLocator()[0]
                mt.match(temp_loc, fk_parent, t=True)
                temp_mirror_grp = mt.mirror_group(temp_loc, world=True)
                mt.match(fk_parent, temp_loc, t=True, r=False)
                clean_rig_grp = root
                clean_ctrl_grp = fk_parent
                cmds.setAttr('{}.scaleZ'.format(fk_parent[0]), 1)
                cmds.delete(temp_mirror_grp)
                cmds.parentConstraint(block_parent, fk_parent, mo=True)
            else:
                cmds.parentConstraint(block_parent, fk_parent, mo=True)
                clean_rig_grp = root
                clean_ctrl_grp = fk_parent
        else:
            cmds.parentConstraint(block_parent, fk_parent, mo=True)
            clean_rig_grp = root
            clean_ctrl_grp = fk_parent

        # create bind Joints for the skin
        cmds.select(cl=True)
        bind_joint = cmds.joint(n=side_guide.replace(nc['joint'], nc['joint_bind']))
        cmds.makeIdentity(bind_joint, a=True, t=True, r=True, s=True)
        cmds.parentConstraint(side_guide, bind_joint, mo=False)
        cmds.scaleConstraint(side_guide, bind_joint, mo=True)
        cmds.setAttr('{}.segmentScaleCompensate'.format(bind_joint), 0)
        cmds.setAttr('{}.inheritsTransform'.format(bind_joint), 0)

        try:
            cmds.parent(bind_joint, w=True)
        except:
            pass
        cmds.setAttr('{}.radius'.format(bind_joint), 1.5)

        # Clean ----------------------------

        bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])
        if cmds.objExists(bind_jnt_grp):
            cmds.parent(bind_joint, bind_jnt_grp)

        # clean ctrls
        cmds.parent(vis_root, clean_ctrl_grp)
        cmds.parent(clean_ctrl_grp, 'Rig_Ctrl_Grp')

        # clean rig
        cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))

        # scale
        cmds.scaleConstraint('Global_Ctrl', clean_rig_grp, mo=True)

    print('Build {} Success'.format(block))

#build_wheel_block()
