"""Render 1 Chronicles 1-9 as a camera over the one welded family tree.

The scenes and verse matching are `generate_1chronicles.py`'s; the world
underneath is `chronicles_tree.py`'s single Adam-rooted tree, laid out in
regions (`layout_regions.py`) and drawn by `svg_chronicles_world.py`, so a
name read in chapter 2 is still standing when chapter 4 comes back to it.
(An earlier renderer drew each chapter as its own world of side-by-side
scenes; its output is archived as backups/1_Chronicles_svg_v2_camera under
config.ARCHIVE_DIR.)

    python generate_1chronicles_tree_svg.py            # write all 407
    python generate_1chronicles_tree_svg.py --dry      # size report only
    python generate_1chronicles_tree_svg.py --only 2   # one chapter
    python generate_1chronicles_tree_svg.py --out DIR  # somewhere else
    python generate_1chronicles_tree_svg.py --centred  # the wall chart's
                                                       # layout, live before
    python generate_1chronicles_tree_svg.py --spine    # the layout tried
                                                       # and rejected here

Every frame is rendered before anything is written, and for the live layout
NOTHING is written if any of these fails (the comparison layouts only
report them):

* no two boxes overlap, and Israel, Esau and Judah stand in the tree;
* every verse's focus fits at 1.25 x the camera's minimum scale or closer;
* no line that joins a family (`svg_family_lines`) runs behind a box, and
  no two lines share a stretch (the panel heads' routed stems share their
  trunk as single pieces);
* every wife stands on a bar beside her husband (one wife rule);
* no verse lights a reference chip (the woman's real box lights);
* no file holds more than 1,050 <rect> or 268 <text> elements, counted in
  the file as written, the most proven smooth on the owner's iPad.
"""

import os
import sys

from generate_1chronicles import BOOK, CHAPTERS, coverage_check
from generate_tabernacle import out_path
from svg_chronicles_world import (IPAD_BOX_RECTS, IPAD_NAMES, VerseFrame,
                                  World)


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

    layout = ("spine" if "--spine" in argv else
              "centred" if "--centred" in argv else None)
    world = World(ot=True, layout=layout)
    x0, y0, x1, y1 = world.world_box
    named = sum(1 for n in world.nodes if n in world.first_of)
    print(f"world: {len(world.nodes)} nodes, {x1 - x0:.0f} x {y1 - y0:.0f} px")
    print(f"       {named} of them read by a verse of 1 Chr 1-9; "
          f"{len(world.nodes) - named} standing as context")

    frame = VerseFrame(world)
    problems = world.audit() + frame.audit()
    files = []
    most = {"rect": (0, ""), "text": (0, "")}
    first = True
    for ch, v, scene in world.order:
        c = frame.render(ch, v, scene, first)
        first = False
        text = c.tostring()
        # counted in the file as written, every element of the kind
        # anywhere in it (boxes, panels, the card, the veil and the HUD;
        # names, labels, titles, the card's names and the HUD's title):
        # the whole file is what the iPad has been proven on
        cn = {k: text.count("<" + k) for k in most}
        for k in most:
            if cn[k] > most[k][0]:
                most[k] = (cn[k], f"{ch}:{v}")
        if cn["rect"] > IPAD_BOX_RECTS:
            problems.append(f"{ch}:{v} draws {cn['rect']} rects "
                            f"(over {IPAD_BOX_RECTS})")
        if cn["text"] > IPAD_NAMES:
            problems.append(f"{ch}:{v} draws {cn['text']} names "
                            f"(over {IPAD_NAMES})")
        if only is not None and ch != only:
            continue
        files.append((ch, f"1_Chronicles_{ch}_{v}.svg", text))
    print(f"most rects in a file: {most['rect'][0]} ({most['rect'][1]}); "
          f"most names (<text>): {most['text'][0]} ({most['text'][1]})")

    if problems:
        print(f"{len(problems)} problems:")
        for p in problems[:16]:
            print("   " + p)
        if layout is None:
            # the comparison layouts are only re-run to be measured; the
            # live layout must come out clean
            print("stopped: nothing written")
            return 1

    total = bytes_ = 0
    per_chapter = {}
    for ch, name, text in files:
        if dry:
            bytes_ += len(text)
        else:
            path = (os.path.join(out_dir, name) if out_dir
                    else out_path(BOOK, ch, name))
            with open(path, "w", encoding="utf-8") as f:   # as SvgCanvas.save
                f.write(text)
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
