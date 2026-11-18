"""Economist 2027 Short (vidIQ recipe: ~20 s, snap zooms every ~1 s, karaoke captions, abrupt loop) -> hf/index.html."""
import json
W = json.load(open('audio/words.json'))
END = 63.7
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
     (34.52, 975, 960, 1.5, 1), (36.0, 430, 880, 1.9, 1),          # AI brain, the robot "stealing something? Mhm."
     (40.88, 1140, 570, 1.5, 1),
     (42.34, 1300, 300, 1.1, 0), (45.32, 1530, 210, 2.0, 1),
     (48.2, 1005, 990, 0.6, 0), (54.24, 1005, 990, 0.7, 0),
     (57.96, 1400, 380, 1.3, 0), (59.3, 1530, 210, 2.2, 0)]       # "look at that corner one more time... what do you see?"
html = open('index.tpl.html').read().replace('{{END}}', str(END)).replace('{{CAPS}}', json.dumps(C)).replace('{{SHOTS}}', json.dumps(S))
open('hf/index.html', 'w').write(html)
print('ok', len(C), 'chunks', len(S), 'shots')
