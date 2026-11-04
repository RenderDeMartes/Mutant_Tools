"""
The scene side of Meta Mutant's Pick Points window (Mutant_Tools/UI/MetaMutant/load_point_picker.py):
the MetaHuman head from the DNA and a copy of your head to click on, laid over each other and seen by
one camera from two panels, so tumbling either view moves both, each panel showing only its head.

Your own mesh is never touched: picks are made on the copy (same topology, same vertex ids) and
written with your mesh's name. Everything lives under one group, removed when the window closes.

    scene = mm_picker.PickScene(reader, "Head")
    scene.build()
    scene.source_panel_objects(), scene.custom_panel_objects()     # what each panel isolates
    scene.remove()
"""

from __future__ import annotations

import os
import sys
from typing import Dict, List, Optional, Sequence

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mm_points as mp  # noqa: E402
import mm_regions  # noqa: E402
import mm_rig  # noqa: E402

ROOT = "metaMutantPick_root"
SOURCE = "metaMutantPick_metaHuman"
CUSTOM = "metaMutantPick_head"
CAMERA = "metaMutantPick_camera"
SOURCE_POINTS = "metaMutantPick_metaHumanPoints"
CUSTOM_POINTS = "metaMutantPick_headPoints"
#: MetaHuman meshes shown, besides the head, so the lips and lids read as they will sit
SOURCE_MESHES = ("head", "teeth", "eyeLeft", "eyeRight")
#: viewport colours (RGB)
SKIN = (0.62, 0.62, 0.62)
REGION_COLORS = {
    "upper_lip": (0.85, 0.35, 0.35),
    "lower_lip": (0.85, 0.55, 0.25),
    "upper_eyelid": (0.35, 0.55, 0.9),
    "lower_eyelid": (0.3, 0.75, 0.75),
    "mouth_bag": (0.6, 0.35, 0.75),
    "eye_socket": (0.75, 0.7, 0.3),
}
POINT_DONE = (0.25, 0.85, 0.4)
POINT_WAITING = (0.3, 0.55, 0.95)
POINT_ACTIVE = (1.0, 0.8, 0.1)


def _maya():
    import maya.api.OpenMaya as om  # type: ignore
    import maya.cmds as cmds  # type: ignore

    return cmds, om


def _fn(mesh: str):
    cmds, om = _maya()
    sel = om.MSelectionList()
    sel.add(mesh)
    return om.MFnMesh(sel.getDagPath(0))


def mesh_positions(mesh: str, space=None) -> np.ndarray:
    _, om = _maya()
    fn = _fn(mesh)
    return np.array([(p.x, p.y, p.z) for p in fn.getPoints(space if space is not None else om.MSpace.kWorld)])


def dna_regions(reader, m: int) -> Dict[str, List[int]]:
    """The MetaHuman head's regions, from the skin weights in the DNA (no rig needed)."""
    names = [reader.getJointName(j) for j in range(reader.getJointCount())]
    _, weights = mm_rig.skin(reader, m)
    return mm_regions.metahuman_regions(names, weights)


def component_vertex(item: str) -> Optional[int]:
    """'mesh.vtx[12]' -> 12, anything else -> None."""
    if ".vtx[" not in item or ":" in item.split(".vtx[")[1]:
        return None
    return int(item.split(".vtx[")[1].rstrip("]"))


def _node_name(side: str, label: str) -> str:
    """Unique in the scene: Maya repeats a short name freely across groups, and then cannot find it."""
    return "metaMutantPick_{}_{}".format(side, "".join(c if c.isalnum() else "_" for c in label))


class PickScene:
    def __init__(self, reader, head: str):
        self.reader, self.head = reader, head
        self.head_index = next(m for m in mm_rig.mm_dna.mesh_indices_for_lod(reader, 0, ("head",)))
        self.source_regions: Dict[str, List[int]] = {}
        self.source_positions = np.zeros((0, 3))
        self.source_meshes: List[str] = []
        self.source_mesh = ""
        self.source_scale = 1.0
        self.custom_positions = np.zeros((0, 3))
        self.others: List[str] = []
        self.spheres: Dict[str, Dict[str, str]] = {"source": {}, "custom": {}}
        self.curves: Dict[str, Dict[str, str]] = {"source": {}, "custom": {}}
        self.shaders: Dict[tuple, str] = {}
        self.sphere_size = mp.DEFAULT_SPHERE_SIZE

    # ------------------------------------------------------------------ build

    def build(self) -> None:
        cmds, _ = _maya()
        self.remove()
        was = cmds.undoInfo(q=True, stateWithoutFlush=True)
        cmds.undoInfo(stateWithoutFlush=False)  # Ctrl+Z while picking must not take the window's meshes apart
        try:
            root = cmds.group(empty=True, world=True, name=ROOT)
            cmds.setAttr(f"{root}.hiddenInOutliner", True)
            self._build_custom(root)
            self._build_source(root)
            self.others = self._other_meshes()
            self._build_camera()
        finally:
            cmds.undoInfo(stateWithoutFlush=was)

    def _build_custom(self, root: str) -> None:
        cmds, _ = _maya()
        if not cmds.objExists(self.head):
            raise RuntimeError(f"your head mesh {self.head!r} is not in the scene")
        copy = cmds.duplicate(self.head, name=CUSTOM, returnRootsOnly=True)[0]
        for attr in ("tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v"):
            cmds.setAttr(f"{copy}.{attr}", lock=False)
        for shape in cmds.listRelatives(copy, shapes=True, fullPath=True) or []:
            if cmds.getAttr(shape + ".intermediateObject"):
                cmds.delete(shape)
        for child in cmds.listRelatives(copy, children=True, type="transform", fullPath=True) or []:
            cmds.delete(child)
        cmds.parent(copy, root)
        cmds.setAttr(f"{CUSTOM}.visibility", True)
        cmds.group(empty=True, parent=root, name=CUSTOM_POINTS)
        self.custom_positions = mesh_positions(CUSTOM)

    def _build_source(self, root: str) -> None:
        cmds, _ = _maya()
        group = cmds.group(empty=True, parent=root, name=SOURCE)
        self.source_meshes = []
        for m in mm_rig.mm_dna.mesh_indices_for_lod(self.reader, 0, SOURCE_MESHES):
            mesh = mm_rig.build_mesh(self.reader, m, group)
            mesh = cmds.rename(mesh, f"metaMutantPick_{self.reader.getMeshName(m)}")
            self.source_meshes.append(mesh)
            if m == self.head_index:
                self.source_mesh = mesh
        # not selectable: the MetaHuman side is already known
        cmds.setAttr(f"{group}.overrideEnabled", True)
        cmds.setAttr(f"{group}.overrideDisplayType", 2)
        cmds.group(empty=True, parent=group, name=SOURCE_POINTS)
        self.source_positions = mesh_positions(self.source_mesh, _maya()[1].MSpace.kObject)
        self.source_regions = dna_regions(self.reader, self.head_index)
        self.fit_source()

    def fit_source(self, pairs: Sequence = ()) -> None:
        """Lay the MetaHuman over your head: by their boxes, then by the points picked so far. Scale and move
        only (both heads look forward): this only has to line the two views up."""
        cmds, _ = _maya()
        if len(pairs) >= 3:
            src = np.array([a for a, _ in pairs], float)
            dst = np.array([b for _, b in pairs], float)
            spread = np.linalg.norm(src - src.mean(0), axis=1).sum()
            scale = float(np.linalg.norm(dst - dst.mean(0), axis=1).sum() / spread) if spread > 0 else self.source_scale
            move = dst.mean(0) - scale * src.mean(0)
        else:
            # the MetaHuman's head only, without the neck and shoulders of its mesh
            chin = self.source_positions[dict((g[0], g[1]) for g in mp.GUIDES)["Chin bottom"], 1]
            head = self.source_positions[self.source_positions[:, 1] >= chin]
            scale, move = mp.bounds_fit(head.min(0), head.max(0), self.custom_positions.min(0), self.custom_positions.max(0))
        if not np.isfinite(scale) or scale <= 0:
            return
        self.source_scale = scale
        cmds.xform(SOURCE, worldSpace=True, scale=(scale, scale, scale), translation=[float(v) for v in move])
        self.set_sphere_size(self.sphere_size)

    def _other_meshes(self) -> List[str]:
        """Your other visible meshes (eyes, teeth...): shown while picking those."""
        cmds, _ = _maya()
        out = []
        for shape in cmds.ls(type="mesh", noIntermediate=True, long=True, visible=True) or []:
            node = cmds.listRelatives(shape, parent=True, fullPath=True)[0]
            if ROOT not in node and node.split("|")[-1] != self.head.split("|")[-1] and node not in out:
                out.append(node)
        return out

    def _build_camera(self) -> None:
        cmds, _ = _maya()
        low, high = self.custom_positions.min(0), self.custom_positions.max(0)
        centre, size = (low + high) / 2, float(max(high - low))
        camera = cmds.camera(name=CAMERA, focalLength=50, nearClipPlane=max(0.01, size * 0.01), farClipPlane=size * 100)[0]
        camera = cmds.rename(cmds.parent(camera, ROOT)[0], CAMERA)
        distance = size * 1.7
        cmds.xform(camera, worldSpace=True, translation=(float(centre[0]), float(centre[1]), float(high[2] + distance)), rotation=(0, 0, 0))
        cmds.setAttr(f"{camera}.centerOfInterest", distance + float(high[2] - centre[2]))

    @property
    def camera(self) -> str:
        return f"{ROOT}|{CAMERA}"

    def source_panel_objects(self) -> List[str]:
        return [SOURCE]

    def custom_panel_objects(self, with_others: bool = False) -> List[str]:
        return [CUSTOM, CUSTOM_POINTS] + (self.others if with_others else [])

    # ------------------------------------------------------------------ points

    def _shader(self, color) -> str:
        cmds, _ = _maya()
        color = tuple(color)
        if color not in self.shaders or not cmds.objExists(self.shaders[color]):
            shader = cmds.shadingNode("lambert", asShader=True, skipSelect=True, name="metaMutantPick_shader")
            cmds.setAttr(shader + ".color", *color, type="double3")
            cmds.setAttr(shader + ".incandescence", *[v * 0.6 for v in color], type="double3")
            group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=shader + "SG")
            cmds.connectAttr(shader + ".outColor", group + ".surfaceShader")
            self.shaders[color] = group
        return self.shaders[color]

    def _sphere_scale(self, side: str, factor: float = 1.0) -> float:
        """The slider's size in hundredths of your head's height, whatever units the head came in."""
        unit = float(self.custom_positions[:, 1].max() - self.custom_positions[:, 1].min()) / 100.0
        return self.sphere_size * unit * factor / (self.source_scale if side == "source" else 1.0)

    def put_sphere(self, side: str, label: str, position, color=POINT_DONE, factor: float = 1.0) -> str:
        """A small sphere you cannot select: where a point is. Replaces the one of the same label."""
        cmds, _ = _maya()
        self.drop_sphere(side, label)
        was = cmds.undoInfo(q=True, stateWithoutFlush=True)
        cmds.undoInfo(stateWithoutFlush=False)
        try:
            node = cmds.polySphere(name=_node_name(side, label), subdivisionsAxis=10, subdivisionsHeight=8, radius=1, constructionHistory=False)[0]
            # relative: the position is in the head's own space, which the MetaHuman's group moves and scales
            node = cmds.parent(node, SOURCE_POINTS if side == "source" else CUSTOM_POINTS, relative=True)[0]
            cmds.setAttr(f"{node}.overrideEnabled", True)
            cmds.setAttr(f"{node}.overrideDisplayType", 2)
            cmds.setAttr(f"{node}.translate", *[float(v) for v in position], type="double3")
            scale = self._sphere_scale(side, factor)
            cmds.setAttr(f"{node}.scale", scale, scale, scale, type="double3")
            cmds.sets(node, edit=True, forceElement=self._shader(color))
        finally:
            cmds.undoInfo(stateWithoutFlush=was)
        self.spheres[side][label] = node
        return node

    def drop_sphere(self, side: str, label: str) -> None:
        cmds, _ = _maya()
        node = self.spheres[side].pop(label, None)
        if node and cmds.objExists(node):
            cmds.delete(node)

    def set_sphere_size(self, size: float) -> None:
        cmds, _ = _maya()
        self.sphere_size = size
        for side, nodes in self.spheres.items():
            for node in nodes.values():
                if cmds.objExists(node):
                    s = self._sphere_scale(side)
                    cmds.setAttr(f"{node}.scale", s, s, s, type="double3")

    def color_sphere(self, side: str, label: str, color) -> None:
        cmds, _ = _maya()
        node = self.spheres[side].get(label)
        if node and cmds.objExists(node):
            cmds.sets(node, edit=True, forceElement=self._shader(color))

    # ------------------------------------------------------------------ lines

    def put_curve(self, side: str, key: str, positions, color=POINT_DONE, width: float = 3.0) -> str:
        cmds, _ = _maya()
        self.drop_curve(side, key)
        was = cmds.undoInfo(q=True, stateWithoutFlush=True)
        cmds.undoInfo(stateWithoutFlush=False)
        try:
            node = cmds.curve(degree=1, point=[tuple(float(v) for v in p) for p in positions], name=_node_name(side, key))
            node = cmds.parent(node, SOURCE_POINTS if side == "source" else CUSTOM_POINTS, relative=True)[0]
            shape = cmds.listRelatives(node, shapes=True, fullPath=True)[0]
            cmds.setAttr(f"{shape}.lineWidth", width)
            cmds.setAttr(f"{shape}.overrideEnabled", True)
            cmds.setAttr(f"{shape}.overrideRGBColors", True)
            cmds.setAttr(f"{shape}.overrideColorRGB", *color)
            cmds.setAttr(f"{node}.overrideEnabled", True)
            cmds.setAttr(f"{node}.overrideDisplayType", 2)
        finally:
            cmds.undoInfo(stateWithoutFlush=was)
        self.curves[side][key] = node
        return node

    def drop_curve(self, side: str, key: str) -> None:
        cmds, _ = _maya()
        node = self.curves[side].pop(key, None)
        if node and cmds.objExists(node):
            cmds.delete(node)

    def color_curve(self, side: str, key: str, color) -> None:
        cmds, _ = _maya()
        node = self.curves[side].get(key)
        if node and cmds.objExists(node):
            shape = cmds.listRelatives(node, shapes=True, fullPath=True)[0]
            cmds.setAttr(f"{shape}.overrideColorRGB", *color)

    # ------------------------------------------------------------------ regions

    def paint_regions(self, mesh: str, regions: Dict[str, Sequence[int]]) -> None:
        """Faces of `mesh` in the region colours (vertex ids per region; a face belongs with all its corners in)."""
        cmds, om = _maya()
        was = cmds.undoInfo(q=True, stateWithoutFlush=True)
        cmds.undoInfo(stateWithoutFlush=False)
        try:
            fn = _fn(mesh)
            counts, connects = fn.getVertices()
            colors = om.MColorArray()
            members = {k: set(v) for k, v in regions.items() if v}
            at = 0
            for count in counts:
                corners = connects[at:at + count]
                at += count
                color = SKIN
                for key, verts in members.items():
                    if all(c in verts for c in corners):
                        color = REGION_COLORS.get(key, SKIN)
                        break
                colors.append(om.MColor((color[0], color[1], color[2], 1.0)))
            fn.setFaceColors(colors, om.MIntArray(list(range(len(counts)))))
            shape = fn.fullPathName()
            cmds.setAttr(shape + ".displayColors", True)
        finally:
            cmds.undoInfo(stateWithoutFlush=was)

    # ------------------------------------------------------------------ picks

    def to_mesh_names(self, items: Sequence[str]) -> List[str]:
        """The selection as you see it, written with your mesh's name instead of the copy's."""
        return [(self.head + item[len(CUSTOM):]) if item.split("|")[-1].startswith(CUSTOM + ".") or item.startswith(CUSTOM + ".") else item
                for item in items]

    def to_copy_names(self, items: Sequence[str]) -> List[str]:
        return [(CUSTOM + item[len(self.head):]) if item.startswith(self.head + ".") else item for item in items]

    def selected_edges(self, items: Sequence[str]) -> List[tuple]:
        """Selected edges of the copy as vertex pairs. Raises what to fix."""
        cmds, _ = _maya()
        edges = []
        for item in cmds.ls(items, flatten=True) or []:
            if ".e[" not in item or item.split(".")[0].split("|")[-1] != CUSTOM:
                raise ValueError("select edges of your head (the right panel)")
            pair = cmds.polyInfo(item, edgeToVertex=True)[0].split(":")[1].split()[:2]
            edges.append((int(pair[0]), int(pair[1])))
        return edges

    def edges_to_lines(self, key: str, items: Sequence[str]) -> Dict[str, List[int]]:
        """The line(s) these edges give: `key` for an open line; for a closed loop both lines it splits into,
        wherever the row was. Vertices along each line by rising X. Raises what to fix."""
        edges = self.selected_edges(items)
        if edges and mp.is_ring(edges):
            pair = next(p for p in mp.LINE_PAIRS if key in p)
            upper, lower = mp.split_ring(mp.ring_from_edges(edges), self.custom_positions)
            return {pair[0]: upper, pair[1]: lower}
        return {key: mp.oriented(mp.chain_from_edges(edges), self.custom_positions)}

    def edges_to_vertices(self, items: Sequence[str]) -> List[int]:
        """Selected edges of the copy, as one open line (rising X). Raises what to fix."""
        return mp.oriented(mp.chain_from_edges(self.selected_edges(items)), self.custom_positions)

    # ------------------------------------------------------------------ cleanup

    def remove(self) -> None:
        cmds, _ = _maya()
        was = cmds.undoInfo(q=True, stateWithoutFlush=True)
        cmds.undoInfo(stateWithoutFlush=False)
        try:
            if cmds.objExists(ROOT):
                cmds.delete(ROOT)
            for node in cmds.ls("metaMutantPick_*") or []:
                if cmds.objExists(node) and cmds.nodeType(node) in ("lambert", "shadingEngine"):
                    cmds.delete(node)
        finally:
            cmds.undoInfo(stateWithoutFlush=was)
        self.spheres = {"source": {}, "custom": {}}
        self.curves = {"source": {}, "custom": {}}
        self.shaders = {}
