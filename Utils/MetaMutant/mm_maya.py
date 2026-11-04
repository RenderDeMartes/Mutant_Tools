"""
Maya side of Meta Mutant (MetaHuman rig on a custom head, through TopoTransfer).

Run inside Maya 2026 (Script Editor, Python tab) with this folder and Epic's `dna`
module on sys.path (the one in dna_module/Maya2026) — or use the guided window:
Mutant-Tools > Misc > Meta Mutant.

    import sys; sys.path.append(r"C:/path/to/Mutant_Tools/Utils/MetaMutant")
    import mm_maya
    mm_maya.build_rig(r"C:/mh/head_custom.dna")                     # mm_rig: joints, meshes, skin, shapes
    mm_maya.check_joint_convention(r"C:/mh/head_custom.dna")        # the built joints match the DNA math
    mm_maya.align_custom_mesh("customHead", r"C:/mh/wrapped.obj")   # into DNA space
    mm_maya.transfer_rig("head_lod0_mesh", "customHead")            # skin + blendshapes

`transfer_rig` binds the custom mesh to the same joints, copies skin weights
from the calibrated MetaHuman head (closest point) and gives it every
blendshape target of the MetaHuman head (each vertex takes the delta of the
closest point on the MetaHuman surface), with its weights driven by the
MetaHuman blendShape node, so one set of weights drives both meshes.
"""

from __future__ import annotations

import os
import sys
from typing import Dict, List, Optional, Sequence, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mm_core as core  # noqa: E402

try:  # pragma: no cover - only inside Maya
    import maya.cmds as cmds  # type: ignore
    import maya.mel as mel  # type: ignore
except ImportError:  # allows importing this module for documentation / tests
    cmds = None
    mel = None


def _require_maya():
    if cmds is None:
        raise RuntimeError("mm_maya must be run inside Maya")


# ----------------------------------------------------------------------------- rig building


def build_rig(dna_path: str, add_rig_logic: bool = False, blendshapes: bool = True):
    """Build the MetaHuman head rig (joints, LOD0 meshes, skin, blendshapes) from a DNA with mm_rig."""
    _require_maya()
    import mm_rig

    return mm_rig.build(dna_path, blendshapes=blendshapes)


def check_joint_convention(dna_path: str, tolerance: float = 1e-3) -> float:
    """
    Compare joint world positions computed by mm_core from the DNA with the
    joints in the current scene (build the rig from the same DNA first, or let
    this function build it). Returns the max error; raises if above tolerance.
    """
    _require_maya()
    import mm_dna

    r = mm_dna.load_dna(dna_path)
    sk = core.skeleton_from_reader(r)
    if not cmds.objExists(sk.names[0]):
        build_rig(dna_path, add_rig_logic=False)
    world, _ = core.joint_world(sk)
    worst = 0.0
    worst_name = ""
    for j, name in enumerate(sk.names):
        if not cmds.objExists(name):
            continue
        p = cmds.xform(name, q=True, ws=True, t=True)
        e = max(abs(p[k] - world[j][k]) for k in range(3))
        if e > worst:
            worst, worst_name = e, name
    print(f"[TopoTransfer] joint convention check: max error {worst:.6f} at {worst_name}")
    if worst > tolerance:
        raise RuntimeError(
            "Joint positions computed from the DNA do not match Maya. The rotation convention in mm_core.euler_xyz_deg "
            "differs from this DNA version; do not use the calibrated joints until fixed."
        )
    return worst


# ----------------------------------------------------------------------------- OBJ in / out


def scene_space():
    """(linear unit, up axis) of the open scene."""
    _require_maya()
    return cmds.currentUnit(q=True, linear=True), cmds.upAxis(q=True, axis=True)


def export_mesh_obj(mesh: str, path: str) -> str:
    """Export one mesh as OBJ in world space (Maya's objExport plugin), e.g. as TopoTransfer Reference."""
    _require_maya()
    if not cmds.objExists(mesh):
        raise RuntimeError(f"{mesh} does not exist")
    cmds.loadPlugin("objExport", quiet=True)
    sel = cmds.ls(selection=True)
    try:
        cmds.select(mesh, replace=True)
        cmds.file(path, force=True, options="groups=0;ptgroups=0;materials=0;smoothing=0;normals=0", type="OBJexport", exportSelected=True, preserveReferences=False)
    finally:
        if sel:
            cmds.select(sel, replace=True)
        else:
            cmds.select(clear=True)
    return path


def import_obj(path: str, name: str, matrix: Optional[List[float]] = None) -> str:
    """Import an OBJ as one mesh named `name` (replacing an older one), optionally placed with `matrix`."""
    _require_maya()
    cmds.loadPlugin("objExport", quiet=True)
    if cmds.objExists(name):
        cmds.delete(name)
    nodes = cmds.file(path, i=True, type="OBJ", options="mo=0", returnNewNodes=True, ignoreVersion=True, namespace="tt_import")
    meshes = cmds.ls(nodes, type="transform") or []
    if not meshes:
        raise RuntimeError(f"no mesh imported from {path}")
    node = cmds.rename(meshes[0], name)
    cmds.namespace(removeNamespace="tt_import", mergeNamespaceWithRoot=True)
    if matrix is not None:
        cmds.xform(node, matrix=matrix, worldSpace=True)
    return node


# ----------------------------------------------------------------------------- custom mesh placement


def align_custom_mesh(mesh: str, wrapped_obj: str) -> List[float]:
    """
    Move the custom (reference) mesh into DNA space using the alignment that
    TopoTransfer wrote into the exported OBJ header (inverse of base->reference).
    The transform is frozen into the vertices. Returns the matrix applied.
    """
    _require_maya()
    import maya.api.OpenMaya as om  # type: ignore

    w = core.read_obj_positions(wrapped_obj)
    inv = core.mat4_inverse(w.alignment)
    if cmds.listRelatives(mesh, parent=True):  # under a group: frozen at world level, no parent offset left
        cmds.parent(mesh, world=True)
    # Maya xform matrices are row-major with translation in the last row = our column-major list.
    # The mesh keeps its own transform: world points go through it first, then through the inverse
    # alignment (row vectors: p * current * inv).
    current = om.MMatrix(cmds.xform(mesh, q=True, matrix=True, worldSpace=True))
    placed = current * om.MMatrix(inv)
    cmds.xform(mesh, matrix=[placed[i] for i in range(16)], worldSpace=True)
    cmds.makeIdentity(mesh, apply=True, translate=True, rotate=True, scale=True, normal=False)
    return inv


def place_in_scene(wrapped_obj: str, meshes: Sequence[str] = ()) -> List[float]:
    """
    Put the rig, built in DNA space, back where the custom head is: `metaMutant_rig` gets the
    DNA -> scene alignment TopoTransfer exported (base -> reference), so the joints move onto the
    head. `meshes` (the rigged copies, in DNA space) go into the geometry group. Skinned meshes
    follow the joints, so the geometry group does not inherit the move (that would apply it twice);
    meshes without a skin get it on their own transform. Returns the matrix applied.
    """
    _require_maya()
    import mm_rig

    alignment = list(core.read_obj_positions(wrapped_obj).alignment)
    for mesh in meshes:
        if cmds.listRelatives(mesh, parent=True) != [mm_rig.GEOMETRY]:
            cmds.parent(mesh, mm_rig.GEOMETRY)
    cmds.setAttr(mm_rig.GEOMETRY + ".inheritsTransform", 0)
    # Maya xform matrices are row-major with translation in the last row = our column-major list
    cmds.xform(mm_rig.ROOT, matrix=alignment, worldSpace=True)
    for mesh in cmds.listRelatives(mm_rig.GEOMETRY, children=True, type="transform") or []:
        if not _skin_cluster(mesh):
            cmds.xform(mesh, matrix=alignment, worldSpace=True)
    return alignment


# ----------------------------------------------------------------------------- rig transfer


#: the material of eyes and teeth that came without a shader
PARTS_MATERIAL = "metaMutant_parts"
PARTS_COLOUR = (0.74, 0.72, 0.70)


def _skin_cluster(mesh: str) -> Optional[str]:
    hist = cmds.listHistory(mesh, pruneDagObjects=True) or []
    sc = cmds.ls(hist, type="skinCluster")
    return sc[0] if sc else None


def _blend_shape(mesh: str) -> Optional[str]:
    hist = cmds.listHistory(mesh, pruneDagObjects=True) or []
    bs = cmds.ls(hist, type="blendShape")
    return bs[0] if bs else None


def _skin_weights(mesh: str):
    """(influence names, weights as a vertices x influences numpy array) of a skinned mesh."""
    import maya.api.OpenMaya as om  # type: ignore
    import maya.api.OpenMayaAnim as oma  # type: ignore
    import numpy as np

    sc = _skin_cluster(mesh)
    sel = om.MSelectionList()
    sel.add(sc)
    sel.add(mesh)
    fn = oma.MFnSkinCluster(sel.getDependNode(0))
    path = sel.getDagPath(1)
    path.extendToShape()
    comp = om.MFnSingleIndexedComponent()
    obj = comp.create(om.MFn.kMeshVertComponent)
    comp.setCompleteData(om.MFnMesh(path).numVertices)
    values, count = fn.getWeights(path, obj)
    names = [p.partialPathName() for p in fn.influenceObjects()]
    return names, np.array(values, float).reshape(-1, count), (fn, path, obj)


def mesh_arrays(mesh: str):
    """(world positions, triangle vertex ids) of a mesh as numpy arrays."""
    import maya.api.OpenMaya as om  # type: ignore
    import numpy as np

    sel = om.MSelectionList()
    sel.add(mesh)
    path = sel.getDagPath(0)
    path.extendToShape()
    fn = om.MFnMesh(path)
    points = np.array([(p.x, p.y, p.z) for p in fn.getPoints(om.MSpace.kWorld)], float)
    _, ids = fn.getTriangles()
    return points, np.array(ids, int).reshape(-1, 3)


def metahuman_regions(source_mesh: str) -> Dict[str, List[int]]:
    """The MetaHuman head's lips / eyelids / mouth bag, from its skin weights (mm_regions)."""
    import mm_regions

    names, w, _ = _skin_weights(source_mesh)
    pairs = [[(j, float(x)) for j, x in enumerate(row) if x > 0] for row in w]
    return mm_regions.metahuman_regions(names, pairs)


def region_correspondence(source_mesh: str, target_mesh: str, target_regions: Dict[str, Sequence[int]],
                          log=print) -> List[Tuple[Tuple[int, int, int], Tuple[float, float, float]]]:
    """surface_correspondence, but each picked region of the target only finds the same region of the
    MetaHuman (and the rest only the MetaHuman outside the picked regions)."""
    import mm_regions

    src_points, tris = mesh_arrays(source_mesh)
    tgt_points, _ = mesh_arrays(target_mesh)
    source_regions = metahuman_regions(source_mesh)
    log("regions: " + ", ".join(f"{k} {len(v)} of yours -> {len(source_regions.get(k, []))} MetaHuman"
                                for k, v in target_regions.items() if v))
    g = mm_regions.groups(len(tgt_points), target_regions, len(src_points), source_regions)
    return mm_regions.correspondence(tgt_points, src_points, tris, g)


def line_correspondence(source_mesh: str, target_mesh: str, points: dict, corr=None, log=print):
    """Closest point (or `corr`, from the regions) with the picked lip and eyelid lines applied on top (mm_zones)."""
    import mm_zones

    base = corr if corr is not None else surface_correspondence(source_mesh, target_mesh)
    return mm_zones.correspondence(points, mesh_points(target_mesh), mesh_edges(target_mesh),
                                   mesh_points(source_mesh), mesh_edges(source_mesh), base, log=log)


def mesh_edges(mesh: str):
    """The polygon edges of a mesh (n, 2), not the triangles' diagonals."""
    import maya.api.OpenMaya as om  # type: ignore
    import mm_zones

    sel = om.MSelectionList()
    sel.add(mesh)
    counts, connects = om.MFnMesh(sel.getDagPath(0)).getVertices()
    return mm_zones.polygon_edges(list(counts), list(connects))


def transfer_skin(source_mesh: str, target_mesh: str, corr=None) -> str:
    """Bind the target to the source's influences and copy weights by closest point (or through
    `corr`, a region_correspondence: each vertex blends the weights of its source triangle)."""
    _require_maya()
    src_sc = _skin_cluster(source_mesh)
    if not src_sc:
        raise RuntimeError(f"{source_mesh} has no skinCluster")
    influences = cmds.skinCluster(src_sc, q=True, influence=True)
    max_inf = cmds.skinCluster(src_sc, q=True, maximumInfluences=True) or 8
    dst_sc = _skin_cluster(target_mesh) or cmds.skinCluster(influences, target_mesh, toSelectedBones=True, maximumInfluences=max_inf, name=f"{target_mesh}_skinCluster")[0]
    if corr is None:
        cmds.copySkinWeights(sourceSkin=src_sc, destinationSkin=dst_sc, noMirror=True, surfaceAssociation="closestPoint", influenceAssociation=["oneToOne", "name"], normalize=True)
        return dst_sc
    import maya.api.OpenMaya as om  # type: ignore
    import numpy as np

    src_names, src_w, _ = _skin_weights(source_mesh)
    dst_names, _, (fn, path, obj) = _skin_weights(target_mesh)
    column = [dst_names.index(n) for n in src_names]
    # entries hold 3 corners of a triangle, or more where a line paired the vertex (mm_zones)
    width = max(len(c[0]) for c in corr)
    tri = np.zeros((len(corr), width), int)
    bary = np.zeros((len(corr), width))
    for row, (ids, weights) in enumerate(corr):
        tri[row, :len(ids)] = ids
        bary[row, :len(ids)] = weights
    blended = np.einsum("tk,tki->ti", bary, src_w[tri])
    out = np.zeros((len(corr), len(dst_names)))
    out[:, column] = blended
    out /= np.maximum(out.sum(1, keepdims=True), 1e-12)
    fn.setWeights(path, obj, om.MIntArray(list(range(len(dst_names)))), om.MDoubleArray(out.ravel().tolist()), False)
    return dst_sc


def _component_ids(components: Sequence[str]) -> List[int]:
    """['vtx[3]', 'vtx[5:9]'] -> [3, 5, 6, 7, 8, 9] (a blendShape target's inputComponentsTarget)."""
    out: List[int] = []
    for c in components or []:
        inside = c[c.index("[") + 1:c.rindex("]")]
        if ":" in inside:
            a, b = inside.split(":")
            out.extend(range(int(a), int(b) + 1))
        else:
            out.append(int(inside))
    return out


def surface_correspondence(source_mesh: str, target_mesh: str) -> List[Tuple[Tuple[int, int, int], Tuple[float, float, float]]]:
    """For each target vertex: the source triangle under it (closest point) and its barycentric weights."""
    import maya.api.OpenMaya as om  # type: ignore

    sel = om.MSelectionList()
    sel.add(source_mesh)
    sel.add(target_mesh)
    src_path, tgt_path = sel.getDagPath(0), sel.getDagPath(1)
    src_path.extendToShape()
    src_fn = om.MFnMesh(src_path)
    intersector = om.MMeshIntersector()
    intersector.create(src_path.node(), src_path.inclusiveMatrix())
    out = []
    for p in om.MFnMesh(tgt_path).getPoints(om.MSpace.kWorld):
        hit = intersector.getClosestPoint(p)
        u, v = hit.barycentricCoords
        tri = src_fn.getPolygonTriangleVertices(hit.face, hit.triangle)
        out.append(((tri[0], tri[1], tri[2]), (u, v, 1.0 - u - v)))
    return out


def transfer_blendshapes(source_mesh: str, target_mesh: str, keep_still: Sequence[int] = (),
                         log=print, corr=None) -> Optional[str]:
    """
    Every blendshape target of `source_mesh` onto `target_mesh`: each target vertex takes the delta
    of the closest point on the source (interpolated over its triangle), written straight into a new
    blendShape node whose weights follow the source weights. Both meshes must be in the same space
    and at rest. `keep_still`: target vertices the shapes must not move (picked eyes, teeth).
    """
    _require_maya()
    src_bs = _blend_shape(source_mesh)
    if not src_bs:
        log(f"{source_mesh} has no blendShape node; nothing to transfer")
        return None
    aliases = cmds.aliasAttr(src_bs, q=True) or []
    by_index = {}
    for alias, plug in zip(aliases[0::2], aliases[1::2]):
        if plug.startswith("weight["):
            by_index[int(plug[7:-1])] = alias
    corr = corr if corr is not None else surface_correspondence(source_mesh, target_mesh)
    still = set(keep_still)
    dst_bs = cmds.blendShape(target_mesh, name=f"{target_mesh}_blendShapes", frontOfChain=True)[0]
    written = 0
    for k, (i, alias) in enumerate(sorted(by_index.items())):
        item = f"{src_bs}.inputTarget[0].inputTargetGroup[{i}].inputTargetItem[6000]"
        ids = _component_ids(cmds.getAttr(item + ".inputComponentsTarget") or [])
        pts = cmds.getAttr(item + ".inputPointsTarget") or []
        delta = {v: p for v, p in zip(ids, pts)}
        out_ids, out_pts = [], []
        for t, (tri, w) in enumerate(corr):
            if t in still:
                continue
            x = y = z = 0.0
            for v, wv in zip(tri, w):
                d = delta.get(v)
                if d is not None:
                    x += d[0] * wv
                    y += d[1] * wv
                    z += d[2] * wv
            if abs(x) + abs(y) + abs(z) > 1e-7:
                out_ids.append(t)
                out_pts.append((x, y, z, 1.0))
        dst_item = f"{dst_bs}.inputTarget[0].inputTargetGroup[{k}].inputTargetItem[6000]"
        cmds.setAttr(dst_item + ".inputPointsTarget", len(out_pts), *out_pts, type="pointArray")
        cmds.setAttr(dst_item + ".inputComponentsTarget", len(out_ids), *[f"vtx[{t}]" for t in out_ids], type="componentList")
        cmds.setAttr(f"{dst_bs}.weight[{k}]", 0.0)
        cmds.aliasAttr(alias, f"{dst_bs}.weight[{k}]")
        cmds.connectAttr(f"{src_bs}.{alias}", f"{dst_bs}.{alias}", force=True)
        written += bool(out_ids)
    log(f"{target_mesh}: {len(by_index)} blendshape targets from {source_mesh} ({written} move it)")
    return dst_bs


def transfer_rig(source_mesh: str, target_mesh: str, blendshapes: bool = True) -> dict:
    """Skin weights + blendshapes from the calibrated MetaHuman head to the custom mesh."""
    _require_maya()
    out = {"skinCluster": transfer_skin(source_mesh, target_mesh)}
    if blendshapes:
        out["blendShape"] = transfer_blendshapes(source_mesh, target_mesh)
    return out


# ----------------------------------------------------------------------------- eyes, teeth and tongue


def selection_spec() -> List[str]:
    """The selection as a part spec: whole meshes and / or faces (or vertices, edges) of a mesh."""
    _require_maya()
    return cmds.ls(selection=True) or []


def _transform(node: str) -> str:
    if cmds.nodeType(node) == "mesh":
        return cmds.listRelatives(node, parent=True)[0]
    return node


def spec_vertices(spec: Sequence[str]) -> Dict[str, List[int]]:
    """{mesh transform: vertex ids} for a spec of meshes and components."""
    _require_maya()
    out: Dict[str, List[int]] = {}
    for item in spec:
        node = item.split(".")[0]
        if not cmds.objExists(node):
            raise RuntimeError(f"{item} is not in the scene")
        node = _transform(node)
        if "." in item:
            verts = cmds.ls(cmds.polyListComponentConversion(item, toVertex=True), flatten=True) or []
            ids = [int(v[v.rindex("[") + 1:-1]) for v in verts]
        else:
            ids = list(range(cmds.polyEvaluate(node, vertex=True)))
        out.setdefault(node, [])
        out[node] = sorted(set(out[node]) | set(ids))
    return out


def mesh_points(mesh: str) -> List[core.Vec3]:
    """All vertex positions of a mesh in world space."""
    import maya.api.OpenMaya as om  # type: ignore

    sel = om.MSelectionList()
    sel.add(mesh)
    return [(p.x, p.y, p.z) for p in om.MFnMesh(sel.getDagPath(0)).getPoints(om.MSpace.kWorld)]


def spec_points(spec: Sequence[str]) -> List[List[core.Vec3]]:
    """World positions of a spec, one list per mesh (two eye objects give two lists)."""
    groups = []
    for mesh, ids in spec_vertices(spec).items():
        pts = mesh_points(mesh)
        groups.append([pts[i] for i in ids])
    return groups


def plain_material_where_missing(meshes: Sequence[str], log=print) -> List[str]:
    """Meshes whose materials have no shader show solid green in the viewport: those get a plain lambert, a bit
    whiter than an untextured face. A mesh with any real material is left as it is. Returns the meshes changed."""
    _require_maya()
    changed = []
    for mesh in meshes:
        shapes = cmds.listRelatives(mesh, shapes=True, noIntermediate=True, fullPath=True) or []
        groups = sorted({g for s in shapes for g in cmds.listConnections(s, type="shadingEngine") or []})
        if not groups or any(cmds.listConnections(g + ".surfaceShader") for g in groups):
            continue
        if not cmds.objExists(PARTS_MATERIAL):
            node = cmds.shadingNode("lambert", asShader=True, name=PARTS_MATERIAL)
            cmds.setAttr(node + ".color", *PARTS_COLOUR, type="double3")
            group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=PARTS_MATERIAL + "SG")
            cmds.connectAttr(node + ".outColor", group + ".surfaceShader")
        cmds.sets(mesh, edit=True, forceElement=PARTS_MATERIAL + "SG")
        changed.append(mesh)
    if changed:
        if not cmds.about(batch=True):
            cmds.ogs(reset=True)  # the viewport can keep drawing the old material, in solid green, until it is reset
        log(f"{', '.join(changed)}: their materials have no shader, so they get a plain lambert ({PARTS_MATERIAL})")
    return changed


def mesh_shells(mesh: str, ids: Optional[Sequence[int]] = None) -> List[List[int]]:
    """The connected pieces of a mesh, as vertex ids: of the vertices `ids` only, when given."""
    edges = mesh_edges(mesh)
    wanted = set(ids) if ids is not None else None
    parent: Dict[int, int] = {}

    def find(a: int) -> int:
        parent.setdefault(a, a)
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for a, b in edges.tolist():
        if wanted is None or (a in wanted and b in wanted):
            parent[find(a)] = find(b)
    for i in (wanted if wanted is not None else ()):
        find(i)
    groups: Dict[int, List[int]] = {}
    for i in sorted(parent):
        groups.setdefault(find(i), []).append(i)
    return list(groups.values())


def set_rigid(mesh: str, by_joint: Dict[str, Sequence[int]]) -> None:
    """These vertices of a skinned mesh follow their one joint and nothing else."""
    import maya.api.OpenMaya as om  # type: ignore

    names, weights, (fn, path, obj) = _skin_weights(mesh)
    for joint, ids in by_joint.items():
        ids = list(ids)
        weights[ids] = 0.0
        weights[ids, names.index(joint)] = 1.0
    fn.setWeights(path, obj, om.MIntArray(list(range(len(names)))), om.MDoubleArray(weights.ravel().tolist()), False)


def copy_part_skin(source_mesh: str, target_mesh: str, vertex_ids: Sequence[int]) -> None:
    """Weights of `vertex_ids` of the target taken from `source_mesh` (closest point), e.g. an eyeball."""
    _require_maya()
    src_sc, dst_sc = _skin_cluster(source_mesh), _skin_cluster(target_mesh)
    if not src_sc or not dst_sc or not vertex_ids:
        return
    have = set(cmds.skinCluster(dst_sc, q=True, influence=True))
    missing = [j for j in cmds.skinCluster(src_sc, q=True, influence=True) if j not in have]
    if missing:
        cmds.skinCluster(dst_sc, edit=True, addInfluence=missing, weight=0.0)
    sel = cmds.ls(selection=True)
    try:
        cmds.select(source_mesh, replace=True)
        cmds.select([f"{target_mesh}.vtx[{i}]" for i in vertex_ids], add=True)
        cmds.copySkinWeights(noMirror=True, surfaceAssociation="closestPoint", influenceAssociation=["oneToOne", "name"], normalize=True)
    finally:
        cmds.select(sel, replace=True) if sel else cmds.select(clear=True)


def export_head_without(mesh: str, vertex_ids: Sequence[int], path: str) -> Optional[List[int]]:
    """Export `mesh` as the TopoTransfer Reference without the faces of `vertex_ids` (picked eyes, teeth).
    Returns old vertex id -> OBJ vertex id (-1 = cut out), or None when nothing was cut."""
    _require_maya()
    if not vertex_ids:
        export_mesh_obj(mesh, path)
        return None
    dup = cmds.duplicate(mesh, name=f"{mesh}_metaMutantReference")[0]
    try:
        before = mesh_points(dup)
        faces = cmds.polyListComponentConversion([f"{dup}.vtx[{i}]" for i in vertex_ids], toFace=True, internal=True)
        if faces:
            cmds.delete(faces)
        export_mesh_obj(dup, path)
        return vertex_map(before, mesh_points(dup))
    finally:
        cmds.delete(dup)


def vertex_map(before: Sequence[core.Vec3], after: Sequence[core.Vec3]) -> List[int]:
    """Old id -> new id after faces were deleted: Maya keeps the surviving vertices in order, so walk both lists."""
    out = [-1] * len(before)
    k = 0
    for i, p in enumerate(before):
        if k < len(after) and p == after[k]:
            out[i] = k
            k += 1
    if k != len(after):
        raise RuntimeError("could not follow the vertices of the Reference after cutting out the eyes and teeth")
    return out


#: how far a scale may be from 1 and still count as 1
SCALE_TOLERANCE = 1e-4


def scale_problems(meshes: Sequence[str]) -> List[Tuple[str, Tuple[float, float, float]]]:
    """(mesh, world scale) of every mesh whose world scale is not 1, its parents' scale included."""
    _require_maya()
    out = []
    for mesh in meshes:
        node = mesh.split(".")[0]
        if not cmds.objExists(node):
            continue
        scale = cmds.xform(_transform(node), query=True, worldSpace=True, scale=True)
        if any(abs(s - 1.0) > SCALE_TOLERANCE for s in scale):
            out.append((_transform(node), tuple(scale)))
    return out


def freeze_blockers(meshes: Sequence[str]) -> List[str]:
    """Why these meshes cannot be frozen, for the artist: deformers (freezing would break them), locks, references."""
    _require_maya()
    out = []
    for mesh in meshes:
        for node in _scaled_chain(mesh):
            if cmds.referenceQuery(node, isNodeReferenced=True):
                out.append(f"{node} comes from a reference")
                continue
            for axis in "xyz":
                plug = f"{node}.s{axis}"
                if cmds.getAttr(plug, lock=True) or cmds.listConnections(plug, source=True, destination=False):
                    out.append(f"{plug} is locked or connected")
                    break
            for shape in cmds.listRelatives(node, allDescendents=True, type="mesh", fullPath=True) or []:
                deformers = [d for d in cmds.listHistory(shape, pruneDagObjects=True) or []
                             if "geometryFilter" in cmds.nodeType(d, inherited=True)]
                if deformers:
                    out.append(f"{shape.split('|')[-1]} has a deformer ({deformers[0]})")
    return sorted(set(out))


def _scaled_chain(mesh: str) -> List[str]:
    """The mesh and its parents that have a scale of their own, top first: what a freeze has to touch."""
    node = _transform(mesh.split(".")[0])
    chain = cmds.ls(node, long=True)[0].split("|")[1:]
    paths = ["|" + "|".join(chain[:i + 1]) for i in range(len(chain))]
    return [p for p in paths if any(abs(s - 1.0) > SCALE_TOLERANCE for s in cmds.getAttr(p + ".scale")[0])]


def freeze_scale(meshes: Sequence[str]) -> List[str]:
    """Freeze the scale of these meshes and of whichever parents scale them; nothing moves in the view.
    Returns the transforms frozen. One undo."""
    _require_maya()
    frozen: List[str] = []
    cmds.undoInfo(openChunk=True, chunkName="Meta Mutant: freeze scale")
    try:
        for mesh in meshes:
            for node in _scaled_chain(mesh):  # top first: freezing a parent pushes its scale into the children
                cmds.makeIdentity(node, apply=True, translate=False, rotate=False, scale=True, normal=0, preserveNormals=True)
                frozen.append(node)
    finally:
        cmds.undoInfo(closeChunk=True)
    return frozen


def nearest_mesh(points: Sequence[core.Vec3], meshes: Sequence[str]) -> str:
    """Of `meshes`, the one whose centre is nearest the centre of `points` (which eyeball is which)."""
    c = core.centroid(points)
    return min(meshes, key=lambda m: sum((a - b) ** 2 for a, b in zip(core.centroid(mesh_points(m)), c)))
