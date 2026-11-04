"""
Corrections the transfer alone cannot make, because they depend on your head's own proportions.

close_eyelids: the rig moves your lids by what it moves the MetaHuman's. When your eye opens wider, or sits
differently on the eyeball, the same motion leaves a gap at full blink, and the lid can sink into the eye at its
corners. It measures that in the blink pose and stores what is missing as one more blendShape target, driven by the
MetaHuman's own blink weight, so it grows with the blink and is nothing at rest.

place_teeth: teeth modelled close behind the lips come through them as soon as the lips press back against the teeth.
It moves the rigged copy of your teeth back, both arches by the same amount so the bite stays, as little as keeps
them behind the skin seen from the front, across the mouth's poses.

fit_teeth: teeth wider than the face around them come through the cheeks when the jaw opens (the wrapped MetaHuman
does the same). What moving them back left over, it narrows, as little as stops that in those poses. Your own teeth
mesh is not touched by either.

Need the rig and the face board in the scene (mm_rig, mm_faceboard), and the lines picked (mm_points).
The math (delta_along_lines, lid_gaps, out_of_sphere, narrowed, height_map, in_front_of_skin, back_needed) needs no Maya.
"""

from __future__ import annotations

from typing import Callable, Dict, List, Sequence, Tuple

import numpy as np

import mm_points as mp
import mm_zones

#: how far from the lid line the correction fades out, as a share of the line's length
LID_REACH = 0.3
#: of what is missing at full blink, the share the upper lid takes (the MetaHuman's upper lid does nearly all the travel)
UPPER_SHARE = 0.85
ITERATIONS = 3
TARGET = "mmFix_lidClose_{}"
#: the lid stays this far outside the eyeball, as a share of the lid line's length
EYE_MARGIN = 0.006
#: at full blink the upper lid rides over the lower by this share of the line's length, so no eye shows from below
#: or from the side; nothing at the corners, where the two lines are one vertex
LID_OVERLAP = 0.02
#: the rigged teeth are not narrowed below this share of their size
TEETH_MIN_SCALE = 0.75
TEETH_SAMPLE = 5  # every how many teeth vertices are checked against the skin
#: poses checked for the teeth: controls set to 1 together
TEETH_POSES = (("CTRL_C_jaw.translateY",),
               ("CTRL_L_mouth_cornerPull.translateY", "CTRL_R_mouth_cornerPull.translateY"),
               ("CTRL_C_jaw.translateY", "CTRL_L_mouth_cornerPull.translateY", "CTRL_R_mouth_cornerPull.translateY"))


#: poses the teeth must stay behind the skin in, as what is set on the board: both sides of each stem, and the jaw
TEETH_PLACE_POSES = (
    (0.0, {}), (1.0, {}), (0.6, {"mouth_cornerPull": 1.0}), (0.0, {"mouth_cornerPull": 1.0}),
    (0.15, {"mouth_cornerPull": 0.85, "mouth_upperLipRaise": 0.25, "mouth_lowerLipDepress": 0.3}), (0.0, {"mouth_sharpCornerPull": 1.0}),
    (0.0, {"mouth_stretch": 1.0}), (0.9, {"mouth_stretch": 0.7, "mouth_upperLipRaise": 0.8, "mouth_lowerLipDepress": 0.8}),
    (0.0, {"mouth_upperLipRaise": 1.0, "mouth_lowerLipDepress": 1.0}), (0.1, {"mouth_lipBiteD": 0.85, "mouth_upperLipRaise": 0.3}),
    (0.0, {"mouth_funnelU": 1.0, "mouth_funnelD": 1.0}), (0.0, {"mouth_purseU": 1.0, "mouth_purseD": 1.0}),
    (0.0, {"mouth_towardsU": 1.0, "mouth_towardsD": 1.0}), (0.0, {"mouth_lipsPressU": 1.0, "mouth_lipsPressD": 1.0}),
    (0.0, {"mouth_cornerDepress": 1.0}), (0.0, {"mouth_tightenU": 1.0, "mouth_tightenD": 1.0}),
)
#: space kept between the teeth and the skin, and the most they move back, as shares of the teeth's width and depth
TEETH_MARGIN = 0.02
TEETH_MAX_BACK = 0.25
#: the size of a cell of the height maps, as a share of the teeth's width
HEIGHT_CELL = 0.01


def falloff(depth: np.ndarray, reach: float) -> np.ndarray:
    """1 on the line, 0 at the reach, smooth."""
    u = np.clip(1.0 - np.asarray(depth, float) / max(reach, 1e-9), 0.0, 1.0)
    return u * u * (3 - 2 * u)


def sample(points: np.ndarray, params: np.ndarray, at: np.ndarray) -> np.ndarray:
    """A polyline's points at parameters `at`, each coordinate interpolated."""
    return np.stack([np.interp(at, params, points[:, k]) for k in range(3)], axis=1)


def overlap_along(t: np.ndarray, size: float, down: np.ndarray) -> np.ndarray:
    """How far past the lower line the upper one goes at each parameter: full in the middle, nothing at the corners."""
    return np.sqrt(np.sin(np.clip(t, 0.0, 1.0) * np.pi))[:, None] * size * np.asarray(down, float)[None, :]


def lid_gaps(pose: np.ndarray, upper: Sequence[int], lower: Sequence[int], offset_of: Callable[[np.ndarray], np.ndarray]) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """For each vertex of the upper line and of the lower line: what separates it from the other line, beyond
    `offset_of(t)`, the separation the lines should keep at parameter t. Returns (t upper, gap upper, t lower, gap lower);
    a gap points from the upper line toward where it should be, for both lines."""
    up, low = pose[list(upper)], pose[list(lower)]
    t_up, t_low = mp.arc_params(up), mp.arc_params(low)
    gap_up = sample(low, t_low, t_up) + offset_of(t_up) - up
    gap_low = low + offset_of(t_low) - sample(up, t_up, t_low)
    return t_up, gap_up, t_low, gap_low


def delta_along_lines(zones: mm_zones.Zones, ids: np.ndarray, reach: float, t_up, gap_up, t_low, gap_low, upper_share: float = UPPER_SHARE) -> np.ndarray:
    """The move of each vertex `ids`: what its line needs at its place along the line, fading with distance."""
    fade = falloff(zones.depth[ids], reach)[:, None]
    out = np.zeros((len(ids), 3))
    upper = zones.part[ids] == mm_zones.UPPER
    out[upper] = sample(gap_up, t_up, zones.along[ids[upper]]) * upper_share
    out[~upper] = sample(gap_low, t_low, zones.along[ids[~upper]]) * -(1.0 - upper_share)
    return out * fade


def out_of_sphere(pose: np.ndarray, centre: Sequence[float], radius: float) -> np.ndarray:
    """The move that takes each point out to the sphere; nothing for points already outside it."""
    away = pose - np.asarray(centre, float)
    dist = np.linalg.norm(away, axis=1, keepdims=True)
    short = np.maximum(radius - dist, 0.0)
    return away / np.maximum(dist, 1e-9) * short


def narrowed(points: np.ndarray, scale: float) -> np.ndarray:
    """Teeth narrower by `scale`, across (X) and front to back (Z), about the middle of their back: the back stays
    where the jaw hinges, the front comes in from the lips."""
    points = np.asarray(points, float)
    out = points.copy()
    middle = (points[:, 0].min() + points[:, 0].max()) / 2
    back = points[:, 2].min()
    out[:, 0] = middle + (points[:, 0] - middle) * scale
    out[:, 2] = back + (points[:, 2] - back) * scale
    return out


class HeightMap:
    """The nearest surface seen from the front (+Z) at each (x, y) of a grid; -inf where there is none."""

    def __init__(self, triangles: np.ndarray, low: Sequence[float], high: Sequence[float], cell: float):
        self.x0, self.y0, self.cell = float(low[0]), float(low[1]), float(cell)
        xs = np.arange(low[0], high[0] + cell, cell)
        ys = np.arange(low[1], high[1] + cell, cell)
        self.z = np.full((len(ys), len(xs)), -np.inf)
        for a, b, c in np.asarray(triangles, float):
            area = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
            if abs(area) < 1e-12:
                continue
            lo, hi = np.minimum(np.minimum(a, b), c), np.maximum(np.maximum(a, b), c)
            i0, i1 = np.searchsorted(xs, lo[0]), np.searchsorted(xs, hi[0], "right")
            j0, j1 = np.searchsorted(ys, lo[1]), np.searchsorted(ys, hi[1], "right")
            if i0 >= i1 or j0 >= j1:
                continue
            X, Y = np.meshgrid(xs[i0:i1], ys[j0:j1])
            w0 = ((b[0] - X) * (c[1] - Y) - (b[1] - Y) * (c[0] - X)) / area
            w1 = ((c[0] - X) * (a[1] - Y) - (c[1] - Y) * (a[0] - X)) / area
            w2 = 1.0 - w0 - w1
            inside = (w0 >= 0) & (w1 >= 0) & (w2 >= 0)
            part = self.z[j0:j1, i0:i1]
            part[inside] = np.maximum(part[inside], (w0 * a[2] + w1 * b[2] + w2 * c[2])[inside])

    def at(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        rows, cols = self.z.shape
        i = np.round((np.asarray(x) - self.x0) / self.cell).astype(int)
        j = np.round((np.asarray(y) - self.y0) / self.cell).astype(int)
        out = np.full(len(i), -np.inf)
        ok = (i >= 0) & (i < cols) & (j >= 0) & (j < rows)
        out[ok] = self.z[j[ok], i[ok]]
        return out


def rigid_move(rest: np.ndarray, pose: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """(R, a, b) of the rigid move from `rest` to `pose`: a point p goes to (p - a) R^T + b."""
    a, b = rest.mean(0), pose.mean(0)
    u, _, vt = np.linalg.svd((rest - a).T @ (pose - b))
    flip = np.sign(np.linalg.det(vt.T @ u.T))
    return vt.T @ np.diag([1.0, 1.0, flip]) @ u.T, a, b


def in_front_of_skin(points: np.ndarray, moves: Sequence[Tuple[tuple, HeightMap]]) -> float:
    """How far `points` (at rest) come in front of the skin, worst of all poses; negative: the space left behind it.
    Each pose gives the rigid move of these points and the height map of the skin. No skin in front of a point is the
    mouth's opening: that point may show."""
    worst = -np.inf
    for (R, a, b), skin in moves:
        q = (points - a) @ R.T + b
        z = skin.at(q[:, 0], q[:, 1])
        seen = np.isfinite(z)
        if seen.any():
            worst = max(worst, float((q[seen, 2] - z[seen]).max()))
    return worst


def back_needed(parts: Sequence[Tuple[np.ndarray, Sequence[Tuple[tuple, HeightMap]]]], margin: float, limit: float) -> float:
    """How far back (-Z) all the `parts` (points at rest, their moves) must go to stay `margin` behind the skin in every
    pose, up to `limit`."""
    def worst(back: float) -> float:
        shift = np.array([0.0, 0.0, back])
        return max(in_front_of_skin(p - shift, moves) for p, moves in parts)

    if worst(0.0) <= -margin:
        return 0.0
    if worst(limit) > -margin:
        return limit
    low, high = 0.0, limit
    for _ in range(12):
        mid = (low + high) / 2
        if worst(mid) > -margin:
            low = mid
        else:
            high = mid
    return high


# ----------------------------------------------------------------------------- Maya


def _world(mesh: str) -> np.ndarray:
    import maya.api.OpenMaya as om  # type: ignore

    sel = om.MSelectionList()
    sel.add(mesh)
    return np.array([(p.x, p.y, p.z) for p in om.MFnMesh(sel.getDagPath(0)).getPoints(om.MSpace.kWorld)])


def _blend_shape_of(mesh: str) -> str:
    import maya.cmds as cmds  # type: ignore

    found = [n for n in cmds.listHistory(mesh, pruneDagObjects=True) or [] if cmds.nodeType(n) == "blendShape"]
    own = [n for n in found if n.startswith(mesh.split("|")[-1])]
    return (own or found)[0]


def _add_target(bs: str, alias: str) -> int:
    """A new empty target on `bs`, under its name; an earlier one of that name is reused. Returns its index."""
    import maya.cmds as cmds  # type: ignore

    names = cmds.aliasAttr(bs, query=True) or []
    used = {}
    for name, plug in zip(names[0::2], names[1::2]):
        if plug.startswith("weight["):
            used[name] = int(plug[7:-1])
    if alias in used:
        return used[alias]
    index = max(used.values(), default=-1) + 1
    cmds.setAttr(f"{bs}.weight[{index}]", 0.0)
    cmds.aliasAttr(alias, f"{bs}.weight[{index}]")
    return index


def _write_target(bs: str, index: int, ids: np.ndarray, deltas: np.ndarray) -> None:
    import maya.cmds as cmds  # type: ignore

    item = f"{bs}.inputTarget[0].inputTargetGroup[{index}].inputTargetItem[6000]"
    cmds.setAttr(item + ".inputPointsTarget", len(ids), *[(float(x), float(y), float(z), 1.0) for x, y, z in deltas], type="pointArray")
    cmds.setAttr(item + ".inputComponentsTarget", len(ids), *[f"vtx[{int(i)}]" for i in ids], type="componentList")


def _push_out_of_meshes(pose: np.ndarray, meshes: Sequence[str], margin: float) -> np.ndarray:
    """The move that takes each point out of the closed meshes, along their surface normal; nothing for points already out."""
    import maya.api.OpenMaya as om  # type: ignore

    out = np.zeros_like(pose)
    for mesh in meshes:
        sel = om.MSelectionList()
        sel.add(mesh)
        fn = om.MFnMesh(sel.getDagPath(0))
        for row, (x, y, z) in enumerate(pose):
            p = om.MPoint(x, y, z)
            q, n, _ = fn.getClosestPointAndNormal(p, om.MSpace.kWorld)
            depth = om.MVector(p - q) * n
            if depth < margin:
                # the deeper of the meshes wins: an eye and its cornea overlap
                need = margin - depth
                if need > np.linalg.norm(out[row]):
                    out[row] = (n.x * need, n.y * need, n.z * need)
    return out


def close_eyelids(head: str, source: str, points: dict, root: str, eyes: Sequence[Tuple[Sequence[float], float]] = (),
                  eye_meshes: Sequence[str] = (), log: Callable[[str], None] = print) -> Dict[str, Tuple[float, float]]:
    """One blendShape target per eye that closes the lids of `head` at full blink as far as those of `source` close.
    The lids must stay out of your eyes: `eye_meshes` (the rigged copies), or `eyes`, (centre, radius) of each, when
    the eyes are part of the head's own mesh. Returns side -> (mean gap before, after), in scene units along Y."""
    import maya.cmds as cmds  # type: ignore
    import mm_maya

    lines = points.get("lines", {})
    rest = _world(head)
    edges = mm_maya.mesh_edges(head)
    bs = _blend_shape_of(head)
    source_bs = _blend_shape_of(source)
    # the blendShape comes before the skin, in the rig's own space: the rig's scale and turn are taken out
    world_to_rig = np.linalg.inv(np.array(cmds.xform(root, query=True, worldSpace=True, matrix=True)).reshape(4, 4)[:3, :3])
    report: Dict[str, Tuple[float, float]] = {}
    for side in "LR":
        up_key, low_key = f"upper_lid_{side}", f"lower_lid_{side}"
        control = f"CTRL_{side}_eye_blink.translateY"
        driver = f"{source_bs}.eye_blink_{side}"
        if up_key not in lines or low_key not in lines or not cmds.objExists(control) or not cmds.objExists(driver):
            continue
        up, low = lines[up_key]["vertices"], lines[low_key]["vertices"]
        zones = mm_zones.zones(rest, edges, mm_zones.Ring("eye", list(up), list(low), None))
        reach = LID_REACH * zones.length
        ids = np.flatnonzero(zones.depth < reach)
        overlap = LID_OVERLAP * zones.length
        down = rest[low].mean(0) - rest[up].mean(0)
        down = down / max(float(np.linalg.norm(down)), 1e-9)
        index = _add_target(bs, TARGET.format(side))
        plug = f"{bs}.weight[{index}]"
        for connection in cmds.listConnections(plug, source=True, destination=False, plugs=True) or []:
            cmds.disconnectAttr(connection, plug)
        total = np.zeros((len(ids), 3))
        _write_target(bs, index, ids, total)
        cmds.setAttr(plug, 1.0)
        cmds.setAttr(control, 1.0)
        mh_up, mh_low = mp.METAHUMAN_LINES[up_key], mp.METAHUMAN_LINES[low_key]
        before = after = 0.0
        try:
            for step in range(ITERATIONS + 1):
                cmds.refresh(force=True)
                pose, mh = _world(head), _world(source)
                mh_t_up, mh_t_low = mp.arc_params(mh[mh_up]), mp.arc_params(mh[mh_low])
                offset = lambda t: sample(mh[mh_up], mh_t_up, t) - sample(mh[mh_low], mh_t_low, t) + overlap_along(t, overlap, down)  # noqa: E731
                t_up, gap_up, t_low, gap_low = lid_gaps(pose, up, low, offset)
                size = float(np.abs(gap_up[:, 1]).mean())
                if step == 0:
                    before = size
                after = size
                if step == ITERATIONS:
                    break
                move = delta_along_lines(zones, ids, reach, t_up, gap_up, t_low, gap_low)
                # the outside rows of the lid, after this step's move; the inside of the socket lies behind the eye anyway
                moved = pose[ids] + move
                margin = EYE_MARGIN * zones.length
                if eye_meshes:
                    outer = np.flatnonzero(~zones.inside[ids])
                    push = np.zeros_like(moved)
                    push[outer] = _push_out_of_meshes(moved[outer], eye_meshes, margin)
                    move = move + push
                elif eyes:
                    centre, radius = min(eyes, key=lambda e: float(((np.asarray(e[0]) - rest[up]) ** 2).sum()))
                    move = move + out_of_sphere(moved, centre, radius + margin) * (~zones.inside[ids])[:, None]
                total += move @ world_to_rig.T
                _write_target(bs, index, ids, total)
        finally:
            cmds.setAttr(control, 0.0)
        cmds.setAttr(plug, 0.0)
        cmds.connectAttr(driver, plug, force=True)
        report[side] = (before, after)
        log(f"{head}: lids of the {side} eye close by {before:.3f} more at full blink (left over {after:.3f}), {len(ids)} vertices")
    cmds.refresh(force=True)
    return report


def _outer_faces(head: str, points: dict) -> np.ndarray:
    """Per face of `head`: on the outer skin, not inside the mouth or an eye (nothing there can show teeth through)."""
    import maya.api.OpenMaya as om  # type: ignore
    import mm_maya

    rest = _world(head)
    edges = mm_maya.mesh_edges(head)
    lines = points["lines"]
    inside = np.zeros(len(rest), bool)
    for up, low in mp.LINE_PAIRS:
        if up in lines and low in lines:
            inside |= mm_zones.zones(rest, edges, mm_zones.Ring("mouth", list(lines[up]["vertices"]), list(lines[low]["vertices"]), None)).inside
    sel = om.MSelectionList()
    sel.add(head)
    counts, connects = om.MFnMesh(sel.getDagPath(0)).getVertices()
    out = []
    at = 0
    for count in counts:
        out.append(not inside[list(connects[at:at + count])].any())
        at += count
    return np.array(out)


def _through_skin(head: str, teeth: Sequence[str], outer: np.ndarray) -> float:
    """How far the teeth come out of the outer skin of `head`, in scene units, in the pose as it is."""
    import maya.api.OpenMaya as om  # type: ignore

    sel = om.MSelectionList()
    sel.add(head)
    fn = om.MFnMesh(sel.getDagPath(0))
    deepest = 0.0
    for mesh in teeth:
        for x, y, z in _world(mesh)[::TEETH_SAMPLE]:
            p = om.MPoint(x, y, z)
            q, n, face = fn.getClosestPointAndNormal(p, om.MSpace.kWorld)
            if outer[face]:
                deepest = max(deepest, om.MVector(p - q) * n)
    return deepest


def _set_rest(mesh: str, points: np.ndarray) -> None:
    """The rest shape of a skinned mesh: its intermediate (Orig) shape, in its own space."""
    import maya.api.OpenMaya as om  # type: ignore
    import maya.cmds as cmds  # type: ignore

    orig = [s for s in cmds.listRelatives(mesh, shapes=True, fullPath=True) or [] if cmds.getAttr(s + ".intermediateObject")]
    sel = om.MSelectionList()
    sel.add(orig[0])
    om.MFnMesh(sel.getDagPath(0)).setPoints(om.MPointArray([om.MPoint(*p) for p in points]), om.MSpace.kObject)


def _rest(mesh: str) -> np.ndarray:
    import maya.api.OpenMaya as om  # type: ignore
    import maya.cmds as cmds  # type: ignore

    orig = [s for s in cmds.listRelatives(mesh, shapes=True, fullPath=True) or [] if cmds.getAttr(s + ".intermediateObject")]
    sel = om.MSelectionList()
    sel.add(orig[0])
    return np.array([(p.x, p.y, p.z) for p in om.MFnMesh(sel.getDagPath(0)).getPoints(om.MSpace.kObject)])


def place_teeth(head: str, arches: Dict[str, Tuple[Sequence[int], Sequence[int]]], points: dict, root: str, log: Callable[[str], None] = print) -> float:
    """Move the rigged teeth (mesh -> upper ids, lower ids) back as little as keeps them behind the skin of `head` in
    TEETH_PLACE_POSES. Returns how far, in scene units."""
    import maya.api.OpenMaya as om  # type: ignore
    import maya.cmds as cmds  # type: ignore

    arches = {m: a for m, a in arches.items() if cmds.objExists(m)}
    if not arches:
        return 0.0
    # in the rig's own space, where the head faces +Z, whatever the scene's alignment
    inverse = np.linalg.inv(np.array(cmds.xform(root, query=True, worldSpace=True, matrix=True)).reshape(4, 4))
    to_rig = lambda p: (np.c_[p, np.ones(len(p))] @ inverse)[:, :3]  # noqa: E731
    rest = {m: to_rig(_world(m)) for m in arches}
    every = np.concatenate(list(rest.values()))
    width, depth = float(np.ptp(every[:, 0])), float(np.ptp(every[:, 2]))
    low, high = every.min(0) - width * 0.2, every.max(0) + width * 0.2
    sel = om.MSelectionList()
    sel.add(head)
    fn = om.MFnMesh(sel.getDagPath(0))
    counts, connects = fn.getTriangles()
    triangles = np.array(connects).reshape(-1, 3)
    triangles = triangles[_outer_faces(head, points)[np.repeat(np.arange(len(counts)), np.array(counts))]]
    skin_rest = to_rig(_world(head))[triangles]
    near = (skin_rest[:, :, :2].max(1) > low[:2]).all(1) & (skin_rest[:, :, :2].min(1) < high[:2]).all(1) & (skin_rest.mean(1)[:, 2] > low[2])
    triangles = triangles[near]
    parts = [(rest[m][list(ids)], []) for m, (up, lo) in arches.items() for ids in (up, lo) if len(ids)]
    jaw = "CTRL_C_jaw.translateY"
    for opened, stems in TEETH_PLACE_POSES:
        plugs = {f"CTRL_{side}_{stem}.translateY": value for stem, value in stems.items() for side in "LR"}
        if opened:
            plugs[jaw] = opened
        # Epic's board drives some controls from their pair
        plugs = {plug: value for plug, value in plugs.items() if cmds.objExists(plug) and cmds.getAttr(plug, settable=True)}
        for plug, value in plugs.items():
            cmds.setAttr(plug, value)
        cmds.refresh(force=True)
        skin = HeightMap(to_rig(_world(head))[triangles], low, high, width * HEIGHT_CELL)
        at = 0
        for m, (up, lo) in arches.items():
            now = to_rig(_world(m))
            for ids in (up, lo):
                if len(ids):
                    parts[at][1].append((rigid_move(rest[m][list(ids)], now[list(ids)]), skin))
                    at += 1
        for plug in plugs:
            cmds.setAttr(plug, 0.0)
    cmds.refresh(force=True)
    limit = depth * TEETH_MAX_BACK
    back = back_needed(parts, width * TEETH_MARGIN, limit)
    scale = float(np.linalg.norm(np.linalg.inv(inverse)[0, :3]))
    if back > 0.0:
        for m in arches:
            q = _rest(m)
            q[:, 2] -= back
            _set_rest(m, q)
        cmds.refresh(force=True)
    left = max(in_front_of_skin(p - np.array([0.0, 0.0, back]), moves) for p, moves in parts)
    if back >= limit and left > 0.0:
        log(f"teeth moved back {back * scale:.2f}, the most allowed, and they still come through the skin by {left * scale:.2f}: they are too far forward or too big for these lips")
    elif back > 0.0:
        log(f"teeth moved back {back * scale:.2f} so the lips clear them in {len(TEETH_PLACE_POSES)} poses (same size, same bite). Your own teeth mesh is as it was")
    else:
        log("teeth stay behind the lips in the poses checked")
    return back * scale


def fit_teeth(head: str, teeth: Sequence[str], points: dict, log: Callable[[str], None] = print) -> float:
    """Narrow the rigged teeth meshes as little as keeps them inside the skin in TEETH_POSES. Returns the scale (1 = no change)."""
    import maya.cmds as cmds  # type: ignore

    teeth = [t for t in teeth if cmds.objExists(t)]
    if not teeth:
        return 1.0
    plugs = sorted({plug for pose in TEETH_POSES for plug in pose if cmds.objExists(plug)})
    outer = _outer_faces(head, points)
    rest = {t: _rest(t) for t in teeth}
    together = np.concatenate(list(rest.values()))
    middle = (together[:, 0].min() + together[:, 0].max()) / 2
    back = together[:, 2].min()

    def apply(scale: float) -> None:
        for t, p in rest.items():
            q = p.copy()
            q[:, 0] = middle + (p[:, 0] - middle) * scale
            q[:, 2] = back + (p[:, 2] - back) * scale
            _set_rest(t, q)

    def worst() -> float:
        out = 0.0
        for pose in TEETH_POSES:
            for plug in pose:
                if plug in plugs:
                    cmds.setAttr(plug, 1.0)
            cmds.refresh(force=True)
            out = max(out, _through_skin(head, teeth, outer))
            for plug in pose:
                if plug in plugs:
                    cmds.setAttr(plug, 0.0)
        cmds.refresh(force=True)
        return out

    start = worst()
    if start <= 0.0:
        log("teeth stay inside the skin in the poses checked")
        return 1.0
    low, high = TEETH_MIN_SCALE, 1.0
    apply(low)
    if worst() > 0.0:
        log(f"teeth come through the skin by {start:.2f}; even at {low:.2f} of their size they still do: narrowing them that far")
        return low
    for _ in range(6):
        scale = (low + high) / 2
        apply(scale)
        if worst() > 0.0:
            high = scale
        else:
            low = scale
    apply(low)
    cmds.refresh(force=True)
    log(f"teeth came through the skin by {start:.2f}: the rigged copy is now {low:.3f} of their size, and stays inside. Your own teeth mesh is as it was")
    return low
