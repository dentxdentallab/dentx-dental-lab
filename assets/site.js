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

// Lead form: POST to /api/lead; if the API isn't configured, fall back to a prefilled email.
document.querySelectorAll('.lead-form').forEach(form => {
  const status = form.querySelector('.form-status'), btn = form.querySelector('button');
  form.addEventListener('submit', async e => {
    e.preventDefault();
    if (!form.reportValidity()) return;
    const data = Object.fromEntries(new FormData(form));
    data.page = location.pathname;
    data.utm = location.search.slice(1);
    btn.disabled = true; status.textContent = 'Sending…';
    try {
      const res = await fetch('/api/lead', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(data) });
      if (!res.ok) throw new Error(res.status);
      form.reset(); status.textContent = 'Got it. The lab will call you back today.';
      track('lead', { need: data.need });
    } catch {
      const body = Object.entries(data).filter(([k, v]) => v && k !== 'company_site').map(([k, v]) => `${k}: ${v}`).join('\n');
      location.href = `mailto:Dentxdentallab@yahoo.com?subject=${encodeURIComponent('New case request: ' + data.practice)}&body=${encodeURIComponent(body)}`;
      status.textContent = 'Opening your email app… or call (818) 687-0085.';
    } finally { btn.disabled = false; }
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
