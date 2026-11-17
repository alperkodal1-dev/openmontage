"""Retime the 72 s Noah SRTs to the Shorts cut (../short/cuts.json): noah_<lang>.srt -> noah_short_<lang>.srt."""
import json, re, glob
C = json.load(open('../short/cuts.json')); END = round(C['end_new'] + 0.9, 2) - 0.05
def M(t):
    s = 0
    for a, b in C['cuts']:
        if t >= b: s += b - a
        elif t > a: s += t - a
    return min(t - s, END)
sec = lambda h, m, s, ms: int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000
fmt = lambda t: f"{int(t//3600):02}:{int(t%3600//60):02}:{int(t%60):02},{int(round(t%1*1000)):03}"
for f in sorted(glob.glob('noah_??.srt')):
    out = []
    for blk in open(f, encoding='utf-8').read().strip().split('\n\n'):
        L = blk.split('\n'); m = re.findall(r'(\d+):(\d+):(\d+),(\d+)', L[1])
        a, b = sec(*m[0]), sec(*m[1])
        if a >= 67.6: continue                      # "Tell me in the comments." was cut
        na, nb = M(a), max(M(b), M(a) + 0.4)
        out.append((na, min(nb, END), L[2:]))
    out[-1] = (out[-1][0], END, out[-1][2])
    open(f.replace('noah_', 'noah_short_'), 'w', encoding='utf-8').write(
        '\n'.join(f"{i+1}\n{fmt(a)} --> {fmt(b)}\n" + '\n'.join(t) + '\n' for i, (a, b, t) in enumerate(out)))
    print(f, len(out), fmt(out[-1][1]))
