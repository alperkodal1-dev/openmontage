"""Economist 2027 Short (vidIQ recipe: ~20 s, snap zooms every ~1 s, karaoke captions, abrupt loop) -> hf/index.html."""
import json
W = json.load(open('audio/words.json'))
END = 56.0
# karaoke chunks: break on punctuation or 3 words
ch, cur = [], []
for w in W:
    cur.append(w)
    if w['t'][-1] in '.,?!' or len(cur) >= 3: ch.append(cur); cur = []
if cur: ch.append(cur)
C = [{'s': c[0]['s'], 'e': (ch[i + 1][0]['s'] if i + 1 < len(ch) else END), 'w': [[w['t'].upper(), w['s']] for w in c]} for i, c in enumerate(ch)]
# camera shots: (time, x, y, scale) in cover_circle.png pixels (2010x1980); frame focus point (540, 760)
# camera shots: (time, x, y, scale, snap) in cover_circle.png pixels (2010x1980); frame focus point (540, 760)
S = [(0.0, 1005, 990, 0.52, 0), (2.4, 1005, 990, 0.66, 0),
     (7.3, 1080, 1590, 1.5, 1),                                   # crystal ball: "prints the future"
     (17.64, 1005, 990, 0.55, 0), (19.36, 1020, 140, 1.5, 1), (22.28, 960, 1480, 1.5, 1), (24.36, 810, 1725, 1.5, 1),
     (27.72, 1680, 1290, 1.5, 1), (28.48, 260, 640, 1.6, 1),      # jets, China
     (34.92, 975, 960, 1.5, 1), (35.98, 420, 885, 1.6, 1), (38.64, 1140, 570, 1.5, 1),
     (39.88, 1300, 300, 1.1, 0), (42.74, 1530, 210, 2.0, 1),
     (45.6, 1005, 990, 0.6, 0), (51.56, 1005, 990, 0.7, 0), (54.22, 1530, 210, 2.1, 1)]
html = open('index.tpl.html').read().replace('{{END}}', str(END)).replace('{{CAPS}}', json.dumps(C)).replace('{{SHOTS}}', json.dumps(S))
open('hf/index.html', 'w').write(html)
print('ok', len(C), 'chunks', len(S), 'shots')
