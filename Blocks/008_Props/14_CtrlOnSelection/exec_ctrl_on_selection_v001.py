from __future__ import absolute_import
from maya import cmds
import json
import os

try:
    import importlib; from importlib import reload
except Exception:
    import imp; from imp import reload

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()

TAB_FOLDER = '008_Props'
PYBLOCK_NAME = 'exec_ctrl_on_selection'


def _load_module_data():
    module_file = os.path.join(os.path.dirname(__file__), '14_CtrlOnSelection.json')
    with open(module_file) as fh:
        return json.load(fh)


def create_ctrl_on_selection_block(name='CtrlOnSelection'):
    nc, curve_data, setup = mt.import_configs()
    module = _load_module_data()

    name = mt.ask_name(text=module['Name'])
    if not name:
        return ''

    if cmds.objExists('{}{}'.format(name, nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    sel = cmds.ls(sl=True)

    block_result = mt.create_block(
        name=name,
        icon='CtrlOnSelection',
        attrs=module['attrs'],
        build_command=module['build_command'],
        import_command=module['import'],
    )
    config = block_result[1]
    block = block_result[0]

    if sel:
        cmds.setAttr('{}.SetJoints'.format(config), ', '.join(sel), type='string')

    loc_guide = cmds.spaceLocator(n=name + nc['locator'])[0]
    cmds.parent(loc_guide, block)

    cmds.select(block)
    print('{} Created Successfully'.format(name))
    return block


def build_ctrl_on_selection_block():
    nc, curve_data, setup = mt.import_configs()

    block = cmds.ls(sl=True)
    if not block:
        cmds.warning('Select a CtrlOnSelection block to build.')
        return

    connections = cmds.listConnections(block) or []
    if len(connections) < 2:
        cmds.warning('Unable to find the selected block config.')
        return

    config = connections[1]
    block = block[0]

    joints_str  = cmds.getAttr('{}.SetJoints'.format(config), asString=True)
    set_parent  = cmds.getAttr('{}.SetParent'.format(config), asString=True)
    shape       = cmds.getAttr('{}.Shape'.format(config), asString=True)
    color       = cmds.getAttr('{}.Color'.format(config), asString=True)
    scale       = int(cmds.getAttr('{}.Scale'.format(config)))
    connection  = cmds.getAttr('{}.Connection'.format(config), asString=True)
    strip_sfx   = bool(cmds.getAttr('{}.StripJointSuffix'.format(config)))

    if not joints_str:
        cmds.warning('No joints defined. Add joints to SetJoints.')
        return

    if scale <= 0:
        scale = 1

    joints = [j.strip() for j in joints_str.split(',') if j.strip()]

    for joint in joints:
        if not cmds.objExists(joint):
            cmds.warning('{} does not exist. Skipping.'.format(joint))
            continue

        ctrl_base = joint
        if strip_sfx and ctrl_base.endswith(nc['joint']):
            ctrl_base = ctrl_base[:-len(nc['joint'])]

        ctrl_name = '{}{}'.format(ctrl_base, nc['ctrl'])

        if cmds.objExists(ctrl_name):
            cmds.warning('{} already exists. Skipping.'.format(ctrl_name))
            continue

        cmds.select(joint)
        ctrl = mt.curve(type=shape, size=scale, rename=False, custom_name=True, name=ctrl_name)
        mt.assign_color(input=ctrl, color=color)

        offset_grps = mt.root_grp(input=ctrl)
        offset_grp = offset_grps[0]

        # Refresh ctrl ref after root_grp reparents it
        ctrl = cmds.listRelatives(offset_grp, children=True, type='transform')[0]

        # Place offset group inside rig Ctrl_Grp
        ctrl_group = '{}{}'.format(setup['base_groups']['control'], nc['group'])
        if cmds.objExists(ctrl_group):
            cmds.parent(offset_grp, ctrl_group)
        else:
            cmds.warning('Ctrl_Grp ({}) not found. {} left at world level.'.format(ctrl_group, offset_grp))

        # Snap offset group to joint world position AND rotation after reparenting
        mt.match(offset_grp, joint, t=True, r=True, s=False)

        # SetParent: parentConstraint + scaleConstraint -> ctrl offset group
        if set_parent and cmds.objExists(set_parent):
            cmds.parentConstraint(set_parent, offset_grp, mo=True)
            cmds.scaleConstraint(set_parent, offset_grp, mo=True)

        # Connection: ctrl drives joint
        if connection == 'DirectConnect':
            for attr in ('translate', 'rotate', 'scale'):
                cmds.connectAttr('{}.{}'.format(ctrl, attr), '{}.{}'.format(joint, attr), force=True)
        elif connection == 'ParentConstraint':
            cmds.parentConstraint(ctrl, joint, mo=True)
        elif connection == 'ScaleConnect':
            cmds.connectAttr('{}.scale'.format(ctrl), '{}.scale'.format(joint), force=True)
        elif connection == 'ParentAndScale':
            cmds.parentConstraint(ctrl, joint, mo=True)
            cmds.connectAttr('{}.scale'.format(ctrl), '{}.scale'.format(joint), force=True)

        print('Created {} for {}'.format(ctrl_name, joint))

    print('Build CtrlOnSelection Success')


