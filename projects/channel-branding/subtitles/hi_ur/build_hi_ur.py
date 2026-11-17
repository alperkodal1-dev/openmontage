"""Hindi (hi) and Urdu (ur) SRTs: English cue timings, translated text (tr_*.py)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tr_noah_salem_pyr import *; from tr_atl_piri import *; from tr_ankara import *
P = '/home/user/openmontage/projects/'
SRC = {'noah': (P + 'noah-ark/publish_long/noah_en.srt', NOAH_HI, NOAH_UR),
       'salem': (P + 'salem-remix/publish/salem_en.srt', SALEM_HI, SALEM_UR),
       'pyramid': (P + 'egypt-pyramids/publish/pyramid_en.srt', PYR_HI, PYR_UR),
       'atlantis': (P + 'atlantis-story/v4/publish/atlantis_en.srt', ATL_HI, ATL_UR),
       'piri': (P + 'channel-branding/subtitles/out/piri_5SXAmr8qgFM/piri_en.srt', PIRI_HI, PIRI_UR),
       'ankara': (P + 'channel-branding/subtitles/out/ankara_MP9oLB-ND9A/ankara_en.srt', ANK_HI, ANK_UR)}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out'); os.makedirs(out, exist_ok=True)
for name, (src, hi, ur) in SRC.items():
    blocks = open(src, encoding='utf-8').read().strip().split('\n\n')
    assert len(blocks) == len(hi) == len(ur), (name, len(blocks), len(hi), len(ur))
    for lang, T in (('hi', hi), ('ur', ur)):
        open(f'{out}/{name}_{lang}.srt', 'w', encoding='utf-8').write(
            '\n'.join(f"{b.split(chr(10))[0]}\n{b.split(chr(10))[1]}\n{t}\n" for b, t in zip(blocks, T)))
    print(name, len(blocks), 'cues ok')
