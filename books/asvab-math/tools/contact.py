"""Tile PDF page PNGs into contact sheets for visual review.

    python tools/contact.py build/pg 1 12 build/sheet.png [cols]
"""
import sys
from PIL import Image

prefix, first, last, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
cols = int(sys.argv[5]) if len(sys.argv) > 5 else 4
import glob
files = sorted(glob.glob(prefix + "-*.png"))
width = len(files[0].rsplit("-", 1)[1].split(".")[0])
pages = [Image.open(f"{prefix}-{i:0{width}d}.png") for i in range(first, last + 1)]
w, h = pages[0].size
rows = (len(pages) + cols - 1) // cols
sheet = Image.new("RGB", (cols * w + (cols - 1) * 6, rows * h + (rows - 1) * 6), (120, 120, 120))
for i, p in enumerate(pages):
    sheet.paste(p, ((i % cols) * (w + 6), (i // cols) * (h + 6)))
sheet.save(out)
print(out, sheet.size)
