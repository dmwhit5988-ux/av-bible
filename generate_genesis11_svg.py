"""Render Genesis 11:1-9 (Babel) as per-verse vector SVGs.

Nine verses, and the whole passage runs on one axis: men build **up** ("a
tower whose top reaches to the sky"), and God comes **down** (v5 "came down to
see", v7 "let's go down"). So the stage is vertical — the plain of Shinar at
the foot, a ziggurat rising course by course, the sky band far above it, and
the descent arriving from off-frame above. The tower's top never gets near the
sky band: that gap is the passage's own irony, left visible rather than
narrated.

Two other things the chapter gives, both drawn:

* the **language**. Verse 1's "one language, one speech" is a single band; at
  verse 7 it breaks into threads, coloured with the three line colours from
  Genesis 10 so that chapter 11 visibly explains chapter 10's seventy nations.
* the **place**. A map inset reuses generate_genesis10_svg's coastlines and
  bands at a smaller scale, marking Shinar; the migration arrives from the
  east in verse 2 and the scattering fires back out of it in verses 8-9.

The side panel carries the three summons — "Come, let's make bricks" (v3, up),
"Come, let's build… let's make a name" (v4, up), "Come, let's go down and
confuse" (v7, down). Two ascending, one descending.

Genesis 11:10-32 belongs to the genealogy family (generate_genealogy_svg.py);
this generator owns verses 1-9 only, which is why svg_generators.json carries
a "verses" range for both.

Run inside the project venv:
    .venv\\Scripts\\python.exe generate_genesis11_svg.py
"""

import os

from svg_surface import SvgCanvas
from generate_tabernacle import (W, H, BG, PANEL, SAND, SAND_DIM, SILVER, TEXT,
                                 TEXT_DIM, GOLD, HL, BROWN, out_path)
from generate_tribal_maps import MapFrame, SEA, LAND, WATER_TXT
# the Table of Nations' own world, reused at inset scale
from generate_genesis10_svg import (MEDITERRANEAN, RED_SEA, PERSIAN_GULF,
                                    SOUTH_SEA, BLACK_SEA, CASPIAN, BANDS,
                                    C_JAPHETH, C_HAM, C_SHEM)


BRICK = (146, 96, 66)
BRICK_DIM = (92, 62, 44)
TAR = (58, 50, 46)
THREADS = [C_JAPHETH, C_HAM, C_SHEM, (176, 148, 200), (200, 168, 108),
           (120, 172, 176), (196, 128, 148)]


def g(alpha):
    return HL + (int(255 * alpha),)


def dim(color, a):
    """`color` with an 0-255 alpha, in the (r, g, b, a) form SvgCanvas takes."""
    return color + (int(a),)


# ---------------------------------------------------------------------------
# Layout — the vertical axis
# ---------------------------------------------------------------------------

SCENE = (24, 86, 700, 556)
SKY_Y, SKY_H = 100, 34             # "the sky" the tower claims to reach
LANG_Y, LANG_H = 148, 26           # the one-language band
PLAIN_Y = 508                      # the plain of Shinar
TOWER_CX = 300

# the ziggurat: (course width, height), base course first
COURSES = [(260, 34), (224, 32), (190, 30), (158, 28), (128, 26), (100, 24),
           (74, 22)]
# how many courses stand at each verse (the seventh is never finished)
COURSES_AT = {1: 0, 2: 0, 3: 2, 4: 6, 5: 6, 6: 6, 7: 6, 8: 6, 9: 6}

PANEL_X = 716
MAP_RECT = (PANEL_X, 96, W - 16, 292)
MF = MapFrame(10.0, 48.0, 0.0, 62.0, MAP_RECT)
SHINAR = (32.4, 44.8)              # the plain, as Genesis 10 places it

# ---------------------------------------------------------------------------
# The three summons.  (verse, direction, text)
# ---------------------------------------------------------------------------

SUMMONS = [
    (3, "up", "“Come, let’s make bricks”", "and burn them thoroughly"),
    (4, "up", "“Come, let’s build ourselves a city”", "and make a name for us"),
    (7, "down", "“Come, let’s go down”", "and confuse their language"),
]

# the four quarters the scattering fires into (lat, lon)
QUARTERS = [(44.0, 28.0), (38.0, 12.0), (18.0, 30.0), (20.0, 54.0),
            (42.0, 56.0)]


# ---------------------------------------------------------------------------
# The tower
# ---------------------------------------------------------------------------

def course_rect(i):
    """(x, y, w, h) of course i (0 = base), stacked up from the plain."""
    y = PLAIN_Y
    for w, h in COURSES[:i]:
        y -= h
    w, h = COURSES[i]
    return TOWER_CX - w / 2, y - h, w, h


def draw_tower(c, v):
    built = COURSES_AT[v]
    stopped = (v >= 8)
    if v <= 2:      # nothing built yet — show the site, as the ark does
        for i in range(len(COURSES)):
            x, y, w, h = course_rect(i)
            c.rect(x, y, w, h, fill=None, stroke=dim(SAND_DIM, 150), width=1.2)
        return
    for i in range(len(COURSES)):
        x, y, w, h = course_rect(i)
        if i < built:
            fresh = (v == 3 and i < 2) or (v == 4 and 2 <= i < 6)
            c.rect(x, y, w, h, fill=dim(BRICK, 225),
                   stroke=HL if fresh else SAND, width=2 if fresh else 1.5)
            # brick coursing
            rows = max(1, int(h / 11))
            for r in range(1, rows):
                yy = y + r * (h / rows)
                c.line((x + 2, yy), (x + w - 2, yy), dim(TAR, 190), 1)
            for r in range(rows):
                yy = y + r * (h / rows) + (h / rows) / 2
                step = 26
                off = 13 if r % 2 else 0
                bx = x + off + 6
                while bx < x + w - 6:
                    c.line((bx, yy - (h / rows) / 2 + 1),
                           (bx, yy + (h / rows) / 2 - 1), dim(TAR, 150), 1)
                    bx += step
        elif i == built and not stopped and v >= 4:
            c.rect(x, y, w, h, fill=None, stroke=SAND_DIM, width=1.5)
        elif i == built and stopped:
            c.rect(x, y, w, h, fill=None, stroke=dim(SAND_DIM, 200), width=1.5)
            c.text((TOWER_CX, y + h / 2), "unfinished", 11, TEXT_DIM, "mm",
                   italic=True)

    if built:
        top_y = course_rect(built - 1)[1]
        if v == 4:      # their claim, and the distance it falls short
            c.polyline([(TOWER_CX, top_y - 6), (TOWER_CX, SKY_Y + SKY_H + 8)],
                       stroke=GOLD, width=1.5, dash="5,6")
        if v == 3:
            materials(c, top_y)


def materials(c, top_y):
    """Verse 3's substitutions, as a two-row callout."""
    x, y = 470, 300
    c.rect(x, y, 210, 74, fill=PANEL, stroke=GOLD, width=1.5, rx=4)
    c.text((x + 12, y + 17), "brick   for stone", 13, HL, "lm")
    c.text((x + 12, y + 40), "tar      for mortar", 13, HL, "lm")
    c.rect(x + 150, y + 10, 18, 12, fill=dim(BRICK, 235), stroke=SAND,
           width=1)
    c.rect(x + 150, y + 33, 18, 12, fill=dim(TAR, 235), stroke=SAND, width=1)


def draw_plain(c, v):
    c.line((SCENE[0] + 8, PLAIN_Y), (SCENE[2] - 8, PLAIN_Y),
           dim(BROWN, 220), 10)
    if v == 2:      # travelling from the east
        pts = [(SCENE[2] - 20, PLAIN_Y - 22), (520, PLAIN_Y - 30),
               (420, PLAIN_Y - 24), (TOWER_CX + 60, PLAIN_Y - 18)]
        c.traced(pts, stroke=g(0.9), width=3, dur="2.0s")
        c.polygon([(TOWER_CX + 48, PLAIN_Y - 18), (TOWER_CX + 62, PLAIN_Y - 24),
                   (TOWER_CX + 62, PLAIN_Y - 12)], fill=HL)


def draw_sky(c, v):
    c.rect(SCENE[0] + 8, SKY_Y, SCENE[2] - SCENE[0] - 16, SKY_H,
           fill=dim(SILVER, 26), stroke=dim(SILVER, 90), width=1)
    c.text((SCENE[0] + 20, SKY_Y + SKY_H / 2), "the sky", 13,
           dim(SILVER, 220), "lm", italic=True)
    # the descent — from above the frame, straight past the tower's claim
    if v in (5, 7):
        x = TOWER_CX + 150
        c.polyline([(x, SCENE[1] - 2), (x, 300)], stroke=g(0.95), width=3,
                   dash="7,6")
        c.polygon([(x, 314), (x - 7, 298), (x + 7, 298)], fill=HL)


def draw_language(c, v):
    """One band, then seven threads."""
    x0, x1 = SCENE[0] + 8, SCENE[2] - 8
    if v <= 6:
        lit = v in (1, 6)
        c.rect(x0, LANG_Y, x1 - x0, LANG_H, fill=dim(GOLD, 60),
               stroke=GOLD if lit else dim(GOLD, 140), width=2 if lit else 1.5,
               rx=4)
        text = ("ONE LANGUAGE  ·  ONE SPEECH" if v <= 5
                else "ONE PEOPLE  ·  ONE LANGUAGE  ·  NOTHING WITHHELD")
        c.text(((x0 + x1) / 2, LANG_Y + LANG_H / 2), text, 14,
               HL if lit else TEXT_DIM, "mm", bold=lit)
        return
    # verse 7 onward: the band has become many
    n = len(THREADS)
    seg = (x1 - x0) / n
    for i, col in enumerate(THREADS):
        bx = x0 + i * seg
        if v == 7:      # each thread peels away from the one band
            pts = [(bx + seg / 2, LANG_Y), (bx + seg / 2 - 12, LANG_Y + 16),
                   (bx + seg / 2 + 8, LANG_Y + 30)]
            c.traced(pts, stroke=col, width=3, dur="1.8s")
        c.rect(bx + 3, LANG_Y, seg - 6, LANG_H * 0.7, fill=dim(col, 150),
               stroke=col, width=1.2, rx=3)


def draw_name(c, v):
    if v < 9:
        return
    x, y, w, h = 430, 366, 250, 74
    c.rect(x, y, w, h, fill=PANEL, stroke=None, width=1.5, rx=5)
    c.pulse_rect(x, y, w, h, g(0.95), width=2.5, first=True, rx=5)
    c.text((x + w / 2, y + h / 2), "BABEL", 26, HL, "mm", bold=True)


# ---------------------------------------------------------------------------
# The map inset — Genesis 10's world, at inset scale
# ---------------------------------------------------------------------------

def _ell(spec):
    lat, lon, rx, ry = spec
    return MF.pt(lat, lon), rx * MF.eff * MF.s, ry * MF.s


def draw_map(c, v):
    c.text((PANEL_X, 76), "THE PLAIN OF SHINAR", 13, TEXT, "la", bold=True)
    with c.group(MF.px, MF.py, clip=(MF.mw, MF.mh)):
        c.rect(0, 0, MF.mw, MF.mh, fill=LAND)
        for key, (poly, _label) in BANDS.items():
            col = {"JAPHETH": C_JAPHETH, "HAM": C_HAM, "SHEM": C_SHEM}[key]
            c.polygon(MF.pts(poly), fill=dim(col, 20), stroke=dim(col, 60),
                      width=1)
        for poly in (MEDITERRANEAN, RED_SEA, PERSIAN_GULF, SOUTH_SEA):
            c.polygon(MF.pts(poly), fill=SEA, stroke=dim(WATER_TXT, 110),
                      width=1)
        for spec in (BLACK_SEA, CASPIAN):
            (cx, cy), rx, ry = _ell(spec)
            c.ellipse(cx, cy, rx, ry, fill=SEA, stroke=dim(WATER_TXT, 110),
                      width=1)

        sx, sy = MF.pt(*SHINAR)
        if v == 2:
            pts = [MF.pt(34.0, 58.0), MF.pt(33.0, 51.0), (sx, sy)]
            c.traced(pts, stroke=g(0.9), width=2.5, dur="2.0s")
        if v >= 8:
            for la, lo in QUARTERS:
                qx, qy = MF.pt(la, lo)
                if v == 8:
                    c.traced([(sx, sy), (qx, qy)], stroke=g(0.85), width=2,
                             dur="2.0s")
                else:
                    c.polyline([(sx, sy), (qx, qy)], stroke=dim(GOLD, 190),
                               width=1.5)
                c.circle(qx, qy, 3, fill=GOLD)
        cur = v in (2, 8, 9)
        c.circle(sx, sy, 6 if cur else 4.5, fill=HL if cur else GOLD,
                 stroke=BG, width=1.5)
        c.text((sx + 10, sy + 4), "Shinar", 12, HL if cur else TEXT, "lm",
               bold=cur)
    c.rect(MF.px - 1, MF.py - 1, MF.mw + 1, MF.mh + 1, stroke=SAND_DIM,
           width=1)


# ---------------------------------------------------------------------------
# The panel: three summons
# ---------------------------------------------------------------------------

def draw_panel(c, v):
    y0 = 344
    c.text((PANEL_X, y0), "THREE TIMES, “COME, LET’S…”", 13, TEXT, "la",
           bold=True)
    y = y0 + 40
    for verse, direction, line, sub in SUMMONS:
        lit = (v == verse)
        past = (v > verse)
        up = (direction == "up")
        c.rect(PANEL_X, y, W - PANEL_X - 16, 52,
               fill=PANEL if (lit or past) else BG,
               stroke=None if lit else (SAND if past else SAND_DIM),
               width=1.5, rx=4)
        if lit:
            c.pulse_rect(PANEL_X, y, W - PANEL_X - 16, 52, g(0.9), width=2.5,
                         first=True, rx=4)
        ax = PANEL_X + 18
        col = GOLD if (lit or past) else SAND_DIM
        c.line((ax, y + 14), (ax, y + 38), col, 2)
        head = (y + 12) if up else (y + 40)
        tip = -1 if up else 1
        c.polygon([(ax, head + tip * 2), (ax - 5, head - tip * 7),
                   (ax + 5, head - tip * 7)], fill=col)
        c.text((ax + 16, y + 26), line, 12,
               HL if lit else (TEXT if past else TEXT_DIM), "lm", bold=lit)
        c.text((W - 24, y + 26), f"v{verse}", 10, TEXT_DIM, "rm", italic=True)
        y += 60


# ---------------------------------------------------------------------------
# Assemble one verse
# ---------------------------------------------------------------------------

def render(v):
    c = SvgCanvas(W, H, bg=BG)
    c.text((28, 24), "Genesis 11 · Babel", 22, TEXT, "la", bold=True)

    draw_sky(c, v)
    draw_language(c, v)
    draw_plain(c, v)
    draw_tower(c, v)
    draw_name(c, v)
    draw_map(c, v)
    draw_panel(c, v)
    return c


def main():
    total = count = 0
    for v in range(1, 10):
        c = render(v)
        out = out_path("Genesis", 11, f"Genesis_11_{v}.svg")
        c.save(out)
        total += os.path.getsize(out)
        count += 1
    print(f"Genesis 11:1-9: {count} SVG files, {total/1e3:.0f} KB")


if __name__ == "__main__":
    main()
