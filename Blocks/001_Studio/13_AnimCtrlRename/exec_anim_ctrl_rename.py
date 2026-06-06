from __future__ import absolute_import
from maya import cmds
import json
import os

try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()

# ---------------------------------------------

def create_animctrlrename_block(name='AnimCtrlRename'):
    PATH = os.path.dirname(__file__)
    MODULE_FILE = os.path.join(PATH, '13_AnimCtrlRename.json')
    if not os.path.exists(MODULE_FILE):
        cmds.warning('13_AnimCtrlRename.json not found.')
        return ''

    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()

    name = mt.ask_name(text=module['Name'])
    if not name:
        return
    if cmds.objExists('{}{}'.format(name, nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(
        name=name,
        icon=module['Icon'].replace('.png', ''),
        attrs=module['attrs'],
        build_command=module['build_command'],
        import_command=module['import']
    )

    config = block[1]
    block = block[0]

    cmds.select(block)
    print('{} Created Successfully'.format(name))


# -------------------------

def build_animctrlrename_block(force=False):
    nc, curve_data, setup = mt.import_configs()
    block = cmds.ls(sl=True)
    if not block:
        cmds.warning("Please select the AnimCtrlRename block to build.")
        return

    # Safely get configuration node
    conns = cmds.listConnections(block, type='network') or []
    if not conns:
        conns = cmds.listConnections(block) or []
        if len(conns) < 2:
            cmds.warning("Could not find configuration node for AnimCtrlRename block {}".format(block))
            return
        config = conns[1]
    else:
        config = conns[0]
    block = block[0]

    # Check if this rename block should run before the build begins
    run_before = False
    if cmds.attributeQuery('RunBeforeBuild', n=config, exists=True):
        run_before = cmds.getAttr('{}.RunBeforeBuild'.format(config))

    if run_before and not force:
        print('AnimCtrlRename block {} deferred to run before build starts'.format(block))
        return

    # Check if this rename block should run after the full build completes (e.g. after skin/ctrl-shapes import)
    run_after = False
    if cmds.attributeQuery('RunAfterBuild', n=config, exists=True):
        run_after = cmds.getAttr('{}.RunAfterBuild'.format(config))

    if run_after and not force:
        print('AnimCtrlRename block {} deferred to run after build completes (post-build procedure)'.format(block))
        return

    revert = False
    if cmds.attributeQuery('Revert', n=config, exists=True):
        revert = cmds.getAttr('{}.Revert'.format(config))

    stored_string = cmds.getAttr('{}.RenameList'.format(config), asString=True)

    if not stored_string:
        cmds.warning("No rename entries found on this block.")
        return

    # Entries are comma-separated in format: old_name = new_name
    entries = [e.strip() for e in stored_string.split(',') if e.strip()]
    success_count = 0
    fail_count = 0

    for entry in entries:
        if '=' not in entry:
            cmds.warning("Invalid rename entry (no '='): {}".format(entry))
            fail_count += 1
            continue

        old_name, new_name = entry.split('=', 1)
        old_name = old_name.strip()
        new_name = new_name.strip()

        if revert:
            old_name, new_name = new_name, old_name

        if not old_name or not new_name:
            cmds.warning("Invalid rename entry (empty names): {}".format(entry))
            fail_count += 1
            continue

        if old_name == new_name:
            print("Old and new names are identical ({}). Skipping.".format(old_name))
            continue

        # Find all nodes in the scene matching *old_name*
        # (This captures shape nodes, constraints, groups, Zero/Offset grps, etc.)
        matched_nodes = cmds.ls('*{}*'.format(old_name))

        if not matched_nodes:
            cmds.warning("No nodes found matching '{}'. Skipping.".format(old_name))
            fail_count += 1
            continue

        # Sort nodes by DAG path length in descending order.
        # This ensures child nodes are renamed before their parent nodes.
        matched_nodes.sort(key=lambda x: x.count('|'), reverse=True)

        renamed_in_entry = 0
        for node in matched_nodes:
            if not cmds.objExists(node):
                continue
            
            # Skip read-only, referenced nodes, or locked nodes
            if cmds.referenceQuery(node, isNodeReferenced=True):
                continue
            
            # Skip any nodes that are under the Mutant_Build hierarchy
            long_name = cmds.ls(node, long=True)[0]
            if 'Mutant_Build' in long_name:
                continue
            
            # Extract short name
            short_name = node.split('|')[-1]
            if old_name in short_name:
                new_short_name = short_name.replace(old_name, new_name)
                try:
                    cmds.rename(node, new_short_name)
                    renamed_in_entry += 1
                except Exception as e:
                    cmds.warning("Could not rename node '{}' to '{}': {}".format(node, new_short_name, str(e)))

        if renamed_in_entry > 0:
            success_count += 1
            print("Successfully renamed {} nodes for entry '{}' -> '{}'.".format(renamed_in_entry, old_name, new_name))
        else:
            fail_count += 1
            cmds.warning("Could not rename any nodes for entry '{}' = '{}'.".format(old_name, new_name))

    print('Build AnimCtrlRename on {} - {} successfully renamed, {} failed'.format(block, success_count, fail_count))
