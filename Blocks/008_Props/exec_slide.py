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

TAB_FOLDER = '008_Props'
PYBLOCK_NAME = 'exec_slide'

#---------------------------------------------

def create_slide_block(name = 'Slide'):

    # Read name conventions as nc[''] and setup as seup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-2]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '02_Slide.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()
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

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    guide = cmds.listRelatives(block, c=True)[0]

    name = block.replace(nc['module'], '')
    size=cmds.getAttr('{}.CtrlSize'.format(config))
    position_locator = cmds.spaceLocator(n=name+'SlideAim'+nc['locator'])[0]
    position_locator_root = mt.root_grp()
    slide_locator = position_locator
    cmds.delete(cmds.pointConstraint(guide, position_locator_root))
    slide_surface = cmds.getAttr('{}.SetSlideNurb'.format(config), asString = True)
    driver_locator = cmds.spaceLocator(n=name+'SlideDriver'+nc['locator'])[0]
    mirror_behavior = cmds.getAttr('{}.MirrorBehavior'.format(config), asString = True)
    color= cmds.getAttr('{}.CtrlColor'.format(config), asString = True)

    #use this locator in case parent is set to new locator
    if cmds.getAttr('{}.SetParent'.format(config)) == 'new_locator':
        block_parent = cmds.spaceLocator( n = '{}'.format(str(block).replace(nc['module'],'_Parent' + nc['locator'])))
    else:
        block_parent = cmds.getAttr('{}.SetParent'.format(config))

    if slide_surface == 'new_plane':
        slide_surface = cmds.nurbsPlane(n = name + nc['nurb'])[0]
        cmds.delete(cmds.parentConstraint(position_locator, slide_surface))

    closest_point_on_sruface_node = cmds.createNode('closestPointOnSurface', n= name + '_CPOS')
    decompose_matrix = cmds.createNode('decomposeMatrix', n=name+'_decomposeMatrix')

    cmds.connectAttr('{}.worldSpace[0]'.format(slide_surface), '{}.inputSurface'.format(closest_point_on_sruface_node))
    cmds.connectAttr('{}.worldMatrix[0]'.format(position_locator), '{}.inputMatrix'.format(decompose_matrix))
    cmds.connectAttr('{}.outputTranslate'.format(decompose_matrix), '{}.inPosition'.format(closest_point_on_sruface_node))
    #cmds.connectAttr('{}.result.position'.format(closest_point_on_sruface_node), '{}.translate'.format(driver_locator))

    #cmds.aimConstraint(position_locator, driver_locator, mo=True)

    #create controller
    slide_ctrl = mt.curve(input=position_locator,
                          type='mover',
                          rename=True,
                          custom_name=True,
                          name=name+nc['ctrl'],
                          size=size)
    mt.assign_color(color=color)
    cmds.delete(cmds.pointConstraint(position_locator, slide_ctrl))
    slide_ctrl_root = mt.root_grp(slide_ctrl)
    mt.hide_attr(input=slide_ctrl, s=True, r=True)

    if mirror_behavior:
        slide_ctrl_root = mt.mirror_group(input=slide_ctrl_root, world=False)

    mt.line_attr(input=slide_ctrl, name='EnableAxis', lines=10)
    blend_nodes = []
    for axis in ['X','Y','Z']:
        cmds.connectAttr('{}.rotate{}'.format(slide_ctrl, axis), '{}.rotate{}'.format(position_locator, axis), f=True)

        axis_attr = mt.new_attr(input=slide_ctrl, name=axis, min=-0, max=1, default=1)
        blend_node = cmds.shadingNode('blendColors', asUtility=True, n=slide_ctrl.replace(nc['ctrl'], nc['blend']))
        cmds.connectAttr('{}.translate{}'.format(slide_ctrl, axis), '{}.color1.color1R'.format(blend_node), f=1)
        cmds.setAttr('{}.color2.color2R'.format(blend_node), 0)
        cmds.connectAttr('{}'.format(axis_attr), '{}.blender'.format(blend_node), f=1)
        cmds.connectAttr('{}.output.outputR'.format(blend_node), '{}.translate{}'.format(position_locator, axis), f=1)
        blend_nodes.append(blend_node)

    mt.assign_color(input=driver_locator ,color=color)

    # Fix Slide
    # create 3 nodes
    node_pos = cmds.shadingNode('pointOnSurfaceInfo', n=name + 'POS', au=True)
    node_fbfm = cmds.shadingNode('fourByFourMatrix', n=name + 'FBFM', au=True)
    node_dcm = cmds.shadingNode('decomposeMatrix', n=name + 'DCM', au=True)

    cmds.connectAttr('{}.positionX'.format(node_pos), '{}.in30'.format(node_fbfm), f=True)
    cmds.connectAttr('{}.positionY'.format(node_pos), '{}.in31'.format(node_fbfm), f=True)
    cmds.connectAttr('{}.positionZ'.format(node_pos), '{}.in32'.format(node_fbfm), f=True)
    cmds.connectAttr('{}.normalX'.format(node_pos), '{}.in00'.format(node_fbfm), f=True)
    cmds.connectAttr('{}.normalY'.format(node_pos), '{}.in01'.format(node_fbfm), f=True)
    cmds.connectAttr('{}.normalZ'.format(node_pos), '{}.in02'.format(node_fbfm), f=True)
    cmds.connectAttr('{}.tangentUx'.format(node_pos), '{}.in10'.format(node_fbfm), f=True)
    cmds.connectAttr('{}.tangentUy'.format(node_pos), '{}.in11'.format(node_fbfm), f=True)
    cmds.connectAttr('{}.tangentUz'.format(node_pos), '{}.in12'.format(node_fbfm), f=True)
    cmds.connectAttr('{}.tangentVx'.format(node_pos), '{}.in20'.format(node_fbfm), f=True)
    cmds.connectAttr('{}.tangentVy'.format(node_pos), '{}.in21'.format(node_fbfm), f=True)
    cmds.connectAttr('{}.tangentVz'.format(node_pos), '{}.in22'.format(node_fbfm), f=True)
    cmds.connectAttr('{}.output'.format(node_fbfm), '{}.inputMatrix'.format(node_dcm), f=True)

    cmds.connectAttr(closest_point_on_sruface_node + '.parameterV', node_pos + '.parameterV')
    cmds.connectAttr(closest_point_on_sruface_node + '.parameterU', node_pos + '.parameterU')
    cmds.connectAttr('{}.worldSpace'.format(slide_surface),'{}.inputSurface'.format(node_pos),f=True)

    cmds.connectAttr(node_dcm + '.outputRotate', driver_locator + '.rotate')
    cmds.connectAttr(node_dcm + '.outputTranslate', driver_locator + '.translate')

    #clean
    cmds.setAttr('{}.v'.format(position_locator), 0)
    cmds.scaleConstraint('Global_Ctrl', driver_locator, mo=True)
    cmds.scaleConstraint('Global_Ctrl', slide_ctrl_root, mo=True)
    cmds.scaleConstraint('Global_Ctrl', position_locator, mo=True)

    #parent to base
    clean_rig_grp = cmds.group(n=name + '_Rig' + nc['group'], em=True)
    clean_ctrl_grp = cmds.group(n = name + '_Ctrl' + nc['group'],em=True)

    cmds.parent(slide_ctrl_root, clean_ctrl_grp)
    cmds.parent(position_locator_root, driver_locator,clean_rig_grp)

    cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
    cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])

    cmds.parentConstraint(block_parent, slide_ctrl_root, mo=True)
    cmds.parentConstraint(block_parent, position_locator_root, mo=True)

    if mirror_behavior:
        md = mt.connect_md_node(in_x1='{}.output.outputR'.format(blend_nodes[0]),in_x2=-1,out_x = '{}.translateX'.format(position_locator), mode = 'multiply', force=True)

#build_slide_block()
