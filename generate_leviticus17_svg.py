"""Leviticus 1-7, the offerings: a still workbench that files, a file a verse.

The frame never moves (no camera). It is a workshop in three fixed regions:
the plan strip (the Tabernacle reference page's court plan, drawn by
generate_tabernacle_reference.draw_court, draw_tent and draw_furnishings),
the bench (where each verse's thing is built on its word) and the dock (the
offerings table's working column under five tabs). A chip lifts off the
thing just built and glides to its slot in the column; at the end of an
offering's section the column is filed into the real reference table
(draw_offerings, the file view) and the workshop comes back.

The modules:
- leviticus17_bench: the engine. One global timeline of elements; each file
  renders every element's state at its start plus its events inside the
  file as SMIL, so seams are exact by construction. Its docstring is the
  SECTION CONTRACT; QC lives there too.
- leviticus17_parts: the plan strip (one world window for the whole book)
  and the bench's shared parts (the altar set, the beasts and their
  cutaways, chips, arrows, not-marks, the bird bay, case clears).
- leviticus17_art: the drawings more than one section shows (the meal
  offering's supplies, the cookware, the breads, the insets, heaps, flames,
  hands), one drawing of each.
- leviticus17_dock: the dock's columns for all five offerings (every slot a
  table_units() id), the tabs, lighting and chip flights, and the file view.
- leviticus17_wb_s1 ... _s7: the seven sections (1:1-17, 2, 3 and 4:1-2,
  4:3-35, 5:1-6:7-8, 6:9-7:10, 7:11-38), each building its own verses.
- leviticus17_spec: data (RANGES, CASES, REACH, EXCUSED).

This module keeps the pieces every part shares: the verse text and the
clock (narration_clock on the WEB text and the MP3; a cue the verse doesn't
say fails the build), the files (163, with the nine RANGES), the table's
units from the reference's own layout (table_units), the veil marks, the
size passes (compact, path merging) and the CLI.

QC (leviticus17_bench.qc_file; a file that fails is not written; the report
says why): seams, cues, the motion budget, the 0.3 s region rule, text
(overlap, off its region, under 11 px), timing (nothing after the
narration, the last animation 0.35 s before the MP3 ends), size (aim 70 KB,
refuse over 130 KB); over the run, the section boundaries and coverage
(every unit lit by 7:37, first in a verse that cites it, or REACH/EXCUSED).

    .venv\\Scripts\\python.exe generate_leviticus17_svg.py --out DIR
        [--only 1:1-1:17,3:4] [--qc-only] [--report qc.json]
    .venv\\Scripts\\python.exe generate_leviticus17_svg.py --web

It writes into web/visuals only with --web; importing it writes nothing.
"""

import argparse
import functools
import json
import os
import re
import sys

import config
import narration_clock
import offerings as OF
import passages
import verse_refs
import generate_tabernacle as GT
import generate_tabernacle_reference as R
import leviticus17_spec as SPEC
from svg_chronicles_world import _mp3_seconds
from svg_surface import FONT_FAMILY, _fmt

BOOK = SPEC.BOOK
SAY_LEAD = 0.1
SKELETON = (44, 44, 58)  # a veil's bar, a step off the panel
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


# ---------------------------------------------------------------------------
# Files and the spec
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Size: geometry to a tenth of a px, paths merged
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
    # what every text inherits from the root (its font) or has by default
    # (start) needn't be said again
    cut = out.find(">") + 1 if out.startswith("<svg") else 0
    out = out[:cut] + (out[cut:].replace(_FONT_ATTR, "").replace(' text-anchor="start"', ""))
    return _merge_paths(out)


_FONT_ATTR = f' font-family="{FONT_FAMILY}"'


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


def build(only=None, out_dir=None, web=False, qc_only=False, echo=print, report=None):
    """Build the whole timeline (every section, so seams are right), render
    the files `only` names (all by default), QC each and write those that
    pass. Returns (reports, run)."""
    import leviticus17_bench as B
    B.build_timeline(force=True)
    reports = []

    def wanted(fk):
        return not only or any(cv in only for cv in file_verses(fk))
    for fk in all_files():
        if not wanted(fk):
            continue
        svg = B.render_file(fk)
        rep = B.qc_file(fk, svg)
        rep["ref"] = ref_str(fk)
        rep["written"] = False
        if not rep["problems"] and not qc_only:
            path = out_file(fk, out_dir, web)
            with open(path, "w", encoding="utf-8") as f:
                f.write(svg)
            rep["written"] = path
        reports.append(rep)
        echo(f"{rep['ref']:>8} {rep['section']} {rep['kb']:6.1f} KB  narr {rep['narr']:6.2f}  "
             f"end {rep['last_end']:6.2f}  flights {rep['flights']}  fv {rep['file_views']}  "
             f"{'OK' if not rep['problems'] else 'REFUSED'}")
        for p in rep["problems"]:
            echo(f"           ! {p}")
        for w in rep["warnings"]:
            echo(f"           ~ {w}")
    run = B.run_report(reports, full=not only)
    for p in run["boundaries"]:
        echo(f"  boundary ! {p}")
    for p in run["coverage"]:
        echo(f"  coverage ! {p}")
    echo(f"  run: {len(run['boundaries'])} boundary, {len(run['coverage'])} coverage problems, "
         f"{len(run['pending'])} pending (stub sections: {', '.join(run['stubs']) or 'none'})")
    if report:
        with open(report, "w", encoding="utf-8") as f:
            json.dump(dict(files=reports, run=run, travels=B.TRAVELS,
                           lit={k: [round(v, 2), B.LIT_BY.get(k)] for k, v in B.LIT.items()},
                           cues=[[c[0], list(c[1]), c[2], c[3], c[4]] for c in B.CUES],
                           file_t0={ref_str(fk): round(B.FILE_T0[fk], 3) for fk in all_files()}),
                      f, indent=1, default=str)
    return reports, run


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", help="write under this folder (as <out>/Leviticus/<c>/)")
    ap.add_argument("--web", action="store_true", help="write into web/visuals")
    ap.add_argument("--only", help="verses, e.g. 1:1-1:17,3:4 (the whole timeline is built)")
    ap.add_argument("--qc-only", action="store_true", help="render and check, write nothing")
    ap.add_argument("--report", help="write the QC report (JSON) here")
    a = ap.parse_args(argv)
    if not a.web and not a.out and not a.qc_only:
        ap.error("give --out DIR (or --web to write into web/visuals, or --qc-only)")
    only = parse_only(a.only) if a.only else None
    reports, run = build(only, a.out, a.web, a.qc_only, report=a.report)
    refused = [r for r in reports if r["problems"]]
    print(f"{len(reports)} files, {len(refused)} refused, "
          f"{sum(1 for r in reports if r['written'])} written")
    return 1 if refused or run["boundaries"] or run["coverage"] else 0


if __name__ == "__main__":
    sys.exit(main())
