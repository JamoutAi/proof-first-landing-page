#!/usr/bin/env python3
"""Build a silent session reel (15-20s) from moments in real recordings.

usage: python3 session_reel.py reel.json out.mp4 [--dur 2.8] [--fade 0.35]

reel.json:
[
  {"src": "/path/call-1.mp4", "start": 2280, "label": "Live call · the whole room, cameras on"},
  {"src": "/path/call-2.mp4", "start": 330,  "label": "We build a real app, live", "crop": [680, 210, 1600, 900]}
]
Each clip is cropped to 16:9 (auto-detects the non-black content area unless
"crop" is given as [x, y, w, h]), scaled to 1280x720 and joined with crossfades.
Prints the label start times for PAGE.reelLabels in the template.
Needs: ffmpeg, Pillow, numpy.
"""
import argparse
import json
import os
import subprocess
import tempfile

import numpy as np
from PIL import Image


def content_crop(src, t, tmp):
    frame = os.path.join(tmp, f"f{abs(hash((src, t)))}.png")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", src, "-frames:v", "1", frame],
                   stdin=subprocess.DEVNULL, check=True)
    a = np.asarray(Image.open(frame).convert("L")).astype(int)
    h, w = a.shape
    cols = np.where((a > 30).mean(axis=0) > 0.12)[0]
    rows = np.where((a > 30).mean(axis=1) > 0.12)[0]
    if not len(cols) or not len(rows):
        return 0, 0, w - w % 2, h - h % 2
    x0, x1, y0, y1 = cols.min(), cols.max() + 1, rows.min(), rows.max() + 1
    cw, ch = x1 - x0, y1 - y0
    nw, nh = (int(ch * 16 / 9), ch) if cw / ch > 16 / 9 else (cw, int(cw * 9 / 16))
    nx, ny = x0 + (cw - nw) // 2, y0 + (ch - nh) // 2
    return int(nx), int(ny), nw - nw % 2, nh - nh % 2


def main():
    p = argparse.ArgumentParser()
    p.add_argument("config")
    p.add_argument("out")
    p.add_argument("--dur", type=float, default=2.8)
    p.add_argument("--fade", type=float, default=0.35)
    p.add_argument("--crf", type=int, default=27)
    args = p.parse_args()

    clips = json.load(open(args.config))
    tmp = tempfile.mkdtemp()
    cmd = ["ffmpeg", "-v", "error", "-y"]
    filters = []
    for i, c in enumerate(clips):
        x, y, w, h = c.get("crop") or content_crop(c["src"], c["start"], tmp)
        cmd += ["-ss", str(c["start"]), "-t", str(args.dur), "-i", c["src"]]
        filters.append(f"[{i}:v]crop={w}:{h}:{x}:{y},scale=1280:720,setsar=1,fps=30,format=yuv420p[c{i}]")
    prev, offset = "c0", args.dur - args.fade
    for i in range(1, len(clips)):
        filters.append(f"[{prev}][c{i}]xfade=transition=fade:duration={args.fade}:offset={offset:.2f}[x{i}]")
        prev, offset = f"x{i}", offset + args.dur - args.fade
    cmd += ["-filter_complex", ";".join(filters), "-map", f"[{prev}]", "-an",
            "-c:v", "libx264", "-preset", "slow", "-crf", str(args.crf), "-profile:v", "high",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart", args.out]
    subprocess.run(cmd, stdin=subprocess.DEVNULL, check=True)

    starts = [round(i * (args.dur - args.fade), 2) for i in range(len(clips))]
    labels = [[s, c.get("label", "")] for s, c in zip(starts, clips)]
    total = args.dur * len(clips) - args.fade * (len(clips) - 1)
    print(f"wrote {args.out} ({total:.1f}s)")
    print("PAGE.reelLabels =", json.dumps(labels, ensure_ascii=False))
    print(f'poster: ffmpeg -ss 0.6 -i {args.out} -frames:v 1 -q:v 4 reel-poster.jpg')


if __name__ == "__main__":
    main()
