"""Render 1 Chronicles 1-9 as a camera over the one welded family tree.

Supersedes generate_1chronicles_svg.py, which drew each chapter as its own
world of side-by-side scenes. Same verse matching, same file names; the world
underneath is now `chronicles_tree.py`'s single Adam-rooted tree, so a name
read in chapter 2 is still standing when chapter 4 comes back to it.

    python generate_1chronicles_tree_svg.py            # write all 407
    python generate_1chronicles_tree_svg.py --dry      # size report only
    python generate_1chronicles_tree_svg.py --only 2   # one chapter
    python generate_1chronicles_tree_svg.py --out DIR  # somewhere else
    python generate_1chronicles_tree_svg.py --spine     # the layout tried
                                                        # and rejected here

Existing files are backed up to backups/1_Chronicles_svg_v2_camera/ the first
time this writes over them.
"""

import os
import shutil
import sys

from generate_1chronicles import BOOK, CHAPTERS, coverage_check
from generate_tabernacle import out_path
from svg_chronicles_world import VerseFrame, World

REPO = os.path.dirname(os.path.abspath(__file__))
BACKUP = os.path.join(REPO, "backups", "1_Chronicles_svg_v2_camera")


def back_up_once():
    """Keep the previous family before overwriting it (project convention —
    the column renderer it replaced is in backups/ too)."""
    if os.path.isdir(BACKUP):
        return False
    src = os.path.join(REPO, "visuals", "1_Chronicles")
    if not os.path.isdir(src):
        return False
    shutil.copytree(src, BACKUP)
    return True


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

    if not dry and out_dir is None and back_up_once():
        print(f"backed up the previous family to {BACKUP}")

    frame = VerseFrame(world)
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
            n = len(c.svg() if hasattr(c, "svg") else "")
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
