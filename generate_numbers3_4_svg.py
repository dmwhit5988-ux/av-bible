"""Render Numbers 3-4 (the Levites: clans, duties and burdens) as per-verse SVGs.

One chart, replayed for all 100 verses of the two chapters. The Levites are the
tribe Numbers 1 left out of the muster roll, and these two chapters explain
what they were left out *for* — so the graphic is an organisation chart of the
one tribe that carries the tabernacle:

* **Across the top — the priesthood.** Aaron's four sons, two struck out at
  3:4. The two who remain are the two names the rest of the chart reports to:
  Eleazar over the Kohathites, Ithamar over Gershon and Merari.
* **Three columns — the three clans.** Gershon, Kohath and Merari, each with
  its families, its prince, the side it camps on, and — the body of the column
  — a drawing of the part of the tabernacle it is responsible for, its pieces
  labelled one or two words each. Both chapters' lists run over the same
  drawing: chapter 3's standing duty and chapter 4's burden on the march name
  the same objects, so the parts simply light up as they are named. Below, the
  two counts: every male a month old and upward, and the smaller number of
  serving age, thirty to fifty.
* **Right — the ring and the ledger.** The Levite positions around the tent
  (east at the top, as in the Numbers 1-2 camp plan), and the redemption
  arithmetic of 3:40-51: 22,273 firstborn, 22,000 Levites, 273 over, five
  shekels each, 1,365 shekels paid.

The Kohathite panel does the most work in chapter 4: its six holy objects are
draped one at a time, in the blue, scarlet and purple the text names, as verses
5-14 cover them.

Text discipline: the verse is read aloud alongside the graphic, so nothing here
restates it — no caption line, no duty/burden prose, no notes. Where the older
draft wrote out "the tabernacle's boards, its bars, its pillars, its sockets",
the drawing now shows boards, bars, pillars and sockets with those words as
labels, and lights them on the verse that names them.

Naming note: the usual `generate_<book><chapters>_svg.py` contraction is not
available here — `generate_numbers34_svg.py` is already Numbers *34*, the
borders map — so these two families spell their chapter range out.

Run inside the project venv:
    .venv\\Scripts\\python.exe generate_numbers3_4_svg.py
"""

import os

from svg_surface import SvgCanvas
from generate_tabernacle import (W, H, BG, PANEL, SAND, SAND_DIM, SILVER, TEXT,
                                 TEXT_DIM, GOLD, HL, BRONZE, BROWN, GRAY,
                                 WHITE_LINEN, GATE_COLORS, out_path)

BLUE, PURPLE, SCARLET, LINEN = GATE_COLORS


def dim(color, a):
    """`color` with an 0-255 alpha, in the (r, g, b, a) form SvgCanvas takes."""
    return color + (int(a),)


def g(alpha):
    return HL + (int(255 * alpha),)


def num(n):
    return f"{n:,}"


CH_LEN = {3: 51, 4: 49}

# ---------------------------------------------------------------------------
# Aaron's sons (3:1-4), and what chapters 3-4 put each surviving one over.
# (name, died, the two or three words under it)
# ---------------------------------------------------------------------------

SONS = [
    ("Nadab",   True,  "strange fire"),
    ("Abihu",   True,  "strange fire"),
    ("Eleazar", False, "over Kohath"),
    ("Ithamar", False, "over Gershon & Merari"),
]

# ---------------------------------------------------------------------------
# The three clans. Chapter 3 fills in who they are; chapter 4 adds the serving
# count. Both chapters' duty lists name the same objects, which the glyph draws
# and labels — GLYPH_A / GLYPH_B below are the two groups the text itself uses
# (the tent's own fabric vs. the court's, the frame vs. its pins and cords).
# ---------------------------------------------------------------------------

CLANS = [
    {
        "key": "G", "name": "GERSHON", "side": "WEST",
        "families": "Libnites · Shimeites",
        "prince": "Eliasaph son of Lael",
        "over": "under Ithamar",
        "month": 7500, "serve": 2630,
        "v_fam": 18, "v_count1": 22, "v_camp": 23, "v_prince": 24,
        "v_count2": 40,
    },
    {
        "key": "K", "name": "KOHATH", "side": "SOUTH",
        "families": "Amramites · Izharites · Hebronites · Uzzielites",
        "prince": "Elizaphan son of Uzziel",
        "over": "under Eleazar",
        "month": 8600, "serve": 2750,
        "v_fam": 19, "v_count1": 28, "v_camp": 29, "v_prince": 30,
        "v_count2": 36,
    },
    {
        "key": "M", "name": "MERARI", "side": "NORTH",
        "families": "Mahlites · Mushites",
        "prince": "Zuriel son of Abihail",
        "over": "under Ithamar",
        "month": 6200, "serve": 3200,
        "v_fam": 20, "v_count1": 34, "v_camp": 35, "v_prince": 35,
        "v_count2": 44,
    },
]

BY_KEY = {c["key"]: c for c in CLANS}

MONTH_TOTAL = 22000        # 3:39, as the text states it
SERVE_TOTAL = 8580         # 4:48
MONTH_MAX = 8600           # Kohath — the scale for the first bar
SERVE_MAX = 3200           # Merari — the scale for the second

# Which clan each verse is about, and which part of its column.
CLAN_AT = {3: {}, 4: {}}
for _v in (18, 21, 22, 23, 24, 25, 26):
    CLAN_AT[3][_v] = "G"
for _v in (19, 27, 28, 29, 30, 31, 32):
    CLAN_AT[3][_v] = "K"
for _v in (20, 33, 34, 35, 36, 37):
    CLAN_AT[3][_v] = "M"
for _v in list(range(1, 21)) + [34, 35, 36, 37]:
    CLAN_AT[4][_v] = "K"
for _v in list(range(21, 29)) + [38, 39, 40, 41]:
    CLAN_AT[4][_v] = "G"
for _v in list(range(29, 34)) + [42, 43, 44, 45]:
    CLAN_AT[4][_v] = "M"

# The part of that clan's column the verse is about.
PART_AT = {3: {
    18: "fam", 19: "fam", 20: "fam", 21: "fam", 27: "fam", 33: "fam",
    22: "count1", 28: "count1", 34: "count1",
    23: "camp", 29: "camp",
    24: "prince", 30: "prince", 35: "prince",
    25: "glyphA", 36: "glyphA",
    26: "glyphB", 37: "glyphB",
    31: "glyphAll", 32: "over",
}, 4: {
    2: "count2", 3: "count2", 22: "count2", 23: "count2",
    29: "count2", 30: "count2",
    34: "count2", 35: "count2", 36: "count2", 37: "count2",
    38: "count2", 39: "count2", 40: "count2", 41: "count2",
    42: "count2", 43: "count2", 44: "count2", 45: "count2",
    4: "glyphAll", 15: "glyphAll", 19: "glyphAll", 20: "glyphAll",
    18: "glyphAll",
    5: "item", 6: "item", 7: "item", 8: "item", 9: "item", 10: "item",
    11: "item", 12: "item", 13: "item", 14: "item",
    24: "glyphA", 25: "glyphA", 31: "glyphA",
    26: "glyphB", 32: "glyphB",
    27: "over", 28: "over", 33: "over",
}}

# The six holy things Kohath carries, each draped on its own verses (4:5-14).
# The table takes blue at 7 and scarlet at 8, so it appears twice; the later
# entry wins.
HOLY = [
    ("ark",          5,  BLUE),
    ("table",        7,  BLUE),
    ("table",        8,  SCARLET),
    ("lamp stand",   9,  BLUE),
    ("gold altar",   11, BLUE),
    ("vessels",      12, BLUE),
    ("bronze altar", 13, PURPLE),
]
HOLY_ORDER = ["ark", "table", "lamp stand", "gold altar", "vessels",
              "bronze altar"]


def cloth_for(item, ch, v):
    """The cloth on a holy thing at this verse, or None while it is bare."""
    cloth = None
    if ch == 4:
        for label, at, col in HOLY:
            if label == item and v >= at:
                cloth = col
    return cloth


# The redemption arithmetic of 3:40-51. (label, value, verse stated, is result)
LEDGER = [
    ("firstborn of Israel", "22,273", 43, False),
    ("Levites in their place", "22,000", 39, False),
    ("in excess", "273", 46, False),
    ("shekels apiece", "× 5", 47, False),
    ("paid to Aaron", "1,365", 50, True),
]

# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

PRIEST_Y, PRIEST_H = 56, 44
COL_Y, COL_H = 118, 390
COL_W = 216
COL_X = [28, 254, 480]

PANEL_X, PANEL_W = 720, 276
LEDG_Y, LEDG_H = 332, 176
FOOT_Y = 532


def shown(clan, part, ch, v):
    """Whether a part of a clan column has been reached yet. Chapter 3's parts
    are all in force by the time chapter 4 opens."""
    ch3 = {"fam": "v_fam", "count1": "v_count1", "camp": "v_camp",
           "prince": "v_prince"}
    if part in ch3:
        return ch == 4 or v >= clan[ch3[part]]
    return ch == 4 and v >= clan["v_count2"]


def focused(clan, part, ch, v):
    return (CLAN_AT[ch].get(v) == clan["key"]
            and PART_AT[ch].get(v) == part)


def first_at(clan, part, ch, v):
    """True only on the verse this part *becomes* the focus, so a highlight
    that holds for several verses animates once instead of restarting."""
    return focused(clan, part, ch, v) and not focused(clan, part, ch, v - 1)


# ---------------------------------------------------------------------------
# The priesthood band
# ---------------------------------------------------------------------------

def draw_priests(c, ch, v):
    c.text((28, PRIEST_Y + 16), "AARON", 15, GOLD, "lm", bold=True)
    c.text((28, PRIEST_Y + 34), "and his sons", 10, TEXT_DIM, "lm",
           italic=True)
    for i, (name, dead, tag) in enumerate(SONS):
        x = 152 + i * 142
        live = (ch == 3 and v >= 2) or ch == 4
        settled = (ch == 3 and v >= 4) or ch == 4
        gone = dead and settled
        cur = ((ch == 3 and 2 <= v <= 4)
               or (ch == 3 and v == 32 and name == "Eleazar")
               or (ch == 4 and v == 16 and name == "Eleazar")
               or (ch == 4 and v in (28, 33) and name == "Ithamar"))
        c.rect(x, PRIEST_Y, 132, PRIEST_H,
               fill=BG if gone else (PANEL if live else BG),
               stroke=None if cur else (GRAY if gone else
                                        (SAND if live else SAND_DIM)),
               width=1.3, rx=4)
        if cur:
            c.pulse_rect(x, PRIEST_Y, 132, PRIEST_H, g(0.9), width=2,
                         first=(v in (2, 32, 16, 28)), rx=4)
        c.text((x + 12, PRIEST_Y + 17), name, 13.5,
               GRAY if gone else (HL if cur else (TEXT if live else TEXT_DIM)),
               "lm", bold=True)
        if gone:
            c.line((x + 12, PRIEST_Y + 17),
                   (x + 12 + 7.6 * len(name), PRIEST_Y + 17), GRAY, 1.4)
        if live:
            c.text((x + 12, PRIEST_Y + 33), tag, 9,
                   GRAY if gone else (GOLD if cur else TEXT_DIM), "lm",
                   italic=True)


# ---------------------------------------------------------------------------
# The clan glyphs — what each clan carries, drawn and labelled
# ---------------------------------------------------------------------------

def _label(c, x, y, s, lit, anchor="mm", on_light=False):
    """A one- or two-word tag on a drawn part. `on_light` flips the ink dark,
    for labels sitting on the pale linen bands."""
    if on_light:
        ink = (24, 22, 18) if lit else (58, 54, 46)
    else:
        ink = HL if lit else TEXT_DIM
    c.text((x, y), s, 9.5, ink, anchor, italic=True, bold=lit)


def _g_gershon(c, x, y, w, h, ch, v, hot_a, hot_b, hot_all):
    """The fabric of the tabernacle: the tent's own curtains and coverings
    (3:25, 4:25), then the court's hangings and cords (3:26, 4:26)."""
    tent_lit = hot_a or hot_all
    court_lit = hot_b or hot_all
    bands = [(LINEN, "curtains", tent_lit), (SCARLET, "covering", tent_lit),
             (PURPLE, "door screen", tent_lit),
             (LINEN, "court hangings", court_lit)]
    bh = 34
    for i, (col, label, lit) in enumerate(bands):
        by = y + i * (bh + 6)
        pts = [(x + w * j / 10, by + (2.5 if j % 2 else -2.5))
               for j in range(11)]
        c.polygon(pts + [(x + w, by + bh), (x, by + bh)],
                  fill=dim(col, 215 if lit else 150),
                  stroke=dim(col, 245 if lit else 180), width=1.1)
        _label(c, x + w - 8, by + bh / 2, label, lit, "rm",
               on_light=(col is LINEN))
    gy = y + h - 22
    c.line((x, gy), (x + w, gy), dim(BROWN, 220), 2)
    for cx in (x + w * 0.2, x + w * 0.5, x + w * 0.8):
        c.line((cx, gy - 22), (cx + 14, gy), dim(SAND, 235 if court_lit else
                                                 170), 1.3)
        c.polygon([(cx + 14, gy), (cx + 10, gy - 6), (cx + 18, gy - 6)],
                  fill=SAND if court_lit else dim(SAND, 170))
    _label(c, x + w / 2, gy + 13, "cords & pins", court_lit)


def _holy_icon(c, item, cx, base, col):
    """A drawing of one piece of the sanctuary furniture, sitting on `base`."""
    if item == "ark":
        c.rect(cx - 16, base - 20, 32, 17, fill=None, stroke=col, width=1.5)
        c.line((cx - 19, base - 20), (cx + 19, base - 20), col, 2)
        c.line((cx - 21, base - 8), (cx + 21, base - 8), col, 1.3)  # the poles
    elif item == "table":
        c.line((cx - 16, base - 17), (cx + 16, base - 17), col, 2)
        for dx in (-13, 13):
            c.line((cx + dx, base - 17), (cx + dx, base), col, 1.4)
        for dx in (-8, 0, 8):
            c.circle(cx + dx, base - 21, 3, fill=None, stroke=col, width=1.1)
    elif item == "lamp stand":
        c.line((cx, base), (cx, base - 21), col, 1.8)
        for s in (-1, 1):
            for r in (7, 12):
                c.line((cx, base - 10), (cx + s * r, base - 21), col, 1.2)
                c.circle(cx + s * r, base - 23, 2.1, fill=col)
        c.circle(cx, base - 23, 2.1, fill=col)
    elif item == "gold altar":
        c.rect(cx - 10, base - 18, 20, 18, fill=None, stroke=col, width=1.5)
        for dx in (-10, 10):
            c.line((cx + dx, base - 18), (cx + dx, base - 23), col, 1.5)
    elif item == "vessels":
        c.ellipse(cx - 9, base - 7, 8, 5, fill=None, stroke=col, width=1.3)
        c.ellipse(cx + 9, base - 11, 6.5, 4.2, fill=None, stroke=col,
                  width=1.3)
        c.line((cx + 1, base - 20), (cx + 6, base - 15), col, 1.3)
    else:                                                    # bronze altar
        c.rect(cx - 16, base - 17, 32, 17, fill=None, stroke=col, width=1.5)
        for dx in (-16, 16):
            c.line((cx + dx, base - 17), (cx + dx, base - 22), col, 1.5)
        c.line((cx - 16, base - 9), (cx + 16, base - 9), dim(col, 170), 1.1)


def _g_kohath(c, x, y, w, h, ch, v, hot_a, hot_b, hot_all):
    """The most holy things — bare in chapter 3, and draped one at a time in
    chapter 4 as Aaron and his sons cover them for the march (4:5-14)."""
    cw, chh = w / 3, h / 2
    for i, item in enumerate(HOLY_ORDER):
        cx = x + (i % 3) * cw + cw / 2
        cy = y + (i // 3) * chh
        cloth = cloth_for(item, ch, v)
        just = ch == 4 and any(lab == item and at == v for lab, at, _ in HOLY)
        lit = just or hot_all
        base = cy + chh - 40
        # the object is always drawn in gold; the cloth goes over it and is
        # translucent, so a covered thing still reads as the thing it is
        _holy_icon(c, item, cx, base, GOLD if lit or cloth else
                   dim(GOLD, 175))
        if cloth:
            c.rect(cx - cw / 2 + 6, base - 32, cw - 12, 38,
                   fill=dim(cloth, 190), stroke=dim(cloth, 245), width=1.2,
                   rx=3)
            if just:
                c.pulse_rect(cx - cw / 2 + 6, base - 32, cw - 12, 38,
                             g(0.95), width=1.9, first=True, rx=3)
        _label(c, cx, cy + chh - 14, item, lit)


def _g_merari(c, x, y, w, h, ch, v, hot_a, hot_b, hot_all):
    """The frame: boards standing in their sockets with the bars that hold
    them (3:36, 4:31), then the court's pillars, pins and cords (3:37, 4:32)."""
    frame_lit = hot_a or hot_all
    court_lit = hot_b or hot_all
    fc = GOLD if frame_lit else dim(GOLD, 165)

    bw, bg = 12, 10                                  # boards and bars
    n = 7
    bx = x + (w - (n * bw + (n - 1) * bg)) / 2
    for i in range(n):
        px = bx + i * (bw + bg)
        c.rect(px, y + 8, bw, 54, fill=dim(BROWN, 210 if frame_lit else 150),
               stroke=fc, width=1)
        c.rect(px - 1, y + 62, bw + 2, 7,
               fill=dim(SILVER, 210 if frame_lit else 150))
    for dy in (24, 44):
        c.line((bx - 4, y + dy), (bx + n * (bw + bg) - bg + 4, y + dy), fc,
               1.8)
    _label(c, x + w / 2, y + 82, "boards · bars · sockets", frame_lit)

    pc = SILVER if court_lit else dim(SILVER, 165)   # the court's pillars
    for i in range(4):
        px = x + w * (0.18 + i * 0.215)
        c.line((px, y + 100), (px, y + 142), pc, 2.2)
        c.circle(px, y + 98, 3, fill=None, stroke=pc, width=1.2)
        c.rect(px - 6, y + 142, 12, 7,
               fill=dim(BRONZE, 215 if court_lit else 150))
    _label(c, x + w / 2, y + 161, "pillars · sockets", court_lit)

    gy = y + h - 14                                  # the pins and the cords
    c.line((x + 10, gy), (x + w - 10, gy), dim(BROWN, 200), 1.6)
    for i in range(3):
        px = x + w * (0.24 + i * 0.26)
        c.line((px - 16, gy - 22), (px, gy), pc, 1.3)
        c.polygon([(px, gy), (px - 4, gy - 7), (px + 4, gy - 7)],
                  fill=SILVER if court_lit else dim(SILVER, 165))
    _label(c, x + w / 2, gy + 11, "pins · cords", court_lit)


GLYPHS = {"G": _g_gershon, "K": _g_kohath, "M": _g_merari}

# The vertical slice of each glyph a focus group occupies, relative to the top
# of the glyph box — so when a group is first named, that part of the drawing
# brightens once rather than merely changing colour.
GLYPH_ZONES = {
    "G": {"glyphA": (0, 114), "glyphB": (118, 210), "glyphAll": (0, 210)},
    "K": {"glyphAll": (0, 210)},
    "M": {"glyphA": (0, 92), "glyphB": (94, 210), "glyphAll": (0, 210)},
}


# ---------------------------------------------------------------------------
# One clan column
# ---------------------------------------------------------------------------

def draw_bar(c, x, y, w, label, value, scale_max, live, cur, first):
    c.text((x, y), label, 9.5, TEXT_DIM if live else SAND_DIM, "lm",
           italic=True)
    c.text((x + w, y), num(value) if live else "—", 14,
           GOLD if cur else (TEXT if live else SAND_DIM), "rm", bold=live)
    c.rect(x, y + 10, w, 13, fill=BG, stroke=SAND_DIM, width=1, rx=2)
    if live:
        c.grow_rect(x, y + 10, w * value / scale_max, 13,
                    fill=dim(GOLD if cur else SAND, 235), rx=2,
                    w_from=0 if first else w * value / scale_max)


def draw_clan(c, i, clan, ch, v):
    x, y, w, h = COL_X[i], COL_Y, COL_W, COL_H
    key = clan["key"]
    active = CLAN_AT[ch].get(v) == key
    inner = w - 20
    ix = x + 10

    c.rect(x, y, w, h, fill=PANEL, stroke=None if active else SAND_DIM,
           width=1.3, rx=5)
    if active:
        c.pulse_rect(x, y, w, h, g(0.85), width=2,
                     first=CLAN_AT[ch].get(v - 1) != key, rx=5)

    named = (ch == 3 and v >= 17) or ch == 4
    c.rect(x, y, w, 34, fill=dim(SILVER, 40), stroke=None, rx=5)
    c.text((ix, y + 18), clan["name"], 18,
           HL if active else (TEXT if named else TEXT_DIM), "lm", bold=True)
    camp_on = shown(clan, "camp", ch, v)
    if focused(clan, "camp", ch, v):
        c.pulse_rect(x + w - 62, y + 5, 56, 24, g(0.9), width=1.6,
                     first=first_at(clan, "camp", ch, v), rx=3)
    c.text((x + w - 10, y + 18), clan["side"] if camp_on else "—", 11,
           GOLD if focused(clan, "camp", ch, v) else
           (TEXT_DIM if camp_on else SAND_DIM), "rm", bold=camp_on)

    fam_on = shown(clan, "fam", ch, v)
    if focused(clan, "fam", ch, v):
        c.pulse_rect(ix - 5, y + 40, inner + 10, 17, g(0.9), width=1.6,
                     first=first_at(clan, "fam", ch, v), rx=3)
    c.text((ix, y + 48), clan["families"] if fam_on else "—", 9,
           HL if focused(clan, "fam", ch, v) else
           (TEXT_DIM if fam_on else SAND_DIM), "lm", italic=True)

    pr_on = shown(clan, "prince", ch, v)
    if focused(clan, "prince", ch, v):
        c.pulse_rect(ix - 5, y + 54, inner + 10, 18, g(0.9), width=1.6,
                     first=first_at(clan, "prince", ch, v), rx=3)
    c.text((ix, y + 63), clan["prince"] if pr_on else "prince —", 10,
           GOLD if focused(clan, "prince", ch, v) else
           (TEXT if pr_on else SAND_DIM), "lm")
    over_on = (ch == 3 and v >= 32 and key == "K") or ch == 4
    c.text((x + w - 10, y + 63), clan["over"] if over_on else "", 9,
           GOLD if focused(clan, "over", ch, v) else
           (SILVER if over_on else SAND_DIM), "rm", italic=True)

    # the body of the column: what this clan carries, drawn and labelled
    GLYPHS[key](c, ix, y + 78, inner, 210, ch, v,
                focused(clan, "glyphA", ch, v),
                focused(clan, "glyphB", ch, v),
                focused(clan, "glyphAll", ch, v))
    for part, (z0, z1) in GLYPH_ZONES[key].items():
        if first_at(clan, part, ch, v):
            c.pulse_rect(ix - 5, y + 78 + z0 - 3, inner + 10, z1 - z0 + 6,
                         g(0.85), width=1.6, first=True, rx=3)

    draw_bar(c, ix, y + 306, inner, "a month old and upward", clan["month"],
             MONTH_MAX, shown(clan, "count1", ch, v),
             focused(clan, "count1", ch, v),
             first_at(clan, "count1", ch, v))
    draw_bar(c, ix, y + 352, inner, "serving age, thirty to fifty",
             clan["serve"], SERVE_MAX, shown(clan, "count2", ch, v),
             focused(clan, "count2", ch, v),
             first_at(clan, "count2", ch, v))


# ---------------------------------------------------------------------------
# The right-hand panel: the Levite ring, and the redemption ledger
# ---------------------------------------------------------------------------

def draw_ring(c, ch, v):
    c.text((PANEL_X, 62), "LEVITE RING", 13, TEXT, "lm", bold=True)
    cx = PANEL_X + PANEL_W / 2

    # the tabernacle in the middle, its gate to the east — here, the top
    c.rect(cx - 19, 160, 38, 70, fill=BG, stroke=WHITE_LINEN, width=1.3)
    c.line((cx - 8, 160), (cx + 8, 160), GOLD, 2.4)
    c.rect(cx - 5, 196, 10, 26, fill=dim(BROWN, 200), stroke=GOLD, width=1.1)

    chips = [
        (cx - 110, 92, 220, 30, "EAST", "Moses & Aaron", 38),
        (cx - 110, 268, 220, 30, "WEST", "Gershon", BY_KEY["G"]["v_camp"]),
        (PANEL_X + 2, 180, 96, 30, "NORTH", "Merari", BY_KEY["M"]["v_camp"]),
        (PANEL_X + PANEL_W - 98, 180, 96, 30, "SOUTH", "Kohath",
         BY_KEY["K"]["v_camp"]),
    ]
    for x, y, w, h, word, who, at in chips:
        live = (ch == 3 and v >= at) or ch == 4
        cur = ch == 3 and v == at
        c.rect(x, y, w, h, fill=PANEL if live else BG,
               stroke=None if cur else (SAND if live else SAND_DIM),
               width=1.2, rx=3)
        if cur:
            c.pulse_rect(x, y, w, h, g(0.9), width=1.9, first=True, rx=3)
        if w < 150:                                  # the two narrow chips
            c.text((x + w / 2, y + 10), word, 9,
                   GOLD if live else SAND_DIM, "mm", bold=True)
            c.text((x + w / 2, y + 22), who, 12,
                   HL if cur else (TEXT if live else TEXT_DIM), "mm",
                   bold=cur)
        else:
            c.text((x + 10, y + h / 2), word, 9,
                   GOLD if live else SAND_DIM, "lm", bold=True)
            c.text((x + w - 10, y + h / 2), who, 12,
                   HL if cur else (TEXT if live else TEXT_DIM), "rm",
                   bold=cur)


def draw_ledger(c, ch, v):
    c.rect(PANEL_X, LEDG_Y, PANEL_W, LEDG_H, fill=PANEL, stroke=SAND_DIM,
           width=1.2, rx=5)
    opened = (ch == 3 and v >= 40) or ch == 4
    c.text((PANEL_X + 12, LEDG_Y + 18), "FIRSTBORN REDEEMED", 11,
           GOLD if opened else TEXT_DIM, "lm", bold=True)
    for i, (label, value, at, result) in enumerate(LEDGER):
        y = LEDG_Y + 46 + i * 26
        live = (ch == 3 and v >= at) or ch == 4
        cur = ch == 3 and v == at
        if result:
            c.line((PANEL_X + 12, y - 13), (PANEL_X + PANEL_W - 12, y - 13),
                   SAND_DIM if live else dim(SAND_DIM, 120), 1)
        c.text((PANEL_X + 12, y), label, 9.5,
               HL if cur else (TEXT_DIM if live else SAND_DIM), "lm",
               italic=True)
        c.text((PANEL_X + PANEL_W - 12, y), value if live else "—",
               14 if result else 12.5,
               GOLD if (cur or (result and live)) else
               (TEXT if live else SAND_DIM), "rm", bold=(result or cur))
        if cur:
            c.pulse_rect(PANEL_X + 8, y - 12, PANEL_W - 16, 23, g(0.85),
                         width=1.6, first=True, rx=3)


def draw_totals(c, ch, v):
    """The two totals as numbers, and the one note the graphic needs: the
    clans' own figures do not add to the total the text states."""
    m_on = (ch == 3 and v >= 39) or ch == 4
    s_on = ch == 4 and v >= 48
    c.text((28, FOOT_Y), num(MONTH_TOTAL), 17,
           GOLD if m_on else SAND_DIM, "lm", bold=True)
    c.text((104, FOOT_Y + 1), "a month old and upward", 10,
           TEXT_DIM if m_on else SAND_DIM, "lm", italic=True)
    c.text((266, FOOT_Y), num(SERVE_TOTAL), 17,
           GOLD if s_on else SAND_DIM, "lm", bold=True)
    c.text((326, FOOT_Y + 1), "of serving age", 10,
           TEXT_DIM if s_on else SAND_DIM, "lm", italic=True)
    c.text((996, FOOT_Y + 1), "the three clans sum to 22,300", 9.5, TEXT_DIM,
           "rm", italic=True)


# ---------------------------------------------------------------------------
# Assemble one verse
# ---------------------------------------------------------------------------

TITLES = {3: "Numbers 3 · The Levites", 4: "Numbers 4 · The Burden of the March"}


def render(ch, v):
    c = SvgCanvas(W, H, bg=BG)
    c.text((28, 24), TITLES[ch], 22, TEXT, "la", bold=True)
    draw_priests(c, ch, v)
    for i, clan in enumerate(CLANS):
        draw_clan(c, i, clan, ch, v)
    draw_ring(c, ch, v)
    draw_ledger(c, ch, v)
    draw_totals(c, ch, v)
    return c


def main():
    total = count = 0
    for ch in (3, 4):
        for v in range(1, CH_LEN[ch] + 1):
            c = render(ch, v)
            out = out_path("Numbers", ch, f"Numbers_{ch}_{v}.svg")
            c.save(out)
            total += os.path.getsize(out)
            count += 1
    print(f"Numbers 3-4: {count} SVG files, {total/1e3:.0f} KB")


if __name__ == "__main__":
    main()
