"""Render the 1 Chronicles 1-9 genealogies as per-verse SVGs.

Scene data + verse matching live in generate_1chronicles.py; drawing lives
in svg_1chronicles_render.py. Files are translation-generic (WEB spellings):
visuals/1_Chronicles/<ch>/1_Chronicles_<ch>_<v>.svg

Run inside the project venv:
    .venv\\Scripts\\python.exe generate_1chronicles_svg.py [--check]

--check validates the scene data (coverage, matching) without writing.
Review the warnings it prints: a name row that never matches a verse is
drawn as always-read context (sometimes intended, e.g. repeated tree roots),
and a verse with no highlight shows the caption only (fine for narrative
asides, wrong for a name list).
"""

import os
import sys

from generate_tabernacle import out_path
from generate_1chronicles import (BOOK, CHAPTERS, assign, coverage_check,
                                  web_verses)
from svg_1chronicles_render import ChapterWorld


def audit(chapter, scenes):
    """Print data problems worth a human look."""
    texts = dict(web_verses(chapter))
    for scene in scenes:
        rows, first_read, highlights = assign(scene, texts)
        lo, hi = scene["verses"]
        unmatched = [r.label for r in rows
                     if not r.heading and r.index not in first_read]
        if unmatched:
            print(f"  ch{chapter} '{scene['title']}': context rows "
                  f"(never matched): {', '.join(unmatched)}")
        empty = [v for v in range(lo, hi + 1) if not highlights.get(v)]
        if empty:
            print(f"  ch{chapter} '{scene['title']}': no highlight in "
                  f"verses {empty}")


def main(check_only=False):
    grand_files = grand_bytes = 0
    for chapter, scenes in sorted(CHAPTERS.items()):
        coverage_check(chapter, scenes)
        audit(chapter, scenes)
        if check_only:
            continue
        texts = dict(web_verses(chapter))
        scene_data = [(scene,) + assign(scene, texts) for scene in scenes]
        world = ChapterWorld(chapter, scene_data)
        n_files = 0
        first = True
        for si, scene in enumerate(scenes):     # verse order — the camera
            lo, hi = scene["verses"]            # carries over between verses
            for v in range(lo, hi + 1):
                c = world.render_verse(si, v, texts[v], first)
                first = False
                out = out_path(BOOK, chapter,
                               f"1_Chronicles_{chapter}_{v}.svg")
                c.save(out)
                n_files += 1
                grand_bytes += os.path.getsize(out)
        grand_files += n_files
        print(f"1 Chronicles {chapter}: {n_files} files")
    if not check_only:
        print(f"TOTAL: {grand_files} SVG files, {grand_bytes/1e3:.0f} KB")


if __name__ == "__main__":
    main(check_only="--check" in sys.argv)
