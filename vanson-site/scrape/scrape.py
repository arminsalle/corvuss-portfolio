#!/usr/bin/env python3
"""Crawl vansonleathers.com category pages and extract all products."""
import re, json, time, urllib.request, urllib.error, sys

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

cats = [l.strip() for l in open("categories.txt") if l.strip()]
products = {}
cat_meta = {}

for cat_url in cats:
    slug = cat_url.rsplit("/", 1)[1]
    page = 1
    while True:
        url = cat_url if page == 1 else f"{cat_url}?page={page}"
        html = fetch(url)
        if not html:
            break
        if page == 1:
            m = re.search(r'<h1[^>]*>([^<]+)</h1>', html)
            desc = re.search(r'id="category-description"[^>]*>(.*?)</div>', html, re.S)
            cat_meta[slug] = {
                "url": cat_url,
                "title": (m.group(1).strip() if m else slug),
                "desc": re.sub(r"<[^>]+>", " ", desc.group(1)).strip()[:500] if desc else "",
            }
        # PrestaShop product miniatures
        blocks = re.findall(r'<article[^>]*class="[^"]*product-miniature[^"]*".*?</article>', html, re.S)
        found_new = 0
        for b in blocks:
            link = re.search(r'href="(https://www\.vansonleathers\.com/[^"]+?\.html[^"]*)"', b)
            name = re.search(r'class="[^"]*product-title[^"]*"[^>]*>\s*<a[^>]*>([^<]+)</a>', b, re.S)
            if not name:
                name = re.search(r'<a[^>]*class="[^"]*"[^>]*title="([^"]+)"', b)
            price = (re.search(r'class="regular-price"[^>]*>\s*([^<]+)', b)
                     or re.search(r'<meta itemprop="price" content="([^"]+)"', b)
                     or re.search(r'class="price"[^>]*>\s*([^<]+)', b))
            img = re.search(r'data-full-size-image-url="([^"]+)"', b) or re.search(r'<img[^>]+src="([^"]+)"', b)
            if not link:
                continue
            purl = link.group(1).split("?")[0]
            if purl not in products:
                found_new += 1
                products[purl] = {
                    "url": purl,
                    "name": name.group(1).strip() if name else "",
                    "price": price.group(1).strip() if price else "",
                    "img": img.group(1) if img else "",
                    "cats": [],
                }
            if slug not in products[purl]["cats"]:
                products[purl]["cats"].append(slug)
        # pagination: check for a next page link
        has_next = re.search(r'rel="next"', html) or re.search(r'page=%d"' % (page + 1), html)
        print(f"{slug} p{page}: {len(blocks)} blocks, {found_new} new (total {len(products)})")
        if not blocks or not has_next:
            break
        page += 1
        time.sleep(0.4)
    time.sleep(0.4)

json.dump({"categories": cat_meta, "products": list(products.values())}, open("products.json", "w"), indent=1)
print(f"\nDONE: {len(products)} products, {len(cat_meta)} categories")
