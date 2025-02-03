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

        # Alt Mode
        if cmds.attributeQuery("AltMode", n=config, ex=True):
            alt_mode = cmds.getAttr("{}.AltMode".format(config))
            if alt_mode:
                print('Alt Mode is On')
        else:
            alt_mode = False

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
        roll_out_connections = cmds.listConnections('{}.FootRoll'.format(side_guide), p=True)
        for c in roll_out_connections:
            double_linear = cmds.shadingNode('addDoubleLinear', asUtility=True)
            cmds.connectAttr('{}.FootRoll'.format(side_guide), '{}.input1'.format(double_linear), f=True)
            cmds.connectAttr('{}.rotateX'.format(rfl_ctrl), '{}.input2'.format(double_linear), f=True)
            cmds.connectAttr('{}.output'.format(double_linear), c, f=True)


        pivot_ball_connections = cmds.listConnections('{}.PivotBall'.format(side_guide), p=True)
        for c in pivot_ball_connections:
            double_linear = cmds.shadingNode('addDoubleLinear', asUtility=True)
            cmds.connectAttr('{}.PivotBall'.format(side_guide), '{}.input1'.format(double_linear), f=True)
            cmds.connectAttr('{}.rotateY'.format(rfl_ctrl), '{}.input2'.format(double_linear), f=True)
            cmds.connectAttr('{}.output'.format(double_linear), c, f=True)

        roll_out_connections = cmds.listConnections('{}.RollOut'.format(side_guide), p=True)
        roll_in_connections = cmds.listConnections('{}.RollIn'.format(side_guide), p=True)

        for c in roll_out_connections:
            if not alt_mode:
                out_remap_node = cmds.createNode('remapValue', name=name + '_RemapValueOut')
                cmds.connectAttr('{}.rotateZ'.format(rfl_ctrl), '{}.inputValue'.format(out_remap_node), f=True)
                cmds.setAttr('{}.inputMin'.format(out_remap_node), 0)
                cmds.setAttr('{}.inputMax'.format(out_remap_node), -180)
                cmds.setAttr('{}.outputMin'.format(out_remap_node), 0)
                cmds.setAttr('{}.outputMax'.format(out_remap_node), -180)

                double_linear = cmds.shadingNode('addDoubleLinear', asUtility=True, name=name + '_DLOut')
                cmds.connectAttr('{}.RollOut'.format(side_guide), '{}.input1'.format(double_linear), f=True)
                cmds.connectAttr('{}.outValue'.format(out_remap_node), '{}.input2'.format(double_linear), f=True)
                cmds.connectAttr('{}.output'.format(double_linear), c, f=True)

        roll_in_connections = cmds.listConnections('{}.RollIn'.format(side_guide), p=True)
        for c in roll_in_connections:
            if not alt_mode:
                in_remap_node = cmds.createNode('remapValue', name=name + '_RemapValueIn')
                cmds.connectAttr('{}.rotateZ'.format(rfl_ctrl), '{}.inputValue'.format(in_remap_node), f=True)
                cmds.setAttr('{}.inputMin'.format(in_remap_node), 0)
                cmds.setAttr('{}.inputMax'.format(in_remap_node), 180)
                cmds.setAttr('{}.outputMin'.format(in_remap_node), 0)
                cmds.setAttr('{}.outputMax'.format(in_remap_node), 180)

                double_linear = cmds.shadingNode('addDoubleLinear', asUtility=True, name=name + '_DLIn')
                cmds.connectAttr('{}.RollIn'.format(side_guide), '{}.input1'.format(double_linear), f=True)
                cmds.connectAttr('{}.outValue'.format(in_remap_node), '{}.input2'.format(double_linear), f=True)
                cmds.connectAttr('{}.output'.format(double_linear), c, f=True)
                #L_Foot_In_RFL_Grp_Auto_Grp.rotateZ

        if alt_mode:
            print(side_guide)
            foot_name = cmds.getAttr("{}.SetFootBlockName".format(config))
            if side_guide.startswith(nc['right']):
                foot_name = foot_name.replace(nc['left'], nc['right'])
            cmds.connectAttr('{}.rotateZ'.format(rfl_ctrl), '{}_Ball_RFL_Grp_Auto_Grp.rotateX'.format(foot_name), f=True)

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
