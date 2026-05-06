from __future__ import absolute_import, division
from maya import cmds, mel
import json
try:
    import importlib
    from importlib import reload
except:
    import imp
    from imp import reload

import os
from pathlib import Path

import Mutant_Tools
import Mutant_Tools.Utils.Rigging
from Mutant_Tools.Utils.Rigging import main_mutant
reload(Mutant_Tools.Utils.Rigging.main_mutant)

mt = main_mutant.Mutant()

# ---------------------------------------------

TAB_FOLDER = '008_Props'
PYBLOCK_NAME = 'exec_ribbon_tweakers'


# ---------------------------------------------

def _safe_int(value, fallback=1, minimum=1):
    try:
        parsed = int(round(float(value)))
    except:
        parsed = fallback
    return max(minimum, parsed)


def _get_surface_shape(surface_transform):
    shapes = cmds.listRelatives(surface_transform, shapes=True, type='nurbsSurface') or []
    if not shapes:
        return None
    return shapes[0]


def _resolve_source_surface(block):
    children = cmds.listRelatives(block, c=True, type='transform') or []
    for child in children:
        if _get_surface_shape(child):
            return child

    return None


def _create_follicles(surface_transform, count, walk_axis, prefix, nc):
    surface_shape = _get_surface_shape(surface_transform)
    if not surface_shape:
        cmds.error('No nurbsSurface shape found under: {}'.format(surface_transform))

    fol_grp_name = '{}{}{}'.format(prefix, nc['follicle'], nc['group'])
    if cmds.objExists(fol_grp_name):
        cmds.delete(fol_grp_name)
    fol_grp = cmds.group(empty=True, name=fol_grp_name)

    follicles = []
    for i in range(count):
        t = i / float(count)

        if walk_axis.lower() == 'u':
            u_val, v_val = t, 0.5
        else:
            u_val, v_val = 0.5, t

        fol_name = '{}_{:02d}{}'.format(prefix, i + 1, nc['follicle'])
        fol_shape = cmds.createNode('follicle', name='{}Shape'.format(fol_name))
        fol_tfm = cmds.listRelatives(fol_shape, parent=True)[0]
        fol_tfm = cmds.rename(fol_tfm, fol_name)
        fol_shape = cmds.listRelatives(fol_tfm, shapes=True)[0]

        cmds.connectAttr(surface_shape + '.local', fol_shape + '.inputSurface', force=True)
        cmds.connectAttr(surface_shape + '.worldMatrix[0]', fol_shape + '.inputWorldMatrix', force=True)
        cmds.connectAttr(fol_shape + '.outTranslate', fol_tfm + '.translate', force=True)
        cmds.connectAttr(fol_shape + '.outRotate', fol_tfm + '.rotate', force=True)

        cmds.setAttr(fol_shape + '.simulationMethod', 0)
        cmds.setAttr(fol_shape + '.parameterU', u_val)
        cmds.setAttr(fol_shape + '.parameterV', v_val)

        cmds.parent(fol_tfm, fol_grp)
        follicles.append(fol_tfm)

    return fol_grp, follicles


def create_ribbon_tweakers_block(name='RibbonTweakers'):

    PATH = os.path.dirname(__file__)
    PATH = Path(PATH)
    PATH_PARTS = PATH.parts[:-2]
    FOLDER = ''
    for f in PATH_PARTS:
        FOLDER = os.path.join(FOLDER, f)

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '13_RibbonTweakers.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()

    name = mt.ask_name(text=module['Name'])
    if cmds.objExists('{}{}'.format(name, nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    default_joints = _safe_int(module['attrs'].get('Joints_float', 16), fallback=16, minimum=3)
    joints_count = default_joints

    prompt_result = cmds.promptDialog(
        title='Ribbon Tweakers',
        message='How many joints/tweakers?',
        button=['OK', 'Cancel'],
        defaultButton='OK',
        cancelButton='Cancel',
        dismissString='Cancel',
        text=str(default_joints)
    )

    if prompt_result == 'OK':
        entered = cmds.promptDialog(query=True, text=True)
        joints_count = _safe_int(entered, fallback=default_joints, minimum=3)

    block_data = mt.create_block(
        name=name,
        icon='RibbonTweakers',
        attrs=module['attrs'],
        build_command=module['build_command'],
        import_command=module['import']
    )
    config = block_data[1]
    block = block_data[0]

    try:
        cmds.setAttr('{}.Joints'.format(config), joints_count)
    except:
        pass

    guide_name = '{}{}'.format(name, nc['guide'])
    guide_surface = mel.eval(
        'cylinder -p 0 0 0 -ax 0 1 0 -ssw 0 -esw 360 -r 1 -hr 2 -d 3 -ut 0 -tol 0.01 -s {} -nsp 1 -ch 1 -n "{}";'.format(
            joints_count,
            guide_name)
    )[0]

    if cmds.listRelatives(guide_surface, p=True):
        cmds.parent(guide_surface, w=True)
    cmds.parent(guide_surface, block)
    cmds.select(block)

    print('{} Created Successfully'.format(name))


# create_ribbon_tweakers_block()

# -------------------------

def build_ribbon_tweakers_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    name = block.replace(nc['module'], '')

    source_surface = _resolve_source_surface(block)
    if not source_surface:
        cmds.warning('No NURBS surface found under the block. Create or parent one and rebuild.')
        return

    count = _safe_int(cmds.getAttr('{}.Joints'.format(config)), fallback=16, minimum=1)
    walk_axis = cmds.getAttr('{}.WalkAxis'.format(config), asString=True).lower()
    ctrl_type = cmds.getAttr('{}.CtrlType'.format(config), asString=True)
    ctrl_size = cmds.getAttr('{}.CtrlSize'.format(config))
    ctrl_color = cmds.getAttr('{}.CtrlColor'.format(config), asString=True)

    if walk_axis not in ['u', 'v']:
        walk_axis = 'v'

    if cmds.getAttr('{}.SetParent'.format(config), asString=True) == 'new_locator':
        block_parent = cmds.spaceLocator(n='{}'.format(str(block).replace(nc['module'], '_Parent' + nc['locator'])))[0]
    else:
        block_parent = cmds.getAttr('{}.SetParent'.format(config), asString=True)

    clean_ctrl_grp = '{}_Tweakers{}{}'.format(name, nc['ctrl'], nc['group'])
    clean_rig_grp = '{}_Tweakers_Rig{}'.format(name, nc['group'])
    runtime_surface_name = '{}_Tweakers{}'.format(name, nc['nurb'])

    for node in [clean_ctrl_grp, clean_rig_grp]:
        if cmds.objExists(node):
            cmds.delete(node)

    # Keep original guide surface untouched by building on a duplicated runtime surface.
    if cmds.objExists(runtime_surface_name):
        cmds.delete(runtime_surface_name)

    clean_ctrl_grp = cmds.group(em=True, n=clean_ctrl_grp)
    clean_rig_grp = cmds.group(em=True, n=clean_rig_grp)

    runtime_surface = cmds.duplicate(source_surface, n=runtime_surface_name)[0]
    cmds.parent(runtime_surface, clean_rig_grp)

    follicle_prefix = '{}_Twk'.format(name)
    fol_grp, follicles = _create_follicles(runtime_surface, count, walk_axis, follicle_prefix, nc)
    cmds.parent(fol_grp, clean_rig_grp)

    bind_jnt_grp = '{}{}'.format(setup['rig_groups']['bind_joints'], nc['group'])

    for fol in follicles:
        base = fol.replace(nc['follicle'], '')

        ctrl_name = '{}{}'.format(base, nc['ctrl'])
        rig_jnt_name = '{}{}'.format(base, nc['joint'])
        bind_jnt_name = '{}{}'.format(base, nc['joint_bind'])

        ctrl = mt.curve(
            input=fol,
            type=ctrl_type,
            rename=False,
            custom_name=True,
            name=ctrl_name,
            size=ctrl_size
        )
        mt.assign_color(input=ctrl, color=ctrl_color)

        ctrl_roots = mt.root_grp(input=ctrl, autoRoot=True)
        ctrl_root = ctrl_roots[0]

        cmds.delete(cmds.parentConstraint(fol, ctrl_root, mo=False))
        cmds.parentConstraint(fol, ctrl_root, mo=True)
        cmds.parent(ctrl_root, clean_ctrl_grp)

        cmds.select(cl=True)
        rig_joint = cmds.joint(n=rig_jnt_name)
        cmds.delete(cmds.parentConstraint(fol, rig_joint, mo=False))
        cmds.setAttr('{}.segmentScaleCompensate'.format(rig_joint), 0)
        cmds.parentConstraint(ctrl, rig_joint, mo=True)
        cmds.scaleConstraint(ctrl, rig_joint, mo=True)
        cmds.parent(rig_joint, clean_rig_grp)

        cmds.select(cl=True)
        bind_joint = cmds.joint(n=bind_jnt_name)
        cmds.delete(cmds.parentConstraint(rig_joint, bind_joint, mo=False))
        cmds.setAttr('{}.segmentScaleCompensate'.format(bind_joint), 0)
        cmds.setAttr('{}.inheritsTransform'.format(bind_joint), 0)
        cmds.parentConstraint(rig_joint, bind_joint, mo=False)
        cmds.scaleConstraint(rig_joint, bind_joint, mo=True)

        if cmds.objExists(bind_jnt_grp):
            cmds.parent(bind_joint, bind_jnt_grp)

    misc_grp = '{}{}'.format(setup['rig_groups']['misc'], nc['group'])
    ctrl_base_grp = '{}{}'.format(setup['base_groups']['control'], nc['group'])

    if cmds.objExists(misc_grp):
        cmds.parent(clean_rig_grp, misc_grp)
    if cmds.objExists(ctrl_base_grp):
        cmds.parent(clean_ctrl_grp, ctrl_base_grp)

    if cmds.objExists(block_parent):
        cmds.parentConstraint(block_parent, clean_ctrl_grp, mo=True)
        cmds.scaleConstraint(block_parent, clean_ctrl_grp, mo=True)

    print('Build {} Success'.format(block))


# build_ribbon_tweakers_block()
