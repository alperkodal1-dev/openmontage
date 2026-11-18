"""12-month Short v3 (10 s, 1080x1920, silent, seamless loop): the 12-month grid is on screen the whole time and only
the picture inside each month moves (slow zoom + pan, one 10 s cycle, so the last frame leads into the first).
Source: the sharpened cover (cover_flat_4k.png). Usage: python3 build3.py -> out/months_v3.mp4"""
import math, subprocess
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

FPS, DUR, W, H = 30, 10.0, 1080, 1920
BG = (242, 236, 232)
cover = Image.open('cover_flat_4k.png').convert('RGB')
TW, TH, GAP, LEFT, TOP = 336, 330, 12, 24, 528
CROPS = [(440, 330, 780), (1120, 300, 980), (1580, -140, 900), (2160, 240, 1120), (60, 1080, 1020), (1180, 760, 1100),
         (1920, 860, 1100), (2860, 1060, 1040), (330, 2080, 1000), (1300, 2440, 1240), (1320, 1600, 1020), (2480, 2300, 1140)]
M = 1.18            # source margin around each month (small, so the subject stays in its tile)
SS = 2              # work at 2x for clean downsampling
srcs = []
for (x, y, w) in CROPS:
    h = round(w * TH / TW); cx, cy = x + w / 2, y + h / 2
    ww, hh = round(w * M), round(h * M); x0, y0 = round(cx - ww / 2), round(cy - hh / 2)
    im = Image.new('RGB', (ww, hh), BG)
    sx0, sy0, sx1, sy1 = max(x0, 0), max(y0, 0), min(x0 + ww, cover.width), min(y0 + hh, cover.height)
    im.paste(cover.crop((sx0, sy0, sx1, sy1)), (sx0 - x0, sy0 - y0))
    srcs.append(im.resize((round(TW * M * SS), round(TH * M * SS)), Image.LANCZOS))
labels = [Image.open(f'ov/label{i}.png').convert('RGBA') for i in range(12)]
title = Image.open('ov/title.png').convert('RGBA')
base = Image.new('RGB', (W, H), (11, 11, 11))
base.paste(ImageEnhance.Brightness(cover.resize((1960, 1930)).filter(ImageFilter.GaussianBlur(18))).enhance(0.22), (-440, -5))
base.paste(title, (0, -10), title)

ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'slow', '-crf', '14', '-tune', 'animation', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
                       'out/months_v3.mp4'], stdin=subprocess.PIPE)
N = int(FPS * DUR)
for f in range(N):
    a = 2 * math.pi * f / N          # one full cycle per video -> seamless loop
    fr = base.copy()
    for i, src in enumerate(srcs):
        ph = i * 2 * math.pi / 12 * 5    # different phase per month
        z = 1.13 + 0.06 * math.sin(a + ph)                      # gentle breathing zoom, subject always in view
        px = 0.5 + 0.5 * math.sin(a * 1 + ph * 1.7)             # pan inside the free margin
        py = 0.5 + 0.5 * math.cos(a * 1 + ph * 0.9)
        cw, ch = TW * SS * M / z, TH * SS * M / z
        cw, ch = min(cw, src.width), min(ch, src.height)
        ox, oy = (src.width - cw) * px, (src.height - ch) * py
        tile = src.resize((TW, TH), Image.LANCZOS, box=(ox, oy, ox + cw, oy + ch)).convert('RGBA')
        tile.alpha_composite(labels[i])
        ImageDraw.Draw(tile).rectangle([0, 0, TW - 1, TH - 1], outline=(240, 240, 240), width=2)
        r, c = divmod(i, 3); fr.paste(tile, (LEFT + c * (TW + GAP), TOP + r * (TH + GAP)), tile)
    ff.stdin.write(fr.tobytes())
ff.stdin.close(); ff.wait()
print('ok out/months_v3.mp4')
