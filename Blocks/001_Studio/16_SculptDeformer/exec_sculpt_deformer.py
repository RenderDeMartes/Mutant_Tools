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

TAB_FOLDER = '001_Studio'
PYBLOCK_NAME = 'exec_sculpt_deformer'

#---------------------------------------------

def create_sculpt_deformer_block(name='SculptDeformer'):

    # Read name conventions as nc[''] and setup as setup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-3]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '16_SculptDeformer.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()
    # name checks and block creation
    name = mt.ask_name(text=module['Name'])
    if cmds.objExists('{}{}'.format(name, nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name=name, icon='SculptDeformer', attrs=module['attrs'], build_command=module['build_command'], import_command=module['import'])
    config = block[1]
    block = block[0]

    # Create two guide locators under the block
    sculptor_loc = cmds.spaceLocator(n=name + '_Sculptor' + nc['locator'])[0]
    cmds.parent(sculptor_loc, block)

    stretch_origin_loc = cmds.spaceLocator(n=name + '_StretchOrigin' + nc['locator'])[0]
    cmds.parent(stretch_origin_loc, block)
    cmds.setAttr(stretch_origin_loc + '.ty', -2)

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_sculpt_deformer_block()

#-------------------------

def build_sculpt_deformer_block(force=False):

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]

    # Check if this block should run after the full build completes
    run_after = False
    if cmds.attributeQuery('RunAfterBuild', n=config, exists=True):
        run_after = cmds.getAttr('{}.RunAfterBuild'.format(config))

    if run_after and not force:
        print('SculptDeformer block {} deferred to run after build completes'.format(block))
        return

    name = block.replace(nc['module'], '')
    size = cmds.getAttr('{}.CtrlSize'.format(config))
    color = cmds.getAttr('{}.CtrlColor'.format(config), asString=True)

    try:
        mirror_mode = cmds.getAttr('{}.Mirror'.format(config), asString=True)
    except:
        mirror_mode = 'False'

    # Parse scale values
    try:
        scale_attr = cmds.getAttr('{}.Scale'.format(config), asString=True)
        scale_values = [float(v.strip()) for v in scale_attr.split(',')]
        if len(scale_values) != 3:
            scale_values = [10, 1, 10]
    except:
        scale_values = [10, 1, 10]

    # Force left naming when mirroring to match the rest of the blocks workflow.
    if mirror_mode in ('True', 'Right_Only') and not name.startswith(nc['left']) and not name.startswith(nc['right']):
        name = nc['left'] + name

    left_name = name
    right_name = name.replace(nc['left'], nc['right'], 1) if name.startswith(nc['left']) else nc['right'] + name

    # Find guide locators under the block
    children = cmds.listRelatives(block, c=True, fullPath=True, type='transform') or []
    sculptor_guide = None
    stretch_origin_guide = None
    for child in children:
        shapes = cmds.listRelatives(child, s=True, type='locator')
        if shapes:
            short_name = child.split('|')[-1]
            if '_Sculptor' in short_name:
                sculptor_guide = child
            elif '_StretchOrigin' in short_name:
                stretch_origin_guide = child

    # Duplicate guides for building
    build_sculptor = cmds.duplicate(sculptor_guide, n='{}SculptBuildSculptor{}'.format(left_name, nc['locator']))[0]
    build_stretch = cmds.duplicate(stretch_origin_guide, n='{}SculptBuildStretch{}'.format(left_name, nc['locator']))[0]
    cmds.parent(build_sculptor, w=True)
    cmds.parent(build_stretch, w=True)

    to_build = [{'sculptor': build_sculptor, 'stretch': build_stretch, 'side': 'left'}]

    if mirror_mode == 'Right_Only':
        # Mirror the source guides to the right side
        sculptor_mirror_grp = mt.mirror_group(build_sculptor, world=True)
        cmds.makeIdentity(sculptor_mirror_grp, a=True, t=True, r=True, s=True)
        cmds.parent(build_sculptor, w=True)
        cmds.delete(sculptor_mirror_grp)

        stretch_mirror_grp = mt.mirror_group(build_stretch, world=True)
        cmds.makeIdentity(stretch_mirror_grp, a=True, t=True, r=True, s=True)
        cmds.parent(build_stretch, w=True)
        cmds.delete(stretch_mirror_grp)

        try:
            if nc['left'] in build_sculptor:
                build_sculptor = cmds.rename(build_sculptor, build_sculptor.replace(nc['left'], nc['right'], 1))
            if nc['left'] in build_stretch:
                build_stretch = cmds.rename(build_stretch, build_stretch.replace(nc['left'], nc['right'], 1))
        except:
            pass

        to_build = [{'sculptor': build_sculptor, 'stretch': build_stretch, 'side': 'right'}]

    elif mirror_mode == 'True':
        right_sculptor = mt.duplicate_change_names(input=build_sculptor, hi=True, search=nc['left'], replace=nc['right'])[0]
        right_stretch = mt.duplicate_change_names(input=build_stretch, hi=True, search=nc['left'], replace=nc['right'])[0]
        to_build.append({'sculptor': right_sculptor, 'stretch': right_stretch, 'side': 'right'})

    # Get parent config
    parent_attr = cmds.getAttr('{}.SetParent'.format(config))

    # Get geo config
    geos_attr = cmds.getAttr('{}.SetGeo'.format(config), asString=True)

    for side_data in to_build:

        side_sculptor = side_data['sculptor']
        side_stretch = side_data['stretch']
        is_right_side = side_data['side'] == 'right'
        side_name = right_name if is_right_side else left_name

        # Resolve parent for this side
        side_parent = parent_attr
        if is_right_side and nc['left'] in str(side_parent):
            side_parent = side_parent.replace(nc['left'], nc['right'], 1)

        if side_parent == 'new_locator':
            block_parent = cmds.spaceLocator(n='{}_Parent{}'.format(side_name, nc['locator']))[0]
        else:
            block_parent = side_parent

        # Resolve geo names for this side
        if geos_attr:
            if ',' in geos_attr:
                geos = [g.strip() for g in geos_attr.split(',') if g.strip()]
            else:
                geos = [geos_attr.strip()]
        else:
            geos = []

        if is_right_side:
            geos = [g.replace(nc['left'], nc['right'], 1) if nc['left'] in g else g for g in geos]

        # Create controller at sculptor position
        sculpt_ctrl = mt.curve(input=side_sculptor,
                               type='cube',
                               rename=True,
                               custom_name=True,
                               name=side_name + nc['ctrl'],
                               size=size)
        mt.assign_color(color=color)

        # Add Maximum Displacement and Dropoff Distance attributes to the controller
        cmds.addAttr(sculpt_ctrl, ln='maxDisplacement', nn='Maximum Displacement', at='double', dv=1.0, k=True)
        cmds.addAttr(sculpt_ctrl, ln='dropoffDistance', nn='Dropoff Distance', at='double', dv=1.0, k=True)

        cmds.delete(cmds.parentConstraint(side_sculptor, sculpt_ctrl))
        sculpt_ctrl_root, sculpt_ctrl_auto = mt.root_grp(input=sculpt_ctrl, autoRoot=True)


        # Create locators driven by the controller (names differ from guide locators to avoid DAG collision)
        sculptor_loc = cmds.spaceLocator(n=side_name + '_SculptPosition' + nc['locator'])[0]
        sculptor_loc_root, sculptor_loc_auto = mt.root_grp(input=sculptor_loc, autoRoot=True)
        cmds.delete(cmds.pointConstraint(side_sculptor, sculptor_loc_root))

        # Mirror the locator position for the right side (guides are duplicated at left pos)
        if is_right_side and mirror_mode == 'True':
            pos = cmds.xform(sculptor_loc_root, q=True, ws=True, t=True)
            cmds.xform(sculptor_loc_root, ws=True, t=[-pos[0], pos[1], pos[2]])



        # Create the sculpt deformer on the target geometry (single shared deformer)
        sculpt_sphere = None
        if geos:
            existing_geos = [g for g in geos if cmds.objExists(g)]
            if existing_geos:
                sculpt_result = cmds.sculpt(*existing_geos,
                                            n=side_name + '_Sculpt',
                                            mode='stretch')
                sculpt_node = sculpt_result[0]
                sculpt_sphere = sculpt_result[1]

                # Connect controller attributes to drive the sculpt deformer node attributes
                cmds.connectAttr('{}.maxDisplacement'.format(sculpt_ctrl), '{}.maximumDisplacement'.format(sculpt_node))
                cmds.connectAttr('{}.dropoffDistance'.format(sculpt_ctrl), '{}.dropoffDistance'.format(sculpt_node))

                # Parent the sculpt sphere under the sculptor locator so it follows
                # the ctrl through DAG hierarchy (avoids constraint conflicts)
                cmds.parent(sculpt_sphere, sculptor_loc)
                cmds.setAttr('{}.translate'.format(sculpt_sphere), 0, 0, 0, type='double3')
                cmds.setAttr('{}.rotate'.format(sculpt_sphere), 0, 0, 0, type='double3')

                # Apply scale values to the sculpt sphere
                cmds.setAttr('{}.scaleX'.format(sculpt_sphere), scale_values[0])
                cmds.setAttr('{}.scaleY'.format(sculpt_sphere), scale_values[1])
                cmds.setAttr('{}.scaleZ'.format(sculpt_sphere), scale_values[2])

                # Find Maya's auto-created stretch origin locator and position it at the guide
                # Maya names it <sculpt_node>StretchOrigin
                stretch_origin_name = sculpt_node + 'StretchOrigin'
                if cmds.objExists(stretch_origin_name):
                    cmds.delete(cmds.pointConstraint(side_stretch, stretch_origin_name, mo=False))
                    # Mirror stretch origin X for right side
                    if is_right_side and mirror_mode == 'True':
                        spos = cmds.xform(stretch_origin_name, q=True, ws=True, t=True)
                        cmds.xform(stretch_origin_name, ws=True, t=[-spos[0], spos[1], spos[2]])
                    cmds.parent(stretch_origin_name, sculptor_loc)
                    cmds.setAttr('{}.v'.format(stretch_origin_name), 0)

                # Hide the sculpt sphere shape
                cmds.setAttr('{}.v'.format(sculpt_sphere), 0)
            else:
                cmds.warning('SculptDeformer: No valid geometry found for side {}'.format(side_name))
        else:
            cmds.warning('SculptDeformer: No geometry specified for {}'.format(side_name))

        # Create rig and ctrl groups
        clean_rig_grp = cmds.group(n=side_name + '_Rig' + nc['group'], em=True)
        clean_ctrl_grp = cmds.group(n=side_name + '_Ctrl' + nc['group'], em=True)

        cmds.parent(sculpt_ctrl_root, clean_ctrl_grp)

        # For right side: mirror the ctrl hierarchy
        if mirror_mode in ('True', 'Right_Only') and is_right_side:
            clean_ctrl_grp = mt.mirror_group(input=clean_ctrl_grp, world=True)

        # Connect control to sculptor locator (after mirror so mo=True offset is correct)
        cmds.parentConstraint(sculpt_ctrl, sculptor_loc_root, mo=True)
        cmds.scaleConstraint(sculpt_ctrl, sculptor_loc_root, mo=True)

        # Parent locators into rig group
        cmds.parent(sculptor_loc_root, clean_rig_grp)


        # Parent constrain to block parent
        if cmds.objExists(str(block_parent)):
            cmds.parentConstraint(block_parent, clean_ctrl_grp, mo=True)
            cmds.parentConstraint(block_parent, clean_rig_grp, mo=True)

        # Parent into base groups
        cmds.parent(clean_rig_grp, '{}{}'.format(setup['rig_groups']['misc'], nc['group']))
        cmds.parent(clean_ctrl_grp, setup['base_groups']['control'] + nc['group'])

        # Clean up
        cmds.setAttr('{}.v'.format(sculptor_loc), 0)


        if cmds.objExists('Global_Ctrl'):
            cmds.scaleConstraint('Global_Ctrl', sculpt_ctrl_root, mo=True)
            cmds.scaleConstraint('Global_Ctrl', sculptor_loc_root, mo=True)


    # Remove temporary duplicated guides
    for side_data in to_build:
        for key in ('sculptor', 'stretch'):
            guide = side_data[key]
            if cmds.objExists(guide):
                try:
                    cmds.delete(guide)
                except:
                    pass

    print('Build {} Success'.format(block))

#build_sculpt_deformer_block()
