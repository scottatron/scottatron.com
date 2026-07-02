# /// script
# requires-python = ">=3.11"
# dependencies = ["pillow"]
# ///
"""Square-crop a photo and render it as a teal/paper duotone for the CV masthead.

Usage: uv run scripts/duotone_portrait.py <input.jpeg> <output.jpg>
"""
import sys
from PIL import Image, ImageOps

SHADOW = (4, 38, 37)      # deep teal, near-black
MID = (0, 125, 121)       # --accent
HIGHLIGHT = (250, 249, 247)  # --paper
MID_POINT = 0.55          # where the accent sits in the tonal range

# crop tuning: fractions of source width/height
CENTER_X, CENTER_Y, SIDE = 0.48, 0.42, 0.78

src = Image.open(sys.argv[1])
src = ImageOps.exif_transpose(src)
w, h = src.size

side = int(SIDE * w)
cx, cy = int(CENTER_X * w), int(CENTER_Y * h)
box = (max(0, cx - side // 2), max(0, cy - side // 2))
box = (*box, min(w, box[0] + side), min(h, box[1] + side))
img = src.crop(box).resize((480, 480), Image.LANCZOS)

grey = ImageOps.autocontrast(img.convert('L'), cutoff=2)
mid_i = int(MID_POINT * 255)
lut = []
for channel in range(3):
    lo, mid, hi = SHADOW[channel], MID[channel], HIGHLIGHT[channel]
    for i in range(256):
        if i <= mid_i:
            lut.append(lo + (mid - lo) * i // mid_i)
        else:
            lut.append(mid + (hi - mid) * (i - mid_i) // (255 - mid_i))
duo = grey.convert('RGB').point(lut)
duo.save(sys.argv[2], quality=88)
print(f'wrote {sys.argv[2]} from crop {box} of {w}x{h}')
