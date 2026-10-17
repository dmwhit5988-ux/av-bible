"""Render Exodus 25 and 27 as per-verse vector SVGs, with Exodus 26's
renderer (generate_exodus26_svg.render_verse_svg).

All three tabernacle chapters share generate_tabernacle.py's drawing code and
CHAPTERS spec, so render_verse_svg — which runs those draw functions against
SvgLayer and wraps the highlight overlay in one breathing-glow group — draws
25 and 27 with no drawing logic of its own.

The one thing render_verse_svg does not carry is the pair of court-dimension
labels on 27:18 (DIM_LABELS); they are added here, static at full highlight,
the way render_verse_svg draws the other plan labels.

Run inside the project venv:
    .venv\\Scripts\\python.exe generate_exodus2527_svg.py
"""

import os

from generate_exodus26_svg import render_verse_svg
from generate_tabernacle import CHAPTERS, DIM_LABELS, cub, F_DIM, HL, out_path


def render(chapter, verse):
    c = render_verse_svg(chapter, verse)
    # 27:18 alone adds the "100 cubits" / "50 cubits" court-dimension labels
    # (they live outside the per-verse `labels` list, in DIM_LABELS).
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
