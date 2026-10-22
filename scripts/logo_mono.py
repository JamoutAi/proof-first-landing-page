#!/usr/bin/env python3
"""Recolor logos to one ink color so a logo strip looks designed, not pasted.

usage:
  python3 logo_mono.py IN_DIR OUT_DIR [--ink "#3b2f27"] [--height 88]
  python3 logo_mono.py BAR.png OUT_DIR --split-bar [--ink ...] [--height ...]

Dark pixels become solid ink, white/background becomes transparent, colored
parts are pushed to full strength (so two-tone logos read evenly).
--split-bar slices one wide "logo bar" image into separate logos (logo-1.png ...).
"""
import argparse
import os

import numpy as np
from PIL import Image


def to_mono(im, ink, height):
    a = np.asarray(im.convert("RGBA")).astype(float)
    lum = 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]
    dark = np.clip((250 - lum) / 250, 0, 1) * (a[:, :, 3] / 255)
    alpha = np.clip((dark - 0.04) / 0.36, 0, 1)
    out = np.zeros(a.shape, dtype=np.uint8)
    out[:, :, 0:3] = ink
    out[:, :, 3] = (alpha * 255).astype(np.uint8)
    img = Image.fromarray(out)
    box = img.getbbox()
    if not box:
        return None
    img = img.crop(box)
    w = round(img.width * height / img.height)
    return img.resize((w, height), Image.LANCZOS)


def split_bar(im, gap=25):
    a = np.asarray(im.convert("RGBA")).astype(int)
    ink = (a[:, :, 3] > 40) & ((a[:, :, 0] + a[:, :, 1] + a[:, :, 2]) < 690)
    cols = ink.any(axis=0)
    runs, start = [], None
    for x, c in enumerate(cols):
        if c and start is None:
            start = x
        if not c and start is not None:
            runs.append([start, x])
            start = None
    if start is not None:
        runs.append([start, len(cols)])
    merged = []
    for r in runs:
        if merged and r[0] - merged[-1][1] < gap:
            merged[-1][1] = r[1]
        else:
            merged.append(r)
    return [im.crop((max(x0 - 4, 0), 0, min(x1 + 4, im.width), im.height)) for x0, x1 in merged]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("src")
    p.add_argument("out_dir")
    p.add_argument("--ink", default="#3b2f27")
    p.add_argument("--height", type=int, default=88)
    p.add_argument("--split-bar", action="store_true")
    args = p.parse_args()
    ink = np.array([int(args.ink[i:i + 2], 16) for i in (1, 3, 5)])
    os.makedirs(args.out_dir, exist_ok=True)

    if args.split_bar:
        items = [(f"logo-{i + 1}", im) for i, im in enumerate(split_bar(Image.open(args.src)))]
    else:
        items = []
        for name in sorted(os.listdir(args.src)):
            if name.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                items.append((os.path.splitext(name)[0], Image.open(os.path.join(args.src, name))))

    for name, im in items:
        mono = to_mono(im, ink, args.height)
        if mono is None:
            print("skipped (empty):", name)
            continue
        path = os.path.join(args.out_dir, name + ".png")
        mono.save(path, optimize=True)
        print(path, mono.size)


if __name__ == "__main__":
    main()
