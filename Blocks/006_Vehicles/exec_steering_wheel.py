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

#------------------------------------------------------------

TAB_FOLDER = '006_Vehicles'
PYBLOCK_NAME = 'exec_steering_wheel'

#------------------------------------------------------------

def create_steering_wheel_block(name='SteeringWheel'):
    
    # PATH = os.path.dirname(__file__)
    # PATH = Path(PATH)
    # PATH_PARTS = PATH.parts[:-2]
    # FOLDER = ''
    # for f in PATH_PARTS:
    #     FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '02_SteeringWheel.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()

    # check name and create block

    name = mt.ask_name(text=name)
    if cmds.objExists('{}{}'.format(name, nc['module'])):
        cmds.warning('Name already exists')
        return

    steering_wheel_block, steering_wheel_config = mt.create_block(
        name=name, 
        icon='SteeringWheel',
        attrs=module['attrs'], 
        build_command=module['build_command'],
        import_command=module['import'],
        )

    cmds.select(clear=1)
    steering_wheel_guide = mt.create_joint_guide(name=name)
    steering_wheel_end_guide = mt.create_joint_guide(name=name+'End')
    cmds.move(0, 5, -5)
    cmds.parent(steering_wheel_end_guide, steering_wheel_guide)
    cmds.parent(steering_wheel_guide, steering_wheel_block)
    
    cmds.select(steering_wheel_block)

    mt.orient_joint(input=steering_wheel_guide)
    

    print("Steering_wheel guides imported successfully")

def build_steering_wheel_block():
    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guide = cmds.listRelatives(block, c=1)[0]

    # orient joint

    mt.orient_joint(input=guide)
    new_guide = mt.duplicate_and_remove_guides(guide)
    
    clean_rig_grp = ''
    clean_ctrl_grp = ''

    # build

    block_parent = cmds.getAttr('{}.SetParent'.format(config))

    if block_parent == 'new_locator':
        block_parent = cmds.spaceLocator(n='{}'.format(str(new_guide).replace(nc['joint'], '_Parent' + nc['locator'])))

    ctrl_color = cmds.getAttr('{}.CtrlColor'.format(config), asString=1)
    ctrl_size = cmds.getAttr('{}.CtrlSize'.format(config))
    ctrl_curve_type = cmds.getAttr('{}.CtrlType'.format(config), asString=1)

    cmds.select(new_guide)
    fk_chain = mt.fk_chain(
        input='',
        size=ctrl_size,
        color=ctrl_color,
        curve_type=ctrl_curve_type
    )
    fk_parent = cmds.listRelatives(fk_chain[0], p=1)
    mt.hide_attr(fk_chain[0], s=1, t=1)

    cmds.parentConstraint(block_parent, fk_parent, mo=1)
    clean_rig_grp = new_guide
    clean_ctrl_grp = fk_parent

    # create bind joints

    cmds.select(cl=1)
    bind_joint = cmds.joint(n=new_guide.replace(nc['joint'], nc['joint_bind']))
    cmds.makeIdentity(bind_joint, a=1, t=1, r=1, s=1)
    cmds.parentConstraint(new_guide, bind_joint, mo=False)
    cmds.scaleConstraint(new_guide, bind_joint, mo=False)
    cmds.setAttr('{}.segmentScaleCompensate'.format(bind_joint), 0)
    cmds.setAttr('{}.inheritsTransform'.format(bind_joint), 0)

    try:
        cmds.parent(bind_joint, w=1)
    except:
        pass
    
    cmds.setAttr('{}.radius'.format(bind_joint), 1.5)

    # clean

    bind_joint_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])
    if cmds.objExists(bind_joint_grp):
        cmds.parent(bind_joint, bind_joint_grp)

    # clean ctrls
    cmds.parent(clean_ctrl_grp, 'Rig_Ctrl_Grp')

    # clean rig
    misc_grp = '{}{}'.format(setup['rig_groups']['misc'], nc['group'])
    cmds.parent(clean_rig_grp, misc_grp)
    
    # scale
    cmds.scaleConstraint('Global_Ctrl', clean_rig_grp, mo=1)