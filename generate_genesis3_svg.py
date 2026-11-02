"""Render Genesis 3 (the serpent on the bough, one fruit from hand to hand, and the two of them
walking east out of the garden) as per-verse vector SVGs.

The chapter plays on the ground Genesis 2 built, from that chapter's last frame, under the same
camera. genesis3_garden.py is the story, a function a verse; garden_stage.py the stage, the build
and, through garden_qc.py, what must be clear before anything is written; garden_art.py the place.
The two chapters are written together, since a change to either can move the other: this writes
Genesis 2's files too, as generate_genesis2_svg.py writes these (garden_stage.write_story).

Run inside the project venv:
    .venv\\Scripts\\python.exe generate_genesis3_svg.py
"""

import sys


def main():
    import garden_stage
    if not garden_stage.write_story():
        sys.exit(1)


if __name__ == "__main__":
    main()
