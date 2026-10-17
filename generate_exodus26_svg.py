"""Render Exodus 26 as per-verse vector SVGs. render_verse_svg() here also
renders Exodus 25 and 27 (generate_exodus2527_svg.py).

generate_tabernacle.py holds the drawing: each verse is the courtyard plan,
plus a detail inset where the verse describes a part up close (the plan is
then dimmed), with the part the verse describes drawn on a separate
overlay. render_verse_svg() runs those draw functions against two SvgLayer
objects (svg_surface's ImageDraw-shaped layer), then composes:

    * base layer  -> static SVG (the plan and its labels, the inset's base
                     shapes, the title and the cubit scale)
    * overlay     -> one <g> whose opacity breathes 0.62..1.0 forever (SMIL),
                     so every highlighted element pulses together

Run inside the project venv:
    .venv\\Scripts\\python.exe generate_exodus26_svg.py
"""

import os

from svg_surface import SvgCanvas, SvgLayer
from generate_tabernacle import (W, H, BG, HL, cub, F_DIM, draw_plan,
                                 draw_chrome, INSETS, CHAPTERS, out_path)

# The overlay's breathing glow: (low opacity, high opacity, one cycle).
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

    # plan labels (26:34-35, and most of chapter 27): full opacity, on the
    # static base so they don't pulse
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
