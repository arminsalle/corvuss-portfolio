#!/usr/bin/env python3
"""Border-connected background removal ONLY (no interior hole pass).
For products with white/light graphics on dark garments (bones, skeleton, x-ray):
loose light-neutral test so gray studio backdrops go too, but enclosed white
graphics are never touched."""
import os, sys
from collections import deque
from PIL import Image, ImageFilter

SRC = os.path.expanduser("~/vanson-site/assets/p")
DST = os.path.expanduser("~/vanson-site/assets/pc")
FEATHER = 2

def is_bg(px, x, y):
    r, g, b = px[x, y]
    mn, mx = min(r, g, b), max(r, g, b)
    return mn >= 170 and mx - mn <= 20

def cutout(path, out):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    px = im.load()
    bg = bytearray(w * h)
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if is_bg(px, x, y) and not bg[y * w + x]:
                bg[y * w + x] = 1; q.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if is_bg(px, x, y) and not bg[y * w + x]:
                bg[y * w + x] = 1; q.append((x, y))
    while q:
        x, y = q.popleft()
        for nx, ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if 0 <= nx < w and 0 <= ny < h and not bg[ny * w + nx] and is_bg(px, nx, ny):
                bg[ny * w + nx] = 1; q.append((nx, ny))
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

for f in sys.argv[1:]:
    cutout(os.path.join(SRC, f + ".jpg"), os.path.join(DST, f + ".webp"))
    print("done", f)
