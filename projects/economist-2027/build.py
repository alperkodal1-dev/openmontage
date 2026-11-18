"""Economist 2027 Short (vidIQ recipe: ~20 s, snap zooms every ~1 s, karaoke captions, abrupt loop) -> hf/index.html."""
import json
W = json.load(open('audio/words.json'))
END = 20.4
# karaoke chunks: break on punctuation or 3 words
ch, cur = [], []
for w in W:
    cur.append(w)
    if w['t'][-1] in '.,?!' or len(cur) >= 3: ch.append(cur); cur = []
if cur: ch.append(cur)
C = [{'s': c[0]['s'], 'e': (ch[i + 1][0]['s'] if i + 1 < len(ch) else END), 'w': [[w['t'].upper(), w['s']] for w in c]} for i, c in enumerate(ch)]
# camera shots: (time, x, y, scale) in cover_circle.png pixels (2010x1980); frame focus point (540, 760)
S = [(0.0, 1005, 990, 0.52), (2.22, 1005, 990, 0.62), (3.04, 1005, 940, 0.75),
     (4.38, 960, 1480, 1.7), (4.78, 240, 1155, 1.7), (5.62, 240, 960, 1.7), (6.92, 1140, 570, 1.7),
     (8.22, 840, 975, 1.8), (9.58, 975, 960, 1.8), (10.84, 1800, 630, 1.7),
     (11.66, 1020, 400, 1.0), (12.8, 1020, 140, 1.6), (13.62, 1020, 140, 2.1),
     (14.7, 1300, 300, 1.2), (15.86, 1530, 210, 2.2), (17.3, 1550, 225, 2.5)]
html = open('index.tpl.html').read().replace('{{END}}', str(END)).replace('{{CAPS}}', json.dumps(C)).replace('{{SHOTS}}', json.dumps(S))
open('hf/index.html', 'w').write(html)
print('ok', len(C), 'chunks', len(S), 'shots')
