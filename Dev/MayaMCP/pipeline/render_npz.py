"""python render_npz.py file.npz out_prefix eye(x,y,z|follow) aim size [fov]  -> PNG per frame (tools venv)"""
import os, sys, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import soft_render as R
d = np.load(sys.argv[1]); out = sys.argv[2]; cam = json.loads(sys.argv[3]); size = int(sys.argv[4]) if len(sys.argv) > 4 else 480
meshes = sorted({k.split('_')[0] for k in d.files if k.startswith('m') and k.endswith('_col')})
static = {}
for m in meshes:
    cnt, idx = d[m + '_counts'], d[m + '_idx']; F = []; o = 0
    for n in cnt: F.append(list(idx[o:o + n])); o += n
    static[m] = (F, d[m + '_col'])
for fi in range(len(d['frames'])):
    ms = [(d['f%d_%s' % (fi, m)].astype(float), static[m][0], static[m][1]) for m in meshes if 'f%d_%s' % (fi, m) in d.files]
    body = ms[0][0]
    if cam.get('follow'):
        ctr = np.array([body[:, 0].mean(), cam['follow'], body[:, 2].mean()]); eye = ctr + np.array(cam['offset']); aim = ctr
    else:
        eye, aim = cam['eye'], cam['aim']
    (R.render_z if cam.get('z') else R.render)(ms, eye, aim, size=(size, int(size * cam.get('aspect', 1.25))), fov=cam.get('fov', 40)).save('%s_%03d.png' % (out, fi))
print('rendered', len(d['frames']))
