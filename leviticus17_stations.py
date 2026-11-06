"""The stations of the Leviticus 1-7 offerings pictures, and their API.

generate_leviticus17_svg.py flies one camera over one world sheet (the
reference page's court plan and offerings table, drawn by
generate_tabernacle_reference at its own coordinates) and over these
stations round it: screen-sized cards for what a table cell can't hold.
Each station is a 1024 x 576 card in its own px, set on the sheet at the
corner leviticus17_spec.STATIONS gives it. A rest on it is the whole card
at leviticus17_spec.STATION_S (the one lens, 0.829: a 14 px word reads at
11.6 px); there are no close-ups.

The Station API
---------------
A station is a `Station` subclass, one instance in `registry()`:

    class Altar(Station):
        key = "A"
        def targets(self, ctx):     # {target id: Target} in card px
        def base(self, ctx):        # the card's own drawing: svg string
        def act(self, ctx, verb, key, t, opts):   # "flare", "move", ...

- `shots()` (the base's, kept by every card): {"": (1.0, x, y)}, the card
  point (x, y) a rest on it puts at the screen's centre (the card's
  middle); the generator adds the card's corner and sets the scale
  (STATION_S; L, Sinai, at 1). A spec names it by the station's key ("A").
- `targets(ctx)`: everything a beat can name, by its full id ("A.fire").
  A `Target` has a `box` (card px, x0 y0 x1 y1), an `outline` (a list of
  (points, closed) the pulse and the steady outline run round) and a
  `draw(ctx, t)` that returns its svg drawn in at `t` seconds, or already
  there when `t` is None. A target with no `draw` is an outline only.
- `base(ctx)`: the card and what is always on it once the card is seen;
  `card(self)` gives the plain panel.
- `act(ctx, verb, key, t, opts)`: the verbs that aren't "light", "pulse"
  or "current" (those the generator does from `targets`); return svg.
- State: a target stays drawn once lit, unless `persists(key)` says no
  (things only this verse shows, as an offerer's hand). `pkey(key, verse)`
  is what persists, `verse` giving the file's `beast` and `ref` (B keeps
  each offering's board apart, and each beast's on it: `offering_of`; A
  keeps each case's stack and blood: `case_of`), `slot_of(key, verse)`
  puts targets in one place where the latest lit is the one shown (C's
  three animals, each case's own), and `moved(key, opts)` names the target
  a "move" leaves drawn in later files (B's shares, D's meat).

Text: every word a station writes goes through `ctx.chip` or `ctx.label`,
which measure it (Georgia, svg_vocab.text_w) and record its box for the
generator's QC (overlaps, off the frame at rest, under the HUD). Figures
are svg_figures parts drawn with `ctx.figure` (inline) or `ctx.fig_def` +
`ctx.use` (in <defs>, for a token that repeats). The house rules hold: no
prose, WEB words of four at most, nothing loops, every motion has its
begin.

Target ids by station:
- plan (world px, the court plan): plan.tent, plan.court, plan.moses,
  plan.priests, plan.ring, plan.north, plan.ash, plan.clean, plan.bloodpath,
  plan.outpath; tokens (verb "move") plan.ox, plan.sheep, plan.crop,
  plan.bull_out, plan.ash_out, plan.goat, plan.fgoat, plan.lamb (the ram's
  way to the north side, or {"to": "door"} the ox's), plan.bread (to the
  priest and the altar, 2:8), plan.ashes (hearth to the ash place, 6:10);
  {"dur": s} sets a walk's length.
- A (altar): A.fire, A.wood, A.slot.<pieces|head|fat|burnt|memorial|bird>,
  A.whole, A.horns, A.side, A.pool, A.ashes, A.neck, A.crop, A.wings,
  A.notdivided ("not severed" in the sin offering), A.bird2 (the pair's
  second bird, each named: 5:7), A.priest, A.days, A.morning, A.continual,
  A.chip:<word> (a word of the verse by the fire, this verse only); verb
  "flare" on A.fire. The stack, the bird bay
  and the priest are each law's own (`section_of`).
- B (parts board, the verse's `beast`): B.<part> for every
  svg_figures.beast_parts key, B.fat (the fat as one), B.water,
  B.share_altar, B.share_priests, B.chip:<word> (this verse only);
  B.up:<part>[:<chip>] and B.at:<share>:<part>, a move's end state in the
  later verses of its board (7:30-36). Verb
  "move" on a part: lifted and held (the breast waved, 7:30; the thigh
  heaved, 7:32; {"chip": word}), or {"to": "altar" | "priests" | "priest"}
  a small copy carried to that share (7:31). B.loins is the loins' line: its
  word is kidney_fat's chip "fat by the loins", so it has a chip of its
  own only in a file where B.kidney_fat isn't shown.
- C (cast): C.ox, C.bull (left), C.sheep, C.ram, C.lamb (middle), C.goat,
  C.fgoat (right); C.offerer, C.hand, C.head, C.elders (this verse only);
  C.chip:<left|mid|right>:<word> (a word under a slot, this verse only).
  The offerer's pose brings his hand down on the verse's beast's head.
  Each case's cast is its own (`slot_of`).
- H (holy place): H.veil, H.drops, H.incense, H.horns.
- G, K (leviticus17_st_meal), M, T (leviticus17_st_law), D, S, L
  (leviticus17_st_peace): see those modules.
"""

import functools
import math
import re
from xml.sax.saxutils import escape

import offerings as OF
import sanctuary as SN
import svg_figures as F
import svg_priest as SP
import generate_tabernacle as GT
from generate_tabernacle import (BG, BRONZE, GOLD, GRAY, HL, PANEL, RED,
                                 SAND, SAND_DIM, SILVER, TEXT, TEXT_DIM,
                                 WHITE_LINEN, ACACIA)
from svg_map_camera import (EASE, fade, inv_scale, ink, traced_el)
from svg_surface import SvgCanvas, SvgLayer, _fmt
from svg_vocab import flame, mix, not_mark_points, text_w

CW, CH = 1024, 576                     # a station card
BLOOD = (178, 42, 38)                  # blood, a step past the house red
WATER = (120, 160, 214)
FIRE_OUT = (236, 150, 64)
FIRE_IN = (255, 214, 120)
ASH = (128, 124, 118)
CHIP_PX = 16                           # a chip's type, card px
FIG_MARK = re.compile(r"\x02(\d+)\x02")   # ctx.figure's mark
HUD_RECT = (0, 0, 300, 50)             # the title plate's corner, screen px


def pts_str(pts):
    return " ".join(f"{_fmt(x)},{_fmt(y)}" for x, y in pts)


def rgb(c):
    return f"rgb({int(c[0])},{int(c[1])},{int(c[2])})"


def rect_pts(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def ellipse_pts(cx, cy, rx, ry, n=28):
    return [(cx + rx * math.cos(2 * math.pi * k / n),
             cy + ry * math.sin(2 * math.pi * k / n)) for k in range(n)]


def bounds(pts):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return (min(xs), min(ys), max(xs), max(ys))


def union_box(bs):
    bs = [b for b in bs if b]
    return (min(b[0] for b in bs), min(b[1] for b in bs),
            max(b[2] for b in bs), max(b[3] for b in bs))


# ---------------------------------------------------------------------------
# The motion helpers: every one plays once, from an explicit begin
# ---------------------------------------------------------------------------

def t_s(t):
    return f"{max(0.0, t):.2f}s"


def appear(inner, t, how="fade", dur=0.5, lift=8, about=(0, 0)):
    """`inner` there from the first frame (t None), or brought in at t:
    "fade", "lift" (fade in while rising), "grow" (up from `about`, its foot)
    or "pop" (scaled up from `about`)."""
    if t is None or not inner:
        return inner
    if how == "lift":
        return (f'<g opacity="0">{fade(t, dur)}<g transform="translate(0 '
                f'{lift})"><animateTransform attributeName="transform" '
                f'type="translate" values="0 {lift};0 0" begin="{t_s(t)}" '
                f'dur="{dur:.2f}s" fill="freeze" calcMode="spline" '
                f'keyTimes="0;1" keySplines="{EASE}"/>{inner}</g></g>')
    if how in ("grow", "pop"):
        x, y = about
        v0 = "1 0.02" if how == "grow" else "0.05 0.05"
        return (f'<g opacity="0"><set attributeName="opacity" to="1" '
                f'begin="{t_s(t)}"/><g transform="translate({_fmt(x)} '
                f'{_fmt(y)})"><g transform="scale({v0})">'
                f'<animateTransform attributeName="transform" type="scale" '
                f'values="{v0};1 1" begin="{t_s(t)}" dur="{dur:.2f}s" '
                f'fill="freeze" calcMode="spline" keyTimes="0;1" '
                f'keySplines="{EASE}"/><g transform="translate({_fmt(-x)} '
                f'{_fmt(-y)})">{inner}</g></g></g></g>')
    return f'<g opacity="0">{fade(t, dur)}{inner}</g>'


def fade_out(inner, t, dur=0.5):
    return f'<g>{fade(t, dur, out=True)}{inner}</g>'


def trace(pts, col, width, t, dur=1.0, closed=False, extra=""):
    """A line drawn on at t, or there (t None). `width` None: the stroke
    width is inherited (the plan's screen-constant group)."""
    sw = "" if width is None else f' stroke-width="{_fmt(width)}"'
    if t is None:
        tag = "polygon" if closed else "polyline"
        return (f'<{tag} points="{pts_str(pts)}" fill="none" '
                f'stroke="{rgb(col)}"{sw} stroke-linejoin="round"{extra}/>')
    el, _L = traced_el(list(pts), col, t, dur, closed=closed)
    return f'<g{sw}{extra}>{el}</g>'


def pulse_at(pts, begin, closed=True, col=HL, op=1.0):
    """One pulse of an outline from `begin`, played once; it holds at full
    strength after it. svg_surface's pulses all begin at 0 s, so a pulse on
    a word is this. Hidden before `begin`. No stroke-width: it rides the
    screen-constant group it is put in."""
    tag = "polygon" if closed else "polyline"
    return (f'<{tag} points="{pts_str(pts)}" fill="none" stroke="{rgb(col)}" '
            f'stroke-linejoin="round" stroke-opacity="0">'
            f'<animate attributeName="stroke-opacity" '
            f'values="{op * .25:.3f};{op:.3f};{op * .72:.3f};{op:.3f}" '
            f'keyTimes="0;0.35;0.7;1" dur="0.8s" begin="{t_s(begin)}" '
            f'fill="freeze" calcMode="spline" '
            f'keySplines="{EASE};{EASE};{EASE}"/></{tag}>')


def steady_at(pts, begin, closed=True, col=HL, op=0.85):
    """A thing current again: its outline faded in, steady, no pulse."""
    tag = "polygon" if closed else "polyline"
    return (f'<{tag} points="{pts_str(pts)}" fill="none" stroke="{rgb(col)}" '
            f'stroke-linejoin="round" stroke-opacity="0">'
            f'<animate attributeName="stroke-opacity" values="0;{op:.2f}" '
            f'dur="0.4s" begin="{t_s(begin)}" fill="freeze" '
            f'calcMode="spline" keyTimes="0;1" keySplines="{EASE}"/>'
            f'</{tag}>')


def flare_anim(t, about, k=1.32, dur=1.2):
    """A fire's one flare: up by k and back, once."""
    x, y = about
    return (f'<animateTransform attributeName="transform" type="scale" '
            f'values="1 1;{k:.2f} {k:.2f};1 1" keyTimes="0;0.4;1" '
            f'begin="{t_s(t)}" dur="{dur:.2f}s" fill="freeze" '
            f'calcMode="spline" keySplines="{EASE};{EASE}"/>'), (x, y)


def motion(path_pts, begin, dur):
    d = "M" + " L".join(f"{_fmt(x)} {_fmt(y)}" for x, y in path_pts)
    return (f'<animateMotion path="{d}" begin="{t_s(begin)}" '
            f'dur="{dur:.2f}s" fill="freeze" calcMode="spline" '
            f'keyPoints="0;1" keyTimes="0;1" keySplines="{EASE}"/>')


# ---------------------------------------------------------------------------
# Text, measured
# ---------------------------------------------------------------------------

class TextBox:
    """A word on the sheet, for the QC: its world box (or, `pinned`, its box
    in screen px about its world anchor), when it comes in, and its key."""

    def __init__(self, key, box, t, pinned=False, anchor=None, station=""):
        self.key, self.box, self.t = key, box, t
        self.pinned, self.anchor, self.station = pinned, anchor, station


def text_box(s, xy, size, anchor="mm", bold=False, italic=False):
    """The ink box of `s` at `xy` (card px): Georgia, as the SVG asks for."""
    l, t, r, b = ink(s, size, bold, italic, anchor)
    return (xy[0] + l, xy[1] + t, xy[0] + r, xy[1] + b)


_SVG_H = {"l": "start", "m": "middle", "r": "end"}
_SVG_V = {"a": "text-before-edge", "t": "text-before-edge", "m": "central",
          "s": "alphabetic", "b": "text-after-edge", "d": "text-after-edge"}


def text_svg(s, xy, size, col=TEXT, anchor="mm", bold=False, italic=False,
             extra=""):
    a = [f'x="{_fmt(xy[0])}"', f'y="{_fmt(xy[1])}"',
         f'font-size="{_fmt(size)}"', f'text-anchor="{_SVG_H[anchor[0]]}"',
         f'dominant-baseline="{_SVG_V[anchor[1]]}"', f'fill="{rgb(col)}"']
    if bold:
        a.append('font-weight="bold"')
    if italic:
        a.append('font-style="italic"')
    return f'<text {" ".join(a)}{extra}>{escape(s)}</text>'


# ---------------------------------------------------------------------------
# Targets, stations and the drawing context
# ---------------------------------------------------------------------------

class Target:
    """One thing a beat can name. Card px (world px on the plan)."""

    def __init__(self, key, box=None, outline=(), draw=None, anchor=None):
        self.key = key
        self.outline = list(outline)       # [(points, closed)]
        if box is None and self.outline:
            box = union_box([bounds(p) for p, _c in self.outline])
        self.box = box
        self.draw = draw                   # draw(ctx, t) -> svg
        self.anchor = anchor or (((box[0] + box[2]) / 2,
                                  (box[1] + box[3]) / 2) if box else None)


class Station:
    """A card on the world sheet. Subclasses set `key` and override the
    methods below; `origin` is set by `registry()` from the spec."""

    key = "?"
    size = (CW, CH)
    origin = (0, 0)
    world = False          # True: drawn from world parts, culled, not a card
    VERSE_LOCAL = ()       # target ids (or prefixes ending in ":") that don't persist
    SLOTS = {}             # target id -> slot name

    def shots(self):
        return {"": (1.0, CW / 2, CH / 2)}

    def targets(self, ctx):
        return {}

    def base(self, ctx):
        return self.card()

    def base_pieces(self, ctx):
        """[(key, svg)]: the parts of the card's own drawing that belong to
        a case or verse, drawn as pieces so the next file carries them
        (generate_leviticus17_svg.Carry) when it doesn't draw them."""
        return []

    def act(self, ctx, verb, key, t, opts):
        raise KeyError(f"{self.key}: no verb {verb!r} for {key!r}")

    def persists(self, key):
        return not any(key == p or (p.endswith(":") and key.startswith(p))
                       for p in self.VERSE_LOCAL)

    def pkey(self, key, verse):
        return key

    def moved(self, key, opts):
        """The target id a "move" leaves drawn in later files (its end
        state), or None: the move is this verse's only."""
        return None

    def slot_of(self, key, verse=None):
        return self.SLOTS.get(key)

    def rect(self):
        ox, oy = self.origin
        return (ox, oy, ox + self.size[0], oy + self.size[1])

    def card(self):
        return (f'<rect x="0" y="0" width="{CW}" height="{CH}" rx="10" '
                f'fill="{rgb(PANEL)}" stroke="{rgb(SAND_DIM)}" '
                f'stroke-width="2"/>')


class Ctx:
    """What a station draws with in one file: the flight (for the
    screen-constant pieces), the verse, the state, and the registers the
    generator reads back (defs, texts for QC, outlines)."""

    def __init__(self, fl, ref, verse, beast="", before=(), lit=None):
        self.fl = fl
        self.ref = ref                     # (c, v) or (c, v1, v2)
        self.verse = verse
        self.beast = beast
        self.before = set(before)          # pkeys lit in earlier files
        self.lit = lit or {}               # target id -> its light time here
        self.origin = (0, 0)
        self.station = ""
        self.defs = {}                     # id -> svg (in <defs>)
        self.texts = []                    # TextBox
        self.pins = []                     # world text under the inverse font
        self.outlines = []                 # world outline elements
        self.notes = []                    # QC remarks a station adds
        self.flares = {}                   # target id -> [times] of "flare"
        self._figs, self._fig_ids = [], {}  # ctx.figure's marks; shared figures' def ids

    # -- coordinates ------------------------------------------------------
    def w(self, p):
        return (p[0] + self.origin[0], p[1] + self.origin[1])

    def wbox(self, b):
        ox, oy = self.origin
        return (b[0] + ox, b[1] + oy, b[2] + ox, b[3] + oy)

    # -- words ------------------------------------------------------------
    def label(self, key, s, xy, size=CHIP_PX, col=TEXT, anchor="mm",
              bold=False, italic=False, t=None, how="fade"):
        """A plain word on the card (no plate)."""
        self.texts.append(TextBox(key, self.wbox(text_box(
            s, xy, size, anchor, bold, italic)), t or 0.0,
            station=self.station))
        return appear(text_svg(s, xy, size, col, anchor, bold, italic), t, how)

    def chip(self, key, s, xy, size=CHIP_PX, anchor="mm", t=None, lead=None,
             col=TEXT, how="fade", edge=SAND_DIM):
        """A word on a plate, with a leader to `lead` if given (card px)."""
        x0, y0, x1, y1 = text_box(s, xy, size, anchor)
        px0, py0, px1, py1 = x0 - 7, y0 - 5, x1 + 7, y1 + 6
        out = ""
        if lead is not None:
            lx = min(max(lead[0], px0 + 4), px1 - 4)
            ly = py1 if lead[1] > py1 else (py0 if lead[1] < py0 else
                                            (py0 + py1) / 2)
            if py0 <= lead[1] <= py1:
                lx = px1 if lead[0] > px1 else px0
            out += (f'<line x1="{_fmt(lx)}" y1="{_fmt(ly)}" '
                    f'x2="{_fmt(lead[0])}" y2="{_fmt(lead[1])}" '
                    f'stroke="{rgb(TEXT_DIM)}" stroke-width="1.3"/>'
                    f'<circle cx="{_fmt(lead[0])}" cy="{_fmt(lead[1])}" '
                    f'r="2.6" fill="{rgb(TEXT_DIM)}"/>')
        out += (f'<rect x="{_fmt(px0)}" y="{_fmt(py0)}" '
                f'width="{_fmt(px1 - px0)}" height="{_fmt(py1 - py0)}" rx="5" '
                f'fill="{rgb(BG)}" fill-opacity="0.88" stroke="{rgb(edge)}" '
                f'stroke-width="1.2"/>')
        out += text_svg(s, xy, size, col, anchor)
        self.texts.append(TextBox(key, self.wbox((px0, py0, px1, py1)),
                                  t or 0.0, station=self.station))
        return appear(out, t, how)

    def pin_text(self, key, s, xy_world, size=15, anchor="mm", t=None,
                 col=TEXT, bold=False):
        """A word held at `size` screen px wherever the camera is (the
        plan's words, at the lens and in the 7:37-38 zooms): under the
        generator's inverse font group, at a world point."""
        l, tp, r, b = ink(s, size, bold, False, anchor)
        self.texts.append(TextBox(key, (l - 3, tp - 3, r + 3, b + 3), t or 0.0,
                                  pinned=True, anchor=xy_world,
                                  station=self.station))
        k = 1.0 / size
        a = (f'x="{_fmt(xy_world[0])}" y="{_fmt(xy_world[1])}" '
             f'text-anchor="{_SVG_H[anchor[0]]}" '
             f'dominant-baseline="{_SVG_V[anchor[1]]}"'
             + (' font-weight="bold"' if bold else ""))
        el = (f'<text {a} fill="{rgb(BG)}" stroke="{rgb(BG)}" '
              f'stroke-opacity="0.85" stroke-linejoin="round">{escape(s)}</text>'
              f'<text {a} fill="{rgb(col)}">{escape(s)}</text>')
        self.pins.append((size, appear(el, t)))
        del k
        return ""

    # -- figures ----------------------------------------------------------
    def _draw(self, parts, x, gy, s, ink_=TEXT, page=PANEL, flip=1, rot=0.0,
              style=None):
        c = SvgCanvas(10, 10)
        F.draw(c, parts, x, gy, s, ink_, page, flip=flip, rot=rot, style=style)
        return "".join(c._els)

    def figure(self, parts, x, gy, s, ink_=TEXT, page=PANEL, flip=1, rot=0.0,
               style=None):
        """A figure at (x, gy), as a mark the generator resolves
        (`resolve_figures`): drawn in place where it is drawn once, or put
        in <defs> and used where a station draws the same figure twice."""
        at0 = self._draw(parts, 0, 0, s, ink_, page, flip, rot, style)
        self._figs.append((at0, x, gy, (parts, s, ink_, page, flip, rot, style)))
        return f"\x02{len(self._figs) - 1}\x02"

    def resolve_figures(self, svg):
        uses = [int(i) for i in FIG_MARK.findall(svg)]
        n = {}
        for i in uses:
            n[self._figs[i][0]] = n.get(self._figs[i][0], 0) + 1

        def one(m):
            at0, x, gy, args = self._figs[int(m.group(1))]
            if not at0:
                return ""
            if n[at0] < 2:
                return self._draw(args[0], x, gy, *args[1:])
            did = self._fig_ids.setdefault(at0, f"fg{len(self._fig_ids)}")
            self.defs.setdefault(did, f'<g id="{did}">{at0}</g>')
            return self.use(did, x, gy)
        return FIG_MARK.sub(one, svg)

    def fig_def(self, did, parts, s, ink_=TEXT, page=PANEL, flip=1,
                style=None):
        """A figure in <defs>, its feet at (0, 0), drawn at scale s."""
        if did not in self.defs:
            self.defs[did] = f'<g id="{did}">' + self._draw(
                parts, 0, 0, s, ink_, page, flip, style=style) + "</g>"
        return did

    def use(self, did, x, y):
        return f'<use href="#{did}" transform="translate({_fmt(x)} {_fmt(y)})"/>'

    # -- outlines ---------------------------------------------------------
    def outline(self, target, t, first=True):
        """The pulse (first) or the steady outline round a target, in world
        px, put in the generator's screen-constant outline group."""
        for pts, closed in target.outline:
            wp = [self.w(p) for p in pts]
            self.outlines.append(pulse_at(wp, t, closed) if first
                                 else steady_at(wp, t, closed))


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
    scale k with the inset's top-left corner (IX, IY) at card point `at`."""
    d, od = FilteredLayer(), SvgLayer()
    GT.INSETS[name](d, od, None, 1.0, 1.0)
    ox, oy = at[0] - GT.IX * k, at[1] - GT.IY * k
    return (f'<g transform="translate({_fmt(ox)} {_fmt(oy)}) scale({k})">'
            + "".join(d.elements()) + "</g>")


def inset_pt(p, k, at):
    return (at[0] + (p[0] - GT.IX) * k, at[1] + (p[1] - GT.IY) * k)


def slab(x0, y0, x1, y1, fill, stroke=TEXT, r=6):
    return (f'<rect x="{_fmt(x0)}" y="{_fmt(y0)}" width="{_fmt(x1 - x0)}" '
            f'height="{_fmt(y1 - y0)}" rx="{r}" fill="{rgb(fill)}" '
            f'stroke="{rgb(stroke)}" stroke-width="1.4"/>')


def heap_pts(cx, gy, w, h):
    return [(cx - w / 2, gy), (cx - w * .36, gy - h * .45),
            (cx - w * .18, gy - h * .85), (cx, gy - h),
            (cx + w * .2, gy - h * .8), (cx + w * .38, gy - h * .4),
            (cx + w / 2, gy)]


def heap(cx, gy, w, h, col=ASH):
    pts = F.smooth(heap_pts(cx, gy, w, h), n=3)
    return (f'<polygon points="{pts_str(pts)}" fill="{rgb(mix(PANEL, col, .7))}"'
            f' stroke="{rgb(col)}" stroke-width="1.4"/>')


def flames(xs, gy, hs, ids=""):
    """Tongues of fire standing on gy: an outer and an inner colour."""
    c = SvgCanvas(10, 10)
    for x, h in zip(xs, hs):
        flame(c, x - h * 0.12, gy, h, FIRE_OUT)
    for x, h in zip(xs, hs):
        flame(c, x - h * 0.07, gy, h * 0.6, FIRE_IN)
    return "".join(c._els)


# ---------------------------------------------------------------------------
# plan: the court plan's Leviticus layer (world px)
# ---------------------------------------------------------------------------

PLAN = SN.Plan(730, 440, 14)                 # the reference page's own


def _pp(x, y):
    return PLAN.pt(x, y)


ALTAR_BOX = PLAN.box(*SN.plan_box("altar"))  # (left, top, w, h)
ALT = (ALTAR_BOX[0], ALTAR_BOX[1], ALTAR_BOX[0] + ALTAR_BOX[2],
       ALTAR_BOX[1] + ALTAR_BOX[3])          # 1605, 755, 1675, 825
TENT_PX = PLAN.box(*SN.TENT)
TENT_R = (TENT_PX[0], TENT_PX[1], TENT_PX[0] + TENT_PX[2],
          TENT_PX[1] + TENT_PX[3])           # 870, 720, 1290, 860
COURT_PX = PLAN.box(*SN.COURT)
COURT_R = (COURT_PX[0], COURT_PX[1], COURT_PX[0] + COURT_PX[2],
           COURT_PX[1] + COURT_PX[3])
NORTH = SN.PLACE["north_side"]
NORTH_R = (_pp(NORTH.box[0], NORTH.box[1]) + _pp(NORTH.box[2], NORTH.box[3]))
ASH_PT = _pp(*SN.PLACE["ash_place"].pt)      # 1703, 790
CLEAN_PT = (2560, 800)                       # off the plan, NOT_GIVEN: east, past the gate
CAMP_EDGE = (590, 300, 2270, 1280)           # dashed, not to scale
GATE_X = COURT_R[2]
DOOR_PT = _pp(SN.DOOR_X, 26.4)                # under the altar of incense's name
VEIL_PT = _pp(SN.VEIL_X, 26.4)
RING_PAD = 9.0                               # the blood ring, round the altar
TOKEN_H = 30.0                               # a beast token's height, world px
PERSON_H = 36.0
PIN_PX = 16                                  # the plan's words, screen px


class Plan(Station):
    key = "plan"
    world = True
    size = (CAMP_EDGE[2] - 560 + 400, 1300)
    origin = (0, 0)
    VERSE_LOCAL = ("plan.moses", "plan.ox", "plan.sheep", "plan.crop", "plan.bull_out",
                   "plan.ash_out", "plan.priest_alt", "plan.goat", "plan.fgoat", "plan.lamb",
                   "plan.bread", "plan.ashes")

    def rect(self):
        return (560, 280, 2720, 1300)

    def shots(self):
        return {}

    def base(self, ctx):
        x0, y0, x1, y1 = CAMP_EDGE
        return (f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" '
                f'height="{y1 - y0}" rx="40" fill="none" '
                f'stroke="{rgb(SAND_DIM)}" stroke-width="3" '
                f'stroke-dasharray="18 14"/>')

    def targets(self, ctx):
        T = {}
        T["plan.tent"] = Target("plan.tent", outline=[(rect_pts(*TENT_R), True)])
        T["plan.court"] = Target("plan.court",
                                 outline=[(rect_pts(*COURT_R), True)])
        mx, my = DOOR_PT[0] + 44, TENT_R[1] + 24

        def moses(c, t):
            did = c.fig_def("man_staff", F.man(staff=True), PERSON_H / 97)
            c.pin_text("plan.moses", "Moses", (mx + 12, my - 20), PIN_PX, "lm", t)
            return appear(c.use(did, mx, my), t)
        T["plan.moses"] = Target("plan.moses", box=(mx - 8, my - 40, mx + 8, my),
                                 draw=moses)
        pr = [(ALT[0] - 34, ALT[3] - 12), (ALT[2] + 58, ALT[3] - 12)]

        def priests(c, t):
            did = c.fig_def("priest_tok", F.priest(), PERSON_H / 105)
            c.pin_text("plan.priests", "Aaron's sons",
                       (pr[1][0] + 12, pr[1][1] - 26), PIN_PX, "lm", t)
            return appear("".join(c.use(did, x, y) for x, y in pr), t)
        T["plan.priests"] = Target("plan.priests", box=(pr[0][0] - 9, pr[0][1] - 37,
                                                        pr[1][0] + 9, pr[1][1]),
                                   draw=priests)
        ring = rect_pts(ALT[0] - RING_PAD, ALT[1] - RING_PAD,
                        ALT[2] + RING_PAD, ALT[3] + RING_PAD)

        def ring_draw(c, t):
            return trace(ring + ring[:1], BLOOD, None, t, 1.4,
                         extra=' stroke-opacity="0.9"')
        # its highlight stands off the red, so the ring itself still reads
        T["plan.ring"] = Target("plan.ring", outline=[(rect_pts(
            ALT[0] - RING_PAD + 4, ALT[1] - RING_PAD + 4, ALT[2] + RING_PAD - 4,
            ALT[3] + RING_PAD - 4), True)], draw=ring_draw)
        nr = NORTH_R

        def north(c, t):
            c.pin_text("plan.north", "north", ((nr[0] + nr[2]) / 2, nr[1] - 6), PIN_PX,
                       "mb", t)
            return appear(f'<rect x="{_fmt(nr[0])}" y="{_fmt(nr[1])}" '
                          f'width="{_fmt(nr[2] - nr[0])}" '
                          f'height="{_fmt(nr[3] - nr[1])}" '
                          f'fill="{rgb(mix(PANEL, SAND, .35))}" fill-opacity="0.35" '
                          f'stroke="{rgb(SAND)}" stroke-dasharray="6 5"/>', t)
        T["plan.north"] = Target("plan.north", outline=[(rect_pts(*nr), True)],
                                 draw=north)
        ax, ay = ASH_PT

        # its name sits on the heap and runs east, clear of the altar's
        # ring and the north side (at the lens the altar is 58 px wide) and
        # over "Aaron's sons"
        def ash(c, t):
            c.pin_text("plan.ash", "place of the ashes", (ax - 10, ay - 26), PIN_PX,
                       "lb", t)
            return appear(heap(ax, ay + 8, 26, 14), t)
        T["plan.ash"] = Target("plan.ash", box=(ax - 14, ay - 8, ax + 14, ay + 8),
                               outline=[(heap_pts(ax, ay + 9, 30, 17), True)],
                               draw=ash)
        cx, cy = CLEAN_PT

        def clean(c, t):
            c.pin_text("plan.clean", "outside the camp", (cx, cy - 64), PIN_PX,
                       "mb", t)
            c.pin_text("plan.clean2", "clean place", (cx, cy + 22), PIN_PX, "mt", t)
            wood = "".join(slab(cx - 30 + i * 21, cy - 2, cx - 12 + i * 21, cy + 6,
                                mix(PANEL, ACACIA, .8), ACACIA, 2)
                           for i in range(3))
            return appear(heap(cx, cy + 10, 70, 22) + wood
                          + flames([cx - 14, cx, cx + 14], cy - 2, [22, 30, 22]),
                          t)
        T["plan.clean"] = Target("plan.clean", box=(cx - 40, cy - 40, cx + 40, cy + 14),
                                 outline=[(rect_pts(cx - 44, cy - 40, cx + 44, cy + 16), True)],
                                 draw=clean)
        bp = [DOOR_PT, (DOOR_PT[0] - 70, DOOR_PT[1]), (VEIL_PT[0] + 10, VEIL_PT[1])]

        def bloodpath(c, t):
            head = [(VEIL_PT[0] + 24, VEIL_PT[1] - 8), (VEIL_PT[0] + 10, VEIL_PT[1]),
                    (VEIL_PT[0] + 24, VEIL_PT[1] + 8)]
            return (trace(bp, BLOOD, None, t, 1.6)
                    + appear(trace(head, BLOOD, None, None), None if t is None
                             else t + 1.4, dur=0.3))
        # its outline's top runs between the arrowhead and the baseline of
        # the reference's "altar of incense" just above it
        T["plan.bloodpath"] = Target("plan.bloodpath", outline=[(rect_pts(
            VEIL_PT[0] + 4, VEIL_PT[1] - 11, DOOR_PT[0] + 4, VEIL_PT[1] + 14), True)],
            draw=bloodpath)
        # from under the reference's "altar of burnt offering", as the bull
        # is carried out (plan.bull_out)
        op = [((ALT[0] + ALT[2]) / 2, ALT[3] + 40), (GATE_X - 60, 880),
              (GATE_X + 60, 870), (CLEAN_PT[0] - 50, CLEAN_PT[1] + 8)]
        T["plan.outpath"] = Target("plan.outpath", outline=[(op, False)],
                                   draw=lambda c, t: trace(
                                       op, SAND, None, t, 1.6,
                                       extra=' stroke-dasharray="10 8"')
                                   if t is None else trace(op, SAND, None, t, 1.6))
        for k in self.TOKENS:
            T[k] = Target(k, box=(0, 0, 1, 1))
        return T

    # the tokens' walks
    PATHS = {
        "plan.ox": [(GATE_X + 20, 880), (1760, 905), (1420, 885),
                    (DOOR_PT[0] + 36, 852)],
        "plan.sheep": [(1890, 700), (1760, 716), (1648, 742)],
        "plan.crop": [((ALT[0] + ALT[2]) / 2 + 8, (ALT[1] + ALT[3]) / 2),
                      (ASH_PT[0] - 2, ASH_PT[1] + 2)],
        "plan.bull_out": [((ALT[0] + ALT[2]) / 2, ALT[3] + 40), (GATE_X - 60, 880),
                          (GATE_X + 60, 870), (CLEAN_PT[0] - 40, CLEAN_PT[1] + 6)],
        "plan.ash_out": [(ASH_PT[0], ASH_PT[1] + 6), (GATE_X - 60, 880),
                         (GATE_X + 60, 870), (CLEAN_PT[0] - 6, CLEAN_PT[1] + 6)],
        # the meal offering presented to the priest by the altar (2:8),
        # set down at his feet, off the altar and its name; the ashes from
        # the hearth to the ash place (6:10)
        "plan.bread": [(GATE_X + 20, 880), (1800, 905), (1734, 858)],
        "plan.ashes": [((ALT[0] + ALT[2]) / 2 + 8, (ALT[1] + ALT[3]) / 2),
                       (ASH_PT[0] - 2, ASH_PT[1] + 2)],
    }
    # a goat, a female goat or a lamb walks the ram's way to the north side,
    # or, with {"to": "door"}, the ox's to the door
    for _k in ("plan.goat", "plan.fgoat", "plan.lamb"):
        PATHS[_k] = PATHS["plan.sheep"]
    del _k
    TO = {"door": "plan.ox", "north": "plan.sheep"}
    TOKENS = {"plan.ox": ("ox", lambda: F.ox(), TOKEN_H * 1.2 / 85, -1),
              "plan.bull_out": ("ox", lambda: F.ox(), TOKEN_H * 1.2 / 85, 1),
              "plan.sheep": ("ram", lambda: F.sheep(ram=True), TOKEN_H / 47, -1),
              "plan.goat": ("goat", lambda: F.goat(), TOKEN_H * 1.05 / 64, -1),
              "plan.fgoat": ("fgoat", lambda: F.goat(female=True), TOKEN_H * 1.05 / 64, -1),
              "plan.lamb": ("lamb", lambda: F.sheep(lamb=True), TOKEN_H * .8 / 28, -1),
              "plan.bread": ("bread", lambda: F.bread(), 2.0, 1),
              "plan.crop": None, "plan.ash_out": None, "plan.ashes": None}
    # a token's chip ({"chip": word}, the verse's word): its world size
    # reads 11.6 px at the lens; above the beasts, under the small ones,
    # where the altar's group leaves room
    CHIP_SIZE = 14
    CHIP_AT = {"plan.crop": ((0, 9), "mt"), "plan.bread": ((0, 6), "mt")}

    def act(self, ctx, verb, key, t, opts):
        if verb != "move":
            return super().act(ctx, verb, key, t, opts)
        path = self.PATHS[self.TO[opts["to"]] if "to" in opts else key]
        show = opts.get("_show", opts["_arrive"])
        dur = opts.get("dur", 2.4 if len(path) > 2 else 1.2)
        spec = self.TOKENS[key]
        if spec is None:
            col = ASH if key in ("plan.ash_out", "plan.ashes") else (150, 110, 70)
            inner = (f'<ellipse cx="0" cy="-5" rx="9" ry="6" fill="{rgb(col)}" '
                     f'stroke="{rgb(TEXT)}" stroke-width="1.2"/>')
        else:
            name, mk, sc, flip = spec
            did = ctx.fig_def(f"tok_{name}_{flip}", mk(), sc, flip=flip)
            inner = f'<use href="#{did}"/>'
        if opts.get("chip"):
            xy, anc = self.CHIP_AT.get(key, ((0, -TOKEN_H - 6), "mb"))
            halo = (f' stroke="{rgb(BG)}" stroke-width="3" stroke-opacity="0.85" '
                    f'stroke-linejoin="round"')
            inner += (text_svg(opts["chip"], xy, self.CHIP_SIZE, BG, anc, extra=halo)
                      + text_svg(opts["chip"], xy, self.CHIP_SIZE, TEXT, anc))
        x0, y0 = path[0]
        rel = [(x - x0, y - y0) for x, y in path]
        return (f'<g opacity="0"><set attributeName="opacity" to="1" '
                f'begin="{t_s(show)}"/>{fade(show, 0.4)}'
                f'<g transform="translate({_fmt(x0)} {_fmt(y0)})"><g>'
                f'{motion(rel, t, dur)}{inner}</g></g></g>')


# ---------------------------------------------------------------------------
# A: the altar
# ---------------------------------------------------------------------------

AK = 1.4                                     # inset_altar's scale on the card
A_AT = (40, 64)                              # where the inset's corner goes


def _a(p):
    return inset_pt(p, AK, A_AT)


A_BODY = _a((GT.AX, GT.AY)) + _a((GT.AX + GT.AW, GT.AY + GT.AH))
A_TOP = A_BODY[1]                            # the hearth, 158.8
A_HORNS = [[GT.AX - 6, GT.AY - 22, GT.AX + 16, GT.AY],
           [GT.AX + GT.AW - 16, GT.AY - 22, GT.AX + GT.AW + 6, GT.AY]]
SLOT_NAMES = ("pieces", "head", "fat", "burnt", "memorial", "bird")
SLOT_WORD = {"pieces": "pieces", "head": "head", "fat": "fat",
             "burnt": "burnt offering", "memorial": "memorial", "bird": "bird"}
SLOT_X0, SLOT_W, SLOT_GAP = 140, 44, 6
SLOT_Y = (A_TOP - 50, A_TOP - 27)            # on the wood
WOOD1 = [(140, 224), (238, 322), (336, 420)]
WOOD2 = [(186, 272), (286, 372)]
FIRE_XS = [172, 230, 290, 350, 408]
FIRE_HS = [40, 54, 62, 52, 40]
BIRD_AT = (800, 236)                         # the bird bay's dove
BIRD_S = 7.6
BIRD2_AT = (830, 476, 4.6)                   # the pair's second bird (5:7): x, gy, s
PRIEST_AT = (640, 548, 210)                  # svg_priest Form x, gy, h
DAY_Y = 498
DAY_X = (740, 990)


def _horn_pts(h):
    hx0, hy0, hx1, hy1 = h
    return [_a(p) for p in GT.horn_points(hx0, hy0, hx1, hy1,
                                          -1 if hx0 < GT.AX else 1)]


def _slot_box(name):
    i = SLOT_NAMES.index(name)
    x0 = SLOT_X0 + i * (SLOT_W + SLOT_GAP)
    return (x0, SLOT_Y[0], x0 + SLOT_W, SLOT_Y[1])


def _dove_pts():
    """The bay's dove, placed, and its landmarks (card px)."""
    parts = F.dove(descending=False)
    return parts


BIRD_MARKS = ("A.bird", "A.bird2", "A.neck", "A.wings", "A.crop", "A.notdivided")
A_CHIP_AT = [(545, A_TOP - 96), (545, A_TOP - 124)]   # A.chip:<word>, in the order lit


class Altar(Station):
    key = "A"
    # "the whole" is the verse's word, not a part; A.chip:<word> a word of
    # this verse by the fire ("food", "pleasant aroma")
    # and the ashes are taken up in their verse (6:10)
    VERSE_LOCAL = ("A.whole", "A.chip:", "A.ashes")
    CASE_OWN = BIRD_MARKS + ("A.priest", "A.days", "A.morning", "A.continual",
                             "A.horns", "A.side", "A.pool")

    def pkey(self, key, verse):
        """The stack on the wood, the blood's marks, the bird bay and the
        priest in linen are each case's own (`case_of`: the ram's fat isn't
        on the altar at the bird, the bird's blood isn't on its side at the
        meal offering); the fire and the wood are the altar's."""
        if key.startswith("A.slot.") or key in self.CASE_OWN:
            return f"{key}@{case_of(getattr(verse, 'ref', None))}"
        return key

    def base(self, ctx):
        return self.card() + inset_svg("altar", AK, A_AT)

    def base_pieces(self, ctx):
        """The bay's dove: there once any of its marks has been drawn, or
        coming in with the first of them. A piece, not the base, so a file
        of the next case carries it and fades it as its camera moves."""
        marks = BIRD_MARKS
        if any(self.pkey(m, ctx) in ctx.before for m in marks):
            t = None
        else:
            ts = [ctx.lit[m] for m in marks if m in ctx.lit]
            if not ts:
                return []
            t = min(ts)
        dx, dy = BIRD_AT
        return [("A.dove", appear(ctx.figure(F.dove(descending=False), dx, dy, BIRD_S,
                                             SILVER, PANEL), t))]

    def targets(self, ctx):
        T = {}
        fire_box = (FIRE_XS[0] - 30, A_TOP - 100, FIRE_XS[-1] + 30, A_TOP)

        def fire(c, t):
            ch = c.chip("A.fire", "fire", (548, A_TOP - 8), lead=(414, A_TOP - 22), t=t)
            g = flames(FIRE_XS, A_TOP, FIRE_HS)
            fx = (FIRE_XS[0] + FIRE_XS[-1]) / 2
            # each "flare" of this verse: the fire up by a third and back,
            # once, about its foot
            fl_ = "".join(flare_anim(tf, (fx, A_TOP))[0] for tf in c.flares.get("A.fire", []))
            if fl_:
                g = (f'<g transform="translate({_fmt(fx)} {_fmt(A_TOP)})"><g>{fl_}'
                     f'<g transform="translate({_fmt(-fx)} {_fmt(-A_TOP)})">{g}</g></g></g>')
            return appear(g, t, "grow", 0.9, about=(fx, A_TOP)) + ch
        T["A.fire"] = Target("A.fire", box=fire_box, draw=fire,
                             outline=[(rect_pts(*fire_box), True)])

        def wood(c, t):
            out = []
            for i, (a, b) in enumerate(WOOD1):
                out.append(appear(slab(a, A_TOP - 13, b, A_TOP - 1, mix(PANEL, ACACIA, .75),
                                       ACACIA, 3), None if t is None else t + i * 0.18,
                                  "lift", 0.4))
            for i, (a, b) in enumerate(WOOD2):
                out.append(appear(slab(a, A_TOP - 26, b, A_TOP - 14, mix(PANEL, ACACIA, .75),
                                       ACACIA, 3), None if t is None else t + 0.6 + i * 0.18,
                                  "lift", 0.4))
            ch = c.chip("A.wood", "wood", (60, A_TOP - 6), lead=(140, A_TOP - 10),
                        t=None if t is None else t + 0.3)
            return "".join(out) + ch
        wb = (WOOD1[0][0], A_TOP - 26, WOOD1[-1][1], A_TOP)
        T["A.wood"] = Target("A.wood", box=wb, draw=wood,
                             outline=[(rect_pts(*wb), True)])
        meat, fat = mix(PANEL, RED, .75), mix(PANEL, WHITE_LINEN, .85)
        look = {"pieces": meat, "head": mix(PANEL, RED, .6), "fat": fat,
                "burnt": meat, "memorial": mix(PANEL, WHITE_LINEN, .7),
                "bird": mix(PANEL, SILVER, .55)}
        for i, name in enumerate(SLOT_NAMES):
            b = _slot_box(name)
            row = i % 2
            cy = A_TOP - 102 + row * 30

            def draw(c, t, name=name, b=b, cy=cy):
                x0, y0, x1, y1 = b
                if name == "pieces":
                    body = "".join(slab(x0 + k * 15, y0 + 4, x0 + k * 15 + 13, y1,
                                        look[name], TEXT, 3) for k in range(3))
                elif name == "bird":
                    body = c.figure(F.dove(descending=False), (x0 + x1) / 2, y1 - 1,
                                    1.5, SILVER, PANEL)
                elif name == "memorial":
                    body = heap((x0 + x1) / 2, y1, x1 - x0, 18, WHITE_LINEN)
                else:
                    body = slab(x0, y0 + 2, x1, y1, look[name], TEXT, 7)
                ch = c.chip(f"A.slot.{name}", SLOT_WORD[name], ((x0 + x1) / 2, cy),
                            size=15, lead=((x0 + x1) / 2, y0 + 2))
                return appear(body, t, "lift", 0.5, lift=14) + appear(ch, t)
            T[f"A.slot.{name}"] = Target(f"A.slot.{name}", box=b, draw=draw,
                                         outline=[(rect_pts(b[0] - 3, b[1] - 1, b[2] + 3,
                                                            b[3] + 1), True)])
        sb = (_slot_box("pieces")[0], SLOT_Y[0], _slot_box("bird")[2], SLOT_Y[1])
        T["A.whole"] = Target("A.whole", box=sb, outline=[(rect_pts(sb[0] - 4, sb[1] - 4,
                                                                    sb[2] + 4, sb[3] + 2), True)],
                              draw=lambda c, t: c.chip("A.whole", "the whole",
                                                       (560, A_TOP - 66),
                                                       lead=(sb[2] + 4, SLOT_Y[0] + 10), t=t))
        horns = [_horn_pts(h) for h in A_HORNS]

        def horns_draw(c, t):
            return appear("".join(
                f'<polygon points="{pts_str(p)}" fill="{rgb(BLOOD)}" '
                f'fill-opacity="0.85"/>' for p in horns), t, "fade", 0.6)
        T["A.horns"] = Target("A.horns", outline=[(p, True) for p in horns],
                              draw=horns_draw)
        side = [(A_BODY[2] - 3, A_TOP + 6), (A_BODY[2] - 6, A_TOP + 60),
                (A_BODY[2] - 2, A_TOP + 120), (A_BODY[2] - 5, A_TOP + 170),
                (A_BODY[2] - 3, A_BODY[3] - 2)]
        T["A.side"] = Target("A.side", outline=[(rect_pts(A_BODY[2] - 16, A_TOP + 2,
                                                          A_BODY[2] + 8, A_BODY[3] + 2), True)],
                             draw=lambda c, t: trace(side, BLOOD, 5, t, 1.4))
        pool = [(A_BODY[0] + 20, A_BODY[3] + 6), (A_BODY[2] - 20, A_BODY[3] + 6)]
        pcx = (A_BODY[0] + A_BODY[2]) / 2

        def pool_draw(c, t):
            el = (f'<ellipse cx="{_fmt(pcx)}" cy="{_fmt(A_BODY[3] + 7)}" '
                  f'rx="{_fmt((A_BODY[2] - A_BODY[0]) / 2 - 10)}" ry="7" '
                  f'fill="{rgb(BLOOD)}" fill-opacity="0.8"/>')
            return (trace(pool, BLOOD, 6, t, 1.2)
                    + appear(el, None if t is None else t + 0.9, dur=0.6))
        T["A.pool"] = Target("A.pool", box=(A_BODY[0], A_BODY[3], A_BODY[2], A_BODY[3] + 14),
                             outline=[(ellipse_pts(pcx, A_BODY[3] + 7,
                                                   (A_BODY[2] - A_BODY[0]) / 2, 12), True)],
                             draw=pool_draw)
        T["A.ashes"] = Target("A.ashes", box=(230, A_TOP - 34, 350, A_TOP),
                              outline=[(heap_pts(290, A_TOP - 1, 130, 36), True)],
                              draw=lambda c, t: appear(heap(290, A_TOP - 1, 120, 30), t)
                              + c.chip("A.ashes", "ashes", (560, A_TOP - 40), lead=(350, A_TOP - 14), t=t))
        # the bird bay
        dx, dy = BIRD_AT
        dove = F.dove(descending=False)
        x0, x1, y0, y1 = F.bbox((dove, 0))
        neck = [(dx + 11.6 * BIRD_S, dy - 11.4 * BIRD_S),
                (dx + 8.6 * BIRD_S, dy - 3.2 * BIRD_S)]
        wing = [(dx - 1.5 * BIRD_S, dy - 9.5 * BIRD_S), (dx + 3.5 * BIRD_S, dy - 4.0 * BIRD_S),
                (dx + 6.0 * BIRD_S, dy + 1.0 * BIRD_S)]
        dbox = (dx + x0 * BIRD_S, dy - y1 * BIRD_S, dx + x1 * BIRD_S, dy - y0 * BIRD_S)
        # the dove itself is the base's (Altar.base), once a mark on it is lit
        T["A.bird"] = Target("A.bird", box=dbox, outline=[(F.outline(dove, dx, dy, BIRD_S), True)])
        T["A.neck"] = Target("A.neck", outline=[(rect_pts(*bounds(neck)), True)] and
                             [(ellipse_pts((neck[0][0] + neck[1][0]) / 2, (neck[0][1] + neck[1][1]) / 2,
                                           30, 40), True)],
                             draw=lambda c, t: trace(neck, BLOOD, 4, t, 0.6)
                             + c.chip("A.neck", "head", (neck[0][0] + 44, neck[0][1] - 26),
                                      lead=neck[0], t=t))
        T["A.wings"] = Target("A.wings", outline=[(wing, False)],
                              draw=lambda c, t: trace(wing, HL, 3, t, 0.8)
                              + c.chip("A.wings", "wings", (wing[0][0] - 70, wing[0][1] - 18),
                                       lead=wing[0], t=t))
        # 1:17 "not divide it apart"; 5:8 "not sever it completely": the
        # chips are the verses' own words
        T["A.notdivided"] = Target("A.notdivided", box=dbox,
                                   draw=lambda c, t: c.chip(
                                       "A.notdivided", "not sever it"
                                       if section_of(c.ref).startswith("sin:") else "not divide it",
                                       (dx, dbox[3] + 26), t=t))
        # the second bird of a pair (5:7): one for a sin offering, the other
        # for a burnt offering, each named under it
        d2x, d2y, d2s = BIRD2_AT
        d2box = (d2x + x0 * d2s, d2y - y1 * d2s, d2x + x1 * d2s, d2y - y0 * d2s)

        def bird2(c, t):
            fig = appear(c.figure(F.dove(descending=False), d2x, d2y, d2s, SILVER, PANEL), t)
            return (fig + c.chip("A.bird2", "burnt offering", (d2x - 200, d2y - 40),
                                 lead=(d2box[0] + 8, d2y - 40), t=t)
                    + c.chip("A.bird2:sin", "sin offering", (dx - 40, dbox[1] - 18),
                             t=None if t is None else t + 0.5))
        T["A.bird2"] = Target("A.bird2", box=d2box,
                              outline=[(F.outline(dove, d2x, d2y, d2s), True)], draw=bird2)
        crop = (dx + 7.5 * BIRD_S, dy - 4.0 * BIRD_S)
        T["A.crop"] = Target("A.crop", outline=[(ellipse_pts(crop[0], crop[1], 12, 9), True)],
                             draw=lambda c, t: c.chip("A.crop", "crop", (crop[0] + 70, crop[1] + 34),
                                                      lead=crop, t=t))
        # the priest in linen (6:10)
        px, pgy, ph = PRIEST_AT
        fo = SP.Form(px, pgy, ph)

        def priest(c, t):
            cv = SvgCanvas(10, 10)
            SP.body(cv, fo, TEXT, mix(PANEL, TEXT, .3))
            SP.coat(cv, fo, mix(PANEL, WHITE_LINEN, .8), mix(PANEL, WHITE_LINEN, .45))
            SP.breeches(cv, fo, WHITE_LINEN, hidden=True)
            body = "".join(cv._els)
            return (appear(body, t)
                    + c.chip("A.priest", "linen garment", (px + 92, pgy - ph * .62),
                             lead=(px + fo.hw(pgy - ph * .6) - 4, pgy - ph * .6), t=t)
                    + c.chip("A.priest2", "linen breeches", (px + 96, pgy - ph * .40),
                             lead=(px + fo.waist_hw * .8, fo.thigh_y - 6),
                             t=None if t is None else t + 0.6))
        T["A.priest"] = Target("A.priest", box=(px - 40, pgy - ph - 10, px + 40, pgy),
                               outline=[(fo.skirt(fo.shldr_y, pgy), True)], draw=priest)
        # the day strip (6:9, 12-13): night to morning
        d0, d1 = DAY_X
        strip = [(d0 + 26, DAY_Y), (d1 - 26, DAY_Y)]

        def days(c, t):
            moon = c.figure(F.moon(), d0, DAY_Y + 14, 0.5, SILVER, PANEL)
            sun = c.figure(F.sun(), d1, DAY_Y + 14, 0.5, GOLD, PANEL)
            return (appear(moon + sun, t) + trace(strip, TEXT_DIM, 2, t, 1.6)
                    + c.label("A.days", "all night", ((d0 + d1) / 2, DAY_Y + 22), 15,
                              TEXT_DIM, "mt", italic=True, t=t))
        T["A.days"] = Target("A.days", box=(d0 - 20, DAY_Y - 30, d1 + 20, DAY_Y + 30),
                             outline=[(strip, False)], draw=days)
        T["A.morning"] = Target("A.morning", outline=[([(d1 - 30, DAY_Y - 12), (d1 - 30, DAY_Y + 12)], False)],
                                draw=lambda c, t: trace([(d1 - 30, DAY_Y - 12), (d1 - 30, DAY_Y + 12)],
                                                        GOLD, 3, t, 0.4)
                                + c.label("A.morning", "morning", (d1 - 30, DAY_Y - 22), 15, TEXT,
                                          "mb", t=t))
        ticks = [[(d0 + 70 + k * 50, DAY_Y - 9), (d0 + 70 + k * 50, DAY_Y + 9)] for k in range(3)]
        T["A.continual"] = Target("A.continual", outline=[(p, False) for p in ticks],
                                  draw=lambda c, t: "".join(
                                      trace(p, TEXT, 2.4, None if t is None else t + k * 0.3, 0.3)
                                      for k, p in enumerate(ticks)))
        # A.chip:<word>: a word of this verse by the fire, the first lit
        # under, a second over it
        words = sorted((tt, k) for k, tt in ctx.lit.items() if k.startswith("A.chip:"))
        for i, (_tt, key) in enumerate(words[:len(A_CHIP_AT)]):
            xy = A_CHIP_AT[i]
            T[key] = Target(key, box=text_box(key[7:], xy, CHIP_PX),
                            draw=lambda c, t, key=key, xy=xy: c.chip(key, key[7:], xy, t=t))
        return T

    def act(self, ctx, verb, key, t, opts):
        if verb == "flare" and key == "A.fire":
            return ""                    # drawn on the fire itself (ctx.flares)
        return super().act(ctx, verb, key, t, opts)


# ---------------------------------------------------------------------------
# B: the parts board
# ---------------------------------------------------------------------------

B_CENTRE_X = 450
B_GROUND = 456
B_MAX_W, B_MAX_H = 640, 340
B_SIDE_X = 900                               # the shares' sidebar


def _cut_label(key):
    if key in OF.CUT:
        return OF.CUT[key].label
    return {"fat": "fat"}.get(key, key)


class Board:
    """One beast's board on B: placed parts, their outlines and the chips'
    places, computed once a beast."""

    _cache = {}

    @classmethod
    def of(cls, kind):
        if kind not in cls._cache:
            cls._cache[kind] = cls(kind)
        return cls._cache[kind]

    def __init__(self, kind):
        self.kind = kind
        self.parts, anchors = F.beast_parts(kind)
        x0, x1, y0, y1 = F.bbox((self.parts["silhouette"], 0))
        k = min(B_MAX_W / (x1 - x0), B_MAX_H / (y1 - y0))
        self.k = k
        self.X0 = B_CENTRE_X + (x0 + x1) / 2 * k          # flip = -1
        self.G = B_GROUND

        def P(p):
            return (self.X0 - p[0] * k, self.G - p[1] * k)
        self.P = P
        self.anchor = {key: P(a) for key, a in anchors.items()}
        self.lines = {}
        self.polys = {}
        for key, ps in self.parts.items():
            for kind_, data, _m in ps:
                if kind_ == "fill":
                    self.polys.setdefault(key, []).append([P(q) for q in data])
                elif kind_ == "line":
                    self.lines.setdefault(key, []).append([P(q) for q in data])
        meat = self.polys["meat"][0]
        self.top = min(p[1] for p in meat)
        self.bot = max(p[1] for p in meat)
        self.box = bounds([P((x0, y0)), P((x1, y1))])
        fat_keys = [k_ for k_ in ("fat_cover", "fat_on", "kidney_fat") if k_ in self.polys]
        self.anchor["fat"] = self.anchor["fat_cover"]
        self.fat_keys = fat_keys
        self._layout()

    def outline(self, key):
        """(points, closed) rings round a part: its largest fill, or its lines."""
        if key == "fat":
            return [o for k_ in self.fat_keys for o in self.outline(k_)]
        if key in self.polys and key not in ("pieces", "loins", "backbone"):
            if key in ("fat_on", "kidneys"):
                return [(p, True) for p in self.polys[key]]
            big = max(self.polys[key], key=lambda p: (bounds(p)[2] - bounds(p)[0])
                      * (bounds(p)[3] - bounds(p)[1]))
            return [(big, True)]
        return [(p, False) for p in self.lines.get(key, [])]

    def _layout(self):
        """Each chip's place: above the back or under the belly, near its
        part, two rows a side, pushed apart so no two touch."""
        keys = [k_ for k_ in F.BEAST_PART_KEYS if k_ in self.anchor] + ["fat"]
        mid = (self.top + self.bot) / 2
        rows = {"t1": self.top - 30, "t2": self.top - 62,
                "b1": self.bot + 30, "b2": self.bot + 62}
        upper = sorted([k_ for k_ in keys if self.anchor[k_][1] < mid and k_ != "head"],
                       key=lambda k_: self.anchor[k_][0])
        lower = sorted([k_ for k_ in keys if self.anchor[k_][1] >= mid],
                       key=lambda k_: self.anchor[k_][0])
        self.chips = {}
        for band, ks in (("t", upper), ("b", lower)):
            for i, k_ in enumerate(ks):
                row = f"{band}{1 + i % 2}"
                self.chips[k_] = [self.anchor[k_][0], rows[row], row]
        hx, hy = self.anchor["head"]
        hb = bounds(self.polys["head"][0]) if "head" in self.polys else (hx, hy, hx, hy)
        self.chips["head"] = [min(hb[0] - 10, hx - 40), hy, "head"]
        for row in rows:
            ks = sorted([k_ for k_, c in self.chips.items() if c[2] == row],
                        key=lambda k_: self.chips[k_][0])
            ws = {k_: text_w(_cut_label(k_), CHIP_PX) + 22 for k_ in ks}
            # push right, then pull back from the card's right edge
            x = 20
            for k_ in ks:
                cx = max(self.chips[k_][0], x + ws[k_] / 2)
                self.chips[k_][0] = cx
                x = cx + ws[k_] / 2 + 6
            x = 860
            for k_ in reversed(ks):
                cx = min(self.chips[k_][0], x - ws[k_] / 2)
                self.chips[k_][0] = cx
                x = cx - ws[k_] / 2 - 6

    def chip_xy(self, key):
        x, y, row = self.chips[key]
        return (x, y), ("rm" if row == "head" else "mm")

    def frame(self, keys, pad=16, chipless=()):
        bs = []
        for k_ in keys:
            (x, y), anc = self.chip_xy(k_)
            if k_ not in chipless:
                bs.append(text_box(_cut_label(k_), (x, y), CHIP_PX, anc))
            o = self.outline(k_)
            if o:
                bs.append(union_box([bounds(p) for p, _c in o]))
        b = union_box(bs)
        return (b[0] - pad, b[1] - pad, b[2] + pad, b[3] + pad)

    def hidden(self):
        """The base's shapes (key, index) that later fills cover wholly, so
        never seen: rasterised at 3x, a shape with its stroke against the
        union of the opaque fills drawn after it."""
        if hasattr(self, "_hidden"):
            return self._hidden
        from PIL import Image, ImageChops, ImageDraw
        sheet = F.parts_palette(TEXT, PANEL, RED)
        K = 3

        def sc(pts):
            return [(x * K, y * K) for x, y in pts]
        items = []
        for key in F.BEAST_PART_ORDER:
            if key in self.parts and key != "pieces":
                for i, (kind_, data, mat) in enumerate(self.parts[key]):
                    items.append((key, i, kind_, data, mat))
        cover = Image.new("L", (CW * K, CH * K), 0)
        cd = ImageDraw.Draw(cover)
        hidden = set()
        for key, i, kind_, data, mat in reversed(items):
            fill, stroke, w = sheet.get(mat, sheet["rule"])
            m = Image.new("L", cover.size, 0)
            md = ImageDraw.Draw(m)
            sw = int(math.ceil((w + 1.5) * K))
            if kind_ == "dot":
                (cx, cy), = F.place([(data[0], data[1])], self.X0, self.G, self.k, -1)
                r = data[2] * self.k * K + sw
                md.ellipse((cx * K - r, cy * K - r, cx * K + r, cy * K + r), fill=255)
                pts = None
            else:
                pts = sc([self.P(q) for q in data])
                if kind_ == "fill":
                    md.polygon(pts, fill=255)
                    md.line(pts + pts[:1], fill=255, width=sw, joint="curve")
                else:
                    md.line(pts, fill=255, width=sw, joint="curve")
            if ImageChops.subtract(m, cover).getbbox() is None:
                hidden.add((key, i))
            if kind_ == "fill" and fill is not None and len(pts) > 2:
                cd.polygon(pts, fill=255)
        self._hidden = hidden
        return hidden


CHIPLESS = ("loins",)          # its word is "fat by the loins", kidney_fat's chip


@functools.cache
def _lev_verses(ref):
    import verse_refs
    out = set()
    for r in verse_refs.parse(ref, "Leviticus"):
        for book, c, v in r.verses():
            if book == "Leviticus":
                out.add((c, v))
    return out


def section_of(ref):
    """The law a file is in: "<offering>:<group>" for the offering's law
    for the people or for the priests that holds its first verse, "" in
    neither. The altar's stack and the cast keep each law's own."""
    if not ref:
        return ""
    cv = (ref[0], ref[1])
    for o in OF.OFFERINGS:
        for group, r in o.verses:
            if group in ("For the people", "For the priests") and cv in _lev_verses(r):
                return f"{o.key}:{group}"
    return ""


def case_of(ref):
    """The case a file is in: "c:v" of the latest leviticus17_spec.CASES
    start at or before its first verse (a new beast or bringing: the herd,
    the flock, the birds...). The altar's stack and blood, the kitchen's
    not-marks and the cast are each case's own: the ram's fat isn't on the
    altar when the bird is burned."""
    if not ref:
        return ""
    import leviticus17_spec as SPEC
    cv, best = (ref[0], ref[1]), None
    for c in SPEC.CASES:
        if c <= cv:
            best = c
    return f"{best[0]}:{best[1]}" if best else ""


def offering_of(ref):
    """The offering a file is about: the one whose law for the people or
    for the priests (offerings.OFFERINGS' verses) holds its first verse;
    "" for a verse in neither (7:22-27, 7:37-38)."""
    if not ref:
        return ""
    cv = (ref[0], ref[1])
    for o in OF.OFFERINGS:
        for group, r in o.verses:
            if group in ("For the people", "For the priests") and cv in _lev_verses(r):
                return o.key
    return ""


B_CHIP_AT = [(170, 506), (170, 546)]         # B.chip:<word>, in the order lit
B_TO = {"altar": (B_SIDE_X, 214), "priests": (B_SIDE_X - 34, 470),
        "priest": (B_SIDE_X + 34, 470)}       # where a share goes (7:31, 33)
B_LOOK = {"fat": (WHITE_LINEN, .8), "kidney_fat": (WHITE_LINEN, .8)}


class PartsBoard(Station):
    key = "B"
    VERSE_LOCAL = ("B.water", "B.chip:")

    def board(self, verse_or_ctx):
        beast = getattr(verse_or_ctx, "beast", "") or "bull"
        return Board.of(beast if beast in F.BEAST_KINDS else "bull")

    def pkey(self, key, verse):
        """What persists on B: each offering's board apart, and each beast's
        on it; a peace offering verse shows only what the peace offering's
        law has named so far of its beast. The shares sidebar is the
        board's own."""
        beast = getattr(verse, "beast", "") or "bull"
        if key.startswith("B.share"):
            return key
        return f"{key}@{offering_of(getattr(verse, 'ref', None))}:{beast}"

    def _shows(self, ctx, key):
        """Is `key` drawn on this file's board: lit here, or before on this
        offering's board of this beast."""
        return key in ctx.lit or self.pkey(key, ctx) in ctx.before

    def base(self, ctx):
        b = self.board(ctx)
        sheet = F.parts_palette(TEXT, PANEL, RED)
        hid = b.hidden()
        out = [self.card()]
        for key in F.BEAST_PART_ORDER:
            if key in b.parts and key != "pieces":
                parts = [p for i, p in enumerate(b.parts[key]) if (key, i) not in hid]
                if parts:
                    out.append(ctx.figure(parts, b.X0, b.G, b.k, TEXT, PANEL,
                                          flip=-1, style=sheet))
        return "".join(out)

    def targets(self, ctx):
        b = self.board(ctx)
        T = {}
        for key in list(b.chips):
            def draw(c, t, key=key):
                (x, y), anc = b.chip_xy(key)
                out = ""
                if key == "pieces":
                    out += "".join(trace(ln, TEXT, 2.6, None if t is None else t + i * 0.1, 0.5)
                                   for i, ln in enumerate(b.lines["pieces"]))
                if key in CHIPLESS and self._shows(c, "B.kidney_fat"):
                    return out          # one word for the part: "fat by the loins"
                lead = b.anchor[key]
                # the words of the verse that named it (leviticus17_spec.CUT_WORDS)
                fk = c.ref if f"B.{key}" in c.lit else getattr(c, "first_lit", {}).get(
                    self.pkey(f"B.{key}", c), c.ref)
                import leviticus17_spec as SPEC
                word = SPEC.CUT_WORDS.get(tuple(fk[:2]), {}).get(key) or _cut_label(key)
                return out + c.chip(f"B.{key}", word, (x, y), anchor=anc,
                                    lead=lead, t=t)
            T[f"B.{key}"] = Target(f"B.{key}", outline=b.outline(key), draw=draw,
                                   box=b.frame([key], 0))
        # water on the innards and the legs (1:9, 13)
        waves = []
        ix, iy = b.anchor["innards"]
        for dy in (-10, 6):
            waves.append([(ix - 50 + k * 8, iy + dy + (4 if k % 2 else -4)) for k in range(13)])
        lx, ly = b.anchor["legs"]
        for dx in (-26, 6):
            waves.append([(lx + dx + k * 6, ly + (3 if k % 2 else -3)) for k in range(7)])
        T["B.water"] = Target("B.water", box=union_box([bounds(w_) for w_ in waves]),
                              draw=lambda c, t: "".join(
                                  trace(w_, WATER, 3, None if t is None else t + i * 0.2, 0.7)
                                  for i, w_ in enumerate(waves)))
        # the shares' sidebar (7:30-34)
        def altar(c, t):
            return appear(c.figure(F.altar("horned", fire=True), B_SIDE_X, 230, 0.62,
                                   BRONZE, PANEL), t)
        T["B.share_altar"] = Target("B.share_altar", box=(B_SIDE_X - 55, 145, B_SIDE_X + 55, 232),
                                    draw=altar)

        def priests(c, t):
            return (appear(c.figure(F.priest(), B_SIDE_X - 34, 520, 1.15, TEXT, PANEL)
                           + c.figure(F.priest(), B_SIDE_X + 34, 520, 1.15, TEXT, PANEL), t)
                    + c.chip("B.share_priests", "Aaron and his sons", (B_SIDE_X - 10, 548),
                             size=14, t=t))
        T["B.share_priests"] = Target("B.share_priests",
                                      box=(B_SIDE_X - 60, 396, B_SIDE_X + 60, 520),
                                      draw=priests)
        # a move's end state from an earlier verse of this board (7:30-36):
        # B.up:<part>[:<chip>] held up, B.at:<share>:<part> at its share
        suffix = "@" + self.pkey("", ctx).split("@", 1)[1]
        held = [pk[:-len(suffix)] for pk in sorted(ctx.before)
                if pk.endswith(suffix) and pk.startswith(("B.up:", "B.at:"))]
        for key in held:
            T[key] = Target(key, box=(0, 0, 1, 1),
                            draw=lambda c, t, key=key, held=held: self._held(c, key, held))
        # B.chip:<word>: a word of this verse ("forever"), bottom left
        words = sorted((tt, k) for k, tt in ctx.lit.items() if k.startswith("B.chip:"))
        for i, (_tt, key) in enumerate(words[:len(B_CHIP_AT)]):
            xy = B_CHIP_AT[i]
            T[key] = Target(key, box=text_box(key[7:], xy, CHIP_PX),
                            draw=lambda c, t, key=key, xy=xy: c.chip(key, key[7:], xy, t=t))
        return T

    def _piece(self, b, key):
        """A part's own fills, drawn lifted off the board, with its look."""
        polys = (b.polys.get(key) or [p for k_ in b.fat_keys for p in b.polys[k_]][:1])
        col, k = B_LOOK.get(key, (RED, .72))
        return "".join(f'<polygon points="{pts_str(p)}" fill="{rgb(mix(PANEL, col, k))}" '
                       f'stroke="{rgb(HL)}" stroke-width="2"/>' for p in polys),             union_box([bounds(p) for p in polys])

    def moved(self, key, opts):
        part = key[2:]
        if "to" in opts:
            return f"B.at:{opts['to']}:{part}"
        return f"B.up:{part}" + (f":{opts['chip']}" if opts.get("chip") else "")

    UP = 46

    def _up_chip_xy(self, part, box):
        x0, y0, x1, y1 = box
        cy = (y0 + y1) / 2
        return (((x0 - 16, cy - self.UP), "rm") if part == "breast"
                else (((x0 + x1) / 2, y0 - self.UP - 24), "mm"))

    def _held(self, ctx, key, held):
        """A part as an earlier move left it: held up with its chip, or a
        small copy at its share; it fades when this verse moves it again,
        and a part held up is gone once it has gone to a share."""
        b = self.board(ctx)
        kind, rest = key.split(":", 1)
        if kind == "B.up":
            part, _, chip = rest.partition(":")
            if any(h.startswith("B.at:") and h.endswith(":" + part) for h in held):
                return ""
            piece, box = self._piece(b, part)
            out = f'<g transform="translate(0 {-self.UP})">{piece}</g>'
            if chip:
                xy, anc = self._up_chip_xy(part, box)
                out += ctx.chip(f"B.up:{part}:{chip}", chip, xy, anchor=anc)
        else:
            to, part = rest.split(":", 1)
            piece, (x0, y0, x1, y1) = self._piece(b, part)
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
            tx, ty = B_TO[to]
            out = (f'<g transform="translate({_fmt(tx)} {_fmt(ty)})"><g transform="scale(0.4)">'
                   f'<g transform="translate({_fmt(-cx)} {_fmt(-cy)})">{piece}</g></g></g>')
        tm = ctx.moves.get("B." + part)
        return fade_out(out, min(tm), 0.3) if tm else out

    def act(self, ctx, verb, key, t, opts):
        """"move" on a part: with {"to": "altar" | "priests" | "priest"} a
        small copy of it goes to that share (7:31, 33); without, it is lifted
        off the board and held up, the breast waved once before Yahweh
        (7:30), the thigh heaved (7:32); {"chip": word} names it there."""
        if verb != "move":
            return super().act(ctx, verb, key, t, opts)
        b = self.board(ctx)
        part = key[2:]
        piece, (x0, y0, x1, y1) = self._piece(b, part)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        if "to" in opts:
            tx, ty = B_TO[opts["to"]]
            k = 0.4
            small = (f'<g transform="scale({k})"><g transform="translate({_fmt(-cx)} '
                     f'{_fmt(-cy)})">{piece}</g></g>')
            rel = [(0, 0), (tx - cx, ty - cy)]
            return (f'<g opacity="0"><set attributeName="opacity" to="1" begin="{t_s(t)}"/>'
                    f'{fade(t, 0.3)}<g transform="translate({_fmt(cx)} {_fmt(cy)})"><g>'
                    f'{motion(rel, t, 1.4)}{small}</g></g></g>')
        up = self.UP
        sway = ""
        if part == "breast":
            sway = (f'<animateTransform attributeName="transform" type="rotate" '
                    f'values="0;-8;8;-5;0" keyTimes="0;0.25;0.55;0.8;1" '
                    f'begin="{t_s(t + 0.5)}" dur="1.4s" fill="freeze"/>')
        lifted = (f'<g transform="translate(0 0)"><animateTransform attributeName="transform" '
                  f'type="translate" values="0 0;0 {-up}" begin="{t_s(t)}" dur="0.6s" '
                  f'fill="freeze" calcMode="spline" keyTimes="0;1" keySplines="{EASE}"/>'
                  f'<g transform="translate({_fmt(cx)} {_fmt(cy)})"><g>{sway}'
                  f'<g transform="translate({_fmt(-cx)} {_fmt(-cy)})">{piece}</g></g></g></g>')
        out = appear(lifted, t, "fade", 0.3)
        if opts.get("chip"):
            # the breast's word beside it (above it is the title plate's
            # corner at B.breast), the thigh's over it
            xy, anc = self._up_chip_xy(part, (x0, y0, x1, y1))
            out += ctx.chip(f"{key}:{opts['chip']}", opts["chip"], xy, anchor=anc, t=t + 0.5)
        return out


# ---------------------------------------------------------------------------
# C: the cast
# ---------------------------------------------------------------------------

C_GROUND = 500
C_K = 2.75                                   # one scale for every animal and person
C_SLOT_X = {"left": 330, "mid": 690, "right": 928}
C_ANIMALS = {
    "C.ox": ("left", "bull", lambda: F.ox()),
    "C.bull": ("left", "bull", lambda: F.ox()),
    "C.sheep": ("mid", "sheep", lambda: F.sheep()),
    "C.ram": ("mid", "ram", lambda: F.sheep(ram=True)),
    "C.lamb": ("mid", "lamb", lambda: F.sheep(lamb=True)),
    "C.goat": ("right", "goat", lambda: F.goat()),
    "C.fgoat": ("right", "goat", lambda: F.goat(female=True)),
}
# the lamb a step under the sheep: its head ring is the parts board's
# sheep at C_LAMB_K, and svg_figures' lamb (28 units to the sheep's 47) is
# drawn up to match
C_LAMB_K = 0.9
C_LAMB_DRAW = C_LAMB_K * 47.0 / 28.1
# the offerer's pose at each beast's head, so his hand comes down on it:
# (arms, legs, lean)
C_POSE = {"bull": ("reach", "stand", 0), "goat": ("pointdn", "stand", 0),
          "fgoat": ("pointdn", "stand", 0), "sheep": ("pointdn", "kneel2", 20),
          "ram": ("pointdn", "kneel2", 20), "lamb": ("pointdn", "kneel2", 20)}


def _hand_pt(fig):
    """The hand of a pose with the arms forward: its foremost point."""
    return max((q for kind, d, _m in fig if kind in ("fill", "line") for q in d),
               key=lambda q: q[0])


C_BEAST_SLOT = {"bull": "left", "sheep": "mid", "ram": "mid", "lamb": "mid",
                "goat": "right", "fgoat": "right"}
C_BEAST_KEY = {"bull": "C.ox", "sheep": "C.sheep", "ram": "C.ram",
               "lamb": "C.lamb", "goat": "C.goat", "fgoat": "C.fgoat"}


def _c_head(beast):
    """The head's ring and centre on C for the verse's beast (card px)."""
    slot = C_BEAST_SLOT.get(beast, "left")
    X = C_SLOT_X[slot]
    kind = {"lamb": "sheep", "fgoat": "goat"}.get(beast, beast)
    if kind not in F.BEAST_KINDS:
        kind = "bull"
    parts, anchors = F.beast_parts(kind)
    k = C_K * (C_LAMB_K if beast == "lamb" else 1.0)
    head = [d for kk, d, _m in parts["head"] if kk == "fill"]
    big = max(head, key=lambda p: (bounds(p)[2] - bounds(p)[0]) * (bounds(p)[3] - bounds(p)[1]))
    ring = [(X - x * k, C_GROUND - y * k) for x, y in big]
    hx, hy = anchors["head"]
    return ring, (X - hx * k, C_GROUND - hy * k), slot


class Cast(Station):
    key = "C"
    VERSE_LOCAL = ("C.offerer", "C.hand", "C.head", "C.elders", "C.chip:")
    SLOTS = {k: v[0] for k, v in C_ANIMALS.items()}

    def slot_of(self, key, verse=None):
        """Each case's cast is its own (`case_of`): the burnt offering's ram
        and goat aren't beside the peace offering's ox, nor the lamb beside
        the goat of 3:12."""
        sl = self.SLOTS.get(key)
        if sl and verse is not None:
            return f"{sl}@{case_of(getattr(verse, 'ref', None))}"
        return sl

    def targets(self, ctx):
        T = {}
        for key, (slot, kind, mk) in C_ANIMALS.items():
            X = C_SLOT_X[slot]
            parts = mk()
            x0, x1, y0, y1 = F.bbox((parts, 0))

            k_ = C_K * (C_LAMB_DRAW if key == "C.lamb" else 1.0)

            def draw(c, t, parts=parts, X=X, k_=k_):
                return appear(c.figure(parts, X, C_GROUND, k_, TEXT, PANEL, flip=-1), t)
            T[key] = Target(key, box=(X - x1 * k_, C_GROUND - y1 * k_, X - x0 * k_, C_GROUND),
                            outline=[(F.outline(parts, X, C_GROUND, k_, flip=-1), True)],
                            draw=draw)
        beast = ctx.beast or "bull"
        ring, (hx, hy), slot = _c_head(beast)
        T["C.head"] = Target("C.head", outline=[(ring, True)])
        # the offerer stands at the head; his hand goes onto it on its word
        # (his arms "down" cross to "reach")
        arms, legs, lean = C_POSE.get(beast, C_POSE["bull"])
        down = F.side_person(arms="down", legs=legs, lean=lean)
        reach = F.side_person(arms=arms, legs=legs, lean=lean)
        hpx, hpy = _hand_pt(reach)
        ox = hx - hpx * C_K - 15
        hand = (ox + hpx * C_K, C_GROUND - hpy * C_K)
        pbox = (ox - 24, C_GROUND - 97 * C_K, ox + 76, C_GROUND)

        def offerer(c, t):
            fig = c.figure(down, ox, C_GROUND, C_K, TEXT, PANEL)
            th = c.lit.get("C.hand")
            if th is not None:
                fig = fade_out(fig, th, 0.35)
            return appear(fig, t)
        T["C.offerer"] = Target("C.offerer", box=pbox, draw=offerer)

        def hand_draw(c, t):
            if "C.elders" in c.lit:
                return ""                  # the elders' own hands (elders_draw)
            fig = c.figure(reach, ox, C_GROUND, C_K, TEXT, PANEL)
            return appear(fig, t, "fade", 0.35)
        T["C.hand"] = Target("C.hand", box=(hand[0] - 22, hand[1] - 26, hand[0] + 18, hand[1] + 14),
                             outline=[(ellipse_pts(hand[0], hand[1] - 2, 26, 20), True)],
                             draw=hand_draw)
        # the elders (4:15) stand where the offerer would, one behind the
        # other; their hands go onto the head on C.hand's word
        elders = [(ox - 46, C_GROUND - 10, C_K * .92), (ox, C_GROUND, C_K)]

        def elders_draw(c, t):
            th = c.lit.get("C.hand")
            men = "".join(c.figure(down, x, y, k_, TEXT, PANEL) for x, y, k_ in elders)
            out = appear(fade_out(men, th, 0.35) if th is not None else men, t)
            if th is not None:
                out += appear("".join(c.figure(reach, x, y, k_, TEXT, PANEL)
                                      for x, y, k_ in elders), th, "fade", 0.35)
            return out + c.chip("C.elders", "elders", (ox - 30, C_GROUND - 97 * C_K - 40), t=t)
        T["C.elders"] = Target("C.elders", box=(ox - 80, C_GROUND - 97 * C_K, ox + 76, C_GROUND),
                               draw=elders_draw)
        for slot_ in C_SLOT_X:
            for word in ("male", "female", "male or female", "young bull", "lamb", "goat"):
                key = f"C.chip:{slot_}:{word}"
                X = C_SLOT_X[slot_]
                T[key] = Target(key, box=(X - 60, C_GROUND + 18, X + 60, C_GROUND + 50),
                                draw=lambda c, t, key=key, X=X, word=word: c.chip(
                                    key, word, (X - 20, C_GROUND + 36), t=t))
        return T


# ---------------------------------------------------------------------------
# H: the holy place
# ---------------------------------------------------------------------------

HV_K, HV_AT = 1.3, (24, 46)                  # the veil inset
HN_K = 1.6                                   # the altar of incense inset
HN_AT = (800 - (GT.ICX - GT.IX) * HN_K, 470 - (GT.NY1 - GT.IY) * HN_K)


def _hv(p):
    return inset_pt(p, HV_K, HV_AT)


def _hn(p):
    return inset_pt(p, HN_K, HN_AT)


VEIL_R = _hv((GT.IX + 68, GT.IY + 84)) + _hv((GT.IX + 68 + 220, GT.IY + 84 + 150))
DROPS_Y = _hv((0, GT.IY + 84 + 150 + 46))[1] + 34
DROPS_X = [VEIL_R[0] + 18 + i * (VEIL_R[2] - VEIL_R[0] - 36) / 6 for i in range(7)]


class HolyPlace(Station):
    key = "H"

    def base(self, ctx):
        return (self.card() + inset_svg("veil", HV_K, HV_AT)
                + inset_svg("incense", HN_K, HN_AT))

    def targets(self, ctx):
        T = {}
        vr = VEIL_R
        T["H.veil"] = Target("H.veil", outline=[(rect_pts(vr[0] - 4, vr[1] - 4, vr[2] + 4, vr[3] + 4), True)],
                             draw=lambda c, t: c.label("H.veil", "veil", ((vr[0] + vr[2]) / 2, vr[1] - 22),
                                                       17, TEXT, "mm", t=t))

        def drops(c, t):
            out = []
            for i, x in enumerate(DROPS_X):
                ti = None if t is None else t + i * 0.3
                d = (f'<circle cx="{_fmt(x)}" cy="{_fmt(DROPS_Y)}" r="7" fill="{rgb(BLOOD)}"/>')
                out.append(appear(d, ti, "pop", 0.25, about=(x, DROPS_Y)))
                out.append(c.label(f"H.drops:{i + 1}", str(i + 1), (x, DROPS_Y + 26), 17, TEXT,
                                   "mm", t=ti))
            return "".join(out)
        T["H.drops"] = Target("H.drops", box=(DROPS_X[0] - 12, DROPS_Y - 12, DROPS_X[-1] + 12,
                                              DROPS_Y + 40),
                              outline=[(rect_pts(DROPS_X[0] - 16, DROPS_Y - 14, DROPS_X[-1] + 16,
                                                 DROPS_Y + 40), True)], draw=drops)
        nb = _hn((GT.NX0, GT.NY0 - 13)) + _hn((GT.NX0 + GT.NW, GT.NY1))
        T["H.incense"] = Target("H.incense", outline=[(rect_pts(nb[0] - 8, nb[1] - 6, nb[2] + 8, nb[3] + 4),
                                                       True)],
                                draw=lambda c, t: c.label("H.incense", "altar of sweet incense",
                                                          ((nb[0] + nb[2]) / 2, nb[3] + 17), 17,
                                                          TEXT, "mm", t=t))
        horns = []
        for hx0, hy0, hx1, hy1 in GT._incense_horns():
            horns.append([_hn(p) for p in GT.horn_points(hx0, hy0, hx1, hy1,
                                                         -1 if hx0 < GT.NX0 else 1)])

        def horns_draw(c, t):
            return (appear("".join(f'<polygon points="{pts_str(p)}" fill="{rgb(BLOOD)}" '
                                   f'fill-opacity="0.9"/>' for p in horns), t, "fade", 0.6)
                    + c.chip("H.horns", "horns", (nb[2] + 70, nb[1] - 20),
                             lead=horns[1][len(horns[1]) // 2], t=t))
        T["H.horns"] = Target("H.horns", outline=[(p, True) for p in horns], draw=horns_draw)
        return T


# ---------------------------------------------------------------------------
# The registry
# ---------------------------------------------------------------------------

_REG = {}


def registry():
    """{key: Station}: every station, each at its corner from the spec. The
    stub modules are imported here, not at the top, since they import this
    module's API."""
    if _REG:
        return _REG
    import leviticus17_spec as SPEC
    import leviticus17_st_meal as MEAL
    import leviticus17_st_law as LAW
    import leviticus17_st_peace as PEACE
    stations = [Plan(), Altar(), PartsBoard(), Cast(), HolyPlace()]
    stations += MEAL.stations() + LAW.stations() + PEACE.stations()
    for st in stations:
        if st.key in SPEC.STATIONS:
            st.origin = SPEC.STATIONS[st.key]
        _REG[st.key] = st
    return _REG
