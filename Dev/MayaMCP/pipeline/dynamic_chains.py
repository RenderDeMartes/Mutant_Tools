"""Dynamic skirt/loincloth (generic): joint chains on cloth panels, skin from the chains, and a baked Verlet
simulation with capsule collision against the legs. Export-safe: the result is plain joint animation."""
import numpy as np, maya.cmds as c, maya.api.OpenMaya as om, maya.api.OpenMayaAnim as oma
try:
    from . import corrective_inversion as G
except ImportError:
    import corrective_inversion as G
def wpos(n): return np.array(c.xform(n, q=True, ws=True, t=True))
def wmat(n): return np.array(c.xform(n, q=True, ws=True, m=True)).reshape(4, 4)
def build_chains(mesh, parent, columns, top_y, joints_per_chain=4, prefix='skirt'):
    """columns: list of (name, x, side) where side +1 front / -1 back; chain runs from top_y down to the hem"""
    P = G.world(mesh); chains = {}
    for name, x, side in columns:
        sel = P[(np.abs(P[:, 0] - x) < 2.0) & (np.sign(P[:, 2] - np.median(P[:, 2])) == side)] if side else P[np.abs(P[:, 0] - x) < 2.0]
        if not len(sel): continue
        ybot = sel[:, 1].min(); ys = np.linspace(top_y, ybot, joints_per_chain + 1)
        pts = []
        for y in ys:
            band = sel[np.abs(sel[:, 1] - y) < 1.5]
            p = band.mean(0) if len(band) else sel[np.argmin(np.abs(sel[:, 1] - y))]
            pts.append(p)
        js = []; par = parent
        for i, p in enumerate(pts):
            c.select(cl=True); j = c.joint(n='%s_%s_%02d' % (prefix, name, i)); c.parent(j, par); c.xform(j, ws=True, t=[float(v) for v in p])
            c.setAttr(j + '.radius', 0.6); js.append(j); par = j
        for j, nxt in zip(js[:-1], js[1:]):        # orient each joint down its chain
            c.joint(j, e=True, oj='xyz', sao='zup', ch=False, zso=True)
        c.setAttr(js[-1] + '.jo', 0, 0, 0)
        chains[name] = js
    return chains
def skin_to_chains(mesh, sc, chains, parent, fade_top=(112.0, 106.0)):
    P = G.world(mesh); n = len(P)
    for js in chains.values():
        for j in js:
            if j not in c.skinCluster(sc, q=True, inf=True): c.skinCluster(sc, e=True, ai=j, wt=0, lw=True)
    for j in c.skinCluster(sc, q=True, inf=True): c.setAttr(j + '.liw', 0)
    sl = om.MSelectionList(); sl.add(sc); fn = oma.MFnSkinCluster(sl.getDependNode(0)); names = [p.partialPathName() for p in fn.influenceObjects()]
    col = {k: i for i, k in enumerate(names)}; W = np.zeros((n, len(names)))
    seg = []                                         # every chain segment, as (j, a, b)
    for js in chains.values():
        for i in range(len(js) - 1): seg.append((js[i], wpos(js[i]), wpos(js[i + 1])))
    for v in range(n):
        p = P[v]; d = []
        for j, a, b in seg:
            ab = b - a; t = np.clip(np.dot(p - a, ab) / np.dot(ab, ab), 0, 1); d.append(np.linalg.norm(p - (a + t * ab)))
        d = np.array(d); o = np.argsort(d)[:3]; w = 1 / (d[o] + 0.5) ** 3; w /= w.sum()
        top = np.clip((p[1] - fade_top[1]) / (fade_top[0] - fade_top[1]), 0, 1)
        for k, wi in zip(o, w): W[v, col[seg[k][0]]] += wi * (1 - top)
        W[v, col[parent]] += top
    W /= W.sum(1, keepdims=True)
    cp = om.MFnSingleIndexedComponent(); co = cp.create(om.MFn.kMeshVertComponent); cp.setCompleteData(n)
    fn.setWeights(G.dag(mesh), co, om.MIntArray(list(range(len(names)))), om.MDoubleArray(W.flatten().tolist()), False)
def capsule_push(p, a, b, r):
    ab = b - a; t = np.clip(np.dot(p - a, ab) / np.dot(ab, ab), 0, 1); q = a + t * ab; d = p - q; dl = np.linalg.norm(d)
    if dl < r and dl > 1e-6: return q + d / dl * r
    return p
def simulate(chains, parent, capsules, spheres, f0, f1, gravity=-980.0, damping=0.92, stiffness=0.08, iters=6, fps=30.0, thickness=1.2):
    """capsules: list of (jointA, jointB, radius); spheres: list of (joint, offset(3), radius). Keys the chain joints."""
    dt = 1.0 / fps
    c.currentTime(f0)
    Minv0 = np.linalg.inv(wmat(parent))
    rest = {k: [np.r_[wpos(j), 1] @ Minv0 for j in js] for k, js in chains.items()}       # chain points in parent space
    L = {k: [np.linalg.norm(wpos(js[i + 1]) - wpos(js[i])) for i in range(len(js) - 1)] for k, js in chains.items()}
    X = {k: [wpos(j) for j in js] for k, js in chains.items()}; Xp = {k: [x.copy() for x in v] for k, v in X.items()}
    # rest calibration: a collider may never push a particle that is already resting on it (cloth sits on the thighs)
    def seg_dist(p, a, b):
        ab = b - a; t = np.clip(np.dot(p - a, ab) / np.dot(ab, ab), 0, 1); return np.linalg.norm(p - (a + t * ab))
    caps0 = [(wpos(a), wpos(b)) for a, b, r in capsules]
    RC = {k: [[min(r + thickness, seg_dist(x, A, Bb) - 0.1) for (a, b, r), (A, Bb) in zip(capsules, caps0)] for x in X[k]] for k in chains}
    sph0 = [(np.r_[off, 1] @ wmat(j))[:3] for j, off, r in spheres]
    RS = {k: [[min(r + thickness, np.linalg.norm(x - cc) - 0.1) for (j, off, r), cc in zip(spheres, sph0)] for x in X[k]] for k in chains}
    for f in range(f0, f1 + 1):
        c.currentTime(f); M = wmat(parent)
        caps = [(wpos(a), wpos(b)) for a, b, r in capsules]
        sph = [(np.r_[off, 1] @ wmat(j))[:3] for j, off, r in spheres]
        for k, js in chains.items():
            tgt = [(rp @ M)[:3] for rp in rest[k]]
            x, xp = X[k], Xp[k]
            for i in range(len(js)):
                if i == 0: xp[i] = x[i] = tgt[0]; continue
                v = (x[i] - xp[i]) * damping
                nx = x[i] + v + np.array([0, gravity, 0]) * dt * dt * 0.25 + stiffness * (tgt[i] - x[i])
                xp[i] = x[i]; x[i] = nx
            for _ in range(iters):
                for i in range(len(js) - 1):           # segment lengths, root fixed
                    a, b = x[i], x[i + 1]; d = b - a; dl = np.linalg.norm(d) + 1e-9; corr = d * (1 - L[k][i] / dl)
                    if i == 0: x[i + 1] = b - corr
                    else: x[i] = a + corr * 0.5; x[i + 1] = b - corr * 0.5
                for i in range(1, len(js)):
                    for ci, (a, b) in enumerate(caps): x[i] = capsule_push(x[i], a, b, RC[k][i][ci])
                    for si, cc in enumerate(sph):
                        r = RS[k][i][si]; d = x[i] - cc; dl = np.linalg.norm(d)
                        if dl < r: x[i] = cc + d / dl * r
            for i in range(len(js) - 1):               # minimal rotation from where the child is now to the simulated point
                j = js[i]; cur = wmat(j); pos = cur[3, :3]
                now = wpos(js[i + 1]) - pos; want = x[i + 1] - pos
                q = om.MQuaternion(om.MVector(*now).normal(), om.MVector(*want).normal())
                R = np.array(q.asMatrix()).reshape(4, 4)
                m = cur.copy(); m[:3, :3] = cur[:3, :3] @ R[:3, :3]; m[3, :3] = pos
                c.xform(j, ws=True, m=[float(v) for v in m.flatten()])
                c.setKeyframe(j, at=['rx', 'ry', 'rz'], t=f)
    return True
