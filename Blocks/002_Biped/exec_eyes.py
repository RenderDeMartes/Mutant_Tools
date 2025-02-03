from __future__ import absolute_import, division
from maya import cmds, mel
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
PYBLOCK_NAME = 'exec_eyes'


#---------------------------------------------

def create_eyes_block(name = 'Eyes'):

    nc, curve_data, setup = mt.import_configs()

    # Read name conventions as nc[''] and setup as setup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-2]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '008_Eyes.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)


    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name = name, icon = 'Eyes',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]

    eye = mt.create_joint_guide(name = name)
    cmds.move(2,0,0)
    aim = mt.create_joint_guide(name = name + '_Aim')
    cmds.move(2,0,5)
    cmds.parent(aim, eye)
    cmds.parent(eye, block)
    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_eyes_block()

#-------------------------

def build_eyes_block():

    nc, curve_data, setup = mt.import_configs()

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
    name = guide.replace(nc['guide'], '')
    if nc['left'] in name:
        name = name.replace(nc['left'], '')
    if nc['right'] in name:
        name = name.replace(nc['left'], '')

    #use this locator in case parent is set to new locator
    if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
        block_parent = cmds.spaceLocator( n = '{}'.format(str(block).replace(nc['module'],'_Parent' + nc['locator'])))[0]
    else:
        block_parent = cmds.getAttr('{}.SetParent'.format(config))

    ctrl_size = cmds.getAttr('{}.CtrlSize'.format(config))
    eyes_amount = cmds.getAttr('{}.EyesAmount'.format(config), asString = True)

    #Build Eye System
    to_build = [new_guide]

    main_eye_ctrl = mt.curve(input=cmds.listRelatives(new_guide,c=True)[0],
                            type='square',
                            rename=True,
                            custom_name=True,
                            name=name + '_Main' + nc['ctrl'],
                            size=ctrl_size)
    main_eye_root = mt.root_grp()[0]
    cmds.select(main_eye_ctrl+'.cv[0:4]')
    cmds.rotate(90,0,90)



    right_guide = mt.duplicate_change_names(input = new_guide, hi = True, search=nc['left'], replace =nc['right'])[0]
    cmds.delete(cmds.parentConstraint(cmds.listRelatives(new_guide,c=True)[0],
                          cmds.listRelatives(right_guide,c=True)[0],
                          main_eye_root))
    cmds.setAttr(main_eye_root+'.translateX', 0)
    if eyes_amount == 'Two':
        to_build.append(right_guide)
    else:
        cmds.delete(right_guide)


    eyes_ctrls = []
    eyes_root= []
    clean_rig_grps=[]
    for side_guide in to_build:
        aim_ik = cmds.ikHandle(sj=side_guide,
                               ee=cmds.listRelatives(side_guide,c=True)[0],
                               sol='ikSCsolver',
                               n=side_guide.replace(nc['joint'], '_Aim'+nc['ik_sc']),
                               ccv=False,
                               pcv=False)

        # Eye controller
        eye_ctrl = mt.curve(input=side_guide,
                            type='circleZ',
                            rename=True,
                            custom_name=True,
                            name=side_guide.replace(nc['joint'], nc['ctrl']),
                            size=ctrl_size/2)
        cmds.rotate(0,0,0)
        eyes_ctrls.append(eye_ctrl)
        if side_guide.startswith(nc['right']):
            color='red'
        elif side_guide.startswith(nc['left']):
            color='blue'
        else:
            color = 'yellow'
        mt.assign_color(color=color)
        eye_ctrl_root = mt.root_grp()[0]

        rig_group = cmds.group(aim_ik[0], side_guide, n = name+'Eye'+nc['group'])

        #mirror system
        if eyes_amount == 'Two':
            if str(side_guide).startswith(nc['right']) :
                eye_ctrl_root = mt.mirror_group(eye_ctrl_root, world = True)
                rig_group = mt.mirror_group(rig_group, world = True)

        cmds.parent(eye_ctrl_root, main_eye_ctrl)
        eyes_root.append(eye_ctrl_root)

        clean_rig_grps.append(rig_group)

        #parent Ctrl to Ik
        cmds.parentConstraint(eye_ctrl, aim_ik[0], mo=True)


    #clean a bit
    clean_ctrl_grp = cmds.group(em=True, name = name + nc['ctrl'] + nc['group'])
    clean_rig_grp = cmds.group(em=True, name = name + '_Rig' + nc['group'])
    cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
    cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])

    cmds.parent(main_eye_root, clean_ctrl_grp)
    cmds.parent(clean_rig_grps, clean_rig_grp)


    for jnt in to_build:
        cmds.parentConstraint(block_parent, jnt, mo=-True)
    cmds.parentConstraint(block_parent, main_eye_root, mo=True)

    #Bind joints
    bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])
    for jnt in to_build:
        cmds.select(cl=True)
        bind_joint = cmds.joint(n = jnt.replace(nc['joint'], nc['joint_bind']))
        cmds.parentConstraint(jnt, bind_joint)
        cmds.setAttr('{}.radius'.format(bind_joint), 1.5)
        cmds.parent(bind_joint, bind_jnt_grp)
        cmds.scaleConstraint('Global_Ctrl', jnt)
        cmds.scaleConstraint(jnt, bind_joint)



    #Add shared loc
    all_controllers = eyes_ctrls + [main_eye_ctrl]
    for ctrl in all_controllers:
        cmds.select(ctrl)
        if cmds.objectType(ctrl) == 'transform':
            eyes_attrs_loc = mt.shape_with_attr(input='', obj_name='{}_Attrs'.format(name), attr_name='Test').split('.')[0]
    mel.eval('catch (`deleteAttr -attribute "Test" "{}|{}_Attrs_Loc"`);'.format(main_eye_ctrl, name))

    #add attrs
    ctrl = main_eye_ctrl
    offset = main_eye_root
    root, auto = mt.root_grp(input=ctrl, autoRoot=True)



    cmds.scaleConstraint('Global_Ctrl', clean_ctrl_grp)
    cmds.scaleConstraint('Global_Ctrl', clean_rig_grp)


    #-----------------------------------------------
    print ('Build {} Success'.format(block))



#build_eyes_block()
