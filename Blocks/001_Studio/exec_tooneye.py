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
PYBLOCK_NAME = 'exec_tooneye'

#---------------------------------------------

def create_tooneye_block(name='ToonEye'):

    # Read name conventions as nc[''] and setup as setup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-2]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '11_ToonEye.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()

    #name checks and block creation
    name = mt.ask_name(text=module['Name'])
    if not name:
        return
    if cmds.objExists('{}{}'.format(name, nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name=name, icon=module['Icon'].replace('.png',''), attrs=module['attrs'],
                            build_command=module['build_command'],
                            import_command=module['import'])
    config = block[1]
    block = block[0]

    # Create a locator guide for positioning
    loc_guide = cmds.spaceLocator(n=name + nc['locator'])
    cmds.parent(loc_guide, block)

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_tooneye_block()

#-------------------------

def _rename_hierarchy(top_node, prefix):
    """Rename all DAG nodes under top_node (inclusive) by prepending a prefix.

    Renames bottom-up (deepest children first) to avoid DAG path invalidation.

    Args:
        top_node: The top-level group node (e.g. 'eye_grp')
        prefix: Side prefix to prepend (e.g. 'L_' or 'R_')

    Returns:
        str: The new name of the top_node after renaming.
    """
    # Get all descendants, allDescendents returns deepest first
    descendants = cmds.listRelatives(top_node, allDescendents=True, fullPath=True) or []

    # Rename children bottom-up (fullPath ensures correct targeting)
    for node in descendants:
        short_name = node.split('|')[-1]
        # Skip if already prefixed
        if not short_name.startswith(prefix):
            try:
                cmds.rename(node, prefix + short_name)
            except Exception as e:
                cmds.warning('Could not rename {}: {}'.format(short_name, str(e)))

    # Rename the top node last
    new_top = cmds.rename(top_node, prefix + top_node)
    return new_top


def _build_tooneye_side(name_prefix, loc_guide, config, nc, setup):
    """Build one side of the toon eye.

    Imports the eye rig file, renames all nodes with the given prefix,
    and positions eye_grp_OffsetCtrl at the locator guide.

    Args:
        name_prefix: Side prefix ('L_' or 'R_')
        loc_guide: Locator to match position/rotation from
        config: Config network node name
        nc: Naming conventions dict
        setup: Rig setup dict

    Returns:
        str: The top-level group name of the imported eye (after renaming).
    """
    eye_file = cmds.getAttr('{}.EyeFile'.format(config))

    if not os.path.exists(eye_file):
        cmds.warning('Eye file not found: {}'.format(eye_file))
        return None

    # Snapshot existing nodes before import
    existing_nodes = set(cmds.ls(dag=True, long=True))

    # Import the eye rig with no namespace
    cmds.file(eye_file, i=True, namespace=':', mergeNamespacesOnClash=True,
              options='v=0;', type='mayaAscii', ignoreVersion=True,
              preserveReferences=True)

    # Find newly imported nodes by diffing
    all_nodes_after = set(cmds.ls(dag=True, long=True))
    new_nodes = all_nodes_after - existing_nodes

    # Look for 'eye_grp' among new top-level nodes
    eye_grp = None
    for node in new_nodes:
        short = node.split('|')[-1]
        if short == 'eye_grp':
            eye_grp = short
            break

    if not eye_grp:
        cmds.warning('Could not find eye_grp after import. Looking for any eye_grp in scene...')
        if cmds.objExists('eye_grp'):
            eye_grp = 'eye_grp'
        else:
            cmds.error('eye_grp not found after importing {}. Aborting.'.format(eye_file))
            return None

    # Rename all nodes in the hierarchy with the side prefix
    new_top = _rename_hierarchy(eye_grp, name_prefix)

    # Move the OffsetCtrl to the locator guide position and rotation
    offset_ctrl = '{}eye_grp_OffsetCtrl'.format(name_prefix)
    if cmds.objExists(offset_ctrl):
        # Get locator world position and rotation
        guide_pos = cmds.xform(loc_guide, q=True, ws=True, t=True)
        guide_rot = cmds.xform(loc_guide, q=True, ws=True, ro=True)

        cmds.xform(offset_ctrl, ws=True, t=guide_pos)
        cmds.xform(offset_ctrl, ws=True, ro=guide_rot)
    else:
        cmds.warning('{} not found. Skipping positioning.'.format(offset_ctrl))

    # Constrain OffsetCtrl to SetCtrlParent (parent + scale constraint)
    try:
        ctrl_parent = cmds.getAttr('{}.SetCtrlParent'.format(config))
        if ctrl_parent and cmds.objExists(ctrl_parent) and cmds.objExists(offset_ctrl):
            cmds.parentConstraint(ctrl_parent, offset_ctrl, mo=True)
            cmds.scaleConstraint(ctrl_parent, offset_ctrl, mo=True)
    except:
        pass

    # Parent the top node under Ctrl_Grp
    try:
        cmds.parent(new_top, 'Ctrl_Grp')
    except:
        pass

    return new_top


def build_tooneye_block():

    mt.check_is_there_is_base()

    nc, curve_data, setup = mt.import_configs()
    block = cmds.ls(sl=True)

    if not block:
        cmds.warning('Please select the ToonEye block to build.')
        return

    config = cmds.listConnections(block)[1]
    loc_guide = cmds.listRelatives(block, c=True, fullPath=True)[0]

    # Read mirror setting
    try:
        mirror_mode = cmds.getAttr('{}.Mirror'.format(config), asString=True)
    except:
        mirror_mode = 'False'

    # Build L_ side
    l_eye = _build_tooneye_side('L_', loc_guide, config, nc, setup)

    # Build R_ side if mirrored
    if mirror_mode == 'True':
        r_eye = _build_tooneye_side('R_', loc_guide, config, nc, setup)

        # Mirror the R_ side position in X
        r_offset_ctrl = 'R_eye_grp_OffsetCtrl'
        if r_eye and cmds.objExists(r_offset_ctrl):
            pos = cmds.xform(r_offset_ctrl, q=True, ws=True, t=True)
            rot = cmds.xform(r_offset_ctrl, q=True, ws=True, ro=True)
            # Negate X for mirror
            cmds.xform(r_offset_ctrl, ws=True, t=[-pos[0], pos[1], pos[2]])
            cmds.xform(r_offset_ctrl, ws=True, ro=[-rot[0], rot[1], rot[2]])

    print('Build ToonEye successful')

#build_tooneye_block()
