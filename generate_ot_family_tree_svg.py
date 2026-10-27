"""The Old Testament family tree, as one zoomable poster.

`chronicles_tree.py` welds the nine Chronicles genealogy chapters into a
single tree rooted at Adam, and `ot_grafts.py` hangs the rest of the canon on
it — every person the Old Testament gives a join for. This draws the result:
one SVG, top-down, one contiguous tree.

Layout notes
------------
* GENERATION BANDS. Every node at depth d sits at the same y. That is the
  whole value of a reference chart of this size: Nahshon and Amram and
  Eliphaz line up. Bands are sized to the tallest box on them.
* GENERATION NUMBERS. The small number in each box is `N.gen`, its
  generation from Adam counted father to son (chronicles_tree.Tree.seal),
  which is not its depth: a wife or a house box is an edge but not a
  generation. Wives, houses, and everything below a join whose length the
  text doesn't give carry none (`printed_gen`).
* LEAF GRIDS. Joktan has thirteen sons and Azel six; laid out as one row
  they would set the width of everything above them. A parent whose children
  are all childless and numerous gets them stacked column-major under a bus
  instead, which trades width for a little height.
* The three edge styles are the tree module's, and they matter: solid is
  descent the text states, dashed is a join the text implies, doubled is a
  wife, or the mother a line is reckoned through. The legend says so on the
  sheet.
* REFERENCE CHIPS. A woman named in two families (Leah, Rachel, Milcah,
  Ruth) has one full box; where her other box would stand is a chip, a
  small pill with a gold dot and her name (`draw_chip`), which the gold
  line in her real box points at.

Output: web/visuals/reference/Old_Testament_family_tree.svg (+ a viewer page).
"""

import math
import os
import sys
import textwrap

import chronicles_tree as CT
from chronicles_tree import walk
from config import VISUALS_DIR
from generate_tabernacle import font
from svg_surface import SvgCanvas, _fmt, _rgb
import svg_figures as F

OUT_DIR = os.path.join(VISUALS_DIR, "reference")
STEM = "Old_Testament_family_tree"

# -- palette ---------------------------------------------------------------
# The house two-colour scheme, plus four badly-needed category accents. They
# are deliberately desaturated: the sheet must still read as sand on night.

BG        = (13, 13, 20)
PANEL     = (22, 22, 32)
RULE      = (52, 50, 64)
SAND      = (138, 129, 95)
SAND_DIM  = (86, 81, 62)
TEXT      = (216, 198, 143)
TEXT_DIM  = (146, 136, 106)
FAINT     = (92, 88, 76)

ROYAL     = (226, 188, 104)      # the line of David
PRIESTLY  = (138, 182, 166)      # Aaron, and the Levites
FEMALE    = (204, 152, 138)      # women through whom a line is reckoned
HOUSE     = (120, 118, 138)      # a house or company, not one man
HL        = (255, 244, 170)

# -- metrics ---------------------------------------------------------------

F_NAME    = font(15)
F_NAME_B  = font(15, bold=True)
F_NOTE    = font(10, italic=True)
F_REF     = font(9)
F_BAND    = font(13)
F_REGION  = font(30, bold=True)
F_REGSUB  = font(15, italic=True)
F_TITLE   = font(76, bold=True)
F_SUB     = font(21, italic=True)
F_LEG     = font(14)
F_LEGS    = font(12, italic=True)

PAD_X, PAD_Y = 10, 7
NAME_H       = 21
NOTE_H       = 12
MIN_W        = 88
NOTE_W       = 208          # box width once a node carries a note
SIB_GAP      = 20
ICON_H       = 26

# A REFERENCE CHIP (chronicles_tree.Tree.chip): a woman's name again where a
# second family names her, in a small pill with a gold dot. Her one full box
# stands elsewhere; the chip carries no note, ref or number.
CHIP_PX      = 13           # the chip's name
F_CHIP       = font(CHIP_PX)
CHIP_H       = 25
CHIP_DOT_X   = 11           # the gold dot's centre, from the chip's left
CHIP_DOT_R   = 3.2
CHIP_NAME_X  = 20           # the name's left, from the chip's left
CHIP_PAD_R   = 11
CHIP_DY      = (PAD_Y * 2 + NAME_H - CHIP_H) / 2   # how far below its row's
                            # top a chip stands, so its middle is on the
                            # row's name line (`top_of`)

MARGIN       = 220
MAST_W       = 540          # left strip for the title block and legend


# ===========================================================================
# Measuring and arranging
# ===========================================================================
#
# A thousand people will not go in one flat tree: laid out with every sibling
# set on one line the sheet comes out 77,000 px wide and 7,000 tall, which is
# a ribbon, not a chart. So a sibling set that is too wide WRAPS into stacked
# rows, and the row width is chosen per family from how much there is to fit
# (sqrt of the block's area, biased to a landscape block). Small families
# still get the ordinary centred bus; only big ones wrap.

ASPECT = 2.4                # target width:height of a wrapped block
ROW_GAP = 26
DROP = 30                   # parent box bottom -> the bus above its children


def _wrap(text, fnt, width, max_lines=5):
    """Greedy wrap to a pixel width, with an ellipsis if it overruns."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if fnt.getlength(trial) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines[-1] and fnt.getlength(lines[-1] + " …") > width:
            lines[-1] = lines[-1].rsplit(" ", 1)[0]
        lines[-1] += " …"
    return lines


def measure(n, notes=True):
    """Box size for one node: its note, and its cross-references.

    `notes=False` gives the name-only box the per-verse chapter renderer
    wants: the verse is narrated aloud, so prose on the graphic is noise
    there, and dropping it takes the world from 27,000 px wide to a third
    of that.

    Cross-references are measured in here rather than drawn floating between
    boxes, so the space they need is reserved by the layout and they cannot
    land on anybody's name.

    A reference chip is its name alone in a CHIP_H pill, with or without
    notes; its cross-reference is written in the real box only.
    """
    if n.chip is not None:
        # name only, whatever `notes` says: the note is the real box's
        n.w = CHIP_NAME_X + F_CHIP.getlength(n.label) + CHIP_PAD_R
        n.h = CHIP_H
        n.tw = n.xw = []
        return n
    fnt = F_NAME_B if n.kind in ("king", "priest") else F_NAME
    # a king's name is drawn 16 px right of the pad to make room for the
    # crown — the box has to be measured for that or the name clips its
    # border (the crown stays; the box grows)
    name_w = fnt.getlength(n.label) + (16 if n.kind == "king" else 0)
    if not notes:
        n.w = max(MIN_W, name_w + 2 * PAD_X)
        n.tw = n.xw = []
        n.h = PAD_Y * 2 + NAME_H + (ICON_H + 2 if n.icon else 0)
        return n
    if n.note or n.xref:
        n.w = max(NOTE_W, min(name_w + 2 * PAD_X, 300))
    else:
        n.w = max(MIN_W, name_w + 2 * PAD_X)
    if n.ref:
        n.w = max(n.w, name_w + F_REF.getlength(n.ref) + 3 * PAD_X)
    inner = n.w - 2 * PAD_X
    n.tw = _wrap(n.note, F_NOTE, inner) if n.note else []
    n.xw = []
    for other, text in n.xref:
        n.xw.extend(_wrap("→ " + other.label + " — " + text,
                          F_NOTE, inner, max_lines=3))
    n.h = PAD_Y * 2 + NAME_H + len(n.tw) * NOTE_H
    if n.xw:
        n.h += len(n.xw) * NOTE_H + 6
    if n.icon:
        n.h += ICON_H + 2
    return n


def arrange(n, notes=True):
    """Bottom-up: every subtree's own footprint, and how its children wrap.

    Leaves `n.rows` as a list of rows of children, and `n.sw` / `n.sh` as the
    subtree's total width and height.
    """
    measure(n, notes)
    for k in n.kids:
        arrange(k, notes)
    n.rows = []
    if not n.kids:
        n.sw, n.sh = n.w, n.h
        return n

    flat = sum(k.sw for k in n.kids) + SIB_GAP * (len(n.kids) - 1)
    widest = max(k.sw for k in n.kids)
    area = sum((k.sw + SIB_GAP) * k.sh for k in n.kids)
    cap = max(widest, math.sqrt(area * ASPECT))
    if flat <= cap * 1.05:                       # one row: the ordinary case
        n.rows = [list(n.kids)]
    else:
        row, rw = [], 0.0
        for k in n.kids:
            step = k.sw + (SIB_GAP if row else 0)
            if row and rw + step > cap:
                n.rows.append(row)
                row, rw = [k], k.sw
            else:
                row.append(k)
                rw += step
        if row:
            n.rows.append(row)

    def row_w(r):
        return sum(k.sw for k in r) + SIB_GAP * (len(r) - 1)

    def row_h(r):
        return max(k.sh for k in r)

    block_w = max(row_w(r) for r in n.rows)
    if len(n.rows) > 1:
        block_w += SPINE                          # room for the left spine
    n.sw = max(n.w, block_w)
    n.sh = (n.h + DROP + sum(row_h(r) for r in n.rows)
            + ROW_GAP * (len(n.rows) - 1))
    return n


SPINE = 26                  # gutter a wrapped block keeps for its left rail


def top_of(n, top):
    """A box's y on a row whose top is `top`. A reference chip is shorter
    than a name box and stands lower, its middle on the row's name line;
    every layout places through this."""
    return top + CHIP_DY if n.chip is not None else top


def place(n, cx, top):
    """Absolute positions. `cx` is where this subtree is centred, `top` its y."""
    n.x = cx - n.w / 2
    n.y = top_of(n, top)
    if not n.kids:
        return
    y = top + n.h + DROP
    if len(n.rows) == 1:                          # centred bus under the box
        row = n.rows[0]
        total = sum(k.sw for k in row) + SIB_GAP * (len(row) - 1)
        x = cx - total / 2
        for k in row:
            place(k, x + k.sw / 2, y)
            x += k.sw + SIB_GAP
        return
    # wrapped: rows left-aligned in the block, hung off a rail on the left
    block_w = n.sw
    left = cx - block_w / 2 + SPINE
    for r in n.rows:
        x = left
        h = max(k.sh for k in r)
        for k in r:
            place(k, x + k.sw / 2, y)
            x += k.sw + SIB_GAP
        y += h + ROW_GAP


# ---------------------------------------------------------------------------
# The spine layout
# ---------------------------------------------------------------------------
#
# `arrange`/`place` above centre a parent over the whole span of its
# descendants. That is right for a sheet somebody stands in front of: the
# eye takes the shape of a house in at a glance, and a father sitting over
# the middle of his descent is what makes it look like a tree.
#
# It is the wrong rule for a CAMERA reading the sheet a verse at a time,
# because it makes a node's x depend on how many descendants it has rather
# than on anything about the node. Measured on this tree, the median
# parent-to-child horizontal offset is 50 px and the 99th percentile is
# 8,278 — so a line of descent, which is what a genealogy mostly is, drifts
# sideways at every generation by however much progeny the last man had, and
# the camera has to chase it.
#
# `arrange_spine`/`place_spine` put the HEIR — the child carrying the widest
# descent — directly under its parent instead, and hang the other children
# beside it. A line of descent then comes out as a straight vertical column
# (median offset 0), the sheet is a fifth smaller in both directions, and
# total camera panning across a whole reading falls by about a fifth.
#
# THE COST IS BIRTH ORDER: the heir goes first, so Israel's sons come out
# Judah first rather than Reuben. The wall chart therefore still uses
# `arrange`/`place`; the spine layout is for the reading worlds that ask for
# it (see svg_matthew_world), and 1 Chronicles is untouched.
#
# The bookkeeping that makes it work is `lx`: with the parent over its first
# child, a subtree is no longer centred on its own node, so a slot cannot be
# allocated from `sw` alone. `lx` is the distance from a node's centre to the
# left edge of its subtree — sw/2 in the centred layout, anything at all in
# this one — and every placement goes through it.

def arrange_spine(n, notes=True):
    """Bottom-up footprint for the spine layout. Fills sw, lx and rows."""
    measure(n, notes)
    for k in n.kids:
        arrange_spine(k, notes)
    n.rows = []
    if not n.kids:
        n.sw, n.sh, n.lx = n.w, n.h, n.w / 2
        return n

    kids = list(n.kids)
    if len(kids) > 1:
        heir = max(kids, key=lambda k: k.sw)
        kids = [heir] + [k for k in kids if k is not heir]

    # Same wrapping rule as `arrange`: a family too wide for one row breaks
    # into rows. Without it the sheet came out 263,000 px wide.
    flat = sum(k.sw for k in kids) + SIB_GAP * (len(kids) - 1)
    widest = max(k.sw for k in kids)
    area = sum((k.sw + SIB_GAP) * k.sh for k in kids)
    cap = max(widest, math.sqrt(area * ASPECT))
    if flat <= cap * 1.05:
        n.rows = [list(kids)]
    else:
        row, rw = [], 0.0
        for k in kids:
            step = k.sw + (SIB_GAP if row else 0)
            if row and rw + step > cap:
                n.rows.append(row)
                row, rw = [k], k.sw
            else:
                row.append(k)
                rw += step
        if row:
            n.rows.append(row)

    def row_w(r):
        return sum(k.sw for k in r) + SIB_GAP * (len(r) - 1)

    # Local coordinates: every row starts at 0, so the block runs 0..block_w.
    # The parent's centre lands on the first child's centre, which sits `lx`
    # into that child's own slot.
    block_w = max(row_w(r) for r in n.rows)
    centre = n.rows[0][0].lx
    left = min(0.0, centre - n.w / 2)
    right = max(block_w, centre + n.w / 2)
    n.sw = right - left
    n.lx = centre - left
    n.sh = (n.h + DROP + sum(max(k.sh for k in r) for r in n.rows)
            + ROW_GAP * (len(n.rows) - 1))
    return n


def place_spine(n, cx, top):
    """Absolute positions, the parent standing over its first child."""
    n.x = cx - n.w / 2
    n.y = top_of(n, top)
    if not n.kids:
        return
    y = top + n.h + DROP
    origin = cx - n.rows[0][0].lx          # world x of the block's local 0
    for r in n.rows:
        x = origin
        for k in r:
            place_spine(k, x + k.lx, y)
            x += k.sw + SIB_GAP
        y += max(k.sh for k in r) + ROW_GAP


def subtree_extent(n):
    xs0 = min(m.x for m in walk(n))
    xs1 = max(m.x + m.w for m in walk(n))
    ys1 = max(m.y + m.h for m in walk(n))
    return xs0, xs1, ys1


def extents(root):
    return subtree_extent(root)


# ===========================================================================
# Drawing
# ===========================================================================

def accent(n):
    return {"king": ROYAL, "priest": PRIESTLY, "woman": FEMALE,
            "house": HOUSE}.get(n.kind, SAND_DIM)


def dim(col, a):
    return (col[0], col[1], col[2], int(255 * a))


LINK_STYLE = {"dash": ("4 4", 1.3), "wife": (None, 1.7), "solid": (None, 1.5)}


def _drop(c, k, from_y):
    """The short vertical from a bus into one child, in that child's style."""
    kcx = k.x + k.w / 2
    dash, wdt = LINK_STYLE.get(k.link, LINK_STYLE["solid"])
    col = {"dash": dim(SAND_DIM, 0.85), "wife": FEMALE}.get(k.link, SAND_DIM)
    c.line((kcx, from_y), (kcx, k.y), col, wdt, dash=dash)
    if k.link == "wife":                       # doubled: a wife or mother
        c.line((kcx + 3.5, from_y + 5), (kcx + 3.5, k.y), col, 1.0)
    if k.link == "dash":                       # open bead: an implied join
        c.circle(kcx, k.y - 6, 2.4, fill=BG, stroke=col, width=1.1)


def draw_edges(c, n):
    if not n.kids:
        return
    py = n.y + n.h
    pcx = n.x + n.w / 2

    if len(n.rows) == 1:
        row = n.rows[0]
        bus = min(k.y for k in row) - DROP / 2
        c.line((pcx, py), (pcx, bus), SAND_DIM, 1.5)
        if len(row) > 1:
            cxs = [k.x + k.w / 2 for k in row] + [pcx]
            c.line((min(cxs), bus), (max(cxs), bus), SAND_DIM, 1.5)
        for k in row:
            _drop(c, k, bus)
    else:
        # A wrapped family: one rail down the left of the block, a shelf out
        # to each row, and the ordinary drop into each child from its shelf.
        spine_x = min(k.x for r in n.rows for k in r) - SPINE + 8
        shelves = [min(k.y for k in r) - DROP / 2 for r in n.rows]
        c.line((pcx, py), (pcx, shelves[0]), SAND_DIM, 1.5)
        c.line((min(spine_x, pcx), shelves[0]), (max(spine_x, pcx),
               shelves[0]), SAND_DIM, 1.5)
        c.line((spine_x, shelves[0]), (spine_x, shelves[-1]), SAND_DIM, 1.5)
        for r, shelf in zip(n.rows, shelves):
            right = max(k.x + k.w / 2 for k in r)
            c.line((spine_x, shelf), (right, shelf), SAND_DIM, 1.4)
            for k in r:
                _drop(c, k, shelf)

    for k in n.kids:
        draw_edges(c, k)


def draw_chip(c, n, edge, ink, dot, fill=PANEL, width=1.1, name=True):
    """A reference chip: a pill, a gold dot, the name. The verse cameras
    draw it through here too, in their own looks; without `name` it is the
    pill alone."""
    c.rect(n.x, n.y, n.w, n.h, fill=fill, stroke=edge, width=width,
           rx=n.h / 2)
    if name:
        c.circle(n.x + CHIP_DOT_X, n.y + n.h / 2, CHIP_DOT_R, fill=dot,
                 stroke=None)
        c.text((n.x + CHIP_NAME_X, n.y + n.h / 2), n.label, CHIP_PX, ink,
               anchor="lm")


def link_anchor(n):
    """The point a cross-reference's length is measured from
    (LINK_ARC_MAX): a box's centre, or a chip's gold dot."""
    if n.chip is not None:
        return n.x + CHIP_DOT_X, n.y + n.h / 2
    return n.x + n.w / 2, n.y + n.h / 2


def link_ends(n):
    """Where a cross-reference arc may meet box `n`, each with the way out.

    A box offers the quarter points of its top and bottom edges and the
    middle of each side, so the end dot sits on the box's edge: not inside,
    where it would cover a letter of the reference it marks, and not at the
    middle of the top or bottom, where the box's family lines join it. A
    chip offers only its own gold dot, left by way of up, down or left."""
    if n.chip is not None:
        p = (n.x + CHIP_DOT_X, n.y + n.h / 2)
        return [(p, (0, -1)), (p, (0, 1)), (p, (-1, 0))]
    x0, y0, x1, y1 = n.x, n.y, n.x + n.w, n.y + n.h
    q1, q3, ym = x0 + n.w / 4, x0 + n.w * 3 / 4, y0 + n.h / 2
    return [((q1, y0), (0, -1)), ((q3, y0), (0, -1)),
            ((q1, y1), (0, 1)), ((q3, y1), (0, 1)),
            ((x0, ym), (-1, 0)), ((x1, ym), (1, 0))]


def draw_node(c, n):
    if n.chip is not None:
        draw_chip(c, n, dim(FEMALE, 0.8), FEMALE, dim(ROYAL, 0.95))
        return
    col = accent(n)
    body = PANEL if n.kind != "house" else BG
    rx = 13 if n.kind == "woman" else 4
    if n.kind == "house":
        c.rect(n.x, n.y, n.w, n.h, fill=body, stroke=dim(col, 0.85),
               width=1.1, rx=6)
        c.line((n.x + 6, n.y + n.h - 3), (n.x + n.w - 6, n.y + n.h - 3),
               dim(col, 0.5), 1.0, dash="3 3")
    else:
        c.rect(n.x, n.y, n.w, n.h, fill=body, stroke=col,
               width=2.0 if n.kind in ("king", "priest") else 1.3, rx=rx)

    ty = n.y + PAD_Y
    if n.icon:
        _icon(c, n, n.x + n.w / 2, ty + ICON_H)
        ty += ICON_H + 2

    if n.kind == "king":
        _crown(c, n.x + PAD_X + 1, ty + NAME_H / 2)
    name_x = n.x + PAD_X + (16 if n.kind == "king" else 0)
    name_col = {"king": HL, "priest": PRIESTLY, "woman": FEMALE,
                "house": dim(TEXT_DIM, 0.95)}.get(n.kind, TEXT)
    c.text((name_x, ty + NAME_H / 2), n.label, 15, name_col, anchor="lm",
           bold=n.kind in ("king", "priest"), italic=n.kind == "house")
    if n.ref:
        c.text((n.x + n.w - PAD_X, ty + NAME_H / 2), n.ref, 9,
               dim(FAINT, 0.95), anchor="rm")
    y = ty + NAME_H
    for line in n.tw:
        c.text((n.x + PAD_X, y + NOTE_H / 2), line, 10, TEXT_DIM,
               anchor="lm", italic=True)
        y += NOTE_H
    if n.xw:
        y += 3
        c.line((n.x + PAD_X, y), (n.x + n.w - PAD_X, y), dim(ROYAL, 0.35),
               1.0)
        y += 3
        for line in n.xw:
            c.text((n.x + PAD_X, y + NOTE_H / 2), line, 10, dim(ROYAL, 0.95),
                   anchor="lm", italic=True)
            y += NOTE_H
    # the generation from Adam, so a name can be placed in time at a glance
    if printed_gen(n) is not None:
        c.text((n.x + n.w - 4, n.y + n.h - 1), str(n.gen), 8,
               dim(FAINT, 0.75), anchor="rb")


def printed_gen(n):
    """The generation number a box carries (chronicles_tree.Tree.seal), or
    None. A house is not a generation, a wife's number is her own line's
    and not her husband's, below a join of unknown length the count is
    unknown, and a reference chip is not a box of her own — none of those
    print one."""
    if n.kind == "house" or n.link == "wife" or n.chip is not None:
        return None
    return n.gen


def deepest_line(nodes):
    """(generations, the deepest numbered box, its father) for the masthead.

    The father is the nearest box above that is neither a wife (the line is
    reckoned through her husband) nor a house. Ties go to the first box in
    reading order."""
    deep = max((n for n in nodes if printed_gen(n) is not None),
               key=lambda n: n.gen)
    up = deep.parent
    while up is not None and (up.link == "wife" or up.kind == "house"):
        up = up.parent
    return deep.gen, deep, up


def _crown(c, x, cy):
    """The mark that says 'reigned' — small enough to sit in a name row."""
    w, h = 12, 8
    pts = [(x, cy + h / 2), (x, cy - h / 2 + 2), (x + w * 0.25, cy + 0.5),
           (x + w * 0.5, cy - h / 2 - 1), (x + w * 0.75, cy + 0.5),
           (x + w, cy - h / 2 + 2), (x + w, cy + h / 2)]
    c.polygon(pts, fill=dim(ROYAL, 0.85), stroke=ROYAL, width=1.0)


_ICON_CACHE = {}


def _icon(c, n, cx, gy):
    """A figure from the shared vocabulary, scaled into an ICON_H band."""
    parts = _ICON_CACHE.get(n.icon)
    if parts is None:
        maker = getattr(F, n.icon, None)
        if maker is None:
            return
        parts = maker()
        _ICON_CACHE[n.icon] = parts
    x0, x1, y0, y1 = F.bbox((parts, 0))        # note: x-pair then y-pair
    s = min(ICON_H / max(1e-6, y1 - y0), (n.w - 26) / max(1e-6, x1 - x0))
    # place() puts local y=0 on `gy` and runs up, so the ground line for a
    # figure whose lowest point is y0 sits y0*s below the box's bottom.
    F.draw(c, parts, cx - (x0 + x1) / 2 * s, gy + y0 * s, s,
           dim(accent(n), 0.95), PANEL)


# ===========================================================================
# Furniture: generation ruler, region bands, cross-links, legend
# ===========================================================================

# Bands drawn behind a named subtree, so the sheet has structure when you are
# zoomed too far out to read a box. Adam's and Shem's subtrees are the whole
# chart, so they get no band — the masthead says that already.
REGIONS = [
    ("Cain",     "CAIN",        "Gen 4:1-24 — the line that ends at the flood"),
    ("Nahor",    "NAHOR",       "Gen 11:29, 22:20-24 — Rebekah, Leah and Rachel come out of this house"),
    ("Japheth",  "JAPHETH",     "1 Chr 1:5-7"),
    ("Ham",      "HAM",         "1 Chr 1:8-16"),
    ("Ishmael",  "ISHMAEL",     "1 Chr 1:29-31 — twelve princes"),
    ("Keturah",  "KETURAH",     "1 Chr 1:32-33 — and Midian, whose priest was Moses' father-in-law"),
    ("Esau",     "ESAU — EDOM", "1 Chr 1:35-54, with the Horites of Seir, the eight kings and the eleven chiefs"),
    ("Reuben",   "REUBEN",      "1 Chr 5:1-10"),
    ("Simeon",   "SIMEON",      "1 Chr 4:24-43"),
    ("Levi",     "LEVI",        "1 Chr 6 — the high priests, the houses, the singers; and on through Ezra to Jaddua"),
    ("Judah",    "JUDAH",       "1 Chr 2:3-55, 4:1-23 — the largest branch in the canon"),
    ("David",    "THE HOUSE OF DAVID", "1 Chr 3, every reign 2 Chronicles records, and the line past the exile"),
    ("Issachar", "ISSACHAR",    "1 Chr 7:1-5"),
    ("Zebulun",  "ZEBULUN",     "Gen 46:14 — all the canon gives him"),
    ("Dan",      "DAN",         "Gen 46:23, and Samson"),
    ("Joseph",   "JOSEPH",      "1 Chr 7:14-29 — Manasseh and Ephraim, Gideon and Joshua"),
    ("Benjamin", "BENJAMIN",    "1 Chr 7:6-12, 8:1-40 — his sons from three lists, the house of Saul, and Mordecai"),
    ("Naphtali", "NAPHTALI",    "1 Chr 7:13"),
    ("Gad",      "GAD",         "1 Chr 5:11-17"),
    ("Asher",    "ASHER",       "1 Chr 7:30-40"),
    ("the kings of Israel", "THE KINGS OF ISRAEL",
     "1 Kgs 12 - 2 Kgs 17 — nine houses in two hundred years"),
]

# Where a band's name repeats on the tree, its anchor is a path: the first
# label must be the only one of its name, and each later one the only child
# of that name under the one before. A bare find() takes whichever namesake
# pre-order reaches first: "Nahor" finds Serug's son (all of Terah's house),
# "Ishmael" Azel's son and "Joseph" a spy's father. The timeline anchors its
# bands the same way (generate_ot_timeline_svg.REGION_LOC).
REGION_AT = {
    "Nahor":    ("Terah", "Nahor"),
    "Ishmael":  ("Abram · Abraham", "Ishmael"),
    "Joseph":   ("Israel", "Joseph"),
    "Benjamin": ("Israel", "Benjamin"),
}

SILENT = ("Dan", "Zebulun")


def region_node(T, label):
    """The node a REGIONS band frames (`Tree.at`); raises rather than
    guess."""
    try:
        return T.at(*REGION_AT.get(label, (label,)))
    except LookupError as e:
        raise LookupError(f"band {label!r}: {e}; give REGION_AT a path") \
            from None


def subtree_box(n, pad=16):
    xs0 = min(m.x for m in walk(n)) - pad
    xs1 = max(m.x + m.w for m in walk(n)) + pad
    ys0 = n.y - pad
    ys1 = max(m.y + m.h for m in walk(n)) + pad
    return xs0, ys0, xs1, ys1


def draw_regions(c, T):
    boxes = []
    for label, title, sub in REGIONS:
        n = region_node(T, label)
        boxes.append((subtree_box(n), title, sub, n))
    boxes.sort(key=lambda b: -( (b[0][2] - b[0][0]) * (b[0][3] - b[0][1]) ))
    for (x0, y0, x1, y1), title, sub, n in boxes:
        c.rect(x0, y0, x1 - x0, y1 - y0, fill=dim(PANEL, 0.30),
               stroke=dim(RULE, 0.95), width=1.2, rx=18)
        c.text((x0 + 20, y0 - 40), title, 30, dim(SAND, 0.62),
               anchor="lm", bold=True)
        c.text((x0 + 20, y0 - 16), sub, 15, dim(FAINT, 0.95),
               anchor="lm", italic=True)


LINK_ARC_MAX = 3200         # beyond this an arc is longer than it is useful
LINK_STEP = 3               # px between the points a route is tested at
LINK_CLEAR = 5              # px a route keeps clear of a box it passes
LINK_CELL = 240             # the box grid a route is tested against
LINK_HANDLES = (0.12, 0.25, 0.4, 0.6)   # how far an end runs straight out,
LINK_HANDLE_MAX = 240                   # as a share of the span, and at most


def _box_grid(nodes):
    grid = {}
    for n in nodes:
        if n.w <= 0 or n.h <= 0:
            continue
        x0, y0 = n.x - LINK_CLEAR, n.y - LINK_CLEAR
        x1, y1 = n.x + n.w + LINK_CLEAR, n.y + n.h + LINK_CLEAR
        for gx in range(int(x0 // LINK_CELL), int(x1 // LINK_CELL) + 1):
            for gy in range(int(y0 // LINK_CELL), int(y1 // LINK_CELL) + 1):
                grid.setdefault((gx, gy), []).append(n)
    return grid


def _bezier(cv, t):
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = cv
    u = 1 - t
    a, b, c, d = u * u * u, 3 * u * u * t, 3 * u * t * t, t * t * t
    return (a * x0 + b * x1 + c * x2 + d * x3,
            a * y0 + b * y1 + c * y2 + d * y3)


def link_route(a, b, grid):
    """The cubic a cross-reference arc is drawn as, from the edge of box `a`
    to the edge of box `b` (its four points; the end dots go on the first
    and last), or None when the two are further apart than LINK_ARC_MAX.

    The candidates are the arc that springs between the two boxes' centres
    (`link_anchor`), cut where it leaves each box, and curves that leave
    each box square to one of the edges `link_ends` offers. A line behind a
    box reads as a line through that name, so the route that passes the
    fewest boxes bearing either end's name wins, then the one behind the
    fewest boxes, then the one that keeps clear of the most, then the
    shortest (`_route_score`). Either way an end dot sits on the box's
    edge, or on a chip's own dot, never on the reference it marks. `grid` is
    `_box_grid` of every box on the sheet."""
    ax, ay = link_anchor(a)
    bx, by = link_anchor(b)
    if math.hypot(bx - ax, by - ay) > LINK_ARC_MAX:
        return None
    mx, my = (ax + bx) / 2, (ay + by) / 2
    lift = min(240, max(90, abs(bx - ax) * 0.22 + abs(by - ay) * 0.18))
    cx, cy = mx, my - lift
    arc = ((ax, ay), (ax + (cx - ax) * 2 / 3, ay + (cy - ay) * 2 / 3),
           (bx + (cx - bx) * 2 / 3, by + (cy - by) * 2 / 3), (bx, by))
    t0 = 0.0 if a.chip is not None else _leave(arc, a, False)
    t1 = 1.0 if b.chip is not None else _leave(arc, b, True)
    cands = [_split(arc, t0, t1)] if t0 < t1 else []
    for p, dp in link_ends(a):
        for q, dq in link_ends(b):
            span = math.hypot(q[0] - p[0], q[1] - p[1])
            for fa in LINK_HANDLES:
                for fb in LINK_HANDLES:
                    ka = min(LINK_HANDLE_MAX, max(20.0, fa * span))
                    kb = min(LINK_HANDLE_MAX, max(20.0, fb * span))
                    cands.append((p, (p[0] + dp[0] * ka, p[1] + dp[1] * ka),
                                  (q[0] + dq[0] * kb, q[1] + dq[1] * kb), q))
    best = None
    for cv in cands:
        score = _route_score(cv, a, b, grid, best[0] if best else None)
        if score is not None and (best is None or score < best[0]):
            best = (score, cv)
    return best[1]


def _inside(n, x, y, pad=-1):
    """Whether (x, y) is inside box `n` grown by `pad` px."""
    return (n.x - pad < x < n.x + n.w + pad
            and n.y - pad < y < n.y + n.h + pad)


def _leave(cv, n, back):
    """Where the curve `cv`, starting (or with `back`, ending) inside box
    `n`, crosses its edge, as a parameter t."""
    inside, out = (1.0, 0.0) if back else (0.0, 1.0)
    for i in range(1, 201):
        t = (1 - i / 200) if back else i / 200
        if not _inside(n, *_bezier(cv, t)):
            out = t
            break
        inside = t
    for _ in range(30):
        mid = (inside + out) / 2
        if _inside(n, *_bezier(cv, mid)):
            inside = mid
        else:
            out = mid
    return out


def _split(cv, t0, t1):
    """The piece of cubic `cv` between t0 and t1, as a cubic."""
    def cut(c, t):                  # de Casteljau: (left part, right part)
        p01 = [c[0][i] + (c[1][i] - c[0][i]) * t for i in (0, 1)]
        p12 = [c[1][i] + (c[2][i] - c[1][i]) * t for i in (0, 1)]
        p23 = [c[2][i] + (c[3][i] - c[2][i]) * t for i in (0, 1)]
        p012 = [p01[i] + (p12[i] - p01[i]) * t for i in (0, 1)]
        p123 = [p12[i] + (p23[i] - p12[i]) * t for i in (0, 1)]
        mid = tuple(p012[i] + (p123[i] - p012[i]) * t for i in (0, 1))
        return ((c[0], tuple(p01), tuple(p012), mid),
                (mid, tuple(p123), tuple(p23), c[3]))
    left = cut(cv, t1)[0]
    return cut(left, t0 / t1)[1] if t0 > 0 else left


def _route_score(cv, a, b, grid, worst):
    """How a route reads, best first: (boxes bearing the name of either end
    that it passes behind or within LINK_CLEAR of, boxes it passes behind,
    other boxes it passes within LINK_CLEAR of, its length). By a namesake,
    the line would seem to point at the wrong man. None as soon as the
    first two pass `worst`'s."""
    poly = sum(math.hypot(cv[i + 1][0] - cv[i][0], cv[i + 1][1] - cv[i][1])
               for i in range(3))
    steps = max(24, int(poly / LINK_STEP))
    pts = [_bezier(cv, i / steps) for i in range(steps + 1)]
    names = (a.label, b.label)
    behind, near, same = set(), set(), set()
    for x, y in pts:
        for n in grid.get((int(x // LINK_CELL), int(y // LINK_CELL)), ()):
            if n is a or n is b:
                if n.chip is None and _inside(n, x, y):
                    behind.add(id(n))     # back into its own box (a chip's
                continue                  # curve starts on its own dot)
            if not _inside(n, x, y, LINK_CLEAR):
                continue
            if n.label in names:
                same.add(id(n))
            if _inside(n, x, y, 0):
                behind.add(id(n))
            else:
                near.add(id(n))
        if worst is not None and (len(same), len(behind)) > worst[:2]:
            return None
    length = sum(math.hypot(u[0] - v[0], u[1] - v[1])
                 for u, v in zip(pts, pts[1:]))
    return len(same), len(behind), len(near - behind), length


def link_routes(T):
    """`link_route` for every cross-reference on a laid-out tree, in
    `T.links` order, leaving out those too far apart to draw."""
    grid = _box_grid(walk(T.root))
    return [cv for cv in (link_route(a, b, grid) for a, b, _ in T.links)
            if cv is not None]


def draw_links(c, routes, dots=False):
    """The gold ties between two boxes that name each other, along
    `link_routes`.

    The reason for the tie is written inside both boxes (see `measure`), so
    the arc carries no label of its own — a floating label on a sheet this
    dense has nowhere to sit that is not on top of somebody. Pairs further
    apart than LINK_ARC_MAX get no arc either: at that length the line stops
    reading as a connection and becomes a scratch across the chart, and the
    two boxes still point at each other in words.

    Called twice: once before the boxes for the arcs, so a curve passes
    BEHIND any name it crosses, and once after for the end dots, which sit
    on the edge of the box they mark.
    """
    for cv in routes:
        if dots:
            for px, py in (cv[0], cv[3]):
                c.circle(px, py, 3.4, fill=dim(ROYAL, 0.8), stroke=None)
            continue
        d = "M %s %s C %s %s %s %s %s %s" % tuple(
            _fmt(v) for pt in cv for v in pt)
        c.path(d, fill=None, stroke=dim(ROYAL, 0.5), width=1.6)


def draw_masthead(c, x, y, T, stats):
    c.text((x, y), "ONE TREE:", 21, dim(SAND, 0.8), anchor="lt", italic=True)
    c.text((x, y + 34), "THE OLD", 76, TEXT, anchor="lt", bold=True)
    c.text((x, y + 116), "TESTAMENT", 76, TEXT, anchor="lt", bold=True)
    sy = y + 208
    for line in _wrap("Built on the spine of 1 & 2 Chronicles, and grafted "
                      "with every person the rest of the canon gives a "
                      "join for.", F_SUB, MAST_W - 40):
        c.text((x, sy), line, 20, dim(TEXT_DIM, 0.95), anchor="lt",
               italic=True)
        sy += 30
    sy += 8
    for line in _wrap("Names and spellings are the World English Bible's.",
                      F_SUB, MAST_W - 40):
        c.text((x, sy), line, 20, dim(FAINT, 0.95), anchor="lt", italic=True)
        sy += 30

    ly = sy + 34
    c.text((x, ly), "HOW TO READ IT", 15, dim(SAND, 0.85), anchor="lt",
           bold=True)
    ly += 30
    rows = [
        ("solid", "father to son, as the text states it"),
        ("dash", "a join the text implies but does not state — the note "
                 "on the box says what the inference is"),
        ("wife", "a wife, or the mother the line is reckoned through"),
    ]
    for kind, what in rows:
        if kind == "solid":
            c.line((x + 4, ly), (x + 34, ly), SAND_DIM, 1.5)
        elif kind == "dash":
            c.line((x + 4, ly), (x + 34, ly), dim(SAND_DIM, 0.8), 1.3,
                   dash="4 4")
            c.circle(x + 34, ly, 2.2, fill=None, stroke=dim(SAND_DIM, 0.8),
                     width=1.1)
        else:
            c.line((x + 4, ly - 2), (x + 34, ly - 2), FEMALE, 1.6)
            c.line((x + 4, ly + 2), (x + 34, ly + 2), FEMALE, 1.0)
        c.text((x + 48, ly), what, 14, TEXT_DIM, anchor="lm")
        ly += 26

    ly += 14
    swatches = [(ROYAL, "a king, of Judah or of Israel"),
                (PRIESTLY, "a priest or Levite"),
                (FEMALE, "a woman the text names"),
                (HOUSE, "a house or company, not one man")]
    for col, what in swatches:
        c.rect(x + 4, ly - 8, 30, 16, fill=dim(PANEL, 1.0), stroke=col,
               width=1.6, rx=4)
        c.text((x + 48, ly), what, 14, TEXT_DIM, anchor="lm")
        ly += 26

    ly += 10
    c.rect(x + 4, ly - 9, 30, 18, fill=dim(PANEL, 1.0),
           stroke=dim(SAND_DIM, 0.9), width=1.2, rx=4)
    c.line((x + 8, ly - 2), (x + 30, ly - 2), dim(ROYAL, 0.6), 1.0)
    c.text((x + 8, ly + 5), "→", 9, dim(ROYAL, 0.95), anchor="lm")
    for line in _wrap("a gold line inside a box is a cross-reference: this "
                      "person is named somewhere else on the sheet, and the "
                      "line says how. Near pairs are tied by a gold arc too.",
                      F_LEG, MAST_W - 110):
        c.text((x + 48, ly), line, 14, TEXT_DIM, anchor="lm")
        ly += 19
    ly += 8

    ly += 10
    c.rect(x + 2, ly - 9, 34, 18, fill=dim(PANEL, 1.0),
           stroke=dim(FEMALE, 0.8), width=1.1, rx=9)
    c.circle(x + 10, ly, 2.6, fill=dim(ROYAL, 0.95), stroke=None)
    for line in _wrap("a small box with a gold dot is a woman named in a "
                      "second family. She is drawn once in full, where her "
                      "children are reckoned (or under her father), and her "
                      "box's gold line points here.", F_LEG, MAST_W - 110):
        c.text((x + 48, ly), line, 14, TEXT_DIM, anchor="lm")
        ly += 19
    ly += 8

    ly += 18
    c.text((x, ly), "WHAT IS AND IS NOT HERE", 15, dim(SAND, 0.85),
           anchor="lt", bold=True)
    ly += 28
    notes = [
        "%(people)d people and %(houses)d houses; %(solid)d stated "
        "descents, %(dash)d implied ones and %(wife)d doubled lines to a "
        "wife or mother. Every one of them reaches Adam." % stats,
        "The deepest line runs %(deep)d generations, Adam to %(deep_who)s. "
        "The small grey number in each box is its generation from Adam, "
        "counted father to son. A wife's box has none, and it is left off "
        "below any join where the text does not say how many generations "
        "lie between." % stats,
        "A person is here only if the text gives a join. Isaiah is not — "
        "\u201cson of Amoz\u201d joins nothing. Zephaniah is: his four "
        "fathers run back to a Hezekiah in Josiah\u2019s day.",
        "City and town lists, the Hagrite war and the gatekeepers\u2019 "
        "duty roster are left out; the people named inside them are kept.",
        "The canon repeats names freely and does not always agree with "
        "itself. Where two books give one man two fathers, the chart never "
        "chooses quietly: both lines are drawn, or one is and the box’s "
        "note gives the other.",
    ]
    for t in notes:
        for line in _wrap(t, F_LEGS, MAST_W - 60):
            c.text((x, ly), line, 12, dim(FAINT, 0.98), anchor="lt",
                   italic=True)
            ly += 18
        ly += 10
    return ly


def draw_silent(c, x, y):
    c.rect(x, y, MAST_W - 60, 122, fill=dim(PANEL, 0.5),
           stroke=dim(HOUSE, 0.8), width=1.2, rx=10)
    c.text((x + 20, y + 26), "THE TRIBES CHRONICLES WILL NOT TRACE", 15,
           dim(HOUSE, 1.0), anchor="lm", bold=True)
    c.text((x + 20, y + 54), "DAN   ·   ZEBULUN", 24, dim(TEXT_DIM, 0.9),
           anchor="lm", bold=True)
    ty = y + 78
    for line in _wrap("named among Israel’s twelve sons in 2:1-2 and "
                      "then dropped. Genesis 46 gives them four sons "
                      "between them, and that is every one the canon has.",
                      F_LEGS, MAST_W - 100):
        c.text((x + 20, ty), line, 12, dim(FAINT, 1.0), anchor="lt",
               italic=True)
        ty += 16


# ===========================================================================
# Build
# ===========================================================================

def build_svg():
    T = CT.build()
    root = T.root

    arrange(root)
    place(root, 0, 0)

    x0, x1, y1 = extents(root)
    left = x0 - MARGIN - MAST_W
    top = -MARGIN - 90
    W = (x1 + MARGIN) - left
    H = (y1 + MARGIN) - top

    c = SvgCanvas(W, H, bg=BG)
    c._els.insert(0, f'<g transform="translate({_fmt(-left)} {_fmt(-top)})">')

    draw_regions(c, T)
    # Order matters: everything that is a LINE goes down before anything
    # that is a BOX, so no connector and no cross-reference arc is drawn
    # across a name. Only the arcs' end dots come back on top.
    draw_edges(c, root)
    routes = link_routes(T)
    draw_links(c, routes)
    for n in walk(root):
        draw_node(c, n)
    draw_links(c, routes, dots=True)

    nodes = list(walk(root))
    stats = {
        "people": sum(1 for n in nodes
                      if n.kind != "house" and n.chip is None),
        "houses": sum(1 for n in nodes if n.kind == "house"),
        "solid": sum(1 for n in nodes if n.link == "solid") - 1,
        "dash": sum(1 for n in nodes if n.link == "dash"),
        "wife": sum(1 for n in nodes if n.link == "wife"),
    }
    gens, deep, father = deepest_line(nodes)
    stats["deep"] = gens
    stats["deep_who"] = deep.label + (
        f" {'daughter' if deep.kind == 'woman' else 'son'} of {father.label}"
        if father is not None else "")
    mast_x = x0 - MAST_W - 90
    below = draw_masthead(c, mast_x, top + 130, T, stats)
    draw_silent(c, mast_x, below + 40)

    c._emit("</g>")
    body = "\n".join(c._els)
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {_fmt(W)} {_fmt(H)}" width="{_fmt(W)}" '
        f'height="{_fmt(H)}" data-kind="genealogy" '
        f'data-title="The Old Testament family tree">\n'
        f'<title>The Old Testament family tree \u2014 one contiguous descent from Adam</title>\n'
        f'{body}\n</svg>\n')
    return svg, W, H, len(nodes)


# The pan/zoom/search page beside each chart. The web app's Reference list
# opens it in a frame (web/js/app.js REFERENCES), so it has to work by touch:
# one finger pans, two pinch, and the search box is 16px so that iOS doesn't
# zoom the whole page when it takes focus.
VIEWER = """<!doctype html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<style>
  html,body{margin:0;height:100%%;background:#0d0d14;color:#d8c68f;
            font-family:Georgia,'Times New Roman',serif;overflow:hidden}
  #stage{position:absolute;inset:0;cursor:grab;touch-action:none}
  #stage.drag{cursor:grabbing}
  #stage svg{position:absolute;top:0;left:0;transform-origin:0 0}
  #bar{position:absolute;top:0;left:0;right:0;z-index:5;display:flex;
       flex-wrap:wrap;gap:8px 10px;align-items:center;padding:10px 14px;
       background:linear-gradient(#0d0d14ee,#0d0d1400)}
  input,button{font:14px Georgia,serif;background:#16161f;color:#d8c68f;
       border:1px solid #4a4658;border-radius:6px;padding:6px 10px}
  input{font-size:16px;flex:0 1 330px;min-width:0}
  button{cursor:pointer;min-width:36px}
  #hits{font-size:13px;color:#8a8270;font-style:italic}
  .found rect:first-of-type{stroke:#fff4aa!important;stroke-width:3.5!important}
</style>
<div id="bar">
  <input id="q" placeholder="find a name — Zerubbabel, Jochebed, Achsah…" size="34">
  <button id="prev">&#8593;</button><button id="next">&#8595;</button>
  <span id="hits"></span>
  <button id="fit">fit</button><button id="in">+</button><button id="out">&minus;</button>
</div>
<div id="stage"></div>
<script>
const stage=document.getElementById('stage');
fetch('%(stem)s.svg').then(r=>r.text()).then(t=>{stage.innerHTML=t;init()});
let k=1,tx=0,ty=0,kmin=0.01,svg,groups=[],at=-1;
function apply(){svg.style.transform=`translate(${tx}px,${ty}px) scale(${k})`}
function fit(){const w=%(w)s,h=%(h)s;k=Math.min(innerWidth/w,innerHeight/h);
  kmin=Math.min(0.01,k);tx=(innerWidth-w*k)/2;ty=(innerHeight-h*k)/2;apply()}
function init(){svg=stage.querySelector('svg');
  svg.removeAttribute('width');svg.removeAttribute('height');
  svg.setAttribute('width',%(w)s);svg.setAttribute('height',%(h)s);
  groups=[...svg.querySelectorAll('text')];fit()}
function zoomAt(x,y,f){const nk=Math.min(8,Math.max(kmin,k*f));
  tx=x-(x-tx)*(nk/k);ty=y-(y-ty)*(nk/k);k=nk}
stage.addEventListener('wheel',e=>{e.preventDefault();
  zoomAt(e.clientX,e.clientY,Math.exp(-e.deltaY*0.0015));apply()},{passive:false});
const pts=new Map();let pinch=null;
function span(){const[a,b]=[...pts.values()];
  return{x:(a.x+b.x)/2,y:(a.y+b.y)/2,d:Math.hypot(a.x-b.x,a.y-b.y)||1}}
stage.addEventListener('pointerdown',e=>{pts.set(e.pointerId,{x:e.clientX,y:e.clientY});
  stage.classList.add('drag');stage.setPointerCapture(e.pointerId);
  pinch=pts.size===2?span():null});
stage.addEventListener('pointermove',e=>{const p=pts.get(e.pointerId);if(!p)return;
  if(pts.size===1){tx+=e.clientX-p.x;ty+=e.clientY-p.y}
  p.x=e.clientX;p.y=e.clientY;
  if(pts.size===2&&pinch){const s=span();tx+=s.x-pinch.x;ty+=s.y-pinch.y;
    zoomAt(s.x,s.y,s.d/pinch.d);pinch=s}
  apply()});
function lift(e){pts.delete(e.pointerId);pinch=pts.size===2?span():null;
  if(!pts.size)stage.classList.remove('drag')}
stage.addEventListener('pointerup',lift);stage.addEventListener('pointercancel',lift);
document.addEventListener('gesturestart',e=>e.preventDefault());
document.getElementById('fit').onclick=fit;
document.getElementById('in').onclick=()=>{zoomAt(innerWidth/2,innerHeight/2,1.3);apply()};
document.getElementById('out').onclick=()=>{zoomAt(innerWidth/2,innerHeight/2,1/1.3);apply()};
let matches=[];
function search(){const s=document.getElementById('q').value.trim().toLowerCase();
  matches=s?groups.filter(t=>t.textContent.toLowerCase().includes(s)):[];
  document.getElementById('hits').textContent=s?`${matches.length} found`:'';
  at=-1;if(matches.length)go(0)}
function go(i){at=(i+matches.length)%%matches.length;const t=matches[at];
  let b=t.getBoundingClientRect();
  if(k<1){zoomAt(b.left+b.width/2,b.top+b.height/2,1/k);apply();
    b=t.getBoundingClientRect()}
  tx-=b.left+b.width/2-innerWidth/2;ty-=b.top+b.height/2-innerHeight/2;apply();
  t.style.fill='#fff4aa';setTimeout(()=>t.style.fill='',2200);
  document.getElementById('hits').textContent=`${at+1} / ${matches.length}`}
document.getElementById('q').addEventListener('input',search);
document.getElementById('next').onclick=()=>matches.length&&go(at+1);
document.getElementById('prev').onclick=()=>matches.length&&go(at-1);
</script>
"""


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    svg, W, H, n = build_svg()
    path = os.path.join(OUT_DIR, STEM + ".svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    vp = os.path.join(OUT_DIR, STEM + ".html")
    with open(vp, "w", encoding="utf-8") as f:
        f.write(VIEWER % {"stem": STEM, "w": _fmt(W), "h": _fmt(H),
                          "title": "The Old Testament family tree"})
    size = os.path.getsize(path) / 1024
    print(f"{path}")
    print(f"  {n} nodes · {W:.0f} x {H:.0f} px · {size:.0f} KB")
    print(f"{vp}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
