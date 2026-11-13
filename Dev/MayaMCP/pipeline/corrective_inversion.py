"""Corrective-shape helpers: ring topology around holes, world points, and pre-skin corrective inversion."""
import maya.cmds as c, maya.api.OpenMaya as om, numpy as np
MESH, BS = 'body_geo', 'face_bs'      # defaults: set corrective_inversion.MESH / .BS for your asset

def dag(mesh=MESH):
    s = om.MSelectionList(); s.add(mesh); return s.getDagPath(0)

def world(mesh=MESH, idx=None):
    P = om.MFnMesh(dag(mesh)).getPoints(om.MSpace.kWorld)
    A = np.array([[p.x, p.y, p.z] for p in P])
    return A if idx is None else A[idx]

def neighbours(mesh=MESH):
    it = om.MItMeshVertex(dag(mesh)); nb = {}
    while not it.isDone():
        nb[it.index()] = list(it.getConnectedVertices()); it.next()
    return nb

def border_loops(mesh=MESH):
    it = om.MItMeshEdge(dag(mesh)); adj = {}
    while not it.isDone():
        if it.onBoundary():
            a, b = it.vertexId(0), it.vertexId(1)
            adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)
        it.next()
    seen, loops = set(), []
    for v in adj:
        if v in seen: continue
        comp, st = [], [v]
        while st:
            x = st.pop()
            if x in seen: continue
            seen.add(x); comp.append(x); st.extend(adj[x])
        loops.append(comp)
    return loops

def order_ring(verts, nb):
    S = set(verts); start = verts[0]; order = [start]; prev = None
    while True:
        cand = [n for n in nb[order[-1]] if n in S and n != prev and n not in order[1:]]
        if not cand: break
        nxt = cand[0]
        if nxt == start: break
        prev = order[-1]; order.append(nxt)
        if len(order) > len(S): break
    return order

def rings(border, nb, n):
    """BFS layers outward from a hole border."""
    out = [list(border)]; seen = set(border)
    for _ in range(n):
        nxt = sorted({y for x in out[-1] for y in nb[x] if y not in seen})
        seen.update(nxt); out.append(nxt)
    return out

def split_ring(order, P):
    """split a closed ordered ring at its min-x and max-x vertices -> (upper, lower), each ordered from -x to +x."""
    xs = P[order, 0]; i0, i1 = int(np.argmin(xs)), int(np.argmax(xs))
    n = len(order)
    def path(a, b):
        out = [order[a]]; k = a
        while k != b: k = (k + 1) % n; out.append(order[k])
        return out
    p1, p2 = path(i0, i1), path(i1, i0)[::-1]
    if P[p1[1:-1], 1].mean() >= P[p2[1:-1], 1].mean(): return p1, p2
    return p2, p1

def arc_u(path, P):
    seg = np.linalg.norm(np.diff(P[path], axis=0), axis=1)
    u = np.r_[0, np.cumsum(seg)]; return u / u[-1]

def interp_path(path, P, u):
    uu = arc_u(path, P); Q = P[path]
    return np.stack([np.interp(u, uu, Q[:, k]) for k in range(3)], 1)

def mesh_inv3(mesh=MESH):
    m = om.MMatrix(c.xform(mesh, q=True, ws=True, m=True))
    M = np.array([[m.getElement(r, k) for k in range(3)] for r in range(3)])
    return np.linalg.inv(M)

def target_plug(idx, bs=BS, item=6000):
    return '%s.inputTarget[0].inputTargetGroup[%d].inputTargetItem[%d]' % (bs, idx, item)

def set_deltas(idx, verts, D, bs=BS, item=6000):
    order = np.argsort(verts); v = np.asarray(verts)[order]; D = np.asarray(D)[order]
    p = target_plug(idx, bs, item)
    c.setAttr(p + '.inputPointsTarget', len(v), *[(float(a), float(b), float(cc), 1.0) for a, b, cc in D], type='pointArray')
    c.setAttr(p + '.inputComponentsTarget', len(v), *['vtx[%d]' % i for i in v], type='componentList')

def new_target(name, bs=BS):
    al = c.aliasAttr(bs, q=True) or []
    if name in al[0::2]:
        return int(al[al.index(name) + 1].split('[')[1].rstrip(']'))
    used = c.getAttr(bs + '.weight', mi=True) or []
    idx = max(used) + 1 if used else 0
    c.setAttr('%s.weight[%d]' % (bs, idx), 0)
    c.aliasAttr(name, '%s.weight[%d]' % (bs, idx))
    return idx

def invert_corrective(name, verts, target_world, iters=2, bs=BS, mesh=MESH, item=6000):
    """Pre-skin deltas so that, in the CURRENT pose with this corrective at weight item/1000-5, verts land on
    target_world. Skinning is linear in the pre-skin position, so each vertex's 3x3 map is measured with three
    probe deltas and solved exactly (works at any joint rotation; the old fixed-point loop diverged past ~60 deg).
    item 6000 = full target, 5500 = in-between at weight 0.5."""
    idx = new_target(name, bs)
    w = '%s.weight[%d]' % (bs, idx)
    for cn in c.listConnections(w, s=True, d=False, p=True) or []:
        c.disconnectAttr(cn, w)
    c.setAttr(w, (item - 5000) / 1000.0)
    verts = list(verts); nv = len(verts); T = np.asarray(target_world, float)
    Z = np.zeros((nv, 3)); set_deltas(idx, verts, Z, bs, item); X0 = world(mesh, verts)
    J = np.zeros((nv, 3, 3)); h = 0.05
    for k in range(3):
        E = np.zeros((nv, 3)); E[:, k] = h
        set_deltas(idx, verts, E, bs, item); J[:, :, k] = (world(mesh, verts) - X0) / h
    D = np.linalg.solve(J + np.eye(3)[None] * 1e-9, (T - X0)[:, :, None])[:, :, 0]
    set_deltas(idx, verts, D, bs, item)
    for _ in range(iters):   # tiny refinements (numerical noise only)
        err = T - world(mesh, verts)
        D = D + np.linalg.solve(J + np.eye(3)[None] * 1e-9, err[:, :, None])[:, :, 0]
        set_deltas(idx, verts, D, bs, item)
    res = np.linalg.norm(T - world(mesh, verts), axis=1)
    return idx, float(res.max()), float(res.mean())

def drive(bs_weight, src_plug, lo, hi, name):
    """weight = smoothstep(lo..hi) of src_plug via remapValue"""
    rm = name + '_remap'
    if not c.objExists(rm):
        rm = c.createNode('remapValue', n=rm)
    c.setAttr(rm + '.inputMin', lo); c.setAttr(rm + '.inputMax', hi)
    c.setAttr(rm + '.value[0].value_Position', 0); c.setAttr(rm + '.value[0].value_FloatValue', 0); c.setAttr(rm + '.value[0].value_Interp', 2)
    c.setAttr(rm + '.value[1].value_Position', 1); c.setAttr(rm + '.value[1].value_FloatValue', 1); c.setAttr(rm + '.value[1].value_Interp', 2)
    if not c.isConnected(src_plug, rm + '.inputValue'): c.connectAttr(src_plug, rm + '.inputValue', f=True)
    c.connectAttr(rm + '.outValue', bs_weight, f=True)
    return rm

def fit_sphere(P):
    A = np.c_[2 * P, np.ones(len(P))]; b = (P ** 2).sum(1)
    x = np.linalg.lstsq(A, b, rcond=None)[0]
    ctr = x[:3]; return ctr, float(np.sqrt(x[3] + ctr @ ctr))

def clear_target(name, bs=BS):
    al = c.aliasAttr(bs, q=True) or []
    if name not in al[0::2]: return
    idx = int(al[al.index(name) + 1].split('[')[1].rstrip(']'))
    w = bs + '.' + name
    for cn in c.listConnections(w, s=True, d=False, p=True) or []: c.disconnectAttr(cn, w)
    c.setAttr(w, 0)
    for it in c.getAttr('%s.inputTarget[0].inputTargetGroup[%d].inputTargetItem' % (bs, idx), mi=True) or []:
        c.removeMultiInstance('%s.inputTarget[0].inputTargetGroup[%d].inputTargetItem[%d]' % (bs, idx, it), b=True)

def drive_linear(bs_weight, src_plug, name):
    cl = name + '_clamp'
    if not c.objExists(cl): cl = c.createNode('clamp', n=cl)
    c.setAttr(cl + '.minR', 0); c.setAttr(cl + '.maxR', 1)
    if not c.isConnected(src_plug, cl + '.inputR'): c.connectAttr(src_plug, cl + '.inputR', f=True)
    c.connectAttr(cl + '.outputR', bs_weight, f=True)
    return cl
