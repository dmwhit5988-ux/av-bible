"""The Old Testament family tree, laid on a year scale. See docs/design/ot-timeline.md.

Same tree as `generate_ot_family_tree_svg.py` — the Chronicles spine with
every Old Testament join grafted on, and Matthew's tail past Zerubbabel —
but here Y IS TIME. Every box sits at its year, and a rail down the left
says which year that is.

How it differs from the wall chart, and why
-------------------------------------------
* The wall chart's docstring says every generation shares a y. Measured, it
  does not: wrapped sibling rows push later rows down by their whole
  subtree height, and 50 of its 65 depth bands are split, one by 13,000 px.
  So a year rail cannot be hung on that sheet. This one places y from the
  year alone, through ONE monotone map the whole sheet shares.
* The map is piecewise linear, and stretches itself wherever the tree is
  dense in time — no box may sit less than a parent's height above its
  child — so the axis compresses where nothing happens and opens out in
  the monarchy. The tick spacing on the rail shows the reader exactly
  where that happened. A stated break is honest; a silent log scale is not.
* Siblings stay on one row, because rows stacked in time would say those
  brothers were born a century apart. The one exception is a set of
  childless brothers too wide to fit, which is gridded — nothing hangs
  below a leaf, so the grid cannot lie about anybody's descent.
* Dated boxes carry their years. Undated ones sit between the nearest dated
  ancestor and descendant on their line, in proportion to the generations
  between; with no dated descendant, a generation below the parent.

Output: web/visuals/reference/Old_Testament_timeline.svg (+ a viewer page).
"""

import math
import os
import sys
from bisect import bisect_left
from collections import defaultdict
from xml.sax.saxutils import escape

from chronicles_tree import walk
import matthew_tree as MT
import chronology as CH
import generate_ot_family_tree_svg as G
import reference_viewer
from generate_ot_family_tree_svg import (
    measure, draw_edges, draw_node, draw_links, link_routes, subtree_box,
    top_of, _wrap,
    dim,
    BG, PANEL, RULE, SAND, SAND_DIM, TEXT, TEXT_DIM, FAINT, ROYAL, PRIESTLY,
    FEMALE, HOUSE, NOTE_H, SIB_GAP, DROP, ROW_GAP, SPINE, ASPECT, MAST_W,
    F_SUB, F_LEG, F_LEGS)
from svg_surface import SvgCanvas, _fmt, _rgb

OUT_DIR = G.OUT_DIR
STEM = "Old_Testament_timeline"

BASE = 0.55          # px per year before the tree stretches it
RUN_W = 240          # a run of childless brothers wider than this is gridded
GRID_ASPECT = 1.2    # taller than the wall chart's 2.4: nothing hangs below a
                     # leaf, so a grid costs no descent and width is the
                     # whole problem on this sheet (758 of 1,270 are leaves)
MARGIN = 220

# the gutter, left of the tree, right to left
GAP_TREE = 120       # lanes -> tree
LANE_W = 22
LANE_GROUP_GAP = 36
RAIL_LABEL_W = 150   # room right of the rail for "2348 BC · AM 1656"
EVENT_LABEL_W = 330  # room left of the rail for event names
ZONE_TITLE_W = 70
RIGHT_RAIL_W = 420

DATE_COL = {"life": SAND, "reign": ROYAL, "at": TEXT_DIM}

YOFF = {}            # node -> extra y inside a leaf grid (N has __slots__)


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

UNITS = {}           # node -> its children as a list of units (see below)


def _grid(run):
    """A run of childless brothers, wrapped into rows. The row width is
    chosen from the block's area, as the wall chart does."""
    widest = max(k.w for k in run)
    area = sum((k.w + SIB_GAP) * k.h for k in run)
    cap = max(widest, math.sqrt(area * GRID_ASPECT))
    rows, row, rw = [], [], 0.0
    for k in run:
        step = k.w + (SIB_GAP if row else 0)
        if row and rw + step > cap:
            rows.append(row)
            row, rw = [k], k.w
        else:
            row.append(k)
            rw += step
    if row:
        rows.append(row)
    w = max(sum(k.w for k in r) + SIB_GAP * (len(r) - 1) for r in rows) + SPINE
    h = sum(max(k.h for k in r) for r in rows) + ROW_GAP * (len(rows) - 1)
    return {"kind": "grid", "rows": rows, "w": w, "h": h}


def arrange_t(n, dated):
    """Widths only; heights are the year map's business.

    A node's children become a single row of UNITS, in birth order. A child
    with descent of its own is a unit by itself. A run of two or more
    childless brothers too wide to sit flat is one unit — a grid, wrapped
    into rows. Nothing hangs below a leaf, so a grid cannot collide with
    anybody's descent, and a brother in its second row is at most a box's
    height below where his year would put him.
    """
    measure(n)
    if n in dated:
        n.h += NOTE_H + 3                          # a line for the years
    for k in n.kids:
        arrange_t(k, dated)
    n.rows = [list(n.kids)]
    if not n.kids:
        n.sw, n.sh = n.w, n.h
        UNITS[n] = []
        return n
    units, run = [], []

    def flush():
        if not run:
            return
        flat = sum(k.w for k in run) + SIB_GAP * (len(run) - 1)
        if len(run) >= 2 and flat > RUN_W:
            units.append(_grid(run))
        else:
            for k in run:
                units.append({"kind": "one", "node": k, "w": k.sw, "h": k.sh})
        run.clear()

    for k in n.kids:
        if k.kids:
            flush()
            units.append({"kind": "one", "node": k, "w": k.sw, "h": k.sh})
        else:
            run.append(k)
    flush()
    UNITS[n] = units
    block_w = sum(u["w"] for u in units) + SIB_GAP * (len(units) - 1)
    n.sw = max(n.w, block_w)
    n.sh = n.h + DROP + max(u["h"] for u in units)
    return n


def year_map(nodes, year):
    """-> (sorted years, {year: y}). One monotone map for the whole sheet:
    BASE px per year, stretched wherever a parent would otherwise sit on
    top of its child."""
    need = defaultdict(list)
    for n in nodes:
        if n.parent is not None:
            need[year[n]].append((year[n.parent], n.parent.h + DROP))
    ts = sorted(set(year.values()))
    Y, prev = {}, None
    for tv in ts:
        y = 0.0 if prev is None else Y[prev] + BASE * (tv - prev)
        for tp, gap in need[tv]:
            y = max(y, Y[tp] + gap)
        Y[tv] = y
        prev = tv
    return ts, Y


class Scale:
    def __init__(self, ts, Y):
        self.ts, self.ys = ts, [Y[t] for t in ts]

    def __call__(self, t):
        ts, ys = self.ts, self.ys
        i = bisect_left(ts, t)
        if i == 0:
            return ys[0] - BASE * (ts[0] - t)
        if i >= len(ts):
            return ys[-1] + BASE * (t - ts[-1])
        t0, t1, y0, y1 = ts[i - 1], ts[i], ys[i - 1], ys[i]
        return y0 + (y1 - y0) * (t - t0) / (t1 - t0)


def place_t(n, cx, scale, year):
    n.x = cx - n.w / 2
    n.y = top_of(n, scale(year[n]) + YOFF.get(n, 0.0))
    if not n.kids:
        return
    units = UNITS[n]
    total = sum(u["w"] for u in units) + SIB_GAP * (len(units) - 1)
    x = cx - total / 2
    for u in units:
        if u["kind"] == "one":
            k = u["node"]
            YOFF[k] = 0.0
            place_t(k, x + u["w"] / 2, scale, year)
        else:
            u["x0"] = x
            off = 0.0
            for r in u["rows"]:
                rx = x + SPINE
                for k in r:
                    YOFF[k] = off
                    place_t(k, rx + k.w / 2, scale, year)
                    rx += k.w + SIB_GAP
                off += max(k.h for k in r) + ROW_GAP
        x += u["w"] + SIB_GAP


def draw_edges_t(c, n):
    """The wall chart's edge drawing, for units: an ordinary bus and drop
    for each child with descent, and for a grid a rail down its left with a
    shelf out to each row."""
    if not n.kids:
        return
    py = n.y + n.h
    pcx = n.x + n.w / 2
    units = UNITS[n]
    bus = min(k.y for k in n.kids if YOFF.get(k, 0.0) == 0.0) - DROP / 2
    c.line((pcx, py), (pcx, bus), SAND_DIM, 1.5)
    xs = [pcx]
    for u in units:
        if u["kind"] == "one":
            xs.append(u["node"].x + u["node"].w / 2)
        else:
            xs.append(u["x0"] + 8)
    if max(xs) - min(xs) > 1:
        c.line((min(xs), bus), (max(xs), bus), SAND_DIM, 1.5)
    for u in units:
        if u["kind"] == "one":
            G._drop(c, u["node"], bus)
            continue
        rail = u["x0"] + 8
        shelves = [min(k.y for k in r) - DROP / 2 for r in u["rows"]]
        c.line((rail, bus), (rail, shelves[-1]), SAND_DIM, 1.5)
        for r, shelf in zip(u["rows"], shelves):
            right = max(k.x + k.w / 2 for k in r)
            c.line((rail, shelf), (right, shelf), SAND_DIM, 1.4)
            for k in r:
                G._drop(c, k, shelf)
    for k in n.kids:
        draw_edges_t(c, k)


# ---------------------------------------------------------------------------
# Furniture
# ---------------------------------------------------------------------------

def rtext(c, x, y, s, size, fill, angle, anchor="middle", bold=False,
          italic=False):
    """Rotated text — the canvas has no rotation, so emit it raw."""
    a = [f'x="{_fmt(x)}"', f'y="{_fmt(y)}"', f'font-size="{_fmt(size)}"',
         f'text-anchor="{anchor}"', 'dominant-baseline="middle"',
         f'fill="{_rgb(fill)}"', 'font-family="Georgia, serif"',
         f'transform="rotate({angle} {_fmt(x)} {_fmt(y)})"']
    if len(fill) > 3 and fill[3] < 255:
        a.append(f'fill-opacity="{fill[3] / 255:.3f}"')
    if bold:
        a.append('font-weight="bold"')
    if italic:
        a.append('font-style="italic"')
    c.raw([f"<text {' '.join(a)}>{escape(s)}</text>"])


def draw_zones(c, scale, x_title, x0, x1):
    for i, (z0, z1, title, _) in enumerate(CH.ZONES):
        y0, y1 = scale(CH.am(z0)), scale(CH.am(z1))
        if i % 2 == 0:
            c.rect(x0, y0, x1 - x0, y1 - y0, fill=dim(PANEL, 0.35))
        c.line((x0, y0), (x1, y0), dim(RULE, 0.9), 1.0)
        rtext(c, x_title, (y0 + y1) / 2, title, 34, dim(SAND, 0.42), -90,
              bold=True)
        c.text((x_title + 26, y0 + 18), f"{z0} – {z1} BC", 13,
               dim(FAINT, 0.9), anchor="lm", italic=True)


def draw_events(c, scale, rail_x, x1):
    for yr, label, strong in CH.EVENTS:
        y = scale(CH.am(yr))
        if strong:
            c.line((rail_x, y), (x1, y), dim(SAND, 0.5), 1.6, dash="12 8")
            c.text((rail_x - 14, y - 5), label, 17, dim(SAND, 0.95),
                   anchor="rb", bold=True)
            sub = f"{yr} BC · AM {CH.am(yr)}"
            c.text((rail_x - 14, y + 7), sub, 12, dim(TEXT_DIM, 0.95),
                   anchor="rt", italic=True)
        else:
            c.line((rail_x, y), (x1, y), dim(FAINT, 0.75), 1.0, dash="4 7")
            c.text((rail_x - 14, y - 4), label, 13, dim(TEXT_DIM, 0.95),
                   anchor="rb", italic=True)
            c.text((rail_x - 14, y + 6), f"{yr} BC", 11, dim(FAINT, 1.0),
                   anchor="rt")


def draw_rail(c, scale, rail_x, t_end):
    c.line((rail_x, scale(0) - 40), (rail_x, scale(t_end) + 40),
           dim(SAND, 0.8), 2.0)
    for t in range(0, int(t_end) + 100, 100):
        y = scale(t)
        big = t % 500 == 0
        c.line((rail_x - (10 if big else 5), y), (rail_x + (10 if big else 5), y),
               dim(SAND, 0.9 if big else 0.6), 1.6 if big else 1.0)
        c.text((rail_x + 16, y), f"{CH.bc(t)} BC", 14 if big else 11,
               dim(TEXT, 0.95) if big else dim(TEXT_DIM, 0.9), anchor="lm",
               bold=big)
        if big:
            c.text((rail_x + 16, y + 15), f"AM {t}", 10, dim(FAINT, 1.0),
                   anchor="lm", italic=True)


def draw_modern_rail(c, scale, x, t_end):
    y_top = scale(CH.am(1095)) - 60
    c.text((x, y_top - 26), "THE MODERN COUNT", 15, dim(SAND, 0.85),
           anchor="lt", bold=True)
    for line in _wrap("Thiele's dates, on the Assyrian eponym canon. "
                      "Where the two rails disagree, the sheet is placed "
                      "on the left-hand one.", F_LEGS, RIGHT_RAIL_W - 40):
        y_top += 16
        c.text((x, y_top), line, 12, dim(FAINT, 1.0), anchor="lt",
               italic=True)
    c.line((x, scale(CH.am(1095))), (x, scale(t_end) + 40),
           dim(SAND_DIM, 0.8), 1.4, dash="2 5")
    for ussher, modern, label in CH.MODERN:
        y = scale(CH.am(ussher))
        c.line((x - 8, y), (x + 8, y), dim(SAND, 0.8), 1.4)
        drift = modern - ussher
        tag = f"{modern} BC" + (f"  ({'+' if drift > 0 else ''}{drift})"
                                if drift else "")
        c.text((x + 16, y - 2), tag, 14, dim(TEXT, 0.95), anchor="lb",
               bold=True)
        c.text((x + 16, y + 12), label, 12, dim(TEXT_DIM, 0.95), anchor="lt",
               italic=True)


def _ancestor_labels(n):
    out = set()
    p = n.parent
    while p is not None:
        out.add(p.label)
        p = p.parent
    return out


def lanes(items, scale):
    """Greedy interval packing. items: [(n, d)] -> [(n, d, lane)]."""
    items = sorted(items, key=lambda nd: nd[1].t0)
    ends, out = [], []
    for n, d in items:
        y0, y1 = scale(d.t0), scale(d.t1)
        for i, e in enumerate(ends):
            if e + 6 < y0:
                ends[i] = y1
                out.append((n, d, i))
                break
        else:
            ends.append(y1)
            out.append((n, d, len(ends) - 1))
    return out, len(ends)


def draw_lanes(c, scale, dated, x_left):
    """Lifespans and reigns as bars in the gutter, in three groups."""
    lives = [(n, d) for n, d in dated.items() if d.kind == "life"]
    reigns = [(n, d) for n, d in dated.items() if d.kind == "reign"]
    israel = [(n, d) for n, d in reigns
              if _ancestor_labels(n) & {"the kings of Israel", "Nebat",
                                        "Ahijah"}]
    judah = [(n, d) for n, d in reigns if (n, d) not in israel]
    x = x_left
    for title, col, group in [("LIVES THE TEXT MEASURES", SAND, lives),
                              ("SAUL · DAVID · JUDAH", ROYAL, judah),
                              ("ISRAEL", ROYAL, israel)]:
        packed, width = lanes(group, scale)
        top = min(scale(d.t0) for _, d in group)
        c.text((x, top - 34), title, 13, dim(SAND, 0.85), anchor="lt",
               bold=True)
        c.line((x, top - 16), (x + width * LANE_W - 4, top - 16),
               dim(SAND_DIM, 0.7), 1.0)
        for n, d, lane in packed:
            bx = x + lane * LANE_W
            y0, y1 = scale(d.t0), max(scale(d.t1), scale(d.t0) + 6)
            fill = dim(col, 0.28 if d.soft else 0.5)
            c.rect(bx, y0, LANE_W - 5, y1 - y0, fill=fill,
                   stroke=dim(col, 0.9), width=1.0, rx=3)
            label = n.label.split(" · ")[-1]
            rtext(c, bx + (LANE_W - 5) / 2, y0 + 8, label, 11,
                  dim(TEXT, 0.95), 90, anchor="start", bold=d.kind == "reign")
        x += width * LANE_W + LANE_GROUP_GAP
    return x


def draw_dates(c, dated):
    for n, d in dated.items():
        col = DATE_COL[d.kind]
        if d.kind == "life":
            s = f"{CH.bc(d.t0)} – {CH.bc(d.t1)} BC"
        elif d.kind == "reign":
            s = (f"reigned {CH.bc(d.t0)} BC" if d.t0 == d.t1
                 else f"reigned {CH.bc(d.t0)} – {CH.bc(d.t1)} BC")
        else:
            s = f"{'c. ' if d.soft else ''}{CH.bc(d.t0)} BC"
        c.text((n.x + G.PAD_X, n.y + n.h - NOTE_H / 2 - 2), s, 10,
               dim(col, 0.95), anchor="lm", bold=d.kind != "at",
               italic=d.kind == "at")


def draw_luke(c, scale, x):
    """Luke's eighteen names, floating through the silence in the gutter."""
    y0, y1 = scale(CH.am(536)), scale(CH.am(4))
    c.text((x, y0 - 34), "LUKE 3:23-27", 13, dim(SAND, 0.85), anchor="lt",
           bold=True)
    for i, line in enumerate(_wrap("the other line through the silence — "
                                   "eighteen names between Zerubbabel and "
                                   "Joseph, none of them Matthew's",
                                   F_LEGS, 230)):
        c.text((x, y0 - 16 + i * 15), line, 11, dim(FAINT, 1.0),
               anchor="lt", italic=True)
    names = ["Zerubbabel"] + CH.LUKE_TAIL + ["Joseph"]
    top, bottom = y0 + 70, y1 - 30
    step = (bottom - top) / (len(names) - 1)
    lx = x + 8
    c.line((lx, top), (lx, bottom), dim(SAND_DIM, 0.8), 1.3, dash="4 4")
    for i, name in enumerate(names):
        y = top + i * step
        end = i in (0, len(names) - 1)
        c.circle(lx, y, 3.2 if end else 2.4, fill=BG,
                 stroke=dim(SAND, 0.9 if end else 0.6), width=1.1)
        c.text((lx + 12, y), name, 12 if end else 11,
               dim(TEXT, 0.95) if end else dim(TEXT_DIM, 0.95), anchor="lm",
               bold=end)


# Each band's anchor is a locator (chronology.locate), never a bare name: a
# repeated name would frame whichever namesake comes first. A band whose
# locator does not resolve stops the build instead of going missing.
REGION_LOC = {
    "Cain": ("root", "Cain"),
    "Nahor": ("Terah", "Nahor"),
    "Japheth": ("Noah", "Japheth"),
    "Ham": ("Noah", "Ham"),
    "Ishmael": ("Abraham", "Ishmael"),
    "Keturah": ("Abraham", "Keturah"),
    "Esau": ("Isaac", "Esau"),
    "David": ("David",),
    "Judah": ("Judah",),
}


def draw_regions_t(c, T, at):
    boxes = []
    for label, title, sub in G.REGIONS:
        loc = REGION_LOC.get(label, ("Jacob", label))
        if loc[0] == "Noah":
            loc = CH._chain(CH._G5)[-1] + loc[1:]
        n = CH.locate(T, at, loc)
        boxes.append((subtree_box(n), title, sub))
    boxes.sort(key=lambda b: -((b[0][2] - b[0][0]) * (b[0][3] - b[0][1])))
    for (x0, y0, x1, y1), title, sub in boxes:
        c.rect(x0, y0, x1 - x0, y1 - y0, fill=dim(PANEL, 0.30),
               stroke=dim(RULE, 0.95), width=1.2, rx=18)
        c.text((x0 + 20, y0 - 40), title, 30, dim(SAND, 0.62),
               anchor="lm", bold=True)
        c.text((x0 + 20, y0 - 16), sub, 15, dim(FAINT, 0.95),
               anchor="lm", italic=True)


def draw_masthead(c, x, y, stats):
    c.text((x, y), "THE SAME TREE, IN TIME:", 21, dim(SAND, 0.8),
           anchor="lt", italic=True)
    c.text((x, y + 34), "THE OLD", 76, TEXT, anchor="lt", bold=True)
    c.text((x, y + 116), "TESTAMENT", 76, TEXT, anchor="lt", bold=True)
    sy = y + 208
    for para, col in [
        ("Every person the Old Testament gives a join for, on a year "
         "scale. A box sits at its first dated year — birth where the text "
         "gives it, accession for a king — and the rail on the left says "
         "which year that is.", TEXT_DIM),
        ("Only %(dated)d of the %(people)d people here can be dated at "
         "all. Those boxes carry their years. Everyone else sits between "
         "the nearest dated ancestor and descendant on their line, in "
         "proportion to the generations between; with no dated descendant, "
         "a generation below the parent. That is a placing, not a date." %
         stats, TEXT_DIM),
        ("Years are Ussher's, as the Authorized Version printed them: "
         "creation 4004 BC, the Masoretic ages in Genesis 5 and 11, Abram "
         "born when Terah was 130. The right-hand rail shows where the "
         "modern count differs.", FAINT),
    ]:
        for line in _wrap(para, F_SUB, MAST_W - 40):
            c.text((x, sy), line, 19, dim(col, 0.95), anchor="lt",
                   italic=True)
            sy += 28
        sy += 10

    ly = sy + 24
    c.text((x, ly), "HOW TO READ THE SCALE", 15, dim(SAND, 0.85),
           anchor="lt", bold=True)
    ly += 30
    for line in _wrap("The scale is not even, and says so. It opens out "
                      "wherever the tree is dense — no box may sit closer "
                      "to its father than his box is tall — and closes up "
                      "where nothing is recorded. Read the spacing of the "
                      "century marks on the rail to see where.",
                      F_LEG, MAST_W - 40):
        c.text((x, ly), line, 14, TEXT_DIM, anchor="lt")
        ly += 19
    ly += 14
    rows = [(SAND, "a life the text measures, birth to death"),
            (ROYAL, "a reign — accession to end; overlaps are co-regencies"),
            (TEXT_DIM, "a person placed by one event the text ties him to")]
    for col, what in rows:
        c.rect(x + 4, ly - 8, 30, 16, fill=dim(col, 0.4), stroke=col,
               width=1.2, rx=3)
        c.text((x + 48, ly), what, 14, TEXT_DIM, anchor="lm")
        ly += 26
    c.rect(x + 4, ly - 8, 30, 16, fill=dim(SAND, 0.15), stroke=dim(SAND, 0.6),
           width=1.2, rx=3)
    c.text((x + 48, ly), "paler: an approximate placing", 14, TEXT_DIM,
           anchor="lm")
    ly += 26

    ly += 18
    c.text((x, ly), "FIVE STRETCHES OF THE SHEET", 15, dim(SAND, 0.85),
           anchor="lt", bold=True)
    ly += 28
    for z0, z1, title, what in CH.ZONES:
        c.text((x, ly), f"{title}  ·  {z0} – {z1} BC", 13, dim(SAND, 0.9),
               anchor="lt", bold=True)
        ly += 20
        for line in _wrap(what, F_LEGS, MAST_W - 60):
            c.text((x, ly), line, 12, dim(FAINT, 0.98), anchor="lt",
                   italic=True)
            ly += 17
        ly += 10

    ly += 12
    c.text((x, ly), "WHAT THIS SHEET WILL NOT DO", 15, dim(SAND, 0.85),
           anchor="lt", bold=True)
    ly += 28
    notes = [
        "It will not settle the forks. The Septuagint's ages put creation "
        "some 1,400 years earlier; Exodus 12:40 reads 430 years in Egypt "
        "or 215; 1 Kings 6:1 reads 480 or 440. The sheet takes one reading "
        "of each and names it.",
        "It will not bridge Jaddua to Joseph. The text does not, and "
        "Matthew's ten names across those five centuries — fifty years a "
        "generation — are a pattern of fourteens, not a census.",
        "It will not give Jesus a year. Ussher's 4 BC is AM 4000; Herod "
        "died in 4 BC; Luke's census under Quirinius is AD 6.",
    ]
    for t in notes:
        for line in _wrap(t, F_LEGS, MAST_W - 60):
            c.text((x, ly), line, 12, dim(FAINT, 0.98), anchor="lt",
                   italic=True)
            ly += 18
        ly += 10
    return ly


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def build_svg():
    T, at = MT.build()
    root = T.root
    dated = CH.bind(T, at)
    year = CH.estimate(root, dated)

    arrange_t(root, dated)
    nodes = list(walk(root))
    ts, Y = year_map(nodes, year)
    scale = Scale(ts, Y)
    place_t(root, 0, scale, year)

    xs0 = min(n.x for n in nodes)
    xs1 = max(n.x + n.w for n in nodes)
    t_end = max(ts)
    ys1 = max(n.y + n.h for n in nodes)

    # the gutter, laid out right to left from the tree's edge
    lanes_right = xs0 - GAP_TREE
    lives = [(n, d) for n, d in dated.items() if d.kind == "life"]
    reigns = [(n, d) for n, d in dated.items() if d.kind == "reign"]
    n_lanes = (lanes(lives, scale)[1] + lanes(reigns, scale)[1] + 2)
    lanes_left = lanes_right - n_lanes * LANE_W - 2 * LANE_GROUP_GAP
    rail_x = lanes_left - RAIL_LABEL_W
    zone_x = rail_x - EVENT_LABEL_W - ZONE_TITLE_W
    mast_x = zone_x - 40 - MAST_W
    right_x = xs1 + 80

    left = mast_x - MARGIN
    top = -MARGIN - 90
    W = (right_x + RIGHT_RAIL_W + MARGIN) - left
    H = (ys1 + MARGIN) - top

    c = SvgCanvas(W, H, bg=BG)
    c._els.insert(0, f'<g transform="translate({_fmt(-left)} {_fmt(-top)})">')

    draw_zones(c, scale, zone_x, zone_x - 30, right_x + RIGHT_RAIL_W)
    draw_regions_t(c, T, at)
    draw_events(c, scale, rail_x, right_x + RIGHT_RAIL_W)
    draw_rail(c, scale, rail_x, t_end)
    draw_modern_rail(c, scale, right_x, t_end)
    gx = draw_lanes(c, scale, dated, lanes_left)
    draw_luke(c, scale, lanes_left)

    draw_edges_t(c, root)
    routes = link_routes(T)
    draw_links(c, routes)
    for n in nodes:
        draw_node(c, n)
    draw_dates(c, dated)
    draw_links(c, routes, dots=True)

    people = sum(1 for n in nodes if n.kind != "house" and n.chip is None)
    stats = {"people": people, "dated": len(dated), "nodes": len(nodes)}
    draw_masthead(c, mast_x, top + 130, stats)

    c._emit("</g>")
    body = "\n".join(c._els)
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {_fmt(W)} {_fmt(H)}" width="{_fmt(W)}" '
        f'height="{_fmt(H)}" data-kind="genealogy" '
        f'data-title="The Old Testament family tree, in time">\n'
        f'<title>The Old Testament family tree, in time — '
        f'Adam to Jesus on a year scale</title>\n'
        f'{body}\n</svg>\n')
    return svg, W, H, stats


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    svg, W, H, stats = build_svg()
    path = os.path.join(OUT_DIR, STEM + ".svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    vp = os.path.join(OUT_DIR, STEM + ".html")
    with open(vp, "w", encoding="utf-8") as f:
        f.write(reference_viewer.page(STEM, _fmt(W), _fmt(H),
                                      "The Old Testament family tree, in time"))
    size = os.path.getsize(path) / 1024
    print(path)
    print(f"  {stats['nodes']} nodes, {stats['dated']} dated · "
          f"{W:.0f} x {H:.0f} px · {size:.0f} KB")
    print(vp)
    return 0


if __name__ == "__main__":
    sys.exit(main())
