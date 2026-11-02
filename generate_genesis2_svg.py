"""Render Genesis 2 (the heavens finished, the bare ground, and the garden planted eastward in
Eden) as per-verse vector SVGs.

The chapter is one long stretch of ground under one camera: the man formed on Eden's dry shoulder,
walked east into a garden coming up round him, the river and its four heads on the plan, his plot
and its one shoot, the animals named, and the woman from his side. genesis2_garden.py is the story,
a function a verse; garden_stage.py the stage, the build and, through garden_qc.py, what must be
clear before anything is written; garden_art.py the place. Genesis 3 plays on from this chapter's
last frame, so the two are written together: this writes Genesis 3's files too, as
generate_genesis3_svg.py writes Genesis 2's (garden_stage.write_story).

This module also keeps the garden's palette, which Genesis 1 and Numbers 1-2 import. That is why
main() imports the stage inside the function: importing this stays cheap.

Run inside the project venv:
    .venv\\Scripts\\python.exe generate_genesis2_svg.py
"""

import sys

import svg_figures as F
from generate_tabernacle import BG, BROWN, GOLD, HL


GREEN = (86, 122, 78)          # garden foliage
GREEN_DIM = (52, 70, 50)
EARTH = (58, 48, 38)           # the ground the man is formed from


def _mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def garden_paint(lit, dead=False):
    """The garden's palette as a figure paint table: crown green, trunk
    brown, fruit gold. One geometry, the scene's own colours."""
    sheet = dict(F.palette(HL if lit else GREEN, BG))
    sheet["wood"] = (_mix(BG, BROWN, 0.62), GOLD if lit else BROWN, 1.4)
    sheet["fleece"] = (_mix(BG, EARTH if dead else GREEN, 0.55),
                       HL if lit else GREEN_DIM, 2.5 if lit else 1.5)
    sheet["fruit"] = (GOLD if lit else _mix(BG, GOLD, 0.75), GOLD, 1.0)
    return sheet


def main():
    import garden_stage
    if not garden_stage.write_story():
        sys.exit(1)


if __name__ == "__main__":
    main()
