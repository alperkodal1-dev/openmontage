"""Narration + music + sound effects -> mix.m4a at -14 LUFS.
The music lifts in the fantastical passages: the alien legend and its clues (14.2-40.2 s) and the closing alien
question (63.3-68.2 s). It sits lower under the evidence (40.3-63.2 s), where the generated score swells on its own."""
import subprocess
SFX = '../../atlantis-story/sfx/'
END = 68.2          # the Short loops: no outro, the last line leads back into the opening question
LIFT = [(14.2, 40.2), (63.3, 68.2)]
LOW = [(47.5, 63.2)]
BASE, UP, DOWN = 0.22, 0.40, 0.14
lift = '+'.join(f"between(t,{a},{b})" for a, b in LIFT)
low = '+'.join(f"between(t,{a},{b})" for a, b in LOW)
vol = f"if({lift},{UP},if({low},{DOWN},{BASE}))"
ev = [("rumble", 0.0, 0.45), ("wash", 0.05, 0.2), ("hit", 1.0, 0.55), ("swell", 1.3, 0.16),
      ("hit", 4.3, 0.4), ("tick", 6.45, 0.3), ("whoosh", 8.3, 0.25), ("tick", 9.4, 0.25), ("hit", 11.55, 0.4),
      # the visitors
      ("swell", 14.2, 0.3), ("hit", 14.35, 0.45), ("tick", 15.8, 0.25), ("tick", 16.4, 0.25), ("hit", 18.05, 0.45), ("rumble", 18.1, 0.35),
      ("whoosh", 20.1, 0.25), ("tick", 20.7, 0.2), ("tick", 21.0, 0.2), ("tick", 21.3, 0.2), ("tick", 21.55, 0.2),
      # the clues
      ("whoosh", 22.75, 0.3), ("swell", 23.65, 0.22), ("whoosh", 24.8, 0.3), ("swell", 25.7, 0.22), ("whoosh", 28.1, 0.3), ("swell", 29.0, 0.22),
      ("hit", 33.6, 0.45), ("rumble", 33.8, 0.4), ("swell", 35.1, 0.28), ("tick", 37.0, 0.22), ("tick", 37.12, 0.22), ("tick", 37.24, 0.22),
      ("whoosh", 37.9, 0.3), ("wash", 38.6, 0.3),
      # the builders
      ("hit", 40.9, 0.4), ("rumble", 42.7, 0.35), ("hit", 46.6, 0.4), ("tick", 50.85, 0.3), ("tick", 52.4, 0.3),
      # the logbook
      ("wash", 53.6, 0.25), ("tick", 54.4, 0.25), ("whoosh", 55.75, 0.25),
      # the empty tomb and the question
      ("hit", 59.9, 0.5), ("rumble", 60.0, 0.35), ("hit", 61.85, 0.45), ("swell", 63.3, 0.3), ("wash", 64.6, 0.3)]
inp = ["-i", "vo_v1.mp3", "-i", "music_v1.wav"]; fl = []; lab = []
for i, (n, t, v) in enumerate(ev):
    inp += ["-i", f"{SFX}{n}.wav"]; ms = int(t * 1000)
    fl.append(f"[{i+2}]aformat=channel_layouts=stereo,aresample=48000,adelay={ms}|{ms},volume={v}[e{i}]"); lab.append(f"[e{i}]")
fl.append(f"[0]aformat=channel_layouts=stereo,aresample=48000,apad=whole_dur={END}[v]")
fl.append("[v]asplit=2[v1][vk]")
fl.append(f"[1]aformat=channel_layouts=stereo,aresample=48000,volume='{vol}':eval=frame,"
          f"afade=t=out:st={END - 0.5}:d=0.5,apad=whole_dur={END}[m0]")
fl.append("[m0][vk]sidechaincompress=threshold=0.03:ratio=5:attack=20:release=350[m]")
fl.append(f"[v1][m]{''.join(lab)}amix=inputs={len(ev)+2}:normalize=0:duration=first,atrim=0:{END},loudnorm=I=-14:TP=-1.5:LRA=11[out]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *inp, "-filter_complex", ";".join(fl), "-map", "[out]", "-ar", "48000", "-c:a", "aac", "-b:a", "192k", "mix.m4a"], check=True)
print("ok")
