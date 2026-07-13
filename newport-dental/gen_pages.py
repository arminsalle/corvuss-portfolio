#!/usr/bin/env python3
"""Generate all subpages (services, doctors, patient info) from scrape/content.json."""
import json, html, pathlib

ROOT = pathlib.Path(__file__).parent
content = json.load(open(ROOT / 'scrape' / 'content.json'))

NAV = '''  <nav class="nav" id="nav">
    <a class="nav-brand" href="index.html">
      <img src="assets/tilmanlogo1.webp" alt="Newport Family & Cosmetic Dentistry" />
    </a>
    <div class="nav-links">
      <a href="index.html#doctors">Meet Us</a>
      <a href="index.html#services">Services</a>
      <a href="technology.html">Technology</a>
      <a href="index.html#locations">Locations</a>
      <a href="tel:(401) 889-2980" class="nav-phone">New Patients: (401) 889-2980</a>
    </div>
    <div class="nav-cta">
      <a class="btn btn-ghost" href="https://flexbook.me/portsmouth" target="_blank" rel="noopener">Book Portsmouth</a>
      <a class="btn btn-solid" href="https://www.flexbook.me/nfcd/1" target="_blank" rel="noopener">Book Newport</a>
    </div>
  </nav>'''

CTA = '''  <section class="band band-green cta" id="book">
    <div class="wrap reveal">
      <h2>Ready to love<br />your smile<span class="accent">?</span></h2>
      <p class="lede">Schedule your appointment today and experience the comfort, care, and quality that make Newport Family &amp; Cosmetic Dentistry a trusted choice for families across Aquidneck Island.</p>
      <div class="cta-actions">
        <a class="btn btn-light" href="https://www.flexbook.me/nfcd/1" target="_blank" rel="noopener">Book Newport</a>
        <a class="btn btn-light" href="https://flexbook.me/portsmouth" target="_blank" rel="noopener">Book Portsmouth</a>
        <a class="btn btn-ghost-light" href="tel:(401) 889-2980">New patients: (401) 889-2980</a>
      </div>
    </div>
  </section>'''

FOOTER = '''  <footer class="footer">
    <div class="wrap footer-grid">
      <div>
        <img class="footer-logo" src="assets/tilmanlogo1.webp" alt="Newport Family & Cosmetic Dentistry" />
        <p>Creating healthy, happy, bright smiles<br />for Newport and beyond.</p>
      </div>
      <div>
        <h4>Patient Information</h4>
        <a href="dental-insurance.html">Dental Insurance</a>
        <a href="financial-policy.html">Financial Policy</a>
        <a href="home-care-instructions.html">Home Care Instructions</a>
        <a href="dental-anxiety-phobia.html">Dental Anxiety &amp; Phobia</a>
        <a href="nitrous-oxide.html">Nitrous Oxide</a>
      </div>
      <div>
        <h4>Visit Us</h4>
        <a href="https://maps.app.goo.gl/3YVaMKnZCPV6vZPp9" target="_blank" rel="noopener">136 Broadway, Newport, RI</a>
        <a href="https://maps.app.goo.gl/2MeEHKQHfLM17BY48" target="_blank" rel="noopener">2765 East Main Rd, Portsmouth, RI</a>
        <a href="tel:(401) 846-3801">Newport: (401) 846-3801</a>
        <a href="tel:(401) 683-9724">Portsmouth: (401) 683-9724</a>
      </div>
    </div>
    <div class="wrap footer-base">
      <span>Copyright © <span class="year">2026</span> Newport Family &amp; Cosmetic Dentistry</span>
      <span>English · Portuguese · Spanish spoken</span>
    </div>
  </footer>'''

def esc(s):
    return html.escape(s, quote=False)

def article_html(blocks, lede_first=True):
    out = []
    first_p = True
    for b in blocks:
        t, x = b['t'], esc(b['x'])
        if t in ('h1', 'h2'):
            out.append(f'      <h2 class="reveal">{x}</h2>')
        elif t in ('h3', 'h4'):
            out.append(f'      <h3 class="reveal">{x}</h3>')
        else:
            cls = 'lede reveal' if (first_p and lede_first) else 'reveal'
            out.append(f'      <p class="{cls}">{x}</p>')
            first_p = False
    return '\n'.join(out)

def film_hero(frames, bg, kicker, l1, l2, l3):
    return f'''  <section class="cinematic cinematic-sub" id="film">
    <div class="sticky">
      <canvas></canvas>
      <div class="shade"></div>
      <div class="overlay">
        <div class="reveal-line" data-in="-0.34" data-out="0.32">
          <p class="kicker">{kicker}</p>
          <h1>{l1}</h1>
        </div>
        <div class="reveal-line" data-in="0.38" data-out="0.66">
          <h1>{l2}</h1>
        </div>
        <div class="reveal-line" data-in="0.72" data-out="1.30">
          <h1>{l3}</h1>
        </div>
      </div>
      <div class="scroll-hint"><span>Scroll</span><i></i></div>
    </div>
  </section>'''

def page(title, desc, body, scrub=None):
    scrub_js = ''
    if scrub:
        scrub_js = f'''    window.SCRUB_SECTIONS = [
      {{ section: "#film", frameCount: 180, bg: "{scrub[1]}", framePath: (i) => `frames/{scrub[0]}/frame_${{String(i).padStart(4, "0")}}.jpg` }}
    ];'''
    else:
        scrub_js = '    window.SCRUB_SECTIONS = [];'
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(title)} | Newport Family &amp; Cosmetic Dentistry</title>
  <meta name="description" content="{html.escape(desc)}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,400&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="styles.css" />
</head>
<body>

{NAV}

{body}

{CTA}

{FOOTER}

  <script src="lenis.min.js"></script>
  <script>
{scrub_js}
    document.querySelectorAll(".year").forEach(e => e.textContent = new Date().getFullYear());
  </script>
  <script src="scroll-cinematic.js"></script>
</body>
</html>
'''

# ---------------- SERVICE PAGES (film hero + original copy) ----------------
services = {
  'botox': dict(frames='svc-botox', bg='#0a0d0b', kicker='Botox',
    l1='Smooth the<br />lines<span class="accent">.</span>',
    l2='Relieve TMJ<br />&amp; migraines<span class="accent">.</span>',
    l3='Artistry meets<br /><em>medicine</em>'),
  'cosmetic-dentistry': dict(frames='svc-cosmetic', bg='#0a0d0b', kicker='Cosmetic Dentistry',
    l1='Your smile,<br />by <em>design</em>',
    l2='Veneers. Whitening.<br />Smile makeovers<span class="accent">.</span>',
    l3='Confidence,<br /><em>crafted</em>'),
  'dental-implants': dict(frames='svc-implants', bg='#0a0d0b', kicker='Dental Implants',
    l1='Titanium<br />precision<span class="accent">.</span>',
    l2='Engineered to last<br /><em>decades</em>',
    l3='A complete<br />smile again<span class="accent">.</span>'),
  'dentures-and-partials': dict(frames='svc-dentures', bg='#0a0d0b', kicker='Dentures &amp; Partials',
    l1='Comfort,<br />custom-made<span class="accent">.</span>',
    l2='So natural, nobody<br /><em>suspects</em>',
    l3='Eat. Speak.<br />Smile<span class="accent">.</span>'),
  'emergency-visits': dict(frames='svc-emergency', bg='#0d0a08', kicker='Emergency Visits',
    l1='Dental pain<br />can’t <em>wait</em>',
    l2='We make room<br />in the schedule<span class="accent">.</span>',
    l3='Relief,<br /><em>restored</em>'),
  'orthodontics': dict(frames='svc-ortho', bg='#0a0d0b', kicker='Orthodontics',
    l1='Invisible.<br />Removable<span class="accent">.</span>',
    l2='Straight teeth,<br /><em>your way</em>',
    l3='No metal<br />required<span class="accent">.</span>'),
  'periodontal-treatment-gum-care': dict(frames='svc-perio', bg='#0a0d0b', kicker='Periodontal Treatment',
    l1='Healthy gums<br /><em>first</em>',
    l2='Guided Biofilm<br />Therapy<span class="accent">.</span>',
    l3='Clean, without<br />the <em>scraping</em>'),
  'sleep-apnea-treatment': dict(frames='svc-sleep', bg='#070a0d', kicker='Sleep Apnea Treatment',
    l1='Breathe<br />easier<span class="accent">.</span>',
    l2='Sleep<br /><em>deeper</em>',
    l3='No CPAP<br />required<span class="accent">.</span>'),
  'technology': dict(frames='tech', bg='#05080a', kicker='Advanced Technology',
    l1='Scanned in 3D<span class="accent">.</span>',
    l2='Designed<br />digitally<span class="accent">.</span>',
    l3='Delivered<br /><em>same-day</em>'),
}

for slug, cfg in services.items():
    c = content[slug]
    body = film_hero(cfg['frames'], cfg['bg'], cfg['kicker'], cfg['l1'], cfg['l2'], cfg['l3'])
    body += f'''

  <section class="band band-cream">
    <div class="wrap article">
{article_html(c['blocks'])}
    </div>
  </section>'''
    (ROOT / f'{slug}.html').write_text(page(c['title'], c['desc'], body, scrub=(cfg['frames'], cfg['bg'])))
    print('service:', slug)

# ---------------- PATIENT INFO PAGES (no film) ----------------
for slug in ['dental-insurance', 'financial-policy', 'home-care-instructions', 'dental-anxiety-phobia', 'nitrous-oxide']:
    c = content[slug]
    body = f'''  <header class="page-hero">
    <div class="wrap">
      <p class="eyebrow">Patient Information</p>
      <h1>{esc(c['title'])}<span class="accent">.</span></h1>
    </div>
  </header>

  <section class="band band-cream">
    <div class="wrap article">
{article_html(c['blocks'])}
    </div>
  </section>'''
    (ROOT / f'{slug}.html').write_text(page(c['title'], c['desc'], body))
    print('info:', slug)

# ---------------- DOCTOR PAGES ----------------
doctors = {
  'dr-nathan-w-tilman': dict(name='Dr. Nathan W. Tilman, DDS', tag='Founder · US Navy Dental Corps veteran',
    photo='assets/dr-tilman.jpg', mono=None, bio=[
    "Originally from Salisbury, MD, Dr. Tilman attended Wake Forest University for his undergraduate degree (GO DEACS!!!). He was awarded his Doctor of Dental Surgery from the University of Maryland, where he graduated Summa Cum Laude in 2001. Dr. Tilman served in the US Navy Dental Corps for four years, including two years forward deployed aboard USS ASHLAND (LSD 48).",
    "Following his military service, Dr. Tilman moved to Newport, RI, in 2007 and opened Newport Family and Cosmetic Dentistry. He has had the pleasure of working with an amazing team and amazing patients in creating a state-of-the-art, caring, and comfortable dental practice. His commitment to incorporating advanced technologies and techniques enables Dr. Tilman and his team provide dental treatment in fewer visits and with greater comfort than with traditional techniques."]),
  'dr-dianne-pannes': dict(name='Dr. Dianne Pannes, DDS', tag='US Army Dental Corps, 25 years · Bronze Star',
    photo=None, mono='DP', bio=[
    "Born in Massachusetts and raised in Upstate New York, Dr. Pannes was a Distinguished Military Graduate from Cornell University and earned her Doctor of Dental Surgery from the State University of New York at Buffalo. She served in the United States Army Dental Corps for twenty-five years, during which time she deployed to Iraq for one year in support of Operation Iraqi Freedom, along with numerous other worldwide military and humanitarian missions. Dr. Pannes served as an Army Dental Residency Program Director and Professor with the Uniformed Services University of Health Sciences. She represented the Army for many years as a leader in the American Dental Association and the Academy of General Dentistry. She was awarded the Surgeon General’s A Designator for Clinical Excellence, Mastership in the Academy of General Dentistry, board certification with the American Board of General Dentistry, as well as the Bronze Star and Legion of Merit.",
    "As a student at the Naval War College in 2013, Dr. Pannes and her husband fell in love with Newport (of course \U0001F60A) and have now returned following Dr. Pannes’ retirement from military service. She is excited and honored to be joining such an amazing team taking care of such amazing patients in such an amazing place!"]),
  'dr-aaron-ramos': dict(name='Dr. Aaron Ramos, DMD', tag='General & family dentistry',
    photo='assets/dr-ramos.jpg', mono=None, bio=[
    "Dr. Aaron Ramos joined our practice in 2025 after graduating from the University of New England’s College of Dental Medicine. Returning to his home area, Dr. Ramos is committed to providing high-quality, patient-centered care with a focus on comfort and long-term oral health.",
    "He enjoys all aspects of general dentistry and values building lasting relationships with his patients. Dr. Ramos prioritizes listening to his patients’ concerns and creating individualized treatment plans that help his patients feel confident in their smiles.",
    "Outside of the office, Dr. Ramos enjoys bike rides around town, golfing and spending time on Newport Harbor."]),
  'dr-bryan-may': dict(name='Dr. Bryan May, DDS', tag='General & cosmetic dentistry',
    photo=None, mono='BM', bio=[
    "Dr. Bryan May provides comprehensive family and cosmetic dentistry for patients across Newport and Portsmouth — from routine preventive care to full smile makeovers.",
    "He is part of the team trusted by families across Aquidneck Island at Newport Family & Cosmetic Dentistry."]),
  'dr-james-safford': dict(name='Dr. James Safford, DDS', tag='General & cosmetic dentistry',
    photo=None, mono='JS', bio=[
    "Dr. James Safford practices skilled, attentive dentistry with a focus on patient comfort — from routine care to restorative and cosmetic treatment.",
    "He is part of the team trusted by families across Aquidneck Island at Newport Family & Cosmetic Dentistry."]),
}

for slug, d in doctors.items():
    photo_html = (f'<div class="doctor-photo doctor-photo-lg"><img src="{d["photo"]}" alt="{esc(d["name"])}" /></div>'
                  if d['photo'] else
                  f'<div class="doctor-photo doctor-photo-lg doctor-mono"><span>{d["mono"]}</span></div>')
    bio_html = '\n'.join(f'      <p class="lede reveal">{esc(p)}</p>' for p in d['bio'])
    body = f'''  <header class="page-hero page-hero-doctor">
    <div class="wrap doctor-hero">
      {photo_html}
      <div>
        <p class="eyebrow">Meet Us</p>
        <h1>{esc(d['name'])}</h1>
        <p class="doctor-tag">{esc(d['tag'])}</p>
      </div>
    </div>
  </header>

  <section class="band band-cream">
    <div class="wrap article">
{bio_html}
      <p class="reveal"><a class="btn btn-solid" href="index.html#doctors">← Back to all doctors</a></p>
    </div>
  </section>'''
    (ROOT / f'{slug}.html').write_text(page(d['name'], f"{d['name']} — {d['tag']} at Newport Family & Cosmetic Dentistry, Newport & Portsmouth RI.", body))
    print('doctor:', slug)

print('DONE')
