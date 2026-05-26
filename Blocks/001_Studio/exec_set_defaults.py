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

def create_set_defaults_block(name='SetDefaults'):
    PATH = os.path.dirname(__file__)
    MODULE_FILE = os.path.join(PATH, '12_SetDefaults.json')
    if not os.path.exists(MODULE_FILE):
        cmds.warning('12_SetDefaults.json not found.')
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


# create_set_defaults_block()

# -------------------------

def build_set_defaults_block():
    nc, curve_data, setup = mt.import_configs()
    block = cmds.ls(sl=True)
    if not block:
        cmds.warning("Please select the SetDefaults block to build.")
        return

    # Safely get configuration node
    conns = cmds.listConnections(block, type='network') or []
    if not conns:
        conns = cmds.listConnections(block) or []
        if len(conns) < 2:
            cmds.warning("Could not find configuration node for SetDefaults block {}".format(block))
            return
        config = conns[1]
    else:
        config = conns[0]
    block = block[0]

    stored_string = cmds.getAttr('{}.SetDefaultsList'.format(config), asString=True)

    if not stored_string:
        cmds.warning("No stored values found on this block.")
        return

    # Entries are comma-separated in format: node.attr = value
    entries = [e.strip() for e in stored_string.split(',') if e.strip()]
    success_count = 0
    fail_count = 0

    for entry in entries:
        if '=' not in entry:
            cmds.warning("Invalid entry (no '='): {}".format(entry))
            fail_count += 1
            continue

        attr_path, value_str = entry.split('=', 1)
        attr_path = attr_path.strip()
        value_str = value_str.strip()

        if not cmds.objExists(attr_path):
            cmds.warning("Attribute {} does not exist. Skipping.".format(attr_path))
            fail_count += 1
            continue

        attr_name = attr_path.split('.')[-1]
        is_trs = attr_name in (
            'translate', 'translateX', 'translateY', 'translateZ', 'tx', 'ty', 'tz',
            'rotate', 'rotateX', 'rotateY', 'rotateZ', 'rx', 'ry', 'rz',
            'scale', 'scaleX', 'scaleY', 'scaleZ', 'sx', 'sy', 'sz'
        )

        try:
            attr_type = cmds.getAttr(attr_path, type=True)

            if attr_type in ('string',):
                cmds.setAttr(attr_path, value_str, type='string')
            elif attr_type in ('double', 'float', 'long', 'short', 'byte', 'doubleAngle', 'doubleLinear'):
                val = float(value_str)
                cmds.setAttr(attr_path, val)
                if not is_trs:
                    try:
                        cmds.addAttr(attr_path, edit=True, defaultValue=val)
                    except Exception:
                        pass
            elif attr_type in ('bool',):
                val = bool(int(float(value_str)))
                cmds.setAttr(attr_path, val)
                if not is_trs:
                    try:
                        cmds.addAttr(attr_path, edit=True, defaultValue=val)
                    except Exception:
                        pass
            elif attr_type in ('enum',):
                resolved_val = None
                try:
                    val = int(float(value_str))
                    cmds.setAttr(attr_path, val)
                    resolved_val = val
                except ValueError:
                    # It's a string name (e.g., 'head')
                    # Query the enum options to find the corresponding index
                    node = attr_path.split('.')[0]
                    attr_name_only = attr_path.split('.')[-1]
                    enums_str = cmds.attributeQuery(attr_name_only, node=node, listEnum=True)[0]
                    enum_list = str(enums_str).split(':')
                    
                    found_idx = None
                    for idx, enum_item in enumerate(enum_list):
                        enum_name = enum_item.split('=')[0].strip()
                        if enum_name == value_str:
                            if '=' in enum_item:
                                try:
                                    found_idx = int(enum_item.split('=')[1].strip())
                                except ValueError:
                                    found_idx = idx
                            else:
                                    found_idx = idx
                            break
                    
                    if found_idx is not None:
                        cmds.setAttr(attr_path, found_idx)
                        resolved_val = found_idx
                    else:
                        # Fallback: try case-insensitive comparison
                        for idx, enum_item in enumerate(enum_list):
                            enum_name = enum_item.split('=')[0].strip()
                            if enum_name.lower() == value_str.lower():
                                if '=' in enum_item:
                                    try:
                                        found_idx = int(enum_item.split('=')[1].strip())
                                    except ValueError:
                                        found_idx = idx
                                else:
                                    found_idx = idx
                                break
                        
                        if found_idx is not None:
                            cmds.setAttr(attr_path, found_idx)
                            resolved_val = found_idx
                        else:
                            raise ValueError("Enum value '{}' not found in options: {}".format(value_str, enums_str))
                
                if resolved_val is not None and not is_trs:
                    try:
                        cmds.addAttr(attr_path, edit=True, defaultValue=resolved_val)
                    except Exception:
                        pass
            else:
                val = float(value_str)
                cmds.setAttr(attr_path, val)
                if not is_trs:
                    try:
                        cmds.addAttr(attr_path, edit=True, defaultValue=val)
                    except Exception:
                        pass

            success_count += 1
        except Exception as e:
            cmds.warning("Could not set {}: {}".format(attr_path, str(e)))
            fail_count += 1

    print('Build SetDefaults on {} - {} set, {} skipped'.format(block, success_count, fail_count))


# build_set_defaults_block()
