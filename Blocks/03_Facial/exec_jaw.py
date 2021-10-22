from maya import cmds
import json
import imp
import os

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
PATH = PATH.replace('/Blocks//{}'.format(TAB_FOLDER), '//Config') #change this path depending of the folder

JSON_FILE = (PATH + '/name_conventions.json')
with open(JSON_FILE) as json_file:
	nc = json.load(json_file)
#Read curve shapes info
CURVE_FILE = (PATH + '/curves.json')
with open(CURVE_FILE) as curve_file:
	curve_data = json.load(curve_file)
#setup File
SETUP_FILE = (PATH+'/rig_setup.json')
with open(SETUP_FILE) as setup_file:
	setup = json.load(setup_file)	

MODULE_FILE = (os.path.dirname(__file__) +'/02_Jaw.json')
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
    jaw_tp = mt.create_joint_guide(name = nc["up"] + name)
    cmds.move(0,1.5,3)
    jaw_bt = mt.create_joint_guide(name = nc["down"] + name)
    cmds.move(0,1.4,3)
    jaw_lf = mt.create_joint_guide(name=nc["left"] + name)
    cmds.move(1.5, 1.8, 3)
    jaw_rt = mt.create_joint_guide(name=nc["right"] + name)
    
    #connect left and right side
    uc_lfrt_guides = cmds.shadingNode('unitConversion', au=1, n=name + nc["unitConversion"])
    cmds.setAttr(uc_lfrt_guides + '.conversionFactor', -1)
    cmds.connectAttr(jaw_lf + '.tx', uc_lfrt_guides + '.input')
    cmds.connectAttr(uc_lfrt_guides + '.output', jaw_rt + '.tx')
    cmds.connectAttr(jaw_lf + '.ty', jaw_rt + '.ty')
    cmds.connectAttr(jaw_lf + '.tz', jaw_rt + '.tz')

    cmds.parent(jaw_tp, jaw_lf, jaw_rt, jaw_start)
    cmds.parent(jaw_bt, jaw_tp)

    cmds.hide(jaw_bt, jaw_rt)
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

    ctrl_size = cmds.getAttr('{}.CtrlSize'.format(config))
    ctrl_type = cmds.getAttr('{}.CtrlType'.format(config), asString = True)

    jnts_name = [name, nc['up'] + name, nc['down'] + name, nc['left'] + name, nc['right'] + name]

    #SPECIFIC NAMES
    jaw_jnt = name + nc['joint']
    no_jnt = name + nc['no_joint']
    base_joint = name + nc['base_joint']

    #CREATE A JOINT FOR EVERY GUIDE
    cmds.select(cl=1)
    for i in jnts_name:
        cmds.joint(n=i + nc['joint'])
        cmds.select(cl=1)

    # CREATE A EXTRA JOINT FOR LIPS/JAWS
    jawNoJnt = cmds.joint(n=no_jnt)

    for i in jnts_name:
        cmds.select(cl=1)
        newJaw = cmds.duplicate(jaw_jnt)[0]
        new_base_joint = cmds.rename(newJaw, i + nc['base_joint'])
        cmds.parent(i + nc['joint'], new_base_joint)

    # PLACE JOINTS IN GUIDES POS
    for i in range(len(jnts_name)):
        position = cmds.xform(jnts_name[i] + nc['guide'], q=1, ws=1, t=1)
        if i == 0:
            cmds.select(jnts_name[i] + nc['no_joint'])
            cmds.xform(ws=1, t=position)
            cmds.select(jnts_name[i] + nc['base_joint'])
            cmds.xform(ws=1, t=position)
        cmds.select(jnts_name[i] + nc['joint'])
        cmds.xform(ws=1, t=position)

    cmds.select(jaw_jnt)
    cmds.xform(os=1, t=(0,0,0))

    # JAW CTL
    jaw_ctrl = mt.curve(input = name, type = ctrl_type, size = ctrl_size)
    mt.assign_color(input = jaw_ctrl, color = setup['center_color'])
    sdk = mt.root_grp(custom = True, custom_name = '_sdk')
    sdk = cmds.rename(jaw_ctrl + '_Sdk')
    grp = mt.root_grp(input=sdk)
    grp = cmds.rename(jaw_ctrl + '_Grp')

    # ATTRS JAW CTL
    cmds.addAttr(jaw_ctrl, ln='jawOpen', k=1, h=0)
    cmds.addAttr(jaw_ctrl, ln='chew', k=1, h=0, min=0, max=1)
    cmds.addAttr(jaw_ctrl, ln='chewHeight', k=1, h=0, min=-1, max=1)
    cmds.addAttr(jaw_ctrl, ln='L_Corner', k=1, h=0, min=-1, max=1)
    cmds.addAttr(jaw_ctrl, ln='R_Corner', k=1, h=0, min=-1, max=1)

    # ATTRS JAW SDK
    cmds.addAttr(sdk, ln='TY', k=1, h=0, dv= -.2)
    cmds.addAttr(sdk, ln='TZ', k=1, h=0, dv= .1)
    cmds.addAttr(sdk, ln='RX', k=1, h=0, dv= 25)

    # REHIERARCHY WITH JAW CTL
    cmds.parent(base_joint, jaw_ctrl)
    cmds.parent(no_jnt, grp)
    
    # CONSTRAINTS
    for i in jnts_name:
        if i == name:
            pass
        else:
            cons = cmds.parentConstraint(no_jnt, jaw_jnt, i + nc['base_joint'])[0]
            cmds.addAttr(cons, ln='switch', k=1, h=0, min=0, max=1)
            reverse = cmds.shadingNode('reverse', au=1, n=cons + nc['reverse'])
            cmds.connectAttr(cons + '.switch', reverse + '.inputX')
            cmds.connectAttr(reverse + '.outputX', cons + '.' + jaw_jnt + 'W1')
            cmds.connectAttr(cons + '.switch', cons + '.' + no_jnt + 'W0')

    # MULTIPLY DIVIDE TO CONTROL OPEN JAW POSITION
    md_open_jaw = cmds.shadingNode('multiplyDivide', au=True, n= name + '_open' + nc["multiplyDivide"])

    #CONNECT JAW ATTRIBUTES
    # DRIVEN KEYS JAW OPEN
    jaw_sdk = [md_open_jaw + '.input1X', md_open_jaw + '.input1Y', md_open_jaw + '.input1Z']

    for i in jaw_sdk:
        cmds.setDrivenKeyframe(i, cd=jaw_ctrl + '.jawOpen', itt='spline', ott='spline' )

    cmds.setAttr(jaw_ctrl + '.jawOpen', 1)
    cmds.setAttr(md_open_jaw + '.input1.input1X', 1)
    cmds.setAttr(md_open_jaw + '.input1.input1Y', 1)
    cmds.setAttr(md_open_jaw + '.input1.input1Z', 1)

    for i in jaw_sdk:
        cmds.setDrivenKeyframe(i, cd=jaw_ctrl + '.jawOpen', itt='spline', ott='spline' )

    cmds.selectKey(md_open_jaw, attribute='input1X')
    cmds.setInfinity( pri='linear', poi='linear' )
    cmds.selectKey(md_open_jaw, attribute='input1Y')
    cmds.setInfinity( pri='linear', poi='linear' )
    cmds.selectKey(md_open_jaw, attribute='input1Z')
    cmds.setInfinity( pri='linear', poi='linear' )

    cmds.setAttr(jaw_ctrl + '.jawOpen', 0)

    # CONNECT TO DRIVEN KEYS TO SDK
    cmds.connectAttr(md_open_jaw + '.outputX', sdk + '.ty')
    cmds.connectAttr(md_open_jaw + '.outputY', sdk + '.tz')
    cmds.connectAttr(md_open_jaw + '.outputZ', sdk + '.rx')

    cmds.connectAttr(sdk + '.TY', md_open_jaw + '.input2X')
    cmds.connectAttr(sdk + '.TZ', md_open_jaw + '.input2Y')
    cmds.connectAttr(sdk + '.RX', md_open_jaw + '.input2Z')

    # CONDITION NODE
    condition = cmds.shadingNode('condition', au=1, n=name + '_Open' + nc["condition"])
    cmds.connectAttr(jaw_ctrl + '.chew', condition + '.colorIfTrueR')
    cmds.connectAttr(jaw_ctrl + '.jawOpen', condition + '.firstTerm')
    cmds.setAttr(condition + '.operation', 3)

    # REMAP VALUES
    attributes_remap = ['chewHeight', 'L_Corner', 'R_Corner']

    for i in attributes_remap:
        rv = cmds.shadingNode('remapValue', au=1, n=name + '_' + i + nc['remap_value'])
        cmds.connectAttr(jaw_ctrl + '.' + i, rv + '.inputValue')
        cmds.setAttr(rv + '.inputMin', -1)

    # BLEND COLORS
    bs_corners = cmds.shadingNode('blendColors', au=1, n=name + '_LfRt' + nc['blend'])
    cmds.connectAttr(condition + '.outColorR', bs_corners + '.blender')
    cmds.connectAttr(name + '_chewHeight{}.outValue'.format( nc['remap_value']), bs_corners + '.color1R')
    cmds.connectAttr(name + '_chewHeight{}.outValue'.format( nc['remap_value']), bs_corners + '.color1G')
    cmds.connectAttr(name + '_L_Corner{}.outValue'.format( nc['remap_value']), bs_corners + '.color2R')
    cmds.connectAttr(name + '_R_Corner{}.outValue'.format( nc['remap_value']), bs_corners + '.color2G')

    bsCenter = cmds.shadingNode('blendColors', au=1, n=name + '_TpBt_' + nc['blend'])
    cmds.connectAttr(condition + '.outColorR', bsCenter + '.blender')
    cmds.connectAttr(name + '_chewHeight{}.outValue'.format( nc['remap_value']), bsCenter + '.color1R')
    cmds.connectAttr(name + '_chewHeight{}.outValue'.format( nc['remap_value']), bsCenter + '.color1G')

    cmds.connectAttr(bs_corners + '.outputR', nc['left'] + jnts_name[0] + nc['base_joint'] + '_parentConstraint1.switch')
    cmds.connectAttr(bs_corners + '.outputG', nc['right'] + jnts_name[0] + nc['base_joint'] + '_parentConstraint1.switch')

    cmds.connectAttr(bsCenter + '.outputR', nc['up'] + jnts_name[0] + nc['base_joint'] + '_parentConstraint1.switch')
    cmds.connectAttr(bsCenter + '.outputG', nc['down'] + jnts_name[0] + nc['base_joint'] + '_parentConstraint1.switch')

    cmds.setAttr(bsCenter + '.color2R', 1)


    #build_jaw_block()

