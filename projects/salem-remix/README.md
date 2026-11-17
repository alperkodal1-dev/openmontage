# Salem, re-mixed with the channel's own music

The original project files are not in this repo; only the published video (5phbMr3egWo, 71 s) was available.
Its music (Pixabay "Cinematic Strings" + Mussorgsky) carried a Content ID risk (the same Pixabay track got Noah blocked).
Steps: Demucs (htdemucs, two stems) split the narration from the music; residual music in the voice stem measured
25-30 dB below the original in the narration gaps. The voice stem was re-mixed with the vidIQ tension score
(`noah-ark/long/music_tension_72.wav`), side-chain ducked, -14 LUFS. Picture and burned-in captions are unchanged.
Output: `out/salem_ownmusic.mp4`. Upload package: `publish/` (metadata + 7 SRTs, same timing as the original).
