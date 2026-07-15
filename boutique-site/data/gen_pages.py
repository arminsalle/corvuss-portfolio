#!/usr/bin/env python3
"""Generate all internal subpages for the Boutique Realty concept site."""
import json, os, html, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, 'data')

agents = json.load(open(f'{D}/agents.json'))
props  = json.load(open(f'{D}/properties.json'))
comms  = json.load(open(f'{D}/communities.json'))
careers = json.load(open(f'{D}/careers.json'))

def esc(s): return html.escape(s or '')

COMM_NAMES = {
    'hoboken':'Hoboken','jersey-city':'Jersey City','weehawken-edgewater':'Weehawken / Edgewater',
    'montclair':'Montclair','westfield':'Westfield','rumson-fairhaven':'Rumson / Fair Haven',
    'holmdel-coltsneck':'Holmdel / Colts Neck','red-bank-middletown':'Red Bank / Middletown',
    'shore-towns':'The Shore Towns'}

COMM_FALLBACK = {
    'hoboken': ["The mile-square city on the Hudson — brownstone streets, a legendary waterfront and skyline views that never get old. Hoboken is the heart of the Gold Coast and home to our second office.",
                "From classic walk-ups on Bloomfield Street to full-amenity towers along the water, Boutique Realty has represented Hoboken buyers, sellers and renters since 2009."],
    'weehawken-edgewater': ["Perched above the Hudson with front-row views of Manhattan, Weehawken and Edgewater pair dramatic waterfront living with quick ferry and light-rail access to the city.",
                "From Port Imperial towers to hillside homes, these markets move quickly — local representation matters."]}

def shell(depth, title, body, crumb, active=''):
    up = '../' * depth
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(title)} — Boutique Realty New Jersey</title>
  <link rel="stylesheet" href="{up}styles.css" />
</head>
<body>
  <header id="header" class="scrolled">
    <a class="logo" href="{up}">Boutique Realty<small>New Jersey · Est. 2009</small></a>
    <nav class="desktop">
      <a href="{up}for-sale/">For Sale</a>
      <a href="{up}for-rent/">For Rent</a>
      <a href="{up}#development">Developments</a>
      <a href="{up}#communities">Communities</a>
      <a href="{up}#team">The Team</a>
    </nav>
    <a class="header-cta" href="{up}#contact">Contact</a>
  </header>

  <section class="panel subpage">
    <span class="crumb">{crumb}</span>
{body}
  </section>

  <footer>
    <div class="foot-grid">
      <div class="foot-brand">
        <span class="logo">Boutique Realty<small>New Jersey · Est. 2009</small></span>
        <p>Full-service real estate — residential, new development, investment,
        multi-family and commercial — across the entire state of New Jersey.</p>
      </div>
      <div class="foot-col">
        <h4>Offices</h4>
        <div class="foot-office"><b>Jersey City — HQ</b><span>215 Newark Ave, Jersey City, NJ 07302</span><a href="tel:+12014335500">201.433.5500</a></div>
        <div class="foot-office"><b>Hoboken</b><a href="tel:+12015330050">201.533.0050</a></div>
        <div class="foot-office"><b>Shrewsbury</b><a href="tel:+17329331900">732.933.1900</a></div>
      </div>
      <div class="foot-col">
        <h4>Explore</h4>
        <a href="{up}for-sale/">For Sale</a>
        <a href="{up}for-rent/">For Rent</a>
        <a href="{up}commercial/">Commercial</a>
        <a href="{up}developments/600-harrison/">Developments</a>
        <a href="{up}careers/">Careers</a>
      </div>
      <div class="foot-col">
        <h4>Follow</h4>
        <a href="https://www.instagram.com/boutique_realty/" target="_blank" rel="noopener">Instagram</a>
        <a href="https://www.facebook.com/boutiquerealtynj/" target="_blank" rel="noopener">Facebook</a>
        <a href="mailto:info@boutiquerealtynj.com">info@boutiquerealtynj.com</a>
      </div>
    </div>
    <div class="legal">
      <span>© 2026 Lana Walsh Falcicchio · Boutique Realty, New Jersey. All rights reserved.</span>
      <span>Concept redesign — <a href="https://corvuss.net" target="_blank" rel="noopener">CORVUSS</a></span>
    </div>
  </footer>
</body>
</html>
"""

def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w').write(content)

def cta(up, heading="Ready to see it in person?"):
    return f"""<div class="cta-band">
      <h3>{heading} <em>Let's talk.</em></h3>
      <div class="hero-ctas" style="margin:0">
        <a class="btn solid" href="mailto:info@boutiquerealtynj.com">info@boutiquerealtynj.com</a>
        <a class="btn" href="tel:+12014335500">201.433.5500</a>
      </div>
    </div>"""

# ---------------- agents ----------------
for a in agents:
    up = '../../'
    img = a.get('local')
    img_html = f'<div class="frame"><img src="{up}{esc(img)}" alt="{esc(a["name"])}"></div>' if img else ''
    rows = []
    if a.get('phone'): rows.append(f'<a href="tel:+1{a["phone"].replace(".","")}"><b>Phone</b><span>{esc(a["phone"])}</span></a>')
    if a.get('email'): rows.append(f'<a href="mailto:{esc(a["email"])}"><b>Email</b><span>{esc(a["email"])}</span></a>')
    if a.get('instagram'): rows.append(f'<a href="{esc(a["instagram"])}" target="_blank" rel="noopener"><b>Instagram</b><span>@{esc(a["instagram"].rstrip("/").split("/")[-1])}</span></a>')
    rows.append('<span><b>Office</b><span>215 Newark Ave, Jersey City, NJ 07302</span></span>')
    bio = a.get('bio_paras') or []
    if bio:
        bio_html = '\n'.join(f'<p>{esc(p)}</p>' for p in bio)
    else:
        bio_html = f'<p>{esc(a["name"])} is a {esc((a.get("title") or "member of the team").lower())} at Boutique Realty, serving buyers, sellers and renters across New Jersey’s Gold Coast. Reach out directly or through our Jersey City office.</p>'
    body = f"""    <h1 class="display">{esc(a['name'])}</h1>
    <div class="agent-hero">
      {img_html}
      <div>
        <span class="crumb" style="margin-top:0.6rem">{esc(a.get('title') or '')}</span>
        <div class="contact-rows">{''.join(rows)}</div>
        <div class="bio">{bio_html}</div>
      </div>
    </div>
    {cta(up, "Work with " + esc(a['name'].split()[0]) + "?")}
    <div class="back-row"><a class="text-link" href="{up}#team">← Back to the team</a></div>"""
    crumb = f'<a href="{up}">Home</a> &nbsp;/&nbsp; <a href="{up}#team">The Team</a> &nbsp;/&nbsp; {esc(a["name"])}'
    write(f'agents/{a["slug"]}/index.html', shell(2, a['name'], body, crumb))

# ---------------- listings ----------------
def prop_card(p, up):
    img = (p.get('photo_local') or [None])[0] or p.get('local')
    price = f"${p['price']:,}" + (' <small>/mo</small>' if p['kind']=='rent' else '')
    street = p['address'].split(',')[0].title().replace('Jc','JC')
    rest = ', '.join(x.strip() for x in p['address'].split(',')[1:])
    rest = re.sub(r'\bJC\b|\bJc\b', 'Jersey City', rest)
    specs = []
    if p.get('beds'): specs.append(f"{p['beds']} Bed")
    if p.get('baths'): specs.append(f"{p['baths']} Bath")
    if p.get('sqft'): specs.append(f"{p['sqft']} Sq Ft")
    if p.get('acres'): specs.append(f"{p['acres']} Acres")
    if p.get('type') and p['type']!='Rental': specs.append(p['type'])
    spec_html = ''.join(f'<span>{esc(s)}</span>' for s in specs[:4])
    return f"""<a class="card reveal in" href="{up}listings/{p['slug']}/">
  <div class="frame"><span class="tag">{'Exclusive' if p['kind']=='sale' else 'For Rent'}</span><img src="{up}{esc(img)}" alt="{esc(street)}" loading="lazy"></div>
  <div class="meta"><div class="addr"><b>{esc(street)}</b>{esc(rest)}</div><div class="price">{price}</div></div>
  <div class="specs">{spec_html}</div>
</a>"""

for p in props:
    up = '../../'
    photos = p.get('photo_local') or []
    g = ''
    if photos:
        g += f'<div class="frame g-main"><img src="{up}{esc(photos[0])}" alt="{esc(p["address"])}"></div>\n'
        for ph in photos[1:]:
            g += f'<div class="frame"><img src="{up}{esc(ph)}" alt="" loading="lazy"></div>\n'
    street = p['address'].split(',')[0].title().replace('Jc','JC')
    rest = ', '.join(x.strip() for x in p['address'].split(',')[1:])
    rest = re.sub(r'\bJC\b|\bJc\b', 'Jersey City', rest)
    price = f"${p['price']:,}" + (' <small>/ month</small>' if p['kind']=='rent' else '')
    specs = []
    if p.get('beds'): specs.append(f"{p['beds']} Bed")
    if p.get('baths'): specs.append(f"{p['baths']} Bath")
    if p.get('sqft'): specs.append(f"{p['sqft']} Sq Ft")
    if p.get('acres'): specs.append(f"{p['acres']} Acres")
    if p.get('type') and p['type']!='Rental': specs.append(p['type'])
    if p.get('mls'): specs.append(f"MLS #{p['mls']}")
    spec_html = ''.join(f'<span>{esc(s)}</span>' for s in specs)
    feats = ''.join(f'<li><b>{esc(k)}</b><span>{esc(v)}</span></li>' for k,v in (p.get('features') or []))
    desc = f'<p class="lede" style="max-width:70ch">{esc(p["desc"])}</p>' if p.get('desc') else ''
    body = f"""    <div class="prop-head">
      <h1 class="display">{esc(street)}<br/><em style="font-size:0.5em">{esc(rest)}</em></h1>
      <div class="price">{price}</div>
    </div>
    <div class="gallery">{g}</div>
    <div class="spec-row">{spec_html}</div>
    {desc}
    {'<ul class="feat-list">'+feats+'</ul>' if feats else ''}
    {cta(up)}
    <div class="back-row"><a class="text-link" href="{up}{'for-sale/' if p['kind']=='sale' else 'for-rent/'}">← All {'listings for sale' if p['kind']=='sale' else 'rentals'}</a></div>"""
    crumb = f'<a href="{up}">Home</a> &nbsp;/&nbsp; <a href="{up}{"for-sale/" if p["kind"]=="sale" else "for-rent/"}">{"For Sale" if p["kind"]=="sale" else "For Rent"}</a> &nbsp;/&nbsp; {esc(street)}'
    write(f'listings/{p["slug"]}/index.html', shell(2, f"{street} — {price.replace('<small>','').replace('</small>','')}", body, crumb))

# ---------------- for-sale / for-rent index ----------------
for kind, slug, title, intro in [
    ('sale','for-sale','Homes for <em>sale.</em>','Every property currently represented by Boutique Realty — exclusively, on and off market.'),
    ('rent','for-rent','Featured <em>rentals.</em>','Current rental listings across Hoboken, Jersey City and the Gold Coast.')]:
    up = '../'
    cards = '\n'.join(prop_card(p, up) for p in sorted((p for p in props if p['kind']==kind), key=lambda x: -(x['price'] or 0)))
    body = f"""    <h1 class="display">{title}</h1>
    <p class="lede" style="margin-top:1.6rem">{intro}</p>
    <div class="listing-grid" style="margin-top:3rem; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr))">
{cards}
    </div>
    {cta(up, "Don't see what you're looking for?")}"""
    crumb = f'<a href="{up}">Home</a> &nbsp;/&nbsp; {"For Sale" if kind=="sale" else "For Rent"}'
    write(f'{slug}/index.html', shell(1, 'For Sale' if kind=='sale' else 'For Rent', body, crumb))

# ---------------- communities ----------------
paras_all = comms['paras']; market_all = comms['listings']
for slug, name in COMM_NAMES.items():
    up = '../../'
    paras = paras_all.get(slug) or COMM_FALLBACK.get(slug) or []
    ptxt = '\n'.join(f'<p class="lede" style="margin-bottom:1.3rem;max-width:66ch">{esc(x)}</p>' for x in paras[:3])
    market = market_all.get(slug) or []
    m = ''
    if market:
        rows = ''.join(f'<div><span>{esc(x["address"])}</span><b>${x["price"]:,}</b></div>' for x in market)
        m = f"""<h2 class="display" style="font-size:clamp(1.6rem,3vw,2.6rem);margin-top:4rem">On the market <em>now.</em></h2>
    <div class="market-list">{rows}</div>"""
    body = f"""    <h1 class="display">{esc(name)}</h1>
    <div style="margin-top:2.4rem">{ptxt}</div>
    {m}
    {cta(up, f"Thinking about {esc(name.split(' /')[0])}?")}
    <div class="back-row"><a class="text-link" href="{up}#communities">← All communities</a></div>"""
    crumb = f'<a href="{up}">Home</a> &nbsp;/&nbsp; <a href="{up}#communities">Communities</a> &nbsp;/&nbsp; {esc(name)}'
    write(f'communities/{slug}/index.html', shell(2, name, body, crumb))

# ---------------- 600 harrison ----------------
up='../../'
body = f"""    <h1 class="display">600 Harrison<br/><em style="font-size:0.55em">Hoboken, NJ</em></h1>
    <div class="gallery">
      <div class="frame g-main"><img src="{up}assets/dev/600-harrison-Building-Exterior.png" alt="600 Harrison exterior"></div>
      <div class="frame"><img src="{up}assets/dev/600-Harrison-Entry.png" alt="Entry" loading="lazy"></div>
      <div class="frame"><img src="{up}assets/dev/600-Harrison-Lobby.png" alt="Lobby" loading="lazy"></div>
      <div class="frame"><img src="{up}assets/dev/600-Harrison-Terrace.png" alt="Terrace" loading="lazy"></div>
    </div>
    <p class="lede" style="margin-top:2.6rem;max-width:70ch">Welcome to 600 Harrison — your new home in the heart of luxury. Boutique Realty proudly
    presents this pet-friendly, new-construction rental building that embodies contemporary living with state-of-the-art
    amenities in the heart of Hoboken: open-concept floor plans, oversized windows with stunning views, hardwood floors
    throughout, and in-unit washer and dryer for your convenience.</p>
    <ul class="feat-list" style="margin-top:2rem">
      <li><b>Kitchens &amp; Baths</b><span>Caesarstone quartz countertops, stainless appliances, glass-enclosed showers, floating vanities</span></li>
      <li><b>Amenities</b><span>Elevator, state-of-the-art gym, package room</span></li>
      <li><b>Outdoor</b><span>Large furnished common patio with lounge seating and an outdoor kitchen with grills</span></li>
      <li><b>Parking</b><span>Indoor parking available</span></li>
      <li><b>Fitness</b><span><img src="{up}assets/dev/600-Harrison-Fitness-Center.png" alt="Fitness center" style="max-width:320px;margin-top:0.4rem"></span></li>
    </ul>
    {cta(up, 'Interested in 600 Harrison?')}
    <div class="back-row"><a class="text-link" href="{up}#development">← Back to developments</a></div>"""
crumb = f'<a href="{up}">Home</a> &nbsp;/&nbsp; Developments &nbsp;/&nbsp; 600 Harrison'
write('developments/600-harrison/index.html', shell(2, '600 Harrison — Hoboken NJ', body, crumb))

# ---------------- commercial ----------------
up='../'
body = f"""    <h1 class="display">Commercial <em>real estate.</em></h1>
    <p class="lede" style="margin-top:2rem;max-width:66ch">Boutique Realty is a full-service team representing clients in
    residential, new development, investment, multi-family and commercial real estate across the entire state of New Jersey.
    Our commercial practice is built on the same principle as everything we do — long-term relationships over transactions.</p>
    <p class="lede" style="margin-top:1.3rem;max-width:66ch">From mixed-use buildings on the Gold Coast to retail and
    investment opportunities across Hudson, Monmouth and Union counties, our brokers bring local insight,
    discretion and seventeen years of market knowledge to every engagement.</p>
    <ul class="feat-list" style="margin-top:2.4rem">
      <li><b>Investment</b><span>Multi-family and mixed-use acquisitions and dispositions</span></li>
      <li><b>Leasing</b><span>Retail and office representation for owners and tenants</span></li>
      <li><b>Development</b><span>New-development marketing and sales, from pre-construction to sell-out</span></li>
    </ul>
    {cta(up, 'Have a commercial requirement?')}"""
crumb = f'<a href="{up}">Home</a> &nbsp;/&nbsp; Commercial'
write('commercial/index.html', shell(1, 'Commercial Real Estate', body, crumb))

# ---------------- careers ----------------
up='../'
ctext = '\n'.join(f'<p class="lede" style="margin-bottom:1.3rem;max-width:66ch">{esc(x)}</p>' for x in careers[:5])
body = f"""    <h1 class="display">Join the <em>team.</em></h1>
    <div style="margin-top:2.4rem">{ctext}</div>
    {cta(up, 'Ready to grow your real estate career?')}"""
crumb = f'<a href="{up}">Home</a> &nbsp;/&nbsp; Careers'
write('careers/index.html', shell(1, 'Careers', body, crumb))

print('Generated:',
      f"{len(agents)} agents,",
      f"{len(props)} listings,",
      f"{len(COMM_NAMES)} communities,",
      "for-sale, for-rent, 600-harrison, commercial, careers")
