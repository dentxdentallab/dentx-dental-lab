"""DentX static site generator. One data source -> all pages, JSON-LD, llms.txt, sitemap.

    python3 build.py          # writes pages into this folder (repo root = Vercel output)
"""
import json, os, html

SITE = os.environ.get("SITE_URL", "https://www.dentxdentallab.com")  # ponytail: placeholder until the real domain is connected
PHONE, PHONE_TEL = "(818) 687-0085", "+18186870085"
EMAIL = "Dentxdentallab@yahoo.com"
ADDR = "18401 Burbank Blvd #110, Tarzana, CA 91356"
HOURS = "Mon–Fri 9 am–6 pm"
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
    ("Los Angeles County", "Free pickup and delivery by our own driver. Call or text before 12 pm and we'll do our best to pick up the same day."),
    ("Outside LA County, digital", "Send your scan. Finished work ships back for $7 per case."),
    ("Outside LA County, impressions", "We email you a prepaid label, billed at the carrier's cost. Finished work ships back for $7 per case."),
]

FAQ_HOME = [
    ("Do you deliver?", "Yes. Across Los Angeles County our own driver picks up and delivers for free. Call or text before 12 pm and we'll do our best to pick up the same day. Outside LA County we ship: finished work is $7 per case to ship back, and for impressions we email a prepaid label billed at the carrier's cost."),
    ("How fast are zirconia and E.max crowns?", "Up to 5 business days in the lab, counted from when your case or scan arrives with a complete Rx. Shipping time outside LA County is on top of that."),
    ("Which intraoral scanners can send cases to DentX?", "Medit, iTero, Shining 3D and DEXIS IOS Cloud, or email STL files. Call the lab and we will walk you through connecting your scanner account."),
    ("What do you need with each case?", "A complete Rx: service, teeth, shade and due date. If the Rx is missing or unclear we call your office before we start, and the clock starts once we have it."),
    ("How do you match shade?", "Digitally. Instead of holding a shade tab up to the tooth and guessing by eye, DentX measures shade with a digital shade system that holds the full VITA range and bleach shades, so the restoration matches the teeth around it. Send your shade notes or photos with the case, or bring the patient by the Tarzana lab."),
    ("How long do dentures and partials take?", "Acrylic dentures: 6 business days for the bite block, 7 for teeth try-in and 7 for the final finish. Printed dentures take 7 business days, combination metal + Valplast 12."),
    ("Is there a rush option?", "Stayplates can be done in 2 business days with a $50 rush fee. For other rush requests, call the lab."),
    ("Where is DentX Dental Lab and when are you open?", f"{ADDR}, in the San Fernando Valley. Open {HOURS}. Phone or text {PHONE}, email {EMAIL}."),
]

PAGES = {
    "/zirconia-crowns/": dict(
        title="Zirconia Crowns Dental Lab | $75, 5 Business Days | DentX",
        desc="Zirconia crowns from $75 in 5 business days. Layered zirconia $99. Free pickup and delivery across LA County, shipping nationwide. DentX Dental Lab, Tarzana CA.",
        h1="Zirconia crowns.<br><em>Five days in the lab.</em>",
        lead="Monolithic zirconia from $75 and layered zirconia from $99, designed from your scan and matched with digital shade technology. Free pickup and delivery across LA County.",
        cats=["ceramic"], img="bench-ceramic.webp", img_alt="Ceramist layering porcelain on a zirconia crown beside the furnace",
        body=[
            ("Monolithic or layered", "Monolithic zirconia for strength on posterior teeth and bruxers. Layered zirconia when the anterior needs more life in the incisal third. Shade is measured digitally, not guessed against a tab."),
            ("From scan to finished crown", "Send from Medit, iTero, Shining 3D, DEXIS IOS Cloud or by STL. Up to 5 business days in the lab, counted from when your scan arrives with a complete Rx. In LA County our driver delivers it free; elsewhere it ships back for $7."),
            ("Temporaries and wax-ups", "PMMA temporary crowns are $45 in 5 business days. Diagnostic wax-ups are $25 in 4 business days."),
        ],
        faq=[("How much does a zirconia crown cost?", "A zirconia crown is $75. Layered zirconia is $99."),
             ("How long does a zirconia crown take?", "5 business days in the lab for monolithic zirconia, 6 for layered, counted from when the case arrives.")]),
    "/emax-crowns-veneers/": dict(
        title="E.max Crowns & Veneers Lab | From $85, 5 Days | DentX",
        desc="E.max crowns $85, veneers $99, inlays and onlays $75, all in up to 5 business days, with digital shade matching. DentX Dental Lab, Tarzana CA.",
        h1="E.max crowns <em>&amp;</em> veneers.",
        lead="Lithium disilicate crowns, veneers and inlays built for esthetics: natural translucency, characterized incisal edges, and shade matched digitally. Up to 5 business days in the lab.",
        cats=["ceramic"], img="hero.webp", img_alt="Glazed three-unit ceramic bridge",
        body=[
            ("Anterior esthetics", "E.max crowns at $85 and veneers at $99 for cases where translucency matters. Layered E.max at $99 in 6 business days."),
            ("Conservative restorations", "Inlays and onlays at $75 in 5 business days. Diagnostic wax-ups at $25 to plan the case with your patient."),
            ("Shade, measured digitally", "No more guessing against a shade tab. Our digital shade system covers the full VITA range and bleach shades, so the color is measured, not eyeballed."),
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
        desc="Send cases to DentX Dental Lab from anywhere in the U.S. Free pickup and delivery across LA County; elsewhere $7 per case to ship finished work back.",
        h1="Pickup in LA County.<br><em>Shipping everywhere else.</em>",
        lead="Our own driver covers Los Angeles County for free. Everywhere else, send your scan or impressions and we ship the finished work back for $7 per case.",
        cats=[], img="bench-ceramic.webp", img_alt="Ceramist finishing a crown at the DentX bench",
        body=[
            ("Los Angeles County", "Free pickup and delivery by our own driver. Call or text (818) 687-0085 before 12 pm and we'll do our best to pick up the same day."),
            ("Digital cases from anywhere", "Send from Medit, iTero, Shining 3D, DEXIS IOS Cloud or by STL. No box to pack. Up to 5 business days in the lab from when the scan arrives with a complete Rx, then it ships back for $7 per case."),
            ("Impressions and models", "Outside LA County we email you a prepaid label, billed at the carrier's cost. Finished work ships back for $7 per case."),
            ("Why offices switch", "One flat price list, published. Turnaround in business days you can book patients around. Digital shade matching. A lab owner who answers the phone."),
        ],
        faq=[("Do you ship to other states?", "Yes. DentX ships to dental offices across the United States."),
             ("Who pays for shipping?", "In LA County, nobody: pickup and delivery are free. Outside LA County, shipping finished work back is $7 per case, and inbound labels for impressions are billed at the carrier's cost.")]),
    "/dental-lab-los-angeles/": dict(
        title="Dental Lab in Los Angeles | Free Pickup & Delivery in LA County | DentX",
        desc="Full-service dental lab serving Los Angeles County with free pickup and delivery by our own driver. Zirconia $75, E.max $85, implants, dentures. Up to 5 business days.",
        h1="The dental lab for<br><em>Los Angeles offices.</em>",
        lead="Our own driver picks up and delivers across Los Angeles County, free. Call or text before 12 pm and we'll do our best to pick up the same day.",
        cats=["ceramic"], img="bench-ceramic.webp", img_alt="Ceramist finishing a crown at the DentX lab in Tarzana",
        body=[
            ("Where we pick up", "All of Los Angeles County, including Los Angeles, Beverly Hills, Santa Monica, Burbank, Glendale, Pasadena, Encino, Sherman Oaks, Woodland Hills, Calabasas, Northridge, Long Beach and Torrance."),
            ("What we make", "Zirconia and E.max crowns, veneers, implant crowns and custom abutments, dentures, partials, Valplast and night guards. Every price is published on this site."),
            ("How fast", "Up to 5 business days in the lab for crowns and veneers, counted from when your case arrives with a complete Rx. Dentures go by stage."),
            ("Why LA offices choose DentX", "A lab owner on the phone, digital shade matching instead of guessing with a tab, and a driver who comes to you."),
        ],
        faq=[("Do you pick up in Los Angeles?", "Yes. Pickup and delivery are free anywhere in Los Angeles County."),
             ("How do I schedule a pickup?", "Call or text (818) 687-0085. Before 12 pm we do our best to pick up the same day.")]),
    "/dental-lab-san-fernando-valley/": dict(
        title="Dental Lab in the San Fernando Valley | Tarzana | DentX Dental Lab",
        desc="DentX Dental Lab in Tarzana serves San Fernando Valley dental offices with free pickup and delivery: Encino, Sherman Oaks, Woodland Hills, Van Nuys, Northridge, Studio City.",
        h1="Your Valley<br><em>dental lab.</em>",
        lead="We're on Burbank Blvd in Tarzana, minutes from your office. Free pickup and delivery across the Valley and all of LA County.",
        cats=["ceramic", "removable"], img="bench-removable.webp", img_alt="Dentures on an articulator at the DentX lab bench in Tarzana",
        body=[
            ("Close by", "Tarzana, Encino, Sherman Oaks, Woodland Hills, Reseda, Van Nuys, Northridge, Studio City, North Hollywood, Calabasas and the rest of the Valley."),
            ("Same-day pickup", "Call or text before 12 pm and our driver will do our best to pick up the same day. Delivery of finished work is free too."),
            ("Bring the patient", "For esthetic anterior cases, patients are welcome at the lab for a digital shade appointment."),
        ],
        faq=[("Where is DentX Dental Lab?", f"{ADDR}, open {HOURS}."),
             ("Do you deliver in the Valley?", "Yes, free, by our own driver, across the San Fernando Valley and all of LA County.")]),
    "/digital-shade-matching/": dict(
        title="Digital Shade Matching for Crowns & Veneers | DentX Dental Lab",
        desc="DentX measures shade digitally with a system that holds the full VITA range and bleach shades, so crowns and veneers match the natural teeth. Esthetic lab in Tarzana, CA.",
        h1="Shade,<br><em>measured digitally.</em>",
        lead="A shade tab held up to a tooth depends on the light in the room and the eye of whoever holds it. We measure shade digitally instead.",
        cats=[], img="shade.webp", img_alt="Ceramic crown compared for shade under daylight",
        body=[
            ("Why a tab isn't enough", "Room light, fatigue and the background all change how a tab reads. Two people can read the same tooth differently. That's where most shade remakes start."),
            ("What we use", "A digital shade system that holds the full VITA range and bleach shades, so the target color is measured and recorded, not eyeballed."),
            ("Where it matters most", "Anterior crowns, veneers and layered zirconia or E.max, where the restoration sits next to natural teeth."),
            ("How to send shade", "Send your shade notes and photos with the case, or bring the patient to the Tarzana lab for a shade appointment."),
        ],
        faq=[("Is digital shade matching extra?", "No. It's how every case is shade-matched at DentX."),
             ("Which shade systems do you cover?", "The full VITA range and bleach shades.")]),
    "/about/": dict(
        title="About Haibert Aivazian, Owner of DentX Dental Lab | Tarzana, CA",
        desc="Meet Haibert Aivazian, licensed owner of DentX Dental Lab, in business since 2008. Esthetic crown and bridge, digital shade matching, published prices. Tarzana, CA.",
        h1="Meet Haibert Aivazian.<br><em>Owner of DentX.</em>",
        lead="Licensed, in business since 2008, and still at the bench. When you send a case to DentX, you know whose hands it's in.",
        cats=[], img="owner-haibert.webp", img_alt="Haibert Aivazian, owner of DentX Dental Lab, in DentX scrubs",
        body=[
            ("Since 2008", "Haibert has been in business since 2008. In that time dentistry moved from impressions to intraoral scans, and DentX takes both."),
            ("Built for esthetics", "Haibert's focus is the work patients notice: anterior crowns and veneers with natural translucency, surface texture and the right value. Shade is measured with digital shade technology, not guessed with a tab. Patients are welcome at the Tarzana lab for a shade appointment."),
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
            ("Every case needs an Rx", "Service, teeth, shade and due date. If something is missing we call your office first, and the 5 business days start once the Rx is complete."),
            ("Sending impressions from outside LA County?", "Request a label below and we'll email a prepaid one, billed at the carrier's cost. Finished work ships back for $7 per case."),
            ("In LA County?", "Call or text before 12 pm and our driver will do their best to pick up the same day. Free."),
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
    return (f'<img src="/assets/{name}.webp" srcset="/assets/{name}-480.webp 480w, /assets/{name}-800.webp 800w, /assets/{name}.webp {w}w" '
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

def guide_data():
    """Facts for the in-browser Quick help guide (no external services)."""
    cats = [{"key": k, "label": l, "rows": [[n, d, p] for n, _, d, p, _ in rows if p.startswith("$")]} for k, l, rows in CATALOG]
    return {"phone": PHONE, "tel": PHONE_TEL, "email": EMAIL, "hours": HOURS, "ship": SHIP, "cats": cats, "scanners": SCANNERS}

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
        "description": "Digital dental laboratory in Tarzana, California. Free pickup and delivery across Los Angeles County, shipping to dental offices nationwide. Zirconia and E.max crowns, veneers, implant crowns, dentures, partials and night guards. Digital shade matching.",
        "telephone": "+1-818-687-0085", "email": EMAIL, "priceRange": "$15–$250", "foundingDate": "2008",
        "founder": {"@type": "Person", "name": OWNER, "jobTitle": "Owner", "image": SITE + "/assets/owner-haibert.webp", "url": SITE + "/about/"},
        "address": {"@type": "PostalAddress", "streetAddress": "18401 Burbank Blvd #110", "addressLocality": "Tarzana",
                    "addressRegion": "CA", "postalCode": "91356", "addressCountry": "US"},
        "areaServed": [{"@type": "AdministrativeArea", "name": "Los Angeles County, CA"}, {"@type": "Country", "name": "United States"}],
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "18:00"}],
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
<script>window.DX={json.dumps(guide_data(), ensure_ascii=False)}</script>
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
  <form class="lead-form" novalidate>
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
    <p class="form-note">Goes straight to the lab by text or email. Nothing is stored on this website.</p>
    <p class="form-status" role="status" aria-live="polite"></p>
  </form>
</section>"""

def footer():
    links = "".join(f'<a href="{p}">{e(d["h1"].replace("<br>", " ").replace("<em>", "").replace("</em>", "").replace("&amp;", "&"))}</a>' for p, d in PAGES.items())
    return f"""<section class="close" id="contact">
  <div class="contact-top">
    <div class="contact-mark">{svg_logo()}</div>
    <h2>Contact us <em>today.</em></h2>
    <p class="contact-who"><img src="/assets/owner-haibert-480.webp" alt="" width="480" height="640" loading="lazy">You'll talk to Haibert directly.</p>
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
    <span>DentX Dental Lab Inc · Tarzana, CA · {HOURS} · Free pickup &amp; delivery in LA County</span>
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
    steps = [("Day 0", "Case arrives", "With a complete Rx, the clock starts."),
             ("Day 1", "Design", "Your crown is designed from the scan."),
             ("Days 2–3", "Mill & sinter", "Milled and fired in-house."),
             ("Day 4", "Stain & glaze", "Characterized to the digital shade."),
             ("Day 5", "Checked & out", "Inspected, packed, on its way."),
             ("Delivery", "To your office", "Free by our driver in LA County, $7 shipping elsewhere.")]
    step_html = "".join(f'<li><span class="day">{d}</span><h3>{t}</h3><p>{p}</p></li>' for d, t, p in steps)
    ld = [lab_ld(), faq_ld(FAQ_HOME)]
    return head("DentX Dental Lab | Zirconia, E.max, Implants &amp; Dentures · Ships Nationwide",
                "Premium dental lab in Tarzana, CA shipping nationwide. Zirconia crowns $75 and E.max $85 in up to 5 business days, free pickup and delivery across LA County, digital shade matching.",
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
      <p>Zirconia &amp; E.max crowns in up to 5 business days. Free pickup and delivery across LA County, shipping nationwide.</p>
      <div class="actions">
        <a class="btn btn-gold" href="/send-a-case/">Send a case</a>
        <a class="btn btn-ghost" href="tel:{PHONE_TEL}" data-ev="call">Call the lab</a>
      </div>
    </div>
    <div class="hero-bottom">
      <span>Free LA County pickup &amp; delivery</span>
      <span>Digital shade matching</span>
      <span>Published prices</span>
    </div>
  </section>

  <section class="clock" aria-labelledby="clock-h">
    <div class="clock-head">
      <p class="eyebrow">HOW A CROWN MOVES</p>
      <h2 id="clock-h">Case in.<br><em>Out in 5.</em></h2>
      <p>Up to 5 business days in the lab, counted from when your case arrives with a complete Rx. In LA County our driver brings it back free.</p>
    </div>
    <ol class="clock-track">{step_html}</ol>
  </section>

  <section class="inside" id="inside">
    <div class="inside-copy">
      <p class="eyebrow">INSIDE THE LAB</p>
      <h2>Walk through<br><em>the lab.</em></h2>
      <p>Scan in, designed, milled, printed, stained and glazed by hand, then checked by Haibert before it ships. All in one lab in Tarzana.</p>
      <div class="actions"><a class="btn btn-gold" href="/send-a-case/">Send a case</a><a class="btn btn-ghost" href="/about/">Meet Haibert</a></div>
    </div>
    <div class="phone"><video class="lazy-video" muted loop playsinline preload="none" poster="/assets/video/lab-poster.webp" width="540" height="960" aria-label="Walkthrough of the DentX dental lab: CAD design, milling, 3D printing, staining and glazing">
      <source data-src="/assets/video/lab-9x16.mp4" type="video/mp4"></video></div>
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
    <div class="shade-photo">{img("shade", "Ceramic crown compared for shade under daylight", "(max-width:980px) 92vw, 50vw", 'loading="lazy"')}</div>
    <div class="shade-copy">
      <p class="eyebrow">DIGITAL SHADE MATCHING</p>
      <h2>Measured,<br><em>not guessed.</em></h2>
      <p>Most labs still match shade by holding a tab next to a tooth. We measure it with a digital shade system that holds the full VITA range and bleach shades, so the crown disappears next to the natural teeth.</p>
      <a class="inline-link" href="/digital-shade-matching/">How digital shade matching works →</a>
    </div>
  </section>

  <section class="owner" id="owner">
    <figure class="owner-photo">{img("owner-haibert", "Haibert Aivazian, owner of DentX Dental Lab, in DentX scrubs", "(max-width:980px) 92vw, 42vw", 'loading="lazy"', 1086, 1448)}</figure>
    <div class="owner-copy">
      <p class="eyebrow">MEET THE OWNER</p>
      <h2>Haibert Aivazian.<br><em>Owner, at the bench.</em></h2>
      <p>Haibert has been in business since 2008, and DentX is his lab. He's licensed, he works the bench himself, and his focus is esthetics: the anterior crowns and veneers patients actually look at.</p>
      <p>Big labs are built for volume, so your case becomes a ticket number. Haibert built DentX for offices that want to know who is making their crowns, and want that person to pick up the phone.</p>
      <p>He runs DentX on current technology, from digital design and in-house milling to digital shade measurement, so what you see in the mouth matches what you planned.</p>
      <ul class="owner-facts"><li><strong>2008</strong>In business since</li><li><strong>Licensed</strong>Dental lab</li><li><strong>Digital</strong>Shade measurement</li></ul>
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
        portrait = d["img"].startswith("owner-")
        pic = (f'<figure class="page-img{" portrait" if portrait else ""}">' + img(d["img"][:-5], e(d["img_alt"]), "(max-width:680px) 92vw, 520px" if portrait else "(max-width:1100px) 92vw, 1100px", 'fetchpriority="high"', *((1086, 1448) if portrait else (1400, 933))) + "</figure>")
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
             "> Premium digital dental laboratory in Tarzana, California, shipping to dental offices across the United States. Digital shade matching. Digital cases from Medit, iTero, Shining 3D, DEXIS IOS Cloud or STL.", "",
             "- Legal name: DentX Dental Lab Inc", f"- Address: {ADDR}", f"- Phone: +1 {PHONE}", f"- Email: {EMAIL}", f"- Hours: {HOURS}",
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
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    print("built", len(urls), "pages")
