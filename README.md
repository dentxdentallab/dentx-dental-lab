# DentX Dental Lab — public site

Static one-page site for Instagram traffic. Open `index.html` through any static server (e.g. `python3 -m http.server` inside `site/`).

## Provenance
- Design ported from the Codex build at `~/Desktop/SkollVoice/builds/dentx` (thread "Build interactive DentX site", 2026-09-10). Copied unchanged: `assets/site.css`, `assets/scrollcraft.{js,css}`, `assets/{hero,shade,denture,implant}.webp` (AI-generated, illustrative).
- `assets/home.js` = the homepage block of Codex `app.js`; portal/upload/login code dropped (needs the Codex worker backend).
- `assets/logo-{light,dark}.png`, `assets/tooth.png` cut from `../PNG image.PNG` (the real logo).
- Prices and turnaround from `../IMG_2027.jpg`, `../IMG_4196.jpg`, `../77BC0813-…PNG`.
- Overrides live only in `assets/dentx.css`.

## Status
- Done: Codex design, real logo, turnaround & prices ledger, FAQ, LocalBusiness/OfferCatalog/FAQPage JSON-LD, robots.txt, sitemap.xml, llms.txt, og.jpg, tel/mailto CTAs, phone layout checked at 375px.
- Bench photos (`assets/bench-*.webp`) generated on Higgsfield 2026-10-01, originals in `../generated/`. Hero + shade still Codex images.
- Owner to confirm: live domain (replace `www.dentxdentallab.com` in index.html, robots.txt, sitemap.xml, llms.txt); hours; Instagram handle; delivery area; real case photos to replace AI imagery.
- Not here: case portal / file upload / owner ops (Codex build, needs hosting + backend).

## Deploy
Static, no build step. Vercel: import the GitHub repo, framework preset "Other", output directory `/` (repo root = this folder).
