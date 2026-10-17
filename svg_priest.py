"""The priestly garments of Exodus 28, as a drawable assembly.

`svg_figures.priest()` already draws a vested priest — a mitre and a ruled
breastplate on a 40-pixel silhouette, which is what a figure standing in a
scene needs. This module is the other thing: the garments at working scale,
each piece its own function, so a chapter that spends forty-three verses
making them can put one on per verse and light the piece it is making.

Two books need it. Exodus 28 makes the garments; Hebrews wears them — the
high priest enters the book at 2:17 and is its subject through chapter 10 —
so the geometry lives here rather than inside either generator.

Nothing here knows a palette. Every function takes its colours, the way
`svg_vocab` does, because Exodus draws the garments in their own gold and
dyed yarn while Hebrews will need them in a shadow key.

The body is a `Form`: one object holding the landmarks every garment hangs
from, computed from a height. Garments are drawn in *wearing* order, not
making order — a caller that has only made some of them simply skips the
rest, and the coat made last at 28:39 still comes out underneath the robe
made at 28:31, which is where it belongs.
"""

import math

# The pieces, in the order they are worn. A caller drawing a partial set
# should follow this order so the layering comes out right.
WEARING_ORDER = ("breeches", "coat", "robe", "ephod", "breastplate", "sash",
                 "turban", "plate")


class Form:
    """The landmarks of a front-on standing body, `h` tall from the ground
    line `gy` to the crown of the head, centred on `x`.

    Fractions rather than fixed offsets, so the same garment code draws the
    full-height diagram figure and a thumbnail without a second set of
    numbers. `h` is the *body* — a turban sits above it.
    """

    def __init__(self, x, gy, h):
        self.x, self.gy, self.h = float(x), float(gy), float(h)
        self.head_r = h * 0.058
        self.head_cy = gy - h + self.head_r
        self.brow_y = self.head_cy - self.head_r * 0.30
        self.neck_y = self.head_cy + self.head_r * 1.15
        self.shldr_y = gy - h * 0.825
        self.shldr_hw = h * 0.150
        self.chest_y = gy - h * 0.665         # the heart — 28:29, 28:30
        self.waist_y = gy - h * 0.520
        self.waist_hw = h * 0.130
        self.thigh_y = gy - h * 0.380         # 28:42, "to the thighs"
        self.knee_y = gy - h * 0.250
        self.cuff_y = gy - h * 0.455
        self.hem_hw = h * 0.163

    def hw(self, y):
        """Half-width of the hanging silhouette at height `y`. Shoulder to
        waist to hem, interpolated — every garment tapers on the same body,
        so a robe drawn short and a coat drawn long agree at the overlap."""
        if y <= self.shldr_y:
            return self.shldr_hw
        if y <= self.waist_y:
            t = (y - self.shldr_y) / (self.waist_y - self.shldr_y)
            return self.shldr_hw + (self.waist_hw - self.shldr_hw) * t
        t = min(1.0, (y - self.waist_y) / (self.gy - self.waist_y))
        return self.waist_hw + (self.hem_hw - self.waist_hw) * t

    def skirt(self, top_y, bot_y, steps=7):
        """The closed outline of a garment hanging from `top_y` to `bot_y`."""
        ys = [top_y + (bot_y - top_y) * i / steps for i in range(steps + 1)]
        left = [(self.x - self.hw(y), y) for y in ys]
        right = [(self.x + self.hw(y), y) for y in reversed(ys)]
        return left + right


def _taper(p0, w0, p1, w1):
    """A four-cornered limb from p0 (width w0) to p1 (width w1)."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    n = math.hypot(dx, dy) or 1.0
    ux, uy = -dy / n, dx / n
    return [(p0[0] + ux * w0 / 2, p0[1] + uy * w0 / 2),
            (p1[0] + ux * w1 / 2, p1[1] + uy * w1 / 2),
            (p1[0] - ux * w1 / 2, p1[1] - uy * w1 / 2),
            (p0[0] - ux * w0 / 2, p0[1] - uy * w0 / 2)]


def weave(c, pts, cols, rule=None, step=6.0, width=1.9, base=None):
    """Fill a convex outline with warp stripes in the materials it is woven
    from — 28:6, 'of gold, of blue, and purple, scarlet, and fine twined
    linen'.

    The verse says the cloth *is* those five, so they are drawn in it rather
    than parked in a key. Narrow and half-strength: at full saturation five
    hues in rotation read as a test card rather than as cloth.
    """
    if base is not None:
        c.polygon(pts, fill=base, stroke=None)
    xs = [p[0] for p in pts]
    x0, x1 = min(xs), max(xs)
    n = max(1, int((x1 - x0) / step))
    for i in range(n + 1):
        gx = x0 + i * (x1 - x0) / n
        hits = []
        for j in range(len(pts)):
            ax, ay = pts[j]
            bx, by = pts[(j + 1) % len(pts)]
            if (ax <= gx <= bx) or (bx <= gx <= ax):
                if abs(bx - ax) < 1e-9:
                    hits += [ay, by]
                else:
                    hits.append(ay + (by - ay) * (gx - ax) / (bx - ax))
        if len(hits) < 2:
            continue
        lo, hi = min(hits), max(hits)
        if hi - lo < 1.5:
            continue
        col = cols[i % len(cols)]
        c.line((gx, lo + 0.8), (gx, hi - 0.8),
               (col[0], col[1], col[2], 145), width)
    if rule is not None:
        c.polyline(pts, rule, 1.7, closed=True)


def silhouette(F, hem_y=None, sleeves=True):
    """The outline of a sleeved garment on this body.

    Body and sleeves are ONE outline with an armpit notch cut into it — the
    rule svg_figures states and the reason its figures read at 40 pixels:
    an arm laid over the robe as a separate mass cannot look like an arm,
    and an arm hidden behind it looks like no arm at all. The notch is what
    gives a silhouette its arms.
    """
    hem_y = F.gy if hem_y is None else hem_y
    side = []
    side.append((-0.034 * F.h, F.neck_y))
    side.append((-F.shldr_hw, F.shldr_y))
    if sleeves:
        side.append((-F.shldr_hw * 1.03, F.shldr_y + F.h * 0.055))
        side.append((-F.shldr_hw * 0.90, F.cuff_y))
        side.append((-F.shldr_hw * 0.58, F.cuff_y))
        side.append((-F.shldr_hw * 0.50, F.shldr_y + F.h * 0.075))
    side.append((-F.waist_hw, F.waist_y))
    side.append((-F.hw(hem_y), hem_y))
    left = [(F.x + dx, y) for dx, y in side]
    right = [(F.x - dx, y) for dx, y in reversed(side)]
    return left + right


def folds(c, F, col, top_y=None, hem_y=None, n=3):
    """The three hanging folds that keep a robe from reading as a flat
    mass. Copied in spirit from svg_figures, which draws the same three."""
    top_y = F.waist_y if top_y is None else top_y
    hem_y = F.gy if hem_y is None else hem_y
    for i in range(n):
        t = (i + 1) / (n + 1)
        x0 = F.x + (t - 0.5) * 2 * F.waist_hw * 0.86
        x1 = F.x + (t - 0.5) * 2 * F.hw(hem_y) * 0.80
        c.path(f"M{x0},{top_y} Q{(x0 + x1) / 2 - (x1 - x0) * 0.25},"
               f"{(top_y + hem_y) / 2} {x1},{hem_y - 2}",
               fill=None, stroke=col, width=1.2)


def _feet(c, F, col, mass):
    for sx in (-1, 1):
        c.polygon([(F.x + sx * 3, F.gy - F.h * 0.012),
                   (F.x + sx * 0.052 * F.h, F.gy - F.h * 0.012),
                   (F.x + sx * 0.056 * F.h, F.gy),
                   (F.x + sx * 3, F.gy)], fill=mass, stroke=col, width=1.2)


def head(c, F, ink, mass, rule, cloth=True):
    """Head, headcloth and beard. Faceless, like the cherubim and like every
    figure in svg_figures: at any size a drawn face is two uncanny marks, and
    what identifies a man is the covering and the beard."""
    r = F.head_r
    if cloth:
        for sx in (-1, 1):
            c.polygon([(F.x + sx * r * 0.62, F.head_cy - r * 0.55),
                       (F.x + sx * r * 1.28, F.head_cy - r * 0.20),
                       (F.x + sx * r * 1.42, F.head_cy + r * 1.35),
                       (F.x + sx * r * 0.80, F.head_cy + r * 1.20)],
                      fill=mass, stroke=rule, width=1.2)
    c.polygon(_taper((F.x, F.head_cy + r * 0.5), F.h * 0.048,
                     (F.x, F.shldr_y + F.h * 0.004), F.h * 0.056),
              fill=mass, stroke=rule, width=1.2)
    c.circle(F.x, F.head_cy, r, fill=mass, stroke=ink, width=1.6)
    c.path(f"M{F.x - r * 0.70},{F.head_cy + r * 0.10} "
           f"Q{F.x},{F.head_cy + r * 2.10} "
           f"{F.x + r * 0.70},{F.head_cy + r * 0.10}",
           fill=mass, stroke=ink, width=1.4)


# ---------------------------------------------------------------------------
# The body
# ---------------------------------------------------------------------------


def body(c, F, ink, mass, rule=None, cloth=True):
    """The man himself, in an ordinary garment: what 28:1 has, before a
    single holy garment is made. Everything else is drawn over it.

    `cloth=False` leaves the head bare, for a figure that is about to have
    the turban of 28:39 put on it — two head coverings at once reads as ear
    flaps rather than as either one.
    """
    rule = rule or ink
    _feet(c, F, ink, mass)
    c.polygon(silhouette(F), fill=mass, stroke=ink, width=1.7)
    folds(c, F, rule)
    c.line((F.x - F.shldr_hw * 0.50, F.shldr_y + F.h * 0.075),
           (F.x - F.waist_hw * 0.96, F.waist_y), rule, 1.1)
    c.line((F.x + F.shldr_hw * 0.50, F.shldr_y + F.h * 0.075),
           (F.x + F.waist_hw * 0.96, F.waist_y), rule, 1.1)
    head(c, F, ink, mass, rule, cloth=cloth)


def breeches(c, F, col, hidden=True):
    """28:42 — linen breeches, from the waist to the thighs.

    They are made last and worn first, so on a dressed figure they are under
    everything. Drawn as hidden line (dashed) rather than cut away: this is
    an assembly drawing, and a dashed outline is how an assembly drawing says
    'underneath'."""
    pts = F.skirt(F.waist_y - F.h * 0.02, F.thigh_y, steps=3)
    if hidden:
        c.polyline(pts, col, 1.5, dash="5,4", closed=True)
    else:
        c.polygon(pts, fill=col, stroke=col, width=1.4)
    c.line((F.x, F.waist_y + F.h * 0.03), (F.x, F.thigh_y), col, 1.3,
           dash="4,4" if hidden else None)


def coat(c, F, cloth, rule, checker=True):
    """28:39 — the coat woven in checker work, full length, sleeved. It is
    made last and worn nearly first, so on a dressed figure only its sleeves
    and the last inch of its hem are ever seen. That is the right answer, and
    it is what the chapter's own order hides."""
    c.polygon(silhouette(F), fill=cloth, stroke=rule, width=1.6)
    if not checker:
        return
    step = F.h * 0.028
    y = F.shldr_y + step * 1.6
    row = 0
    while y < F.gy - step * 0.4:
        hw = (F.hw(y) if y > F.cuff_y else F.shldr_hw * 0.86) * 0.92
        n = max(2, int(hw * 2 / step))
        for i in range(n + 1):
            gx = F.x - hw + i * (2 * hw / n)
            if (i + row) % 2 == 0:
                c.line((gx, y), (min(gx + 2 * hw / n, F.x + hw), y),
                       rule, 0.9)
        y += step
        row += 1


def robe(c, F, cloth, rule, hem_y=None, collar=True):
    """28:31–32 — the robe of the ephod, all of blue, with a bound hole for
    the head 'that it not be torn'. Its hem stops short of the coat's."""
    hem_y = hem_y or (F.gy - F.h * 0.085)
    # Sleeveless, and starting just below the shoulder line, so the coat
    # underneath keeps its sleeves — 28:31 makes the robe *of the ephod*,
    # not another tunic.
    c.polygon(silhouette(F, hem_y=hem_y, sleeves=False), fill=cloth,
              stroke=rule, width=1.7)
    folds(c, F, rule, top_y=F.waist_y, hem_y=hem_y)
    if collar:
        r = F.h * 0.048
        c.ellipse(F.x, F.shldr_y - F.h * 0.004, r, r * 0.52,
                  fill=None, stroke=rule, width=2.6)
        c.ellipse(F.x, F.shldr_y - F.h * 0.004, r * 0.72, r * 0.36,
                  fill=None, stroke=rule, width=1.3)
    return hem_y


def hem_ring(c, F, hem_y, n, bell, dyes, span=1.0, first_bell=True, r=None):
    """28:33–34 — 'a golden bell and a pomegranate, a golden bell and a
    pomegranate, around the hem of the robe.'

    The alternation is the verse, so it is drawn strictly: odd stations are
    bells, even are pomegranates, and the pomegranates cycle the three dyed
    yarns. `span` < 1 draws only the front of the hem, which is what 28:33
    has before 28:34 takes it all the way round.
    """
    r = r or F.h * 0.021
    hw = F.hw(hem_y)
    lit = max(1, int(round(n * span)))
    skip = (n - lit) // 2                 # a partial hem fills from the
    for i in range(skip, skip + lit):     # front, not from one edge
        t = (i + 0.5) / n
        gx = F.x - hw + 2 * hw * t
        # The hem is an ellipse seen nearly edge-on, so the stations near the
        # sides sit a little higher than those at the front.
        gy = hem_y + math.sin(math.pi * t) * F.h * 0.014
        if (i % 2 == 0) == first_bell:
            bell_mark(c, gx, gy, r, bell)
        else:
            pomegranate(c, gx, gy + r * 0.2, r, dyes[(i // 2) % len(dyes)])
    return lit


def bell_mark(c, x, y, r, col):
    """One golden bell, hanging."""
    c.path(f"M{x - r * 0.82},{y + r * 0.62} "
           f"Q{x - r * 0.72},{y - r * 0.85} {x},{y - r * 0.95} "
           f"Q{x + r * 0.72},{y - r * 0.85} {x + r * 0.82},{y + r * 0.62} Z",
           fill=col, stroke=col, width=1.0)
    c.circle(x, y + r * 0.86, r * 0.26, fill=col)


def pomegranate(c, x, y, r, col):
    """One pomegranate, with the crown that makes it one."""
    c.circle(x, y, r * 0.78, fill=col, stroke=col, width=1.0)
    for a in (-0.5, 0.0, 0.5):
        c.line((x, y - r * 0.62),
               (x + math.sin(a) * r * 0.52, y - r * 1.20), col, 1.4)


# ---------------------------------------------------------------------------
# The ephod, and what hangs on it
# ---------------------------------------------------------------------------


def ephod(c, F, cloth, rule, band=None, straps=True, cols=None):
    """28:6–8 — the ephod: a front piece from the shoulders to the waist,
    two shoulder straps joined to its two ends, and the skilfully woven band
    'of the same piece' at the waist.

    `cols` are the five materials of 28:5. Passing them weaves the piece
    instead of filling it flat, which is what keeps a garment the text
    describes four times by its materials from reading as a coloured slab.
    """
    top = F.shldr_y + F.h * 0.042
    bot = F.waist_y + F.h * 0.015
    hw_t, hw_b = F.hw(top) * 0.70, F.hw(bot) * 0.80
    front = [(F.x - hw_t, top), (F.x + hw_t, top),
             (F.x + hw_b, bot), (F.x - hw_b, bot)]
    if cols:
        weave(c, front, cols, rule, step=F.h * 0.018,
              width=F.h * 0.013, base=cloth)
    else:
        c.polygon(front, fill=cloth, stroke=rule, width=1.7)
    if straps:
        for sx in (-1, 1):
            strap = _taper((F.x + sx * hw_t * 0.72, top + F.h * 0.010),
                           F.h * 0.040,
                           (F.x + sx * F.shldr_hw * 0.62,
                            F.shldr_y - F.h * 0.014), F.h * 0.044)
            if cols:
                weave(c, strap, cols, rule, step=F.h * 0.016,
                      width=F.h * 0.011, base=cloth)
            else:
                c.polygon(strap, fill=cloth, stroke=rule, width=1.5)
    if band is not None:
        c.polygon([(F.x - hw_b * 1.04, bot), (F.x + hw_b * 1.04, bot),
                   (F.x + hw_b * 1.06, bot + F.h * 0.036),
                   (F.x - hw_b * 1.06, bot + F.h * 0.036)],
                  fill=band, stroke=rule, width=1.5)
    return top, bot


def strap_points(F):
    """Where the two shoulder stones sit — 28:12, 'on his two shoulders'."""
    return [(F.x - F.shldr_hw * 0.62, F.shldr_y - F.h * 0.008),
            (F.x + F.shldr_hw * 0.62, F.shldr_y - F.h * 0.008)]


def shoulder_stones(c, F, stone, setting, w=None):
    """28:9–12 — the two onyx stones, each in its setting of gold."""
    w = w or F.h * 0.062
    for px, py in strap_points(F):
        setting_box(c, px, py, w, w * 0.70, stone, setting)


def setting_box(c, cx, cy, w, h, stone, setting, rx=None):
    """A stone enclosed in a setting of gold — 28:11, 28:20. The setting is
    drawn proud of the stone on every side, because that is what a setting
    is and it is named four times in this chapter."""
    rx = rx if rx is not None else min(w, h) * 0.28
    c.rect(cx - w / 2 - 2.2, cy - h / 2 - 2.2, w + 4.4, h + 4.4,
           fill=None, stroke=setting, width=2.2, rx=rx + 2)
    c.rect(cx - w / 2, cy - h / 2, w, h, fill=stone, stroke=setting,
           width=1.2, rx=rx)


def braided_chain(c, p0, p1, col, width=2.0, n=None, amp=None):
    """28:14, 28:22 — 'chains of pure gold ... like cords of braided work'.
    Two strands crossing, which is what makes a drawn line read as braid
    rather than as wire."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    ln = math.hypot(dx, dy) or 1.0
    n = n or max(4, int(ln / 9))
    amp = amp if amp is not None else min(4.4, ln * 0.05)
    ux, uy = -dy / ln, dx / ln
    for phase in (0.0, math.pi):
        pts = []
        for i in range(n + 1):
            t = i / n
            s = math.sin(t * math.pi * n / 2 + phase) * amp
            pts.append((p0[0] + dx * t + ux * s, p0[1] + dy * t + uy * s))
        c.polyline(pts, col, width)


def ring(c, x, y, r, col, width=2.0):
    """One ring of gold — 28:23, 28:26, 28:27."""
    c.circle(x, y, r, fill=None, stroke=col, width=width)


def breastplate_on(c, F, frame, cells=None, w=None):
    """28:29 — the breastplate worn, on the heart. Small: the full-size
    working drawing lives in the detail panel; this is where it sits."""
    w = w or F.h * 0.150
    x0, y0 = F.x - w / 2, F.chest_y - w / 2
    c.rect(x0, y0, w, w, fill=None, stroke=frame, width=2.0, rx=2)
    for i in range(1, 3):
        c.line((x0 + w * i / 3, y0), (x0 + w * i / 3, y0 + w), frame, 1.0)
    for i in range(1, 4):
        c.line((x0, y0 + w * i / 4), (x0 + w, y0 + w * i / 4), frame, 1.0)
    if cells:
        cw, ch = w / 3, w / 4
        for i, col in enumerate(cells[:12]):
            if col is None:
                continue
            r, k = divmod(i, 3)
            c.rect(x0 + k * cw + cw * 0.18, y0 + r * ch + ch * 0.20,
                   cw * 0.64, ch * 0.60, fill=col, rx=1.4)
    return x0, y0, w


def sash(c, F, cloth, rule, ends=True):
    """28:39 — the sash, the work of the embroiderer: a band wound round the
    waist, knotted at the front, with the two ends left hanging. The knot is
    what makes a drawn band read as a sash and not as a belt."""
    y = F.waist_y + F.h * 0.055
    hw = F.hw(y)
    d = F.h * 0.040
    c.polygon([(F.x - hw * 1.03, y), (F.x + hw * 1.03, y),
               (F.x + hw * 1.05, y + d), (F.x - hw * 1.05, y + d)],
              fill=cloth, stroke=rule, width=1.5)
    c.line((F.x - hw, y + d * 0.5), (F.x + hw, y + d * 0.5),
           rule, 1.0)
    if not ends:
        return
    for sx, drop in ((-1, 0.150), (1, 0.108)):
        c.polygon(_taper((F.x + sx * hw * 0.20, y + d), F.h * 0.030,
                         (F.x + sx * hw * 0.34, y + F.h * drop),
                         F.h * 0.024), fill=cloth, stroke=rule, width=1.3)
    c.ellipse(F.x, y + d * 0.55, hw * 0.20, d * 0.62, fill=cloth,
              stroke=rule, width=1.5)


def turban(c, F, cloth, rule, wraps=3):
    """28:39 — the turban of fine linen. Taller than it is wide, and it sits
    proud of the brow: the silhouette is what names it."""
    r = F.head_r
    top = F.head_cy - r * 2.35
    c.path(f"M{F.x - r * 1.16},{F.head_cy - r * 0.34} "
           f"Q{F.x - r * 1.22},{top} {F.x},{top} "
           f"Q{F.x + r * 1.22},{top} {F.x + r * 1.16},"
           f"{F.head_cy - r * 0.34} Z",
           fill=cloth, stroke=rule, width=1.6)
    for i in range(1, wraps + 1):
        y = F.head_cy - r * 0.34 - (r * 2.0) * i / (wraps + 1)
        k = 1.0 - 0.10 * i
        c.path(f"M{F.x - r * 1.14 * k},{y} Q{F.x},{y - r * 0.34} "
               f"{F.x + r * 1.14 * k},{y}", fill=None, stroke=rule, width=1.2)
    return top


def plate_on(c, F, gold, lace, w=None):
    """28:36–38 — the plate of pure gold on a lace of blue, on the forehead.
    'It shall be always on his forehead.'"""
    w = w or F.head_r * 1.86
    h = w * 0.38
    y = F.brow_y
    c.line((F.x - w * 0.62, y - h * 0.1), (F.x + w * 0.62, y - h * 0.1),
           lace, 2.4)
    c.rect(F.x - w / 2, y - h / 2, w, h, fill=gold, stroke=gold, width=1.2,
           rx=h * 0.3)
    return F.x, y, w, h


# ---------------------------------------------------------------------------
# The working drawings — the pieces at the scale you can read them
# ---------------------------------------------------------------------------


def breastplate_plate(c, x0, y0, w, frame, setting, cells=(), labels=(),
                      sub=(), text_col=None, sub_col=None, fold=None,
                      size=13, sub_size=9.5):
    """28:15–21 at working scale: the square, four rows of three, each stone
    in its setting, each carrying a name.

    `cells` are the twelve stone colours (None for a row not yet set),
    `labels` the twelve names cut into them, `sub` the stone names. The grid
    is 3 wide and 4 deep inside a square, so the cells come out wider than
    they are tall — which is the room the names need.
    """
    cw, ch = w / 3, w / 4
    c.rect(x0, y0, w, w, fill=None, stroke=frame, width=2.4, rx=3)
    for i in range(12):
        r, k = divmod(i, 3)
        cx, cy = x0 + k * cw + cw / 2, y0 + r * ch + ch / 2
        col = cells[i] if i < len(cells) else None
        if col is None:
            c.rect(cx - cw * 0.40, cy - ch * 0.34, cw * 0.80, ch * 0.68,
                   fill=None, stroke=frame, width=0.9, rx=3)
            continue
        setting_box(c, cx, cy, cw * 0.80, ch * 0.68, col, setting, rx=3)
        name = labels[i] if i < len(labels) else ""
        if name:
            c.text((cx, cy - (ch * 0.09 if i < len(sub) and sub[i] else 0)),
                   name, size, text_col or frame, "mm", bold=True)
        s = sub[i] if i < len(sub) else ""
        if s:
            c.text((cx, cy + ch * 0.20), s, sub_size, sub_col or frame, "mm",
                   italic=True)
    if fold is not None:
        # 28:16, "folded double" — the fold is what makes it a pouch, and
        # the pouch is why 28:30 can put anything *in* it.
        c.line((x0, y0), (x0 + w, y0), fold, 3.0)
        c.path(f"M{x0 - 9},{y0} q{-7},{w * 0.5} 0,{w * 0.86}",
               fill=None, stroke=fold, width=1.6)


def onyx_stone(c, cx, cy, w, h, stone, setting, names=(), text_col=None,
               size=12, engraved=False):
    """28:9–11 — one onyx stone in its setting, with six names cut into it
    'like the engravings of a signet'."""
    setting_box(c, cx, cy, w, h, stone, setting, rx=h * 0.20)
    if not names:
        return
    for i, nm in enumerate(names):
        c.text((cx, cy - h * 0.34 + (i + 0.5) * (h * 0.70 / len(names))),
               nm, size, text_col or setting, "mm", bold=engraved)


def signet(c, cx, cy, r, col, ink=None):
    """The mark this chapter uses three times for 'cut so it stays cut' —
    28:11 on the shoulder stones, 28:21 on the twelve, 28:36 on the plate."""
    ink = ink or col
    c.circle(cx, cy, r, fill=None, stroke=col, width=2.0)
    c.circle(cx, cy, r * 0.62, fill=None, stroke=ink, width=1.2)
    for i in range(8):
        a = i * math.pi / 4
        c.line((cx + math.cos(a) * r * 0.66, cy + math.sin(a) * r * 0.66),
               (cx + math.cos(a) * r * 0.96, cy + math.sin(a) * r * 0.96),
               ink, 1.2)
