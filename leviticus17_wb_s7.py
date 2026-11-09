"""Leviticus 7:11-38 on the workbench (section s7): the law of the peace
offerings, the bans, the breast and the thigh, 7:37's whole table and 7:38
Sinai.

It starts on the s6|s7 boundary (the places named so far on the strip, the
altar set on the bench, the meal column in the dock) and ends the book: the
table filed whole at 7:37, Sinai over it, full frame, at 7:38.

The bench, in five sets (every set is laid out at bench size here, from the
shared drawings of leviticus17_art: the breads, meat, fat, drop, flames and
figures; 14 px words):

- 7:11-14, the bread rack (7:11 is the tab; on 7:12's "thanksgiving" the
  altar set steps out and the rack comes in: a full board). The four
  breads of offerings.BREADS on two shelves, each on its word; one of each
  lifted, heaved up, and lowered into the priest's hands.
- 7:15-18, the day strip (offerings.DAYS): day 1-3 columns, the thanksgiving,
  vow and freewill bars grown day by day, the third day's fire and the
  third day's meat under a not-mark.
- 7:19-22, the split: the meat to "unclean" (burned) or to the clean (they
  eat it); the one cut off slides away, with the causes (offerings.CAUSES).
- 7:23-28, the bans (S): the fat row and the blood row, each under a
  not-mark, with what they name, and "cut off" (offerings.PENALTIES).
- 7:28-36, the animal set (the altar back): the bull's cutaway between Aaron
  and his sons (left) and the priest who sprinkles the blood (right); the
  fat to the fire, the breast waved and carried to Aaron and his sons, the
  right thigh heaved and given to the priest.

Moves (QC's budget): no camera; chip flights at 7:12 (2), 7:13, 7:18, 7:19
(2), 7:31, 7:33; bench moves at 7:14 (2), 7:19, 7:20, 7:30, 7:31 (2), 7:32, 7:33;
the filing glide at 7:37.
"""

import offerings as OF
import svg_figures as F
import leviticus17_bench as B
import leviticus17_dock as D
import leviticus17_parts as P
import leviticus17_art as ART
from generate_tabernacle import (ACACIA, BG, GOLD, PANEL, RED, SAND, SAND_DIM, SILVER, TEXT, TEXT_DIM)
from leviticus17_bench import El, add, cue, fit, pulse_el, traced_el, glide, rect_pts
from leviticus17_art import drop_svg, fat_svg, meat_svg
from svg_vocab import mix

STUB = False
VERSES = [(7, v) for v in range(11, 39)]

BX0, BY0, BW, BH = B.BENCH
BX1, BY1 = BX0 + BW, BY0 + BH
CHIP = 14


def _label(board, key):
    return next(e for e in board if e.key == key).label


# ---------------------------------------------------------------------------
# small helpers (all bench elements, owned by s7)
# ---------------------------------------------------------------------------

def art(key, svg, T=None, dur=0.5, z=20, group=None, how=None, about=None, lift=8,
        texts=(), region="bench"):
    """A drawing that comes in at T (fade, lift or grow)."""
    el = add(El(key, region, svg, z=z, texts=texts, hidden0=T is None))
    if T is not None:
        kw = {}
        if how == "lift":
            kw = dict(how="lift", lift=lift)
        elif how == "grow":
            kw = dict(how="grow", about=about)
        el.ev("in", T, dur, group=group, **kw)
    return el


def label(key, s, x, y, T, size=14, anchor="mm", dur=0.4, group=None, col=TEXT, z=40,
          bold=False):
    """A drawing's name: plain words (no plate), registered for the text QC."""
    return art(key, B.text(s, x, y, size, col, anchor, bold=bold), T, dur, z, group,
               texts=[(B.tbox(s, x, y, size, anchor, bold), size, "bench label")])


def chip(key, s, x, y, T, lead=None, anchor="mm", group=None, out=None, dur=0.4, edge=SAND_DIM,
         z=60):
    """A 14 px word on a plate (leviticus17_bench.chip), with a leader."""
    svg, box = B.chip(s, x, y, CHIP, anchor, lead, edge=edge)
    el = add(El(key, "bench", svg, z=z, texts=[(box, CHIP, "bench chip")]))
    el.ev("in", T, dur, group=group)
    if out is not None:
        el.ev("out", out, 0.5)
    el.box = box
    return el


def arrow(key, pts, T, dur=0.5, col=TEXT_DIM, w=2.2, head=9.0):
    """An arrow traced along pts, its head after (parts.arrow_el)."""
    return P.arrow_el(key, pts, T, dur, col=col, width=w, head=head, z=30)


def bar(key, x0, x1, y, T, dur=0.7, h=22, col=SAND):
    """A day bar grown left to right (a thick line traced; its caps round)."""
    r = h / 2
    pts = [(x0 + r, y), (x1 - r, y)]
    return traced_el(key, "bench", pts, mix(PANEL, col, .45), h, T, dur, z=18)


def bread(kind, x, gy, k):
    """offerings.BREADS (leviticus17_art.bread_svg)."""
    return ART.bread_svg(kind, x, gy, k)


def person(did, parts, k):
    """A figure drawn once (<defs>) and used at (x, ground)."""
    B.define(did, B.fig(parts, 0, 0, k, TEXT, PANEL, tol=0.35))
    return did


def current(unit, T, group, link=()):
    """A dock unit named again: one pulse round it if it's lit (no steady
    outline, so nothing of it ends while the bench is busy), else lit."""
    return D.current(unit, T, link=link, group=group)


def shifted(pts, d):
    return [(x + d[0], y + d[1]) for x, y in pts]


# ---------------------------------------------------------------------------
# geometry
# ---------------------------------------------------------------------------

# D1, the rack (right of centre: its flights to BROUGHT stay under 560 px)
RACK_X = (300, 668)
SHELF = (372, 488)                       # the boards' tops
BREAD_K = 3.8
BREAD_AT = {"cakes": (392, SHELF[0]), "wafers": (576, SHELF[0]),
            "oil_cakes": (392, SHELF[1]), "leavened": (576, SHELF[1])}
BREAD_KEYS = ("cakes", "wafers", "oil_cakes", "leavened")
BRACKET_Y = 312
HEAVE_K = 2.1
D_PRIEST = (178, 528, 1.3)               # x, ground, scale
_HAND_Y = (D_PRIEST[1] - 127 * D_PRIEST[2] + 6, D_PRIEST[1] - 113 * D_PRIEST[2] + 6)
HEAVE_TO = [(D_PRIEST[0] - 17, _HAND_Y[1]), (D_PRIEST[0] + 17, _HAND_Y[1]),
            (D_PRIEST[0] - 17, _HAND_Y[0]), (D_PRIEST[0] + 17, _HAND_Y[0])]
HEAVE_UP = 70                            # how high they're heaved over his hands

# D2, the day strip
DAY_C = (164, 332, 500, 668)             # the columns' edges
DAY_HEAD_Y = 266
ROW_Y = {"thanksgiving": 314, "vow": 360, "freewill": 406}
FIRE3 = (584, 432)                       # the flame's foot
EAT3 = (584, 516)

# D3, the split
PLATE = (112, 300)
SPOT = (306, 440)                        # where the unclean meat goes (the flame's top)
FLAME_U = (306, 470)                     # the flame's foot
MEN_X = (440, 474, 508, 542)
CUT_FROM, CUT_TO = 578, 640
MEN_G = 452
MEN_K = 0.75

# S, the bans
FAT_ROW = (16, 246, 670, 396)
BLOOD_ROW = (16, 404, 670, 562)
ICON_X = 64

# the animal set (7:28-36): Aaron and his sons in the pen's back row, the
# bull, the priest who sprinkles the blood, the altar
GROUP_X = (36, 64, 92)
GROUP_K = 0.82
GROUP_G = P.PEN_BACK_G
OX_K = 1.6
OX_X = 70 + 51.6 * OX_K                  # its rump at x 70
OX_G = P.PEN_G
O_PRIEST = (310, OX_G, 1.08)             # the priest who sprinkles the blood
WAVE_AT = (275, 312)                     # where the breast is waved
CHIP_Y = 372                             # the parts' chips, over the bull


def build():
    E = B.ELS

    # ===================================================================
    # 7:11  the law of the sacrifice of peace offerings: the rack; the tab
    # ===================================================================
    D.switch("peace", cue(7, 11, "peace offerings"))

    # ===================================================================
    # 7:12  thanksgiving: the rack (the altar set steps out for it); the
    # unleavened cakes, wafers, cakes mixed with oil
    # ===================================================================
    t = cue(7, 12, "thanksgiving")
    P.altar_out(t, group="s7.set12")
    x0, x1 = RACK_X
    wood, dim = mix(PANEL, ACACIA, .7), mix(PANEL, ACACIA, .5)
    posts = "".join(B.slab(x - 5, SHELF[0] - 50, x + 5, SHELF[1] + 22, dim, ACACIA, 2)
                    for x in (x0 + 5, x1 - 5))
    boards = "".join(B.slab(x0, y, x1, y + 11, wood, ACACIA, 3) for y in SHELF)
    art("s7.rack", posts + boards, t, 0.6, z=12, group="s7.set12")
    tx = (x0 + x1) / 2
    traced_el("s7.bracket", "bench", [(x0 + 4, BRACKET_Y + 10), (x0 + 4, BRACKET_Y),
                                      (x1 - 4, BRACKET_Y), (x1 - 4, BRACKET_Y + 10)],
              TEXT_DIM, 2, t, 0.7, z=14)
    chip("s7.thanks", _label(OF.DAYS, "thanksgiving"), tx, BRACKET_Y - 20, t + 0.1,
         group="s7.bracket")

    def bread_in(kind, T):
        bx, gy = BREAD_AT[kind]
        art(f"s7.bread.{kind}", bread(kind, bx, gy, BREAD_K), T, 0.5, z=16, how="lift",
            group=f"s7.b.{kind}")
        label(f"s7.bread.{kind}.n", _label(OF.BREADS, kind), bx, gy + 24, T + 0.15,
              group=f"s7.b.{kind}")
        return bx, gy

    bx, gy = bread_in("cakes", cue(7, 12, "unleavened cakes"))
    land = D.fly("cakes", (bx - 24, gy - 18), "peace.thing:cakes", cue(7, 12, "unleavened cakes",
                                                                        d=0.55))
    t = cue(7, 12, "unleavened wafers")
    assert t > land + 0.05, (B.local(t), B.local(land))
    bx, gy = bread_in("wafers", t)
    land = D.fly("wafers", (bx - 26, gy - 18), "peace.thing:wafers", t + 0.55)
    t = cue(7, 12, "cakes mixed with oil", n=1)
    assert t > land + 0.05
    bread_in("oil_cakes", t)

    # ===================================================================
    # 7:13  leavened bread
    # ===================================================================
    t = cue(7, 13, "leavened bread")
    bx, gy = bread_in("leavened", t)
    land = D.fly("leavened bread", (bx - 40, gy - 22), "peace.thing:leavened bread", t + 0.55)
    case_breads = D.case_outline(["peace.thing:cakes", "peace.thing:wafers",
                                  "peace.thing:leavened bread"], land + 0.4, pad=1)

    # ===================================================================
    # 7:14  one out of each, heaved; the priest's who sprinkles the blood
    # ===================================================================
    t = cue(7, 14, "one out of each")
    lifts = []
    for kind in BREAD_KEYS:
        bx, gy = BREAD_AT[kind]
        el = art(f"s7.heave.{kind}", bread(kind, 0, 0, HEAVE_K), t, 0.4, z=26, how="lift",
                 lift=6, group="s7.one")
        el.off0 = (round(bx + 14, 1), round(gy - 4, 1))
        lifts.append(el)
    t = cue(7, 14, "heave offering")
    Ls = []
    for el, (hx, hy) in zip(lifts, HEAVE_TO):
        ox_, oy_ = el.off0
        to = (hx - ox_, hy - HEAVE_UP - oy_)
        Ls.append(glide(el, t, B.arc_path((0, 0), to, 0.12), 1.1, "", "", quad=True,
                        record=False, group="s7.heave"))
    B.travel(t, "one of each bread heaved up", max(Ls), 1.1, "bench move",
             keys=[e.key for e in lifts], group="s7.heave")
    hv = chip("s7.heavechip", "heave offering", D_PRIEST[0], BY0 + 20, t + 1.15)
    t = cue(7, 14, "priest's")
    px, pgy, pk = D_PRIEST
    pr_up = F.priest(arms="up")
    art("s7.priest14", B.fig(pr_up, px, pgy, pk, TEXT, PANEL), t, 0.5, z=22)
    t = cue(7, 14, "sprinkles")
    chip("s7.sprinkles", "sprinkles the blood", px, pgy + 22, t)
    t2 = t + 0.5
    for el in lifts:
        glide(el, t2, [(0, 0), (0, HEAVE_UP)], 0.9, "", "", record=False, group="s7.hands")
    B.travel(t2, "the breads into the priest's hands", HEAVE_UP, 0.9, "bench move",
             keys=[e.key for e in lifts], group="s7.hands")

    # ===================================================================
    # 7:15  the day strip: thanksgiving, day 1, until the morning
    # ===================================================================
    t = cue(7, 15, "flesh")
    P.case_clear(t, group="s7.set15", dur=0.6)
    case_breads.ev("out", t, 0.35, group="s7.set15")
    c0, c1, c2, c3 = DAY_C

    def head(n, xa, xb, T):
        traced_el(f"s7.day{n}.rule", "bench", [(xa + 6, DAY_HEAD_Y + 16), (xb - 6, DAY_HEAD_Y + 16)],
                  SAND_DIM, 1.6, T, 0.4, z=14)
        # the day's dashed divider fades in (a traced line can't be dashed)
        art(f"s7.day{n}.sep",
            f'<line x1="{xb}" y1="{DAY_HEAD_Y - 10}" x2="{xb}" y2="{ROW_Y["freewill"] + 18}" '
            f'stroke="{B.rgb(SAND_DIM)}" stroke-width="1.2" stroke-dasharray="4 5"/>',
            T + 0.1, 0.4, z=14, group=f"s7.day{n}.rule")
        label(f"s7.day{n}", f"day {n}", (xa + xb) / 2, DAY_HEAD_Y, T, group=f"s7.day{n}.rule")

    label("s7.row.thanks", _label(OF.DAYS, "thanksgiving"), BX0 + 14, ROW_Y["thanksgiving"],
          cue(7, 15, "thanksgiving"), anchor="lm")
    t = cue(7, 15, "day")
    head(1, c0, c1, t)
    bar("s7.bar.thanks", c0 + 2, c1 - 2, ROW_Y["thanksgiving"], t + 0.2)
    t = cue(7, 15, "morning")
    r1 = ROW_Y["thanksgiving"]
    traced_el("s7.tick", "bench", [(c1, r1 - 17), (c1, r1 + 17)], GOLD, 3.2, t, 0.4, z=24)
    label("s7.morning", _label(OF.DAYS, "morning"), c1 + 8, r1, t + 0.15, anchor="lm",
          dur=fit(t + 0.15, 0.4))

    # ===================================================================
    # 7:16  a vow, a freewill offering; the next day
    # ===================================================================
    for row, word in (("vow", "vow"), ("freewill", "freewill offering")):
        t = cue(7, 16, word)
        label(f"s7.row.{row}", _label(OF.DAYS, row), BX0 + 14, ROW_Y[row], t, anchor="lm",
              group=f"s7.r.{row}")
        bar(f"s7.bar.{row}", c0 + 2, c1 - 2, ROW_Y[row], t + 0.05, dur=0.6)
    t = cue(7, 16, "next day")
    head(2, c1, c2, t)
    bar("s7.bar.vow2", c1 + 2, c2 - 2, ROW_Y["vow"], t + 0.25, dur=0.6)
    bar("s7.bar.freewill2", c1 + 2, c2 - 2, ROW_Y["freewill"], t + 0.3, dur=0.6)

    # ===================================================================
    # 7:17  the third day; burned with fire
    # ===================================================================
    head(3, c2, c3, cue(7, 17, "third day"))
    t = cue(7, 17, "burned with fire")
    fx, fgy = FIRE3
    art("s7.fire3", ART.flames([fx - 16, fx, fx + 16], fgy, [34, 50, 34]), t, 0.7, z=20,
        how="grow", about=(fx, fgy), group="s7.fire3")
    chip("s7.fire3.n", _label(OF.DAYS, "burned"), fx, fgy + 20, t + 0.2,
         dur=fit(t + 0.2, 0.4))

    # ===================================================================
    # 7:18  eaten on the third day: not accepted, an abomination
    # ===================================================================
    t = cue(7, 18, "eaten")
    ex, ey = EAT3
    art("s7.eat3", meat_svg(ex, ey), t, 0.4, z=20)
    P.not_el("s7.eat3.not", "bench", (ex, ey + 2), 26, t + 0.35, dur=0.7)
    land = D.fly("third day's meat", (ex + 30, ey + 2), "peace.not_eaten:third day's meat",
                 t + 1.15)
    t = cue(7, 18, "accepted")
    assert t > land + 0.05
    cx_ = (c1 + c2) / 2 + 6
    chip("s7.notacc", _label(OF.DAYS, "not_accepted"), cx_, ey - 22, t, lead=(ex - 30, ey))
    chip("s7.abom", _label(OF.DAYS, "abomination"), cx_, ey + 22, cue(7, 18, "abomination"),
         lead=(ex - 30, ey + 6))

    # ===================================================================
    # 7:19  the meat: unclean (burned) or clean (eaten)
    # ===================================================================
    t = cue(7, 19, "meat")
    P.case_clear(t, group="s7.set19", dur=0.6)
    sx, sy = PLATE
    art("s7.plate", meat_svg(sx, sy, 46, 22), t, 0.6, z=20, group="s7.set19")
    label("s7.plate.n", "the meat", sx, sy + 36, t, dur=0.6, group="s7.set19")
    t = cue(7, 19, "unclean")
    arrow("s7.fork.u", [(sx + 34, sy + 14), (SPOT[0] - 32, SPOT[1] - 24)], t, 0.4)
    t2 = t + 0.55                            # the arrow is drawn; then the token goes
    tok = art("s7.tok.u", meat_svg(0, 0, 26, 12), t2, 0.25, z=30, group="s7.tok")
    tok.off0 = (sx, sy - 2)
    glide(tok, t2, B.arc_path((0, 0), (SPOT[0] - sx, SPOT[1] - sy + 2), 0.15), 0.7,
          "the meat to the unclean", "bench move", quad=True, group="s7.tok")
    label("s7.unclean", "unclean", FLAME_U[0], FLAME_U[1] + 20, t2, group="s7.tok")
    land = D.fly("unclean meat", (SPOT[0] + 20, SPOT[1]), "peace.not_eaten:unclean meat",
                 cue(7, 19, "not"))
    t = cue(7, 19, "burned")
    assert t > land + 0.05
    ux, ugy = FLAME_U
    art("s7.flame.u", ART.flames([ux - 18, ux, ux + 18], ugy, [42, 60, 42]), t, 0.8, z=24,
        how="grow", about=(ux, ugy))
    t = cue(7, 19, "everyone")
    did = person("s7_man", F.man(), MEN_K)
    gx = (MEN_X[0] + MEN_X[-1]) / 2
    arrow("s7.fork.c", [(sx + 38, sy - 6), (MEN_X[0] - 20, MEN_G - 76)], t, 0.45)
    art("s7.men", "".join(B.use(did, x, MEN_G) for x in MEN_X), t, 0.5, z=22, group="s7.men")
    art("s7.cutman", B.use(did, CUT_FROM, MEN_G), t, 0.5, z=22, group="s7.men")
    land = D.fly("the offerer", (MEN_X[0] - 4, MEN_G - 92), "peace.eaten:the offerer",
                 t + 0.4, T_go=t + 0.52)
    label("s7.clean", "clean", gx, MEN_G + 18, land + 0.08, dur=fit(land + 0.08, 0.3))

    # ===================================================================
    # 7:20  the soul who eats with his uncleanness: cut off
    # ===================================================================
    man_line = F.outline(F.man(), CUT_FROM, MEN_G, MEN_K)
    t = cue(7, 20, "uncleanness")
    D.light("peace.not_eaten:unclean meat", t, link=[("bench", man_line, True)],
            group="s7.unc20", steady_out=t + 1.6)
    t = cue(7, 20, "cut off")
    glide(E["s7.cutman"], t, [(0, 0), (CUT_TO - CUT_FROM, 0)], 0.8, "the one cut off",
          "bench move", group="s7.cut20")
    chip("s7.cutoff", _label(OF.PENALTIES, "unclean_eats"), CUT_TO, MEN_G - 100 * MEN_K - 14, t,
         edge=RED, group="s7.cut20")

    # ===================================================================
    # 7:21-22  the uncleanness of man, an unclean animal; cut off
    # ===================================================================
    man2 = F.outline(F.man(), CUT_TO, MEN_G, MEN_K)
    hx, hy = CUT_TO - 6, MEN_G - 34
    cx2 = 486
    chip("s7.cause.man", _label(OF.CAUSES, "uncleanness_of_man"), cx2, 515,
         cue(7, 21, "uncleanness of man"), lead=(hx, hy))
    chip("s7.cause.animal", _label(OF.CAUSES, "unclean_animal"), cx2, 549,
         cue(7, 21, "unclean animal"), lead=(hx + 2, hy + 12))
    t = cue(7, 21, "eats")
    D.light("peace.not_eaten:unclean meat", t,
            link=[("bench", rect_pts(SPOT[0] - 18, SPOT[1] - 10, SPOT[0] + 18, SPOT[1] + 10), True)],
            group="s7.unc21", steady_out=t + 1.6)
    t = cue(7, 21, "cut off")
    pulse_el("s7.cut21.p", "bench", man2, t, group="s7.cut21")
    pulse_el("s7.cut21.cp", "bench", B.box_pts(E["s7.cutoff"].box, 2), t, group="s7.cut21")
    P.case_clear(cue(7, 22, "Yahweh"), group="s7.set22")

    # ===================================================================
    # 7:23  no fat: of bull, or sheep, or goat
    # ===================================================================
    rowc = mix(PANEL, BG, .45)

    def row_frame(key, b, T):
        return art(key, f'<rect x="{b[0]}" y="{b[1]}" width="{b[2] - b[0]}" height="{b[3] - b[1]}" '
                        f'rx="8" fill="{B.rgb(rowc)}" stroke="{B.rgb(SAND_DIM)}" '
                        f'stroke-width="1.2"/>', T, 0.4, z=8)

    fy = (FAT_ROW[1] + FAT_ROW[3]) / 2 - 8
    row_frame("s7.row.fat", FAT_ROW, cue(7, 23, "eat"))
    t = cue(7, 23, "fat")
    art("s7.fat", fat_svg(ICON_X, fy, 58, 32), t, 0.4, z=20, group="s7.fat23")
    label("s7.fat.n", "fat", ICON_X, FAT_ROW[3] - 22, t, group="s7.fat23")
    current("peace.not_eaten:the fat, the blood", t, group="s7.fat23")
    P.not_el("s7.fat.not", "bench", (ICON_X, fy), 32, t + 0.8, dur=0.7)
    ban_g = FAT_ROW[3] - 44                 # the beasts' ground

    def beast(key, parts, x, gy, k, word, T, ink_=TEXT, flip=-1, ly=None):
        x0_, x1_, _y0, _y1 = F.bbox((parts, 0))
        art(key, B.fig(parts, x, gy, k, ink_, PANEL, flip=flip), T, fit(T, 0.5), z=20,
            how="lift", group=key)
        label(key + ".n", word, x, (ly or gy + 22), T + 0.1, dur=fit(T + 0.1, 0.4), group=key)
        return F.outline(parts, x, gy, k, flip=flip)

    beast("s7.ban.ox", F.ox(), 168, ban_g, 0.7, "bull", cue(7, 23, "bull"))
    beast("s7.ban.sheep", F.sheep(ram=True), 262, ban_g, 1.15, "sheep", cue(7, 23, "sheep"))
    beast("s7.ban.goat", F.goat(), 344, ban_g, 0.85, "goat", cue(7, 23, "goat"))

    # ===================================================================
    # 7:24  dies of itself, torn: other service; in no way eat
    # ===================================================================
    nx, ny = 418, fy
    art("s7.noeat", fat_svg(nx, ny, 32, 20), cue(7, 24, "fat"), 0.4, z=20)
    cx3 = 512
    label("s7.died", "dies of itself", cx3, fy - 20, cue(7, 24, "dies of itself"))
    label("s7.torn", "torn", cx3, fy + 16, cue(7, 24, "torn"))
    t = cue(7, 24, "service")
    arrow("s7.svc.a", [(562, fy - 2), (580, fy - 2)], t, 0.3)
    chip("s7.service", "other service", 588, fy - 2, t + 0.25, anchor="lm")
    P.not_el("s7.noeat.not", "bench", (nx, ny), 22, cue(7, 24, "no way"), dur=0.7)

    # ===================================================================
    # 7:25  whoever eats the fat: cut off
    # ===================================================================
    pulse_el("s7.fat25.p", "bench", B.ring_pts((ICON_X, fy), 36), cue(7, 25, "fat"))
    chip("s7.cutfat", _label(OF.PENALTIES, "eats_fat"), 636, FAT_ROW[3] - 22,
         cue(7, 25, "cut off"), edge=RED)

    # ===================================================================
    # 7:26  no blood: bird or animal, in any of your dwellings
    # ===================================================================
    by = (BLOOD_ROW[1] + BLOOD_ROW[3]) / 2 - 10
    t = cue(7, 26, "blood")
    art("s7.row.blood", f'<rect x="{BLOOD_ROW[0]}" y="{BLOOD_ROW[1]}" '
                        f'width="{BLOOD_ROW[2] - BLOOD_ROW[0]}" height="{BLOOD_ROW[3] - BLOOD_ROW[1]}" '
                        f'rx="8" fill="{B.rgb(rowc)}" stroke="{B.rgb(SAND_DIM)}" stroke-width="1.2"/>',
        t, 0.4, z=8, group="s7.blood26")
    art("s7.drop", drop_svg(ICON_X, by, 48), t, 0.4, z=20, group="s7.blood26")
    label("s7.drop.n", "blood", ICON_X, BLOOD_ROW[3] - 22, t, group="s7.blood26")
    current("peace.not_eaten:the fat, the blood", t, group="s7.blood26")
    P.not_el("s7.drop.not", "bench", (ICON_X, by), 32, t + 0.8, dur=0.7)
    bg_ = BLOOD_ROW[3] - 44
    beast("s7.ban.dove", F.dove(descending=False), 168, bg_ - 4, 2.5, "bird",
          cue(7, 26, "bird"), ink_=SILVER, ly=bg_ + 22)
    beast("s7.ban.animal", F.goat(), 262, bg_, 0.85, "animal", cue(7, 26, "animal"))
    tent = F.tent()
    t = cue(7, 26, "dwellings")
    art("s7.tent", B.fig(tent, 372, bg_, 0.36, SAND, PANEL), t, fit(t, 0.5), z=20, how="lift",
        group="s7.tent")
    label("s7.tent.n", "dwellings", 372, bg_ + 22, t + 0.1, dur=fit(t + 0.1, 0.4), group="s7.tent")

    # ===================================================================
    # 7:27-28  whoever eats any blood: cut off; Yahweh spoke to Moses
    # ===================================================================
    pulse_el("s7.blood27.p", "bench", B.ring_pts((ICON_X, by), 36), cue(7, 27, "blood"))
    chip("s7.cutblood", _label(OF.PENALTIES, "eats_blood"), 636, BLOOD_ROW[3] - 22,
         cue(7, 27, "cut off"), edge=RED)
    t = cue(7, 28, "Yahweh")
    P.case_clear(t, group="s7.set28", dur=0.6)
    P.altar_in(t, group="s7.set28")

    # ===================================================================
    # 7:29  he who offers the sacrifice of his peace offerings: the bull
    # ===================================================================
    t = cue(7, 29, "offers")
    ox = P.Beast("bull", OX_X, OX_G, OX_K)
    P.figure_el("s7.ox", F.ox(), OX_X, OX_G, OX_K, t, group="s7.ox")
    reach = F.side_person(arms="reach")
    hpx, _hpy = ART.hand_pt(reach)
    hx, _hy = ox.anchor["head"]
    P.figure_el("s7.offerer", reach, hx + hpx * OX_K + 12, OX_G, OX_K, t, flip=-1, z=22,
                group="s7.ox")
    t = cue(7, 29, "peace offerings")
    ox_line = F.outline(F.ox(), OX_X, OX_G, OX_K)
    D.light("peace.thing:herd", t, link=[("bench", ox_line, True)], group="s7.herd29",
            steady_out=t + 0.9)
    case_beasts = D.case_outline(["peace.thing:herd", "peace.thing:lamb", "peace.thing:goat"],
                                 t + 1.0, pad=1)

    # ===================================================================
    # 7:30  made by fire; the fat with the breast; the breast waved
    # ===================================================================
    P.flare(cue(7, 30, "fire"), 1.25, 0.9, group="s7.fire30")
    t = cue(7, 30, "fat")
    E["s7.ox"].ev("out", t, 0.6, group="s7.cut30")
    E["s7.offerer"].ev("out", t, 0.6, group="s7.cut30")
    P.cutaway(ox, "s7bull", t, group="s7.cut30")
    fa = ox.anchor["fat"]
    chip("s7.chip.fat", "fat", fa[0] - 14, CHIP_Y, t + 0.05, lead=fa, group="s7.cut30")
    P.part_pulse(ox, "s7bull", "fat", t + 0.05, group="s7.cut30")
    t = cue(7, 30, "breast")
    ba = ox.anchor["breast"]
    P.part_pulse(ox, "s7bull", "breast", t, group="s7.br30")
    chip_br = chip("s7.chip.breast", "breast", ba[0] + 24, CHIP_Y, t, lead=ba, group="s7.br30")
    t = cue(7, 30, "waved")
    brs = add(El("s7.breast", "bench", ox.part_svg("breast"), z=34, hidden0=True))
    brs.ev("show", t, group="s7.wave")
    E["cut.s7bull.breast"].ev("dim", t, 0.4, to=0.3, group="s7.wave")
    chip_br.ev("out", t, 0.4, group="s7.wave")
    w = (WAVE_AT[0] - ba[0], WAVE_AT[1] - ba[1])
    wave = [(0, 0), (w[0] * 0.5, w[1] * 0.9), w, (w[0] + 16, w[1]), (w[0] - 16, w[1]), w]
    glide(brs, t, wave, 1.6, "the breast waved", "bench move", group="s7.wave")
    chip("s7.chip.wave", "wave offering", WAVE_AT[0] + 30, WAVE_AT[1], cue(7, 30, "wave offering"),
         anchor="lm", group="s7.wave")

    # ===================================================================
    # 7:31  the fat burned on the altar; the breast: Aaron's and his sons'
    # ===================================================================
    t = cue(7, 31, "priest")
    opx, opg, opk = O_PRIEST
    pr = F.priest()
    art("s7.priest", B.fig(pr, opx, opg, opk, TEXT, PANEL, flip=-1), t, 0.5, z=22,
        group="s7.pr31")
    pr_chip = chip("s7.chip.priest", "the priest", opx, opg - 105 * opk - 22, t + 0.05,
                   group="s7.pr31")
    t = cue(7, 31, "burn")
    E["s7.chip.fat"].ev("out", t, 0.4)
    P.to_wood(ox, "s7bull", {"fat": fa}, t, ["fat"])
    t = max(cue(7, 31, "altar"), t + 0.1 + 1.0 + 0.05)      # once the fat is on the wood
    P.place("altar", t, group="s7.alt31")
    P.flare(t + 0.2, 1.3, 0.8, group="s7.alt31")
    t = cue(7, 31, "breast")
    E["s7.chip.wave"].ev("out", t, 0.3)
    land = D.fly("the breast", (WAVE_AT[0] + 10, WAVE_AT[1]), "peace.eaten:the breast", t,
                 T_go=t + 0.15)
    t = max(land + 0.12, cue(7, 31, "Aaron's"))     # after the slot's reveal
    gdid = person("s7_priest_s", F.priest(), GROUP_K)
    art("s7.group", "".join(B.use(gdid, x, GROUP_G) for x in GROUP_X), t, 0.4, z=22,
        group="s7.toaaron")
    br_hold = (GROUP_X[-1] + 30, GROUP_G - 36)
    d = fit(t, 0.75)
    glide(brs, t, B.arc_path((0, 0), (br_hold[0] - WAVE_AT[0], br_hold[1] - WAVE_AT[1]), 0.12),
          d, "the breast to Aaron and his sons", "bench move", quad=True, group="s7.toaaron")
    chip("s7.chip.group", "Aaron and his sons", BX0 + 8, BY0 + 16, t, anchor="lm",
         group="s7.toaaron", dur=fit(t, 0.4))

    # ===================================================================
    # 7:32  the right thigh, to the priest, heaved
    # ===================================================================
    t = cue(7, 32, "right thigh")
    ta = ox.anchor["right_thigh"]
    P.part_pulse(ox, "s7bull", "right_thigh", t, group="s7.th32")
    th_chip = chip("s7.chip.thigh", "right thigh", ta[0] + 30, CHIP_Y, t, lead=ta,
                   group="s7.th32")
    t = cue(7, 32, "priest")
    pulse_el("s7.pr32.p", "bench", F.outline(pr, opx, opg, opk, flip=-1), t)
    t = cue(7, 32, "heave offering")
    ths = add(El("s7.thigh", "bench", ox.part_svg("right_thigh"), z=34, hidden0=True))
    ths.ev("show", t, group="s7.heave32")
    E["cut.s7bull.right_thigh"].ev("dim", t, 0.4, to=0.3, group="s7.heave32")
    th_chip.ev("out", t, 0.4, group="s7.heave32")
    up = -95
    glide(ths, t, [(0, 0), (0, up), (0, up + 15)], 1.0, "the thigh heaved", "bench move",
          group="s7.heave32")
    chip("s7.chip.heave", "heave offering", ta[0] + 34, ta[1] + up + 15, t + 0.3, anchor="lm",
         group="s7.heave32")

    # ===================================================================
    # 7:33  the sons of Aaron who offers the blood: the right thigh
    # ===================================================================
    t = cue(7, 33, "sons of Aaron")
    th_hold = (opx - 14, opg - 62)
    rel = (th_hold[0] - ta[0], th_hold[1] - (ta[1] + up + 15))
    glide(ths, t, B.arc_path((0, 0), rel, 0.12), 0.9, "the thigh to the priest", "bench move",
          quad=True, group="s7.th33")
    E["s7.chip.heave"].ev("out", t, 0.4, group="s7.th33")
    th_off = (th_hold[0] - ta[0], th_hold[1] - ta[1])
    land = D.fly("the right thigh", (th_hold[0] + 22, th_hold[1] - 20),
                 "peace.eaten:the right thigh", cue(7, 33, "blood"))
    th_line = shifted(ox.outline("right_thigh")[0][0], th_off)
    t = cue(7, 33, "right thigh")
    assert t > land
    D.light("peace.eaten:the right thigh", t, link=[("bench", th_line, True)], group="s7.th33b",
            steady_out=t + 0.9)

    # ===================================================================
    # 7:34  the waved breast, the heaved thigh: Aaron the priest and his sons
    # ===================================================================
    br_off = (br_hold[0] - ba[0], br_hold[1] - ba[1])
    br_line = shifted(ox.outline("breast")[0][0], br_off)
    t = cue(7, 34, "waved breast")
    D.light("peace.eaten:the breast", t, link=[("bench", br_line, True)], group="s7.br34",
            steady_out=t + 0.75)
    t = cue(7, 34, "heaved thigh")
    D.light("peace.eaten:the right thigh", t, link=[("bench", th_line, True)], group="s7.th34",
            steady_out=t + 1.4)
    t = cue(7, 34, "Aaron the priest")
    group_line = rect_pts(GROUP_X[0] - 16, GROUP_G - 90, GROUP_X[-1] + 16, GROUP_G + 3)
    pulse_el("s7.g34.p", "bench", group_line, t, group="s7.g34")
    pulse_el("s7.pr34.p", "bench", F.outline(pr, opx, opg, opk, flip=-1), t, group="s7.g34")

    # ===================================================================
    # 7:35-36  the anointing portion of Aaron and of his sons
    # ===================================================================
    t = cue(7, 35, "anointing portion")
    chip("s7.chip.anoint", "anointing portion", 300, BY0 + 24, t, group="s7.an35")
    pulse_el("s7.an35.b", "bench", br_line, t, group="s7.an35")
    pulse_el("s7.an35.t", "bench", th_line, cue(7, 35, "anointing portion", n=1))
    # the case ends with the law of the shares: the bench and the case
    # outline clear (the altar set stays) before 7:37's file view
    t = cue(7, 36, "throughout")
    P.case_clear(t, group="s7.clear36")
    case_beasts.ev("out", t, 0.6, group="s7.clear36")

    # ===================================================================
    # 7:37  the law of all of them: the final file view
    # ===================================================================
    t_fv = cue(7, 37, "law")
    P.section_clear(t_fv, group="fileview")
    # the peace column is filed after "burnt offering"'s WHEN has lifted and
    # lands before "meal offering"'s: nothing in the view lights up while it
    # glides; it takes the low road, under the sin and trespass keys
    t_burnt = cue(7, 37, "burnt offering")
    fv = D.file_view("peace", t_fv, T_back=None, glide_at=t_burnt + 0.65, glide_dur=0.9, low=30)
    for off, phrase in (("burnt", "burnt offering"), ("meal", "meal offering"),
                        ("sin", "sin offering"), ("trespass", "trespass offering")):
        t = cue(7, 37, phrase)
        if off != "burnt":
            t = max(t, fv.t_land + 0.05)
        fv.pulse_column(off, t, group=f"s7.law.{off}")
        fv.lift(f"{off}.when", t, group=f"s7.law.{off}")
    t = cue(7, 37, "consecration")
    cx, cy = (941 + 1024) / 2, 28
    svg, box = B.chip("consecration", cx, cy, 12, "mm", edge=B.HL)
    cons = add(El("s7.consecration", "top", svg, z=106, hidden0=True,
                  texts=[(box, 12, "file view chip")]))
    cons.ev("in", t, 0.5, group="s7.cons")
    pulse_el("s7.cons.p", "top", B.box_pts(box, 2), t + 0.4, group="s7.cons", z=106)
    t = cue(7, 37, "peace offerings")
    fv.pulse_column("peace", t, group="s7.law.peace")
    fv.lift("peace.when", t, dur=fit(t, 0.6), group="s7.law.peace")

    # ===================================================================
    # 7:38  Mount Sinai, the wilderness of Sinai: full frame, over the table
    # ===================================================================
    # the table crossfades straight into the Sinai drawing: the panel comes
    # in as Moses is named, so no blank frame comes between
    t = max(cue(7, 38, "which"), cue(7, 38, "Moses") - 0.6)
    W_, H_ = B.W, B.H
    panel = (f'<rect width="{W_}" height="{H_}" fill="{B.rgb(BG)}"/>'
             f'<rect x="8" y="8" width="{W_ - 16}" height="{H_ - 16}" rx="10" '
             f'fill="{B.rgb(PANEL)}" stroke="{B.rgb(SAND_DIM)}" stroke-width="1.5"/>')
    art("s7.sinai", panel, t, 0.8, z=120, region="top", group="s7.sinai").cover = True
    for k_ in [k.key for k in fv.key_els] + ["s7.consecration"]:
        E[k_].ev("hide", t + 0.85, group="fileview")
    # Moses
    t = cue(7, 38, "Moses")
    mx, mgy, mk = 858, 470, 1.5
    art("s7.moses", B.fig(F.man(staff=True), mx, mgy, mk, TEXT, PANEL), t, 0.5, z=124,
        region="top", how="lift", group="s7.moses")
    svg, box = B.chip(_label(OF.SINAI, "moses"), mx, mgy + 28, 16, "mm")
    art("s7.moses.n", svg, t + 0.15, 0.4, z=126, region="top", group="s7.moses",
        texts=[(box, 16, "Sinai chip")])
    # the mountain, drawn in
    t = cue(7, 38, "Mount Sinai")
    mt_x, mt_g, mt_k = 470, 452, 2.2
    mtn = F.mountain()
    art("s7.mount", B.fig(mtn, mt_x, mt_g, mt_k, SAND, PANEL), t, 1.2, z=122, region="top",
        how="grow", about=(mt_x, mt_g), group="s7.mount")
    ring = F.outline(mtn, mt_x, mt_g, mt_k)
    top = min(p[1] for p in ring)
    peak_x = [p[0] for p in ring if p[1] == top][0]
    svg, box = B.chip(_label(OF.SINAI, "mount"), peak_x, top - 30, 16, "mm", lead=(peak_x, top - 4))
    art("s7.mount.n", svg, t + 0.3, 0.4, z=126, region="top", group="s7.mount",
        texts=[(box, 16, "Sinai chip")])
    # the wilderness
    t = cue(7, 38, "wilderness of Sinai")
    gr = [(60, 462), (220, 458), (380, 466), (540, 460), (700, 466), (860, 470), (980, 466)]
    sand = (f'<polygon points="{B.pts_str(gr + [(980, 520), (60, 520)])}" '
            f'fill="{B.rgb(mix(PANEL, SAND, .22))}" stroke="none"/>')
    art("s7.sand", sand, t, fit(t, 0.8), z=121, region="top", group="s7.wild")
    tr = traced_el("s7.ground", "top", gr, SAND, 2.4, t, fit(t, 0.9), z=123)
    del tr
    svg, box = B.chip(_label(OF.SINAI, "wilderness"), 330, 504, 16, "mm")
    art("s7.wild.n", svg, t + 0.2, fit(t + 0.2, 0.4), z=126, region="top", group="s7.wild",
        texts=[(box, 16, "Sinai chip")])
