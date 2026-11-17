"""Shorts cut (<60 s): shorten long pauses, drop the last line "Tell me in the comments." -> vo_short.mp3, cuts.json."""
import json, subprocess
W = json.load(open('audio/words_v3.json'))
W = W[:[w['t'] for w in W].index('Tell')]           # drop "Tell me in the comments."
cuts = []                                            # removed intervals in the old (vo_v4) time
for a, b in zip(W, W[1:]):
    g = b['s'] - a['e']
    tgt = 0.34 if g >= 0.7 else 0.22
    if g > tgt + 0.05:
        cuts.append((round(a['e'] + tgt / 2, 3), round(b['s'] - tgt / 2, 3)))
END_OLD = W[-1]['e'] + 0.6
def M(t):
    s = 0
    for c0, c1 in cuts:
        if t >= c1: s += c1 - c0
        elif t > c0: s += t - c0
    return t - s
keep, t = [], 0.0
for c0, c1 in cuts: keep.append((t, c0)); t = c1
keep.append((t, END_OLD))
f = ''.join(f'[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.008,afade=t=out:st={b-a-0.008:.3f}:d=0.008[s{i}];' for i, (a, b) in enumerate(keep))
f += ''.join(f'[s{i}]' for i in range(len(keep))) + f'concat=n={len(keep)}:v=0:a=1[o]'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'audio/vo_v4.mp3', '-filter_complex', f, '-map', '[o]', '-c:a', 'libmp3lame', '-q:a', '2', 'short/vo_short.mp3'], check=True)
json.dump({'cuts': cuts, 'end_old': END_OLD, 'end_new': round(M(END_OLD), 3)}, open('short/cuts.json', 'w'))
print(len(cuts), 'cuts; new narration end', round(M(END_OLD), 2), 's; removed', round(END_OLD - M(END_OLD), 2))
