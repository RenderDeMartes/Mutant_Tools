"""Retarget skeleton animation (Unreal / Mixamo FBX) onto a Mutant rig's controls.

Runs INSIDE Maya (live session through the bridge, or mayapy). See RETARGET.md.

The rig must carry an export skeleton with the same joint names as the source
(e.g. a Mutant rig whose game skeleton is constrained to the bind joints). Each
control's offset to the export joint it drives is measured once on the rig's
default pose; every frame the control is then solved in world space so that
the export joint lands on the source joint. No constraints are used, so
mirrored (negative-scale) controls do not flip.

    from Mutant_Tools.Dev.MayaMCP.retarget import skeleton_retarget as sr
    print(sr.compare_skeletons('|root', 'BIND:', rename={'head': 'head1'}))
    sr.retarget_fbx(base_scene, 'A_Run.fbx', 'Run.ma', sr.mutant_biped_map(),
                    switches=sr.MUTANT_BIPED_SWITCHES, rename={'head': 'head1'})
"""
import math
import os

import maya.cmds as mc
import maya.mel as mel
import maya.api.OpenMaya as om


# --------------------------------------------------------------------------
# Mapping preset: Mutant biped controls -> Unreal mannequin bone names
# --------------------------------------------------------------------------
MUTANT_BIPED_SWITCHES = {'L_Hip_Jnt_Switch_Ctrl.Switch_IK_FK': 0,
                         'R_Hip_Jnt_Switch_Ctrl.Switch_IK_FK': 0,
                         'L_Shoulder_Jnt_Switch_Ctrl.Switch_IK_FK': 0,
                         'R_Shoulder_Jnt_Switch_Ctrl.Switch_IK_FK': 0}


def mutant_biped_map(fk=True, fingers=True, cape=0):
    """(control, export joint, mode) rows for a Mutant biped on a UE skeleton.

    mode: 'parent' (translate+rotate), 'orient' (rotate only) or 'pole'
    (translate only; the joint is the middle joint of the limb). Rows are
    solved in order, so parents must come before the controls that follow
    them. fk=True also keys the FK controls, so the IK/FK switch keeps working.
    cape: number of Cape_0N_Ctrl -> Cape_0N rows to add.
    """
    rows = [
        ('Mover_Ctrl', 'root', 'parent'),
        ('COG_Ctrl', 'pelvis', 'parent'),
        ('Spine_Bottom_Ik_Ctrl', 'pelvis', 'parent'),
        ('Spine_Base_FK_Ctrl', 'spine_01', 'parent'),
        ('Spine_Belly_FK_Ctrl', 'spine_03', 'parent'),
        ('Spine_Chest_FK_Ctrl', 'spine_05', 'parent'),
        ('Neck_Ctrl', 'neck_01', 'parent'),
        ('Head_Ctrl', 'head', 'parent'),
    ]
    rows += [('Cape_0%d_Ctrl' % i, 'Cape_0%d' % i, 'parent') for i in range(1, cape + 1)]
    for S, s in (('L', 'l'), ('R', 'r')):
        rows.append(('%s_Clavicle_Ctrl' % S, 'clavicle_%s' % s, 'parent'))
        if fk:
            rows += [('%s_Shoulder_Fk_Ctrl' % S, 'upperarm_%s' % s, 'orient'),
                     ('%s_Elbow_Fk_Ctrl' % S, 'lowerarm_%s' % s, 'orient'),
                     ('%s_Wrist_Fk_Ctrl' % S, 'hand_%s' % s, 'orient'),
                     ('%s_Hip_Fk_Ctrl' % S, 'thigh_%s' % s, 'orient'),
                     ('%s_Knee_Fk_Ctrl' % S, 'calf_%s' % s, 'orient'),
                     ('%s_Ankle_Fk_Ctrl' % S, 'foot_%s' % s, 'orient')]
        rows += [('%s_Wrist_Ik_Ctrl' % S, 'hand_%s' % s, 'parent'),
                 ('%s_Wrist_Ik_PoleVector_Ctrl' % S, 'lowerarm_%s' % s, 'pole'),
                 ('%s_Ankle_Ik_Ctrl' % S, 'foot_%s' % s, 'parent'),
                 ('%s_Ankle_Ik_PoleVector_Ctrl' % S, 'calf_%s' % s, 'pole'),
                 ('%s_Foot_Toes_Ctrl' % S, 'ball_%s' % s, 'orient')]
        if fingers:
            for f in ('Index', 'Middle', 'Ring', 'Pinky'):
                rows.append(('%s_Hand_%s_00_Ctrl' % (S, f), '%s_metacarpal_%s' % (f.lower(), s), 'orient'))
                rows += [('%s_Hand_%s_0%d_Ctrl' % (S, f, k), '%s_0%d_%s' % (f.lower(), k, s), 'orient')
                         for k in (1, 2, 3)]
            rows += [('%s_Hand_Thumb_0%d_Ctrl' % (S, k), 'thumb_0%d_%s' % (k + 1, s), 'orient')
                     for k in (0, 1, 2)]
    return [r for r in rows if mc.objExists(r[0])]


# --------------------------------------------------------------------------
# Lookups
# --------------------------------------------------------------------------
def _mtx(node):
    return om.MMatrix(mc.xform(node, q=True, ws=True, m=True))


def _pos(node):
    return om.MVector(mc.xform(node, q=True, ws=True, t=True))


def export_joint(name, root='|root'):
    """Long name of joint `name` under the export skeleton `root`."""
    hits = [x for x in mc.ls(name, l=True, type='joint') if x == root or x.startswith(root + '|')]
    if not hits:
        raise RuntimeError('no joint %s under %s' % (name, root))
    return hits[0]


def source_joint(name, ns='SRC', rename=None):
    """Long name of the source joint for export-joint `name` (rename maps rig -> source names)."""
    n = (rename or {}).get(name, name)
    hits = mc.ls('%s:%s' % (ns, n), l=True, type='joint')
    if not hits:
        raise RuntimeError('no source joint %s:%s' % (ns, n))
    return hits[0]


def _free(ctrl, attrs):
    return [a for a in attrs if mc.getAttr(ctrl + '.' + a, se=True)]


# --------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------
def compare_skeletons(root='|root', ns='BIND', rename=None, top=20):
    """World-space differences between the export skeleton and an imported one.

    Import the source bind pose first (import_fbx(path, ns)). Returns lines
    'joint dist(cm) angle(deg)', worst first, plus joints missing either side.
    """
    out, missing = [], []
    for j in [root] + (mc.listRelatives(root, ad=True, type='joint', f=True) or []):
        name = j.split('|')[-1]
        try:
            s = source_joint(name, ns, rename)
        except RuntimeError:
            missing.append(name)
            continue
        out.append((math.dist(_pos(j), _pos(s)), _axis_angle(_mtx(j), _mtx(s)), name))
    out.sort(reverse=True)
    lines = ['%-28s %7.2f cm %6.1f deg' % (n, d, a) for d, a, n in out[:top]]
    if missing:
        lines.append('only on the rig: %s' % ', '.join(missing))
    return '\n'.join(lines)


def _axis_angle(ma, mb):
    worst = 0.0
    for r in range(3):
        va = om.MVector(ma[r * 4], ma[r * 4 + 1], ma[r * 4 + 2])
        vb = om.MVector(mb[r * 4], mb[r * 4 + 1], mb[r * 4 + 2])
        if va.length() > 1e-6 and vb.length() > 1e-6:
            worst = max(worst, math.degrees(va.angle(vb)))
    return worst


# --------------------------------------------------------------------------
# Import
# --------------------------------------------------------------------------
def import_fbx(path, ns='SRC', set_fps=True):
    """Import an FBX into namespace `ns`; returns (start, end) of its joint keys."""
    if not mc.pluginInfo('fbxmaya', q=True, l=True):
        mc.loadPlugin('fbxmaya')
    mc.namespace(set=':')
    if not mc.namespace(ex=ns):
        mc.namespace(add=ns)
    mc.namespace(set=ns)
    try:
        mel.eval('FBXResetImport; FBXImportMode -v add; FBXImportFillTimeline -v true;')
        mel.eval('FBXImportSetMayaFrameRate -v %s;' % ('true' if set_fps else 'false'))
        mel.eval('FBXImport -f "%s";' % path.replace('\\', '/'))
    finally:
        mc.namespace(set=':')
    keys = mc.keyframe(mc.ls('%s:*' % ns, type='joint'), q=True, tc=True) or [0]
    return int(math.floor(min(keys))), int(math.ceil(max(keys)))


def remove_namespace(ns):
    if mc.namespace(ex=ns):
        mc.delete(mc.ls('%s:*' % ns, assemblies=True) or [])
        mc.namespace(rm=ns, deleteNamespaceContent=True)


# --------------------------------------------------------------------------
# Solve
# --------------------------------------------------------------------------
def measure(mapping, root='|root'):
    """Measure control->export-joint offsets on the CURRENT pose (rig default).

    Returns per-row data used by solve(). Set IK/FK switches before calling.
    """
    data = []
    for ctrl, joint, mode in mapping:
        ej = export_joint(joint, root)
        row = {'ctrl': ctrl, 'joint': joint, 'mode': mode,
               'off': _mtx(ctrl) * _mtx(ej).inverse(),
               't0': mc.getAttr(ctrl + '.t')[0]}
        if mode == 'pole':
            up = mc.listRelatives(ej, p=True, f=True)[0]
            low = _limb_end(ej)
            row['dist'] = math.dist(_pos(ctrl), _pos(ej))
            # hinge axis: the export skeleton's bend normal, as an axis of the upper joint
            n = ((_pos(ej) - _pos(up)) ^ (_pos(low) - _pos(ej))).normal()
            um = _mtx(up)
            dots = [n * om.MVector(um[k * 4], um[k * 4 + 1], um[k * 4 + 2]).normal() for k in range(3)]
            k = max(range(3), key=lambda i: abs(dots[i]))
            row['hinge'] = (k, 1 if dots[k] > 0 else -1)
        if mode == 'pole':
            row['attrs'] = _free(ctrl, ['tx', 'ty', 'tz'])
        elif mode == 'orient':
            row['attrs'] = _free(ctrl, ['rx', 'ry', 'rz'])
        else:
            row['attrs'] = _free(ctrl, ['tx', 'ty', 'tz', 'rx', 'ry', 'rz'])
        data.append(row)
    return data


def _limb_end(mid):
    kids = [k for k in mc.listRelatives(mid, c=True, type='joint', f=True) or []
            if not any(t in k.split('|')[-1].split(':')[-1] for t in ('twist', 'corrective', 'Cor_'))]
    return kids[0]


def _pole_position(row, src_mid, last):
    """Pole on the source limb plane; a hyperextended limb keeps the hinge on its natural side."""
    up = mc.listRelatives(src_mid, p=True, f=True)[0]
    a, b, c = _pos(up), _pos(src_mid), _pos(_limb_end(src_mid))
    ac = c - a
    v = b - (a + ac * ((b - a) * ac / max(ac * ac, 1e-6)))
    k, sgn = row['hinge']
    um = _mtx(up)
    axis = om.MVector(um[k * 4], um[k * 4 + 1], um[k * 4 + 2]).normal()
    if v.length() < 1e-3:
        v = last.get(row['ctrl'], (axis * sgn) ^ ac)
    elif ((b - a) ^ (c - b)) * axis * sgn < 0:
        v = -v  # an IK hinge cannot bend backwards; flipping the pole would twist the limb 180
    last[row['ctrl']] = v
    return b + v.normal() * row['dist']


def solve(data, start, end, ns='SRC', rename=None, passes=2):
    """Key every mapped control, frame by frame, so the export skeleton follows the source."""
    rows = [dict(r, src=source_joint(r['joint'], ns, rename)) for r in data]
    last, attrs = {}, []
    for r in rows:
        attrs += [r['ctrl'] + '.' + a for a in r['attrs']]
    mc.refresh(suspend=True)
    try:
        for f in range(start, end + 1):
            mc.currentTime(f)
            # extra passes settle controls whose space follows a later control
            for _ in range(passes):
                for r in rows:
                    ctrl = r['ctrl']
                    if r['mode'] == 'pole':
                        p = _pole_position(r, r['src'], last)
                        mc.xform(ctrl, ws=True, t=(p.x, p.y, p.z))
                        continue
                    mc.xform(ctrl, ws=True, m=list(r['off'] * _mtx(r['src'])))
                    if r['mode'] == 'orient':
                        mc.setAttr(ctrl + '.t', *r['t0'])
                    for sa in ('sx', 'sy', 'sz'):
                        if mc.getAttr(ctrl + '.' + sa, se=True):
                            mc.setAttr(ctrl + '.' + sa, 1)
            for r in rows:
                mc.setKeyframe(r['ctrl'], at=r['attrs'], t=f)
    finally:
        mc.refresh(suspend=False)
    curves = [c for c in set(mc.listConnections(attrs, s=True, d=False, type='animCurve') or [])
              if mc.nodeType(c) == 'animCurveTA']
    if curves:
        mc.filterCurve(curves, filter='euler')


SKIP_VERIFY = ('ik_', 'interaction', 'center_of_mass', 'weapon')
SKIP_VERIFY_PARTS = ('twist', 'corrective', 'Cor_', 'scap', '_out_', 'pec', 'latissimus')


def verify(start, end, root='|root', ns='SRC', rename=None, samples=15, top=3):
    """Worst position (cm), rotation (deg) and bone-direction (deg) error over sampled frames.

    Rotation includes twist; bone direction ignores it. A large rotation error
    with a small bone-direction error is twist the rig does not reproduce
    (e.g. a no-roll upper arm), not a broken retarget.
    """
    pairs = []
    for j in [root] + (mc.listRelatives(root, ad=True, type='joint', f=True) or []):
        n = j.split('|')[-1]
        if n.startswith(SKIP_VERIFY) or any(p in n for p in SKIP_VERIFY_PARTS):
            continue
        try:
            pairs.append((n, j, source_joint(n, ns, rename)))
        except RuntimeError:
            pass
    pos, rot, aim = {}, {}, {}
    for f in range(start, end + 1, max(1, (end - start) // samples)):
        mc.currentTime(f)
        for n, j, s in pairs:
            pos[n] = max(pos.get(n, 0), math.dist(_pos(j), _pos(s)))
            rot[n] = max(rot.get(n, 0), _axis_angle(_mtx(j), _mtx(s)))
            kids = [k for k in mc.listRelatives(j, c=True, type='joint', f=True) or []
                    if not any(p in k.split('|')[-1] for p in SKIP_VERIFY_PARTS + ('weapon', 'Cape'))]
            if kids:
                kn = kids[0].split('|')[-1]
                try:
                    ks = source_joint(kn, ns, rename)
                except RuntimeError:
                    continue
                va, vb = _pos(kids[0]) - _pos(j), _pos(ks) - _pos(s)
                if va.length() > 1e-3 and vb.length() > 1e-3:
                    aim[n] = max(aim.get(n, 0), math.degrees(va.angle(vb)))

    def worst(d, unit):
        return ', '.join('%s=%.1f%s' % (k, v, unit) for k, v in sorted(d.items(), key=lambda kv: -kv[1])[:top])
    return 'pos: %s | rot: %s | boneDir: %s' % (worst(pos, 'cm'), worst(rot, 'deg'), worst(aim, 'deg'))


# --------------------------------------------------------------------------
# Pipeline
# --------------------------------------------------------------------------
def retarget_fbx(base_scene, fbx, out_ma, mapping_fn=mutant_biped_map, switches=None,
                 root='|root', rename=None, fps='ntsc', check_switches=True):
    """Open the clean rig, retarget one FBX onto its controls, save a .ma.

    mapping_fn: callable returning (control, joint, mode) rows (called after
    the scene opens). switches: {'node.attr': value} set (and keyed) before
    measuring, e.g. MUTANT_BIPED_SWITCHES for IK arms and legs.
    check_switches: also report the error with every switch flipped (FK).
    Returns a one-line report.
    """
    mc.file(base_scene, open=True, force=True)
    if fps:
        mc.currentUnit(time=fps)
    for plug, v in (switches or {}).items():
        mc.setAttr(plug, v)
    data = measure(mapping_fn(), root)
    start, end = import_fbx(fbx, 'SRC', set_fps=True)
    mc.playbackOptions(min=start, max=end, ast=start, aet=end)
    solve(data, start, end, 'SRC', rename)
    report = ['frames %d-%d' % (start, end), 'IK ' + verify(start, end, root, 'SRC', rename)]
    if switches and check_switches:
        for plug, v in switches.items():
            mc.setAttr(plug, 1 - v)
        report.append('FK ' + verify(start, end, root, 'SRC', rename))
    for plug, v in (switches or {}).items():
        mc.setAttr(plug, v)
        node, attr = plug.split('.', 1)
        mc.setKeyframe(node, at=attr, t=start)
    remove_namespace('SRC')
    mc.currentTime(start)
    d = os.path.dirname(out_ma)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    mc.file(rename=out_ma)
    mc.file(save=True, type='mayaAscii', force=True)
    return '%s: %s' % (os.path.basename(out_ma), ' | '.join(report))


def retarget_folder(base_scene, fbx_dir, out_dir, pattern_prefix='', **kw):
    """retarget_fbx() for every .fbx in fbx_dir (optionally only names starting with a prefix)."""
    lines = []
    for name in sorted(os.listdir(fbx_dir)):
        if not name.lower().endswith('.fbx') or not name.startswith(pattern_prefix):
            continue
        out = os.path.join(out_dir, os.path.splitext(name)[0] + '.ma')
        try:
            lines.append(retarget_fbx(base_scene, os.path.join(fbx_dir, name), out, **kw))
        except Exception as e:  # keep going; report the failure in the summary
            lines.append('%s: FAILED %s' % (name, e))
    return '\n'.join(lines)
