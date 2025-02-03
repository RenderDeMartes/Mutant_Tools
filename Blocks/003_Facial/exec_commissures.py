from __future__ import absolute_import
from maya import cmds, mel
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

TAB_FOLDER = '03_Facial'
PYBLOCK_NAME = 'exec_commissures'

#Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-2]
FOLDER=''
for f in PATH_PARTS:
	FOLDER = os.path.join(FOLDER, f)

#---------------------------------------------

def create_commissures_block(name='Commissures'):
    # Read name conventions as nc[''] and setup as seup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-2]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '012_Commissures.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()

    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name = name, icon = 'Commissures',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]
      
    wide = mel.eval("curve -d 3 -p 2 0 0 -p 2.333333 0 0 -p 3 0 0 -p 3.666667 0 0 -p 4 0 0 -k 0 -k 0 -k 0 -k 1 -k 2 -k 2 -k 2 -n {};".format(nc['left']+name+'_Wide'+nc['guide']))
    mt.assign_color(color='purple')
    cmds.xform(pivots=[2.0, 0.0, 0.0])
    narrow = mel.eval("curve -d 3 -p 2 0 0 -p 1.666667 0 0 -p 1 0 0 -p 0.333333 0 0 -p 0 0 0 -k 0 -k 0 -k 0 -k 1 -k 2 -k 2 -k 2 -n {};".format(nc['left']+name+'_Narrow'+nc['guide']))
    mt.assign_color(color='green')
    cmds.xform(pivots=[2.0, 0.0, 0.0])
    up = mel.eval("curve -d 3 -p 2 0 0 -p 2 0.333333 0 -p 2 1 0 -p 2 1.666667 0 -p 2 2 0 -k 0 -k 0 -k 0 -k 1 -k 2 -k 2 -k 2 -n {};".format(nc['left']+name+'_Up'+nc['guide']))
    mt.assign_color(color='lightBlue')
    cmds.xform(pivots=[2.0, 0.0, 0.0])
    down = mel.eval("curve -d 3 -p 2 0 0 -p 2 -0.333333 0 -p 2 -1 0 -p 2 -1.666667 0 -p 2 -2 0 -k 0 -k 0 -k 0 -k 1 -k 2 -k 2 -k 2 -n {};".format(nc['left']+name+'_Down'+nc['guide']))
    mt.assign_color(color='yellow')
    cmds.xform(pivots=[2.0, 0.0, 0.0])

    cmds.parent(wide, narrow, up, down, block)

    cmds.select(block)

    print('{} Created Successfully'.format(name))


# create_commissures_block()

# -------------------------

def build_commissures_block():
    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    name = block.replace(nc['module'], '')

    sides = []
    ctrls = []
    left_ctrl = cmds.getAttr('{}.LeftCornerCtrl'.format(config))
    if left_ctrl:
        if left_ctrl == 'new_locator':
            left_ctrl = cmds.spaceLocator(n=nc['left'] + name + nc['ctrl'])[0]
        ctrls.append(left_ctrl)
        sides.append(nc['left'])
    right_ctrl = cmds.getAttr('{}.RightCornerCtrl'.format(config))
    if right_ctrl:
        if right_ctrl == 'new_locator':
            right_ctrl = cmds.spaceLocator(n=nc['right'] + name + nc['ctrl'])[0]
        ctrls.append(right_ctrl)
        sides.append(nc['right'])

    if not sides:
        return False

    attrs = ['translateX', 'translateX', 'translateY', 'translateY']
    values = [1, -1, 1, -1]

    all_curves = []
    all_joints = []
    curves_grp = []

    for ctrl, side, in zip(ctrls, sides):
        wide_curve = cmds.duplicate(nc['left'] + name + '_Wide' + nc['guide'], n=side + name + '_Wide' + nc['curve'])[0]
        cmds.parent(wide_curve, w=True)
        narrow_curve = \
        cmds.duplicate(nc['left'] + name + '_Narrow' + nc['guide'], n=side + name + '_Narrow' + nc['curve'])[0]
        cmds.parent(narrow_curve, w=True)
        up_curve = cmds.duplicate(nc['left'] + name + '_Up' + nc['guide'], n=side + name + '_Up' + nc['curve'])[0]
        cmds.parent(up_curve, w=True)
        down_curve = cmds.duplicate(nc['left'] + name + '_Down' + nc['guide'], n=side + name + '_Down' + nc['curve'])[0]
        cmds.parent(down_curve, w=True)

        all_curves.append(wide_curve)
        all_curves.append(narrow_curve)
        all_curves.append(up_curve)
        all_curves.append(down_curve)

        curves = [wide_curve, narrow_curve, up_curve, down_curve]

        joints = []
        for curve, attr, value in zip(curves, attrs, values):
            cmds.select(cl=True)
            print(curve)
            jnt = cmds.joint(n=curve.replace(nc['curve'], nc['joint']))
            poci = cmds.createNode('pointOnCurveInfo', n=curve.replace(nc['curve'], '_POCI'))
            cmds.connectAttr('{}.worldSpace[0]'.format(curve), '{}.inputCurve'.format(poci))
            cmds.connectAttr('{}.position'.format(poci), '{}.translate'.format(jnt))
            print(attr)
            mt.connect_md_node(in_x1=ctrl + '.' + attr, in_x2=value, out_x='{}.parameter'.format(poci),
                               mode='multiply')
            cmds.setAttr(poci + '.turnOnPercentage', 1)
            joints.append(jnt)
            all_joints.append(jnt)
            
            print('DEBUG'.center(30, '#'))
            print('curve = {}, value = {}, side = {}'.format(curve, value, side))

            #add remap to wide and narrow
            if 'Wide' in jnt or 'Narrow' in jnt:
                remap_node = cmds.createNode('remapValue', name=jnt + '_RemapValue')
                cmds.setAttr(remap_node + '.outputMin', 0)
                coefficient = 5
                if side == nc['right']:
                    coefficient = -5

                print('jnt = {}, coefficient = {}'.format(jnt, coefficient))
                cmds.setAttr(remap_node + '.outputMax', value * coefficient)
                cmds.setAttr(remap_node + '.inputMin', 0)
                cmds.setAttr(remap_node + '.inputMax', 1*value)

                cmds.connectAttr('{}.{}'.format(ctrl, attr), '{}.inputValue'.format(remap_node))
                cmds.connectAttr('{}.outColor.outColorR'.format(remap_node), '{}.rotateY'.format(jnt))


        curve_grp = cmds.group(empty=True, n=side + name + nc['group'])
        cmds.parent(curves, curve_grp)
        if side == nc['right']:
            curve_grp = mt.mirror_group(curve_grp, world=True)

        curves_grp.append(curve_grp)

        for jnt in joints:
            bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])
            cmds.select(cl=True)
            bind_joint = cmds.joint(n=jnt.replace(nc['joint'], nc['joint_bind']))
            cmds.parentConstraint(jnt, bind_joint)
            cmds.scaleConstraint(jnt, bind_joint)
            cmds.setAttr('{}.radius'.format(bind_joint), 1.5)
            cmds.parent(bind_joint, bind_jnt_grp)

    # groups for later cleaning
    # clean a bit
    clean_rig_grp = cmds.group(em=True, name=name + '_Rig' + nc['group'])
    cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
    cmds.parent(all_joints, curves_grp, clean_rig_grp)

    print('Build {} Success'.format(block))

# build_commissures_block()
