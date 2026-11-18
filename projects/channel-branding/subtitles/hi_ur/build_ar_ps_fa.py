"""Arabic (ar), Pashto (ps), Dari/Persian (fa) SRTs: English cue timings, translated text (tr_ar_ps_fa.py)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tr_ar_ps_fa import *
P = '/home/user/openmontage/projects/'
SRC = {'economist': (P + 'economist-2027/publish/economist_en.srt', ECO), 'alexander': (P + 'alexander-great/publish/alexander_en.srt', ALEX),
       'piri': (P + 'channel-branding/subtitles/out/piri_5SXAmr8qgFM/piri_en.srt', PIRI), 'noah': (P + 'noah-ark/publish_long/noah_en.srt', NOAH),
       'salem': (P + 'salem-remix/publish/salem_en.srt', SALEM), 'pyramid': (P + 'egypt-pyramids/publish/pyramid_en.srt', PYR),
       'atlantis': (P + 'atlantis-story/v4/publish/atlantis_en.srt', ATL)}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')
for name, (src, T) in SRC.items():
    blocks = open(src, encoding='utf-8').read().strip().split('\n\n')
    for lang in ('ar', 'ps', 'fa'):
        assert len(blocks) == len(T[lang]), (name, lang, len(blocks), len(T[lang]))
        open(f'{out}/{name}_{lang}.srt', 'w', encoding='utf-8').write(
            '\n'.join(f"{b.split(chr(10))[0]}\n{b.split(chr(10))[1]}\n{t}\n" for b, t in zip(blocks, T[lang])))
    print(name, len(blocks), 'cues ok')
