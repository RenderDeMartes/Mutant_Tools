from __future__ import absolute_import
from maya import cmds
import json

try:
    import importlib;
    from importlib import reload
except:
    import imp;
    from imp import reload

import os
from pathlib import Path

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant

reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()

# ---------------------------------------------

TAB_FOLDER = '003_Facial'
PYBLOCK_NAME = 'exec_teeth'


# ---------------------------------------------

def create_teeth_block(name='Teeth'):
    # Read name conventions as nc[''] and setup as seup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-2]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '011_Teeth.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()
    # name checks and block creation
    name = mt.ask_name(text=module['Name'])
    if cmds.objExists('{}{}'.format(name, nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name=name, icon='Teeth', attrs=module['attrs'], build_command=module['build_command'],
                            import_command=module['import'])
    config = block[1]
    block = block[0]

    # cmds.getAttr('{}.AttrName'.format(config)) #get attrs from config
    # cmds.getAttr('{}.AttrName'.format(config), asString = True) #for enums
    upr = mt.create_joint_guide(name=name + '_Upr')
    cmds.move(0, 1, 0)
    lwr = mt.create_joint_guide(name=name + '_Lwr')
    cmds.parent(upr, block)
    cmds.parent(lwr, block)

    cmds.select(block)

    print('{} Created Successfully'.format(name))


# create_teeth_block()

# -------------------------

def build_teeth_block():
    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    upr_guide = cmds.listRelatives(block, c=True)[0]
    lwr_guide = cmds.listRelatives(block, c=True)[1]
    name = block.replace(nc['module'], '')

    # groups for later cleaning
    clean_rig_grp = ''
    clean_ctrl_grp = ''

    # use this locator in case parent is set to new locator
    if cmds.getAttr('{}.SetUprParent'.format(config)) == 'new_locator':
        upr_block_parent = cmds.spaceLocator(
            n='{}'.format(str(block).replace(nc['module'], '_UprParent' + nc['locator'])))
    else:
        upr_block_parent = cmds.getAttr('{}.SetUprParent'.format(config))

    if cmds.getAttr('{}.SetLwrParent'.format(config)) == 'new_locator':
        lwr_block_parent = cmds.spaceLocator(
            n='{}'.format(str(block).replace(nc['module'], '_LwrParent' + nc['locator'])))
    else:
        lwr_block_parent = cmds.getAttr('{}.SetLwrParent'.format(config))

    ctrl_size = cmds.getAttr('{}.CtrlSize'.format(config))
    do_upr = cmds.getAttr('{}.UprTeeth'.format(config))
    do_lwr = cmds.getAttr('{}.LwrTeeth'.format(config))

    to_buid = []
    if do_upr:
        upr_jnt = mt.duplicate_and_remove_guides(upr_guide)
        to_buid.append(upr_jnt)
    if do_lwr:
        lwr_jnt = mt.duplicate_and_remove_guides(lwr_guide)
        to_buid.append(lwr_jnt)
    if not to_buid:
        return

    ctrls = []
    ctrls_root = []
    jnt_roots = []

    attrs_position = cmds.getAttr('{}.SetAttrsPosition'.format(config), asString=True)
    if attrs_position == 'new_locator':
        guide_attrs_position = cmds.spaceLocator(n=name + '_Attrs' + nc['locator'])[0]
    else:
        guide_attrs_position = attrs_position
    mt.line_attr(input=guide_attrs_position, name='Mouth_Vis')
    vis_attrs = mt.new_enum(input=guide_attrs_position, name='{}Vis'.format(name), enums='Hide:Show', keyable=False)

    for jnt in to_buid:
        cmds.select(jnt)
        jnt_root = mt.root_grp()[0]
        ctrl = mt.curve(input=jnt,
                        type='cube',
                        rename=True,
                        custom_name=True,
                        name=jnt.replace(nc['joint'], nc['ctrl']),
                        size=ctrl_size)
        mt.assign_color(color='purple')
        ctrl_root = mt.root_grp()[0]
        cmds.connectAttr('{}.translate'.format(ctrl), '{}.translate'.format(jnt))
        cmds.connectAttr('{}.scale'.format(ctrl), '{}.scale'.format(jnt))
        cmds.connectAttr('{}.rotate'.format(ctrl), '{}.rotate'.format(jnt))
        cmds.connectAttr(vis_attrs, cmds.listRelatives(ctrl, s=True)[0] + '.v')

        ctrls.append(ctrl)
        ctrls_root.append(ctrl_root)
        jnt_roots.append(jnt_root)

    # Add parent to lower theet
    if cmds.attributeQuery('SetJawJnt', n=config, exists=True):
        jaw_jnt = cmds.getAttr('{}.SetJawJnt'.format(config))
    else:
        jaw_jnt = 'JawLowerLip_Jnt'

    # cmds.parentConstraint(jaw_jnt, jnt_roots[1], mo=True)

    bind_joints = []
    bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])

    for jnt in to_buid:
        cmds.select(cl=True)
        bind_joint = cmds.joint(n=jnt.replace(nc['joint'], nc['joint_bind']))
        cmds.parentConstraint(jnt, bind_joint)
        cmds.scaleConstraint(jnt, bind_joint)
        cmds.setAttr('{}.radius'.format(bind_joint), 1.5)
        cmds.parent(bind_joint, bind_jnt_grp)
        bind_joints.append(bind_joint)

    # clean a bit
    clean_ctrl_grp = cmds.group(em=True, name=name + nc['ctrl'] + nc['group'])
    clean_rig_grp = cmds.group(em=True, name=name + '_Rig' + nc['group'])

    # cmds.parentConstraint(block_parent, clean_ctrl_grp)
    cmds.parentConstraint(upr_block_parent, cmds.listRelatives(ctrls[0], p=True), mo=True)
    cmds.parentConstraint(lwr_block_parent, cmds.listRelatives(ctrls[1], p=True), mo=True)

    cmds.parentConstraint(upr_block_parent, jnt_roots[0], mo=True)
    cmds.parentConstraint(lwr_block_parent, jnt_roots[1], mo=True)
    cmds.scaleConstraint(upr_block_parent, jnt_roots[0], mo=True)
    cmds.scaleConstraint(lwr_block_parent, jnt_roots[1], mo=True)

    cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
    cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])

    cmds.parent(ctrls_root, clean_ctrl_grp)
    cmds.parent(jnt_roots, clean_rig_grp)

    print('Build {} Success'.format(block))

# build_teeth_block()
