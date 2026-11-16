"""index.tpl.html + maps + word timings -> hf/index.html and hf/captions.js (times in the narration's timeline)."""
import json, re
from PIL import Image
END = 78.0
P = json.load(open('maps/mappts.json'))
w, h = Image.open('hf/assets/piri_map.jpg').size
MW = 2000; MH = round(MW * h / w)
gx, gy = P['gelibolu']; ix, iy = P['istanbul']
globe = open('maps/globe.svg.html').read()
R = {
    'END': END, 'S7D': round(END - 62.2, 2), 'MW': MW, 'MH': MH,
    'MED': open('maps/med.svg.html').read(), 'GLOBE': globe,
    'GLOBE2': globe.replace('id="globesvg"', 'id="globesvg2"').replace('id="gant"', 'id="gant2"').replace('id="gsam"', 'id="gsam2"'),
    'GX': gx, 'GY': gy, 'IX': ix, 'IY': iy, 'GTX': round(gx - 250), 'GTY': round(gy + 26), 'ITX': round(ix + 26), 'ITY': round(iy - 60),
    # where the map's own drawings sit, as fractions of the image (checked on snapshots)
    'W1X': 0.34, 'W1Y': 0.09, 'W2X': 0.43, 'W2Y': 0.62, 'W3X': 0.17, 'W3Y': 0.45,
}
s = open('index.tpl.html').read()
for k, v in R.items(): s = s.replace('{{' + k + '}}', str(v))
assert '{{' not in s, re.findall(r'\{\{\w+\}\}', s)
open('hf/index.html', 'w').write(s)
W = json.load(open('audio/words.json'))
ch, cur = [], []
for x in W:
    cur.append(x)
    if re.search(r'[.,?!:]["”]?$', x['t']) or x['t'].endswith('...') or len(cur) >= 4 or cur[-1]['e'] - cur[0]['s'] > 1.7:
        ch.append(cur); cur = []
if cur: ch.append(cur)
C = [{'s': c[0]['s'], 'e': c[-1]['e'], 'w': c} for c in ch]
for i in range(len(C) - 1): C[i]['e'] = min(C[i + 1]['s'], round(C[i]['e'] + 0.5, 2))
C[-1]['e'] = round(C[-1]['e'] + 1.2, 2)
open('hf/captions.js', 'w').write('window.CAPS=' + json.dumps(C) + ';')
print('ok', len(C), 'caption chunks; map', MW, 'x', MH)
