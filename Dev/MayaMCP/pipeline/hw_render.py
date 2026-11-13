"""Headless viewport-style images for rig reviews and tutorials: Maya Hardware 2.0 batch render driven from mayapy.

No GUI and no commandPort needed. The look matches a playblast: shaded colour, smooth mesh preview (the '3' key),
control curves, isolate, wireframe-on-shaded, x-ray, SSAO and 16x MSAA. Output is RGBA PNG; composite a background
afterwards (hw_composite.py, any Python with Pillow).

    R = hw_render.Renderer('/path/shots')
    set_some_pose(); R.shot('smile', eye=(0, 190, 60), aim=(0, 189, 5), fov=50, w=800, h=800, isolate=['geo_grp'])
    R.seq('walk', range(100, 173, 2), eye=(250, 140, 300), aim=(0, 105, 0))      # the scene's own animation
    R.flush()                                                                     # renders everything

How it works
  shot() snapshots every keyable channel of the tracked nodes (controls, animated nodes, deformer envelopes, extras).
  flush() renders the sequences first, each from the scene state it was queued in. Then it keys every snapshot on its own
  spare frame, one block of frames per batch (same size and visibility setup), with a keyed camera, and renders each
  block with one Render call. Finally it removes the keys and nodes it added.
  Curves and joints only draw in hw2's 'Wire On Shaded' mode, so meshes that should not show wire get a zero-alpha wire
  colour."""
import os, re, glob, json, math, shutil, subprocess, tempfile
import maya.cmds as c, maya.api.OpenMaya as om, maya.api.OpenMayaAnim as oma

MAYA = os.environ.get('MAYA_LOCATION') or '/Applications/Autodesk/maya2026/Maya.app/Contents'
RENDER = os.path.join(MAYA, 'bin', 'Render')
WIRE_RGBA = (0.03, 0.09, 0.28, 0.6)
FILTER = {'curves': 'NURBS Curves', 'joints': 'Joints', 'locators': 'Locators', 'surfaces': 'NURBS Surfaces'}


def _long(n):
    r = c.ls(n, l=True)
    return r[0] if r else None


def _shapes(nodes, types):
    out = set()
    for n in nodes or []:
        if not c.objExists(n): continue
        for t in types:
            if c.nodeType(n) == t: out.add(_long(n))
            out.update(c.listRelatives(n, ad=True, type=t, f=True) or [])
    return out


def _mplug(name):
    sl = om.MSelectionList(); sl.add(name); return sl.getPlug(0)


def _read(p):
    try: return p.asDouble()
    except Exception:
        try: return float(p.asInt())
        except Exception: return None


def look_at(eye, aim, up=(0, 1, 0)):
    """Euler (degrees, xyz) that points a Maya camera (looks down -Z) from eye to aim."""
    e, a, u = om.MVector(eye), om.MVector(aim), om.MVector(up)
    z = (e - a).normal(); x = (u ^ z).normal(); y = z ^ x
    m = om.MMatrix([x.x, x.y, x.z, 0, y.x, y.y, y.z, 0, z.x, z.y, z.z, 0, e.x, e.y, e.z, 1])
    r = om.MTransformationMatrix(m).rotation()
    return [math.degrees(v) for v in (r.x, r.y, r.z)]


def default_track():
    """Controls by name, everything that is animated, and deformer envelopes."""
    nodes = set()
    for pat in ('*_Ctrl', '*_ctrl', '*_CTRL', 'CTRL_*', '*:*_Ctrl', '*:*_ctrl', '*:CTRL_*'):
        nodes.update(c.ls(pat, type='transform'))
    for m in c.ls(type=('mesh', 'nurbsCurve'), noIntermediate=True):       # so hide/show between shots is kept
        nodes.update(c.listRelatives(m, p=True) or [])
    for cv in c.ls(type=('animCurveTA', 'animCurveTL', 'animCurveTU')):
        for d in c.listConnections(cv + '.output', s=False, d=True) or []:
            if c.objectType(d, isAType='transform'): nodes.add(d)
    return sorted(nodes)


class Renderer(object):
    def __init__(self, out, track=None, extra_plugs=(), base=20000, smooth=2, ssao=True, msaa=16, line_width=None,
                 wire_rgba=WIRE_RGBA, keep_scene=False, log=print):
        self.out = out; self.base = base; self.smooth = smooth; self.ssao = ssao; self.msaa = msaa
        self.line_width = line_width; self.wire_rgba = wire_rgba; self.keep_scene = keep_scene; self.log = log
        os.makedirs(out, exist_ok=True)
        nodes = track if track is not None else default_track()
        plugs = []
        for n in nodes:
            for a in c.listAttr(n, k=True) or []:
                plugs.append('%s.%s' % (n, a))
        for d in c.ls(type=('blendShape', 'deltaMush', 'skinCluster', 'cluster', 'wire', 'ffd', 'tension')):
            plugs.append(d + '.envelope')
        for b in c.ls(type='blendShape'):
            plugs += ['%s.weight[%d]' % (b, i) for i in (c.getAttr(b + '.weight', mi=True) or [])]
        plugs += list(extra_plugs)
        self.plugs = []
        for p in plugs:
            try:
                mp = _mplug(p)
            except Exception:
                continue
            if mp.isLocked or _read(mp) is None: continue
            src = mp.source()
            if not src.isNull:
                if not src.node().hasFn(om.MFn.kAnimCurve): continue      # driven/constrained: it follows anyway
                if src.node().hasFn(om.MFn.kAnimCurveUnitlessToAngular) or src.node().hasFn(om.MFn.kAnimCurveUnitlessToDistance) \
                        or src.node().hasFn(om.MFn.kAnimCurveUnitlessToUnitless): continue  # set-driven key
            self.plugs.append((p, mp))
        self.batches = {}; self.seqs = []
        self.log('hwrender: tracking %d channels on %d nodes' % (len(self.plugs), len(nodes)))

    # ---------------------------------------------------------------- queue
    def snapshot(self):
        return [_read(mp) for _, mp in self.plugs]

    def _settings(self, w, h, curves, joints, xray, wire, isolate, smooth, ortho, lights):
        vis = None
        if isolate:
            vis = sorted(_shapes(isolate, ('mesh', 'nurbsCurve', 'nurbsSurface')) |
                         set(c.ls([j for j in (c.listRelatives(isolate, ad=True, type='joint', f=True) or [])], l=True)) |
                         set(c.ls(isolate, type='joint', l=True)))
        if wire is True: wired = '*'
        elif wire: wired = sorted(_shapes(wire, ('mesh',)))
        else: wired = []
        return dict(w=int(w), h=int(h), curves=bool(curves), joints=bool(joints), xray=bool(xray), wired=wired, vis=vis,
                    smooth=self.smooth if smooth is None else smooth, ortho=bool(ortho), lights=lights)

    def shot(self, name, eye=None, aim=None, fov=None, w=1600, h=900, wire=False, xray=False, joints=True, curves=True,
             isolate=None, ortho=None, smooth=None, lights=None, shaded=True):
        """Queue a still of the current state (same arguments as a viewport shot helper)."""
        st = self._settings(w, h, curves, joints, xray, wire, isolate, smooth, ortho, lights)
        key = json.dumps(st, sort_keys=True)
        b = self.batches.setdefault(key, dict(settings=st, shots=[]))
        b['shots'].append(dict(name=name, snap=self.snapshot(), cam=(tuple(eye), tuple(aim), fov or 50, ortho)))

    def seq(self, name, frames, eye=None, aim=None, fov=None, w=640, h=640, cam_fn=None, wire=False, xray=False,
            joints=True, curves=True, isolate=None, ortho=None, smooth=None, lights=None):
        """Queue the scene's own animation over frames. cam_fn(frame) -> (eye, aim) for a moving camera."""
        st = self._settings(w, h, curves, joints, xray, wire, isolate, smooth, ortho, lights)
        frames = [int(f) for f in frames]
        cams = [(tuple(cam_fn(f)[0]), tuple(cam_fn(f)[1])) if cam_fn else (tuple(eye), tuple(aim)) for f in frames]
        self.seqs.append(dict(name=name, frames=frames, cams=cams, fov=fov or 50, ortho=ortho, settings=st, snap=self.snapshot()))

    # ---------------------------------------------------------------- scene setup
    def _camera(self, tag):
        t = c.camera(n='hwr_cam_' + tag)[0]
        return t, c.listRelatives(t, s=True, f=True)[0]

    def _key_camera(self, cam, shape, frames, cams, fov, ortho):
        for f, (eye, aim) in zip(frames, cams):
            r = look_at(eye, aim)
            for a, v in zip(('tx', 'ty', 'tz', 'rx', 'ry', 'rz'), list(eye) + r):
                c.setKeyframe(cam, at=a, t=f, v=v)
            c.setKeyframe(shape, at='focalLength', t=f, v=fov)
        c.setAttr(shape + '.orthographic', 1 if ortho else 0)
        if ortho: c.setAttr(shape + '.orthographicWidth', ortho)
        curves = c.listConnections(cam, shape, s=True, d=False, type='animCurve') or []
        if curves: c.filterCurve(curves, filter='euler')
        if curves: c.keyTangent(curves, itt='linear', ott='step')

    def _setup(self, st, cam_shape):
        undo = []
        def sa(plug, *v, **kw):
            try:
                old = c.getAttr(plug)
                if isinstance(old, list) and old and isinstance(old[0], tuple): old = old[0]
                c.setAttr(plug, *v, **kw); undo.append((plug, old, kw))
            except Exception:
                pass
        meshes = [m for m in c.ls(type='mesh', l=True) if not c.getAttr(m + '.intermediateObject')]
        curves = [m for m in c.ls(type=('nurbsCurve', 'nurbsSurface'), l=True) if not c.getAttr(m + '.intermediateObject')]
        vis = set(st['vis']) if st['vis'] is not None else None
        if vis is not None:
            for s in meshes + curves:
                if s not in vis: sa(s + '.lodVisibility', 0)
            if st['joints']:
                for j in c.ls(type='joint', l=True):
                    if j not in vis: sa(j + '.drawStyle', 2)
        # display layers own drawOverride: disconnect while rendering
        layer_links = []; parents = set()
        for s in meshes:
            p = s.rsplit('|', 1)[0]
            while p:
                parents.add(p); p = p.rsplit('|', 1)[0] if '|' in p[1:] else ''
        for n in list(meshes) + sorted(parents):
            for src in c.listConnections(n + '.drawOverride', s=True, d=False, p=True) or []:
                c.disconnectAttr(src, n + '.drawOverride'); layer_links.append((src, n + '.drawOverride'))
        for p in sorted(parents):           # e.g. a geo group set to Reference: its override would win over the shapes'
            try:
                if c.getAttr(p + '.overrideEnabled') and c.getAttr(p + '.overrideVisibility'): sa(p + '.overrideEnabled', 0)
            except Exception:
                pass
        wired = set(meshes) if st['wired'] == '*' else set(st['wired'])
        r, g, b, a = self.wire_rgba
        for s in meshes:
            sa(s + '.overrideEnabled', 1); sa(s + '.overrideRGBColors', 1)
            if s in wired: sa(s + '.overrideColorRGB', r, g, b, type='double3'); sa(s + '.overrideColorA', a)
            else: sa(s + '.overrideColorA', 0)
            if st['smooth']:
                sa(s + '.displaySmoothMesh', 2); sa(s + '.useSmoothPreviewForRender', 1); sa(s + '.renderSmoothLevel', st['smooth'])
                sa(s + '.smoothLevel', st['smooth'])
        if self.line_width:
            for s in curves:
                if c.nodeType(s) == 'nurbsCurve': sa(s + '.lineWidth', self.line_width)
        H = 'hardwareRenderingGlobals.'
        names = c.getAttr(H + 'objectTypeFilterNameArray'); vals = list(c.getAttr(H + 'objectTypeFilterValueArray'))
        want = {FILTER['curves']: st['curves'], FILTER['joints']: st['joints'], FILTER['locators']: False}
        for i, nme in enumerate(names):
            if nme in want: vals[i] = 1 if want[nme] else 0
        old_vals = list(c.getAttr(H + 'objectTypeFilterValueArray'))
        c.setAttr(H + 'objectTypeFilterValueArray', vals, type='Int32Array')
        lit = st['lights'] if st['lights'] is not None else bool([l for l in c.ls(lights=True) if c.getAttr(l + '.visibility')])
        sa(H + 'renderMode', 2)                                  # Wire On Shaded (curves/joints draw; mesh wire is alpha 0)
        sa(H + 'lightingMode', 1 if lit else 0)
        sa(H + 'multiSampleEnable', 1 if self.msaa else 0); sa(H + 'multiSampleCount', self.msaa or 1); sa(H + 'lineAAEnable', 1)
        sa(H + 'ssaoEnable', 1 if self.ssao else 0); sa(H + 'ssaoAmount', 1.2); sa(H + 'ssaoRadius', 8)
        sa(H + 'xrayMode', 1 if st['xray'] else 0); sa(H + 'xrayJointDisplay', 1 if (st['xray'] and st['joints']) else 0)
        R = 'defaultRenderGlobals.'
        c.setAttr(R + 'currentRenderer', 'mayaHardware2', type='string')
        for a, v in (('imageFormat', 32), ('animation', 1), ('outFormatControl', 0), ('putFrameBeforeExt', 1), ('periodInExt', 1),
                     ('extensionPadding', 5)):
            sa(R + a, v)
        sa('defaultResolution.width', st['w']); sa('defaultResolution.height', st['h'])
        sa('defaultResolution.deviceAspectRatio', st['w'] / float(st['h'])); sa('defaultResolution.pixelAspect', 1)
        for cs in c.ls(type='camera', l=True):
            sa(cs + '.renderable', 1 if cs == cam_shape else 0)
        sa(cam_shape + '.backgroundColor', 0, 0, 0, type='double3')
        for l in c.ls(lights=True, l=True):                        # viewport look: no shadows
            for a in ('useRayTraceShadows', 'useDepthMapShadows'): sa(l + '.' + a, 0)
        return undo, layer_links, old_vals

    def _restore(self, undo, layer_links, old_vals):
        for plug, old, kw in reversed(undo):
            try:
                if isinstance(old, tuple): c.setAttr(plug, *old, type='double3')
                else: c.setAttr(plug, old)
            except Exception:
                pass
        for src, dst in layer_links:
            try: c.connectAttr(src, dst, f=True)
            except Exception: pass
        c.setAttr('hardwareRenderingGlobals.objectTypeFilterValueArray', old_vals, type='Int32Array')

    def _apply_static(self, snap):
        """Put back non-animated channels as they were when a sequence was queued."""
        for (p, mp), v in zip(self.plugs, snap):
            if v is None or not mp.source().isNull: continue
            try:
                if abs(_read(mp) - v) > 1e-9: mp.setDouble(v)
            except Exception:
                try: mp.setInt(int(round(v)))
                except Exception: pass

    def _render(self, cam, frames_runs, st, prefix, folder):
        tmp = tempfile.mkdtemp(prefix='hwr_')
        scene = os.path.join(tmp, 'hwr.mb')
        cur = c.file(q=True, sn=True)
        c.file(rename=scene); c.file(save=True, type='mayaBinary', force=True)
        if cur and os.path.isabs(cur) and cur.lower().endswith(('.ma', '.mb')): c.file(rename=cur)
        env = dict(os.environ)
        for k in ('PYTHONHOME', 'PYTHONPATH', 'PYTHONEXECUTABLE'): env.pop(k, None)
        done = []
        for a, b, step in frames_runs:
            cmd = [RENDER, '-r', 'hw2', '-s', str(a), '-e', str(b), '-b', str(step), '-x', str(st['w']), '-y', str(st['h']),
                   '-cam', cam, '-rd', tmp, '-im', prefix, scene]
            r = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=3600)
            if r.returncode: self.log('hwrender: Render failed (%d): %s' % (r.returncode, (r.stdout + r.stderr)[-800:]))
        os.makedirs(folder, exist_ok=True)
        for f in glob.glob(os.path.join(tmp, '**', prefix + '.*.png'), recursive=True):
            m = re.search(r'\.(\d+)\.png$', f)
            if m: done.append((int(m.group(1)), f))
        out = {}
        for fr, f in done:
            out[fr] = f
        if not self.keep_scene: os.remove(scene)
        return out, tmp

    @staticmethod
    def _runs(frames):
        frames = sorted(set(frames)); runs = []; i = 0
        while i < len(frames):
            if i + 1 < len(frames):
                step = frames[i + 1] - frames[i]; j = i + 1
                while j + 1 < len(frames) and frames[j + 1] - frames[j] == step: j += 1
                runs.append((frames[i], frames[j], step)); i = j + 1
            else:
                runs.append((frames[i], frames[i], 1)); i += 1
        return runs

    # ---------------------------------------------------------------- flush
    def flush(self):
        t0 = c.currentTime(q=True); cur_snap = self.snapshot(); written = []
        # 1) sequences: the scene's own animation, each from the state it was queued in
        for k, s in enumerate(self.seqs):
            self._apply_static(s['snap'])
            cam, shape = self._camera('seq%d' % k)
            self._key_camera(cam, shape, s['frames'], s['cams'], s['fov'], s['ortho'])
            undo, links, ov = self._setup(s['settings'], shape)
            files, tmp = self._render(cam, self._runs(s['frames']), s['settings'], 'seq', os.path.join(self.out, 'seq', s['name']))
            self._restore(undo, links, ov); c.delete(cam)
            folder = os.path.join(self.out, 'seq', s['name'])
            for f in glob.glob(os.path.join(folder, '*.png')): os.remove(f)
            for i, fr in enumerate(s['frames']):
                if fr in files:
                    dst = os.path.join(folder, '%s.%04d.png' % (s['name'], i)); shutil.move(files[fr], dst); written.append(dst)
            shutil.rmtree(tmp, ignore_errors=True)
            self.log('hwrender: seq %s %d/%d frames' % (s['name'], len([f for f in s['frames'] if f in files]), len(s['frames'])))
        # 2) stills: key every snapshot on a spare frame, one block per batch
        if self.batches:
            self._apply_static(cur_snap)
            blocks = []; f = self.base
            for key, b in self.batches.items():
                blocks.append((b, list(range(f, f + len(b['shots'])))))
                f += len(b['shots']) + 10
            all_frames = [fr for _, frs in blocks for fr in frs]
            snaps = [sh['snap'] for b, _ in blocks for sh in b['shots']]
            created, touched = self._key_snaps(all_frames, snaps)
            for k, (b, frs) in enumerate(blocks):
                cam, shape = self._camera('b%d' % k)
                fov = b['shots'][0]['cam'][2]; ortho = b['shots'][0]['cam'][3]
                for fr, sh in zip(frs, b['shots']):
                    e, a, fv, _ = sh['cam']; self._key_camera(cam, shape, [fr], [(e, a)], fv, ortho)
                undo, links, ov = self._setup(b['settings'], shape)
                files, tmp = self._render(cam, [(frs[0], frs[-1], 1)], b['settings'], 'still', self.out)
                self._restore(undo, links, ov); c.delete(cam)
                for fr, sh in zip(frs, b['shots']):
                    if fr in files:
                        dst = os.path.join(self.out, sh['name'] + '.png'); os.makedirs(os.path.dirname(dst), exist_ok=True)
                        shutil.move(files[fr], dst); written.append(dst)
                    else:
                        self.log('hwrender: missing still %s' % sh['name'])
                shutil.rmtree(tmp, ignore_errors=True)
                self.log('hwrender: batch %d (%dx%d) %d stills' % (k, b['settings']['w'], b['settings']['h'], len(frs)))
            for cv in created:
                if c.objExists(cv): c.delete(cv)
            for cv in touched:
                if c.objExists(cv): c.cutKey(cv, t=(self.base - 0.5, 10 ** 7), cl=True)
        self.batches = {}; self.seqs = []
        c.currentTime(t0); self._apply_static(cur_snap)
        return written

    def _key_snaps(self, frames, snaps):
        """Bulk keys with MFnAnimCurve: one curve per channel that changes or is already animated."""
        created, touched = [], []
        times = [om.MTime(f, om.MTime.uiUnit()) for f in frames]
        for i, (p, mp) in enumerate(self.plugs):
            vals = [s[i] for s in snaps]
            if any(v is None for v in vals): continue
            src = mp.source()
            if src.isNull:
                if max(vals) - min(vals) < 1e-9 and abs(vals[0] - (_read(mp) or 0)) < 1e-9: continue
                fn = oma.MFnAnimCurve(); obj = fn.create(mp)
                created.append(om.MFnDependencyNode(obj).name())
            else:
                fn = oma.MFnAnimCurve(src.node()); touched.append(om.MFnDependencyNode(src.node()).name())
            fn.addKeys(times, vals, oma.MFnAnimCurve.kTangentLinear, oma.MFnAnimCurve.kTangentStep, keepExistingKeys=True)
        return created, touched


_SESSION = {}


def session(out=None, **kw):
    """One shared Renderer per output folder (survives importlib.reload of the calling helpers)."""
    out = out or os.path.join(tempfile.gettempdir(), 'hwrender')
    if out not in _SESSION: _SESSION[out] = Renderer(out, **kw)
    return _SESSION[out]


def flush_all():
    written = []
    for k in list(_SESSION):
        written += _SESSION.pop(k).flush()
    return written
