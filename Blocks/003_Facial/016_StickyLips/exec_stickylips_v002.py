from __future__ import absolute_import
from maya import cmds
from maya.api import OpenMaya as om
import json
import re
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
from Mutant_Tools.Utils.Rigging import block_errors

mt = main_mutant.Mutant()

#---------------------------------------------

TAB_FOLDER = '003_Facial'
PYBLOCK_NAME = 'exec_stickylips'

# StickyLips v002: zip for the local face (Lips v003 + Jaw v002 + BodyJaw /
# BodyLips local geos), working like the MouthGames zip: each lip point slides
# to the middle of both lips, from the corners in (Zip 0-3 at the corner, 7-10
# in the middle). The lips themselves never follow the jaw, the BodyJaw layer
# opens the mouth, so "both lips" = the lip bind joints plus what the BodyJaw
# layer does under them, read live with one uvPin on the jaw geo (any skin
# weights, any build order). The offset goes on the lip bind joints, the
# BodyLips layer adds it on top of the jaw. Uses the Zip attr the Lips block
# leaves hidden + locked on L/R_<Lips>_Main_Ctrl.

#---------------------------------------------

def create_stickylips_block(name = 'StickyLips'):

    MODULE_FILE = os.path.join(os.path.dirname(__file__), '016_StickyLips_v002.json')
    with open(MODULE_FILE) as module_file:
        module = json.load(module_file)

    nc, curve_data, setup = mt.import_configs()

    #name checks and block creation
    name = mt.ask_name(text = module['Name'])
    if cmds.objExists('{}{}'.format(name,nc['module'])):
        cmds.warning('Name already exists.')
        return ''

    block = mt.create_block(name = name, icon = 'Sticky',  attrs = module['attrs'], build_command = module['build_command'], import_command = module['import'])
    block = block[0]

    cmds.select(block)

    print('{} Created Successfully'.format(name))

#create_stickylips_block()

#-------------------------

def build_stickylips_block():

    nc, curve_data, setup = mt.import_configs()

    mt.check_is_there_is_base()

    block = cmds.ls(sl=True)
    config = cmds.listConnections(block)[1]
    block = block[0]
    name = block.replace(nc['module'],'')

    lips = (cmds.getAttr('{}.SetLips'.format(config)) or '').strip()
    jaw_geo = (cmds.getAttr('{}.SetJawGeo'.format(config)) or '').strip()

    # --- checks, with messages the artist can act on ---
    lips_block = lips + nc['module']
    corner_ctrls = {side: side + lips + '_Main' + nc['ctrl'] for side in (nc['left'], nc['right'])}
    missing = [n for n in [lips_block] + sorted(corner_ctrls.values()) if not cmds.objExists(n)]
    if missing:
        raise block_errors.BlockBuildError(
            'Build the Lips before the StickyLips',
            '"{}" works on the Lips block "{}" (SetLips), but these are not in the scene yet: {}.\n\n'
            'Move "{}" below the Lips block (and the Jaw block) in Mutant_Build, or set SetLips to the Lips block '
            'name (Mouth in the face templates).'.format(block, lips, ', '.join(missing), block), block=block)
    lips_config = _config(lips_block)
    if lips_config and cmds.attributeQuery('GameMode', n=lips_config, exists=True) \
            and cmds.getAttr(lips_config + '.GameMode'):
        raise block_errors.BlockBuildError(
            'StickyLips works on local lips',
            '"{}" has GameMode on: its bind joints are in world space and there is no BodyJaw layer to stick to.\n\n'
            'Turn GameMode off on "{}" (or remove this block from game rigs).'.format(lips_block, lips_block),
            block=block)
    jaw_shape = _mesh_shape(jaw_geo)
    if not jaw_shape:
        raise block_errors.BlockBuildError(
            'Jaw geo not found',
            '"{}" (SetJawGeo) is not a mesh in the scene. Set it to the local jaw layer geo (BodyJaw), the one '
            'the Jaw block bind joints are skinned to.'.format(jaw_geo), block=block)

    lips_binds = {lip: _lip_binds(lips, lip, nc) for lip in ('Up', 'Dw')}
    if not lips_binds['Up'] or not lips_binds['Dw']:
        raise block_errors.BlockBuildError(
            'Lip bind joints not found',
            'No {}_Up_Lip / {}_Dw_Lip joints with bind joints in the scene. StickyLips v002 works with the Lips '
            'v003 block.'.format(lips, lips), block=block)

    # --- the Zip attrs the Lips block left hidden + locked ---
    zip_attrs = {}
    for side, ctrl in corner_ctrls.items():
        if not cmds.attributeQuery('Zip', n=ctrl, exists=True):
            mt.new_attr(input=ctrl, name='Zip', min=0, max=10, default=0)
        plug = ctrl + '.Zip'
        cmds.setAttr(plug, lock=False)
        cmds.setAttr(plug, keyable=True)
        zip_attrs[side] = plug

    # --- each lip bind: where it ends up = its own motion + the jaw layer under it ---
    pin = cmds.createNode('uvPin', n=name + '_JawGeo_UvPin')
    cmds.connectAttr(jaw_shape + '.worldMesh[0]', pin + '.deformedGeometry')
    mesh_fn = om.MFnMesh(om.MSelectionList().add(jaw_shape).getDagPath(0))
    if not mesh_fn.numUVs():
        raise block_errors.BlockBuildError(
            'Jaw geo has no UVs',
            '"{}" needs UVs: StickyLips pins a point on it under each lip joint to read what the jaw does '
            'there.'.format(jaw_geo), block=block)

    lips_points = {}
    index = 0
    for lip in ('Up', 'Dw'):
        points = []
        for bind, pre in lips_binds[lip]:
            rest = om.MVector(cmds.xform(bind, q=True, ws=True, t=True))
            u, v, _ = mesh_fn.getUVAtPoint(om.MPoint(rest), om.MSpace.kWorld)
            pin_matrix = '{}.outputMatrix[{}]'.format(pin, index)
            cmds.setAttr('{}.coordinate[{}].coordinateU'.format(pin, index), u)
            cmds.setAttr('{}.coordinate[{}].coordinateV'.format(pin, index), v)
            pin_point = cmds.createNode('decomposeMatrix', n=bind + '_JawGeo_DM')
            cmds.connectAttr(pin_matrix, pin_point + '.inputMatrix')
            pin_rest = cmds.getAttr(pin_point + '.outputTranslate')[0]
            # bind position + jaw layer motion under it (pin - pin at rest)
            final = cmds.createNode('plusMinusAverage', n=bind + '_ZipFinal_PMA')
            cmds.connectAttr(_parent_matrix_plug(pre, bind, world=True), final + '.input3D[0]')
            cmds.connectAttr(pin_point + '.outputTranslate', final + '.input3D[1]')
            cmds.setAttr(final + '.input3D[2]', *[-x for x in pin_rest])
            points.append({'bind': bind, 'pre': pre, 'rest': rest, 'final': final + '.output3D'})
            index += 1
        _arc_fractions(points)
        lips_points[lip] = points

    # --- zip: each point to the middle of both lips, from the corners in ---
    for lip, other in [('Up', 'Dw'), ('Dw', 'Up')]:
        for point in lips_points[lip]:
            other_final = _final_at(lips_points[other], point['u'], point['bind'])
            gap = cmds.createNode('plusMinusAverage', n=point['bind'] + '_ZipGap_PMA')
            cmds.setAttr(gap + '.operation', 2)
            cmds.connectAttr(other_final, gap + '.input3D[0]')
            cmds.connectAttr(point['final'], gap + '.input3D[1]')
            half = _zip_weight(point['bind'], point['u'], zip_attrs, nc)
            offset = cmds.createNode('multiplyDivide', n=point['bind'] + '_Zip_MD')
            cmds.connectAttr(gap + '.output3D', offset + '.input1')
            for axis in 'XYZ':
                cmds.connectAttr(half, offset + '.input2' + axis)
            result = cmds.createNode('plusMinusAverage', n=point['bind'] + '_Zip_PMA')
            cmds.connectAttr(point['pre'], result + '.input3D[0]')
            cmds.connectAttr(_parent_matrix_plug(offset + '.output', point['bind']), result + '.input3D[1]')
            cmds.connectAttr(result + '.output3D', point['bind'] + '.translate', f=True)

    cmds.select(block)
    print ('Build {} Success'.format(block))

#build_stickylips_block()

#-------------------------

def _config(block):
    for node in cmds.listConnections(block, type='network') or []:
        if cmds.attributeQuery('Import_Command', n=node, exists=True):
            return node
    return None


def _mesh_shape(geo):
    if not geo or not cmds.objExists(geo):
        return None
    if cmds.nodeType(geo) == 'mesh':
        return geo
    shapes = cmds.listRelatives(geo, s=True, ni=True, type='mesh', f=True) or []
    return shapes[0] if shapes else None


def _lip_binds(lips, lip, nc):
    """[(bind, translate source plug)] of one lip, right corner -> left corner.
    Found from the lip joints (R_/Mid_/L_<lips>_<lip>_Lip[_NN]_Jnt), whose bind
    copies them through <bind>_Follow_MM, so LegacyBindNames binds work too."""
    pattern = re.compile(r'^({}|{}|Mid_){}_{}_Lip(?:_(\d+))?{}$'.format(
        re.escape(nc['right']), re.escape(nc['left']), re.escape(lips), lip, re.escape(nc['joint'])))
    found = []
    for jnt in cmds.ls('*{}_{}_Lip*{}'.format(lips, lip, nc['joint']), type='joint'):
        match = pattern.match(jnt)
        if not match:
            continue
        bind = None
        for mult in cmds.listConnections(jnt + '.worldMatrix[0]', s=False, d=True, type='multMatrix') or []:
            candidate = mult[:-len('_Follow_MM')] if mult.endswith('_Follow_MM') else None
            if candidate and cmds.objExists(candidate) and cmds.nodeType(candidate) == 'joint':
                bind = candidate
                break
        pre = cmds.listConnections(bind + '.translate', s=True, d=False, p=True) if bind else None
        if not pre:
            continue
        side, num = match.group(1), int(match.group(2) or 0)
        order = -num if side == nc['right'] else (num if side == nc['left'] else 0)
        found.append((order, bind, pre[0]))
    return [(bind, pre) for order, bind, pre in sorted(found)]


def _arc_fractions(points):
    """point['u']: 0 at the right corner -> 1 at the left one, by length."""
    lengths = [0.0]
    for a, b in zip(points, points[1:]):
        lengths.append(lengths[-1] + (b['rest'] - a['rest']).length())
    total = lengths[-1] or 1.0
    for point, length in zip(points, lengths):
        point['u'] = length / total


def _final_at(points, u, name):
    """Plug of the other lip's final position at the fraction u (blend of the two around it)."""
    for a, b in zip(points, points[1:]):
        if a['u'] - 1e-6 <= u <= b['u'] + 1e-6:
            t = (u - a['u']) / max(b['u'] - a['u'], 1e-9)
            t = min(max(t, 0.0), 1.0)
            if t < 1e-4:
                return a['final']
            if t > 1 - 1e-4:
                return b['final']
            blend = cmds.createNode('blendColors', n=name + '_ZipOther_BC')
            cmds.connectAttr(b['final'], blend + '.color1')
            cmds.connectAttr(a['final'], blend + '.color2')
            cmds.setAttr(blend + '.blender', t)
            return blend + '.output'
    return (points[0] if u < points[0]['u'] else points[-1])['final']


def _zip_weight(name, u, zip_attrs, nc):
    """Half of the zip amount at u (0..0.5: each lip goes half the gap). Each
    corner zips its own half, corner first (Zip 0-3) to middle (7-10), like
    the MouthGames zip."""
    sides = []
    if u > 0.5 - 1e-4:
        sides.append((nc['left'], (1 - u) * 2))
    if u < 0.5 + 1e-4:
        sides.append((nc['right'], u * 2))
    remaps = []
    for side, f in sides:
        remap = cmds.createNode('remapValue', n='{}_Zip{}Remap'.format(name, side.replace('_', '')))
        cmds.connectAttr(zip_attrs[side], remap + '.inputValue')
        cmds.setAttr(remap + '.inputMin', f * 7)
        cmds.setAttr(remap + '.inputMax', f * 7 + 3)
        cmds.setAttr(remap + '.outputMax', 0.5)
        cmds.setAttr(remap + '.value[0].value_Interp', 2)
        cmds.setAttr(remap + '.value[1].value_Interp', 2)
        remaps.append(remap + '.outValue')
    if len(remaps) == 1:
        return remaps[0]
    both = cmds.createNode('plusMinusAverage', n=name + '_Zip_Both_PMA')
    for i, plug in enumerate(remaps):
        cmds.connectAttr(plug, '{}.input1D[{}]'.format(both, i))
    clamp = cmds.createNode('clamp', n=name + '_Zip_Clamp')
    cmds.setAttr(clamp + '.maxR', 0.5)
    cmds.connectAttr(both + '.output1D', clamp + '.inputR')
    return clamp + '.outputR'


def _parent_matrix_plug(plug, bind, world=False):
    """The zip math is in world space, the bind translate lives in its parent
    (Bind_Joints_Grp, normally identity: then the plug as it is).
    world=True: bind translate -> world point. Else: world vector -> parent space."""
    parent = cmds.listRelatives(bind, p=True)
    if not parent:
        return plug
    matrix = om.MMatrix(cmds.xform(parent[0], q=True, ws=True, m=True))
    if matrix.isEquivalent(om.MMatrix(), 1e-6):
        return plug
    convert = cmds.createNode('pointMatrixMult', n=bind + ('_ZipWorld_PMM' if world else '_ZipLocal_PMM'))
    cmds.setAttr(convert + '.vectorMultiply', 0 if world else 1)
    cmds.connectAttr(plug, convert + '.inPoint')
    cmds.connectAttr(parent[0] + ('.worldMatrix[0]' if world else '.worldInverseMatrix[0]'), convert + '.inMatrix')
    return convert + '.output'
