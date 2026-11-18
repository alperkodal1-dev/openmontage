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
END = 52.6
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
open('hf/index.html', 'w').write(html)
print('ok', len(C), 'caption chunks')
