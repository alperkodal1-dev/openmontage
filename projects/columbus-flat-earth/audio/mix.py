"""Narration + music (ducked under the voice, up for the outro) + sound effects -> mix.m4a at -14 LUFS."""
import subprocess
SFX = '../../atlantis-story/sfx/'
END = 76.0
ev = [("rumble", 0.0, 0.45), ("wash", 0.05, 0.2), ("hit", 1.0, 0.55), ("swell", 1.3, 0.16),
      ("tick", 6.55, 0.28), ("hit", 9.95, 0.35), ("whoosh", 13.2, 0.25), ("tick", 17.5, 0.25), ("tick", 18.6, 0.25),
      ("whoosh", 19.75, 0.25), ("wash", 21.6, 0.3), ("whoosh", 28.65, 0.3), ("swell", 30.4, 0.2), ("hit", 33.95, 0.4),
      ("whoosh", 37.55, 0.3), ("tick", 38.6, 0.25), ("tick", 40.1, 0.25), ("hit", 43.4, 0.4), ("whoosh", 45.15, 0.25),
      ("hit", 47.45, 0.3), ("tick", 52.3, 0.3), ("whoosh", 56.4, 0.3), ("hit", 62.65, 0.5), ("rumble", 62.65, 0.35),
      ("whoosh", 69.25, 0.3), ("swell", 69.3, 0.18)]
inp = ["-i", "vo_v1.mp3", "-i", "music_v1.wav"]; fl = []; lab = []
for i, (n, t, v) in enumerate(ev):
    inp += ["-i", f"{SFX}{n}.wav"]; ms = int(t * 1000)
    fl.append(f"[{i+2}]aformat=channel_layouts=stereo,aresample=48000,adelay={ms}|{ms},volume={v}[e{i}]"); lab.append(f"[e{i}]")
fl.append("[0]aformat=channel_layouts=stereo,aresample=48000,apad=whole_dur=76[v]")
fl.append("[v]asplit=2[v1][vk]")
# music: starts 0.2 s in, base level, louder for the outro once the voice ends (71.6 s), fades at the very end
fl.append("[1]aformat=channel_layouts=stereo,aresample=48000,adelay=200|200,"
          "volume='if(lt(t,71.4),0.30,0.30+0.45*min(1,(t-71.4)/1.2))':eval=frame,afade=t=out:st=74.6:d=1.4,apad=whole_dur=76[m0]")
fl.append("[m0][vk]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=350[m]")
fl.append(f"[v1][m]{''.join(lab)}amix=inputs={len(ev)+2}:normalize=0:duration=first,atrim=0:{END},loudnorm=I=-14:TP=-1.5:LRA=11[out]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *inp, "-filter_complex", ";".join(fl), "-map", "[out]", "-ar", "48000", "-c:a", "aac", "-b:a", "192k", "mix.m4a"], check=True)
