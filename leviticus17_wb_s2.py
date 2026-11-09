"""Leviticus 2:1-16, the meal offering, on the workbench (section s2).

Starts on the s1|s2 boundary (the places of Lev 1, the altar set, the burnt
column lit under the burnt tab) and leaves the s2|s3 boundary (the same
places, the altar set at rest, the meal column lit under the meal tab); the
meal column is filed at the end of 2:16 and the file view holds across the
2:16|3:1 seam, gone by 3:1 t = 1.5 s (bench.SEAM_RESERVE).

The bench's sets (in the pen half, x 8-338, with the altar on the right):

- the meal set (2:1-3): the jar of oil, the basket of fine flour, the cup of
  frankincense (leviticus17_art.supply_svg), the cupped hand with its
  handful (leviticus17_art.hand_svg), and over the
  altar the split bar: the memorial end over the fire, the rest "Aaron and
  his sons";
- the kitchen set (2:4-10): oven, griddle and pan (leviticus17_art.cookware_svg),
  the unleavened cakes and wafers (leviticus17_art.bread_svg);
- the rules set (2:11-13): yeast and honey under not-marks (svg_vocab), the
  first fruits, the struck way to the altar, the salt and the covenant;
- the first fruits set (2:14-16): the ears (svg_figures.grass), parched,
  bruised, oil and frankincense, and the part burned.

Cases (leviticus17_spec.CASES 2:1, 2:4, 2:11, 2:14) each clear the bench;
the current case's icons carry the dock's case outline.

Moves (QC's budget): no camera; chip flights at 2:2 ("a handful"), 2:3
("Aaron and his sons") and 2:16 ("part of it"); bench moves at 2:2 (the
handful to the fire), 2:9 (the memorial cake) and 2:16 (the part); a token
walk at 2:8 (the meal offering to the priest); the filing glide at 2:16.
"""

import svg_figures as F
import leviticus17_bench as B
import leviticus17_dock as D
import leviticus17_parts as P
import leviticus17_art as ART
from generate_tabernacle import BG, GOLD, PANEL, SAND, TEXT, TEXT_DIM
from leviticus17_bench import El, add, cue, at, fit, pulse_el, traced_el, glide, rect_pts
from leviticus17_parts import S
from svg_vocab import mix

STUB = False
VERSES = [(2, v) for v in range(1, 17)]

REACH = {}
EXCUSED = {}

OIL = ART.OIL
FLOUR = ART.FLOUR
CLAY = ART.CLAY
CHIP = 14
E = B.ELS

# -- the meal set (pen half) ---------------------------------------------------
GS = 440                                    # the supplies' ground
JAR_X, JAR_K = 58, 2.6
BASKET_X, BASKET_K = 168, 3.0
CUP_X, CUP_K = 284, 4.4
SUP_CHIP_Y = GS + 20
WRIST, HAND_K = (226, 328), 3.8          # the cupped hand, palm up, reaching in from the right
# -- the split bar, over the altar --------------------------------------------
BAR_Y0, BAR_Y1 = 258, 292
BAR_X0, BAR_MEM, BAR_X1 = 362, 452, 662
# -- the kitchen set ----------------------------------------------------------
KG = 448
OVEN_X, OVEN_K = 62, 1.8
GRID_X, GRID_K = 172, 1.7
PAN_X, PAN_K = 266, 1.4
K_CHIP_Y = KG + 20
CAKE_XS, CAKE_G, CAKE_K = (42, 92, 142), 334, 2.8
CAKE_CHIP_Y = 290
WAFER_X, WAFER_Y, WAFER_K = 262, 328, 3.2
# -- the rules set --------------------------------------------------------------
YEAST = (70, 312)
HONEY_X, HONEY_G, HONEY_K = 70, 420, 2.0
BRACE_X = 160
SALT_X, SALT_G, SALT_K = 250, 524, 4.0
FF_CHIP = (262, 290)
# -- the first fruits set -----------------------------------------------------
EARS_XS, EARS_G, EARS_K = (112, 158, 204), 446, 5.0
FLAME_G = 480                               # the flames' foot: their tips touch the ears
CRUSH = (272, 452)
FCUP_X, FCUP_G, FCUP_K = 300, 410, 4.0
# -- where things land on the altar's wood -------------------------------------
ON_WOOD = (470, 376)
FLY_SRC = (500, 300)                        # a chip that flies off the fire
MEM_CHIP = (430, 318)                       # "memorial" by the fire


# ---------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------

def thing(key, svg, T=None, dur=0.5, group=None, z=20, how=None, lift=10, region="bench",
          texts=()):
    """A drawing on the bench (or strip), in at T."""
    el = add(El(key, region, svg, z=z, hidden0=T is None, texts=list(texts)))
    if T is not None:
        kw = dict(how="lift", lift=lift) if how == "lift" else {}
        el.ev("in", T, fit(T, dur), group=group, **kw)
    return el


def chip(key, s, x, y, T, lead=None, group=None, anchor="mm", dur=0.5):
    """A 14 px bench chip on a leader, in at T."""
    return P.bench_chip(key, s, x, y, T, lead=lead, anchor=anchor, dur=dur, group=group)


def out(keys, T, group, dur=0.5):
    P.outs(keys, T, dur, group)


def fig_svg(parts, x, gy, k, ink_):
    return B.fig(parts, x, gy, k, ink_, PANEL)


def ellipse(cx, cy, rx, ry, fill, stroke=None, op=1.0, sw=1.2):
    st = f' stroke="{B.rgb(stroke)}" stroke-width="{sw}"' if stroke else ""
    fo = f' fill-opacity="{op}"' if op < 1 else ""
    return (f'<ellipse cx="{B.f2(cx)}" cy="{B.f2(cy)}" rx="{B.f2(rx)}" ry="{B.f2(ry)}" '
            f'fill="{B.rgb(fill)}"{fo}{st}/>')


def move_together(keys, T, rel, dur, what, group, bow=0.3):
    """Several elements glide as one thing (one bench move)."""
    path = B.arc_path((0, 0), rel, bow)
    L = 0
    for k in keys:
        L = glide(E[k], T, path, dur, "", "", quad=True, record=False, group=group)
    B.travel(T, what, L, dur, "bench move", keys=list(keys), group=group)
    return T + dur


def burn_on_wood(keys, land, group):
    """What landed on the wood burns: it fades as the fire flares."""
    out(keys, land, group, dur=0.6)
    P.flare(land, 1.3, fit(land, 0.8), group=group)


# ---------------------------------------------------------------------------
# the build
# ---------------------------------------------------------------------------

def build():
    road = S["road_y"]
    a = S["altar"]

    # ======================================================================
    # 2:1  meal offering; anyone; fine flour, oil, frankincense
    # ======================================================================
    t = cue(2, 1, "meal offering")
    t_named = D.switch("meal", t)                    # burnt steps back; meal is named
    D.light("meal.by", t_named + 0.15)               # "anyone" (said at 0.56)

    b_top = ART.supply_top("basket", GS, BASKET_K)
    flour_y = b_top + 7
    j_top = ART.supply_top("jar", GS, JAR_K)

    t = cue(2, 1, "fine flour")
    thing("s2.basket", ART.supply_svg("basket", BASKET_X, GS, BASKET_K), t, group="s2.flour")
    chip("s2.c.flour", "fine flour", BASKET_X, SUP_CHIP_Y, t, group="s2.flour")
    basket_line = ART.supply_outline("basket", BASKET_X, GS, BASKET_K)
    D.light("meal.thing:fine flour", t, link=[("bench", basket_line, True)], group="s2.flour")

    t = cue(2, 1, "oil")
    mouth = (JAR_X + 2, j_top - 2)
    pour = F.smooth([mouth, (JAR_X + 22, mouth[1] - 30), (JAR_X + 62, mouth[1] - 40),
                     (BASKET_X - 30, flour_y - 18), (BASKET_X - 14, flour_y - 10)],
                    closed=False, n=4)
    thing("s2.jar", ART.supply_svg("jar", JAR_X, GS, JAR_K), t, group="s2.oil")
    chip("s2.c.oil", "oil", JAR_X, SUP_CHIP_Y, t, group="s2.oil")
    jar_line = ART.supply_outline("jar", JAR_X, GS, JAR_K)
    D.light("meal.thing:oil", t, link=[("bench", jar_line, True)], group="s2.oil")
    # "pour oil on it": the stream traced, then the oil on the flour
    traced_el("s2.pour", "bench", pour, OIL, 4.5, t + 0.25, 0.6, z=22, group="s2.oil")
    thing("s2.pour.on", ellipse(BASKET_X - 6, flour_y - 8, 20, 5, OIL, op=0.9), t + 0.7, dur=0.3,
          group="s2.oil", z=22)

    t = cue(2, 1, "frankincense")
    thing("s2.cup", ART.supply_svg("cup", CUP_X, GS, CUP_K), t, group="s2.frank")
    chip("s2.c.frank", "frankincense", CUP_X - 2, SUP_CHIP_Y, t, group="s2.frank")
    cup_line = ART.supply_outline("cup", CUP_X, GS, CUP_K)
    D.light("meal.thing:frankincense", t, link=[("bench", cup_line, True)], group="s2.frank")
    case1 = D.case_outline(["meal.thing:fine flour", "meal.thing:oil",
                            "meal.thing:frankincense"], t + 0.6)

    # ======================================================================
    # 2:2  Aaron's sons; handful of flour, oil, frankincense; burn; memorial
    # ======================================================================
    P.priests_el("s2.priests", [a[0] - 14, a[0] + 8], cue(2, 2, "Aaron's"))

    t = cue(2, 2, "handful")
    hand = ART.hand_svg("cup", WRIST, 0, HAND_K, flip=-1, arm=16)
    palm = _palm()
    thing("s2.hand", hand, t, dur=0.5, group="s2.hand", z=40, how="lift", lift=-14)
    hx, hy = palm
    thing("s2.hf", ART.heap(hx, hy, 36, 14, FLOUR), t + 0.35, dur=0.35, group="s2.hand", z=42)
    chip("s2.c.handful", "handful", 66, 300, t + 0.35, lead=(hx - 14, hy - 6), group="s2.hand")
    t = cue(2, 2, "fine flour")
    pulse_el("s2.basket.p2", "bench", basket_line, t, group="s2.p2flour")
    t = cue(2, 2, "oil")
    thing("s2.hf.oil", ellipse(hx + 1, hy - 9, 9, 3, OIL), t, dur=0.4, group="s2.p2oil", z=43)
    pulse_el("s2.jar.p2", "bench", jar_line, t, group="s2.p2oil")
    t = cue(2, 2, "frankincense")
    thing("s2.hf.frank", ellipse(hx + 7, hy - 12, 5, 3, (246, 242, 230), TEXT_DIM, sw=0.9)
          + ellipse(hx - 4, hy - 12, 4, 2.5, (246, 242, 230), TEXT_DIM, sw=0.9),
          t, dur=0.4, group="s2.p2frank", z=44)
    pulse_el("s2.cup.p2", "bench", cup_line, t, group="s2.p2frank")

    t = cue(2, 2, "burn")
    hf = ["s2.hf", "s2.hf.oil", "s2.hf.frank"]
    out(["s2.hand", "s2.c.handful"], t, "s2.burn2")
    land = move_together(hf, t, (ON_WOOD[0] - hx, ON_WOOD[1] - hy), 1.0,
                         "the handful to the fire", "s2.burn2")
    chip("s2.c.mem2", "memorial", *MEM_CHIP, cue(2, 2, "memorial"),
         lead=(ON_WOOD[0] - 6, ON_WOOD[1] - 10), group="s2.burn2")
    burn_on_wood(hf, land, "s2.fire2")
    P.place("altar", cue(2, 2, "altar"), group="s2.fire2")
    t_up = land + 0.5                    # its glide starts as the flare ends
    land = D.fly("a handful", FLY_SRC, "meal.burns:a handful", t_up)
    out(["s2.c.mem2"], land + 0.35, "s2.mem2out")

    # ======================================================================
    # 2:3  that which is left: Aaron's and his sons'; most holy
    # ======================================================================
    t = cue(2, 3, "left")
    mid_y = (BAR_Y0 + BAR_Y1) / 2
    mx = (BAR_X0 + BAR_MEM) / 2
    frame = (f'<rect x="{BAR_X0}" y="{BAR_Y0}" width="{BAR_X1 - BAR_X0}" '
             f'height="{BAR_Y1 - BAR_Y0}" rx="4" fill="none" stroke="{B.rgb(SAND)}" '
             f'stroke-width="1.6" stroke-dasharray="7 5"/>')
    mem = (f'<rect x="{BAR_X0}" y="{BAR_Y0}" width="{BAR_MEM - BAR_X0}" '
           f'height="{BAR_Y1 - BAR_Y0}" rx="4" fill="{B.rgb(mix(PANEL, FLOUR, .35))}" '
           f'stroke="{B.rgb(FLOUR)}" stroke-width="1.4" stroke-dasharray="5 4"/>'
           + B.text("memorial", mx, mid_y, CHIP, TEXT))
    thing("s2.bar", frame + mem, t, dur=0.6, group="s2.bar", z=30,
          texts=[(B.tbox("memorial", mx, mid_y, CHIP), CHIP, "bar label")])
    t = cue(2, 3, "Aaron's")
    rx_ = (BAR_MEM + BAR_X1) / 2
    word = "Aaron and his sons"
    rest = (f'<rect x="{BAR_MEM + 3}" y="{BAR_Y0}" width="{BAR_X1 - BAR_MEM - 3}" '
            f'height="{BAR_Y1 - BAR_Y0}" rx="4" fill="{B.rgb(mix(PANEL, SAND, .85))}" '
            f'stroke="{B.rgb(SAND)}" stroke-width="1.4"/>' + B.text(word, rx_, mid_y, CHIP, BG))
    thing("s2.rest", rest, t, dur=0.5, group="s2.rest", z=31,
          texts=[(B.tbox(word, rx_, mid_y, CHIP), CHIP, "bar label")])
    wb = B.tbox(word, rx_, mid_y, CHIP)
    land = D.fly(word, (wb[0], mid_y), "meal.eaten:the priests|Aaron and his sons", t + 0.55)
    t = cue(2, 3, "most holy")
    assert t >= land, (B.local(t), B.local(land))
    chip("s2.c.holy3", "most holy", rx_, BAR_Y1 + 24, t, lead=(rx_, BAR_Y1 + 2),
         group="s2.holy3")

    # ======================================================================
    # 2:4  case: baked in the oven; unleavened cakes, unleavened wafers
    # ======================================================================
    t = at(2, 4, 0.2)
    P.case_clear(t, regions=("bench", "strip"), group="s2.clear4")
    case1.ev("out", t, 0.35, group="s2.clear4")

    t = cue(2, 4, "oven")
    thing("s2.oven", ART.cookware_svg("oven", OVEN_X, KG, OVEN_K, "bread"), t, dur=0.6,
          group="s2.oven",
          how="lift", lift=12)
    chip("s2.c.oven", "oven", OVEN_X, K_CHIP_Y, t, group="s2.oven")

    t = cue(2, 4, "unleavened cakes")
    for i, x in enumerate(CAKE_XS):
        thing(f"s2.cake{i}", ART.bread_svg("loaf", x, CAKE_G, CAKE_K), t + i * 0.12, dur=0.4,
              group="s2.cakes", how="lift", lift=6, z=22)
    chip("s2.c.cakes", "unleavened cakes", CAKE_XS[1], CAKE_CHIP_Y, t, group="s2.cakes")
    cakes_pts = rect_pts(CAKE_XS[0] - 27, CAKE_G - 24, CAKE_XS[2] + 27, CAKE_G + 4)
    D.light("meal.thing:cakes", t, link=[("bench", cakes_pts, True)], group="s2.cakes")

    t = cue(2, 4, "unleavened wafers")
    thing("s2.wafers", ART.bread_svg("wafers", WAFER_X, WAFER_Y + 4, WAFER_K), t, dur=0.5,
          group="s2.wafers", how="lift", lift=6, z=22)
    chip("s2.c.wafers", "unleavened wafers", WAFER_X, CAKE_CHIP_Y, t, group="s2.wafers")
    wafer_pts = rect_pts(WAFER_X - 40, WAFER_Y - 27, WAFER_X + 52, WAFER_Y + 9)
    D.light("meal.thing:wafers", t, link=[("bench", wafer_pts, True)], group="s2.wafers")
    case2 = D.case_outline(["meal.thing:cakes", "meal.thing:wafers"], t + 0.6)

    # ======================================================================
    # 2:5  a griddle; mixed with oil
    # ======================================================================
    t = cue(2, 5, "griddle")
    thing("s2.grid", ART.cookware_svg("griddle", GRID_X, KG, GRID_K, "bread"), t, dur=0.6,
          group="s2.grid",
          how="lift", lift=12)
    chip("s2.c.grid", "griddle", GRID_X, K_CHIP_Y, t, group="s2.grid")
    out(["s2.c.cakes", "s2.c.wafers"], t, "s2.grid")
    g_cake_y = KG - 18.4 * GRID_K
    t = cue(2, 5, "mixed with oil")
    chip("s2.c.mixed", "mixed with oil", GRID_X, 384, t, lead=(GRID_X + 10, g_cake_y - 3),
         group="s2.mixed")

    # ======================================================================
    # 2:6  cut in pieces; pour oil on it
    # ======================================================================
    t = cue(2, 6, "pieces")
    out(["s2.c.mixed"], t, "s2.pieces")
    for i, dx in enumerate((-14, 0, 14)):
        traced_el(f"s2.cut{i}", "bench", [(GRID_X + dx - 4, g_cake_y - 6),
                                          (GRID_X + dx + 4, g_cake_y + 5)],
                  BG, 2.6, t + i * 0.15, 0.3, z=30)
    chip("s2.c.pieces", "pieces", GRID_X, 384, t, lead=(GRID_X, g_cake_y - 6), group="s2.pieces")
    t = cue(2, 6, "oil")
    oil6 = F.smooth([(GRID_X - 24, g_cake_y - 5), (GRID_X - 8, g_cake_y - 10),
                     (GRID_X + 8, g_cake_y - 3), (GRID_X + 24, g_cake_y - 8)], closed=False, n=4)
    traced_el("s2.oil6", "bench", oil6, OIL, 4.0, t, 0.7, z=31)

    # ======================================================================
    # 2:7  of the pan; fine flour with oil
    # ======================================================================
    t = cue(2, 7, "pan")
    thing("s2.pan", ART.cookware_svg("pan", PAN_X, KG, PAN_K, "bread"), t, dur=0.6,
          group="s2.pan",
          how="lift", lift=12)
    chip("s2.c.pan", "pan", PAN_X + 10, K_CHIP_Y, t, group="s2.pan")
    out(["s2.c.pieces"], t, "s2.pan")
    D.pulse("meal.thing:fine flour", cue(2, 7, "fine flour"))

    # ======================================================================
    # 2:8  brought, presented to the priest, brought to the altar (strip)
    # ======================================================================
    ox_ = 504
    t = cue(2, 8, "bring")
    off = add(El("s2.offerer", "strip", P.token(F.man(), ox_, road, 30), z=30))
    off.ev("in", t, 0.6)
    bx_, by_ = ox_ + 15, road - 15
    bread_svg = P.token(F.bread(), bx_, by_ + 3, 8)
    br = add(El("s2.bread", "strip", bread_svg, z=32))
    t = cue(2, 8, "meal offering")
    br.ev("in", t, 0.5, group="s2.mo8")
    P.strip_chip("s2.c.mo8", "meal offering", ox_ + 2, road - 46, t, group="s2.mo8")
    t = cue(2, 8, "priest")
    px_ = a[0] + 8
    pr = add(El("s2.priest8", "strip", P.token(F.priest(), px_, road, 30, did="tok_priest"),
                z=30))
    pr.ev("in", t, 0.6, group="s2.present")
    E["s2.c.mo8"].ev("out", t, 0.4, group="s2.present")
    P.walk(br, t, [(0, 0), (px_ + 13 - bx_, 0)], 1.5, "the meal offering to the priest",
           group="s2.present")

    # ======================================================================
    # 2:9  its memorial; burned on the altar
    # ======================================================================
    t = cue(2, 9, "priest")
    off.ev("out", t, 0.6, group="s2.off9")
    t = cue(2, 9, "memorial")
    cx2 = CAKE_XS[2]
    cake2_line = ART.bread_outline("loaf", cx2, CAKE_G, CAKE_K)
    pulse_el("s2.cake2.p9", "bench", cake2_line, t, group="s2.mem9")
    chip("s2.c.mem9", "memorial", cx2 + 2, CAKE_CHIP_Y, t, lead=(cx2, CAKE_G - 14), group="s2.mem9")
    t = cue(2, 9, "burn")
    out(["s2.c.mem9"], t, "s2.burn9")
    br.ev("out", t, 0.6, group="s2.burn9")
    land = move_together(["s2.cake2"], t, (ON_WOOD[0] - cx2, ON_WOOD[1] - (CAKE_G - 4)), 1.1,
                         "the memorial to the fire", "s2.burn9")
    burn_on_wood(["s2.cake2"], land, "s2.fire9")

    # ======================================================================
    # 2:10  that which is left: Aaron's and his sons'; most holy
    # ======================================================================
    t = cue(2, 10, "left")
    left_pts = rect_pts(CAKE_XS[0] - 27, CAKE_G - 24, CAKE_XS[1] + 27, CAKE_G + 4)
    pulse_el("s2.left10", "bench", left_pts, t, group="s2.left10")
    pulse_el("s2.left10w", "bench", wafer_pts, t, group="s2.left10")
    out(["s2.c.oven", "s2.c.grid", "s2.c.pan"], t, "s2.left10")
    t = cue(2, 10, "Aaron's")
    chip("s2.c.aaron10", "Aaron and his sons", 92, CAKE_CHIP_Y, t, lead=(CAKE_XS[0] + 8, CAKE_G - 16),
         group="s2.aaron10")
    D.light("meal.eaten:the priests|Aaron and his sons", t,
            link=[("bench", left_pts, True)], group="s2.aaron10",
            steady_out=cue(2, 10, "most holy", d=-0.4))
    t = cue(2, 10, "most holy")
    chip("s2.c.holy10", "most holy", 92, CAKE_CHIP_Y - 34, t, group="s2.holy10")

    # ======================================================================
    # 2:11  case: no yeast; burn no yeast, nor any honey
    # ======================================================================
    t = at(2, 11, 0.2)
    P.case_clear(t, regions=("bench", "strip"), group="s2.clear11")
    case2.ev("out", t, 0.35, group="s2.clear11")

    t = cue(2, 11, "yeast")
    lump = F.smooth([(-17, 0), (-16, 10), (-6, 17), (6, 17), (16, 10), (17, 0)], n=4)
    lp = [(YEAST[0] + x, YEAST[1] + 9 - y) for x, y in lump]
    thing("s2.yeast", f'<polygon points="{B.pts_str(lp)}" fill="{B.rgb(mix(PANEL, FLOUR, .6))}" '
          f'stroke="{B.rgb(FLOUR)}" stroke-width="1.4"/>', t, group="s2.yeast")
    chip("s2.c.yeast", "yeast", YEAST[0] + 64, YEAST[1], t, group="s2.yeast")
    P.not_el("s2.no.yeast", "bench", (YEAST[0], YEAST[1]), 27, cue(2, 11, "yeast", 1))
    t = cue(2, 11, "honey")
    h_cy = (HONEY_G + ART.supply_top("honey", HONEY_G, HONEY_K)) / 2
    thing("s2.honey", ART.supply_svg("honey", HONEY_X, HONEY_G, HONEY_K), t, group="s2.honey")
    chip("s2.c.honey", "honey", HONEY_X + 64, h_cy, t, group="s2.honey")
    P.not_el("s2.no.honey", "bench", (HONEY_X, h_cy), 31, t + 0.4)

    # ======================================================================
    # 2:12  first fruits; they shall not rise up on the altar
    # ======================================================================
    J = (BRACE_X + 4, (YEAST[1] + h_cy) / 2)
    brace = [(BRACE_X - 8, YEAST[1] - 18), (BRACE_X, YEAST[1] - 18), (BRACE_X, h_cy + 22),
             (BRACE_X - 8, h_cy + 22)]
    t = cue(2, 12, "first fruits")
    traced_el("s2.brace", "bench", brace, TEXT_DIM, 2.0, t, 0.4, z=30)
    ffw = B.tbox("first fruits", *FF_CHIP, CHIP)
    P.arrow_el("s2.to_ff", [J, (ffw[0] - 12, FF_CHIP[1] + 6)], t + 0.3, 0.5, col=TEXT,
               width=2.2, z=30)
    chip("s2.c.ff12", "first fruits", *FF_CHIP, t, group="s2.ff12")
    t = cue(2, 12, "rise")
    to_alt = [J, (P.FIRE_XS[0] - 18, P.A_TOP - 34)]
    P.arrow_el("s2.to_alt", to_alt, t, 0.5, width=2.2, z=30)
    mid = ((to_alt[0][0] + to_alt[1][0]) / 2, (to_alt[0][1] + to_alt[1][1]) / 2)
    P.not_el("s2.no.rise", "bench", mid, 18, t + 0.5)

    # ======================================================================
    # 2:13  salt; the covenant; all your offerings
    # ======================================================================
    t = cue(2, 13, "salt")
    s_top = ART.supply_top("cup", SALT_G, SALT_K)
    thing("s2.salt", ART.supply_svg("cup", SALT_X, SALT_G, SALT_K), t, group="s2.salt")
    chip("s2.c.salt", "salt", SALT_X + 40, SALT_G - 20, t, group="s2.salt")
    out(["s2.c.ff12", "s2.to_ff", "s2.to_ff.h"], t, "s2.salt")
    salt_line = ART.supply_outline("cup", SALT_X, SALT_G, SALT_K)
    D.light("meal.thing:salt", t, link=[("bench", salt_line, True)], group="s2.salt")
    t = cue(2, 13, "covenant")
    chip("s2.c.cov", "covenant", SALT_X - 2, s_top - 34, t, lead=(SALT_X, s_top - 4),
         group="s2.cov")
    t = cue(2, 13, "all your offerings")
    for i in range(5):
        x, y, w, h = D.tab_rect(i)
        pulse_el(f"s2.tab.p{i}", "dock", rect_pts(x - 1, y - 1, x + w + 1, y + h + 1), t,
                 group="s2.tabs")

    # ======================================================================
    # 2:14  case: first fruits; parched; bruised
    # ======================================================================
    t = at(2, 14, 0.2)
    P.case_clear(t, regions=("bench", "strip"), group="s2.clear14")

    ears = F.grass()
    eb = F.bbox((ears, 0))
    e_top = EARS_G - eb[3] * EARS_K
    t = cue(2, 14, "first fruits")
    for i, x in enumerate(EARS_XS):
        el = add(El(f"s2.ear{i}", "bench", fig_svg(ears, x, EARS_G, EARS_K, GOLD), z=22))
        el.ev("in", t + i * 0.12, 0.5, group="s2.ff14", how="grow", about=(x, EARS_G))
    ears_box = (EARS_XS[0] + eb[0] * EARS_K, e_top, EARS_XS[-1] + eb[1] * EARS_K, EARS_G)
    ears_pts = rect_pts(ears_box[0] - 6, ears_box[1] - 6, ears_box[2] + 6, ears_box[3] + 4)
    chip("s2.c.ff14", "first fruits", EARS_XS[1], e_top - 26, t, lead=(EARS_XS[1], e_top + 4),
         group="s2.ff14")
    D.light("meal.thing:first fruits", t, link=[("bench", ears_pts, True)], group="s2.ff14")
    D.case_outline(["meal.thing:first fruits"], t + 0.6)
    t = cue(2, 14, "parched")
    fl = [x + 2 for x in EARS_XS]
    el = add(El("s2.parched", "bench", ART.flames(fl, FLAME_G, [26, 34, 26]), z=21))
    el.ev("in", t, 0.6, group="s2.parched", how="grow", about=(EARS_XS[1], FLAME_G))
    chip("s2.c.parched", "parched", 44, FLAME_G - 14, t, lead=(fl[0] - 12, FLAME_G - 10),
         group="s2.parched")
    t = cue(2, 14, "bruised")
    thing("s2.crush", ART.heap(CRUSH[0], CRUSH[1], 48, 14, GOLD), t, group="s2.bruised", z=22)
    chip("s2.c.bruised", "bruised", CRUSH[0], CRUSH[1] + 20, t, lead=(CRUSH[0], CRUSH[1] - 4),
         group="s2.bruised")

    # ======================================================================
    # 2:15  oil on it; frankincense on it
    # ======================================================================
    t = cue(2, 15, "oil")
    oil15 = F.smooth(ART.wave(ears_box[0] + 8, ears_box[2] - 8, e_top + 26, 4, 22),
                     closed=False, n=4)
    traced_el("s2.oil15", "bench", oil15, OIL, 4.0, t, 0.8, z=30)
    chip("s2.c.oil15", "oil", 36, e_top + 26, t, lead=(ears_box[0] + 6, e_top + 26),
         group="s2.oil15")
    out(["s2.c.parched"], t, "s2.oil15")
    t = cue(2, 15, "frankincense")
    f_top = ART.supply_top("cup", FCUP_G, FCUP_K)
    thing("s2.fcup", ART.supply_svg("cup", FCUP_X, FCUP_G, FCUP_K), t, group="s2.frank15")
    chip("s2.c.frank15", "frankincense", FCUP_X - 6, f_top - 26, t,
         lead=(FCUP_X, f_top - 2), group="s2.frank15")

    # ======================================================================
    # 2:16  the memorial: part of the grain, part of the oil, all the
    #       frankincense; part of it to the dock; the meal column filed
    # ======================================================================
    t = cue(2, 16, "memorial")
    chip("s2.c.mem16", "memorial", *MEM_CHIP, t, lead=(ON_WOOD[0] - 6, ON_WOOD[1] - 10),
         group="s2.mem16")
    out(["s2.c.bruised", "s2.c.oil15"], t, "s2.mem16")
    t = cue(2, 16, "part")
    sx, sy = CRUSH[0] - 8, CRUSH[1] - 2
    thing("s2.part", ART.heap(sx, sy, 30, 12, GOLD) + ellipse(sx, sy - 9, 8, 3, OIL), t,
          dur=0.3, group="s2.part", z=40)
    pulse_el("s2.crush.p", "bench", ART.heap_pts(CRUSH[0], CRUSH[1], 52, 16), t, group="s2.part")
    land = move_together(["s2.part"], t + 0.3, (ON_WOOD[0] - sx, ON_WOOD[1] - sy), 1.0,
                         "part of it to the fire", "s2.part")
    burn_on_wood(["s2.part"], land, "s2.fire16")
    land = D.fly("part of it", FLY_SRC, "meal.burns:part of it", land + 0.5)
    t = cue(2, 16, "oil")
    pulse_el("s2.oil16", "bench", oil15, max(t, land + 0.05), closed=False, group="s2.oil16")
    t = cue(2, 16, "all its frankincense")
    cup2_line = ART.supply_outline("cup", FCUP_X, FCUP_G, FCUP_K)
    pulse_el("s2.fcup.p", "bench", cup2_line, t, group="s2.all16")
    out(["s2.c.frank15"], t, "s2.all16", dur=0.4)
    chip("s2.c.all16", "all its frankincense", FCUP_X - 6, f_top - 26, t + 0.2,
         lead=(FCUP_X, f_top - 2), group="s2.all16")

    # the file view: the workshop crossfades to the table; the meal column
    # is filed; it holds across the seam and is gone by 3:1 t = 1.5
    t_fv = at(2, 16, 7.3)
    P.section_clear(t_fv, group="fileview")
    D.file_view("meal", t_fv, T_back=at(3, 1, 0.5))


def _palm():
    """Where the handful sits in the cupped hand (bench px): on the palm's
    top, over its middle (the hand is drawn flipped, palm up, unrotated)."""
    pts = F.hand("cup")["palm"]
    cx = sum(p[0] for p in pts) / len(pts)
    top = max(p[1] for p in pts)
    return (WRIST[0] - cx * HAND_K, WRIST[1] - top * HAND_K + 2)
