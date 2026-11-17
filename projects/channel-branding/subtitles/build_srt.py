"""All channel videos -> out/<video>/<video>_<lang>.srt (en, es, pt, de, fr, ja), plus plain English transcripts for
the videos whose timings are approximate (YouTube Studio > Subtitles > Upload file > Without timing auto-syncs them).
Run: python3 build_srt.py"""
import importlib, os, textwrap
LANGS = ['en', 'es', 'pt', 'de', 'fr', 'ja']
# Turkish: the reviewed project SRTs for the three Shorts made here, TR lists in data_salem/data_ankara for the others
TR_FILES = {'piri': '../../piri-reis-map/out/piri_reis_tr.srt', 'noah': '../../noah-ark/out/nuh_tr.srt',
            'atlantis': '../../atlantis-story/out/atlantis_tr.srt'}
import shutil
VIDEOS = {'piri': '5SXAmr8qgFM', 'noah': '68mjjXGN5EI', 'atlantis': '_PpRv_GMMlk', 'salem': '5phbMr3egWo', 'ankara': 'MP9oLB-ND9A'}

def ts(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def wrap(text, lang):
    if lang == 'ja':
        n = 20
        return '\n'.join(text[i:i + n] for i in range(0, len(text), n)) if len(text) > n else text
    lines = textwrap.wrap(text, 42)
    if len(lines) > 2: lines = textwrap.wrap(text, (len(text) + 1) // 2 + 6)
    return '\n'.join(lines)

def from_chunks(mod):
    cues = []
    ch = mod.CHUNKS
    for i, (start, sents) in enumerate(ch):
        stop = ch[i + 1][0] if i + 1 < len(ch) else mod.END
        total = sum(len(s[0]) for s in sents); t = start
        for s in sents:
            d = (stop - start) * len(s[0]) / total
            cues.append((round(t, 2), round(t + d - 0.15, 2), *s)); t += d
    return cues

os.makedirs('out', exist_ok=True)
for name, vid in VIDEOS.items():
    mod = importlib.import_module('data_' + name)
    cues = mod.CUES if hasattr(mod, 'CUES') else from_chunks(mod)
    d = f'out/{name}_{vid}'; os.makedirs(d, exist_ok=True)
    for li, lang in enumerate(LANGS):
        out = []
        for k, c in enumerate(cues):
            s, e, texts = c[0], c[1], c[2:]
            if k + 1 < len(cues): e = min(e + 0.3, cues[k + 1][0] - 0.05)
            out.append(f"{k + 1}\n{ts(s)} --> {ts(e)}\n{wrap(texts[li], lang)}\n")
        open(f'{d}/{name}_{lang}.srt', 'w', encoding='utf-8').write('\n'.join(out))
    if name in TR_FILES: shutil.copy(TR_FILES[name], f'{d}/{name}_tr.srt')
    else:
        assert len(mod.TR) == len(cues), (name, len(mod.TR), len(cues))
        out = []
        for k, c in enumerate(cues):
            s, e = c[0], c[1]
            if k + 1 < len(cues): e = min(e + 0.3, cues[k + 1][0] - 0.05)
            out.append(f"{k + 1}\n{ts(s)} --> {ts(e)}\n{wrap(mod.TR[k], 'tr')}\n")
        open(f'{d}/{name}_tr.srt', 'w', encoding='utf-8').write('\n'.join(out))
    if not hasattr(mod, 'CUES'):
        open(f'{d}/{name}_en_transcript.txt', 'w', encoding='utf-8').write('\n'.join(c[2] for c in cues) + '\n')
    print(name, vid, len(cues), 'cues')
