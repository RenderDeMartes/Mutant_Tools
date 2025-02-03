from __future__ import absolute_import, division
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
PYBLOCK_NAME = 'exec_chasis'

#---------------------------------------------

def create_chasis_block(name = 'Chasis'):

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

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '04_Chasis.json')
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

    block = mt.create_block(name = name, icon = 'Chasis',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]

    joint_one = mt.create_joint_guide(name=name+'_Center')  # guide base with shapes
    joint_back = mt.create_joint_guide(name=name+'_Back')  # guide base with shapes
    cmds.move(0,0,-2)
    joint_front = mt.create_joint_guide(name=name+'_Front')  # guide base with shapes
    cmds.move(0,0,2)

    cmds.parent(joint_back, joint_one)
    cmds.parent(joint_front, joint_one)
    cmds.parent(joint_one, block)
    cmds.select(block)

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_chasis_block()

#-------------------------

def build_chasis_block():
    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guide = cmds.listRelatives(block, c=1)[0]
    name = block.replace(nc['module'], '')

    new_guide = mt.duplicate_and_remove_guides(guide)
    print('guide:', new_guide)

    cmds.select(new_guide, hi=True)
    new_guides = cmds.ls(sl=True)


    main_guide = new_guides[0]
    for g in new_guides:
        if 'Back' in g:
            back_guide = g
        if 'Front' in g:
            front_guide = g

    #Order grps
    clean_rig_grp = cmds.group(em=True, name = name + '_Rig' + nc['group'])
    clean_ctrl_grp = cmds.group(em=True, name = name + nc['ctrl'] + nc['group'])


    # build
    block_parent = cmds.getAttr('{}.SetParent'.format(config))

    if block_parent == 'new_locator':
        block_parent = cmds.spaceLocator(n='{}'.format(str(new_guide).replace(nc['joint'], '_Parent' + nc['locator'])))

    size = cmds.getAttr("{}.tz".format(back_guide))
    curve_type = 'trapezoid'
    main_color = 'purple'
    sec_color = 'green'

    cmds.select(new_guide)

    #Create 2 controllers for main one
    main_ctrl = mt.curve(input=main_guide,
                    type='trapezoid',
                    rename=True,
                    custom_name=True,
                    name=main_guide.replace(nc['joint'], nc['ctrl']),
                    size=size*-1)
    mt.hide_attr(main_ctrl, s=True)
    mt.assign_color(color=main_color)
    main_root_grp = mt.root_grp()[0]
    mt.match(main_root_grp, main_guide, r=True, t=True)
    #cmds.parentConstraint(main_ctrl, main_guide)
    mt.line_attr(main_ctrl, name='Manual Rotation')


    suspension_ctrl = mt.curve(input=main_guide,
                    type='3dArrow',
                    rename=True,
                    custom_name=True,
                    name=main_guide.replace(nc['joint'], '_Suspension' + nc['ctrl']),
                    size=size/-5)
    mt.hide_attr(suspension_ctrl, s=True)
    mt.assign_color(color=main_color)
    suspension_root_grp = mt.root_grp()[0]
    mt.match(suspension_root_grp, main_guide, r=True, t=True)
    cmds.parentConstraint(suspension_ctrl, main_guide)
    cmds.scaleConstraint(suspension_ctrl, main_guide)

    cmds.parent(suspension_root_grp, main_ctrl)

    #Create 2 controllers for 2 front/back ones

    #Parent hierarchy
    cmds.parentConstraint(block_parent, clean_ctrl_grp)
    cmds.scaleConstraint(block_parent, clean_ctrl_grp)

    # create bind joints
    bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])
    for jnt in [main_guide]:
        cmds.select(cl=True)
        bind_joint = cmds.joint(n=jnt.replace(nc['joint'], nc['joint_bind']))
        cmds.parentConstraint(jnt, bind_joint)
        cmds.scaleConstraint(jnt, bind_joint)
        cmds.setAttr('{}.radius'.format(bind_joint), 1.5)
        cmds.parent(bind_joint, bind_jnt_grp)


        #Clean a bit
    cmds.parent(main_root_grp, clean_ctrl_grp)
    cmds.parent(main_guide, clean_rig_grp)
    cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
    cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])



#build_chasis_block()
