"""Build a cartoon walk-in-place cycle on a Mutant biped, from scratch, as editable key poses.

Runs INSIDE Maya. Clears the body/leg/arm keys it owns, keys one cycle
(contact, down, passing, up per step) and sets the curves to cycle, so the
animator edits one loop. Feet: heel strike pivoting on the heel, flat stance
sliding back at constant speed (treadmill), toe-off hinging on the ball with
the toes kept flat. Arms are posed in IK, then matched to FK and switched to FK.

    from Mutant_Tools.Dev.MayaMCP.retarget import cartoon_walk as cw
    cw.build(period=28, stride=26, lift=26, heel_z=-24)
"""
import math

import maya.cmds as mc
import maya.api.OpenMaya as om

from Mutant_Tools.Dev.MayaMCP.retarget import anim_polish as ap

TAU = 2 * math.pi
TR = ('tx', 'ty', 'tz', 'rx', 'ry', 'rz')

# One step of the left foot over a 28-frame cycle (the right foot is shifted half a cycle):
# (frame, pivot, z as a fraction of half the stride, pivot lift as a fraction of `lift`,
#  pitch: + heel up / - toes up, toes: 'flat' | 'follow' | world pitch in degrees)
STEP = [
    (0, 'heel', 1.0, 0.0, -25, 'follow'),
    (1, 'heel', 0.872, 0.0, -12, 'follow'),
    (2, 'heel', 0.739, 0.0, 0, 'follow'),
    (4, 'heel', 0.478, 0.0, 0, 'follow'),
    (6, 'heel', 0.222, 0.0, 0, 'follow'),
    (8, 'heel', -0.039, 0.0, 0, 'follow'),
    (10, 'heel', -0.3, 0.0, 0, 'follow'),
    (11, 'ball', -0.428, 0.0, 0, 'flat'),
    (12, 'ball', -0.556, 0.0, 8, 'flat'),
    (13, 'ball', -0.689, 0.0, 18, 'flat'),
    (14, 'ball', -0.817, 0.0, 28, 'flat'),
    (15, 'ball', -0.95, 0.0, 38, 'flat'),
    (16, 'ball', -1.0, 0.167, 34, 12),
    (17, 'ball', -0.889, 0.389, 26, 18),
    (19, 'ball', -0.444, 0.778, 12, 'follow'),
    (21, 'ball', 0.111, 1.0, 0, 'follow'),
    (23, 'ball', 0.556, 0.833, -12, 'follow'),
    (25, 'heel', 0.889, 0.333, -22, 'follow'),
    (26, 'heel', 1.028, 0.139, -26, 'follow'),
    (27, 'heel', 1.022, 0.044, -26, 'follow'),
]
BODY = ['COG_Ctrl', 'Spine_Bottom_Ik_Ctrl', 'Spine_Chest_FK_Ctrl', 'Spine_Belly_FK_Ctrl', 'Head_Ctrl', 'Belly_Ctrl']
LEGS = ['L_Ankle_Ik_Ctrl', 'R_Ankle_Ik_Ctrl', 'L_Foot_Toes_Ctrl', 'R_Foot_Toes_Ctrl']
ARMS_IK = ['L_Wrist_Ik_Ctrl', 'R_Wrist_Ik_Ctrl', 'L_Wrist_Ik_PoleVector_Ctrl', 'R_Wrist_Ik_PoleVector_Ctrl']


def _M(node):
    return om.MMatrix(mc.xform(node, q=True, ws=True, m=True))


def _T(v):
    m = om.MMatrix()
    m[12], m[13], m[14] = v[0], v[1], v[2]
    return m


def _Rx(deg):
    return om.MEulerRotation(math.radians(deg), 0, 0).asMatrix()


def _Rz(deg):
    return om.MEulerRotation(0, 0, math.radians(deg)).asMatrix()


def _pos(n):
    return mc.xform(n, q=True, ws=True, t=True)


def _joint(j):
    return ap._export_joint(j)


def _free(ctrl, a):
    return ap._free(ctrl, a)


def _setw(ctrl, W, rot_only=False):
    t0 = mc.getAttr(ctrl + '.t')[0]
    mc.xform(ctrl, ws=True, m=list(W))
    if rot_only:
        mc.setAttr(ctrl + '.t', *t0)
    for a in ('sx', 'sy', 'sz'):
        if _free(ctrl, a):
            mc.setAttr(ctrl + '.' + a, 1)


def _key(ctrl, f, attrs=TR):
    mc.setKeyframe(ctrl, at=[a for a in attrs if _free(ctrl, a)], t=f)


def build(period=28, stride=26.0, lift=26.0, heel_z=-24.0, ground=0.0, heel_round=0.058,
          bounce=(-8, -18, -15, -8, -1, -4), sway=6.0, hip_yaw=15.0, hip_roll=9.0,
          chest_yaw=20.0, chest_roll=7.0, chest_lean=8.0, chest_dip=6.0, head_nod=8.0, belly=4.0,
          swing=50.0, flop=32.0, arm_down=22.0, arm_reach=0.86, arm_pump=0.1, arms_fk=True,
          fingers=True, cycles=3):
    """Key the cycle on the open rig. Units: cm and degrees; frames per cycle = period.

    stride/lift: half the foot travel, and swing-foot lift, in cm. heel_z: back
    of the boot sole in world Z at rest. heel_round lowers the heel per degree
    of toe-up pitch (rounded heels). bounce: COG Y at contact, down, ...,
    up, settle within one step. Arms: swing (deg), down (closer to the body),
    reach (<1 bends the elbow), pump (extra bend on the forward swing).
    """
    s = period / 28.0
    owned = BODY + LEGS + ARMS_IK
    mc.cutKey(owned, at=list(TR), cl=True)
    for c in owned:
        for a in TR:
            if not mc.getAttr(c + '.' + a, lock=True):
                mc.setAttr(c + '.' + a, 0)
    for sw in ap.MUTANT_ARM_CHAINS:
        mc.cutKey(sw.split('.')[0], at=sw.split('.', 1)[1], cl=True)
        mc.setAttr(sw, 0)
    mc.currentTime(0)
    rest = {c: _M(c) for c in LEGS + ARMS_IK}
    sh0 = {S: _pos(_joint('upperarm_%s' % S.lower())) for S in 'LR'}
    ank0 = {S: _pos(_joint('foot_%s' % S.lower())) for S in 'LR'}
    ball0 = {S: _pos(_joint('ball_%s' % S.lower())) for S in 'LR'}

    # ------------------------------------------------------------ body
    half = period / 2.0
    bt = [0, 2, 4, 7, 10, 12]
    bkeys = list(zip([b * s for b in bt], bounce)) + [(half, bounce[0])]

    def cog_y(f):
        h = f % half
        for (a, va), (b, vb) in zip(bkeys, bkeys[1:]):
            if a <= h <= b:
                return va + (vb - va) * (h - a) / float(b - a)
        return bounce[0]

    body_frames = sorted(set(int(round(x * s)) for x in (0, 2, 4, 7, 10, 12, 14, 16, 18, 21, 24, 26)) | {period})
    for f in body_frames:
        mc.currentTime(f)
        t = f / float(period)
        cy = chest_yaw * math.cos(TAU * t)
        cr = -chest_roll * math.sin(TAU * t)
        cp = chest_lean + chest_dip * math.cos(2 * TAU * (t - 0.14))
        vals = {'COG_Ctrl': {'ty': cog_y(f), 'tx': sway * math.sin(TAU * t)},
                'Spine_Bottom_Ik_Ctrl': {'ry': -hip_yaw * math.cos(TAU * t), 'rz': hip_roll * math.sin(TAU * t)},
                'Spine_Chest_FK_Ctrl': {'rx': cp, 'ry': cy, 'rz': cr},
                'Spine_Belly_FK_Ctrl': {'ry': 0.4 * cy},
                'Head_Ctrl': {'rx': -0.8 * cp + head_nod * math.cos(2 * TAU * (t - 0.22)), 'ry': -0.85 * cy, 'rz': -0.7 * cr},
                'Belly_Ctrl': {'ty': belly * math.cos(2 * TAU * (t - 0.2)), 'tz': 0.3 * belly * math.cos(2 * TAU * (t - 0.25))}}
        for c, av in vals.items():
            if not mc.objExists(c):
                continue
            for a, v in av.items():
                mc.setAttr(c + '.' + a, v)
            _key(c, f, tuple(av))

    # ------------------------------------------------------------ feet
    def foot(S, f, piv, dz, dy, pitch, toes):
        ank, toe = '%s_Ankle_Ik_Ctrl' % S, '%s_Foot_Toes_Ctrl' % S
        dz *= stride
        dy *= lift
        a0, b0 = ank0[S], ball0[S]
        pivot = (a0[0], ground, heel_z) if piv == 'heel' else tuple(b0)   # ball: hinge on the ball joint
        if piv == 'heel':
            dy -= heel_round * abs(pitch)
        W = rest[ank] * _T((-pivot[0], -pivot[1], -pivot[2])) * _Rx(pitch) * _T((pivot[0], pivot[1] + dy, pivot[2] + dz))
        _setw(ank, W)
        mc.setAttr(toe + '.r', 0, 0, 0)
        tw = rest[toe] if toes == 'flat' else None if toes == 'follow' else rest[toe] * _Rx(toes)
        if tw is not None:
            _setw(toe, tw, rot_only=True)
        _key(ank, f)
        _key(toe, f, ('rx', 'ry', 'rz'))

    for S, shift in (('L', 0), ('R', period // 2)):
        rows = sorted(((int(round(r[0] * s)) + shift) % period,) + r[1:] for r in STEP)
        rows.append((period,) + rows[0][1:])
        for row in rows:
            mc.currentTime(row[0])
            foot(S, *row)

    # ------------------------------------------------------------ arms (posed in IK)
    arm_frames = sorted(set(int(round(x * s)) for x in (0, 3, 7, 10, 14, 17, 21, 24)) | {period})
    for f in arm_frames:
        mc.currentTime(f)
        t = f / float(period)
        for S, sgn in (('L', 1), ('R', -1)):
            th = sgn * swing * math.cos(TAU * (t - 0.05))          # + back, - forward
            fl = sgn * flop * math.cos(TAU * (t - 0.17))
            sh = _pos(_joint('upperarm_%s' % S.lower()))
            wr, pv = '%s_Wrist_Ik_Ctrl' % S, '%s_Wrist_Ik_PoleVector_Ctrl' % S
            rot = _Rz(-sgn * arm_down) * _Rx(th)
            fwd = max(0.0, -th / swing)
            reach = arm_reach - arm_pump * fwd + 0.05 * max(0.0, th / swing)
            h0, o = rest[wr], sh0[S]
            v = om.MVector(h0[12] - o[0], h0[13] - o[1], h0[14] - o[2]) * reach * rot
            hp = (sh[0] + v.x, sh[1] + v.y, sh[2] + v.z)
            W = om.MMatrix(h0) * _T((-h0[12], -h0[13], -h0[14])) * rot * _Rx(-25 * fwd) * _T(hp)
            W = W * _T((-hp[0], -hp[1], -hp[2])) * _Rx(fl * 0.6) * _T(hp)
            _setw(wr, W)
            pm = rest[pv] * _T((-o[0], -o[1], -o[2])) * rot * _T(sh)
            mc.xform(pv, ws=True, t=(pm[12], pm[13], pm[14]))
            _key(wr, f)
            _key(pv, f, ('tx', 'ty', 'tz'))

    curves = mc.listConnections(owned, s=True, d=False, type='animCurve') or []
    mc.filterCurve([c for c in curves if mc.nodeType(c) == 'animCurveTA'], filter='euler')
    ap.cycle_curves(owned)
    if arms_fk:
        ap.match_fk_to_ik(ap.MUTANT_ARM_CHAINS, arm_frames)
        ap.cycle_curves([c for chain in ap.MUTANT_ARM_CHAINS.values() for c, _ in chain])
    if fingers:
        _cyclic_fingers(period)
    mc.playbackOptions(min=0, max=period * cycles - 1, ast=0, aet=period * cycles - 1)
    mc.currentTime(0)


def _cyclic_fingers(period, drag=6.0, lag=0.22):
    """Relaxed fingers that trail the arm swing a little, as a looping cycle."""
    s = period / 28.0
    frames = sorted(set(int(round(x * s)) for x in (0, 4, 7, 11, 14, 18, 21, 25)) | {period})
    ctrls = []
    for S in ('L', 'R'):
        sgn = 1 if S == 'L' else -1
        rows = []
        for n, vals in ap.RELAXED_CURL.items():
            rows.append(('%s_Hand_%s_00_Ctrl' % (S, n), ap.RELAXED_CUP[n], 0.3))
            rows += [('%s_Hand_%s_0%d_Ctrl' % (S, n, k), v, 1.0) for k, v in zip((1, 2, 3), vals)]
        rows += [('%s_Hand_Thumb_0%d_Ctrl' % (S, k), v, 0.4) for k, v in zip((0, 1, 2), ap.RELAXED_THUMB)]
        for c, base, w in rows:
            if not mc.objExists(c):
                continue
            mc.cutKey(c, at=['rx', 'ry', 'rz'], cl=True)
            mc.setAttr(c + '.r', 0, 0, 0)
            for f in frames:
                t = f / float(period)
                mc.setKeyframe(c, at='rz', t=f, v=base + w * sgn * drag * math.cos(TAU * (t - lag)))
            ctrls.append(c)
    ap.cycle_curves(ctrls)
