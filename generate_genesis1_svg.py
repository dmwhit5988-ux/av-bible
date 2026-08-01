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
(retired to backups/png_replaced_by_svg/; see visuals/CREDITS.txt).

Run inside the project venv:
    .venv\\Scripts\\python.exe generate_genesis1_svg.py
"""

import math
import os

from svg_surface import SvgCanvas
from generate_tabernacle import (W, H, BG, PANEL, SAND, SAND_DIM, SILVER, TEXT,
                                 TEXT_DIM, GOLD, HL, BROWN, out_path)
from generate_tribal_maps import RIVER, WATER_TXT as FOAM
# the garden palette, shared with Genesis 2 and 3
from generate_genesis2_svg import GREEN, GREEN_DIM, EARTH


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


def _g_land(c, x, y, w, h, lit, reached):
    """Day 3 — dry land out of the waters, and what grows on it."""
    gy = y + h - 5
    col = GREEN if lit else GREEN_DIM
    c.rect(x + w * 0.70, gy - 9, w * 0.30, 11, fill=dim(RIVER, 205))
    c.line((x, gy), (x + w * 0.72, gy), dim(EARTH, 245), 4)
    for dx in (0.07, 0.11, 0.15):           # grass
        c.line((x + w * dx, gy - 1), (x + w * dx - 4, gy - 13), col, 1.8)
    hx = x + w * 0.31                       # a seed-bearing herb
    c.line((hx, gy), (hx, gy - 19), col, 2)
    for s in (-1, 1):
        c.line((hx, gy - 11), (hx + s * 6, gy - 16), col, 1.5)
    c.circle(hx, gy - 22, 3.4, fill=GOLD if lit else dim(GOLD, 160))
    tx = x + w * 0.53                       # a fruit tree
    c.rect(tx - 2, gy - 15, 4, 15, fill=BROWN)
    c.circle(tx, gy - 21, 10, fill=dim(col, 225), stroke=col, width=1.2)
    c.circle(tx + 5, gy - 23, 2.3, fill=GOLD if lit else dim(GOLD, 160))


def _g_lights(c, x, y, w, h, lit, reached):
    """Day 4 — the greater light, the lesser, and the stars."""
    c.rect(x, y, w, h, fill=NIGHT, stroke=SAND_DIM, width=1)
    sx, sy, r = x + w * 0.20, y + h / 2, h * 0.31
    for i in range(8):                      # the greater light, with rays
        a = math.radians(i * 45)
        c.line((sx + math.cos(a) * (r + 3), sy + math.sin(a) * (r + 3)),
               (sx + math.cos(a) * (r + 9), sy + math.sin(a) * (r + 9)),
               GOLD if lit else dim(GOLD, 160), 1.6)
    c.circle(sx, sy, r, fill=GOLD if lit else dim(GOLD, 175))
    mx = x + w * 0.48                       # the lesser light, a crescent
    c.circle(mx, sy, h * 0.23, fill=dim(SILVER, 225))
    c.circle(mx + h * 0.11, sy - h * 0.04, h * 0.21, fill=NIGHT)
    for dx, dy in ((0.68, 0.24), (0.76, 0.62), (0.84, 0.34),
                   (0.64, 0.74), (0.92, 0.68), (0.90, 0.22)):
        c.circle(x + w * dx, y + h * dy, 1.9, fill=HL if lit else SAND)


def _bird(c, x, y, col):
    c.polyline([(x - 8, y), (x - 3, y - 5), (x + 1, y - 1)], stroke=col,
               width=1.8)
    c.polyline([(x + 1, y - 1), (x + 5, y - 6), (x + 10, y)], stroke=col,
               width=1.8)


def _fish(c, x, y, col):
    c.ellipse(x, y, 7, 3.6, fill=dim(col, 165), stroke=col, width=1.1)
    c.polygon([(x - 7, y), (x - 12, y - 3.5), (x - 12, y + 3.5)], fill=col)


def _g_swarms(c, x, y, w, h, lit, reached):
    """Day 5 — birds in the expanse, and the swarming seas."""
    wl = y + h * 0.54
    col = HL if lit else SAND
    c.rect(x, wl, w, y + h - wl, fill=dim(RIVER, 215))
    wave = [(x + w * i / 12, wl + (2.5 if i % 2 else -2.5))
            for i in range(13)]
    c.polyline(wave, stroke=dim(FOAM, 200), width=1.5)
    for bx, by in ((0.16, 0.22), (0.33, 0.11), (0.50, 0.28)):
        _bird(c, x + w * bx, y + h * by, col)
    for fx, fy in ((0.26, 0.78), (0.48, 0.90), (0.70, 0.74),
                   (0.88, 0.86)):
        _fish(c, x + w * fx, y + h * fy, col)


def _g_creatures(c, x, y, w, h, lit, reached):
    """Day 6 — the creatures of the land, and man in God's image."""
    gy = y + h - 5
    col = HL if lit else SAND
    c.line((x, gy), (x + w, gy), dim(EARTH, 245), 4)
    qx = x + w * 0.20                       # livestock
    c.ellipse(qx, gy - 15, 14, 7, fill=dim(col, 165), stroke=col, width=1.2)
    for dx in (-9, -4, 4, 9):
        c.line((qx + dx, gy - 9), (qx + dx, gy - 1), col, 1.5)
    c.circle(qx + 18, gy - 21, 4.5, fill=dim(col, 165), stroke=col, width=1.2)
    c.line((qx - 14, gy - 17), (qx - 20, gy - 23), col, 1.5)
    cx = x + w * 0.46                       # a creeping thing
    c.polyline([(cx, gy - 3), (cx + 5, gy - 7), (cx + 10, gy - 3),
                (cx + 15, gy - 7), (cx + 20, gy - 3)], stroke=col, width=1.8)
    fx = x + w * 0.78                       # man, in God's image
    c.circle(fx, gy - 27, 5, fill=col)
    c.line((fx, gy - 22), (fx, gy - 10), col, 2.4)
    c.line((fx - 7, gy - 18), (fx + 7, gy - 18), col, 2.2)
    c.line((fx, gy - 10), (fx - 5, gy), col, 2.2)
    c.line((fx, gy - 10), (fx + 5, gy), col, 2.2)
    if lit:
        c.circle(fx, gy - 16, 19, stroke=g(0.7), width=1.5)


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
