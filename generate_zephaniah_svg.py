"""Render Zephaniah (3 chapters, 53 verses) as per-verse vector SVGs.

Design (see SHORT_BOOKS_IDEAS.md): three chapters, three geometries.

  ch1  The created world drawn as three registers — sky, land, sea — and then
       swept, in the order 1:3 gives (man, animal, birds, fish). That order is
       the filling of Genesis 1 run backwards, so the chapter opens by undoing
       the chapter the canon opens with; the registers carry it without a word
       of commentary. Then the hand stretched out over Jerusalem, the rooftop
       worshippers who swear two ways at once, the sacrifice with its bidden
       guests, a plan of the city searched quarter by quarter with a lamp, and
       the nine words of 1:15 as a bar that goes to black one word at a time.
  ch2  A compass laid over Judah. The oracles go round the points in the
       text's own order — west (the four Philistine cities), east (Moab and
       Ammon), south (Cush), north (Nineveh) — so a small compass in the
       corner is the whole progress indicator. Nineveh's ruin is drawn as a
       building labelled by the creatures that now occupy its named parts:
       capitals, windows, thresholds, cedar beams.
  ch3  One centre point, three occupants. The four offices of 3:3-4 fail
       around it while Yahweh, within her, brings justice to light every
       morning without fail (3:5); the proud are taken out from among her
       (3:11) and the afflicted and poor left in their place (3:12); and at
       the end the same centre is occupied by the King who rejoices over her
       with singing (3:17). The position never moves; who stands in it does.

Threads across the chapters, so the book reads as one set: the fire of
jealousy at 1:18 and 3:8 is the same flame; Cush is struck at 2:12 and brings
an offering at 3:10 along the same line; the animals that lie down in ruined
Nineveh (2:14) and the remnant that lies down with no one to make it afraid
(3:13) share a posture; and the morning that never fails (3:5) is set against
the morning they rose early to corrupt (3:7).

WEB is the only text (passages.TRANSLATION), so the divine name is Yahweh
and the labels follow WEB wording.

Text budget: names, numbers and labelled parts, plus short engraved phrases
(2-7 words, WEB wording) at hinge verses only. Nothing counts the verses.
What changes each verse is the drawing.

Run inside the project venv:
    .venv\\Scripts\\python.exe generate_zephaniah_svg.py
"""

import math
import os

import svg_figures as F
from svg_surface import SvgCanvas
# The stick figure, beast, bird and fish that used to come from svg_vocab are
# replaced below by the drawn vocabulary, with the same signatures. svg_vocab
# itself is left alone: 2 Peter still draws from it, and changing it here
# would restyle that book without anyone having looked at it. Its generic
# quadruped is still imported, for the one creature svg_figures has no answer
# for — see the porcupine of 2:14.
from svg_vocab import (dim, mix, text_w, reading_position, arrow, cross,
                       struck, tick_row, hatch, flame,
                       beast as generic_beast)
from passages import verse_numbers
from generate_tabernacle import (W, H, BG, PANEL, SAND, SAND_DIM, TEXT,
                                 TEXT_DIM, HL, GOLD, RED, BROWN, GRAY,
                                 SILVER, out_path)

BOOK = "Zephaniah"
SLUG = BOOK

# Colours this book needs that the tabernacle palette has no name for.
SEA = (96, 122, 152)            # the fish of the sea, the sea coast
SKY = (118, 132, 164)           # the birds of the sky, the army of the sky
NIGHT = (20, 20, 30)            # the day of clouds and blackness
FIRE = (216, 124, 58)           # the fire of his jealousy, 1:18 and 3:8
ASH = (110, 106, 100)           # desolation
GREEN = (122, 146, 92)          # pasture on the sea coast, 2:6
WINE = (138, 72, 78)            # the dregs of 1:12, the wine of 1:13

CH_LEN = {1: 18, 2: 15, 3: 20}
P, since = reading_position(CH_LEN)


def header(c, ch, v):
    c.text((28, 24), f"Zephaniah {ch}", 23, TEXT, "la", bold=True)
    c.text((28, 54), f"v{v}", 13, dim(TEXT_DIM, 0.85), "la", italic=True)


def phrase(c, xy, s, size=21, col=None, first=False):
    """A hinge-verse phrase: caps, bold, ringed once on the verse it lands.
    The ring is measured off the text, so it never crops the ends."""
    col = col or HL
    c.text(xy, s, size, col, "mm", bold=True)
    if first:
        w = text_w(s, size, bold=True) + size * 1.30
        h = size * 1.80
        c.pulse_rect(xy[0] - w / 2, xy[1] - h / 2, w, h,
                     dim(col, 0.7), width=1.6, first=True, rx=h / 2)


# ---------------------------------------------------------------------------
# The living world, drawn
# ---------------------------------------------------------------------------
#
# 1:3 sweeps the creation away in the order Genesis 1 filled it — man, animal,
# birds, fish, backwards — and that is the strongest idea in the book. It only
# lands if the four creatures being swept are the SAME four Genesis 1 puts
# there, so they come from svg_figures, as Genesis 1's do.
#
# Every signature below is the stick mark's, unchanged, so no scene in this
# file moved. What each takes is still an EXTENT in pixels — a man's height,
# a beast's length, a wingspan — because that is what the layouts were built
# on; where true relative size matters (the sweep), the caller passes one
# shared scale instead. `kind` is always passed at the call site and never
# inferred from a nearby label.

MAN_UNITS = F.bbox((F.man(), 0))[3] - F.bbox((F.man(), 0))[2]

_KINDS = {"sheep": F.sheep, "ox": F.ox, "lion": F.lion, "wolf": F.wolf,
          "donkey": F.donkey}
_paint_cache = {}


def _fade(col, a):
    if col is None or a >= 1.0:
        return col
    had = (col[3] / 255.0) if len(col) > 3 else 1.0
    return (col[0], col[1], col[2], int(255 * had * a))


def paint(col, width):
    """The vocabulary's paint table in this scene's colour and opacity. The
    book dims whole creatures to say they are gone (1:3) or not yet come, and
    a table built from the RGB alone would bring them all back to full."""
    key = (tuple(col), width)
    if key not in _paint_cache:
        a = (col[3] / 255.0) if len(col) > 3 else 1.0
        k = width / 1.9
        _paint_cache[key] = {
            m: (_fade(f, a), _fade(s, a), w * k)
            for m, (f, s, w) in F.palette(tuple(col[:3]), BG).items()}
    return _paint_cache[key]


def _put(c, parts, x, y, s, col, width, flip=1):
    F.draw(c, parts, x, y, s, col, BG, flip=flip, style=paint(col, width))


def _fit(parts, w=None, h=None):
    x0, x1, y0, y1 = F.bbox((parts, 0))
    return w / (x1 - x0) if w is not None else h / (y1 - y0)


def figure(c, x, gy, h, col, width=2, arms="down", legs="stand", lean=0.0,
           s=None, kind="man"):
    """A person standing on `gy`, `h` tall. `lean` survives as a sideways
    shift of the whole body, which is what it always drew."""
    parts = {"woman": F.woman, "child": F.child}.get(kind, F.man)(
        pose="walk" if legs == "walk" else
             ("kneel" if legs == "kneel" else "stand"), arms=arms)
    _put(c, parts, x + lean * h, gy, s or h / MAN_UNITS, col, width)


def beast(c, x, gy, ln, col, width=1.8, head_low=False, tail=True,
          kind="sheep", s=None):
    """A four-footed animal standing on `gy`, `ln` long. `head_low` and
    `tail` are accepted and ignored: the drawn creatures carry their own head
    and their own tail, and a sheep that could put its head down would be a
    second sheep rather than a flag on this one."""
    parts = _KINDS[kind]()
    _put(c, parts, x, gy, s or _fit(parts, w=ln), col, width)


def lying_beast(c, x, gy, ln, col, width=1.8, kind="sheep", s=None):
    """The couched posture the book gives both to the animals in ruined
    Nineveh (2:14) and to the remnant no one makes afraid (3:13) — one
    posture, so the two verses rhyme."""
    parts = F.sheep(lying=True) if kind == "sheep" else _KINDS[kind]()
    _put(c, parts, x, gy, s or _fit(parts, w=ln), col, width)


def bird(c, x, y, w, col, width=1.8, s=None, flip=1):
    """On the wing, facing right, `w` across. (x, y) is its centreline, as it
    was for the mark this replaces."""
    parts = F.bird(pose="glide", view="profile")
    _put(c, parts, x, y, s or _fit(parts, w=w), col, width, flip=flip)


def fish(c, x, y, ln, col, width=1.6, s=None, flip=1):
    """Facing right, `ln` long, on its centreline."""
    parts = F.fish()
    _put(c, parts, x, y, s or _fit(parts, w=ln), col, width, flip=flip)


# ---------------------------------------------------------------------------
# Shared marks
# ---------------------------------------------------------------------------

def sunrise(c, x, y, r, col, width=1.8, rays=True):
    """A morning: half a disc on a line. Used for the justice brought to light
    every morning (3:5) and for the morning they rose early to spoil (3:7)."""
    c.path(f"M{x - r},{y} A{r},{r} 0 0 1 {x + r},{y}", stroke=col, width=width)
    c.line((x - r * 1.5, y), (x + r * 1.5, y), col, width)
    if rays:
        for k in range(5):
            a = math.pi + k * math.pi / 4
            c.line((x + r * 1.25 * math.cos(a), y + r * 1.25 * math.sin(a)),
                   (x + r * 1.65 * math.cos(a), y + r * 1.65 * math.sin(a)),
                   col, width * 0.8)


def house(c, x, gy, w, h, col, width=1.8, fill=None):
    """A house in elevation. Signature unchanged — `w` is still the width the
    street was laid out on; `h` and `fill` are the elevation's own business
    now and are accepted for the call sites that still pass them."""
    hs = F.house()
    _put(c, hs, x, gy, _fit(hs, w=w + 12), col, width)


def jar(c, x, gy, w, h, col, dregs=0.0, width=1.8):
    """A wine jar; `dregs` fills the settled layer at the bottom (1:12) —
    the men settled on their lees, who say Yahweh will do neither good nor
    evil. The dregs are this book's own mark and stay hand-drawn: the
    vocabulary draws the vessel, not what has gone to the bottom of it."""
    js = F.jar()
    _put(c, js, x, gy, _fit(js, h=h), col, width)
    if dregs > 0:
        jw = (F.bbox((js, 0))[1] - F.bbox((js, 0))[0]) * _fit(js, h=h)
        dh = h * dregs * 0.42
        c.path(f"M{x - jw * 0.34},{gy - dh} q{jw * 0.34},{-jw * 0.07} "
               f"{jw * 0.68},0 l0,{dh} l{-jw * 0.68},0 z",
               fill=dim(WINE, 0.85))


def altar(c, x, gy, w, h, col, width=2.0):
    """The horned altar of the sacrifice Yahweh has prepared (1:7)."""
    al = F.altar("horned")
    _put(c, al, x, gy, _fit(al, w=w + 16), col, width)


def compass(c, active, seen):
    """The chapter-2 progress indicator: Judah at the centre, the four points
    round it. `active` is lit, everything in `seen` is marked done."""
    cx, cy = 912, 470
    c.rect(cx - 26, cy - 15, 52, 30, fill=dim(PANEL, 0.95),
           stroke=dim(SAND, 0.9), width=1.6, rx=3)
    c.text((cx, cy), "JUDAH", 10, dim(TEXT, 0.92), "mm")
    pts = {"N": (cx, cy - 50), "S": (cx, cy + 50),
           "W": (cx - 66, cy), "E": (cx + 66, cy)}
    for key, (px, py) in pts.items():
        on = key == active
        done = key in seen
        col = GOLD if on else (dim(SAND, 0.85) if done else dim(SAND_DIM, 0.5))
        c.rect(px - 17, py - 13, 34, 26, fill=dim(GOLD, 0.22) if on else None,
               stroke=col, width=1.9 if on else 1.4, rx=3)
        c.text((px, py), key, 12, HL if on else
               (dim(TEXT, 0.9) if done else dim(TEXT_DIM, 0.6)), "mm",
               bold=on)
        c.line((cx + (px - cx) * 0.34, cy + (py - cy) * 0.34),
               (cx + (px - cx) * 0.68, cy + (py - cy) * 0.68), col, 1.4)


# ---------------------------------------------------------------------------
# Chapter 1
# ---------------------------------------------------------------------------

def draw_ch1(c, v, pos):
    if v == 1:
        _ch1_line(c, v, pos)
    elif v <= 3:
        _ch1_sweep(c, v, pos)
    elif v == 4:
        _ch1_hand(c, v, pos)
    elif v <= 6:
        _ch1_rooftops(c, v, pos)
    elif v <= 9:
        _ch1_sacrifice(c, v, pos)
    elif v <= 13:
        _ch1_search(c, v, pos)
    elif v <= 16:
        _ch1_wrath(c, v, pos)
    else:
        _ch1_blind(c, v, pos)


NAMES = ["ZEPHANIAH", "CUSHI", "GEDALIAH", "AMARIAH", "HEZEKIAH"]


def _ch1_line(c, v, pos):
    phrase(c, (512, 152), "YAHWEH'S WORD CAME TO ZEPHANIAH", 21, HL,
           first=True)
    y = 300
    xs = [166, 336, 506, 676, 846]
    for i, (x, name) in enumerate(zip(xs, NAMES)):
        if i:
            c.line((xs[i - 1] + 12, y), (x - 12, y), dim(SAND, 0.9), 1.8)
            c.text(((xs[i - 1] + x) / 2, y - 18), "son of", 11,
                   dim(TEXT_DIM, 0.95), "mm", italic=True)
        c.circle(x, y, 12, fill=dim(PANEL, 0.95),
                 stroke=GOLD if i == 0 else dim(SAND, 0.95), width=2)
        c.text((x, y + 34), name, 13.5, HL if i == 0 else dim(TEXT, 0.92),
               "mm", bold=i == 0)
    c.pulse_ellipse(xs[0], y, 24, 24, dim(HL, 0.9), width=2, first=True)

    # the reign the word came in
    c.line((xs[0], y + 52), (xs[0], y + 96), dim(SAND_DIM, 0.9), 1.4,
           dash="5,5")
    c.rect(72, y + 96, 300, 34, fill=dim(PANEL, 0.95),
           stroke=dim(SAND, 0.9), width=1.6, rx=4)
    c.text((222, y + 113), "JOSIAH, KING OF JUDAH", 13, dim(TEXT, 0.92), "mm")
    c.text((222, y + 148), "the son of Amon", 11.5, dim(TEXT_DIM, 0.95),
           "mm", italic=True)


# The created world, and the order 1:3 sweeps it away.
SWEEP = [("MAN", 1), ("ANIMAL", 2), ("THE BIRDS OF THE SKY", 3),
         ("THE FISH OF THE SEA", 4)]
BIRDS = ((176, 262), (300, 230), (420, 268), (536, 238))
FISHES = ((186, 450), (318, 472), (448, 446), (576, 470))


def _ch1_sweep(c, v, pos):
    sky0, gnd, sea1 = 196, 402, 502
    swept, sw_first = since(pos, 1, 3)

    # the three registers
    c.rect(84, sky0, 576, gnd - sky0, fill=dim(SKY, 0.05))
    c.rect(84, gnd, 576, sea1 - gnd, fill=dim(SEA, 0.16))
    c.line((84, gnd), (660, gnd), dim(BROWN, 0.95), 2.4)
    c.line((84, sea1), (660, sea1), dim(SEA, 0.7), 1.6)
    c.text((100, sky0 + 18), "THE SKY", 12, dim(TEXT_DIM, 0.95), "lm",
           italic=True)
    c.text((100, gnd - 16), "THE SURFACE OF THE EARTH", 12,
           dim(TEXT_DIM, 0.95), "lm", italic=True)
    c.text((100, sea1 - 18), "THE SEA", 12, dim(TEXT_DIM, 0.95), "lm",
           italic=True)

    live = dim(TEXT, 0.92)
    gone = dim(GRAY, 0.45)

    # One shared scale for the three that stand on the SAME ground line, so
    # the man is taller than his sheep and shorter than his ox — a comparison
    # the eye actually makes, because they share a line to make it against.
    # The birds and the fish keep their own extents: they are in registers of
    # their own, nothing in the frame invites their size to be compared with
    # the land's, and at true scale against a 62-pixel man a fish comes out
    # at nineteen pixels and stops being a fish.
    # 304, not 268: the register's own label runs to x=274, and the stick
    # figure that used to stand there was thin enough for the words to pass
    # through it.
    sw = 62 / MAN_UNITS
    figure(c, 304, gnd, 62, gone if swept else GOLD, 2.1)
    beast(c, 400, gnd, 78, gone if swept else live, 1.8, kind="ox", s=sw)
    beast(c, 524, gnd, 62, gone if swept else live, 1.7, kind="sheep", s=sw)
    # birds in the sky
    for bx, by in BIRDS:
        bird(c, bx, by, 60, gone if swept else live, 1.8)
    # fish in the sea
    for fx, fy in FISHES:
        fish(c, fx, fy, 68, gone if swept else live, 1.7)

    if not swept:
        arrow(c, (900, 160), (170, 160), dim(HL, 0.9), 2.6, 12)
        c.text((536, 138), "SWEEP AWAY EVERYTHING", 15, HL, "mm",
               bold=v == 2)
        if since(pos, 1, 2)[1]:
            c.pulse_rect(84, sky0 - 8, 576, sea1 - sky0 + 16, dim(HL, 0.85),
                         width=2, first=True)
        return

    # 1:3 — struck in the order the verse names them
    # every creature struck, not one specimen standing for the rest;
    # the numbered list beside it carries the order, so the marks can
    # stay small enough not to scribble over each other
    for mx, my, mr in ((304, gnd - 34, 17), (400, gnd - 36, 18),
                       (524, gnd - 30, 16)):
        cross(c, mx, my, mr, dim(RED, 0.85), 2.4)
    for bx, by in BIRDS:
        cross(c, bx, by - 5, 13, dim(RED, 0.85), 2.1)
    for fx, fy in FISHES:
        cross(c, fx, fy, 15, dim(RED, 0.85), 2.1)
    order_x = 700
    c.text((order_x, 176), "SWEPT AWAY, IN ORDER", 12, dim(TEXT_DIM, 0.95),
           "lm", italic=True)
    for i, (label, n) in enumerate(SWEEP):
        yy = 202 + i * 26
        c.circle(order_x + 10, yy, 10, fill=dim(RED, 0.30),
                 stroke=dim(RED, 0.9), width=1.5)
        c.text((order_x + 10, yy), str(n), 11, HL, "mm", bold=True)
        c.text((order_x + 28, yy), label, 12.5, dim(TEXT, 0.92), "lm")
    c.text((372, 542), "AND THE HEAPS OF RUBBLE WITH THE WICKED", 13,
           dim(TEXT_DIM, 0.95), "mm", italic=True)
    phrase(c, (400, 132), "CUT OFF MAN FROM THE SURFACE", 20, dim(RED, 1.0),
           first=sw_first)


def _ch1_hand(c, v, pos):
    # the hand stretched out
    hx, hy = 330, 150
    c.rect(hx - 34, hy, 68, 92, fill=dim(PANEL, 0.9), stroke=GOLD, width=2.2,
           rx=14)
    for i, dx in enumerate((-24, -8, 8, 24)):
        c.rect(hx + dx - 6, hy + 84, 12, 46 - abs(dx) * 0.5,
               stroke=GOLD, width=1.9, rx=6)
    c.rect(hx + 34, hy + 52, 34, 13, stroke=GOLD, width=1.9, rx=6)
    c.text((hx, hy - 24), "MY HAND", 15, HL, "mm", bold=True)
    c.pulse_rect(hx - 44, hy - 10, 128, 160, dim(HL, 0.9), width=2,
                 first=True, rx=18)
    arrow(c, (hx, hy + 140), (hx, hy + 196), dim(GOLD, 0.85), 2.2, 10)

    # what it reaches over
    gy = 470
    c.line((110, gy), (952, gy), dim(SAND_DIM, 0.85), 1.6)
    for i, (bx, bw, bh) in enumerate(((190, 60, 74), (272, 44, 52),
                                      (346, 54, 90), (426, 40, 60))):
        c.rect(bx - bw / 2, gy - bh, bw, bh, fill=dim(PANEL, 0.85),
               stroke=dim(SAND, 0.9), width=1.6)
    c.text((300, gy + 26), "JUDAH — AND ALL JERUSALEM", 13,
           dim(TEXT, 0.92), "mm")

    # the remnant of Baal, and the priests
    px = 630
    c.rect(px - 16, gy - 108, 32, 108, fill=dim(PANEL, 0.9),
           stroke=dim(SAND, 0.9), width=1.8)
    c.circle(px, gy - 126, 20, fill=dim(PANEL, 0.9), stroke=dim(SAND, 0.9),
             width=1.8)
    cross(c, px, gy - 70, 30, dim(RED, 0.9), 2.6)
    c.text((px, gy + 26), "THE REMNANT OF BAAL", 13, dim(RED, 0.95), "mm",
           bold=True)
    for i, fx in enumerate((790, 840, 890)):
        figure(c, fx, gy, 56, dim(GRAY, 0.9), 1.9)
    c.line((762, gy - 34), (918, gy - 34), dim(RED, 0.9), 2.6)
    c.text((840, gy + 26), "THE IDOLATROUS", 12.5, dim(RED, 0.95), "mm",
           bold=True)
    c.text((840, gy + 44), "AND PAGAN PRIESTS", 12.5, dim(RED, 0.95), "mm",
           bold=True)


def _ch1_rooftops(c, v, pos):
    gy = 430
    roof_on, roof_first = since(pos, 1, 5)
    # the army of the sky
    for k, (sx, sy) in enumerate(((190, 130), (300, 168), (420, 122),
                                  (540, 160), (660, 132), (780, 170),
                                  (880, 140))):
        c.circle(sx, sy, 2.6, fill=dim(SILVER, 0.85))
    c.text((512, 96), "THE ARMY OF THE SKY", 14,
           HL if v == 5 else dim(TEXT, 0.92), "mm", bold=v == 5)

    # the housetops
    tops = ((210, 120, 96), (350, 110, 132), (480, 104, 108))
    for tx, tw, th in tops:
        c.rect(tx - tw / 2, gy - th, tw, th, fill=dim(PANEL, 0.88),
               stroke=dim(SAND, 0.9), width=1.7)
        c.line((tx - tw / 2 - 8, gy - th), (tx + tw / 2 + 8, gy - th),
               dim(SAND, 0.95), 2.2)
        if roof_on:
            figure(c, tx, gy - th, 44, GOLD, 1.9, arms="up")
    c.line((110, gy), (952, gy), dim(SAND_DIM, 0.85), 1.6)
    if roof_on:
        c.text((350, gy + 26), "ON THE HOUSETOPS", 13,
               HL if v == 5 else dim(TEXT, 0.92), "mm", bold=v == 5)
        if roof_first:
            c.pulse_rect(140, 108, 420, 226, dim(HL, 0.88), width=2,
                         first=True, rx=10)

        # sworn two ways at once
        sx0 = 720
        figure(c, sx0, gy, 66, dim(TEXT, 0.95), 2.1, arms="open")
        arrow(c, (sx0 - 26, gy - 76), (sx0 - 108, gy - 148),
              dim(GOLD, 0.9), 2.0, 9)
        c.text((sx0 - 128, gy - 164), "YAHWEH", 13.5, dim(TEXT, 0.95), "mm")
        arrow(c, (sx0 + 26, gy - 76), (sx0 + 108, gy - 148),
              dim(RED, 0.9), 2.0, 9)
        c.text((sx0 + 132, gy - 164), "MALCAM", 13.5, dim(RED, 0.95), "mm")
        c.text((sx0, gy + 26), "AND ALSO SWEAR BY MALCAM", 12.5,
               dim(RED, 0.95) if v == 5 else dim(TEXT_DIM, 0.95), "mm",
               bold=v == 5)

    # v6 — two ways of not seeking
    back_on, back_first = since(pos, 1, 6)
    if back_on:
        c.line((110, 540), (952, 540), dim(SAND_DIM, 0.6), 1.3)
        for i in range(3):
            figure(c, 268 - i * 46, 528, 44, dim(GRAY, 0.95), 1.8,
                   legs="walk")
        arrow(c, (300, 500), (176, 500), dim(RED, 0.85), 1.9, 8, dash="6,6")
        c.text((234, 566), "TURNED BACK", 12.5, dim(RED, 0.95), "mm",
               bold=v == 6)
        for i in range(3):
            figure(c, 640 + i * 46, 528, 44, dim(GRAY, 0.95), 1.8)
        c.text((686, 566), "NEVER SOUGHT HIM", 12.5, dim(RED, 0.95), "mm",
               bold=v == 6)
        if back_first:
            c.pulse_rect(140, 476, 700, 74, dim(RED, 0.85), width=1.8,
                         first=True, rx=12)


def _ch1_sacrifice(c, v, pos):
    gy = 400
    c.line((100, gy), (620, gy), dim(SAND_DIM, 0.85), 1.6)
    altar(c, 240, gy, 118, 84, dim(SAND, 0.95))
    c.text((240, gy + 28), "YAHWEH HAS PREPARED", 12.5, dim(TEXT, 0.92),
           "mm")
    c.text((240, gy + 46), "A SACRIFICE", 12.5, dim(TEXT, 0.92), "mm")
    if v == 7:
        phrase(c, (512, 112), "BE SILENT AT HIS PRESENCE", 21, HL,
               first=True)
        for r in (26, 40, 54):
            c.circle(240, gy - 46, r, stroke=dim(GOLD, 0.20), width=1.4)

    # the guests, consecrated then punished
    gx = 470
    guests = [("THE PRINCES", 0), ("THE KING'S SONS", 1),
              ("FOREIGN CLOTHING", 2)]
    g_on, g_first = since(pos, 1, 7)
    p_on, p_first = since(pos, 1, 8)
    if g_on:
        for label, i in guests:
            fx = gx + i * 140
            figure(c, fx, gy, 66, dim(RED, 0.95) if p_on else GOLD, 2.0)
            if p_on:
                cross(c, fx, gy - 40, 20, dim(RED, 0.9), 2.4)
            c.text((fx, gy + 28), label, 12,
                   dim(RED, 0.95) if p_on else dim(TEXT, 0.92), "mm",
                   bold=p_on and v == 8)
        c.text((gx + 140, 172), "HIS CONSECRATED GUESTS", 13.5,
               HL if v == 7 else dim(TEXT, 0.92), "mm", bold=v == 7)
        if g_first:
            c.pulse_rect(gx - 66, gy - 96, 424, 120, dim(HL, 0.88),
                         width=1.9, first=True, rx=10)
        if p_first:
            c.pulse_rect(gx - 66, gy - 96, 424, 120, dim(RED, 0.88),
                         width=1.9, first=True, rx=10)

    # v9 — leaping over the threshold, and what comes in behind
    th_on, th_first = since(pos, 1, 9)
    if th_on:
        tx, ty = 430, 536
        c.line((330, ty), (700, ty), dim(SAND_DIM, 0.85), 1.5)
        c.rect(tx - 60, ty - 14, 120, 14, fill=dim(BROWN, 0.55),
               stroke=dim(SAND, 0.9), width=1.8)
        c.text((tx, ty + 22), "THE THRESHOLD", 12, dim(TEXT, 0.92), "mm")
        c.path(f"M{tx - 92},{ty - 16} Q{tx},{ty - 104} {tx + 92},{ty - 16}",
               stroke=dim(RED, 0.85), width=1.9)
        figure(c, tx + 92, ty - 16, 46, dim(RED, 0.95), 1.9, legs="walk")
        c.text((790, ty - 74), "VIOLENCE", 13, dim(RED, 0.95), "mm",
               bold=v == 9)
        c.text((790, ty - 50), "DECEIT", 13, dim(RED, 0.95), "mm",
               bold=v == 9)
        arrow(c, (734, ty - 62), (652, ty - 36), dim(RED, 0.9), 2.0, 8)
        c.text((790, ty + 4), "into their master's house", 11.5,
               dim(TEXT_DIM, 0.95), "mm", italic=True)
        if th_first:
            c.pulse_ellipse(tx, ty - 42, 104, 50, dim(RED, 0.85), width=1.9,
                            first=True)


QUARTERS = [("THE FISH GATE", 244, 268, 10), ("THE SECOND QUARTER", 452, 224, 10),
            ("THE HILLS", 664, 196, 10), ("MAKTESH", 430, 388, 11)]


def _ch1_search(c, v, pos):
    # a plan of the city
    c.path("M150,196 Q330,140 560,166 Q790,190 830,300 "
           "Q866,414 660,452 Q420,492 250,430 Q136,388 150,196 Z",
           stroke=dim(SAND, 0.9), width=2.0)
    # Tucked under the city outline rather than below it: verse 13 puts a
    # house on the strip beneath, and the outlined box that used to stand
    # there let this word show through where the drawn one covers it.
    c.text((166, 452), "JERUSALEM", 12.5, dim(TEXT_DIM, 0.95), "lm",
           italic=True)

    for label, qx, qy, at in QUARTERS:
        on, first = since(pos, 1, at)
        col = HL if (on and v == at) else (dim(TEXT, 0.92) if on
                                           else dim(TEXT_DIM, 0.45))
        c.circle(qx, qy, 7, fill=dim(GOLD, 0.95) if on else None,
                 stroke=dim(SAND_DIM, 0.8), width=1.5)
        c.text((qx, qy - 22), label, 12.5, col, "mm", bold=on and v == at)
        if on:
            for r in (18, 30, 42):
                c.circle(qx, qy, r, stroke=dim(GOLD, 0.16), width=1.3)
        if first:
            c.pulse_ellipse(qx, qy, 40, 34, dim(HL, 0.9), width=2,
                            first=True)

    # v11 — those loaded with silver, cut off
    s_on, s_first = since(pos, 1, 11)
    if s_on:
        # The merchants' silver, as a stack. Four loose discs read as four
        # discs; a stack with one coin stood on edge beside it reads as
        # money, which is what the verse is weighing.
        # Below Maktesh's marker (430, 388) rather than across it — the
        # quarter's rings run to about y 428, and a stack of masses drawn
        # over them cuts the marker in half.
        cn = F.coins()
        _put(c, cn, 430, 472, _fit(cn, h=38), dim(SILVER, 0.95), 1.4)
        c.line((392, 480), (474, 430), dim(RED, 0.95), 2.6)
        c.text((430, 486), "LOADED WITH SILVER — CUT OFF", 12.5,
               dim(RED, 0.95) if v == 11 else dim(TEXT, 0.92), "mm",
               bold=v == 11)

    # v12 — searched with lamps; men settled on their dregs
    l_on, l_first = since(pos, 1, 12)
    if l_on:
        lx, ly = 792, 300
        c.ellipse(lx, ly + 8, 74, 26, fill=dim(GOLD, 0.13))
        c.polygon([(lx - 24, ly), (lx + 24, ly), (lx + 17, ly - 17),
                   (lx - 17, ly - 17)], fill=dim(PANEL, 0.95),
                  stroke=dim(SAND, 0.95), width=1.7)
        c.path(f"M{lx + 30},{ly - 8} q6,-16 -2,-24 q14,8 2,24",
               fill=dim(GOLD, 0.9))
        c.line((lx + 24, ly - 6), (lx + 34, ly - 5), dim(SAND, 0.95), 1.7)
        c.text((lx, ly + 44), "SEARCHED WITH LAMPS", 13,
               HL if v == 12 else dim(TEXT, 0.92), "mm", bold=v == 12)
        for i, jx in enumerate((730, 800, 870)):
            jar(c, jx, 470, 46, 74, dim(SAND, 0.95), dregs=0.34)
        c.text((800, 500), "SETTLED ON THEIR DREGS", 12.5,
               dim(TEXT, 0.92), "mm", bold=v == 12)
        if l_first:
            c.pulse_ellipse(lx, ly - 4, 62, 46, dim(HL, 0.9), width=2,
                            first=True)

    # v13 — built but not inhabited, planted but not drunk
    b_on, b_first = since(pos, 1, 13)
    if b_on:
        gy2 = 546
        c.line((120, gy2), (620, gy2), dim(SAND_DIM, 0.8), 1.4)
        house(c, 200, gy2, 84, 56, dim(SAND, 0.95), 1.8,
              fill=dim(PANEL, 0.85))
        c.line((156, gy2 - 20), (244, gy2 - 20), dim(RED, 0.95), 2.6)
        c.text((200, gy2 + 20), "BUILT — NOT INHABITED", 12,
               dim(RED, 0.95), "mm", bold=v == 13)
        # A row of the vocabulary's vines. These were a stroke with a disc on
        # top — the lollipop the tree in svg_figures exists to avoid — and
        # they sat next to a drawn house, which is where it showed.
        vn = F.vine()
        for vx in (452, 502, 552):
            _put(c, vn, vx, gy2, _fit(vn, h=58), dim(GREEN, 0.9), 1.6)
        c.line((428, gy2 - 46), (576, gy2 - 8), dim(RED, 0.95), 2.6)
        c.text((500, gy2 + 20), "PLANTED — WINE NOT DRUNK", 12,
               dim(RED, 0.95), "mm", bold=v == 13)
        if b_first:
            c.pulse_rect(140, gy2 - 66, 462, 78, dim(RED, 0.85), width=1.8,
                         first=True, rx=10)


# the nine words of 1:15, in the order the verse piles them up
WRATH = ["WRATH", "DISTRESS", "ANGUISH", "TROUBLE", "RUIN", "DARKNESS",
         "GLOOM", "CLOUDS", "BLACKNESS"]


def _ch1_wrath(c, v, pos):
    # v14 — near, and hurrying
    n_on, n_first = since(pos, 1, 14)
    if n_on:
        arrow(c, (960, 148), (620, 148), HL, 2.8, 13)
        c.text((512, 122), "NEAR — AND HURRIES GREATLY", 16,
               HL if v == 14 else dim(TEXT, 0.92), "mm", bold=v == 14)
        figure(c, 190, 200, 60, dim(RED, 0.95), 2.1, arms="up")
        c.text((190, 226), "THE MIGHTY MAN CRIES BITTERLY", 12,
               dim(RED, 0.95) if v == 14 else dim(TEXT_DIM, 0.95), "mm",
               bold=v == 14)
        if n_first:
            c.pulse_rect(600, 128, 380, 40, dim(HL, 0.85), width=2,
                         first=True, rx=18)

    # v15 — the day named nine times, going to black
    d_on, d_first = since(pos, 1, 15)
    if d_on:
        x0, bw, gap = 62, 92, 8
        for i, word in enumerate(WRATH):
            bx = x0 + i * (bw + gap)
            col = mix(SAND, NIGHT, (i / (len(WRATH) - 1)) ** 0.85)
            c.rect(bx, 300, bw, 96, fill=col, stroke=dim(SAND_DIM, 0.55),
                   width=1.2)
            c.text((bx + bw / 2, 412), word, 11, dim(TEXT, 0.92), "mm")
        c.text((512, 274), "THAT DAY IS A DAY OF —", 13, dim(TEXT_DIM, 0.95),
               "mm", italic=True)
        if d_first:
            c.pulse_rect(x0 - 6, 294, 9 * (bw + gap) - gap + 12, 108,
                         dim(HL, 0.88), width=2, first=True, rx=6)

    # v16 — trumpet and alarm, against the fortified cities
    t_on, t_first = since(pos, 1, 16)
    if t_on:
        tx, ty = 214, 494
        c.polygon([(tx - 44, ty - 8), (tx + 30, ty - 20), (tx + 44, ty - 34),
                   (tx + 44, ty + 6), (tx + 30, ty - 8)],
                  fill=dim(PANEL, 0.9), stroke=GOLD, width=2.0)
        for r in (18, 30, 42):
            c.path(f"M{tx + 52},{ty - 14 - r * 0.5} "
                   f"A{r},{r} 0 0 1 {tx + 52},{ty - 14 + r * 0.5}",
                   stroke=dim(GOLD, 0.45), width=1.5)
        c.text((tx, ty + 34), "TRUMPET AND ALARM", 13, HL, "mm", bold=v == 16)
        for i, (bx, bh) in enumerate(((640, 76), (720, 104), (800, 68),
                                      (880, 92))):
            c.rect(bx - 26, 540 - bh, 52, bh, fill=dim(PANEL, 0.85),
                   stroke=dim(SAND, 0.9), width=1.7)
            for k in range(3):
                c.rect(bx - 26 + k * 19, 540 - bh - 8, 12, 8,
                       stroke=dim(SAND, 0.9), width=1.3)
        c.line((600, 540), (940, 540), dim(SAND_DIM, 0.85), 1.5)
        c.text((760, 566), "THE FORTIFIED CITIES — THE HIGH BATTLEMENTS", 12,
               dim(TEXT, 0.92), "mm", bold=v == 16)
        if t_first:
            c.pulse_rect(600, 420, 340, 128, dim(HL, 0.85), width=1.9,
                         first=True, rx=8)


def _ch1_blind(c, v, pos):
    gy = 400
    c.line((90, gy), (600, gy), dim(SAND_DIM, 0.85), 1.6)
    for i, fx in enumerate((180, 268, 356, 444)):
        figure(c, fx, gy, 72, dim(GRAY, 0.95), 2.1, arms="grope",
               legs="walk")
        c.line((fx - 11, gy - 62), (fx + 11, gy - 62), dim(GRAY, 0.95), 2.2)
    c.text((312, gy + 30), "THEY WILL WALK LIKE BLIND MEN", 14,
           HL if v == 17 else dim(TEXT, 0.92), "mm", bold=v == 17)
    if since(pos, 1, 17)[1]:
        c.pulse_rect(120, gy - 92, 384, 116, dim(HL, 0.88), width=2,
                     first=True, rx=12)

    # v18 — the weight that cannot buy them out
    g_on, g_first = since(pos, 1, 18)
    if g_on:
        bx, by = 790, 250
        c.line((bx, by - 40), (bx, by + 92), dim(SAND, 0.95), 2.2)
        c.line((bx - 96, by - 4), (bx + 96, by - 36), dim(SAND, 0.95), 2.2)
        c.line((bx + 96, by + 92), (bx - 96, by + 92), dim(SAND_DIM, 0.8),
               1.4)
        for sx, sy, dp in ((bx - 96, by - 4, 28), (bx + 96, by - 36, 20)):
            c.path(f"M{sx - 30},{sy + dp} A30,{dp} 0 0 0 {sx + 30},{sy + dp}",
                   stroke=dim(SAND, 0.95), width=1.8)
            c.line((sx, sy), (sx, sy + dp), dim(SAND_DIM, 0.9), 1.2)
        for dx, dy in ((-14, -2), (2, -9), (16, -1)):
            c.circle(bx - 96 + dx, by + 6 + dy, 8, fill=dim(SILVER, 0.8))
        for dx, dy in ((-8, -2), (8, -2)):
            c.circle(bx - 96 + dx, by - 12 + dy, 8, fill=dim(GOLD, 0.85))
        arrow(c, (bx - 96, by + 60), (bx - 96, by + 20), dim(RED, 0.8), 1.8,
              7, dash="5,5")
        cross(c, bx - 96, by + 66, 11, dim(RED, 0.95), 2.4)
        c.text((bx, by + 122), "NEITHER SILVER NOR GOLD", 13,
               dim(RED, 0.95) if v == 18 else dim(TEXT, 0.92), "mm",
               bold=v == 18)
        c.text((bx, by + 142), "will be able to deliver them", 11.5,
               dim(TEXT_DIM, 0.95), "mm", italic=True)
        # the fire of his jealousy — the same flame as 3:8
        for i in range(11):
            flame(c, 120 + i * 74, 546, 40 + (i % 3) * 12, dim(FIRE, 0.85))
        c.text((512, 566), "THE FIRE OF HIS JEALOUSY", 13, dim(FIRE, 1.0),
               "mm", bold=v == 18)
        if g_first:
            c.pulse_ellipse(bx, by + 30, 128, 92, dim(RED, 0.85), width=1.9,
                            first=True)


# ---------------------------------------------------------------------------
# Chapter 2 — the compass
# ---------------------------------------------------------------------------

def draw_ch2(c, v, pos):
    if v <= 3:
        _ch2_gather(c, v, pos)
    elif v <= 7:
        _ch2_west(c, v, pos)
    elif v <= 11:
        _ch2_east(c, v, pos)
    elif v == 12:
        _ch2_south(c, v, pos)
    else:
        _ch2_north(c, v, pos)


def _ch2_gather(c, v, pos):
    # the three "before"s, running to the day
    rail_y = 300
    c.line((120, rail_y), (880, rail_y), dim(SAND, 0.9), 2.2)
    stops = [("BEFORE THE APPOINTED TIME", 250), ("BEFORE THE FIERCE ANGER",
              460), ("BEFORE THE DAY", 660)]
    b_on, b_first = since(pos, 2, 2)
    for i, (label, sx) in enumerate(stops):
        col = dim(TEXT, 0.92) if b_on else dim(TEXT_DIM, 0.4)
        c.line((sx, rail_y - 14), (sx, rail_y + 14),
               dim(SAND, 0.9) if b_on else dim(SAND_DIM, 0.5), 2.0)
        if b_on:
            c.text((sx, rail_y - 30), label, 12, col, "mm", bold=v == 2)
    # the day itself, at the end of the rail
    c.rect(880, rail_y - 54, 66, 108, fill=dim(RED, 0.22),
           stroke=dim(RED, 0.9), width=2)
    c.text((913, rail_y + 74), "THE DAY OF", 12, dim(RED, 0.95), "mm")
    c.text((913, rail_y + 92), "YAHWEH'S ANGER", 12, dim(RED, 0.95), "mm")
    if b_first:
        c.pulse_rect(120, rail_y - 46, 760, 92, dim(HL, 0.85), width=1.9,
                     first=True, rx=10)
    # chaff blowing past
    if b_on:
        for i in range(7):
            xx = 180 + i * 96
            c.path(f"M{xx},{rail_y + 44} q10,-7 22,-2", stroke=dim(SAND_DIM,
                   0.75), width=1.4)

    # v1 — gathered together
    g_on, g_first = since(pos, 2, 1)
    if g_on:
        for i, fx in enumerate((196, 232, 268, 304)):
            figure(c, fx, 470, 48, dim(TEXT, 0.92), 1.9)
        for i, sx in enumerate((150, 350)):
            arrow(c, (sx, 430), (sx + (44 if i == 0 else -44), 430),
                  dim(GOLD, 0.85), 1.9, 8)
        c.text((250, 500), "GATHER YOURSELVES TOGETHER", 13,
               HL if v == 1 else dim(TEXT, 0.92), "mm", bold=v == 1)
        if g_first:
            c.pulse_ellipse(250, 448, 116, 56, dim(HL, 0.9), width=2,
                            first=True)

    # v3 — three things to seek, and a place to be hidden
    s_on, s_first = since(pos, 2, 3)
    if s_on:
        for i, label in enumerate(("SEEK YAHWEH", "SEEK RIGHTEOUSNESS",
                                   "SEEK HUMILITY")):
            yy = 424 + i * 32
            arrow(c, (540, yy), (622, yy), dim(GOLD, 0.9), 2.0, 8)
            c.text((634, yy), label, 13, HL if v == 3 else dim(TEXT, 0.92),
                   "lm", bold=v == 3)
        c.polygon([(714, 566), (806, 566), (806, 538), (760, 516),
                   (714, 538)], fill=dim(PANEL, 0.9), stroke=GOLD, width=1.9)
        c.text((760, 552), "HIDDEN", 12, HL, "mm", bold=v == 3)
        if s_first:
            c.pulse_rect(528, 406, 330, 100, dim(HL, 0.88), width=1.9,
                         first=True, rx=12)
    compass(c, None, ())


def _ch2_west(c, v, pos):
    compass(c, "W", ())
    gy = 320
    # the coast
    c.path("M240,150 Q214,250 244,340 Q272,428 246,520", stroke=dim(SEA, 0.9),
           width=2.2)
    c.rect(84, 130, 156, 400, fill=dim(SEA, 0.14))
    c.text((150, 160), "THE SEA COAST", 12, dim(TEXT_DIM, 0.95), "mm",
           italic=True)

    CITIES = [("GAZA", 350, 190, "FORSAKEN"), ("ASHKELON", 350, 288,
               "A DESOLATION"), ("ASHDOD", 350, 386, "DRIVEN OUT AT NOONDAY"),
              ("EKRON", 350, 484, "ROOTED UP")]
    c_on, c_first = since(pos, 2, 4)
    if c_on:
        for i, (name, cx, cy, fate) in enumerate(CITIES):
            c.rect(cx - 44, cy - 22, 88, 44, fill=dim(PANEL, 0.88),
                   stroke=dim(SAND, 0.9), width=1.7)
            c.text((cx, cy), name, 13, dim(TEXT, 0.95), "mm")
            cross(c, cx, cy, 26, dim(RED, 0.85), 2.2)
            c.text((cx + 62, cy), fate, 12.5, dim(RED, 0.95), "lm",
                   bold=v == 4)
            if i == 2:      # driven out at noonday — the sun at its height
                c.circle(cx + 250, cy - 4, 15, fill=dim(GOLD, 0.35),
                         stroke=dim(GOLD, 0.95), width=1.6)
                for k in range(8):
                    a = k * math.pi / 4
                    c.line((cx + 250 + 20 * math.cos(a),
                            cy - 4 + 20 * math.sin(a)),
                           (cx + 250 + 28 * math.cos(a),
                            cy - 4 + 28 * math.sin(a)), dim(GOLD, 0.8), 1.5)
            if i == 3:      # rooted up
                for k, ddx in enumerate((-18, 0, 18)):
                    c.line((cx + ddx, cy - 22), (cx + ddx * 1.5, cy - 44),
                           dim(BROWN, 0.9), 1.6)
        if c_first:
            c.pulse_rect(298, 160, 104, 350, dim(RED, 0.85), width=2,
                         first=True, rx=8)
    w_on, w_first = since(pos, 2, 5)
    if w_on:
        c.text((640, 148), "CANAAN, THE LAND OF THE PHILISTINES", 13,
               dim(RED, 0.95) if v == 5 else dim(TEXT, 0.92), "mm",
               bold=v == 5)
        c.text((640, 168), "the nation of the Cherethites — no inhabitant",
               11.5, dim(TEXT_DIM, 0.95), "mm", italic=True)
        if w_first:
            c.pulse_rect(410, 132, 460, 50, dim(RED, 0.85), width=1.8,
                         first=True, rx=14)

    # vv6-7 — the same coast, become pasture for the remnant
    p_on, p_first = since(pos, 2, 6)
    if p_on:
        c.rect(84, 130, 156, 400, fill=dim(GREEN, 0.16))
        gy2 = 470
        for i, hx in enumerate((122, 194)):
            house(c, hx, gy2, 46, 32, dim(SAND, 0.9), 1.6,
                  fill=dim(PANEL, 0.85))
        c.text((160, gy2 + 22), "COTTAGES", 11.5, dim(TEXT, 0.92), "mm")
        c.text((160, gy2 + 38), "FOR SHEPHERDS", 11.5, dim(TEXT, 0.92), "mm")
        for i, bx in enumerate((136, 200)):
            lying_beast(c, bx, 384, 62, dim(TEXT, 0.92), 1.7)
        c.text((160, 348), "FOLDS FOR FLOCKS", 11.5, dim(TEXT, 0.92), "mm")
        if p_first:
            c.pulse_rect(84, 320, 156, 210, dim(GREEN, 0.95), width=2,
                         first=True, rx=6)
    r_on, r_first = since(pos, 2, 7)
    if r_on:
        c.text((640, 520), "FOR THE REMNANT OF THE HOUSE OF JUDAH", 13.5,
               HL if v == 7 else dim(TEXT, 0.92), "mm", bold=v == 7)
        c.text((640, 542), "they will lie down in the evening", 11.5,
               dim(TEXT_DIM, 0.95), "mm", italic=True)
        if r_first:
            c.pulse_rect(400, 504, 480, 34, dim(HL, 0.88), width=1.9,
                         first=True, rx=16)


def _ch2_east(c, v, pos):
    compass(c, "E", ("W",))
    m_on, m_first = since(pos, 2, 8)
    j_on, j_first = since(pos, 2, 9)

    pairs = [("MOAB", "AS SODOM", 400), ("AMMON", "AS GOMORRAH", 700)]
    for name, like, cx in pairs:
        cy = 300
        if m_on:
            c.rect(cx - 92, cy - 60, 184, 120, fill=dim(PANEL, 0.6),
                   stroke=dim(SAND, 0.9), width=1.8, rx=4)
            c.text((cx, cy - 84), name, 16, dim(TEXT, 0.95), "mm",
                   bold=v == 8)
        if j_on:
            # ruined, and named for the ruin it is like
            for k, (bx, bw, bh) in enumerate(((cx - 52, 40, 34),
                                              (cx - 4, 30, 48),
                                              (cx + 44, 36, 28))):
                c.polygon([(bx - bw / 2, cy + 44), (bx + bw / 2, cy + 44),
                           (bx + bw / 2 - 6, cy + 44 - bh * 0.34),
                           (bx - bw / 2 + 8, cy + 44 - bh * 0.28)],
                          fill=dim(ASH, 0.45), stroke=dim(ASH, 0.9),
                          width=1.4)
            c.text((cx, cy - 24), like, 14, dim(RED, 0.95), "mm",
                   bold=v == 9)
            # nettles and salt pits
            for k, nx in enumerate((cx - 60, cx - 20, cx + 24, cx + 62)):
                c.line((nx, cy + 44), (nx - 5, cy + 18), dim(GREEN, 0.7), 1.5)
                c.line((nx - 5, cy + 30), (nx + 7, cy + 24), dim(GREEN, 0.7),
                       1.3)
            c.ellipse(cx, cy + 56, 62, 9, fill=dim(SILVER, 0.30))
        if j_first:
            c.pulse_rect(cx - 100, cy - 68, 200, 140, dim(RED, 0.85),
                         width=1.9, first=True, rx=8)
    if j_on:
        c.text((550, 400), "NETTLES — SALT PITS — PERPETUAL DESOLATION", 12.5,
               dim(TEXT_DIM, 0.95), "mm", italic=True)
    if m_on:
        c.text((550, 152), "THE REPROACH OF MOAB — THE INSULTS OF AMMON",
               13.5, HL if v == 8 else dim(TEXT, 0.92), "mm", bold=v == 8)
        if m_first:
            c.pulse_rect(300, 136, 500, 34, dim(HL, 0.88), width=1.9,
                         first=True, rx=16)

    # v10 — this they will have for their pride
    p_on, p_first = since(pos, 2, 10)
    if p_on:
        arrow(c, (550, 200), (550, 168), dim(RED, 0.9), 2.0, 8)
        c.text((550, 218), "FOR THEIR PRIDE", 13,
               dim(RED, 0.95) if v == 10 else dim(TEXT, 0.92), "mm",
               bold=v == 10)
        if p_first:
            c.pulse_rect(470, 202, 160, 32, dim(RED, 0.85), width=1.8,
                         first=True, rx=15)

    # v11 — the gods of the land famished
    f_on, f_first = since(pos, 2, 11)
    if f_on:
        for i, ix in enumerate((360, 430, 500)):
            c.rect(ix - 12, 470, 24, 56, fill=dim(PANEL, 0.85),
                   stroke=dim(GRAY, 0.8), width=1.6)
            c.circle(ix, 460, 13, fill=dim(PANEL, 0.85),
                     stroke=dim(GRAY, 0.8), width=1.6)
            c.line((ix - 20, 500), (ix + 20, 470), dim(RED, 0.9), 2.2)
        c.text((430, 546), "HE WILL FAMISH ALL THE GODS OF THE LAND", 12.5,
               dim(RED, 0.95) if v == 11 else dim(TEXT, 0.92), "mm",
               bold=v == 11)
        for i, fx in enumerate((680, 760, 840)):
            figure(c, fx, 526, 44, GOLD, 1.8, arms="up")
        c.text((740, 552), "EVERYONE FROM HIS PLACE", 12,
               HL if v == 11 else dim(TEXT, 0.92), "mm", bold=v == 11)
        if f_first:
            c.pulse_rect(636, 470, 250, 66, dim(HL, 0.88), width=1.9,
                         first=True, rx=10)


def _ch2_south(c, v, pos):
    """v12 — one line of text, one line of drawing."""
    compass(c, "S", ("W", "E"))
    phrase(c, (560, 180), "YOU CUSHITES ALSO", 22, dim(RED, 1.0), first=True)
    gy = 380
    c.line((330, gy), (860, gy), dim(SAND_DIM, 0.8), 1.5)
    for i, fx in enumerate((470, 540, 610)):
        figure(c, fx, gy, 60, dim(GRAY, 0.95), 2.0)
    # the sword
    sx, sy = 740, 300
    c.polygon([(sx, sy), (sx + 11, sy + 16), (sx + 11, sy + 108),
               (sx, sy + 122), (sx - 11, sy + 108), (sx - 11, sy + 16)],
              fill=dim(SILVER, 0.30), stroke=dim(SILVER, 0.95), width=1.9)
    c.line((sx - 30, sy + 8), (sx + 30, sy + 8), dim(SAND, 0.95), 2.4)
    c.line((sx, sy - 26), (sx, sy + 8), dim(SAND, 0.95), 2.4)
    c.text((sx, gy + 30), "BY MY SWORD", 13.5, dim(RED, 0.95), "mm",
           bold=True)
    c.pulse_ellipse(sx, sy + 60, 40, 88, dim(RED, 0.85), width=1.9,
                    first=True)


def _ch2_north(c, v, pos):
    compass(c, "N", ("W", "E", "S"))
    n_on, n_first = since(pos, 2, 13)
    gy = 466

    if n_on:
        c.text((600, 132), "ASSYRIA — AND NINEVEH A DESOLATION", 15,
               HL if v == 13 else dim(TEXT, 0.92), "mm", bold=v == 13)
        c.text((600, 154), "as dry as the wilderness", 11.5,
               dim(TEXT_DIM, 0.95), "mm", italic=True)
        if n_first:
            c.pulse_rect(346, 116, 508, 34, dim(HL, 0.88), width=1.9,
                         first=True, rx=16)

    # the ruin, labelled by what now lives in each named part
    bx0, bx1 = 340, 860
    c.line((300, gy), (800, gy), dim(SAND_DIM, 0.85), 1.6)
    # columns and their capitals
    for i, cx in enumerate((400, 520, 640, 760)):
        c.rect(cx - 15, gy - 150, 30, 150, fill=dim(PANEL, 0.85),
               stroke=dim(SAND, 0.9), width=1.7)
        c.rect(cx - 25, gy - 172, 50, 22, fill=dim(PANEL, 0.9),
               stroke=dim(SAND, 0.9), width=1.7)
    # the cedar beams above, laid bare
    c.line((360, gy - 182), (820, gy - 182), dim(BROWN, 0.9), 3.0)
    for i in range(9):
        c.line((378 + i * 52, gy - 182), (378 + i * 52, gy - 202),
               dim(BROWN, 0.7), 2.0)
    c.text((880, gy - 192), "CEDAR BEAMS", 12, dim(TEXT, 0.92), "lm",
           bold=v == 14)
    c.text((880, gy - 174), "laid bare", 11, dim(TEXT_DIM, 0.95), "lm",
           italic=True)

    s_on, s_first = since(pos, 2, 14)
    if s_on:
        # Pelican and porcupine, lodging in the capitals. The pelican is the
        # vocabulary's bird; the porcupine is the one creature in this book
        # svg_figures has no answer for, and one disputed word in one verse
        # does not earn a subject in a canon-wide set — so it keeps the
        # generic labelled quadruped, which is what that mark is for.
        bird(c, 400, gy - 190, 44, GOLD, 1.9)
        generic_beast(c, 760, gy - 178, 40, GOLD, 1.6)
        c.text((400, gy - 214), "PELICAN", 11.5, HL, "mm", bold=v == 14)
        c.text((760, gy - 214), "PORCUPINE", 11.5, HL, "mm", bold=v == 14)
        c.text((250, gy - 168), "THE CAPITALS", 12, dim(TEXT, 0.92), "rm",
               bold=v == 14)
        arrow(c, (262, gy - 168), (368, gy - 172), dim(SAND, 0.7), 1.5, 6)
        # windows their calls echo through
        for i, wx in enumerate((460, 580, 700)):
            c.rect(wx - 17, gy - 116, 34, 42, fill=dim(NIGHT, 0.85),
                   stroke=dim(SAND, 0.9), width=1.6)
            for r in (10, 18):
                c.path(f"M{wx + 20},{gy - 104} A{r},{r} 0 0 1 "
                       f"{wx + 20},{gy - 104 + r}", stroke=dim(GOLD, 0.45),
                       width=1.4)
        c.text((250, gy - 96), "THE WINDOWS", 12, dim(TEXT, 0.92), "rm",
               bold=v == 14)
        # desolation in the thresholds
        c.rect(bx0 + 100, gy - 14, 300, 14, fill=dim(ASH, 0.45),
               stroke=dim(ASH, 0.9), width=1.6)
        c.text((250, gy - 8), "THE THRESHOLDS", 12, dim(TEXT, 0.92), "rm",
               bold=v == 14)
        # the herds lying down in the middle of her
        for i, lx in enumerate((470, 566, 662)):
            lying_beast(c, lx, gy - 22, 62, dim(TEXT, 0.92), 1.7)
        c.text((566, gy + 26), "HERDS LIE DOWN IN THE MIDDLE OF HER", 12.5,
               HL if v == 14 else dim(TEXT, 0.92), "mm", bold=v == 14)
        if s_first:
            c.pulse_rect(320, gy - 226, 580, 262, dim(HL, 0.88), width=2,
                         first=True, rx=8)

    # v15 — the boast, and what passes by now
    b_on, b_first = since(pos, 2, 15)
    if b_on:
        phrase(c, (600, 196), "I AM, AND THERE IS NO ONE BESIDES ME", 19,
               dim(RED, 1.0), first=b_first)
        c.text((600, 546), "EVERYONE WHO PASSES BY WILL HISS", 12.5,
               dim(RED, 0.95), "mm", bold=v == 15)


# ---------------------------------------------------------------------------
# Chapter 3 — one centre, three occupants
# ---------------------------------------------------------------------------

CENTRE = (512, 322)

OFFICES = [("PRINCES", "ROARING LIONS", 3), ("JUDGES", "EVENING WOLVES", 3),
           ("PROPHETS", "ARROGANT AND TREACHEROUS", 4),
           ("PRIESTS", "PROFANED THE SANCTUARY", 4)]
OFFICE_POS = [(196, 208), (828, 208), (196, 452), (828, 452)]


def draw_ch3(c, v, pos):
    if v <= 5:
        _ch3_offices(c, v, pos)
    elif v <= 8:
        _ch3_gathering(c, v, pos)
    elif v <= 13:
        _ch3_turn(c, v, pos)
    else:
        _ch3_singing(c, v, pos)


def city_ring(c, lit=False):
    cx, cy = CENTRE
    col = dim(SAND, 0.9) if not lit else dim(GOLD, 0.9)
    c.ellipse(cx, cy, 236, 148, stroke=col, width=2.0)
    for k in range(16):
        a = k * math.pi / 8
        c.line((cx + 236 * math.cos(a), cy + 148 * math.sin(a)),
               (cx + 250 * math.cos(a), cy + 158 * math.sin(a)),
               dim(SAND_DIM, 0.6), 1.3)


def _ch3_offices(c, v, pos):
    city_ring(c)
    w_on, w_first = since(pos, 3, 1)
    if w_on:
        phrase(c, (512, 108), "WOE TO THE OPPRESSING CITY", 21,
               dim(RED, 1.0), first=w_first)
        c.text((512, 148), "rebellious and polluted", 12,
               dim(TEXT_DIM, 0.95), "mm", italic=True)

    # v2 — four things she did not do, each stopped short of the centre
    r_on, r_first = since(pos, 3, 2)
    if r_on:
        c.text((CENTRE[0], 196), "SHE DIDN'T —", 13, dim(RED, 0.95), "mm",
               italic=True)
        for label, rx in (("OBEY", 380), ("CORRECTION", 472),
                          ("TRUST", 570), ("DRAW NEAR", 668)):
            c.text((rx, 220), label, 12, dim(TEXT, 0.92), "mm",
                   bold=v == 2)
            c.line((rx, 234), (rx, 258), dim(RED, 0.55), 1.7, dash="6,6")
            cross(c, rx, 266, 8, dim(RED, 0.9), 2.0)
        if r_first:
            c.pulse_rect(330, 206, 388, 76, dim(RED, 0.8), width=1.9,
                         first=True, rx=10)

    # vv3-4 — the four offices, each struck
    for i, (name, charge, at) in enumerate(OFFICES):
        on, first = since(pos, 3, at)
        ox, oy = OFFICE_POS[i]
        col = dim(SAND, 0.9) if on else dim(SAND_DIM, 0.35)
        c.rect(ox - 92, oy - 44, 184, 88, fill=dim(PANEL, 0.6), stroke=col,
               width=1.8, rx=5)
        c.text((ox, oy - 62), name, 14,
               dim(TEXT, 0.95) if on else dim(TEXT_DIM, 0.45), "mm",
               bold=on and v == at)
        if on:
            if i == 0:                       # her princes are roaring lions
                beast(c, ox, oy + 28, 66, dim(RED, 0.9), 1.8, kind="lion")
            elif i == 1:                     # her judges, evening wolves
                beast(c, ox, oy + 28, 62, dim(RED, 0.9), 1.7, kind="wolf")
            elif i == 2:
                for k, dx in enumerate((-40, 0, 40)):
                    figure(c, ox + dx, oy + 30, 46, dim(RED, 0.9), 1.7,
                           arms="up")
            else:
                altar(c, ox, oy + 30, 76, 44, dim(RED, 0.9), 1.8)
            c.text((ox, oy + 62), charge, 12, dim(RED, 0.95), "mm",
                   bold=on and v == at)
        if first:
            c.pulse_rect(ox - 100, oy - 52, 200, 104, dim(RED, 0.85),
                         width=1.9, first=True, rx=8)

    # v5 — the one within her who does not fail
    j_on, j_first = since(pos, 3, 5)
    if j_on:
        figure(c, CENTRE[0], CENTRE[1] + 64, 86, GOLD, 2.4)
        c.text((CENTRE[0], CENTRE[1] - 34), "YAHWEH, WITHIN HER", 15, HL,
               "mm", bold=v == 5)
        c.text((CENTRE[0], CENTRE[1] - 14), "is righteous", 11.5,
               dim(TEXT_DIM, 0.95), "mm", italic=True)
        for i in range(6):
            sunrise(c, 400 + i * 45, CENTRE[1] + 100, 13, dim(GOLD, 0.9), 1.5)
        c.text((CENTRE[0], CENTRE[1] + 132), "EVERY MORNING — HE DOESN'T FAIL",
               12.5, HL if v == 5 else dim(TEXT, 0.92), "mm", bold=v == 5)
        if j_first:
            c.pulse_ellipse(CENTRE[0], CENTRE[1] + 64, 62, 64, dim(HL, 0.9),
                            width=2.2, first=True)


def _ch3_gathering(c, v, pos):
    # v6 — the nations already cut off
    n_on, n_first = since(pos, 3, 6)
    if n_on:
        gy = 268
        c.line((110, gy), (952, gy), dim(SAND_DIM, 0.85), 1.5)
        for i, (bx, bh) in enumerate(((190, 74), (330, 96), (470, 62),
                                      (610, 88), (750, 70), (880, 92))):
            c.rect(bx - 30, gy - bh, 60, bh, fill=dim(PANEL, 0.6),
                   stroke=dim(ASH, 0.85), width=1.6)
            for k in range(2):
                c.line((bx - 30, gy - bh + 12 + k * 22),
                       (bx + 30, gy - bh + 4 + k * 22), dim(ASH, 0.7), 1.3)
        c.text((512, 200), "THEIR BATTLEMENTS ARE DESOLATE", 14,
               HL if v == 6 else dim(TEXT, 0.92), "mm", bold=v == 6)
        c.text((512, 296), "no man — no inhabitant", 12,
               dim(TEXT_DIM, 0.95), "mm", italic=True)
        if n_first:
            c.pulse_rect(140, 160, 780, 120, dim(HL, 0.85), width=1.9,
                         first=True, rx=10)

    # v7 — the morning that answers 3:5, gone the other way
    e_on, e_first = since(pos, 3, 7)
    if e_on:
        sunrise(c, 300, 400, 22, dim(GOLD, 0.9), 1.9)
        c.text((300, 440), "EVERY MORNING", 12.5, dim(TEXT, 0.92), "mm")
        c.text((300, 458), "he brings justice to light", 11,
               dim(TEXT_DIM, 0.95), "mm", italic=True)
        sunrise(c, 700, 400, 22, dim(RED, 0.9), 1.9)
        cross(c, 700, 386, 15, dim(RED, 0.95), 2.2)
        c.text((700, 440), "THEY ROSE EARLY", 12.5,
               dim(RED, 0.95) if v == 7 else dim(TEXT, 0.92), "mm",
               bold=v == 7)
        c.text((700, 458), "and corrupted all their doings", 11,
               dim(TEXT_DIM, 0.95), "mm", italic=True)
        c.line((500, 372), (500, 428), dim(SAND_DIM, 0.7), 1.4, dash="5,6")
        if e_first:
            c.pulse_ellipse(700, 404, 56, 50, dim(RED, 0.85), width=1.9,
                            first=True)

    # v8 — wait; the nations gathered, and the same fire as 1:18
    g_on, g_first = since(pos, 3, 8)
    if g_on:
        phrase(c, (512, 112), "WAIT FOR ME, SAYS YAHWEH", 21, HL,
               first=g_first)
        cx, cy = 512, 508
        for a_deg in (200, 232, 264, 296, 328):
            a = math.radians(a_deg)
            arrow(c, (cx + 250 * math.cos(a), cy + 150 * math.sin(a)),
                  (cx + 96 * math.cos(a), cy + 58 * math.sin(a)),
                  dim(GOLD, 0.9), 2.0, 8)
        c.text((cx, cy - 4), "GATHER THE NATIONS", 13.5, HL, "mm",
               bold=v == 8)
        for i in range(9):
            flame(c, 200 + i * 78, 566, 34 + (i % 3) * 10, dim(FIRE, 0.8))
        c.text((cx, 542), "THE FIRE OF MY JEALOUSY", 12.5, dim(FIRE, 1.0),
               "mm", bold=v == 8)


def _ch3_turn(c, v, pos):
    city_ring(c)

    # v9 — many lips made one
    l_on, l_first = since(pos, 3, 9)
    if l_on:
        jx, jy = 512, 140
        for i, sx in enumerate((250, 336, 422, 602, 688, 774)):
            c.path(f"M{sx},{jy + 66} Q{(sx + jx) / 2},{jy + 40} {jx},{jy + 8}",
                   stroke=dim(GOLD, 0.7), width=1.7)
            c.circle(sx, jy + 70, 6, fill=dim(SAND, 0.85))
        c.circle(jx, jy, 12, fill=dim(GOLD, 0.85))
        c.text((jx, jy - 30), "A PURE LANGUAGE", 14, HL, "mm", bold=v == 9)
        c.text((jx, jy + 34), "shoulder to shoulder", 11.5,
               dim(TEXT_DIM, 0.95), "mm", italic=True)
        if l_first:
            c.pulse_ellipse(jx, jy + 34, 300, 62, dim(HL, 0.88), width=1.9,
                            first=True)

    # v10 — the line to Cush, run the other way
    cu_on, cu_first = since(pos, 3, 10)
    if cu_on:
        arrow(c, (196, 520), (CENTRE[0] - 168, CENTRE[1] + 96),
              dim(GOLD, 0.9), 2.2, 9)
        c.text((196, 546), "FROM BEYOND THE RIVERS OF CUSH", 12.5,
               HL if v == 10 else dim(TEXT, 0.92), "mm", bold=v == 10)
        c.text((196, 566), "my worshipers bring my offering", 11,
               dim(TEXT_DIM, 0.95), "mm", italic=True)
        if cu_first:
            c.pulse_rect(56, 530, 280, 32, dim(HL, 0.88), width=1.8,
                         first=True, rx=15)

    # v11 — the proud taken out from among her
    p_on, p_first = since(pos, 3, 11)
    if p_on:
        for i, fx in enumerate((690, 736)):
            figure(c, fx, CENTRE[1] - 10, 56, dim(GRAY, 0.7), 1.8)
        arrow(c, (660, CENTRE[1] - 46), (786, CENTRE[1] - 76),
              dim(RED, 0.9), 2.0, 8)
        c.text((760, CENTRE[1] - 96), "YOUR PROUDLY EXULTING ONES", 12.5,
               dim(RED, 0.95) if v == 11 else dim(TEXT_DIM, 0.95), "mm",
               bold=v == 11)
        c.text((760, CENTRE[1] + 34), "taken away", 11.5,
               dim(TEXT_DIM, 0.95), "mm", italic=True)
        if p_first:
            c.pulse_ellipse(714, CENTRE[1] - 34, 66, 60, dim(RED, 0.85),
                            width=1.9, first=True)

    # v12 — and who is left in their place
    a_on, a_first = since(pos, 3, 12)
    if a_on:
        for i, fx in enumerate((466, 512, 558)):
            figure(c, fx, CENTRE[1] + 30, 58, GOLD, 2.0)
        c.text((CENTRE[0], CENTRE[1] - 44), "AN AFFLICTED AND POOR PEOPLE",
               14, HL if v == 12 else dim(TEXT, 0.92), "mm", bold=v == 12)
        c.text((CENTRE[0], CENTRE[1] - 24), "left among you", 11.5,
               dim(TEXT_DIM, 0.95), "mm", italic=True)
        if a_first:
            c.pulse_ellipse(CENTRE[0], CENTRE[1], 92, 78, dim(HL, 0.9),
                            width=2.1, first=True)

    # v13 — the posture the animals had in ruined Nineveh, meant well
    d_on, d_first = since(pos, 3, 13)
    if d_on:
        for i, lx in enumerate((408, 512, 616)):
            lying_beast(c, lx, CENTRE[1] + 116, 66, GOLD, 1.8)
        c.text((CENTRE[0], CENTRE[1] + 150), "THEY WILL FEED AND LIE DOWN",
               13.5, HL if v == 13 else dim(TEXT, 0.92), "mm", bold=v == 13)
        c.text((CENTRE[0], CENTRE[1] + 170), "no one will make them afraid",
               11.5, dim(TEXT_DIM, 0.95), "mm", italic=True)
        if d_first:
            c.pulse_ellipse(CENTRE[0], CENTRE[1] + 116, 140, 40,
                            dim(HL, 0.9), width=2, first=True)


def _ch3_singing(c, v, pos):
    city_ring(c, lit=since(pos, 3, 15)[0])

    # v14 — three summons
    s_on, s_first = since(pos, 3, 14)
    if s_on:
        for i, (word, who) in enumerate((("SING", "daughter of Zion"),
                                         ("SHOUT", "Israel"),
                                         ("BE GLAD", "daughter of Jerusalem"))):
            xx = 236 + i * 276
            c.text((xx, 132), word, 17, HL if v == 14 else dim(TEXT, 0.92),
                   "mm", bold=v == 14)
            c.text((xx, 154), who, 11.5, dim(TEXT_DIM, 0.95), "mm",
                   italic=True)
        if s_first:
            c.pulse_rect(140, 112, 744, 56, dim(HL, 0.88), width=1.9,
                         first=True, rx=20)

    # v15 — the King, among you
    k_on, k_first = since(pos, 3, 15)
    if k_on:
        figure(c, CENTRE[0], CENTRE[1] + 44, 92, GOLD, 2.5, arms="open")
        # a crown
        cxx, cyy = CENTRE[0], CENTRE[1] - 56
        c.polyline([(cxx - 22, cyy + 12), (cxx - 22, cyy - 8),
                    (cxx - 11, cyy + 2), (cxx, cyy - 12), (cxx + 11, cyy + 2),
                    (cxx + 22, cyy - 8), (cxx + 22, cyy + 12)],
                   GOLD, 2.2, closed=True)
        c.text((CENTRE[0], CENTRE[1] - 86), "THE KING OF ISRAEL, YAHWEH", 15,
               HL, "mm", bold=v == 15)
        c.text((CENTRE[0], CENTRE[1] - 66), "is among you", 11.5,
               dim(TEXT_DIM, 0.95), "mm", italic=True)
        if k_first:
            c.pulse_ellipse(CENTRE[0], CENTRE[1], 84, 104, dim(HL, 0.9),
                            width=2.2, first=True)

    # v16 — don't be afraid
    f_on, f_first = since(pos, 3, 16)
    if f_on:
        c.text((196, 232), "DON'T BE AFRAID, ZION", 13,
               HL if v == 16 else dim(TEXT, 0.92), "mm", bold=v == 16)
        c.text((196, 252), "don't let your hands be weak", 11,
               dim(TEXT_DIM, 0.95), "mm", italic=True)
        if f_first:
            c.pulse_rect(88, 218, 216, 48, dim(HL, 0.88), width=1.8,
                         first=True, rx=14)

    # v17 — the same centre, singing
    g_on, g_first = since(pos, 3, 17)
    if g_on:
        for i, (dx, dy, sz) in enumerate(((-116, -34, 20), (-84, -66, 15),
                                          (108, -30, 20), (78, -62, 15),
                                          (-142, 8, 15), (134, 4, 20))):
            nx, ny = CENTRE[0] + dx, CENTRE[1] + dy
            c.circle(nx, ny, sz * 0.24, fill=dim(GOLD, 0.9))
            c.line((nx + sz * 0.22, ny), (nx + sz * 0.22, ny - sz * 0.9),
                   dim(GOLD, 0.9), 1.8)
            c.path(f"M{nx + sz * 0.22},{ny - sz * 0.9} q{sz * 0.42},"
                   f"{sz * 0.10} {sz * 0.30},{sz * 0.42}",
                   stroke=dim(GOLD, 0.9), width=1.8)
        phrase(c, (512, 108), "HE WILL REJOICE OVER YOU WITH SINGING", 20,
               HL, first=g_first)

    # vv18-20 — brought in and gathered
    b_on, b_first = since(pos, 3, 18)
    if b_on:
        gy = 496
        c.line((110, gy), (952, gy), dim(SAND_DIM, 0.8), 1.4)
        figure(c, 156, gy, 58, dim(TEXT, 0.92), 2.0, arms="up")
        c.rect(130, gy - 118, 52, 30, fill=dim(PANEL, 0.9),
               stroke=dim(GRAY, 0.9), width=1.7)
        arrow(c, (156, gy - 126), (156, gy - 172), dim(GOLD, 0.9), 2.0, 8)
        c.text((156, gy - 194), "A BURDEN AND A REPROACH", 12.5,
               HL if v == 18 else dim(TEXT, 0.92), "mm", bold=v == 18)
        c.text((156, gy - 176), "removed", 11, dim(TEXT_DIM, 0.95), "mm",
               italic=True)
        if b_first:
            c.pulse_ellipse(156, gy - 96, 62, 74, dim(HL, 0.9), width=2,
                            first=True)
        lame_on, lame_first = since(pos, 3, 19)
        if lame_on:
            figure(c, 250, gy, 54, GOLD, 2.0, legs="kneel")
            c.text((250, gy + 26), "THOSE WHO ARE LAME — SAVED", 12,
                   HL if v == 19 else dim(TEXT, 0.92), "mm", bold=v == 19)
            for i, fx in enumerate((760, 812, 864)):
                figure(c, fx, gy, 50, dim(TEXT, 0.92), 1.9, legs="walk")
            arrow(c, (900, gy - 34), (700, gy - 34), dim(GOLD, 0.9), 2.1, 9)
            c.text((812, gy + 26), "THOSE DRIVEN AWAY — GATHERED", 12,
                   HL if v == 19 else dim(TEXT, 0.92), "mm", bold=v == 19)
            if lame_first:
                c.pulse_rect(196, gy - 62, 116, 74, dim(HL, 0.9),
                             width=2, first=True, rx=10)
        r_on, r_first = since(pos, 3, 20)
        if r_on:
            c.text((512, gy + 56), "A NAME AND A PRAISE AMONG ALL PEOPLES",
                   13.5, HL, "mm", bold=v == 20)
            if r_first:
                c.pulse_rect(280, gy + 40, 464, 32, dim(HL, 0.88),
                             width=1.9, first=True, rx=17)


# ---------------------------------------------------------------------------
# Assemble one verse
# ---------------------------------------------------------------------------

SCENES = {1: draw_ch1, 2: draw_ch2, 3: draw_ch3}


def render(ch, v):
    c = SvgCanvas(W, H, bg=BG)
    header(c, ch, v)
    SCENES[ch](c, v, P(ch, v))
    return c


def main():
    total = count = 0
    for ch in (1, 2, 3):
        for v in verse_numbers(BOOK, ch):
            out = out_path(BOOK, ch, f"{SLUG}_{ch}_{v}.svg")
            render(ch, v).save(out)
            total += os.path.getsize(out)
            count += 1
    print(f"Zephaniah: {count} SVG files, {total / 1e3:.0f} KB")


if __name__ == "__main__":
    main()
