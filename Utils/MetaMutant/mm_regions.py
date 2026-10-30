"""
Face regions for the rig transfer: lips, eyelids, mouth bag, eye sockets.

Closest-point transfer bleeds where two surfaces touch: a point of your upper lip can be closer to the
MetaHuman's lower lip, and then opens with the jaw (the same for eyelids). With regions, each vertex
of your head picked as, say, the upper lip takes its skin weights and blendshapes only from the
MetaHuman's upper lip; the rest of your head only from the MetaHuman outside the regions you picked.

The MetaHuman's regions need no picking: its topology is always the same, and its skin weights say
which joints move each vertex (FACIAL_*_LipUpper*, *_EyelidLower*, *_MouthInterior*...). The eye
socket has no joints of its own: socket vertices take their skin from the face around the eye (not
the lids) and are kept still by the blendshapes.

Pure Python + numpy (no Maya), so it is tested on its own.
"""

from __future__ import annotations

import re
from typing import Dict, List, Sequence, Tuple

import numpy as np

#: (key, label shown in Meta Mutant) in the window's order
REGIONS = (
    ("upper_lip", "Upper lip"),
    ("lower_lip", "Lower lip"),
    ("upper_eyelid", "Upper eyelids"),
    ("lower_eyelid", "Lower eyelids"),
    ("mouth_bag", "Mouth bag"),
    ("eye_socket", "Eye sockets"),
)
#: regions matched to the same region of the MetaHuman (the eye socket is matched to the face around it)
MATCHED = ("upper_lip", "lower_lip", "upper_eyelid", "lower_eyelid", "mouth_bag")
THRESHOLD = 0.35  # a MetaHuman vertex belongs to a region when its joints there weigh at least this much


def _family(joint: str) -> str:
    """'FACIAL_L_12IPV_LipUpper3' -> '12IPV_LipUpper'."""
    return re.sub(r"\d+$", "", re.sub(r"^FACIAL_[LRC]_", "", joint))


def _rule(region: str, family: str) -> bool:
    if region == "upper_lip":
        return "LipUpper" in family
    if region == "lower_lip":
        return "LipLower" in family or family == "LowerLipRotation"
    if region == "upper_eyelid":
        return family.startswith(("EyelidUpperA", "EyelidUpperB"))
    if region == "lower_eyelid":
        return family.startswith("EyelidLower")
    if region == "mouth_bag":
        return family.startswith(("MouthUpper", "MouthLower")) or "MouthInterior" in family
    return False


def metahuman_regions(joint_names: Sequence[str], weights: Sequence[Sequence[Tuple[int, float]]],
                      threshold: float = THRESHOLD) -> Dict[str, List[int]]:
    """The MetaHuman head's region of each vertex from its skin: (joint, weight) pairs per vertex."""
    families = [_family(n) for n in joint_names]
    member = {r: [_rule(r, f) for f in families] for r in MATCHED}
    out: Dict[str, List[int]] = {r: [] for r in MATCHED}
    for v, vw in enumerate(weights):
        score = {r: sum(w for j, w in vw if member[r][j]) for r in MATCHED}
        best = max(score, key=score.get)
        if score[best] >= threshold:
            out[best].append(v)
    return out


def groups(target_count: int, target_regions: Dict[str, Sequence[int]], source_count: int,
           source_regions: Dict[str, Sequence[int]]) -> List[Tuple[np.ndarray, np.ndarray]]:
    """(target vertices, source vertices they may use): each picked region with its MetaHuman region,
    the eye sockets and everything else with the MetaHuman outside every picked region."""
    picked = {r: np.unique(np.asarray(ids, int)) for r, ids in target_regions.items() if len(ids)}
    taken = np.zeros(target_count, bool)
    out = []
    used_source = np.zeros(source_count, bool)
    for r in MATCHED:
        if r in picked and len(source_regions.get(r, ())):
            src = np.unique(np.asarray(source_regions[r], int))
            tgt = picked[r][~taken[picked[r]]]
            taken[tgt] = True
            used_source[src] = True
            out.append((tgt, src))
    if "eye_socket" in picked:
        # the sockets: the face around the eye, never the MetaHuman's lids, lips or mouth
        tgt = picked["eye_socket"][~taken[picked["eye_socket"]]]
        taken[tgt] = True
        every = np.zeros(source_count, bool)
        for r in MATCHED:
            every[np.asarray(source_regions.get(r, ()), int)] = True
        out.append((tgt, np.flatnonzero(~every)))
    rest = np.flatnonzero(~taken)
    outside = np.flatnonzero(~used_source)
    out.append((rest, outside if len(outside) else np.arange(source_count)))
    return [(t, s) for t, s in out if len(t)]


def _closest_on_triangle(p: np.ndarray, a: np.ndarray, b: np.ndarray, c: np.ndarray) -> Tuple[float, Tuple[float, float, float]]:
    """Squared distance from p to triangle abc and the barycentric weights (for a, b, c) of the closest point."""
    ab, ac, ap = b - a, c - a, p - a
    d1, d2 = ab @ ap, ac @ ap
    if d1 <= 0 and d2 <= 0:
        w = (1.0, 0.0, 0.0)
    else:
        bp = p - b
        d3, d4 = ab @ bp, ac @ bp
        cp = p - c
        d5, d6 = ab @ cp, ac @ cp
        vc, vb, va = d1 * d4 - d3 * d2, d5 * d2 - d1 * d6, d3 * d6 - d5 * d4
        if d3 >= 0 and d4 <= d3:
            w = (0.0, 1.0, 0.0)
        elif d6 >= 0 and d5 <= d6:
            w = (0.0, 0.0, 1.0)
        elif vc <= 0 and d1 >= 0 and d3 <= 0:
            t = d1 / (d1 - d3)
            w = (1 - t, t, 0.0)
        elif vb <= 0 and d2 >= 0 and d6 <= 0:
            t = d2 / (d2 - d6)
            w = (1 - t, 0.0, t)
        elif va <= 0 and (d4 - d3) >= 0 and (d5 - d6) >= 0:
            t = (d4 - d3) / ((d4 - d3) + (d5 - d6))
            w = (0.0, 1 - t, t)
        else:
            den = 1.0 / (va + vb + vc)
            v, u = vb * den, vc * den
            w = (1 - v - u, v, u)
    q = a * w[0] + b * w[1] + c * w[2]
    return float(((p - q) ** 2).sum()), w


def correspondence(target_points: np.ndarray, source_points: np.ndarray, triangles: np.ndarray,
                   groups_: List[Tuple[np.ndarray, np.ndarray]]) -> List[Tuple[Tuple[int, int, int], Tuple[float, float, float]]]:
    """For each target vertex: a source triangle and barycentric weights of its closest point, searching
    only the source vertices its group allows (nearest allowed vertex, then the best of the triangles
    around it whose corners are all allowed; the vertex itself when none is)."""
    target_points = np.asarray(target_points, float)
    source_points = np.asarray(source_points, float)
    triangles = np.asarray(triangles, int).reshape(-1, 3)
    around: List[List[int]] = [[] for _ in range(len(source_points))]
    for t, tri in enumerate(triangles):
        for v in tri:
            around[v].append(t)
    out: List = [None] * len(target_points)
    for tgt, allowed in groups_:
        mask = np.zeros(len(source_points), bool)
        mask[allowed] = True
        pts = source_points[allowed]
        sq = (pts ** 2).sum(1)
        for start in range(0, len(tgt), 512):
            chunk = tgt[start:start + 512]
            p = target_points[chunk]
            d = (p ** 2).sum(1)[:, None] - 2 * p @ pts.T + sq[None, :]
            nearest = allowed[np.argmin(d, axis=1)]
            for t, v in zip(chunk, nearest):
                best = None
                for tri_id in around[v]:
                    tri = triangles[tri_id]
                    if not mask[tri].all():
                        continue
                    dist, w = _closest_on_triangle(target_points[t], *source_points[tri])
                    if best is None or dist < best[0]:
                        best = (dist, (int(tri[0]), int(tri[1]), int(tri[2])), w)
                if best is None:
                    tri = triangles[around[v][0]] if around[v] else (v, v, v)
                    corner = [float(int(x) == int(v)) for x in tri]
                    best = (0.0, tuple(int(x) for x in tri), tuple(corner))
                out[int(t)] = (best[1], best[2])
    return out
