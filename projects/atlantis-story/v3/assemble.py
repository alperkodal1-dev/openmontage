"""Re-cut the Atlantis Short for retention: cold open on the flood, tighter order, 1.07x pace, hook headline, loop end."""
import subprocess, sys

VIS = sys.argv[1] if len(sys.argv) > 1 else "../out/visual_nochap.mp4"
AUD = "../sfx/mix.m4a"
OUT = sys.argv[2] if len(sys.argv) > 2 else "../out/atlantis_story_v3.mp4"
SPEED = 1.07

# (in, out) in v2 timeline seconds; order is the new story order
EDL = [
    (47.36, 52.75),  # in a single day and night, earthquakes and floods swallowed it into the sea
    (6.00, 10.45),   # there is no ancient map, no ruins, no inscription
    (10.75, 14.50),  # the entire legend comes from one man, Plato
    (14.90, 21.08),  # around 360 BC ... Timaeus and the Critias
    (25.20, 29.10),  # an Egyptian priest told it to Solon
    (29.40, 34.62),  # Solon passed it on ... generation after generation
    (34.85, 37.78),  # until it reached Plato's character Critias
    (37.90, 43.00),  # a mighty naval empire beyond the Pillars of Hercules
    (43.45, 46.35),  # an empire that tried to conquer the Mediterranean
    (52.85, 60.18),  # when did this happen? 9,000 years before Plato, yet no writer ...
    (60.35, 66.05),  # many historians believe Plato invented it ...
    (66.15, 71.70),  # so was Atlantis real or the greatest story ever told?
]

inputs = ["-i", VIS, "-i", AUD, "-loop", "1", "-t", "4", "-i", "hook.png", "-i", "../sfx/whoosh.wav"]
fc, cat = [], []
cuts, t = [], 0.0
for i, (a, b) in enumerate(EDL):
    d = b - a
    fc.append(f"[0:v]trim={a}:{b},setpts=(PTS-STARTPTS)/{SPEED}[v{i}]")
    fc.append(f"[1:a]atrim={a}:{b},asetpts=PTS-STARTPTS,atempo={SPEED},"
              f"afade=t=in:d=0.04,afade=t=out:st={d/SPEED-0.06:.3f}:d=0.06[a{i}]")
    cat.append(f"[v{i}][a{i}]")
    t += d / SPEED
    cuts.append(t)
fc.append(f"{''.join(cat)}concat=n={len(EDL)}:v=1:a=1[vc][ac]")
# hook headline on the first 3.4 s, fading out
fc.append("[2:v]format=rgba,fade=t=out:st=3.1:d=0.3:alpha=1[hk]")
fc.append("[vc][hk]overlay=0:0:enable='lt(t,3.45)'[vo]")
# soft whoosh on each story cut (skip the last end point)
w = []
for j, c in enumerate(cuts[:-1]):
    ms = int(max(0, c - 0.25) * 1000)
    fc.append(f"[3:a]volume=0.18,adelay={ms}|{ms}[w{j}]")
    w.append(f"[w{j}]")
fc.append(f"[ac]{''.join(w)}amix=inputs={len(w)+1}:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11[ao]")
cmd = ["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(fc), "-map", "[vo]", "-map", "[ao]",
       "-c:v", "libx264", "-preset", "slow", "-crf", "22", "-maxrate", "8M", "-bufsize", "16M", "-pix_fmt", "yuv420p",
       "-r", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", OUT]
subprocess.run(cmd, check=True)
print(f"total {t:.2f}s, cuts at", [round(c, 2) for c in cuts])
