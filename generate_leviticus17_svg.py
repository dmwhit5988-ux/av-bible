"""Leviticus 1-7, the offerings: one camera over one sheet, a file a verse.

The sheet (world px, where 1 world px is 1 screen px at s = 1):

- the Tabernacle reference page's court plan, drawn by
  generate_tabernacle_reference.draw_court, draw_tent and draw_furnishings
  at the reference's own coordinates (sanctuary.Plan(730, 440, 14)), with
  the Leviticus layer over it (the camp edge, the north side, the place of
  the ashes, the clean place, the blood ring and paths, the tokens:
  leviticus17_stations.Plan);
- the reference's offerings table, drawn by draw_offerings as it is, with a
  veil over each unit (a name, a by-line, an entry, a who-line, a drawn
  thing, a sin offering rank's line) computed from the reference's own
  layout (entries, ranks, OFF_ROWS, offer_columns and its constants); a
  unit's veil fades on the word of the verse that lights it;
- the stations (leviticus17_stations), screen-sized cards round them.

The verse plan is leviticus17_spec (its docstring has the format). Each
file starts where the file before it ends, so the whole run is one flight;
the chain and every piece of state (what is reached, what is drawn, the
title) are worked out from the spec in canonical order, so any subset
renders as the whole run would. Beats are timed by narration_clock on the
WEB text and the MP3 (the 1.2 s + words / 3.5 s estimate without one); a
cue the verse doesn't say fails the build.

The camera: one lens. Every rest is at s LENS (leviticus17_spec: a
station's whole card, the plan's two homes, the table's six), so a leg
between two rests is a plain eased pan; only 7:37 (out to the whole table,
s 0.45) and 7:38 (back in to Sinai) zoom. A leg is timed by `lev_duration`:
long enough that its peak stays under PAN_PEAK_PX_S on screen (a zoom's
under ZOOM_PEAK_PX_S), PAN_MAX_D at most.

The seams: a file waits on its first camera (`plans`: the opening hold)
until the file before's last stop has rested LAST_REST, and what the file
before drew that this file doesn't (a verse's chip or token, a case's stack,
a pulse still running) is carried into its first frame with its times
shifted back, and fades as the camera first moves (`Carry`).

QC (a file that fails is not written; the report says why):
- the lens: a rest off LENS (but LENS_EXEMPT's), a leg between two LENS
  rests that isn't a pure pan, more than MAX_LEGS legs, more than
  MAX_FILE_PAN screen widths of pan (at the wider end) or MAX_FILE_ZOOM
  octaves of zoom in a file, a leg over MAX_LEG_PAN widths or faster than
  MAX_PEAK_PX_S on screen (its fastest corner, sampled 60/s) is refused; a
  leg over PAN_PEAK_PX_S, or a seam whose rest (the file before's last
  stop and this file's opening hold) is under LAST_REST, is a warning;
- no animation begins after the narration (- 0.1 s);
- it lands AUDIO_SLACK (0.35 s) before its MP3 ends, and a verse under 5 s
  has one stop, up to 10 s two, three only above;
- no word overlaps another, runs off the frame or sits under the title
  plate at a rest; words of the stop's own beats are wholly in the frame;
- no word at a rest is cut by the frame's edge: the stations' and the
  plan's words, the reference plan's own labels (draw_court, draw_tent,
  draw_furnishings) and the table's words once unveiled;
- at most 1,050 rects and 268 texts; no clip, mask or filter;

Size: the written file is compacted (`compact`): polygons and polylines
become relative paths at a tenth of a px, colours hex, runs of unfilled
lines of one paint one path; the camera and its screen-constant attributes
share one decimated keyframe list (`CamOut`); the veils that stay are
three shapes; a card's shapes that no camera of the file sees are culled
(`cull_card`), and so are B's that later fills cover. The report's
"sections" give the bytes by part of the sheet.
- the run as a whole (`--qc-only` over everything): every unit reached by
  7:37, each first reach in a verse that cites it (or REACH,
  REACHED_OFFSCREEN, EXCUSED), every verse planned.

    .venv\\Scripts\\python.exe generate_leviticus17_svg.py --out DIR
        [--only 1:1-1:17,3:4] [--verses-extra scratch.py] [--qc-only]
    .venv\\Scripts\\python.exe generate_leviticus17_svg.py --web

It writes into web/visuals only with --web.
"""

import argparse
import functools
import importlib.util
import math
import os
import re
import sys
from xml.sax.saxutils import escape

import config
import narration_clock
import offerings as OF
import passages
import sanctuary as SN
import verse_refs
import generate_tabernacle as GT
import generate_tabernacle_reference as R
import leviticus17_spec as SPEC
import leviticus17_stations as ST
from generate_tabernacle import (BG, HL, PANEL, SAND_DIM, TEXT, TEXT_DIM, W,
                                 H)
from svg_chronicles_world import AUDIO_SLACK, _mp3_seconds
from svg_map_camera import (Flight, Leg, cam_T, cam_duration, fade, ink, title_rect,
                            title_svg, to_screen, visible_world)
from svg_surface import FONT_FAMILY, SvgCanvas, _fmt

BOOK = SPEC.BOOK
SAY_LEAD = 0.1
VEIL_OP = 1.0           # a veiled unit hides its words; a faint bar marks the place
SKELETON = (44, 44, 58)  # the bar, a step off the panel
VEIL_FADE = 0.5
MIN_LEG = 1.2           # a move never quicker than this
MIN_LEG_SQUEEZE = 0.6   # unless the verse can't afford it
SQUEEZE_PEAK_PX_S = 1750  # nor so quick a pan peaks above this on screen
DWELL = 1.3             # the least rest at a stop before moving on
AFTER_WORD = 0.7        # time a beat gets before the camera leaves
NEEDS = {"light": 1.0, "move": 2.2, "flare": 1.0, "pulse": 0.8, "not": 1.2}
OUTLINE_PX = 2.6
# the pan's pace (lev_duration): its eased peak under PAN_PEAK_PX_S screen
# px/s (the ease's peak is EASE_PEAK times its mean: keySplines EASE's
# slope at its middle, 1.5 / 0.87), PAN_MAX_D s at most
PAN_PEAK_PX_S = 1300
EASE_PEAK = 1.724
PAN_MAX_D = 3.8
# a zoom (7:38's flight back to Sinai) slower still: the whole frame
# scales as it slides
ZOOM_PEAK_PX_S = 1050
# the lens's budgets (qc_file)
LENS_EXEMPT = {"table"}        # the one rest off the lens: 7:37
MAX_LEGS = 3            # legs in a file
MAX_FILE_PAN = 5.5      # screen widths of pan in a file (at the wider end)
MAX_FILE_ZOOM = 1.2     # octaves of zoom in a file
MAX_LEG_PAN = 3.0       # screen widths in one leg
MAX_PEAK_PX_S = 1800    # a leg's fastest on-screen speed (refused above)
SPEED_FPS = 60          # how often the flight is sampled for it
MAX_RECTS, MAX_TEXTS = 1050, 268
SAFE_IN = 4             # px a stop's own words keep from the frame's edge
TABLE_FLY_PX = 24       # a table drawing seen only in flight: kept from this size on screen
FIELDS = {"BROUGHT": "brought", "ON THE ALTAR": "burns", "THE BLOOD": "blood",
          "WHO EATS": "eaten", "NOT EATEN": "not_eaten", "WHEN": "when"}


# ---------------------------------------------------------------------------
# The text and the clock
# ---------------------------------------------------------------------------

def _norm(s):
    return (s.replace("’", "'").replace("‘", "'").replace("“", '"')
            .replace("”", '"'))


@functools.cache
def verse_text(c, v):
    for num, text in passages.load_chapter(BOOK, c).verses:
        if int(num) == v:
            return text
    raise KeyError((c, v))


def _mp3(c, v):
    return os.path.join(str(config.WEB_AUDIO_DIR), f"{BOOK}_{c}_{v}.mp3")


@functools.cache
def narration(c, v):
    """The verse's MP3 length, or the estimate when there's none."""
    d = _mp3_seconds(_mp3(c, v))
    if d:
        return round(d, 3)
    return round(1.2 + len(verse_text(c, v).split()) / 3.5, 2)


@functools.cache
def _clock(c, v):
    try:
        return narration_clock.clock(verse_text(c, v), _mp3(c, v))
    except Exception:
        return None


@functools.cache
def occurrences(c, v, phrase):
    """Where the verse says `phrase`, whole, as character offsets. A capital
    first letter matches that very word; a small one either case."""
    text = _norm(verse_text(c, v))
    words = [re.escape(w) for w in _norm(phrase).split()]
    pat = r"(?<![\w'])" + r"\s+".join(words) + r"(?![\w'])"
    flags = 0 if phrase[:1].isupper() else re.IGNORECASE
    return [m.start() for m in re.finditer(pat, text, flags)]


def said(c, v, phrase, n=0):
    """Seconds into the MP3 when `phrase` (its nth time) is said. KeyError if
    the verse doesn't say it: a misspelt cue must not build."""
    hits = occurrences(c, v, phrase)
    if n >= len(hits):
        raise KeyError(f"Lev {c}:{v} doesn't say {phrase!r}"
                       + (f" {n + 1} times" if n else ""))
    clock = _clock(c, v)
    if clock is not None:
        return clock(hits[n])
    text = verse_text(c, v)
    return narration(c, v) * hits[n] / max(1, len(text))


_CUE = re.compile(r"^(?P<w>[^#+]+?)(?:#(?P<n>\d+))?(?:\+(?P<d>[\d.]+))?$")


def cue_word(cue):
    """(phrase, n, delay) of a word cue, or None for "@", "t=".."""
    if cue.startswith("@") or cue.startswith("t="):
        return None
    m = _CUE.match(cue.strip())
    if not m:
        raise ValueError(f"can't read cue {cue!r}")
    return m["w"].strip(), int(m["n"] or 1) - 1, float(m["d"] or 0)


# ---------------------------------------------------------------------------
# Files and the spec
# ---------------------------------------------------------------------------

def load_verses(extra=None):
    """The spec's VERSES, with a scratch module's VERSES (and REACH,
    EXCUSED, REACHED_OFFSCREEN) laid over it."""
    verses = dict(SPEC.VERSES)
    tables = {"REACH": dict(SPEC.REACH), "EXCUSED": dict(SPEC.EXCUSED),
              "REACHED_OFFSCREEN": dict(SPEC.REACHED_OFFSCREEN)}
    if extra:
        spec = importlib.util.spec_from_file_location("lev17_extra", extra)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        verses.update(getattr(mod, "VERSES", {}))
        for name, d in tables.items():
            d.update(getattr(mod, name, {}))
    return verses, tables


def range_of(c, v):
    for rc, a, b in SPEC.RANGES:
        if rc == c and a <= v <= b:
            return (rc, a, b)
    return None


def all_files():
    """Every file key in canonical order: (c, v) or (c, v1, v2)."""
    out = []
    for c in SPEC.CHAPTERS:
        for v in passages.verse_numbers(BOOK, c):
            r = range_of(c, v)
            if r:
                if v == r[1]:
                    out.append(r)
            else:
                out.append((c, v))
    return out


def file_verses(fk):
    if len(fk) == 3:
        return [(fk[0], v) for v in range(fk[1], fk[2] + 1)]
    return [fk]


def file_name(fk):
    if len(fk) == 3:
        return f"{BOOK}_{fk[0]}_{fk[1]}-{fk[2]}.svg"
    return f"{BOOK}_{fk[0]}_{fk[1]}.svg"


def ref_str(fk):
    return f"{fk[0]}:{fk[1]}" + (f"-{fk[2]}" if len(fk) == 3 else "")


def parse_only(s):
    """'1:1-1:17,3:4' -> the set of (c, v) it names."""
    want = set()
    for part in s.split(","):
        part = part.strip()
        if not part:
            continue
        a, _, b = part.partition("-")
        c1, v1 = map(int, a.split(":"))
        if b:
            c2, v2 = (map(int, b.split(":")) if ":" in b else (c1, int(b)))
        else:
            c2, v2 = c1, v1
        for c in range(c1, c2 + 1):
            for v in passages.verse_numbers(BOOK, c):
                if (c, v) >= (c1, v1) and (c, v) <= (c2, v2):
                    want.add((c, v))
    return want


def lev_verses(ref):
    out = []
    for r in verse_refs.parse(ref, BOOK):
        for book, c, v in r.verses():
            if book == BOOK and 1 <= c <= 7:
                out.append((c, v))
    return out


# ---------------------------------------------------------------------------
# The table's units, from the reference's own layout
# ---------------------------------------------------------------------------

class Unit:
    def __init__(self, key, box, anchor, text, refs):
        self.key, self.box, self.anchor, self.text = key, box, anchor, text
        self.refs = sorted(set(refs))


TY = R.OFF_Y + 80                       # the table frame's top


def row_tops():
    y, out = TY + R.OFF_HEAD, {}
    for lab, _sub, _kind, _content, rh in R.OFF_ROWS:
        out[FIELDS[lab]] = (y, rh)
        y += rh
    return out


def _entries_rows(rs, sub=True):
    """R.entries' grouping, keeping the rows behind each entry."""
    order, rows = [], {}
    for r in rs:
        if not r.short:
            continue
        main, s = r.short, (r.who if sub else "")
        if s in ("every one", "no one", main):
            s = ""
        if (main, s) not in rows:
            order.append((main, s))
            rows[(main, s)] = []
        rows[(main, s)].append(r)
    return [(m, s, rows[(m, s)]) for m, s in order]


@functools.cache
def table_units():
    units = {}
    cols = R.offer_columns()
    tops = row_tops()
    for o in OF.OFFERINGS:
        x = cols[o.key][0]
        names = R.wrap(o.name, 20, R.OFF_CW - 24, bold=True)
        people = dict(o.verses).get("For the people", "")
        refs = lev_verses(people)[:1]
        units[f"{o.key}.head"] = Unit(
            f"{o.key}.head", (x + 8, TY + 6, x + R.OFF_CW - 8, TY + R.OFF_HEAD - 4),
            (x + R.OFF_CW / 2, TY + 36 - 12 * (len(names) - 1)), names[0], refs)
    for field, (y, rh) in tops.items():
        for o in OF.OFFERINGS:
            x = cols[o.key][0] + R.PAD
            right = x + R.CELL_TW + 6
            if field == "brought" and o.by is None:
                yy = y + 16
                groups = []
                for r in o.brought:
                    for g in groups:
                        if g[0] == (r.things, r.short):
                            g[1].append(r)
                            break
                    else:
                        groups.append([(r.things, r.short), [r]])
                width = R.CELL_TW - R.RANK_ICON - 10
                for i, ((things, short), rs) in enumerate(groups, 1):
                    n = len(things)
                    iw = R.RANK_ICON / n
                    for j, key in enumerate(things):
                        th = next(t for t in OF.THINGS[o.key] if t.key == key)
                        units[f"{o.key}.icon{i}:{key}"] = Unit(
                            f"{o.key}.icon{i}:{key}",
                            (x + iw * j + 1, yy, x + iw * (j + 1) - 1, yy + 58),
                            (x + iw * (j + 0.5), yy + 30), key, lev_verses(th.ref))
                    tx, ty = x + R.RANK_ICON + 10, yy
                    for r in rs:
                        lines = R.wrap(r.who, R.SHORT, width)
                        units[f"{o.key}.who:{r.who}"] = Unit(
                            f"{o.key}.who:{r.who}", (tx - 5, ty, right, ty + R.LINE * len(lines) + 1),
                            (tx, ty + 12), lines[0], lev_verses(r.ref))
                        ty += R.LINE * len(lines)
                    subs = R.wrap(short, R.WHO, width, italic=True)
                    refs = [cv for r in rs for cv in lev_verses(r.ref)]
                    units[f"{o.key}.rank{i}"] = Unit(
                        f"{o.key}.rank{i}", (tx - 5, ty, right, ty + R.SUBLINE * len(subs) + 3),
                        (tx, ty + 9), subs[0], refs)
                    n_main = sum(len(R.wrap(r.who, R.SHORT, width)) for r in rs)
                    yy += max(60, R.LINE * n_main + R.SUBLINE * len(subs)) + R.GAP
            elif field == "brought":
                units[f"{o.key}.by"] = Unit(f"{o.key}.by", (x - 6, y + 14, right, y + 40),
                                            (x, y + 28), o.by_short, lev_verses(o.by.ref))
                things = OF.THINGS[o.key]
                per = min(3, len(things))
                slot = R.CELL_TW / per
                for i, t in enumerate(things):
                    r_, k = divmod(i, per)
                    tcx = x + k * slot + slot / 2
                    base = y + 16 + R.LINE + 6 + r_ * R.THING_ROW + 64
                    units[f"{o.key}.thing:{t.key}"] = Unit(
                        f"{o.key}.thing:{t.key}",
                        (tcx - slot / 2 + 2, base - 60, tcx + slot / 2 - 2, base + 34),
                        (tcx, base + 22), t.short or t.key, lev_verses(t.ref))
            elif field == "when":
                units[f"{o.key}.when"] = Unit(f"{o.key}.when", (x - 6, y + 8, right, y + rh - 6),
                                              (x, y + 28), o.when_short,
                                              lev_verses(o.when.ref))
            else:
                es = _entries_rows(getattr(o, field), field != "not_eaten")
                shorts = [m for m, _s, _r in es]
                yy = y + 16
                for main, s, rs in es:
                    mains = R.wrap(main, R.SHORT, R.CELL_TW)
                    subl = R.wrap(s, R.WHO, R.CELL_TW, italic=True) if s else []
                    h = R.LINE * len(mains) + R.SUBLINE * len(subl)
                    key = f"{o.key}.{field}:{main}"
                    if shorts.count(main) > 1:
                        key += f"|{s}"
                    refs = [cv for r in rs for cv in lev_verses(r.ref)]
                    hm = R.LINE * len(mains)
                    units[key] = Unit(key, (x - 6, yy - 1, right, yy + hm + 1), (x, yy + 12),
                                      mains[0], refs)
                    if subl:
                        # its who-line is a unit of its own: it comes with
                        # the entry unless REACH holds it back
                        units[key + "/who"] = Unit(key + "/who", (x - 6, yy + hm + 1, right,
                                                                  yy + h + 3),
                                                   (x, yy + hm + 9), subl[0], refs)
                    yy += h + R.GAP
    return units


class Table(ST.Station):
    """The offerings table's veils: a unit is a target; lighting it fades its
    veil (the first time) and outlines it."""
    key = "table"
    world = True

    def rect(self):
        return (R.OFF_X, R.OFF_Y, R.OFF_X + R.TABLE_W, TY + R.OFF_TABLE_H)

    def shots(self):
        return {}

    def base(self, ctx):
        """The veils that stay all file long, as three shapes: one path of
        panels, one of bars (round-capped strokes, the bars' own shape) and
        the things' discs."""
        panels, bars, discs = [], [], []
        for u in table_units().values():
            if u.key in ctx.before or u.key in ctx.lit:
                continue
            if not ctx.sees(u.box):
                continue
            x0, y0, x1, y1 = u.box
            panels.append(f"M{_fmt(x0)} {_fmt(y0)}h{_fmt(x1 - x0)}v{_fmt(y1 - y0)}"
                          f"h{_fmt(x0 - x1)}z")
            mark = veil_mark(u.box, u.anchor, ".thing:" in u.key or ".icon" in u.key)
            if mark[0] == "disc":
                discs.append(mark[1])
            else:
                bx, by, bw = mark[1]
                if bw > 8:
                    bars.append(f"M{_fmt(bx + 4)} {_fmt(by)}h{_fmt(bw - 8)}")
        out = ""
        if panels:
            out += f'<path d="{"".join(panels)}" fill="{ST.rgb(PANEL)}"/>'
        if bars:
            out += (f'<path d="{"".join(bars)}" fill="none" stroke="{ST.rgb(SKELETON)}" '
                    f'stroke-width="8" stroke-linecap="round"/>')
        if discs:
            out += f'<g fill="{ST.rgb(SKELETON)}">' + "".join(discs) + "</g>"
        return out

    def targets(self, ctx):
        out = {}
        for u in table_units().values():
            x0, y0, x1, y1 = u.box
            out[u.key] = ST.Target(
                u.key, box=u.box, outline=[(ST.rect_pts(x0 - 2, y0 - 2, x1 + 2, y1 + 2), True)],
                draw=lambda c, t, u=u: "" if t is None else veil(
                    u.box, t, u.anchor, ".thing:" in u.key or ".icon" in u.key))
        # 7:37's "consecration", a Leviticus-only chip in the margin right
        # of the trespass header (the table has no column for it)
        xy, size = CONSECRATION
        box = ST.text_box("consecration", xy, size)
        pad = (box[0] - 16, box[1] - 12, box[2] + 16, box[3] + 14)
        out["trespass.consecration"] = ST.Target(
            "trespass.consecration", box=pad,
            outline=[(ST.rect_pts(pad[0] - 4, pad[1] - 4, pad[2] + 4, pad[3] + 4), True)],
            draw=lambda c, t: c.chip("trespass.consecration", "consecration", xy, size, t=t))
        # "<off>.col": a column's frame, an outline only (pulse it)
        for key, (x, y, w, h) in R.offer_columns().items():
            out[f"{key}.col"] = ST.Target(f"{key}.col", outline=[(ST.rect_pts(
                x + 3, y + 3, x + w - 3, y + h - 3), True)])
        return out


CONSECRATION = ((R.OFF_X + R.TABLE_W + 158, TY + 44), 34)


def veil_mark(box, anchor=None, thing=False):
    """Where a veil's faint mark goes: ("disc", its ellipse) for a drawn
    thing, ("bar", (x, y, w)) for words, the bar 8 px high about y."""
    x0, y0, x1, y1 = box
    if thing:
        cx, cy = (x0 + x1) / 2, y0 + (y1 - y0) * 0.38
        return "disc", (f'<ellipse cx="{_fmt(cx)}" cy="{_fmt(cy)}" '
                        f'rx="{_fmt(min(26, (x1 - x0) / 3))}" ry="14"/>')
    ax, ay = anchor if anchor else (x0 + 8, (y0 + y1) / 2)
    if ax > (x0 + x1) / 2 - 20:            # a centred name
        bw = min(150, x1 - x0 - 40)
        bx = ax - bw / 2
    else:
        bx, bw = ax, min(120, x1 - ax - 30)
    return "bar", (bx, ay, bw)


def veil(box, t=None, anchor=None, thing=False):
    """A unit's veil: the panel over it, and a faint bar (or, for a drawn
    thing, a faint disc) where it will be; faded out at t."""
    x0, y0, x1, y1 = box
    rect = (f'<rect x="{_fmt(x0)}" y="{_fmt(y0)}" width="{_fmt(x1 - x0)}" '
            f'height="{_fmt(y1 - y0)}" fill="{ST.rgb(PANEL)}"/>')
    kind, m = veil_mark(box, anchor, thing)
    if kind == "disc":
        mark = m[:-2] + f' fill="{ST.rgb(SKELETON)}"/>'
    else:
        bx, by, bw = m
        mark = (f'<rect x="{_fmt(bx)}" y="{_fmt(by - 4)}" width="{_fmt(bw)}" height="8" '
                f'rx="4" fill="{ST.rgb(SKELETON)}"/>')
    if t is None:
        return f"<g>{rect}{mark}</g>"
    return f'<g>{fade(t, VEIL_FADE, out=True)}{rect}{mark}</g>'


TABLE = Table()


def station_of(key):
    reg = ST.registry()
    pre = key.split(".")[0]
    if pre in reg:
        return reg[pre]
    if pre in OF.OFFERING:
        return TABLE
    raise KeyError(f"no station for target {key!r}")


# ---------------------------------------------------------------------------
# Shots
# ---------------------------------------------------------------------------

def shot_cam(name, beast=""):
    """A spec's shot name -> (s, x, y) in world px: a home of SHOTS, the
    whole table ("table", s 0.45) or a station's whole card ("A", "L", at
    STATION_S). `beast` is kept for the callers; every station's rest is
    the same card whatever its beast."""
    if name in SPEC.SHOTS:
        return SPEC.SHOTS[name]
    if name == "table":
        return (0.45, R.OFF_X - 5 + W / 2 / 0.45, TY + R.OFF_TABLE_H / 2)
    st_key, dot, _sub = name.partition(".")
    st = ST.registry().get(st_key)
    if st is None or st.world:
        raise KeyError(f"no shot {name!r}")
    if dot:
        raise KeyError(f"{name!r}: close-up shots are retired: rest on the whole card")
    _s, x, y = st.shots()[""]
    return (SPEC.STATION_S, x + st.origin[0], y + st.origin[1])


def lev_duration(cam0, cam1):
    """A leg's time: cam_duration's, and long enough that its peak stays
    under PAN_PEAK_PX_S on screen (PAN_MAX_D at most): a pan by its ease's
    peak; a zoom (7:37, 7:38) under ZOOM_PEAK_PX_S, by its van Wijk flight
    sampled SPEED_FPS a second."""
    d = cam_duration(cam0, cam1)
    if not d:
        return d
    if abs(cam0[0] - cam1[0]) < 1e-9:
        travel = math.hypot(cam1[1] - cam0[1], cam1[2] - cam0[2]) * cam0[0]
        return min(PAN_MAX_D, max(d, travel * EASE_PEAK / PAN_PEAK_PX_S))
    leg = Leg(cam0, cam1, d, "zoom")
    n = max(2, math.ceil(d * SPEED_FPS))
    cs = [leg.at(i / n) for i in range(n + 1)]
    peak = max(screen_flow(a, b) for a, b in zip(cs, cs[1:])) / (d / n)
    return min(PAN_MAX_D, max(d, d * peak / ZOOM_PEAK_PX_S))


LAST_REST = 1.5          # a file's last stop rests this long, with the next file's hold

_CHAIN = {}


def plans(verses, extra=None):
    """Every file's schedule (Plan_), in canonical order: each file starts
    on the camera the file before it ends on, and holds it until that
    file's last stop has rested LAST_REST (the next file's opening hold)."""
    got = _CHAIN.get((id(verses), extra))
    if got and got[0] is verses:
        return got[1]
    out, prev, cam = {}, None, shot_cam(SPEC.OPENING)
    for fk in all_files():
        hold = 0.0
        if prev is not None:
            rest = prev.narr - prev.arr[-1] if prev.cams else prev.narr
            hold = max(0.0, round(LAST_REST - rest, 3))
        P = Plan_(fk, verses[fk], cam, hold)
        out[fk] = P
        prev, cam = P, P.cam1
    _CHAIN[(id(verses), extra)] = (verses, out)
    return out


@functools.cache
def file_cams(extra=None):
    """Each file's opening and closing camera, in canonical order: a file
    ends on its last stop, a file with no stops holds where it began."""
    verses, _t = load_verses(extra)
    cam = shot_cam(SPEC.OPENING)
    out = {}
    for fk in all_files():
        V = verses[fk]
        c0 = cam
        for st in V.stops:
            cam = shot_cam(st.shot, V.beast)
        out[fk] = (c0, cam)
    return out


# ---------------------------------------------------------------------------
# State, worked out from the spec in canonical order
# ---------------------------------------------------------------------------

def companions(key, fk, tables):
    """What lights with a unit: an entry's who-line, unless REACH puts it
    in a later verse."""
    w = key + "/who"
    if w not in table_units():
        return []
    at = tables["REACH"].get(w)
    if at and at not in file_verses(fk) and at > file_verses(fk)[0]:
        return []
    return [w]


class FileV:
    """What a station's pkey sees of a file: the spec's V (its beast) and
    the file's ref, so B can keep each offering's board apart."""

    def __init__(self, V, fk):
        self.V, self.ref = V, fk

    def __getattr__(self, name):
        return getattr(self.V, name)


class History:
    def __init__(self, verses, tables):
        self.before, self.slots, self.title_at, self.first_lit = {}, {}, {}, {}
        persisted, slots, title, prev_c = set(), {}, None, None
        off = tables["REACHED_OFFSCREEN"]
        for i, fk in enumerate(all_files()):
            V = verses[fk]
            if fk[0] != prev_c:
                title = f"Leviticus {fk[0]}"
            self.before[fk] = frozenset(persisted)
            self.slots[fk] = dict(slots)
            self.title_at[fk] = title
            for stop in V.stops:
                for beat in stop.beats:
                    verb, key = beat[0], beat[1]
                    if verb == "hud":
                        title = key
                    if verb == "move":
                        st = station_of(key)
                        mid = st.moved(key, beat[3] if len(beat) > 3 else {})
                        if mid:
                            pk = st.pkey(mid, FileV(V, fk))
                            persisted.add(pk)
                            self.first_lit.setdefault(pk, fk)
                    if verb != "light":
                        continue
                    st = station_of(key)
                    if st.persists(key):
                        for k2 in [key] + (companions(key, fk, tables) if st is TABLE else []):
                            pk = st.pkey(k2, FileV(V, fk))
                            persisted.add(pk)
                            self.first_lit.setdefault(pk, fk)
                    sl = st.slot_of(key, FileV(V, fk))
                    if sl:
                        slots[(st.key, sl)] = key
            for unit, cv in off.items():
                if cv in file_verses(fk):
                    persisted.add(unit)
                    self.first_lit.setdefault(unit, fk)
            prev_c = fk[0]


# ---------------------------------------------------------------------------
# One file: the flight, the beats, the drawing
# ---------------------------------------------------------------------------

class Plan_:
    """One file's schedule: the stops' cameras, arrivals and departures,
    and the beats with their times."""

    def __init__(self, fk, V, cam0, hold=0.0):
        self.fk, self.V, self.cam0 = fk, V, cam0
        # the opening hold: the camera waits so the previous file's last
        # stop rests LAST_REST in all (`plans`); given up first when the
        # verse can't afford it
        self.hold_wanted = self.hold = hold
        c, v = fk[0], fk[1]
        self.narr = narration(c, v)
        self.end = self.narr - AUDIO_SLACK
        self.cams = [shot_cam(st.shot, V.beast) for st in V.stops]
        self.words = []
        for st in V.stops:
            ws = []
            for beat in st.beats:
                cw = cue_word(beat[2]) if len(beat) > 2 and beat[2] else None
                if cw:
                    w, n, d = cw
                    ws.append((said(c, v, w, n) - SAY_LEAD + d, NEEDS.get(beat[0], 0.7)))
                elif beat[2].startswith("@"):
                    lag = float(beat[2][2:]) if beat[2].startswith("@+") else 0.0
                    ws.append((None, lag + NEEDS.get(beat[0], 0.7)))
                for k in ("show",):
                    if len(beat) > 3 and k in beat[3]:
                        cw2 = cue_word(beat[3][k])
                        if cw2:
                            said(c, v, cw2[0], cw2[1])
            self.words.append(ws)
        self.squeezed = False
        self._schedule()

    def _run(self, D, dwell, after):
        t = self.hold if (D and D[0] > 0) else 0.0
        ready, arr, starts = 0.0, [], []
        for k in range(len(self.cams)):
            start = max(t, ready)
            a = start + D[k]
            starts.append(start)
            arr.append(a)
            ws = self.words[k]
            scale = after / AFTER_WORD
            last = max([(a if x is None else max(a, x)) + need * scale for x, need in ws],
                       default=a + dwell)
            ready = max(a + dwell, last)
            t = a
        return starts, arr

    def _schedule(self):
        n = len(self.cams)
        prev, D, floor = self.cam0, [], []
        for cam in self.cams:
            d = lev_duration(prev, cam)
            D.append(0.0 if d == 0 else max(MIN_LEG, d))
            # a squeezed pan stops short of SQUEEZE_PEAK_PX_S on screen; the
            # beats' time after their words goes next
            travel = (math.hypot(cam[1] - prev[1], cam[2] - prev[2]) * cam[0]
                      if abs(cam[0] - prev[0]) < 1e-9 else 0.0)
            floor.append(max(MIN_LEG_SQUEEZE, travel * EASE_PEAK / SQUEEZE_PEAK_PX_S))
            prev = cam
        dwell, after = DWELL, AFTER_WORD
        starts, arr = self._run(D, dwell, after)
        tries = 0
        while n and arr[-1] > self.end - 0.05 - self._tail(arr, dwell) and tries < 40:
            tries += 1
            over = arr[-1] - (self.end - 0.05)
            if self.hold > 0:
                # the hold goes only where it costs the landing
                h0 = self.hold
                self.hold = max(0.0, h0 - (over + self._tail(arr, dwell)) - 0.02)
                s2, a2 = self._run(D, dwell, after)
                if a2[-1] < arr[-1] - 1e-6:
                    starts, arr = s2, a2
                    continue
                self.hold = h0
            self.squeezed = True
            # only the legs whose speed-up brings the landing forward: a
            # leg that lands before its stop's words are said keeps its time

            def helps(k):
                D2 = [d - 0.1 if j == k else d for j, d in enumerate(D)]
                return self._run(D2, dwell, after)[1][-1] < arr[-1] - 1e-6
            moving = [k for k in range(n) if D[k] > floor[k] + 1e-6 and helps(k)]
            if moving:
                cut = min(over / len(moving) + 0.02, 0.4)
                D = [max(floor[k], d - cut) if k in moving else d
                     for k, d in enumerate(D)]
            elif dwell > 0.3 or after > 0.3:
                dwell, after = max(0.3, dwell - 0.2), max(0.3, after - 0.2)
            else:
                break
            starts, arr = self._run(D, dwell, after)
        self.D, self.starts, self.arr = D, starts, arr
        self.after_scale = after / AFTER_WORD
        self.dep = [starts[k + 1] for k in range(n - 1)] + ([max(self.narr, arr[-1])] if n else [])
        legs, t = [], 0.0
        for k in range(n):
            if starts[k] - t > 1e-3:
                legs.append(("hold", None, starts[k] - t))
            legs.append(("to", self.cams[k], D[k]))
            t = starts[k] + D[k]
        self.legs = legs
        self.fl = Flight(self.cam0, legs)
        self.cam1 = self.cams[-1] if n else self.cam0

    def _tail(self, arr, dwell):
        """What the last stop's landing beats ("@") need before the end."""
        if not self.words or not self.words[-1]:
            return 0.0
        return min(0.2, max([need for x, need in self.words[-1] if x is None] + [0.0]))

    def resolve(self, cue, k):
        c, v = self.fk[0], self.fk[1]
        a = self.arr[k]
        if cue.startswith("@"):
            return a + (float(cue[2:]) if cue.startswith("@+") else 0.0)
        if cue.startswith("t="):
            return float(cue[2:])
        w, n, d = cue_word(cue)
        return max(a, said(c, v, w, n) - SAY_LEAD + d)

    def beats(self):
        out = []
        for k, st in enumerate(self.V.stops):
            for beat in st.beats:
                verb, key, cue = beat[0], beat[1], beat[2]
                opts = dict(beat[3]) if len(beat) > 3 else {}
                t = round(self.resolve(cue, k), 2)
                opts["_arrive"] = round(self.arr[k], 2)
                opts["_depart"] = round(self.dep[k], 2)
                if "show" in opts:
                    opts["_show"] = round(self.resolve(opts["show"], k), 2)
                out.append((verb, key, t, opts, k))
        return out


def _attr(el, name):
    m = re.search(r'\s' + name + r'="([^"]*)"', el)
    return m.group(1) if m else None


def el_box(el):
    """An element's world box, roughly, for culling; None: keep it always."""
    tag = el[1:el.find(" ")] if " " in el else el[1:-1]
    try:
        if tag == "rect":
            x, y = float(_attr(el, "x")), float(_attr(el, "y"))
            return (x, y, x + float(_attr(el, "width")), y + float(_attr(el, "height")))
        if tag == "line":
            xs = [float(_attr(el, "x1")), float(_attr(el, "x2"))]
            ys = [float(_attr(el, "y1")), float(_attr(el, "y2"))]
            return (min(xs), min(ys), max(xs), max(ys))
        if tag in ("polygon", "polyline"):
            nums = [float(q) for q in re.split(r"[ ,]+", _attr(el, "points").strip())]
            xs, ys = nums[0::2], nums[1::2]
            return (min(xs), min(ys), max(xs), max(ys))
        if tag == "circle":
            cx, cy, r = (float(_attr(el, k)) for k in ("cx", "cy", "r"))
            return (cx - r, cy - r, cx + r, cy + r)
        if tag == "ellipse":
            cx, cy, rx, ry = (float(_attr(el, k)) for k in ("cx", "cy", "rx", "ry"))
            return (cx - rx, cy - ry, cx + rx, cy + ry)
        if tag == "text":
            x, y, size = float(_attr(el, "x")), float(_attr(el, "y")), float(_attr(el, "font-size"))
            s = re.sub(r"<[^>]+>", "", el[el.find(">") + 1:])
            anc = {"start": "l", "middle": "m", "end": "r"}[_attr(el, "text-anchor") or "start"]
            vb = {"text-before-edge": "a", "central": "m", "alphabetic": "s",
                  "text-after-edge": "d"}.get(_attr(el, "dominant-baseline") or "alphabetic", "s")
            from html import unescape
            l, t, r, b = ink(unescape(s), size, 'font-weight="bold"' in el,
                             'font-style="italic"' in el, anc + vb)
            return (x + l, y + t, x + r, y + b)
    except (TypeError, ValueError):
        return None
    return None


def _strip_groups(els):
    out = []
    for el in els:
        if el.startswith("<g") or el == "</g>":
            if "transform" in el or "clip" in el:
                raise AssertionError("a reference drawing grew a transform group")
            continue
        out.append(el)
    return out


# ---------------------------------------------------------------------------
# Size: geometry to a tenth of a px, the camera's keyframes, culled cards
# ---------------------------------------------------------------------------

def _tenths(t):
    """An integer count of tenths as the shortest SVG number: 12, 1.5, -.5."""
    q = f"{t / 10:.1f}"
    if q.endswith(".0"):
        q = q[:-2]
    if q.startswith("0."):
        q = q[1:]
    elif q.startswith("-0."):
        q = "-" + q[2:]
    return "0" if q == "-0" else q


def _join(nums):
    """Numbers run together as SVG path data allows: no space before a
    minus, nor before ".5" after a number that has its own point."""
    out, last = [], ""
    for q in nums:
        if out and not (q[0] == "-" or (q[0] == "." and "." in last)):
            out.append(" ")
        out.append(q)
        last = q
    return "".join(out)


def path_d(points, closed):
    """Points as a path: the first absolute, the rest relative steps, each
    to a tenth of a px (rounded on the absolute grid, so nothing drifts)."""
    v = [float(q) for q in re.split(r"[ ,]+", points.strip()) if q]
    P = [(round(v[i] * 10), round(v[i + 1] * 10)) for i in range(0, len(v) - 1, 2)]
    if not P:
        return ""
    rel = []
    for a, b in zip(P, P[1:]):
        if b != a:
            rel += [_tenths(b[0] - a[0]), _tenths(b[1] - a[1])]
    return ("M" + _join([_tenths(P[0][0]), _tenths(P[0][1])])
            + ("l" + _join(rel) if rel else "") + ("z" if closed else ""))


_SHAPE = re.compile(r'<(polygon|polyline)\b([^>]*?)\spoints="([^"]*)"([^>]*?)(/?)>')
_NUM_ATTR = re.compile(r'(\s(?:x|y|x1|y1|x2|y2|cx|cy|r|rx|ry|width|height)=")'
                       r'(-?\d*\.\d+)(")')
_TRANSLATE = re.compile(r'translate\((-?[\d.]+)[ ,](-?[\d.]+)\)')


def compact(svg):
    """The written file's geometry made short: polygons and polylines as
    relative paths (a traced line, its dashes measured on its points,
    stays as it is), and shapes' places, sizes and translates to a tenth
    of a px. An animation's values, times and splines are left alone."""
    def shape(m):
        tag, pre, pts, post, sc = m.groups()
        if "stroke-dasharray" in pre + post:
            return m.group(0) + ("" if sc else "\x01")
        d = path_d(pts, tag == "polygon")
        if not d:
            return m.group(0) + ("" if sc else "\x01")
        return f'<path{pre} d="{d}"{post}{sc}>' + ("" if sc else "\x00")
    out = _SHAPE.sub(shape, svg)
    # a converted element with children closes as a path
    if "\x00" in out or "\x01" in out:
        parts = re.split(r"(\x00|\x01|</polygon>|</polyline>)", out)
        stack, res = [], []
        for part in parts:
            if part in ("\x00", "\x01"):
                stack.append(part == "\x00")
            elif part in ("</polygon>", "</polyline>"):
                res.append("</path>" if stack and stack.pop() else part)
            else:
                res.append(part)
        out = "".join(res)
    out = _NUM_ATTR.sub(lambda m: m.group(1) + _tenths(round(float(m.group(2)) * 10))
                        + m.group(3), out)
    out = _TRANSLATE.sub(lambda m: f"translate({_tenths(round(float(m.group(1)) * 10))} "
                         f"{_tenths(round(float(m.group(2)) * 10))})", out)
    out = _RGB.sub(_hex, out)
    return _merge_paths(out)


_RGB = re.compile(r"rgb\((\d+),\s*(\d+),\s*(\d+)\)")
_PATH_EL = re.compile(r'<path d="([^"]*)"([^>]*)/>')


def _hex(m):
    h = "".join(f"{min(255, int(q)):02x}" for q in m.groups())
    if h[0] == h[1] and h[2] == h[3] and h[4] == h[5]:
        h = h[0] + h[2] + h[4]
    return "#" + h


def _mergeable(attrs):
    """Shapes that may share one path with the next of the same paint:
    unfilled lines (a fill could cancel where two shapes wound opposite
    ways overlap)."""
    return 'fill="none"' in attrs and "id=" not in attrs and "dasharray" not in attrs


def _merge_paths(svg):
    """Runs of sibling paths with the same paint, one after another, made
    one path."""
    out, pos, run = [], 0, None           # run: [start, end, [ds], attrs]
    for m in _PATH_EL.finditer(svg):
        d, attrs = m.groups()
        if run and m.start() == run[1] and attrs == run[3]:
            run[2].append(d)
            run[1] = m.end()
            continue
        if run:
            out.append(svg[pos:run[0]])
            out.append(f'<path d="{"".join(run[2])}"{run[3]}/>')
            pos = run[1]
            run = None
        if _mergeable(attrs):
            run = [m.start(), m.end(), [d], attrs]
    if run:
        out.append(svg[pos:run[0]])
        out.append(f'<path d="{"".join(run[2])}"{run[3]}/>')
        pos = run[1]
    out.append(svg[pos:])
    return "".join(out)


CAM_TOL = 0.6            # px a dropped camera keyframe may move the frame's corners (in motion)


def _corner_err(ca, cb, cm, u):
    """How far (screen px) the frame's corners at cm land when the camera
    is interpolated from ca to cb at u, as SMIL does (translate and scale
    each linearly)."""
    sa, (tax, tay) = ca[0], cam_T(ca)
    sb, (tbx, tby) = cb[0], cam_T(cb)
    s_ = sa + (sb - sa) * u
    tx, ty = tax + (tbx - tax) * u, tay + (tby - tay) * u
    sm, (tmx, tmy) = cm[0], cam_T(cm)
    err = 0.0
    for X, Y in ((0, 0), (W, 0), (0, H), (W, H)):
        px, py = (X - tmx) / sm, (Y - tmy) / sm
        err = max(err, abs(tx + s_ * px - X), abs(ty + s_ * py - Y))
    return err


def keyframes(cams, tol=CAM_TOL):
    """The keyframes a baked flight needs: a hold is two, a pan or a zoom
    as many as keep every frame within `tol` px of the baked one."""
    n = len(cams) - 1
    keep, a, j = [0], 0, 1
    while j < n:
        b = j + 1
        if all(cams[m] == cams[a] for m in range(a, b + 1)) or all(
                _corner_err(cams[a], cams[b], cams[m], (m - a) / (b - a)) <= tol
                for m in range(a + 1, b)):
            j = b
            continue
        keep.append(j)
        a, j = j, j + 1
    keep.append(n)
    return keep


class CamOut:
    """The flight written out: its camera group and the inherited
    screen-constant attributes, on one shared list of keyframes (with
    keyTimes) instead of every baked frame. A still camera or a single
    eased pan is written as svg_map_camera writes it."""

    def __init__(self, fl):
        self.fl = fl
        self.plain = fl.static or fl.pure_pan
        if not self.plain:
            self.keep = keyframes(fl.cams)
            n = len(fl.cams) - 1
            kts = []
            for i in self.keep:
                q = ("%.5f" % (i / n)).rstrip("0").rstrip(".")
                kts.append(q or "0")
            self.kt = ";".join(kts)
            self.cams = [fl.cams[i] for i in self.keep]

    def _anim(self, attr, vals, typ=None):
        if len(set(vals)) == 1:
            return ""
        kind = "animateTransform" if typ else "animate"
        t = f' type="{typ}"' if typ else ""
        return (f'<{kind} attributeName="{attr}"{t} values="{";".join(vals)}" '
                f'keyTimes="{self.kt}" dur="{self.fl.dur:.2f}s" begin="0s" '
                f'fill="freeze"/>')

    def open_camera(self):
        if self.plain:
            return self.fl.open_camera()
        tv = []
        for c in self.cams:
            tx, ty = cam_T(c)
            tv.append(f"{_tenths(round(tx * 10))} {_tenths(round(ty * 10))}")
        sv = [("%.5f" % c[0]).rstrip("0").rstrip(".") for c in self.cams]
        return (f'<g transform="translate({tv[0]})">' + self._anim("transform", tv, "translate")
                + f'<g transform="scale({sv[0]})">' + self._anim("transform", sv, "scale"))

    def inverse(self, attr, px):
        if self.plain:
            return self.fl.inverse(attr, px)
        vals = ["%.4g" % (px / c[0]) for c in self.cams]
        return f'{attr}="{vals[0]}"', self._anim(attr, vals)

    def emit_class(self, px, els):
        if not els:
            return ""
        a, anim = self.inverse("stroke-width", px)
        return f'<g {a} stroke-linejoin="round">{anim}' + "".join(els) + "</g>"


_TAG = re.compile(r"<(/?)([a-zA-Z]+)([^>]*?)(/?)>")
_SHAPES = ("polygon", "polyline", "rect", "circle", "ellipse", "line")


def _affine(tr):
    """A static transform of translates and scales as (kx, dx, ky, dy):
    x' = kx x + dx; None for anything else."""
    kx, ky, dx, dy = 1.0, 1.0, 0.0, 0.0
    for name, args in re.findall(r"(\w+)\(([^)]*)\)", tr):
        a = [float(q) for q in re.split(r"[ ,]+", args.strip()) if q]
        if name == "translate":
            tx, ty = a[0], (a[1] if len(a) > 1 else 0.0)
            dx, dy = dx + kx * tx, dy + ky * ty
        elif name == "scale":
            sx, sy = a[0], (a[1] if len(a) > 1 else a[0])
            kx, ky = kx * sx, ky * sy
        else:
            return None
    return (kx, dx, ky, dy)


def cull_card(inner, origin, views):
    """A card's drawing without the shapes no camera of the file sees
    (none at a rest, none big enough in flight). Only shapes whose groups
    are plain or statically translated and scaled are judged; anything
    under a moving transform stays."""
    out, stack, pos = [], [], 0
    cur = (1.0, origin[0], 1.0, origin[1])       # card px -> world px
    tags = list(_TAG.finditer(inner))
    for i, m in enumerate(tags):
        close, tag, attrs, sc = m.groups()
        keep_el = True
        if tag == "g" and not close and not sc:
            nxt = tags[i + 1].group(2) if i + 1 < len(tags) else ""
            tr = _attr(" " + attrs, "transform")
            if cur is None or nxt == "animateTransform":
                new = None
            elif tr:
                af = _affine(tr)
                new = None if af is None else (cur[0] * af[0], cur[1] + cur[0] * af[1],
                                               cur[2] * af[2], cur[3] + cur[2] * af[3])
            else:
                new = cur
            stack.append(cur)
            cur = new
        elif tag == "g" and close:
            cur = stack.pop() if stack else cur
        elif tag in _SHAPES and sc and not close and cur is not None:
            b = el_box(m.group(0))
            if b is not None:
                kx, dx, ky, dy = cur
                wb = (kx * b[0] + dx, ky * b[1] + dy, kx * b[2] + dx, ky * b[3] + dy)
                wb = (min(wb[0], wb[2]), min(wb[1], wb[3]), max(wb[0], wb[2]), max(wb[1], wb[3]))
                keep_el = views.sees(wb)
        if not keep_el:
            out.append(inner[pos:m.start()])
            pos = m.end()
    out.append(inner[pos:])
    return "".join(out)


@functools.cache
def ref_world():
    """The reference's plan and table, as (element, box, is_text)."""
    c = SvgCanvas(10, 10)
    R.draw_court(c)
    R.draw_tent(c)
    R.draw_furnishings(c)
    plan = [(el, el_box(el), el.startswith("<text")) for el in _strip_groups(c._els)]
    c = SvgCanvas(10, 10)
    R.draw_offerings(c)
    table = [(el, el_box(el), el.startswith("<text")) for el in _strip_groups(c._els)]
    # the WHEN cells' source flag ("derived") is the reference page's, not
    # WEB wording: left out of the verse pictures
    wy, wh = row_tops()["when"]
    flags = {SN.DERIVED, SN.NOT_GIVEN}
    table = [(el, box, it) for el, box, it in table
             if not (it and box and _text_of(el) in flags and 'font-style="italic"' in el
                     and wy <= box[1] <= wy + wh)]
    # nor its heading over the frame ("THE OFFERINGS", "Leviticus 1-7"),
    # the reference page's too
    table = [(el, box, it) for el, box, it in table
             if not (it and box and box[3] <= TY and _text_of(el) in TABLE_HEADING)]
    return plan, table


TABLE_HEADING = {"THE OFFERINGS", "Leviticus 1–7"}


def _hit(a, b):
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


class Views:
    """What a flight's camera sees: (box, s) at its keyframes, for culling."""

    def __init__(self, fl, rests):
        cams = list(fl.cams)
        if fl.pure_pan:
            cams = [fl.at(fl.dur * i / 12) for i in range(13)]
        step = max(1, len(cams) // 90)
        cams = cams[::step] + [cams[-1]] + list(rests)
        self.views = [(visible_world(c, 8), c[0]) for c in cams]
        self.rests = [visible_world(c, 8) for c in rests]

    def sees(self, box, px=10.0, text_size=None):
        """In view at a rest, or in flight at a scale it reads at (a word
        6 px high, a shape 10 px across): a flight's wide frames keep the
        table's frame, rules and veils, not every word and drawing."""
        if box is None:
            return True
        if any(_hit(box, vb) for vb in self.rests):
            return True
        size = max(box[2] - box[0], box[3] - box[1])
        for vb, s in self.views:
            if _hit(box, vb):
                if text_size is not None:
                    if text_size * s >= 6.0:
                        return True
                elif size * s >= px:
                    return True
        return False


class LevCtx(ST.Ctx):
    """The stations' Ctx, keeping which target drew each outline and each
    held-size word (for the carry into the next file)."""
    cur = None

    def sees(self, box):
        return self.views.sees(box)

    def outline(self, target, t, first=True):
        self.outlined.append(target.key)
        n = len(self.outlines)
        super().outline(target, t, first)
        self.outline_keys += [target.key] * (len(self.outlines) - n)

    def pin_text(self, *a, **k):
        n = len(self.pins)
        out = super().pin_text(*a, **k)
        self.pin_keys += [self.cur] * (len(self.pins) - n)
        return out

    def inline_figures(self, svg):
        """`svg` with its figures drawn in place, none in <defs>."""
        def one(m):
            at0, x, gy, args = self._figs[int(m.group(1))]
            return self._draw(args[0], x, gy, *args[1:]) if at0 else ""
        return ST.FIG_MARK.sub(one, svg)


# ---------------------------------------------------------------------------
# The carry: what the file before drew that this file doesn't draw
# ---------------------------------------------------------------------------
# A file's last frame is the next file's first. What the next file wouldn't
# draw (a verse's own chip or token, a case's stack left behind, a pulse
# still running) is carried into it as the file before drew it, its times
# shifted by that file's length (begin < 0: SMIL plays it to its end state
# before the first frame, and a pulse still running runs on), and faded out
# as the camera first moves (`leave_time`).

CARRY_FADE = 0.5
_BEGIN = re.compile(r'begin="(-?[\d.]+)s"')
_HREF = re.compile(r'href="#([\w-]+)"')


_ANIM_TAG = re.compile(r"<(?:animate|animateTransform|animateMotion|set)\b[^>]*>")
_DUR = re.compile(r'\sdur="([\d.]+)s"')


def shift_times(svg, by):
    """Every animation's begin moved `by` seconds earlier. One that would
    end before the first frame begins just before it instead, ending a
    hundredth in (browsers drop an interval wholly before 0, freeze and
    all)."""
    def tag(m):
        el = m.group(0)
        b = _BEGIN.search(el)
        if not b:
            return el
        new = float(b.group(1)) - by
        d = _DUR.search(el)
        if d:
            new = max(new, 0.01 - float(d.group(1)))
        return el[:b.start()] + f'begin="{new:.2f}s"' + el[b.end():]
    return _ANIM_TAG.sub(tag, svg)


def leave_time(P):
    """When the carried things go: as the camera first moves, or soon."""
    for k, d in enumerate(P.D):
        if d > 0:
            return round(P.starts[k], 2)
    return 0.4


class Carry:
    """What one file drew, by station and by target, its times shifted to
    the next file's clock: (key, svg) pieces, the plan's held-size words,
    the outlines, and the <defs> they use."""

    def __init__(self):
        self.pieces, self.pins, self.outlines, self.defs = {}, [], [], {}

    def take(self, ctx, by):
        for st_key, items in ctx.pieces.items():
            out = []
            for key, svg in items:
                s = shift_times(ctx.inline_figures(svg), by)
                for did in _HREF.findall(s):
                    if did in ctx.defs:
                        self.defs[did] = ctx.defs[did]
                out.append((key, s))
            self.pieces[st_key] = out
        self.pins = [(k, size, shift_times(el, by))
                     for k, (size, el) in zip(ctx.pin_keys, ctx.pins)]
        self.outlines = [(k, shift_times(el, by))
                         for k, el in zip(ctx.outline_keys, ctx.outlines)]
        return self


def prev_file(fk):
    files = all_files()
    i = files.index(fk)
    return files[i - 1] if i else None


def render(fk, verses, tables, hist, extra=None, carry="auto"):
    """-> (svg, report dict) for one file. `carry`: the file before's
    Carry (report["carry"]); "auto" renders that file to get it, None
    carries nothing in."""
    V = verses[fk]
    if carry == "auto":
        pf = prev_file(fk)
        carry = render(pf, verses, tables, hist, extra, None)[1]["carry"] if pf else None
    P = plans(verses, extra)[fk]
    cam0 = P.cam0
    fl = P.fl
    beats = P.beats()
    lit = {}
    for verb, key, t, _o, _k in beats:
        if verb == "light" and key not in lit:
            lit[key] = t
    extra_beats, joined = [], {}
    for verb, key, t, o, k in beats:
        if verb == "light" and station_of(key) is TABLE:
            for w in companions(key, fk, tables):
                if w not in lit:
                    lit[w] = t
                    # it lights with its entry: one outline round the two
                    extra_beats.append(("light", w, t, dict(o, _with=key), k))
                    joined[(key, t)] = w
    beats = beats + extra_beats
    ctx = LevCtx(fl, fk, V, V.beast, before=hist.before[fk], lit=lit)
    FV = FileV(V, fk)
    ctx.outlined, ctx.outline_keys, ctx.pin_keys, ctx.pieces = [], [], [], {}
    ctx.first_lit = hist.first_lit
    ctx.drawn = set()
    ctx.carried = []
    rests = [cam0] + P.cams
    ctx.views = Views(fl, rests)
    cam_out = CamOut(fl)
    reg = ST.registry()
    problems, notes = [], []

    # which stations: world ones always (culled), cards when a rest sees them
    named = {station_of(b[1]).key for b in beats if b[0] not in ("hud", "forgiven")}
    shown, passed = [], []
    for st in [reg["plan"], TABLE] + [s_ for k_, s_ in reg.items() if k_ != "plan"]:
        if st.world:
            shown.append(st)
        elif any(_hit(st.rect(), visible_world(c)) for c in rests):
            shown.append(st)
        elif ctx.views.sees(st.rect(), px=60):
            passed.append(st)
    for k_ in named:
        if k_ not in {s_.key for s_ in shown}:
            problems.append(f"station {k_} is named but no rest camera sees it")

    plan_els, table_els = ref_world()
    world = []
    sizes = {}

    def put(section, el):
        world.append(el)
        sizes.setdefault(section, []).append(el)
    for el, box, is_text in plan_els:
        if ctx.views.sees(box, text_size=float(_attr(el, "font-size")) if is_text else None):
            put("ref plan", el)
    # what a veil covers all file long isn't drawn under it
    hidden = [u.box for u in table_units().values()
              if u.key not in ctx.before and u.key not in lit]
    for el, box, is_text in table_els:
        if box and any(box[0] >= h[0] - 1 and box[1] >= h[1] - 1 and box[2] <= h[2] + 1
                       and box[3] <= h[3] + 1 for h in hidden):
            continue
        # a drawn thing seen only in flight is kept where it reads (TABLE_FLY_PX)
        if ctx.views.sees(box, px=TABLE_FLY_PX,
                          text_size=float(_attr(el, "font-size")) if is_text else None):
            put("ref table", el)

    for st in passed:
        ox, oy = st.origin
        put("passed cards", f'<g transform="translate({_fmt(ox)} {_fmt(oy)})">{st.card()}</g>')
    ctx.flares, ctx.moves = {}, {}
    for verb, key, t, _o, _k in beats:
        if verb == "flare":
            ctx.flares.setdefault(key, []).append(t)
        if verb == "move":
            ctx.moves.setdefault(key, []).append(t)
    t_leave = leave_time(P)
    by_station = {}
    for b in beats:
        if b[0] in ("hud", "forgiven"):
            continue
        by_station.setdefault(station_of(b[1]).key, []).append(b)
    slots_before = hist.slots[fk]
    for st in shown:
        ctx.origin = st.origin if not st.world else (0, 0)
        ctx.station = st.key
        T = st.targets(ctx)
        base = st.base(ctx)
        pieces = ctx.pieces.setdefault(st.key, [])

        def add(pkey_, svg_):
            if svg_:
                pieces.append((pkey_, svg_))
        for k_, s_ in st.base_pieces(ctx):
            add(k_, s_)

        def draw(key, tg, t):
            ctx.cur = key
            return tg.draw(ctx, t)
        # who holds each slot now, and who comes in
        new_in_slot = {}
        for verb, key, t, _o, _k in sorted(by_station.get(st.key, []), key=lambda b: b[2]):
            sl = st.slot_of(key, FV)
            if verb == "light" and sl and sl not in new_in_slot:
                new_in_slot[sl] = (key, t)
        for key, tg in T.items():
            if tg.draw is None:
                continue
            pk = st.pkey(key, FV)
            sl = st.slot_of(key, FV)
            if sl:
                occ = slots_before.get((st.key, sl))
                new = new_in_slot.get(sl)
                if key == occ:
                    if new and new[0] != key:
                        add(key, ST.fade_out(draw(key, tg, None), new[1]))
                    else:
                        add(key, draw(key, tg, None))
                elif new and new[0] == key:
                    add(key, draw(key, tg, new[1]))
                continue
            if st.persists(key) and pk in ctx.before:
                if not st.world or ctx.sees(tg.box):
                    add(key, draw(key, tg, None))
            elif key in lit:
                add(key, draw(key, tg, lit[key]))
        for verb, key, t, opts, k in by_station.get(st.key, []):
            if key not in T:
                raise KeyError(f"Lev {ref_str(fk)}: station {st.key} has no target {key!r}")
            tg = T[key]
            pk = st.pkey(key, FV)
            if verb == "light" and opts.get("_with"):
                continue                     # outlined with its entry
            if verb == "light":
                first = not (st.persists(key) and pk in ctx.before) and lit.get(key) == t
                w = joined.get((key, t))
                if w:
                    first = first or not (st.persists(w) and st.pkey(w, FV) in ctx.before)
                    x0, y0, x1, y1 = ST.union_box([tg.box, T[w].box])
                    tg = ST.Target(key, outline=[(ST.rect_pts(x0 - 2, y0 - 2, x1 + 2, y1 + 2),
                                                  True)])
                ctx.outline(tg, t, first)
            elif verb == "pulse":
                ctx.outline(tg, t, True)
            elif verb == "current":
                ctx.outline(tg, t, False)
            else:
                ctx.cur = key
                add(("act", verb, key, st.moved(key, opts) if verb == "move" else None),
                    st.act(ctx, verb, key, t, opts))
        # what the file before drew here that this file doesn't, faded out
        # as the camera first moves (the table's veils aren't carried)
        drawn = {k for k, _s in pieces if isinstance(k, str)}
        carried = []
        # (only where the first frame sees it: it is gone as the camera moves)
        if carry and st is not TABLE and _hit(st.rect(), visible_world(cam0, 8)):
            for k, s in carry.pieces.get(st.key, []):
                if isinstance(k, str) and k in drawn:
                    continue
                if not isinstance(k, str) and k[3] and k[3] in drawn:
                    continue                 # its moved end state is drawn here
                carried.append(ST.fade_out(s, t_leave, CARRY_FADE))
                ctx.carried.append(k)
        body = [base] + [s for _k, s in pieces] + carried
        ctx.drawn |= drawn
        inner = ctx.resolve_figures("".join(b for b in body if b))
        if not st.world:
            inner = cull_card(inner, st.origin, ctx.views)
        if st.key == "plan":
            # the plan's own strokes hold their screen width (at the lens,
            # and through 7:37-38's zooms)
            sa, sanim = cam_out.inverse("stroke-width", 3.0)
            put(st.key, f'<g {sa}>{sanim}{inner}</g>')
        elif st.world:
            put(st.key, inner)
        else:
            ox, oy = st.origin
            put(st.key, f'<g transform="translate({_fmt(ox)} {_fmt(oy)})">{inner}</g>')

    # the screen-constant layers: outlines, the plan's words (and the file
    # before's that this file doesn't draw, faded as the camera moves)
    outs = list(ctx.outlines)
    pins = list(ctx.pins)
    if carry:
        mine = set(ctx.outline_keys)
        outs += [ST.fade_out(el, t_leave, CARRY_FADE) for k, el in carry.outlines
                 if k not in mine]
        pins += [(size, ST.fade_out(el, t_leave, CARRY_FADE)) for k, size, el in carry.pins
                 if k not in ctx.drawn]
        for did, d in carry.defs.items():
            ctx.defs.setdefault(did, d)
    put("outlines", cam_out.emit_class(OUTLINE_PX, outs))
    by_size = {}
    for size, el in pins:
        by_size.setdefault(size, []).append(el)
    for size, els in sorted(by_size.items()):
        fa, fanim = cam_out.inverse("font-size", size)
        sa, sanim = cam_out.inverse("stroke-width", 3.6)
        put("pins", f'<g {fa} {sa}>{fanim}{sanim}' + "".join(els) + "</g>")

    # the HUD
    hud, hud_rects = hud_svg(fk, beats, hist)
    defs = "".join(ctx.defs.values())
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" data-kind="chart" '
           f'viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
           f'font-family="{FONT_FAMILY}">'
           + (f"<defs>{defs}</defs>" if defs else "")
           + f'<rect width="{W}" height="{H}" fill="{ST.rgb(BG)}"/>'
           + cam_out.open_camera() + "".join(world).replace(_ROOT_FONT, "")
           + "</g></g>" + hud + "</svg>")
    svg = compact(svg)
    report = qc_file(fk, P, beats, ctx, svg, hud_rects, problems)
    sizes = {k: len(compact("".join(v))) for k, v in sizes.items()}
    sizes["defs"], sizes["hud"] = len(compact(defs)), len(hud)
    sizes["camera"] = len(cam_out.open_camera())
    report["sections"] = sizes        # bytes as written, by part of the sheet
    report["outlined"] = list(ctx.outlined)
    report["words"] = sorted({tb.key for tb in ctx.texts})
    report["carry"] = Carry().take(ctx, P.narr)
    report["carried"] = ctx.carried
    report["hold"] = (P.hold, P.hold_wanted)
    return svg, report


# the root's font, said again on every word the reference draws
_ROOT_FONT = f' font-family="{FONT_FAMILY}"'


HUD_OUT, HUD_IN = 0.25, 0.3     # a title fades out, then the next fades in


def hud_svg(fk, beats, hist):
    """The title plate (the chapter, then the offering's name) and the
    'forgiven' chip, outside the camera."""
    title = hist.title_at[fk]
    changes = sorted((t, key) for verb, key, t, _o, _k in beats if verb == "hud")
    out, rects = [], []
    plates = [(0.0, title)] + changes
    for i, (t, ttl) in enumerate(plates):
        el = title_svg(ttl, TEXT)
        t_next = plates[i + 1][0] if i + 1 < len(plates) else None
        if i == 0 and t_next is None:
            out.append(el)
        elif i == 0:
            out.append(f'<g>{fade(t_next, HUD_OUT, out=True)}{el}</g>')
        else:
            inner = el if t_next is None else f'<g>{fade(t_next, HUD_OUT, out=True)}{el}</g>'
            out.append(f'<g opacity="0">{fade(t + HUD_OUT, HUD_IN)}{inner}</g>')
        rects.append(title_rect(ttl))
    for verb, _key, t, _o, _k in beats:
        if verb == "forgiven":
            x0, y0 = 6, 50
            l, tp, r, b = ink("forgiven", 17, False, True, "lm")
            w = r - l + 24
            out.append(f'<g opacity="0">{fade(t, 0.5)}<rect x="{x0}" y="{y0}" '
                       f'width="{_fmt(w)}" height="30" rx="8" fill="{ST.rgb(BG)}" '
                       f'fill-opacity="0.82" stroke="{ST.rgb(SAND_DIM)}"/>'
                       f'<text x="{x0 + 12}" y="{y0 + 15}" font-size="17" '
                       f'font-style="italic" fill="{ST.rgb(HL)}" '
                       f'dominant-baseline="central">forgiven</text></g>')
            rects.append((x0, y0, x0 + w, y0 + 30))
            break
    return "".join(out), rects


# ---------------------------------------------------------------------------
# QC
# ---------------------------------------------------------------------------

def screen_box(tb, cam):
    if tb.box is None and not tb.pinned:
        return None
    if tb.pinned:
        sx, sy = to_screen(cam, tb.anchor)
        l, t, r, b = tb.box
        return (sx + l, sy + t, sx + r, sy + b)
    a = to_screen(cam, tb.box[:2])
    b = to_screen(cam, tb.box[2:])
    return (a[0], a[1], b[0], b[1])


def _inside(b, frame):
    return b[0] >= frame[0] and b[1] >= frame[1] and b[2] <= frame[2] and b[3] <= frame[3]


def _text_of(el):
    from html import unescape
    return unescape(re.sub(r"<[^>]+>", "", el[el.find(">") + 1:]))


@functools.cache
def _plan_text_boxes():
    """The reference plan's labels, (text, world box), as draw_court,
    draw_tent and draw_furnishings set them."""
    plan, _t = ref_world()
    return [(_text_of(el), box) for el, box, is_text in plan if is_text and box]


@functools.cache
def _table_text_boxes():
    """The reference table's words, (text, world box, the unit whose veil
    covers it or None)."""
    _p, table = ref_world()
    units = table_units().values()
    out = []
    for el, box, is_text in table:
        if not (is_text and box):
            continue
        under = next((u.key for u in units if box[0] >= u.box[0] - 1 and box[1] >= u.box[1] - 1
                      and box[2] <= u.box[2] + 1 and box[3] <= u.box[3] + 1), None)
        out.append((_text_of(el), box, under))
    return out


def plan_labels_cut(cam):
    """The reference plan's labels a camera's frame cuts."""
    frame = (0, 0, W, H)
    return [lab for lab, box in _plan_text_boxes()
            if _cut(to_screen(cam, box[:2]) + to_screen(cam, box[2:]), frame)]


def _cut(sb, frame):
    """A word partly in the frame: some of it in, some out."""
    return _hit(sb, frame) and not _inside(sb, (frame[0] - 0.5, frame[1] - 0.5,
                                                frame[2] + 0.5, frame[3] + 0.5))


_FLOW_AT = ((0, 0), (W, 0), (0, H), (W, H), (W / 2, H / 2))


def screen_flow(a, b):
    """How far (screen px) the world points under the screen's corners and
    centre move between camera a and camera b."""
    best = 0.0
    for qx, qy in _FLOW_AT:
        wx, wy = a[1] + (qx - W / 2) / a[0], a[2] + (qy - H / 2) / a[0]
        px, py = W / 2 + b[0] * (wx - b[1]), H / 2 + b[0] * (wy - b[2])
        best = max(best, math.hypot(px - qx, py - qy))
    return best


def camera_legs(P):
    """One file's moving legs, as the browser plays them: per leg its stop
    index k, kind ("pan" or "zoom", Flight's), time, screen widths of pan
    at the wider end, octaves of zoom end to end, the octaves it zooms out
    past its wider end in flight (arc), its peak on-screen speed (px/s,
    sampled SPEED_FPS a second) and whether both ends are on the lens."""
    kinds = [lg.kind for lg in P.fl.legs if lg.kind != "hold"]
    out, prev = [], P.cam0
    for k, (cam, d) in enumerate(zip(P.cams, P.D)):
        if d <= 0 or cam == prev:
            prev = cam
            continue
        t0 = P.starts[k]
        n = max(2, math.ceil(d * SPEED_FPS))
        cs = [P.fl.at(t0 + d * i / n) for i in range(n + 1)]
        peak = max(screen_flow(a, b) for a, b in zip(cs, cs[1:])) / (d / n)
        wide = min(prev[0], cam[0])
        out.append(dict(
            k=k, kind=kinds[len(out)] if len(out) < len(kinds) else "?", dur=d,
            pan=math.hypot(cam[1] - prev[1], cam[2] - prev[2]) * wide / W,
            zoom=abs(math.log2(cam[0] / prev[0])),
            arc=max(0.0, math.log2(wide / min(c[0] for c in cs))),
            peak=peak, lens=(abs(prev[0] - SPEC.LENS) < 1e-9 and abs(cam[0] - SPEC.LENS) < 1e-9)))
        prev = cam
    return out


def qc_file(fk, P, beats, ctx, svg, hud_rects, problems):
    problems = list(problems)
    warn = []
    n = len(P.cams)
    if n:
        margin = P.narr - P.arr[-1]
        if margin < AUDIO_SLACK - 1e-6:
            problems.append(f"lands {margin:.2f} s before the MP3 ends (< {AUDIO_SLACK})")
    else:
        margin = P.narr
    limit = 1 if P.narr < 5 else 2 if P.narr <= 10 else 3
    if n > limit:
        problems.append(f"{n} stops in a {P.narr:.1f} s verse (at most {limit})")
    for verb, key, t, _o, k in beats:
        if t > P.narr - 0.15:
            problems.append(f"{verb} {key} at {t:.2f} s, after the narration")
        elif k < n - 1 and t > P.dep[k] - 0.2:
            problems.append(f"{verb} {key} at {t:.2f} s, after the camera leaves stop {k + 1} "
                            f"({P.dep[k]:.2f} s)")
    if P.squeezed and any(0 < d < MIN_LEG for d in P.D):
        warn.append("legs squeezed below %.1f s: %s" % (MIN_LEG, ", ".join(f"{d:.2f}" for d in P.D)))
    # words at each rest
    frame = (0, 0, W, H)
    safe = (SAFE_IN, SAFE_IN, W - SAFE_IN, H - SAFE_IN)
    plan_boxes = _plan_text_boxes()
    for k in range(n):
        cam = P.cams[k]
        t_rest = P.dep[k]
        own = [b[1] for b in beats if b[4] == k and b[1]]     # "forgiven" has none
        vis = []
        for tb in ctx.texts:
            if tb.t > t_rest + 1e-6:
                continue
            sb = screen_box(tb, cam)
            if sb is None or not _hit(sb, frame):
                continue
            vis.append((tb, sb))
            mine = any(tb.key.startswith(o) for o in own) and tb.t >= P.arr[k] - 0.6
            if mine and not _inside(sb, safe):
                problems.append(f"stop {k + 1}: {tb.key!r} runs off the frame "
                                f"({', '.join(f'{v:.0f}' for v in sb)})")
            for hr in hud_rects:
                if _hit(sb, hr):
                    (problems if mine else warn).append(
                        f"stop {k + 1}: {tb.key!r} under the title plate")
            if tb.pinned:
                for _lab, pb in plan_boxes:
                    ps = (to_screen(cam, pb[:2]) + to_screen(cam, pb[2:]))
                    if _hit(sb, ps):
                        problems.append(f"stop {k + 1}: {tb.key!r} touches a plan label")
                        break
        for i in range(len(vis)):
            for j in range(i + 1, len(vis)):
                a, b = vis[i], vis[j]
                if a[0].key == b[0].key:
                    continue
                if _hit(a[1], b[1]):
                    problems.append(f"stop {k + 1}: {a[0].key!r} overlaps {b[0].key!r}")
        # no word at a rest is cut by the frame's edge: the stations' and the
        # plan's words, the reference plan's labels, the table's unveiled words
        for tb, sb in vis:
            if _cut(sb, frame):
                problems.append(f"stop {k + 1}: {tb.key!r} is cut by the frame edge")
        for lab in plan_labels_cut(cam):
            problems.append(f"stop {k + 1}: plan label {lab!r} is cut by the frame edge")
        for lab, box, under in _table_text_boxes():
            if under and under not in ctx.before and ctx.lit.get(under, 1e9) > t_rest:
                continue                         # still veiled
            sb = to_screen(cam, box[:2]) + to_screen(cam, box[2:])
            if _cut(sb, frame):
                problems.append(f"stop {k + 1}: table word {lab!r} is cut by the frame edge")
            elif _hit(sb, frame) and hud_rects and _hit(sb, hud_rects[-1]):
                # the plate the file ends on (an earlier title fades on its beat)
                warn.append(f"stop {k + 1}: table word {lab!r} under the title plate")
    # mid-flight: the plan's held-size words against each other
    pins = [tb for tb in ctx.texts if tb.pinned]
    fl = P.fl
    if pins and not fl.static:
        for i in range(1, 24):
            t = fl.dur * i / 24
            cam = fl.at(t)
            vis = [(tb, screen_box(tb, cam)) for tb in pins if tb.t <= t]
            vis = [(tb, b) for tb, b in vis if _hit(b, frame)]
            for a in range(len(vis)):
                for b in range(a + 1, len(vis)):
                    if vis[a][0].key != vis[b][0].key and _hit(vis[a][1], vis[b][1]):
                        warn.append(f"mid-flight {t:.1f} s: {vis[a][0].key} / {vis[b][0].key}")
    late = [float(b) for b in _BEGIN.findall(svg) if float(b) > P.narr - 0.1]
    if late:
        problems.append(f"{len(late)} animation(s) begin after the narration "
                        f"(latest {max(late):.2f} s, narration {P.narr:.2f} s)")
    # the lens
    for k, (cam, stop) in enumerate(zip(P.cams, P.V.stops)):
        if stop.shot not in LENS_EXEMPT and abs(cam[0] - SPEC.LENS) > 1e-9:
            problems.append(f"stop {k + 1}: {stop.shot!r} rests at s {cam[0]:g}, off the "
                            f"lens ({SPEC.LENS})")
    legs = camera_legs(P)
    if len(legs) > MAX_LEGS:
        problems.append(f"{len(legs)} legs (> {MAX_LEGS})")
    pan = sum(lg["pan"] for lg in legs)
    zoom = sum(lg["zoom"] for lg in legs)
    if pan > MAX_FILE_PAN:
        problems.append(f"{pan:.2f} screen widths of pan (> {MAX_FILE_PAN})")
    if zoom > MAX_FILE_ZOOM:
        problems.append(f"{zoom:.2f} octaves of zoom (> {MAX_FILE_ZOOM})")
    for lg in legs:
        k = lg["k"]
        if lg["lens"] and lg["kind"] != "pan":
            problems.append(f"leg {k + 1}: between two lens rests, but a {lg['kind']}")
        if lg["pan"] > MAX_LEG_PAN:
            problems.append(f"leg {k + 1}: {lg['pan']:.2f} screen widths (> {MAX_LEG_PAN})")
        if round(lg["peak"]) > MAX_PEAK_PX_S:
            problems.append(f"leg {k + 1}: {lg['peak']:.0f} px/s on screen (> {MAX_PEAK_PX_S}, "
                            f"{lg['dur']:.2f} s)")
        elif round(lg["peak"]) > PAN_PEAK_PX_S:
            warn.append(f"leg {k + 1}: {lg['peak']:.0f} px/s on screen ({lg['dur']:.2f} s)")
    if P.hold_wanted > 0:
        # the rest across the seam: the file before's last stop, then this
        # file's opening hold up to its first move
        first = next((P.starts[k] for k, d in enumerate(P.D) if d > 0), P.narr)
        seam = LAST_REST - P.hold_wanted + first
        if seam < LAST_REST - 0.05:
            warn.append(f"the rest across the seam is {seam:.2f} s (opening hold "
                        f"{first:.2f} s)")
    rects = svg.count("<rect")
    texts = svg.count("<text")
    if rects > MAX_RECTS:
        problems.append(f"{rects} rects (> {MAX_RECTS})")
    if texts > MAX_TEXTS:
        problems.append(f"{texts} texts (> {MAX_TEXTS})")
    for bad in ("clip-path", "<mask", "filter=", "<clipPath"):
        if bad in svg:
            problems.append(f"{bad} in the file")
    # dedupe, keep order
    seen = set()
    problems = [p for p in problems if not (p in seen or seen.add(p))]
    warn = sorted(set(warn))[:6]
    return dict(file=file_name(fk), ref=ref_str(fk), kb=round(len(svg.encode()) / 1024, 1),
                rects=rects, texts=texts, narr=P.narr, land=P.arr[-1] if n else 0.0,
                margin=round(margin, 2), stops=n, legs=[round(d, 2) for d in P.D],
                problems=problems, warnings=warn, stub=P.V.stub)


def coverage_gaps(verses, tables):
    """Every offerings.py row and thing ref in Lev 1-7 lights its unit: the
    file holding each verse a unit cites lights, pulses or holds it current,
    or the pair is accounted for: (unit, (c, v)) or unit in EXCUSED (with a
    reason), the unit reached off camera in that file (REACHED_OFFSCREEN), or
    a verse before the unit's REACH. A who-line goes with its entry."""
    files = all_files()
    fv = {cv: fk for fk in files for cv in file_verses(fk)}
    touched = {}
    for fk in files:
        got = touched.setdefault(fk, set())
        for st in verses[fk].stops:
            for b in st.beats:
                if b[1] and b[0] in ("light", "pulse", "current"):
                    got.add(b[1])
                    if b[0] == "light":
                        got.update(companions(b[1], fk, tables))
    units = table_units()

    def ok(key, cv):
        fk = fv.get(cv)
        if fk is None:
            return True
        if key in touched[fk]:
            return True
        off = tables["REACHED_OFFSCREEN"].get(key)
        if off and off in file_verses(fk):
            return True
        reach = tables["REACH"].get(key) or tables["REACH"].get(key.removesuffix("/who"))
        if reach and cv < reach:
            return True
        return key in tables["EXCUSED"] or (key, cv) in tables["EXCUSED"]
    gaps = []
    for key, u in units.items():
        for cv in u.refs:
            if ok(key, cv):
                continue
            if key.endswith("/who") and ok(key.removesuffix("/who"), cv):
                continue
            gaps.append(f"{key}: its row cites {cv[0]}:{cv[1]}, which doesn't light it "
                        f"(EXCUSED or REACHED_OFFSCREEN?)")
    for k in tables["EXCUSED"]:
        unit = k[0] if isinstance(k, tuple) else k
        if unit not in units:
            gaps.append(f"EXCUSED names {unit!r}, which is no unit")
        if not str(tables["EXCUSED"][k]).strip():
            gaps.append(f"EXCUSED {k!r} gives no reason")
    for unit in tables["REACHED_OFFSCREEN"]:
        if unit not in units:
            gaps.append(f"REACHED_OFFSCREEN names {unit!r}, which is no unit")
    return gaps


def qc_run(verses, tables, hist):
    """The checks over the whole run: coverage, reaches."""
    out, pending = [], []
    out += coverage_gaps(verses, tables)
    units = table_units()
    stubs = [fk for fk in all_files() if verses[fk].stub]
    if stubs:
        pending.append(f"{len(stubs)} of {len(all_files())} files are stubs")
    files = all_files()
    order = {fk: i for i, fk in enumerate(files)}
    fv = {cv: fk for fk in files for cv in file_verses(fk)}
    for key, u in units.items():
        fk = hist.first_lit.get(key)
        if fk is None:
            (pending if stubs else out).append(f"{key} is never reached")
            continue
        want = (tables["REACH"].get(key) or tables["REACH"].get(key.removesuffix("/who"))
                or (u.refs[0] if u.refs else None))
        cvs = file_verses(fk)
        if key in tables["REACHED_OFFSCREEN"]:
            continue
        if want and want not in cvs and key not in tables["EXCUSED"]:
            msg = (f"{key} first lit at {ref_str(fk)}, but its first verse is "
                   f"{want[0]}:{want[1]} (REACH, REACHED_OFFSCREEN or EXCUSED?)")
            if want in fv and verses[fv[want]].stub:
                pending.append(msg)
            else:
                out.append(msg)
        if order[fk] > order[fv[(7, 37)]]:
            out.append(f"{key} reached after 7:37")
    return out, pending


# ---------------------------------------------------------------------------
# Writing
# ---------------------------------------------------------------------------

def out_file(fk, out_dir, web):
    name = file_name(fk)
    if web:
        return GT.out_path(BOOK, fk[0], name)
    d = os.path.join(out_dir, BOOK, str(fk[0]))
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, name)


def build(only=None, extra=None, out_dir=None, web=False, qc_only=False, echo=print):
    verses, tables = load_verses(extra)
    for fk in all_files():
        if fk not in verses:
            raise KeyError(f"no spec for Lev {ref_str(fk)}")
    hist = History(verses, tables)
    file_cams.cache_clear()
    reports, carry, files = [], None, all_files()

    def wanted(fk):
        return not only or any(cv in only for cv in file_verses(fk))
    for i, fk in enumerate(files):
        if not wanted(fk):
            # rendered only for its carry into the next file
            if i + 1 < len(files) and wanted(files[i + 1]):
                carry = render(fk, verses, tables, hist, extra, None)[1]["carry"]
            else:
                carry = None
            continue
        svg, rep = render(fk, verses, tables, hist, extra, carry)
        carry = rep["carry"]
        rep["written"] = False
        if not rep["problems"] and not qc_only:
            path = out_file(fk, out_dir, web)
            with open(path, "w", encoding="utf-8") as f:
                f.write(svg)
            rep["written"] = path
        reports.append(rep)
        flag = "STUB " if rep["stub"] else ""
        echo(f"{rep['ref']:>8} {flag}{rep['kb']:6.1f} KB  rects {rep['rects']:4d}  "
             f"texts {rep['texts']:3d}  narr {rep['narr']:5.2f}  land {rep['land']:5.2f}  "
             f"stops {rep['stops']}  {'OK' if not rep['problems'] else 'REFUSED'}")
        for p in rep["problems"]:
            echo(f"           ! {p}")
        for wmsg in rep["warnings"]:
            echo(f"           ~ {wmsg}")
    run_bad, pending = qc_run(verses, tables, hist)
    if not only:
        for p in run_bad:
            echo(f"  run ! {p}")
    echo(f"  run: {len(run_bad)} problems, {len(pending)} pending "
         f"(stubs: {sum(1 for fk in all_files() if verses[fk].stub)})")
    return reports, run_bad, pending


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", help="write under this folder (as <out>/Leviticus/<c>/)")
    ap.add_argument("--web", action="store_true", help="write into web/visuals")
    ap.add_argument("--only", help="verses, e.g. 1:1-1:17,3:4")
    ap.add_argument("--verses-extra", help="a .py whose VERSES lie over the spec's")
    ap.add_argument("--qc-only", action="store_true", help="render and check, write nothing")
    a = ap.parse_args(argv)
    if not a.web and not a.out and not a.qc_only:
        ap.error("give --out DIR (or --web to write into web/visuals, or --qc-only)")
    only = parse_only(a.only) if a.only else None
    reports, run_bad, _pending = build(only, a.verses_extra, a.out, a.web, a.qc_only)
    refused = [r for r in reports if r["problems"]]
    print(f"{len(reports)} files, {len(refused)} refused, "
          f"{sum(1 for r in reports if r['written'])} written")
    return 1 if refused else 0


if __name__ == "__main__":
    sys.exit(main())
