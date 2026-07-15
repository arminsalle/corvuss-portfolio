#!/usr/bin/env python3
"""Hybrid cutout: AI matte removes the (non-white) backdrop, then enclosed
near-white regions from the SOURCE (white bones/graphics the AI wrongly ate)
are restored on top. Usage: cutout-hybrid.py <name> <ai_png_path> [...]"""
import os, sys
from collections import deque
from PIL import Image, ImageFilter

SRC = os.path.expanduser("~/vanson-site/assets/p")
DST = os.path.expanduser("~/vanson-site/assets/pc")
NW = 221  # near-white threshold

def enclosed_white_mask(im):
    """near-white pixels NOT connected to the border (i.e., enclosed graphics)"""
    w, h = im.size
    px = im.load()
    near = bytearray(w * h)
    for y in range(h):
        base = y * w
        for x in range(w):
            r, g, b = px[x, y]
            if r >= NW and g >= NW and b >= NW:
                near[base + x] = 1
    border = bytearray(w * h)
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            i = y * w + x
            if near[i] and not border[i]:
                border[i] = 1; q.append(i)
    for y in range(h):
        for x in (0, w - 1):
            i = y * w + x
            if near[i] and not border[i]:
                border[i] = 1; q.append(i)
    while q:
        i = q.popleft()
        x, y = i % w, i // w
        for nx, ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if 0 <= nx < w and 0 <= ny < h:
                j = ny * w + nx
                if near[j] and not border[j]:
                    border[j] = 1; q.append(j)
    m = Image.new("L", (w, h), 0)
    mp = m.load()
    for y in range(h):
        base = y * w
        for x in range(w):
            if near[base + x] and not border[base + x]:
                mp[x, y] = 255
    return m

args = sys.argv[1:]
for i in range(0, len(args), 2):
    name, ai_png = args[i], args[i + 1]
    src = Image.open(os.path.join(SRC, name + ".jpg")).convert("RGB")
    ai = Image.open(ai_png).convert("RGBA")
    if ai.size != src.size:
        ai = ai.resize(src.size, Image.LANCZOS)
    keep = enclosed_white_mask(src)
    keep = keep.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(1))
    a_ai = ai.split()[3]
    # final alpha = max(ai alpha, enclosed-white restore mask)
    a = Image.composite(Image.new("L", src.size, 255), a_ai, keep.point(lambda v: 255 if v > 128 else 0))
    out = src.convert("RGBA")
    out.putalpha(a)
    out.save(os.path.join(DST, name + ".webp"), "WEBP", quality=86, method=4)
    print("hybrid done", name)
