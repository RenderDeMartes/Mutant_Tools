"""
The points you pick in Meta Mutant's Pick Points window, without Maya: what there is to pick, how it is
stored (<work>/points.json) and how it reaches TopoTransfer (<work>/guides.json).

Three kinds of picks, always on your head; the MetaHuman side is already known, its topology never changes:

* guides: named points, one vertex each (nose tip, eye corners...);
* lines: the lip contact lines and eyelid margins, edge loops from corner to corner. Each is matched to
  its MetaHuman line by arc length (lips: each side of the midline on its own), giving many exact pairs
  where a closest-point wrap goes wrong: where two surfaces touch;
* regions: faces of the lips, eyelids and mouth bag (mm_regions.REGIONS), for the wrap and the rig transfer.

Your side goes to TopoTransfer as positions, not vertex ids: the exported Reference has the picked eyes
and teeth cut out, which renumbers its vertices. Regions do need vertex ids, so they go through the
old id -> OBJ id map of the export.

Pure Python + numpy (no Maya), so it is tested on its own.
"""

from __future__ import annotations

import json
import os
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

Vec3 = Tuple[float, float, float]

VERSION = 1
#: every how many MetaHuman line vertices a pair is made (the lip lines have over 120 vertices)
LINE_STEP = 3
#: weight of one line pair against a named guide (1). There are many, close together: on a test head 0.02 and 0.2
#: both kept the lips from crossing, but 0.2 flipped about six times as many faces
LINE_WEIGHT = 0.02
#: radius of the spheres marking points, in hundredths of your head's height
DEFAULT_SPHERE_SIZE = 0.5

#: (label, MetaHuman head vertex, TopoTransfer group), in the order they are asked for. The same points
#: as METAHUMAN_FACE_VERTEX in TopoTransfer's landmarks/presets.ts (tests/test_points.py keeps them equal)
GUIDES: Tuple[Tuple[str, int, str], ...] = (
    ("Glabella", 16130, "face"),
    ("Nasion", 9854, "nose"),
    ("Nose tip", 17088, "nose"),
    ("Subnasale", 17113, "nose"),
    ("Nose ala L", 22337, "nose"),
    ("Nose ala R", 700, "nose"),
    ("Eye inner corner L", 4076, "eyes"),
    ("Eye inner corner R", 13836, "eyes"),
    ("Eye outer corner L", 22252, "eyes"),
    ("Eye outer corner R", 19239, "eyes"),
    ("Upper eyelid L", 9699, "eyes"),
    ("Upper eyelid R", 19741, "eyes"),
    ("Lower eyelid L", 9305, "eyes"),
    ("Lower eyelid R", 15290, "eyes"),
    ("Mouth corner L", 21624, "mouth"),
    ("Mouth corner R", 18611, "mouth"),
    ("Upper lip center", 2909, "mouth"),
    ("Lower lip center", 2881, "mouth"),
    ("Chin", 2971, "face"),
    ("Chin bottom", 2977, "face"),
    ("Jaw angle L", 23934, "face"),
    ("Jaw angle R", 20921, "face"),
    ("Cheekbone L", 4910, "face"),
    ("Cheekbone R", 1839, "face"),
    ("Ear top L", 4853, "ears"),
    ("Ear top R", 1782, "ears"),
    ("Tragus L", 5299, "ears"),
    ("Tragus R", 2228, "ears"),
    ("Earlobe L", 8011, "ears"),
    ("Earlobe R", 13989, "ears"),
)

#: short help for each guide, shown while it is being asked for
GUIDE_HINTS: Dict[str, str] = {
    "Glabella": "between the eyebrows, most forward point",
    "Nasion": "deepest point of the nose bridge",
    "Nose tip": "most forward point of the nose",
    "Subnasale": "where the nose septum meets the upper lip",
    "Nose ala": "outermost point of the nostril wing",
    "Eye inner corner": "inner corner of the eye",
    "Eye outer corner": "outer corner of the eye",
    "Upper eyelid": "middle of the upper lid, on the skin above the margin",
    "Lower eyelid": "middle of the lower lid, on the skin below the margin",
    "Mouth corner": "where the lips meet at the side",
    "Upper lip center": "centre of the upper lip, on its outer border",
    "Lower lip center": "centre of the lower lip, on its outer border",
    "Chin": "most forward point of the chin",
    "Chin bottom": "lowest point of the chin",
    "Jaw angle": "corner of the jaw",
    "Cheekbone": "most prominent point of the cheekbone",
    "Ear top": "highest point of the ear",
    "Tragus": "small flap in front of the ear canal",
    "Earlobe": "lowest point of the earlobe",
}

#: (key, label shown, help) of each line, in the order they are asked for
LINES: Tuple[Tuple[str, str, str], ...] = (
    ("upper_lip", "Upper lip line", "line where the lips meet"),
    ("lower_lip", "Lower lip line", "line where the lips meet"),
    ("upper_lid_L", "Upper eyelid line L", "edge of the eye opening (character's left)"),
    ("lower_lid_L", "Lower eyelid line L", "edge of the eye opening (character's left)"),
    ("upper_lid_R", "Upper eyelid line R", "edge of the eye opening (character's right)"),
    ("lower_lid_R", "Lower eyelid line R", "edge of the eye opening (character's right)"),
)
LIP_LINES = ("upper_lip", "lower_lip")
#: the two lines one closed loop around the mouth or an eye splits into
LINE_PAIRS = (("upper_lip", "lower_lip"), ("upper_lid_L", "lower_lid_L"), ("upper_lid_R", "lower_lid_R"))

#: the same lines on the MetaHuman head, ordered by rising X (character's right to left). Found on Ada: the
#: edge loops where the lips touch, then the fold out to the mouth corner; the 60 vertex ring of each eye
#: opening, split at its corners
METAHUMAN_LINES: Dict[str, List[int]] = {
    "upper_lip": [
        18611, 13270, 20699, 13268, 18610, 13267, 20586, 15042, 19406, 13086, 18543, 13031, 18516,
        12077, 18038, 12075, 18085, 12199, 18090, 12209, 18091, 12213, 18092, 12216, 18096, 12225,
        18108, 12255, 18117, 12274, 18127, 12293, 156, 12289, 157, 12300, 162, 12303, 163, 12304, 164,
        12306, 165, 12308, 166, 12334, 178, 12344, 183, 12354, 188, 12364, 193, 12808, 202, 12382, 201,
        12392, 208, 12402, 213, 12412, 2904, 6461, 3284, 6455, 3279, 6445, 3272, 6432, 3273, 6844, 3264,
        6417, 3259, 6407, 3254, 6397, 3249, 6387, 3237, 6361, 3236, 6359, 3235, 6357, 3234, 6354, 3233,
        6353, 3228, 6343, 3227, 6344, 21140, 6325, 21130, 6306, 21121, 6276, 21109, 6266, 21105, 6263,
        21104, 6261, 21103, 6252, 21098, 6134, 21051, 6132, 21529, 7057, 21556, 7111, 22419, 9063,
        23599, 7293, 21623, 7292, 23712, 7296, 21624,
    ],
    "lower_lip": [
        18611, 13270, 20699, 13268, 18610, 13267, 20586, 15042, 19406, 13086, 18543, 13031, 18516,
        12077, 18038, 12075, 18085, 12199, 18090, 12209, 18091, 12213, 18092, 12214, 18243, 12533,
        18247, 12542, 18259, 12570, 18268, 12586, 18278, 12607, 311, 12604, 310, 12612, 314, 12613, 315,
        12616, 316, 12618, 317, 12620, 318, 12628, 322, 12636, 326, 12644, 330, 12652, 334, 12660, 338,
        12668, 342, 12671, 343, 12684, 350, 12692, 2884, 6731, 3421, 6726, 3414, 6712, 3413, 6710, 3409,
        6702, 3405, 6694, 3401, 6686, 3397, 6678, 3393, 6670, 3389, 6662, 3388, 6660, 3387, 6658, 3386,
        6657, 3385, 6654, 3381, 6649, 3382, 6651, 21291, 6630, 21281, 6614, 21272, 6586, 21260, 6577,
        21256, 6268, 21105, 6263, 21104, 6261, 21103, 6252, 21098, 6134, 21051, 6132, 21529, 7057,
        21556, 7111, 22419, 9063, 23599, 7293, 21623, 7292, 23712, 7296, 21624,
    ],
    "upper_lid_L": [
        7896, 4079, 7863, 4076, 7857, 4067, 7841, 4064, 7839, 4059, 7831, 4060, 8696, 4025, 7776, 4024,
        9121, 3980, 7700, 3979, 7707, 3985, 8749, 4087, 7889, 3909, 7595, 3908, 8767, 3896,
    ],
    "lower_lid_L": [
        7896, 4009, 7748, 4006, 7742, 4001, 7735, 3999, 7732, 3997, 7727, 3996, 8702, 3976, 7696, 3973,
        7692, 3972, 7689, 3971, 8760, 3942, 7645, 3941, 7644, 3903, 7588, 3902, 8763, 3897, 7581, 3896,
    ],
    "upper_lid_R": [
        825, 14746, 837, 13573, 838, 13867, 1016, 14729, 914, 13686, 908, 13680, 909, 15102, 953, 13756,
        954, 14675, 989, 13811, 988, 13816, 993, 13820, 996, 13838, 1005, 13842, 1008, 13874,
    ],
    "lower_lid_R": [
        825, 13560, 826, 14742, 831, 13567, 832, 13621, 870, 13625, 871, 14739, 900, 13670, 901, 13673,
        902, 13676, 905, 14681, 925, 13707, 926, 13709, 928, 13716, 930, 13721, 935, 13725, 938, 13874,
    ],
}


def guide_hint(label: str) -> str:
    return GUIDE_HINTS.get(label[:-2] if label.endswith((" L", " R")) else label, "")


def mirror_label(label: str) -> Optional[str]:
    if label.endswith(" L"):
        return label[:-2] + " R"
    if label.endswith(" R"):
        return label[:-2] + " L"
    return None


# ----------------------------------------------------------------------------- points.json


def empty(mesh: str = "", vertex_count: int = 0) -> dict:
    return {"version": VERSION, "mesh": mesh, "vertex_count": vertex_count, "guides": {}, "lines": {},
            "mirror": False, "sphere_size": DEFAULT_SPHERE_SIZE}


def load(path: str) -> dict:
    """The points saved in `path`, or nothing picked when there is no such file or it is not readable."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        return empty()
    out = empty()
    if isinstance(data, dict):
        out.update({k: v for k, v in data.items() if k in out})
    return out


def save(points: dict, path: str) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(points, f, indent=1)


def stale(points: dict, mesh: str, vertex_count: int) -> Optional[str]:
    """Why saved points do not fit this mesh (vertex ids mean nothing on other topology), or None."""
    if not points.get("guides") and not points.get("lines"):
        return None
    if points.get("vertex_count") != vertex_count:
        return f"the points were picked on {points.get('mesh') or 'another mesh'} ({points.get('vertex_count')} vertices), {mesh} has {vertex_count}"
    return None


def refreshed(points: dict, positions) -> dict:
    """The points with their positions read again from the mesh (it may have moved since they were picked)."""
    p = [tuple(float(v) for v in q) for q in positions]
    out = dict(points)
    out["guides"] = {k: dict(g, position=list(p[g["vertex"]])) for k, g in points.get("guides", {}).items()}
    out["lines"] = {k: dict(l, positions=[list(p[v]) for v in l["vertices"]]) for k, l in points.get("lines", {}).items()}
    return out


def summary(points: dict, regions: Optional[Dict[str, list]] = None, eyes: Sequence[str] = (), teeth: Sequence[str] = ()) -> str:
    """One line for the window: what was picked."""
    parts = [f"{len(points.get('guides', {}))} of {len(GUIDES)} points", f"{len(points.get('lines', {}))} of {len(LINES)} lines"]
    picked = sum(1 for v in (regions or {}).values() if v)
    if picked:
        parts.append(f"{picked} regions")
    if eyes:
        parts.append("eyes")
    if teeth:
        parts.append("teeth")
    return ", ".join(parts)


# ----------------------------------------------------------------------------- lines


def chain_from_edges(edges: Sequence[Tuple[int, int]]) -> List[int]:
    """The vertices of selected edges in path order. The message says what to fix when they are not one open path."""
    if not edges:
        raise ValueError("no edges selected")
    around: Dict[int, List[int]] = {}
    for a, b in edges:
        around.setdefault(a, []).append(b)
        around.setdefault(b, []).append(a)
    branching = [v for v, n in around.items() if len(n) > 2]
    if branching:
        raise ValueError(f"the edges branch at vertex {branching[0]}: select one line, from corner to corner")
    ends = [v for v, n in around.items() if len(n) == 1]
    if not ends:
        raise ValueError("the edges make a closed loop: select only this part of it, from corner to corner")
    if len(ends) > 2:
        raise ValueError(f"the edges are {len(ends) // 2} separate lines: select one line, from corner to corner, with no gaps")
    chain = [ends[0]]
    previous = None
    while True:
        following = [n for n in around[chain[-1]] if n != previous]
        if not following:
            return chain
        previous = chain[-1]
        chain.append(following[0])


def is_ring(edges: Sequence[Tuple[int, int]]) -> bool:
    """The edges close on themselves: every vertex has exactly two of them, and they are all one loop."""
    around: Dict[int, List[int]] = {}
    for a, b in edges:
        around.setdefault(a, []).append(b)
        around.setdefault(b, []).append(a)
    if len(around) < 3 or any(len(n) != 2 for n in around.values()):
        return False
    return len(ring_from_edges(edges)) == len(around)


def ring_from_edges(edges: Sequence[Tuple[int, int]]) -> List[int]:
    """The vertices of a closed loop in order (the loop holding the first edge)."""
    around: Dict[int, List[int]] = {}
    for a, b in edges:
        around.setdefault(a, []).append(b)
        around.setdefault(b, []).append(a)
    ring = [edges[0][0]]
    previous = None
    while True:
        following = [n for n in around[ring[-1]] if n != previous]
        step = following[0] if following else previous
        if step == ring[0] and len(ring) > 2:
            return ring
        previous = ring[-1]
        ring.append(step)


def split_ring(ring: Sequence[int], positions) -> Tuple[List[int], List[int]]:
    """A closed loop around the mouth or an eye cut at its corners (lowest and highest X): the upper line and
    the lower line, each by rising X, both holding the two corners."""
    p = np.asarray(positions, float)
    ring = list(ring)
    x = p[ring, 0]
    a, b = sorted((int(np.argmin(x)), int(np.argmax(x))))
    one, other = ring[a:b + 1], ring[b:] + ring[:a + 1]
    if p[one, 1].mean() < p[other, 1].mean():
        one, other = other, one
    return oriented(one, p), oriented(other, p)


def opening_of(upper: Sequence[int], lower: Sequence[int]) -> Tuple[List[int], List[int]]:
    """Two lines cut down to where they really part. The MetaHuman's lip lines run on to the mouth corner as one and the
    same crease of skin, which cannot open: only the part between the last shared vertices is the mouth's opening."""
    upper, lower = list(upper), list(lower)
    start = 0
    while start + 1 < min(len(upper), len(lower)) and upper[start + 1] == lower[start + 1]:
        start += 1
    end = 0
    while end + 1 < min(len(upper), len(lower)) - start and upper[-2 - end] == lower[-2 - end]:
        end += 1
    return upper[start:len(upper) - end], lower[start:len(lower) - end]


def line_side_problem(key: str, vertices: Sequence[int], positions, midline: float) -> Optional[str]:
    """An eyelid line on the wrong side of the face, in words; left is the character's left, X above the midline."""
    if not key.endswith(("_L", "_R")):
        return None
    x = float(np.asarray(positions, float)[list(vertices), 0].mean())
    if key.endswith("_L") != (x > midline):
        return "That is the {} eye; this line is for the {} eye (the character's).".format(
            "right" if key.endswith("_L") else "left", "left" if key.endswith("_L") else "right")
    return None


def oriented(chain: Sequence[int], positions) -> List[int]:
    """The chain ordered by rising X, like METAHUMAN_LINES."""
    chain = list(chain)
    p = np.asarray(positions, float)
    return chain if p[chain[0], 0] <= p[chain[-1], 0] else chain[::-1]


def arc_params(points, midline: Optional[float] = None) -> np.ndarray:
    """Position of each point along the line: 0..1 by arc length, or with `midline` -1..0 on the side of
    lower X and 0..1 on the other, so the middle of two lines meets even when one side of a lip is longer."""
    p = np.asarray(points, float)
    if len(p) < 2:
        return np.zeros(len(p))
    arc = np.r_[0.0, np.cumsum(np.linalg.norm(np.diff(p, axis=0), axis=1))]
    if arc[-1] <= 0:
        return np.zeros(len(p))
    if midline is not None:
        x = p[:, 0]
        cross = [i for i in range(len(p) - 1) if (x[i] - midline) * (x[i + 1] - midline) <= 0 and x[i] != x[i + 1]]
        if cross:
            i = cross[0]
            at = arc[i] + (midline - x[i]) / (x[i + 1] - x[i]) * (arc[i + 1] - arc[i])
            if 0 < at < arc[-1]:
                return np.where(arc <= at, (arc - at) / at, (arc - at) / (arc[-1] - at))
    return arc / arc[-1]


def point_at(points, params, t: float) -> Vec3:
    """The point of a polyline at parameter `t` (see arc_params)."""
    p = np.asarray(points, float)
    q = np.asarray(params, float)
    t = float(np.clip(t, q[0], q[-1]))
    i = int(np.clip(np.searchsorted(q, t, side="right") - 1, 0, len(q) - 2))
    span = q[i + 1] - q[i]
    u = 0.0 if span <= 0 else (t - q[i]) / span
    return tuple(float(v) for v in p[i] + (p[i + 1] - p[i]) * u)


def match_line(base_points, custom_points, base_midline: Optional[float] = None, custom_midline: Optional[float] = None) -> List[Vec3]:
    """For each point of the MetaHuman line, the matching point on your line. Both ordered by rising X."""
    both = base_midline is not None and custom_midline is not None
    b = arc_params(base_points, base_midline if both else None)
    c = arc_params(custom_points, custom_midline if both else None)
    if both and (b[0] < 0) != (c[0] < 0):  # one of them does not cross its midline: plain arc length
        b, c = arc_params(base_points), arc_params(custom_points)
    return [point_at(custom_points, c, t) for t in b]


def line_pairs(key: str, custom_points, base_positions, base_midline: Optional[float] = None,
               custom_midline: Optional[float] = None, step: int = LINE_STEP) -> List[Tuple[int, Vec3]]:
    """(MetaHuman vertex, position on your head) along a line; every `step` vertices and always both ends."""
    chain = METAHUMAN_LINES[key]
    if key not in LIP_LINES:
        base_midline = custom_midline = None
    matched = match_line(np.asarray(base_positions, float)[chain], custom_points, base_midline, custom_midline)
    keep = sorted(set(range(0, len(chain), max(1, step))) | {len(chain) - 1})
    return [(chain[i], matched[i]) for i in keep]


# ----------------------------------------------------------------------------- alignment


def fit_similarity(source, target) -> Tuple[float, np.ndarray, np.ndarray]:
    """Umeyama: scale, rotation (3x3) and translation mapping source points onto target points."""
    s, t = np.asarray(source, float), np.asarray(target, float)
    if len(s) != len(t) or len(s) < 3:
        raise ValueError("needs at least 3 pairs")
    cs, ct = s.mean(0), t.mean(0)
    a, b = s - cs, t - ct
    u, d, vt = np.linalg.svd(b.T @ a / len(s))
    sign = np.eye(3)
    if np.linalg.det(u) * np.linalg.det(vt) < 0:
        sign[2, 2] = -1
    r = u @ sign @ vt
    var = (a ** 2).sum() / len(s)
    scale = float(np.trace(np.diag(d) @ sign) / var) if var > 0 else 1.0
    return scale, r, ct - scale * r @ cs


def similarity_matrix(scale: float, r: np.ndarray, t: np.ndarray) -> List[float]:
    """Maya's row-major list: row 3 holds the translation."""
    m = np.eye(4)
    m[:3, :3] = (scale * r).T
    m[3, :3] = t
    return [float(v) for v in m.ravel()]


def bounds_fit(source_min, source_max, target_min, target_max) -> Tuple[float, np.ndarray]:
    """Scale and translation that lay a head over another by their boxes: same width, top and centre together."""
    smin, smax, tmin, tmax = (np.asarray(v, float) for v in (source_min, source_max, target_min, target_max))
    ss, ts = smax - smin, tmax - tmin
    scale = float(ts[0] / max(ss[0], 1e-9))
    move = np.array([(tmin[0] + tmax[0]) / 2 - scale * (smin[0] + smax[0]) / 2, tmax[1] - scale * smax[1],
                     (tmin[2] + tmax[2]) / 2 - scale * (smin[2] + smax[2]) / 2])
    return scale, move


def midline_x(points: dict, fallback: float) -> float:
    """The head's midline, from the centre-line guides picked; `fallback` (the middle of the mesh) without them."""
    xs = [g["position"][0] for label, g in points.get("guides", {}).items() if not label.endswith((" L", " R"))]
    return float(np.median(xs)) if xs else fallback


def nearest_vertex(positions, point) -> int:
    p = np.asarray(positions, float)
    return int(np.argmin(((p - np.asarray(point, float)) ** 2).sum(1)))


def mirrored_vertex(positions, vertex: int, midline: float) -> int:
    """The vertex nearest the reflection of `vertex` across the plane X = midline."""
    p = np.asarray(positions, float)
    q = p[vertex].copy()
    q[0] = 2 * midline - q[0]
    return nearest_vertex(p, q)


# ----------------------------------------------------------------------------- guides.json


def launch_guides(points: dict, base_positions, base_regions: Optional[Dict[str, List[int]]] = None,
                  ref_regions: Optional[Dict[str, List[int]]] = None, custom_fallback_midline: float = 0.0) -> dict:
    """What TopoTransfer loads: every picked pair, and the regions with vertices on both sides."""
    base = np.asarray(base_positions, float)
    by_label = {label: (vertex, group) for label, vertex, group in GUIDES}
    landmarks = []
    for label, picked in points.get("guides", {}).items():
        if label in by_label:
            vertex, group = by_label[label]
            landmarks.append({"label": label, "group": group, "weight": 1.0, "base_vertex": vertex,
                              "ref": [float(v) for v in picked["position"]]})
    # the midline of the MetaHuman head: its nose tip, nose bridge and chin
    centre = [by_label[k][0] for k in ("Nasion", "Nose tip", "Chin")]
    base_mid = float(np.median(base[centre, 0]))
    custom_mid = midline_x(points, custom_fallback_midline)
    # a vertex on two lines (the lips share the fold out to the corner) takes the middle of both
    shared: Dict[int, List[Vec3]] = {}
    keys = {}
    for key, _, _ in LINES:
        line = points.get("lines", {}).get(key)
        if not line or len(line.get("positions", [])) < 2:
            continue
        for vertex, spot in line_pairs(key, line["positions"], base, base_mid, custom_mid):
            shared.setdefault(vertex, []).append(spot)
            keys.setdefault(vertex, key)
    for vertex, spots in shared.items():
        landmarks.append({"label": f"Line {keys[vertex]} {vertex}", "group": "lines", "weight": LINE_WEIGHT,
                          "base_vertex": vertex, "ref": [float(v) for v in np.mean(spots, axis=0)]})
    regions = {}
    for name, ref in (ref_regions or {}).items():
        src = (base_regions or {}).get(name)
        if ref and src:
            regions[name] = {"base": [int(v) for v in src], "ref": [int(v) for v in ref]}
    return {"version": VERSION, "landmarks": landmarks, "regions": regions}


def reference_regions(regions: Dict[str, List[int]], remap: Optional[Sequence[int]]) -> Dict[str, List[int]]:
    """Region vertex ids of your head as ids of the exported Reference (`remap`: old id -> OBJ id, -1 = cut out)."""
    if remap is None:
        return {k: list(v) for k, v in regions.items()}
    return {k: [remap[v] for v in ids if 0 <= v < len(remap) and remap[v] >= 0] for k, ids in regions.items()}


def write_guides(path: str, guides: dict) -> str:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(guides, f)
    return path
