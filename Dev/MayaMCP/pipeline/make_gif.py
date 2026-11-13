"""GIF from a viewport sequence folder: python mkgif.py <folder> <out.gif> [width] [fps]"""
import sys, os
from PIL import Image
folder, out = sys.argv[1], sys.argv[2]
w = int(sys.argv[3]) if len(sys.argv) > 3 else 480
fps = float(sys.argv[4]) if len(sys.argv) > 4 else 20
files = sorted(f for f in os.listdir(folder) if f.endswith('.png'))
frames = []
for f in files:
    im = Image.open(os.path.join(folder, f)).convert('RGB')
    im = im.resize((w, int(w * im.height / im.width)), Image.LANCZOS)
    frames.append(im)
# one shared palette from a few frames keeps the grey viewport smooth
pal = frames[len(frames) // 2].quantize(colors=128, method=Image.MEDIANCUT)
q = [fr.quantize(palette=pal, dither=Image.NONE) for fr in frames]
q[0].save(out, save_all=True, append_images=q[1:], duration=int(1000 / fps), loop=0, optimize=True, disposal=1)
print(out, len(q), 'frames', os.path.getsize(out) // 1024, 'KB')
