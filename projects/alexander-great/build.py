"""Alexander composition -> hf/index.html + hf/captions.js (times from audio/words.json)."""
import json, re
W = json.load(open('audio/words.json'))
# fix whisper tokenisation
F = []
for w in W:
    t = w['t']
    if F and (t.startswith('-') or t.startswith(',')): F[-1]['t'] += t; F[-1]['e'] = w['e']; continue
    F.append(dict(w))
for w in F:
    w['t'] = w['t'].replace('9,000', '9,000')
    if w['t'] == 'one.' and 32.0 < w['s'] < 33.0: w['t'] = 'won.'   # "all won" (whisper heard "all one")
END = 56.2
LEG = {'wept', 'worlds', 'conquer', 'zeus', 'son', 'tamed', 'horse', 'oracle', 'asia', 'knot', 'cut', 'sword', 'never', 'lost'}
FACT = {'philosopher', 'infinite', 'text', 'lifetime', 'first', 'issus', 'gaugamela', 'hydaspes', 'won', 'plutarch', 'greek', 'roman', 'comedy', 'real'}
key = lambda t: re.sub(r"[^a-z0-9,\-]", "", t.lower()).strip(',')
ch, cur = [], []
for w in F:
    cur.append(w)
    if re.search(r"[.,?!:]$", w['t']) or len(cur) >= 4 or cur[-1]['e'] - cur[0]['s'] > 1.6: ch.append(cur); cur = []
if cur: ch.append(cur)
C = []
for c in ch:
    ws = [{'t': w['t'], 's': w['s'], 'e': w['e'], 'k': ('L' if key(w['t']) in LEG else 'F' if key(w['t']) in FACT else '')} for w in c]
    C.append({'s': c[0]['s'], 'e': c[-1]['e'], 'w': ws})
for i in range(len(C) - 1): C[i]['e'] = min(C[i + 1]['s'] - 0.02, round(C[i]['e'] + 0.45, 2))
C[-1]['e'] = round(min(END - 0.3, C[-1]['e'] + 1.2), 2)
open('hf/captions.js', 'w').write('window.CAPS=' + json.dumps(C) + ';')
P = json.load(open('hf/assets/mappts.json'))
html = open('index.tpl.html').read().replace('{{END}}', str(END))
for k, v in P.items():
    if k == 'route': continue
    x, y = v; html = html.replace('{{%s_X}}' % k.upper(), str(x)).replace('{{%s_Y}}' % k.upper(), str(y))
html = html.replace('{{MAP}}', open('hf/assets/map.svg.html').read()).replace('{{ROUTE}}', P['route'])
import random
random.seed(7)
cs = []
for _ in range(1600):   # stars
    x, y, r = random.uniform(0, 3240), random.uniform(0, 5760), random.choice([1.5, 2, 2, 3, 4])
    cs.append(f'<i style="left:{x:.0f}px;top:{y:.0f}px;width:{r}px;height:{r}px;background:#fff;opacity:{random.uniform(.35, 1):.2f}"></i>')
pal = [('#9fd3ff', '#1d3b6e'), ('#f1d49a', '#7a4a16'), ('#ff9a6b', '#6b1f10'), ('#7dffb0', '#0f4a3a'), ('#d9d2ff', '#3a2f7a'), ('#e8e2d0', '#3a3a3a')]
for _ in range(170):    # worlds
    x, y = random.uniform(0, 3240), random.uniform(0, 5760)
    r = random.choice([8, 12, 16, 22, 30, 44, 60, 90, 130]) * random.uniform(.8, 1.2)
    a, b = random.choice(pal)
    glow = f'box-shadow:0 0 {r*0.6:.0f}px {a}55;' if r > 40 else ''
    cs.append(f'<i style="left:{x-r:.0f}px;top:{y-r:.0f}px;width:{2*r:.0f}px;height:{2*r:.0f}px;background:radial-gradient(circle at 32% 30%,{a} 0,{b} 62%,#02050a 100%);{glow}"></i>')
html = html.replace('{{COSMOS}}', ''.join(cs))
open('hf/index.html', 'w').write(html)
print('ok', len(C), 'caption chunks')
