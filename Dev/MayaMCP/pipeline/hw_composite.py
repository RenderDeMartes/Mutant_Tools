"""Composite RGBA renders (hw_render output) over a viewport-style vertical gradient, in place.
usage: python hw_composite.py <file-or-folder> [top r,g,b] [bottom r,g,b]   (0-255; default Maya-like dark gradient)"""
import sys, os
from PIL import Image


def gradient(w, h, top, bot):
    g = Image.new('RGB', (1, h))
    for y in range(h):
        t = y / max(1, h - 1)
        g.putpixel((0, y), tuple(int(round(top[i] + (bot[i] - top[i]) * t)) for i in range(3)))
    return g.resize((w, h))


def one(path, top, bot):
    im = Image.open(path)
    if im.mode != 'RGBA': return False
    bg = gradient(im.width, im.height, top, bot).convert('RGBA')
    bg.alpha_composite(im); bg.convert('RGB').save(path)
    return True


if __name__ == '__main__':
    tgt = sys.argv[1]
    top = tuple(int(v) for v in sys.argv[2].split(',')) if len(sys.argv) > 2 else (84, 89, 97)
    bot = tuple(int(v) for v in sys.argv[3].split(',')) if len(sys.argv) > 3 else (33, 33, 36)
    files = [tgt] if os.path.isfile(tgt) else [os.path.join(r, f) for r, _, fs in os.walk(tgt) for f in fs if f.endswith('.png')]
    n = sum(one(f, top, bot) for f in sorted(files))
    print('composited', n, 'of', len(files))
