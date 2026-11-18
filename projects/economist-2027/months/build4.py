"""12-month Short v4 (10 s seamless loop, 1080x1920, silent). All 12 month pictures are cut from the cover and placed
as tiles; every tile runs its OWN short loop with a clearly visible motion that fits its picture (plane flies, missiles
rain, fire flickers, brain beats...). Every loop period divides 10 s, so the whole video loops seamlessly.
Usage: python3 build4.py -> out/months_v4.mp4"""
import math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

FPS, DUR, W, H = 30, 10.0, 1080, 1920
N = int(FPS * DUR)
BG = (242, 236, 232)
cover = Image.open('cover_flat_4k.png').convert('RGB')
TW, TH, GAP, LEFT, TOP = 336, 330, 12, 24, 528
CROPS = [(440, 330, 780), (1120, 300, 980), (1580, -140, 900), (2160, 240, 1120), (60, 1080, 1020), (1180, 760, 1100),
         (1920, 860, 1100), (2860, 1060, 1040), (330, 2080, 1000), (1300, 2440, 1240), (1320, 1600, 1020), (2480, 2300, 1140)]
# motion per month: (kind, period in seconds)
MOTION = ['launch', 'pulse', 'scan', 'fly', 'fire', 'pulse', 'crash', 'ride', 'missiles', 'blast', 'heartbeat', 'waves']
PERIOD = [5, 2.5, 5, 5, 2.5, 2.5, 2.5, 5, 2.5, 1.25, 1.25, 2.5]
M, SS = 1.40, 2
srcs, reds = [], []
for (x, y, w) in CROPS:
    h = round(w * TH / TW); cx, cy = x + w / 2, y + h / 2
    ww, hh = round(w * M), round(h * M); x0, y0 = round(cx - ww / 2), round(cy - hh / 2)
    im = Image.new('RGB', (ww, hh), BG)
    sx0, sy0, sx1, sy1 = max(x0, 0), max(y0, 0), min(x0 + ww, cover.width), min(y0 + hh, cover.height)
    im.paste(cover.crop((sx0, sy0, sx1, sy1)), (sx0 - x0, sy0 - y0))
    im = im.resize((round(TW * M * SS), round(TH * M * SS)), Image.LANCZOS)
    srcs.append(im)
    a = np.asarray(im).astype(np.int16)
    reds.append(((a[..., 0] > 140) & (a[..., 1] < 90)).astype(np.float32))   # red ink mask (fire, blood, flags)
labels = [Image.open(f'ov/label{i}.png').convert('RGBA') for i in range(12)]
title = Image.open('ov/title.png').convert('RGBA')
base = Image.new('RGB', (W, H), (11, 11, 11))
base.paste(ImageEnhance.Brightness(cover.resize((1960, 1930)).filter(ImageFilter.GaussianBlur(18))).enhance(0.22), (-440, -5))
base.paste(title, (0, -10), title)

def view(src, z, px, py, rot=0.0):
    """Crop a window (zoom z >= 1 relative to the tile area, position px/py in 0..1 of the free margin) -> tile."""
    cw, ch = TW * SS * M / z / 1.0, TH * SS * M / z
    cw, ch = min(cw, src.width), min(ch, src.height)
    ox, oy = (src.width - cw) * px, (src.height - ch) * py
    if rot:
        pad = 1.12; bw, bh = min(cw * pad, src.width), min(ch * pad, src.height)
        bx = max(0, min(ox - (bw - cw) / 2, src.width - bw)); by = max(0, min(oy - (bh - ch) / 2, src.height - bh))
        im = src.resize((round(TW * pad * SS), round(TH * pad * SS)), Image.BICUBIC, box=(bx, by, bx + bw, by + bh))
        im = im.rotate(rot, resample=Image.BICUBIC, fillcolor=BG)
        l = (im.width - TW * SS) // 2; t = (im.height - TH * SS) // 2
        return im.crop((l, t, l + TW * SS, t + TH * SS)).resize((TW, TH), Image.LANCZOS)
    return src.resize((TW, TH), Image.LANCZOS, box=(ox, oy, ox + cw, oy + ch))

def tile_at(i, t):
    k, P = MOTION[i], PERIOD[i]
    u = (t % P) / P; s = math.sin(2 * math.pi * u); c = math.cos(2 * math.pi * u)
    src = srcs[i]
    if k == 'launch':    im = view(src, 1.30, 0.5 + 0.06 * s, 0.75 - 0.5 * u if u < 0.8 else 0.35 + 2.0 * (u - 0.8), rot=2.5 * s)
    elif k == 'pulse':   im = view(src, 1.18 + 0.16 * (0.5 - 0.5 * c), 0.5, 0.5)
    elif k == 'scan':    im = view(src, 1.35, 0.5 - 0.48 * c, 0.15)
    elif k == 'fly':     im = view(src, 1.30, 0.5 + 0.48 * c, 0.4 + 0.08 * s)
    elif k == 'crash':   im = view(src, 1.30, 0.5, 0.5 - 0.45 * c, rot=-3 * s)
    elif k == 'ride':    im = view(src, 1.30, 0.5 - 0.45 * s, 0.5 + 0.05 * abs(math.sin(8 * math.pi * u)))
    elif k == 'missiles':im = view(src, 1.40, 0.95 - 0.9 * u, 0.05 + 0.9 * u)       # slides along the missiles' path
    elif k == 'waves':   im = view(src, 1.30, 0.5 + 0.12 * s, 0.5 + 0.25 * math.sin(4 * math.pi * u), rot=2.2 * s)
    elif k == 'blast':
        sh = 0.04 * (1 - u) ** 2; im = view(src, 1.30 + 0.12 * (1 - u) ** 3, 0.5 + sh * math.sin(60 * u), 0.5 + sh * math.cos(53 * u))
    elif k == 'heartbeat':
        b = math.exp(-((u - 0.12) / 0.06) ** 2) + 0.6 * math.exp(-((u - 0.34) / 0.06) ** 2)
        im = view(src, 1.15 + 0.20 * b, 0.5, 0.5)
    elif k == 'fire':    im = view(src, 1.25 + 0.05 * s, 0.5, 0.55 + 0.05 * c)
    else:                im = view(src, 1.2, 0.5, 0.5)
    if k in ('fire', 'blast', 'missiles'):   # red ink flickers like flames (loop-safe: sum of integer harmonics)
        fl = 1 + 0.28 * math.sin(2 * math.pi * 3 * u) + 0.16 * math.sin(2 * math.pi * 7 * u + 1.3)
        a = np.asarray(im).astype(np.float32)
        red = (a[..., 0] > 140) & (a[..., 1] < 90)
        a[red] = np.clip(a[red] * [fl, 0.55 + 0.45 * fl, 0.55 + 0.45 * fl], 0, 255)
        im = Image.fromarray(a.astype(np.uint8))
    if k == 'blast' and u < 0.1:             # flash on each blast
        im = Image.blend(im, Image.new('RGB', im.size, (255, 255, 255)), 0.5 * (1 - u / 0.1))
    return im

ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'slow', '-crf', '14', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
                       'out/months_v4.mp4'], stdin=subprocess.PIPE)
for f in range(N):
    t = f / FPS; fr = base.copy()
    for i in range(12):
        tile = tile_at(i, t).convert('RGBA'); tile.alpha_composite(labels[i])
        ImageDraw.Draw(tile).rectangle([0, 0, TW - 1, TH - 1], outline=(240, 240, 240), width=2)
        r, c = divmod(i, 3); fr.paste(tile, (LEFT + c * (TW + GAP), TOP + r * (TH + GAP)), tile)
    ff.stdin.write(fr.tobytes())
ff.stdin.close(); ff.wait()
print('ok out/months_v4.mp4')
