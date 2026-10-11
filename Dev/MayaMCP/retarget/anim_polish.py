"""Polish retargeted (mocap) animation on a Mutant rig: cartoon feel, clean
foot contacts, relaxed hands, FK arms, and side-view review playblasts.

Runs INSIDE Maya (live session through the bridge, or mayapy). See RETARGET.md.

    from Mutant_Tools.Dev.MayaMCP.retarget import anim_polish as ap
    ap.cartoon_filter(ap.body_controls(), 0, 83, k=1.2)
    ap.plant_feet(ap.foot_setup('Boots'), 0, 83)
    ap.relax_fingers(0, 83)
    ap.match_fk_to_ik(ap.MUTANT_ARM_CHAINS, range(0, 84))
"""
import math
import os

import maya.cmds as mc
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma

TR = ('tx', 'ty', 'tz', 'rx', 'ry', 'rz')


def _M(node):
    return om.MMatrix(mc.xform(node, q=True, ws=True, m=True))


def _export_joint(name, root='|root'):
    return [x for x in mc.ls(name, l=True, type='joint') if x == root or x.startswith(root + '|')][0]


def _free(ctrl, attr):
    return (mc.objExists(ctrl + '.' + attr) and mc.getAttr(ctrl + '.' + attr, k=True)
            and not mc.getAttr(ctrl + '.' + attr, lock=True))


# --------------------------------------------------------------------------
# Mutant biped presets
# --------------------------------------------------------------------------
MUTANT_ARM_CHAINS = {
    'L_Shoulder_Jnt_Switch_Ctrl.Switch_IK_FK': [('L_Shoulder_Fk_Ctrl', 'upperarm_l'), ('L_Elbow_Fk_Ctrl', 'lowerarm_l'),
                                                ('L_Wrist_Fk_Ctrl', 'hand_l')],
    'R_Shoulder_Jnt_Switch_Ctrl.Switch_IK_FK': [('R_Shoulder_Fk_Ctrl', 'upperarm_r'), ('R_Elbow_Fk_Ctrl', 'lowerarm_r'),
                                                ('R_Wrist_Fk_Ctrl', 'hand_r')],
}
# finger curl is -rz on Mutant finger controls; cascade so the pinky curls most
RELAXED_CURL = {'Index': (-15, -25, -18), 'Middle': (-20, -30, -22), 'Ring': (-25, -33, -25), 'Pinky': (-30, -36, -28)}
RELAXED_CUP = {'Index': 0, 'Middle': -2, 'Ring': -4, 'Pinky': -7}
RELAXED_THUMB = (-4, -12, -18)


def body_controls(arms='fk', cape=7):
    """Controls the cartoon filter should touch on a Mutant biped (not Mover, not fingers)."""
    c = ['COG_Ctrl', 'Spine_Bottom_Ik_Ctrl', 'Spine_Base_FK_Ctrl', 'Spine_Belly_FK_Ctrl', 'Spine_Chest_FK_Ctrl',
         'Neck_Ctrl', 'Head_Ctrl', 'Belly_Ctrl']
    for S in ('L', 'R'):
        c += ['%s_Clavicle_Ctrl' % S, '%s_Ankle_Ik_Ctrl' % S, '%s_Foot_Toes_Ctrl' % S]
        if arms == 'fk':
            c += ['%s_Shoulder_Fk_Ctrl' % S, '%s_Elbow_Fk_Ctrl' % S, '%s_Wrist_Fk_Ctrl' % S]
        else:
            c += ['%s_Wrist_Ik_Ctrl' % S]
    c += ['Cape_0%d_Ctrl' % i for i in range(1, cape + 1)]
    return [x for x in c if mc.objExists(x)]


# --------------------------------------------------------------------------
# Curve helpers
# --------------------------------------------------------------------------
def _curves(ctrls, attrs=TR):
    out = []
    for c in ctrls:
        for a in attrs:
            if not _free(c, a):
                continue
            cv = mc.listConnections(c + '.' + a, s=True, d=False, type='animCurve')
            if cv:
                out.append(cv[0])
    return out


def _fn(curve):
    sel = om.MSelectionList()
    sel.add(curve)
    return oma.MFnAnimCurve(sel.getDependNode(0))


def _gauss(vals, sigma, cyclic):
    if sigma <= 0:
        return list(vals)
    r = int(math.ceil(3 * sigma))
    w = [math.exp(-0.5 * (i / float(sigma)) ** 2) for i in range(-r, r + 1)]
    n, out = len(vals), []
    for i in range(n):
        acc = ws = 0.0
        for k, wk in zip(range(-r, r + 1), w):
            j = i + k
            if cyclic:
                j %= n
            elif j < 0 or j >= n:
                j = min(max(j, 0), n - 1)
            acc += vals[j] * wk
            ws += wk
        out.append(acc / ws)
    return out


def _plugs(ctrls, attrs=TR):
    return [c + '.' + a for c in ctrls for a in attrs if _free(c, a)]


def _resample(plugs, start, end):
    """Make sure every plug's curve has one key per frame in [start, end] (bakes in place)."""
    if plugs:
        mc.bakeResults(plugs, t=(start, end), sb=1, simulation=False, preserveOutsideKeys=True)


# --------------------------------------------------------------------------
# Cartoon
# --------------------------------------------------------------------------
def cartoon_filter(ctrls, start, end, k=1.0, sigma=3.0, pre=1.0, cyclic=False, attrs=TR):
    """Cartoon Animation Filter (Wang et al. 2006): x' = x + k * (x - blur(x)).

    Adds anticipation, overshoot and follow-through while keeping slow,
    large motion (root travel, flips) unchanged. `pre` lightly smooths
    mocap jitter first so it is not amplified. cyclic wraps the blur for loops.
    """
    _resample(_plugs(ctrls, attrs), start, end)
    curves = _curves(ctrls, attrs)
    for cv in curves:
        def f(vals):
            x = _gauss(vals, pre, cyclic)
            b = _gauss(x, sigma, cyclic)
            return [xi + k * (xi - bi) for xi, bi in zip(x, b)]
        _edit_deg(cv, start, end, f)
    return len(curves)


def exaggerate(ctrls, start, end, factor=1.3, attrs=('rx', 'ry', 'rz')):
    """Scale each channel's motion about its average (for in-place loops)."""
    _resample(_plugs(ctrls, attrs), start, end)
    curves = _curves(ctrls, attrs)
    for cv in curves:
        def f(vals):
            m = sum(vals) / len(vals)
            return [m + factor * (v - m) for v in vals]
        _edit_deg(cv, start, end, f)
    return len(curves)


def _edit_deg(curve, start, end, func):
    """Rewrite the per-frame keys of `curve` in [start, end] with func(values).

    Angular values are handed to func, and expected back, in degrees.
    """
    fn = _fn(curve)
    tu = om.MTime.uiUnit()
    idx = {}
    for i in range(fn.numKeys):
        f = int(round(fn.input(i).asUnits(tu)))
        if start <= f <= end:
            idx[f] = i
    frames = sorted(idx)
    if len(frames) < 3:
        return
    angular = fn.animCurveType == oma.MFnAnimCurve.kAnimCurveTA
    vals = [fn.value(idx[f]) for f in frames]
    if angular:
        vals = [math.degrees(v) for v in vals]
    new = func(vals)
    for f, v in zip(frames, new):
        fn.setValue(idx[f], math.radians(v) if angular else v)


# --------------------------------------------------------------------------
# Feet
# --------------------------------------------------------------------------
def foot_setup(mesh, sides=(('L', 1), ('R', -1)), frame=None, band=20.0, max_points=300):
    """Sole geometry of each foot for plant_feet().

    Takes the mesh's vertices up to `band` cm above the sole on each side:
    the part behind the ball is stored in the ankle IK control's space, the
    part in front in the ball joint's space (it bends with the toes).
    'points' = heel, ball, toe sole points (control space) for the flat test.
    """
    if frame is not None:
        mc.currentTime(frame)
    pts = mc.xform(mesh + '.vtx[*]', q=True, ws=True, t=True)
    P = [om.MPoint(pts[i], pts[i + 1], pts[i + 2]) for i in range(0, len(pts), 3)]
    out = []
    for S, sgn in sides:
        ctrl = '%s_Ankle_Ik_Ctrl' % S
        ball_j = _export_joint('ball_%s' % S.lower())
        inv, binv = _M(ctrl).inverse(), _M(ball_j).inverse()
        side = [p for p in P if sgn * p.x > 0]
        loc = [p * inv for p in side]
        lo = min(p.y for p in loc)
        ball_z = (om.MPoint(mc.xform(ball_j, q=True, ws=True, t=True)) * inv).z
        back, front = [], []
        for pw, pl in zip(side, loc):
            if pl.y < lo + band:
                if pl.z < ball_z:
                    back.append(pl)
                else:
                    front.append(pw * binv)
        sole = [p for p in loc if p.y < lo + 1.5]
        heel = min(sole, key=lambda p: p.z)
        toe = max(sole, key=lambda p: p.z)
        ball = min(sole, key=lambda p: abs(p.z - ball_z))
        out.append({'ctrl': ctrl, 'toes': '%s_Foot_Toes_Ctrl' % S, 'ball': ball_j, 'points': [heel, ball, toe],
                    'back': back[::max(1, len(back) // max_points)], 'front': front[::max(1, len(front) // max_points)]})
    return out


def _yaw_only(W):
    """Keep position and heading; drop pitch and roll (flat on the ground)."""
    z = om.MVector(W[8], 0, W[10])
    if z.length() < 1e-6:
        return om.MMatrix(W)
    sx = om.MVector(W[0], W[1], W[2]).length()
    sy = om.MVector(W[4], W[5], W[6]).length()
    sz = om.MVector(W[8], W[9], W[10]).length()
    det = W.det3x3()
    z = z.normal()
    y = om.MVector(0, 1, 0)
    x = y ^ z
    if det < 0:
        x = -x
    return om.MMatrix([x.x * sx, x.y * sx, x.z * sx, 0, y.x * sy, y.y * sy, y.z * sy, 0,
                       z.x * sz, z.y * sz, z.z * sz, 0, W[12], W[13], W[14], 1])


def _scale_delta(m, w):
    """A rigid offset matrix scaled by w (0 = identity, 1 = m): slerped rotation, lerped translation."""
    tm = om.MTransformationMatrix(m)
    q = om.MQuaternion.slerp(om.MQuaternion(), tm.rotation(asQuaternion=True), w)
    t = tm.translation(om.MSpace.kTransform) * w
    out = om.MTransformationMatrix()
    out.setRotation(q)
    out.setTranslation(t, om.MSpace.kTransform)
    return out.asMatrix()


def plant_feet(feet, start, end, ground=0.0, contact=3.0, speed=3.0, lock_travel=12.0, flat=5.0, min_run=3, blend=0):
    """Clean foot contacts on ankle IK controls (feet from foot_setup()).

    A frame is in contact when the sole is within `contact` of the ground and
    the ankle moves less than `speed` per frame. In a contact run the sole is
    put on the ground, flattened (toes straight too) when heel and ball are
    both down (within `flat`), and pinned in place if the run travels less
    than `lock_travel` (treadmill/in-place slides keep sliding). Every frame
    is also pushed out of the ground. The correction fades in and out over
    `blend` frames around each run (off by default: blending between short runs can swing the knee). Returns the
    contact runs per foot.
    """
    report = {}
    for foot in feet:
        ctrl, toes, ball = foot['ctrl'], foot['toes'], foot['ball']
        pts, back, front = foot['points'], foot['back'], foot['front']
        W, B = {}, {}
        for f in range(start, end + 1):
            mc.currentTime(f)
            W[f] = _M(ctrl)
            B[f] = _M(ball) * W[f].inverse()           # ball relative to the control: unaffected by moving it

        def low(m, b):
            lo = min((p * m).y for p in back) if back else 1e9
            if front:
                bm = b * m
                lo = min(lo, min((p * bm).y for p in front))
            return lo - ground

        def heel_ball(m):
            return [(p * m).y - ground for p in pts[:2]]

        cont = []
        for f in range(start, end + 1):
            prev, nxt = W.get(f - 1, W[f]), W.get(f + 1, W[f])
            v = max(math.hypot(W[f][12] - prev[12], W[f][14] - prev[14]), math.hypot(nxt[12] - W[f][12], nxt[14] - W[f][14]))
            cont.append(low(W[f], B[f]) < contact and v < speed)
        runs, f0 = [], None
        for i, c in enumerate(cont + [False]):
            if c and f0 is None:
                f0 = i
            elif not c and f0 is not None:
                if i - f0 >= min_run:
                    runs.append((start + f0, start + i - 1))
                f0 = None
        target, flatten = {}, set()
        for a, b in runs:
            xs = [W[f][12] for f in range(a, b + 1)]
            zs = [W[f][14] for f in range(a, b + 1)]
            lock = max(math.hypot(x - xs[0], z - zs[0]) for x, z in zip(xs, zs)) < lock_travel
            lx, lz = sum(xs) / len(xs), sum(zs) / len(zs)
            for f in range(a, b + 1):
                m = om.MMatrix(W[f])
                h = heel_ball(m)
                up = om.MVector(m[4], m[5], m[6]).normal()
                if abs(h[0] - h[1]) < flat and up.y > 0.7:      # only a foot that is right way up
                    m = _yaw_only(m)
                    flatten.add(f)
                if lock:
                    m[12], m[14] = lx, lz
                target[f] = m
        # fade the run's correction (as a local offset of the control) in and out
        fades = {}
        for a, b in runs:
            for edge, step in ((a, -1), (b, 1)):
                delta = target[edge] * W[edge].inverse()
                for i in range(1, blend + 1):
                    f = edge + step * i
                    if f < start or f > end or f in target:
                        continue
                    w = 1.0 - i / float(blend + 1)
                    if w > fades.get(f, (0, None))[0]:
                        fades[f] = (w, delta)
        for f, (w, delta) in fades.items():
            target[f] = _scale_delta(delta, w) * W[f]
        for f in range(start, end + 1):
            mc.currentTime(f)
            if f in flatten and mc.objExists(toes):
                for a in ('rx', 'ry', 'rz'):
                    if _free(toes, a):
                        mc.setAttr(toes + '.' + a, 0)
                mc.setKeyframe(toes, at=[a for a in ('rx', 'ry', 'rz') if _free(toes, a)], t=f)
            b_rel = _M(ball) * _M(ctrl).inverse()
            m = om.MMatrix(target.get(f, W[f]))
            lo = low(m, b_rel)
            if f in target or lo < 0:
                m[13] -= lo
            else:
                continue
            s0 = mc.getAttr(ctrl + '.s')[0]
            mc.xform(ctrl, ws=True, m=list(m))
            for a, v in zip(('sx', 'sy', 'sz'), s0):
                if _free(ctrl, a):
                    mc.setAttr(ctrl + '.' + a, v)
            mc.setKeyframe(ctrl, at=[a for a in TR if _free(ctrl, a)], t=f)
        report[ctrl] = runs
    return report


# --------------------------------------------------------------------------
# Hands and arms
# --------------------------------------------------------------------------
def relax_fingers(start, end, keep=0.4, curl=None, cup=None, thumb=None, sides=('L', 'R')):
    """Relaxed hand: curl cascade on -rz, keeping `keep` of the mocap motion around its average."""
    curl, cup, thumb = curl or RELAXED_CURL, cup or RELAXED_CUP, thumb or RELAXED_THUMB
    rows = []
    for S in sides:
        for n, vals in curl.items():
            rows.append(('%s_Hand_%s_00_Ctrl' % (S, n), cup[n]))
            rows += [('%s_Hand_%s_0%d_Ctrl' % (S, n, k), v) for k, v in zip((1, 2, 3), vals)]
        rows += [('%s_Hand_Thumb_0%d_Ctrl' % (S, k), v) for k, v in zip((0, 1, 2), thumb)]
    for ctrl, base in rows:
        if not mc.objExists(ctrl):
            continue
        for a in ('rx', 'ry', 'rz'):
            if not mc.listConnections(ctrl + '.' + a, s=True, d=False, type='animCurve'):
                mc.setKeyframe(ctrl, at=a, t=start)
        _resample(_plugs([ctrl], ('rx', 'ry', 'rz')), start, end)
        for cv in _curves([ctrl], ('rx', 'ry', 'rz')):
            target = base if cv.endswith(('rotateZ', 'rz')) else 0.0

            def f(vals, target=target):
                m = sum(vals) / len(vals)
                return [target + keep * (v - m) for v in vals]
            _edit_deg(cv, start, end, f)
    return len(rows)


def match_fk_to_ik(chains=None, frames=None, fk_value=1):
    """Key FK controls to the current IK pose on `frames`, then key the switch to FK.

    chains: {'switch.attr': [(fk_ctrl, export_joint), ...]} (parents first).
    Offsets are measured on the FK rest pose, so FK controls must be unkeyed
    at zero or will be cleared first.
    """
    chains = chains or MUTANT_ARM_CHAINS
    frames = list(frames)
    for plug, chain in chains.items():
        node = plug.split('.')[0]
        attr = plug.split('.', 1)[1]
        for c, _ in chain:
            mc.cutKey(c, at=['rx', 'ry', 'rz'], cl=True)
            mc.setAttr(c + '.r', 0, 0, 0)
        mc.cutKey(node, at=attr, cl=True)
        mc.setAttr(plug, fk_value)
        off = {c: _M(c) * _M(_export_joint(j)).inverse() for c, j in chain}
        mc.setAttr(plug, 1 - fk_value)
        pose = {}
        for f in frames:
            mc.currentTime(f)
            pose[f] = {j: _M(_export_joint(j)) for _, j in chain}
        mc.setAttr(plug, fk_value)
        for f in frames:
            mc.currentTime(f)
            for c, j in chain:
                t0 = mc.getAttr(c + '.t')[0]
                mc.xform(c, ws=True, m=list(off[c] * pose[f][j]))
                mc.setAttr(c + '.t', *t0)
                for a in ('sx', 'sy', 'sz'):
                    if _free(c, a):
                        mc.setAttr(c + '.' + a, 1)
                mc.setKeyframe(c, at=['rx', 'ry', 'rz'], t=f)
        mc.setKeyframe(node, at=attr, t=frames[0], v=fk_value)
        cv = mc.listConnections([c for c, _ in chain], s=True, d=False, type='animCurve') or []
        if cv:
            mc.filterCurve(cv, filter='euler')


def cycle_curves(ctrls):
    cv = mc.listConnections(ctrls, s=True, d=False, type='animCurve') or []
    if cv:
        mc.setInfinity(cv, pri='cycle', poi='cycle')


# --------------------------------------------------------------------------
# Limb stability: no elbow twist, no knee pops or flips
# --------------------------------------------------------------------------
MUTANT_LEGS = {'L': ('thigh_l', 'calf_l', 'foot_l', 'ball_l', 'L_Ankle_Ik_PoleVector_Ctrl'),
               'R': ('thigh_r', 'calf_r', 'foot_r', 'ball_r', 'R_Ankle_Ik_PoleVector_Ctrl')}


def _key_times(plugs, start, end):
    t = set()
    for p in plugs:
        t.update(int(round(x)) for x in (mc.keyframe(p, q=True, tc=True) or []))
    t = sorted(x for x in t if start <= x <= end)
    return t or list(range(start, end + 1))


def untwist_elbows(start, end, chains=None):
    """Make the FK elbow a hinge: drop its twist about the forearm and give it to the wrist.

    The hand keeps its world orientation; the forearm twist joints spread the
    twist instead of the elbow wringing. Works on the elbow's own key times.
    """
    chains = chains or MUTANT_ARM_CHAINS
    for chain in chains.values():
        elbow, wrist, hand = chain[1][0], chain[2][0], _export_joint(chain[2][1])
        frames = _key_times([elbow + '.r' + a for a in 'xyz'], start, end)
        mc.currentTime(frames[0])
        em = _M(elbow)
        b = om.MVector(mc.xform(wrist, q=True, ws=True, t=True)) - om.MVector(em[12], em[13], em[14])
        b = (b * om.MTransformationMatrix(em).asRotateMatrix().inverse()).normal()   # forearm axis, elbow space
        ro = mc.getAttr(elbow + '.rotateOrder')
        for f in frames:
            mc.currentTime(f)
            hw = _M(hand)
            off = _M(wrist) * hw.inverse()
            r = [math.radians(v) for v in mc.getAttr(elbow + '.r')[0]]
            q = om.MEulerRotation(r[0], r[1], r[2], ro).asQuaternion()
            d = q.x * b.x + q.y * b.y + q.z * b.z
            if q.w * q.w + d * d < 1e-12:
                continue
            tw = om.MQuaternion(b.x * d, b.y * d, b.z * d, q.w).normalizeIt()
            e = (tw.inverse() * q).asEulerRotation().reorderIt(ro)
            mc.setAttr(elbow + '.r', *[math.degrees(v) for v in (e.x, e.y, e.z)])
            t0 = mc.getAttr(wrist + '.t')[0]
            mc.xform(wrist, ws=True, m=list(off * hw))
            mc.setAttr(wrist + '.t', *t0)
            for a in ('sx', 'sy', 'sz'):
                if _free(wrist, a):
                    mc.setAttr(wrist + '.' + a, 1)
            mc.setKeyframe(elbow, at=['rx', 'ry', 'rz'], t=f)
            mc.setKeyframe(wrist, at=['rx', 'ry', 'rz'], t=f)
        cv = mc.listConnections([elbow, wrist], s=True, d=False, type='animCurveTA') or []
        if cv:
            mc.filterCurve(cv, filter='euler')


def clamp_leg_reach(start, end, legs=None, cog='COG_Ctrl', reach=0.97, sigma=2.0):
    """Lower the COG wherever a leg would straighten past `reach` of its length.

    A fully straight IK leg pops (and stretches); keeping it just short of
    straight stops the knee snapping. Feet stay where they are. Returns the
    largest drop in cm.
    """
    legs = legs or MUTANT_LEGS
    mc.currentTime(start)
    lengths = {}
    for S, (th, ca, fo, _, _) in legs.items():
        th, ca, fo = [_export_joint(j) for j in (th, ca, fo)]
        a, b, c = [om.MVector(mc.xform(j, q=True, ws=True, t=True)) for j in (th, ca, fo)]
        lengths[S] = ((b - a).length() + (c - b).length(), th, fo)
    need = []
    for f in range(start, end + 1):
        mc.currentTime(f)
        h = 0.0
        for L, th, fo in lengths.values():
            v = om.MVector(mc.xform(th, q=True, ws=True, t=True)) - om.MVector(mc.xform(fo, q=True, ws=True, t=True))
            r = reach * L
            xz = math.hypot(v.x, v.z)
            if v.length() > r and xz < r:
                h = max(h, v.y - math.sqrt(r * r - xz * xz))
        need.append(h)
    if max(need) <= 0:
        return 0.0
    grown = [max(need[max(0, i - 2):i + 3]) for i in range(len(need))]
    drop = [max(a, b) for a, b in zip(_gauss(grown, sigma, False), need)]
    _resample(_plugs([cog], ('ty',)), start, end)
    curve = mc.listConnections(cog + '.ty', s=True, d=False, type='animCurve')[0]
    _edit_deg(curve, start, end, lambda vals: [v - h for v, h in zip(vals, drop)])
    return max(need)


def knee_poles(start, end, legs=None, dist=50.0, foot_weight=0.5, pelvis='pelvis'):
    """Key each knee pole so the knee points between the body's front and the foot's (no flips).

    Both directions turn with the character (flips, rolls), are taken
    perpendicular to the hip-ankle line, and the result is kept continuous
    from frame to frame, so the pole never swaps sides.
    """
    legs = legs or MUTANT_LEGS
    pj = _export_joint(pelvis)
    mc.currentTime(start)
    # the pelvis axis that points forward (+Z) at rest is found on the clip's first frame
    pm = _M(pj)
    axes = [om.MVector(pm[i * 4], pm[i * 4 + 1], pm[i * 4 + 2]).normal() for i in range(3)]
    k = max(range(3), key=lambda i: abs(axes[i].z))
    sign = 1 if axes[k].z > 0 else -1
    for th, ca, fo, ba, pole in legs.values():
        th, ca, fo, ba = [_export_joint(j) for j in (th, ca, fo, ba)]
        mc.cutKey(pole, at=['tx', 'ty', 'tz'], cl=True)
        last = None
        for f in range(start, end + 1):
            mc.currentTime(f)
            a, kn, c, bl = [om.MVector(mc.xform(j, q=True, ws=True, t=True)) for j in (th, ca, fo, ba)]
            line = (c - a).normal()
            m = _M(pj)
            body = om.MVector(m[k * 4], m[k * 4 + 1], m[k * 4 + 2]) * sign
            foot = bl - c

            def perp(v):
                v = v - line * (v * line)
                return v.normal() if v.length() > 1e-4 else om.MVector()
            fwd = perp(body) * (1 - foot_weight) + perp(foot) * foot_weight
            if fwd.length() < 1e-3:
                fwd = last or perp(body)
            fwd = fwd.normal()
            if last is not None and fwd * last < 0.5:
                fwd = (fwd + last * 2).normal()      # no sudden swaps
            last = fwd
            ratio = (kn - a).length() / ((kn - a).length() + (c - kn).length())
            p = a + (c - a) * ratio + fwd * dist
            mc.xform(pole, ws=True, t=(p.x, p.y, p.z))
            mc.setKeyframe(pole, at=['tx', 'ty', 'tz'], t=f)


def fix_limbs(start=None, end=None, arms=True, reach=0.97, poles=True):
    """Elbow hinge (FK arms), no straight-leg pops, flip-free knee poles."""
    start = int(mc.playbackOptions(q=True, min=True)) if start is None else start
    end = int(mc.playbackOptions(q=True, max=True)) if end is None else end
    out = {}
    if reach:
        out['cog_lowered_cm'] = round(clamp_leg_reach(start, end, reach=reach), 1)
    if poles:
        knee_poles(start, end)
    if arms:
        untwist_elbows(start, end)
    mc.currentTime(start)
    return out


# --------------------------------------------------------------------------
# One call per clip
# --------------------------------------------------------------------------
def polish_clip(k=1.0, sigma=3.0, cyclic=False, exaggeration=1.0, feet_mesh='Boots', plant=True,
                fingers=True, arms_fk=True, rebuild_poles=True, start=None, end=None, **plant_kw):
    """Cartoon-filter the body, exaggerate loops, plant feet, relax hands, arms to FK.

    Works on the open scene (a clip retargeted with skeleton_retarget, keyed
    on every frame, FK and IK both keyed). Knee poles are never filtered;
    rebuild_poles=False keeps the retargeted ones (best for flips, rolls and
    tucks, where the knee does not follow the body's front). Returns a report.
    """
    start = int(mc.playbackOptions(q=True, min=True)) if start is None else start
    end = int(mc.playbackOptions(q=True, max=True)) if end is None else end
    if arms_fk:
        for plug in MUTANT_ARM_CHAINS:
            node, attr = plug.split('.', 1)
            mc.cutKey(node, at=attr, cl=True)
            mc.setAttr(plug, 1)
            mc.setKeyframe(node, at=attr, t=start)
    ctrls = body_controls('fk' if arms_fk else 'ik')
    n = cartoon_filter(ctrls, start, end, k=k, sigma=sigma, cyclic=cyclic)
    if exaggeration != 1.0:
        exaggerate(ctrls, start, end, factor=exaggeration)
    clamp_leg_reach(start, end)
    runs = {}
    if plant and feet_mesh and mc.objExists(feet_mesh):
        runs = plant_feet(foot_setup(feet_mesh, frame=start), start, end, **plant_kw)
    if rebuild_poles:
        knee_poles(start, end)   # else the retargeted poles (unfiltered) are kept
    if arms_fk:
        untwist_elbows(start, end)
    if fingers:
        relax_fingers(start, end)
    mc.currentTime(start)
    return '%d curves filtered, contacts %s' % (n, {c.split('_')[0]: r for c, r in runs.items()})


# --------------------------------------------------------------------------
# Review
# --------------------------------------------------------------------------
def side_playblast(out_dir, name, start, end, follow='COG_Ctrl', side=1, dist=320.0, height=85.0,
                   size=(480, 540), focal=30.0, show=('polymeshes',)):
    """Image-sequence playblast from the character's side, tracking `follow` in X/Z.

    side=1 looks from +X. Writes <out_dir>/<name>.####.png; returns the pattern.
    """
    grp = mc.group(em=True, n='side_pb_grp')
    cam = mc.camera(n='side_pb_cam', focalLength=focal)[0]
    mc.parent(cam, grp)
    mc.pointConstraint(follow, grp, skip='y', mo=False)
    mc.setAttr(grp + '.ty', 0)
    mc.setAttr(cam + '.t', side * dist, height, 0)
    mc.setAttr(cam + '.r', 0, side * 90, 0)
    panel = 'modelPanel4'
    old_cam = mc.modelPanel(panel, q=True, cam=True)
    mc.modelPanel(panel, e=True, cam=cam)
    mc.modelEditor(panel, e=True, allObjects=False, grid=True, hud=False, displayAppearance='smoothShaded')
    for s in show:
        mc.modelEditor(panel, e=True, **{s: True})
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    path = os.path.join(out_dir, name).replace('\\', '/')
    try:
        mc.playblast(filename=path, format='image', compression='png', startTime=start, endTime=end,
                     viewer=False, showOrnaments=False, percent=100, widthHeight=list(size),
                     forceOverwrite=True, offScreen=True, framePadding=4)
    finally:
        mc.modelEditor(panel, e=True, allObjects=True, hud=True)
        mc.modelPanel(panel, e=True, cam=old_cam)
        mc.delete(grp)
    return path + '.####.png'
