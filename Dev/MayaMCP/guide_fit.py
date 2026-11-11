"""Guide-fitting helpers for placing Mutant block guides on a mesh.

Runs INSIDE Maya (live session through the bridge, or mayapy). See
GUIDE_FITTING.md for the workflow. Everything works in world space and only
writes the channels each solver is allowed to touch -- jointOrient is never
changed, so fitted guides stay comparable across assets.

    from Mutant_Tools.Dev.MayaMCP import guide_fit as gf
    gf.snap('arm_top', 'top', cx=40, cy=-5, width=60, out_dir=OUT)
    gf.fit_limb('L_Shoulder_Guide', 'L_Elbow_Guide', 'L_Wrist_Guide', S, E, W)
    gf.fit_hand('L_Hand_Palm_Guide', targets, weights)
"""
import math

import maya.cmds as mc
import maya.api.OpenMaya as om


# --------------------------------------------------------------------------
# Viewing: calibrated orthographic playblasts
# --------------------------------------------------------------------------
def snap(name, view, cx, cy, width, out_dir, w=1400, h=1000, guides=True,
         panel='modelPanel4', show=('Mutant_Build',)):
    """Playblast an ortho camera with a known pixel->world mapping.

    view 'top'  : screen right = +X, screen down = +Z  (cx, cy = world X, Z)
    view 'front': screen right = +X, screen down = -Y  (cx, cy = world X, Y)
    view 'side' : screen right = -Z, screen down = -Y  (cx, cy = world -Z, Y)
    One pixel = width / w world units. Use px_to_world() to convert.
    Returns the written png path.
    """
    for node in show:
        if mc.objExists(node):
            mc.setAttr(node + '.v', 1)
    shape = mc.listRelatives(view, s=True)[0]
    mc.setAttr(shape + '.filmFit', 1)
    mc.setAttr(shape + '.orthographicWidth', width)
    mc.setAttr(shape + '.farClipPlane', 10000)
    if view == 'top':
        mc.setAttr(view + '.t', cx, 1000, cy)
    elif view == 'front':
        mc.setAttr(view + '.t', cx, cy, 1000)
    elif view == 'side':
        mc.setAttr(view + '.t', 1000, cy, -cx)
    mc.modelPanel(panel, e=True, cam=view)
    mc.modelEditor(panel, e=True, allObjects=True, joints=guides,
                   nurbsCurves=guides, locators=True, polymeshes=True,
                   grid=False, displayAppearance='smoothShaded',
                   wireframeOnShaded=True, xray=True, jointXray=True,
                   hud=False, displayTextures=False)
    path = '%s/%s.png' % (out_dir.rstrip('/\\'), name)
    mc.playblast(completeFilename=path, format='image', compression='png',
                 frame=[mc.currentTime(q=True)], viewer=False,
                 showOrnaments=False, percent=100, widthHeight=[w, h],
                 forceOverwrite=True, offScreen=True)
    return path


def px_to_world(view, cx, cy, width, px, py, w=1400, h=1000):
    """Pixel (px, py) of a snap() image -> the two world coords of that view."""
    k = float(width) / w
    a = cx + (px - w / 2.0) * k
    if view == 'top':
        return a, cy + (py - h / 2.0) * k   # X, Z
    return a, cy - (py - h / 2.0) * k       # X (side: -Z), Y


def locator(name, pos, size=0.5):
    """Drop a marker locator (handy to check estimated targets in a snap)."""
    if mc.objExists(name):
        mc.delete(name)
    loc = mc.spaceLocator(n=name)[0]
    mc.xform(loc, ws=True, t=pos)
    mc.setAttr(loc + 'Shape.localScale', size, size, size)
    return loc


# --------------------------------------------------------------------------
# Mesh analysis
# --------------------------------------------------------------------------
def _fn_mesh(mesh):
    sel = om.MSelectionList()
    sel.add(mesh)
    return om.MFnMesh(sel.getDagPath(0))


def mesh_shells(mesh, min_x=None):
    """Connected pieces of a mesh: list of dicts (bbox min/max, centroid, n).

    Hard-surface/robot parts are often separate shells per segment, which
    gives exact joint locations (segment ends / centroids).
    """
    fn = _fn_mesh(mesh)
    pts = fn.getPoints(om.MSpace.kWorld)
    parent = list(range(fn.numVertices))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    for e in range(fn.numEdges):
        a, b = fn.getEdgeVertices(e)
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    groups = {}
    for v in range(fn.numVertices):
        groups.setdefault(find(v), []).append(v)
    out = []
    for verts in groups.values():
        p = [pts[i] for i in verts]
        lo = [min(q[i] for q in p) for i in range(3)]
        hi = [max(q[i] for q in p) for i in range(3)]
        if min_x is not None and hi[0] < min_x:
            continue
        c = [sum(q[i] for q in p) / len(p) for i in range(3)]
        out.append({'min': lo, 'max': hi, 'centroid': c, 'n': len(verts),
                    'verts': verts})
    return sorted(out, key=lambda s: s['min'][0])


def shell_chain_joints(mesh, chain, shells=None):
    """Joint points of a chain of rigid segments (one shell each, or a list
    of shell indices merged per segment), ordered root -> tip.

    Returns [root_start, joint_1, ..., tip_end]: ends are measured along the
    segment axis (centroid to centroid), joints are the midpoint of the gap
    between consecutive segments.
    """
    shells = shells or mesh_shells(mesh)
    pts = _fn_mesh(mesh).getPoints(om.MSpace.kWorld)
    segs = []
    for item in chain:
        ids = item if isinstance(item, (list, tuple)) else [item]
        verts = [v for i in ids for v in shells[i]['verts']]
        c = om.MVector()
        for v in verts:
            c += om.MVector(pts[v].x, pts[v].y, pts[v].z)
        segs.append((c / len(verts), verts))
    out = []
    for k, (c, verts) in enumerate(segs):
        if k + 1 < len(segs):
            d = (segs[k + 1][0] - c).normal()
        else:
            d = (c - segs[k - 1][0]).normal()
        proj = [(om.MVector(pts[v].x, pts[v].y, pts[v].z) - c) * d for v in verts]
        start, end = c + d * min(proj), c + d * max(proj)
        if k == 0:
            out.append(start)
        else:
            out[-1] = (out[-1] + start) * 0.5
        out.append(end)
    return [[p.x, p.y, p.z] for p in out]


def tube_center(mesh, point, axis, rays=24, max_dist=1000.0):
    """Center of the mesh cross-section through `point` perpendicular to `axis`.

    Casts rays in the cross-section plane and averages the first hits, so an
    eyeballed point inside a limb/finger snaps to its middle. Returns
    (center, mean_radius) or (point, None) when nothing is hit.
    """
    fn = _fn_mesh(mesh)
    p = om.MVector(point)
    ax = om.MVector(axis).normal()
    ref = om.MVector(0, 1, 0) if abs(ax.y) < 0.9 else om.MVector(1, 0, 0)
    u = (ref ^ ax).normal()
    v = (ax ^ u).normal()
    hits = []
    for i in range(rays):
        ang = 2 * math.pi * i / rays
        d = u * math.cos(ang) + v * math.sin(ang)
        hit = fn.closestIntersection(
            om.MFloatPoint(p.x, p.y, p.z), om.MFloatVector(d.x, d.y, d.z),
            om.MSpace.kWorld, max_dist, False)
        if hit and hit[3] != -1:
            hits.append(om.MVector(hit[0].x, hit[0].y, hit[0].z))
    if len(hits) < rays // 2:
        return list(point), None
    c = om.MVector()
    for h in hits:
        c += h
    c /= len(hits)
    rad = sum((h - c).length() for h in hits) / len(hits)
    return [c.x, c.y, c.z], rad


def surface_extreme(mesh, origin, direction, cone_deg=25.0):
    """Farthest vertex from `origin` along `direction` inside a cone.

    Use for fingertips: origin = knuckle, direction = rough finger direction.
    """
    fn = _fn_mesh(mesh)
    o = om.MVector(origin)
    d = om.MVector(direction).normal()
    cos_lim = math.cos(math.radians(cone_deg))
    best, best_t = None, -1e9
    for q in fn.getPoints(om.MSpace.kWorld):
        r = om.MVector(q.x, q.y, q.z) - o
        L = r.length()
        if L < 1e-6 or (r * d) / L < cos_lim:
            continue
        if r * d > best_t:
            best_t, best = r * d, [q.x, q.y, q.z]
    return best


# --------------------------------------------------------------------------
# Matrix helpers
# --------------------------------------------------------------------------
def _rot_only(m):
    return om.MMatrix([m[0], m[1], m[2], 0, m[4], m[5], m[6], 0,
                       m[8], m[9], m[10], 0, 0, 0, 0, 1])


def _euler_matrix(deg, order=0):
    return om.MEulerRotation([math.radians(a) for a in deg], order).asMatrix()


def frame_matrix(x_axis, z_hint, pos=(0, 0, 0)):
    """Orthonormal world matrix: X along x_axis, Z as close to z_hint as allowed."""
    x = om.MVector(x_axis).normal()
    y = (om.MVector(z_hint) ^ x).normal()
    z = (x ^ y).normal()
    return om.MMatrix([x.x, x.y, x.z, 0, y.x, y.y, y.z, 0,
                       z.x, z.y, z.z, 0, pos[0], pos[1], pos[2], 1])


def set_world_rotation(node, world_rot):
    """Write node.r so its world rotation equals world_rot (jointOrient kept)."""
    parent_inv = om.MMatrix(mc.getAttr(node + '.parentInverseMatrix'))
    local = _rot_only(world_rot) * _rot_only(parent_inv)
    order = mc.getAttr(node + '.rotateOrder')
    ra = _euler_matrix(mc.getAttr(node + '.rotateAxis')[0])
    jo = om.MMatrix()
    if mc.nodeType(node) == 'joint':
        jo = _euler_matrix(mc.getAttr(node + '.jointOrient')[0])
    r = ra.inverse() * local * jo.inverse()
    e = om.MTransformationMatrix(r).rotation(asQuaternion=False)
    e.reorderIt(order)
    mc.setAttr(node + '.r', *[math.degrees(a) for a in (e.x, e.y, e.z)])


def roll_to_up(node, up=(0, 1, 0)):
    """Roll node around its own X so its Y points as close to `up` as possible.

    Only changes node.r (jointOrient kept); X direction is unchanged.
    """
    x = axis_of(world_rot(node), 0)
    set_world_rotation(node, frame_matrix(x, x ^ om.MVector(up)))
    return list(mc.getAttr(node + '.r')[0])


def world_rot(node):
    return _rot_only(om.MMatrix(mc.xform(node, q=True, ws=True, m=True)))


def axis_of(m, i):
    return om.MVector(m[i * 4], m[i * 4 + 1], m[i * 4 + 2])


# --------------------------------------------------------------------------
# Limb: shoulder (t + r), elbow (tx + rz), wrist (tx)
# --------------------------------------------------------------------------
def fit_limb(shoulder, elbow, wrist, S, E, W, bend_axis='z', up=None):
    """Place a 3-joint limb guide chain on world targets S, E, W.

    Shoulder gets translate + rotate, elbow only tx and one bend rotation,
    wrist only tx. jointOrient untouched. The bend-plane normal is picked on
    the same side as the shoulder's current bend axis so nothing flips.

    up: world vector the guides' Y axis should point to (e.g. (0, 1, 0)).
    Forces bend_axis='y' and a bend plane whose normal is `up` made
    perpendicular to shoulder->wrist; E is projected onto that plane, so an
    elbow offset along `up` is dropped.
    """
    S, E, W = om.MVector(S), om.MVector(E), om.MVector(W)
    if up is not None:
        bend_axis = 'y'
        d = (W - S).normal()
        n = om.MVector(up)
        n = (n - d * (n * d)).normal()
        E = E - n * ((E - S) * n)
        upper, lower = E - S, W - E
    else:
        bi = 'xyz'.index(bend_axis)
        hint = axis_of(world_rot(shoulder), bi)
        upper, lower = E - S, W - E
        n = upper ^ lower
        if n.length() < 1e-4 * upper.length() * lower.length():
            n = hint - upper.normal() * (hint * upper.normal())  # straight limb
        n = n.normal()
        if n * hint < 0:
            n = -n
    mc.xform(shoulder, ws=True, t=list(S))
    if bend_axis == 'z':
        set_world_rotation(shoulder, frame_matrix(upper, n))
    else:  # bend around Y: Y = n, Z = X ^ Y
        x = upper.normal()
        set_world_rotation(shoulder, frame_matrix(upper, x ^ n))
    ang = math.atan2((upper.normal() ^ lower.normal()) * n,
                     upper.normal() * lower.normal())
    mc.setAttr(elbow + '.t', upper.length(), 0, 0)
    mc.setAttr(elbow + '.r', 0, 0, 0)
    mc.setAttr(elbow + '.r' + bend_axis, math.degrees(ang))
    mc.setAttr(wrist + '.t', lower.length(), 0, 0)
    return {'upper': upper.length(), 'lower': lower.length(),
            'bend': math.degrees(ang)}


# --------------------------------------------------------------------------
# Hand: palm (t + r), every other guide tx only
# --------------------------------------------------------------------------
def _hierarchy(root):
    order, kids = [], {}
    stack = [root]
    while stack:
        n = stack.pop(0)
        order.append(n)
        ch = [c for c in (mc.listRelatives(n, c=True, type='joint') or [])
              if c.endswith('_Guide')]
        kids[n] = ch
        stack.extend(ch)
    return order, kids


class HandModel(object):
    """Pure-python copy of a guide hierarchy where only tx of children moves."""

    def __init__(self, palm):
        self.palm = palm
        self.order, self.kids = _hierarchy(palm)
        self.parent = {c: p for p, cs in self.kids.items() for c in cs}
        self.local_rot = {}
        self.ty_tz = {}
        self.tx = {}
        for g in self.order[1:]:
            m = om.MMatrix(mc.getAttr(g + '.matrix'))
            self.local_rot[g] = _rot_only(m)
            t = mc.getAttr(g + '.t')[0]
            self.tx[g], self.ty_tz[g] = t[0], (t[1], t[2])

    def solve(self, palm_world, targets, fixed_tx=None, free_t=(), min_tx=0.05):
        """World positions for a palm world matrix.

        Returns (world positions, local t per guide). Guides in `free_t`
        translate on all axes: placed so their first targeted child lands
        exactly on its target, keeping their own X depth from their target.
        Every other guide only gets tx (projection on its target).
        """
        fixed_tx = fixed_tx or {}
        rot = {self.palm: _rot_only(palm_world)}
        pos = {self.palm: om.MVector(palm_world[12], palm_world[13],
                                     palm_world[14])}
        loc = {}
        for g in self.order[1:]:
            p = self.parent[g]
            R = rot[p]
            X, Y, Z = axis_of(R, 0), axis_of(R, 1), axis_of(R, 2)
            rot[g] = self.local_rot[g] * R
            if g in free_t and g in targets:
                Rg = rot[g]
                Xg, Yg, Zg = axis_of(Rg, 0), axis_of(Rg, 1), axis_of(Rg, 2)
                tg = om.MVector(targets[g])
                kids = [c for c in self.kids[g] if c in targets]
                if kids:
                    c = kids[0]
                    tc = om.MVector(targets[c])
                    cy, cz = self.ty_tz[c]
                    s = max(min_tx, (tc - tg) * Xg)
                    pos[g] = tc - Yg * cy - Zg * cz - Xg * s
                else:
                    pos[g] = tg
                d = pos[g] - pos[p]
                loc[g] = (d * X, d * Y, d * Z)
                continue
            ty, tz = self.ty_tz[g]
            base = pos[p] + Y * ty + Z * tz
            if g in fixed_tx:
                t = fixed_tx[g]
            elif g in targets:
                t = max(min_tx, (om.MVector(targets[g]) - base) * X)
            else:
                t = self.tx[g]
            loc[g] = (t, ty, tz)
            pos[g] = base + X * t
        return pos, loc

    def error(self, palm_world, targets, weights, fixed_tx=None, free_t=()):
        pos, _ = self.solve(palm_world, targets, fixed_tx, free_t)
        return sum(weights.get(g, 1.0) * (pos[g] - om.MVector(t)).length() ** 2
                   for g, t in targets.items() if g in pos)


def _nelder_mead(f, x0, step, iters=600, tol=1e-7):
    n = len(x0)
    pts = [list(x0)]
    for i in range(n):
        p = list(x0)
        p[i] += step[i]
        pts.append(p)
    vals = [f(p) for p in pts]
    for _ in range(iters):
        idx = sorted(range(n + 1), key=lambda i: vals[i])
        pts, vals = [pts[i] for i in idx], [vals[i] for i in idx]
        if abs(vals[-1] - vals[0]) < tol:
            break
        c = [sum(p[i] for p in pts[:-1]) / n for i in range(n)]
        xr = [c[i] + (c[i] - pts[-1][i]) for i in range(n)]
        fr = f(xr)
        if fr < vals[0]:
            xe = [c[i] + 2 * (c[i] - pts[-1][i]) for i in range(n)]
            fe = f(xe)
            pts[-1], vals[-1] = (xe, fe) if fe < fr else (xr, fr)
        elif fr < vals[-2]:
            pts[-1], vals[-1] = xr, fr
        else:
            xc = [c[i] + 0.5 * (pts[-1][i] - c[i]) for i in range(n)]
            fc = f(xc)
            if fc < vals[-1]:
                pts[-1], vals[-1] = xc, fc
            else:
                for j in range(1, n + 1):
                    pts[j] = [pts[0][i] + 0.5 * (pts[j][i] - pts[0][i])
                              for i in range(n)]
                    vals[j] = f(pts[j])
    return pts[0], vals[0]


def fit_hand(palm, targets, weights=None, palm_pos=None, x_hint=None,
             z_hint=None, fixed_tx=None, free_pos=False, free_t=(),
             up=None, apply=True):
    """Fit a hand guide tree: palm translate+rotate, children tx only.

    targets : {guide: world pos} -- any subset (knuckles, joints, tips).
    weights : {guide: weight}, default 1.
    palm_pos: palm world position (default: its current position, e.g. the
              wrist). free_pos=True lets the optimizer move it too.
    x_hint/z_hint: initial palm X (toward the middle finger) and Z (thumb
              side) directions; default = current palm axes.
    fixed_tx: {guide: tx} for guides without targets (cups, ...).
    free_t  : guides allowed full translate (e.g. finger roots '_00'), see
              HandModel.solve. Rotations of children are never touched.
    up      : world vector for the palm's Y axis (e.g. (0, 1, 0)); the palm
              then only aims X, roll stays locked to Y as close to `up` as
              possible (fingers inherit it).
    Returns per-guide residual distances.
    """
    weights = weights or {}
    model = HandModel(palm)
    cur = om.MMatrix(mc.xform(palm, q=True, ws=True, m=True))
    p0 = om.MVector(palm_pos) if palm_pos else om.MVector(cur[12], cur[13], cur[14])
    m0 = frame_matrix(x_hint or axis_of(cur, 0), z_hint or axis_of(cur, 2), p0)

    def build(x):
        r = om.MEulerRotation(x[0], x[1], x[2]).asMatrix()
        m = r * m0
        if up is not None:
            ax = axis_of(m, 0)
            m = frame_matrix(ax, ax ^ om.MVector(up))
        pos = p0 + om.MVector(x[3], x[4], x[5]) if free_pos else p0
        m[12], m[13], m[14] = pos.x, pos.y, pos.z
        return m

    nparam = 6 if free_pos else 3
    f = lambda x: model.error(build(x + [0] * (6 - len(x))), targets, weights,
                              fixed_tx, free_t)
    best, _ = _nelder_mead(f, [0.0] * nparam, [0.2] * 3 + [1.0] * (nparam - 3))
    best = best + [0] * (6 - len(best))
    m = build(best)
    pos, loc = model.solve(m, targets, fixed_tx, free_t)
    if apply:
        mc.xform(palm, ws=True, t=[m[12], m[13], m[14]])
        set_world_rotation(palm, m)
        for g in model.order[1:]:
            mc.setAttr(g + '.t', *loc[g])
    return {g: round((pos[g] - om.MVector(t)).length(), 3)
            for g, t in targets.items() if g in pos}


def hand_targets(wrist, fingers, thumb=None, prefix='L_Hand_',
                 meta_ratio=0.45, thumb_weight=0.3):
    """Build (targets, weights, free_t) for fit_hand from anatomical points.

    wrist  : world wrist point (palm guide position).
    fingers: {'Index': [knuckle, j2, j3, tip], 'Middle': ..., ...}
    thumb  : [mcp, ip, tip] (Thumb_01..03); Thumb_00 is derived.
    Finger/thumb '_00' roots go in free_t, cups get weak targets.
    """
    V = om.MVector
    w = V(wrist)
    T, Wt = {}, {}
    for f, pts in fingers.items():
        for i, p in enumerate(pts, 1):
            g = '%s%s_%02d_Guide' % (prefix, f, i)
            T[g] = list(p)
            Wt[g] = 1.5 if i == len(pts) else 1.0
        g = '%s%s_00_Guide' % (prefix, f)
        T[g] = list(w + (V(pts[0]) - w) * meta_ratio)
        Wt[g] = 0.2
    if thumb:
        for i, p in enumerate(thumb, 1):
            T['%sThumb_%02d_Guide' % (prefix, i)] = list(p)
            Wt['%sThumb_%02d_Guide' % (prefix, i)] = thumb_weight
        T[prefix + 'Thumb_00_Guide'] = list(w + (V(thumb[0]) - w) * 0.4)
        Wt[prefix + 'Thumb_00_Guide'] = 0.1
        T[prefix + 'InnerCup_Guide'] = list(w + (V(thumb[0]) - w) * 0.3)
        Wt[prefix + 'InnerCup_Guide'] = 0.1
    outer = [fingers[f][0] for f in ('Ring', 'Pinky') if f in fingers]
    if outer:
        mid = V()
        for p in outer:
            mid += V(p)
        mid /= len(outer)
        T[prefix + 'OutterCup_Guide'] = list(w + (mid - w) * 0.3)
        Wt[prefix + 'OutterCup_Guide'] = 0.1
    free = [g for g in T if g.endswith('_00_Guide')]
    return T, Wt, free


def fit_hand_points(wrist, fingers, thumb=None, prefix='L_Hand_', up=None, **kw):
    """One call: hand_targets() + fit_hand() with palm at the wrist.

    Palm X hint = wrist -> middle (or first) knuckle, Z hint = pinky -> index
    knuckle line (thumb side). `up` goes to fit_hand(); extra kwargs go to
    hand_targets().
    """
    V = om.MVector
    T, Wt, free = hand_targets(wrist, fingers, thumb, prefix, **kw)
    names = list(fingers)
    mid = fingers.get('Middle', fingers[names[0]])[0]
    first = fingers.get('Index', fingers[names[0]])[0]
    last = fingers.get('Pinky', fingers.get('Ring', fingers[names[-1]]))[0]
    zh = V(first) - V(last)
    if zh.length() < 1e-4:
        zh = None
    return fit_hand(prefix + 'Palm_Guide', T, Wt, palm_pos=list(wrist),
                    x_hint=V(mid) - V(wrist), z_hint=zh, free_t=free, up=up), T


def finger_points(knuckle, tip, ratios=(0.45, 0.30, 0.25)):
    """Joint targets between knuckle and tip by phalanx length ratios.

    Returns [knuckle, j2, j3, tip] (len(ratios)+1 points)."""
    k, t = om.MVector(knuckle), om.MVector(tip)
    pts, acc = [list(k)], 0.0
    for r in ratios:
        acc += r
        p = k + (t - k) * acc
        pts.append([p.x, p.y, p.z])
    return pts


def show_targets(targets, size=0.3, grp='fit_targets_grp'):
    """Locators for a {name: pos} dict under one group (delete before saving)."""
    if mc.objExists(grp):
        mc.delete(grp)
    locs = [locator('tgt_' + n, p, size) for n, p in targets.items()]
    return mc.group(locs, n=grp)


def save_as(path, build_visible=None, grp='fit_targets_grp', overwrite=False):
    """Remove fit helpers, optionally set Mutant_Build visibility, save .ma.

    Refuses to replace an existing file (or one the pipeline already
    registered with a .json) unless overwrite=True -- pick the next version.
    """
    import os
    stem = os.path.splitext(path)[0]
    if not overwrite and (os.path.exists(path) or os.path.exists(stem + '.json')):
        raise RuntimeError('%s already exists (or has a .json); use a new '
                           'version or overwrite=True' % path)
    if mc.objExists(grp):
        mc.delete(grp)
    if build_visible is not None and mc.objExists('Mutant_Build'):
        mc.setAttr('Mutant_Build.v', build_visible)
    mc.file(rename=path)
    return mc.file(save=True, type='mayaAscii', force=True)


def guide_report(root):
    """Print t / r / jo of every guide under root (sanity check)."""
    for g in mc.listRelatives(root, ad=True, type='joint') or []:
        print('%-26s t%s r%s jo%s' % (
            g, [round(v, 3) for v in mc.getAttr(g + '.t')[0]],
            [round(v, 2) for v in mc.getAttr(g + '.r')[0]],
            [round(v, 2) for v in mc.getAttr(g + '.jo')[0]]))


# --------------------------------------------------------------------------
# Cross-sections: joints from the mesh shape (toes, fingers, tails, limbs)
# --------------------------------------------------------------------------
try:
    from . import fit_math as fm
except ImportError:  # loaded as a plain module (mayapy, run_in_maya scripts)
    import fit_math as fm


class rest_pose(object):
    """Context: skinClusters on `meshes` off, so measurements read the bind pose."""

    def __init__(self, meshes):
        meshes = [meshes] if isinstance(meshes, str) else list(meshes)
        self.nodes = []
        for m in meshes:
            for sc in mc.ls(mc.listHistory(m) or [], type='skinCluster'):
                self.nodes.append((sc, mc.getAttr(sc + '.envelope')))

    def __enter__(self):
        for sc, _ in self.nodes:
            mc.setAttr(sc + '.envelope', 0)
        return self

    def __exit__(self, *exc):
        for sc, value in self.nodes:
            mc.setAttr(sc + '.envelope', value)
        return False


class MeshSlicer(object):
    """Plane / mesh intersection loops, one loop per separate tube cut.

    Build it once per mesh (reads the mesh at the current pose; wrap in
    rest_pose() on a skinned mesh), then call loops() as often as needed.
    """

    def __init__(self, mesh):
        fn = _fn_mesh(mesh)
        self.mesh = mesh
        self.points = [om.MVector(p.x, p.y, p.z) for p in fn.getPoints(om.MSpace.kWorld)]
        self.edges = {}
        for f in range(fn.numPolygons):
            vs = list(fn.getPolygonVertices(f))
            for i in range(len(vs)):
                a, b = vs[i], vs[(i + 1) % len(vs)]
                self.edges.setdefault((a, b) if a < b else (b, a), []).append(f)

    def loops(self, point, normal, reach=9.0):
        """Loops of the plane (point, normal) within `reach` of point.

        Returns [{'center', 'radius' (mean), 'rmax', 'n'}, ...]; edges sharing
        a face join the same loop, so two toes cut by one plane stay apart.
        """
        c = om.MVector(point)
        d = om.MVector(normal).normal()
        hits = {}
        for (a, b), faces in self.edges.items():
            pa, pb = self.points[a], self.points[b]
            if (pa - c).length() > reach and (pb - c).length() > reach:
                continue
            sa, sb = (pa - c) * d, (pb - c) * d
            if (sa > 0) == (sb > 0) or sa == sb:
                continue
            hits[(a, b)] = (pa + (pb - pa) * (sa / (sa - sb)), faces)
        parent = {k: k for k in hits}

        def find(k):
            while parent[k] != k:
                parent[k] = parent[parent[k]]
                k = parent[k]
            return k
        by_face = {}
        for k, (_, faces) in hits.items():
            for f in faces:
                if f in by_face:
                    parent[find(k)] = find(by_face[f])
                else:
                    by_face[f] = k
        groups = {}
        for k, (p, _) in hits.items():
            groups.setdefault(find(k), []).append(p)
        out = []
        for pts in groups.values():
            if len(pts) < 5:
                continue
            cen = om.MVector()
            for p in pts:
                cen += p
            cen /= len(pts)
            rs = [(p - cen).length() for p in pts]
            out.append({'center': [cen.x, cen.y, cen.z], 'radius': sum(rs) / len(rs),
                        'rmax': max(rs), 'n': len(pts)})
        return out


def walk_tube(mesh, start, direction, step=0.5, steps=40, max_radius=9.0, snap=None,
              stop_radius=None, slicer=None):
    """Follow a tube from `start` along `direction`, re-centring every slice.

    Each slice is cut perpendicular to the current direction, the loop
    nearest the predicted point is kept (within `snap`, default
    0.4 * max_radius) and the direction eases toward the new centre line.
    Use it tip -> root (nail to foot) so the tube is unambiguous at the start.
    Returns [{'dist', 'center', 'radius', 'rmax'}, ...]; center/radius None
    where no loop was found. Stops after `stop_radius` or 3 empty slices.
    """
    snap = 0.4 * max_radius if snap is None else snap
    if slicer is None:
        with rest_pose(mesh):
            slicer = MeshSlicer(mesh)
    p = om.MVector(start)
    d = om.MVector(direction).normal()
    prev, misses, dist, out = None, 0, 0.0, []
    for i in range(steps):
        p = p + d * step
        dist += step
        loops = [l for l in slicer.loops(p, d, reach=max_radius)
                 if (om.MVector(l['center']) - p).length() <= snap]
        if not loops:
            out.append({'dist': dist, 'center': None, 'radius': None, 'rmax': None})
            misses += 1
            if misses >= 3:
                break
            continue
        misses = 0
        best = min(loops, key=lambda l: (om.MVector(l['center']) - p).length())
        cen = om.MVector(best['center'])
        out.append({'dist': dist, 'center': best['center'], 'radius': best['radius'],
                    'rmax': best['rmax']})
        if prev is not None and i > 3:
            d = (d * 0.7 + (cen - prev).normal() * 0.3).normal()
        p, prev = cen, cen
        if stop_radius and best['radius'] > stop_radius:
            break
    return out


def tube_joints(mesh, tip, direction, count=3, step=0.5, max_dist=20.0, max_radius=9.0,
                **crease_kw):
    """Joint positions of a toe / finger / tail from its shape, root -> tip.

    Walks from `tip` (e.g. the nail centre) along `direction` (toward the
    body), then: joint 0 = the last slice before the tube merges into the
    body (knuckle), the next joints = the creases (radius dips between
    bulges) nearest the knuckle. `count` joints at most; fewer when the
    tube has fewer creases (a spur gives only its base). crease_kw goes to
    fit_math.tube_joint_indices (window, span, min_depth, ratio).
    Returns {'joints', 'dists', 'radii', 'profile'}.
    """
    prof = walk_tube(mesh, tip, direction, step=step, steps=int(round(max_dist / step)),
                     max_radius=max_radius)
    good = [s for s in prof if s['radius'] is not None]
    if not good:
        raise ValueError('no cross-section found from {} along {}'.format(tip, direction))
    idx = fm.tube_joint_indices([(s['dist'], s['radius']) for s in prof], count=count, **crease_kw)
    return {'joints': [good[i]['center'] for i in idx], 'dists': [good[i]['dist'] for i in idx],
            'radii': [round(good[i]['radius'], 3) for i in idx],
            'profile': [(s['dist'], None if s['radius'] is None else round(s['radius'], 3)) for s in prof]}


def bone_axis(mesh, start, direction, length, step=1.0, max_radius=14.0, slicer=None):
    """Centre line of a limb segment: slice centres from start over `length`.

    Returns {'origin', 'direction', 'points'} (fit_math.fit_line of the centres).
    """
    prof = walk_tube(mesh, start, direction, step=step, steps=int(round(length / step)),
                     max_radius=max_radius, slicer=slicer)
    pts = [s['center'] for s in prof if s['center'] is not None]
    if len(pts) < 3:
        raise ValueError('bone_axis found {} slices; check start/direction'.format(len(pts)))
    origin, axis = fm.fit_line(pts)
    return {'origin': origin, 'direction': axis, 'points': pts}


def limb_joints(mesh, segments, max_radius=14.0):
    """Joints between limb segments from their centre lines.

    segments: [{'start', 'direction', 'length'}, ...] in chain order, each
    a stretch of straight bone (keep away from the bends). Returns
    {'axes': [...], 'joints': [crossing of segment k and k+1, ...],
    'gaps': [...]} -- a big gap means the two axes do not really cross.
    """
    with rest_pose(mesh):
        slicer = MeshSlicer(mesh)
    axes = [bone_axis(mesh, s['start'], s['direction'], s['length'],
                      step=s.get('step', 1.0), max_radius=max_radius, slicer=slicer)
            for s in segments]
    joints, gaps = [], []
    for a, b in zip(axes, axes[1:]):
        mid, gap = fm.closest_points(a['origin'], a['direction'], b['origin'], b['direction'])
        joints.append(mid)
        gaps.append(gap)
    return {'axes': [{'origin': a['origin'], 'direction': a['direction']} for a in axes],
            'joints': joints, 'gaps': gaps}


def put_keep_children(node, pos):
    """Move a guide in world space without moving its children."""
    kids = mc.listRelatives(node, c=True, type='transform', f=True) or []
    keep = [(k, mc.xform(k, q=True, ws=True, t=True)) for k in kids]
    mc.xform(node, ws=True, t=list(pos))
    for k, kp in keep:
        mc.xform(k, ws=True, t=kp)


def project_chain_to_plane(nodes, apply=True):
    """Put a chain's guides on their best-fit plane (stable IK, no knee pop).

    nodes in chain order; parents move first and children keep their place
    until moved. Returns {'normal', 'offsets': {node: distance moved}}.
    """
    pos = [mc.xform(n, q=True, ws=True, t=True) for n in nodes]
    origin, normal = fm.fit_plane(pos)
    new = [fm.project_to_plane(p, origin, normal) for p in pos]
    offsets = {}
    for n, p, q in zip(nodes, pos, new):
        offsets[n] = round(fm._len(fm._sub(p, q)), 4)
        if apply:
            put_keep_children(n, q)
    return {'normal': normal, 'offsets': offsets}


# --------------------------------------------------------------------------
# Perspective snapshots with the rig controls showing
# --------------------------------------------------------------------------
class controls_visible(object):
    """Context: controls draw in playblasts (Mutant's Global_Ctrl.CtrlPlayback
    turns hideOnPlayback on), restored afterwards."""

    def __init__(self):
        self.saved = []

    def __enter__(self):
        for plug in mc.ls('*.CtrlPlayback'):
            if mc.getAttr(plug, settable=True):
                self.saved.append((plug, mc.getAttr(plug)))
                mc.setAttr(plug, 0)
        for shape in mc.ls(type='nurbsCurve'):
            plug = shape + '.hideOnPlayback'
            if mc.getAttr(plug) and mc.getAttr(plug, settable=True):
                self.saved.append((plug, True))
                mc.setAttr(plug, False)
        return self

    def __exit__(self, *exc):
        for plug, value in reversed(self.saved):
            if mc.objExists(plug):
                mc.setAttr(plug, value)
        return False


_EDITOR_FLAGS = ('polymeshes', 'nurbsCurves', 'controllers', 'joints', 'locators', 'grid',
                 'xray', 'wireframeOnShaded', 'hud', 'ikHandles', 'deformers', 'cameras',
                 'lights', 'handles', 'dimensions', 'selectionHiliteDisplay')


def snap_persp(name, eye, aim, out_dir, w=1200, h=1000, focal=35.0, xray=False,
               controls=True, joints=False, panel='modelPanel4'):
    """Playblast one frame from a temporary camera at `eye` looking at `aim`.

    The panel's camera and display flags are put back afterwards; with
    controls=True the rig controls show even though Mutant hides them on
    playback. Returns the png path.
    """
    import os
    cam = mc.camera(n='mcp_snap_cam', focalLength=focal)[0]
    loc = mc.spaceLocator(n='mcp_snap_aim')[0]
    old_cam = mc.modelPanel(panel, q=True, cam=True)
    flags = {f: mc.modelEditor(panel, q=True, **{f: True}) for f in _EDITOR_FLAGS}
    appearance = mc.modelEditor(panel, q=True, displayAppearance=True)
    path = os.path.join(out_dir, name + '.png')
    try:
        mc.xform(cam, ws=True, t=list(eye))
        mc.xform(loc, ws=True, t=list(aim))
        mc.delete(mc.aimConstraint(loc, cam, aim=(0, 0, -1), u=(0, 1, 0), wu=(0, 1, 0)))
        mc.modelPanel(panel, e=True, cam=cam)
        mc.modelEditor(panel, e=True, polymeshes=True, nurbsCurves=controls, controllers=controls,
                       joints=joints, locators=False, grid=False, xray=xray, wireframeOnShaded=False,
                       hud=False, ikHandles=False, deformers=False, cameras=False, lights=False,
                       handles=False, dimensions=False, selectionHiliteDisplay=False,
                       displayAppearance='smoothShaded')
        sel = mc.ls(sl=True)
        mc.select(cl=True)
        with controls_visible() if controls else _null():
            mc.playblast(completeFilename=path, format='image', compression='png',
                         frame=[mc.currentTime(q=True)], viewer=False, showOrnaments=False,
                         percent=100, widthHeight=[w, h], forceOverwrite=True, offScreen=True)
        if sel:
            mc.select(sel)
    finally:
        mc.modelPanel(panel, e=True, cam=old_cam)
        mc.modelEditor(panel, e=True, displayAppearance=appearance, **flags)
        mc.delete(cam, loc)
    return path


class _null(object):
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False
