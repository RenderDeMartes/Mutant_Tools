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
    size = cmds.getAttr('{}.CtrlSize'.format(config))
    color = cmds.getAttr('{}.CtrlColor'.format(config), asString=True)

    try:
        mirror_mode = cmds.getAttr('{}.Mirror'.format(config), asString=True)
    except:
        mirror_mode = 'False'

    # Force left naming when mirroring to match the rest of the blocks workflow.
    if mirror_mode in ('True', 'Right_Only') and not name.startswith(nc['left']) and not name.startswith(nc['right']):
        name = nc['left'] + name

    left_name = name
    right_name = name.replace(nc['left'], nc['right'], 1) if name.startswith(nc['left']) else nc['right'] + name

    # Build side list from duplicated guides (same as other mirrored blocks).
    build_guide_name = '{}SlideBuildGuide{}'.format(left_name, nc['locator'])
    new_guide = cmds.duplicate(guide, n=build_guide_name)[0]
    to_build = [new_guide]

    if mirror_mode == 'Right_Only':
        # Convert the source guide into right side while preserving mirror behavior.
        miror_grp = mt.mirror_group(new_guide, world=True)
        cmds.makeIdentity(miror_grp, a=True, t=True, r=True, s=True)
        cmds.parent(new_guide, w=True)
        cmds.delete(miror_grp)
        try:
            if nc['left'] in new_guide:
                new_guide = cmds.rename(new_guide, new_guide.replace(nc['left'], nc['right'], 1))
        except:
            pass
        to_build = [new_guide]

    elif mirror_mode == 'True':
        right_guide = mt.duplicate_change_names(input=new_guide, hi=True, search=nc['left'], replace=nc['right'])[0]
        to_build.append(right_guide)

    for side_guide in to_build:

        is_right_side = str(side_guide).startswith(nc['right'])
        side_name = right_name if is_right_side else left_name

        # Side-resolved config attrs
        slide_surface = cmds.getAttr('{}.SetSlideNurb'.format(config), asString=True)
        if is_right_side and nc['left'] in str(slide_surface):
            slide_surface = slide_surface.replace(nc['left'], nc['right'], 1)

        parent_attr = cmds.getAttr('{}.SetParent'.format(config))
        if is_right_side and nc['left'] in str(parent_attr):
            parent_attr = parent_attr.replace(nc['left'], nc['right'], 1)

        # Build position locator from this side guide
        position_locator = cmds.spaceLocator(n=side_name + 'SlideAim' + nc['locator'])[0]
        position_locator_root = mt.root_grp()
        cmds.delete(cmds.parentConstraint(side_guide, position_locator_root))

        if slide_surface == 'new_plane':
            slide_surface = cmds.nurbsPlane(n=side_name + nc['nurb'])[0]
            cmds.delete(cmds.parentConstraint(position_locator, slide_surface))

        if parent_attr == 'new_locator':
            block_parent = cmds.spaceLocator(n='{}_Parent{}'.format(side_name, nc['locator']))[0]
        else:
            block_parent = parent_attr

        driver_locator = cmds.spaceLocator(n=side_name + 'SlideDriver' + nc['locator'])[0]

        closest_point_on_sruface_node = cmds.createNode('closestPointOnSurface', n=side_name + '_CPOS')
        decompose_matrix = cmds.createNode('decomposeMatrix', n=side_name + '_decomposeMatrix')

        cmds.connectAttr('{}.worldSpace[0]'.format(slide_surface), '{}.inputSurface'.format(closest_point_on_sruface_node))
        cmds.connectAttr('{}.worldMatrix[0]'.format(position_locator), '{}.inputMatrix'.format(decompose_matrix))
        cmds.connectAttr('{}.outputTranslate'.format(decompose_matrix), '{}.inPosition'.format(closest_point_on_sruface_node))

        # Create controller
        slide_ctrl = mt.curve(input=position_locator,
                              type='mover',
                              rename=True,
                              custom_name=True,
                              name=side_name + nc['ctrl'],
                              size=size)
        mt.assign_color(color=color)
        cmds.delete(cmds.parentConstraint(position_locator, slide_ctrl))
        slide_ctrl_root = mt.root_grp(slide_ctrl)
        mt.hide_attr(input=slide_ctrl, s=True, r=True)

        mt.line_attr(input=slide_ctrl, name='EnableAxis', lines=10)
        blend_nodes = []
        for axis in ['X', 'Y', 'Z']:
            cmds.connectAttr('{}.rotate{}'.format(slide_ctrl, axis), '{}.rotate{}'.format(position_locator, axis), f=True)

            axis_attr = mt.new_attr(input=slide_ctrl, name=axis, min=-0, max=1, default=1)
            blend_node = cmds.shadingNode('blendColors', asUtility=True, n=slide_ctrl.replace(nc['ctrl'], nc['blend']))
            cmds.connectAttr('{}.translate{}'.format(slide_ctrl, axis), '{}.color1.color1R'.format(blend_node), f=1)
            cmds.setAttr('{}.color2.color2R'.format(blend_node), 0)
            cmds.connectAttr('{}'.format(axis_attr), '{}.blender'.format(blend_node), f=1)
            cmds.connectAttr('{}.output.outputR'.format(blend_node), '{}.translate{}'.format(position_locator, axis), f=1)
            blend_nodes.append(blend_node)

        mt.assign_color(input=driver_locator, color=color)

        # Fix Slide – build surface-following matrix
        node_pos  = cmds.shadingNode('pointOnSurfaceInfo', n=side_name + 'POS',  au=True)
        node_fbfm = cmds.shadingNode('fourByFourMatrix',   n=side_name + 'FBFM', au=True)
        node_dcm  = cmds.shadingNode('decomposeMatrix',    n=side_name + 'DCM',  au=True)

        cmds.connectAttr('{}.positionX'.format(node_pos), '{}.in30'.format(node_fbfm), f=True)
        cmds.connectAttr('{}.positionY'.format(node_pos), '{}.in31'.format(node_fbfm), f=True)
        cmds.connectAttr('{}.positionZ'.format(node_pos), '{}.in32'.format(node_fbfm), f=True)
        cmds.connectAttr('{}.normalX'.format(node_pos),   '{}.in00'.format(node_fbfm), f=True)
        cmds.connectAttr('{}.normalY'.format(node_pos),   '{}.in01'.format(node_fbfm), f=True)
        cmds.connectAttr('{}.normalZ'.format(node_pos),   '{}.in02'.format(node_fbfm), f=True)
        cmds.connectAttr('{}.tangentUx'.format(node_pos), '{}.in10'.format(node_fbfm), f=True)
        cmds.connectAttr('{}.tangentUy'.format(node_pos), '{}.in11'.format(node_fbfm), f=True)
        cmds.connectAttr('{}.tangentUz'.format(node_pos), '{}.in12'.format(node_fbfm), f=True)
        cmds.connectAttr('{}.tangentVx'.format(node_pos), '{}.in20'.format(node_fbfm), f=True)
        cmds.connectAttr('{}.tangentVy'.format(node_pos), '{}.in21'.format(node_fbfm), f=True)
        cmds.connectAttr('{}.tangentVz'.format(node_pos), '{}.in22'.format(node_fbfm), f=True)
        cmds.connectAttr('{}.output'.format(node_fbfm), '{}.inputMatrix'.format(node_dcm), f=True)

        cmds.connectAttr(closest_point_on_sruface_node + '.parameterV', node_pos + '.parameterV')
        cmds.connectAttr(closest_point_on_sruface_node + '.parameterU', node_pos + '.parameterU')
        cmds.connectAttr('{}.worldSpace'.format(slide_surface), '{}.inputSurface'.format(node_pos), f=True)

        # For right side, wrap driver_locator in a mirror group before connecting DCM
        # so the rig hierarchy sits in the correct world side from the start.
        rig_mirror_grp = None
        if mirror_mode in ('True', 'Right_Only') and is_right_side:
            rig_mirror_grp = mt.mirror_group(input=driver_locator, world=True)

        cmds.connectAttr(node_dcm + '.outputRotate',    driver_locator + '.rotate')
        cmds.connectAttr(node_dcm + '.outputTranslate', driver_locator + '.translate')


        # Parent to base
        clean_rig_grp  = cmds.group(n=side_name + '_Rig'  + nc['group'], em=True)
        clean_ctrl_grp = cmds.group(n=side_name + '_Ctrl' + nc['group'], em=True)

        cmds.parent(slide_ctrl_root, clean_ctrl_grp)
        # For right side: driver_locator is already inside rig_mirror_grp; parent that instead.

        # Mirror complete right-side ctrl hierarchy.
        if mirror_mode in ('True', 'Right_Only') and is_right_side:
            clean_ctrl_grp = mt.mirror_group(input=clean_ctrl_grp, world=True)

        if rig_mirror_grp:
            cmds.parent(position_locator_root, rig_mirror_grp, clean_rig_grp)
        else:
            cmds.parent(position_locator_root, driver_locator, clean_rig_grp)

        cmds.parentConstraint(block_parent, clean_ctrl_grp, mo=True)
        cmds.parentConstraint(block_parent, clean_rig_grp,  mo=True)

        cmds.parent(clean_rig_grp,  '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
        cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])

        # Clean
        cmds.setAttr('{}.v'.format(position_locator), 0)
        cmds.scaleConstraint('Global_Ctrl', driver_locator,        mo=True)
        cmds.scaleConstraint('Global_Ctrl', slide_ctrl_root,       mo=True)
        cmds.scaleConstraint('Global_Ctrl', position_locator,      mo=True)

    # Remove temporary duplicated guides used only for build side resolution.
    for side_guide in to_build:
        if cmds.objExists(side_guide):
            try:
                cmds.delete(side_guide)
            except:
                pass

    print('Build {} Success'.format(block))

#build_slide_block()
