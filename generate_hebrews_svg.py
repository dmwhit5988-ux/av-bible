"""Render the epistle to the Hebrews (13 chapters, 303 verses) as per-verse
vector SVGs. Design and reasoning: docs/design/hebrews.md.

THE FRAME. One vertical section, drawn twice. The heavenly sanctuary stands
solid at the top with the throne in it; the earthly sanctuary hangs below as
the shadow that throne's light casts — 8:5 "a copy and shadow of the heavenly
things", 9:24 "representations of the true", 10:1 "a shadow of the good to
come, not the very image". 8:5's "pattern that was shown to you on the
mountain" is drawn as the projection lines between the two, so the frame
justifies itself on screen the moment the text names it.

The whole column is 0-1000 in its own units and no verse sees all of it. Each
chapter sets a viewport (`VIEWS`) and the drawing is that slice, enlarged; a
gauge down the left margin says where in the column the slice sits. That is
the entire progress indicator — no bead track, no per-verse caption word, no
verse counter. The Romans post-mortem is the reason: what moved there only
ever said "verse 23 of 31".

What the frame buys, in the order it pays out:

    2:9   the only descent below the camp before chapter 13, rehearsing it
    6:19  the veil is punctured at exactly one point, by an anchor's line
    8:5   the doubling is named, so the frame explains itself
    8:13  "near to vanishing away" — the shadow's edges first fade
    10:20 the puncture of 6:19 opens into a way
    12:27 "the removing of those things that are shaken" — the shadow layer
          is shaken off and gone. The frame resolves in one verse.
    13:13 the camera drops below the camp, because the altar moved

THREE BREAK-AWAYS, each because the text turns and the column cannot follow:
chapter 7 is the Melchizedek genealogy (a chart, not a section); chapters 11
and 12 leave for a ground plane, where the pilgrims walk toward a city that
is the top of this same column seen from outside — which is why 12:2's
"looking to Jesus ... has sat down" can fuse the two geometries in one verse,
landing the road's sightline on the seat drawn at 1:3.

THREADS.
  voice     Hebrews quotes the Old Testament some thirty-five times and
            almost never says "it is written" — it says "he says", "the Holy
            Spirit says". Every quotation is an arc from a speaker above the
            frame. 1:1's "many times and in various ways" is many short
            fragmentary arcs collapsing at 1:2 into one; 5:11's "dull of
            hearing" greys out at the ear; 11:4's Abel rises from a grave and
            12:24's better-speaking blood answers it thirteen chapters later.
  warnings  Five, and at each the floor gives way in its own manner: a
            current that carries sideways (2:1), a path that loops and never
            arrives (3:7-4:13), a field burned to the root (6:8), a floor
            opened over fire (10:26-31), a shaking that takes everything not
            fastened (12:25-29).
  BETTER    The eleven verses that carry the word - 1:4, 6:9, 7:19, 7:22,
            8:6, 9:23, 10:34, 11:16, 11:35, 11:40, 12:24 - cut it small into
            the substance side.
  the seat  1:3, 8:1, 10:12, 12:2. Drawn at 1:3 and never altered for the
            remaining 300 verses, which is what makes 13:8 land. There is no
            seat anywhere in the lower structure, so the standing priests of
            10:11 have nowhere to sit long before the text says so — the
            omission Exodus 28's vested figure already established.

TEXT BUDGET. Hebrews argues, so a wordless canvas fights it. Same allowance
as Romans: short engraved phrases, 2-7 words, ALL-CAPS, at hinge verses only
(`ENGRAVED`) — twenty-two across 303 verses. Never sentences, never captions,
never per-verse prose.

TEXT. WEB is the only text (passages.TRANSLATION), and CH_LEN is WEB's
verse count for every chapter.

Run inside the project venv:
    .venv\\Scripts\\python.exe generate_hebrews_svg.py
"""

import math
import os

import svg_figures as F
import svg_priest as G
from svg_surface import SvgCanvas
from svg_vocab import dim, mix, text_w, reading_position, arrow, cross, hatch
from passages import verse_numbers
from generate_tabernacle import (W, H, BG, PANEL, SAND, SAND_DIM, TEXT,
                                 TEXT_DIM, HL, GOLD, RED, BROWN, GRAY,
                                 SILVER, WHITE_LINEN, GATE_COLORS, out_path)

BOOK = "Hebrews"
SLUG = "Hebrews"

CH_LEN = {1: 14, 2: 18, 3: 19, 4: 16, 5: 14, 6: 20, 7: 28, 8: 13, 9: 28,
          10: 39, 11: 40, 12: 29, 13: 25}
P, since = reading_position(CH_LEN)

BLUE, PURPLE, SCARLET, LINEN = GATE_COLORS

# The shadow key. Flat, cool and low-contrast on purpose: it is a cast
# shadow, so it has no light of its own and no interior detail the substance
# above has not already given it.
SHADOW = (66, 72, 88)
SHADOW_LIT = (96, 104, 124)
SHADOW_DIM = (44, 48, 60)

FIRE = (216, 124, 58)           # 12:18 on the one mountain, 12:29 on the other
BLOOD = (168, 62, 58)
CITY = (226, 198, 130)          # 11:10, 11:16, 12:22, 13:14
DEEP = (14, 14, 20)             # below the camp — outside the gate


# ---------------------------------------------------------------------------
# The column
# ---------------------------------------------------------------------------
#
# One coordinate system for the whole book, 0 at the bottom of the frame and
# 1000 at the top of it. Every chapter names a slice of it.

U_OUT = 60          # outside the gate — 13:12-13
U_CAMP = 150        # the camp
U_COURT = 250       # the court, and the altar
U_HOLY = 390        # the holy place: lampstand, table, show bread
U_VEIL = 480        # the veil
U_MOST = 545        # the holy of holies, the ark, the mercy seat
U_TOP = 620         # the top of the earthly structure
U_HEAVENS = 706     # "passed through the heavens" — 4:14
U_TRUE = 800        # the true tabernacle, which the Lord pitched, not man
U_SEAT = 900        # the throne, and the seat

STATIONS = [(U_OUT, "OUTSIDE"), (U_CAMP, "CAMP"), (U_COURT, "COURT"),
            (U_HOLY, "HOLY PLACE"), (U_VEIL, "VEIL"), (U_MOST, "MOST HOLY"),
            (U_HEAVENS, "THE HEAVENS"), (U_TRUE, "TRUE TENT"),
            (U_SEAT, "THE THRONE")]

# Half-widths of the shadow structure, in canvas pixels at full zoom.
HW_CAMP, HW_COURT, HW_HOLY, HW_MOST = 386, 292, 196, 128
HW_TRUE, HW_SEAT = 214, 96

CX = 552                        # the column's centre line
SX0, SX1 = 104, 1000            # the stage
SYT, SYB = 92, 540
GX = 52                         # the altitude gauge


class Cam:
    """A viewport on the column: `lo`..`hi` in column units, filling the
    stage. Everything a scene draws goes through it, so a chapter changes
    what is on screen by changing where it is looking rather than by
    redrawing the world at a new size."""

    def __init__(self, lo, hi):
        self.lo, self.hi = float(lo), float(hi)

    def y(self, u):
        t = (u - self.lo) / (self.hi - self.lo)
        return SYB - t * (SYB - SYT)

    def s(self, du):
        """A length in column units, in canvas pixels."""
        return abs(du) * (SYB - SYT) / (self.hi - self.lo)

    def k(self):
        """How much the column is magnified — 1.0 at full zoom-out."""
        return 1000.0 * (SYB - SYT) / ((self.hi - self.lo) * (SYB - SYT)) \
            * (self.hi - self.lo) / (self.hi - self.lo)

    def w(self, hw):
        """A half-width, shrunk with the zoom so the structure keeps its
        proportions when the camera comes in close."""
        return hw * min(1.35, (1000.0 / (self.hi - self.lo)) ** 0.42)


# Chapter viewports. Chapter 7, 11 and 12 break away and set their own.
VIEWS = {1: (600, 1000), 2: (40, 1000), 3: (120, 700), 4: (120, 990),
         5: (230, 940), 6: (230, 940), 7: None, 8: (330, 1000),
         9: (110, 660), 10: (200, 950), 11: None, 12: None,
         13: (0, 660)}

# One chapter changes viewport partway through. 13:8 letters "the same
# yesterday, today, and forever" beside the seat, which the low viewport of
# the second half does not contain — so the chapter opens wide on the whole
# column and then drops, which is also what it says it is doing.
VIEW_BY_VERSE = {13: lambda v: (0, 1000) if v <= 8 else (0, 660)}


# ---------------------------------------------------------------------------
# Page furniture
# ---------------------------------------------------------------------------


def header(c, ch, v):
    c.text((28, 24), f"Hebrews {ch}", 23, TEXT, "la", bold=True)
    c.text((28, 54), f"v{v}", 13, dim(TEXT_DIM, 0.85), "la", italic=True)


ENGRAVED = {
    (2, 9): "BUT WE SEE HIM", (3, 7): "TODAY, IF YOU WILL HEAR HIS VOICE",
    (4, 9): "A SABBATH REST REMAINS", (4, 12): "LIVING AND ACTIVE",
    (4, 16): "LET US DRAW NEAR WITH BOLDNESS", (5, 6): "A PRIEST FOREVER",
    (6, 19): "SURE AND STEADFAST", (7, 25): "TO THE UTTERMOST",
    (8, 5): "A COPY AND SHADOW", (8, 12): "I WILL REMEMBER THEIR SINS NO MORE",
    (9, 12): "ONCE FOR ALL", (10, 12): "HE SAT DOWN",
    (10, 20): "A NEW AND LIVING WAY", (10, 31): "THE HANDS OF THE LIVING GOD",
    (11, 10): "THE CITY WHICH HAS THE FOUNDATIONS",
    (11, 16): "A BETTER COUNTRY", (11, 38): "OF WHOM THE WORLD WAS NOT WORTHY",
    (12, 1): "THE RACE SET BEFORE US", (12, 2): "LOOKING TO JESUS",
    (12, 28): "A KINGDOM THAT CANNOT BE SHAKEN",
    (13, 8): "THE SAME YESTERDAY, TODAY, AND FOREVER",
    (13, 14): "NO ENDURING CITY HERE"}


def phrase(c, xy, s, size=21, col=None, first=False):
    """A hinge-verse phrase: caps, bold, ringed once on the verse it lands.
    The ring is measured off the real advance width, never estimated — a
    characters-times-a-guess box is what cropped the first Romans cut."""
    col = col or HL
    c.text(xy, s, size, col, "mm", bold=True)
    if first:
        w = text_w(s, size, bold=True) + size * 1.25
        h = size * 1.75
        c.pulse_rect(xy[0] - w / 2, xy[1] - h / 2, w, h, dim(col, 0.75),
                     width=1.7, first=True, rx=h / 2)


def engrave(c, ch, at, v, xy, size=21, col=None):
    """The engraved phrase for verse `at`, drawn only on the verse it lands.

    A hinge phrase is a moment, not furniture: left standing it accumulates,
    and chapter 11 ended up with three ringed phrases and a weighing scale in
    one frame. `at` is the verse it belongs to and `v` is the verse being
    drawn, so it rings once and is gone.
    """
    if v != at:
        return
    txt = ENGRAVED.get((ch, at))
    if txt:
        phrase(c, xy, txt, size, col, first=True)


# The eleven verses that carry the word.
BETTER = [(1, 4), (6, 9), (7, 19), (7, 22), (8, 6), (9, 23), (10, 34),
          (11, 16), (11, 35), (11, 40), (12, 24)]


def better_mark(c, pos, xy=None, size=13):
    """BETTER, cut small into the substance side on each of its eleven
    verses. A content thread, not a tally: eleven marks in 303 verses."""
    hit = [p for p in BETTER if P(*p) == pos]
    if not hit:
        return
    x, y = xy or (SX1 - 40, SYT + 16)
    c.text((x, y), "BETTER", size, HL, "rm", bold=True)
    w = text_w("BETTER", size, bold=True)
    c.line((x - w - 6, y + size * 0.62), (x + 2, y + size * 0.62),
           dim(HL, 0.8), 1.6)


def gauge(c, cam, mark=None, off=False, label=None):
    """The altitude gauge: the whole column as a strip, with the slice the
    camera is looking at bracketed on it. Thirty pixels wide, and the only
    thing on the page that tracks position."""
    top, bot = SYT, SYB
    c.line((GX, top), (GX, bot), dim(SAND_DIM, 0.85), 1.4)
    for u, name in STATIONS:
        gy = bot - (u / 1000.0) * (bot - top)
        c.line((GX - 5, gy), (GX + 5, gy), dim(SAND_DIM, 0.9), 1.2)
    if off:
        c.text((GX, top - 16), "OFF", 9, dim(TEXT_DIM, 0.9), "mm",
               italic=True)
        if label:
            c.text((GX, bot + 18), label, 8.5, dim(TEXT_DIM, 0.9), "mm",
                   italic=True)
        return
    y0 = bot - (cam.hi / 1000.0) * (bot - top)
    y1 = bot - (cam.lo / 1000.0) * (bot - top)
    c.rect(GX - 8, y0, 16, y1 - y0, fill=None, stroke=dim(HL, 0.85),
           width=1.6, rx=3)
    if mark is not None:
        my = bot - (mark / 1000.0) * (bot - top)
        c.circle(GX, my, 4.2, fill=HL)


# ---------------------------------------------------------------------------
# The two halves of the frame
# ---------------------------------------------------------------------------


def substance(c, cam, seat=False, tent=True, light=False, glow=1.0):
    """The heavenly side: the true tabernacle and the throne, solid, lit,
    and the source of the light that casts everything below."""
    if tent:
        w = cam.w(HW_TRUE)
        yt, yb = cam.y(U_TRUE + 56), cam.y(U_HEAVENS)
        c.polygon([(CX - w, yb), (CX + w, yb), (CX + w * 0.74, yt),
                   (CX - w * 0.74, yt)],
                  fill=dim(BROWN, 0.30 * glow), stroke=dim(GOLD, 0.90 * glow),
                  width=2.0)
        for i in (-0.42, 0.0, 0.42):
            c.line((CX + w * i * 0.86, yt + 2), (CX + w * i, yb - 2),
                   dim(GOLD, 0.40 * glow), 1.2)
    if seat:
        throne(c, cam, glow=glow)
    if light:
        # 8:5 — "according to the pattern that was shown to you on the
        # mountain", drawn as the projection that makes a shadow.
        for sx in (-1, 1):
            c.line((CX + sx * cam.w(HW_TRUE), cam.y(U_HEAVENS)),
                   (CX + sx * cam.w(HW_CAMP), cam.y(U_CAMP)),
                   dim(GOLD, 0.32), 1.2, dash="7,7")


def throne(c, cam, glow=1.0, occupied=True):
    """The seat. Drawn at 1:3 and never altered again — which is the whole
    of what 13:8 has to say, and it can only be said by a book drawn a verse
    at a time."""
    w = cam.w(HW_SEAT)
    y_seat = cam.y(U_SEAT)              # the seat itself
    y_foot = cam.y(U_SEAT - 34)         # where it stands
    y_back = cam.y(U_SEAT + 74)         # the top of the back
    ink = dim(GOLD, 0.95 * glow)
    # The back first, so the seat laps over it.
    c.polygon([(CX - w * 0.80, y_seat), (CX + w * 0.80, y_seat),
               (CX + w * 0.66, y_back), (CX - w * 0.66, y_back)],
              fill=dim(GOLD, 0.16 * glow), stroke=ink, width=2.0)
    # The seat: the one horizontal in the whole frame that is sat on, and
    # the only seat anywhere in this book. Nothing below the veil has one.
    c.polygon([(CX - w, y_seat), (CX + w, y_seat),
               (CX + w, y_seat + (y_foot - y_seat) * 0.34),
               (CX - w, y_seat + (y_foot - y_seat) * 0.34)],
              fill=dim(GOLD, 0.42 * glow), stroke=ink, width=2.2)
    for sx in (-1, 1):                  # the legs
        c.line((CX + sx * w * 0.84, y_seat + (y_foot - y_seat) * 0.34),
               (CX + sx * w * 0.78, y_foot), ink, 2.0)
    for sx in (-1, 1):                  # arms
        c.line((CX + sx * w, y_seat), (CX + sx * w * 0.94, y_seat - 8),
               ink, 1.6)
    if occupied:
        for i in range(11):
            a = -math.pi / 2 + (i - 5) * 0.26
            r0, r1 = 30, 30 + 52
            c.line((CX + math.cos(a) * r0, y_back + math.sin(a) * r0),
                   (CX + math.cos(a) * r1, y_back + math.sin(a) * r1),
                   dim(HL, 0.26 * glow), 1.4)


def shadow(c, cam, fade=1.0, upto=U_TOP, veil=True, pierced=False,
           opened=False, labels=False):
    """The earthly side, drawn as what it is called: a cast shadow. Flat,
    edgeless, cool, and carrying no detail of its own.

    `fade` dims the whole layer — 8:13's "becoming old ... near to vanishing
    away" starts it, and 12:27 finishes it by not calling this at all.
    """
    if fade <= 0:
        return
    a = fade
    body = dim(SHADOW, 0.62 * a)
    edge = dim(SHADOW_LIT, 0.75 * a)

    # Drawn as a building in section with floors, not as nested enclosures
    # stacked. Stacking widths would put a stepped pyramid on the page, and a
    # ziggurat is the one thing this sanctuary must not look like — Genesis 11
    # already owns that silhouette in this canon.
    hw_house = cam.w(HW_HOLY)
    if upto >= U_CAMP:                                   # the camp: a plinth
        y0, y1 = cam.y(U_CAMP), cam.y(U_COURT)
        w = cam.w(HW_CAMP)
        c.polygon([(CX - w, y0), (CX + w, y0), (CX + w, y1), (CX - w, y1)],
                  fill=dim(SHADOW, 0.44 * a), stroke=edge, width=1.4)
    if upto >= U_COURT:                                  # the court wall
        y0, y1 = cam.y(U_COURT), cam.y(U_HOLY)
        w = cam.w(HW_COURT)
        c.polygon([(CX - w, y0), (CX + w, y0), (CX + w, y1), (CX - w, y1)],
                  fill=dim(SHADOW, 0.52 * a), stroke=edge, width=1.4)
    if upto >= U_HOLY:                                   # the house itself
        y0 = cam.y(U_HOLY)
        y1 = cam.y(min(upto, U_TOP))
        c.polygon([(CX - hw_house, y0), (CX + hw_house, y0),
                   (CX + hw_house, y1), (CX - hw_house, y1)],
                  fill=body, stroke=edge, width=1.6)
        if upto >= U_TOP:                                # and its roof
            yt = cam.y(U_TOP + 42)
            c.polygon([(CX - hw_house, y1), (CX, yt), (CX + hw_house, y1)],
                      fill=dim(SHADOW, 0.70 * a), stroke=edge, width=1.6)
        if upto >= U_MOST:
            c.line((CX - hw_house, cam.y(U_MOST)),
                   (CX + hw_house, cam.y(U_MOST)), dim(SHADOW_LIT, 0.55 * a),
                   1.2)
    if upto >= U_VEIL and veil:
        y = cam.y(U_VEIL)
        w = cam.w(HW_HOLY * 0.96)
        if opened:
            # 10:20 — the puncture of 6:19 opened into a way.
            c.line((CX - w, y), (CX - cam.w(26), y), dim(HL, 0.9), 3.4)
            c.line((CX + cam.w(26), y), (CX + w, y), dim(HL, 0.9), 3.4)
        else:
            c.line((CX - w, y), (CX + w, y), dim(SILVER, 0.85 * a), 3.4)
            if pierced:
                c.circle(CX, y, 4.6, fill=None, stroke=HL, width=2.0)
    if labels:
        for u, name in ((U_CAMP + 46, "THE CAMP"), (U_COURT + 60, "THE COURT"),
                        (U_HOLY + 42, "THE HOLY PLACE"),
                        (U_VEIL + 30, "THE MOST HOLY")):
            gy = cam.y(u)
            if not (SYT + 8 <= gy <= SYB - 8):
                continue             # that station is outside this viewport
            c.text((CX, gy), name, 10, dim(SHADOW_LIT, 0.95 * a), "mm",
                   bold=True)


def ground(c, cam, u=U_CAMP, col=None, dash=None):
    """A line across the frame at a column height — the camp line, the
    angel rank line of 1:4, the horizon of a break-away."""
    y = cam.y(u)
    c.line((SX0, y), (SX1, y), col or dim(SAND_DIM, 0.9), 1.4, dash=dash)
    return y


# ---------------------------------------------------------------------------
# Marks the threads are made of
# ---------------------------------------------------------------------------


def voice_arc(c, p0, p1, col=None, width=1.8, dash=None, bulge=0.34,
              speaker=True, refused=False):
    """A quotation: an arc from a speaker to a hearer. Hebrews says "he
    says", never "it is written", so the arc starts at a mouth and not at a
    scroll, and it starts above."""
    col = col or dim(HL, 0.85)
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    d = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
    cy = my - d * bulge
    if refused:
        # 12:25 — "see that you don't refuse him who speaks".
        cy = my + d * bulge * 0.5
    c.path(f"M{p0[0]},{p0[1]} Q{mx},{cy} {p1[0]},{p1[1]}",
           fill=None, stroke=col, width=width)
    if speaker:
        c.circle(p0[0], p0[1], 4.0, fill=col)
    if refused:
        cross(c, p1[0], p1[1], 7, dim(RED, 0.95), 2.2)


def figure(c, x, gy, h, col, kind="man", width=1.9, arms="down", pose="stand"):
    """A person, from the shared vocabulary."""
    parts = {"priest": F.priest, "woman": F.woman,
             "child": F.child, "king": F.king}.get(kind, F.man)
    parts = parts(pose=pose, arms=arms) if kind != "man" else \
        F.man(pose=pose, arms=arms)
    F.draw(c, parts, x, gy, h / MAN_UNITS, col, BG, style=_paint(col, width))


MAN_UNITS = F.bbox((F.man(), 0))[3] - F.bbox((F.man(), 0))[2]
_paint_cache = {}


def _paint(col, width):
    key = (tuple(col), width)
    if key not in _paint_cache:
        a = (col[3] / 255.0) if len(col) > 3 else 1.0
        k = width / 1.9

        def fade(x):
            if x is None:
                return None
            return (x[0], x[1], x[2], int(255 * a * ((x[3] / 255.0)
                                                     if len(x) > 3 else 1.0)))
        _paint_cache[key] = {m: (fade(f), fade(s), w * k) for m, (f, s, w)
                             in F.palette(tuple(col[:3]), BG).items()}
    return _paint_cache[key]


def put(c, parts, x, gy, s, col, width=1.8, flip=1):
    F.draw(c, parts, x, gy, s, col, BG, flip=flip, style=_paint(col, width))


def fit(parts, w=None, h=None):
    """Scale that fits `parts` into the given width and/or height. With both,
    whichever binds wins — fitting by width alone makes a narrow thing (a
    cross, a pillar) tower, and fitting by height alone makes a wide one (a
    stack of coins, a table) sprawl."""
    x0, x1, y0, y1 = F.bbox((parts, 0))
    ks = []
    if w is not None:
        ks.append(w / (x1 - x0))
    if h is not None:
        ks.append(h / (y1 - y0))
    return min(ks)


def balance(c, x, gy, h, left, right, heavy, cold=None, warm=None,
            size=9.5):
    """A pair of balances with a real thing in each pan, tipped to the side
    the text says is heavier.

    Hebrews weighs twice and the two weighings answer each other: Moses
    accounts the reproach of Christ greater riches than the treasures of
    Egypt (11:26), and Esau lets one meal outweigh his birthright (12:16).
    Same instrument, same objects-in-pans, opposite verdict — so they are
    drawn by one function, and the only thing that differs is which way it
    goes down.

    `left` and `right` are (parts, label) pairs; `heavy` is -1 or +1.
    """
    cold = cold or dim(SHADOW_LIT, 0.95)
    warm = warm or HL
    parts = F.scales(tilt=heavy)
    s = fit(parts, h=h)
    put(c, parts, x, gy, s, dim(SAND, 0.95), 1.7)
    pans = F.scales_pans(tilt=heavy)
    for i, ((obj, txt), sx) in enumerate(zip((left, right), (-1, 1))):
        (px, py), = F.place([pans[i]], x, gy, s)
        col = warm if sx == heavy else cold
        # The pan rim is the ground the object stands on, and each object is
        # cut to the pan rather than to a shared size — a stack of coins and
        # a cross are not the same shape and should not pretend to be.
        put(c, obj, px, py, fit(obj, w=h * 0.34, h=h * 0.30), col, 1.7)
        # clear of the pan, which hangs below the rim the object stands on
        c.text((px, py + h * 0.24), txt, size, col, "mm",
               bold=(sx == heavy))


def label(c, xy, s, size=11, col=None, anchor="mm", bold=False, italic=False):
    c.text(xy, s, size, col or dim(TEXT, 0.92), anchor, bold=bold,
           italic=italic)


def rail(c, x, y0, y1, items, lit, col=None, size=10.5):
    """A short list down one side — the catena of chapter 1, the wilderness
    ledger of chapter 3. Rows appear as their verse lands; nothing counts."""
    col = col or dim(TEXT_DIM, 0.9)
    step = (y1 - y0) / max(1, len(items) - 1) if len(items) > 1 else 0
    for i, (txt, ok) in enumerate(items):
        if not ok:
            continue
        gy = y0 + i * step
        hot = (i == lit)
        c.text((x, gy), txt, size, HL if hot else col, "lm", bold=hot)


# ---------------------------------------------------------------------------
# 1 — the throne, and the servants who have no seat
# ---------------------------------------------------------------------------
#
# The catena of vv5-13 is the chapter's own structure: seven quotations, each
# landing on the Son's side of the angel line or the angels'. The rail lists
# them; the arcs say where each one goes.

CATENA = [("YOU ARE MY SON", 5, "son"),
          ("A FATHER ... A SON", 5, "son"),
          ("LET ALL THE ANGELS WORSHIP HIM", 6, "son"),
          ("HIS ANGELS, WINDS AND FIRE", 7, "angels"),
          ("YOUR THRONE, O GOD, IS FOREVER", 8, "son"),
          ("YOU LAID THE FOUNDATION", 10, "son"),
          ("SIT AT MY RIGHT HAND", 13, "son")]


def ch1(c, cam, v, pos):
    # No tent: chapter 1 never mentions the tabernacle. Its subject is the
    # throne, the Son and the angels, and the true tent standing in the
    # middle of the frame was only crowding the catena out of it.
    y_rank = cam.y(U_HEAVENS)
    shadow(c, cam, upto=U_TOP)

    # v1 — many times, and in various ways: fragmentary arcs at scattered
    # angles, each to a different hearer. v2 collapses them into one.
    if v == 1:
        for i, fx in enumerate((300, 396, 492, 604, 704, 800)):
            figure(c, fx, cam.y(U_TOP) - 2, 34, dim(SAND, 0.85))
            voice_arc(c, (fx - 90 + i * 34, SYT + 8), (fx, cam.y(U_TOP) - 34),
                      dim(SAND, 0.55 + 0.05 * i), 1.4, bulge=0.16 + i * 0.06)
        label(c, (552, cam.y(U_TOP) + 22), "THE FATHERS, BY THE PROPHETS",
              10.5, dim(TEXT_DIM, 0.95), italic=True)
        label(c, (552, SYT + 26), "at many times, and in various ways", 12,
              dim(TEXT, 0.9), italic=True)

    if v >= 2:
        substance(c, cam, seat=v >= 3, tent=False)
        voice_arc(c, (236, SYT + 22), (CX - 116, cam.y(U_SEAT + 12)),
                  dim(HL, 0.9), 2.2, bulge=0.26)
        if v == 2:
            # He has not sat down yet — that is v3. Here he stands, and the
            # one arc that replaced the six of v1 lands on him.
            figure(c, CX, cam.y(U_SEAT - 34), 74, HL)
            label(c, (CX, cam.y(U_SEAT - 34) + 18), "HIS SON", 11, HL,
                  bold=True)
        for wx, wy, r in ((792, 148, 16), (862, 190, 11), (826, 232, 7)):
            c.circle(wx, wy, r, fill=None, stroke=dim(SAND, 0.85), width=1.5)
        label(c, (830, 262), "THE WORLDS", 9.5, dim(TEXT_DIM, 0.95))
        if v == 3:
            label(c, (CX, cam.y(U_SEAT - 60)), "sat down on the right hand "
                  "of the Majesty on high", 10, dim(TEXT, 0.9), italic=True)

    if v >= 4:
        c.line((SX0, y_rank), (SX1, y_rank), dim(SILVER, 0.75), 1.4,
               dash="8,6")
        label(c, (SX1 - 8, y_rank - 12), "THE ANGELS", 10.5,
              dim(SILVER, 0.95), anchor="rm", bold=True)

    # vv5-13 — the seven quotations, in the text's order. Six land on the
    # Son's side of the rank line and one on the angels', which is the
    # chapter's argument; the rail names them and the arcs say where each
    # goes. Only the arc whose verse this is carries any weight.
    shown = [(t, v >= at) for t, at, _s in CATENA]
    lit = max([i for i, (_t, at, _s) in enumerate(CATENA) if at == v],
              default=-1)
    if v >= 5:
        rail(c, 122, 250, 466, shown, lit, size=9.5)
        for i, (_t, at, side) in enumerate(CATENA):
            if v < at:
                continue
            gy = 250 + i * (466 - 250) / 6
            tgt = (CX - 130, cam.y(U_SEAT - 16)) if side == "son" else \
                (704, y_rank)
            voice_arc(c, (312, gy), tgt,
                      dim(HL, 0.9) if i == lit else dim(SAND, 0.28),
                      2.0 if i == lit else 1.0, bulge=0.16, speaker=False)

    if v >= 7:                       # servants: winds, and a flame of fire
        for fx in (692, 762, 832):
            c.path(f"M{fx},{y_rank} q{-9},{-14} {3},{-27} "
                   f"q{7},{13} {13},{20} q{-4},{-14} {0},{-22} "
                   f"q{11},{18} {2},{29} z",
                   fill=dim(FIRE, 0.85 if v == 7 else 0.42))
        if v == 7:
            label(c, (762, y_rank + 18), "winds, and a flame of fire", 9.5,
                  dim(FIRE, 0.95), italic=True)

    if v >= 8:                       # the sceptre of uprightness
        c.line((CX + 74, cam.y(U_SEAT + 26)), (CX + 104, cam.y(U_SEAT - 30)),
               dim(GOLD, 0.95), 3.0)
        c.circle(CX + 72, cam.y(U_SEAT + 30), 6, fill=GOLD)
        if v == 8:
            label(c, (CX + 118, cam.y(U_SEAT - 4)), "THE SCEPTER", 9.5,
                  dim(TEXT, 0.9), anchor="lm", bold=True)
    if v >= 9:                       # the oil of gladness, above his fellows
        for i in range(5):
            c.circle(CX - 88 + i * 9, cam.y(U_SEAT + 54) - i * 4, 2.6,
                     fill=dim(HL, 0.9))
        label(c, (CX - 100, cam.y(U_SEAT + 56)), "OIL OF GLADNESS", 9.5,
              dim(TEXT_DIM, 0.95), anchor="rm")

    if v >= 10:                      # they will perish, but you continue
        # The right-hand column, clear of the rail, the throne and the angel
        # label at the margin.
        c.text((830, 300), "THE HEAVENS", 10, dim(SAND, 0.9), "mm")
        for i in range(4):
            k = 1.0 if v < 12 else 0.44
            c.path(f"M{786 + i * 22},{314} q{6 * k},{30} {0},{56 * k}",
                   fill=None, stroke=dim(SAND, 0.75), width=1.6)
        if v >= 11:
            label(c, (830, 384), "grow old like a garment", 9,
                  dim(TEXT_DIM, 0.95), italic=True)
        if v >= 12:
            label(c, (830, 398), "rolled up like a mantle", 9,
                  dim(TEXT_DIM, 0.95), italic=True)
            label(c, (830, 396 + 22), "BUT YOU ARE THE SAME", 10, HL,
                  bold=True)

    if v >= 13:                      # the footstool begun — placed at 10:13
        fy = cam.y(U_SEAT - 62)
        c.polyline([(CX - 52, fy), (CX + 52, fy), (CX + 52, fy + 15),
                    (CX - 52, fy + 15)], dim(GOLD, 0.7), 1.6,
                   dash="5,4" if v < 14 else None, closed=True)
        label(c, (CX, fy + 28), "A FOOTSTOOL", 9.5, dim(TEXT_DIM, 0.95))

    if v == 14:                      # sent out, for the sake of the heirs
        for fx in (664, 748, 832, 916):
            arrow(c, (fx, y_rank + 14), (fx - 12, SYB - 30),
                  dim(SILVER, 0.85), 1.6, 7)
        label(c, (790, SYB - 14), "SENT OUT TO DO SERVICE", 11,
              dim(SILVER, 0.95), bold=True)


# ---------------------------------------------------------------------------
# 2 — the descent below the line
# ---------------------------------------------------------------------------


def ch2(c, cam, v, pos):
    shadow(c, cam, upto=U_TOP, labels=v <= 4)
    substance(c, cam, seat=True, tent=True)
    y_rank = cam.y(U_HEAVENS)
    c.line((SX0, y_rank), (SX1, y_rank), dim(SILVER, 0.60), 1.3, dash="8,6")
    label(c, (SX1 - 8, y_rank - 11), "THE ANGELS", 9.5, dim(SILVER, 0.9),
          anchor="rm", bold=True)
    y_camp = cam.y(U_CAMP)

    if v == 1:                       # first warning — lest we drift away
        c.circle(300, cam.y(U_COURT), 5, fill=dim(HL, 0.9))
        label(c, (300, cam.y(U_COURT) - 18), "THE THINGS HEARD", 9.5,
              dim(TEXT, 0.9))
        for i in range(4):
            c.path(f"M{318 + i * 6},{cam.y(U_COURT) + 14 + i * 9} "
                   f"q{54},{-8} {108},{2}", fill=None,
                   stroke=dim(SHADOW_LIT, 0.8), width=1.4)
        figure(c, 452, cam.y(U_COURT) + 46, 40, dim(SAND, 0.9))
        arrow(c, (330, cam.y(U_COURT) + 30), (438, cam.y(U_COURT) + 30),
              dim(RED, 0.9), 1.8, 8, dash="6,5")
        label(c, (552, cam.y(U_COURT) + 66), "DRIFT AWAY", 12,
              dim(RED, 0.95), bold=True)

    if 2 <= v <= 4:                  # two deliveries, and four attestations
        voice_arc(c, (300, SYT + 18), (300, y_rank - 6), dim(SAND, 0.8), 1.6)
        voice_arc(c, (300, y_rank + 6), (330, cam.y(U_COURT)),
                  dim(SAND, 0.8), 1.6, speaker=False)
        label(c, (300, cam.y(U_COURT) + 16), "through angels", 9.5,
              dim(TEXT_DIM, 0.95), italic=True)
        voice_arc(c, (700, SYT + 18), (720, cam.y(U_COURT)), dim(HL, 0.9),
                  2.2, bulge=0.22)
        label(c, (720, cam.y(U_COURT) + 16), "by the Lord", 9.5, HL,
              italic=True)
        if v >= 3:
            label(c, (720, cam.y(U_COURT) + 32), "confirmed by those "
                  "who heard", 9, dim(TEXT_DIM, 0.95), italic=True)
        if v >= 4:
            for i, s in enumerate(("SIGNS", "WONDERS", "POWERS", "GIFTS")):
                c.rect(628 + i * 96, cam.y(U_COURT) + 46, 84, 20, fill=None,
                       stroke=dim(GOLD, 0.8), width=1.3, rx=3)
                label(c, (670 + i * 96, cam.y(U_COURT) + 56), s, 9,
                      dim(TEXT, 0.92), bold=True)

    if 5 <= v <= 8:                  # Psalm 8 on the height line
        for u, s, on in ((U_HEAVENS - 40, "A LITTLE LOWER", v >= 7),
                         (U_HEAVENS + 46, "CROWNED WITH GLORY", v >= 7),
                         (U_CAMP + 40, "ALL THINGS UNDER HIS FEET", v >= 8)):
            if not on:
                continue
            c.line((360, cam.y(u)), (744, cam.y(u)), dim(HL, 0.75), 1.5,
                   dash="4,4")
            label(c, (352, cam.y(u)), s, 10, dim(TEXT, 0.92), anchor="rm",
                  bold=True)
        if v == 6:
            label(c, (552, cam.y(U_COURT)), "WHAT IS MAN?", 15, HL, bold=True)
        if v == 8:
            label(c, (760, cam.y(U_CAMP) + 40), "but we don't see all things "
                  "subjected to him, yet", 10, dim(SHADOW_LIT, 0.95),
                  anchor="lm", italic=True)

    if v >= 9:                       # the descent — the only one before 13:13
        pts = [(CX, cam.y(U_SEAT - 40)), (CX - 40, cam.y(U_TRUE)),
               (CX - 30, cam.y(U_HEAVENS)), (CX - 60, cam.y(U_COURT)),
               (CX - 40, cam.y(U_OUT))]
        c.polyline(pts, dim(HL, 0.9), 2.6)
        arrow(c, pts[-2], pts[-1], dim(HL, 0.9), 2.6, 9)
        figure(c, CX - 40, cam.y(U_OUT), 40, HL)
        if v == 9:
            engrave(c, 2, 9, v, (CX + 210, cam.y(U_COURT) - 10), 19)
        label(c, (CX - 40, cam.y(U_OUT) + 18), "the suffering of death", 9.5,
              dim(TEXT_DIM, 0.95), italic=True)

    if v >= 10:                      # and back, made perfect through it
        c.path(f"M{CX - 40},{cam.y(U_OUT) - 46} Q{CX + 150},"
               f"{cam.y(U_COURT)} {CX + 8},{cam.y(U_SEAT - 44)}",
               fill=None, stroke=dim(GOLD, 0.85), width=2.2)
        if v == 10:
            label(c, (CX + 168, cam.y(U_HOLY)), "made perfect", 10.5,
                  dim(TEXT, 0.92), anchor="lm", italic=True)

    if 11 <= v <= 13:                # the arcs turn sideways: brothers
        for i in range(3):
            voice_arc(c, (CX - 30, cam.y(U_COURT)),
                      (300 - i * 0, cam.y(U_CAMP) + 30 + i * 16),
                      dim(HL, 0.85 - i * 0.18), 1.8, bulge=0.20)
        for i, fx in enumerate((250, 292, 334)):
            figure(c, fx, cam.y(U_CAMP) + 4, 34, dim(SAND, 0.9))
        label(c, (292, cam.y(U_CAMP) + 22), "BROTHERS", 11, HL, bold=True)
        label(c, (292, cam.y(U_CAMP) + 38), "he is not ashamed to call them",
              9, dim(TEXT_DIM, 0.95), italic=True)

    if v >= 14:                      # the lifetime, shackled and released
        bx, by = 400, cam.y(U_CAMP) + 30
        c.rect(bx, by, 296, 20, fill=None, stroke=dim(SAND, 0.9), width=1.5)
        if v == 14 or v == 15:
            hatch(c, bx, by, bx + (296 if v == 14 else 94), by + 20,
                  dim(RED, 0.7), step=11)
        label(c, (bx + 148, by - 14), "ALL THEIR LIFETIME", 10,
              dim(TEXT, 0.92), bold=True)
        label(c, (bx + 308, by + 10),
              "subject to bondage" if v == 14 else "delivered", 9.5,
              dim(RED, 0.95) if v == 14 else HL, anchor="lm", italic=True)

    if v >= 16:                      # not to angels, but to Abraham's seed
        c.line((300, y_rank + 10), (356, y_rank + 34), dim(SILVER, 0.6), 2.0)
        cross(c, 356, y_rank + 34, 7, dim(RED, 0.9), 2.0)
        arrow(c, (CX - 30, cam.y(U_COURT) + 10), (330, cam.y(U_CAMP) + 6),
              dim(HL, 0.9), 2.0, 8)

    if v >= 17:                      # a merciful and faithful high priest
        # The garment geometry Exodus 28 built — svg_priest.py — vested for
        # the first time in this book, and its subject through chapter 10.
        PF = G.Form(884, cam.y(U_CAMP) + 4, 110)
        G.body(c, PF, dim(SAND, 0.95), dim(BROWN, 0.5),
               rule=dim(SAND_DIM, 0.95), cloth=False)
        G.ephod(c, PF, dim(BROWN, 0.7), dim(GOLD, 0.85),
                band=dim(SCARLET, 0.8))
        G.breastplate_on(c, PF, dim(GOLD, 0.9))
        G.turban(c, PF, dim(LINEN, 0.8), dim(SAND_DIM, 0.95))
        label(c, (884, cam.y(U_CAMP) + 22), "A MERCIFUL AND", 9.5, HL,
              bold=True)
        label(c, (884, cam.y(U_CAMP) + 35), "FAITHFUL HIGH PRIEST", 9.5, HL,
              bold=True)
        if v == 18:
            label(c, (884, cam.y(U_CAMP) + 52), "able to help those", 9,
                  dim(TEXT_DIM, 0.95), italic=True)
            label(c, (884, cam.y(U_CAMP) + 65), "who are tempted", 9,
                  dim(TEXT_DIM, 0.95), italic=True)


# ---------------------------------------------------------------------------
# 3 — the house, and the road that never arrives
# ---------------------------------------------------------------------------
#
# 3:7-4:13 is one continuous warning and is built as one sub-world: a
# wilderness plane beside the column with a gate marked REST at the far end,
# and a path that loops and never reaches it.

Q316 = [("who rebelled?", 16), ("with whom was he displeased forty years?",
                                17), ("to whom did he swear?", 18)]


def wilderness(c, cam, v, ch, gate_open=False, walked=0.0, fallen=0,
               joshua=False):
    """The plane of 3:7-4:11, shared by both chapters that stand on it."""
    gy = cam.y(U_CAMP) - 4
    c.line((240, gy), (960, gy), dim(SHADOW_LIT, 0.85), 1.6)
    # the gate at the far end
    gx = 916
    col = HL if gate_open else dim(SILVER, 0.85)
    c.rect(gx - 40, gy - 96, 80, 96, fill=None, stroke=col, width=2.2)
    label(c, (gx, gy + 18), "REST", 12, col, bold=True)
    if not gate_open:
        c.line((gx - 46, gy - 48), (gx + 46, gy - 48), dim(RED, 0.9), 3.0)
    # the path: a loop that returns on itself
    n = 26
    pts = []
    for i in range(n + 1):
        t = i / n
        px = 280 + t * 470
        py = gy - 34 - math.sin(t * math.pi * 3.0) * 30
        pts.append((px, py))
    lit = max(2, int(len(pts) * walked))
    c.polyline(pts[:lit], dim(SAND, 0.85), 1.8)
    for i in range(fallen):
        fx = 320 + i * 92
        figure(c, fx, gy, 26, dim(SHADOW_LIT, 0.9), pose="kneel")
    if joshua:
        c.line((790, gy), (790, gy - 60), dim(GOLD, 0.8), 1.6, dash="5,4")
        label(c, (790, gy - 72), "JOSHUA", 10, dim(TEXT, 0.9), bold=True)
        label(c, (790, gy + 18), "not this day", 9,
              dim(TEXT_DIM, 0.95), italic=True)
    return gy, gx


def ch3(c, cam, v, pos):
    shadow(c, cam, upto=U_TOP, labels=False)

    if v <= 6:                       # the house, and who is in it or over it
        w = cam.w(HW_HOLY)
        yt, yb = cam.y(U_VEIL + 30), cam.y(U_COURT)
        c.polygon([(CX - w, yb), (CX + w, yb), (CX + w * 0.8, yt),
                   (CX - w * 0.8, yt)], fill=dim(SHADOW, 0.5),
                  stroke=dim(SILVER, 0.85), width=1.8)
        label(c, (CX, yb + 22), "THE HOUSE", 12, dim(TEXT, 0.92), bold=True)
        if v >= 2:
            figure(c, CX - 60, yb - 14, 58, dim(SAND, 0.95))
            label(c, (CX - 60, yb + 4), "MOSES", 10.5, dim(TEXT, 0.92),
                  bold=True)
            label(c, (CX - 60, cam.y(U_COURT) + 40),
                  "faithful ... as a servant", 9.5, dim(TEXT_DIM, 0.95),
                  italic=True)
        if v >= 3:
            figure(c, CX + 40, yt - 6, 62, HL)
            label(c, (CX + 40, yt - 76), "THE SON", 10.5, HL, bold=True)
            label(c, (CX + 150, yt - 40), "over the house", 9.5, HL,
                  anchor="lm", italic=True)
        if v >= 4:
            label(c, (CX, SYT + 30), "he who built all things is God", 11.5,
                  dim(TEXT, 0.9), italic=True)
        if v >= 6:
            for i, fx in enumerate((CX - 130, CX - 96, CX + 96, CX + 130)):
                c.rect(fx - 14, yb - 24, 28, 20, fill=dim(SHADOW_LIT, 0.5),
                       stroke=dim(HL, 0.8), width=1.4)
            label(c, (CX, yb + 62), "WHOSE HOUSE WE ARE", 11, HL, bold=True)

    else:                            # vv7-19 — the second warning
        walked = min(1.0, 0.18 + (v - 7) * 0.07)
        gy, gx = wilderness(c, cam, v, 3, walked=walked,
                            fallen=0 if v < 17 else 4)
        if v in (7, 15):
            c.circle(300, SYT + 52, 22, fill=None, stroke=dim(GOLD, 0.85),
                     width=2.0)
            for i in range(8):
                a = i * math.pi / 4
                c.line((300 + math.cos(a) * 28, SYT + 52 + math.sin(a) * 28),
                       (300 + math.cos(a) * 38, SYT + 52 + math.sin(a) * 38),
                       dim(GOLD, 0.7), 1.6)
            label(c, (300, SYT + 92), "TODAY", 11, HL, bold=True)
        if v == 7:
            engrave(c, 3, 7, v, (620, SYT + 46), 17)
        if v >= 8:
            voice_arc(c, (600, SYT + 26), (622, gy - 100), dim(HL, 0.8), 1.8)
        if v >= 11:
            label(c, (gx, gy - 118), "they will not enter", 9.5,
                  dim(RED, 0.95), italic=True)
        # The annotations stack above the plane, not below it: the camp line
        # sits near the foot of this viewport and there is no room under it.
        if v >= 12:
            label(c, (300, SYT + 116), "AN EVIL HEART OF UNBELIEF", 10.5,
                  dim(RED, 0.95), anchor="lm", bold=True)
        if v >= 13:
            label(c, (300, SYT + 134), "exhort one another day by day", 9.5,
                  dim(TEXT_DIM, 0.95), anchor="lm", italic=True)
        if v >= 16:                  # the chapter's own four-row ledger
            rows = [(t, v >= at) for t, at in Q316]
            rail(c, 300, SYT + 180, SYT + 228, rows,
                 max([i for i, (_t, at) in enumerate(Q316) if at == v],
                     default=-1), size=10)
            if v >= 19:
                label(c, (300, SYT + 256), "BECAUSE OF UNBELIEF", 12,
                      dim(RED, 0.95), anchor="lm", bold=True)


# ---------------------------------------------------------------------------
# 4 — the rest, the sword, the ascent
# ---------------------------------------------------------------------------


def ch4(c, cam, v, pos):
    shadow(c, cam, upto=U_TOP)
    substance(c, cam, seat=v >= 14, tent=True)

    if v <= 11:                      # the wilderness continues from ch3
        gy, gx = wilderness(c, cam, v, 4, walked=0.9,
                            gate_open=v >= 9, fallen=3, joshua=v >= 8)
        if v >= 4:                   # the seventh day
            for i in range(7):
                on = i == 6
                c.rect(300 + i * 34, SYT + 120, 28, 28,
                       fill=dim(GOLD, 0.35) if on else None,
                       stroke=dim(SAND, 0.9), width=1.4, rx=2)
            label(c, (402, SYT + 108), "GOD RESTED ON THE SEVENTH DAY", 10,
                  dim(TEXT, 0.92), bold=True)
        if v >= 5:                   # the oath quoted a second time
            voice_arc(c, (640, SYT + 34), (gx - 20, gy - 112),
                      dim(RED, 0.85), 1.7, bulge=0.24)
        if v >= 6:                   # some are still to enter in
            arrow(c, (740, gy - 40), (gx - 46, gy - 40),
                  dim(HL, 0.85) if v >= 9 else dim(SAND, 0.6), 1.8, 8,
                  dash=None if v >= 9 else "6,5")
        if v >= 7:                   # today, defined again — through David
            sx_, sy_ = 700, SYT + 152
            c.circle(sx_, sy_, 17, fill=None, stroke=dim(GOLD, 0.85),
                     width=1.8)
            for i in range(8):
                a = i * math.pi / 4
                c.line((sx_ + math.cos(a) * 22, sy_ + math.sin(a) * 22),
                       (sx_ + math.cos(a) * 30, sy_ + math.sin(a) * 30),
                       dim(GOLD, 0.7), 1.4)
            label(c, (sx_, sy_ + 46), "TODAY", 10.5, HL, bold=True)
        # The left-hand stack, above the plane: the camp line sits near the
        # foot of this viewport and there is no room under it.
        for at, s, size, col, it, bold in (
                (3, "we who have believed do enter", 10, HL, True, False),
                (5, "and in this place again: they will not enter", 9.5,
                 dim(RED, 0.95), True, False),
                (6, "it remains that some should enter", 9.5,
                 dim(TEXT_DIM, 0.95), True, False),
                (7, "through David, so long a time afterward", 9.5,
                 dim(TEXT_DIM, 0.95), True, False),
                (10, "has himself also rested from his works", 9.5,
                 dim(TEXT_DIM, 0.95), True, False),
                (11, "let us therefore give diligence", 10.5, HL, False,
                 True)):
            if v >= at:
                label(c, (300, SYT + 180 + [3, 5, 6, 7, 10, 11].index(at)
                          * 19), s, size, col, anchor="lm", italic=it,
                      bold=bold)
        if v == 9:
            engrave(c, 4, 9, v, (620, SYT + 60), 18)

    elif v <= 13:                    # the sword: a section cut, not a swing
        fx = 430
        FF = G.Form(fx, cam.y(U_CAMP) + 10, 300)
        c.polyline(G.silhouette(FF), dim(SAND, 0.9), 1.6, closed=True)
        c.line((fx, cam.y(U_CAMP) + 10 - 300), (fx, cam.y(U_CAMP) + 10),
               dim(HL, 0.95), 2.6)
        for u, s in ((0.30, "SOUL / SPIRIT"), (0.55, "JOINTS / MARROW"),
                     (0.78, "THOUGHTS AND INTENTIONS")):
            ly = cam.y(U_CAMP) + 10 - 300 * (1 - u)
            c.line((fx - 78, ly), (fx + 78, ly), dim(HL, 0.75), 1.4,
                   dash="4,4")
            label(c, (fx + 96, ly), s, 9.5, dim(TEXT, 0.92), anchor="lm")
        engrave(c, 4, 12, v, (700, SYT + 70), 19)
        if v == 13:
            label(c, (700, SYT + 116), "all things are naked and laid open",
                  11, dim(TEXT, 0.92), italic=True)
            label(c, (700, SYT + 136), "before the eyes of him to whom "
                  "we must give an account", 9.5, dim(TEXT_DIM, 0.95),
                  italic=True)

    else:                            # vv14-16 — the ascent, and the throne
        pts = [(CX - 30, cam.y(U_CAMP)), (CX - 10, cam.y(U_HOLY)),
               (CX + 10, cam.y(U_HEAVENS)), (CX, cam.y(U_SEAT - 52))]
        c.polyline(pts, dim(HL, 0.9), 2.6)
        arrow(c, pts[-2], pts[-1], dim(HL, 0.9), 2.6, 9)
        label(c, (CX + 40, cam.y(U_HEAVENS) - 8), "passed through "
              "the heavens", 10, HL, anchor="lm", italic=True)
        if v >= 15:
            label(c, (240, cam.y(U_HOLY)), "tempted like we are,", 10,
                  dim(TEXT, 0.92), anchor="lm")
            label(c, (240, cam.y(U_HOLY) + 16), "yet without sin", 10,
                  dim(TEXT, 0.92), anchor="lm", bold=True)
        if v >= 16:
            label(c, (CX, cam.y(U_SEAT + 62)), "THE THRONE OF GRACE", 12,
                  HL, bold=True)
            engrave(c, 4, 16, v, (CX, SYB - 22), 18)


# ---------------------------------------------------------------------------
# 5 — the commission, and the two diets
# ---------------------------------------------------------------------------
#
# vv1-4 are a job spec, so they are drawn as one: six requirements, ticked
# against Aaron. vv5-6 run the same six against Christ, and the row Aaron
# cannot tick is FOREVER — left blank here and paid off in chapter 7.

COMMISSION = [("taken from among men", 1), ("appointed for men", 1),
              ("offers gifts and sacrifices", 1),
              ("deals gently, being himself weak", 2),
              ("must offer for himself also", 3),
              ("does not take the honor on himself", 4)]


def vested(c, x, gy, h, ink=None, breastplate=True, turban=True):
    """A high priest in the garments of Exodus 28 — svg_priest.py, the
    module that chapter built and this book spends."""
    ink = ink or dim(SAND, 0.95)
    PF = G.Form(x, gy, h)
    G.body(c, PF, ink, dim(BROWN, 0.5), rule=dim(SAND_DIM, 0.95), cloth=False)
    G.ephod(c, PF, dim(BROWN, 0.7), dim(GOLD, 0.85), band=dim(SCARLET, 0.8))
    if breastplate:
        G.breastplate_on(c, PF, dim(GOLD, 0.9))
    if turban:
        G.turban(c, PF, dim(LINEN, 0.8), dim(SAND_DIM, 0.95))
    return PF


def ch5(c, cam, v, pos):
    shadow(c, cam, upto=U_TOP)
    substance(c, cam, seat=True, tent=True)
    gy = cam.y(U_HOLY)

    # the six requirements, ticked as the verses name them
    for i, (txt, at) in enumerate(COMMISSION):
        if v < at:
            continue
        ry = 176 + i * 21
        hot = (at == v and v <= 4)
        c.rect(122, ry - 6, 11, 11, fill=GOLD if v > at or v > 4 else None,
               stroke=HL if hot else dim(SAND, 0.9), width=1.3, rx=2)
        label(c, (142, ry), txt, 9.5, HL if hot else dim(TEXT, 0.9),
              anchor="lm", bold=hot)
    if v >= 1:
        label(c, (122, 156), "EVERY HIGH PRIEST", 10.5, dim(TEXT, 0.92),
              anchor="lm", bold=True)

    if v <= 4:
        vested(c, 470, gy, 118)
        label(c, (470, gy + 20), "AARON", 11, dim(TEXT, 0.92), bold=True)
        if v >= 4:
            label(c, (470, gy + 38), "called by God, just like Aaron was",
                  9.5, dim(TEXT_DIM, 0.95), italic=True)

    if v >= 5:                       # the same six, run against the Son
        vested(c, 420, gy, 118)
        label(c, (420, gy + 20), "AARON", 10.5, dim(TEXT_DIM, 0.95))
        vested(c, 640, gy, 130, ink=HL)
        label(c, (640, gy + 20), "CHRIST", 11, HL, bold=True)
        voice_arc(c, (330, SYT + 30), (640, gy - 140), dim(HL, 0.9), 2.0)
        if v == 5:
            label(c, (640, gy + 38), "he didn't glorify himself", 9.5,
                  dim(TEXT_DIM, 0.95), italic=True)
    if v >= 6:                       # the row Aaron cannot tick
        ry = 176 + 6 * 21
        c.rect(122, ry - 6, 11, 11, fill=None, stroke=dim(SILVER, 0.7),
               width=1.3, rx=2)
        label(c, (142, ry), "forever", 9.5, dim(SILVER, 0.8), anchor="lm")
        cross(c, 127, ry - 1, 7, dim(RED, 0.9), 1.8)
        c.rect(122, ry + 15, 11, 11, fill=GOLD, stroke=HL, width=1.3, rx=2)
        label(c, (142, ry + 21), "after the order of Melchizedek", 9.5, HL,
              anchor="lm", bold=True)
        engrave(c, 5, 6, v, (700, SYT + 44), 18)

    if 7 <= v <= 10:                 # the days of his flesh
        pts = [(640, gy - 140), (700, cam.y(U_COURT) - 10),
               (790, cam.y(U_COURT) - 40), (840, gy - 150)]
        c.polyline(pts[:min(4, v - 5)], dim(GOLD, 0.85), 2.2)
        for at, s, px, py in ((7, "strong crying and tears", 700, 512),
                              (8, "learned obedience by what he suffered",
                               700, 528),
                              (9, "the author of eternal salvation", 830,
                               300),
                              (10, "named by God a high priest", 830, 316)):
            if v >= at:
                label(c, (px, py), s, 9.5,
                      HL if v == at else dim(TEXT_DIM, 0.95),
                      anchor="lm" if px == 830 else "mm", italic=True)

    if v >= 11:                      # the third warning opens: dull of hearing
        voice_arc(c, (700, SYT + 26), (868, 240), dim(SAND, 0.40), 1.6)
        c.circle(868, 240, 7, fill=None, stroke=dim(SHADOW_LIT, 0.9),
                 width=2.0)
        label(c, (868, 262), "DULL OF HEARING", 10, dim(SHADOW_LIT, 0.95),
              bold=True)
    if v >= 12:                      # milk, and solid food
        for i, (s, at, col) in enumerate((("MILK", 12, dim(SILVER, 0.9)),
                                          ("SOLID FOOD", 14, GOLD))):
            if v < at:
                continue
            bx = 760 + i * 130
            c.circle(bx, 336, 26, fill=None, stroke=col, width=2.0)
            label(c, (bx, 372), s, 10, col, bold=True)
        if v >= 13:
            figure(c, 760, 424, 40, dim(SAND, 0.9), kind="child")
            label(c, (760, 440), "a baby", 9.5, dim(TEXT_DIM, 0.95),
                  italic=True)
        if v >= 14:
            figure(c, 890, 424, 62, HL)
            label(c, (890, 440), "full grown", 9.5, HL, italic=True)
            label(c, (826, 462), "senses exercised to discern good and evil",
                  9, dim(TEXT_DIM, 0.95), italic=True)


# ---------------------------------------------------------------------------
# 6 — foundation, field, oath, anchor
# ---------------------------------------------------------------------------

FOUNDATION = ["repentance from dead works", "faith toward God",
              "the teaching of baptisms", "laying on of hands",
              "resurrection of the dead", "eternal judgment"]

TASTED = ["once enlightened", "tasted the heavenly gift",
          "partakers of the Holy Spirit", "tasted the good word of God",
          "the powers of the age to come"]


def _ch6_foundation(c, cam, v):
    """vv1-6 — a course laid once, and a figure that falls off it."""
    course_y = 380
    for i, s in enumerate(FOUNDATION):
        if v < (1 if i < 2 else 2):
            continue
        sx_ = 130 + i * 74
        c.rect(sx_, course_y, 68, 22, fill=dim(SHADOW, 0.7),
               stroke=dim(SHADOW_LIT, 0.9), width=1.3, rx=2)
        label(c, (sx_ + 34, course_y + 34 + (i % 2) * 13), s, 8,
              dim(TEXT_DIM, 0.95), italic=True)
    label(c, (130, course_y - 18), "A FOUNDATION, NOT LAID AGAIN", 10,
          dim(TEXT, 0.92), anchor="lm", bold=True)
    if v == 3:
        label(c, (700, course_y + 4), "this will we do, if God permits",
              10.5, dim(TEXT, 0.9), anchor="lm", italic=True)
    if v >= 4:
        for i, s in enumerate(TASTED):
            if v < (4 if i < 3 else 5):
                continue
            label(c, (652, 180 + i * 20), s, 9.5,
                  HL if v <= 5 else dim(SHADOW_LIT, 0.9), anchor="lm")
            c.circle(638, 176 + i * 20, 4, fill=dim(HL, 0.9) if v <= 5
                     else dim(SHADOW_LIT, 0.85))
    if v == 6:
        fx = 300
        arrow(c, (fx, course_y + 60), (fx, course_y + 108), dim(RED, 0.9),
               2.0, 8)
        figure(c, fx, course_y + 158, 46, dim(SHADOW_LIT, 0.9), pose="kneel")
        label(c, (fx + 46, course_y + 132), "fell away", 10.5,
              dim(RED, 0.95), anchor="lm", bold=True)
        label(c, (652, 296), "impossible to renew them again", 9.5,
              dim(RED, 0.95), anchor="lm", italic=True)


def _ch6_field(c, cam, v):
    """vv7-12 — the same rain on two fields, and the ledger God keeps."""
    rx_ = 552
    c.circle(rx_, 178, 5, fill=dim(SILVER, 0.9))
    label(c, (rx_, 160), "THE SAME RAIN", 9.5, dim(TEXT_DIM, 0.95),
          italic=True)
    for sx in (-1, 1):
        c.path(f"M{rx_},{184} Q{rx_ + sx * 76},{216} "
               f"{rx_ + sx * 168},{250}", fill=None,
               stroke=dim(SILVER, 0.8), width=1.6)
    for sx in (-1, 1):
        px = rx_ + sx * 168
        good = sx < 0
        if v < (7 if good else 8):
            continue
        c.rect(px - 76, 256, 152, 48, fill=dim(SHADOW, 0.55),
               stroke=dim(SHADOW_LIT, 0.9), width=1.3)
        if good:
            for k in range(7):
                c.line((px - 60 + k * 20, 256), (px - 60 + k * 20, 236),
                       dim(GOLD, 0.9), 2.0)
            label(c, (px, 320), "RECEIVES BLESSING", 9.5, HL, bold=True)
        else:
            for k in range(5):
                c.line((px - 56 + k * 28, 256), (px - 62 + k * 28, 238),
                       dim(BROWN, 0.95), 1.8)
                c.line((px - 56 + k * 28, 250), (px - 48 + k * 28, 238),
                       dim(BROWN, 0.95), 1.6)
            label(c, (px, 320), "THORNS AND THISTLES", 9.5, dim(RED, 0.95),
                  bold=True)
            label(c, (px, 336), "whose end is to be burned", 9,
                  dim(FIRE, 0.95), italic=True)
    for at, s in ((9, "we are persuaded of better things for you"),
                  (10, "your work, and the labor of love, which you showed"),
                  (11, "the fullness of hope, even to the end"),
                  (12, "imitators of those who inherited the promises")):
        if v >= at:
            label(c, (200, 392 + (at - 9) * 19), s, 9.5,
                  HL if v == at else dim(TEXT_DIM, 0.95), anchor="lm",
                  italic=True)
    if v >= 10:
        label(c, (200, 370), "GOD IS NOT UNRIGHTEOUS, SO AS TO FORGET", 10,
              dim(TEXT, 0.92), anchor="lm", bold=True)


def _ch6_oath(c, cam, v):
    """vv13-18 — an oath sworn by no one greater, so it curves back."""
    ox, oy = 280, 250
    c.path(f"M{ox},{oy + 56} Q{ox + 8},{oy - 46} {ox + 84},{oy - 28} "
           f"Q{ox + 146},{oy - 10} {ox + 96},{oy + 48}",
           fill=None, stroke=dim(GOLD, 0.9), width=2.2)
    arrow(c, (ox + 110, oy + 32), (ox + 94, oy + 52), dim(GOLD, 0.9), 2.0, 7)
    label(c, (ox + 50, oy + 86), "he could swear by no one greater", 10,
          HL, italic=True)
    if v >= 14:
        label(c, (ox + 50, oy + 108), "BLESSING I WILL BLESS YOU", 10.5, HL,
              bold=True)
    if v >= 15:
        label(c, (ox + 50, oy + 128), "having patiently endured, "
              "he obtained the promise", 9, dim(TEXT_DIM, 0.95), italic=True)
    if v >= 16:
        label(c, (ox + 50, oy + 148), "the oath is final for confirmation",
              9, dim(TEXT_DIM, 0.95), italic=True)
    if v >= 17:                      # two immutable things, as two pillars
        for i, s in enumerate(("THE PROMISE", "THE OATH")):
            bx = 700 + i * 150
            c.rect(bx - 50, 222, 100, 120, fill=None, stroke=dim(GOLD, 0.85),
                   width=1.8)
            for k in range(3):
                c.line((bx - 50, 246 + k * 32), (bx + 50, 246 + k * 32),
                       dim(GOLD, 0.35), 1.1)
            label(c, (bx, 358), s, 9.5, dim(TEXT, 0.92), bold=True)
        label(c, (775, 204), "TWO IMMUTABLE THINGS", 10.5, HL, bold=True)
    if v >= 18:
        label(c, (775, 388), "we who have fled for refuge", 10, HL,
              italic=True)
        label(c, (775, 406), "to take hold of the hope set before us", 9,
              dim(TEXT_DIM, 0.95), italic=True)


def ch6(c, cam, v, pos):
    shadow(c, cam, upto=U_TOP, pierced=v >= 19)
    substance(c, cam, seat=True, tent=True)

    # Four movements, and only one on screen at a time. All four at once is
    # what put the field on top of the oath and the fall off the canvas.
    if v <= 6:
        _ch6_foundation(c, cam, v)
    elif v <= 12:
        _ch6_field(c, cam, v)
    elif v <= 18:
        _ch6_oath(c, cam, v)

    if v >= 19:                      # the anchor — the first thing to cross
        ay = cam.y(U_COURT) - 40
        vy = cam.y(U_VEIL)
        c.line((CX, ay), (CX, vy - 6), dim(HL, 0.95), 2.4)
        c.path(f"M{CX - 22},{ay - 6} Q{CX},{ay + 22} {CX + 22},{ay - 6}",
               fill=None, stroke=dim(HL, 0.95), width=2.6)
        c.line((CX - 16, ay - 20), (CX + 16, ay - 20), dim(HL, 0.95), 2.4)
        engrave(c, 6, 19, v, (CX + 200, cam.y(U_HOLY) + 10), 17)
        label(c, (CX, ay + 40), "entering into that within the veil", 9.5,
              HL, italic=True)
    if v >= 20:                      # the forerunner, already inside
        figure(c, CX, cam.y(U_MOST), 42, HL)
        label(c, (CX + 130, cam.y(U_MOST) - 30), "A FORERUNNER", 10.5, HL,
              anchor="lm", bold=True)
        label(c, (CX + 130, cam.y(U_MOST) - 14), "entered for us", 9.5,
              dim(TEXT_DIM, 0.95), anchor="lm", italic=True)


# ---------------------------------------------------------------------------
# 7 — break-away: the genealogy with the boxes missing
# ---------------------------------------------------------------------------
#
# Three arguments in twenty-eight verses, and they do not share a drawing:
# the genealogy and the tithe (1-10), the change of priesthood and law
# (11-22), and the many priests against the one (23-28). Precedent for
# cutting rather than accumulating: Acts 15-18 steps aside from its map five
# times.

TRIBES12 = ["REUBEN", "SIMEON", "LEVI", "JUDAH", "DAN", "NAPHTALI", "GAD",
            "ASHER", "ISSACHAR", "ZEBULUN", "JOSEPH", "BENJAMIN"]


def _node(c, x, y, w, h, name, col, sockets=True, bar=None, sub=None):
    """A genealogy node in the house style, with its parent sockets drawn.
    Melchizedek's are drawn empty, which is the whole of 7:3."""
    c.rect(x - w / 2, y - h / 2, w, h, fill=dim(PANEL, 0.9), stroke=col,
           width=2.0, rx=3)
    label(c, (x, y - (5 if sub else 0)), name, 12, col, bold=True)
    if sub:
        label(c, (x, y + 11), sub, 8.5, dim(TEXT_DIM, 0.95), italic=True)
    for sx in (-1, 1):
        px = x + sx * w * 0.28
        c.circle(px, y - h / 2 - 9, 5, fill=None,
                 stroke=col if sockets else dim(SILVER, 0.55), width=1.6)
        if sockets:
            c.line((px, y - h / 2 - 4), (px, y - h / 2), col, 1.6)
    if bar is not None:
        c.line((bar[0], y + h / 2 + 14), (bar[1], y + h / 2 + 14), col, 2.6)
        for bx in bar[:2]:
            c.line((bx, y + h / 2 + 9), (bx, y + h / 2 + 19), col, 2.0)


def ch7(c, cam, v, pos):
    if v <= 10:
        _ch7_genealogy(c, v)
    elif v <= 22:
        _ch7_change(c, v)
    else:
        _ch7_many(c, v)


def _ch7_genealogy(c, v):
    label(c, (SX0 + 10, 116), "MELCHIZEDEK", 16.5, TEXT, anchor="lm",
          bold=True)
    label(c, (SX0 + 10, 138), "king of Salem, priest of God Most High", 11.5,
          dim(TEXT_DIM, 0.95), anchor="lm", italic=True)

    # Melchizedek: no parents, and a life with no drawn ends.
    mx, my = 320, 236
    _node(c, mx, my, 190, 62, "MELCHIZEDEK", HL, sockets=False)
    if v >= 2:
        label(c, (mx, my + 52), "king of righteousness", 9.5, HL,
              italic=True)
        label(c, (mx, my + 68), "king of peace", 9.5, HL, italic=True)
    if v >= 3:
        # A life bar with no drawn ends: it runs off the frame on the left
        # and stops short of Abraham's on the right, where his own bar has
        # two ticks and a length.
        c.line((SX0 - 20, my + 96), (596, my + 96), dim(HL, 0.9), 3.0)
        arrow(c, (SX0 + 40, my + 96), (SX0 - 20, my + 96), dim(HL, 0.9),
              3.0, 9)
        arrow(c, (536, my + 96), (596, my + 96), dim(HL, 0.9), 3.0, 9)
        label(c, (SX0 + 6, my + 112), "no beginning of days", 9,
              dim(TEXT_DIM, 0.95), anchor="lm", italic=True)
        label(c, (594, my + 112), "no end of life", 9,
              dim(TEXT_DIM, 0.95), anchor="rm", italic=True)
        label(c, (mx, my - 62), "without father, without mother, "
              "without genealogy", 10, dim(SILVER, 0.95), italic=True)

    # Abraham, with a life that has two ends — and Levi still inside him.
    ax, ay = 760, 236
    _node(c, ax, ay, 170, 62, "ABRAHAM", dim(TEXT, 0.92),
          bar=(ax - 74, ax + 74))
    if v >= 4:
        label(c, (ax, ay + 66), "the patriarch", 9.5, dim(TEXT_DIM, 0.95),
              italic=True)
        arrow(c, (ax - 92, ay - 22), (mx + 102, ay - 22), dim(GOLD, 0.95),
              2.0, 8)
        label(c, (540, ay - 36), "A TENTH OF THE BEST PLUNDER", 9.5, GOLD,
              bold=True)
    if v >= 6:
        arrow(c, (mx + 102, ay + 18), (ax - 92, ay + 18), dim(HL, 0.9),
              2.0, 8)
        label(c, (540, ay + 34), "AND BLESSED HIM", 9.5, HL, bold=True)
    if v >= 7:
        c.line((SX0 + 40, 372), (SX1 - 40, 372), dim(SILVER, 0.7), 1.3,
               dash="6,5")
        label(c, (SX0 + 40, 386), "the lesser is blessed by the greater",
              9.5, dim(SILVER, 0.95), anchor="lm", italic=True)
    if v >= 8:                       # two receipt columns
        for i, (t, s) in enumerate((("HERE", "people who die receive tithes"),
                                    ("THERE", "one of whom it is testified "
                                     "that he lives"))):
            bx = 300 + i * 400
            c.rect(bx - 118, 410, 236, 62, fill=None,
                   stroke=dim(SILVER, 0.8) if i == 0 else dim(HL, 0.85),
                   width=1.5, rx=3)
            label(c, (bx, 426), t, 11, dim(TEXT, 0.9) if i == 0 else HL,
                  bold=True)
            label(c, (bx, 448), s, 8.5, dim(TEXT_DIM, 0.95), italic=True)
            if i == 0:
                for k in range(5):
                    c.line((bx - 96 + k * 48, 462), (bx - 76 + k * 48, 462),
                           dim(RED, 0.85), 2.0)
    if v >= 9:                       # Levi, still in the body of his father
        # Nested inside the node, below the name rather than over it: the
        # picture only works if you can still read whose body he is in.
        c.rect(ax - 50, ay + 8, 100, 28, fill=dim(PANEL, 0.95),
               stroke=dim(GOLD, 0.9), width=1.6, rx=3)
        label(c, (ax, ay + 22), "LEVI", 10.5, GOLD, bold=True)
        if v >= 10:
            label(c, (ax, ay + 96), "yet in the body of his father", 9.5,
                  GOLD, italic=True)
            label(c, (ax, ay + 112), "when Melchizedek met him", 9,
                  dim(TEXT_DIM, 0.95), italic=True)


def _ch7_change(c, v):
    label(c, (SX0 + 10, 116), "THE PRIESTHOOD BEING CHANGED", 16.5, TEXT,
          anchor="lm", bold=True)
    label(c, (SX0 + 10, 138), "there is of necessity a change made also "
          "in the law", 11.5, dim(TEXT_DIM, 0.95), anchor="lm", italic=True)

    # the twelve tribes as a row; only one column has ever carried an altar
    for i, t in enumerate(TRIBES12):
        bx = 132 + i * 72
        levi, judah = (t == "LEVI"), (t == "JUDAH")
        col = GOLD if levi else (HL if (judah and v >= 14)
                                 else dim(TEXT_DIM, 0.8))
        c.rect(bx, 218, 62, 40, fill=None, stroke=col, width=1.6, rx=2)
        c.text((bx + 31, 238), t, 7.5, col, "mm", bold=levi or judah)
        if levi:
            c.rect(bx + 14, 186, 34, 22, fill=None, stroke=GOLD, width=1.6)
            label(c, (bx + 31, 174), "altar", 8, GOLD, italic=True)
    if v >= 13:
        label(c, (132, 282), "he of whom these things are said belongs "
              "to another tribe", 9.5, dim(TEXT, 0.9), anchor="lm",
              italic=True)
    if v >= 14:
        bx = 132 + 3 * 72
        arrow(c, (bx + 31, 300), (bx + 31, 262), HL, 2.0, 8)
        label(c, (bx + 31, 316), "OUR LORD SPRANG OUT OF JUDAH", 9.5, HL,
              bold=True)
        label(c, (bx + 31, 332), "of which tribe Moses spoke nothing "
              "concerning priesthood", 8.5, dim(TEXT_DIM, 0.95), italic=True)
    if v >= 16:
        label(c, (132, 360), "not after a fleshly commandment, but after "
              "the power of an endless life", 9.5, HL, anchor="lm",
              italic=True)
    if v >= 18:                      # the foregoing commandment, struck out
        c.rect(132, 384, 300, 34, fill=None, stroke=dim(SILVER, 0.8),
               width=1.5, rx=3)
        label(c, (282, 401), "A FOREGOING COMMANDMENT", 9.5,
              dim(SILVER, 0.9), bold=True)
        c.line((126, 401), (438, 401), dim(RED, 0.9), 2.4)
        label(c, (132, 432), "weakness and uselessness — the law made "
              "nothing perfect", 9, dim(TEXT_DIM, 0.95), anchor="lm",
              italic=True)
    if v >= 19:
        arrow(c, (446, 401), (556, 401), HL, 2.0, 8)
        c.rect(566, 384, 300, 34, fill=None, stroke=HL, width=1.8, rx=3)
        label(c, (716, 401), "A BETTER HOPE", 11, HL, bold=True)
        label(c, (716, 432), "through which we draw near to God", 9.5, HL,
              italic=True)
    if v >= 20:                      # two appointments, one sealed
        for i, (t, sealed) in enumerate((("THEY", False), ("HE", True))):
            bx = 640 + i * 180
            c.rect(bx - 62, 190, 124, 74, fill=None,
                   stroke=HL if sealed else dim(SILVER, 0.75), width=1.6,
                   rx=3)
            for k in range(4):
                c.line((bx - 46, 208 + k * 12), (bx + 34, 208 + k * 12),
                       dim(SAND_DIM, 0.9), 1.1)
            label(c, (bx, 276), t, 10, HL if sealed else dim(TEXT_DIM, 0.9),
                  bold=True)
            if sealed:
                G.signet(c, bx + 42, 252, 15, GOLD, HL)
                label(c, (bx, 292), "with an oath", 9, HL, italic=True)
            else:
                label(c, (bx, 292), "without an oath", 9,
                      dim(TEXT_DIM, 0.95), italic=True)
    if v >= 21:
        label(c, (730, 312), "THE LORD SWORE AND WILL NOT CHANGE HIS MIND",
              9.5, HL, bold=True)
    if v >= 22:
        label(c, (730, 336), "the collateral of a better covenant", 10, HL,
              italic=True)


def _ch7_many(c, v):
    label(c, (SX0 + 10, 116), "MANY PRIESTS, AND ONE", 16.5, TEXT,
          anchor="lm", bold=True)
    label(c, (SX0 + 10, 138), "hindered from continuing by death", 11.5,
          dim(TEXT_DIM, 0.95), anchor="lm", italic=True)

    # A row that does not end on screen. The text gives no number, so the
    # drawing gives none.
    gy = 300
    for i in range(11):
        px = 140 + i * 62
        vested(c, px, gy, 78, ink=dim(SHADOW_LIT, 0.95), breastplate=False)
        c.line((px - 26, gy - 42), (px + 26, gy - 30), dim(RED, 0.85), 2.0)
    label(c, (SX1 - 200, gy - 12), "...", 20, dim(SHADOW_LIT, 0.9))
    label(c, (400, gy + 24), "MANY, BECAUSE THEY DIE", 11,
          dim(SHADOW_LIT, 0.95), bold=True)

    if v >= 24:
        vested(c, 880, gy, 104, ink=HL)
        label(c, (880, gy + 24), "ONE", 12, HL, bold=True)
        label(c, (880, gy + 42), "because he lives forever", 9.5, HL,
              italic=True)
    if v >= 25:                      # to the uttermost, drawn as reach
        c.line((880, gy - 116), (SX0 + 6, gy - 116), dim(HL, 0.9), 2.0)
        arrow(c, (300, gy - 116), (SX0 + 6, gy - 116), dim(HL, 0.9), 2.0, 8)
        engrave(c, 7, 25, v, (620, gy - 146), 18)
        label(c, (620, gy - 96), "he lives forever to make intercession "
              "for them", 9.5, HL, italic=True)
    if v >= 26:                      # five fitnesses
        for i, s in enumerate(("holy", "guiltless", "undefiled",
                               "separated from sinners",
                               "higher than the heavens")):
            if v < 26:
                break
            label(c, (140 + i * 176, 402), s.upper(), 9.5,
                  HL if i == 4 else dim(TEXT, 0.92), anchor="mm",
                  bold=i == 4)
    if v >= 27:
        label(c, (SX0 + 10, 440), "not daily, like those high priests —", 10,
              dim(TEXT_DIM, 0.95), anchor="lm", italic=True)
        label(c, (SX0 + 10, 458), "HE DID THIS ONCE FOR ALL, WHEN HE "
              "OFFERED UP HIMSELF", 11, HL, anchor="lm", bold=True)
    if v >= 28:
        label(c, (SX0 + 10, 484), "the law appoints men who have weakness; "
              "the word of the oath appoints a Son", 9.5,
              dim(TEXT, 0.9), anchor="lm", italic=True)


# ---------------------------------------------------------------------------
# Assemble one verse
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# 8 — the doubling declared
# ---------------------------------------------------------------------------
#
# The chapter that explains the frame. 8:5's "copy and shadow" is the whole
# design stated in the text, so this is where the projection lines are drawn
# and where the shadow's edges first begin to go.

COVENANT = [("laws into the mind, written on the heart", 10),
            ("I will be their God, they my people", 10),
            ("all will know me, from least to greatest", 11),
            ("I will remember their sins no more", 12)]


def ch8(c, cam, v, pos):
    fade = 1.0 if v < 13 else 0.55
    shadow(c, cam, upto=U_TOP, fade=fade, labels=v <= 5)
    substance(c, cam, seat=True, tent=v >= 2, light=v >= 5)

    if v == 1:
        label(c, (CX, cam.y(U_SEAT + 96)), "THE MAIN POINT", 12, HL,
              bold=True)
        label(c, (CX, cam.y(U_SEAT - 78)), "we have such a high priest, "
              "who sat down", 10, dim(TEXT, 0.9), italic=True)
    if v >= 2:
        label(c, (CX, cam.y(U_TRUE + 74)), "THE TRUE TABERNACLE", 10.5, HL,
              bold=True)
        if v == 2:
            label(c, (CX, cam.y(U_TRUE + 92)), "which the Lord pitched, "
                  "not man", 9.5, dim(TEXT_DIM, 0.95), italic=True)
    if v >= 3:
        label(c, (170, 200), "every high priest is appointed", 9.5,
              dim(TEXT_DIM, 0.95), anchor="lm", italic=True)
        label(c, (170, 216), "to offer gifts and sacrifices", 9.5,
              dim(TEXT_DIM, 0.95), anchor="lm", italic=True)
    if v >= 4:
        label(c, (170, 240), "if he were on earth,", 9.5,
              dim(SHADOW_LIT, 0.95), anchor="lm", italic=True)
        label(c, (170, 256), "he would not be a priest at all", 9.5,
              dim(SHADOW_LIT, 0.95), anchor="lm", italic=True)
    if v >= 5:
        engrave(c, 8, 5, v, (CX, cam.y(U_HEAVENS) - 4), 19)
        label(c, (CX, cam.y(U_HEAVENS) + 22), "according to the pattern "
              "shown to you on the mountain", 9.5, dim(GOLD, 0.95),
              italic=True)

    if v >= 6:                       # the new covenant, and the four terms
        for i, (s, at) in enumerate(COVENANT):
            if v < at:
                continue
            gy = 348 + i * 22
            c.circle(700, gy - 4, 4, fill=dim(HL, 0.9))
            label(c, (716, gy), s, 9.5, HL if at == v else
                  dim(TEXT_DIM, 0.95), anchor="lm", italic=True)
        label(c, (700, 326), "A NEW COVENANT, ON BETTER PROMISES", 10, HL,
              anchor="lm", bold=True)
    if v >= 8:                       # the longest quotation in the letter
        voice_arc(c, (640, SYT + 18), (700, 316), dim(HL, 0.9), 2.2,
                  bulge=0.20)
    if v >= 9:
        label(c, (170, 300), "not according to the covenant", 9.5,
              dim(SHADOW_LIT, 0.95), anchor="lm", italic=True)
        label(c, (170, 316), "I made with their fathers", 9.5,
              dim(SHADOW_LIT, 0.95), anchor="lm", italic=True)
    if v >= 10:                      # the tablets become a heart
        hx, hy = 250, 400
        if v == 10:
            c.rect(hx - 46, hy - 34, 40, 62, fill=None,
                   stroke=dim(SILVER, 0.8), width=1.6, rx=3)
            c.rect(hx + 6, hy - 34, 40, 62, fill=None,
                   stroke=dim(SILVER, 0.8), width=1.6, rx=3)
            arrow(c, (hx + 60, hy), (hx + 108, hy), HL, 2.0, 8)
        c.path(f"M{hx + 150},{hy + 26} q{-48},{-34} {-48},{-62} "
               f"q0,{-30} {48},{-14} q{48},{-16} {48},{14} "
               f"q0,{28} {-48},{62} z", fill=None, stroke=HL, width=2.0)
        label(c, (hx + 150, hy + 48), "ON THEIR HEART", 9.5, HL, bold=True)
    if v >= 12:                      # a record whose entries are absent
        c.rect(700, 430, 232, 62, fill=None, stroke=dim(SILVER, 0.75),
               width=1.5, rx=3)
        for k in range(3):
            c.line((716, 448 + k * 16), (740 + k * 8, 448 + k * 16),
                   dim(SILVER, 0.30), 1.2)
        engrave(c, 8, 12, v, (330, SYB - 22), 15)
    if v >= 13:                      # near to vanishing away
        label(c, (640, SYB - 30), "becoming old, and grows aged,", 9.5,
              dim(SHADOW_LIT, 0.9), anchor="lm", italic=True)
        label(c, (640, SYB - 14), "NEAR TO VANISHING AWAY", 10.5,
              dim(SHADOW_LIT, 0.95), anchor="lm", bold=True)


# ---------------------------------------------------------------------------
# 9 — the tabernacle in section
# ---------------------------------------------------------------------------
#
# Twenty-eight verses in one room, and chapter 10 adds thirty-nine more. The
# stagnation risk the Romans post-mortem documented lives here, so the
# chapter is built as five sub-scenes rather than one accumulating drawing.

FURNITURE = [("lampstand", 2, -110, U_HOLY + 44), ("table", 2, -30, U_HOLY + 44),
             ("show bread", 2, 52, U_HOLY + 44),
             ("altar of incense", 4, -60, U_VEIL + 22),
             ("the ark", 4, 30, U_VEIL + 22),
             ("mercy seat", 5, 30, U_VEIL + 50)]


def ch9(c, cam, v, pos):
    shadow(c, cam, upto=U_TOP, labels=v <= 5,
           opened=False, pierced=False)

    if v <= 5:                       # the rooms furnished, object per verse
        for name, at, dx, u in FURNITURE:
            if v < at:
                continue
            px, py = CX + dx, cam.y(u)
            hot = (at == v)
            c.rect(px - 26, py - 18, 52, 36, fill=dim(SHADOW, 0.8),
                   stroke=HL if hot else dim(GOLD, 0.75), width=1.6, rx=3)
            label(c, (px, py + 30), name, 8.5, HL if hot else
                  dim(TEXT_DIM, 0.95), italic=True)
        if v == 4:
            label(c, (820, 250), "a golden pot of manna,", 9.5,
                  dim(TEXT_DIM, 0.95), anchor="lm", italic=True)
            label(c, (820, 266), "Aaron's rod that budded,", 9.5,
                  dim(TEXT_DIM, 0.95), anchor="lm", italic=True)
            label(c, (820, 282), "the tablets of the covenant", 9.5,
                  dim(TEXT_DIM, 0.95), anchor="lm", italic=True)
        if v == 5:
            label(c, (820, 306), "of which we can't speak now in detail",
                  9.5, dim(TEXT, 0.9), anchor="lm", italic=True)
        label(c, (SX0 + 8, 130), "AN EARTHLY SANCTUARY", 13, TEXT,
              anchor="lm", bold=True)

    elif v <= 10:                    # the traffic diagram, and the block
        label(c, (SX0 + 8, 130), "WHO GOES IN, AND HOW OFTEN", 13, TEXT,
              anchor="lm", bold=True)
        y_h, y_m = cam.y(U_HOLY), cam.y(U_MOST)
        for k in range(9):           # continually: many worn paths
            c.path(f"M{300 + k * 6},{cam.y(U_COURT)} "
                   f"Q{CX - 60 + k * 5},{(y_h + cam.y(U_COURT)) / 2} "
                   f"{CX - 40 + k * 9},{y_h + 6}",
                   fill=None, stroke=dim(SHADOW_LIT, 0.55), width=1.4)
        label(c, (250, cam.y(U_HOLY) + 40), "THE PRIESTS, CONTINUALLY", 10,
              dim(SHADOW_LIT, 0.95), anchor="lm", bold=True)
        if v >= 7:                   # one thin dated path
            c.path(f"M{CX + 120},{cam.y(U_COURT)} Q{CX + 90},{y_h} "
                   f"{CX + 20},{y_m + 8}", fill=None, stroke=dim(HL, 0.9),
                   width=1.8)
            label(c, (CX + 150, cam.y(U_HOLY) + 8), "THE HIGH PRIEST ALONE",
                  10, HL, anchor="lm", bold=True)
            label(c, (CX + 150, cam.y(U_HOLY) + 24), "once in the year, "
                  "not without blood", 9, dim(BLOOD, 0.95), anchor="lm",
                  italic=True)
        if v >= 8:                   # the building is the obstruction
            c.line((CX - 190, cam.y(U_VEIL)), (CX + 190, cam.y(U_VEIL)),
                   dim(RED, 0.9), 4.0)
            label(c, (CX, cam.y(U_VEIL) - 24), "THE WAY NOT YET REVEALED",
                  10.5, dim(RED, 0.95), bold=True)
            label(c, (CX, cam.y(U_VEIL) - 8), "while the first tabernacle "
                  "was still standing", 9, dim(TEXT_DIM, 0.95), italic=True)
        if v >= 9:
            label(c, (SX0 + 8, 400), "incapable, concerning the conscience,",
                  9.5, dim(SHADOW_LIT, 0.95), anchor="lm", italic=True)
            label(c, (SX0 + 8, 416), "of making the worshiper perfect", 9.5,
                  dim(SHADOW_LIT, 0.95), anchor="lm", italic=True)
        if v >= 10:
            label(c, (SX0 + 8, 440), "imposed until a time of reformation",
                  9.5, HL, anchor="lm", italic=True)

    elif v <= 14:                    # the path relocates to the substance
        substance(c, cam, seat=True, tent=True)
        label(c, (SX0 + 8, 130), "A GREATER AND MORE PERFECT TABERNACLE",
              13, TEXT, anchor="lm", bold=True)
        label(c, (SX0 + 8, 152), "not made with hands, that is to say, "
              "not of this creation", 10.5, dim(TEXT_DIM, 0.95),
              anchor="lm", italic=True)
        c.path(f"M{CX - 140},{cam.y(U_COURT)} Q{CX - 40},{cam.y(U_HOLY)} "
               f"{CX},{cam.y(U_TRUE)}", fill=None, stroke=dim(HL, 0.95),
               width=2.6)
        if v >= 12:
            engrave(c, 9, 12, v, (CX + 210, cam.y(U_MOST)), 19)
            label(c, (CX + 210, cam.y(U_MOST) + 26), "through his own blood",
                  9.5, dim(BLOOD, 0.95), italic=True)
        if v >= 13:                  # two cleansings, outer and inner
            for i, (s, sub, col) in enumerate(
                    (("THE FLESH", "goats, bulls, the ashes of a heifer",
                      dim(SHADOW_LIT, 0.95)),
                     ("YOUR CONSCIENCE", "the blood of Christ", HL))):
                if v < 13 + i:
                    continue
                bx = 260 + i * 0
                c.circle(250, 400 + i * 74, 22 - i * 8, fill=None,
                         stroke=col, width=2.0)
                label(c, (286, 394 + i * 74), s, 10, col, anchor="lm",
                      bold=True)
                label(c, (286, 410 + i * 74), sub, 9,
                      dim(TEXT_DIM, 0.95), anchor="lm", italic=True)

    elif v <= 22:                    # the will, and the dedication in blood
        label(c, (SX0 + 8, 130), "WHERE A WILL IS, THERE MUST BE A DEATH",
              13, TEXT, anchor="lm", bold=True)
        c.rect(180, 180, 250, 150, fill=dim(PANEL, 0.9),
               stroke=dim(SAND, 0.9), width=1.8, rx=4)
        for k in range(6):
            c.line((202, 208 + k * 20), (408 - (k % 2) * 40, 208 + k * 20),
                   dim(SAND_DIM, 0.9), 1.2)
        label(c, (305, 350), "A LAST WILL AND TESTAMENT", 10,
              dim(TEXT, 0.92), bold=True)
        if v >= 17:
            G.signet(c, 400, 312, 18, dim(SILVER, 0.85),
                     dim(SILVER, 0.6) if v < 18 else HL)
            label(c, (305, 372), "never in force while he who made it lives",
                  9.5, dim(TEXT_DIM, 0.95), italic=True)
        if v >= 15:
            label(c, (SX0 + 8, 152), "the mediator of a new covenant", 10.5,
                  HL, anchor="lm", italic=True)
        if v >= 19:                  # the sprinkling, accumulating
            targets = [("the book", 560, 220), ("all the people", 700, 220),
                       ("the tabernacle", 560, 300),
                       ("the vessels", 700, 300)]
            n = {19: 2, 20: 2, 21: 4, 22: 4}[min(22, v)]
            for name, px, py in targets[:n]:
                c.rect(px - 54, py - 24, 108, 48, fill=None,
                       stroke=dim(SAND, 0.85), width=1.4, rx=3)
                label(c, (px, py + 38), name, 9, dim(TEXT_DIM, 0.95),
                      italic=True)
                for k in range(5):
                    c.circle(px - 36 + k * 18, py - 6 + (k % 2) * 12, 2.6,
                             fill=dim(BLOOD, 0.95))
            label(c, (630, 174), "BLOOD, WATER, SCARLET WOOL, HYSSOP", 10,
                  dim(BLOOD, 0.95), bold=True)
        if v >= 20:
            label(c, (630, 358), "THIS IS THE BLOOD OF THE COVENANT", 10.5,
                  HL, bold=True)
        if v >= 22:
            label(c, (630, 392), "apart from shedding of blood", 10,
                  dim(BLOOD, 0.95), bold=True)
            label(c, (630, 410), "there is no remission", 10,
                  dim(BLOOD, 0.95), bold=True)

    else:                            # vv23-28 — two tracks, and one 'once'
        substance(c, cam, seat=True, tent=True)
        label(c, (SX0 + 8, 130), "ONCE, AT THE END OF THE AGES", 13, TEXT,
              anchor="lm", bold=True)
        if v >= 24:
            label(c, (SX0 + 8, 152), "not into holy places made with hands, "
                  "but into heaven itself", 10.5, dim(TEXT_DIM, 0.95),
                  anchor="lm", italic=True)
        if v >= 25:
            label(c, (200, 226), "not year by year, with blood not his own",
                  9.5, dim(SHADOW_LIT, 0.95), anchor="lm", italic=True)
        if v >= 26:
            label(c, (200, 248), "he has been revealed to put away sin", 9.5,
                  HL, anchor="lm", italic=True)
            label(c, (200, 264), "BY THE SACRIFICE OF HIMSELF", 10.5, HL,
                  anchor="lm", bold=True)
        if v >= 27:                  # the parallel, drawn as two tracks
            for i, (a, b, col) in enumerate(
                    ((("MEN DIE ONCE", "AND AFTER THIS, JUDGMENT"),
                      None, dim(SHADOW_LIT, 0.95)),
                     (("CHRIST OFFERED ONCE", "AND WILL APPEAR "
                       "A SECOND TIME"), None, HL))):
                if v < 27 + i:
                    continue
                ty = 350 + i * 62
                c.line((220, ty), (880, ty), col, 1.8)
                c.circle(300, ty, 6, fill=col)
                c.circle(760, ty, 6, fill=None, stroke=col, width=2.0)
                label(c, (300, ty - 16), a[0], 10, col, bold=True)
                label(c, (760, ty - 16), a[1], 10, col, bold=True)
        if v >= 28:
            label(c, (760, 434), "without sin, to those who are "
                  "eagerly waiting", 9, dim(TEXT_DIM, 0.95), italic=True)


# ---------------------------------------------------------------------------
# 10 — the crossing
# ---------------------------------------------------------------------------
#
# Thirty-nine verses, six sub-scenes. The centre of it is vv11-12, which pays
# off an omission the frame has been carrying since 1:3: there is no seat
# anywhere below the veil, so the standing priests have nowhere to sit long
# before the text says one of them sat down.


def ch10(c, cam, v, pos):
    fade = 0.45 if v >= 18 else 0.75
    shadow(c, cam, upto=U_TOP, fade=fade, opened=v >= 20, veil=True)
    substance(c, cam, seat=True, tent=True)

    if v <= 4:                       # a cycle that never closes out
        label(c, (SX0 + 8, 130), "THE SAME SACRIFICES, YEAR BY YEAR", 13,
              TEXT, anchor="lm", bold=True)
        label(c, (SX0 + 8, 152), "a shadow of the good to come, "
              "not the very image", 10.5, dim(SHADOW_LIT, 0.95),
              anchor="lm", italic=True)
        ox, oy, r = 300, 300, 58
        c.circle(ox, oy, r, fill=None, stroke=dim(SHADOW_LIT, 0.85),
                 width=2.0)
        for k in range(8):
            a = k * math.pi / 4
            c.line((ox + math.cos(a) * (r - 8), oy + math.sin(a) * (r - 8)),
                   (ox + math.cos(a) * (r + 8), oy + math.sin(a) * (r + 8)),
                   dim(SHADOW_LIT, 0.7), 1.4)
        arrow(c, (ox + r - 4, oy + 22), (ox + r + 2, oy - 6),
              dim(SHADOW_LIT, 0.9), 1.8, 7)
        label(c, (ox, oy + 84), "CONTINUALLY", 10, dim(SHADOW_LIT, 0.95),
              bold=True)
        if v >= 3:                   # the reminder accumulates
            for k in range(min(9, (v - 2) * 4)):
                c.line((500 + k * 16, 340), (500 + k * 16, 300),
                       dim(BLOOD, 0.85), 2.4)
            label(c, (560, 364), "A YEARLY REMINDER OF SINS", 10,
                  dim(BLOOD, 0.95), anchor="lm", bold=True)
        if v >= 4:
            label(c, (560, 392), "it is impossible that the blood of bulls "
                  "and goats", 9.5, dim(TEXT_DIM, 0.95), anchor="lm",
                  italic=True)
            label(c, (560, 408), "should take away sins", 9.5,
                  dim(TEXT_DIM, 0.95), anchor="lm", italic=True)

    elif v <= 10:                    # the first taken away, the second set
        label(c, (SX0 + 8, 130), "A BODY YOU PREPARED FOR ME", 13, TEXT,
              anchor="lm", bold=True)
        voice_arc(c, (300, SYT + 26), (CX - 60, 250), dim(HL, 0.9), 2.0)
        label(c, (SX0 + 8, 152), "sacrifice and offering you didn't desire",
              10.5, dim(TEXT_DIM, 0.95), anchor="lm", italic=True)
        if v >= 7:
            label(c, (CX + 40, 250), "BEHOLD, I HAVE COME TO DO YOUR WILL",
                  11, HL, anchor="lm", bold=True)
            label(c, (CX + 40, 268), "in the scroll of the book it is "
                  "written of me", 9, dim(TEXT_DIM, 0.95), anchor="lm",
                  italic=True)
        if v >= 9:                   # lifted out, and set in its place
            c.rect(240, 330, 210, 70, fill=None,
                   stroke=dim(SHADOW_LIT, 0.8), width=1.5, rx=3)
            label(c, (345, 365), "THE FIRST", 10.5, dim(SHADOW_LIT, 0.95),
                  bold=True)
            arrow(c, (462, 365), (552, 365), HL, 2.0, 8)
            c.line((234, 365), (456, 365), dim(RED, 0.85), 2.2)
            c.rect(566, 330, 210, 70, fill=None, stroke=HL, width=1.8, rx=3)
            label(c, (671, 365), "THE SECOND", 10.5, HL, bold=True)
            label(c, (508, 420), "he takes away the first, that he may "
                  "establish the second", 9.5, dim(TEXT, 0.9), italic=True)
        if v >= 10:
            label(c, (508, 448), "THROUGH THE OFFERING OF THE BODY OF "
                  "JESUS CHRIST, ONCE FOR ALL", 10, HL, bold=True)

    elif v <= 14:                    # the seated priest
        label(c, (SX0 + 8, 130), "EVERY PRIEST STANDS", 13, TEXT,
              anchor="lm", bold=True)
        label(c, (SX0 + 8, 152), "day by day, serving and often offering "
              "the same sacrifices", 10.5, dim(SHADOW_LIT, 0.95),
              anchor="lm", italic=True)
        gy = cam.y(U_HOLY) + 30
        for k in range(7):
            px = 160 + k * 62
            vested(c, px, gy, 74, ink=dim(SHADOW_LIT, 0.95),
                   breastplate=False)
            c.line((px - 16, gy + 8), (px + 16, gy + 8),
                   dim(SHADOW_LIT, 0.7), 1.2)
        label(c, (350, gy + 28), "WHICH CAN NEVER TAKE AWAY SINS", 10,
              dim(SHADOW_LIT, 0.95), bold=True)
        label(c, (350, gy + 46), "and no seat anywhere in this house", 9,
              dim(TEXT_DIM, 0.95), italic=True)
        if v >= 12:                  # but he, when he had offered one
            engrave(c, 10, 12, v, (760, cam.y(U_SEAT) - 66), 20)
            label(c, (760, cam.y(U_SEAT) + 62), "ONE SACRIFICE FOR SINS "
                  "FOREVER", 10, HL, bold=True)
        if v >= 13:                  # the footstool of 1:13, now placed
            fy = cam.y(U_SEAT - 78)
            c.rect(CX - 54, fy, 108, 17, fill=dim(GOLD, 0.32), stroke=GOLD,
                   width=1.6, rx=3)
            label(c, (CX, fy + 32), "HIS ENEMIES, A FOOTSTOOL", 9.5,
                  dim(TEXT, 0.9))
        if v >= 14:
            label(c, (760, cam.y(U_SEAT) + 84), "he has perfected forever "
                  "those who are being sanctified", 9,
                  dim(TEXT_DIM, 0.95), italic=True)

    elif v <= 18:                    # nothing new is written
        label(c, (SX0 + 8, 130), "I WILL REMEMBER THEIR SINS NO MORE", 13,
              TEXT, anchor="lm", bold=True)
        label(c, (SX0 + 8, 152), "the covenant of 8:12, already on "
              "the stone", 10.5, dim(TEXT_DIM, 0.95), anchor="lm",
              italic=True)
        c.rect(300, 210, 420, 96, fill=dim(PANEL, 0.9),
               stroke=dim(SAND, 0.85), width=1.8, rx=4)
        label(c, (510, 246), "ON THEIR HEART, ON THEIR MIND", 11,
              dim(TEXT, 0.92), bold=True)
        label(c, (510, 276), "THEIR SINS AND INIQUITIES NO MORE", 11,
              dim(TEXT, 0.92), bold=True)
        if v >= 18:                  # the altar goes out
            ax_, ay_ = CX, cam.y(U_COURT) - 26
            c.rect(ax_ - 52, ay_, 104, 34, fill=None,
                   stroke=dim(SHADOW_LIT, 0.7), width=1.6)
            cross(c, ax_, ay_ + 17, 16, dim(RED, 0.9), 2.4)
            label(c, (ax_, ay_ + 52), "NO MORE OFFERING FOR SIN", 10.5,
                  dim(RED, 0.95), bold=True)

    elif v <= 25:                    # the crossing, and the three 'let us'
        label(c, (SX0 + 8, 130), "BOLDNESS TO ENTER", 13, TEXT, anchor="lm",
              bold=True)
        engrave(c, 10, 20, v, (CX, cam.y(U_VEIL) - 30), 19)
        c.line((CX, cam.y(U_COURT)), (CX, cam.y(U_MOST)), dim(HL, 0.95), 2.6)
        arrow(c, (CX, cam.y(U_VEIL)), (CX, cam.y(U_MOST)), dim(HL, 0.95),
              2.6, 9)
        label(c, (CX + 150, cam.y(U_VEIL) + 26), "through the veil,", 9.5,
              HL, anchor="lm", italic=True)
        label(c, (CX + 150, cam.y(U_VEIL) + 42), "that is to say, his flesh",
              9.5, HL, anchor="lm", italic=True)
        if v >= 21:
            label(c, (SX0 + 8, 152), "and having a great priest over "
                  "God's house", 10.5, dim(TEXT_DIM, 0.95), anchor="lm",
                  italic=True)
        if v >= 22:                  # several, not one
            for i, (s, at) in enumerate((("DRAW NEAR", 22),
                                         ("HOLD FAST", 23),
                                         ("CONSIDER ONE ANOTHER", 24))):
                if v < at:
                    continue
                px = 230 + i * 76
                figure(c, px, cam.y(U_COURT) + 18, 48,
                       HL if at == v else dim(SAND, 0.9))
                label(c, (px, cam.y(U_COURT) - 46 - i * 15), s, 9,
                      HL if at == v else dim(TEXT_DIM, 0.95), bold=at == v)
        if v >= 25:
            label(c, (830, 230), "not forsaking our own", 9.5, HL,
                  anchor="lm", italic=True)
            label(c, (830, 246), "assembling together", 9.5, HL,
                  anchor="lm", italic=True)
            c.circle(900, 300, 34, fill=None, stroke=dim(GOLD, 0.5),
                     width=1.6)
            label(c, (900, 348), "AS YOU SEE THE DAY APPROACHING", 9.5, HL,
                  bold=True)

    elif v <= 31:                    # the fourth warning, and the floor
        label(c, (SX0 + 8, 130), "IF WE SIN WILLFULLY", 13, TEXT,
              anchor="lm", bold=True)
        label(c, (SX0 + 8, 152), "there remains no more a sacrifice "
              "for sins", 10.5, dim(RED, 0.95), anchor="lm", italic=True)
        fy = 450
        hatch(c, 240, fy, 864, fy + 66, dim(FIRE, 0.55), step=15)
        c.line((240, fy), (864, fy), dim(RED, 0.9), 2.4)
        label(c, (552, fy + 82), "A FIERCENESS OF FIRE", 11,
              dim(FIRE, 0.95), bold=True)
        if v >= 28:                  # the severity comparison
            c.line((300, 250), (500, 250), dim(SHADOW_LIT, 0.9), 2.0)
            label(c, (300, 234), "MOSES' LAW: TWO OR THREE WITNESSES", 9.5,
                  dim(SHADOW_LIT, 0.95), anchor="lm", bold=True)
        if v >= 29:
            c.line((300, 300), (830, 300), dim(RED, 0.9), 3.0)
            label(c, (300, 284), "HOW MUCH WORSE PUNISHMENT", 10.5,
                  dim(RED, 0.95), anchor="lm", bold=True)
            for i, s in enumerate(("trodden under foot the Son of God",
                                   "counted the blood an unholy thing",
                                   "insulted the Spirit of grace")):
                label(c, (300, 318 + i * 16), s, 9,
                      dim(TEXT_DIM, 0.95), anchor="lm", italic=True)
        if v >= 31:
            engrave(c, 10, 31, v, (CX, 386), 19)

    else:                            # vv32-39 — the ledger, and two paths
        label(c, (SX0 + 8, 130), "REMEMBER THE FORMER DAYS", 13, TEXT,
              anchor="lm", bold=True)
        for i, (s, at) in enumerate((("reproaches and oppressions", 33),
                                     ("partakers with those so treated", 33),
                                     ("compassion on me in my chains", 34),
                                     ("the plundering of your possessions",
                                      34))):
            if v < at:
                continue
            label(c, (200, 200 + i * 19), s, 9.5, dim(SHADOW_LIT, 0.95),
                  anchor="lm", italic=True)
        if v >= 32:
            label(c, (200, 178), "a great struggle with sufferings", 10,
                  dim(SHADOW_LIT, 0.95), anchor="lm", bold=True)
        if v >= 34:
            arrow(c, (560, 220), (640, 220), HL, 2.0, 8)
            label(c, (660, 206), "A BETTER POSSESSION", 11, HL, anchor="lm",
                  bold=True)
            label(c, (660, 224), "and an enduring one, in the heavens", 9.5,
                  HL, anchor="lm", italic=True)
        if v >= 35:
            label(c, (200, 300), "don't throw away your boldness", 10, HL,
                  anchor="lm", italic=True)
        if v >= 36:
            label(c, (200, 318), "you need endurance", 10, HL, anchor="lm",
                  italic=True)
        if v >= 37:
            c.circle(880, 244, 30, fill=None, stroke=dim(GOLD, 0.55),
                     width=1.6)
            label(c, (880, 288), "IN A VERY LITTLE WHILE", 9.5, HL,
                  bold=True)
            label(c, (880, 304), "he who comes will come", 9,
                  dim(TEXT_DIM, 0.95), italic=True)
        if v >= 38:                  # two paths out of one point
            px, py = 400, 400
            c.line((300, py), (px, py), dim(SAND, 0.9), 2.0)
            c.polyline([(px, py), (600, py - 40), (760, py - 56)],
                       HL, 2.4)
            c.polyline([(px, py), (600, py + 44), (700, py + 60)],
                       dim(RED, 0.85), 2.0, dash="6,5")
            label(c, (770, py - 60), "FAITH, TO THE SAVING OF THE SOUL",
                  10, HL, anchor="lm", bold=True)
            label(c, (710, py + 64), "shrink back to destruction", 9.5,
                  dim(RED, 0.95), anchor="lm", italic=True)
        if v >= 39:
            figure(c, 690, 348, 44, HL)
            label(c, (200, 460), "BUT WE ARE NOT OF THOSE WHO SHRINK BACK",
                  11, HL, anchor="lm", bold=True)


# ---------------------------------------------------------------------------
# 11 and 12 — break-away: the road, the race, the two mountains
# ---------------------------------------------------------------------------
#
# One drawing across two chapters. The pilgrims walk toward a city that is
# the top of this same column seen from outside, and none of them reach it
# (11:39); the gap becomes the track at 12:1, and 12:2's "looking to Jesus
# ... has sat down" lands the road's sightline on the seat drawn at 1:3.

ROAD_Y = 430
CITY_X = 916


def city(c, lit=1.0, label_on=True, arrived=False):
    """The city which has the foundations, on the horizon. Drawn solid while
    the road is still short — 11:16, "he has prepared a city for them"."""
    base = ROAD_Y - 6
    for i, (dx, w, h) in enumerate(((-52, 34, 74), (-14, 30, 104),
                                    (22, 26, 86), (54, 30, 62))):
        c.rect(CITY_X + dx, base - h, w, h, fill=dim(CITY, 0.18 * lit),
               stroke=dim(CITY, 0.92 * lit), width=1.6)
    c.line((CITY_X - 62, base), (CITY_X + 92, base), dim(CITY, 0.92 * lit),
           2.0)
    if arrived:
        c.rect(CITY_X - 20, base - 40, 32, 40, fill=dim(GOLD, 0.42),
               stroke=HL, width=2.0)
    if label_on:
        c.text((CITY_X + 14, base + 20), "THE CITY", 10,
               dim(CITY, 0.95 * lit), "mm", bold=True)


def road(c, upto_x, underground=False, gap=False):
    """The road the pilgrims walk. `underground` drops it below the world's
    line for 11:35b-38; `gap` leaves 11:39's shortfall visible."""
    end = min(upto_x, CITY_X - 96) if gap else upto_x
    c.line((150, ROAD_Y), (end, ROAD_Y), dim(SAND, 0.9), 2.2)
    if gap:
        c.line((end, ROAD_Y), (CITY_X - 66, ROAD_Y), dim(SAND, 0.35), 1.6,
               dash="6,6")
    if underground:
        c.polyline([(560, ROAD_Y), (600, ROAD_Y + 56), (700, ROAD_Y + 62),
                    (742, ROAD_Y + 10)], dim(SAND, 0.85), 2.0)
        hatch(c, 560, ROAD_Y + 8, 742, ROAD_Y + 66, dim(SHADOW_LIT, 0.4),
              step=13)


WITNESSES = [("ABEL", 4, 190), ("ENOCH", 5, 250), ("NOAH", 7, 310),
             ("ABRAHAM", 8, 372), ("SARAH", 11, 434), ("ISAAC", 20, 496),
             ("JACOB", 21, 552), ("JOSEPH", 22, 608), ("MOSES", 23, 668),
             ("RAHAB", 31, 730)]


def ch11(c, cam, v, pos):
    label(c, (SX0 + 8, 122), "FAITH", 17, TEXT, anchor="lm", bold=True)
    label(c, (SX0 + 8, 144), "assurance of things hoped for, "
          "proof of things not seen", 11, dim(TEXT_DIM, 0.95), anchor="lm",
          italic=True)
    c.line((SX0, ROAD_Y + 84), (SX1, ROAD_Y + 84), dim(SHADOW_LIT, 0.55),
           1.3)                                        # the world's line

    walked = 150 + min(1.0, v / 33.0) * (CITY_X - 96 - 150)
    city(c, lit=1.0)
    road(c, walked, underground=v >= 35, gap=v >= 39)

    for name, at, px in WITNESSES:
        if v < at or px > walked + 40:
            continue
        hot = (at == v)
        figure(c, px, ROAD_Y, 44 if not hot else 52,
               HL if hot else dim(SAND, 0.92),
               pose="walk" if name not in ("ISAAC", "JACOB", "JOSEPH")
               else "kneel")
        c.text((px, ROAD_Y + 16), name, 8.5,
               HL if hot else dim(TEXT_DIM, 0.95), "mm", bold=hot)
    if v >= 5:                       # Enoch alone leaves the road upward
        arrow(c, (250, ROAD_Y - 54), (250, 250), dim(HL, 0.85), 1.8, 8)
        label(c, (250, 236), "taken away", 9, HL, italic=True)
    if v >= 4:                       # Abel, dead, still speaks
        voice_arc(c, (190, ROAD_Y + 20), (320, 254), dim(HL, 0.7), 1.6,
                  bulge=0.30)
        label(c, (328, 250), "being dead, he still speaks", 9, HL,
              anchor="lm", italic=True)
    if v >= 10:
        engrave(c, 11, 10, v, (CITY_X - 130, 210), 15)
    if 13 <= v <= 16:                # the sightline every one of them holds
        for _n, at, px in WITNESSES:
            if v < at or px > walked:
                continue
            c.line((px, ROAD_Y - 40), (CITY_X - 70, ROAD_Y - 70),
                   dim(CITY, 0.30), 1.1)
        label(c, (SX0 + 8, 176), "having seen them and embraced them "
              "from afar", 10, HL, anchor="lm", italic=True)
        if v >= 14:
            label(c, (SX0 + 8, 194), "strangers and pilgrims on the earth",
                  9.5, dim(TEXT_DIM, 0.95), anchor="lm", italic=True)
        if v >= 15:                  # the road back, unused
            c.line((150, ROAD_Y + 34), (420, ROAD_Y + 34),
                   dim(SAND_DIM, 0.85), 1.4, dash="6,6")
            arrow(c, (300, ROAD_Y + 34), (152, ROAD_Y + 34),
                  dim(SAND_DIM, 0.85), 1.4, 7)
            label(c, (430, ROAD_Y + 34), "they would have had time "
                  "to return", 9, dim(TEXT_DIM, 0.9), anchor="lm",
                  italic=True)
        if v >= 16:
            engrave(c, 11, 16, v, (620, 152), 17)
    if v >= 26:                      # Moses weighs, and weighs it right
        # The verse puts Christ into Moses' scale itself — "the reproach of
        # Christ ... greater riches than the treasures of Egypt" — so the
        # cross in that pan is the text's own move, not the drawing's.
        balance(c, 690, 342, 148,
                (F.coins(n=5), "TREASURES OF EGYPT"),
                (F.cross(), "THE REPROACH OF CHRIST"), heavy=1)
        c.line((668, ROAD_Y - 50), (690, 346), dim(SAND_DIM, 0.9), 1.1,
               dash="4,4")
        label(c, (690, 176), "ACCOUNTING IT GREATER RICHES", 9.5, HL,
              bold=True)
    if v >= 32:                      # the road crowds, for one verse
        for i, nm in enumerate(("GIDEON", "BARAK", "SAMSON", "JEPHTHAH",
                                "DAVID", "SAMUEL")):
            px = 552 + i * 32
            figure(c, px, ROAD_Y, 34, dim(SAND, 0.9), pose="walk")
        label(c, (632, ROAD_Y - 62), "THE TIME WOULD FAIL ME", 10, HL,
              bold=True)
    if 33 <= v <= 34:
        for i, s in enumerate(("subdued kingdoms", "stopped lions' mouths",
                               "quenched the power of fire",
                               "from weakness were made strong")):
            if v < 33 + (i // 2):
                continue
            label(c, (SX0 + 8, 300 + i * 17), s, 9.5, HL, anchor="lm",
                  italic=True)
    if v >= 35:                      # the turn: others, and the ground opens
        for i, s in enumerate(("tortured, not accepting deliverance",
                               "mocking and scourging, bonds and prison",
                               "stoned, sawn apart, slain with the sword",
                               "in sheep skins and in goat skins")):
            if v < 35 + i:
                continue
            label(c, (SX0 + 8, 300 + i * 17), s, 9.5,
                  dim(SHADOW_LIT, 0.95), anchor="lm", italic=True)
        for k in range(3):
            figure(c, 596 + k * 46, ROAD_Y + 56, 32,
                   dim(SHADOW_LIT, 0.9), pose="kneel")
    if v >= 38:                      # the world's line, below them
        label(c, (650, ROAD_Y + 100), "deserts, mountains, caves, "
              "and the holes of the earth", 9, dim(TEXT_DIM, 0.95),
              italic=True)
        engrave(c, 11, 38, v, (760, 500), 16)
    if v >= 39:                      # the road stops short, visibly
        label(c, (CITY_X - 176, ROAD_Y - 22), "did not receive the promise",
              9.5, dim(TEXT_DIM, 0.95), anchor="mm", italic=True)
    if v >= 40:
        label(c, (SX0 + 8, 490), "GOD HAVING PROVIDED SOME BETTER THING "
              "CONCERNING US", 11, HL, anchor="lm", bold=True)
        label(c, (SX0 + 8, 510), "that apart from us they should not "
              "be made perfect", 9.5, dim(TEXT_DIM, 0.95), anchor="lm",
              italic=True)


# Seven items a side, each pinned to the verse that names it. Arithmetic
# gating put three of Zion's seven past v24, where this section ends, so
# they never appeared at all — the verses are listed instead.
MOUNTAIN_L = [("a mountain that might be touched", 18), ("burned with fire", 18),
              ("blackness, darkness, storm", 18), ("the sound of a trumpet", 19),
              ("the voice of words", 19), ("if even an animal touches it", 20),
              ("I am terrified and trembling", 21)]
MOUNTAIN_R = [("Mount Zion, the city of the living God", 22),
              ("the heavenly Jerusalem", 22),
              ("innumerable multitudes of angels", 22),
              ("the festal gathering of the firstborn", 23),
              ("God the Judge of all", 23),
              ("the spirits of just men made perfect", 23),
              ("Jesus, the mediator of a new covenant", 24)]


def ch12(c, cam, v, pos):
    if v <= 17:
        _ch12_race(c, v)
    elif v <= 24:
        _ch12_mountains(c, v)
    else:
        _ch12_shaking(c, cam, v)


def _ch12_race(c, v):
    label(c, (SX0 + 8, 122), "THE RACE SET BEFORE US", 17, TEXT,
          anchor="lm", bold=True)
    city(c, lit=0.85)
    # The gap of 11:39 has become the track; the pilgrims are now the verges.
    c.line((150, ROAD_Y), (CITY_X - 66, ROAD_Y), dim(HL, 0.9), 2.6)
    for i, (_n, _at, px) in enumerate(WITNESSES):
        for sy in (-1, 1):
            figure(c, px, ROAD_Y + sy * 62, 34, dim(SAND, 0.55),
                   pose="stand")
    label(c, (400, ROAD_Y - 84), "SO GREAT A CLOUD OF WITNESSES", 10.5,
          dim(TEXT, 0.9), bold=True)
    if v == 1:
        engrave(c, 12, 1, v, (400, 200), 18)
        for k, s in enumerate(("EVERY WEIGHT", "THE SIN THAT ENTANGLES")):
            c.circle(250 + k * 120, ROAD_Y + 30, 9, fill=None,
                     stroke=dim(RED, 0.85), width=1.8)
            label(c, (250 + k * 120, ROAD_Y + 48), s, 8.5,
                  dim(RED, 0.95), bold=True)
    figure(c, 300, ROAD_Y, 54, HL, pose="walk")
    if v >= 2:                       # the sightline lands on the seat
        c.line((320, ROAD_Y - 46), (CITY_X - 40, 168), dim(HL, 0.75), 1.4)
        c.polygon([(CITY_X - 74, 168), (CITY_X - 6, 168),
                   (CITY_X - 6, 196), (CITY_X - 74, 196)],
                  fill=dim(GOLD, 0.42), stroke=GOLD, width=2.0)
        c.polygon([(CITY_X - 66, 168), (CITY_X - 14, 168),
                   (CITY_X - 14, 128), (CITY_X - 66, 128)],
                  fill=dim(GOLD, 0.16), stroke=GOLD, width=1.8)
        label(c, (CITY_X - 40, 214), "HAS SAT DOWN", 9.5, HL, bold=True)
        if v == 2:
            engrave(c, 12, 2, v, (400, 236), 18)
    if v >= 3:
        label(c, (SX0 + 8, 152), "consider him who has endured such "
              "contradiction", 10, dim(TEXT_DIM, 0.95), anchor="lm",
              italic=True)
    if v >= 4:                       # how far the striving has gone
        c.line((300, ROAD_Y + 96), (300, ROAD_Y + 116), dim(SAND, 0.9), 2.0)
        c.line((300, ROAD_Y + 106), (700, ROAD_Y + 106), dim(SAND, 0.6),
               1.4, dash="6,5")
        c.line((700, ROAD_Y + 96), (700, ROAD_Y + 116), dim(BLOOD, 0.9), 2.4)
        label(c, (700, ROAD_Y + 132), "TO BLOOD", 9.5, dim(BLOOD, 0.95),
              bold=True)
        label(c, (300, ROAD_Y + 132), "not yet", 9.5, dim(TEXT_DIM, 0.95),
              italic=True)
    if 5 <= v <= 11:                 # chastening: two ledgers, one short
        for i, (t, s, col, at) in enumerate(
                (("THE FATHERS OF OUR FLESH", "for a few days, "
                  "as seemed good to them", dim(SHADOW_LIT, 0.95), 9),
                 ("THE FATHER OF SPIRITS", "for our profit, that we may be "
                  "partakers of his holiness", HL, 10))):
            if v < at:
                continue
            label(c, (SX0 + 8, 190 + i * 40), t, 10.5, col, anchor="lm",
                  bold=True)
            label(c, (SX0 + 8, 208 + i * 40), s, 9, dim(TEXT_DIM, 0.95),
                  anchor="lm", italic=True)
        if v >= 6:
            label(c, (SX0 + 8, 170), "whom the Lord loves, he chastens",
                  10, HL, anchor="lm", italic=True)
        if v >= 11:                  # now, and afterward
            for i, (s, col) in enumerate((("NOT JOYOUS BUT GRIEVOUS",
                                           dim(SHADOW_LIT, 0.95)),
                                          ("THE PEACEFUL FRUIT OF "
                                           "RIGHTEOUSNESS", HL))):
                bx = 560 + i * 210
                c.rect(bx - 96, 264, 192, 46, fill=None, stroke=col,
                       width=1.5, rx=3)
                label(c, (bx, 287), s, 8.5, col, bold=True)
            arrow(c, (568, 336), (692, 336), HL, 1.8, 7)
            label(c, (630, 352), "afterward", 9, HL, italic=True)
    if v >= 12:
        label(c, (SX0 + 8, 300), "lift up the hands that hang down "
              "and the feeble knees", 9.5, HL, anchor="lm", italic=True)
    if v >= 13:
        label(c, (SX0 + 8, 318), "make straight paths for your feet", 9.5,
              HL, anchor="lm", italic=True)
    if v >= 15:                      # a root, under the track
        c.path(f"M420,{ROAD_Y + 8} q40,40 130,30 q-70,26 -150,-6",
               fill=None, stroke=dim(RED, 0.85), width=1.8)
        label(c, (500, ROAD_Y + 70), "A ROOT OF BITTERNESS", 9.5,
              dim(RED, 0.95), bold=True)
    if v >= 16:                      # Esau, on the same scale, weighed wrong
        balance(c, 700, 306, 128,
                (F.bread(), "ONE MEAL"),
                (F.scroll(), "HIS BIRTHRIGHT"), heavy=-1,
                warm=dim(RED, 0.95), cold=dim(SHADOW_LIT, 0.9))
        label(c, (700, 158), "ESAU SOLD HIS BIRTHRIGHT", 9.5,
              dim(RED, 0.95), bold=True)
    if v >= 17:
        label(c, (760, ROAD_Y - 30), "no place for a "
              "change of mind, though he sought it with tears", 8.5,
              dim(TEXT_DIM, 0.95), italic=True)


def _ch12_mountains(c, v):
    label(c, (SX0 + 8, 122), "TWO MOUNTAINS", 17, TEXT, anchor="lm",
          bold=True)
    for side, items, at0, col, name in (
            (-1, MOUNTAIN_L, 18, dim(FIRE, 0.95), "SINAI"),
            (1, MOUNTAIN_R, 22, dim(CITY, 0.95), "ZION")):
        bx = CX + side * 250
        if v < at0:
            continue
        c.polygon([(bx - 190, 470), (bx, 210), (bx + 190, 470)],
                  fill=dim(BROWN if side < 0 else CITY, 0.14),
                  stroke=col, width=2.0)
        label(c, (bx, 492), name, 13, col, bold=True)
        for i, (txt, at) in enumerate(items):
            if v < at:
                continue
            hot = (v == at)
            label(c, (bx, 250 + i * 30), txt, 8.5, HL if hot else col,
                  bold=hot)
    if v >= 18:
        label(c, (SX0 + 8, 144), "you have NOT come to a mountain that "
              "might be touched", 10.5, dim(FIRE, 0.95), anchor="lm",
              italic=True)
    if v >= 22:
        label(c, (SX0 + 8, 164), "BUT YOU HAVE COME TO MOUNT ZION", 11, HL,
              anchor="lm", bold=True)
    if v >= 24:                      # Abel's arc from 11:4, answered
        voice_arc(c, (CX - 250, 480), (CX + 250, 480), dim(HL, 0.85), 1.8,
                  bulge=0.16)
        label(c, (CX, 528), "THE BLOOD OF SPRINKLING THAT SPEAKS "
              "BETTER THAN ABEL", 10, HL, bold=True)


def _ch12_shaking(c, cam, v):
    # The frame resolves. From v27 the shadow is not drawn at all.
    fade = 0.5 if v < 27 else 0.0
    shadow(c, cam, upto=U_TOP, fade=fade)
    substance(c, cam, seat=True, tent=True)
    label(c, (SX0 + 8, 122), "YET ONCE MORE", 17, TEXT, anchor="lm",
          bold=True)
    if v == 25:                      # the arc turned away
        voice_arc(c, (300, SYT + 26), (300, 300), dim(HL, 0.85), 2.0,
                  refused=True)
        label(c, (322, 300), "don't refuse him who speaks", 10, HL,
              anchor="lm", italic=True)
    if v >= 26:
        label(c, (SX0 + 8, 148), "I will shake not only the earth, "
              "but also the heavens", 10.5, dim(TEXT_DIM, 0.95),
              anchor="lm", italic=True)
        for k in range(5):
            c.line((200 + k * 20, 380), (208 + k * 20, 420),
                   dim(FIRE, 0.7), 1.6)
    if v >= 27:
        label(c, (SX0 + 8, 176), "THE REMOVING OF THOSE THINGS "
              "THAT ARE SHAKEN", 11, HL, anchor="lm", bold=True)
        label(c, (SX0 + 8, 196), "that those which are not shaken "
              "may remain", 9.5, HL, anchor="lm", italic=True)
    if v >= 28:
        engrave(c, 12, 28, v, (CX, SYB - 40), 19)
    if v >= 29:                      # the fire of v18, now on this side
        for k, fx in enumerate((360, 460, 640, 740)):
            c.path(f"M{fx},{SYB - 6} q{-11},{-17} {4},{-33} "
                   f"q{9},{16} {16},{25} q{-5},{-17} {0},{-27} "
                   f"q{13},{22} {2},{35} z", fill=dim(FIRE, 0.85))
        label(c, (CX, SYB + 14), "OUR GOD IS A CONSUMING FIRE", 11,
              dim(FIRE, 0.95), bold=True)


# ---------------------------------------------------------------------------
# 13 — outside the gate
# ---------------------------------------------------------------------------
#
# The reversal. Twelve chapters climb; this one deliberately goes back down
# and out, because the altar moved — and 13:14 gives the reason, so the book
# ends walking rather than arrived.


def ch13(c, cam, v, pos):
    shadow(c, cam, upto=U_TOP, fade=0.0)     # shaken off at 12:27, and gone
    substance(c, cam, seat=v <= 8, tent=v <= 8)
    y_camp = cam.y(U_CAMP)
    c.line((SX0, y_camp), (SX1, y_camp), dim(SHADOW_LIT, 0.8), 1.8)
    label(c, (SX0 + 8, y_camp - 12), "THE CAMP", 9.5,
          dim(SHADOW_LIT, 0.95), anchor="lm", bold=True)

    if v <= 8:                       # the settled community, at the foot
        for i, (s, at) in enumerate((("brotherly love", 1),
                                     ("hospitality to strangers", 2),
                                     ("those who are in bonds", 3),
                                     ("marriage held in honor", 4),
                                     ("free from the love of money", 5))):
            if v < at:
                continue
            label(c, (SX0 + 8, 168 + i * 19), s, 9.5,
                  HL if at == v else dim(TEXT_DIM, 0.95), anchor="lm",
                  italic=True)
        gy = y_camp - 4
        if v >= 2:                   # an angel at the table, unmarked
            for k, px in enumerate((420, 470, 560)):
                figure(c, px, gy, 46, dim(SAND, 0.92)
                       if k != 2 else dim(SAND, 0.92))
            c.line((400, gy - 52), (580, gy - 52), dim(SAND, 0.9), 2.0)
        if v >= 3:
            for px in (660, 700):
                figure(c, px, gy, 46, dim(SHADOW_LIT, 0.9))
            c.line((644, gy - 30), (716, gy - 30), dim(SILVER, 0.9), 2.4)
        if v >= 5:                   # a voice arc that simply stays
            voice_arc(c, (300, SYT + 40), (300, gy - 80), dim(HL, 0.9), 2.0)
            label(c, (312, gy - 92), "I WILL IN NO WAY LEAVE YOU", 10, HL,
                  anchor="lm", bold=True)
        if v >= 6:
            label(c, (312, gy - 74), "the Lord is my helper; I will not fear",
                  9.5, HL, anchor="lm", italic=True)
        if v >= 7:
            label(c, (SX0 + 8, 280), "remember your leaders — imitate "
                  "their faith", 9.5, dim(TEXT, 0.9), anchor="lm",
                  italic=True)
        if v >= 8:                   # the seat, unaltered since 1:3
            engrave(c, 13, 8, v, (CX, cam.y(U_SEAT) - 74), 16)
            c.line((CX, cam.y(U_SEAT) - 58), (CX, cam.y(U_SEAT) - 30),
                   dim(HL, 0.6), 1.4, dash="4,4")

    else:                            # vv9-25 — out of the camp
        if v >= 10:
            label(c, (SX0 + 8, 168), "we have an altar", 11, HL,
                  anchor="lm", bold=True)
            label(c, (SX0 + 8, 186), "from which those who serve the "
                  "tabernacle have no right to eat", 9.5,
                  dim(TEXT_DIM, 0.95), anchor="lm", italic=True)
        if v >= 11:
            label(c, (SX0 + 8, 212), "their bodies are burned OUTSIDE "
                  "OF THE CAMP", 9.5, dim(BLOOD, 0.95), anchor="lm",
                  italic=True)
        if v >= 12:
            label(c, (SX0 + 8, 232), "therefore Jesus also suffered "
                  "OUTSIDE OF THE GATE", 10, HL, anchor="lm", bold=True)
        if v >= 13:                  # the camera drops below the camp
            oy = cam.y(U_OUT)
            arrow(c, (CX, y_camp + 12), (CX, oy - 26), HL, 2.6, 10)
            figure(c, CX, oy, 52, HL, pose="walk")
            c.rect(CX + 90, oy - 40, 96, 40, fill=None,
                   stroke=dim(BLOOD, 0.9), width=1.8)
            label(c, (CX + 138, oy + 16), "THE ALTAR", 9.5,
                  dim(BLOOD, 0.95), bold=True)
            label(c, (CX - 130, oy - 16), "bearing his reproach", 9.5, HL,
                  anchor="rm", italic=True)
        if v >= 14:
            engrave(c, 13, 14, v, (CX, y_camp - 40), 18)
            city(c, lit=0.85, label_on=False)
            label(c, (CITY_X + 14, ROAD_Y - 152), "THAT WHICH IS TO COME",
                  9.5, dim(CITY, 0.95), bold=True)
        if v >= 15:
            label(c, (SX0 + 8, 300), "a sacrifice of praise, continually",
                  10, HL, anchor="lm", italic=True)
            label(c, (SX0 + 8, 318), "the fruit of lips which proclaim "
                  "allegiance to his name", 9,
                  dim(TEXT_DIM, 0.95), anchor="lm", italic=True)
        if v >= 16:
            label(c, (SX0 + 8, 342), "doing good, and sharing", 10, HL,
                  anchor="lm", italic=True)
        if v >= 17:
            label(c, (SX0 + 8, 366), "they watch on behalf of your souls",
                  9.5, dim(TEXT_DIM, 0.95), anchor="lm", italic=True)
        if v >= 18:
            label(c, (SX0 + 8, 390), "pray for us", 9.5,
                  dim(TEXT_DIM, 0.95), anchor="lm", italic=True)
        if v >= 20:                  # the great shepherd of the sheep
            gy = cam.y(U_OUT) - 2
            figure(c, 300, gy, 58, HL)
            for k in range(4):
                F.draw(c, F.sheep(), 200 + k * 40, gy, 0.30, dim(SAND, 0.9),
                       BG, style=_paint(dim(SAND, 0.9), 1.7))
            label(c, (300, gy - 74), "THE GREAT SHEPHERD OF THE SHEEP",
                  10, HL, bold=True)
            if v >= 21:
                label(c, (300, gy + 18), "make you complete in every "
                      "good work", 9.5, HL, italic=True)
        if v >= 22:
            label(c, (SX1 - 8, 420), "I have written to you in few words",
                  9.5, dim(TEXT_DIM, 0.95), anchor="rm", italic=True)
        if v >= 23:
            label(c, (SX1 - 8, 438), "our brother Timothy has been freed",
                  9.5, dim(TEXT_DIM, 0.95), anchor="rm", italic=True)
        if v >= 24:
            label(c, (SX1 - 8, 456), "the Italians greet you", 9.5,
                  dim(TEXT_DIM, 0.95), anchor="rm", italic=True)
        if v >= 25:
            label(c, (SX1 - 8, 480), "GRACE BE WITH YOU ALL", 11, HL,
                  anchor="rm", bold=True)
            # the road runs off the frame edge: the book ends walking
            c.line((CX + 40, cam.y(U_OUT)), (SX1, cam.y(U_OUT) - 14),
                   dim(SAND, 0.85), 2.0)


SCENES = {1: ch1, 2: ch2, 3: ch3, 4: ch4, 5: ch5, 6: ch6, 7: ch7, 8: ch8,
          9: ch9, 10: ch10, 11: ch11, 12: ch12, 13: ch13}


def render(ch, v):
    c = SvgCanvas(W, H, bg=BG)
    header(c, ch, v)
    view = VIEW_BY_VERSE[ch](v) if ch in VIEW_BY_VERSE else VIEWS[ch]
    cam = Cam(*view) if view else Cam(0, 1000)
    SCENES[ch](c, cam, v, P(ch, v))
    gauge(c, cam, off=view is None)
    better_mark(c, P(ch, v))
    return c


def main():
    total = count = 0
    for ch in sorted(SCENES):
        for v in verse_numbers(BOOK, ch):
            out = out_path(BOOK, ch, f"{SLUG}_{ch}_{v}.svg")
            render(ch, v).save(out)
            total += os.path.getsize(out)
            count += 1
    print(f"Hebrews: {count} SVG files "
          f"(chapters {min(SCENES)}-{max(SCENES)}), {total / 1e3:.0f} KB")


if __name__ == "__main__":
    main()
