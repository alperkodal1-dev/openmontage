"""index.tpl.html + maps + word timings -> hf/index.html and hf/captions.js. Times are in the narration's timeline."""
import json, re
END = 76.0
P = json.load(open('maps/mappts.json'))
(ax, ay), (sx, sy) = P['alex'], P['syene']
cx, cy = P['canary']; hx, hy = P['hisJapan']; jx, jy = P['japan']
R = {
    'END': END, 'BG7D': round(END - 64.7, 2), 'S7D': round(END - 64.9, 2),
    'EGYPT': open('maps/egypt.svg.html').read(), 'OCEAN': open('maps/ocean.svg.html').read(),
    'SUNX': sx, 'SYX_R': sx - 3, 'SYH': round(sy - 110), 'ALX_R': ax - 3, 'ALH': round(ay + 40),
    'ALX': ax, 'ALY': ay, 'SYX': sx, 'SYY': sy,
    'ALTX': round(ax + 30), 'ALTY': round(ay - 20), 'SYTX': round(sx - 450), 'SYTY': round(sy - 22),
    'ANGX': round(ax - 130), 'ANGY': round(ay + 20),
    'CAX': cx, 'CAY': cy, 'HISX': round(hx - 170), 'HISY': round(hy + 30), 'JPX': round(jx - 40), 'JPY': round(jy + 40),
    'SACRO': '<img src="assets/sphaera_met.jpg" alt=""><div class="cap2">SACROBOSCO · DE SPHAERA · VENICE 1482</div>',
}
s = open('index.tpl.html').read()
for k, v in R.items(): s = s.replace('{{' + k + '}}', str(v))
assert '{{' not in s, re.findall(r'\{\{\w+\}\}', s)
open('hf/index.html', 'w').write(s)

W = json.load(open('audio/words.json'))
ch, cur = [], []
for w in W:
    cur.append(w)
    if re.search(r'[.,?!:]["”]?$', w['t']) or len(cur) >= 4 or cur[-1]['e'] - cur[0]['s'] > 1.7:
        ch.append(cur); cur = []
if cur: ch.append(cur)
C = [{'s': c[0]['s'], 'e': c[-1]['e'], 'w': c} for c in ch]
for i in range(len(C) - 1): C[i]['e'] = min(C[i + 1]['s'], round(C[i]['e'] + 0.5, 2))
C[-1]['e'] = round(C[-1]['e'] + 1.2, 2)
open('hf/captions.js', 'w').write('window.CAPS=' + json.dumps(C) + ';')
print('ok', len(C), 'caption chunks')
