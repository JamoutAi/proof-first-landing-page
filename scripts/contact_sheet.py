#!/usr/bin/env python3
"""Make a numbered contact sheet so you can actually look at photos or video frames.

usage: python3 contact_sheet.py OUT.jpg COLUMNS THUMB_PX LIST.txt
LIST.txt holds one image path per line. Prints "number  filename" for each tile.
HEIC/WEBP/GIF/SVG are converted with macOS `sips` when Pillow can't open them.
"""
import math
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont, ImageOps


def load(path, tmpdir):
    try:
        im = Image.open(path)
        im.load()
    except Exception:
        out = os.path.join(tmpdir, f"{abs(hash(path))}.png")
        subprocess.run(["sips", "-s", "format", "png", path, "--out", out], capture_output=True)
        im = Image.open(out)
    im = ImageOps.exif_transpose(im)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGBA", im.size, (235, 235, 235, 255))
        bg.alpha_composite(im)
        im = bg
    return im.convert("RGB")


def main():
    if len(sys.argv) != 5:
        sys.exit(__doc__)
    out, cols, thumb, listfile = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    files = [l.strip() for l in open(listfile) if l.strip()]
    if not files:
        sys.exit("list is empty")
    rows = math.ceil(len(files) / cols)
    label_h = 22
    sheet = Image.new("RGB", (cols * thumb, rows * (thumb + label_h)), "white")
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 15)
    except Exception:
        font = ImageFont.load_default()
    tmpdir = tempfile.mkdtemp()
    for i, path in enumerate(files):
        x, y = (i % cols) * thumb, (i // cols) * (thumb + label_h)
        try:
            im = load(path, tmpdir)
            im.thumbnail((thumb - 6, thumb - 6))
            sheet.paste(im, (x + (thumb - im.width) // 2, y + (thumb - im.height) // 2))
        except Exception as exc:  # keep going; one bad file shouldn't stop the sheet
            print(f"ERR {i + 1} {path}: {exc}", file=sys.stderr)
        draw.text((x + 4, y + thumb + 2), str(i + 1), fill="red", font=font)
    sheet.save(out, quality=82)
    for i, path in enumerate(files):
        print(i + 1, os.path.basename(path))


if __name__ == "__main__":
    main()
