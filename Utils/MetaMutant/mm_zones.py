"""
Where each vertex sits relative to the lip and eyelid lines, on your head and on the MetaHuman, so the
rig transfer can pair them by that instead of by closest point.

Closest point does not know which side of a lip a vertex is on: inside the mouth or in a fold under the brow
it jumps between surfaces, and then lips stay stuck across an open mouth and lids crumple. A line picked
around the mouth or an eye gives every vertex near it local coordinates:

* side: outside (the skin) or inside (the mouth, the eye socket). The closed line cuts the mesh in two;
* part: upper or lower, whichever line is nearer along the surface;
* along: how far along that line (for the lips, each side of the midline on its own);
* depth: how far from the line along the surface.

A vertex of your head takes the skin weights and blendshapes of the MetaHuman points with the same
coordinates. Away from the line the outside blends back into closest point, which is right on open skin.
The same zones say which faces belong to which lip for the wrap's region lock, so no region has to be picked.

Pure Python + numpy (no Maya), so it is tested on its own.
"""

from __future__ import annotations

import heapq
from typing import Dict, List, NamedTuple, Optional, Sequence, Tuple

import numpy as np

import mm_points as mp

UPPER, LOWER = 0, 1
#: how far from a line the zone reaches on the skin, as a share of the line's length
REACH = {"mouth": 0.35, "eye": 0.35}
#: the zone holds alone up to this share of its reach, then blends into closest point
HOLD = 0.5
NEIGHBOURS = 4
#: rounds of averaging each paired vertex with its neighbours, and how much it takes from them each round
SMOOTH_ROUNDS = 3
SMOOTH_AMOUNT = 0.5
#: source vertices kept per vertex after smoothing
MAX_SOURCES = 12


class Ring(NamedTuple):
    name: str  # "mouth" or "eye"
    upper: List[int]
    lower: List[int]
    midline: Optional[float]  # lips: X of the head's midline, so each side of it is matched on its own


class Zones(NamedTuple):
    inside: np.ndarray  # bool per vertex
    part: np.ndarray  # UPPER, LOWER or -1 where not reached
    along: np.ndarray  # -1..1 or 0..1 along the line
    depth: np.ndarray  # distance along the surface from the line
    length: float  # length of the line


def polygon_edges(counts: Sequence[int], connects: Sequence[int]) -> np.ndarray:
    """Unique edges (n, 2) of a mesh given as polygon vertex counts and connects."""
    out = set()
    at = 0
    for count in counts:
        face = connects[at:at + count]
        at += count
        for a, b in zip(face, list(face[1:]) + [face[0]]):
            out.add((int(a), int(b)) if a < b else (int(b), int(a)))
    return np.array(sorted(out), int).reshape(-1, 2)


def _neighbours(count: int, edges: np.ndarray) -> List[List[int]]:
    around: List[List[int]] = [[] for _ in range(count)]
    for a, b in edges:
        around[a].append(int(b))
        around[b].append(int(a))
    return around


def inside_of(ring_vertices: Sequence[int], around: List[List[int]], outside_seed: int) -> np.ndarray:
    """Vertices cut off from `outside_seed` by the closed line. All False when the line does not close."""
    count = len(around)
    wall = np.zeros(count, bool)
    wall[list(ring_vertices)] = True
    seen = np.zeros(count, bool)
    seen[outside_seed] = True
    stack = [outside_seed]
    while stack:
        for n in around[stack.pop()]:
            if not seen[n] and not wall[n]:
                seen[n] = True
                stack.append(n)
    # vertices no edge reaches (loose ones) are not "inside" either
    linked = np.array([bool(a) for a in around])
    return ~seen & ~wall & linked


def _spread(sources: Dict[int, Tuple[int, float]], allowed: np.ndarray, around, points, part, along, depth) -> None:
    """Dijkstra along the edges from the line vertices, carrying which line and where along it each vertex is nearest."""
    heap = []
    for v, (p, t) in sources.items():
        depth[v] = 0.0
        part[v], along[v] = p, t
        heap.append((0.0, v))
    heapq.heapify(heap)
    while heap:
        d, v = heapq.heappop(heap)
        if d > depth[v]:
            continue
        for n in around[v]:
            if not allowed[n]:
                continue
            nd = d + float(np.linalg.norm(points[v] - points[n]))
            if nd < depth[n]:
                depth[n] = nd
                part[n], along[n] = part[v], along[v]
                heapq.heappush(heap, (nd, n))


def zones(points, edges: np.ndarray, ring: Ring, outside_seed: Optional[int] = None) -> Zones:
    """The coordinates of every vertex against one closed line (the upper and lower line of a mouth or an eye)."""
    points = np.asarray(points, float)
    count = len(points)
    around = _neighbours(count, edges)
    seed = int(np.argmax(points[:, 1])) if outside_seed is None else outside_seed
    wall = sorted(set(ring.upper) | set(ring.lower))
    inside = inside_of(wall, around, seed)
    sources: Dict[int, Tuple[int, float]] = {}
    for p, chain in ((LOWER, ring.lower), (UPPER, ring.upper)):  # a corner on both lines counts as upper
        params = mp.arc_params(points[chain], ring.midline)
        for v, t in zip(chain, params):
            sources[v] = (p, float(t))
    part = np.full(count, -1, int)
    along = np.zeros(count)
    depth = np.full(count, np.inf)
    is_wall = np.zeros(count, bool)
    is_wall[wall] = True
    for side in (inside, ~inside & ~is_wall):
        partial_part, partial_along, partial_depth = part.copy(), along.copy(), depth.copy()
        _spread(sources, side | is_wall, around, points, partial_part, partial_along, partial_depth)
        part[side], along[side], depth[side] = partial_part[side], partial_along[side], partial_depth[side]
    for v, (p, t) in sources.items():
        part[v], along[v], depth[v] = p, t, 0.0
    # the walk only knows the nearest vertex of the line, and a line of few vertices would leave whole columns of
    # the head at one place along it: each vertex takes the nearest point of the segments there instead
    for p, chain in ((UPPER, ring.upper), (LOWER, ring.lower)):
        params = mp.arc_params(points[chain], ring.midline)
        reached = np.flatnonzero((part == p) & (depth > 0) & np.isfinite(depth))
        along[reached] = _along_segments(points[reached], points[chain], params, along[reached])
    length = max(float(np.linalg.norm(np.diff(points[ring.upper], axis=0), axis=1).sum()),
                 float(np.linalg.norm(np.diff(points[ring.lower], axis=0), axis=1).sum()))
    return Zones(inside, part, along, depth, length)


def _along_segments(query: np.ndarray, line: np.ndarray, params: np.ndarray, near: np.ndarray) -> np.ndarray:
    """The parameter of the nearest point of the line's segments, for points whose nearest line vertex is at parameter `near`."""
    out = near.copy()
    for row, (p, t) in enumerate(zip(query, near)):
        i = int(np.clip(np.searchsorted(params, t), 0, len(params) - 1))
        best = np.inf
        for a in (i - 1, i):
            if a < 0 or a + 1 >= len(line):
                continue
            seg = line[a + 1] - line[a]
            length = float(seg @ seg)
            u = 0.0 if length <= 0 else float(np.clip((p - line[a]) @ seg / length, 0.0, 1.0))
            dist = float(((line[a] + seg * u - p) ** 2).sum())
            if dist < best:
                best = dist
                out[row] = params[a] + (params[a + 1] - params[a]) * u
    return out


def smooth_pairs(paired: Dict[int, Dict[int, float]], around: List[List[int]], fixed: np.ndarray,
                 rounds: int = SMOOTH_ROUNDS, amount: float = SMOOTH_AMOUNT, keep: int = MAX_SOURCES) -> Dict[int, Dict[int, float]]:
    """Each paired vertex takes part of its neighbours' sources: a step between neighbours in the MetaHuman's motion
    would show as a crease on a head of coarser wires. `fixed` vertices (the lines themselves) stay as they are."""
    current = paired
    for _ in range(rounds):
        following: Dict[int, Dict[int, float]] = {}
        for v, own in current.items():
            if fixed[v]:
                following[v] = own
                continue
            others = [current[n] for n in around[v] if n in current]
            if not others:
                following[v] = own
                continue
            mixed: Dict[int, float] = {s: w * (1.0 - amount) for s, w in own.items()}
            share = amount / len(others)
            for other in others:
                for s, w in other.items():
                    mixed[s] = mixed.get(s, 0.0) + w * share
            if len(mixed) > keep:
                mixed = dict(sorted(mixed.items(), key=lambda item: -item[1])[:keep])
            total = sum(mixed.values())
            following[v] = {s: w / total for s, w in mixed.items()}
        current = following
    return current


def blend(depth: np.ndarray, reach: float, hold: float = HOLD) -> np.ndarray:
    """Share of closest point in the mix, by distance from the line: 0 near it, 1 at the reach, smooth in between."""
    u = np.clip((depth - hold * reach) / max((1 - hold) * reach, 1e-9), 0.0, 1.0)
    return u * u * (3 - 2 * u)


def _nearest(query: np.ndarray, pool: np.ndarray, k: int = NEIGHBOURS) -> Tuple[np.ndarray, np.ndarray]:
    """The k nearest of `pool` for each query point, with inverse distance weights summing to 1 (an exact hit takes all)."""
    k = min(k, len(pool))
    ids = np.zeros((len(query), k), int)
    weights = np.zeros((len(query), k))
    for start in range(0, len(query), 512):
        q = query[start:start + 512]
        dist = ((q[:, None] - pool[None]) ** 2).sum(2)
        order = np.argpartition(dist, k - 1, axis=1)[:, :k] if k < len(pool) else np.tile(np.arange(len(pool)), (len(q), 1))
        near = np.take_along_axis(dist, order, axis=1)
        w = 1.0 / np.maximum(near, 1e-10)
        ids[start:start + len(q)] = order
        weights[start:start + len(q)] = w / w.sum(1, keepdims=True)
    return ids, weights


def pair(target: Zones, source: Zones, reach: float) -> Dict[int, Tuple[List[int], List[float], float]]:
    """
    target vertex -> (source vertices, their weights, share of closest point to mix in), for each vertex this line
    reaches. Outside: within `reach` of the line, by absolute distance. Inside: all of it, its depth measured
    from the line to the deepest point, so the bottoms of two mouths meet.
    """
    out: Dict[int, Tuple[List[int], List[float], float]] = {}
    half = source.length / 2.0 if (source.along < 0).any() else source.length
    for side_inside in (False, True):
        for part_id in (UPPER, LOWER):
            t_ids = np.flatnonzero((target.inside == side_inside) & (target.part == part_id) & np.isfinite(target.depth))
            s_ids = np.flatnonzero(((source.inside == side_inside) | (source.depth == 0)) & (source.part == part_id) & np.isfinite(source.depth))
            if not side_inside:
                t_ids = t_ids[target.depth[t_ids] < reach]
                s_ids = s_ids[source.depth[s_ids] < reach * 1.5]
            if not len(t_ids) or not len(s_ids):
                continue
            t_depth, s_depth = target.depth[t_ids], source.depth[s_ids]
            if side_inside:
                t_max, s_max = t_depth.max(), s_depth.max()
                t_depth = t_depth / max(t_max, 1e-9) * s_max
            query = np.c_[target.along[t_ids] * half, t_depth]
            pool = np.c_[source.along[s_ids] * half, s_depth]
            ids, weights = _nearest(query, pool)
            mix = np.zeros(len(t_ids)) if side_inside else blend(target.depth[t_ids], reach)
            for row, t in enumerate(t_ids):
                out[int(t)] = ([int(v) for v in s_ids[ids[row]]], [float(w) for w in weights[row]], float(mix[row]))
    return out


def rings_of(points: dict, target_points, source_points) -> List[Tuple[Ring, Ring]]:
    """(your ring, MetaHuman ring) for each closed line picked: mouth, left eye, right eye."""
    lines = points.get("lines", {})
    target_points = np.asarray(target_points, float)
    source_points = np.asarray(source_points, float)
    out = []
    by_label = {g[0]: g[1] for g in mp.GUIDES}
    source_mid = float(np.median(source_points[[by_label[k] for k in ("Nasion", "Nose tip", "Chin")], 0]))
    guide_x = [target_points[g["vertex"], 0] for label, g in points.get("guides", {}).items() if not label.endswith((" L", " R"))]
    target_mid = float(np.median(guide_x)) if guide_x else float((target_points[:, 0].min() + target_points[:, 0].max()) / 2)
    for up, low in mp.LINE_PAIRS:
        if up in lines and low in lines:
            lip = up in mp.LIP_LINES
            name = "mouth" if lip else "eye"
            # a corner of your mouth moves like the corner of the MetaHuman's opening, not like the end of its crease
            # (there its upper and lower lip are one line, and yours would stay stuck together that far)
            mh_up, mh_low = mp.opening_of(mp.METAHUMAN_LINES[up], mp.METAHUMAN_LINES[low])
            out.append((Ring(name, list(lines[up]["vertices"]), list(lines[low]["vertices"]), target_mid if lip else None),
                        Ring(name, mh_up, mh_low, source_mid if lip else None)))
    return out


def correspondence(points: dict, target_points, target_edges: np.ndarray, source_points, source_edges: np.ndarray,
                   base: Sequence[Tuple[Sequence[int], Sequence[float]]], log=print) -> List[Tuple[Tuple[int, ...], Tuple[float, ...]]]:
    """
    `base` (for each target vertex, source vertices and weights: closest point or regions) with the lines applied
    on top. Both meshes in the same space and at rest. A vertex two lines reach goes with the nearer one.
    """
    target_points = np.asarray(target_points, float)
    source_points = np.asarray(source_points, float)
    out = [(tuple(ids), tuple(w)) for ids, w in base]
    nearest = np.full(len(target_points), np.inf)
    counts = []
    joined_all: Dict[int, Dict[int, float]] = {}
    fixed = np.zeros(len(target_points), bool)
    for mine, theirs in rings_of(points, target_points, source_points):
        target = zones(target_points, target_edges, mine)
        source = zones(source_points, source_edges, theirs)
        reach = REACH[mine.name] * source.length
        paired = pair(target, source, reach)
        for t, (ids, weights, mix) in paired.items():
            d = target.depth[t]
            if d >= nearest[t]:
                continue
            nearest[t] = d
            joined: Dict[int, float] = {}
            for v, w in zip(ids, weights):
                joined[v] = joined.get(v, 0.0) + w * (1.0 - mix)
            if mix > 0:
                for v, w in zip(*base[t]):
                    joined[int(v)] = joined.get(int(v), 0.0) + float(w) * mix
            joined_all[t] = joined
        fixed[list(mine.upper) + list(mine.lower)] = True
        counts.append(f"{mine.name}: {len(paired)} of yours ({int(target.inside.sum())} inside)")
    if joined_all:
        around = _neighbours(len(target_points), target_edges)
        for t, joined in smooth_pairs(joined_all, around, fixed).items():
            out[t] = (tuple(joined), tuple(joined.values()))
    if counts:
        log("lines: " + ", ".join(counts))
    return out


def lock_regions(points: dict, head_points, head_edges: np.ndarray, base_points, base_edges: np.ndarray) -> Tuple[Dict[str, List[int]], Dict[str, List[int]]]:
    """The wrap's regions as the lines give them: (MetaHuman vertices, your vertices) per mm_regions name."""
    head_points = np.asarray(head_points, float)
    base_points = np.asarray(base_points, float)
    base: Dict[str, List[int]] = {}
    head: Dict[str, List[int]] = {}
    for mine, theirs in rings_of(points, head_points, base_points):
        for pts, edges, ring, store in ((head_points, head_edges, mine, head), (base_points, base_edges, theirs, base)):
            z = zones(pts, edges, ring)
            reach = REACH[ring.name] * z.length
            close = z.depth < reach
            if ring.name == "mouth":
                # the deep part of the mouth belongs to no lip
                store.setdefault("upper_lip", []).extend(np.flatnonzero(close & (z.part == UPPER)).tolist())
                store.setdefault("lower_lip", []).extend(np.flatnonzero(close & (z.part == LOWER)).tolist())
                store.setdefault("mouth_bag", []).extend(np.flatnonzero(z.inside & ~close).tolist())
            else:
                outside = ~z.inside
                store.setdefault("upper_eyelid", []).extend(np.flatnonzero(close & outside & (z.part == UPPER)).tolist())
                store.setdefault("lower_eyelid", []).extend(np.flatnonzero(close & outside & (z.part == LOWER)).tolist())
    return base, head
