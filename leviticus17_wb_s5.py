"""Leviticus 5:1-6:7 (and the 5:13-14, 5:18-19, 6:7-8 ranges), on the
workbench (section s5): the sin offering's causes, birds and flour, then the
trespass offering.

It starts on the s4|s5 boundary (the places named so far, the altar set, the
sin column lit under the sin tab) and leaves the s5|s6 boundary: the same
places, the altar set at rest, and the trespass column lit under the trespass
tab, with no outline on.

The bench, verse by verse:

- 5:1-5  the full board M (the altar out): a 2 x 2 of the four things
  "hidden from him", one cell a verse (the witness; the carcass of three
  kinds; the uncleanness of man; the rash oath), each earlier cell dimmed as
  the next comes in; 5:5 pulses the four on "one of these" and draws
  "confess" out of the grid toward the dock.
- 5:6  "one guilty of 5:1-4" lifts in BROUGHT with a link pulse on the four
  cells; on "female" the board gives way to the animal set: a lamb and a
  female goat (their icons current again).
- 5:7-10  the birds: two doves ("sin offering", "burnt offering"); the sin
  dove to the bird bay, its neck wrung, "not severed"; the blood on the
  altar's side ("the altar's side" flies to THE BLOOD), drained at its base;
  the second dove onto the fire.
- 5:11-13  the flour: the ephah in ten parts and its tenth, the basket of
  fine flour, no oil and no frankincense (not-marks); the priest; his handful
  to the fire ("a handful" flies to ON THE ALTAR); "the remaining flour"
  flies to WHO EATS, and the sin column is filed (the file view holds
  through 5:14's formula, and the workshop comes back before 5:14 ends, so
  5:15 opens on it).
- 5:15-6:7  the trespass offering: the board T (the altar out). The man who
  sins stays at the left throughout. The value set: the ram, the balance
  ("estimation"), the coins ("silver", whose unit flies), "shekel of the
  sanctuary"; 5:16's restitution bar of five parts and its fifth, to the
  priest; 5:17 dims it for "didn't know" / "guilty"; 5:18 brings the ram,
  the estimation and the priest back. 6:2-4: the neighbor and the six wrongs
  with their return arrows; 6:5: the bar again, "in full", the fifth, "to
  whom it belongs", "in the day"; 6:6: the ram, the estimation, the priest.
  6:7: "before Yahweh" brings the altar back (priests at the strip's altar),
  "forgiven", and the trespass column is filed.

Moves (QC's budget): chip flights at 5:9, 5:12, 5:13 and 5:15; bench moves
at 5:8, 5:10 and 5:12; the filing glides in the 5:13-14 and 6:7-8 ranges.
"""

import svg_figures as F
import leviticus17_bench as B
import leviticus17_dock as D
import leviticus17_parts as P
import leviticus17_art as ART
from generate_tabernacle import GOLD, PANEL, SAND, SAND_DIM, SILVER, TEXT, WHITE_LINEN
from leviticus17_bench import El, add, cue, at, fit, pulse_el, traced_el, glide, rect_pts
from leviticus17_parts import S, BLOOD
from leviticus17_art import hand_svg
from svg_vocab import mix

STUB = False
VERSES = [(5, v) for v in range(1, 20)] + [(6, v) for v in range(1, 9)]

REACH = {}
EXCUSED = {}

DIM = mix(PANEL, TEXT, .55)            # a figure spoken of, not there
ARROW = SAND
FLOUR = WHITE_LINEN
FRAME = mix(PANEL, SAND_DIM, .7)
LOW = 0.38                             # a dimmed earlier cell
GUILTY = "sin.who:one guilty of 5:1–4"
E = B.ELS


# ---------------------------------------------------------------------------
# small helpers (everything keyed "s5.")
# ---------------------------------------------------------------------------

def k5(key):
    return key if key.startswith("s5.") else "s5." + key


def chip(key, s, x, y, T, lead=None, anchor="mm", out=None, group=None, dur=0.5):
    return P.bench_chip(k5(key), s, x, y, T, lead=lead, anchor=anchor, out=out, group=group,
                        dur=fit(T, dur))


def figure(key, parts, x, gy, k, T, flip=1, ink_=TEXT, z=20, group=None, dur=0.6):
    return P.figure_el(k5(key), parts, x, gy, k, T, flip=flip, ink_=ink_, z=z,
                       dur=fit(T, dur), group=group)


def outline(parts, x, gy, k, flip=1):
    return F.outline(parts, x, gy, k, flip=flip)


def shape(key, svg, T, z=18, group=None, dur=0.5, texts=(), how=None, **kw):
    el = add(El(k5(key), "bench", svg, z=z, texts=list(texts)))
    if how:
        el.ev("in", T, fit(T, dur), how=how, group=group, **kw)
    else:
        el.ev("in", T, fit(T, dur), group=group)
    return el


def frame_svg(b):
    return (f'<rect x="{B.f2(b[0])}" y="{B.f2(b[1])}" width="{B.f2(b[2] - b[0])}" '
            f'height="{B.f2(b[3] - b[1])}" rx="8" fill="none" stroke="{B.rgb(FRAME)}" '
            f'stroke-width="1.4"/>')


def arrow_el(key, pts, T, dur=0.7, col=ARROW, width=3.2, head=11, z=40):
    """parts.arrow_el in the trespass board's colour. Returns (line, head)."""
    return P.arrow_el(k5(key), pts, T, dur, col=col, width=width, head=head, z=z)


def label_el(key, s, x, y, size, T, col=TEXT, bold=True, anchor="mm", z=62, group=None, dur=0.4):
    el = add(El(k5(key), "bench", B.text(s, x, y, size, col, anchor, bold=bold), z=z,
                texts=[(B.tbox(s, x, y, size, anchor, bold), size, "bench label")]))
    el.ev("in", T, fit(T, dur), group=group)
    return el


def outs(els, T, dur=0.6, group=None):
    """Fade out the given elements (keys, Els or arrows) that are on at T."""
    P.outs([k5(e) if isinstance(e, str) else e for e in els], T, dur, group)


def dims(els, T, to, dur=0.6, group=None):
    for el in els:
        el = E[k5(el)] if isinstance(el, str) else el
        el.ev("dim", T, fit(T, dur), to=to, group=group)


# ---------------------------------------------------------------------------
# geometry
# ---------------------------------------------------------------------------

BX0, BY0, BW, BH = B.BENCH
BX1, BY1 = BX0 + BW, BY0 + BH
_PAD, _GAP = 8, 8
_CW = (BW - 2 * _PAD - _GAP) / 2                    # 323
_CH = (BH - 2 * _PAD - _GAP) / 2                    # 153
CELLS = {}
for _i, (_cx, _cy) in enumerate(((0, 0), (1, 0), (0, 1), (1, 1))):
    _x0 = BX0 + _PAD + _cx * (_CW + _GAP)
    _y0 = BY0 + _PAD + _cy * (_CH + _GAP)
    CELLS[_i + 1] = (_x0, _y0, _x0 + _CW, _y0 + _CH)
del _i, _cx, _cy, _x0, _y0
MID = (CELLS[1][2] + _GAP / 2, CELLS[1][3] + _GAP / 2)   # the grid's crossing

# the trespass board
MAN = (62, 556, 1.38)                  # the one who sins (left, throughout)
TG = 400                               # the value set's ground
RAM = (232, TG, 2.6)
SCALES = (442, TG, 2.4)
COINS = (536, TG, 4.4)
PRIEST = (630, TG, 1.45)
BAR_X0, BAR_PART, BAR_Y = 170, 50, (470, 500)
BAR_X1 = BAR_X0 + 5 * BAR_PART         # 420
FIFTH_X1 = BAR_X1 + BAR_PART           # 470
NEIGHBOR = (612, 556, 1.38)
WRONG_X = 300
WRONG_Y = [262 + 45 * i for i in range(6)]


def _fig_box(parts, x, gy, s, flip=1):
    x0, x1, y0, y1 = F.bbox((parts, 0))
    if flip < 0:
        x0, x1 = -x1, -x0
    return (x + x0 * s, gy - y1 * s, x + x1 * s, gy - y0 * s)


def bar_svg(x0, y0, y1, n=5, w=BAR_PART, fill=None):
    fill = fill or mix(PANEL, SILVER, .5)
    return "".join(f'<rect x="{B.f2(x0 + i * w)}" y="{y0}" width="{w}" height="{y1 - y0}" rx="3" '
                   f'fill="{B.rgb(fill)}" stroke="{B.rgb(TEXT)}" stroke-width="1.4"/>'
                   for i in range(n))


# ---------------------------------------------------------------------------
# the build
# ---------------------------------------------------------------------------

def build():
    causes()
    birds()
    flour()
    trespass()


# ---- 5:1-6: the causes (board M), the female of the flock ------------------

def causes():
    c1, c2, c3, c4 = (CELLS[i] for i in (1, 2, 3, 4))
    cell = {i: [] for i in range(1, 5)}

    # 5:1  anyone; a witness; seen or known
    t = cue(5, 1, "anyone")
    P.altar_out(t, group="s5.m51")
    cell[1].append(shape("m.f1", frame_svg(c1), t, z=8, group="s5.m51"))
    man = F.man()
    wx, wgy, wk = c1[0] + 62, c1[3] - 9, 1.1
    wb = _fig_box(man, wx, wgy, wk)
    cell[1].append(figure("m.witness", man, wx, wgy, wk, t, group="s5.m51"))
    cell[1].append(chip("m.c.witness", "a witness", c1[0] + 178, wb[1] + 2,
                        cue(5, 1, "a witness"), lead=(wx + 10, wb[1] + 16)))
    cell[1].append(chip("m.c.seen", "seen", c1[0] + 160, c1[1] + 100, cue(5, 1, "seen")))
    cell[1].append(chip("m.c.known", "known", c1[0] + 246, c1[1] + 100, cue(5, 1, "known")))

    # 5:2  the carcass, of three kinds
    t = cue(5, 2, "the carcass")
    dims(cell[1], t, LOW, group="s5.m52")
    cell[2].append(shape("m.f2", frame_svg(c2), t, z=8, group="s5.m52"))
    cell[2].append(chip("m.c.carcass", "the carcass", (c2[0] + c2[2]) / 2, c2[1] + 16, t,
                        group="s5.m52"))
    fx, cx_ = c2[0] + 62, c2[0] + 104
    kinds = (("unclean animal", "an unclean animal", F.wolf(), 0.55, 68),
             ("unclean livestock", "unclean livestock", F.donkey(), 0.36, 106),
             ("unclean creeping things", "unclean creeping things", F.small_snake(), 1.2, 144))
    for i, (said, word, parts, k, gdy) in enumerate(kinds):
        t = cue(5, 2, said)
        gy = c2[1] + gdy
        cell[2].append(figure(f"m.kind{i}", parts, fx, gy, k, t, ink_=DIM, group=f"s5.k{i}"))
        cell[2].append(chip(f"m.c.kind{i}", word, cx_, gy - 12, t, anchor="lm",
                            group=f"s5.k{i}"))

    # 5:3  he touches the uncleanness of man
    t = cue(5, 3, "touches")
    dims(cell[2], t, LOW, group="s5.m53")
    cell[3].append(shape("m.f3", frame_svg(c3), t, z=8, group="s5.m53"))
    tk, tgy = 1.1, c3[3] - 8
    tx, ux = c3[0] + 70, c3[0] + 124
    toucher, unclean = F.side_person(arms="reach"), F.man()
    ub = _fig_box(unclean, ux, tgy, tk)
    cell[3].append(figure("m.unclean", unclean, ux, tgy, tk, t, ink_=DIM, z=19, group="s5.m53"))
    cell[3].append(figure("m.toucher", toucher, tx, tgy, tk, t, group="s5.m53"))
    cell[3].append(chip("m.c.man", "the uncleanness of man", c3[0] + 226, ub[1] - 12,
                        cue(5, 3, "uncleanness of man"), lead=(ux + 3, ub[1] + 10)))

    # 5:4  he swears rashly: to do evil, to do good; an oath
    t = cue(5, 4, "swears")
    dims(cell[3], t, LOW, group="s5.m54")
    cell[4].append(shape("m.f4", frame_svg(c4), t, z=8, group="s5.m54"))
    sx, sgy, sk = c4[0] + 64, c4[3] - 8, 1.1
    sb = _fig_box(man, sx, sgy, sk)
    cell[4].append(figure("m.swearer", man, sx, sgy, sk, t, group="s5.m54"))
    mouth = (sx + 9, sb[1] + 20)
    cell[4].append(chip("m.c.evil", "to do evil", c4[0] + 196, c4[1] + 76,
                        cue(5, 4, "to do evil")))
    cell[4].append(chip("m.c.good", "to do good", c4[0] + 196, c4[1] + 116,
                        cue(5, 4, "to do good")))
    cell[4].append(chip("m.c.oath", "an oath", c4[0] + 170, c4[1] + 30, cue(5, 4, "an oath"),
                        lead=mouth))

    # 5:5  one of these; confess (out of the grid, toward the dock)
    t = cue(5, 5, "one of these")
    dims(cell[4], t, LOW, group="s5.m55")
    for i, b in CELLS.items():
        pulse_el(f"s5.m.p{i}", "bench", rect_pts(b[0] + 3, b[1] + 3, b[2] - 3, b[3] - 3), t,
                 group="s5.m55")
    t = cue(5, 5, "confess")
    mx, my = MID
    conf = chip("m.c.confess", "confess", mx, my, t, group="s5.conf")
    a, h = arrow_el("m.confess", [(mx + 40, my), (BX1 - 8, my)], t + 0.15, 0.8, width=3.6,
                    head=12)

    # 5:6  one guilty of 5:1-4 (the four cells); on "female", the animal set
    t = cue(5, 6, "bring")
    D.light(GUILTY, t, group="s5.guilty",
            link=[("bench", rect_pts(b[0] + 3, b[1] + 3, b[2] - 3, b[3] - 3), True)
                  for b in CELLS.values()])
    global CASE
    CASE = D.case_outline([GUILTY, "sin.rank3"], t + 0.7)
    t = cue(5, 6, "female")
    P.case_clear(t, group="s5.set56")
    P.altar_in(t, group="s5.set56")
    lamb, goat = F.sheep(lamb=True), F.goat(female=True)
    lx, gx = 105, 250
    t = cue(5, 6, "lamb")
    figure("pen.lamb", lamb, lx, P.PEN_G, 2.6, t, group="s5.lamb")
    D.current("sin.icon3:lamb", t, group="s5.lamb", how="steady")
    pulse_el("s5.pen.lamb.p", "bench", outline(lamb, lx, P.PEN_G, 2.6), t, group="s5.lamb")
    t = cue(5, 6, "goat")
    figure("pen.goat", goat, gx, P.PEN_G, 1.9, t, group="s5.goat")
    D.current("sin.icon3:female goat", t, group="s5.goat", how="steady")
    D.current("sin.rank3", t, group="s5.goat", how="steady")
    pulse_el("s5.pen.goat.p", "bench", outline(goat, gx, P.PEN_G, 1.9), t, group="s5.goat")
    chip("pen.female", "female", (lx + gx) / 2 - 2, P.PEN_G + 21, t + 0.45)


CASE = None


# ---- 5:7-10: the birds -----------------------------------------------------

def birds():
    global CASE
    dv = P.Dove()
    xs, xb = P.DOVE_X[1], P.DOVE_X[0]          # the sin dove (by the altar), the burnt one

    # 5:7  can't afford a lamb; turtledoves, pigeons; one for each offering
    t = cue(5, 7, "can't afford a lamb")
    P.case_clear(t, group="s5.c57")
    CASE.ev("out", t, 0.35, group="s5.c57")
    D.light("sin.who:can't afford a lamb", t, group="s5.c57")
    CASE = D.case_outline(["sin.who:can't afford a lamb", "sin.rank4", "sin.icon4:turtledove",
                           "sin.icon4:pigeon"], t + 0.6, group="s5.c57b")
    t = cue(5, 7, "turtledoves")
    ds = add(El("s5.dove.sin", "bench", dv.svg("all", xs), z=21))
    ds.ev("in", t, 0.5, group="s5.td")
    D.light("sin.icon4:turtledove", t, link=[("bench", dv.outline(xs), True)], group="s5.td")
    t = cue(5, 7, "pigeons")
    db = add(El("s5.dove.burnt", "bench", dv.svg("all", xb), z=21))
    db.ev("in", t, 0.5, group="s5.pg")
    D.light("sin.icon4:pigeon", t, link=[("bench", dv.outline(xb), True)], group="s5.pg")
    D.light("sin.rank4", t + 0.3, group="s5.pg")
    top = dv.ground - 70
    c_sin = chip("pen.c.sin", "sin offering", xs - 4, top, cue(5, 7, "sin offering"),
                 lead=(xs, top + 26))
    c_burnt = chip("pen.c.burnt", "burnt offering", xb, top, cue(5, 7, "burnt offering"),
                   lead=(xb, top + 26))

    # 5:8  to the priest; the sin dove first, to the bird bay; wring; not severed
    a = S["altar"]
    pr = P.priests_el("s5.priest58", [a[0] - 4], cue(5, 8, "priest"))
    t = cue(5, 8, "first")
    rel = (dv.bay_x - xs, dv.bay_g - dv.ground)
    glide(ds, t, B.arc_path((0, 0), rel, 0.45), 1.0, "the sin dove to the bird bay",
          "bench move", quad=True, group="s5.bay")
    c_sin.ev("out", t, 0.5, group="s5.bay")
    DP = dv.DP
    neck = traced_el("s5.bay.neck", "bench", [DP((8.4, 4.6)), DP((7.4, -0.6))], BLOOD, 3,
                     cue(5, 8, "wring"), 0.5, z=27)
    t = cue(5, 8, "sever")
    nd = chip("bay.c.notsev", "not severed", P.BAY[0] - 40, P.A_TOP - 92, t,
              lead=DP((8.0, 3.0)))

    # 5:9  the blood on the altar's side ("the altar's side" flies); drained at its base
    A = P.A_BODY
    t = cue(5, 9, "side")
    drops = "".join(f'<ellipse cx="{B.f2(A[2] - 7 + dx)}" cy="{B.f2(P.A_TOP + dy)}" rx="2.6" '
                    f'ry="3.6" fill="{B.rgb(BLOOD)}"/>'
                    for dx, dy in ((0, 16), (-3, 30), (1, 44), (-2, 58), (0, 72)))
    sp = shape("bay.drops", drops, t, z=27, dur=0.5)
    land = D.fly("the altar's side", (A[2] - 118, P.A_TOP + 40),
                 "sin.blood:the altar's side", t + 0.6)
    run = [(A[2] - 4, P.A_TOP + 76), (A[2] - 5, P.A_TOP + 100), (A[2] - 3, P.A_TOP + 124),
           (A[2] - 4, A[3] - 3)]
    rn = traced_el("s5.bay.run", "bench", run, BLOOD, 4.2, max(cue(5, 9, "drained"), land + 0.4),
                   0.8, z=27)
    t = cue(5, 9, "base")
    pool = shape("bay.pool", f'<ellipse cx="{B.f2(A[2] - 16)}" cy="{B.f2(A[3] + 3)}" rx="20" '
                             f'ry="4.5" fill="{B.rgb(BLOOD)}"/>', t, z=27, dur=0.5)

    # 5:10  the second for a burnt offering: onto the fire
    t = cue(5, 10, "second")
    outs([ds, neck, nd, sp, rn, pool], t, group="s5.second")
    t = cue(5, 10, "burnt offering")
    onto = (P.FIRE_XS[2] + 10 - xb, (dv.bay_g - 14) - dv.ground)
    L = glide(db, t, B.arc_path((0, 0), onto, 0.3), 1.1, "the burnt dove onto the fire",
              "bench move", quad=True, group="s5.burn510")
    c_burnt.ev("out", t, 0.5, group="s5.burn510")
    P.flare(t + 1.13, 1.3, 0.9, group="s5.flare510")
    t = cue(5, 10, "forgiven")
    if not E["col.sin.forgiven"].state(t)[0]:
        D.forgiven("sin", t)
    del L, pr


# ---- 5:11-13: the flour; the sin column filed --------------------------------

def flour():
    global CASE
    t = cue(5, 11, "can't afford two turtledoves")
    P.case_clear(t, regions=("bench", "strip"), group="s5.c511")
    CASE.ev("out", t, 0.35, group="s5.c511")
    D.light("sin.who:can't afford two turtledoves", t, group="s5.c511")
    CASE = D.case_outline(["sin.who:can't afford two turtledoves", "sin.rank5",
                           "sin.icon5:fine flour"], t + 0.6, group="s5.c511b")

    # the ephah in ten parts, its tenth filled
    mx0, mw, my0, mh = 24, 30, 300, 24
    mx1 = mx0 + 10 * mw
    meas = (f'<rect x="{mx0}" y="{my0}" width="{mx1 - mx0}" height="{mh}" rx="3" '
            f'fill="{B.rgb(mix(PANEL, SAND, .25))}" stroke="{B.rgb(SAND)}" stroke-width="1.6"/>'
            + "".join(f'<line x1="{mx0 + i * mw}" y1="{my0}" x2="{mx0 + i * mw}" '
                      f'y2="{my0 + mh}" stroke="{B.rgb(SAND)}" stroke-width="1.2"/>'
                      for i in range(1, 10))
            + f'<rect x="{mx1 - mw + 2}" y="{my0 + 2}" width="{mw - 4}" height="{mh - 4}" rx="2" '
              f'fill="{B.rgb(FLOUR)}"/>')
    t = cue(5, 11, "one tenth")
    m_el = shape("k.measure", meas, t, z=16, group="s5.tenth")
    c_tenth = chip("k.c.tenth", "one tenth", mx1 - mw / 2 - 10, my0 - 22, t + 0.15,
                   lead=(mx1 - mw / 2, my0), group="s5.tenth")
    # "a tenth of an ephah" (its rank line) on "ephah", one gesture with the flour
    D.light("sin.rank5", cue(5, 11, "ephah"), group="s5.ff")

    # the basket of fine flour (by the altar), the jar and the cup (not-marked)
    G = P.PEN_G
    bxx, bk_k = 268, 2.6
    btop = ART.supply_top("basket", G, bk_k)
    t = cue(5, 11, "fine flour")
    basket = shape("k.basket", ART.supply_svg("basket", bxx, G, bk_k), t, z=18, group="s5.ff")
    c_flour = chip("k.c.flour", "fine flour", bxx, G + 21, t, group="s5.ff")
    D.light("sin.icon5:fine flour", t, group="s5.ff",
            link=[("bench", ART.supply_outline("basket", bxx, G, bk_k), True)])
    jar, cup = F.jar(), F.cup()
    jx, jk, cx_, ck = 42, 2.4, 132, 4.0
    t = cue(5, 11, "no oil")
    j_el = shape("k.jar", ART.supply_svg("jar", jx, G, jk), t, z=18, group="s5.oil")
    c_oil = chip("k.c.oil", "oil", jx, G + 21, t, group="s5.oil")
    jb = _fig_box(jar, jx, G, jk)
    n_oil = P.not_el("s5.k.not.oil", "bench", ((jb[0] + jb[2]) / 2, (jb[1] + jb[3]) / 2), 33,
                     t + 0.45)
    t = cue(5, 11, "frankincense")
    cb = _fig_box(cup, cx_, G, ck)
    c_el = shape("k.cup", ART.supply_svg("cup", cx_, G, ck), t, z=18, group="s5.fr")
    c_fr = chip("k.c.fr", "frankincense", cx_ + 6, G + 21, t, group="s5.fr")
    n_fr = P.not_el("s5.k.not.fr", "bench", ((cb[0] + cb[2]) / 2, (cb[1] + cb[3]) / 2 - 4), 30,
                    t + 0.45)

    # 5:12  to the priest; his handful, the memorial portion; burned
    t = cue(5, 12, "bring")
    outs([m_el, c_tenth, j_el, c_oil, c_el, c_fr, n_oil, n_fr], t, group="s5.k512")
    px, pk = 168, 1.15
    pr = F.priest()
    pr_el = figure("k.priest", pr, px, G, pk, cue(5, 12, "priest"), z=17)
    palm = (bxx + 2, btop - 12)
    hat = (palm[0] + 30, palm[1] - 28)
    t = cue(5, 12, "handful")
    hand = shape("k.hand", hand_svg("cup", hat, 140, 3.0, arm=18), t, z=40, group="s5.hf",
                 how="lift", lift=-10)
    hp = shape("k.handful", ART.heap(palm[0] + 2, palm[1] + 4, 24, 10, FLOUR), t, z=41,
               group="s5.hf", how="lift", lift=-10)
    c_hf = chip("k.c.handful", "handful", bxx - 72, btop - 74, t + 0.3,
                lead=(palm[0] - 10, palm[1] - 4), group="s5.hf")
    c_mem = chip("k.c.mem", "memorial portion", bxx - 46, btop - 112,
                 cue(5, 12, "memorial portion"), lead=(palm[0] + 2, palm[1] - 18))
    t = cue(5, 12, "burn")
    to = (P.FIRE_XS[2] - (palm[0] + 2), (P.A_TOP - 8) - (palm[1] + 4))
    glide(hp, t, B.arc_path((0, 0), to, 0.3), 1.0, "the handful to the fire", "bench move",
          quad=True, group="s5.hf2")
    outs([hand, c_hf, c_mem], t, 0.5, group="s5.hf2")
    tf = t + 1.03
    P.flare(tf, 1.3, 0.8, group="s5.flare512")
    hp.ev("out", tf + 0.1, 0.6, group="s5.flare512")
    D.fly("a handful", (P.FIRE_XS[1] - 4, P.A_TOP - 96), "sin.burns:a handful", tf + 0.55,
          T_go=tf + 0.85)

    # 5:13  the priest; forgiven; the rest, the priest's ("the remaining flour" flies)
    pulse_el("s5.k.priest.p", "bench", outline(pr, px, G, pk), cue(5, 13, "priest"))
    D.forgiven("sin", cue(5, 13, "forgiven"))
    t = cue(5, 13, "rest")
    land = D.fly("the remaining flour", (bxx + 14, btop - 22), "sin.eaten:the remaining flour", t)
    # the sin column filed (its glide is short: the sin slot is next to the
    # dock); the workshop comes back before 5:14 ends, so 5:15 opens on it
    t_fv = land + 0.3
    P.case_clear(t_fv, regions=("bench", "strip"), group="fileview")
    CASE.ev("out", t_fv, 0.35, group="fileview")
    back = 0.6
    D.file_view("sin", t_fv, T_back=B.limit(5, 14) - back, hold=1.0, glide_dur=0.9,
                back_dur=back)
    del basket, c_flour, pr_el


# ---- 5:15-6:7: the trespass offering (board T) -------------------------------

def trespass():
    man = F.man()
    ram, scales, coins, priest = F.sheep(ram=True), F.scales(), F.coins(), F.priest()
    mb = _fig_box(man, *MAN)
    rb = _fig_box(ram, *RAM)
    sb = _fig_box(scales, *SCALES)
    cb = _fig_box(coins, *COINS)
    pb = _fig_box(priest, *PRIEST)
    man_line = outline(man, *MAN)
    ram_line = outline(ram, *RAM)

    def vfig(key, parts, spec, ink_=TEXT):
        x, gy, k = spec
        return add(El(k5(key), "bench", B.fig(parts, x, gy, k, ink_, PANEL), z=20, hidden0=True))

    # 5:15  a trespass: the board; the man; the tab; anyone; a ram; its value
    t = cue(5, 15, "trespass")
    P.altar_out(t, group="s5.t515")
    m_el = figure("t.man", man, MAN[0], MAN[1], MAN[2], t, group="s5.t515")
    P.place("tent", cue(5, 15, "holy things"))
    t_sw = cue(5, 15, "trespass offering")
    D.switch("trespass", t_sw)
    # "anyone" (said at 0.41) lifts once its column shows; the tab is named at
    # t_sw + 0.9, so its link pulse on the man waits 0.3 s more
    t = t_sw + 0.9 + 0.31
    D.light("trespass.by", t, link=[("bench", man_line, True)], group="s5.by")
    r_el = vfig("t.ram", ram, RAM)
    t = max(cue(5, 15, "ram"), t + 0.45 + 0.31)        # after the by-pulse
    r_el.ev("in", t, 0.6, group="s5.ram")
    c_ram = chip("t.c.ram", "ram", RAM[0], TG + 18, t, group="s5.ram")
    D.light("trespass.thing:ram", t, link=[("bench", ram_line, True)], group="s5.ram")
    s_el = vfig("t.scales", scales, SCALES, SILVER)
    t = cue(5, 15, "estimation")
    s_el.ev("in", t, 0.6, group="s5.est")
    c_est = chip("t.c.est", "estimation", SCALES[0], TG + 18, t, group="s5.est")
    c_el = vfig("t.coins", coins, COINS, SILVER)
    t = cue(5, 15, "silver")
    c_el.ev("in", t, 0.6, group="s5.silver")
    c_sil = chip("t.c.silver", "silver", COINS[0] + 6, TG + 18, t, group="s5.silver")
    land = D.fly("estimation in silver", (SCALES[0] + 8, cb[1] - 30), "trespass.thing:silver",
                 t + 0.55)
    t = max(cue(5, 15, "shekel of the sanctuary"), land + 0.4)
    c_shk = chip("t.c.shekel", "shekel of the sanctuary", (SCALES[0] + COINS[0]) / 2, TG + 47, t,
                 lead=(COINS[0] + 4, cb[3] + 2))

    # 5:16  restitution (five parts), a fifth part, to the priest; the ram; forgiven
    y0, y1 = BAR_Y
    t = cue(5, 16, "restitution")
    outs([c_ram, c_est, c_sil, c_shk], t, group="s5.r516")
    bar = shape("t.bar", bar_svg(BAR_X0, y0, y1), t, z=18, group="s5.r516", dur=0.6,
                how="lift", lift=8)
    c_rest = chip("t.c.rest", "restitution", (BAR_X0 + BAR_X1) / 2, y1 + 22, t + 0.3,
                  group="s5.r516")
    t = cue(5, 16, "fifth part")
    fifth = shape("t.fifth", bar_svg(BAR_X1, y0, y1, 1, fill=mix(PANEL, GOLD, .6)), t, z=18,
                  group="s5.fifth", dur=0.5, how="lift", lift=8)
    l15 = label_el("t.l.fifth", "1/5", (BAR_X1 + FIFTH_X1) / 2, (y0 + y1) / 2, 15, t + 0.35,
                   col=TEXT, group="s5.fifth")
    p_el = vfig("t.priest", priest, PRIEST)
    t = cue(5, 16, "priest")
    p_el.ev("in", t, 0.6, group="s5.pr516")
    a_bp = arrow_el("t.a.bp", [(FIFTH_X1 + 6, (y0 + y1) / 2), (pb[0] - 4, TG - 6)], t + 0.35, 0.7)
    t = cue(5, 16, "ram")
    D.light("trespass.thing:ram", t, link=[("bench", ram_line, True)], group="s5.ram516")
    ry = rb[1] + 22
    a_rp = arrow_el("t.a.rp", [(rb[2] + 8, ry), (pb[0] - 6, ry)], t + 0.35, 0.7)
    D.forgiven("trespass", cue(5, 16, "forgiven"))

    # 5:17  anyone (a sin he didn't know): the value set dims; didn't know; guilty
    t = cue(5, 17, "anyone")
    vset = [r_el, s_el, c_el, p_el, *a_rp]
    dims(vset, t, LOW, group="s5.c517")
    outs([bar, fifth, l15, c_rest, *a_bp], t, group="s5.c517")
    D.light("trespass.by", t, link=[("bench", man_line, True)], group="s5.c517")
    cx_ = mb[2] + 16
    c_dk = chip("t.c.dk", "didn’t know", cx_, mb[1] + 8, cue(5, 17, "didn't know"),
                anchor="lm")
    c_gl = chip("t.c.guilty", "guilty", cx_, mb[1] + 44, cue(5, 17, "guilty"), anchor="lm")

    # 5:18-19  the ram, by estimation, to the priest; didn't know; forgiven; guilty
    t = cue(5, 18, "ram")
    dims([r_el], t, 1.0, group="s5.ram518")
    D.light("trespass.thing:ram", t, link=[("bench", ram_line, True)], group="s5.ram518")
    t = cue(5, 18, "estimation")
    dims([s_el], t, 1.0, group="s5.est518")
    c_est2 = chip("t.c.est2", "estimation", SCALES[0], TG + 18, t, group="s5.est518")
    t = cue(5, 18, "priest")
    dims([p_el, *a_rp], t, 1.0, group="s5.pr518")
    pulse_el("s5.t.dk.p", "bench", B.box_pts(c_dk.texts[0][0], 3), cue(5, 18, "didn't know"))
    D.forgiven("trespass", cue(5, 18, "forgiven"))
    pulse_el("s5.t.gl.p", "bench", B.box_pts(c_gl.texts[0][0], 3), cue(5, 19, "guilty"))

    # 6:1  the formula: the bench clears to the man
    t = at(6, 1, 0.2)
    outs([r_el, s_el, c_el, p_el, *a_rp, c_dk, c_gl, c_est2], t, 0.8, group="s5.c61")

    # 6:2-3  anyone; the neighbor; the six wrongs
    t = cue(6, 2, "anyone")
    D.light("trespass.by", t, link=[("bench", man_line, True)], group="s5.by62")
    nb_el = figure("t.neighbor", man, NEIGHBOR[0], NEIGHBOR[1], NEIGHBOR[2],
                   cue(6, 2, "neighbor"), group="s5.nb")
    nbb = _fig_box(man, *NEIGHBOR)
    c_nb = chip("t.c.nb", "neighbor", NEIGHBOR[0], nbb[1] - 16, cue(6, 2, "neighbor"),
                group="s5.nb")
    wrongs = (("deposit", "deposit", (6, 2, "deposit")),
              ("bargain", "bargain", (6, 2, "bargain")),
              ("robbery", "robbery", (6, 2, "robbery")),
              ("oppressed", "oppressed his neighbor", (6, 2, "oppressed his neighbor")),
              ("lost", "that which was lost", (6, 3, "that which was lost")),
              ("lie", "swearing to a lie", (6, 3, "swearing to a lie")))
    wch = {}
    for i, (key, word, (c, v, said)) in enumerate(wrongs):
        wch[key] = chip(f"t.w.{key}", word, WRONG_X, WRONG_Y[i], cue(c, v, said))

    # 6:4-5  each restored to the neighbor (a return arrow)
    rets = {}
    order = (("robbery", (6, 4, "robbery")), ("oppressed", (6, 4, "oppression")),
             ("deposit", (6, 4, "deposit")), ("lost", (6, 4, "lost thing")),
             ("lie", (6, 5, "sworn")))
    keys = [w[0] for w in wrongs]
    for key, (c, v, said) in order:
        i = keys.index(key)
        box = wch[key].texts[0][0]
        rets[key] = arrow_el(f"t.ret.{key}", [(box[2] + 6, WRONG_Y[i]),
                                               (nbb[0] - 4, nbb[1] + 22 + i * 13)],
                             cue(c, v, said), 0.7, width=2.6, head=10)

    # 6:5  in full, a fifth more, to whom it belongs, in the day
    # (the bar in the bench's middle: the wrongs have gone back to the neighbor)
    t = cue(6, 5, "in full")
    outs([*wch.values(), *[e for a in rets.values() for e in a], c_nb], t, group="s5.f65")
    z0, z1 = 396, 426
    bar2 = shape("t.bar2", bar_svg(BAR_X0, z0, z1), t, z=18, group="s5.f65", dur=0.6,
                 how="lift", lift=8)
    c_full = chip("t.c.full", "in full", (BAR_X0 + BAR_X1) / 2, z1 + 22, t + 0.3,
                  group="s5.f65")
    t = cue(6, 5, "fifth")
    fifth2 = shape("t.fifth2", bar_svg(BAR_X1, z0, z1, 1, fill=mix(PANEL, GOLD, .6)), t, z=18,
                   group="s5.fifth65", dur=0.5, how="lift", lift=8)
    l15b = label_el("t.l.fifth2", "1/5", (BAR_X1 + FIFTH_X1) / 2, (z0 + z1) / 2, 15, t + 0.35,
                    group="s5.fifth65")
    t = cue(6, 5, "belongs")
    a_own = arrow_el("t.a.own", [(FIFTH_X1 + 6, (z0 + z1) / 2), (nbb[0] - 4, nbb[1] + 30)],
                     t, 0.7)
    c_own = chip("t.c.own", "to whom it belongs", (FIFTH_X1 + nbb[0]) / 2 - 6, z0 - 22, t + 0.3)
    c_day = chip("t.c.day", "in the day", (FIFTH_X1 + nbb[0]) / 2 - 22, z1 + 52,
                 cue(6, 5, "day"))

    # 6:6  his trespass offering: the ram, by estimation, to the priest
    t = cue(6, 6, "trespass offering")
    outs([bar2, fifth2, l15b, c_full, *a_own, c_own, c_day, nb_el], t, group="s5.c66")
    t = cue(6, 6, "ram")
    r_el.ev("in", t, 0.6, group="s5.ram66")
    D.light("trespass.thing:ram", t, link=[("bench", ram_line, True)], group="s5.ram66")
    t = cue(6, 6, "estimation")
    s_el.ev("in", t, 0.6, group="s5.est66")
    c_est3 = chip("t.c.est3", "estimation", SCALES[0], TG + 18, t, group="s5.est66")
    t = cue(6, 6, "priest")
    p_el.ev("in", t, fit(t, 0.5), group="s5.pr66")
    a_rp2 = arrow_el("t.a.rp2", [(rb[2] + 8, ry), (pb[0] - 6, ry)], t, fit(t, 0.4))

    # 6:7  before Yahweh: the altar back, priests at the strip's altar; forgiven;
    # the trespass column filed
    t = cue(6, 7, "before Yahweh")
    outs([r_el, s_el, p_el, *a_rp2, c_est3, m_el], t, group="s5.c67")
    P.altar_in(t, group="s5.c67")
    a = S["altar"]
    P.priests_el("s5.priests67", [a[0] - 14, a[0] + 8], t)
    E["s5.priests67"].events[-1]["group"] = "s5.c67"
    t = cue(6, 7, "forgiven")
    D.forgiven("trespass", t)
    t_fv = t + 0.9
    P.section_clear(t_fv, group="fileview")
    D.file_view("trespass", t_fv, T_back=B.limit(6, 7) - 1.0)
    del c_el
