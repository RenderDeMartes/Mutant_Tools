"""Controller-shape helpers: size and place curve shapes on a character.

Runs INSIDE Maya (live session through the bridge, or mayapy). Only CV
positions change: the controllers, their pivots, colours and connections
stay as the build made them, so the shapes survive Mutant rebuilds through
its usual controller save / load.

    from Mutant_Tools.Dev.MayaMCP import ctrl_fit as cf
    cf.flat_shape('COG_Ctrl', center=(0, 91, -3), radius=26, radius2=19)
    cf.ring_around_bone('L_Toe_A_Ctrl', radius=2.0)
    cf.fit_fk_box('L_Hip_Fk_Ctrl', length=36.7, half_thickness=(9, 8))
    cf.mirror_shapes()          # Mutant's L -> R mirror, then a check
"""
import io
import sys

import maya.cmds as mc

try:
    from . import fit_math as fm
except ImportError:
    import fit_math as fm

_AXES = {'x': (1, 0, 0), 'y': (0, 1, 0), 'z': (0, 0, 1)}
_PLANES = {'xz': ('x', 'z'), 'xy': ('x', 'y'), 'yz': ('y', 'z')}


def _cvs(ctrl):
    shapes = mc.listRelatives(ctrl, s=True, type='nurbsCurve', f=True) or []
    if not shapes:
        raise ValueError('{} has no curve shapes'.format(ctrl))
    return mc.ls([s + '.cv[*]' for s in shapes], fl=True)


def _get(cvs, space):
    return [mc.xform(c, q=True, t=True, **{space: True}) for c in cvs]


def _set(cvs, points, space):
    for c, p in zip(cvs, points):
        mc.xform(c, t=list(p), **{space: True})


def _flat_coords(points, axes=None):
    """2D coordinates of a flat shape, normalized to -1..1 on each axis.

    axes=(e1, e2): read the shape along these directions (keeps its
    orientation when it already lies in that plane). None: the shape's own
    two longest directions.
    """
    c = fm.centroid(points)
    if axes is None:
        c, e1, e2, _ = fm.plane_axes(points)
    else:
        e1, e2 = [fm._unit(a) for a in axes]
    uv = [(fm._dot(fm._sub(p, c), e1), fm._dot(fm._sub(p, c), e2)) for p in points]
    mid = [(max(q[i] for q in uv) + min(q[i] for q in uv)) / 2.0 for i in (0, 1)]
    half = [(max(q[i] for q in uv) - min(q[i] for q in uv)) / 2.0 for i in (0, 1)]
    if min(half) < 1e-6:
        raise ValueError('the shape is flat along one of those axes (a line); pick other axes')
    return [((u - mid[0]) / half[0], (v - mid[1]) / half[1]) for u, v in uv]


def flat_shape(ctrl, center, radius, radius2=None, plane='xz'):
    """Lay a flat shape (ring, gear, hexagon...) in a world plane.

    center: world position of the shape's middle (the pivot does not move).
    radius / radius2: half sizes along the plane's first / second axis.
    plane: 'xz' (floor, default), 'xy' or 'yz'. A shape already lying in
    that plane keeps its orientation; any other flat shape is read along its
    own longest directions.
    """
    cvs = _cvs(ctrl)
    pts = _get(cvs, 'ws')
    a, b = [_AXES[k] for k in _PLANES[plane]]
    _, _, _, n = fm.plane_axes(pts)
    target_n = [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
    aligned = abs(fm._dot(n, target_n)) > 0.9
    uv = _flat_coords(pts, (a, b) if aligned else None)
    r2 = radius if radius2 is None else radius2
    new = [fm._add(fm._add(list(center), fm._mul(a, u * radius)), fm._mul(b, v * r2)) for u, v in uv]
    _set(cvs, new, 'ws')
    return {'ctrl': ctrl, 'cvs': len(cvs), 'kept_orientation': aligned}


def ring_around_bone(ctrl, radius, radius2=None, axis='x', offset=0.0):
    """Turn a flat shape into a ring around the bone the controller sits on.

    axis: the controller's local axis running down the bone (Mutant: 'x').
    The ring is centred on the pivot (plus `offset` along the bone).
    radius / radius2: half sizes on the other two local axes.
    """
    cvs = _cvs(ctrl)
    pts = _get(cvs, 'os')
    others = [k for k in 'xyz' if k != axis]
    e1, e2 = _AXES[others[0]], _AXES[others[1]]
    _, _, _, n = fm.plane_axes(pts)
    aligned = abs(fm._dot(n, _AXES[axis])) > 0.9
    uv = _flat_coords(pts, (e1, e2) if aligned else None)
    r2 = radius if radius2 is None else radius2
    base = fm._mul(_AXES[axis], offset)
    new = [fm._add(fm._add(base, fm._mul(e1, u * radius)), fm._mul(e2, v * r2)) for u, v in uv]
    _set(cvs, new, 'os')
    return {'ctrl': ctrl, 'cvs': len(cvs)}


def fit_fk_box(ctrl, length, half_thickness=None, axis='x'):
    """Stretch an FK box (or any shape running down the bone) to a bone length.

    length: distance to the next joint; the far end of the shape along the
    local `axis` lands there, the near end scales with it. half_thickness:
    optional (a, b) half sizes on the other two local axes, centred on the bone.
    """
    cvs = _cvs(ctrl)
    pts = _get(cvs, 'os')
    i = 'xyz'.index(axis)
    far = max((p[i] for p in pts), key=abs)
    if abs(far) < 1e-6:
        raise ValueError('{} has no extent along {}'.format(ctrl, axis))
    k = (length if far > 0 else -length) / far
    others = [j for j in range(3) if j != i]
    scale = {}
    if half_thickness is not None:
        for j, h in zip(others, half_thickness):
            ext = max(abs(p[j]) for p in pts)
            if ext < 1e-6:
                raise ValueError('{} is flat on axis {}'.format(ctrl, 'xyz'[j]))
            scale[j] = h / ext
    new = []
    for p in pts:
        q = list(p)
        q[i] *= k
        for j, s in scale.items():
            q[j] *= s
        new.append(q)
    _set(cvs, new, 'os')
    return {'ctrl': ctrl, 'length': length, 'was': round(abs(far), 4)}


def mirror_shapes(verify=True, tol=0.01, left='L_', right='R_'):
    """Mutant's own L -> R shape mirror (world X), then check every pair.

    Returns {'mirrored': True, 'mismatches': [(left ctrl, worst cv distance)]};
    a mismatch means the right control's CVs do not mirror the left ones
    (different CV counts show as -1).
    """
    from Mutant_Tools.Utils.IO import CtrlUtils
    out = sys.stdout
    sys.stdout = io.StringIO()   # the mirror prints every control
    try:
        CtrlUtils.Ctrls().mirror_all_ctrl_shapes()
    finally:
        sys.stdout = out
    bad = []
    if verify:
        for l_ctrl in CtrlUtils.get_all_ctrls():
            if not l_ctrl.startswith(left):
                continue
            r_ctrl = right + l_ctrl[len(left):]
            l_sh = mc.listRelatives(l_ctrl, s=True, type='nurbsCurve', f=True)
            if not l_sh or not mc.objExists(r_ctrl):
                continue
            r_sh = mc.listRelatives(r_ctrl, s=True, type='nurbsCurve', f=True) or []
            a = mc.ls([s + '.cv[*]' for s in l_sh], fl=True)
            b = mc.ls([s + '.cv[*]' for s in r_sh], fl=True) if r_sh else []
            if len(a) != len(b):
                bad.append((l_ctrl, -1))
                continue
            worst = 0.0
            for x, y in zip(a, b):
                p, q = mc.xform(x, q=True, ws=True, t=True), mc.xform(y, q=True, ws=True, t=True)
                worst = max(worst, fm._len([p[0] + q[0], p[1] - q[1], p[2] - q[2]]))
            if worst > tol:
                bad.append((l_ctrl, round(worst, 4)))
    return {'mirrored': True, 'mismatches': bad}
