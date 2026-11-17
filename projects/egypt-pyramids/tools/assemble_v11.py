"""v11 narration: tighten pauses, cut "aligned to true north" and "Next door,", swap in the new builders line.
Writes audio/vo_v11.mp3, audio/words.json (new times) and audio/timemap.json (old -> new anchors, final timeline)."""
import json, subprocess
W = json.load(open('words_v10.json'))                     # final timeline of v10 (hook + narration)
BW = json.load(open('builders_words.json'))               # the new builders line, local times
txt = [w['t'] for w in W]
i_al = next(i for i, w in enumerate(W) if w['t'] == 'aligned')
i_bn = next(i for i, w in enumerate(W) if w['t'] == 'Beneath')
i_bp = next(i for i in range(i_bn, len(W)) if W[i]['t'] == 'pyramid.')
i_nd = next(i for i, w in enumerate(W) if w['t'] == 'Next')
cut = set(range(i_al, i_al + 4)) | {i_nd, i_nd + 1}
assert ' '.join(txt[i_al:i_al + 4]) == 'aligned to true north.' and ' '.join(txt[i_nd:i_nd + 2]) == 'Next door,'
items = []                                               # (src, word dict, old index or None)
for i, w in enumerate(W):
    if i in cut: continue
    if i_bn <= i <= i_bp:
        if i == i_bn: items += [('b', {'t': t, 's': s, 'e': e}, None) for t, s, e in BW]
        continue
    items.append(('v', dict(w), i))
# segments: runs of words from one source with gaps under 0.25 s
segs = []
for it in items:
    if segs and segs[-1]['src'] == it[0] and it[1]['s'] - segs[-1]['words'][-1][1]['e'] < 0.25:
        segs[-1]['words'].append(it)
    else:
        segs.append({'src': it[0], 'words': [it]})
SPECIAL = {'they?': 0.4, 'goes.': 0.35, 'belt.': 0.3, 'stars?': 0.3}
pieces, t, new_words, anchors = [], 0.0, [], []
for k, sg in enumerate(segs):
    w0, w1 = sg['words'][0][1], sg['words'][-1][1]
    # whisper word starts run a little late: open the cut earlier, but never into the previous (kept or cut) word
    oi0 = sg['words'][0][2]
    if sg['src'] == 'v' and oi0:
        a = max(W[oi0 - 1]['e'] + 0.02, w0['s'] - 0.15)
    else:
        a = max(0, w0['s'] - 0.06)
    oi1 = sg['words'][-1][2]
    b = min(W[oi1 + 1]['s'] - 0.02, w1['e'] + 0.12) if sg['src'] == 'v' and oi1 is not None and oi1 + 1 < len(W) else w1['e'] + 0.1
    if k:
        prev = segs[k - 1]['words'][-1][1]['t']
        gap = SPECIAL.get(prev, 0.18 if prev[-1] in '.?!' or prev.endswith('...') else 0.04)
        t += gap
    src = 'vo_v10.mp3' if sg['src'] == 'v' else 'vo_builders.mp3'
    pieces.append((src, a, b, t))
    for src_, w, oi in sg['words']:
        nw = {'t': w['t'], 's': round(t + w['s'] - a, 2), 'e': round(t + w['e'] - a, 2)}
        new_words.append(nw)
        if oi is not None: anchors.append((W[oi]['s'], nw['s']))
    t += b - a
END = round(new_words[-1]['e'] + 1.0, 2)
# audio: place each piece on a silent bed
inp, fl, lab = [], [], []
for n, (src, a, b, at) in enumerate(pieces):
    inp += ['-i', src]
    fl.append(f"[{n}]atrim={a}:{b},asetpts=PTS-STARTPTS,aresample=44100,aformat=channel_layouts=mono,afade=t=in:d=0.02,afade=t=out:st={b-a-0.03:.3f}:d=0.03,adelay={int(at*1000)}|{int(at*1000)}[p{n}]")
    lab.append(f"[p{n}]")
fl.append(f"{''.join(lab)}amix=inputs={len(pieces)}:normalize=0:duration=longest,apad=whole_dur={END}[o]")
subprocess.run(['ffmpeg', '-v', 'error', '-y', *inp, '-filter_complex', ';'.join(fl), '-map', '[o]', '-c:a', 'libmp3lame', '-q:a', '2', 'vo_v11.mp3'], check=True)
json.dump(new_words, open('words.json', 'w'))
# anchors for scenes: old word starts -> new; the cut words map onto the next kept word
old = [a for a, _ in anchors]; new = [b for _, b in anchors]
json.dump({'old': [0.0] + old + [W[-1]['e'] + 5], 'new': [0.0] + new + [new_words[-1]['e'] + 5], 'end': END}, open('timemap.json', 'w'))
print('pieces', len(pieces), 'old end', W[-1]['e'], 'new end', new_words[-1]['e'], 'END', END)
