# DentX Dental Lab — public site

Static site, no server code, built for Vercel. Instagram/Google traffic → prices & turnaround → call / text / lead form.

## Edit & build
- All prices, turnaround, shipping terms, FAQs and page copy live in `build.py` (one source → pages, JSON-LD, `llms.txt`, `sitemap.xml`, `robots.txt`).
- `python3 build.py` regenerates everything. Set the real domain first: `SITE_URL=https://yourdomain.com python3 build.py`.
- Styles: `assets/dentx.css` (DentX layer) on top of Codex's `assets/site.css` + `assets/scrollcraft.css`; all three are minified and inlined into each page at build.
- Logo: `tools/logo.py` builds `assets/logo.svg`, `logo-white.svg`, `favicon.svg` as pure vector (Gilda Display + Montserrat outlines, drawn tooth ribbons). Needs fonttools and the two OFL fonts (download path in the script header).
- `tools/og.html` → `assets/og.jpg` (link preview), rendered with headless Chrome.

## Pages
`/` · `/zirconia-crowns/` · `/emax-crowns-veneers/` · `/implant-crowns/` · `/dentures-partials/` · `/nationwide-dental-lab/` · `/dental-lab-los-angeles/` · `/dental-lab-san-fernando-valley/` · `/digital-shade-matching/` · `/about/` · `/send-a-case/` (11 pages, all in `sitemap.xml`). `.vercelignore` keeps `README.md`, `build.py` and `tools/` out of the deployment.

## Lead form
No server, no API. On submit the form builds the request and opens Messages (SMS to (818) 687-0085), with an email button as the alternative. Nothing is stored by the website. Vercel Web Analytics counts calls/texts/emails/leads/Quick help steps as events.

## Quick help
Button-driven guide in `assets/site.js`, fed by `guide_data()` in `build.py` (prices, delivery terms, hours). No external services.

## Deploy
Push this folder as the repo root → import in Vercel (framework preset "Other", no build command, output = root).

## Verified 2026-10-01
Lighthouse (mobile, compressed local server): home 100/100/100/100; inner pages 99–100 performance, 100 accessibility, best practices, SEO. Phone layout checked at 375px, no horizontal scroll.

## Provenance
- Layout and hero bridge/shade images from the Codex build (`~/Desktop/SkollVoice/builds/dentx`).
- Bench photos generated on Higgsfield 2026-10-01 (originals in `../generated/`).
- Prices/turnaround from the lab's sheets in `../`; shipping terms from competitor research 2026-10-01 (see `../marketing/GROWTH_PLAN.md`).

## Owner to confirm
Domain (then `SITE_URL=https://yourdomain.com python3 build.py`); Instagram handle; Meta Pixel ID; real case photos.
