"""Leviticus 1-7 workbench: the drawings the sections share.

One drawing of each thing the bench shows in more than one section, and the
colours, plan points and small drawing helpers behind them. Everything here
returns svg (or points); nothing is an element (leviticus17_parts and the
sections make those).

Colours: BLOOD, WATER, FIRE_OUT, FIRE_IN, ASH, OIL, FLOUR, CLAY (the
earthen vessel, the oven), LOAF (leavened bread's crust), MEAT.

The plan (the reference page's sanctuary.Plan, world px): PLAN, ALT (the
altar's box), TENT_R, NORTH_R, ASH_PT, GATE_X, DOOR_PT, VEIL_PT.

The bench sets more than one section shows (one drawing of each):
    supply_svg(kind, x, g, k)  the meal offering's supplies standing on g: "basket"
                               (fine flour heaped in it), "jar" (oil), "cup"
                               (frankincense heaped in it; salt), "honey" (a jar);
                               supply_top(kind, g, k) the top of what is in it,
                               supply_outline(kind, x, g, k) for a link pulse
    cookware_svg(kind, x, g, k, state=None)   svg_figures.cookware in its ink: the
                               oven and the earthen pot clay, the griddle, the pan
                               and the bronze pot bronze
    bread_svg(kind, x, gy, k)  offerings.BREADS: "loaf" (one unleavened cake),
                               "cakes" (two), "wafers" (three thin rounds),
                               "oil_cakes", "leavened" (risen)

Drawings:
    inset_svg(name, k, at)     generate_tabernacle.INSETS[name] (altar, veil,
                               incense...) whole, without its panel, scale k,
                               its corner (IX, IY) at `at`; inset_pt(p, k, at)
    A_HORNS                    the bronze altar inset's horns (inset px)
    heap(cx, gy, w, h, col)    a heap (ashes, flour, salt); heap_pts
    flames(xs, gy, hs)         tongues of fire standing on gy
    hand_svg(pose, at, ang, s, flip=1, arm=34)   svg_figures.hand at the wrist
    hand_pt(parts)             a pose's hand (its foremost point); C_POSE the
                               offerer's pose at each beast's head
    wave(x0, x1, y)            a wavy line (oil, water)
    meat_svg, fat_svg, drop_svg   a piece of meat on a plate, a lump of fat, a
                               drop of blood
"""

import svg_figures as F
import sanctuary as SN
import generate_tabernacle as GT
from generate_tabernacle import BRONZE, GOLD, PANEL, RED, TEXT, WHITE_LINEN, SILVER
from svg_surface import SvgCanvas, SvgLayer, _fmt
from svg_vocab import flame, mix

BLOOD = (178, 42, 38)                  # blood, a step past the house red
WATER = (120, 160, 214)
FIRE_OUT = (236, 150, 64)
FIRE_IN = (255, 214, 120)
ASH = (128, 124, 118)
OIL = (226, 186, 84)                   # oil, poured: a step off the gold
FLOUR = WHITE_LINEN
CLAY = (186, 120, 80)                  # the earthen vessel, the oven
LOAF = (196, 140, 96)                  # leavened bread's crust
MEAT = mix(PANEL, RED, .72)
SKIN = F.palette(TEXT, PANEL)["skin"][0]


def pts_str(pts):
    return " ".join(f"{_fmt(x)},{_fmt(y)}" for x, y in pts)


def rgb(c):
    return f"rgb({int(c[0])},{int(c[1])},{int(c[2])})"


# ---------------------------------------------------------------------------
# generate_tabernacle's insets, without their panels
# ---------------------------------------------------------------------------

class FilteredLayer(SvgLayer):
    """An SvgLayer that leaves out an inset's panel(): its frame and its
    title and subtitle, and the measurement line under it, which on a
    Leviticus verse would be caption lines. generate_tabernacle's inset
    drawers stay as they are."""

    _DROP_TEXT = {(GT.ICX, GT.IY + 22), (GT.ICX, GT.IY + 44),
                  (GT.ICX, GT.CAPY1), (GT.ICX, GT.CAPY2)}

    def rounded_rectangle(self, box, radius=0, fill=None, outline=None,
                          width=1):
        x0, y0, x1, y1 = box if len(box) == 4 else (*box[0], *box[1])
        if (x0, y0, x1, y1) == (GT.IX, GT.IY, GT.IX + GT.IW, GT.IY + GT.IH):
            return
        super().rounded_rectangle(box, radius, fill, outline, width)

    def text(self, xy, s, font=None, fill=(0, 0, 0), anchor=None):
        if (round(xy[0]), round(xy[1])) in self._DROP_TEXT:
            return
        super().text(xy, s, font, fill, anchor)


def inset_svg(name, k, at):
    """generate_tabernacle.INSETS[name] drawn whole, without its panel, at
    scale k with the inset's top-left corner (IX, IY) at point `at`."""
    d, od = FilteredLayer(), SvgLayer()
    GT.INSETS[name](d, od, None, 1.0, 1.0)
    ox, oy = at[0] - GT.IX * k, at[1] - GT.IY * k
    return (f'<g transform="translate({_fmt(ox)} {_fmt(oy)}) scale({k})">'
            + "".join(d.elements()) + "</g>")


def inset_pt(p, k, at):
    return (at[0] + (p[0] - GT.IX) * k, at[1] + (p[1] - GT.IY) * k)


# the bronze altar inset's horns (generate_tabernacle's inset px)
A_HORNS = [[GT.AX - 6, GT.AY - 22, GT.AX + 16, GT.AY],
           [GT.AX + GT.AW - 16, GT.AY - 22, GT.AX + GT.AW + 6, GT.AY]]


# ---------------------------------------------------------------------------
# small drawings
# ---------------------------------------------------------------------------

def heap_pts(cx, gy, w, h):
    return [(cx - w / 2, gy), (cx - w * .36, gy - h * .45),
            (cx - w * .18, gy - h * .85), (cx, gy - h),
            (cx + w * .2, gy - h * .8), (cx + w * .38, gy - h * .4),
            (cx + w / 2, gy)]


def heap(cx, gy, w, h, col=ASH):
    pts = F.smooth(heap_pts(cx, gy, w, h), n=3)
    return (f'<polygon points="{pts_str(pts)}" fill="{rgb(mix(PANEL, col, .7))}"'
            f' stroke="{rgb(col)}" stroke-width="1.4"/>')


def flames(xs, gy, hs):
    """Tongues of fire standing on gy: an outer and an inner colour."""
    c = SvgCanvas(10, 10)
    for x, h in zip(xs, hs):
        flame(c, x - h * 0.12, gy, h, FIRE_OUT)
    for x, h in zip(xs, hs):
        flame(c, x - h * 0.07, gy, h * 0.6, FIRE_IN)
    return "".join(c._els)


def wave(x0, x1, y, amp=4, step=8):
    n = max(2, int((x1 - x0) / step))
    return [(x0 + (x1 - x0) * k / n, y + (amp if k % 2 else -amp)) for k in range(n + 1)]


def _hand_d(shape, arm):
    pts = [(max(x, -arm), y) for x, y in shape]
    return "M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in pts) + " Z"


HAND_ORDER = ("arm", "palm", "patch", "f3", "f2", "f1", "f0", "th")


def hand_svg(pose, at, ang, s, flip=1, arm=34):
    """svg_figures.hand at `at` (the wrist), its forearm run at `ang`
    degrees, scale s."""
    sh = F.hand(pose)
    out = []
    for name in HAND_ORDER:
        d = _hand_d(sh[name], arm)
        if name == "patch":
            out.append(f'<path d="{d}" fill="{rgb(SKIN)}"/>')
        else:
            out.append(f'<path d="{d}" fill="{rgb(SKIN)}" stroke="{rgb(TEXT)}" '
                       f'stroke-width="{1.3 / s:.3f}" stroke-linejoin="round"></path>')
    return (f'<g transform="translate({_fmt(at[0])} {_fmt(at[1])}) rotate({ang:.1f}) '
            f'scale({_fmt(flip * s)} {_fmt(-s)})">' + "".join(out) + "</g>")


# the offerer's pose at each beast's head, so his hand comes down on it:
# (arms, legs, lean)
C_POSE = {"bull": ("reach", "stand", 0), "goat": ("pointdn", "stand", 0),
          "fgoat": ("pointdn", "stand", 0), "sheep": ("pointdn", "kneel2", 20),
          "ram": ("pointdn", "kneel2", 20), "lamb": ("pointdn", "kneel2", 20)}


def hand_pt(fig):
    """The hand of a pose with the arms forward: its foremost point."""
    return max((q for kind, d, _m in fig if kind in ("fill", "line") for q in d),
               key=lambda q: q[0])


def meat_svg(x, y, w=34, h=16):
    """A piece of meat on a plate, centred on (x, y)."""
    return (f'<ellipse cx="{_fmt(x)}" cy="{_fmt(y + h * .45)}" rx="{_fmt(w * .8)}" '
            f'ry="{_fmt(h * .32)}" fill="{rgb(mix(PANEL, SILVER, .35))}" '
            f'stroke="{rgb(SILVER)}" stroke-width="1.2"/>'
            f'<rect x="{_fmt(x - w / 2)}" y="{_fmt(y - h / 2)}" width="{_fmt(w)}" '
            f'height="{_fmt(h)}" rx="{_fmt(h * .45)}" fill="{rgb(MEAT)}" '
            f'stroke="{rgb(TEXT)}" stroke-width="1.3"/>'
            f'<path d="M{_fmt(x - w * .25)} {_fmt(y - h * .1)} q{_fmt(w * .2)} '
            f'{_fmt(-h * .3)} {_fmt(w * .45)} 0" fill="none" '
            f'stroke="{rgb(mix(MEAT, WHITE_LINEN, .6))}" stroke-width="1.4"/>')


def fat_svg(x, y, w=46, h=26):
    """A lump of fat, centred on (x, y)."""
    pts = F.smooth([(x - w / 2, y + h * .3), (x - w * .4, y - h * .3),
                    (x - w * .1, y - h / 2), (x + w * .25, y - h * .4),
                    (x + w / 2, y), (x + w * .3, y + h / 2), (x - w * .2, y + h * .45)], n=4)
    return (f'<polygon points="{pts_str(pts)}" fill="{rgb(mix(PANEL, WHITE_LINEN, .8))}" '
            f'stroke="{rgb(TEXT)}" stroke-width="1.4"/>')


def drop_svg(x, y, h=40):
    """A drop of blood, centred on (x, y)."""
    w = h * .62
    pts = F.smooth([(x, y - h / 2), (x + w * .28, y - h * .1), (x + w / 2, y + h * .2),
                    (x + w * .3, y + h * .45), (x, y + h / 2), (x - w * .3, y + h * .45),
                    (x - w / 2, y + h * .2), (x - w * .28, y - h * .1)], n=3)
    return (f'<polygon points="{pts_str(pts)}" fill="{rgb(BLOOD)}" '
            f'stroke="{rgb(mix(BLOOD, TEXT, .4))}" stroke-width="1.3"/>')


# ---------------------------------------------------------------------------
# The plan: the reference page's court plan (world px)
# ---------------------------------------------------------------------------

PLAN = SN.Plan(730, 440, 14)                 # the reference page's own


def _pp(x, y):
    return PLAN.pt(x, y)


_ALTAR_BOX = PLAN.box(*SN.plan_box("altar"))  # (left, top, w, h)
ALT = (_ALTAR_BOX[0], _ALTAR_BOX[1], _ALTAR_BOX[0] + _ALTAR_BOX[2],
       _ALTAR_BOX[1] + _ALTAR_BOX[3])        # 1605, 755, 1675, 825
_TENT = PLAN.box(*SN.TENT)
TENT_R = (_TENT[0], _TENT[1], _TENT[0] + _TENT[2], _TENT[1] + _TENT[3])   # 870, 720, 1290, 860
_COURT = PLAN.box(*SN.COURT)
GATE_X = _COURT[0] + _COURT[2]
_NORTH = SN.PLACE["north_side"]
NORTH_R = (_pp(_NORTH.box[0], _NORTH.box[1]) + _pp(_NORTH.box[2], _NORTH.box[3]))
ASH_PT = _pp(*SN.PLACE["ash_place"].pt)      # 1703, 790
DOOR_PT = _pp(SN.DOOR_X, 26.4)               # under the altar of incense's name
VEIL_PT = _pp(SN.VEIL_X, 26.4)


# ---------------------------------------------------------------------------
# The shared bench sets
# ---------------------------------------------------------------------------

def _fig(parts, x, gy, k, ink_):
    import leviticus17_bench as B
    return B.fig(parts, x, gy, k, ink_, PANEL)


_SUPPLY = {"basket": (F.basket, FLOUR), "jar": (F.jar, OIL), "cup": (F.cup, FLOUR),
           "honey": (F.jar, GOLD)}


def _supply_box(kind, k):
    return F.bbox((_SUPPLY[kind][0](), 0))


def supply_top(kind, g, k):
    """The top of the supply standing on g at scale k (its rim)."""
    return g - _supply_box(kind, k)[3] * k


def supply_svg(kind, x, g, k):
    """A supply of the meal offering standing on g at scale k: the basket
    with its fine flour heaped, the jar of oil, the cup with its
    frankincense (or salt) heaped, the jar of honey."""
    fn, ink_ = _SUPPLY[kind]
    out = _fig(fn(), x, g, k, ink_)
    top = supply_top(kind, g, k)
    if kind == "basket":
        out += heap(x, top + 2.3 * k, 24.7 * k, 7.3 * k, FLOUR)
    elif kind == "cup":
        out += heap(x, top + 0.8 * k, 6.4 * k, 2.6 * k, FLOUR)
    return out


def supply_outline(kind, x, g, k):
    return F.outline(_SUPPLY[kind][0](), x, g, k)


def cookware_svg(kind, x, g, k, state=None):
    """svg_figures.cookware standing on g: the oven and the earthen pot in
    clay, the griddle, the pan and the bronze pot ("bronze") in bronze."""
    if kind == "bronze":
        return _fig(F.cookware("pot", state, bronze=True), x, g, k, BRONZE)
    return _fig(F.cookware(kind, state), x, g, k, CLAY if kind in ("oven", "pot") else BRONZE)


def bread_svg(kind, x, gy, k):
    """offerings.BREADS as svg_figures.bread, its foot at (x, gy), scale k:
    a loaf (one unleavened cake), cakes (two loaves), wafers (three thin
    rounds), the cakes mixed with oil in the oil's gold, the leavened loaf
    risen."""
    import leviticus17_bench as B
    linen = WHITE_LINEN
    if kind == "loaf":
        return _fig(F.bread(), x, gy, k, linen)
    if kind == "cakes":
        return _fig(F.bread(), x - 3 * k, gy, k, linen) + _fig(F.bread(), x + 3 * k, gy - 5 * k, k, linen)
    if kind == "wafers":
        one = _fig(F.bread(), 0, 0, k, linen)
        return "".join(f'<g transform="translate({B.f2(x)} {B.f2(gy - i * 2.6 * k)}) '
                       f'scale(1.08 0.42)">{one}</g>' for i in range(3))
    if kind == "oil_cakes":
        return (_fig(F.bread(), x, gy, k, mix(linen, GOLD, .55))
                + "".join(f'<circle cx="{B.f2(x + dx * k)}" cy="{B.f2(gy - dy * k)}" '
                          f'r="{B.f2(0.9 * k)}" fill="{rgb(GOLD)}"/>'
                          for dx, dy in ((-4, 7.8), (1.5, 8.4), (5.5, 7.2))))
    if kind == "leavened":
        one = _fig(F.bread(), 0, 0, k * 1.1, mix(linen, LOAF, .35))
        return f'<g transform="translate({B.f2(x)} {B.f2(gy)}) scale(1 1.75)">{one}</g>'
    raise KeyError(kind)


def bread_outline(kind, x, gy, k):
    """A loaf's outline (kind "loaf") for a link pulse."""
    return F.outline(F.bread(), x, gy, k)
