from maya import cmds
import json
import imp
import os
from pathlib import Path

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
imp.reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()

#---------------------------------------------

TAB_FOLDER = '06_Props'
PYBLOCK_NAME = 'exec_slide'

#Read name conventions as nc[''] and setup as seup['']
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

MODULE_FILE = os.path.join(os.path.dirname(__file__),'02_Slide.json')
with open(MODULE_FILE) as module_file:
	module = json.load(module_file)

#---------------------------------------------

def create_slide_block(name = 'Slide'):

    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name = name, icon = 'Down',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    config = block[1]
    block = block[0]
      
    #cmds.getAttr('{}.AttrName'.format(config)) #get attrs from config
    #cmds.getAttr('{}.AttrName'.format(config), asString = True) #for enums
    #joint_one = mt.create_joint_guide(name = name) #guide base with shapes

    loc = cmds.spaceLocator(n=name+'_SlidePosition'+nc['locator'])
    cmds.parent(loc, block)
    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_slide_block()

#-------------------------

def build_slide_block():

    mt.check_is_there_is_base()


    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guide = cmds.listRelatives(block, c=True)[0]

    name = block.replace(nc['module'], '')
    size=cmds.getAttr('{}.CtrlSize'.format(config))
    position_locator = cmds.spaceLocator(n=name+'SlideAim'+nc['locator'])[0]
    cmds.delete(cmds.parentConstraint(guide, position_locator))
    slide_surface = cmds.getAttr('{}.SetSlideNurb'.format(config), asString = True)
    driver_locator = cmds.spaceLocator(n=name+'SlideDriver'+nc['locator'])[0]
    mirror_behavior = cmds.getAttr('{}.MirrorBehavior'.format(config), asString = True)
    color= cmds.getAttr('{}.CtrlColor'.format(config), asString = True)

    if slide_surface == 'new_plane':
        slide_surface = cmds.nurbsPlane(n = name + nc['nurb'])[0]
        cmds.delete(cmds.parentConstraint(position_locator, slide_surface))

    closest_point_on_sruface_node = cmds.createNode('closestPointOnSurface', n= name + '_CPOS')
    decompose_matrix = cmds.createNode('decomposeMatrix', n=name+'_decomposeMatrix')

    cmds.connectAttr('{}.worldSpace[0]'.format(slide_surface), '{}.inputSurface'.format(closest_point_on_sruface_node))
    cmds.connectAttr('{}.worldMatrix[0]'.format(position_locator), '{}.inputMatrix'.format(decompose_matrix))
    cmds.connectAttr('{}.outputTranslate'.format(decompose_matrix), '{}.inPosition'.format(closest_point_on_sruface_node))
    cmds.connectAttr('{}.result.position'.format(closest_point_on_sruface_node), '{}.translate'.format(driver_locator))

    cmds.aimConstraint(position_locator, driver_locator, mo=True)

    #create controller
    slide_ctrl = mt.curve(input=position_locator,
                          type='mover',
                          rename=True,
                          custom_name=True,
                          name=name+nc['ctrl'],
                          size=size)
    mt.assign_color(color=color)
    slide_ctrl_root = mt.root_grp(slide_ctrl)

    if mirror_behavior:
        mt.mirror_group(world=False)

    cmds.parentConstraint(slide_ctrl, position_locator,mo=True)
    mt.assign_color(input=driver_locator ,color=color)

    #clean
    cmds.setAttr('{}.v'.format(position_locator), 0)

    #parent to base
    clean_rig_grp = cmds.group(n=name + '_Rig' + nc['group'], em=True)
    clean_ctrl_grp = cmds.group(n = name + '_Ctrl' + nc['group'],em=True)

    cmds.parent(slide_ctrl_root, clean_ctrl_grp)
    cmds.parent(position_locator, driver_locator,clean_rig_grp)

    cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
    cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])


#build_slide_block()
