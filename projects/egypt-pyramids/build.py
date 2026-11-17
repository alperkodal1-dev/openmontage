"""index.tpl.html + map + word timings -> hf/index.html and hf/captions.js. Also copies the pictures from img/ to
hf/assets/ at render size. Keyword colours in the captions: green for the alien legend, orange for the evidence."""
import json, os, re
from PIL import Image
END = 78.2
A = {'pyr.jpg': 'pyr_khufu.jpg', 'roberts.jpg': 'dauzats.jpg', 'orion.jpg': 'orion.jpg', 'desc.jpg': 'greene_1853.jpg',
     'giza.jpg': 'frith_1858.jpg', 'menkaure.jpg': 'menkaure.jpg', 'legray.jpg': 'legray.jpg', 'bonfils.jpg': 'bonfils.jpg', 'ptexts.jpg': 'pyramid_texts.jpg', 'dogu.jpg': 'dogu.jpg', 'chamber.jpg': 'kings_chamber.jpg', 'abydos.jpg': 'abydos.jpg', 'dendera.jpg': 'dendera.jpg',
     'saqqara.jpg': 'saqqara_bird.jpg'}
for dst, src in A.items():
    p = 'img/' + src
    if not os.path.exists(p) or not os.path.getsize(p): print('missing', src); continue
    im = Image.open(p).convert('RGB'); im.thumbnail((1600, 2200)); im.save('hf/assets/' + dst, quality=88)
P = json.load(open('maps/mappts.json'))
eg = open('maps/egypt.svg.html').read()
(gx, gy), (tx, ty) = P['giza'], P['tura']
# a stair of light from the apex (540,580) to Orion's belt (860,110), and a small one for the split screen
steps = ''.join(f'<rect x="{540 + 32 * i:.0f}" y="{560 - 46 * i:.0f}" width="26" height="12" rx="3"/>' for i in range(10))
steps2 = ''.join(f'<rect x="{480 + 30 * i:.0f}" y="{238 - 22 * i:.0f}" width="20" height="8" rx="2"/>' for i in range(9))
R = {'END': END, 'S7D': round(END - 56.9, 2), 'STEPS': steps, 'STEPS2': steps2, 'EGYPT': eg, 'EGYPT2': eg.replace('id="egsvg"', 'id="egsvg2"').replace('id="nile"', 'id="nile2"'),
     'ABX': P['abydos'][0], 'ABY': P['abydos'][1], 'DEX': P['dendera'][0], 'DEY': P['dendera'][1],
     'SAX': P['saqqara'][0], 'SAY': P['saqqara'][1], 'GIX': gx, 'GIY': gy, 'TUX': tx, 'TUY': ty,
     'TUY2': round(ty - 30, 1), 'GIY2': round(gy + 30, 1), 'MIDX': round((gx + tx) / 2, 1), 'MIDY': round((gy + ty) / 2, 1),
     # where the "helicopter" and the "bulb" sit in their photos, in % (checked on snapshots)
     'RAX': 30, 'RAY': 45, 'RDX': 50, 'RDY': 45}
s = open('index.tpl.html').read()
for k, v in R.items(): s = s.replace('{{' + k + '}}', str(v))
assert '{{' not in s, re.findall(r'\{\{\w+\}\}', s)
open('hf/index.html', 'w').write(s)
ALIEN = {'helicopter.', 'astronauts', 'bulb.', 'glider', 'power', 'plant.', 'stargate:', "orion's", 'staircase', 'sky,', 'orion.', 'stairway', 'stars?', 'really?'}
FACT = {'1968,', '1990,', 'builders,', 'khufu.', 'menkaure.', 'papyrus', 'logbook', 'empty.', 'sarcophagus', 'north.', 'tomb...', 'texts'}
W = json.load(open('audio/words.json'))
for x in W:
    t = x['t'].lower()
    x['k'] = 2 if t in ALIEN else 1 if t in FACT else 0
ch, cur = [], []
for x in W:
    cur.append(x)
    if re.search(r'[.,?!:]["”]?$', x['t']) or x['t'].endswith('...') or len(cur) >= 4 or cur[-1]['e'] - cur[0]['s'] > 1.7:
        ch.append(cur); cur = []
if cur: ch.append(cur)
C = [{'s': c[0]['s'], 'e': c[-1]['e'], 'w': c} for c in ch]
for i in range(len(C) - 1): C[i]['e'] = min(C[i + 1]['s'], round(C[i]['e'] + 0.5, 2))
C[-1]['e'] = round(min(C[-1]['e'] + 1.2, END - 0.1), 2)
open('hf/captions.js', 'w').write('window.CAPS=' + json.dumps(C) + ';')
print('ok', len(C), 'caption chunks')
