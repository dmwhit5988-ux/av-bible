"""Stations D (peace law), S (shares and bans) and L (Sinai) of the
Leviticus 1-7 pictures.

Each is a 1024 x 576 card on the world sheet (corner in
leviticus17_spec.STATIONS: D at (2960, 772), right of M; S at (4080, 772),
right of T; L at (-560, 100), far outside the camp to the west), drawn in
its own card px with leviticus17_stations' Station API. Facts come from
offerings.py's boards (BREADS, DAYS, CAUSES, PENALTIES, SINAI, VESSELS),
figures from svg_figures, the not-mark from svg_vocab.not_mark_points.
Every word is a WEB word, four at most; nothing is drawn before its target
is lit; everything plays once and holds.

D, the peace law (7:11-21). Shots "", "breads", "days", "split".
- The bread rack (top left): D.shelf (two shelves), the four breads of
  offerings.BREADS, each a bread() with its label: D.cakes ("unleavened
  cakes"), D.wafers ("unleavened wafers"), D.oil_cakes ("cakes mixed with
  oil"), D.leavened ("leavened bread"); D.breads (all four at once);
  D.thanksgiving (a bracket over the rack with its chip).
- The heave (7:14): D.priest (priest(), arms up, right of the rack),
  D.sprinkles ("sprinkles the blood", and the priest if he isn't there),
  D.heave ("heave offering"). Verb "move" on D.heave: one of each bread
  rises off the shelf at the beat's "show" cue (else at D.heave's light, else
  on arrival) and goes up into the priest's hands on the cue. Lit with no
  "move" in its verse, the four rise and stay over the shelf. From the next
  verse they are in his hands.
- The day strip (top right, offerings.DAYS): D.day1 (the column "day 1"
  and the "thanksgiving" bar grown across it), D.morning (the tick at its
  end, "until the morning"), D.vow ("a vow") and D.freewill ("a freewill
  offering"), each a bar a day long, D.day2 ("day 2": both bars grown on
  through it), D.day3 ("day 3"), D.fire3 (a flame in day 3, "burned with
  fire"), D.eat3 (a dish of meat in day 3; verb "not" marks it, and lit
  with no "not" it is marked anyway), D.not_accepted ("not be accepted"),
  D.abomination ("an abomination").
- The split (bottom): D.split (the meat, "the meat"), D.unclean (a
  flame, "unclean"), D.clean (four people, "clean"). Lit, each of the last
  two sends a token of the meat to it; verb "move" on either times that
  token instead. D.cut_off (one figure slides once from the group, "cut
  off"), D.uncleanness_of_man and D.unclean_animal (CAUSES' words, leaders
  to that figure).

S, shares and bans (7:8-10, 22-27; 3:17). Shots "", "shares", "bans".
- The shares (top): S.skin (an ox, its hide traced, "the skin", an arrow
  to the priest), S.priest (priest(), "the priest"), S.oven,
  S.pan, S.griddle (cookware, each with its name), S.baked (the arrow from them to
  the priest, and any of the three not yet there), S.mixed ("mixed with
  oil"), S.dry ("dry"), S.sons (four priests, "sons of Aaron", the
  arrow to them). S.skin and S.baked bring the priest in if he isn't there.
- The bans (bottom): S.fat and S.blood (each row's thing and word; verb
  "not" marks it, and lit with no "not" it is marked anyway), S.ox, S.sheep,
  S.goat ("bull", "sheep", "goat"), S.no_eat (the fat of what dies or is
  torn, under a not-mark), S.died ("dies of itself"), S.torn ("torn"),
  S.service (an arrow to "other service"), S.cut_off_fat, S.dove ("bird"),
  S.animal ("animal", a goat), S.dwellings (tent(), "dwellings"),
  S.cut_off_blood.

L, Sinai (7:38). Shot "".
- L.mountain (mountain(), grown up from its foot), L.mount ("Mount Sinai",
  and the mountain if it isn't there), L.wilderness (the ground traced,
  "wilderness of Sinai"), L.moses (man() with his staff, "Moses").

Verbs beyond light, pulse and current: "not" on any target (the not-mark
traced over it; on D.eat3, S.fat, S.blood and S.no_eat it then stays), and
"move" on D.heave, D.unclean and D.clean.
"""

import math

import offerings as OF
import svg_figures as F
from generate_tabernacle import (ACACIA, BG, BRONZE, GOLD, PANEL, RED, SAND,
                                 SAND_DIM, SILVER, TEXT, TEXT_DIM, WHITE_LINEN)
from leviticus17_stations import (BLOOD, CH, CW, Station, Target, appear,
                                  bounds, ellipse_pts, flames, motion, pts_str,
                                  rect_pts, rgb, slab, t_s, trace)
from svg_map_camera import EASE, fade
from svg_surface import _fmt
from svg_vocab import NOT_RED, mix, not_mark_points

CHIP = 15                                   # these cards' chip type
MEAT = mix(PANEL, RED, .72)
CLAY = (196, 140, 96)


def _entry(board, key):
    return next(e for e in board if e.key == key)


def _label(board, key):
    return _entry(board, key).label


def _verse_beats(ctx, verb, key):
    """This file's beats of `verb` on `key` (the cue strings)."""
    return [b for st in ctx.verse.stops for b in st.beats
            if b[0] == verb and b[1] == key]


def _has(ctx, key):
    """Is `key` drawn in this file: lit here, or lit before."""
    return key in ctx.lit or key in ctx.before


def _t(t, d):
    return None if t is None else t + d


def grow_x(inner, t, x0, dur=0.8):
    """`inner` grown rightwards from x0 at t (there from the start, t None)."""
    if t is None or not inner:
        return inner
    return (f'<g opacity="0"><set attributeName="opacity" to="1" '
            f'begin="{t_s(t)}"/><g transform="translate({_fmt(x0)} 0)">'
            f'<g transform="scale(0.02 1)"><animateTransform '
            f'attributeName="transform" type="scale" values="0.02 1;1 1" '
            f'begin="{t_s(t)}" dur="{dur:.2f}s" fill="freeze" '
            f'calcMode="spline" keyTimes="0;1" keySplines="{EASE}"/>'
            f'<g transform="translate({_fmt(-x0)} 0)">{inner}</g></g></g></g>')


def arrow(p0, p1, t, col=TEXT_DIM, w=2.2, head=9.0, dur=0.6):
    """An arrow traced from p0 to p1 (or along the points p0, when p1 is
    None), its head after."""
    pts = list(p0) if p1 is None else [p0, p1]
    p0, p1 = pts[-2], pts[-1]
    a = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    hx, hy = p1
    h = [(hx - head * math.cos(a - 0.45), hy - head * math.sin(a - 0.45)),
         (hx, hy),
         (hx - head * math.cos(a + 0.45), hy - head * math.sin(a + 0.45))]
    tip = (f'<polygon points="{pts_str(h)}" fill="{rgb(col)}" '
           f'stroke="{rgb(col)}" stroke-width="1" stroke-linejoin="round"/>')
    return trace(pts, col, w, t, dur) + appear(tip, _t(t, dur * 0.8), dur=0.2)


def not_svg(xy, r, t, op=1.0, col=NOT_RED, w=3.6):
    """The not-mark drawn in at t (ring, then bar), or there (t None)."""
    ring, bar = not_mark_points(xy, r)
    extra = f' stroke-opacity="{op:.2f}" stroke-linecap="round"'
    if t is None:
        return trace(ring, col, w, None, extra=extra) + trace(bar, col, w, None, extra=extra)
    return (trace(ring, col, w, t, 0.55, extra=extra)
            + trace(bar, col, w, t + 0.55, 0.3, extra=extra))


def bread_svg(ctx, kind, x, gy, k):
    """One of offerings.BREADS as bread(), its foot at (x, gy), scale k:
    cakes two loaves, wafers three thin rounds, the cakes mixed with oil in
    the oil's gold, the leavened loaf risen."""
    linen = WHITE_LINEN
    if kind == "cakes":
        return (ctx.figure(F.bread(), x - 3 * k, gy, k, linen, PANEL)
                + ctx.figure(F.bread(), x + 3 * k, gy - 5 * k, k, linen, PANEL))
    if kind == "wafers":
        out = ""
        for i in range(3):
            fig = ctx.figure(F.bread(), 0, 0, k, linen, PANEL)
            out += (f'<g transform="translate({_fmt(x)} {_fmt(gy - i * 2.6 * k)}) '
                    f'scale(1.08 0.42)">{fig}</g>')
        return out
    if kind == "oil_cakes":
        return (ctx.figure(F.bread(), x, gy, k, mix(linen, GOLD, .55), PANEL)
                + "".join(f'<circle cx="{_fmt(x + dx * k)}" cy="{_fmt(gy - dy * k)}" '
                          f'r="{_fmt(0.9 * k)}" fill="{rgb(GOLD)}"/>'
                          for dx, dy in ((-4, 7.8), (1.5, 8.4), (5.5, 7.2))))
    # leavened: the same loaf, risen
    fig = ctx.figure(F.bread(), 0, 0, k * 1.1, mix(linen, CLAY, .35), PANEL)
    return f'<g transform="translate({_fmt(x)} {_fmt(gy)}) scale(1 1.75)">{fig}</g>'


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
    pts = F.smooth([(x - w / 2, y + h * .3), (x - w * .4, y - h * .3),
                    (x - w * .1, y - h / 2), (x + w * .25, y - h * .4),
                    (x + w / 2, y), (x + w * .3, y + h / 2), (x - w * .2, y + h * .45)], n=4)
    return (f'<polygon points="{pts_str(pts)}" fill="{rgb(mix(PANEL, WHITE_LINEN, .8))}" '
            f'stroke="{rgb(TEXT)}" stroke-width="1.4"/>')


def drop_svg(x, y, h=40):
    w = h * .62
    pts = F.smooth([(x, y - h / 2), (x + w * .28, y - h * .1), (x + w / 2, y + h * .2),
                    (x + w * .3, y + h * .45), (x, y + h / 2), (x - w * .3, y + h * .45),
                    (x - w / 2, y + h * .2), (x - w * .28, y - h * .1)], n=3)
    return (f'<polygon points="{pts_str(pts)}" fill="{rgb(BLOOD)}" '
            f'stroke="{rgb(mix(BLOOD, TEXT, .4))}" stroke-width="1.3"/>')


def slide(inner, t, dx, dur=1.1):
    """`inner` moved dx across at t, once (there, moved, when t is None)."""
    if t is None:
        return f'<g transform="translate({_fmt(dx)} 0)">{inner}</g>'
    return (f'<g><animateTransform attributeName="transform" type="translate" '
            f'values="0 0;{_fmt(dx)} 0" begin="{t_s(t)}" dur="{dur:.2f}s" '
            f'fill="freeze" calcMode="spline" keyTimes="0;1" keySplines="{EASE}"/>'
            f'{inner}</g>')


def token_move(inner, start, end, show, t, dur=1.0):
    """`inner` (drawn about its own origin) shown at `start` from `show` and
    carried to `end` from t, once."""
    rel = [(0, 0), (end[0] - start[0], end[1] - start[1])]
    return (f'<g opacity="0"><set attributeName="opacity" to="1" '
            f'begin="{t_s(show)}"/>{fade(max(0.0, show), 0.3)}'
            f'<g transform="translate({_fmt(start[0])} {_fmt(start[1])})"><g>'
            f'{motion(rel, t, dur)}{inner}</g></g></g>')


class _Card(Station):
    """What the three cards share: the "not" verb and its kept marks."""

    NOT_AT = {}            # target -> (xy, r) of its kept not-mark

    def not_at(self, T, key):
        if key in self.NOT_AT:
            return self.NOT_AT[key]
        b = T[key].box
        r = min(40, max(16, max(b[2] - b[0], b[3] - b[1]) * .55))
        return ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2), r

    def kept_not(self, ctx, key, t):
        """A kept mark, as its target draws it: there (dim, traced again by
        any "not" this verse) once drawn before, drawn in after the target
        when it is lit with no "not" of its own here."""
        xy, r = self.NOT_AT[key]
        if t is None:
            return not_svg(xy, r, None, op=0.8)
        if _verse_beats(ctx, "not", key):
            return ""
        return not_svg(xy, r, t + 0.6)

    def act(self, ctx, verb, key, t, opts):
        if verb == "not":
            xy, r = self.not_at(self.targets(ctx), key)
            return not_svg(xy, r, t, w=4.0 if key in self.NOT_AT else 3.6)
        if verb == "move":
            return self.move(ctx, key, t, opts)
        return super().act(ctx, verb, key, t, opts)

    def move(self, ctx, key, t, opts):
        raise KeyError(f"{self.key}: no move for {key!r}")


# ---------------------------------------------------------------------------
# D: the peace law
# ---------------------------------------------------------------------------

# the bread rack (top left): two shelves, two breads on each
SHELVES = (150, 250)                        # each board's top
RACK_X = (30, 350)
BREAD_KEYS = ("cakes", "wafers", "oil_cakes", "leavened")
BREAD_AT = {"cakes": (110, 150), "wafers": (270, 150),
            "oil_cakes": (110, 250), "leavened": (270, 250)}
BREAD_K = 4.2
LIFT = 8
BRACKET_Y = 88
D_PRIEST = (552, 270, 1.5)                  # x, ground, scale
HEAVE_TO = [(530, 100), (574, 100), (530, 80), (574, 80)]
HEAVE_K = 0.62
HEAVE_CHIP = (444, 92)

# the day strip (top right)
DAY_COLS = (636, 760, 884, 1008)
DAY_HEAD_Y = 44
DAY_ROWS = {"thanksgiving": 84, "vow": 124, "freewill": 164}
BAR_H = 26
FIRE3 = (948, 178)                          # the flame's foot
EAT3 = (948, 246)
DAY_CHIPS = {"D.not_accepted": (948, 292), "D.abomination": (948, 324)}

# the split (bottom)
SPLIT_SRC = (500, 340)
UNCLEAN_AT = (330, 462)                     # the flame's foot
GROUP_X = (614, 652, 690, 728)
GROUND = 462
PERSON_K = 0.6
CUT_FROM, CUT_DX = 576, -84
CAUSE_X, CAUSE_Y = 338, (516, 550)


class PeaceLaw(_Card):
    key = "D"
    NOT_AT = {"D.eat3": (EAT3, 27)}

    def shots(self):
        return {"": (1.0, CW / 2, CH / 2),
                "breads": self.clamp_shot(1.6, 320, 180),
                "days": self.clamp_shot(1.6, 704, 180),
                # the top edge under the bread rack and the priest
                "split": (1.8, 507, 282 + 288 / 1.8)}

    # -- helpers ----------------------------------------------------------
    def _priest(self, ctx, t):
        x, gy, k = D_PRIEST
        return appear(ctx.figure(F.priest(arms="up"), x, gy, k, TEXT, PANEL), t)

    def _heave_cluster(self, ctx):
        return "".join(bread_svg(ctx, kind, x, y, BREAD_K * HEAVE_K)
                       for kind, (x, y) in zip(BREAD_KEYS, HEAVE_TO))

    def _person(self, ctx, x):
        return ctx.use(ctx.fig_def("lev17_D_man", F.man(), PERSON_K), x, GROUND)

    def targets(self, ctx):
        T = {}
        # -- the rack -----------------------------------------------------
        x0, x1 = RACK_X

        def rack(c, t):
            wood, dim = mix(PANEL, ACACIA, .7), mix(PANEL, ACACIA, .5)
            posts = "".join(slab(x - 5, SHELVES[0] - 54, x + 5, SHELVES[1] + 24, dim, ACACIA, 2)
                            for x in (x0 + 6, x1 - 6))
            boards = "".join(slab(x0, y, x1, y + 11, wood, ACACIA, 3) for y in SHELVES)
            return appear(posts + boards, t, "lift", 0.5)
        rb = (x0, SHELVES[0] - 54, x1, SHELVES[1] + 24)
        T["D.shelf"] = Target("D.shelf", box=rb, draw=rack,
                              outline=[(rect_pts(rb[0] - 4, rb[1] - 4, rb[2] + 4, rb[3] + 2), True)])
        for kind in BREAD_KEYS:
            bx, gy = BREAD_AT[kind]
            box = (bx - 40, gy - 50, bx + 40, gy)
            word = _label(OF.BREADS, kind)

            def draw(c, t, kind=kind, bx=bx, gy=gy, word=word):
                return (appear(bread_svg(c, kind, bx, gy, BREAD_K), t, "lift", 0.5)
                        + c.label(f"D.{kind}", word, (bx, gy + 24), CHIP, TEXT, "mm",
                                  t=_t(t, 0.15)))
            T[f"D.{kind}"] = Target(f"D.{kind}", box=box, draw=draw,
                                    outline=[(rect_pts(bx - 44, gy - 52, bx + 44, gy + 2), True)])

        def breads(c, t):
            out = ""
            for i, kind in enumerate(BREAD_KEYS):
                k = f"D.{kind}"
                if not _has(c, k):
                    out += T[k].draw(c, _t(t, i * 0.35))
            return out
        T["D.breads"] = Target("D.breads", box=rb, draw=breads,
                               outline=[(rect_pts(x0 + 14, SHELVES[0] - 52, x1 - 14,
                                                  SHELVES[1] + 2), True)])
        br = [(x0, BRACKET_Y + 10), (x0, BRACKET_Y), (x1, BRACKET_Y), (x1, BRACKET_Y + 10)]
        tx = (x0 + x1) / 2

        def thanks(c, t):
            return (trace(br, TEXT_DIM, 2, t, 0.8)
                    + c.chip("D.thanksgiving", _label(OF.DAYS, "thanksgiving"),
                             (tx, BRACKET_Y - 20), CHIP, t=t))
        T["D.thanksgiving"] = Target("D.thanksgiving", box=(x0, BRACKET_Y - 34, x1, BRACKET_Y + 10),
                                     outline=[(rect_pts(tx - 54, BRACKET_Y - 34, tx + 54,
                                                        BRACKET_Y - 6), True)],
                                     draw=thanks)
        # -- the heave ----------------------------------------------------
        px, pgy, pk = D_PRIEST
        pb = (px - 36, pgy - 105 * pk - 4, px + 36, pgy)
        T["D.priest"] = Target("D.priest", box=pb, draw=lambda c, t: self._priest(c, t),
                               outline=[(F.outline(F.priest(arms="up"), px, pgy, pk), True)])

        def sprinkles(c, t):
            out = "" if _has(c, "D.priest") else self._priest(c, t)
            return out + c.chip("D.sprinkles", "sprinkles the blood", (px - 10, pgy + 24), CHIP,
                                t=t)
        T["D.sprinkles"] = Target("D.sprinkles", box=(px - 82, pgy + 12, px + 62, pgy + 36),
                                  outline=[(rect_pts(px - 84, pgy + 11, px + 64, pgy + 37), True)],
                                  draw=sprinkles)
        hc = HEAVE_CHIP

        def heave(c, t):
            chip = c.chip("D.heave", "heave offering", hc, CHIP, t=t)
            if t is None:
                fig = ("" if _has(c, "D.priest") or _has(c, "D.sprinkles")
                       else self._priest(c, None))
                return fig + self._heave_cluster(c) + chip
            if _verse_beats(c, "move", "D.heave"):
                return chip                      # the breads are the move's
            lifted = "".join(token_move(bread_svg(c, kind, 0, 0, BREAD_K), BREAD_AT[kind],
                                        (BREAD_AT[kind][0], BREAD_AT[kind][1] - LIFT),
                                        t, t + 0.1, 0.7) for kind in BREAD_KEYS)
            return lifted + chip
        T["D.heave"] = Target("D.heave", box=(hc[0] - 55, hc[1] - 14, hc[0] + 55, hc[1] + 14),
                              outline=[(rect_pts(hc[0] - 56, hc[1] - 16, hc[0] + 56, hc[1] + 16), True)],
                              draw=heave)
        # -- the day strip ------------------------------------------------
        c0, c1, c2, c3 = DAY_COLS
        r_last = DAY_ROWS["freewill"]

        def col_head(n, xa, xb):
            def draw(c, t):
                rule = trace([(xa + 6, DAY_HEAD_Y + 16), (xb - 6, DAY_HEAD_Y + 16)],
                             SAND_DIM, 1.6, t, 0.4)
                sep = trace([(xb, DAY_HEAD_Y - 8), (xb, r_last + 24)],
                            SAND_DIM, 1.2, _t(t, 0.2), 0.4, extra=' stroke-dasharray="4 5"')
                return rule + sep + c.label(f"D.day{n}", f"day {n}", ((xa + xb) / 2, DAY_HEAD_Y),
                                            CHIP, TEXT, "mm", t=t)
            return draw

        def bar(row, xa, xb, col=SAND):
            y = DAY_ROWS[row]
            return (f'<rect x="{_fmt(xa)}" y="{_fmt(y - BAR_H / 2)}" width="{_fmt(xb - xa)}" '
                    f'height="{BAR_H}" fill="{rgb(mix(PANEL, col, .4))}" '
                    f'stroke="{rgb(col)}" stroke-width="1.3"/>')

        def row_label(c, row, key, t):
            return c.label(key, _label(OF.DAYS, row), (c0 + 7, DAY_ROWS[row]), 14, TEXT,
                           "lm", t=t)

        def day1(c, t):
            return (col_head(1, c0, c1)(c, t)
                    + grow_x(bar("thanksgiving", c0, c1), _t(t, 0.2), c0)
                    + row_label(c, "thanksgiving", "D.day1:thanksgiving", _t(t, 0.2)))
        r1 = DAY_ROWS["thanksgiving"]
        T["D.day1"] = Target("D.day1", box=(c0, DAY_HEAD_Y - 12, c1, r1 + BAR_H / 2),
                             outline=[(rect_pts(c0 - 2, r1 - BAR_H / 2 - 3, c1 + 2,
                                                r1 + BAR_H / 2 + 3), True)], draw=day1)
        tick = [(c1, r1 - 17), (c1, r1 + 17)]
        T["D.morning"] = Target("D.morning", outline=[(rect_pts(c1 - 5, r1 - 19, c1 + 132, r1 + 14), True)],
                                draw=lambda c, t: trace(tick, GOLD, 3.2, t, 0.4)
                                + c.label("D.morning", _label(OF.DAYS, "morning"),
                                          (c1 + 8, r1), 14, TEXT, "lm", t=_t(t, 0.2)))
        for row in ("vow", "freewill"):
            y = DAY_ROWS[row]

            def draw(c, t, row=row):
                return (grow_x(bar(row, c0, c1), t, c0, 0.6)
                        + row_label(c, row, f"D.{row}", t))
            T[f"D.{row}"] = Target(f"D.{row}", box=(c0, y - 13, c1, y + 13), draw=draw,
                                   outline=[(rect_pts(c0 - 2, y - BAR_H / 2 - 3, c1 + 2,
                                                      y + BAR_H / 2 + 3), True)])

        def day2(c, t):
            ext = bar("vow", c1, c2) + bar("freewill", c1, c2)
            return col_head(2, c1, c2)(c, t) + grow_x(ext, _t(t, 0.2), c1, 0.8)
        y2 = DAY_ROWS["vow"]
        T["D.day2"] = Target("D.day2", box=(c1, DAY_HEAD_Y - 12, c2, r_last + 12), draw=day2,
                             outline=[(rect_pts(c1 - 2, y2 - BAR_H / 2 - 3, c2 + 2,
                                                r_last + BAR_H / 2 + 3), True)])
        T["D.day3"] = Target("D.day3", box=(c2, DAY_HEAD_Y - 12, c3, DAY_HEAD_Y + 18),
                             outline=[(rect_pts(c2 + 4, DAY_HEAD_Y - 14, c3 - 4, DAY_HEAD_Y + 18), True)],
                             draw=col_head(3, c2, c3))
        fx, fgy = FIRE3

        def fire3(c, t):
            g = flames([fx - 16, fx, fx + 16], fgy, [36, 52, 36])
            return (appear(g, t, "grow", 0.8, about=(fx, fgy))
                    + c.chip("D.fire3", _label(OF.DAYS, "burned"), (c3 - 6, fgy + 24), CHIP,
                             anchor="rm", t=_t(t, 0.3)))
        T["D.fire3"] = Target("D.fire3", box=(fx - 30, fgy - 56, fx + 30, fgy),
                              outline=[(rect_pts(fx - 32, fgy - 58, fx + 32, fgy + 2), True)],
                              draw=fire3)
        ex, ey = EAT3
        T["D.eat3"] = Target("D.eat3", box=(ex - 28, ey - 14, ex + 28, ey + 14),
                             outline=[(ellipse_pts(ex, ey, 31, 31), True)],
                             draw=lambda c, t: appear(meat_svg(ex, ey), t)
                             + self.kept_not(c, "D.eat3", t))
        for key, board_key in (("D.not_accepted", "not_accepted"),
                               ("D.abomination", "abomination")):
            word = _label(OF.DAYS, board_key)
            x, y = DAY_CHIPS[key]
            T[key] = Target(key, box=(x - 64, y - 14, x + 64, y + 14),
                            outline=[(rect_pts(x - 66, y - 16, x + 66, y + 16), True)],
                            draw=lambda c, t, key=key, word=word, x=x, y=y: c.chip(
                                key, word, (x, y), CHIP, t=t))
        # -- the split ----------------------------------------------------
        sx, sy = SPLIT_SRC
        T["D.split"] = Target("D.split", box=(sx - 30, sy - 12, sx + 30, sy + 14),
                              outline=[(rect_pts(sx - 32, sy - 14, sx + 108, sy + 16), True)],
                              draw=lambda c, t: appear(meat_svg(sx, sy), t)
                              + c.chip("D.split", "the meat", (sx + 66, sy), CHIP, t=_t(t, 0.2)))
        ux, ugy = UNCLEAN_AT
        gx = (GROUP_X[1] + GROUP_X[2]) / 2
        fork_l = [(sx - 24, sy + 16), (ux + 20, ugy - 70)]
        fork_r = [(sx + 24, sy + 16), (gx - 10, GROUND - 82)]

        def unclean(c, t):
            g = flames([ux - 16, ux, ux + 16], ugy, [38, 54, 38])
            out = (arrow(*fork_l, t, dur=0.5) + appear(g, _t(t, 0.3), "grow", 0.8, about=(ux, ugy))
                   + c.chip("D.unclean", "unclean", (ux, ugy + 22), CHIP, t=_t(t, 0.3)))
            if t is None:                    # the token where it went
                out += f'<g transform="translate({_fmt(ux)} {_fmt(ugy - 22)})">{meat_svg(0, 0, 26, 12)}</g>'
            elif not _verse_beats(c, "move", "D.unclean"):
                out += token_move(meat_svg(0, 0, 26, 12), SPLIT_SRC, (ux, ugy - 22),
                                  t, t + 0.4, 0.9)
            return out
        T["D.unclean"] = Target("D.unclean", box=(ux - 32, ugy - 58, ux + 32, ugy),
                                outline=[(rect_pts(ux - 34, ugy - 60, ux + 34, ugy + 2), True)],
                                draw=unclean)

        def clean(c, t):
            men = "".join(self._person(c, x) for x in GROUP_X)
            if not _has(c, "D.cut_off"):
                men += self._person(c, CUT_FROM)
            out = (arrow(*fork_r, t, dur=0.5) + appear(men, _t(t, 0.3))
                   + c.chip("D.clean", "clean", (gx, GROUND + 22), CHIP, t=_t(t, 0.3)))
            if t is None:
                out += f'<g transform="translate({_fmt(gx)} {_fmt(GROUND - 80)})">{meat_svg(0, 0, 26, 12)}</g>'
            elif not _verse_beats(c, "move", "D.clean"):
                out += token_move(meat_svg(0, 0, 26, 12), SPLIT_SRC, (gx, GROUND - 80),
                                  t, t + 0.4, 0.9)
            return out
        gb = (CUT_FROM - 16, GROUND - 70, GROUP_X[-1] + 16, GROUND)
        T["D.clean"] = Target("D.clean", box=gb, draw=clean,
                              outline=[(rect_pts(GROUP_X[0] - 18, GROUND - 72,
                                                 GROUP_X[-1] + 18, GROUND + 2), True)])
        cx_ = CUT_FROM + CUT_DX

        def cut_off(c, t):
            man = self._person(c, CUT_FROM)
            if t is None:
                fig = slide(man, None, CUT_DX)
            elif "D.clean" in c.before:
                fig = slide(man, t, CUT_DX)
            elif c.lit.get("D.clean", t + 1) <= t:   # it comes in with the group
                fig = appear(slide(man, t, CUT_DX), _t(c.lit["D.clean"], 0.3))
            else:
                fig = appear(slide(man, t + 0.4, CUT_DX), t)
            return fig + c.chip("D.cut_off", _label(OF.PENALTIES, "unclean_eats"),
                                ((cx_ + GROUP_X[0]) / 2 - 4, GROUND + 50), CHIP,
                                t=_t(t, 0.6), edge=RED)
        T["D.cut_off"] = Target("D.cut_off", box=(cx_ - 16, GROUND - 70, cx_ + 16, GROUND),
                                outline=[(rect_pts(cx_ - 18, GROUND - 72, cx_ + 18, GROUND + 2), True)],
                                draw=cut_off)
        for key, ck, y in (("D.uncleanness_of_man", "uncleanness_of_man", CAUSE_Y[0]),
                           ("D.unclean_animal", "unclean_animal", CAUSE_Y[1])):
            word = _label(OF.CAUSES, ck)
            lx = CAUSE_X
            T[key] = Target(key, box=(lx - 85, y - 14, lx + 85, y + 14),
                            outline=[(rect_pts(lx - 88, y - 15, lx + 88, y + 15), True)],
                            draw=lambda c, t, key=key, word=word, y=y, lx=lx: c.chip(
                                key, word, (lx, y), CHIP, t=t,
                                lead=(cx_ - 8, GROUND - 34 + (y - CAUSE_Y[0]) * 0.5)))
        return T

    def moved(self, key, opts):
        """The meat's token stays where it went (the target draws it)."""
        return key if key in ("D.unclean", "D.clean") else None

    def move(self, ctx, key, t, opts):
        show = opts.get("_show")
        if key == "D.heave":
            tl = show if show is not None else ctx.lit.get("D.heave", opts["_arrive"])
            tl = min(tl, t - 0.3)
            out = ""
            if not _has(ctx, "D.priest") and not _has(ctx, "D.sprinkles"):
                out += self._priest(ctx, max(opts["_arrive"], t - 0.5))
            for i, kind in enumerate(BREAD_KEYS):
                bx, gy = BREAD_AT[kind]
                fx, fy = HEAVE_TO[i]
                rise = [(0, 0), (0, -LIFT)]
                to = [(0, 0), (fx - bx, fy - (gy - LIFT))]
                body = (f'<g transform="scale(1)"><animateTransform attributeName="transform" '
                        f'type="scale" values="1;{HEAVE_K}" begin="{t_s(t)}" dur="1.20s" '
                        f'fill="freeze" calcMode="spline" keyTimes="0;1" '
                        f'keySplines="{EASE}"/>{bread_svg(ctx, kind, 0, 0, BREAD_K)}</g>')
                out += (f'<g opacity="0"><set attributeName="opacity" to="1" '
                        f'begin="{t_s(tl)}"/>{fade(tl, 0.3)}'
                        f'<g transform="translate({_fmt(bx)} {_fmt(gy)})"><g>'
                        f'{motion(rise, tl + 0.05, 0.7)}<g>{motion(to, t + i * 0.08, 1.2)}'
                        f'{body}</g></g></g></g>')
            return out
        if key in ("D.unclean", "D.clean"):
            st = show if show is not None else opts["_arrive"]
            st = min(st, t - 0.2)
            end = ((UNCLEAN_AT[0], UNCLEAN_AT[1] - 22) if key == "D.unclean"
                   else ((GROUP_X[1] + GROUP_X[2]) / 2, GROUND - 80))
            return token_move(meat_svg(0, 0, 26, 12), SPLIT_SRC, end, st, t, 0.9)
        return super().move(ctx, key, t, opts)


# ---------------------------------------------------------------------------
# S: shares and bans
# ---------------------------------------------------------------------------

R1, R2 = 150, 256                           # the shares' rows, ground
S_PRIEST = (802, 166, 1.06)
SONS_X = (620, 654, 688, 722)
SONS_K = 0.6
VESSEL_X = {"oven": 442, "pan": 530, "griddle": 645}
FAT_Y, BLOOD_Y = 364, 498                   # the bans' rows, centre
BAN_X0, BAN_X1 = 18, 784
ICON_X = 68
CUT_X = 745


class Shares(_Card):
    key = "S"
    NOT_AT = {"S.fat": ((ICON_X, FAT_Y - 8), 34), "S.blood": ((ICON_X, BLOOD_Y - 8), 34),
              "S.no_eat": ((444, FAT_Y - 4), 22)}

    def shots(self):
        return {"": (1.0, CW / 2, CH / 2),
                "shares": self.clamp_shot(1.3, 630, 222),
                # the top edge between the shares' two rows: the skin and
                # vessels row wholly out, the breads' wholly in
                "bans": (1.3, 394, 184 + 288 / 1.3)}

    def _priest(self, ctx, t):
        x, gy, k = S_PRIEST
        return (appear(ctx.figure(F.priest(), x, gy, k, TEXT, PANEL), t)
                + ctx.chip("S.priest", "the priest", (x + 30, gy - 70), CHIP,
                           anchor="lm", t=_t(t, 0.2)))

    def targets(self, ctx):
        T = {}
        px, pgy, pk = S_PRIEST

        def priest_once(c, t, me):
            if _has(c, "S.priest"):
                return ""
            ks = [k for k in ("S.skin", "S.baked") if _has(c, k)] or [me]
            # the earliest of them draws him: one drawn before, else the
            # first lit here
            before = [k for k in ks if k in c.before]
            first = before[0] if before else min(ks, key=lambda k: c.lit.get(k, 0))
            return self._priest(c, t) if first == me else ""
        T["S.priest"] = Target("S.priest", box=(px - 20, pgy - 112, px + 20, pgy),
                               outline=[(F.outline(F.priest(), px, pgy, pk), True)],
                               draw=lambda c, t: self._priest(c, t))
        # the skin
        ox_x = 330
        ox = F.ox()
        ring = F.outline(ox, ox_x, R1, 1.0, flip=-1)

        def skin(c, t):
            body = appear(c.figure(ox, ox_x, R1, 1.0, mix(PANEL, TEXT, .55), PANEL, flip=-1),
                          t, dur=0.6)
            hide = body + trace(ring, TEXT, 2.4, _t(t, 0.2), 1.0, closed=True,
                                extra=' stroke-dasharray="7 4"')
            return (hide + c.chip("S.skin", "the skin", (ox_x, R1 + 22), CHIP, t=_t(t, 0.4))
                    + arrow([(ox_x + 30, R1 - 90), (ox_x + 70, 62), (px - 70, 62),
                             (px - 26, pgy - 92)], None, _t(t, 0.6), dur=1.0)
                    + priest_once(c, _t(t, 0.9), "S.skin"))
        T["S.skin"] = Target("S.skin", box=bounds(ring), outline=[(ring, True)], draw=skin)
        # the baked
        for name in ("oven", "pan", "griddle"):
            vx = VESSEL_X[name]

            def draw(c, t, name=name, vx=vx):
                ink = BRONZE if name != "oven" else CLAY
                fig = c.figure(F.cookware(name, "bread"), vx, R1, 1.1, ink, PANEL)
                return (appear(fig, t, "lift", 0.5)
                        + c.label(f"S.{name}", _label(OF.VESSELS, name), (vx, R1 + 22), CHIP,
                                  TEXT, "mm", t=_t(t, 0.15)))
            parts = F.cookware(name, "bread")
            b = F.bbox((parts, 0))
            box = (vx + b[0] * 1.1, R1 - b[3] * 1.1, vx + b[1] * 1.1, R1)
            T[f"S.{name}"] = Target(f"S.{name}", box=box, draw=draw,
                                    outline=[(rect_pts(box[0] - 4, box[1] - 4, box[2] + 4, box[3] + 3), True)])

        def baked(c, t):
            out = ""
            for i, name in enumerate(("oven", "pan", "griddle")):
                k = f"S.{name}"
                if not _has(c, k):
                    out += T[k].draw(c, _t(t, i * 0.3))
            return (out + arrow((690, R1 - 36), (px - 30, pgy - 56), _t(t, 0.9), dur=0.6)
                    + priest_once(c, _t(t, 1.1), "S.baked"))
        bb = (VESSEL_X["oven"] - 30, R1 - 60, VESSEL_X["griddle"] + 34, R1)
        T["S.baked"] = Target("S.baked", box=bb, draw=baked,
                              outline=[(rect_pts(bb[0] - 4, bb[1] - 4, bb[2] + 4, bb[3] + 4), True)])
        # mixed with oil / dry
        for key, word, x, oil in (("S.mixed", "mixed with oil", 300, True),
                                  ("S.dry", "dry", 460, False)):
            def draw(c, t, key=key, word=word, x=x, oil=oil):
                fig = bread_svg(c, "oil_cakes" if oil else "cakes", x, R2, 4.4)
                return (appear(fig, t, "lift", 0.5)
                        + c.label(key, word, (x, R2 + 22), CHIP, TEXT, "mm", t=_t(t, 0.15)))
            box = (x - 46, R2 - 40, x + 46, R2)
            T[key] = Target(key, box=box, draw=draw,
                            outline=[(rect_pts(box[0] - 3, box[1] - 3, box[2] + 3, box[3] + 3), True)])

        def sons(c, t):
            did = c.fig_def("lev17_S_son", F.priest(), SONS_K)
            men = "".join(c.use(did, x, R2) for x in SONS_X)
            return (arrow((512, R2 - 22), (SONS_X[0] - 24, R2 - 34), t, dur=0.6)
                    + appear(men, _t(t, 0.4))
                    + c.chip("S.sons", "sons of Aaron", (sum(SONS_X) / 4, R2 + 22), CHIP,
                             t=_t(t, 0.5)))
        sbx = (SONS_X[0] - 14, R2 - 66, SONS_X[-1] + 14, R2)
        T["S.sons"] = Target("S.sons", box=sbx, draw=sons,
                             outline=[(rect_pts(sbx[0] - 4, sbx[1] - 4, sbx[2] + 4, sbx[3] + 2), True)])
        # -- the bans -----------------------------------------------------

        def row(c, key, y, icon, word, t):
            frame = (f'<rect x="{BAN_X0}" y="{_fmt(y - 58)}" width="{BAN_X1 - BAN_X0}" '
                     f'height="116" rx="8" fill="{rgb(mix(PANEL, BG, .45))}" '
                     f'stroke="{rgb(SAND_DIM)}" stroke-width="1.2"/>')
            return (appear(frame, t, dur=0.4) + appear(icon, _t(t, 0.1), "pop", 0.4,
                                                       about=(ICON_X, y - 8))
                    + c.label(key, word, (ICON_X, y + 40), CHIP, TEXT, "mm", t=_t(t, 0.2))
                    + self.kept_not(c, key, t))
        for key, y, icon, word in (("S.fat", FAT_Y, fat_svg(ICON_X, FAT_Y - 8, 58, 32), "fat"),
                                   ("S.blood", BLOOD_Y, drop_svg(ICON_X, BLOOD_Y - 8, 50), "blood")):
            T[key] = Target(key, box=(ICON_X - 38, y - 46, ICON_X + 38, y + 52),
                            outline=[(rect_pts(BAN_X0, y - 58, BAN_X1, y + 58), True)],
                            draw=lambda c, t, key=key, y=y, icon=icon, word=word:
                            row(c, key, y, icon, word, t))

        def beast(key, parts, x, y, k, word, ink=TEXT, flip=-1, gdy=0):
            b = F.bbox((parts, 0))
            gy = y + 20 + gdy
            box = (x - b[1] * k, gy - b[3] * k, x - b[0] * k, gy) if flip < 0 else \
                (x + b[0] * k, gy - b[3] * k, x + b[1] * k, gy)

            def draw(c, t):
                return (appear(c.figure(parts, x, gy, k, ink, PANEL, flip=flip), t, "lift", 0.5)
                        + c.label(key, word, ((box[0] + box[2]) / 2, y + 40), CHIP, TEXT, "mm",
                                  t=_t(t, 0.15)))
            T[key] = Target(key, box=box, draw=draw,
                            outline=[(F.outline(parts, x, gy, k, flip=flip), True)])
        beast("S.ox", F.ox(), 180, FAT_Y, 0.64, "bull")
        beast("S.sheep", F.sheep(ram=True), 290, FAT_Y, 1.04, "sheep")
        beast("S.goat", F.goat(), 376, FAT_Y, 0.8, "goat")
        beast("S.dove", F.dove(descending=False), 180, BLOOD_Y, 2.7, "bird", SILVER, gdy=-16)
        beast("S.animal", F.goat(), 292, BLOOD_Y, 0.8, "animal")
        nx, ny = self.NOT_AT["S.no_eat"][0]
        T["S.no_eat"] = Target("S.no_eat", box=(nx - 18, ny - 12, nx + 18, ny + 12),
                               outline=[(ellipse_pts(nx, ny, 23, 23), True)],
                               draw=lambda c, t: appear(fat_svg(nx, ny, 30, 18), t)
                               + self.kept_not(c, "S.no_eat", t))
        for key, word, y in (("S.died", "dies of itself", FAT_Y - 20),
                             ("S.torn", "torn", FAT_Y + 20)):
            T[key] = Target(key, box=(530 - 50, y - 14, 530 + 50, y + 14),
                            outline=[(rect_pts(530 - 52, y - 15, 530 + 52, y + 15), True)],
                            draw=lambda c, t, key=key, word=word, y=y: c.chip(
                                key, word, (530, y), CHIP, t=t))
        T["S.service"] = Target("S.service", box=(606, FAT_Y - 14, 706, FAT_Y + 14),
                                outline=[(rect_pts(604, FAT_Y - 15, 708, FAT_Y + 15), True)],
                                draw=lambda c, t: arrow((584, FAT_Y), (602, FAT_Y), t, dur=0.4)
                                + c.chip("S.service", "other service", (656, FAT_Y), CHIP,
                                         t=_t(t, 0.3)))
        tent = F.tent()
        tk = 0.42
        tx = 486
        tb = F.bbox((tent, 0))
        tbox = (tx + tb[0] * tk, BLOOD_Y + 20 - tb[3] * tk, tx + tb[1] * tk, BLOOD_Y + 20)
        T["S.dwellings"] = Target("S.dwellings", box=tbox,
                                  outline=[(rect_pts(tbox[0] - 4, tbox[1] - 4, tbox[2] + 4, tbox[3] + 3), True)],
                                  draw=lambda c, t: appear(c.figure(tent, tx, BLOOD_Y + 20, tk, SAND, PANEL),
                                                           t, "lift", 0.5)
                                  + c.label("S.dwellings", "dwellings", (tx, BLOOD_Y + 40), CHIP,
                                            TEXT, "mm", t=_t(t, 0.15)))
        for key, entry, y in (("S.cut_off_fat", "eats_fat", FAT_Y),
                              ("S.cut_off_blood", "eats_blood", BLOOD_Y)):
            word = _label(OF.PENALTIES, entry)
            T[key] = Target(key, box=(CUT_X - 34, y - 14, CUT_X + 34, y + 14),
                            outline=[(rect_pts(CUT_X - 36, y - 15, CUT_X + 36, y + 15), True)],
                            draw=lambda c, t, key=key, word=word, y=y: c.chip(
                                key, word, (CUT_X, y), CHIP, t=t, edge=RED))
        return T


# ---------------------------------------------------------------------------
# L: Sinai
# ---------------------------------------------------------------------------

MT = (470, 452, 2.2)                         # x, foot, scale
L_MOSES = (858, 470, 1.5)
L_GROUND = [(60, 462), (220, 458), (380, 466), (540, 460), (700, 466), (860, 470), (980, 466)]


class Sinai(_Card):
    key = "L"

    def shots(self):
        return {"": (1.0, CW / 2, CH / 2)}

    def _mountain(self, ctx, t):
        x, gy, k = MT
        return appear(ctx.figure(F.mountain(), x, gy, k, SAND, PANEL), t, "grow", 1.2,
                      about=(x, gy))

    def targets(self, ctx):
        T = {}
        x, gy, k = MT
        mtn = F.mountain()
        ring = F.outline(mtn, x, gy, k)
        T["L.mountain"] = Target("L.mountain", box=bounds(ring), outline=[(ring, True)],
                                 draw=lambda c, t: self._mountain(c, t))
        top = min(p[1] for p in ring)
        peak_x = [p[0] for p in ring if p[1] == top][0]

        def mount(c, t):
            out = "" if _has(c, "L.mountain") else self._mountain(c, t)
            return out + c.chip("L.mount", _label(OF.SINAI, "mount"), (peak_x, top - 30),
                                16, t=t, lead=(peak_x, top - 4))
        T["L.mount"] = Target("L.mount", box=(peak_x - 50, top - 46, peak_x + 50, top - 14),
                              outline=[(rect_pts(peak_x - 54, top - 46, peak_x + 54, top - 14), True)],
                              draw=mount)

        def wild(c, t):
            sand = (f'<polygon points="{pts_str(L_GROUND + [(980, 520), (60, 520)])}" '
                    f'fill="{rgb(mix(PANEL, SAND, .22))}" stroke="none"/>')
            return (appear(sand, _t(t, 0.3), dur=0.8) + trace(L_GROUND, SAND, 2.4, t, 1.2)
                    + c.chip("L.wilderness", _label(OF.SINAI, "wilderness"), (330, 504), 16,
                             t=_t(t, 0.4)))
        T["L.wilderness"] = Target("L.wilderness", box=(60, 456, 980, 520),
                                   outline=[(rect_pts(256, 488, 404, 520), True)], draw=wild)
        mx, mgy, mk = L_MOSES
        man = F.man(staff=True)

        def moses(c, t):
            return (appear(c.figure(man, mx, mgy, mk, TEXT, PANEL), t, "lift", 0.5)
                    + c.chip("L.moses", _label(OF.SINAI, "moses"), (mx, mgy + 28), 16,
                             t=_t(t, 0.2)))
        T["L.moses"] = Target("L.moses", box=(mx - 30, mgy - 170, mx + 32, mgy),
                              outline=[(F.outline(man, mx, mgy, mk), True)], draw=moses)
        return T


def stations():
    return [PeaceLaw(), Shares(), Sinai()]
