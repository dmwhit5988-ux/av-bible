"""Render Matthew 1 as per-verse vector SVGs — genealogy on the real tree,
Nativity in figures.

    .venv\\Scripts\\python.exe generate_matthew1_svg.py
    .venv\\Scripts\\python.exe generate_matthew1_svg.py --dry
    .venv\\Scripts\\python.exe generate_matthew1_svg.py --out DIR

THE DESIGN. Matthew 1 is two chapters wearing one number, and it gets two
drawings.

Verses 1-17 are a CAMERA OVER THE OLD TESTAMENT FAMILY TREE — the same
welded Adam-to-Jaddua tree that 1 Chronicles 1-9 is read against
(`chronicles_tree` + `ot_grafts`, drawn by `generate_ot_family_tree_svg`).
That works because it turns out to be literally true: Abraham to Zerubbabel
is one unbroken parent-child chain already standing on that sheet, thirty-six
of Matthew's forty-two names, in his order, with Tamar and Ruth already in
place as wives. Matthew adds fifteen nodes and not one of them is in the
middle — Rahab, Bathsheba and Uriah at the side, and twelve in a tail past
Zerubbabel, which is to say past the end of the Old Testament. See
`matthew_tree` for the grafts and `svg_matthew_world` for the camera.

What the reader therefore watches is not a list being built but a line being
traced down something already there, running off the bottom of the known
world at verse 13 and ending at a name the tree could not have contained.
Five generations Matthew skips are on the sheet, unlit, because his fourteens
depend on the skipping; the one place he disagrees with Chronicles about a
father is drawn as a gold arc rather than quietly resolved.

Verses 18-25 are a STAGE (`svg_matthew_nativity`): Joseph, Mary, an angel and
a child, on one ground line, with the bond between the two of them betrothed,
cut, and made — and the last inch of the genealogy's thread coming down onto
Joseph, lit on the verse that calls him "son of David".

NAMES. WEB is the only text (passages.TRANSLATION). The boxes carry the
TREE's names, which are the Old Testament's, and give the four where
Matthew's differ most the doubled label the chart already uses for
Abram · Abraham — Jacob · Israel, Salma · Salmon, Jeconiah · Jechoniah,
Azariah · Uzziah. So any listener hears a name they can find on the sheet.

(The fractal-tree design this replaces is in backups/matthew1_fractal_tree/,
with its rendered files. See the README there to restore it.)
"""

import os
import sys

from generate_tabernacle import out_path
from svg_matthew_nativity import NativityFrame, VERSES as NATIVITY_VERSES
from svg_matthew_world import (BOOK, CHAPTER, MatthewFrame,
                               MatthewWorld)

REPO = os.path.dirname(os.path.abspath(__file__))
BACKUP = os.path.join(REPO, "backups", "matthew1_fractal_tree")


def main(argv):
    dry = "--dry" in argv
    out_dir = None
    if "--out" in argv:
        out_dir = argv[argv.index("--out") + 1]
        os.makedirs(out_dir, exist_ok=True)

    if not os.path.isdir(BACKUP):
        print(f"refusing to run: {BACKUP} is missing — the previous design "
              f"and its rendered files should be there before this "
              f"overwrites them")
        return 1

    world = MatthewWorld()
    x0, y0, x1, y1 = world.world_box
    print(f"world: {len(world.nodes)} nodes, {x1 - x0:.0f} x {y1 - y0:.0f} px")
    print(f"       {len(world.line.new)} of them added by Matthew; "
          f"{len(world.nodes) - len(world.line.new)} standing from the "
          f"Old Testament")

    frame = MatthewFrame(world)
    nativity = NativityFrame(narr={
        v: world.narr.get((CHAPTER, v)) for v in NATIVITY_VERSES})

    total = bytes_ = 0
    first = True
    canvases = []
    for ch, v, scene in world.order:
        canvases.append((v, frame.render(ch, v, scene, first)))
        first = False
    for v in NATIVITY_VERSES:
        canvases.append((v, nativity.render(v)))

    for v, c in canvases:
        name = f"Matthew_{CHAPTER}_{v}.svg"
        if dry:
            bytes_ += len(c.tostring())
            total += 1
            continue
        path = (os.path.join(out_dir, name) if out_dir
                else out_path(BOOK, CHAPTER, name))
        c.save(path)
        bytes_ += os.path.getsize(path)
        total += 1

    print(f"TOTAL: {total} SVG files, {bytes_ / 1e6:.1f} MB "
          f"({bytes_ / max(total, 1) / 1e3:.0f} KB each)")
    if not dry:
        print("next: python build_manifest.py")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
