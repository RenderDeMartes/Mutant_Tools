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
PYBLOCK_NAME = 'exec_multibone'

#---------------------------------------------

def create_multibone_block(name = 'MultiBone'):

    #---------------------------------------------------
    #---------------------------------------------------
    #---------------------------------------------------


    # Read name conventions as nc[''] and setup as seup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-2]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '10_MultiBone.json')
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

    amount = mt.ask_name(text=1, ask_for='Amount')

    block = mt.create_block(name = name, icon = 'MultiBone',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]

    alphabet = string.ascii_uppercase
    x_pos = 0
    for num in range(int(amount)):
        cmds.select(cl=True)
        guide = mt.create_joint_guide(name=name+'_'+alphabet[num])
        cmds.move(x_pos,0,0)
        cmds.parent(guide,block)
        x_pos = x_pos+1

    print('{} Created Successfully'.format(name))

#create_multibone_block()

#-------------------------

def build_multibone_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guides = cmds.listRelatives(block, c=True)
    name = block.replace(nc['module'],'')


    #cmds.getAttr('{}.AttrName'.format(config))
    #cmds.getAttr('{}.AttrName'.format(config), asString = True)

    #orient the joints

    #use this locator in case parent is set to new locator
    if cmds.getAttr('{}.SetParents'.format(config)) == 'new_locator':
        block_parents = cmds.spaceLocator( n = '{}'.format(str(block).replace(nc['module'],'_Parent' + nc['locator'])))
    else:
        block_parents = cmds.getAttr('{}.SetParents'.format(config))

    #clean a bit
    clean_ctrl_grp = cmds.group(em=True, name = name + nc['ctrl'] + nc['group'])
    clean_rig_grp = cmds.group(em=True, name = name + '_Rig' + nc['group'])

    cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
    cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])

    bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])

    for num, guide in enumerate(guides):

        bone = mt.duplicate_and_remove_guides(guide)
        print(bone)

        if block_parents == 'new_locator_each':
            block_parent = cmds.spaceLocator( n = '{}'.format(str(block).replace(nc['module'],'_Parent' + nc['locator'])))
        elif block_parents == 'new_locator':
            block_parent = block_parents
        else:
            block_parent = block_parents.replace(' ', '').split(',')

        size = cmds.getAttr('{}.CtrlSize'.format(config))
        ctrl_type = cmds.getAttr('{}.CtrlType'.format(config), asString=True)
        ctrl_color = cmds.getAttr('{}.CtrlColor'.format(config), asString=True)
        ctrl = mt.curve(input=bone,
                        type=ctrl_type,
                        rename=True,
                        custom_name=True,
                        name=bone.replace(nc['joint'], nc['ctrl']),
                        size=size)
        cmds.delete(cmds.parentConstraint(bone, ctrl))
        mt.assign_color(color=ctrl_color)
        root_grp = mt.root_grp()[0]
        cmds.parentConstraint(ctrl, bone, mo=True)
        cmds.scaleConstraint(ctrl, bone, mo=True)

        cmds.parent(root_grp, clean_ctrl_grp)
        cmds.parent(bone, clean_rig_grp)

        cmds.select(cl=True)
        bind_joint = cmds.joint(n=bone.replace(nc['joint'], nc['joint_bind']))
        cmds.parentConstraint(bone, bind_joint)
        cmds.scaleConstraint(bone, bind_joint)
        cmds.setAttr('{}.radius'.format(bind_joint), 1.5)
        cmds.parent(bind_joint, bind_jnt_grp)

        #parent
        if block_parents == 'new_locator_each':
            cmds.parentConstraint(block_parent, root_grp, mo=True)
            cmds.scaleConstraint(block_parent, root_grp, mo=True)
        elif block_parents == 'new_locator':
            cmds.parentConstraint(block_parent, root_grp, mo=True)
            cmds.scaleConstraint(block_parent, root_grp, mo=True)
        else:
            cmds.parentConstraint(block_parent, root_grp, mo=True)
            cmds.scaleConstraint(block_parent, root_grp, mo=True)

    print ('Build {} Success'.format(block))



#build_multibone_block()
