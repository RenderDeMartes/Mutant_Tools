from __future__ import absolute_import
'''
content: skin long meshes to joint chains, one chain per mesh. Every mesh is read from a view (top by
         default): its long axis gives two ends, the root is the end closest to the chain bases. Meshes
         and chains are matched one to one (best total, some pairs can be not perfect) and every mesh is
         skinned to its chain only, vertices blended between the two chain joints around them.
version: 1.0.0
date: 19/10/2026

how to:
try:
    import importlib;from importlib import reload
except:
    import imp;from imp import reload

import Mutant_Tools
from Mutant_Tools.Utils.IO import ChainSkin
reload(ChainSkin)

# chains: lists of joints, base first
pairs = ChainSkin.skin_meshes_to_chains(meshes=['meshA', 'meshB'],
                                        chains=[['jntA', 'jntA1', 'jntA2'], ['jntB', 'jntB1', 'jntB2']])
# only the matching, nothing skinned
pairs = ChainSkin.match_meshes_to_chains(meshes, chains)
# chains shared, every mesh to its best chain
pairs = ChainSkin.skin_meshes_to_chains(meshes, chains, unique=False)

dependencies:
cmds, OpenMaya 2

www.mutanttools.com
author:  Esteban Rodriguez <info@mutanttools.com>
'''

import math

from maya import cmds
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma

AXES = {'x': 0, 'y': 1, 'z': 2}


def _plane(view_axis):
    """The two axes seen when looking down view_axis (y: top view, x z)."""
    return [axis for axis in range(3) if axis != AXES[view_axis]]


def _dag(node):
    sel = om.MSelectionList()
    sel.add(node)
    return sel.getDagPath(0)


def mesh_points(mesh):
    return [om.MVector(p) for p in om.MFnMesh(_dag(mesh)).getPoints(om.MSpace.kWorld)]


def joint_position(joint):
    return om.MVector(*cmds.xform(joint, q=True, ws=True, t=True))


def _flat(point, plane):
    return (point[plane[0]], point[plane[1]])


def _flat_distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def mesh_ends(mesh, view_axis='y'):
    """The two ends of the mesh along its long axis as seen from view_axis (world points of the
    vertices furthest each way) and the length seen."""
    points = mesh_points(mesh)
    plane = _plane(view_axis)
    flat = [_flat(p, plane) for p in points]
    count = float(len(flat))
    cu = sum(p[0] for p in flat) / count
    cv = sum(p[1] for p in flat) / count
    suu = sum((p[0] - cu) ** 2 for p in flat)
    svv = sum((p[1] - cv) ** 2 for p in flat)
    suv = sum((p[0] - cu) * (p[1] - cv) for p in flat)
    angle = 0.5 * math.atan2(2 * suv, suu - svv)
    du, dv = math.cos(angle), math.sin(angle)
    along = [(p[0] - cu) * du + (p[1] - cv) * dv for p in flat]
    low = min(range(len(along)), key=lambda i: along[i])
    high = max(range(len(along)), key=lambda i: along[i])
    return points[low], points[high], along[high] - along[low]


def mesh_root(mesh, anchors, view_axis='y'):
    """(root, tip) of the mesh: the end closest (seen from view_axis) to any of the anchors is the root."""
    plane = _plane(view_axis)
    first, second, length = mesh_ends(mesh, view_axis)
    anchors = [_flat(a, plane) for a in anchors]

    def gap(point):
        return min(_flat_distance(_flat(point, plane), a) for a in anchors)
    return (first, second) if gap(first) <= gap(second) else (second, first)


def _hungarian(cost):
    """Rows to columns, one to one, smallest total cost (rows <= columns). Returns the column of each row."""
    rows, cols = len(cost), len(cost[0])
    inf = float('inf')
    u = [0.0] * (rows + 1)
    v = [0.0] * (cols + 1)
    match = [0] * (cols + 1)
    way = [0] * (cols + 1)
    for row in range(1, rows + 1):
        match[0] = row
        col0 = 0
        minv = [inf] * (cols + 1)
        used = [False] * (cols + 1)
        while True:
            used[col0] = True
            row0 = match[col0]
            delta = inf
            col1 = 0
            for col in range(1, cols + 1):
                if used[col]:
                    continue
                current = cost[row0 - 1][col - 1] - u[row0] - v[col]
                if current < minv[col]:
                    minv[col] = current
                    way[col] = col0
                if minv[col] < delta:
                    delta = minv[col]
                    col1 = col
            for col in range(cols + 1):
                if used[col]:
                    u[match[col]] += delta
                    v[col] -= delta
                else:
                    minv[col] -= delta
            col0 = col1
            if match[col0] == 0:
                break
        while col0:
            col1 = way[col0]
            match[col0] = match[col1]
            col0 = col1
    result = [None] * rows
    for col in range(1, cols + 1):
        if match[col]:
            result[match[col] - 1] = col - 1
    return result


def match_meshes_to_chains(meshes, chains, view_axis='y', direction_weight=0.5, unique=True):
    """One chain per mesh, no chain used twice (unique, else every mesh takes its best chain and many
    meshes can share one), the best total fit. The fit of a pair, seen from
    view_axis: distance from the mesh root to the chain base, plus how much the mesh (root to tip) and
    the chain (base to last joint) point other ways (direction_weight * mesh length * (1 - cos)).

    Returns a list of dicts (mesh, chain, root_gap, angle) in the meshes order, chain None when there are
    more meshes than chains."""
    plane = _plane(view_axis)
    bases = [joint_position(chain[0]) for chain in chains]
    lasts = [joint_position(chain[-1]) for chain in chains]
    flat_bases = [_flat(b, plane) for b in bases]
    chain_dirs = []
    for base, last in zip(flat_bases, lasts):
        last = _flat(last, plane)
        chain_dirs.append(_unit2(last[0] - base[0], last[1] - base[1]))

    infos = []
    cost = []
    for mesh in meshes:
        root, tip = mesh_root(mesh, bases, view_axis)
        root_flat, tip_flat = _flat(root, plane), _flat(tip, plane)
        length = _flat_distance(root_flat, tip_flat)
        mesh_dir = _unit2(tip_flat[0] - root_flat[0], tip_flat[1] - root_flat[1])
        row = []
        for base, chain_dir in zip(flat_bases, chain_dirs):
            dot = mesh_dir[0] * chain_dir[0] + mesh_dir[1] * chain_dir[1]
            row.append(_flat_distance(root_flat, base) + direction_weight * length * (1.0 - dot))
        cost.append(row)
        infos.append((root_flat, mesh_dir))

    if unique:
        # more meshes than chains: extra columns nobody wants, those meshes stay without chain
        width = max(len(chains), len(meshes))
        padded = [row + [1e9] * (width - len(chains)) for row in cost]
        columns = _hungarian(padded)
    else:
        columns = [min(range(len(row)), key=lambda col: row[col]) for row in cost]

    pairs = []
    for mesh, column, (root_flat, mesh_dir) in zip(meshes, columns, infos):
        if column is None or column >= len(chains):
            pairs.append({'mesh': mesh, 'chain': None, 'root_gap': None, 'angle': None})
            continue
        chain_dir = chain_dirs[column]
        dot = max(-1.0, min(1.0, mesh_dir[0] * chain_dir[0] + mesh_dir[1] * chain_dir[1]))
        pairs.append({'mesh': mesh, 'chain': chains[column],
                      'root_gap': _flat_distance(root_flat, flat_bases[column]),
                      'angle': math.degrees(math.acos(dot))})
    return pairs


def _unit2(u, v):
    length = math.hypot(u, v)
    return (u / length, v / length) if length > 1e-9 else (0.0, 0.0)


def chain_weights(points, joint_points):
    """Per point, {joint index: weight}: the point goes on the closest chain segment and blends between
    its two joints. Before the base it is all base, past the last joint all the last joint."""
    if len(joint_points) == 1:
        return [{0: 1.0} for _ in points]
    weights = []
    segments = list(zip(joint_points[:-1], joint_points[1:]))
    for point in points:
        best = None
        for index, (start, end) in enumerate(segments):
            span = end - start
            length2 = span * span
            t = ((point - start) * span) / length2 if length2 > 1e-12 else 0.0
            # only the ends of the chain go past their joint
            low = -float('inf') if index == 0 else 0.0
            high = float('inf') if index == len(segments) - 1 else 1.0
            t = max(low, min(high, t))
            distance = (point - (start + span * t)).length()
            if best is None or distance < best[0]:
                best = (distance, index, t)
        distance, index, t = best
        t = max(0.0, min(1.0, t))
        if t < 1e-6:
            weights.append({index: 1.0})
        elif t > 1.0 - 1e-6:
            weights.append({index + 1: 1.0})
        else:
            weights.append({index: 1.0 - t, index + 1: t})
    return weights


def _skin_cluster(mesh):
    return (cmds.ls(cmds.listHistory(mesh, pdo=True) or [], type='skinCluster') or [None])[0]


def skin_mesh_to_chain(mesh, chain, replace=True):
    """Skin mesh to the chain joints only, blended along the chain (chain_weights)."""
    old = _skin_cluster(mesh)
    if old:
        if not replace:
            cmds.warning('{} has {} already, skipped'.format(mesh, old))
            return old
        cmds.skinCluster(old, e=True, ub=True)
    name = mesh.split('|')[-1] + '_SkinCluster'
    skin = cmds.skinCluster(chain, mesh, tsb=True, mi=2, n=name)[0]

    weights = chain_weights(mesh_points(mesh), [joint_position(j) for j in chain])
    fn_skin = oma.MFnSkinCluster(om.MSelectionList().add(skin).getDependNode(0))
    # influence order of the skinCluster to chain order
    influences = [path.fullPathName() for path in fn_skin.influenceObjects()]
    to_influence = [influences.index(_dag(joint).fullPathName()) for joint in chain]

    shape = _dag(mesh)
    shape.extendToShape()
    component = om.MFnSingleIndexedComponent()
    vertices = component.create(om.MFn.kMeshVertComponent)
    component.setCompleteData(len(weights))
    values = om.MDoubleArray(len(weights) * len(influences), 0.0)
    for vertex, vertex_weights in enumerate(weights):
        for joint_index, weight in vertex_weights.items():
            values[vertex * len(influences) + to_influence[joint_index]] = weight
    fn_skin.setWeights(shape, vertices, om.MIntArray(list(range(len(influences)))), values, False)
    return skin


def skin_meshes_to_chains(meshes, chains, view_axis='y', direction_weight=0.5, unique=True, replace=True, report=True):
    """match_meshes_to_chains then skin_mesh_to_chain for every pair. Returns the pairs."""
    pairs = match_meshes_to_chains(meshes, chains, view_axis, direction_weight, unique)
    for pair in pairs:
        if pair['chain'] is None:
            cmds.warning('{}: no chain left for it, not skinned'.format(pair['mesh']))
            continue
        pair['skin'] = skin_mesh_to_chain(pair['mesh'], pair['chain'], replace)
        if report:
            print('{} -> {}  root gap {:.2f}  angle {:.1f}'.format(pair['mesh'], pair['chain'][0], pair['root_gap'], pair['angle']))
    return pairs
