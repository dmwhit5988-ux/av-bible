"""Render the letter to the Romans (16 chapters, 433 verses) as per-verse
vector SVGs — one full-frame scene per chapter, threaded by the Romans Road.

Design and reasoning: docs/design/romans.md. Every chapter owns the whole
frame with its own set-piece, and the classic Romans Road — 3:23, 5:8, 6:23,
10:9, 10:13 — is drawn literally: a winding Roman road toward a distant arch,
gaining an engraved milestone at each of those verses. The road returns
whenever the letter does. (The earlier design, a seven-stop rail with a
per-verse bead track, is archived in backups/romans_rail/ under
config.ARCHIVE_DIR.)

Text budget (revised for this book): names, numbers, labelled parts, plus
short engraved phrases (2-7 words, WEB wording or tight paraphrase, caps)
at the hinge verses only. Nothing counts the verses: no track, no dots, no
per-verse caption word. What changes each verse is the drawing.

Run inside the project venv:
    .venv\\Scripts\\python.exe generate_romans_svg.py
"""

import math
import os

import svg_figures as F
from svg_surface import SvgCanvas
from generate_tabernacle import (W, H, BG, PANEL, SAND, SAND_DIM, TEXT,
                                 TEXT_DIM, HL, GOLD, RED, BROWN, GRAY,
                                 out_path)
from passages import verse_numbers

BOOK = "Romans"

# Colours this book needs that the tabernacle palette has no name for.
OLIVE = (122, 146, 92)           # the good olive tree
WILD = (150, 168, 104)           # the wild branches grafted in
WATER = (96, 122, 152)           # the grave-pool of chapter 6
STONE = (104, 100, 92)           # milestone rock
STONE_LIT = (188, 178, 150)      # milestone face catching light


def dim(col, a):
    """The palette colour at `a` opacity."""
    return (col[0], col[1], col[2], int(255 * a))


# ---------------------------------------------------------------------------
# Text metrics
# ---------------------------------------------------------------------------
#
# Every box drawn around a label is sized from the label's real advance width
# in the canvas font (Georgia — see svg_surface.FONT_FAMILY), never from a
# characters-times-a-guess estimate: caps in a serif face are far wider than
# such a guess, which is what clipped the engraved milestone faces.

_FONT_FILES = {(False, False): "georgia.ttf", (True, False): "georgiab.ttf",
               (False, True): "georgiai.ttf", (True, True): "georgiaz.ttf"}
_FONT_DIR = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
_font_cache, _width_cache = {}, {}

_PROBE = 64          # measure once at this size, scale linearly


def _font(bold, italic):
    key = (bold, italic)
    if key not in _font_cache:
        try:
            from PIL import ImageFont
            _font_cache[key] = ImageFont.truetype(
                os.path.join(_FONT_DIR, _FONT_FILES[key]), _PROBE)
        except Exception:
            _font_cache[key] = None
    return _font_cache[key]


def text_w(s, size, bold=False, italic=False):
    """Rendered width of `s` at `size`, in canvas units."""
    key = (s, bold, italic)
    if key not in _width_cache:
        f = _font(bold, italic)
        _width_cache[key] = (f.getlength(s) / _PROBE if f
                             else len(s) * 0.66)      # safe over-estimate
    return _width_cache[key] * size


# Verse counts are WEB's (WEB is the only text, passages.TRANSLATION); they
# place each verse on the letter's one reading line, and main() writes the
# verses passages.verse_numbers() lists. Romans 14 is the trap: the WEB,
# following the manuscripts that place the closing doxology early, prints the
# familiar Romans 16:25-27 as 14:24-26, so chapter 14 runs to 26 and
# chapter 16 ends at 24.
CH_LEN = {1: 32, 2: 29, 3: 31, 4: 25, 5: 21, 6: 23, 7: 25, 8: 39,
          9: 33, 10: 21, 11: 36, 12: 21, 13: 14, 14: 26, 15: 33, 16: 24}

_OFFSET = {}
_run = 0
for _ch in range(1, 17):
    _OFFSET[_ch] = _run
    _run += CH_LEN[_ch]


def P(ch, v):
    """Reading position: one number across the whole letter."""
    return _OFFSET[ch] + v


def since(pos, ch, v):
    """(shown, first) for an element that appears at ch:v — `first` marks
    the one verse it animates on ('draw once, then hold')."""
    p = P(ch, v)
    return pos >= p, pos == p


def header(c, ch, v):
    c.text((28, 24), f"Romans {ch}", 23, TEXT, "la", bold=True)
    c.text((28, 54), f"v{v}", 13, dim(TEXT_DIM, 0.85), "la", italic=True)


def phrase(c, xy, s, size=24, col=None, first=False):
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
# Small figure vocabulary shared by several scenes
# ---------------------------------------------------------------------------

# The people are drawn from svg_figures, so the man who stands on the altar in
# chapter 12 is the man who came up out of the grave in chapter 6 and the man
# who walked out of chapter 1 — one body through the letter, which is the
# argument the letter is making.
#
# The signature below is the stick figure's, unchanged: feet on `gy`, `h` tall,
# same `arms` and `legs` names. Every scene in this file therefore kept its
# geometry, and the swap is a swap of bodies and nothing else.

# Pixels per local unit come from a MAN's height, not from each figure's own,
# so a woman passed the same `h` arrives at her true height beside him rather
# than being stretched to his. Measured, not guessed, so it follows the
# vocabulary if the vocabulary changes.
MAN_UNITS = F.bbox((F.man(), 0))[3] - F.bbox((F.man(), 0))[2]

# The head, asked of the vocabulary rather than restated here — it is the
# topmost bare-skin disc in the parts list, which is true of every person the
# vocabulary draws and stays true if the proportions are ever retuned.
# Chapter 3 needs it: the mouth that stops at 3:19 has to land on a face, and
# on the stick figure it was measured from, the face was 5% of a body lower.
_HEAD_Y, _HEAD_R = max((d[1], d[2]) for k, d, m in F.man()
                       if k == "dot" and m == "skin")

_paint_cache = {}


def _fade(col, a):
    """`col` at `a` times whatever opacity it already carried."""
    if col is None or a >= 1.0:
        return col
    had = (col[3] / 255.0) if len(col) > 3 else 1.0
    return (col[0], col[1], col[2], int(255 * had * a))


def figure_paint(col, width):
    """The vocabulary's paint table in this scene's colour and opacity.

    Romans pushes figures back by drawing them dimmer — the grey queue of
    chapter 5, the quiet company behind the table of chapter 14 — and a paint
    table built only from the RGB would bring them all forward to full
    strength. The alpha the scene asked for is carried onto every material,
    and the old `width` argument survives as a multiplier on the linework, so
    a figure the scene wanted heavy still comes out heavy.
    """
    key = (tuple(col), width)
    if key not in _paint_cache:
        a = (col[3] / 255.0) if len(col) > 3 else 1.0
        k = width / 2.0
        _paint_cache[key] = {
            m: (_fade(fill, a), _fade(stroke, a), w * k)
            for m, (fill, stroke, w) in F.palette(tuple(col[:3]), BG).items()}
    return _paint_cache[key]


def figure(c, x, gy, h, col, width=2, arms="down", legs="stand", kind="man"):
    """A person standing on ground line `gy`, an adult man `h` tall.

    `kind` is passed at the call site and never inferred from a nearby label:
    the one place this file draws a woman (Phoebe, 16:1) says so here.
    """
    make = {"woman": F.woman, "child": F.child}.get(kind, F.man)
    parts = make(pose="walk" if legs == "walk" else "stand", arms=arms)
    F.draw(c, parts, x, gy, h / MAN_UNITS, col, BG,
           style=figure_paint(col, width))


def units(h):
    """Pixels per local unit for a scene whose men stand `h` tall."""
    return h / MAN_UNITS


def prop(c, parts, x, gy, s, col, width=2, flip=1, centre=False):
    """A made thing from the vocabulary, its origin at (x, gy), at scale `s`.

    Scale rather than height, so a scene can pass the same `s` its people are
    drawn at and have the table come out waist high on the man behind it
    without anyone having to know how tall a table is. `centre` puts the
    thing's middle on `gy` instead of its base, for the few marks — a shackle
    hanging in the air — that never stood on anything.
    """
    if centre:
        y0, y1 = F.bbox((parts, 0))[2:]
        gy = gy + (y1 - y0) * s / 2
    F.draw(c, parts, x, gy, s, col, BG, flip=flip,
           style=figure_paint(col, width))


def fit(parts, w=None, h=None):
    """The scale that draws `parts` at a given pixel width or height."""
    x0, x1, y0, y1 = F.bbox((parts, 0))
    return w / (x1 - x0) if w is not None else h / (y1 - y0)


def mouth(x, gy, h):
    """A figure's mouth: (x, y, half-width), low on the face and sized to the
    head, so the mark reads as a mouth at every height the letter draws one
    rather than as a bar across the eyes."""
    r = h * _HEAD_R / MAN_UNITS
    return x, gy - h * _HEAD_Y / MAN_UNITS + r * 0.45, r * 0.42


# ---------------------------------------------------------------------------
# The Romans Road — shared scene machinery
# ---------------------------------------------------------------------------
#
# A winding road in gentle 3/4 view, bottom-left foreground to a distant
# arch upper-right. Milestones plant at the classic verses and stay for
# every later road frame, so the road accumulates as the letter walks it.

R_NEAR_Y, R_FAR_Y = 500, 224            # road vertical span
R_SCALE_FAR = 0.42                      # perspective scale at the arch


def road_pt(t):
    """Centreline of the road at t in [0,1] (0 = foreground)."""
    x = 356 + 442 * t - 108 * math.sin(math.pi * t)
    y = R_NEAR_Y - (R_NEAR_Y - R_FAR_Y) * (t ** 0.9)
    return x, y


def road_scale(t):
    return 1 - (1 - R_SCALE_FAR) * (t ** 0.9)


def road_halfw(t):
    return (118 * road_scale(t) ** 1.6) + 10


ARCH_T = 1.0
ARCH_X, ARCH_Y = road_pt(ARCH_T)

# (key, t, side, engraved lines, reference, plants at)
MILES = [
    ("M1", 0.13, -1, ["ALL HAVE", "SINNED"], "3:23", (3, 23)),
    ("M2", 0.38, +1, ["CHRIST DIED", "FOR US"], "5:8", (5, 8)),
    ("M3", 0.60, -1, ["WAGES OF SIN: DEATH", "GIFT OF GOD: LIFE"], "6:23",
     (6, 23)),
    ("M4", 0.78, -1, ["CONFESS", "BELIEVE"], "10:9", (10, 9)),
]


def _verges(t0, t1, n):
    """The two kerb lines of the road over t in [t0, t1]."""
    left, right = [], []
    for i in range(n + 1):
        t = t0 + (t1 - t0) * i / n
        x, y = road_pt(t)
        hw = road_halfw(t)
        left.append((x - hw, y))
        right.append((x + hw, y))
    return left, right


def draw_road(c, pos, seg=1.0, grow_from=None):
    """The road bed, verges and flagstone joints, up to t=seg (so chapter 1
    can draw the road *arriving*). Milestones and arch are separate.

    `grow_from` is the reach of the road on the *previous* verse: everything
    already laid is drawn static and only the newly reached stretch animates,
    so the kerbs are not re-traced from the start on every verse. Pass None
    for a road that is simply there.
    """
    left, right = _verges(0.0, seg, 26)
    c.polygon(left + right[::-1], fill=dim(PANEL, 0.9))
    if grow_from is not None and grow_from < seg - 1e-6:
        l_old, r_old = _verges(0.0, grow_from, 20)
        l_new, r_new = _verges(grow_from, seg, 8)
        if grow_from > 1e-6:
            c.polyline(l_old, dim(SAND, 0.85), 2.2)
            c.polyline(r_old, dim(SAND, 0.85), 2.2)
        c.traced(l_new, dim(SAND, 0.85), 2.2, dur="1.1s")
        c.traced(r_new, dim(SAND, 0.85), 2.2, dur="1.1s")
    else:
        c.polyline(left, dim(SAND, 0.85), 2.2)
        c.polyline(right, dim(SAND, 0.85), 2.2)
    # flagstone joints
    for i in range(1, 14):
        t = seg * i / 14
        x, y = road_pt(t)
        hw = road_halfw(t) * 0.92
        c.line((x - hw, y), (x + hw, y), dim(SAND_DIM, 0.7),
               max(0.8, 1.6 * road_scale(t)))
    # centre spine of larger pavers
    for i in range(0, 20):
        t = seg * (i + 0.5) / 20
        x, y = road_pt(t)
        s = road_scale(t)
        c.line((x - 9 * s, y), (x + 9 * s, y), dim(SAND_DIM, 0.5),
               max(0.8, 3.5 * s))
    # the way still ahead, sketched as a dashed centreline
    if seg < 0.999:
        ahead = [road_pt(seg + (1 - seg) * i / 10) for i in range(11)]
        c.polyline(ahead, dim(SAND_DIM, 0.8), 1.6, dash="3,8")


def draw_arch(c, pos, lit=False, lit_first=False, label="ROME"):
    """The gate at the road's end."""
    s = R_SCALE_FAR
    aw, ah = 132 * s, 150 * s
    x, y = ARCH_X, ARCH_Y + 4
    col = HL if lit else dim(SAND, 0.9)
    wdt = 2.6 if lit else 2
    # pillars
    c.line((x - aw / 2, y), (x - aw / 2, y - ah * 0.62), col, wdt)
    c.line((x + aw / 2, y), (x + aw / 2, y - ah * 0.62), col, wdt)
    # arch curve
    c.path(f"M{x - aw / 2:.1f},{y - ah * 0.62:.1f} "
           f"A{aw / 2:.1f},{ah * 0.38:.1f} 0 0 1 "
           f"{x + aw / 2:.1f},{y - ah * 0.62:.1f}",
           stroke=col, width=wdt)
    # capstones
    c.line((x - aw / 2 - 4, y - ah * 0.62), (x - aw / 2 + 6, y - ah * 0.62),
           col, wdt)
    c.line((x + aw / 2 - 6, y - ah * 0.62), (x + aw / 2 + 4, y - ah * 0.62),
           col, wdt)
    c.text((x, y - ah - 12), label, 14, HL if lit else TEXT_DIM, "mm",
           bold=lit)
    if lit:
        for k in range(7):
            a = math.pi * (0.12 + 0.76 * k / 6)
            c.line((x + (aw * 0.75) * math.cos(a),
                    y - ah * 0.62 - (ah * 0.55) * math.sin(a)),
                   (x + (aw * 1.15) * math.cos(a),
                    y - ah * 0.62 - (ah * 0.95) * math.sin(a)),
                   dim(GOLD, 0.6), 1.6)
        if lit_first:
            c.pulse_ellipse(x, y - ah * 0.5, aw * 0.85, ah * 0.7,
                            dim(HL, 0.8), width=2, first=True)


def draw_milestone(c, key, pos, focus_key=None, focus_first=False):
    """One milestone, if planted by `pos`. Returns True if drawn."""
    for k, t, side, lines, ref, at in MILES:
        if k != key:
            continue
        on, first = since(pos, *at)
        if not on:
            return False
        x, y = road_pt(t)
        s = road_scale(t)
        hw = road_halfw(t)

        # The face is cut to fit its engraving, never the other way round.
        fs = max(9.5, 13.5 * s + 3)
        n = len(lines)
        pad = fs * 1.5
        sw = max(max(text_w(ln, fs, bold=True) for ln in lines) + pad,
                 96 * s + 40)
        sh = n * (fs + 5) + fs * 2.6

        sx = x + side * (hw + sw * 0.52 + 18 * s)
        sx = min(max(sx, sw / 2 + 14), W - sw / 2 - 14)
        sy = y - sh                        # stone sits on the verge
        lit = (k == focus_key) or first
        face = dim(STONE_LIT, 0.95 if lit else 0.6)
        c.rect(sx - sw / 2, sy, sw, sh, fill=dim(STONE, 0.55),
               stroke=face, width=2 if lit else 1.4, rx=fs * 0.9)
        for i, ln in enumerate(lines):
            ly = sy + fs * 1.15 + i * (fs + 5)
            c.text((sx, ly), ln, fs, HL if lit else dim(TEXT, 0.8), "mm",
                   bold=True)
        c.text((sx, sy + sh - fs * 0.85), ref, fs * 0.82,
               dim(TEXT, 0.75), "mm", italic=True)
        if first or (focus_first and lit):
            c.pulse_rect(sx - sw / 2 - 5, sy - 5, sw + 10, sh + 10,
                         dim(HL, 0.9), width=2.4, first=True,
                         rx=fs * 0.9 + 5)
        return True
    return False


def road_horizon(c):
    """Faint horizon line + far hills, common to every road frame."""
    c.line((24, R_FAR_Y + 10), (W - 24, R_FAR_Y + 10), dim(SAND_DIM, 0.45), 1)
    c.path(f"M{60},{R_FAR_Y + 10} Q{170},{R_FAR_Y - 26} {290},{R_FAR_Y + 10}",
           stroke=dim(SAND_DIM, 0.6), width=1.2)
    c.path(f"M{210},{R_FAR_Y + 10} Q{330},{R_FAR_Y - 14} {430},{R_FAR_Y + 10}",
           stroke=dim(SAND_DIM, 0.5), width=1.2)


# ---------------------------------------------------------------------------
# Chapter 1 — the road to Rome, then the darkening
# ---------------------------------------------------------------------------

def draw_ch1(c, v, pos):
    dark = v >= 18
    if not dark:
        # The road *arrives* over vv1-15: each verse lays the next stretch,
        # and only that stretch draws itself in.
        def reach(n):
            return min(1.0, 0.18 + 0.82 * (n / 15))

        seg = reach(v)
        grow = 0.0 if v == 1 else reach(v - 1)
        road_horizon(c)
        draw_road(c, pos, seg=seg, grow_from=grow if v <= 15 else None)
        draw_arch(c, pos, lit=v >= 15, lit_first=v == 15)
        # Paul at the road head with the letter
        px, py = road_pt(0.02)
        figure(c, px - 60, py + 26, 62, dim(SAND, 0.95), 2.2, legs="walk")
        c.text((px - 60, py + 46), "PAUL", 13, TEXT_DIM, "mm")
        lw, lh = 30, 20
        c.rect(px - 18, py - 30, lw, lh, stroke=GOLD, width=1.8, rx=3)
        c.polyline([(px - 18, py - 30), (px - 18 + lw / 2, py - 30 + lh * 0.55),
                    (px - 18 + lw, py - 30)], GOLD, 1.8)
        if v == 1:
            c.pulse_rect(px - 24, py - 36, lw + 12, lh + 12, dim(HL, 0.9),
                         width=2, first=True, rx=5)
        if v >= 16:
            phrase(c, (W / 2, 118), "THE POWER OF GOD FOR SALVATION",
                   24, HL, first=v == 16)
        if v >= 17:
            phrase(c, (W / 2, 156), "THE RIGHTEOUS SHALL LIVE BY FAITH",
                   19, dim(TEXT, 0.95), first=v == 17)
        return

    # vv18-32 — the wrath revealed: the sky lowers over the same road
    shade = min(1.0, (v - 17) / 8)
    c.rect(0, 0, W, 150 + 60 * shade, fill=dim((30, 16, 18), 0.55 * shade))
    road_horizon(c)
    draw_road(c, pos, seg=1.0)
    draw_arch(c, pos, lit=False)
    for i in range(13):
        x = 80 + i * 72
        ln = 16 if i % 2 else 24
        c.line((x, 66), (x, 66 + ln + 26 * shade), dim(RED, 0.7), 2,
               linecap="round")
    c.text((W - 30, 60), "WRATH", 15, dim(RED, 0.95), "rm", bold=True)

    # the exchange: glory traded for an image (vv21-25)
    ex_on, ex_first = since(pos, 1, 21)
    if ex_on:
        gx, gy = 190, 320
        c.circle(gx, gy, 26, stroke=GOLD, width=2.2)
        for k in range(8):
            a = k * math.pi / 4
            c.line((gx + 32 * math.cos(a), gy + 32 * math.sin(a)),
                   (gx + 44 * math.cos(a), gy + 44 * math.sin(a)), GOLD, 1.8)
        c.text((gx, gy - 56), "GLORY", 13, TEXT_DIM, "mm")
        ix, iy = gx, gy + 118
        c.rect(ix - 16, iy - 14, 32, 34, stroke=dim(GRAY, 0.95), width=2,
               rx=4)
        c.circle(ix, iy - 24, 9, stroke=dim(GRAY, 0.95), width=2)
        c.text((ix, iy + 40), "IMAGES", 13, dim(TEXT_DIM, 0.9), "mm")
        c.polyline([(gx + 52, gy + 20), (gx + 66, gy + 59),
                    (gx + 52, gy + 98)], dim(RED, 0.85), 2)
        c.polyline([(gx + 46, gy + 88), (gx + 52, gy + 100),
                    (gx + 60, gy + 92)], dim(RED, 0.85), 2)
        if ex_first:
            c.pulse_ellipse(ix, iy, 34, 34, dim(RED, 0.8), width=2,
                            first=True)
        if pos >= P(1, 25):
            c.text((gx + 96, gy + 59), "THE LIE", 13, dim(RED, 0.95), "lm",
                   bold=pos == P(1, 25))

    # vv24-32: the marks accumulate in the darkened sky
    n_marks = max(0, v - 23)
    for i in range(n_marks):
        mx = 420 + (i % 5) * 96 + (i * 37 % 23)
        my = 122 + (i // 5) * 34
        c.line((mx - 7, my - 7), (mx + 7, my + 7), dim(RED, 0.8), 2.2)
        c.line((mx - 7, my + 7), (mx + 7, my - 7), dim(RED, 0.8), 2.2)
        if i == n_marks - 1 and v >= 24:
            c.pulse_ellipse(mx, my, 14, 14, dim(RED, 0.85), width=1.8,
                            first=True)


# ---------------------------------------------------------------------------
# Chapter 2 — the impartial judge
# ---------------------------------------------------------------------------

def draw_ch2(c, v, pos):
    # the bema: a stepped platform right of centre, radiant, empty seat
    bx, by = 700, 300                      # seat top centre
    for i, (w2, h2) in enumerate([(240, 26), (200, 26), (160, 26)]):
        c.rect(bx - w2 / 2, by + 78 - (i + 1) * 26, w2, h2,
               stroke=dim(SAND, 0.9), width=1.6, fill=dim(PANEL, 0.8))
    c.rect(bx - 46, by - 58, 92, 58, stroke=dim(GOLD, 0.95), width=2,
           fill=dim(GOLD, 0.05), rx=6)
    c.line((bx - 34, by - 14), (bx + 34, by - 14), dim(GOLD, 0.6), 1.6)
    for k in range(7):
        a = math.pi * (0.15 + 0.7 * k / 6)
        x0 = bx + 62 * math.cos(a)
        y0 = by - 66 - 26 * math.sin(a)
        x1 = bx + 88 * math.cos(a)
        y1 = by - 66 - 44 * math.sin(a)
        c.line((x0, y0), (x1, y1), dim(GOLD, 0.55), 1.6)
    c.text((bx, by + 102), "THE JUDGMENT SEAT", 14, TEXT_DIM, "mm")

    gy = by + 78
    c.line((80, gy), (W - 80, gy), dim(SAND_DIM, 0.8), 1.5)

    # vv1-5: the accuser — his pointing arm curves back at himself
    ax = 240
    lit_acc = v <= 5
    figure(c, ax, gy, 96, dim(SAND, 0.95) if lit_acc else dim(SAND_DIM, 1.0),
           2.2, arms="point_r")
    c.text((ax, gy + 22), "THE JUDGE OF OTHERS", 13,
           HL if lit_acc else TEXT_DIM, "mm", bold=lit_acc)
    turn_on, turn_first = since(pos, 2, 1)
    if turn_on and v <= 11:
        # the accusation loops out toward the seat and comes back around
        x0, y0 = ax + 33, gy - 62
        lcx, lcy = x0 + 118, y0 - 52
        pts = []
        for k in range(23):
            a = math.pi * (1.12 - 1.95 * k / 22)
            pts.append((lcx + 126 * math.cos(a), lcy - 66 * math.sin(a)))
        if turn_first:
            c.traced(pts, dim(RED, 0.85), 2.2, dur="2.2s")
        else:
            c.polyline(pts, dim(RED, 0.85), 2.2)
        ex2, ey2 = pts[-1]
        c.polyline([(ex2 + 12, ey2 - 10), (ex2, ey2), (ex2 + 14, ey2 + 4)],
                   dim(RED, 0.85), 2.2)
        c.text((lcx, lcy - 84), "YOU WHO JUDGE", 13, dim(RED, 0.95),
               "mm", bold=lit_acc)

    if pos >= P(2, 4):
        c.text((bx, by - 130), "GOODNESS LEADS TO REPENTANCE", 14,
               HL if v in (4, 5) else dim(TEXT, 0.75), "mm", bold=v in (4, 5))
    if pos >= P(2, 6):
        phrase(c, (W / 2, 96), "TO EACH ACCORDING TO HIS WORKS", 21,
               HL if 6 <= v <= 11 else dim(TEXT, 0.8), first=v == 6)

    # vv7-11: glory to one side, wrath to the other, a verdict laid down per
    # verse — and at v11 a level rule between them: no partiality
    g_i = w_i = 0
    for at_v, side2 in ((7, +1), (8, -1), (9, -1), (10, +1)):
        on2, m_first = since(pos, 2, at_v)
        if not on2:
            continue
        if side2 > 0:
            mx3, my3 = bx + 150, by - 30 + g_i * 30
            g_i += 1
        else:
            mx3, my3 = bx - 150, by - 30 + w_i * 30
            w_i += 1
        c.circle(mx3, my3, 6,
                 fill=dim(GOLD, 0.9) if side2 > 0 else dim(RED, 0.85))
        if m_first:
            c.pulse_ellipse(mx3, my3, 14, 14, dim(HL, 0.85), width=1.8,
                            first=True)
    if g_i:
        c.text((bx + 150, by - 62), "GLORY", 12.5, dim(TEXT, 0.9), "mm")
    if w_i:
        c.text((bx - 150, by - 62), "WRATH", 12.5, dim(RED, 0.9), "mm")
    lev_on, lev_first = since(pos, 2, 11)
    if lev_on:
        c.line((bx - 150, by - 96), (bx + 150, by - 96),
               dim(SAND, 0.9), 1.6, dash="6,6")
        c.polygon([(bx, by - 104), (bx + 9, by - 96), (bx, by - 88),
                   (bx - 9, by - 96)], fill=dim(SAND, 0.95))
        if lev_first:
            c.pulse_ellipse(bx, by - 96, 26, 18, dim(HL, 0.85), width=2,
                            first=True)

    # vv12-16: law tablet and conscience heart on equal ground
    pair_on, pair_first = since(pos, 2, 12)
    if pair_on:
        for x, glyph, label, at in ((430, "tablet", "THE LAW", (2, 12)),
                                    (540, "heart", "CONSCIENCE", (2, 14))):
            g_on, g_first = since(pos, *at)
            if not g_on:
                continue
            lit = 12 <= v <= 16
            col = dim(SAND, 0.95) if lit else dim(SAND_DIM, 1.0)
            if glyph == "tablet":
                c.rect(x - 22, gy - 76, 44, 58, stroke=col, width=2, rx=10)
                for r in range(3):
                    c.line((x - 12, gy - 60 + r * 14),
                           (x + 12, gy - 60 + r * 14), col, 1.4)
            else:
                c.path(f"M{x},{gy - 22} C{x - 30},{gy - 48} {x - 22},{gy - 76}"
                       f" {x},{gy - 60} C{x + 22},{gy - 76} {x + 30},{gy - 48}"
                       f" {x},{gy - 22}", stroke=col, width=2)
            c.text((x, gy + 22), label, 12.5, HL if lit else TEXT_DIM, "mm",
                   bold=lit)
            if g_first:
                c.pulse_ellipse(x, gy - 48, 40, 46, dim(HL, 0.85), width=2,
                                first=True)

    # vv17-24: the boast cracks
    boast_on, _ = since(pos, 2, 17)
    if boast_on and v <= 24:
        c.text((430, gy - 130), "BOAST IN GOD", 13.5,
               HL if v == 17 else dim(TEXT, 0.8), "mm", bold=v == 17)
        if pos >= P(2, 18):          # instructed out of the law
            c.circle(430, gy - 47, 40, stroke=dim(GOLD, 0.55), width=1.5)
        # the boast names itself, a claim at a time (vv19-20)
        for word, wx4, at in (("A GUIDE", 330, (2, 19)),
                              ("A LIGHT", 408, (2, 19)),
                              ("A TEACHER", 492, (2, 20))):
            if pos >= P(*at):
                c.text((wx4, gy - 108), word, 12.5,
                       HL if v == at[1] else dim(TEXT, 0.8), "mm",
                       italic=True)
        # the crack runs a little further with each charge (vv21-24)
        crack_on, crack_first = since(pos, 2, 21)
        if crack_on:
            crack = [(430, gy - 76), (424, gy - 58), (434, gy - 44),
                     (426, gy - 26), (436, gy - 8)]
            c.polyline(crack[:2 + min(3, v - 21)], dim(RED, 0.9), 2)
            if crack_first:
                c.pulse_ellipse(430, gy - 50, 34, 40, dim(RED, 0.85),
                                width=2, first=True)

    # vv25-29: the circle moves inward, to the heart
    inw_on, inw_first = since(pos, 2, 25)
    if inw_on:
        hx = 540
        ring_col = HL if v >= 28 else dim(GOLD, 0.8)
        c.circle(hx, gy - 48, 34, stroke=ring_col, width=2.2)
        if inw_first or v == 29:
            c.pulse_ellipse(hx, gy - 48, 40, 40, dim(HL, 0.9), width=2,
                            first=True)
        if v >= 29:
            c.text((hx - 60, gy - 152), "OF THE HEART, IN THE SPIRIT", 14,
                   HL, "mm", bold=True)


# ---------------------------------------------------------------------------
# Chapter 3 — every mouth stopped, then BUT NOW
# ---------------------------------------------------------------------------

def draw_ch3(c, v, pos):
    if v == 23:
        # Road frame I — the first milestone plants
        road_horizon(c)
        draw_road(c, pos)
        draw_arch(c, pos)
        draw_milestone(c, "M1", pos, focus_key="M1")
        phrase(c, (W / 2, 110),
               "ALL HAVE SINNED, AND FALL SHORT", 24, HL, first=True)
        c.text((W / 2, 146), "OF THE GLORY OF GOD", 17, dim(TEXT, 0.9),
               "mm")
        return

    gy = 396
    if v <= 20:
        # vv1-8: the oracles entrusted; vv9-20 the dock falls silent
        c.line((90, gy), (W - 90, gy), dim(SAND_DIM, 0.8), 1.5)
        scroll_on, scroll_first = since(pos, 3, 2)
        if scroll_on and v <= 8:
            sx, sy = 250, 180
            c.rect(sx - 60, sy - 34, 120, 68, stroke=GOLD, width=2, rx=8,
                   fill=dim(GOLD, 0.08))
            # a further line of the oracles stands written each verse
            for r in range(max(1, min(6, v - 1))):
                c.line((sx - 40, sy - 22 + r * 11), (sx + 40, sy - 22 + r * 11),
                       dim(GOLD, 0.7 if r < v - 2 else 0.95), 1.6)
            c.text((sx, sy + 54), "THE ORACLES OF GOD", 14,
                   HL if v == 2 else TEXT_DIM, "mm", bold=v == 2)
            if scroll_first:
                c.pulse_rect(sx - 66, sy - 40, 132, 80, dim(HL, 0.85),
                             width=2, first=True, rx=10)
        # the assembled world: a shallow arc of figures
        n_fig = 13
        for i in range(n_fig):
            t = i / (n_fig - 1)
            fx = 150 + t * (W - 300)
            fy = gy - 20 * math.sin(math.pi * t)
            h = 52 + 16 * math.sin(math.pi * t)
            quiet_on, _ = since(pos, 3, 9)
            col = dim(SAND_DIM, 1.0) if quiet_on else dim(SAND, 0.8)
            figure(c, fx, fy, h, col, 1.8)
            # the mouth: a small line that closes at v19
            mstop, mstop_first = since(pos, 3, 19)
            mx, my, mw = mouth(fx, fy, h)
            if not mstop:
                c.line((mx - mw, my), (mx + mw, my), dim(RED, 0.8), 1.5)
        c.text((W / 2, gy + 34), "JEW AND GREEK ALIKE", 14,
               HL if v == 9 else TEXT_DIM, "mm", bold=v == 9)
        # vv10-18 — the catena: the charge sheet lowers line by line
        if pos >= P(3, 10):
            k = min(v, 18) - 9
            for i in range(k):
                yq = 126 + i * 21
                ln = [
                    "NO ONE RIGHTEOUS", "NO ONE UNDERSTANDS",
                    "ALL TURNED ASIDE", "THROATS: AN OPEN TOMB",
                    "MOUTHS FULL OF CURSING", "FEET SWIFT TO SHED BLOOD",
                    "DESTRUCTION AND MISERY", "NO PEACE · NO FEAR OF GOD",
                ][i] if i < 8 else ""
                lit = (i == k - 1 and v <= 18)
                c.text((W / 2, yq), ln, 15 if lit else 13.5,
                       dim(RED, 0.95) if lit else dim(RED, 0.55), "mm",
                       bold=lit)
        stop_on, stop_first = since(pos, 3, 19)
        if stop_on:
            phrase(c, (W / 2, 88), "EVERY MOUTH STOPPED", 24,
                   dim(RED, 1.0), first=stop_first)
        return

    # vv21-31 (except 23): BUT NOW — light breaks over the mercy seat
    but_on, but_first = since(pos, 3, 21)
    shaft_w = 150
    c.polygon([(W / 2 - shaft_w / 2, 0), (W / 2 + shaft_w / 2, 0),
               (W / 2 + shaft_w * 0.9, 340), (W / 2 - shaft_w * 0.9, 340)],
              fill=dim(GOLD, 0.10))
    phrase(c, (W / 2, 92), "BUT NOW", 30, HL, first=but_first)
    c.text((W / 2, 128), "RIGHTEOUSNESS APART FROM THE LAW", 15,
           dim(TEXT, 0.9), "mm")
    # the mercy seat / atoning sacrifice
    ax, ay = W / 2, 330
    seat_on, seat_first = since(pos, 3, 24)
    if seat_on:
        c.rect(ax - 90, ay - 40, 180, 52, stroke=GOLD, width=2.2,
               fill=dim(GOLD, 0.10), rx=6)
        c.polyline([(ax - 70, ay - 40), (ax - 52, ay - 58)], GOLD, 2)
        c.polyline([(ax + 70, ay - 40), (ax + 52, ay - 58)], GOLD, 2)
        c.circle(ax, ay - 14, 5, fill=dim(RED, 0.9))
        c.text((ax, ay + 36), "AN ATONING SACRIFICE", 15,
               HL if 24 <= v <= 26 else dim(TEXT, 0.85), "mm",
               bold=24 <= v <= 26)
        c.text((ax, ay + 58), "BY HIS BLOOD, THROUGH FAITH", 13,
               dim(TEXT_DIM, 0.95), "mm", italic=True)
        if seat_first:
            c.pulse_rect(ax - 96, ay - 64, 192, 82, dim(HL, 0.9), width=2.4,
                         first=True, rx=8)
    just_on, just_first = since(pos, 3, 26)
    if just_on:
        c.text((ax, ay - 84), "JUST, AND THE JUSTIFIER", 15, HL, "mm",
               bold=True)
        if just_first:
            c.pulse_rect(ax - 118, ay - 100, 236, 30, dim(HL, 0.85),
                         width=2, first=True, rx=15)
    # vv27-31: boasting excluded — a small shut door stage left
    bo_on, bo_first = since(pos, 3, 27)
    if bo_on:
        bx2, by2 = 190, 300
        c.rect(bx2 - 46, by2 - 20, 92, 30, stroke=dim(SAND_DIM, 1.0),
               width=1.6, rx=4)
        c.text((bx2, by2 - 5), "BOASTING", 13, dim(TEXT_DIM, 0.95), "mm")
        c.line((bx2 - 46, by2 + 10), (bx2 + 46, by2 - 20), dim(RED, 0.9), 2.2)
        c.text((bx2, by2 + 34), "EXCLUDED", 12.5, dim(RED, 0.9), "mm",
               bold=bo_first)
        if bo_first:
            c.pulse_rect(bx2 - 52, by2 - 26, 104, 44, dim(RED, 0.8),
                         width=2, first=True, rx=6)
    faith_on, faith_first = since(pos, 3, 28)
    if faith_on:
        c.text((W - 190, 300), "BY FAITH,", 15, HL, "mm", bold=True)
        c.text((W - 190, 322), "APART FROM WORKS", 13, dim(TEXT, 0.9), "mm")
        if faith_first:
            c.pulse_rect(W - 268, 284, 156, 52, dim(HL, 0.85), width=2,
                         first=True, rx=8)
    one_on, _ = since(pos, 3, 29)
    if one_on:
        c.text((W / 2, 436), "ONE GOD — JEW AND GENTILE, THE SAME WAY",
               14, HL if v >= 29 else TEXT_DIM, "mm", bold=v >= 29)


# ---------------------------------------------------------------------------
# Chapter 4 — Abraham's stars
# ---------------------------------------------------------------------------

# a fixed constellation, kindled a few stars per verse
_STARS = []
_sx = 137
for _i in range(90):
    _sx = (_sx * 73 + 41) % 883
    _sy = (_sx * 57 + 29) % 331
    _STARS.append((120 + (_sx / 883) * (W - 220),
                   70 + (_sy / 331) * 260))

STARS_PER_V = [4, 3, 5, 3, 3, 3, 3, 3, 3, 3, 4, 3, 4, 3, 3, 3, 4, 5, 3, 3,
               3, 4, 4, 4, 5]
assert len(STARS_PER_V) == 25 and sum(STARS_PER_V) <= len(_STARS)


def draw_ch4(c, v, pos):
    gy = 470
    c.line((60, gy), (W - 60, gy), dim(SAND_DIM, 0.8), 1.5)
    # Abraham, looking up
    axf = 190
    figure(c, axf, gy, 92, dim(SAND, 0.95), 2.2, arms="up")
    c.text((axf, gy + 22), "ABRAHAM", 14, TEXT, "mm", bold=v == 1)
    # David joins at v6 (the second witness)
    dav_on, dav_first = since(pos, 4, 6)
    if dav_on:
        figure(c, axf + 92, gy, 74, dim(SAND, 0.85), 2)
        c.text((axf + 92, gy + 22), "DAVID", 13,
               HL if 6 <= v <= 8 else TEXT_DIM, "mm", bold=6 <= v <= 8)
        if dav_first:
            c.pulse_ellipse(axf + 92, gy - 38, 30, 46, dim(HL, 0.85),
                            width=2, first=True)
    # the slate wiped clean (vv7-8, Psalm 32)
    slate_on, slate_first = since(pos, 4, 7)
    if slate_on and v <= 9:
        sx2, sy2 = axf + 220, gy - 64
        c.rect(sx2 - 44, sy2 - 26, 88, 52, stroke=dim(SAND, 0.9), width=1.8,
               rx=5)
        for r in range(3):
            c.line((sx2 - 30, sy2 - 12 + r * 12), (sx2 + 30, sy2 - 12 + r * 12),
                   dim(SAND_DIM, 0.9), 1.4)
        c.line((sx2 - 36, sy2 + 20), (sx2 + 36, sy2 - 20), dim(GOLD, 0.95),
               2.6)
        c.text((sx2, sy2 + 44), "FORGIVEN · COVERED", 13,
               HL if v <= 8 else TEXT_DIM, "mm", bold=v <= 8)
        if slate_first:
            c.pulse_rect(sx2 - 50, sy2 - 32, 100, 64, dim(HL, 0.85),
                         width=2, first=True, rx=7)
    # the stars kindle
    lit_n = sum(STARS_PER_V[:v])
    new_n = STARS_PER_V[v - 1]
    for i, (x, y) in enumerate(_STARS[:lit_n]):
        fresh = i >= lit_n - new_n
        r = 2.6 if not fresh else 3.4
        c.circle(x, y, r, fill=dim(HL if fresh else GOLD,
                                   0.95 if fresh else 0.7))
        if fresh:
            c.pulse_ellipse(x, y, 8, 8, dim(HL, 0.8), width=1.2, first=True)
    # phrases at the hinges
    if pos >= P(4, 3):
        phrase(c, (W / 2, 42),
               "BELIEVED — ACCOUNTED FOR RIGHTEOUSNESS", 20, HL,
               first=v == 3)
    seal_on, seal_first = since(pos, 4, 11)
    if seal_on:
        # the seal: a dashed ring around an early cluster
        cx4, cy4 = 620, 170
        c.circle(cx4, cy4, 64, stroke=dim(GOLD, 0.8), width=1.8)
        c.text((cx4, cy4 + 84), "A SEAL OF FAITH'S RIGHTEOUSNESS", 13,
               HL if v == 11 else TEXT_DIM, "mm", bold=v == 11)
        if seal_first:
            c.pulse_ellipse(cx4, cy4, 70, 70, dim(HL, 0.85), width=2,
                            first=True)
    fa_on, fa_first = since(pos, 4, 17)
    if fa_on:
        phrase(c, (W / 2, gy - 116), "A FATHER OF MANY NATIONS", 19,
               HL if v in (17, 18) else dim(TEXT, 0.85), first=fa_first)
    if pos >= P(4, 18):
        c.text((W / 2, gy - 88), "SO SHALL YOUR OFFSPRING BE", 15,
               dim(TEXT, 0.9), "mm", italic=True)
    us_on, us_first = since(pos, 4, 23)
    if us_on:
        ux, uy = W - 170, 120
        c.circle(ux, uy, 6, fill=HL)
        for k in range(8):
            a = k * math.pi / 4
            c.line((ux + 10 * math.cos(a), uy + 10 * math.sin(a)),
                   (ux + 18 * math.cos(a), uy + 18 * math.sin(a)),
                   dim(HL, 0.8), 1.4)
        c.text((ux, uy + 34), "FOR US ALSO", 14, HL, "mm", bold=True)
        if us_first:
            c.pulse_ellipse(ux, uy, 24, 24, dim(HL, 0.9), width=2,
                            first=True)


# ---------------------------------------------------------------------------
# Chapter 5 — peace, the road again, and the two doors
# ---------------------------------------------------------------------------

def draw_ch5(c, v, pos):
    if v <= 5:
        # the stair: peace -> access -> hope -> love, a figure climbing
        steps = [("PEACE", (5, 1)), ("ACCESS", (5, 2)),
                 ("HOPE", (5, 4)), ("LOVE", (5, 5))]
        x0, y0 = 300, 430
        sw2, sh2 = 128, 62
        top = 0
        for i, (word, at) in enumerate(steps):
            on, s_first = since(pos, *at)
            if not on:
                continue
            top = i
            sx = x0 + i * sw2
            sy = y0 - i * sh2
            c.rect(sx, sy - sh2, sw2, sh2 + i * sh2, stroke=dim(SAND, 0.9),
                   width=1.8, fill=dim(PANEL, 0.85))
            c.text((sx + sw2 / 2, sy - sh2 / 2), word, 16,
                   HL if on and v == at[1] else dim(TEXT, 0.85), "mm",
                   bold=v == at[1])
            if s_first:
                c.pulse_rect(sx, sy - sh2, sw2, sh2, dim(HL, 0.85),
                             width=2.2, first=True)
        # On the tread, not inside the riser. The stick figure stood within
        # the step's own box and the word showed through it; a drawn body is
        # a mass and blots the word out, so the climber goes where a climber
        # would be — on top of the step he has reached.
        fx = x0 + top * sw2 + sw2 / 2
        figure(c, fx, y0 - top * sh2 - sh2, 58, dim(GOLD, 0.95),
               2, arms="open" if top >= 2 else "down")
        # glory shining on the top stair
        c.circle(x0 + 4 * sw2 + 60, y0 - 4 * sh2 - 10, 30,
                 stroke=dim(GOLD, 0.55), width=1.6)
        c.text((x0 + 4 * sw2 + 60, y0 - 4 * sh2 + 34), "GLORY", 12.5,
               TEXT_DIM, "mm")
        if v == 3:
            c.text((x0 + sw2 * 1.5, y0 + 40),
                   "SUFFERING WORKS PERSEVERANCE", 14, dim(TEXT, 0.9), "mm")
        phrase(c, (W / 2, 90), "PEACE WITH GOD THROUGH FAITH", 22, HL,
               first=v == 1)
        return

    if v <= 11:
        # Road frame II — the cross on the hill, the second milestone
        road_horizon(c)
        # the hill and cross beyond the road, off to the left
        hx, hy = 300, R_FAR_Y + 8
        c.path(f"M{hx - 110},{hy} Q{hx},{hy - 60} {hx + 110},{hy}",
               stroke=dim(SAND_DIM, 0.8), width=1.4)
        cr_on, cr_first = since(pos, 5, 6)
        if cr_on:
            # standing on the crown of the hill, which a quadratic puts at
            # half its rise
            cx5, cy5 = hx, hy - 28
            crs = F.cross()
            prop(c, crs, cx5, cy5, fit(crs, h=62), GOLD, 2.6)
            if cr_first:
                c.pulse_ellipse(cx5, cy5 - 32, 28, 42, dim(HL, 0.9),
                                width=2, first=True)
        draw_road(c, pos)
        draw_arch(c, pos)
        draw_milestone(c, "M1", pos)
        draw_milestone(c, "M2", pos, focus_key="M2")
        if v >= 8:
            phrase(c, (W / 2, 100), "WHILE WE WERE YET SINNERS,", 22, HL,
                   first=v == 8)
            c.text((W / 2, 136), "CHRIST DIED FOR US", 19, HL, "mm",
                   bold=True)
        elif v >= 6:
            phrase(c, (W / 2, 100), "FOR THE UNGODLY", 21,
                   dim(TEXT, 0.95), first=v == 6)
        rec_on, rec_first = since(pos, 5, 10)
        if rec_on:
            c.text((W / 2, 176), "RECONCILED", 15, dim(TEXT, 0.9), "mm",
                   bold=rec_first)
        return

    # vv12-21 — the two gates
    gy = 440
    c.line((100, gy), (W - 100, gy), dim(SAND_DIM, 0.8), 1.5)
    adx, chx = 330, 700

    def gate(x, w2, h2, col, wdt):
        c.line((x - w2 / 2, gy), (x - w2 / 2, gy - h2), col, wdt)
        c.line((x + w2 / 2, gy), (x + w2 / 2, gy - h2), col, wdt)
        c.path(f"M{x - w2 / 2:.1f},{gy - h2:.1f} "
               f"A{w2 / 2:.1f},{h2 * 0.52:.1f} 0 0 1 "
               f"{x + w2 / 2:.1f},{gy - h2:.1f}", stroke=col, width=wdt)

    # Adam's gate: narrow, gray; a procession passes down through it
    gate(adx, 128, 148, dim(GRAY, 0.95), 2.2)
    c.text((adx, gy - 244), "ADAM", 17, dim(TEXT, 0.9), "mm",
           bold=v in (12, 14))
    c.text((adx, gy - 224), "one man", 11.5, dim(TEXT_DIM, 0.9), "mm",
           italic=True)
    c.text((adx, gy + 24), "SIN ENTERED — DEATH REIGNED", 13,
           dim(RED, 0.9) if 12 <= v <= 14 else TEXT_DIM, "mm",
           bold=12 <= v <= 14)
    n_gray = min(8, 2 + (v - 12))
    for i in range(n_gray):
        t = i / 7
        px = adx + 34 - 150 * t + (17 * i % 13) - 6
        py = gy - 96 + 74 * t
        if py > gy - 8:
            py = gy - 8
        # 44, not the 26 the sticks stood at: below about forty a drawn body
        # has no room for a head and a shoulder and goes back to being a
        # smudge. The feet stay where they were, so the queue's slope is the
        # slope it always had.
        figure(c, px, min(gy, py + 26), 44, dim(GRAY, 0.7), 1.4)
    # Christ's gate: wide, gold, light pours through
    grace_wide, gw_first = since(pos, 5, 20)
    cw = 196 if grace_wide else 160
    gate(chx, cw, 176, GOLD, 2.8)
    c.text((chx, gy - 312), "CHRIST", 17, HL, "mm", bold=v >= 15)
    c.text((chx, gy - 292), "one man", 11.5, dim(TEXT_DIM, 0.9), "mm",
           italic=True)
    c.text((chx, gy + 24), "GRACE REIGNS THROUGH RIGHTEOUSNESS", 13,
           HL if v >= 17 else TEXT_DIM, "mm", bold=v >= 17)
    n_gold = min(8, 2 + (v - 15)) if v >= 15 else 0
    for i in range(n_gold):
        t = i / 7
        px = chx - 30 + 150 * t + (13 * i % 11) - 5
        py = gy - 60 - 60 * t
        c.circle(px, py, 3.2, fill=dim(GOLD, 0.85))
    mm_on, mm_first = since(pos, 5, 15)
    if mm_on:
        phrase(c, (chx, 92), "MUCH MORE", 24, HL, first=mm_first)
    ab_on, ab_first = since(pos, 5, 20)
    if ab_on:
        c.text((W / 2, gy + 58), "WHERE SIN ABOUNDED, GRACE ABOUNDED MORE",
               15, HL, "mm", bold=ab_first)


# ---------------------------------------------------------------------------
# Chapter 6 — buried with him, raised with him
# ---------------------------------------------------------------------------

def draw_ch6(c, v, pos):
    if v == 23:
        # Road frame III
        road_horizon(c)
        draw_road(c, pos)
        draw_arch(c, pos)
        draw_milestone(c, "M1", pos)
        draw_milestone(c, "M2", pos)
        draw_milestone(c, "M3", pos, focus_key="M3")
        phrase(c, (W / 2, 96), "THE WAGES OF SIN IS DEATH", 23,
               dim(RED, 1.0), first=True)
        phrase(c, (W / 2, 140), "THE FREE GIFT OF GOD IS ETERNAL LIFE",
               23, HL, first=True)
        return

    gy = 340                              # ground on both banks
    pool_x0, pool_x1 = 380, 660
    # the grave-pool between two banks
    c.line((80, gy), (pool_x0, gy), dim(SAND, 0.9), 2)
    c.line((pool_x1, gy), (W - 80, gy), dim(SAND, 0.9), 2)
    c.polygon([(pool_x0, gy), (pool_x1, gy), (pool_x1 - 34, gy + 120),
               (pool_x0 + 34, gy + 120)], fill=dim(WATER, 0.22))
    for wy, wa in ((gy + 26, 0.6), (gy + 58, 0.45), (gy + 90, 0.3)):
        c.path(f"M{pool_x0 + 30},{wy} Q{(pool_x0 + pool_x1) / 2},{wy - 10} "
               f"{pool_x1 - 30},{wy}", stroke=dim(WATER, wa), width=1.8)
    c.text(((pool_x0 + pool_x1) / 2, gy + 164), "BURIED WITH HIM", 14,
           HL if 3 <= v <= 4 else TEXT_DIM, "mm", bold=3 <= v <= 4)

    # the figure's passage: left bank -> under -> right bank
    down_on, down_first = since(pos, 6, 3)
    up_on, up_first = since(pos, 6, 4)
    if not down_on:
        figure(c, 250, gy, 84, dim(SAND, 0.95), 2.2)
        c.text((250, gy + 24), "THE OLD LIFE", 13, TEXT_DIM, "mm")
    else:
        # what is left on the near bank: the grave the old life was left in.
        # A rock-hewn tomb rather than the rounded box that stood here — the
        # chapter's own word is buried, and a tomb with a stone at its door
        # says that where a headstone only says died.
        tomb = F.tomb()
        prop(c, tomb, 196, gy, fit(tomb, h=92), dim(SAND_DIM, 1.0), 1.6)
        c.text((196, gy + 20), "DEAD TO SIN", 11.5, dim(TEXT_DIM, 0.95), "mm")
        # the old man, sunk — and dissolving further with every verse that
        # reckons him dead (vv6-14)
        om = dim(GRAY, max(0.10, 0.55 - 0.05 * max(0, v - 5)))
        cx6 = (pool_x0 + pool_x1) / 2
        cro_on, cro_first = since(pos, 6, 6)
        # His arms go out at v6: the crossbar that used to be ruled across
        # him is the posture itself now, which is one mark instead of two and
        # says crucified without a caption having to.
        figure(c, cx6, gy + 108, 54, om, 1.8,
               arms="open" if cro_on else "down")
        if cro_on:
            c.text((cx6, gy + 124), "OLD MAN CRUCIFIED", 12.5,
                   dim(TEXT_DIM, 0.9), "mm", italic=True)
        # starts clear of the tomb now standing on the near bank
        path_pts = [(300, gy - 20), (348, gy - 4), (pool_x0 + 50, gy + 40),
                    (cx6, gy + 60), (pool_x1 - 50, gy + 36),
                    (730, gy - 10), (790, gy - 34)]
        if up_on:
            if up_first:
                c.traced(path_pts, dim(GOLD, 0.85), 2.4, dur="2.4s")
            else:
                c.polyline(path_pts, dim(GOLD, 0.85), 2.4)
        else:
            half = path_pts[:4]
            if down_first:
                c.traced(half, dim(GOLD, 0.85), 2.4, dur="1.8s")
            else:
                c.polyline(half, dim(GOLD, 0.85), 2.4)
    if up_on:
        arms = "up" if v >= 13 else "open"
        figure(c, 800, gy, 92, GOLD, 2.4, arms=arms)
        c.text((800, gy + 24), "NEWNESS OF LIFE", 13.5,
               HL if v in (4, 5) else TEXT_DIM, "mm", bold=v in (4, 5))
        if up_first:
            c.pulse_ellipse(800, gy - 46, 34, 56, dim(HL, 0.9), width=2,
                            first=True)
    # the broken shackle (vv6-7, 17-18)
    br_on, br_first = since(pos, 6, 7)
    if br_on:
        shx, shy = 800, gy - 156       # clear of the risen figure's head
        sh = F.shackle(broken=True)
        prop(c, sh, shx, shy, fit(sh, w=84), dim(SAND, 0.9), 2.4, centre=True)
        c.text((shx, shy - 42), "FREED FROM SIN", 13.5,
               HL if v in (7, 18) else TEXT_DIM, "mm", bold=v in (7, 18))
        if br_first:
            c.pulse_ellipse(shx, shy, 48, 22, dim(HL, 0.85), width=2,
                            first=True)
    # vv12-13: members presented as instruments — light lines from the hands
    inst_on, inst_first = since(pos, 6, 13)
    if inst_on and v <= 15:
        for a in (-0.5, -0.2, 0.15):
            c.line((800 + 30 * math.cos(a - 1.2), gy - 70),
                   (800 + 74 * math.cos(a - 1.2), gy - 96 - 30 * a),
                   dim(GOLD, 0.6), 1.6)
        c.text((880, gy - 130), "INSTRUMENTS", 12.5,
               HL if v == 13 else TEXT_DIM, "mm", bold=v == 13)
    # vv16-22: two masters
    ma_on, ma_first = since(pos, 6, 16)
    if ma_on:
        my = 120
        c.text((330, my), "SIN", 16, dim(RED, 0.95), "mm",
               bold=v in (16, 20))
        c.text((330, my + 20), "unto death", 12, dim(TEXT_DIM, 0.9), "mm",
               italic=True)
        c.text((700, my), "OBEDIENCE", 16, HL, "mm", bold=16 <= v <= 19)
        c.text((700, my + 20), "unto righteousness", 12,
               dim(TEXT_DIM, 0.9), "mm", italic=True)
        c.polyline([(430, my - 4), (600, my - 4)], dim(SAND_DIM, 0.9), 1.6,
                   dash="5,6")
        c.polyline([(586, my - 10), (600, my - 4), (586, my + 2)],
                   dim(SAND, 0.9), 1.6)
        if ma_first:
            c.pulse_ellipse(700, my - 2, 74, 22, dim(HL, 0.85), width=2,
                            first=True)


# ---------------------------------------------------------------------------
# Chapter 7 — the two laws at war in one man
# ---------------------------------------------------------------------------

def draw_ch7(c, v, pos):
    cx7, gy = W / 2 + 40, 430
    c.line((140, gy), (W - 140, gy), dim(SAND_DIM, 0.8), 1.5)

    # vv1-6: the marriage released (inset, left)
    rel_on, rel_first = since(pos, 7, 2)
    if rel_on and v <= 8:
        rx7, ry7 = 200, 170
        c.circle(rx7 - 20, ry7, 22, stroke=dim(SAND, 0.9), width=2.2)
        freed, freed_first = since(pos, 7, 4)
        if freed:
            c.path(f"M{rx7 + 34},{ry7 - 22} A22,22 0 1 1 {rx7 + 10},{ry7 + 8}",
                   stroke=dim(GOLD, 0.95), width=2.2)
            c.text((rx7 + 6, ry7 + 52), "DEAD TO THE LAW", 13,
                   HL if v == 4 else TEXT_DIM, "mm", bold=v == 4)
            if freed_first:
                c.pulse_ellipse(rx7 + 22, ry7 - 8, 32, 32, dim(HL, 0.85),
                                width=2, first=True)
        else:
            c.circle(rx7 + 22, ry7, 22, stroke=dim(SAND, 0.9), width=2.2)
            c.text((rx7 + 2, ry7 + 52), "BOUND BY LAW", 13, TEXT_DIM, "mm")
        if rel_first:
            c.pulse_ellipse(rx7, ry7, 56, 34, dim(HL, 0.8), width=2,
                            first=True)

    # the divided man
    lean = 0
    if 14 <= v <= 23:
        lean = -8 if v % 2 else 8
    figure(c, cx7 + lean * 0.4, gy, 108, dim(SAND, 0.95), 2.4,
           arms="up" if v >= 24 else "open")

    # the law above, held in light
    tx, ty = cx7, 120
    c.rect(tx - 34, ty - 26, 68, 62, stroke=GOLD, width=2.2, rx=10,
           fill=dim(GOLD, 0.07))
    for r in range(3):
        c.line((tx - 20, ty - 8 + r * 15), (tx + 20, ty - 8 + r * 15),
               dim(GOLD, 0.8), 1.5)
    for k in range(5):
        a = math.pi * (0.2 + 0.6 * k / 4)
        c.line((tx + 44 * math.cos(a), ty + 4 - 40 * math.sin(a)),
               (tx + 60 * math.cos(a), ty + 4 - 56 * math.sin(a)),
               dim(GOLD, 0.45), 1.4)
    if v <= 23:
        c.text((tx, ty - 44), "THE LAW — HOLY, JUST, GOOD", 14,
               HL if v in (12, 22) else TEXT_DIM, "mm", bold=v in (12, 22))
    # the up-cord: delight of the inward man
    up_col = dim(GOLD, 0.9 if v >= 22 else 0.55)
    c.line((cx7, gy - 104), (tx, ty + 40), up_col, 2)
    de_on, de_first = since(pos, 7, 22)
    if de_on:
        c.text((cx7 + 24, 300), "THE INWARD MAN", 13, HL, "lm",
               bold=de_first)

    # the sin-block below, chained to the members
    bx7, by7 = cx7, gy + 74
    c.rect(bx7 - 40, by7 - 20, 80, 40, fill=dim((40, 22, 22), 0.9),
           stroke=dim(RED, 0.9), width=2)
    c.text((bx7, by7), "SIN", 15, dim(RED, 1.0), "mm", bold=True)
    n_links = 3
    broken, broken_first = since(pos, 7, 25)
    for i in range(n_links):
        ly = gy + 8 + i * 16
        if broken and i >= 1:
            break
        c.circle(bx7, ly, 7, stroke=dim(RED, 0.85), width=2)
    if broken:
        c.text((bx7 + 120, by7 - 34), "THANKS BE TO GOD", 14, HL, "mm",
               bold=broken_first)
        if broken_first:
            c.pulse_ellipse(bx7, gy + 30, 26, 26, dim(HL, 0.9), width=2,
                            first=True)
    c.text((bx7 + 120, by7), "IN MY MEMBERS", 12.5, dim(TEXT_DIM, 0.95),
           "mm", italic=True)

    # v7: the commandment that exposed
    cov_on, cov_first = since(pos, 7, 7)
    if cov_on and v <= 13:
        phrase(c, (W - 240, 150), "YOU SHALL NOT COVET", 18,
               HL if 7 <= v <= 8 else dim(TEXT, 0.85), first=cov_first)
        if pos >= P(7, 9):
            c.text((W - 240, 184), "SIN REVIVED — I DIED", 13.5,
                   dim(RED, 0.95), "mm", bold=v == 9)

    # vv15-20: the war annotated
    war_on, _ = since(pos, 7, 15)
    if war_on and v <= 23:
        c.polyline([(cx7 - 150, gy - 150), (cx7 - 150, gy - 190)],
                   dim(GOLD, 0.85), 2)
        c.polyline([(cx7 - 157, gy - 180), (cx7 - 150, gy - 192),
                    (cx7 - 143, gy - 180)], dim(GOLD, 0.85), 2)
        c.text((cx7 - 150, gy - 208), "WHAT I WANT", 12.5, TEXT, "mm")
        c.polyline([(cx7 + 170, gy - 190), (cx7 + 170, gy - 150)],
                   dim(RED, 0.85), 2)
        c.polyline([(cx7 + 163, gy - 160), (cx7 + 170, gy - 148),
                    (cx7 + 177, gy - 160)], dim(RED, 0.85), 2)
        c.text((cx7 + 170, gy - 208), "WHAT I DO", 12.5, dim(RED, 0.95),
               "mm")
    wr_on, wr_first = since(pos, 7, 24)
    if wr_on:
        phrase(c, (W / 2, 64), "WHO WILL DELIVER ME?", 24, HL,
               first=wr_first)


# ---------------------------------------------------------------------------
# Chapter 8 — no condemnation, and nothing can separate
# ---------------------------------------------------------------------------

CHAIN_LINKS = [("FOREKNEW", (8, 29)), ("PREDESTINED", (8, 29)),
               ("CALLED", (8, 30)), ("JUSTIFIED", (8, 30)),
               ("GLORIFIED", (8, 30))]


def draw_ch8(c, v, pos):
    gy = 440
    cx8 = W / 2
    c.line((120, gy), (W - 120, gy), dim(SAND_DIM, 0.8), 1.5)

    # v1: the verdict of ch3 shattered
    if v <= 4:
        sx, sy = cx8, 160
        sw, sh = 190, 46
        c.rect(sx - sw / 2, sy - sh / 2, sw, sh, stroke=dim(RED, 0.55),
               width=2, rx=5)
        c.text((sx, sy), "GUILTY", 26, dim(RED, 0.6), "mm", bold=True)
        c.line((sx - sw / 2 - 12, sy + sh / 2 + 8),
               (sx + sw / 2 + 12, sy - sh / 2 - 8), HL, 3.4)
        for ddx, ddy in ((-sw / 2 - 26, 18), (sw / 2 + 22, -14),
                         (-30, sh / 2 + 22), (44, -sh / 2 - 20)):
            c.line((sx + ddx, sy + ddy), (sx + ddx * 1.14, sy + ddy * 1.3),
                   dim(RED, 0.5), 1.6)
        phrase(c, (cx8, 84), "NO CONDEMNATION", 28, HL, first=v == 1)

    # the figure — in the Spirit
    arms = "up" if v >= 31 else "open"
    figure(c, cx8, gy, 100, GOLD, 2.4, arms=arms)

    # vv2-11: the Spirit descends
    sp_on, sp_first = since(pos, 8, 5)
    if sp_on and v <= 27:
        for k in range(5):
            a = math.pi * (0.30 + 0.4 * k / 4)
            x0 = cx8 + 120 * math.cos(a)
            y0 = gy - 250 - 40 * math.sin(a)
            c.line((x0, y0), (cx8 + 30 * math.cos(a), gy - 150),
                   dim(GOLD, 0.35), 1.6)
        if not 17 <= v <= 25:          # the sonship block owns the centre
            c.text((cx8, gy - 300), "THE SPIRIT", 15,
                   HL if 2 <= v <= 11 or 26 <= v <= 27 else TEXT_DIM, "mm",
                   bold=2 <= v <= 11)
    if 5 <= v <= 8:
        c.text((cx8 - 240, gy - 60), "THE MIND OF THE FLESH", 13,
               dim(RED, 0.9), "mm", bold=v in (6, 7))
        c.text((cx8 - 240, gy - 40), "death", 12, dim(TEXT_DIM, 0.9), "mm",
               italic=True)
        c.text((cx8 + 240, gy - 60), "THE MIND OF THE SPIRIT", 13, HL,
               "mm", bold=v == 6)
        c.text((cx8 + 240, gy - 40), "life and peace", 12,
               dim(TEXT_DIM, 0.9), "mm", italic=True)

    # vv14-17: Abba — sonship
    ab_on, ab_first = since(pos, 8, 15)
    if ab_on and v <= 25:
        phrase(c, (cx8, 110), "ABBA — FATHER", 24, HL, first=ab_first)
        if pos >= P(8, 17):
            c.text((cx8, 146), "HEIRS OF GOD, JOINT HEIRS WITH CHRIST",
                   14, dim(TEXT, 0.9), "mm", bold=v == 17)

    # vv18-25: creation groans (the ground itself bows)
    gr_on, gr_first = since(pos, 8, 19)
    if gr_on and v <= 27:
        c.path(f"M{170},{gy + 40} Q{cx8},{gy + 78} {W - 170},{gy + 40}",
               stroke=dim(SAND_DIM, 0.95), width=2)
        # one more of creation joins the groaning each verse (vv19-23)
        for i in range(max(1, min(5, v - 18))):
            gx = 260 + i * 130
            fresh = i == v - 19
            col_g = dim(SAND, 0.95 if fresh else 0.7)
            c.polyline([(gx, gy + 66), (gx, gy + 52)], col_g, 1.6)
            c.polyline([(gx - 5, gy + 60), (gx, gy + 50), (gx + 5, gy + 60)],
                       col_g, 1.6)
            if fresh:
                c.pulse_ellipse(gx, gy + 56, 14, 16, dim(HL, 0.8), width=1.6,
                                first=True)
        c.text((cx8, gy + 96), "CREATION WAITS — GROANING, IN HOPE", 13.5,
               HL if 19 <= v <= 22 else TEXT_DIM, "mm", bold=19 <= v <= 22)

    # vv28-30: the golden chain arcs overhead
    n_links = 0
    for i, (_, at) in enumerate(CHAIN_LINKS):
        if pos >= P(*at):
            n_links = i + 1
    all_on, all_first = since(pos, 8, 28)
    if all_on and v <= 30:
        c.text((cx8, 78), "ALL THINGS WORK TOGETHER FOR GOOD", 15,
               HL if v == 28 else dim(TEXT, 0.85), "mm", bold=v == 28)
    if n_links and 29 <= v <= 30:
        for i in range(n_links):
            a = math.pi * (0.82 - 0.64 * i / 4)
            lx = cx8 + 320 * math.cos(a)
            ly = 330 - 190 * math.sin(a)
            fresh = (v == 29 and i < 2 and n_links == 2) or \
                    (v == 30 and i >= 2)
            c.circle(lx, ly, 15, stroke=HL if fresh else GOLD,
                     width=3)
            if i < n_links - 1:
                a2 = math.pi * (0.82 - 0.64 * (i + 1) / 4)
                c.line((lx + 15 * math.cos(a - 0.5), ly - 15 * math.sin(a - 0.5)),
                       (cx8 + 320 * math.cos(a2) - 15 * math.cos(a2 + 0.5),
                        330 - 190 * math.sin(a2) + 15 * math.sin(a2 + 0.5)),
                       dim(GOLD, 0.8), 2)
            name = CHAIN_LINKS[i][0]
            c.text((lx, ly + 30), name, 12.5,
                   HL if fresh else dim(TEXT, 0.8), "mm", bold=fresh)
            if fresh:
                c.pulse_ellipse(lx, ly, 21, 21, dim(HL, 0.9), width=2,
                                first=True)

    # vv31-39: the ring nothing breaks through
    ring_on, ring_first = since(pos, 8, 31)
    if ring_on:
        r = 132 if v < 38 else 148
        c.circle(cx8, gy - 80, r, stroke=dim(GOLD, 0.85), width=2.6)
        if v >= 38:
            c.circle(cx8, gy - 80, r - 14, stroke=dim(GOLD, 0.5), width=1.6)
        if ring_first or v == 38:
            c.pulse_ellipse(cx8, gy - 80, r + 8, r + 8, dim(HL, 0.9),
                            width=2.4, first=True)
        arrows = [("TRIBULATION", 2.60, (8, 35)), ("DISTRESS", 2.95, (8, 35)),
                  ("PERSECUTION", 0.55, (8, 35)), ("FAMINE", 0.18, (8, 35)),
                  ("SWORD", 5.9, (8, 35)), ("DEATH", 3.6, (8, 38)),
                  ("LIFE", 5.3, (8, 38)), ("HEIGHT", 0.9, (8, 39)),
                  ("DEPTH", 4.4, (8, 39))]
        for name, a, at in arrows:
            on, a_first = since(pos, *at)
            if not on:
                continue
            rr1 = r + 74
            y1 = gy - 80 - rr1 * math.sin(a)
            if y1 > 552:                   # keep inside the frame
                rr1 = (552 - (gy - 80)) / -math.sin(a)
                y1 = 552
            x1 = cx8 + rr1 * math.cos(a)
            x2 = cx8 + (r + 10) * math.cos(a)
            y2 = gy - 80 - (r + 10) * math.sin(a)
            c.line((x1, y1), (x2, y2), dim(RED, 0.7), 2)
            # the deflected tip
            c.polyline([(x2, y2),
                        (x2 + 12 * math.cos(a + 2.2), y2 - 12 * math.sin(a + 2.2))],
                       dim(RED, 0.7), 2)
            if name in ("TRIBULATION", "SWORD", "DEATH", "HEIGHT"):
                c.text((x1 + 16 * math.cos(a), y1 - 16 * math.sin(a)), name,
                       11.5, dim(RED, 0.85), "mm")
            if a_first and name in ("TRIBULATION", "DEATH", "HEIGHT"):
                c.pulse_ellipse(x2, y2, 12, 12, dim(RED, 0.8), width=1.6,
                                first=True)
        conq_on, conq_first = since(pos, 8, 37)
        if conq_on:
            phrase(c, (cx8, 84), "MORE THAN CONQUERORS", 26, HL,
                   first=conq_first)
        sep_on, sep_first = since(pos, 8, 38)
        if sep_on:
            c.text((cx8, 122), "NOTHING CAN SEPARATE US FROM THE LOVE OF GOD",
                   15, HL, "mm", bold=sep_first)


# ---------------------------------------------------------------------------
# Chapter 9 — the potter, the line, the stone on the road
# ---------------------------------------------------------------------------

def draw_ch9(c, v, pos):
    if v >= 30:
        # the stumbling stone, laid in the roadway itself
        road_horizon(c)
        draw_road(c, pos)
        draw_arch(c, pos)
        draw_milestone(c, "M1", pos)
        draw_milestone(c, "M2", pos)
        draw_milestone(c, "M3", pos)
        st_on, st_first = since(pos, 9, 32)
        if st_on:
            sx, sy = road_pt(0.30)
            c.polygon([(sx - 34, sy + 6), (sx - 10, sy - 22), (sx + 26, sy - 16),
                       (sx + 38, sy + 8), (sx + 6, sy + 16)],
                      fill=dim(GRAY, 0.6), stroke=dim(SAND, 0.95), width=2)
            c.text((sx, sy + 38), "A STONE OF STUMBLING", 14,
                   dim(RED, 0.95), "mm", bold=v == 32)
            c.text((sx, sy - 36), "LAID IN ZION", 13, dim(TEXT, 0.9), "mm",
                   italic=True)
            if st_first:
                c.pulse_ellipse(sx, sy, 48, 30, dim(RED, 0.85), width=2,
                                first=True)
        if v >= 33:
            phrase(c, (W / 2, 100), "WHO BELIEVES WILL NOT BE DISAPPOINTED",
                   21, HL, first=v == 33)
        else:
            c.text((W / 2, 100), "RIGHTEOUSNESS — NOT BY WORKS BUT BY FAITH",
                   15, dim(TEXT, 0.9), "mm", bold=v == 30)
        return

    # the potter's house
    wx, wy = 700, 350                     # wheel centre
    gy = wy + 60
    c.line((420, gy), (W - 80, gy), dim(SAND_DIM, 0.8), 1.5)
    # wheel: two discs and an axle
    c.ellipse(wx, wy + 34, 96, 17, stroke=dim(BROWN, 0.95), width=2.6,
              fill=dim(BROWN, 0.25))
    c.ellipse(wx, wy + 12, 60, 11, stroke=dim(BROWN, 0.95), width=2)
    c.line((wx, wy + 46), (wx, wy + 12), dim(BROWN, 0.95), 3)
    # the wheel is turning: a chip in the rim comes round as the chapter runs
    a_w = 0.8 * v
    c.circle(wx + 92 * math.cos(a_w), wy + 34 + 15 * math.sin(a_w), 4.5,
             fill=dim(BROWN, 0.9), stroke=dim(SAND, 0.85), width=1.3)
    # the lump / the vessel forming
    pot_on, pot_first = since(pos, 9, 20)
    if not pot_on:
        c.ellipse(wx, wy - 4, 30, 20, stroke=dim(SAND, 0.95), width=2.2,
                  fill=dim(BROWN, 0.35))
        c.text((wx, wy - 44), "THE CLAY", 13, TEXT_DIM, "mm")
    else:
        c.path(f"M{wx - 26},{wy + 4} C{wx - 34},{wy - 30} {wx - 12},{wy - 40} "
               f"{wx - 10},{wy - 52} L{wx + 10},{wy - 52} C{wx + 12},{wy - 40} "
               f"{wx + 34},{wy - 30} {wx + 26},{wy + 4}",
               stroke=dim(SAND, 0.95), width=2.2, fill=dim(BROWN, 0.35))
        c.text((wx, wy - 84), "THE POTTER'S RIGHT", 13.5,
               HL if 20 <= v <= 21 else TEXT_DIM, "mm", bold=20 <= v <= 21)
        if pot_first:
            c.pulse_ellipse(wx, wy - 20, 46, 46, dim(HL, 0.85), width=2,
                            first=True)
    # the two finished vessels (vv21-23)
    ves_on, ves_first = since(pos, 9, 21)
    if ves_on:
        hx, hy = wx + 170, gy
        c.path(f"M{hx - 20},{hy} C{hx - 26},{hy - 28} {hx - 8},{hy - 34} "
               f"{hx - 7},{hy - 46} L{hx + 7},{hy - 46} C{hx + 8},{hy - 34} "
               f"{hx + 26},{hy - 28} {hx + 20},{hy}",
               stroke=GOLD, width=2.2, fill=dim(GOLD, 0.14))
        c.text((hx, hy + 20), "HONOR", 12.5, HL, "mm",
               bold=21 <= v <= 23)
        dx2, dy2 = wx + 250, gy
        c.path(f"M{dx2 - 16},{dy2} C{dx2 - 20},{dy2 - 20} {dx2 - 6},{dy2 - 26} "
               f"{dx2 - 5},{dy2 - 34} L{dx2 + 5},{dy2 - 34} C{dx2 + 6},{dy2 - 20} "
               f"{dx2 + 20},{dy2 - 20} {dx2 + 16},{dy2}",
               stroke=dim(GRAY, 0.95), width=2, fill=dim(GRAY, 0.2))
        c.text((dx2, dy2 + 20), "COMMON", 12.5, dim(TEXT_DIM, 0.95), "mm")
        if ves_first:
            c.pulse_ellipse(hx, hy - 24, 34, 34, dim(HL, 0.85), width=2,
                            first=True)

    # the chosen line (vv6-13), stage left
    line_on, _ = since(pos, 9, 6)
    if line_on:
        lx0, ly0 = 150, 150
        gens = [("ABRAHAM", (9, 6)), ("ISAAC", (9, 7)), ("JACOB", (9, 13))]
        drops = [("ISHMAEL", 0, (9, 8)), ("ESAU", 1, (9, 13))]
        for i, (name, at) in enumerate(gens):
            on, g_first = since(pos, *at)
            if not on:
                continue
            ny = ly0 + i * 74
            lit = v == at[1] or (name == "JACOB" and 10 <= v <= 13)
            c.circle(lx0, ny, 6, fill=HL if lit else dim(GOLD, 0.85))
            c.text((lx0 + 20, ny), name, 14.5, HL if lit else TEXT, "lm",
                   bold=lit)
            if i:
                c.line((lx0, ny - 68), (lx0, ny - 6), dim(GOLD, 0.8), 2)
            if g_first:
                c.pulse_ellipse(lx0, ny, 14, 14, dim(HL, 0.9), width=2,
                                first=True)
        for name, gen_i, at in drops:
            on, d_first = since(pos, *at)
            if not on:
                continue
            ny = ly0 + gen_i * 74 + 37
            c.line((lx0, ny - 20), (lx0 - 46, ny + 10), dim(SAND_DIM, 1.0),
                   1.8)
            c.text((lx0 - 52, ny + 22), name, 12, dim(TEXT_DIM, 0.9), "rm")
        c.text((lx0 + 90, ly0 - 40), "CHILDREN OF THE PROMISE", 13.5,
               HL if 6 <= v <= 9 else TEXT_DIM, "mm", bold=6 <= v <= 9)
    # vv14-18: mercy on whom I will
    me_on, me_first = since(pos, 9, 15)
    if me_on and v <= 19:
        phrase(c, (W / 2, 66), "MERCY ON WHOM I WILL HAVE MERCY", 19,
               HL if 14 <= v <= 18 else dim(TEXT, 0.85), first=me_first)
        if pos >= P(9, 17):
            c.text((260, 400), "PHARAOH", 13,
                   dim(RED, 0.9) if 17 <= v <= 18 else TEXT_DIM, "mm",
                   bold=17 <= v <= 18)
            c.text((260, 420), "hardened", 11.5, dim(TEXT_DIM, 0.9), "mm",
                   italic=True)
    # vv25-29: the remnant chip
    rem_on, rem_first = since(pos, 9, 27)
    if rem_on:
        c.rect(180, 470, 168, 32, stroke=dim(GOLD, 0.85), width=1.8, rx=16,
               fill=dim(GOLD, 0.14))
        c.text((264, 486), "A REMNANT SAVED", 14, HL, "mm", bold=v == 27)
        if rem_first:
            c.pulse_rect(180, 470, 168, 32, dim(HL, 0.85), width=2,
                         first=True, rx=16)


# ---------------------------------------------------------------------------
# Chapter 10 — the word is near: the road reaches the arch
# ---------------------------------------------------------------------------

def draw_ch10(c, v, pos):
    road_horizon(c)
    draw_road(c, pos)
    lit = v >= 13
    draw_arch(c, pos, lit=lit, lit_first=v == 13,
              label="SALVATION" if lit else "ROME")
    draw_milestone(c, "M1", pos)
    draw_milestone(c, "M2", pos)
    draw_milestone(c, "M3", pos)
    draw_milestone(c, "M4", pos, focus_key="M4" if 9 <= v <= 13 else None,
                   focus_first=v == 9)

    if v <= 4:
        # zeal without knowledge: a runner off the road, against the verge
        rx, ry = 260, 300
        figure(c, rx, ry, 64, dim(SAND_DIM, 1.0), 2, legs="walk")
        c.polyline([(rx + 24, ry - 30), (rx + 56, ry - 36)],
                   dim(RED, 0.7), 1.8, dash="4,5")
        c.text((rx, ry + 22), "ZEAL, NOT KNOWLEDGE", 12.5,
               dim(TEXT_DIM, 0.95), "mm", italic=True)
        c.text((W / 2, 96), "CHRIST — THE END OF THE LAW", 17,
               HL if v == 4 else dim(TEXT, 0.85), "mm", bold=v == 4)
    if 5 <= v <= 8:
        phrase(c, (W / 2, 96), "THE WORD IS NEAR YOU", 24, HL,
               first=v == 8)
        if v >= 8:
            c.text((W / 2, 132), "IN YOUR MOUTH, AND IN YOUR HEART", 15,
                   dim(TEXT, 0.9), "mm")
    if 9 <= v <= 12:
        # mouth + heart glyphs beside the fresh milestone
        mx, my = 300, 130
        c.circle(mx, my, 17, stroke=HL, width=2.2)
        c.path(f"M{mx - 7},{my + 1} Q{mx},{my + 10} {mx + 7},{my + 1}",
               stroke=HL, width=2)
        c.text((mx, my + 38), "CONFESS", 13, HL, "mm", bold=v == 9)
        hx2 = mx + 110
        c.path(f"M{hx2},{my + 14} C{hx2 - 20},{my - 4} {hx2 - 14},{my - 22} "
               f"{hx2},{my - 12} C{hx2 + 14},{my - 22} {hx2 + 20},{my - 4} "
               f"{hx2},{my + 14}", stroke=HL, width=2.2)
        c.text((hx2, my + 38), "BELIEVE", 13, HL, "mm", bold=v == 10)
        phrase(c, (W / 2 + 160, 100), "JESUS IS LORD", 24, HL,
               first=v == 9)
        if v >= 12:
            c.text((W / 2 + 160, 136), "THE SAME LORD OVER ALL", 14,
                   dim(TEXT, 0.9), "mm")
    if v == 13:
        phrase(c, (W / 2, 96), "WHOEVER WILL CALL ON THE NAME", 22, HL,
               first=True)
        c.text((W / 2, 132), "OF THE LORD WILL BE SAVED", 18, HL, "mm",
               bold=True)
    # vv14-17: the sending — messengers run outward from the arch
    sent_on, sent_first = since(pos, 10, 14)
    if sent_on:
        for i, t in enumerate((0.86, 0.68, 0.5)):
            if v < 14 + i and v <= 17:
                continue
            mx2, my2 = road_pt(t)
            s = road_scale(t)
            # 84 rather than 54: the perspective ramp is kept, but the far end
            # of it now starts above the height a drawn body needs to read as
            # one. At the old base the whole company was under forty pixels.
            figure(c, mx2 + 20 * s, my2, 84 * s, GOLD, 2, legs="walk")
        c.text((W / 2, 96), "HOW BEAUTIFUL ARE THE FEET", 19,
               HL if 14 <= v <= 15 else dim(TEXT, 0.85), "mm",
               bold=14 <= v <= 15)
        if sent_first:
            mx2, my2 = road_pt(0.86)
            c.pulse_ellipse(mx2 + 16, my2 - 20, 26, 34, dim(HL, 0.9),
                            width=2, first=True)
    snd_on, _ = since(pos, 10, 18)
    if snd_on:
        # their sound went out — rings from the arch to the world's ends
        for i, rr in enumerate((40, 72, 106)):
            if v < 18:
                break
            c.path(f"M{ARCH_X - rr},{ARCH_Y - 8} "
                   f"A{rr},{rr * 0.6} 0 0 1 {ARCH_X + rr},{ARCH_Y - 8}",
                   stroke=dim(GOLD, 0.55 - i * 0.13), width=1.8)
        c.text((ARCH_X, ARCH_Y - 120), "TO THE ENDS OF THE WORLD", 13,
               HL if v == 18 else TEXT_DIM, "mm", bold=v == 18)
    hands_on, hands_first = since(pos, 10, 21)
    if hands_on:
        hx3, hy3 = 200, 180
        for a in (-0.35, 0.0, 0.35):
            c.line((hx3, hy3), (hx3 + 90 * math.cos(a - 0.5),
                                hy3 + 90 * math.sin(a - 0.5)),
                   dim(GOLD, 0.8), 2.4, linecap="round")
        c.text((hx3 + 10, hy3 + 74), "ALL DAY LONG", 13.5, HL, "mm",
               bold=True)
        c.text((hx3 + 10, hy3 + 94), "I stretched out my hands", 12,
               dim(TEXT_DIM, 0.95), "mm", italic=True)


# ---------------------------------------------------------------------------
# Chapter 11 — the olive tree, kept and enlarged
# ---------------------------------------------------------------------------

TRUNK_X, ROOT_Y, FORK_Y = 512, 430, 260

NATURAL = [(300, 190, True), (356, 138, False), (430, 104, True),
           (512, 90, False), (596, 112, True), (668, 152, False),
           (724, 204, True)]
WILD_TIPS = [(792, 240), (826, 286), (844, 338)]


def _leaves(c, x, y, col, r=10):
    for ddx, ddy in ((-11, 2), (0, -9), (11, 2)):
        c.ellipse(x + ddx, y + ddy, r, r * 0.55, fill=col)


def draw_ch11(c, v, pos):
    graft_on = pos >= P(11, 17)
    restored = pos >= P(11, 26)

    # doxology (vv33-36): rings behind the whole tree
    dox_on, dox_first = since(pos, 11, 33)
    if dox_on:
        for i, rr in enumerate((150, 210, 270)):
            c.circle(TRUNK_X, FORK_Y + 30, rr, stroke=dim(GOLD, 0.4 - i * 0.09),
                     width=1.6)
        for i, wrd in enumerate(("OF HIM", "THROUGH HIM", "TO HIM")):
            on2, w_first = since(pos, 11, 33 + min(i, 3))
            if pos >= P(11, 36) or on2:
                a = math.pi * (0.25 + 0.25 * i)
                lx = TRUNK_X + (270) * math.cos(a)
                ly = FORK_Y + 30 - 250 * math.sin(a)
                c.text((lx, ly), wrd, 14.5, HL if v >= 36 else dim(TEXT, 0.85),
                       "mm", bold=v >= 36)
        phrase(c, (W / 2, 62), "O THE DEPTH OF THE RICHES", 21, HL,
               first=dox_first)

    c.ellipse(TRUNK_X, ROOT_Y, 150, 22, fill=dim(BROWN, 0.45),
              stroke=dim(BROWN, 0.9), width=2)
    c.text((TRUNK_X, ROOT_Y + 36), "THE ROOT", 15,
           HL if v in (16, 18) else TEXT_DIM, "mm", bold=v in (16, 18))
    c.polyline([(TRUNK_X - 13, ROOT_Y), (TRUNK_X - 9, FORK_Y),
                (TRUNK_X + 9, FORK_Y), (TRUNK_X + 13, ROOT_Y)],
               dim(BROWN, 0.9), 2, closed=True, fill=dim(BROWN, 0.55))

    for tx, ty, breaks in NATURAL:
        mx, my = (TRUNK_X + tx) / 2, (FORK_Y + ty) / 2 - 20
        gone = breaks and graft_on and not restored
        if gone:
            c.polyline([(TRUNK_X, FORK_Y),
                        ((TRUNK_X + mx) / 2, (FORK_Y + my) / 2)],
                       dim(OLIVE, 0.45), 4)
            c.polyline([(mx, my + 66), (tx - 12, ty + 104)],
                       dim(OLIVE, 0.35), 3)
        else:
            grafted_back = breaks and restored
            c.polyline([(TRUNK_X, FORK_Y), (mx, my), (tx, ty)], OLIVE, 4)
            _leaves(c, tx, ty, dim(OLIVE, 0.62 if grafted_back else 0.9))
            if grafted_back and pos == P(11, 26):
                c.pulse_ellipse(tx, ty, 22, 16, dim(HL, 0.85), width=1.8,
                                first=True)
    if not dox_on:
        c.text((285, 122), "ISRAEL", 16,
               HL if v in (1, 2, 7, 26) else TEXT_DIM, "mm",
               bold=v in (1, 2, 26))

    if graft_on:
        for i, (tx, ty) in enumerate(WILD_TIPS):
            on, wild_first = since(pos, 11, 17 + i)
            if not on:
                continue
            pts = [(TRUNK_X, FORK_Y + 20 + i * 13),
                   ((TRUNK_X + tx) / 2 + 22, (FORK_Y + ty) / 2 + 12),
                   (tx, ty)]
            if wild_first:
                c.traced(pts, WILD, 4, dur="1.6s")
            else:
                c.polyline(pts, WILD, 4)
            _leaves(c, tx, ty, dim(WILD, 0.9))
            c.rect(TRUNK_X - 15, FORK_Y + 14 + i * 13, 30, 9,
                   fill=dim(GOLD, 0.55), rx=3)
        if not dox_on:
            c.text((866, 176), "GENTILES", 16,
                   HL if 17 <= v <= 24 else TEXT_DIM, "mm",
                   bold=17 <= v <= 24)
            c.text((866, 198), "a wild olive, grafted in", 12,
                   dim(TEXT_DIM, 0.95), "mm", italic=True)

    # vv1-5: Elijah and the seven thousand
    sev_on, sev_first = since(pos, 11, 4)
    if sev_on and v <= 10:
        c.rect(140, 350, 170, 34, stroke=dim(GOLD, 0.85), width=1.8,
               rx=17, fill=dim(GOLD, 0.16))
        c.text((225, 367), "7000 RESERVED", 15.5, HL, "mm",
               bold=4 <= v <= 5)
        if sev_first:
            c.pulse_rect(140, 350, 170, 34, dim(HL, 0.9), width=2,
                         first=True, rx=17)
    if pos >= P(11, 5) and v <= 16:
        c.text((225, 402), "a remnant, by grace", 12.5,
               dim(TEXT_DIM, 0.95), "mm", italic=True)

    # vv8-15: the fall, and what came of it — one beat drawn per verse, so
    # the tree is never simply held while the argument moves
    if 8 <= v <= 16:
        eye_on, eye_first = since(pos, 11, 8)
        if eye_on:
            ex3, ey3 = 176, 232
            for k in (-1, 1):
                c.path(f"M{ex3 - 27},{ey3} Q{ex3},{ey3 + k * 17} "
                       f"{ex3 + 27},{ey3}", stroke=dim(SAND, 0.9), width=2)
            dark_eye = pos >= P(11, 10)
            if dark_eye:
                c.line((ex3 - 27, ey3), (ex3 + 27, ey3), dim(GRAY, 0.95), 2.6)
            else:
                c.circle(ex3, ey3, 6, fill=dim(SAND, 0.8))
            c.text((ex3, ey3 + 38), "DARKENED" if dark_eye else "SLUMBER",
                   12, dim(TEXT_DIM, 0.95), "mm")
            if eye_first or pos == P(11, 10):
                c.pulse_ellipse(ex3, ey3, 36, 24, dim(HL, 0.8), width=1.8,
                                first=True)
        sn_on, sn_first = since(pos, 11, 9)
        if sn_on:
            c.ellipse(262, 486, 30, 11, stroke=dim(RED, 0.8), width=2)
            c.polyline([(292, 486), (326, 470)], dim(RED, 0.8), 2)
            c.text((262, 510), "A SNARE", 12, dim(RED, 0.9), "mm")
            if sn_first:
                c.pulse_ellipse(262, 486, 42, 22, dim(HL, 0.8), width=1.8,
                                first=True)
        fu_on, fu_first = since(pos, 11, 12)
        if fu_on:
            c.rect(392, 452, 28, 36, stroke=dim(OLIVE, 0.95), width=2, rx=3)
            c.rect(394, 460, 24, 26, fill=dim(OLIVE, 0.55))
            c.text((406, 506), "FULNESS", 12, dim(TEXT, 0.85), "mm")
            if fu_first:
                c.pulse_rect(388, 448, 36, 44, dim(HL, 0.85), width=1.8,
                             first=True, rx=4)
        if pos >= P(11, 13) and graft_on:
            for tx, ty in WILD_TIPS:
                c.circle(tx, ty, 20, stroke=dim(WILD, 0.55), width=1.5)
        je_on, je_first = since(pos, 11, 14)
        if je_on:
            # what the Gentiles received swings back toward Israel
            arc_j = [(892 - 176 * t,
                      392 + 34 * math.sin(math.pi * t) + 26 * t)
                     for t in [i / 12 for i in range(13)]]
            if je_first:
                c.traced(arc_j, dim(GOLD, 0.8), 2, dur="1.6s")
            else:
                c.polyline(arc_j, dim(GOLD, 0.8), 2)
            c.polyline([(730, 410), (716, 418), (730, 426)],
                       dim(GOLD, 0.8), 2)
            c.text((806, 466), "TO JEALOUSY", 12, dim(TEXT, 0.85), "mm")
        li_on, li_first = since(pos, 11, 15)
        if li_on:
            c.polyline([(600, 506), (600, 470)], dim(GOLD, 0.9), 2.4)
            c.polyline([(592, 480), (600, 466), (608, 480)],
                       dim(GOLD, 0.9), 2.4)
            c.text((600, 528), "LIFE FROM THE DEAD", 12, HL, "mm",
                   bold=v == 15)
            if li_first:
                c.pulse_ellipse(600, 486, 26, 32, dim(HL, 0.85), width=1.8,
                                first=True)

    # vv28-32: mercy widening — an arc laid under the tree per verse
    if 28 <= v <= 32:
        if pos >= P(11, 28):
            c.ellipse(TRUNK_X, ROOT_Y, 168, 30, stroke=dim(GOLD, 0.35),
                      width=1.6)
        if pos >= P(11, 29):
            c.ellipse(TRUNK_X, ROOT_Y, 188, 38, stroke=dim(GOLD, 0.22),
                      width=1.4)
        for i in range(max(0, min(3, v - 29))):
            r_m = 200 + i * 30
            c.path(f"M{TRUNK_X - r_m},{ROOT_Y} A{r_m},{r_m * 0.40} 0 0 0 "
                   f"{TRUNK_X + r_m},{ROOT_Y}",
                   stroke=dim(GOLD, 0.60 - i * 0.13), width=1.8)
        if v >= 32:
            c.text((TRUNK_X, 552), "MERCY ON ALL", 14, HL, "mm", bold=True)

    # v18: boast not
    bo_on, bo_first = since(pos, 11, 18)
    if bo_on and v <= 24:
        c.text((866, 258), "BOAST NOT", 13.5, dim(RED, 0.95), "mm",
               bold=18 <= v <= 21)
        c.text((866, 278), "the root bears you", 12, dim(TEXT_DIM, 0.95),
               "mm", italic=True)
    sav_on, sav_first = since(pos, 11, 26)
    if sav_on and not dox_on:
        phrase(c, (W / 2, 62), "ALL ISRAEL WILL BE SAVED", 21, HL,
               first=sav_first)


# ---------------------------------------------------------------------------
# Chapter 12 — the living sacrifice, the one body
# ---------------------------------------------------------------------------

GIFTS12 = [("PROPHECY", (12, 6)), ("SERVICE", (12, 7)), ("TEACHING", (12, 7)),
           ("EXHORTATION", (12, 8)), ("GIVING", (12, 8)),
           ("LEADING", (12, 8)), ("MERCY", (12, 8))]


def draw_ch12(c, v, pos):
    # the altar, stage left, with a living figure standing on it
    ax, ay = 270, 420
    c.rect(ax - 90, ay - 40, 180, 40, stroke=dim(SAND, 0.95), width=2.2,
           fill=dim(PANEL, 0.9))
    c.rect(ax - 70, ay - 58, 140, 18, stroke=dim(SAND, 0.9), width=1.8)
    c.line((ax - 110, ay), (ax + 110, ay), dim(SAND, 0.9), 2)
    # soft flame lines around the base
    for i, (fx, fh) in enumerate(((-62, 26), (-38, 36), (34, 32), (58, 24))):
        c.path(f"M{ax + fx},{ay - 58} Q{ax + fx - 9},{ay - 58 - fh * 0.55} "
               f"{ax + fx + 3},{ay - 58 - fh} "
               f"Q{ax + fx + 9},{ay - 58 - fh * 0.5} {ax + fx + 14},{ay - 58}",
               stroke=dim(GOLD, 0.6), width=1.7)
    figure(c, ax, ay - 58, 92, GOLD, 2.4, arms="open")
    phrase(c, (ax, ay - 250), "A LIVING SACRIFICE", 20, HL, first=v == 1)
    c.text((ax, ay + 26), "YOUR REASONABLE SERVICE", 12.5,
           dim(TEXT_DIM, 0.95), "mm", italic=True)
    # v2: the renewed mind — a halo hovering above the head
    tr_on, tr_first = since(pos, 12, 2)
    if tr_on:
        hy2 = ay - 58 - 92 - 16
        c.circle(ax, hy2, 14, stroke=HL if v == 2 else dim(GOLD, 0.8),
                 width=2)
        c.text((ax + 118, hy2 + 6), "TRANSFORMED", 13,
               HL if v == 2 else TEXT_DIM, "mm", bold=v == 2)
        if tr_first:
            c.pulse_ellipse(ax, hy2, 21, 21, dim(HL, 0.9), width=2,
                            first=True)

    # the one body: a ring of members, right of centre
    bx, by = 700, 270
    body_on, body_first = since(pos, 12, 4)
    if body_on:
        c.circle(bx, by, 108, stroke=dim(SAND, 0.85), width=2)
        c.text((bx, by), "ONE BODY", 16, HL if 4 <= v <= 5 else TEXT,
               "mm", bold=4 <= v <= 5)
        c.text((bx, by + 22), "many members", 12, dim(TEXT_DIM, 0.95),
               "mm", italic=True)
        if body_first:
            c.pulse_ellipse(bx, by, 114, 114, dim(HL, 0.85), width=2,
                            first=True)
        for i, (name, at) in enumerate(GIFTS12):
            on, g_first = since(pos, *at)
            if not on:
                continue
            a = math.pi / 2 - i * 2 * math.pi / 7
            gx = bx + 108 * math.cos(a)
            gyy = by - 108 * math.sin(a)
            lit = v == at[1]
            c.circle(gx, gyy, 7, fill=HL if lit else dim(GOLD, 0.85))
            lx = bx + 140 * math.cos(a)
            ly = by - 140 * math.sin(a)
            c.text((lx, ly), name, 12, HL if lit else dim(TEXT, 0.8), "mm",
                   bold=lit)
            if g_first:
                c.pulse_ellipse(gx, gyy, 14, 14, dim(HL, 0.9), width=1.8,
                                first=True)

        # vv9-21 are a list of thirteen things love does; each one kindles
        # another light inside the body, so the frame moves every verse
        if pos >= P(12, 9):
            n_love = min(13, v - 8)
            for i in range(n_love):
                a = math.pi / 2 - i * 2 * math.pi / 13
                mx2 = bx + 76 * math.cos(a)
                my2 = by - 76 * math.sin(a)
                fresh = i == n_love - 1
                c.circle(mx2, my2, 4.5 if fresh else 3,
                         fill=dim(HL if fresh else GOLD, 0.9))
                if fresh:
                    c.pulse_ellipse(mx2, my2, 11, 11, dim(HL, 0.85),
                                    width=1.6, first=True)

    # vv9-21: love's instructions — the burning coals and the overcome
    co_on, co_first = since(pos, 12, 20)
    if co_on:
        cx2, cy2 = 700, 470
        for i, (ox, r2) in enumerate(((-22, 8), (0, 10), (22, 8), (-10, 6),
                                      (12, 6))):
            c.circle(cx2 + ox, cy2 - (4 if i > 2 else 0), r2,
                     fill=dim(RED, 0.55), stroke=dim(GOLD, 0.8), width=1.4)
        for ox in (-14, 4, 20):
            c.path(f"M{cx2 + ox},{cy2 - 14} Q{cx2 + ox - 4},{cy2 - 24} "
                   f"{cx2 + ox + 2},{cy2 - 32}", stroke=dim(GOLD, 0.6),
                   width=1.5)
        c.text((cx2, cy2 + 24), "COALS OF FIRE", 12.5,
               HL if v == 20 else TEXT_DIM, "mm", bold=v == 20)
        if co_first:
            c.pulse_ellipse(cx2, cy2 - 8, 44, 30, dim(HL, 0.85), width=2,
                            first=True)
    ov_on, ov_first = since(pos, 12, 21)
    if ov_on:
        phrase(c, (W / 2, 66), "OVERCOME EVIL WITH GOOD", 24, HL,
               first=ov_first)
    elif pos >= P(12, 9):
        c.text((W / 2, 66), "LET LOVE BE WITHOUT HYPOCRISY", 16,
               HL if v == 9 else dim(TEXT, 0.85), "mm", bold=v == 9)


# ---------------------------------------------------------------------------
# Chapter 13 — the sword, the debt of love, the dawn
# ---------------------------------------------------------------------------

COMMANDS13 = ["NO ADULTERY", "NO MURDER", "NO STEALING", "NO COVETING"]


def draw_ch13(c, v, pos):
    # left: the governing authority — sword and tribute
    sx, sy = 200, 300
    c.line((sx, sy - 90), (sx, sy + 60), dim(SAND, 0.95), 3)
    c.polyline([(sx - 4, sy - 90), (sx, sy - 108), (sx + 4, sy - 90)],
               dim(SAND, 0.95), 2, closed=True, fill=dim(SAND, 0.7))
    c.line((sx - 26, sy + 22), (sx + 26, sy + 22), dim(SAND, 0.95), 3)
    c.line((sx, sy + 60), (sx, sy + 78), dim(SAND, 0.95), 5)
    c.text((sx, sy + 106), "THE SWORD", 13.5,
           HL if 1 <= v <= 4 else TEXT_DIM, "mm", bold=1 <= v <= 4)
    c.text((sx, sy + 126), "God's servant", 12, dim(TEXT_DIM, 0.95), "mm",
           italic=True)
    if v <= 7:
        c.text((sx, sy - 148), "APPOINTED BY GOD", 13.5,
               HL if v <= 2 else dim(TEXT, 0.8), "mm", bold=v <= 2)
        for k in range(5):
            a = math.pi * (0.2 + 0.6 * k / 4)
            c.line((sx + 40 * math.cos(a), sy - 116 - 16 * math.sin(a)),
                   (sx + 56 * math.cos(a), sy - 116 - 30 * math.sin(a)),
                   dim(GOLD, 0.5), 1.5)
        if v == 1:
            c.pulse_ellipse(sx, sy - 10, 52, 110, dim(HL, 0.7), width=1.8,
                            first=True)
    tr_on, tr_first = since(pos, 13, 6)
    if tr_on and v <= 8:
        c.circle(sx + 110, sy + 30, 20, stroke=GOLD, width=2)
        c.text((sx + 110, sy + 30), "T", 15, GOLD, "mm", bold=True)
        c.text((sx + 110, sy + 70), "TRIBUTE", 12.5,
               HL if 6 <= v <= 7 else TEXT_DIM, "mm", bold=6 <= v <= 7)
        if tr_first:
            c.pulse_ellipse(sx + 110, sy + 30, 26, 26, dim(HL, 0.85),
                            width=2, first=True)

    # centre: the commandments fold into LOVE (vv8-10)
    lo_on, lo_first = since(pos, 13, 8)
    if lo_on:
        lx, ly = 512, 240
        done = pos >= P(13, 10)
        for i, cmd in enumerate(COMMANDS13):
            a = math.pi / 4 + i * math.pi / 2
            ox = lx + 168 * math.cos(a)
            oy = ly + 66 * math.sin(a)
            colc = dim(SAND_DIM, 1.0) if done else dim(SAND, 0.9)
            c.rect(ox - 56, oy - 13, 112, 26, stroke=colc, width=1.5, rx=13)
            c.text((ox, oy), cmd, 11.5,
                   dim(TEXT_DIM, 0.9) if done else dim(TEXT, 0.9), "mm")
            c.line((ox + (lx - ox) * 0.35, oy + (ly - oy) * 0.35),
                   (ox + (lx - ox) * 0.72, oy + (ly - oy) * 0.72),
                   dim(GOLD, 0.55), 1.4)
        c.rect(lx - 62, ly - 21, 124, 42, stroke=GOLD, width=2.4, rx=21,
               fill=dim(GOLD, 0.14))
        c.text((lx, ly), "LOVE", 20, HL, "mm", bold=True)
        if lo_first or v == 10:
            c.pulse_rect(lx - 62, ly - 21, 124, 42, dim(HL, 0.9), width=2.2,
                         first=True, rx=21)
        if done:
            c.text((lx, ly + 104), "LOVE FULFILLS THE LAW",
                   14.5, HL, "mm", bold=v == 10)
        else:
            c.text((lx, ly + 116), "OWE NO ONE ANYTHING, BUT TO LOVE",
                   13.5, dim(TEXT, 0.9), "mm", italic=True)

    # right: the dawn (vv11-14)
    da_on, da_first = since(pos, 13, 11)
    if da_on:
        hx, hy = 800, 420
        prog = min(1.0, (v - 10) / 4)          # dawn rises v11 -> v14
        c.line((620, hy), (1000, hy), dim(SAND_DIM, 0.9), 1.5)
        # the sun's rim
        r = 60
        c.path(f"M{hx - r},{hy} A{r},{r} 0 0 1 {hx + r},{hy}",
               stroke=dim(GOLD, 0.35 + 0.6 * prog), width=2.6)
        for k in range(7):
            a = math.pi * (0.12 + 0.76 * k / 6)
            ln = 18 + 26 * prog
            c.line((hx + (r + 8) * math.cos(a), hy - (r + 8) * math.sin(a)),
                   (hx + (r + 8 + ln) * math.cos(a),
                    hy - (r + 8 + ln) * math.sin(a)),
                   dim(GOLD, 0.25 + 0.5 * prog), 1.6)
        c.text((hx, hy + 58), "THE DAY IS AT HAND", 13.5,
               HL if v >= 12 else TEXT_DIM, "mm", bold=v == 12)
        if da_first:
            c.pulse_ellipse(hx, hy - 20, r + 26, r * 0.8, dim(HL, 0.85),
                            width=2, first=True)
        # armour of light on a waking figure
        ar_on, ar_first = since(pos, 13, 12)
        if ar_on:
            fx2, fh2 = hx - 150, 86
            figure(c, fx2, hy, fh2, GOLD, 2.4, arms="open")
            # The breastplate is cut to the body it is worn on. Sized for the
            # stick figure it came off, it ran from the shoulders to below the
            # hip and out past the arms — a sandwich board rather than armour.
            def _bp(u, w):                 # local units up from the feet
                return fx2 + w * fh2 / MAN_UNITS, hy - u * fh2 / MAN_UNITS
            c.polyline([_bp(76, -11.2), _bp(80, 0), _bp(76, 11.2),
                        _bp(54, 9.6), _bp(47, 0), _bp(54, -9.6)],
                       dim(HL, 0.9), 1.8, closed=True)
            c.text((fx2, hy + 32), "ARMOUR OF LIGHT", 13, HL, "mm",
                   bold=12 <= v <= 14)
            if ar_first:
                c.pulse_ellipse(fx2, hy - 46, 40, 58, dim(HL, 0.9), width=2,
                                first=True)
    if pos >= P(13, 11) and v >= 11:
        phrase(c, (W / 2, 70), "THE NIGHT IS FAR GONE", 22, HL,
               first=v == 11)


# ---------------------------------------------------------------------------
# Chapter 14 — one table
# ---------------------------------------------------------------------------

# The company's board. Drawn at the scale its people are drawn at, so the top
# lands at the waist of the man standing behind it without the scene having to
# be told how tall a table is — which is the whole force of the shared unit.
# The span is chosen to reach across the company; the height follows from it.
T14_MAN = 152                            # the tallest men at the table
T14_SPAN = 3.10


def table14():
    """(parts, scale, height of the top above the floor). Everything the
    chapter puts on, beside or under the table measures from that height."""
    parts = F.table(span=T14_SPAN)
    s = units(T14_MAN)
    y0, y1 = F.bbox((parts, 0))[2:]
    return parts, s, (y1 - y0) * s


def draw_ch14_doxology(c, v, pos):
    """WEB Romans 14:24-26 — the doxology most versions print at 16:25-27.

    Drawn to rhyme with the chapter-16 treatment of the same three verses
    (a sealed mystery opened, then widening rings of glory), so a reader who
    meets this text at either place meets the same picture. The table of the
    chapter stays behind it, quiet.
    """
    fy = 452
    tx0, tx1 = 210, 810
    for fx, fh in ((330, 152), (480, 138), (570, 144), (690, 152)):
        figure(c, fx, fy, fh, dim(SAND_DIM, 0.9), 1.6)
    tbl, ts, th = table14()
    prop(c, tbl, (tx0 + tx1) / 2, fy, ts, dim(SAND_DIM, 1.0), 1.6)

    sx, sy = W / 2, 236
    revealed = pos >= P(14, 25)

    glory_on, glory_first = since(pos, 14, 26)
    if glory_on:
        for i, r in enumerate((130, 175, 215)):
            c.ellipse(sx, sy, r, r * 0.42, stroke=dim(GOLD, 0.44 - i * 0.12),
                      width=1.6)

    if not revealed:
        # the mystery, still sealed: a bound roll under a stamp
        c.rect(sx - 74, sy - 26, 148, 52, stroke=dim(SAND, 0.9), width=2,
               rx=8, fill=dim(PANEL, 0.9))
        c.line((sx, sy - 26), (sx, sy + 26), dim(SAND_DIM, 1.0), 1.6)
        c.circle(sx, sy, 13, fill=dim(RED, 0.5), stroke=dim(RED, 0.95),
                 width=2)
    else:
        c.rect(sx - 92, sy - 34, 184, 68, stroke=GOLD, width=2.2, rx=8,
               fill=dim(GOLD, 0.07))
        for r in range(4):
            c.line((sx - 66, sy - 18 + r * 12), (sx + 66, sy - 18 + r * 12),
                   dim(GOLD, 0.7), 1.5)
        for k in range(9):
            a = math.pi * (0.06 + 0.88 * k / 8)
            c.line((sx + 104 * math.cos(a), sy - 46 * math.sin(a)),
                   (sx + 134 * math.cos(a), sy - 74 * math.sin(a)),
                   dim(GOLD, 0.5), 1.6)
        if pos == P(14, 25):
            c.pulse_rect(sx - 98, sy - 40, 196, 80, dim(HL, 0.9), width=2.4,
                         first=True, rx=10)

    if v <= 25:
        c.text((sx, sy + 52),
               "kept secret through long ages" if not revealed
               else "made known to all the nations", 12,
               dim(TEXT_DIM, 0.95), "mm", italic=True)

    if v == 24:
        phrase(c, (sx, 96), "ABLE TO ESTABLISH YOU", 24, HL, first=True)
    elif v == 25:
        phrase(c, (sx, 96), "NOW REVEALED", 26, HL, first=True)
    else:
        phrase(c, (sx, 92), "TO THE ONLY WISE GOD", 24, HL, first=True)
        c.text((sx, 128), "BE GLORY FOREVER — AMEN", 17, HL, "mm", bold=True)


def draw_ch14(c, v, pos):
    if v >= 24:                    # the WEB's early doxology (see CH_LEN)
        draw_ch14_doxology(c, v, pos)
        return

    fy = 452                              # the floor
    tx0, tx1 = 210, 810
    wx, sx2 = 330, 690
    tbl, ts, th = table14()
    ty = fy - th                          # table top, at the company's waist

    # the company stands behind the table (drawn first, table in front)
    weak_lit = v in (1, 2, 3, 5, 13, 14, 15, 21)
    strong_lit = v in (1, 2, 3, 14, 15, 16, 20, 22)
    figure(c, wx, fy, 152,
           dim(SAND, 0.95) if weak_lit else dim(SAND_DIM, 1.0), 2)
    figure(c, 480, fy, 138, dim(SAND_DIM, 0.8), 1.8)
    figure(c, 570, fy, 144, dim(SAND_DIM, 0.8), 1.8)
    figure(c, sx2, fy, 152,
           dim(SAND, 0.95) if strong_lit else dim(SAND_DIM, 1.0), 2)

    # the one table, in front of them all
    prop(c, tbl, (tx0 + tx1) / 2, fy, ts, dim(SAND, 0.95), 2)
    # below the trestle feet, not among them
    c.text((wx, fy + 32), "WEAK IN FAITH", 12.5,
           HL if weak_lit else TEXT_DIM, "mm", bold=weak_lit and v <= 3)
    c.text((sx2, fy + 32), "STRONG", 12.5, HL if strong_lit else TEXT_DIM,
           "mm", bold=strong_lit and v <= 3)

    # Each one's plate, on the table beside him: herbs for the weak, the
    # whole board for the strong (14:2). The food is fitted to a plate rather
    # than drawn at the company's scale — `herb` is the growing plant, and a
    # sprig cut and served is not the size of the thing in the field.
    px14, qx14 = wx + 62, sx2 - 62
    c.ellipse(px14, ty - 7, 30, 8, stroke=dim(SAND, 0.9), width=1.6)
    hb = F.herb()
    for ox in (-11, 0, 11):
        prop(c, hb, px14 + ox, ty - 9, fit(hb, h=25), OLIVE, 1.5,
             flip=-1 if ox > 0 else 1)
    c.ellipse(qx14, ty - 7, 30, 8, stroke=dim(SAND, 0.9), width=1.6)
    br, cp = F.bread(), F.cup()
    prop(c, br, qx14 - 8, ty - 9, fit(br, w=30), dim(GOLD, 0.9), 1.6)
    prop(c, cp, qx14 + 19, ty - 9, fit(cp, h=22), dim(GOLD, 0.9), 1.6)
    rec_on, rec_first = since(pos, 14, 1)
    if rec_on and v <= 4:
        c.line((wx + 40, 236), (sx2 - 40, 236), dim(GOLD, 0.6),
               1.8, dash="6,6")
        c.text(((wx + sx2) / 2, 218), "RECEIVE ONE ANOTHER", 13.5,
               HL, "mm", bold=v == 1)

    # vv5-6: the days, esteemed alike, above the table
    day_on, day_first = since(pos, 14, 5)
    if day_on and v <= 9:
        for i, lbl in enumerate(("ONE DAY", "EVERY DAY")):
            dx3 = 430 + i * 160
            c.circle(dx3, 130, 24, stroke=dim(GOLD, 0.8), width=1.8)
            c.text((dx3, 130), lbl, 10.5, dim(TEXT, 0.9), "mm")
        c.text((510, 176), "TO THE LORD — ALIKE", 13,
               HL if 5 <= v <= 6 else TEXT_DIM, "mm", bold=5 <= v <= 6)
        if day_first:
            c.pulse_ellipse(510, 130, 116, 40, dim(HL, 0.8), width=1.8,
                            first=True)

    # vv10-12: the head of the table is the judgment seat
    js_on, js_first = since(pos, 14, 10)
    if js_on:
        # At the head of the table, the seat itself — the vocabulary's throne,
        # which is a raised seat with steps, since that is what makes a
        # throne and not a chair.
        jx = tx1 + 86
        thr = F.throne()
        jh = 150
        c.line((jx - 46, fy), (jx + 46, fy), dim(SAND_DIM, 0.9), 1.6)
        prop(c, thr, jx, fy, fit(thr, h=jh), GOLD, 2)
        for k in range(4):
            a = math.pi * (0.25 + 0.5 * k / 3)
            c.line((jx + 46 * math.cos(a), fy - jh - 8 - 10 * math.sin(a)),
                   (jx + 64 * math.cos(a), fy - jh - 8 - 28 * math.sin(a)),
                   dim(GOLD, 0.55), 1.5)
        c.text((jx, fy - jh - 54), "THE JUDGMENT SEAT", 12.5,
               HL if 10 <= v <= 12 else TEXT_DIM, "mm", bold=10 <= v <= 12)
        if js_first:
            c.pulse_rect(jx - 52, fy - jh - 8, 104, jh + 10, dim(HL, 0.9),
                         width=2, first=True, rx=7)
        if pos >= P(14, 11):
            phrase(c, (W / 2, 70), "EVERY KNEE WILL BOW", 22, HL,
                   first=v == 11)

    # v13: the stumbling block lifted from under the table
    sb_on, sb_first = since(pos, 14, 13)
    if sb_on:
        bx2, by2 = (wx + sx2) / 2, fy
        if v == 13:
            # A stone, not a red box. The verse is about what a foot finds in
            # the way, and a rough stone on the floor says that where a
            # rectangle only said something-is-wrong-here.
            st = F.stone()
            prop(c, st, bx2, by2, fit(st, w=52), dim(RED, 0.9), 2)
            c.polyline([(bx2, by2 - 44), (bx2, by2 - 74)], dim(GOLD, 0.9), 2)
            c.polyline([(bx2 - 7, by2 - 64), (bx2, by2 - 76),
                        (bx2 + 7, by2 - 64)], dim(GOLD, 0.9), 2)
            c.text((bx2 + 44, by2 - 14), "TAKEN AWAY", 12.5, HL, "lm",
                   bold=True)
        else:
            c.text((bx2, by2), "no stumbling block", 12,
                   dim(TEXT_DIM, 0.8), "mm", italic=True)

    # v17: what the kingdom is
    kg_on, kg_first = since(pos, 14, 17)
    if kg_on:
        words = ["RIGHTEOUSNESS", "PEACE", "JOY"]
        for i, wd in enumerate(words):
            wx2 = 512 + (i - 1) * 190
            c.rect(wx2 - 80, 96 - 17, 160, 34, stroke=dim(GOLD, 0.85),
                   width=1.8, rx=17, fill=dim(GOLD, 0.10))
            c.text((wx2, 96), wd, 14.5, HL, "mm", bold=v == 17)
        if kg_first:
            c.pulse_rect(512 - 290, 70, 580, 52, dim(HL, 0.85), width=2,
                         first=True, rx=26)
        c.text((512, 142), "THE KINGDOM OF GOD", 13, dim(TEXT, 0.85), "mm")
    do_on, do_first = since(pos, 14, 23)
    if do_on:
        c.text((W / 2, 218), "HE WHO DOUBTS IS CONDEMNED IF HE EATS",
               13.5, dim(RED, 0.95), "mm", bold=True)


# ---------------------------------------------------------------------------
# Chapter 15 — from Jerusalem round to Spain
# ---------------------------------------------------------------------------

CITIES15 = [("JERUSALEM", 880, 372), ("ILLYRICUM", 610, 230),
            ("ROME", 360, 252), ("SPAIN", 130, 310)]

# one westward sweep through the four cities, sampled as smooth arcs
_LEGS15 = []
for _a, _b in zip(CITIES15, CITIES15[1:]):
    (_, _x0, _y0), (_, _x1, _y1) = _a, _b
    _LEGS15.append([(_x0 + (_x1 - _x0) * t,
                     _y0 + (_y1 - _y0) * t - 44 * math.sin(math.pi * t))
                    for t in [i / 14 for i in range(15)]])


def draw_ch15(c, v, pos):
    # the sea beneath the journey
    c.path("M100,462 C300,438 520,452 720,458 C790,460 830,452 900,440",
           stroke=dim(WATER, 0.55), width=1.6)
    c.path("M180,486 C360,468 560,478 780,482",
           stroke=dim(WATER, 0.35), width=1.2)
    c.text((512, 508), "THE GREAT SEA", 12, dim(WATER, 0.8), "mm",
           italic=True)

    pts = {name: (x, y) for name, x, y in CITIES15}
    # the sweep so far: Jerusalem -> Illyricum (v19), gold and solid
    sw_on, sw_first = since(pos, 15, 19)
    if sw_on:
        if sw_first:
            c.traced(_LEGS15[0], GOLD, 2.6, dur="2.2s")
        else:
            c.polyline(_LEGS15[0], GOLD, 2.6)
        c.text((790, 246), "FULLY PREACHED", 12.5,
               HL if v == 19 else TEXT_DIM, "mm")
    # the plan: on to Rome (v23), and past it to Spain (v24)
    ro_on, ro_first = since(pos, 15, 23)
    if ro_on:
        c.polyline(_LEGS15[1], dim(GOLD, 0.75), 2, dash="6,7")
        sp_on, sp_first = since(pos, 15, 24)
        if sp_on:
            c.polyline(_LEGS15[2], dim(GOLD, 0.55), 2, dash="3,7")
            if sp_first:
                c.pulse_ellipse(*pts["SPAIN"], 30, 20, dim(HL, 0.85),
                                width=2, first=True)
    # but first: the collection carried back to Jerusalem (vv25-28)
    col_on, col_first = since(pos, 15, 25)
    if col_on and v <= 28:
        bx, by = 740, 322
        c.circle(bx, by, 10, stroke=GOLD, width=2)
        c.line((bx - 6, by - 8), (bx + 6, by - 8), GOLD, 2)
        c.polyline([(bx + 16, by), (820, 342), (858, 360)],
                   dim(GOLD, 0.6), 1.6, dash="4,5")
        c.polyline([(846, 350), (860, 361), (844, 366)], dim(GOLD, 0.8),
                   1.6)
        c.text((700, 356), "THE CONTRIBUTION", 12.5,
               HL if 25 <= v <= 27 else TEXT_DIM, "mm",
               bold=25 <= v <= 27)
        c.text((700, 374), "for the saints at Jerusalem", 11,
               dim(TEXT_DIM, 0.95), "mm", italic=True)
    for name, x, y in CITIES15:
        state = {"JERUSALEM": pos >= P(15, 19), "ILLYRICUM": pos >= P(15, 19),
                 "ROME": pos >= P(15, 23), "SPAIN": pos >= P(15, 24)}[name]
        lit = (name == "SPAIN" and v == 24) or (name == "ROME" and
                                                v in (23, 29, 32))
        c.circle(x, y, 6 if state else 4,
                 fill=HL if lit else (dim(GOLD, 0.85) if state else None),
                 stroke=None if state else dim(SAND_DIM, 1.0),
                 width=1.6)
        ly15 = y + 26 if name == "JERUSALEM" else y - 20
        c.text((x, ly15), name, 13.5, HL if lit else
               (TEXT if state else TEXT_DIM), "mm", bold=lit or state)
        if lit:
            c.pulse_ellipse(x, y, 15, 15, dim(HL, 0.9), width=2, first=True)

    # vv1-13: the one-mouth doxology over the map
    if v <= 13:
        if v <= 7:
            phrase(c, (W / 2, 76), "BEAR — PLEASE YOUR NEIGHBOR — RECEIVE",
                   18, HL if v in (1, 2, 7) else dim(TEXT, 0.85),
                   first=v == 1)
        # vv3-6: what was written, and the one mouth it produces
        wr_on, wr_first = since(pos, 15, 4)
        if wr_on and v <= 8:
            c.rect(150, 130, 96, 58, stroke=dim(GOLD, 0.9), width=1.8, rx=6)
            for r in range(3):
                c.line((168, 148 + r * 13), (228, 148 + r * 13),
                       dim(GOLD, 0.7), 1.5)
            c.text((198, 204), "WRITTEN FOR OUR LEARNING", 11.5,
                   HL if v == 4 else dim(TEXT_DIM, 0.95), "mm", bold=v == 4)
            if wr_first:
                c.pulse_rect(146, 126, 104, 66, dim(HL, 0.85), width=1.8,
                             first=True, rx=8)
        om_on, om_first = since(pos, 15, 5)
        if om_on and v <= 8:
            n_m = 2 if pos < P(15, 6) else 5
            for i in range(n_m):
                fx4 = 320 + i * 34
                figure(c, fx4, 196, 54,
                       dim(SAND, 0.95) if pos >= P(15, 6) else
                       dim(SAND_DIM, 1.0), 1.6)
            if pos >= P(15, 6):
                c.polyline([(310, 150), (320, 138), (438, 138), (448, 150)],
                           dim(GOLD, 0.8), 1.8)
                c.text((379, 122), "WITH ONE MOUTH", 12, HL, "mm",
                       bold=v == 6)
            if om_first or pos == P(15, 6):
                c.pulse_ellipse(379, 172, 90, 46, dim(HL, 0.8), width=1.8,
                                first=True)
        vo_on, vo_first = since(pos, 15, 9)
        if vo_on:
            # four voices of the nations rise (the four OT quotes, vv9-12)
            for i in range(min(4, v - 8)):
                qx = 380 + i * 90
                c.polyline([(qx, 160), (qx, 128)], dim(GOLD, 0.8), 2)
                c.polyline([(qx - 6, 138), (qx, 126), (qx + 6, 138)],
                           dim(GOLD, 0.8), 2)
            c.text((515, 108), "LET ALL THE PEOPLES PRAISE HIM", 14.5,
                   HL if 9 <= v <= 12 else dim(TEXT, 0.85), "mm",
                   bold=9 <= v <= 12)
        if v == 13:
            phrase(c, (W / 2, 76), "THE GOD OF HOPE FILL YOU WITH JOY",
                   19, HL, first=True)
    elif v == 20:
        c.text((W / 2, 96), "NOT ON ANOTHER'S FOUNDATION", 16, HL, "mm",
               bold=True)
    elif v >= 30:
        phrase(c, (W / 2, 76), "STRIVE TOGETHER WITH ME IN PRAYER", 18,
               HL if v == 30 else dim(TEXT, 0.85), first=v == 30)

    # vv16-18: the offering of the nations — a censer lit per verse
    off_on, off_first = since(pos, 15, 16)
    if off_on and v <= 18:
        c.rect(430, 150, 120, 24, stroke=dim(SAND, 0.95), width=2)
        c.rect(444, 136, 92, 14, stroke=dim(SAND, 0.9), width=1.6)
        for i, fx5 in enumerate((464, 490, 516)):
            if pos < P(15, 16 + i):
                continue
            c.path(f"M{fx5},{136} Q{fx5 - 7},{118} {fx5 + 3},{104}",
                   stroke=dim(GOLD, 0.75), width=1.8)
        c.text((490, 194), "THE OFFERING OF THE NATIONS", 12,
               HL if v == 16 else dim(TEXT_DIM, 0.95), "mm", bold=v == 16)
        if off_first:
            c.pulse_rect(426, 132, 128, 46, dim(HL, 0.85), width=1.8,
                         first=True, rx=5)


# ---------------------------------------------------------------------------
# Chapter 16 — the lamps of Rome
# ---------------------------------------------------------------------------

# houses of the church in Rome: (x, y, w) — a scattered cluster
HOUSES16 = [(300, 250, 74), (420, 200, 64), (540, 250, 80), (660, 195, 62),
            (780, 245, 72), (360, 350, 66), (500, 360, 70), (640, 350, 64),
            (770, 350, 60), (880, 290, 56)]
# greeting verse -> houses lit (index into HOUSES16), cumulative
LAMP_AT = {3: [0], 5: [1], 6: [2], 7: [3], 8: [4], 9: [5], 10: [6],
           11: [7], 12: [8], 13: [9], 14: [5, 6], 15: [7, 8],
           21: [1, 2], 22: [3], 23: [4, 9]}


def _house(c, x, y, w2, col, width=1.8):
    """One household of the greeting list. Signature unchanged: `w2` is still
    the width the plan lays the street out on."""
    hs = F.house()
    prop(c, hs, x, y, fit(hs, w=w2), col, width)


def draw_ch16(c, v, pos):
    lit_idx = set()
    fresh_idx = set()
    for gv, idxs in LAMP_AT.items():
        if v >= gv:
            lit_idx.update(idxs)
        if v == gv:
            fresh_idx.update(idxs)

    for i, (x, y, w2) in enumerate(HOUSES16):
        on = i in lit_idx
        col = dim(GOLD, 0.9) if on else dim(SAND_DIM, 1.0)
        _house(c, x, y, w2, col, 2 if on else 1.6)
        if on:
            # the lamp in the window: a warm dot in a soft glow
            c.circle(x, y - w2 * 0.3, 4.5, fill=dim(HL, 0.95))
            c.circle(x, y - w2 * 0.3, 9.5, stroke=dim(GOLD, 0.45),
                     width=1.4)
        if i in fresh_idx:
            c.pulse_ellipse(x, y - w2 * 0.3, 17, 17, dim(HL, 0.9),
                            width=2, first=True)
    c.text((590, 130), "THE CHURCH AT ROME", 14,
           dim(TEXT, 0.9), "mm", italic=True)

    # Phoebe arrives with the letter (vv1-2)
    ph_on, ph_first = since(pos, 16, 1)
    if ph_on and v <= 2:
        px, py = 150, 430
        figure(c, px, py, 78, GOLD, 2.2, legs="walk", kind="woman")
        c.rect(px + 22, py - 66, 26, 18, stroke=GOLD, width=1.8, rx=2)
        c.polyline([(px + 22, py - 66), (px + 35, py - 56), (px + 48, py - 66)],
                   GOLD, 1.6)
        c.text((px, py + 24), "PHOEBE", 14, HL, "mm", bold=True)
        c.text((px, py + 44), "servant of the church, bearer of the letter",
               11.5, dim(TEXT_DIM, 0.95), "mm", italic=True)
        if ph_first:
            c.pulse_ellipse(px, py - 40, 40, 56, dim(HL, 0.9), width=2,
                            first=True)
        c.polyline([(px + 60, py - 20), (240, 340)], dim(GOLD, 0.5), 1.6,
                   dash="4,6")
    pr_on, _ = since(pos, 16, 3)
    if pr_on and v <= 5:
        c.text((300, 300), "PRISCILLA & AQUILA", 12.5,
               HL if 3 <= v <= 4 else TEXT_DIM, "mm", bold=3 <= v <= 4)
        if pos >= P(16, 4):
            c.text((300, 318), "who risked their necks", 11,
                   dim(TEXT_DIM, 0.95), "mm", italic=True)
    if 6 <= v <= 16 or 21 <= v <= 23:
        c.text((512, 470), "GREET — GREET — GREET", 14,
               dim(TEXT, 0.7), "mm", italic=True)

    # v17: the crooked path avoided
    div_on, div_first = since(pos, 16, 17)
    if div_on and v <= 19:
        c.polyline([(870, 430), (900, 410), (886, 390), (920, 372),
                    (904, 352)], dim(RED, 0.8), 2, dash="5,5")
        c.line((858, 442), (884, 416), dim(RED, 0.9), 2.2)
        c.line((858, 416), (884, 442), dim(RED, 0.9), 2.2)
        c.text((880, 466), "AVOID DIVISIONS", 12,
               dim(RED, 0.95), "mm", bold=v == 17)
        if div_first:
            c.pulse_ellipse(890, 400, 44, 56, dim(RED, 0.8), width=1.8,
                            first=True)
    # v20: Satan under foot
    sa_on, sa_first = since(pos, 16, 20)
    if sa_on and v <= 24:
        fx3, fy3 = 200, 430
        c.path(f"M{fx3 - 30},{fy3 + 14} Q{fx3 - 10},{fy3 + 4} {fx3},{fy3 + 12} "
               f"Q{fx3 + 12},{fy3 + 20} {fx3 + 26},{fy3 + 10}",
               stroke=dim(RED, 0.8), width=2)
        c.line((fx3 - 8, fy3 + 2), (fx3 + 10, fy3 + 2), dim(SAND, 0.95), 4,
               linecap="round")
        c.line((fx3 + 10, fy3 + 2), (fx3 + 16, fy3 - 8), dim(SAND, 0.95), 3)
        c.text((fx3, fy3 + 40), "SATAN CRUSHED UNDERFOOT", 12,
               HL if v == 20 else TEXT_DIM, "mm", bold=v == 20)


# ---------------------------------------------------------------------------
# Assemble one verse
# ---------------------------------------------------------------------------

SCENES = {1: draw_ch1, 2: draw_ch2, 3: draw_ch3, 4: draw_ch4, 5: draw_ch5,
          6: draw_ch6, 7: draw_ch7, 8: draw_ch8, 9: draw_ch9, 10: draw_ch10,
          11: draw_ch11, 12: draw_ch12, 13: draw_ch13, 14: draw_ch14,
          15: draw_ch15, 16: draw_ch16}


def render(ch, v):
    c = SvgCanvas(W, H, bg=BG)
    header(c, ch, v)
    SCENES[ch](c, v, P(ch, v))
    return c


def main():
    total = count = 0
    for ch in range(1, 17):
        for v in verse_numbers(BOOK, ch):
            out = out_path(BOOK, ch, f"{BOOK}_{ch}_{v}.svg")
            render(ch, v).save(out)
            total += os.path.getsize(out)
            count += 1
    print(f"Romans: {count} SVG files, {total / 1e3:.0f} KB")


if __name__ == "__main__":
    main()
