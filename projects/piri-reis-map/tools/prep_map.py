"""Turn the scan's white surround into the dark ground, so camera moves never show white.
Usage: python3 tools/prep_map.py <scan.jpg> hf/assets/piri_map.jpg"""
import sys
from PIL import Image, ImageDraw, ImageFilter
src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert('RGB')
w, h = im.size
key = (255, 0, 255)
step = max(1, w // 40)
for x in list(range(0, w, step)) + [w - 1]:
    for y in (0, h - 1):
        if sum(im.getpixel((x, y))) > 600: ImageDraw.floodfill(im, (x, y), key, thresh=60)
for y in list(range(0, h, step)) + [h - 1]:
    for x in (0, w - 1):
        if sum(im.getpixel((x, y))) > 600: ImageDraw.floodfill(im, (x, y), key, thresh=60)
mask = Image.eval(im.split()[1], lambda g: 0).copy()
px = im.load(); mp = mask.load()
for y in range(h):
    for x in range(w):
        if px[x, y] == key: mp[x, y] = 255
mask = mask.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(max(1, w // 400)))
ground = Image.new('RGB', (w, h), (11, 15, 16))
Image.composite(ground, Image.open(src).convert('RGB'), mask).save(out, quality=92)
print(out, w, h)
