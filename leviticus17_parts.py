"""Leviticus 1-7 workbench: the plan strip and the bench's shared parts.

A library the sections call (leviticus17_bench has the section contract).
Every element a helper adds is owned by the section building it (bench.OWNER),
except the shared furniture `setup()` makes: the panels, the strip's plan,
the places and the altar set, which are `keep` (they outlive any section).

THE STRIP (bench.STRIP, 8, 8, 670, 222)
---------------------------------------
The reference's own draw_court, draw_tent and draw_furnishings, words
dropped and culled to one world window for the whole book: x WX0 (just west
of the veil) to the gate (strip x ~598), y about the altar's line, at PS
(0.52) strip px a world px. Past the gate a band (strip x 606-678) holds the
camp edge and the clean place, pulled in, not to scale. No clipPath.

    SP(wx, wy) -> strip px of a world (reference plan) point
    S                 named strip points and boxes: S["door"], S["veil"] (x, y0, y1),
                      S["altar"] (box), S["altar_c"], S["north"] (box), S["ashes"],
                      S["gate"] (x, y0, y1), S["camp_x"], S["clean"], S["incense"],
                      S["tent"] (box), S["road_y"] (where people stand)
    place(name, T)    a PLACE named: its mark and 13 px chip (the veil's and the
                      altar of incense's on a short leader up into the tent)
                      come in at T, once
                      for the book (keep); named again later, it pulses ("current
                      again"). Names: tent, veil, incense, door, altar, north, ashes,
                      gate, camp, clean. Returns the place's El.
    strip_chip(key, s, x, y, T, anchor="mm", out=None)   a passing 13 px chip
    token(parts, x, gy, height, did=None)                a figure at strip size (svg)
    token_el(key, parts, x, gy, height, T, did=None)     ... as an element, fading in at T
    priests_el(key, xs, T)       priest tokens standing on S["road_y"] at strip xs
    walk(el, T, path, dur, what)  a token walk (path relative to its place now)
    route(*names)                 strip points through named places (e.g.
                                  route("altar", "gate", "clean")) for a walk or a trace

No animal tokens on the strip: a beast's place is a ring or a chip with a
link pulse on the bench's beast. Priests and carried things (the carcass,
the ashes, a bread) may walk.

THE BENCH (bench.BENCH, 8, 238, 670, 330)
-----------------------------------------
The animal set: the pen (left, x 8-338) and the altar (right). The altar set
(the inset altar, its wood, its fire) is keep: shown by section 1 (body_in at
1:5, fire_in and wood_in at 1:7) and there at every later boundary.

    altar_out(T) / altar_in(T)   hide / restore the altar set (full boards)
    flare(T, k=1.3, dur=1.0)     the fire flares once
    A_BODY, A_TOP, WOOD_X, FIRE_XS, FIRE_C, BAY, slot_box(i), SLOT_Y   altar geometry
    PEN_G, PEN_BACK_G, OX_K, OX_X, RAM_K, RAM_X, BACK_K, DOVE_K, DOVE_X   pen geometry
    figure_el(key, parts, x, gy, k, T, flip=1, ink=TEXT, z=20, dur=0.6)
                                 a cast figure fading in at T (svg_figures parts)
    Beast(kind, X, G, k)         a beast and its beast_parts cutaway in one frame
                                 (kind: bull, sheep, ram, goat); .anchor[key],
                                 .outline(key), .lines(key), .polys(key), .part_svg(key)
    cutaway(beast, name, T, keys=None)      its parts fade in at T (els "cut.<name>.<key>")
    part_pulse(beast, name, key, T, group=None)  its part's outline pulses
    bench_chip(key, s, x, y, T, lead=None, out=None, how="fade", anchor="mm",
               out_group=None)   a 14 px chip on a leader; out=T it retires (in
                                 out_group, to go with another region's event)
    CHIP_BAND_Y, CHIP_BAND_X     the cutaway's chip band (three slots over the beast)
    to_wood(beast, name, srcs, T, words, dims=None, dim_to=0.35, kinds=None)
                                 the parts glide together onto the wood (one
                                 bench move, landing at T + 0.1 + dur) as slabs
                                 of their kinds (fat white, pieces, head,
                                 innards); the cutaway's parts dim
    water(beast, name, T)        water traced over the innards and legs
    burn(beast, name, T)         innards and legs dim onto the stack; a slab; flare
    Dove(at_x, ground)           a dove split into body and head (bay geometry: .DP)
    case_clear(T, extra=(), regions=("bench",), dur=0.8, group="clear", dock=False)
                                 the case's own pieces fade (everything the
                                 section owns in those regions still on, and
                                 its dock outlines with dock=True); the altar
                                 set and the places stay
    outs(els, T, dur=0.6, group=None)   fade each of els (keys, Els, arrows) still on
    not_el(key, region, xy, r, T, dur=0.7, group=None)  svg_vocab's not-mark drawn in
                                 over a forbidden thing in one stroke (the ring,
                                 then the bar); `group` ties it to its unveil
    arrow_el(key, pts, T, dur=0.5, col, width, head, region, z, group)
                                 an arrow traced along pts, its filled head in
                                 as it arrives; returns (line, head)
    set_change(outs, ins, T, dur=0.6)       a crossfade of bench sets (element keys)
    section_clear(T, dur=0.8, group=...)    everything the section owns that is still
                                 on (strip, bench, dock outlines) fades: a section's
                                 last act, so the boundary holds
"""

import math
from contextlib import contextmanager

import generate_tabernacle as GT
import generate_tabernacle_reference as R
import leviticus17_bench as B
import leviticus17_art as ART
import svg_figures as F
from generate_tabernacle import (ACACIA, PANEL, RED, SAND, SAND_DIM, SILVER, TEXT, TEXT_DIM,
                                 WHITE_LINEN)
from svg_vocab import mix

from leviticus17_bench import (El, add, f2, rgb, halo_text, tbox, chip, fig, slab,
                               LeanCanvas, pulse_el, traced_el, glide, rect_pts, ring_pts)

BLOOD = ART.BLOOD
WATER = ART.WATER
STRIP, BENCH, DOCK = B.STRIP, B.BENCH, B.DOCK

# ---------------------------------------------------------------------------
# The strip's window
# ---------------------------------------------------------------------------

PS = 0.52                                  # strip px a world px
PLAN_W = 600                               # strip px the plan takes; the band past it
WX0 = 995.0                                # just west of the veil (x 1010)
WY0 = 790.0 - (STRIP[3] / 2) / PS          # centred on the altar's line
WX1 = WX0 + PLAN_W / PS
WY1 = WY0 + STRIP[3] / PS


def SP(wx, wy):
    """World (the reference plan) -> strip px."""
    return STRIP[0] + (wx - WX0) * PS, STRIP[1] + (wy - WY0) * PS


def _box(b):
    a = SP(b[0], b[1])
    c = SP(b[2], b[3])
    return (a[0], a[1], c[0], c[1])


_inc = ART.PLAN.box(*__import__("sanctuary").plan_box("incense_altar"))
S = {
    "altar": _box(ART.ALT),
    "tent": _box((WX0, ART.TENT_R[1], ART.TENT_R[2], ART.TENT_R[3])),
    "north": _box(ART.NORTH_R),
    "door": SP(*ART.DOOR_PT),
    "veil": (SP(ART.VEIL_PT[0], 0)[0], SP(0, ART.TENT_R[1])[1], SP(0, ART.TENT_R[3])[1]),
    "ashes": SP(*ART.ASH_PT),
    "gate": (SP(ART.GATE_X, 0)[0], SP(0, 650)[1], SP(0, 930)[1]),
    "incense": SP(_inc[0] + _inc[2] / 2, _inc[1] + _inc[3] / 2),
    "road_y": SP(0, 950)[1],
    "camp_x": STRIP[0] + PLAN_W + 12,
    "clean": (STRIP[0] + PLAN_W + 44, SP(0, 800)[1]),
}
S["altar_c"] = ((S["altar"][0] + S["altar"][2]) / 2, (S["altar"][1] + S["altar"][3]) / 2)
S["gate_c"] = (S["gate"][0], (S["gate"][1] + S["gate"][2]) / 2)
S["outside"] = (S["camp_x"] + 30, S["road_y"])         # outside the gate, where Moses stands
del _inc


class StripCanvas(LeanCanvas):
    """A canvas for the reference's draw_court, draw_tent and draw_furnishings
    that drops their words (the strip has chips of its own) and culls every
    shape to the window: rects and polygons clipped, lines cut, circles kept
    whole or dropped. No clipPath."""

    def __init__(self):
        super().__init__(0.3 / PS)
        self.win = (WX0, WY0, WX1, WY1)

    @contextmanager
    def group(self, *a, **k):
        yield self

    def text(self, *a, **k):
        return

    def _inside(self, x, y, pad=0):
        x0, y0, x1, y1 = self.win
        return x0 - pad <= x <= x1 + pad and y0 - pad <= y <= y1 + pad

    def rect(self, x, y, w, h, fill=None, stroke=None, width=1, rx=None):
        x0, y0, x1, y1 = self.win
        a0, b0, a1, b1 = max(x, x0), max(y, y0), min(x + w, x1), min(y + h, y1)
        if a0 >= a1 or b0 >= b1:
            return
        if (a0, b0, a1, b1) == (x, y, x + w, y + h):
            return super().rect(x, y, w, h, fill, stroke, width, rx)
        if fill is not None:
            super().rect(a0, b0, a1 - a0, b1 - b0, fill=fill)
        if stroke is not None:
            for p, q in (((x, y), (x + w, y)), ((x + w, y), (x + w, y + h)),
                         ((x + w, y + h), (x, y + h)), ((x, y + h), (x, y))):
                self.line(p, q, stroke, width)

    def _clip_seg(self, p, q):
        x0, y0, x1, y1 = self.win
        (ax, ay), (bx, by) = p, q
        dx, dy = bx - ax, by - ay
        t0, t1 = 0.0, 1.0
        for pp, qq in ((-dx, ax - x0), (dx, x1 - ax), (-dy, ay - y0), (dy, y1 - ay)):
            if pp == 0:
                if qq < 0:
                    return None
            else:
                r = qq / pp
                if pp < 0:
                    t0 = max(t0, r)
                else:
                    t1 = min(t1, r)
        if t0 > t1:
            return None
        return (ax + t0 * dx, ay + t0 * dy), (ax + t1 * dx, ay + t1 * dy)

    def line(self, p0, p1, stroke, width=1, dash=None, linecap="butt"):
        s = self._clip_seg(p0, p1)
        if s:
            super().line(s[0], s[1], stroke, width, dash, linecap)

    def circle(self, cx, cy, r, fill=None, stroke=None, width=1):
        x0, y0, x1, y1 = self.win
        if x0 + r <= cx <= x1 - r and y0 + r <= cy <= y1 - r:
            super().circle(cx, cy, r, fill, stroke, width)

    def _sh(self, pts):
        x0, y0, x1, y1 = self.win
        for ax, v, sgn in ((0, x0, 1), (0, x1, -1), (1, y0, 1), (1, y1, -1)):
            out = []
            n = len(pts)
            for i in range(n):
                a, b = pts[i], pts[(i + 1) % n]
                ina, inb = (a[ax] - v) * sgn >= 0, (b[ax] - v) * sgn >= 0
                if ina:
                    out.append(a)
                if ina != inb:
                    t = (v - a[ax]) / (b[ax] - a[ax])
                    out.append((a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])))
            pts = out
            if not pts:
                return []
        return pts

    def polygon(self, points, fill=None, stroke=None, width=1):
        pts = list(points)
        if all(self._inside(x, y) for x, y in pts):
            return super().polygon(pts, fill, stroke, width)
        cl = self._sh(pts)
        if len(cl) > 2:
            super().polygon(cl, fill, None, width)

    def polyline(self, points, stroke, width=1, dash=None, closed=False, fill=None,
                 linejoin="round"):
        pts = list(points) + (list(points)[:1] if closed else [])
        if all(self._inside(x, y) for x, y in pts):
            return super().polyline(points, stroke, width, dash, closed, fill, linejoin)
        for a, b in zip(pts, pts[1:]):
            self.line(a, b, stroke, width, dash)


def strip_art():
    c = StripCanvas()
    R.draw_court(c)
    R.draw_tent(c)
    R.draw_furnishings(c)
    inner = "".join(c._els)
    return (f'<g transform="translate({f2(STRIP[0] - WX0 * PS)} {f2(STRIP[1] - WY0 * PS)}) '
            f'scale({PS})">{inner}</g>')


def token(parts, x, gy, height, ink_=TEXT, flip=1, did=None):
    """A figure `height` px tall standing on gy, centred on x."""
    x0, x1, y0, y1 = F.bbox((parts, 0))
    s = height / (y1 - y0)
    cx = (x0 + x1) / 2 * s * flip
    if did:
        B.define(did, fig(parts, 0, y0 * s, s, ink_, PANEL, flip=flip, tol=0.35))
        return B.use(did, x - cx, gy)
    return fig(parts, x - cx, gy + y0 * s, s, ink_, PANEL, flip=flip, tol=0.35)


def token_el(key, parts, x, gy, height, T, did=None, dur=0.6, z=30, flip=1, ink_=TEXT):
    el = add(El(key, "strip", token(parts, x, gy, height, ink_, flip, did), z=z))
    el.ev("in", T, dur)
    return el


def priests_el(key, xs, T, height=30, dur=0.6):
    """Priest tokens standing on S["road_y"] at strip xs, fading in at T."""
    el = add(El(key, "strip", "".join(token(F.priest(), x, S["road_y"], height, did="tok_priest")
                                       for x in xs), z=30))
    el.ev("in", T, dur)
    return el


def strip_chip(key, s, x, y, T, anchor="mm", dur=0.5, size=13, out=None, group=None,
               keep=False, out_group=None):
    """A passing 13 px chip with a halo; `out` retires it (in `out_group`)."""
    el = add(El(key, "strip", halo_text(s, x, y, size, TEXT, anchor), z=60, keep=keep,
                texts=[(tbox(s, x, y, size, anchor), size, "strip chip")]))
    el.ev("in", T, B.fit(T, dur), group=group)
    if out is not None:
        el.ev("out", out, B.fit(out, 0.5), group=out_group)
    return el


def walk(el, T, path, dur, what, group=None):
    """A token walk on the strip (path relative to the token's place now)."""
    return glide(el, T, path, dur, what, "token walk", group=group)


def route(*names):
    """Strip points through named places, for a walk or a trace."""
    pts = []
    for n in names:
        if n == "gate":
            pts.append(S["gate_c"])
        elif n == "altar":
            pts.append(S["altar_c"])
        elif n == "veil":
            pts.append((S["veil"][0] + 4, S["door"][1]))
        elif n in ("north",):
            b = S["north"]
            pts.append(((b[0] + b[2]) / 2, (b[1] + b[3]) / 2))
        else:
            p = S[n]
            pts.append(p if len(p) == 2 else p[:2])
    return pts


# -- the places ---------------------------------------------------------------

def _place_defs():
    a, n, t, (gx, gy0, gy1) = S["altar"], S["north"], S["tent"], S["gate"]
    vx, vy0, vy1 = S["veil"]
    cx, cy = S["clean"]
    ax, ay = S["ashes"]
    dx, dy = S["door"]
    ix, iy = S["incense"]
    return {
        "tent": dict(chip=("Tent of Meeting", (t[0] + t[2]) / 2, t[1] - 13, "mm"),
                     pulse=rect_pts(t[0] - 2, t[1] - 3, t[2] + 3, t[3] + 3)),
        "veil": dict(chip=("veil", vx + 4, t[3] + 12, "lm"), lead=(vx, t[3] - 10),
                     mark=(f'<line x1="{f2(vx)}" y1="{f2(vy0)}" x2="{f2(vx)}" y2="{f2(vy1)}" '
                           f'stroke="{rgb(B.HL)}" stroke-width="2" stroke-opacity="0.8"/>'),
                     pulse=rect_pts(vx - 3, vy0 - 2, vx + 3, vy1 + 2)),
        "incense": dict(chip=("altar of incense", ix + 2, t[3] + 30, "lm"), lead=(ix + 4, iy + 5),
                        lead_x=ix + 18,                 # clear of the veil's chip
                        pulse=ring_pts((ix, iy), 7)),
        "door": dict(chip=("door", dx + 14, dy - 2, "lm"), pulse=ring_pts((dx, dy), 10)),
        "altar": dict(chip=("altar", a[0] - 6, (a[1] + a[3]) / 2, "rm"),
                      pulse=rect_pts(a[0] - 2, a[1] - 2, a[2] + 2, a[3] + 2)),
        "north": dict(chip=("north", (n[0] + n[2]) / 2, n[1] - 10, "mm"),
                      mark=(f'<rect x="{f2(n[0])}" y="{f2(n[1])}" width="{f2(n[2] - n[0])}" '
                            f'height="{f2(n[3] - n[1])}" fill="{rgb(mix(PANEL, SAND, .35))}" '
                            f'fill-opacity="0.35" stroke="{rgb(SAND)}" stroke-width="1.2" '
                            f'stroke-dasharray="4 3"/>'),
                      pulse=rect_pts(n[0] - 2, n[1] - 2, n[2] + 2, n[3] + 2)),
        "ashes": dict(chip=("place of the ashes", ax + 4, a[3] + 13, "mm"),
                      mark=ART.heap(ax, ay + 7, 16, 8),
                      pulse=rect_pts(ax - 10, ay - 3, ax + 10, ay + 9)),
        "gate": dict(chip=("gate", gx - 8, gy1 + 12, "rm"),
                     pulse=rect_pts(gx - 4, gy0 - 2, gx + 4, gy1 + 2)),
        "camp": dict(chip=("outside the camp", STRIP[0] + STRIP[2] - 5, STRIP[1] + 16, "rm"),
                     mark=(f'<line x1="{f2(S["camp_x"])}" y1="{f2(STRIP[1] + 28)}" '
                           f'x2="{f2(S["camp_x"])}" y2="{f2(STRIP[1] + STRIP[3] - 8)}" '
                           f'stroke="{rgb(SAND_DIM)}" stroke-width="2" stroke-dasharray="7 5"/>'),
                     pulse=rect_pts(S["camp_x"] - 3, STRIP[1] + 26, S["camp_x"] + 3,
                                    STRIP[1] + STRIP[3] - 6)),
        "clean": dict(chip=("clean place", STRIP[0] + STRIP[2] - 4, cy + 26, "rm"),
                      mark=ART.heap(cx, cy + 8, 26, 11, col=mix(PANEL, SAND, .55)),
                      pulse=rect_pts(cx - 16, cy - 6, cx + 16, cy + 11)),
    }


PLACES = {}
PLACE_SHOWN = {}                # name -> T it came in


def place(name, T, dur=0.5, pulse=True, group=None):
    """The place `name` named at T: its mark and chip come in (once for the
    book, keep), or, named again, its outline pulses. Returns its El."""
    pd = PLACES[name]
    key = f"place.{name}"
    if name in PLACE_SHOWN and PLACE_SHOWN[name] < T - 1e-6:
        if pulse:
            n = sum(1 for k in B.ELS if k.startswith(key + ".p"))
            pulse_el(f"{key}.p{n}", "strip", pd["pulse"], T, group=group or key)
        return B.ELS[key]
    s, x, y, anc = pd["chip"]
    lead = ""
    if pd.get("lead"):              # a short leader from the chip up to what it names
        lx, ly = pd["lead"]
        x0, y0, x1, _y1 = tbox(s, x, y, 13, anc)
        sx = pd.get("lead_x", min(max(lx, x0 + 4), x1 - 4))
        lead = (f'<line x1="{f2(sx)}" y1="{f2(y0 - 2)}" x2="{f2(lx)}" y2="{f2(ly)}" '
                f'stroke="{rgb(TEXT_DIM)}" stroke-width="1.3"/>'
                f'<circle cx="{f2(lx)}" cy="{f2(ly)}" r="2.4" fill="{rgb(TEXT_DIM)}"/>')
    el = add(El(key, "strip", pd.get("mark", "") + lead + halo_text(s, x, y, 13, TEXT, anc), z=55,
                keep=True, texts=[(tbox(s, x, y, 13, anc), 13, "place chip")]))
    el.ev("in", T, dur, group=group or key)
    PLACE_SHOWN[name] = T
    if pulse:
        pulse_el(f"{key}.p0", "strip", pd["pulse"], T, group=group or key)
    return el


# ---------------------------------------------------------------------------
# The bench: the pen and the altar
# ---------------------------------------------------------------------------

PEN_G = 532                         # the pen's ground (front row)
PEN_BACK_G = 352                    # the back row's
OX_K, OX_X = 2.0, 128               # the ox and the bull's cutaway, facing the altar
RAM_K, RAM_X = 3.2, 150             # the flock case's ram and its cutaway
BACK_K = 1.6                        # the back row's scale
DOVE_K = 3.0
DOVE_X = (160, 306)                 # two doves in the pen
STYLE = F.parts_palette(TEXT, PANEL, RED)
CHIP_BAND_Y = BENCH[1] + 40         # the cutaway's chip band
CHIP_BAND_X = (70, 168, 268)

AK = 0.95                           # the altar inset's scale
_BODY_L = 508 - GT.AW * AK / 2
A_AT = (_BODY_L - (GT.AX - GT.IX) * AK, 552 - (GT.AY + GT.AH - GT.IY) * AK)


def _a(p):
    return ART.inset_pt(p, AK, A_AT)


A_BODY = _a((GT.AX, GT.AY)) + _a((GT.AX + GT.AW, GT.AY + GT.AH))
A_TOP = A_BODY[1]
WOOD_X = (A_BODY[0] + 16, A_BODY[2] - 66)       # the wood: the hearth's left part
FIRE_XS = [WOOD_X[0] + 14 + i * (WOOD_X[1] - WOOD_X[0] - 28) / 4 for i in range(5)]
FIRE_HS = [34, 46, 52, 44, 34]
SLOT_W, SLOT_GAP = 42, 6
SLOT_Y = (A_TOP - 50, A_TOP - 28)               # on the wood
BAY = (A_BODY[2] - 36, A_TOP)                   # the bird bay: the hearth's right end
FIRE_C = ((FIRE_XS[0] + FIRE_XS[-1]) / 2, A_TOP)
MEAT = mix(PANEL, RED, .75)
FAT = mix(PANEL, WHITE_LINEN, .85)
INN = mix(PANEL, RED, .55)


def slot_box(i):
    """The i-th slab's place on the wood (0-2)."""
    x0 = WOOD_X[0] + 6 + i * (SLOT_W + SLOT_GAP)
    return (x0, SLOT_Y[0], x0 + SLOT_W, SLOT_Y[1])


def slab_svg(kind, b):
    """A part on the wood as a slab: pieces, head, fat, inn (innards and legs)."""
    x0, y0, x1, y1 = b
    if kind == "pieces":
        return "".join(slab(x0 + k * 14.5, y0 + 4, x0 + k * 14.5 + 12.5, y1, MEAT, TEXT, 3)
                       for k in range(3))
    if kind == "head":
        return slab(x0, y0 + 2, x1, y1, mix(PANEL, RED, .6), TEXT, 7)
    if kind == "fat":
        return slab(x0, y0 + 2, x1, y1, FAT, TEXT, 7)
    return slab(x0, y0 + 6, x1, y1, INN, TEXT, 5)


ALTAR_KEYS = ("bench.altar", "bench.wood.a0", "bench.wood.a1", "bench.wood.a2",
              "bench.wood.b0", "bench.wood.b1", "bench.fire")


def _wood_bars():
    w1 = [(WOOD_X[0] + i * (WOOD_X[1] - WOOD_X[0]) / 3 + 2,
           WOOD_X[0] + (i + 1) * (WOOD_X[1] - WOOD_X[0]) / 3 - 2) for i in range(3)]
    w2 = [(a + 24, b + 24) for a, b in w1[:2]]
    return ([("a", i, a, b, A_TOP - 12, A_TOP - 1) for i, (a, b) in enumerate(w1)]
            + [("b", i, a, b, A_TOP - 24, A_TOP - 13) for i, (a, b) in enumerate(w2)])


def _altar_setup():
    add(El("bench.altar", "bench", ART.inset_svg("altar", AK, A_AT), z=10, hidden0=True,
           keep=True))
    for row, i, a, b, y0, y1 in _wood_bars():
        add(El(f"bench.wood.{row}{i}", "bench", slab(a, y0, b, y1, mix(PANEL, ACACIA, .75), ACACIA, 3),
               z=14, hidden0=True, keep=True))
    add(El("bench.fire", "bench", ART.flames(FIRE_XS, A_TOP - 2, FIRE_HS), z=12, hidden0=True,
           keep=True))


def body_in(T, dur=0.6):
    """The altar's body comes in (1:5)."""
    B.ELS["bench.altar"].ev("in", T, dur, group="altar")


def fire_in(T, dur=0.9):
    """The fire grows on the hearth (1:7)."""
    B.ELS["bench.fire"].ev("in", T, dur, how="grow", about=FIRE_C, group="fire")


def wood_in(T):
    """The wood lifts in, course by course (1:7)."""
    for row, i, *_r in _wood_bars():
        B.ELS[f"bench.wood.{row}{i}"].ev("in", T + (0.5 if row == "b" else 0) + i * 0.16, 0.4,
                                         how="lift", lift=8, group="wood")


_ALTAR_HID = {}


def altar_out(T, dur=0.6, group="set"):
    """Hide the altar set (a full board needs the whole bench)."""
    shown = [k for k in ALTAR_KEYS if B.ELS[k].state(T)[0]]
    _ALTAR_HID[T] = shown
    for k in shown:
        B.ELS[k].ev("out", T, dur, group=group)
    return shown


def altar_in(T, dur=0.6, group="set"):
    """Restore what the last altar_out before T hid."""
    last = max((t for t in _ALTAR_HID if t < T), default=None)
    if last is None:
        raise ValueError("altar_in without an altar_out before it")
    for k in _ALTAR_HID.pop(last):
        B.ELS[k].ev("in", T, dur, group=group)


def flare(T, k=1.3, dur=1.0, group=None):
    """The fire flares once."""
    B.ELS["bench.fire"].ev("flare", T, dur, about=FIRE_C, k=k, group=group)


def figure_el(key, parts, x, gy, k, T=None, flip=1, ink_=TEXT, z=20, dur=0.6, group=None,
              style=None):
    """A cast figure at bench size (x, ground gy, scale k), in at T."""
    el = add(El(key, "bench", fig(parts, x, gy, k, ink_, PANEL, flip=flip, style=style), z=z,
                hidden0=T is None))
    if T is not None:
        el.ev("in", T, dur, group=group)
    return el


class Beast:
    """A beast in the pen and its cutaway, in one frame (beast_parts is in
    the figure's own frame), facing the altar."""

    def __init__(self, kind, X, G_, k):
        self.kind, self.X, self.G, self.k = kind, X, G_, k
        self.parts, an = F.beast_parts(kind)
        self.anchor = {key: self.P(a) for key, a in an.items()}
        self.anchor["fat"] = self.anchor["fat_cover"]

    def P(self, p):
        return (self.X + p[0] * self.k, self.G - p[1] * self.k)

    def polys(self, key):
        return [[self.P(q) for q in d] for kk, d, _m in self.parts.get(key, []) if kk == "fill"]

    def lines(self, key):
        return [[self.P(q) for q in d] for kk, d, _m in self.parts.get(key, []) if kk == "line"]

    def outline(self, key):
        """[(points, closed)] to pulse a part ("fat" is every fat)."""
        if key == "fat":
            return [(p, True) for k_ in ("fat_cover", "fat_on", "kidney_fat") for p in self.polys(k_)]
        if key in ("pieces",):
            return [(p, False) for p in self.lines(key)]
        if key == "skin":
            return [(self.polys("skin")[0], True)]
        ps = self.polys(key)
        if not ps:
            return [(p, False) for p in self.lines(key)]
        if key in ("legs",):
            return [(p, True) for p in ps]
        big = max(ps, key=lambda p: (max(x for x, _ in p) - min(x for x, _ in p))
                  * (max(y for _, y in p) - min(y for _, y in p)))
        return [(big, True)]

    def part_svg(self, key):
        return fig(self.parts[key], self.X, self.G, self.k, TEXT, PANEL, style=STYLE, tol=0.35)


CUT_ORDER = [k for k in F.BEAST_PART_ORDER if k not in ("pieces",)]


def cutaway(beast, name, T, keys=None, dur=0.6, group=None):
    """The beast's parts (els "cut.<name>.<key>") fade in at T."""
    out = []
    for i, key in enumerate(CUT_ORDER):
        if key not in beast.parts or (keys and key not in keys):
            continue
        el = add(El(f"cut.{name}.{key}", "bench", beast.part_svg(key), z=24 + i * 0.01))
        el.ev("in", T, dur, group=group)
        out.append(el)
    return out


def part_pulse(beast, name, key, T, group=None, tag=""):
    """The part's outline pulses once."""
    words = {"pieces": "meat"}
    for j, (pts, cl) in enumerate(beast.outline(words.get(key, key))):
        pulse_el(f"cut.{name}.{key}.p{tag}{j}", "bench", pts, T, closed=cl, group=group or f"p{name}{key}")


def bench_chip(key, s, x, y, T, lead=None, anchor="mm", dur=0.5, size=14, out=None,
               how="fade", group=None, out_dur=0.6, out_group=None, edge=SAND_DIM):
    """A 14 px chip on a plate, with a leader to `lead`; retires at `out`
    (in `out_group`, so it can go with another region's event). Its plate
    box is `.box`."""
    svg, box = chip(s, x, y, size, anchor, lead, edge=edge)
    el = add(El(key, "bench", svg, z=60, texts=[(box, size, "bench chip")]))
    if how == "lift":
        el.ev("in", T, B.fit(T, dur), how="lift", lift=6, group=group)
    else:
        el.ev("in", T, B.fit(T, dur), group=group)
    if out is not None:
        el.ev("out", out, B.fit(out, out_dur), group=out_group)
    el.box = box
    return el


SLAB_KIND = {"pieces": "pieces", "head": "head", "fat": "fat", "tail_fat": "fat", "tail": "fat",
             "cover": "fat", "liver_cover": "fat", "kidney_fat": "fat", "fat_on": "fat",
             "fat_cover": "fat"}


def to_wood(beast, name, srcs, T, words, dur=1.0, dims=None, dim_to=0.35, kinds=None):
    """The parts lift off the cutaway and glide together onto the wood (one
    bench move, landing at T + 0.1 + dur); the cutaway's parts dim (to
    `dim_to`). srcs: {word: (x, y)}; each word becomes a slab of its kind
    (SLAB_KIND, or `kinds` {word: "pieces" | "head" | "fat" | "inn"}: fat is
    white, anything else an innards slab); `dims` {word: [part keys]} says
    which cutaway parts dim for it."""
    order = sorted(words, key=lambda w: srcs[w][0])
    kinds = {**SLAB_KIND, **(kinds or {})}
    els, Ls = [], []
    for i, word in enumerate(order):
        sb = slot_box(i)
        el = add(El(f"stack.{name}.{word}", "bench", slab_svg(kinds.get(word, "inn"), sb), z=30))
        cx, cy = (sb[0] + sb[2]) / 2, (sb[1] + sb[3]) / 2
        sx, sy = srcs[word]
        dd = (dims or {}).get(word) or {"pieces": ["meat"], "head": ["head"],
                                        "fat": ["fat_cover", "fat_on", "kidney_fat"]}.get(word, [word])
        for k_ in dd:
            if f"cut.{name}.{k_}" in B.ELS:
                B.ELS[f"cut.{name}.{k_}"].ev("dim", T, 0.6, to=dim_to, group=f"wood.{name}")
        el.off0 = (round(sx - cx, 1), round(sy - cy, 1))
        el.ev("in", T, 0.3, group=f"wood.{name}")
        Ls.append(glide(el, T + 0.1, [(0, 0), (cx - sx, cy - sy)], dur, "", "", record=False,
                        group=f"wood.{name}"))
        els.append(el)
    B.travel(T + 0.1, f"{', '.join(words)} onto the wood (together)", max(Ls), dur, "bench move",
             keys=[e.key for e in els], group=f"wood.{name}")
    return els


def water(beast, name, T):
    out = []
    ix, iy = beast.anchor["innards"]
    lx, ly = beast.anchor["legs"]
    waves = [[(ix - 34 + k * 7, iy + dy + (3 if k % 2 else -3)) for k in range(11)] for dy in (-8, 6)]
    waves += [[(lx + dx + k * 5, ly + (3 if k % 2 else -3)) for k in range(7)] for dx in (-20, 4)]
    for i, w in enumerate(waves):
        out.append(traced_el(f"water.{name}.{i}", "bench", w, WATER, 2.6, T + i * 0.15, 0.6, z=28))
    return out


def burn(beast, name, T, keys=("innards", "legs")):
    """The parts dim onto the stack; their slab lifts in on top; the fire flares."""
    for k_ in keys:
        if f"cut.{name}.{k_}" in B.ELS:
            B.ELS[f"cut.{name}.{k_}"].ev("dim", T, 0.6, to=0.35, group=f"burn.{name}")
    sb0, sb2 = slot_box(0), slot_box(2)
    top = (sb0[0] + 10, SLOT_Y[0] - 16, sb2[2] - 10, SLOT_Y[0] + 1)
    el = add(El(f"stack.{name}.inn", "bench", slab_svg("inn", top), z=30))
    el.ev("in", T, 0.5, how="lift", lift=10, group=f"burn.{name}")
    flare(T + 0.1, 1.32, 1.0, group=f"burn.{name}")
    return el


class Dove:
    """A dove (svg_figures.dove, facing the fire) split into body and head;
    DP(p) maps its own frame at the bird bay to bench px."""
    HEAD_IDX = {6, 7, 12}

    def __init__(self):
        self.parts = F.dove(descending=False)
        dx0, dx1, dy0, dy1 = F.bbox((self.parts, 0))
        self.dy0 = dy0
        self.ground = PEN_G + dy0 * DOVE_K            # its lowest point on the pen's ground
        self.body = [p for i, p in enumerate(self.parts) if i not in self.HEAD_IDX]
        self.head = [p for i, p in enumerate(self.parts) if i in self.HEAD_IDX]
        self.bay_x = BAY[0]
        self.bay_g = A_TOP - 2 + dy0 * DOVE_K

    def DP(self, p):
        return (self.bay_x - p[0] * DOVE_K, self.bay_g - p[1] * DOVE_K)

    def svg(self, which, x, flip=-1):
        parts = {"body": self.body, "head": self.head, "all": self.parts}[which]
        return fig(parts, x, self.ground, DOVE_K, SILVER, flip=flip)

    def outline(self, x, flip=-1):
        return F.outline(self.parts, x, self.ground, DOVE_K, flip=flip)


def _owned_on(T, regions, include_dock=False):
    out = []
    for k, el in B.ELS.items():
        if el.owner != B.OWNER or el.keep or el.transient:
            continue
        if el.parent and not include_dock:
            continue
        if el.region not in regions and not (el.parent and include_dock):
            continue
        if not el.state(T + 1e-6)[0]:
            continue
        if any(e["kind"] in ("out", "hide") and e["T"] >= T - 1e-6 for e in el.events):
            continue
        out.append(el)
    return out


def case_clear(T, extra=(), regions=("bench",), dur=0.8, group="clear", dock=False):
    """The case's own pieces fade: everything the section owns in `regions`
    still on at T (the altar set and the places stay), plus `extra` keys;
    dock=True (or "dock" in regions) its dock outlines too."""
    dock = dock or "dock" in regions
    els = _owned_on(T, regions, include_dock=dock) + [B.ELS[k] for k in extra]
    seen = set()
    for el in els:
        if el.key in seen:
            continue
        seen.add(el.key)
        el.ev("out", T, B.fit(T, dur), group=group)
    return [e.key for e in els]


def outs(els, T, dur=0.6, group=None):
    """Fade out each of `els` (keys, Els, or lists of them: an arrow) still
    on at T."""
    for el in els:
        if isinstance(el, (list, tuple)):
            outs(el, T, dur, group)
            continue
        el = B.ELS[el] if isinstance(el, str) else el
        if el.state(T + 1e-6)[0] and not any(
                e["kind"] in ("out", "hide") and e["T"] >= T - 1e-6 for e in el.events):
            el.ev("out", T, B.fit(T, dur), group=group)


def section_clear(T, dur=0.8, group="clear"):
    """Everything the section owns that is still on (strip, bench, the
    dock's outlines) fades: a section's last act, so the boundary holds."""
    els = _owned_on(T, ("strip", "bench", "dock"), include_dock=True)
    for el in els:
        el.ev("out", T, B.fit(T, dur), group=group)
    return [e.key for e in els]


def not_el(key, region, xy, r, T, dur=0.7, group=None, z=70):
    """svg_vocab's not-mark (a ring and one bar, upper left to lower right)
    drawn in over a forbidden thing at xy in one stroke: the ring from its
    upper left, then the bar across (one trace, so one animation; `group`
    ties it to the unveil it goes with). Returns the element."""
    from svg_vocab import NOT_RED, not_mark_points
    ring, bar = not_mark_points(xy, r, n=28)
    return traced_el(key, region, list(ring) + list(bar), NOT_RED, max(2.4, r * 0.16), T, dur,
                     z=z, group=group)


def arrow_el(key, pts, T, dur=0.5, col=TEXT_DIM, width=2.4, head=9.0, region="bench", z=40,
             group=None):
    """An arrow traced along pts, its filled head coming in as the line
    arrives (both in one group). Returns (line, head)."""
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    L = max(1e-6, math.hypot(x1 - x0, y1 - y0))
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    hd = [(x1 - ux * head - uy * head * .55, y1 - uy * head + ux * head * .55), (x1, y1),
          (x1 - ux * head + uy * head * .55, y1 - uy * head - ux * head * .55)]
    stop = min(head * 0.4, L * 0.5)
    group = group or key
    line = traced_el(key, region, list(pts[:-1]) + [(x1 - ux * stop, y1 - uy * stop)], col, width,
                     T, dur, z=z, group=group)
    tip = add(El(key + ".h", region,
                 f'<polygon points="{B.pts_str(hd)}" fill="{rgb(col)}" stroke="{rgb(col)}" '
                 f'stroke-width="1" stroke-linejoin="round"/>', z=z))
    th = T + dur * 0.8
    tip.ev("in", th, B.fit(th, 0.2, least=0.1), group=group)
    return line, tip


def set_change(outs, ins, T, dur=0.6, group="set"):
    """A crossfade of bench sets (element keys), inside the bench."""
    for k in outs:
        B.ELS[k].ev("out", T, dur, group=group)
    for k in ins:
        B.ELS[k].ev("in", T, dur, group=group)


# ---------------------------------------------------------------------------
# setup: the panels, the strip's plan, the places, the altar set
# ---------------------------------------------------------------------------

def setup():
    PLACES.clear()
    PLACES.update(_place_defs())
    PLACE_SHOWN.clear()
    _ALTAR_HID.clear()
    sx, sy, sw, sh = STRIP
    bx, by, bw, bh = BENCH
    panels = (f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="8" fill="{rgb(PANEL)}" '
              f'stroke="{rgb(SAND_DIM)}" stroke-width="1.5"/>'
              f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="8" fill="{rgb(PANEL)}" '
              f'stroke="{rgb(SAND_DIM)}" stroke-width="1.5"/>')
    add(El("panels", "base", panels, z=0, keep=True))
    add(El("strip.art", "strip", strip_art(), z=5, keep=True))
    _altar_setup()
