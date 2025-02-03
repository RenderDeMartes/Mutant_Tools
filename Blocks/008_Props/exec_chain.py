from __future__ import absolute_import
from maya import cmds
import json
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload
import os
from pathlib import Path
import string

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()

#---------------------------------------------

TAB_FOLDER = '008_Props'
PYBLOCK_NAME = 'exec_chain'

#---------------------------------------------

def create_chain_block(name = 'Chain'):

    #---------------------------------------------------
    #---------------------------------------------------
    #---------------------------------------------------

    letters = string.ascii_uppercase

    # Read name conventions as nc[''] and setup as seup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-2]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '08_Chain.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()

    #---------------------------------------------------
    #---------------------------------------------------
    #---------------------------------------------------

    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''
    amount = mt.ask_name(ask_for='Amount of Joints', text='5')

    block = mt.create_block(name = name, icon = 'Chain',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]

    cmds.select(cl=True)

    joints =[]
    jnt=None
    for i in range(int(amount)):
        parent = jnt
        jnt = mt.create_joint_guide(name=name+'_'+letters[i]+nc['guide'])
        cmds.move(i,0,0)
        if parent:
            cmds.parent(jnt, parent)
        joints.append(jnt)

    cmds.parent(joints[0], block)
    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_chain_block()

#-------------------------

def build_chain_block():

    print('Start of build chain func')

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guides = cmds.listRelatives(block, c=True)
    name = block.replace(nc['module'],'')

    clean_ctrl_grp = cmds.group(em=True, name=name + nc['ctrl'] + nc['group'])
    clean_rig_grp = cmds.group(em=True, name=name + '_Rig' + nc['group'])

    cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
    cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])

    for guide in guides:

        new_guide = mt.duplicate_and_remove_guides(guide)
        guide_childs=cmds.listRelatives(new_guide, ad=True)
        if guide_childs:
            all_guides = [new_guide]+guide_childs
        else:
            all_guides = [new_guide]



        if not new_guide.startswith(nc['left']) and cmds.getAttr('{}.Mirror'.format(config)):
            name = nc['left'] + name
            new_guide = nc['left'] + new_guide
            for guide in all_guides:
                guide = cmds.rename(guide, nc['left'] + guide)

        to_build = [new_guide]

        if cmds.getAttr('{}.Mirror'.format(config)):

            right_guide = cmds.mirrorJoint(new_guide, mirrorYZ = True, mirrorBehavior=True, searchReplace = (nc['left'],nc['right']))[0]
            #right_guide = mt.duplicate_change_names(input=new_guide, hi=True, search=nc['left'], replace=nc['right'])[0]
            #mt.orient_joint(input=right_guide)
            to_build.append(right_guide)


        for guide in to_build:
            guide_childs_build=cmds.listRelatives(guide, ad=True)
            if guide_childs_build:
                guide_hierarchy = [guide] + list(reversed(guide_childs_build))
            else:
                guide_hierarchy = [guide]
            cmds.select(guide_hierarchy)

            color = cmds.getAttr('{}.CtrlColor'.format(config), asString=True)
            is_right_side = guide.startswith(nc['right'])
            # if mirror is set, ignore ctrlColor attr and use default side colors
            if cmds.getAttr('{}.Mirror'.format(config)):
                if guide.startswith(nc['left']):
                    color = setup['left_color']
                elif is_right_side:
                    color = setup['right_color']



            fk_system = mt.fk_chain(input='',
                                    size=cmds.getAttr('{}.CtrlSize'.format(config)),
                                    color=color,
                                    curve_type=cmds.getAttr('{}.CtrlType'.format(config), asString=True),
                                    scale=True,
                                    twist_axis=cmds.getAttr('{}.TwistAxis'.format(config), asString=True),
                                    world_orient=False)

            if is_right_side:
                name = name.replace(nc['left'], nc['right'])

            #clean a bit

            ctrl_root = cmds.listRelatives(fk_system[0], p=1)[0]
            cmds.parent(ctrl_root, clean_ctrl_grp)
            print('fk system = {}'.format(fk_system))
            cmds.parent(guide, clean_rig_grp)

            #use this locator in case parent is set to new locator
            if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
                loc_name = '{}'.format(str(block).replace(nc['module'],'_Parent' + nc['locator']))
                if is_right_side:
                    #print(' loc for right side')
                    loc_name = loc_name.replace(nc['left'], nc['right'])

                block_parent = cmds.spaceLocator( n = loc_name)
                cmds.parentConstraint(block_parent, ctrl_root, maintainOffset=1)
            else:
                block_parent = cmds.getAttr('{}.SetParent'.format(config))
                if is_right_side:
                    block_parent = block_parent.replace(nc['left'], nc['right'])
                cmds.parentConstraint(block_parent, ctrl_root, maintainOffset=1)


            # auto rotate

            if cmds.getAttr('{}.AutoRotate'.format(config)):
                mt.create_auto_rotate_fk(fk_system[0], ctrl_root, cmds.getAttr('{}.CtrlSize'.format(config)))

            # bind joints
            bind_joints = []
            for i, joint in enumerate(guide_hierarchy):
                bind_joint = cmds.duplicate(joint, n=joint.replace(nc['joint'], nc['joint_bind']), parentOnly=1)[0]
                cmds.parentConstraint(joint, bind_joint)
                cmds.scaleConstraint(joint, bind_joint)
                bind_joints.append(bind_joint)
                if i > 0:
                    cmds.parent(bind_joint, bind_joints[i-1])


            bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])
            if cmds.objExists(bind_jnt_grp):
                cmds.parent(bind_joints[0], bind_jnt_grp)

            print ('Build {} Success'.format(block))


#build_chain_block()
