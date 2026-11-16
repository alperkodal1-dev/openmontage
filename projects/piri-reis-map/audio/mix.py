"""Narration + music + sound effects -> mix.m4a at -14 LUFS.
The music is mysterious throughout and lifts in the fantastical passages: the map's wonders (18.7-29.5 s),
the lost-civilization legend (29.8-37.6 s) and the green Antarctica / "who knows" ending (61.7-69.2 s)."""
import subprocess
SFX = '../../atlantis-story/sfx/'
END = 76.0
LIFT = [(18.6, 29.6), (29.8, 37.6), (61.6, 69.2)]   # fantastical windows
BASE, UP, OUTRO = 0.22, 0.42, 0.72
lift = '+'.join(f"between(t,{a},{b})" for a, b in LIFT)
vol = f"if(gte(t,71.4),{BASE}+{OUTRO - BASE}*min(1,(t-71.4)/1.2),if({lift},{UP},{BASE}))"
ev = [("rumble", 0.0, 0.45), ("wash", 0.05, 0.2), ("hit", 1.0, 0.55), ("swell", 1.3, 0.16), ("hit", 3.85, 0.45),
      ("whoosh", 6.2, 0.25), ("tick", 8.4, 0.3), ("whoosh", 14.25, 0.25), ("tick", 16.15, 0.25),
      # the wonders
      ("swell", 18.4, 0.3), ("wash", 21.0, 0.3), ("tick", 23.66, 0.25), ("rumble", 25.1, 0.35), ("swell", 26.8, 0.22),
      # the legend
      ("whoosh", 29.7, 0.3), ("tick", 31.2, 0.25), ("tick", 32.0, 0.25), ("rumble", 35.8, 0.4), ("hit", 35.95, 0.4),
      ("whoosh", 37.85, 0.3), ("tick", 39.6, 0.25), ("tick", 42.3, 0.25), ("whoosh", 46.9, 0.3),
      ("whoosh", 49.3, 0.25), ("hit", 50.9, 0.35), ("tick", 52.9, 0.25), ("tick", 57.6, 0.2), ("tick", 57.8, 0.2), ("tick", 58.0, 0.2),
      ("hit", 60.6, 0.45),
      # the ending
      ("swell", 61.5, 0.3), ("wash", 62.4, 0.3), ("rumble", 65.9, 0.35), ("whoosh", 69.1, 0.3), ("swell", 69.2, 0.18)]
inp = ["-i", "vo_v1.mp3", "-i", "music_v1.wav"]; fl = []; lab = []
for i, (n, t, v) in enumerate(ev):
    inp += ["-i", f"{SFX}{n}.wav"]; ms = int(t * 1000)
    fl.append(f"[{i+2}]aformat=channel_layouts=stereo,aresample=48000,adelay={ms}|{ms},volume={v}[e{i}]"); lab.append(f"[e{i}]")
fl.append(f"[0]aformat=channel_layouts=stereo,aresample=48000,apad=whole_dur={END}[v]")
fl.append("[v]asplit=2[v1][vk]")
fl.append(f"[1]aformat=channel_layouts=stereo,aresample=48000,adelay=0|0,volume='{vol}':eval=frame,"
          f"afade=t=out:st={END - 1.4}:d=1.4,apad=whole_dur={END}[m0]")
fl.append("[m0][vk]sidechaincompress=threshold=0.03:ratio=5:attack=20:release=350[m]")
fl.append(f"[v1][m]{''.join(lab)}amix=inputs={len(ev)+2}:normalize=0:duration=first,atrim=0:{END},loudnorm=I=-14:TP=-1.5:LRA=11[out]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *inp, "-filter_complex", ";".join(fl), "-map", "[out]", "-ar", "48000", "-c:a", "aac", "-b:a", "192k", "mix.m4a"], check=True)
print("ok")
