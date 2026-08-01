"""Render Numbers 1-2 (the census and the camp) as per-verse vector SVGs.

One world, two halves, replayed for all 88 verses of the two chapters:

* **Left — the camp.** A plan of the four camps around the Tent of Meeting,
  drawn with **east at the top**, because that is the axis the text itself
  uses: the tabernacle's door faced the sunrise, Judah camps there, and Judah
  sets out first. Rotating east to the top puts the marching order — Judah,
  Reuben, Ephraim, Dan — in clockwise order around the plan, so the sequence
  of Numbers 2 is legible as a shape. (North therefore falls on the left and
  south on the right; the compass rose in the corner says so.)
* **Right — the census.** The twelve tribes as a roster, each a name, a bar
  and a number, with Levi held out of the count on its own dashed row and the
  running total growing along the foot to 603,550.

Chapter 1 is the roster's chapter: each tribe's bar wipes in on the verse that
states its number, the camp plan sitting ghosted behind. Chapter 2 is the
plan's chapter: the roster stays lit and done while the four camps light one
at a time, each with its standard, its three tribes, its total and its place in
the order of march.

The bars share one scale (Judah's 74,600 is full width), so the chapter's real
subject — that these tribes are wildly unequal — is visible without arithmetic.

Text discipline: the verse is read aloud alongside the graphic, so nothing here
restates it. No caption line, no notes, no footer. The twelve princes are names
rather than prose, but showing all twelve at once is twelve lines of text for
no gain — so a prince appears only on the row the current verse is naming.

Naming note: the usual `generate_<book><chapters>_svg.py` contraction is not
available here — `generate_numbers34_svg.py` is already Numbers *34*, the
borders map — so these two families spell their chapter range out.

Run inside the project venv:
    .venv\\Scripts\\python.exe generate_numbers1_2_svg.py
"""

import math
import os

from svg_surface import SvgCanvas
from generate_tabernacle import (W, H, BG, PANEL, SAND, SAND_DIM, SILVER, TEXT,
                                 TEXT_DIM, GOLD, HL, RED, BROWN, WHITE_LINEN,
                                 out_path)
from generate_tribal_maps import RIVER
from generate_genesis2_svg import GREEN


def dim(color, a):
    """`color` with an 0-255 alpha, in the (r, g, b, a) form SvgCanvas takes."""
    return color + (int(a),)


def g(alpha):
    return HL + (int(255 * alpha),)


def num(n):
    return f"{n:,}"


# ---------------------------------------------------------------------------
# The twelve tribes.  name -> (count, prince, prince-verse, camp side)
# Counts and princes are the chapter's own figures (1:5-15, 1:20-43); the camp
# assignment is Numbers 2. Order below is the census order of chapter 1, which
# is *not* the camp order — that difference is half the point of the graphic.
# ---------------------------------------------------------------------------

TRIBES = [
    ("Reuben",   46500, "Elizur son of Shedeur",         5,  "S"),
    ("Simeon",   59300, "Shelumiel son of Zurishaddai",  6,  "S"),
    ("Gad",      45650, "Eliasaph son of Deuel",         14, "S"),
    ("Judah",    74600, "Nahshon son of Amminadab",      7,  "E"),
    ("Issachar", 54400, "Nethanel son of Zuar",          8,  "E"),
    ("Zebulun",  57400, "Eliab son of Helon",            9,  "E"),
    ("Ephraim",  40500, "Elishama son of Ammihud",       10, "W"),
    ("Manasseh", 32200, "Gamaliel son of Pedahzur",      10, "W"),
    ("Benjamin", 35400, "Abidan son of Gideoni",         11, "W"),
    ("Dan",      62700, "Ahiezer son of Ammishaddai",    12, "N"),
    ("Asher",    41500, "Pagiel son of Ochran",          13, "N"),
    ("Naphtali", 53400, "Ahira son of Enan",             15, "N"),
]

COUNT = {t[0]: t[1] for t in TRIBES}
PRINCE = {t[0]: t[2] for t in TRIBES}
PRINCE_V = {t[0]: t[3] for t in TRIBES}
SIDE = {t[0]: t[4] for t in TRIBES}

MAX_COUNT = max(COUNT.values())          # Judah, 74,600 — the bar scale
GRAND_TOTAL = 603550                     # 1:46, 2:32

# The four camps, in the order they set out (2:9, 16, 24, 31).
# side -> (compass word, standard tribe, its three tribes, total, march order)
CAMPS = {
    "E": ("EAST",  "Judah",   ["Judah", "Issachar", "Zebulun"],  186400, 1),
    "S": ("SOUTH", "Reuben",  ["Reuben", "Simeon", "Gad"],       151450, 2),
    "W": ("WEST",  "Ephraim", ["Ephraim", "Manasseh", "Benjamin"], 108100, 3),
    "N": ("NORTH", "Dan",     ["Dan", "Asher", "Naphtali"],      157600, 4),
}

CAMP_COLOR = {"E": GOLD, "S": RED, "W": GREEN, "N": RIVER}
ORDINAL = {1: "1st", 2: "2nd", 3: "3rd", 4: "4th"}

# Chapter 1's census runs in pairs: an introducing verse, then the number.
CENSUS_PAIRS = [
    (20, 21, "Reuben"), (22, 23, "Simeon"),   (24, 25, "Gad"),
    (26, 27, "Judah"),  (28, 29, "Issachar"), (30, 31, "Zebulun"),
    (32, 33, "Ephraim"), (34, 35, "Manasseh"), (36, 37, "Benjamin"),
    (38, 39, "Dan"),    (40, 41, "Asher"),    (42, 43, "Naphtali"),
]
COUNT_V = {name: cv for _, cv, name in CENSUS_PAIRS}
INTRO_V = {name: iv for iv, _, name in CENSUS_PAIRS}

# Chapter 2 walks each camp tribe by tribe: verse -> (side, tribe or None).
# A None tribe is the camp's summary verse.
CH2_CAMP_VERSES = {}
CH2_COUNT_V = {}                          # the second verse of each pair
for _side, _first in (("E", 3), ("S", 10), ("W", 18), ("N", 25)):
    _tribes = CAMPS[_side][2]
    for _i, _t in enumerate(_tribes):
        CH2_CAMP_VERSES[_first + _i * 2] = (_side, _t)
        CH2_CAMP_VERSES[_first + _i * 2 + 1] = (_side, _t)
        CH2_COUNT_V[_t] = _first + _i * 2 + 1
    CH2_CAMP_VERSES[_first + 6] = (_side, None)

CAMP_FIRST_V = {"E": 3, "S": 10, "W": 18, "N": 25}
CAMP_LAST_V = {"E": 9, "S": 16, "W": 24, "N": 31}

CH_LEN = {1: 54, 2: 34}

# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

HEAD_Y = 62                               # the two column headers

# -- left: the camp plan ----------------------------------------------------
SIDE_W, MID_W, PLAN_GAP = 116, 196, 8
PL_X = 28
COL_L = PL_X                              # north card
COL_M = PL_X + SIDE_W + PLAN_GAP          # 152 — east/centre/west column
COL_R = COL_M + MID_W + PLAN_GAP          # 356 — south card
PLAN_X1 = COL_R + SIDE_W                  # 472

TOP_Y, TOP_H = 84, 92                     # east card
MID_Y, MID_H = 184, 180                   # the tabernacle, in the middle
BOT_Y, BOT_H = 372, 92                    # west card
MARCH_Y, MARCH_H = 496, 30                # the order-of-march strip

# -- right: the census roster ----------------------------------------------
RX0, RX1 = 498, 996
ROW_Y0, ROW_H = 84, 29
BAR_X, BAR_W = 716, 200                   # the shared count-bar scale
LEVI_Y, LEVI_H = 440, 26
TOT_Y, TOT_H = 476, 32


def bar_w(n):
    return BAR_W * n / MAX_COUNT


# ---------------------------------------------------------------------------
# The camp plan
# ---------------------------------------------------------------------------

def camp_rect(side):
    """Where each camp's card sits. East is at the top, so north falls on the
    left and south on the right — the compass rose spells this out."""
    return {"E": (COL_M, TOP_Y, MID_W, TOP_H),
            "W": (COL_M, BOT_Y, MID_W, BOT_H),
            "N": (COL_L, MID_Y, SIDE_W, MID_H),
            "S": (COL_R, MID_Y, SIDE_W, MID_H)}[side]


def draw_compass(c, cx, cy, r):
    """East up, north left, south right, west down — stated, not assumed."""
    c.circle(cx, cy, r, fill=None, stroke=SAND_DIM, width=1.2)
    for ang, label in ((-90, "E"), (90, "W"), (180, "N"), (0, "S")):
        a = math.radians(ang)
        c.line((cx + math.cos(a) * (r - 8), cy + math.sin(a) * (r - 8)),
               (cx + math.cos(a) * (r - 1), cy + math.sin(a) * (r - 1)),
               SAND, 1.2)
        c.text((cx + math.cos(a) * (r + 10), cy + math.sin(a) * (r + 10)),
               label, 12, GOLD if label == "E" else TEXT_DIM, "mm",
               bold=(label == "E"))
    c.polygon([(cx, cy - r + 4), (cx - 5, cy - r + 15), (cx + 5, cy - r + 15)],
              fill=GOLD)


def draw_tabernacle(c):
    """The middle of the camp: the Levite ring, and inside it the courtyard
    drawn to the Exodus 27 proportions (100 x 50 cubits) with its gate on the
    east — which, on this plan, is the top."""
    c.rect(COL_M + 8, MID_Y + 8, MID_W - 16, MID_H - 16, fill=PANEL,
           stroke=None, rx=4)
    c.raw([f'<rect x="{COL_M + 8}" y="{MID_Y + 8}" width="{MID_W - 16}" '
           f'height="{MID_H - 16}" rx="4" fill="none" '
           f'stroke="rgb{SILVER}" stroke-width="1.3" stroke-opacity="0.6" '
           f'stroke-dasharray="5 4"/>'])
    c.text((COL_M + MID_W / 2, MID_Y + 22), "LEVITES", 11, SILVER, "mm",
           bold=True)

    s = 1.24                                   # px per cubit
    cw, chh = 50 * s, 100 * s                  # 50 wide (N-S), 100 long (E-W)
    x0 = COL_M + (MID_W - cw) / 2
    y0 = MID_Y + (MID_H - chh) / 2 + 6
    c.rect(x0, y0, cw, chh, fill=BG, stroke=WHITE_LINEN, width=1.4)
    gx = x0 + (cw - 20 * s) / 2                # the gate, 20 cubits, east end
    c.line((gx, y0), (gx + 20 * s, y0), GOLD, 2.8)
    c.rect(x0 + cw / 2 - 3.1, y0 + 12 * s, 6.2, 6.2, fill=None, stroke=SAND,
           width=1.1)                          # the bronze altar
    c.circle(x0 + cw / 2, y0 + 27 * s, 2.8, fill=None, stroke=SILVER, width=1)
    tw, th = 10 * s, 30 * s                    # the tent, in the western half
    tx, ty = x0 + (cw - tw) / 2, y0 + 56 * s
    c.rect(tx, ty, tw, th, fill=dim(BROWN, 190), stroke=GOLD, width=1.3)
    c.line((tx, ty + 20 * s), (tx + tw, ty + 20 * s), GOLD, 1.2)   # the veil


def draw_wide_camp(c, side, ch, v):
    """The east and west cards — wide, so their three tribes sit in one column
    with the count to the right."""
    x, y, w, h = camp_rect(side)
    word, standard, tribes, total, order = CAMPS[side]
    col = CAMP_COLOR[side]
    live = ch == 2 and v >= CAMP_FIRST_V[side]
    cur = ch == 2 and CAMP_FIRST_V[side] <= v <= CAMP_LAST_V[side]

    c.rect(x, y, w, h, fill=PANEL if live else BG,
           stroke=None if cur else (dim(col, 190) if live else SAND_DIM),
           width=1.4, rx=5)
    if cur:
        c.pulse_rect(x, y, w, h, dim(col, 250), width=2.4,
                     first=(v == CAMP_FIRST_V[side]), rx=5)
    c.text((x + 12, y + 15), word, 10, col if live else SAND_DIM, "lm",
           bold=True)
    c.text((x + w - 12, y + 15), ORDINAL[order] if live else "", 10, TEXT_DIM,
           "rm", italic=True)
    c.text((x + 12, y + 35), standard.upper(), 15,
           HL if cur else (TEXT if live else TEXT_DIM), "lm", bold=True)
    tot_lit = ch == 2 and v >= CAMP_LAST_V[side]
    c.text((x + w - 12, y + 35), num(total) if live else "", 12,
           GOLD if tot_lit else TEXT_DIM, "rm", bold=tot_lit)

    for i, t in enumerate(tribes):
        ty = y + 55 + i * 14
        here = ch == 2 and CH2_CAMP_VERSES.get(v, (None, None)) == (side, t)
        c.text((x + 16, ty), t, 11,
               HL if here else (TEXT if live else TEXT_DIM), "lm", bold=here)
        c.text((x + w - 16, ty), num(COUNT[t]) if live else "—", 11,
               GOLD if here else (TEXT_DIM if live else SAND_DIM), "rm")


def draw_tall_camp(c, side, ch, v):
    """The north and south cards — narrow, so each tribe takes two lines."""
    x, y, w, h = camp_rect(side)
    word, standard, tribes, total, order = CAMPS[side]
    col = CAMP_COLOR[side]
    live = ch == 2 and v >= CAMP_FIRST_V[side]
    cur = ch == 2 and CAMP_FIRST_V[side] <= v <= CAMP_LAST_V[side]

    c.rect(x, y, w, h, fill=PANEL if live else BG,
           stroke=None if cur else (dim(col, 190) if live else SAND_DIM),
           width=1.4, rx=5)
    if cur:
        c.pulse_rect(x, y, w, h, dim(col, 250), width=2.4,
                     first=(v == CAMP_FIRST_V[side]), rx=5)
    mid = x + w / 2
    c.text((mid, y + 16), word, 10, col if live else SAND_DIM, "mm", bold=True)
    c.text((mid, y + 34), standard.upper(), 15,
           HL if cur else (TEXT if live else TEXT_DIM), "mm", bold=True)
    tot_lit = ch == 2 and v >= CAMP_LAST_V[side]
    c.text((mid, y + 52), num(total) if live else "", 12,
           GOLD if tot_lit else TEXT_DIM, "mm", bold=tot_lit)

    for i, t in enumerate(tribes):
        ty = y + 76 + i * 30
        here = ch == 2 and CH2_CAMP_VERSES.get(v, (None, None)) == (side, t)
        c.text((mid, ty), t, 11.5,
               HL if here else (TEXT if live else TEXT_DIM), "mm", bold=here)
        c.text((mid, ty + 15), num(COUNT[t]) if live else "—", 11,
               GOLD if here else (TEXT_DIM if live else SAND_DIM), "mm")
    c.text((mid, y + h - 10), ORDINAL[order] if live else "", 10, TEXT_DIM,
           "mm", italic=True)


def draw_march_strip(c, ch, v):
    """The order of march along the foot of the plan (2:9, 16, 24, 31). The
    Levite marker between the second camp and the third is 2:17 — the tent
    travels in the middle — drawn rather than written out."""
    c.text((PL_X, MARCH_Y - 12), "ORDER OF MARCH", 10,
           GOLD if ch == 2 else SAND_DIM, "la", bold=True)
    cw, mw, gap = 95, 38, 5
    xs = {"E": PL_X, "S": PL_X + cw + gap,
          "W": PL_X + 2 * cw + mw + 3 * gap, "N": PL_X + 3 * cw + mw + 4 * gap}
    for side in ("E", "S", "W", "N"):
        x = xs[side]
        lit = ch == 2 and v >= CAMP_LAST_V[side]
        cur = ch == 2 and CAMP_FIRST_V[side] <= v <= CAMP_LAST_V[side]
        col = CAMP_COLOR[side]
        c.rect(x, MARCH_Y, cw, MARCH_H, fill=dim(col, 210) if lit else BG,
               stroke=None if lit else (dim(col, 200) if cur else SAND_DIM),
               width=1.3, rx=3)
        c.text((x + cw / 2, MARCH_Y + MARCH_H / 2),
               f"{CAMPS[side][4]}  {CAMPS[side][1]}", 12,
               BG if lit else (HL if cur else TEXT_DIM), "mm",
               bold=(lit or cur))
    # the tent and the Levites, travelling in the middle of the camps
    mx = PL_X + 2 * cw + 2 * gap
    mid_lit = ch == 2 and v >= 17
    c.rect(mx, MARCH_Y, mw, MARCH_H, fill=PANEL if mid_lit else BG,
           stroke=SILVER if mid_lit else SAND_DIM, width=1.3, rx=3)
    c.rect(mx + mw / 2 - 6, MARCH_Y + 8, 12, 14,
           fill=dim(BROWN, 190) if mid_lit else None,
           stroke=SILVER if mid_lit else SAND_DIM, width=1.2)
    if ch == 2 and v == 17:
        c.pulse_rect(mx, MARCH_Y, mw, MARCH_H, g(0.95), width=2, first=True,
                     rx=3)


def draw_plan(c, ch, v):
    c.text((PL_X, HEAD_Y), "THE CAMP", 16, GOLD if ch == 2 else SAND_DIM,
           "la", bold=True)

    # In chapter 1 the camp is the *answer*, not yet given — it shows faintly
    # so the shape of the two chapters is legible from verse 1 onward.
    ghost = ch == 1 and v < 50
    if ghost:
        c.raw(['<g opacity="0.42">'])
    draw_compass(c, COL_L + SIDE_W / 2, TOP_Y + TOP_H / 2, 26)
    for side in ("E", "W"):
        draw_wide_camp(c, side, ch, v)
    for side in ("N", "S"):
        draw_tall_camp(c, side, ch, v)
    draw_tabernacle(c)
    draw_march_strip(c, ch, v)
    if ghost:
        c.raw(['</g>'])

    # 1:50-53 hands the middle of the camp to the Levites; 2:17 is where the
    # tent and that same middle set out between the second camp and the third.
    if (ch == 1 and 50 <= v <= 53) or (ch == 2 and v == 17):
        c.pulse_rect(COL_M + 8, MID_Y + 8, MID_W - 16, MID_H - 16,
                     g(0.95), width=2.2, first=(v in (50, 17)), rx=4)
    # the grand total, sitting in the plan's free bottom corner
    if ch == 2 and v >= 32:
        c.rect(COL_R, BOT_Y + 14, SIDE_W, 56, fill=PANEL, stroke=GOLD,
               width=1.4, rx=4)
        c.text((COL_R + SIDE_W / 2, BOT_Y + 32), "ALL CAMPS", 10, TEXT_DIM,
               "mm", bold=True)
        c.text((COL_R + SIDE_W / 2, BOT_Y + 52), num(GRAND_TOTAL), 15, GOLD,
               "mm", bold=True)


# ---------------------------------------------------------------------------
# The census roster
# ---------------------------------------------------------------------------

def counted_total(ch, v):
    if ch == 2:
        return GRAND_TOTAL
    return sum(COUNT[t] for t in COUNT if COUNT_V[t] <= v)


def draw_roster_row(c, i, name, ch, v):
    y = ROW_Y0 + i * ROW_H
    mid = y + ROW_H / 2
    col = CAMP_COLOR[SIDE[name]]

    counted = ch == 2 or COUNT_V[name] <= v
    prince_now = ch == 1 and PRINCE_V[name] == v
    if ch == 1:
        current = prince_now or INTRO_V[name] <= v <= COUNT_V[name]
        first = prince_now or v == INTRO_V[name]
    else:
        current = CH2_CAMP_VERSES.get(v, (None, None))[1] == name
        first = current and CH2_CAMP_VERSES.get(v - 1, (None, None))[1] != name

    if current:
        c.rect(RX0 - 5, y, RX1 - RX0 + 10, ROW_H - 3, fill=PANEL, stroke=None,
               rx=3)
        c.pulse_rect(RX0 - 5, y, RX1 - RX0 + 10, ROW_H - 3, g(0.9), width=1.8,
                     first=first, rx=3)

    c.text((RX0, mid), name, 13.5,
           HL if current else (TEXT if counted else TEXT_DIM), "lm",
           bold=current)
    # the prince, only on the verse that names him — twelve of these on screen
    # at once would be twelve lines of text the listener is already hearing
    if prince_now:
        c.text((RX0 + 96, mid), PRINCE[name], 10.5, GOLD, "lm", italic=True)

    c.rect(BAR_X, mid - 6.5, BAR_W, 13, fill=BG, stroke=SAND_DIM, width=1,
           rx=2)
    if counted:
        stated = v == (COUNT_V[name] if ch == 1 else CH2_COUNT_V[name])
        c.grow_rect(BAR_X, mid - 6.5, bar_w(COUNT[name]), 13,
                    fill=dim(col, 255 if current else 200), rx=2,
                    w_from=0 if stated else bar_w(COUNT[name]))
    c.text((RX1, mid), num(COUNT[name]) if counted else "—", 12.5,
           HL if current else (TEXT if counted else SAND_DIM), "rm",
           bold=current)


def draw_levi_row(c, ch, v):
    """Levi's row is drawn like the others and then held empty — the chapter
    makes a point of the tribe that is not in the total."""
    lit = (ch == 1 and v >= 47) or (ch == 2 and v >= 33)
    c.raw([f'<rect x="{RX0 - 5}" y="{LEVI_Y}" width="{RX1 - RX0 + 10}" '
           f'height="{LEVI_H}" rx="3" fill="none" '
           f'stroke="rgb{SILVER if lit else SAND_DIM}" stroke-width="1.2" '
           f'stroke-dasharray="5 4"/>'])
    mid = LEVI_Y + LEVI_H / 2
    c.text((RX0, mid), "Levi", 13.5, SILVER if lit else TEXT_DIM, "lm",
           bold=lit)
    c.text((RX0 + 96, mid), "not counted", 10.5,
           SILVER if lit else SAND_DIM, "lm", italic=True)
    if lit:
        c.pulse_rect(RX0 - 5, LEVI_Y, RX1 - RX0 + 10, LEVI_H, g(0.8),
                     width=1.8, first=(v in (47, 33)), rx=3)


def draw_total(c, ch, v):
    running = counted_total(ch, v)
    done = (ch == 1 and v >= 46) or ch == 2
    mid = TOT_Y + TOT_H / 2
    c.rect(RX0 - 5, TOT_Y, RX1 - RX0 + 10, TOT_H, fill=PANEL, stroke=None,
           rx=3)
    c.text((RX0, mid), "TOTAL", 14, GOLD if done else TEXT, "lm", bold=True)
    c.rect(BAR_X, mid - 7.5, BAR_W, 15, fill=BG, stroke=SAND_DIM, width=1,
           rx=2)
    if running:
        prev = counted_total(ch, v - 1) if ch == 1 and v > 1 else running
        c.grow_rect(BAR_X, mid - 7.5, BAR_W * running / GRAND_TOTAL, 15,
                    fill=dim(GOLD, 235) if done else dim(SAND, 235), rx=2,
                    w_from=BAR_W * prev / GRAND_TOTAL)
    c.text((RX1, mid), num(running) if running else "—", 15,
           GOLD if done else TEXT, "rm", bold=True)


def draw_roster(c, ch, v):
    c.text((RX0, HEAD_Y), "THE CENSUS", 16, GOLD if ch == 1 else SAND_DIM,
           "la", bold=True)
    for i, (name, *_rest) in enumerate(TRIBES):
        draw_roster_row(c, i, name, ch, v)
    draw_levi_row(c, ch, v)
    draw_total(c, ch, v)


# ---------------------------------------------------------------------------
# Assemble one verse
# ---------------------------------------------------------------------------

TITLES = {1: "Numbers 1 · The Census", 2: "Numbers 2 · The Camp"}


def render(ch, v):
    c = SvgCanvas(W, H, bg=BG)
    c.text((28, 24), TITLES[ch], 22, TEXT, "la", bold=True)
    draw_plan(c, ch, v)
    draw_roster(c, ch, v)
    return c


def main():
    total = count = 0
    for ch in (1, 2):
        for v in range(1, CH_LEN[ch] + 1):
            c = render(ch, v)
            out = out_path("Numbers", ch, f"Numbers_{ch}_{v}.svg")
            c.save(out)
            total += os.path.getsize(out)
            count += 1
    print(f"Numbers 1-2: {count} SVG files, {total/1e3:.0f} KB")


if __name__ == "__main__":
    main()
