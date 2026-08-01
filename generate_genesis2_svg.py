"""Render Genesis 2 (the garden eastward in Eden) as per-verse vector SVGs.

One schematic garden plan, replayed for all 25 verses. The chapter gives an
unusual amount of layout detail — a garden planted eastward in Eden, two named
trees in the middle of it, and one river that leaves Eden and parts into four
heads with three of them tied to named lands — so the graphic is a *plan*, not
a map: the four rivers fan out from the parting as labelled branches rather
than pretending to know where the Pishon and the Gihon ran.

The scene builds as the chapter does: the ground and its mist, the man formed
of dust, the garden planted round him, the two trees, the river and its four
heads (each tracing itself once and holding, per the house animation rules),
the command, the animals brought to be named, and the woman taken from his
side. Verses 1-3 — the seventh day, which belongs to the creation account
rather than the garden — play as a band over a garden not yet planted, closing
the day bar that Genesis 1 leaves open.

A side panel gives the chapter's twelve beats as a vertical strip with the
current one lit, so the stationary stretches still move verse by verse.

Run inside the project venv:
    .venv\\Scripts\\python.exe generate_genesis2_svg.py
"""

import os

from svg_surface import SvgCanvas
from generate_tabernacle import (W, H, BG, PANEL, SAND, SAND_DIM, TEXT,
                                 TEXT_DIM, GOLD, HL, BROWN, out_path)
from generate_tribal_maps import RIVER, RIVER_DIM, WATER_TXT


GREEN = (86, 122, 78)          # garden foliage
GREEN_DIM = (52, 70, 50)
EARTH = (58, 48, 38)           # the ground the man is formed from
RED = (170, 70, 60)            # the one prohibition


def g(alpha):
    return HL + (int(255 * alpha),)


def dim(color, a):
    """`color` with an 0-255 alpha, in the (r, g, b, a) form SvgCanvas takes
    (it turns the fourth element into a fill-/stroke-opacity)."""
    return color + (int(a),)


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

SCENE = (24, 86, 688, 556)     # x0, y0, x1, y1 of the garden plan window
PANEL_X = 712
BAND_Y, BAND_H = 96, 40        # the seventh-day band (verses 1-3)

# The garden: an oval in the west of the scene, so the four heads have the
# whole east side to fan into.
GX, GY, GRX, GRY = 250, 320, 140, 118

# The river: out of Eden (north-west), through the garden, to the parting.
SOURCE = [(38, 108), (74, 152), (100, 208), (110, 262), (114, 300)]
THROUGH = [(114, 300), (180, 312), (250, 320), (330, 328), (400, 336)]
PART = (400, 336)

# The four heads, in the order the text names them, each ending at a terminus
# chip stacked down the east side.
# (key, label, land, [points from PART], chip_y)
CHIP_X, CHIP_W, CHIP_H = 520, 160, 44
HEADS = [
    ("PISHON", "Pishon", "land of Havilah",
     [PART, (444, 282), (476, 206), (CHIP_X, 162)], 140),
    ("GIHON", "Gihon", "land of Cush",
     [PART, (452, 308), (486, 268), (CHIP_X, 250)], 228),
    ("HIDDEKEL", "Hiddekel", "before Assyria",
     [PART, (456, 342), (CHIP_X, 338)], 316),
    ("EUPHRATES", "Euphrates", "",
     [PART, (446, 382), (488, 416), (CHIP_X, 426)], 404),
]

# Which verse traces which head, and when each becomes "already flowing".
HEAD_VERSE = {"PISHON": 11, "GIHON": 13, "HIDDEKEL": 14, "EUPHRATES": 14}

# ---------------------------------------------------------------------------
# The chapter's beats (side panel).  (v_lo, v_hi, title, note)
# ---------------------------------------------------------------------------

BEATS = [
    (1, 3, "The seventh day", "finished, blessed, made holy"),
    (4, 6, "Before the rain", "no plant, no man — only a mist"),
    (7, 7, "The man formed", "dust of the ground, breath of life"),
    (8, 8, "A garden eastward", "planted in Eden; the man put there"),
    (9, 9, "Two trees in the middle", "life — and knowledge of good and evil"),
    (10, 14, "One river, four heads", "Pishon, Gihon, Hiddekel, Euphrates"),
    (15, 15, "To cultivate and keep", "the garden given as work"),
    (16, 17, "The one command", "eat freely — but not of that tree"),
    (18, 18, "Not good to be alone", "I will make him a helper"),
    (19, 20, "The naming", "every animal and bird brought to him"),
    (21, 23, "The woman", "taken from his side — bone of my bones"),
    (24, 25, "One flesh", "and they were not ashamed"),
]


def beat_index(v):
    for i, (lo, hi, _t, _n) in enumerate(BEATS):
        if lo <= v <= hi:
            return i
    return 0


# ---------------------------------------------------------------------------
# Scene pieces
# ---------------------------------------------------------------------------

def tree(c, x, y, live, lit, forbidden=False, label=None, sub=None,
         anchor="mb", ly=-56):
    """A schematic tree: trunk plus canopy. `live` = introduced already."""
    if not live:
        c.circle(x, y - 26, 20, fill=None, stroke=SAND_DIM, width=1.5)
        return
    canopy = GREEN if not lit else GREEN
    c.rect(x - 3, y - 22, 6, 24, fill=BROWN if not lit else GOLD)
    c.circle(x, y - 30, 21, fill=canopy, stroke=HL if lit else GREEN_DIM,
             width=2.5 if lit else 1.5)
    if lit:
        c.circle(x, y - 30, 27, stroke=g(0.85), width=2)
    if forbidden:
        c.line((x - 15, y - 45), (x + 15, y - 15), RED, 3)
        c.line((x + 15, y - 45), (x - 15, y - 15), RED, 3)
    if label:
        col = HL if lit else TEXT
        c.text((x, y + ly), label, 14, col, anchor, bold=lit)
    if sub:
        # to the side of the canopy, so it never lands on the tree itself
        c.text((x + 36, y - 30), sub, 11, RED, "lm", italic=True)


def figure(c, x, y, lit, label, scale=1.0):
    """A schematic standing figure (head + body + arms)."""
    col = HL if lit else TEXT_DIM
    h = 13 * scale
    c.circle(x, y - h - 6 * scale, 5 * scale, fill=col)
    c.line((x, y - h), (x, y), col, 2.5)
    c.line((x - 6 * scale, y - h + 4), (x + 6 * scale, y - h + 4), col, 2.5)
    c.line((x, y), (x - 5 * scale, y + 9 * scale), col, 2.5)
    c.line((x, y), (x + 5 * scale, y + 9 * scale), col, 2.5)
    if lit:
        c.circle(x, y - 8 * scale, 24 * scale, stroke=g(0.8), width=2)
    if label:
        c.text((x, y + 24 * scale), label, 13, HL if lit else TEXT, "mt",
               bold=lit)


def draw_ground(c, v):
    """The ground the man is formed from, and the mist that waters it."""
    y = SCENE[3] - 24
    c.line((SCENE[0] + 8, y), (SCENE[2] - 8, y), dim(EARTH, 210), 10)
    if 5 <= v <= 6:
        lit = True
        col = RIVER
        for i in range(6):
            mx = SCENE[0] + 46 + i * 70
            pts = [(mx, y - 6), (mx - 7, y - 26), (mx + 6, y - 46),
                   (mx - 4, y - 64)]
            if v == 6:
                c.traced(pts, stroke=col, width=2, dur="2.0s")
            else:
                c.polyline(pts, stroke=dim(col, 150), width=1.5, dash="3,5")
        c.text((SCENE[0] + 12, y - 78), "the mist", 12,
               WATER_TXT, "la", italic=True)


def draw_garden(c, v):
    """The garden itself: planted at verse 8, ghosted before that."""
    planted = v >= 8
    if not planted:
        c.ellipse(GX, GY, GRX, GRY, fill=None, stroke=SAND_DIM, width=1.5)
        return
    c.ellipse(GX, GY, GRX, GRY, fill=dim(GREEN_DIM, 120),
              stroke=GREEN if v == 8 else GREEN_DIM, width=2)
    if v == 8:
        c.ellipse(GX, GY, GRX + 7, GRY + 7, stroke=g(0.8), width=2)
    c.text((GX, GY - GRY - 12), "THE GARDEN IN EDEN", 14,
           GOLD if v == 8 else TEXT_DIM, "mb", bold=(v == 8))
    # scattered "every tree pleasant to the sight, and good for food"
    for dx, dy in ((-104, -52), (-118, 26), (-58, -88), (38, -92), (96, -58),
                   (112, 22), (46, 84), (-30, 92), (-124, -8), (114, -14)):
        c.circle(GX + dx, GY + dy, 11, fill=dim(GREEN, 130),
                 stroke=GREEN_DIM, width=1)


def draw_rivers(c, v):
    """The river out of Eden, and the four heads it parts into."""
    flowing = v >= 10
    src = SOURCE + THROUGH[1:]
    if v == 10:
        c.traced(src, stroke=RIVER, width=4, dur="2.4s")
    elif flowing:
        c.polyline(src, stroke=RIVER, width=3.5)
    else:
        c.polyline(src, stroke=SAND_DIM + (255,), width=1.5, dash="5,6")
    c.text((SOURCE[0][0] + 4, SOURCE[0][1] - 14), "the river", 12,
           WATER_TXT if flowing else TEXT_DIM, "la", italic=True)

    if flowing:
        c.circle(*PART, 6, fill=RIVER, stroke=BG, width=1.5)
        if v == 10:
            c.circle(*PART, 12, stroke=g(0.85), width=2)

    for i, (key, label, land, pts, chip_y) in enumerate(HEADS, start=1):
        trig = HEAD_VERSE[key]
        if not flowing:
            c.polyline(pts, stroke=dim(SAND_DIM, 160), width=1, dash="4,7")
        elif v == trig:
            c.traced(pts, stroke=RIVER, width=4, dur="2.4s")
        elif v > trig:
            c.polyline(pts, stroke=RIVER, width=3)
        else:
            c.polyline(pts, stroke=SAND_DIM + (255,), width=1.5, dash="5,6")

        cur = (v == trig) or (key == "PISHON" and v == 12)
        reached = flowing and v >= trig
        c.rect(CHIP_X, chip_y, CHIP_W, CHIP_H,
               fill=PANEL if reached else BG,
               stroke=None if cur else (SAND if reached else SAND_DIM),
               width=1.5, rx=4)
        if cur:
            # brightens on the verse that names the river; Pishon stays
            # current through verse 12 without re-animating
            c.pulse_rect(CHIP_X, chip_y, CHIP_W, CHIP_H, g(0.9), width=2.5,
                         first=(v == trig), rx=4)
        col = HL if cur else (TEXT if reached else TEXT_DIM)
        c.text((CHIP_X + 12, chip_y + 15), f"{i}. {label}", 16, col, "lm",
               bold=cur)
        c.text((CHIP_X + 12, chip_y + 32), land, 11,
               GOLD if cur else TEXT_DIM, "lm", italic=True)
        if key == "PISHON" and v >= 11:
            c.text((CHIP_X + 12, chip_y + CHIP_H + 13),
                   "gold · bdellium · onyx", 11,
                   HL if v == 12 else TEXT_DIM, "lm", italic=True)


def draw_trees(c, v):
    if v < 9:
        return
    tree(c, GX - 50, GY - 24, live=True, lit=(v == 9),
         label="the tree of life", ly=-72)
    tree(c, GX + 72, GY + 20, live=True, lit=(v in (9, 17)),
         forbidden=(v >= 17),
         label="the knowledge of good and evil", ly=-72)


def draw_people(c, v):
    if v < 7:
        return
    solo = v in (7, 15)
    mx, my = GX - 74, GY + 76
    figure(c, mx, my, lit=solo or v in (16, 17, 18, 19, 20, 21, 23),
           label="the man")
    if v >= 22:
        figure(c, mx + 78, my, lit=(v >= 22), label="the woman")
        c.line((mx + 16, my - 14), (mx + 62, my - 14), GOLD, 2)
        if v >= 24:
            c.text((mx + 39, my + 40), "one flesh", 13, HL, "mt", bold=True)


def draw_animals(c, v):
    if v < 19:
        return
    lit = v in (19, 20)
    y = GY + 152
    for i in range(6):
        x = GX - 96 + i * 34
        col = HL if lit else TEXT_DIM
        c.ellipse(x, y, 9, 6, fill=dim(col, 150), stroke=col, width=1.2)
        c.line((x - 4, y + 6), (x - 4, y + 11), col, 1.5)
        c.line((x + 4, y + 6), (x + 4, y + 11), col, 1.5)
        c.line((x + 9, y - 3), (x + 15, y - 7), col, 1.5)
    c.text((GX + 96, y - 2), "the animals", 12, GOLD if lit else TEXT_DIM,
           "lm", italic=True)


def draw_seventh_day(c, v):
    """Verses 1-3: the seventh day, closing Genesis 1's six."""
    if v > 3:
        return
    x0, x1 = SCENE[0] + 8, SCENE[2] - 8
    c.rect(x0, BAND_Y, x1 - x0, BAND_H, fill=PANEL, rx=5)
    c.pulse_rect(x0, BAND_Y, x1 - x0, BAND_H, g(0.95), width=2.5,
                 first=(v == 1), rx=5)
    c.text((x0 + 16, BAND_Y + BAND_H / 2), "THE SEVENTH DAY", 17, HL, "lm",
           bold=True)
    marks = [(1, "finished"), (2, "rested"), (3, "blessed and made holy")]
    tx = x0 + 215
    for mv, word in marks:
        cur = (mv == v)
        c.circle(tx, BAND_Y + BAND_H / 2, 5 if cur else 3.5,
                 fill=HL if cur else (SAND if mv < v else BG),
                 stroke=BG if cur else SAND_DIM, width=1.5)
        c.text((tx + 12, BAND_Y + BAND_H / 2), word, 14,
               HL if cur else (TEXT if mv < v else TEXT_DIM), "lm", bold=cur)
        tx += 148


# ---------------------------------------------------------------------------
# Side panel
# ---------------------------------------------------------------------------

ROW0, ROWH = 128, 33


def draw_panel(c, v):
    cur = beat_index(v)
    c.text((PANEL_X, 92), "IN THE GARDEN", 19, TEXT, "la", bold=True)
    dot_x, name_x = PANEL_X + 8, PANEL_X + 24
    top_y = ROW0
    bot_y = ROW0 + (len(BEATS) - 1) * ROWH
    c.line((dot_x, top_y), (dot_x, bot_y), SAND_DIM, 2)
    for i, (lo, hi, title, _note) in enumerate(BEATS):
        y = ROW0 + i * ROWH
        live = (i == cur)
        if live:
            c.circle(dot_x, y, 6, fill=HL, stroke=BG, width=1)
        else:
            c.circle(dot_x, y, 4, fill=SAND if i < cur else BG,
                     stroke=SAND_DIM, width=1.5)
        c.text((name_x, y), title, 14, HL if live else
               (TEXT if i < cur else TEXT_DIM), "lm", bold=live)
        rng = f"{lo}" if lo == hi else f"{lo}–{hi}"
        c.text((W - 20, y), rng, 11, TEXT_DIM, "rm", italic=True)


# ---------------------------------------------------------------------------
# Assemble one verse
# ---------------------------------------------------------------------------

def render(v):
    c = SvgCanvas(W, H, bg=BG)
    c.text((28, 24), "Genesis 2 · The Garden in Eden", 22, TEXT, "la",
           bold=True)

    c.rect(SCENE[0], SCENE[1], SCENE[2] - SCENE[0], SCENE[3] - SCENE[1],
           stroke=SAND_DIM, width=1)
    c.text((SCENE[2] - 12, SCENE[1] + 14), "east  →", 12, TEXT_DIM, "ra",
           italic=True)

    draw_ground(c, v)
    draw_garden(c, v)
    draw_rivers(c, v)
    draw_trees(c, v)
    draw_animals(c, v)
    draw_people(c, v)
    draw_seventh_day(c, v)
    draw_panel(c, v)
    return c


def main():
    total = count = 0
    for v in range(1, 26):
        c = render(v)
        out = out_path("Genesis", 2, f"Genesis_2_{v}.svg")
        c.save(out)
        total += os.path.getsize(out)
        count += 1
    print(f"Genesis 2: {count} SVG files, {total/1e3:.0f} KB")


if __name__ == "__main__":
    main()
