"""Render Genesis 6-9 (the ark and the flood) as per-verse vector SVGs.

One scene, replayed for all 97 verses (Genesis 6 = 22, 7 = 24, 8 = 22, 9 = 29).
The chapter set gives two kinds of hard detail and the graphic serves both at
once:

* the ark's dimensions — 300 x 50 x 30 cubits, three levels, a door in the
  side, a roof finished to a cubit — drawn to scale as a side elevation with a
  50 x 30 end-view callout, so the 10:1 proportions read for themselves;
* the flood's dates — the 17th day of the second month, forty days of rain,
  a hundred fifty days prevailing, rest on Ararat in the seventh month, the
  first day of the tenth, the 601st year — drawn as a dated timeline strip
  along the foot.

The water level is a function of the verse: it rises through chapter 7 until
the mountains are covered, holds, then recedes through chapter 8. The ark
floats with it, grounds on Ararat's summit at 8:4 while the water is still
above the peak (as the text has it — the tops only appear at 8:5), and stays
perched there as the water drops away. Animals queue to the door while the ship
is loading; the raven and the dove fly from the window; the rainbow arcs over
the sky from 9:13.

Run inside the project venv:
    .venv\\Scripts\\python.exe generate_genesis69_svg.py
"""

import os

from svg_surface import SvgCanvas
from generate_tabernacle import (W, H, BG, PANEL, SAND, SAND_DIM, SILVER, TEXT,
                                 TEXT_DIM, GOLD, HL, BROWN, GRAY, out_path)
from generate_tribal_maps import RIVER, RIVER_DIM, WATER_TXT


GREEN = (86, 122, 78)
DECK = (96, 74, 50)            # timber
HULL = (74, 58, 40)
FLOOD = (38, 58, 84)           # the risen waters
FLOOD_TOP = (86, 122, 160)
RED = (170, 70, 60)            # the corruption of 6:5-13
RED_WASH = (150, 52, 44)
RAINBOW = [(122, 134, 216), (154, 95, 176), (200, 85, 85), (214, 168, 92),
           (110, 158, 120)]

CH_LEN = {6: 22, 7: 24, 8: 22, 9: 29}
OFFSET = {6: 0, 7: 22, 8: 46, 9: 68}


def pos(ch, v):
    return OFFSET[ch] + v


def g(alpha):
    return HL + (int(255 * alpha),)


def dim(color, a):
    """`color` with an 0-255 alpha, in the (r, g, b, a) form SvgCanvas takes
    (it turns the fourth element into a fill-/stroke-opacity)."""
    return color + (int(a),)


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

SCENE = (24, 82, 1000, 432)     # x0, y0, x1, y1
GROUND_Y = 400                  # the plain
TOP_WATER_Y = 220               # water level when the mountains are covered
                                # (kept clear of the state badge above)
ARARAT_X, ARARAT_Y = 520, 252   # the summit the ark grounds on

CUBIT = 2.4                     # px per cubit
ARK_X0 = 200
ARK_L = 300 * CUBIT             # 720 px
ARK_H = 30 * CUBIT              # 72 px
ARK_X1 = ARK_X0 + ARK_L         # 920

END_X, END_Y = 40, 100          # the 50 x 30 end-view callout
END_W, END_H = 50 * CUBIT, 30 * CUBIT

BAR_Y = 496                     # the dated timeline strip

# ---------------------------------------------------------------------------
# Water level by reading position (last breakpoint at or before the verse)
# ---------------------------------------------------------------------------

WATER = [
    ((6, 1), 0.0),
    ((7, 10), 0.05), ((7, 11), 0.12), ((7, 12), 0.22), ((7, 17), 0.50),
    ((7, 18), 0.66), ((7, 19), 0.86), ((7, 20), 1.00),
    ((8, 1), 0.95), ((8, 3), 0.86), ((8, 4), 0.78), ((8, 5), 0.62),
    ((8, 6), 0.50), ((8, 8), 0.42), ((8, 10), 0.34), ((8, 12), 0.26),
    ((8, 13), 0.10), ((8, 14), 0.0),
]


def water_level(ch, v):
    p = pos(ch, v)
    lvl = 0.0
    for (bc, bv), value in WATER:
        if pos(bc, bv) <= p:
            lvl = value
    return lvl


def water_y(ch, v):
    return GROUND_Y - water_level(ch, v) * (GROUND_Y - TOP_WATER_Y)


# ark state -> badge text
STATES = [
    ((6, 1), "before the flood", "the earth is corrupt; the ark not yet commanded"),
    ((6, 14), "under construction", "gopher wood, pitch, three levels"),
    ((7, 1), "loading", "the household and the animals go in"),
    ((7, 17), "afloat", "the waters prevail on the earth"),
    ((8, 4), "rested on Ararat", "grounded while the waters recede"),
    ((8, 18), "emptied", "every living thing goes out"),
    ((9, 8), "the covenant", "never again a flood to destroy the earth"),
]


def state(ch, v):
    p = pos(ch, v)
    chosen = STATES[0]
    for entry in STATES:
        if pos(*entry[0]) <= p:
            chosen = entry
    return chosen[1], chosen[2]


def afloat(ch, v):
    return (7, 17) <= (ch, v) < (8, 4) if ch in (7, 8) else False


def grounded(ch, v):
    return pos(ch, v) >= pos(8, 4)


def ark_top(ch, v):
    """The ark's top edge: on the ground before the flood, riding the water
    while afloat, perched on Ararat's summit once grounded."""
    if grounded(ch, v):
        return ARARAT_Y - ARK_H
    if water_level(ch, v) >= 0.5:
        return water_y(ch, v) - ARK_H - 2
    return GROUND_Y - ARK_H


# ---------------------------------------------------------------------------
# The dated timeline (13 stops).  (label, note, trigger (ch, v))
# ---------------------------------------------------------------------------

STOPS = [
    ("before", "the ark built", (6, 14)),
    ("600th yr", "the flood comes", (7, 6)),
    ("2 · 17", "the deep bursts", (7, 11)),
    ("40 days", "of rain", (7, 12)),
    ("150 days", "waters prevail", (7, 24)),
    ("7 · 17", "rests on Ararat", (8, 4)),
    ("10 · 1", "peaks appear", (8, 5)),
    ("+40 days", "the raven", (8, 6)),
    ("+7 days", "the dove", (8, 8)),
    ("+7 days", "the olive leaf", (8, 10)),
    ("601 · 1 · 1", "waters dried", (8, 13)),
    ("2 · 27", "the earth dry", (8, 14)),
    ("after", "the covenant", (9, 8)),
]


def stop_index(ch, v):
    """The last stop reached at this verse (-1 before the first)."""
    p = pos(ch, v)
    idx = -1
    for i, (_l, _n, trig) in enumerate(STOPS):
        if pos(*trig) <= p:
            idx = i
    return idx


# ---------------------------------------------------------------------------
# Captions
# ---------------------------------------------------------------------------

# The ark's given measurements, lit on the verse that gives them.
DIMS = {"length": 15, "width": 15, "height": 15, "levels": 16,
        "door": 16, "roof": 16, "pitch": 14}

# Loading verses -> (how many pairs to draw, label)
LOADING = {
    (6, 19): (6, "two and two"),
    (6, 20): (6, "two and two"),
    (7, 2): (7, "seven and seven — the clean"),
    (7, 3): (7, "seven and seven"),
    (7, 8): (6, "two and two"),
    (7, 9): (6, "two and two"),
    (7, 14): (6, "two and two"),
    (7, 15): (6, "two and two"),
}

# The household enters (7:7, 7:13) / goes out (8:18)
HOUSEHOLD = {(7, 7), (7, 13), (8, 16), (8, 18)}


# ---------------------------------------------------------------------------
# Scene pieces
# ---------------------------------------------------------------------------

def draw_sky_and_rain(c, ch, v):
    p = pos(ch, v)
    raining = pos(7, 11) <= p <= pos(7, 12)
    if raining:
        for i in range(34):
            x = SCENE[0] + 14 + i * 28.5
            c.line((x, SCENE[1] + 4), (x - 6, SCENE[1] + 46),
                   dim(FLOOD_TOP, 150), 1.5)
        c.text((SCENE[0] + 12, SCENE[1] + 58), "the windows of the sky", 12,
               WATER_TXT, "la", italic=True)


def draw_rainbow(c, ch, v):
    """The covenant sign, arcing over the whole sky. Drawn inside a clipped
    group so the legs stop at the scene edge instead of running down through
    the timeline; drawn before the mountains, so they occlude it as ground
    does a real rainbow."""
    if ch != 9 or v < 13:
        return
    lit = (v in (13, 16, 17))
    cx, cy = 512 - SCENE[0], 470 - SCENE[1]
    with c.group(SCENE[0], SCENE[1],
                 clip=(SCENE[2] - SCENE[0], SCENE[3] - SCENE[1])):
        for i, col in enumerate(RAINBOW):
            r = 330 + i * 12
            c.path(f"M{cx - r},{cy} A{r},{r} 0 0 1 {cx + r},{cy}",
                   fill=None, stroke=col if lit else dim(col, 170), width=7)
    c.text((SCENE[0] + 12, SCENE[1] + 18), "the rainbow", 13,
           HL if lit else TEXT_DIM, "la", italic=True)


# ---------------------------------------------------------------------------
# Per-verse motion: the level moves from where the previous verse left it to
# this verse's, once, then freezes — the same "draw once, then hold" rule the
# traced reveals follow. Built as raw elements because what animates here is
# geometry (a rect's y/height, a line's ends, the hull's offset), which the
# SvgCanvas primitives do not animate.
# ---------------------------------------------------------------------------

_EASE = "0.42 0 0.58 1"
_RISE_DUR = "1.8s"


def _num(x):
    return f"{x:.2f}".rstrip("0").rstrip(".")


def _paint(color):
    r, g_, b = color[:3]
    out = f'fill="rgb({int(r)},{int(g_)},{int(b)})"'
    if len(color) > 3 and color[3] < 255:
        out += f' fill-opacity="{color[3] / 255.0:.3f}"'
    return out


def _anim(attr, v_from, v_to, dur=_RISE_DUR):
    return (f'<animate attributeName="{attr}" values="{_num(v_from)};'
            f'{_num(v_to)}" dur="{dur}" begin="0s" fill="freeze" '
            f'calcMode="spline" keyTimes="0;1" keySplines="{_EASE}"/>')


def _rise_rect(c, x, w, y_from, y_to, color):
    """A body of water whose top edge moves from y_from to y_to."""
    h_from, h_to = SCENE[3] - y_from, SCENE[3] - y_to
    c.raw([f'<rect x="{_num(x)}" y="{_num(y_from)}" width="{_num(w)}" '
           f'height="{_num(h_from)}" {_paint(color)}>'
           + _anim("y", y_from, y_to) + _anim("height", h_from, h_to)
           + "</rect>"])


def _rise_line(c, x0, x1, y_from, y_to, color, width):
    """The surface line, following the same move."""
    c.raw([f'<line x1="{_num(x0)}" y1="{_num(y_from)}" x2="{_num(x1)}" '
           f'y2="{_num(y_from)}" stroke="rgb({int(color[0])},'
           f'{int(color[1])},{int(color[2])})" stroke-width="{_num(width)}">'
           + _anim("y1", y_from, y_to) + _anim("y2", y_from, y_to)
           + "</line>"])


def prev_verse(ch, v):
    """The verse read before this one, across the chapter break."""
    if v > 1:
        return ch, v - 1
    if ch == 6:
        return None
    prev_ch = ch - 1
    return prev_ch, CH_LEN[prev_ch]


def prev_water_y(ch, v):
    pv = prev_verse(ch, v)
    return GROUND_Y if pv is None else water_y(*pv)


def prev_ark_top(ch, v):
    pv = prev_verse(ch, v)
    return ark_top(ch, v) if pv is None else ark_top(*pv)


# ---------------------------------------------------------------------------
# Before the flood (6:1-13) — the generation the ark answers
# ---------------------------------------------------------------------------

PRE_ARK_Y = 236          # the slim "not yet commanded" placeholder,
                         # kept high so the plain below is the scene
CROWD_X0, CROWD_STEP = 340, 44
CROWD_AT = {1: 9, 2: 14}          # how many stand there
NOAH_X, SON_X = 140, (192, 240, 288)


def draw_before_flood(c, ch, v):
    """Verses 6:1-13: the multiplying generation on the right, the one man
    who found favor on the left, and the corruption that settles over both."""
    if ch != 6 or v > 13:
        return
    corrupt = (v >= 5)
    if corrupt:      # a wash over the whole plain
        depth = 26 if v < 11 else 44
        c.rect(SCENE[0], GROUND_Y - 108, SCENE[2] - SCENE[0], 108 + 32,
               fill=dim(RED_WASH, depth))

    n = CROWD_AT.get(v, 14)
    for i in range(n):
        x = CROWD_X0 + i * CROWD_STEP
        col = dim(TEXT_DIM, 210) if corrupt else SAND
        figure(c, x, GROUND_Y - 6, col, scale=0.8)
    if v == 2:
        for i in range(0, n, 3):     # the daughters, among them
            c.circle(CROWD_X0 + i * CROWD_STEP, GROUND_Y - 40, 13,
                     stroke=g(0.7), width=1.5)

    if v == 3:      # the span set on him
        y = GROUND_Y - 78
        c.line((CROWD_X0, y), (CROWD_X0 + (n - 1) * CROWD_STEP, y), GOLD, 2)
        for x in (CROWD_X0, CROWD_X0 + (n - 1) * CROWD_STEP):
            c.line((x, y - 5), (x, y + 5), GOLD, 2)
        c.text((CROWD_X0 + (n - 1) * CROWD_STEP / 2, y - 8),
               "120 years", 13, HL, "mb", bold=True)

    if v == 4:      # taller among them
        for x in (CROWD_X0 + 3 * CROWD_STEP, CROWD_X0 + 8 * CROWD_STEP):
            figure(c, x, GROUND_Y - 6, HL, scale=1.5)
        c.text((CROWD_X0 + 5.5 * CROWD_STEP, GROUND_Y - 44), "the Nephilim",
               13, HL, "mb", bold=True)

    if v >= 8:      # the one man
        figure(c, NOAH_X, GROUND_Y - 6, GOLD if v >= 9 else HL, scale=1.0)
        c.circle(NOAH_X, GROUND_Y - 24, 30, stroke=g(0.8), width=2)
        c.text((NOAH_X, GROUND_Y - 62), "Noah", 15, HL, "mb", bold=True)
    if v >= 10:
        for x, name in zip(SON_X, ("Shem", "Ham", "Japheth")):
            figure(c, x, GROUND_Y - 6, HL if v == 10 else SAND, scale=0.8)
            c.text((x, GROUND_Y + 18), name, 10,
                   GOLD if v == 10 else TEXT_DIM, "mt", italic=True)



def draw_mountains(c, ch, v):
    """A range across the plain, with Ararat the highest summit."""
    peaks = [(120, 336), (250, 318), (ARARAT_X, ARARAT_Y), (700, 322),
             (860, 344)]
    pts = [(SCENE[0], GROUND_Y)]
    for px, py in peaks:
        pts += [(px - 92, GROUND_Y), (px, py), (px + 92, GROUND_Y)]
    pts += [(SCENE[2], GROUND_Y)]
    c.polygon(pts, fill=dim(GRAY, 110), stroke=SAND_DIM, width=1.5)
    c.rect(SCENE[0], GROUND_Y, SCENE[2] - SCENE[0], SCENE[3] - GROUND_Y,
           fill=dim(BROWN, 130))
    if grounded(ch, v):
        lit = (ch == 8 and v in (4, 5))
        c.text((ARARAT_X, ARARAT_Y - 12), "Ararat", 14,
               HL if lit else TEXT_DIM, "mb", bold=lit, italic=not lit)


def draw_water(c, ch, v):
    lvl = water_level(ch, v)
    prev_y = prev_water_y(ch, v)
    if lvl <= 0 and prev_y >= GROUND_Y:
        return
    wy = water_y(ch, v)
    moving = abs(prev_y - wy) > 0.5
    if moving:
        # the surface rises (or falls) from where the previous verse left it
        # into this verse's level, once, then holds
        _rise_rect(c, SCENE[0], SCENE[2] - SCENE[0], prev_y, wy,
                   dim(FLOOD, 205))
        _rise_line(c, SCENE[0], SCENE[2], prev_y, wy, FLOOD_TOP, 2.5)
    else:
        c.rect(SCENE[0], wy, SCENE[2] - SCENE[0], SCENE[3] - wy,
               fill=dim(FLOOD, 205))
        c.line((SCENE[0], wy), (SCENE[2], wy), FLOOD_TOP, 2.5)
    p = pos(ch, v)
    if pos(7, 11) <= p <= pos(7, 12):     # fountains of the great deep
        for i in range(7):
            x = SCENE[0] + 90 + i * 130
            c.polyline([(x, SCENE[3] - 6), (x - 7, SCENE[3] - 34),
                        (x + 6, wy + 12)], stroke=FLOOD_TOP, width=2,
                       dash="4,5")
    # below the surface line, so the label never lands on the hull
    if ch == 7 and v == 20:
        c.text((SCENE[2] - 14, wy + 14), "15 cubits higher", 12, HL,
               "ra", italic=True)



def draw_ark(c, ch, v):
    """The side elevation: hull, three decks, door, roof ridge, window.

    Whenever the water level has changed the whole hull rides with it: the
    group starts at the previous verse's height and glides to this one's,
    once, then freezes."""
    p = pos(ch, v)
    built = p >= pos(6, 14)
    top = ark_top(ch, v)
    bot = top + ARK_H

    if not built:
        # A slim placeholder rather than the full hull: verses 1-13 have not
        # reached the command yet, and the ground below belongs to the
        # pre-flood scene (draw_before_flood).
        c.rect(ARK_X0, PRE_ARK_Y, ARK_L, 30, fill=None,
               stroke=dim(SAND_DIM, 200), width=1.5)
        return

    lift = prev_ark_top(ch, v) - top
    riding = abs(lift) > 0.5
    if riding:
        c.raw([f'<g><animateTransform attributeName="transform" '
               f'type="translate" values="0 {_num(lift)};0 0" '
               f'dur="{_RISE_DUR}" begin="0s" fill="freeze" '
               f'calcMode="spline" keyTimes="0;1" keySplines="{_EASE}"/>'])

    building = p < pos(7, 1)
    c.rect(ARK_X0, top, ARK_L, ARK_H, fill=dim(HULL, 235), stroke=SAND,
           width=2, rx=3)
    # roof "finished to a cubit upward"
    roof_lit = (ch == 6 and v == 16)
    c.polyline([(ARK_X0 + 6, top), (ARK_X0 + 30, top - 6),
                (ARK_X1 - 30, top - 6), (ARK_X1 - 6, top)],
               stroke=HL if roof_lit else SAND, width=2.5)
    # three levels
    lv_lit = (ch == 6 and v == 16)
    for i, name in ((1, "third"), (2, "second"), (3, "lower")):
        dy = top + (i - 1) * (ARK_H / 3)
        if i > 1:
            c.line((ARK_X0 + 3, dy), (ARK_X1 - 3, dy),
                   HL if lv_lit else dim(DECK, 220), 2 if lv_lit else 1.5)
        c.text((ARK_X0 + 12, dy + ARK_H / 6), name, 11,
               GOLD if lv_lit else TEXT_DIM, "lm", italic=True)
    # rooms
    for i in range(1, 12):
        x = ARK_X0 + i * (ARK_L / 12)
        c.line((x, top + 2), (x, bot - 2), dim(DECK, 150), 1)
    # the door in the side
    door_lit = (ch == 6 and v == 16) or (ch == 7 and v == 16)
    dx0 = ARK_X0 + ARK_L * 0.13
    c.rect(dx0, bot - ARK_H / 3 + 4, 26, ARK_H / 3 - 8,
           fill=BG if not (ch == 7 and v >= 16) else dim(SAND, 220),
           stroke=HL if door_lit else SAND, width=2)

    # the window Noah opens in 8:6
    if pos(ch, v) >= pos(8, 6):
        wx = ARK_X1 - 120
        c.rect(wx, top + 8, 18, 14, fill=BG, stroke=GOLD, width=2)
        if ch == 8 and v == 6:
            c.text((wx + 9, top - 10), "the window", 12, HL, "mb",
                   italic=True)
    if riding:
        c.raw(["</g>"])


def draw_dimensions(c, ch, v):
    """The measured callouts along and beside the elevation. Only while the
    ship is being built — from 6:19 the ground below it belongs to the queue
    of animals."""
    if ch != 6 or not (14 <= v <= 18):
        return
    top = ark_top(ch, v)
    lit = (ch == 6 and v == 15)
    col = HL if lit else TEXT_DIM
    y = GROUND_Y + 18
    c.line((ARK_X0, y), (ARK_X1, y), col, 1.5)
    for x in (ARK_X0, ARK_X1):
        c.line((x, y - 5), (x, y + 5), col, 1.5)
    c.text(((ARK_X0 + ARK_X1) / 2, y + 4), "300 cubits", 13, col, "mt",
           bold=lit)
    hx = ARK_X1 + 16
    c.line((hx, top), (hx, top + ARK_H), col, 1.5)
    c.line((hx - 5, top), (hx + 5, top), col, 1.5)
    c.line((hx - 5, top + ARK_H), (hx + 5, top + ARK_H), col, 1.5)
    c.text((hx + 8, top + ARK_H / 2 - 7), "30", 13, col, "lm", bold=lit)
    c.text((hx + 8, top + ARK_H / 2 + 7), "cubits", 11, col, "lm",
           italic=True)


def draw_end_view(c, ch, v):
    """The 50 x 30 cross-section callout, so the width is not just a number."""
    if ch != 6 or v < 14:
        return
    lit = (ch == 6 and v == 15)
    c.rect(END_X - 6, END_Y - 20, END_W + 12, END_H + 46, fill=BG,
           stroke=SAND_DIM, width=1)
    c.text((END_X + END_W / 2, END_Y - 16), "end view", 11, TEXT_DIM, "mt",
           italic=True)
    c.rect(END_X, END_Y, END_W, END_H, fill=dim(HULL, 235),
           stroke=HL if lit else SAND, width=2)
    for i in (1, 2):
        yy = END_Y + i * (END_H / 3)
        c.line((END_X + 2, yy), (END_X + END_W - 2, yy), dim(DECK, 220), 1.5)
    c.text((END_X + END_W / 2, END_Y + END_H + 12),
           "50 × 30 cubits", 12, HL if lit else TEXT_DIM, "mt", bold=lit)


def creature(c, x, y, col):
    c.ellipse(x, y, 6.5, 4, fill=dim(col, 150), stroke=col, width=1.2)
    c.line((x - 3, y + 4), (x - 3, y + 9), col, 1.4)
    c.line((x + 3, y + 4), (x + 3, y + 9), col, 1.4)
    c.line((x + 6.5, y - 2), (x + 11, y - 6), col, 1.4)


def figure(c, x, y, col, scale=0.85):
    h = 13 * scale
    c.circle(x, y - h - 6 * scale, 4.6 * scale, fill=col)
    c.line((x, y - h), (x, y), col, 2.2)
    c.line((x - 5.5 * scale, y - h + 4), (x + 5.5 * scale, y - h + 4), col, 2)
    c.line((x, y), (x - 4.5 * scale, y + 8 * scale), col, 2)
    c.line((x, y), (x + 4.5 * scale, y + 8 * scale), col, 2)


def draw_loading(c, ch, v):
    """The queue at the door: the animals by pairs, then the household of
    eight. Both stay west of the hull (x < 190) and route along the ground
    up into the door, so nothing is drawn over the ship."""
    key = (ch, v)
    door_x = ARK_X0 + ARK_L * 0.13 + 13
    ramp_y = GROUND_Y + 12
    if key in LOADING:
        n, label = LOADING[key]
        y = GROUND_Y - 14
        for i in range(n):
            bx = 52 + i * 24
            creature(c, bx, y, HL)
            creature(c, bx + 9, y + 3, GOLD)
        c.text((52, GROUND_Y + 26), label, 12, HL, "la", italic=True)
        c.polyline([(52 + n * 24, y), (188, y), (188, ramp_y),
                    (door_x, ramp_y), (door_x, GROUND_Y - 6)],
                   stroke=GOLD, width=1.5, dash="5,5")
    if key in HOUSEHOLD:
        going_out = (ch == 8)
        for i in range(8):
            figure(c, 50 + i * 20, GROUND_Y - 10, HL, scale=0.7)
        c.text((50, GROUND_Y + 26), "eight", 12, HL, "la", italic=True)
        path = [(214, GROUND_Y - 16), (188, GROUND_Y - 16)]
        c.polyline(path if going_out else path[::-1], stroke=GOLD, width=2,
                   dash="4,5")


def bird(c, x, y, col, leaf=False):
    c.polyline([(x - 9, y), (x - 3, y - 6), (x + 2, y - 1)], stroke=col,
               width=2)
    c.polyline([(x + 2, y - 1), (x + 7, y - 7), (x + 12, y)], stroke=col,
               width=2)
    if leaf:
        c.ellipse(x + 14, y + 3, 5, 2.6, fill=GREEN, stroke=GREEN)


def draw_birds(c, ch, v):
    """The raven and the dove, out of the window Noah opened."""
    if ch != 8 or not (7 <= v <= 12):
        return
    top = ark_top(ch, v)
    wx, wy = ARK_X1 - 111, top + 15
    if v == 7:
        path = [(wx, wy), (wx + 60, wy - 34), (wx + 20, wy - 58),
                (wx - 30, wy - 30), (wx + 34, wy - 12)]
        c.polyline(path, stroke=dim(SILVER, 150), width=1.5, dash="4,5")
        bird(c, wx + 34, wy - 12, SILVER)
        c.text((wx + 60, wy - 66), "the raven", 12, HL, "lm", italic=True)
        return
    out = [(wx, wy), (wx + 46, wy - 26), (wx + 96, wy - 34)]
    if v in (8, 9):
        c.polyline(out, stroke=dim(HL, 150), width=1.5, dash="4,5")
        c.polyline([(wx + 96, wy - 30), (wx + 46, wy - 20), (wx, wy + 4)],
                   stroke=dim(HL, 110), width=1.5, dash="2,5")
        bird(c, wx + 18, wy - 6, HL)
        c.text((wx + 106, wy - 38), "the dove", 12, HL, "lm", italic=True)
    elif v in (10, 11):
        c.polyline(out, stroke=dim(HL, 150), width=1.5, dash="4,5")
        bird(c, wx + 24, wy - 10, HL, leaf=(v == 11))
        if v == 11:
            c.text((wx + 106, wy - 38), "the olive leaf", 12, HL, "lm",
                   italic=True)
    else:      # v == 12, she does not return
        far = [(wx, wy), (wx + 50, wy - 30), (wx + 120, wy - 48)]
        c.polyline(far, stroke=dim(HL, 150), width=1.5, dash="4,5")
        bird(c, wx + 120, wy - 48, HL)



def draw_altar(c, ch, v):
    """Noah's altar (8:20-22) on the dry ground."""
    if pos(ch, v) < pos(8, 20):
        return
    lit = (ch == 8 and 20 <= v <= 22)
    x, y = 400, GROUND_Y - 8
    c.polygon([(x - 20, y + 8), (x + 20, y + 8), (x + 14, y - 6),
               (x - 14, y - 6)], fill=dim(SAND_DIM, 210),
              stroke=HL if lit else SAND_DIM, width=1.5)
    c.polygon([(x, y - 30), (x + 8, y - 12), (x - 8, y - 12)],
              fill=GOLD if lit else dim(GOLD, 150), stroke=GOLD, width=1.5)
    if lit:
        c.text((x, y + 24), "the altar", 12, HL, "mt", italic=True)


def draw_sons(c, ch, v):
    """Genesis 9:18-27 — the three sons, and the word over each."""
    if ch != 9 or v < 18:
        return
    sons = [
        ("Shem", "blessed be Yahweh, the God of Shem", 26),
        ("Ham", "the father of Canaan", 18),
        ("Japheth", "may God enlarge Japheth", 27),
    ]
    bw, bh = 96, 46

    def son_lit(name, verse, vv):
        return (vv == verse) or (vv in (18, 19)) or (name == "Ham"
                                                    and vv == 22)

    for i, (name, note, verse) in enumerate(sons):
        x = 690 + i * 102
        y = 302
        lit = son_lit(name, verse, v)
        c.rect(x, y, bw, bh, fill=PANEL, stroke=None if lit else SAND,
               width=1.5, rx=4)
        if lit:
            # brightens when this son becomes the subject, then holds
            c.pulse_rect(x, y, bw, bh, g(0.9), width=2,
                         first=not son_lit(name, verse, v - 1), rx=4)
        c.text((x + bw / 2, y + 15), name, 14, HL if lit else TEXT, "mm",
               bold=lit)
        c.text((x + bw / 2, y + 32), "· · ·" if v < 22 else
               ("saw" if name == "Ham" else "covered"), 10,
               GOLD if lit else TEXT_DIM, "mm", italic=True)
    if v >= 25:
        lit = (v in (25, 26, 27))
        cx = 792
        c.line((cx, 348), (cx, 366), SAND_DIM, 1.5)
        c.rect(722, 366, 140, 30, fill=PANEL,
               stroke=(170, 70, 60) if lit else SAND, width=1.5, rx=4)
        c.text((792, 381), "Canaan is cursed", 13,
               HL if lit else TEXT, "mm", bold=lit)
    if v >= 28:
        c.text((690, 286), "Noah · 950 years", 12, HL, "la", italic=True)


def draw_badge(c, ch, v):
    label, note = state(ch, v)
    c.rect(SCENE[2] - 268, SCENE[1] + 6, 260, 30, fill=PANEL,
           stroke=SAND_DIM, width=1, rx=4)
    c.text((SCENE[2] - 256, SCENE[1] + 21), label.upper(), 14, GOLD, "lm",
           bold=True)


def draw_timeline(c, ch, v):
    idx = stop_index(ch, v)
    x0, x1 = 60, 980
    step = (x1 - x0) / (len(STOPS) - 1)
    c.line((x0, BAR_Y), (x1, BAR_Y), SAND_DIM, 2)
    if idx >= 0:
        c.line((x0, BAR_Y), (x0 + idx * step, BAR_Y), GOLD, 2.5)
    for i, (label, note, trig) in enumerate(STOPS):
        x = x0 + i * step
        cur = (pos(*trig) == pos(ch, v))
        past = (i <= idx)
        if cur:
            c.circle(x, BAR_Y, 6.5, fill=HL, stroke=BG, width=1.5)
            c.circle(x, BAR_Y, 12, stroke=g(0.85), width=2)
        else:
            c.circle(x, BAR_Y, 4, fill=SAND if past else BG, stroke=SAND_DIM,
                     width=1.5)
        c.text((x, BAR_Y - 14), label, 12,
               HL if cur else (TEXT if past else TEXT_DIM), "mb", bold=cur)
        c.text((x, BAR_Y + 16), note, 10,
               GOLD if cur else TEXT_DIM, "mm", italic=True)
        c.text((x, BAR_Y + 30), f"{trig[0]}:{trig[1]}", 10,
               TEXT_DIM if not cur else GOLD, "mm")


# ---------------------------------------------------------------------------
# Assemble one verse
# ---------------------------------------------------------------------------

def render(ch, v):
    c = SvgCanvas(W, H, bg=BG)
    c.text((28, 24), f"Genesis {ch} · The Ark and the Flood", 22, TEXT, "la",
           bold=True)

    draw_sky_and_rain(c, ch, v)
    draw_rainbow(c, ch, v)
    draw_mountains(c, ch, v)
    draw_water(c, ch, v)
    draw_ark(c, ch, v)
    draw_before_flood(c, ch, v)
    draw_dimensions(c, ch, v)
    draw_loading(c, ch, v)
    draw_birds(c, ch, v)
    draw_altar(c, ch, v)
    draw_sons(c, ch, v)
    draw_end_view(c, ch, v)
    draw_badge(c, ch, v)
    draw_timeline(c, ch, v)
    return c


def main():
    total = count = 0
    for ch in (6, 7, 8, 9):
        for v in range(1, CH_LEN[ch] + 1):
            c = render(ch, v)
            out = out_path("Genesis", ch, f"Genesis_{ch}_{v}.svg")
            c.save(out)
            total += os.path.getsize(out)
            count += 1
    print(f"Genesis 6-9: {count} SVG files, {total/1e3:.0f} KB")


if __name__ == "__main__":
    main()
