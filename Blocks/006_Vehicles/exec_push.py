from __future__ import absolute_import, division
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
PYBLOCK_NAME = 'exec_push'

#---------------------------------------------

def create_push_block(name = 'Push'):

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

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '13_Push.json')
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

    block = mt.create_block(name = name, icon = 'Push',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]
      
    #cmds.getAttr('{}.AttrName'.format(config)) #get attrs from config
    #cmds.getAttr('{}.AttrName'.format(config), asString = True) #for enums
    #joint_one = mt.create_joint_guide(name = name) #guide base with shapes

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_push_block()

#-------------------------

def build_push_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    name = block.replace(nc['module'],'')

    # use this locator in case parent is set to new locator
    if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
        block_parent = cmds.spaceLocator(n='{}'.format(str(block).replace(nc['module'], '_Parent' + nc['locator'])))
    else:
        block_parent = cmds.getAttr('{}.SetParent'.format(config))

    #get data
    wheel_geo = cmds.getAttr('{}.SetWheelGeo'.format(config))
    # create lattice
    if ',' in wheel_geo:
        wheel_geo = wheel_geo.split(',')
    cmds.select(wheel_geo)

    #Do lattice

    lattice_deformer = cmds.lattice(divisions=(2, 5, 2), objectCentered=True, ldv=(2, 2, 2), ol=False,
                                    n='{}_Lat_'.format(name), outsideLattice=1)

    cmds.setAttr('{}.outsideLattice'.format(lattice_deformer[0]), 1)
    cmds.select('{}.pt[0:1][0][0]'.format(lattice_deformer[1]),'{}.pt[0:1][0][1]'.format(lattice_deformer[1]))

    #clusters and stuff
    lat_cluster = cmds.cluster(n='{}{}'.format(name,nc['cluster']))[1]

    #create ctrl for lattice
    if name.startswith(nc['right']):
        color = 'red'
    elif name.startswith(nc['left']):
        color = 'blue'
    else:
        color = 'yellow'

    size = cmds.getAttr('{}.scaleY'.format(lattice_deformer[1]))

    ctrl = mt.curve(input=lat_cluster,
                    type='square',
                    rename=True,
                    custom_name=True,
                    name=lat_cluster.replace(nc['cluster'], '') + nc['ctrl'],
                    size=size/2)

    mt.assign_color(color=color)
    root_grp = mt.root_grp()[0]
    mt.match(root_grp, lat_cluster, r=True, t=True)

    cmds.connectAttr('{}.translate'.format(ctrl),
                     '{}.translate'.format(lat_cluster))
    cmds.connectAttr('{}.rotate'.format(ctrl),
                     '{}.rotate'.format(lat_cluster))
    cmds.connectAttr('{}.scale'.format(ctrl),
                     '{}.scale'.format(lat_cluster))

    cmds.parentConstraint(block_parent, root_grp, mo=True)

    #Clean
    clean_ctrl_grp = cmds.group(em=True, name = name + nc['ctrl'] + nc['group'])
    clean_rig_grp = cmds.group(em=True, name = name + '_Rig' + nc['group'])
    cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
    cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])

    cmds.parent(lat_cluster, clean_rig_grp)
    cmds.parent(lattice_deformer, clean_rig_grp)

    cmds.parent(root_grp, clean_ctrl_grp)

#build_push_block()
