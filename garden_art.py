"""The garden of Genesis 2-3: what the place is drawn from, not how the story is staged on it.

A hand-coloured woodcut on the house's dark page: muted fills, one light ink for the scenery,
crowns of lobed masses cut with parallel lines, a light that comes from up and to the west as it
does on every figure in svg_figures. It sits beside Joshua 14 and Acts 14, and the people are the
brightest thing in it, so they can act in front of it. Importing this runs nothing and writes
nothing. The story is in genesis2_garden.py and genesis3_garden.py, on garden_stage.py's engine.

Conventions
    World px are card px: one is one screen px at zoom 1. A man is 110 px tall, east is right,
    the people's line is near y 1400. Drawn subjects are parts lists in svg_figures' format
    ((kind, data, material), y up, in figure units, feet on zero); a paint table maps material to
    (fill, stroke, width), so geometry never knows a colour. What repeats goes in <defs> and <use>.
    No filter, no mask, no group opacity under a camera at rest: the only soft things are
    gradients on single shapes.

One place, two projections
    A point in the garden is (x, d): x east, d north of the people's line. The side view's card y
    is `land_y(x, d)` and the plan's is GROUND - d. x is the same in both, so the plan's river IS
    the side view's river from above, and a camera can rise from the one to the other with the
    place staying put (exact in x, and in y on the people's line). Perspective is a cheat: x is
    not foreshortened and only the people's line has `ground_y`.

To stage on it
    See THE STAGER'S CONSTANTS for where everything is. A verse on the planted side view:

        card = G.GardenCard(**G.card_kwargs())
        sc = G.panorama("planted", lean=True, heroes=False, flow=(0, 5), flow_reaches=("near",))
        sc = sc.trimmed((-700, 1000, 600, 1600), keep=("LF", "KN", "kf", "fn", "sa"))
        sc.behind += G.heroes_svg() + G.life_twig_svg() + G.fig_near_svg() + G.figs_svg()
        sc.front += G.shrubs_svg()
        fl = svg_map_camera.Flight(cam0, [("to", (1.4, 640, 1312), 4.0)])
        body = card.verse_svg("2:15", fl, sc)

    `GardenCard` is the svg_scene_card engine hosted here (town_xy (0, 0), S 1), so a camera is
    (zoom, x, y). garden_stage.Stage is the same card with the pair's profile people on it.

What the module gives a stager
    Trees      shade_tree olive fig date_palm cypress pomegranate shrub; SPECIES, forest, place
    Named      tree_of_life tree_of_knowledge knowledge_fruit heroes_svg knowledge_svg
               knowledge_reach, fig_leaf
    Close up   fruit_macro knowledge_tips (the bough's tip, thin-lined), life_twig_svg (the low
               bough, from 2:9), life_spray (its plate), TWIG_FRUIT; fig_near_svg figs_svg fig_one
               FIG_SVG FIG_A FIG_B FIG_C (the near fig and the three figs on it)
    Ground     panorama(state) -> Scene: "planted", "barren"; ground_y land_y project depth_scale
               depth_of; grass_tuft herb fern lily anemone daisy violet reed rock outcrop pebbles
               cracks patch; shrubs_svg SHRUBS (what they hide behind at 3:8)
    Thorns     thorns thistle thorn_land_svg (Scene.outside), thorns_near NEAR_THORNS
    Extent     garden_density way_svg (the edge is the reach of the water; no wall, no oval; see
               the note at GARDEN_EDGE); Scene.trimmed in_frame (what a camera can see)
    Water      panorama(flow=(begin, dur), flow_reaches=...), river_svg dry_course_svg, SLIVER_OFF,
               RIVER HEADS PARTING; water_top (what stands by it keeps above it)
    Planting   panorama(plant_in={phase: (begin, dur)}), heroes_svg(grow=...): 2:8-9 happening;
               bare_scrub bare_patch_def (the bare land's dry patches), SHOULDER, FORMED_CLEAR
    Sky        sky_svg, after_sky (stars over it), streak_cloud (2:5's dry cloud)
    Plan       plan_svg -> pieces; hang_in_plan side_op plan_garden, PLAN_NAMES; havilah gold_heap
               nugget_outline bdellium_tree onyx_stones citadel acacia acacia_at red_hill reed_bed
    Paint      PLANT_PAINT and each tree's own; MOUND_PAINT, SPROUT_PAINT, DEAD_SPROUT_PAINT,
               SMALL_SNAKE_PAINT, STICK_KEY_PAINT, STICK_PAINT for svg_figures' mound, sprout,
               small_snake and digging_stick; HL, NAME_INK
    Host       card_kwargs GardenCard thing_actor

Spending the budget. A file's limit is about 350 KB; this scenery takes about a third of it. A
rest with nothing moving costs nothing, and anything that moves, a camera's creep or a sliver of
water, repaints the whole of the picture inside its <img>, so a frame costs all that is in it. What
costs is ink in frame. A full-frame fill costs little if it is flat and much more if it is a
gradient or translucent, so the air's haze is in the colours (HAZE_FAR), no ground goes further
down than what covers it, and a gradient of the ground goes wherever a verse's camera can't see it
change. `Scene.trimmed(rect)` always, to the frame's edges over the whole flight, takes out what
can't be seen; `lean=True` for the planted land draws all but the nearest plain trees as flat cut
silhouettes and looks well behind people at any zoom; garden_stage switches the whole scene off
under a whole plate; and `hang_in_plan` switches the plan off whenever the side view covers it.
Flow only what is in frame.

Not in the text, and drawn anyway, none of it named, for the owner to rule on: every species but
the fig (2:9 says "every tree"; 3:7 gives the fig); the shapes of the two named trees (tall and
pale; low, wide and copper, because 2:9 and 3:6 say it was good to look at) and life standing west
of knowledge; the near fig's place, and that it is the tree he eats from and the one that gives
3:7's leaves; the low bough and its three pale fruit; the shrubs; the flowers; the far ranges; two
old cypresses as the last trees; the worn way; the gold as nuggets and grains in the gravel; the
bdellium as a tree; the banded stones; Cush's acacias and red hills; the walled tower for Assyria,
on the Hiddekel's north bank, which is all of Assyria that is tinted (the text says only that the
Hiddekel flows in front of it); the palms and reeds on the Euphrates'
land; the dry cloud; the dark sky. The fan of four rivers is pictorial: only two of them can be
located at all, and the chapter's own geography is one river parting.

Seen in headless Edge and in Playwright's WebKit, paused and played inside an <img>. Not yet seen
on an iPad.
"""

import functools
import math
import random
import re

import svg_figures as F
import svg_map_camera as C
import svg_scene_card as SC

GROUND = 1400
MAN = 110.0
MAN_H = 97.0
PXU = MAN / MAN_H           # card px per figure unit

TAU = math.pi * 2
LIGHT = (-.62, .78)         # where the light comes from: up and left (west)


# ---------------------------------------------------------------------------
# The compact emitter
# ---------------------------------------------------------------------------

def _hex(c):
    return "#%02x%02x%02x" % (int(c[0]), int(c[1]), int(c[2]))


# Materials whose dots are drawn as zero-length round-capped strokes: nine bytes
# a dot instead of thirty. (h.001, not h0: WebKit's trap with zero-length caps.)
PIP = {"pip", "pip_lit", "pip_rose", "pip_gold", "pip_violet", "pip_dark",
       "pip_white"}

# Materials cut with straight strokes: never rounded by the emitter.
CUT = {"gold_lit", "gold_sh", "onyx", "onyx_band", "brick", "brick_deep", "brick_line", "brick_edge", "gate_dark", "peak", "peak_deep",
       "peak_line", "peak_edge", "gold", "gold_hi", "tear", "dry_blade", "pebble", "pebble_foot", "crack", "fern_lit", "carve", "blade_deep", "blade_lit", "thistle_leaf", "thistle_cup", "tick", "fern", "hatch", "bark", "dab_deep", "dab_mid", "dab_lit", "frond",
       "frond_deep", "frond_lit", "rock", "rock_lit", "rock_deep", "rock_line",
       "spine", "blade", "blade_deep", "blade_lit", "ring", "thorn"}


class _D:
    """A path's `d`, in relative coordinates on a fixed grid, with the pen
    tracked in grid units so that rounding never accumulates."""

    def __init__(self, prec=0):
        self.prec, self.k = prec, 10 ** prec
        self.out = []
        self.px = self.py = self.sx = self.sy = 0
        self.started = False

    def i(self, v):
        return int(round(v * self.k))

    def _n(self, iv):
        if self.prec == 0:
            return str(iv)
        s = f"{abs(iv) / self.k:.{self.prec}f}".rstrip("0").rstrip(".")
        if s.startswith("0."):
            s = s[1:]
        if s in ("", "0"):
            return "0"
        return ("-" + s) if iv < 0 else s

    def _emit(self, cmd, nums):
        s = cmd
        prev = ""
        for iv in nums:
            n = self._n(iv)
            if prev and not (n[0] == "-" or (n[0] == "." and "." in prev)):
                s += " "
            s += n
            prev = n
        self.out.append(s)

    def _move_nums(self, ix, iy):
        if not self.started:
            cmd, nums = "M", [ix, iy]
            self.started = True
        else:
            cmd, nums = "m", [ix - self.px, iy - self.py]
        self.px, self.py = ix, iy
        self.sx, self.sy = ix, iy
        return cmd, nums

    def poly(self, pts, closed):
        q = [(self.i(x), self.i(y)) for x, y in pts]
        cmd, nums = self._move_nums(*q[0])
        rel = []
        for ix, iy in q[1:]:
            rel += [ix - self.px, iy - self.py]
            self.px, self.py = ix, iy
        if cmd == "M" and rel:
            self._emit("M", nums)
            self._emit("l", rel)
        else:
            self._emit(cmd, nums + rel)
        if closed:
            self.out.append("z")
            self.px, self.py = self.sx, self.sy

    def closed_curve(self, pts):
        """A closed quadratic B-spline. `t` costs two numbers a vertex, and
        its implied control is steered back onto the wanted point each step,
        so that rounding cannot drift."""
        Q = [(self.i(x), self.i(y)) for x, y in pts]
        n = len(Q)
        if n < 4:
            return self.poly(pts, True)
        sx, sy = (Q[-1][0] + Q[0][0]) // 2, (Q[-1][1] + Q[0][1]) // 2
        cmd, nums = self._move_nums(sx, sy)
        self._emit(cmd, nums)
        c = Q[0]
        m = ((c[0] + Q[1][0]) // 2, (c[1] + Q[1][1]) // 2)
        self._emit("q", [c[0] - self.px, c[1] - self.py,
                         m[0] - self.px, m[1] - self.py])
        self.px, self.py = m
        nums = []
        for j in range(2, n + 1):
            c = (2 * self.px - c[0], 2 * self.py - c[1])
            tgt = Q[j % n]
            m = ((c[0] + tgt[0]) // 2, (c[1] + tgt[1]) // 2)
            nums += [m[0] - self.px, m[1] - self.py]
            self.px, self.py = m
        self._emit("t", nums)
        self.out.append("z")
        self.px, self.py = self.sx, self.sy

    def open_curve(self, pts):
        Q = [(self.i(x), self.i(y)) for x, y in pts]
        n = len(Q)
        if n < 3:
            return self.poly(pts, False)
        cmd, nums = self._move_nums(*Q[0])
        self._emit(cmd, nums)
        if n == 3:
            self._emit("q", [Q[1][0] - self.px, Q[1][1] - self.py,
                             Q[2][0] - self.px, Q[2][1] - self.py])
            self.px, self.py = Q[2]
            return
        c = Q[1]
        m = ((c[0] + Q[2][0]) // 2, (c[1] + Q[2][1]) // 2)
        self._emit("q", [c[0] - self.px, c[1] - self.py,
                         m[0] - self.px, m[1] - self.py])
        self.px, self.py = m
        nums = []
        for j in range(3, n - 1):
            c = (2 * self.px - c[0], 2 * self.py - c[1])
            m = ((c[0] + Q[j][0]) // 2, (c[1] + Q[j][1]) // 2)
            nums += [m[0] - self.px, m[1] - self.py]
            self.px, self.py = m
        if nums:
            self._emit("t", nums)
        c = (2 * self.px - c[0], 2 * self.py - c[1])
        self._emit("q", [c[0] - self.px, c[1] - self.py,
                         Q[-1][0] - self.px, Q[-1][1] - self.py])
        self.px, self.py = Q[-1]

    def dot(self, x, y, r):
        """A disc, wound the way the polygons are, so that where one lies on another (a hand on
        the body, a head on the neck) the nonzero rule fills it and leaves no dark hole."""
        ir = max(1, self.i(r))
        cmd, nums = self._move_nums(self.i(x) - ir, self.i(y))
        self._emit(cmd, nums)
        rs = self._n(ir)
        self.out.append(f"a{rs} {rs} 0 1 1 {self._n(2 * ir)} 0"
                        f"a{rs} {rs} 0 1 1 {self._n(-2 * ir)} 0z")
        self.px, self.py = self.sx, self.sy

    def pip(self, x, y):
        cmd, nums = self._move_nums(self.i(x), self.i(y))
        self._emit(cmd, nums)
        self.out.append("h.001")
        self.px += 0

    def text(self):
        return "".join(self.out)


def _area(pts):
    a = 0.0
    for i in range(len(pts)):
        x0, y0 = pts[i - 1]
        x1, y1 = pts[i]
        a += x0 * y1 - x1 * y0
    return a


def render(parts, paint, s=PXU, flip=1, prec=0, curve=True, ox=0.0, oy=0.0, whole=()):
    """Parts (svg_figures' format, y up) to SVG, one `<path>` per run of a
    material, so a tree is six to ten elements however much is drawn in it. A material
    in `whole` is one `<path>` a part instead, its fill and outline together, so that
    each covers what it lies on: a leaf seen close, in front of another."""
    out = []
    i = 0
    n = len(parts)
    while i < n:
        kind, data, mat = parts[i]
        line = kind == "line"
        d = _D(prec)
        j = i
        while (j < n and parts[j][2] == mat and (parts[j][0] == "line") == line
               and (j == i or mat not in whole)):
            k2, dat, _m = parts[j]
            if k2 == "dot":
                if mat in PIP:
                    d.pip(ox + dat[0] * s * flip, oy - dat[1] * s)
                else:
                    d.dot(ox + dat[0] * s * flip, oy - dat[1] * s, dat[2] * s)
            else:
                pts = [(ox + x * s * flip, oy - y * s) for x, y in dat]
                if k2 == "fill":
                    if _area(pts) < 0:
                        pts = pts[::-1]
                    if curve and mat not in CUT:
                        d.closed_curve(pts)
                    else:
                        d.poly(pts, True)
                else:
                    if curve and mat not in CUT:
                        d.open_curve(pts)
                    else:
                        d.poly(pts, False)
            j += 1
        fill, stroke, w = paint.get(mat, (None, (255, 0, 255), 1))
        if mat in PIP:
            w = parts[i][1][2] * s * 2
        a = ""
        if fill is not None and not line:
            a += f' fill="{_hex(fill)}"'
        else:
            a += ' fill="none"'
        if stroke is not None and w:
            a += f' stroke="{_hex(stroke)}" stroke-width="{w:g}"'
        out.append(f'<path{a} d="{d.text()}"/>')
        i = j
    return "".join(out)


# ---------------------------------------------------------------------------
# Geometry of drawn things
# ---------------------------------------------------------------------------

def _inside(p, poly):
    x, y = p
    c = False
    for i in range(len(poly)):
        x0, y0 = poly[i - 1]
        x1, y1 = poly[i]
        if (y0 > y) != (y1 > y):
            if x < x0 + (y - y0) / (y1 - y0) * (x1 - x0):
                c = not c
    return c


def _runs(polys, keep=None, min_pts=3):
    """The stretches of each closed outline not inside another: the union's
    edge as open lines, so a mass of overlapping lobes has one contour."""
    runs = []
    for i, poly in enumerate(polys):
        flags = []
        for p in poly:
            ok = not any(_inside(p, q) for j, q in enumerate(polys) if j != i)
            if ok and keep is not None:
                ok = keep(p)
            flags.append(ok)
        if all(flags):
            runs.append(list(poly) + [poly[0]])
            continue
        if not any(flags):
            continue
        st = flags.index(False)
        cur = []
        for k in range(len(poly)):
            idx = (st + k) % len(poly)
            if flags[idx]:
                cur.append(poly[idx])
            else:
                if len(cur) >= min_pts:
                    runs.append(cur)
                cur = []
        if len(cur) >= min_pts:
            runs.append(cur)
    return runs


def lobed(rng, cx, cy, rx, ry, lobe=18.0, jag=0.5):
    """An irregular cluster of lobes round (cx, cy): the outline of a mass of
    leaves. Peaks and notches at uneven angles and depths, on an outline that
    is itself pushed out of round, so no two come out alike."""
    perim = TAU * math.sqrt((rx * rx + ry * ry) / 2)
    n = max(7, int(perim / lobe))
    amp = min(lobe * jag, .2 * min(rx, ry))
    gaps = [rng.uniform(0.55, 1.45) for _ in range(n)]
    tot = sum(gaps)
    a = rng.uniform(0, TAU)
    p2, p3 = rng.uniform(0, TAU), rng.uniform(0, TAU)
    a2, a3 = rng.uniform(.05, .16), rng.uniform(.03, .1)
    pts = []
    for g in gaps:
        da = TAU * g / tot
        for frac, d in ((0.0, amp * rng.uniform(.5, 1.2)),
                        (0.5, -amp * rng.uniform(.3, 1.0))):
            t = a + da * frac
            w = 1 + a2 * math.sin(2 * t + p2) + a3 * math.sin(3 * t + p3)
            pts.append((cx + (rx * w + d) * math.cos(t),
                        cy + (ry * w + d) * math.sin(t)))
        a += da
    return pts


def _thin_hidden(polys):
    """Drop the vertices of each outline that lie inside another: they are
    merged in one fill, so nobody sees them. About a third of a crown's bytes."""
    out = []
    for i, poly in enumerate(polys):
        hid = [any(_inside(q, o) for j, o in enumerate(polys) if j != i) for q in poly]
        n = len(poly)
        kept = [poly[k] for k in range(n)
                if not (hid[k] and hid[k - 1] and hid[(k + 1) % n])]
        out.append(kept if len(kept) >= 5 else poly)
    return out


def _hatch(rng, poly, deg, step, trim=0.3):
    """Rule lines cut through a polygon (svg_figures.hatch_poly), each one
    ended a little unevenly, as a graver ends them."""
    segs = []
    for a, b in F.hatch_poly(poly, deg, step, inset=0.6):
        t0 = rng.uniform(0, trim * .5)
        t1 = rng.uniform(0, trim)
        dx, dy = b[0] - a[0], b[1] - a[1]
        segs.append([(a[0] + dx * t0, a[1] + dy * t0),
                     (b[0] - dx * t1, b[1] - dy * t1)])
    return segs


def _shade_side(poly, cx, cy, lo=-115, hi=25):
    """The part of an outline on the side away from the light."""
    out = []
    for p in poly:
        ang = math.degrees(math.atan2(p[1] - cy, p[0] - cx))
        if lo <= ang <= hi:
            out.append(p)
    return out


def _dab(rng, x, y, ang, L, mat, wob=.55):
    a = ang + rng.uniform(-wob, wob)
    return ("line", [(x, y), (x + L * math.cos(a), y + L * math.sin(a))], mat)


def _cap(rng, cx, cy, rx, ry, leaf, w=.42, span=1.15):
    """The sunlit top of a mass: its edge toward the light with a fringe of leaf scallops
    on it, and a scalloped lower edge coming back. Thick in the middle, gone at the ends.
    This, not a blot in the middle, is what makes a mass read as a heap of leaves with
    the light on it."""
    light = math.atan2(LIGHT[1], LIGHT[0])
    r = math.sqrt((rx * rx + ry * ry) / 2)
    k = max(3, int(2 * span * r / max(leaf, 1)))
    outer, inner = [], []
    for i in range(k + 1):
        t = i / k
        a = light - span + 2 * span * t
        q = math.cos((t - .5) * math.pi)            # 0 at the ends, 1 midway
        f = (.5 if i % 2 else -.5) * (leaf / r) * rng.uniform(.5, 1.2) * min(1, q * 2)
        outer.append((cx + math.cos(a) * rx * (1 + f), cy + math.sin(a) * ry * (1 + f)))
        d = w * q * rng.uniform(.7, 1.25) + (.6 if i % 2 else -.1) * (leaf / r) * q
        inner.append((cx + math.cos(a) * rx * (1 - d), cy + math.sin(a) * ry * (1 - d)))
    return outer + inner[-2:0:-1]


# How thinly a crown's cut lines and leaf marks are laid. Measured in WebKit, in an <img>, under a
# moving camera: strokes inside the trees are the largest single cost of a frame, so this
# was set as far as the crowns still read as cut, and no further.
STROKE_THIN = 1.5


def foliage(rng, blobs, lobe=18.0, jag=.5, carve_step=6.0, carve_deg=52,
            dabs=1.0, dab_len=(3.5, 6), dab_ang="form", mid_k=.72, lit_k=.3,
            contour=True, wob=.5, collect=None, dark_marks=False):
    """A crown's leaf masses, as parts, in the engraver's way.

    Each mass is a dark shape, a body laid on it toward the light, and a scalloped
    cap along the edge the light strikes (`_cap`). Dark pockets are what is left
    between them, which is what gives a crown depth. The body's shaded half is CUT with
    parallel lines in the colour of the dark, as a graver cuts it, so the tone
    falls away by line and not by a flat edge. Light leaf marks gather round
    the cap; a few dark ones break the body's edge. The marks follow the form
    (`dab_ang="form"`, going round the mass), or lie one way (an angle), or any
    way (None). The contour runs only where the light catches the mass, and it
    runs broken.

    `blobs` is (cx, cy, rx, ry). `dabs` scales how many marks there are.
    """
    deep, mid, lit, carve, dk, lt = [], [], [], [], [], []
    outers = []
    carve_step *= STROKE_THIN
    dabs /= STROKE_THIN ** 2
    centres = []
    for cx, cy, rx, ry in blobs:
        o = lobed(rng, cx, cy, rx, ry, lobe, jag)
        outers.append(o)
        centres.append((cx, cy))
        deep.append(("fill", o, "deep"))
        sw = rng.uniform(-.14, .14)
        mx = cx + (LIGHT[0] + sw) * rx * .18
        my = cy + (LIGHT[1] + sw) * ry * .18
        mr = (rx * mid_k * rng.uniform(.92, 1.06),
              ry * mid_k * rng.uniform(.92, 1.06))
        m = lobed(rng, mx, my, mr[0], mr[1], lobe * 1.05, jag)
        mid.append(("fill", m, "mid"))
        if carve_step:
            sh = _shade_side(m, mx, my, -130, 38)
            if len(sh) >= 3:
                for seg in _hatch(rng, sh + [(mx - rx * .12, my + ry * .02)],
                                  carve_deg, carve_step):
                    carve.append(("line", seg, "carve"))
        if lit_k:
            lit.append(("fill", _cap(rng, mx, my, mr[0], mr[1], lobe * .62,
                                     lit_k * 1.5, rng.uniform(1.0, 1.25)), "lit"))
        n = int(rx * ry * .0065 * dabs)
        for _ in range(n):
            a = rng.uniform(0, TAU)
            r = math.sqrt(rng.uniform(.04, 1))
            u, v = r * math.cos(a), r * math.sin(a)
            x, y = cx + u * rx, cy + v * ry
            t = u * LIGHT[0] + v * LIGHT[1]        # how much it faces the light
            L = rng.uniform(*dab_len)
            if dab_ang == "form":
                ang = math.atan2(v, u) + math.pi / 2
            elif dab_ang is None:
                ang = rng.uniform(0, TAU)
            else:
                ang = dab_ang
            if t > .22:
                lt.append(_dab(rng, x, y, ang, L, "dab_lit", wob))
            elif t > -.05 and rng.random() < .5:
                dk.append(_dab(rng, x, y, ang, L, "dab_deep", wob))
    if collect is not None:
        collect.extend(outers)
    deep = [("fill", q, "deep") for q in _thin_hidden(outers)]
    out = deep + mid + carve + lit + (dk if dark_marks else []) + lt
    if contour:
        def lit_side(p):
            best = min(centres, key=lambda c: (c[0] - p[0]) ** 2
                       + (c[1] - p[1]) ** 2)
            dx, dy = p[0] - best[0], p[1] - best[1]
            L = math.hypot(dx, dy) or 1
            return (dx * LIGHT[0] + dy * LIGHT[1]) / L > .12
        for r in _runs(outers, keep=lit_side):
            cur = []
            for q in r:
                if rng.random() < .13 or len(cur) > 9:
                    if len(cur) >= 3:
                        out.append(("line", cur, "contour"))
                    cur = []
                else:
                    cur.append(q)
            if len(cur) >= 3:
                out.append(("line", cur, "contour"))
    return out


def _taper_poly(joints, widths):
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
    return left + right[::-1]


def limbs(rng, specs, flow=1, tick_step=18.0):
    """A trunk and its boughs, as parts: the wood, a shadow down the side away
    from the light, long lines of grain following each limb, cross-contour
    ticks in the shadow, and one contour round the union of it.

    `specs` is (joints, widths). Authored first, so boughs run into the crown
    that is drawn over them.
    """
    fills, shade, grain, ticks = [], [], [], []
    polys = []
    for joints, widths in specs:
        dense = F.smooth(joints, closed=False, n=2)
        ws = []
        tot = len(dense) - 1
        m = len(widths) - 1
        for i in range(len(dense)):
            t = i / tot * m
            k = min(int(t), m - 1)
            ws.append(widths[k] + (widths[k + 1] - widths[k]) * (t - k))
        poly = _taper_poly(dense, ws)
        polys.append(poly)
        fills.append(("fill", poly, "wood"))
        nrm = []
        for i in range(len(dense)):
            a = dense[max(i - 1, 0)]
            b = dense[min(i + 1, len(dense) - 1)]
            dx, dy = b[0] - a[0], b[1] - a[1]
            L = math.hypot(dx, dy) or 1
            nx, ny = dy / L, -dx / L
            if nx * LIGHT[0] + ny * LIGHT[1] > 0:
                nx, ny = -nx, -ny
            nrm.append((nx, ny, dx / L, dy / L))
        if max(widths) >= 13:
            inner = [(p[0] + n[0] * w * .08, p[1] + n[1] * w * .08)
                     for p, n, w in zip(dense, nrm, ws)][::2]
            outer = [(p[0] + n[0] * w * .5, p[1] + n[1] * w * .5)
                     for p, n, w in zip(dense, nrm, ws)][::2]
            shade.append(("fill", inner + outer[::-1], "wood_deep"))
        if max(widths) >= 20:
            for k in range(flow if max(widths) >= 30 else min(flow, 2)):
                off = rng.uniform(-.42, .3)
                st = rng.randint(0, 2)
                en = len(dense) - rng.randint(0, 3)
                run = [(p[0] + n[0] * w * off, p[1] + n[1] * w * off)
                       for p, n, w in list(zip(dense, nrm, ws))[st:en]]
                if len(run) >= 3:
                    grain.append(("line", run, "grain"))
        run = 0.0
        for i in range(1, len(dense)):
            L = math.hypot(dense[i][0] - dense[i - 1][0],
                           dense[i][1] - dense[i - 1][1])
            run += L
            if run < tick_step or ws[i] < 8:
                continue
            run = 0
            nx, ny, dx, dy = nrm[i]
            w = ws[i] / 2
            frac = rng.uniform(.35, .85)
            ax, ay = dense[i][0] + nx * w * .95, dense[i][1] + ny * w * .95
            bx = dense[i][0] + nx * w * (.95 - frac) - dx * 2.6
            by = dense[i][1] + ny * w * (.95 - frac) - dy * 2.6
            ticks.append(("line", [(ax, ay), (bx, by)], "bark"))
    out = fills + shade + grain + ticks
    for r in _runs(polys, min_pts=2):
        out.append(("line", r, "wood_line"))
    return out


def crown_contour(rng, outers, gap=.12, maxlen=11):
    """The contour of a whole crown, drawn only against the sky and only where
    the light catches it, in short broken runs. Storeyed crowns call this once
    (with what `foliage(collect=...)` gathered) rather than letting each storey
    wire itself over the one behind."""
    xs = [p[0] for o in outers for p in o]
    ys = [p[1] for o in outers for p in o]
    gx, gy = sum(xs) / len(xs), sum(ys) / len(ys)

    def lit_side(p):
        dx, dy = p[0] - gx, p[1] - gy
        L = math.hypot(dx, dy) or 1
        return (dx * LIGHT[0] + dy * LIGHT[1]) / L > -.35
    out = []
    for r in _runs(outers, keep=lit_side):
        cur = []
        for q in r:
            if rng.random() < gap or len(cur) > maxlen:
                if len(cur) >= 3:
                    out.append(("line", cur, "contour"))
                cur = []
            else:
                cur.append(q)
        if len(cur) >= 3:
            out.append(("line", cur, "contour"))
    return out


# ---------------------------------------------------------------------------
# Paint
# ---------------------------------------------------------------------------

INK = (168, 178, 128)           # the one ink of the scenery


def _mix(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))


def sheet(deep, mid, lit, ink=INK, wood=(96, 80, 60), wood_deep=None,
          wood_ink=None, hatch=None, dab=(2.2, 2.2, 2.2), **extra):
    """A paint table: material -> (fill, stroke, width)."""
    wi = wood_ink or ink
    wd = wood_deep or (wood[0] * .52, wood[1] * .52, wood[2] * .55)
    t = {"rule": (None, ink, 1.0),
         "deep": (deep, None, 0), "mid": (mid, None, 0), "lit": (lit, None, 0),
         "hatch": (None, _mix(deep, mid, .55), 1.0),
         "carve": (None, hatch or _mix(deep, mid, .12), 1.15),
         "dab_deep": (None, deep, dab[0]), "dab_mid": (None, mid, dab[1]),
         "dab_lit": (None, lit, dab[2]),
         "contour": (None, ink, 1.0), "wood": (wood, None, 0),
         "wood_deep": (wd, None, 0), "grain": (None, wd, 1.0),
         "bark": (None, wi, .8), "wood_line": (None, wi, 1.1)}
    t.update(extra)
    return t


# ---------------------------------------------------------------------------
# The trees
# ---------------------------------------------------------------------------

def shade_tree(seed=11):
    """The broad shade tree (a terebinth): a short massive trunk, thick forks,
    a wide dome of big separate masses with deep shade under it. Height about
    3.8 men, spread about 5.

    Call: `render(shade_tree(), SHADE_PAINT)` for its SVG, card px, feet at the origin. In a
    scene it is `place("s", x, y, k)`; `forest()` says where each one stands."""
    rng = random.Random(seed)
    P = limbs(rng, [
        ([(-30, 0), (-20, 16), (-8, 30)], [18, 18, 12]),
        ([(34, 0), (22, 14), (10, 30)], [20, 18, 12]),
        ([(0, 0), (-5, 44), (-1, 88), (5, 122)], [60, 44, 38, 32]),
        ([(0, 100), (-52, 150), (-112, 205), (-172, 236)], [28, 19, 12, 6]),
        ([(3, 112), (-25, 172), (-50, 242), (-70, 292)], [24, 16, 10, 5]),
        ([(6, 114), (30, 176), (45, 252), (40, 312)], [24, 16, 10, 5]),
        ([(6, 104), (62, 152), (126, 196), (192, 226)], [28, 19, 12, 6]),
        ([(-42, 146), (-102, 162), (-166, 166)], [13, 8, 4]),
        ([(52, 146), (106, 166), (172, 168)], [13, 8, 4]),
    ])
    P += foliage(rng, [
        (-192, 214, 52, 36), (-124, 186, 46, 28), (-200, 268, 54, 44),
        (-120, 276, 74, 54), (-46, 330, 80, 50), (56, 336, 82, 46),
        (138, 282, 76, 54), (206, 232, 54, 40), (122, 192, 56, 30),
        (6, 254, 68, 52), (-64, 212, 50, 30), (70, 244, 52, 38),
    ], lobe=27, dabs=.5, carve_step=7.2)
    return P


SHADE_PAINT = sheet((24, 42, 30), (52, 84, 50), (92, 128, 66),
                    dab=(2.1, 2.0, 2.0),
                    **{"dab_lit": (None, (134, 166, 92), 2.0)})


def olive(seed=23):
    """The olive: a short, wide, twisted double trunk with a gap in it, and a
    broken silver crown of many small flat masses with sky between them.

    Call: `render(olive(), OLIVE_PAINT)` for its SVG, card px, feet at the origin. In a
    scene it is `place("o", x, y, k)`; `forest()` says where each one stands."""
    rng = random.Random(seed)
    P = limbs(rng, [
        ([(-16, 0), (-26, 30), (-8, 62), (-26, 98)], [40, 30, 26, 20]),
        ([(18, 0), (26, 32), (10, 60), (30, 102)], [36, 26, 22, 18]),
        ([(-26, 96), (-62, 130), (-108, 150)], [18, 10, 4]),
        ([(-24, 96), (-30, 142), (-54, 192)], [14, 9, 4]),
        ([(30, 100), (70, 130), (118, 150)], [16, 10, 4]),
        ([(30, 100), (22, 150), (44, 202)], [14, 9, 4]),
        ([(0, 80), (2, 130), (-6, 180)], [12, 8, 4]),
    ])
    P += foliage(rng, [
        (-122, 158, 40, 22), (-68, 142, 34, 18), (-96, 196, 46, 26),
        (-44, 186, 38, 22), (-58, 232, 42, 22), (6, 226, 46, 26),
        (0, 176, 32, 18), (54, 190, 40, 24), (66, 232, 34, 18),
        (112, 186, 44, 26), (130, 152, 34, 20), (72, 146, 32, 16),
    ], lobe=19, carve_step=5.6, dab_len=(4, 8), dab_ang=.95, dabs=1.15,
        mid_k=.74, lit_k=.34)
    return P


OLIVE_PAINT = sheet((40, 52, 50), (82, 98, 86), (124, 140, 118),
                    wood=(112, 102, 86), ink=(190, 198, 168),
                    dab=(1.3, 1.3, 1.3),
                    **{"dab_lit": (None, (172, 184, 158), 1.3)})


def fig_leaf(r=20.0):
    """One fig leaf on its own, in parts, for a hand to hold or a thread to
    sew (3:7): the outline, a midrib and two side veins.

    Call: `render(fig_leaf(20), {"leaf": (fill, stroke, w), "vein": (None, stroke, w)})`; stem at the origin."""
    P = [("fill", F.fig_leaf_outline(0, 0, r, 0), "leaf"),
         ("line", [(0, -r * .10), (0, r * .86)], "vein"),
         ("line", [(0, r * .25), (r * .34, r * .46)], "vein"),
         ("line", [(0, r * .25), (-r * .34, r * .46)], "vein")]
    return P


def fig(seed=31, close=False):
    """The fig: low and wide, several pale smooth stems forking from the
    ground, and a crown you can see the separate big leaves of. `close` is the
    same tree for a camera that comes in on its crown: each leaf followed by its
    own midrib, to be drawn a leaf at a time (`render(..., whole=WHOLE_LEAVES)`), so
    that a leaf in front hides the outlines of those behind it.

    Call: `render(fig(), FIG_PAINT)` for its SVG, card px, feet at the origin. In a
    scene it is `place("f", x, y, k)`; `forest()` says where each one stands. The
    near fig, the one seen close, is `fig_near_svg()`."""
    rng = random.Random(seed)
    P = limbs(rng, [
        ([(-12, 0), (-34, 46), (-72, 90), (-122, 116)], [20, 14, 9, 4]),
        ([(0, 0), (-2, 60), (-14, 122), (-24, 172)], [22, 14, 9, 4]),
        ([(14, 0), (42, 50), (82, 100), (128, 128)], [20, 14, 9, 4]),
        ([(-52, 72), (-48, 118), (-74, 158)], [9, 6, 3]),
        ([(60, 74), (58, 122), (84, 160)], [9, 6, 3]),
    ], flow=1, tick_step=14)
    blobs = [(-104, 118, 50, 30), (-58, 152, 50, 34), (6, 178, 54, 34),
             (64, 152, 50, 34), (112, 122, 50, 30), (0, 118, 46, 28)]
    P += foliage(rng, blobs, lobe=26, jag=.45, dabs=0, carve_step=7,
                 mid_k=.7, lit_k=0, contour=False)
    leaves, lit, veins = [], [], []
    ribs = {}                   # each leaf's midrib, if it has one, by the leaf's first point
    spots = []
    for cx, cy, rx, ry in blobs:
        for _ in range(int(rx * ry * .0026) + 2):
            a = rng.uniform(0, TAU)
            r = rng.uniform(.25, 1.25)
            spots.append((cx + rx * r * math.cos(a), cy + ry * r * math.sin(a),
                          (a - math.pi / 2 + rng.uniform(-.7, .7))))
    spots.sort(key=lambda q: -q[1])
    for x, y, rot in spots:
        r = rng.uniform(20, 28)
        o = F.fig_leaf_outline(x, y, r, rot)
        t = ((x - 0) * LIGHT[0] + (y - 140) * LIGHT[1]) / 160
        (lit if t + rng.uniform(-.25, .25) > .15 else leaves).append(
            ("fill", o, "leaf_lit" if t > .15 else "leaf"))
        ca, sa = math.cos(rot), math.sin(rot)
        if t > .15:
            veins.append(("line", [(x, y), (x - sa * r * .8, y + ca * r * .8)],
                          "vein"))
            ribs[o[0]] = [veins[-1]]
    lit = [("fill", q[1], "leaf_lit") for q in lit]
    if close:
        P += [q for leaf in leaves + lit for q in [leaf] + ribs.get(leaf[1][0], [])]
    else:
        P += leaves + lit + veins
    for _ in range(7):
        x, y = rng.uniform(-100, 100), rng.uniform(96, 150)
        P.append(("dot", (x, y, 3.2), "pip"))
    return P


FIG_PAINT = sheet((30, 50, 30), (56, 86, 44), (108, 136, 62),
                  wood=(136, 128, 112), ink=(178, 190, 128),
                  dab=(2.0, 2.0, 2.0),
                  leaf=((72, 106, 52), (150, 170, 104), .8),
                  leaf_lit=((104, 138, 66), (178, 196, 120), .8),
                  vein=(None, (38, 62, 34), .8),
                  pip=(None, (70, 68, 50), 7))


def _frond(rng, base, ang, L, droop, wide=17.0, teeth=10):
    """One feather frond: a rachis that arches under its own weight, leaflets
    on both sides cut as a saw. Returns (blade outline, rachis)."""
    x, y = base
    a = ang
    side = 1 if math.cos(ang) >= 0 else -1
    seg = L / teeth
    spine = []
    for i in range(teeth + 1):
        spine.append((x, y))
        x += seg * math.cos(a)
        y += seg * math.sin(a)
        a -= side * droop
    up, dn = [], []
    for i in range(1, len(spine)):
        px, py = spine[i - 1]
        qx, qy = spine[i]
        dx, dy = (qx - px) / seg, (qy - py) / seg
        nx, ny = -dy, dx
        t = i / teeth
        w = wide * math.sin(min(1.0, t * 1.25) * math.pi * .86) ** .7 + 1.5
        fw = seg * 1.15
        up.append((px + nx * w * .85 + dx * fw, py + ny * w * .85 + dy * fw))
        up.append((qx + nx * .8, qy + ny * .8))
        dn.append((px - nx * w * 1.05 + dx * fw, py - ny * w * 1.05 + dy * fw))
        dn.append((qx - nx * .8, qy - ny * .8))
    return [spine[0]] + up + dn[::-1], spine


def date_palm(seed=41):
    """The date palm: one tall ringed trunk with a slight bend, a burst of
    arching feather fronds, and dates hanging under them.

    Call: `render(date_palm(), PALM_PAINT)` for its SVG, card px, feet at the origin. In a
    scene it is `place("p", x, y, k)`; `forest()` says where each one stands."""
    rng = random.Random(seed)
    trunk = [(0, 0), (9, 90), (6, 200), (-6, 310), (-12, 368)]
    dense = F.smooth(trunk, closed=False, n=4)
    ws = [30 - 12 * (i / (len(dense) - 1)) for i in range(len(dense))]
    P = [("fill", _taper_poly(dense, ws), "wood")]
    # the shadow side, then a ring at each frond's old base
    P.append(("fill", [(p[0] + w * .1, p[1]) for p, w in zip(dense, ws)] +
              [(p[0] + w * .5, p[1]) for p, w in zip(dense, ws)][::-1],
              "wood_deep"))
    for i, y in enumerate(range(10, 350, 13)):
        t = y / 368
        k = t * (len(dense) - 1)
        p = dense[int(k)]
        w = ws[int(k)] / 2
        P.append(("line", [(p[0] - w, y - 2), (p[0] + w, y + 2)], "ring"))
    P.append(("line", [(p[0] - w / 2, p[1]) for p, w in zip(dense, ws)][::3],
              "wood_line"))
    P.append(("line", [(p[0] + w / 2, p[1]) for p, w in zip(dense, ws)][::3],
              "wood_line"))
    top = (-12, 372)
    # old stubs under the crown
    for k in range(5):
        a = -2.7 + k * .55
        P.append(("fill", F.taper(
            [(top[0], top[1] - 8), (top[0] + 26 * math.cos(a),
                                    top[1] - 8 + 22 * math.sin(a))],
            [6, 2], round_end=False), "wood_deep"))
    back, front, spines = [], [], []
    angs = [(-.15, 150), (.3, 150), (.85, 132), (1.42, 116),
            (2.05, 124), (2.6, 140), (3.0, 152), (3.3, 148)]
    for a, L in angs:
        o, sp = _frond(rng, top, a + rng.uniform(-.08, .08),
                       L * rng.uniform(.94, 1.06), .125, 15)
        back.append(("fill", o, "frond_deep"))
    for a, L in [(.08, 138), (.62, 128), (1.2, 110), (1.7, 108),
                 (2.28, 126), (2.72, 138), (3.08, 142)]:
        o, sp = _frond(rng, (top[0], top[1] + 2), a + rng.uniform(-.06, .06),
                       L * rng.uniform(.94, 1.06), .145, 16)
        front.append(("fill", o, "frond"))
        spines.append(("line", sp[::2] + [sp[-1]], "frond_line"))
    P += back + front + spines
    # the dates
    for sx, n in ((-1, 7), (1, 8)):
        cx, cy = top[0] + sx * 15, top[1] - 16
        for k in range(n):
            P.append(("dot", (cx + sx * (k % 3) * 4.6 + rng.uniform(-1, 1),
                              cy - k * 3.4, 2.5), "pip"))
    return P


PALM_PAINT = sheet((36, 54, 32), (70, 96, 48), (110, 134, 62),
                   wood=(110, 88, 62), ink=(176, 184, 118),
                   frond=((88, 116, 52), (170, 182, 106), .6),
                   frond_deep=((42, 66, 38), (84, 108, 62), .6),
                   frond_line=(None, (178, 190, 112), 1.0),
                   ring=(None, (46, 36, 28), 1.2),
                   pip=(None, (176, 116, 58), 5.6))


def cypress(seed=53):
    """The cypress: a tall dark flame, its masses running upward, with hardly
    any trunk showing. The straightest thing in the garden, and a mark for how
    far away a place is.

    Call: `render(cypress(), CYPRESS_PAINT)` for its SVG, card px, feet at the origin. In a
    scene it is `place("c", x, y, k)`; `forest()` says where each one stands."""
    rng = random.Random(seed)
    H = 476.0
    P = limbs(rng, [([(0, 0), (1, 34)], [18, 15])], flow=1)
    left, right = [], []
    n = 22
    for i in range(n + 1):
        t = i / n
        w = 46 * (math.sin(math.pi * t ** .72) ** .72) + .5
        y = 26 + (H - 26) * t
        j = (i % 2 == 0) * 5.0
        left.append((-w - j * rng.uniform(.4, 1.0) * (1 - t * .6), y + j))
        right.append((w + j * rng.uniform(.4, 1.0) * (1 - t * .6), y + j))
    o = left + right[::-1]
    P.append(("fill", o, "deep"))
    # the flame masses that run up it
    mids = []
    for k in range(10):
        t = rng.uniform(.04, .78)
        y0 = 26 + (H - 26) * t
        L = rng.uniform(70, 130)
        w0 = 46 * (math.sin(math.pi * t ** .72) ** .72)
        cx = -w0 * rng.uniform(.05, .55)
        wid = rng.uniform(7, 13)
        mids.append(("fill", [(cx, y0), (cx - wid, y0 + L * .28),
                              (cx - wid * .7, y0 + L * .6),
                              (cx + 2, y0 + L), (cx + wid * .8, y0 + L * .55),
                              (cx + wid, y0 + L * .24)], "mid"))
    P += mids
    P += [("line", seg, "hatch") for seg in
          _hatch(rng, [(x * .9 + 2, y) for x, y in right] + [(4, H - 40), (4, 40)],
                 84, 6.0, trim=.45)]
    for _ in range(100):
        t = rng.uniform(.02, .95)
        y = 26 + (H - 26) * t
        w0 = 46 * (math.sin(math.pi * t ** .72) ** .72)
        x = rng.uniform(-1.02, 1.02) * w0
        L = rng.uniform(7, 15)
        k = (x / (w0 + 1)) * LIGHT[0] * 1.2 + rng.uniform(-.35, .35)
        mat = "dab_lit" if k > .22 else ("dab_mid" if k > -.2 else "dab_deep")
        P.append(_dab(rng, x, y, math.pi / 2 + x / 120, L, mat, .16))
    run = [q for q in left]
    cur = []
    for q in run:
        if rng.random() < .1:
            if len(cur) >= 3:
                P.append(("line", cur, "contour"))
            cur = []
        else:
            cur.append(q)
    if len(cur) >= 3:
        P.append(("line", cur, "contour"))
    return _gather(P, ("dab_deep", "dab_mid", "dab_lit"))


CYPRESS_PAINT = sheet((20, 36, 34), (34, 60, 50), (58, 92, 70),
                      wood=(84, 70, 54), ink=(150, 172, 128),
                      dab=(2.0, 2.2, 2.0),
                      **{"dab_lit": (None, (92, 128, 88), 2.0)})


def _gather(P, mats):
    """Move the parts of the given materials together, in place of the first
    of them, so each becomes one path."""
    out, held = [], {m: [] for m in mats}
    idx = None
    for q in P:
        if q[2] in held:
            if idx is None:
                idx = len(out)
            held[q[2]].append(q)
        else:
            out.append(q)
    if idx is None:
        return P
    ins = []
    for m in mats:
        ins += held[m]
    return out[:idx] + ins + out[idx:]


def pomegranate(seed=61):
    """The pomegranate: a thin-stemmed many-branched bush of a tree, its crown
    a dense round of small glossy masses, its fruit dull red and small, each
    with its little crown. Kept dull: the bright fruit in this garden is the
    other tree's.

    Call: `render(pomegranate(), POMEGRANATE_PAINT)` for its SVG, card px, feet at the origin. In a
    scene it is `place("g", x, y, k)`; `forest()` says where each one stands."""
    rng = random.Random(seed)
    P = limbs(rng, [
        ([(-6, 0), (-16, 40), (-40, 84), (-74, 118)], [12, 9, 6, 3]),
        ([(0, 0), (2, 52), (-8, 106), (-14, 150)], [13, 9, 6, 3]),
        ([(8, 0), (20, 44), (46, 86), (82, 112)], [12, 9, 6, 3]),
        ([(-30, 72), (-62, 80), (-96, 78)], [6, 4, 2]),
        ([(36, 72), (70, 78), (102, 72)], [6, 4, 2]),
    ], flow=0, tick_step=12)
    blobs = [(-84, 110, 34, 24), (-50, 132, 36, 26), (-92, 74, 22, 15),
             (-6, 162, 40, 28), (44, 134, 38, 26), (86, 106, 34, 24),
             (98, 70, 22, 15), (0, 110, 38, 26), (-42, 92, 26, 18),
             (42, 90, 26, 18)]
    P += foliage(rng, blobs, lobe=19, carve_step=5.6, dab_len=(2.5, 4.5),
                 dabs=.9, mid_k=.74, lit_k=.32)
    spots = ((-92, 62), (-52, 96), (-20, 134), (30, 108), (62, 124),
             (92, 86), (12, 80), (-60, 138), (48, 72))
    for x, y in spots:
        P.append(("dot", (x, y, 5.0), "fruit"))
    for x, y in spots:
        P.append(("line", [(x - 2.2, y - 4.6), (x, y - 7.2), (x + 2.2, y - 4.6)],
                  "calyx"))
    return P


POMEGRANATE_PAINT = sheet((26, 46, 30), (50, 84, 48), (84, 118, 62),
                          wood=(92, 74, 56), ink=(170, 180, 120),
                          dab=(1.6, 1.6, 1.6),
                          **{"dab_lit": (None, (128, 158, 84), 1.6)},
                          fruit=((152, 80, 70), (210, 150, 120), .8),
                          calyx=(None, (210, 150, 120), .9))


# ---------------------------------------------------------------------------
# The two named trees
# ---------------------------------------------------------------------------

def tree_of_life(seed=71):
    """The tree of life: the tallest thing in the garden, and pale. A massive
    bare fluted trunk goes up a long way before it opens, like a cup, into
    limbs that all rise and fork and fork again. Nothing else here has that
    shape: every other crown is a dome, a column or a burst, and this is a
    goblet, wide and flat-domed at the top, with the sky showing under it.
    Pale fruit hang in its crown in small clusters. 2:9 says only where it
    stands; the shape is the drawing's own. Height about 6 men.

    Call: `render(tree_of_life(), LIFE_PAINT)`, foot at the origin. In a scene it stands at
    LIFE_XY: `panorama` draws it, or `heroes_svg(grow=...)` does on its word."""
    rng = random.Random(seed)
    L = [([(0, 0), (-2, 70), (2, 150), (0, 238)], [86, 64, 54, 44])]

    def fork(x, y, ang, length, w, depth):
        """A limb that rises, bends a little and forks."""
        bend = rng.uniform(-.1, .1)
        mx = x + length * .55 * math.cos(ang)
        my = y + length * .55 * math.sin(ang)
        ex = x + length * math.cos(ang + bend)
        ey = y + length * math.sin(ang + bend)
        L.append(([(x, y), (mx, my), (ex, ey)], [w, w * .72, w * .5]))
        if depth:
            spread = rng.uniform(.3, .42)
            fork(ex, ey, ang + bend + spread * .5 + .06, length * .7, w * .5,
                 depth - 1)
            fork(ex, ey, ang + bend - spread * .5 - .06, length * .7, w * .5,
                 depth - 1)
    for ang, ln, w, d in ((1.57, 190, 30, 1), (1.27, 170, 28, 1),
                          (1.87, 170, 28, 1), (.94, 170, 24, 1),
                          (2.2, 170, 24, 1), (.62, 160, 18, 1),
                          (2.52, 160, 18, 1)):
        fork(0 + math.cos(ang) * 8, 210, ang, ln, w, d)
    # the roots, running out over the ground, the two long ones thinning to nothing as they go
    # into it, so that close up a tip is a root's and not a cut-off limb's
    L += [([(-30, 28), (-74, 10), (-128, -3)], [34, 18, 1]),
          ([(32, 26), (76, 8), (134, -3)], [34, 18, 1]),
          ([(-14, 14), (-40, 0), (-66, -8)], [22, 12, 4]),
          ([(14, 14), (46, -2), (84, -8)], [22, 12, 4])]
    P = limbs(rng, L, flow=5, tick_step=16)
    back = [(-254, 416, 62, 40), (254, 410, 62, 40), (-190, 472, 76, 50),
            (190, 468, 76, 50), (-108, 530, 84, 54), (108, 534, 84, 54),
            (0, 566, 92, 50), (-160, 526, 44, 28), (160, 524, 44, 28)]
    front = [(-218, 392, 44, 24), (220, 386, 44, 24), (-146, 436, 56, 34),
             (146, 432, 56, 34), (-64, 486, 64, 42), (66, 490, 64, 42),
             (0, 508, 50, 34)]
    out = []
    P += foliage(rng, back, lobe=23, dabs=.55, contour=False, collect=out)
    P += foliage(rng, front, lobe=22, dabs=.55, contour=False, collect=out)
    P += crown_contour(rng, out)
    fruit = []
    for cx, cy, rx, ry in back + front:
        for k in range(rng.randint(1, 2)):
            fx = cx + rng.uniform(-.7, .7) * rx
            fy = cy - ry * rng.uniform(.25, .72)
            for dx, dy in ((0, 0), (5.2, -3.6), (-4.8, -4.4)):
                fruit.append(("dot", (fx + dx, fy + dy, 3.3), "pip"))
    P += fruit
    return P


LIFE_PAINT = sheet((52, 74, 66), (102, 128, 106), (156, 176, 138),
                   wood=(168, 160, 134), wood_deep=(96, 92, 80),
                   ink=(222, 224, 190), hatch=(84, 108, 92),
                   dab=(2.0, 2.0, 2.0),
                   **{"dab_lit": (None, (206, 212, 170), 2.0)},
                   pip=(None, (232, 208, 130), 7.5))


# Where a leaf_oval's midrib runs, as parts of its length: from inside its rounded base, which
# the curve drawn through the oval's points leaves about a tenth of the way along, to near its tip
MIDRIB = (.14, .84)
# The materials of leaves that are seen close, drawn one at a time (`render(..., whole=...)`), so
# that a leaf in front hides the outlines of those behind it
WHOLE_LEAVES = ("leaf", "leaf_lit")


def leaf_oval(x, y, L, W, ang):
    """A plain pointed leaf, stem at (x, y): wider than a blade, with a tip."""
    ca, sa = math.cos(ang), math.sin(ang)
    out = []
    for px, py in ((0, 0), (.42 * L, W * .55), (.78 * L, W * .32), (L, 0),
                   (L, 0), (.78 * L, -W * .32), (.42 * L, -W * .55)):
        out.append((x + px * ca - py * sa, y + px * sa + py * ca))
    return out


def knowledge_fruit(r=1.0):
    """One fruit of the tree of knowledge, hanging from its stem at the
    origin: parts. Plump and a little uneven, a stem, a little crown at its
    foot, a lit shoulder and a hatched shadow side. It is good to look at
    (3:6), which is the point; it carries no mark of any kind.

    Call: `render(knowledge_fruit(.82), FRUIT_PAINT, prec=1)`, or `place("kf", x, y)` in a scene, where
    (x, y) is the point its stem hangs from. A hand that takes one carries this drawing."""
    k = r
    def sc(pts):
        return [(x * k, y * k) for x, y in pts]
    P = [("line", sc([(0, 0), (.6, -3), (0, -5.4)]), "stem")]
    P.append(("fill", sc([(-.4, -4.8), (4.2, -4.6), (7.2, -8.6), (7.2, -13.6),
                          (3.8, -17.6), (.2, -17.2), (-3.8, -17.8), (-7.4, -13.6),
                          (-7.2, -8.4), (-4.4, -4.8)]), "fruit"))
    P.append(("fill", sc([(1.6, -5.8), (5.8, -8.8), (6.2, -13.6), (2.6, -16.6),
                          (3.8, -12.8), (3.6, -8.8)]), "fruit_deep"))
    P.append(("fill", sc([(-5, -8.2), (-2.6, -6.8), (-1.6, -8.6), (-3.8, -11.6),
                          (-5.6, -11.2)]), "fruit_hi"))
    for a, b in (((2.6, -8), (4.8, -7)), ((3, -10.4), (5.8, -9.8)),
                 ((3, -12.8), (5.8, -12.8)), ((2.4, -15), (4.8, -15.4))):
        P.append(("line", sc([a, b]), "fruit_hatch"))
    for a, b in (((-1.4, -17.6), (-1.8, -18.8)), ((0, -17.4), (0, -19)),
                 ((1.4, -17.6), (1.8, -18.8))):
        P.append(("line", sc([a, b]), "calyx"))
    return P


FRUIT_PAINT = {"stem": (None, (150, 130, 90), 1.1),
               "fruit": ((246, 178, 76), (255, 236, 190), .9),
               "fruit_deep": ((198, 100, 46), None, 0),
               "fruit_hi": ((255, 228, 160), None, 0),
               "fruit_hatch": (None, (128, 56, 32), .8),
               "calyx": (None, (240, 212, 160), .9)}

# Where the fruit hang, units from the foot of the trunk. The first three are
# the ones a hand can reach: stand a figure on the ground beside them.
KNOWLEDGE_FRUIT_LOW = [(344, 64), (320, 80), (296, 86)]
# the same at the west end of the crown, on the side toward the tree of life
KNOWLEDGE_FRUIT_WEST = [(-344, 64), (-320, 80), (-296, 86)]


def tree_of_knowledge(seed=83):
    """The tree of the knowledge of good and evil: the other thing the eye goes to,
    and as unlike the tree of life as the same pencil can make it. Where that one is
    tall, pale and rising, this one is low, wide and heavy: two trunks wound round each
    other, great boughs that go out and come down under their own weight, a crown like a
    roof, and the only copper in the garden, hung everywhere with the brightest colour
    in it. It should look good: "pleasant to the sight, and good for food" (2:9), "a
    delight to the eyes" (3:6). Nothing marks it as forbidden and nothing about it is
    sinister. The boughs' ends come down to a hand.

    Returns the tree without its fruit: see `knowledge_fruit_spots` and `heroes_svg`.
    Each fruit is its own <use>, so a hand can take one.

    Call: `render(tree_of_knowledge(), KNOWLEDGE_PAINT, whole=WHOLE_LEAVES)`, foot at the
    origin. In a scene it stands at KNOWLEDGE_XY: `panorama` draws it, or
    `heroes_svg(taken=..., grow=...)` does."""
    rng = random.Random(seed)
    L = [([(-40, 0), (-34, 30), (14, 72), (20, 102), (-22, 142)],
          [34, 30, 26, 24, 20]),
         ([(-22, 136), (-82, 182), (-172, 208), (-252, 188), (-302, 134),
           (-320, 96)], [26, 18, 12, 8, 5, 3]),
         ([(0, 142), (-8, 216), (-24, 292)], [18, 12, 5]),
         ([(-12, 150), (-62, 222), (-122, 284)], [14, 9, 4]),
         ([(-172, 206), (-216, 166), (-234, 116)], [8, 5, 3])]
    R = [([(40, 0), (32, 30), (-10, 70), (-20, 102), (24, 142)],
          [34, 30, 26, 24, 20]),
         ([(24, 136), (86, 186), (178, 210), (260, 188), (306, 134),
           (318, 92)], [26, 18, 12, 8, 5, 3]),
         ([(8, 142), (42, 222), (90, 292)], [16, 10, 4]),
         ([(178, 208), (224, 162), (242, 108)], [8, 5, 3]),
         ([(-40, 16), (-84, 4), (-120, 0)], [20, 10, 4]),
         ([(44, 16), (88, 4), (126, 0)], [20, 10, 4])]
    P = limbs(rng, L + R, flow=3, tick_step=16)
    back = [(-212, 276, 118, 52), (-76, 326, 136, 48), (80, 330, 136, 46),
            (216, 280, 120, 52), (0, 276, 150, 50), (-140, 300, 90, 40), (146, 304, 90, 40)]
    mid = [(-290, 214, 76, 46), (-150, 246, 104, 44), (152, 250, 106, 44),
           (292, 212, 78, 46), (0, 240, 110, 36), (-70, 282, 90, 30), (76, 286, 90, 30)]
    hang = [(-330, 152, 34, 34), (-262, 158, 44, 34), (-196, 186, 52, 26),
            (202, 188, 52, 26), (266, 158, 44, 34), (334, 148, 34, 36)]
    out = []
    kw = dict(mid_k=.8, lit_k=.2, carve_step=9.0, contour=False, collect=out, dark_marks=True)
    P += foliage(rng, back, lobe=30, dabs=.3, **kw)
    P += foliage(rng, mid, lobe=27, dabs=.34, **kw)
    P += foliage(rng, hang, lobe=20, dabs=.5, **kw)
    P += crown_contour(rng, out)
    # the leaves at the ends of the boughs, each one drawn: this is where a
    # hand comes in close. Each leaf is followed by its own midrib, to be drawn a
    # leaf at a time (WHOLE_LEAVES), the lit ones over the rest
    leaves, lit, twigs = [], [], []
    for sx, tips in ((1, [(q[0], q[1] + 6) for q in KNOWLEDGE_FRUIT_LOW]),
                     (-1, [(q[0], q[1] + 6) for q in KNOWLEDGE_FRUIT_WEST])):
        for tx, ty in tips:
            twigs.append(("line", [(tx - sx * 2, ty + 34), (tx + sx * 1, ty + 12),
                                   (tx, ty)], "twig"))
            for k in range(5):
                ang = -math.pi / 2 + (k - 2) * .62 + rng.uniform(-.2, .2)
                LL = rng.uniform(19, 26)
                bx, by = tx + rng.uniform(-3, 3), ty + rng.uniform(2, 14)
                ca, sa = math.cos(ang), math.sin(ang)
                o = leaf_oval(bx, by, LL, 10, ang)
                rib = [(bx + LL * u * ca, by + LL * u * sa) for u in MIDRIB]
                (lit if ca < 0 else leaves).append(
                    [("fill", o, "leaf_lit" if ca < 0 else "leaf"), ("line", rib, "vein")])
    return P + twigs + [q for leaf in leaves + lit for q in leaf]


KNOWLEDGE_PAINT = sheet((78, 42, 38), (132, 76, 52), (180, 122, 74),
                        wood=(112, 76, 56), wood_deep=(54, 34, 32),
                        ink=(214, 176, 132), wood_ink=(206, 170, 134),
                        hatch=(96, 54, 42), dab=(2.2, 2.2, 2.2),
                        **{"dab_lit": (None, (206, 152, 96), 2.2)},
                        twig=(None, (132, 96, 68), 1.4),
                        leaf=((142, 80, 50), (214, 172, 124), .8),
                        leaf_lit=((186, 122, 70), (232, 192, 140), .8),
                        vein=(None, (76, 40, 32), .8))


def knowledge_fruit_spots(seed=97):
    """Where the fruit hang on `tree_of_knowledge`, units from its foot. The
    first three are KNOWLEDGE_FRUIT_LOW, the ones within reach.

    Call: `knowledge_fruit_spots()` -> [(x, y)]; world px are KNOWLEDGE_XY + (x * PXU, -y * PXU)."""
    rng = random.Random(seed)
    out = list(KNOWLEDGE_FRUIT_LOW) + list(KNOWLEDGE_FRUIT_WEST)
    # clusters, heavier low on the crown than at its top
    seeds = [(-268, 158), (-210, 196), (-146, 214), (-226, 252), (-112, 262),
             (-46, 232), (-30, 300), (40, 262), (56, 214), (110, 300),
             (136, 226), (206, 200), (232, 262), (272, 160), (-284, 214),
             (288, 216)]
    for sx, sy in seeds:
        for k in range(rng.choice((1, 2, 3))):
            x = sx + rng.uniform(-16, 16)
            y = sy + rng.uniform(-14, 14)
            if all(math.hypot(x - a, y - b) > 15 for a, b in out):
                out.append((x, y))
    return out


# ---------------------------------------------------------------------------
# Plants of the ground (parts: y up, units, origin on the ground)
# ---------------------------------------------------------------------------

def shift(parts, dx, dy, k=1.0):
    """Parts moved by (dx, dy) and scaled by k about the origin."""
    out = []
    for kind, data, mat in parts:
        if kind == "dot":
            out.append((kind, (data[0] * k + dx, data[1] * k + dy,
                               data[2] * k), mat))
        else:
            out.append((kind, [(x * k + dx, y * k + dy) for x, y in data], mat))
    return out


def grass_tuft(rng, h=30.0, n=5, dry=False):
    """A tuft of grass: blades of uneven length leaning out, the back ones
    darker. Blades of one length read as a comb.

    Call (and for herb, fern, lily, anemone, daisy, violet, reed): `render(grass_tuft(random.Random(1)),
    PLANT_PAINT)`. A drift of them: `patch`. The scene's own drifts are `place("ma", x, y)` (see `place`)."""
    P = []
    for i in range(n):
        t = (i + .5) / n - .5
        x0 = t * h * .5
        tipx = x0 + t * h * rng.uniform(.5, 1.2) + rng.uniform(-3, 3)
        tipy = h * rng.uniform(.55, 1.1) * (1 - abs(t) * .7)
        w = rng.uniform(1.5, 2.2)
        mat = "blade_deep" if i % 3 == 0 else "blade"
        if dry:
            mat = "dry_blade"
        P.append(("fill", [(x0 - w, 0), (x0 + (tipx - x0) * .45 - w * .4, tipy * .55),
                           (tipx, tipy),
                           (x0 + (tipx - x0) * .55 + w * .5, tipy * .5),
                           (x0 + w, 0)], mat))
    return P


def herb(rng, h=46.0):
    """The herb of the field: a stalk, broad leaves up it in turn, and a head
    of seed (1:11-12), which is the thing about a herb."""
    P = [("line", [(0, 0), (rng.uniform(-2, 2), h * .5), (rng.uniform(-3, 3), h)],
          "stalk")]
    for i in range(4):
        y = h * (.14 + i * .19)
        sx = 1 if i % 2 else -1
        ang = math.pi / 2 - sx * rng.uniform(.75, 1.1)
        L = h * (.36 - i * .04)
        P.append(("fill", leaf_oval(0, y, L, L * .42, ang),
                  "herb"))
    tx, ty = P[0][1][-1]
    for k in range(4):
        P.append(("dot", (tx + rng.uniform(-2.4, 2.4), ty + k * 2.6, 1.5),
                  "pip_gold"))
    return P


def fern(rng, h=16.0):
    """A low leafy plant, a cushion of short thick leaf strokes."""
    P = []
    for _ in range(9):
        a = rng.uniform(.25, 2.9)
        r0 = rng.uniform(1, h * .45)
        L = rng.uniform(4, 7)
        x, y = r0 * math.cos(a), r0 * math.sin(a) * .8
        P.append(("line", [(x, y), (x + L * math.cos(a), y + L * math.sin(a))],
                  "fern"))
    return P


def _flower(P, x, y, r, petal, eye=None, n=5):
    a0 = 0.3
    for i in range(n):
        a = a0 + TAU * i / n
        P.append(("line", [(x + r * .2 * math.cos(a), y + r * .2 * math.sin(a)),
                           (x + r * math.cos(a), y + r * math.sin(a))], petal))
    if eye:
        P.append(("dot", (x, y, .8), eye))


def lily(rng, h=40.0):
    """A clump of white lilies of the field: strap leaves and tall stems."""
    P = []
    for i in range(5):
        t = (i - 2) / 2
        P.append(("fill", [(t * 4 - 1.6, 0), (t * 12, h * .32),
                           (t * 22, h * .55 * (1 - abs(t) * .25)),
                           (t * 12 + 2, h * .28), (t * 4 + 1.6, 0)], "blade"))
    for dx in (-6, 2, 9):
        top = (dx * 1.5 + rng.uniform(-2, 2), h * rng.uniform(.8, 1.08))
        P.append(("line", [(dx * .3, 0), (dx, h * .5), top], "stalk"))
        _flower(P, top[0], top[1], 3.4, "petal_white", "pip_gold", 6)
    return P


def anemone(rng, h=20.0):
    """A little scatter of red anemones on thin stems over cut leaves."""
    P = []
    for dx, ht in ((-9, 1.0), (0, 1.25), (9, .9)):
        top = (dx + rng.uniform(-2, 2), h * ht)
        P.append(("line", [(dx * .4, 0), top], "stalk"))
        _flower(P, top[0], top[1], 3.0, "petal_rose", None, 5)
    for i in range(4):
        a = .5 + i * .7
        P.append(("line", [(0, 1), (9 * math.cos(a), 7 * math.sin(a) + 1)], "fern"))
    return P


def daisy(rng, h=14.0):
    """Small yellow flowers in a low clump."""
    P = []
    for _ in range(4):
        x, y = rng.uniform(-11, 11), h * rng.uniform(.5, 1.05)
        P.append(("line", [(x * .5, 0), (x, y)], "stalk"))
        _flower(P, x, y, 2.1, "petal_gold", None, 5)
    return P


def violet(rng, h=12.0):
    """Violet flowers close to the ground."""
    P = []
    for _ in range(4):
        x, y = rng.uniform(-9, 9), h * rng.uniform(.5, 1.05)
        P.append(("line", [(x * .5, 0), (x, y)], "stalk"))
        _flower(P, x, y, 1.9, "petal_violet", None, 5)
    return P


def reed(rng, h=84.0):
    """Reeds at the water: long leaning blades and a few brown heads."""
    P = []
    for i in range(7):
        x0 = (i - 3) * 3.2
        lean = (i - 3) * rng.uniform(2.2, 5)
        ht = h * rng.uniform(.62, 1.05)
        mat = "blade_deep" if i % 2 else "blade"
        P.append(("fill", [(x0 - 1.5, 0), (x0 + lean * .4 - .9, ht * .55),
                           (x0 + lean, ht), (x0 + lean * .45 + 1.1, ht * .5),
                           (x0 + 1.5, 0)], mat))
    for dx in (-5, 4):
        tx, ty = dx * 1.6, h * rng.uniform(1.0, 1.2)
        P.append(("line", [(dx * .6, 0), (tx, ty)], "stalk"))
        P.append(("line", [(tx, ty - 11), (tx, ty - 1)], "reed_head"))
    return P


def rock(seed=1, w=70.0, h=40.0):
    """A rock: an irregular block with a lit top plane, a shaded side cut with
    rule lines, and a crack or two. Straight cuts, not curves: stone is what is
    NOT soft here.

    Call: `render(_in_order(rock(1), ("rock", "rock_lit", "rock_deep", "rock_line")), PLANT_PAINT)`."""
    rng = random.Random(seed)
    n = 7
    pts = [(-w / 2, 0)]
    for i in range(1, n):
        t = i / n
        x = -w / 2 + w * t + rng.uniform(-w * .05, w * .05)
        y = h * math.sin(math.pi * t) ** .7 * rng.uniform(.8, 1.1)
        pts.append((x, y))
    pts.append((w / 2, 0))
    ridge = rng.uniform(-.1, .22) * w
    top = max(pts, key=lambda q: q[1])
    apex = (ridge, h * .42)
    P = [("fill", pts, "rock")]
    # the lit plane: the upper left of it, down to the fold
    lit = [q for q in pts if q[0] <= top[0] + w * .02 and q[1] > h * .02]
    if len(lit) >= 2:
        P.append(("fill", lit + [(top[0] + w * .08, h * .58), apex,
                                 (-w * .3, h * .1)], "rock_lit"))
    deep = [q for q in pts if q[0] >= top[0]]
    if len(deep) >= 2:
        P.append(("fill", deep + [(w * .2, 0), apex], "rock_deep"))
        for seg in _hatch(rng, deep + [(w * .2, 0), apex], 62, 5.0):
            P.append(("line", seg, "rock_line"))
    P.append(("line", pts + [], "rock_line"))
    P.append(("line", [apex, (apex[0] - w * .08, h * .14)], "rock_line"))
    return P


def outcrop(seed=5, w=170.0, h=70.0):
    """A shelf of rock breaking out of a bank: three or four blocks.

    Call: as `rock`. In a scene, `place("rc", x, y)`."""
    rng = random.Random(seed)
    P = []
    x = -w / 2
    i = 0
    while x < w / 2:
        bw = rng.uniform(.34, .55) * w
        P += shift(rock(seed + i, bw, h * rng.uniform(.5, 1.0)), x + bw / 2, 0)
        x += bw * rng.uniform(.62, .85)
        i += 1
    return _in_order(P, ("rock", "rock_lit", "rock_deep", "rock_line"), True)


def _in_order(P, order, keep_rest=False):
    """Parts sorted by material so each comes out one path."""
    rank = {m: i for i, m in enumerate(order)}
    return sorted(P, key=lambda q: rank.get(q[2], len(order)))


def shrub(seed=3, w=120.0, h=66.0):
    """A low flowering bush: small masses, no trunk showing.

    Call: `render(shrub(3), SHADE_PAINT)`; in a planted scene, `place("sa", x, y)`."""
    rng = random.Random(seed)
    blobs = []
    for i in range(5):
        t = i / 4 - .5
        blobs.append((t * w * .78, h * (.42 + (1 - abs(t) * 2) * .24),
                      w * .24 * rng.uniform(.85, 1.2), h * .38 * rng.uniform(.8, 1.1)))
    return foliage(rng, blobs, lobe=17, dabs=.8, carve_step=5.2, mid_k=.72,
                   lit_k=.3, contour=False, dab_len=(2.4, 4.2))


def thorns(seed=7, h=62.0):
    """Thorns (3:18): a thicket of stems, some arching and some stiff, every one
    set with spines, a few small dry leaves, no flower. A plant that has grown,
    not a zigzag.

    Call: `render(thorns(7), PLANT_PAINT)`, foot at the origin; as a place, `thorn_land_svg`
    (Scene.outside); drifts of it, `place("ta", x, y)` in a scene built with thorns_too."""
    rng = random.Random(seed)
    stems, spines, leaves = [], [], []
    for i in range(6):
        a = math.pi / 2 + (i - 3) * rng.uniform(.2, .42) + rng.uniform(-.14, .14)
        L = h * rng.uniform(.62, 1.3)
        side = 1 if math.cos(a) >= 0 else -1
        bend = rng.uniform(.02, .24)
        x, y = (i - 3) * 2.2, 0.0
        pts = [(x, y)]
        steps = 6
        for k in range(steps):
            x += L / steps * math.cos(a)
            y += L / steps * math.sin(a)
            a -= side * (bend + rng.uniform(-.1, .1))
            pts.append((x, y))
            for sgn in ((1,) if k % 2 else (-1,)):
                ang = a + sgn * 1.15
                sl = rng.uniform(3.2, 5.6)
                spines.append(("line", [(x, y), (x + sl * math.cos(ang),
                                                 y + sl * math.sin(ang))],
                               "spine"))
            if k == 3 and rng.random() < .6:      # a side shoot
                b = a + rng.choice((-1, 1)) * rng.uniform(.5, 1)
                sx, sy = x + L * .28 * math.cos(b), y + L * .28 * math.sin(b)
                stems.append(("line", [(x, y), (sx, sy)], "thorn_stem"))
                spines.append(("line", [(sx, sy), (sx + 4 * math.cos(b + 1), sy + 4 * math.sin(b + 1))],
                               "spine"))
        stems.append(("line", pts, "thorn_stem"))
        if i % 2 == 0:
            leaves.append(("fill", leaf_oval(pts[3][0], pts[3][1], 6, 3, a + 1), "dry_leaf"))
    return stems + spines + leaves


def thistle(seed=9, h=70.0):
    """Thistles (3:18): a rosette of jagged spiny leaves at the ground, stiff
    stems, and spiked heads. Straight cuts for the leaf; a thistle is a plant
    with corners.

    Call: `render(thistle(9), PLANT_PAINT)`, foot at the origin; as a place, `thorn_land_svg`
    (Scene.outside); drifts of it, `place("tb", x, y)` in a scene built with thorns_too."""
    rng = random.Random(seed)
    P = []
    # rosette
    for sx, ang, L in ((-1, 2.75, 34), (-1, 2.25, 28), (1, .9, 28), (1, .4, 34),
                       (1, 1.3, 22), (-1, 1.85, 22)):
        ca, sa = math.cos(ang), math.sin(ang)
        out = [(0, 2)]
        back = []
        for k in range(1, 6):
            t = k / 5
            wd = 8 * math.sin(math.pi * t) + .5
            nx, ny = -sa, ca
            bx, by = L * t * ca, 2 + L * t * sa
            out.append((bx + nx * wd, by + ny * wd))
            out.append((bx + nx * wd * .35 - ca * 2, by + ny * wd * .35 - sa * 2))
            back.append((bx - nx * wd, by - ny * wd))
            back.append((bx - nx * wd * .35 - ca * 2, by - ny * wd * .35 - sa * 2))
        P.append(("fill", out + back[::-1], "thistle_leaf"))
    heads = []
    for dx, ht in ((-7, .86), (2, 1.0), (10, .74)):
        tx, ty = dx * 1.6 + rng.uniform(-2, 2), h * ht
        P.append(("line", [(dx * .3, 0), (dx, h * .5), (tx, ty)], "thistle_stem"))
        for k in range(3):                 # the stem's little spiny leaves
            y = h * (.22 + k * .2)
            P.append(("line", [(dx * .5, y), (dx * .5 + 7 * (1 if k % 2 else -1), y + 5)],
                      "spine"))
        heads.append((tx, ty))
    for tx, ty in heads:
        # the spiked cup and the brush on it
        cup = [(tx - 5.6, ty + 1), (tx - 3, ty - 4), (tx + 3, ty - 4),
               (tx + 5.6, ty + 1), (tx + 3.6, ty + 6), (tx - 3.6, ty + 6)]
        P.append(("fill", cup, "thistle_cup"))
        for k in range(7):
            a = math.pi * (.12 + .76 * k / 6)
            P.append(("line", [(tx + 3 * math.cos(a), ty + 5 + 2 * math.sin(a)),
                               (tx + 7 * math.cos(a), ty + 7 + 8 * math.sin(a))],
                      "thistle_brush"))
        for a in (-.5, -1.0, -2.1, -2.6, .1, 3.0):
            P.append(("line", [(tx + 4.6 * math.cos(a), ty + 1 + 3 * math.sin(a)),
                               (tx + 8.4 * math.cos(a), ty + 1 + 6.4 * math.sin(a))],
                      "spine"))
    return P


PLANT_PAINT = {
    "blade_deep": ((44, 66, 44), None, 0),
    "blade": ((78, 106, 62), None, 0),
    "blade_lit": ((116, 142, 82), None, 0),
    "stalk": (None, (104, 128, 76), .9),
    "herb": ((62, 92, 54), (128, 150, 96), .6),
    "herb_lit": ((92, 122, 66), (148, 168, 108), .6),
    "fern": (None, (94, 122, 72), 2.4),
    "fern_lit": (None, (124, 150, 88), 2.4),
    "petal_white": (None, (218, 214, 188), 1.7),
    "petal_rose": (None, (180, 92, 96), 1.8),
    "petal_gold": (None, (198, 166, 84), 1.5),
    "petal_violet": (None, (134, 116, 168), 1.5),
    "pip_gold": (None, (198, 166, 84), 2),
    "pip_dark": (None, (40, 30, 40), 2),
    "pip_white": (None, (216, 212, 186), 2),
    "reed_head": (None, (104, 76, 54), 3.8),
    "rock": ((74, 72, 62), None, 0), "rock_lit": ((110, 106, 88), None, 0),
    "rock_deep": ((42, 42, 38), None, 0),
    "rock_line": (None, (150, 146, 118), .9),
    "spine": (None, (186, 162, 118), .95),
    "thorn_stem": (None, (70, 54, 42), 2.3),
    "dry_leaf": ((104, 96, 60), None, 0),
    "thistle_leaf": ((72, 96, 80), (124, 146, 116), .6),
    "thistle_stem": (None, (120, 140, 110), 1.8),
    "thistle_cup": ((96, 116, 96), (170, 186, 150), .6),
    "thistle_brush": (None, (122, 104, 132), 1.5),
    "tick": (None, (104, 130, 78), 1.0),
    "dry_blade": ((132, 118, 76), None, 0),
    "pebble": ((132, 120, 96), None, 0),
    "pebble_foot": (None, (46, 40, 32), 1.2),
    "crack": (None, (54, 46, 36), 1.2),
}

PLANT_ORDER = ("dry_blade", "blade_deep", "stalk", "fern", "fern_lit", "herb", "herb_lit", "blade",
               "blade_lit", "reed_head", "thorn_stem", "spine", "dry_leaf",
               "thistle_leaf", "thistle_stem", "thistle_cup", "thistle_brush",
               "petal_white", "petal_rose", "petal_gold", "petal_violet",
               "pip_gold", "pip_dark", "pip_white", "tick", "pebble", "pebble_foot", "crack")


def patch(seed, recipe, w=230.0, depth=26.0, marks=0):
    """A drift of plants: `recipe` is [(plant function, count)]. One drawing, a
    path per material: scattered over the ground it costs a few bytes a time,
    and a meadow is thirty of these."""
    rng = random.Random(seed)
    P = []
    for fn, count in recipe:
        for _ in range(count):
            dx, dy = rng.uniform(-w / 2, w / 2), rng.uniform(-depth, 0)
            P += shift(fn(rng), dx, dy, rng.uniform(.8, 1.15))
    for _ in range(marks):
        x, y = rng.uniform(-w / 2, w / 2), rng.uniform(-depth * 1.2, depth * .2)
        L = rng.uniform(3, 6)
        a = rng.uniform(1.0, 2.1)
        P.append(("line", [(x, y), (x + L * math.cos(a), y + L * math.sin(a))],
                  "stalk"))
    return _in_order(P, PLANT_ORDER)


# ---------------------------------------------------------------------------
# The place: one plan, seen two ways
# ---------------------------------------------------------------------------
#
# There is one garden. A point in it is (x, d): x east, d north of the line the
# people stand on, both in card px. The side view and the high plan are two
# projections of those same points: every tree and every bend of the river has
# one (x, d), so the plan's river IS the panorama's river, seen from above.
# `project(d)` is the side view's card y. A long panorama has no vanishing
# point across, so x is the same in both, which is what lets a camera rise from
# one to the other and the place stay put under it.

HORIZON = 1130.0
FOCAL = 900.0
X0, X1 = -3600.0, 3650.0            # where the side view is drawn in full
# how far its sky and its ground go on, plain, so that its edge never shows while
# it fades over the plan (SIDE_IN's zooms): Card(origin, size)
CARD_X = (-8600, 13000)
CARD_Y = (-3800, 6800)
Y_END = 6800.0


def project(d):
    """The card y of the ground `d` px north of the people's line.

    Call: `project(d)`. `land_y(x, d)` also has the land's rise in the west."""
    return HORIZON + (GROUND - HORIZON) * FOCAL / max(FOCAL + d, 40.0)


def depth_scale(d):
    """How big a thing `d` px north of the people's line is drawn."""
    return FOCAL / max(FOCAL + d, 40.0)


def depth_of(y):
    """The inverse of `project`: which `d` a card y lies on."""
    return FOCAL * ((GROUND - HORIZON) / (y - HORIZON) - 1.0)


# The river, flowing east: (x, d, width). It comes out of the high ground of
# Eden in the west (2:10 "went out of Eden"), crosses in front of the place the
# people stand, and parts at the east end of the garden ("from there it was
# parted"). West of x -1900 it is on the far side of the people's line, and
# from there to the parting it stays on the near side, so nobody has to wade to
# get from one named tree to the other, or to go out at the east.
RIVER = [(-5300, 1250, 70), (-4500, 1720, 80), (-3760, 1650, 62), (-3260, 1320, 62),
         (-2860, 880, 70), (-2520, 470, 80), (-2240, 120, 92), (-1960, -170, 104),
         (-1660, -370, 124), (-1300, -440, 140), (-920, -330, 124),
         (-540, -200, 100), (-160, -162, 92), (220, -196, 96), (580, -318, 112),
         (940, -436, 136), (1300, -404, 134), (1640, -286, 118), (1950, -262, 124)]

PARTING = (1950, -262)

HEADS = {
    "Pishon": [(1950, -262, 96), (2200, -236, 64), (2500, -170, 58), (2800, -90, 56),
               (3100, 10, 58), (3420, 190, 60), (3800, 500, 64), (4200, 900, 68),
               (4760, 1500, 74), (5560, 2360, 84), (6660, 2960, 92), (7860, 3660, 96),
               (9260, 4060, 100)],
    "Gihon": [(1950, -262, 96), (2220, -272, 66), (2520, -262, 60), (2860, -226, 60),
              (3300, -150, 64), (3800, -40, 70), (4450, 240, 74), (5350, 480, 84),
              (6450, 800, 90), (7750, 850, 96), (9250, 1200, 100)],
    "Hiddekel": [(1950, -262, 96), (2230, -324, 66), (2550, -352, 62), (2900, -388, 64),
                 (3350, -420, 70), (3850, -520, 74), (4650, -520, 80), (5650, -900, 88),
                 (6850, -1000, 92), (8150, -1500, 96), (9450, -1600, 100)],
    "Euphrates": [(1950, -262, 96), (2150, -380, 70), (2390, -486, 70), (2630, -566, 72),
                  (2900, -646, 76), (3250, -1000, 96), (3750, -1500, 110),
                  (4450, -1850, 124), (5450, -2700, 138), (6650, -3100, 148),
                  (7950, -3900, 156), (9450, -4200, 164)],
}


def _centre(points, n=5):
    """A river's centreline, sampled: (x, d, width, nx, nd), the normal to the
    left of the flow (north, as it runs east)."""
    xy = [(p[0], p[1]) for p in points]
    dense = F.smooth(xy, closed=False, n=n)
    m = len(points) - 1
    out = []
    for i, (x, d) in enumerate(dense):
        t = i / (len(dense) - 1) * m
        k = min(int(t), m - 1)
        w = points[k][2] + (points[k + 1][2] - points[k][2]) * (t - k)
        a = dense[max(i - 1, 0)]
        b = dense[min(i + 1, len(dense) - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1.0
        out.append((x, d, w, -dy / L, dx / L))
    return out


def _cut_side(samples, x_max=X1 + 200, d_min=-790):
    """The samples a side view can see."""
    return [q for q in samples if q[0] <= x_max and q[1] >= d_min]


_MAIN = _centre(RIVER, 3)
_HEADS = {k: _centre(v, 3) for k, v in HEADS.items()}


def _near_water(x):
    """The lowest d of any water at this x: where the near bank's lip must be."""
    best = None
    for run in [_MAIN] + list(_HEADS.values()):
        for a, b in zip(run, run[1:]):
            if a[0] <= x <= b[0] or b[0] <= x <= a[0]:
                t = (x - a[0]) / ((b[0] - a[0]) or 1.0)
                d = a[1] + (b[1] - a[1]) * t
                w = a[2] + (b[2] - a[2]) * t
                edge = d - w / 2
                if best is None or edge < best:
                    best = edge
    return best


def _wave(x, seed, amp, wl):
    r = random.Random(seed)
    p = [r.uniform(0, TAU) for _ in range(4)]
    return amp * (.5 * math.sin(TAU * x / wl + p[0])
                  + .32 * math.sin(TAU * x / (wl * .47) + p[1])
                  + .18 * math.sin(TAU * x / (wl * .21) + p[2])
                  + .06 * math.sin(TAU * x / (wl * .09) + p[3]))


def _smoothstep(a, b, x):
    t = max(0.0, min(1.0, (x - a) / (b - a)))
    return t * t * (3 - 2 * t)


def upland(x):
    """How far the land rises toward Eden's high ground in the west."""
    return _smoothstep(-1900, -3700, x)


def land_y(x, d):
    """The card y of the ground at plan point (x, d) in the side view: `project`,
    plus the lift of the land toward Eden. Everything standing in the west stands
    on this, and the river climbs it, so it comes down out of the high ground and
    does not start from nowhere.

    Call: `land_y(x, d)`; things standing there are scaled by `depth_scale(d)`."""
    y = project(d)
    u = upland(x)
    if u <= 0 or d <= -100:
        return y
    k = (0, 90, 124, 158, 192, 226, 260)
    ds = (-100, 60, 300, 650, 1150, 1900, 3000)
    for i in range(len(ds) - 1):
        if d <= ds[i + 1]:
            t = (d - ds[i]) / (ds[i + 1] - ds[i])
            return y - u * (k[i] + (k[i + 1] - k[i]) * t)
    return y - u * 260


# far to near: (d of the bank's crest, amplitude, wavelength)
BANKS = [(3000, 13, 1100), (1900, 12, 900), (1150, 12, 800), (650, 16, 720),
         (300, 18, 640), (60, 15, 600)]
STAGE_BANK = 5
# the banks nearer than the water: (margin behind which they run, amp, wl)
NEAR_BANKS = [(0, 5, 300)]


def bank_y(i, x):
    """A far bank's crest at x, card y."""
    d, amp, wl = BANKS[i]
    u = upland(x)
    return project(d) + _wave(x, 100 + i, amp, wl) - u * (260 - 34 * i)


_NEAR_CACHE = {}


def _near_lip(x):
    """The near bank's lip at x, as a d: on the water's near edge in the river's
    reach, and in front of the people's line where there is none."""
    key = round(x / 40.0)
    if key not in _NEAR_CACHE:
        vals = []
        for dx in (-160, -80, 0, 80, 160):
            e = _near_water(x + dx)
            vals.append(-160.0 if e is None or x + dx < -1960 else e)
        _NEAR_CACHE[key] = min(-140.0, sum(vals) / len(vals))
    return _NEAR_CACHE[key]


def near_bank_y(i, x):
    """A near bank's crest at x, card y: bank 0 is the water's near lip, the
    others stand in front of it, each with its own swell."""
    margin, amp, wl = NEAR_BANKS[i]
    lip = _near_lip(x)
    d = lip if i == 0 else min(margin, lip - 40.0 * i)
    d = max(d, -815.0)
    y = project(d) + _wave(x, 200 + i, amp, wl)
    return y


def ground_y(x):
    """Where a figure's feet go at x: on the turf just below the crest behind
    the people's line, so the ground rises and falls under them.

    Call: `ground_y(x)`; a man at x stands at `ground_y(x) + 2`, a woman at `ground_y(x) + 6`."""
    return bank_y(STAGE_BANK, x) + 20.0


# ---- the two palettes of the land ------------------------------------------

GARDEN_BANK = [(62, 74, 70), (58, 74, 64), (54, 74, 58), (54, 78, 54),
               (56, 84, 52), (60, 90, 54)]
DUST_BANK = [(92, 88, 78), (92, 85, 72), (94, 84, 66), (96, 84, 62),
             (102, 88, 62), (110, 94, 66)]
GARDEN_NEAR = [(54, 80, 48), (36, 56, 38)]
DUST_NEAR = [(100, 84, 60), (64, 54, 42)]
SKY_TOP = (17, 20, 32)
SKY_LOW = (74, 76, 80)

WATER = (100, 142, 160)
WATER_DEEP = (78, 118, 142)
BANK_CUT = (66, 58, 44)
BANK_LINE = (128, 128, 92)


# The air thickens with distance. It is in the colours, because a translucent gradient over two
# thirds of the frame would be paid for on every frame: each thing is mixed toward the haze by how
# much air lies in front of it.
HAZE_FAR, HAZE_MID = .3, .16        # the two veils of air: past the far banks, past the middle ones
HAZE_TOP, HAZE_FULL = 620, 1230     # the veils thicken from here down to here
_HEX = re.compile(r"#([0-9a-fA-F]{6})\b")


def tinted(svg, toward, a):
    """Every colour in a run of svg mixed `a` of the way toward a colour."""
    def mix(m):
        h = m.group(1)
        c = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
        return "#%02x%02x%02x" % tuple(round(q + (t - q) * a) for q, t in zip(c, toward))
    return _HEX.sub(mix, svg)


def _air(y, *veils):
    """How much haze lies over something at card y, behind these veils."""
    r = max(0.0, min(1.0, (y - HAZE_TOP) / (HAZE_FULL - HAZE_TOP)))
    clear = 1.0
    for a in veils:
        clear *= 1 - a * r
    return 1 - clear


def _hazed(svg, *veils):
    """A run of the far ground, all of it low enough to be behind the veils at their thickest."""
    return tinted(svg, SKY_LOW, _air(HAZE_FULL, *veils))


def _fill(pts, fill, stroke=None, w=0, curve=True, prec=0, extra=""):
    """A closed shape, already in card px."""
    d = _D(prec)
    if _area(pts) < 0:
        pts = pts[::-1]
    (d.closed_curve if curve else lambda q: d.poly(q, True))(pts)
    a = f' fill="{fill}"'
    if stroke:
        a += f' stroke="{stroke}" stroke-width="{w:g}"'
    return f'<path{a}{extra} d="{d.text()}"/>'


def _strokes(runs, stroke, w, curve=True, prec=0, extra=""):
    """Open lines, already in card px, as one path, each starting from an absolute point, so that
    `in_frame` can drop them one at a time."""
    ds = ""
    for r in runs:
        if len(r) < 2:
            continue
        d = _D(prec)
        (d.open_curve(r) if curve else d.poly(r, False))
        ds += d.text()
    return f'<path fill="none" stroke="{stroke}" stroke-width="{w:g}"{extra} d="{ds}"/>'


def _curve_points(pts, step=60.0):
    """Points along the curve `_D.open_curve` draws through pts, about `step` apart."""
    if len(pts) < 3:
        return list(pts)

    def mid(a, b):
        return (a[0] + b[0]) / 2, (a[1] + b[1]) / 2

    def back(p, c):
        return 2 * p[0] - c[0], 2 * p[1] - c[1]
    if len(pts) == 3:
        quads = [(pts[0], pts[1], pts[2])]
    else:
        c, p = pts[1], mid(pts[1], pts[2])
        quads = [(pts[0], c, p)]
        for q in pts[3:-1]:
            c = back(p, c)
            m = mid(c, q)
            quads.append((p, c, m))
            p = m
        quads.append((p, back(p, c), pts[-1]))
    out = [pts[0]]
    for a, c, b in quads:
        n = max(1, math.ceil(math.hypot(b[0] - a[0], b[1] - a[1]) / step))
        for i in range(1, n + 1):
            t = i / n
            out.append(((1 - t) ** 2 * a[0] + 2 * t * (1 - t) * c[0] + t * t * b[0],
                        (1 - t) ** 2 * a[1] + 2 * t * (1 - t) * c[1] + t * t * b[1]))
    return out


def _dashes(run):
    """A line along a curve through `run`, broken by FORM_DASH, as [the points of each dash]."""
    pts = _curve_points(run)
    out, cur = [], [pts[0]]
    i, left, on = 0, FORM_DASH[0], True
    for a, b in zip(pts, pts[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        at = 0.0
        while L - at > left:
            at += left
            u = at / L
            q = (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u)
            if on:
                out.append(cur + [q])
            cur = [q]
            i = (i + 1) % len(FORM_DASH)
            left, on = FORM_DASH[i], not on
        left -= L - at
        if on:
            cur.append(b)
    if on and len(cur) > 1:
        out.append(cur)
    return out


def _engraved(runs, w, opacity=.2):
    """The engraver's broken lines. Each dash is a short line of its own, so that the renderer has
    no long path to dash on every frame, a trim keeps only those in frame, and a dash lies in the
    same place in every verse's file, whatever its trim. None crosses FORMED_CLEAR: close up, a
    line on the land behind him there would read as a line on him."""
    ds = ""
    for run in runs:
        for dash in _dashes(run):
            xs, ys = [p[0] for p in dash], [p[1] for p in dash]
            if _meets(FORMED_CLEAR, min(xs), min(ys), max(xs), max(ys)):
                continue
            d = _D(0)
            d.poly(dash, False)
            ds += d.text()
    return f'<path fill="none" stroke="#cfcb92" stroke-width="{w:g}" stroke-opacity="{opacity:g}" d="{ds}"/>'


def _gradient(gid, stops):
    """A horizontal gradient across the whole land, in card px. `Scene.trimmed` takes it off any
    verse whose camera never sees it change: a gradient costs far more to paint than a flat fill,
    and more again under a moving camera, which has it rebuilt on every frame."""
    s = (f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" '
         f'x1="{X0:g}" y1="0" x2="{X1:g}" y2="0">')
    for x, c in stops:
        s += f'<stop offset="{(x - X0) / (X1 - X0):.3f}" stop-color="{_hex(c)}"/>'
    return s + "</linearGradient>"


def _garden_span(d):
    """Where the garden's outline crosses this depth: (west x, east x)."""
    xs = []
    E = GARDEN_EDGE
    for i in range(len(E)):
        (x0, d0), (x1, d1) = E[i - 1], E[i]
        if (d0 > d) != (d1 > d):
            xs.append(x0 + (d - d0) / (d1 - d0) * (x1 - x0))
    return (min(xs), max(xs)) if xs else (-1000.0, 1000.0)


def land_stops(garden, dust, d=0.0, west=None):
    """West to east, at one depth: Eden's dry shoulder, the green the water
    reaches, the dust beyond its reach. There is no line anywhere: it goes over
    a long way, it goes over at a different place on every swell, because the
    garden's outline does, and the planting thins with it (`garden_density`).
    `west` = (dust to, green from) holds the green east of those x's (SHOULDER)."""
    w, e = _garden_span(d)
    a, b = w - 420, w + 340
    if west:
        a, b = max(a, west[0]), max(b, west[1])
    return [(a, dust), (b, garden), (e - 300, garden), (e + 460, dust)]


def _dust(near, i, wet=False):
    """Bank i's dust. After the mist of 2:6 it stays a shade darker, `wet`, until the green has
    gone over it at 2:9."""
    c = (DUST_NEAR if near else DUST_BANK)[i]
    return _mix(c, (10, 18, 14), .2) if wet else c


def _bank_veils(i):
    """The veils of air in front of far bank i."""
    return (HAZE_FAR, HAZE_MID) if i < 3 else (HAZE_MID,) if i < 5 else ()


def shoulder_edge(d):
    """Where Eden's dry shoulder ends at depth d, (dust to, green from): SHOULDER on the people's
    line, and going back as the garden's own west edge goes, half as far, so that the edge lies
    on the land and doesn't run straight up the picture."""
    dx = (_garden_span(d)[0] - _garden_span(0)[0]) / 2
    return SHOULDER[0] + dx, SHOULDER[1] + dx


def land_ramps(wet=False, shoulder=False):
    """The planted ground's colour from west to east, as {gradient's id: stops}; with `shoulder`,
    the same while Eden's dry shoulder keeps its dust (`shoulder_edge`), by ids of their own."""
    ramps, pre = {}, "s" if shoulder else "g"
    for i in range(len(BANKS)):
        a = _air(HAZE_FULL, *_bank_veils(i))
        d = min(BANKS[i][0], 1500)
        ramps[f"{pre}b{i}"] = land_stops(_mix(GARDEN_BANK[i], SKY_LOW, a),
                                         _mix(_dust(False, i, wet), SKY_LOW, a),
                                         d, shoulder_edge(d) if shoulder else None)
    ramps[f"{pre}n0"] = land_stops(GARDEN_NEAR[0], _dust(True, 0, wet), -420,
                                   shoulder_edge(-420) if shoulder else None)
    return ramps


def land_defs(state, wet=False, shoulder=False):
    """The ground's gradients for a state of the land. The near ground darkens toward the eye: a
    gradient over one rect, and no group opacity, no filter."""
    out = ('<linearGradient id="gvig" gradientUnits="userSpaceOnUse" x1="0" '
           'y1="1760" x2="0" y2="2800"><stop offset="0" stop-color="#0c1210" '
           'stop-opacity="0"/><stop offset="1" stop-color="#0c1210" '
           'stop-opacity=".72"/></linearGradient>')
    if state == "planted":
        out += "".join(_gradient(gid, stops) for gid, stops in land_ramps(wet).items())
        if shoulder:
            out += "".join(_gradient(gid, stops)
                           for gid, stops in land_ramps(wet, shoulder=True).items())
    return out


def _fade_in(begin, dur):
    """SMIL: an opacity from 0 to 1, eased, held. The thing it is in starts at
    opacity="0"."""
    return (f'<animate attributeName="opacity" values="0;1" begin="{begin:.2f}s" '
            f'dur="{dur:.2f}s" fill="freeze" calcMode="spline" keyTimes="0;1" '
            f'keySplines=".42 0 .58 1"/>')


def _fade_out(begin, dur):
    """SMIL: an opacity from 1 to 0, eased, held."""
    return (f'<animate attributeName="opacity" values="1;0" begin="{begin:.2f}s" '
            f'dur="{dur:.2f}s" fill="freeze" calcMode="spline" keyTimes="0;1" '
            f'keySplines=".42 0 .58 1"/>')


def _land_fill(shape, state, near, i, curve=True, green=None, wet=False, shoulder=None):
    """A piece of ground in its state's colour. `green=(begin, dur)` (planted only) lays
    the watered colour over the same shape's dust as a fade, and the dust at either end
    of it is the same dust, so only what the water reaches changes. `shoulder=(begin, dur)`
    keeps Eden's dry shoulder dust through that, and greens it then."""
    if green and state == "planted":
        d = _D(0)
        pts = shape[::-1] if _area(shape) < 0 else shape
        (d.closed_curve if curve else lambda q: d.poly(q, True))(pts)
        d = d.text()
        out = (f'<path fill="{_hex(_dust(near, i, wet))}" d="{d}"/>'
               f'<path fill="{_bank_fill(state, near, i, wet, bool(shoulder))}" opacity="0" '
               f'd="{d}">{_fade_in(*green)}</path>')
        if shoulder:
            out += (f'<path fill="{_bank_fill(state, near, i, wet)}" opacity="0" d="{d}">'
                    f'{_fade_in(*shoulder)}</path>')
        return out
    return _fill(shape, _bank_fill(state, near, i, wet), curve=curve)


def _bank_fill(state, near, i, wet=False, shoulder=False):
    if state == "planted":
        return f'url(#{"s" if shoulder else "g"}{"n" if near else "b"}{i})'
    return _hex(_dust(near, i, wet))


def _bank_xs(step):
    """The x's a bank's crest is sampled at: fine where the side view is drawn in
    full, coarse out to the edge of the card, where it is only ever seen fading."""
    xs = [X0 + k * step for k in range(int((X1 - X0) / step) + 1)]
    return ([CARD_X[0] - 300, -7000, -5600, -4500] + xs
            + [4800, 6400, 9000, CARD_X[1] + 300])


def bank_svg(state, near, i, step=None, green=None, wet=False, shoulder=None):
    """One bank of the land: a swell of ground with its crest line, broken."""
    crest = near_bank_y if near else bank_y
    step = step or (190 if near and i == 0 else 300 if near else (300 - 30 * i))
    pts = [(x, crest(i, x)) for x in _bank_xs(step)]
    last = i == len(BANKS) - 1
    # a bank goes down only as far as the next one's crest can dip, and that one covers the rest
    y_low = (Y_END if near or last else project(BANKS[i + 1][0]) + BANKS[i + 1][1] + 8)
    shape = pts + [(pts[-1][0], y_low), (pts[0][0], y_low)]
    out = _land_fill(shape, state, near, i, green=green, wet=wet, shoulder=shoulder)
    # the crest, as a drawn line that comes and goes, over the full width only
    rng = random.Random(300 + i + (50 if near else 0))
    runs, cur = [], []
    for p in pts:
        if not X0 <= p[0] <= X1:
            continue
        if rng.random() < .22:
            if len(cur) >= 2:
                runs.append(cur)
            cur = []
        else:
            cur.append(p)
    if len(cur) >= 2:
        runs.append(cur)
    tone = (.55 if near else .3 + i * .08)
    col = _mix(SKY_LOW, BANK_LINE, tone)
    out += _strokes(runs, _hex(col), 1.5 if near else 1.2, curve=True)
    out += form_lines(state, near, i)
    return out


# Hand-cut breaks, on and off: a dash array like this never repeats visibly on a swell.
FORM_DASH = (46, 22, 18, 40, 120, 34, 60, 110, 14, 30, 200, 60)


def form_lines(state, near, i):
    """The engraver's lines on a swell of ground: long strokes that follow its
    shape, closer together toward the far side of it, and broken by a dash
    pattern long enough never to look repeated. One path per bank, and this is
    what stops the land being a flat colour."""
    if near:
        spec = {0: (7, 36, 1.38)}[i]
    else:
        spec = {0: (0, 0, 1), 1: (1, 8, 1), 2: (1, 12, 1), 3: (2, 13, 1.1),
                4: (3, 13, 1.25), 5: (4, 13, 1.25)}[i]
    n, gap, grow = spec
    if not n:
        return ""
    crest = near_bank_y if near else bank_y
    step = 260 if near else 300
    runs = []
    for j in range(1, n + 1):
        off = sum(gap * grow ** m for m in range(j))
        run = []
        for k in range(int((X1 - X0) / step) + 2):
            x = X0 + k * step + j * 37
            y = crest(i, x) + off + _wave(x, 400 + i * 7 + j, 3 + off * .08, 330)
            run.append((x, y))
        runs.append(run)
    return _engraved(runs, 1.2)


# Swells of ground: (x, d, width, height, sheet). Whole-width banks read as strata
# from far off, so the land's relief is carried by these: each its own rise, lit
# on the west, with its own lines. The sheet is whichever bank's fill it takes.
SWELLS_FAR = [(-1760, 760, 900, 26, 3), (-1040, 520, 760, 18, 4), (420, 760, 900, 20, 3),
              (1120, 500, 820, 20, 4), (1640, 300, 760, 22, 4), (-2100, 330, 620, 26, 4),
              (2640, 420, 1100, 34, 4), (3300, 200, 900, 36, 4)]
SWELLS_NEAR = [(-1500, -640, 1500, 90, 0), (-420, -560, 1000, 50, 0), (420, -640, 1600, 100, 0),
               (1360, -660, 1100, 90, 0), (-2240, -560, 1100, 70, 0), (2320, -700, 1000, 90, 0),
               (-860, -730, 1700, 170, 0), (760, -745, 1900, 220, 0), (-2500, -730, 1500, 190, 0)]


def swell_svg(state, x, d, w, h, sheet, near=False, green=None, wet=False, shoulder=None):
    """One rise of the ground, its crest a drawn line on its lit side."""
    n = 8
    base = project(d)
    top = []
    rng = random.Random(int(x * 3 + d))
    for i in range(n + 1):
        t = -1 + 2 * i / n
        px = x + t * w / 2
        py = base - h * (1 - t * t) ** 1.1 * (1 + .18 * math.sin(3 * t + d))
        if near:
            py = max(py, near_bank_y(0, px) + 14)
        top.append((px, py))
    bottom = (top[-1][0], base + h * .5), (x, base + h * .9), (top[0][0], base + h * .5)
    out = _land_fill(top + list(bottom), state, near, sheet, green=green, wet=wet,
                     shoulder=shoulder)
    out += _strokes([top[:6]], "#cfcb92", 1.4, curve=True, extra=' stroke-opacity=".34"')
    # the rule lines below the crest, falling away on the east side
    runs = []
    for k in (1, 2, 3):
        run = [(q[0] + w * .05 * k, q[1] + h * .28 * k) for q in top[2 + k - 1:8]]
        runs.append(run)
    out += _engraved(runs, 1.1)
    return out


# ---- sky and hills -----------------------------------------------------------

HILL_FOOT = project(BANKS[0][0]) + BANKS[0][1] + 8      # the first bank's crest can't dip below this
# The sky's bands: (top y, colour), from the dark overhead to the horizon's haze.
SKY_BANDS = [(-260, (21, 24, 37)), (130, (26, 30, 43)), (430, (32, 37, 50)),
             (660, (40, 45, 57)), (840, (50, 54, 65)), (980, (60, 63, 71)),
             (1080, (68, 70, 76))]


def sky_svg():
    """The sky, in flat cut bands: the house's dark overhead, lifting by steps to a
    muted haze at the horizon, each band's edge a slow wave. Each goes down only as far
    as the next band's edge can dip, and each has the air in it at its own height, so
    that the sky is one fill deep. No clouds: 2:5 has not rained yet. There is nothing
    in it that a viewer could take for a sign. The same sky stands over both states of
    the land, on the card's own dark.

    Call: `panorama` draws it first; on its own it needs no defs. `after_sky` puts the
    stars over it."""
    x0, x1 = CARD_X
    out = ""
    for k, (y, c) in enumerate(SKY_BANDS):
        top = [(x, y + 16 * math.sin(x / 1300 + k * 1.3) + 7 * math.sin(x / 470 + k))
               for x in range(x0, x1 + 1, 1100)]
        next_y = SKY_BANDS[k + 1][0] if k + 1 < len(SKY_BANDS) else HILL_FOOT
        foot = next_y + 26 if k + 1 < len(SKY_BANDS) else HILL_FOOT
        air = _air((y + next_y) / 2, HAZE_FAR, HAZE_MID)
        out += _fill(top + [(x1, foot), (x0, foot)], _hex(_mix(c, SKY_LOW, air)), curve=False)
    return f'<g data-sky="1">{out}</g>'


def after_sky(behind, svg):
    """A Scene's `behind` with `svg` drawn just after its sky: the stars of 2:1 and 3:24."""
    if not svg:
        return behind
    j = behind.index("</g>", behind.index("data-sky")) + 4
    return behind[:j] + svg + behind[j:]


def _skyline(ctrl, seed, rough=.1, passes=3):
    """A ridge from its main points: midpoint displacement, so that it has the broken
    line of real rock and no two ridges share a rhythm. Traced from nothing."""
    r = random.Random(seed)
    P = list(ctrl)
    amp = rough
    for _ in range(passes):
        Q = []
        for (x0, y0), (x1, y1) in zip(P, P[1:]):
            L = x1 - x0
            Q.append((x0, y0))
            Q.append((x0 + L * r.uniform(.4, .6),
                      (y0 + y1) / 2 + r.uniform(-1, 1) * L * amp))
        Q.append(P[-1])
        P = Q
        amp *= .78
    return P


# The far country, (x, y): the high ground of Eden in the west, where the river comes
# from, falling away to the low plains in the east, which is the way out. It stays low
# behind the two named trees, so that their crowns stand against the sky.
RANGE_FAR = [(-8600, 560), (-6200, 260), (-5000, 120), (-4200, -60), (-3650, 170), (-3180, 60),
             (-2650, 340), (-2150, 300), (-1560, 610), (-1000, 690), (-320, 880), (420, 860),
             (1120, 930), (1900, 900), (2720, 990), (3620, 960), (4720, 1040), (6400, 1030),
             (8600, 1070), (13000, 1060)]
RANGE_NEAR = [(-8600, 900), (-5600, 560), (-4400, 410), (-3500, 560), (-2800, 470), (-2100, 720),
              (-1300, 800), (-600, 980), (200, 950), (1000, 1020), (1900, 990), (2900, 1060),
              (4100, 1040), (5600, 1090), (8600, 1100), (13000, 1096)]
RANGE_LOW = [(-8600, 1040), (-5000, 880), (-3900, 820), (-2900, 900), (-2300, 1010), (-1700, 1040),
             (-1050, 1090), (-560, 1058), (-40, 1106), (520, 1066), (1100, 1112), (1760, 1074),
             (2400, 1118), (3000, 1086), (3600, 1120), (5200, 1110), (8600, 1130), (13000, 1130)]


def _facets(line, rng, drop):
    """The faces a ridge turns to the light, which here is the west: each peak's
    left-hand slope, closed by a broken line of shadow back up to the peak. A face
    takes its depth from how far the slope falls, and a slope too shallow to catch
    the light has none, so no face hangs off a flat ridge like a pennant."""
    out = []
    mirrored = [(-x, y) for x, y in reversed(line)]
    n = len(mirrored)
    i = 1
    while i < n - 1:
        if (mirrored[i][1] < mirrored[i - 1][1]
                and mirrored[i][1] <= mirrored[i + 1][1]):
            j = i
            while j < n - 1 and mirrored[j + 1][1] >= mirrored[j][1]:
                j += 1
            w = mirrored[j][0] - mirrored[i][0]
            rise = mirrored[j][1] - mirrored[i][1]
            if w > 120 and rise > 46:
                px, py = mirrored[i]
                ex, ey = mirrored[j]
                dd = min(drop, rise * .55)
                back = []
                for m in range(1, 5):
                    t = m / 5
                    back.append((ex - w * .34 * (1 - t) + (px - ex) * t + rng.uniform(-.06, .06) * w,
                                 ey + dd + (py - ey - dd) * t + rng.uniform(-.06, .06) * dd))
                face = mirrored[i:j + 1] + [(ex - w * .34, ey + dd)] + back
                out.append([(-x, y) for x, y in face])
            i = j
        i += 1
    return out


def hills_svg():
    """The far country behind everything, which nothing that happens changes: three
    ranges, cut flat, each nearer one darker, with the faces toward the light cut out
    of them in a paler ink, and strokes running down the faces turned from it. High in
    the west, where the river comes from; low and open in the east.

    Call: `panorama` draws it after the sky; on its own it needs no defs."""
    x0, x1 = CARD_X
    out = ""
    low = _skyline(RANGE_LOW, 23, .05, 3)
    near = _skyline(RANGE_NEAR, 22, .1)
    for ctrl, seed, rough, base, lit, drop, hs, foot, y_air in (
            (RANGE_FAR, 21, .1, (66, 72, 84), (104, 108, 114), 300, 120, near, 880),
            (RANGE_NEAR, 22, .1, (54, 61, 71), (86, 91, 94), 210, 90, low, 1000)):
        line = _skyline(ctrl, seed, rough)
        rng = random.Random(seed + 9)
        # each goes down only as far as the range in front of it can dip
        y_foot = max(y for _x, y in foot) + 8
        air = _air(y_air, HAZE_FAR, HAZE_MID)
        out += _fill(line + [(x1, y_foot), (x0, y_foot)], _hex(_mix(base, SKY_LOW, air)), curve=False)
        faces = _D(0)
        for f in _facets(line, rng, drop):
            faces.poly(f, True)
        out += f'<path fill="{_hex(_mix(lit, SKY_LOW, air))}" d="{faces.text()}"/>'
        # the woodcut's strokes down the turned faces, where the side view looks
        strokes = []
        for a, b in zip(line, line[1:]):
            if not X0 - 600 < a[0] < X1 + 600:
                continue
            dx, dy = b[0] - a[0], b[1] - a[1]
            if dy > 10 and dy / max(dx, 1) > .14:
                n = int(math.hypot(dx, dy) / hs)
                for k in range(n):
                    t = (k + rng.uniform(.1, .9)) / max(n, 1)
                    px, py = a[0] + dx * t, a[1] + dy * t + 3
                    ln = rng.uniform(24, 70)
                    strokes.append([(px, py), (px + ln * .3, py + ln)])
        if strokes:
            out += _strokes(strokes, _hex(_mix(_mix(base, (20, 24, 34), .5), SKY_LOW, air)), 1.2, curve=False)
    out += _fill(low + [(x1, HILL_FOOT), (x0, HILL_FOOT)],
                 _hex(_mix((62, 66, 66), SKY_LOW, _air(1090, HAZE_FAR, HAZE_MID))), curve=True)
    return out


# ---- the water -----------------------------------------------------------------

def _ribbon_points(samples, k=1.0):
    """A ribbon's two edges in the side view, card px: (left, right)."""
    left, right = [], []
    for x, d, w, nx, nd in samples:
        left.append((x + nx * w * k / 2, land_y(x, d + nd * w * k / 2)))
        right.append((x - nx * w * k / 2, land_y(x, d - nd * w * k / 2)))
    return left, right


def _strand(samples, off):
    return [(x + nx * w * off / 2, land_y(x, d + nd * w * off / 2))
            for x, d, w, nx, nd in samples]


def water_svg(samples, water=WATER, ink=BANK_LINE, cut=BANK_CUT, flow=None, width=1.3,
              deep=WATER_DEEP, seed=1, channel=True):
    """One reach of the river in the side view: the earth cut of its far bank,
    which stands up in places and in others lets the grass come down to the
    water; the water, darker down its channel; the current drawn on it as tapered
    slivers. `flow=(begin, dur)` runs them (see `_sliver_anim`).

    Call: `river_svg` does, for each reach. `samples` come from `_centre`."""
    left, right = _ribbon_points(samples)
    out = ""
    rng = random.Random(seed)
    top, hs = [], []
    ph, ph2 = rng.uniform(0, 7), rng.uniform(0, 7)
    for k, (x, y) in enumerate(left):
        sc = depth_scale(depth_of(max(y, HORIZON + 8)))
        v = .5 + .5 * math.sin(k * .23 + ph) * math.sin(k * .07 + ph2)
        h = (.6 + 8.0 * v * v) * min(sc, 2.0)
        top.append((x, y - h))
    out += _fill(top + left[::-1], _hex(cut), curve=True)
    out += _fill(left + right[::-1], _hex(water), curve=True)
    if channel:
        chan = _strand(samples, -.34)[::2]
        chan2 = _strand(samples, .46)[::2]
        out += _fill(chan + chan2[::-1], _hex(deep), curve=True)
    out += _strands_svg(samples, flow, width)
    runs, cur = [], []
    for q in top:
        if rng.random() < .16:
            if len(cur) > 1:
                runs.append(cur)
            cur = []
        else:
            cur.append(q)
    if len(cur) > 1:
        runs.append(cur)
    out += _strokes(runs, _hex(ink), 1.1, curve=True)
    return out


SLIVER = (168, 206, 226)
# The current's four strands: (offset across the stream, wander, dashes). Each dash list is 420
# long. No strand down the middle, and none in white: it should read as light on moving water,
# not as the ruled lanes of a road.
SLIVER_OFF = ((-.62, .1, (34, 196, 16, 174)), (-.2, .18, (70, 240, 14, 96)),
              (.26, .15, (12, 128, 44, 236)), (.66, .1, (52, 300, 20, 48)))


def _sliver_anim(flow, speed):
    """Finite SMIL for a sliver: its dashes slide along the river at about `speed` px a second
    for flow=(begin, dur), start and stop gently, and freeze a whole number of dash periods on,
    so the rest pose is the pose every other verse's file opens on. Returns a function of
    (the dash's period, its offset at rest), or of nothing at all if there is no flow."""
    def anim(p, base):
        if not flow:
            return ""
        n = max(1, round(flow[1] * speed / p))
        return (f'<animate attributeName="stroke-dashoffset" from="{base:g}" to="{base - n * p:g}" '
                f'begin="{flow[0]:g}s" dur="{flow[1]:g}s" fill="freeze" calcMode="spline" '
                f'keyTimes="0;1" keySplines=".35 0 .4 1"/>')
    return anim


def _taper_layers(run_d, dash, width, anim, col, op):
    """A broken strand with tapered ends: the same dashes twice on one path, the thick ones
    shorter and centred on the thin."""
    p = sum(dash)
    thick = []
    for i in range(0, len(dash), 2):
        on, off = dash[i], dash[i + 1]
        thick += [on * .45, off + on * .55]
    sh = dash[0] * .275
    arr0, arr1 = " ".join(f"{v:g}" for v in dash), " ".join(f"{v:.1f}" for v in thick)
    return (f'<path fill="none" stroke="{col}" stroke-opacity="{op}" stroke-width="{width:g}" '
            f'stroke-dasharray="{arr0}" d="{run_d}">{anim(p, 0)}</path>'
            f'<path fill="none" stroke="{col}" stroke-opacity="{op}" stroke-width="{width * 1.9:g}" '
            f'stroke-dasharray="{arr1}" stroke-dashoffset="{-sh:.1f}" d="{run_d}">{anim(p, -sh)}</path>')


def _strands_svg(samples, flow=None, width=1.3):
    """The side view's current: tapered, wavering slivers at varied offsets, each starting at
    its own place, so that their dashes never fall in step. Reaches far off get two thin ones;
    the near one four. They sit in a `data-sl` group, which `garden_stage.bind_slivers` takes
    out or fades with the camera, since under about z .5 they are detail nobody can see."""
    rng = random.Random(len(samples))
    offs = SLIVER_OFF if width >= 1.25 else SLIVER_OFF[:3:2]
    anim = _sliver_anim(flow, 34.0)
    out = ""
    for j, (o, wander, dsh) in enumerate(offs):
        ph, f = rng.uniform(0, 7), rng.uniform(.09, .2)
        run = [(x + nx * w * (o + wander * math.sin(k * f + ph)) / 2,
                land_y(x, d + nd * w * (o + wander * math.sin(k * f + ph)) / 2))
               for k, (x, d, w, nx, nd) in enumerate(samples)][j * 2 % max(len(samples) - 3, 1)::2]
        if len(run) < 3:
            continue
        d_ = _D(0)
        d_.open_curve(run)
        out += _taper_layers(d_.text(), dsh, width * .62, anim, _hex(SLIVER), .72)
    return f'<g data-sl="1">{out}</g>'


def river_svg(flow=None, reaches=None):
    """The whole river in the side view, as {zone: svg}: `far` lies over the far
    banks, `mid` over the middle ones, `near` from the people's line to the parting,
    with the four heads. `flow=(begin, dur)` runs the water for that long and stops it
    (see `_sliver_anim`). `reaches` limits which of "far", "mid", "near", "heads" run; a
    close shot needs only "near", and every other strand stays still at the same pose.

    Call: `panorama(flow=...)` draws it. By hand, `river_svg((0, 6))["near"]`: the zones go between banks."""
    def on(name):
        return flow if reaches is None or name in reaches else None
    main = _cut_side(_MAIN)
    far, mid, near = [], [], []
    for q in main:
        (far if q[1] > 620 else (mid if q[1] > 40 else near)).append(q)
    # overlap the reaches so no seam shows
    if mid and far:
        mid = [far[-1]] + mid
    if near and mid:
        near = [mid[-1]] + near
    out = {"far": "", "mid": "", "near": ""}
    if far:
        out["far"] = water_svg(far, _mix(WATER, SKY_LOW, .45), _mix(BANK_LINE, SKY_LOW, .4),
                               _mix(BANK_CUT, SKY_LOW, .3), on("far"), .9,
                               _mix(WATER_DEEP, SKY_LOW, .45), 2)
    if mid:
        out["mid"] = water_svg(mid, _mix(WATER, SKY_LOW, .22), _mix(BANK_LINE, SKY_LOW, .2),
                               BANK_CUT, on("mid"), 1.1,
                               _mix(WATER_DEEP, SKY_LOW, .22), 3)
    for k, name in enumerate(("Pishon", "Gihon", "Hiddekel", "Euphrates")):
        out["near"] += water_svg(_cut_side(_HEADS[name]), flow=on("heads"), seed=10 + k,
                                 channel=name == "Euphrates")
    out["near"] += water_svg(near, flow=on("near"), seed=4)
    return out


# ---------------------------------------------------------------------------
# The garden's extent
# ---------------------------------------------------------------------------
#
# The text gives no wall. It gives a river "to water the garden" (2:10) and
# "the east of the garden" (3:24). So the edge drawn here is the edge of what
# water does: the planting is thickest in the river's reach, thins to single
# trees, then bushes, then tufts, and the ground goes over from green to dust
# across about seven hundred px. In the west the land lifts toward Eden's high
# ground and the river comes down out of it. In the east there are two old
# cypresses, the last trees, with the way going out past their feet: no gate, but
# a thing you can recognise from any distance as where the garden stops.

# The garden's outline in plan, (x, d). Not an oval: long along the river, with
# bays where the water does not reach and a tongue to the parting.
GARDEN_EDGE = [(-3420, 1560), (-3040, 1360), (-2640, 980), (-2300, 760), (-1800, 1180),
               (-1340, 1720), (-760, 1560), (-420, 1060), (120, 980), (520, 1500),
               (1060, 1720), (1500, 1240), (1860, 1100), (2040, 620), (1880, 260),
               (2160, 20), (2420, -180), (2460, -460), (2160, -620), (2060, -1060),
               (1720, -1640), (1140, -1500), (680, -1120), (240, -760), (-260, -1020),
               (-640, -1560), (-1240, -1620), (-1760, -1240), (-1840, -760),
               (-2240, -460), (-2580, 40), (-2960, 560), (-3300, 1060), (-3560, 1440)]

LIFE_X, LIFE_D = -420.0, 34.0
KNOW_X, KNOW_D = 370.0, 22.0
WAY_TREES = ((2130.0, 150.0), (2330.0, 96.0))      # the two last cypresses


def _seg_dist(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    t = ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / ((dx * dx + dy * dy) or 1)
    t = max(0, min(1, t))
    return math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy)


def garden_density(x, d):
    """How thickly the garden is planted at a point of the plan: 1 well inside
    the outline, falling to nothing a little past it. It is what thins the
    trees, then the bushes, then the tufts, and it is the whole of the edge.

    Call: `garden_density(x, d)` -> 0..1, (x, d) a plan point (see `depth_of` for a card y's d)."""
    p = (x, d)
    dist = min(_seg_dist(p, GARDEN_EDGE[i - 1], GARDEN_EDGE[i])
               for i in range(len(GARDEN_EDGE)))
    if not _inside(p, GARDEN_EDGE):
        dist = -dist
    return max(0.0, min(1.0, (dist + 180.0) / 620.0))


# ---------------------------------------------------------------------------
# THE STAGER'S CONSTANTS. World px: one px is one screen px at zoom 1. x is east.
# The side view and the plan share x; on the people's line they share y too.
# ---------------------------------------------------------------------------

# The ground. GROUND is the people's line, nominally; feet go on ground_y(x), which rises
# and falls under them. Elsewhere on the land, use land_y(x, d) and depth_scale(d).

# The two trees' feet.
LIFE_XY = (LIFE_X, project(LIFE_D))         # stands west
KNOWLEDGE_XY = (KNOW_X, project(KNOW_D))    # stands east
QUIET_X = (-360, 320)               # behind this stretch of the line, out to QUIET_D north of it,
QUIET_D = 560                       # only low plants grow, so that nothing stands behind a figure's head

# The man. He is formed on Eden's dry shoulder, west of where the garden will stand ("planted
# a garden eastward, in Eden, and there he put the man", 2:8), and put between the trees.
MAN_FIRST = (-1700, ground_y(-1700))
MAN_PUT = (-110, ground_y(-110))
# The bare land has no dry patch here, round where he is formed, from the ground to his head, and
# the land no engraved line: the camera goes down to this ground at z 7 and to his face at z 6
# (2:7), and pebbles at that size would be grains in the air before him, and a line one on him
FORMED_CLEAR = (MAN_FIRST[0] - 60, MAN_FIRST[1] - 140, MAN_FIRST[0] + 60, MAN_FIRST[1] + 2)
# Eden's dry shoulder, where he is formed: as the garden is planted (2:8) the land is dust to the
# first x and green from the second on the people's line (`shoulder_edge` elsewhere), and only
# greens to the west of them as he walks off it
SHOULDER = (MAN_FIRST[0] + 140, MAN_FIRST[0] + 500)
ON_SHOULDER = sum(SHOULDER) / 2     # what is placed west of this is on it

# The fruit: knowledge_reach() lists those a hand can reach. TAKE_FRUIT is the first of them,
# by its index for heroes_svg(taken=...).
TAKE_FRUIT = 3


def _far_shape(rng, kind):
    """A far tree as two flat shapes (deep, body), for the wood in the distance:
    at that size the silhouette is all there is, and it costs a tenth of the
    drawing. Paint comes from the `use`: fill for the dark, color for the body,
    so the same drawing goes back in tone with distance."""
    deep, mid = [], []
    if kind == "dome":
        for cx, cy, rx, ry in ((-120, 210, 92, 72), (0, 280, 120, 84),
                               (118, 214, 92, 70), (0, 170, 110, 56)):
            deep.append(lobed(rng, cx, cy, rx, ry, 38, .5))
        for cx, cy, rx, ry in ((-128, 228, 60, 44), (-16, 300, 80, 52),
                               (98, 232, 58, 42)):
            mid.append(lobed(rng, cx, cy, rx, ry, 38, .5))
        deep.append([(-14, 0), (-10, 130), (10, 130), (14, 0)])
    elif kind == "broken":
        for cx, cy, rx, ry in ((-92, 150, 58, 32), (-34, 214, 60, 32),
                               (62, 204, 62, 34), (106, 146, 50, 28)):
            deep.append(lobed(rng, cx, cy, rx, ry, 32, .55))
        for cx, cy, rx, ry in ((-104, 160, 34, 16), (-42, 224, 36, 16),
                               (50, 216, 38, 16), (94, 156, 30, 14)):
            mid.append(lobed(rng, cx, cy, rx, ry, 38, .5))
        deep.append([(-16, 0), (-8, 110), (8, 110), (16, 0)])
    elif kind == "column":
        n = 9
        left = [(-44 * math.sin(math.pi * (i / n) ** .72) ** .72 - 1,
                 20 + 440 * i / n) for i in range(n + 1)]
        right = [(44 * math.sin(math.pi * (i / n) ** .72) ** .72 + 1,
                  20 + 440 * i / n) for i in range(n + 1)]
        deep.append(left + right[::-1])
        deep.append([(-8, 0), (-6, 30), (6, 30), (8, 0)])
        mid.append([(-30 * math.sin(math.pi * (i / n) ** .72) ** .72,
                     40 + 380 * i / n) for i in range(n + 1)] +
                   [(-4, 410), (-2, 40)])
    elif kind == "palm":
        deep.append([(-7, 0), (4, 180), (-6, 370), (2, 370), (12, 180), (9, 0)])
        for a, L in ((-.1, 130), (.5, 130), (1.1, 110), (1.7, 110), (2.3, 125),
                     (2.9, 130), (3.3, 120)):
            x1 = L * math.cos(a)
            y1 = L * math.sin(a) - L * .3
            mx, my = x1 * .55, L * .55 * math.sin(a) + L * .12
            deep.append([(-2, 370), (mx, 370 + my + 9), (x1, 370 + y1),
                         (mx, 370 + my - 9)])
    return deep, mid


def far_tree_def(gid, kind, seed=1):
    """A far tree (`_far_shape`) as a <defs> entry: "dome", "broken", "column" or
    "palm". Its paint comes from the parent of the <use> (fill and color)."""
    rng = random.Random(seed)
    deep, mid = _far_shape(rng, kind)
    dd = _D(0)
    for o in deep:
        pts = [(x * PXU, -y * PXU) for x, y in o]
        if _area(pts) < 0:
            pts = pts[::-1]
        dd.closed_curve(pts)
    out = f'<path d="{dd.text()}"/>'
    if mid:
        dm = _D(0)
        for o in mid:
            pts = [(x * PXU, -y * PXU) for x, y in o]
            if _area(pts) < 0:
                pts = pts[::-1]
            dm.closed_curve(pts)
        out += f'<path fill="currentColor" d="{dm.text()}"/>'
    return f'<g id="{gid}">{out}</g>'


# ---------------------------------------------------------------------------
# The panorama
# ---------------------------------------------------------------------------

SPECIES = {"s": (shade_tree, SHADE_PAINT), "o": (olive, OLIVE_PAINT),
           "f": (fig, FIG_PAINT), "p": (date_palm, PALM_PAINT),
           "c": (cypress, CYPRESS_PAINT), "g": (pomegranate, POMEGRANATE_PAINT)}


def _pick_species(rng, x, d, density):
    """Which tree grows here: figs and pomegranates in the watered middle,
    olives and cypresses toward the dry edge, palms by the water."""
    near_river = _near_water(x)
    wet = near_river is not None and d - near_river < 260
    table = [("s", 20), ("o", 18), ("f", 13), ("g", 11), ("p", 16 if wet else 9),
             ("c", 8)]
    if density < .55:
        table = [("o", 34), ("c", 26), ("s", 8), ("p", 6)]
    r = rng.uniform(0, sum(w for _, w in table))
    for k, w in table:
        r -= w
        if r <= 0:
            return k
    return table[0][0]


# the trees that frame the two named ones, by hand: (species, x, d, size)
HAND_TREES = [("s", -1120, 150, .98), ("f", -860, 74, .92), ("p", -960, 250, 1.02),
              ("g", -790, 230, .9), ("c", -1310, 330, 1.0), ("o", -1420, 120, 1.0),
              ("f", 900, 70, .96), ("p", 1060, 200, 1.04), ("g", 830, 210, .94),
              ("s", 1340, 160, 1.0), ("o", 1140, 60, 1.0), ("c", 1000, 340, 1.0),
              ("s", 720, 520, .9), ("c", -640, 500, .94), ("o", -760, 400, .92)]


def forest():
    """Every tree the side view plants, (species, x, d, size): the hand-placed
    ones round the middle, then a jittered grid thinned by `garden_density`,
    leaving clear the people's line and the air round the two named trees.

    Call: `forest()` -> [(species id, x, d, size)]; its card y is `land_y(x, d)` and its scale
    `depth_scale(d) * size`. This is what the plan's crowns are too."""
    rng = random.Random(1234)
    out = list(HAND_TREES)
    taken = [(t[1], t[2]) for t in out]
    d = 90.0
    row = 0
    while d < 2600:
        dx = 250 + d * .04
        x = X0 + (row % 2) * dx / 2
        while x < X1:
            px = x + rng.uniform(-dx * .4, dx * .4)
            pd = d + rng.uniform(-40, 40)
            x += dx
            den = garden_density(px, pd)
            # stragglers beyond the edge are olives and cypresses, rarely
            if rng.random() > den ** 1.4 * 1.05:
                continue
            if abs(px - LIFE_X) < 400 and pd < 480:
                continue
            if -300 < px < 150 and pd < 900:
                continue
            if abs(px - KNOW_X) < 460 and pd < 440:
                continue
            if any(abs(px - a) < 130 and abs(pd - b) < 90 for a, b in taken):
                continue
            taken.append((px, pd))
            out.append((_pick_species(rng, px, pd, den), px, pd,
                        rng.uniform(.84, 1.12)))
        d += 120 + d * .18
        row += 1
    # the last trees, on the way out
    for wx, wd in WAY_TREES:
        out.append(("c", wx, wd, 1.08))
    return out


def pebbles(rng, n=9):
    """Small stones lying about: each a lit top and a dark foot."""
    P = []
    for _ in range(n):
        x, y = rng.uniform(-30, 30), rng.uniform(-14, 6)
        w = rng.uniform(2.6, 7)
        P.append(("fill", [(x - w, y + w * .1), (x - w * .4, y + w * .62),
                           (x + w * .5, y + w * .4), (x + w, y - w * .1),
                           (x + w * .2, y - w * .24)], "pebble"))
        P.append(("line", [(x - w * .3, y - w * .22), (x + w, y - w * .1)], "pebble_foot"))
    return P


def cracks(rng, w=120.0):
    """Ground dried and split: a few branching lines, no plant anywhere."""
    P = []
    for _ in range(4):
        x, y = rng.uniform(-w / 2, w / 2), rng.uniform(-22, 0)
        a = rng.uniform(-.6, .6) + (math.pi if rng.random() < .5 else 0)
        pts = [(x, y)]
        for k in range(5):
            L = rng.uniform(7, 16)
            a += rng.uniform(-.8, .8)
            x += L * math.cos(a)
            y += L * .36 * math.sin(a)
            pts.append((x, y))
            if k == 2:
                b = a + rng.choice((-1, 1)) * 1.1
                P.append(("line", [(x, y), (x + 12 * math.cos(b), y + 4.4 * math.sin(b))], "crack"))
        P.append(("line", pts, "crack"))
    return P


MEADOW_PATCHES = {
    "ma": [(grass_tuft, 5), (fern, 2), (daisy, 2)],
    "mb": [(grass_tuft, 3), (herb, 2), (anemone, 2), (fern, 1)],
    "mc": [(grass_tuft, 3), (lily, 2), (violet, 1), (fern, 1)],
    "lo": [(lambda r: grass_tuft(r, 14, 4), 5), (fern, 2), (daisy, 1), (violet, 1)],
    "re": [(reed, 3), (grass_tuft, 1)],
}
DRY_PATCHES = {
    "da": [(lambda r: grass_tuft(r, 16, 4, dry=True), 3), (lambda r: pebbles(r, 4), 1)],
    "db": [(lambda r: pebbles(r, 8), 2), (lambda r: cracks(r), 1)],
}
THORN_PATCHES = {
    "ta": [(lambda r: thorns(r.randint(0, 99), 62), 2), (lambda r: grass_tuft(r, 18, 4, dry=True), 1)],
    "tb": [(lambda r: thistle(r.randint(0, 99), 72), 2), (lambda r: thorns(r.randint(0, 99), 46), 1)],
}


def plant_defs(state="planted", thorns_too=False):
    """The drifts of plants a land's state uses, as <defs> content."""
    out = ""
    table = {}
    if state == "planted":
        table.update(MEADOW_PATCHES)
        table.update(DRY_PATCHES)
    else:
        table.update(DRY_PATCHES)
    if state == "barren":
        table.pop("da", None)
    if thorns_too:
        table.update(THORN_PATCHES)
    for i, (name, recipe) in enumerate(table.items()):
        rng_w = 230 if name[0] != "r" else 190
        out += f'<g id="{name}">' + render(patch(500 + i, recipe, rng_w, 26, marks=3),
                                           PLANT_PAINT) + "</g>"
    if state == "planted":
        out += '<g id="sa">' + render(shrub(3), SHADE_PAINT) + "</g>"
    for name, parts in (("ra", rock(11, 70, 36)), ("rb", rock(12, 110, 52)),
                        ("rc", outcrop(5, 210, 78))):
        out += f'<g id="{name}">' + render(_in_order(parts, ("rock", "rock_lit",
                                                             "rock_deep", "rock_line")),
                                           PLANT_PAINT) + "</g>"
    return out


def _use(gid, x, y, k=1.0, flip=False):
    if k == 1.0 and not flip:
        return f'<use href="#{gid}" x="{x:.0f}" y="{y:.0f}"/>'
    sx = f"-{k:.2f}" if flip else f"{k:.2f}"
    sc = f"scale({sx} {k:.2f})" if flip else f"scale({k:.2f})"
    return f'<use href="#{gid}" transform="translate({x:.0f} {y:.0f}){sc}"/>'


def place(gid, x, y, k=1.0, flip=False):
    """One of the scene's drawings, placed: `place("f", x, y)` for a fig at its foot (x, y).
    Ids: s o f p c g (shade tree, olive, fig, date palm, cypress, pomegranate), sa (a shrub), ma
    mb mc lo (plant drifts), re (reeds), ra rb rc (rocks), da db (dry ground), ta tb (thorns,
    thistles: thorns_too only), LF KN (the named trees), kf (a fruit), Fd Fb Fc
    Fp (far trees). Scene.trimmed(..., keep=[ids]) keeps a drawing a stager means to place."""
    return _use(gid, x, y, k, flip)


def _grow_use(gid, x, y, k=1.0, flip=False, begin=0.0, dur=1.4):
    """A <use> that rises out of the ground about its feet: scale 0 to k, eased, held.
    The world does the growing: there is no hand in it and nothing that glows."""
    sx = -k if flip else k
    return (f'<g transform="translate({x:.0f} {y:.0f})"><use href="#{gid}" transform="scale(0)">'
            f'<animateTransform attributeName="transform" type="scale" values="0 0;{sx:.2f} {k:.2f}" '
            f'begin="{begin:.2f}s" dur="{dur:.2f}s" fill="freeze" calcMode="spline" '
            f'keyTimes="0;1" keySplines=".2 .7 .3 1"/></use></g>')


# Rocks are the same in every state of the land: (id, x, d, size). That is what
# makes the barren land the garden's own ground: the same swell, the same stones.
ROCKS = [("rc", -2620, 300, 1.2), ("rb", -2330, 240, 1.1), ("rc", -2960, 620, 1.3),
         ("rb", -3120, 330, 1.2), ("ra", -2080, 60, 1.0),
         ("ra", -1560, 120, .8), ("ra", -720, 40, .7),
         ("ra", 700, -30, .7), ("rb", 1180, -40, .8),
         ("ra", 1560, 90, .9), ("rc", 1840, -60, .85),
         ("ra", 2560, 40, 1.0), ("rc", 2760, 210, 1.1), ("rb", 3050, 60, 1.2),
         ("ra", 3320, 240, 1.2),
         ("rb", -860, -520, .8), ("ra", 280, -540, .7), ("rc", 1490, -560, .6),
         ("ra", -1680, -560, .8), ("rb", 2500, -560, .55)]


def _rounded(svg):
    """A run of scenery in a group that sets round caps and joins. Scenery depends on them:
    a pip of fruit or flower is a zero-length stroke with a round cap, and nothing at all
    with any other. So it carries them itself, whatever a stager's page sets."""
    return f'<g stroke-linecap="round" stroke-linejoin="round">{svg}</g>'


def _prune(defs, used_in):
    """`defs` without the <g id=...> drawings that nothing in `used_in` calls."""
    used = set(re.findall(r'href="#([^"]+)"', used_in))

    def drop(m):
        return m.group(0) if m.group(1) in used else ""
    return re.sub(r'<g id="([^"]+)">.*?</g>', drop, defs, flags=re.S)


# ---- what a frame can see ------------------------------------------------------

_D_TOKEN = re.compile(r"[A-Za-z]|-?(?:\d+\.\d*|\.\d+|\d+)")
_D_ARGS = {"m": 2, "l": 2, "h": 1, "v": 1, "q": 4, "t": 2, "c": 6, "s": 4, "a": 7}


def _arc_box(p0, rx, ry, phi, large, sweep, p1):
    """The box of the whole ellipse an SVG arc from p0 to p1 runs on, (x0, y0, x1, y1): its centre
    by the spec's endpoint-to-centre conversion, its radii grown, as SVG grows them, where they
    can't span the chord. It holds any part of the ellipse, the long way round included."""
    rx, ry = abs(rx), abs(ry)
    if not rx or not ry or p0 == p1:
        return min(p0[0], p1[0]), min(p0[1], p1[1]), max(p0[0], p1[0]), max(p0[1], p1[1])
    c, s = math.cos(math.radians(phi)), math.sin(math.radians(phi))
    dx, dy = (p0[0] - p1[0]) / 2, (p0[1] - p1[1]) / 2
    x1, y1 = c * dx + s * dy, -s * dx + c * dy
    lam = x1 * x1 / (rx * rx) + y1 * y1 / (ry * ry)
    if lam > 1:
        rx, ry = rx * math.sqrt(lam), ry * math.sqrt(lam)
    num = rx * rx * ry * ry - rx * rx * y1 * y1 - ry * ry * x1 * x1
    k = math.sqrt(max(0.0, num / ((rx * rx * y1 * y1 + ry * ry * x1 * x1) or 1)))
    k = -k if large == sweep else k
    cx1, cy1 = k * rx * y1 / ry, -k * ry * x1 / rx
    cx = c * cx1 - s * cy1 + (p0[0] + p1[0]) / 2
    cy = s * cx1 + c * cy1 + (p0[1] + p1[1]) / 2
    hx, hy = math.hypot(rx * c, ry * s), math.hypot(rx * s, ry * c)
    return cx - hx, cy - hy, cx + hx, cy + hy


@functools.lru_cache(maxsize=None)
def _path_box(d):
    """A path's box, (x0, y0, x1, y1): its points and its curves' controls, a smooth curve's
    reflected one too, and the whole ellipse of an arc, so that it can be a little generous and is
    never short. Every command of SVG's path grammar."""
    toks = _D_TOKEN.findall(d)
    xs, ys = [], []
    px = py = sx = sy = 0.0
    ctrl = None
    i, cmd = 0, ""
    while i < len(toks):
        if toks[i].isalpha():
            cmd = toks[i]
            i += 1
            if cmd in "zZ":
                px, py, ctrl = sx, sy, None
                continue
        low, rel = cmd.lower(), cmd.islower()
        a = [float(q) for q in toks[i:i + _D_ARGS[low]]]
        i += _D_ARGS[low]
        ox, oy = (px, py) if rel else (0.0, 0.0)
        if low == "h":
            px = ox + a[0]
        elif low == "v":
            py = oy + a[0]
        elif low == "a":
            ex, ey = ox + a[5], oy + a[6]
            box = _arc_box((px, py), a[0], a[1], a[2], int(a[3]), int(a[4]), (ex, ey))
            xs += [px - a[0], px + a[0], ex - a[0], ex + a[0], box[0], box[2]]
            ys += [py - a[1], py + a[1], ey - a[1], ey + a[1], box[1], box[3]]
            px, py = ex, ey
        elif low == "t":
            ctrl = (2 * px - ctrl[0], 2 * py - ctrl[1]) if ctrl else (px, py)
            xs.append(ctrl[0])
            ys.append(ctrl[1])
            px, py = ox + a[0], oy + a[1]
            xs.append(px)
            ys.append(py)
            continue
        else:
            if low == "s":
                first = (2 * px - ctrl[0], 2 * py - ctrl[1]) if ctrl else (px, py)
                xs.append(first[0])
                ys.append(first[1])
            for k in range(0, len(a) - 2, 2):
                xs.append(ox + a[k])
                ys.append(oy + a[k + 1])
            px, py = ox + a[-2], oy + a[-1]
            ctrl = (ox + a[-4], oy + a[-3]) if low in "qcs" else None
        if low == "m":
            sx, sy = px, py
            cmd = "l" if rel else "L"
        xs.append(px)
        ys.append(py)
    return (min(xs), min(ys), max(xs), max(ys)) if xs else (0.0, 0.0, 0.0, 0.0)


_G_ID = re.compile(r'<g id="([^"]+)">(.*?)</g>', re.S)
_D_ATTR = re.compile(r'<path\b[^>]*?\bd="([^"]*)"[^>]*?>')
_WIDTH = re.compile(r'stroke-width="([\d.]+)"')


@functools.lru_cache(maxsize=8)
def _drawing_boxes(defs):
    """{a drawing's id in `defs`: its box}, its strokes included."""
    out = {}
    for gid, body in _G_ID.findall(defs):
        boxes = []
        for m in _D_ATTR.finditer(body):
            b = _path_box(m.group(1))
            w = _WIDTH.search(m.group(0))
            w = float(w.group(1)) / 2 if w else 1.0
            boxes.append((b[0] - w, b[1] - w, b[2] + w, b[3] + w))
        if boxes:
            out[gid] = (min(b[0] for b in boxes), min(b[1] for b in boxes),
                        max(b[2] for b in boxes), max(b[3] for b in boxes))
    return out


_PATH_EL = re.compile(r'<path\b[^>]*?\bd="([^"]*)"[^>]*?(?:/>|>.*?</path>)', re.S)
_RECT_EL = re.compile(r'<rect x="(-?[\d.]+)" y="(-?[\d.]+)" width="([\d.]+)" height="([\d.]+)"[^>]*/>')
_USE_AT = re.compile(r'<use href="#([^"]+)" x="(-?[\d.]+)" y="(-?[\d.]+)"/>')
_USE_TF = re.compile(r'<use href="#([^"]+)" transform="translate\((-?[\d.]+) (-?[\d.]+)\)'
                     r'scale\((-?[\d.]+)(?: (-?[\d.]+))?\)"/>')
_USE_GROW = re.compile(r'<g transform="translate\((-?[\d.]+) (-?[\d.]+)\)"><use href="#([^"]+)" '
                       r'transform="scale\(0\)"><animateTransform [^>]*?values="0 0;(-?[\d.]+) (-?[\d.]+)"'
                       r'[^>]*/></use></g>')
_EMPTY_G = re.compile(r'<g(?: [^>]*)?></g>')


def _meets(rect, x0, y0, x1, y1):
    return x0 <= rect[2] and x1 >= rect[0] and y0 <= rect[3] and y1 >= rect[1]


def _grown(box, w):
    return box[0] - w, box[1] - w, box[2] + w, box[3] + w


def _placed(box, x, y, kx, ky):
    """A drawing's box, placed at (x, y) and scaled."""
    xa, xb = sorted((x + box[0] * kx, x + box[2] * kx))
    return xa, y + box[1] * ky, xb, y + box[3] * ky


def in_frame(svg, rect, defs):
    """A run of scenery without what a camera over `rect` can never see. Only for a run whose paths
    are in world px, with no transformed group round them, as `panorama`'s are, and its <use>s as
    `_use` and `_grow_use` place them. A <use> of a drawing not in `defs` stays."""
    boxes = _drawing_boxes(defs)

    def placed(m, gid, x, y, kx, ky):
        b = boxes.get(gid)
        if b is None or _meets(rect, *_placed(b, x, y, kx, ky)):
            return m.group(0)
        return ""

    def path(m):
        w = _WIDTH.search(m.group(0))
        w = max(float(w.group(1)) if w else 1.0, 2.0)
        d = m.group(1)
        pieces = re.split(r"(?=M)", d)[1:] if d.count("M") > 1 else [d]
        kept = [q for q in pieces if _meets(rect, *_grown(_path_box(q), w))]
        if not kept:
            return ""
        return m.group(0) if len(kept) == len(pieces) else m.group(0).replace(d, "".join(kept), 1)

    def box(m):
        x, y, w, h = (float(q) for q in m.groups())
        return m.group(0) if _meets(rect, x, y, x + w, y + h) else ""

    def tf(m):
        k = float(m.group(4))
        return placed(m, m.group(1), float(m.group(2)), float(m.group(3)), k, float(m.group(5) or k))

    def grow(m):
        return placed(m, m.group(3), float(m.group(1)), float(m.group(2)), float(m.group(4)),
                      float(m.group(5)))
    svg = _USE_GROW.sub(grow, svg)
    svg = _USE_AT.sub(lambda m: placed(m, m.group(1), float(m.group(2)), float(m.group(3)), 1.0, 1.0),
                      svg)
    svg = _USE_TF.sub(tf, svg)
    svg = _PATH_EL.sub(path, svg)
    svg = _RECT_EL.sub(box, svg)
    return _EMPTY_G.sub("", svg)


def _flat_between(stops, x0, x1):
    """The one colour a west-to-east ramp has from x0 to x1, or None if it changes there."""
    (wa, dust), (wb, green), (ea, _g), (eb, _d) = stops
    if x1 <= wa or x0 >= eb:
        return dust
    if wb <= x0 and x1 <= ea:
        return green
    return None


class Scene:
    """A drawn state of the land. `defs` goes in <defs>. Draw `behind`, then `outside`
    (the thorn land, if any: a stager brings it up at 3:18), then the people, then
    `front` (the river's near reach, its banks, the near ground). Every x and y in it
    is a world px (see THE STAGER'S CONSTANTS). `ramps` is `land_ramps`, for a trim."""

    def __init__(self, defs, behind, front, outside="", ramps=None):
        self.defs, self.behind, self.front = defs, behind, front
        self.outside = outside
        self.ramps = ramps

    def trimmed(self, rect, keep=()):
        """The same scene with what a camera over `rect` can never see taken out: every path, rect,
        placed plant, rock or tree wholly outside it (`in_frame`), every drawing nothing is left to
        call, and every gradient of the ground that doesn't change within it, which becomes a flat
        fill. A verse that stays near the middle needs no olive grove in the far west, and this is
        how a file stays well under the budget and a frame stays cheap. `rect` is (x0, y0, x1, y1),
        world px at the frame's edges over the whole flight. `keep` names drawings to hold on to for
        your own `place`."""
        behind, front, outside = (in_frame(self.behind, rect, self.defs),
                                  in_frame(self.front, rect, self.defs),
                                  in_frame(self.outside, rect, self.defs))
        defs = self.defs
        for gid, stops in (self.ramps or {}).items():
            flat = _flat_between(stops, rect[0], rect[2])
            if flat:
                fill, hex_ = f"url(#{gid})", _hex(flat)
                behind, front, outside = (behind.replace(fill, hex_), front.replace(fill, hex_),
                                          outside.replace(fill, hex_))
            if f"url(#{gid})" not in behind + front + outside:
                defs = re.sub(f'<linearGradient id="{gid}".*?</linearGradient>', "", defs)
        if "url(#gvig)" not in front:
            defs = re.sub('<linearGradient id="gvig".*?</linearGradient>', "", defs)
        calls = "".join(f'href="#{k}"' for k in keep)
        # so that panorama(heroes=False).trimmed(...) can still take heroes_svg(...)
        boxes = _drawing_boxes(self.defs)
        for gid, x, d in (("LF", LIFE_X, LIFE_D), ("KN", KNOW_X, KNOW_D)):
            if gid in boxes and _meets(rect, *_placed(boxes[gid], x, project(d), 1.0, 1.0)):
                calls += f'href="#{gid}"href="#kf"'
        return Scene(_prune(defs, behind + front + outside + calls), behind, front, outside)


def _stage_patches(rng, y_fn, kinds, x_lo, x_hi, step, k=1.0, gap=0.0):
    out = ""
    x = x_lo
    while x < x_hi:
        px = x + rng.uniform(-step * .3, step * .3)
        kind = rng.choice(kinds)
        if kind == "re" and QUIET_X[0] - 120 < px < QUIET_X[1] + 120:
            kind = "lo"             # reeds would stand as high as a figure's knees
        out += _use(kind, px, y_fn(px) + gap, k * rng.uniform(.9, 1.1), rng.random() < .5)
        x += step * rng.uniform(.7, 1.3)
    return out


# (species, x, card y, size): the near wings of the wide shot. Their crowns stop
# well below y 1560 at the middle, and clear of the river's bends at the sides.
NEAR_TREES = [("o", -2800, 2110, 1.6), ("s", -2400, 2340, 1.7), ("f", -2050, 2280, 1.6),
              ("p", -3150, 2300, 1.3), ("g", -1700, 2420, 1.7),
              ("s", 1680, 2800, 1.8), ("f", 1300, 2740, 1.6), ("o", 2100, 2680, 1.6),
              ("g", 960, 2800, 1.7)]


def way_svg(state="planted", fade=None):
    """The way (3:24): the ground worn pale, running out to the east along the people's
    line, between the last two trees. It starts from nothing in the grass well inside the
    garden and only becomes a track where the grass gives out. A wide band of ground
    colour, not a road; no edge is drawn on it. `fade=(begin, dur)` brings it up.

    Call: `panorama` draws it. By hand, `way_svg()`, between the last bank and the people."""
    if state == "barren":
        return ""
    xs = list(range(1000, 4100, 240))
    upper, lower = [], []
    for x in xs:
        t = _smoothstep(1000, 2200, x)
        hw = (1 + 13 * t) * (1 + .22 * math.sin(x * .013))
        c = ground_y(x) + 14
        upper.append((x, c - hw))
        lower.append((x, c + hw * 1.2))
    if fade:
        d = _D(0)
        pts = upper + lower[::-1]
        d.closed_curve(pts[::-1] if _area(pts) < 0 else pts)
        return (f'<path fill="#a39067" fill-opacity=".34" opacity="0" d="{d.text()}">'
                f'{_fade_in(*fade)}</path>')
    return _fill(upper + lower[::-1], "#a39067", curve=True, extra=' fill-opacity=".34"')


def _plant_spots(rng, planted, lean):
    """Where the plants between the trees go, depth by depth, in the land's random stream: (x, d).
    Thick where the garden is; on the bare land, its dry patches."""
    d = 100.0
    while (planted and d < 700) or (not planted and d < 2400):
        dx = (360 + d * .36) if planted else (300 + d * .4)
        if lean:
            dx *= 2.2
        x = X0
        while x < X1:
            px = x + rng.uniform(-dx * .45, dx * .45)
            pd = d + rng.uniform(-30, 30)
            x += dx
            yield px, pd
        d += (80 + d * .3) if planted else (90 + d * .4)


def _scrub_spots(rng, planted, lean):
    """The stones and scrub past the water's reach, in the land's random stream: (kind, x, d,
    flip), everywhere if nothing is planted, at the two ends if something is."""
    for _ in range(46 if not planted else 12 if lean else 24):
        px = rng.uniform(-3600, 3800)
        if planted and -2500 < px < 2300:
            continue
        pd = rng.uniform(-680, -40)
        if project(pd) < near_bank_y(0, px) + 8 and (pd < -60 or planted):
            continue
        kind = "db" if (not planted or rng.random() < .55) else "da"
        yield kind, px, pd, rng.random() < .5


@functools.cache
def _bare_patch_box():
    return _drawing_boxes(plant_defs("barren"))["db"]


def _bare_use(gid, x, y, k, flip):
    """One of the bare land's dry patches, or nothing where he is formed (FORMED_CLEAR)."""
    if _meets(FORMED_CLEAR, *_placed(_bare_patch_box(), x, y, -k if flip else k, k)):
        return ""
    return _use(gid, x, y, k, flip)


def bare_scrub(gid="bd"):
    """The bare land's dry patches where panorama("barren") lays them, as {"far", "stage",
    "front": [(x, svg)]}, its plants beyond d 360 and nearer, and the scrub on the near ground,
    by the drawing `gid` (`bare_patch_def`): for a scene that opens on the bare land and greens
    it (2:8)."""
    rng = random.Random(77)
    out = {"far": [], "stage": [], "front": []}
    for px, pd in _plant_spots(rng, False, False):
        u = _bare_use(gid, px, land_y(px, pd), depth_scale(pd), rng.random() < .5)
        out["far" if pd > 360 else "stage"].append((px, u))
    for _kind, px, pd, flip in _scrub_spots(rng, False, False):
        out["front"].append((px, _bare_use(gid, px, project(pd), min(depth_scale(pd), 2.3), flip)))
    return out


def bare_patch_def(gid="bd"):
    """The bare land's dry patch, its drawing in plant_defs("barren"), by another id."""
    return f'<g id="{gid}">' + render(patch(500, DRY_PATCHES["db"], 230, 26, marks=3),
                                      PLANT_PAINT) + "</g>"


_USE_X = re.compile(r'<use href="#[^"]+" (?:x="(-?[\d.]+)"|transform="translate\((-?[\d.]+) )')


def _west_of(svg, x):
    """A run of placed drawings split at x: (those west of it, the rest)."""
    west = east = ""
    for m in re.finditer(r"<use\b[^>]*/>", svg):
        at = _USE_X.match(m.group(0))
        if at and float(at.group(1) or at.group(2)) < x:
            west += m.group(0)
        else:
            east += m.group(0)
    return west, east


def panorama(state="planted", flow=None, thorns_too=False, lean=False, heroes=True,
             plant_in=None, flow_reaches=None, wet=False, river=None):
    """The whole side view, as a Scene. Call it once per file: it takes about a fifth of
    a second, and Scene.trimmed(rect) cuts it down to what that verse's camera sees.

    `state`: "planted" (the garden, the land beyond its reach as dust) or "barren" (2:5:
    no plant or herb, dust, the river's course a dry hollow). The contours and the rocks
    are the same in both.

    `flow=(begin, dur)` runs the water for that long and stops it where it began;
    `flow_reaches` limits it to some of "far", "mid", "near", "heads". `thorns_too` puts
    the thorn land at the east end of a planted panorama, in Scene.outside, for a stager
    who has reached 3:18. `heroes=False` leaves off the two named trees for `heroes_svg`,
    drawn after `.behind`. `wet=True` is the dust a shade darker, from 2:6's "watered" to
    2:9. `river` is the {zone: svg} to draw in place of `river_svg(flow, flow_reaches)`, as
    `dry_course_svg()` is at 2:8-9, or a stager's own at 2:10.

    `lean=True` is for a camera that moves (see the module's note on the budget): flat cut
    silhouettes for all but the nearest plain trees, a third of the plants; the named trees are
    unchanged. Much the same at zoom .17, about half the paint, and behind people at zoom .5 or 1
    it holds up well. Keep the full drawing where a verse happens among the trees.

    `plant_in` (planted only) is 2:8-9 as it happens, as {phase: (begin, dur)} for "green",
    "plants" and "trees": the file opens on the dust and those come up over it, the near
    trees each rising about their feet. A phase not named is already there. "trees": None
    leaves the trees out, for the verse before they rise, with everything else where it will
    be when they have. It costs about the barren land again in bytes, on that one verse.
    "lean", under `lean=True`, brings the flat silhouettes up on a time of their own. "bare"
    is the bare land's own dry patches, there as the file opens and going over that time, so
    that a verse can open on the bare land's frame. "shoulder" keeps Eden's dry shoulder
    (SHOULDER) dust through "green" and "plants", with its own dry patches, and brings its green
    and its plants up then."""
    rng = random.Random(77)
    planted = state == "planted"
    ph = dict(plant_in or {}) if planted else {}
    shoulder = ph.get("shoulder")
    defs = land_defs(state, wet, bool(shoulder)) + plant_defs(state, thorns_too)
    if planted:
        for k, (fn, paint) in SPECIES.items():
            defs += f'<g id="{k}">' + render(fn(), paint) + "</g>"
        defs += '<g id="fn">' + render(fig(close=True), FIG_PAINT, whole=WHOLE_LEAVES) + "</g>"
        defs += '<g id="LF">' + render(tree_of_life(), LIFE_PAINT) + "</g>"
        defs += ('<g id="KN">' + render(tree_of_knowledge(), KNOWLEDGE_PAINT, whole=WHOLE_LEAVES)
                 + "</g>")
        defs += '<g id="kf">' + render(knowledge_fruit(.82), FRUIT_PAINT, prec=1) + "</g>"
        for gid, kind in (("Fd", "dome"), ("Fb", "broken"), ("Fc", "column"),
                          ("Fp", "palm")):
            defs += far_tree_def(gid, kind, 7)

    def faded(svg, phase):
        """Wrap a run of things so that it comes up with its phase: the plants on the dry
        shoulder with the shoulder's, when it has one."""
        if not svg or phase not in ph:
            return svg
        runs = [(svg, ph[phase])]
        if phase == "plants" and shoulder:
            west, east = _west_of(svg, ON_SHOULDER)
            runs = [(east, ph[phase]), (west, shoulder)]
        return "".join(f'<g opacity="0">{_fade_in(*t)}{run}</g>' for run, t in runs if run)

    def bare(layer):
        """The bare land's dry patches in this layer, going over with "bare", and those on the
        shoulder with it."""
        if "bare" not in ph:
            return ""
        on = [shoulder is not None and x < ON_SHOULDER for x, _u in bare_patches[layer]]
        west = "".join(u for (_x, u), w in zip(bare_patches[layer], on) if w)
        east = "".join(u for (_x, u), w in zip(bare_patches[layer], on) if not w)
        return "".join(f'<g>{_fade_out(*t)}{run}</g>'
                       for run, t in ((east, ph["bare"]), (west, shoulder)) if run)
    green = ph.get("green")
    bare_patches = bare_scrub() if "bare" in ph else {}
    if bare_patches:
        defs += bare_patch_def()

    stand = sorted(forest(), key=lambda t: -t[2]) if planted else []
    z1, z2, z2b, z3, zl = "", "", "", "", ""
    FAR = {"s": "Fd", "o": "Fb", "f": "Fd", "g": "Fb", "p": "Fp", "c": "Fc"}
    unplanted = "trees" in ph and ph["trees"] is None
    tb, td = ph.get("trees") or (0, 1)
    for sp, x, d, k in stand:
        y = land_y(x, d)
        sc = depth_scale(d) * k
        if d > 1150:
            z1 += _use(FAR[sp], x, y, sc, rng.random() < .5)
        elif d > 760:
            z2 += _use(FAR[sp], x, y, sc, rng.random() < .5)
        elif lean and d > 140:
            zl += _use(FAR[sp], x, y, sc, rng.random() < .5)
        else:
            flip = d > 300 and rng.random() < .4    # a near tree keeps the light on its west
            if ph:          # they come up in a wave, from the water outward
                wave = min(1.0, abs(x - 300) / 2600)
                u = _grow_use(sp, x, y, sc, flip, tb + wave * td * .6, td * .4)
            else:
                u = _use(sp, x, y, sc, flip)
            if d > 300:
                z2b += u
            else:
                z3 += u

    if unplanted:           # placed all the same: the random stream is what places the rest
        z1 = z2 = z2b = z3 = zl = ""

    # the plants between the trees, thick where the garden is
    p2, p3 = "", ""
    for px, pd in _plant_spots(rng, planted, lean):
        if not planted:
            u = _bare_use("db", px, land_y(px, pd), depth_scale(pd), rng.random() < .5)
        else:
            den = garden_density(px, pd)
            r = rng.random()
            if den < .08 or r > den + .05:
                if r >= .5:
                    continue
                u = _use("da" if r < .25 else "db", px, land_y(px, pd), depth_scale(pd))
            else:
                # where the pair stand, the ground behind them stays low and quiet
                quiet = QUIET_X[0] < px < QUIET_X[1] and pd < QUIET_D
                kind = "lo" if quiet else rng.choice(("ma", "mb", "mc", "ma", "sa"))
                u = _use(kind, px, land_y(px, pd), depth_scale(pd) * rng.uniform(.85, 1.1),
                         rng.random() < .5)
        if pd > 360:
            p2 += u
        else:
            p3 += u

    rocks = {"z2": "", "z3": "", "n": ""}
    for gid, x, d, k in ROCKS:
        u = _use(gid, x, land_y(x, d), min(depth_scale(d) * k, 1.9))
        rocks["z2" if d > 520 else "z3" if d > 0 else "n"] += u

    if river is not None:
        r = river
    else:
        r = river_svg(flow, flow_reaches) if planted else dry_course_svg()

    cw = CARD_X[1] - CARD_X[0]

    # the air is in the colours: see HAZE_FAR
    far_air, mid_air = (HAZE_FAR, HAZE_MID), (HAZE_MID,)
    greens = dict(green=green, wet=wet, shoulder=shoulder)
    behind = sky_svg() + hills_svg()
    for i in (0, 1, 2):
        behind += _hazed(bank_svg(state, False, i, **greens), *far_air)
    behind += _hazed(r["far"], *far_air)
    if z1:
        behind += faded(_hazed(f'<g fill="#3a4a46" color="#4a5c50">{z1}</g>', *far_air), "trees")
    for i in (3, 4):
        behind += _hazed(bank_svg(state, False, i, **greens), *mid_air)
    for x, d, w, h, sheet in SWELLS_FAR:
        behind += _hazed(swell_svg(state, x, d, w, h, sheet, **greens), *mid_air)
    behind += _hazed(r["mid"], *mid_air) + rocks["z2"]
    if z2:
        behind += faded(_hazed(f'<g fill="#28402f" color="#3e5a3e">{z2}</g>', *mid_air), "trees")
    behind += bare("far") + faded(p2, "plants") + z2b
    if zl:
        lean_in = f' opacity="0">{_fade_in(*ph["lean"])}' if "lean" in ph else ">"
        behind += f'<g fill="#21392b" color="#42603e"{lean_in}{zl}</g>'
    behind += bank_svg(state, False, 5, **greens)
    behind += way_svg(state, green) + rocks["z3"] + bare("stage") + z3 + faded(p3, "plants")
    if planted and heroes:
        behind += heroes_svg()

    front = ""
    if planted and not lean:
        front += faded(_stage_patches(rng, lambda x: ground_y(x) + 30, ("lo",),
                                      -1800, 1800, 460, 1.0), "plants")
    front += r["near"]
    front += _use("rb", PARTING[0] + 60, project(PARTING[1] - 6), .62)
    if planted:
        front += faded(_use("re", PARTING[0] + 16, project(PARTING[1] - 20), 1.05), "plants")
    front += bank_svg(state, True, 0, **greens)
    for x, d, w, h, sheet in SWELLS_NEAR:
        front += swell_svg(state, x, d, w, h, sheet, near=True, **greens)
    if planted:
        # along the lip of the water
        front += faded(_stage_patches(rng, lambda x: near_bank_y(0, x) + 16,
                                      ("ma", "lo", "re", "mc", "mb"), -2100, 2000,
                                      900 if lean else 480, 1.25), "plants")
        # and in drifts over the near ground, thinning at the edges
        drift = ""
        for _ in range(7 if lean else 15):
            px = rng.uniform(-2400, 2300)
            lip = _near_lip(px)
            pd = rng.uniform(max(lip - 340, -770), lip - 50)
            if pd < -780:
                continue
            if rng.random() > garden_density(px, max(pd, -300)) + .1:
                continue
            k = min(depth_scale(pd) * .8, 2.3)
            drift += _use(rng.choice(("ma", "mb", "mc", "lo")), px, project(pd), k,
                          rng.random() < .5)
        front += faded(drift, "plants")
    # the land past the water's reach, stones and scrub: everywhere if nothing
    # is planted, at the two ends if something is
    for kind, px, pd, flip in _scrub_spots(rng, planted, lean):
        front += (_use if planted else _bare_use)(kind, px, project(pd), min(depth_scale(pd), 2.3),
                                                  flip)
    front += bare("front") + rocks["n"]
    if planted and not unplanted:
        # trees on this side of the water, on the viewer's side of the garden,
        # standing low in the frame so they never cross the people's line
        for sp, x, y, k in NEAR_TREES:
            if lean and sp in ("g", "f"):
                continue
            front += (_grow_use(sp, x, y, k, False, tb + td * .5, td * .4) if ph
                      else _use(sp, x, y, k))
    front += (f'<rect x="{CARD_X[0]}" y="1760" width="{cw}" height="{Y_END - 1760:g}" '
              'fill="url(#gvig)"/>')

    outside = thorn_land_svg(defs) if thorns_too else ""
    # the named trees' drawings and the things a stager is likely to place stay in defs
    calls = '' if not planted else 'href="#LF"href="#KN"href="#kf"href="#fn"href="#sa"'
    return Scene(_prune(defs, behind + front + outside + calls), _rounded(behind), _rounded(front),
                 _rounded(outside) if outside else "",
                 dict(land_ramps(wet), **(land_ramps(wet, True) if shoulder else {}))
                 if planted else None)


def thorn_land_svg(defs):
    """Thorns and thistles (3:18) as a place: thickets over the land beyond the
    garden, east of the last trees, in a <g> of their own so a stager can bring them
    up at their verse. A thicket is a clump of plants at depths of their own, and one
    that would have any of them stand in the river is left out: each keeps 2 px north
    of it (`water_top`, by the drawings' boxes in `defs`).

    Call: you rarely need to: `panorama(thorns_too=True)` puts it in Scene.outside. Bring it
    up at 3:18 with `<g opacity="0"><animate .../>...</g>`. It needs those defs."""
    boxes = _drawing_boxes(defs)
    rng = random.Random(55)
    x0 = 2340
    out = ""
    d = 460.0
    while d > -110:
        dx = 300 + d * .4
        x = x0
        while x < X1:
            px = x + rng.uniform(-dx * .4, dx * .4)
            x += dx
            if rng.random() < .3:
                continue
            pd = d + rng.uniform(-30, 30)
            gid, k, flip = rng.choice(("ta", "tb")), depth_scale(pd) * rng.uniform(.9, 1.2), rng.random() < .5
            y, b = project(pd), boxes[gid]
            top = water_top(px - b[2] * k, px - b[0] * k) if flip else water_top(px + b[0] * k, px + b[2] * k)
            if top is None or y + b[3] * k < top - 2:
                out += _use(gid, px, y, k, flip)
        d -= 70 + (d + 110) * .22
    return f"<g>{out}</g>"


@functools.lru_cache(maxsize=None)
def _river_edges():
    """Both edges of every run of the river in the side view, card px."""
    return [e for run in [_MAIN] + list(_HEADS.values()) for e in _ribbon_points(_cut_side(run))]


def water_top(x0, x1):
    """How high any run of the river's band comes in the side view over x0..x1, card y: what
    stands there keeps north of it, above this. None where there is no water."""
    ys = []
    for edge in _river_edges():
        for (ax, ay), (bx, by) in zip(edge, edge[1:]):
            if max(ax, bx) < x0 or min(ax, bx) > x1:
                continue
            for x in (max(min(ax, bx), x0), min(max(ax, bx), x1)):
                ys.append(ay + (by - ay) * (x - ax) / ((bx - ax) or 1))
    return min(ys) if ys else None


def knowledge_reach():
    """World px of the fruit a hand can reach, west side first (toward where the
    people stand between the two trees), as (index, x, y, stem height above the
    ground). Pass an index to `heroes_svg(taken=...)` once it has been taken.

    Call: `i, x, y, h = knowledge_reach()[0]` is the one taken at 3:6, TAKE_FRUIT."""
    kx, ky = KNOW_X, project(KNOW_D)
    spots = knowledge_fruit_spots()
    out = []
    for i in (3, 4, 5, 0, 1, 2):
        fx, fy = spots[i]
        out.append((i, kx + fx * PXU, ky - fy * PXU, fy * PXU))
    return out


def heroes_svg(taken=(), grow=None):
    """The two named trees where they stand, each fruit its own <use>, as
    `panorama(heroes=False)` leaves them for a stager to place at the end of `behind`.
    `taken` is the indexes no longer on the tree (3:6; see `knowledge_reach`). `grow` makes
    them rise on their words (2:9): {"life": (b, d), "knowledge": (b, d), "fruit": (b, d)}.
    They need `panorama`'s defs, which carry them, and a trim keeps them if they
    are in range. The verse after 3:6:

        sc = panorama("planted", heroes=False).trimmed((-700, 1000, 600, 1600))
        sc.behind += heroes_svg(taken=(TAKE_FRUIT,))"""
    kx, ky = KNOW_X, project(KNOW_D)
    if grow:
        out = _grow_use("LF", LIFE_X, project(LIFE_D), 1.0, False, *grow["life"])
        out += _grow_use("KN", kx, ky, 1.0, False, *grow["knowledge"])
        return out + f'<g opacity="0">{_fade_in(*grow["fruit"])}{_knowledge_fruit(taken)}</g>'
    return _use("LF", LIFE_X, project(LIFE_D)) + knowledge_svg(taken)


def _knowledge_fruit(taken=()):
    kx, ky = KNOW_X, project(KNOW_D)
    return "".join(_use("kf", kx + fx * PXU, ky - fy * PXU)
                   for i, (fx, fy) in enumerate(knowledge_fruit_spots()) if i not in taken)


def knowledge_svg(taken=()):
    """The tree of knowledge where it stands, with its fruit."""
    return _use("KN", KNOW_X, project(KNOW_D)) + _knowledge_fruit(taken)


def dry_course_svg():
    """The river's course before there is a river (2:5): the same hollow, dry.
    Same ribbon, a bed of paler gravel, a cut bank, no water.

    Call: `panorama("barren")` draws it. By hand it returns {"far", "mid", "near": svg}, like `river_svg`."""
    out = {"far": "", "mid": "", "near": ""}
    main = _cut_side(_MAIN)
    far, mid, near = [], [], []
    for q in main:
        (far if q[1] > 620 else (mid if q[1] > 40 else near)).append(q)
    if mid and far:
        mid = [far[-1]] + mid
    if near and mid:
        near = [mid[-1]] + near
    bed = (96, 84, 62)
    bed2 = (90, 78, 58)
    cut = (70, 60, 46)

    def dry(run, seed):
        left, right = _ribbon_points(run)
        rng = random.Random(seed)
        top = []
        ph, ph2 = rng.uniform(0, 7), rng.uniform(0, 7)
        for k, (x, y) in enumerate(left):
            sc = depth_scale(depth_of(max(y, HORIZON + 8)))
            v = .5 + .5 * math.sin(k * .23 + ph) * math.sin(k * .07 + ph2)
            top.append((x, y - (.6 + 7.0 * v * v) * min(sc, 2.0)))
        o = _fill(top + left[::-1], _hex(cut), curve=False)
        o += _fill(left + right[::-1], _hex(bed), curve=False)
        a = [_strand(run, -.3)[i] for i in range(len(run))]
        b = [_strand(run, .4)[i] for i in range(len(run))]
        o += _fill(a + b[::-1], _hex(bed2), curve=False)
        stones = []
        for q in run[::1]:
            for _ in range(2):
                off = rng.uniform(-.8, .8)
                x = q[0] + q[3] * q[2] * off / 2 + rng.uniform(-14, 14)
                y = project(q[1] + q[4] * q[2] * off / 2)
                L = rng.uniform(2, 6) * depth_scale(q[1])
                stones.append([(x, y), (x + L, y + rng.uniform(-.6, .6))])
        o += _strokes(stones, _hex((150, 136, 104)), 1.3, curve=False)
        return o
    out["far"] = dry(far, 2)
    out["mid"] = dry(mid, 3)
    for k, name in enumerate(("Pishon", "Gihon", "Hiddekel", "Euphrates")):
        out["near"] += dry(_cut_side(_HEADS[name]), 10 + k)
    out["near"] += dry(near, 4)
    return out


# ---------------------------------------------------------------------------
# The land signatures: things you can see (parts: y up, unit = plan px / s)
# ---------------------------------------------------------------------------

GOLD_AT = (7245, -1450)     # the heap, on Havilah's own ground, at Pishon's edge and clear of it


def gold_heap(seed=7):
    """The gold of Havilah (2:11-12): rounded irregular nuggets you could pick up, heaped on a
    gravel bar, each with a lit blob toward the west and a shaded blob away from it. "The gold
    of that land is good": it is the brightest thing on the plan. Parts in plan px, about 700
    wide; render with s=1.

    Call: `render(gold_heap(), PLAN_PAINT, s=1, curve=False)`, or `havilah()["gold"]`, where it stands."""
    r = random.Random(seed)
    P = []
    spots = [(-220, -40, 96), (-90, -90, 120), (60, -60, 136), (210, -90, 100), (300, -20, 72),
             (-30, 50, 108), (130, 70, 92), (-170, 70, 70), (260, 70, 60), (40, 150, 62)]
    for x, y, s in sorted(spots, key=lambda t: -t[1]):
        ph = r.uniform(0, 6)
        body = []
        for i in range(11):
            a = TAU * i / 11
            q = s * (.86 + .13 * math.sin(a * 2 + ph) + .08 * math.sin(a * 3 + ph * 2) + r.uniform(-.03, .03))
            body.append((x + math.cos(a) * q, y + math.sin(a) * q * .78))
        P.append(("fill", F.smooth(body, n=3), "gold"))
        lit = [(x - s * .62 + s * .34 * math.cos(a), y + s * .26 + s * .24 * math.sin(a))
               for a in [TAU * i / 7 for i in range(7)]]
        P.append(("fill", F.smooth(lit, n=3), "gold_lit"))
        sh = [(x + s * .36 + s * .34 * math.cos(a), y - s * .32 + s * .2 * math.sin(a))
              for a in [TAU * i / 7 for i in range(7)]]
        P.append(("fill", F.smooth(sh, n=3), "gold_sh"))
    return P


def nugget_outline():
    """The biggest nugget's outline, in world px, where the heap stands: for 2:12's "good"."""
    big = max((d for _k, d, m in gold_heap() if m == "gold"), key=lambda b: abs(_area(b)))
    return [(GOLD_AT[0] + x * 1.5, GOLD_AT[1] - y * 1.5) for x, y in big]


def _gravel_grains():
    """Small round grains of gold in the Pishon's gravel, all along its run through Havilah (2:11)."""
    rng = random.Random(3)
    d_ = _D(0)
    for x, d, w, nx, nd in _centre(HEADS["Pishon"][4:], 3):
        for _ in range(2):
            off = w * PLAN_K["head"] * rng.uniform(.62, 1.3) * rng.choice((-1, 1))
            d_.dot(x + nx * off + rng.uniform(-60, 60), GROUND - d - nd * off + rng.uniform(-40, 40), rng.uniform(9, 21))
    return f'<path fill="#eebe4c" d="{d_.text()}"/>'


@functools.cache
def havilah():
    """What Havilah shows on the plan (2:11-12), each piece where it stands, so that a verse can
    bring each up on its word: {"gravel", "gold", "bdellium", "onyx": svg}."""
    return {"gravel": _gravel_grains(),
            "gold": (f'<g transform="translate({GOLD_AT[0]} {GOLD_AT[1]}) scale(1.5)">'
                     + render(gold_heap(), PLAN_PAINT, s=1, curve=False) + "</g>"),
            "bdellium": (f'<g transform="translate(9560 {GROUND - 2720:.0f})">'
                         + render(bdellium_tree(), PLAN_PAINT, s=12) + "</g>"),
            "onyx": ('<g transform="translate(8040 -1330) scale(1.2)">'
                     + render(onyx_stones(), PLAN_PAINT, s=1, curve=False) + "</g>")}


def bdellium_tree(seed=33):
    """Bdellium (2:12): a resin. So a low gnarled gum tree, thorn-branched, with
    the tears of it standing pale on the bark, each one big enough to count.

    Call: `render(bdellium_tree(), PLAN_PAINT, s=12)`, on the plan at its scale."""
    rng = random.Random(seed)
    P = limbs(rng, [
        ([(-3, 0), (-6, 18), (2, 34), (-4, 50)], [13, 10, 8, 6]),
        ([(0, 26), (-22, 42), (-44, 50)], [6, 4, 2]),
        ([(1, 30), (22, 44), (46, 48)], [6, 4, 2]),
        ([(-4, 48), (-14, 68), (-30, 78)], [5, 3, 1.6]),
        ([(-4, 48), (8, 70), (26, 80)], [5, 3, 1.6]),
    ], flow=0, tick_step=40)
    for cx, cy, rx, ry in ((-44, 56, 18, 8), (46, 54, 18, 8), (-30, 84, 20, 8),
                           (26, 86, 20, 8)):
        P.append(("fill", lobed(rng, cx, cy, rx, ry, 9, .5), "gum_leaf"))
    for x, y in ((-5, 14), (5, 22), (-4, 32), (5, 42), (-14, 40), (14, 40), (-30, 50),
                 (34, 48), (-10, 62), (6, 64), (-3, 4)):
        P.append(("fill", [(x, y + 3.4), (x + 2.8, y - 1), (x + 1.2, y - 3.4),
                           (x - 1.2, y - 3.4), (x - 2.8, y - 1)], "tear"))
    return P


def onyx_stones():
    """Onyx stone (2:12): a heap of split stones showing their dark and pale bands, the
    one thing onyx is known by. Parts in plan px, about 600 wide; render with s=1.

    Call: `render(onyx_stones(), PLAN_PAINT, s=1, curve=False)`, on the plan at its scale."""
    P = []
    stones = [(-160, -40, 150, 112, .1), (110, -70, 170, 110, -.16), (-20, 70, 150, 110, .05),
              (190, 50, 112, 86, .2)]

    def turned(pts, cx, cy, a):
        ca, sa = math.cos(a), math.sin(a)
        return [(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in pts]
    for cx, cy, rx, ry, a in stones:
        o = [(rx * math.cos(k * .785 + .3) * (.9 + .16 * math.sin(k * 2.4)),
              ry * math.sin(k * .785 + .3) * (.9 + .16 * math.cos(k * 1.7))) for k in range(8)]
        P.append(("fill", turned(o, cx, cy, a), "onyx"))
        for k, t in enumerate((-.64, -.26, .1, .46)):
            xw = rx * math.sqrt(max(.1, 1 - t * t)) * .86
            yy = t * ry
            band = [(-xw, yy), (-xw * .3, yy + ry * .1), (xw * .4, yy - ry * .04), (xw, yy + ry * .06),
                    (xw, yy + ry * .15 + k), (xw * .4, yy + ry * .06), (-xw * .3, yy + ry * .2), (-xw, yy + ry * .1)]
            P.append(("fill", turned(band, cx, cy, a), "onyx_band"))
    return P


def citadel(seed=37):
    """Assyria, which the Hiddekel flows in front of (2:14): the one made thing on
    the plan. A stepped tower behind a wall with a gate, in brick, on the far
    bank. Straight cuts.

    Call: `render(citadel(), PLAN_PAINT, s=6.8)`, on the plan at its scale."""
    P = []

    def block(x0, x1, y0, y1, cren=False):
        pts = [(x0, y0), (x0, y1)]
        if cren:
            n = int((x1 - x0) / 9)
            for i in range(n):
                xa = x0 + (x1 - x0) * i / n
                xb = x0 + (x1 - x0) * (i + .5) / n
                pts += [(xa, y1 + 5), (xb, y1 + 5), (xb, y1)]
                if i < n - 1:
                    pts.append((x0 + (x1 - x0) * (i + 1) / n, y1))
        pts += [(x1, y1), (x1, y0)]
        P.append(("fill", pts, "brick"))
        shade = [(x0 + (x1 - x0) * .68, y0), (x0 + (x1 - x0) * .68, y1), (x1, y1), (x1, y0)]
        P.append(("fill", shade, "brick_deep"))
        for k in range(1, int((y1 - y0) / 8)):
            yy = y0 + k * 8
            P.append(("line", [(x0 + 2, yy), (x1 - 2, yy)], "brick_line"))
        P.append(("line", pts + [pts[0]], "brick_edge"))
    block(-26, 26, 76, 100, True)
    block(-40, 40, 52, 76)
    block(-56, 56, 30, 52)
    block(-92, 92, 0, 30, True)
    P.append(("fill", [(-10, 0), (-10, 16), (0, 24), (10, 16), (10, 0)], "gate_dark"))
    P.append(("line", [(-10, 0), (-10, 16), (0, 24), (10, 16), (10, 0)], "brick_edge"))
    return P


def acacia():
    """A flat-topped thorn tree, the mark of a dry red land: Cush (2:13)."""
    rng = random.Random(41)
    P = limbs(rng, [([(0, 0), (-2, 24), (-16, 44)], [6, 4, 2]),
                    ([(0, 18), (12, 34), (24, 46)], [4, 3, 1.6])], flow=0, tick_step=40)
    P += [("fill", lobed(rng, -18, 50, 26, 9, 12, .5), "deep"),
          ("fill", lobed(rng, 14, 54, 30, 9, 12, .5), "deep"),
          ("fill", lobed(rng, -18, 53, 20, 5, 12, .5), "mid"),
          ("fill", lobed(rng, 12, 57, 24, 5, 12, .5), "mid")]
    return P


def red_hill(w=120.0, h=46.0):
    """A bare round hill, ruled down its turned side."""
    rng = random.Random(int(w))
    top = [(-w / 2 + w * i / 8, h * math.sin(math.pi * i / 8) ** .8) for i in range(9)]
    P = [("fill", top, "hill")]
    sh = [q for q in top if q[0] > -w * .05] + [(w * .05, 0)]
    P.append(("fill", sh, "hill_deep"))
    for seg in _hatch(rng, sh, 66, 7.0):
        P.append(("line", seg, "hill_line"))
    P.append(("line", top, "hill_edge"))
    return P


def low_palm():
    """A date palm for the plan: stem and seven fronds, as an old map draws one."""
    P = [("fill", [(-2, 0), (1, 34), (3, 34), (4, 0)], "wood")]
    for a, L in ((.15, 22), (.65, 22), (1.2, 20), (1.75, 20), (2.3, 22), (2.85, 22),
                 (-.25, 18), (3.4, 18)):
        x1, y1 = L * math.cos(a), L * math.sin(a) * .72 - L * .1
        P.append(("fill", [(2, 34), (x1 * .55, 34 + y1 * .7 + 3), (x1, 34 + y1),
                           (x1 * .55, 34 + y1 * .7 - 3)], "frond"))
    return P


def reed_bed():
    """Reeds in a bed, the Euphrates' margin."""
    rng = random.Random(43)
    P = []
    for _ in range(14):
        x = rng.uniform(-40, 40)
        h = rng.uniform(16, 34)
        P.append(("line", [(x, 0), (x + rng.uniform(-3, 3), h)], "reed_line"))
        if rng.random() < .35:
            P.append(("line", [(x, h - 2), (x, h + 5)], "reed_head"))
    return P


def peak(seed=1, w=90.0, h=70.0):
    """A mountain as a plan draws one: a lit face, a ruled face. Eden's heights."""
    rng = random.Random(seed)
    apex = (rng.uniform(-w * .12, w * .12), h)
    left = (-w / 2, 0)
    right = (w / 2, 0)
    knee = (apex[0] + w * .1, h * .46)
    foot = (apex[0] + w * .04, 0)
    sh_l = (-w * .24 + rng.uniform(-3, 3), h * .52)
    sh_r = (w * .24 + rng.uniform(-3, 3), h * .42)
    outline = [left, (-w * .36, h * .2), sh_l, (apex[0] - w * .06, h * .84), apex,
               (apex[0] + w * .1, h * .72), sh_r, (w * .38, h * .14), right]
    P = [("fill", outline, "peak"),
         ("fill", [apex, (apex[0] + w * .1, h * .72), sh_r, (w * .38, h * .14), right, foot, knee],
          "peak_deep")]
    for seg in _hatch(rng, [apex, sh_r, right, foot, knee], 64, 6.0):
        P.append(("line", seg, "peak_line"))
    P.append(("line", outline, "peak_edge"))
    return P


# ---------------------------------------------------------------------------
# The plan: 2:10-14
# ---------------------------------------------------------------------------

WAY_GATE_X = (WAY_TREES[0][0] + WAY_TREES[1][0]) / 2   # the way out, between the last two trees
PLAN_K = {"main": 1.9, "head": 2.4}
# where each name hangs (for a stager, on the verse it is said): a world point by what it names,
# and how far from that point it sits on the screen, px, so that it keeps by a river's bank or a
# heap's foot at the plan's widest and at the close shots of 2:11-14 alike: (x, y, dx, dy)
PLAN_NAMES = {"Pishon": (6770, -1740, -20, -30), "Havilah": (6020, -3120, 0, 0),
              "Gihon": (8200, 70, 0, 0), "Cush": (7300, 40, -25, 6),
              "Hiddekel": (6200, 2453, 0, 14), "Assyria": (6890, 1790, 0, 0),
              "Euphrates": (8700, 4760, 0, 0), "Eden": (-4020, 700, 14, 11),
              "gold": (GOLD_AT[0], GOLD_AT[1] + 296, -8, 9), "bdellium": (9740, -1652, 47, 28),
              "onyx stone": (8037, -1553, 20, -12)}

# ridges between the four rivers: (x, d). Nothing is traced: these only say that
# the lands are different lands.
RIDGES = [[(3200, -60), (3800, 230), (4450, 700), (5400, 1340), (7200, 2050), (9800, 2700),
           (13200, 3000)],
          [(3000, -300), (4200, -200), (5900, -60), (8200, -300), (10600, -360), (13200, -560)],
          [(2900, -660), (3900, -1100), (5200, -1500), (7400, -2300), (10200, -2800), (13200, -3000)]]

LAND_TINT = {"Havilah": (124, 100, 52), "Cush": (110, 62, 46), "Assyria": (76, 80, 88),
             "Euphrates": (78, 90, 56)}

PLAN_PAINT = {
    "rock": ((84, 80, 70), (60, 56, 50), 0), "rock_lit": ((122, 116, 96), None, 0),
    "rock_deep": ((48, 46, 42), None, 0), "rock_line": (None, (150, 146, 118), 5),
    "gold": ((238, 186, 72), None, 0), "gold_lit": ((255, 226, 136), None, 0), "gold_sh": ((170, 114, 38), None, 0),
    "wood": ((96, 76, 56), None, 0), "wood_deep": ((52, 42, 34), None, 0),
    "wood_line": (None, (176, 160, 124), 4), "bark": (None, (176, 160, 124), 3),
    "grain": (None, (52, 42, 34), 3),
    "gum_leaf": ((66, 84, 54), (132, 150, 100), 3),
    "tear": ((236, 204, 138), (120, 90, 50), 2.5),
    "onyx": ((214, 208, 190), None, 0), "onyx_band": ((36, 32, 34), None, 0),
    "brick": ((148, 124, 92), None, 0), "brick_deep": ((94, 78, 60), None, 0),
    "brick_line": (None, (96, 80, 62), 3.2), "brick_edge": (None, (214, 196, 158), 5),
    "gate_dark": ((26, 22, 20), None, 0),
    "deep": ((58, 62, 36), None, 0), "mid": ((102, 104, 56), None, 0),
    "hill": ((112, 74, 54), None, 0), "hill_deep": ((74, 48, 40), None, 0),
    "hill_line": (None, (126, 84, 62), 4), "hill_edge": (None, (178, 132, 100), 5),
    "frond": ((96, 122, 58), None, 0),
    "reed_line": (None, (120, 142, 84), 5), "reed_head": (None, (106, 78, 54), 12),
    "peak": ((76, 78, 84), None, 0), "peak_deep": ((44, 46, 56), None, 0),
    "peak_line": (None, (96, 98, 108), 4.5), "peak_edge": (None, (152, 154, 156), 6.5),
}


def _plan_crown(seed, r, kind):
    """A crown seen from above: a lobed dark mass, a body and a cap pushed toward
    the light, the shaded side cut with lines; `kind` sets its habit, so the plan
    has the same trees the side view has."""
    rng = random.Random(seed)
    P = []
    if kind == "p":                         # a palm from above is a star
        n = 9
        pts = []
        for i in range(n * 2):
            a = TAU * i / (n * 2) + .2
            k = 1.0 if i % 2 == 0 else .36
            pts.append((r * k * math.cos(a), r * k * math.sin(a)))
        P.append(("fill", pts, "cdeep"))
        pts2 = [(x * .62 - r * .1, y * .62 + r * .12) for x, y in pts]
        P.append(("fill", pts2, "cmid"))
        return P
    if kind == "c":                         # a cypress from above is a small tight round
        P.append(("fill", lobed(rng, 0, 0, r, r, r * .9, .3), "cdeep"))
        P.append(("fill", lobed(rng, -r * .2, r * .24, r * .6, r * .6, r * .7, .3), "cmid"))
        return P
    lob = r * .42 if kind == "o" else r * .34
    o = lobed(rng, 0, 0, r, r * .94, lob, .7 if kind == "o" else .55)
    P.append(("fill", o, "cdeep"))
    m = lobed(rng, LIGHT[0] * r * .16, LIGHT[1] * r * .16, r * .72, r * .68, lob, .55)
    P.append(("fill", m, "cmid"))
    sh = _shade_side(m, LIGHT[0] * r * .16, LIGHT[1] * r * .16, -130, 38)
    for seg in _hatch(rng, sh + [(-r * .05, r * .02)], 52, r * .13):
        P.append(("line", seg, "ccut"))
    P.append(("fill", lobed(rng, LIGHT[0] * r * .4, LIGHT[1] * r * .4, r * .3, r * .28, lob * .8, .5), "clit"))
    return P


_CROWN_PAINT = {
    "s": ((24, 42, 30), (54, 86, 52), (96, 132, 70)),
    "o": ((36, 50, 44), (70, 90, 72), (108, 128, 100)),
    "f": ((30, 50, 30), (70, 104, 52), (118, 146, 70)),
    "g": ((26, 46, 30), (52, 86, 50), (92, 124, 64)),
    "p": ((44, 66, 38), (92, 120, 56), (120, 140, 64)),
    "c": ((16, 32, 30), (34, 58, 50), (50, 76, 62)),
    "L": ((62, 86, 74), (122, 148, 120), (186, 204, 160)),
    "K": ((58, 30, 32), (122, 68, 48), (190, 132, 78)),
}


def _crown_defs():
    out = ""
    sizes = {"s": 250, "o": 200, "f": 210, "g": 170, "p": 170, "c": 80, "L": 300, "K": 280}
    for i, (k, r) in enumerate(sizes.items()):
        d, m, l = _CROWN_PAINT[k]
        paint = {"cdeep": (d, None, 0), "cmid": (m, None, 0), "clit": (l, None, 0),
                 "ccut": (None, d, max(4, r * .028))}
        parts = _plan_crown(900 + i, r, k)
        pts = render(parts, paint, s=1.0, prec=0)
        out += f'<g id="C{k}">{pts}</g>'
    return out


def _plan_forest():
    """Every crown on the plan: the side view's own trees where they stand, then
    the rest of the garden, which goes on south past where the side view looks
    from. Each kept off the water, and thinned by `garden_density`."""
    rng = random.Random(4321)
    crowns = [(sp, x, d) for sp, x, d, _k in forest() if garden_density(x, d) > .02
              and math.hypot(x - LIFE_X, d - LIFE_D) > 280
              and math.hypot(x - KNOW_X, d - KNOW_D) > 260]
    taken = [(x, d) for _s, x, d in crowns]

    def wet(x, d):
        for q in _MAIN:
            if abs(q[0] - x) < 240 and abs(q[1] - d) < 130 + q[2] * PLAN_K["main"] / 2:
                return True
        return False
    d = -2600.0
    while d < 2500:
        x = -2600.0
        while x < 2500:
            px = x + rng.uniform(-90, 90)
            pd = d + rng.uniform(-90, 90)
            x += 215
            den = garden_density(px, pd)
            if rng.random() > den * 1.6:
                continue
            if wet(px, pd):
                continue
            if math.hypot(px - LIFE_X, pd - LIFE_D) < 300:
                continue
            if math.hypot(px - KNOW_X, pd - KNOW_D) < 280:
                continue
            if any(abs(px - a) < 135 and abs(pd - b) < 125 for a, b in taken):
                continue
            taken.append((px, pd))
            crowns.append((_pick_species(rng, px, pd, den), px, pd))
        d += 195
    crowns = [c for c in crowns if not wet(c[1], c[2])]
    return sorted(crowns, key=lambda c: -c[2])


def _plan_ribbon(samples, k):
    """A river's two edges in the plan, (left, right), its banks wandering in width."""
    left, right = [], []
    for i, (x, d, w, nx, nd) in enumerate(samples):
        v = 1 + .13 * math.sin(i * .37 + 1.1) + .08 * math.sin(i * .11 + .4)
        v2 = 1 + .1 * math.sin(i * .29 + 2.7) + .09 * math.sin(i * .17)
        left.append((x + nx * w * k * v / 2, GROUND - d - nd * w * k * v / 2))
        right.append((x - nx * w * k * v2 / 2, GROUND - d + nd * w * k * v2 / 2))
    return left, right


def _plan_strands(samples, k, flow):
    """A river's slivers on the plan, for the verse that runs it, coming and going with the verse:
    the next verse's plan has none on this head. A head whose verse this isn't has none."""
    if not flow:
        return ""
    rng = random.Random(len(samples))
    anim = _sliver_anim(flow, 240.0)
    out = ""
    for j, (o, wander, dsh) in enumerate(SLIVER_OFF):
        ph, f = rng.uniform(0, 7), rng.uniform(.1, .2)
        run = [(x + nx * w * k * (o + wander * math.sin(i * f + ph)) / 2,
                GROUND - d - nd * w * k * (o + wander * math.sin(i * f + ph)) / 2)
               for i, (x, d, w, nx, nd) in enumerate(samples)]
        d_ = _D(0)
        d_.open_curve(run[j * 3:])
        out += _taper_layers(d_.text(), tuple(v * 3 for v in dsh), 6.0, anim, _hex(SLIVER), .8)
    return (f'<g opacity="0"><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.08;.9;1" '
            f'begin="{flow[0]:g}s" dur="{flow[1]:g}s" fill="freeze"/>{out}</g>')


_HEAD_PTS = {n: [(x, GROUND - d, w) for x, d, w in run] for n, run in HEADS.items()}


def _clear_of_heads(x, y, margin, tall=0.0, half_w=0.0):
    """The (x, y) a tree must stand at to be clear of every head of the river by `margin`, pushed
    north or south, the way it's nearest: its foot at (x, y), its crown up to `tall` above that and
    `half_w` to either side. The river is drawn over the lands, so a crown under it would read as
    a trunk growing out of the bank."""
    n = max(1, math.ceil(half_w / 40))
    for _ in range(6):
        hit = None
        for run in _HEAD_PTS.values():
            for (ax, ay, aw), (bx, by, bw) in zip(run, run[1:]):
                for sx in (x + half_w * i / n for i in range(-n, n + 1)):
                    if min(ax, bx) - 40 <= sx <= max(ax, bx) + 40:
                        u = max(0.0, min(1.0, (sx - ax) / ((bx - ax) or 1)))
                        cy = ay + (by - ay) * u
                        half = (aw + (bw - aw) * u) * PLAN_K["head"] / 2 + margin
                        if y - tall < cy + half and y > cy - half:
                            hit = (cy, half)
        if not hit:
            return x, y
        cy, half = hit
        y = cy + half + tall + 8 if y - tall / 2 >= cy else cy - half - 8
    return x, y


ACACIA_S = 7                # the plan's acacia drawing, world px a unit at size 1


def acacia_at(x, d, k):
    """Where Cush's acacia (x, d, size k) stands on the plan, crown and all clear of the heads."""
    x0, x1, _y0, y1 = F.bbox((acacia(), 0))
    return _clear_of_heads(x, GROUND - d, 150, y1 * ACACIA_S * k,
                           max(-x0, x1) * ACACIA_S * k)


# What stands on the lands the heads run through: (x, d, size).
CUSH_HILLS =((6060, 1720, 1.07), (7900, 1990, 1.05), (9700, 2060, 1.13), (10900, 1980, 1.11),
              (9300, 240, 1.17), (11200, 120, 1.18))
CUSH_ACACIAS = ((5200, 960, .96), (6050, 1160, .87), (6880, 1400, 1.05),
                (7760, 1540, .87), (8800, 1760, .98), (4900, 620, .92), (6250, 280, 1.0),
                (7500, 240, 1.09), (8700, 330, .87), (9900, 730, .98), (10700, 1340, .96),
                (11300, 500, .88))
EUPHRATES_PALMS = ((3380, -1560, 1.23), (4050, -2100, .94), (4620, -2400, 1.0), (5000, -1660, .97),
                   (5100, -3050, 1.13), (5960, -2360, .96), (6260, -3460, 1.15), (7300, -2860, 1.09),
                   (7620, -4230, .97), (8700, -3360, 1.19), (9500, -4800, 1.15), (10400, -3760, 1.17),
                   (11600, -4060, 1.24), (3000, -1320, 1.04))
EUPHRATES_REEDS = ((3320, -1280, 1.3), (3820, -1820, .97), (4380, -1500, 1.01), (5200, -2520, 1.18),
                   (5720, -2520, 1.17), (6420, -2780, .99), (7100, -3640, 1.27), (7700, -3400, .96),
                   (8700, -4260, 1.17), (9500, -3880, 1.26), (10500, -4300, 1.08), (11300, -4580, .92))


# the rest of each head, past the panorama's edge, to the plan's own edge
HEAD_ENDS = {"Pishon": [(12900, 4700, 104)], "Gihon": [(12900, 1500, 104)],
             "Hiddekel": [(12900, -2000, 104)], "Euphrates": [(12900, -5000, 170)]}


def plan_svg(flow=None):
    """The high pictorial plan of 2:10-14, in world px on the same x as the side view: x as
    it is, north up, the people's line on y = GROUND, so that a point (x, d) of the garden
    lies at (x, GROUND - d), and the side view hangs in it at no transform at all. Returns
    {"defs", "land", "garden", "river", "heads": {name: svg}, "named", "lands": {name: svg}, "fields"},
    so a stager can bring each head and each land up when its verse says it; "lands" has
    Cush, Assyria and the Euphrates' land, "fields" has Assyria's alone, without its tower, and
    `havilah()` has Havilah's, which come up one by one. Drawn from nothing but the text: there is no coast in it and no line taken from
    any map: one river out of Eden's heights, through a garden, parting into four over four
    different lands.

    Call: `p = plan_svg()`, then in paint order, `_rounded` round it: p["land"], the lands
    already said, p["garden"], p["river"], the heads, p["named"], with p["defs"] in <defs>;
    `hang_in_plan` hangs the side view in it. `flow=(begin, dur)` runs each head's water for
    that long, its slivers coming and going with it: a head with no flow has none."""
    rng = random.Random(2020)
    defs = _crown_defs()

    def stamp(gid, parts, s, paint=PLAN_PAINT):
        return f'<g id="{gid}">' + render(parts, paint, s=s, prec=0) + "</g>"
    defs += stamp("pk1", _in_order(peak(1, 90, 74), ("peak", "peak_deep", "peak_line", "peak_edge")), 11)
    defs += stamp("pk2", _in_order(peak(2, 70, 50), ("peak", "peak_deep", "peak_line", "peak_edge")), 11)
    neutral = dict(PLAN_PAINT, hill=((96, 86, 64), None, 0), hill_deep=((62, 56, 46), None, 0),
                   hill_line=(None, (112, 102, 78), 4), hill_edge=(None, (150, 140, 110), 5))
    defs += stamp("hl", red_hill(90, 30), 7, neutral)
    defs += stamp("hr", red_hill(120, 46), 8)
    defs += stamp("ac", acacia(), ACACIA_S)
    defs += stamp("pm", low_palm(), 12)
    defs += stamp("rd", reed_bed(), 11)

    # the ground, and the lands
    x0, x1, top, bot = -7200, 13400, -5200, 8000
    land = f'<rect x="{x0}" y="{top}" width="{x1 - x0}" height="{bot - top}" fill="#4a483c"/>'
    r1, r2, r3 = RIDGES
    # the Hiddekel "flows in front of Assyria": Assyria is its north bank alone, from the ridge to
    # the middle of its water, which is drawn over the edge
    hiddekel = [(x, d) for x, d, *_w in _centre(HEADS["Hiddekel"] + HEAD_ENDS["Hiddekel"], 3)
                if x >= r2[0][0]]
    wedge = {
        "Havilah": r1 + [(13400, 8000), (2500, 8000), (2500, 900)],
        "Cush": r1[::-1] + r2,
        "Assyria": r2[::-1] + hiddekel,
        "Euphrates": r3[::-1] + [(2400, -5200), (13400, -5200)],
    }
    lands = {}
    for name, poly in wedge.items():
        pts = [(x, GROUND - d) for x, d in poly]
        gid = "gl" + name[0]
        defs += (f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="2520" y1="0" '
                 f'x2="5000" y2="0"><stop offset="0" stop-color="{_hex(LAND_TINT[name])}" '
                 f'stop-opacity="0"/><stop offset="1" stop-color="{_hex(LAND_TINT[name])}"/>'
                 '</linearGradient>')
        lands[name] = _fill(pts, f"url(#{gid})", curve=False)
    # the engraver's lines over everything: long, dashed, and running with the land
    runs = []
    for k in range(26):
        y = top + 200 + k * 500
        run = []
        for j in range(16):
            x = x0 + j * 1400
            run.append((x, y + _wave(x + k * 700, 500 + k, 240, 3600)))
        runs.append(run)
    land += "".join(lands.values())
    for cx, cy, rx, ry, c in ((-2600, 3900, 1900, 620, "#524f41"), (1100, 4700, 2000, 700, "#504d40"),
                              (-3000, -600, 900, 700, "#524f41"), (1900, -1500, 1300, 420, "#46443a"),
                              (-900, -2600, 1500, 520, "#504d40"), (2300, 3000, 900, 440, "#524f41")):
        land += _fill(lobed(rng, cx, cy, rx, ry, rx * .4, .3), c, curve=True)
    land += _strokes(runs, "#d8d0a0", 9, extra=' stroke-opacity=".12" stroke-dasharray="520 260 180 340 900 420 140 300"')

    # the ridges, as lines of low hills
    hills = ""
    for r in RIDGES:
        pts = F.smooth(r, closed=False, n=5)
        for q in pts[1:]:
            if rng.random() < .25:
                continue
            hills += _use("hl", q[0] + rng.uniform(-90, 90), GROUND - q[1] + rng.uniform(-70, 70),
                          rng.uniform(.8, 1.15))
    land += hills
    # Eden's heights in the west
    pk = ""
    spots = []
    for _ in range(90):
        x, d = rng.uniform(-7200, -3300), rng.uniform(-3600, 5000)
        if abs(d - (1250 + (x + 5300) * .0)) < 420 and x < -3900:
            continue
        if x > -3900 - abs(d - 1500) * .22:
            continue
        if any(abs(x - a) < 620 and abs(d - b) < 500 for a, b in spots):
            continue
        spots.append((x, d))
    for x, d in sorted(spots, key=lambda q: -q[1]):
        pk += _use("pk1" if rng.random() < .6 else "pk2", x, GROUND - d, rng.uniform(.85, 1.2))
    land += pk

    # the garden: its ground, then its crowns
    edge = [(x, GROUND - d) for x, d in GARDEN_EDGE]
    garden = _fill(edge, "#54764a", curve=True)
    # the worn way out: from the middle of the garden, east along the people's line
    garden += _strokes([[(LIFE_X + 200, GROUND + 40), (KNOW_X + 400, GROUND + 60), (1500, GROUND + 50),
                         (WAY_GATE_X, GROUND - 10), (2880, GROUND - 24)]],
                       "#a39067", 24, curve=True, extra=' stroke-opacity=".7"')
    crowns = ""
    for sp, x, d in _plan_forest():
        crowns += _use("C" + sp, x, GROUND - d)
    garden += crowns

    # the river
    river = ""
    k = PLAN_K["main"]
    main = _centre(RIVER, 3)
    left, right = _plan_ribbon(main, k)
    river += _fill(left + right[::-1], _hex(WATER), "#2f4038", 7, curve=True)
    a = [(x + nx * w * k * .34 / 2, GROUND - d - nd * w * k * .34 / 2) for x, d, w, nx, nd in main]
    b = [(x - nx * w * k * .46 / 2, GROUND - d + nd * w * k * .46 / 2) for x, d, w, nx, nd in main]
    river += _fill(a + b[::-1], _hex(WATER_DEEP), curve=True)
    river += _plan_strands(main, k, flow)

    heads = {}
    k = PLAN_K["head"]
    for name, run in HEADS.items():
        pts = [q for q in run] + HEAD_ENDS[name]
        sm = _centre(pts, 3)
        left, right = _plan_ribbon(sm, k)
        s_ = _fill(left + right[::-1], _hex(WATER), "#2f4038", 7, curve=True)
        a = [(x + nx * w * k * .34 / 2, GROUND - d - nd * w * k * .34 / 2) for x, d, w, nx, nd in sm]
        b = [(x - nx * w * k * .46 / 2, GROUND - d + nd * w * k * .46 / 2) for x, d, w, nx, nd in sm]
        s_ += _fill(a + b[::-1], _hex(WATER_DEEP), curve=True)
        s_ += _plan_strands(sm, k, flow)
        heads[name] = s_

    # the named trees over the river's level
    crown_lf = _use("CL", LIFE_X, GROUND - LIFE_D)
    crown_kn = _use("CK", KNOW_X, GROUND - KNOW_D)
    pips = ""
    for i in range(16):
        a = rng.uniform(0, TAU)
        r = 250 * math.sqrt(rng.uniform(.05, 1))
        pips += f"M{KNOW_X + r * math.cos(a):.0f} {GROUND - KNOW_D + r * math.sin(a) * .9:.0f}h.001"
    pips_svg = f'<path fill="none" stroke="#f6b24c" stroke-width="44" d="{pips}"/>'
    named = crown_lf + crown_kn + pips_svg

    # the land signatures, each of them where it stands and how big
    def at(gid, x, y, k):
        return f'<use href="#{gid}" transform="translate({x:.0f} {y:.0f})scale({k:.2f})"/>'
    sig = {}
    sig["Cush"] = ("".join(at("hr", x, GROUND - d, k) for x, d, k in CUSH_HILLS)
                   + "".join(at("ac", *acacia_at(x, d, k), k) for x, d, k in CUSH_ACACIAS))
    fields = []
    for fx, fd in ((3950, -320), (4400, -320), (7500, -520), (8000, -560), (9300, -700)):
        for j in range(5):
            fields.append([(fx, GROUND - fd + j * 60), (fx + 360, GROUND - fd + j * 60 - 18)])
    fields = _strokes(fields, "#c4b894", 10, curve=False)
    sig["Assyria"] = (f'<g transform="translate(5700 {GROUND + 570:.0f})">' + render(citadel(), PLAN_PAINT, s=6.8) + "</g>" + fields)
    sig["Euphrates"] = ("".join(at("pm", x, GROUND - d, k) for x, d, k in EUPHRATES_PALMS)
                        + "".join(at("rd", x, GROUND - d, k) for x, d, k in EUPHRATES_REEDS))
    named += _use("pk1", -5380, GROUND - 1020, 1.5)
    named += _use("pk2", -5000, GROUND - 860, 1.2)
    return {"defs": defs, "land": land, "garden": garden, "river": river, "heads": heads,
            "named": named, "lands": sig, "fields": fields}


# ---------------------------------------------------------------------------
# The card the cast stands on
# ---------------------------------------------------------------------------





NAME_INK = (240, 228, 188)      # a name on this land, in Georgia; TEXT is too dim on the green
HL = (255, 244, 170)            # the one highlight (generate_tabernacle.HL): pulses, a name as it is said


def thing_actor(key, svg, x, y, **kw):
    """Any drawing as an Actor on a `GardenCard`, origin at (x, y), for what a hand carries:
    the fruit (3:6) is `thing_actor("fruit", fruit_macro(lw=.5), fx, fy, shown=False)`, moved with
    "move" events, and a fig the same way. "ink" and "pulse" events do nothing to it. Other
    keywords go to Actor."""
    def make(**_p):
        return []
    make.garden_svg = lambda _p, _fl, _s: svg
    return SC.Actor(key, make, x, y, **kw)


def card_kwargs():
    """The side view as a card: `svg_scene_card.Card(**card_kwargs())`. World units are card
    px (S=1) and the anchor is the world's origin, so a Flight's scale is the zoom, a camera is
    (zoom, x, y), and the plan shares every coordinate. It goes up to y -9000, for the heavens of
    2:1-4, and the page there is the same dark."""
    return {"key": "gar", "town_xy": (0, 0), "anchor": (0, 0),
            "size": (CARD_X[1] - CARD_X[0], CARD_Y[1] + 9000), "S": 1,
            "page": GARDEN_NEAR[0], "sky": SKY_TOP, "ground_y": GROUND,
            "origin": (CARD_X[0], -9000)}


class GardenCard(SC.Card):
    """A svg_scene_card.Card hosting this garden, under a Flight, with the engine's whole cast
    and event vocabulary. An actor whose maker has a `garden_svg` draws by that, once, as a symbol;
    a plain Actor still draws as the engine draws it. Each verse's scenery is passed in, because
    a verse has its own trim and its own flow."""

    def _drawing(self, a, pose, ink, flip):
        if not hasattr(a.make, "garden_svg"):
            return super()._drawing(a, pose, ink, flip)
        k = (id(a.make), tuple(sorted(pose.items())), a.h, flip)
        if k not in self._syms:
            sid = f"{self.key}{len(self._sym_defs)}"
            self._sym_defs.append(f'<g id="{sid}">' + a.make.garden_svg(pose, flip, a.h / a.unit_h) + "</g>")
            self._syms[k] = sid
        return f'<use href="#{self._syms[k]}"/>'

    def verse_svg(self, ref, fl, scene, font_px=16, label_ink=NAME_INK, pulse_ink=HL):
        """The card's group in world units for this verse: Scene.behind and Scene.outside under
        the cast, Scene.front over it, and the card's fx over that."""
        saved = self.scenery, self.fx, self.fx_after
        before = []
        for r in self.refs:
            if r == ref:
                break
            before += saved[2].get(r, [])
        self.scenery = [f"<defs>{scene.defs}</defs>{scene.behind}{scene.outside}"]
        self.fx = {ref: [scene.front] + before + saved[1].get(ref, [])}
        self.fx_after = {}
        try:
            return self.svg(ref, fl, font_px, label_ink, pulse_ink)
        finally:
            self.scenery, self.fx, self.fx_after = saved


SIDE_IN = (.09, .16)                # the zooms over which the side view dissolves over the plan


def side_op(z):
    """The side view's opacity over the plan at zoom z. While it is partly there the whole of it
    and the whole plan are both painted, through a group opacity, so it is kept short."""
    return max(0.0, min(1.0, (z - SIDE_IN[0]) / (SIDE_IN[1] - SIDE_IN[0])))


# the zooms over which the plan's garden comes in as the side view goes, under its dissolve: seen
# from above, the crowns are dark rosettes that would stand in the side view's sky
GARDEN_IN = (SIDE_IN[0], .12)


def plan_garden(fl, svg):
    """`svg`, the plan's garden or its named crowns, for a verse hung in the plan: in only where
    the side view is mostly gone (GARDEN_IN), so that the two pictures overlap on the land, the
    rivers and the lands, and not on the trees."""
    ops = [f"{max(0.0, min(1.0, (GARDEN_IN[1] - c[0]) / (GARDEN_IN[1] - GARDEN_IN[0]))):.2f}"
           for c in fl.cams]
    return f'<g opacity="{ops[0]}">{fl._anim("opacity", ops)}{svg}</g>'


def hang_in_plan(fl, plan, scene_or_card_svg):
    """The rise: the plan under, the side view (the result of a GardenCard's `verse_svg`)
    over it, faded by the camera's zoom (`side_op`), and the plan switched off while the side view
    covers it, so that a close shot pays nothing for it. The side view reaches far enough
    (CARD_X, CARD_Y) that its edge never shows. Goes inside the Flight's camera. `plan`
    is the plan's pieces with its defs in front; see `plan_svg`."""
    ops = [f"{side_op(c[0]):.2f}" for c in fl.cams]
    vis = ["visible" if float(o) < 1 else "hidden" for o in ops]
    return (f'<g visibility="{vis[0]}">{C.discrete(fl, "visibility", vis)}{plan}</g>'
            f'<g opacity="{ops[0]}">{fl._anim("opacity", ops)}{scene_or_card_svg}</g>')


# ---------------------------------------------------------------------------
# The close shots: what a camera at z 3 to z 9 is shown in place of the scenery
# ---------------------------------------------------------------------------

def _d(pts):
    """Points to a straight-sided closed path at two places, for what a camera closes on."""
    return "M" + "L".join(f"{x:.2f} {y:.2f}" for x, y in pts) + "Z"


def _thin(paint, k):
    return {m: (f, st, (w * k if w else w)) for m, (f, st, w) in paint.items()}


def fruit_macro(lw=.26):
    """The fruit for the close shots, world px, y down, the stem's top at the origin, where
    `place("kf", x, y)` puts it: the same size and the same colours as `knowledge_fruit`, round
    where that is squared, lit from the west, a small fused crown at its foot. It should look good: 3:6."""
    cy = 10.6
    rx, ry = 7.3, 7.9
    body = [(rx * math.cos(a) * (1 + .03 * math.sin(3 * a)), cy + ry * math.sin(a) * (1 + .025 * math.cos(2 * a)))
            for a in [i * TAU / 22 for i in range(22)]]
    sh = F.smooth([(1.4, cy - ry + .9), (4.6, cy - ry + 2.2), (6.6, cy - 2.6), (6.9, cy + 1.6), (5.4, cy + 5.2), (2.6, cy + ry - 1.1),
                   (4.0, cy + 3.2), (4.5, cy - .8), (3.6, cy - 4.0)], n=4)
    hi = F.smooth([(-5.0, cy - 3.2), (-3.2, cy - 5.2), (-1.0, cy - 5.8), (-.9, cy - 4.4), (-2.8, cy - 3.2), (-3.8, cy - .8),
                   (-5.0, cy - .6)], n=4)
    ticks = "".join(f'M{x0:.1f} {y0:.1f}L{x1:.1f} {y1:.1f}' for x0, y0, x1, y1 in
                    ((3.8, cy - 3.8, 6.0, cy - 3.0), (4.4, cy - 1.6, 6.7, cy - 1.0), (4.4, cy + .6, 6.8, cy + 1.0), (4.0, cy + 2.8, 6.1, cy + 3.4),
                     (3.0, cy + 4.8, 4.8, cy + 5.4)))
    crown = (f'M-3 {cy + ry - .8:.1f}Q0 {cy + ry + .2:.1f} 3 {cy + ry - .8:.1f}L3.3 {cy + ry + 1.5:.1f}L1.7 {cy + ry + .7:.1f}L0 {cy + ry + 1.8:.1f}'
             f'L-1.7 {cy + ry + .7:.1f}L-3.3 {cy + ry + 1.5:.1f}Z')
    return (f'<path d="M0 0Q.8 2.4 0 3.1" fill="none" stroke="#96825a" stroke-width=".8"/>'
            f'<path d="{_d(body)}" fill="#f6b24c" stroke="#ffecbe" stroke-width="{lw}"/>'
            f'<path d="{_d(sh)}" fill="#c6642e"/><path d="{_d(hi)}" fill="#ffe4a0"/>'
            f'<path d="{ticks}" fill="none" stroke="#803820" stroke-width="{lw}"/>'
            f'<path d="{crown}" fill="#b87a38" stroke="#6a4420" stroke-width="{lw:g}" stroke-linejoin="round"/>')


@functools.cache
def _knowledge_parts():
    return tree_of_knowledge()


def knowledge_tips(x0, x1, y0, y1):
    """The twigs and leaves at the bough's end, from the tree's own geometry, with thin lines, in
    world px, for the leaves whose stem falls within the box, each with its own midrib, and the
    twigs they grow on: so they stand exactly over the tree's own, and are drawn as it is, a leaf
    at a time, so that a leaf in front hides the ones behind it."""
    kx, ky = KNOWLEDGE_XY

    def inside(pt):
        qx, qy = pt[0] * PXU + kx, ky - pt[1] * PXU
        return x0 <= qx <= x1 and y0 <= qy <= y1
    parts = _knowledge_parts()
    twigs, leaves = [], []
    for i, (kind, data, mat) in enumerate(parts):
        if mat == "twig" and inside(data[-1]):
            twigs.append(parts[i])
        elif mat in WHOLE_LEAVES and inside(data[0]):
            leaves += parts[i:i + 2]            # the leaf, and its midrib after it
    return (f'<g transform="translate({kx} {ky:.2f})">'
            + render(twigs + leaves, _thin(KNOWLEDGE_PAINT, .3), s=PXU, prec=2, whole=WHOLE_LEAVES)
            + "</g>")


# The low bough on the tree of life (3:22): a hand can come within a finger of its fruit, and no more.
TWIG_FRUIT = (-300, LIFE_XY[1] - 146)


@functools.cache
def _twig():
    rng = random.Random(171)
    fx, fy = (TWIG_FRUIT[0] - LIFE_XY[0]) / PXU, (LIFE_XY[1] - TWIG_FRUIT[1]) / PXU
    P = limbs(rng, [([(10, 214), (46, 206), (82, 176), (fx - 2, fy + 18)], [17, 11, 7, 3])], flow=2, tick_step=16)
    P += foliage(rng, [(40, 222, 30, 16), (76, 200, 28, 16), (104, 170, 22, 13)], lobe=14, dabs=.55, contour=False)
    P += [("line", [(fx - 2, fy + 18), (fx, fy + 6)], "bark")]
    for dx, dy in ((0, 0), (9, 4), (-8, 5)):
        P.append(("dot", (fx + dx, fy + dy, 3.3), "pip"))
    paint = dict(LIFE_PAINT)
    paint["pip"] = (None, (240, 214, 130), 11)
    return f'<g transform="translate({LIFE_XY[0]} {LIFE_XY[1]})">' + render(P, paint) + "</g>"


def life_twig_svg(grow=None):
    """A real low bough of the tree of life, in its wood and its leaves and its three pale fruit,
    for 3:22's hand. It is the only one a man could ever reach, and it is drawn from 2:9 on.
    `grow=(begin, dur)` fades it in."""
    if grow:
        return f'<g opacity="0">{C.fade(grow[0], grow[1])}{_twig()}</g>'
    return _twig()


def _life_fruit(x, y, r=4.8):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="#e6d08a" stroke="#fff4c8" stroke-width=".5"/>'
            f'<path d="M{x - r * .5:.1f} {y - r * .1:.1f}A{r * .55:.1f} {r * .55:.1f} 0 0 1 {x - r * .05:.1f} {y - r * .55:.1f}" fill="none" stroke="#fffbe4" stroke-width=".7"/>')


def life_spray(macro=True):
    """The plate of the low bough at z 9, registered to TWIG_FRUIT: a long pale spray coming
    down out of the crown, its leaves and three fruit, thin-lined. `macro=False` is the same
    spray with a stem to be seen from further off."""
    x, y = TWIG_FRUIT[0] * 1.0, TWIG_FRUIT[1] * 1.0
    w = .8 if macro else 2.0
    stem = f'<path d="M{x + 80} 935C{x + 30} 1000 {x + 12} 1120 {x + 2} {y - 20}C{x + 1} {y - 12} {x} {y - 8} {x} {y - 4}" fill="none" stroke="#b8ba98" stroke-width="{w}"/>'
    leaf = ""
    for lx, ly, a, L in ((x + 6, y - 42, 200, 20), (x + 8, y - 60, -20, 22), (x + 3, y - 28, 10, 17), (x + 2, y - 14, 165, 14)):
        # a curved blade with its midrib, as the tree of knowledge's leaves are at this zoom
        d = _D(2)
        d.closed_curve(leaf_oval(0, 0, L, L * .44, 0))
        leaf += (f'<g transform="translate({lx} {ly}) rotate({a})"><path d="{d.text()}" fill="#66806a" stroke="#ced8b4" stroke-width=".4"/>'
                 f'<path d="M.8 0Q{L * .45:.1f} {-L * .03:.1f} {L * .88:.1f} 0" fill="none" stroke="#ced8b4" stroke-width=".25" stroke-opacity=".8"/></g>')
    return stem + leaf + _life_fruit(x - 4, y, 4.8) + _life_fruit(x + 5, y + 2, 4.4) + _life_fruit(x, y + 8, 4.8)


# The near fig (x, d), and its size: the tree he eats from at 2:16, and 3:7's leaves are its leaves.
FIG_NEAR = (150, 26)
FIG_K = .72
# Its three figs, on its east side. FIG_A is the one he takes: where his raised hand comes, from
# his place at x 262, facing west.
FIG_A = (234.3, 1307.1)
FIG_B = (FIG_A[0] - 30, FIG_A[1] - 20)
FIG_C = (FIG_A[0] - 12, FIG_A[1] - 44)
FIG_SVG = ('<path d="M0 -7C2.6 -5 5 -1 4.4 2.6C3.8 6 -3.8 6 -4.4 2.6C-5 -1 -2.6 -5 0 -7z" fill="#64405a" stroke="#e2d0d8" stroke-width=".8"/>'
           '<path d="M-2 -3.6Q-3.2 -.4 -2.2 2" fill="none" stroke="#9a7690" stroke-width=".7"/>')


def fig_near_svg(grow=None):
    """The near fig, where it stands, in its drawing for the close shots, `fig(close=True)`.
    `grow=(begin, dur)` raises it out of the ground. Needs the `fn` drawing in the Scene's defs:
    `trimmed(..., keep=("fn",))`."""
    x, d = FIG_NEAR
    y = land_y(x, d)
    if grow:
        return _grow_use("fn", x, y, FIG_K, False, *grow)
    return place("fn", x, y, FIG_K)


def fig_one(pt):
    """One fig, a teardrop 9 wide and 13 tall, hanging at pt."""
    return f'<g transform="translate({pt[0]:.1f} {pt[1]:.1f})">{FIG_SVG}</g>'


def figs_svg(taken=False):
    """The figs on the near fig: three, or two once he has taken FIG_A (`taken`, from 2:16)."""
    return ("" if taken else fig_one(FIG_A)) + fig_one(FIG_B) + fig_one(FIG_C)


# What they hide behind at 3:8. In Scene.front, drawn after the cast: place(*q).
SHRUBS = (("sa", 952, 1450, 1.34), ("sa", 1072, 1456, 1.3))


def shrubs_svg():
    """The shrubs, where they stand. Needs `sa` in the Scene's defs: `trimmed(..., keep=("sa",))`."""
    return "".join(place(*q) for q in SHRUBS)


# The thorns round where he digs (3:18): (id, x, how far below the people's line it stands, size). Each
# is a clump whose plants stand at depths of their own, the nearest 33 x size south of its point, and
# the river runs close along the line here, so they stand behind it: every plant of them north of
# the river's bands.
NEAR_THORNS = (("ta", 2500, -15, 1.25), ("tb", 2556, -24, 1.2), ("ta", 2714, -40, 1.3), ("tb", 2760, -35, 1.15),
               ("ta", 2820, -47, 1.3), ("tb", 2452, -2, 1.1), ("ta", 2610, -32, 1.4), ("tb", 2690, -36, 1.3))


def thorns_near(t_thorns=None, t_thistles=None):
    """The thorns close round the land outside, standing, or with the times given each rising
    from the ground on its word (3:18), the thorns on one and the thistles on the other. It
    needs `panorama(thorns_too=True)`'s defs, and `ta`, `tb` kept in a trim."""
    out = ""
    for i, (gid, x, dy, k) in enumerate(NEAR_THORNS):
        y = ground_y(x) + dy
        if t_thorns is None:
            out += place(gid, x, y, k)
        else:
            out += _grow_use(gid, x, y, k, False, (t_thorns if gid == "ta" else t_thistles) + .06 * i, 1.0)
    return out


def streak_cloud(x, y, w, h, seed, col="#2c303e", edge="#3e4352"):
    """High dry cloud (2:5): a long broken streak with torn ends, in world px, its west end at
    (x, y). It goes over, and nothing falls."""
    r = random.Random(seed)
    n = 16
    top, bot = [], []
    for i in range(n + 1):
        u = i / n
        env = math.sin(math.pi * u) ** .5
        top.append((x + w * u + r.uniform(-w * .012, w * .012), y - h * env * (.55 + .45 * abs(math.sin(u * 9 + seed))) * r.uniform(.8, 1.1)))
        bot.append((x + w * u + r.uniform(-w * .012, w * .012), y + h * .55 * env * (.4 + .6 * abs(math.sin(u * 7 + seed * 2))) * r.uniform(.7, 1.1)))
    # torn ends: fingers of it, pulled out
    east = [(x + w * 1.05, y - h * .14), (x + w * .99, y + h * .02), (x + w * 1.09, y + h * .12), (x + w * .97, y + h * .2)]
    west = [(x - w * .06, y + h * .16), (x + w * .02, y + h * .03), (x - w * .1, y - h * .1), (x + w * .03, y - h * .2)]
    return f'<path d="{_d(top + east + bot[::-1] + west)}" fill="{col}" stroke="{edge}" stroke-width="1.6" stroke-linejoin="round"/>'


# ---------------------------------------------------------------------------
# The paint of what svg_figures draws for this garden. The mound is the ground's colour; the
# sprout is green at 2:15 and dry from 3:17.
# ---------------------------------------------------------------------------

MOUND_PAINT = {"mound": ((106, 92, 68), (168, 150, 110), .4), "mound_lit": ((126, 110, 82), None, 0),
               "grain": ((168, 150, 110), None, 0)}
SPROUT_PAINT = {"stem": (None, (168, 192, 128), 1.3), "leaf": ((124, 160, 88), (200, 216, 152), .6)}
DEAD_SPROUT_PAINT = {"stem": (None, (138, 122, 80), 1.0), "leaf": ((106, 92, 56), (138, 122, 80), .5)}
SMALL_SNAKE_PAINT = {"hide": ((150, 142, 70), (50, 50, 26), .8), "rule": (None, (50, 50, 26), 1.5),
                     "muzzle": ((122, 116, 56), (50, 50, 26), .8), "hair": ((50, 50, 26), None, 0)}
# The stick is drawn twice, unrounded: its dark keyline, and over that the wood.
STICK_KEY_PAINT = {"wood": ((20, 24, 16), (20, 24, 16), 2.2)}
STICK_PAINT = {"wood": ((138, 108, 68), None, 0)}
