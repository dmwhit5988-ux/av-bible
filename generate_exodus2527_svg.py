"""Render Exodus 25 and 27 as per-verse vector SVGs, the vector twins of the
Exodus 26 conversion (generate_exodus26_svg.py).

All three tabernacle chapters share generate_tabernacle.py's drawing code and
CHAPTERS spec, so render_verse_svg — which runs those exact draw functions
against SvgLayer and wraps the highlight overlay in one breathing-glow group —
already produces faithful vectors for 25 and 27 with no new drawing logic.

The only chapter-27 special case the raster loop had that the shared
render_verse_svg does not carry is the pair of court-dimension labels drawn on
27:18 (DIM_LABELS); we add them here, static at full highlight, matching how
render_verse_svg draws the other plan captions.

Run inside the project venv:
    .venv\\Scripts\\python.exe generate_exodus2527_svg.py
"""

import os

from generate_exodus26_svg import render_verse_svg
from generate_tabernacle import CHAPTERS, DIM_LABELS, cub, F_DIM, HL, out_path


def render(chapter, verse):
    c = render_verse_svg(chapter, verse)
    # 27:18 alone adds the "100 cubits" / "50 cubits" court-dimension labels
    # (the raster generator drew these outside the per-verse `labels` list).
    if chapter == 27 and verse == 18:
        for text, x, y in DIM_LABELS:
            c.text(cub(x, y), text, F_DIM.size, HL, anchor="mm", bold=True)
    return c


def main():
    for chapter in (25, 27):
        total = 0
        for verse in sorted(CHAPTERS[chapter]):
            c = render(chapter, verse)
            out = out_path("Exodus", chapter, f"Exodus_{chapter}_{verse}.svg")
            c.save(out)
            total += os.path.getsize(out)
        print(f"Exodus {chapter}: {len(CHAPTERS[chapter])} SVG files, "
              f"{total/1e3:.0f} KB")


if __name__ == "__main__":
    main()
