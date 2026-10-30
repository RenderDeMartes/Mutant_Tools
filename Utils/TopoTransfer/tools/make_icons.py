"""
TopoTransfer and Meta Mutant icons in the Mutant Tools style: pastel rounded tile, bold black line art.

    python tools/make_icons.py              # writes Mutant_Tools/Icons/TopoTransfer.png and MetaMutant.png
    python tools/make_icons.py <folder> --preview

Needs Pillow.
"""
import math
import os
import sys

from PIL import Image, ImageDraw

OUT = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "Icons")
S = 4  # supersampling
N = 512
INK = (24, 24, 24, 255)
W = 20  # stroke at 512


def canvas(bg):
    im = Image.new("RGBA", (N * S, N * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, N * S - 1, N * S - 1), radius=64 * S, fill=bg)
    return im, d


def P(pts):
    return [(x * S, y * S) for x, y in pts]


def poly(d, pts, w=W, closed=False, fill=INK):
    pts = list(pts) + ([pts[0]] if closed else [])
    d.line(P(pts), fill=fill, width=int(w * S), joint="curve")
    for x, y in (pts[0], pts[-1]):  # round caps
        r = w * S / 2
        d.ellipse((x * S - r, y * S - r, x * S + r, y * S + r), fill=fill)


def ellipse_pts(cx, cy, rx, ry, a0=0, a1=360, n=96, rot=0.0):
    out = []
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n)
        x, y = rx * math.cos(a), ry * math.sin(a)
        c, s = math.cos(rot), math.sin(rot)
        out.append((cx + x * c - y * s, cy + x * s + y * c))
    return out


def bezier(p0, p1, p2, n=48):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
             (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in (i / n for i in range(n + 1))]


def arrow_head(d, tip, frm, size=34):
    ang = math.atan2(tip[1] - frm[1], tip[0] - frm[0])
    left = (tip[0] - size * math.cos(ang - 0.55), tip[1] - size * math.sin(ang - 0.55))
    right = (tip[0] - size * math.cos(ang + 0.55), tip[1] - size * math.sin(ang + 0.55))
    poly(d, [left, tip, right])


def save(im, name):
    im.resize((N, N), Image.LANCZOS).save(os.path.join(OUT, name))


# ----------------------------------------------------------------- TopoTransfer
# a flat quad grid, and the same grid wrapped onto a round shape: topology carried over
im, d = canvas((150, 214, 196, 255))
x0, y0, size, cells = 62, 262, 176, 3
step = size / cells
for i in range(cells + 1):
    poly(d, [(x0 + i * step, y0), (x0 + i * step, y0 + size)])
    poly(d, [(x0, y0 + i * step), (x0 + size, y0 + i * step)])
cx, cy, r = 348, 196, 104


def ball(u, v, k=0.75):
    """The flat grid's square pulled towards a disc and tilted: the same 3x3 quads, bulged."""
    du, dv = u * math.sqrt(1 - v * v / 2), v * math.sqrt(1 - u * u / 2)
    x, y = u + (du - u) * k, v + (dv - v) * k
    x, y = x * (1 + 0.18 * y), y  # a little perspective: wider at the bottom
    a = math.radians(-12)
    return cx + r * (x * math.cos(a) - y * math.sin(a)), cy + r * (x * math.sin(a) + y * math.cos(a))


for i in range(cells + 1):
    t = -1 + 2 * i / cells
    poly(d, [ball(t, -1 + 2 * j / 48) for j in range(49)])
    poly(d, [ball(-1 + 2 * j / 48, t) for j in range(49)])
curve = bezier((150, 236), (150, 120), (210, 118))
poly(d, curve)
arrow_head(d, curve[-1], curve[-6])
save(im, "TopoTransfer.png")

# ----------------------------------------------------------------- Meta Mutant
# a head with a stitched seam (a mutant) and a DNA helix (the MetaHuman DNA)
im, d = canvas((198, 182, 240, 255))
hx, hy, hrx, hry = 222, 228, 118, 152
poly(d, ellipse_pts(hx, hy, hrx, hry, 0, 360), closed=True)
poly(d, ellipse_pts(hx - hrx + 1, hy + 18, 12, 22, 100, 260, n=32), w=16)  # ears
poly(d, ellipse_pts(hx + hrx - 1, hy + 18, 12, 22, -80, 80, n=32), w=16)
for ex in (hx - 44, hx + 44):  # eyes
    d.ellipse(P([(ex - 13, hy + 2 - 13), (ex + 13, hy + 2 + 13)]), fill=INK)
poly(d, ellipse_pts(hx, hy + 58, 40, 22, 20, 160, n=32))  # smile
seam = bezier((150, 176), (210, 160), (282, 104), n=64)  # a stitched scar across the forehead
poly(d, seam, w=14)
for t in (0.15, 0.38, 0.62, 0.85):  # stitches across it
    i = int(t * (len(seam) - 1))
    (x1, y1), (x2, y2) = seam[i - 1], seam[i + 1]
    nx, ny = -(y2 - y1), x2 - x1
    ln = math.hypot(nx, ny) or 1
    nx, ny = nx / ln * 20, ny / ln * 20
    x, y = seam[i]
    poly(d, [(x - nx, y - ny), (x + nx, y + ny)], w=14)
# DNA badge
bx, by, br = 392, 392, 92
d.ellipse(P([(bx - br, by - br), (bx + br, by + br)]), fill=(255, 226, 150, 255))
poly(d, ellipse_pts(bx, by, br, br), closed=True, w=16)
top, bottom = by - 58, by + 58
for phase in (0, math.pi):
    pts = [(bx + 34 * math.sin(phase + (yy - top) / (bottom - top) * 2 * math.pi), yy)
           for yy in [top + (bottom - top) * i / 48 for i in range(49)]]
    poly(d, pts, w=13)
for i in range(1, 6):
    yy = top + (bottom - top) * i / 6
    a = (yy - top) / (bottom - top) * 2 * math.pi
    xa, xb = bx + 34 * math.sin(a), bx + 34 * math.sin(a + math.pi)
    if abs(xa - xb) > 14:
        poly(d, [(min(xa, xb) + 8, yy), (max(xa, xb) - 8, yy)], w=9)
save(im, "MetaMutant.png")

# preview: full size, and menu sizes on Maya's grey
if "--preview" not in sys.argv:
    sys.exit(0)
sheet = Image.new("RGBA", (2 * 256 + 4 * 40 + 40, 256), (68, 68, 68, 255))
for i, n in enumerate(("TopoTransfer.png", "MetaMutant.png")):
    icon = Image.open(os.path.join(OUT, n))
    sheet.alpha_composite(icon.resize((256, 256), Image.LANCZOS), (i * 256, 0))
    for j, s in enumerate((20, 32)):
        sheet.alpha_composite(icon.resize((s, s), Image.LANCZOS), (512 + 20 + i * 80 + j * 36, 100))
sheet.save(os.path.join(OUT, "icons_preview.png"))
print("ok")
