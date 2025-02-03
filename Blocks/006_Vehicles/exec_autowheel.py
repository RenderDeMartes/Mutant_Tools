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

TAB_FOLDER = '006_Vehicles'
PYBLOCK_NAME = 'exec_autowheel'

#---------------------------------------------

def create_autowheel_block(name = 'AutoWheel'):

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

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '10_AutoWheel.json')
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

    block = mt.create_block(name = name, icon = 'AutoWheel',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]
      
    #cmds.getAttr('{}.AttrName'.format(config)) #get attrs from config
    #cmds.getAttr('{}.AttrName'.format(config), asString = True) #for enums
    #joint_one = mt.create_joint_guide(name = name) #guide base with shapes

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_autowheel_block()

#-------------------------

def build_autowheel_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    name = block.replace(nc['module'],'')


    #cmds.getAttr('{}.AttrName'.format(config))
    #cmds.getAttr('{}.AttrName'.format(config), asString = True)

    #Gather data
    auto_mover_controllers = cmds.getAttr('{}.SetMoverCtrls'.format(config)).replace(' ', '').split(',')
    if not auto_mover_controllers:
        cmds.error('No ctrls selected for the auto rotate wheels')
    wheels_ctrls = cmds.getAttr('{}.SetWheelsName'.format(config)).replace(' ', '').split(',')

    #Create shared locator and proxy new attrs on all ctrls [speed, on/off]
    #Shared loc
    attrs = ['AutoWheel', 'Speed']
    for ctrl in auto_mover_controllers:
        cmds.select(ctrl)
        if cmds.objectType(ctrl) == 'transform':
            attrs_loc = mt.shape_with_attr(input='', obj_name='{}_Attrs'.format(name), attr_name='').split('.')[0]

    auto_attr = mt.new_attr(input=attrs_loc, name=attrs[0], min=0, max=1, default=1)
    speed_attr = mt.new_attr(input=attrs_loc, name=attrs[1], min=0, max=10000, default=1)

    for ctrl in auto_mover_controllers:
        mt.proxy_this_attrs(attrs_from=attrs_loc, attrs_to=ctrl, attrs_to_proxy=attrs)


    for wheel_ctrl in wheels_ctrls:
        for move_ctrl in auto_mover_controllers:
            # Connect attrs with md inbetween, connect md to attrs
            wheel_joint = wheel_ctrl.replace(nc['ctrl'], nc['joint'])

            #New grps
            speed_grp = mt.root_grp(input = wheel_joint, custom = True, custom_name = '_Speed', autoRoot = False, replace_nc = False)[0]

            # Connect autowheel with speed
            speed_md = mt.connect_md_node(in_x1="{}.translateZ".format(move_ctrl), in_x2=speed_attr, out_x='{}.rotateX'.format(speed_grp), mode='multiply')

            # Connect On/Off with md
            toggle_md = mt.connect_md_node(in_x1=auto_attr, in_x2="{}.translateZ".format(move_ctrl), out_x='{}.input1X'.format(speed_md), mode='multiply', force=True)


    print ('Build {} Success'.format(block))

#build_autowheel_block()
