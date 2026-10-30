"""
Meta Mutant face board: MetaHuman-style controls (CTRL_L_brow_down, CTRL_C_jaw, ...) that move the
rig's joints and blendshapes the way RigLogic does, built only from Maya's own nodes, so the scene
opens and works in any Maya 2026 (no plugin, no Epic files). The math is mm_face.py's:

    controls --animCurveUU (ranges)--> plusMinusAverage --clamp--> raw controls
    raw controls --multDoubleLinear (products)--> clamp --> correctives (PSD)
    raw + correctives --> blendShape weights on a hidden curve (one point per joint channel triple,
        one target per control holding its joint moves) --curveInfo--> joint translate / rotate / scale
    raw + correctives --> the MetaHuman blendShape weights (channel names)

The curve is the trick: its blendShape adds up ~800 controls' joint moves (the DNA's joint groups,
hundreds of thousands of weights) in one fast native node instead of one node per weight.
Rotations are stored in radians (Maya's internal angle unit), so curve points connect straight to
joint rotations. Scene unit: centimetres (as MetaHuman DNAs).

    import mm_faceboard
    mm_faceboard.build("head_custom.dna", head="Head_MH")
"""

from __future__ import annotations

import math
import os
from collections import defaultdict
from typing import Callable, Dict, List, Optional, Tuple

import numpy as np

import mm_dna
import mm_face
import mm_rig

BOARD = "metaMutant_faceBoard"
DRIVER = "metaMutant_faceDriver"
NETWORK = "metaMutant_faceNetwork"  # container set of the network nodes, so a rebuild removes them
REGIONS = ("brow", "eye", "eyelashes", "ear", "nose", "mouth", "jaw", "teeth", "tongue", "neck")
COLORS = {"L": 6, "R": 13, "C": 17}  # Maya index colours: blue, red, yellow


def _maya():
    import maya.cmds as cmds  # type: ignore

    return cmds


def region(control: str) -> str:
    """'CTRL_L_brow_down' -> 'brow'; unusual names (throat...) go with the neck."""
    parts = control.split("_")
    key = parts[2] if len(parts) > 2 else parts[-1]
    for name in REGIONS:
        if key.startswith(name):
            return name
    return "neck"


def side(control: str) -> str:
    parts = control.split("_")
    return parts[1] if len(parts) > 1 and parts[1] in ("L", "R", "C") else "C"


def gui_ranges(beh) -> Dict[int, Tuple[float, float]]:
    """(min, max) each GUI control can take, from its range table rows."""
    out: Dict[int, List[float]] = {}
    for i, lo, hi in zip(beh["gui_in"], beh["gui_from"], beh["gui_to"]):
        r = out.setdefault(int(i), [0.0, 0.0])
        r[0], r[1] = min(r[0], float(lo)), max(r[1], float(hi))
    return {i: (a, b) for i, (a, b) in out.items()}


# ----------------------------------------------------------------------------- the board


def _square(name: str, x0: float, x1: float, y0: float, y1: float) -> str:
    cmds = _maya()
    return cmds.curve(name=name, degree=1, point=[(x0, y0, 0), (x1, y0, 0), (x1, y1, 0), (x0, y1, 0), (x0, y0, 0)])


def _reference(node: str) -> str:
    """Drawn but not selectable (frames, labels): only the controls can be picked."""
    cmds = _maya()
    cmds.setAttr(node + ".overrideEnabled", 1)
    cmds.setAttr(node + ".overrideDisplayType", 2)
    return node


def _text(name: str, text: str, x: float, y: float, height: float, parent: str, centre: bool = True) -> str:
    """Curve text (Maya's own textCurves, history removed), `height` tall, centred at x (or starting at x)."""
    cmds = _maya()
    node = cmds.textCurves(name=name, font="Arial", text=text, constructionHistory=False)[0]
    bb = cmds.exactWorldBoundingBox(node)  # at the origin, unscaled: its own size
    node = cmds.parent(node, parent, relative=True)[0]
    k = height / max(1e-6, bb[4] - bb[1])
    cmds.setAttr(node + ".scale", k, k, k)
    width = (bb[3] - bb[0]) * k
    cmds.setAttr(node + ".translate", x - (width / 2 if centre else 0) - bb[0] * k, y - bb[1] * k, 0)
    return _reference(node)


def short_name(control: str) -> str:
    """'CTRL_L_mouth_cornerPull' -> 'cornerPull' (the side is where it sits on the face)."""
    parts = control.split("_")[2:] if control.count("_") >= 2 else [control]
    if len(parts) > 1 and any(parts[0].startswith(r) for r in REGIONS):
        parts = parts[1:]
    return "_".join(parts) or control


def _euler(deg: np.ndarray) -> np.ndarray:
    """Rotation matrices (column vectors) for Maya's xyz order: Rz @ Ry @ Rx, per row of degrees."""
    x, y, z = np.radians(deg).T
    cx, sx, cy, sy, cz, sz = np.cos(x), np.sin(x), np.cos(y), np.sin(y), np.cos(z), np.sin(z)
    one, zero = np.ones_like(x), np.zeros_like(x)
    rx = np.stack([one, zero, zero, zero, cx, -sx, zero, sx, cx], -1).reshape(-1, 3, 3)
    ry = np.stack([cy, zero, sy, zero, one, zero, -sy, zero, cy], -1).reshape(-1, 3, 3)
    rz = np.stack([cz, -sz, zero, sz, cz, zero, zero, zero, one], -1).reshape(-1, 3, 3)
    return rz @ ry @ rx


class _Skeleton:
    """Forward kinematics of the rig's joints (translate, jointOrient then rotate, as Maya joints)."""

    def __init__(self, r):
        data = mm_rig.joints(r)
        self.parents = [p for _, p, _, _ in data]
        self.orient = _euler(np.array([o for _, _, _, o in data], float))
        self.order: List[int] = []
        seen = set()

        def visit(j):
            if j in seen:
                return
            if self.parents[j] >= 0:
                visit(self.parents[j])
            seen.add(j)
            self.order.append(j)

        for j in range(len(data)):
            visit(j)

    def pose(self, values: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """World positions and rotations from mm_face.evaluate's joint values (translate, rotate delta)."""
        v = values.reshape(-1, 9)
        local = self.orient @ _euler(v[:, 3:6])
        pos, rot = np.zeros((len(v), 3)), np.zeros((len(v), 3, 3))
        for j in self.order:
            p = self.parents[j]
            if p < 0:
                pos[j], rot[j] = v[j, :3], local[j]
            else:
                pos[j], rot[j] = pos[p] + rot[p] @ v[j, :3], rot[p] @ local[j]
        return pos, rot


def directions(r, beh) -> Dict[int, bool]:
    """Which controls to draw flipped, so dragging a control moves the face the same way: down when
    its joints go down, towards the screen's right when they go to the character's left (+X)."""
    names = [str(n) for n in beh["gui_names"]]
    sk = _Skeleton(r)
    gui = np.zeros(len(names), np.float32)
    p0, r0 = sk.pose(mm_face.evaluate(beh, gui)[0])
    front = np.array([0.0, 0.0, 2.0])  # a point 2 cm in front of each joint shows its rotation
    probe0 = p0 + front
    flips: Dict[int, bool] = {}
    for i, (lo, hi) in gui_ranges(beh).items():
        value = hi if hi > 0 else lo
        if value == 0:
            continue
        gui[:] = 0
        gui[i] = value
        p, rot = sk.pose(mm_face.evaluate(beh, gui)[0])
        move = (p - p0) + (p + np.einsum("nij,njk,k->ni", rot, np.transpose(r0, (0, 2, 1)), front) - probe0)
        top = np.argsort(-np.linalg.norm(move, axis=1))[:8]
        s = move[top].sum(axis=0) * np.sign(value)  # the way the face moves as the value goes up
        k = 1 if names[i].endswith(".ty") else 0  # ty: up / down; tx: screen right = +X
        if abs(s[k]) >= 0.3 * np.linalg.norm(s) and s[k] < 0:
            flips[i] = True
    return flips


#: the board as a face, top to bottom: the regions of each row, listed from the middle outwards
FACE_ROWS = (("brow",), ("eye", "eyelashes", "ear"), ("nose",), ("mouth",), ("jaw", "teeth"), ("tongue",), ("neck",))


def build_board(beh, log: Callable[[str], None] = print, flips: Optional[Dict[int, bool]] = None) -> Dict[int, str]:
    """The controls laid out like a face (brows on top, eyes, nose, mouth, jaw, tongue, neck), the
    character's right on the left as seen from the front, left and right mirrored around the middle.
    Each control sits in a frame of its range with its name under it.
    Returns GUI control index -> plug ('CTRL_L_brow_down.ty')."""
    cmds = _maya()
    names = [str(n) for n in beh["gui_names"]]
    ranges = gui_ranges(beh)
    axes: Dict[str, Dict[str, int]] = defaultdict(dict)
    for i, n in enumerate(names):
        ctrl, axis = n.split(".")
        axes[ctrl][axis] = i

    def extent(ctrl: str, axis: str) -> Tuple[float, float]:
        lo, hi = ranges.get(axes[ctrl].get(axis, -1), (0.0, 0.0))
        return min(lo, -0.2), max(hi, 0.2)

    flips = flips or {}
    board = cmds.group(empty=True, world=True, name=BOARD)
    plugs: Dict[int, str] = {}
    label_h, gap, middle = 0.24, 0.35, 0.8

    def place(ctrl: str, sd: str, cx: float, top: float, parent: str):
        """One control: frame of its range centred at x = cx, its top at y = top. A flipped axis
        (see `directions`) mirrors the frame, so the control moves the way its joints do."""
        tx, ty = extent(ctrl, "tx"), extent(ctrl, "ty")
        fx = -1.0 if flips.get(axes[ctrl].get("tx", -1)) else 1.0
        fy = -1.0 if flips.get(axes[ctrl].get("ty", -1)) else 1.0
        frame = _reference(_square(ctrl + "_frame", tx[0], tx[1], ty[0], ty[1]))
        cmds.parent(frame, parent)
        cmds.setAttr(frame + ".scale", fx, fy, 1)
        cmds.setAttr(frame + ".translate", cx - fx * (tx[0] + tx[1]) / 2, top - (ty[1] if fy > 0 else -ty[0]), 0)
        _text(ctrl + "_label", short_name(ctrl), cx, top - (ty[1] - ty[0]) - label_h * 1.7, label_h, parent)
        c = cmds.circle(name=ctrl, normal=(0, 0, 1), radius=0.16, constructionHistory=False)[0]
        cmds.setAttr(c + ".overrideEnabled", 1)
        cmds.setAttr(c + ".overrideColor", COLORS.get(sd, 17))
        cmds.parent(c, frame, relative=True)
        for attr in ("tz", "rx", "ry", "rz", "sx", "sy", "sz", "v"):
            cmds.setAttr(f"{c}.{attr}", lock=True, keyable=False, channelBox=False)
        for axis in ("tx", "ty"):
            if axis in axes[ctrl]:
                lo, hi = ranges.get(axes[ctrl][axis], (0.0, 1.0))
                flag = {"tx": "translationX", "ty": "translationY"}[axis]
                cmds.transformLimits(c, **{flag: (lo, hi), "enable" + flag[0].upper() + flag[1:]: (True, True)})
                plugs[axes[ctrl][axis]] = f"{c}.{axis}"
            else:
                cmds.setAttr(f"{c}.{axis}", lock=True, keyable=False, channelBox=False)

    y = 0.0
    for regs in FACE_ROWS:
        row = [c for c in axes if region(c) in regs]
        if not row:
            continue
        group = cmds.group(empty=True, parent=board, name=f"faceBoard_{regs[0]}")
        # middle outwards: the row's regions in order, then by name; the right side mirrors the left
        order = {r: k for k, r in enumerate(regs)}
        by_side = {sd: sorted((c for c in row if side(c) == sd), key=lambda c: (order[region(c)], short_name(c))) for sd in ("R", "C", "L")}
        if by_side["R"] and by_side["L"]:  # pair right controls with their left twins so they mirror
            twins = {c.replace("CTRL_R_", "CTRL_L_"): c for c in by_side["R"]}
            by_side["R"] = [twins.pop(c) for c in by_side["L"] if c in twins] + sorted(twins.values())
        per_row = 7 if "mouth" in regs else 4
        cw = max(extent(c, "tx")[1] - extent(c, "tx")[0] for c in row) + gap + 0.6
        ch = max(extent(c, "ty")[1] - extent(c, "ty")[0] for c in row) + gap + label_h * 3
        centre = by_side["C"]
        cols_c = min(per_row, len(centre))
        half = cols_c * cw / 2 if centre else 0.0
        rows = 0
        for k, ctrl in enumerate(centre):
            n_row = min(per_row, len(centre) - (k // per_row) * per_row)
            place(ctrl, "C", -n_row * cw / 2 + (k % per_row + 0.5) * cw, y - (k // per_row) * ch, group)
            rows = max(rows, k // per_row + 1)
        for sd, sign in (("L", 1.0), ("R", -1.0)):
            for k, ctrl in enumerate(by_side[sd]):
                # left of the character on the right of the screen, growing outwards from the middle
                x = sign * (half + middle + (k % per_row + 0.5) * cw)
                place(ctrl, sd, x, y - (k // per_row) * ch, group)
                rows = max(rows, k // per_row + 1)
        y -= rows * ch + gap * 2
    # a face outline around it all
    bb = cmds.exactWorldBoundingBox(board)
    outline = cmds.circle(name="faceBoard_outline", normal=(0, 0, 1), radius=1, sections=24, constructionHistory=False)[0]
    cmds.setAttr(outline + ".scale", (bb[3] - bb[0]) / 2 * 1.12, (bb[4] - bb[1]) / 2 * 1.08, 1)
    cmds.xform(outline, translation=((bb[0] + bb[3]) / 2, (bb[1] + bb[4]) / 2, 0))
    cmds.parent(_reference(outline), board)
    log(f"face board: {len(axes)} controls")
    return plugs


# ----------------------------------------------------------------------------- the network


class _Net:
    """Creates network nodes and remembers them (they go into the NETWORK set)."""

    def __init__(self):
        self.nodes: List[str] = []

    def node(self, kind: str, name: str) -> str:
        n = _maya().createNode(kind, name=name, skipSelect=True)
        self.nodes.append(n)
        return n


def _range_curve(net: _Net, name: str, rows: List[Tuple[float, float, float, float]]) -> str:
    """One GUI -> raw pair: linear keys through its ranges (the first matching range wins at shared ends);
    0 outside them, as RigLogic adds nothing when no range matches."""
    cmds = _maya()
    curve = net.node("animCurveUU", name)
    keys: Dict[float, float] = {}
    for lo, hi, slope, cut in rows:
        for x in (lo, hi):
            keys.setdefault(round(x, 6), slope * x + cut)
    xs = sorted(keys)
    for x, edge in ((xs[0], -1e-3), (xs[-1], 1e-3)):
        if abs(keys[x]) > 1e-9:
            keys.setdefault(round(x + edge, 6), 0.0)
    for x in sorted(keys):
        cmds.setKeyframe(curve, float=x, value=keys[x], inTangentType="linear", outTangentType="linear")
    return curve


def build_controls(beh, plugs: Dict[int, str], net: _Net) -> Dict[int, str]:
    """Raw controls and correctives: control index (raw or PSD, as the DNA counts them) -> output plug."""
    cmds = _maya()
    raw_n = int(beh["raw_count"])
    pairs: Dict[Tuple[int, int], List[Tuple[float, float, float, float]]] = defaultdict(list)
    for i, o, lo, hi, s, c in zip(beh["gui_in"], beh["gui_out"], beh["gui_from"], beh["gui_to"], beh["gui_slope"], beh["gui_cut"]):
        pairs[(int(i), int(o))].append((float(lo), float(hi), float(s), float(c)))
    by_out: Dict[int, List[Tuple[int, List]]] = defaultdict(list)
    for (i, o), rows in pairs.items():
        by_out[o].append((i, rows))
    out: Dict[int, str] = {}
    for o, items in sorted(by_out.items()):
        total = net.node("plusMinusAverage", f"mmFace_raw{o}_sum")
        for k, (i, rows) in enumerate(items):
            if i not in plugs:
                continue
            curve = _range_curve(net, f"mmFace_raw{o}_in{i}", rows)
            cmds.connectAttr(plugs[i], curve + ".input")
            cmds.connectAttr(curve + ".output", f"{total}.input1D[{k}]")
        clamp = net.node("clamp", f"mmFace_raw{o}")
        cmds.setAttr(clamp + ".maxR", 1.0)
        cmds.connectAttr(total + ".output1D", clamp + ".inputR")
        out[o] = clamp + ".outputR"
    # correctives: weight * product of their (0..1) inputs, at most 1
    psd: Dict[int, List[Tuple[int, float]]] = defaultdict(list)
    for row, col, val in zip(beh["psd_rows"], beh["psd_cols"], beh["psd_values"]):
        psd[int(row)].append((int(col), float(val)))

    def plug(index: int) -> Optional[str]:
        if index in out:
            return out[index]
        if index < raw_n or index not in psd:
            return None
        weight = 1.0
        current: Optional[str] = None
        for col, val in psd[index]:
            weight *= val
            src = plug(col)
            if src is None:
                return None
            if current is None:
                current = src
            else:
                mul = net.node("multDoubleLinear", f"mmFace_psd{index}_x{col}")
                cmds.connectAttr(current, mul + ".input1")
                cmds.connectAttr(src, mul + ".input2")
                current = mul + ".output"
        scale = net.node("multDoubleLinear", f"mmFace_psd{index}_w")
        cmds.connectAttr(current, scale + ".input1")
        cmds.setAttr(scale + ".input2", weight)
        clamp = net.node("clamp", f"mmFace_psd{index}")
        cmds.setAttr(clamp + ".maxR", 1.0)
        cmds.connectAttr(scale + ".output", clamp + ".inputR")
        out[index] = clamp + ".outputR"
        return out[index]

    for index in sorted(psd):
        plug(index)
    return out


def build_joint_driver(beh, controls: Dict[int, str], net: _Net, parent: str) -> int:
    """The hidden curve whose points are the joints' translate / rotate / scale; one blendShape target
    per control that moves joints. Returns the number of driven joint attributes."""
    cmds = _maya()
    n = int(beh["joint_count"])
    names = [str(j) for j in beh["joint_names"]]
    rows = np.repeat(np.arange(len(beh["joint_out"])), np.diff(beh["joint_offsets"]))
    out_attr = beh["joint_out"][rows]  # joint * 9 + attribute, per weight
    weights = beh["joint_val"].astype(np.float64)
    weights = np.where((out_attr % 9 >= 3) & (out_attr % 9 < 6), np.radians(weights), weights)
    keep = np.abs(weights) > 1e-7
    out_attr, inputs, weights = out_attr[keep], beh["joint_in"][keep], weights[keep]
    # triples (joint, t / r / s) that move, and their curve point
    triples = sorted({(int(a) // 9, int(a) % 9 // 3) for a in np.unique(out_attr)})
    point = {t: k for k, t in enumerate(triples)}
    base = []
    for j, kind in triples:
        if kind == 0:  # the DNA's neutral (as the rig was built; never the scene's, which may be posed)
            base.append(tuple(float(v) for v in beh["neutral_t"][j]))
        else:
            base.append((0.0, 0.0, 0.0) if kind == 1 else (1.0, 1.0, 1.0))
    curve = cmds.curve(name=DRIVER, degree=1, point=base + ([base[-1]] if len(base) == 1 else []))
    cmds.parent(curve, parent)
    cmds.setAttr(curve + ".visibility", 0)
    shape = cmds.listRelatives(curve, shapes=True)[0]
    bs = cmds.blendShape(curve, name="mmFace_jointDriver")[0]
    net.nodes.append(bs)
    # one target per control: summed deltas per curve point
    order = np.argsort(inputs, kind="stable")
    inputs, out_attr, weights = inputs[order], out_attr[order], weights[order]
    starts = np.flatnonzero(np.r_[True, inputs[1:] != inputs[:-1]])
    ends = np.r_[starts[1:], len(inputs)]
    target = 0
    for s, e in zip(starts, ends):
        control = int(inputs[s])
        if control not in controls:
            continue
        delta: Dict[int, List[float]] = defaultdict(lambda: [0.0, 0.0, 0.0])
        for a, w in zip(out_attr[s:e], weights[s:e]):
            j, attr = int(a) // 9, int(a) % 9
            delta[point[(j, attr // 3)]][attr % 3] += float(w)
        ids = sorted(delta)
        item = f"{bs}.inputTarget[0].inputTargetGroup[{target}].inputTargetItem[6000]"
        cmds.setAttr(item + ".inputPointsTarget", len(ids), *[(*delta[i], 1.0) for i in ids], type="pointArray")
        cmds.setAttr(item + ".inputComponentsTarget", len(ids), *[f"cv[{i}]" for i in ids], type="componentList")
        cmds.connectAttr(controls[control], f"{bs}.weight[{target}]")
        target += 1
    info = net.node("curveInfo", "mmFace_jointValues")
    cmds.connectAttr(shape + ".local", info + ".inputCurve")
    for (j, kind), k in point.items():
        attr = ("translate", "rotate", "scale")[kind]
        dst = f"{names[j]}.{attr}"
        if not cmds.objExists(names[j]):
            continue
        if kind == 1:
            # point values are radians: no unit conversion on the way into the rotation
            conv = net.node("unitConversion", f"mmFace_{names[j]}_rot")
            cmds.setAttr(conv + ".conversionFactor", 1.0)
            cmds.connectAttr(f"{info}.controlPoints[{k}]", conv + ".input")
            cmds.connectAttr(conv + ".output", dst, force=True)
        else:
            cmds.connectAttr(f"{info}.controlPoints[{k}]", dst, force=True)
    return len(point)


def build_shape_links(beh, controls: Dict[int, str]) -> int:
    """Controls -> the MetaHuman blendShape weights (aliases are the DNA channel names)."""
    cmds = _maya()
    channels = [str(c) for c in beh["channel_names"]]
    nodes = cmds.ls(cmds.listHistory(cmds.listRelatives(mm_rig.GEOMETRY, allDescendents=True, type="mesh") or []) or [], type="blendShape")
    nodes = [b for b in set(nodes) if not cmds.listConnections(b + ".weight", source=True, destination=False, type="blendShape")]
    linked = 0
    for i, o in zip(beh["shape_in"], beh["shape_out"]):
        src = controls.get(int(i))
        if src is None:
            continue
        for b in nodes:
            alias = f"{b}.{channels[int(o)]}"
            if cmds.objExists(alias) and not cmds.listConnections(alias, source=True, destination=False):
                cmds.connectAttr(src, alias)
                linked += 1
    return linked


def import_epic_board(path: str, log: Callable[[str], None] = print) -> Dict[int, str]:
    """Epic's own MetaHuman face board (gui.ma from the artist's MetaHuman-DNA-Calibration download,
    never shipped with Mutant Tools), imported under BOARD. Returns GUI control index -> plug."""
    cmds = _maya()
    log("face board: importing Epic's board; Maya may say MayaUERBFPlugin was not found: expected, "
        "that part (Epic's neck setup) is removed right after")
    before = set(cmds.ls(assemblies=True))
    added = cmds.file(path, i=True, type="mayaAscii", ignoreVersion=True, mergeNamespacesOnClash=False,
                      preserveReferences=True, returnNewNodes=True) or []
    # Epic's neck setup needs Epic's RBF plugin (not in Maya 2026) and RigLogic: drop it, and any node
    # of a plugin Maya does not have, so the scene stays plain Maya
    for group in ("GRP_neckSetupGUI",):
        if cmds.objExists(group):
            cmds.delete(group)
    unknown = [n for n in cmds.ls(added, type=("unknown", "unknownDag", "unknownTransform")) if cmds.objExists(n)]
    if unknown:
        cmds.lockNode(unknown, lock=False)
        cmds.delete(unknown)
    for plugin in cmds.unknownPlugin(q=True, list=True) or []:
        if "UERBF" in plugin:
            cmds.unknownPlugin(plugin, remove=True)
    new = [n for n in cmds.ls(assemblies=True) if n not in before and cmds.nodeType(n) == "transform"]
    board = cmds.group(empty=True, world=True, name=BOARD)
    if new:
        cmds.parent(new, board)
    log(f"face board: imported Epic's board, dropped its neck setup and {len(unknown)} plugin node(s) Maya 2026 lacks")
    return {}


def remove():
    cmds = _maya()
    if cmds.objExists(NETWORK):
        nodes = cmds.sets(NETWORK, q=True) or []
        cmds.delete([n for n in nodes if cmds.objExists(n)] + [NETWORK])
    for n in (BOARD, DRIVER):
        if cmds.objExists(n):
            cmds.delete(n)


def build(dna_path: str, head: str = "", log: Callable[[str], None] = print, epic_board: str = "") -> dict:
    """Face board + network from the rig's DNA, next to `head` (the rigged copy), replacing an earlier one.
    `epic_board`: Epic's gui.ma (the MetaHuman board itself) to use instead of Meta Mutant's own board."""
    cmds = _maya()
    remove()
    r = mm_dna.load_dna(dna_path)
    beh = mm_face.export_behaviour(r)
    flips: Dict[int, bool] = {}
    net = _Net()
    if epic_board:
        import_epic_board(epic_board, log)
        names = [str(n) for n in beh["gui_names"]]
        plugs = {i: n for i, n in enumerate(names) if cmds.objExists(n)}
        missing = [n for n in names if not cmds.objExists(n)]
        log(f"face board: Epic's MetaHuman board ({os.path.basename(epic_board)}), {len(plugs)} of {len(names)} control channels"
            + (f"; missing {', '.join(missing[:5])}{'…' if len(missing) > 5 else ''}" if missing else ""))
    else:
        flips = directions(r, beh)
        plugs = build_board(beh, log, flips)
    controls = build_controls(beh, plugs, net)
    driven = build_joint_driver(beh, controls, net, mm_rig.ROOT)
    shapes = build_shape_links(beh, controls)
    cmds.sets(net.nodes, name=NETWORK)
    # sized and placed from the MetaHuman head (fitted onto your head): your own mesh may carry a neck
    # or a body that would make the board huge
    ref = "head_lod0_mesh" if cmds.objExists("head_lod0_mesh") else head
    if ref and cmds.objExists(ref):
        # beside the head (character's left), 1.5 times as tall as it
        # the visible shape only: a skinned mesh's Orig shape still sits where the rig was built
        visible = cmds.listRelatives(ref, shapes=True, noIntermediate=True, fullPath=True) or [ref]
        box = cmds.exactWorldBoundingBox(visible)
        lo, hi = box[:3], box[3:]
        blo = cmds.exactWorldBoundingBox(BOARD)
        k = 1.5 * (hi[1] - lo[1]) / max(1e-6, blo[4] - blo[1])
        cmds.setAttr(BOARD + ".scale", k, k, k)
        cmds.xform(BOARD, translation=(hi[0] + (hi[0] - lo[0]) * 0.3 - blo[0] * k, hi[1] - blo[4] * k, (lo[2] + hi[2]) / 2))
    log(f"face board: {len(plugs)} control channels drive {driven} joint channels and {shapes} blendshape weights; "
        f"{len(flips)} drawn flipped so they move the way the face does")
    return {"board": BOARD, "controls": len(plugs), "joint_channels": driven, "shapes": shapes}
