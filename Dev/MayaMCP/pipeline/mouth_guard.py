"""Mouth guard (generic, Mutant Tools style face rigs): keeps tusks, teeth, gums and tongue from cutting through the lips
by moving the lip *tweak controls* (and, a little, the upper / lower teeth controls). The geometry is never edited: the
fix is animation on controls the animator can see, key over or switch off.

    g = Guard()             # build with the face at neutral: finds the controls, measures what they move (Jacobian)
    g.solve()               # current pose: sets the controls so nothing crosses the lip surface -> report dict
    g.bake(frames)          # solve + key every frame (lightly smoothed): face animation, mocap face, video face

Everything is measured in the head's rest frame (from the skin's bind matrix of the `head` joint), so it works while
mocap turns the head. Every constraint is a row "skin vertex s must move by `need` along direction d, relative to teeth
vertex t", and the solver turns rows into control moves through a 3D Jacobian of both meshes.

Tests per pose
  fangs  a fang (tusk) vertex that faces the camera at rest and is not covered at rest must stay uncovered, seen from
         the front and from both three-quarter sides (the cameras animators and these renders use).
         - skin that sat behind the fang at rest (upper lip) and now covers it goes back behind it, along the view;
         - skin that sat in front of the fang root at rest (lower lip) and now rides up over it goes *down*, under the
           fang, by the height it covers (measured by marching up the fang until the lip edge is passed). Pushing that
           lip back instead would drag it through the gum.
  inner  a gum / tongue / teeth vertex visible from the front with the lip's front surface right behind it is poking
         through; one hidden by the lip's outer surface by less than `clear` would still show once both meshes are
         smoothed (smooth preview / subdivision pulls a convex lip inwards) -> lip forward / teeth back
  red    gum / tongue vertices (the red parts) keep `clear` from the closest *outer* skin (faces seen from the front at
         rest, not the mouth bag), in any direction
Rows become control moves by weighted ridge least squares, with a line search (a step is kept only if the total
violation drops). Upper-teeth moves are cheap, lower-teeth (fang) moves expensive and small; fang rows weigh `tusk_weight`;
neighbouring lip tweaks are tied by a smoothness term so a correction bends the lip instead of folding it."""
import math, numpy as np, maya.cmds as c, maya.api.OpenMaya as om

FRONT, UP = np.array([0., 0., 1.]), np.array([0., 1., 0.])


def _dag(n):
    sl = om.MSelectionList(); sl.add(n); return sl.getDagPath(0)


def _shape_dag(n):
    d = _dag(n); d.extendToShape(); return d


def _mat_faces(mesh, mats):
    """face ids of `mesh` assigned to any of the materials"""
    out, nf = set(), c.polyEvaluate(mesh, f=True)
    shapes = {s.split('|')[-1] for s in c.listRelatives(mesh, s=True, f=True) or []}
    for m in mats:
        if not c.objExists(m): continue
        for sg in set(c.listConnections(m + '.outColor', d=True, s=False, type='shadingEngine') or []):
            for e in c.ls(c.sets(sg, q=True) or [], fl=True):
                node = e.split('.')[0].split('|')[-1]
                if node != mesh.split('|')[-1] and node not in shapes: continue
                if '.f[' in e: out.add(int(e.split('[')[-1][:-1]))
                else: out.update(range(nf))
    return sorted(out)


def _pts(fn):
    return np.array([(p.x, p.y, p.z) for p in fn.getPoints(om.MSpace.kWorld)])


def _wm(n):
    return om.MMatrix(c.getAttr(n + '.worldMatrix[0]'))


def _bind_matrix(skin, joint):
    """world matrix of `joint` at bind time (inverse of the skinCluster's bindPreMatrix), else its current one"""
    for sc in c.ls(c.listHistory(skin) or [], type='skinCluster'):
        for p in c.listConnections(joint + '.worldMatrix[0]', d=True, s=False, p=True, type='skinCluster') or []:
            if p.split('.')[0] == sc:
                i = int(p.split('[')[-1][:-1])
                return om.MMatrix(c.getAttr('%s.bindPreMatrix[%d]' % (sc, i))).inverse()
    return _wm(joint)


class Guard:
    def __init__(self, skin='body_geo', teeth='teeth_geo', head='head', tusk=('M_tusk',),
                 inner=('M_gums', 'M_tongue', 'M_teeth'), red=('M_gums', 'M_tongue'), ctrls=None,
                 teeth_ctrls=(('UpperTeeth_Ctrl', 'yz', 1.0, 0.5), ('LowerTeeth_Ctrl', 'z', 0.25, 3.0)), views=(0, 25, -25), margin=0.1, inner_margin=0.15,
                 ridge=0.05, smooth=0.3, limit=1.6, tusk_weight=3.0, reach=1.2, clear=0.2,
                 fang_clear=0.3, teeth_vis_cost=3.0, lower_lip_down=False, vis_tuck=0.35, gum_weight=2.0, rounds=6,
                 log=print):
        self.skin = om.MFnMesh(_dag(skin)); self.teeth = om.MFnMesh(_dag(teeth)); self.skin_dp = _shape_dag(skin)
        self.margin, self.inner_margin, self.ridge, self.rounds, self.log = margin, inner_margin, ridge, rounds, log
        self.tusk_weight, self.reach, self.clear, self.smooth, self.fang_clear = tusk_weight, reach, clear, smooth, fang_clear
        self.views = [np.array([math.sin(math.radians(a)), 0.0, math.cos(math.radians(a))]) for a in views]
        self.head = head if head and c.objExists(head) else None
        self.M0 = _bind_matrix(skin, head) if self.head else om.MMatrix()
        self.tusk_f = _mat_faces(teeth, tusk); tf = set(self.tusk_f)
        verts = lambda fs: sorted({v for f in fs for v in self.teeth.getPolygonVertices(f)})
        self.inner_v = verts([f for f in _mat_faces(teeth, inner) if f not in tf])
        self.red_v = verts([f for f in _mat_faces(teeth, red) if f not in tf])
        self.tusk_v = np.array(verts(self.tusk_f), dtype=int)
        if ctrls is None:
            ctrls = sorted({n for n in c.ls('*Mouth*Tweek_Ctrl', '*Lip*Tweek*Ctrl', '*:*Mouth*Tweek_Ctrl', type='transform')})
        self.plugs, lim, cost, isteeth = [], [], [], []
        # teeth controls: (name, axes, limit, cost). Upper teeth move only the upper teeth and gums (cheap, hides gum specks);
        # lower teeth carry the tusks, so they are expensive and kept small (the fangs should not wander)
        for n, axes, L, w, tt in ([(n, 'xyz', limit, 1.0, 0) for n in ctrls] +
                                  [(n, ax, tl, tc, 1) for n, ax, tl, tc in teeth_ctrls if c.objExists(n)]):
            for a in axes:
                p = n + '.t' + a
                if c.getAttr(p, k=True) and not c.getAttr(p, l=True):
                    self.plugs.append(p); lim.append(L); cost.append(w); isteeth.append(tt)
        self.lim, self.cost, self.isteeth = np.array(lim), np.array(cost), np.array(isteeth, dtype=bool)
        self.teeth_vis_cost, self.lower_lip_down, self.vis_tuck, self.gum_weight = teeth_vis_cost, lower_lip_down, vis_tuck, gum_weight
        self.acc = self.skin.autoUniformGridParams()
        self._frame()
        self.S0, self.T0 = _pts(self.skin), _pts(self.teeth)
        self.S0r, self.T0r = self._to_rest(self.S0), self._to_rest(self.T0)
        self._smoothness(ctrls)
        self._jacobian()
        self._outer_faces()
        self._rest()
        self.log('mouthguard: %d plugs (%d teeth), %d responsive lip verts, %d fang verts (seen at rest per view: %s), %d lip '
                 'verts near fangs (%d behind, %d in front), %d gum/teeth/tongue verts, %d outer faces'
                 % (len(self.plugs), int(self.isteeth.sum()), len(self.region), len(self.tusk_v),
                    '/'.join(str(len(e)) for e in self.exposed), len(self.side), sum(1 for v in self.side.values() if v > 0),
                    sum(1 for v in self.side.values() if v < 0), len(self.inner_v), len(self.outer)))

    # ---- head frame: world <-> rest for the current head pose
    def _frame(self):
        Mh = _wm(self.head) if self.head else om.MMatrix()
        Q = Mh.inverse() * self.M0                                   # world now -> world at rest (row vectors)
        self.Q = np.array(list(Q)).reshape(4, 4); self.R = self.Q[:3, :3]
        u, _, vt = np.linalg.svd(self.R); self.R = u @ vt           # pure rotation (drop any scale)

    def _w(self, d_rest):                                            # rest direction -> world MFloatVector
        d = d_rest @ self.R.T; return om.MFloatVector(*(d / (np.linalg.norm(d) + 1e-12)))

    def _to_rest(self, P):
        return np.hstack([P, np.ones((len(P), 1))]) @ self.Q[:, :3]

    def _rest_dir(self, v):                                          # world MVector -> rest numpy
        return np.array([v.x, v.y, v.z]) @ self.R

    # ---- setup (face at neutral)
    def _smoothness(self, ctrls):
        """difference operator between neighbouring lip tweaks (upper and lower lip each sorted across the mouth), so a
        correction bends the lip instead of folding it at one control"""
        idx = {p: i for i, p in enumerate(self.plugs)}; rows = []
        for lip in ('_Up_', '_Dw_'):
            cs = [n for n in ctrls if lip in n]
            if len(cs) < 2: continue
            xs = self._to_rest(np.array([c.xform(n, q=True, ws=True, t=True) for n in cs]))[:, 0]
            cs = [n for _, n in sorted(zip(xs, cs))]
            for a, b in zip(cs[:-1], cs[1:]):
                for ax in 'xyz':
                    i, j = idx.get(a + '.t' + ax), idx.get(b + '.t' + ax)
                    if i is None or j is None: continue
                    r = np.zeros(len(self.plugs)); r[i], r[j] = 1, -1; rows.append(r)
        self.D = np.array(rows) if rows else np.zeros((0, len(self.plugs)))
        self.DtD = self.D.T @ self.D

    def _jacobian(self, h=0.2):
        cs, ct = [], []
        for p in self.plugs:
            v = c.getAttr(p); c.setAttr(p, v + h)
            cs.append((_pts(self.skin) - self.S0) @ self.R / h); ct.append((_pts(self.teeth) - self.T0) @ self.R / h)
            c.setAttr(p, v)
        self.Js = np.transpose(np.array(cs), (1, 0, 2))             # skin verts x plugs x 3, rest frame, per unit
        self.Jt = np.transpose(np.array(ct), (1, 0, 2))             # teeth verts x plugs x 3
        self.region = set(np.where(np.abs(self.Js).max((1, 2)) > 2e-3)[0].tolist())

    def _tusk_hits(self, p, d, far=4.0):
        r = self.teeth.allIntersections(om.MFloatPoint(*p), d, om.MSpace.kWorld, far, False, faceIds=self.tusk_f,
                                        idsSorted=True, sortHits=True)
        if not r or not len(r[1]): return []
        return [(float(t), int(f), self._rest_dir(self.teeth.getPolygonNormal(int(f), om.MSpace.kWorld))[2])
                for t, f in zip(r[1], r[2])]

    def _skin_hit(self, pt, d, far):
        r = self.skin.closestIntersection(om.MFloatPoint(*pt), d, om.MSpace.kWorld, far, False, accelParams=self.acc)
        return r if r and r[2] >= 0 else None

    def _outer_faces(self):
        """skin faces around the mouth seen from the front at rest: the face itself, not the mouth bag / inner lip"""
        counts, conn = self.skin.getVertices(); counts, conn = np.array(counts), np.array(conn)
        starts = np.concatenate([[0], np.cumsum(counts)[:-1]]); reg = np.zeros(len(self.S0), bool); reg[list(self.region)] = True
        self.outer = set(); fw = self._w(FRONT)
        for f, (a, n) in enumerate(zip(starts, counts)):
            vs = conn[a:a + n]
            if not reg[vs].any(): continue
            nm = self.skin.getPolygonNormal(f, om.MSpace.kWorld)
            if self._rest_dir(nm)[2] <= 0.05: continue
            ctr = self.S0[vs].mean(0) + np.array([nm.x, nm.y, nm.z]) * 0.02
            if not self._skin_hit(ctr, fw, 4.0): self.outer.add(f)

    def _rest(self):
        """fang vertices seen at rest from each view, and for lip vertices near a fang which side of it they live on
        (from the fang's front surface at the same rest x/y: +1 behind it, -1 in front, 0 beside)"""
        self.exposed, self.near, self.side = [[] for _ in self.views], {}, {}
        if not len(self.tusk_v): return
        T = self.T0r[self.tusk_v]
        nrm = {int(t): self._rest_dir(self.teeth.getVertexNormal(int(t), True, om.MSpace.kWorld)) for t in self.tusk_v}
        # every front-facing fang point that is uncovered at rest is protected from lips coming over it ('back' rows);
        # the 'down' rows (lower lip riding up the root) only use points `fang_clear` above the lip at rest, so the lip
        # may roll a few mm over the root as it does at rest without the guard prying the mouth open
        down = np.array([0, -1., 0]) * self.fang_clear @ self.R.T
        self.exposed_clear = [[] for _ in self.views]
        for k, v in enumerate(self.views):
            vw = self._w(v)
            self.exposed[k] = [int(t) for t in self.tusk_v if nrm[int(t)] @ v > -0.15 and not self._skin_hit(self.T0[t], vw, 4.0)]
            self.exposed_clear[k] = [t for t in self.exposed[k] if not self._skin_hit(self.T0[t] + down, vw, 4.0)]
        fw = self._w(FRONT)
        for v in self.region:
            p = self.S0r[v]; d3 = np.linalg.norm(T - p, axis=1)
            if d3.min() > 3.0: continue
            hits = self._tusk_hits(self.S0[v], fw)
            if hits and hits[0][2] > 0: continue                      # inside already at rest: leave it
            dxy = np.linalg.norm(T[:, :2] - p[:2], axis=1)
            if dxy.min() > 1.2: self.side[int(v)] = 0
            else:
                zf = T[dxy <= max(0.45, dxy.min() + 0.15), 2].max()   # fang front surface around this x/y
                self.side[int(v)] = 1 if p[2] < zf - 0.05 else -1
            self.near[int(v)] = int(self.tusk_v[int(np.argmin(d3))])

    def _teeth_visible(self):
        """fraction of the front teeth surface seen from the front right now (0 lips closed .. 1 all teeth showing)"""
        if not hasattr(self, '_front_teeth'):
            fn = self.teeth; vs = [v for f in _mat_faces('teeth_geo', ('M_teeth',)) for v in fn.getPolygonVertices(f)]
            vs = sorted(set(vs)); n = np.array([self._rest_dir(fn.getVertexNormal(v, True, om.MSpace.kWorld)) for v in vs])
            self._front_teeth = [v for v, nn in zip(vs, n) if nn[2] > 0.5][::3]
        T = _pts(self.teeth); fw = self._w(FRONT)
        seen = [0 if self._skin_hit(T[v], fw, 4.0) else 1 for v in self._front_teeth]
        return float(np.mean(seen)) if seen else 0.0

    def _cover_height(self, p, vw, uw, top=2.0, step=0.05):
        """how far up the fang (from p) the skin keeps covering it along view vw"""
        h = step
        while h <= top:
            if not self._skin_hit(p + uw * h, vw, 4.0): return h
            h += step
        return top

    # ---- per pose
    def needs(self):
        """[(skin vertex, teeth vertex or -1, direction (rest frame), need along it, weight)] for the current pose"""
        self._frame()
        out = []; self.kinds = dict(fang_back=0, fang_down=0, inner=0, red=0)
        S, T = _pts(self.skin), _pts(self.teeth)
        uw = np.array(self._w(UP))
        if not hasattr(self, '_clear'): self._clear = [set(e) for e in self.exposed_clear]
        # how open the mouth is, from how far the fangs (lower jaw) dropped: the gum checks ease off as it opens, where
        # the lower lip rolls in and the rest-pose 'outer skin' labels stop meaning much
        drop = float(self.T0r[self.tusk_v, 1].mean() - self._to_rest(T[self.tusk_v])[:, 1].mean()) if len(self.tusk_v) else 0.0
        self.open = min(1.0, max(0.0, drop / 2.0)); wi = self.gum_weight * (1.0 - 0.8 * self.open)   # a red speck is as bad as a covered fang
        for k, v in enumerate(self.views):                            # fangs, per view
            vw = self._w(v)
            for t in self.exposed[k]:
                r = self._skin_hit(T[t], vw, 4.0)
                if not r: continue
                F = [s for s in self.skin.getPolygonVertices(r[2]) if s in self.region]
                if not F: continue
                if np.mean([self.side.get(s, 0) for s in F]) < -0.3:  # lower lip riding up over the root: go under it
                    if t not in self._clear[k]: continue
                    # lower lip riding up over the fang: near the root (within `fang_clear` of the rest lip line) that is
                    # how the mouth looks at rest, so it is left alone; higher up, the lip edge tucks *behind* the fang
                    # locally (a notch, as a lip wraps a tusk). Pulling the lip down instead parts a closed smile.
                    if not self.lower_lip_down:
                        # only with the mouth closed: once the jaw opens the fangs belong behind the lower lip, inside
                        if t not in self._clear[k] or self.open > 0.2: continue
                        need = r[1] + self.margin; d = -v; self.kinds['fang_back'] += 1
                        for s in F: out.append((s, t, d, need, self.tusk_weight * 0.7))
                        continue
                    need = min(self._cover_height(T[t], vw, uw) + self.margin, self.fang_clear); d = -UP
                    self.kinds['fang_down'] += 1
                    for s in F: out.append((s, t, d, need, 1.0))
                    continue
                else:                                                 # lip that came over the fang: back, along the view
                    need = r[1] + self.margin; d = -v; self.kinds['fang_back'] += 1
                for s in F: out.append((s, t, d, need, self.tusk_weight))
        fw = self._w(FRONT); bw = self._w(-FRONT)
        for v in self.inner_v:                                        # inner
            r = self._skin_hit(T[v], fw, 4.0)
            if r:                                                     # hidden: enough lip in front of it?
                if r[1] < self.clear and self._rest_dir(self.skin.getPolygonNormal(r[2], om.MSpace.kWorld))[2] > 0.2:
                    for s in self.skin.getPolygonVertices(r[2]):
                        if s in self.region: out.append((s, v, FRONT, self.clear - r[1] + 0.03, wi)); self.kinds['inner'] += 1
                continue
            r = self._skin_hit(T[v], bw, self.reach)
            if not r or self._rest_dir(self.skin.getPolygonNormal(r[2], om.MSpace.kWorld))[2] <= 0.2: continue
            for s in self.skin.getPolygonVertices(r[2]):
                if s in self.region: out.append((s, v, FRONT, r[1] + self.inner_margin, wi)); self.kinds['inner'] += 1
        if self.red_v:                                                # red
            M = self.skin_dp.inclusiveMatrix(); mi = om.MMeshIntersector(); mi.create(self.skin_dp.node(), M)
            for v in self.red_v:
                try: pom = mi.getClosestPoint(om.MPoint(*T[v]), 1.0)
                except Exception: continue
                if pom is None or pom.face not in self.outer: continue
                cp, n = om.MPoint(pom.point) * M, (om.MVector(pom.normal) * M).normal()   # results come in object space
                nf = self._rest_dir(n)[2]
                if nf <= 0.2: continue
                sd = (T[v][0] - cp.x) * n.x + (T[v][1] - cp.y) * n.y + (T[v][2] - cp.z) * n.z
                if sd <= -self.clear: continue
                need = (sd + self.clear) / max(nf, 0.5) + 0.03
                for s in self.skin.getPolygonVertices(pom.face):
                    if s in self.region: out.append((s, v, FRONT, need, wi)); self.kinds['red'] += 1
        best = {}                                                     # one row per pair + direction, the largest need
        for s, t, d, need, w in out:
            key = (s, t, tuple(np.round(d, 3)))
            if key not in best or need > best[key][1]: best[key] = (d, need, w)
        return [(s, t, d, need, w) for (s, t, _), (d, need, w) in best.items()]

    def _plug_vals(self): return np.array([c.getAttr(p) for p in self.plugs])

    def _set(self, vals):
        for p, v in zip(self.plugs, vals): c.setAttr(p, float(v))

    @staticmethod
    def _err(rows): return float(sum(w * abs(n) for _, _, _, n, w in rows))

    def solve(self, start=None, base=None):
        """fix the current pose; start = control values to begin from (default: what they are now); the move limits are
        measured from `base` (default: the values before solving)"""
        if start is not None: self._set(start)
        x0 = self._plug_vals() if base is None else np.asarray(base, float); rep = dict(rounds=[])
        rows = self.needs(); err = self._err(rows); rep['rounds'].append(len(rows)); first = dict(self.kinds)
        # moving teeth that are on show reads as the teeth sliding (and shows the tongue behind them): teeth moves get
        # expensive as more of the teeth are visible
        vis = self._teeth_visible(); rep['teeth_visible'] = round(vis, 2)
        cost = self.cost * np.where(self.isteeth, 1.0 + self.teeth_vis_cost * vis, 1.0)
        lim = self.lim * np.where(self.isteeth, max(0.0, 1.0 - 5.0 * vis), 1.0)
        lim = np.where(self.isteeth, np.minimum(self.lim, np.maximum(lim, self.vis_tuck)), lim)   # a small tuck stays allowed (gum specks)
        # two stages: teeth controls alone first (tuck the gums back without touching the lips), then everything for
        # what is left - so a closed smile is fixed behind the lips instead of by prying them open. With the teeth on
        # show there is no teeth stage and the teeth barely move.
        stages = ((self.isteeth, np.ones(len(self.plugs), bool)) if vis < 0.08 else (np.ones(len(self.plugs), bool),))
        for free in stages:
            for _ in range(self.rounds):
                if not rows: break
                W = np.array([w for *_, w in rows])[:, None]
                A = W * np.array([(self.Js[s] - (self.Jt[t] if t >= 0 else 0)) @ d for s, t, d, _, _ in rows])
                A[:, ~free] = 0
                b = W[:, 0] * np.array([n for _, _, _, n, _ in rows])
                sc = np.trace(A.T @ A) / max(1, int(free.sum())) + 1e-9
                lam, mu = self.ridge * sc, self.smooth * sc
                cur = self._plug_vals()
                x = np.linalg.solve(A.T @ A + lam * np.diag(cost ** 2) + mu * self.DtD, A.T @ b - mu * self.DtD @ (cur - x0))
                x[~free] = 0
                best = None
                for a in (1.0, 0.5, 0.25):                            # line search: keep a step only if it helps
                    new = np.clip(cur + a * x, x0 - lim, x0 + lim); self._set(new)
                    r2 = self.needs(); e2 = self._err(r2)
                    if best is None or e2 < best[0]: best = (e2, new, r2)
                    if e2 < err * 0.7: break
                if best[0] >= err:                                    # no step helped: back to where we were, next stage
                    self._set(cur); break
                err, rows = best[0], best[2]; self._set(best[1]); rep['rounds'].append(len(rows))
        d = self._plug_vals() - x0
        rep.update(err=round(err, 3), first=first, kinds=dict(self.kinds), moved=float(np.abs(d).max()) if self.plugs else 0.0,
                   teeth={p: round(float(v), 3) for p, v, tt in zip(self.plugs, d, self.isteeth) if tt and abs(v) > 1e-3})
        return rep

    def bake(self, frames, smooth=1, warm=True):
        """solve every frame (from the previous frame's answer when `warm`, else from 0), smooth over +-smooth frames,
        key the plugs that moved. Limits always count from rest, so warm starts can't creep. Returns a summary."""
        frames = list(frames)
        for p in self.plugs:
            c.cutKey(p.split('.')[0], at=p.split('.')[1], t=(min(frames), max(frames)), cl=True)
        vals = np.zeros((len(frames), len(self.plugs))); err = []; prev = zero = np.zeros(len(self.plugs))
        for i, f in enumerate(frames):
            c.currentTime(f)
            r = self.solve(start=prev if warm else zero, base=zero)
            if warm and r['err'] > 0:                                 # a cold start may do better where the warm one sticks
                keep = self._plug_vals(); r0 = self.solve(start=zero, base=zero)
                if r0['err'] >= r['err']: self._set(keep)
                else: r = r0
            vals[i] = prev = self._plug_vals(); err.append(r['err'])
        if smooth:
            sm = np.empty_like(vals)
            for i in range(len(frames)):
                lo, hi = max(0, i - smooth), min(len(frames), i + smooth + 1); sm[i] = vals[lo:hi].mean(0)
            vals = np.where(np.abs(vals) > np.abs(sm), vals, sm)      # never smooth a correction away
        keyed = 0
        for j, p in enumerate(self.plugs):
            if np.abs(vals[:, j]).max() < 1e-3: continue
            n, a = p.split('.')
            for f, v in zip(frames, vals[:, j]): c.setKeyframe(n, at=a, t=f, v=float(v))
            keyed += 1
        return dict(frames=len(frames), plugs_keyed=keyed, frames_clean=int(sum(1 for e in err if e == 0)),
                    worst_err=round(float(max(err or [0])), 3), max_move=round(float(np.abs(vals).max()), 3))
