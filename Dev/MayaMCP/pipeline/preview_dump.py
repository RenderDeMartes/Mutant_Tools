"""mayapy helper: grab posed meshes (world points + faces + material colour per face) for soft_render.py."""
import numpy as np, maya.cmds as c, maya.api.OpenMaya as om
_cache = {}
def mesh_data(mesh):
    if mesh in _cache: return _cache[mesh]
    sl = om.MSelectionList(); sl.add(mesh); dag = sl.getDagPath(0); fn = om.MFnMesh(dag)
    F = [list(fn.getPolygonVertices(i)) for i in range(fn.numPolygons)]
    C = np.full((len(F), 3), 0.6)
    shapes = [s for s in c.listRelatives(mesh, s=True, f=True) if not c.getAttr(s + '.io')]
    for sg in set(c.listConnections(shapes[0], type='shadingEngine') or []):
        mats = c.listConnections(sg + '.surfaceShader') or []
        if not mats or not c.attributeQuery('color', node=mats[0], exists=True): continue
        col = np.array(c.getAttr(mats[0] + '.color')[0])
        for m in c.sets(sg, q=True) or []:
            if '.f[' not in m:
                if m.split('.')[0].split('|')[-1] in (mesh, shapes[0].split('|')[-1]): C[:] = col
                continue
            r = m.split('.f[')[1].rstrip(']')
            a, b = (r.split(':') + [r])[:2]; C[int(a):int(b) + 1] = col
    _cache[mesh] = (dag, F, C); return _cache[mesh]
def all_meshes():
    return [c.listRelatives(s, p=True)[0] for s in c.ls(type='mesh', noIntermediate=True)]
def grab(meshes=None):
    meshes = meshes or all_meshes(); out = []
    for m in meshes:
        if not c.objExists(m): continue
        dag, F, C = mesh_data(m)
        P = np.array([[p.x, p.y, p.z] for p in om.MFnMesh(dag).getPoints(om.MSpace.kWorld)])
        out.append((P, F, C))
    return out
def dump(path, frames, meshes=None, extra=None):
    """save posed meshes at the given frames: npz with per-mesh faces/colours and per-frame points"""
    meshes = meshes or all_meshes(); data = {}
    for k, m in enumerate(meshes):
        if not c.objExists(m): continue
        dag, F, C = mesh_data(m)
        data['m%d_counts' % k] = np.array([len(f) for f in F]); data['m%d_idx' % k] = np.concatenate([np.array(f) for f in F])
        data['m%d_col' % k] = C
    for fi, f in enumerate(frames):
        c.currentTime(f)
        for k, (P, F, C) in enumerate(grab(meshes)): data['f%d_m%d' % (fi, k)] = P.astype(np.float32)
        if extra: data['f%d_extra' % fi] = np.array(extra(), np.float32)
    data['frames'] = np.array(frames); np.savez_compressed(path, **data)
def dump_poses(path, poses, setter, meshes=None):
    """poses: list of dicts applied with setter(dict) -> npz like dump()"""
    meshes = meshes or all_meshes(); data = {}
    for k, m in enumerate(meshes):
        dag, F, C = mesh_data(m)
        data['m%d_counts' % k] = np.array([len(f) for f in F]); data['m%d_idx' % k] = np.concatenate([np.array(f) for f in F]); data['m%d_col' % k] = C
    for fi, p in enumerate(poses):
        setter(p)
        for k, (P, F, C) in enumerate(grab(meshes)): data['f%d_m%d' % (fi, k)] = P.astype(np.float32)
    data['frames'] = np.arange(len(poses)); np.savez_compressed(path, **data)
