# DentX Dental Lab — public site

Static site + one serverless function, built for Vercel. Instagram/Google traffic → prices & turnaround → call / text / lead form.

## Edit & build
- All prices, turnaround, shipping terms, FAQs and page copy live in `build.py` (one source → pages, JSON-LD, `llms.txt`, `sitemap.xml`, `robots.txt`).
- `python3 build.py` regenerates everything. Set the real domain first: `SITE_URL=https://yourdomain.com python3 build.py`.
- Styles: `assets/dentx.css` (DentX layer) on top of Codex's `assets/site.css` + `assets/scrollcraft.css`; all three are minified and inlined into each page at build.
- Logo: `tools/logo.py` builds `assets/logo.svg`, `logo-white.svg`, `favicon.svg` as pure vector (Gilda Display + Montserrat outlines, drawn tooth ribbons). Needs fonttools and the two OFL fonts (download path in the script header).
- `tools/og.html` → `assets/og.jpg` (link preview), rendered with headless Chrome.

## Pages
`/` · `/zirconia-crowns/` · `/emax-crowns-veneers/` · `/implant-crowns/` · `/dentures-partials/` · `/nationwide-dental-lab/` · `/send-a-case/`

## Lead form (`api/lead.js`)
Without env vars the form falls back to opening a prefilled email. Set in Vercel → Settings → Environment Variables:
- SMS to owner: `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_FROM`, `OWNER_SMS_TO`
- Email to owner + auto-reply to the office: `RESEND_API_KEY`, `LEAD_FROM_EMAIL` (verified domain sender), `LEAD_TO_EMAIL`
Turn on Vercel Web Analytics; calls/texts/emails/leads are tracked as events.

## Deploy
Push this folder as the repo root → import in Vercel (framework preset "Other", no build command, output = root).

## Verified 2026-10-01
Lighthouse (mobile, compressed local server): home 100/100/100/100; inner pages 99–100 performance, 100 accessibility, best practices, SEO. Phone layout checked at 375px, no horizontal scroll.

## Provenance
- Layout and hero bridge/shade images from the Codex build (`~/Desktop/SkollVoice/builds/dentx`).
- Bench photos generated on Higgsfield 2026-10-01 (originals in `../generated/`).
- Prices/turnaround from the lab's sheets in `../`; shipping terms from competitor research 2026-10-01 (see `../marketing/GROWTH_PLAN.md`).

## Owner to confirm
Domain; margin on free FedEx 2Day return for single $75 crowns; whether (818) 687-0085 receives texts; hours; Instagram handle; Meta Pixel ID; real case photos.
