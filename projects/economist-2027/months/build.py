"""12-month grid Short (10 s, 1080x1920, no audio: the owner adds music from YouTube's library in the app).
Each month is a crop of the sharpened cover; tiles pop in one by one, then a highlight runs through the months
and the question card slides up. Usage: python3 build.py [cover_flat_4k.png] -> out/months.mp4"""
import math, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

FPS, DUR, W, H = 30, 10.0, 1080, 1920
SRC = sys.argv[1] if len(sys.argv) > 1 else 'cover_flat_4k.png'
cover = Image.open(SRC).convert('RGB')                      # 4020x3960
TW, TH, GAP, LEFT, TOP = 336, 271, 12, 24, 540
# month -> crop (x, y, w) in cover pixels; height follows the tile ratio
CROPS = [(440, 330, 780),    # Jan: satellite, astronaut, rocket
         (1120, 300, 980),   # Feb: mountain, handshake, radio tower
         (1580, -140, 900),  # Mar: the leaders lined up (padded above)
         (2160, 240, 1120),  # Apr: plane, camel rider
         (60, 1080, 1020),   # May: flag, crowd, fire, deer
         (1180, 760, 1100),  # Jun: bank, men in suits, car
         (1920, 860, 1100),  # Jul: crash chart, coins, statue
         (2860, 1060, 1040), # Aug: rider, Kremlin
         (60, 2060, 1060),   # Sep: missiles, fire
         (1300, 2440, 1240), # Oct: tanks, explosion
         (1320, 1600, 1020), # Nov: AI brain, syringe, lab
         (2480, 2300, 1140)] # Dec: warships, red sea
tiles = []
for (x, y, w) in CROPS:
    h = round(w * TH / TW)
    src = Image.new('RGB', (w, h), (242, 236, 232)); src.paste(cover.crop((x, max(y, 0), x + w, y + h)), (0, max(-y, 0)))
    tiles.append(src.resize((round(TW * 1.12), round(TH * 1.12)), Image.LANCZOS))
labels = [Image.open(f'ov/label{i}.png').convert('RGBA') for i in range(12)]
title = Image.open('ov/title.png').convert('RGBA')
question = Image.open('ov/question.png').convert('RGBA')
bg = ImageEnhance.Brightness(cover.resize((1960, 1930)).filter(ImageFilter.GaussianBlur(18))).enhance(0.22)

def pos(i):
    r, c = divmod(i, 3)
    return LEFT + c * (TW + GAP), TOP + r * (TH + GAP)

def ease_back(t):  # overshoot pop
    c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2

def clamp(v): return max(0.0, min(1.0, v))

POP0, STEP, POPD = 0.55, 0.40, 0.28           # tile i pops at POP0 + i*STEP
HL0, HLD = 5.75, 0.27                          # highlight run: one month every HLD seconds
Q0 = 6.2
ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
                       '-i', '-', '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
                       'out/months.mp4'], stdin=subprocess.PIPE)
for f in range(int(FPS * DUR)):
    t = f / FPS
    fr = Image.new('RGB', (W, H), (11, 11, 11))
    # slow drifting blurred cover behind everything
    dx = int(-200 + 120 * t / DUR); fr.paste(bg, (dx - 240, -5))
    # title: slides down + fades in during the first 0.5 s
    a = clamp(t / 0.5); tl = title.copy(); tl.putalpha(tl.split()[-1].point(lambda v: int(v * a)))
    fr.paste(tl, (0, int(-30 * (1 - a))), tl)
    hl = int((t - HL0) / HLD) if t >= HL0 else -1
    for i in range(12):
        p = (t - (POP0 + i * STEP)) / POPD
        if p <= 0: continue
        s = ease_back(clamp(p)) if p < 1 else 1.0
        # Ken Burns inside the tile: 1.12 -> 1.0 crop window drift
        z = 1 + 0.12 * (1 - clamp((t - POP0 - i * STEP) / 6.0))
        src = tiles[i]; cw, ch = round(TW * z), round(TH * z)
        ox = (src.width - cw) // 2; oy = (src.height - ch) // 2
        tile = src.crop((ox, oy, ox + cw, oy + ch)).resize((TW, TH), Image.LANCZOS).convert('RGBA')
        tile.alpha_composite(labels[i], (0, 0))
        d = ImageDraw.Draw(tile)
        if p < 1.6:   # white flash on arrival
            fl = Image.new('RGBA', (TW, TH), (255, 255, 255, int(200 * clamp(1 - p / 1.6) ** 2))); tile.alpha_composite(fl)
        if 0 <= hl and (hl % 12) == i and t < HL0 + 12 * HLD + 0.6:
            d.rectangle([0, 0, TW - 1, TH - 1], outline=(227, 18, 11), width=9)
        else:
            d.rectangle([0, 0, TW - 1, TH - 1], outline=(240, 240, 240), width=2)
        if s != 1.0:
            tw, th = max(1, round(TW * s)), max(1, round(TH * s)); tile = tile.resize((tw, th), Image.LANCZOS)
        x, y = pos(i); fr.paste(tile, (x + (TW - tile.width) // 2, y + (TH - tile.height) // 2), tile)
    if t >= Q0:   # question slides up from the bottom
        q = clamp((t - Q0) / 0.35); qy = 1660 + int(260 * (1 - ease_back(q) if q < 1 else 0))
        fr.paste(question, (0, qy), question)
    ff.stdin.write(fr.tobytes())
ff.stdin.close(); ff.wait()
print('ok out/months.mp4')
