"""build_site.py: write index.html from films.json (the film list and all copy) and _head.html (fonts + the look's stylesheet).
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
"""
head = head.replace('</style>', extra + '</style>')
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
nav = ''.join(f'<a href="#{s["id"]}">{e(s["title"])}</a>' for s in d['sections'])
body = f"""<body>
<div class="sheet">
<header class="top"><a class="mark cond" href="#">SOLUS FX</a><nav class="nav" aria-label="Main">{nav}<a href="#process">Process</a><a href="#contact" class="cta">Contact</a></nav></header>
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
<section class="contact" id="contact"><div><p class="cond">Contact</p><p class="sub">For quotes and availability, email Jordan at {e(d['email'])}.</p></div><a class="btn big on-red" href="mailto:{e(d['email'])}">Email Jordan</a></section>
</main>
<footer class="foot mono"><span>Solus FX</span><span>United Kingdom, 2026</span></footer>
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
