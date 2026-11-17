# History Shorts: Atlantis and Noah's Ark

Two vertical (1080x1920) history Shorts for the Unsealed History channel, built with HyperFrames (HTML/GSAP) and ffmpeg.

| Project | Published | Final file | Turkish subtitles |
|---|---|---|---|
| `atlantis-story/` | https://www.youtube.com/watch?v=_PpRv_GMMlk | `atlantis-story/out/atlantis_story_v2_strings.mp4` | `atlantis-story/out/atlantis_tr.srt` |
| `noah-ark/` | https://www.youtube.com/watch?v=68mjjXGN5EI | `noah-ark/out/nuh_ark_final.mp4` | `noah-ark/out/nuh_tr.srt` |
| `piri-reis-map/` | https://www.youtube.com/watch?v=5SXAmr8qgFM | `piri-reis-map/out/piri_reis_v9_loop.mp4` | `piri-reis-map/out/piri_reis_tr.srt` |
| `egypt-pyramids/` | not published yet (draft v7) | `egypt-pyramids/out/pyramid_v7_draft.mp4` | `egypt-pyramids/out/pyramid_tr.srt` |
| `columbus-flat-earth/` | not published yet | `columbus-flat-earth/out/columbus_final.mp4` | `columbus-flat-earth/out/columbus_tr.srt` |

## Shared look

- Fonts: Cinzel (titles), Cormorant Garamond italic (subtitles), Manrope (captions), Noto Serif Hebrew and Amiri for
  source-language lines. All self-hosted in `hf/assets/fonts/`.
- Palette: ink `#0a1417`, bone `#efe6d2`, gold `#d9b26a`, red stamp `#9c2f1f`.
- Layout: top 250 px kept clear for the platform UI, chapter label at y 268, scene cards between y 400 and 1220,
  word-by-word karaoke captions on a dark plate at y 1235 to 1615.
- Ending: a REAL / MYTH style poll card, with a calm strings outro.

## Atlantis

Narration and footage come from an existing vidIQ composition (not in the repo, 80 MB). The background pass
`hf/assets/bg.mp4` (graded footage with the old captions blurred) is also left out because of its size; rebuild it
from the source video before rendering:

```bash
ffmpeg -i source/atlantis_src.mp4 -filter_complex "[0:v]split=2[base][band];\
[band]crop=1080:180:0:1340,gblur=sigma=28,eq=brightness=-0.08[bl];[base][bl]overlay=0:1340[cov];\
[cov]colorbalance=rs=-0.04:bs=0.06:rh=0.05:gh=0.02:bh=-0.05,eq=contrast=1.07:saturation=0.88:gamma=0.97,\
vignette=angle=PI/4.2,noise=alls=7:allf=t[v]" -map "[v]" -an -c:v libx264 -crf 17 -pix_fmt yuv420p -r 30 hf/assets/bg.mp4
```

- `hf/index.html`: the composition (v2 with chapter labels). `versions/` keeps v1 and v2.
- `sfx/`: synthesized hits, whooshes, rumble and wash; `sfx/mix.py` places them on the narration.
- `v3/assemble.py`: the shorter re-cut that was tried and rejected (kept for reference).

## Noah's Ark

Narration: vidIQ voiceover, voice "George" (closest match to the Atlantis narrator). `audio/vo_v4.mp3` is the
final narration: a new hook line, the main read, and a new closing question spliced together.

Build steps:

```bash
python3 build.py      # index.tpl.html + map -> hf/index.html (times in the old narration's timeline, remapped by timemap.py)
python3 post.py       # shift to the final narration (new hook and ending), write captions.js and words_v3.json
cd hf && npx hyperframes render --quality high --output ../out/visual.mp4
# then mux with audio/mix_v5.m4a, adding light grain:
ffmpeg -i out/visual.mp4 -i audio/mix_v5.m4a -filter_complex "[0:v]noise=alls=6:allf=t,format=yuv420p[v]" \
  -map "[v]" -map 1:a -c:v libx264 -crf 22 -maxrate 8M -bufsize 16M -c:a copy -shortest out/final.mp4
```

The map (`hf/map.svg.html`) is drawn from Natural Earth lakes and rivers (public domain).

## Image credits

- Simon de Myle, *Noah's Ark on Mount Ararat* (1570), public domain.
- Gustave Doré, *The Deluge*, public domain. Athanasius Kircher, Atlantis map (1678), public domain.
- Plato and Solon busts, Josephus portrait (Rijksmuseum, CC0): Wikimedia Commons.
- Mount Ararat photo by Dosseman; Mount Cudi photos by KediÇobanı and M. Abokaram (Wikimedia Commons, CC BY-SA 4.0).
- Music: "Cinematic Strings" by AtlasAudio (Pixabay Content License), not stored here; it is mixed into the final audio.

## Piri Reis map

"Did Someone Map Antarctica Before the Ice?" Narration: vidIQ voiceover, George (`audio/vo_v3.mp3`, script v9 in
`script.md`). The Short loops: the last line ("so how can we be so sure?") leads back into the opening question, and
the camera returns to the map's southern coast. Music: a generated mysterious orchestral score (`audio/music_v1.wav`,
mixed by `audio/mix.py`), lifting in the fantastical passages. `audio/signature_piano.wav` is the channel's signature
piano piece, tried as an alternative.

```bash
python3 tools/prep_map.py <scan.jpg> hf/assets/piri_map.jpg   # white surround -> dark ground
python3 build.py && python3 make_srt.py
cd hf && npx hyperframes render --quality high --output ../out/visual.mp4
```

Map scan: Piri Reis map, 1513 (Wikimedia Commons, public domain). Globe and Mediterranean maps from Natural Earth.

## Great Pyramid (draft)

"Who Really Built the Great Pyramid? The Alien Clues". Narration: vidIQ voiceover, George (`audio/vo_v1.mp3`, script v3);
v4 in `script.md` is the jury's revision, not voiced yet. Music: generated mysterious orchestral score
(`audio/music_v1.wav`), lifting under the alien legend and the closing question. Images: Wikimedia Commons and
The Met Open Access (CC0); map from Natural Earth. Jury notes: `review/jury_report.md`.

```bash
python3 build.py && python3 make_srt.py && (cd audio && python3 mix.py)
cd hf && npx hyperframes render --quality high --output ../out/visual.mp4
```
