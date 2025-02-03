from __future__ import absolute_import
from maya import cmds, mel
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
TAB_FOLDER = '003_Facial'
PYBLOCK_NAME = 'exec_orbicularis'

#Read name conventions as nc[''] and setup as seup['']
PATH = os.path.dirname(__file__)
PATH = Path(PATH)
PATH_PARTS = PATH.parts[:-2]
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

MODULE_FILE = os.path.join(os.path.dirname(__file__),'013_Orbicularis.json')
with open(MODULE_FILE) as module_file:
	module = json.load(module_file)

#---------------------------------------------

def create_orbicularis_block(name = 'L_Orbicularis'):

    nc, curve_data, setup = mt.import_configs()
    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name = name, icon = 'Orbicularis',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]
    name = block.replace(nc['module'],'')

    cmds.select(cl=True)
    cv =mt.curve(input='',
                type='circleZ',
                rename=True,
                custom_name=True,
                name=name+nc['guide'],
                size=1)
    mt.assign_color(color='purple')
    cmds.parent(cv, block)
    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_orbicularis_block()

#-------------------------

def build_orbicularis_block():

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guide = cmds.listRelatives(block, c=True)[0]
    name = block.replace(nc['module'], '')

    #orient the joints
    if name.startswith(nc['left']) or name.startswith(nc['right']):
        left_guide = cmds.duplicate(guide, n=name+nc['curve'])[0]
        right_guide = cmds.duplicate(guide, n=name.replace(nc['left'],nc['right'])+nc['curve'])[0]
        to_build = [left_guide, right_guide]
        cmds.parent(left_guide, w=True)
        cmds.parent(right_guide, w=True)

    else:
        guide = cmds.duplicate(guide, n=name + nc['curve'])[0]
        cmds.parent(guide, w=True)
        to_build = [guide]

#build ------------------------------------------------------
    for side_guide in to_build:

        #use this locator in case parent is set to new locator
        if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
            block_parent = cmds.spaceLocator( n = '{}'.format(str(side_guide).replace(nc['curve'],'_Parent' + nc['locator'])))
        else:
            block_parent = cmds.getAttr('{}.SetParent'.format(config))
            if side_guide.startswith(nc['right']):
                block_parent = block_parent.replace(nc['left'],nc['right'])

        #smart select the colors
        if str(side_guide).startswith(nc['left']):
            color = setup['left_color']
        elif str(side_guide).startswith(nc['right']):
            color = setup['right_color']       
        else:
            color = setup['main_color']       

        geo = cmds.getAttr('{}.SetGeo'.format(config))

        #main funcion -------------------------------------------

        #Flip side guide
        if side_guide.startswith(nc['right']):
            grp = mt.mirror_group(side_guide, world = True)
            cmds.parent(side_guide, w=True)
            cmds.delete(grp)
            name = name.replace(nc['left'], nc['right'])

        cmds.select(side_guide)
        joints_grp = cmds.group(em=True, n='{}_{}{}'.format(name, nc['joint'], nc['group']))
        ctrl_grp = cmds.group(em=True, n='{}_{}{}'.format(name, nc['joint'], nc['group']))

        joints = []
        cvs = cmds.getAttr('{}.spans'.format(side_guide))
        for num in range(cvs):
            #Create twwek joints
            cmds.select(cl=True)
            jnt = cmds.joint(n='{}_{}{}'.format(side_guide, num, nc['joint']))
            joints.append(jnt)
            cmds.select('{}.cv[{}]'.format(side_guide, num))
            temp_cls = cmds.cluster()
            cmds.delete(cmds.parentConstraint(temp_cls, jnt))
            cmds.delete(temp_cls)
            jnt_root, jnt_auto = mt.root_grp(input=jnt, autoRoot=True)
            cmds.parent(jnt_root, joints_grp)

            ctrl = mt.curve(input=jnt,
                            type='circleZ',
                            rename=True,
                            custom_name=True,
                            name=jnt.replace(nc['joint'], nc['ctrl']),
                            size=1)

            mt.assign_color(color=color)
            root_grp, auto_grp = mt.root_grp(autoRoot=True)
            mt.match(root_grp, jnt, r=True, t=True)
            cmds.connectAttr('{}.translate'.format(ctrl), '{}.translate'.format(jnt))
            mt.hide_attr(input=ctrl, r=True, s=True, rotate_order=True)
            cmds.parent(root_grp, ctrl_grp)

        wire = cmds.wire(geo, n="{}_Wire".format(side_guide), w=side_guide)
        #cmds.setAttr('{}.dropoffDistance[0]'.format(wire[0]), 1)
        cmds.setAttr('{}.rotation'.format(wire[0]), 0)
        wire_base = wire[1] + 'BaseWire'

        cmds.select(joints, side_guide)
        cmds.skinCluster(sm=0, bm=1, tsb=True)

        #clean a bit
        clean_ctrl_grp = cmds.group(em=True, name = name + nc['ctrl'] + nc['group'])
        clean_rig_grp = cmds.group(em=True, name = name + '_Rig' + nc['group'])

        cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
        cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])
    
        cmds.parent(side_guide, wire_base, joints_grp, clean_rig_grp)
        cmds.parent(ctrl_grp, clean_ctrl_grp)

        cmds.parentConstraint(block_parent, clean_ctrl_grp, mo=True)
        cmds.scaleConstraint(block_parent, clean_ctrl_grp, mo=True)

    # build complete ----------------------------------------------------    
    print ('Build {} Success'.format(block))


#build_orbicularis_block()
