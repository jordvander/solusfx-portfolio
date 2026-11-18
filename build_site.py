"""build_site.py: write index.html, terms.html and thanks.html from films.json (the film list, business details and all copy) and _head.html (fonts + the look's stylesheet).
Add a film: encode it (encode.sh), put a thumbnail in thumbs/, add a row to films.json, run this again."""
import json, html, pathlib
D = pathlib.Path(__file__).parent; d = json.load(open(D / 'films.json')); e = html.escape
head = (D / '_head.html').read_text().replace('<title>Solus FX. Animation that explains what you do.</title>', '<title>Solus FX. Animated explainers, sports and product films.</title>')
extra = """
.tile,.film{cursor:pointer;text-align:left;font:inherit;color:inherit}
button.tile{border-left:0;border-top:0;border-radius:0;appearance:none}
button.film{padding:0;border-radius:0;appearance:none}
.note p.plain{font:500 clamp(16px,1.25vw,19px)/1.4 var(--disp);font-stretch:100%;text-transform:none;letter-spacing:0;max-width:30em}
h1{font-size:clamp(50px,8vw,118px)}
.contact p.sub{font:500 clamp(17px,1.5vw,22px)/1.4 var(--disp);font-stretch:100%;text-transform:none;letter-spacing:0;margin-top:18px;max-width:26em}
.lb{position:fixed;inset:0;background:rgba(21,19,15,.92);display:none;align-items:center;justify-content:center;z-index:50;padding:16px}
.lb.on{display:flex}
.lb video{max-width:min(100%,1280px);max-height:calc(100vh - 90px);border:1.5px solid var(--paper);background:#000}
.lb .x{position:absolute;top:14px;right:16px;font:500 13px/1 var(--mono);letter-spacing:.04em;text-transform:uppercase;color:var(--paper);background:none;border:1.5px solid var(--paper);padding:10px 14px;cursor:pointer}
.lb .t{position:absolute;left:16px;top:20px;color:var(--paper)}
@media (max-width:980px){.grid>.note{grid-column:1/-1!important;border-right:0!important}}
.price{display:grid;grid-template-columns:repeat(3,minmax(0,1fr))}
.price>div{border-right:var(--rule);border-bottom:var(--rule);padding:clamp(14px,1.6vw,24px);background:var(--cell);display:flex;flex-direction:column;justify-content:space-between;gap:22px;min-height:clamp(170px,15vw,230px)}
.price>div:last-child{border-right:0}
.price b{font-size:clamp(34px,3.7vw,56px);line-height:.86}
.price p{margin:0;font-size:15.5px;line-height:1.45;max-width:24em;color:#b3ad9f}
.price a,.doc a,.foot a,.cform .alt a{text-decoration:underline;text-underline-offset:3px}
.contact{align-items:start}
.cform{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:12px;width:min(100%,580px)}
.cform label{display:flex;flex-direction:column;gap:7px;font:500 11.5px/1 var(--mono);letter-spacing:.04em;text-transform:uppercase;color:#07080d}
.cform .full,.cform button,.cform .alt{grid-column:1/-1}
.cform input,.cform select,.cform textarea{font:500 16px/1.3 var(--disp);color:var(--ink);background:#07080d;border:1.5px solid #07080d;border-radius:0;padding:13px 12px;width:100%}
.cform textarea{min-height:130px;resize:vertical}
.cform input:focus,.cform select:focus,.cform textarea:focus{outline:2px solid #07080d;outline-offset:2px}
.cform .hp{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}
.cform button{justify-content:center;cursor:pointer}
.contact .cform .alt{font:500 14.5px/1.4 var(--disp);font-stretch:100%;text-transform:none;letter-spacing:0;max-width:none;margin:2px 0 0}
.foot{flex-wrap:wrap;line-height:1.5}
.foot .addr{text-transform:none;letter-spacing:.01em}
.doc{padding:clamp(20px,3vw,44px) clamp(14px,1.9vw,28px) clamp(40px,5vw,72px)}
.doc>*{max-width:44em}
.doc h3{font-size:clamp(26px,2.6vw,36px);line-height:.95;margin:38px 0 10px}
.doc h3:first-child{margin-top:0}
.doc p,.doc li{font-size:16.5px;line-height:1.55;color:#cfc8b8;margin:0 0 10px}
.doc ul{padding-left:1.2em;margin:0 0 10px}
@media (max-width:980px){.price{grid-template-columns:minmax(0,1fr)}.price>div{border-right:0;min-height:0}}
@media (max-width:640px){.cform{grid-template-columns:minmax(0,1fr)}}
"""
head = head.replace('</style>', extra + (D / 'brand.css').read_text() + '</style>').replace('<meta name="viewport"', '<meta name="theme-color" content="#07080d"><meta name="viewport"')
MARK = '''<svg class="ecl" viewBox="0 0 100 100" aria-hidden="true"><circle cx="50" cy="50" r="44" fill="none" stroke="#efe6d2" stroke-width="2.6"/><circle cx="61" cy="55" r="27" fill="none" stroke="#efe6d2" stroke-width="2.6"/><path d="M52.3 6.06A44 44 0 0 1 82.5 20.3" fill="none" stroke="#f0652f" stroke-width="3"/><path d="M93.6 55.4A44 44 0 0 1 92.6 61" fill="none" stroke="#f0652f" stroke-width="3"/></svg>'''
films = {f['slug']: f for s in d['sections'] for f in s['films']}; hero = films[d['hero']]
def tile(f, code, i, cls=''):
    wide = f.get('wide'); c = 'cell tile ' + ('feature ' if f.get('feature') else '') + ('w3 ' if wide else '') + cls
    tag = '<span class="tag">Featured</span>' if f.get('feature') else ''
    return (f'<button class="{c.strip()}" data-v="{f["slug"]}" data-w="{1 if wide else 0}" data-t="{e(f["title"])}" aria-label="Play {e(f["title"])}">'
            f'<span class="ph{" wide" if wide else ""}"><img src="thumbs/{f["thumb"]}" alt="Frame from {e(f["title"])}" loading="lazy">{tag}</span>'
            f'<span class="mono"><span>{code}/{i:02d}</span><span>{f["dur"]} / {"16:9" if wide else "9:16"}</span></span>'
            f'<b class="cond">{e(f["title"])}</b><span class="d">{e(f["desc"])}</span></button>')
def section(n, s):
    fs = s['films']; cells = []; used = 0
    for i, f in enumerate(fs, 1): cells.append(tile(f, s['code'], i)); used += 4 if f.get('feature') else 3 if f.get('wide') else 1
    feat = any(f.get('feature') for f in fs)
    rem = (10 - used) if feat and used < 10 else (5 - used % 5) % 5          # a feature fills a 2 x 2 block of the five columns
    if feat and used < 10 and rem > 3: rem = rem - 3 if rem > 3 else rem
    if rem == 0: rem = 5
    span = f' style="grid-column:span {min(rem, 5)}"'
    cells.append(f'<div class="cell note last r0 keep"{span}><p class="plain">{e(s["note"])}</p><span class="go"><span>{len(fs)} film{"s" if len(fs) != 1 else ""}</span><span>{e(s["title"])}</span></span></div>')
    return (f'<section id="{s["id"]}"><div class="bar"><span class="mono">{n:02d}</span><h2 class="cond">{e(s["title"])}</h2><span class="mono">{len(fs)} film{"s" if len(fs) != 1 else ""}</span></div>'
            f'<div class="grid">{"".join(cells)}</div></section>')
steps = [('Brief', 'You send the subject, the audience and where the film will be shown.'), ('Script', 'I write the script. You approve it before any design starts.'),
         ('Style frame', 'You see one finished frame and approve the look.'), ('Film', 'The finished film with voice-over, captions and sound, in the sizes you need.')]
b = d['business']
def top(pre=''):  # pre='index.html' on the other pages so the section links go back to the home page
    nav = ''.join(f'<a href="{pre}#{s["id"]}">{e(s["title"])}</a>' for s in d['sections'])
    return (f'<header class="top"><a class="mark cond" href="{pre or "#"}">{MARK}<span>SOLUS FX</span></a><nav class="nav" aria-label="Main">{nav}'
            f'<a href="{pre}#pricing">Pricing</a><a href="{pre}#contact" class="cta">Contact</a></nav></header>')
FOOT = (f'<footer class="foot mono"><span class="addr">{e(b["legal"])} {e(b["address"])}. {e(d["email"])}</span>'
        f'<span><a href="terms.html">Terms and refunds</a></span></footer>')
FORM = f"""<form class="cform" action="{e(b['form_action'])}" method="POST">
<input type="hidden" name="_subject" value="New Solus FX enquiry"><input type="hidden" name="_next" value="{e(b['site'])}/thanks.html"><input type="hidden" name="_template" value="table"><input type="hidden" name="_captcha" value="false">
<label class="hp" aria-hidden="true">Leave empty<input type="text" name="_honey" tabindex="-1" autocomplete="off"></label>
<label>Name<input name="name" required autocomplete="name"></label>
<label>Email<input type="email" name="email" required autocomplete="email"></label>
<label>Company<input name="company" autocomplete="organization"></label>
<label>Film type<select name="film_type"><option>Explainer</option><option>Sports</option><option>Product film</option><option>Something else</option></select></label>
<label class="full">About the project<textarea name="message" required placeholder="Subject, audience, where it will be shown, and when you need it."></textarea></label>
<button class="btn big on-red" type="submit">Send enquiry</button>
<p class="alt">Or email <a href="mailto:{e(d['email'])}">{e(d['email'])}</a>. Booking follows the <a href="terms.html">terms and refund policy</a>.</p>
</form>"""
body = f"""<body>
<div class="sheet">
{top()}
<main>
<section class="hero">
<div class="hero-l">
<p class="mono" style="margin:0"><span>Animation studio. United Kingdom.</span><span>Explainers / Sports / Product films</span></p>
<h1 class="cond">Explainers.<br>Sports.<br>Product films.</h1>
<div class="hero-b"><p class="lede">Solus FX makes short animated films for software, finance and technology companies, sports media and agencies. Run by Jordan, based in the UK.</p>
<div class="actions"><a class="btn" href="#work">View work</a><a class="btn alt" href="#contact">Contact</a></div></div>
</div>
<div class="hero-r"><button class="film" data-v="{hero['slug']}" data-w="0" data-t="{e(hero['title'])}" aria-label="Play {e(hero['title'])}"><img src="thumbs/{d.get('hero_thumb', hero['thumb'])}" alt="Frame from {e(hero['title'])}"><span class="play" aria-hidden="true"><svg viewBox="0 0 18 18"><path d="M3 1.5v15l13-7.5z" fill="#15130f"/></svg></span></button>
<p class="mono" style="margin:0"><span>{e(hero['title'])}</span><span>{hero['dur']}</span></p></div>
</section>
<div id="work">{''.join(section(i, s) for i, s in enumerate(d['sections'], 1))}</div>
<section id="process"><div class="bar"><span class="mono">{len(d['sections']) + 1:02d}</span><h2 class="cond">Process</h2><span class="mono">Four steps</span></div>
<ol class="steps">{''.join(f'<li><span class="mono"></span><h3 class="cond">{a}</h3><p>{b}</p></li>' for a, b in steps)}</ol></section>
<section id="pricing"><div class="bar"><span class="mono">{len(d['sections']) + 2:02d}</span><h2 class="cond">Pricing</h2><span class="mono">Fixed quotes</span></div>
<div class="price">
<div><b class="cond">From {e(b['price_from'])}</b><p>The price depends on the length of the film, the number of sizes and versions, and whether it needs voice-over. To discuss a different budget, a retainer or ongoing work, <a href="#contact">get in touch</a>.</p></div>
<div><b class="cond">Fixed quote</b><p>You get a fixed price after the brief, before any work starts. It states the length, the sizes, the delivery date and the cost.</p></div>
<div><b class="cond">50% deposit</b><p>A 50% deposit books the project. The balance is due when you approve the finished film. Two rounds of changes are included. See the <a href="terms.html">terms and refund policy</a>.</p></div>
</div></section>
<section class="contact" id="contact"><div><p class="cond">Contact</p><p class="sub">For quotes and availability, send the form. Jordan replies by email.</p></div>{FORM}</section>
</main>
{FOOT}
</div>
<div class="lb" id="lb" role="dialog" aria-modal="true"><span class="t mono" id="lbt"></span><button class="x" id="lbx">Close</button><video id="lbv" controls playsinline preload="none"></video></div>
<script>
const lb = document.getElementById('lb'), v = document.getElementById('lbv'), t = document.getElementById('lbt');
const shut = () => {{ v.pause(); v.removeAttribute('src'); v.load(); lb.classList.remove('on'); }};
document.querySelectorAll('[data-v]').forEach(b => b.addEventListener('click', () => {{ v.src = 'video/' + b.dataset.v + '.mp4'; t.textContent = b.dataset.t; lb.classList.add('on'); v.play().catch(() => {{}}); }}));
document.getElementById('lbx').addEventListener('click', shut); lb.addEventListener('click', e => {{ if (e.target === lb) shut(); }}); addEventListener('keydown', e => {{ if (e.key === 'Escape') shut(); }});
</script>
</body></html>"""
(D / 'index.html').write_text(head + body); print('wrote index.html', len(head + body))

TERMS = [
 ('Who we are', [f'{b["legal"]}', f'Address: {b["address"]}.', f'Email: <a href="mailto:{e(d["email"])}">{e(d["email"])}</a>.']),
 ('Services', ['Solus FX makes short animated films: explainers, sports animation and product films. Each project is agreed in writing, by email, with a fixed quote that states the length of the film, the sizes delivered, the delivery date and the price.']),
 ('Prices', [f'Prices start from {b["price_from"]}. The price depends on the length of the film, the number of sizes and versions, and whether it needs voice-over. Prices are in pounds sterling. Any VAT due is shown on the quote.', f'To discuss a different price, a retainer or ongoing work, email <a href="mailto:{e(d["email"])}">{e(d["email"])}</a> or use the <a href="index.html#contact">contact form</a>.']),
 ('Booking and payment', ['A project is booked when you accept the quote and pay a 50% deposit. The remaining 50% is due when you approve the finished film, before the final files are sent. Payment is by bank transfer or card, as shown on the invoice.']),
 ('Changes', ['Two rounds of changes are included. Further changes, or changes to a script or style you have already approved, are quoted before the work is done.']),
 ('Cancellation and refunds', ['You can cancel a project at any time by email.', '<ul><li>Cancelled before script work starts: the deposit is refunded in full.</li><li>Cancelled after script work starts: the deposit is not refundable. It covers the work already done.</li><li>Cancelled after you approve the finished film: the balance is due.</li><li>If Solus FX cancels a project, any money paid for work not delivered is refunded in full.</li></ul>', 'Refunds go back to the original payment method within 14 days.']),
 ('Delivery and use', ['Films are delivered as digital files by download link. Once the project is paid in full, you can use the film for any purpose. Solus FX may show the film in its portfolio unless you ask it not to before the project starts.']),
 ('Privacy', ['When you send an enquiry, the details you give (name, email, company and message) are used only to reply and to quote. They are not shared or sold. Ask at any time and they will be deleted.']),
 ('Your rights', ['These terms do not affect your statutory rights.']),
]
def page(fname, title, label, inner):
    h = head.replace('<title>Solus FX. Animated explainers, sports and product films.</title>', f'<title>{e(title)}. Solus FX.</title>')
    (D / fname).write_text(h + f"""<body>
<div class="sheet">
{top('index.html')}
<main><section><div class="bar"><span class="mono">{e(label)}</span><h2 class="cond">{e(title)}</h2><span class="mono"></span></div>
<div class="doc">{inner}</div></section></main>
{FOOT}
</div>
</body></html>"""); print('wrote', fname)
page('terms.html', 'Terms and refunds', 'Updated 18 November 2026',
     ''.join(f'<h3 class="cond">{t}</h3>' + ''.join(x if x.startswith('<ul>') else f'<p>{x}</p>' for x in ps) for t, ps in TERMS))
page('thanks.html', 'Thanks', 'Message sent',
     '<p>Your message has been sent. Jordan will reply by email.</p><p><a href="index.html">Back to the films</a></p>')
