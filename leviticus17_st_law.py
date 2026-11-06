"""Stations M (causes) and T (trespass) of the Leviticus 1-7 pictures.

Each is a 1024 x 576 card on the world sheet (corner in
leviticus17_spec.STATIONS: M at (2960, 100), above the table; T at
(4080, 100), above it to the right), drawn through leviticus17_stations'
Station API. Their words are offerings.py's (CAUSES, WRONGS) or the WEB's
own, four at most; their figures are svg_figures'.

M, the causes of 5:1-6: a 2 x 2 of the four things "hidden from him",
and the confession that follows them.
- shots: "" (the card), "c1".."c4" (one cell each, s 1.75);
- cell 1, 5:1: M.witness (a man, "a witness"), M.seen, M.known;
- cell 2, 5:2: M.carcass ("the carcass", the cell's word), then a dim
  figure a row with its CAUSES label: M.unclean_animal (a wolf, the wild
  beast), M.unclean_livestock (a donkey, the unclean beast of the herd),
  M.creeping_things (a small snake);
- cell 3, 5:3: M.uncleanness_of_man (a man reaching to touch a dim man);
- cell 4, 5:4: M.evil, M.good, M.oath (the man who swears comes in with
  the first of them);
- M.cell1..M.cell4 and M.cells (all four: the pulse on "one of these"),
  outlines only; M.confess, 5:5 (an arrow traced out of the grid, down
  toward the table's sin offering).

T, the trespass offering of 5:14-6:7:
- shots: "" (the card), "bar" (the restitution bar and the priest, s 1.65),
  "wrongs" (the man, the six wrongs and his neighbor, s 1.32);
- the top band, 5:15-18: T.estimation (the balance, "estimation") and
  T.silver (coins, "silver"), the balance coming in with the first of the
  two; T.shekel ("shekel of the sanctuary"); T.ram (svg_figures.sheep(ram=True), "ram"), T.priest (the priest, "priest"),
  T.ram_to_priest (an arrow, ram to priest: 5:18, 6:6);
- the bar, 5:16 and 6:5: T.bar (five parts grown, "restitution"), T.fifth
  (its sixth part "1/5", grown on), T.to_priest (an arrow, bar to priest),
  T.in_full (a bracket under the five parts), T.owner (an arrow down to
  the neighbor, "to whom it belongs"), T.in_the_day;
- the bottom band, 5:17 and 6:2-5: T.man, T.neighbor (two man(),
  "neighbor"), the six wrongs of offerings.WRONGS as T.deposit,
  T.bargain, T.robbery, T.oppressed, T.lost and T.lie, each with its
  return arrow to the neighbor, T.return:<the same key>; T.wrongs (the six,
  an outline only); T.didnt_know and T.guilty, chips by the man that are
  this verse's only (5:17 is a sin he didn't know; 6:2 is not).
The priest stands once any of T.priest, T.to_priest or T.ram_to_priest
is lit. Every arrow persists once drawn, as everything else does.
"""

import offerings as OF
import svg_figures as F
from leviticus17_stations import (CH, CW, GOLD, PANEL, SAND, SAND_DIM,
                                  SILVER, TEXT, TEXT_DIM, Station, Target,
                                  appear, mix, pts_str, rect_pts, rgb,
                                  t_s, trace, union_box)
from svg_map_camera import EASE
from svg_surface import _fmt

DIM = mix(PANEL, TEXT, .55)            # a figure that is spoken of, not there
ARROW = SAND
CAUSE = {e.key: e.label for e in OF.CAUSES}
WRONG = {e.key: e.label for e in OF.WRONGS}


def arrow(pts, col, width, t, dur=0.8, head=11):
    """A line traced on at t (or there, t None) with its head coming in as
    the line arrives."""
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    dx, dy = x1 - x0, y1 - y0
    L = max(1e-6, (dx * dx + dy * dy) ** 0.5)
    ux, uy = dx / L, dy / L
    hd = [(x1 - ux * head - uy * head * .55, y1 - uy * head + ux * head * .55),
          (x1, y1),
          (x1 - ux * head + uy * head * .55, y1 - uy * head - ux * head * .55)]
    line = list(pts[:-1]) + [(x1 - ux * 3, y1 - uy * 3)]
    tip = (f'<polygon points="{pts_str(hd)}" fill="{rgb(col)}" '
           f'stroke="{rgb(col)}" stroke-width="1" stroke-linejoin="round"/>')
    return (trace(line, col, width, t, dur)
            + appear(tip, None if t is None else t + dur * 0.85, "fade", 0.2))


def grow_x(inner, t, x0, dur=0.8):
    """`inner` grown out to the right from x0 at t (there, t None)."""
    if t is None:
        return inner
    return (f'<g opacity="0"><set attributeName="opacity" to="1" '
            f'begin="{t_s(t)}"/><g transform="translate({_fmt(x0)} 0)">'
            f'<g transform="scale(0.02 1)"><animateTransform '
            f'attributeName="transform" type="scale" values="0.02 1;1 1" '
            f'begin="{t_s(t)}" dur="{dur:.2f}s" fill="freeze" '
            f'calcMode="spline" keyTimes="0;1" keySplines="{EASE}"/>'
            f'<g transform="translate({_fmt(-x0)} 0)">{inner}</g></g></g></g>')


def _first(ctx, keys):
    """None if any of keys was lit before this file, else the first light
    time of them here, else False (not drawn)."""
    if any(k in ctx.before for k in keys):
        return None
    ts = [ctx.lit[k] for k in keys if k in ctx.lit]
    return min(ts) if ts else False


def _fig_box(parts, x, gy, s, flip=1):
    x0, x1, y0, y1 = F.bbox((parts, 0))
    if flip < 0:
        x0, x1 = -x1, -x0
    return (x + x0 * s, gy - y1 * s, x + x1 * s, gy - y0 * s)


# ---------------------------------------------------------------------------
# M: the causes (5:1-6)
# ---------------------------------------------------------------------------

M_GAP, M_PAD = 14, 20
M_CW = (860 - M_PAD - M_GAP) / 2                     # 413
M_CH = (CH - 2 * M_PAD - M_GAP) / 2                  # 261
M_CELLS = {}
for _i, (_cx, _cy) in enumerate(((0, 0), (1, 0), (0, 1), (1, 1))):
    _x0 = M_PAD + _cx * (M_CW + M_GAP)
    _y0 = M_PAD + _cy * (M_CH + M_GAP)
    M_CELLS[_i + 1] = (_x0, _y0, _x0 + M_CW, _y0 + M_CH)
del _i, _cx, _cy, _x0, _y0
M_ROWS = (125, 190, 255)                             # cell 2's ground lines
M_FIG_X = 545
M_CHIP_X = 622                                       # cell 2's chips, left aligned
CONFESS_X = (M_CELLS[2][2] + CW - 20) / 2            # 936
M_SWEAR = (560, 540, 1.7)                            # cell 4's man


class Causes(Station):
    key = "M"

    def shots(self):
        out = {"": (1.0, CW / 2, CH / 2)}
        for i, (x0, y0, x1, y1) in M_CELLS.items():
            out[f"c{i}"] = self.clamp_shot(1.75, (x0 + x1) / 2, (y0 + y1) / 2)
        return out

    def base(self, ctx):
        out = [self.card()]
        for x0, y0, x1, y1 in M_CELLS.values():
            out.append(f'<rect x="{_fmt(x0)}" y="{_fmt(y0)}" width="{_fmt(x1 - x0)}" '
                       f'height="{_fmt(y1 - y0)}" rx="8" fill="none" '
                       f'stroke="{rgb(mix(PANEL, SAND_DIM, .7))}" stroke-width="1.4"/>')
        # cell 4's man swears: there with the first of its words
        t = _first(ctx, ("M.evil", "M.good", "M.oath"))
        if t is not False:
            x, gy, s = M_SWEAR
            out.append(appear(ctx.figure(F.man(), x, gy, s, TEXT, PANEL), t))
        return "".join(out)

    def targets(self, ctx):
        T = {}
        for i, b in M_CELLS.items():
            T[f"M.cell{i}"] = Target(f"M.cell{i}", outline=[(rect_pts(
                b[0] + 3, b[1] + 3, b[2] - 3, b[3] - 3), True)])
        T["M.cells"] = Target("M.cells", outline=[o for i in M_CELLS
                                                  for o in T[f"M.cell{i}"].outline])

        # cell 1 (5:1): the witness, what he has seen or known
        wx, wgy, ws = 135, 262, 1.95
        man = F.man()
        wb = _fig_box(man, wx, wgy, ws)

        def witness(c, t):
            return (appear(c.figure(man, wx, wgy, ws, TEXT, PANEL), t)
                    + c.chip("M.witness", CAUSE["witness"], (300, 105),
                             lead=(wx + 20, wb[1] + 42), t=t))
        T["M.witness"] = Target("M.witness", box=wb, draw=witness,
                                outline=[(F.outline(man, wx, wgy, ws), True)])
        for key, xy in (("seen", (262, 172)), ("known", (338, 172))):
            T[f"M.{key}"] = Target(
                f"M.{key}", box=(xy[0] - 34, xy[1] - 14, xy[0] + 34, xy[1] + 14),
                draw=lambda c, t, key=key, xy=xy: c.chip(f"M.{key}", CAUSE[key], xy, t=t))

        # cell 2 (5:2): the carcass, of three kinds
        c2 = M_CELLS[2]
        hx = (c2[0] + c2[2]) / 2
        T["M.carcass"] = Target(
            "M.carcass", box=(hx - 50, 36, hx + 50, 60),
            draw=lambda c, t: c.label("M.carcass", CAUSE["carcass"], (hx, 48), 17,
                                      TEXT, "mm", italic=True, t=t))
        kinds = (("unclean_animal", F.wolf(), 1.0), ("unclean_livestock", F.donkey(), 0.6),
                 ("creeping_things", F.small_snake(), 1.6))
        for (key, parts, s), gy in zip(kinds, M_ROWS):
            fb = _fig_box(parts, M_FIG_X, gy, s)
            cy = gy - min(22, (fb[3] - fb[1]) / 2)

            def draw(c, t, key=key, parts=parts, s=s, gy=gy, cy=cy):
                return (appear(c.figure(parts, M_FIG_X, gy, s, DIM, PANEL), t)
                        + c.chip(f"M.{key}", CAUSE[key], (M_CHIP_X, cy), anchor="lm", t=t))
            T[f"M.{key}"] = Target(f"M.{key}", box=fb, draw=draw,
                                   outline=[(F.outline(parts, M_FIG_X, gy, s), True)])

        # cell 3 (5:3): he touches the uncleanness of man
        tx, ux, ugy, us = 165, 238, 540, 1.7
        toucher = F.side_person(arms="reach")
        unclean = F.man()
        ub = _fig_box(unclean, ux, ugy, us)
        tb = _fig_box(toucher, tx, ugy, us)

        def touch(c, t):
            figs = (c.figure(unclean, ux, ugy, us, DIM, PANEL)
                    + c.figure(toucher, tx, ugy, us, TEXT, PANEL))
            return (appear(figs, t)
                    + c.chip("M.uncleanness_of_man", CAUSE["uncleanness_of_man"],
                             (226, 336), lead=(ux + 4, ub[1] + 6), t=t))
        T["M.uncleanness_of_man"] = Target(
            "M.uncleanness_of_man", box=union_box([ub, tb]), draw=touch,
            outline=[(F.outline(unclean, ux, ugy, us), True)])

        # cell 4 (5:4): the rash oath, to do evil or to do good
        sx, sgy, ss = M_SWEAR
        sb = _fig_box(F.man(), sx, sgy, ss)
        mouth = (sx + 12, sb[1] + 30)
        for key, xy, lead in (("oath", (680, 368), mouth),
                              ("evil", (700, 438), None), ("good", (700, 488), None)):
            T[f"M.{key}"] = Target(
                f"M.{key}", box=(xy[0] - 50, xy[1] - 14, xy[0] + 50, xy[1] + 14),
                draw=lambda c, t, key=key, xy=xy, lead=lead: c.chip(
                    f"M.{key}", CAUSE[key], xy, lead=lead, t=t))

        # 5:5: he confesses: out of the grid, down toward the table
        g = M_CELLS[2][2] + 4
        path = [(g, CH / 2), (CONFESS_X, CH / 2), (CONFESS_X, CH - 46)]

        def confess(c, t):
            return (arrow(path, ARROW, 4, t, 1.0, head=14)
                    + c.chip("M.confess", "confess", (CONFESS_X, CH / 2 - 40),
                             t=t))
        T["M.confess"] = Target("M.confess", box=(g, CH / 2 - 60, CW - 20, CH - 40),
                                draw=confess, outline=[(path, False)])
        return T


# ---------------------------------------------------------------------------
# T: the trespass offering (5:14-6:7)
# ---------------------------------------------------------------------------

TG = 245                                 # the top band's ground
SCALES = (110, TG, 2.2)
COINS = (195, TG, 3.0)
RAM = (310, TG, 2.6)
PRIEST = (520, TG, 1.9)
BAR_X0, BAR_PART, BAR_Y = 630, 56, (150, 186)
BAR_X1 = BAR_X0 + 5 * BAR_PART           # 910: the five parts
FIFTH_X1 = BAR_X1 + BAR_PART             # 966: and the fifth
BG_ = 556                                # the bottom band's ground
MAN = (70, BG_, 2.0)
NEIGHBOR = (680, BG_, 2.0)
WRONG_X = 300
WRONG_Y = [352 + 38 * i for i in range(6)]
WRONG_KEYS = [e.key for e in OF.WRONGS]


def _row_plate(key):
    """A wrong's chip plate, measured as ctx.chip draws it."""
    from svg_vocab import text_w
    w = text_w(WRONG[key], 16)
    y = WRONG_Y[WRONG_KEYS.index(key)]
    return (WRONG_X - w / 2 - 7, y - 13, WRONG_X + w / 2 + 7, y + 13)


class Trespass(Station):
    key = "T"
    VERSE_LOCAL = ("T.didnt_know", "T.guilty")

    def shots(self):
        return {"": (1.0, CW / 2, CH / 2),
                "bar": self.clamp_shot(1.65, 714, 175),
                "wrongs": self.clamp_shot(1.32, 415, 363)}

    def base(self, ctx):
        out = [self.card()]
        # the balance: there with the first of "estimation" and "silver"
        t = _first(ctx, ("T.estimation", "T.silver"))
        if t is not False:
            out.append(appear(ctx.figure(F.scales(), *SCALES, SILVER, PANEL), t))
        t = _first(ctx, ("T.priest", "T.to_priest", "T.ram_to_priest"))
        if t is not False:
            x, gy, s = PRIEST
            out.append(appear(ctx.figure(F.priest(), x, gy, s, TEXT, PANEL), t)
                       + ctx.chip("T.priest", "priest", (x, gy + 24), t=t))
        return "".join(out)

    def targets(self, ctx):
        T = {}
        # -- the top band: the ram, its value in silver, the priest -------
        scales, coins = F.scales(), F.coins()
        sb = _fig_box(scales, *SCALES)
        cb = _fig_box(coins, *COINS)

        def silver(c, t):
            return (appear(c.figure(coins, *COINS, SILVER, PANEL), t)
                    + c.chip("T.silver", "silver", (COINS[0] + 5, TG + 24), t=t))
        T["T.silver"] = Target("T.silver", box=cb, draw=silver,
                               outline=[(rect_pts(cb[0] - 6, cb[1] - 6, cb[2] + 6, TG + 4), True)])
        T["T.estimation"] = Target(
            "T.estimation", box=sb,
            outline=[(rect_pts(sb[0] - 6, sb[1] - 6, sb[2] + 6, TG + 4), True)],
            draw=lambda c, t: c.chip("T.estimation", "estimation", (SCALES[0] - 10, TG + 24),
                                     t=t))
        T["T.shekel"] = Target(
            "T.shekel", box=(62, 287, 238, 313),
            draw=lambda c, t: c.chip("T.shekel", "shekel of the sanctuary", (150, TG + 55),
                                     t=t))
        ram = F.sheep(ram=True)
        rb = _fig_box(ram, *RAM)

        def ram_draw(c, t):
            return (appear(c.figure(ram, *RAM, TEXT, PANEL), t)
                    + c.chip("T.ram", "ram", (RAM[0] + 6, TG + 24), t=t))
        T["T.ram"] = Target("T.ram", box=rb, draw=ram_draw,
                            outline=[(F.outline(ram, *RAM), True)])
        pb = _fig_box(F.priest(), *PRIEST)
        T["T.priest"] = Target("T.priest", box=pb,
                               outline=[(F.outline(F.priest(), *PRIEST), True)])
        rp = [(rb[2] + 8, 186), (pb[0] - 6, 186)]
        T["T.ram_to_priest"] = Target("T.ram_to_priest", outline=[(rp, False)],
                                      draw=lambda c, t: arrow(rp, ARROW, 3.5, t, 0.6))

        # -- the bar: restitution, and a fifth part added to it -----------
        y0, y1 = BAR_Y
        silver_fill = mix(PANEL, SILVER, .5)

        def bar(c, t):
            parts = "".join(
                f'<rect x="{_fmt(BAR_X0 + i * BAR_PART)}" y="{y0}" width="{BAR_PART}" '
                f'height="{y1 - y0}" rx="3" fill="{rgb(silver_fill)}" '
                f'stroke="{rgb(TEXT)}" stroke-width="1.4"/>' for i in range(5))
            return (grow_x(parts, t, BAR_X0, 1.0)
                    + c.chip("T.bar", "restitution", ((BAR_X0 + BAR_X1) / 2, 122), t=t))
        T["T.bar"] = Target("T.bar", box=(BAR_X0, y0, BAR_X1, y1), draw=bar,
                            outline=[(rect_pts(BAR_X0 - 3, y0 - 3, BAR_X1 + 3, y1 + 3), True)])

        def fifth(c, t):
            part = (f'<rect x="{BAR_X1}" y="{y0}" width="{BAR_PART}" height="{y1 - y0}" '
                    f'rx="3" fill="{rgb(mix(PANEL, GOLD, .6))}" stroke="{rgb(TEXT)}" '
                    f'stroke-width="1.4"/>')
            return (grow_x(part, t, BAR_X1, 0.7)
                    + c.label("T.fifth", "1/5", ((BAR_X1 + FIFTH_X1) / 2, (y0 + y1) / 2), 17,
                              TEXT, "mm", bold=True, t=None if t is None else t + 0.5))
        T["T.fifth"] = Target("T.fifth", box=(BAR_X1, y0, FIFTH_X1, y1), draw=fifth,
                              outline=[(rect_pts(BAR_X1 - 2, y0 - 5, FIFTH_X1 + 5, y1 + 5), True)])
        bp = [(BAR_X0 - 8, (y0 + y1) / 2), (pb[2] + 8, (y0 + y1) / 2)]
        T["T.to_priest"] = Target("T.to_priest", outline=[(bp, False)],
                                  draw=lambda c, t: arrow(bp, ARROW, 3.5, t, 0.6))
        br = [(BAR_X0 + 2, y1 + 6), (BAR_X0 + 2, y1 + 12), (BAR_X1 - 2, y1 + 12),
              (BAR_X1 - 2, y1 + 6)]
        T["T.in_full"] = Target(
            "T.in_full", box=(BAR_X0, y1 + 4, BAR_X1, y1 + 50), outline=[(br, False)],
            draw=lambda c, t: trace(br, TEXT_DIM, 2, t, 0.6)
            + c.chip("T.in_full", "in full", ((BAR_X0 + BAR_X1) / 2, y1 + 36),
                     t=None if t is None else t + 0.3))
        nb = _fig_box(F.man(), *NEIGHBOR)
        op = [(FIFTH_X1 - 16, y1 + 6), (nb[2] - 12, nb[1] - 22)]

        def owner(c, t):
            return (arrow(op, ARROW, 3.5, t, 0.9)
                    + c.chip("T.owner", "to whom it belongs", (830, 330),
                             t=None if t is None else t + 0.4))
        T["T.owner"] = Target("T.owner", box=(op[1][0], op[0][1], 1004, op[1][1]),
                              outline=[(op, False)], draw=owner)
        T["T.in_the_day"] = Target(
            "T.in_the_day", box=(708, 249, 792, 275),
            draw=lambda c, t: c.chip("T.in_the_day", "in the day",
                                     (750, y1 + 76), t=t))

        # -- the bottom band: the man, the wrongs, the neighbor ------------
        man = F.man()
        mb = _fig_box(man, *MAN)
        T["T.man"] = Target("T.man", box=mb, outline=[(F.outline(man, *MAN), True)],
                            draw=lambda c, t: appear(c.figure(man, *MAN, TEXT, PANEL), t))

        def neighbor(c, t):
            return (appear(c.figure(man, *NEIGHBOR, TEXT, PANEL), t)
                    + c.chip("T.neighbor", "neighbor", (nb[2] + 42, BG_ - 86), t=t))
        T["T.neighbor"] = Target("T.neighbor", box=nb, draw=neighbor,
                                 outline=[(F.outline(man, *NEIGHBOR), True)])
        T["T.didnt_know"] = Target(
            "T.didnt_know", box=(116, 330, 214, 356),
            draw=lambda c, t: c.chip("T.didnt_know", "didn’t know", (165, 343), t=t))
        T["T.guilty"] = Target(
            "T.guilty", box=(123, 370, 177, 396),
            draw=lambda c, t: c.chip("T.guilty", "guilty", (150, 383), t=t))
        plates = {}
        for i, key in enumerate(WRONG_KEYS):
            y = WRONG_Y[i]
            pl = _row_plate(key)
            plates[key] = pl
            T[f"T.{key}"] = Target(
                f"T.{key}", box=pl, outline=[(rect_pts(pl[0] - 3, pl[1] - 3, pl[2] + 3,
                                                       pl[3] + 3), True)],
                draw=lambda c, t, key=key, y=y: c.chip(f"T.{key}", WRONG[key], (WRONG_X, y),
                                                       t=t))
            ret = [(pl[2] + 6, y), (nb[0] + 4, 412 + i * 16)]
            T[f"T.return:{key}"] = Target(
                f"T.return:{key}", outline=[(ret, False)],
                draw=lambda c, t, ret=ret: arrow(ret, ARROW, 3, t, 0.7))
        T["T.wrongs"] = Target("T.wrongs", outline=[o for k in WRONG_KEYS
                                                    for o in T[f"T.{k}"].outline])
        return T


def stations():
    return [Causes(), Trespass()]
