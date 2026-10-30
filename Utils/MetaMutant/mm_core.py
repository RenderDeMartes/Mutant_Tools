"""
Dependency-free core of the MetaHuman <-> TopoTransfer pipeline.

Everything here is plain Python (works in `mayapy`, in any Python 3.8+, and in
tests without Maya or Epic's DNA libraries). It operates on a *reader-like*
object exposing the subset of the DNA reader API we need (method names match
`dna.BinaryStreamReader`), so the real reader can be passed in directly.

Conventions
-----------
* Positions are in DNA space (MetaHuman: centimetres, Y up).
* Joint neutral rotations are Euler angles in degrees, rotate order XYZ,
  composed as R = Rz @ Ry @ Rx (column vectors) - the Maya `xyz` convention.
  `mm_maya.py: check_joint_convention` verifies this against a
  rig built in Maya before relying on it.
* 4x4 matrices are column-major flat lists (TopoTransfer / three.js layout).
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, asdict
from typing import Callable, Dict, Iterable, List, Optional, Sequence, Tuple

Vec3 = Tuple[float, float, float]
Mat3 = Tuple[Vec3, Vec3, Vec3]  # rows

# ----------------------------------------------------------------------------- manifest


@dataclass
class MeshBlock:
    """One DNA mesh inside the combined OBJ."""

    name: str
    dna_index: int
    vertex_count: int
    offset: int  # first vertex of this mesh in the combined OBJ (0-based)


def write_manifest(path: str, dna_path: str, lod: int, blocks: List[MeshBlock]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"format": "topotransfer-metahuman-manifest/1", "dna": dna_path, "lod": lod, "meshes": [asdict(b) for b in blocks]}, f, indent=2)


def read_manifest(path: str) -> List[MeshBlock]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if data.get("format") != "topotransfer-metahuman-manifest/1":
        raise ValueError(f"{path} is not a TopoTransfer MetaHuman manifest")
    return [MeshBlock(**m) for m in data["meshes"]]


# ----------------------------------------------------------------------------- OBJ


def write_obj(path: str, meshes: Sequence[dict], header: Iterable[str] = ()) -> List[MeshBlock]:
    """
    Write several meshes into one OBJ, in order, with UVs.

    Each mesh dict: name, dna_index, positions [(x,y,z)], uvs [(u,v)],
    faces [[(position_index, uv_index), ...], ...] (0-based, local to the mesh).
    Returns the manifest blocks (vertex offsets in the combined file).
    """
    blocks: List[MeshBlock] = []
    v_off = 0
    t_off = 0
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for h in header:
            f.write(f"# {h}\n")
        for m in meshes:
            f.write(f"o {m['name']}\n")
            for p in m["positions"]:
                f.write(f"v {p[0]:.6f} {p[1]:.6f} {p[2]:.6f}\n")
            for uv in m.get("uvs", []):
                f.write(f"vt {uv[0]:.6f} {uv[1]:.6f}\n")
            has_uv = bool(m.get("uvs"))
            for face in m["faces"]:
                if has_uv:
                    f.write("f " + " ".join(f"{vi + 1 + v_off}/{ti + 1 + t_off}" for vi, ti in face) + "\n")
                else:
                    f.write("f " + " ".join(f"{vi + 1 + v_off}" for vi, _ in face) + "\n")
            blocks.append(MeshBlock(m["name"], int(m["dna_index"]), len(m["positions"]), v_off))
            v_off += len(m["positions"])
            t_off += len(m.get("uvs", []))
    return blocks


@dataclass
class WrappedObj:
    positions: List[Vec3]
    #: base -> reference placement written by TopoTransfer (column-major), identity if absent
    alignment: List[float]
    #: 'reference' or 'original' (which space the positions are in), None if unknown
    space: Optional[str]


IDENTITY4 = [1.0, 0, 0, 0, 0, 1.0, 0, 0, 0, 0, 1.0, 0, 0, 0, 0, 1.0]


def read_obj_positions(path: str) -> WrappedObj:
    """Read `v` records in file order plus TopoTransfer's alignment header (if present)."""
    positions: List[Vec3] = []
    alignment = list(IDENTITY4)
    space: Optional[str] = None
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            if line.startswith("v "):
                t = line.split()
                positions.append((float(t[1]), float(t[2]), float(t[3])))
            elif line.startswith("#"):
                if "topotransfer-alignment" in line:
                    nums = [float(x) for x in line.split()[-16:]]
                    if len(nums) == 16:
                        alignment = nums
                elif "space:" in line:
                    space = "original" if "original" in line else "reference" if "reference" in line else None
    return WrappedObj(positions, alignment, space)


def split_positions(positions: Sequence[Vec3], blocks: Sequence[MeshBlock]) -> Dict[int, List[Vec3]]:
    """Split combined positions back into DNA meshes, validating the counts."""
    total = sum(b.vertex_count for b in blocks)
    if len(positions) != total:
        raise ValueError(
            f"Wrapped OBJ has {len(positions)} vertices but the manifest expects {total}. "
            "Was the file exported from TopoTransfer with the exported MetaHuman OBJ as Base?"
        )
    out: Dict[int, List[Vec3]] = {}
    for b in blocks:
        out[b.dna_index] = list(positions[b.offset : b.offset + b.vertex_count])
    return out


# ----------------------------------------------------------------------------- matrices


def mat4_apply(m: Sequence[float], p: Sequence[float]) -> Vec3:
    x, y, z = p
    return (
        m[0] * x + m[4] * y + m[8] * z + m[12],
        m[1] * x + m[5] * y + m[9] * z + m[13],
        m[2] * x + m[6] * y + m[10] * z + m[14],
    )


def mat4_inverse(m: Sequence[float]) -> List[float]:
    """Inverse of an affine column-major 4x4 (linear part inverted by cofactors)."""
    a = [[m[0], m[4], m[8]], [m[1], m[5], m[9]], [m[2], m[6], m[10]]]
    det = (
        a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
        - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
        + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0])
    )
    if abs(det) < 1e-300:
        raise ValueError("alignment matrix is singular")
    inv = [[0.0] * 3 for _ in range(3)]
    for r in range(3):
        for c in range(3):
            rows = [i for i in range(3) if i != c]
            cols = [j for j in range(3) if j != r]
            minor = a[rows[0]][cols[0]] * a[rows[1]][cols[1]] - a[rows[0]][cols[1]] * a[rows[1]][cols[0]]
            inv[r][c] = ((-1) ** (r + c)) * minor / det
    t = [m[12], m[13], m[14]]
    ti = [-(inv[r][0] * t[0] + inv[r][1] * t[1] + inv[r][2] * t[2]) for r in range(3)]
    return [inv[0][0], inv[1][0], inv[2][0], 0.0, inv[0][1], inv[1][1], inv[2][1], 0.0, inv[0][2], inv[1][2], inv[2][2], 0.0, ti[0], ti[1], ti[2], 1.0]


def to_dna_space(obj: WrappedObj) -> List[Vec3]:
    """Positions in Base (= DNA) space whichever export space was chosen in TopoTransfer."""
    if obj.space == "reference" and obj.alignment != IDENTITY4:
        inv = mat4_inverse(obj.alignment)
        return [mat4_apply(inv, p) for p in obj.positions]
    return list(obj.positions)


def _mm(a: Mat3, b: Mat3) -> Mat3:
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)) for i in range(3))  # type: ignore


def _mv(a: Mat3, v: Sequence[float]) -> Vec3:
    return (a[0][0] * v[0] + a[0][1] * v[1] + a[0][2] * v[2], a[1][0] * v[0] + a[1][1] * v[1] + a[1][2] * v[2], a[2][0] * v[0] + a[2][1] * v[1] + a[2][2] * v[2])


def _mtv(a: Mat3, v: Sequence[float]) -> Vec3:
    """transpose(a) @ v"""
    return (a[0][0] * v[0] + a[1][0] * v[1] + a[2][0] * v[2], a[0][1] * v[0] + a[1][1] * v[1] + a[2][1] * v[2], a[0][2] * v[0] + a[1][2] * v[1] + a[2][2] * v[2])


def euler_xyz_deg(rx: float, ry: float, rz: float) -> Mat3:
    """Rotation matrix for Maya rotate order xyz: R = Rz @ Ry @ Rx."""
    x, y, z = math.radians(rx), math.radians(ry), math.radians(rz)
    cx, sx, cy, sy, cz, sz = math.cos(x), math.sin(x), math.cos(y), math.sin(y), math.cos(z), math.sin(z)
    Rx = ((1, 0, 0), (0, cx, -sx), (0, sx, cx))
    Ry = ((cy, 0, sy), (0, 1, 0), (-sy, 0, cy))
    Rz = ((cz, -sz, 0), (sz, cz, 0), (0, 0, 1))
    return _mm(Rz, _mm(Ry, Rx))  # type: ignore


# ----------------------------------------------------------------------------- joints


@dataclass
class Skeleton:
    names: List[str]
    parents: List[int]  # parent index; root has parent == own index (DNA convention) or -1
    translations: List[Vec3]  # local
    rotations: List[Vec3]  # local, degrees XYZ

    def is_root(self, j: int) -> bool:
        p = self.parents[j]
        return p < 0 or p == j


def skeleton_from_reader(r) -> Skeleton:
    n = r.getJointCount()
    tx, ty, tz = r.getNeutralJointTranslationXs(), r.getNeutralJointTranslationYs(), r.getNeutralJointTranslationZs()
    rx, ry, rz = r.getNeutralJointRotationXs(), r.getNeutralJointRotationYs(), r.getNeutralJointRotationZs()
    return Skeleton(
        names=[r.getJointName(j) for j in range(n)],
        parents=[r.getJointParentIndex(j) for j in range(n)],
        translations=[(tx[j], ty[j], tz[j]) for j in range(n)],
        rotations=[(rx[j], ry[j], rz[j]) for j in range(n)],
    )


def joint_world(sk: Skeleton) -> Tuple[List[Vec3], List[Mat3]]:
    """World positions and world rotation matrices of all joints (parents may come in any order)."""
    n = len(sk.names)
    pos: List[Optional[Vec3]] = [None] * n
    rot: List[Optional[Mat3]] = [None] * n

    def solve(j: int, depth: int = 0) -> None:
        if pos[j] is not None:
            return
        if depth > n:
            raise ValueError("joint hierarchy has a cycle")
        local_r = euler_xyz_deg(*sk.rotations[j])
        if sk.is_root(j):
            pos[j] = sk.translations[j]
            rot[j] = local_r
            return
        p = sk.parents[j]
        solve(p, depth + 1)
        pr = rot[p]
        pp = pos[p]
        t = _mv(pr, sk.translations[j])  # type: ignore[arg-type]
        pos[j] = (pp[0] + t[0], pp[1] + t[1], pp[2] + t[2])  # type: ignore[index]
        rot[j] = _mm(pr, local_r)  # type: ignore[arg-type]

    for j in range(n):
        solve(j)
    return pos, rot  # type: ignore[return-value]


def local_translations_after_move(sk: Skeleton, world_rot: List[Mat3], world_delta: Dict[int, Vec3]) -> List[Vec3]:
    """
    New local translations when joint world positions move by `world_delta`
    and all rotations stay unchanged:  t'_j = t_j + R_parent^T (d_j - d_parent).
    """
    out: List[Vec3] = []
    for j, t in enumerate(sk.translations):
        dj = world_delta.get(j, (0.0, 0.0, 0.0))
        if sk.is_root(j):
            out.append((t[0] + dj[0], t[1] + dj[1], t[2] + dj[2]))
            continue
        p = sk.parents[j]
        dp = world_delta.get(p, (0.0, 0.0, 0.0))
        rel = _mtv(world_rot[p], (dj[0] - dp[0], dj[1] - dp[1], dj[2] - dp[2]))
        out.append((t[0] + rel[0], t[1] + rel[1], t[2] + rel[2]))
    return out


# ----------------------------------------------------------------------------- joint deltas


def skin_weighted_joint_deltas(
    joint_count: int,
    skin: Dict[int, List[List[Tuple[int, float]]]],
    deltas: Dict[int, List[Vec3]],
    min_total_weight: float = 1e-3,
) -> Tuple[Dict[int, Vec3], Dict[int, float]]:
    """
    Per-joint displacement = skin-weight-averaged displacement of the vertices
    the joint influences (over all given meshes). Returns deltas and total
    weight per joint (joints below `min_total_weight` are left out).
    """
    acc = [[0.0, 0.0, 0.0, 0.0] for _ in range(joint_count)]
    for mesh, per_vertex in skin.items():
        d = deltas.get(mesh)
        if d is None:
            continue
        for v, influences in enumerate(per_vertex):
            dv = d[v]
            for j, w in influences:
                if w <= 0:
                    continue
                a = acc[j]
                a[0] += w * dv[0]
                a[1] += w * dv[1]
                a[2] += w * dv[2]
                a[3] += w
    out: Dict[int, Vec3] = {}
    weights: Dict[int, float] = {}
    for j, a in enumerate(acc):
        if a[3] >= min_total_weight:
            out[j] = (a[0] / a[3], a[1] / a[3], a[2] / a[3])
            weights[j] = a[3]
    return out, weights


def nearest_vertex_deltas(points: Dict[int, Vec3], positions: Sequence[Vec3], deltas: Sequence[Vec3], k: int = 8) -> Dict[int, Vec3]:
    """Inverse-distance average of the k nearest vertex displacements, for joints without skin weights."""
    out: Dict[int, Vec3] = {}
    for j, p in points.items():
        best: List[Tuple[float, int]] = []
        for i, q in enumerate(positions):
            d2 = (q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2 + (q[2] - p[2]) ** 2
            if len(best) < k:
                best.append((d2, i))
                best.sort()
            elif d2 < best[-1][0]:
                best[-1] = (d2, i)
                best.sort()
        wsum = 0.0
        acc = [0.0, 0.0, 0.0]
        for d2, i in best:
            w = 1.0 / (math.sqrt(d2) + 1e-6)
            wsum += w
            for c in range(3):
                acc[c] += w * deltas[i][c]
        out[j] = (acc[0] / wsum, acc[1] / wsum, acc[2] / wsum) if wsum > 0 else (0.0, 0.0, 0.0)
    return out


# ----------------------------------------------------------------------------- eyes and teeth


def _solve4(m: List[List[float]], b: List[float]) -> Optional[List[float]]:
    """Gaussian elimination with partial pivoting for a 4x4 system; None when singular."""
    a = [row[:] + [b[i]] for i, row in enumerate(m)]
    for c in range(4):
        p = max(range(c, 4), key=lambda r: abs(a[r][c]))
        if abs(a[p][c]) < 1e-12:
            return None
        a[c], a[p] = a[p], a[c]
        for r in range(4):
            if r != c:
                f = a[r][c] / a[c][c]
                a[r] = [x - f * y for x, y in zip(a[r], a[c])]
    return [a[i][4] / a[i][i] for i in range(4)]


def centroid(points: Sequence[Vec3]) -> Vec3:
    n = float(len(points))
    return (sum(p[0] for p in points) / n, sum(p[1] for p in points) / n, sum(p[2] for p in points) / n)


def sphere_fit(points: Sequence[Vec3]) -> Tuple[Vec3, float]:
    """Least-squares sphere (centre, radius) through `points`; works on a partial sphere too."""
    if len(points) < 4:
        raise ValueError("a sphere needs at least 4 points")
    ata = [[0.0] * 4 for _ in range(4)]
    atb = [0.0] * 4
    for x, y, z in points:
        row = (2 * x, 2 * y, 2 * z, 1.0)
        rhs = x * x + y * y + z * z
        for i in range(4):
            atb[i] += row[i] * rhs
            for j in range(4):
                ata[i][j] += row[i] * row[j]
    u = _solve4(ata, atb)
    c = centroid(points)
    if u is None or u[3] + u[0] ** 2 + u[1] ** 2 + u[2] ** 2 <= 0:  # flat or degenerate: centroid + mean distance
        return c, sum(_dist(p, c) for p in points) / len(points)
    centre = (u[0], u[1], u[2])
    return centre, math.sqrt(u[3] + u[0] ** 2 + u[1] ** 2 + u[2] ** 2)


def _dist(a: Sequence[float], b: Sequence[float]) -> float:
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)


def split_two(points: Sequence[Vec3]) -> Tuple[List[Vec3], List[Vec3]]:
    """Two groups (both eyes picked as one selection): 2-means seeded at the ends of the widest axis."""
    axis = max(range(3), key=lambda k: max(p[k] for p in points) - min(p[k] for p in points))
    a, b = min(points, key=lambda p: p[axis]), max(points, key=lambda p: p[axis])
    for _ in range(20):
        ga = [p for p in points if _dist(p, a) <= _dist(p, b)]
        gb = [p for p in points if _dist(p, a) > _dist(p, b)]
        if not ga or not gb:
            break
        na, nb = centroid(ga), centroid(gb)
        if na == a and nb == b:
            break
        a, b = na, nb
    return ga, gb


def bounds(points: Sequence[Vec3]) -> Tuple[Vec3, Vec3]:
    """(centre, size) of the axis-aligned box around `points`."""
    lo = [min(p[k] for p in points) for k in range(3)]
    hi = [max(p[k] for p in points) for k in range(3)]
    return tuple((lo[k] + hi[k]) / 2 for k in range(3)), tuple(hi[k] - lo[k] for k in range(3))  # type: ignore


def _blocks_named(blocks: Sequence[MeshBlock], key: str) -> List[MeshBlock]:
    return [b for b in blocks if key.lower() in b.name.lower()]


def fit_parts(new_positions: Dict[int, List[Vec3]], blocks: Sequence[MeshBlock], eyes: Sequence[Sequence[Vec3]] = (),
              teeth: Sequence[Vec3] = ()) -> List[str]:
    """
    Put the MetaHuman eyes and teeth on the artist's (all in DNA space), in place in `new_positions`.

    eyes: the picked eye points, one list per eye or one list with both (split in two). Each
    MetaHuman eyeball is moved and scaled onto the nearer picked eye (sphere fit); the eye shell
    and eye edge follow the nearer eye. teeth: the picked teeth / gums / tongue points; the
    MetaHuman teeth (with the tongue) and saliva are moved and scaled onto their box.
    """
    report: List[str] = []
    if eyes:
        groups = [list(g) for g in eyes if g]
        if len(groups) == 1:
            groups = list(split_two(groups[0]))
        targets = [sphere_fit(g) for g in groups[:2]]
        mh = [(b, sphere_fit(new_positions[b.dna_index])) for b in _blocks_named(blocks, "eyeLeft") + _blocks_named(blocks, "eyeRight")]
        if len(targets) == 2 and len(mh) == 2:
            (b0, (c0, r0)), (b1, (c1, r1)) = mh
            straight = _dist(c0, targets[0][0]) + _dist(c1, targets[1][0])
            crossed = _dist(c0, targets[1][0]) + _dist(c1, targets[0][0])
            pairs = [(b0, c0, r0, targets[0]), (b1, c1, r1, targets[1])] if straight <= crossed else \
                [(b0, c0, r0, targets[1]), (b1, c1, r1, targets[0])]

            def move(p, cm, rm, cu, ru):
                s = ru / rm
                return (cu[0] + (p[0] - cm[0]) * s, cu[1] + (p[1] - cm[1]) * s, cu[2] + (p[2] - cm[2]) * s)

            for b, cm, rm, (cu, ru) in pairs:
                new_positions[b.dna_index] = [move(p, cm, rm, cu, ru) for p in new_positions[b.dna_index]]
                report.append(f"{b.name}: onto the picked eye (moved {_dist(cm, cu):.3f}, radius {rm:.3f} -> {ru:.3f})")
            for b in _blocks_named(blocks, "eyeshell") + _blocks_named(blocks, "eyeEdge"):
                out = []
                for p in new_positions[b.dna_index]:
                    _, cm, rm, (cu, ru) = min(pairs, key=lambda q: _dist(p, q[1]))
                    out.append(move(p, cm, rm, cu, ru))
                new_positions[b.dna_index] = out
                report.append(f"{b.name}: follows the eyes")
        else:
            report.append("eyes: need two picked eyes and the MetaHuman eyeLeft / eyeRight meshes; left as wrapped")
    if teeth:
        mh_teeth = _blocks_named(blocks, "teeth")
        if mh_teeth:
            cm, sm = bounds([p for b in mh_teeth for p in new_positions[b.dna_index]])
            cu, su = bounds(list(teeth))
            s = [min(2.0, max(0.5, su[k] / sm[k])) if sm[k] > 1e-9 else 1.0 for k in range(3)]
            for b in mh_teeth + _blocks_named(blocks, "saliva"):
                new_positions[b.dna_index] = [tuple(cu[k] + (p[k] - cm[k]) * s[k] for k in range(3)) for p in new_positions[b.dna_index]]  # type: ignore
                report.append(f"{b.name}: onto the picked teeth (moved {_dist(cm, cu):.3f}, scale {s[0]:.2f} {s[1]:.2f} {s[2]:.2f})")
        else:
            report.append("teeth: no MetaHuman teeth mesh in the manifest; left as wrapped")
    return report


# ----------------------------------------------------------------------------- calibration plan


def default_joint_filter(name: str) -> bool:
    """Move the facial rig only; body/neck joints keep their positions so the head still fits a MetaHuman body."""
    return name.startswith("FACIAL_")


@dataclass
class CalibrationPlan:
    #: mesh index -> per-vertex displacement (new - old), DNA space
    mesh_deltas: Dict[int, List[Vec3]]
    #: new local neutral joint translations for every joint
    joint_translations: List[Vec3]
    #: joint index -> world displacement applied
    joint_world_deltas: Dict[int, Vec3]
    report: List[str]


def read_mesh_positions(r, mesh: int) -> List[Vec3]:
    xs, ys, zs = r.getVertexPositionXs(mesh), r.getVertexPositionYs(mesh), r.getVertexPositionZs(mesh)
    return [(xs[i], ys[i], zs[i]) for i in range(len(xs))]


def read_skin(r, mesh: int) -> List[List[Tuple[int, float]]]:
    out = []
    for v in range(r.getSkinWeightsCount(mesh)):
        out.append(list(zip(r.getSkinWeightsJointIndices(mesh, v), r.getSkinWeightsValues(mesh, v))))
    return out


def build_calibration_plan(
    r,
    new_positions: Dict[int, List[Vec3]],
    joint_filter: Callable[[str], bool] = default_joint_filter,
    skin_meshes: Optional[Sequence[int]] = None,
    max_joint_move: Optional[float] = None,
) -> CalibrationPlan:
    """
    Compute what to write into the DNA:
    * mesh displacements for every wrapped mesh,
    * joint moves = skin-weighted average displacement of their vertices
      (fallback: nearest vertices of the first skin mesh), for joints that
      pass `joint_filter`; converted to local translations with rotations kept.
    """
    report: List[str] = []
    mesh_deltas: Dict[int, List[Vec3]] = {}
    old_positions: Dict[int, List[Vec3]] = {}
    for mesh, new in new_positions.items():
        old = read_mesh_positions(r, mesh)
        if len(old) != len(new):
            raise ValueError(f"mesh {mesh} ({r.getMeshName(mesh)}): DNA has {len(old)} vertices, wrapped result has {len(new)}")
        old_positions[mesh] = old
        d = [(n[0] - o[0], n[1] - o[1], n[2] - o[2]) for o, n in zip(old, new)]
        mesh_deltas[mesh] = d
        mx = max((math.sqrt(x * x + y * y + z * z) for x, y, z in d), default=0.0)
        report.append(f"mesh {mesh} {r.getMeshName(mesh)}: {len(d)} vertices, max move {mx:.3f}")

    sk = skeleton_from_reader(r)
    world_pos, world_rot = joint_world(sk)
    skin_list = list(skin_meshes) if skin_meshes is not None else [m for m in new_positions if r.getSkinWeightsCount(m) > 0]
    skin = {m: read_skin(r, m) for m in skin_list}
    weighted, weights = skin_weighted_joint_deltas(len(sk.names), skin, mesh_deltas)
    wanted = [j for j, n in enumerate(sk.names) if joint_filter(n)]
    deltas: Dict[int, Vec3] = {}
    missing = {}
    for j in wanted:
        if j in weighted:
            deltas[j] = weighted[j]
        else:
            missing[j] = world_pos[j]
    if missing and skin_list:
        fb = skin_list[0]
        deltas.update(nearest_vertex_deltas(missing, old_positions[fb], mesh_deltas[fb]))
        report.append(f"{len(missing)} selected joint(s) without skin weights moved with their nearest vertices")
    if max_joint_move is not None:
        for j, d in list(deltas.items()):
            l = math.sqrt(d[0] ** 2 + d[1] ** 2 + d[2] ** 2)
            if l > max_joint_move:
                s = max_joint_move / l
                deltas[j] = (d[0] * s, d[1] * s, d[2] * s)
    translations = local_translations_after_move(sk, world_rot, deltas)
    moved = [math.sqrt(d[0] ** 2 + d[1] ** 2 + d[2] ** 2) for d in deltas.values()]
    report.append(f"{len(deltas)} of {len(sk.names)} joints moved (max {max(moved) if moved else 0:.3f}, mean {sum(moved) / len(moved) if moved else 0:.3f})")
    return CalibrationPlan(mesh_deltas, translations, deltas, report)
