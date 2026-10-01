// DentX site behaviour: Codex hero motion, lead form, contact-click tracking.
const $ = s => document.querySelector(s);
addEventListener('DOMContentLoaded', () => { if (window.ScrollCraft && $('[data-sc-act]')) ScrollCraft.mount(document.body); });

// Hero bridge parallax (from the Codex build), skipped for reduced motion.
const hero = $('.hero'), product = $('.hero-product');
if (hero && product && !matchMedia('(prefers-reduced-motion:reduce)').matches) {
  let px = 0, py = 0, queued = false;
  const draw = () => {
    queued = false;
    const r = hero.getBoundingClientRect();
    if (r.bottom > 0) product.style.transform = `translateY(${-Math.max(0, -r.top) * .1}px) rotateX(${py * -5}deg) rotateY(${px * 7}deg)`;
  };
  const tick = () => { if (!queued) { queued = true; requestAnimationFrame(draw); } };
  addEventListener('scroll', tick, { passive: true });
  hero.addEventListener('pointermove', e => { if (e.pointerType === 'mouse') { const r = hero.getBoundingClientRect(); px = (e.clientX / r.width - .5) * 2; py = ((e.clientY - r.top) / r.height - .5) * 2; tick(); } });
  hero.addEventListener('pointerleave', () => { px = py = 0; tick(); });
}

// Analytics: Vercel Web Analytics on the live site only; contact clicks become events.
const live = !/^(localhost|127\.|0\.0\.0\.0)/.test(location.hostname);
if (live) {
  window.va = window.va || function () { (window.vaq = window.vaq || []).push(arguments); };
  const s = document.createElement('script'); s.defer = true; s.src = '/_vercel/insights/script.js'; document.head.append(s);
}
const track = (name, data) => { try { window.va && window.va('event', { name, data }); } catch {} };
document.addEventListener('click', e => { const a = e.target.closest('[data-ev]'); if (a) track(a.dataset.ev, { page: location.pathname }); });

// Lead form: no server. Builds the request and hands it to the phone's Messages app (SMS to the lab),
// with email as the alternative on computers. Nothing is stored by the website.
document.querySelectorAll('.lead-form').forEach(form => {
  const status = form.querySelector('.form-status');
  const tel = (window.DX && window.DX.tel) || '+18186870085';
  form.addEventListener('submit', e => {
    e.preventDefault();
    if (!form.reportValidity()) return;
    const d = Object.fromEntries(new FormData(form));
    if (d.company_site) return;
    const msg = [`New case request (website)`, `Practice: ${d.practice}`, `Name: ${d.name}`, `Phone: ${d.phone}`,
      d.email && `Email: ${d.email}`, d.location && `Location: ${d.location}`, `Wants: ${d.need}`, d.message && `Notes: ${d.message}`].filter(Boolean).join('\n');
    const sep = /iPhone|iPad|Mac/.test(navigator.userAgent) ? '&' : '?';
    const smsHref = `sms:${tel}${sep}body=${encodeURIComponent(msg)}`;
    const mailHref = `mailto:Dentxdentallab@yahoo.com?subject=${encodeURIComponent('New case request: ' + d.practice)}&body=${encodeURIComponent(msg)}`;
    track('lead', { need: d.need });
    status.replaceChildren('Your request is ready. Send it to the lab: ');
    const a1 = Object.assign(document.createElement('a'), { href: smsHref, className: 'btn btn-gold', textContent: 'Send by text' });
    const a2 = Object.assign(document.createElement('a'), { href: mailHref, className: 'btn btn-ghost', textContent: 'Send by email' });
    a1.dataset.ev = 'text'; a2.dataset.ev = 'email';
    status.append(a1, ' ', a2);
    if (matchMedia('(pointer:coarse)').matches) location.href = smsHref; // phones: open Messages right away
  });
});

// Lazy-load the walkthrough video only when it scrolls into view (keeps first load fast).
document.querySelectorAll('.lazy-video').forEach(v => {
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (!e.isIntersecting) { v.pause(); return; }
    const s = v.querySelector('source[data-src]');
    if (s) { s.src = s.dataset.src; s.removeAttribute('data-src'); v.load(); }
    if (!matchMedia('(prefers-reduced-motion:reduce)').matches) v.play().catch(() => {});
  }), { rootMargin: '200px' });
  io.observe(v);
});

// Quick help: a scripted, button-driven guide. Runs entirely in the browser, no external services, no AI claims.
(() => {
  const D = window.DX; if (!D) return;
  const el = (t, a = {}, ...kids) => { const e = document.createElement(t); Object.entries(a).forEach(([k, v]) => k === 'class' ? e.className = v : e.setAttribute(k, v)); kids.flat().forEach(c => e.append(c)); return e; };
  const sms = body => `sms:${D.tel}${/iPhone|iPad|Mac/.test(navigator.userAgent) ? '&' : '?'}body=${encodeURIComponent(body)}`;
  const openNow = () => { const t = new Date(new Date().toLocaleString('en-US', { timeZone: 'America/Los_Angeles' })); const d = t.getDay(), h = t.getHours(); return d >= 1 && d <= 5 && h >= 9 && h < 18; };
  const call = el('a', { class: 'qh-act gold', href: `tel:${D.tel}`, 'data-ev': 'call' }, `Call ${D.phone}`);
  const actions = (...xs) => el('div', { class: 'qh-acts' }, ...xs);
  const txt = (label, body) => el('a', { class: 'qh-act', href: sms(body), 'data-ev': 'text' }, label);
  const link = (label, href) => el('a', { class: 'qh-act', href }, label);
  const ship = Object.fromEntries(D.ship.map(([k, v]) => [k, v]));

  const nodes = {
    root: () => ({ say: 'What can we help with?', opts: [['Prices', 'prices'], ['Turnaround', 'turn'], ['Pickup & shipping', 'ship'], ['Send my first case', 'first'], ['Scanners we accept', 'scan'], ['Talk to Haibert', 'talk']] }),
    prices: () => ({ say: 'Which work?', opts: D.cats.map(c => [c.label, 'cat:' + c.key]) }),
    turn: () => ({ say: 'Up to 5 business days in the lab, counted from when your case arrives with a complete Rx. Dentures and partials go by stage (bite block, try-in, finish). Shipping time outside LA County is on top.', end: actions(link('Full turnaround list', '/#prices'), call) }),
    ship: () => ({ say: 'Where is your office?', opts: [['Los Angeles County', 'la'], ['Outside LA County', 'out']] }),
    la: () => ({ say: ship['Los Angeles County'], end: actions(txt('Text a pickup request', 'Hi DentX, pickup request.\nOffice:\nAddress:\nNumber of cases:'), call) }),
    out: () => ({ say: 'Sending a scan or physical impressions?', opts: [['Digital scan', 'outd'], ['Impressions / models', 'outi']] }),
    outd: () => ({ say: ship['Outside LA County, digital'], end: actions(link('Send a case', '/send-a-case/#start'), call) }),
    outi: () => ({ say: ship['Outside LA County, impressions'], end: actions(txt('Text for a label', 'Hi DentX, please email a prepaid shipping label.\nOffice:\nAddress:\nEmail:'), link('Request by form', '/send-a-case/#start')) }),
    first: () => ({ say: '1. Scan (Medit, iTero, Shining 3D, DEXIS) or take impressions.  2. Fill the Rx: service, teeth, shade, due date.  3. LA County: we pick up free. Elsewhere: send the scan, or we email a label.  4. Up to 5 business days in the lab.', end: actions(link('Start my first case', '/send-a-case/#start'), call) }),
    scan: () => ({ say: `We receive from ${D.scanners.join(', ')}. Call and we'll walk you through connecting your scanner account.`, end: actions(call) }),
    talk: () => ({ say: `${openNow() ? 'The lab is open now.' : 'The lab is closed right now.'} Hours: ${D.hours} (Pacific). ${openNow() ? 'Call or text, Haibert or the team will answer.' : 'Text or email and we\'ll get back to you first thing.'}`, end: actions(call, txt('Text the lab', 'Hi DentX, '), link('Email', `mailto:${D.email}`)) }),
  };
  D.cats.forEach(c => nodes['cat:' + c.key] = () => ({
    say: c.label, list: c.rows.map(([n, d, p]) => `${n}${d ? ' · ' + d + ' days' : ''} · ${p}`),
    end: actions(link('Full price list', '/#prices'), call) }));

  const btn = el('button', { class: 'qh-launch', type: 'button', 'aria-expanded': 'false', 'aria-controls': 'qh-panel' }, 'Quick help');
  const body = el('div', { class: 'qh-body', 'aria-live': 'polite' });
  const panel = el('div', { class: 'qh-panel', id: 'qh-panel', role: 'dialog', 'aria-label': 'Quick help', hidden: '' },
    el('div', { class: 'qh-head' }, el('strong', {}, 'DentX quick help'), el('button', { class: 'qh-x', type: 'button', 'aria-label': 'Close' }, '×')), body,
    el('p', { class: 'qh-foot' }, 'Answers come from the lab\'s published prices and policies.'));
  const history = [];
  const show = (id, push = true) => {
    if (push) history.push(id);
    const n = nodes[id](); body.replaceChildren(el('p', { class: 'qh-say' }, n.say));
    if (n.list) body.append(el('ul', { class: 'qh-list' }, n.list.map(t => el('li', {}, t))));
    if (n.opts) body.append(el('div', { class: 'qh-opts' }, n.opts.map(([l, k]) => { const b = el('button', { type: 'button', class: 'qh-opt' }, l); b.onclick = () => show(k); return b; })));
    if (n.end) body.append(n.end);
    if (history.length > 1) { const b = el('button', { type: 'button', class: 'qh-back' }, '← Back'); b.onclick = () => { history.pop(); show(history[history.length - 1], false); }; body.append(b); }
    (body.querySelector('button, a') || body).focus?.();
    try { window.va && window.va('event', { name: 'quick_help', data: { step: id } }); } catch {}
  };
  const toggle = open => { panel.hidden = !open; btn.setAttribute('aria-expanded', String(open)); if (open) { history.length = 0; show('root'); } else btn.focus(); };
  btn.onclick = () => toggle(panel.hidden);
  panel.querySelector('.qh-x').onclick = () => toggle(false);
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && !panel.hidden) toggle(false); });
  document.body.append(btn, panel);
})();

// Sound toggle for the lab film (autoplay must start muted).
document.querySelectorAll('.film .sound').forEach(b => b.addEventListener('click', () => {
  const v = b.parentElement.querySelector('video'); v.muted = !v.muted;
  b.setAttribute('aria-pressed', String(!v.muted)); b.textContent = v.muted ? 'Sound on' : 'Sound off';
  if (!v.muted) v.play().catch(() => {});
}));
