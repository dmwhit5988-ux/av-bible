"""Render Matthew 1 as per-verse vector SVGs — genealogy on the real tree,
Nativity in figures.

    .venv\\Scripts\\python.exe generate_matthew1_svg.py
    .venv\\Scripts\\python.exe generate_matthew1_svg.py --dry
    .venv\\Scripts\\python.exe generate_matthew1_svg.py --out DIR

Every frame is rendered before anything is written, and NOTHING is written
if a file draws a line that joins a family (`svg_family_lines`) behind a
box it draws, or two such lines on one stretch (`MatthewFrame.problems`),
or holds more than 1,050 <rect> or 268 <text> elements, counted in the file
as written, the most proven smooth on the owner's iPad.

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

(The fractal-tree design this replaces is kept for reference outside the
repo, in backups/matthew1_fractal_tree/ under config.ARCHIVE_DIR.)
"""

import os
import sys

from generate_tabernacle import out_path
from svg_chronicles_world import IPAD_BOX_RECTS, IPAD_NAMES
from svg_matthew_nativity import NativityFrame, VERSES as NATIVITY_VERSES
from svg_matthew_world import (BOOK, CHAPTER, MatthewFrame,
                               MatthewWorld)


def main(argv):
    dry = "--dry" in argv
    out_dir = None
    if "--out" in argv:
        out_dir = argv[argv.index("--out") + 1]
        os.makedirs(out_dir, exist_ok=True)

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

    problems = list(frame.problems)
    files = []
    most = {"rect": (0, ""), "text": (0, "")}
    for v, c in canvases:
        text = c.tostring()
        # every element of the kind anywhere in the file, as the 1
        # Chronicles driver counts them: the whole file is what the iPad
        # has been proven on
        cn = {k: text.count("<" + k) for k in most}
        for k in most:
            if cn[k] > most[k][0]:
                most[k] = (cn[k], f"{CHAPTER}:{v}")
        if cn["rect"] > IPAD_BOX_RECTS:
            problems.append(f"{CHAPTER}:{v} draws {cn['rect']} rects "
                            f"(over {IPAD_BOX_RECTS})")
        if cn["text"] > IPAD_NAMES:
            problems.append(f"{CHAPTER}:{v} draws {cn['text']} names "
                            f"(over {IPAD_NAMES})")
        files.append((v, text))
    print(f"most rects in a file: {most['rect'][0]} ({most['rect'][1]}); "
          f"most names (<text>): {most['text'][0]} ({most['text'][1]})")
    if problems:
        print(f"{len(problems)} problems:")
        for p in problems[:16]:
            print("   " + p)
        print("stopped: nothing written")
        return 1

    for v, text in files:
        name = f"Matthew_{CHAPTER}_{v}.svg"
        if dry:
            bytes_ += len(text)
            total += 1
            continue
        path = (os.path.join(out_dir, name) if out_dir
                else out_path(BOOK, CHAPTER, name))
        with open(path, "w", encoding="utf-8") as f:   # as SvgCanvas.save
            f.write(text)
        bytes_ += os.path.getsize(path)
        total += 1

    print(f"TOTAL: {total} SVG files, {bytes_ / 1e6:.1f} MB "
          f"({bytes_ / max(total, 1) / 1e3:.0f} KB each)")
    if not dry:
        print("next: python build_manifest.py")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
