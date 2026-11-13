"""Tiny headless preview renderer (no OpenGL needed): depth-sorted shaded polygons with Pillow.
For checking poses from mayapy; not a replacement for viewport captures."""
import numpy as np
from PIL import Image, ImageDraw
def look_at(eye, aim, up=(0, 1, 0)):
    eye, aim, up = np.array(eye, float), np.array(aim, float), np.array(up, float)
    f = aim - eye; f /= np.linalg.norm(f); r = np.cross(f, up); r /= np.linalg.norm(r); u = np.cross(r, f)
    return eye, np.stack([r, u, -f])
def render(meshes, eye, aim, size=(560, 560), fov=40.0, bg=((86, 90, 98), (34, 35, 38)), ss=2, light=(0.4, 0.7, 0.6)):
    """meshes: list of (P (n,3) world, faces list of vertex-index lists, face colours (m,3) 0..1)"""
    W, H = size[0] * ss, size[1] * ss
    img = Image.new('RGB', (W, H)); top, bot = np.array(bg[0]), np.array(bg[1])
    grad = (top[None] * (1 - np.linspace(0, 1, H))[:, None] + bot[None] * np.linspace(0, 1, H)[:, None]).astype(np.uint8)
    img.paste(Image.fromarray(np.repeat(grad[:, None, :], W, axis=1)))
    e, R = look_at(eye, aim); fl = 0.5 * H / np.tan(np.radians(fov) / 2)
    L = np.array(light, float); L /= np.linalg.norm(L)
    polys = []
    for P, F, C in meshes:
        V = (np.asarray(P) - e) @ R.T
        for fi, f in enumerate(F):
            v = V[f]; z = -v[:, 2]
            if (z <= 1).any(): continue
            n = np.cross(P[f[1]] - P[f[0]], P[f[2]] - P[f[0]]); nn = np.linalg.norm(n)
            if nn < 1e-12: continue
            n = n / nn
            view = e - P[f].mean(0); view /= np.linalg.norm(view)
            if np.dot(n, view) < 0: continue                     # back face
            sh = 0.28 + 0.72 * max(0.0, float(np.dot(n, L))) + 0.12 * max(0.0, float(np.dot(n, view)))
            col = tuple(int(255 * min(1.0, c * sh)) for c in C[fi])
            xy = [(W / 2 + fl * vv[0] / zz, H / 2 - fl * vv[1] / zz) for vv, zz in zip(v, z)]
            polys.append((float(z.mean()), xy, col))
    polys.sort(key=lambda t: -t[0])
    d = ImageDraw.Draw(img)
    for _, xy, col in polys: d.polygon(xy, fill=col)
    return img.resize(size, Image.LANCZOS)

def render_z(meshes, eye, aim, size=(420, 420), fov=40.0, bg=((86, 90, 98), (34, 35, 38)), light=(0.4, 0.7, 0.6)):
    """z-buffered version (exact visibility, per-pixel depth) - slower, for checking penetrations"""
    W, H = size
    top, bot = np.array(bg[0], float), np.array(bg[1], float)
    img = (top[None, None] * (1 - np.linspace(0, 1, H))[:, None, None] + bot[None, None] * np.linspace(0, 1, H)[:, None, None]).repeat(W, 1)
    zbuf = np.full((H, W), np.inf)
    e, R = look_at(eye, aim); fl = 0.5 * H / np.tan(np.radians(fov) / 2)
    L = np.array(light, float); L /= np.linalg.norm(L)
    for P, F, C in meshes:
        P = np.asarray(P, float); V = (P - e) @ R.T; z = -V[:, 2]
        sx = W / 2 + fl * V[:, 0] / np.maximum(z, 1e-3); sy = H / 2 - fl * V[:, 1] / np.maximum(z, 1e-3)
        for fi, f in enumerate(F):
            for t in range(1, len(f) - 1):
                tri = (f[0], f[t], f[t + 1])
                if (z[list(tri)] <= 1).any(): continue
                x = sx[list(tri)]; y = sy[list(tri)]; zz = z[list(tri)]
                x0, x1 = int(max(0, np.floor(x.min()))), int(min(W - 1, np.ceil(x.max()))); y0, y1 = int(max(0, np.floor(y.min()))), int(min(H - 1, np.ceil(y.max())))
                if x1 < x0 or y1 < y0: continue
                den = (y[1] - y[2]) * (x[0] - x[2]) + (x[2] - x[1]) * (y[0] - y[2])
                if abs(den) < 1e-9: continue
                n = np.cross(P[tri[1]] - P[tri[0]], P[tri[2]] - P[tri[0]]); nn = np.linalg.norm(n)
                if nn < 1e-12: continue
                n /= nn; view = e - P[list(tri)].mean(0); view /= np.linalg.norm(view)
                if np.dot(n, view) < 0: continue
                sh = 0.28 + 0.72 * max(0.0, float(np.dot(n, L))) + 0.12 * max(0.0, float(np.dot(n, view)))
                gx, gy = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
                a = ((y[1] - y[2]) * (gx - x[2]) + (x[2] - x[1]) * (gy - y[2])) / den
                b = ((y[2] - y[0]) * (gx - x[2]) + (x[0] - x[2]) * (gy - y[2])) / den
                g = 1 - a - b; m = (a >= 0) & (b >= 0) & (g >= 0)
                if not m.any(): continue
                depth = a * zz[0] + b * zz[1] + g * zz[2]
                sub = zbuf[y0:y1 + 1, x0:x1 + 1]; upd = m & (depth < sub)
                sub[upd] = depth[upd]
                img[y0:y1 + 1, x0:x1 + 1][upd] = np.array(C[fi]) * 255 * min(sh, 1.2)
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
