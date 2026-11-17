"""Remap the 72.2 s composition (hf/index.html) to the Shorts cut: clip attributes in Python, GSAP tweens in JS."""
import json, re
C = json.load(open('short/cuts.json')); cuts = C['cuts']; END = round(C['end_new'] + 0.9, 2)
def M(t):
    s = 0
    for c0, c1 in cuts:
        if t >= c1: s += c1 - c0
        elif t > c0: s += t - c0
    return min(t - s, END)
s = open('short/index_final72.html').read()
def attr(m):
    a, d = float(m.group(1)), float(m.group(2)); e = a + d
    na, ne = M(a), (END if e >= 69.9 else M(e))
    return f'data-start="{na:.2f}" data-duration="{ne-na:.2f}"'
s = re.sub(r'data-start="([\d.]+)" data-duration="([\d.]+)"', attr, s)
s = s.replace('data-duration="72.2"', f'data-duration="{END}"')
js = ("const CUTS=" + json.dumps(cuts) + ", END=" + str(END) + ";\n"
      "  const Mx = t => { let s = 0; for (const [a, b] of CUTS) { if (t >= b) s += b - a; else if (t > a) s += t - a; } return Math.min(t - s, END); };\n"
      "  tl.getChildren(false, true, true).forEach(c => { const a = c.startTime(), e = a + c.totalDuration(); const na = Mx(a), ne = Mx(e);\n"
      "    c.startTime(na); if (e - a > 0.001 && ne - na > 0.001) c.timeScale((e - a) / (ne - na)); });\n"
      "  window.__timelines = window.__timelines || {};")
s = s.replace('window.__timelines = window.__timelines || {};', js, 1)
# Shorts safe area: keep captions clear of the right-hand action buttons
s = s.replace('.cap{position:absolute;left:80px;right:80px;', '.cap{position:absolute;left:70px;right:150px;')
open('hf/index.html', 'w').write(s)
caps = open('short/captions_final72.js').read()
C2 = json.loads(caps[len('window.CAPS='):].rstrip(';\n'))
C2 = [c for c in C2 if not any(w['t'] in ('Tell', 'me', 'comments.') and w['s'] > 67 for w in c['w'])]
C2[-1]['e'] = round(C2[-1]['w'][-1]['e'] + 1.2, 2)
open('hf/captions.js', 'w').write('window.CAPS=' + json.dumps(C2) + ';')
print('END', END, 'caps', len(C2), 'last', C2[-1]['w'][-1]['t'])
