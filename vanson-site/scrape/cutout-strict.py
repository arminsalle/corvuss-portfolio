#!/usr/bin/env python3
"""Strict border flood-fill for garments whose white graphics touch the white
background: flood only PURE white (>=248, neutral) from borders, then grow the
bg mask a few constrained steps into near-white halo pixels. White appliqués
survive because the flood can't enter their shaded (<248) interiors, and halo
growth is capped at a few px."""
import os, sys
from collections import deque
from PIL import Image, ImageFilter

SRC = os.path.expanduser("~/vanson-site/assets/p")
DST = os.path.expanduser("~/vanson-site/assets/pc")
PURE, HALO, GROW, FEATHER = 248, 205, 4, 2

def cutout(path, out):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    px = im.load()
    def pure(x, y):
        r, g, b = px[x, y]
        return min(r, g, b) >= PURE and max(r, g, b) - min(r, g, b) <= 10
    def halo(x, y):
        r, g, b = px[x, y]
        return min(r, g, b) >= HALO and max(r, g, b) - min(r, g, b) <= 22
    bg = bytearray(w * h)
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if pure(x, y) and not bg[y * w + x]:
                bg[y * w + x] = 1; q.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if pure(x, y) and not bg[y * w + x]:
                bg[y * w + x] = 1; q.append((x, y))
    while q:
        x, y = q.popleft()
        for nx, ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if 0 <= nx < w and 0 <= ny < h and not bg[ny * w + nx] and pure(nx, ny):
                bg[ny * w + nx] = 1; q.append((nx, ny))
    # constrained halo growth
    front = [i for i in range(w * h) if bg[i]]
    for _ in range(GROW):
        nxt = []
        for i in front:
            x, y = i % w, i // w
            for nx, ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
                if 0 <= nx < w and 0 <= ny < h:
                    j = ny * w + nx
                    if not bg[j] and halo(nx, ny):
                        bg[j] = 1; nxt.append(j)
        front = nxt
        if not front:
            break
    a = Image.new("L", (w, h), 255)
    ap = a.load()
    for y in range(h):
        base = y * w
        for x in range(w):
            if bg[base + x]:
                ap[x, y] = 0
    a = a.filter(ImageFilter.MinFilter(3))
    if FEATHER:
        a = a.filter(ImageFilter.GaussianBlur(FEATHER))
    rgba = im.convert("RGBA")
    rgba.putalpha(a)
    rgba.save(out, "WEBP", quality=86, method=4)

for f in sys.argv[1:]:
    cutout(os.path.join(SRC, f + ".jpg"), os.path.join(DST, f + ".webp"))
    print("done", f)
