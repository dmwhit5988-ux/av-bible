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
floats with it. Animals queue to the door while the ship is loading; the raven
and the dove fly from the window; the rainbow arcs over the sky from 9:13.

There are two camera positions, and the ark grounding is the cut between them:

* the flood view (6:1 - 8:3) — the side elevation square on, the water rising
  across the whole frame;
* the rested view (8:4 - 9:29) — the camera comes round and down. Ararat is a
  whole massif with its summit to the right and a broad rock shoulder under it,
  the hull is seen three-quarter and tilted along the shoulder it settled on,
  and the flank falls away to the left toward the plain the household walks
  down to. The water table works exactly as before; it just drains down a
  mountainside instead of past a row of peaks.

The door follows the text and nothing else: set in the side at 6:16, standing
open through the whole loading, shut at 7:16 ("and the LORD shut him in") and
still shut through every verse of the flood, opened again only at 8:18 when
they go out.

Run inside the project venv:
    .venv\\Scripts\\python.exe generate_genesis69_svg.py
"""

import math
import os

import svg_figures as F
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
# The hull's shape
#
# The given measurements are a box — 300 x 50 x 30 — and the elevation is drawn
# to that scale, but a plain rectangle does not read as a ship. Rounding the
# two bottom corners costs nothing in accuracy (the cubits along and up are
# unchanged) and buys the whole silhouette: flat deck, straight sides, a bilge
# turning into a flat keel.
# ---------------------------------------------------------------------------

BILGE_RX = 0.09                 # of the length, at each end
BILGE_RY = 0.45                 # of the height


def hull_points(x0, top, length, height, steps=9):
    """The side elevation traced as a closed outline."""
    x1, bot = x0 + length, top + height
    rx, ry = length * BILGE_RX, height * BILGE_RY
    pts = [(x0, top), (x1, top), (x1, bot - ry)]
    for cx, a0 in ((x1 - rx, 0.0), (x0 + rx, 90.0)):
        for i in range(steps + 1):
            a = math.radians(a0 + 90.0 * i / steps)
            pts.append((cx + rx * math.cos(a), bot - ry + ry * math.sin(a)))
    return pts


def hull_bottom(x, x0, top, length, height):
    """How far down the hull reaches at `x` — so the room dividers stop at the
    planking instead of poking out through the turn of the bilge."""
    x1, bot = x0 + length, top + height
    rx, ry = length * BILGE_RX, height * BILGE_RY
    if x0 + rx <= x <= x1 - rx:
        return bot
    cx = x0 + rx if x < x0 + rx else x1 - rx
    t = min(1.0, abs(x - cx) / rx)
    return bot - ry + ry * math.sqrt(max(0.0, 1.0 - t * t))


def clip_below(points, y):
    """The part of a closed outline at or below `y` — used to tint the hull's
    draft, so the ship sits in the water instead of on it."""
    out = []
    for i, a in enumerate(points):
        b = points[(i + 1) % len(points)]
        a_in, b_in = a[1] >= y, b[1] >= y
        if a_in:
            out.append(a)
        if a_in != b_in:
            t = (y - a[1]) / (b[1] - a[1])
            out.append((a[0] + (b[0] - a[0]) * t, y))
    return out


def hull_inset(y, top, length, height):
    """How far in from each end the hull has drawn at `y` — the same trim for
    the deck lines."""
    ry = height * BILGE_RY
    bot = top + height
    if y <= bot - ry:
        return 0.0
    t = min(1.0, (y - (bot - ry)) / ry)
    return length * BILGE_RX * (1.0 - math.sqrt(max(0.0, 1.0 - t * t)))


def draw_door(c, x, y, w, h, st, lit, xf=None):
    """The door in the ark's side. `xf` maps the corners into place, so the
    same door serves the square-on elevation and the tilted rested view."""
    if st == "none":
        return
    xf = xf or (lambda p: p)
    box = [xf((x, y)), xf((x + w, y)), xf((x + w, y + h)), xf((x, y + h))]
    edge = HL if lit else SAND
    if st == "shut":
        c.polyline(box, stroke=edge, width=2, closed=True, fill=dim(SAND, 210))
        for f in (0.34, 0.67):                  # planked across
            c.line(xf((x + w * f, y + 1.5)), xf((x + w * f, y + h - 1.5)),
                   dim(BROWN, 200), 1.2)
        c.line(xf((x - 2, y + h * 0.44)), xf((x + w + 2, y + h * 0.44)),
               edge, 2)                          # and barred
    else:
        c.polyline(box, stroke=edge, width=2, closed=True, fill=BG)
    if lit:
        pad = 3
        c.pulse_outline([xf((x - pad, y - pad)), xf((x + w + pad, y - pad)),
                         xf((x + w + pad, y + h + pad)),
                         xf((x - pad, y + h + pad))], g(0.9), width=2)

# ---------------------------------------------------------------------------
# Water level by reading position (last breakpoint at or before the verse)
# ---------------------------------------------------------------------------

WATER = [
    ((6, 1), 0.0),
    # it climbs the hull's side while the ark is still aground, then 7:17 is
    # where "the waters increased, and bare up the ark" and it lifts
    ((7, 10), 0.02), ((7, 11), 0.06), ((7, 12), 0.12), ((7, 17), 0.50),
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


def ground_dry(ch, v):
    """Whether there is still plain to stand on beside the ark."""
    return water_level(ch, v) <= 0.06


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


REST_AT = (8, 4)             # "the ark rested upon the mountains of Ararat"


def rested(ch, v):
    """True once the ark grounds — which is also where the camera cuts from
    the flood view to the rested view."""
    return pos(ch, v) >= pos(*REST_AT)


DRAFT = 0.24                 # how much of the hull rides under the surface


def ark_top(ch, v):
    """The ark's top edge in the flood view: on the ground before the flood,
    riding the water once there is enough of it to float on — and riding *in*
    it, drawing its draft, rather than perched on the surface."""
    if water_level(ch, v) >= 0.5:
        return water_y(ch, v) - ARK_H * (1 - DRAFT)
    return GROUND_Y - ARK_H


# ---------------------------------------------------------------------------
# The door
# ---------------------------------------------------------------------------

# Where in the side it sits, in both views: along at 0.28 of the length, and
# up on the middle storey — the lower one is under water for the whole flood,
# and a door that reads as shut is the point.
DOOR_AT = 0.28
DOOR_MADE = (6, 16)          # "the door of the ark shalt thou set in the side"
DOOR_SHUT = (7, 16)          # "and the LORD shut him in"
DOOR_OPEN = (8, 18)          # "and Noah went forth"

DOOR_LABEL = {DOOR_MADE: "the door", DOOR_SHUT: "shut", DOOR_OPEN: "opened"}


def door_state(ch, v):
    """none / open / shut. It is not there before it is commanded, stands open
    for the whole loading, and once the LORD shuts it at 7:16 it stays shut
    through every verse of the flood — it opens again only at 8:18."""
    p = pos(ch, v)
    if p < pos(*DOOR_MADE):
        return "none"
    if pos(*DOOR_SHUT) <= p < pos(*DOOR_OPEN):
        return "shut"
    return "open"


def door_lit(ch, v):
    """Lit on the verses that act on the door itself."""
    return (ch, v) in (DOOR_MADE, DOOR_SHUT, DOOR_OPEN, (8, 19))


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
        # at the crowd's own scale, so the head-and-shoulders over them is the
        # unit's doing and not a number picked to look right
        for x in (CROWD_X0 + 3 * CROWD_STEP, CROWD_X0 + 8 * CROWD_STEP):
            figure(c, x, GROUND_Y - 6, HL, scale=0.8, kind="nephilim")
        c.text((CROWD_X0 + 5.5 * CROWD_STEP, GROUND_Y - 86), "the Nephilim",
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
    """The flood view's side elevation: hull, three decks, door, roof ridge.

    Whenever the water level has changed the whole hull rides with it: the
    group starts at the previous verse's height and glides to this one's,
    once, then freezes."""
    p = pos(ch, v)
    built = p >= pos(6, 14)
    top = ark_top(ch, v)
    bot = top + ARK_H

    if not built:
        # Nothing. Verses 6:1-13 have not reached the command to make an ark,
        # and an empty outline standing in the sky over the plain reads as a
        # stray box rather than as a thing not yet built — it says nothing the
        # absence of a ship does not say better.
        return

    lift = prev_ark_top(ch, v) - top
    riding = abs(lift) > 0.5
    if riding:
        c.raw([f'<g><animateTransform attributeName="transform" '
               f'type="translate" values="0 {_num(lift)};0 0" '
               f'dur="{_RISE_DUR}" begin="0s" fill="freeze" '
               f'calcMode="spline" keyTimes="0;1" keySplines="{_EASE}"/>'])

    hull = hull_points(ARK_X0, top, ARK_L, ARK_H)
    c.polyline(hull, stroke=SAND, width=2, closed=True, fill=dim(HULL, 235))
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
            ins = hull_inset(dy, top, ARK_L, ARK_H)
            c.line((ARK_X0 + ins + 3, dy), (ARK_X1 - ins - 3, dy),
                   HL if lv_lit else dim(DECK, 220), 2 if lv_lit else 1.5)
        # Set in from the planking at the label's OWN height, not from the
        # ark's squared-off end. The hull draws in through the turn of the
        # bilge, so a fixed offset that clears the side on the third deck
        # sits out through it on the lower one.
        ly = dy + ARK_H / 6
        c.text((ARK_X0 + hull_inset(ly, top, ARK_L, ARK_H) + 12, ly), name,
               11, GOLD if lv_lit else TEXT_DIM, "lm", italic=True)
    # rooms
    for i in range(1, 12):
        x = ARK_X0 + i * (ARK_L / 12)
        c.line((x, top + 2),
               (x, hull_bottom(x, ARK_X0, top, ARK_L, ARK_H) - 2),
               dim(DECK, 150), 1)
    # the door in the side
    dst = door_state(ch, v)
    dlit = door_lit(ch, v)
    dx0, dw = ARK_X0 + ARK_L * DOOR_AT, 26
    dy0, dh = top + ARK_H / 3 + 5, ARK_H / 3 - 10
    draw_door(c, dx0, dy0, dw, dh, dst, dlit)
    if dlit and (ch, v) in DOOR_LABEL:
        c.text((dx0 + dw / 2, top - 14), DOOR_LABEL[(ch, v)], 12, HL, "mb",
               italic=True)

    # everything below the surface, seen through it
    wy = water_y(ch, v)
    if water_level(ch, v) > 0 and top < wy < bot:
        c.polygon(clip_below(hull, wy), fill=dim(FLOOD, 128))
        c.line((ARK_X0 + hull_inset(wy, top, ARK_L, ARK_H), wy),
               (ARK_X1 - hull_inset(wy, top, ARK_L, ARK_H), wy),
               dim(FLOOD_TOP, 210), 2)

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


# Of every sort, two of every sort. The queue at the door is the one place
# in these four chapters where variety IS the subject, so the creature drawn
# is chosen from its place in the line rather than being the same blob each
# time — and the choice is made from x, so a verse redrawn tomorrow has the
# same beasts in the same order as today.

# Two of every sort is the text, but a queue of six different sorts is a
# menagerie and it fights the ark for the eye. Two kinds, walking in pairs.
# Nothing that flies or creeps: at this size a bird on the ground reads as
# debris and a serpent reads as a crack.
_KINDS = (F.ox, F.sheep)


def creature(c, x, y, col, height=17.0):
    """One beast of the queue. Which sort it is comes from where it stands in
    the line — by pairs, so the two of every sort are seen to be two — and it
    is taken from x, so a verse redrawn tomorrow has the same beasts in the
    same order as today."""
    parts = _KINDS[(int(abs(x) / 24) // 2) % len(_KINDS)]()
    x0, x1, y0, y1 = F.bbox((parts, 0))
    s = height / (y1 - y0)
    F.draw(c, parts, x - (x0 + x1) / 2 * s, y + 9 - y0 * s, s, col, BG)


# The schematic figure these replace stood about 27 pixels tall, which is
# enough for a stick and not enough for a drawn body. They stand on their own
# feet, so enlarging them moves nothing else in the scene.

FIGURE_SCALE = 1.6


def figure(c, x, y, col, scale=0.85, kind="man"):
    """`y` is the waist the schematic figure hung from; the drawn one stands
    on its feet, so the feet go where that figure's feet were.

    `kind` is "man", "woman", or "nephilim" — and the Nephilim of 6:4 are a
    build, not a bigger man, which is the whole of what that verse says about
    them."""
    parts = (F.nephilim() if kind == "nephilim" else
             F.woman() if kind == "woman" else F.man())
    # Pixels per unit, NOT a fitted height: fitting each figure to one height
    # makes a giant the size of a man, which is the only thing 6:4 says about
    # him. At this scale a man comes out 31.6*scale*FIGURE_SCALE tall and a
    # Nephilim comes out half again that, because the unit says so.
    s = 31.6 * scale * FIGURE_SCALE / 98.0
    F.draw(c, parts, x, y + 8 * scale, s, col, BG)


def draw_loading(c, ch, v):
    """The queue at the door: the animals by pairs, then the household of
    eight. Both wait west of the hull (x < 190) and route along the ground to
    the gangplank, which climbs the side to the door on the middle storey."""
    if rested(ch, v) or not ground_dry(ch, v):
        return
    key = (ch, v)
    door_x = ARK_X0 + ARK_L * DOOR_AT
    sill_y = ark_top(ch, v) + ARK_H / 3 + ARK_H / 3 - 5
    ramp_y = GROUND_Y + 12
    if key in LOADING:
        n, label = LOADING[key]
        y = GROUND_Y - 14
        # Three pairs, not eight. A drawn beast is twice the width the old
        # blob was, so the queue that used to read as a line reads as a heap
        # at the same spacing — and the verse says two and two, which three
        # pairs say and a crowd does not.
        pairs = min(n, 3)
        for i in range(pairs):
            bx = 52 + i * 46
            creature(c, bx, y, HL)
            creature(c, bx + 20, y + 3, GOLD)
        c.text((52, GROUND_Y + 26), label, 12, HL, "la", italic=True)
        c.polyline([(52 + pairs * 46, y), (188, y), (188, ramp_y),
                    (door_x - 96, ramp_y), (door_x - 2, sill_y)],
                   stroke=GOLD, width=1.5, dash="5,5")
    if key in HOUSEHOLD:
        for i in range(8):
            figure(c, 50 + i * 20, GROUND_Y - 10, HL, scale=0.7)
        c.text((50, GROUND_Y + 26), "eight", 12, HL, "la", italic=True)
        c.polyline([(188, GROUND_Y - 16), (214, GROUND_Y - 16)], stroke=GOLD,
                   width=2, dash="4,5")


def draw_aboard(c, ch, v):
    """7:13-16 recount the boarding, but by then the rain has been falling for
    forty days — so on those verses the household and the pairs are drawn
    where they now are, inside, rather than standing in the rising water."""
    if rested(ch, v) or ground_dry(ch, v):
        return
    if (ch, v) not in HOUSEHOLD | set(LOADING):
        return
    top = ark_top(ch, v)
    deck = top + ARK_H / 3                   # the second storey, above the
    for i in range(8):                       # water climbing the hull's side
        figure(c, ARK_X0 + 84 + i * 26, deck + 22, HL, scale=0.52)
    if (ch, v) in LOADING:
        n, label = LOADING[(ch, v)]
        for i in range(n):
            bx = ARK_X0 + 340 + i * 34
            creature(c, bx, deck + 14, HL)
            creature(c, bx + 11, deck + 17, GOLD)
        c.text((ARK_X0 + 340, top - 10), label, 12, HL, "lb", italic=True)


def bird(c, x, y, col, leaf=False, pose="up", flip=1):
    """The raven and the dove. Drawn in profile: these two are the one case
    in the chapter where a bird has somewhere to be — sent forth, and come
    back again — and a bird seen from below has a spread but no heading."""
    F.draw(c, F.bird(pose=pose, view="profile"), x, y, 0.42, col, BG,
           flip=flip)
    if leaf:
        c.ellipse(x + flip * 15, y + 2, 5, 2.6, fill=GREEN, stroke=GREEN)


def draw_birds(c, ch, v):
    """The raven and the dove, out of the window Noah opened. Every one of
    these verses falls after the grounding, so the window they leave from is
    the rested view's."""
    if ch != 8 or not (7 <= v <= 12):
        return
    wx, wy = rest_window()          # they fly out over the open western sky
    if v == 7:
        path = [(wx, wy), (wx - 78, wy - 30), (wx - 40, wy - 68),
                (wx + 4, wy - 44), (wx - 52, wy - 40)]
        c.polyline(path, stroke=dim(SILVER, 150), width=1.5, dash="4,5")
        bird(c, wx - 52, wy - 40, SILVER)
        c.text((wx - 74, wy - 74), "the raven", 12, HL, "rm", italic=True)
        return
    out = [(wx, wy), (wx - 52, wy - 30), (wx - 108, wy - 40)]
    if v in (8, 9):
        c.polyline(out, stroke=dim(HL, 150), width=1.5, dash="4,5")
        c.polyline([(wx - 108, wy - 36), (wx - 52, wy - 24), (wx, wy + 4)],
                   stroke=dim(HL, 110), width=1.5, dash="2,5")
        bird(c, wx - 46, wy - 26, HL)
        c.text((wx - 120, wy - 44), "the dove", 12, HL, "rm", italic=True)
    elif v in (10, 11):
        c.polyline(out, stroke=dim(HL, 150), width=1.5, dash="4,5")
        bird(c, wx - 62, wy - 32, HL, leaf=(v == 11))
        if v == 11:
            c.text((wx - 120, wy - 44), "the olive leaf", 12, HL, "rm",
                   italic=True)
    else:      # v == 12, she does not return
        far = [(wx, wy), (wx - 58, wy - 34), (wx - 136, wy - 56)]
        c.polyline(far, stroke=dim(HL, 150), width=1.5, dash="4,5")
        bird(c, wx - 136, wy - 56, HL)



# ---------------------------------------------------------------------------
# The rested view (8:4 onward)
#
# A 300-cubit hull balanced on a needle, with people stepping off into thin
# air, was the wrong picture. From the grounding the camera comes round and
# down: Ararat is a whole massif with its summit to the right and a broad rock
# shoulder beneath it, the hull lies three-quarter and tilted along that
# shoulder, and the flank falls away west to the plain. The water table is the
# same device as before — one surface across the frame, dropping verse by
# verse — it just drains down a mountainside now.
# ---------------------------------------------------------------------------

# The ridge, west base to east base. SHOULDER is the long shallow stretch the
# hull came to rest along; the flank steps down sharply off its western end, so
# the ark reads as having stopped somewhere rather than as sliding down a ramp.
SHOULDER = [(452, 234), (560, 228), (680, 220), (776, 212)]
RIDGE = ([(300, 400), (336, 366), (372, 330), (400, 300), (410, 286),
          (432, 262), (444, 240)] + SHOULDER +
         [(806, 180), (842, 150), (880, 132), (918, 176), (952, 244),
          (984, 320), (1000, 372), (1000, 400)])

# The range behind and below it, whose tops are the ones seen at 8:5.
FAR_RIDGE = [(24, 400), (72, 328), (120, 276), (168, 246), (214, 294),
             (252, 256), (290, 300), (332, 250), (374, 308), (416, 400)]

R_X0, R_L, R_H = 452.0, 331.0, 33.0          # the hull, at 0.46 of the elevation
R_BOT = 230.0                                # bedded into the shoulder's face
R_TOP = R_BOT - R_H
R_CX, R_CY = R_X0 + R_L / 2, R_BOT
R_TILT = -4.0                                # settled along the shoulder's fall
DECK_DX, DECK_DY = 21.0, -14.0               # the deck, seen from below
LEDGE = 18                                   # how deep the shoulder's face is

SUMMIT = (880, 132)

# Off the plank, west along the shoulder, down the step, then the flank.
TRAIL = [(496, 250), (460, 252), (432, 274), (410, 296), (378, 324),
         (344, 352), (310, 376), (280, 392)]

WINDOW_AT = 0.07             # forward and high, well clear of the door


def rot(p):
    """Into the tilted hull's place on the shoulder."""
    a = math.radians(R_TILT)
    dx, dy = p[0] - R_CX, p[1] - R_CY
    return (R_CX + dx * math.cos(a) - dy * math.sin(a),
            R_CY + dx * math.sin(a) + dy * math.cos(a))


def rest_window():
    """The window's outer edge, in final coordinates — where the birds go
    out from."""
    return rot((R_X0 + R_L * WINDOW_AT, R_TOP + 9))


# Water in this view is set as a height on the mountain rather than as a
# fraction of the plain: 8:4 is the surface the hull grounds against, 8:5 is
# the line the lesser tops break through, 8:14 is gone.
REST_WATER = [((8, 4), 216), ((8, 5), 262), ((8, 6), 292), ((8, 8), 310),
              ((8, 10), 328), ((8, 12), 346), ((8, 13), 380), ((8, 14), 433)]


def rest_water_y(ch, v):
    p = pos(ch, v)
    y = REST_WATER[0][1]
    for (bc, bv), value in REST_WATER:
        if pos(bc, bv) <= p:
            y = value
    return y


def draw_massif(c, ch, v):
    c.polygon(FAR_RIDGE, fill=dim(GRAY, 58))
    c.polygon(RIDGE, fill=dim(GRAY, 150), stroke=SAND_DIM, width=1.5)
    # a lit band along the shoulder, so it reads as a ledge the hull is sitting
    # on rather than as the edge of a flat grey field
    c.polygon(SHOULDER + [(x, y + LEDGE) for x, y in reversed(SHOULDER)],
              fill=dim(SAND_DIM, 62))
    # two spurs off the summit, to give the face some form
    for spur in ([(880, 136), (846, 232), (826, 330), (836, 400)],
                 [(880, 136), (924, 226), (946, 320)]):
        c.polyline(spur, stroke=dim(SAND_DIM, 46), width=1.5)
    c.rect(SCENE[0], GROUND_Y, SCENE[2] - SCENE[0], SCENE[3] - GROUND_Y,
           fill=dim(BROWN, 130))
    lit = (ch == 8 and v in (4, 5))
    c.text((SUMMIT[0] - 22, SUMMIT[1] + 34), "Ararat", 14,
           HL if lit else SAND, "rm", bold=lit, italic=not lit)


def draw_rest_water(c, ch, v):
    wy = rest_water_y(ch, v)
    prev_y = wy if (ch, v) == REST_AT else rest_water_y(*prev_verse(ch, v))
    if wy >= SCENE[3] and prev_y >= SCENE[3]:
        return
    if abs(prev_y - wy) > 0.5:
        _rise_rect(c, SCENE[0], SCENE[2] - SCENE[0], prev_y, wy,
                   dim(FLOOD, 205))
        _rise_line(c, SCENE[0], SCENE[2], prev_y, wy, FLOOD_TOP, 2.5)
    else:
        c.rect(SCENE[0], wy, SCENE[2] - SCENE[0], SCENE[3] - wy,
               fill=dim(FLOOD, 205))
        c.line((SCENE[0], wy), (SCENE[2], wy), FLOOD_TOP, 2.5)


def draw_rest_ark(c, ch, v):
    """The hull on the shoulder: the long side, a sliver of deck above it to
    give the angle, and the door low in the side."""
    x1 = R_X0 + R_L
    deck = [rot((R_X0, R_TOP)), rot((x1, R_TOP)),
            rot((x1 + DECK_DX, R_TOP + DECK_DY)),
            rot((R_X0 + DECK_DX, R_TOP + DECK_DY))]
    c.polyline(deck, stroke=SAND, width=2, closed=True, fill=dim(DECK, 225))
    c.polyline([rot(p) for p in hull_points(R_X0, R_TOP, R_L, R_H)],
               stroke=SAND, width=2, closed=True, fill=dim(HULL, 240))
    for i in (1, 2):                     # the three levels
        y = R_TOP + i * (R_H / 3)
        ins = hull_inset(y, R_TOP, R_L, R_H) + 3
        c.line(rot((R_X0 + ins, y)), rot((x1 - ins, y)), dim(DECK, 210), 1.2)
    for i in range(1, 8):                # the rooms
        x = R_X0 + i * (R_L / 8)
        c.line(rot((x, R_TOP + 2)),
               rot((x, hull_bottom(x, R_X0, R_TOP, R_L, R_H) - 2)),
               dim(DECK, 140), 1)

    dw, dh = 15.0, 10.0
    dx0, dy0 = R_X0 + R_L * DOOR_AT, R_TOP + R_H / 3 + 1
    draw_door(c, dx0, dy0, dw, dh, door_state(ch, v), door_lit(ch, v), rot)
    if door_lit(ch, v) and (ch, v) in DOOR_LABEL:
        c.text(rot((dx0 + dw / 2, R_TOP + DECK_DY - 9)), DOOR_LABEL[(ch, v)],
               12, HL, "mb", italic=True)

    if pos(ch, v) >= pos(8, 6):          # the window Noah opens
        wx, wy = R_X0 + R_L * WINDOW_AT, R_TOP + 4
        c.polyline([rot((wx, wy)), rot((wx + 14, wy)), rot((wx + 14, wy + 10)),
                    rot((wx, wy + 10))], stroke=GOLD, width=1.8, closed=True,
                   fill=BG)
        if ch == 8 and v == 6:
            lx, ly = rot((wx - 4, wy + 5))
            c.text((lx, ly), "the window", 12, HL, "rm", italic=True)


def _along(pts, t):
    """The point a fraction `t` of the way down a polyline."""
    segs = [(a, b, math.hypot(b[0] - a[0], b[1] - a[1]))
            for a, b in zip(pts, pts[1:])]
    d = t * sum(s[2] for s in segs)
    for a, b, ln in segs:
        if d <= ln:
            k = d / ln if ln else 0.0
            return (a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k)
        d -= ln
    return pts[-1]


def draw_disembark(c, ch, v):
    """8:18-19 — the plank down onto the shoulder, and the household and the
    beasts strung out along the path down the flank to the plain."""
    if ch != 8 or v < 18:
        return
    sill = rot((R_X0 + R_L * DOOR_AT - 1, R_TOP + R_H / 3 + 11))
    foot = TRAIL[0]
    c.polygon([sill, (sill[0] + 5, sill[1] + 7), (foot[0] + 5, foot[1] + 7),
               (foot[0], foot[1])], fill=dim(DECK, 240), stroke=SAND,
              width=1.2)
    c.polyline(TRAIL, stroke=dim(GOLD, 160), width=1.5, dash="5,5")
    for i in range(8):
        x, y = _along(TRAIL, 0.08 + i * 0.115)
        figure(c, x, y, HL, scale=0.5)
    if v <= 19:
        end = TRAIL[-1]
        c.text((end[0] - 10, end[1] + 10), "eight", 12, HL, "rm", italic=True)
    if v == 19:
        for i in range(6):
            x, y = _along(TRAIL, 0.15 + i * 0.14)
            creature(c, x + 17, y + 4, GOLD)


def draw_altar(c, ch, v):
    """Noah's altar (8:20-22) on the dry ground."""
    if pos(ch, v) < pos(8, 20):
        return
    lit = (ch == 8 and 20 <= v <= 22)
    x, y = 170, GROUND_Y
    # The unhewn heap, not a hewn block: this is the altar a man raises out of
    # what is lying about him, which is what Noah does the moment he lands.
    parts = F.altar("stone", fire=True)
    y0, y1 = F.bbox((parts, 0))[2:]
    sheet = dict(F.palette(HL if lit else SAND_DIM, BG))
    sheet["fire"] = (GOLD if lit else dim(GOLD, 150), GOLD, 1.2)
    F.draw(c, parts, x, y, 46.0 / (y1 - y0), HL, BG, style=sheet)
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
    if rested(ch, v):
        draw_massif(c, ch, v)
        # the hull goes under the surface, so at 8:4 it is still awash
        draw_rest_ark(c, ch, v)
        draw_rest_water(c, ch, v)
        draw_disembark(c, ch, v)
    else:
        draw_mountains(c, ch, v)
        draw_water(c, ch, v)
        draw_ark(c, ch, v)
        draw_before_flood(c, ch, v)
        draw_dimensions(c, ch, v)
        draw_loading(c, ch, v)
        draw_aboard(c, ch, v)
        draw_end_view(c, ch, v)
    draw_birds(c, ch, v)
    draw_altar(c, ch, v)
    draw_sons(c, ch, v)
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
