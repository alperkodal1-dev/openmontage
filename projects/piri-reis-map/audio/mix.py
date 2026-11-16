"""Narration + music + sound effects -> mix.m4a at -14 LUFS.
The music is mysterious throughout and lifts in the fantastical passages: the lost-civilization legend
(18.3-25.5 s), the map's wonders (46.4-59.4 s) and the green Antarctica / "how can we be so sure" ending (62.2-72.4 s)."""
import subprocess
SFX = '../../atlantis-story/sfx/'
END = 69.8          # the Short loops: no outro, the last line leads back into the opening question
VO_END = 69.0
LIFT = [(19.5, 25.5), (44.8, 56.8), (59.7, 69.8)]   # fantastical windows: the legend, the wonders, the ending
BASE, UP, OUTRO = 0.22, 0.42, 0.42
lift = '+'.join(f"between(t,{a},{b})" for a, b in LIFT)
vol = f"if({lift},{UP},{BASE})"
ev = [("rumble", 0.0, 0.45), ("wash", 0.05, 0.2), ("hit", 1.0, 0.55), ("swell", 1.3, 0.16),
      ("hit", 4.6, 0.4), ("hit", 8.25, 0.4), ("hit", 9.95, 0.45),
      ("whoosh", 11.3, 0.25), ("tick", 12.2, 0.25), ("tick", 15.4, 0.3), ("tick", 17.6, 0.25),
      # the legend
      ("swell", 19.4, 0.28), ("tick", 19.8, 0.25), ("tick", 20.9, 0.25), ("rumble", 24.0, 0.4), ("hit", 24.2, 0.4),
      # the ice
      ("whoosh", 25.7, 0.3), ("tick", 26.6, 0.25), ("whoosh", 31.1, 0.3),
      # the notes
      ("hit", 33.45, 0.35), ("tick", 34.8, 0.3), ("tick", 36.95, 0.25), ("tick", 43.0, 0.2), ("tick", 43.3, 0.2), ("tick", 43.6, 0.2),
      # the wonders
      ("swell", 44.7, 0.3), ("wash", 47.6, 0.3), ("tick", 49.62, 0.25), ("rumble", 51.4, 0.35), ("swell", 54.5, 0.26),
      # the ending
      ("hit", 58.5, 0.45), ("swell", 59.7, 0.3), ("wash", 60.4, 0.3), ("whoosh", 67.2, 0.3)]
inp = ["-i", "vo_v3.mp3", "-i", "music_v1.wav"]; fl = []; lab = []
for i, (n, t, v) in enumerate(ev):
    inp += ["-i", f"{SFX}{n}.wav"]; ms = int(t * 1000)
    fl.append(f"[{i+2}]aformat=channel_layouts=stereo,aresample=48000,adelay={ms}|{ms},volume={v}[e{i}]"); lab.append(f"[e{i}]")
fl.append(f"[0]aformat=channel_layouts=stereo,aresample=48000,apad=whole_dur={END}[v]")
fl.append("[v]asplit=2[v1][vk]")
fl.append(f"[1]aformat=channel_layouts=stereo,aresample=48000,adelay=0|0,volume='{vol}':eval=frame,"
          f"afade=t=out:st={END - 0.5}:d=0.5,apad=whole_dur={END}[m0]")
fl.append("[m0][vk]sidechaincompress=threshold=0.03:ratio=5:attack=20:release=350[m]")
fl.append(f"[v1][m]{''.join(lab)}amix=inputs={len(ev)+2}:normalize=0:duration=first,atrim=0:{END},loudnorm=I=-14:TP=-1.5:LRA=11[out]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *inp, "-filter_complex", ";".join(fl), "-map", "[out]", "-ar", "48000", "-c:a", "aac", "-b:a", "192k", "mix.m4a"], check=True)
print("ok")
