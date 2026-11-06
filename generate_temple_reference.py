"""The Temple reference page: Solomon's house, its courts and its furnishings,
drawn to scale from the one model (temple.py), with a card for each part.

Writes web/visuals/reference/Temple.svg, its sidecar Temple.json and the
viewer page Temple.html (reference_viewer.page). The web app's Reference
list opens it (web/js/app.js REFERENCES).

The sheet, every drawing on it but the details at 16 px a cubit:

- **The plan**, east to the right: the house with its walls, the side
  rooms round it, the porch and the two pillars, the holy place's lamp
  stands, tables and golden altar, the ark under the cherubim, and in the
  inner court (its size not given) the bronze altar, the scaffold, the Sea
  and the ten bases.
- **A section looking north**, under the plan and on the same line, so a
  thing in it stands under itself on the plan: the side rooms' three
  floors, the inner sanctuary's cube under the house's 30 cubits, the
  windows, the porch, Boaz, and the altar.
- **A section looking west** through the inner sanctuary: the cherubim
  with their wings wall to wall, and the walls stepping in at each floor.
- **The east front**: the porch, Jachin and Boaz, and a man for scale.
- **Measurements** (a layer, on), **the Tabernacle** at the same scale (a
  layer, off: sanctuary.py's tent and court laid on the house), and **in
  detail** (a layer, on): a pillar, the Sea on its oxen, and a base.

A card gives the part's measurements, each marked stated, derived or not
given, with Chronicles' figure beside Kings' where they differ; where it
stands; what it was made of and what it was for; and its verses grouped as
planned, built, in Chronicles, dedicated, later and named elsewhere. A part
drawn in a section or in detail is its card again, with a link to the plan.

    .venv\\Scripts\\python.exe generate_temple_reference.py
"""

import copy
import json
import math
import os

import reference_viewer
import sanctuary as SN
import svg_figures as F
import temple as TM
import verse_refs
from books import BOOK_NAMES
from config import VISUALS_DIR
from generate_tabernacle import (BG, BRONZE, GATE_COLORS, GOLD, HL, PANEL,
                                 SAND, SILVER, TEXT, TEXT_DIM, WHITE_LINEN)
from svg_surface import SvgCanvas, _fmt
from temple import Plan, Section

OUT_DIR = os.path.join(VISUALS_DIR, "reference")
STEM = "Temple"
TITLE = "Solomon's Temple"

S = 16                              # px per cubit on the sheet
U = S / F.CUBIT                     # px per figure unit
MARGIN = 200
CX0, CY0, CX1, CY1 = TM.INNER_COURT
W = int((CX1 - CX0) * S + 2 * MARGIN)
PLAN_TOP = 330
PLAN = Plan(MARGIN - CX0 * S, PLAN_TOP - CY0 * S, S)
PLAN_BOTTOM = PLAN.pt(0, CY1)[1]

# the long section, on the plan's own x
LONG_GY = PLAN_BOTTOM + 190 + (TM.HOUSE_HEIGHT + 1) * S
LONG = Section(PLAN.ox, LONG_GY, S, "along")

# the cross section and the east front, side by side; north on the right
ROW3_GY = LONG_GY + 230 + (TM.HOUSE_HEIGHT + 1) * S
SPAN = TM.SIDE_DEPTH * 2 + TM.HOUSE[3]          # 52 cubits, outside to out
ROW3_GAP = 260
ROW3_X = (W - 2 * SPAN * S - ROW3_GAP) / 2
# h is plan y; x(h) = ox - h*s, so the south outside (y 36) is the left edge
CROSS = Section(ROW3_X + (TM.HOUSE[3] + TM.SIDE_DEPTH) * S, ROW3_GY, S,
                "across")
ELEV = Section(CROSS.ox + SPAN * S + ROW3_GAP, ROW3_GY, S, "across")

# the details, each at its own scale
DETAIL_TOP = ROW3_GY + 170
DETAIL_GY = DETAIL_TOP + 120 + 23 * 20
DETAILS = [("pillar", "jachin", 20), ("sea", "sea", 36), ("base", "bases", 64)]
DETAIL_LABEL = {"pillar": "a pillar", "sea": "the molten sea",
                "base": "a base and its basin"}
H = int(DETAIL_GY + 150)


def mix(col, f, over=PANEL):
    return tuple(int(over[i] + (col[i] - over[i]) * f) for i in range(3))


STONE = mix(WHITE_LINEN, 0.46)          # a wall, cut
STONE_EDGE = mix(WHITE_LINEN, 0.75)
ROOM = mix(SAND, 0.16)
CEDAR = (150, 104, 66)
OLIVE = (150, 140, 80)
INNER = mix(GOLD, 0.2)                  # the inner sanctuary's gold
HOLY = mix(GOLD, 0.11)
BEYOND = mix(SAND, 0.08)                # the face of a wall beyond the cut
GHOST = WHITE_LINEN + (150,)
DIM = mix(SAND, 0.95, BG)

# Short words for where a part stands, for the card's second line.
WHERE = {
    "house": "60 by 20 cubits, 30 high",
    "oracle": "the house's west end",
    "holy": "between the inner sanctuary and the porch",
    "porch": "the house's east end",
    "side_rooms": "three floors round the house",
    "windows": "in the walls of the house",
    "oracle_doors": "between the holy place and the inner sanctuary",
    "veil": "at the inner sanctuary, in Chronicles",
    "house_doors": "between the porch and the holy place",
    "jachin": "at the porch, on the right",
    "boaz": "at the porch, on the left",
    "altar": "in the court, before the house",
    "platform": "in the middle of the court",
    "sea": "in the court, to the south-east",
    "bases": "in the court, five each side of the house",
    "lamp_stands": "in the holy place, five each side",
    "tables": "in the holy place, five each side",
    "incense_altar": "in the holy place, before the inner sanctuary",
    "ark": "in the inner sanctuary",
    "cherubim": "in the inner sanctuary, wall to wall",
    "courts": "round the house",
}


# ---------------------------------------------------------------------------
# Verses
# ---------------------------------------------------------------------------

def rows(ref, default="1 Kings"):
    """[[book index, c1, v1, c2, v2]] for one ref string (0 = none)."""
    return [[BOOK_NAMES.index(r.book), r.c1, r.v1 or 0, r.c2 or 0, r.v2 or 0]
            for r in verse_refs.parse(ref, default)]


def card(part):
    """The sidecar fields of a temple.Part's card."""
    item = {
        "n": part.name[0].upper() + part.name[1:],
        "s": WHERE[part.key],
        "a": list(part.aka),
        "dims": [[d.what, d.value, d.flag, rows(d.ref) if d.ref else []]
                 for d in part.dims],
        "pl": [part.place[0], part.place[1],
               rows(part.place[2]) if part.place[2] else []],
        "rg": [[group, rows(ref)] for group, ref in part.verses],
    }
    tx = []
    if part.material:
        tx.append(["Made of", part.material])
    if part.use:
        tx.append(["For", part.use])
    if tx:
        item["tx"] = tx
    if part.note:
        item["note"] = part.note
    return item


# ---------------------------------------------------------------------------
# Drawing helpers
# ---------------------------------------------------------------------------

def rect(c, box, **kw):
    x, y, w, h = box
    c.rect(x, y, w, h, **kw)


def figure(c, parts, x, gy, s, ink, flip=1, page=PANEL, style=None):
    F.draw(c, parts, x, gy, s, ink, page, flip=flip, style=style)


def overlaid(ink=GOLD, page=PANEL):
    """The figure style with wings as bright as the body: the cherubim of
    the inner sanctuary were overlaid with gold, wings and all (6:28)."""
    st = dict(F.palette(ink, page))
    st["wing"] = (mix(ink, 0.5, page), ink, 1.3)
    return st


def dim_arrow(c, p0, p1, text, side, size=15):
    c.line(p0, p1, DIM, 1.6)
    for a, b in ((p0, p1), (p1, p0)):
        dx, dy = b[0] - a[0], b[1] - a[1]
        n = (dx * dx + dy * dy) ** 0.5 or 1
        ux, uy = dx / n, dy / n
        c.polygon([a, (a[0] + 10 * ux - 4 * uy, a[1] + 10 * uy + 4 * ux),
                   (a[0] + 10 * ux + 4 * uy, a[1] + 10 * uy - 4 * ux)],
                  fill=DIM)
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    at = {"below": ((mx, my + 17), "mm"), "above": ((mx, my - 13), "mm"),
          "left": ((mx - 10, my), "rm"), "right": ((mx + 10, my), "lm")}
    xy, anchor = at[side]
    c.text(xy, text, size, TEXT_DIM, anchor, bold=True)


def hdim(c, sec, h0, h1, z, text, side="below"):
    """A dimension along a section's ground, between plan positions."""
    dim_arrow(c, sec.pt(h0, z), sec.pt(h1, z), text, side)


def vdim(c, sec, h, z0, z1, text, side):
    dim_arrow(c, sec.pt(h, z0), sec.pt(h, z1), text, side)


def heading(c, x, y, text, sub=None):
    c.text((x, y), text, 20, TEXT, "mm", bold=True)
    if sub:
        c.text((x, y + 26), sub, 14, TEXT_DIM, "mm", italic=True)


# ---------------------------------------------------------------------------
# The masthead
# ---------------------------------------------------------------------------

def draw_masthead(c):
    c.text((60, 74), TITLE, 44, TEXT, "lm", bold=True)
    c.text((60, 116), "the house, its courts and its furnishings, to scale",
           20, TEXT_DIM, "lm", italic=True)
    c.text((60, 148), "1 Kings 6–8 · 2 Chronicles 3–7", 16, TEXT_DIM, "lm")
    x0, y = 60, 196
    c.line((x0, y), (x0 + 10 * S, y), SAND, 3)
    for i in range(11):
        h = 8 if i % 5 == 0 else 4
        c.line((x0 + i * S, y - h), (x0 + i * S, y), SAND, 1.5)
    c.text((x0 + 10 * S + 12, y), "10 cubits", 14, TEXT_DIM, "lm")
    c.text((x0, y + 26), "a cubit is about 18 inches, 45 cm", 13, TEXT_DIM,
           "lm", italic=True)
    cx, cy = W - 110, 120
    c.line((cx, cy), (cx, cy - 40), SAND, 2)
    c.polygon([(cx - 6, cy - 32), (cx, cy - 44), (cx + 6, cy - 32)], fill=SAND)
    c.line((cx, cy), (cx + 40, cy), SAND, 2)
    c.polygon([(cx + 32, cy - 6), (cx + 44, cy), (cx + 32, cy + 6)], fill=SAND)
    c.text((cx, cy - 58), "N", 16, TEXT, "mm")
    c.text((cx + 58, cy), "E", 16, TEXT, "lm")


# ---------------------------------------------------------------------------
# The plan
# ---------------------------------------------------------------------------

def draw_plan_court(c):
    rect(c, PLAN.box(*TM.INNER_COURT), fill=mix(SAND, 0.05))
    x, y, w, h = PLAN.box(*TM.INNER_COURT)
    c.polyline([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], SAND, 2.4,
               dash="14 10", closed=True)
    c.text((x + w / 2, y - 40), "THE INNER COURT", 18, TEXT, "mm", bold=True)
    c.text((x + w / 2, y - 16), "its size is not given", 13, TEXT_DIM, "mm",
           italic=True)


def draw_plan_house(c):
    P = PLAN
    # the walls, as one mass, with the rooms and the house cut out of it
    rect(c, P.box(*TM.OUTSIDE), fill=STONE, stroke=STONE_EDGE, width=1.5)
    for room in TM.side_rooms(0).values():
        rect(c, P.box(*room), fill=ROOM)
    # the porch's side walls, running on from the house's
    w = TM.WALL[0]
    for y0, y1 in ((-w, 0), (TM.HOUSE[3], TM.HOUSE[3] + w)):
        rect(c, P.box(TM.PORCH[0], y0, TM.PORCH[2], y1), fill=STONE,
             stroke=STONE_EDGE, width=1.5)
    rect(c, P.box(*TM.PORCH), fill=mix(SAND, 0.2))
    # the house within: the inner sanctuary and the holy place
    rect(c, P.box(*TM.ORACLE), fill=INNER)
    rect(c, P.box(*TM.HOLY), fill=HOLY)
    # the house's east wall, with its doorway
    d0, d1 = TM.HOUSE_DOOR
    rect(c, P.box(TM.EAST_WALL[0], d0, TM.EAST_WALL[1], d1), fill=HOLY)
    for yy in (d0, d1):                     # the folding leaves, open
        (ax, ay) = P.pt(TM.EAST_WALL[0], yy)
        c.line((ax, ay), (ax - 1.25 * S, ay + (1 if yy == d0 else -1)
                          * 1.25 * S), CEDAR, 2)
    # the side rooms' door on the right, the south (6:8)
    a, b = TM.SIDE_DOOR
    rect(c, P.box(a, TM.HOUSE[3] + TM.SIDE_DEPTH - TM.OUTER_WALL, b,
                  TM.HOUSE[3] + TM.SIDE_DEPTH), fill=mix(SAND, 0.05))
    # the cedar wall and the olive doors of the inner sanctuary
    x = P.pt(TM.PARTITION_X, 0)[0]
    o0, o1 = TM.ORACLE_DOOR
    for ya, yb in ((0, o0), (o1, TM.HOUSE[3])):
        c.line((x, P.pt(0, ya)[1]), (x, P.pt(0, yb)[1]), CEDAR, 6)
    for yy, sg in ((o0, 1), (o1, -1)):
        c.line((x, P.pt(0, yy)[1]), (x + 1.4 * S, P.pt(0, yy)[1] + sg * 1.4 * S),
               OLIVE, 2.4)
    # the chains of gold across before it (6:21)
    c.line((x + 0.7 * S, P.pt(0, 0.4)[1]), (x + 0.7 * S, P.pt(0, 19.6)[1]),
           GOLD, 1.2, dash="3 4")
    c.text(P.pt(30, -11), "SIDE ROOMS", 15, TEXT, "mm", bold=True)
    c.text(P.pt(30, TM.HOUSE[3] + 11), "SIDE ROOMS", 15, TEXT, "mm", bold=True)
    c.text(P.pt(TM.PORCH[0] + 5, TM.AXIS - 3.8), "porch", 15, TEXT, "mm")
    c.text(P.pt(41.5, TM.AXIS), "THE HOLY PLACE", 17, TEXT, "mm", bold=True)
    c.text(P.pt(TM.ORACLE[2] / 2, 18.4), "inner sanctuary", 14, TEXT, "mm",
           italic=True)


def draw_plan_furnishings(c):
    P = PLAN
    gold, line = mix(GOLD, 0.75), mix(GOLD, 1.0)
    # the ark under the cherubim's wings (8:6-7), its poles to the east
    x, y, w, h = P.box(*TM.ARK)
    for py in (TM.ARK[1] + 0.3, TM.ARK[3] - 0.3):
        c.line(P.pt(TM.POLES[0], py), P.pt(TM.POLES[1], py), line, 2)
    rect(c, (x, y, w, h), fill=gold, stroke=HL, width=1.4)
    # the cherubim: their four wings in one line across the room, wall to
    # wall, their two bodies under them
    cx = TM.CHERUBIM[0][0]
    c.line(P.pt(cx, 0.2), P.pt(cx, TM.HOUSE[3] - 0.2), mix(GOLD, 0.6), 12)
    c.line(P.pt(cx, 0.2), P.pt(cx, TM.HOUSE[3] - 0.2), HL, 1)
    for _x, yy in TM.CHERUBIM:
        px, py = P.pt(cx, yy)
        c.ellipse(px, py, 0.9 * S, 1.1 * S, fill=gold, stroke=HL, width=1.4)
    c.text(P.pt(cx, 1.6), "cherubim", 14, TEXT, "mm", italic=True)
    c.text(P.pt(TM.ARK[2] + 0.6, TM.AXIS + 1.6), "ark", 14, TEXT, "lm")
    # the golden altar
    x, y, w, h = P.box(*TM.INCENSE_ALTAR)
    rect(c, (x, y, w, h), fill=gold, stroke=line, width=1.2)
    for hx, hy in ((x, y), (x + w, y), (x, y + h), (x + w, y + h)):
        c.circle(hx, hy, 2.2, fill=HL)
    c.text((x + w + 7, y + h / 2), "golden altar", 13, TEXT, "lm")
    # the ten lamp stands and the ten tables, five on each side
    for side, pts in TM.lamp_stands().items():
        for lx, ly in pts:
            px, py = P.pt(lx, ly)
            c.line((px - 15, py), (px + 15, py), line, 2.2)
            for k in range(7):
                c.circle(px - 15 + k * 5, py, 2, fill=HL)
    for side, boxes in TM.tables().items():
        for b in boxes:
            rect(c, P.box(*b), fill=gold, stroke=line, width=1.1)
    for side in ("north", "south"):
        c.text(P.pt(TM.LAMPS_X[-1] + 3.4, TM.LAMPS_Y[side]), "lamp stands",
               13, TEXT_DIM, "lm", italic=True)
        c.text(P.pt(TM.TABLES_X[-1] + 3.4, TM.TABLES_Y[side]), "tables", 13,
               TEXT_DIM, "lm", italic=True)


def draw_plan_court_things(c):
    P = PLAN
    # Jachin and Boaz
    for (x, y), name, below in ((TM.JACHIN, "Jachin", True),
                                (TM.BOAZ, "Boaz", False)):
        px, py = P.pt(x, y)
        r = TM.PILLAR_D / 2 * S
        c.circle(px, py, r, fill=mix(BRONZE, 0.7), stroke=HL, width=1.6)
        c.circle(px, py, r * 0.6, stroke=mix(BRONZE, 1.0, BG), width=1)
        c.text((px + r + 6, py + (r + 2 if below else -r - 2)), name, 16,
               TEXT, "lm", bold=True)
    # the bronze altar, its grating and horns
    x, y, w, h = P.box(*TM.ALTAR)
    rect(c, (x, y, w, h), fill=mix(BRONZE, 0.55), stroke=BRONZE, width=3)
    for k in range(1, 10):
        c.line((x + k * w / 10, y + 8), (x + k * w / 10, y + h - 8),
               mix(BRONZE, 0.95, BG), 1.2)
        c.line((x + 8, y + k * h / 10), (x + w - 8, y + k * h / 10),
               mix(BRONZE, 0.95, BG), 1.2)
    for hx, hy in ((x, y), (x + w, y), (x, y + h), (x + w, y + h)):
        c.circle(hx, hy, 6, fill=mix(BRONZE, 1.0, BG), stroke=HL, width=1)
    c.text((x + w / 2, y - 16), "bronze altar", 16, TEXT, "mm", bold=True)
    # the scaffold
    x, y, w, h = P.box(*TM.PLATFORM)
    rect(c, (x, y, w, h), fill=mix(BRONZE, 0.45), stroke=BRONZE, width=2)
    c.text((x + w / 2, y + h + 16), "scaffold", 13, TEXT, "mm", italic=True)
    # the Sea, with its twelve oxen under the brim, three to each quarter
    sx, sy = P.pt(*TM.SEA)
    R = TM.SEA_D / 2 * S
    c.circle(sx, sy, R, fill=mix(BRONZE, 0.4), stroke=HL, width=2)
    c.circle(sx, sy, R - 7, fill=mix((120, 150, 190), 0.45))
    for q in range(4):
        for k in (-1, 0, 1):
            a = q * math.pi / 2 + k * 0.32
            ix, iy = sx + math.cos(a) * (R - 22), sy + math.sin(a) * (R - 22)
            ox, oy = sx + math.cos(a) * (R - 10), sy + math.sin(a) * (R - 10)
            c.line((ix, iy), (ox, oy), mix(BRONZE, 1.0, BG), 3)
    c.text((sx, sy + R + 18), "the Sea", 16, TEXT, "mm", bold=True)
    # the ten bases with their basins
    for side, boxes in TM.bases().items():
        for b in boxes:
            x, y, w, h = P.box(*b)
            rect(c, (x, y, w, h), fill=mix(BRONZE, 0.45), stroke=BRONZE,
                 width=1.6)
            c.circle(x + w / 2, y + h / 2, w / 2 - 3,
                     fill=mix((120, 150, 190), 0.35), stroke=BRONZE, width=1)
    for side, y in TM.BASES_Y.items():
        off = -3.6 if side == "north" else 3.6
        c.text(P.pt(TM.BASES_X[0] - 2, y + off), "bases", 14, TEXT_DIM, "lm",
               italic=True)


def draw_plan_dims(c):
    P = PLAN
    with c.group(data={"layer": "dims"}):
        y = -18.3
        for x0, x1, t in ((0, 20, "20"), (20, 60, "40"),
                          (TM.PORCH[0], TM.PORCH[2], "10")):
            dim_arrow(c, P.pt(x0, y), P.pt(x1, y), t, "above")
        x = -TM.SIDE_DEPTH - 3.5
        dim_arrow(c, P.pt(x, 0), P.pt(x, TM.HOUSE[3]), "20", "left")
        dim_arrow(c, P.pt(TM.ALTAR[0], TM.ALTAR[3] + 3),
                  P.pt(TM.ALTAR[2], TM.ALTAR[3] + 3), "20", "below")
        dim_arrow(c, P.pt(TM.ALTAR[2] + 3.5, TM.ALTAR[1]),
                  P.pt(TM.ALTAR[2] + 3.5, TM.ALTAR[3]), "20", "right")
        sx, sy = TM.SEA
        dim_arrow(c, P.pt(sx - 5, sy - 7), P.pt(sx + 5, sy - 7), "10", "above")


def draw_plan_tabernacle(c):
    """sanctuary.py's court and tent laid on the house (a layer)."""
    P = PLAN
    with c.group(data={"layer": "tabernacle"}):
        court = TM.tabernacle(SN.COURT)
        x, y, w, h = P.box(*court)
        c.polyline([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], GHOST, 2,
                   dash="6 6", closed=True)
        g0, g1 = SN.GATE
        seg = (g1 - g0) / len(GATE_COLORS)
        for i, col in enumerate(GATE_COLORS):
            c.line(P.pt(court[2], g0 + TM.TAB_DY + i * seg),
                   P.pt(court[2], g0 + TM.TAB_DY + (i + 1) * seg),
                   col + (200,), 5)
        tent = TM.tabernacle(SN.TENT)
        rect(c, P.box(*tent), fill=WHITE_LINEN + (40,), stroke=GHOST, width=2.4)
        mh = TM.tabernacle(SN.MOST_HOLY)
        rect(c, P.box(*mh), stroke=GHOST, width=1.6)
        tx, ty = P.pt((tent[0] + tent[2]) / 2, tent[3] + 1.3)
        c.text((tx, ty), "the Tabernacle's tent", 14, HL, "mm", italic=True)
        c.text((x + 10, y + 16), "the Tabernacle's court", 14, HL, "lm",
               italic=True)


# ---------------------------------------------------------------------------
# The sections
# ---------------------------------------------------------------------------

def draw_side_block(c, sec, face, d):
    """The side rooms and the house's wall, cut: `face` is the house's inner
    face (plan h), `d` the way out from it (-1 or +1)."""
    inner = TM.SIDE_DEPTH - TM.OUTER_WALL

    def box(h0, z0, h1, z1, **kw):
        rect(c, sec.box(face + d * h0, z0, face + d * h1, z1), **kw)
    for k in range(len(TM.SIDE_WIDTHS)):
        z0, z1 = k * TM.FLOOR_HEIGHT, (k + 1) * TM.FLOOR_HEIGHT
        w = TM.wall_at(k)
        box(0, z0, w, z1, fill=STONE)
        box(w, z0, inner, z1, fill=ROOM)
        if k:                               # the floor, on the offset
            box(w, z0 - 0.35, inner, z0 + 0.1, fill=CEDAR)
        c.text(sec.pt(face + d * (w + inner) / 2, z0 + 2.5),
               str(TM.SIDE_WIDTHS[k]), 14, TEXT_DIM, "mm", bold=True)
    box(inner, 0, TM.SIDE_DEPTH, TM.SIDE_TOP, fill=STONE)
    box(TM.wall_at(2), TM.SIDE_TOP, TM.SIDE_DEPTH,
        TM.SIDE_TOP + TM.SIDE_ROOF, fill=CEDAR)
    box(0, TM.SIDE_TOP, TM.wall_at(2), TM.HOUSE_HEIGHT, fill=STONE)
    # one outline round the cut
    pts = [sec.pt(face, 0), sec.pt(face + d * TM.SIDE_DEPTH, 0),
           sec.pt(face + d * TM.SIDE_DEPTH, TM.SIDE_TOP + TM.SIDE_ROOF),
           sec.pt(face + d * TM.wall_at(2), TM.SIDE_TOP + TM.SIDE_ROOF),
           sec.pt(face + d * TM.wall_at(2), TM.HOUSE_HEIGHT),
           sec.pt(face, TM.HOUSE_HEIGHT)]
    c.polyline(pts, STONE_EDGE, 1.5, closed=True)


def draw_oracle_cut(c, sec, h0, h1):
    """The inner sanctuary's cube, and the 10 cubits over it."""
    rect(c, sec.box(h0, 0, h1, TM.ORACLE_HEIGHT), fill=INNER)
    rect(c, sec.box(h0, TM.ORACLE_HEIGHT, h1, TM.ORACLE_HEIGHT + 0.6),
         fill=CEDAR)
    x, y, w, h = sec.box(h0, TM.ORACLE_HEIGHT + 0.6, h1, TM.HOUSE_HEIGHT)
    rect(c, (x, y, w, h), fill=mix(SAND, 0.05))
    step = 18
    k = 0
    while k * step < w + h:                 # hatched: not given
        a = (x + min(k * step, w), y + max(0, k * step - w))
        b = (x + max(0, k * step - h), y + min(k * step, h))
        c.line(a, b, mix(SAND, 0.35), 1)
        k += 1
    c.text((x + w / 2, y + h / 2), "not given", 13, TEXT_DIM, "mm",
           italic=True)


def draw_roof(c, sec, h0, h1):
    rect(c, sec.box(h0, TM.HOUSE_HEIGHT, h1, TM.HOUSE_HEIGHT + 1), fill=CEDAR,
         stroke=mix(CEDAR, 1.2, BG), width=1)


def draw_long_section(c):
    L = LONG
    heading(c, L.x(25), L.y(TM.HOUSE_HEIGHT + 1) - 92,
            "THE HOUSE, CUT THROUGH ITS MIDDLE, LOOKING NORTH")
    c.line(L.pt(CX0, 0), L.pt(CX1, 0), SAND, 2)
    # the north wall's inner face beyond the cut, and the porch's
    rect(c, L.box(TM.PARTITION_X, 0, TM.HOLY[2], TM.HOUSE_HEIGHT), fill=HOLY)
    rect(c, L.box(*(TM.PORCH[0], 0, TM.PORCH[2], TM.PORCH_HEIGHT)),
         fill=BEYOND)
    draw_oracle_cut(c, L, 0, TM.PARTITION_X)
    draw_side_block(c, L, 0, -1)
    # the windows high in the north wall (6:4)
    for wx in TM.WINDOWS_X:
        x, y, w, h = L.box(wx - 1, TM.WINDOW_SILL, wx + 1, TM.WINDOW_HEAD)
        rect(c, (x, y, w, h), fill=BG, stroke=mix(CEDAR, 0.9), width=1.5)
        for k in range(1, 4):
            c.line((x, y + k * h / 4), (x + w, y + k * h / 4), CEDAR, 1)
        c.line((x + w / 2, y), (x + w / 2, y + h), CEDAR, 1)
    # the cedar wall with the olive doors (6:31)
    rect(c, L.box(TM.PARTITION_X - 0.3, 0, TM.PARTITION_X + 0.3,
                  TM.ORACLE_HEIGHT), fill=CEDAR)
    rect(c, L.box(TM.PARTITION_X - 0.3, 0, TM.PARTITION_X + 0.3,
                  TM.DOOR_HEIGHT * 0.8), fill=OLIVE)
    # the house's east wall, its doorway, and the roof
    rect(c, L.box(TM.EAST_WALL[0], TM.DOOR_HEIGHT, TM.EAST_WALL[1],
                  TM.HOUSE_HEIGHT), fill=STONE, stroke=STONE_EDGE, width=1.5)
    rect(c, L.box(TM.EAST_WALL[0] + 0.3, 0, TM.EAST_WALL[0] + 0.9,
                  TM.DOOR_HEIGHT), fill=CEDAR)
    draw_roof(c, L, -TM.wall_at(2), TM.PORCH[2])
    # the cherub on the north, the ark under its wing, facing the house
    cx = TM.CHERUBIM[0][0]
    figure(c, F.temple_cherub("side"), L.x(cx), L.gy, U, GOLD,
           style=overlaid())
    figure(c, F.ark(), L.x(TM.AXIS), L.gy, U * 1.2, GOLD, page=PANEL)
    # the holy place: the golden altar, the tables and the lamp stands
    x, y, w, h = L.box(*(TM.INCENSE_ALTAR[0], 0, TM.INCENSE_ALTAR[2], 2))
    rect(c, (x, y, w, h), fill=mix(GOLD, 0.75), stroke=GOLD, width=1.2)
    for lx, _ly in TM.lamp_stands()["north"]:          # by the wall
        figure(c, F.lampstand(lit=True), L.x(lx), L.gy, U, GOLD, page=HOLY)
    for tb in TM.tables()["north"]:                      # nearer the cut
        rect(c, L.box(tb[0], 0, tb[2], 1.5), fill=mix(GOLD, 0.6),
             stroke=GOLD, width=1.1)
    # Boaz before the porch, on the north
    figure(c, F.temple_pillar(), L.x(TM.BOAZ[0]), L.gy, U, BRONZE, page=BG)
    c.text(L.pt(TM.BOAZ[0], TM.PILLAR_HEIGHT + TM.CAPITAL_HEIGHT + 1.5),
           "Boaz", 16, TEXT, "mm", bold=True)
    # a priest in the porch, for scale
    figure(c, F.priest(), L.x(TM.PORCH[0] + 6), L.gy, U, SILVER,
           page=BEYOND)
    # the altar, cut, and the scaffold
    x, y, w, h = L.box(TM.ALTAR[0], 0, TM.ALTAR[2], TM.ALTAR_HEIGHT)
    rect(c, (x, y, w, h), fill=mix(BRONZE, 0.55), stroke=BRONZE, width=3)
    for hx in (x, x + w - 14):
        c.polygon([(hx, y), (hx + 14, y), (hx + 7, y - 16)],
                  fill=mix(BRONZE, 0.9))
    c.text((x + w / 2, y + h / 2), "bronze altar", 16, TEXT, "mm", bold=True)
    rect(c, L.box(TM.PLATFORM[0], 0, TM.PLATFORM[2], TM.PLATFORM_HEIGHT),
         fill=mix(BRONZE, 0.45), stroke=BRONZE, width=2)
    # labels
    c.text(L.pt(TM.ORACLE[2] / 2, TM.ORACLE_HEIGHT - 1.4), "inner sanctuary",
           14, TEXT, "mm", italic=True)
    c.text(L.pt(41.5, TM.HOUSE_HEIGHT - 3), "THE HOLY PLACE", 17, TEXT, "mm",
           bold=True)
    c.text(L.pt(TM.PORCH[0] + 5, TM.HOUSE_HEIGHT - 3), "porch", 15, TEXT,
           "mm")
    c.text(L.pt(41.5, TM.WINDOW_SILL - 1.2), "windows", 13, TEXT_DIM, "mm",
           italic=True)
    c.text(L.pt(-TM.SIDE_DEPTH / 2 - 2, TM.SIDE_TOP + 3.5), "side rooms", 14,
           TEXT, "mm", italic=True)


def draw_long_dims(c):
    L = LONG
    with c.group(data={"layer": "dims"}):
        z = -2.4
        hdim(c, L, 0, 20, z, "20")
        hdim(c, L, 20, 60, z, "40")
        hdim(c, L, TM.PORCH[0], TM.PORCH[2], z, "10")
        hdim(c, L, TM.ALTAR[0], TM.ALTAR[2], z, "20")
        vdim(c, L, -TM.SIDE_DEPTH - 3, 0, TM.HOUSE_HEIGHT, "30", "left")
        for k in range(3):
            vdim(c, L, -TM.SIDE_DEPTH - 0.9, k * 5, (k + 1) * 5, "5", "left")
        vdim(c, L, 1.6, 0, TM.ORACLE_HEIGHT, "20", "right")
        px = TM.BOAZ[0] + TM.PILLAR_D / 2 + 2.4
        vdim(c, L, px, 0, TM.PILLAR_HEIGHT, "18", "right")
        vdim(c, L, px, TM.PILLAR_HEIGHT, TM.PILLAR_HEIGHT + TM.CAPITAL_HEIGHT,
             "5", "right")
        vdim(c, L, TM.ALTAR[2] + 2.5, 0, TM.ALTAR_HEIGHT, "10", "right")


def draw_long_tabernacle(c):
    L = LONG
    with c.group(data={"layer": "tabernacle"}):
        tent = TM.tabernacle(SN.TENT)
        rect(c, L.box(tent[0], 0, tent[2], SN.TENT_HEIGHT),
             fill=WHITE_LINEN + (36,), stroke=GHOST, width=2.4)
        mh = TM.tabernacle(SN.MOST_HOLY)
        rect(c, L.box(mh[0], 0, mh[2], SN.TENT_HEIGHT), stroke=GHOST,
             width=1.6)
        c.text(L.pt((tent[0] + tent[2]) / 2, SN.TENT_HEIGHT + 1.2),
               "the Tabernacle's tent", 14, HL, "mm", italic=True)


def draw_cross_section(c):
    X = CROSS
    heading(c, X.x(TM.AXIS), X.y(TM.HOUSE_HEIGHT + 1) - 92,
            "ACROSS THE INNER SANCTUARY, LOOKING WEST")
    c.line(X.pt(TM.HOUSE[3] + TM.SIDE_DEPTH + 2, 0),
           X.pt(-TM.SIDE_DEPTH - 2, 0), SAND, 2)
    draw_oracle_cut(c, X, 0, TM.HOUSE[3])
    draw_side_block(c, X, 0, -1)
    draw_side_block(c, X, TM.HOUSE[3], 1)
    draw_roof(c, X, -TM.wall_at(2), TM.HOUSE[3] + TM.wall_at(2))
    # the cherubim, wing to wall and wing to wing; the ark under them
    for _x, y in TM.CHERUBIM:
        figure(c, F.temple_cherub("front"), X.x(y), X.gy, U, GOLD,
               style=overlaid())
    ax = X.x(TM.AXIS)
    w = 1.5 * S
    rect(c, (ax - w / 2, X.y(1.5), w, 1.5 * S - 2), fill=mix(GOLD, 0.8),
         stroke=HL, width=1.2)                          # the ark, end on
    for dx in (-w / 4, w / 4):
        c.circle(ax + dx, X.y(0.9), 2.6, fill=HL)        # its poles' ends
    c.text(X.pt(TM.AXIS, TM.ORACLE_HEIGHT - 1.4), "inner sanctuary", 14,
           TEXT, "mm", italic=True)
    c.text(X.pt(TM.AXIS, 2.6), "ark", 13, TEXT, "mm")
    c.text(X.pt(-TM.SIDE_DEPTH / 2, TM.SIDE_TOP + 3.5), "side rooms", 14,
           TEXT, "mm", italic=True)
    c.text(X.pt(TM.HOUSE[3] + TM.SIDE_DEPTH / 2, TM.SIDE_TOP + 3.5),
           "side rooms", 14, TEXT, "mm", italic=True)
    c.text(X.pt(-TM.SIDE_DEPTH - 1, -1.6), "N", 15, TEXT, "mm", bold=True)
    c.text(X.pt(TM.HOUSE[3] + TM.SIDE_DEPTH + 1, -1.6), "S", 15, TEXT, "mm",
           bold=True)


def draw_cross_dims(c):
    X = CROSS
    with c.group(data={"layer": "dims"}):
        hdim(c, X, 0, TM.HOUSE[3], -2.4, "20")
        vdim(c, X, TM.HOUSE[3] + TM.SIDE_DEPTH + 3, 0, TM.HOUSE_HEIGHT, "30",
             "left")
        for k in range(3):
            vdim(c, X, TM.HOUSE[3] + TM.SIDE_DEPTH + 0.9, k * 5,
                 (k + 1) * 5, "5", "left")
        vdim(c, X, 0.9, 0, TM.ORACLE_HEIGHT, "20", "left")
        # the wings: 5 and 5 for each cherub, 20 wall to wall
        z = TM.CHERUB_HEIGHT + 1.6
        for y0 in (0, 5, 10, 15):
            hdim(c, X, y0, y0 + 5, z, "5", "above")
        vdim(c, X, TM.CHERUBIM[1][1] + 2.2, 0, TM.CHERUB_HEIGHT, "10",
             "left")


def draw_cross_tabernacle(c):
    X = CROSS
    with c.group(data={"layer": "tabernacle"}):
        y0, y1 = TM.AXIS - 5, TM.AXIS + 5
        rect(c, X.box(y0, 0, y1, SN.TENT_HEIGHT), fill=WHITE_LINEN + (36,),
             stroke=GHOST, width=2.4)
        c.text(X.pt(TM.AXIS, SN.TENT_HEIGHT + 1.2), "the Most Holy Place",
               14, HL, "mm", italic=True)


def draw_elevation(c):
    E = ELEV
    heading(c, E.x(TM.AXIS), E.y(TM.HOUSE_HEIGHT + 1) - 92,
            "THE EAST FRONT")
    c.line(E.pt(TM.HOUSE[3] + TM.SIDE_DEPTH + 2, 0),
           E.pt(-TM.SIDE_DEPTH - 2, 0), SAND, 2)
    face = mix(WHITE_LINEN, 0.32)
    # the side rooms' east ends, either side of the porch
    for y0, y1 in ((-TM.SIDE_DEPTH, -TM.WALL[0]),
                   (TM.HOUSE[3] + TM.WALL[0], TM.HOUSE[3] + TM.SIDE_DEPTH)):
        rect(c, E.box(y0, 0, y1, TM.SIDE_TOP + TM.SIDE_ROOF), fill=face,
             stroke=STONE_EDGE, width=1.5)
        for k in (1, 2):
            c.line(E.pt(y0, k * TM.FLOOR_HEIGHT), E.pt(y1, k * TM.FLOOR_HEIGHT),
                   mix(SAND, 0.6), 1)
    # the porch: its two side walls, the opening, the house's door beyond
    rect(c, E.box(-TM.WALL[0], 0, TM.HOUSE[3] + TM.WALL[0], TM.PORCH_HEIGHT
                  + 1), fill=face, stroke=STONE_EDGE, width=1.5)
    rect(c, E.box(0, 0, TM.HOUSE[3], TM.PORCH_HEIGHT - 2), fill=mix(SAND, 0.12))
    d0, d1 = TM.HOUSE_DOOR
    rect(c, E.box(d0, 0, d1, TM.DOOR_HEIGHT), fill=mix(CEDAR, 0.7),
         stroke=GOLD, width=1.4)
    c.line(E.pt(TM.AXIS, 0), E.pt(TM.AXIS, TM.DOOR_HEIGHT), GOLD, 1.2)
    c.text(E.pt(TM.AXIS, TM.PORCH_HEIGHT - 4), "porch", 15, TEXT, "mm")
    # Jachin on the right of the house, the south: on the left from here
    for (_x, y), name in ((TM.JACHIN, "Jachin"), (TM.BOAZ, "Boaz")):
        figure(c, F.temple_pillar(), E.x(y), E.gy, U, BRONZE, page=BG)
        c.text(E.pt(y, -2.0), name, 16, TEXT, "mm", bold=True)
    figure(c, F.man(), E.x(TM.JACHIN[1] + 4.2), E.gy, U, SILVER, page=BG)
    c.text(E.pt(TM.HOUSE[3] + TM.SIDE_DEPTH + 1, -1.6), "S", 15, TEXT, "mm",
           bold=True)
    c.text(E.pt(-TM.SIDE_DEPTH - 1, -1.6), "N", 15, TEXT, "mm", bold=True)
    c.text(E.pt(TM.AXIS, TM.PORCH_HEIGHT + 2.4), "its height is not given",
           13, TEXT_DIM, "mm", italic=True)


def draw_elevation_dims(c):
    E = ELEV
    with c.group(data={"layer": "dims"}):
        hdim(c, E, 0, TM.HOUSE[3], TM.PORCH_HEIGHT - 6.5, "20", "above")
        px = TM.BOAZ[1] - TM.PILLAR_D / 2 - 2.6
        vdim(c, E, px, 0, TM.PILLAR_HEIGHT, "18", "right")
        vdim(c, E, px, TM.PILLAR_HEIGHT, TM.PILLAR_HEIGHT + TM.CAPITAL_HEIGHT,
             "5", "right")


# ---------------------------------------------------------------------------
# The details
# ---------------------------------------------------------------------------

def detail_frames():
    """[(name, part key, scale, ground x, frame box)] for the details."""
    widths = {"pillar": 7, "sea": 14, "base": 6}      # cubits, to lay out
    gap = 260
    total = sum(widths[n] * s for n, _k, s in DETAILS) + gap * (len(DETAILS)
                                                                 - 1)
    x = (W - total) / 2
    out = []
    for name, key, s in DETAILS:
        w = widths[name] * s
        tall = {"pillar": 23.5, "sea": 8.2, "base": 5.1}[name] * s
        out.append((name, key, s, x + w / 2,
                    [round(x, 1), round(DETAIL_GY - tall, 1), round(w, 1),
                     round(tall, 1)]))
        x += w + gap
    return out


def draw_details(c):
    with c.group(data={"layer": "details"}):
        c.text((W / 2, DETAIL_TOP), "IN DETAIL", 22, TEXT, "mm", bold=True)
        for name, _key, s, gx, (fx, fy, fw, fh) in detail_frames():
            u = s / F.CUBIT
            c.line((fx - 30, DETAIL_GY), (fx + fw + 30, DETAIL_GY), SAND, 1.5)
            c.text((gx, DETAIL_GY + 34), DETAIL_LABEL[name], 16, TEXT, "mm",
                   bold=True)
            if name == "pillar":
                figure(c, F.temple_pillar(), gx, DETAIL_GY, u, BRONZE, page=BG)
                r = TM.PILLAR_D / 2 * s
                x = gx + r + 30
                dim_arrow(c, (x, DETAIL_GY), (x, DETAIL_GY - 18 * s), "18",
                          "right")
                dim_arrow(c, (x, DETAIL_GY - 18 * s),
                          (x, DETAIL_GY - 23 * s), "5", "right")
                c.text((gx, DETAIL_GY + 58), "Jachin and Boaz, 12 cubits "
                       "round", 14, TEXT_DIM, "mm", italic=True)
            elif name == "sea":
                figure(c, F.molten_sea(), gx, DETAIL_GY, u, BRONZE, page=BG)
                top = max(p[1] for k, d, _m in F.molten_sea() if k != "dot"
                          for p in d) / F.CUBIT
                R = TM.SEA_D / 2 * s
                dim_arrow(c, (gx - R, DETAIL_GY - top * s - 24),
                          (gx + R, DETAIL_GY - top * s - 24), "10", "above")
                x = gx + R + 26
                dim_arrow(c, (x, DETAIL_GY - top * s),
                          (x, DETAIL_GY - (top - TM.SEA_HEIGHT) * s), "5",
                          "right")
                c.text((gx, DETAIL_GY + 58), "on twelve oxen", 14, TEXT_DIM,
                       "mm", italic=True)
            else:
                figure(c, F.temple_base(), gx, DETAIL_GY, u, BRONZE, page=BG)
                b = TM.BASE / 2 * s
                dim_arrow(c, (gx - b, DETAIL_GY + 8), (gx + b, DETAIL_GY + 8),
                          "", "below")
                c.text((gx, DETAIL_GY + 58), "4 by 4, and 3 high", 14,
                       TEXT_DIM, "mm", italic=True)
                x = gx + b + 26
                dim_arrow(c, (x, DETAIL_GY), (x, DETAIL_GY - 3 * s), "3",
                          "right")
                dim_arrow(c, (gx - b - 26, DETAIL_GY),
                          (gx - b - 26, DETAIL_GY - TM.WHEEL * s), "1½",
                          "left")


def build_svg():
    c = SvgCanvas(W, H, bg=BG)
    draw_masthead(c)
    draw_plan_court(c)
    draw_plan_house(c)
    draw_plan_furnishings(c)
    draw_plan_court_things(c)
    draw_plan_tabernacle(c)
    draw_plan_dims(c)
    draw_long_section(c)
    draw_long_tabernacle(c)
    draw_long_dims(c)
    draw_cross_section(c)
    draw_cross_tabernacle(c)
    draw_cross_dims(c)
    draw_elevation(c)
    draw_elevation_dims(c)
    draw_details(c)
    return c.tostring().replace(
        "<svg ", f'<svg data-kind="architecture" data-title="{TITLE}" ', 1)


# ---------------------------------------------------------------------------
# The sidecar
# ---------------------------------------------------------------------------

def _b(box, pad=0):
    x, y, w, h = box
    return [round(x - pad, 1), round(y - pad, 1), round(w + 2 * pad, 1),
            round(h + 2 * pad, 1)]


def _pb(x0, y0, x1, y1, pad=0):
    return _b(PLAN.box(x0, y0, x1, y1), pad)


def _union(boxes):
    x0 = min(b[0] for b in boxes)
    y0 = min(b[1] for b in boxes)
    x1 = max(b[0] + b[2] for b in boxes)
    y1 = max(b[1] + b[3] for b in boxes)
    return [round(x0, 1), round(y0, 1), round(x1 - x0, 1), round(y1 - y0, 1)]


def _round(cx, cy, r):
    return [round(cx - r, 1), round(cy - r, 1), round(2 * r, 1),
            round(2 * r, 1)]


def plan_boxes():
    """{key: (box, [more boxes])} for the parts on the plan."""
    P = PLAN
    out = {}
    w0 = TM.WALL[0]
    hb = _pb(-w0, -w0, TM.EAST_WALL[1], TM.HOUSE[3] + w0)
    # the house is tapped on its walls; its inside is the rooms'
    out["house"] = (hb, [_pb(-w0, -w0, TM.EAST_WALL[1], 0),
                         _pb(-w0, TM.HOUSE[3], TM.EAST_WALL[1],
                             TM.HOUSE[3] + w0),
                         _pb(-w0, -w0, 0, TM.HOUSE[3] + w0),
                         _pb(TM.EAST_WALL[0], -w0, TM.EAST_WALL[1],
                             TM.HOUSE[3] + w0)])
    out["oracle"] = (_pb(*TM.ORACLE), [])
    out["holy"] = (_pb(*TM.HOLY), [])
    out["porch"] = (_pb(TM.PORCH[0], -w0, TM.PORCH[2], TM.HOUSE[3] + w0), [])
    rooms = TM.side_rooms(0)
    out["side_rooms"] = (_pb(-TM.SIDE_DEPTH, -TM.SIDE_DEPTH, TM.SIDE_EAST,
                             -w0),
                         [_pb(-TM.SIDE_DEPTH, TM.HOUSE[3] + w0, TM.SIDE_EAST,
                              TM.HOUSE[3] + TM.SIDE_DEPTH),
                          _pb(-TM.SIDE_DEPTH, -w0, -w0, TM.HOUSE[3] + w0)])
    del rooms
    out["oracle_doors"] = (_pb(TM.PARTITION_X - 0.6, TM.ORACLE_DOOR[0],
                               TM.PARTITION_X + 1.6, TM.ORACLE_DOOR[1]), [])
    out["house_doors"] = (_pb(TM.EAST_WALL[0] - 1.4, TM.HOUSE_DOOR[0],
                              TM.EAST_WALL[1], TM.HOUSE_DOOR[1]), [])
    r = TM.PILLAR_D / 2 * S + 4
    out["jachin"] = (_round(*P.pt(*TM.JACHIN), r), [])
    out["boaz"] = (_round(*P.pt(*TM.BOAZ), r), [])
    out["altar"] = (_pb(*TM.ALTAR, pad=6), [])
    out["platform"] = (_pb(*TM.PLATFORM, pad=4), [])
    out["sea"] = (_round(*P.pt(*TM.SEA), TM.SEA_D / 2 * S + 4), [])
    rows_ = TM.bases()
    out["bases"] = (_union([_pb(*b, pad=3) for b in rows_["north"]]),
                    [_union([_pb(*b, pad=3) for b in rows_["south"]])])
    lamps = TM.lamp_stands()

    def lamp_row(side):
        return _union([_b((P.pt(x, y)[0] - 16, P.pt(x, y)[1] - 6, 32, 12))
                       for x, y in lamps[side]])
    out["lamp_stands"] = (lamp_row("north"), [lamp_row("south")])
    tb = TM.tables()
    out["tables"] = (_union([_pb(*b, pad=3) for b in tb["north"]]),
                     [_union([_pb(*b, pad=3) for b in tb["south"]])])
    out["incense_altar"] = (_pb(*TM.INCENSE_ALTAR, pad=5), [])
    out["ark"] = (_pb(*TM.ARK, pad=4), [])
    cx = TM.CHERUBIM[0][0]
    out["cherubim"] = (_pb(cx - 1.2, 0, cx + 1.2, TM.HOUSE[3]), [])
    x, y, w, h = PLAN.box(*TM.INNER_COURT)
    out["courts"] = (_b((x, y, w, h)),
                     [[x - 10, y - 10, w + 20, 20], [x - 10, y + h - 10,
                                                     w + 20, 20],
                      [x - 10, y - 10, 20, h + 20], [x + w - 10, y - 10, 20,
                                                     h + 20],
                      [x + w / 2 - 120, y - 56, 240, 54]])
    return out


def section_boxes():
    """[(part key, box)] for the parts drawn in the sections and the east
    front: each becomes a copy of the part's card, linked to the plan."""
    L, X, E = LONG, CROSS, ELEV
    out = []
    # the long section
    out.append(("oracle", _b(L.box(0, 0, TM.PARTITION_X, TM.ORACLE_HEIGHT))))
    out.append(("holy", _b(L.box(TM.PARTITION_X, 0, TM.HOLY[2],
                                 TM.HOUSE_HEIGHT))))
    out.append(("porch", _b(L.box(TM.PORCH[0], 0, TM.PORCH[2],
                                  TM.PORCH_HEIGHT))))
    out.append(("side_rooms", _b(L.box(-TM.SIDE_DEPTH, 0, 0, TM.SIDE_TOP
                                       + TM.SIDE_ROOF))))
    out.append(("house", _b(L.box(-TM.wall_at(2), TM.SIDE_TOP + TM.SIDE_ROOF,
                                  0, TM.HOUSE_HEIGHT + 1))))
    out.append(("house_doors", _b(L.box(TM.EAST_WALL[0], 0, TM.EAST_WALL[1],
                                        TM.DOOR_HEIGHT))))
    out.append(("oracle_doors", _b(L.box(TM.PARTITION_X - 0.8, 0,
                                         TM.PARTITION_X + 0.8,
                                         TM.DOOR_HEIGHT * 0.8))))
    cx = TM.CHERUBIM[0][0]
    out.append(("cherubim", _b(L.box(cx - 2, 2.2, cx + 1.6,
                                     TM.CHERUB_HEIGHT))))
    out.append(("ark", _b(L.box(TM.AXIS - 2, 0, TM.AXIS + 2, 2.1))))
    out.append(("incense_altar", _b(L.box(TM.INCENSE_ALTAR[0] - 0.4, 0,
                                          TM.INCENSE_ALTAR[2] + 0.4, 2.4))))
    out.append(("lamp_stands", _b(L.box(TM.LAMPS_X[0] - 1.8, 0,
                                        TM.LAMPS_X[-1] + 1.8, 2.6))))
    out.append(("boaz", _b(L.box(TM.BOAZ[0] - 2.6, 0, TM.BOAZ[0] + 2.6,
                                 TM.PILLAR_HEIGHT + TM.CAPITAL_HEIGHT))))
    out.append(("altar", _b(L.box(TM.ALTAR[0], 0, TM.ALTAR[2],
                                  TM.ALTAR_HEIGHT + 1))))
    out.append(("platform", _b(L.box(TM.PLATFORM[0], 0, TM.PLATFORM[2],
                                     TM.PLATFORM_HEIGHT), 4)))
    # across the inner sanctuary
    out.append(("oracle", _b(X.box(0, 0, TM.HOUSE[3], TM.ORACLE_HEIGHT))))
    out.append(("side_rooms", _b(X.box(-TM.SIDE_DEPTH, 0, 0, TM.SIDE_TOP
                                       + TM.SIDE_ROOF))))
    out.append(("side_rooms", _b(X.box(TM.HOUSE[3], 0, TM.HOUSE[3]
                                       + TM.SIDE_DEPTH,
                                       TM.SIDE_TOP + TM.SIDE_ROOF))))
    out.append(("cherubim", _b(X.box(0, 6.2, TM.HOUSE[3],
                                     TM.CHERUB_HEIGHT))))
    out.append(("ark", _b(X.box(TM.AXIS - 1.2, 0, TM.AXIS + 1.2, 1.8))))
    # the east front
    out.append(("porch", _b(E.box(-TM.WALL[0], TM.DOOR_HEIGHT + 1,
                                  TM.HOUSE[3] + TM.WALL[0],
                                  TM.PORCH_HEIGHT + 1))))
    out.append(("house_doors", _b(E.box(TM.HOUSE_DOOR[0], 0, TM.HOUSE_DOOR[1],
                                        TM.DOOR_HEIGHT))))
    for key, (_x, y) in (("jachin", TM.JACHIN), ("boaz", TM.BOAZ)):
        out.append((key, _b(E.box(y - 2.6, -3, y + 2.6,
                                  TM.PILLAR_HEIGHT + TM.CAPITAL_HEIGHT))))
    out.append(("side_rooms", _b(E.box(-TM.SIDE_DEPTH, 0, -TM.WALL[0],
                                       TM.SIDE_TOP + TM.SIDE_ROOF))))
    out.append(("side_rooms", _b(E.box(TM.HOUSE[3] + TM.WALL[0], 0,
                                       TM.HOUSE[3] + TM.SIDE_DEPTH,
                                       TM.SIDE_TOP + TM.SIDE_ROOF))))
    return out


def windows_box():
    L = LONG
    return _b(L.box(TM.WINDOWS_X[0] - 1.4, TM.WINDOW_SILL - 2,
                    TM.WINDOWS_X[-1] + 1.4, TM.WINDOW_HEAD + 0.4))


def sidecar():
    items, index = [], {}
    boxes = plan_boxes()
    for part in TM.PARTS:
        it = card(part)
        it["id"] = part.key.replace("_", "-")
        if part.key in boxes:
            b, more = boxes[part.key]
            it["b"] = b
            if more:
                it["hb"] = more
        index[part.key] = len(items)
        items.append(it)
    # the windows are only in the long section
    items[index["windows"]]["b"] = windows_box()
    # the veil is Chronicles' word for what Kings calls doors: one place
    items[index["veil"]]["b"] = items[index["oracle_doors"]]["b"]
    items[index["veil"]]["nohit"] = True
    items[index["oracle_doors"]]["see"] = [index["veil"]]
    items[index["veil"]]["see"] = [index["oracle_doors"]]
    # the two pillars point to each other, and the ark and the cherubim
    items[index["jachin"]]["see"] = [index["boaz"]]
    items[index["boaz"]]["see"] = [index["jachin"]]
    items[index["ark"]]["see"] = [index["cherubim"]]
    items[index["cherubim"]]["see"] = [index["ark"]]
    items[index["house"]]["see"] = [index["side_rooms"], index["windows"]]

    def copy_of(key, b, extra):
        it = copy.deepcopy(items[index[key]])
        for k in ("hb", "nohit", "see", "dt"):
            it.pop(k, None)
        it.update(extra)
        it["of"] = index[key]
        it["nos"] = True                  # search and #at find the part
        it["b"] = b
        return it
    seen = {}
    for key, b in section_boxes():
        n = seen[key] = seen.get(key, 0) + 1
        items.append(copy_of(key, b, {"id": f"cut-{key.replace('_', '-')}-{n}"}))
    for name, key, _s, _gx, frame in detail_frames():
        it = copy_of(key, frame, {"id": f"drawing-{name}", "ly": "details",
                                  "dl": DETAIL_LABEL[name]})
        items[index[key]].setdefault("dt", []).append(len(items))
        if key == "jachin":
            items[index["boaz"]].setdefault("dt", []).append(len(items))
        items.append(it)
    # the Tabernacle laid on the house (a layer)
    tent = TM.tabernacle(SN.TENT)
    court = TM.tabernacle(SN.COURT)
    cx0, cy0, cw, ch = _pb(*court)
    items.append({
        "id": "tabernacle", "n": "The Tabernacle, at the same scale",
        "s": "its tent and court laid on the house", "ly": "tabernacle",
        "a": ["Tabernacle", "tent of meeting"],
        "b": _pb(*tent, pad=4),
        "hb": [[cx0 - 8, cy0 - 8, cw + 16, 16],
               [cx0 - 8, cy0 + ch - 8, cw + 16, 16],
               [cx0 - 8, cy0 - 8, 16, ch + 16],
               [cx0 + cw - 8, cy0 - 8, 16, ch + 16]],
        "dims": [[d.what, d.value, d.flag, rows(d.ref) if d.ref else []]
                 for d in TM.TABERNACLE_DIMS],
        "pl": ["laid here with its Most Holy Place in the inner sanctuary's "
               "corner; where it stood is not this", SN.NOT_GIVEN, []],
        "rg": [[g, rows(r)] for g, r in TM.TABERNACLE_VERSES],
        "note": "The priests and the Levites brought up the Tent of Meeting "
                "and its holy vessels with the ark at the dedication.",
        "ln": [["The Tabernacle", "/visuals/reference/Tabernacle.html"]]})
    # every verse a card names, for #at
    for it in items:
        flat = [r for _g, rs in it.get("rg", []) for r in rs]
        flat += [r for d in it.get("dims", []) for r in d[3]]
        flat += it.get("pl", [None, None, []])[2]
        it["r"] = [list(r) for r in sorted({tuple(r) for r in flat})]
    used = sorted({r[0] for it in items for r in it["r"]})
    remap = {b: i for i, b in enumerate(used)}

    def re_book(rs):
        for r in rs:
            r[0] = remap[r[0]]
    for it in items:
        re_book(it["r"])
        for _g, rs in it.get("rg", []):
            re_book(rs)
        for d in it.get("dims", []):
            re_book(d[3])
        if "pl" in it:
            re_book(it["pl"][2])
    ids = [it["id"] for it in items]
    assert len(set(ids)) == len(ids), "ids collide"
    return {"version": 1, "card": "parts", "noun": ["part", "parts"],
            "books": [BOOK_NAMES[b] for b in used],
            "layers": [{"id": "dims", "label": "Measurements", "on": True},
                       {"id": "tabernacle", "label": "The Tabernacle",
                        "on": False, "fr": _pb(*court, pad=60)},
                       {"id": "details", "label": "In detail", "on": True}],
            "items": items}


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    svg = build_svg()
    path = os.path.join(OUT_DIR, STEM + ".svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    data = sidecar()
    dp = os.path.join(OUT_DIR, STEM + ".json")
    with open(dp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    vp = os.path.join(OUT_DIR, STEM + ".html")
    with open(vp, "w", encoding="utf-8") as f:
        f.write(reference_viewer.page(
            STEM, _fmt(W), _fmt(H), TITLE, data=True,
            placeholder="find a part — Jachin, the Sea, cherubim…"))
    print(path)
    print(f"  {W} x {H} px · {os.path.getsize(path) / 1024:.0f} KB")
    print(dp)
    print(f"  {len(data['items'])} cards · "
          f"{sum(len(it['r']) for it in data['items'])} verse refs · "
          f"{os.path.getsize(dp) / 1024:.0f} KB")
    print(vp)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
