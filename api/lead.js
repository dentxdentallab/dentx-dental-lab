// Vercel serverless function: new-office lead -> SMS + email to the lab owner, confirmation email to the office.
// Env (set in Vercel): RESEND_API_KEY, LEAD_FROM_EMAIL (verified sender), LEAD_TO_EMAIL,
//                      TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM, OWNER_SMS_TO
// Each channel is optional; the request succeeds if at least one notification to the owner went out.

const clean = (v, n = 300) => String(v ?? '').replace(/[\r\n]+/g, ' ').trim().slice(0, n);

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'POST only' });
  const b = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {});
  if (b.company_site) return res.status(200).json({ ok: true }); // honeypot: silently drop bots

  const lead = {
    practice: clean(b.practice, 120), name: clean(b.name, 120), phone: clean(b.phone, 40),
    email: clean(b.email, 160), location: clean(b.location, 120), need: clean(b.need, 80),
    message: clean(b.message, 1000), page: clean(b.page, 120), utm: clean(b.utm, 200),
  };
  if (!lead.practice || !lead.name || !/\d{7,}/.test(lead.phone.replace(/\D/g, '')))
    return res.status(400).json({ error: 'Practice, name and a valid phone are required.' });
  if (lead.email && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(lead.email)) lead.email = '';

  const summary = `New DentX lead: ${lead.practice} (${lead.name}) ${lead.phone}${lead.location ? ', ' + lead.location : ''}. Wants: ${lead.need}.`;
  const env = process.env, sent = [];

  if (env.TWILIO_ACCOUNT_SID && env.TWILIO_AUTH_TOKEN && env.TWILIO_FROM && env.OWNER_SMS_TO) {
    const r = await fetch(`https://api.twilio.com/2010-04-01/Accounts/${env.TWILIO_ACCOUNT_SID}/Messages.json`, {
      method: 'POST',
      headers: { authorization: 'Basic ' + Buffer.from(`${env.TWILIO_ACCOUNT_SID}:${env.TWILIO_AUTH_TOKEN}`).toString('base64'),
                 'content-type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ From: env.TWILIO_FROM, To: env.OWNER_SMS_TO, Body: summary.slice(0, 600) }),
    }).catch(() => null);
    if (r?.ok) sent.push('sms');
  }

  if (env.RESEND_API_KEY && env.LEAD_FROM_EMAIL && env.LEAD_TO_EMAIL) {
    const mail = (to, subject, text, reply_to) => fetch('https://api.resend.com/emails', {
      method: 'POST', headers: { authorization: `Bearer ${env.RESEND_API_KEY}`, 'content-type': 'application/json' },
      body: JSON.stringify({ from: env.LEAD_FROM_EMAIL, to, subject, text, ...(reply_to ? { reply_to } : {}) }),
    }).catch(() => null);
    const body = Object.entries(lead).filter(([, v]) => v).map(([k, v]) => `${k}: ${v}`).join('\n');
    const r = await mail(env.LEAD_TO_EMAIL, `New case request: ${lead.practice}`, body, lead.email || undefined);
    if (r?.ok) sent.push('email');
    if (lead.email) await mail(lead.email, 'DentX Dental Lab received your request',
      `Hi ${lead.name},\n\nThanks for reaching out to DentX Dental Lab. We'll call you at ${lead.phone} today to get your first case started.\n\nZirconia & E.max crowns: 5 business days in the lab. Digital cases ship back free by FedEx 2Day.\nPrices and turnaround: https://${req.headers.host}/#prices\n\nDentX Dental Lab · (818) 687-0085 · 18401 Burbank Blvd #110, Tarzana, CA 91356`);
  }

  if (!sent.length) return res.status(503).json({ error: 'Lead delivery is not configured.' });
  return res.status(200).json({ ok: true, sent });
}
