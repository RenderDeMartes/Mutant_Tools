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
PYBLOCK_NAME = 'exec_nose'

#Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-2]
FOLDER=''
for f in PATH_PARTS:
	FOLDER = os.path.join(FOLDER, f)

#---------------------------------------------

def create_nose_block(name = 'Nose'):

    # Read name conventions as nc[''] and setup as seup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-2]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '005_Nose.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()
    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name = name, icon = 'Nose',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]
      
    nose_start = mt.create_joint_guide(name = name + '_Origin')
    cmds.move(0,5,-4)
    nose_a = mt.create_joint_guide(name = name + '_Bridge')
    cmds.move(0,3.5,-1.5)
    cmds.parent(nose_a, nose_start)
    nose_b = mt.create_joint_guide(name = name + '_Base')
    cmds.move(0,1.75,0.5)
    cmds.parent(nose_b, nose_a)
    nose_c = mt.create_joint_guide(name = name + '_Tip')
    cmds.move(0,0,3.5)
    cmds.parent(nose_c, nose_b)
    l_nostril = mt.create_joint_guide(name = nc['left'] + name + 'Nostril')
    cmds.move(2,1,3)
    cmds.parent(l_nostril, nose_b)
    l_nostril_end = mt.create_joint_guide(name = nc['left'] + name + 'NostrilEnd')
    cmds.move(3.5,1,3)
    cmds.parent(l_nostril_end, l_nostril)
    r_nostril = mt.create_joint_guide(name = nc['right'] + name + 'Nostril')
    cmds.move(-2,1,3)
    cmds.parent(r_nostril, nose_b)
    r_nostril_end = mt.create_joint_guide(name = nc['right'] + name + 'NostrilEnd')
    cmds.move(-3.5,1,3)
    cmds.parent(r_nostril_end, r_nostril)
    top_nose = mt.create_joint_guide(name = name + '_Top')
    cmds.move(0,3,3)
    cmds.parent(top_nose, nose_b)

    cmds.parent(nose_start, block)

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_nose_block()

#-------------------------

def build_nose_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guide = cmds.listRelatives(block, c=True)[0]
    name = block.replace(nc['module'], '')

    #use this locator in case parent is set to new locator
    if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
        block_parent = cmds.spaceLocator( n = '{}'.format(str(block).replace(nc['module'],'_Parent' + nc['locator'])))
    else:
        block_parent = cmds.getAttr('{}.SetParent'.format(config))

    ctrl_size = cmds.getAttr('{}.CtrlSize'.format(config))

    new_guide = mt.duplicate_and_remove_guides(guide)
    #mt.orient_joint(new_guide)

    #Build Nose
    nose_joints = cmds.listRelatives(new_guide, ad=True)
    all_joints = [nose_joints[0],nose_joints[1],nose_joints[2],nose_joints[3],
                  nose_joints[4],nose_joints[5],nose_joints[6],nose_joints[7],
                  new_guide]

    all_joints = cmds.listRelatives(new_guide, c=True, ad=True)
    all_joints.insert(0, new_guide)
    # Reorder to match desire order
    # ['Nose_Origin_Jnt', 'Nose_Tip_Jnt', 'L_NoseNostrilEnd_Jnt', 'L_NoseNostril_Jnt', 'R_NoseNostrilEnd_Jnt',
     # 'R_NoseNostril_Jnt', 'Nose_Top_Jnt', 'Nose_Base_Jnt', 'Nose_Bridge_Jnt']
    order_keys = {0: 'Origin' + nc['joint'],
                  1: 'Tip' + nc['joint'],
                  2: nc['left'] + name + 'Nostril' + nc['joint'],
                  3: nc['left'] + name + 'NostrilEnd' + nc['joint'],
                  4: nc['right'] + name + 'Nostril' + nc['joint'],
                  5: nc['right'] + name + 'NostrilEnd' + nc['joint'],
                  6: 'Top' + nc['joint'],
                  7: 'Base' + nc['joint'],
                  8: 'Bridge' + nc['joint']
                  }
    ordered_joints = []
    for key in order_keys:
        for jnt in all_joints:
            if order_keys[key] in jnt:
                ordered_joints.append(jnt)

    #set names for easy use
    origin = ordered_joints[0]
    bridge = ordered_joints[8]
    base = ordered_joints[7]
    tip = ordered_joints[1]
    l_nostril = ordered_joints[2]
    l_nostril_end = ordered_joints[3]
    r_nostril = ordered_joints[4]
    r_nostril_end = ordered_joints[5]
    top = ordered_joints[6]

    #reparent_hardcoded:
    for jnt in ordered_joints:
        try:cmds.parent(jnt, w=True)
        except:pass

    cmds.parent(bridge, origin)
    cmds.parent(base, bridge)
    cmds.parent(tip, base)
    cmds.parent(l_nostril_end, l_nostril)
    cmds.parent(l_nostril, base)
    cmds.parent(r_nostril_end, r_nostril)
    cmds.parent(r_nostril, base)
    cmds.parent(top, base)

    #Build the nose
    cmds.select(origin, bridge)
    nose_fk = mt.fk_chain(curve_type='cube', direct_connect=True)
    origin_ctrl = nose_fk[0]
    bridge_ctrl = nose_fk[1]
    cmds.select(base)
    base_ctrl = mt.fk_chain(curve_type='cube', direct_connect=True)
    cmds.select(tip)
    tip_ctrl = mt.fk_chain(curve_type='cube', direct_connect=True)
    cmds.select(top)
    top_ctrl = mt.fk_chain(curve_type='sphere', direct_connect=True)
    cmds.select(l_nostril)
    l_nostril_ctrl = mt.fk_chain(curve_type='circleY', direct_connect=True)
    cmds.select(l_nostril_end)
    l_nostril_end_ctrl = mt.fk_chain(curve_type='sphere', direct_connect=True)
    cmds.select(r_nostril)
    r_nostril_ctrl = mt.fk_chain(curve_type='circleY', direct_connect=True)
    cmds.select(r_nostril_end)
    r_nostril_end_ctrl = mt.fk_chain(curve_type='sphere', direct_connect=True)

    #mirror behavior
    #r_nostril_mirror = mt.mirror_group(cmds.listRelatives(r_nostril_ctrl, p=True)[0], world=False)
    #r_nostril_end_mirror= mt.mirror_group(cmds.listRelatives(r_nostril_end_ctrl, p=True)[0], world=False)

    #create hierarchy
    cmds.parent(cmds.listRelatives(tip_ctrl, p=True)[0], base_ctrl)
    cmds.parent(cmds.listRelatives(top_ctrl, p=True)[0], base_ctrl)
    cmds.parent(cmds.listRelatives(l_nostril_end_ctrl, p=True)[0], l_nostril_ctrl)
    cmds.parent(cmds.listRelatives(l_nostril_ctrl, p=True)[0], base_ctrl)
    # cmds.parent(r_nostril_end_mirror, r_nostril_ctrl)
    # cmds.parent(r_nostril_mirror, base_ctrl)
    cmds.parent(cmds.listRelatives(base_ctrl, p=True)[0], bridge_ctrl)
    cmds.parent(cmds.listRelatives(r_nostril_ctrl, p=True)[0], base_ctrl)
    cmds.parent(cmds.listRelatives(r_nostril_end_ctrl, p=True)[0], r_nostril_ctrl)


    #Bind joints
    bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])
    bind_joints = []
    for jnt in all_joints:
        cmds.select(cl=True)
        bind_joint = cmds.joint(n=jnt.replace(nc['joint'], nc['joint_bind']))
        cmds.parentConstraint(jnt, bind_joint)
        cmds.setAttr('{}.radius'.format(bind_joint), 1.5)
        cmds.parent(bind_joint, bind_jnt_grp)
        bind_joints.append(bind_joint)

    #hardcoded joints i dont have time sorry :)
    cmds.parent(bind_joints[8], bind_joints[0]) #bridge-origin
    cmds.parent(bind_joints[7], bind_joints[8]) #base - bridge
    cmds.parent(bind_joints[1], bind_joints[7]) #tip - base
    cmds.parent(bind_joints[6], bind_joints[7]) #top - base
    
    cmds.parent(bind_joints[3], bind_joints[7]) #L_nostril - base
    cmds.parent(bind_joints[5], bind_joints[7]) #R_nostril - base

    cmds.parent(bind_joints[2], bind_joints[3]) #L_nostril_end - L_nostril
    cmds.parent(bind_joints[4], bind_joints[5]) #R_nostril_end - R_nostril

    cmds.showHidden(bind_joints[4])

    #['Nose_Tip_Bnd', 'L_NoseNostrilEnd_Bnd', 'L_NoseNostril_Bnd',
    # 'R_NoseNostrilEnd_Bnd', 'R_NoseNostril_Bnd'
    # , 'Nose_Top_Bnd', 'Nose_Base_Bnd', 'Nose_Bridge_Bnd', 'Nose_Origin_Bnd']

    cmds.parentConstraint(block_parent, cmds.listRelatives(origin_ctrl, p=True)[0],mo=True)

    #Clean
    clean_ctrl_grp = cmds.group(em=True, name = name + nc['ctrl'] + nc['group'])
    clean_rig_grp = cmds.group(em=True, name = name + '_Rig' + nc['group'])

    cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
    cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])

    cmds.parent(cmds.listRelatives(origin_ctrl, p=True)[0], clean_ctrl_grp)
    cmds.parent(cmds.listRelatives(cmds.listRelatives(new_guide, p=True)[0], p=True)[0], clean_rig_grp)

    #vis
    attrs_position = cmds.getAttr('{}.SetAttrsPosition'.format(config), asString=True)

    if attrs_position == 'new_locator':
        guide_attrs_position = cmds.spaceLocator(n=name + '_Attrs' + nc['locator'])[0]
    else:
        guide_attrs_position = attrs_position

    mt.line_attr(input=guide_attrs_position, name='Nose_Vis')
    main_ctrl_attr = mt.new_enum(input=guide_attrs_position, name='noseMainCtrls', enums='Hide:Show', keyable=False)
    mid_ctrl_attr = mt.new_enum(input=guide_attrs_position, name='noseMidCtrls', enums='Hide:Show', keyable=False)
    show_tweeks_attr = mt.new_enum(input=guide_attrs_position, name='noseTweekCtrls', enums='Hide:Show', keyable=False)

    cmds.setAttr(main_ctrl_attr, 1)

    if guide_attrs_position != base_ctrl:
        for ctrl in [base_ctrl]:
            shape = cmds.listRelatives(ctrl, s=True)[0]
            cmds.connectAttr(main_ctrl_attr, '{}.v'.format(shape))
    for ctrl in [top_ctrl, l_nostril_ctrl, r_nostril_ctrl]:
        shape = cmds.listRelatives(ctrl, s=True)[0]
        cmds.connectAttr(mid_ctrl_attr, '{}.v'.format(shape))
    for ctrl in [origin_ctrl, bridge_ctrl, tip_ctrl, r_nostril_end_ctrl, l_nostril_end_ctrl]:
        shape = cmds.listRelatives(ctrl, s=True)[0]
        cmds.connectAttr(show_tweeks_attr, '{}.v'.format(shape))

    print(bind_joints)