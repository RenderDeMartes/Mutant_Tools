"""
The MetaHuman head rig in Maya, built straight from a DNA with Epic's `dna` module (the one Meta
Mutant ships for Maya 2026, built from OpenRigLogic). Replaces Epic's dna_viewer:

    import mm_rig
    built = mm_rig.build(r"C:/work/head_custom.dna")      # joints, LOD0 meshes, skin, blendshapes
    built["meshes"]   # ["head_lod0_mesh", "teeth_lod0_mesh", ...]

What it builds, as dna_viewer does without RigLogic:
* joints: each joint's neutral translation and rotation (degrees) as translate / jointOrient,
  relative to its parent, in DNA order and names;
* the LOD meshes with the DNA's UVs, vertex order kept;
* a skinCluster per skinned mesh with the DNA weights (set in bulk, not one setAttr per weight);
* a blendShape per mesh with every DNA target (deltas written straight into the node).

No RigLogic node: Epic ships no RigLogic plugin for Maya 2026. The face's behaviour (controls to
joints and shapes) stays in the DNA, for Unreal.

The readers (`joints`, `mesh_data`, `skin`, `blend_shapes`) only need a DNA reader, so they run
(and are tested) outside Maya.
"""

from __future__ import annotations

import os
import sys
from typing import Callable, Dict, List, Sequence, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mm_core as core  # noqa: E402
import mm_dna  # noqa: E402

Vec3 = Tuple[float, float, float]
ROOT = "metaMutant_rig"
GEOMETRY = "metaMutant_geometry"
SKIN_CHUNK = 2048  # vertices per bulk skin-weight write


# ----------------------------------------------------------------------------- reading (no Maya)


def joints(r) -> List[Tuple[str, int, Vec3, Vec3]]:
    """(name, parent index or -1, local translation, jointOrient in degrees) per DNA joint."""
    tx, ty, tz = r.getNeutralJointTranslationXs(), r.getNeutralJointTranslationYs(), r.getNeutralJointTranslationZs()
    rx, ry, rz = r.getNeutralJointRotationXs(), r.getNeutralJointRotationYs(), r.getNeutralJointRotationZs()
    out = []
    for j in range(r.getJointCount()):
        parent = r.getJointParentIndex(j)
        out.append((r.getJointName(j), -1 if parent == j else parent, (tx[j], ty[j], tz[j]), (rx[j], ry[j], rz[j])))
    return out


def mesh_data(r, m: int) -> dict:
    """Positions, polygon counts / connects and per-corner UV ids, as MFnMesh.create wants them."""
    geo = mm_dna.mesh_geometry(r, m)
    counts, connects, uv_ids = [], [], []
    for face in geo["faces"]:
        counts.append(len(face))
        connects.extend(p for p, _ in face)
        uv_ids.extend(t for _, t in face)
    return {
        "name": geo["name"],
        "positions": geo["positions"],
        "counts": counts,
        "connects": connects,
        "us": [u for u, _ in geo["uvs"]],
        "vs": [v for _, v in geo["uvs"]],
        "uv_ids": uv_ids,
    }


def skin(r, m: int) -> Tuple[List[int], List[List[Tuple[int, float]]]]:
    """(joints the mesh uses, sorted; per vertex [(joint, weight)]). Empty when the mesh is not skinned."""
    weights = core.read_skin(r, m) if r.getSkinWeightsCount(m) else []
    used = sorted({j for vertex in weights for j, w in vertex if w > 0.0})
    return used, weights


def blend_shapes(r, m: int) -> List[Tuple[str, List[int], List[Vec3]]]:
    """(channel name, vertex ids, deltas) per blendshape target of mesh `m`."""
    out = []
    for t in range(r.getBlendShapeTargetCount(m)):
        name = r.getBlendShapeChannelName(r.getBlendShapeChannelIndex(m, t))
        xs, ys, zs = r.getBlendShapeTargetDeltaXs(m, t), r.getBlendShapeTargetDeltaYs(m, t), r.getBlendShapeTargetDeltaZs(m, t)
        ids = list(r.getBlendShapeTargetVertexIndices(m, t))
        out.append((name, ids, [(xs[i], ys[i], zs[i]) for i in range(len(ids))]))
    return out


def unique_names(names: Sequence[str]) -> List[str]:
    """Channel names as blendShape aliases: unique per node."""
    seen: Dict[str, int] = {}
    out = []
    for n in names:
        k = seen.get(n, 0)
        seen[n] = k + 1
        out.append(n if k == 0 else f"{n}_{k}")
    return out


# ----------------------------------------------------------------------------- building (Maya)


def _maya():
    import maya.api.OpenMaya as om  # type: ignore
    import maya.api.OpenMayaAnim as oma  # type: ignore
    import maya.cmds as cmds  # type: ignore

    return cmds, om, oma


def build_joints(r, parent: str) -> List[str]:
    cmds, _, _ = _maya()
    data = joints(r)
    names = []
    for name, _, t, o in data:  # all first, then the hierarchy: parents may come after children
        node = cmds.createNode("joint", name=name, skipSelect=True)
        cmds.setAttr(node + ".translate", *t, type="double3")
        cmds.setAttr(node + ".jointOrient", *o, type="double3")
        cmds.setAttr(node + ".segmentScaleCompensate", 0)
        names.append(node)
    for (name, p, _, _), node in zip(data, names):
        cmds.parent(node, names[p] if p >= 0 else parent, relative=True)
    return names


def build_mesh(r, m: int, parent: str) -> str:
    cmds, om, _ = _maya()
    d = mesh_data(r, m)
    fn = om.MFnMesh()
    transform = fn.create(om.MPointArray([om.MPoint(*p) for p in d["positions"]]), d["counts"], d["connects"],
                          d["us"], d["vs"])
    fn.assignUVs(d["counts"], d["uv_ids"])
    node = om.MFnDependencyNode(transform).setName(d["name"])
    om.MFnDependencyNode(fn.object()).setName(d["name"] + "Shape")
    node = cmds.parent(node, parent)[0]
    cmds.sets(node, edit=True, forceElement="initialShadingGroup")
    return node


def add_blend_shapes(r, m: int, mesh: str) -> str:
    """One blendShape with every DNA target of the mesh, deltas written into the node (no target meshes)."""
    cmds, _, _ = _maya()
    shapes = blend_shapes(r, m)
    if not shapes:
        return ""
    bs = cmds.blendShape(mesh, name=f"{mesh}_blendShapes")[0]
    for i, (alias, (_, ids, deltas)) in enumerate(zip(unique_names([s[0] for s in shapes]), shapes)):
        item = f"{bs}.inputTarget[0].inputTargetGroup[{i}].inputTargetItem[6000]"
        cmds.setAttr(item + ".inputPointsTarget", len(deltas), *[(x, y, z, 1.0) for x, y, z in deltas], type="pointArray")
        cmds.setAttr(item + ".inputComponentsTarget", len(ids), *[f"vtx[{v}]" for v in ids], type="componentList")
        cmds.setAttr(f"{bs}.weight[{i}]", 0.0)
        cmds.aliasAttr(alias, f"{bs}.weight[{i}]")
    return bs


def add_skin(r, m: int, mesh: str, joint_names: Sequence[str]) -> str:
    """A skinCluster with the DNA weights, written in vertex chunks with MFnSkinCluster.setWeights."""
    cmds, om, oma = _maya()
    used, weights = skin(r, m)
    if not used:
        return ""
    influences = [joint_names[j] for j in used]
    max_inf = max(1, r.getMaximumInfluencePerVertex(m))
    sc = cmds.skinCluster(influences, mesh, toSelectedBones=True, maximumInfluences=max_inf, obeyMaxInfluences=False,
                          normalizeWeights=1, skinMethod=0, name=f"{mesh}_skinCluster")[0]
    sel = om.MSelectionList()
    sel.add(sc)
    sel.add(mesh)
    fn = oma.MFnSkinCluster(sel.getDependNode(0))
    path = sel.getDagPath(1)
    order = {p.partialPathName(): i for i, p in enumerate(fn.influenceObjects())}
    column = {j: order[joint_names[j]] for j in used}
    n_inf = len(order)
    all_infl = om.MIntArray(list(range(n_inf)))
    for start in range(0, len(weights), SKIN_CHUNK):
        chunk = weights[start:start + SKIN_CHUNK]
        values = [0.0] * (len(chunk) * n_inf)
        for k, vertex in enumerate(chunk):
            row = k * n_inf
            for j, w in vertex:
                if w > 0.0:
                    values[row + column[j]] = w
        comp = om.MFnSingleIndexedComponent()
        obj = comp.create(om.MFn.kMeshVertComponent)
        comp.addElements(list(range(start, start + len(chunk))))
        fn.setWeights(path, obj, all_infl, om.MDoubleArray(values), False)
    return sc


def build(dna_path: str, lod: int = 0, blendshapes: bool = True, log: Callable[[str], None] = print, reader=None) -> dict:
    """Build the rig from `dna_path` (replacing an earlier Meta Mutant rig). Returns the created node names."""
    cmds, _, _ = _maya()
    r = reader if reader is not None else mm_dna.load_dna(dna_path)
    if cmds.objExists(ROOT):
        cmds.delete(ROOT)
    root = cmds.group(empty=True, world=True, name=ROOT)
    geometry = cmds.group(empty=True, parent=root, name=GEOMETRY)
    joint_names = build_joints(r, root)
    log(f"{len(joint_names)} joints")
    meshes, skins, shapes = [], 0, 0
    for m in r.getMeshIndicesForLOD(lod):
        mesh = build_mesh(r, m, geometry)
        meshes.append(mesh)
        if blendshapes and add_blend_shapes(r, m, mesh):  # before the skin: shapes, then skinning
            shapes += 1
        if add_skin(r, m, mesh, joint_names):
            skins += 1
        log(f"{mesh}: {cmds.polyEvaluate(mesh, vertex=True)} vertices")
    log(f"rig built from {os.path.basename(dna_path)}: {len(meshes)} meshes, {skins} skinned, {shapes} with blendshapes")
    return {"root": root, "joints": joint_names, "meshes": meshes}
