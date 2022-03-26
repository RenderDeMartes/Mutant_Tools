from maya import cmds
import json
import imp
import os
from pathlib import Path

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
imp.reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()

#---------------------------------------------

TAB_FOLDER = '03_Facial'
PYBLOCK_NAME = 'exec_skull'

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

MODULE_FILE = os.path.join(os.path.dirname(__file__),'01_Skull.json')
with open(MODULE_FILE) as module_file:
	module = json.load(module_file)


#---------------------------------------------

def create_skull_block(name = 'Skull'):

    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name = name, icon = 'Skull',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]

    upr = mt.create_joint_guide(name = name + '_Upr')
    cmds.move(0,2,0)
    lwr = mt.create_joint_guide(name = name + '_Lwr')
    cmds.move(0,0,0)

    cmds.parent(upr,lwr)
    cmds.parent(lwr,block)

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_skull_block()

#-------------------------

def build_skull_block():

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guide = cmds.listRelatives(block, c=True)[0]
    name = guide.replace('_Lwr'+nc['guide'], '')

    #use this locator in case parent is set to new locator
    if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
        block_parent = cmds.spaceLocator( n = '{}'.format(str(block).replace(nc['module'],'_Parent' + nc['locator'])))
    else:
        block_parent = cmds.getAttr('{}.SetParent'.format(config))

    ctrl_size = cmds.getAttr('{}.CtrlSize'.format(config))
    ctrl_type = cmds.getAttr('{}.CtrlType'.format(config), asString = True)
    ctrl_color = cmds.getAttr('{}.CtrlColor'.format(config), asString = True)

    #clean a bit
    clean_ctrl_grp = cmds.group(em=True, name = name + nc['ctrl'] + nc['group'])
    clean_rig_grp = cmds.group(em=True, name = name + '_Rig' + nc['group'])

    #orient the joints
    new_guide = mt.duplicate_and_remove_guides(guide)
    lower_head = cmds.listRelatives(new_guide, c=True)[0]
    cmds.parent(lower_head,  w=True)
    ctrls = []
    for jnt in [new_guide, lower_head]:
        jnt_root = mt.root_grp(input=jnt)
        ctrl = mt.curve(input=jnt,
                              type=ctrl_type,
                              rename=True,
                              custom_name=True,
                              name=jnt.replace(nc['joint'], nc['ctrl']),
                              size=ctrl_size)
        mt.assign_color(color=ctrl_color)
        ctrl_root = mt.root_grp()[0]
        mt.match(ctrl_root, jnt, r=True, t=True)
        cmds.connectAttr(ctrl+'.rotate', jnt+'.rotate')
        cmds.connectAttr(ctrl+'.translate', jnt+'.translate')
        mt.hide_attr(input=ctrl, s=True)
        cmds.parent(ctrl_root, clean_ctrl_grp)
        cmds.parent(jnt_root, clean_rig_grp)
        ctrls.append(ctrl)

    cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
    cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])

    cmds.parentConstraint(block_parent, clean_ctrl_grp)

    #Bind joints
    bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])
    for jnt in [new_guide, lower_head]:
        cmds.select(cl=True)
        bind_joint = cmds.joint(n = jnt.replace(nc['joint'], nc['joint_bind']))
        cmds.parentConstraint(jnt, bind_joint)
        cmds.setAttr('{}.radius'.format(bind_joint), 1.5)
        cmds.parent(bind_joint, bind_jnt_grp)


    #VIS
    # hide ctrls
    attrs_position = cmds.getAttr('{}.SetAttrsPosition'.format(config), asString=True)
    if attrs_position == 'new_locator':
        guide_attrs_position = cmds.spaceLocator(n=name + '_Attrs' + nc['locator'])[0]
    else:
        guide_attrs_position = attrs_position

    mt.line_attr(input=guide_attrs_position, name='Skull_Vis')
    main_ctrl_attr = mt.new_enum(input=guide_attrs_position, name='skullMainCtrls', enums='Hide:Show')
    cmds.setAttr(main_ctrl_attr, 1)
    for ctrl in ctrls:
        shape = cmds.listRelatives(ctrl, s=True)[0]
        cmds.connectAttr(main_ctrl_attr, '{}.v'.format(shape))

    print ('Build {} Success'.format(block))



#build_skull_block()
