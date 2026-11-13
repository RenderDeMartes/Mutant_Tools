"""Mouth guard (generic, Mutant Tools style face rigs): keeps tusks, teeth, gums and tongue from cutting through the lips
by moving the lip *tweak controls* (and, a little, the upper / lower teeth controls). The geometry is never edited: the
fix is animation on controls the animator can see, key over or switch off.

    g = Guard()             # build with the face at neutral: finds the controls, measures what they move (Jacobian)
    g.solve()               # current pose: sets the controls so nothing crosses the lip surface -> report dict
    g.bake(frames)          # solve + key every frame (lightly smoothed): face animation, mocap face, video face

Everything is measured in the head's rest frame (from the skin's bind matrix of the `head` joint), so it works while
mocap turns the head. "Forward" below = the face's forward axis.

Tests per pose (rows are pairs skin vertex / teeth vertex, so moving either side fixes them)
  cover  a forward-facing tusk vertex seen from the front at rest gets covered by skin: the lip went through the tusk
         (or slid over it) -> that skin goes back behind it, so the fangs always read. Skin that sat in front of the
         tusk at rest (lower lip over the root) only gets a light row: it may cover the root rather than be pushed
         through the gum
  inner  a gum / tongue / teeth vertex visible from the front with the lip's front surface right behind it is poking
         through; one hidden by the lip's outer surface by less than `clear` would still show once both meshes are
         smoothed (smooth preview / subdivision pulls a convex lip inwards) -> lip forward / teeth back
  red    gum / tongue vertices (the red parts) keep `clear` from the closest *outer* skin (faces seen from the front at
         rest, not the mouth bag), in any direction - the sloped front of a pushed-back lower lip is not caught by rays
  inside (optional, off) a lip vertex inside a tusk -> out the way it came. Contact on the back of a tusk is never
         seen and fights the gum tests
Needed offsets along forward become control translations by weighted ridge least squares on the Jacobian of both
meshes, with a line search (a step is kept only if the total violation drops), so the lip slides around the tusk /
over the gum with the rig's own falloff. Teeth controls cost a little more than the lip tweaks."""
import numpy as np, maya.cmds as c, maya.api.OpenMaya as om


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
                 teeth_ctrls=('UpperTeeth_Ctrl', 'LowerTeeth_Ctrl'), margin=0.08, inner_margin=0.15, ridge=0.05, limit=2.0,
                 teeth_limit=0.6, teeth_cost=0.8, tusk_weight=3.0, inside=False, reach=1.2, clear=0.2, rounds=6, log=print):
        self.skin = om.MFnMesh(_dag(skin)); self.teeth = om.MFnMesh(_dag(teeth)); self.skin_dp = _shape_dag(skin)
        self.margin, self.inner_margin, self.ridge, self.rounds, self.log = margin, inner_margin, ridge, rounds, log
        self.tusk_weight, self.use_inside, self.reach, self.clear = tusk_weight, inside, reach, clear
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
        for n, axes, L, w, tt in ([(n, 'xyz', limit, 1.0, 0) for n in ctrls] +
                                  [(n, 'yz', teeth_limit, teeth_cost, 1) for n in teeth_ctrls if c.objExists(n)]):
            for a in axes:
                p = n + '.t' + a
                if c.getAttr(p, k=True) and not c.getAttr(p, l=True):
                    self.plugs.append(p); lim.append(L); cost.append(w); isteeth.append(tt)
        self.lim, self.cost, self.isteeth = np.array(lim), np.array(cost), np.array(isteeth, dtype=bool)
        self.acc = self.skin.autoUniformGridParams()
        self._frame()
        self.S0, self.T0 = _pts(self.skin), _pts(self.teeth)
        self.S0r, self.T0r = self._to_rest(self.S0), self._to_rest(self.T0)
        self._jacobian()
        self._outer_faces()
        self._rest()
        self.log('mouthguard: %d plugs (%d teeth), %d responsive lip verts, %d tusk verts (%d seen from the front), %d lip '
                 'verts near tusks (%d behind, %d in front), %d gum/teeth/tongue verts, %d outer faces'
                 % (len(self.plugs), int(self.isteeth.sum()), len(self.region), len(self.tusk_v), len(self.exposed),
                    len(self.side), sum(1 for v in self.side.values() if v > 0), sum(1 for v in self.side.values() if v < 0),
                    len(self.inner_v), len(self.outer)))

    # ---- head frame: forward axis and world -> rest mapping for the current head pose
    def _frame(self):
        Mh = _wm(self.head) if self.head else om.MMatrix()
        Q = Mh.inverse() * self.M0                                   # world now -> world at rest (row vectors)
        self.Q = np.array(list(Q)).reshape(4, 4)
        f = om.MVector(0, 0, 1) * Q.inverse()                        # rest +z, now
        self.f = np.array([f.x, f.y, f.z]); self.f /= np.linalg.norm(self.f)
        self.FW = om.MFloatVector(*self.f); self.BW = om.MFloatVector(*(-self.f))

    def _to_rest(self, P):
        return np.hstack([P, np.ones((len(P), 1))]) @ self.Q[:, :3]

    def _fz(self, v):                                                # forward component of an MVector / MFloatVector
        return v.x * self.f[0] + v.y * self.f[1] + v.z * self.f[2]

    # ---- setup (face at neutral)
    def _jacobian(self, h=0.2):
        cs, ct = [], []
        for p in self.plugs:
            v = c.getAttr(p); c.setAttr(p, v + h)
            cs.append((_pts(self.skin) - self.S0) @ self.f / h); ct.append((_pts(self.teeth) - self.T0) @ self.f / h)
            c.setAttr(p, v)
        self.Js, self.Jt = np.array(cs).T, np.array(ct).T           # verts x plugs: forward motion per unit of control
        self.region = set(np.where(np.abs(self.Js).max(1) > 2e-3)[0].tolist())

    def _tusk_hits(self, p, d, far=4.0):
        r = self.teeth.allIntersections(om.MFloatPoint(*p), d, om.MSpace.kWorld, far, False, faceIds=self.tusk_f,
                                        idsSorted=True, sortHits=True)
        if not r or not len(r[1]): return []
        return [(float(t), int(f), self._fz(self.teeth.getPolygonNormal(int(f), om.MSpace.kWorld))) for t, f in zip(r[1], r[2])]

    def _skin_hit(self, pt, d, far):
        r = self.skin.closestIntersection(om.MFloatPoint(*pt), d, om.MSpace.kWorld, far, False, accelParams=self.acc)
        return r if r and r[2] >= 0 else None

    def _outer_faces(self):
        """skin faces around the mouth seen from the front at rest: the face itself, not the mouth bag / inner lip"""
        counts, conn = self.skin.getVertices(); counts, conn = np.array(counts), np.array(conn)
        starts = np.concatenate([[0], np.cumsum(counts)[:-1]]); reg = np.zeros(len(self.S0), bool); reg[list(self.region)] = True
        self.outer = set()
        for f, (a, n) in enumerate(zip(starts, counts)):
            vs = conn[a:a + n]
            if not reg[vs].any(): continue
            nm = self.skin.getPolygonNormal(f, om.MSpace.kWorld)
            if self._fz(nm) <= 0.05: continue
            ctr = self.S0[vs].mean(0) + np.array([nm.x, nm.y, nm.z]) * 0.02
            if not self._skin_hit(ctr, self.FW, 4.0): self.outer.add(f)

    def _rest(self):
        """tusk vertices seen from the front, and for lip vertices near a tusk which side of it they live on (from the
        tusk's front surface at the same rest x/y: +1 behind it, -1 in front, 0 beside)"""
        self.exposed, self.near, self.side = [], {}, {}
        if not len(self.tusk_v): return
        T = self.T0r[self.tusk_v]
        self.exposed = [int(t) for t in self.tusk_v if self._fz(self.teeth.getVertexNormal(int(t), True, om.MSpace.kWorld)) > 0.2
                        and not self._skin_hit(self.T0[t], self.FW, 4.0)]
        for v in self.region:
            p = self.S0r[v]; d3 = np.linalg.norm(T - p, axis=1)
            if d3.min() > 3.0: continue
            fw = self._tusk_hits(self.S0[v], self.FW)
            if fw and fw[0][2] > 0: continue                          # inside already at rest: leave it
            dxy = np.linalg.norm(T[:, :2] - p[:2], axis=1)
            if dxy.min() > 1.2: self.side[int(v)] = 0
            else:
                zf = T[dxy <= max(0.45, dxy.min() + 0.15), 2].max()   # tusk front surface around this x/y
                self.side[int(v)] = 1 if p[2] < zf - 0.05 else -1
            self.near[int(v)] = int(self.tusk_v[int(np.argmin(d3))])

    # ---- per pose
    def needs(self):
        """[(skin vertex, teeth vertex or -1, needed forward change of skin minus teeth, weight)] for the current pose"""
        self._frame()
        out = []; self.kinds = dict(cover=0, inside=0, inner=0, red=0)
        S, T = _pts(self.skin), _pts(self.teeth)
        for t in self.exposed:                                        # cover
            r = self._skin_hit(T[t], self.FW, 4.0)
            if not r: continue
            for s in self.skin.getPolygonVertices(r[2]):
                w = 0.5 if self.side.get(s) == -1 else self.tusk_weight
                out.append((s, t, -(r[1] + self.margin), w)); self.kinds['cover'] += 1
        for s, t in (self.near.items() if self.use_inside else ()):    # inside (optional)
            fw = self._tusk_hits(S[s], self.FW)
            if not (fw and fw[0][2] > 0): continue
            tv = self.teeth.getPolygonVertices(fw[0][1])[0]; sd = self.side.get(s, 0)
            bw = self._tusk_hits(S[s], self.BW); back = -((bw[0][0] if bw else 0) + self.margin); front = fw[0][0] + self.margin
            out.append((s, tv, back if sd > 0 else front if sd < 0 else (front if front < -back else back), self.tusk_weight))
            self.kinds['inside'] += 1
        for v in self.inner_v:                                        # inner
            r = self._skin_hit(T[v], self.FW, 4.0)
            if r:                                                     # hidden: enough lip in front of it?
                if r[1] < self.clear and self._fz(self.skin.getPolygonNormal(r[2], om.MSpace.kWorld)) > 0.2:
                    for s in self.skin.getPolygonVertices(r[2]):
                        if s in self.region: out.append((s, v, self.clear - r[1] + 0.03, 1.0)); self.kinds['inner'] += 1
                continue
            r = self._skin_hit(T[v], self.BW, self.reach)
            if not r or self._fz(self.skin.getPolygonNormal(r[2], om.MSpace.kWorld)) <= 0.2: continue
            for s in self.skin.getPolygonVertices(r[2]):
                if s in self.region: out.append((s, v, r[1] + self.inner_margin, 1.0)); self.kinds['inner'] += 1
        if self.red_v:                                                # red
            M = self.skin_dp.inclusiveMatrix(); mi = om.MMeshIntersector(); mi.create(self.skin_dp.node(), M)
            for v in self.red_v:
                try: pom = mi.getClosestPoint(om.MPoint(*T[v]), 1.0)
                except Exception: continue
                if pom is None or pom.face not in self.outer: continue
                cp, n = om.MPoint(pom.point) * M, (om.MVector(pom.normal) * M).normal()   # results come in object space
                nf = self._fz(n)
                if nf <= 0.2: continue
                sd = (T[v][0] - cp.x) * n.x + (T[v][1] - cp.y) * n.y + (T[v][2] - cp.z) * n.z
                if sd <= -self.clear: continue
                d = (sd + self.clear) / max(nf, 0.5) + 0.03
                for s in self.skin.getPolygonVertices(pom.face):
                    if s in self.region: out.append((s, v, d, 1.0)); self.kinds['red'] += 1
        best = {}                                                     # one row per pair, the largest need
        for s, t, d, w in out:
            k = (s, t)
            if k not in best or abs(d) > abs(best[k][0]): best[k] = (d, w)
        return [(s, t, d, w) for (s, t), (d, w) in best.items()]

    def _plug_vals(self): return np.array([c.getAttr(p) for p in self.plugs])

    def _set(self, vals):
        for p, v in zip(self.plugs, vals): c.setAttr(p, float(v))

    def solve(self, start=None, base=None):
        """fix the current pose; start = control values to begin from (default: what they are now); the move limits are
        measured from `base` (default: the values before solving)"""
        if start is not None: self._set(start)
        x0 = self._plug_vals() if base is None else np.asarray(base, float); rep = dict(rounds=[])
        rows = self.needs(); err = sum(w * abs(d) for _, _, d, w in rows); rep['rounds'].append(len(rows))
        for _ in range(self.rounds):
            if not rows: break
            W = np.array([w for _, _, _, w in rows])[:, None]
            A = W * np.array([self.Js[s] - (self.Jt[t] if t >= 0 else 0) for s, t, _, _ in rows])
            b = W[:, 0] * np.array([d for _, _, d, _ in rows])
            lam = self.ridge * (np.trace(A.T @ A) / A.shape[1] + 1e-9)
            x = np.linalg.solve(A.T @ A + lam * np.diag(self.cost ** 2), A.T @ b)
            cur = self._plug_vals(); best = None
            for a in (1.0, 0.5, 0.25):                                # line search: keep a step only if it helps
                new = np.clip(cur + a * x, x0 - self.lim, x0 + self.lim); self._set(new)
                r2 = self.needs(); e2 = sum(w * abs(d) for _, _, d, w in r2)
                if best is None or e2 < best[0]: best = (e2, new, r2)
                if e2 < err * 0.7: break
            if best[0] >= err:                                        # no step helped: back to where we were, stop
                self._set(cur); break
            err, rows = best[0], best[2]; self._set(best[1]); rep['rounds'].append(len(rows))
        d = self._plug_vals() - x0
        rep.update(err=round(float(err), 3), kinds=dict(self.kinds), moved=float(np.abs(d).max()) if self.plugs else 0.0,
                   teeth={p: round(float(v), 3) for p, v, tt in zip(self.plugs, d, self.isteeth) if tt and abs(v) > 1e-3})
        return rep

    def bake(self, frames, smooth=1, warm=True):
        """solve every frame (from the previous frame's answer when `warm`, else from 0), smooth over +-smooth frames,
        key the plugs that moved. Returns a summary."""
        frames = list(frames)
        for p in self.plugs:
            c.cutKey(p.split('.')[0], at=p.split('.')[1], t=(min(frames), max(frames)), cl=True)
        vals = np.zeros((len(frames), len(self.plugs))); err = []; prev = np.zeros(len(self.plugs))
        for i, f in enumerate(frames):
            c.currentTime(f)
            zero = np.zeros(len(self.plugs))                           # limits always from rest, so warm starts can't creep
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
