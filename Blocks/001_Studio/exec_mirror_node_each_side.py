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
PYBLOCK_NAME = 'exec_mirror_node_each_side'

#---------------------------------------------

def create_mirror_node_each_side_block(name='MirrorNodeEachSide'):

    # Read name conventions as nc[''] and setup as setup['']
    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-2]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '09_MirrorNodeEachSide.json')
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

    loc = cmds.spaceLocator(n=name + nc['locator'])
    cmds.parent(loc, block)

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_mirror_node_each_side_block()

#-------------------------

def build_mirror_node_each_side_block():
    """Find all nodes ending with Mirror_Grp and create matching groups on the opposite side.

    For each node ending with Mirror_Grp (e.g. R_Antenna_A_Ctrl_Offset_GrpMirror_Grp):
      1. Strip the Mirror_Grp suffix  -> R_Antenna_A_Ctrl_Offset_Grp
      2. Swap the R_ prefix to L_     -> L_Antenna_A_Ctrl_Offset_Grp  (must exist)
      3. Create L_Antenna_A_Ctrl_Offset_GrpMirror_Grp at origin
      4. Insert it above L_Antenna_A_Ctrl_Offset_Grp in the hierarchy
    """

    nc, curve_data, setup = mt.import_configs()
    mirror_suffix = 'Mirror_Grp'

    # Find all nodes ending with Mirror_Grp
    all_nodes = cmds.ls('*' + mirror_suffix, type='transform') or []

    if not all_nodes:
        cmds.warning('No nodes ending with {} found in the scene.'.format(mirror_suffix))
        return

    created_count = 0

    for mirror_node in all_nodes:
        # Strip the Mirror_Grp suffix to get the base name
        base_name = mirror_node[:-len(mirror_suffix)]  # e.g. R_Antenna_A_Ctrl_Offset_Grp

        # Determine the opposite side name
        if base_name.startswith('R_'):
            opposite_base = 'L_' + base_name[2:]
        elif base_name.startswith('L_'):
            opposite_base = 'R_' + base_name[2:]
        else:
            # Not a sided node, skip
            continue

        # Check that the opposite-side node exists
        if not cmds.objExists(opposite_base):
            cmds.warning('Opposite side node {} does not exist. Skipping.'.format(opposite_base))
            continue

        # Build the new mirror group name for the opposite side
        new_mirror_grp = opposite_base + mirror_suffix  # e.g. L_Antenna_A_Ctrl_Offset_GrpMirror_Grp

        # Skip if it already exists
        if cmds.objExists(new_mirror_grp):
            print('{} already exists. Skipping.'.format(new_mirror_grp))
            continue

        # Get the current parent of the opposite-side node so we can re-parent later
        current_parent = cmds.listRelatives(opposite_base, parent=True)

        # Create the new mirror group at origin (identity transform)
        cmds.group(empty=True, name=new_mirror_grp)

        # Insert above the opposite-side node:
        # 1. Parent the new group where the opposite node was
        if current_parent:
            cmds.parent(new_mirror_grp, current_parent[0])

        # 2. Parent the opposite node under the new mirror group
        cmds.parent(opposite_base, new_mirror_grp)

        created_count += 1
        print('Created {} above {}'.format(new_mirror_grp, opposite_base))

    print('MirrorNodeEachSide complete. Created {} mirror groups.'.format(created_count))

#build_mirror_node_each_side_block()
