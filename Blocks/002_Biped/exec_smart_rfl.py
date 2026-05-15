from __future__ import absolute_import
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
PYBLOCK_NAME = 'exec_smart_rfl'

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

MODULE_FILE = os.path.join(os.path.dirname(__file__), '009_Smart_RFL.json')
with open(MODULE_FILE) as module_file:
	module = json.load(module_file)

#---------------------------------------------

SMART_RFL_MODES = ('Original', 'SCL', 'SN')


def _smart_rfl_attr_exists(attr):

    if '.' not in attr:
        return False

    node, attr_name = attr.split('.', 1)
    return cmds.objExists(node) and cmds.attributeQuery(attr_name, node=node, exists=True)


def _get_smart_rfl_mode(config):

    if not cmds.attributeQuery('AltMode', node=config, exists=True):
        return 'Original'

    attr = '{}.AltMode'.format(config)
    attr_type = cmds.getAttr(attr, type=True)

    if attr_type == 'enum':
        mode = cmds.getAttr(attr, asString=True)
        if mode in SMART_RFL_MODES:
            return mode
        return 'Original'

    if attr_type == 'bool':
        return 'SCL' if cmds.getAttr(attr) else 'Original'

    value = cmds.getAttr(attr)
    if value in [True, 1, 'True']:
        return 'SCL'

    return 'Original'


def _get_smart_rfl_foot_name(config, side_guide):

    if not cmds.attributeQuery('SetFootBlockName', node=config, exists=True):
        return ''

    foot_name = cmds.getAttr('{}.SetFootBlockName'.format(config))
    if side_guide.startswith(nc['right']):
        foot_name = foot_name.replace(nc['left'], nc['right'])

    return foot_name


def _connect_smart_rfl_direct(control_attr, target_attr):

    if not _smart_rfl_attr_exists(target_attr):
        return False

    cmds.connectAttr(control_attr, target_attr, f=True)
    return True


def _connect_smart_rfl_additive(source_attr, control_attr, target_attr, name=''):

    if name:
        double_linear = mt.create_add_double_linear(name=name)
    else:
        double_linear = mt.create_add_double_linear()

    input1_attr, input2_attr, output_attr = mt.get_add_double_linear_attrs(double_linear)
    cmds.connectAttr(source_attr, '{}.{}'.format(double_linear, input1_attr), f=True)
    cmds.connectAttr(control_attr, '{}.{}'.format(double_linear, input2_attr), f=True)
    cmds.connectAttr('{}.{}'.format(double_linear, output_attr), target_attr, f=True)

    return double_linear


def _connect_original_pivot_ball(side_guide, rfl_ctrl, pivot_ball_connections):

    for connection in pivot_ball_connections:
        _connect_smart_rfl_additive('{}.PivotBall'.format(side_guide),
                                    '{}.rotateY'.format(rfl_ctrl),
                                    connection)


def _connect_sn_pivot_ball_floor(side_guide, rfl_ctrl):

    if not cmds.attributeQuery('PivotBallFloor', node=side_guide, exists=True):
        return False

    pivot_ball_floor_connections = cmds.listConnections('{}.PivotBallFloor'.format(side_guide), p=True) or []
    if not pivot_ball_floor_connections:
        return False

    for connection in pivot_ball_floor_connections:
        _connect_smart_rfl_additive('{}.PivotBallFloor'.format(side_guide),
                                    '{}.rotateY'.format(rfl_ctrl),
                                    connection)

    return True


def _connect_original_roll(name, side_guide, rfl_ctrl, roll_out_connections, roll_in_connections):

    for connection in roll_out_connections:
        out_remap_node = cmds.createNode('remapValue', name=name + '_RemapValueOut')
        cmds.connectAttr('{}.rotateZ'.format(rfl_ctrl), '{}.inputValue'.format(out_remap_node), f=True)
        cmds.setAttr('{}.inputMin'.format(out_remap_node), 0)
        cmds.setAttr('{}.inputMax'.format(out_remap_node), -180)
        cmds.setAttr('{}.outputMin'.format(out_remap_node), 0)
        cmds.setAttr('{}.outputMax'.format(out_remap_node), -180)

        _connect_smart_rfl_additive('{}.RollOut'.format(side_guide),
                                    '{}.outValue'.format(out_remap_node),
                                    connection,
                                    name=name + '_DLOut')

    for connection in roll_in_connections:
        in_remap_node = cmds.createNode('remapValue', name=name + '_RemapValueIn')
        cmds.connectAttr('{}.rotateZ'.format(rfl_ctrl), '{}.inputValue'.format(in_remap_node), f=True)
        cmds.setAttr('{}.inputMin'.format(in_remap_node), 0)
        cmds.setAttr('{}.inputMax'.format(in_remap_node), 180)
        cmds.setAttr('{}.outputMin'.format(in_remap_node), 0)
        cmds.setAttr('{}.outputMax'.format(in_remap_node), 180)

        _connect_smart_rfl_additive('{}.RollIn'.format(side_guide),
                                    '{}.outValue'.format(in_remap_node),
                                    connection,
                                    name=name + '_DLIn')

def create_smart_rfl_block(name = 'Smart_RFL'):

    nc, curve_data, setup = mt.import_configs()
    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name = name, icon = 'RFL',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]
    name = block.replace(nc['module'],'')

    #cmds.getAttr('{}.AttrName'.format(config)) #get attrs from config
    #cmds.getAttr('{}.AttrName'.format(config), asString = True) #for enums
    #joint_one = mt.create_joint_guide(name = name) #guide base with shapes

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_smart_rfl_block()

#-------------------------

def build_smart_rfl_block():

    mt.check_is_there_is_base()


    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]

    #orient the joints
    to_build = []

    attrs_pos = cmds.getAttr('{}.SetRFLAttrsPosition'.format(config))
    if cmds.attributeQuery('TransferAttrs', node=config, exists=True):
        transfer_attrs = cmds.getAttr('{}.TransferAttrs'.format(config), asString=True)
    else:
        transfer_attrs=False

    if not attrs_pos:
        return

    to_build = [attrs_pos.replace(nc['right'], nc['left']), attrs_pos.replace(nc['left'], nc['right'])]
    print(to_build)


    #build ------------------------------------------------------
    for side_guide in to_build:

        name = side_guide.replace(nc['ctrl'], '') + '_RFL'

        #use this locator in case parent is set to new locator
        #smart select the colors
        if str(side_guide).startswith(nc['left']):
            color = setup['left_color']
        elif str(side_guide).startswith(nc['right']):
            color = setup['right_color']       
        else:
            color = setup['main_color']       

        if not cmds.objExists(side_guide):
            continue

        rfl_mode = _get_smart_rfl_mode(config)
        if rfl_mode != 'Original':
            print('{} Mode is On'.format(rfl_mode))

        foot_name = ''
        if rfl_mode in ['SCL', 'SN']:
            foot_name = _get_smart_rfl_foot_name(config, side_guide)

        #main funcion -------------------------------------------

        #Create ctrl
        rfl_ctrl = mt.curve(input=side_guide,
                        type='cubePlus',
                        rename=True,
                        custom_name=True,
                        name=side_guide.replace(nc['ctrl'], '_RFL'+nc['ctrl']),
                        size=2)

        mt.assign_color(color=color)
        root_grp, auto_grp = mt.root_grp(autoRoot=True)
        mt.match(root_grp, side_guide, r=True, t=True)
        mt.hide_attr(input=rfl_ctrl, t=True, s=True, rotate_order=True)

        #Repalce connections with double linear probably
        #setAttr "L_Ankle_Ik_Ctrl.PivotBall" -29.3;
        #setAttr "L_Ankle_Ik_Ctrl.FootRoll" -42.9;
        #setAttr "L_Ankle_Ik_Ctrl.RollOut" -31.9;
        #setAttr "L_Ankle_Ik_Ctrl.RollIn" 28.7;

        #get connections of main one
        roll_out_connections = cmds.listConnections('{}.FootRoll'.format(side_guide), p=True) or []
        for c in roll_out_connections:
            _connect_smart_rfl_additive('{}.FootRoll'.format(side_guide),
                                        '{}.rotateX'.format(rfl_ctrl),
                                        c)


        pivot_ball_connections = cmds.listConnections('{}.PivotBall'.format(side_guide), p=True) or []
        if rfl_mode == 'SN':
            if not _connect_sn_pivot_ball_floor(side_guide, rfl_ctrl):
                cmds.warning('Smart RFL SN mode could not find PivotBallFloor connections on {}. Using legacy PivotBall behavior.'.format(side_guide))
                _connect_original_pivot_ball(side_guide, rfl_ctrl, pivot_ball_connections)
        else:
            _connect_original_pivot_ball(side_guide, rfl_ctrl, pivot_ball_connections)

        roll_out_connections = cmds.listConnections('{}.RollOut'.format(side_guide), p=True) or []
        roll_in_connections = cmds.listConnections('{}.RollIn'.format(side_guide), p=True) or []

        if rfl_mode == 'Original':
            _connect_original_roll(name, side_guide, rfl_ctrl, roll_out_connections, roll_in_connections)
        else:
            print(side_guide)
            scl_target = '{}_Ball_RFL_Grp_Auto_Grp.rotateX'.format(foot_name)
            if not _connect_smart_rfl_direct('{}.rotateZ'.format(rfl_ctrl), scl_target):
                cmds.warning('Smart RFL {} mode could not find {}. Using legacy roll behavior.'.format(rfl_mode, scl_target))
                _connect_original_roll(name, side_guide, rfl_ctrl, roll_out_connections, roll_in_connections)

        #clean a bit
        clean_ctrl_grp = cmds.group(em=True, name = name + nc['ctrl'] + nc['group'])

        cmds.parent(root_grp, clean_ctrl_grp)


        if str(side_guide).startswith(nc['right']):
            clean_ctrl_grp = mt.mirror_group(clean_ctrl_grp, world=True)
            #cmds.setAttr(root_grp+'.scaleX', -1)
            cmds.parentConstraint(attrs_pos.replace(nc['left'], nc['right']), root_grp, mo=False)
            cmds.scaleConstraint(attrs_pos.replace(nc['left'], nc['right']), root_grp, mo=False)
        else:
            cmds.parentConstraint(attrs_pos, root_grp, mo=True)
            cmds.scaleConstraint(attrs_pos, root_grp, mo=True)

            # Ensure mirror: wrap L side with identity Mirror_Grp for hierarchy consistency
            if cmds.optionVar(q="mutant_ensure_mirror") if cmds.optionVar(ex="mutant_ensure_mirror") else False:
                clean_ctrl_grp = mt.ensure_mirror_group(clean_ctrl_grp, world=True)

        cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])

    
        # transfer attrs from ik to smart rfl ctrl
        if transfer_attrs:
            attrs = cmds.listAttr(side_guide, ud=True)
            for attr in attrs:
                if 'RotateOrder' == attr:
                    continue
                if 'Switch_IK_FK' == attr:
                    continue
                if '__' in attr:
                    if cmds.getAttr('{}.{}'.format(side_guide, attr), asString=True) == 'Switch' :
                        continue
                    if cmds.getAttr('{}.{}'.format(side_guide, attr), asString=True) == 'Attrs' :
                        continue
                    mt.line_attr(input=rfl_ctrl, name=cmds.getAttr("{}.{}".format(side_guide, attr), asString=True))
                    cmds.setAttr('{}.{}'.format(side_guide, attr), l=True)
                    cmds.setAttr('{}.{}'.format(side_guide, attr), keyable=False, channelBox=False)
                    continue
                print(attr)
                new_attr = mt.new_attr(rfl_ctrl, name=attr, min=-999, max=999, default=cmds.getAttr('{}.{}'.format(side_guide, attr)))
                cmds.connectAttr(new_attr, '{}.{}'.format(side_guide, attr))
                cmds.setAttr('{}.{}'.format(side_guide, attr), l=True)
                cmds.setAttr('{}.{}'.format(side_guide, attr), keyable =False, channelBox=False)

    #tiny hard code fix
    try:
        # creating reverse nodes to connect to IK Switch attributes.
        L_IK_RFL_RevNode = cmds.createNode("reverse", name="L_Ankle_Ik_RFL_Reverse")
        R_IK_RFL_RevNode = cmds.createNode("reverse", name="R_Ankle_Ik_RFL_Reverse")

        # connecting reverse nodes to offset groups of RFL ctrls
        cmds.connectAttr("L_Hip_Jnt_Switch_Loc.Switch_IK_FK", "{}.inputX".format(L_IK_RFL_RevNode), force=True)
        cmds.connectAttr("{}.output.outputX".format(L_IK_RFL_RevNode), "L_Ankle_Ik_RFL_Ctrl_Grp.visibility", force=True)

        cmds.connectAttr("R_Hip_Jnt_Switch_Loc.Switch_IK_FK", "{}.inputX".format(R_IK_RFL_RevNode), force=True)
        cmds.connectAttr("{}.output.outputX".format(R_IK_RFL_RevNode), "R_Ankle_Ik_RFL_Ctrl_GrpMirror_Grp.visibility",
                         force=True)
    except:
        pass




    # build complete ----------------------------------------------------
    print ('Build {} Success'.format(block))




#build_smart_rfl_block()
