"""Render the second epistle of Peter (3 chapters, 61 verses) as per-verse
vector SVGs — one full-frame scene per passage, three geometries for three
chapters (see docs/design/short-books.md).

  ch1  The ladder of 1:5-7 — eight rungs added a clause at a time — with a
       sight gauge on the right, because the charge in v9 against the man who
       lacks them is that he "cannot see afar off". What he cannot see is the
       entrance of v11, drawn at the far end of that same horizon, so the two
       verses share one drawing. Then the tent Peter is about to put off set
       against the mount that stands, and the three light sources of v19 in
       the order the verse gives them: lamp, dawn, day star — fed by the
       source diagram of vv20-21, two paths struck and one live.
  ch2  Three judgment precedents on one rail, each carrying the count that
       came out of it (0, 8, 1); the withheld accusation of v11 drawn as a
       power comparison; Balaam's fork; and the proverbs of v22 drawn as a
       loop, so the last frame returns to the first.
  ch3  The scoffers' unbroken line (v4) broken into three worlds by water and
       fire; the two rulers of v8 at true relative length, with v9's reason
       for the long one drawn on it; and the ladder of chapter 1 returning at
       3:18 with one more rung.

Threads across the chapters, so the book reads as one set: the flood of 2:5
and 3:6 are drawn with the same water level; the spots and blemishes of 2:13
return cleaned at 3:14; the ladder of 1:5 returns at 3:18; the fall warned
off at 1:10 is the fall warned off at 3:17.

Text budget: names, numbers and labelled parts, plus short engraved phrases
(2-7 words, WEB wording) at hinge verses only. Nothing counts the verses — no
track, no dots, no per-verse caption. What changes each verse is the drawing.

Run inside the project venv:
    .venv\\Scripts\\python.exe generate_2peter_svg.py
"""

import math
import os

import svg_figures as F
from svg_surface import SvgCanvas
# `figure` and `beast` are drawn from svg_figures below, with the signatures
# svg_vocab gave them. With this book converted nothing draws svg_vocab's
# stick creatures any more; its measuring and marking helpers below are what
# it is now for.
from svg_vocab import (dim, mix, text_w, reading_position, arrow, cross,
                       struck, tick_row, hatch)
from passages import verse_numbers
from generate_tabernacle import (W, H, BG, PANEL, SAND, SAND_DIM, TEXT,
                                 TEXT_DIM, HL, GOLD, RED, BROWN, GRAY,
                                 SILVER, out_path)

BOOK = "2 Peter"
SLUG = BOOK.replace(" ", "_")

# Colours this book needs that the tabernacle palette has no name for.
WATER = (96, 122, 152)          # the flood of 2:5 and 3:6
FIRE = (216, 124, 58)           # the boundary of 3:7, 3:10, 3:12
NIGHT = (22, 22, 34)            # the dark place of 1:19, the night of 3:10
DAWN = (168, 138, 102)          # the day dawning of 1:19
ASH = (110, 106, 100)           # Sodom and Gomorrha turned into ashes
MIRE = (78, 66, 52)             # the wallowing of 2:22


# ---------------------------------------------------------------------------
# Reading position and page furniture
# ---------------------------------------------------------------------------

CH_LEN = {1: 21, 2: 22, 3: 18}
P, since = reading_position(CH_LEN)


# ---------------------------------------------------------------------------
# The people and the creatures
# ---------------------------------------------------------------------------
#
# Drawn from svg_figures. The signatures are the stick marks' own, so nothing
# in this file moved: `figure` still takes a height and stands on `gy`,
# `beast` still takes a LENGTH. What `beast` no longer does is stand for
# every animal at once — chapter 2 names three, and the whole force of 2:22
# is that the dog and the sow are two different creatures doing the same
# thing, which one silhouette used twice cannot say. `kind` is passed at every
# call site and never inferred from a nearby label.

MAN_UNITS = F.bbox((F.man(), 0))[3] - F.bbox((F.man(), 0))[2]

_KINDS = {"dog": F.dog, "sow": F.sow, "donkey": F.donkey, "sheep": F.sheep,
          "ox": F.ox, "lion": F.lion, "wolf": F.wolf}
_paint_cache = {}


def _fade(col, a):
    if col is None or a >= 1.0:
        return col
    had = (col[3] / 255.0) if len(col) > 3 else 1.0
    return (col[0], col[1], col[2], int(255 * had * a))


def paint(col, width):
    """The vocabulary's paint table in this scene's colour and opacity. The
    book pushes whole figures back by dimming them — the crowd behind the
    ladder, the grey fallen of 2:4 — and a table built from the RGB alone
    would bring them all forward to full strength."""
    key = (tuple(col), width)
    if key not in _paint_cache:
        a = (col[3] / 255.0) if len(col) > 3 else 1.0
        k = width / 1.9
        _paint_cache[key] = {
            m: (_fade(f, a), _fade(s, a), w * k)
            for m, (f, s, w) in F.palette(tuple(col[:3]), BG).items()}
    return _paint_cache[key]


def put(c, parts, x, gy, s, col, width=1.9, flip=1):
    F.draw(c, parts, x, gy, s, col, BG, flip=flip, style=paint(col, width))


def fit(parts, w=None, h=None):
    x0, x1, y0, y1 = F.bbox((parts, 0))
    return w / (x1 - x0) if w is not None else h / (y1 - y0)


def figure(c, x, gy, h, col, width=2, arms="down", legs="stand", lean=0.0,
           kind="man"):
    """A person standing on `gy`, `h` tall. `legs="fall"` has no drawn pose
    and comes out kneeling — the nearest posture the vocabulary has, and the
    scene that used it (2:4, the angels cast down) already carries the fall
    in the arrow above it."""
    pose = {"walk": "walk", "kneel": "kneel", "fall": "kneel"}.get(legs,
                                                                  "stand")
    parts = {"woman": F.woman, "child": F.child}.get(kind, F.man)(
        pose=pose, arms=arms)
    put(c, parts, x + lean * h, gy, h / MAN_UNITS, col, width)


def beast(c, x, gy, ln, col, width=1.8, head_low=False, tail=True,
          kind="sheep", flip=1):
    """A four-footed animal standing on `gy`, `ln` long. `head_low` and
    `tail` are accepted and ignored: each drawn creature carries its own head
    and its own tail, and a pig with its head up would be a different animal
    rather than a flag on this one."""
    parts = _KINDS[kind]()
    put(c, parts, x, gy, fit(parts, w=ln), col, width, flip=flip)


def header(c, ch, v):
    c.text((28, 24), f"2 Peter {ch}", 23, TEXT, "la", bold=True)
    c.text((28, 54), f"v{v}", 13, dim(TEXT_DIM, 0.85), "la", italic=True)


def phrase(c, xy, s, size=22, col=None, first=False):
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
# The ladder — 1:5-7, and again at 3:18
# ---------------------------------------------------------------------------
#
# Eight rungs, each added on the clause that names it. The same geometry
# function draws the big lettered ladder of chapter 1 and the small one that
# closes the letter, so 3:18's "grow in grace" is visibly one more rung on
# the ladder the book opened with.

RUNGS = [("FAITH", 1), ("MORAL EXCELLENCE", 5), ("KNOWLEDGE", 5),
         ("SELF-CONTROL", 6), ("PERSEVERANCE", 6), ("GODLINESS", 6),
         ("BROTHERLY AFFECTION", 7), ("LOVE", 7)]

# (x_bot, y_bot, x_top, y_top, half_bot, half_top)
LADDER_1 = (258, 498, 326, 150, 86, 68)
LADDER_3 = (884, 546, 906, 286, 44, 36)


def rung_at(geo, i, n=8):
    """(centre x, y, half width) of rung i — 0 is the foot."""
    xb, yb, xt, yt, hb, ht = geo
    t = 0.06 + i * (0.86 / (n - 1))
    return xb + (xt - xb) * t, yb + (yt - yb) * t, hb + (ht - hb) * t


def draw_ladder(c, geo, shown, fresh=(), labels=True, size=14.5,
                extra=None, rail=None, lit=None):
    """`shown` rungs are up; `fresh` are the indices that landed this verse
    (pulsed once). `extra` draws an unfinished rung above the top."""
    xb, yb, xt, yt, hb, ht = geo
    rail = rail or dim(SAND, 0.95)
    lit = lit or GOLD
    c.line((xb - hb, yb), (xt - ht, yt), rail, 2.6)
    c.line((xb + hb, yb), (xt + ht, yt), rail, 2.6)
    for i in range(min(shown, len(RUNGS))):
        cx, cy, half = rung_at(geo, i)
        hot = i in fresh
        c.line((cx - half, cy), (cx + half, cy),
               HL if hot else lit, 3.2 if hot else 2.4)
        if hot:
            c.pulse_rect(cx - half - 7, cy - 11, 2 * half + 14, 22,
                         dim(HL, 0.9), width=1.8, first=True, rx=11)
        if labels:
            c.text((cx + half + 20, cy), RUNGS[i][0], size,
                   HL if hot else dim(TEXT, 0.92), "lm", bold=hot)
    if extra is not None:
        cx, cy, half = rung_at(geo, 8)
        c.line((cx - half, cy), (cx + half, cy), dim(HL, 0.85), 2.6,
               dash="6,5")
        # the rails carry on past the last finished rung
        c.line((cx - half - 6, cy + 26), (cx - half - 2, cy - 18),
               dim(SAND_DIM, 0.9), 2)
        c.line((cx + half + 6, cy + 26), (cx + half + 2, cy - 18),
               dim(SAND_DIM, 0.9), 2)
        c.text((cx, cy - 26), extra, size, HL, "mm", bold=True)


# ---------------------------------------------------------------------------
# The flood — 2:5 and 3:6 draw the same water at the same level
# ---------------------------------------------------------------------------

# The height the water reaches in both places the flood is drawn. Short of
# the top of its box on purpose: a box filled edge to edge reads as a blue
# rectangle, not as a drowned world with an ark riding on it.
FLOOD_LEVEL = 0.78


def flood(c, x0, y0, x1, y1, level, ark=True, label=None):
    """A land strip under a rising water band. `level` in [0,1] is the water's
    height up the box: 0 dry land, 1 the world that then was, overflowed."""
    gy = y1 - (y1 - y0) * 0.30
    # hills
    hills = [(x0, gy)]
    span = x1 - x0
    for i in range(1, 8):
        t = i / 8
        hills.append((x0 + span * t,
                      gy - (14 + 9 * math.sin(t * 5.2)) * (1 - level * 0.2)))
    hills.append((x1, gy))
    c.polyline(hills, dim(BROWN, 0.95), 1.8)
    c.line((x0, y1), (x1, y1), dim(SAND_DIM, 0.9), 1.4)
    if level > 0:
        wy = y1 - (y1 - y0) * (0.30 + 0.58 * level)
        c.rect(x0, wy, x1 - x0, y1 - wy, fill=dim(WATER, 0.55))
        c.line((x0, wy), (x1, wy), dim(WATER, 1.0), 2.2)
        for k in range(3):
            yy = wy + 12 + k * 13
            if yy < y1 - 4:
                c.line((x0 + 10 + 7 * k, yy), (x1 - 12 - 5 * k, yy),
                       dim(WATER, 0.5), 1.2, dash="9,11")
        if ark:
            ax = (x0 + x1) / 2
            aw = (x1 - x0) * 0.26
            c.polygon([(ax - aw / 2, wy - 4), (ax + aw / 2, wy - 4),
                       (ax + aw / 2 - 6, wy - 22), (ax - aw / 2 + 6, wy - 22)],
                      stroke=dim(SAND, 0.95), width=1.8)
            c.line((ax - aw / 2 + 4, wy - 22), (ax + aw / 2 - 4, wy - 22),
                   dim(SAND, 0.95), 1.6)
    if label:
        c.text(((x0 + x1) / 2, y1 + 16), label, 11.5,
               dim(TEXT_DIM, 0.95), "mm", italic=True)


# ---------------------------------------------------------------------------
# The spots and blemishes — 2:13, cleaned at 3:14
# ---------------------------------------------------------------------------

SPOTS = [(-0.32, -0.18, 7), (-0.05, 0.22, 5.5), (0.26, -0.24, 6),
         (0.38, 0.16, 4.5), (0.02, -0.30, 4), (-0.24, 0.30, 5)]


def spot_panel(c, cx, cy, w, h, col, opacity, lift=False):
    """The cloth of 2:13 — the same six blots both times it is drawn."""
    c.rect(cx - w / 2, cy - h / 2, w, h, fill=dim(PANEL, 0.85),
           stroke=dim(SAND, 0.9), width=1.8, rx=6)
    for dx, dy, r in SPOTS:
        sx, sy = cx + dx * w, cy + dy * h
        c.circle(sx, sy, r, fill=dim(col, opacity))
        if lift:
            arrow(c, (sx, sy - r - 4), (sx, sy - r - 18), dim(HL, 0.75),
                  1.4, head=5)


# ---------------------------------------------------------------------------
# Chapter 1 — the ladder, the tent and the mount, the light
# ---------------------------------------------------------------------------

def draw_ch1(c, v, pos):
    if v <= 11:
        _ch1_ladder(c, v, pos)
    elif v <= 18:
        _ch1_tent_and_mount(c, v, pos)
    else:
        _ch1_light(c, v, pos)


def _ch1_ladder(c, v, pos):
    gy = 498
    # v3 — the divine power resting on the whole climb
    dp_on, dp_first = since(pos, 1, 3)
    if dp_on:
        # rays rather than a filled wedge — a wedge dark enough to read as
        # light is also dark enough to swallow the ladder behind it
        c.grown([(140, 88), (180, 88), (412, gy + 4), (116, gy + 4)],
                GOLD, 0.008, 0.035)
        for tx in (170, 232, 296, 356, 408):
            c.line((158, 90), (tx, gy + 4), dim(GOLD, 0.20), 1.3)
        c.text((172, 74), "DIVINE POWER", 13, dim(GOLD, 0.95), "mm",
               bold=v == 3)
        if v <= 4:
            c.text((512, 108), "ALL THINGS FOR LIFE AND GODLINESS", 15,
                   HL if v == 3 else dim(TEXT, 0.85), "mm", bold=v == 3)

    # v4 — the corruption stepped out of, and the plinth stepped onto
    esc_on, esc_first = since(pos, 1, 4)
    if esc_on:
        hatch(c, 62, gy + 6, 156, gy + 52, dim(GRAY, 0.5), step=11)
        c.rect(62, gy + 6, 94, 46, stroke=dim(GRAY, 0.75), width=1.4)
        c.text((109, gy + 66), "CORRUPTION", 11.5, dim(GRAY, 0.95), "mm")
        figure(c, 140, gy + 4, 40, dim(TEXT_DIM, 0.9), 1.8, arms="point_r",
               legs="walk")
    plinth_on, _ = since(pos, 1, 4)
    if plinth_on:
        c.rect(158, gy, 208, 22, fill=dim(PANEL, 0.95),
               stroke=dim(SAND, 0.95), width=1.8)
        c.text((262, gy + 38), "PRECIOUS PROMISES", 13,
               HL if v == 4 else dim(TEXT, 0.9), "mm", bold=v == 4)
        if esc_first:
            c.pulse_rect(158, gy, 208, 22, dim(HL, 0.9), width=2, first=True)
    else:
        c.line((158, gy), (366, gy), dim(SAND_DIM, 0.9), 1.6)

    # v2 — grace and peace multiplied
    if v <= 4:
        gp_on, gp_first = since(pos, 1, 2)
        if gp_on:
            c.text((880, 108), "GRACE", 14, dim(TEXT, 0.9), "mm",
                   bold=v == 2)
            c.text((934, 108), "×", 15, dim(GOLD, 0.9), "mm")
            c.text((980, 108), "PEACE", 14, dim(TEXT, 0.9), "mm",
                   bold=v == 2)
            c.text((930, 130), "MULTIPLIED", 11.5, dim(TEXT_DIM, 0.95),
                   "mm", italic=True)
            if gp_first:
                c.pulse_rect(842, 92, 176, 50, dim(HL, 0.85), width=1.8,
                             first=True, rx=14)

    # the ladder itself
    up, fresh = 0, []
    for i, (_word, vv) in enumerate(RUNGS):
        on, first = since(pos, 1, vv)
        if on:
            up = i + 1
            if first:
                fresh.append(i)
    draw_ladder(c, LADDER_1, up, fresh)

    # v8 — fruit on the rungs
    fr_on, fr_first = since(pos, 1, 8)
    if fr_on:
        for i in (1, 3, 5, 6):
            cx, cy, half = rung_at(LADDER_1, i)
            c.circle(cx - half - 9, cy + 9, 4.2, fill=dim(GOLD, 0.9))
        cx, cy, half = rung_at(LADDER_1, 4)
        c.text((cx - half - 22, cy + 26), "FRUITFUL", 12,
               HL if v == 8 else dim(TEXT_DIM, 0.95), "rm", bold=v == 8)

    # v10 — the footing that does not slip
    nf_on, nf_first = since(pos, 1, 10)
    if nf_on:
        for fx in (172, 344):
            c.polygon([(fx - 15, gy), (fx + 15, gy), (fx + 9, gy - 13),
                       (fx - 9, gy - 13)], fill=dim(GOLD, 0.30),
                      stroke=dim(GOLD, 0.95), width=1.8)
        c.text((430, 76), "WILL NEVER STUMBLE", 15,
               HL if v == 10 else dim(TEXT, 0.9), "mm", bold=v == 10)
        if nf_first:
            c.pulse_rect(150, gy - 20, 224, 30, dim(HL, 0.9), width=2,
                         first=True, rx=14)

    # ---- the sight gauge: the horizon the ladder lets you see ----
    hz = 250
    c.line((600, hz), (996, hz), dim(SAND_DIM, 0.75), 1.4)
    for x in (656, 742, 828, 914):
        c.line((x, hz), (x, hz - 5), dim(SAND_DIM, 0.6), 1.2)

    # the entrance at the far end — v11 lights what v9 could not see
    gate_x, gate_w, gate_h = 916, 50, 62
    ent_on, ent_first = since(pos, 1, 11)
    gcol = GOLD if ent_on else dim(SAND_DIM, 0.9)
    c.line((gate_x - gate_w / 2, hz), (gate_x - gate_w / 2, hz - gate_h),
           gcol, 2.4)
    c.line((gate_x + gate_w / 2, hz), (gate_x + gate_w / 2, hz - gate_h),
           gcol, 2.4)
    c.path(f"M{gate_x - gate_w / 2},{hz - gate_h} "
           f"A{gate_w / 2},{gate_h * 0.46} 0 0 1 "
           f"{gate_x + gate_w / 2},{hz - gate_h}", stroke=gcol, width=2.4)
    if ent_on:
        c.polygon([(gate_x - gate_w / 2 + 4, hz),
                   (gate_x + gate_w / 2 - 4, hz),
                   (gate_x + gate_w / 2 + 20, hz + 44),
                   (gate_x - gate_w / 2 - 20, hz + 44)],
                  fill=dim(GOLD, 0.14))
        if ent_first:
            c.pulse_ellipse(gate_x, hz - gate_h * 0.42, 44, 52,
                            dim(HL, 0.9), width=2, first=True)
    c.text((gate_x, hz + 62), "THE ETERNAL", 12,
           HL if ent_on else dim(TEXT_DIM, 0.9), "mm", bold=v == 11)
    c.text((gate_x, hz + 80), "KINGDOM", 12,
           HL if ent_on else dim(TEXT_DIM, 0.9), "mm", bold=v == 11)
    if v == 11:
        c.text((760, 118), "RICHLY SUPPLIED WITH THE ENTRANCE", 15, HL, "mm",
               bold=True)

    # v9 — the two ranges of sight
    see_on, see_first = since(pos, 1, 9)
    if see_on:
        top_x, top_y, top_h = rung_at(LADDER_1, 7)
        c.line((top_x + top_h + 4, top_y + 4), (gate_x - 34, hz - 22),
               dim(GOLD, 0.65), 1.6, dash="7,7")
        c.text((640, 196), "FAR", 12.5,
               HL if v == 9 else dim(TEXT, 0.85), "lm", bold=v == 9)
        bgy = 470
        c.line((600, bgy), (860, bgy), dim(SAND_DIM, 0.7), 1.3)
        figure(c, 648, bgy, 52, dim(GRAY, 0.95), 1.9, arms="down")
        c.line((648 - 9, bgy - 44), (648 + 9, bgy - 44), dim(GRAY, 0.95), 2.2)
        c.line((664, bgy - 44), (742, bgy - 50), dim(GRAY, 0.8), 1.6,
               dash="6,6")
        cross(c, 756, bgy - 51, 8, dim(RED, 0.95), 2.2)
        c.text((700, bgy + 30), "BLIND — SEEING ONLY WHAT IS NEAR", 12.5,
               dim(RED, 0.95) if v == 9 else dim(TEXT_DIM, 0.95), "mm",
               bold=v == 9)
        if see_first:
            c.pulse_ellipse(700, bgy - 30, 92, 52, dim(RED, 0.8), width=1.8,
                            first=True)

    # v1 — the base of the whole climb
    if v == 1:
        phrase(c, (700, 380), "LIKE PRECIOUS FAITH", 21, HL, first=True)
    if v in (5, 6, 7):
        c.text((700, 380), "ADD TO YOUR FAITH", 16, dim(TEXT, 0.85), "mm",
               italic=True)


def _ch1_tent_and_mount(c, v, pos):
    gy = 470
    c.line((90, gy), (984, gy), dim(SAND_DIM, 0.8), 1.5)

    # ---- the tabernacle Peter is shortly to put off ----
    tx, apex = 250, 342
    struck_on, struck_first = since(pos, 1, 14)
    gone_on, gone_first = since(pos, 1, 15)
    tcol = dim(SAND, 0.30) if gone_on else dim(SAND, 0.95)
    ap_x = apex_x = tx + (26 if struck_on else 0)
    ap_y = apex + (22 if struck_on else 0)
    c.polyline([(tx - 82, gy), (ap_x, ap_y), (tx + 82, gy)], tcol, 2.4,
               dash="6,6" if gone_on else None)
    c.line((tx - 82, gy), (tx + 82, gy), tcol, 2.0)
    c.polyline([(ap_x, ap_y), (ap_x - 6, gy)], tcol, 1.6)
    # door flap
    c.polyline([(tx + 6, gy), (tx + 20, gy - 46), (tx + 30, gy)], tcol, 1.6)
    # v13 — still in it: the pegs driven, and Peter at the door
    dwell_on, dwell_first = since(pos, 1, 13)
    if dwell_on and not gone_on:
        figure(c, tx + 46, gy, 44, dim(GOLD, 0.95), 1.9)
        if dwell_first:
            c.pulse_ellipse(tx, gy - 24, 116, 40, dim(HL, 0.9), width=1.9,
                            first=True)
    # guy ropes — the right one released at v14
    c.line((ap_x, ap_y), (tx - 128, gy), tcol, 1.4)
    if struck_on:
        c.path(f"M{ap_x},{ap_y} Q{tx + 118},{gy - 26} {tx + 108},{gy}",
               stroke=dim(RED, 0.75), width=1.4)
    else:
        c.line((ap_x, ap_y), (tx + 128, gy), tcol, 1.4)
    for px in (tx - 128, tx + 128):
        c.line((px, gy - 8), (px, gy + 8), tcol, 1.8)

    c.text((tx, gy + 34), "THIS TENT", 14,
           dim(TEXT, 0.55) if gone_on else
           (HL if v in (13, 14) else dim(TEXT, 0.92)), "mm",
           bold=v in (13, 14))
    if v == 12:
        c.text((tx, 150), "TO REMIND YOU", 15, HL, "mm", bold=True)
        arrow(c, (tx + 96, 176), (tx + 168, 176), dim(GOLD, 0.7), 1.6, 7)
        c.pulse_rect(tx - 88, 132, 176, 36, dim(HL, 0.85), width=1.8,
                     first=True, rx=17)
    if struck_on:
        c.text((tx, gy + 56), "THE PUTTING OFF COMES SWIFTLY", 12.5,
               dim(RED, 0.95) if v == 14 else dim(TEXT_DIM, 0.95), "mm",
               bold=v == 14)
        if struck_first:
            c.pulse_ellipse(tx + 10, gy - 68, 118, 82, dim(RED, 0.8),
                            width=1.8, first=True)
    if gone_on:
        # what is left standing after the decease
        c.rect(tx - 22, gy - 76, 44, 76, fill=dim(PANEL, 0.95),
               stroke=dim(SAND, 0.95), width=2, rx=4)
        c.path(f"M{tx - 22},{gy - 76} A22,22 0 0 1 {tx + 22},{gy - 76}",
               stroke=dim(SAND, 0.95), width=2)
        c.text((tx, gy - 40), "REMEMBER", 10.5, dim(TEXT, 0.9), "mm")
        c.text((tx, gy - 22), "AFTER MY", 9.5, dim(TEXT_DIM, 0.95), "mm")
        c.text((tx, gy - 10), "DEPARTURE", 9.5, dim(TEXT_DIM, 0.95), "mm")
        if gone_first:
            c.pulse_rect(tx - 30, gy - 100, 60, 104, dim(HL, 0.9), width=2,
                         first=True, rx=8)

    # ---- the mount that stands ----
    c.polyline([(560, gy), (700, 262), (820, 262), (960, gy)],
               dim(SAND, 0.95), 2.4)
    c.line((700, 262), (820, 262), dim(SAND, 0.95), 2.0)
    for xx, yy in ((640, 356), (886, 366)):
        c.line((xx, yy), (xx + 26, yy - 44), dim(SAND_DIM, 0.8), 1.2)
    c.text((760, gy + 34), "THE HOLY MOUNTAIN", 14,
           HL if v == 18 else dim(TEXT, 0.92), "mm", bold=v == 18)

    fab_on, fab_first = since(pos, 1, 16)
    if fab_on:
        struck(c, (452, 212), "CUNNINGLY DEVISED FABLES", 13.5,
               dim(TEXT_DIM, 0.95), dim(RED, 0.95))
        if fab_first:
            fw = text_w("CUNNINGLY DEVISED FABLES", 13.5)
            c.pulse_rect(452 - fw / 2 - 14, 194, fw + 28, 36,
                         dim(RED, 0.8), width=1.8, first=True, rx=18)

    voice_on, voice_first = since(pos, 1, 17)
    heard_on, heard_first = since(pos, 1, 18)
    if voice_on:
        # the excellent glory, and the voice that came out of it
        for r, a in ((52, 0.10), (38, 0.16), (24, 0.30)):
            c.circle(760, 138, r, fill=dim(GOLD, a))
        c.circle(760, 138, 15, fill=dim(HL, 0.95))
        for k in range(12):
            ang = k * math.pi / 6
            c.line((760 + 22 * math.cos(ang), 138 + 22 * math.sin(ang)),
                   (760 + 34 * math.cos(ang), 138 + 34 * math.sin(ang)),
                   dim(GOLD, 0.7), 1.4)
        c.text((868, 138), "THE MAJESTIC GLORY", 12,
               dim(TEXT_DIM, 0.95), "lm", italic=True)
        phrase(c, (512, 74), "THIS IS MY BELOVED SON", 21, HL,
               first=voice_first)

    # the three on the plateau
    if fab_on:
        for i, fx in enumerate((722, 760, 798)):
            figure(c, fx, 262, 46, GOLD if heard_on else dim(TEXT, 0.9),
                   2, arms="up" if (heard_on and i == 1) else "down")
        c.text((760, 300), "EYEWITNESSES", 13,
               HL if v in (16, 18) else dim(TEXT, 0.9), "mm",
               bold=v in (16, 18))
    if voice_on:
        c.path("M760,168 Q744,208 760,232", stroke=dim(GOLD, 0.85), width=2.2)
    if heard_on:
        for fx in (722, 798):
            c.path(f"M760,176 Q{(760 + fx) / 2},214 {fx},234",
                   stroke=dim(GOLD, 0.55), width=1.6)
        if heard_first:
            c.pulse_ellipse(760, 250, 74, 40, dim(HL, 0.9), width=2,
                            first=True)


def _ch1_light(c, v, pos):
    # ---- the sky: dark on the left, dawning to the right ----
    sky0, sky1, hz = 96, 330, 330
    for i in range(18):
        t = i / 17
        c.rect(80 + i * (904 / 18), sky0, 904 / 18 + 1, sky1 - sky0,
               fill=mix(NIGHT, DAWN, t ** 1.7))
    c.line((80, hz), (984, hz), dim(SAND, 0.9), 1.8)

    # the lamp in the dark place — which is the scripture of vv20-21
    lx = 224
    c.ellipse(lx, hz - 6, 78, 22, fill=dim(GOLD, 0.13))
    c.polygon([(lx - 30, hz), (lx + 30, hz), (lx + 22, hz - 20),
               (lx - 22, hz - 20)], fill=dim(PANEL, 0.95),
              stroke=dim(SAND, 0.95), width=1.8)
    c.line((lx + 30, hz - 6), (lx + 44, hz - 4), dim(SAND, 0.95), 1.8)
    c.path(f"M{lx + 40},{hz - 8} Q{lx + 46},{hz - 26} {lx + 38},{hz - 34} "
           f"Q{lx + 52},{hz - 26} {lx + 40},{hz - 8}",
           fill=dim(GOLD, 0.9))
    c.text((lx, hz + 26), "THE MORE SURE WORD", 13.5,
           HL if v == 19 else dim(TEXT, 0.92), "mm", bold=v == 19)

    # the day dawning
    for r, a in ((116, 0.07), (86, 0.10), (56, 0.15)):
        c.path(f"M{600 - r},{hz} A{r},{r} 0 0 1 {600 + r},{hz}",
               fill=dim(DAWN, a))
    c.path(f"M{600 - 56},{hz} A56,56 0 0 1 {600 + 56},{hz}",
           stroke=dim(GOLD, 0.55), width=1.6)
    c.text((600, hz + 26), "UNTIL THE DAY DAWNS", 13.5,
           HL if v == 19 else dim(TEXT, 0.92), "mm", bold=v == 19)

    # the day star arising
    sx, sy = 852, 196
    for k in range(8):
        ang = k * math.pi / 4
        ln = 26 if k % 2 == 0 else 13
        c.line((sx, sy), (sx + ln * math.cos(ang), sy + ln * math.sin(ang)),
               dim(HL, 0.95), 2.2)
    c.circle(sx, sy, 7, fill=HL)
    arrow(c, (sx, sy + 74), (sx, sy + 42), dim(GOLD, 0.7), 1.6, 7)
    c.text((sx, hz + 26), "THE MORNING STAR", 13.5,
           HL if v == 19 else dim(TEXT, 0.92), "mm", bold=v == 19)
    if since(pos, 1, 19)[1]:
        c.pulse_rect(80, 96, 904, 234, dim(HL, 0.85), width=2, first=True)

    # ---- where the sure word came from: two paths struck, one live ----
    scroll_on = True
    sxx, syy = 264, 470
    c.rect(sxx - 82, syy - 26, 164, 52, fill=dim(PANEL, 0.95),
           stroke=dim(SAND, 0.95), width=1.8, rx=4)
    for ex in (sxx - 82, sxx + 82):
        c.ellipse(ex, syy, 9, 28, fill=dim(PANEL, 0.98),
                  stroke=dim(SAND, 0.95), width=1.8)
    for k in range(3):
        c.line((sxx - 56, syy - 12 + k * 12), (sxx + 56, syy - 12 + k * 12),
               dim(TEXT_DIM, 0.7), 1.2)
    c.text((sxx, syy + 46), "SCRIPTURE", 13, dim(TEXT, 0.92), "mm")
    if scroll_on:
        arrow(c, (sxx - 20, syy - 32), (lx - 4, hz + 46), dim(GOLD, 0.75),
              1.8, 8, dash="6,6")

    pi_on, pi_first = since(pos, 1, 20)
    if pi_on:
        struck(c, (620, 424), "PRIVATE INTERPRETATION", 13.5,
               dim(TEXT_DIM, 0.95), dim(RED, 0.95))
        arrow(c, (500, 430), (348, 452), dim(TEXT_DIM, 0.6), 1.6, 7,
              dash="5,6")
        cross(c, 424, 441, 9, dim(RED, 0.95), 2.2)
        if pi_first:
            c.pulse_ellipse(424, 441, 22, 20, dim(RED, 0.85), width=1.8,
                            first=True)
    wm_on, wm_first = since(pos, 1, 21)
    if wm_on:
        struck(c, (600, 478), "THE WILL OF MAN", 13.5,
               dim(TEXT_DIM, 0.95), dim(RED, 0.95))
        arrow(c, (528, 480), (348, 474), dim(TEXT_DIM, 0.6), 1.6, 7,
              dash="5,6")
        cross(c, 438, 477, 9, dim(RED, 0.95), 2.2)
        # the live path
        c.text((776, 530), "THE HOLY SPIRIT", 13.5, HL, "mm", bold=v == 21)
        c.text((478, 530), "HOLY MEN", 13.5, dim(TEXT, 0.95), "mm",
               bold=v == 21)
        arrow(c, (696, 530), (534, 530), dim(GOLD, 0.9), 2.0, 8)
        arrow(c, (424, 528), (350, 500), dim(GOLD, 0.9), 2.0, 8)
        if wm_first:
            c.pulse_rect(430, 512, 400, 36, dim(HL, 0.85), width=1.8,
                         first=True, rx=18)


# ---------------------------------------------------------------------------
# Chapter 2 — the intrusion, the precedents, the beasts, Balaam, the loop
# ---------------------------------------------------------------------------

def draw_ch2(c, v, pos):
    if v <= 3:
        _ch2_folds(c, v, pos)
    elif v <= 9:
        _ch2_precedents(c, v, pos)
    elif v <= 14:
        _ch2_beasts(c, v, pos)
    elif v <= 16:
        _ch2_balaam(c, v, pos)
    elif v <= 18:
        _ch2_wells(c, v, pos)
    elif v == 19:
        _ch2_bondage(c, v, pos)
    else:
        _ch2_loop(c, v, pos)


def _ch2_folds(c, v, pos):
    cy, ry, rx = 286, 82, 122

    def fold(cx, label, intruder_label, now):
        # the enclosure, open at the back where they came in privily
        c.path(f"M{cx - rx * 0.72},{cy + ry * 0.70} "
               f"A{rx},{ry} 0 1 1 {cx - rx * 0.30},{cy + ry * 0.94}",
               stroke=dim(SAND, 0.95), width=2.2)
        c.text((cx, cy - ry - 34), label, 14, dim(TEXT, 0.92), "mm",
               bold=v == 1)
        for i, (dx, dy) in enumerate(((-52, 16), (-8, -22), (34, 22),
                                      (58, -14))):
            figure(c, cx + dx, cy + dy + 20, 34, dim(TEXT_DIM, 0.95), 1.6)
        # the one that came in, and the path he took
        c.path(f"M{cx - rx - 52},{cy + ry * 1.16} "
               f"Q{cx - rx * 0.72},{cy + ry * 0.80} {cx - 84},{cy + 44}",
               stroke=dim(RED, 0.75), width=1.6)
        figure(c, cx - 84, cy + 44, 40, dim(RED, 0.95), 2.0, arms="open")
        c.text((cx - rx - 44, cy + ry * 1.16 + 18), "secretly", 11.5,
               dim(RED, 0.9), "mm", italic=True)
        c.text((cx, cy + ry + 30), intruder_label, 14, dim(RED, 0.95), "mm",
               bold=v == 1)
        if now:
            # bought — and the mark denied
            c.rect(cx + 24, cy - 8, 56, 26, fill=dim(PANEL, 0.95),
                   stroke=dim(GOLD, 0.9), width=1.6, rx=3)
            c.text((cx + 52, cy + 5), "BOUGHT", 10.5, dim(GOLD, 0.95), "mm")
            c.line((cx + 18, cy + 22), (cx + 86, cy - 14), dim(RED, 0.95), 2.4)
            arrow(c, (cx - 84, cy + 62), (cx - 84, cy + 116),
                  dim(RED, 0.9), 2.0, 8)
            c.text((cx - 84, cy + 136), "SWIFT DESTRUCTION", 12,
                   dim(RED, 0.95), "mm", bold=v == 1)

    on1, first1 = since(pos, 2, 1)
    if on1:
        fold(268, "AMONG THE PEOPLE", "FALSE PROPHETS", False)
        fold(640, "AMONG YOU", "FALSE TEACHERS", True)
        arrow(c, (410, cy), (500, cy), dim(SAND_DIM, 0.9), 1.8, 8)
        phrase(c, (512, 96), "DENYING THE MASTER WHO BOUGHT THEM", 20,
               dim(RED, 1.0), first=first1)

    # v2 — the way of truth, and its name defaced
    way_on, way_first = since(pos, 2, 2)
    if way_on:
        c.line((766, cy - 16), (992, cy - 16), dim(SAND, 0.9), 1.8)
        c.line((766, cy + 16), (992, cy + 16), dim(SAND, 0.9), 1.8)
        for i in range(3):
            figure(c, 800 + i * 42, cy + 14, 30, dim(TEXT_DIM, 0.95), 1.5,
                   legs="walk")
        c.rect(838, cy - 62, 130, 32, fill=dim(PANEL, 0.95),
               stroke=dim(SAND, 0.9), width=1.6, rx=3)
        c.text((903, cy - 46), "THE WAY OF THE TRUTH", 11.5, dim(TEXT, 0.92),
               "mm")
        c.line((844, cy - 34), (962, cy - 58), dim(RED, 0.95), 2.4)
        c.line((844, cy - 58), (962, cy - 34), dim(RED, 0.95), 2.4)
        c.text((903, cy - 78), "MALIGNED", 12,
               dim(RED, 0.95) if v == 2 else dim(TEXT_DIM, 0.95), "mm",
               bold=v == 2)
        if way_first:
            c.pulse_rect(834, cy - 66, 138, 40, dim(RED, 0.85), width=1.8,
                         first=True, rx=6)

    # v3 — made merchandise, and the judgment that does not slumber
    mer_on, mer_first = since(pos, 2, 3)
    if mer_on:
        bx, by = 268, 470
        c.line((bx, by - 34), (bx, by + 52), dim(SAND, 0.95), 2.2)
        c.line((bx - 92, by - 30), (bx + 92, by - 22), dim(SAND, 0.95), 2.2)
        c.line((bx + 92, by + 52), (bx - 92, by + 52), dim(SAND_DIM, 0.8), 1.4)
        for sx, sy, dp in ((bx - 92, by - 30, 26), (bx + 92, by - 22, 22)):
            c.path(f"M{sx - 30},{sy + dp} A30,{dp} 0 0 0 {sx + 30},{sy + dp}",
                   stroke=dim(SAND, 0.95), width=1.8)
            c.line((sx, sy), (sx, sy + dp), dim(SAND_DIM, 0.9), 1.2)
        for i in range(3):
            figure(c, bx - 112 + i * 20, by + 2, 24, dim(TEXT_DIM, 0.95), 1.4)
        for i, (dx, dy) in enumerate(((-14, 0), (2, -6), (16, 0), (0, -14))):
            c.circle(bx + 92 + dx, by + 0 + dy, 6, fill=dim(GOLD, 0.85))
        c.text((bx, by + 76), "THEY WILL EXPLOIT YOU", 13,
               HL if v == 3 else dim(TEXT, 0.92), "mm", bold=v == 3)
        if mer_first:
            c.pulse_rect(bx - 130, by - 60, 260, 100, dim(HL, 0.85),
                         width=1.8, first=True, rx=10)
        # the weight already hanging over them — not slumbering
        c.line((900, 336), (900, 404), dim(SAND_DIM, 0.9), 1.4)
        c.polygon([(886, 404), (914, 404), (908, 432), (892, 432)],
                  fill=dim(GRAY, 0.55), stroke=dim(SAND, 0.9), width=1.6)
        c.text((900, 454), "SENTENCE — DOESN’T LINGER", 12,
               dim(TEXT_DIM, 0.95), "mm", italic=True)


def _ch2_precedents(c, v, pos):
    box_y, box_h = 186, 204
    cols = (240, 512, 784)
    bw = 224

    c.line((100, box_y + box_h), (960, box_y + box_h), dim(SAND_DIM, 0.85),
           1.6)

    def frame(cx, title, sub, on, first):
        col = dim(SAND, 0.95) if on else dim(SAND_DIM, 0.4)
        c.rect(cx - bw / 2, box_y, bw, box_h, fill=dim(PANEL, 0.55),
               stroke=col, width=1.8, rx=4)
        c.text((cx, box_y - 20), title, 14,
               dim(TEXT, 0.95) if on else dim(TEXT_DIM, 0.5), "mm",
               bold=first)
        if on:
            c.text((cx, box_y + box_h + 18), sub, 12,
                   dim(TEXT_DIM, 0.95), "mm", italic=True)
        if first:
            c.pulse_rect(cx - bw / 2 - 6, box_y - 6, bw + 12, box_h + 12,
                         dim(HL, 0.9), width=2, first=True, rx=8)

    # 1 — the angels that sinned
    a_on, a_first = since(pos, 2, 4)
    frame(cols[0], "ANGELS WHEN THEY SINNED", "PITS OF DARKNESS",
          a_on, a_first)
    if a_on:
        px0, px1, py = cols[0] - 84, cols[0] + 84, box_y + box_h - 16
        c.polygon([(px0, py), (px1, py), (px1 - 22, py - 74),
                   (px0 + 22, py - 74)], fill=dim(NIGHT, 0.95),
                  stroke=dim(GRAY, 0.7), width=1.4)
        hatch(c, px0 + 24, py - 70, px1 - 24, py - 6, dim(GRAY, 0.30), step=10)
        for i, (fx, fy) in enumerate(((cols[0] - 42, py - 96),
                                      (cols[0] + 6, py - 116),
                                      (cols[0] + 48, py - 86))):
            figure(c, fx, fy, 34, dim(GRAY, 0.95), 1.7, legs="fall",
                   arms="up")
        for k in range(4):
            yy = py - 62 + k * 15
            c.line((px0 + 26, yy), (px1 - 26, yy), dim(GRAY, 0.55), 1.6,
                   dash="7,6")

    # 2 — the old world
    b_on, b_first = since(pos, 2, 5)
    frame(cols[1], "THE ANCIENT WORLD", "A PREACHER OF RIGHTEOUSNESS",
          b_on, b_first)
    if b_on:
        flood(c, cols[1] - 96, box_y + 34, cols[1] + 96, box_y + box_h - 14,
              FLOOD_LEVEL)

    # 3 — Sodom and Gomorrha
    d_on, d_first = since(pos, 2, 6)
    frame(cols[2], "SODOM AND GOMORRAH", "TURNED INTO ASHES", d_on, d_first)
    if d_on:
        gy2 = box_y + box_h - 20
        for bx, bw2, bh2 in ((cols[2] - 58, 46, 44), (cols[2] - 4, 34, 62),
                             (cols[2] + 42, 40, 36)):
            c.polygon([(bx - bw2 / 2, gy2), (bx + bw2 / 2, gy2),
                       (bx + bw2 / 2 - 6, gy2 - bh2 * 0.35),
                       (bx - bw2 / 2 + 10, gy2 - bh2 * 0.30)],
                      fill=dim(ASH, 0.45), stroke=dim(ASH, 0.9), width=1.4)
        for k in range(9):
            t = k / 8
            c.circle(cols[2] - 66 + 132 * t,
                     gy2 - 44 - 26 * math.sin(t * 3.1), 2.6 + (k % 3),
                     fill=dim(ASH, 0.45))
        c.line((cols[2] - 84, gy2), (cols[2] + 84, gy2), dim(ASH, 0.9), 2.0)

    # v7 — just Lot delivered
    lot_on, lot_first = since(pos, 2, 7)
    if lot_on:
        figure(c, cols[2] + 76, box_y + box_h - 20, 40, GOLD, 2.0,
               arms="point_r", legs="walk")
        arrow(c, (cols[2] + 96, box_y + box_h - 44),
              (cols[2] + 124, box_y + box_h - 44), dim(GOLD, 0.9), 1.8, 7)
        c.text((cols[2] + 60, box_y + 22), "RIGHTEOUS LOT", 13,
               HL if v == 7 else dim(TEXT, 0.95), "mm", bold=v == 7)
        if lot_first:
            c.pulse_ellipse(cols[2] + 76, box_y + box_h - 42, 30, 34,
                            dim(HL, 0.9), width=2, first=True)

    # v8 — vexed from day to day
    day_on, day_first = since(pos, 2, 8)
    if day_on:
        tick_row(c, cols[2] - 72, box_y + 62, 16, 9.6, dim(TEXT_DIM, 0.95),
                 1.5, 12)
        c.text((cols[2], box_y + 80), "DAY TO DAY", 11,
               HL if v == 8 else dim(TEXT_DIM, 0.95), "mm", bold=v == 8)
        if day_first:
            c.pulse_rect(cols[2] - 84, box_y + 44, 168, 50, dim(HL, 0.9),
                         width=1.8, first=True, rx=8)

    # the count that came out of each
    counts = ((cols[0], "0", a_on, (2, 4)), (cols[1], "8", b_on, (2, 5)),
              (cols[2], "1", lot_on, (2, 7)))
    if a_on:
        c.text((108, 446), "SPARED", 12, dim(TEXT_DIM, 0.95), "lm",
               italic=True)
    for cx, n, on, at in counts:
        if not on:
            continue
        _, cfirst = since(pos, *at)
        c.text((cx, 446), n, 31, HL if cfirst else dim(TEXT, 0.95), "mm",
               bold=True)
        if cfirst:
            c.pulse_ellipse(cx, 446, 27, 27, dim(HL, 0.9), width=2,
                            first=True)
    if b_on:
        c.text((cols[1], 476), "NOAH WITH SEVEN OTHERS", 11.5,
               dim(TEXT_DIM, 0.95), "mm", italic=True)

    # v9 — the rule the three panels prove
    r_on, r_first = since(pos, 2, 9)
    if r_on:
        c.line((100, 496), (960, 496), dim(SAND_DIM, 0.8), 1.4)
        c.text((512, 518), "THE LORD KNOWS HOW", 14, HL, "mm",
               bold=r_first)
        arrow(c, (410, 544), (338, 532), dim(GOLD, 0.9), 2.0, 8)
        c.text((246, 528), "DELIVER THE GODLY", 13, dim(TEXT, 0.95), "mm",
               bold=v == 9)
        arrow(c, (614, 544), (686, 556), dim(RED, 0.9), 2.0, 8)
        c.text((790, 560), "KEEP THE UNRIGHTEOUS", 13, dim(RED, 0.95), "mm",
               bold=v == 9)
        if r_first:
            c.pulse_rect(140, 504, 744, 68, dim(HL, 0.85), width=1.8,
                         first=True, rx=14)


def _ch2_beasts(c, v, pos):
    # ---- vv10-11: the greater power withholds what the lesser one launches
    tgt = (628, 276)
    pw_on, pw_first = since(pos, 2, 11)
    ev_on, ev_first = since(pos, 2, 10)

    c.rect(tgt[0] - 62, tgt[1] - 26, 124, 52, fill=dim(PANEL, 0.9),
           stroke=dim(SAND, 0.9), width=1.8, rx=4)
    c.text(tgt, "DIGNITIES", 13.5, dim(TEXT, 0.95), "mm")

    # angels: long power bar, accusation withheld
    if pw_on:
        c.text((146, 168), "ANGELS", 14, dim(TEXT, 0.95), "lm", bold=v == 11)
        c.grow_rect(146, 182, 172, 13, fill=dim(SILVER, 0.55),
                    stroke=dim(SILVER, 0.9), width=1.4, rx=3,
                    w_from=0 if pw_first else 172)
        c.text((330, 189), "GREATER IN MIGHT AND POWER", 11.5,
               dim(TEXT_DIM, 0.95), "lm", italic=True)
        c.line((186, 210), (400, 210), dim(SILVER, 0.55), 1.8, dash="6,7")
        c.line((406, 198), (406, 222), dim(SILVER, 0.95), 3.0)
        c.text((418, 210), "NO RAILING JUDGMENT", 12.5,
               HL if v == 11 else dim(TEXT, 0.9), "lm", bold=v == 11)
        if pw_first:
            c.pulse_ellipse(406, 210, 20, 24, dim(HL, 0.9), width=2,
                            first=True)

    # these: short power bar, the accusation launched
    if ev_on:
        c.text((146, 288), "THESE", 14, dim(RED, 0.95), "lm", bold=v == 10)
        c.grow_rect(146, 302, 62, 13, fill=dim(RED, 0.45),
                    stroke=dim(RED, 0.9), width=1.4, rx=3,
                    w_from=0 if ev_first else 62)
        c.text((220, 309), "DARING — SELF-WILLED", 11.5,
               dim(TEXT_DIM, 0.95), "lm", italic=True)
        arrow(c, (186, 330), (596, 292), dim(RED, 0.9), 2.2, 10)
        c.text((300, 358), "SPEAK EVIL OF DIGNITARIES", 12.5,
               dim(RED, 0.95) if v == 10 else dim(TEXT_DIM, 0.95), "lm",
               bold=v == 10)
        if ev_first:
            c.pulse_rect(tgt[0] - 70, tgt[1] - 34, 140, 68, dim(RED, 0.85),
                         width=1.8, first=True, rx=8)

    # ---- v12: brute beasts, made to be taken
    br_on, br_first = since(pos, 2, 12)
    if br_on:
        bxc, bgy = 838, 232
        c.ellipse(bxc, bgy - 26, 92, 60, stroke=dim(SAND, 0.8), width=1.6)
        c.line((bxc - 92, bgy - 26), (bxc - 128, bgy - 70),
               dim(SAND, 0.8), 1.6)
        # v12: "unreasoning creatures, born mere animals to be taken and
        # destroyed" — the beasts a man hunts, so an ox and a sheep rather
        # than the two the chapter names later. Keeping those back until v22
        # is what lets the dog and the sow land when they arrive.
        beast(c, bxc - 24, bgy, 66, dim(GRAY, 0.95), 1.7, kind="ox")
        beast(c, bxc + 46, bgy - 6, 52, dim(GRAY, 0.8), 1.5, kind="sheep")
        c.text((bxc, bgy + 52), "UNREASONING CREATURES", 12.5,
               HL if v == 12 else dim(TEXT, 0.92), "mm", bold=v == 12)
        c.text((bxc, bgy + 72), "TAKEN AND DESTROYED", 11.5,
               dim(TEXT_DIM, 0.95), "mm", italic=True)
        if br_first:
            c.pulse_ellipse(bxc, bgy - 26, 104, 72, dim(HL, 0.9), width=2,
                            first=True)

    # ---- v13: spots and blemishes at the feast
    sp_on, sp_first = since(pos, 2, 13)
    if sp_on:
        fx, fy = 512, 470
        c.line((fx - 178, fy - 38), (fx + 178, fy - 38), dim(SAND, 0.95), 2.4)
        for lx in (fx - 150, fx + 150):
            c.line((lx, fy - 36), (lx, fy + 34), dim(SAND, 0.95), 2.0)
        spot_panel(c, fx, fy - 62, 300, 44, RED, 0.75)
        for i in range(4):
            c.circle(fx - 108 + i * 72, fy - 24, 11,
                     stroke=dim(SAND_DIM, 0.9), width=1.4)
        c.text((fx, fy + 56), "SPOTS AND DEFECTS", 13.5,
               dim(RED, 0.95) if v == 13 else dim(TEXT, 0.92), "mm",
               bold=v == 13)
        c.text((fx, fy + 76), "while they feast with you", 11.5,
               dim(TEXT_DIM, 0.95), "mm", italic=True)
        if sp_first:
            c.pulse_rect(fx - 156, fy - 88, 312, 52, dim(RED, 0.85),
                         width=1.8, first=True, rx=8)

    # ---- v14: unstable souls beguiled
    un_on, un_first = since(pos, 2, 14)
    if un_on:
        ux, uy = 176, 470
        c.polygon([(ux - 46, uy + 26), (ux + 46, uy + 26), (ux + 30, uy),
                   (ux - 30, uy)], fill=dim(PANEL, 0.9),
                  stroke=dim(SAND_DIM, 0.9), width=1.6)
        c.line((ux - 52, uy + 34), (ux + 52, uy + 18), dim(SAND_DIM, 0.9),
               1.6)
        figure(c, ux + 4, uy, 46, dim(TEXT_DIM, 0.95), 1.9, arms="open",
               lean=-0.14)
        arrow(c, (ux - 26, uy - 44), (ux - 86, uy - 56), dim(RED, 0.9),
              2.0, 8)
        c.text((ux, uy + 54), "ENTICING UNSETTLED SOULS", 12.5,
               dim(RED, 0.95) if v == 14 else dim(TEXT, 0.92), "mm",
               bold=v == 14)
        if un_first:
            c.pulse_ellipse(ux, uy - 16, 66, 58, dim(RED, 0.85), width=1.8,
                            first=True)


def _ch2_balaam(c, v, pos):
    ry = 236                                # centre of the right way
    # the right way, and the fork off it
    c.line((110, ry - 22), (962, ry - 22), dim(SAND, 0.95), 2.0)
    c.line((110, ry + 22), (962, ry + 22), dim(SAND, 0.95), 2.0)
    for x in range(150, 950, 80):
        c.line((x, ry - 12), (x, ry + 12), dim(SAND_DIM, 0.40), 1.2)
    c.text((216, ry - 44), "THE RIGHT WAY", 15, dim(TEXT, 0.95), "mm",
           bold=v == 15)

    crooked = [(380, ry + 22), (438, ry + 68), (500, ry + 86),
               (566, ry + 124), (650, ry + 142), (742, ry + 184),
               (846, ry + 212), (912, ry + 250)]
    fk_on, fk_first = since(pos, 2, 15)
    if fk_on:
        c.polyline(crooked, dim(RED, 0.9), 2.4)
        cross(c, 380, ry, 11, dim(RED, 0.95), 2.4)
        c.text((338, ry + 56), "WENT ASTRAY", 12, dim(RED, 0.95), "rm",
               bold=v == 15)
        c.text((420, ry + 36), "THE WAY OF BALAAM", 14, dim(RED, 0.95),
               "mm", bold=v == 15)
        # the wages, at the end of it — a stack, not five loose discs
        cn = F.coins()
        put(c, cn, 906, ry + 286, fit(cn, h=40), dim(GOLD, 0.9), 1.4)
        c.text((860, ry + 312), "THE WAGES OF WRONGDOING", 12.5,
               HL if v == 15 else dim(TEXT, 0.92), "mm", bold=v == 15)
        if fk_first:
            c.pulse_ellipse(380, ry + 6, 30, 40, dim(RED, 0.85), width=2,
                            first=True)

    # v16 — the dumb beast, and the prophet it stops
    ass_on, ass_first = since(pos, 2, 16)
    if fk_on:
        figure(c, 760, ry + 188, 64, dim(TEXT, 0.95), 2.1,
               arms="down" if ass_on else "walk", legs="stand")
        c.text((816, ry + 156), "BALAAM", 14, dim(TEXT, 0.95), "lm",
               bold=v == 15)
        c.text((816, ry + 176), "the son of Beor", 11.5,
               dim(TEXT_DIM, 0.95), "lm", italic=True)
    if ass_on:
        beast(c, 566, ry + 124, 92, GOLD, 2.1, kind="donkey")   # 2:16
        c.text((520, ry + 162), "A MUTE DONKEY", 13,
               HL if v == 16 else dim(TEXT, 0.95), "mm", bold=v == 16)
        c.path(f"M{626},{ry + 54} Q{690},{ry + 44} {738},{ry + 116}",
               stroke=dim(GOLD, 0.95), width=2.2)
        arrow(c, (730, ry + 104), (740, ry + 120), dim(GOLD, 0.95), 2.2, 8)
        # no ring on the ass — a second ellipse round the beast's own body
        # reads as two animals; the phrase above carries the accent
        phrase(c, (512, 96), "STOPPED THE MADNESS OF THE PROPHET", 20, HL,
               first=ass_first)


def _ch2_wells(c, v, pos):
    # the mist of darkness reserved, at the end of all of them
    dk_on, _ = since(pos, 2, 17)
    if dk_on:
        for i in range(9):
            c.rect(884 + i * 12, 118, 13, 244,
                   fill=dim(NIGHT, 0.25 + 0.08 * i))
        c.line((884, 118), (884, 362), dim(GRAY, 0.35), 1.2)
        c.text((898, 384), "THE BLACKNESS OF DARKNESS", 12,
               dim(TEXT_DIM, 0.95), "mm")
        c.text((898, 402), "RESERVED FOREVER", 12,
               dim(TEXT_DIM, 0.95), "mm")

    w_on, w_first = since(pos, 2, 17)
    if w_on:
        # a well with nothing in it: rim, windlass, rope, dry bottom
        wx, wy = 208, 236
        c.line((wx - 46, wy - 10), (wx - 46, wy - 74), dim(SAND, 0.95), 2.0)
        c.line((wx + 46, wy - 10), (wx + 46, wy - 74), dim(SAND, 0.95), 2.0)
        c.line((wx - 54, wy - 74), (wx + 54, wy - 74), dim(SAND, 0.95), 2.2)
        c.ellipse(wx, wy, 62, 18, stroke=dim(SAND, 0.95), width=2.2)
        c.ellipse(wx, wy, 49, 13, stroke=dim(SAND_DIM, 0.9), width=1.4)
        c.line((wx - 62, wy), (wx - 50, wy + 96), dim(SAND, 0.95), 2.0)
        c.line((wx + 62, wy), (wx + 50, wy + 96), dim(SAND, 0.95), 2.0)
        c.line((wx - 50, wy + 96), (wx + 50, wy + 96), dim(BROWN, 0.9), 2.2)
        hatch(c, wx - 48, wy + 60, wx + 48, wy + 94, dim(BROWN, 0.5), step=11)
        c.line((wx + 6, wy - 74), (wx + 6, wy + 22), dim(SAND_DIM, 0.95), 1.4)
        c.polygon([(wx - 8, wy + 22), (wx + 20, wy + 22), (wx + 16, wy + 46),
                   (wx - 4, wy + 46)], stroke=dim(SAND, 0.95), width=1.6)
        c.text((wx, wy + 124), "WELLS WITHOUT WATER", 13,
               HL if v == 17 else dim(TEXT, 0.92), "mm", bold=v == 17)
        if w_first:
            c.pulse_ellipse(wx, wy + 20, 82, 104, dim(HL, 0.9), width=2,
                            first=True)

        # a cloud with nothing in it, carried off
        cx2, cy2 = 512, 186
        c.path(f"M{cx2 - 74},{cy2 + 16} Q{cx2 - 86},{cy2 - 14} "
               f"{cx2 - 44},{cy2 - 18} Q{cx2 - 34},{cy2 - 46} "
               f"{cx2 + 4},{cy2 - 38} Q{cx2 + 42},{cy2 - 54} "
               f"{cx2 + 56},{cy2 - 16} Q{cx2 + 86},{cy2 - 8} "
               f"{cx2 + 72},{cy2 + 16} Z", stroke=dim(SAND, 0.9), width=2.0)
        for k, yy in enumerate((cy2 - 34, cy2 - 12, cy2 + 10)):
            c.line((cx2 + 88, yy), (cx2 + 154 + 12 * k, yy - 6),
                   dim(SILVER, 0.55), 1.6)
            arrow(c, (cx2 + 148 + 12 * k, yy - 6),
                  (cx2 + 166 + 12 * k, yy - 8), dim(SILVER, 0.55), 1.6, 6)
        for i in range(5):
            c.line((cx2 - 52 + i * 26, cy2 + 22), (cx2 - 56 + i * 26,
                   cy2 + 34), dim(WATER, 0.28), 1.6)
        c.text((cx2, cy2 + 68), "CLOUDS DRIVEN BY A STORM", 13,
               HL if v == 17 else dim(TEXT, 0.92), "mm", bold=v == 17)

    # v18 — great swelling words, and nothing inside them
    sw_on, sw_first = since(pos, 2, 18)
    if sw_on:
        bx, by = 596, 428
        c.ellipse(bx, by, 152, 58, stroke=dim(TEXT_DIM, 0.85), width=2.0)
        c.polyline([(bx - 60, by + 46), (bx - 112, by + 78),
                    (bx - 30, by + 54)], dim(TEXT_DIM, 0.85), 2.0)
        c.text((bx, by + 96), "GREAT SWELLING WORDS OF EMPTINESS", 13,
               dim(TEXT_DIM, 0.95) if v != 18 else HL, "mm", bold=v == 18)
        # those clean escaped, allured back toward it
        figure(c, 246, 470, 50, dim(TEXT, 0.92), 2.0, legs="walk")
        arrow(c, (286, 442), (410, 428), dim(RED, 0.85), 2.0, 8, dash="6,6")
        c.text((246, 508), "ESCAPING FROM ERROR", 12.5, dim(TEXT, 0.92), "mm",
               bold=v == 18)
        if sw_first:
            c.pulse_ellipse(bx, by, 162, 68, dim(RED, 0.85), width=1.8,
                            first=True)


def _ch2_bondage(c, v, pos):
    """v19 — the offer of liberty, made by a man wearing the chain."""
    gy = 448
    c.line((110, gy), (960, gy), dim(SAND_DIM, 0.85), 1.5)
    phrase(c, (512, 112), "PROMISING THEM LIBERTY", 21,
           dim(RED, 1.0), first=True)

    # the one making the offer
    figure(c, 372, gy, 100, dim(RED, 0.95), 2.3, arms="hold_r")
    # His own ankles, in irons, and the block he is not moving. The whole
    # shackle here against the broken one in his hand below: the same object
    # twice in one frame, once shut and once open, which is the verse's own
    # argument about who is promising what.
    sh = F.shackle()
    put(c, sh, 372, gy, fit(sh, w=64), dim(GRAY, 0.95), 1.7)
    c.line((348, gy - 12), (276, gy - 18), dim(GRAY, 0.95), 1.7)
    c.rect(232, gy - 32, 44, 32, fill=dim(GRAY, 0.35),
           stroke=dim(GRAY, 0.95), width=1.8)
    c.text((288, gy + 36), "BONDSERVANTS OF CORRUPTION", 13, dim(RED, 0.95),
           "mm", bold=True)
    c.pulse_ellipse(300, gy - 16, 104, 42, dim(RED, 0.85), width=1.9,
                    first=True)

    # the broken chain held out as though it were freedom — at hand height,
    # which the hold_r gesture puts a little below the shoulder
    shb = F.shackle(broken=True)
    put(c, shb, 438, gy - 62, fit(shb, w=78), dim(GOLD, 0.9), 1.7)
    c.text((492, gy - 52), "LIBERTY", 15, dim(GOLD, 0.95), "lm", bold=True)

    # the one it is offered to
    figure(c, 620, gy, 88, dim(TEXT_DIM, 0.95), 2.1, arms="open")

    # the rule underneath it
    c.text((372, 540), "OVERCOME", 14, dim(TEXT, 0.92), "mm")
    arrow(c, (444, 540), (538, 540), dim(RED, 0.9), 2.2, 9)
    c.text((646, 540), "BROUGHT INTO BONDAGE", 14, dim(RED, 0.95), "mm",
           bold=True)


def _ch2_loop(c, v, pos):
    """vv20-22 — the level chart and the proverb are one drawing: the line
    that fell below where it started curves round and closes on itself."""
    base = 300
    marks = [(196, base, "THE FIRST STATE", (2, 20)),
             (438, 208, "ESCAPED", (2, 20)),
             (652, base, "ENTANGLED AGAIN", (2, 20)),
             (846, 402, "THE LAST STATE", (2, 20))]

    c.line((150, base), (930, base), dim(SAND_DIM, 0.55), 1.3, dash="5,7")
    c.text((146, base), "level of the first state", 11,
           dim(TEXT_DIM, 0.85), "rm", italic=True)

    lv_on, lv_first = since(pos, 2, 20)
    if lv_on:
        pts = [(x, y) for x, y, _l, _a in marks]
        if lv_first:
            c.traced(pts, dim(SAND, 0.95), 2.6, dur="1.8s")
        else:
            c.polyline(pts, dim(SAND, 0.95), 2.6)
        for i, (x, y, label, _at) in enumerate(marks):
            hot = (i == 3 and v == 20)
            c.circle(x, y, 7, fill=HL if hot else dim(GOLD, 0.95))
            c.text((x, y - 26 if i in (1, 2) else y + 30), label, 12.5,
                   HL if hot else dim(TEXT, 0.92), "mm", bold=hot)
        c.text((846, 458), "WORSE THAN THE FIRST", 12.5,
               dim(RED, 0.95) if v == 20 else dim(TEXT_DIM, 0.95), "mm",
               bold=v == 20)
        if lv_first:
            c.pulse_ellipse(846, 402, 30, 30, dim(RED, 0.85), width=2,
                            first=True)

    # v21 — the road not taken stays at the level it started
    bt_on, bt_first = since(pos, 2, 21)
    if bt_on:
        c.line((196, base), (930, base), dim(SILVER, 0.85), 2.0, dash="9,7")
        c.text((930, base - 20), "BETTER NOT TO HAVE KNOWN", 12.5,
               HL if v == 21 else dim(TEXT, 0.92), "rm", bold=v == 21)
        if bt_first:
            c.pulse_rect(600, base - 34, 340, 30, dim(HL, 0.85), width=1.8,
                         first=True, rx=15)

    # v22 — the proverb closes the circuit
    lp_on, lp_first = since(pos, 2, 22)
    if lp_on:
        d = ("M846,402 C880,486 800,536 660,530 "
             "C520,524 380,540 274,506 C186,478 158,392 196,300")
        c.path(d, stroke=dim(MIRE, 1.0), width=2.6)
        arrow(c, (206, 340), (198, 312), dim(MIRE, 1.0), 2.6, 9)
        # the mire both proverbs end in
        c.ellipse(564, 536, 140, 20, fill=dim(MIRE, 0.85))
        hatch(c, 452, 528, 676, 546, dim(BROWN, 0.45), step=12)
        c.text((564, 566), "THE MIRE", 11.5, dim(TEXT_DIM, 0.95), "mm")
        beast(c, 456, 528, 74, dim(TEXT, 0.95), 1.8, kind="sow")
        c.text((444, 440), "THE SOW", 12.5,
               HL if v == 22 else dim(TEXT, 0.92), "mm", bold=v == 22)
        # facing left, back toward what it left — the loop the frame draws
        beast(c, 684, 528, 68, dim(TEXT, 0.95), 1.8, kind="dog", flip=-1)
        c.text((690, 440), "THE DOG", 12.5,
               HL if v == 22 else dim(TEXT, 0.92), "mm", bold=v == 22)
        phrase(c, (512, 104), "TURNS TO HIS OWN VOMIT AGAIN", 20, dim(RED, 1.0),
               first=lp_first)


# ---------------------------------------------------------------------------
# Chapter 3 — the line broken into three worlds, the two rulers, the ladder
# ---------------------------------------------------------------------------

def draw_ch3(c, v, pos):
    if v <= 4:
        _ch3_flat_line(c, v, pos)
    elif v <= 7:
        _ch3_eras(c, v, pos)
    elif v <= 9:
        _ch3_rulers(c, v, pos)
    elif v <= 13:
        _ch3_eras(c, v, pos)
    else:
        _ch3_close(c, v, pos)


def _ch3_flat_line(c, v, pos):
    ly = 340
    c.line((120, ly), (976, ly), dim(SAND, 0.95), 2.6)

    # vv1-2 — the two that spoke before, standing on the near end
    rm_on, rm_first = since(pos, 3, 1)
    if rm_on:
        arrow(c, (232, 396), (150, 396), dim(GOLD, 0.85), 1.8, 8)
        c.text((244, 396), "REMINDING YOU", 12.5,
               HL if v == 1 else dim(TEXT, 0.92), "lm", bold=v == 1)
        if rm_first:
            c.pulse_rect(138, 378, 244, 36, dim(HL, 0.85), width=1.8,
                         first=True, rx=17)
    ap_on, ap_first = since(pos, 3, 2)
    if ap_on:
        for px, label in ((192, "THE HOLY PROPHETS"), (356, "THE APOSTLES")):
            c.rect(px - 9, ly - 62, 18, 62, fill=dim(PANEL, 0.95),
                   stroke=dim(SAND, 0.95), width=1.8)
            c.line((px - 15, ly - 62), (px + 15, ly - 68), dim(SAND, 0.95),
                   2.0)
            c.text((px, ly - 86), label, 12.5,
                   HL if v == 2 else dim(TEXT, 0.92), "mm", bold=v == 2)
        if ap_first:
            c.pulse_rect(160, ly - 74, 232, 80, dim(HL, 0.9), width=2,
                         first=True, rx=8)

    # v3 — the scoffers at the far end
    sc_on, sc_first = since(pos, 3, 3)
    if sc_on:
        for i in range(4):
            figure(c, 686 + i * 62, ly, 50, dim(RED, 0.95), 2.0, legs="walk")
        c.text((810, ly - 76), "MOCKERS", 15,
               dim(RED, 0.95) if v == 3 else dim(TEXT, 0.92), "mm",
               bold=v == 3)
        c.text((810, ly - 56), "in the last days", 11.5,
               dim(TEXT_DIM, 0.95), "mm", italic=True)
        if sc_first:
            c.pulse_ellipse(810, ly - 26, 156, 44, dim(RED, 0.85), width=1.8,
                            first=True)

    # v4 — the fathers asleep, and the line they say never breaks
    fl_on, fl_first = since(pos, 3, 4)
    if fl_on:
        for i in range(3):
            xx = 452 + i * 44
            c.ellipse(xx, ly + 30, 19, 6.5, fill=dim(TEXT_DIM, 0.55))
            c.circle(xx - 21, ly + 30, 5.5, fill=dim(TEXT_DIM, 0.55))
        c.text((496, ly + 58), "THE FATHERS FELL ASLEEP", 12.5,
               dim(TEXT_DIM, 0.95), "mm", italic=True)
        c.line((120, ly), (976, ly), HL, 3.0)
        c.text((496, ly - 24), "ALL THINGS CONTINUE", 15, HL, "mm",
               bold=True)
        phrase(c, (512, 116), "WHERE IS THE PROMISE OF HIS COMING?", 21,
               dim(RED, 1.0), first=fl_first)


# --- the era bar, built across vv5-7 and crossed at vv10-13 ----------------

BAR_Y0, BAR_Y1 = 286, 394
SEG = ((130, 392), (452, 716), (776, 962))     # the three worlds
BND = ((392, 452), (716, 776))                 # water, then fire


def _ch3_eras(c, v, pos):
    y0, y1 = BAR_Y0, BAR_Y1
    (s1a, s1b), (s2a, s2b), (s3a, s3b) = SEG
    (wa, wb), (fa, fb) = BND

    # the word of God, running the length of all three
    wd_on, wd_first = since(pos, 3, 5)
    if wd_on:
        if wd_first:
            c.traced([(100, 196), (962, 196)], dim(GOLD, 0.85), 2.0,
                     dur="1.6s")
        else:
            c.line((100, 196), (962, 196), dim(GOLD, 0.85), 2.0)
        c.text((100, 174), "THE WORD OF GOD", 13,
               HL if v == 5 else dim(TEXT, 0.92), "lm", bold=v == 5)
        c.line(((wa + wb) / 2, 196), ((wa + wb) / 2, y0 - 6),
               dim(GOLD, 0.55), 1.6, dash="5,6")
        if since(pos, 3, 7)[0]:
            c.line(((fa + fb) / 2, 196), ((fa + fb) / 2, y0 - 6),
                   dim(GOLD, 0.55), 1.6, dash="5,6")
            c.text(((fa + fb) / 2 + 12, 214), "by the same word", 11,
                   dim(TEXT_DIM, 0.95), "lm", italic=True)

    def seg_frame(a, b, l1, l2, on):
        col = dim(SAND, 0.95) if on else dim(SAND_DIM, 0.35)
        c.rect(a, y0, b - a, y1 - y0, fill=dim(PANEL, 0.55), stroke=col,
               width=1.8)
        c.text(((a + b) / 2, 240), l1, 13,
               dim(TEXT, 0.95) if on else dim(TEXT_DIM, 0.45), "mm")
        c.text(((a + b) / 2, 260), l2, 13,
               dim(TEXT, 0.95) if on else dim(TEXT_DIM, 0.45), "mm")

    # ---- world 1 ----
    w1_on, w1_first = since(pos, 3, 5)
    seg_frame(s1a, s1b, "THE WORLD", "THAT THEN WAS", w1_on)
    drowned, dr_first = since(pos, 3, 6)
    if w1_on:
        if not drowned:
            # standing out of the water, and in the water
            c.rect(s1a + 2, y0 + 2, s1b - s1a - 4, 20, fill=dim(WATER, 0.35))
            flood(c, s1a + 14, y0 + 26, s1b - 14, y1 - 8, 0.30, ark=False)
        else:
            c.rect(s1a + 2, y0 + 2, s1b - s1a - 4, y1 - y0 - 4,
                   fill=dim(WATER, 0.22))
            flood(c, s1a + 14, y0 + 26, s1b - 14, y1 - 8, FLOOD_LEVEL)
            c.text(((s1a + s1b) / 2, 450), "PERISHED", 14,
                   dim(WATER, 1.0) if v == 6 else dim(TEXT, 0.92), "mm",
                   bold=v == 6)
        if dr_first:
            c.pulse_rect(s1a - 6, y0 - 6, s1b - s1a + 12, y1 - y0 + 12,
                         dim(WATER, 0.95), width=2.4, first=True, rx=4)

    # ---- the water boundary ----
    if w1_on:
        c.rect(wa, y0, wb - wa, y1 - y0,
               fill=dim(WATER, 0.55 if drowned else 0.18),
               stroke=dim(WATER, 0.9), width=1.8)
        for k in range(4):
            yy = y0 + 16 + k * 24
            c.path(f"M{wa + 4},{yy} q14,-8 28,0 q14,8 28,0",
                   stroke=dim(WATER, 0.9 if drowned else 0.4), width=1.6)
        c.text(((wa + wb) / 2, 418), "WATER", 12.5,
               dim(WATER, 1.0) if v == 6 else dim(TEXT_DIM, 0.95), "mm",
               bold=v == 6)

    # ---- world 2 ----
    w2_on, w2_first = since(pos, 3, 7)
    burned, bu_first = since(pos, 3, 10)
    seg_frame(s2a, s2b, "THE HEAVENS THAT NOW EXIST", "AND THE EARTH", w2_on)
    if w2_on:
        gy2 = y1 - 20
        c.line((s2a + 12, gy2), (s2b - 12, gy2), dim(SAND, 0.9), 1.8)
        works = ((s2a + 62, 34, 46), (s2a + 128, 44, 62), (s2a + 196, 30, 38))
        for i, (bx, bw, bh) in enumerate(works):
            if burned:
                # the works that are therein, burned up
                c.polygon([(bx - bw / 2, gy2), (bx + bw / 2, gy2),
                           (bx + bw / 2 - 8, gy2 - bh * 0.22),
                           (bx - bw / 2 + 8, gy2 - bh * 0.18)],
                          fill=dim(ASH, 0.5), stroke=dim(ASH, 0.9), width=1.4)
            else:
                c.rect(bx - bw / 2, gy2 - bh, bw, bh, fill=dim(PANEL, 0.9),
                       stroke=dim(SAND, 0.9), width=1.6)
                c.polyline([(bx - bw / 2 - 5, gy2 - bh), (bx, gy2 - bh - 14),
                            (bx + bw / 2 + 5, gy2 - bh)], dim(SAND, 0.9), 1.6)
        if not burned:
            # kept in store — the seal on the second world
            skx, sky = s2b - 30, y0 + 24
            c.circle(skx, sky, 15, fill=dim(GOLD, 0.22),
                     stroke=dim(GOLD, 0.95), width=1.8)
            c.line((skx - 8, sky), (skx + 8, sky), dim(GOLD, 0.95), 1.8)
            c.line((skx, sky - 8), (skx, sky + 8), dim(GOLD, 0.95), 1.8)
            c.text(((s2a + s2b) / 2, 450), "STORED UP FOR FIRE", 14,
                   HL if v == 7 else dim(TEXT, 0.92), "mm", bold=v == 7)
        else:
            c.text(((s2a + s2b) / 2, 450), "DISSOLVED", 14,
                   dim(FIRE, 1.0) if v in (10, 11) else dim(TEXT, 0.92),
                   "mm", bold=v in (10, 11))
        if w2_first:
            c.pulse_rect(s2a - 6, y0 - 6, s2b - s2a + 12, y1 - y0 + 12,
                         dim(HL, 0.9), width=2.2, first=True, rx=4)

    # ---- the fire boundary ----
    if w2_on:
        c.rect(fa, y0, fb - fa, y1 - y0,
               fill=dim(FIRE, 0.45 if burned else 0.10),
               stroke=dim(FIRE, 0.95 if burned else 0.55), width=1.8)
        if burned:
            for k in range(5):
                bx = fa + 8 + k * 11
                c.path(f"M{bx},{y1 - 6} q-5,-24 4,-38 q3,16 10,22 "
                       f"q4,-12 1,-22 q12,20 3,38 z", fill=dim(FIRE, 0.85))
        c.text(((fa + fb) / 2, 418), "FIRE", 12.5,
               dim(FIRE, 1.0) if v in (10, 12) else dim(TEXT_DIM, 0.95),
               "mm", bold=v in (10, 12))
        if bu_first:
            c.pulse_rect(fa - 6, y0 - 6, fb - fa + 12, y1 - y0 + 12,
                         dim(FIRE, 0.95), width=2.4, first=True, rx=4)

    # ---- world 3 ----
    w3_on, w3_first = since(pos, 3, 13)
    seg_frame(s3a, s3b, "NEW HEAVENS", "AND A NEW EARTH", w3_on)
    if w3_on:
        c.rect(s3a + 2, y0 + 2, s3b - s3a - 4, 44, fill=dim(GOLD, 0.16))
        gy3 = y1 - 22
        c.polyline([(s3a + 10, gy3), (s3a + 56, gy3 - 24),
                    (s3a + 104, gy3 - 10), (s3b - 44, gy3 - 30),
                    (s3b - 10, gy3)], dim(GOLD, 0.9), 2.0)
        c.rect(s3a + 2, gy3, s3b - s3a - 4, y1 - gy3 - 2,
               fill=dim(GOLD, 0.12))
        c.text(((s3a + s3b) / 2, 450), "IN WHICH", 12.5, HL, "mm",
               bold=v == 13)
        c.text(((s3a + s3b) / 2, 468), "RIGHTEOUSNESS DWELLS", 12.5, HL, "mm",
               bold=v == 13)
        if w3_first:
            c.pulse_rect(s3a - 6, y0 - 6, s3b - s3a + 12, y1 - y0 + 12,
                         dim(HL, 0.9), width=2.4, first=True, rx=4)

    # ---- v10: the thief in the night, above the bar ----
    th_on, th_first = since(pos, 3, 10)
    if th_on:
        c.rect(80, 96, 904, 74, fill=dim(NIGHT, 0.85))
        for k, (sx, sy) in enumerate(((190, 118), (330, 140), (470, 112),
                                      (610, 146), (760, 120), (900, 138))):
            c.circle(sx, sy, 1.8, fill=dim(SILVER, 0.7))
        figure(c, 700, 162, 44, dim(SILVER, 0.9), 1.9, legs="walk")
        c.text((512, 132), "AS A THIEF IN THE NIGHT", 17,
               HL if v == 10 else dim(TEXT, 0.9), "mm", bold=v == 10)
        if th_first:
            c.pulse_rect(80, 96, 904, 74, dim(HL, 0.85), width=2, first=True)

    # ---- vv11-12: the persons the dissolving asks for ----
    hp_on, hp_first = since(pos, 3, 11)
    ht_on, ht_first = since(pos, 3, 12)
    if hp_on:
        figure(c, s2b - 16, y1 - 20, 48, GOLD, 2.2,
               arms="point_r" if ht_on else "down",
               lean=0.16 if ht_on else 0.0)
        c.text((512, 496), "HOLY LIVING AND GODLINESS", 14,
               HL if v == 11 else dim(TEXT, 0.92), "mm", bold=v == 11)
        if hp_first:
            c.pulse_ellipse(s2b - 16, y1 - 44, 34, 38, dim(HL, 0.9),
                            width=2, first=True)
    if ht_on:
        arrow(c, (fa - 4, y0 - 10), (fb + 30, y0 - 10), dim(GOLD, 0.95),
              2.2, 9)
        c.text((512, 524), "LOOKING FOR AND EARNESTLY DESIRING", 14,
               HL if v == 12 else dim(TEXT, 0.92), "mm", bold=v == 12)
        if ht_first:
            c.pulse_ellipse((fa + fb) / 2 + 14, y0 - 10, 62, 18,
                            dim(HL, 0.9), width=2, first=True)


def _ch3_rulers(c, v, pos):
    x0, x1 = 176, 848
    y_day, y_yrs = 224, 344

    def ruler(y, label, right, divisions, on, first, col):
        c.text((x0, y - 34), label, 16, HL if first else dim(TEXT, 0.95),
               "lm", bold=True)
        c.text((x1, y - 34), right, 12, dim(TEXT_DIM, 0.95), "rm",
               italic=True)
        c.grow_rect(x0, y - 15, x1 - x0, 30, fill=dim(col, 0.32),
                    stroke=dim(col, 0.95), width=2.0, rx=3,
                    w_from=0 if first else (x1 - x0))
        for i in range(divisions + 1):
            xx = x0 + (x1 - x0) * i / divisions
            major = (divisions <= 12) or (i % 6 == 0)
            c.line((xx, y + 15), (xx, y + 15 + (13 if major else 7)),
                   dim(col, 0.9 if major else 0.55), 1.6 if major else 1.2)
        if first:
            c.pulse_rect(x0 - 7, y - 22, x1 - x0 + 14, 44, dim(HL, 0.9),
                         width=2, first=True, rx=6)

    _, d_first = since(pos, 3, 8)
    ruler(y_day, "ONE DAY", "24 hours", 24, True, d_first, SILVER)
    ruler(y_yrs, "A THOUSAND YEARS", "10 centuries", 10, True, d_first, GOLD)

    # the two ends squared off, and the equality between them
    for xx in (x0, x1):
        c.line((xx, y_day + 34), (xx, y_yrs - 24), dim(SAND_DIM, 0.8), 1.3,
               dash="4,6")
    c.text((904, (y_day + y_yrs) / 2), "=", 44, HL, "mm", bold=True)
    c.text((904, (y_day + y_yrs) / 2 + 42), "with the Lord", 11.5,
           dim(TEXT_DIM, 0.95), "mm", italic=True)

    # v9 — what men measure the delay against, and why it is long
    sl_on, sl_first = since(pos, 3, 9)
    if sl_on:
        sy = 496
        c.grow_rect(x0, sy, 96, 20, fill=dim(RED, 0.30),
                    stroke=dim(RED, 0.9), width=1.8, rx=3,
                    w_from=0 if sl_first else 96)
        c.text((x0 + 110, sy + 10), "AS SOME COUNT SLOWNESS", 13,
               dim(RED, 0.95) if v == 9 else dim(TEXT, 0.92), "lm",
               bold=v == 9)
        # the reason the long ruler is long
        for i in range(9):
            xx = x0 + 34 + i * 78
            arrow(c, (xx, y_yrs + 88), (xx, y_yrs + 42), dim(GOLD, 0.75),
                  1.6, 6)
            figure(c, xx, y_yrs + 112, 24, dim(TEXT_DIM, 0.95), 1.4)
        c.text((680, sy + 10), "ALL SHOULD COME TO REPENTANCE", 14,
               HL if v == 9 else dim(TEXT, 0.92), "lm", bold=v == 9)
        c.text((512, y_yrs - 34), "PATIENT", 12,
               HL if v == 9 else dim(TEXT_DIM, 0.95), "mm", bold=v == 9)
        if sl_first:
            c.pulse_rect(x0 - 7, sy - 7, 110, 34, dim(RED, 0.85), width=1.8,
                         first=True, rx=6)


def _ch3_close(c, v, pos):
    # v14 — the cloth of 2:13, without spot
    sp_on, sp_first = since(pos, 3, 14)
    if sp_on:
        spot_panel(c, 196, 250, 250, 108, RED, 0.14, lift=True)
        c.text((196, 326), "WITHOUT DEFECT AND BLAMELESS", 13,
               HL if v == 14 else dim(TEXT, 0.92), "mm", bold=v == 14)
        c.text((196, 346), "found in peace", 11.5,
               dim(TEXT_DIM, 0.95), "mm", italic=True)
        if sp_first:
            c.pulse_rect(196 - 133, 250 - 62, 266, 124, dim(HL, 0.9),
                         width=2, first=True, rx=8)

    # v15 — the longsuffering measured in ch3:8 is itself the salvation
    ls_on, ls_first = since(pos, 3, 15)
    if ls_on:
        c.grow_rect(468, 214, 150, 17, fill=dim(GOLD, 0.30),
                    stroke=dim(GOLD, 0.95), width=1.7, rx=3,
                    w_from=0 if ls_first else 150)
        c.text((543, 196), "PATIENCE", 13,
               HL if v == 15 else dim(TEXT, 0.92), "mm", bold=v == 15)
        c.text((646, 222), "=", 24, HL, "mm", bold=True)
        c.text((730, 222), "SALVATION", 15,
               HL if v == 15 else dim(TEXT, 0.92), "lm", bold=v == 15)
        if ls_first:
            c.pulse_rect(460, 186, 384, 54, dim(HL, 0.85), width=1.8,
                         first=True, rx=12)

    # v16 — Paul's epistles, and the twist put into them
    ep_on, ep_first = since(pos, 3, 16)
    if ep_on:
        sy, x0s, x1s = 392, 460, 812
        c.rect(x0s, sy - 26, x1s - x0s, 52, fill=dim(PANEL, 0.95),
               stroke=dim(SAND, 0.95), width=1.8)
        for ex in (x0s, x1s):
            c.ellipse(ex, sy, 10, 30, fill=dim(PANEL, 0.98),
                      stroke=dim(SAND, 0.95), width=1.8)
        for k in range(3):
            c.line((x0s + 22, sy - 12 + k * 12), (622, sy - 12 + k * 12),
                   dim(TEXT_DIM, 0.7), 1.2)
            c.line((712, sy - 12 + k * 12), (x1s - 22, sy - 12 + k * 12),
                   dim(TEXT_DIM, 0.7), 1.2)
        # the wrested section
        for k in range(3):
            yy = sy - 12 + k * 12
            c.path(f"M622,{yy} q22,-16 44,0 q22,16 46,0",
                   stroke=dim(RED, 0.95), width=1.8)
        c.polygon([(622, sy - 26), (712, sy - 26), (712, sy + 26),
                   (622, sy + 26)], stroke=dim(RED, 0.85), width=1.6)
        c.text((667, sy - 44), "TWIST", 12.5,
               dim(RED, 0.95) if v == 16 else dim(TEXT_DIM, 0.95), "mm",
               bold=v == 16)
        c.text((664, sy + 52), "PAUL — HARD TO UNDERSTAND", 12.5,
               HL if v == 16 else dim(TEXT, 0.92), "mm", bold=v == 16)
        if ep_first:
            c.pulse_rect(616, sy - 32, 102, 64, dim(RED, 0.85), width=1.8,
                         first=True, rx=6)

    # v17 — the edge that 1:10 promised he would not go over
    st_on, st_first = since(pos, 3, 17)
    if st_on:
        px, py = 206, 484
        c.rect(px - 96, py, 192, 26, fill=dim(PANEL, 0.95),
               stroke=dim(SAND, 0.95), width=2)
        hatch(c, px - 96, py + 26, px + 96, py + 52, dim(SAND_DIM, 0.45),
              step=12)
        figure(c, px + 16, py, 50, GOLD, 2.1)
        arrow(c, (px - 16, py - 34), (px - 106, py - 26), dim(RED, 0.9),
              2.0, 8, dash="6,6")
        c.text((px - 56, py - 60), "CARRIED AWAY", 12,
               dim(RED, 0.95) if v == 17 else dim(TEXT_DIM, 0.95), "rm",
               bold=v == 17)
        c.text((px, py + 74), "YOUR OWN STEADFASTNESS", 13,
               HL if v == 17 else dim(TEXT, 0.92), "mm", bold=v == 17)
        if st_first:
            c.pulse_rect(px - 104, py - 8, 208, 42, dim(HL, 0.9), width=2,
                         first=True, rx=6)

    # v18 — the ladder of chapter 1, one rung further
    gr_on, gr_first = since(pos, 3, 18)
    if gr_on:
        draw_ladder(c, LADDER_3, 8, labels=False,
                    extra="GROW" if gr_on else None)
        cx, cy, half = rung_at(LADDER_3, 0)
        c.text((cx - half - 12, cy), "FAITH", 11, dim(TEXT_DIM, 0.95), "rm")
        cx, cy, half = rung_at(LADDER_3, 7)
        c.text((cx - half - 12, cy), "LOVE", 11, dim(TEXT_DIM, 0.95),
               "rm")
        c.text((896, 196), "GROW IN THE GRACE", 14, HL, "mm", bold=True)
        c.text((896, 216), "and knowledge", 11.5,
               dim(TEXT_DIM, 0.95), "mm", italic=True)
        phrase(c, (446, 108), "TO HIM BE THE GLORY FOREVER", 21, HL,
               first=gr_first)
        c.text((446, 142), "Amen.", 14, dim(TEXT, 0.9), "mm", italic=True)


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
    print(f"2 Peter: {count} SVG files, {total / 1e3:.0f} KB")


if __name__ == "__main__":
    main()
