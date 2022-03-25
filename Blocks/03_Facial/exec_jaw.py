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
PYBLOCK_NAME = 'exec_jaw'

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

MODULE_FILE = os.path.join(os.path.dirname(__file__),'02_Jaw.json')
with open(MODULE_FILE) as module_file:
	module = json.load(module_file)



#---------------------------------------------

def create_jaw_block(name = 'Jaw'):

    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name = name, icon = 'Jaw',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]
      
    jaw_start = mt.create_joint_guide(name = name)
    cmds.move(0,3,0)
    jaw_upper_lip = mt.create_joint_guide(name = name + 'UpperLip')
    cmds.move(0,1.5,3)
    jaw_lower_lip = mt.create_joint_guide(name = name + 'LowerLip')
    cmds.move(0,1.4,3)

    cmds.parent(jaw_upper_lip, jaw_start)
    cmds.parent(jaw_lower_lip, jaw_start)

    cmds.parent(jaw_start, block)

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_jaw_block()

#-------------------------

def build_jaw_block():
    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guide = cmds.listRelatives(block, c=True)[0]
    name = guide.replace(nc['guide'], '')

    #use this locator in case parent is set to new locator
    if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
        block_parent = cmds.spaceLocator( n = '{}'.format(str(block).replace(nc['module'],'_Parent' + nc['locator'])))
    else:
        block_parent = cmds.getAttr('{}.SetParent'.format(config))

    ctrl_size = cmds.getAttr('{}.CtrlSize'.format(config))
    ctrl_type = cmds.getAttr('{}.CtrlType'.format(config), asString = True)

    new_guide = mt.duplicate_and_remove_guides(guide)
    mt.orient_joint(input=new_guide)
    jaw_joints = [new_guide] + cmds.listRelatives(new_guide, ad=True, type='joint')
    print(jaw_joints)
    jaw_pivot_joint = jaw_joints[0]
    upper_lip = jaw_joints[1]
    lower_lip = jaw_joints[2]

    jaw_jnt_root = mt.root_grp(input=jaw_pivot_joint)
    jaw_jnt_mover = cmds.group(em=True, n =jaw_pivot_joint.replace(nc['joint'], 'Mover'+nc['group']))
    cmds.delete(cmds.pointConstraint(jaw_jnt_root, jaw_jnt_mover))
    cmds.parent(jaw_jnt_mover, jaw_jnt_root)
    cmds.parent(jaw_pivot_joint, jaw_jnt_mover)

    cmds.select(cl=True)
    upper_pivot_joint = cmds.joint(n =  name +'UpperLipPivot' + nc['joint'])
    cmds.delete(cmds.parentConstraint(jaw_jnt_root, upper_pivot_joint))
    cmds.parent(upper_lip, upper_pivot_joint)
    mt.orient_joint(input=upper_pivot_joint)

    global_locator = cmds.spaceLocator(n=name + 'Global' + nc['locator'])[0]
    global_locator_root = mt.root_grp()
    cmds.delete(cmds.parentConstraint(jaw_pivot_joint, global_locator_root))
    cmds.parentConstraint(global_locator, upper_pivot_joint)
    cmds.parentConstraint(global_locator, jaw_jnt_root)

    #Jaw controller
    jaw_ctrl = mt.curve(input=global_locator,
                          type=ctrl_type,
                          rename=True,
                          custom_name=True,
                          name=name + nc['ctrl'],
                          size=ctrl_size)
    mt.assign_color(color='green')
    jaw_ctrl_root = mt.root_grp()[0]
    cmds.connectAttr(jaw_ctrl+'.rotate', global_locator+'.rotate')
    cmds.connectAttr('{}.translate'.format(jaw_ctrl), '{}.translate'.format(jaw_jnt_mover))

    up_limit = mt.new_attr(input=jaw_ctrl, name='UpperLipBreak', min=0, max=90, default=5)
    side_limits = mt.new_attr(input=jaw_ctrl, name='SideBreaks', min=0, max=90, default=5)

    cmds.transformLimits(upper_pivot_joint, erz=[True, False],ery=[True, True], erx=[True, True], rx=[0,0])
    mt.connect_md_node(in_x1=up_limit, in_x2=-1, out_x=upper_pivot_joint+'.minRotLimit.minRotZLimit', mode='multiply')
    mt.connect_md_node(in_x1=side_limits, in_x2=-1, out_x=upper_pivot_joint+'.minRotLimit.minRotYLimit', mode='multiply')
    mt.connect_md_node(in_x1=side_limits, in_x2=1, out_x=upper_pivot_joint+'.maxRotLimit.maxRotYLimit', mode='multiply')

    mt.hide_attr(input=jaw_ctrl, s=True)


    #Bind joints
    bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])
    for jnt in [jaw_pivot_joint, upper_pivot_joint]:
        cmds.select(cl=True)
        bind_joint = cmds.joint(n = jnt.replace(nc['joint'], nc['joint_bind']))
        cmds.parentConstraint(jnt, bind_joint)
        cmds.setAttr('{}.radius'.format(bind_joint), 1.5)
        cmds.parent(bind_joint, bind_jnt_grp)


    #Parent system
    cmds.parentConstraint(block_parent, jaw_ctrl_root, mo=True)

    #Clean
    clean_ctrl_grp = cmds.group(em=True, name = name + nc['ctrl'] + nc['group'])
    clean_rig_grp = cmds.group(em=True, name = name + '_Rig' + nc['group'])

    cmds.parent(jaw_ctrl_root, clean_ctrl_grp)
    cmds.parent(jaw_jnt_root, upper_pivot_joint, global_locator_root, clean_rig_grp)

    cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
    cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])

    #VIS
    # hide ctrls
    attrs_position = cmds.getAttr('{}.SetAttrsPosition'.format(config), asString=True)
    if attrs_position == 'new_locator':
        guide_attrs_position = cmds.spaceLocator(n=name + '_Attrs' + nc['locator'])[0]

    mt.line_attr(input=guide_attrs_position, name='Jaw_Vis')
    main_ctrl_attr = mt.new_enum(input=guide_attrs_position, name='jawMainCtrls', enums='Hide:Show')
    cmds.setAttr(main_ctrl_attr, 1)
    for ctrl in [jaw_ctrl]:
        shape = cmds.listRelatives(ctrl, s=True)[0]
        cmds.connectAttr(main_ctrl_attr, '{}.v'.format(shape))