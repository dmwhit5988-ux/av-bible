"""Stations G (meal) and K (kitchen) of the Leviticus 1-7 pictures.

Each is a 1024 x 576 card on the world sheet (corner in
leviticus17_spec.STATIONS: G at (2960, 2920), under the burnt and meal
columns; K at (4080, 2920), under the peace and sin columns), drawn in its
own card px with the API of leviticus17_stations (its docstring). There is
no title on either card: only WEB names, numbers and labelled drawings,
each brought in on its word, played once and held.

G, the meal offering (2:1-3, 8-10, 14-16; 5:12-13; 6:14-18, 25, 29; 7:7)
-------------------------------------------------------------------------
Shots: "" (whole), "supplies" (the flour, oil and frankincense with the
hand, s 1.4), "fruits" (the first fruits, s 1.4).

- the supplies (top left): G.oil (the jar), G.flour (the basket of fine
  flour), G.frankincense (the cup); G.pour (oil traced from the jar onto
  the flour); G.handful (svg_figures.hand opening and closing to "cup" on
  the flour, chip "handful"; verb "move" lifts it, as the handful taken up
  for the fire); G.memorial_portion (chip "memorial portion", 5:12);
- the priest (centre): G.priest (svg_figures.priest()), G.the_priests
  (chip "the priest's", 5:13), G.remnant (the rest of the flour slid from
  the basket to the priest; light or "move"); a target that needs the
  priest draws him if G.priest is not lit;
- the split bar (under the supplies): G.split (its frame, outline only
  when lit alone), G.memorial (its memorial end, with the dashed frame),
  G.rest ("Aaron and his sons", grown from the memorial end);
- the first fruits (bottom left): G.fruits (three ears, chip "first
  fruits"), G.parched (a flame under them, chip "parched"), G.bruised
  (chip "bruised"), G.fruit_oil (oil traced over them, 2:15),
  G.fruit_frankincense (a cup, chip "frankincense", 2:15), G.part (a token
  split off the ears, chip "part"; light or "move"), G.all_frankincense
  (chip "all its frankincense", 2:16);
- most holy (top right): G.most_holy (chip "most holy", the bracket's
  stub and the name "meal offering" under it, 2:3); G.name_meal (an
  outline on that name); G.bracket (the bracket traced over all three
  names, 6:17); G.name_sin, G.name_trespass (the names, 6:17); G.one_law
  ("=" traced between sin and trespass, chip "one law for them", 7:7);
  G.to_priest (an arrow from it to the priest, 7:7);
- every male (bottom right): G.males (four priest() figures in turn, chip
  "every male"), G.forever (chip "forever"), G.touch (a hand on the
  portion, chip "holy").

K, the kitchen (2:4-7, 11-13; 5:11; 6:20-23, 27-28)
---------------------------------------------------
Shots: "" (whole); the card's four quadrants at s 2, "cook" (top left),
"rules" (top right), "measure" (bottom left), "vessels" (bottom right),
which no word crosses; "griddle" (the griddle close, s 2.4).

- cook (top left): K.oven, K.griddle (with its flat round), K.pan
  (svg_figures.cookware, each drawn in, chip under it); K.cakes
  ("unleavened cakes"), K.wafers ("unleavened wafers"); K.mixed ("mixed
  with oil"); K.cut (cut lines traced across the griddle's round); K.oil
  (oil traced on it); K.soaked ("soaked"); K.baked_pieces ("baked
  pieces");
- rules (top right): K.yeast, K.honey (the chips, each with its drawing);
  K.not:yeast, K.not:honey (the not-mark traced over each, lit, so it
  stays); K.altar (the altar, and a struck arrow from yeast and honey to
  it: "burn no"); K.first_fruits (chip "first fruits", arrows traced to it
  from yeast and honey); K.salt (the cup, chip "salt"); K.covenant (chip
  "covenant"); K.names (the chip "all your offerings", 2:13's words, with
  a line from the salt to it);
- measure (bottom left): K.measure (the ephah in ten parts, chip
  "ephah"); K.tenth (its tenth lit, chip "one tenth"); K.flour (basket,
  "fine flour"), K.jar ("oil"), K.cup ("frankincense"); K.not:oil,
  K.not:frankincense (the marks over the jar and the cup, 5:11);
  K.morning, K.evening (the tenth split in two halves, with the sun and
  the moon, 6:20);
- vessels (bottom right), offerings.VESSELS: K.earthen (the clay pot,
  "earthen vessel"), K.broken (its crack traced, then its halves part
  once, chip "broken"), K.bronze (the bronze pot, "bronze vessel"),
  K.scoured (scour strokes, "scoured"), K.rinsed (water traced, "rinsed");
  K.coat (a garment with the blood on it, chip "garment"), K.wash (water
  traced over it), K.holy_place (chip "holy place"); K.holy (a hand on
  the flesh, chip "holy", 6:27).

Verbs beyond light/pulse/current: "not" on any G or K target traces the
not-mark over it for this verse only (the K.not:* targets are the ones
that persist); "move" on G.handful, G.part and G.remnant.
"""

import math

import offerings as OF
import svg_figures as F
from generate_tabernacle import (BG, BRONZE, GOLD, PANEL, RED, SAND, SAND_DIM,
                                 SILVER, TEXT, TEXT_DIM, WHITE_LINEN, ACACIA)
from leviticus17_stations import (BLOOD, CH, CW, WATER, Station, Target,
                                  appear, bounds, case_of, ellipse_pts, fade_out,
                                  flames, heap, motion, pts_str, rect_pts,
                                  rgb, t_s, trace, union_box)
from svg_map_camera import EASE, fade
from svg_surface import _fmt
from svg_vocab import NOT_RED, mix, not_mark_points, text_w

OIL = (226, 186, 84)                   # oil, poured: a step off the gold
FLOUR = WHITE_LINEN
CLAY = (186, 120, 80)                  # the earthen vessel
SKIN = F.palette(TEXT, PANEL)["skin"][0]


def _later(t, dt):
    return None if t is None else t + dt


def box_pts(b, pad=4):
    return rect_pts(b[0] - pad, b[1] - pad, b[2] + pad, b[3] + pad)


def grow_rect(x0, y0, w, h, fill, t, dur=0.8, stroke=None, extra=""):
    """A bar grown from its left end at t (there at t None)."""
    st = (f' stroke="{rgb(stroke)}" stroke-width="1.4"' if stroke else "")
    if t is None:
        return (f'<rect x="{_fmt(x0)}" y="{_fmt(y0)}" width="{_fmt(w)}" '
                f'height="{_fmt(h)}" rx="4" fill="{rgb(fill)}"{st}{extra}/>')
    return (f'<rect x="{_fmt(x0)}" y="{_fmt(y0)}" width="0" height="{_fmt(h)}" '
            f'rx="4" fill="{rgb(fill)}"{st}{extra}><animate attributeName="width" '
            f'values="0;{_fmt(w)}" begin="{t_s(t)}" dur="{dur:.2f}s" fill="freeze" '
            f'calcMode="spline" keyTimes="0;1" keySplines="{EASE}"/></rect>')


def not_svg(xy, r, t, col=NOT_RED, width=3.2):
    """The not-mark (svg_vocab), traced ring then bar at t, or there."""
    ring, bar = not_mark_points(xy, r)
    return (trace(ring, col, width, t, 0.5)
            + trace(bar, col, width, _later(t, 0.45), 0.3))


def arrow(pts, col, t, width=2.4, dur=0.8, head=9):
    """A line traced along pts with a head at its end."""
    (ax, ay), (bx, by) = pts[-2], pts[-1]
    a = math.atan2(by - ay, bx - ax)
    hd = [(bx - head * math.cos(a - 0.45), by - head * math.sin(a - 0.45)),
          (bx, by),
          (bx - head * math.cos(a + 0.45), by - head * math.sin(a + 0.45))]
    return (trace(pts, col, width, t, dur)
            + appear(trace(hd, col, width, None), _later(t, dur - 0.1), dur=0.25))


def wave(x0, x1, y, amp=4, step=8):
    n = max(2, int((x1 - x0) / step))
    return [(x0 + (x1 - x0) * k / n, y + (amp if k % 2 else -amp)) for k in range(n + 1)]


def _hand_d(shape, arm):
    pts = [(max(x, -arm), y) for x, y in shape]
    return "M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in pts) + " Z"


HAND_ORDER = ("arm", "palm", "patch", "f3", "f2", "f1", "f0", "th")


def hand_svg(pose, at, ang, s, flip=1, to=None, t=None, dur=0.5, arm=34):
    """svg_figures.hand at `at` (the wrist), its forearm run at `ang`
    degrees, scale s; with `to` and t it closes into that pose at t (the
    poses share their point counts, so the outlines morph)."""
    sh0 = F.hand(pose)
    sh1 = F.hand(to) if to else None
    out = []
    for name in HAND_ORDER:
        d0 = _hand_d(sh0[name], arm)
        anim = ""
        if sh1 is not None and t is not None and name not in ("arm", "patch"):
            d1 = _hand_d(sh1[name], arm)
            if d1 != d0:
                anim = (f'<animate attributeName="d" values="{d0};{d1}" '
                        f'begin="{t_s(t)}" dur="{dur:.2f}s" fill="freeze" '
                        f'calcMode="spline" keyTimes="0;1" keySplines="{EASE}"/>')
        elif sh1 is not None and t is None and name not in ("arm", "patch"):
            d0 = _hand_d(sh1[name], arm)
        if name == "patch":
            out.append(f'<path d="{d0}" fill="{rgb(SKIN)}"/>')
        else:
            out.append(f'<path d="{d0}" fill="{rgb(SKIN)}" stroke="{rgb(TEXT)}" '
                       f'stroke-width="{1.3 / s:.3f}" stroke-linejoin="round">{anim}</path>')
    return (f'<g transform="translate({_fmt(at[0])} {_fmt(at[1])}) rotate({ang:.1f}) '
            f'scale({_fmt(flip * s)} {_fmt(-s)})">' + "".join(out) + "</g>")


def slide(inner, path, t, dur=1.0, show=None):
    """`inner` (drawn about (0, 0)) standing at path[0] from `show` (or t),
    and moved along the path at t, once; at its end from the first frame
    when t is None."""
    if t is None:
        x, y = path[-1]
        return f'<g transform="translate({_fmt(x)} {_fmt(y)})">{inner}</g>'
    x0, y0 = path[0]
    rel = [(x - x0, y - y0) for x, y in path]
    sh = t if show is None else min(show, t)
    return (f'<g opacity="0"><set attributeName="opacity" to="1" begin="{t_s(sh)}"/>'
            f'{fade(sh, 0.3)}<g transform="translate({_fmt(x0)} {_fmt(y0)})"><g>'
            f'{motion(rel, t, dur)}{inner}</g></g></g>')


class _Card(Station):
    """What G and K share: the not-mark verb and a target-box cache."""

    def _box(self, ctx, key):
        T = self.targets(ctx)
        if key not in T:
            raise KeyError(f"{self.key}: no target {key!r}")
        return T[key].box

    def act(self, ctx, verb, key, t, opts):
        if verb == "not":
            b = self._box(ctx, key)
            r = opts.get("r") or max(18, min(60, 0.62 * max(b[2] - b[0], b[3] - b[1])))
            return not_svg(((b[0] + b[2]) / 2, (b[1] + b[3]) / 2), r, t)
        if verb == "move":
            return self.move(ctx, key, t, opts)
        return super().act(ctx, verb, key, t, opts)

    def move(self, ctx, key, t, opts):
        raise KeyError(f"{self.key}: no move for {key!r}")


# ---------------------------------------------------------------------------
# G: the meal offering
# ---------------------------------------------------------------------------

GS_Y = 292                                   # the supplies' ground
JAR_X, JAR_S = 92, 3.0
BASKET_X, BASKET_S = 236, 3.8
CUP_X, CUP_S = 384, 5.0
BASKET_TOP = GS_Y - 24.5 * BASKET_S          # 199
FLOUR_GY = BASKET_TOP + 8
SUP_CHIP_Y = GS_Y + 24
HAND_AT, HAND_ANG, HAND_S = (292, 146), 140, 5.0
G_PALM = (BASKET_X + 6, FLOUR_GY - 14)    # where the handful sits
PRIEST_X, PRIEST_GY, PRIEST_S = 528, 300, 1.45
BAR_Y, BAR_H = 350, 40
BAR_X0, BAR_MEM, BAR_X1 = 40, 150, 500
FR_GY = 506                                  # the ears' ground
FR_XS = (196, 256, 316)
FR_S = 7.2
FR_FLAME_GY = 566
FR_CUP = (478, 528)
MH_Y = 72                                    # "most holy"
BR_Y = 98                                    # the bracket's line
NAME_Y = 128
NAME_X = {"meal": 668, "sin": 792, "trespass": 930}
EQ_X = 853
MALES_X = (672, 748, 824, 900)
MALES_GY, MALES_S = 500, 1.36
PORTION = (930, 300)                         # what the hand touches


def _name_box(key, size=16):
    w = text_w(OF.OFFERING[key].name, size)
    x = NAME_X[key]
    return (x - w / 2, NAME_Y - 11, x + w / 2, NAME_Y + 11)


class Meal(_Card):
    key = "G"

    def shots(self):
        return {"": (1.0, CW / 2, CH / 2),
                "supplies": self.clamp_shot(1.4, 270, 210),
                "fruits": self.clamp_shot(1.4, 300, 470)}

    # -- pieces -----------------------------------------------------------
    def _priest_fig(self, c):
        return c.figure(F.priest(), PRIEST_X, PRIEST_GY, PRIEST_S, TEXT, PANEL)

    def _needs_priest(self, c, t):
        """The priest, for a target that points at him, unless G.priest is
        drawn in this file (lit, or lit before) or another target drew him."""
        if "G.priest" in c.before or "G.priest" in c.lit or getattr(c, "_g_priest", False):
            return ""
        c._g_priest = True
        return appear(self._priest_fig(c), t)

    def targets(self, ctx):
        T = {}
        # -- the supplies -------------------------------------------------
        jar = F.jar()
        jb = F.bbox((jar, 0))
        jbox = (JAR_X + jb[0] * JAR_S, GS_Y - jb[3] * JAR_S, JAR_X + jb[1] * JAR_S, GS_Y)
        T["G.oil"] = Target("G.oil", box=jbox, outline=[(F.outline(jar, JAR_X, GS_Y, JAR_S), True)],
                            draw=lambda c, t: appear(c.figure(jar, JAR_X, GS_Y, JAR_S, GOLD, PANEL), t)
                            + c.chip("G.oil", "oil", (JAR_X, SUP_CHIP_Y), t=t))
        bk = F.basket()
        bb = F.bbox((bk, 0))
        bbox_ = (BASKET_X + bb[0] * BASKET_S, FLOUR_GY - 30, BASKET_X + bb[1] * BASKET_S, GS_Y)

        def flour(c, t):
            return (appear(c.figure(bk, BASKET_X, GS_Y, BASKET_S, FLOUR, PANEL)
                           + heap(BASKET_X, FLOUR_GY, 92, 30, FLOUR), t)
                    + c.chip("G.flour", "fine flour", (BASKET_X, SUP_CHIP_Y), t=t))
        T["G.flour"] = Target("G.flour", box=bbox_, outline=[(F.outline(bk, BASKET_X, GS_Y, BASKET_S), True)],
                              draw=flour)
        cup = F.cup()
        cb = F.bbox((cup, 0))
        cbox = (CUP_X + cb[0] * CUP_S, GS_Y - cb[3] * CUP_S - 12, CUP_X + cb[1] * CUP_S, GS_Y)

        def incense(c, t):
            top = GS_Y - cb[3] * CUP_S
            return (appear(c.figure(cup, CUP_X, GS_Y, CUP_S, FLOUR, PANEL)
                           + heap(CUP_X, top + 4, 34, 14, FLOUR), t)
                    + c.chip("G.frankincense", "frankincense", (CUP_X, SUP_CHIP_Y), t=t))
        T["G.frankincense"] = Target("G.frankincense", box=cbox,
                                     outline=[(F.outline(cup, CUP_X, GS_Y, CUP_S), True)], draw=incense)
        mouth = (JAR_X + 2, GS_Y - jb[3] * JAR_S - 2)
        pour = [mouth, (JAR_X + 30, mouth[1] - 40), (BASKET_X - 66, mouth[1] - 52),
                (BASKET_X - 22, FLOUR_GY - 22), (BASKET_X - 8, FLOUR_GY - 16)]
        pour = F.smooth(pour, closed=False, n=4)
        T["G.pour"] = Target("G.pour", outline=[(pour, False)],
                             draw=lambda c, t: trace(pour, OIL, 5, t, 1.0)
                             + appear(f'<ellipse cx="{_fmt(BASKET_X - 6)}" cy="{_fmt(FLOUR_GY - 14)}" '
                                      f'rx="18" ry="5" fill="{rgb(OIL)}" fill-opacity="0.85"/>',
                                      _later(t, 0.9), dur=0.4))
        palm = G_PALM

        def handful(c, t):
            h = hand_svg("open", HAND_AT, HAND_ANG, HAND_S, flip=1, to="cup",
                         t=_later(t, 0.5), dur=0.5, arm=20)
            grain = "" if _moves(c, "G.handful") else heap(palm[0] + 4, palm[1] + 4, 30, 12, FLOUR)
            body = appear(grain, _later(t, 0.85), dur=0.3) + h
            return (appear(body, t, "lift", 0.5, lift=-16)
                    + c.chip("G.handful", "handful", (250, 92), lead=(palm[0] + 6, palm[1] - 14),
                             t=_later(t, 0.4)))
        hb = (palm[0] - 34, HAND_AT[1] - 30, HAND_AT[0] + 40, palm[1] + 14)
        T["G.handful"] = Target("G.handful", box=hb,
                                outline=[(ellipse_pts(palm[0] + 6, palm[1] - 2, 46, 30), True)],
                                draw=handful)
        T["G.memorial_portion"] = Target(
            "G.memorial_portion", box=(380, 78, 524, 104),
            draw=lambda c, t: c.chip("G.memorial_portion", "memorial portion", (452, 92),
                                     lead=(palm[0] + 30, palm[1] - 24), t=t))
        # -- the priest ---------------------------------------------------
        pb = (PRIEST_X - 26, PRIEST_GY - 105 * PRIEST_S, PRIEST_X + 26, PRIEST_GY)
        pring = F.outline(F.priest(), PRIEST_X, PRIEST_GY, PRIEST_S)

        def priest(c, t):
            c._g_priest = True
            return appear(self._priest_fig(c), t)
        T["G.priest"] = Target("G.priest", box=pb, outline=[(pring, True)], draw=priest)
        T["G.the_priests"] = Target(
            "G.the_priests", box=(PRIEST_X - 50, PRIEST_GY + 12, PRIEST_X + 50, PRIEST_GY + 36),
            outline=[(pring, True)],
            draw=lambda c, t: self._needs_priest(c, t)
            + c.chip("G.the_priests", "the priest's", (PRIEST_X, PRIEST_GY + 24), t=t))
        rem_path = [(BASKET_X + 16, FLOUR_GY - 4), (380, 236), (PRIEST_X - 40, PRIEST_GY - 8)]

        def remnant(c, t):
            return self._needs_priest(c, t) + slide(heap(0, 0, 44, 16, FLOUR), rem_path, t, 1.1)
        T["G.remnant"] = Target("G.remnant", box=(PRIEST_X - 64, PRIEST_GY - 24,
                                                  PRIEST_X - 16, PRIEST_GY),
                                outline=[(ellipse_pts(PRIEST_X - 40, PRIEST_GY - 12, 30, 16), True)],
                                draw=remnant)
        # -- the split bar ------------------------------------------------
        sb = (BAR_X0, BAR_Y, BAR_X1, BAR_Y + BAR_H)
        T["G.split"] = Target("G.split", box=sb, outline=[(box_pts(sb, 3), True)],
                              draw=lambda c, t: appear(self._bar_frame(), t))
        mb = (BAR_X0, BAR_Y, BAR_MEM, BAR_Y + BAR_H)

        def memorial(c, t):
            frame = "" if ("G.split" in c.before or "G.split" in c.lit) else appear(self._bar_frame(), t)
            seg = appear(f'<rect x="{BAR_X0}" y="{BAR_Y}" width="{BAR_MEM - BAR_X0}" '
                         f'height="{BAR_H}" rx="4" fill="{rgb(mix(PANEL, FLOUR, .7))}" '
                         f'stroke="{rgb(FLOUR)}" stroke-width="1.4"/>', t)
            return (frame + seg + c.label("G.memorial", "memorial", ((BAR_X0 + BAR_MEM) / 2,
                                                                    BAR_Y + BAR_H / 2), 15,
                                          BG, "mm", t=t))
        T["G.memorial"] = Target("G.memorial", box=mb, outline=[(box_pts(mb, 3), True)], draw=memorial)
        rb = (BAR_MEM + 3, BAR_Y, BAR_X1, BAR_Y + BAR_H)

        def rest(c, t):
            frame = ("" if any(k in c.before or k in c.lit for k in ("G.split", "G.memorial"))
                     else appear(self._bar_frame(), t))
            return (frame + grow_rect(BAR_MEM + 3, BAR_Y, BAR_X1 - BAR_MEM - 3, BAR_H,
                                      mix(PANEL, SAND, .55), t, 0.9, stroke=SAND)
                    + c.label("G.rest", "Aaron and his sons", ((BAR_MEM + BAR_X1) / 2,
                                                               BAR_Y + BAR_H / 2), 16, BG, "mm",
                              t=_later(t, 0.6)))
        T["G.rest"] = Target("G.rest", box=rb, outline=[(box_pts(rb, 3), True)], draw=rest)
        # -- the first fruits ---------------------------------------------
        ears = F.grass()
        eb = F.bbox((ears, 0))
        frb = (FR_XS[0] + eb[0] * FR_S, FR_GY - eb[3] * FR_S, FR_XS[-1] + eb[1] * FR_S, FR_GY)

        def fruits(c, t):
            figs = "".join(appear(c.figure(ears, x, FR_GY, FR_S, GOLD, PANEL), _later(t, i * 0.15),
                                  "grow", 0.5, about=(x, FR_GY))
                           for i, x in enumerate(FR_XS))
            return figs + c.chip("G.fruits", "first fruits", (96, 438),
                                 lead=(frb[0] + 6, 440), t=t)
        T["G.fruits"] = Target("G.fruits", box=frb, outline=[(box_pts(frb, 6), True)], draw=fruits)
        fxs = [FR_XS[0] + 4, FR_XS[1] + 4, FR_XS[2] + 4]

        def parched(c, t):
            return (appear(flames(fxs, FR_FLAME_GY, [30, 40, 30]), t, "grow", 0.6,
                           about=(FR_XS[1], FR_FLAME_GY))
                    + c.chip("G.parched", "parched", (92, 544), lead=(fxs[0] - 18, 552), t=t))
        T["G.parched"] = Target("G.parched", box=(fxs[0] - 16, FR_FLAME_GY - 42, fxs[-1] + 16, FR_FLAME_GY),
                                outline=[(box_pts((fxs[0] - 16, FR_FLAME_GY - 42, fxs[-1] + 16,
                                                   FR_FLAME_GY), 3), True)], draw=parched)
        T["G.bruised"] = Target("G.bruised", box=frb, outline=[(box_pts(frb, 10), True)],
                                draw=lambda c, t: c.chip("G.bruised", "bruised", (96, 486),
                                                         lead=(frb[0] + 10, 484), t=t))
        oil_w = F.smooth(wave(frb[0] + 10, frb[2] - 10, frb[1] + 26, 4, 30), closed=False, n=4)
        T["G.fruit_oil"] = Target("G.fruit_oil", outline=[(oil_w, False)],
                                  draw=lambda c, t: trace(oil_w, OIL, 4.5, t, 0.9))
        fcx, fgy = FR_CUP
        fcb = (fcx + cb[0] * 4.2, fgy - cb[3] * 4.2 - 10, fcx + cb[1] * 4.2, fgy)

        def fruit_incense(c, t):
            top = fgy - cb[3] * 4.2
            return (appear(c.figure(cup, fcx, fgy, 4.2, FLOUR, PANEL)
                           + heap(fcx, top + 4, 28, 12, FLOUR), t)
                    + c.chip("G.fruit_frankincense", "frankincense", (fcx, fgy + 26), t=t))
        T["G.fruit_frankincense"] = Target("G.fruit_frankincense", box=fcb,
                                           outline=[(F.outline(cup, fcx, fgy, 4.2), True)],
                                           draw=fruit_incense)
        part_path = [(FR_XS[2] + 8, frb[1] + 30), (370, 432), (400, 470)]

        def part(c, t):
            tok = (heap(0, 0, 34, 15, GOLD) + f'<ellipse cx="0" cy="-12" rx="9" ry="3" '
                   f'fill="{rgb(OIL)}"/>')
            return (slide(tok, part_path, t, 1.0)
                    + c.chip("G.part", "part", (400, 496), t=_later(t, 0.6)))
        T["G.part"] = Target("G.part", box=(380, 452, 420, 472),
                             outline=[(ellipse_pts(400, 462, 28, 18), True)], draw=part)
        T["G.all_frankincense"] = Target(
            "G.all_frankincense", box=fcb, outline=[(F.outline(cup, fcx, fgy, 4.2), True)],
            draw=lambda c, t: c.chip("G.all_frankincense", "all its frankincense", (482, 440),
                                     lead=(fcx, fcb[1] + 2), t=t))
        # -- most holy ----------------------------------------------------
        mbx = _name_box("meal")

        def most_holy(c, t):
            stub = [(mbx[0] - 4, BR_Y + 10), (mbx[0] - 4, BR_Y), (mbx[2] + 4, BR_Y),
                    (mbx[2] + 4, BR_Y + 10)]
            return (trace(stub, TEXT, 2.2, t, 0.6)
                    + c.chip("G.most_holy", "most holy", (NAME_X["meal"], MH_Y),
                             lead=(NAME_X["meal"], BR_Y), t=t)
                    + c.label("G.most_holy:meal", OF.OFFERING["meal"].name,
                              (NAME_X["meal"], NAME_Y), 16, TEXT, "mm", t=_later(t, 0.3)))
        T["G.most_holy"] = Target("G.most_holy", box=(mbx[0] - 6, MH_Y - 14, mbx[2] + 6, mbx[3]),
                                  outline=[(box_pts((mbx[0] - 6, BR_Y - 4, mbx[2] + 6, mbx[3]), 2),
                                            True)],
                                  draw=most_holy)
        T["G.name_meal"] = Target("G.name_meal", box=mbx, outline=[(box_pts(mbx, 4), True)])
        tbx = _name_box("trespass")
        full = [(mbx[0] - 4, BR_Y + 10), (mbx[0] - 4, BR_Y), (tbx[2] + 4, BR_Y),
                (tbx[2] + 4, BR_Y + 10)]
        T["G.bracket"] = Target("G.bracket", box=(mbx[0] - 6, BR_Y - 4, tbx[2] + 6, tbx[3]),
                                outline=[(box_pts((mbx[0] - 6, BR_Y - 4, tbx[2] + 6, tbx[3]), 3),
                                          True)],
                                draw=lambda c, t: trace(full, TEXT, 2.2, t, 0.9))
        for k in ("sin", "trespass"):
            b = _name_box(k)
            T[f"G.name_{k}"] = Target(
                f"G.name_{k}", box=b, outline=[(box_pts(b, 4), True)],
                draw=lambda c, t, k=k: c.label(f"G.name_{k}", OF.OFFERING[k].name,
                                               (NAME_X[k], NAME_Y), 16, TEXT, "mm", t=t, how="lift"))
        eq = [[(EQ_X - 8, NAME_Y - 4), (EQ_X + 8, NAME_Y - 4)],
              [(EQ_X - 8, NAME_Y + 4), (EQ_X + 8, NAME_Y + 4)]]
        law = OF.ONE_LAW[-1].label

        def one_law(c, t):
            return ("".join(trace(p, GOLD, 2.6, _later(t, i * 0.25), 0.3) for i, p in enumerate(eq))
                    + c.chip("G.one_law", law, (EQ_X + 10, 172), lead=(EQ_X, NAME_Y + 10),
                             t=_later(t, 0.3)))
        T["G.one_law"] = Target("G.one_law", box=(EQ_X - 12, NAME_Y - 10, EQ_X + 12, NAME_Y + 10),
                                outline=[(ellipse_pts(EQ_X, NAME_Y, 16, 14), True)], draw=one_law)
        to_p = [(EQ_X + 10 - text_w(law, 16) / 2 - 10, 176), (680, 206), (PRIEST_X + 34, 222)]
        T["G.to_priest"] = Target("G.to_priest", outline=[(to_p, False)],
                                  draw=lambda c, t: self._needs_priest(c, t)
                                  + arrow(to_p, TEXT, t, 2.4, 0.8))
        # -- every male ---------------------------------------------------
        pr = F.priest()
        mlb = (MALES_X[0] - 28, MALES_GY - 105 * MALES_S, MALES_X[-1] + 28, MALES_GY)

        def males(c, t):
            did = c.fig_def("g_priest", pr, MALES_S)
            figs = "".join(appear(c.use(did, x, MALES_GY), _later(t, i * 0.2), "lift", 0.4)
                           for i, x in enumerate(MALES_X))
            return figs + c.chip("G.males", "every male", ((MALES_X[0] + MALES_X[-1]) / 2,
                                                           MALES_GY + 26), t=t)
        T["G.males"] = Target("G.males", box=mlb, outline=[(box_pts(mlb, 8), True)], draw=males)
        T["G.forever"] = Target("G.forever", box=(930, 398, 1000, 422),
                                draw=lambda c, t: c.chip("G.forever", "forever", (962, 420), t=t))
        px_, py_ = PORTION

        def touch(c, t):
            dish = heap(px_, py_, 46, 18, FLOUR)
            h = hand_svg("near", (px_ + 56, py_ - 22), 180, 3.0, flip=1, to="rest",
                         t=_later(t, 0.3), dur=0.4, arm=12)
            return (appear(dish, t) + appear(h, t, "lift", 0.5, lift=-14)
                    + c.chip("G.touch", "holy", (px_ - 4, py_ + 30), t=_later(t, 0.5)))
        T["G.touch"] = Target("G.touch", box=(px_ - 30, py_ - 80, px_ + 30, py_),
                              outline=[(ellipse_pts(px_, py_ - 8, 34, 18), True)], draw=touch)
        return T

    def _bar_frame(self):
        return (f'<rect x="{BAR_X0}" y="{BAR_Y}" width="{BAR_X1 - BAR_X0}" height="{BAR_H}" '
                f'rx="4" fill="none" stroke="{rgb(SAND)}" stroke-width="1.6" '
                f'stroke-dasharray="7 5"/>')

    def move(self, ctx, key, t, opts):
        T = self.targets(ctx)
        if key == "G.handful":
            # the handful taken up for the fire: the flour in the cupped hand
            # (drawn here, not by the hand, when the verse moves it) rises
            # and goes, once
            tl = ctx.lit.get("G.handful")
            show = (tl + 0.85) if tl is not None else opts.get("_show", opts.get("_arrive", t))
            show = min(show, t)
            px, py = G_PALM
            grain = heap(0, 0, 30, 12, FLOUR)
            return (f'<g opacity="0"><set attributeName="opacity" to="1" begin="{t_s(show)}"/>'
                    f'{fade(show, 0.3)}<g>{fade(t + 0.5, 0.5, out=True)}'
                    f'<g transform="translate({_fmt(px + 4)} {_fmt(py + 4)})"><g>'
                    f'{motion([(0, 0), (40, -60), (110, -120)], t, 1.0)}{grain}</g></g></g></g>')
        if key in ("G.part", "G.remnant"):
            return T[key].draw(ctx, t)
        return super().move(ctx, key, t, opts)


def _moves(ctx, key):
    """Whether this file's verse moves `key` (verb "move")."""
    V = getattr(ctx, "verse", None)
    for stop in getattr(V, "stops", ()) or ():
        for b in stop.beats:
            if b[0] == "move" and b[1] == key:
                return True
    return False


# ---------------------------------------------------------------------------
# K: the kitchen
# ---------------------------------------------------------------------------

# K is four quadrants, each a s 2 close-up (cook, rules / measure,
# vessels): no word crosses x 512 or y 288, so no close-up cuts one
KC_GY = 244                                  # the cookware's ground
OVEN_X, GRID_X, PAN_X, KC_S = 84, 236, 380, 2.0
KC_CHIP_Y = KC_GY + 22
RULE_X = 640                                 # yeast and honey
YEAST_Y, HONEY_Y = 64, 132
FF_XY = (860, 46)                            # "first fruits"
ALTAR_XY = (850, 172)                        # its foot
SALT_XY = (570, 270)                         # the salt cup's foot
NAMES_X, NAMES_Y0, NAMES_DY = 900, 192, 20
MEAS_X0, MEAS_Y, MEAS_W, MEAS_H = 40, 392, 40, 36
MEAS_X1 = MEAS_X0 + 10 * MEAS_W
SPLIT_Y = 466
KM_GY = 548                                  # the basket, jar and cup (their not-rings clear the card's foot)
POT_GY, POT_S = 526, 2.0
EARTH_X, BRONZE_X = 590, 730
COAT_X, COAT_GY, COAT_H = 900, 540, 196
HOLY_XY = (650, 352)                         # the flesh touched


def _oil_on(x0, x1, y):
    return F.smooth([(x0, y), ((x0 + x1) / 2 - 8, y - 6), ((x0 + x1) / 2 + 10, y + 3), (x1, y - 2)],
                    closed=False, n=4)


class Kitchen(_Card):
    key = "K"

    def pkey(self, key, verse):
        """The not-marks are each case's own (leviticus17_stations.case_of):
        5:11's oil and frankincense struck out aren't struck at 6:20, whose
        meal offering is made with oil."""
        if key.startswith("K.not:"):
            return f"{key}@{case_of(getattr(verse, 'ref', None))}"
        return key

    def shots(self):
        return {"": (1.0, CW / 2, CH / 2),
                "cook": (2.0, 256, 144),
                "griddle": (2.4, 373.3, 190),
                "rules": (2.0, 768, 144),
                "measure": (2.0, 256, 432),
                "vessels": (2.0, 768, 432)}

    def targets(self, ctx):
        T = {}
        # -- cook ---------------------------------------------------------
        vessel = {v.key: v for v in OF.VESSELS}
        cook = {"oven": (OVEN_X, F.cookware("oven", "bread")),
                "griddle": (GRID_X, F.cookware("griddle", "bread")),
                "pan": (PAN_X, F.cookware("pan", "bread"))}
        for k, (x, parts) in cook.items():
            b = F.bbox((parts, 0))
            box = (x + b[0] * KC_S, KC_GY - b[3] * KC_S, x + b[1] * KC_S, KC_GY)
            cx = x if k != "pan" else x + 6

            def draw(c, t, k=k, x=x, parts=parts, cx=cx):
                return (appear(c.figure(parts, x, KC_GY, KC_S, BRONZE if k != "oven" else CLAY,
                                        PANEL), t, "lift", 0.6, lift=14)
                        + c.chip(f"K.{k}", vessel[k].label, (cx, KC_CHIP_Y), t=t))
            T[f"K.{k}"] = Target(f"K.{k}", box=box, outline=[(F.outline(parts, x, KC_GY, KC_S), True)],
                                 draw=draw)
        # the griddle's round: its cake lies at y 17 (units) and is 34 wide
        rx0, rx1 = GRID_X - 17 * KC_S * F.UNIT["cookware"], GRID_X + 17 * KC_S * F.UNIT["cookware"]
        ry = KC_GY - 18.4 * KC_S * F.UNIT["cookware"]
        cuts = [[(GRID_X + dx - 5, ry - 6), (GRID_X + dx + 5, ry + 8)] for dx in (-22, 0, 22)]
        T["K.cut"] = Target("K.cut", box=(rx0, ry - 10, rx1, ry + 10),
                            outline=[(box_pts((rx0, ry - 10, rx1, ry + 10), 4), True)],
                            draw=lambda c, t: "".join(trace(p, BG, 2.6, _later(t, i * 0.2), 0.3)
                                                      for i, p in enumerate(cuts)))
        oil = _oil_on(rx0 + 6, rx1 - 6, ry - 4)
        T["K.oil"] = Target("K.oil", outline=[(oil, False)],
                            draw=lambda c, t: trace(oil, OIL, 4.5, t, 0.8))
        T["K.mixed"] = Target("K.mixed", box=(GRID_X - 70, 112, GRID_X + 50, 136),
                              draw=lambda c, t: c.chip("K.mixed", "mixed with oil", (GRID_X - 10, 124),
                                                       lead=(GRID_X + 34, ry - 8), t=t))
        T["K.soaked"] = Target("K.soaked", box=(GRID_X + 54, 112, GRID_X + 114, 136),
                               draw=lambda c, t: c.chip("K.soaked", "soaked", (GRID_X + 84, 124),
                                                        lead=(rx1 - 10, ry - 6), t=t))
        T["K.baked_pieces"] = Target("K.baked_pieces", box=(GRID_X - 58, 148, GRID_X + 42, 172),
                                     draw=lambda c, t: c.chip("K.baked_pieces", "baked pieces",
                                                              (GRID_X - 8, 160),
                                                              lead=(GRID_X - 22, ry - 6), t=t))
        bread = F.bread()

        def cakes(c, t):
            figs = "".join(appear(c.figure(bread, OVEN_X - 50 + i * 50, 118, 2.8, FLOUR, PANEL),
                                  _later(t, i * 0.15), "lift", 0.4)
                           for i in range(3))
            return figs + c.chip("K.cakes", "unleavened cakes", (OVEN_X + 4, 84), t=t)
        T["K.cakes"] = Target("K.cakes", box=(OVEN_X - 72, 100, OVEN_X + 72, 118),
                              outline=[(box_pts((OVEN_X - 72, 100, OVEN_X + 72, 118), 4), True)],
                              draw=cakes)
        wx = PAN_X + 20

        def wafers(c, t):
            ws = "".join(appear(f'<ellipse cx="{_fmt(wx + i * 6)}" cy="{_fmt(124 - i * 8)}" rx="34" '
                                f'ry="5" fill="{rgb(mix(PANEL, FLOUR, .75))}" '
                                f'stroke="{rgb(FLOUR)}" stroke-width="1.3"/>',
                                _later(t, i * 0.15), "lift", 0.4) for i in range(3))
            return ws + c.chip("K.wafers", "unleavened wafers", (wx - 6, 84), t=t)
        T["K.wafers"] = Target("K.wafers", box=(wx - 36, 102, wx + 50, 130),
                               outline=[(box_pts((wx - 36, 102, wx + 50, 130), 4), True)],
                               draw=wafers)
        # -- rules --------------------------------------------------------
        yb = (RULE_X - 70, YEAST_Y - 24, RULE_X + 40, YEAST_Y + 14)
        hb = (RULE_X - 70, HONEY_Y - 34, RULE_X + 40, HONEY_Y + 14)

        def yeast(c, t):
            lump = F.smooth([(-16, 0), (-15, 9), (-6, 16), (6, 16), (15, 9), (16, 0)], n=4)
            lp = [(RULE_X - 50 + x, YEAST_Y + 8 - y) for x, y in lump]
            el = (f'<polygon points="{pts_str(lp)}" fill="{rgb(mix(PANEL, FLOUR, .6))}" '
                  f'stroke="{rgb(FLOUR)}" stroke-width="1.4"/>')
            return appear(el, t) + c.chip("K.yeast", "yeast", (RULE_X + 6, YEAST_Y), t=t)
        T["K.yeast"] = Target("K.yeast", box=yb, outline=[(box_pts(yb, 4), True)], draw=yeast)
        jar = F.jar()

        def honey(c, t):
            return (appear(c.figure(jar, RULE_X - 50, HONEY_Y + 12, 1.7, GOLD, PANEL), t)
                    + c.chip("K.honey", "honey", (RULE_X + 6, HONEY_Y), t=t))
        T["K.honey"] = Target("K.honey", box=hb, outline=[(box_pts(hb, 4), True)], draw=honey)
        # the not-rings clear the words beside them
        icon = {"yeast": (RULE_X - 50, YEAST_Y), "honey": (RULE_X - 50, HONEY_Y - 8)}
        for k, b in (("yeast", yb), ("honey", hb)):
            cxy = icon[k]
            T[f"K.not:{k}"] = Target(f"K.not:{k}", box=(cxy[0] - 24, cxy[1] - 24, cxy[0] + 24, cxy[1] + 24),
                                     outline=[(ellipse_pts(cxy[0], cxy[1], 27, 27), True)],
                                     draw=lambda c, t, cxy=cxy: not_svg(cxy, 22, t))
        # yeast and honey braced together, then to the altar (struck) and
        # to the first fruits
        bx = RULE_X + 44
        brace = [(bx - 8, YEAST_Y - 14), (bx, YEAST_Y - 14), (bx, HONEY_Y + 12), (bx - 8, HONEY_Y + 12)]
        J = (bx, (YEAST_Y + HONEY_Y) / 2)

        def brace_el(t):
            return trace(brace, TEXT_DIM, 2.0, t, 0.4)
        ax, ay = ALTAR_XY
        alt = F.altar("horned", fire=True)
        ab = F.bbox((alt, 0))
        abox = (ax + ab[0] * 0.5, ay - ab[3] * 0.5, ax + ab[1] * 0.5, ay)
        to_alt = [J, (abox[0] - 10, ay - 26)]
        mid = ((to_alt[0][0] + to_alt[1][0]) / 2, (to_alt[0][1] + to_alt[1][1]) / 2)

        def no_burn(c, t):
            return (appear(c.figure(alt, ax, ay, 0.5, BRONZE, PANEL), t)
                    + c.chip("K.altar", "altar", (abox[2] + 40, ay - 22), t=t)
                    + brace_el(t) + arrow(to_alt, TEXT_DIM, _later(t, 0.3), 2.2, 0.6)
                    + not_svg(mid, 20, _later(t, 0.9)))
        T["K.altar"] = Target("K.altar", box=abox, outline=[(F.outline(alt, ax, ay, 0.5), True)],
                             draw=no_burn)
        ffw = text_w("first fruits", 16)
        to_ff = [J, (FF_XY[0] - ffw / 2 - 12, FF_XY[1] + 6)]
        T["K.first_fruits"] = Target(
            "K.first_fruits", box=(FF_XY[0] - ffw / 2 - 8, FF_XY[1] - 14, FF_XY[0] + ffw / 2 + 8,
                                   FF_XY[1] + 14),
            draw=lambda c, t: c.chip("K.first_fruits", "first fruits", FF_XY, t=t)
            + brace_el(t) + arrow(to_ff, TEXT, _later(t, 0.3), 2.2, 0.6))
        cup = F.cup()
        sx, sy = SALT_XY
        cb = F.bbox((cup, 0))
        sbox = (sx + cb[0] * 3.6, sy - cb[3] * 3.6 - 8, sx + cb[1] * 3.6, sy)

        def salt(c, t):
            top = sy - cb[3] * 3.6
            return (appear(c.figure(cup, sx, sy, 3.6, FLOUR, PANEL) + heap(sx, top + 3, 24, 10, FLOUR), t)
                    + c.chip("K.salt", "salt", (sx + 50, sy - 22), t=t))
        T["K.salt"] = Target("K.salt", box=sbox, outline=[(F.outline(cup, sx, sy, 3.6), True)], draw=salt)
        T["K.covenant"] = Target("K.covenant", box=(sx + 30, sy - 82, sx + 110, sy - 58),
                                 draw=lambda c, t: c.chip("K.covenant", "covenant", (sx + 70, sy - 70),
                                                          t=t))
        # "with all your offerings you shall offer salt" (2:13): the verse's
        # own words, not the five names, which aren't said till 3:1-5:15
        ny = NAMES_Y0 + NAMES_DY * 2
        word = "all your offerings"
        nw = text_w(word, 16)
        nbox = (NAMES_X - nw / 2 - 8, ny - 14, NAMES_X + nw / 2 + 8, ny + 14)

        def names_draw(c, t, word=word, ny=ny, nbox=nbox):
            return (trace([(sx + 72, sy - 22), (nbox[0] - 4, ny)], SAND_DIM, 1.4, t, 0.4)
                    + c.chip("K.names", word, (NAMES_X, ny), 16, t=_later(t, 0.3)))
        T["K.names"] = Target("K.names", box=nbox, outline=[(box_pts(nbox, 2), True)], draw=names_draw)
        # -- measure ------------------------------------------------------
        mbox = (MEAS_X0, MEAS_Y, MEAS_X1, MEAS_Y + MEAS_H)

        def measure(c, t):
            out = [appear(f'<rect x="{MEAS_X0}" y="{MEAS_Y}" width="{MEAS_X1 - MEAS_X0}" '
                          f'height="{MEAS_H}" rx="3" fill="{rgb(mix(PANEL, SAND, .25))}" '
                          f'stroke="{rgb(SAND)}" stroke-width="1.6"/>', t)]
            for i in range(1, 10):
                x = MEAS_X0 + i * MEAS_W
                out.append(trace([(x, MEAS_Y), (x, MEAS_Y + MEAS_H)], SAND, 1.2, _later(t, 0.2 + i * 0.05),
                                 0.2))
            out.append(c.chip("K.measure", "ephah", ((MEAS_X0 + MEAS_X1) / 2 - 40, MEAS_Y - 22), t=t))
            return "".join(out)
        T["K.measure"] = Target("K.measure", box=mbox, outline=[(box_pts(mbox, 3), True)], draw=measure)
        tx0 = MEAS_X1 - MEAS_W
        tbox = (tx0, MEAS_Y, MEAS_X1, MEAS_Y + MEAS_H)
        T["K.tenth"] = Target(
            "K.tenth", box=tbox, outline=[(box_pts(tbox, 3), True)],
            draw=lambda c, t: appear(f'<rect x="{tx0 + 2}" y="{MEAS_Y + 2}" width="{MEAS_W - 4}" '
                                     f'height="{MEAS_H - 4}" rx="2" fill="{rgb(FLOUR)}"/>', t)
            + c.chip("K.tenth", "one tenth", (tx0 + 26, MEAS_Y - 22), lead=(tx0 + MEAS_W / 2, MEAS_Y), t=t))
        half_w = 80
        hx = {"morning": tx0 - 96, "evening": tx0 - 6}
        for k, fig in (("morning", F.sun()), ("evening", F.moon())):
            x0 = hx[k]
            hb_ = (x0, SPLIT_Y, x0 + half_w, SPLIT_Y + 48)
            col = GOLD if k == "morning" else SILVER

            def half(c, t, k=k, x0=x0, fig=fig, col=col):
                link = [(tx0 + MEAS_W / 2, MEAS_Y + MEAS_H + 2), (x0 + half_w / 2, SPLIT_Y - 4)]
                slab_ = (f'<rect x="{x0}" y="{SPLIT_Y}" width="{half_w}" height="20" rx="3" '
                         f'fill="{rgb(FLOUR)}" stroke="{rgb(SAND)}" stroke-width="1.2"/>')
                body = c.figure(fig, x0 + half_w / 2, SPLIT_Y + 42, 0.32, col, PANEL)
                return (trace(link, SAND, 1.6, t, 0.4) + appear(slab_ + body, _later(t, 0.3))
                        + c.label(f"K.{k}", k, (x0 + half_w / 2, SPLIT_Y + 66), 15, TEXT, "mm",
                                  t=_later(t, 0.3)))
            T[f"K.{k}"] = Target(f"K.{k}", box=hb_, outline=[(box_pts(hb_, 4), True)], draw=half)
        items = {"flour": (F.basket(), 72, 2.3, FLOUR, "fine flour"),
                 "jar": (F.jar(), 168, 2.4, GOLD, "oil"),
                 "cup": (F.cup(), 248, 3.6, FLOUR, "frankincense")}
        for k, (parts, x, s_, col, word) in items.items():
            b = F.bbox((parts, 0))
            box = (x + b[0] * s_, KM_GY - b[3] * s_, x + b[1] * s_, KM_GY)

            def item(c, t, k=k, parts=parts, x=x, s_=s_, col=col, word=word, box=box):
                body = c.figure(parts, x, KM_GY, s_, col, PANEL)
                if k == "flour":
                    body += heap(x, box[1] + 6, 56, 18, FLOUR)
                return appear(body, t) + c.chip(f"K.{k}", word, (x, KM_GY - 82), t=t)
            T[f"K.{k}"] = Target(f"K.{k}", box=box, outline=[(F.outline(parts, x, KM_GY, s_), True)],
                                 draw=item)
            if k in ("jar", "cup"):
                nk = "oil" if k == "jar" else "frankincense"
                cxy = ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)
                T[f"K.not:{nk}"] = Target(f"K.not:{nk}", box=box,
                                          outline=[(ellipse_pts(cxy[0], cxy[1], 36, 36), True)],
                                          draw=lambda c, t, cxy=cxy: not_svg(cxy, 32, t))
        # -- vessels ------------------------------------------------------
        pot = F.cookware("pot")
        bpot = F.cookware("pot", bronze=True)
        pb = F.bbox((pot, 0))

        def pot_box(x):
            return (x + pb[0] * POT_S, POT_GY - pb[3] * POT_S, x + pb[1] * POT_S, POT_GY)
        eb = pot_box(EARTH_X)

        def earthen(c, t):
            fig = c.figure(pot, EARTH_X, POT_GY, POT_S, CLAY, PANEL)
            br = c.lit.get("K.broken")
            if "K.broken" in c.before:
                fig = ""
            elif br is not None:
                fig = fade_out(fig, br + 0.7, 0.15)
            return appear(fig, t) + c.chip("K.earthen", vessel["earthen"].label, (EARTH_X, POT_GY + 26), t=t)
        T["K.earthen"] = Target("K.earthen", box=eb, outline=[(ellipse_pts(EARTH_X, POT_GY - 44, 72, 56), True)],
                                draw=earthen)
        L, R, crack = F.pot_halves()
        cpts = [(EARTH_X + x * POT_S, POT_GY - y * POT_S) for x, y in crack]

        def broken(c, t):
            pieces = []
            for half, dx, rot in ((L, -14, -9), (R, 14, 9)):
                fig = c.figure(half, EARTH_X, POT_GY, POT_S, CLAY, PANEL)
                if t is None:
                    pieces.append(f'<g transform="translate({dx} 0) rotate({rot} {EARTH_X} {POT_GY})">'
                                  f'{fig}</g>')
                else:
                    tb = t + 0.7
                    pieces.append(
                        f'<g opacity="0"><set attributeName="opacity" to="1" begin="{t_s(tb)}"/>'
                        f'<g><animateTransform attributeName="transform" type="translate" '
                        f'values="0 0;{dx} 0" begin="{t_s(tb + 0.05)}" dur="0.6s" fill="freeze" '
                        f'calcMode="spline" keyTimes="0;1" keySplines="{EASE}"/>'
                        f'<g><animateTransform attributeName="transform" type="rotate" '
                        f'values="0 {EARTH_X} {POT_GY};{rot} {EARTH_X} {POT_GY}" begin="{t_s(tb + 0.05)}" '
                        f'dur="0.6s" fill="freeze" calcMode="spline" keyTimes="0;1" '
                        f'keySplines="{EASE}"/>{fig}</g></g></g>')
            crk = "" if t is None else fade_out(trace(cpts, BG, 2.4, t, 0.6), t + 0.7, 0.1)
            return ("".join(pieces) + crk
                    + c.chip("K.broken", "broken", (EARTH_X, eb[1] - 22), t=_later(t, 0.7)))
        T["K.broken"] = Target("K.broken", box=eb, outline=[(ellipse_pts(EARTH_X, POT_GY - 44, 72, 56), True)],
                               draw=broken)
        bb = pot_box(BRONZE_X)
        bring = F.outline(bpot, BRONZE_X, POT_GY, POT_S)
        T["K.bronze"] = Target("K.bronze", box=bb, outline=[(bring, True)],
                               draw=lambda c, t: appear(c.figure(bpot, BRONZE_X, POT_GY, POT_S, BRONZE,
                                                                 PANEL), t)
                               + c.chip("K.bronze", vessel["bronze"].label, (BRONZE_X, POT_GY + 26), t=t))
        strokes = [[(BRONZE_X - 26 + k * 13 + (j * 4), POT_GY - 66 + j * 16),
                    (BRONZE_X - 18 + k * 13 + (j * 4), POT_GY - 58 + j * 16)]
                   for j in range(3) for k in range(4)]

        def scoured(c, t):
            return ("".join(trace(p, HL_SCOUR, 2.2, _later(t, i * 0.06), 0.15) for i, p in enumerate(strokes))
                    + c.chip("K.scoured", "scoured", (BRONZE_X - 54, bb[1] - 22), t=t))
        T["K.scoured"] = Target("K.scoured", box=bb, outline=[(bring, True)], draw=scoured)
        drops = [[(BRONZE_X + dx, bb[1] - 14), (BRONZE_X + dx + 2, bb[1] + 30)] for dx in (-14, 0, 14)]
        rw = wave(bb[0] + 8, bb[2] - 8, POT_GY - 30, 4, 10)

        def rinsed(c, t):
            return ("".join(trace(p, WATER, 3, _later(t, i * 0.12), 0.4) for i, p in enumerate(drops))
                    + trace(rw, WATER, 3, _later(t, 0.4), 0.6)
                    + c.chip("K.rinsed", "rinsed", (BRONZE_X + 50, bb[1] - 22), t=_later(t, 0.2)))
        T["K.rinsed"] = Target("K.rinsed", box=bb, outline=[(bring, True)], draw=rinsed)
        # the garment of 6:27
        import svg_priest as SP
        fo = SP.Form(COAT_X, COAT_GY, COAT_H)
        coat_pts = SP.silhouette(fo)
        cbx = bounds(coat_pts)

        def coat(c, t):
            el = (f'<polygon points="{pts_str(coat_pts)}" fill="{rgb(mix(PANEL, WHITE_LINEN, .7))}" '
                  f'stroke="{rgb(WHITE_LINEN)}" stroke-width="1.6"/>')
            spots = "".join(appear(f'<circle cx="{_fmt(COAT_X + dx)}" cy="{_fmt(dy)}" r="{r}" '
                                   f'fill="{rgb(BLOOD)}"/>', _later(t, 0.4 + i * 0.12), "pop", 0.25,
                                   about=(COAT_X + dx, dy))
                            for i, (dx, dy, r) in enumerate(((-8, 428, 7), (6, 440, 5), (-2, 454, 4),
                                                             (12, 422, 3.5))))
            return (appear(el, t) + spots
                    + c.chip("K.coat", "garment", (COAT_X + 76, cbx[1] + 38),
                             lead=(COAT_X + 26, cbx[1] + 44), t=t))
        T["K.coat"] = Target("K.coat", box=cbx, outline=[(coat_pts, True)], draw=coat)
        ww = [wave(COAT_X - 30, COAT_X + 30, y, 4, 8) for y in (412, 436, 460)]
        T["K.wash"] = Target("K.wash", box=(COAT_X - 34, 404, COAT_X + 34, 468),
                             outline=[(box_pts((COAT_X - 34, 404, COAT_X + 34, 468), 4), True)],
                             draw=lambda c, t: "".join(trace(w_, WATER, 3, _later(t, i * 0.25), 0.6)
                                                       for i, w_ in enumerate(ww)))
        T["K.holy_place"] = Target("K.holy_place", box=(COAT_X + 30, 470, COAT_X + 130, 494),
                                   draw=lambda c, t: c.chip("K.holy_place", "holy place",
                                                            (COAT_X + 76, 482), t=t))
        hx_, hy_ = HOLY_XY

        def holy(c, t):
            flesh = (f'<rect x="{hx_ - 34}" y="{hy_ - 12}" width="68" height="24" rx="9" '
                     f'fill="{rgb(mix(PANEL, RED, .75))}" stroke="{rgb(TEXT)}" stroke-width="1.4"/>')
            h = hand_svg("near", (hx_ + 62, hy_ - 26), 180, 2.6, flip=1, to="rest",
                         t=_later(t, 0.3), dur=0.4, arm=12)
            return (appear(flesh, t) + appear(h, t, "lift", 0.5, lift=-12)
                    + c.chip("K.holy", "holy", (hx_ - 70, hy_), t=_later(t, 0.4)))
        T["K.holy"] = Target("K.holy", box=(hx_ - 36, hy_ - 14, hx_ + 36, hy_ + 14),
                             outline=[(ellipse_pts(hx_, hy_, 44, 22), True)], draw=holy)
        return T


HL_SCOUR = (240, 220, 170)


def stations():
    return [Meal(), Kitchen()]
