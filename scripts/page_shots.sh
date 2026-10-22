#!/usr/bin/env bash
# Full-page screenshots for owner review: one desktop image (1440 wide) and a
# true 390px phone render split into readable parts.
#
#   bash page_shots.sh "http://localhost:8000/index.html" shots/
#
# Headless Chrome won't render narrower than ~500px, so the phone view is drawn
# inside a 390px iframe. That frame is taller than the page, so the sticky phone
# bar never appears here: check it with phone_check.mjs.
# Needs Google Chrome, Python 3 with Pillow + numpy.
set -euo pipefail
URL="$1"; OUT="${2:-shots}"; mkdir -p "$OUT"
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
PROFILE="$(mktemp -d)"
FRAME="$OUT/.phone-frame.html"

"$CHROME" --headless=new --disable-gpu --hide-scrollbars --no-first-run --no-default-browser-check \
  --user-data-dir="$PROFILE" --window-size=1440,16000 --virtual-time-budget=15000 \
  --screenshot="$OUT/.desktop-raw.png" "$URL" >/dev/null 2>&1

cat > "$FRAME" <<EOF
<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;background:#fff}iframe{display:block;width:390px;height:22000px;border:0}</style></head>
<body><iframe src="$URL"></iframe></body></html>
EOF
"$CHROME" --headless=new --disable-gpu --hide-scrollbars --no-first-run --no-default-browser-check \
  --user-data-dir="$PROFILE" --window-size=600,22000 --force-device-scale-factor=2 --virtual-time-budget=20000 \
  --screenshot="$OUT/.phone-raw.png" "file://$(cd "$(dirname "$FRAME")" && pwd)/$(basename "$FRAME")" >/dev/null 2>&1

python3 - "$OUT" <<'PY'
import sys
import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
out = sys.argv[1]

def trim(im, ignore_bottom=0):
    """Cut the empty page background below the footer (ignore a fixed bar at the bottom)."""
    a = np.asarray(im).astype(int)
    a = a[:-ignore_bottom] if ignore_bottom else a
    bg = a[-1, a.shape[1] // 2]
    rows = np.where((np.abs(a - bg).sum(axis=2) > 12).mean(axis=1) > 0.002)[0]
    return im.crop((0, 0, im.width, min(int(rows.max()) + 60, im.height)))

d = trim(Image.open(f"{out}/.desktop-raw.png").convert("RGB"))
d = d.resize((1100, round(d.height * 1100 / d.width)), Image.LANCZOS)
d.save(f"{out}/desktop.jpg", quality=84, optimize=True)
print(f"{out}/desktop.jpg", d.size)

p = Image.open(f"{out}/.phone-raw.png").convert("RGB").crop((0, 0, 780, 44000))
p = trim(p, ignore_bottom=400)          # the sticky phone bar sits at the bottom of the frame
n = max(1, -(-p.height // 7000))
step = -(-p.height // n)
for i in range(n):
    part = p.crop((0, i * step, 780, min((i + 1) * step, p.height)))
    part.save(f"{out}/phone-{i + 1}.jpg", quality=84, optimize=True)
    print(f"{out}/phone-{i + 1}.jpg", part.size)
PY
rm -rf "$PROFILE" "$OUT/.desktop-raw.png" "$OUT/.phone-raw.png" "$FRAME"
