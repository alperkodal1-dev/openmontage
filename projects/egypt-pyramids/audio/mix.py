"""Narration + music + sound effects -> mix.m4a at -14 LUFS.
The music lifts in the fantastical passages: the alien legend and its clues (0-20.3 s, 26.6-33.8 s) and the stairway to the stars
and the closing question (57-68.6 s). It sits lower under the evidence (40.3-63.2 s), where the generated score swells on its own."""
import subprocess
SFX = '../../atlantis-story/sfx/'
END = 68.6          # the Short loops: no outro, "what were the pyramids, really?" leads back into the opening carving
LIFT = [(0.0, 20.3), (26.6, 33.8), (57.0, 68.6)]   # the alien legend, power plant and stargate, the stairway to the stars
LOW = [(33.8, 56.9)]                                 # the evidence
BASE, UP, DOWN = 0.20, 0.36, 0.14
lift = '+'.join(f"between(t,{a},{b})" for a, b in LIFT)
low = '+'.join(f"between(t,{a},{b})" for a, b in LOW)
vol = f"if({lift},{UP},if({low},{DOWN},{BASE}))"
ev = [("hit", 0.0, 0.5), ("rumble", 0.0, 0.4), ("whoosh", 0.2, 0.3), ("swell", 0.8, 0.22), ("tick", 0.9, 0.25), ("hit", 0.95, 0.35),
      # the visitors and the clues
      ("hit", 4.95, 0.45), ("tick", 6.45, 0.25), ("tick", 6.9, 0.25), ("hit", 7.95, 0.45), ("rumble", 8.0, 0.35),
      ("whoosh", 10.4, 0.25), ("tick", 10.65, 0.2), ("tick", 10.95, 0.2), ("tick", 11.25, 0.2), ("tick", 11.55, 0.2),
      ("whoosh", 13.0, 0.3), ("swell", 13.8, 0.22), ("whoosh", 17.0, 0.3), ("swell", 17.8, 0.22),
      # the Great Pyramid, power plant, stargate
      ("hit", 20.35, 0.5), ("rumble", 20.4, 0.4), ("whoosh", 22.2, 0.2), ("tick", 22.3, 0.25), ("whoosh", 24.6, 0.2), ("tick", 25.5, 0.25),
      ("hit", 27.75, 0.45), ("rumble", 27.8, 0.4), ("swell", 29.2, 0.28), ("tick", 30.6, 0.22), ("tick", 30.72, 0.22), ("tick", 30.84, 0.22),
      ("whoosh", 31.3, 0.3), ("wash", 32.0, 0.3),
      # the builders
      ("hit", 33.9, 0.45), ("rumble", 36.6, 0.35), ("whoosh", 38.6, 0.2), ("hit", 40.4, 0.4), ("tick", 45.3, 0.3), ("tick", 47.05, 0.3),
      # the logbook, the empty sarcophagus
      ("wash", 49.75, 0.25), ("tick", 50.4, 0.25), ("whoosh", 51.4, 0.25), ("hit", 55.65, 0.5), ("rumble", 55.7, 0.35),
      # the pyramid texts, the stairway, the question
      ("swell", 56.95, 0.3), ("wash", 60.4, 0.35), ("tick", 60.6, 0.2), ("tick", 60.9, 0.2), ("tick", 61.2, 0.2),
      ("whoosh", 62.8, 0.25), ("whoosh", 63.7, 0.25), ("swell", 66.0, 0.3), ("hit", 66.05, 0.35)]
inp = ["-i", "vo_v2.mp3", "-i", "music_v2.wav"]; fl = []; lab = []
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
