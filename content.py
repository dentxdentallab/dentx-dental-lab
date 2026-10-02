"""Extra pages for build.py: service-area pages, scanner/price hubs and guides.
Facts must match build.py data (prices, turnaround, delivery). Body text is trusted HTML (inline links allowed).
"""

# ---------------------------------------------------------------- service areas
# (slug, city, miles from the lab (approx.), route, ZIPs, neighbors, local note)
CITIES = [
    ("encino", "Encino", 3, "east on Ventura Blvd", "91316, 91436", "Tarzana, Sherman Oaks, Van Nuys",
     "Encino is the next neighborhood over, so most Encino offices are a short hop on Ventura Blvd. Offices along the Ventura corridor are usually on the same pickup loop as Tarzana."),
    ("woodland-hills", "Woodland Hills", 3, "west on Ventura Blvd", "91364, 91367", "Tarzana, Calabasas, Canoga Park",
     "Woodland Hills borders Tarzana to the west. Medical buildings around Warner Center and along Ventura Blvd are minutes from the lab."),
    ("sherman-oaks", "Sherman Oaks", 8, "east on the 101", "91403, 91423", "Encino, Studio City, Van Nuys",
     "Sherman Oaks has one of the densest clusters of dental offices in the Valley, around Ventura and Van Nuys Blvd. It's a regular stop for our driver."),
    ("van-nuys", "Van Nuys", 6, "east on Victory or Burbank Blvd", "91401, 91405, 91406, 91411", "Encino, Sherman Oaks, North Hills",
     "Van Nuys offices are a straight drive across the Valley floor, without the freeway. Specialists and general offices along Van Nuys Blvd are on our regular route."),
    ("burbank", "Burbank", 15, "east on the 101 and 134", "91501, 91502, 91504, 91505, 91506", "Glendale, North Hollywood, Toluca Lake",
     "Burbank is east across the Valley on the 101 and 134. Our driver covers Burbank on the same free pickup and delivery as the rest of LA County."),
    ("glendale", "Glendale", 18, "east on the 134", "91201–91208", "Burbank, Eagle Rock, La Crescenta",
     "Glendale is on our eastern route via the 134. Glendale offices get the same free pickup and delivery and the same published prices."),
]

def city_pages():
    out = {}
    for slug, city, miles, route, zips, near, note in CITIES:
        out[f"/dental-lab-{slug}/"] = dict(
            group="areas", nav=city,
            title=f"Dental Lab Near {city}, CA | Free Pickup | DentX",
            desc=f"DentX Dental Lab is about {miles} miles from {city}. Free pickup and delivery for {city} dental offices. Zirconia $75, E.max $85, 5 business days.",
            h1=f"Dental lab for<br><em>{city} offices.</em>",
            lead=f"DentX is in Tarzana, about {miles} miles from {city} ({route}). Our own driver picks up and delivers for free, and every price is published.",
            cats=["ceramic"], img="bench-ceramic.webp", img_alt=f"Ceramist finishing a crown at DentX Dental Lab, which serves {city} dental offices",
            body=[
                (f"Pickup in {city}", f"{note} Call or text <a href=\"tel:+18186870085\">(818) 687-0085</a> before 12 pm and we'll do our best to pick up the same day. Delivery of finished work is free too."),
                ("Where we go", f"All of {city} ({zips}) plus {near}, and the rest of <a href=\"/dental-lab-los-angeles/\">Los Angeles County</a>."),
                ("What we make", "<a href=\"/zirconia-crowns/\">Zirconia crowns</a> from $75, <a href=\"/emax-crowns-veneers/\">E.max crowns</a> $85 and veneers $99, <a href=\"/implant-crowns/\">implant crowns</a> from $120, <a href=\"/dentures-partials/\">dentures and partials</a> from $160, <a href=\"/night-guards/\">night guards</a> $85. See the full <a href=\"/dental-lab-price-list/\">price list</a>."),
                ("How fast", f"Up to 5 business days in the lab for crowns and veneers, counted from when your case arrives with a complete Rx. Because {city} is local, there's no shipping time on top: our driver brings it back."),
                ("Digital or impressions", "Send scans from Medit, iTero, Shining 3D or DEXIS, or STL by email (see <a href=\"/digital-dental-lab/\">digital cases</a>). Impressions and models go with our driver, with a <a href=\"/assets/dentx-lab-slip.pdf\">printed lab slip</a>."),
            ],
            faq=[(f"Do you pick up from dental offices in {city}?", f"Yes. Pickup and delivery are free in {city} and everywhere in Los Angeles County. Call or text (818) 687-0085; before 12 pm we do our best to pick up the same day."),
                 (f"How far is DentX Dental Lab from {city}?", f"About {miles} miles. The lab is at 18401 Burbank Blvd #110, Tarzana, CA 91356."),
                 (f"How long do crowns take for a {city} office?", "Up to 5 business days in the lab from when the case arrives with a complete Rx. Local delivery is free and adds no shipping time.")])
    return out

# ---------------------------------------------------------------- hubs, services, guides
EXTRA = {
    "/dental-lab-price-list/": dict(
        group="lab", nav="Price list",
        title="Dental Lab Price List & Fees 2026 | DentX Dental Lab",
        desc="DentX Dental Lab price list: zirconia $75, E.max $85, veneers $99, implant crowns $120–$130, dentures from $160, night guards $85, with turnaround.",
        h1="Dental lab<br><em>price list.</em>",
        lead="Every price and turnaround time we charge, published. No quote requests, no surprise line items. Turnaround is business days in the lab, counted from when your case arrives with a complete Rx.",
        cats=["ceramic", "implant", "removable"], img=None, img_alt="",
        body=[
            ("What's included", "Design from your scan, milling or printing, staining and glazing, <a href=\"/digital-shade-matching/\">digital shade matching</a>, and a final check before the case leaves the lab."),
            ("Delivery and shipping", "Free pickup and delivery across Los Angeles County by our own driver. Outside LA County, finished work ships back for $7 per case; for impressions we email a prepaid label billed at the carrier's cost. Details on <a href=\"/nationwide-dental-lab/\">shipping</a>."),
            ("Rush", "Stayplates can be done in 2 business days with a $50 rush fee. For other rush cases, call <a href=\"tel:+18186870085\">(818) 687-0085</a> and we'll tell you honestly what's possible."),
            ("How turnaround is counted", "Business days in the lab, starting when the case and a complete Rx arrive. Weekends and shipping time are not included. See <a href=\"/guides/dental-lab-turnaround-times/\">turnaround times explained</a>."),
        ],
        faq=[("How much does a zirconia crown cost from DentX?", "$75 for monolithic zirconia and $99 for layered zirconia or E.max."),
             ("Are there extra fees for delivery?", "Not in Los Angeles County: pickup and delivery are free. Outside LA County, return shipping is $7 per case."),
             ("Do prices change by case?", "No. The published price is the price for that restoration.")]),
    "/digital-dental-lab/": dict(
        group="lab", nav="Digital cases",
        title="Digital Dental Lab | Medit, iTero, DEXIS, STL | DentX",
        desc="Send digital cases to DentX Dental Lab from Medit, iTero, Shining 3D, DEXIS IOS Cloud or STL by email. Crowns in up to 5 business days, shipped nationwide.",
        h1="Digital cases from<br><em>your scanner.</em>",
        lead="Scan, send, done. DentX receives cases from Medit, iTero, Shining 3D and DEXIS IOS Cloud, or STL files by email, from offices anywhere in the U.S.",
        cats=["ceramic"], img="bench-implant.webp", img_alt="Implant crown designed from an intraoral scan at DentX Dental Lab",
        body=[
            ("Medit", "Send from Medit Link to DentX as your lab. Call us once and we'll confirm the connection so your first case lands on our side."),
            ("iTero", "Send iTero scans to DentX by adding us as a lab in your iTero account. We'll walk you through it on the phone the first time."),
            ("Shining 3D and DEXIS IOS Cloud", "Both send straight to the lab once we're connected. Same process: one call, then every case after that is a click."),
            ("No integration? Send STL", "Export STL files from any scanner and email them with the Rx to <a href=\"mailto:Dentxdentallab@yahoo.com\">Dentxdentallab@yahoo.com</a>."),
            ("What to include", "Prep and opposing scans, bite registration, and a complete Rx: service, teeth, shade, due date. Shade photos help for anterior work. See the <a href=\"/guides/dental-lab-rx-checklist/\">Rx checklist</a>."),
            ("No box, no courier", "Digital cases start the moment they arrive. Up to 5 business days in the lab, then the work comes back by our driver in LA County or ships for $7 per case elsewhere."),
        ],
        faq=[("Which intraoral scanners can send cases to DentX?", "Medit, iTero, Shining 3D and DEXIS IOS Cloud. Any other scanner can export STL files and email them."),
             ("Do you accept STL files by email?", "Yes. Email the STL files and Rx to Dentxdentallab@yahoo.com."),
             ("Can I send digital cases from outside California?", "Yes. DentX takes digital cases from offices across the United States and ships finished work back for $7 per case.")]),
    "/night-guards/": dict(
        group="services", nav="Night guards",
        title="Night Guards Dental Lab | Hard or Soft, $85, 3 Days | DentX",
        desc="Hard and soft night guards from DentX Dental Lab: $85, 3 business days in the lab. Free pickup and delivery in LA County, shipping nationwide.",
        h1="Night guards.<br><em>Three days in the lab.</em>",
        lead="Hard or soft night guards at $85, back in 3 business days. From a scan or an impression, with free pickup and delivery across LA County.",
        cats=["removable"], img="bench-removable.webp", img_alt="Removable appliances at the DentX lab bench",
        body=[
            ("Hard or soft", "Hard night guards for bruxers who need a durable, adjustable surface. Soft guards for patients who want comfort first. Both are $85."),
            ("From a scan or an impression", "Send a full-arch scan with a bite from Medit, iTero, Shining 3D or DEXIS, or STL by email. Impressions and models work too. See <a href=\"/digital-dental-lab/\">digital cases</a>."),
            ("Turnaround", "3 business days in the lab from when the case arrives with a complete Rx. In LA County our driver delivers it free."),
            ("Protecting your restorations", "After a big <a href=\"/zirconia-crowns/\">zirconia</a> or <a href=\"/emax-crowns-veneers/\">E.max</a> case, a night guard is the cheapest insurance the patient can buy."),
        ],
        faq=[("How much is a night guard?", "$85, hard or soft."),
             ("How long does a night guard take?", "3 business days in the lab from when the case arrives.")]),
    "/guides/": dict(
        group="guides", nav="All guides", kind="guide-hub",
        title="Dental Lab Guides for Dentists | DentX Dental Lab",
        desc="Practical guides from DentX Dental Lab: zirconia vs E.max, monolithic vs layered zirconia, how to send a case, the Rx checklist and turnaround times.",
        h1="Guides for<br><em>dental offices.</em>",
        lead="Short, practical answers to the questions offices ask us most. Written by the lab, for the people sending the cases.",
        cats=[], img=None, img_alt="",
        body=[
            ("Zirconia vs E.max", "When to choose each material, prep requirements and cementation. <a href=\"/guides/zirconia-vs-emax/\">Read the guide →</a>"),
            ("Monolithic vs layered zirconia", "Strength versus esthetics, and where each belongs in the mouth. <a href=\"/guides/monolithic-vs-layered-zirconia/\">Read the guide →</a>"),
            ("How to send a case to a dental lab", "Digital, impressions, pickup or shipping, step by step. <a href=\"/guides/how-to-send-a-case-to-a-dental-lab/\">Read the guide →</a>"),
            ("Dental lab Rx checklist", "What every Rx needs so the case starts on time. <a href=\"/guides/dental-lab-rx-checklist/\">Read the guide →</a>"),
            ("Dental lab turnaround times", "How turnaround is counted and how to schedule seats. <a href=\"/guides/dental-lab-turnaround-times/\">Read the guide →</a>"),
        ],
        faq=[]),
    "/guides/zirconia-vs-emax/": dict(
        group="guides", nav="Zirconia vs E.max", kind="guide",
        title="Zirconia vs E.max Crowns: Which to Prescribe | DentX",
        desc="Zirconia vs E.max (lithium disilicate): strength, esthetics, prep depth and cementation, and when a dental lab recommends each. Prices: zirconia $75, E.max $85.",
        h1="Zirconia vs E.max:<br><em>which to prescribe.</em>",
        lead="Both are metal-free and both look good. The choice comes down to where the tooth is, how much room you have, and how the patient bites.",
        cats=["ceramic"], img="hero.webp", img_alt="Glazed ceramic crowns at DentX Dental Lab",
        body=[
            ("Short answer", "Posterior, heavy bite, limited reduction or a bruxer: monolithic zirconia. Anterior or premolar where translucency matters and you can bond: E.max. For an anterior that needs strength and life, layered zirconia sits in between."),
            ("Strength", "Zirconia is the stronger material by a wide margin. Typical flexural strength for conventional zirconia is several times that of lithium disilicate, which is why it's the default for molars and bruxers. Higher-translucency zirconias trade some of that strength for looks."),
            ("Esthetics", "E.max has more natural translucency and is easier to characterize, which is why it's the go-to for veneers and anterior crowns. Modern multilayer zirconia closes much of the gap, and we <a href=\"/digital-shade-matching/\">measure shade digitally</a> for both."),
            ("Prep and reduction", "Monolithic zirconia tolerates thinner walls, so it's forgiving when you can't take more tooth. E.max generally needs more reduction to reach its strength. If the Rx leaves us short on room, we call before we mill."),
            ("Cementation", "E.max is etched and bonded, which adds strength and suits thin or less retentive preps. Zirconia can be cemented conventionally when the prep is retentive, or bonded with an MDP-containing resin cement."),
            ("Price and turnaround at DentX", "Zirconia crown $75, E.max crown $85, layered zirconia or E.max $99. Up to 5 business days in the lab (6 for layered). Full list: <a href=\"/dental-lab-price-list/\">price list</a>."),
        ],
        faq=[("Is zirconia stronger than E.max?", "Yes. Conventional monolithic zirconia is considerably stronger than lithium disilicate, which is why it's preferred for molars and bruxers."),
             ("Which looks more natural, zirconia or E.max?", "E.max has more natural translucency and is the usual choice for anterior esthetics. Layered and multilayer zirconia narrow the gap."),
             ("How much do zirconia and E.max crowns cost at DentX?", "Zirconia $75, E.max $85, layered zirconia or E.max $99.")]),
    "/guides/monolithic-vs-layered-zirconia/": dict(
        group="guides", nav="Monolithic vs layered zirconia", kind="guide",
        title="Monolithic vs Layered Zirconia Crowns | DentX Dental Lab",
        desc="Monolithic zirconia ($75) for strength, layered zirconia ($99) for anterior esthetics. How a dental lab decides, chipping risk, and turnaround.",
        h1="Monolithic vs<br><em>layered zirconia.</em>",
        lead="Same core material, two different finishes. One is built for strength, the other for the smile line.",
        cats=["ceramic"], img="bench-ceramic.webp", img_alt="Porcelain being layered on a zirconia crown at DentX",
        body=[
            ("Monolithic zirconia", "One solid piece, stained and glazed. No porcelain layer to chip, so it's the safe choice for molars, bruxers and tight interarch space. $75, 5 business days."),
            ("Layered zirconia", "A zirconia core with porcelain layered over the facial and incisal areas for depth and translucency. Best for anteriors where the patient will look closely. $99, 6 business days."),
            ("Chipping risk", "The porcelain layer is the weak point of layered work. Keep it out of heavy function, and consider a <a href=\"/night-guards/\">night guard</a> for grinders."),
            ("Our recommendation", "Monolithic behind the canines, layered or <a href=\"/emax-crowns-veneers/\">E.max</a> in the esthetic zone. Not sure? Send the case and a note; we'll call. See also <a href=\"/guides/zirconia-vs-emax/\">zirconia vs E.max</a>."),
        ],
        faq=[("What is the difference between monolithic and layered zirconia?", "Monolithic zirconia is one solid piece, stained and glazed. Layered zirconia adds porcelain over a zirconia core for better anterior esthetics."),
             ("Does layered zirconia chip?", "The porcelain layer can chip under heavy load, which is why monolithic zirconia is preferred for molars and bruxers.")]),
    "/guides/how-to-send-a-case-to-a-dental-lab/": dict(
        group="guides", nav="How to send a case", kind="guide",
        title="How to Send a Case to a Dental Lab | DentX",
        desc="Step-by-step: send a digital scan or impressions to a dental lab, what to include, how pickup and shipping work, and how turnaround is counted.",
        h1="How to send a case<br><em>to a dental lab.</em>",
        lead="Whether you scan or take impressions, the steps are the same: get the records right, fill out the Rx, and get it to the lab.",
        cats=[], img=None, img_alt="",
        body=[
            ("1. Digital: send from your scanner", "From Medit, iTero, Shining 3D or DEXIS, choose DentX as the lab and send. Any other scanner: email STL files. First time? Call <a href=\"tel:+18186870085\">(818) 687-0085</a> and we'll connect your account. More on <a href=\"/digital-dental-lab/\">digital cases</a>."),
            ("2. Impressions: pack and label", "Disinfect, bag and box the impressions or models with the bite and the Rx. In LA County, call or text before 12 pm for a free pickup. Outside LA County, ask for a prepaid label; we email it and bill it at the carrier's cost."),
            ("3. Fill out the Rx completely", "Service, tooth numbers, shade (and stump shade for E.max), due date, doctor and license number. Use the <a href=\"/assets/dentx-lab-slip.pdf\">DentX lab slip</a>. Incomplete Rx = we call first, and the clock starts once it's complete. See the <a href=\"/guides/dental-lab-rx-checklist/\">Rx checklist</a>."),
            ("4. Schedule the seat", "Crowns and veneers are up to 5 business days in the lab from arrival. Add shipping time outside LA County. <a href=\"/guides/dental-lab-turnaround-times/\">How to count turnaround</a>."),
            ("5. Get it back", "LA County: our driver delivers free. Everywhere else: it ships back for $7 per case."),
        ],
        faq=[("How do I send a digital case to DentX?", "Send from Medit, iTero, Shining 3D or DEXIS IOS Cloud, or email STL files with the Rx. Call (818) 687-0085 the first time to connect."),
             ("How do I ship impressions to DentX?", "Outside LA County, ask for a prepaid label; we email it and bill it at the carrier's cost. In LA County our driver picks up for free.")]),
    "/guides/dental-lab-rx-checklist/": dict(
        group="guides", nav="Rx checklist", kind="guide",
        title="Dental Lab Rx Checklist: What to Include | DentX",
        desc="What to put on a dental lab prescription so the case starts on time: service, teeth, shade, stump shade, due date, license. Free printable DentX lab slip.",
        h1="The dental lab<br><em>Rx checklist.</em>",
        lead="Most delays start with a missing line on the Rx. Here's everything we need, in the order we read it.",
        cats=[], img=None, img_alt="",
        body=[
            ("Doctor and office", "Doctor name, office phone and address, signature and license number."),
            ("Patient", "Name or case ID, and the due date with AM or PM if the seat is tight."),
            ("Service and teeth", "What you want (zirconia, E.max, layered, implant crown, denture stage…) and the tooth numbers. For implants: system, platform and screw or cement retained."),
            ("Shade", "Shade and, for E.max and other translucent work, the stump shade. Photos with a shade tab in frame help. We <a href=\"/digital-shade-matching/\">measure shade digitally</a> when the patient can come in."),
            ("Records", "Prep and opposing scans or impressions, bite registration, and anything special: contacts, occlusion, margins, embrasures."),
            ("Print the lab slip", "Use the <a href=\"/assets/dentx-lab-slip.pdf\">DentX lab slip (PDF)</a>. Send it in the box with impressions, or snap a photo and text it with a scan to <a href=\"sms:+18186870085\">(818) 687-0085</a>."),
        ],
        faq=[("What should a dental lab prescription include?", "Doctor and license, patient or case ID, due date, service, tooth numbers, shade and stump shade, records and bite, and any special instructions."),
             ("What happens if the Rx is incomplete?", "We call your office before starting. Turnaround starts once the Rx is complete.")]),
    "/guides/dental-lab-turnaround-times/": dict(
        group="guides", nav="Turnaround times", kind="guide",
        title="Dental Lab Turnaround Times Explained | DentX Dental Lab",
        desc="How dental lab turnaround is counted: business days in the lab from arrival with a complete Rx. Crowns 5 days, layered 6, night guards 3, dentures by stage.",
        h1="Dental lab turnaround<br><em>times, explained.</em>",
        lead="Turnaround is business days in the lab, counted from when the case arrives with a complete Rx. Here's what that means for booking seats.",
        cats=["ceramic", "removable"], img=None, img_alt="",
        body=[
            ("How we count", "Day 0 is the day the case and complete Rx arrive. Weekends don't count. Shipping time outside LA County is on top; in LA County our driver delivers, so there's none."),
            ("Crowns and veneers", "Zirconia, E.max, veneers, inlays and onlays: up to 5 business days. Layered zirconia or E.max: 6. Implant crowns: 5."),
            ("Removable", "Acrylic dentures: bite block 6, teeth try-in 7, final 7. Printed dentures 7. Valplast 6 · 7 · 12. Night guards 3. Repairs and relines 2."),
            ("Booking the seat", "Arrival day + turnaround + shipping (if any), then a day of buffer. Example: a zirconia crown arriving Monday is ready by the following Monday; local delivery is free."),
            ("When it slows down", "Missing Rx details, unclear margins, or a bite that doesn't seat. We call the same day so you don't lose the appointment. See the <a href=\"/guides/dental-lab-rx-checklist/\">Rx checklist</a>."),
        ],
        faq=[("How long does a dental lab take to make a crown?", "At DentX, up to 5 business days in the lab for zirconia and E.max, counted from when the case arrives with a complete Rx."),
             ("Do turnaround times include shipping?", "No. Outside LA County, add shipping time. In LA County our driver delivers for free.")]),
}

PRICES_PAGE = "/dental-lab-price-list/"

# ---------------------------------------------------------------- extra depth for the core pages in build.py
EXTRA_BODY = {
    "/zirconia-crowns/": [
        ("Prep guidelines", "Monolithic zirconia is forgiving: it holds up in thinner sections than lithium disilicate, so it suits short clinical crowns and cases where you can't take more reduction. Give us a clean, continuous margin (chamfer or light shoulder) and a scan or impression that captures it. If clearance is tight, we call before we mill."),
        ("Cementation", "On a retentive prep, zirconia can go in with conventional cement such as resin-modified glass ionomer. On short or tapered preps, air-abrade the intaglio and bond with an MDP-containing resin cement."),
        ("When to choose E.max instead", "In the esthetic zone, where translucency matters more than strength, <a href=\"/emax-crowns-veneers/\">E.max</a> is often the better call. Our <a href=\"/guides/zirconia-vs-emax/\">zirconia vs E.max guide</a> lays out the trade-offs."),
    ],
    "/emax-crowns-veneers/": [
        ("Veneers", "Veneers at $99 in up to 5 business days. Send a full-arch scan or impression, photos with a shade tab in frame, and the stump shade on the Rx. Patients can come to the Tarzana lab for a <a href=\"/digital-shade-matching/\">digital shade appointment</a> on high-esthetic cases."),
        ("Prep and bonding", "E.max reaches its strength when it's etched and bonded, so it works well on thin or less retentive preps. Give it enough reduction for the material and a clear margin. If we see a thin spot on the scan, we flag it before we make the restoration."),
        ("Stump shade matters", "Because E.max is translucent, the color of the prep shows through. Always include the stump shade on the Rx; it's on our <a href=\"/assets/dentx-lab-slip.pdf\">lab slip</a>."),
    ],
    "/implant-crowns/": [
        ("What to send", "Scan body or impression coping, implant system and platform, screw or cement retained, and the shade. For custom abutments, tell us the emergence profile you want."),
        ("Screw vs cement retained", "Screw-retained is retrievable and avoids residual cement around the implant, which is why many offices default to it. Cement-retained can make sense when the access hole would land in an esthetic area."),
        ("Digital implant cases", "Send scan-body scans from Medit, iTero, Shining 3D or DEXIS, or STL by email. See <a href=\"/digital-dental-lab/\">digital cases</a>. Up to 5 business days in the lab from when the case arrives with a complete Rx."),
    ],
    "/dentures-partials/": [
        ("Printed or acrylic", "Printed dentures ($160, 7 business days) come from a digital design, so a lost or broken denture can be reprinted from the file. Conventional acrylic dentures ($180) go through bite block, teeth try-in and final finish: 6 · 7 · 7 business days."),
        ("Valplast and combination", "Valplast flexible partials at $230 (bite block 6, try-in 7, final 12 business days) for patients who don't want metal clasps. Combination metal + Valplast at $250 when you need the rigidity of metal and the look of flexible clasps."),
        ("Stayplates and relines", "Acrylic stayplates $95 per arch (up to 3 units, 4+ units $110) and printed flexible stayplates $85 per arch, both in 4 business days, or 2 with the $50 rush fee. Repairs $60 and soft relines $80 in 2 business days, excluding delivery time."),
    ],
    "/dental-lab-san-fernando-valley/": [
        ("What Valley offices send us", "<a href=\"/zirconia-crowns/\">Zirconia crowns</a> from $75, <a href=\"/emax-crowns-veneers/\">E.max and veneers</a>, <a href=\"/implant-crowns/\">implant crowns</a>, <a href=\"/dentures-partials/\">dentures and partials</a> and <a href=\"/night-guards/\">night guards</a>. Every price is on the <a href=\"/dental-lab-price-list/\">price list</a>."),
        ("Turnaround without shipping", "Up to 5 business days in the lab for crowns, counted from when the case arrives with a complete Rx. In the Valley our driver brings it back, so there's no shipping time to add."),
    ],
    "/dental-lab-los-angeles/": [
        ("Neighborhood pages", "Pickup details for <a href=\"/dental-lab-encino/\">Encino</a>, <a href=\"/dental-lab-woodland-hills/\">Woodland Hills</a>, <a href=\"/dental-lab-sherman-oaks/\">Sherman Oaks</a>, <a href=\"/dental-lab-van-nuys/\">Van Nuys</a>, <a href=\"/dental-lab-burbank/\">Burbank</a> and <a href=\"/dental-lab-glendale/\">Glendale</a>. Every other neighborhood in LA County gets the same free pickup and delivery."),
    ],
    "/digital-shade-matching/": [
        ("Shade photos that help", "Take photos in daylight-balanced light with the shade tab in the same plane as the tooth, plus one with the tab beside the prep for stump shade. Avoid colored walls and lipstick in frame. Text them to <a href=\"sms:+18186870085\">(818) 687-0085</a> with the case."),
    ],
}
