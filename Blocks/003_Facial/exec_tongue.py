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

TAB_FOLDER = '003_Facial'
PYBLOCK_NAME = 'exec_tongue'



#---------------------------------------------

def create_tongue_block(name = 'Tongue'):

    # Read name conventions as nc[''] and setup as seup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-2]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '010_Tongue.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()

    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name = name, icon = 'Tongue',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]
      
    joint_a = mt.create_joint_guide(name = name + '_01')
    cmds.move(0,0,-2)
    cmds.parent(joint_a, block)
    joint_b = mt.create_joint_guide(name = name + '_02')
    cmds.move(0,0,-1)
    cmds.parent(joint_b, joint_a)
    joint_c = mt.create_joint_guide(name = name + '_03')
    cmds.move(0,0,0)
    cmds.parent(joint_c, joint_b)
    joint_d = mt.create_joint_guide(name = name + '_04')
    cmds.move(0,0,1)
    cmds.parent(joint_d, joint_c)
    joint_e = mt.create_joint_guide(name = name + '_05')
    cmds.move(0,0,2)
    cmds.parent(joint_e, joint_d)


    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_tongue_block()

#-------------------------

def build_tongue_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guide = cmds.listRelatives(block, c=True)[0]
    name = block.replace(nc['module'], '')
    #groups for later cleaning
    clean_rig_grp = ''
    clean_ctrl_grp = ''
    
    ctrl_size = cmds.getAttr('{}.CtrlSize'.format(config))
    ctrl_color = cmds.getAttr('{}.CtrlColor'.format(config), asString = True)

    #orient the joints
    new_guide = mt.duplicate_and_remove_guides(guide)
    cmds.makeIdentity(new_guide, a=True, t=True, r=True, s=True)
    cmds.select(new_guide)
    for jnt in reversed(cmds.listRelatives(new_guide, ad=True)[1:]):
        cmds.makeIdentity(jnt, a=True, t=True, r=True, s=True)
        cmds.select(jnt, add=True)

    joints = cmds.ls(sl=True)
    fk_ctrls = mt.fk_chain(input = '', size = ctrl_size, color = ctrl_color, curve_type = 'circleZ', scale = True, twist_axis = 'Z')
    granfather_ctrl_root = cmds.listRelatives(fk_ctrls[0],p=True)

    #vis
    attrs_position = cmds.getAttr('{}.SetAttrsPosition'.format(config), asString=True)
    if attrs_position == 'new_locator':
        guide_attrs_position = cmds.spaceLocator(n=name + '_Attrs' + nc['locator'])[0]
    else:
        guide_attrs_position = attrs_position

    mt.line_attr(input=guide_attrs_position, name='{}_Vis'.format(name))
    main_vis_attr = mt.new_enum(input=guide_attrs_position, name='{}MainCtrl'.format(name), enums='Hide:Show', keyable=False)
    tweek_vis_attr = mt.new_enum(input=guide_attrs_position, name='{}TweekCtrls'.format(name), enums='Hide:Show', keyable=False)
    cmds.setAttr(main_vis_attr,1)

    main_ctrl = mt.curve(input=new_guide,
                          type='2dArrow',
                          rename=True,
                          custom_name=True,
                          name=name+'_Main'+nc['ctrl'],
                          size=ctrl_size)
    mt.assign_color(color=ctrl_color)
    main_root_grp = mt.root_grp()[0]
    mt.match(main_root_grp, fk_ctrls[-1], r=True, t=True)
    cmds.select(main_ctrl+'.cv[0:9]')
    cmds.rotate(90,0,90)
    cmds.connectAttr(main_vis_attr, cmds.listRelatives(main_ctrl, s=True)[0]+'.v')

    for ctrl in fk_ctrls:
        cmds.select(ctrl)
        root, auto = mt.root_grp(autoRoot=True)
        cmds.connectAttr(tweek_vis_attr, cmds.listRelatives(ctrl, s=True)[0]+'.v')
        #omit 1st joint translate
        if ctrl == fk_ctrls[0]:
            continue
        cmds.connectAttr('{}.rotate'.format(main_ctrl), '{}.rotate'.format(auto))
        cmds.connectAttr('{}.translate'.format(main_ctrl), '{}.translate'.format(auto))
        cmds.connectAttr('{}.scale'.format(main_ctrl), '{}.scale'.format(auto))


    #use this locator in case parent is set to new locator
    if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
        block_parent = cmds.spaceLocator( n = '{}'.format(str(block).replace(nc['module'],'_Parent' + nc['locator'])))
    else:
        block_parent = cmds.getAttr('{}.SetParent'.format(config))

    bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])

    bind_joints=[]
    for num, jnt in enumerate(joints):
        cmds.select(cl=True)
        bind_joint = cmds.joint(n=jnt.replace(nc['joint'], nc['joint_bind']))
        cmds.parentConstraint(jnt, bind_joint)
        cmds.scaleConstraint(jnt, bind_joint)
        cmds.setAttr('{}.radius'.format(bind_joint), 1.5)
        try:cmds.parent(bind_joint, bind_joints[num-1])
        except:cmds.parent(bind_joint, bind_jnt_grp)
        bind_joints.append(bind_joint)


    #clean a bit
    clean_ctrl_grp = cmds.group(em=True, name=name + nc['ctrl'] + nc['group'])
    clean_rig_grp = cmds.group(em=True, name=name + '_Rig' + nc['group'])

    cmds.parentConstraint(block_parent, clean_ctrl_grp, mo=True)

    cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
    cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])

    cmds.parent(granfather_ctrl_root, main_root_grp, clean_ctrl_grp)
    cmds.parent(new_guide, clean_rig_grp)


    print ('Build {} Success'.format(block))



#build_tongue_block()
