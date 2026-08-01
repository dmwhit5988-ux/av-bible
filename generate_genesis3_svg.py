"""Render Genesis 3 (the fall) as per-verse vector SVGs.

The chapter has no numbers, no geography and no genealogy to hang a diagram on
— what it has is a *reversal*. Nearly every line undoes something Genesis 2
established, and it is carried almost entirely by speech. So the graphic is
built from those two facts:

* a **speaker strip** across the top — the serpent, the woman, the man, Yahweh
  God — with an arc drawn from speaker to hearer on every verse that is
  dialogue. The blame arcs of verses 12-13 stay on screen once drawn, so the
  chain (God → the man → the woman → the serpent) reads whole.
* a **before/after ledger** down the side, pairing each Genesis 2 statement
  with the verse that reverses it: not ashamed → coverings sewn; God walking
  in the garden → hidden among the trees; cultivate and keep → thorns and
  sweat; the breath of life → to dust you shall return; the tree of life at
  hand → a sword guards the way.

The body of the stage runs in three modes, because the chapter changes
register twice: the garden (1-13), the three sentences as a triptych (14-19),
and the expulsion (20-24). Colours and the garden's own shapes come from
generate_genesis2_svg, so reading chapter 2 into chapter 3 stays in one place.

Verse 24's "flaming sword which turned every way" is the one element given
perpetual motion — the text asks for it outright, the same licence the
tabernacle's breathing glow has.

Run inside the project venv:
    .venv\\Scripts\\python.exe generate_genesis3_svg.py
"""

import math
import os

from svg_surface import SvgCanvas
from generate_tabernacle import (W, H, BG, PANEL, SAND, SAND_DIM, SILVER, TEXT,
                                 TEXT_DIM, GOLD, HL, BROWN, out_path)
# the garden's own palette, so chapters 2 and 3 read as one place
from generate_genesis2_svg import GREEN, GREEN_DIM, EARTH, RED

def g(alpha):
    return HL + (int(255 * alpha),)


def dim(color, a):
    """`color` with an 0-255 alpha, in the (r, g, b, a) form SvgCanvas takes."""
    return color + (int(a),)


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

SCENE = (24, 86, 700, 556)
PANEL_X = 716

STRIP_Y, STRIP_H = 96, 42          # the speaker strip
ARC_Y = STRIP_Y + STRIP_H          # arcs hang below it
GROUND_Y = 512

# the garden, carried over from Genesis 2's plan
GX, GY, GRX, GRY = 330, 355, 200, 128
KNOW = (400, 400, 34)              # tree of knowledge: x, base y, canopy r
LIFE = (215, 372, 24)              # tree of life
WOMAN_XY = (320, 455)
MAN_XY = (368, 455)

# east gate (verses 23-24)
GATE_X, GATE_Y = 530, 355
OUT_W, OUT_M = (600, 452), (642, 452)

ACTORS = [
    ("SERPENT", "the serpent", 36),
    ("WOMAN", "the woman", 200),
    ("MAN", "the man", 364),
    ("GOD", "Yahweh God", 528),
]
CHIP_W = 150
CENTER = {key: x + CHIP_W / 2 for key, _l, x in ACTORS}

# ---------------------------------------------------------------------------
# Who speaks to whom.  verse -> (speaker, hearer or None)
# ---------------------------------------------------------------------------

EXCHANGE = {
    1: ("SERPENT", "WOMAN"), 2: ("WOMAN", "SERPENT"), 3: ("WOMAN", "SERPENT"),
    4: ("SERPENT", "WOMAN"), 5: ("SERPENT", "WOMAN"),
    9: ("GOD", "MAN"), 10: ("MAN", "GOD"), 11: ("GOD", "MAN"),
    12: ("MAN", "WOMAN"), 13: ("WOMAN", "SERPENT"),
    14: ("GOD", "SERPENT"), 15: ("GOD", "SERPENT"), 16: ("GOD", "WOMAN"),
    17: ("GOD", "MAN"), 18: ("GOD", "MAN"), 19: ("GOD", "MAN"),
    20: ("MAN", "WOMAN"), 21: ("GOD", "MAN"), 22: ("GOD", None),
    23: ("GOD", "MAN"), 24: ("GOD", "MAN"),
}
# the two arcs that make the blame chain — kept on screen once drawn
BLAME = [(12, "MAN", "WOMAN"), (13, "WOMAN", "SERPENT")]

# verses 6-8 are action rather than speech: the strip goes quiet and the
# scene itself (the fruit passing, the eyes, the hiding) carries the verse


def mode(v):
    return "garden" if v <= 13 else ("sentences" if v <= 19 else "expulsion")


# ---------------------------------------------------------------------------
# The three sentences (verses 14-19).  column -> [(verse, line)]
# ---------------------------------------------------------------------------

COLUMNS = [
    ("SERPENT", "THE SERPENT", 36, 210, [
        (14, "cursed"),
        (14, "on your belly"),
        (14, "eating dust"),
        (15, "hostility"),
        (15, "head · heel"),
    ]),
    ("WOMAN", "THE WOMAN", 258, 210, [
        (16, "pain in childbirth"),
        (16, "desire"),
        (16, "he will rule"),
    ]),
    ("MAN", "THE MAN", 480, 210, [
        (17, "the ground cursed"),
        (17, "labor"),
        (18, "thorns & thistles"),
        (19, "sweat"),
        (19, "to dust"),
    ]),
]

# ---------------------------------------------------------------------------
# The ledger: Genesis 2 read against Genesis 3.  (verse, before, after)
# ---------------------------------------------------------------------------

LEDGER = [
    (7, "not ashamed", "fig leaves", "2:25 → 3:7"),
    (8, "God walking", "hidden", "3:8"),
    (12, "eat freely", "you ate", "2:16 → 3:12"),
    (18, "keep the garden", "thorns & sweat", "2:15 → 3:18"),
    (19, "the breath of life", "to dust", "2:7 → 3:19"),
    (24, "the tree of life", "the sword", "2:9 → 3:24"),
]


# ---------------------------------------------------------------------------
# Shared shapes (tuned larger than Genesis 2's, this chapter being a close-up)
# ---------------------------------------------------------------------------

def tree(c, x, base, r, lit=False, forbidden=False, dead=False,
         label=None, ring=False):
    cy = base - r - 8
    trunk = BROWN if not lit else GOLD
    c.rect(x - 4, cy + r - 2, 8, base - cy - r + 2, fill=trunk)
    canopy = dim(GREEN, 235) if not dead else dim(EARTH, 220)
    c.circle(x, cy, r, fill=canopy, stroke=HL if lit else GREEN_DIM,
             width=2.5 if lit else 1.5)
    if ring:
        c.circle(x, cy, r + 8, stroke=g(0.85), width=2)
    if forbidden:
        c.line((x - r * 0.5, cy - r * 0.5), (x + r * 0.5, cy + r * 0.5), RED, 3)
        c.line((x + r * 0.5, cy - r * 0.5), (x - r * 0.5, cy + r * 0.5), RED, 3)
    if label:
        c.text((x, cy - r - 10), label, 13, HL if lit else TEXT_DIM, "mb",
               bold=lit, italic=not lit)


def figure(c, x, y, lit=True, covering=None, hiding=False, label=None,
           scale=1.0):
    """A schematic figure. `covering` = None | 'leaves' | 'skins'."""
    col = HL if lit else (TEXT_DIM if not hiding else dim(TEXT_DIM, 130))
    h = 15 * scale
    c.circle(x, y - h - 7 * scale, 5.5 * scale, fill=col)
    c.line((x, y - h), (x, y), col, 2.6)
    c.line((x - 7 * scale, y - h + 5), (x + 7 * scale, y - h + 5), col, 2.4)
    c.line((x, y), (x - 5.5 * scale, y + 10 * scale), col, 2.4)
    c.line((x, y), (x + 5.5 * scale, y + 10 * scale), col, 2.4)
    if covering:
        fill = GREEN if covering == "leaves" else BROWN
        c.rect(x - 8 * scale, y - 9 * scale, 16 * scale, 10 * scale,
               fill=fill, stroke=SAND_DIM, width=1)
    if label:
        c.text((x, y + 24 * scale), label, 12, col, "mt", italic=True)


def eyes(c, x, y, opened):
    """The promise of verse 5, kept in verse 7."""
    for dx in (-7, 7):
        if opened:
            c.ellipse(x + dx, y, 5, 3.4, fill=None, stroke=GOLD, width=1.6)
            c.circle(x + dx, y, 1.5, fill=GOLD)
        else:
            c.polyline([(x + dx - 5, y), (x + dx, y + 2), (x + dx + 5, y)],
                       stroke=dim(TEXT_DIM, 200), width=1.4)


# ---------------------------------------------------------------------------
# The speaker strip
# ---------------------------------------------------------------------------

def arc(c, frm, to, color, width, dip=26):
    x1, x2 = CENTER[frm], CENTER[to]
    mx = (x1 + x2) / 2
    c.path(f"M{x1},{ARC_Y} Q{mx},{ARC_Y + dip} {x2},{ARC_Y}",
           fill=None, stroke=color, width=width)
    d = 1 if x2 > x1 else -1
    c.polygon([(x2, ARC_Y), (x2 - d * 7, ARC_Y + 8), (x2 - d * 12, ARC_Y + 1)],
              fill=color)


def draw_strip(c, v):
    speaker, hearer = EXCHANGE.get(v, (None, None))
    prev_speaker = EXCHANGE.get(v - 1, (None, None))[0]
    for key, label, x in ACTORS:
        live = (key == speaker)
        heard = (key == hearer)
        c.rect(x, STRIP_Y, CHIP_W, STRIP_H, fill=PANEL if live else BG,
               stroke=None if live else (GOLD if heard else SAND_DIM),
               width=1.5, rx=4)
        if live:
            # a brief brighten only when the speaker actually changes — the
            # strip switches on most verses, and re-drawing the ring each time
            # is just noise
            c.pulse_rect(x, STRIP_Y, CHIP_W, STRIP_H, g(0.95), width=2.5,
                         first=(key != prev_speaker), rx=4, dur="0.6s")
        c.text((x + CHIP_W / 2, STRIP_Y + 16), label, 15,
               HL if live else (TEXT if heard else TEXT_DIM), "mm", bold=live)
        tag = "speaks" if live else ("hears" if heard else "")
        c.text((x + CHIP_W / 2, STRIP_Y + 32), tag, 10, GOLD, "mm",
               italic=True)

    for bv, bf, bt in BLAME:            # the blame chain, once drawn, stays
        if v > bv:
            arc(c, bf, bt, dim(SAND, 190), 1.5)
    if speaker and hearer:
        arc(c, speaker, hearer, g(0.9), 2.5)


# ---------------------------------------------------------------------------
# Mode 1: the garden (verses 1-13)
# ---------------------------------------------------------------------------

def draw_garden_body(c, v, expelled=False):
    """The garden. `expelled` draws the post-sentence state: gate, cherubim,
    the pair outside."""
    hiding = (v == 8)
    c.ellipse(GX, GY, GRX, GRY, fill=dim(GREEN_DIM, 110),
              stroke=GREEN_DIM, width=2)
    c.text((GX, GY - GRY - 12), "THE GARDEN IN EDEN", 13, TEXT_DIM, "mb",
           italic=True)
    for dx, dy in ((-150, -60), (-58, -96), (46, -98), (140, -50),
                   (156, 30), (60, 96), (-46, 100), (-160, 20)):
        c.circle(GX + dx, GY + dy, 11, fill=dim(GREEN, 130), stroke=GREEN_DIM,
                 width=1)
    c.line((SCENE[0] + 8, GROUND_Y), (SCENE[2] - 8, GROUND_Y),
           dim(EARTH, 220), 9)

    # the cool of the day sweeps the garden
    if v == 8:
        c.rect(GX - GRX, GY - 66, GRX * 2, 44, fill=dim(SILVER, 40))
        c.text((GX, GY - 74), "the cool of the day", 12, SILVER, "mb",
               italic=True)

    # the two trees
    lx, lbase, lr = LIFE
    kx, kbase, kr = KNOW
    tree(c, lx, lbase, lr, lit=(v in (22,)), ring=(v == 22),
         label="the tree of life")
    tree(c, kx, kbase, kr, lit=(v in (3, 6)),
         forbidden=(3 <= v <= 3) or (v >= 11 and not expelled),
         label="knowledge of good and evil")
    if v == 4:      # the denial: the prohibition itself struck through
        c.line((kx - 54, kbase - kr - 8), (kx + 54, kbase - kr - 8),
               dim(RED, 170), 2, dash="6,5")

    # the serpent, tracing itself along the branch
    if v <= 13:
        snake = [(432, 340), (410, 330), (388, 338), (366, 352), (348, 372),
                 (336, 396), (332, 420)]
        if v == 1:
            c.traced(snake, stroke=dim(SAND, 240), width=4, dur="2.2s")
        elif v <= 5 or v == 13:
            c.polyline(snake, stroke=dim(SAND, 200), width=3)
        else:
            c.polyline(snake, stroke=dim(SAND_DIM, 220), width=2)
        c.circle(snake[-1][0], snake[-1][1], 4.5,
                 fill=HL if (v <= 5 or v == 13) else dim(SAND_DIM, 220))

    # verse 6: the fruit passing from the tree to her, and from her to him
    if v == 6:
        c.path(f"M{kx - 10},{kbase - kr - 8} Q{kx - 40},{kbase - 30} "
               f"{WOMAN_XY[0] + 10},{WOMAN_XY[1] - 20}",
               fill=None, stroke=GOLD, width=2)
        c.circle(WOMAN_XY[0] + 12, WOMAN_XY[1] - 18, 5, fill=GOLD)
        c.circle(MAN_XY[0] + 12, MAN_XY[1] - 18, 5, fill=GOLD)
        c.line((WOMAN_XY[0] + 18, WOMAN_XY[1] - 18),
               (MAN_XY[0] + 6, MAN_XY[1] - 18), GOLD, 2)

    # the pair
    covering = None
    if v >= 21:
        covering = "skins"
    elif v >= 7:
        covering = "leaves"
    if expelled and v >= 23:
        figure(c, *OUT_W, lit=True, covering=covering)
        figure(c, *OUT_M, lit=True, covering=covering)
    else:
        wx, wy = WOMAN_XY
        mx, my = MAN_XY
        if hiding:                      # behind the trees
            wx, mx = 250, 292
        figure(c, wx, wy, lit=(v in (2, 3, 6, 7, 13, 16, 20)),
               covering=covering, hiding=hiding,
               label="Eve" if v >= 20 else None)
        figure(c, mx, my, lit=(v in (6, 7, 10, 12, 17)), covering=covering,
               hiding=hiding)
        if v >= 5:
            eyes(c, wx, wy - 44, opened=(v >= 7))
            eyes(c, mx, my - 44, opened=(v >= 7))

    # the east gate
    if expelled:
        gate_open = v >= 23
        col = GOLD if gate_open else SAND_DIM
        c.line((GATE_X, GATE_Y - 40), (GATE_X + 16, GATE_Y - 40), col, 2.5)
        c.line((GATE_X, GATE_Y + 40), (GATE_X + 16, GATE_Y + 40), col, 2.5)
        c.text((GATE_X + 8, GATE_Y + 56), "the east", 11, TEXT_DIM, "mt",
               italic=True)
        if v == 23:
            c.polyline([(GX + 90, GY), (GATE_X + 40, GY)], stroke=GOLD,
                       width=2, dash="5,5")
        if v == 24:
            cherub(c, GATE_X + 14, GATE_Y - 62)
            cherub(c, GATE_X + 14, GATE_Y + 62)
            sword(c, GATE_X + 46, GATE_Y)


def cherub(c, x, y):
    """A guardian: a narrow body between two upswept wings."""
    c.polygon([(x, y - 14), (x + 6, y), (x, y + 14), (x - 6, y)],
              fill=dim(SILVER, 210), stroke=SILVER, width=1.4)
    for s in (-1, 1):
        c.path(f"M{x + s * 6},{y - 4} Q{x + s * 24},{y - 16} "
               f"{x + s * 20},{y + 8}", fill=None, stroke=SILVER, width=2)


def _tongue(a_deg, r0, r1, sweep, half):
    """One flame tongue as a path: a tapered shape leaving the core at angle
    `a_deg` and curving `sweep` degrees round as it reaches out to `r1`."""
    def pol(r, deg):
        rad = math.radians(deg)
        return r * math.cos(rad), r * math.sin(rad)

    b1 = pol(r0, a_deg - half)
    b2 = pol(r0, a_deg + half)
    tip = pol(r1, a_deg + sweep)
    c1 = pol((r0 + r1) * 0.55, a_deg + sweep * 0.3 - half * 0.7)
    c2 = pol((r0 + r1) * 0.55, a_deg + sweep * 0.8 + half * 0.9)
    f = lambda p: f"{p[0]:.1f},{p[1]:.1f}"
    return (f"M{f(b1)} Q{f(c1)} {f(tip)} Q{f(c2)} {f(b2)} Z")


def sword(c, x, y):
    """The flaming sword of verse 24 — drawn as a wheel of fire.

    The text's emphasis is that it *turned every way*, so the emblem is
    radially symmetric: five tongues sweeping out of a bright core, rather
    than one blade. A single elongated blade would pass through a vertical
    reading at some point in every rotation; a wheel never does. It also means
    the reduced-motion still — which strips the rotation — keeps reading as
    something turning, because the sweep of the tongues carries it.
    """
    c.raw([f'<g transform="translate({x},{y})">'
           f'<animateTransform attributeName="transform" type="rotate" '
           f'values="0;360" dur="7s" begin="0s" repeatCount="indefinite" '
           f'additive="sum"/>'])
    # Outer flame: seven tongues, alternating long and short. The uneven
    # lengths and the strong curl keep it reading as fire rather than as a
    # flower, which even spacing and equal petals would give.
    for k in range(7):
        r1 = 40 if k % 2 == 0 else 29
        c.path(_tongue(k * 360 / 7, 12, r1, 42, 7), fill=dim(RED, 230),
               stroke=GOLD, width=1.2)
    for k in range(5):                       # inner, brighter flame
        c.path(_tongue(k * 72 + 18, 6, 21, 34, 6), fill=GOLD, stroke=HL,
               width=1)
    c.circle(0, 0, 6.5, fill=HL, stroke=GOLD, width=1.5)
    c.raw(["</g>"])


# ---------------------------------------------------------------------------
# Mode 2: the three sentences (verses 14-19)
# ---------------------------------------------------------------------------

def draw_sentences(c, v):
    c.text((SCENE[0] + 8, 176), "THREE SENTENCES", 15, GOLD, "la", bold=True)
    for key, header, x, w, lines in COLUMNS:
        active = any(lv == v for lv, _t in lines)
        c.rect(x, 196, w, 300, fill=PANEL if active else BG,
               stroke=GOLD if active else SAND_DIM, width=1.5, rx=5)
        c.text((x + w / 2, 214), header, 15, HL if active else TEXT_DIM, "mm",
               bold=active)
        y = 244
        for lv, text in lines:
            lit = (lv == v)
            past = (lv < v)
            c.circle(x + 16, y, 3.4 if not lit else 5,
                     fill=HL if lit else (SAND if past else BG),
                     stroke=SAND_DIM, width=1.2)
            c.text((x + 28, y), text, 12,
                   HL if lit else (TEXT if past else dim(TEXT_DIM, 150)),
                   "lm", bold=lit)
            y += 26
    # verse 15 — the one thread of promise, between the first two columns
    if v >= 15:
        lit = (v == 15)
        y = 452
        c.polyline([(160, y), (360, y)], stroke=GOLD if lit else dim(GOLD, 150),
                   width=2.5 if lit else 1.5, dash=None if lit else "5,5")
        c.text((150, y + 14), "his heel", 11, GOLD if lit else TEXT_DIM, "rm")
        c.text((370, y + 14), "your head", 11, GOLD if lit else TEXT_DIM, "lm")
    # verse 18 — thorns out of the ground; verse 19 — back to dust
    c.line((SCENE[0] + 8, GROUND_Y), (SCENE[2] - 8, GROUND_Y),
           dim(EARTH, 220), 9)
    if v >= 18:
        for i in range(7):
            tx = 496 + i * 28
            pts = [(tx, GROUND_Y - 4), (tx - 6, GROUND_Y - 20),
                   (tx + 5, GROUND_Y - 30), (tx - 3, GROUND_Y - 44)]
            if v == 18:
                c.traced(pts, stroke=dim(BROWN, 240), width=2, dur="1.8s")
            else:
                c.polyline(pts, stroke=dim(BROWN, 200), width=1.8)
    if v == 19:
        c.polyline([(586, 500), (586, GROUND_Y - 4)], stroke=GOLD, width=2)
        c.polygon([(586, GROUND_Y + 2), (581, GROUND_Y - 8),
                   (591, GROUND_Y - 8)], fill=GOLD)
        c.text((586, GROUND_Y + 16), "dust", 12, HL, "mt", italic=True)


# ---------------------------------------------------------------------------
# The ledger panel
# ---------------------------------------------------------------------------

def draw_panel(c, v):
    c.text((PANEL_X, 92), "WHAT IS UNDONE", 18, TEXT, "la", bold=True)
    c.text((PANEL_X, 114), "Genesis 2 → Genesis 3", 11,
           TEXT_DIM, "la", italic=True)
    y = 142
    for lv, before, after, ref in LEDGER:
        lit = (lv == v)
        done = (v > lv)
        c.text((PANEL_X + 4, y), before, 11,
               TEXT_DIM if (lit or done) else dim(TEXT_DIM, 140), "la",
               italic=True)
        c.text((PANEL_X + 4, y + 15), "↓", 11,
               GOLD if lit else (SAND_DIM if not done else SAND), "la")
        c.text((PANEL_X + 20, y + 15), after, 12,
               HL if lit else (TEXT if done else dim(TEXT_DIM, 150)), "la",
               bold=lit)
        c.text((W - 16, y + 15), ref, 10,
               GOLD if lit else dim(TEXT_DIM, 170), "ra", italic=True)
        if lit:
            c.rect(PANEL_X - 6, y - 6, W - PANEL_X - 4, 44, stroke=g(0.7),
                   width=1.5, rx=3)
        y += 58


# ---------------------------------------------------------------------------
# Assemble one verse
# ---------------------------------------------------------------------------

def render(v):
    c = SvgCanvas(W, H, bg=BG)
    c.text((28, 24), "Genesis 3 · The Garden Undone", 22, TEXT, "la",
           bold=True)

    m = mode(v)
    if m == "sentences":
        draw_sentences(c, v)
    else:
        draw_garden_body(c, v, expelled=(m == "expulsion"))
    draw_strip(c, v)
    draw_panel(c, v)
    return c


def main():
    total = count = 0
    for v in range(1, 25):
        c = render(v)
        out = out_path("Genesis", 3, f"Genesis_3_{v}.svg")
        c.save(out)
        total += os.path.getsize(out)
        count += 1
    print(f"Genesis 3: {count} SVG files, {total/1e3:.0f} KB")


if __name__ == "__main__":
    main()
