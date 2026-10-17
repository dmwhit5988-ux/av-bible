"""Render Genesis 1 (the six days: forming and filling) as per-verse vector SVGs.

One chart, replayed for all 31 verses. The six creation days are laid out as a
two-column parallel — the three *forming* days on the left (light; sky and sea;
land and plants) against the three *filling* days on the right (the lights; the
birds and fish; the animals and man) — because Genesis 1:2 states the two
problems the six days answer in order: the earth was "formless" (days 1-3 form
it) *and* "empty" (days 4-6 fill it). Each row pairs a realm with what comes to
fill or rule it.

Per verse: the day's card lights (its ring tracing itself once, then holding,
per the house animation rules), the verse's own pip inside that card lights, the
row's pairing arrow turns gold once both of its days have been reached, and the
seven-day bar along the bottom advances. Days not yet reached stay ghosted, so
the chart reads as the chapter's whole shape from verse 1 onward.

This replaces the photographic stills that used to fill visuals/Genesis/1/
(retired to backups/png_replaced_by_svg/ under config.ARCHIVE_DIR; see docs/archive/genesis1-photo-credits.txt).

Run inside the project venv:
    .venv\\Scripts\\python.exe generate_genesis1_svg.py
"""

import math
import os

import svg_figures as F
from svg_surface import SvgCanvas
from generate_tabernacle import (W, H, BG, PANEL, SAND, SAND_DIM, SILVER, TEXT,
                                 TEXT_DIM, GOLD, HL, BROWN, out_path)
from generate_tribal_maps import RIVER, WATER_TXT as FOAM
# the garden palette, shared with Genesis 2 and 3
from generate_genesis2_svg import GREEN, GREEN_DIM, EARTH, garden_paint


def g(alpha):
    return HL + (int(255 * alpha),)


def dim(color, a):
    """`color` with an 0-255 alpha, in the (r, g, b, a) form SvgCanvas takes
    (it turns the fourth element into a fill-/stroke-opacity)."""
    return color + (int(a),)


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

COL_W = 430
LEFT_X = 40
GAP_W = 84
RIGHT_X = LEFT_X + COL_W + GAP_W          # 554
RIGHT_END = RIGHT_X + COL_W               # 984

BAND1_Y, BAND_H = 80, 34                  # "in the beginning" (v1)
BAND2_Y = 118                             # "formless / and empty" (v2)
HEAD_Y = 166                              # column headers
CARD_Y0, CARD_H, CARD_GAP = 186, 96, 10   # three paired rows
BAR_Y, BAR_H = 512, 22                    # the seven-day bar

GLYPH_W, GLYPH_H = 240, 38                # the drawn day inside each card

# ---------------------------------------------------------------------------
# The six days.  day -> (column, row, theme, (v_lo, v_hi))
# column 0 = forming (left), 1 = filling (right); row 0..2 top to bottom.
# Each card's body is a small drawing of the day (GLYPHS below) rather than a
# restatement of the verse — the narration carries the words.
# ---------------------------------------------------------------------------

DAYS = {
    1: (0, 0, "Light", (3, 5)),
    4: (1, 0, "Lights", (14, 19)),
    2: (0, 1, "Sky & Sea", (6, 8)),
    5: (1, 1, "Birds & Fish", (20, 23)),
    3: (0, 2, "Land & Plants", (9, 13)),
    6: (1, 2, "Animals & Man", (24, 31)),
}

# The realm each row is about — formed on the left, filled on the right.
ROW_TAGS = ["light", "sky & sea", "land"]
ROW_PAIRS = [(1, 4), (2, 5), (3, 6)]

# Verse -> the day it belongs to (0 = the two prologue bands, handled apart).
VERSE_DAY = {1: 0, 2: 0}
for _d, (_c, _r, _t, (_lo, _hi)) in DAYS.items():
    for _v in range(_lo, _hi + 1):
        VERSE_DAY[_v] = _d

# ---------------------------------------------------------------------------
# Drawing
# ---------------------------------------------------------------------------

def card_rect(col, row):
    x = LEFT_X if col == 0 else RIGHT_X
    y = CARD_Y0 + row * (CARD_H + CARD_GAP)
    return x, y, COL_W, CARD_H


# ---------------------------------------------------------------------------
# The days, drawn.  Each takes the glyph box and renders that day's work in
# it: forming days on the left of the chart, the filling days that answer them
# on the right, so the pairs read as pairs visually and not only by number.
# ---------------------------------------------------------------------------

NIGHT = (10, 10, 16)


def _g_light(c, x, y, w, h, lit, reached):
    """Day 1 — the light divided from the darkness."""
    mid = x + w / 2
    c.rect(x, y, w / 2, h, fill=NIGHT, stroke=SAND_DIM, width=1)
    c.rect(mid, y, w / 2, h, fill=dim(GOLD, 205 if lit else 130),
           stroke=SAND_DIM, width=1)
    c.line((mid, y), (mid, y + h), HL if lit else SAND, 2.5)
    for i in range(3):                      # a few rays into the light
        yy = y + h * (i + 1) / 4
        c.line((mid + 8, yy), (mid + 26, yy), dim(NIGHT, 150), 1.5)
    for sx, sy in ((0.14, 0.3), (0.28, 0.66), (0.38, 0.24)):
        c.circle(x + w * sx, y + h * sy, 1.6, fill=dim(SAND, 190))


def _g_expanse(c, x, y, w, h, lit, reached):
    """Day 2 — an expanse dividing the waters from the waters."""
    band = h * 0.27
    edge = HL if lit else SAND
    for by in (y, y + h - band):
        c.rect(x, by, w, band, fill=dim(RIVER, 215))
    c.line((x, y + band), (x + w, y + band), edge, 2)
    c.line((x, y + h - band), (x + w, y + h - band), edge, 2)
    for i in range(5):                      # the gap between them: the sky
        xx = x + w * (i + 0.5) / 5
        c.line((xx - 9, y + h / 2), (xx + 9, y + h / 2),
               dim(SAND_DIM, 170), 1.2)


# Everything drawn on a card comes from svg_figures, so the creation days and
# the garden of chapters 2 and 3 are populated by the same creatures. Days 1
# and 2 are left as they were: light divided from darkness, and the waters
# above from the waters beneath, are not things the vocabulary has, or should.
#
# MAN_H is the one number that matters on day 6. Everything standing on that
# card is drawn at the scale it implies, so the ox is an ox beside the man
# rather than a larger blob and the creeping thing creeps at its own size.

MAN_H = 30.0


def _ground(c, x, w, gy):
    c.line((x, gy), (x + w, gy), dim(EARTH, 245), 3)


def _fit(c, parts, x, gy, height, col, page=BG, flip=1, style=None):
    """Draw `parts` to an overall `height`, standing on gy."""
    y0, y1 = F.bbox((parts, 0))[2:]
    F.draw(c, parts, x, gy, height / (y1 - y0), col, page, flip=flip,
           style=style)


def _g_land(c, x, y, w, h, lit, reached):
    """Day 3 — dry land out of the waters, and what grows on it."""
    gy = y + h - 5
    c.rect(x + w * 0.72, gy - 9, w * 0.28, 11, fill=dim(RIVER, 205))
    _ground(c, x, w * 0.74, gy)
    paint = garden_paint(lit)
    for parts, fx, hgt in ((F.grass(), 0.07, 9), (F.herb(), 0.20, 15),
                           (F.tree(fruit=3), 0.44, 32)):
        _fit(c, parts, x + w * fx, gy, hgt, GREEN, style=paint)


def _g_lights(c, x, y, w, h, lit, reached):
    """Day 4 — the greater light, the lesser, and the stars."""
    c.rect(x, y, w, h, fill=NIGHT, stroke=SAND_DIM, width=1)
    cy = y + h / 2
    F.draw(c, F.sun(), x + w * 0.16, cy, h * 0.0125,
           GOLD if lit else dim(GOLD, 175), NIGHT)
    F.draw(c, F.moon(), x + w * 0.36, cy, h * 0.0125, SILVER, NIGHT)
    for dx, dy, r in ((0.60, 0.30, 0.011), (0.70, 0.66, 0.008),
                      (0.80, 0.36, 0.010), (0.88, 0.70, 0.007),
                      (0.94, 0.28, 0.009)):
        F.draw(c, F.star(), x + w * dx, y + h * dy, h * r,
               HL if lit else SAND, NIGHT)


def _g_swarms(c, x, y, w, h, lit, reached):
    """Day 5 — fowl in the open firmament, and the swarming seas.

    The birds are drawn in profile rather than from below: this card is a
    band of sky read edge on, and a bird seen from beneath has a spread but
    no heading, so a skyful of them sits still. Three attitudes and three
    sizes, because a flock all at one point of one stroke reads as wallpaper.
    """
    wl = y + h * 0.52
    col = HL if lit else SAND
    c.rect(x, wl, w, y + h - wl, fill=dim(RIVER, 215))
    for fx, fy, s, pose, rot in ((0.10, 0.30, 0.20, "up", 0.06),
                                 (0.26, 0.16, 0.15, "glide", -0.10),
                                 (0.41, 0.34, 0.12, "down", 0.08)):
        F.draw(c, F.bird(pose=pose, view="profile"), x + w * fx,
               y + h * fy, s, col, BG, rot=rot)
    for fx, fy, s, fl in ((0.60, 0.72, 0.36, 1), (0.76, 0.88, 0.30, -1),
                          (0.90, 0.70, 0.26, 1)):
        F.draw(c, F.fish(), x + w * fx, y + h * fy, s, col, BG, flip=fl)


def _g_creatures(c, x, y, w, h, lit, reached):
    """Day 6 — cattle, the creeping thing, the beast, and man in God's
    image, all at one scale."""
    gy = y + h - 5
    col = HL if lit else SAND
    _ground(c, x, w, gy)
    s = MAN_H / 98.0
    for parts, fx, k in ((F.ox(), 0.17, 1.0), (F.sheep(), 0.42, 1.0),
                         (F.serpent(raised=False), 0.60, 0.8),
                         (F.man(), 0.86, 1.0)):
        F.draw(c, parts, x + w * fx, gy, s * k, col, BG)
    if lit:
        c.circle(x + w * 0.86, gy - MAN_H * 0.52, MAN_H * 0.78,
                 stroke=g(0.7), width=1.5)


GLYPHS = {1: _g_light, 2: _g_expanse, 3: _g_land,
          4: _g_lights, 5: _g_swarms, 6: _g_creatures}


def ring(c, x, y, w, h, color, width=2, first=True):
    """The highlight ring on the current box. It brightens once, on the verse
    the box becomes current, and then simply stays — a day card is current for
    up to eight verses and re-animating on each of them is a distraction."""
    c.pulse_rect(x, y, w, h, color, width=width, first=first, rx=4)


def draw_band(c, y, x, w, label, state, center=False):
    """One of the two prologue bands. state: 'current' | 'past' | 'future'."""
    fill = PANEL if state != "future" else BG
    edge = SAND if state == "past" else (HL if state == "current" else SAND_DIM)
    c.rect(x, y, w, BAND_H, fill=fill, stroke=None if state == "current" else edge,
           width=1.5, rx=4)
    if state == "current":
        ring(c, x, y, w, BAND_H, g(0.95), width=2)
    txt = HL if state == "current" else (TEXT if state == "past" else TEXT_DIM)
    c.text((x + w / 2 if center else x + 14, y + BAND_H / 2), label, 16, txt,
           "mm" if center else "lm", bold=(state == "current"))


def draw_prologue(c, v):
    def state(target):
        return "current" if v == target else ("past" if v > target else "future")

    # verse 1 in four words, verse 2 in the two the columns answer — the
    # narration carries the sentences
    draw_band(c, BAND1_Y, LEFT_X, RIGHT_END - LEFT_X, "In the beginning",
              state(1))
    half = (RIGHT_END - LEFT_X - 14) / 2
    draw_band(c, BAND2_Y, LEFT_X, half, "FORMLESS", state(2), center=True)
    draw_band(c, BAND2_Y, LEFT_X + half + 14, half, "EMPTY", state(2),
              center=True)
    # arrows down into each column header
    for cx in (LEFT_X + COL_W / 2, RIGHT_X + COL_W / 2):
        top, bot = BAND2_Y + BAND_H + 3, HEAD_Y - 16
        col_started = (cx < 500 and v >= 3) or (cx > 500 and v >= 14)
        col = GOLD if col_started else SAND_DIM
        c.line((cx, top), (cx, bot), col, 2)
        c.polygon([(cx, bot + 6), (cx - 4, bot - 1), (cx + 4, bot - 1)], fill=col)


def draw_headers(c, v):
    for col, (label, sub, first_v) in enumerate([
            ("FORMING", "days 1–3", 3), ("FILLING", "days 4–6", 14)]):
        x = LEFT_X if col == 0 else RIGHT_X
        live = v >= first_v
        c.text((x, HEAD_Y), label, 19, GOLD if live else SAND_DIM, "la",
               bold=True)
        c.text((x + 106, HEAD_Y + 3), sub, 13,
               TEXT_DIM if live else dim(TEXT_DIM, 150), "la", italic=True)


def draw_card(c, day, v):
    col, row, theme, (lo, hi) = DAYS[day]
    x, y, w, h = card_rect(col, row)
    current = lo <= v <= hi
    reached = v >= lo

    c.rect(x, y, w, h, fill=PANEL if reached else BG,
           stroke=SAND if reached and not current else
           (None if current else SAND_DIM), width=1.5, rx=5)
    if current:
        ring(c, x, y, w, h, g(0.95), width=2.5, first=(v == lo))

    head = HL if current else (TEXT if reached else TEXT_DIM)
    c.text((x + 16, y + 22), f"DAY {day}", 17, head, "lm", bold=True)
    c.text((x + 82, y + 22), theme, 17, GOLD if reached else SAND_DIM, "lm",
           italic=True)
    c.text((x + w - 16, y + 22), f"verses {lo}–{hi}", 12, TEXT_DIM, "rm",
           italic=True)
    # the day itself, drawn rather than restated — the narration carries
    # the words. A day not yet reached shows faintly, so the chart's shape is
    # readable from verse 1 without the days looking done.
    if not reached:
        c.raw(['<g opacity="0.4">'])
    GLYPHS[day](c, x + (w - GLYPH_W) / 2, y + 38, GLYPH_W, GLYPH_H,
                lit=current, reached=reached)
    if not reached:
        c.raw(['</g>'])

    # verse pips — one per verse of the day, the current one lit, so a long
    # day (6: verses 24-31) still moves verse by verse.
    px, py = x + 16, y + h - 14
    for i, vv in enumerate(range(lo, hi + 1)):
        cx = px + i * 17
        if vv == v:
            c.circle(cx, py, 5.5, fill=HL, stroke=BG, width=1)
        elif vv < v:
            c.circle(cx, py, 3.5, fill=SAND, stroke=SAND_DIM, width=1)
        else:
            c.circle(cx, py, 3.5, fill=BG, stroke=SAND_DIM, width=1.5)


def draw_pair_arrows(c, v):
    """The gap between the columns: a row tag and an arrow that goes gold once
    the row's filling day has been reached."""
    for row, (fday, lday) in enumerate(ROW_PAIRS):
        y = CARD_Y0 + row * (CARD_H + CARD_GAP) + CARD_H / 2
        x0, x1 = LEFT_X + COL_W + 12, RIGHT_X - 12
        cx = (x0 + x1) / 2
        filled = v >= DAYS[lday][3][0]
        col = GOLD if filled else SAND_DIM
        c.text((cx, y - 16), ROW_TAGS[row], 11,
               TEXT_DIM if filled else dim(TEXT_DIM, 150), "mm", italic=True)
        c.line((x0, y), (x1 - 6, y), col, 2.5 if filled else 1.5)
        c.polygon([(x1, y), (x1 - 8, y - 5), (x1 - 8, y + 5)], fill=col)
        c.text((cx, y + 17), f"{fday} → {lday}", 12,
               GOLD if filled else SAND_DIM, "mm", bold=filled)


def draw_day_bar(c, v):
    """Seven segments along the foot — the days closed by the chapter's
    'evening and morning' refrain, plus the seventh day still to come."""
    day = VERSE_DAY.get(v, 0)
    seg = (RIGHT_END - LEFT_X - 6 * 4) / 7
    c.text((LEFT_X, BAR_Y - 12), "EVENING AND MORNING", 11, TEXT_DIM, "la",
           italic=True)
    for i in range(1, 8):
        x = LEFT_X + (i - 1) * (seg + 4)
        if i == 7:
            c.rect(x, BAR_Y, seg, BAR_H, fill=BG, stroke=SAND_DIM, width=1.5,
                   rx=3)
            c.text((x + seg / 2, BAR_Y + BAR_H / 2), "7 · rest", 12, TEXT_DIM,
                   "mm", italic=True)
            continue
        current = (i == day)
        past = (day > i)
        c.rect(x, BAR_Y, seg, BAR_H,
               fill=GOLD if current else (SAND_DIM if past else BG),
               stroke=None if current else (SAND if past else SAND_DIM),
               width=1.5, rx=3)
        label = f"{i}"
        c.text((x + seg / 2, BAR_Y + BAR_H / 2), label, 13,
               BG if current else (TEXT if past else TEXT_DIM), "mm",
               bold=current)


# ---------------------------------------------------------------------------
# Assemble one verse
# ---------------------------------------------------------------------------

def render(v):
    c = SvgCanvas(W, H, bg=BG)
    c.text((28, 24), "Genesis 1 · Forming and Filling", 22, TEXT, "la",
           bold=True)
    draw_prologue(c, v)
    draw_headers(c, v)
    for day in DAYS:
        draw_card(c, day, v)
    draw_pair_arrows(c, v)
    draw_day_bar(c, v)
    return c


def main():
    total = count = 0
    for v in range(1, 32):
        c = render(v)
        out = out_path("Genesis", 1, f"Genesis_1_{v}.svg")
        c.save(out)
        total += os.path.getsize(out)
        count += 1
    print(f"Genesis 1: {count} SVG files, {total/1e3:.0f} KB")


if __name__ == "__main__":
    main()
