#!/usr/bin/env python3
"""Fetch every product page and extract size/color attribute options."""
import re, json, time, urllib.request, sys, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"}

def fetch(url, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:
            if i == tries - 1:
                print(f"FAIL {url}: {e}", file=sys.stderr)
                return ""
            time.sleep(2)

prods = json.load(open("products.json"))["products"]
urls = sorted(set(p["url"].split("#")[0] for p in prods))
out = {}
if os.path.exists("sizes.json"):
    out = json.load(open("sizes.json"))

for i, url in enumerate(urls):
    if url in out:
        continue
    html = fetch(url)
    if not html:
        out[url] = {}
        continue
    groups = {}
    for gid, body in re.findall(r'<select[^>]*name="group\[(\d+)\]"[^>]*>(.*?)</select>', html, re.S):
        opts = re.findall(r'<option[^>]*value="(\d+)"[^>]*>\s*([^<]+?)\s*</option>', body)
        groups[gid] = opts
    # group 1 = size on their store; anything else = color/material
    entry = {}
    if "1" in groups and groups["1"]:
        entry["sz"] = groups["1"]
    for gid, opts in groups.items():
        if gid != "1" and opts:
            entry["cl"] = opts
            break
    out[url] = entry
    if (i + 1) % 40 == 0:
        json.dump(out, open("sizes.json", "w"))
        print(f"{i+1}/{len(urls)}")
    time.sleep(0.2)

json.dump(out, open("sizes.json", "w"))
withsz = sum(1 for v in out.values() if v.get("sz"))
print(f"DONE: {len(out)} pages, {withsz} with sizes")
