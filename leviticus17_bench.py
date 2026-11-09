"""Leviticus 1-7 as a workbench that files: the engine (one timeline, no camera).

The frame never moves. It is a still workshop in three fixed regions:

- STRIP (8, 8, 670, 222): the reference court plan, one world window for the
  whole book (leviticus17_parts: the veil to the gate, then the camp edge and
  the clean place pulled in, not to scale);
- BENCH (8, 238, 670, 330): where each verse's thing is built on its word
  (leviticus17_parts: the pen, the altar, the animal set...);
- DOCK (686, 8, 330, 560): five tabs and the active offering's column of the
  offerings table (leviticus17_dock), which fills on cue words and is filed
  into the real reference table at the end of an offering's section (the
  file view, leviticus17_dock.file_view).

Everything that changes is an element (El) on ONE global timeline: T is
seconds from the start of 1:1 across all 163 files in canonical order. A file
renders every element's state at its start (so file n's first frame is file
n-1's frozen last frame, by construction) and the element's events inside the
file as SMIL, each with its own begin. A range file (leviticus17_spec.RANGES)
is one file whose clock spans its verses: the app leaves the <img> running
across a range's verses (docs/visuals.md, D17), so verse k of a range starts
at the sum of the earlier verses' MP3s; a cue in a later verse of a range is
RANGE_LAG later still, so the clip change's latency can't put a picture ahead
of its word.

SECTION CONTRACT
================

Seven sections build the book, each a module of its own with `build()`:

    s1  leviticus17_wb_s1   1:1-1:17            burnt (the reference section)
    s2  leviticus17_wb_s2   2:1-2:16            meal; files meal in 2:16 (may hold into 3:1)
    s3  leviticus17_wb_s3   3:1-3:17, 4:1-2     peace; files peace in the 4:1-2 range
    s4  leviticus17_wb_s4   4:3-4:35            sin: priest, congregation, ruler, person, lamb
    s5  leviticus17_wb_s5   5:1-5:19, 6:1-6:7-8 sin causes, birds, flour (files sin in 5:13-14);
                                                trespass 5:15-6:7 (files trespass in 6:7-8)
    s6  leviticus17_wb_s6   6:9-7:10            the laws: burnt, meal, sin, trespass, shares
    s7  leviticus17_wb_s7   7:11-7:38           peace law, bans, breast and thigh, 7:37, 7:38

`build_timeline()` imports each module in this order and calls its `build()`
with `OWNER` set to its id; every element a section adds is owned by it. A
section module (a) adds elements and events through the helpers of this
module, leviticus17_parts, leviticus17_dock and leviticus17_art (the
drawings more than one section shows), and (b) may declare `REACH = {...}` /
`EXCUSED = {...}` dicts in its own module, laid over leviticus17_spec's for
the coverage rule. Element keys are global: a section prefixes its own with
its id. A module's `STUB = True` makes the coverage gaps "pending" (a
section being written).

Timing: `cue(c, v, phrase, n=0, d=0.0)` is the global T SAY_LEAD (0.1 s)
before the verse says `phrase` (its nth time, 0-based) plus d; a phrase the
verse doesn't say raises KeyError, so the build fails. `at(c, v, t)` is t s
into the verse's MP3. `limit(c, v)` is the latest an animation may END in the
file holding (c, v) (its last MP3's end - AUDIO_SLACK); `fit(T, want)` is a
duration that ends by it.

The state at every section boundary (the first frame of a section's first
file, and the frozen last frame of its last file):

- STRIP: the plan art and the PLACES named so far (leviticus17_parts.place():
  their chips and marks stay for the book). Nothing else: tokens, blood
  rings and paths, carried things and passing chips are section-owned and
  cleared by the section's end.
- BENCH: empty before 1:5; from 1:7 on, the altar set (the bronze altar, its
  wood and its fire, at rest, opacity 1) and nothing else. A section may hide
  the altar set (parts.altar_out) for a full board but restores it
  (parts.altar_in) by its end.
- DOCK: the five tabs, those named so far named; the BOUNDARY tab active
  (BOUNDARY below: s1 burnt, s2 meal, s3 peace, s4 sin, s5 trespass, s6 meal)
  with its column showing every unit lit so far; no outline (case or steady)
  left on.
- TOP: no file view, except that s2's meal file view may hold across the
  2:16|3:1 seam: it must be gone by 3:1 t = SEAM_RESERVE (1.5 s), and s3
  begins nothing in 3:1 before 1.6 s.

QC (`qc_file`, `qc_run`; a file that fails is not written):
seams (no animation runs across a file's end; a pixel check is the Edge
sampler's job), cues (KeyError; every unit first lit in a verse that cites
it, or REACH, or EXCUSED), the motion budget (0 camera moves; at most
MAX_FLIGHTS chip flights a file, each at most MAX_FLIGHT_PX long; every
travel's peak at most MAX_PEAK px/s; at most one file view a file; one thing
travels at a time and nothing lights up or pulses elsewhere while it does
(in the file view too, while its column glides); at most one region begins
an animation in any REGION_GAP s, unless they share a group; nothing begins after the narration - BEGIN_LIMIT; the last animation ends
AUDIO_SLACK before the file's MP3 ends), text (no overlap, nothing off its
region, nothing under MIN_TEXT px in the workshop; a filing glide's words
clear of the file view's keys at GLIDE_SAMPLES of its way), well-formed XML
(an <img> shows nothing for a file that isn't), size (warn over KB_AIM,
refuse over KB_MAX), and the boundaries above (the book's end included).
Times are checked as the file writes them, to 0.01 s.

Build and check only your verses (the whole timeline is always computed, so
seams are right):

    .venv\\Scripts\\python.exe generate_leviticus17_svg.py --out DIR --only 2:1-2:16
    .venv\\Scripts\\python.exe generate_leviticus17_svg.py --qc-only --only 2:1-2:16

Every helper's API is in the docstrings of leviticus17_parts (strip and
bench), leviticus17_dock (dock and file view) and leviticus17_art (the
shared drawings); leviticus17_wb_s1 is the reference section.
docs/design/leviticus-1-7.md is the design.
"""

import importlib
import math
import re
from xml.sax.saxutils import escape

import generate_leviticus17_svg as G
import leviticus17_spec as SPEC
from generate_tabernacle import (BG, HL, PANEL, SAND_DIM, TEXT, TEXT_DIM)
from svg_map_camera import ink
from svg_surface import FONT_FAMILY, SvgCanvas, _fmt

W, H = 1024, 576
SAY_LEAD = G.SAY_LEAD                 # 0.1 s: a reveal begins this before its word
AUDIO_SLACK = 0.35                    # the last animation ends this before the MP3 does
RANGE_LAG = 0.15                      # a cue in a range's later verse waits this more
EASE = "0.42 0 0.58 1"
EASE_PEAK = 1.724                     # the spline's peak / its mean speed
EASE_IN, EASE_OUT = "0.42 0 1 1", "0 0 0.58 1"     # EASE's halves, for a path through a point

STRIP = (8, 8, 670, 222)
BENCH = (8, 238, 670, 330)
DOCK = (686, 8, 330, 560)
REGIONS = {"strip": STRIP, "bench": BENCH, "dock": DOCK}

# the motion budget (QC)
MAX_FLIGHTS = 3                       # chip flights a file
MAX_FLIGHT_PX = 560                   # a flight's (and a walk's, a bench move's) length
MAX_PEAK = 800                        # px/s, any travel's eased peak
MAX_FILE_VIEWS = 1
REGION_GAP = 0.3                      # one region begins an animation per this
BEGIN_LIMIT = 0.1                     # nothing begins after the narration - this
MIN_TEXT = 11                         # px, the workshop's smallest text
KB_AIM, KB_MAX = 70, 130
SEAM_RESERVE = 1.5                    # s2's file view may hold this far into 3:1

SECTIONS = [
    ("s1", "leviticus17_wb_s1", (1, 1), (1, 17)),
    ("s2", "leviticus17_wb_s2", (2, 1), (2, 16)),
    ("s3", "leviticus17_wb_s3", (3, 1), (4, 2)),
    ("s4", "leviticus17_wb_s4", (4, 3), (4, 35)),
    ("s5", "leviticus17_wb_s5", (5, 1), (6, 8)),
    ("s6", "leviticus17_wb_s6", (6, 9), (7, 10)),
    ("s7", "leviticus17_wb_s7", (7, 11), (7, 38)),
]
# the dock's active tab at each section's end
BOUNDARY = {"s1": "burnt", "s2": "meal", "s3": "peace", "s4": "sin", "s5": "trespass",
            "s6": "meal"}


# ---------------------------------------------------------------------------
# The clock: files, verses and global T
# ---------------------------------------------------------------------------

FILES = G.all_files()
FILE_T0, FILE_DUR, VERSE_T0, VERSE_FILE = {}, {}, {}, {}
_acc = 0.0
for _fk in FILES:
    FILE_T0[_fk] = _acc
    _off = 0.0
    for _cv in G.file_verses(_fk):
        VERSE_T0[_cv] = _acc + _off
        VERSE_FILE[_cv] = _fk
        _off += G.narration(*_cv)
    FILE_DUR[_fk] = _off
    _acc += _off
T_END = _acc
del _acc, _off, _fk, _cv


def file_end(fk):
    return FILE_T0[fk] + FILE_DUR[fk]


def said_T(c, v, phrase, n=0):
    """Global T at which (c, v) says `phrase` (its nth time, 0-based)."""
    lag = RANGE_LAG if G.file_verses(VERSE_FILE[(c, v)])[0] != (c, v) else 0.0
    return VERSE_T0[(c, v)] + G.said(c, v, phrase, n) + lag


CUES = []                       # every cue asked for: (T, (c, v), phrase, n, owner)


def cue(c, v, phrase, n=0, d=0.0):
    """Global T: SAY_LEAD before (c, v) says `phrase` (its nth time, 0-based),
    plus d. KeyError if the verse doesn't say it."""
    T = said_T(c, v, phrase, n) - SAY_LEAD + d
    CUES.append((round(T, 3), (c, v), phrase, n, OWNER))
    return T


def at(c, v, t):
    """Global T, t s into the MP3 of (c, v)."""
    return VERSE_T0[(c, v)] + t


def limit(c, v):
    """The latest an animation may end in the file that holds (c, v)."""
    return file_end(VERSE_FILE[(c, v)]) - AUDIO_SLACK


def file_of(T):
    """The file key playing at global T."""
    lo, hi = 0, len(FILES) - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if FILE_T0[FILES[mid]] <= T + 1e-6:
            lo = mid
        else:
            hi = mid - 1
    return FILES[lo]


def verse_of(T):
    """The verse (c, v) whose MP3 plays at global T."""
    fk = file_of(T)
    out = G.file_verses(fk)[0]
    for cv in G.file_verses(fk):
        if VERSE_T0[cv] <= T + 1e-6:
            out = cv
    return out


def file_limit(T):
    return file_end(file_of(T)) - AUDIO_SLACK


def fit(T, want, least=0.25):
    """A duration from T that ends by its file's limit, as the file writes
    them (begin and dur each to 0.01 s): rounded down."""
    A = FILE_T0[file_of(T)]
    room = file_limit(T) - A - round(T - A, 2)
    return max(least, min(want, math.floor(room * 100 + 1e-6) / 100))


def local(T):
    """(file key, seconds into the file) of a global T."""
    fk = file_of(T)
    return fk, T - FILE_T0[fk]


# ---------------------------------------------------------------------------
# Drawing primitives, measured (Georgia, as svg_map_camera.ink measures it)
# ---------------------------------------------------------------------------

def rgb(c):
    return f"rgb({int(c[0])},{int(c[1])},{int(c[2])})"


def f2(v):
    return _fmt(round(v, 2))


_SVG_H = {"l": "start", "m": "middle", "r": "end"}
_SVG_V = {"t": "text-before-edge", "m": "central", "s": "alphabetic", "b": "text-after-edge"}


def tbox(s, x, y, size, anchor="mm", bold=False, italic=False):
    """The ink box of a word at (x, y)."""
    l, t, r, b = ink(s, size, bold, italic, anchor)
    return (x + l, y + t, x + r, y + b)


def text(s, x, y, size, col=TEXT, anchor="mm", bold=False, italic=False, extra=""):
    a = [f'x="{f2(x)}"', f'y="{f2(y)}"', f'font-size="{_fmt(size)}"',
         f'text-anchor="{_SVG_H[anchor[0]]}"', f'dominant-baseline="{_SVG_V[anchor[1]]}"',
         f'fill="{rgb(col)}"']
    if bold:
        a.append('font-weight="bold"')
    if italic:
        a.append('font-style="italic"')
    return f'<text {" ".join(a)}{extra}>{escape(s)}</text>'


def halo_text(s, x, y, size, col=TEXT, anchor="mm", bold=False):
    """A word with a halo (the strip's chips): a BG stroke under it."""
    halo = (f' stroke="{rgb(BG)}" stroke-width="3.2" stroke-opacity="0.9" '
            f'stroke-linejoin="round"')
    return (text(s, x, y, size, BG, anchor, bold, extra=halo)
            + text(s, x, y, size, col, anchor, bold))


def chip(s, x, y, size=14, anchor="mm", lead=None, col=TEXT, edge=SAND_DIM):
    """A word on a plate, with a leader to `lead`. Returns (svg, plate box)."""
    x0, y0, x1, y1 = tbox(s, x, y, size, anchor)
    px0, py0, px1, py1 = x0 - 6, y0 - 4, x1 + 6, y1 + 5
    out = ""
    if lead is not None:
        lx = min(max(lead[0], px0 + 4), px1 - 4)
        ly = py1 if lead[1] > py1 else (py0 if lead[1] < py0 else (py0 + py1) / 2)
        if py0 <= lead[1] <= py1:
            lx = px1 if lead[0] > px1 else px0
        out += (f'<line x1="{f2(lx)}" y1="{f2(ly)}" x2="{f2(lead[0])}" y2="{f2(lead[1])}" '
                f'stroke="{rgb(TEXT_DIM)}" stroke-width="1.3"/>'
                f'<circle cx="{f2(lead[0])}" cy="{f2(lead[1])}" r="2.4" fill="{rgb(TEXT_DIM)}"/>')
    out += (f'<rect x="{f2(px0)}" y="{f2(py0)}" width="{f2(px1 - px0)}" height="{f2(py1 - py0)}" '
            f'rx="5" fill="{rgb(BG)}" fill-opacity="0.88" stroke="{rgb(edge)}" stroke-width="1.2"/>')
    out += text(s, x, y, size, col, anchor)
    return out, (px0, py0, px1, py1)


def ring_pts(c, r, n=16):
    return [(c[0] + r * math.cos(2 * math.pi * i / n), c[1] + r * math.sin(2 * math.pi * i / n))
            for i in range(n)]


def pts_str(pts):
    return " ".join(f"{f2(x)},{f2(y)}" for x, y in pts)


def rect_pts(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def box_pts(b, pad=0):
    return rect_pts(b[0] - pad, b[1] - pad, b[2] + pad, b[3] + pad)


def rdp(pts, tol):
    """Ramer-Douglas-Peucker: the points a line needs at `tol` px."""
    pts = list(pts)
    if len(pts) < 4 or tol <= 0:
        return pts
    keep = [False] * len(pts)
    keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        a, b = stack.pop()
        (x0, y0), (x1, y1) = pts[a], pts[b]
        dx, dy = x1 - x0, y1 - y0
        L = math.hypot(dx, dy)
        best, bi = -1.0, -1
        for i in range(a + 1, b):
            px, py = pts[i]
            d = (abs(dy * px - dx * py + x1 * y0 - y1 * x0) / L) if L > 1e-9 else math.hypot(px - x0, py - y0)
            if d > best:
                best, bi = d, i
        if best > tol and bi > 0:
            keep[bi] = True
            stack += [(a, bi), (bi, b)]
    return [p for p, k in zip(pts, keep) if k]


def rdp_closed(pts, tol):
    pts = list(pts)
    if len(pts) < 6:
        return pts
    far = max(range(len(pts)), key=lambda i: math.hypot(pts[i][0] - pts[0][0], pts[i][1] - pts[0][1]))
    a = rdp(pts[:far + 1], tol)
    b = rdp(pts[far:] + pts[:1], tol)
    out = a[:-1] + b[:-1]
    return out if len(out) >= 3 else pts


class LeanCanvas(SvgCanvas):
    """An SvgCanvas whose polygons and polylines keep only the points they
    need at `tol` px (in the canvas's own units)."""

    def __init__(self, tol=0.3):
        super().__init__(10, 10)
        self.tol = tol

    def polygon(self, points, fill=None, stroke=None, width=1):
        return super().polygon(rdp_closed(points, self.tol), fill, stroke, width)

    def polyline(self, points, stroke, width=1, dash=None, closed=False, fill=None,
                 linejoin="round"):
        pts = rdp_closed(points, self.tol) if closed else rdp(points, self.tol)
        return super().polyline(pts, stroke, width, dash, closed, fill, linejoin)


def fig(parts, x, gy, s, ink_=TEXT, page=PANEL, flip=1, style=None, tol=0.3):
    """svg_figures parts drawn at (x, ground gy), scale s."""
    import svg_figures as F
    c = LeanCanvas(tol)
    F.draw(c, parts, x, gy, s, ink_, page, flip=flip, style=style)
    return "".join(c._els)


def slab(x0, y0, x1, y1, fill, stroke=TEXT, r=4):
    return (f'<rect x="{f2(x0)}" y="{f2(y0)}" width="{f2(x1 - x0)}" height="{f2(y1 - y0)}" '
            f'rx="{r}" fill="{rgb(fill)}" stroke="{rgb(stroke)}" stroke-width="1.3"/>')


def steady_svg(pts, col=HL, width=2.0, op=0.85, closed=True):
    tag = "polygon" if closed else "polyline"
    return (f'<{tag} points="{pts_str(pts)}" fill="none" stroke="{rgb(col)}" '
            f'stroke-width="{width}" stroke-opacity="{op}" stroke-linejoin="round"/>')


DEFS = {}                       # id -> svg, put in a file's <defs> when it uses it


def define(did, svg):
    """A shared drawing (<use href="#did">); the first definition wins."""
    if did not in DEFS:
        DEFS[did] = f'<g id="{did}">{svg}</g>'
    return did


def use(did, x=0.0, y=0.0):
    return f'<use href="#{did}" transform="translate({f2(x)} {f2(y)})"/>'


# ---------------------------------------------------------------------------
# The timeline: elements and their events
# ---------------------------------------------------------------------------

KINDS = ("in", "out", "dim", "hide", "show", "move", "flare", "glide")
OWNER = "engine"                # the section building now (set by build_timeline)


class El:
    """One thing on screen, on the global timeline.

    `svg` is its drawing at its base place (or a callable returning it, drawn
    at render time, after every section has built); `region` is "strip",
    "bench", "dock", "top" (the file view) or "base"; `z` orders it; `texts`
    [(box, size, what)] are its words, for the text QC; `off0` an offset it
    starts at; `hidden0` that it starts unseen though its first event isn't
    an "in". `trace` (T, dur, fn(begin) -> svg) draws a line on instead of
    fading it in (traced_el); `transient` (T, fn(begin) -> svg) is drawn only
    in its own file (a pulse, pulse_el). `parent` puts it inside a group
    element (the dock's columns), whose opacity it then shares. `keep`
    marks what may outlive its section (the altar set, places, lit units).

    Events (global T): in, out (fades, dur), dim (to=level), hide, show
    (instant), move (path relative to its offset now, quad=True for a
    quadratic arc; it keeps the end offset), flare (about=(x, y), k), glide
    (the file view's column: from, to, k, hold). "in" takes how="lift"
    (lift=px) or how="grow" (about=(x, y)). An event's `group` names what it
    belongs to, for the 0.3 s region rule (a link pulse and its unveil share
    one)."""

    def __init__(self, key, region, svg="", z=0, texts=(), off0=(0.0, 0.0),
                 trace=None, transient=None, hidden0=False, keep=False):
        if region not in ("strip", "bench", "dock", "top", "base"):
            raise ValueError(f"{key}: no region {region!r}")
        self.key, self.region, self._svg, self.z = key, region, svg, z
        self.hidden0 = hidden0
        self.texts = list(texts)
        self.off0 = (round(off0[0], 1), round(off0[1], 1))
        self.trace = trace
        self.transient = transient
        self.events = []
        self.children = []
        self.parent = None
        self.keep = keep
        self.owner = OWNER
        self.order = 0

    @property
    def svg(self):
        return self._svg() if callable(self._svg) else self._svg

    def ev(self, kind, T, dur=0.0, group=None, **kw):
        if kind not in KINDS:
            raise ValueError(f"{self.key}: no event {kind!r}")
        if self.transient:
            raise ValueError(f"{self.key}: a transient takes no events")
        if "path" in kw:            # tenths, as the written file keeps a translate
            kw["path"] = [(round(x, 1), round(y, 1)) for x, y in kw["path"]]
        e = dict(kind=kind, T=T, dur=dur, group=group or self.key, owner=OWNER, **kw)
        self.events.append(e)
        self.events.sort(key=lambda e: e["T"])
        return self

    def initially_visible(self):
        if self.trace or self.transient or self.hidden0:
            return False
        for e in self.events:
            if e["kind"] in ("in", "show"):
                return False
            if e["kind"] in ("out", "hide"):
                return True
        return True

    def state(self, T):
        """(visible, level, offset) once every event before T is done."""
        vis = self.initially_visible()
        lev, (dx, dy) = 1.0, self.off0
        if self.trace and self.trace[0] < T - 1e-9:
            vis = True
        if self.transient:
            return False, 1.0, (dx, dy)
        for e in self.events:
            if e["T"] >= T - 1e-9:
                break
            k = e["kind"]
            if k in ("in", "show"):
                vis = True
            elif k in ("out", "hide"):
                vis = False
            elif k == "dim":
                lev = e["to"]
            elif k == "move":
                ex, ey = e["path"][-1]
                dx, dy = dx + ex, dy + ey
        return vis, lev, (dx, dy)

    def seen(self, T):
        """Visible at T (once its events before T are done), through its
        parents, at a level of half or more."""
        el = self
        while el is not None:
            vis, lev, _o = el.state(T)
            if not vis or lev < 0.5:
                return False
            el = ELS[el.parent] if el.parent else None
        return True


ELS = {}


def add(el, parent=None):
    """Register an element (inside the group element `parent`, if given)."""
    if el.key in ELS:
        raise KeyError(f"an element {el.key!r} exists already")
    el.order = len(ELS)
    ELS[el.key] = el
    if parent is not None:
        p = ELS[parent]
        p.children.append(el)
        el.parent = parent
        if el.region != p.region:
            raise ValueError(f"{el.key}: region {el.region} inside {p.region}")
    return el


def get(key):
    return ELS[key]


def t_s(t):
    return f"{max(0.0, t):.2f}s"


def spline_anim(attr, values, begin, dur, extra=""):
    return (f'<animate attributeName="{attr}" values="{values}" begin="{t_s(begin)}" '
            f'dur="{dur:.2f}s" fill="freeze" calcMode="spline" keyTimes="0;1" '
            f'keySplines="{EASE}"{extra}/>')


def arc_path(p0, p1, bow=0.18):
    """A shallow arc from p0 to p1 (relative pts): a quadratic bowed up."""
    (x0, y0), (x1, y1) = p0, p1
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy) or 1
    nx, ny = dy / L, -dx / L
    if ny > 0:
        nx, ny = -nx, -ny
    cx, cy = mx + nx * L * bow, my + ny * L * bow
    return [(x0, y0), (cx, cy), (x1, y1)]


def path_len(path, quad=None):
    if quad is None:
        quad = len(path) == 3
    if quad:
        (x0, y0), (cx, cy), (x1, y1) = path
        n, L, px, py = 40, 0.0, x0, y0
        for i in range(1, n + 1):
            t = i / n
            x = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t * t * x1
            y = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t * t * y1
            L += math.hypot(x - px, y - py)
            px, py = x, y
        return L
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(path, path[1:]))


def path_d(path, quad):
    if quad:
        (x0, y0), (cx, cy), (x1, y1) = path
        return f"M{f2(x0)} {f2(y0)} Q{f2(cx)} {f2(cy)} {f2(x1)} {f2(y1)}"
    return "M" + " L".join(f"{f2(x)} {f2(y)}" for x, y in path)


def _in_file(T, A, B):
    return A - 1e-9 <= T < B - 1e-9


def render_el(el, A, B):
    """The element's SVG for the file [A, B), or "" if not seen in it."""
    loc = lambda T: T - A                       # noqa: E731
    if el.transient:
        T, fn = el.transient
        return fn(loc(T)) if _in_file(T, A, B) else ""
    vis0, lev0, off0 = el.state(A)
    evs = [e for e in el.events if _in_file(e["T"], A, B)]
    traced_here = el.trace and _in_file(el.trace[0], A, B)
    if not vis0 and not traced_here and not any(e["kind"] in ("in", "show") for e in evs):
        return ""
    if el.children:
        kids = sorted(el.children, key=lambda e: (e.z, e.order))
        inner = el.svg + "".join(render_el(k, A, B) for k in kids)
    else:
        inner = el.trace[2](loc(el.trace[0])) if traced_here else el.svg
    if traced_here:
        vis0 = True                 # the trace is its own reveal
    for e in evs:
        if e["kind"] == "flare":
            fx, fy = e["about"]
            k = e.get("k", 1.3)
            inner = (f'<g transform="translate({f2(fx)} {f2(fy)})"><g>'
                     f'<animateTransform attributeName="transform" type="scale" '
                     f'values="1 1;{k} {k};1 1" keyTimes="0;0.4;1" begin="{t_s(loc(e["T"]))}" '
                     f'dur="{e["dur"]:.2f}s" fill="freeze" calcMode="spline" '
                     f'keySplines="{EASE};{EASE}"/>'
                     f'<g transform="translate({f2(-fx)} {f2(-fy)})">{inner}</g></g></g>')
    moves = [e for e in evs if e["kind"] == "move"]
    for e in reversed(moves):
        quad = e.get("quad", False)
        inner = (f'<g><animateMotion path="{path_d(e["path"], quad)}" begin="{t_s(loc(e["T"]))}" '
                 f'dur="{e["dur"]:.2f}s" fill="freeze" calcMode="spline" keyPoints="0;1" '
                 f'keyTimes="0;1" keySplines="{EASE}"/>{inner}</g>')
    for e in evs:
        if e["kind"] == "glide":
            (x0, y0), (x1, y1), k = e["from"], e["to"], e["k"]
            b, d = t_s(loc(e["T"])), f'{e["dur"]:.2f}s'
            sc = (f'values="1;{k};{k}" begin="{b}" dur="{d}" fill="freeze" calcMode="spline" '
                  f'keyTimes="0;{e["scale_by"]:.3f};1" keySplines="{EASE};0 0 1 1"'
                  if e.get("scale_by") else
                  f'values="1;1;{k}" begin="{b}" dur="{d}" fill="freeze" calcMode="spline" '
                  f'keyTimes="0;0.5;1" keySplines="0 0 1 1;{EASE}"' if e.get("hold") else
                  f'values="1;{k}" begin="{b}" dur="{d}" fill="freeze" calcMode="spline" '
                  f'keyTimes="0;1" keySplines="{EASE}"')
            if e.get("via"):            # eased in to the point, out from it, one speed
                (xv, yv), fv_ = e["via"], e["via_at"]
                tr_ = (f'values="{f2(x0)} {f2(y0)};{f2(xv)} {f2(yv)};{f2(x1)} {f2(y1)}" '
                       f'keyTimes="0;{fv_:.3f};1" keySplines="{EASE_IN};{EASE_OUT}"')
            else:
                tr_ = (f'values="{f2(x0)} {f2(y0)};{f2(x1)} {f2(y1)}" keyTimes="0;1" '
                       f'keySplines="{EASE}"')
            inner = (f'<g transform="translate({f2(x0)} {f2(y0)})">'
                     f'<animateTransform attributeName="transform" type="translate" '
                     f'{tr_} begin="{b}" dur="{d}" fill="freeze" calcMode="spline"/>'
                     f'<g><animateTransform attributeName="transform" type="scale" {sc}/>'
                     f'<g transform="translate({f2(-x0)} {f2(-y0)})">{inner}</g></g></g>')
        if e["kind"] == "in" and e.get("how") == "lift":
            lift = e.get("lift", 8)
            inner = (f'<g transform="translate(0 {lift})"><animateTransform attributeName="transform" '
                     f'type="translate" values="0 {lift};0 0" begin="{t_s(loc(e["T"]))}" '
                     f'dur="{e["dur"]:.2f}s" fill="freeze" calcMode="spline" keyTimes="0;1" '
                     f'keySplines="{EASE}"/>{inner}</g>')
        if e["kind"] == "in" and e.get("how") == "grow":
            gx, gy = e["about"]
            inner = (f'<g transform="translate({f2(gx)} {f2(gy)})"><g transform="scale(1 0.03)">'
                     f'<animateTransform attributeName="transform" type="scale" values="1 0.03;1 1" '
                     f'begin="{t_s(loc(e["T"]))}" dur="{e["dur"]:.2f}s" fill="freeze" '
                     f'calcMode="spline" keyTimes="0;1" keySplines="{EASE}"/>'
                     f'<g transform="translate({f2(-gx)} {f2(-gy)})">{inner}</g></g></g>')
    if off0 != (0, 0) and off0 != (0.0, 0.0):
        inner = f'<g transform="translate({f2(off0[0])} {f2(off0[1])})">{inner}</g>'
    disp0 = lev0 if vis0 else 0.0
    anims = []
    vis, lev = vis0, lev0
    for e in evs:
        k, b = e["kind"], loc(e["T"])
        if k == "in":
            anims.append(spline_anim("opacity", f"{lev if vis else 0:.2f};{lev:.2f}"
                                     if vis else f"0;{lev:.2f}", b, e["dur"]))
            vis = True
        elif k == "out":
            anims.append(spline_anim("opacity", f"{lev if vis else 0:.2f};0", b, e["dur"]))
            vis = False
        elif k == "dim":
            if vis:
                anims.append(spline_anim("opacity", f"{lev:.2f};{e['to']:.2f}", b, e["dur"]))
            lev = e["to"]
        elif k == "hide":
            anims.append(f'<set attributeName="opacity" to="0" begin="{t_s(b)}"/>')
            vis = False
        elif k == "show":
            anims.append(f'<set attributeName="opacity" to="{lev:.2f}" begin="{t_s(b)}"/>')
            vis = True
    if not anims and disp0 >= 0.999:
        return inner
    op = "" if disp0 >= 0.999 else f' opacity="{disp0:.2f}"'
    return f"<g{op}>{''.join(anims)}{inner}</g>"


# -- element helpers ---------------------------------------------------------

def pulse_el(key, region, pts, T, closed=True, col=HL, width=2.4, dur=0.9, group=None,
             z=90, parent=None):
    """One pulse of an outline: up and away, once (it ends unseen, so
    nothing of it crosses a seam)."""
    tag = "polygon" if closed else "polyline"
    pts = rdp_closed(pts, 0.4) if closed else rdp(pts, 0.4)

    def fn(b):
        return (f'<{tag} points="{pts_str(pts)}" fill="none" stroke="{rgb(col)}" '
                f'stroke-width="{width}" stroke-linejoin="round" stroke-opacity="0">'
                f'<animate attributeName="stroke-opacity" values="0;1;0.85;0" '
                f'keyTimes="0;0.3;0.6;1" dur="{dur:.2f}s" begin="{t_s(b)}" fill="freeze" '
                f'calcMode="spline" keySplines="{EASE};{EASE};{EASE}"/></{tag}>')
    el = add(El(key, region, z=z, transient=(T, fn)), parent=parent)
    el.pulse = (T, dur, group or key)
    return el


def steady_el(key, region, pts, T, T_out=None, dur_in=0.4, closed=True, group=None,
              parent=None, z=88):
    """A steady outline ("current again"), faded in at T and out at T_out."""
    el = add(El(key, region, steady_svg(pts, closed=closed), z=z), parent=parent)
    el.ev("in", T, dur_in, group=group)
    if T_out is not None:
        el.ev("out", T_out, 0.4, group=(group + ":out") if group else None)
    return el


def traced_svg(pts, col, width, closed=False, extra=""):
    """A line drawn on by its dash offset. It writes its own stroke-dasharray
    and stroke-dashoffset, so `extra` may carry neither (a second copy of an
    attribute is not well-formed XML, and an <img> refuses the file): fade a
    dashed line in instead."""
    if "stroke-dash" in extra:
        raise ValueError("traced_svg: a traced line can't be dashed (extra has a stroke-dash "
                         "attribute); fade a dashed line in instead")
    p = list(pts) + list(pts[:1]) if closed else list(pts)
    L = sum(math.hypot(q[0] - p_[0], q[1] - p_[1]) for p_, q in zip(p, p[1:]))

    def fn(b, dur):
        return (f'<polyline points="{pts_str(p)}" fill="none" stroke="{rgb(col)}" '
                f'stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round" '
                f'stroke-dasharray="{f2(L)} {f2(L * 4)}" stroke-dashoffset="{f2(L)}"{extra}>'
                f'<animate attributeName="stroke-dashoffset" values="{f2(L)};0" '
                f'dur="{dur:.2f}s" begin="{t_s(b)}" fill="freeze" calcMode="spline" '
                f'keyTimes="0;1" keySplines="{EASE}"/></polyline>')
    # drawn as the trace leaves it (same dashes, offset 0), so a seam matches
    static = (f'<polyline points="{pts_str(p)}" fill="none" stroke="{rgb(col)}" '
              f'stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round" '
              f'stroke-dasharray="{f2(L)} {f2(L * 4)}" stroke-dashoffset="0"{extra}/>')
    return fn, static


def traced_el(key, region, pts, col, width, T, dur, z=40, closed=False, extra="",
              parent=None, keep=False, group=None):
    """A line drawn on from T over dur (blood, cut lines, paths). `group`
    ties the trace to other events for the 0.3 s region rule and a travel
    (a not-mark with the unveil it goes with)."""
    fn, static = traced_svg(pts, col, width, closed, extra)
    el = add(El(key, region, static, z=z, trace=(T, dur, lambda b: fn(b, dur)), keep=keep),
             parent=parent)
    el.trace_group = group or key
    return el


TRAVELS = []                    # dict(file, what, px, dur, peak, kind, T, keys, group)
TRAVEL_KINDS = ("chip flight", "bench move", "token walk", "filing glide")


def travel(T, what, px, dur, kind, keys=(), group=""):
    """Record a travel for the budget (moves made by glide() record
    themselves). A glide through a point (the file view's `via`) eases in to
    it and out from it at one speed, so its peak is EASE_PEAK x its mean
    speed too."""
    if kind not in TRAVEL_KINDS:
        raise ValueError(kind)
    TRAVELS.append(dict(file=file_of(T), what=what, px=round(px, 1), dur=round(dur, 2),
                        peak=round(px * EASE_PEAK / dur, 1) if dur else 0.0, kind=kind, T=T,
                        keys=list(keys), group=group, owner=OWNER))


def glide(el, T, path, dur, what, kind, quad=False, record=True, group=None):
    """Move an element along `path` (relative to its offset now) from T over
    dur; recorded as a travel of `kind` unless record=False. Returns its
    length."""
    el.ev("move", T, dur, path=path, quad=quad, group=group)
    L = path_len(path, quad)
    if record:
        travel(T, what, L, dur, kind, keys=[el.key], group=group or el.key)
    return L


LIT = {}                        # table unit -> global T it was first lit
LIT_BY = {}                     # table unit -> how ("unveil", "flight", "file view")


def mark_lit(unit, T, how):
    if unit not in LIT or T < LIT[unit]:
        LIT[unit] = T
        LIT_BY[unit] = how


def is_lit(unit, T):
    """Lit before T (by any section built so far)."""
    return unit in LIT and LIT[unit] < T - 1e-6


FILE_VIEWS = []                 # (T_in, offering, owner)


# ---------------------------------------------------------------------------
# Building the timeline
# ---------------------------------------------------------------------------

_BUILT = {"ok": False}
SECTION_REACH, SECTION_EXCUSED = {}, {}


def reset():
    global OWNER
    ELS.clear()
    DEFS.clear()
    TRAVELS.clear()
    LIT.clear()
    LIT_BY.clear()
    CUES.clear()
    FILE_VIEWS.clear()
    SECTION_REACH.clear()
    SECTION_EXCUSED.clear()
    OWNER = "engine"
    _BUILT["ok"] = False


def build_timeline(force=False):
    """The whole book's timeline: the regions and the shared furniture
    (leviticus17_dock, leviticus17_parts), then every section in order."""
    global OWNER
    if _BUILT["ok"] and not force:
        return
    import leviticus17_dock as D
    import leviticus17_parts as P
    reset()
    OWNER = "engine"
    P.setup()
    D.setup()
    for sid, modname, _a, _b in SECTIONS:
        OWNER = sid
        mod = importlib.import_module(modname)
        mod.build()
        SECTION_REACH.update(getattr(mod, "REACH", {}))
        SECTION_EXCUSED.update(getattr(mod, "EXCUSED", {}))
    OWNER = "engine"
    _BUILT["ok"] = True


def section_of_file(fk):
    cv = G.file_verses(fk)[0]
    for sid, _m, a, b in SECTIONS:
        if a <= cv <= b:
            return sid
    raise KeyError(fk)


def section_files(sid):
    return [fk for fk in FILES if section_of_file(fk) == sid]


# ---------------------------------------------------------------------------
# Rendering a file
# ---------------------------------------------------------------------------

ROOT_OPEN = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" '
             f'height="{H}" font-family="{FONT_FAMILY}">')


def render_file(fk):
    A, B = FILE_T0[fk], file_end(fk)
    parts = [f'<rect width="{W}" height="{H}" fill="{rgb(BG)}"/>']
    dock, at_ = [], None
    tops = sorted((e for e in ELS.values() if e.parent is None), key=lambda e: (e.z, e.order))
    # an opaque full-frame element (`cover`: the file view's table) shown
    # whole through the file hides everything under it: leave that out
    floor = None
    for el in tops:
        if getattr(el, "cover", False):
            vis, lev, _o = el.state(A)
            if vis and lev >= 0.999 and not any(_in_file(e["T"], A, B) for e in el.events):
                floor = (el.z, el.order)
    if floor is not None:
        tops = [e for e in tops if (e.z, e.order) >= floor]
    for el in tops:
        s = render_el(el, A, B)
        if el.key.startswith("col."):
            if at_ is None:
                at_ = len(parts)
            if s:
                dock.append(s)
            continue
        if s:
            parts.append(s)
    if at_ is not None:
        parts.insert(at_, '<g id="dockcol">' + "".join(dock) + "</g>")
    body = "".join(parts)
    used, todo = set(), set(re.findall(r'href="#([\w-]+)"', body))
    while todo:                             # a def may use another
        d = todo.pop()
        if d in used or d not in DEFS:
            continue
        used.add(d)
        todo |= set(re.findall(r'href="#([\w-]+)"', DEFS[d])) - used
    defs = "".join(DEFS[d] for d in sorted(used))
    svg = ROOT_OPEN + (f"<defs>{defs}</defs>" if defs else "") + body + "</svg>"
    return G.compact(svg)


# ---------------------------------------------------------------------------
# QC
# ---------------------------------------------------------------------------

def _events_in(A, B):
    """Every (T, end, el, kind, group, region) beginning in [A, B)."""
    out = []
    for el in ELS.values():
        if el.transient:
            T = el.transient[0]
            if _in_file(T, A, B):
                T_, dur, grp = el.pulse
                out.append((T, T + dur, el, "pulse", grp, el.region))
            continue
        if el.trace and _in_file(el.trace[0], A, B):
            out.append((el.trace[0], el.trace[0] + el.trace[1], el, "trace",
                        getattr(el, "trace_group", el.key), el.region))
        for e in el.events:
            if _in_file(e["T"], A, B):
                out.append((e["T"], e["T"] + e.get("dur", 0.0), el, e["kind"], e["group"],
                            el.region))
    return out


def last_end(fk):
    A, B = FILE_T0[fk], file_end(fk)
    return max((end - A for _T, end, *_r in _events_in(A, B)), default=0.0)


def region_starts(A, B):
    """Each animation's start: (T, region, group, what). A flight's glide is
    region "flight" (it crosses regions; the travel rules hold it)."""
    out = []
    for T, _end, el, kind, grp, reg in _events_in(A, B):
        if kind in ("hide", "show") and grp == "fileview":
            continue
        if kind == "move" and el.key.startswith("fly."):
            reg = "flight"
        out.append((T, reg, grp, f"{el.key}:{kind}"))
    return sorted(out, key=lambda s: s[0])


def region_problems(fk):
    A, B = FILE_T0[fk], file_end(fk)
    starts = region_starts(A, B)
    bad = []
    for i, (T, reg, grp, what) in enumerate(starts):
        for T2, reg2, grp2, what2 in starts[i + 1:]:
            if T2 - T >= REGION_GAP - 1e-6:
                break
            if reg != reg2 and grp != grp2 and "flight" not in (reg, reg2) \
                    and "base" not in (reg, reg2):
                bad.append(f"regions: {reg} {what} at {T - A:.2f} and {reg2} {what2} "
                           f"{T2 - T:.2f} s later")
    return bad


def text_problems(fk):
    """Words at rest (the file's frozen end, and just after each event) that
    overlap, leave their region, or are under MIN_TEXT px; the smallest."""
    A, B = FILE_T0[fk], file_end(fk)
    times = sorted({B - 0.02} | {min(B - 0.02, T + (end - T) + 0.05)
                                 for T, end, *_r in _events_in(A, B)} | {A + 0.01})
    moving = [(e["T"], e["T"] + e["dur"], el.key) for el in ELS.values() for e in el.events
              if e["kind"] in ("move", "glide") and e["T"] < B and e["T"] + e["dur"] > A]
    problems, sizes = [], []
    tops = [el for el in ELS.values() if el.region == "top" and el.key.endswith(".table")]
    for T in times:
        covered = any(el.seen(T) for el in tops)     # the file view covers the workshop
        live = []
        for el in ELS.values():
            if not el.texts or el.region == "base" or (covered and el.region != "top"):
                continue
            if any(a <= T <= b and k == el.key for a, b, k in moving):
                continue
            if not el.seen(T):
                continue
            off = el.state(T)[2]
            p = el.parent
            while p:
                po = ELS[p].state(T)[2]
                off = (off[0] + po[0], off[1] + po[1])
                p = ELS[p].parent
            for box, size, what in el.texts:
                b = (box[0] + off[0], box[1] + off[1], box[2] + off[0], box[3] + off[1])
                live.append((el.key, b, size, el.region == "top"))
                sizes.append(size)
                if size < MIN_TEXT - 1e-6:
                    problems.append(f"t={T - A:.2f} {el.key} text {size} px < {MIN_TEXT}")
                rg = REGIONS.get(el.region)
                if rg and not el.key.startswith("fly.") and (
                        b[0] < rg[0] + 1 or b[1] < rg[1] + 1 or b[2] > rg[0] + rg[2] - 1
                        or b[3] > rg[1] + rg[3] - 1):
                    problems.append(f"t={T - A:.2f} {el.key} leaves its region "
                                    f"{tuple(round(q) for q in b)}")
        for i in range(len(live)):
            for j in range(i + 1, len(live)):
                a, b = live[i][1], live[j][1]
                if live[i][3] != live[j][3]:
                    continue                    # the top layer over the workshop
                if a[0] < b[2] - 1 and b[0] < a[2] - 1 and a[1] < b[3] - 1 and b[1] < a[3] - 1:
                    ka, kb = live[i][0], live[j][0]
                    if ka == kb:
                        continue
                    problems.append(f"t={T - A:.2f} overlap {ka} / {kb}")
    problems += glide_text_problems(fk)
    return sorted(set(problems)), (min(sizes) if sizes else None)


def eased(u, spline=EASE):
    """A keySpline's progress at time fraction u (the cubic Bezier x -> y)."""
    x1, y1, x2, y2 = (float(q) for q in spline.split())
    lo, hi = 0.0, 1.0
    for _ in range(40):
        s = (lo + hi) / 2
        x = 3 * (1 - s) ** 2 * s * x1 + 3 * (1 - s) * s * s * x2 + s ** 3
        lo, hi = (s, hi) if x < u else (lo, s)
    s = (lo + hi) / 2
    return 3 * (1 - s) ** 2 * s * y1 + 3 * (1 - s) * s * s * y2 + s ** 3


def glide_at(e, u):
    """A filing glide's (translate x, y, scale) at time fraction u."""
    (x0, y0), (x1, y1), k = e["from"], e["to"], e["k"]
    if e.get("via"):
        (xv, yv), f = e["via"], e["via_at"]
        if u <= f:
            p = eased(u / f, EASE_IN)
            tx, ty = x0 + (xv - x0) * p, y0 + (yv - y0) * p
        else:
            p = eased((u - f) / (1 - f), EASE_OUT)
            tx, ty = xv + (x1 - xv) * p, yv + (y1 - yv) * p
    else:
        p = eased(u)
        tx, ty = x0 + (x1 - x0) * p, y0 + (y1 - y0) * p
    if e.get("scale_by"):
        f = e["scale_by"]
        sc = 1 + (k - 1) * eased(u / f) if u < f else k
    elif e.get("hold"):
        sc = 1.0 if u <= 0.5 else 1 + (k - 1) * eased((u - 0.5) / 0.5)
    else:
        sc = 1 + (k - 1) * eased(u)
    return tx, ty, sc


GLIDE_SAMPLES = (0.25, 0.5, 0.75, 0.9)


def glide_text_problems(fk):
    """A filing glide's words against the file view's, at its midpoint and
    three-quarter point: a word drawn over the gliding column may not touch
    its words, and one under it may not peek out beside them (the column's
    panel is opaque, so a word wholly under it is hidden)."""
    import leviticus17_dock as D
    A, B = FILE_T0[fk], file_end(fk)
    out = []
    for gl in ELS.values():
        for e in gl.events:
            if e["kind"] != "glide" or not _in_file(e["T"], A, B):
                continue
            x0, y0 = e["from"]
            for u in GLIDE_SAMPLES:
                T = e["T"] + e["dur"] * u
                tx, ty, sc = glide_at(e, u)

                def M(b):
                    return (tx + sc * (b[0] - x0), ty + sc * (b[1] - y0),
                            tx + sc * (b[2] - x0), ty + sc * (b[3] - y0))
                panel = M((D.D_X0, D.COL_Y, D.D_X0 + D.D_W, D.COL_BOT))
                mine = []                       # the column's words, as they glide
                col = ELS[f"col.{e.get('off')}"] if e.get("off") else None
                for ch in (col.children if col else []):
                    if ch.texts and ch.seen(e["T"] - 0.01):
                        mine += [M(b) for b, _s, _w in ch.texts]
                for el in ELS.values():
                    if el.region != "top" or el is gl or not el.texts or not el.seen(T):
                        continue
                    above = (el.z, el.order) > (gl.z, gl.order)
                    for b, _s, _w in el.texts:
                        inside = (b[0] >= panel[0] and b[1] >= panel[1] and b[2] <= panel[2]
                                  and b[3] <= panel[3])
                        if not above and inside:
                            continue
                        pad = 0 if above else 4
                        for m in mine:
                            if b[0] < m[2] + pad and m[0] < b[2] + pad and b[1] < m[3] + pad \
                                    and m[1] < b[3] + pad:
                                out.append(f"t={T - A:.2f} the gliding column's words touch "
                                           f"{el.key}'s ({'over' if above else 'beside'} it)")
                                break
    return out


def budget_problems(fk):
    A, B = FILE_T0[fk], file_end(fk)
    out = []
    tr = sorted((t for t in TRAVELS if A - 1e-9 <= t["T"] < B - 1e-9), key=lambda t: t["T"])
    flights = [t for t in tr if t["kind"] == "chip flight"]
    if len(flights) > MAX_FLIGHTS:
        out.append(f"{len(flights)} chip flights (at most {MAX_FLIGHTS})")
    for t in tr:
        if t["kind"] != "filing glide" and t["px"] > MAX_FLIGHT_PX + 0.5:
            out.append(f"{t['kind']} '{t['what']}' is {t['px']:.0f} px (at most {MAX_FLIGHT_PX})")
        if t["peak"] > MAX_PEAK + 0.5:
            out.append(f"{t['kind']} '{t['what']}' peaks at {t['peak']:.0f} px/s (at most {MAX_PEAK})")
    fv = [f for f in FILE_VIEWS if A - 1e-9 <= f[0] < B - 1e-9]
    if len(fv) > MAX_FILE_VIEWS:
        out.append(f"{len(fv)} file views (at most {MAX_FILE_VIEWS})")
    for a, b in zip(tr, tr[1:]):
        if b["T"] < a["T"] + a["dur"] - 1e-6:
            out.append(f"two things travel at once: '{a['what']}' / '{b['what']}'")
    # nothing lights up elsewhere while a thing travels
    for t_ in tr:
        a0, a1 = t_["T"], t_["T"] + t_["dur"]
        for el in ELS.values():
            if el.transient:            # a pulse may not begin mid-travel either
                T, _d, grp = el.pulse
                if a0 + 0.05 < T < a1 - 0.05 and grp != t_["group"] \
                        and (el.region != "top" or t_["kind"] == "filing glide"):
                    out.append(f"{el.key} pulse at {T - A:.2f} during the travel '{t_['what']}'")
                continue
            if el.key.startswith(("fly.", "fv.")) or el.key in t_["keys"]:
                continue
            for e in el.events:
                if e["kind"] in ("in", "flare") and e["T"] < a1 - 0.05 and e["T"] + e["dur"] > a0 + 0.05:
                    if e["group"] == t_["group"]:
                        continue
                    # the file view's own crossfades (group "fileview") go with
                    # its glide; anything else in the view lighting up mid-glide
                    # is caught (7:37's WHEN lifts)
                    if el.region == "top" and t_["kind"] != "filing glide":
                        continue
                    out.append(f"{el.key} {e['kind']} at {e['T'] - A:.2f} during the travel "
                               f"'{t_['what']}'")
            if el.trace and a0 + 0.05 < el.trace[0] + el.trace[1] and el.trace[0] < a1 - 0.05 \
                    and getattr(el, "trace_group", el.key) != t_["group"]:
                out.append(f"{el.key} traced during the travel '{t_['what']}'")
    return out


def timing_problems(fk):
    A, B = FILE_T0[fk], file_end(fk)
    out = []
    for T, end, el, kind, grp, reg in _events_in(A, B):
        # as the file writes them: begin and dur each to 0.01 s, against the
        # limit to 0.01 s
        b_w = round(max(0.0, T - A), 2)
        e_w = round(b_w + round(end - T, 2), 2)
        if b_w > round(FILE_DUR[fk] - BEGIN_LIMIT, 2) + 1e-6:
            out.append(f"{el.key} {kind} begins at {b_w:.2f}, after the narration - {BEGIN_LIMIT}")
        if e_w > round(FILE_DUR[fk] - AUDIO_SLACK, 2) + 1e-6:
            out.append(f"{el.key} {kind} ends at {e_w:.2f}, past {FILE_DUR[fk] - AUDIO_SLACK:.2f} "
                       f"(the MP3's end - {AUDIO_SLACK})")
        if T < A - 1e-6:
            out.append(f"{el.key} {kind} begins before the file")
    return out


def boundary_problems():
    """Each section's end against the contract (the module docstring)."""
    import leviticus17_dock as D
    out = []
    for i, (sid, _m, _a, _b) in enumerate(SECTIONS[:-1]):
        files = section_files(sid)
        if not files:
            continue
        B = file_end(files[-1])
        reserve = SEAM_RESERVE if sid == "s2" else 0.0
        for el in ELS.values():
            if el.owner != sid or el.keep or el.transient or el.parent:
                continue
            T = B + (reserve if el.region == "top" else 0.0) - 1e-3
            if el.state(T)[0] or (el.region == "top" and el.state(B + reserve + 1e-3)[0]):
                out.append(f"{sid} leaves {el.key} ({el.region}) on at its end")
        for el in ELS.values():
            if el.parent and el.owner == sid and not el.keep and not el.transient \
                    and el.state(B - 1e-3)[0]:
                out.append(f"{sid} leaves {el.key} (dock) on at its end")
        want = BOUNDARY.get(sid)
        if want and D.active(B - 1e-3) != want:
            out.append(f"{sid} ends with the {D.active(B - 1e-3)} tab active, not {want}")
    # the book's end: under the last file view nothing of the last section's
    # workshop is left on (no case outline, no chip); its top layer stays
    sid = SECTIONS[-1][0]
    for el in ELS.values():
        if el.owner != sid or el.keep or el.transient or el.region == "top":
            continue
        if el.state(T_END - 1e-3)[0]:
            out.append(f"{sid} leaves {el.key} ({el.region}) on at the book's end")
    return out


def seam_problems(fk):
    """By construction a file starts on the state the file before ends on;
    what can break it is an animation still running at a file's end."""
    A, B = FILE_T0[fk], file_end(fk)
    return [f"{el.key} {kind} runs across the file's end ({end - A:.2f} > {B - A:.2f})"
            for T, end, el, kind, *_r in _events_in(A, B) if end > B + 1e-6]


def xml_problems(svg):
    """The file must be well-formed XML: the app shows a verse in an <img>,
    which parses it strictly (an inline sampler forgives, say, a doubled
    attribute; an <img> shows nothing)."""
    import xml.etree.ElementTree as ET
    try:
        ET.fromstring(svg)
    except ET.ParseError as e:
        return [f"not well-formed XML ({e}): an <img> would show nothing"]
    return []


def qc_file(fk, svg):
    probs, warns = [], []
    probs += xml_problems(svg)
    probs += seam_problems(fk)
    probs += timing_problems(fk)
    probs += budget_problems(fk)
    probs += region_problems(fk)
    tp, mt = text_problems(fk)
    probs += tp
    kb = len(svg.encode()) / 1024
    if kb > KB_MAX:
        probs.append(f"{kb:.1f} KB (at most {KB_MAX})")
    elif kb > KB_AIM:
        warns.append(f"{kb:.1f} KB (aim {KB_AIM})")
    for bad in ("clip-path", "<mask", "<filter", "repeatCount"):
        if bad in svg:
            probs.append(f"{bad} in the file")
    A, B = FILE_T0[fk], file_end(fk)
    tr = [t for t in TRAVELS if A - 1e-9 <= t["T"] < B - 1e-9]
    return dict(problems=probs, warnings=warns, kb=round(kb, 1), narr=round(FILE_DUR[fk], 3),
                last_end=round(last_end(fk), 2), min_text=mt,
                flights=sum(1 for t in tr if t["kind"] == "chip flight"),
                travels=[(t["kind"], t["px"], t["dur"], t["peak"], t["what"]) for t in tr],
                file_views=sum(1 for f in FILE_VIEWS if A - 1e-9 <= f[0] < B - 1e-9),
                section=section_of_file(fk))


def reach_tables():
    reach = dict(SPEC.REACH)
    reach.update(SECTION_REACH)
    excused = dict(SPEC.EXCUSED)
    excused.update(SECTION_EXCUSED)
    return reach, excused


def coverage():
    """(problems, pending, warnings): every table unit lit by the end of 7:37,
    first in a verse that cites it (or its REACH, or EXCUSED as a whole unit);
    a cited verse whose file doesn't light, pulse or outline its unit is a
    warning. Units still unlit while a section is a stub are pending."""
    reach, excused = reach_tables()
    units = G.table_units()
    stubs = [sid for sid, m, _a, _b in SECTIONS
             if getattr(importlib.import_module(m), "STUB", False)]
    probs, pending, warns = [], [], []
    end737 = file_end(VERSE_FILE[(7, 37)])
    for key, u in units.items():
        T = LIT.get(key)
        if T is None:
            (pending if stubs else probs).append(f"{key} is never lit")
            continue
        if T > end737:
            probs.append(f"{key} first lit after 7:37")
        cv = verse_of(T + SAY_LEAD + 0.01)        # a reveal leads its word by SAY_LEAD
        base = key.removesuffix("/who")
        want = reach.get(key) or (reach.get(base) if key.endswith("/who") else None)
        ok = (cv == want) if want else (cv in u.refs)
        if not ok and key not in excused and base not in excused:
            msg = (f"{key} first lit at {cv[0]}:{cv[1]}, but "
                   + (f"its REACH is {want[0]}:{want[1]}" if want else
                      f"its row cites {', '.join(f'{c}:{v}' for c, v in u.refs)}"))
            (pending if stubs else probs).append(msg)
    for k in excused:
        unit = k[0] if isinstance(k, tuple) else k
        if unit not in units:
            probs.append(f"EXCUSED names {unit!r}, which is no unit")
    return probs, pending, warns, stubs


def run_report(reports, full):
    out = dict(boundaries=boundary_problems())
    probs, pending, warns, stubs = coverage()
    out.update(coverage=probs if full else [], pending=pending, stubs=stubs)
    return out
