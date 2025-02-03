from __future__ import absolute_import
from maya import cmds
from maya import mel
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

TAB_FOLDER = '010_Other'
PYBLOCK_NAME = 'exec_spaceSwitches'

#---------------------------------------------

#Print For Gaston

def create_spaceSwitches_block(name='target_switches'):
    # Read name conventions as nc[''] and setup as seup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-2]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '010_SpaceSwitches.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()
    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name = name, icon = 'SpaceSwitch',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]

    print('{} Created succesfully'.format(name))



def build_spaceSwitches_block():
    nc, curve_data, setup = mt.import_configs()
    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]

    # get the translate/rotate configuration to determine which type of constrain to use

    translate = cmds.getAttr('{}.Translate'.format(config))
    rotate = cmds.getAttr('{}.Rotate'.format(config))
    def constrain(source, target):
        if translate and rotate:
            pc = cmds.parentConstraint(source, target, mo=1)[0]
            cmds.setAttr('{}.interpType'.format(pc), 2)
            return pc
        elif translate:
            return cmds.pointConstraint(source, target, mo=1)[0]
        elif rotate:
            oc = cmds.orientConstraint(source, target, mo=1)[0]
            cmds.setAttr('{}.interpType'.format(oc), 2)
            return oc


    def create_space_switch_setup(target_ctrl, spaces, attrs_holder, clean_rig_grp, block):

        block = block.replace('_Block', '')

        # get the target controller and add an auto_grp above it

        auto_grp = cmds.group(em=1, n=target_ctrl + nc['auto'] + '_SpSw' + nc['group'])
        target_ctrl_parent = cmds.listRelatives(target_ctrl, p=1)
        cmds.parent(auto_grp, target_ctrl_parent)
        cmds.delete(cmds.parentConstraint(target_ctrl, auto_grp))
        cmds.delete(cmds.scaleConstraint(target_ctrl, auto_grp))
        cmds.parent(target_ctrl, auto_grp)

        spaces_grp = cmds.group(em=1, n=block+'_locs'+nc['group'])
        spaces = spaces.replace(" ", "")
        spaces = spaces.split(',')

        # create space attrs

        # if each side has a separate ctrl to hold space attrs, we can omit the side token in the attr name

        if 'L_' in attrs_holder or 'R_' in attrs_holder:
            attr_name = block.replace('L_', '')
            attr_name = attr_name.replace('R_', '')
        else:
            attr_name = block


        def process_spaces(spaces):

            # Change the display name in the space enum attr for particular cases

            c_spaces = list(spaces)
            for index, space in enumerate(c_spaces):
                if space == 'Mutant_Tools_Grp':
                    c_spaces[index] = "World"
                if space == 'Mover_Gimbal_Ctrl':
                    c_spaces[index] = 'Global_Ctrl'
            return c_spaces

        processed_spaces = process_spaces(spaces)

        animbot_friendly=True
        if not cmds.attributeQuery('Animbot', n=config, exists=True):
            animbot_friendly = False
        else:
            animbot_friendly = cmds.getAttr('{}.Animbot'.format(config))

        if animbot_friendly:
            space_attr = mt.new_enum(input=target_ctrl, name='Follow', enums=':'.join(processed_spaces), keyable=True,
                                     long_name=True)
        else:
            space_attr = mt.new_enum(input=attrs_holder, name=attr_name, enums=':'.join(processed_spaces), keyable=True,
                                     long_name=True)
            mt.create_proxy_attr(original_attr=space_attr, output_node=target_ctrl, line_on_top=False, line_name='', new_name=True, name='Follow')


        print(space_attr)

        #Reorder the Rotate Order
        # if cmds.attributeQuery('RotateOrder', n=target_ctrl, exists=True):
        #     try:
        #         cmds.deleteAttr('{}.RotateOrder'.format(target_ctrl))
        #         cmds.undo()
        #     except:
        #         pass


        for index, space in enumerate(spaces):

            space_loc = cmds.spaceLocator(n=space+'_'+block+nc['locator'])[0]
            cmds.parent(space_loc, spaces_grp)
            cmds.parentConstraint(space, space_loc, mo=True)

            c = constrain(space_loc, auto_grp)

            condition_node = cmds.shadingNode('condition', asUtility=True, n=block+space+nc['condition'])
            cmds.setAttr('{}.operation'.format(condition_node), 0)
            cmds.setAttr('{}.colorIfTrueR'.format(condition_node), 1)
            cmds.setAttr('{}.colorIfFalseR'.format(condition_node), 0)
            cmds.setAttr('{}.secondTerm'.format(condition_node), index)

            cmds.connectAttr(space_attr, '{}.firstTerm'.format(condition_node))
            cmds.connectAttr('{}.outColorR'.format(condition_node), '{}.{}W{}'.format(c, space_loc, index))

        cmds.parent(spaces_grp, clean_rig_grp)
        cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
        if cmds.objExists('scale_reader '):
            cmds.scaleConstraint('scale_reader ', spaces_grp)
        else:
            cmds.scaleConstraint('Global_Ctrl', spaces_grp)

        #make keyable
        cmds.setAttr(space_attr, e=True, k=True)

    clean_rig_grp = cmds.group(em=True, n=block.replace('_Block', '') + '_Rig' + nc['group'])

    target_ctrl = cmds.getAttr('{}.SetTargetCtrl'.format(config), asString=True)
    spaces = cmds.getAttr('{}.Spaces'.format(config), asString=True)
    attrs_holder = cmds.getAttr('{}.SetAttrsHolder'.format(config), asString=1)
    if not cmds.attributeQuery('___________', n=attrs_holder, exists=True) and not cmds.attributeQuery('Animbot', n=config, exists=True):
        line_attr = mt.new_enum(input=attrs_holder, name='___________', enums='{}:'.format('Spaces'))
        cmds.setAttr(line_attr, e=True, lock=True)
    create_space_switch_setup(target_ctrl, spaces, attrs_holder, clean_rig_grp, block)

    mirror = cmds.getAttr('{}.Mirror'.format(config))
    if mirror:
        r_name = block.replace('L_', 'R_')
        r_name = r_name.replace('_Block', '')
        r_clean_rig_group = cmds.group(em=True, n=r_name + '_Rig' + nc['group'])
        r_target_ctrl = target_ctrl.replace('L_', 'R_')
        r_spaces = spaces.replace('L_', 'R_')
        r_attrs = attrs_holder.replace('L_', 'R_')

        create_space_switch_setup(r_target_ctrl, r_spaces, r_attrs, r_clean_rig_group, r_name)

    print('Build {} sucess'.format(block))