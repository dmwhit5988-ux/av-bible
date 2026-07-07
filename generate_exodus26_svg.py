"""Render Exodus 26 as per-verse vector SVGs, reusing the tabernacle raster
generator's drawing code unchanged.

generate_tabernacle.py builds each verse from a dimmed courtyard plan plus a
detail inset, with the described part highlighted on a separate overlay whose
alpha breathes (pulse) and loops forever. Here we run those exact drawing
functions against SvgLayer (an ImageDraw stand-in), then compose:

    * base layer  -> static SVG (the plan + inset base shapes + chrome)
    * overlay     -> a <g> whose opacity oscillates 0.62..1.0 forever,
                     reproducing the pulse (every overlay element shared one
                     alpha in the raster loop, so one group animation suffices)

So the vectors are faithful to the raster art by construction — no drawing
logic is re-implemented — and stay crisp at any size.

Run inside the project venv:
    .venv\\Scripts\\python.exe generate_exodus26_svg.py
"""

import os

from svg_surface import SvgCanvas, SvgLayer
from generate_tabernacle import (W, H, BG, HL, cub, F_DIM, draw_plan,
                                 draw_chrome, INSETS, CHAPTERS, out_path)

# One pulse cycle ~= the raster loop (16 frames x 130 ms).
PULSE = (0.62, 1.0, "2.1s")


def render_verse_svg(chapter, verse):
    caption, highlights, inset, labels = CHAPTERS[chapter][verse]
    base, over = SvgLayer(), SvgLayer()

    # base image: dimmed plan (when an inset draws the detail) + chrome
    draw_plan(base, dim=bool(inset))
    draw_chrome(base, chapter, verse, caption)

    # inset base shapes -> base; the highlighted part + caption -> overlay
    if inset:
        name, part = inset
        INSETS[name](base, over, part, 1.0, 1.0)   # alpha=1, frac=1 (held)

    # plan highlights (tent walls, veil, ark, table, lamp) -> overlay
    for fn, kwargs, grows in highlights:
        fn(over, alpha=1.0, frac=1.0, **kwargs)

    # plan captions (vv34-35): full opacity, static (they never pulsed)
    for text, x, y in labels:
        base.text(cub(x, y), text, font=F_DIM, fill=HL, anchor="mm")

    c = SvgCanvas(W, H, bg=BG)
    c.raw(base.elements())
    with c.group(pulse=PULSE):
        c.raw(over.elements())
    return c


def main():
    total = 0
    for verse in sorted(CHAPTERS[26]):
        c = render_verse_svg(26, verse)
        out = out_path("Exodus", 26, f"Exodus_26_{verse}.svg")
        c.save(out)
        total += os.path.getsize(out)
    print(f"Exodus 26: {len(CHAPTERS[26])} SVG files, {total/1e3:.0f} KB")


if __name__ == "__main__":
    main()
