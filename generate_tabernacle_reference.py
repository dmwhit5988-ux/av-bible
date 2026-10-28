"""The Tabernacle reference page: the court, the tent and its furnishings,
drawn to scale from the one model (sanctuary.py), with a card for each part.

Writes web/visuals/reference/Tabernacle.svg, its sidecar Tabernacle.json
and the viewer page Tabernacle.html (reference_viewer.page). The web app's
Reference list opens it (web/js/app.js REFERENCES).

The sheet, east to the right as in the Exodus plan:

- **The plan**, 14 px a cubit: the court with its hangings, pillars and
  gate, the tent with the veil and the door screen, and the six
  furnishings. Each is a part on the sheet: a tap opens its card.
- **Measurements** (a layer, on): the court's, the gate's and the tent's
  figures.
- **The camp** (a layer, off): the Levites on the four sides and the twelve
  tribes beyond them by their standards (Numbers 2-3), not to scale.
- **In detail** (a layer, on): the Exodus 25-27 drawings of the ark, the
  table, the lamp stand, the altar, the veil, the screen, the boards, the
  curtains, the coverings and the materials (generate_tabernacle.INSETS),
  each drawn whole, without a verse's highlight.

A card gives the part's measurements, each marked stated, derived or not
given, where it stands, what it was made of, who carried it on the march,
and its verses grouped as commanded, made, set up and named elsewhere. The
part and its drawing link to each other.

    .venv\\Scripts\\python.exe generate_tabernacle_reference.py
"""

import copy
import json
import os

import sanctuary as SN
import verse_refs
from books import BOOK_NAMES
from generate_numbers1_2_svg import CAMPS, COUNT
from generate_tabernacle import (BG, BRONZE, GATE_COLORS, GOLD, HL, IH, INSETS,
                                 IW, IX, IY, PANEL, SAND, SAND_DIM, SILVER, TEXT,
                                 TEXT_DIM, WHITE_LINEN)
import reference_viewer
from config import VISUALS_DIR
from sanctuary import COURT, DOOR_X, GATE, TENT, VEIL_X, Plan
from svg_surface import SvgCanvas, SvgLayer, _fmt

OUT_DIR = os.path.join(VISUALS_DIR, "reference")
STEM = "Tabernacle"

S = 14                              # px per cubit on the sheet
MX, MY = 730, 400                   # room round the court for the camp
OX, OY = MX, MY + 40                # the court's north-west corner
PLAN = Plan(OX, OY, S)
CW, CH = (COURT[2] - COURT[0]) * S, (COURT[3] - COURT[1]) * S
DETAIL_COLS, DETAIL_GAP = 4, 28
DETAIL_Y = OY + CH + MY + 40
W = CW + 2 * MX
DETAIL_ROWS = 3
H = DETAIL_Y + 70 + DETAIL_ROWS * IH + (DETAIL_ROWS - 1) * DETAIL_GAP + 60


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

# The detail drawings, in sheet order, and the part each shows.
DETAILS = [("ark", "ark"), ("table", "table"), ("lamp", "lamp_stand"),
           ("altar", "altar"), ("veil", "veil"), ("screen", "door"),
           ("boards", "tent"), ("materials", None), ("linen", "coverings"),
           ("goat", "coverings"), ("coverings", "coverings")]
# What the card's link to each drawing says.
DETAIL_LABEL = {"ark": "the ark", "table": "the table",
                "lamp": "the lamp stand", "altar": "the altar",
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


def card(part):
    """The sidecar fields of a sanctuary.Part's card."""
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
    if part.carried:
        tx.append(["Carried by", part.carried])
    if tx:
        item["tx"] = tx
    if part.note:
        item["note"] = part.note
    return item


# ---------------------------------------------------------------------------
# The sheet
# ---------------------------------------------------------------------------

def label(c, xy, text, size=16, fill=TEXT, anchor="mm", **kw):
    c.text(xy, text, size, fill, anchor, **kw)


def draw_masthead(c):
    c.text((60, 74), "The Tabernacle", 44, TEXT, "lm", bold=True)
    c.text((60, 116), "the court, the tent and its furnishings, to scale",
           20, TEXT_DIM, "lm", italic=True)
    c.text((60, 148), "Exodus 25–40 · Numbers 2–4", 16,
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
    # the compass
    cx, cy = W - 110, 120
    c.line((cx, cy), (cx, cy - 40), SAND, 2)
    c.polygon([(cx - 6, cy - 32), (cx, cy - 44), (cx + 6, cy - 32)], fill=SAND)
    c.line((cx, cy), (cx + 40, cy), SAND, 2)
    c.polygon([(cx + 32, cy - 6), (cx + 44, cy), (cx + 32, cy + 6)], fill=SAND)
    c.text((cx, cy - 58), "N", 16, TEXT, "mm")
    c.text((cx + 58, cy), "E", 16, TEXT, "lm")


def draw_court(c):
    x, y, w, h = PLAN.box(*COURT)
    c.rect(x, y, w, h, fill=mix(SAND, 0.07))
    linen = WHITE_LINEN
    (x0, y0), (x1, y1) = PLAN.pt(COURT[0], COURT[1]), PLAN.pt(COURT[2], COURT[3])
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
        c.circle(px, py, 4.5, fill=mix(BRONZE, 0.8), stroke=SILVER, width=1.4)
    label(c, PLAN.pt(50, -2.2), "THE COURT", 18, TEXT, bold=True)
    label(c, PLAN.pt(103.2, 25), "GATE", 16, TEXT, "lm", bold=True)


def draw_tent(c):
    x, y, w, h = PLAN.box(*TENT)
    c.rect(x, y, w, h, fill=mix(SAND, 0.18))
    mx, my, mw, mh = PLAN.box(*SN.MOST_HOLY)
    c.rect(mx, my, mw, mh, fill=mix(GOLD, 0.14))
    c.rect(x, y, w, h, stroke=mix(GOLD, 0.8), width=4)
    # the veil and the door screen, in their colours
    for xx, cols, wd in ((VEIL_X, GATE_COLORS[:3], 2.4),
                         (DOOR_X, GATE_COLORS, 2.0)):
        for i, col in enumerate(cols):
            off = (i - (len(cols) - 1) / 2) * wd
            c.line((PLAN.pt(xx, 0)[0] + off, y + 2),
                   (PLAN.pt(xx, 0)[0] + off, y + h - 2), col, wd)
    label(c, PLAN.pt(25, TENT[1] - 2.2), "THE TABERNACLE", 16, TEXT, bold=True)
    label(c, PLAN.pt(15, TENT[3] - 1.4), "Most Holy Place", 13, TEXT_DIM,
          italic=True)
    label(c, PLAN.pt(30, TENT[3] + 1.6), "holy place", 13, TEXT_DIM,
          italic=True)
    label(c, PLAN.pt(VEIL_X, TENT[3] + 1.6), "veil", 13, TEXT_DIM,
          italic=True)
    label(c, PLAN.pt(DOOR_X + 1.0, TENT[3] + 1.6), "door", 13, TEXT_DIM, "lm",
          italic=True)


def draw_furnishings(c):
    gold, line = mix(GOLD, 0.75), mix(GOLD, 1.0)
    # the ark, the mercy seat on it, and the cherubim at its two ends
    x, y, w, h = PLAN.box(*SN.plan_box("ark"))
    c.rect(x, y, w, h, fill=gold, stroke=HL, width=1.6)
    c.rect(x + 3, y + 3, w - 6, h - 6, stroke=mix(GOLD, 0.45, BG), width=1)
    for ex in (x + 6, x + w - 6):
        c.polyline([(ex, y + 4), (x + w / 2, y + h / 2), (ex, y + h - 4)],
                   mix(GOLD, 0.4, BG), 1.3)
    label(c, (x + w / 2, y + h + 15), "ark", 14, TEXT)
    # the altar of incense, with its four horns
    x, y, w, h = PLAN.box(*SN.plan_box("incense_altar"))
    c.rect(x, y, w, h, fill=gold, stroke=line, width=1.2)
    for hx, hy in ((x, y), (x + w, y), (x, y + h), (x + w, y + h)):
        c.circle(hx, hy, 2.2, fill=HL)
    label(c, (x + w + 6, y + h / 2), "altar of incense", 13, TEXT, "lm")
    # the table, with the bread in two rows of six (Leviticus 24:6)
    x, y, w, h = PLAN.box(*SN.plan_box("table"))
    c.rect(x, y, w, h, fill=gold, stroke=line, width=1.2)
    for r in range(2):
        for k in range(6):
            c.rect(x + 2.5 + k * 4, y + 2.5 + r * 5, 3, 3.5,
                   fill=mix(SAND, 0.9, BG))
    label(c, (x + w + 7, y + h / 2), "table", 14, TEXT, "lm")
    # the lamp stand: seven lamps
    lx, ly = PLAN.pt(*SN.plan_point("lamp_stand"))
    c.line((lx - 15, ly), (lx + 15, ly), line, 2.4)
    for k in range(7):
        c.circle(lx - 15 + k * 5, ly, 2.2, fill=HL)
    label(c, (lx + 22, ly), "lamp stand", 14, TEXT, "lm")
    # the basin
    bx, by = PLAN.pt(*SN.plan_point("basin"))
    c.circle(bx, by, 15, fill=mix(BRONZE, 0.35), stroke=SILVER, width=2)
    c.circle(bx, by, 9, fill=mix((120, 150, 190), 0.45), stroke=None)
    label(c, (bx, by + 30), "basin", 15, TEXT)
    # the altar of burnt offering, its grating and four horns
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
    with c.group(data={"layer": "dims"}):
        y = PLAN.pt(0, COURT[3] + 4)[1]
        dim_arrow(c, (PLAN.pt(0, 0)[0], y), (PLAN.pt(100, 0)[0], y),
                  "100 cubits", "below")
        x = PLAN.pt(-4, 0)[0]
        dim_arrow(c, (x, PLAN.pt(0, 0)[1]), (x, PLAN.pt(0, 50)[1]),
                  "50 cubits", "left")
        x = PLAN.pt(COURT[2] + 9, 0)[0]
        dim_arrow(c, (x, PLAN.pt(0, GATE[0])[1]), (x, PLAN.pt(0, GATE[1])[1]),
                  "20", "right")
        y = PLAN.pt(0, TENT[1] - 5.4)[1]
        dim_arrow(c, (PLAN.pt(TENT[0], 0)[0], y), (PLAN.pt(TENT[2], 0)[0], y),
                  "30 cubits", "above")
        x = PLAN.pt(TENT[0] - 3, 0)[0]
        dim_arrow(c, (x, PLAN.pt(0, TENT[1])[1]), (x, PLAN.pt(0, TENT[3])[1]),
                  "10", "left")
        y = PLAN.pt(0, TENT[3] + 4.4)[1]
        dim_arrow(c, (PLAN.pt(TENT[0], 0)[0], y), (PLAN.pt(VEIL_X, 0)[0], y),
                  "10", "below")
        dim_arrow(c, (PLAN.pt(VEIL_X, 0)[0], y), (PLAN.pt(DOOR_X, 0)[0], y),
                  "20", "below")


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


def detail_boxes():
    out = []
    x0 = (W - (DETAIL_COLS * IW + (DETAIL_COLS - 1) * DETAIL_GAP)) / 2
    for i, (name, key) in enumerate(DETAILS):
        r, k = divmod(i, DETAIL_COLS)
        out.append((name, key, x0 + k * (IW + DETAIL_GAP),
                    DETAIL_Y + 70 + r * (IH + DETAIL_GAP)))
    return out


def draw_details(c):
    with c.group(data={"layer": "details"}):
        c.text((W / 2, DETAIL_Y + 24), "IN DETAIL", 22, TEXT, "mm", bold=True)
        c.text((W / 2, DETAIL_Y + 50), "the drawings of Exodus 25–27",
               15, TEXT_DIM, "mm", italic=True)
        for name, _key, x, y in detail_boxes():
            base, _over = SvgLayer(), SvgLayer()
            INSETS[name](base, _over, None, 1.0, 1.0)
            with c.group(tx=x - IX, ty=y - IY):
                c.raw(base.elements())


def build_svg():
    c = SvgCanvas(W, H, bg=BG)
    draw_masthead(c)
    draw_camp(c)
    draw_court(c)
    draw_tent(c)
    draw_furnishings(c)
    draw_dims(c)
    draw_details(c)
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
    # The coverings have no place of their own on the plan: they lie over
    # the tent, so their box is the tent's, reached by search and the tent's
    # card.
    items[index["coverings"]]["b"] = items[index["tent"]]["b"]
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
    # every verse a card names, for #at
    for it in items:
        flat = [r for _g, rs in it.get("rg", []) for r in rs]
        flat += [r for d in it.get("dims", []) for r in d[3]]
        flat += it.get("pl", [None, None, []])[2]
        it["r"] = sorted({tuple(r) for r in flat})
        it["r"] = [list(r) for r in it["r"]]
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
                       {"id": "camp", "label": "The camp", "on": False},
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
            STEM, _fmt(W), _fmt(H), "The Tabernacle", data=True,
            placeholder="find a part — ark, lamp stand, gate…"))
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
