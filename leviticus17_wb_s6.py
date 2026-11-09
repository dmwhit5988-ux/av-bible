"""Leviticus 6:9-7:10, the laws of the burnt, meal, sin and trespass
offerings and the priests' shares, on the workbench (section s6).

It starts on the s5|s6 boundary (the trespass column filed and active, the
altar set at rest, the places named so far) and the dock's tab switches
(a 0.6 s crossfade) as the law turns from one offering to the next:

- 6:9-13, the burnt offering's law (burnt): the day strip ("all night",
  "morning") over the pen, the burnt offering on the wood, the priest in
  linen, the ashes beside the altar, his other garments, and a man token
  carrying the ashes out of the camp to the clean place on the strip
  (6:11: "the ashes: outside the camp" unveils in NOT EATEN as the token
  crosses the camp's edge); the fire kept burning (a line along the day
  strip, "continually").
- 6:14-23, the meal offering's law (meal): the priest, the flour, oil and
  frankincense and the handful to the fire (6:15), "without yeast", "most
  holy" as the sin and trespass offerings (their tabs pulse), every male;
  then the anointing day (6:20-23): the tenth halved for morning and
  evening, the griddle, soaked, the baked pieces to the fire, "wholly
  burned" ("all of it" unveils), and "a priest's own" flies from the
  not-marked cake to NOT EATEN (6:23).
- 6:25-30, the sin offering's law (sin): the north side, "most holy", the
  priests' portion (the dish; "the priests" flies to WHO EATS, 6:26), the
  court, the garment washed (6:27), the earthen vessel broken and the bronze
  one scoured and rinsed (6:28), every male, and the blood carried into the
  Tent: its path traced on the strip to the Holy Place, the dish not-marked
  and "blood in the Tent: burned" unveiled on "burned" (6:30).
- 7:1-7, the trespass offering's law (trespass): the ram, the north side, the
  ring round the altar (7:2), the ram's cutaway and its fat, kidneys and
  liver (7:3-4), the fat to the wood and the fire ("the fat" flies, 7:5),
  every male ("the priests" flies, 7:6), "one law" for the sin and trespass
  offerings (7:7).
- 7:8-10, the shares (burnt at 7:8, meal at 7:9), in three rows left of the
  altar, which stays: the skin to the priest ("the skin: the priest's"
  flies off him), the oven, pan and griddle to the priest ("the priest"
  unveils on "priest's"), mixed with oil or dry to all the sons of Aaron
  ("the priests" flies); then the board clears.

It leaves the s6|s7 boundary: the meal tab active, the altar set at rest,
the strip's places, nothing else of its own.

Moves (QC's budget): no camera; chip flights at 6:23, 6:26, 7:5, 7:6, 7:8,
7:10 (one a file); bench moves at 6:10 (the ashes beside the altar), 6:15
(the handful), 6:20 (the two halves), 6:21 (the baked pieces), 7:5 (the
fat onto the wood); a token walk at 6:11 (the ashes out of the camp).
"""

import generate_tabernacle as GT
import leviticus17_bench as B
import leviticus17_dock as D
import leviticus17_parts as P
import leviticus17_art as ART
import svg_figures as F
from generate_tabernacle import (GOLD, PANEL, SAND, SAND_DIM, TEXT, TEXT_DIM,
                                 WHITE_LINEN)
from leviticus17_bench import (El, add, cue, at, fit, pulse_el, traced_el, glide, rect_pts,
                               f2, rgb)
from leviticus17_parts import S, BLOOD, WATER
from svg_vocab import mix

STUB = False
VERSES = [(6, v) for v in range(9, 31)] + [(7, v) for v in range(1, 11)]

REACH = {}
EXCUSED = {}

E = B.ELS
NIGHT = (58, 66, 110)
DAWN = (226, 176, 92)
FLOUR = WHITE_LINEN
OIL = (226, 186, 84)
MEAT = P.MEAT
FIRE = ART.FIRE_OUT

# the pen's people stand here
PR_X, PR_G, PR_K = 52, 548, 1.45            # a priest at bench size (152 px)
MALES_X = (150, 195, 240, 285)               # every male: four priests in a row
MALES_K = 0.95
CHIP_TOP = 262                               # the pen's top chip line


# ---------------------------------------------------------------------------
# small drawing helpers
# ---------------------------------------------------------------------------

def figdef(did, parts, k, ink_=TEXT, flip=1):
    B.define(did, B.fig(parts, 0, 0, k, ink_, PANEL, flip=flip))
    return did


def fel(key, parts, x, gy, k, T=None, ink_=TEXT, flip=1, did=None, z=20, dur=0.6,
        group=None):
    """A figure on the bench (svg_figures parts, ground gy), in at T."""
    if did:
        figdef(did, parts, k, ink_, flip)
        svg = B.use(did, x, gy)
    else:
        svg = B.fig(parts, x, gy, k, ink_, PANEL, flip=flip)
    el = add(El(key, "bench", svg, z=z))
    if T is not None:
        el.ev("in", T, dur, group=group)
    return el


def sel(key, svg, T=None, z=22, dur=0.5, group=None, region="bench", how=None, lift=8):
    """A drawn thing (svg) in at T."""
    el = add(El(key, region, svg, z=z))
    if T is not None:
        if how == "lift":
            el.ev("in", T, dur, how="lift", lift=lift, group=group)
        else:
            el.ev("in", T, dur, group=group)
    return el


def clear_mine(T, regions=("bench",), dur=0.8, group="clear"):
    """Everything of this section still on at T in `regions` fades (the
    dock's outlines too when "dock" is named): parts.case_clear."""
    P.case_clear(T, regions=regions, dur=dur, group=group)


def outl(parts, x, gy, k, flip=1):
    return F.outline(parts, x, gy, k, flip=flip)


def outs(keys, T, dur=0.6, group=None):
    """Fade out every key still on at T (parts.outs)."""
    P.outs(keys, T, dur, group)


def dish_svg(x, gy, w=64, fill=FLOUR, heap_h=14, what="flour"):
    """A dish on the ground gy with flour (a heap) or a cake on it (meat on
    a plate is leviticus17_art.meat_svg)."""
    rx = w / 2
    out = (f'<ellipse cx="{f2(x)}" cy="{f2(gy - 5)}" rx="{f2(rx)}" ry="6" '
           f'fill="{rgb(mix(PANEL, SAND, .55))}" stroke="{rgb(TEXT)}" stroke-width="1.3"/>')
    if what == "flour":
        out += ART.heap(x, gy - 8, w * 0.72, heap_h, col=fill)
    elif what == "cake":
        out += (f'<ellipse cx="{f2(x)}" cy="{f2(gy - 11)}" rx="{f2(rx * 0.7)}" ry="6.5" '
                f'fill="{rgb(mix(PANEL, (214, 170, 110), .9))}" stroke="{rgb(TEXT)}" '
                f'stroke-width="1.3"/>')
    return out


def dish_line(x, gy, w=64, h=26):
    return rect_pts(x - w / 2 - 3, gy - h, x + w / 2 + 3, gy + 3)


def half_heap(x, gy, w, h, side):
    """One half of a flour heap (side -1 left, +1 right), as a polygon."""
    pts = ART.heap_pts(x, gy, w, h)
    pts = F.smooth(pts, n=3)
    half = [p for p in pts if (p[0] - x) * side >= -0.01]
    half = [(x, gy)] + half if side > 0 else half + [(x, gy)]
    return (f'<polygon points="{B.pts_str(half)}" fill="{rgb(mix(PANEL, FLOUR, .7))}" '
            f'stroke="{rgb(FLOUR)}" stroke-width="1.4"/>')


def bracket_pts(x0, x1, y, tick=10):
    return [(x0, y + tick), (x0, y), (x1, y), (x1, y + tick)]


def waves(x0, x1, y, amp=3, step=7):
    n = max(2, int((x1 - x0) / step))
    return [(x0 + i * (x1 - x0) / n, y + (amp if i % 2 else -amp)) for i in range(n + 1)]


def tab_pts(off):
    x, y, w, h = D.tab_rect(D.ORDER.index(off))
    return rect_pts(x - 1, y + 1, x + w + 1, y + h + 2)


def fire_pts():
    return rect_pts(P.FIRE_XS[0] - 14, P.A_TOP - 58, P.FIRE_XS[-1] + 10, P.A_TOP + 2)


def strip_court():
    t = S["tent"]
    return rect_pts(t[0] + 2, S["gate"][1] - 30, S["gate"][0], S["gate"][2] + 30)


def tunic_svg(x, y, w=74, h=78):
    """A garment (a tunic laid flat), with blood sprinkled on it."""
    pts = [(x - w * .18, y), (x + w * .18, y), (x + w * .5, y + h * .16),
           (x + w * .42, y + h * .36), (x + w * .28, y + h * .28), (x + w * .3, y + h),
           (x - w * .3, y + h), (x - w * .28, y + h * .28), (x - w * .42, y + h * .36),
           (x - w * .5, y + h * .16)]
    out = (f'<polygon points="{B.pts_str(pts)}" fill="{rgb(mix(PANEL, WHITE_LINEN, .78))}" '
           f'stroke="{rgb(TEXT)}" stroke-width="1.4" stroke-linejoin="round"/>')
    for dx, dy, r in ((-12, 30, 3.4), (6, 40, 2.6), (14, 26, 2.2), (-4, 55, 3.0), (10, 62, 2.0)):
        out += f'<circle cx="{f2(x + dx)}" cy="{f2(y + dy)}" r="{r}" fill="{rgb(BLOOD)}"/>'
    return out


def males(key, T, xs=MALES_X, gy=P.PEN_G, k=MALES_K, group=None):
    """Every male: four priests in a row (one shared drawing). Returns the
    element and the row's outline (for a link pulse)."""
    did = figdef(f"s6_male_{int(k * 100)}", F.priest(), k)
    el = add(El(key, "bench", "".join(B.use(did, x, gy) for x in xs), z=20))
    el.ev("in", T, 0.6, group=group)
    box = rect_pts(xs[0] - 22 * k, gy - 110 * k, xs[-1] + 22 * k, gy + 3)
    return el, box


# ---------------------------------------------------------------------------
# the build
# ---------------------------------------------------------------------------

def build():
    burnt_law()
    meal_law()
    sin_law()
    trespass_law()
    shares()


# ---- 6:9-13: the law of the burnt offering ----------------------------------

DAY_Y = (276, 296)                  # the day strip's bar
DAY_X = (34, 314)
NIGHT_X1 = 236


def burnt_law():
    # ---- 6:9  burnt offering; on the hearth all night; morning; fire ------
    D.switch("burnt", cue(6, 9, "burnt offering"))
    t = cue(6, 9, "burnt offering", 1)
    sel("s6.stack9", P.slab_svg("pieces", P.slot_box(0)) + P.slab_svg("head", P.slot_box(1))
                + P.slab_svg("fat", P.slot_box(2)), t, z=30, dur=0.5, how="lift", lift=10)
    sb0, sb2 = P.slot_box(0), P.slot_box(2)
    P.bench_chip("s6.c.burnt9", "burnt offering", 474, 318, t + 0.1,
                 lead=((sb0[0] + sb2[2]) / 2, sb0[1]), out=cue(6, 10, "linen garment"),
                 group="s6.stack9")
    t = cue(6, 9, "all night")
    y0, y1 = DAY_Y
    moon = B.fig(F.moon(), DAY_X[0] + 22, (y0 + y1) / 2, 0.32, WHITE_LINEN, NIGHT)
    sel("s6.day.night",
        f'<rect x="{DAY_X[0]}" y="{y0}" width="{NIGHT_X1 - DAY_X[0]}" height="{y1 - y0}" rx="5" '
        f'fill="{rgb(NIGHT)}" stroke="{rgb(SAND_DIM)}" stroke-width="1.2"/>' + moon, t, z=18)
    P.bench_chip("s6.c.night", "all night", (DAY_X[0] + NIGHT_X1) / 2 + 10, y1 + 22, t + 0.05,
                 group="s6.day.night")
    t = cue(6, 9, "morning")
    sun = B.fig(F.sun(), NIGHT_X1 + 39, (y0 + y1) / 2, 0.2, GOLD, DAWN)
    sel("s6.day.morn",
        f'<rect x="{NIGHT_X1 + 2}" y="{y0}" width="{DAY_X[1] - NIGHT_X1 - 2}" height="{y1 - y0}" '
        f'rx="5" fill="{rgb(mix(PANEL, DAWN, .55))}" stroke="{rgb(SAND_DIM)}" stroke-width="1.2"/>'
        + sun, t, z=18)
    P.bench_chip("s6.c.morn", "morning", NIGHT_X1 + 39, y1 + 22, t + 0.05, group="s6.day.morn")
    P.flare(cue(6, 9, "kept burning"), 1.3, 1.0)

    # ---- 6:10  the priest in linen; the ashes; beside the altar ----------
    t = cue(6, 10, "linen garment")
    fel("s6.pr.linen", F.priest(), PR_X + 30, PR_G, PR_K, t, ink_=WHITE_LINEN)
    lin = outl(F.priest(), PR_X + 30, PR_G, PR_K)
    P.bench_chip("s6.c.garment", "linen garment", 200, 420, t + 0.1, lead=(PR_X + 46, 450),
                 out=cue(6, 11, "garments"), group="s6.pr.linen")
    P.bench_chip("s6.c.breeches", "linen breeches", 200, 500, cue(6, 10, "linen breeches"),
                 lead=(PR_X + 44, 520), out=cue(6, 10, "ashes"))
    t = cue(6, 10, "ashes")
    hx, hg = 476, P.A_TOP - 24
    ash = sel("s6.ash", ART.heap(hx, hg, 96, 18), t, z=31, dur=0.5)
    P.bench_chip("s6.c.ashes", "ashes", 590, 318, t + 0.1, lead=(hx + 30, hg - 12),
                 group="s6.ash")
    E["s6.stack9"].ev("out", cue(6, 10, "consumed"), 0.8)
    t = cue(6, 10, "beside the altar")
    to = (652 - hx, 556 - hg)
    glide(ash, t, B.arc_path((0, 0), to, 0.2), 0.8, "the ashes beside the altar", "bench move",
          quad=True, group="ashside")
    P.place("ashes", t, group="ashside")
    E["s6.c.ashes"].ev("out", t, 0.5, group="ashside")

    # ---- 6:11  other garments; the ashes carried outside the camp --------
    t = cue(6, 11, "garments")
    E["s6.pr.linen"].ev("out", cue(6, 11, "other garments"), 0.6, group="s6.pr.other")
    fel("s6.pr.other", F.man(), PR_X + 30, PR_G, PR_K, cue(6, 11, "other garments"),
        group="s6.pr.other")
    P.bench_chip("s6.c.other", "other garments", 200, 420, cue(6, 11, "other garments") + 0.1,
                 lead=(PR_X + 46, 450), group="s6.pr.other")
    t = cue(6, 11, "carry")
    ax0, gy = S["ashes"][0] + 16, 131
    tok = add(El("s6.ashman", "strip",
                 P.token(F.man(), ax0, gy, 28, did="s6tok_man")
                 + ART.heap(ax0 + 1, gy - 25, 14, 7), z=32))
    tok.ev("in", t, 0.4, group="ashwalk")
    for k in ("s6.pr.other", "s6.ash", "s6.c.other"):
        E[k].ev("out", t, 0.6, group="ashwalk")
    cx, cy = S["clean"]
    path = [(0, 0), (S["gate_c"][0] - ax0, 0), (cx - 14 - ax0, 0)]
    P.walk(tok, t, path, 2.0, "the ashes out of the camp", group="ashwalk")
    t = cue(6, 11, "outside the camp")
    P.place("camp", t, group="ashwalk")
    D.light("burnt.not_eaten:the ashes: outside the camp", t, group="ashwalk")
    P.place("clean", cue(6, 11, "clean place"), pulse=False)

    # ---- 6:12  kept burning; wood every morning; the burnt offering; fat --
    tok.ev("out", at(6, 12, 0.05), 0.6)
    P.flare(cue(6, 12, "kept burning"), 1.25, 1.0)
    t = cue(6, 12, "wood")
    bars = "".join(B.slab(a, P.A_TOP - 36, b, P.A_TOP - 25, mix(PANEL, GT.ACACIA, .75), GT.ACACIA, 3)
                   for a, b in ((P.WOOD_X[0] + 10, P.WOOD_X[0] + 60), (P.WOOD_X[0] + 64, P.WOOD_X[0] + 114),
                                (P.WOOD_X[0] + 118, P.WOOD_X[0] + 160)))
    sel("s6.wood12", bars, t, z=29, dur=0.4, how="lift", lift=8)
    P.bench_chip("s6.c.wood", "wood", 372, 330, t + 0.1, lead=(P.WOOD_X[0] + 14, P.A_TOP - 30),
                 group="s6.wood12", out=cue(6, 12, "fat"))
    pulse_el("s6.morn.p12", "bench", rect_pts(NIGHT_X1 + 1, DAY_Y[0] - 2, DAY_X[1] + 2, DAY_Y[1] + 2),
             cue(6, 12, "every morning"))
    t = cue(6, 12, "burnt offering")
    ys = (P.A_TOP - 58, P.A_TOP - 37)
    bx = [(410, 452), (458, 500), (506, 548)]
    sel("s6.stack12", P.slab_svg("pieces", (bx[0][0], ys[0], bx[0][1], ys[1]))
        + P.slab_svg("head", (bx[1][0], ys[0], bx[1][1], ys[1])), t, z=30, dur=0.5, how="lift",
        lift=10, group="bo12")
    D.light("burnt.burns:the whole", t + 0.05, group="bo12", steady_out=t + 1.8)
    t = cue(6, 12, "fat")
    sel("s6.fat12", P.slab_svg("fat", (bx[2][0], ys[0], bx[2][1], ys[1])), t, z=30, dur=0.5,
        how="lift", lift=10)
    P.bench_chip("s6.c.peace12", "peace offerings", 548, 300, cue(6, 12, "peace offerings"),
                 lead=(bx[2][0] + 20, ys[0]))

    # ---- 6:13  fire kept burning continually -----------------------------
    P.flare(cue(6, 13, "Fire"), 1.22, 0.9)
    t = cue(6, 13, "continually")
    traced_el("s6.cont", "bench", [(DAY_X[0], DAY_Y[0] - 8), (DAY_X[1], DAY_Y[0] - 8)], FIRE, 4,
              t, 1.0, z=26)
    P.bench_chip("s6.c.cont", "continually", 412, (DAY_Y[0] + DAY_Y[1]) / 2 - 2, t + 0.35,
                 anchor="lm")


# ---- 6:14-23: the law of the meal offering ----------------------------------

SUP_G = 548
BASKET_X, JAR_X, CUP_X = 108, 182, 254
SUP_CHIP_Y = 470


def meal_law():
    # ---- 6:14  meal offering; the sons of Aaron; before the altar --------
    t = cue(6, 14, "meal offering")
    clear_mine(t, ("bench", "strip"), group="sw614")
    D.switch("meal", t, group="sw614")
    fel("s6.pr14", F.priest(), PR_X, PR_G, PR_K, cue(6, 14, "sons of Aaron"), did="s6_priest")
    pr_line = outl(F.priest(), PR_X, PR_G, PR_K)
    t = cue(6, 14, "before the altar")
    P.place("altar", t, group="balt")
    pulse_el("s6.alt.p14", "bench", rect_pts(*P.A_BODY), t, group="balt")

    # ---- 6:15  the handful of flour, oil, frankincense; burned; memorial --
    t = cue(6, 15, "fine flour")
    sel("s6.basket", ART.supply_svg("basket", BASKET_X, SUP_G, 2.2), t, z=20, group="s6.basket")
    P.bench_chip("s6.c.flour", "fine flour", BASKET_X, SUP_CHIP_Y, t + 0.05, group="s6.basket")
    t = cue(6, 15, "oil")
    sel("s6.jar", ART.supply_svg("jar", JAR_X, SUP_G, 2.6), t, z=20, group="s6.jar")
    P.bench_chip("s6.c.oil", "oil", JAR_X, SUP_CHIP_Y, t + 0.05, group="s6.jar")
    t = cue(6, 15, "frankincense")
    sel("s6.cup", ART.supply_svg("cup", CUP_X, SUP_G, 4.2), t, z=20, group="s6.cup")
    P.bench_chip("s6.c.frank", "frankincense", CUP_X, SUP_CHIP_Y, t + 0.05, group="s6.cup")
    t = cue(6, 15, "burn")
    hand = sel("s6.handful", ART.heap(BASKET_X, ART.supply_top("basket", SUP_G, 2.2) - 4, 26, 12,
                                      col=FLOUR), None, z=40)
    hand.ev("in", t, 0.25, group="handful")
    to = (P.FIRE_XS[2] - BASKET_X, (P.A_TOP - 30) - (ART.supply_top("basket", SUP_G, 2.2) - 4))
    glide(hand, t, B.arc_path((0, 0), to, 0.25), 1.1, "the handful to the fire", "bench move",
          quad=True, group="handful")
    P.flare(t + 1.12, 1.3, 0.9, group="handful2")
    hand.ev("out", t + 1.12, 0.5, group="handful2")
    t = cue(6, 15, "memorial")
    P.bench_chip("s6.c.memorial", "memorial", P.FIRE_XS[1] - 4, P.A_TOP - 96, t, anchor="lm",
                 group="mem15", out=at(6, 16, 0.1))
    D.light("meal.burns:a handful", t + 0.05, group="mem15", steady_out=t + 1.0)

    # ---- 6:16  Aaron and his sons eat; without yeast; the court ----------
    t = cue(6, 16, "Aaron and his sons")
    D.light("meal.eaten:the priests|Aaron and his sons", t, link=[("bench", pr_line, True)],
            group="aas16", steady_out=t + 1.6)
    t = cue(6, 16, "yeast")
    bx_, by_ = 600, 312
    sel("s6.bread", ART.bread_svg("leavened", bx_, by_ + 10, 3.4), t, z=22, group="yeast")
    P.bench_chip("s6.c.yeast", "yeast", bx_, 262, t, group="yeast")
    P.not_el("s6.not.yeast", "bench", (bx_, by_ - 2), 30, t + 0.35)
    t = cue(6, 16, "court")
    pulse_el("s6.court.p16", "strip", strip_court(), t, group="court16")
    P.strip_chip("s6.court16", "court", 470, 60, t, group="court16")

    # ---- 6:17  not baked with yeast; most holy, as sin and trespass -------
    outs(["s6.c.flour", "s6.c.oil", "s6.c.frank", "s6.court16"], at(6, 17, 0.1), group="c617")
    pulse_el("s6.not.yeast.p", "bench", B.ring_pts((bx_, by_ - 2), 33), cue(6, 17, "yeast"))
    t = cue(6, 17, "most holy")
    P.bench_chip("s6.c.mh17", "most holy", 172, CHIP_TOP, t)
    traced_el("s6.br17", "bench", bracket_pts(84, 262, CHIP_TOP + 18), TEXT_DIM, 2, t + 0.1, 0.5,
              z=26)
    t = cue(6, 17, "sin offering")
    P.bench_chip("s6.c.sin17", "sin offering", 84, CHIP_TOP + 46, t, group="sin17")
    pulse_el("s6.tab.sin17", "dock", tab_pts("sin"), t, group="sin17")
    t = cue(6, 17, "trespass offering")
    P.bench_chip("s6.c.tr17", "trespass offering", 262, CHIP_TOP + 46, t, group="tr17")
    pulse_el("s6.tab.tr17", "dock", tab_pts("trespass"), t, group="tr17")

    # ---- 6:18-19  every male; forever; holy; (6:19) the case ends ---------
    t = cue(6, 18, "Every male")
    outs(["s6.c.mh17", "s6.br17", "s6.c.sin17", "s6.c.tr17", "s6.bread", "s6.c.yeast",
          "s6.not.yeast"], t, group="m618")
    _m, mbox = males("s6.males18", t, xs=(130, 172, 214, 256), gy=346, k=0.72, group="m618")
    D.light("meal.eaten:the priests|Aaron and his sons", t, link=[("bench", mbox, True)],
            group="m618", steady_out=t + 1.8)
    P.bench_chip("s6.c.forever", "forever", 300, 290, cue(6, 18, "forever"), anchor="lm")
    P.bench_chip("s6.c.holy18", "holy", 300, 325, cue(6, 18, "holy"), anchor="lm")
    clear_mine(at(6, 19, 0.2))

    # ---- 6:20  Aaron's anointing day: a tenth; morning and evening --------
    t = cue(6, 20, "Aaron")
    fel("s6.pr20", F.priest(), PR_X, PR_G, PR_K, t, did="s6_priest")
    pr20_line = outl(F.priest(), PR_X, PR_G, PR_K)
    P.bench_chip("s6.c.anointed", "anointed", PR_X + 12, 378, cue(6, 20, "anointed"),
                 lead=(PR_X, 398))
    t = cue(6, 20, "tenth")
    dx_, dg = 196, 548
    sel("s6.dish20", dish_svg(dx_, dg, 84, what=None), t, z=21, group="tenth")
    hl = sel("s6.halfL", half_heap(dx_, dg - 8, 60, 18, -1), t, z=22, group="tenth")
    hr = sel("s6.halfR", half_heap(dx_, dg - 8, 60, 18, 1), t, z=22, group="tenth")
    P.bench_chip("s6.c.tenth", "one tenth", dx_, 486, t + 0.05, group="tenth")
    mx, ex, my = 150, 270, 330
    t = cue(6, 20, "half")
    sel("s6.dishM", dish_svg(mx, my + 4, 50, what=None), t, z=21, dur=0.4, group="half1")
    glide(hl, t, B.arc_path((0, 0), (mx - dx_ + 15, my - dg + 4), 0.2), 0.6,
          "half to the morning", "bench move", quad=True, group="half1")
    t = cue(6, 20, "morning")
    sel("s6.sun20", B.fig(F.sun(), mx, my - 42, 0.24, GOLD, DAWN), t, z=22, group="morn20")
    P.bench_chip("s6.c.morn20", "morning", mx, CHIP_TOP, t, group="morn20")
    t = cue(6, 20, "half", 1)
    sel("s6.dishE", dish_svg(ex, my + 4, 50, what=None), t, z=21, dur=0.4, group="half2")
    glide(hr, t, B.arc_path((0, 0), (ex - dx_ - 15, my - dg + 4), 0.2), 0.55,
          "half to the evening", "bench move", quad=True, group="half2")
    t = cue(6, 20, "evening")
    sel("s6.moon20", B.fig(F.moon(), ex, my - 42, 0.36, WHITE_LINEN, NIGHT), t, z=22,
        dur=fit(t, 0.5), group="eve20")
    P.bench_chip("s6.c.eve20", "evening", ex, CHIP_TOP, t, dur=fit(t, 0.5), group="eve20")

    # ---- 6:21  with oil on a griddle; soaked; baked pieces to the fire ----
    t = at(6, 21, 0.05)
    outs(["s6.dish20", "s6.dishM", "s6.dishE", "s6.halfL", "s6.halfR", "s6.c.tenth", "s6.sun20",
          "s6.c.morn20",
          "s6.moon20", "s6.c.eve20"], t, group="c621")
    gx = 236
    t = cue(6, 21, "oil")
    sel("s6.jar21", ART.supply_svg("jar", 128, SUP_G, 2.6), t, z=20, group="s6.jar21")
    P.bench_chip("s6.c.oil21", "oil", 128, SUP_CHIP_Y, t + 0.05, group="s6.jar21")
    t = cue(6, 21, "griddle")
    sel("s6.griddle", ART.cookware_svg("griddle", gx, SUP_G, 2.0), t, z=20, group="s6.griddle")
    P.bench_chip("s6.c.griddle", "griddle", gx + 30, 500, t + 0.05, group="s6.griddle")
    t = cue(6, 21, "soaked")
    dough = sel("s6.dough", ART.cookware_svg("griddle", gx, SUP_G, 2.0, "dough"), t, z=21,
                group="s6.dough")
    P.bench_chip("s6.c.soaked", "soaked", gx + 30, 440, t + 0.05, group="s6.dough",
                 out=cue(6, 21, "baked pieces"))
    t = cue(6, 21, "baked pieces")
    py0 = SUP_G - 46
    pcs = sel("s6.pieces", "".join(B.slab(gx - 34 + i * 24, py0, gx - 14 + i * 24, py0 + 11,
                                          mix(PANEL, (196, 140, 80), .9), TEXT, 3)
                                   for i in range(3)), t, z=24, group="pcs")
    dough.ev("out", t, 0.5, group="pcs")
    P.bench_chip("s6.c.pieces", "baked pieces", gx + 30, 440, t + 0.05, group="pcs",
                 out=cue(6, 21, "pleasant aroma"))
    t = cue(6, 21, "pleasant aroma")
    to = (P.FIRE_XS[2] - gx, (P.A_TOP - 34) - (py0 + 5))
    glide(pcs, t, B.arc_path((0, 0), to, 0.22), 0.9, "the baked pieces to the fire", "bench move",
          quad=True, group="pcs2")
    P.flare(t + 0.92, 1.28, 0.6, group="pcs3")
    pcs.ev("out", t + 0.92, 0.5, group="pcs3")

    # ---- 6:22  the anointed priest; his son in his place; wholly burned ---
    outs(["s6.jar21", "s6.c.oil21", "s6.griddle", "s6.c.griddle"], at(6, 22, 0.05), group="c622")
    pulse_el("s6.pr20.p22", "bench", pr20_line, cue(6, 22, "anointed priest"))
    t = cue(6, 22, "his sons")
    son_x = 132
    fel("s6.son22", F.priest(), son_x, PR_G, 1.3, t)
    son_line = outl(F.priest(), son_x, PR_G, 1.3)
    t = cue(6, 22, "wholly burned")
    P.flare(t, 1.3, 0.9, group="wb22")
    P.bench_chip("s6.c.wb22", "wholly burned", P.FIRE_XS[1] - 4, P.A_TOP - 96, t, anchor="lm",
                 group="wb22")
    D.light("meal.burns:all of it", t, link=[("bench", fire_pts(), True)], group="wb22")

    # ---- 6:23-24  every priest's meal offering: wholly burned, not eaten ---
    t = cue(6, 23, "priest")
    cx_, cg = 600, 330
    sel("s6.cake23", dish_svg(cx_, cg, 70, what="cake"), t, z=22, group="cake23")
    pulse_el("s6.son.p23", "bench", son_line, t, group="cake23")
    t = cue(6, 23, "wholly burned")
    P.flare(t, 1.25, 0.9, group="wb23")
    D.light("meal.burns:all of it", t, group="wb23", steady_out=t + 1.2)
    t = cue(6, 23, "not be eaten")
    P.not_el("s6.not.cake", "bench", (cx_, cg - 12), 30, t, dur=0.3)
    land = D.fly("a priest's own", (cx_ - 46, cg - 54), "meal.not_eaten:a priest's own", t)
    assert B.verse_of(land - 0.25 + B.SAY_LEAD + 0.01) == (6, 23), B.local(land)
    clear_mine(max(land + 0.1, at(6, 24, 0.3)))


# ---- 6:24-30: the law of the sin offering -----------------------------------

def sin_law():
    # ---- 6:25  Aaron; sin offering; the north; most holy ------------------
    fel("s6.pr25", F.priest(), PR_X, PR_G, PR_K, cue(6, 25, "Aaron"), did="s6_priest")
    D.switch("sin", cue(6, 25, "sin offering"))
    P.place("north", cue(6, 25, "burnt offering"))
    P.bench_chip("s6.c.mh25", "most holy", 190, CHIP_TOP, cue(6, 25, "most holy"),
                 out=at(6, 26, 0.1))

    # ---- 6:26  the priest eats it; the court ------------------------------
    t = cue(6, 26, "eat")
    mx, mg = 290, 500
    sel("s6.meat26", ART.meat_svg(mx, mg - 15, 52, 18), t, z=22)
    D.fly("the priests", (mx + 2, mg - 40), "sin.eaten:the priests", t + 0.4)
    t = cue(6, 26, "court")
    pulse_el("s6.court.p26", "strip", strip_court(), t, group="court26")
    P.strip_chip("s6.court26", "court", 470, 60, t, group="court26", out=at(6, 27, 0.1))

    # ---- 6:27  touch: holy; blood on a garment; wash ----------------------
    t = cue(6, 27, "touch")
    pulse_el("s6.meat.p27", "bench", dish_line(mx, mg, 76, 30), t)
    P.bench_chip("s6.c.holy27", "holy", mx, 440, cue(6, 27, "holy"))
    t = cue(6, 27, "garment")
    gx, gy = 170, 270
    sel("s6.tunic", tunic_svg(gx, gy), t, z=22)
    P.bench_chip("s6.c.garment27", "garment", gx + 96, 290, t + 0.05, lead=(gx + 36, gy + 16),
                 group="s6.tunic")
    t = cue(6, 27, "wash")
    for i, y in enumerate((gy + 34, gy + 50)):
        traced_el(f"s6.wash27.{i}", "bench", waves(gx - 26, gx + 26, y), WATER, 2.6, t + i * 0.12,
                  0.6, z=28)
    P.bench_chip("s6.c.wash", "wash", gx + 96, 326, t + 0.05)

    # ---- 6:28  the earthen vessel broken; the bronze scoured, rinsed ------
    outs(["s6.meat26", "s6.c.holy27", "s6.tunic", "s6.c.garment27", "s6.wash27.0", "s6.wash27.1",
          "s6.c.wash"], at(6, 28, 0.05), group="c628")
    ex, bx2, vg, vk = 150, 286, 548, 1.8
    t = cue(6, 28, "earthen vessel")
    left, right, crack = F.pot_halves()
    pl = fel("s6.potL", left, ex, vg, vk, t, ink_=ART.CLAY, group="pot")
    pr_ = fel("s6.potR", right, ex, vg, vk, t, ink_=ART.CLAY, group="pot")
    P.bench_chip("s6.c.earthen", "earthen vessel", ex, 446, t + 0.05, group="pot",
                 out=cue(6, 28, "broken"))
    t = cue(6, 28, "broken")
    traced_el("s6.crack", "bench", [(ex + x * vk, vg - y * vk) for x, y in crack], TEXT, 2, t, 0.4,
              z=26)
    pl.ev("move", t + 0.4, 0.5, path=[(0, 0), (-7, 2)], group="crack")
    pr_.ev("move", t + 0.4, 0.5, path=[(0, 0), (7, 2)], group="crack")
    E["s6.crack"].ev("out", t + 0.4, 0.3, group="crack")
    P.bench_chip("s6.c.broken", "broken", ex, 446, t + 0.05, how="lift")
    t = cue(6, 28, "bronze vessel")
    sel("s6.bronze", ART.cookware_svg("bronze", bx2, vg, vk), t, z=20, group="s6.bronze")
    P.bench_chip("s6.c.bronze", "bronze vessel", bx2, 446, t + 0.05, group="s6.bronze",
                 out=cue(6, 28, "rinsed"))
    t = cue(6, 28, "scoured")
    for i in range(3):
        traced_el(f"s6.scour.{i}", "bench",
                  [(bx2 - 22 + i * 14, vg - 52), (bx2 - 10 + i * 14, vg - 22)], WHITE_LINEN, 2.2,
                  t + i * 0.1, 0.35, z=28)
    P.bench_chip("s6.c.scoured", "scoured", bx2, 412, t + 0.05)
    t = cue(6, 28, "rinsed")
    for i, y in enumerate((vg - 66, vg - 76)):
        traced_el(f"s6.rinse.{i}", "bench", waves(bx2 - 26, bx2 + 26, y), WATER, 2.6, t + i * 0.12,
                  0.5, z=28)
    P.bench_chip("s6.c.rinsed", "rinsed", bx2, 446, t + 0.05, how="lift")

    # ---- 6:29  every male among the priests; most holy -------------------
    t = cue(6, 29, "Every male")
    outs(["s6.potL", "s6.potR", "s6.c.broken", "s6.bronze", "s6.c.scoured", "s6.c.rinsed",
          "s6.scour.0", "s6.scour.1", "s6.scour.2", "s6.rinse.0", "s6.rinse.1"], t, group="m629")
    _m, mbox = males("s6.males29", t, group="m629")
    D.light("sin.eaten:the priests", t, link=[("bench", mbox, True)], group="m629",
            steady_out=t + 1.6)
    P.bench_chip("s6.c.mh29", "most holy", 190, CHIP_TOP, cue(6, 29, "most holy"))

    # ---- 6:30  blood into the Tent, the Holy Place: not eaten; burned -----
    t = at(6, 30, 0.05)
    outs(["s6.males29", "s6.c.mh29"], t, group="c630")
    t = cue(6, 30, "sin offering")
    sel("s6.meat30", ART.meat_svg(290, 500 - 15, 52, 18), t, z=22)
    t = cue(6, 30, "Tent of Meeting")
    a = S["altar"]
    dx, dy = S["door"]
    traced_el("s6.bpath1", "strip", [(a[0], a[3] - 4), (a[0] - 12, 142), (dx + 12, 142),
                                     (dx, dy)], BLOOD, 3, t, 0.9, z=36)
    t = cue(6, 30, "Holy Place")
    # into the Holy Place, to the altar of incense (whose horns 4:7 and 4:18 touch)
    ix, iy = S["incense"]
    traced_el("s6.bpath2", "strip", [(dx, dy), (ix + 30, dy), (ix + 7, iy + 3)], BLOOD, 3, t, 0.6,
              z=36)
    P.strip_chip("s6.holyplace", "Holy Place", 88, 106, t + 0.05)
    t = cue(6, 30, "eaten")
    P.not_el("s6.not.meat", "bench", (290, 486), 34, t)
    t = cue(6, 30, "burned")
    P.flare(t, 1.3, 0.8, group="burn30")
    D.light("sin.not_eaten:blood in the Tent: burned", t, link=[("bench", fire_pts(), True)],
            group="burn30")


# ---- 7:1-7: the law of the trespass offering ---------------------------------

def trespass_law():
    # ---- 7:1  trespass offering; the ram; most holy ------------------------
    t = cue(7, 1, "trespass offering")
    clear_mine(t, ("bench", "strip"), group="sw71")
    D.switch("trespass", t, group="sw71")
    ram = P.Beast("ram", P.RAM_X, P.PEN_G, P.RAM_K)
    fel("s6.ram", F.sheep(ram=True), P.RAM_X, P.PEN_G, P.RAM_K, t, group="sw71")
    ram_line = F.outline(F.sheep(ram=True), P.RAM_X, P.PEN_G, P.RAM_K)
    t_mh = cue(7, 1, "most holy")
    D.light("trespass.thing:ram", t + 0.62, link=[("bench", ram_line, True)], group="ram71",
            steady_out=t_mh)
    P.bench_chip("s6.c.mh71", "most holy", 300, CHIP_TOP + 10, t_mh, group="ram71:out",
                 out=at(7, 2, 0.1))

    # ---- 7:2  where the burnt offering is killed; the ring ----------------
    t = cue(7, 2, "burnt offering")
    P.place("north", t, group="north72")
    pulse_el("s6.ram.north", "bench", ram_line, t, group="north72")
    a = S["altar"]
    t = cue(7, 2, "around")
    ring = traced_el("s6.ring72", "strip", rect_pts(a[0] - 4, a[1] - 4, a[2] + 4, a[3] + 4), BLOOD,
                     2.4, t, 0.7, z=35, closed=True)
    D.light("trespass.blood:around the altar", t, group="s6.ring72")
    ring.ev("out", at(7, 3, 0.05), 0.6)

    # ---- 7:3  all its fat: the fat tail, the fat that covers ---------------
    t = cue(7, 3, "fat")
    E["s6.ram"].ev("out", t, 0.6, group="cut73")
    P.cutaway(ram, "s6ram", t, group="cut73")
    band, bxs = P.CHIP_BAND_Y, P.CHIP_BAND_X
    t = cue(7, 3, "fat tail")
    P.part_pulse(ram, "s6ram", "tail_fat", t, group="ft73")
    P.bench_chip("s6.c.tail", "fat tail", bxs[0], band, t, lead=ram.anchor["tail_fat"],
                 group="ft73", out=at(7, 4, 0.05))
    t = cue(7, 3, "covers")
    P.part_pulse(ram, "s6ram", "fat_cover", t, group="fc73")
    P.bench_chip("s6.c.cover", "fat that covers", 210, band, t, lead=ram.anchor["fat_cover"],
                 group="fc73", out=at(7, 4, 0.05))

    # ---- 7:4  the kidneys, the fat by the loins, the cover on the liver ----
    t = cue(7, 4, "kidneys")
    P.part_pulse(ram, "s6ram", "kidneys", t, group="kd74")
    P.bench_chip("s6.c.kidneys", "kidneys", 62, band, t, lead=ram.anchor["kidneys"],
                 group="kd74")
    t = cue(7, 4, "loins")
    P.part_pulse(ram, "s6ram", "kidney_fat", t, group="ln74")
    P.bench_chip("s6.c.loins", "fat by the loins", 186, band, t, lead=ram.anchor["kidney_fat"],
                 group="ln74")
    t = cue(7, 4, "liver")
    P.part_pulse(ram, "s6ram", "liver_cover", t, group="lv74")
    P.bench_chip("s6.c.liver", "cover on the liver", 322, band, t,
                 lead=ram.anchor["liver_cover"], group="lv74")

    # ---- 7:5  the priest burns them: the fat to the wood; the fire ---------
    t = cue(7, 5, "burn")
    outs(["s6.c.kidneys", "s6.c.loins", "s6.c.liver"], t, group="wood.s6ram")
    P.to_wood(ram, "s6ram", {"tail_fat": ram.anchor["tail_fat"], "fat": ram.anchor["fat"],
                             "kidneys": ram.anchor["kidneys"]}, t, ["tail_fat", "fat", "kidneys"])
    P.flare(t + 1.14, 1.3, 0.75, group="burn75")
    D.fly("the fat", (P.FIRE_XS[1] - 4, P.A_TOP - 96), "trespass.burns:the fat", t + 1.92)

    # ---- 7:6  every male among the priests; most holy -----------------------
    t = cue(7, 6, "Every male")
    clear_mine(t, group="m76")
    _m, mbox = males("s6.males76", t, group="m76")
    D.fly("the priests", (MALES_X[-1] + 20, P.PEN_G - 112), "trespass.eaten:the priests",
          cue(7, 6, "priests"))
    P.bench_chip("s6.c.mh76", "most holy", 190, CHIP_TOP, cue(7, 6, "most holy"))

    # ---- 7:7  as the sin offering, so the trespass: one law; the priest -----
    t = at(7, 7, 0.05)
    outs(["s6.males76", "s6.c.mh76"], t, group="c77")
    t = cue(7, 7, "sin offering")
    P.bench_chip("s6.c.sin77", "sin offering", 110, 300, t, group="sin77")
    pulse_el("s6.tab.sin77", "dock", tab_pts("sin"), t, group="sin77")
    t = cue(7, 7, "trespass offering")
    P.bench_chip("s6.c.tr77", "trespass offering", 280, 300, t, group="tr77")
    pulse_el("s6.tab.tr77", "dock", tab_pts("trespass"), t, group="tr77")
    t = cue(7, 7, "one law")
    traced_el("s6.br77", "bench", [(110, 322), (110, 334), (280, 334), (280, 322)], TEXT_DIM, 2, t,
              0.5, z=26)
    P.bench_chip("s6.c.onelaw", "one law", 195, 358, t + 0.1)
    t = cue(7, 7, "priest")
    fel("s6.pr77", F.priest(), PR_X, PR_G, PR_K, t, did="s6_priest", group="pr77")
    D.light("trespass.eaten:the priests", t, link=[("bench", outl(F.priest(), PR_X, PR_G, PR_K),
                                                    True)], group="pr77")


# ---- 7:8-10: the priests' shares (left of the altar, which stays) ------------

ROW_G = (342, 452, 562)              # each row's ground
RCV_X = 322                          # the receiving priest (clear of the altar's poles)


def shares():
    # ---- 7:8  the priest; burnt offering; the skin ------------------------
    t = at(7, 8, 0.05)
    clear_mine(t, group="set78")
    pk = 0.82
    t = cue(7, 8, "priest")
    fel("s6.rcv1", F.priest(), RCV_X, ROW_G[0], pk, t, did="s6_rcv")
    t = cue(7, 8, "burnt offering")
    D.switch("burnt", t, group="sw78")
    ox_x, ox_k = 150, 0.86
    fel("s6.ox78", F.ox(), ox_x, ROW_G[0], ox_k, t, group="sw78")
    bull = P.Beast("bull", ox_x, ROW_G[0], ox_k)
    t = cue(7, 8, "skin")
    hide = bull.outline("skin")[0][0]
    traced_el("s6.skin78", "bench", hide, (214, 170, 110), 3, t, 0.5, z=26, closed=True)
    sel("s6.hide78", f'<polygon points="{B.pts_str(hide)}" fill="{rgb((214, 170, 110))}" '
        f'fill-opacity="0.45"/>', t, z=25, group="s6.skin78")
    P.bench_chip("s6.c.skin78", "skin", ox_x - 104, ROW_G[0] - 50, t, lead=bull.anchor["skin"],
                 group="s6.skin78")
    P.arrow_el("s6.ar78", [(ox_x + 72, ROW_G[0] - 40), (RCV_X - 22, ROW_G[0] - 40)], t, 0.5)
    D.fly("the skin", (RCV_X + 22, ROW_G[0] - 50), "burnt.not_eaten:the skin: the priest's",
          t + 0.52)

    # ---- 7:9  meal offering: baked in the oven, the pan, the griddle -------
    t = cue(7, 9, "meal offering")
    D.switch("meal", t, group="sw79")
    g2 = ROW_G[1]
    for key, kind, x, word, k in (("oven", "oven", 50, "oven", 1.2), ("pan", "pan", 126, "pan", 1.2),
                                  ("griddle", "griddle", 230, "griddle", 1.2)):
        t = cue(7, 9, word)
        sel(f"s6.{key}79", ART.cookware_svg(kind, x, g2, k), t, z=20, group=f"s6.{key}79")
        P.bench_chip(f"s6.c.{key}79", word, x + (14 if kind == "pan" else 0), g2 - 78, t + 0.05,
                     group=f"s6.{key}79")
    t = cue(7, 9, "priest's")
    P.arrow_el("s6.ar79", [(272, g2 - 22), (RCV_X - 22, g2 - 22)], t, 0.4)
    fel("s6.rcv2", F.priest(), RCV_X, g2, pk, t, did="s6_rcv", group="s6.ar79")
    D.light("meal.eaten:the priest", t, link=[("bench", outl(F.priest(), RCV_X, g2, pk), True)],
            group="s6.ar79")

    # ---- 7:10  mixed with oil, or dry: to all the sons of Aaron ------------
    g3 = ROW_G[2]
    outs(["s6.c.skin78", "s6.c.oven79", "s6.c.pan79", "s6.c.griddle79"], at(7, 10, 0.05),
         group="c710")
    t = cue(7, 10, "mixed with oil")
    sel("s6.mixed", dish_svg(74, g3, 70, fill=OIL, what="flour"), t, z=22)
    P.bench_chip("s6.c.mixed", "mixed with oil", 74, g3 - 46, t + 0.05, group="s6.mixed")
    t = cue(7, 10, "dry")
    sel("s6.dry", dish_svg(166, g3, 70, what="flour"), t, z=22)
    P.bench_chip("s6.c.dry", "dry", 166, g3 - 46, t + 0.05, group="s6.dry")
    t = cue(7, 10, "sons of Aaron")
    xs = (254, 290, 326, 362)
    males("s6.sons710", t, xs=xs, gy=g3, k=0.74, group="sons")
    P.arrow_el("s6.ar710", [(206, g3 - 24), (xs[0] - 22, g3 - 24)], t, 0.4)
    land = D.fly("the priests", (xs[0] - 20, g3 - 96), "meal.eaten:the priests|all the sons of Aaron",
                 t + 0.42)
    # the board clears (the altar set stays): the s6|s7 boundary
    t = land + 0.05
    clear_mine(t, ("strip", "bench", "dock"), dur=0.6, group="set710")
