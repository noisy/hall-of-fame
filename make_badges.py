"""Generate badge candidates through fal, then clean them up.

Two lessons from xFuroo's badge are baked in:

  Never ask for a transparent background. The model paints the CHECKERBOARD
  that represents transparency straight into the image, including through the
  outer glow, where no colour test can separate it. Ask for flat white instead
  and key that - white is neutral and bright, the badge is cyan on near-black,
  so they separate cleanly.

  Say "spell every word exactly as written". Lettering is where these models
  fail, and naming the words explicitly is what got three correct lines first
  try last time.

    python3 make_badges.py            # all five
    python3 make_badges.py 1 4        # just those
"""
import importlib.util
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "badges", "swisstourist-drafts")
FAL = os.path.expanduser("~/life/brand/fal_assets.py")

STYLE = (
    "A circular achievement badge in a dark sci-fi HUD style. Deep navy face "
    "(#02060c) with a faint blueprint grid, glowing cyan line art (#3fd8ff), "
    "thin corner brackets like a heads-up display. Sharp vector lines, subtle "
    "inner glow, no gradients, no photo texture. The badge is a clean circle "
    "centred on a FLAT PURE WHITE background - solid white, no checkerboard, no "
    "transparency pattern, no shadow. Square image. Spell every word exactly as "
    "written."
)

# Each is one idea. A badge holds about three words; anything more is a
# certificate. Lines are his own, from what he said in chat tonight.
CANDIDATES = {
    "1-supervisor": (
        "In the centre, in large clean monospace capitals: 'CLAUDE'S "
        "SUPERVISOR'. Curved along the top edge, smaller: 'SWISSTOURIST'. Along "
        "the bottom edge, smaller still: 'SINCE MARCH 2026'. Above the centre "
        "text, a small icon of two nested chevrons pointing right, like a "
        "command prompt."),
    "2-tourist": (
        "In the centre, in large clean monospace capitals: 'THE TOURIST'. "
        "Curved along the top edge, smaller: 'SWISSTOURIST'. Along the bottom "
        "edge, smaller still: 'NEVER THE EXPECTED PATH'. Above the centre text, "
        "a small icon of a dotted route line that forks away from a straight "
        "line."),
    "3-king": (
        "In the centre, in large clean monospace capitals across two lines: "
        "'CODEX' then 'KING OF AI'. Curved along the top edge, smaller: "
        "'SWISSTOURIST'. Along the bottom edge, smaller still: 'DECLARED IN "
        "CHAT'. Above the centre text, a small simple crown drawn in thin cyan "
        "line art."),
    "4-yolo": (
        "In the centre, in large clean monospace lowercase: '--yolo'. Curved "
        "along the top edge, smaller: 'SWISSTOURIST'. Along the bottom edge, "
        "smaller still: 'AT START OR NOT AT ALL'. Above the centre text, a "
        "small icon of a terminal window with a blinking cursor block."),
    "5-save": (
        "In the centre, in large clean monospace capitals across two lines: "
        "'THE EMAIL' then 'SAVE'. Curved along the top edge, smaller: "
        "'SWISSTOURIST'. Along the bottom edge, smaller still: 'CAUGHT IT "
        "BEFORE IT WENT LIVE'. Above the centre text, a small icon of a shield "
        "with an envelope inside it."),
}

WHITE_SPREAD = 26        # max channel spread for "this is the white plate"
WHITE_FLOOR = 150        # and it has to be bright
RING_ALLOWANCE = 14      # the cyan rim sits outside the dark interior


def fal():
    spec = importlib.util.spec_from_file_location("fal_assets", FAL)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def cut_to_disc(path):
    """Drop the white plate and keep the badge disc.

    Locating the disc from its near-black interior rather than from the art as
    a whole: the outer glow blends into the plate, so anything that includes it
    drags plate pixels along with it.
    """
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(int)
    dark = a.max(axis=2) < 80
    if not dark.any():
        print(f"  ! {os.path.basename(path)}: no dark interior found, left as-is")
        return
    ys, xs = np.nonzero(dark)
    cx, cy = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2
    radius = max(xs.max() - xs.min(), ys.max() - ys.min()) / 2 + RING_ALLOWANCE

    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).ellipse([cx - radius, cy - radius,
                                  cx + radius, cy + radius], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(1.0))
    out = im.convert("RGBA")
    out.putalpha(mask)
    box = mask.point(lambda v: 255 if v > 40 else 0).getbbox()
    out.crop(box).resize((512, 512), Image.LANCZOS).save(path, optimize=True)
    print(f"  cleaned {os.path.basename(path)}  disc r={radius:.0f}")


def main():
    wanted = sys.argv[1:]
    os.makedirs(OUT, exist_ok=True)
    m = fal()
    for slug, idea in CANDIDATES.items():
        if wanted and not any(slug.startswith(w) for w in wanted):
            continue
        status, result = m.submit(m.PLATE_MODEL, {
            "prompt": f"{idea} {STYLE}", "aspect_ratio": "1:1",
            "resolution": "2K", "output_format": "png"})
        paths = m.save_images(m.await_result(status, result), OUT, slug)
        for path in paths:
            cut_to_disc(path)
    print("\ndrafts in", OUT)


if __name__ == "__main__":
    main()
