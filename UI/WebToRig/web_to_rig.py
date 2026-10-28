"""WebToRig: rig a character placed on mutanttools.com/web-to-rig/.

The website's download is a folder holding the character's own file, Unreal's
Manny skeleton fitted to it (manny_skeleton.json, in the format of
Utils/Unreal/mannequin_skeleton_capture.json), a skin pack for those joints,
and the HumanUnrealGameTemplate guide positions (skeleton.json).
web_to_rig.json says which file is which.

Three stages, each reporting its progress through `report(percent, text)`:
    import_character   the mesh, the Manny joints, the skin
    place_template     the HumanUnrealGameTemplate guides, moved onto the body
    build_rig          the Mutant Tools build, then Manny driven by it
and, to try the rig, apply_animation with one of Mutant Tools' Mixamo
animations.
"""
from __future__ import absolute_import

import glob
import itertools
import json
import os
import re
import shutil
import tempfile

import maya.cmds as cmds
import maya.mel as mel

try:
    from importlib import reload
except ImportError:  # Python 2
    pass

import Mutant_Tools

FOLDER = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TEMPLATE_FILE = os.path.join(FOLDER, 'Utils', 'IO', 'Guide_Data', 'HumanUnrealGameTemplate.ma')
MIXAMO_FOLDER = os.path.join(FOLDER, 'Utils', 'Mocap', 'MocapFiles', 'Mixamo')
MANIFEST = 'web_to_rig.json'

# template guides the website does not place: they follow the head
FACE_GROUP = 'HumanGameTemplate_Face'
HEAD_FOLLOWERS = (FACE_GROUP, 'L_Eyes_Block')
SPINE = ['Spine_Root_Guide', 'Spine_Base_Guide', 'Spine_Belly_Guide', 'Spine_Chest_Guide', 'Spine_End_Guide']
NECK = ['Neck_Guide', 'Head_Guide', 'HeadEnd_Guide']
UP, FRONT = (0, 1, 0), (0, 0, 1)
# where the Extra tab keeps the pose the rig was built in
POSE_NODE = 'webToRig_restPose'


def _quiet(percent, text):
    print('WebToRig {:3.0f}%  {}'.format(percent, text))


def read_manifest(folder):
    path = os.path.join(folder, MANIFEST)
    if not os.path.isfile(path):
        raise RuntimeError('{} not found in {}. Use the folder the website download unzipped to.'.format(MANIFEST, folder))
    with open(path, 'r') as handle:
        manifest = json.load(handle)
    if manifest.get('format') != 'mutant-tools-web-to-rig':
        raise RuntimeError('{} is not a joint placer download.'.format(path))
    return manifest


def _cm_factor():
    """The scene's linear unit per centimetre: the website writes centimetres."""
    return {'mm': 10.0, 'cm': 1.0, 'm': 0.01, 'in': 1 / 2.54, 'ft': 1 / 30.48, 'yd': 1 / 91.44}.get(
        cmds.currentUnit(query=True, linear=True), 1.0)


def _pos(node):
    return cmds.xform(node, query=True, worldSpace=True, translation=True)


# ---------------------------------------------------------------------------
# Stage 2: the character, on Manny, skinned

def import_character(folder, report=_quiet):
    manifest = read_manifest(folder)
    mesh_file = os.path.join(folder, manifest['mesh'])
    if not os.path.isfile(mesh_file):
        raise RuntimeError('The character file {} is missing from {}.'.format(manifest['mesh'], folder))

    report(5, 'Importing {}...'.format(manifest['mesh']))
    ext = os.path.splitext(mesh_file)[1].lower()
    if ext == '.fbx':
        cmds.loadPlugin('fbxmaya', quiet=True)
        # stand a Z-up file upright and convert its units; _align then turns it
        # to stand as the website showed it
        mel.eval('FBXResetImport; FBXImportMode -v add; FBXImportUpAxis y; FBXImportConvertUnitString cm;')
        new_nodes = cmds.file(mesh_file, i=True, type='FBX', ignoreVersion=True, returnNewNodes=True,
                              mergeNamespacesOnClash=False, namespace=':', options='v=0;')
    elif ext == '.obj':
        cmds.loadPlugin('objExport', quiet=True)
        new_nodes = cmds.file(mesh_file, i=True, type='OBJ', ignoreVersion=True, returnNewNodes=True,
                              options='mo=1')
    else:
        raise RuntimeError('Maya cannot import {} files. Load the FBX on the website instead.'.format(ext))
    new_nodes = cmds.ls(new_nodes or [], long=True) or []

    # the file may bring its own skeleton and skin: the website's replace them
    report(25, 'Removing the skeleton the file came with...')
    meshes = sorted(set(cmds.listRelatives(s, parent=True, fullPath=True)[0]
                        for s in cmds.ls(new_nodes, type='mesh', long=True) or []
                        if not cmds.getAttr(s + '.intermediateObject')))
    for mesh in meshes:
        for cluster in cmds.ls(cmds.listHistory(mesh) or [], type='skinCluster') or []:
            cmds.skinCluster(cluster, edit=True, unbind=True)
    old_joints = [j for j in cmds.ls(new_nodes, type='joint', long=True) or [] if cmds.objExists(j)]
    if old_joints:
        # a mesh parented under the old skeleton would go with it
        for i, mesh in enumerate(meshes):
            if any(mesh.startswith(j + '|') for j in old_joints):
                meshes[i] = cmds.ls(cmds.parent(mesh, world=True), long=True)[0]
        old_joints = [j for j in cmds.ls(new_nodes, type='joint', long=True) or [] if cmds.objExists(j)]
        tops = [j for j in old_joints if not any(j.startswith(o + '|') for o in old_joints)]
        cmds.delete(tops)

    report(35, 'Lining the character up with the skeleton...')
    _align(meshes, manifest.get('anchors') or {}, _cm_factor())

    report(45, 'Building the Manny skeleton...')
    from Mutant_Tools.Utils.Unreal import mannequin_utils
    reload(mannequin_utils)
    mannequin_utils.recreate_mannequin_from_json(os.path.join(folder, manifest['manny']))
    if cmds.objExists('root'):
        factor = _cm_factor()
        if factor != 1.0:
            cmds.scale(factor, factor, factor, 'root', relative=True, pivot=(0, 0, 0))

    pack = manifest.get('skin_pack')
    if pack:
        report(70, 'Skinning it to Manny...')
        from Mutant_Tools.Utils.IO import IOSkin
        reload(IOSkin)
        work = tempfile.mkdtemp(prefix='web_to_rig_')
        try:
            result = IOSkin.importSkinPack(_skin_pack_for(os.path.join(folder, pack), meshes, work)) or {}
        finally:
            shutil.rmtree(work, ignore_errors=True)
        problems = result.get('errors', []) + result.get('skipped_missing', [])
        if problems:
            cmds.warning('WebToRig skin: {}'.format('; '.join(problems)))
    else:
        cmds.warning('WebToRig: this download has no skin pack (the website could not read the file\'s vertex order).')

    report(100, 'Character imported on Manny: {} mesh(es).'.format(len(meshes)))
    return meshes


def _align(meshes, anchors, factor):
    """Put the imported character where the website showed it: Y up, facing
    front, in centimetres. Maya's FBX import stands a file up by the file's
    own axis settings, which can leave it turned from how the page had it, so
    the download says where some of its vertices were; the quarter turns,
    scale and offset that put them back there are applied to the import."""
    pairs, used = [], set()
    for name, data in anchors.items():
        mesh = _scene_mesh(name, data.get('vertices'), meshes, used)
        if mesh not in meshes:
            continue
        used.add(mesh)
        for i, x, y, z in data['points']:
            have = cmds.pointPosition('{}.vtx[{}]'.format(mesh, int(i)), world=True)
            pairs.append((have, (x * factor, y * factor, z * factor)))
    if len(pairs) < 3:
        cmds.warning('WebToRig: the download does not say where the character stood; it is left as imported.')
        return

    mean = lambda vs: [sum(v[k] for v in vs) / len(vs) for k in range(3)]
    cp, cq = mean([p for p, q in pairs]), mean([q for p, q in pairs])
    p0 = [[a - b for a, b in zip(p, cp)] for p, q in pairs]
    q0 = [[a - b for a, b in zip(q, cq)] for p, q in pairs]
    spread = sum(v * v for p in p0 for v in p)
    if spread < 1e-12:
        return
    scale = (sum(v * v for q in q0 for v in q) / spread) ** 0.5

    def error(turn):
        return sum((q[r] - scale * sum(turn[r][c] * p[c] for c in range(3))) ** 2
                   for p, q in zip(p0, q0) for r in range(3))
    turn = min(_quarter_turns(), key=error)
    height = max(q[1] for p, q in pairs) - min(q[1] for p, q in pairs)
    miss = (error(turn) / len(pairs)) ** 0.5
    if miss > 0.02 * max(height, 1e-6):
        cmds.warning('WebToRig: the character lines up with the skeleton only to within {:.1f} units.'.format(miss))

    shift = [cq[r] - scale * sum(turn[r][c] * cp[c] for c in range(3)) for r in range(3)]
    if turn == [[1, 0, 0], [0, 1, 0], [0, 0, 1]] and abs(scale - 1) < 1e-4 and max(map(abs, shift)) < 1e-3:
        return
    # Maya's matrices act on row vectors: the turn goes in transposed
    matrix = [scale * turn[c][r] for r in range(3) for c in range(3)]
    matrix = matrix[0:3] + [0] + matrix[3:6] + [0] + matrix[6:9] + [0] + shift + [1]
    tops = [a for a in cmds.ls(assemblies=True, long=True) or []
            if any(m == a or m.startswith(a + '|') for m in meshes)]
    holder = cmds.group(empty=True, world=True, name='webToRig_align')
    cmds.parent(tops, holder)
    cmds.xform(holder, worldSpace=True, matrix=matrix)
    cmds.parent(cmds.listRelatives(holder, children=True, fullPath=True), world=True)
    cmds.delete(holder)


def _quarter_turns():
    """The 24 rotations that map axes onto axes."""
    turns = []
    for order in itertools.permutations(range(3)):
        for signs in itertools.product((1, -1), repeat=3):
            m = [[0] * 3 for _ in range(3)]
            for row, (col, sign) in enumerate(zip(order, signs)):
                m[row][col] = sign
            det = (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
                   + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
            if det > 0:
                turns.append(m)
    return turns


def _skin_pack_for(pack_path, meshes, work):
    """A copy of the skin pack in `work` whose jSkins name the meshes as this
    scene does: Maya's FBX import renames what it cannot use (Body.001 comes in
    as BodyFBXASC046001), and a name may already be taken."""
    with open(pack_path, 'r') as handle:
        pack = json.load(handle)
    files, used = [], set()
    for i, name in enumerate(pack['packFiles']):
        with open(os.path.join(os.path.dirname(pack_path), name), 'r') as handle:
            skin = json.load(handle)
        for data in skin['objDDic']:
            data['objName'] = _scene_mesh(data['objName'], data.get('vertexCount'), meshes, used)
            used.add(data['objName'])
        skin['objs'] = [data['objName'] for data in skin['objDDic']]
        out = '{:02d}_{}'.format(i, os.path.basename(name))
        with open(os.path.join(work, out), 'w') as handle:
            json.dump(skin, handle)
        files.append(out)
    path = os.path.join(work, os.path.basename(pack_path))
    with open(path, 'w') as handle:
        json.dump({'packFiles': files, 'rootPath': ''}, handle)
    return path


def _scene_mesh(name, vertex_count, meshes, used):
    """The imported mesh a jSkin's objName means, by name if Maya kept it
    recognisable, else by its vertex count."""
    free = [m for m in meshes if m not in used]
    short = lambda m: m.split('|')[-1]
    decoded = lambda m: re.sub(r'FBXASC(\d{3})', lambda c: chr(int(c.group(1))), short(m))
    clean = re.sub(r'\W', '_', name)
    for match in (lambda m: short(m) == name, lambda m: decoded(m) == name, lambda m: short(m) == clean,
                  lambda m: re.match(re.escape(clean) + r'\d+$', short(m))):
        found = [m for m in free if match(m)]
        if len(found) == 1:
            return found[0]
    found = [m for m in free if cmds.polyEvaluate(m, vertex=True) == vertex_count]
    return found[0] if len(found) == 1 else name


# ---------------------------------------------------------------------------
# Stage 3: the template guides, where the website placed them

def place_template(folder, report=_quiet):
    manifest = read_manifest(folder)
    with open(os.path.join(folder, manifest['skeleton']), 'r') as handle:
        guides = json.load(handle).get('guides', {})

    if cmds.objExists('Mutant_Build'):
        raise RuntimeError('There is already a Mutant_Build group in the scene. Rename it or start a new scene.')
    report(10, 'Importing the {} guides...'.format(manifest.get('template', 'HumanUnrealGameTemplate')))
    cmds.file(TEMPLATE_FILE, i=True, type='mayaAscii', ignoreVersion=True)

    factor = _cm_factor()
    targets = dict((g, [v * factor for v in p]) for g, p in guides.items() if cmds.objExists(g))
    targets.update(_follow_head(targets))

    # parents first: moving a guide carries its children along, then each
    # child is put where it goes
    order = sorted(targets, key=lambda g: cmds.ls(g, long=True)[0].count('|'))
    skipped = []
    for i, guide in enumerate(order):
        try:
            cmds.xform(guide, worldSpace=True, translation=targets[guide])
        except Exception:
            skipped.append(guide)
        if i % 8 == 0:
            report(20 + 60.0 * i / max(len(order), 1), 'Placing guides: {} of {}'.format(i, len(order)))
    if skipped:
        cmds.warning('WebToRig: could not move {} guide(s): {}'.format(len(skipped), ', '.join(skipped)))

    report(85, 'Aiming the guides down their chains...')
    orient_guides()

    # the face's eyelid and lip blocks are built on edges picked on the mesh,
    # so the first build is the body: the face blocks are switched off (the
    # Auto Rigger shows them dimmed) until their edges are set
    face = cmds.listRelatives(FACE_GROUP, children=True) if cmds.objExists(FACE_GROUP) else None
    for block in face or []:
        if cmds.objExists(block + '.lodVisibility'):
            cmds.setAttr(block + '.lodVisibility', False)
    cmds.select(clear=True)
    report(100, 'Placed {} guides. Check them, then build.'.format(len(order) - len(skipped)))
    return order


def _follow_head(targets):
    """Where the face and eye guides go: the template's, moved with the head
    and scaled to it, since the website places the body only."""
    if not ('Head_Guide' in targets and 'HeadEnd_Guide' in targets):
        return {}
    head0, top0 = _pos('Head_Guide'), _pos('HeadEnd_Guide')
    head1, top1 = targets['Head_Guide'], targets['HeadEnd_Guide']
    size0 = sum((a - b) ** 2 for a, b in zip(top0, head0)) ** 0.5
    if size0 < 1e-6:
        return {}
    scale = sum((a - b) ** 2 for a, b in zip(top1, head1)) ** 0.5 / size0
    out = {}
    for group in HEAD_FOLLOWERS:
        if not cmds.objExists(group):
            continue
        for node in cmds.ls(cmds.listRelatives(group, allDescendents=True, fullPath=True) or [], type='transform'):
            name = node.split('|')[-1]
            if name.endswith('_Guide') and name not in targets:
                out[name] = [h1 + scale * (p - h0) for h0, h1, p in zip(head0, head1, _pos(node))]
    return out


def orient_guides():
    """Aim the template's guides down their chains, with the axes Mutant Tools'
    own guide placement gives them (Utils/Wrap/wrap_utils.py), moving none.
    The arm and leg guides stay as they are: the limb block orients its joints
    from their positions."""
    for guide in SPINE + NECK:
        if cmds.objExists(guide):
            x, y, z = _pos(guide)
            _keeping_below(guide, lambda: cmds.xform(guide, worldSpace=True, translation=(0, y, z)))
    _aim_chain(SPINE, (1, 0, 0), (0, 1, 0), FRONT)
    _aim_chain(NECK, (1, 0, 0), (0, 1, 0), FRONT)
    _aim_chain(['L_Clavicle_Guide', 'L_Shoulder_Guide'], (1, 0, 0), (0, 0, -1), UP, last=False)
    if cmds.objExists('L_Pelvis_Guide'):
        _keeping_below('L_Pelvis_Guide', lambda: cmds.rotate(0, 0, 0, 'L_Pelvis_Guide'))

    _aim_chain(['L_Foot_Ankle_Guide', 'L_Foot_Ball_Guide'], (0, 1, 0), (-1, 0, 0), UP, last=False)
    _aim_chain(['L_Foot_Ball_Guide', 'L_Foot_Toes_Guide'], (1, 0, 0), (0, 1, 0), UP, last=False)
    for pivot, target, aim, up in (('L_Foot_Heel_Guide', 'L_Foot_Toes_Guide', (0, 0, 1), (0, 1, 0)),
                                   ('L_Foot_HeelMid_Guide', 'L_Foot_Toes_Guide', (0, 0, 1), (0, 1, 0)),
                                   ('L_Foot_Out_Guide', 'L_Foot_BallFloor_Guide', (-1, 0, 0), (0, 1, 0)),
                                   ('L_Foot_In_Guide', 'L_Foot_BallFloor_Guide', (1, 0, 0), (0, 1, 0)),
                                   ('L_Foot_BallFloor_Guide', 'L_Foot_Toes_Guide', (0, 1, 0), (0, 0, 1))):
        _aim(pivot, target, aim, up, UP)
    _orient_like('L_Foot_Toes_Guide', 'L_Foot_HeelMid_Guide')

    # the fingers bend toward the palm whatever pose the hand is in
    back = _back_of_hand()
    _aim_chain(['L_Hand_Palm_Guide', 'L_Hand_Middle_01_Guide'], (1, 0, 0), (0, 1, 0), back, last=False)
    for finger in ('Index', 'Middle', 'Ring', 'Pinky', 'Thumb'):
        joints = 4 if finger == 'Thumb' else 5
        _aim_chain(['L_Hand_{}_{:02d}_Guide'.format(finger, i) for i in range(joints)], (1, 0, 0), (0, 1, 0), back)
    outer = 'L_Hand_Pinky_00_Guide' if cmds.objExists('L_Hand_Pinky_00_Guide') else 'L_Hand_Ring_00_Guide'
    _aim_chain(['L_Hand_InnerCup_Guide', 'L_Hand_Thumb_00_Guide'], (1, 0, 0), (0, 1, 0), back, last=False)
    _aim_chain(['L_Hand_OutterCup_Guide', outer], (1, 0, 0), (0, 1, 0), back, last=False)

    if all(cmds.objExists(n) for n in ('COG_Loc', 'Spine_Base_Guide', 'Spine_Root_Guide')):
        middle = [(a + b) / 2.0 for a, b in zip(_pos('Spine_Base_Guide'), _pos('Spine_Root_Guide'))]
        _keeping_below('COG_Loc', lambda: cmds.xform('COG_Loc', worldSpace=True, translation=middle))


def _keeping_below(node, change):
    """Run `change` on a guide, then put every guide under it back where it
    was, so turning a parent never moves its children."""
    below = cmds.ls(cmds.listRelatives(node, allDescendents=True, fullPath=True) or [], type='transform', long=True)
    kept = [(n, cmds.xform(n, query=True, worldSpace=True, matrix=True))
            for n in sorted(below, key=lambda n: n.count('|'))]
    try:
        change()
    except Exception as error:
        cmds.warning('WebToRig: could not orient {} ({})'.format(node, error))
    for child, matrix in kept:
        try:
            cmds.xform(child, worldSpace=True, matrix=matrix)
        except Exception:
            pass


def _aim(guide, target, aim, up, world_up):
    # at a locator where the target is: the target is often the guide's own
    # child, which would turn with it
    if cmds.objExists(guide) and cmds.objExists(target):
        spot = _stand_in(target)
        try:
            _keeping_below(guide, lambda: cmds.delete(cmds.aimConstraint(
                spot, guide, aimVector=aim, upVector=up, worldUpType='vector', worldUpVector=world_up)))
        finally:
            cmds.delete(spot)


def _orient_like(guide, source):
    if cmds.objExists(guide) and cmds.objExists(source):
        spot = _stand_in(source)
        try:
            _keeping_below(guide, lambda: cmds.delete(cmds.orientConstraint(spot, guide)))
        finally:
            cmds.delete(spot)


def _stand_in(node):
    """A locator where a guide is and turned as it is, outside every hierarchy."""
    spot = cmds.spaceLocator(name='webToRig_tmp')[0]
    cmds.xform(spot, worldSpace=True, matrix=cmds.xform(node, query=True, worldSpace=True, matrix=True))
    return spot


def _aim_chain(chain, aim, up, world_up, last=True):
    """Each guide aims at the next; the last turns like the one before it."""
    chain = [g for g in chain if cmds.objExists(g)]
    for guide, target in zip(chain, chain[1:]):
        _aim(guide, target, aim, up, world_up)
    if last and len(chain) > 1:
        _orient_like(chain[-1], chain[-2])


def _back_of_hand():
    """Which way the back of the left hand faces, from its knuckles: up for a
    T-pose with the palms down."""
    def at(*names):
        for name in names:
            if cmds.objExists(name):
                return _pos(name)
    palm = at('L_Hand_Palm_Guide', 'L_Wrist_Guide')
    first = at('L_Hand_Index_01_Guide', 'L_Hand_Middle_01_Guide')
    last = at('L_Hand_Pinky_01_Guide', 'L_Hand_Ring_01_Guide')
    if palm and first and last:
        a = [f - p for f, p in zip(first, palm)]
        b = [l - p for l, p in zip(last, palm)]
        n = (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
        length = sum(v * v for v in n) ** 0.5
        if length > 1e-6:
            return tuple(v / length for v in n)
    return UP


# ---------------------------------------------------------------------------
# Stage 4: the rig, driving Manny

def build_rig(report=_quiet):
    if not cmds.objExists('Mutant_Build'):
        raise RuntimeError('Place the template first: there is no Mutant_Build in the scene.')
    report(5, 'Building the Mutant Tools rig, block by block...')
    from Mutant_Tools.UI.AutoRigger import load_autoRigger
    reload(load_autoRigger)
    builder = load_autoRigger.AutoRigger()
    # the build opens its log only when a block fails (it then undoes itself)
    failed, show_log = [], builder.view_log
    builder.view_log = lambda: (failed.append(True), show_log())
    finished = builder.build_autorigger(only_progressbar=True)
    try:
        builder.close()
    except Exception:
        pass
    if failed or not cmds.objExists('Spine_Root_Bnd'):
        revert = cmds.optionVar(query='mutant_revert_on_fail') if cmds.optionVar(exists='mutant_revert_on_fail') else True
        raise RuntimeError('The Mutant Tools build stopped; its log says which block failed. {}'.format(
            'The scene goes back to the placed template.' if revert else
            'The scene is left where the build stopped (Revert on Fail is off).'))
    if finished is False:
        raise RuntimeError('Build cancelled.')

    report(85, 'Driving the Manny skeleton with the rig...')
    driven, missing = connect_manny()
    # a new rig has a new rest pose
    if cmds.objExists(POSE_NODE):
        cmds.delete(POSE_NODE)
    report(100, 'Rig built. {} Manny joints follow it.'.format(len(driven)))
    if missing:
        cmds.warning('WebToRig: not driven, joint missing: {}'.format(', '.join(missing)))
    return driven


def connect_manny():
    """Constrain each Manny joint to its Mutant Tools bind joint, both sides,
    keeping the offset: the two skeletons' joint orientations differ. Manny
    joints left out follow their parent."""
    from Mutant_Tools.Utils.Unreal import mannequin_utils
    if cmds.objExists('root'):
        # a rebuild: the old rig's constraints go first
        for kind in ('parentConstraint', 'scaleConstraint'):
            old = cmds.listRelatives('root', allDescendents=True, type=kind, fullPath=True) or []
            if old:
                cmds.delete(old)
    pairs = []
    for manny, bind in mannequin_utils.rig_map.items():
        pairs.append((manny, bind))
        if manny.endswith('_l'):
            pairs.append((mannequin_utils.replace_last_l_with_r(manny), bind.replace('L_', 'R_', 1)))
    driven, missing = [], []
    for manny, bind in pairs:
        if not (cmds.objExists(manny) and cmds.objExists(bind)):
            missing.append('{} <- {}'.format(manny, bind))
            continue
        cmds.parentConstraint(bind, manny, maintainOffset=True)
        cmds.scaleConstraint(bind, manny, maintainOffset=True)
        driven.append(manny)
    # spine_03 has no bind joint of its own: halfway between belly and chest
    if cmds.objExists('spine_03') and cmds.objExists('Spine_Belly_Bnd') and cmds.objExists('Spine_Chest_Bnd'):
        cmds.parentConstraint('Spine_Belly_Bnd', 'Spine_Chest_Bnd', 'spine_03', maintainOffset=True)
        driven.append('spine_03')
    # Unreal's IK bones follow the hands and feet
    for ik, target in (('ik_foot_l', 'foot_l'), ('ik_foot_r', 'foot_r'), ('ik_hand_l', 'hand_l'),
                       ('ik_hand_r', 'hand_r'), ('ik_hand_gun', 'hand_r')):
        if cmds.objExists(ik) and cmds.objExists(target):
            cmds.parentConstraint(target, ik, maintainOffset=True)
            driven.append(ik)
    return driven, missing


# ---------------------------------------------------------------------------
# Extra: animation on the rig

def animations():
    """The Mixamo animations Mutant Tools ships, by name."""
    names = [os.path.splitext(os.path.basename(p))[0] for p in glob.glob(os.path.join(MIXAMO_FOLDER, '*.json'))]
    return sorted(n for n in names if not n.endswith('_map'))


def apply_animation(name, report=_quiet):
    """Key one of Mutant Tools' Mixamo animations onto the rig's FK controls,
    as the Anim Loader does: the skinned character follows through Manny."""
    if not cmds.objExists('Mutant_Tools_Grp'):
        raise RuntimeError('Build the rig first.')
    # the first animation remembers the pose the rig was built in; a later
    # one starts from it again
    if cmds.objExists(POSE_NODE):
        remove_animation()
    else:
        _keep_pose()
    report(10, 'Keying {} on the controls...'.format(name))
    from Mutant_Tools.Utils.Mocap.Retarget import retarget
    reload(retarget)
    keyer = retarget.Retarget()
    # the map names the controls of Mutant Tools' own biped: a template
    # without some of them is keyed on the rest
    missing = sorted(set(c for c in keyer.rig_map.values() if c and not cmds.objExists(c)))
    keyer.rig_map = dict((k, c if c and cmds.objExists(c) else '') for k, c in keyer.rig_map.items())
    if not any(keyer.rig_map.values()):
        raise RuntimeError('This rig has none of the controls the Mixamo animations key.')
    # it steps through every frame: without redrawing each one it is much faster
    interactive = not cmds.about(batch=True)
    if interactive:
        cmds.refresh(suspend=True)
    try:
        keyer.load_mixamo_animation(anim_file=name)
    finally:
        if interactive:
            cmds.refresh(suspend=False)
    if missing:
        cmds.warning('WebToRig: not keyed, no such control: {}'.format(', '.join(missing)))
    start, end = cmds.playbackOptions(query=True, minTime=True), cmds.playbackOptions(query=True, maxTime=True)
    report(100, '{} is on the rig, frames {:.0f} to {:.0f}. Press play.'.format(name, start, end))
    return missing


def remove_animation():
    """The keys come off every control and its switches, and each value goes
    back to what it was before the first animation. (Tested headless, the IK
    limbs of the HumanUnrealGameTemplate rig still settle a few centimetres
    from their build pose afterwards: state inside the rig, not the controls.)"""
    if not cmds.objExists(POSE_NODE):
        from Mutant_Tools.Utils.Mocap.Retarget import retarget
        reload(retarget)
        retarget.Retarget().restore_scene()
        return
    pose = json.loads(cmds.getAttr(POSE_NODE + '.pose') or '{}')
    nodes = [n for n in sorted(set(plug.rsplit('.', 1)[0] for plug in pose)) if cmds.objExists(n)]
    if nodes:  # with no nodes, cutKey would take the selection
        cmds.cutKey(nodes, clear=True)
    for plug, value in pose.items():
        try:
            cmds.setAttr(plug, value)
        except Exception:
            pass


def _keep_pose():
    """Write down every control's and switch's values (keyable, in the
    channel box, and the rig's own attributes like the IK/FK switches), in
    the scene, for remove_animation."""
    pose = {}
    for ctrl in cmds.ls('*_Ctrl', type='transform', long=True) or []:
        for node in [ctrl] + (cmds.listRelatives(ctrl, shapes=True, fullPath=True) or []):
            for attr in set((cmds.listAttr(node, keyable=True, unlocked=True, scalar=True) or []) +
                            (cmds.listAttr(node, channelBox=True, unlocked=True, scalar=True) or []) +
                            (cmds.listAttr(node, userDefined=True, unlocked=True, scalar=True) or [])):
                plug = '{}.{}'.format(node, attr)
                try:
                    value = cmds.getAttr(plug)
                except Exception:
                    continue
                if isinstance(value, (bool, int, float)):
                    pose[plug] = value
    node = cmds.createNode('network', name=POSE_NODE)
    cmds.addAttr(node, longName='pose', dataType='string')
    cmds.setAttr(node + '.pose', json.dumps(pose), type='string')


def open_anim_loader():
    """Mutant Tools' Anim Loader, for the rest of its animation tools."""
    from Mutant_Tools.UI.AnimLoader import load_anim_loader
    reload(load_anim_loader)
    window = load_anim_loader.AnimLoaderUI()
    window.show()
    return window
