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

def create_pickwalk_block(name='Pickwalk'):
    PATH = os.path.dirname(__file__)
    MODULE_FILE = os.path.join(PATH, '15_Pickwalk.json')
    if not os.path.exists(MODULE_FILE):
        cmds.warning('15_Pickwalk.json not found.')
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

    # Prompt the user to pick a pickwalk JSON file immediately
    filepath = cmds.fileDialog2(
        dialogStyle=2,
        fileMode=1,
        fileFilter='JSON Files (*.json)',
        caption='Select Pickwalk JSON File'
    )
    if filepath:
        cmds.setAttr('{}.PickwalkFile'.format(config), filepath[0], type='string')

    cmds.select(block)
    print('{} Created Successfully'.format(name))


# create_pickwalk_block()

# -------------------------

def build_pickwalk_block(force=False):
    """Build the Pickwalk block: read a JSON file and apply quickPick attributes."""
    nc, curve_data, setup = mt.import_configs()
    block = cmds.ls(sl=True)
    if not block:
        cmds.warning("Please select the Pickwalk block to build.")
        return

    # Safely get configuration node
    conns = cmds.listConnections(block, type='network') or []
    if not conns:
        conns = cmds.listConnections(block) or []
        if len(conns) < 2:
            cmds.warning("Could not find configuration node for Pickwalk block {}".format(block))
            return
        config = conns[1]
    else:
        config = conns[0]
    block = block[0]

    # Check if this block should run before the build begins
    run_before = False
    if cmds.attributeQuery('RunBeforeBuild', n=config, exists=True):
        run_before = cmds.getAttr('{}.RunBeforeBuild'.format(config))

    if run_before and not force:
        print('Pickwalk block {} deferred to run before build starts'.format(block))
        return

    # Check if this block should run after the full build completes
    run_after = False
    if cmds.attributeQuery('RunAfterBuild', n=config, exists=True):
        run_after = cmds.getAttr('{}.RunAfterBuild'.format(config))

    if run_after and not force:
        print('Pickwalk block {} deferred to run after build completes'.format(block))
        return

    # --- Get the file path from the block attribute ---
    filepath = cmds.getAttr('{}.PickwalkFile'.format(config), asString=True)

    if not filepath or not filepath.strip():
        cmds.warning("No pickwalk file specified. Please set the PickwalkFile field.")
        return

    filepath = filepath.strip()

    if not os.path.exists(filepath):
        cmds.warning("Pickwalk file not found: {}".format(filepath))
        return

    # --- Read the JSON data ---
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except Exception as e:
        cmds.warning("Failed to read pickwalk file {}: {}".format(filepath, str(e)))
        return

    # --- Apply pickwalk attributes to scene objects ---
    success_count = 0
    skip_count = 0

    for obj_path, attrs in data.items():
        objects = cmds.ls(obj_path)
        if not objects:
            cmds.warning("Object {} does not exist in the scene. Skipping.".format(obj_path))
            skip_count += 1
            continue

        for obj in objects:
            for attr_name, value in attrs.items():
                if cmds.attributeQuery(attr_name, node=obj, exists=True):
                    try:
                        cmds.setAttr("{}.{}".format(obj, attr_name), value, type="string")
                    except Exception as e:
                        cmds.warning("Error setting {} to {} on {}: {}".format(attr_name, value, obj, str(e)))
                        skip_count += 1
                        continue
                else:
                    try:
                        cmds.addAttr(obj, longName=attr_name, dataType='string')
                        cmds.setAttr("{}.{}".format(obj, attr_name), value, type="string")
                    except Exception as e:
                        cmds.warning("Error creating {} on {}: {}".format(attr_name, obj, str(e)))
                        skip_count += 1
                        continue
            success_count += 1

    print('Build Pickwalk on {} - {} objects updated, {} skipped'.format(block, success_count, skip_count))


# build_pickwalk_block()
