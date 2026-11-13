"""Copy a scene's look (per-face material assignments, material colours, directional light rig) to other versions of
the same asset. Meshes are matched by name; faces by index when the face count matches, otherwise the mesh gets its
majority material. Generic: works for any asset whose meshes keep their names across versions.

    look_transfer.export('/path/look.json')        # in the finished scene
    look_transfer.apply('/path/look.json')         # in an older version (e.g. to re-shoot early steps in colour)"""
import json, maya.cmds as c

SHADER_ATTRS = ('color', 'specularColor', 'eccentricity', 'diffuse', 'specularRollOff', 'reflectivity', 'transparency')


def _faces(members, mesh_t):
    out = []
    for m in c.ls(members or [], fl=False):
        node = m.split('.')[0]
        t = c.listRelatives(node, p=True)[0] if c.nodeType(node) == 'mesh' else node
        if t.split('|')[-1] != mesh_t: continue
        if '.f[' not in m:
            return 'all'
        for part in c.ls(m, fl=True):
            out.append(int(part.split('[')[-1][:-1]))
    return out


def export(path, meshes=None, light_group=None):
    meshes = meshes or sorted({c.listRelatives(m, p=True)[0] for m in c.ls(type='mesh', noIntermediate=True)})
    data = dict(materials={}, meshes={}, lights=[])
    for t in meshes:
        shp = c.listRelatives(t, s=True, noIntermediate=True) or []
        if not shp: continue
        nf = c.polyEvaluate(t, f=True)
        sgs = set(c.listConnections(shp[0], type='shadingEngine') or [])
        assign = {}
        for sg in sgs:
            f = _faces(c.sets(sg, q=True), t)
            if f == 'all': f = list(range(nf))
            if not f: continue
            sh = (c.listConnections(sg + '.surfaceShader', s=True, d=False) or [None])[0]
            if not sh: continue
            assign[sh] = f
            if sh not in data['materials']:
                attrs = {}
                for a in SHADER_ATTRS:
                    if c.attributeQuery(a, node=sh, exists=True):
                        v = c.getAttr(sh + '.' + a); attrs[a] = list(v[0]) if isinstance(v, list) else v
                data['materials'][sh] = dict(type=c.nodeType(sh), attrs=attrs)
        data['meshes'][t] = dict(faces=nf, assign=assign)
    lights = c.listRelatives(light_group, ad=True, type='light') if light_group else c.ls(type='directionalLight')
    for l in lights or []:
        t = c.listRelatives(l, p=True)[0]
        data['lights'].append(dict(name=t, type=c.nodeType(l), rotate=list(c.getAttr(t + '.r')[0]),
                                   intensity=c.getAttr(l + '.intensity'), color=list(c.getAttr(l + '.color')[0]),
                                   group=(c.listRelatives(t, p=True) or [None])[0]))
    json.dump(data, open(path, 'w'))
    return {k: len(v) for k, v in data.items()}


def material(name, spec):
    if not c.objExists(name):
        c.shadingNode(spec['type'], asShader=True, n=name)
        for a, v in spec['attrs'].items():
            try:
                if isinstance(v, list): c.setAttr(name + '.' + a, *v, type='double3')
                else: c.setAttr(name + '.' + a, v)
            except Exception:
                pass
    sg = (c.listConnections(name + '.outColor', d=True, s=False, type='shadingEngine') or [None])[0]
    if not sg:
        sg = c.sets(renderable=True, noSurfaceShader=True, empty=True, n=name + 'SG')
        c.connectAttr(name + '.outColor', sg + '.surfaceShader', f=True)
    return sg


# (keyword in an old mesh name, reference mesh in the look file), e.g. (('teeth', 'teeth_geo'), ('head', 'body_geo'))
AUTO = ()


def apply(path, meshes=None, lights=True, rename_map=None, auto=True):
    """rename_map: {'old scene mesh': 'reference mesh'} for meshes that had other names in that version.
    auto: meshes still on the default shader get a reference picked by name keyword (teeth, eye, head...)."""
    data = json.load(open(path)); done = {}
    targets = [t for t in data['meshes']] if meshes is None else meshes
    rename_map = dict(rename_map or {})
    if auto:
        for shp in c.ls(type='mesh', noIntermediate=True):
            t = c.listRelatives(shp, p=True)[0]
            if t in data['meshes'] or t in rename_map: continue
            if (c.listConnections(shp, type='shadingEngine') or ['initialShadingGroup'])[0] != 'initialShadingGroup': continue
            ref = next((r for k, r in AUTO if k in t.lower() and r in data['meshes']), None)
            if ref: rename_map[t] = ref
    for here, ref in [(m, m) for m in targets] + list(rename_map.items()):
        if not c.objExists(here) or ref not in data['meshes']: continue
        spec = data['meshes'][ref]; nf = c.polyEvaluate(here, f=True)
        if nf == spec['faces']:
            for sh, faces in spec['assign'].items():
                sg = material(sh, data['materials'][sh])
                c.sets(['%s.f[%d]' % (here, f) for f in faces], e=True, forceElement=sg)
            done[here] = 'faces'
        else:
            sh = max(spec['assign'], key=lambda k: len(spec['assign'][k]))
            c.sets(here, e=True, forceElement=material(sh, data['materials'][sh])); done[here] = 'majority ' + sh
    if lights and data['lights'] and not c.objExists(data['lights'][0]['name']):
        for L in data['lights']:
            grp = L['group']
            if grp and not c.objExists(grp): c.group(em=True, n=grp)
            shp = c.directionalLight(n=L['name'] + 'Shape', i=L['intensity'], rgb=L['color'])
            t = c.rename(c.listRelatives(shp, p=True)[0], L['name']); c.setAttr(t + '.r', *L['rotate'])
            if grp: c.parent(t, grp)
        done['lights'] = len(data['lights'])
    return done
