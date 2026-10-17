"""The figure vocabulary: creatures every book has to draw, drawn once.

A man, a donkey, a fish and a giant come up across the whole canon, and every
generator that needed one was drawing its own — so the same creature looked
like a different creature two books apart, and none of them looked as good as
the cherubim in Exodus 25 and Genesis 3, which were the only figures anyone
had taken the trouble over.

This module holds them, and holds the split that keeps them consistent:

  * a creature is GEOMETRY ONLY — a list of parts in local units, each part
    tagged with a material ("robe", "hide", "hair", "hoof", ...). It knows
    nothing about colour.
  * a style is a TABLE from material to paint. `palette()` builds one from
    the two colours a book already has: its linework and its page. Swap the
    table and every creature changes together; add a creature and it arrives
    already in the house style.

Three conventions make the parts reusable rather than merely shared:

  ONE UNIT.  1 unit = 1/100 of an adult man's height, for everything. A
  donkey is authored ~70 tall at the withers, a Nephilim ~155, a fish ~30
  long. Two creatures drawn at the same scale are therefore at true relative
  size without a scene having to be told how big a donkey is — which is the
  whole force of the Nephilim, and of a man beside a great fish.

  FEET ON ZERO.  Local y runs UP from the creature's own ground line, x runs
  across, and the origin sits between the feet. `place()` drops that anywhere
  on the canvas at any size, facing either way, at any angle.

  REAL COORDINATES.  place() returns points, not an SVG transform. Stroke
  weights therefore do not scale with the figure, and the results still feed
  SvgCanvas.traced() / pulse_outline() / grown(), so a figure can be drawn on
  the verse it enters exactly like every other mark in the book.

Masses are opaque. The cherubim's dim alpha fills let stacked shapes bleed
through one another, which a wing survives and a person does not.

Nothing here is wired into the existing generators; they keep their own
figures. New work should come from here.
"""

import math

# ---------------------------------------------------------------------------
# Geometry
# ---------------------------------------------------------------------------


def smooth(pts, closed=True, n=6, k=1.0):
    """A Catmull-Rom curve through the given points.

    This is what makes a hand-authored outline read as a body: a barrel drawn
    as sixteen points stays short enough to edit by hand and comes out round.
    Straight polygons at this scale are what made the old marks look built
    rather than drawn.
    """
    p = list(pts)
    ext = ([p[-1]] + p + [p[0], p[1]]) if closed else ([p[0]] + p + [p[-1]])
    out = []
    for i in range(len(ext) - 3):
        p0, p1, p2, p3 = ext[i:i + 4]
        for j in range(n):
            t = j / n
            t2, t3 = t * t, t * t * t
            out.append((
                0.5 * ((2 * p1[0]) + k * (-p0[0] + p2[0]) * t +
                       k * (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 +
                       k * (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3),
                0.5 * ((2 * p1[1]) + k * (-p0[1] + p2[1]) * t +
                       k * (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 +
                       k * (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)))
    if not closed:
        out.append(p[-1])
    return out


def taper(joints, widths, round_end=True):
    """A limb: a closed outline running along `joints`, `widths` thick at each.

    Serves arms, legs, necks, tails, ears, horns, a spear shaft — anything
    with a spine and a thickness. `round_end` caps the far end, which an ear
    or a tail wants and a leg standing on the ground does not.
    """
    n = len(joints)
    left, right = [], []
    for i, (p, w) in enumerate(zip(joints, widths)):
        if i == 0:
            dx, dy = joints[1][0] - p[0], joints[1][1] - p[1]
        elif i == n - 1:
            dx, dy = p[0] - joints[-2][0], p[1] - joints[-2][1]
        else:
            dx = joints[i + 1][0] - joints[i - 1][0]
            dy = joints[i + 1][1] - joints[i - 1][1]
        L = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / L, dx / L
        left.append((p[0] + nx * w / 2, p[1] + ny * w / 2))
        right.append((p[0] - nx * w / 2, p[1] - ny * w / 2))
    if round_end:
        p, w = joints[-1], widths[-1]
        dx, dy = p[0] - joints[-2][0], p[1] - joints[-2][1]
        L = math.hypot(dx, dy) or 1.0
        tip = (p[0] + dx / L * w * 0.45, p[1] + dy / L * w * 0.45)
        return smooth(left + [tip] + right[::-1], closed=True, n=3)
    return smooth(left + right[::-1], closed=True, n=2)


def hatch_poly(poly, deg, step, inset=1.4):
    """Parallel rule lines clipped to a polygon — the engraver's shading.

    Real segments rather than a fill pattern, so they scale and animate like
    every other mark. Independent of the figure style: it will shade a pit,
    a shadow or a dead region just as well as a flank.
    """
    a = math.radians(deg)
    ca, sa = math.cos(-a), math.sin(-a)
    rot = [(x * ca - y * sa, x * sa + y * ca) for x, y in poly]
    ys = [p[1] for p in rot]
    lo, hi = min(ys) + inset, max(ys) - inset
    ca2, sa2 = math.cos(a), math.sin(a)
    segs, y = [], lo
    while y <= hi:
        xs = []
        for i in range(len(rot)):
            x1, y1 = rot[i]
            x2, y2 = rot[(i + 1) % len(rot)]
            if (y1 <= y < y2) or (y2 <= y < y1):
                xs.append(x1 + (y - y1) / (y2 - y1) * (x2 - x1))
        xs.sort()
        for i in range(0, len(xs) - 1, 2):
            if xs[i + 1] - xs[i] > 2.2:
                ends = ((xs[i] + inset, y), (xs[i + 1] - inset, y))
                segs.append([(px * ca2 - py * sa2, px * sa2 + py * ca2)
                             for px, py in ends])
        y += step
    return segs


def place(pts, x, gy, s, flip=1, rot=0.0):
    """Local units -> canvas coordinates.

    (x, gy) is where the creature's own origin lands — for a standing figure
    that is the ground between its feet. `s` is canvas units per local unit,
    `flip` = -1 turns it to face the other way, `rot` leans it (radians,
    positive = clockwise on the page).
    """
    ca, sa = math.cos(rot), math.sin(rot)
    out = []
    for px, py in pts:
        px, py = px * flip * s, py * s
        out.append((x + px * ca - py * sa, gy - (py * ca + px * sa)))
    return out


def _scale(parts, u):
    """Restate a creature's parts in the shared unit."""
    out = []
    for kind, data, mat in parts:
        if kind == "dot":
            out.append((kind, (data[0] * u, data[1] * u, data[2] * u), mat))
        else:
            out.append((kind, [(px * u, py * u) for px, py in data], mat))
    return out


def bbox(*groups):
    """The local-unit extent of one or more (parts, x_offset) groups. Panels
    and scenes fit from this rather than from a guessed height."""
    xs, ys = [], []
    for parts, ox in groups:
        for kind, data, _m in parts:
            pts = [(data[0], data[1])] if kind == "dot" else data
            r = data[2] if kind == "dot" else 0
            for px, py in pts:
                xs += [px + ox - r, px + ox + r]
                ys += [py - r, py + r]
    return min(xs), max(xs), min(ys), max(ys)


# ---------------------------------------------------------------------------
# Paint
# ---------------------------------------------------------------------------
#
# A part is one of
#   ("fill", points, material)     a closed mass
#   ("line", points, material)     an open rule
#   ("dot",  (x, y, r), material)  a disc
#
# and the style table says, for each material, (fill, stroke, stroke_width).

MATERIALS = ("robe", "mantle", "cloth", "skin", "hair", "hide", "muzzle",
             "far", "fin", "hoof", "horn", "fleece", "wing", "metal", "wood",
             "stone", "clay", "fire", "fruit", "void", "mane", "rule",
             "sclera", "eye")

_cache = {}


def _mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _dim(col, a):
    return (col[0], col[1], col[2], int(255 * a))


def palette(ink, page):
    """The house style, built from a book's own linework colour and its page.

    Masses are opaque steps between the two, so a figure occludes whatever it
    stands in front of; the contour is the full-strength ink; interior seams
    sit a step down from it. A book that wants its figures in another key —
    the red of a judgment scene, say — passes that colour as `ink`.
    """
    # The whole colour, not just its RGB: a book that dims a figure by passing
    # the same colour at a lower opacity must get its own sheet, not the one
    # the full-strength call left in the cache.
    key = (tuple(ink), tuple(page))
    if key in _cache:
        return _cache[key]

    def t(v):
        return _mix(page[:3], ink[:3], v)

    sheet = {m: (t(0.26), ink, 1.5) for m in MATERIALS}
    sheet.update({
        "mantle": (t(0.42), ink, 1.5),
        "cloth": (t(0.38), ink, 1.4),
        "skin": (t(0.50), ink, 1.4),
        "hair": (t(0.12), ink, 1.3),
        "muzzle": (t(0.44), _dim(ink, 0.7), 1.1),
        "far": (t(0.16), _dim(ink, 0.55), 1.2),   # the off-side of a pair
        "fin": (t(0.16), ink, 1.3),
        "hoof": (t(0.10), ink, 1.2),
        "horn": (t(0.62), ink, 1.3),      # bone, and the brightest thing on
                                          # an ox — which is the point of it
        "fleece": (t(0.36), ink, 1.5),
        "wing": (t(0.20), ink, 1.3),
        "stone": (t(0.30), ink, 1.5),
        "clay": (t(0.42), ink, 1.5),      # pottery, and bread
        "fruit": (t(0.74), ink, 1.2),
        "fire": (t(0.82), ink, 1.2),      # the brightest mass there is, so it
                                          # reads as light and not as a shape
        "void": (page[:3], ink, 1.3),     # a hole: the page, punched through
                                          # whatever it is drawn on top of
        "wood": (t(0.20), ink, 1.2),
        "metal": (t(0.68), ink, 1.3),
        "rule": (None, _dim(ink, 0.72), 1.2),
        "mane": (None, _dim(ink, 0.72), 1.2),
        "sclera": (t(0.46), _dim(ink, 0.8), 1.0),
        "eye": (t(0.02), None, 0)})
    _cache[key] = sheet
    return sheet


def draw(c, parts, x, gy, s, ink, page, flip=1, rot=0.0, style=None):
    """Draw a creature on canvas `c`, its origin at (x, gy), at scale `s`."""
    sheet = style or palette(ink, page)
    for kind, data, mat in parts:
        fill, stroke, w = sheet.get(mat, sheet["rule"])
        if kind == "dot":
            (cx, cy), = place([(data[0], data[1])], x, gy, s, flip, rot)
            c.circle(cx, cy, data[2] * s, fill=fill, stroke=stroke, width=w)
        elif kind == "fill":
            c.polygon(place(data, x, gy, s, flip, rot), fill=fill,
                      stroke=stroke, width=w)
        else:
            c.polyline(place(data, x, gy, s, flip, rot), stroke=stroke,
                       width=w, fill=None)


def outline(parts, x, gy, s, flip=1, rot=0.0):
    """The placed points of the creature's largest mass — for a book that
    wants to trace a figure on the verse it enters, or ring it."""
    big, area = None, -1.0
    for kind, data, _m in parts:
        if kind != "fill":
            continue
        xs = [p[0] for p in data]
        ys = [p[1] for p in data]
        a = (max(xs) - min(xs)) * (max(ys) - min(ys))
        if a > area:
            big, area = data, a
    return place(big, x, gy, s, flip, rot) if big else []


# ---------------------------------------------------------------------------
# The creatures
# ---------------------------------------------------------------------------


# --- people ----------------------------------------------------------------
#
# Every human here is one function. A king is not a different body from a
# shepherd — he is the same body under a crown, and the moment they are
# written as separate figures they stop being the same height, the same
# shoulder, the same fold. What varies is declared, and nothing else can.
#
# The lower body is the only part a pose changes: the profile from the hem up
# to the waist, plus how far the whole upper body drops. Each is given as a
# left and a right side so a stride can be asymmetric.

_LOWER = {                                     # (left, right, drop, hem_y)
    "stand": ([(-13.6, 1.5), (-12.4, 18), (-11.2, 36), (-10.4, 50)],
              None, 0.0, 0.0),
    "walk":  ([(-17.6, 2.0), (-14.4, 20), (-11.6, 38), (-10.4, 50)],
              [(11.4, 22.0), (12.6, 32), (11.0, 41), (10.4, 50)], 0.0, 0.0),
    "kneel": ([(-21.0, 1.0), (-19.0, 13), (-14.0, 25), (-10.2, 33)],
              [(19.0, 1.0), (20.0, 10), (15.0, 23), (10.2, 33)], 27.0, 0.0),
    "sit":   ([(-17.0, 1.0), (-16.6, 12), (-13.4, 23), (-10.2, 29)],
              [(17.0, 1.0), (16.6, 12), (13.4, 23), (10.2, 29)], 29.0, 0.0)}

# The sleeve, from the armpit round the cuff and back up to the shoulder.
_SLEEVE = {
    "long": [(-9.8, 60.5), (-11.2, 54), (-12.6, 45), (-13.2, 40.4),
             (-16.4, 39.8), (-16.6, 50), (-16.0, 62), (-14.2, 72)],
    "short": [(-9.8, 60.5), (-11.0, 56.4), (-14.6, 55.6), (-15.8, 62),
              (-14.2, 72)]}

# The chest wall from armpit to shoulder, used in place of a sleeve on a side
# whose arm has been lifted out of the silhouette. Without it a raised arm is
# drawn on top of a sleeve that is still hanging, and the figure has three.
_STUMP = [(-9.8, 60.5), (-10.8, 66.4), (-12.0, 72.0)]

# The gestures.
#
# An arm inside the robe outline can only hang: the sleeve IS the silhouette,
# and a silhouette cannot raise anything. So a lifted arm leaves the outline
# and becomes its own limb, and the side it left gets _STUMP instead.
#
# Keyed by side, in PAGE terms — -1 is page-left, +1 is page-right, which is
# the convention the schematic figures these replace already used ("point_r"
# points to the right of the page, not the figure's own right). Each side is
# shoulder, elbow, hand; the hand lands a little beyond the last joint.
#
# Heights are set against the head, which sits at 89.6 with a radius of 6.6
# and headgear to about 104: "up" reaches 92 at x 20.6, clear of the widest
# mitre, so a raised hand never crosses a face.

_ARMS = {
    "down": {},
    "open": {-1: [(-11.5, 70.5), (-20.5, 66.5), (-28.0, 70.5)],
             1: [(11.5, 70.5), (20.5, 66.5), (28.0, 70.5)]},
    "up": {-1: [(-11.5, 71.5), (-17.5, 80.0), (-20.6, 92.0)],
           1: [(11.5, 71.5), (17.5, 80.0), (20.6, 92.0)]},
    "point_r": {1: [(11.5, 70.5), (21.0, 68.5), (31.0, 67.0)]},
    "point_l": {-1: [(-11.5, 70.5), (-21.0, 68.5), (-31.0, 67.0)]},
    "hold_r": {1: [(11.5, 70.0), (19.5, 63.5), (28.0, 61.5)]},
    "hold_l": {-1: [(-11.5, 70.0), (-19.5, 63.5), (-28.0, 61.5)]},
    # Both hands out, at unequal heights so it reads as searching and not as
    # a pose. A frontal figure cannot reach toward the reader, so the feeling
    # forward is carried sideways.
    "grope": {-1: [(-11.5, 69.5), (-18.5, 64.0), (-26.0, 63.0)],
              1: [(11.5, 70.5), (18.5, 65.0), (26.5, 66.5)]},
}

_ARM_W = [8.6, 6.8, 5.2]


def _arm(P, joints, sleeve, shoulder, drop):
    """One lifted arm, from the shoulder out. Sleeved to the wrist, or — on a
    short sleeve — sleeved to the elbow with the forearm bare, which is the
    same split the standing soldier has."""
    j = [(px * shoulder, py - drop) for px, py in joints]
    if sleeve == "short":
        P.append(("fill", taper(j[:2], _ARM_W[:2], round_end=False), "robe"))
        P.append(("fill", taper(j[1:], _ARM_W[1:], round_end=False), "skin"))
    else:
        P.append(("fill", taper(j, _ARM_W, round_end=False), "robe"))
    dx, dy = j[-1][0] - j[-2][0], j[-1][1] - j[-2][1]
    L = math.hypot(dx, dy) or 1.0
    P.append(("dot", (j[-1][0] + dx / L * 2.0, j[-1][1] + dy / L * 2.0, 2.8),
              "skin"))


def _head(P, hy, r, kind, beard, drop):
    """The head and whatever is on it, centred at (0, hy).

    The headgear is the whole of what tells one man from another at this
    size, so it is the one thing drawn with any care: a turban is taller than
    it is wide, a crown sits proud of the brow, a helmet comes down over it.
    """
    hy -= drop
    P.append(("fill", taper([(0, hy - 12.6), (0, hy - 4.6)], [6.6, 6.0],
                            round_end=False), "skin"))               # neck
    if kind in ("cloth", "crown"):           # a headcloth held by a band
        for sx in (-1, 1):
            P.append(("fill", taper(
                [(sx * 6.2, hy + 3.4), (sx * 7.4, hy - 3.6),
                 (sx * 7.8, hy - 11.2)], [4.4, 4.2, 4.0],
                round_end=False), "cloth"))
    elif kind == "veil":                     # falls past the shoulders
        for sx in (-1, 1):
            P.append(("fill", taper(
                [(sx * 6.4, hy + 4.0), (sx * 9.6, hy - 8.0),
                 (sx * 11.4, hy - 20.0), (sx * 11.0, hy - 29.0)],
                [5.2, 6.4, 7.0, 6.4], round_end=False), "cloth"))
    P.append(("dot", (0, hy, r), "skin"))
    if beard:
        P.append(("fill", smooth(
            [(-4.6, hy - 0.6), (-4.8, hy - 5.6), (-2.4, hy - 9.0),
             (0, hy - 9.8), (2.4, hy - 9.0), (4.8, hy - 5.6),
             (4.6, hy - 0.6), (0, hy + 0.8)]), "hair"))
    if kind in ("cloth", "crown", "veil"):
        w = 8.6 if kind == "veil" else 7.9
        P.append(("fill", smooth(
            [(-w, hy - 1.0), (-w + 0.7, hy + 4.4), (-3.6, hy + 7.2),
             (0, hy + 7.8), (3.6, hy + 7.2), (w - 0.7, hy + 4.4),
             (w, hy - 1.0), (4.4, hy + 1.6), (0, hy + 2.2),
             (-4.4, hy + 1.6)]), "cloth"))
    if kind == "cloth":
        P.append(("line", smooth([(-7.6, hy), (0, hy + 1.8), (7.6, hy)],
                                 closed=False), "rule"))
    elif kind == "crown":                    # a band and five points
        P.append(("fill", smooth([(-8.2, hy + 1.6), (0, hy + 3.6),
                                  (8.2, hy + 1.6), (8.4, hy + 6.4),
                                  (0, hy + 8.4), (-8.4, hy + 6.4)]),
                  "metal"))
        for k in (-2, -1, 0, 1, 2):
            bx = k * 3.9
            P.append(("fill", smooth(
                [(bx - 2.2, hy + 7.4), (bx, hy + 13.4 - abs(k) * 1.4),
                 (bx + 2.2, hy + 7.4)]), "metal"))
    elif kind == "mitre":                    # the priest's wound turban
        P.append(("fill", smooth(
            [(-8.0, hy - 0.6), (-8.8, hy + 6.0), (-6.4, hy + 13.0),
             (0, hy + 15.6), (6.4, hy + 13.0), (8.8, hy + 6.0),
             (8.0, hy - 0.6), (0, hy + 1.4)]), "cloth"))
        for k in (3.4, 8.0, 12.0):           # the windings
            P.append(("line", smooth([(-7.6 + k * 0.11, hy + k - 1.6),
                                      (0, hy + k + 0.6),
                                      (7.6 - k * 0.11, hy + k - 1.6)],
                                     closed=False), "rule"))
    elif kind == "helmet":                   # down over the brow, with a nasal
        P.append(("fill", smooth(
            [(-8.2, hy - 2.4), (-8.6, hy + 5.0), (-4.6, hy + 10.4),
             (0, hy + 11.6), (4.6, hy + 10.4), (8.6, hy + 5.0),
             (8.2, hy - 2.4), (5.6, hy + 1.0), (0, hy + 2.0),
             (-5.6, hy + 1.0)]), "metal"))
        P.append(("fill", taper([(0, hy + 2.4), (0, hy - 4.6)],
                                [2.6, 2.2], round_end=False), "metal"))
    return P


def _person(pose="stand", head="cloth", beard=True, mantle=True,
            sleeve="long", hem=1.0, prop=None, shoulder=1.0, r=6.6,
            hy=89.6, sash=False, ephod=False, shield=False, arms="down"):
    """A standing, walking, kneeling or seated human, facing the reader.

    Faceless, like the cherubim: at the size these are used a face is two
    grey pixels, and an uncanny two. What identifies a person here is the
    robe, what is on the head, and what is in the hand — which is what
    identified one in the period and is what still reads at any size.

    `pose` is what the legs do, `arms` what the hands do, and they compose:
    a man may walk with his arm out or kneel with both raised. See _ARMS for
    the gestures and for which side of the page each one names.

    A prop occupies the right hand and a shield the left, so a gesture that
    wants an occupied hand is dropped on that side and kept on the other — a
    man cannot raise the hand he is leaning on a staff with, and one arm up
    beside a staff is the right drawing rather than a compromise. A soldier
    carrying both has no free hand, and gestures for him do nothing at all,
    which is the truthful answer rather than a floating shield.
    """
    P = []
    lo_l, lo_r, drop, _hem_y = _LOWER[pose]
    lifted = dict(_ARMS.get(arms, {}))
    if prop is not None:
        lifted.pop(1, None)
    if shield:
        lifted.pop(-1, None)
    lo_r = lo_r or [(-px, py) for px, py in lo_l]
    lo_l = [(px, py * hem if py < 50 else py) for px, py in lo_l]
    lo_r = [(px, py * hem if py < 50 else py) for px, py in lo_r]

    def U(pts, sx):                     # a sleeve/shoulder side, dropped
        return [(px * sx * shoulder, py - drop) for px, py in pts]

    if prop in ("staff", "spear"):
        top = 104 if prop == "staff" else 116
        P.append(("fill", taper([(15.6, 0), (16.8, 50), (18, top)],
                                [2.6, 2.8, 2.4], round_end=False), "wood"))
        if prop == "spear":
            P.append(("fill", smooth([(18, top), (14.6, top + 9),
                                      (18, top + 21), (21.4, top + 9)]),
                      "metal"))
    elif prop == "sceptre":                  # short, held, and gold-headed
        P.append(("fill", taper([(15.8, 36 - drop), (16.8, 56 - drop)],
                                [2.4, 2.4], round_end=False), "wood"))
        P.append(("dot", (16.9, 58.4 - drop, 3.4), "metal"))
    # Body and sleeves are ONE outline with an armpit notch cut into it. An
    # arm laid over the robe as its own mass cannot read as an arm, and an
    # arm hidden behind it reads as no arm at all; the notch is what gives a
    # silhouette its arms.
    # A pose needs one thing the silhouette cannot get from a changed hem:
    # walking needs a leg out from under it, kneeling a knee coming up
    # through it, sitting the thing sat on. Without these three the poses
    # differ only in height, and a kneeling man reads as a short one.
    if pose == "walk":
        # The leading leg has to sit clear of the robe's own outline or the
        # lifted hem is all there is to see, and a swept hem on its own reads
        # as a robe hanging oddly rather than as a man in motion.
        P.append(("fill", taper([(8.0, 34), (11.5, 14), (12.5, 3.6)],
                                [8.6, 7.4, 6.6], round_end=False), "skin"))
        P.append(("fill", smooth([(10.0, 0.4), (18.2, 0.4), (18.6, 3.8),
                                  (9.8, 3.8)]), "skin"))
    elif pose == "sit":                      # the stool, drawn behind
        for sx in (-1, 1):
            P.append(("fill", smooth([(sx * 14.4, 0.4), (sx * 19.6, 0.4),
                                      (sx * 19.0, 15), (sx * 15.0, 15)]),
                      "wood"))
        P.append(("fill", smooth([(-21.6, 15), (21.6, 15), (21.0, 20.4),
                                  (-21.0, 20.4)]), "wood"))
    # The sleeve is authored on the left, so it is used as given on the left
    # and mirrored on the right — negating it twice was what folded the torso
    # into a bow.
    def top(sx):
        pts = U(_STUMP if sx in lifted else _SLEEVE[sleeve], 1) + [
            (-11.4 * shoulder, 77.6 - drop), (-6.4, 80 - drop),
            (-3.0, 81 - drop)]
        return pts if sx < 0 else [(-px, py) for px, py in reversed(pts)]

    top_l, top_r = top(-1), top(1)
    P.append(("fill", smooth(
        list(lo_l) + top_l + [(0, 81.2 - drop)] + top_r + list(reversed(lo_r))
        + [(lo_r[0][0] * 0.5, 0.2), (0, -0.6), (lo_l[0][0] * 0.5, 0.2)]),
        "robe"))
    # After the torso and before the mantle, so the yoke lands over the top of
    # the arm the way a garment does and the join needs no hiding.
    for sx in sorted(lifted):
        _arm(P, lifted[sx], sleeve, shoulder, drop)
    cuff = (-16.4, 39.8) if sleeve == "long" else (-15.2, 55.6)
    for sx in (-1, 1):
        if sx in lifted:                 # its hand is on the lifted arm
            continue
        if sleeve == "short":            # a bare forearm below a short sleeve
            P.append(("fill", taper(
                [(sx * 14.2 * shoulder, 56 - drop),
                 (sx * 15.4 * shoulder, 46 - drop)], [7.4, 6.0],
                round_end=False), "skin"))
            P.append(("dot", (sx * 15.6 * shoulder, 43.6 - drop, 3.0),
                      "skin"))
        else:
            P.append(("dot", (sx * (abs(cuff[0]) - 1.9) * shoulder,
                              cuff[1] - 0.4 - drop, 2.4), "skin"))
    if pose in ("stand", "walk"):
        for sx in (-1, 1):
            fx = sx * 2.2 + (5 if pose == "walk" and sx > 0 else 0)
            P.append(("fill", smooth([(fx, 0.4), (fx + sx * 5.2, 0.4),
                                      (fx + sx * 5.6, 3.4), (fx + sx * 2.0,
                                                             3.4)]), "skin"))
    if pose == "kneel":                     # the raised knee, through the robe
        P.append(("fill", smooth([(2.0, 3.0), (13.6, 5.6), (17.4, 17),
                                  (12.6, 25.4), (3.4, 21.4), (0.6, 12)]),
                  "robe"))
        P.append(("line", smooth([(4.0, 21.0), (11.6, 20.0), (15.6, 13.4)],
                                 closed=False), "rule"))
    if pose == "sit":                       # both knees, coming forward
        for sx in (-1, 1):
            P.append(("fill", smooth(
                [(sx * 2.4, 6.0), (sx * 12.4, 8.0), (sx * 14.6, 17.4),
                 (sx * 10.0, 23.4), (sx * 2.0, 20.0)]), "robe"))
    if mantle:                              # a yoke over both shoulders
        P.append(("fill", smooth(
            [(px * shoulder, py - drop) for px, py in
             [(-12.2, 78), (-13.2, 70), (-11.4, 64), (-6, 66.5), (0, 63.4),
              (6, 66.5), (11.4, 64), (13.2, 70), (12.2, 78), (6, 80.2),
              (0, 81), (-6, 80.2)]]), "mantle"))
    if sash:                                # worn across, shoulder to hip
        P.append(("fill", smooth([(-11.0, 75 - drop), (-4.6, 77 - drop),
                                  (11.0, 55 - drop), (4.8, 52 - drop)]),
                  "mantle"))
    if ephod:                               # the breastplate of judgment
        P.append(("fill", smooth([(-6.4, 74 - drop), (6.4, 74 - drop),
                                  (6.4, 61 - drop), (-6.4, 61 - drop)]),
                  "metal"))
        for gy in (70.6, 67.4, 64.2):
            P.append(("line", [(-6.4, gy - drop), (6.4, gy - drop)], "rule"))
        for gx in (-2.1, 2.1):
            P.append(("line", [(gx, 74 - drop), (gx, 61 - drop)], "rule"))
    if shield:
        P.append(("fill", smooth([(-13, 62 - drop), (-6.6, 66 - drop),
                                  (-1.4, 60 - drop), (-2.6, 47 - drop),
                                  (-9, 41 - drop), (-14.6, 48 - drop)]),
                  "metal"))
        P.append(("dot", (-7.8, 54 - drop, 2.2), "rule"))
    _head(P, hy, r, head, beard, drop)
    folds = ([(-4.6, 52), (-7.0, 28), (-8.2, 4)],
             [(0.4, 54), (0.9, 28), (0.7, 3)],
             [(4.6, 52), (7.0, 28), (8.2, 4)])
    for f in folds:
        f = [(px, py * hem) for px, py in f]
        if f[0][1] * 1.0 > (50 - drop):
            continue
        P.append(("line", smooth(f, closed=False), "rule"))
    return P


def _man(mantle=True, staff=False, pose="stand"):
    return _person(pose=pose, mantle=mantle,
                   prop="staff" if staff else None)


# Her hair is what makes the figure legible as a woman and decent at the same
# time, which is how she has been drawn for as long as she has been drawn: it
# comes over the shoulders and down the chest, and the body underneath is the
# same body the man has. Each style below is only the hair — nothing else in
# the figure changes between them.

# Her hair is one piece, and one piece only. It goes on BEFORE the head, so
# the face lands on top of it and stays open, and it does the covering across
# the breast on its way down.
#
# The thing that makes or breaks it is the notch up the middle. Carried across
# the bottom as a single hem the mass closes under the chin and reads as a
# beard; cut up the centre, the two falls hang from the shoulders the way hair
# does. The notch only has to clear the chin — its top is tucked up behind the
# face, where the head disc hides the join — and once it is there, no separate
# locks are needed in front, because the falls ARE the locks.

_HAIR = {
    "fall": [
        (-8.8, 58), (-10.2, 70), (-10.4, 84), (-9.0, 96), (-4.6, 100.8),
        (0, 101.6), (4.6, 100.8), (9.0, 96), (10.4, 84), (10.2, 70),
        (8.8, 58), (6.2, 51),
        (4.4, 62), (3.8, 76), (4.0, 88), (0, 93), (-4.0, 88), (-3.8, 76),
        (-4.4, 62), (-6.2, 51)],
    "sweep": [
        (-11.2, 56), (-13.0, 68), (-11.6, 82), (-9.2, 96), (-4.6, 100.8),
        (0, 101.6), (4.6, 100.8), (9.2, 96), (11.6, 82), (13.0, 68),
        (11.2, 56), (7.6, 48),
        (5.0, 60), (4.2, 76), (4.2, 88), (0, 93), (-4.2, 88), (-4.2, 76),
        (-5.0, 60), (-7.6, 48)],
    "long": [
        (-8.6, 44), (-9.6, 62), (-9.8, 82), (-8.8, 96), (-4.6, 100.8),
        (0, 101.6), (4.6, 100.8), (8.8, 96), (9.8, 82), (9.6, 62),
        (8.6, 44), (6.0, 36),
        (4.4, 50), (3.9, 70), (4.0, 88), (0, 93), (-4.0, 88), (-3.9, 70),
        (-4.4, 50), (-6.0, 36)],
    "braid": [
        (-9.0, 56), (-10.4, 70), (-10.6, 84), (-9.0, 96), (-4.6, 100.8),
        (0, 101.6), (4.6, 100.8), (9.2, 96), (10.6, 86), (10.0, 74),
        (7.4, 62), (4.6, 50), (3.4, 42), (0.6, 46),
        (2.2, 60), (3.4, 74), (4.0, 88), (0, 93), (-4.2, 88), (-4.0, 74),
        (-4.6, 60), (-6.4, 49)],
}


def _hair(style):
    """One mass, notched up the centre. `braid` gathers the near side into a
    plait, which is the only style that needs a mark on top of the shape."""
    P = [("fill", smooth(_HAIR.get(style, _HAIR["fall"])), "hair")]
    if style == "braid":
        for k in (0.22, 0.42, 0.62, 0.82):
            P.append(("line", [(9.4 - 6.6 * k, 88 - 44 * k),
                               (4.4 - 3.4 * k, 84 - 41 * k)], "rule"))
    return P


def _unclothed(head="bare", beard=True, hair=None, covering=None,
               shoulder=1.0, arms="down"):
    """The man and the woman before the coats of skins.

    Genesis 3 needs a body the robed figure cannot give it: the chapter turns
    on being naked and knowing it, and every covering in it — the apron of fig
    leaves at verse 7, the coats of skins at verse 21 — is a thing put ON that
    body and has to be seen being put on. Built at the same height and the
    same shoulder as the robed man so the two are one person before and after.
    """
    P = []
    if arms == "reach":                       # taking of the fruit
        joints = [(13, 76), (20, 66), (24, 56)]
    else:
        joints = [(13, 76), (17, 62), (16, 46)]
    P.append(("fill", taper([(-j[0] * shoulder, j[1]) for j in joints],
                            [8.4, 6.2, 4.6], round_end=False), "skin"))
    P.append(("dot", (-joints[-1][0] * shoulder, joints[-1][1] - 2.4, 2.8),
              "skin"))
    for sx in (-1, 1):                                            # legs
        P.append(("fill", taper([(sx * 5.4, 32), (sx * 7.0, 18), (sx * 6, 3)],
                                [10.4, 6.6, 5.2], round_end=False), "skin"))
        P.append(("fill", smooth([(sx * 6 - 4.6, 3), (sx * 6 + 4.6, 3),
                                  (sx * 6 + 5.4, 0), (sx * 6 - 5, 0)]),
                  "skin"))
    P.append(("fill", smooth(
        [(-13 * shoulder, 77), (-14 * shoulder, 69), (-10.6, 59), (-8, 49),
         (-8.4, 43), (8.4, 43), (8, 49), (10.6, 59), (14 * shoulder, 69),
         (13 * shoulder, 77), (7, 81), (0, 82), (-7, 81)]), "skin"))
    P.append(("fill", taper([(0, 76), (0, 85)], [6.6, 6.0],
                            round_end=False), "skin"))
    if covering == "leaves":                  # the apron of verse 7
        for k in range(5):
            bx = -9.6 + k * 4.8
            P.append(("fill", smooth([(bx - 3.4, 44), (bx, 47), (bx + 3.4, 44),
                                      (bx + 2.6, 36), (bx, 33.4),
                                      (bx - 2.6, 36)]), "fleece"))
        P.append(("line", [(-11, 45.4), (11, 45.4)], "rule"))
    elif covering == "skins":                 # the coats of verse 21
        P.append(("fill", smooth(
            [(-12.6, 78), (-13.6, 66), (-12, 52), (-11.4, 30), (11.4, 30),
             (12, 52), (13.6, 66), (12.6, 78), (6, 81), (0, 82),
             (-6, 81)], n=3), "hide"))
        P.append(("line", smooth([(-12, 56), (0, 53.4), (12, 56)],
                                 closed=False), "rule"))
    P.append(("fill", taper([(j[0] * shoulder, j[1]) for j in joints],
                            [8.4, 6.2, 4.6], round_end=False), "skin"))
    P.append(("dot", (joints[-1][0] * shoulder, joints[-1][1] - 2.4, 2.8),
              "skin"))
    if hair:                                  # her hair, for his beard
        P.extend(_hair(hair))                 # behind the face, over the breast
    _head(P, 89.6, 6.6, head, beard, 0.0)
    return P


def _donkey():
    """Facing right, standing. The dorsal stripe and the bar across the
    withers are the donkey's own markings and are what tell it from a horse
    at a glance, so they are drawn, not decoration."""
    P = _quadruped([
        ([(12.5, 31), (14, 17), (12, 3)], [9.5, 5.0, 4.2], "far"),
        ([(-27.5, 33), (-24.5, 19), (-27, 3)], [12, 5.6, 4.4], "far"),
        ([(19, 31), (20.5, 17), (18.5, 3)], [11, 5.8, 4.8], "hide"),
        ([(-22, 33), (-18.5, 19), (-21, 3)], [14, 6.4, 5.0], "hide")])
    P.append(("fill", taper([(-30, 44), (-34.2, 34), (-35.6, 25)],
                            [6.0, 3.6, 3.0], round_end=False), "hide"))
    P.append(("fill", smooth([(-35.6, 27), (-32.4, 20), (-34.8, 11),
                              (-38.8, 19), (-38.4, 25)]), "hair"))   # tuft
    P.append(("fill", taper([(33, 68), (30.6, 76.5), (31.4, 82)],
                            [7.4, 5.6, 2.2]), "hide"))               # ears
    P.append(("fill", taper([(37.6, 68), (38.6, 77), (40.6, 82)],
                            [7.4, 5.6, 2.2]), "hide"))
    P.append(("fill", taper([(19, 44), (27, 54), (34, 62)],
                            [23, 15.5, 11], round_end=False), "hide"))
    P.append(("fill", smooth(                                        # barrel
        [(24, 34), (26, 43), (21, 51), (13, 54), (2, 51), (-9, 50.5),
         (-19, 52.5), (-27, 49), (-31.5, 41), (-32, 32), (-29, 25),
         (-22, 22.5), (-10, 22), (2, 22.5), (13, 24.5), (20, 28)]), "hide"))
    P.append(("fill", smooth(                                        # head
        [(31.5, 68.5), (38, 69), (46, 64), (51.6, 57), (51.4, 52.6),
         (46.8, 51), (40, 54.4), (33, 59.5), (29.8, 64)]), "hide"))
    P.append(("fill", smooth([(51.6, 57), (52.4, 54.6), (51.4, 52.4),
                              (48.6, 51.6), (47.4, 54), (48.6, 56.6)]),
              "muzzle"))
    P.append(("line", smooth([(13, 53), (0, 50.4), (-19, 51.4), (-28, 47)],
                             closed=False), "rule"))                 # dorsal
    P.append(("line", smooth([(17, 52), (16, 42), (15.5, 33)], closed=False),
              "rule"))                                               # the bar
    P.append(("line", smooth([(19.5, 47), (25.5, 52), (32, 58.5)],
                             closed=False), "mane"))
    P.append(("dot", (38.6, 63.4, 1.7), "sclera"))
    P.append(("dot", (38.8, 63.4, 0.95), "eye"))
    P.append(("dot", (49.6, 54.4, 1.0), "eye"))                      # nostril
    return P


def _quadruped(legs, tuck=10.0):
    """The four legs and feet of a standing animal, off-side pair first.

    Every four-footed creature here starts with this: the far pair drawn
    before the near pair and a step dimmer, which is the whole of what makes
    a side view read as a solid animal rather than a cut-out.

    `tuck` runs each leg on up into the body past the joint it was authored
    from. A leg whose flat top stops at the belly line shows that top as a
    straight edge and the whole limb reads as a rectangle propped against the
    animal; carried up inside the barrel, it disappears under it. Authors give
    the leg the joint they can see and this hides the rest.
    """
    P = []
    for j, w, m in legs:
        dx, dy = j[0][0] - j[1][0], j[0][1] - j[1][1]
        L = math.hypot(dx, dy) or 1.0
        j = [(j[0][0] + dx / L * tuck, j[0][1] + dy / L * tuck)] + list(j)
        w = [w[0]] + list(w)
        P.append(("fill", taper(j, w, round_end=False), m))
        P.append(("fill", smooth([(j[-1][0] - w[-1] * 0.62, 3.4),
                                  (j[-1][0] + w[-1] * 0.62, 3.4),
                                  (j[-1][0] + w[-1] * 0.72, 0),
                                  (j[-1][0] - w[-1] * 0.72, 0)]),
                  "hoof" if m != "far" else "far"))
    return P


def _ox():
    """Facing right, standing. What has to be unmistakable is that this is
    not a large donkey: the hump over the withers, the dewlap swinging under
    the throat and the horns are the three marks that settle it, and the head
    is carried low — an ox looks at the ground it is ploughing."""
    P = _quadruped([
        ([(17, 26), (18, 14), (16.5, 3)], [12, 7.0, 6.0], "far"),
        ([(-25, 27), (-22, 14), (-24, 3)], [15, 7.5, 6.2], "far"),
        ([(23, 26), (24, 14), (22.5, 3)], [14, 8.0, 6.8], "hide"),
        ([(-19, 27), (-16, 14), (-18, 3)], [17, 8.5, 7.0], "hide")])
    P.append(("fill", taper([(-33, 44), (-36.5, 30), (-35.5, 17)],
                            [4.5, 3.0, 2.4], round_end=False), "hide"))
    P.append(("fill", smooth([(-35.5, 19), (-32.4, 13), (-35, 4),
                              (-38.8, 12), (-38.4, 18)]), "hair"))    # tuft
    P.append(("fill", taper([(20, 46), (30, 48), (38, 46)],
                            [26, 20, 16], round_end=False), "hide"))  # neck
    P.append(("fill", smooth(                                         # barrel
        [(26, 36), (28, 46), (26, 54), (20, 60), (12, 62), (2, 55),
         (-10, 53), (-20, 54), (-28, 52), (-33, 45), (-34, 34), (-31, 25),
         (-24, 21), (-10, 20), (2, 20.5), (14, 23), (22, 27)]), "hide"))
    P.append(("fill", smooth([(34, 47), (38.4, 43), (36.6, 35.4),
                              (30.6, 32.6), (27, 36.6), (28, 43)]),
              "hide"))                              # dewlap, under the throat
    P.append(("fill", smooth(                                         # head
        [(36, 54), (44, 55), (51, 51), (54, 45), (53, 40), (47, 38),
         (41, 41), (36, 46)]), "hide"))
    P.append(("fill", smooth([(54, 45), (55.6, 42.4), (54, 39.4),
                              (50, 38.2), (48.4, 41), (50, 44.6)]), "muzzle"))
    P.append(("fill", taper([(38.6, 50), (33.8, 51.4), (30.6, 49.4)],
                            [4.6, 3.4, 1.4]), "hide"))                # ear
    # Both horns leave the poll; the off one sweeps back, the near one
    # forward, which is what a pair of horns does in profile and what keeps
    # them from reading as a second set of ears.
    P.append(("fill", taper([(40.6, 55), (42.6, 61.4), (47.6, 63.6)],
                            [4.0, 2.4, 1.0]), "far"))
    P.append(("fill", taper([(44, 54.6), (50.6, 58.6), (55.4, 55.6)],
                            [4.2, 2.6, 1.1]), "horn"))
    P.append(("line", smooth([(12, 61), (0, 54.4), (-20, 53), (-30, 50)],
                             closed=False), "rule"))                  # spine
    P.append(("dot", (41.4, 50.4, 1.8), "sclera"))
    P.append(("dot", (41.6, 50.4, 1.0), "eye"))
    P.append(("dot", (52.6, 42.6, 1.1), "eye"))                       # nostril
    return P


def _sheep(lamb=False, lying=False):
    """Facing right. A sheep is a fleece with a face on it: the back is drawn
    as a run of low bumps rather than a smooth line, the wool stops in a hard
    edge at the throat and above the knee, and the head is small, dark and
    carried level. A lamb is the same animal with more leg and more head for
    its body, which is what makes a young thing look young.

    `lying` couches it. This is not the standing animal squashed: the whole
    body drops to within a few units of the ground and the legs FOLD — the
    forelegs tuck forward under the chest and the hind legs disappear beneath
    the haunch — because what says a resting animal is that the belly is on
    the ground and no leg is bearing anything. Scripture has more animals
    lying down than most drawing sets expect: the flocks in ruined Nineveh,
    the remnant no one makes afraid, green pastures, the wolf with the lamb.
    """
    hk = 1.16 if lamb else 1.0            # head, about its own root
    bx = 0.86 if lamb else 1.0            # body length
    lg = 1.18 if lamb else 1.0            # leg length
    dy = -20.5 if lying else 0.0          # the couched body, near the ground

    def H(pts):
        return [(24 + (px - 24) * hk, 40 + (py - 40) * hk + dy)
                for px, py in pts]

    def B(pts):
        return [(px * bx, py + dy) for px, py in pts]

    def L(j):
        return [(px * bx, 3 + (py - 3) * lg) for px, py in j]

    if lying:
        # Folded: the near foreleg out in front with the knee on the ground,
        # the far one just showing behind it, and the hindquarters carrying
        # no leg at all — a couched sheep shows almost none of its legs, and
        # drawing them anyway is what makes a lying animal look broken.
        P = _quadruped([
            ([(13, 10), (19, 5.4), (25, 4)], [7.4, 5.0, 4.2], "far"),
            ([(15, 9), (22, 4.6), (29, 3.4)], [8.2, 5.4, 4.6], "fleece")],
            tuck=4.0)
    else:
        P = _quadruped([
            (L([(15, 26), (15.5, 16), (14.5, 3)]), [7.0, 4.0, 3.6], "far"),
            (L([(-20, 27), (-18, 16), (-19.5, 3)]), [8.0, 4.2, 3.8], "far"),
            (L([(19, 26), (19.5, 16), (18.5, 3)]), [8.0, 4.4, 4.0], "fleece"),
            (L([(-16, 27), (-14, 16), (-15.5, 3)]), [9.0, 4.6, 4.2],
             "fleece")])
    P.append(("fill", taper(B([(-28, 40), (-30, 34), (-29, 29)]),
                            [5, 4, 3]), "fleece"))                    # tail
    P.append(("fill", smooth(B(                       # the fleece, in bumps
        [(24, 40), (25, 46), (21, 50), (16, 52), (10, 54), (3, 52),
         (-4, 54), (-11, 52), (-18, 53), (-24, 49), (-28, 44), (-29, 37),
         (-27, 30), (-22, 26), (-14, 24), (-4, 23.5), (6, 24), (15, 26),
         (21, 31)])), "fleece"))
    # One ear back, one forward: a sheep carries them out sideways, and that
    # is how the pair resolves once the head is turned to profile.
    P.append(("fill", taper(H([(30, 45), (32.8, 49.6), (35.8, 50.6)]),
                            [4.2, 3.4, 1.4]), "far"))
    P.append(("fill", smooth(H(                                       # head
        [(24, 44), (30, 45.4), (35, 42), (37.4, 37), (35.4, 32.6),
         (30, 31.6), (26, 34.6), (23, 39)])), "hair"))
    P.append(("fill", taper(H([(28.4, 44.4), (24.4, 48.6), (20.6, 49.4)]),
                            [4.6, 3.8, 1.6]), "hair"))                # near ear
    P.append(("fill", smooth(H([(37.4, 37), (38.6, 34.6), (36.6, 32.4),
                                (33.4, 32), (32.4, 34.4), (34, 36.8)])),
              "muzzle"))
    P.append(("line", smooth(B([(22.6, 44), (23.4, 37), (25.6, 31.6)]),
                             closed=False), "rule"))            # the wool line
    P.append(("dot", (H([(31.6, 40.4)])[0][0], H([(31.6, 40.4)])[0][1],
                      1.5 * hk), "sclera"))
    P.append(("dot", (H([(31.8, 40.4)])[0][0], H([(31.8, 40.4)])[0][1],
                      0.85 * hk), "eye"))
    return P


def _lion():
    """Facing right. The mane is the whole creature: a dark ruff drawn wide
    enough to swallow the neck, with the face set into it — which is why it
    is laid down before the head and not after. Level back, heavy forequarters
    and a tufted tail carried out behind finish it."""
    P = _quadruped([
        ([(16, 27), (16.5, 15), (15, 3)], [12, 6.5, 5.5], "far"),
        ([(-27, 28), (-23, 15), (-26, 3)], [15, 7.0, 5.8], "far"),
        ([(21, 27), (21.5, 15), (20, 3)], [14, 7.5, 6.2], "hide"),
        ([(-22, 28), (-18, 15), (-21, 3)], [17, 8.0, 6.6], "hide")])
    # The tail hangs and flicks. Carried out behind at leg thickness it reads
    # as a fifth limb, which is what it was doing.
    P.append(("fill", taper([(-33, 46), (-41, 33), (-44, 17)],
                            [4.6, 3.2, 2.4], round_end=False), "hide"))
    P.append(("fill", smooth([(-44, 19), (-40.6, 13), (-44, 5), (-47.6, 13),
                              (-47, 19)]), "hair"))                   # tuft
    P.append(("fill", taper([(20, 46), (28, 50), (34, 50)],
                            [22, 19, 16], round_end=False), "hide"))  # neck
    P.append(("fill", smooth(                                         # body
        [(22, 40), (24, 48), (19, 53), (10, 54), (0, 53), (-12, 53.5),
         (-22, 55), (-30, 52), (-35, 45), (-36, 36), (-33, 28), (-26, 24),
         (-14, 23), (-2, 23.5), (10, 25), (18, 30)]), "hide"))
    P.append(("dot", (28.6, 60.4, 3.2), "hide"))                      # ears
    P.append(("dot", (36.4, 60.0, 3.0), "hide"))
    # The mane is drawn ragged rather than round: a smooth circle round the
    # face reads as a bear, and the ruff is the one mark that has to carry.
    P.append(("fill", smooth(
        [(22.6, 61), (29.4, 67.4), (35, 60.6), (41.6, 65), (46.6, 56),
         (49.6, 50), (45.4, 42.4), (49, 35.4), (41.6, 32.6), (36.6, 27.6),
         (29.4, 31.4), (22.6, 26.6), (17.6, 35.6), (14.6, 44.6),
         (17.4, 55)]), "hair"))
    P.append(("line", smooth([(-18, 52), (-25, 41), (-27, 30)], closed=False),
              "rule"))                                          # the haunch
    P.append(("fill", smooth(                                         # face
        [(33, 55), (41, 54), (47, 49), (48, 43), (44, 38.6), (37, 38.6),
         (32, 43), (30, 49)]), "hide"))
    P.append(("fill", smooth([(48, 43), (49.4, 40.6), (47.6, 38.4),
                              (44.4, 38), (43.2, 40.4), (44.8, 42.8)]),
              "muzzle"))
    P.append(("dot", (40.4, 48.4, 1.9), "sclera"))
    P.append(("dot", (40.6, 48.4, 1.0), "eye"))
    P.append(("dot", (47.4, 40.4, 1.0), "eye"))                       # nostril
    return P


def _wolf():
    """Facing right. Everything that tells a wolf from a dog is in the
    outline, so the outline is where the work goes: a deep narrow chest over
    a tucked belly, legs longer than they look right for the body, a straight
    tail carried low and heavy, ears held stiffly up, and a long muzzle on a
    head the neck carries LEVEL rather than above the shoulder. Draw the head
    high and it is a dog; drop it to the line of the back and it is a wolf.
    """
    P = _quadruped([
        ([(14, 26), (15.5, 15), (13.5, 3)], [8.6, 4.8, 4.0], "far"),
        ([(-23, 27), (-19, 15), (-22, 3)], [10.4, 5.2, 4.2], "far"),
        ([(19, 26), (20.5, 15), (18.5, 3)], [9.6, 5.4, 4.4], "hide"),
        ([(-18, 27), (-14, 15), (-17, 3)], [11.6, 5.8, 4.6], "hide")])
    # low and straight, not curled — a curled tail is every domestic dog
    P.append(("fill", taper([(-28, 40), (-37, 33), (-46, 24)],
                            [7.2, 5.4, 3.0]), "hair"))
    P.append(("fill", taper([(18, 42), (28, 45), (36, 45.4)],
                            [15, 12.6, 10.4], round_end=False), "hide"))
    P.append(("fill", smooth(                                        # body
        [(20, 36), (21, 44), (16, 48), (6, 49), (-4, 48), (-14, 48.6),
         (-23, 49), (-29, 45), (-31, 38), (-28, 31), (-20, 27.6),
         (-8, 27), (2, 26.4), (11, 27.6), (17, 31)]), "hide"))
    P.append(("line", smooth([(-15, 47), (-21, 38), (-23, 30)], closed=False),
              "rule"))                                               # haunch
    P.append(("line", smooth([(6, 27.4), (0, 30.6), (-8, 29.6)],
                             closed=False), "rule"))                 # the tuck
    for ex, tilt in ((33.6, -1.6), (39.4, 0.4)):                     # ears
        P.append(("fill", smooth([(ex - 3.2, 49), (ex + tilt, 58.6),
                                  (ex + 3.4, 49)]), "hair"))
    P.append(("fill", smooth(                                        # head
        [(33, 50.4), (40, 50), (44, 47), (45.6, 43), (43, 39.6), (37, 39),
         (32.4, 41.6), (30.4, 46)]), "hide"))
    P.append(("fill", taper([(43, 44), (50, 42.4), (55.4, 41.4)],
                            [8.4, 6.6, 5.0], round_end=False), "hide"))
    P.append(("fill", smooth([(55.4, 43.4), (57.4, 42), (56.6, 39.6),
                              (53.4, 39), (52, 40.8), (53, 43)]), "muzzle"))
    P.append(("dot", (39.6, 46.4, 1.7), "sclera"))
    P.append(("dot", (39.8, 46.4, 0.95), "eye"))
    P.append(("dot", (56.4, 41, 0.95), "eye"))                       # nostril
    return P


def _dog():
    """Facing right. The pariah dog of the streets, which is the only dog
    scripture has — it eats what is thrown out, licks sores, and returns to
    its vomit, and it is never once a pet.

    Built from the wolf and separated from it by the two marks the wolf's
    docstring names as the whole difference: the head is carried ABOVE the
    line of the back rather than level with it, and the tail curls up over
    the haunch instead of hanging straight. Lighter in the chest and shorter
    in the leg as well, but those two are what read at forty pixels.
    """
    P = _quadruped([
        ([(13, 24), (14.5, 14), (12.5, 3)], [7.6, 4.4, 3.6], "far"),
        ([(-21, 25), (-17.5, 14), (-20, 3)], [9.2, 4.8, 3.8], "far"),
        ([(17.5, 24), (19, 14), (17, 3)], [8.6, 5.0, 4.0], "hide"),
        ([(-16.5, 25), (-13, 14), (-15.5, 3)], [10.4, 5.2, 4.2], "hide")])
    P.append(("fill", taper([(-26, 38), (-33, 47), (-28, 55)],
                            [5.6, 4.2, 2.6]), "hide"))          # the curl
    P.append(("fill", taper([(17, 40), (25, 47), (31, 51)],
                            [13, 11, 9.2], round_end=False), "hide"))
    P.append(("fill", smooth(                                   # body
        [(19, 34), (20, 42), (15, 45.6), (5, 46.6), (-4, 45.6), (-13, 46),
         (-21, 46.4), (-26.6, 42.6), (-28.4, 36), (-25.6, 29.6),
         (-18, 26.6), (-7, 26), (2, 25.4), (10.4, 26.6), (16, 29.6)]),
        "hide"))
    P.append(("line", smooth([(-14, 44.6), (-19.4, 36), (-21, 29)],
                             closed=False), "rule"))            # haunch
    for ex, tilt in ((29.4, -2.4), (34.6, 0.6)):                # ears, folded
        P.append(("fill", smooth([(ex - 3.4, 54), (ex + tilt, 61.6),
                                  (ex + 4.4, 55.4)]), "hide"))
    P.append(("fill", smooth(                                   # head, raised
        [(28.4, 55.6), (35, 55), (39, 52), (40.4, 48), (38, 44.6), (32, 44),
         (27.6, 46.6), (25.8, 51)]), "hide"))
    P.append(("fill", taper([(38, 49.4), (44.4, 48), (49, 47.2)],
                            [7.6, 6.0, 4.6], round_end=False), "hide"))
    P.append(("fill", smooth([(49, 49), (50.8, 47.6), (50, 45.4), (47, 45),
                              (45.8, 46.6), (46.8, 48.6)]), "muzzle"))
    P.append(("dot", (34.6, 51.4, 1.6), "sclera"))
    P.append(("dot", (34.8, 51.4, 0.9), "eye"))
    P.append(("dot", (49.8, 46.8, 0.9), "eye"))                 # nostril
    return P


def _sow():
    """Facing right, head down — which is where a pig's head lives.

    A pig is a wedge: heaviest at the shoulder, tapering to a snout carried
    low and forward, on legs far too short for the mass above them. Get the
    proportion of body to leg wrong and the animal reads as a sheep with a
    bad head. The snout disc is the one mark that is unmistakably swine, so
    it is drawn flat-on and given its own material.
    """
    P = _quadruped([
        ([(13, 18), (14, 11), (12.5, 3)], [8.6, 5.0, 4.2], "far"),
        ([(-18, 19), (-15.5, 11), (-17.5, 3)], [10.0, 5.4, 4.4], "far"),
        ([(17, 18), (18, 11), (16.5, 3)], [9.6, 5.6, 4.6], "hide"),
        ([(-14, 19), (-11.5, 11), (-13.5, 3)], [11.4, 6.0, 4.8], "hide")],
        tuck=8.0)
    P.append(("fill", taper([(-25, 30), (-31, 36), (-29, 41)],
                            [4.0, 3.0, 2.0]), "hide"))          # curled tail
    P.append(("fill", smooth(                                   # the wedge
        [(24, 30), (22, 38), (14, 41), (4, 42), (-6, 41.4), (-16, 40),
         (-23, 37), (-26.4, 31), (-25, 24), (-19, 20.4), (-8, 19),
         (4, 18.6), (15, 20), (22, 23)]), "hide"))
    P.append(("line", smooth([(-15, 39), (-20, 31), (-21.4, 24)],
                             closed=False), "rule"))
    P.append(("fill", smooth([(22, 36), (27.6, 33), (30, 27),        # head
                              (28, 21.4), (22, 19.6), (18, 23)]), "hide"))
    P.append(("fill", smooth([(24.6, 35.4), (29.4, 37.6), (30.4, 32.6),
                              (27, 31)]), "hide"))                        # ear
    P.append(("fill", taper([(28, 26.6), (33.4, 24.4), (37, 23)],
                            [8.0, 6.6, 5.4], round_end=False), "hide"))
    # The snout is the one mark that is unmistakably swine at any size, so it
    # is drawn a little larger than life and given the flat face-on disc a
    # pig's nose actually presents.
    P.append(("dot", (37.8, 22.6, 4.3), "muzzle"))
    P.append(("dot", (38.8, 23.8, 0.95), "eye"))
    P.append(("dot", (38.8, 21.2, 0.95), "eye"))
    P.append(("dot", (26.4, 28.6, 1.5), "sclera"))
    P.append(("dot", (26.6, 28.6, 0.85), "eye"))
    return P


def _serpent(spine=None, raised=True, girth=8.6, pattern=None):
    """A serpent laid along a path.

    `spine` is the line it follows, head first, in local units — so the same
    creature runs down a branch, coils on a rock, or lies flat, and a scene
    that already knows the path the snake takes can hand that path straight
    over. Without one, `raised` gives the posture of verse 1, the serpent more
    subtil than any beast of the field, or dropped, the sentence of verse 14:
    upon thy belly shalt thou go. Both are the same creature, which is the
    point the chapter makes.

    The girth runs thin at the tail, thickest a third of the way back from the
    head, and narrows again into a neck — a snake of even thickness reads as a
    rope, and one that tapers straight from head to tail reads as a carrot.
    """
    if spine is None:
        spine = ([(26, 36), (22, 24), (14, 12), (2, 5), (-12, 8), (-26, 4),
                  (-40, 9), (-55, 3)] if raised else
                 [(30, 6), (18, 3), (4, 8), (-10, 3), (-24, 8), (-38, 4),
                  (-48, 8), (-58, 3)])
    n = len(spine)
    ws = []
    for i in range(n):
        t = i / (n - 1)                      # 0 at the head, 1 at the tail
        if t < 0.30:
            k = 0.62 + (1.0 - 0.62) * (t / 0.30)   # a neck behind the head
        else:
            k = 1.0 - 0.86 * ((t - 0.30) / 0.70) ** 1.25
        ws.append(girth * k)

    P = [("fill", taper(spine[::-1], ws[::-1]), "hide")]

    # The head is built along the body's own direction, so it points where the
    # serpent points however the path is bent.
    hx, hy = spine[0]
    dx, dy = hx - spine[1][0], hy - spine[1][1]
    L = math.hypot(dx, dy) or 1.0
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    g = girth * 0.5

    def A(a, b):
        return (hx + ux * a * g + nx * b * g, hy + uy * a * g + ny * b * g)

    P.append(("fill", smooth(
        [A(-0.6, 0.72), A(0.7, 1.34), A(2.2, 1.16), A(3.3, 0.42),
         A(3.4, 0.0), A(3.3, -0.42), A(2.2, -1.16), A(0.7, -1.34),
         A(-0.6, -0.72)]), "hide"))
    P.append(("line", [A(3.4, 0.06), A(4.9, 0.06), A(6.3, 0.66)], "rule"))
    P.append(("line", [A(4.9, 0.06), A(6.3, -0.54)], "rule"))     # the tongue
    if pattern is None:                      # only worth it on a big one
        pattern = spine is None
    if pattern:                              # one line down the back, no more
        P.append(("line", smooth([(px, py + ws[i] * 0.30)
                                  for i, (px, py) in enumerate(spine)],
                                 closed=False), "rule"))
    ex, ey = A(1.6, 0.56)
    P.append(("dot", (ex, ey, girth * 0.20), "sclera"))
    P.append(("dot", (ex + girth * 0.03, ey, girth * 0.11), "eye"))
    return P


# A bird has to be able to be doing something. Genesis 1 fills a sky with
# them, and a sky of identical birds in identical attitudes reads as wallpaper
# — what makes a flock alive is that no two are at the same point of the same
# stroke. So the wings are the parameter, and the body underneath never moves.

_WINGS = {
    "glide": [(3, 9), (16, 10.4), (28, 7), (38.4, 0.6), (27, -2.4),
              (14, -1.4), (4, 1)],
    "up": [(2.6, 8), (11, 15), (20, 24), (28.4, 33.6), (32, 30.4),
           (25, 20), (16, 11.4), (6, 3.6)],
    "down": [(2.6, 9), (11, 2.6), (20.4, -5.6), (28.6, -15), (32, -11),
             (26, -1.6), (17.6, 6), (6, 12)],
    "beat": [(3, 9), (14, 13.6), (25, 15), (35, 12), (27, 4), (15, 1.6),
             (4, 1)],
}


def _bird(pose="glide"):
    """On the wing, seen from below — the way a bird over a man's head is
    actually seen, and the only view of one that reads at a glance.

    A bird drawn in profile resolves into three loose leaves: the near wing,
    the off wing and the body never lock together, because in profile a wing
    is edge-on and has no shape. From beneath, the spread is symmetrical and
    the silhouette is the bird. Local y runs up the bird's own length, head at
    the top; the caller leans it with `rot` to give it a heading.

    `pose` is where in the stroke it is caught: level and soaring, wings up,
    wings down, or part way. See _WINGS.
    """
    P = []
    wing = _WINGS.get(pose, _WINGS["glide"])
    for sx in (-1, 1):
        P.append(("fill", smooth([(sx * px, py) for px, py in wing]), "wing"))
    P.append(("fill", smooth([(-2.6, -13), (-7.6, -26), (0, -22.4),
                              (7.6, -26), (2.6, -13)]), "wing"))      # tail
    P.append(("fill", smooth([(0, 15), (3.6, 8), (4.2, -2), (2.6, -12),
                              (0, -16), (-2.6, -12), (-4.2, -2),
                              (-3.6, 8)]), "hide"))
    P.append(("dot", (0, 16.6, 3.4), "hide"))                         # head
    P.append(("fill", smooth([(-1.6, 19), (0, 23.6), (1.6, 19)]), "horn"))
    # the pinions, laid along whatever the wing is doing
    n = len(wing)
    for sx in (-1, 1):
        for k in (0.30, 0.46, 0.62):
            i = 1 + int(k * (n - 3))
            lx, ly = wing[i]
            tx, ty = wing[n - 1 - i]
            P.append(("line", [(sx * lx, ly),
                               (sx * (lx * 0.36 + tx * 0.64),
                                ly * 0.36 + ty * 0.64)], "rule"))
    return P


# Seen side on. The from-below bird cannot serve a bird going somewhere — a
# raven sent out of an ark, a fowl crossing a sky band — because from below it
# has no heading, only a spread.
#
# What sank the first attempt at a profile bird was drawing both wings at the
# same weight, as two lens shapes standing off the body: near wing, off wing
# and body never locked together and it read as three loose leaves. The fix is
# that in profile the wings are NOT equal. The near one is the whole bird —
# broad at the root, swept, tapering to its primaries, and rooted inside the
# body outline. The off one is a sliver showing past the far side, no more.

_PROFILE = {                            # (near wing, off wing)
    "up": ([(9, 4), (3, 17), (-9, 29), (-23, 35), (-18.6, 26), (-6.6, 14.6),
            (1.6, 4)],
           [(3, -3), (-4, -11), (-14, -17), (-8.6, -8), (-1, -2)]),
    "down": ([(9, -2), (3, -15), (-9, -27), (-23, -33), (-18.6, -24),
              (-6.6, -12.6), (1.6, -2)],
             [(3, 3), (-4, 11), (-14, 17), (-8.6, 8), (-1, 2)]),
    "glide": ([(9, 3.5), (1, 10), (-11, 15.4), (-25, 16.6), (-19, 10),
               (-7, 4.6), (1, 1.6)],
              [(3, -2.6), (-5, -6.6), (-15, -8.6), (-8, -4), (-1, -1.6)]),
}


def _bird_profile(pose="up"):
    """A bird on the wing, side on and facing right.

    The body alone reads as a bird before any wing is added — breast forward,
    head up and out, tail swept behind — which is what lets the one near wing
    do the rest of the work.
    """
    near, off = _PROFILE.get(pose, _PROFILE["up"])
    P = [("fill", smooth(off), "far")]
    P.append(("fill", smooth([(-21, 2), (-34, 6.6), (-39.4, 2), (-36, -2.4),
                              (-22, -3)]), "wing"))                  # tail
    for k in (0.34, 0.62):                                           # its vanes
        P.append(("line", [(-23, 1.4 - 2 * k), (-36 - k, 4.4 - 7 * k)],
                  "rule"))
    P.append(("fill", smooth(
        [(22, 1), (17, 5.5), (8, 7.5), (-2, 7), (-13, 4.5), (-21, 1.5),
         (-24, -0.5), (-19, -4), (-8, -7), (3, -7.5), (13, -5.5),
         (19, -2.5)]), "hide"))                                      # body
    P.append(("dot", (24.4, 4.4, 4.2), "hide"))                      # head
    P.append(("fill", smooth([(28.2, 5.4), (36.4, 3.4), (28.2, 1.6)]),
              "horn"))                                               # beak
    P.append(("fill", smooth(near), "wing"))
    n = len(near)
    for k in (0.28, 0.48, 0.68):                                     # pinions
        i = 1 + int(k * (n - 3))
        lx, ly = near[i]
        tx, ty = near[n - 1 - i]
        P.append(("line", [(lx, ly), (lx * 0.34 + tx * 0.66,
                                      ly * 0.34 + ty * 0.66)], "rule"))
    P.append(("dot", (25.8, 5.0, 1.0), "eye"))
    return P


def _dove(descending=True):
    """A dove, side on and facing right — and by default coming DOWN.

    Its own subject rather than a recolour of `bird`, because the two are
    different silhouettes: a dove is short-necked and deep-breasted with a
    small round head and a stubby beak, where the generic bird is drawn long
    and raptor-ish. At the size a verse gives one, that difference is the
    whole of what makes it a dove and not a hawk.

    `descending` is the posture Luke 3:22 needs and no other bird here has:
    wings thrown UP and back, tail fanned and forward, breast rotated toward
    the ground. A bird gliding level, dropped onto a scene about something
    settling on someone, reads as a bird that happens to be passing.
    """
    P = []
    tilt = -0.30 if descending else 0.0
    ca, sa = math.cos(tilt), math.sin(tilt)

    def R(pts):
        return [(px * ca - py * sa, px * sa + py * ca) for px, py in pts]

    # A wing is a SWEPT BLADE — root forward, tip carried back, leading and
    # trailing edges diverging from a narrow root. Authored as a closed
    # lozenge it comes out a paddle, which is what the first attempt did. So
    # both wings borrow the profile bird's own point structure, lifted higher
    # and lengthened for a bird braking on the way down.
    lift = 1.22 if descending else 1.0
    far = [(px * lift, py * lift * (-1 if descending else 1))
           for px, py in ((3, -3), (-4, -11), (-14, -17), (-8.6, -8),
                          (-1, -2))]
    P.append(("fill", smooth(R(far)), "far"))
    # the fanned tail — broad and blunt, not the generic bird's swept point
    P.append(("fill", smooth(R([(-17, 1), (-31, 7), (-35, 2), (-33, -4),
                                (-29, -8), (-17, -4)])), "wing"))
    for k in (0.3, 0.5, 0.7):
        P.append(("line", R([(-19, 1 - 3 * k), (-32.4, 5 - 11 * k)]), "rule"))
    P.append(("fill", smooth(R(                                     # body
        [(19, 0.5), (14, 5.5), (5, 8), (-4, 7.5), (-13, 4), (-18, 0.5),
         (-15, -4.5), (-6, -8), (4, -8.5), (13, -5.5), (17, -2.5)])),
        "fleece"))
    P.append(("dot", R([(21.6, 5.2)])[0] + (5.0,), "fleece"))        # head
    P.append(("fill", smooth(R([(25.4, 6.0), (31.4, 4.6), (25.4, 2.8)])),
              "horn"))                                              # beak
    near = [(px * lift, py * lift) for px, py in
            ((9, 4), (3, 17), (-9, 29), (-23, 35), (-18.6, 26),
             (-6.6, 14.6), (1.6, 4))]
    P.append(("fill", smooth(R(near)), "wing"))
    for k in (0.3, 0.55, 0.8):                                      # pinions
        i = 1 + int(k * (len(near) - 3))
        lx, ly = near[i]
        tx, ty = near[len(near) - 1 - i]
        P.append(("line", R([(lx, ly), (lx * 0.4 + tx * 0.6,
                                        ly * 0.4 + ty * 0.6)]), "rule"))
    P.append(("dot", R([(22.8, 5.8)])[0] + (0.95,), "eye"))
    return P


def _fish():
    """Facing right, on its own centreline rather than a ground line — a
    swimming thing has no feet, so local y = 0 runs through the body and the
    caller places it at the height it swims."""
    P = []
    P.append(("fill", smooth([(-27, 3), (-42, 15), (-47, 12), (-44, 0),
                              (-47, -12), (-42, -15), (-27, -3)]), "fin"))
    P.append(("fill", smooth([(3, 14), (10, 22.5), (20, 20), (26, 10.5)]),
              "fin"))                                                # dorsal
    P.append(("fill", smooth([(-2, -16), (-9, -26), (3, -20)]), "fin"))
    P.append(("fill", smooth(
        [(50, 0), (40, 8), (26, 14), (10, 16.5), (-6, 15), (-20, 10),
         (-29, 4), (-29, -4), (-20, -11), (-6, -17), (10, -18), (26, -15),
         (40, -8)]), "hide"))
    P.append(("fill", smooth([(19, -6), (8, -15), (21, -12)]), "fin"))
    P.append(("line", smooth([(35, 10.6), (30, 0), (34, -11)], closed=False),
              "rule"))                                               # gill
    P.append(("line", smooth([(28, 3), (4, 2), (-24, 1)], closed=False),
              "rule"))                                               # lateral
    P.append(("line", [(50, 0), (43.6, -2.6)], "rule"))              # mouth
    P.append(("dot", (40, 4.6, 2.1), "sclera"))
    P.append(("dot", (40.4, 4.6, 1.0), "eye"))
    return P


def _nephilim():
    """The giant of Genesis 6:4 and Numbers 13:33.

    Small head, heavy shoulders, bare and armed — deliberately the opposite
    build to the robed man, so the two tell apart in silhouette alone. The
    size does the rest: drawn at the same scale as a man he is half again as
    tall, which is the whole of what the verses say about him.
    """
    P = []
    P.append(("fill", taper([(31, 4), (28.5, 60), (26.6, 100)],
                            [3.4, 3.8, 3.4], round_end=False), "wood"))
    P.append(("fill", smooth([(26.6, 100), (22.6, 109), (26, 122),
                              (30.2, 109)]), "metal"))               # spear
    P.append(("fill", taper([(-18, 76), (-26.5, 63), (-25, 44)],
                            [11.5, 8.4, 6], round_end=False), "skin"))
    P.append(("dot", (-25.2, 41.6, 3.6), "skin"))                    # fist
    for sx in (-1, 1):
        P.append(("fill", taper([(sx * 7.5, 32), (sx * 9.5, 18), (sx * 8, 4)],
                                [14, 9, 6.6], round_end=False), "skin"))
        P.append(("fill", smooth([(sx * 8 - 6, 4), (sx * 8 + 6, 4),
                                  (sx * 8 + 7, 0), (sx * 8 - 6.6, 0)]),
                  "skin"))
    P.append(("fill", smooth(                                        # torso
        [(-19, 78), (-20.5, 70), (-15.5, 60), (-11, 50), (-11.5, 44),
         (11.5, 44), (11, 50), (15.5, 60), (20.5, 70), (19, 78), (10, 82.5),
         (0, 83.5), (-10, 82.5)]), "skin"))
    P.append(("fill", taper([(0, 78), (0, 86)], [8.4, 7.6],
                            round_end=False), "skin"))               # neck
    P.append(("dot", (0, 91, 6.8), "skin"))
    P.append(("fill", smooth([(-6.2, 90), (-6.6, 83), (-3.4, 77.6),
                              (0, 76.6), (3.4, 77.6), (6.6, 83), (6.2, 90),
                              (0, 91.6)]), "hair"))                  # beard
    P.append(("fill", smooth([(-8.0, 90.4), (-8.8, 95.4), (-5.6, 99.6),
                              (0, 101), (5.6, 99.6), (8.8, 95.4),
                              (8.0, 90.4), (4.4, 93.4), (0, 94.2),
                              (-4.4, 93.4)]), "hair"))
    P.append(("fill", smooth([(-13.8, 47), (13.8, 47), (15.8, 32),
                              (13, 28.6), (0, 27), (-13, 28.6),
                              (-15.8, 32)]), "robe"))                # kilt
    P.append(("line", smooth([(-14.8, 31.4), (0, 29.2), (14.8, 31.4)],
                             closed=False), "rule"))
    P.append(("fill", taper([(18, 76), (25.5, 65), (26.6, 55)],
                            [11.5, 8.4, 6], round_end=False), "skin"))
    P.append(("dot", (26.8, 52.4, 3.6), "skin"))                     # grip
    P.append(("line", smooth([(-13.8, 47), (0, 44.4), (13.8, 47)],
                             closed=False), "rule"))                 # belt
    for f in ([(-7, 45), (-8.6, 37), (-10, 30)],
              [(0, 45), (0.6, 37), (0.6, 29)],
              [(7, 45), (8.6, 37), (10, 30)]):
        P.append(("line", smooth(f, closed=False), "rule"))
    P.append(("line", smooth([(-10, 65), (0, 59.5), (10, 65)],
                             closed=False), "rule"))                 # chest
    return P


# ---------------------------------------------------------------------------
# Made things
# ---------------------------------------------------------------------------
#
# Same conventions as the creatures: local units, sitting on zero, tagged by
# material. These are drawn in elevation, flat on, because a made thing put
# into perspective has to agree with a perspective the rest of the scene does
# not have — and because what the text names is almost always a face of the
# thing (the horns of the altar, the gate of the city) rather than its volume.

_ROUGH = ((1.00, 0.88, 1.06, 0.92, 1.04, 0.90),      # stones are not round,
          (0.92, 1.06, 0.90, 1.04, 0.94, 1.02),      # and no two alike
          (1.06, 0.94, 1.02, 0.88, 1.00, 0.96),
          (0.90, 1.02, 0.96, 1.06, 0.92, 1.00))


def _stone(cx, cy, w, h, i=0):
    """One unhewn stone. The irregularity is table-driven rather than random
    so a chapter redrawn tomorrow has the same stones in it as today."""
    k = _ROUGH[i % len(_ROUGH)]
    pts = []
    for j, (dx, dy) in enumerate(((-1, -0.4), (-0.7, 0.75), (0, 1),
                                  (0.7, 0.75), (1, -0.4), (0, -1))):
        pts.append((cx + dx * w / 2 * k[j], cy + dy * h / 2 * k[(j + 2) % 6]))
    return smooth(pts)


def _crenels(P, x0, x1, y, w, h, mat="stone"):
    """The battlement along the top of a wall — the one mark that makes a
    block of masonry read as a fortification and not as a box."""
    n = max(2, int((x1 - x0) // (w * 2)))
    step = (x1 - x0 - w) / max(1, n - 1)
    for i in range(n):
        bx = x0 + i * step
        P.append(("fill", [(bx, y), (bx + w, y), (bx + w, y + h),
                           (bx, y + h)], mat))
    return P


def _wheel(P, cx, cy, r, mat="wood", spokes=8):
    """A spoked wheel: a rim with the page punched out of it, so whatever the
    cart is standing in front of shows through between the spokes."""
    P.append(("dot", (cx, cy, r), mat))
    P.append(("dot", (cx, cy, r * 0.80), "void"))
    for i in range(spokes):
        a = math.pi * 2 * i / spokes
        P.append(("line", [(cx + math.cos(a) * r * 0.13,
                            cy + math.sin(a) * r * 0.13),
                           (cx + math.cos(a) * r * 0.80,
                            cy + math.sin(a) * r * 0.80)], "rule"))
    P.append(("dot", (cx, cy, r * 0.16), mat))
    return P


def _fire(P, cx, gy, w, h):
    """Fire on an altar: three tongues, uneven, the tallest off centre.
    Three even tongues read as a crown."""
    for dx, k, lean in ((-0.30, 0.66, -0.16), (0.06, 1.00, 0.10),
                        (0.34, 0.74, 0.20)):
        bx = cx + dx * w
        P.append(("fill", smooth(
            [(bx - w * 0.14, gy), (bx - w * 0.17, gy + h * k * 0.42),
             (bx + lean * w * 0.5, gy + h * k),
             (bx + w * 0.17, gy + h * k * 0.44),
             (bx + w * 0.15, gy)]), "fire"))
    return P


def _altar(kind="stone", fire=False):
    """An altar. Two of them, because scripture builds two different things.

    The unhewn heap is what Noah, Abraham, Gideon and Elijah raise — "thou
    shalt not build it of hewn stone, for if thou lift up thy tool upon it,
    thou hast polluted it" — so it is drawn as stones that were carried, not
    cut. The horned altar is the made one of Exodus 27: squared, bronze, its
    grate halfway up, its poles through the rings, and the four horns that
    the man fleeing for his life lays hold of.
    """
    P = []
    if kind == "stone":
        for i, (cx, cy, w, h) in enumerate(
                [(-23, 7, 20, 15), (-7.5, 6.5, 18, 14), (8, 7, 19, 15),
                 (23.5, 6.5, 19, 14),
                 (-16, 20, 19, 14), (0, 19.5, 18, 13), (16, 20, 19, 14),
                 (-8, 32, 18, 13), (8, 32, 18, 13)]):
            P.append(("fill", _stone(cx, cy, w, h, i), "stone"))
        P.append(("fill", smooth([(-25, 37), (25, 37), (27, 41), (24, 45),
                                  (-24, 45), (-27, 41)]), "stone"))
        if fire:
            _fire(P, 0, 44, 26, 30)
    else:
        # Nothing here is smoothed. A made thing of boards and bronze has
        # corners, and run through the curve fitter its horns come out as
        # lumps and its box as a cushion.
        for sx in (-1, 1):                       # the two horns behind
            P.append(("fill", [(sx * 30, 52), (sx * 38, 52), (sx * 41, 67),
                               (sx * 36.5, 67), (sx * 34, 56)], "far"))
        P.append(("fill", [(-46, 0), (46, 0), (40, 56), (-40, 56)], "metal"))
        for sx in (-1, 1):                       # the horns of the altar
            P.append(("fill", [(sx * 36, 54), (sx * 45, 54), (sx * 48.5, 71),
                               (sx * 43.5, 71), (sx * 40.5, 58)], "metal"))
        P.append(("fill", [(-43.4, 24), (43.4, 24), (42.6, 32),   # the grate,
                           (-42.6, 32)], "void"))                 # halfway up
        for gx in range(-38, 42, 7):
            P.append(("line", [(gx, 24), (gx, 32)], "rule"))
        P.append(("fill", [(-58, 36), (58, 36), (58, 40.5), (-58, 40.5)],
                  "wood"))                                        # the poles
        for sx in (-1, 1):                                        # the rings
            P.append(("dot", (sx * 41.4, 38.2, 4.2), "metal"))
            P.append(("dot", (sx * 41.4, 38.2, 2.4), "void"))
        if fire:
            _fire(P, 0, 56, 30, 34)
    return P


def _boat():
    """A small vessel, facing right: the fishing boat of the lake and the ship
    of Jonah are the same hull at different sizes. Prow and stern both rise —
    a hull drawn flat-ended reads as a trough."""
    P = []
    P.append(("fill", taper([(-6, 100), (-6, 26)], [3.4, 4.0],
                            round_end=False), "wood"))           # the mast
    P.append(("fill", taper([(-10, 84), (48, 77)], [3.0, 2.4],
                            round_end=False), "wood"))           # the yard
    P.append(("fill", smooth(                                    # the sail
        [(-6, 81), (20, 79), (44, 73), (53, 57), (47, 38), (20, 33),
         (-6, 32)], n=3), "cloth"))
    for k in (0.30, 0.55, 0.80):                                 # its seams
        P.append(("line", smooth([(-6 + 52 * k, 80 - 9 * k),
                                  (-6 + 54 * k, 33 - 1 * k)],
                                 closed=False), "rule"))
    P.append(("fill", smooth(
        [(-76, 44), (-70, 22), (-52, 12), (-20, 8), (20, 8), (52, 12),
         (70, 22), (76, 44), (64, 34), (44, 26), (10, 22), (-24, 22),
         (-52, 26), (-64, 34)]), "wood"))                        # the hull
    for k in (-40, -14, 14, 40):                                 # the strakes
        P.append(("line", [(k - 9, 21.4), (k + 9, 21.4)], "rule"))
    P.append(("fill", taper([(-66, 30), (-88, 12)], [4.0, 6.4],
                            round_end=False), "wood"))           # steering oar
    P.append(("line", smooth([(-70, 26), (0, 20), (70, 26)], closed=False),
              "rule"))                                           # the gunwale
    return P


def _cart():
    """A two-wheeled cart, facing right — the cart the ark was set on and the
    wagon that carried Jacob down into Egypt. The pole runs forward to the
    yoke, so a cart and an ox drawn at the same scale meet where they should.
    """
    P = []
    # A wheel's centre sits one radius up, or the cart stands in a rut of its
    # own making.
    _wheel(P, -18, 21.5, 21.5, "far", spokes=6)                  # the off wheel
    P.append(("fill", [(-44, 30), (36, 30), (36, 34), (-44, 34)], "wood"))
    P.append(("fill", [(-46, 34), (38, 34), (38, 52), (-46, 52)],
              "wood"))                                           # the bed
    for gx in range(-38, 36, 9):                                 # its boards
        P.append(("line", [(gx, 36), (gx, 50)], "rule"))
    P.append(("fill", taper([(38, 40), (86, 26), (114, 22)],
                            [7.0, 5.4, 4.6], round_end=False), "wood"))
    P.append(("fill", [(108, 14), (118, 14), (118, 30), (108, 30)], "wood"))
    _wheel(P, -4, 24, 24, "wood", spokes=6)                      # the near one
    return P


def _manger(straw=True, light=True):
    """A feeding trough on crossed trestles, front on.

    Two things make it a manger and not a box. The first is the TRESTLES:
    the X under each end is the whole silhouette, and a trough on four
    straight legs reads as a table. The second is that its mouth is OPEN —
    drawn as the page punched through the top of the vessel, so the eye goes
    into it rather than across a flat front. Everything a manger is ever
    drawn for is what is lying in it.

    `light` fills that mouth with the brightest material there is and domes
    it above the rim. It is not a lamp set in a trough: no source is drawn,
    because the point of the picture is that the thing in the manger is
    itself the light. `straw` lays a few stalks over the rim, which is what
    keeps the glow from reading as an appliance.
    """
    P = []
    for sx in (-1, 1):                                   # the two trestles
        bx = sx * 33
        P.append(("fill", taper([(bx - 16, 0), (bx + 14, 37)], [4.4, 3.6],
                                round_end=False), "wood"))
        P.append(("fill", taper([(bx + 16, 0), (bx - 14, 37)], [4.4, 3.6],
                                round_end=False), "wood"))
        P.append(("line", [(bx - 13, 12), (bx + 13, 12)], "rule"))
    P.append(("fill", [(-44, 30), (44, 30), (54, 54), (-54, 54)], "wood"))
    for gx in (-30, -10, 10, 30):                        # its boards
        P.append(("line", [(gx * 1.18, 32), (gx, 52)], "rule"))
    mouth = smooth([(-54, 54), (0, 47), (54, 54), (0, 61)], n=5)
    P.append(("fill", mouth, "void"))
    if light:
        # A LENS lying in the mouth, cresting a little over the rim — not a
        # dome sitting on top of it, which was the first cut and read as a
        # loaf of bread on a trestle table. It has to be seen to be down
        # inside the trough, with the dark of the mouth still showing at
        # both ends, or the manger stops being open.
        P.append(("fill", smooth([(-38, 53), (0, 46), (38, 53),
                                  (21, 63), (0, 67), (-21, 63)], n=5),
                  "fire"))
    if straw:
        # Laid over the light, not under it: a stalk crossing the glow is
        # what says the light is IN the straw rather than a lamp standing
        # behind the trough.
        for x0, x1, y1 in ((-40, -50, 62), (-16, -24, 65), (12, 6, 66),
                           (36, 46, 63), (46, 54, 60)):
            P.append(("line", [(x0, 55), (x1, y1)], "rule"))
    return P


def _tent():
    """A goat-hair tent, front on. The sag of the ridge between its poles is
    the whole of what makes it cloth: drawn as two straight slopes it reads as
    a roof, and a roof is a house."""
    P = []
    for sx in (-1, 1):                                    # guy ropes and pegs
        P.append(("line", [(sx * 52, 26), (sx * 86, 1)], "rule"))
        P.append(("line", [(sx * 30, 41), (sx * 66, 1)], "rule"))
        P.append(("fill", [(sx * 84, 0), (sx * 88, 0), (sx * 88, 6),
                           (sx * 84, 6)], "wood"))
        P.append(("fill", [(sx * 64, 0), (sx * 68, 0), (sx * 68, 6),
                           (sx * 64, 6)], "wood"))
    P.append(("fill", smooth(
        [(-74, 0), (-58, 22), (-34, 38), (-16, 45), (0, 43), (16, 45),
         (34, 38), (58, 22), (74, 0)], n=4), "hair"))            # the cloth
    for k in (-46, -26, 26, 46):                                 # its seams
        P.append(("line", smooth([(k, 0), (k * 0.42, 34), (k * 0.10, 43)],
                                 closed=False), "rule"))
    P.append(("fill", smooth([(-13, 0), (13, 0), (11, 24), (0, 29),
                              (-11, 24)], n=2), "void"))         # the doorway
    P.append(("fill", taper([(-13, 0), (-15, 26)], [3.0, 2.6],
                            round_end=False), "wood"))           # door poles
    P.append(("fill", taper([(13, 0), (15, 26)], [3.0, 2.6],
                            round_end=False), "wood"))
    return P


def _tree(fruit=0, bare=False):
    """A tree: trunk, two boughs, and a lobed crown.

    The crown is the whole of it. Drawn as a circle on a stick — which is what
    Genesis 1 and 2 have been drawing — it reads as a lollipop and cannot tell
    a fruit tree from a shrub; lobed, with the boughs entering it, it reads as
    a tree at forty pixels. `fruit` hangs that many; `bare` drops the crown for
    the tree in a winter or a curse.
    """
    P = []
    P.append(("fill", taper([(0, 0), (-1, 20), (-3, 44)], [17, 11, 8],
                            round_end=False), "wood"))            # the trunk
    for sx, top in ((-1, 62), (1, 58)):                           # the boughs
        P.append(("fill", taper([(sx * 1, 34), (sx * 11, 48), (sx * 17, top)],
                                [9, 6, 4], round_end=False), "wood"))
    for sx in (-1, 1):                                            # root flare
        P.append(("fill", [(sx * 7, 0), (sx * 15, 0), (sx * 8, 8)], "wood"))
    if not bare:
        # An EVEN lobe count, or the alternation fails to close and the crown
        # comes out lopsided — which reads as a damaged tree, not a full one.
        lobes, n = [], 12
        for i in range(n):
            a = math.pi * 2 * i / n + 0.26
            k = 1.07 if i % 2 else 0.92
            if math.sin(a) < -0.5:                # settle the underside
                k *= 0.88
            lobes.append((math.cos(a) * 40 * k, 70 + math.sin(a) * 31 * k))
        P.append(("fill", smooth(lobes, n=5), "fleece"))
        for k in range(fruit):
            a = 0.7 + k * 1.9
            P.append(("dot", (math.cos(a) * 26, 68 + math.sin(a) * 19, 4.0),
                      "fruit"))
    return P


# Five lobes with SHALLOW notches between them. The depth of the notch is the
# whole difference between a leaf and a star: cut in to two thirds of the
# radius and the thing that comes out is a maple star, whatever the outline
# was called. These sit at about four fifths, and the silhouette stays broad.
_LEAF = [(0, 1.2), (-5.5, 2.5), (-11, 6), (-9.5, 10.5), (-12.5, 15),
         (-7, 17.5), (0, 21.5), (7, 17.5), (12.5, 15), (9.5, 10.5),
         (11, 6), (5.5, 2.5)]


def _leaf(cx, cy, r, rot):
    """One vine leaf, `r` tall, its stem end at (cx, cy) and turned by `rot`.
    The base notch is what makes it read as a leaf rather than a spade."""
    ca, sa = math.cos(rot), math.sin(rot)
    out = []
    for px, py in _LEAF:
        px, py = px * r / 22.0, py * r / 22.0
        out.append((cx + px * ca - py * sa, cy + px * sa + py * ca))
    return out


def _bunch(P, x, y, r=2.7, step=4.9):
    """A hanging cluster: three rows narrowing downward. Individual berries
    rather than one blob, because a blob at this size is a fig."""
    for row, n in enumerate((3, 2, 1)):
        for i in range(n):
            P.append(("dot", (x + (i - (n - 1) / 2) * step,
                              y - row * step * 0.94, r), "fruit"))


def _vine(fruit=2, stake=True):
    """A vine on its stake: the short gnarled stock, the arms trained off it,
    lobed leaves, and the bunches hanging under them.

    Everything that separates a vine from the `_tree` above is deliberate. The
    stock is SHORT and thick and kinked — a vine's wood is old and low, and
    given a straight trunk the drawing becomes a small tree. The leaves sit in
    separate clusters along the arms instead of massing into one crown,
    because a vine is mostly gaps. And the fruit HANGS BELOW the leaves rather
    than sitting in them, which is the one mark no other growing thing here
    has. Take the bunches away and this is a shrub, which is exactly what the
    lollipop it replaces was.

    Scripture has more vines in it than almost anything else that grows —
    Noah's, Naboth's, the song of the vineyard, every man under his own vine,
    the true vine — and the winepress in this module had nothing to fill it.
    """
    P = []
    if stake:                       # a made thing: no curve fitter near it
        P.append(("fill", [(5, 0), (9.4, 0), (9.4, 70), (5, 70)], "wood"))
    P.append(("fill", taper([(0, 0), (-3.4, 12), (1.2, 22), (-1, 32)],
                            [15, 12, 10, 8.6], round_end=False), "wood"))
    for sx in (-1, 1):                                        # root flare
        P.append(("fill", [(sx * 6, 0), (sx * 13, 0), (sx * 7, 7)], "wood"))
    for j in ([(-1, 30), (-14, 40), (-27, 47)],               # the arms
              [(-1, 32), (13, 43), (26, 52)],
              [(-1, 32), (0.5, 46), (3, 60)]):
        P.append(("fill", taper(j, [7.6, 5.0, 3.2], round_end=False), "wood"))
    for a, b in (((-20, 44), (-24, 54)), ((18, 47), (23, 57))):   # tendrils
        mid = ((a[0] + b[0]) / 2 + 4, (a[1] + b[1]) / 2)
        P.append(("line", smooth([a, mid, b], closed=False), "rule"))
    # Authored as a LEAF, not as a radial blob. A ring of points at
    # alternating radii is what the tree's crown does, and at the eight points
    # a cluster this small can afford it comes out a rounded square. The vine
    # leaf is the one leaf in scripture anybody could draw from memory —
    # broad, five-pointed, notched where the stem enters — so it is worth the
    # twelve points it takes.
    for cx, cy, r, rot in ((-28, 52, 15, -0.5), (27, 57, 15, 0.5),
                           (3, 68, 17, 0.06), (-11, 49, 12, -0.9),
                           (14, 48, 12, 0.9)):
        P.append(("fill", smooth(_leaf(cx, cy, r, rot), n=3), "fleece"))
    for bx, by in (((-17, 38), (16, 41), (1, 43))[:max(0, fruit)]):
        _bunch(P, bx, by)
    return P


def _herb():
    """The herb yielding seed of Genesis 1:11 — a stalk, paired leaves and a
    seed head, which is the one part the verse is actually about."""
    P = []
    P.append(("fill", taper([(0, 0), (1, 30), (0, 52)], [6, 4.4, 3.4],
                            round_end=False), "fleece"))
    for sx, y in ((-1, 20), (1, 30), (-1, 40)):
        P.append(("fill", smooth([(sx * 1, y), (sx * 13, y + 9),
                                  (sx * 20, y + 4), (sx * 9, y - 3)]),
                  "fleece"))
    P.append(("dot", (0, 58, 7.0), "fruit"))
    for a in (0.5, 1.6, 2.7):                                     # the seed
        P.append(("line", [(math.cos(a) * 7, 58 + math.sin(a) * 7),
                           (math.cos(a) * 13, 58 + math.sin(a) * 13)],
                  "rule"))
    return P


def _grass():
    """A tuft. Blades of one length read as a comb, so they vary."""
    P = []
    for x0, tip, w in ((-13, (-19, 20), 4.4), (-6, (-9, 30), 4.8),
                       (0, (2, 36), 5.2), (6, (11, 27), 4.8),
                       (12, (18, 17), 4.2)):
        P.append(("fill", taper([(x0, 0), tip], [w, 1.2]), "fleece"))
    return P


def _sun():
    """The greater light. An emblem, not a body: it has no scale against a
    man, so a scene sets its size."""
    P = [("dot", (0, 0, 26), "fire")]
    for i in range(12):
        a = math.pi * 2 * i / 12
        P.append(("fill", [(math.cos(a) * 30, math.sin(a) * 30),
                           (math.cos(a + 0.09) * 44, math.sin(a + 0.09) * 44),
                           (math.cos(a - 0.09) * 44, math.sin(a - 0.09) * 44)],
                  "fire"))
    return P


def _moon():
    """The lesser light: a disc with a disc taken out of it, which is the only
    way a crescent stays a crescent when the page behind it changes."""
    return [("dot", (0, 0, 24), "metal"),
            ("dot", (11, 4, 21), "void")]


def _star(points=5, r=15):
    P, pts = [], []
    for i in range(points * 2):
        a = math.pi * 2 * i / (points * 2) + math.pi / 2
        k = r if i % 2 == 0 else r * 0.42
        pts.append((math.cos(a) * k, math.sin(a) * k))
    P.append(("fill", pts, "fire"))
    return P


def _gate():
    """The gate of a city: two towers, the curtain wall between them, and the
    arch. This is where the elders sit and where judgment is given, so what
    is drawn is the face a man walks up to, not the plan of the works."""
    P = []
    P.append(("fill", [(-46, 0), (46, 0), (46, 88), (-46, 88)], "stone"))
    _crenels(P, -46, 46, 88, 11, 9)
    for sx in (-1, 1):                                           # the towers
        P.append(("fill", [(sx * 46, 0), (sx * 84, 0), (sx * 84, 120),
                           (sx * 46, 120)], "stone"))
        _crenels(P, min(sx * 46, sx * 84), max(sx * 46, sx * 84), 120, 12, 10)
        for gy in (30, 62, 94):                                  # the courses
            P.append(("line", [(sx * 47, gy), (sx * 83, gy)], "rule"))
        P.append(("fill", [(sx * 60, 74), (sx * 70, 74), (sx * 70, 96),
                           (sx * 60, 96)], "void"))              # a window
    for gy in (22, 48, 74):
        P.append(("line", [(-45, gy), (45, gy)], "rule"))
    P.append(("fill", smooth(
        [(-27, 0), (-27, 50), (-20, 68), (0, 76), (20, 68), (27, 50),
         (27, 0)], n=3), "void"))                                # the archway
    P.append(("fill", taper([(-27, 52), (-19, 69), (0, 77)], [5.0, 5.0, 5.0],
                            round_end=False), "stone"))          # the voussoir
    P.append(("fill", taper([(27, 52), (19, 69), (0, 77)], [5.0, 5.0, 5.0],
                            round_end=False), "stone"))
    for sx in (-1, 1):                                           # the leaves
        P.append(("line", [(sx * 13, 0), (sx * 13, 62)], "rule"))
    return P


# Each creature's own drawing units restated in the shared unit — the factor
# is its real size against a man's height, and it is applied once, here, so
# a caller never scales one creature against another by hand.
UNIT = {"man": 1.00,        # the reference: ~97 units tall
        "donkey": 1.16,     # ears up, an ass stands about a man's height;
                            # the withers, which is what a rider sits above,
                            # come to two thirds of it
        "ox": 1.32,         # withers at a man's chest, and twice his weight
        "sheep": 0.87,      # withers at a man's knee
        "lamb": 0.52,
        "lion": 1.10,       # withers just above a sheep's back, and long
        "wolf": 0.86,       # a big dog: shorter than a lion and far lighter
        "dog": 0.72,        # the street dog, smaller again than the wolf
        "sow": 0.80,        # heavy, and low to the ground
        "serpent": 0.93,    # a man's height laid out, a third of it raised
        "bird": 0.78,
        "dove": 0.42,          # a hand's bird — half the generic wingspan       # a wingspan, not a body length
        "fish": 0.30,       # a fish a man could carry
        "woman": 0.94,
        "child": 0.62,      # a child of seven or so, against a grown man
        "nephilim": 1.55,   # half again a man's height, and heavier
        # made things, sized off the text wherever the text gives a size
        "altar_stone": 1.10,   # a heap a man could raise alone, waist high
        "altar_horned": 1.48,  # Exodus 27: five cubits square, three high
        "boat": 3.10,          # a lake boat: four times a man, mast and all
        "cart": 1.55,
        "manger": 0.62,        # a trough at a man's thigh, and an arm long
        "tent": 2.30,
        "gate": 3.05,
        # growing things
        "tree": 2.35,          # a fruit tree: a man reaches its lower boughs
        "vine": 1.12,          # staked, it comes to a man's shoulder
        "herb": 0.55,
        "grass": 0.30,
        # The lights are emblems, not bodies — they have no size against a
        # man, so they are authored at 1 and a scene sets what it wants.
        "sun": 1.00, "moon": 1.00, "star": 1.00,
        # the handled things, sized off what a hand or a neck is
        "lamp": 0.30,          # a lamp fills a palm
        "idol": 1.42,          # image and plinth together, over a man's head
        "ark": 0.62,           # chest at a man's thigh, cherubim to his chest
        "lampstand": 0.95,     # its lights at about a man's shoulder
        "coins": 0.32,         # a stack in the hand, about a lamp's bulk
        "jar": 0.38,           # a waterpot carried on the shoulder
        "sword": 0.78,
        "axe": 0.62,           # helve and head, a two-hand felling axe         # blade and hilt, a little over half a man
        "scroll": 0.62,
        "cup": 0.30,
        "bread": 0.36,
        "yoke": 0.90,          # the beam spans two necks
        "well": 1.05,
        # the worked things
        "millstone": 0.60,     # a hand-mill two women turn between them
        "plough": 1.10,        # beam, stilt and share, near a man's length
        "winepress": 1.45,
        "censer": 0.50,
        "tomb": 1.90,          # the rock face, and the stone at its door
        "cross": 1.60,       # a little over a man and a half
        "scales": 0.55,
        "harp": 0.60,
        "pillar": 1.50,
        "house": 2.60,
        # the second rank
        "table": 1.30,         # top at a man's waist, and long enough that a
                               # company stands behind it rather than at it
        "stone": 0.55,         # a stone a foot finds: shin high, no more
        "shackle": 0.44,       # wrist irons — a hand's span across
        "throne": 1.07,
        "tower": 2.94,         # a watchtower over a vineyard
        "net": 1.47,
        "basket": 0.48,
        "trumpet": 0.44,
        "ladder": 1.81,
        "chariot": 1.18}


def man(pose="stand", mantle=True, staff=False, arms="down"):
    """A robed figure. See _person for what is drawn and why."""
    return _scale(_person(pose=pose, mantle=mantle, arms=arms,
                          prop="staff" if staff else None), UNIT["man"])


def woman(pose="stand", arms="down"):
    """The veil is the difference that reads: it falls past the shoulders
    where a man's headcloth stops at them. No beard, and a narrower
    shoulder."""
    return _scale(_person(pose=pose, head="veil", beard=False, arms=arms,
                          shoulder=0.93, r=6.3), UNIT["woman"])


def child(pose="stand", arms="down"):
    """A child is not a small adult: the head is nearly the same size the
    grown head will be, on a body two thirds the length. Getting that ratio
    wrong is what makes a drawn child read as a dwarf."""
    return _scale(_person(pose=pose, head="cloth", beard=False, mantle=False,
                          arms=arms, r=8.4, hy=87, shoulder=0.9),
                  UNIT["child"])


def king(pose="stand", arms="down"):
    return _scale(_person(pose=pose, head="crown", sash=True, arms=arms,
                          prop="sceptre"), UNIT["man"])


def priest(pose="stand", arms="down"):
    """Mitre and breastplate — the two things Exodus 28 spends its length
    on, and the two that identify him without a caption."""
    return _scale(_person(pose=pose, head="mitre", ephod=True, sash=True,
                          arms=arms), UNIT["man"])


def soldier(pose="stand", arms="down"):
    """Helmet, spear, shield, and a tunic cut at the knee — the short hem is
    what separates a fighting man from every other figure in silhouette."""
    return _scale(_person(pose=pose, head="helmet", sleeve="short", arms=arms,
                          hem=0.62, mantle=False, prop="spear", shield=True),
                  UNIT["man"])


_WINGS_ANGEL = {
    # Outer edge first, from the shoulder up, then the inner edge back down.
    # Authored for the right-hand wing; the left is mirrored.
    "raised": [(8, 63), (16, 84), (26, 106), (36, 124), (41, 138),
               (38, 122), (33, 100), (30, 78), (28, 56), (25, 38),
               (20, 30), (14, 44), (10, 55)],
    "spread": [(8, 63), (20, 72), (34, 82), (48, 90), (60, 95),
               (56, 84), (48, 72), (40, 60), (33, 48), (26, 40),
               (19, 38), (13, 48), (10, 57)],
    "furled": [(8, 63), (14, 74), (20, 84), (25, 90), (27, 82),
               (26, 66), (24, 48), (21, 30), (17, 20), (13, 32),
               (10, 50)],
}


def _angel(pose="stand", arms="down", wings="raised"):
    """A messenger: the human figure, with two wings behind the shoulders.

    Nothing else is added, and that is deliberate. Haloes, harps and white
    nightgowns are late; what the text gives is a man's appearance and the
    fact that people who meet one are told not to be afraid. So this is
    `_person` — same height, same robe, same fold, so an angel standing over
    a sleeping Joseph is at true scale beside him — with the one thing the
    canon does say about the heavenly ones, which is that they have wings.

    The wings go on FIRST, before any of the body, because parts are drawn
    in order and a wing over the shoulder reads as a cloak. Behind it, the
    body occludes the roots and only the spread shows, which is what a pair
    of wings looks like on something standing facing you.

    `wings` is what they are doing: "raised" for the arrival — both swept up
    past the head, the tallest the figure ever is, and the shape that says
    *angel* at forty pixels; "spread" for one hovering or going; "furled"
    for one standing still and talking, where great wings would fight the
    gesture the arms are making.
    """
    span = _WINGS_ANGEL.get(wings, _WINGS_ANGEL["raised"])
    P = []
    for sx in (-1, 1):
        pts = smooth([(sx * px, py) for px, py in span], n=4)
        P.append(("fill", pts if sx == 1 else pts[::-1], "wing"))
        # Three quills laid along the wing's length. They are what keeps a
        # big pale mass from reading as a cape.
        for k in (0.3, 0.52, 0.74):
            i = int(k * 4)
            ox, oy = span[1 + i]
            P.append(("line", [(sx * ox * 0.42, oy * 0.62),
                               (sx * ox * 0.94, oy * 0.94)], "rule"))
    P.extend(_person(pose=pose, head="cloth", beard=False, mantle=False,
                     arms=arms, shoulder=0.97))
    return P


def angel(pose="stand", arms="down", wings="raised"):
    """The angel of the Lord. See `_angel` for what is and is not drawn."""
    return _scale(_angel(pose=pose, arms=arms, wings=wings), UNIT["man"])


def donkey():
    return _scale(_donkey(), UNIT["donkey"])


def ox():
    return _scale(_ox(), UNIT["ox"])


def wolf():
    """The evening wolf of Zephaniah 3:3, and the one Isaiah lies down with
    the lamb. Read the docstring on _wolf before retuning it: the head is
    carried level with the back, and raising it turns the animal into a dog.
    """
    return _scale(_wolf(), UNIT["wolf"])


def dog():
    """The street dog — Proverbs 26:11 and the second half of 2 Peter 2:22,
    the Gentile dogs of Matthew 15, the ones outside in Revelation 22. Head
    up and tail curled: see _dog, and _wolf for what it is NOT."""
    return _scale(_dog(), UNIT["dog"])


def sow():
    """Swine: the herd that went down the cliff, the prodigal's employment,
    the pearls not to be cast, and the sow washed to her wallowing."""
    return _scale(_sow(), UNIT["sow"])


def sheep(lamb=False, lying=False):
    """A ewe, or — with `lamb` — the same animal young: more leg and more
    head for its body, and drawn a good deal smaller. `lying` couches it."""
    return _scale(_sheep(lamb=lamb, lying=lying),
                  UNIT["lamb" if lamb else "sheep"])


def lion():
    return _scale(_lion(), UNIT["lion"])


def serpent(spine=None, raised=True, girth=8.6, pattern=None):
    """`raised` for verse 1; dropped for the sentence of verse 14.

    Hand it a `spine` and it follows that path instead. A supplied spine is
    read as ALREADY being in shared units — a caller who has a path has
    measured it in the scene, not in the serpent's private drawing units — so
    the unit factor is not applied on top of it.
    """
    if spine is not None:
        return _serpent(spine=spine, girth=girth, pattern=pattern)
    return _scale(_serpent(raised=raised, girth=girth, pattern=pattern),
                  UNIT["serpent"])


def bird(pose="glide", view="below"):
    """A bird on the wing.

    `view` is "below" — the spread, for a sky overhead — or "profile", for a
    bird that is going somewhere: the raven and the dove out of the ark, a
    fowl crossing a band of sky. `pose` catches it at a point in the stroke:
    "glide", "up", "down", and for the from-below view also "beat". A flock
    wants a mix of poses; one repeated reads as wallpaper.
    """
    if view == "profile":
        return _scale(_bird_profile(pose=pose), UNIT["bird"])
    return _scale(_bird(pose=pose), UNIT["bird"])


def dove(descending=True):
    """The dove of Luke 3:22 and Genesis 8, in profile. `descending` throws
    the wings up and rotates the breast toward the ground; pass False for one
    at rest. See _dove for why it is not `bird` in another colour."""
    return _scale(_dove(descending=descending), UNIT["dove"])


def fish():
    return _scale(_fish(), UNIT["fish"])


def nephilim():
    return _scale(_nephilim(), UNIT["nephilim"])


def altar(kind="stone", fire=False):
    """`kind` is "stone" for the unhewn heap or "horned" for the made altar
    of Exodus 27. See _altar for why they are two things and not one."""
    return _scale(_altar(kind=kind, fire=fire),
                  UNIT["altar_stone" if kind == "stone" else "altar_horned"])


def boat():
    return _scale(_boat(), UNIT["boat"])


def cart():
    return _scale(_cart(), UNIT["cart"])


def manger(straw=True, light=True):
    """The manger, with what is in it drawn as light. See `_manger`."""
    return _scale(_manger(straw=straw, light=light), UNIT["manger"])


def tent():
    return _scale(_tent(), UNIT["tent"])


def gate():
    return _scale(_gate(), UNIT["gate"])


def vine(fruit=2, stake=True):
    """`fruit` hangs that many bunches — set it to 0 for the vine that yields
    nothing, which is the other half of what the prophets do with one."""
    return _scale(_vine(fruit=fruit, stake=stake), UNIT["vine"])


def tree(fruit=0, bare=False):
    return _scale(_tree(fruit=fruit, bare=bare), UNIT["tree"])


def herb():
    return _scale(_herb(), UNIT["herb"])


def grass():
    return _scale(_grass(), UNIT["grass"])


def sun():
    return _scale(_sun(), UNIT["sun"])


def moon():
    return _scale(_moon(), UNIT["moon"])


def star(points=5, r=15):
    return _scale(_star(points=points, r=r), UNIT["star"])


def unclothed(woman=False, covering=None, arms="down", hair="long"):
    """The man or the woman of Genesis 3. `covering` is None before verse 7,
    "leaves" from verse 7, "skins" from verse 21.

    `hair` picks her fall of hair — see _hair. The default is the long fall,
    chosen because at the size these are used the silhouette is all there is,
    and a fall past the hip is the one shape the man's has not got: she reads
    as a woman at a glance without anything else having to say so. It is
    ignored for the man, who has the beard instead.
    """
    return _scale(_unclothed(beard=not woman, covering=covering,
                             hair=hair if woman else None,
                             shoulder=0.93 if woman else 1.0, arms=arms),
                  UNIT["woman" if woman else "man"])


# ---------------------------------------------------------------------------
# The handled things
# ---------------------------------------------------------------------------
#
# Small made things: what a person carries, pours from, reads, eats, fights
# with, or draws water at. Sized off the hand or the neck rather than off the
# text, since the text almost never gives them a measure.


IDOL_KINDS = ("image", "herm", "stone", "seated")


def _idol(kind="image"):
    """A graven or molten image on its plinth.

    The PLINTH is what makes it an idol. Without it a standing image is a
    person and a standing stone is a rock; set on a stepped base, all of them
    read as something raised up to be looked at, which is the whole of what
    the word means. So every variant here shares one, and the variants differ
    above it.

    The four are the ones a reader of the canon has actually met. `image` is
    the rigid frontal cult figure — columnar, symmetrical, arms fast to its
    sides, which is exactly how it differs from `man()`; nothing about it can
    move, and that is the joke the prophets keep making about them. `herm` is
    the square tapering post with a bearded head that Athens was full of,
    and which Acts 17 is literally standing among. `stone` is the plain
    standing pillar, the massebah set up beside an altar. `seated` is the
    enthroned image of the great temples.

    Drawn in `stone` throughout except the molten `image`, which takes the
    metal — so a scatter of them across a city has some tonal variety without
    the caller having to colour each one.
    """
    P = [("fill", [(-16, 0), (16, 0), (16, 5), (-16, 5)], "stone"),
         ("fill", [(-13, 5), (13, 5), (13, 11), (-13, 11)], "stone"),
         ("line", [(-13, 8), (13, 8)], "rule")]
    if kind == "herm":
        P.append(("fill", [(-7, 11), (7, 11), (9, 50), (-9, 50)], "stone"))
        for sx in (-1, 1):                       # the shoulder pegs
            P.append(("fill", [(sx * 9, 44), (sx * 14, 43), (sx * 14, 48),
                               (sx * 9, 49)], "stone"))
        P.append(("dot", (0, 58, 7.4), "stone"))
        P.append(("fill", smooth([(-5, 55), (-5.4, 49), (0, 46), (5.4, 49),
                                  (5, 55), (0, 56.4)]), "hair"))   # the beard
    elif kind == "stone":
        P.append(("fill", smooth([(-9, 11), (9, 11), (7.4, 44), (5, 58),
                                  (0, 61), (-5, 58), (-7.4, 44)], n=3),
                  "stone"))
        P.append(("line", [(-6.6, 30), (6.6, 30)], "rule"))
    elif kind == "seated":
        P.append(("fill", [(-14, 11), (14, 11), (14, 30), (-14, 30)],
                  "stone"))                                        # the seat
        for sx in (-1, 1):                                         # knees
            P.append(("fill", smooth([(sx * 5, 30), (sx * 13, 31),
                                      (sx * 15, 38), (sx * 6, 39)]), "stone"))
        P.append(("fill", [(-8, 30), (8, 30), (9.6, 52), (-9.6, 52)],
                  "stone"))
        P.append(("dot", (0, 59, 7.0), "stone"))
    else:                                                          # image
        P.append(("fill", [(-8.4, 11), (8.4, 11), (7, 47), (-7, 47)],
                  "metal"))
        for sx in (-1, 1):                       # arms fast to the sides
            P.append(("fill", [(sx * 8.4, 44), (sx * 11.4, 43),
                               (sx * 10, 20), (sx * 7.6, 20)], "metal"))
        P.append(("fill", [(-11, 47), (11, 47), (11, 52), (-11, 52)],
                  "metal"))                      # the shoulders
        P.append(("dot", (0, 58, 6.6), "metal"))
    return P


def _cherub(sx):
    """One cherub of the mercy seat, facing inward (`sx` = -1 stands on the
    left and faces right). The Exodus 25 inset in generate_tabernacle draws
    these with feathered wings and quills, which is right at half a page and
    illegible at the forty pixels an icon gets; this is the same creature
    reduced to what still reads — a small standing body and one long wing
    arched up and over toward its fellow."""
    # `sx` is which side it stands on; the wing goes the OTHER way, inward
    # over the seat, because that is the whole instruction — wings spread out
    # on high, covering the mercy seat, and the two faces toward one another.
    # Splayed outward they are a pair of decorations on a box.
    ix = -sx
    P = []
    P.append(("fill", taper([(0, 0), (ix * 1.5, 11), (ix * 3, 19)],
                            [9, 7.5, 6], round_end=False), "metal"))
    P.append(("fill", taper([(ix * 3, 17), (ix * 16, 29), (ix * 27, 38)],
                            [8.5, 6, 2.6]), "metal"))            # the wing
    for k in (0.34, 0.66):                                       # its quills
        qx, qy = ix * (3 + 24 * k), 17 + 21 * k
        P.append(("line", [(qx - ix * 3, qy + 3), (qx + ix * 3, qy - 3)],
                  "rule"))
    P.append(("dot", (ix * 4, 23.5, 4.2), "metal"))
    return P


def _ark():
    """The ark of the testimony: the chest, the mercy seat on it, the two
    cherubim over that, and the poles left in the rings.

    The POLES are the mark. Every other gold box in the sanctuary is a box;
    only this one is carried, and only this one is commanded never to have its
    poles taken out — so they run clear of the chest on both sides and are the
    first thing the silhouette says. The cherubim settle the rest.
    """
    P = []
    ry = 11.0
    # The poles go down FIRST, so the chest covers their middle and only the
    # carrying ends show. Laid over the chest they read as a bar strapped
    # across it; behind it, they read as what they are — gold-overlaid staves
    # run through rings on its sides, and left there.
    P.append(("fill", [(-74, ry - 3.4), (74, ry - 3.4), (74, ry + 3.4),
                       (-74, ry + 3.4)], "metal"))
    P.append(("fill", [(-46, 4), (46, 4), (46, 34), (-46, 34)], "metal"))
    for fx in (-42, 30):                                    # the four feet
        P.append(("fill", [(fx, 0), (fx + 12, 0), (fx + 12, 5), (fx, 5)],
                  "metal"))
    P.append(("line", [(-46, 30), (46, 30)], "rule"))       # the gold molding
    for rx in (-38, 38):                                    # the rings
        P.append(("dot", (rx, ry, 6.8), "metal"))
        P.append(("dot", (rx, ry, 3.4), "void"))
    P.append(("fill", [(-50, 34), (50, 34), (50, 43), (-50, 43)], "metal"))
    P.append(("line", [(-50, 38), (50, 38)], "rule"))       # the mercy seat
    for sx in (-1, 1):
        for kind, data, mat in _cherub(sx):
            if kind == "dot":
                P.append((kind, (sx * 26 + data[0], 43 + data[1], data[2]),
                          mat))
            else:
                P.append((kind, [(sx * 26 + px, 43 + py) for px, py in data],
                          mat))
    return P


def _lampstand(lit=True):
    """The seven-branched lampstand of Exodus 25:31-40.

    Three pairs of branches out of one shaft, and — the thing that has to be
    got right — all seven lamps finishing at THE SAME HEIGHT. Branches drawn
    rising to their own levels give a candelabrum; brought level they give the
    lampstand, whose seven lights are lit as one row across the holy place.
    """
    P = [("fill", smooth([(-21, 0), (21, 0), (14, 7), (7, 10), (-7, 10),
                          (-14, 7)], n=3), "metal")]              # the base
    P.append(("fill", taper([(0, 8), (0, 34), (0, 60)], [9, 7, 6.4],
                            round_end=False), "metal"))
    for sx in (-1, 1):
        for root, tip in ((22, 36), (32, 24), (42, 12)):
            P.append(("fill", taper(
                [(sx * 3, root), (sx * (tip * 0.55), root + 9),
                 (sx * tip, root + 20), (sx * tip, 60)],
                [6.2, 5.0, 4.4, 4.0], round_end=False), "metal"))
    for k in (18, 28, 38, 48):                        # knops along the shaft
        P.append(("dot", (0, k, 5.0), "metal"))
    for bx in (-42, -32, -22, 0, 22, 32, 42):         # the seven lamps
        P.append(("fill", smooth([(bx - 6.5, 60), (bx + 6.5, 60),
                                  (bx + 5, 67), (bx - 5, 67)], n=2), "metal"))
        if lit:
            P.append(("fill", smooth([(bx - 3.4, 67), (bx, 76),
                                      (bx + 3.4, 67)], n=3), "fire"))
    return P


def _axe():
    """Helve and head, laid with the edge down and the haft running up-right.

    The head is the whole of it: a broad bit flaring to the cutting edge with
    a squared poll behind the eye, which is what separates an axe from a
    hammer at any size. Drawn laid rather than swung — Luke 3:9 has it lying
    at the root, not in the air, and the borrowed one of 2 Kings 6 is lost
    out of a hand that was already swinging.
    """
    P = [("fill", taper([(6, 3), (38, 26), (66, 48)], [7.4, 6.6, 5.6],
                        round_end=False), "wood")]
    P.append(("fill", [(0, 0), (12, 0), (17, 7), (16, 20), (8, 24), (0, 17),
                       (-3, 8)], "metal"))                    # the bit
    P.append(("fill", [(12, 4), (22, 10), (20, 18), (11, 15)], "metal"))
    P.append(("line", [(1.4, 3), (1.4, 15)], "rule"))         # the edge
    return P


def _disc(cx, cy, rx, ry, n=22):
    """An ellipse as a polygon — the part list has circles but no ovals, and
    a disc seen at a slant is an oval."""
    return [(cx + math.cos(math.pi * 2 * i / n) * rx,
             cy + math.sin(math.pi * 2 * i / n) * ry) for i in range(n)]


# The stack is not machine-stacked. Real coins sit slightly off one another,
# and the offsets come from a table rather than a random call so a chapter
# redrawn tomorrow has the same stack in it as today — the same reasoning as
# the masonry's _ROUGH.
_TILT = (0.0, -1.5, 0.9, -0.7, 1.7, -1.2, 0.5, -0.3)


def _coins(n=5, face=True):
    """A stack of coins, and one stood on edge beside it.

    The face-on coin is what makes the pile legible. A stack of flat discs
    seen edge-on is equally a stack of plates, of wheels or of loaves, and
    nothing in the silhouette settles it; one coin turned to the reader, with
    its struck ring showing, names the whole heap — the same trick as the
    fish's eye settling which end is the head.

    It carries no colour of its own. Everything here is the `metal` material,
    so the caller's ink decides whether this is the silver Maktesh was loaded
    with, the gold of a treasury, or the thirty pieces.
    """
    P = []
    for i in range(max(1, n)):
        P.append(("fill", _disc(_TILT[i % len(_TILT)], 2.6 + i * 4.0,
                                11.0, 2.9), "metal"))
    if face:
        P.append(("dot", (21.5, 9.5, 9.6), "metal"))
        P.append(("dot", (21.5, 9.5, 6.2), "rule"))
    return P


def _lamp():
    """The clay lamp of the parable and the psalm: a closed oval body, a
    pinched spout, a wick alight in it. The light is the whole point of the
    thing, so the flame is drawn at full height and not as a token."""
    P = [("fill", smooth([(-15, 3), (-13, 10), (-4, 13), (7, 12), (16, 8),
                          (20, 4), (16, 0), (4, -1), (-8, -0.6)]), "clay"),
         ("fill", smooth([(16, 8), (25, 7.4), (26.4, 4), (20, 2)]), "clay"),
         ("line", smooth([(-11, 8.6), (-2, 10.4), (6, 9.6)], closed=False),
          "rule"),
         ("dot", (-4, 9.2, 3.2), "void")]              # the filling hole
    _fire(P, 23.4, 8, 5.6, 14)                         # the wick alight
    return P


def _jar(handles=True):
    """A waterpot: the vessel at the well, the pitcher on the shoulder, the
    cruse of oil. The profile is what names it, so it is a silhouette and
    almost nothing else."""
    P = [("fill", smooth(
        [(-8, 62), (-13, 58), (-14, 52), (-9, 46), (-15, 36), (-17, 24),
         (-13, 10), (-6, 2), (0, 0.6), (6, 2), (13, 10), (17, 24), (15, 36),
         (9, 46), (14, 52), (13, 58), (8, 62), (0, 63)], n=5), "clay")]
    if handles:
        for sx in (-1, 1):
            P.append(("fill", taper([(sx * 11, 55), (sx * 20, 48),
                                     (sx * 17, 38)], [5, 4.4, 5]), "clay"))
            P.append(("fill", taper([(sx * 11.5, 53.4), (sx * 16.6, 47.6),
                                     (sx * 14, 40.6)], [1.8, 1.6, 1.8]),
                      "void"))
    P.append(("line", smooth([(-14.6, 50), (0, 47.6), (14.6, 50)],
                             closed=False), "rule"))
    P.append(("line", smooth([(-16.4, 28), (0, 26), (16.4, 28)],
                             closed=False), "rule"))
    return P


def _sword():
    """Point down, as it hangs. Blade, guard, grip and pommel are drawn as
    four parts, because a sword drawn as one tapered shape is a spike."""
    P = [("fill", [(-4.2, 46), (4.2, 46), (4.6, 16), (0, 2), (-4.6, 16)],
          "metal"),
         ("fill", [(-13, 46), (13, 46), (12, 51), (-12, 51)], "metal"),
         ("fill", taper([(0, 51), (0, 66)], [6.4, 5.6], round_end=False),
          "wood"),
         ("dot", (0, 68.4, 4.4), "metal"),
         ("line", [(0, 43), (0, 7)], "rule")]              # the fuller
    for gy in (55, 59, 63):
        P.append(("line", [(-2.8, gy), (2.8, gy)], "rule"))  # the binding
    return P


def _scroll(shut=False):
    """The roll of a book. Open, it is two rollers with the sheet between —
    the only form that reads as something written rather than as a tube."""
    if shut:
        return [("fill", [(-7, 2), (7, 2), (7, 32), (-7, 32)], "cloth"),
                ("dot", (0, 33.4, 7.0), "cloth"),
                ("dot", (0, 0.6, 7.0), "cloth"),
                ("line", [(-9, 17), (9, 17)], "rule")]
    P = [("fill", [(-19, 4), (19, 4), (19, 34), (-19, 34)], "cloth")]
    for i, gy in enumerate((10, 16, 22, 28)):               # the writing
        P.append(("line", [(-14, gy), (13 if i % 2 else 8, gy)], "rule"))
    for sx in (-1, 1):
        P.append(("fill", taper([(sx * 19, 2), (sx * 19, 36)], [11, 11],
                                round_end=False), "wood"))
        P.append(("dot", (sx * 19, 37.0, 5.6), "wood"))
        P.append(("dot", (sx * 19, 1.0, 5.6), "wood"))
    return P


def _cup():
    """A footed cup — the cup of blessing, and the cup that passes."""
    return [("fill", smooth([(-10, 30), (-9, 18), (-5, 11), (5, 11),
                             (9, 18), (10, 30), (0, 32)], n=3), "metal"),
            ("fill", taper([(0, 11.4), (0, 3)], [5, 8], round_end=False),
             "metal"),
            ("fill", [(-11, 0), (11, 0), (10, 3.4), (-10, 3.4)], "metal"),
            ("line", smooth([(-9.4, 26), (0, 24.4), (9.4, 26)],
                            closed=False), "rule")]


def _bread():
    """A round loaf, broken. Whole it reads as a stone; parted, it is bread,
    and parted is how it is nearly always spoken of."""
    P = [("fill", smooth([(-20, 2), (-22, 9), (-16, 15), (-4, 17.4),
                          (-1, 12), (-2, 3)], n=4), "clay"),
         ("fill", smooth([(2, 3), (1, 12), (4, 17.4), (16, 15), (22, 9),
                          (20, 2)], n=4), "clay")]
    for a, b in (((-15, 12.4), (-9, 13.6)), ((10, 13), (16, 10.4))):
        P.append(("line", [a, b], "rule"))
    return P


def _yoke():
    """A beam and two bows. What the figure means is that two go under one
    beam, so both bows are drawn even where the verse speaks of one neck."""
    P = [("fill", [(-40, 22), (40, 22), (40, 30), (-40, 30)], "wood")]
    for sx in (-1, 1):
        P.append(("fill", taper([(sx * 10, 24), (sx * 12, 10), (sx * 20, 3),
                                 (sx * 29, 10), (sx * 31, 24)],
                                [5, 4.6, 4.6, 4.6, 5], round_end=False),
                  "wood"))
        P.append(("line", [(sx * 20, 30), (sx * 20, 34)], "rule"))
    P.append(("fill", [(-3.4, 30), (3.4, 30), (3.4, 36), (-3.4, 36)], "wood"))
    return P


def _well():
    """The mouth of a well: the stone ring, the frame over it, the bucket on
    its rope. Meeting-places, all of them — Rebekah, Jacob, the woman of
    Samaria — so what is drawn is the thing a person stands at."""
    P = [("fill", [(-30, 0), (30, 0), (26, 26), (-26, 26)], "stone")]
    for gy in (8.6, 17.4):
        P.append(("line", [(-28.4, gy), (28.4, gy)], "rule"))
    for gx in (-13, 0, 13):
        P.append(("line", [(gx, 0), (gx, 26)], "rule"))
    P.append(("fill", smooth([(-27, 26), (0, 21.4), (27, 26), (27, 31),
                              (0, 26.6), (-27, 31)], n=3), "stone"))
    for sx in (-1, 1):
        P.append(("fill", taper([(sx * 24, 30), (sx * 20, 56)], [5, 4.4],
                                round_end=False), "wood"))
    P.append(("fill", [(-24, 56), (24, 56), (24, 61), (-24, 61)], "wood"))
    P.append(("line", [(0, 56), (0, 41)], "rule"))              # the rope
    P.append(("fill", [(-6, 41), (6, 41), (5, 30), (-5, 30)], "wood"))
    return P


def idol(kind="image"):
    """A graven image on its plinth. `kind` is one of IDOL_KINDS — see _idol
    for what each one is and why the plinth is the mark."""
    return _scale(_idol(kind=kind), UNIT["idol"])


def ark():
    """The ark of the testimony, with the mercy seat, the cherubim and the
    poles that were never taken out. See _ark: the poles are the mark."""
    return _scale(_ark(), UNIT["ark"])


def lampstand(lit=True):
    """The seven-branched lampstand. `lit` puts the flames on it."""
    return _scale(_lampstand(lit=lit), UNIT["lampstand"])


def axe():
    """The axe laid at the root (Luke 3:9), the one that floated (2 Kings 6),
    and the tool Deuteronomy 19 sends a man into the wood with."""
    return _scale(_axe(), UNIT["axe"])


def coins(n=5, face=True):
    """`n` in the stack; `face` stands one on edge beside it, which is what
    tells a pile of coins from a pile of anything else. Pass the metal as the
    ink — silver, gold, brass — the geometry has no colour of its own."""
    return _scale(_coins(n=n, face=face), UNIT["coins"])


def lamp():
    return _scale(_lamp(), UNIT["lamp"])


def jar(handles=True):
    return _scale(_jar(handles=handles), UNIT["jar"])


def sword():
    return _scale(_sword(), UNIT["sword"])


def scroll(shut=False):
    return _scale(_scroll(shut=shut), UNIT["scroll"])


def cup():
    return _scale(_cup(), UNIT["cup"])


def bread():
    return _scale(_bread(), UNIT["bread"])


def yoke():
    return _scale(_yoke(), UNIT["yoke"])


def well():
    return _scale(_well(), UNIT["well"])

# ---------------------------------------------------------------------------
# The worked things
# ---------------------------------------------------------------------------
#
# Tools, presses, instruments and structures. Nearly all are boards and
# masonry, so they are authored as raw point lists — run through the curve
# fitter a beam becomes a bolster and a cut stone becomes a cushion.


def _millstone():
    """The hand-mill: the nether stone, the upper turning on it, the eye the
    corn is fed through and the peg it is turned by. The pair is the point —
    a single disc is a wheel."""
    P = [("fill", [(-30, 0), (30, 0), (28, 9), (-28, 9)], "stone"),
         ("fill", [(-26, 9), (26, 9), (24, 22), (-24, 22)], "stone"),
         ("fill", [(-8, 22), (8, 22), (7, 26), (-7, 26)], "void")]
    P.append(("fill", taper([(17, 22), (19, 40)], [4.6, 4.0],
                            round_end=False), "wood"))
    P.append(("line", [(-27, 9.6), (27, 9.6)], "rule"))
    for gx in (-16, 0, 16):
        P.append(("line", [(gx, 11.4), (gx, 20)], "rule"))
    return P


def _plough():
    """The ard, facing right: the beam running forward to the yoke, the stilt
    a man holds, the share in the ground. Three members meeting is what a
    plough is — drawn as a blade alone it is a spade."""
    P = [("fill", taper([(-30, 6), (10, 26), (54, 38)], [6, 5.4, 4.6],
                        round_end=False), "wood"),
         ("fill", taper([(-30, 6), (-36, 26), (-34, 44)], [6, 5, 4.4],
                        round_end=False), "wood"),
         ("fill", [(-38, 0), (-6, 0), (-14, 10), (-34, 10)], "metal"),
         ("fill", taper([(-29, 9), (-22, 24)], [4.4, 3.6],
                        round_end=False), "wood")]
    P.append(("fill", [(50, 32), (58, 32), (58, 44), (50, 44)], "wood"))
    return P


def _winepress():
    """Cut in the rock: the tread above, the vat below, the channel between.
    What the figure always turns on is that what is trodden runs down into
    something, so both basins are drawn, and the run between them."""
    P = [("fill", [(-46, 14), (10, 14), (10, 48), (-46, 48)], "stone"),
         ("fill", [(-40, 32), (4, 32), (4, 48), (-40, 48)], "void"),
         ("fill", [(10, 0), (52, 0), (52, 30), (10, 30)], "stone"),
         ("fill", [(16, 8), (46, 8), (46, 26), (16, 26)], "void"),
         ("fill", [(16, 8), (46, 8), (46, 17), (16, 17)], "fruit"),
         ("fill", [(4, 30), (16, 30), (14, 36), (6, 36)], "stone")]
    P.append(("fill", taper([(8, 33), (11, 20)], [3.4, 3.0],
                            round_end=False), "fruit"))
    for gy in (20, 30, 40):
        P.append(("line", [(-45, gy), (9, gy)], "rule"))
    return P


def _censer():
    """A firepan with a long handle, coals alight in it — the thing carried
    in, and the thing Korah's company were struck for carrying."""
    P = [("fill", smooth([(-16, 10), (-13, 20), (13, 20), (16, 10),
                          (10, 6), (-10, 6)], n=2), "metal"),
         ("fill", taper([(16, 14), (44, 22)], [5.0, 4.2], round_end=False),
          "wood"),
         ("dot", (46, 22.6, 3.6), "wood"),
         ("fill", [(-9, 6), (9, 6), (7, 0), (-7, 0)], "metal")]
    _fire(P, 0, 20, 15, 20)
    return P


def _tomb():
    """A tomb hewn in the rock, and the stone rolled to the door. The stone
    stands beside the opening rather than over it, which is the only way one
    drawing says both that there is a door and that it can be shut."""
    P = [("fill", [(-56, 0), (34, 0), (34, 66), (-56, 66)], "stone")]
    for gy in (18, 38, 56):
        P.append(("line", [(-55, gy), (33, gy)], "rule"))
    P.append(("fill", [(-34, 0), (-34, 32), (-26, 44), (-10, 48),
                       (6, 44), (14, 32), (14, 0)], "void"))
    P.append(("fill", [(-40, 0), (36, 0), (36, 6), (-40, 6)], "stone"))
    P.append(("dot", (30, 26, 25), "stone"))
    P.append(("dot", (30, 26, 6), "void"))
    for k in range(6):
        a = math.pi * k / 3
        P.append(("line", [(30 + math.cos(a) * 7.6, 26 + math.sin(a) * 7.6),
                           (30 + math.cos(a) * 23, 26 + math.sin(a) * 23)],
                  "rule"))
    return P


def _cross():
    """Two beams. Drawn plain, because everything the shape carries it
    carries already."""
    return [("fill", [(-7, 0), (7, 0), (7, 100), (-7, 100)], "wood"),
            ("fill", [(-34, 66), (34, 66), (34, 79), (-34, 79)], "wood"),
            ("line", [(0, 6), (0, 62)], "rule"),
            ("line", [(-30, 72.6), (-10, 72.6)], "rule"),
            ("line", [(10, 72.6), (30, 72.6)], "rule")]


_SCALES_HANG = 32.0      # where the cords meet the beam
_SCALES_DROP = 19.0      # how far a pan hangs below its end of the beam
_SCALES_SWING = 0.19     # radians at full tilt — a verdict, not a collapse


def _scales_geom(tilt=0.0):
    """The balance, and where its two pans came to rest.

    `tilt` in [-1, 1] swings the beam: +1 puts the RIGHT pan down, which is
    the whole use of the thing. A level balance can show that two things are
    being compared but not which of them won, and every text that reaches for
    a balance — Belshazzar weighed and found wanting, a false balance an
    abomination, Moses accounting the reproach greater riches — is about the
    verdict rather than the comparison.

    The pans hang rather than turn: a pan swinging with the beam would spill
    what is in it, and the cords are what take up the angle.
    """
    a = max(-1.0, min(1.0, tilt)) * _SCALES_SWING
    ca, sa = math.cos(a), math.sin(a)
    P = [("fill", [(-8, 0), (8, 0), (5, 7), (-5, 7)], "metal"),
         ("fill", taper([(0, 5), (0, 50)], [4.4, 3.6], round_end=False),
          "metal")]
    # The beam, as a quad rotated about the post head. Local y is up, so a
    # positive tilt has to *subtract* on the right — putting that sign the
    # other way round rides the heavy pan up, which is the one thing a
    # balance must never do.
    bx, by = 34 * ca, 34 * sa
    px, py = 2 * sa, 2 * ca               # half-thickness, perpendicular
    P.append(("fill", [(-bx + px, 52 + by + py), (bx + px, 52 - by + py),
                       (bx - px, 52 - by - py), (-bx - px, 52 + by - py)],
              "metal"))
    P.append(("dot", (0, 55.6, 3.2), "metal"))
    pans = []
    for sx in (-1, 1):
        hx, hy = sx * _SCALES_HANG * ca, 52 - sx * _SCALES_HANG * sa
        ty = hy - _SCALES_DROP           # the pan's rim
        P.append(("line", [(hx, hy), (hx - 5, ty)], "rule"))
        P.append(("line", [(hx, hy), (hx + 5, ty)], "rule"))
        P.append(("fill", [(hx + 9, ty), (hx - 9, ty), (hx - 6.5, ty - 9),
                           (hx + 6.5, ty - 9)], "metal"))
        pans.append((hx, ty))
    return P, pans


def _scales(tilt=0.0):
    return _scales_geom(tilt)[0]


def _harp():
    """The kinnor: a soundbox, two arms, a yoke, strung between. The strings
    are the instrument, so they are drawn as strings — evenly spaced and
    filled they read as a grille."""
    P = [("fill", smooth([(-22, 0), (22, 0), (26, 13), (20, 22), (-20, 22),
                          (-26, 13)], n=3), "wood"),
         ("fill", taper([(-19, 20), (-24, 44), (-20, 62)], [7, 6, 5],
                        round_end=False), "wood"),
         ("fill", taper([(19, 20), (24, 44), (20, 62)], [7, 6, 5],
                        round_end=False), "wood"),
         ("fill", [(-24, 59), (24, 59), (23, 66), (-23, 66)], "wood")]
    for k in range(7):
        gx = -16 + k * 5.4
        P.append(("line", [(gx * 0.9, 21), (gx, 59)], "rule"))
    P.append(("dot", (0, 11, 5.0), "void"))
    return P


def _pillar():
    """A pillar with its base and capital. What names it is the capital — a
    shaft on its own is a post — so the pomegranates of 1 Kings 7 are on it.
    """
    P = [("fill", [(-26, 0), (26, 0), (26, 10), (-26, 10)], "stone"),
         ("fill", [(-22, 10), (22, 10), (22, 15), (-22, 15)], "stone"),
         ("fill", [(-17, 15), (17, 15), (17, 128), (-17, 128)], "stone"),
         ("fill", [(-22, 128), (22, 128), (22, 134), (-22, 134)], "stone"),
         ("fill", smooth([(-24, 134), (24, 134), (28, 146), (18, 156),
                          (0, 159), (-18, 156), (-28, 146)], n=3), "stone")]
    for gx in (-11, -4, 4, 11):
        P.append(("line", [(gx, 18), (gx, 125)], "rule"))
    for k in range(5):
        P.append(("dot", (-18 + k * 9, 148, 3.4), "fruit"))
    return P


def _house():
    """A flat-roofed dwelling with the outside stair to the roof — where
    Rahab hid the spies, where Peter went up to pray, and through which the
    palsied man was let down. Without the stair it is a box with a door."""
    P = [("fill", [(-46, 0), (46, 0), (46, 62), (-46, 62)], "stone"),
         ("fill", [(-50, 62), (50, 62), (50, 68), (-50, 68)], "stone")]
    for gx in range(-42, 46, 12):
        P.append(("fill", [(gx, 68), (gx + 7, 68), (gx + 7, 76), (gx, 76)],
                  "stone"))
    for gy in (16, 34, 50):
        P.append(("line", [(-45, gy), (45, gy)], "rule"))
    P.append(("fill", [(-28, 0), (-8, 0), (-8, 34), (-28, 34)], "void"))
    P.append(("fill", [(12, 38), (30, 38), (30, 52), (12, 52)], "void"))
    for k in range(8):
        P.append(("fill", [(46, k * 8), (60 - k * 1.5, k * 8),
                           (60 - k * 1.5, 6 + k * 8), (46, 6 + k * 8)],
                  "stone"))
    return P


def millstone():
    return _scale(_millstone(), UNIT["millstone"])


def plough():
    return _scale(_plough(), UNIT["plough"])


def winepress():
    return _scale(_winepress(), UNIT["winepress"])


def censer():
    return _scale(_censer(), UNIT["censer"])


def tomb():
    return _scale(_tomb(), UNIT["tomb"])


def cross():
    return _scale(_cross(), UNIT["cross"])


def scales(tilt=0.0):
    """A balance. `tilt` in [-1, 1]; +1 puts the right pan down."""
    return _scale(_scales(tilt), UNIT["scales"])


def scales_pans(tilt=0.0):
    """Where the two pans' rims sit, in the same units `scales(tilt)` is
    drawn in — so a caller can stand something in each pan with `place()`
    rather than guessing where the pans ended up."""
    u = UNIT["scales"]
    return [(px * u, py * u) for px, py in _scales_geom(tilt)[1]]


def harp():
    return _scale(_harp(), UNIT["harp"])


def pillar():
    return _scale(_pillar(), UNIT["pillar"])


def house():
    return _scale(_house(), UNIT["house"])

def _throne():
    """A seat of judgment: the dais, the seat, the high back, and a lion at
    either arm. Solomon's had six steps and twelve lions, and every throne in
    scripture is a raised seat — the steps are what make it a throne and not
    a chair, so they are drawn even where a verse does not count them."""
    P = []
    for k, (hw, y0, y1) in enumerate(((52, 0, 9), (45, 9, 18), (38, 18, 27))):
        P.append(("fill", [(-hw, y0), (hw, y0), (hw, y1), (-hw, y1)],
                  "stone"))
    P.append(("fill", [(-30, 27), (30, 27), (30, 40), (-30, 40)], "wood"))
    P.append(("fill", [(-30, 40), (-20, 40), (-20, 96), (-30, 96)], "wood"))
    P.append(("fill", [(20, 40), (30, 40), (30, 96), (20, 96)], "wood"))
    P.append(("fill", [(-30, 84), (30, 84), (30, 96), (-30, 96)], "wood"))
    P.append(("fill", smooth([(-30, 96), (0, 108), (30, 96)], n=3), "wood"))
    for sx in (-1, 1):                       # a lion couching at either arm
        P.append(("fill", smooth([(sx * 22, 40), (sx * 34, 42), (sx * 40, 50),
                                  (sx * 36, 58), (sx * 24, 56),
                                  (sx * 18, 48)], n=3), "hide"))
        P.append(("dot", (sx * 34, 52, 1.4), "eye"))
    for gy in (48, 60, 72):
        P.append(("line", [(-19, gy), (19, gy)], "rule"))
    return P


def _tower():
    """A tower: tall, battered inward, battlemented, with the door well up
    the wall. The batter is what tells it from a chimney, and the high door
    from a house."""
    P = [("fill", [(-30, 0), (30, 0), (22, 150), (-22, 150)], "stone"),
         ("fill", [(-26, 150), (26, 150), (26, 158), (-26, 158)], "stone")]
    _crenels(P, -26, 26, 158, 9, 9)
    for gy in (22, 48, 74, 100, 126):
        hw = 30 - (30 - 22) * gy / 150.0
        P.append(("line", [(-hw + 1, gy), (hw - 1, gy)], "rule"))
    P.append(("fill", [(-9, 34), (9, 34), (9, 58), (-9, 58)], "void"))
    P.append(("fill", [(-6, 96), (6, 96), (6, 112), (-6, 112)], "void"))
    return P


def _net():
    """A net, hanging: the head rope with its floats, the mesh, the weights
    along the foot. The mesh is the thing — a net drawn as an outline is a
    sack — and it is cut from the outline by the same helper that shades a
    pit, so it costs nothing to make it follow whatever shape the net takes.
    """
    outline = smooth([(-52, 46), (-44, 20), (-26, 4), (0, 0), (26, 4),
                      (44, 20), (52, 46)], n=4)
    P = [("fill", outline, "void")]
    for deg in (46, -46):
        for a, b in hatch_poly(outline, deg, 8.0, inset=0.6):
            P.append(("line", [a, b], "rule"))
    P.append(("fill", taper([(-53, 46), (0, 47), (53, 46)], [4.4, 4.0, 4.4],
                            round_end=False), "wood"))       # the head rope
    for k in range(7):                                       # the floats
        P.append(("dot", (-45 + k * 15, 50.6, 3.6), "wood"))
    for gx, gy in ((-42, 20), (-24, 5), (0, 1), (24, 5), (42, 20)):
        P.append(("fill", [(gx - 2.6, gy), (gx + 2.6, gy),
                           (gx + 2.0, gy - 6), (gx - 2.0, gy - 6)], "metal"))
    return P


def _basket():
    """Woven: the stakes standing and the weave running round them. A smooth
    tapered pot is a pot; the weave is the whole difference."""
    P = [("fill", [(-22, 0), (22, 0), (28, 44), (-28, 44)], "clay"),
         ("fill", [(-30, 44), (30, 44), (30, 51), (-30, 51)], "clay")]
    for k in range(7):                                       # the stakes
        gx = -18 + k * 6
        P.append(("line", [(gx * 0.79, 2), (gx, 43)], "rule"))
    for gy in (10, 20, 30, 39):                              # the weave
        hw = 22 + (28 - 22) * gy / 44.0
        P.append(("line", [(-hw + 1, gy), (hw - 1, gy)], "rule"))
    return P


def _trumpet(horn=True):
    """`horn` is the shofar — a ram's horn, curved, and the curve is the
    whole of what names it. Otherwise the straight silver trumpet of Numbers
    10, which is a different instrument doing a different job."""
    if horn:
        P = [("fill", taper([(-26, 4), (-8, 0), (12, 4), (26, 16)],
                            [7, 10, 15, 24]), "horn"),
             ("line", smooth([(-18, 6), (0, 4), (16, 10)], closed=False),
              "rule"),
             ("line", smooth([(-12, 8), (4, 7), (18, 14)], closed=False),
              "rule")]
        return P
    P = [("fill", taper([(-30, 6), (14, 6)], [5.6, 8.0], round_end=False),
          "metal"),
         ("fill", smooth([(14, 0), (30, -6), (32, 6), (30, 18), (14, 12)],
                         n=3), "metal"),
         ("dot", (-31, 6, 4.4), "metal")]
    return P


def _ladder():
    """Two rails and its rungs, leaning as a ladder leans. Set upright it is
    a frame; the lean is what says it is set against something."""
    P = []
    for sx in (-1, 1):
        P.append(("fill", taper([(sx * 13 - 5, 0), (sx * 13 + 13, 120)],
                                [6.4, 5.6], round_end=False), "wood"))
    for k in range(9):
        t = (k + 0.5) / 9.0
        y = 6 + t * 108
        x0 = -18 + t * 18
        P.append(("fill", [(x0 - 8, y), (x0 + 34, y),
                           (x0 + 34, y + 5), (x0 - 8, y + 5)], "wood"))
    return P


def _chariot():
    """A war chariot, facing right: a light car on two tall wheels, open
    behind, the rail a man holds, the pole running forward to the yoke.
    Everything about it is lighter than the cart — that is the difference
    between a thing that carries a load and a thing that carries a man into
    a battle."""
    P = []
    _wheel(P, -6, 30, 30, "far", spokes=8)
    P.append(("fill", taper([(24, 34), (72, 26), (104, 22)],
                            [6.4, 5.0, 4.4], round_end=False), "wood"))
    P.append(("fill", [(98, 14), (108, 14), (108, 30), (98, 30)], "wood"))
    P.append(("fill", [(-26, 30), (26, 30), (26, 38), (-26, 38)], "wood"))
    P.append(("fill", smooth([(-26, 38), (26, 38), (30, 52), (28, 64),
                              (8, 66), (-24, 62), (-26, 50)], n=3), "wood"))
    P.append(("fill", smooth([(-20, 44), (22, 44), (24, 58), (6, 60),
                              (-19, 56)], n=3), "void"))
    P.append(("fill", taper([(26, 40), (30, 56), (26, 68)], [5.0, 4.4, 4.0],
                            round_end=False), "wood"))       # the front rail
    _wheel(P, 4, 32, 32, "wood", spokes=8)
    return P


def _table(span=1.0):
    """The top, two trestles and the stretcher between them.

    Drawn end-on like everything else here, so a company can stand behind it
    and the top reads as one line rather than as an ellipse in a perspective
    the rest of the page is not in. Every table that matters in scripture is
    a table people are received at — David's, the Lord's, the showbread — so
    what is drawn is the thing they sit down to, plain and heavy enough to
    stand a company behind.

    `span` lengthens the board WITHOUT thickening the timber, which is how a
    real table gets longer and is the only way a long one still reads as a
    table: scale the whole drawing instead and the top becomes a beam and the
    legs become piers. The height never changes, so a table at any span is
    still waist high on the man standing behind it.
    """
    hw = 48 * span
    ox = hw - 6                                          # the trestle centres
    P = [("fill", [(-hw, 30), (hw, 30), (hw, 35), (-hw, 35)], "wood")]
    P.append(("line", [(-hw + 3, 30.4), (hw - 3, 30.4)], "rule"))
    for sx in (-1, 1):                                   # trestle and foot
        P.append(("fill", [(sx * ox + 4.5, 4), (sx * ox - 4.5, 4),
                           (sx * ox - 2.5, 30), (sx * ox + 6.5, 30)], "wood"))
        P.append(("fill", [(sx * ox + 9.5, 0), (sx * ox - 9.5, 0),
                           (sx * ox - 9.5, 4.6), (sx * ox + 9.5, 4.6)],
                  "wood"))
    P.append(("fill", [(-ox, 12), (ox, 12), (ox, 16.4), (-ox, 16.4)], "wood"))
    return P


def _rock():
    """One unhewn stone, the kind a foot finds.

    The stumbling stone, the stone the builders rejected, the stone at the
    door: one shape serves them all, and it is built from the same
    irregularity table the masonry uses, so a stone standing alone and a wall
    of them are made of the same rock. Smoothed, unlike the made things — a
    boulder really is round, and the curve fitter is what stops it reading as
    a crystal.
    """
    P = [("fill", _stone(0, 15, 46, 30, 2), "stone")]
    P.append(("line", [(-15, 11), (0, 17), (16, 12)], "rule"))
    P.append(("line", [(-7, 22.6), (7, 24)], "rule"))
    return P


def _shackle(broken=False):
    """Iron on the wrists, and — `broken` — the link that no longer holds.

    Two rings and the chain between them. Whole, the chain hangs in a slack
    curve; broken, the two halves fly back from a gap and the rings fall
    open. The gap is the entire content of the image, so everything else is
    kept quiet enough that the eye goes to it.
    """
    P = []
    for sx in (-1, 1):
        P.append(("dot", (sx * 26, 20, 12), "metal"))
        P.append(("dot", (sx * 26, 20, 7.6), "void"))
    if broken:
        # Each half hangs from its own cuff and stops. Nothing is drawn in
        # the middle, and the empty middle is the whole of what the picture
        # says — an energetic burst of fragments would only give the eye
        # something to read instead of the gap.
        links = [(-17.4, 11.6), (-12.6, 3.4), (17.4, 11.6), (12.6, 3.4)]
    else:
        links = [(-9.4, 12.6), (0, 9.4), (9.4, 12.6)]     # the chain, slack
    for cx, cy in links:
        P.append(("dot", (cx, cy, 4.8), "metal"))
        P.append(("dot", (cx, cy, 2.5), "void"))
    return P


def table(span=1.0):
    """`span` lengthens the board only — a company's table is the same table
    as a small one, with more of it."""
    return _scale(_table(span=span), UNIT["table"])


def stone():
    return _scale(_rock(), UNIT["stone"])


def shackle(broken=False):
    """`broken` for the fetter that has been struck off — which is how the
    canon nearly always has occasion to mention one."""
    return _scale(_shackle(broken=broken), UNIT["shackle"])


def throne():
    return _scale(_throne(), UNIT["throne"])


def tower():
    return _scale(_tower(), UNIT["tower"])


def net():
    return _scale(_net(), UNIT["net"])


def basket():
    return _scale(_basket(), UNIT["basket"])


def trumpet(horn=True):
    """`horn` for the shofar, otherwise the straight silver trumpet."""
    return _scale(_trumpet(horn=horn), UNIT["trumpet"])


def ladder():
    return _scale(_ladder(), UNIT["ladder"])


def chariot():
    return _scale(_chariot(), UNIT["chariot"])
