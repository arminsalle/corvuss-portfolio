#!/usr/bin/env python3
"""Fetch every product page and extract descriptions + gallery image URLs."""
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

ALLOWED = re.compile(r"</?(p|br|ul|ol|li|strong|b|em|i|h3|h4)( [^>]*)?>", re.I)

def clean_html(frag):
    # strip scripts/styles/comments, keep basic formatting tags only
    frag = re.sub(r"<(script|style).*?</\1>", "", frag, flags=re.S | re.I)
    frag = re.sub(r"<!--.*?-->", "", frag, flags=re.S)
    out, pos = [], 0
    for m in re.finditer(r"<[^>]+>", frag):
        out.append(frag[pos:m.start()])
        if ALLOWED.match(m.group(0)):
            out.append(re.sub(r"\s(class|style|id|align)=\"[^\"]*\"", "", m.group(0)))
        pos = m.end()
    out.append(frag[pos:])
    txt = "".join(out)
    txt = re.sub(r"&nbsp;", " ", txt)
    txt = re.sub(r"\n{3,}", "\n\n", txt)
    txt = re.sub(r"(<br\s*/?>\s*){3,}", "<br><br>", txt, flags=re.I)
    return txt.strip()

prods = json.load(open("products.json"))["products"]
urls = [p["url"].split("#")[0] for p in prods]
seen, details = set(), {}
if os.path.exists("details.json"):
    details = json.load(open("details.json"))

for i, url in enumerate(urls):
    if url in seen or url in details:
        seen.add(url)
        continue
    seen.add(url)
    html = fetch(url)
    if not html:
        details[url] = {}
        continue
    short = re.search(r'<div[^>]*itemprop="description"[^>]*>(.*?)</div>', html, re.S)
    longd = re.search(r'<div[^>]*id="description"[^>]*>(.*?)</section>', html, re.S)
    gal = []
    for g in re.findall(r'data-image-large-src="([^"]+)"', html):
        if g not in gal:
            gal.append(g)
    details[url] = {
        "ds": clean_html(short.group(1))[:3000] if short else "",
        "dl": clean_html(longd.group(1))[:6000] if longd else "",
        "gal": gal[:4],
    }
    if (i + 1) % 25 == 0:
        json.dump(details, open("details.json", "w"))
        print(f"{i+1}/{len(urls)} pages, {len(details)} unique")
    time.sleep(0.25)

json.dump(details, open("details.json", "w"))
print(f"DONE: {len(details)} product pages")
