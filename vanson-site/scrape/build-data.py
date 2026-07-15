#!/usr/bin/env python3
"""Transform scraped products.json (+details.json) into site data:
data/products.js (deduped catalog) and data/details.js (per-product content)."""
import json, re, os

HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE, "products.json")))
products = d["products"]
details_raw = {}
dp = os.path.join(HERE, "details.json")
if os.path.exists(dp):
    details_raw = json.load(open(dp))
sizes_raw = {}
sp = os.path.join(HERE, "sizes.json")
if os.path.exists(sp):
    sizes_raw = json.load(open(sp))

GROUPS = [
    ("limited",     "Limited & New",      ["823-", "824-", "826-", "287-", "392-"]),
    ("traditional", "Traditional",        ["111-", "695-", "696-", "698-", "699-"]),
    ("sportrider",  "SportRider",         ["114-", "703-", "704-", "707-", "710-"]),
    ("casual",      "Casual & Street",    ["122-", "725-", "727-", "840-", "36-"]),
    ("adventure",   "Adventure Touring",  ["827-", "828-", "830-", "832-"]),
    ("military",    "Military & Police",  ["125-", "731-", "733-"]),
    ("racing",      "Racing Suits",       ["131-", "72-", "742-", "743-", "746-", "750-"]),
    ("pants",       "Pants & Chaps",      ["110-", "127-", "128-", "737-"]),
    ("gloves",      "Gloves",             ["66-", "129-", "130-"]),
    ("bags",        "Bags & Totes",       ["74-", "147-", "884-"]),
    ("tees",        "Tees & Sweats",      ["73-", "133-", "752-"]),
    ("armor",       "Armor & Protection", ["763-", "764-", "757-", "778-", "779-", "781-", "878-", "879-"]),
    ("accessories", "Accessories",        ["94-", "753-", "755-", "759-", "761-", "882-"]),
]

def clean_name(n):
    return re.sub(r"\s+", " ", n).strip()

# pass 1: merge category memberships across duplicate listings
def key_of(p):
    return (clean_name(p["name"]).upper(), p["price"].strip(), p["img"].rsplit("/", 1)[-1])

merged_cats = {}
for p in products:
    merged_cats.setdefault(key_of(p), set()).update(p["cats"])

# pass 2: build deduped catalog, group by priority over merged cats
out, details_out, seen = [], {}, set()
for i, p in enumerate(products):
    key = key_of(p)
    if key in seen:
        continue
    seen.add(key)
    cats = merged_cats[key]
    group = None
    for gid, glabel, prefixes in GROUPS:
        if any(c.startswith(pref) for c in cats for pref in prefixes):
            group = gid
            break
    if group is None:
        group = "accessories"
    pid = len(out)
    base = f"p{i+1:04d}"
    out.append({
        "id": pid,
        "n": clean_name(p["name"]),
        "pr": p["price"].strip(),
        "im": f"assets/pc/{base}.webp?v=4",
        "u": p["url"],
        "g": group,
    })
    det = details_raw.get(p["url"].split("#")[0], {})
    dl = det.get("dl", "")
    # strip PrestaShop metadata junk (reference codes, stock, data sheet table)
    for marker in ("Reference ", "Data sheet", "In stock "):
        idx = dl.find(marker)
        if idx > 100:
            dl = dl[:idx]
    dl = re.sub(r"(<(p|br|ul|li|h3|h4)[^>]*>\s*)+$", "", dl).strip()
    szd = sizes_raw.get(p["url"].split("#")[0], {})
    details_out[pid] = {
        "ds": det.get("ds", ""),
        "dl": dl,
        "gal": det.get("gal", [])[:4],
        "sz": szd.get("sz", []),
        "cl": szd.get("cl", []),
    }

groups_js = [{"id": gid, "label": glabel} for gid, glabel, _ in GROUPS]
counts = {}
for p in out:
    counts[p["g"]] = counts.get(p["g"], 0) + 1
for g in groups_js:
    g["count"] = counts.get(g["id"], 0)

root = os.path.dirname(HERE)
os.makedirs(os.path.join(root, "data"), exist_ok=True)
with open(os.path.join(root, "data", "products.js"), "w") as f:
    f.write("window.VANSON_GROUPS = ")
    json.dump(groups_js, f)
    f.write(";\nwindow.VANSON_PRODUCTS = ")
    json.dump(out, f, separators=(",", ":"))
    f.write(";\n")
with open(os.path.join(root, "data", "details.js"), "w") as f:
    f.write("window.VANSON_DETAILS = ")
    json.dump(details_out, f, separators=(",", ":"))
    f.write(";\n")

print("groups:", [(g["id"], g["count"]) for g in groups_js])
print("total (deduped):", len(out), "of", len(products))
withdesc = sum(1 for v in details_out.values() if v["ds"] or v["dl"])
print("with descriptions:", withdesc)
