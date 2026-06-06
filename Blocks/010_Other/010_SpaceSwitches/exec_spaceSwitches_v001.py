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
    PATH_PARTS = PATH.parts[:-3]
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



def build_spaceSwitches_block(force=False):
    nc, curve_data, setup = mt.import_configs()
    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]

    # Check if this block should run after the full build completes
    run_after = False
    if cmds.attributeQuery('RunAfterBuild', n=config, exists=True):
        run_after = cmds.getAttr('{}.RunAfterBuild'.format(config))

    if run_after and not force:
        print('SpaceSwitches block {} deferred to run after build completes'.format(block))
        return

    # get the translate/rotate configuration to determine which type of constrain to use

    translate = cmds.getAttr('{}.Translate'.format(config))
    rotate = cmds.getAttr('{}.Rotate'.format(config))

    # get custom attr name (fallback to 'Follow')
    custom_attr_name = 'Follow'
    if cmds.attributeQuery('AttrName', n=config, exists=True):
        val = cmds.getAttr('{}.AttrName'.format(config), asString=True) or ''
        if val.strip():
            custom_attr_name = val.strip()

    # get split translate/rotate toggle (default off)
    split_tr = False
    if cmds.attributeQuery('SplitTranslateRotate', n=config, exists=True):
        split_tr = cmds.getAttr('{}.SplitTranslateRotate'.format(config))

    # get maintain offset toggle (default on for backward compatibility)
    maintain_offset = True
    if cmds.attributeQuery('MaintainOffset', n=config, exists=True):
        maintain_offset = cmds.getAttr('{}.MaintainOffset'.format(config))
    
    print("WILL BUILD WITH MAINTAIN OFFSET SET TO : {}".format(maintain_offset))

    def constrain(source, target, mo=True):
        if translate and rotate:
            pc = cmds.parentConstraint(source, target, mo=mo)[0]
            cmds.setAttr('{}.interpType'.format(pc), 2)
            return pc
        elif translate:
            return cmds.pointConstraint(source, target, mo=mo)[0]
        elif rotate:
            oc = cmds.orientConstraint(source, target, mo=mo)[0]
            cmds.setAttr('{}.interpType'.format(oc), 2)
            return oc

    def constrain_translate(source, target, mo=True):
        return cmds.pointConstraint(source, target, mo=mo)[0]

    def constrain_rotate(source, target, mo=True):
        oc = cmds.orientConstraint(source, target, mo=mo)[0]
        cmds.setAttr('{}.interpType'.format(oc), 2)
        return oc


    def create_space_switch_setup(target_ctrl, spaces, attrs_holder, clean_rig_grp, block, custom_names=''):

        block = block.replace('_Block', '')

        spaces_str = spaces
        spaces = spaces.replace(" ", "")
        spaces = spaces.split(',')

        # if each side has a separate ctrl to hold space attrs, we can omit the side token in the attr name

        if 'L_' in attrs_holder or 'R_' in attrs_holder:
            attr_name = block.replace('L_', '')
            attr_name = attr_name.replace('R_', '')
        else:
            attr_name = block


        def process_spaces(spaces, custom_names=''):

            # If custom names provided and count matches, use them directly
            if custom_names and custom_names.strip():
                cn_list = [n.strip() for n in custom_names.split(',')]
                if len(cn_list) == len(spaces):
                    return cn_list

            # Change the display name in the space enum attr for particular cases

            c_spaces = list(spaces)
            for index, space in enumerate(c_spaces):
                if space == 'Mutant_Tools_Grp':
                    c_spaces[index] = "World"
                if space == 'Mover_Gimbal_Ctrl':
                    c_spaces[index] = 'Global_Ctrl'
            return c_spaces

        processed_spaces = process_spaces(spaces, custom_names)

        animbot_friendly=True
        if not cmds.attributeQuery('Animbot', n=config, exists=True):
            animbot_friendly = False
        else:
            animbot_friendly = cmds.getAttr('{}.Animbot'.format(config))

        enums_str = ':'.join(processed_spaces)

        # ---- SPLIT MODE: separate translate and rotate attrs ----
        if split_tr and translate and rotate:

            # Create two auto_grps: one for translate, one for rotate
            auto_grp_t = cmds.group(em=1, n=target_ctrl + nc['auto'] + '_SpSw_T' + nc['group'])
            auto_grp_r = cmds.group(em=1, n=target_ctrl + nc['auto'] + '_SpSw_R' + nc['group'])
            target_ctrl_parent = cmds.listRelatives(target_ctrl, p=1)

            cmds.parent(auto_grp_t, target_ctrl_parent)
            cmds.delete(cmds.parentConstraint(target_ctrl, auto_grp_t))
            cmds.delete(cmds.scaleConstraint(target_ctrl, auto_grp_t))

            cmds.parent(auto_grp_r, auto_grp_t)
            cmds.delete(cmds.parentConstraint(target_ctrl, auto_grp_r))
            cmds.delete(cmds.scaleConstraint(target_ctrl, auto_grp_r))

            cmds.parent(target_ctrl, auto_grp_r)

            spaces_grp = cmds.group(em=1, n=block+'_locs'+nc['group'])

            # Create the two enum attrs
            t_attr_display = 'Translation'
            r_attr_display = 'Rotation'

            if animbot_friendly:
                space_attr_t = mt.new_enum(input=target_ctrl, name=t_attr_display, enums=enums_str, keyable=True,
                                           long_name=True)
                space_attr_r = mt.new_enum(input=target_ctrl, name=r_attr_display, enums=enums_str, keyable=True,
                                           long_name=True)
            else:
                space_attr_t = mt.new_enum(input=attrs_holder, name=attr_name + '_T', enums=enums_str, keyable=True,
                                           long_name=True)
                mt.create_proxy_attr(original_attr=space_attr_t, output_node=target_ctrl, line_on_top=False, line_name='', new_name=True, name=t_attr_display)
                space_attr_r = mt.new_enum(input=attrs_holder, name=attr_name + '_R', enums=enums_str, keyable=True,
                                           long_name=True)
                mt.create_proxy_attr(original_attr=space_attr_r, output_node=target_ctrl, line_on_top=False, line_name='', new_name=True, name=r_attr_display)

            print(space_attr_t)
            print(space_attr_r)

            for index, space in enumerate(spaces):
                space_short = space.split('|')[-1]

                # Translate locator â€” snap to target_ctrl so offset is zero at default
                t_loc = cmds.spaceLocator(n=space_short+'_'+block+'_T'+nc['locator'])[0]
                cmds.delete(cmds.parentConstraint(target_ctrl, t_loc))
                t_loc = cmds.parent(t_loc, spaces_grp)[0]
                cmds.parentConstraint(space, t_loc, mo=maintain_offset)

                c_t = constrain_translate(t_loc, auto_grp_t, maintain_offset)

                cond_t = cmds.shadingNode('condition', asUtility=True, n=block+space_short+'_T'+nc['condition'])
                cmds.setAttr('{}.operation'.format(cond_t), 0)
                cmds.setAttr('{}.colorIfTrueR'.format(cond_t), 1)
                cmds.setAttr('{}.colorIfFalseR'.format(cond_t), 0)
                cmds.setAttr('{}.secondTerm'.format(cond_t), index)
                cmds.connectAttr(space_attr_t, '{}.firstTerm'.format(cond_t))
                cmds.connectAttr('{}.outColorR'.format(cond_t), '{}.{}W{}'.format(c_t, t_loc, index))

                # Rotate locator â€” snap to target_ctrl so offset is zero at default
                r_loc = cmds.spaceLocator(n=space_short+'_'+block+'_R'+nc['locator'])[0]
                cmds.delete(cmds.parentConstraint(target_ctrl, r_loc))
                r_loc = cmds.parent(r_loc, spaces_grp)[0]
                cmds.parentConstraint(space, r_loc, mo=maintain_offset)

                c_r = constrain_rotate(r_loc, auto_grp_r, maintain_offset)

                cond_r = cmds.shadingNode('condition', asUtility=True, n=block+space_short+'_R'+nc['condition'])
                cmds.setAttr('{}.operation'.format(cond_r), 0)
                cmds.setAttr('{}.colorIfTrueR'.format(cond_r), 1)
                cmds.setAttr('{}.colorIfFalseR'.format(cond_r), 0)
                cmds.setAttr('{}.secondTerm'.format(cond_r), index)
                cmds.connectAttr(space_attr_r, '{}.firstTerm'.format(cond_r))
                cmds.connectAttr('{}.outColorR'.format(cond_r), '{}.{}W{}'.format(c_r, r_loc, index))

            cmds.parent(spaces_grp, clean_rig_grp)
            cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
            if cmds.objExists('scale_reader '):
                cmds.scaleConstraint('scale_reader ', spaces_grp)
            else:
                cmds.scaleConstraint('Global_Ctrl', spaces_grp)

            #make keyable
            cmds.setAttr(space_attr_t, e=True, k=True)
            cmds.setAttr(space_attr_r, e=True, k=True)

        # ---- COMBINED MODE (default): single attr ----
        else:

            # get the target controller and add an auto_grp above it

            auto_grp = cmds.group(em=1, n=target_ctrl + nc['auto'] + '_SpSw' + nc['group'])
            target_ctrl_parent = cmds.listRelatives(target_ctrl, p=1)
            cmds.parent(auto_grp, target_ctrl_parent)
            cmds.delete(cmds.parentConstraint(target_ctrl, auto_grp))
            cmds.delete(cmds.scaleConstraint(target_ctrl, auto_grp))
            cmds.parent(target_ctrl, auto_grp)

            spaces_grp = cmds.group(em=1, n=block+'_locs'+nc['group'])

            if animbot_friendly:
                space_attr = mt.new_enum(input=target_ctrl, name=custom_attr_name, enums=enums_str, keyable=True,
                                         long_name=True)
            else:
                space_attr = mt.new_enum(input=attrs_holder, name=attr_name, enums=enums_str, keyable=True,
                                         long_name=True)
                mt.create_proxy_attr(original_attr=space_attr, output_node=target_ctrl, line_on_top=False, line_name='', new_name=True, name=custom_attr_name)


            print(space_attr)

            for index, space in enumerate(spaces):
                space_short = space.split('|')[-1]
                space_loc = cmds.spaceLocator(n=space_short+'_'+block+nc['locator'])[0]

                # Snap locator to the target ctrl's world transform so the
                # maintain-offset constraint preserves the control's position
                cmds.delete(cmds.parentConstraint(target_ctrl, space_loc))

                space_loc = cmds.parent(space_loc, spaces_grp)[0]
                cmds.parentConstraint(space, space_loc, mo=maintain_offset)

                c = constrain(space_loc, auto_grp, maintain_offset)

                condition_node = cmds.shadingNode('condition', asUtility=True, n=block+space_short+nc['condition'])
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
    custom_names = ''
    if cmds.attributeQuery('CustomNames', n=config, exists=True):
        custom_names = cmds.getAttr('{}.CustomNames'.format(config), asString=True) or ''
    if not cmds.attributeQuery('___________', n=attrs_holder, exists=True) and not cmds.attributeQuery('Animbot', n=config, exists=True):
        line_attr = mt.new_enum(input=attrs_holder, name='___________', enums='{}:'.format('Spaces'))
        cmds.setAttr(line_attr, e=True, lock=True)
    create_space_switch_setup(target_ctrl, spaces, attrs_holder, clean_rig_grp, block, custom_names)

    mirror = cmds.getAttr('{}.Mirror'.format(config))
    if mirror:
        r_name = block.replace('L_', 'R_')
        r_name = r_name.replace('_Block', '')
        r_clean_rig_group = cmds.group(em=True, n=r_name + '_Rig' + nc['group'])
        r_target_ctrl = target_ctrl.replace('L_', 'R_')
        r_spaces = spaces.replace('L_', 'R_')
        r_attrs = attrs_holder.replace('L_', 'R_')
        r_custom_names = custom_names.replace('L_', 'R_') if custom_names else ''

        create_space_switch_setup(r_target_ctrl, r_spaces, r_attrs, r_clean_rig_group, r_name, r_custom_names)

    print('Build {} sucess'.format(block))