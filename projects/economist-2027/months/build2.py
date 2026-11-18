"""12-month Short v2 (10 s, 1080x1920, silent): the cover, then each month FULL SCREEN with a snap zoom (sharp, large
details), then the 12-month grid with the question. Source: the sharpened cover (cover_flat_4k.png, 4020x3960).
Usage: python3 build2.py -> out/months_v2.mp4 (needs out/ from build.py's tiles: it imports nothing, self-contained)."""
import subprocess
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

FPS, DUR, W, H = 30, 10.0, 1080, 1920
BG = (242, 236, 232)
cover = Image.open('cover_flat_4k.png').convert('RGB')
CW, CH = cover.size

def region(cx, cy, h):
    """Portrait 9:16 crop centred on (cx, cy), padded with the paper colour outside the cover."""
    w = round(h * 9 / 16); x0, y0 = round(cx - w / 2), round(cy - h / 2)
    im = Image.new('RGB', (w, h), BG)
    sx0, sy0, sx1, sy1 = max(x0, 0), max(y0, 0), min(x0 + w, CW), min(y0 + h, CH)
    im.paste(cover.crop((sx0, sy0, sx1, sy1)), (sx0 - x0, sy0 - y0))
    return im

# month centres in cover pixels and crop height (smaller = closer)
MONTHS = [(870, 640, 1500),    # Jan: satellite, astronaut, rocket
          (1420, 560, 1500),   # Feb: mountain, handshake
          (1960, 420, 1400),   # Mar: the leaders lined up
          (2850, 640, 1500),   # Apr: plane, camel rider
          (520, 1640, 1600),   # May: flag, crowd, fire, deer
          (1640, 1300, 1500),  # Jun: bank, men in suits, car
          (2420, 1520, 1500),  # Jul: crash chart, coins, statue
          (3300, 1300, 1500),  # Aug: rider, Kremlin
          (700, 2460, 1600),   # Sep: missiles, fire
          (1960, 2800, 1500),  # Oct: tanks, explosion
          (1820, 1960, 1500),  # Nov: AI brain, syringe, lab
          (3150, 2860, 1600)]  # Dec: warships, red sea
full = [region(*m) for m in MONTHS]
big = [Image.open(f'ov/big{i}.png').convert('RGBA') for i in range(12)]
title = Image.open('ov/title.png').convert('RGBA')
question = Image.open('ov/question.png').convert('RGBA')
grid_tiles = []
TW, TH, GAP, LEFT, TOP = 336, 271, 12, 24, 540
CROPS = [(440, 330, 780), (1120, 300, 980), (1580, -140, 900), (2160, 240, 1120), (60, 1080, 1020), (1180, 760, 1100),
         (1920, 860, 1100), (2860, 1060, 1040), (60, 2060, 1060), (1300, 2440, 1240), (1320, 1600, 1020), (2480, 2300, 1140)]
labels = [Image.open(f'ov/label{i}.png').convert('RGBA') for i in range(12)]
for i, (x, y, w) in enumerate(CROPS):
    h = round(w * TH / TW); src = Image.new('RGB', (w, h), BG)
    src.paste(cover.crop((x, max(y, 0), x + w, y + h)), (0, max(-y, 0)))
    t = src.resize((TW, TH), Image.LANCZOS).convert('RGBA'); t.alpha_composite(labels[i])
    ImageDraw.Draw(t).rectangle([0, 0, TW - 1, TH - 1], outline=(240, 240, 240), width=2); grid_tiles.append(t)
whole = cover.resize((1060, round(1060 * CH / CW)), Image.LANCZOS)
bgblur = ImageEnhance.Brightness(cover.resize((1960, 1930)).filter(ImageFilter.GaussianBlur(18))).enhance(0.22)

def clamp(v): return max(0.0, min(1.0, v))
def ease_out(t): return 1 - (1 - t) ** 3

INTRO, PER, GRID = 1.0, 0.62, 1.0 + 12 * 0.62     # grid starts at 8.44 s
ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'slow', '-crf', '14', '-tune', 'animation', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
                       'out/months_v2.mp4'], stdin=subprocess.PIPE)
for f in range(int(FPS * DUR)):
    t = f / FPS
    if t < INTRO:                       # the whole cover, pushing in, title on top
        fr = Image.new('RGB', (W, H), (11, 11, 11)); fr.paste(bgblur, (-440, -5))
        z = 1 + 0.08 * ease_out(clamp(t / INTRO)); im = whole.resize((round(1060 * z), round(whole.height * z)), Image.LANCZOS)
        fr.paste(im, ((W - im.width) // 2, 560 + (whole.height - im.height) // 2))
        a = clamp(t / 0.35); tl = title.copy(); tl.putalpha(tl.split()[-1].point(lambda v: int(v * a))); fr.paste(tl, (0, 0), tl)
    elif t < GRID:                      # one month, full screen: snap zoom 1.25 -> 1.0, then slow push
        i = int((t - INTRO) / PER); lt = t - INTRO - i * PER
        z = 1.25 - 0.25 * ease_out(clamp(lt / 0.18)) + 0.0 - 0.04 * clamp(lt / PER)
        src = full[i]; cw, ch = round(src.width / max(z, 0.96) / 1.04), round(src.height / max(z, 0.96) / 1.04)
        ox, oy = (src.width - cw) // 2, (src.height - ch) // 2
        fr = src.crop((ox, oy, ox + cw, oy + ch)).resize((W, H), Image.LANCZOS)
        if lt < 0.08:                   # white flash on the cut
            fr = Image.blend(fr, Image.new('RGB', (W, H), (255, 255, 255)), 0.55 * (1 - lt / 0.08))
        fr = fr.convert('RGBA'); grad = Image.new('RGBA', (W, 520), (0, 0, 0, 0)); gd = ImageDraw.Draw(grad)
        for y in range(520): gd.line([(0, y), (W, y)], fill=(0, 0, 0, int(150 * (1 - y / 520))))
        fr.alpha_composite(grad, (0, 0)); fr.alpha_composite(big[i], (0, 200 - int(40 * (1 - ease_out(clamp(lt / 0.15))))))
        fr = fr.convert('RGB')
    else:                               # the 12-month grid, tiles snapping in fast, then the question
        fr = Image.new('RGB', (W, H), (11, 11, 11)); fr.paste(bgblur, (-440, -5)); fr.paste(title, (0, 0), title)
        gt = t - GRID
        for i in range(12):
            if gt < i * 0.04: continue
            r, c = divmod(i, 3); fr.paste(grid_tiles[i], (LEFT + c * (TW + GAP), TOP + r * (TH + GAP)), grid_tiles[i])
        q = clamp((gt - 0.35) / 0.3)
        if q > 0: fr.paste(question, (0, 1660 + int(260 * (1 - ease_out(q)))), question)
    ff.stdin.write(fr.tobytes())
ff.stdin.close(); ff.wait()
print('ok out/months_v2.mp4')
