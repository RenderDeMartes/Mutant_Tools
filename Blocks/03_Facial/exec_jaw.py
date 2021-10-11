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
    jaw_tp = mt.create_joint_guide(name = name + 'Tp')
    cmds.move(0,1.5,3)
    jaw_bt = mt.create_joint_guide(name = name + 'Bt')
    cmds.move(0,1.4,3)
    jaw_Lf = mt.create_joint_guide(name=name + 'Lf')
    cmds.move(1.5, 1.8, 3)
    jaw_Rt = mt.create_joint_guide(name=name + 'Rt')
    cmds.move(-1.5, 1.8, 3)

    cmds.parent(jaw_tp, jaw_Lf, jaw_Rt, jaw_start)
    cmds.parent(jaw_bt, jaw_tp)

    cmds.hide(jaw_bt)

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_jaw_block()

#-------------------------

def build_jaw_block():
    mt.check_is_there_is_base()

    name = mt.ask_name(text=module['Name'])
    # if cmds.objExists('{}{}'.format(name, nc['module'])):
    #     cmds.warning('Name already exists.')
    #     return ''

    block = mt.create_block(name=name, icon='Clavicle', attrs=module['attrs'], build_command=module['build_command'],
                            import_command=module['import'])
    config = block[1]
    block = block[0]

    jntsName = [name, name + 'Tp', name + 'Bt', name + 'Lf', name + 'Rt']

    #CREATE A JOINT FOR EVERY GUIDE
    for i in jntsName:
        cmds.joint(n=i + '_jnt')
        cmds.select(cl=1)

    # CREATE A EXTRA JOINT FOR LIPS/JAWS
    cmds.joint(n=name + '_No_jnt')

    for i in jntsName:
        cmds.select(cl=1)
        newJaw = cmds.duplicate(name + '_jnt')[0]
        cmds.rename(newJaw, i + '_base_jnt')
        cmds.parent(i + '_jnt', i + '_base_jnt')

    # PLACE JOINTS IN GUIDES POS
    for i in range(len(jntsName)):
        position = cmds.xform(jntsName[i] + '_Guide', q=1, ws=1, t=1)
        if i == 0:
            cmds.select(jntsName[i] + '_No_jnt')
            cmds.xform(ws=1, t=position)
            cmds.select(jntsName[i] + '_base_jnt')
            cmds.xform(ws=1, t=position)
        cmds.select(jntsName[i] + '_jnt')
        cmds.xform(ws=1, t=position)

    cmds.select(name + '_jnt')
    cmds.xform(os=1, t=(0,0,0))

    # JAW CTL
    ctl = cmds.circle(n=name + '_Ctrl', nr=[0, 1, 0])[0]
    cmds.setAttr(ctl + '.overrideEnabled', 1)
    cmds.setAttr(ctl + '.overrideColor', 17)
    sdk = cmds.group(n=name + '_sdk')
    grp = cmds.group(n=name + '_grp')
    cons = cmds.parentConstraint(name + '_jnt', grp, mo=0)
    cmds.delete(cons)

    # ATTRS JAW CTL
    cmds.addAttr(ctl, ln='jawOpen', k=1, h=0)
    cmds.addAttr(ctl, ln='chew', k=1, h=0, min=0, max=1)
    cmds.addAttr(ctl, ln='chewHeight', k=1, h=0, min=-1, max=1)
    cmds.addAttr(ctl, ln='cornerPinLf', k=1, h=0, min=-1, max=1)
    cmds.addAttr(ctl, ln='cornerPinRt', k=1, h=0, min=-1, max=1)

    # REHIERARCHY WITH JAW CTL
    cmds.parent(name + '_base_jnt', name + '_Ctrl')
    cmds.parent(name + '_No_jnt', name + '_grp')
    #
    # CONSTRAINTS
    for i in jntsName:
        if i == name:
            pass
        else:
            cons = cmds.parentConstraint(name + '_No_jnt', name + '_jnt', i + '_base_jnt')[0]
            cmds.addAttr(cons, ln='switch', k=1, h=0, min=0, max=1)
            reverse = cmds.shadingNode('reverse', au=1, n=cons + '_Rev')
            cmds.connectAttr(cons + '.switch', reverse + '.inputX')
            cmds.connectAttr(reverse + '.outputX', cons + '.' + name + '_jntW1')
            cmds.connectAttr(cons + '.switch', cons + '.' + name + '_No_jntW0')


    #CONNECT JAW ATTRIBUTES
    #DRIVEN KEYS JAW OPEN
    jawSdk = [sdk + '.ty', sdk + '.tz', sdk + '.rx']

    for i in jawSdk:
        cmds.setDrivenKeyframe(i, cd=ctl + '.jawOpen', itt='spline', ott='spline' )

    cmds.setAttr(ctl + '.jawOpen', 1)
    cmds.setAttr(sdk + '.ty', -.2)
    cmds.setAttr(sdk + '.tz', .1)
    cmds.setAttr(sdk + '.rx', 25)

    for i in jawSdk:
        cmds.setDrivenKeyframe(i, cd=ctl + '.jawOpen', itt='spline', ott='spline' )

    cmds.selectKey(sdk, attribute='translateY')
    cmds.setInfinity( pri='linear', poi='linear' )
    cmds.selectKey(sdk, attribute='translateZ')
    cmds.setInfinity( pri='linear', poi='linear' )
    cmds.selectKey(sdk, attribute='rotateX')
    cmds.setInfinity( pri='linear', poi='linear' )

    cmds.setAttr(ctl + '.jawOpen', 0)

    # CONDITION NODE
    condition = cmds.shadingNode('condition', au=1, n=name + '_Open_Con')
    cmds.connectAttr(ctl + '.chew', condition + '.colorIfTrueR')
    cmds.connectAttr(ctl + '.jawOpen', condition + '.firstTerm')
    cmds.setAttr(condition + '.operation', 3)

    # REMAP VALUES
    attributesRemap = ['chewHeight', 'cornerPinLf', 'cornerPinRt']

    for i in attributesRemap:
        rv = cmds.shadingNode('remapValue', au=1, n=name + '_' + i + '_RV')
        cmds.connectAttr(ctl + '.' + i, rv + '.inputValue')
        cmds.setAttr(rv + '.inputMin', -1)

    # BLEND COLORS
    bsCorners = cmds.shadingNode('blendColors', au=1, n=name + '_LfRt_blendColors')
    cmds.connectAttr(condition + '.outColorR', bsCorners + '.blender')
    cmds.connectAttr(name + '_chewHeight_RV.outValue', bsCorners + '.color1R')
    cmds.connectAttr(name + '_chewHeight_RV.outValue', bsCorners + '.color1G')
    cmds.connectAttr(name + '_cornerPinLf_RV.outValue', bsCorners + '.color2R')
    cmds.connectAttr(name + '_cornerPinRt_RV.outValue', bsCorners + '.color2G')

    bsCenter = cmds.shadingNode('blendColors', au=1, n=name + '_TpBt_blendColors')
    cmds.connectAttr(condition + '.outColorR', bsCenter + '.blender')
    cmds.connectAttr(name + '_chewHeight_RV.outValue', bsCenter + '.color1R')
    cmds.connectAttr(name + '_chewHeight_RV.outValue', bsCenter + '.color1G')

    cmds.connectAttr(bsCorners + '.outputR', name + 'Lf_base_jnt_parentConstraint1.switch')
    cmds.connectAttr(bsCorners + '.outputG', name + 'Rt_base_jnt_parentConstraint1.switch')

    cmds.connectAttr(bsCenter + '.outputR', name + 'Tp_base_jnt_parentConstraint1.switch')
    cmds.connectAttr(bsCenter + '.outputG', name + 'Bt_base_jnt_parentConstraint1.switch')

    cmds.setAttr(bsCenter + '.color2R', 1)


    #build_jaw_block()
