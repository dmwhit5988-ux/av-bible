"""Render 1 Chronicles 1-9 as a camera over the one welded family tree.

The scenes and verse matching are `generate_1chronicles.py`'s; the world
underneath is `chronicles_tree.py`'s single Adam-rooted tree, drawn by
`svg_chronicles_world.py`, so a name read in chapter 2 is still standing when
chapter 4 comes back to it. (An earlier renderer drew each chapter as its own
world of side-by-side scenes; its output is archived as
backups/1_Chronicles_svg_v2_camera under config.ARCHIVE_DIR.)

    python generate_1chronicles_tree_svg.py            # write all 407
    python generate_1chronicles_tree_svg.py --dry      # size report only
    python generate_1chronicles_tree_svg.py --only 2   # one chapter
    python generate_1chronicles_tree_svg.py --out DIR  # somewhere else
    python generate_1chronicles_tree_svg.py --spine     # the layout tried
                                                        # and rejected here

It writes nothing if any of the lines that join a family
(`svg_family_lines`) would run behind a box; under --spine it only reports
them.
"""

import os
import sys

from generate_1chronicles import BOOK, CHAPTERS, coverage_check
from generate_tabernacle import out_path
from svg_chronicles_world import VerseFrame, World

def main(argv):
    dry = "--dry" in argv
    only = None
    if "--only" in argv:
        only = int(argv[argv.index("--only") + 1])
    out_dir = None
    if "--out" in argv:
        out_dir = argv[argv.index("--out") + 1]
        os.makedirs(out_dir, exist_ok=True)

    for ch, scenes in sorted(CHAPTERS.items()):
        coverage_check(ch, scenes)

    layout = "spine" if "--spine" in argv else None
    world = World(ot=True, layout=layout)
    x0, y0, x1, y1 = world.world_box
    named = sum(1 for n in world.nodes if n in world.first_of)
    print(f"world: {len(world.nodes)} nodes, {x1 - x0:.0f} x {y1 - y0:.0f} px")
    print(f"       {named} of them read by a verse of 1 Chr 1-9; "
          f"{len(world.nodes) - named} standing as context")

    frame = VerseFrame(world)
    if frame.lines_behind:
        print(f"family lines behind boxes: {len(frame.lines_behind)}")
        for s, n in frame.lines_behind[:12]:
            print(f"   the {s.role} of {s.fam.label}'s family, behind {n.label}")
        if layout is None:
            # the spine is only re-run for comparison, and leaves its rails
            # no gutter; the live layout must come out clean
            print("stopped: nothing written")
            return 1
    total = bytes_ = 0
    per_chapter = {}
    first = True
    for ch, v, scene in world.order:
        c = frame.render(ch, v, scene, first)
        first = False
        if only is not None and ch != only:
            continue
        name = f"1_Chronicles_{ch}_{v}.svg"
        if dry:
            n = len(c.tostring())
            bytes_ += n
            total += 1
            per_chapter[ch] = per_chapter.get(ch, 0) + 1
            continue
        path = (os.path.join(out_dir, name) if out_dir
                else out_path(BOOK, ch, name))
        c.save(path)
        bytes_ += os.path.getsize(path)
        total += 1
        per_chapter[ch] = per_chapter.get(ch, 0) + 1

    for ch in sorted(per_chapter):
        print(f"1 Chronicles {ch}: {per_chapter[ch]} files")
    print(f"TOTAL: {total} SVG files, {bytes_ / 1e6:.1f} MB "
          f"({bytes_ / max(total, 1) / 1e3:.0f} KB each)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
