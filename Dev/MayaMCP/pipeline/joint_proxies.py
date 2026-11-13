"""Joint proxies for headless renders (generic): Hardware 2.0 batch rendering does not draw joints, so joints are shown
as small spheres and bones made of real meshes with a flat colour, rendered as their own layer and composited over a
see-through body. Proxies are built at the current pose and deleted afterwards."""
import numpy as np, maya.cmds as c, maya.api.OpenMaya as om


def _mat(name, rgb):
    if c.objExists(name): return name + 'SG'
    sh = c.shadingNode('lambert', asShader=True, n=name)
    c.setAttr(sh + '.color', *rgb, type='double3'); c.setAttr(sh + '.incandescence', *[v * 0.55 for v in rgb], type='double3')
    sg = c.sets(renderable=True, noSurfaceShader=True, empty=True, n=name + 'SG'); c.connectAttr(sh + '.outColor', sg + '.surfaceShader')
    return sg


def _bone(p, q, r, sg, grp):
    d = np.array(q) - np.array(p); L = float(np.linalg.norm(d))
    if L < 1e-3: return None
    cyl = c.polyCylinder(r=r, h=L, sx=10, sy=1, ax=(0, 1, 0), n='jviz_bone#')[0]
    y = d / L; x = np.cross(y, [0, 0, 1.0]); x = x if np.linalg.norm(x) > 1e-3 else np.cross(y, [1.0, 0, 0]); x /= np.linalg.norm(x); z = np.cross(x, y)
    mid = (np.array(p) + np.array(q)) / 2
    c.xform(cyl, ws=True, m=[x[0], x[1], x[2], 0, y[0], y[1], y[2], 0, z[0], z[1], z[2], 0, mid[0], mid[1], mid[2], 1])
    c.sets(cyl, e=True, forceElement=sg); c.parent(cyl, grp); return cyl


def proxies(joints, radius=0.8, rgb=(1.0, 0.72, 0.15), name='jviz', bones=True, bone_rgb=None, groups=None):
    """spheres at `joints` (+ bones to their child joints in the set). groups: {rgb: [joints]} to colour sets apart."""
    grp = c.group(em=True, n=name + '_grp')
    sets = groups or {tuple(rgb): joints}
    allj = set(j for js in sets.values() for j in js)
    for k, (col, js) in enumerate(sets.items()):
        sg = _mat('%s_mat%d' % (name, k), col); bsg = _mat('%s_bmat%d' % (name, k), bone_rgb or [v * 0.8 for v in col])
        for j in js:
            p = c.xform(j, q=True, ws=True, t=True)
            s = c.polySphere(r=radius, sx=12, sy=8, n='jviz_ball#')[0]; c.xform(s, ws=True, t=p)
            c.sets(s, e=True, forceElement=sg); c.parent(s, grp)
            if bones:
                for ch in c.listRelatives(j, c=True, type='joint') or []:
                    if ch in allj: _bone(p, c.xform(ch, q=True, ws=True, t=True), radius * 0.35, bsg, grp)
    return grp
