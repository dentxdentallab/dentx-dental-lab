"""DentX static site generator. One data source -> all pages, JSON-LD, llms.txt, sitemap.

    python3 build.py          # writes pages into this folder (repo root = Vercel output)
"""
import json, os, html

SITE = os.environ.get("SITE_URL", "https://www.dentxdentallab.com")  # ponytail: placeholder until the real domain is connected
PHONE, PHONE_TEL = "(818) 687-0085", "+18186870085"
EMAIL = "Dentxdentallab@yahoo.com"
ADDR = "18401 Burbank Blvd #110, Tarzana, CA 91356"
MAPS = "https://www.google.com/maps/search/?api=1&query=18401+Burbank+Blvd+%23110+Tarzana+CA+91356"
TODAY = "2026-10-01"

# ---------------------------------------------------------------- data
# (name, note, days, price, page)
CATALOG = [
    ("ceramic", "Metal-free / full ceramic", [
        ("Zirconia crown", "", "5", "$75", "/zirconia-crowns/"),
        ("E.max crown", "", "5", "$85", "/emax-crowns-veneers/"),
        ("Veneers", "", "5", "$99", "/emax-crowns-veneers/"),
        ("Layered zirconia / E.max", "", "6", "$99", "/zirconia-crowns/"),
        ("Inlay / onlay", "", "5", "$75", "/emax-crowns-veneers/"),
        ("PMMA temporary crown", "", "5", "$45", "/zirconia-crowns/"),
        ("Diagnostic wax-up", "", "4", "$25", "/emax-crowns-veneers/"),
    ]),
    ("implant", "Implant & attachments", [
        ("Implant crown, screw retained", "", "5", "$130", "/implant-crowns/"),
        ("Implant crown, cement retained", "", "5", "$120", "/implant-crowns/"),
        ("Custom abutment, milled", "", "", "$230", "/implant-crowns/"),
        ("Surgical guide", "", "", "$95", "/implant-crowns/"),
        ("Verification jig", "", "", "$60", "/implant-crowns/"),
        ("Soft tissue", "", "", "$15", "/implant-crowns/"),
    ]),
    ("removable", "Removable", [
        ("Acrylic denture", "Bite block · teeth try-in · final finish", "6 · 7 · 7", "$180", "/dentures-partials/"),
        ("Printed denture", "", "7", "$160", "/dentures-partials/"),
        ("Metal partial", "Metal try-in · teeth try-in · final finish", "11 · 7 · 7", "$230", "/dentures-partials/"),
        ("Valplast", "Bite block · teeth try-in · final finish", "6 · 7 · 12", "$230", "/dentures-partials/"),
        ("Combination", "Metal + Valplast", "12", "$250", "/dentures-partials/"),
        ("Stayplate, acrylic", "Per arch, up to 3 units · 4+ units $110", "4", "$95", "/dentures-partials/"),
        ("Printed flexible stayplate", "Per arch", "4", "$85", "/dentures-partials/"),
        ("Stayplate rush", "Rush fee", "2", "+$50", "/dentures-partials/"),
        ("Night guard", "Hard or soft", "3", "$85", "/dentures-partials/"),
        ("Repair / reline", "Soft reline $80 · excluding delivery time", "2", "$60", "/dentures-partials/"),
    ]),
]
OWNER = "Haibert Aivazian"
SCANNERS = ["Medit", "iTero", "Shining 3D", "DEXIS IOS Cloud", "STL by email"]

SHIP = [
    ("Digital cases", "Free FedEx 2Day return shipping. No minimum."),
    ("Impressions & models", "Free 2-day shipping both ways on cases $150+. Under $150: prepaid label, $15 each way."),
    ("Los Angeles area", "Free pickup from your office and dropoff of finished work."),
]

FAQ_HOME = [
    ("Do you work with dental offices outside California?", "Yes. DentX ships to dental offices across the United States. Digital cases ship back free by FedEx 2Day with no minimum. For impressions and models, shipping is free both ways on cases of $150 or more, and a $15 prepaid label each way below that."),
    ("How fast are zirconia and E.max crowns?", "Zirconia crowns, E.max crowns and veneers take 5 business days in the lab, counted from when your scan or case arrives. With free FedEx 2Day return, a digital crown case is in your office in about 7 business days."),
    ("Which intraoral scanners can send cases to DentX?", "Medit, iTero, Shining 3D and DEXIS IOS Cloud, or email STL files. Call the lab and we will walk you through connecting your scanner account."),
    ("Is shade matching included?", "Yes. DentX does complimentary shade matching for every client. Send a shade tab reading or a photo with the case."),
    ("How long do dentures and partials take?", "Acrylic dentures: 6 business days for the bite block, 7 for teeth try-in and 7 for the final finish. Printed dentures take 7 business days, combination metal + Valplast 12."),
    ("Is there a rush option?", "Stayplates can be done in 2 business days with a $50 rush fee. For other rush requests, call the lab."),
    ("Where is DentX Dental Lab?", f"{ADDR}, in the San Fernando Valley. Phone {PHONE}, email {EMAIL}."),
]

PAGES = {
    "/zirconia-crowns/": dict(
        title="Zirconia Crowns Dental Lab | $75, 5 Business Days | DentX",
        desc="Zirconia crowns from $75 in 5 business days. Layered zirconia $99. Digital cases ship back free by FedEx 2Day to dental offices nationwide. DentX Dental Lab, Tarzana CA.",
        h1="Zirconia crowns.<br><em>Five days in the lab.</em>",
        lead="Monolithic zirconia from $75 and layered zirconia from $99, designed from your scan and shade-matched at no charge. Shipped back free by FedEx 2Day.",
        cats=["ceramic"], img="bench-ceramic.webp", img_alt="Ceramist layering porcelain on a zirconia crown beside the furnace",
        body=[
            ("Monolithic or layered", "Monolithic zirconia for strength on posterior teeth and bruxers. Layered zirconia when the anterior needs more life in the incisal third. Tell us the shade and we match it, free."),
            ("From scan to your door", "Send from Medit, iTero, Shining 3D, DEXIS IOS Cloud or by STL. The 5 in-lab days start when your scan lands. FedEx 2Day return is free, so most offices have the crown in about 7 business days."),
            ("Temporaries and wax-ups", "PMMA temporary crowns are $45 in 5 business days. Diagnostic wax-ups are $25 in 4 business days."),
        ],
        faq=[("How much does a zirconia crown cost?", "A zirconia crown is $75. Layered zirconia is $99."),
             ("How long does a zirconia crown take?", "5 business days in the lab for monolithic zirconia, 6 for layered, counted from when the case arrives.")]),
    "/emax-crowns-veneers/": dict(
        title="E.max Crowns & Veneers Lab | From $85, 5 Days | DentX",
        desc="E.max crowns $85, veneers $99, inlays and onlays $75, all in 5 business days with complimentary shade matching. DentX Dental Lab ships nationwide.",
        h1="E.max crowns <em>&amp;</em> veneers.",
        lead="Lithium disilicate crowns, veneers, inlays and onlays, shade-matched for every client and finished in 5 business days.",
        cats=["ceramic"], img="hero.webp", img_alt="Glazed three-unit ceramic bridge",
        body=[
            ("Anterior esthetics", "E.max crowns at $85 and veneers at $99 for cases where translucency matters. Layered E.max at $99 in 6 business days."),
            ("Conservative restorations", "Inlays and onlays at $75 in 5 business days. Diagnostic wax-ups at $25 to plan the case with your patient."),
            ("Shade on us", "Send the shade tab reading or a photo under daylight. Matching is complimentary for every office."),
        ],
        faq=[("How much is an E.max crown?", "An E.max crown is $85. Veneers are $99."),
             ("How long do veneers take?", "Veneers take 5 business days in the lab.")]),
    "/implant-crowns/": dict(
        title="Implant Crowns & Custom Abutments Lab | DentX Dental Lab",
        desc="Screw-retained implant crowns $130, cement-retained $120, custom milled abutments $230, surgical guides $95. 5 business days. DentX Dental Lab ships nationwide.",
        h1="Implant crowns,<br><em>abutments &amp; guides.</em>",
        lead="Screw-retained and cement-retained implant crowns in 5 business days, with custom milled abutments, surgical guides and verification jigs.",
        cats=["implant"], img="bench-implant.webp", img_alt="Zirconia implant crown on a custom milled titanium abutment",
        body=[
            ("Screw or cement retained", "Screw-retained implant crowns at $130 and cement-retained at $120, both in 5 business days."),
            ("Custom milled abutments", "Custom milled abutments at $230 for emergence profiles a stock part can't give you. Soft tissue on the model at $15."),
            ("Planning", "Surgical guides at $95 and verification jigs at $60. Call the lab to talk through the case before you place."),
        ],
        faq=[("How much is an implant crown?", "Screw-retained implant crowns are $130 and cement-retained are $120."),
             ("Do you make custom abutments?", "Yes. Custom milled abutments are $230.")]),
    "/dentures-partials/": dict(
        title="Dentures, Partials & Valplast Lab | From $160 | DentX",
        desc="Acrylic dentures $180, printed dentures $160, metal partials and Valplast $230, combination $250, night guards $85, stayplates from $85 per arch. DentX Dental Lab.",
        h1="Dentures, partials <em>&amp;</em> night guards.",
        lead="Acrylic and printed dentures, metal and Valplast partials, stayplates, night guards, relines and repairs, with stage-by-stage turnaround you can schedule patients around.",
        cats=["removable"], img="bench-removable.webp", img_alt="Complete dentures mounted on an articulator at the bench",
        body=[
            ("Dentures", "Acrylic dentures at $180: bite block 6 business days, teeth try-in 7, final finish 7. Printed dentures at $160 in 7 business days."),
            ("Partials", "Metal partials at $230 and Valplast at $230. Combination metal + Valplast at $250 in 12 business days."),
            ("Same-week work", "Night guards (hard or soft) $85 in 3 business days. Repairs and relines $60 in 2 business days. Stayplates in 4 business days, or 2 with a $50 rush fee."),
        ],
        faq=[("How much is a denture?", "An acrylic denture is $180 and a printed denture is $160."),
             ("How long does a Valplast partial take?", "Bite block 6 business days, teeth try-in 7, final Valplast finish 12.")]),
    "/nationwide-dental-lab/": dict(
        title="Nationwide Dental Lab with Free Return Shipping | DentX",
        desc="Send cases to DentX Dental Lab from anywhere in the U.S. Free FedEx 2Day return on digital cases, no minimum. Free 2-day shipping both ways on impression cases $150+.",
        h1="A Los Angeles lab<br><em>for offices anywhere in the U.S.</em>",
        lead="Scan today, crown in your office in about 7 business days. Digital cases ship back free by FedEx 2Day with no minimum.",
        cats=[], img="bench-ceramic.webp", img_alt="Ceramist finishing a crown at the DentX bench",
        body=[
            ("Digital cases", "Send from Medit, iTero, Shining 3D, DEXIS IOS Cloud or by STL. No box to pack. The in-lab clock starts the moment your scan lands, and the finished work ships back free by FedEx 2Day."),
            ("Impressions & models", "Cases of $150 or more ship free both ways by 2-day service. Under $150, we send a prepaid label at $15 each way."),
            ("Los Angeles area", "Offices in Los Angeles and the San Fernando Valley get free pickup and dropoff. Call to schedule."),
            ("Why offices switch", "One flat price list, published. Turnaround in business days you can book patients around. Complimentary shade matching. A lab owner who answers the phone."),
        ],
        faq=[("Do you ship to other states?", "Yes. DentX ships to dental offices across the United States."),
             ("Who pays for shipping?", "Digital cases ship back free by FedEx 2Day with no minimum. Impression cases of $150+ ship free both ways; below $150 it's a $15 prepaid label each way.")]),
    "/about/": dict(
        title="About Haibert Aivazian, Owner of DentX Dental Lab | Tarzana, CA",
        desc="Meet Haibert Aivazian, licensed owner of DentX Dental Lab, in business since 2008. He does the shade matching himself. Published prices, 5-day crowns, shipping nationwide.",
        h1="Meet Haibert Aivazian.<br><em>Owner of DentX.</em>",
        lead="Licensed, in business since 2008, and still at the bench. When you send a case to DentX, you know whose hands it's in.",
        cats=[], img="owner-haibert-shade.webp", img_alt="Haibert Aivazian, owner of DentX Dental Lab, checking a crown against a shade guide at his bench",
        body=[
            ("Since 2008", "Haibert has been in business since 2008. In that time dentistry moved from impressions to intraoral scans, and DentX takes both."),
            ("Shade, in person", "Haibert does the shade matching himself, free for every client. Send a photo under daylight, or bring your patient to the Tarzana lab and he'll match it with you there."),
            ("Why offices switch", "Big labs run on volume, so your case becomes a ticket number. DentX publishes its prices, quotes turnaround in business days, ships digital cases back free, and puts you on the phone with the owner."),
            ("Licensed and accountable", "DentX Dental Lab Inc is a licensed lab, owned and run by Haibert. If something about a case needs a second look, you call him and talk it through."),
        ],
        faq=[("Who owns DentX Dental Lab?", "Haibert Aivazian. He has been in business since 2008."),
             ("Can a patient come in for a shade match?", "Yes. Call (818) 687-0085 to set a time at the Tarzana lab.")]),
    "/send-a-case/": dict(
        title="Send a Case to DentX Dental Lab | Scan, Ship or Pickup",
        desc="Send your first case to DentX Dental Lab: connect Medit, iTero, Shining 3D or DEXIS, email an STL, or request a pickup or shipping label. Call (818) 687-0085.",
        h1="Send your <em>first case.</em>",
        lead="Tell us how you work and we'll set you up the same day: scanner connection, shipping label or local pickup.",
        cats=[], img=None, img_alt="",
        body=[
            ("Scanning digitally?", "We receive from Medit, iTero, Shining 3D and DEXIS IOS Cloud, or STL by email. Call the lab and we'll walk you through connecting your scanner account to DentX."),
            ("Sending impressions?", "Request a shipping label below. Cases of $150+ ship free both ways."),
            ("In Los Angeles?", "Request a pickup and we'll collect from your office."),
        ],
        faq=[]),
}

# ---------------------------------------------------------------- helpers
def _min(css):
    import re as _re
    css = _re.sub(r"/\*.*?\*/", "", css, flags=_re.S)
    css = _re.sub(r"\s+", " ", css)
    return _re.sub(r"\s*([{}:;,>])\s*", r"\1", css).replace(";}", "}").strip()
CSS = _min("".join(open(f"assets/{n}").read() for n in ("scrollcraft.css", "site.css", "dentx.css"))).replace("url(fonts/", "url(/assets/fonts/")

def img(name, alt, sizes="(max-width:680px) 92vw, 50vw", extra="", w=1400, h=933):
    return (f'<img src="/assets/{name}.webp" srcset="/assets/{name}-480.webp 480w, /assets/{name}-800.webp 800w, /assets/{name}.webp 1400w" '
            f'sizes="{sizes}" alt="{alt}" width="{w}" height="{h}" {extra}>')
e = html.escape
def svg_logo(cls=""):
    return f'<img class="{cls}" src="/assets/logo-white.svg" width="1000" height="680" alt="DentX Dental Lab">'

def ledger(keys=None):
    out = []
    for key, label, rows in CATALOG:
        if keys is not None and key not in keys: continue
        has_days = any(r[2] for r in rows)
        head = "<thead><tr><th>Service</th>" + ("<th>Days</th>" if has_days else "") + "<th>Price</th></tr></thead>"
        body = "".join(
            f'<tr><td><a href="{r[4]}">{e(r[0])}</a>{f"<small>{e(r[1])}</small>" if r[1] else ""}</td>'
            + (f'<td class="d">{r[2] or "—"}</td>' if has_days else "") + f'<td class="p">{r[3]}</td></tr>'
            for r in rows)
        out.append(f'<table><caption>{e(label)}</caption>{head}<tbody>{body}</tbody></table>')
    return "\n".join(out)

def faq_html(items):
    return "\n".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in items)

def lab_ld():
    offers = []
    for _, _, rows in CATALOG:
        for name, note, days, price, page in rows:
            if not price.startswith("$"): continue
            item = {"@type": "Service", "name": name, "url": SITE + page}
            if days: item["description"] = f"Turnaround {days} business days. {note}".strip()
            offers.append({"@type": "Offer", "itemOffered": item, "price": price.strip("$"), "priceCurrency": "USD"})
    return {
        "@context": "https://schema.org", "@type": "LocalBusiness", "@id": SITE + "/#lab",
        "additionalType": "https://en.wikipedia.org/wiki/Dental_laboratory",
        "name": "DentX Dental Lab", "legalName": "DentX Dental Lab Inc", "url": SITE + "/",
        "logo": SITE + "/assets/logo.svg", "image": SITE + "/assets/og.jpg",
        "description": "Digital dental laboratory in Tarzana, California, serving dental offices nationwide. Zirconia and E.max crowns, veneers, implant crowns, dentures, partials and night guards. Free return shipping on digital cases, complimentary shade matching.",
        "telephone": "+1-818-687-0085", "email": EMAIL, "priceRange": "$15–$250", "foundingDate": "2008",
        "founder": {"@type": "Person", "name": OWNER, "jobTitle": "Owner", "image": SITE + "/assets/owner-haibert.webp", "url": SITE + "/about/"},
        "address": {"@type": "PostalAddress", "streetAddress": "18401 Burbank Blvd #110", "addressLocality": "Tarzana",
                    "addressRegion": "CA", "postalCode": "91356", "addressCountry": "US"},
        "areaServed": [{"@type": "Country", "name": "United States"}, {"@type": "Place", "name": "San Fernando Valley, CA"}],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Dental lab services and prices", "itemListElement": offers},
    }

def faq_ld(items):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}

def crumbs_ld(path, name):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "DentX Dental Lab", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": name, "item": SITE + path}]}

NAV = [("/zirconia-crowns/", "Crowns"), ("/implant-crowns/", "Implants"), ("/dentures-partials/", "Dentures"),
       ("/nationwide-dental-lab/", "Shipping"), ("/#prices", "Prices"), ("/about/", "About")]

def head(title, desc, path, ld, preload=None):
    pre = (f'<link rel="preload" as="image" href="/assets/{preload}" imagesrcset="/assets/{preload[:-5]}-480.webp 480w, /assets/{preload[:-5]}-800.webp 800w, /assets/{preload} 1400w" imagesizes="(max-width:980px) 92vw, 58vw" fetchpriority="high">' if preload else "")
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE}{path}">
<meta property="og:type" content="website"><meta property="og:site_name" content="DentX Dental Lab">
<meta property="og:title" content="{title}"><meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE}{path}"><meta property="og:image" content="{SITE}/assets/og.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#071a3d">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/InstrumentSerif-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/Geist-normal.woff2" as="font" type="font/woff2" crossorigin>
{pre}
<style>{CSS}</style>
<script defer src="/assets/scrollcraft.js"></script>
<script defer src="/assets/site.js"></script>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>"""

def header():
    nav = "".join(f'<a href="{h}">{t}</a>' for h, t in NAV)
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <a href="/" class="brand" aria-label="DentX Dental Lab home"><img src="/assets/logo-white.svg" width="1000" height="680" alt="DentX Dental Lab"></a>
  <nav class="main-nav" aria-label="Main">{nav}</nav>
  <div class="header-actions">
    <a class="header-phone" href="tel:{PHONE_TEL}" data-ev="call">{PHONE}</a>
    <a class="btn btn-gold" href="/send-a-case/">Send a case</a>
  </div>
</header>"""

def lead_form(title="Start your first case", sub="We reply the same business day. Prefer to talk? Call or text the lab."):
    return f"""<section class="lead" id="start">
  <div class="lead-copy">
    <p class="eyebrow">NEW OFFICES</p>
    <h2>{title}</h2>
    <p>{sub}</p>
    <div class="lead-direct">
      <a class="btn btn-gold" href="tel:{PHONE_TEL}" data-ev="call">Call {PHONE}</a>
      <a class="btn btn-ghost" href="sms:{PHONE_TEL}" data-ev="text">Text the lab</a>
    </div>
  </div>
  <form class="lead-form" action="/api/lead" method="post" novalidate>
    <label>Practice name<input name="practice" autocomplete="organization" required></label>
    <label>Your name<input name="name" autocomplete="name" required></label>
    <div class="row">
      <label>Phone<input name="phone" type="tel" autocomplete="tel" required></label>
      <label>Email<input name="email" type="email" autocomplete="email"></label>
    </div>
    <div class="row">
      <label>City, state<input name="location" autocomplete="address-level2"></label>
      <label>I'd like to
        <select name="need">
          <option>Send a digital case</option><option>Get a shipping label</option>
          <option>Schedule a local pickup</option><option>Get pricing / talk to the lab</option>
        </select>
      </label>
    </div>
    <label>Notes <span>(no patient names)</span><textarea name="message" rows="3"></textarea></label>
    <label class="hp" aria-hidden="true">Leave empty<input name="company_site" tabindex="-1" autocomplete="off"></label>
    <button class="btn btn-gold" type="submit">Send request</button>
    <p class="form-status" role="status" aria-live="polite"></p>
  </form>
</section>"""

def footer():
    links = "".join(f'<a href="{p}">{e(d["h1"].replace("<br>", " ").replace("<em>", "").replace("</em>", "").replace("&amp;", "&"))}</a>' for p, d in PAGES.items())
    return f"""<section class="close" id="contact">
  <div class="contact-top">
    <div class="contact-mark">{svg_logo()}</div>
    <h2>Contact us <em>today.</em></h2>
    <p class="contact-who"><img src="/assets/owner-haibert-480.webp" alt="" width="480" height="600" loading="lazy">You'll talk to Haibert directly.</p>
  </div>
  <div class="contact-row">
    <div class="contact-details">
      <a href="tel:{PHONE_TEL}" class="phone" data-ev="call">+1 {PHONE}</a>
      <a href="sms:{PHONE_TEL}" data-ev="text">Text the lab</a>
      <a href="mailto:{EMAIL}" data-ev="email">{EMAIL}</a>
      <a href="{MAPS}" target="_blank" rel="noopener">{ADDR}</a>
    </div>
    <a class="btn btn-gold" href="/send-a-case/">Send a case</a>
  </div>
  <footer class="footer">
    <span>DentX Dental Lab Inc · Tarzana, CA · Shipping nationwide</span>
    <nav aria-label="Footer">{links}</nav>
  </footer>
</section>
<div class="mobile-bar">
  <a href="tel:{PHONE_TEL}" data-ev="call">Call</a>
  <a href="sms:{PHONE_TEL}" data-ev="text">Text</a>
  <a class="gold" href="/send-a-case/">Send a case</a>
</div>
</body>
</html>"""

# ---------------------------------------------------------------- home
def home():
    scanners = "".join(f"<li>{s}</li>" for s in SCANNERS)
    ship = "".join(f"<div><h3>{a}</h3><p>{b}</p></div>" for a, b in SHIP)
    benches = [("removable", "Removable", "bench-removable.webp", "Complete dentures mounted on an articulator at the bench",
                "Dentures · Partials · Valplast · Night guards", "/dentures-partials/"),
               ("ceramic", "Metal-free / full ceramic", "bench-ceramic.webp", "Ceramist layering porcelain on a crown beside the furnace",
                "Zirconia · E.max · Veneers · Inlays & onlays", "/zirconia-crowns/"),
               ("implant", "Implant & attachments", "bench-implant.webp", "Zirconia implant crown on a custom milled abutment",
                "Screw & cement retained · Custom abutments · Guides", "/implant-crowns/")]
    bench_html = "".join(f"""<a class="bench" href="{u}"><div class="bench-image">{img(im[:-5], alt, "(max-width:680px) 82vw, 40vw", 'loading="lazy"')}</div>
<div class="bench-label"><h3>{t}</h3><span aria-hidden="true">→</span></div><p>{p}</p></a>""" for k, t, im, alt, p, u in benches)
    steps = [("Day 0", "Your scan lands", "The in-lab clock starts the moment it arrives."),
             ("Day 1", "Design", "Your crown is designed from the scan."),
             ("Days 2–3", "Mill & sinter", "Milled and fired in-house."),
             ("Day 4", "Stain, glaze, shade", "Matched to your shade, free."),
             ("Day 5", "Ships FedEx 2Day", "Return shipping on us."),
             ("Day 7", "In your office", "Ready to seat.")]
    step_html = "".join(f'<li><span class="day">{d}</span><h3>{t}</h3><p>{p}</p></li>' for d, t, p in steps)
    ld = [lab_ld(), faq_ld(FAQ_HOME)]
    return head("DentX Dental Lab | Zirconia, E.max, Implants &amp; Dentures · Ships Nationwide",
                "Premium dental lab in Tarzana, CA shipping nationwide. Zirconia crowns $75 and E.max $85 in 5 business days, free FedEx 2Day return on digital cases, complimentary shade matching.",
                "/", ld, preload="hero.webp") + f"""
<body class="home">
{header()}
<main id="main">
  <section class="hero" data-sc-act="flow">
    <div class="hero-backdrop"></div>
    <div class="hero-title">
      <p class="eyebrow">PREMIUM DENTAL LAB · TARZANA, CA · SHIPPING NATIONWIDE</p>
      <h1>{svg_logo()}<span class="sr-only">DentX Dental Lab: zirconia, E.max, implant and denture lab shipping nationwide</span></h1>
    </div>
    <div class="hero-product">
      <div class="tray"></div>
      {img("hero", "Glazed three-unit ceramic bridge", "(max-width:980px) 92vw, 58vw", 'fetchpriority="high"')}
      <div class="tray-lip"></div>
    </div>
    <div class="hero-copy">
      <h2>Digital cases in.<br><em>Restorations out.</em></h2>
      <p>Zirconia &amp; E.max crowns in 5 business days. Shipped back free to offices anywhere in the U.S.</p>
      <div class="actions">
        <a class="btn btn-gold" href="/send-a-case/">Send a case</a>
        <a class="btn btn-ghost" href="tel:{PHONE_TEL}" data-ev="call">Call the lab</a>
      </div>
    </div>
    <div class="hero-bottom">
      <span>Free FedEx 2Day return on digital cases</span>
      <span>Shade matching on us</span>
      <span>Published prices</span>
    </div>
  </section>

  <section class="clock" aria-labelledby="clock-h">
    <div class="clock-head">
      <p class="eyebrow">HOW A CROWN MOVES</p>
      <h2 id="clock-h">Scan today.<br><em>In your office in 7.</em></h2>
      <p>5 business days in the lab, starting the moment your scan lands. Free FedEx 2Day back to you.</p>
    </div>
    <ol class="clock-track">{step_html}</ol>
  </section>

  <section class="scanners">
    <div>
      <p class="eyebrow">WORKS WITH YOUR SCANNER</p>
      <h2>Send it the way <em>you already scan.</em></h2>
    </div>
    <div>
      <ul class="chips">{scanners}</ul>
      <p>New to DentX? Call and we'll walk you through connecting your account. Takes a few minutes.</p>
    </div>
  </section>

  <section class="catalog light" data-sc-act="pan" data-sc-span="2" id="services">
    <div data-sc-stage class="catalog-stage">
      <div class="section-heading">
        <h2>Three benches.<br><em>One lab.</em></h2>
        <a href="#prices" class="inline-link">Turnaround &amp; prices ↓</a>
      </div>
      <div class="bench-rail" data-sc-pan="0.03">{bench_html}</div>
    </div>
  </section>

  <section class="ledger light" id="prices">
    <div class="ledger-head">
      <div><p class="eyebrow dark">TURNAROUND &amp; PRICES</p><h2>The date it<br><em>comes back.</em></h2></div>
      <p>Business days in the lab, counted from when your scan or case arrives. Published, so you can quote patients with confidence.</p>
    </div>
    <div class="ledger-grid"><div>{ledger(["ceramic", "implant"])}</div><div>{ledger(["removable"])}</div></div>
  </section>

  <section class="shipping" id="shipping">
    <div class="shipping-copy">
      <p class="eyebrow">SHIPPING NATIONWIDE</p>
      <h2>Wherever your<br><em>chair is.</em></h2>
      <a class="inline-link" href="/nationwide-dental-lab/">How shipping works →</a>
    </div>
    <div class="shipping-grid">{ship}</div>
  </section>

  <section class="shade">
    <div class="shade-photo">{img("shade", "Crown beside ceramic shade tabs", "(max-width:980px) 92vw, 50vw", 'loading="lazy"')}</div>
    <div class="shade-copy">
      <p class="eyebrow">COMPLIMENTARY SHADE MATCHING</p>
      <h2>A shade<br><em>closer.</em></h2>
      <p>We match shade for every client. Send the tab reading or a photo under daylight. We do the rest.</p>
    </div>
  </section>

  <section class="owner" id="owner">
    <figure class="owner-photo">{img("owner-haibert", "Haibert Aivazian, owner of DentX Dental Lab, in the lab", "(max-width:980px) 92vw, 42vw", 'loading="lazy"', 1400, 1750)}</figure>
    <div class="owner-copy">
      <p class="eyebrow">MEET THE OWNER</p>
      <h2>Haibert Aivazian.<br><em>Owner, at the bench.</em></h2>
      <p>Haibert has been in business since 2008, and DentX is his lab. He's licensed, he works the bench himself, and he does the shade matching.</p>
      <p>Big labs are built for volume, so your case becomes a ticket number. Haibert built DentX for offices that want to know who is making their crowns, and want that person to pick up the phone.</p>
      <p>Shade is the part he won't hand off. Send a photo, or bring your patient by the Tarzana lab and he'll match it in person.</p>
      <ul class="owner-facts"><li><strong>2008</strong>In business since</li><li><strong>Licensed</strong>Dental lab</li><li><strong>Free</strong>Shade matching, by Haibert</li></ul>
      <div class="actions"><a class="btn btn-gold" href="tel:{PHONE_TEL}" data-ev="call">Call Haibert</a><a class="btn btn-ghost" href="/about/">About Haibert</a></div>
    </div>
  </section>

  <section class="faq light" id="faq">
    <div class="ledger-head"><div><p class="eyebrow dark">QUESTIONS FROM OFFICES</p><h2>Before you<br><em>send a case.</em></h2></div></div>
    <div class="faq-list">{faq_html(FAQ_HOME)}</div>
  </section>

  {lead_form()}
</main>
{footer()}"""

# ---------------------------------------------------------------- inner pages
def page(path, d):
    name = d["h1"].replace("<br>", " ").replace("<em>", "").replace("</em>", "").replace("&amp;", "&")
    ld = [lab_ld(), crumbs_ld(path, name)] + ([faq_ld(d["faq"])] if d["faq"] else [])
    body = "".join(f"<div><h2>{e(t)}</h2><p>{e(p)}</p></div>" for t, p in d["body"])
    pic = ""
    if d["img"]:
        pic = '<figure class="page-img">' + img(d["img"][:-5], e(d["img_alt"]), "(max-width:1100px) 92vw, 1100px", 'fetchpriority="high"') + "</figure>"
    prices = (f'<section class="ledger light"><div class="ledger-head"><div><p class="eyebrow dark">TURNAROUND &amp; PRICES</p><h2>Published <em>prices.</em></h2></div></div><div class="ledger-one">{ledger(d["cats"])}</div></section>' if d["cats"] else "")
    ship = "".join(f"<div><h3>{a}</h3><p>{b}</p></div>" for a, b in SHIP)
    related = "".join(f'<a href="{p}">{e(x["h1"].replace("<br>", " ").replace("<em>", "").replace("</em>", "").replace("&amp;", "&"))} →</a>' for p, x in PAGES.items() if p != path)
    faq = (f'<section class="faq light"><div class="faq-list">{faq_html(d["faq"])}</div></section>' if d["faq"] else "")
    return head(d["title"], d["desc"], path, ld, preload=d["img"]) + f"""
<body class="inner">
{header()}
<main id="main">
  <section class="page-hero">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/">DentX Dental Lab</a> / <span>{e(name)}</span></nav>
    <h1>{d["h1"]}</h1>
    <p class="page-lead">{e(d["lead"])}</p>
    <div class="actions"><a class="btn btn-gold" href="#start">Send a case</a><a class="btn btn-ghost" href="tel:{PHONE_TEL}" data-ev="call">Call {PHONE}</a></div>
    {pic}
  </section>
  <section class="page-body light">{body}</section>
  {prices}
  <section class="shipping"><div class="shipping-copy"><p class="eyebrow">SHIPPING NATIONWIDE</p><h2>Wherever your<br><em>chair is.</em></h2></div><div class="shipping-grid">{ship}</div></section>
  {faq}
  {lead_form()}
  <nav class="related" aria-label="More from DentX">{related}<a href="/">Home →</a></nav>
</main>
{footer()}"""

# ---------------------------------------------------------------- llms.txt + sitemap + robots
def llms():
    lines = ["# DentX Dental Lab", "",
             "> Premium digital dental laboratory in Tarzana, California, shipping to dental offices across the United States. Complimentary shade matching. Digital cases from Medit, iTero, Shining 3D, DEXIS IOS Cloud or STL.", "",
             "- Legal name: DentX Dental Lab Inc", f"- Address: {ADDR}", f"- Phone: +1 {PHONE}", f"- Email: {EMAIL}",
             "- Audience: dentists and dental office managers (not patients)", "", "## Shipping"]
    lines += [f"- {a}: {b}" for a, b in SHIP]
    lines += ["", "## Turnaround (business days in the lab, from arrival) and prices"]
    for _, label, rows in CATALOG:
        lines.append(f"### {label}")
        lines += [f"- {n}: " + (f"{d} days, " if d else "") + p + (f" ({note})" if note else "") for n, note, d, p, _ in rows]
    lines += ["", "## Pages", f"- Home: {SITE}/"] + [f"- {d['title'].split(' |')[0]}: {SITE}{p}" for p, d in PAGES.items()]
    return "\n".join(lines) + "\n"

def write(path, text):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    open(path, "w").write(text)

if __name__ == "__main__":
    write("index.html", home())
    for p, d in PAGES.items():
        write(p.strip("/") + "/index.html", page(p, d))
    write("llms.txt", llms())
    urls = ["/"] + list(PAGES)
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls) + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: {SITE}/sitemap.xml\n")
    print("built", len(urls), "pages")
