# Media recipes

Exact commands for the media work. Required: Python 3 with Pillow and numpy, and ffmpeg. Optional: macOS 14+ (for Apple Vision cutouts), faster-whisper (for transcripts and captions), Google Chrome (for screenshots), Node 22+ (for the phone check).

Keep downloaded or untrusted files in their own folder, and run scripts from a different folder.

## Contents
1. Contact sheets
2. HEIC and other formats
3. Cutouts of the founder
4. Web image export
5. Logos to one ink color
6. Video trims, posters and size
7. Transcripts and captions
8. Session reel
9. Screenshots of public pages
10. Local preview

---

## 1. Contact sheets
```bash
ls photos/*.{jpg,png,heic} > list.txt
python3 scripts/contact_sheet.py sheet.jpg 6 260 list.txt   # out, columns, thumb px, list
```
The script prints `number filename` pairs. Look at the image, then choose by number.

## 2. HEIC and other formats
On macOS, `sips -s format png in.heic --out out.png` converts the file. The contact sheet script already does this for HEIC, WEBP and GIF.

## 3. Cutouts of the founder
Best results come from a photo on a plain background (white seamless, solid color backdrop).

```bash
swiftc -O scripts/cutout.swift -o /tmp/cutout        # macOS 14+, compile once
/tmp/cutout photo.jpg cutout.png                       # writes a transparent PNG
```
Without macOS, use `pip install rembg` and then `rembg i photo.jpg cutout.png`, or ask the owner for a transparent PNG.

Then check the result. Composite it on the brand color and on the page background, and look at the hair edges.
- A thin halo of the old background color is invisible on a matching backdrop. On cream it shows, so keep cutouts that came off an orange backdrop on orange.
- If the cutout is flat-cut at the top of the head (the original photo cropped the hair), make the image a bit taller than its frame (`height:104%`, bottom-aligned). The arch's rounded top then crops the hair naturally.
- Crop to the alpha bounding box before exporting: `im.crop(im.getbbox())`.

## 4. Web image export
```python
from PIL import Image
im = Image.open(src).convert("RGB")          # keep RGBA for cutouts
im.thumbnail((900, 9999), Image.LANCZOS)     # width cap; hero cutouts ~1000-1200px tall
im.save("out.webp", "WEBP", quality=84, method=6)
```
Target sizes:
- Hero cutout: 100 to 180 KB.
- Section photos: 60 to 120 KB.
- Certificates and avatars: under 20 KB.

Always set `width` and `height` attributes on `img` tags so the page doesn't jump while loading. If CSS sets the width to 100%, also set `height:auto` or `aspect-ratio`. Otherwise the height attribute squishes the image.

## 5. Logos to one ink color
```bash
python3 scripts/logo_mono.py logos_in/ logos_out/ --ink "#3b2f27" --height 88
```
Each logo becomes a transparent PNG in a single ink color. Dark parts go solid, white parts go clear, and colored parts are pushed to full strength, so two-tone logos like purple and orange read evenly.

When the owner has a "logo bar" image (several logos in a row), slice it into separate logos. Find columns with ink, merge gaps under 25px, and crop each run. The script's `--split-bar` option does this.

In the marquee, logos have very different shapes, so set heights per logo: about 44px for round badges, 30 to 34px for wordmarks, and about 22px for very wide wordmarks.

## 6. Video trims, posters and size
Re-encode when trimming. Stream-copy cuts land on keyframes and can start seconds early.
```bash
ffmpeg -ss 397.6 -to 429.8 -i in.mov \
  -vf "scale=720:-2,fade=t=in:d=0.25,fade=t=out:st=31.8:d=0.4" \
  -af "afade=t=in:d=0.2,afade=t=out:st=31.6:d=0.6" \
  -c:v libx264 -preset slow -profile:v high -pix_fmt yuv420p -movflags +faststart -crf 25 \
  -c:a aac -b:a 96k clip.mp4
```
- Use crf 25 to 29 for talking heads. Aim for 2 to 7 MB per vertical clip under a minute.
- **Removing lines from the middle of a talk** (an outdated offer, for example):
  - Get word timestamps, then `trim`/`atrim` the segments and `concat` them.
  - Add `setsar=1` after `scale` on every segment, or concat fails.
  - Add a small punch-in (`crop=iw/1.1:ih/1.1,scale=...`) on alternate segments to hide the jump cuts.
  - Add 30 to 50ms audio fades at each cut so it doesn't click.
- **Poster frame:**
  - `ffmpeg -ss <t> -i clip.mp4 -frames:v 1 -q:v 4 poster.jpg`
  - Pick a frame with a smile, eyes open and no caption on screen. Make a contact sheet of 8 to 12 candidate frames.
- **Check faststart:** `ffprobe -v trace clip.mp4 2>&1 | grep -m2 -o "type:'\(moov\|mdat\)'"` should print `moov` before `mdat`.

## 7. Transcripts and captions
```bash
python3 scripts/make_vtt.py clip.mp4 > clip.vtt      # faster-whisper word timestamps -> WebVTT cues
```
- Read every cue. Speech recognition mishears openings ("Love it or hate it" came out as "Well, I better hate it"), names and brand words. Fix them by hand.
- Skip the caption track when captions are already burned into the video. Two sets of captions look broken.
- Also use transcripts to choose clean in and out points: start on the first word of a complete thought, and end before the interviewer reacts.

## 8. Session reel
A silent 15 to 20 second loop of real moments, cropped to fill 16:9 with no black bars.
```bash
python3 scripts/session_reel.py reel.json reel.mp4    # prints label timings for the template
```
`reel.json` holds a list of clips: `{"src": "...", "start": 2280, "label": "Live call · the whole room, cameras on", "crop": [x, y, w, h]}`. The `crop` is optional; leave it out to auto-detect the non-black content area.
- Each clip runs 2.8 seconds, with 0.35 second crossfades between clips.
- Pick a mix: a full gallery of faces, a "today we're building X live" slide, a member demo slide, and the end-of-call gallery.
- Crop out anything stale, like an old "Try it free" button in a corner.

## 9. Screenshots of public pages
Logged-out, retina, no admin buttons:
```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu \
  --hide-scrollbars --user-data-dir=/tmp/chrome-shot --window-size=1280,1500 \
  --force-device-scale-factor=2 --virtual-time-budget=20000 \
  --screenshot=about.png "https://example.com/community/about"
```
Crop with Pillow to the header and stats block, and separately to the reviews block. Export as webp at 1000 to 1400px wide.

## 10. Local preview
`python3 -m http.server 8000` in the site folder is enough. Python's simple server can't skip ahead within a video (it doesn't support range requests), so seeking won't work locally even though it works on real hosts.
