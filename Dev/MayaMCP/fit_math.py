"""Pure-math helpers for fitting guides to a mesh (no Maya imports).

Used by guide_fit.py inside Maya, and testable with plain Python:

    python -m unittest Tests/test_maya_mcp_fit_math.py

Points and vectors are plain 3-sequences (lists / tuples / MVector-like).
"""
import math


# --------------------------------------------------------------------------
# Small vector helpers
# --------------------------------------------------------------------------
def _sub(a, b):
    return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]


def _add(a, b):
    return [a[0] + b[0], a[1] + b[1], a[2] + b[2]]


def _mul(a, s):
    return [a[0] * s, a[1] * s, a[2] * s]


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _len(a):
    return math.sqrt(_dot(a, a))


def _unit(a):
    n = _len(a)
    if n < 1e-12:
        raise ValueError('zero-length vector')
    return [a[0] / n, a[1] / n, a[2] / n]


def centroid(points):
    pts = [list(p) for p in points]
    if not pts:
        raise ValueError('no points')
    return [sum(p[i] for p in pts) / len(pts) for i in range(3)]


def _covariance(points, c):
    m = [[0.0] * 3 for _ in range(3)]
    for p in points:
        d = _sub(p, c)
        for i in range(3):
            for j in range(3):
                m[i][j] += d[i] * d[j]
    return m


def sym_eigen3(m, sweeps=50):
    """Eigenvalues / eigenvectors of a symmetric 3x3 matrix (Jacobi).

    Returns [(value, vector), ...] sorted by value, largest first.
    """
    a = [list(r) for r in m]
    v = [[1.0 if i == j else 0.0 for j in range(3)] for i in range(3)]
    for _ in range(sweeps):
        off = sum(a[i][j] ** 2 for i in range(3) for j in range(3) if i != j)
        if off < 1e-18:
            break
        for p in range(3):
            for q in range(p + 1, 3):
                if abs(a[p][q]) < 1e-15:
                    continue
                theta = (a[q][q] - a[p][p]) / (2.0 * a[p][q])
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(3):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p], a[k][q] = c * akp - s * akq, s * akp + c * akq
                for k in range(3):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k], a[q][k] = c * apk - s * aqk, s * apk + c * aqk
                for k in range(3):
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p], v[k][q] = c * vkp - s * vkq, s * vkp + c * vkq
    pairs = [(a[i][i], [v[0][i], v[1][i], v[2][i]]) for i in range(3)]
    return sorted(pairs, key=lambda pv: -pv[0])


# --------------------------------------------------------------------------
# Lines and planes
# --------------------------------------------------------------------------
def fit_line(points):
    """Best line through points: (centroid, unit direction).

    The direction points from the first point toward the last one.
    """
    pts = [list(p) for p in points]
    if len(pts) < 2:
        raise ValueError('fit_line needs at least 2 points')
    c = centroid(pts)
    d = sym_eigen3(_covariance(pts, c))[0][1]
    if _dot(d, _sub(pts[-1], pts[0])) < 0:
        d = _mul(d, -1)
    return c, _unit(d)


def closest_points(p, u, q, v):
    """Closest approach of lines p + s*u and q + t*v.

    Returns (midpoint, gap). Use it for a joint between two bones: the
    crossing of their centre lines (knee from thigh + shin axes).
    """
    u, v = _unit(u), _unit(v)
    w = _sub(p, q)
    a, b, c = _dot(u, u), _dot(u, v), _dot(v, v)
    d, e = _dot(u, w), _dot(v, w)
    den = a * c - b * b
    if abs(den) < 1e-12:
        raise ValueError('lines are parallel')
    s = (b * e - c * d) / den
    t = (a * e - b * d) / den
    pa = _add(p, _mul(u, s))
    pb = _add(q, _mul(v, t))
    return _mul(_add(pa, pb), 0.5), _len(_sub(pa, pb))


def fit_plane(points):
    """Best plane through points: (centroid, unit normal).

    Least squares in every direction (smallest-variance axis), so it works
    whatever way the limb faces.
    """
    pts = [list(p) for p in points]
    if len(pts) < 3:
        raise ValueError('fit_plane needs at least 3 points')
    c = centroid(pts)
    eig = sym_eigen3(_covariance(pts, c))
    if eig[1][0] < 1e-12:
        raise ValueError('points are collinear, the plane is undefined')
    return c, _unit(eig[2][1])


def project_to_plane(point, origin, normal):
    n = _unit(normal)
    d = _dot(_sub(point, origin), n)
    return _sub(point, _mul(n, d))


def plane_axes(points):
    """In-plane axes of a flat point set: (centroid, e1, e2, normal), e1 the longest."""
    pts = [list(p) for p in points]
    c = centroid(pts)
    eig = sym_eigen3(_covariance(pts, c))
    if eig[1][0] < 1e-12:
        raise ValueError('points are collinear: no plane to read the shape from')
    return c, _unit(eig[0][1]), _unit(eig[1][1]), _unit(eig[2][1])


# --------------------------------------------------------------------------
# Tube profiles (fingers, toes, tails): creases and the base
# --------------------------------------------------------------------------
def _clean(profile):
    """[(dist, radius), ...] without the samples that found no loop."""
    out = []
    for item in profile:
        d, r = item[0], item[1]
        if r is not None:
            out.append((float(d), float(r)))
    return out


def find_merge(profile, ratio=1.25, look_back=3):
    """Where a tube walked from its tip merges into the body.

    profile: [(dist, radius), ...] ordered tip -> root (radius None = no loop).
    Returns the index (into the cleaned profile) of the last sample before
    the radius jumps above `ratio` x the largest of the previous `look_back`
    samples, or the last index when it never jumps. The steep ramp at the
    tip is skipped: the search starts once the radius reaches 80% of the
    profile's median.
    """
    p = _clean(profile)
    if not p:
        raise ValueError('empty profile')
    radii = sorted(r for _, r in p)
    median = radii[len(radii) // 2]
    start = next((i for i, (_, r) in enumerate(p) if r >= 0.8 * median), 0)
    for i in range(max(1, start + 1), len(p)):
        ref = max(r for _, r in p[max(0, i - look_back):i])
        if p[i][1] > ratio * ref:
            return i - 1
    return len(p) - 1


def find_creases(profile, window=2, span=5, min_depth=0.05, end=None):
    """Creases of a tube: local radius minima with real bulges on both sides.

    profile: [(dist, radius), ...] ordered tip -> root. A sample is a crease
    when it is the smallest within +-`window` samples and the largest radius
    within `span` samples on each side is at least `min_depth` (fraction of
    the crease radius) bigger. `end` limits the search to cleaned indices
    below it (pass find_merge()+1 to ignore the body). Returns cleaned
    indices, tip -> root.
    """
    p = _clean(profile)
    end = len(p) if end is None else min(end, len(p))
    out = []
    for i in range(1, end - 1):
        r = p[i][1]
        lo, hi = max(0, i - window), min(end, i + window + 1)
        if r > min(q for _, q in p[lo:hi]):
            continue
        left = max(q for _, q in p[max(0, i - span):i])
        right = max(q for _, q in p[i + 1:min(end, i + span + 1)])
        if left >= r * (1 + min_depth) and right >= r * (1 + min_depth):
            if out and i - out[-1] <= window:
                continue
            out.append(i)
    return out


def tube_joint_indices(profile, count=None, **kw):
    """Joint samples of a tube, root -> tip: [base, crease, crease, ...].

    base = last sample before the tube merges into the body. With `count`
    the creases nearest the base are kept so the result has `count` joints.
    Keyword arguments go to find_creases (window, span, min_depth) and
    find_merge (ratio, look_back).
    """
    merge_kw = {k: kw.pop(k) for k in ('ratio', 'look_back') if k in kw}
    base = find_merge(profile, **merge_kw)
    creases = find_creases(profile, end=base + 1, **kw)
    creases = [i for i in creases if i < base]
    joints = [base] + sorted(creases, reverse=True)
    if count is not None:
        if count < 1:
            raise ValueError('count must be at least 1')
        joints = joints[:count]
    return joints
