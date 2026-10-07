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
TAB_FOLDER = '002_Biped'
PYBLOCK_NAME = 'exec_smarthand'

#Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-3]
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

MODULE_FILE = os.path.join(os.path.dirname(__file__),'01_SmartHand.json')
with open(MODULE_FILE) as module_file:
	module = json.load(module_file)

#---------------------------------------------

def create_smarthand_block(name = 'SmartHand'):

    nc, curve_data, setup = mt.import_configs()
    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name = name, icon = 'SmartHand',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]
    name = block.replace(nc['module'],'')

    #cmds.getAttr('{}.AttrName'.format(config)) #get attrs from config
    #cmds.getAttr('{}.AttrName'.format(config), asString = True) #for enums
    #joint_one = mt.create_joint_guide(name = name) #guide base with shapes

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_smarthand_block()

#-------------------------
# Hand v002 with Orients = SN puts an OrientChange group above the finger ctrls at build. On a v001 hand
# that group came later (Custom_Biped_Orients after SmartHand), right above the ctrl and under the smart
# groups. Same layout here: the smart groups go above the OrientChange group, in the frame the ctrl had
# before it was re oriented, so curl / sides / spread rotate the same way.

def _orient_change(ctrl):
    parent = (cmds.listRelatives(ctrl, p=True) or [''])[0]
    return parent if parent.endswith('OrientChange' + nc['group']) else None


def insert_group(ctrl, custom_name):
    """Group right above the ctrl (mt.root_grp), or above its OrientChange group."""
    orient_change = _orient_change(ctrl)
    if not orient_change:
        return mt.root_grp(ctrl, custom=True, custom_name=custom_name)[0]
    grp = cmds.group(em=True, n='{}{}{}'.format(ctrl, custom_name, nc['group']),
                     p=cmds.listRelatives(orient_change, p=True)[0])
    cmds.parent(orient_change, grp, relative=True)
    return grp


def smart_group(ctrl, custom_name):
    """insert_group with its rest transform moved to the offset parent matrix, its channels start at zero
    (a root group less per ctrl)."""
    grp = insert_group(ctrl, custom_name)
    cmds.setAttr(grp + '.offsetParentMatrix', cmds.xform(grp, q=True, os=True, m=True), type='matrix')
    cmds.xform(grp, os=True, m=[1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1])
    return grp


def original_frame(ctrl):
    """Node with the ctrl orientation before an OrientChange group."""
    orient_change = _orient_change(ctrl)
    return cmds.listRelatives(orient_change, p=True)[0] if orient_change else ctrl


# Axes enum: every way to give curl, sides and spread to the smart ctrl rotate X, Y, Z.
# The first one is the default (same as the v001 Mode A), MODE_B is the v001 Mode B.
AXES_OPTIONS = ['XSpread_YSides_ZCurl', 'XSides_YSpread_ZCurl', 'XCurl_YSides_ZSpread',
                'XCurl_YSpread_ZSides', 'XSpread_YCurl_ZSides', 'XSides_YCurl_ZSpread']
MODE_B = 'XCurl_YSpread_ZSides'


def parse_axes(option):
    """'XSpread_YSides_ZCurl' -> {'Spread': 'X', 'Sides': 'Y', 'Curl': 'Z'}"""
    return dict((part[1:], part[0]) for part in option.split('_'))


def build_smarthand_block():

    mt.check_is_there_is_base()


    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]

    hand_block = cmds.getAttr('{}.HandBlock'.format(config), asString=True)
    # which smart ctrl rotation drives curl, sides and spread
    if cmds.attributeQuery('Axes', n=config, exists=True):
        axes = parse_axes(cmds.getAttr('{}.Axes'.format(config), asString=True))
    elif cmds.attributeQuery('Mode', n=config, exists=True) and cmds.getAttr('{}.Mode'.format(config), asString=True) == 'B':
        axes = parse_axes(MODE_B)
    else:
        axes = parse_axes(AXES_OPTIONS[0])


    if cmds.objExists(hand_block+'_Wrist_Ctrl'):
        to_build = [hand_block, hand_block.replace(nc['left'], nc['right'])]
    else:
        to_build = [hand_block]

    #build ------------------------------------------------------
    for side_guide in to_build:

        #prefix for right hand
        if str(side_guide).startswith(nc['right']):
            hand_grp = f'{side_guide}_Palm_Jnt_Ctrl_Grp'

            constraint = cmds.listRelatives(hand_grp, type='constraint', children=True)
            targets = cmds.parentConstraint(constraint, query=True, targetList=True)
            restore_parent_contraint = targets[0]

            cmds.delete(constraint)

            guide_parent = cmds.listRelatives(hand_grp, parent=True)[0]
            # Zero out rotation and scale on the parent
            for attr in ['rx', 'ry', 'rz', 'sx', 'sy', 'sz']:
                if cmds.objExists(f'{guide_parent}.{attr}'):
                    cmds.setAttr(f'{guide_parent}.{attr}', 0 if 'r' in attr else 1)


        #smart select the colors
        if str(side_guide).startswith(nc['left']):
            color = setup['left_color']
        elif str(side_guide).startswith(nc['right']):
            color = setup['right_color']       
        else:
            color = setup['main_color']       

        fingers = ['Pinky','Ring','Middle','Index']
        thumb = ['Thumb']

        size = mt.get_distance_between('{}_Middle_03_Ctrl'.format(side_guide), '{}_Middle_02_Ctrl'.format(side_guide))

        cmds.select(cl=True)
        main_ctrl = mt.curve(input='{}_Middle_03_Ctrl'.format(side_guide),
                        type='sphere',
                        rename=True,
                        custom_name=True,
                        name=side_guide+'_Middle_03_Ctrl'.replace(nc['ctrl'], '_Smart'+nc['ctrl']),
                        size=size)
        mt.assign_color(color=color)
        root_grp, auto_grp = mt.root_grp(autoRoot=True)
        mt.match(root_grp, original_frame('{}_Middle_03_Ctrl'.format(side_guide)), r=True, t=True)
        cmds.parent(root_grp, setup['base_groups']['control'] + nc['group'])
        cmds.move(5,0,0, auto_grp, r=True)


        mt.hide_attr(main_ctrl, t=True, s=True, rotate_order=True)

        spread_values = {'Middle': -0.15, 'Pinky': 0.6, 'Ring': 0.15, 'Index': -0.6}
        for finger in fingers:
            for num in range(1, 4):
                ctrl = '{}_{}_0{}_Ctrl'.format(side_guide, finger, num)
                if not cmds.objExists(ctrl):
                    continue
                # one group does curl (Z) and sides (Y, phalanx 1 only) with rotate order yzx, the same as the
                # v001 curl > sides groups. The rest place goes in its offset parent matrix (no root groups).
                curl = smart_group(ctrl, ctrl.replace('_Ctrl', '_SmartCurl_Grp'))
                cmds.connectAttr(main_ctrl + '.rotate' + axes['Curl'], curl + '.rotateZ')
                if num > 1:
                    continue
                cmds.setAttr(curl + '.rotateOrder', 1)  # yzx: sides then curl
                cmds.connectAttr(main_ctrl + '.rotate' + axes['Sides'], curl + '.rotateY')

                # spread under them, the main ctrl rotation times the finger value
                spread = insert_group(ctrl, ctrl.replace('_Ctrl', '_SmartSpread_Grp'))
                mult = cmds.createNode('multDoubleLinear', n=ctrl.replace('_Ctrl', '_SmartSpread_MultDoubleLinear'))
                cmds.connectAttr(main_ctrl + '.rotate' + axes['Spread'], mult + '.input1')
                cmds.setAttr(mult + '.input2', spread_values[finger])
                cmds.connectAttr(mult + '.output', spread + '.rotateZ')

        # prefix for right hand
        if str(side_guide).startswith(nc['right']):
            # Zero out rotation and scale on the parent
            for attr in ['rx', 'sx', 'sy', 'sz']:
                if cmds.objExists(f'{guide_parent}.{attr}'):
                    cmds.setAttr(f'{guide_parent}.{attr}', 180 if 'r' in attr else -1)
            cmds.parentConstraint(restore_parent_contraint, hand_grp, mo=True)

            miror_jnt_grp = mt.mirror_group(root_grp, world=True)
            cmds.parent(miror_jnt_grp, setup['base_groups']['control'] + nc['group'])

        cmds.parentConstraint('{}_Wrist_Ctrl'.format(side_guide), root_grp, mo=True)
        cmds.scaleConstraint('{}_Wrist_Ctrl'.format(side_guide), root_grp, mo=True)


    # build complete ----------------------------------------------------
    print ('Build {} Success'.format(block))


#build_smarthand_block()
