"""The Tabernacle reference page: the court, the tent and its furnishings,
drawn to scale from the one model (sanctuary.py), the high priest's
garments (garments.py) and the five offerings of Leviticus 1-7
(offerings.py), with a card for each part.

Writes web/visuals/reference/Tabernacle.svg, its sidecar Tabernacle.json
and the viewer page Tabernacle.html (reference_viewer.page). The web app's
Reference list opens it (web/js/app.js REFERENCES).

The sheet is four sections, two by two, each a view chip in the viewer's
bar (the sidecar's `views`); the page opens on the first:

- **Plan** (top left), 14 px a cubit, east to the right as in the Exodus
  plan: the court with its hangings, pillars and gate, the tent with the
  veil and the door screen, and the six furnishings. Each is a part on the
  sheet: a tap opens its card. Every piece is grouped by the verse of
  Exodus 40:17-33 that sets it up (<g data-tour="raise" data-rise=N>), for
  the "Raising it" tour.
- **Measurements** (a layer, on): the court's, the gate's and the tent's
  figures, each in the raise group of what it measures.
- **The camp** (a layer, off): the Levites on the four sides and the twelve
  tribes beyond them by their standards (Numbers 2-3), not to scale.
- **In detail** (bottom left, the "Drawings" layer, on): the Exodus 25-27
  and 30 drawings of the ark, the table, the lamp stand, the altar of
  incense, the altar, the basin, the veil, the screen, the boards, the
  curtains, the coverings and the materials (generate_tabernacle.INSETS),
  each drawn whole, without a verse's highlight.
- **Garments** (top right): the high priest dressed, drawn with svg_priest
  in generate_exodus28_svg.figure()'s colours at Exodus 28:43, in the order
  of Leviticus 8:7-9 (garments.DRESSING), each step a group
  (<g data-tour="dress" data-rise=N>), so the robe covers the sash; beside
  him each garment laid out in svg_priest.WEARING_ORDER, then the garments
  of his sons and the linen garments of Leviticus 16.
- **Offerings** (bottom right): the five offerings of Leviticus 1-7 side by
  side: what is brought and by whom (drawn with svg_figures; the sin
  offering's ranks), what burns on the altar, the blood, who eats, what is
  not eaten, and when.

A card gives the part's measurements (or a garment's or an offering's
facts), each marked stated, derived or not given, where it stands, what it
was made of, who carried it on the march, and its verses grouped. A part and
its drawing link to each other, as do a garment on the figure and its own
drawing, and the altar of burnt offering and the five offerings. Three tours
(`tours`): "Gate to ark", "Raising it" (Exodus 40:17-33) and "Dressing
Aaron" (Leviticus 8:7-9).

    .venv\\Scripts\\python.exe generate_tabernacle_reference.py
"""

import copy
import json
import os

import garments as GM
import offerings as OF
import sanctuary as SN
import svg_figures as F
import svg_priest as G
import verse_refs
from books import BOOK_NAMES
from generate_exodus28_svg import (BLUE, FLESH, LACE, LINEN, PURPLE, SCARLET,
                                   MATERIALS as WOVEN, STONES as STONE_COLS)
from generate_numbers1_2_svg import CAMPS, COUNT
from generate_tabernacle import (BG, BRONZE, BROWN, GATE_COLORS, GOLD, HL, IH,
                                 INSETS, IW, IX, IY, PANEL, RED, SAND,
                                 SAND_DIM, SILVER, TEXT, TEXT_DIM,
                                 WHITE_LINEN)
import reference_viewer
from config import VISUALS_DIR
from sanctuary import COURT, DOOR_X, GATE, TENT, VEIL_X, Plan
from svg_surface import SvgCanvas, SvgLayer, _fmt
from svg_vocab import dim, text_w

OUT_DIR = os.path.join(VISUALS_DIR, "reference")
STEM = "Tabernacle"

S = 14                              # px per cubit on the sheet
MX, MY = 730, 400                   # room round the court for the camp
OX, OY = MX, MY + 40                # the court's north-west corner
PLAN = Plan(OX, OY, S)
CW, CH = (COURT[2] - COURT[0]) * S, (COURT[3] - COURT[1]) * S
PLAN_W = CW + 2 * MX                # the plan and the drawings under it

# The drawings, four to a row under the plan.
DETAIL_COLS, DETAIL_GAP = 4, 28
DETAIL_Y = OY + CH + MY + 40

# The garments and the offerings, in a column to the right of both.
RIGHT_X = PLAN_W + 100
CELL_W, CELL_H, CELL_GAP = 290, 380, 24      # a garment's drawing
GCOLS = 4
FIG_COL = 440                                # the high priest's panel
GRID_W = GCOLS * CELL_W + (GCOLS - 1) * CELL_GAP
GAR_W = FIG_COL + 48 + GRID_W
GAR_ROWS = 3
GAR_H = 80 + GAR_ROWS * CELL_H + (GAR_ROWS - 1) * CELL_GAP
OFF_RH, OFF_CW = 150, 360                    # the table's label column, a column
TABLE_W = OFF_RH + 5 * OFF_CW
RIGHT_W = max(GAR_W, TABLE_W)
GAR_X, GAR_Y = RIGHT_X + (RIGHT_W - GAR_W) / 2, 100
OFF_X, OFF_Y = RIGHT_X + (RIGHT_W - TABLE_W) / 2, GAR_Y + GAR_H + 100
W = RIGHT_X + RIGHT_W + 100


def mix(col, f, over=PANEL):
    return tuple(int(over[i] + (col[i] - over[i]) * f) for i in range(3))


# Short words for where a part stands, for the card's second line.
WHERE = {
    "court": "100 by 50 cubits, round the tent",
    "gate": "the court's east side",
    "tent": "30 by 10 cubits, in the court",
    "coverings": "over the tent",
    "most_holy": "the tent's west end, within the veil",
    "holy_place": "the tent, between the veil and the door",
    "veil": "between the holy place and the Most Holy Place",
    "door": "the tent's east end",
    "ark": "in the Most Holy Place",
    "mercy_seat": "on the ark",
    "table": "in the holy place, on the north",
    "lamp_stand": "in the holy place, on the south",
    "incense_altar": "in the holy place, before the veil",
    "basin": "in the court, between the tent and the altar",
    "altar": "in the court, before the door",
}

# The detail drawings, in sheet order (the holy place's furnishings, the
# court's and the screens, the tent's fabric, the materials), and the part
# each shows.
DETAILS = [("ark", "ark"), ("table", "table"), ("lamp", "lamp_stand"),
           ("incense", "incense_altar"),
           ("altar", "altar"), ("basin", "basin"), ("veil", "veil"),
           ("screen", "door"),
           ("boards", "tent"), ("linen", "coverings"), ("goat", "coverings"),
           ("coverings", "coverings"),
           ("materials", None)]
DETAIL_ROWS = -(-len(DETAILS) // DETAIL_COLS)
DETAIL_H = 70 + DETAIL_ROWS * IH + (DETAIL_ROWS - 1) * DETAIL_GAP
# What the card's link to each drawing says.
DETAIL_LABEL = {"ark": "the ark", "table": "the table",
                "lamp": "the lamp stand", "incense": "the altar of incense",
                "altar": "the altar", "basin": "the basin",
                "veil": "the veil", "screen": "the screen for the door",
                "boards": "the boards and bars",
                "linen": "the ten linen curtains",
                "goat": "the eleven curtains of goats' hair",
                "coverings": "the four coverings"}
MATERIALS = dict(
    n="The offering for the sanctuary",
    s="what the people brought",
    note="Gold, silver and brass; blue, purple and scarlet; fine linen, "
         "goats' hair, rams' skins and sea cow hides; acacia wood; oil, "
         "spices, onyx and the stones for the ephod and breastplate.",
    verses=(("Commanded", "Exod 25:1-9"), ("Made", "Exod 35:4-9, 20-29")))

SIDE_WORD = {"east": "EAST", "south": "SOUTH", "west": "WEST",
             "north": "NORTH"}
SIDE_KEY = {"east": "E", "south": "S", "west": "W", "north": "N"}

# Exodus 40:17-33, raising the tabernacle: each verse or verse group that
# sets a thing up, in the text's order, and the part it sets up. The stop's
# number is the rise of the plan's pieces it puts up.
RAISE = [("Exod 40:17-18", "tent"), ("Exod 40:19", "coverings"),
         ("Exod 40:20", "ark"), ("Exod 40:21", "veil"),
         ("Exod 40:22-23", "table"), ("Exod 40:24-25", "lamp_stand"),
         ("Exod 40:26-27", "incense_altar"), ("Exod 40:28", "door"),
         ("Exod 40:29", "altar"), ("Exod 40:30-32", "basin"),
         ("Exod 40:33", "court")]
RISE = {key: n for n, (_ref, key) in enumerate(RAISE)}
RISE["gate"] = RISE["court"]                 # 40:33, with the court

# From the gate to the ark, the way one walks in.
GATE_TO_ARK = ["gate", "altar", "basin", "door", "table", "lamp_stand",
               "incense_altar", "veil", "ark"]

# Leviticus 8:7-9: the step each garment goes on at, the dressing tour's
# rise.
DRESS = {key: n for n, (_ref, keys) in enumerate(GM.DRESSING) for key in keys}

# A garment's card's second line.
GARMENT_SUB = {"sons": "worn by Aaron's sons",
               "linen": "worn by the high priest, once in the year"}

# An offering's column: the chapters that give it.
OFFER_SUB = {"burnt": "Leviticus 1", "meal": "Leviticus 2",
             "peace": "Leviticus 3", "sin": "Leviticus 4:1–5:13",
             "trespass": "Leviticus 5:14–6:7"}


def cap1(s):
    return s[0].upper() + s[1:]


def raise_group(c, key):
    """The <g> a plan piece is drawn in, for the Raising it tour."""
    return c.group(data={"tour": "raise", "rise": RISE[key]})


def wrap(s, size, width, bold=False, italic=False):
    """`s` in lines no wider than `width` at `size`."""
    lines, cur = [], ""
    for word in s.split():
        t = (cur + " " + word).strip()
        if cur and text_w(t, size, bold=bold, italic=italic) > width:
            lines.append(cur)
            cur = word
        else:
            cur = t
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------------------
# Verses
# ---------------------------------------------------------------------------

def rows(ref, default="Exodus"):
    """[[book index, c1, v1, c2, v2]] for one ref string (0 = none)."""
    out = []
    for r in verse_refs.parse(ref, default):
        out.append([BOOK_NAMES.index(r.book), r.c1, r.v1 or 0, r.c2 or 0,
                    r.v2 or 0])
    return out


def dims_of(dims, default="Exodus"):
    return [[d.what, d.value, d.flag, rows(d.ref, default) if d.ref else []]
            for d in dims]


def card(part):
    """The sidecar fields of a sanctuary.Part's card."""
    item = {
        "n": cap1(part.name),
        "s": WHERE[part.key],
        "a": list(part.aka),
        "dims": dims_of(part.dims),
        "pl": [part.place[0], part.place[1],
               rows(part.place[2]) if part.place[2] else []],
        "rg": [[group, rows(ref)] for group, ref in part.verses],
    }
    tx = []
    if part.material:
        tx.append(["Made of", part.material])
    if part.carried:
        tx.append(["Carried by", part.carried])
    if tx:
        item["tx"] = tx
    if part.note:
        item["note"] = part.note
    return item


def garment_card(g):
    """The sidecar fields of a garments.Garment's card."""
    dims = list(g.dims)
    if g.key == "ephod":
        for k, names in enumerate(GM.SHOULDER_STONES):
            dims.append(SN.Dim(f"on the {['first', 'second'][k]} stone",
                               ", ".join(names), SN.DERIVED,
                               "Exod 28:10; " + GM.NAMES_REF))
    if g.key == "breastplate":
        dims.insert(3, SN.Dim("the stones", "; ".join(
            ", ".join(r) for r in GM.STONES), SN.STATED, GM.STONES_REF))
    item = {"n": cap1(g.name),
            "s": GARMENT_SUB.get(g.key, "worn by the high priest"),
            "a": list(g.aka), "dims": dims_of(dims),
            "tx": [["Worn by", g.worn_by]],
            "rg": [[group, rows(ref)] for group, ref in g.verses]}
    if g.note:
        item["note"] = g.note
    return item


def offering_card(o):
    """The sidecar fields of an offerings.Offering's card."""
    dims = []
    if o.by is not None:
        dims.append([o.by.what, o.by.value, o.by.flag,
                     rows(o.by.ref, "Leviticus")])
    for label, rs in (("brought", o.brought), ("on the altar", o.burns),
                      ("the blood", o.blood), ("eaten", o.eaten),
                      ("not eaten", o.not_eaten)):
        for k, r in enumerate(rs):
            dims.append([label if k == 0 else "", f"{r.who}: {r.what}",
                         r.flag, rows(r.ref, "Leviticus")])
    dims.append(["when", o.when.value, o.when.flag,
                 rows(o.when.ref, "Leviticus")])
    item = {"n": cap1(o.name), "s": OFFER_SUB[o.key],
            "a": list(o.aka) + [t.key for t in OF.THINGS[o.key]],
            "dims": dims,
            "rg": [[group, rows(ref, "Leviticus")] for group, ref in o.verses]}
    if o.note:
        item["note"] = o.note
    return item


# ---------------------------------------------------------------------------
# The plan
# ---------------------------------------------------------------------------

def label(c, xy, text, size=16, fill=TEXT, anchor="mm", **kw):
    c.text(xy, text, size, fill, anchor, **kw)


def draw_masthead(c):
    c.text((60, 74), "The Tabernacle", 44, TEXT, "lm", bold=True)
    c.text((60, 116), "the court, the tent and its furnishings, to scale",
           20, TEXT_DIM, "lm", italic=True)
    c.text((60, 148), "Exodus 25–40 · Leviticus 1–8, 16 · Numbers 2–4", 16,
           TEXT_DIM, "lm")
    # a scale bar of ten cubits
    x0, y = 60, 196
    c.line((x0, y), (x0 + 10 * S, y), SAND, 3)
    for i in range(11):
        h = 8 if i % 5 == 0 else 4
        c.line((x0 + i * S, y - h), (x0 + i * S, y), SAND, 1.5)
    c.text((x0 + 10 * S + 12, y), "10 cubits", 14, TEXT_DIM, "lm")
    c.text((x0, y + 26), "a cubit is about 18 inches, 45 cm", 13, TEXT_DIM,
           "lm", italic=True)
    # the compass, for the plan
    cx, cy = PLAN_W - 110, 120
    c.line((cx, cy), (cx, cy - 40), SAND, 2)
    c.polygon([(cx - 6, cy - 32), (cx, cy - 44), (cx + 6, cy - 32)], fill=SAND)
    c.line((cx, cy), (cx + 40, cy), SAND, 2)
    c.polygon([(cx + 32, cy - 6), (cx + 44, cy), (cx + 32, cy + 6)], fill=SAND)
    c.text((cx, cy - 58), "N", 16, TEXT, "mm")
    c.text((cx + 58, cy), "E", 16, TEXT, "lm")


def draw_court(c):
    with raise_group(c, "court"):
        x, y, w, h = PLAN.box(*COURT)
        c.rect(x, y, w, h, fill=mix(SAND, 0.07))
        linen = WHITE_LINEN
        (x0, y0), (x1, y1) = (PLAN.pt(COURT[0], COURT[1]),
                              PLAN.pt(COURT[2], COURT[3]))
        c.line((x0, y0), (x1, y0), linen, 4)
        c.line((x0, y1), (x1, y1), linen, 4)
        c.line((x0, y0), (x0, y1), linen, 4)
        for f0, f1 in SN.FLANKS:
            c.line(PLAN.pt(COURT[2], f0), PLAN.pt(COURT[2], f1), linen, 4)
        seg = (GATE[1] - GATE[0]) / len(GATE_COLORS)
        for i, col in enumerate(GATE_COLORS):
            c.line(PLAN.pt(COURT[2], GATE[0] + i * seg),
                   PLAN.pt(COURT[2], GATE[0] + (i + 1) * seg), col, 8)
        for px, py in (PLAN.pt(*p) for p in SN.pillar_points()):
            c.circle(px, py, 4.5, fill=mix(BRONZE, 0.8), stroke=SILVER,
                     width=1.4)
        label(c, PLAN.pt(50, -2.2), "THE COURT", 18, TEXT, bold=True)
        label(c, PLAN.pt(103.2, 25), "GATE", 16, TEXT, "lm", bold=True)


COVER_PAD = 0.8                     # cubits; the plan's own, not the text's


def coverings_box():
    """The coverings over the tent (Exodus 40:19), on the plan: a band past
    its walls on the north, the south and the west, where they hang down;
    the east end is the door."""
    x, y, w, h = PLAN.box(*TENT)
    pad = COVER_PAD * S
    return x - pad, y - pad, w + pad, h + 2 * pad


def draw_tent(c):
    x, y, w, h = PLAN.box(*TENT)
    # drawn under the tent, so only the band past its walls shows
    with raise_group(c, "coverings"):
        c.rect(*coverings_box(), fill=mix(BROWN, 0.5),
               stroke=mix(RED, 0.65), width=1.6)
    with raise_group(c, "tent"):
        c.rect(x, y, w, h, fill=mix(SAND, 0.18))
        mx, my, mw, mh = PLAN.box(*SN.MOST_HOLY)
        c.rect(mx, my, mw, mh, fill=mix(GOLD, 0.14))
        c.rect(x, y, w, h, stroke=mix(GOLD, 0.8), width=4)
        label(c, PLAN.pt(25, TENT[1] - 2.2), "THE TABERNACLE", 16, TEXT,
              bold=True)
        label(c, PLAN.pt(15, TENT[3] - 1.4), "Most Holy Place", 13, TEXT_DIM,
              italic=True)
        label(c, PLAN.pt(30, TENT[3] + 1.6), "holy place", 13, TEXT_DIM,
              italic=True)
    # the veil and the door screen, in their colours
    for key, xx, cols, wd, word, dx, anchor in (
            ("veil", VEIL_X, GATE_COLORS[:3], 2.4, "veil", 0, "mm"),
            ("door", DOOR_X, GATE_COLORS, 2.0, "door", 1.0, "lm")):
        with raise_group(c, key):
            for i, col in enumerate(cols):
                off = (i - (len(cols) - 1) / 2) * wd
                c.line((PLAN.pt(xx, 0)[0] + off, y + 2),
                       (PLAN.pt(xx, 0)[0] + off, y + h - 2), col, wd)
            label(c, PLAN.pt(xx + dx, TENT[3] + 1.6), word, 13, TEXT_DIM,
                  anchor, italic=True)


def draw_furnishings(c):
    gold, line = mix(GOLD, 0.75), mix(GOLD, 1.0)
    # the ark, the mercy seat on it, and the cherubim at its two ends
    with raise_group(c, "ark"):
        x, y, w, h = PLAN.box(*SN.plan_box("ark"))
        c.rect(x, y, w, h, fill=gold, stroke=HL, width=1.6)
        c.rect(x + 3, y + 3, w - 6, h - 6, stroke=mix(GOLD, 0.45, BG), width=1)
        for ex in (x + 6, x + w - 6):
            c.polyline([(ex, y + 4), (x + w / 2, y + h / 2), (ex, y + h - 4)],
                       mix(GOLD, 0.4, BG), 1.3)
        label(c, (x + w / 2, y + h + 15), "ark", 14, TEXT)
    # the altar of incense, with its four horns
    with raise_group(c, "incense_altar"):
        x, y, w, h = PLAN.box(*SN.plan_box("incense_altar"))
        c.rect(x, y, w, h, fill=gold, stroke=line, width=1.2)
        for hx, hy in ((x, y), (x + w, y), (x, y + h), (x + w, y + h)):
            c.circle(hx, hy, 2.2, fill=HL)
        label(c, (x + w + 6, y + h / 2), "altar of incense", 13, TEXT, "lm")
    # the table, with the bread in two rows of six (Leviticus 24:6)
    with raise_group(c, "table"):
        x, y, w, h = PLAN.box(*SN.plan_box("table"))
        c.rect(x, y, w, h, fill=gold, stroke=line, width=1.2)
        for r in range(2):
            for k in range(6):
                c.rect(x + 2.5 + k * 4, y + 2.5 + r * 5, 3, 3.5,
                       fill=mix(SAND, 0.9, BG))
        label(c, (x + w + 7, y + h / 2), "table", 14, TEXT, "lm")
    # the lamp stand: seven lamps
    with raise_group(c, "lamp_stand"):
        lx, ly = PLAN.pt(*SN.plan_point("lamp_stand"))
        c.line((lx - 15, ly), (lx + 15, ly), line, 2.4)
        for k in range(7):
            c.circle(lx - 15 + k * 5, ly, 2.2, fill=HL)
        label(c, (lx + 22, ly), "lamp stand", 14, TEXT, "lm")
    # the basin
    with raise_group(c, "basin"):
        bx, by = PLAN.pt(*SN.plan_point("basin"))
        c.circle(bx, by, 15, fill=mix(BRONZE, 0.35), stroke=SILVER, width=2)
        c.circle(bx, by, 9, fill=mix((120, 150, 190), 0.45), stroke=None)
        label(c, (bx, by + 30), "basin", 15, TEXT)
    # the altar of burnt offering, its grating and four horns
    with raise_group(c, "altar"):
        x, y, w, h = PLAN.box(*SN.plan_box("altar"))
        c.rect(x, y, w, h, fill=mix(BRONZE, 0.55), stroke=BRONZE, width=3)
        for k in range(1, 7):
            c.line((x + k * w / 7, y + 6), (x + k * w / 7, y + h - 6),
                   mix(BRONZE, 0.95, BG), 1.2)
            c.line((x + 6, y + k * h / 7), (x + w - 6, y + k * h / 7),
                   mix(BRONZE, 0.95, BG), 1.2)
        for hx, hy in ((x, y), (x + w, y), (x, y + h), (x + w, y + h)):
            c.circle(hx, hy, 4, fill=mix(BRONZE, 1.0, BG), stroke=HL, width=1)
        label(c, (x + w / 2, y + h + 18), "altar of burnt offering", 15, TEXT)


def dim_arrow(c, p0, p1, text, side):
    col = mix(SAND, 0.95, BG)
    c.line(p0, p1, col, 1.6)
    for a, b in ((p0, p1), (p1, p0)):
        dx, dy = b[0] - a[0], b[1] - a[1]
        n = (dx * dx + dy * dy) ** 0.5 or 1
        ux, uy = dx / n, dy / n
        c.polygon([a, (a[0] + 10 * ux - 4 * uy, a[1] + 10 * uy + 4 * ux),
                   (a[0] + 10 * ux + 4 * uy, a[1] + 10 * uy - 4 * ux)],
                  fill=col)
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    if side == "below":
        c.text((mx, my + 18), text, 15, TEXT_DIM, "mm", bold=True)
    elif side == "above":
        c.text((mx, my - 14), text, 15, TEXT_DIM, "mm", bold=True)
    elif side == "left":
        c.text((mx - 12, my), text, 15, TEXT_DIM, "rm", bold=True)
    else:
        c.text((mx + 12, my), text, 15, TEXT_DIM, "lm", bold=True)


def draw_dims(c):
    """The measurements layer. Each figure rises with what it measures in
    the Raising it tour: the court's and the gate's with the court (40:33),
    the tent's with the tent (40:18), the veil's split with the veil
    (40:21)."""
    with c.group(data={"layer": "dims"}):
        with raise_group(c, "court"):
            y = PLAN.pt(0, COURT[3] + 4)[1]
            dim_arrow(c, (PLAN.pt(0, 0)[0], y), (PLAN.pt(100, 0)[0], y),
                      "100 cubits", "below")
            x = PLAN.pt(-4, 0)[0]
            dim_arrow(c, (x, PLAN.pt(0, 0)[1]), (x, PLAN.pt(0, 50)[1]),
                      "50 cubits", "left")
            x = PLAN.pt(COURT[2] + 9, 0)[0]
            dim_arrow(c, (x, PLAN.pt(0, GATE[0])[1]),
                      (x, PLAN.pt(0, GATE[1])[1]), "20", "right")
        with raise_group(c, "tent"):
            y = PLAN.pt(0, TENT[1] - 5.4)[1]
            dim_arrow(c, (PLAN.pt(TENT[0], 0)[0], y),
                      (PLAN.pt(TENT[2], 0)[0], y), "30 cubits", "above")
            x = PLAN.pt(TENT[0] - 3, 0)[0]
            dim_arrow(c, (x, PLAN.pt(0, TENT[1])[1]),
                      (x, PLAN.pt(0, TENT[3])[1]), "10", "left")
        with raise_group(c, "veil"):
            y = PLAN.pt(0, TENT[3] + 4.4)[1]
            dim_arrow(c, (PLAN.pt(TENT[0], 0)[0], y),
                      (PLAN.pt(VEIL_X, 0)[0], y), "10", "below")
            dim_arrow(c, (PLAN.pt(VEIL_X, 0)[0], y),
                      (PLAN.pt(DOOR_X, 0)[0], y), "20", "below")


def plan_frame():
    """The Plan view: the court, its labels and its measurements."""
    x0, y0 = PLAN.pt(COURT[0], COURT[1])
    x1, y1 = PLAN.pt(COURT[2], COURT[3])
    return [round(x0 - 150), round(y0 - 70), round(x1 - x0 + 330),
            round(y1 - y0 + 150)]


def camp_boxes():
    """{side: (levite box, tribe box)} in sheet px, east to the right."""
    x0, y0 = PLAN.pt(COURT[0], COURT[1])
    x1, y1 = PLAN.pt(COURT[2], COURT[3])
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    lw, lh = 300, 86                       # north and south Levite cards
    sw, sh = 230, 130                      # east and west Levite cards
    tw, th = 250, 150                      # tribe cards
    # clear of THE COURT and the 100-cubit line above and below, of the
    # 50-cubit and gate dimensions to the west and east
    north, south, side = 70, 110, 190
    return {
        "north": ((cx - lw / 2, y0 - north - lh, lw, lh),
                  (cx - tw / 2, y0 - north - lh - 24 - th, tw, th)),
        "south": ((cx - lw / 2, y1 + south, lw, lh),
                  (cx - tw / 2, y1 + south + lh + 24, tw, th)),
        "west": ((x0 - side - sw, cy - sh / 2, sw, sh),
                 (x0 - side - sw - 24 - tw, cy - th / 2, tw, th)),
        "east": ((x1 + side, cy - sh / 2, sw, sh),
                 (x1 + side + sw + 24, cy - th / 2, tw, th)),
    }


def draw_camp(c):
    with c.group(data={"layer": "camp"}):
        for side, ((lx, ly, lw, lh), (tx, ty, tw, th)) in camp_boxes().items():
            who, _ref = SN.LEVITE_CAMP[side]
            c.rect(lx, ly, lw, lh, fill=PANEL, stroke=mix(SILVER, 0.7, BG),
                   width=1.5, rx=8)
            c.text((lx + 14, ly + 22), f"{SIDE_WORD[side]} · LEVITES",
                   12, TEXT_DIM, "lm", bold=True)
            # a long name ("Moses, and Aaron and his sons") wraps at its comma
            parts = who.split(", ")
            lines = [s + "," for s in parts[:-1]] + parts[-1:]
            for i, ln in enumerate(lines):
                c.text((lx + 14, ly + 50 + i * 22), ln, 16, TEXT, "lm")
            word, standard, tribes, total, order = CAMPS[SIDE_KEY[side]]
            c.rect(tx, ty, tw, th, fill=PANEL, stroke=mix(GOLD, 0.6, BG),
                   width=1.5, rx=8)
            c.text((tx + 14, ty + 22), f"{word} · the camp of {standard}",
                   12, TEXT_DIM, "lm", bold=True)
            for i, t in enumerate(tribes):
                yy = ty + 50 + i * 24
                c.text((tx + 14, yy), t, 16, TEXT, "lm")
                c.text((tx + tw - 14, yy), f"{COUNT[t]:,}", 15, TEXT_DIM, "rm")
            c.text((tx + tw - 14, ty + th - 16), f"{total:,}", 15, GOLD, "rm",
                   bold=True)
        x0, y0 = PLAN.pt(COURT[0], COURT[1])
        c.text((x0, y0 - 18), "the camp round it is not to scale", 13,
               TEXT_DIM, "lm", italic=True)


# ---------------------------------------------------------------------------
# In detail
# ---------------------------------------------------------------------------

def detail_boxes():
    """(inset name, part key, x, y) for each drawing; a short last row is
    centred."""
    out = []
    row_w = DETAIL_COLS * IW + (DETAIL_COLS - 1) * DETAIL_GAP
    x0 = (PLAN_W - row_w) / 2
    for i, (name, key) in enumerate(DETAILS):
        r, k = divmod(i, DETAIL_COLS)
        n = min(DETAIL_COLS, len(DETAILS) - r * DETAIL_COLS)
        xr = x0 + (row_w - (n * IW + (n - 1) * DETAIL_GAP)) / 2
        out.append((name, key, xr + k * (IW + DETAIL_GAP),
                    DETAIL_Y + 70 + r * (IH + DETAIL_GAP)))
    return out


def detail_frame():
    row_w = DETAIL_COLS * IW + (DETAIL_COLS - 1) * DETAIL_GAP
    return [round((PLAN_W - row_w) / 2 - 20), DETAIL_Y - 10, row_w + 40,
            DETAIL_H + 20]


def draw_details(c):
    with c.group(data={"layer": "details"}):
        c.text((PLAN_W / 2, DETAIL_Y + 24), "IN DETAIL", 22, TEXT, "mm",
               bold=True)
        c.text((PLAN_W / 2, DETAIL_Y + 50), "the drawings of Exodus 25–30",
               15, TEXT_DIM, "mm", italic=True)
        for name, _key, x, y in detail_boxes():
            base, _over = SvgLayer(), SvgLayer()
            INSETS[name](base, _over, None, 1.0, 1.0)
            with c.group(tx=x - IX, ty=y - IY):
                c.raw(base.elements())


# ---------------------------------------------------------------------------
# The garments
# ---------------------------------------------------------------------------
#
# The colours are generate_exodus28_svg.figure()'s at its last verse, so the
# high priest here is the one Exodus 28 finishes dressing.

FIG_PANEL = (GAR_X, GAR_Y + 80, FIG_COL, GAR_H - 80)
FIG_H = 1000                                 # his body, without the turban
FIG = G.Form(GAR_X + FIG_COL / 2, GAR_Y + GAR_H - 40, FIG_H)
CLOTH = [col for _n, col in WOVEN]
SASH_CLOTH = [LINEN, BLUE, PURPLE, SCARLET]  # Exodus 39:29, no gold
STONE_COL = dict(STONE_COLS)
INK = (20, 18, 14)                           # names cut in the stones
PALE = (244, 238, 220)                       # ... on the dark stones
# On the dressed figure each garment is opaque, so what goes on later
# covers what went on before: the coat over the flesh, the robe over the
# coat and the sash. Laid out alone, a garment keeps Exodus 28's alphas.
COAT_ON = mix(LINEN, 0.55, FLESH)
ROBE_ON = mix(BLUE, 0.90, COAT_ON)
TURBAN = mix(LINEN, 0.80)                    # opaque, on the figure and alone
RULE = dim(SAND_DIM, 0.95)


def robe_hem(F_):
    return F_.gy - F_.h * 0.085


def plate_box(F_):
    """(cx, cy, w, h) of the plate on the front of the turban: its foot
    just above the turban's rim, on the forehead (Exod 28:38; 39:31; Lev
    8:9). svg_priest.plate_on's own default sits it on the brow, under a
    turban drawn over the brow, as Exodus 28's and Hebrews' pictures have
    it; this sheet lifts it onto the turban."""
    r = F_.head_r
    w = r * 1.6
    h = w * 0.38
    rim = F_.head_cy - r * 0.34                # svg_priest.turban's lower edge
    return F_.x, rim - r * 0.06 - h / 2, w, h


def ephod_band(c, F_):
    """28:8, the skillfully woven band, "of the same piece and the same
    work" as the ephod: woven in its stripes."""
    bot = F_.waist_y + F_.h * 0.015
    hw_b, d = F_.hw(bot) * 0.80, F_.h * 0.036
    pts = [(F_.x - hw_b * 1.04, bot), (F_.x + hw_b * 1.04, bot),
           (F_.x + hw_b * 1.06, bot + d), (F_.x - hw_b * 1.06, bot + d)]
    G.weave(c, pts, CLOTH, dim(GOLD, 0.85), step=F_.h * 0.018,
            width=F_.h * 0.013, base=dim(BROWN, 0.75))


def sash_woven(c, F_):
    """39:29, the sash "of fine twined linen, and blue, and purple, and
    scarlet": svg_priest.sash's shape, the band in four stripes and its
    ends woven lengthwise."""
    y = F_.waist_y + F_.h * 0.055
    hw, d = F_.hw(y), F_.h * 0.040
    n = len(SASH_CLOTH)
    for i, col in enumerate(SASH_CLOTH):
        ya, yb = y + d * i / n, y + d * (i + 1) / n
        fa, fb = 1.03 + 0.02 * i / n, 1.03 + 0.02 * (i + 1) / n
        c.polygon([(F_.x - hw * fa, ya), (F_.x + hw * fa, ya),
                   (F_.x + hw * fb, yb), (F_.x - hw * fb, yb)],
                  fill=mix(col, 0.9))
    c.polygon([(F_.x - hw * 1.03, y), (F_.x + hw * 1.03, y),
               (F_.x + hw * 1.05, y + d), (F_.x - hw * 1.05, y + d)],
              stroke=RULE, width=1.5)
    for sx, drop in ((-1, 0.150), (1, 0.108)):
        tail = G._taper((F_.x + sx * hw * 0.20, y + d), F_.h * 0.030,
                        (F_.x + sx * hw * 0.34, y + F_.h * drop),
                        F_.h * 0.024)
        G.weave(c, tail, SASH_CLOTH, RULE, step=F_.h * 0.0075,
                width=F_.h * 0.0068, base=mix(LINEN, 0.6))
    c.ellipse(F_.x, y + d * 0.55, hw * 0.20, d * 0.62, fill=mix(BLUE, 0.9),
              stroke=RULE, width=1.5)


def wear(c, F_, key, hidden=True, on=False):
    """One garment on form F_, in Exodus 28's colours and calls; `on`, on
    the dressed figure (opaque, so later garments cover it)."""
    if key == "breeches":
        G.breeches(c, F_, dim(LINEN, 0.85), hidden=hidden)
    elif key == "coat":
        G.coat(c, F_, COAT_ON if on else dim(LINEN, 0.55), RULE)
    elif key == "robe":
        hem = robe_hem(F_)
        G.robe(c, F_, ROBE_ON if on else dim(BLUE, 0.90), dim(SILVER, 0.75),
               hem_y=hem, collar=True)
        G.hem_ring(c, F_, hem, 11, GOLD, (BLUE, PURPLE, SCARLET))
    elif key == "ephod":
        G.ephod(c, F_, dim(BROWN, 0.75), dim(GOLD, 0.85), band=None,
                straps=True, cols=CLOTH)
        ephod_band(c, F_)
        G.shoulder_stones(c, F_, dim(SILVER, 0.9), GOLD)
    elif key == "breastplate":
        G.breastplate_on(c, F_, GOLD,
                         cells=[STONE_COL[s] for s in GM.stone_list()])
    elif key == "sash":
        sash_woven(c, F_)
    elif key == "turban":
        G.turban(c, F_, TURBAN, RULE)
    elif key == "plate":
        _x, py, pw, _ph = plate_box(F_)
        G.plate_on(c, F_, GOLD, LACE, w=pw, y=py)


def ghost(c, F_, head=True):
    """The form a laid-out garment hangs on, in outline."""
    c.polyline(G.silhouette(F_), dim(SAND_DIM, 0.85), 1.3, closed=True)
    if head:
        c.circle(F_.x, F_.head_cy, F_.head_r, stroke=dim(SAND_DIM, 0.85),
                 width=1.3)


def piece_boxes(F_):
    """{garment: (box, [tap boxes])} on the dressed figure, in sheet px."""
    x, h = F_.x, F_.h
    hem = robe_hem(F_)
    sash_y = F_.waist_y + h * 0.055
    band_bot = F_.waist_y + h * 0.015 + h * 0.036
    sw = F_.shldr_hw * 1.03

    def box(x0, y0, x1, y1):
        return [round(x0, 1), round(y0, 1), round(x1 - x0, 1),
                round(y1 - y0, 1)]
    bp = h * 0.150
    r = F_.head_r
    px, py, pw, ph = plate_box(F_)
    out = {
        "breeches": (box(x - F_.hw(F_.thigh_y), F_.waist_y - h * 0.02,
                         x + F_.hw(F_.thigh_y), F_.thigh_y), []),
        "coat": (box(x - sw, F_.neck_y, x + sw, F_.gy),
                 # the sleeves below the shoulder straps, and the hem
                 [box(x - sw, F_.shldr_y + h * 0.06, x - F_.shldr_hw * 0.85,
                      F_.cuff_y),
                  box(x + F_.shldr_hw * 0.85, F_.shldr_y + h * 0.06, x + sw,
                      F_.cuff_y),
                  box(x - F_.hem_hw, hem + h * 0.02, x + F_.hem_hw, F_.gy)]),
        "robe": (box(x - F_.hw(hem), F_.shldr_y - h * 0.03, x + F_.hw(hem),
                     hem + h * 0.02),
                 [box(x - F_.hw(hem), band_bot + h * 0.01, x + F_.hw(hem),
                      hem + h * 0.02)]),
        "ephod": (box(x - F_.shldr_hw * 0.8, F_.shldr_y - h * 0.03,
                      x + F_.shldr_hw * 0.8, band_bot), []),
        "breastplate": (box(x - bp / 2, F_.chest_y - bp / 2, x + bp / 2,
                            F_.chest_y + bp / 2), []),
        "sash": (box(x - F_.hw(sash_y) * 1.06, sash_y,
                     x + F_.hw(sash_y) * 1.06, sash_y + h * 0.15), []),
        "turban": (box(x - r * 1.25, F_.head_cy - r * 2.4, x + r * 1.25,
                       F_.head_cy - r * 0.3), []),
        "plate": (box(px - pw * 0.62, py - ph / 2 - 3, px + pw * 0.62,
                      py + ph / 2 + 3), []),
    }
    return out


def figure_frame():
    x, y, w, h = FIG_PANEL
    return [round(x), round(y), w, round(h)]


def draw_figure(c):
    """The high priest dressed, as Exodus 28 leaves him at 28:43: the body,
    then the garments in the order Leviticus 8:7-9 puts them on
    (garments.DRESSING), one group for each step. The sash goes on with
    the coat and the robe over both, so the dressed figure hides it, as it
    hides the breeches."""
    x, y, w, h = FIG_PANEL
    c.rect(x, y, w, h, fill=PANEL, stroke=SAND_DIM, width=2, rx=10)
    c.text((x + w / 2, y + 26), "AARON", 16, TEXT, "mm", bold=True)
    c.text((x + w / 2, y + 50), "Exodus 28 · Leviticus 8:7–9", 14, TEXT_DIM,
           "mm", italic=True)
    G.body(c, FIG, dim(SAND, 0.95), FLESH, rule=dim(SAND_DIM, 0.95),
           cloth=False)
    for n, (_ref, keys) in enumerate(GM.DRESSING):
        with c.group(data={"tour": "dress", "rise": n}):
            for key in keys:
                # the breeches drawn solid, for the tour's first stop; the
                # coat covers them from the next
                wear(c, FIG, key, hidden=False, on=True)


def garment_cells():
    """{garment key: (x, y, w, h)}: WEARING_ORDER four to a row, then the
    sons' and the linen garments, from the left under them."""
    gx0, gy0 = GAR_X + FIG_COL + 48, GAR_Y + 80
    out = {}
    for i, key in enumerate(list(G.WEARING_ORDER) + ["sons", "linen"]):
        r, k = divmod(i, GCOLS)
        out[key] = (gx0 + k * (CELL_W + CELL_GAP),
                    gy0 + r * (CELL_H + CELL_GAP), CELL_W, CELL_H)
    return out


def cell_panel(c, x, y, w, h, title):
    c.rect(x, y, w, h, fill=PANEL, stroke=SAND_DIM, width=2, rx=10)
    size = 15
    while text_w(title, size) > w - 24 and size > 12:
        size -= 0.5
    c.text((x + w / 2, y + 24), title, size, TEXT, "mm")


def luminance(col):
    def lin(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return (0.2126 * lin(col[0]) + 0.7152 * lin(col[1])
            + 0.0722 * lin(col[2]))


def ink_on(col):
    """INK or PALE, whichever has the more contrast on colour `col`."""
    lum = luminance(col)
    dark = (lum + 0.05) / (luminance(INK) + 0.05)
    light = (luminance(PALE) + 0.05) / (lum + 0.05)
    return INK if dark >= light else PALE


def draw_breastplate(c, x, y, w):
    """28:15-21 at working scale: the twelve stones in their settings, each
    with its tribe's name and the stone's, sized to sit inside the stone."""
    bw = 270
    x0, y0 = x + (w - bw) / 2, y + 62
    stones = GM.stone_list()
    G.breastplate_plate(c, x0, y0, bw, dim(GOLD, 0.95), GOLD,
                        cells=[STONE_COL[s] for s in stones])
    cw, ch = bw / 3, bw / 4
    room = cw * 0.80 - 14                    # the stone, less its padding
    size = 13.5
    while size > 9 and max(text_w(n, size, bold=True)
                           for n in GM.NAMES) > room:
        size -= 0.5
    sub = 11
    while sub > 8 and max(text_w(s, sub, italic=True)
                          for s in stones) > room:
        sub -= 0.5
    for i, (name, stone) in enumerate(zip(GM.NAMES, stones)):
        r, k = divmod(i, 3)
        cx, cy = x0 + k * cw + cw / 2, y0 + r * ch + ch / 2
        ink = ink_on(STONE_COL[stone])
        c.text((cx, cy - ch * 0.10), name, size, ink, "mm", bold=True)
        c.text((cx, cy + ch * 0.19), stone, sub, ink, "mm", italic=True)


def draw_garment(c, key, x, y, w, h):
    """One garment alone, on its own form or as its working drawing, under
    its WEB name."""
    cell_panel(c, x, y, w, h, GM.GARMENT[key].name.upper())
    cx = x + w / 2
    if key in ("breeches", "coat", "robe"):
        F_ = G.Form(cx, y + h - 22, 300)
        ghost(c, F_)
        wear(c, F_, key, hidden=False)
    elif key == "ephod":
        # the ephod on its form, and its two onyx stones at reading size
        F_ = G.Form(x + 78, y + h - 22, 300)
        ghost(c, F_)
        wear(c, F_, "ephod")
        for k, (sx, sy) in enumerate(G.strap_points(F_)):
            cy = y + 112 + k * 146
            c.line((sx, sy), (x + 214 - 62, cy), dim(SILVER, 0.7), 1.3,
                   dash="4,4")
            G.onyx_stone(c, x + 214, cy, 122, 124, dim(SILVER, 0.88), GOLD,
                         names=GM.SHOULDER_STONES[k], text_col=INK, size=13,
                         engraved=True)
    elif key == "breastplate":
        draw_breastplate(c, x, y, w)
    elif key == "sash":
        # the waist, drawn larger
        with c.group(tx=x, ty=y + 40, clip=(w, h - 44)):
            F_ = G.Form(w / 2, 470, 640)
            ghost(c, F_, head=False)
            wear(c, F_, "sash")
    elif key in ("turban", "plate"):
        if key == "plate":
            py = y + 92
            c.line((cx - 128, py - 4), (cx + 128, py - 4), LACE, 5)
            c.rect(cx - 112, py - 30, 224, 56, fill=GOLD, stroke=HL,
                   width=1.8, rx=9)
            c.text((cx, py), "HOLY TO YAHWEH", 18, INK, "mm", bold=True)
        top = y + (150 if key == "plate" else 40)
        hh = 1000 if key == "turban" else 760
        with c.group(tx=x, ty=top, clip=(w, y + h - 6 - top)):
            r = hh * 0.058
            F_ = G.Form(w / 2, hh + 1.35 * r + 26, hh)
            ghost(c, F_)
            G.head(c, F_, dim(SAND, 0.95), FLESH, dim(SAND_DIM, 0.95),
                   cloth=False)
            if key == "plate":
                # the turban it is tied to, quieter than the plate
                G.turban(c, F_, mix(LINEN, 0.45), dim(SAND_DIM, 0.8))
            wear(c, F_, key)
    elif key == "sons":
        # coat, sash and headband (28:40), over the breeches (28:42); the
        # coat of woven work, not checker work, which is Aaron's (28:39)
        F_ = G.Form(cx, y + h - 22, 300)
        G.head(c, F_, dim(SAND, 0.95), FLESH, dim(SAND_DIM, 0.95),
               cloth=False)
        ghost(c, F_, head=False)
        G.breeches(c, F_, dim(LINEN, 0.85), hidden=True)
        G.coat(c, F_, dim(LINEN, 0.55), RULE, checker=False)
        G.sash(c, F_, mix(LINEN, 0.75), RULE)
        r = F_.head_r
        c.rect(F_.x - r * 1.08, F_.head_cy - r * 0.95, r * 2.16, r * 0.62,
               fill=mix(LINEN, 0.80), stroke=RULE, width=1.3, rx=r * 0.2)
    elif key == "linen":
        # the holy linen coat, breeches, sash and turban (Lev 16:4)
        F_ = G.Form(cx, y + h - 22, 300)
        G.head(c, F_, dim(SAND, 0.95), FLESH, dim(SAND_DIM, 0.95),
               cloth=False)
        ghost(c, F_, head=False)
        G.breeches(c, F_, dim(LINEN, 0.85), hidden=True)
        G.coat(c, F_, dim(LINEN, 0.60), RULE, checker=False)
        G.sash(c, F_, mix(LINEN, 0.80), RULE)
        G.turban(c, F_, TURBAN, RULE)


def draw_garments(c):
    c.text((GAR_X + GAR_W / 2, GAR_Y + 24), "THE GARMENTS", 22, TEXT, "mm",
           bold=True)
    c.text((GAR_X + GAR_W / 2, GAR_Y + 50),
           "Exodus 28 and 39 · Leviticus 8 and 16", 15, TEXT_DIM, "mm",
           italic=True)
    draw_figure(c)
    for key, (x, y, w, h) in garment_cells().items():
        draw_garment(c, key, x, y, w, h)


# ---------------------------------------------------------------------------
# The offerings
# ---------------------------------------------------------------------------

def thing_parts(key):
    """A thing brought, as svg_figures draws it, and its ink."""
    beast, bird, made = TEXT, SILVER, WHITE_LINEN
    return {
        "bull": (F.ox(), beast), "herd": (F.ox(), beast),
        "male sheep": (F.sheep(ram=True), beast),
        "ram": (F.sheep(ram=True), beast),
        "lamb": (F.sheep(lamb=True), beast),
        "male goat": (F.goat(), beast), "goat": (F.goat(), beast),
        "female goat": (F.goat(female=True), beast),
        "turtledove": (F.dove(descending=False), bird),
        "pigeon": (F.dove(descending=False), bird),
        "fine flour": (F.basket(), made), "oil": (F.jar(), GOLD),
        "frankincense": (F.cup(), made), "salt": (F.cup(), made),
        "cakes": (F.bread(), made), "wafers": (F.bread(), made),
        "leavened bread": (F.bread(), made),
        "first fruits": (F.grass(), TEXT), "silver": (F.coins(), SILVER),
    }[key]


def draw_thing(c, key, cx, bottom, bw, bh):
    """`key` fitted into a bw x bh box standing on `bottom`, centred on cx."""
    parts, ink = thing_parts(key)
    x0, x1, y0, y1 = F.bbox((parts, 0))
    s = min(bw / (x1 - x0), bh / (y1 - y0))
    if key == "lamb":
        s *= 0.75
    F.draw(c, parts, cx - (x0 + x1) / 2 * s, bottom + y0 * s, s, ink, PANEL)


# The table's type: a row's entries at SHORT, the line under each (which
# kind, or who) at WHO in SUB, which is 5.5:1 on the panel.
SHORT, WHO, LABEL = 17.5, 14, 15
LINE, SUBLINE, GAP = 23, 19, 11
SUB = (165, 155, 122)
PAD = 16                                     # a cell's side padding
CELL_TW = OFF_CW - 2 * PAD                   # its text's width
THING_ROW = 116                              # a row of drawn things
RANK_ICON = 96                               # a sin offering rank's drawing


def entries(rs, sub=True):
    """The table's entries for Rows: [(main lines, sub lines)], one per
    different thing said; a row with no `short` is on its card only."""
    out, seen = [], set()
    for r in rs:
        if not r.short:
            continue
        main, s = r.short, (r.who if sub else "")
        if s in ("every one", "no one", main):
            s = ""
        if (main, s) in seen:
            continue
        seen.add((main, s))
        out.append((wrap(main, SHORT, CELL_TW),
                    wrap(s, WHO, CELL_TW, italic=True) if s else []))
    return out


def entries_h(es):
    return sum(GAP + LINE * len(m) + SUBLINE * len(s) for m, s in es)


def ranks(o):
    """The sin offering's BROUGHT: [(who lines, what lines, figure keys)],
    rows that bring the same thing merged."""
    groups = []
    for r in o.brought:
        for g in groups:
            if g[0] == (r.things, r.short):
                g[1].append(r.who)
                break
        else:
            groups.append([(r.things, r.short), [r.who]])
    width = CELL_TW - RANK_ICON - 10
    return [([ln for w in whos for ln in wrap(w, SHORT, width)],
             wrap(short, WHO, width, italic=True), things)
            for (things, short), whos in groups]


def rank_h(rk):
    mains, subs, _things = rk
    return max(60, LINE * len(mains) + SUBLINE * len(subs)) + GAP


def brought_h(o):
    if o.by is None:
        return 16 + sum(rank_h(rk) for rk in ranks(o)) + 8
    n = len(OF.THINGS[o.key])
    return 16 + LINE + 6 + -(-n // 3) * THING_ROW + 4


def offer_rows():
    """The table's rows: (label, sub-label, kind, {offering key: content},
    height)."""
    out = [("BROUGHT", "by whom", "brought",
            {o.key: o for o in OF.OFFERINGS},
            max(brought_h(o) for o in OF.OFFERINGS))]
    for lab, field, sub in (("ON THE ALTAR", "burns", True),
                            ("THE BLOOD", "blood", True),
                            ("WHO EATS", "eaten", True),
                            ("NOT EATEN", "not_eaten", False)):
        es = {o.key: entries(getattr(o, field), sub) for o in OF.OFFERINGS}
        out.append((lab, "", "entries", es,
                    max(entries_h(e) for e in es.values()) + 30))
    out.append(("WHEN", "", "when", {o.key: o for o in OF.OFFERINGS}, 84))
    return out


OFF_HEAD = 96
OFF_ROWS = offer_rows()
OFF_TABLE_H = OFF_HEAD + sum(r[4] for r in OFF_ROWS)
OFF_H = 80 + OFF_TABLE_H
H = max(DETAIL_Y + DETAIL_H + 60, OFF_Y + OFF_H + 60, GAR_Y + GAR_H + 60)


def offer_columns():
    """{offering key: (x, y, w, h)}, the table's columns."""
    ty = OFF_Y + 80
    return {o.key: (OFF_X + OFF_RH + k * OFF_CW, ty, OFF_CW, OFF_TABLE_H)
            for k, o in enumerate(OF.OFFERINGS)}


def offer_frame(key):
    """Where selecting an offering looks: its name and what is brought, at
    a size to read; the reader pans down for the rest."""
    x, y, w, _h = offer_columns()[key]
    return _rb([x, y, w, OFF_HEAD + OFF_ROWS[0][4]])


def draw_brought(c, o, x, y):
    """One offering's BROUGHT cell, from its left edge x and top y."""
    if o.by is None:
        # the sin offering: each rank, and what it brings
        yy = y + 16
        for rk in ranks(o):
            mains, subs, things = rk
            n = len(things)
            for i, key in enumerate(things):
                iw = RANK_ICON / n
                draw_thing(c, key, x + iw * (i + 0.5), yy + 54, iw - 6, 50)
            tx = x + RANK_ICON + 10
            ty = yy
            for ln in mains:
                c.text((tx, ty + 12), ln, SHORT, TEXT, "lm")
                ty += LINE
            for ln in subs:
                c.text((tx, ty + 9), ln, WHO, SUB, "lm", italic=True)
                ty += SUBLINE
            yy += rank_h(rk)
        return
    c.text((x, y + 16 + 12), o.by_short, SHORT, TEXT, "lm")
    things = OF.THINGS[o.key]
    per = min(3, len(things))
    slot = CELL_TW / per
    for i, t in enumerate(things):
        r, k = divmod(i, per)
        tcx = x + k * slot + slot / 2
        base = y + 16 + LINE + 6 + r * THING_ROW + 64
        draw_thing(c, t.key, tcx, base, min(88, slot - 12), 54)
        c.text((tcx, base + 22), t.short or t.key, LABEL, TEXT, "mm")


def draw_offerings(c):
    c.text((OFF_X + TABLE_W / 2, OFF_Y + 24), "THE OFFERINGS", 22, TEXT, "mm",
           bold=True)
    c.text((OFF_X + TABLE_W / 2, OFF_Y + 50), "Leviticus 1–7", 15, TEXT_DIM,
           "mm", italic=True)
    ty = OFF_Y + 80
    c.rect(OFF_X, ty, TABLE_W, OFF_TABLE_H, fill=PANEL, stroke=SAND_DIM,
           width=2, rx=10)
    rule = mix(SAND, 0.45)
    cols = offer_columns()
    for k, o in enumerate(OF.OFFERINGS):
        x = cols[o.key][0]
        if k:
            c.line((x, ty + 10), (x, ty + OFF_TABLE_H - 10), rule, 1.2)
        names = wrap(o.name, 20, OFF_CW - 24, bold=True)
        y = ty + 36 - 12 * (len(names) - 1)
        for i, ln in enumerate(names):
            c.text((x + OFF_CW / 2, y + i * 24), ln, 20, TEXT, "mm",
                   bold=True)
        c.text((x + OFF_CW / 2, ty + OFF_HEAD - 20), OFFER_SUB[o.key], 15,
               SUB, "mm", italic=True)
    y = ty + OFF_HEAD
    for lab, sub, kind, content, rh in OFF_ROWS:
        c.line((OFF_X + 10, y), (OFF_X + TABLE_W - 10, y), rule, 1.2)
        c.text((OFF_X + 18, y + 28), lab, LABEL, SUB, "lm", bold=True)
        if sub:
            c.text((OFF_X + 18, y + 50), sub, WHO, SUB, "lm", italic=True)
        for o in OF.OFFERINGS:
            x = cols[o.key][0] + PAD
            got = content[o.key]
            if kind == "brought":
                draw_brought(c, got, x, y)
            elif kind == "entries":
                if not got:
                    c.text((x, y + 28), "—", SHORT, SUB, "lm")
                yy = y + 16
                for main, subl in got:
                    for ln in main:
                        c.text((x, yy + 12), ln, SHORT, TEXT, "lm")
                        yy += LINE
                    for ln in subl:
                        c.text((x, yy + 9), ln, WHO, SUB, "lm", italic=True)
                        yy += SUBLINE
                    yy += GAP
            else:
                yy = y + 28
                for ln in wrap(got.when_short, SHORT, CELL_TW, bold=True):
                    c.text((x, yy), ln, SHORT, TEXT, "lm", bold=True)
                    yy += LINE
                if got.when.flag != SN.STATED:
                    c.text((x, yy), got.when.flag, WHO, SUB, "lm",
                           italic=True)
        y += rh


# ---------------------------------------------------------------------------
# The sheet
# ---------------------------------------------------------------------------

def build_svg():
    c = SvgCanvas(W, H, bg=BG)
    draw_masthead(c)
    draw_camp(c)
    draw_court(c)
    draw_tent(c)
    draw_furnishings(c)
    draw_dims(c)
    draw_details(c)
    draw_garments(c)
    draw_offerings(c)
    svg = c.tostring().replace(
        "<svg ", '<svg data-kind="architecture" data-title="The Tabernacle" ', 1)
    return svg


# ---------------------------------------------------------------------------
# The sidecar
# ---------------------------------------------------------------------------

def _box(x0, y0, x1, y1, pad=0):
    x, y, w, h = PLAN.box(x0, y0, x1, y1)
    return [round(x - pad, 1), round(y - pad, 1), round(w + 2 * pad, 1),
            round(h + 2 * pad, 1)]


def _around(pt, r):
    x, y = PLAN.pt(*pt)
    return [round(x - r, 1), round(y - r, 1), 2 * r, 2 * r]


def part_box(key):
    p = SN.PART[key].plan
    if key == "court":
        return _box(*COURT)
    if key in ("veil", "door", "gate"):
        x, y, w, h = _box(*p)
        return [round(x - 8, 1), y, 16, h]
    if len(p) == 2:
        return _around(p, 17 if key == "basin" else 16)
    return _box(*p, pad=4)


def _rb(b):
    return [round(v, 1) for v in b]


def sidecar():
    items, index = [], {}
    for part in SN.PARTS:
        it = card(part)
        it["id"] = part.key.replace("_", "-")
        if part.plan is not None:
            it["b"] = part_box(part.key)
        index[part.key] = len(items)
        items.append(it)
    # Hit areas beyond a part's own box: the court and the tent are tapped
    # on their walls and labels, since their insides hold other parts.
    cx, cy, cw, ch = items[index["court"]]["b"]
    items[index["court"]]["hb"] = [
        [cx - 8, cy - 8, cw + 16, 16], [cx - 8, cy + ch - 8, cw + 16, 16],
        [cx - 8, cy - 8, 16, ch + 16], [cx + cw / 2 - 80, cy - 46, 160, 26]]
    tx, ty, tw, th = items[index["tent"]]["b"]
    items[index["tent"]]["hb"] = [
        [tx - 6, ty - 6, tw + 12, 12], [tx - 6, ty + th - 6, tw + 12, 12],
        [tx - 6, ty - 6, 12, th + 12], [tx + 10, ty - 44, tw - 20, 26]]
    # The mercy seat lies on the ark: one box on the plan. The ark takes
    # the tap, and each card points to the other.
    items[index["mercy_seat"]]["b"] = items[index["ark"]]["b"]
    items[index["mercy_seat"]]["nohit"] = True
    items[index["ark"]]["see"] = [index["mercy_seat"]]
    items[index["mercy_seat"]]["see"] = [index["ark"]]
    # The coverings lie over the tent: their box is the band they show past
    # its walls, too thin to tap, so they are reached by search, the tent's
    # card and the Raising it tour.
    items[index["coverings"]]["b"] = _rb(coverings_box())
    items[index["coverings"]]["nohit"] = True
    items[index["tent"]]["see"] = [index["coverings"]]

    # the detail drawings: each is its part's card again, linked both ways
    for name, key, x, y in detail_boxes():
        b = [round(x, 1), round(y, 1), IW, IH]
        if key is None:
            it = {"n": MATERIALS["n"], "s": MATERIALS["s"],
                  "note": MATERIALS["note"],
                  "rg": [[g, rows(r)] for g, r in MATERIALS["verses"]],
                  "id": "materials", "a": ["materials", "offering"]}
        else:
            it = copy.deepcopy(items[index[key]])
            it.pop("hb", None)
            it.pop("nohit", None)
            it.pop("see", None)
            it.pop("dt", None)                # only the part lists its drawings
            it["id"] = f"drawing-{name}"
            it["of"] = index[key]
            it["dl"] = DETAIL_LABEL[name]
            it["nos"] = True                  # search and #at find the part
            src = items[index[key]]
            src.setdefault("dt", []).append(len(items))
        it["b"] = b
        it["ly"] = "details"
        items.append(it)
    # the camp
    for side, ((lx, ly, lw, lh), (tx, ty, tw, th)) in camp_boxes().items():
        who, ref = SN.LEVITE_CAMP[side]
        clan = who if who in SN.CARRIED else None
        lev = {"id": f"levites-{side}", "n": who,
               "s": f"camped on the {side} of the tabernacle", "ly": "camp",
               "b": [round(lx, 1), round(ly, 1), lw, lh],
               "rg": [["Their camp", rows(ref, "Numbers")]], "a": ["Levites"]}
        if clan:
            what, cref = SN.CARRIED[clan]
            lev["tx"] = [["They carried", what]]
            lev["rg"].append(["What they carried", rows(cref, "Numbers")])
        else:
            lev["note"] = ("They kept the charge of the sanctuary, toward the "
                           "sunrise, before the Tent of Meeting.")
        items.append(lev)
        standard, tribes, tref = SN.TRIBE_CAMP[side]
        word, _std, _t, total, order = CAMPS[SIDE_KEY[side]]
        items.append({
            "id": f"camp-{side}", "n": f"The camp of {standard}",
            "s": f"on the {side}, {['first', 'second', 'third', 'fourth'][order - 1]} to set out",
            "ly": "camp", "b": [round(tx, 1), round(ty, 1), tw, th],
            "dims": [[t, f"{COUNT[t]:,}", SN.STATED, []] for t in tribes]
                    + [["in all", f"{total:,}", SN.STATED, []]],
            "rg": [["Their camp", rows(tref, "Numbers")]],
            "a": list(tribes)})

    # The garments: each laid-out drawing is the garment's part; the piece
    # on the dressed figure is its card again (`nos`), framing the whole
    # figure, and the two point to each other.
    gindex, findex = {}, {}
    for key, (x, y, w, h) in garment_cells().items():
        it = garment_card(GM.GARMENT[key])
        it["id"] = {"sons": "sons-garments",
                    "linen": "linen-garments"}.get(key, key)
        it["b"] = _rb([x, y, w, h])
        gindex[key] = len(items)
        items.append(it)
    for key, (b, taps) in piece_boxes(FIG).items():
        it = copy.deepcopy(items[gindex[key]])
        it["id"] = f"aaron-{key}"
        it["s"] = "on the high priest, dressed"
        it["b"] = b
        it["fr"] = figure_frame()
        it["nos"] = True
        if key in ("breeches", "sash"):
            it["nohit"] = True                # under the coat, the robe
        elif taps:
            it["t"] = taps
        it["see"] = [gindex[key]]
        items[gindex[key]].setdefault("see", []).append(len(items))
        findex[key] = len(items)
        items.append(it)

    # The offerings: a column each, and the altar they are offered on.
    oindex = {}
    for o in OF.OFFERINGS:
        it = offering_card(o)
        it["id"] = {"peace": "peace-offerings"}.get(o.key, f"{o.key}-offering")
        it["b"] = _rb(offer_columns()[o.key])
        it["fr"] = offer_frame(o.key)
        it["see"] = [index["altar"]]
        oindex[o.key] = len(items)
        items.append(it)
    items[index["altar"]]["see"] = [oindex[o.key] for o in OF.OFFERINGS]

    def commanded(key):
        """The verses that command a part, less Exodus 40:2-15's command
        to set it up, which the Raising it tour has."""
        return [r for r in rows(dict(SN.PART[key].verses)["Commanded"])
                if r[1] != 40]
    tours = [
        {"id": "gate", "label": "Gate to ark", "build": False,
         "stops": [{"i": index[k], "r": commanded(k)}
                   for k in GATE_TO_ARK]},
        {"id": "raise", "label": "Raising it", "build": True,
         "stops": [{"i": index[k], "r": rows(ref), "rise": n}
                   for n, (ref, k) in enumerate(RAISE)]},
        {"id": "dress", "label": "Dressing Aaron", "build": True,
         "stops": [{"i": findex[keys[0]], "r": rows(ref), "rise": n}
                   for n, (ref, keys) in enumerate(GM.DRESSING)]},
    ]

    # every verse a card names, for #at
    for it in items:
        flat = [r for _g, rs in it.get("rg", []) for r in rs]
        flat += [r for d in it.get("dims", []) for r in d[3]]
        flat += it.get("pl", [None, None, []])[2]
        it["r"] = sorted({tuple(r) for r in flat})
        it["r"] = [list(r) for r in it["r"]]
    used = sorted({r[0] for it in items for r in it["r"]}
                  | {r[0] for t in tours for s in t["stops"] for r in s["r"]})
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
    for t in tours:
        for s in t["stops"]:
            re_book(s["r"])
    ids = [it["id"] for it in items]
    assert len(set(ids)) == len(ids), "ids collide"
    views = [
        {"id": "plan", "label": "Plan", "fr": plan_frame()},
        {"id": "detail", "label": "In detail", "fr": detail_frame(),
         "ly": "details"},
        {"id": "garments", "label": "Garments",
         "fr": _rb([GAR_X - 20, GAR_Y - 10, GAR_W + 40, GAR_H + 20])},
        {"id": "offerings", "label": "Offerings",
         "fr": _rb([OFF_X - 20, OFF_Y - 10, TABLE_W + 40, OFF_H + 20])},
    ]
    return {"version": 1, "card": "parts", "noun": ["part", "parts"],
            "books": [BOOK_NAMES[b] for b in used],
            "layers": [{"id": "dims", "label": "Measurements", "on": True},
                       {"id": "camp", "label": "The camp", "on": False},
                       {"id": "details", "label": "Drawings", "on": True}],
            "views": views, "tours": tours,
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
            STEM, _fmt(W), _fmt(H), "The Tabernacle", data=True,
            placeholder="find a part — ark, ephod, sin offering…"))
    print(path)
    print(f"  {_fmt(W)} x {_fmt(H)} px · {os.path.getsize(path) / 1024:.0f} KB")
    print(dp)
    print(f"  {len(data['items'])} cards · "
          f"{sum(len(it['r']) for it in data['items'])} verse refs · "
          f"{os.path.getsize(dp) / 1024:.0f} KB")
    print(vp)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
