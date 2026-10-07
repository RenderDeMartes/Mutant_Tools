"""Block hooks: a block can react when one of its config attrs is edited, before it is built.

A block opts in by defining, in the module of its Import_Command (e.g. exec_hand_v002.py):

    def on_attr_changed(config, attr, value):
        ...

config is the block config network node, attr the attr name without the JSON suffix (Thumb, not Thumb_bool)
and value the new value. The AutoRigger calls it after a checkbox or enum edit, any other tool can call
run_attr_changed() after setting a config attr.

Blocks without the function are not imported (the file is only read), so nothing changes for them.
"""
from __future__ import absolute_import
import importlib
import importlib.util
import re
import sys
import traceback

from maya import cmds

HOOK_NAME = 'on_attr_changed'

# module name -> has the hook, the file is read only once per session
_HAS_HOOK = {}


def block_module_name(config):
    """Module name of a block config Import_Command ('import exec_hand_v002' -> 'exec_hand_v002')."""
    if not cmds.objExists(config) or not cmds.attributeQuery('Import_Command', n=config, exists=True):
        return None
    match = re.search(r'\bimport\s+([A-Za-z_][A-Za-z0-9_]*)', cmds.getAttr(config + '.Import_Command') or '')
    return match.group(1) if match else None


def _has_hook(module_name):
    if module_name not in _HAS_HOOK:
        found = False
        try:
            spec = importlib.util.find_spec(module_name)
            if spec and spec.origin and spec.origin.endswith('.py'):
                with open(spec.origin) as source:
                    found = 'def {}('.format(HOOK_NAME) in source.read()
        except Exception:
            found = False
        _HAS_HOOK[module_name] = found
    return _HAS_HOOK[module_name]


def get_hook(config):
    """The block on_attr_changed function, or None."""
    module_name = block_module_name(config)
    if not module_name or not _has_hook(module_name):
        return None
    module = sys.modules.get(module_name) or importlib.import_module(module_name)
    return getattr(module, HOOK_NAME, None)


def run_attr_changed(config, attr, value=None):
    """Calls the block hook for config.attr (value read from the attr when not given).
    One undo step, the selection is kept, errors are printed and never raised. Returns True if a hook ran."""
    try:
        hook = get_hook(config)
    except Exception:
        traceback.print_exc()
        return False
    if not hook:
        return False
    if value is None and cmds.attributeQuery(attr, n=config, exists=True):
        value = cmds.getAttr('{}.{}'.format(config, attr))

    selection = cmds.ls(sl=True) or []
    cmds.undoInfo(openChunk=True, chunkName='{}_{}'.format(config, attr))
    try:
        hook(config, attr, value)
        return True
    except Exception:
        traceback.print_exc()
        cmds.warning('Block hook failed on {}.{}, see the script editor'.format(config, attr))
        return False
    finally:
        selection = [node for node in selection if cmds.objExists(node)]
        if selection:
            cmds.select(selection, r=True)
        else:
            cmds.select(cl=True)
        cmds.undoInfo(closeChunk=True)
