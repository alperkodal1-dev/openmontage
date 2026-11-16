"""No-music version: narration + sound effects only (the music input is muted). Based on: narration + the channel's signature piece (an original solo piano in a Gnossienne mood, signature_piano.wav) + sound effects -> mix.m4a at -14 LUFS.
The piece plays under the whole narration and lifts a little in the fantastical passages.
The earlier generated score is kept in music_v1.wav / mix_v1 for reference.
The music is mysterious throughout and lifts in the fantastical passages: the lost-civilization legend
(18.3-25.5 s), the map's wonders (46.4-59.4 s) and the green Antarctica / "how can we be so sure" ending (62.2-72.4 s)."""
import subprocess
SFX = '../../atlantis-story/sfx/'
END = 78.0
VO_END = 75.2
LIFT = [(18.3, 25.5), (46.4, 59.4), (62.2, 72.4)]   # fantastical windows: the legend, the wonders, the ending
BASE, UP, OUTRO = 0.0, 0.0, 0.0
lift = '+'.join(f"between(t,{a},{b})" for a, b in LIFT)
vol = f"if(gte(t,{VO_END}),{BASE}+{OUTRO - BASE}*min(1,(t-{VO_END})/1.2),if({lift},{UP},{BASE}))"
ev = [("rumble", 0.0, 0.45), ("wash", 0.05, 0.2), ("hit", 1.0, 0.55), ("swell", 1.3, 0.16), ("hit", 3.85, 0.45),
      ("whoosh", 6.3, 0.25), ("tick", 8.55, 0.3), ("whoosh", 14.25, 0.25), ("tick", 15.7, 0.25),
      # the legend
      ("swell", 18.2, 0.28), ("tick", 19.3, 0.25), ("tick", 20.4, 0.25), ("rumble", 23.8, 0.4), ("hit", 23.95, 0.4),
      # the ice
      ("whoosh", 25.7, 0.3), ("tick", 27.5, 0.25), ("tick", 30.2, 0.25), ("whoosh", 34.2, 0.3),
      # the notes
      ("hit", 36.55, 0.35), ("tick", 39.4, 0.3), ("tick", 40.6, 0.25), ("tick", 44.5, 0.2), ("tick", 44.75, 0.2), ("tick", 45.0, 0.2),
      # the wonders
      ("swell", 46.3, 0.3), ("wash", 48.6, 0.3), ("tick", 50.66, 0.25), ("rumble", 52.5, 0.35), ("swell", 56.4, 0.26),
      # the ending
      ("hit", 60.95, 0.45), ("swell", 62.2, 0.3), ("wash", 63.0, 0.3), ("rumble", 69.9, 0.35), ("hit", 69.95, 0.3),
      ("whoosh", 72.6, 0.3), ("swell", 72.7, 0.18)]
inp = ["-i", "vo_v2.mp3", "-i", "signature_piano.wav"]; fl = []; lab = []
for i, (n, t, v) in enumerate(ev):
    inp += ["-i", f"{SFX}{n}.wav"]; ms = int(t * 1000)
    fl.append(f"[{i+2}]aformat=channel_layouts=stereo,aresample=48000,adelay={ms}|{ms},volume={v}[e{i}]"); lab.append(f"[e{i}]")
fl.append(f"[0]aformat=channel_layouts=stereo,aresample=48000,apad=whole_dur={END}[v]")
fl.append("[v]asplit=2[v1][vk]")
fl.append(f"[1]aformat=channel_layouts=stereo,aresample=48000,adelay=0|0,volume='{vol}':eval=frame,"
          f"afade=t=out:st={END - 1.4}:d=1.4,apad=whole_dur={END}[m0]")
fl.append("[m0][vk]sidechaincompress=threshold=0.03:ratio=5:attack=20:release=350[m]")
fl.append(f"[v1][m]{''.join(lab)}amix=inputs={len(ev)+2}:normalize=0:duration=first,atrim=0:{END},loudnorm=I=-14:TP=-1.5:LRA=11[out]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *inp, "-filter_complex", ";".join(fl), "-map", "[out]", "-ar", "48000", "-c:a", "aac", "-b:a", "192k", "mix_nomusic.m4a"], check=True)
print("ok")
