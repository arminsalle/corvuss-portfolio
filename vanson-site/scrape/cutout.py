#!/usr/bin/env python3
"""Remove white studio background -> WebP with alpha.
Pass 1: border flood-fill over near-white (tolerant of JPEG block noise).
Pass 2: interior near-white components seeded by pure white (encl. holes),
        only if large enough — protects white garments' highlights."""
import os, sys
from collections import deque
from PIL import Image, ImageFilter

SRC = os.path.expanduser("~/vanson-site/assets/p")
DST = os.path.expanduser("~/vanson-site/assets/pc")
os.makedirs(DST, exist_ok=True)
TOL = 34          # near-white threshold (255-TOL)
PURE = 250        # pure-white seed for interior holes
MIN_HOLE = 300    # px, min interior component size to remove
FEATHER = 2

def cutout(path, out):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    px = im.load()
    NW = 255 - TOL
    near = bytearray(w * h)   # near-white mask
    for y in range(h):
        base = y * w
        for x in range(w):
            r, g, b = px[x, y]
            if r >= NW and g >= NW and b >= NW:
                near[base + x] = 1
    bg = bytearray(w * h)
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            i = y * w + x
            if near[i] and not bg[i]:
                bg[i] = 1; q.append(i)
    for y in range(h):
        for x in (0, w - 1):
            i = y * w + x
            if near[i] and not bg[i]:
                bg[i] = 1; q.append(i)
    while q:
        i = q.popleft()
        x, y = i % w, i // w
        for nx, ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if 0 <= nx < w and 0 <= ny < h:
                j = ny * w + nx
                if near[j] and not bg[j]:
                    bg[j] = 1; q.append(j)

    # pass 2: enclosed near-white components with a pure-white seed
    visited = bytearray(bg)
    for start in range(w * h):
        if near[start] and not visited[start]:
            comp, pure, qq = [], False, deque([start])
            visited[start] = 1
            while qq:
                i = qq.popleft()
                comp.append(i)
                x, y = i % w, i // w
                r, g, b = px[x, y]
                if r >= PURE and g >= PURE and b >= PURE:
                    pure = True
                for nx, ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
                    if 0 <= nx < w and 0 <= ny < h:
                        j = ny * w + nx
                        if near[j] and not visited[j]:
                            visited[j] = 1; qq.append(j)
            if pure and len(comp) >= MIN_HOLE:
                for i in comp:
                    bg[i] = 1

    a = Image.new("L", (w, h), 255)
    ap = a.load()
    for y in range(h):
        base = y * w
        for x in range(w):
            if bg[base + x]:
                ap[x, y] = 0
    a = a.filter(ImageFilter.MinFilter(5))
    if FEATHER:
        a = a.filter(ImageFilter.GaussianBlur(FEATHER))
    rgba = im.convert("RGBA")
    rgba.putalpha(a)
    rgba.save(out, "WEBP", quality=86, method=4)

files = sorted(f for f in os.listdir(SRC) if f.endswith(".jpg"))
only = sys.argv[1:] if len(sys.argv) > 1 else None
if only:
    files = [f for f in files if f in only]
for i, f in enumerate(files):
    out = os.path.join(DST, f.replace(".jpg", ".webp"))
    try:
        cutout(os.path.join(SRC, f), out)
    except Exception as e:
        print("FAIL", f, e)
    if (i + 1) % 50 == 0:
        print(f"{i+1}/{len(files)}")
print("done", len(files))
