"""Contact sheets from snap frames: python3 tools/sheet.py <dir>"""
import glob, os, sys
from PIL import Image
d = sys.argv[1]
fs = sorted(glob.glob(d + '/f_*.jpg'), key=lambda f: float(os.path.basename(f)[2:-4]))
for k in range(0, len(fs), 9):
    g = fs[k:k + 9]; im = Image.new('RGB', (9 * 270, 480))
    for i, f in enumerate(g): im.paste(Image.open(f).resize((270, 480)), (i * 270, 0))
    im.save(f'{d}/sheet{k // 9}.jpg')
