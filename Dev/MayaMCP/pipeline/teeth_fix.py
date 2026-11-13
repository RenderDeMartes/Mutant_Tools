"""Teeth binding fix (generic): split a one-piece teeth mesh into upper and lower parts by shell and bind the lower part
(lower teeth, lower gums, tusks) to the lower-teeth joint that follows the jaw. Rest pose is unchanged."""
import numpy as np, maya.cmds as c, maya.api.OpenMaya as om, maya.api.OpenMayaAnim as oma


def _dag(n):
    sl = om.MSelectionList(); sl.add(n); d = sl.getDagPath(0); d.extendToShape(); return d


def shells(mesh):
    """connected vertex shells -> list of vertex index arrays"""
    fn = om.MFnMesh(_dag(mesh)); counts, conn = fn.getVertices(); n = fn.numVertices
    parent = list(range(n))
    def find(a):
        while parent[a] != a: parent[a] = parent[parent[a]]; a = parent[a]
        return a
    i = 0
    for k in counts:
        vs = conn[i:i + k]; i += k; r0 = find(vs[0])
        for v in vs[1:]:
            r = find(v)
            if r != r0: parent[r] = r0
    groups = {}
    for v in range(n): groups.setdefault(find(v), []).append(v)
    return [np.array(g) for g in groups.values()]


def split(mesh='teeth_geo', upper='UpperTeeth_Skl', lower='LowerTeeth_Skl', force_lower=('M_tusk',), skip=('M_tongue',)):
    """returns (upper verts, lower verts, report) - shells split in two by height (2-means on shell centres);
    shells holding any `force_lower` faces always go to the lower jaw, `skip` shells are left alone"""
    from . import mouth_guard as MG
    fn = om.MFnMesh(_dag(mesh)); P = np.array([(p.x, p.y, p.z) for p in fn.getPoints(om.MSpace.kWorld)])
    fv = lambda mats: {v for f in MG._mat_faces(mesh, mats) for v in fn.getPolygonVertices(f)}
    forced, skipped = fv(force_lower), fv(skip)
    S = [s for s in shells(mesh) if not (set(s.tolist()) & skipped)]
    cy = np.array([P[s, 1].mean() for s in S]); lo, hi = cy.min(), cy.max()
    for _ in range(20):                                               # 2-means on shell heights
        lab = np.abs(cy - lo) < np.abs(cy - hi)                        # True = lower
        lo, hi = cy[lab].mean() if lab.any() else lo, cy[~lab].mean() if (~lab).any() else hi
    up, low = [], []
    for s, isl in zip(S, lab):
        (low if (isl or (set(s.tolist()) & forced)) else up).extend(s.tolist())
    return np.array(sorted(up)), np.array(sorted(low)), dict(shells=len(S), lower_shells=int(sum(1 for s, l in zip(S, lab) if l or set(s.tolist()) & forced)),
                                                           upper_y=round(float(hi), 2), lower_y=round(float(lo), 2))


def bind_lower(mesh='teeth_geo', upper='UpperTeeth_Skl', lower='LowerTeeth_Skl', **kw):
    up, low, rep = split(mesh, upper, lower, **kw)
    sc = c.ls(c.listHistory(mesh), type='skinCluster')[0]
    infl = c.skinCluster(sc, q=True, inf=True)
    if lower not in infl: c.skinCluster(sc, e=True, ai=lower, wt=0, lw=True)
    fn = om.MFnMesh(_dag(mesh)); P0 = np.array([(p.x, p.y, p.z) for p in fn.getPoints(om.MSpace.kWorld)])
    c.skinPercent(sc, ['%s.vtx[%d]' % (mesh, v) for v in low], transformValue=[(lower, 1.0)], normalize=True)
    P1 = np.array([(p.x, p.y, p.z) for p in fn.getPoints(om.MSpace.kWorld)])
    rep.update(lower_verts=len(low), upper_verts=len(up), rest_shift_cm=round(float(np.abs(P1 - P0).max()), 5))
    return rep


def tongue_settle(jaw='Mouth_Jaw_Ctrl.rx', grp='Tongue_A_CtrlAutoRotate_Grp', mesh='teeth_geo', tongue=('M_tongue',),
                  per_deg=(0.0, -0.1, -0.02)):
    """the tongue drops (and slides back a little) as the jaw opens, instead of riding over the lower teeth:
    jaw opening (clamped at 0) x per-degree world offset -> the tongue root group's translate (local axes solved
    numerically, so it works whatever the group's orientation). Plain nodes, exports as joint motion."""
    from . import mouth_guard as MG
    fn = om.MFnMesh(_dag(mesh))
    tv = sorted({v for f in MG._mat_faces(mesh, tongue) for v in fn.getPolygonVertices(f)})
    P0 = np.array([(p.x, p.y, p.z) for p in fn.getPoints(om.MSpace.kWorld)])[tv].mean(0)
    cols = []
    for a in 'xyz':                                                   # world motion of the tongue per unit of local translate
        v = c.getAttr('%s.t%s' % (grp, a)); c.setAttr('%s.t%s' % (grp, a), v + 1)
        P = np.array([(p.x, p.y, p.z) for p in fn.getPoints(om.MSpace.kWorld)])[tv].mean(0); c.setAttr('%s.t%s' % (grp, a), v)
        cols.append(P - P0)
    A = np.array(cols).T                                              # world = A @ local
    local = np.linalg.lstsq(A, np.array(per_deg), rcond=None)[0]       # local translate per degree of jaw opening
    cl = c.createNode('clamp', n='tongueSettle_jawOpen_clamp'); c.setAttr(cl + '.maxR', 90)
    c.connectAttr(jaw, cl + '.inputR'); out = {}
    for a, k in zip('xyz', local):
        if abs(k) < 1e-4: continue
        m = c.createNode('multDL', n='tongueSettle_%s_mult' % a); c.setAttr(m + '.i2', float(k))
        c.connectAttr(cl + '.outputR', m + '.i1'); c.connectAttr(m + '.o', '%s.t%s' % (grp, a), f=True); out[a] = round(float(k), 4)
    return out


def smile_jaw_fade(bs='face_shapes', mesh='body_geo', jaw='Mouth_Jaw_Ctrl.rx', jaw_ref='LowerTeeth_Skl',
                   targets=('L_smile', 'R_smile', 'C_smile', 'L_up', 'R_up', 'L_kiss', 'R_kiss', 'C_kiss', 'L_wide', 'R_wide'), full_at=12.0, drop_old=('col_jaw_smile_L',
                   'col_jaw_smile_R', 'col_jaw_smile_LR')):
    """shapes captured with the jaw closed lift the lower lip to meet the upper one. With the jaw open (and teeth that
    follow the jaw) that lift keeps the lower lip up while the lower teeth and tusks drop, so they show on the chin.
    For each target, a cancel target = -(how much each vertex follows the jaw) x (the target's offsets), weighted by
    target weight x jaw opening (full at `full_at` degrees). Upper lip and cheeks don't follow the jaw, so they keep the
    smile; the lower lip and chin ride down with the jaw. The old jaw x smile lip/teeth collision combos assumed teeth
    that never moved, so they are switched off."""
    from . import corrective_inversion as GC
    fn = om.MFnMesh(_dag(mesh)); pts = lambda: np.array([(p.x, p.y, p.z) for p in fn.getPoints(om.MSpace.kWorld)])
    al = c.aliasAttr(bs, q=True) or []; names = al[0::2]
    rep = dict(dropped=[], added=[])
    for t in drop_old:                                               # old collision combos off
        if t in names:
            for s in c.listConnections(bs + '.' + t, s=True, d=False, p=True) or []: c.disconnectAttr(s, bs + '.' + t)
            c.setAttr(bs + '.' + t, 0); rep['dropped'].append(t)
    # jaw-follow ratio per vertex (skin only), against a point riding rigidly on the jaw reference joint
    env = c.getAttr(bs + '.envelope'); c.setAttr(bs + '.envelope', 0)
    P0 = pts(); M0 = om.MMatrix(c.xform(jaw_ref, q=True, ws=True, m=True))
    j0 = c.getAttr(jaw); c.setAttr(jaw, 10)
    P1 = pts(); M1 = om.MMatrix(c.xform(jaw_ref, q=True, ws=True, m=True)); c.setAttr(jaw, j0)
    R = np.array(list(M0.inverse() * M1)).reshape(4, 4)
    rigid = np.hstack([P0, np.ones((len(P0), 1))]) @ R; rigid = rigid[:, :3] - P0
    ratio = np.clip(np.linalg.norm(P1 - P0, axis=1) / (np.linalg.norm(rigid, axis=1) + 1e-6), 0, 1)
    mask = np.clip((ratio - 0.15) / 0.7, 0, 1); mask = mask * mask * (3 - 2 * mask)   # smoothstep 0.15..0.85
    c.setAttr(bs + '.envelope', env)
    inv = GC.mesh_inv3(mesh)
    # jaw opening 0..1
    jm = c.createNode('multDL', n='smileJawFade_jaw_scale'); c.setAttr(jm + '.i2', 1.0 / full_at); c.connectAttr(jaw, jm + '.i1')
    jc = c.createNode('clamp', n='smileJawFade_jaw_clamp'); c.setAttr(jc + '.maxR', 1); c.connectAttr(jm + '.o', jc + '.inputR')
    for t in targets:
        if t not in names: continue
        w = bs + '.' + t; src = (c.listConnections(w, s=True, d=False, p=True) or [None])[0]
        if src: c.disconnectAttr(src, w)
        c.setAttr(w, 1); D = pts() - P0; c.setAttr(w, 0)
        if src: c.connectAttr(src, w)
        D = -(D * mask[:, None]); keep = np.where(np.linalg.norm(D, axis=1) > 1e-4)[0]
        if not len(keep): continue
        idx = GC.new_target(t + '_jawFade', bs); GC.set_deltas(idx, keep, D[keep] @ inv, bs)
        m = c.createNode('multDL', n='smileJawFade_%s' % t); c.connectAttr(jc + '.outputR', m + '.i2')
        if src: c.connectAttr(src, m + '.i1')
        else: c.connectAttr(w, m + '.i1')
        c.connectAttr(m + '.o', bs + '.' + t + '_jawFade', f=True)
        rep['added'].append('%s_jawFade (%d verts, max %.2f cm)' % (t, len(keep), float(np.linalg.norm(D, axis=1).max())))
    rep['mask_lower_lip_verts'] = int((mask > 0.5).sum())
    return rep
