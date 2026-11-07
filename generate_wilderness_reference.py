"""The wilderness journey: the forty-two camps of Numbers 33, from Rameses to
the plains of Moab, on a map of Egypt's east, the Sinai and the land east of
the Jordan, beside a strip of the forty years with the text's own dates.

Writes web/visuals/reference/Wilderness_journey.svg, its sidecar
Wilderness_journey.json and the viewer page Wilderness_journey.html
(reference_viewer.page). The coasts are point facts: sinai.py's gulfs,
lakes and Nile, gazetteer's Levant (the coast, the Salt Sea, the Jordan,
the Arnon, the Zered, the brook of Egypt) and mediterranean.AFRICA's delta
coast. The camps, events, dates and lines between camps are wilderness.py's.
No line is traced from a map.

The sheet, north up, 1,000 px a degree of latitude (about 9 px a km), with
the strip of the forty years in a column to its right:

- **The route** is the traditional southern one, a dashed line through the
  camps in Numbers 33's order. A camp with a site is a dot in its
  certainty's style (filled where known, a thick ring where probable, a
  thin ring where possible, a dashed ring where held by tradition); a camp
  with none is a small bead on the line, spaced evenly between its
  neighbours, which claims no place. Each is numbered in Numbers 33's
  order, and the names come in as you zoom. The sea crossing is a dashed
  span over the water where tradition puts it; the plains of Moab are a bar
  between their two ends.
- **Events** (a layer, on): what happened at a camp, or between two camps
  where the text names none, in a small labelled list beside it.
- **Other itineraries** (a layer, off): the lists of Numbers 21,
  Deuteronomy 10, Deuteronomy 2 and Judges 11, as lists, never as points.
- **The forty years**: the text's dates on a broken time line, years 1 and 2
  by month, years 3 to 39 closed up, year 40 and the first month of year 41
  by month; the lengths of time it gives as bars where they can be dated,
  and as a list where they can't. Its two columns are two views (years 1
  and 2, years 3 to 41), so a phone opens on a column at a size it can
  read.

A camp's card gives its Numbers 33 verses, its site and how sure that is,
or that it is not identified and where it is drawn, where Numbers 33 and
the narrative differ, what happened there, its dates and its verses. A
leg's card steps to the leg before and after, glowing along its line.
Opened from a verse, the sheet starts on the camps that verse names, or the
camp or event whose passage it falls in.

    .venv\\Scripts\\python.exe generate_wilderness_reference.py
"""

import json
import math
import os
import re

import gazetteer as GZ
import mediterranean as M
import near_east as NE
import reference_viewer
import sinai as S
import wilderness as WD
from books import BOOK_NAMES
from config import VISUALS_DIR
from generate_israel_atlas import (COAST_LINE, DOT, GRID, LAKE, TEXT_WEB, _bx, box_of, finds,
                                   hits, overlap, range_rows, rows, shown_rows,
                                   smooth, text, verses)
from generate_tabernacle import BG, SAND, SAND_DIM, TEXT, TEXT_DIM
from generate_tribal_maps import LAND, RIVER, SEA, WATER_TXT
from svg_map_camera import Projection, ink, seg_hits_rect
from svg_surface import SvgCanvas, _fmt, _rgb

OUT_DIR = os.path.join(VISUALS_DIR, "reference")
STEM = "Wilderness_journey"
TITLE = "The wilderness journey"

LAT_TOP, LAT_BOT, LON_L, LON_R = 32.20, 27.50, 31.00, 36.40
K = 1000                                    # px per degree of latitude
PROJ = Projection(LAT_TOP, LON_L, (LAT_TOP + LAT_BOT) / 2, K)
MAP_W = round((LON_R - LON_L) * PROJ.eff * K)
MAP_H = round((LAT_TOP - LAT_BOT) * K)
KM = K / 111.2                              # px per km
COL_W = 1900                                # the right column: the strip, the lists, the key
X0 = MAP_W
W, H = MAP_W + COL_W, MAP_H

ROUTE = (228, 180, 96)
ROUTE_TXT = (244, 204, 126)
SPAN_COL = (240, 220, 160)
EVENT = (232, 134, 114)
EVENT_TXT = (240, 206, 192)
LANDMARK = (150, 146, 130)
LANDMARK_TXT = (168, 162, 144)
REGION_TXT = (150, 138, 104)
VARIANT_TXT = (206, 196, 168)
PANEL = (20, 20, 30)
DERIVED = (190, 170, 120)                   # a length worked out from two dates

FS_NUM = 26
TIERS = {"B": (52, 11), "C": (32, 8), "D": (24, 5)}       # (font, dot radius)
MAJOR = {"rameses", "wilderness_of_sinai", "kadesh", "mount_hor", "ezion_geber",
         "plains_of_moab"}
BEAD_R = 5
FS_EVENT = 22
FS_LANDMARK = 24
FS_REGION, FS_REGION_SMALL, REGION_FADE = 72, 52, 40
FS_VARIANT = 26
FS_KEY = 30
FS_TITLE = 112

MAST = (60, 60, 2300, 420)             # the title block, in the great sea

LANDMARKS = ["jerusalem", "jericho", "gilgal_jericho", "arad", "hormah"]

# where the waters' names sit: (lat, lon, size, anchor, rotate)
WATER_LABELS = {
    "great_sea": (31.78, 33.55, 64, "mm", 0),
    "red_sea": (27.60, 34.62, 56, "mm", 0),
    "gulf_suez": (28.42, 33.22, 30, "mm", -56),
    "gulf_aqaba": (28.62, 34.73, 30, "mm", -72),
    "salt_sea": (31.45, 35.475, 26, "mm", -90),
    "nile": (29.30, 31.30, 34, "mm", 0),
    "jordan": (32.10, 35.585, 24, "lm", 0),
    "arnon": (31.405, 35.70, 22, "ma", 0),
    "zered": (31.00, 35.70, 22, "ma", 0),
    "brook_of_egypt": (30.98, 33.98, 22, "lm", 0),
    "timsah": (30.62, 32.36, 22, "lm", 0),
    "bitter": (30.36, 32.50, 22, "lm", 0),
    "bardawil": (31.02, 33.12, 22, "ma", 0),
}
WATER_TEXT = {
    "great_sea": "The great sea", "red_sea": "Red Sea", "gulf_suez": "Gulf of Suez",
    "gulf_aqaba": "Gulf of Aqaba", "salt_sea": "Salt Sea", "nile": "Nile",
    "jordan": "Jordan", "arnon": "Arnon", "zered": "Zered",
    "brook_of_egypt": "brook of Egypt", "timsah": "Lake Timsah", "bitter": "Bitter Lakes",
    "bardawil": "Lake Bardawil",
}
MODERN = {"gulf_suez", "gulf_aqaba", "timsah", "bitter", "bardawil"}


def P(lat, lon):
    return PROJ.P(lat, lon)


def _plains_label():
    """The plains of Moab's name up and to the right of its north end, east
    of the Jordan."""
    s = WD.ENDS["shittim"].site
    x, y = P(s.lat, s.lon)
    return [("ld", x + 16, y - 26, False)]


def _west_of(key):
    """A landmark's name to the left of its dot."""
    g = GZ.SITES[key]
    x, y = P(g.lat, g.lon)
    return [("rm", x - 12, y, False)]


# a label's own first choice, where the placer's would mislead: Jerusalem's
# name west of its dot, clear of Beth Jeshimoth's
PREFER = {"plains_of_moab": _plains_label(), "lm-jerusalem": _west_of("jerusalem")}
# an events list's top left corner (lat, lon), where the placer's would
# mislead: the plains' list north of its name, not across the Jordan, and
# Jotbathah's over its name, clear of the line back north from Ezion Geber
EVENT_PREFER = {"plains_of_moab": (32.125, 35.72), "jotbathah": (29.745, 34.903)}
# the lists that run on from the end of their camp's name, with no leader:
# the mountains of Abarim's, which would otherwise cross the Jordan
EVENT_AFTER_NAME = {"mountains_of_abarim"}
# the lists kept east of the point they hang from, off the Jordan valley:
# Sihon and Og's, told between Dibon Gad and the plains
EVENT_EAST = {("dibon_gad", "plains_of_moab")}
EVENT_APART = 40                            # the least gap between two events lists


# ---------------------------------------------------------------------------
# The land
# ---------------------------------------------------------------------------

def africa_west():
    """mediterranean.AFRICA from the brook of Egypt west, to its first point
    off the sheet's west edge."""
    out = []
    for p in M.AFRICA[1:]:
        out.append(p)
        if p[1] < LON_L - 0.3:
            break
    return out


def land_ring():
    """The land as one ring: the Levant's coast and the delta's, round the
    sheet's west and south edges, up the Gulf of Suez and down the Sinai,
    up the Gulf of Aqaba and down the Arabian shore, and round the sheet's
    east and north edges."""
    west = africa_west()
    lo = LAT_BOT - 1
    return (GZ.COAST + west
            + [(lo, west[-1][1]), (lo, S.SUEZ_WEST_SHORE[0][1])]
            + S.SUEZ_WEST_SHORE + S.SINAI_WEST_SHORE[1:] + S.SINAI_EAST_SHORE[1:]
            + S.ARABIA_EAST_SHORE[1:]
            + [(lo, S.ARABIA_EAST_SHORE[-1][1]), (lo, LON_R + 1), (LAT_TOP + 2, LON_R + 1),
               (LAT_TOP + 2, GZ.COAST[0][1])])


COASTS = [GZ.COAST, M.AFRICA, S.SUEZ_WEST_SHORE, S.SINAI_WEST_SHORE, S.SINAI_EAST_SHORE,
          S.ARABIA_EAST_SHORE]
LAKES = list(S.LAKES.values()) + [GZ.LAKES["salt_sea"], GZ.LAKES["galilee"]]
ISLANDS = list(S.ISLANDS.values())
RIVERS = [S.NILE, NE.NILE_ROSETTA] + [GZ.RIVERS[k] for k in
                                      ("jordan_lower", "arnon", "zered", "brook_of_egypt",
                                       "jabbok")]


def draw_base(c):
    with c.group(data={"fs": 30}):
        for lat in range(28, 33):
            y = P(lat, LON_L)[1]
            c.line((0, y), (MAP_W, y), GRID, 1.5)
            text(c, (MAP_W - 14, y - 8), f"{lat}°N", 30, GRID, "rd")
        for lon in range(32, 37):
            x = P(LAT_TOP, lon)[0]
            c.line((x, 0), (x, H), GRID, 1.5)
            text(c, (x + 10, H - 14), f"{lon}°E", 30, GRID, "ld")
    c.path(smooth(PROJ.PS(land_ring()), closed=True), fill=LAND)
    for ring in ISLANDS:
        c.path(smooth(PROJ.PS(ring), closed=True), fill=LAND, stroke=COAST_LINE, width=2)
    for line in COASTS:
        c.path(smooth(PROJ.PS(line)), stroke=COAST_LINE, width=2.5)
    for line in RIVERS:
        c.path(smooth(PROJ.PS(line)), stroke=RIVER, width=3.5, linecap="round")
    for ring in LAKES:
        c.path(smooth(PROJ.PS(ring), closed=True), fill=LAKE, stroke=COAST_LINE, width=2)


# ---------------------------------------------------------------------------
# The route: the line through the camps, and where each camp stands on it
# ---------------------------------------------------------------------------

def site_point(key):
    """(lat, lon) of a camp drawn at a point, or None."""
    if key == "crossing_w":
        return WD.CROSSING_SPAN[0]
    if key == "crossing_e":
        return WD.CROSSING_SPAN[-1]
    s = WD.STATION[key]
    if s.site:
        return (s.site.lat, s.site.lon)
    if s.ends:
        a, b = (WD.ENDS[k].site for k in s.ends)
        return ((a.lat + b.lat) / 2, (a.lon + b.lon) / 2)
    return None


def nodes():
    """The camps in order, with the crossing's two shores after Pihahiroth."""
    out = []
    for s in WD.STATIONS:
        out.append(s.key)
        if s.key == "pihahiroth":
            out += ["crossing_w", "crossing_e"]
    return out


def bezier(pts):
    """The route's curve: [(p, c0, c1, q)] per segment. As smooth(), the
    tangent at a point runs from the point before to the point after, each
    handle a third of its own segment; but where the line turns sharply
    (Kadesh, Ezion Geber) the handles shrink with the turn, so the curve
    turns at the camp and doesn't swing past it."""
    n = len(pts)
    if n < 3:
        return [(p, p, q, q) for p, q in zip(pts, pts[1:])]

    def unit(a, b):
        dx, dy = b[0] - a[0], b[1] - a[1]
        m = math.hypot(dx, dy) or 1
        return dx / m, dy / m

    def tangent(i):
        return unit(pts[max(i - 1, 0)], pts[min(i + 1, n - 1)])

    def ease(i):
        """1 where the line runs straight on, falling to 0 as it turns back."""
        if i == 0 or i == n - 1:
            return 1.0
        a, b = unit(pts[i - 1], pts[i]), unit(pts[i], pts[i + 1])
        return max(0.0, min(1.0, (1 + a[0] * b[0] + a[1] * b[1]) / 2))
    out = []
    for i in range(n - 1):
        p, q = pts[i], pts[i + 1]
        L = math.hypot(q[0] - p[0], q[1] - p[1]) / 3
        t0, t1 = tangent(i), tangent(i + 1)
        L0, L1 = L * ease(i), L * ease(i + 1)
        out.append((p, (p[0] + t0[0] * L0, p[1] + t0[1] * L0),
                    (q[0] - t1[0] * L1, q[1] - t1[1] * L1), q))
    return out


def route_path(pts):
    """bezier()'s curve as a path."""
    segs = bezier(pts)
    d = [f"M{_fmt(pts[0][0])},{_fmt(pts[0][1])}"]
    for _p, c0, c1, q in segs:
        d.append(f"C{_fmt(c0[0])},{_fmt(c0[1])} {_fmt(c1[0])},{_fmt(c1[1])} "
                 f"{_fmt(q[0])},{_fmt(q[1])}")
    return " ".join(d) if len(pts) >= 3 else         "M" + " L".join(f"{_fmt(x)},{_fmt(y)}" for x, y in pts)


def sample(pts, step=6.0):
    """The smoothed line as dense points, with the index in the dense list
    of each original point: (dense, at)."""
    dense, at = [pts[0]], [0]
    for p, c0, c1, q in bezier(pts):
        n = max(2, int(math.dist(p, q) / step))
        for k in range(1, n + 1):
            u = k / n
            dense.append(tuple((1 - u) ** 3 * a + 3 * (1 - u) ** 2 * u * b +
                               3 * (1 - u) * u ** 2 * cc + u ** 3 * e
                               for a, b, cc, e in zip(p, c0, c1, q)))
        at.append(len(dense) - 1)
    return dense, at


def arcs(dense):
    out = [0.0]
    for p, q in zip(dense, dense[1:]):
        out.append(out[-1] + math.dist(p, q))
    return out


def point_at(dense, arc, s):
    """The point at arc length s along the dense line."""
    for i in range(1, len(dense)):
        if arc[i] >= s:
            t = (s - arc[i - 1]) / ((arc[i] - arc[i - 1]) or 1)
            p, q = dense[i - 1], dense[i]
            return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)
    return dense[-1]


def between(dense, arc, s0, s1):
    """The dense line from arc length s0 to s1, ends included."""
    return ([point_at(dense, arc, s0)] + [p for p, a in zip(dense, arc) if s0 < a < s1]
            + [point_at(dense, arc, s1)])


class Route:
    """The route in two parts, either side of the crossing: each a line
    through the camps with sites and our points between, smoothed, with
    every camp's place on it."""

    def __init__(self):
        order = nodes()
        cut = order.index("crossing_w") + 1
        self.parts = []
        self.at = {}                    # key -> (part, arc length, (x, y))
        for keys in (order[:cut], order[cut:]):
            anchors = [k for k in keys if site_point(k)]
            latlon, idx = [], {}
            for a, b in zip(anchors, anchors[1:] + [None]):
                idx[a] = len(latlon)
                latlon.append(site_point(a))
                if b:
                    latlon += WD.ROUTE_VIA.get((a, "crossing" if b == "crossing_w" else b), [])
            pts = PROJ.PS(latlon)
            dense, at = sample(pts)
            arc = arcs(dense)
            part = len(self.parts)
            self.parts.append(dict(latlon=latlon, pts=pts, dense=dense, arc=arc))
            for a in anchors:
                s = arc[at[idx[a]]]
                self.at[a] = (part, s, point_at(dense, arc, s))
            # the camps with no site, evenly between the anchors either side,
            # or either side of a point of ours the text puts them before
            for a, b in zip(anchors, anchors[1:]):
                inner = keys[keys.index(a) + 1:keys.index(b)]
                stops = [(self.at[a][1], [])]
                if (a, b) in WD.ROUTE_BREAKS:
                    vi, last = WD.ROUTE_BREAKS[(a, b)]
                    cut = inner.index(last) + 1
                    stops = [(self.at[a][1], inner[:cut]), (arc[at[idx[a] + 1 + vi]], inner[cut:])]
                else:
                    stops = [(self.at[a][1], inner)]
                stops.append((self.at[b][1], []))
                for (s0, ks), (s1, _n) in zip(stops, stops[1:]):
                    for j, k in enumerate(ks, 1):
                        s = s0 + (s1 - s0) * j / (len(ks) + 1)
                        self.at[k] = (part, s, point_at(dense, arc, s))
        self.span = PROJ.PS(WD.CROSSING_SPAN)

    def xy(self, key):
        return self.at[key][2]

    def line(self, a, b):
        """The drawn line from camp a to camp b, in px."""
        pa, sa, _ = self.at[a]
        pb, sb, _ = self.at[b]
        if pa == pb:
            p = self.parts[pa]
            return between(p["dense"], p["arc"], sa, sb)
        p0, p1 = self.parts[pa], self.parts[pb]
        return (between(p0["dense"], p0["arc"], sa, p0["arc"][-1]) + self.span
                + between(p1["dense"], p1["arc"], 0, sb))

    def midway(self, a, b):
        """The point halfway along the line from camp a to camp b."""
        pts = self.line(a, b)
        arc = arcs(pts)
        return point_at(pts, arc, arc[-1] / 2)


def anchors_beside(key):
    """For a camp with no site: what is drawn at a point before and after
    it, a camp with a site or the crossing's shore."""
    order = nodes()
    i = order.index(key)
    before = next(k for k in reversed(order[:i]) if site_point(k))
    after = next(k for k in order[i + 1:] if site_point(k))
    return before, after


def km_along(pts):
    return sum(math.dist(p, q) for p, q in zip(pts, pts[1:])) / KM


def route_marks(route, step=14):
    out = []
    for part in route.parts:
        pts = part["dense"]
        arc = part["arc"]
        s = 0
        while s < arc[-1]:
            x, y = point_at(pts, arc, s)
            out.append((x - 5, y - 5, x + 5, y + 5))
            s += step
    x0, y0 = route.span[0]
    x1, y1 = route.span[-1]
    n = int(math.dist(route.span[0], route.span[-1]) / step)
    out += [(x0 + (x1 - x0) * i / n - 5, y0 + (y1 - y0) * i / n - 5,
             x0 + (x1 - x0) * i / n + 5, y0 + (y1 - y0) * i / n + 5) for i in range(n + 1)]
    return out


# ---------------------------------------------------------------------------
# Glyphs
# ---------------------------------------------------------------------------

def stroke(c, d, col, width, dash=None, opacity=1.0):
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    if opacity < 1:
        extra += f' opacity="{opacity:.2f}"'
    c._emit(f'<path d="{d}" fill="none" stroke="{_rgb(col)}" stroke-width="{_fmt(width)}" '
            f'stroke-linecap="round" stroke-linejoin="round"{extra}/>')


def draw_dot(c, x, y, r, certainty):
    if certainty == WD.TRADITIONAL:
        c._emit(f'<circle cx="{_fmt(x)}" cy="{_fmt(y)}" r="{_fmt(r * 0.85)}" '
                f'fill="{_rgb(LAND)}" stroke="{_rgb(DOT)}" stroke-width="{_fmt(r * 0.36)}" '
                f'stroke-dasharray="{_fmt(r * 0.5)} {_fmt(r * 0.42)}"/>')
        c.circle(x, y, r * 0.28, fill=DOT)
    elif certainty == WD.POSSIBLE:
        c.circle(x, y, r * 0.8, fill=LAND, stroke=DOT, width=r * 0.4)
    else:
        c.circle(x, y, r, fill=DOT, stroke=BG, width=r * 0.2)
        if certainty == WD.PROBABLE:
            c.circle(x, y, r * 0.42, fill=LAND)


def draw_bead(c, x, y, r=BEAD_R):
    c.circle(x, y, r, fill=ROUTE, stroke=BG, width=2)


def diamond(c, x, y, s, fill, stroke_col=BG, width=1.5, hollow=False):
    pts = [(x, y - s), (x + s, y), (x, y + s), (x - s, y)]
    if hollow:
        c.polygon(pts, fill=PANEL, stroke=fill, width=max(2, s * 0.32))
    else:
        c.polygon(pts, fill=fill, stroke=stroke_col, width=width)


def rtext(c, xy, s, size, fill, angle, anchor="mm", italic=False, bold=False):
    """Text turned by `angle` degrees about its anchor."""
    ta = {"l": "start", "m": "middle", "r": "end"}[anchor[0]]
    db = {"a": "text-before-edge", "m": "central", "d": "text-after-edge"}[anchor[1]]
    a = (f'x="{_fmt(xy[0])}" y="{_fmt(xy[1])}" font-size="{_fmt(size)}" '
         f'text-anchor="{ta}" dominant-baseline="{db}" fill="{_rgb(fill)}"')
    if italic:
        a += ' font-style="italic"'
    if bold:
        a += ' font-weight="bold"'
    if angle:
        a += f' transform="rotate({_fmt(angle)} {_fmt(xy[0])} {_fmt(xy[1])})"'
    c._emit(f"<text {a}>{s.replace('&', '&amp;')}</text>")


def rbox(s, size, xy, angle, anchor="mm", italic=False):
    """The box of turned text (its turned ink box's bounds)."""
    b = box_of(s, size, (0, 0), anchor, italic=italic)
    corners = [(b[0], b[1]), (b[2], b[1]), (b[2], b[3]), (b[0], b[3])]
    a = math.radians(angle)
    pts = [(xy[0] + x * math.cos(a) - y * math.sin(a), xy[1] + x * math.sin(a) + y * math.cos(a))
           for x, y in corners]
    xs, ys = zip(*pts)
    return (min(xs), min(ys), max(xs), max(ys))


# ---------------------------------------------------------------------------
# Labels on the map
# ---------------------------------------------------------------------------

def label_text(key):
    s = WD.STATION.get(key) or WD.ENDS.get(key)
    if key == "red_sea_camp":
        return "By the Red Sea"
    return s.name[:1].upper() + s.name[1:]


def in_words(key):
    """A camp's name inside a sentence: "the wilderness of Sinai"."""
    if key == "red_sea_camp":
        return "the camp by the Red Sea"
    if key in ("crossing_w", "crossing_e"):
        return "the crossing of the sea"
    s = WD.STATION[key]
    return ("the " + s.name) if s.name[:1].islower() else s.name


def tier(key):
    if key in MAJOR:
        return "B"
    if WD.STATION[key].site:
        return "C"
    return "D"


def candidates(x, y, r, fs):
    out = []
    for i, f in enumerate((1.0, 2.2, 3.6)):
        g = (r + 0.32 * fs) * f + (6 if i else 0)
        d = g * 0.72
        for anchor, dx, dy in (("lm", g, 0), ("rm", -g, 0), ("md", 0, -g),
                               ("ma", 0, g), ("ld", d, -d), ("la", d, d),
                               ("rd", -d, -d), ("ra", -d, d)):
            out.append((anchor, x + dx, y + dy, i > 0))
    return out


def place(labels, taken, dots, marks):
    """Greedy, the biggest first: each label at the first spot that touches
    no other label, no dot and nothing taken, crossing the fewest route
    marks; failing that, the spot that touches least. labels: [dict(key,
    x, y, r, fs, text, bold, italic)] -> {key: (anchor, x, y, leader, box)}."""
    out, crowded = {}, []
    for p in sorted(labels, key=lambda p: (-p["fs"], p["order"])):
        own = (p["x"] - p["r"] - 2, p["y"] - p["r"] - 2, p["x"] + p["r"] + 2, p["y"] + p["r"] + 2)
        best, best_cost = None, None
        for anchor, x, y, leader in p.get("prefer", []) + candidates(p["x"], p["y"], p["r"],
                                                                      p["fs"]):
            b = box_of(p["text"], p["fs"], (x, y), anchor, p.get("bold", False),
                       p.get("italic", False))
            if b[0] < 8 or b[1] < 8 or b[2] > MAP_W - 8 or b[3] > H - 8:
                continue
            cost = sum(overlap(b, t) + 1 for t in taken if hits(b, t, 6)) * 10
            cost += sum(overlap(b, d) + 1 for d in dots if d != own and hits(b, d, 3)) * 10
            cost += sum(1 for m in marks if hits(b, m)) * 8
            cost += 30 if leader else 0
            if best_cost is None or cost < best_cost:
                best, best_cost = (anchor, x, y, leader, b), cost
            if cost == 0 or (best_cost < 10 and (anchor, x, y, leader) in p.get("prefer", [])):
                break
        if best_cost >= 10:
            crowded.append(p["key"])
        out[p["key"]] = best
        taken.append(best[4])
    return out, crowded


def number_spot(route, key, r, taken, marks):
    """Where a camp's number goes: beside its dot, square to the line, on
    the side that touches least."""
    x, y = route.xy(key)
    part, s, _ = route.at[key]
    p = route.parts[part]
    a = point_at(p["dense"], p["arc"], max(0, s - 20))
    b = point_at(p["dense"], p["arc"], min(p["arc"][-1], s + 20))
    dx, dy = b[0] - a[0], b[1] - a[1]
    m = math.hypot(dx, dy) or 1
    nx, ny = dy / m, -dx / m
    n = str(order_of(key))
    best = None
    for side in (1, -1):
        for g in (r + 16, r + 30, r + 46):
            cx, cy = x + nx * g * side, y + ny * g * side
            b_ = box_of(n, FS_NUM, (cx, cy), "mm", bold=True)
            cost = sum(1 for t in taken if hits(b_, t, 2)) * 10 + \
                sum(1 for m_ in marks if hits(b_, m_))
            if best is None or cost < best[0]:
                best = (cost, (cx, cy), b_)
    return best[1], best[2]


def order_of(key):
    return [s.key for s in WD.STATIONS].index(key) + 1


def water_spots():
    out = {}
    for key, (lat, lon, fs, anchor, rot) in WATER_LABELS.items():
        xy = P(lat, lon)
        s = WATER_TEXT[key]
        b = rbox(s, fs, xy, rot, anchor, italic=True) if rot else \
            box_of(s, fs, xy, anchor, italic=True)
        out[key] = (xy, fs, anchor, rot, b)
    return out


def region_spot(key):
    r = WD.REGIONS[key]
    x, y = P(r.lat, r.lon)
    if r.name.startswith("Wilderness of "):
        main = r.name[len("Wilderness of "):].upper()
        small = "WILDERNESS OF"
        bm = box_of(main, FS_REGION, (x, y + 10), "ma", spacing=FS_REGION * 0.16)
        bs = box_of(small, FS_REGION_SMALL, (x, y), "md", spacing=FS_REGION_SMALL * 0.16)
        return [(small, FS_REGION_SMALL, (x, y), "md", bs),
                (main, FS_REGION, (x, y + 10), "ma", bm)]
    main = r.name.upper()
    return [(main, FS_REGION, (x, y), "mm",
             box_of(main, FS_REGION, (x, y), "mm", spacing=FS_REGION * 0.16))]


def region_box(key):
    bs = [b for *_r, b in region_spot(key)]
    return (min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs),
            max(b[3] for b in bs))


# The other itineraries: lists in the Hisma, south-east of Edom
VARIANT_AT = (29.42, 35.42)


def variant_lines():
    """[(variant, [(text, fs, bold)])]: each list as a title and its names,
    wrapped."""
    out = []
    for v in WD.VARIANTS:
        lines = [(f"{v.title} ({re.sub(r'^[A-Za-z]+ ', '', v.ref)})", FS_VARIANT + 4, True)]
        cur = ""
        for n in v.names:
            nxt = (cur + " · " if cur else "") + n
            if ink(nxt, FS_VARIANT, False, True, "lm")[2] > 700 and cur:
                lines.append((cur, FS_VARIANT, False))
                cur = n
            else:
                cur = nxt
        lines.append((cur, FS_VARIANT, False))
        out.append((v, lines))
    return out


def variant_blocks():
    """[(variant, [(text, fs, bold, (x, y))], box)]."""
    x, y = P(*VARIANT_AT)
    out = []
    head = (x, y)
    y += 50
    for v, lines in variant_lines():
        placed = []
        for t, fs, bold in lines:
            placed.append((t, fs, bold, (x, y)))
            y += fs + 12
        bs = [box_of(t, fs, xy, "lm", bold=bold, italic=not bold) for t, fs, bold, xy in placed]
        box = (min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs),
               max(b[3] for b in bs))
        out.append((v, placed, box))
        y += 24
    return head, out


# ---------------------------------------------------------------------------
# The map's items, placed
# ---------------------------------------------------------------------------

class Map:
    def __init__(self):
        self.route = R = Route()
        self.marks = route_marks(R)
        self.waters = water_spots()
        self.vhead, self.vblocks = variant_blocks()
        fixed = [MAST] + [w[4] for w in self.waters.values()] + \
            [region_box(k) for k in WD.REGIONS] + [b for _v, _p, b in self.vblocks] + \
            [box_of("Other itineraries", 34, self.vhead, "lm", bold=True)]
        # the dots: camps with sites, the plains' ends, the landmarks
        self.dots = {}
        for s in WD.STATIONS:
            if s.site:
                fs, r = TIERS[tier(s.key)]
                self.dots[s.key] = (R.xy(s.key), r)
        for k, s in WD.ENDS.items():
            self.dots[k] = (P(s.site.lat, s.site.lon), TIERS["C"][1])
        for k in LANDMARKS:
            g = GZ.SITES[k]
            self.dots["lm-" + k] = (P(g.lat, g.lon), 5)
        dot_boxes = [(x - r - 2, y - r - 2, x + r + 2, y + r + 2)
                     for (x, y), r in self.dots.values()]
        bead_boxes = [(x - BEAD_R - 2, y - BEAD_R - 2, x + BEAD_R + 2, y + BEAD_R + 2)
                      for x, y in (R.xy(s.key) for s in WD.STATIONS if not s.site and not s.ends)]
        # the plains' bar
        a, b = (P(WD.ENDS[k].site.lat, WD.ENDS[k].site.lon)
                for k in WD.STATION["plains_of_moab"].ends)
        self.bar = (a, b)
        taken = list(fixed)
        # numbers first, beside each camp
        self.numbers = {}
        for s in WD.STATIONS:
            r = self.dots[s.key][1] if s.key in self.dots else (9 if s.ends else BEAD_R)
            xy, nb = number_spot(R, s.key, r, taken + dot_boxes + bead_boxes,
                                 self.marks + self.bar_marks())
            self.numbers[s.key] = (xy, nb)
            taken.append(nb)
        # names
        labels = []
        for i, s in enumerate(WD.STATIONS):
            t = tier(s.key)
            fs, r = TIERS[t]
            x, y = R.xy(s.key)
            r = r if s.site else (12 if s.ends else BEAD_R + 2)
            labels.append(dict(key=s.key, x=x, y=y, r=r, fs=fs, text=label_text(s.key),
                               bold=t == "B", order=i, prefer=PREFER.get(s.key, [])))
        for i, (k, s) in enumerate(WD.ENDS.items()):
            (x, y), r = self.dots[k]
            labels.append(dict(key=k, x=x, y=y, r=r, fs=TIERS["D"][0], text=s.name, order=50 + i))
        for i, k in enumerate(LANDMARKS):
            (x, y), r = self.dots["lm-" + k]
            labels.append(dict(key="lm-" + k, x=x, y=y, r=r, fs=FS_LANDMARK,
                               text=GZ.SITES[k].name, italic=True, order=60 + i,
                               prefer=PREFER.get("lm-" + k, [])))
        # the crossing's words, by the span
        mx = (R.span[0][0] + R.span[-1][0]) / 2
        my = (R.span[0][1] + R.span[-1][1]) / 2
        labels.append(dict(key="crossing", x=mx, y=my, r=10, fs=TIERS["D"][0],
                           text="through the middle of the sea", italic=True, order=70))
        self.spots, self.crowded = place(labels, taken, dot_boxes + bead_boxes, self.marks)
        taken += dot_boxes + bead_boxes
        # the events, in a small list beside their camp
        self.events = self.place_events(taken)

    def bar_marks(self):
        (ax, ay), (bx, by) = self.bar
        return [(ax + (bx - ax) * t / 10 - 8, ay + (by - ay) * t / 10 - 8,
                 ax + (bx - ax) * t / 10 + 8, ay + (by - ay) * t / 10 + 8) for t in range(11)]

    def event_anchor(self, at):
        if at == "crossing":
            s = self.route.span
            return ((s[0][0] + s[-1][0]) / 2, (s[0][1] + s[-1][1]) / 2)
        if isinstance(at, tuple):
            return self.route.midway(*at)
        return self.route.xy(at)

    def place_events(self, taken):
        """{at: (anchor xy, [(event, (x, y), box)], block box, leader)}."""
        groups = {}
        for e in WD.EVENTS:
            groups.setdefault(e.at, []).append(e)
        out = {}
        lists = []                          # the lists placed so far
        lh = FS_EVENT + 10
        for at, evs in groups.items():
            ax, ay = self.event_anchor(at)
            wmax = max(ink(e.label, FS_EVENT, False, False, "lm")[2] for e in evs) + 22
            hgt = lh * len(evs)
            best = None
            if at in EVENT_PREFER:
                # a list the placer would set across the Jordan from its camp
                ex, ey = P(*EVENT_PREFER[at])
                best = (0, (ex, ey, ex + wmax, ey + hgt))
            elif at in EVENT_AFTER_NAME:
                lb = self.spots[at][4]
                ex, ey = lb[2] + 14, (lb[1] + lb[3]) / 2 - hgt / 2
                best = (0, (ex, ey, ex + wmax, ey + hgt))
            for g in (() if best else (30, 60, 100, 150, 220, 300)):
                d = g * 0.7
                for dx, dy in ((g, -hgt / 2), (-g - wmax, -hgt / 2), (-wmax / 2, g),
                               (-wmax / 2, -g - hgt), (d, d), (-d - wmax, d),
                               (d, -d - hgt), (-d - wmax, -d - hgt)):
                    bx = (ax + dx, ay + dy, ax + dx + wmax, ay + dy + hgt)
                    if bx[0] < 8 or bx[1] < 8 or bx[2] > MAP_W - 8 or bx[3] > H - 8:
                        continue
                    if at in EVENT_EAST and bx[0] < ax:
                        continue
                    cost = sum(overlap(bx, t) + 1 for t in taken if hits(bx, t, 4)) * 10
                    # two lists side by side read as one camp's
                    cost += sum(10 for t in lists if hits(bx, t, EVENT_APART))
                    cost += sum(1 for m in self.marks if hits(bx, m)) * 2 + g / 8
                    # a leader that crosses a name reads badly
                    end = (min(max(ax, bx[0]), bx[2]), min(max(ay, bx[1]), bx[3]))
                    if math.dist((ax, ay), end) > 14:
                        cost += 15 * sum(1 for t in taken if seg_hits_rect(
                            (ax, ay), end, (t[0] + 2, t[1] + 2, t[2] - 2, t[3] - 2)))
                    if best is None or cost < best[0]:
                        best = (cost, bx)
                if best and best[0] < 10:
                    break
            bx = best[1]
            rows_ = []
            for i, e in enumerate(evs):
                y = bx[1] + lh * i + lh / 2
                tb = box_of(e.label, FS_EVENT, (bx[0] + 22, y), "lm")
                rows_.append((e, (bx[0], y), (bx[0], tb[1] - 3, tb[2], tb[3] + 3)))
            out[at] = ((ax, ay), rows_, bx)
            taken.append(bx)
            lists.append(bx)
        return out


# ---------------------------------------------------------------------------
# The forty years
# ---------------------------------------------------------------------------

U = 82                                      # px a month
STRIP_TOP = 230
COLS = [X0 + 40, X0 + 980]                  # the two columns' left edges
AXIS = 420                                  # the time line, from a column's left edge
LANE = 44                                   # a span bar's lane
FS_MARK = 28
MARK_GAP, MARK_STEP = 22, 22                # diamonds closer than this stand side by side
FS_MONTH = 28
FS_SPAN = 28                                # a span bar's turned label
FS_YEAR = 44
STRIP_H = 2420

# the bands: (key, label, column, months, first month's y)
# years 1 and 2 by month in the first column; years 3 to 39 closed up, then
# year 40 and the first month of 41 by month, in the second
BAND_GAP = 70


def bands():
    out = []
    y = STRIP_TOP
    for yr in (1, 2):
        out.append(dict(key=f"year{yr}", label=f"Year {yr}", col=0, y0=y + BAND_GAP,
                        months=12, year=yr))
        y += BAND_GAP + 12 * U + 20
    y = STRIP_TOP
    out.append(dict(key="between", label="Years 3 to 39", col=1, y0=y + BAND_GAP, months=3,
                    year=None))
    y += BAND_GAP + 3 * U + 20
    out.append(dict(key="year40", label="Year 40", col=1, y0=y + BAND_GAP, months=12, year=40))
    y += BAND_GAP + 12 * U + 20
    out.append(dict(key="year41", label="Year 41", col=1, y0=y + BAND_GAP, months=1, year=41))
    return out


BANDS = bands()


def band_of(year):
    if year in (1, 2, 40, 41):
        return next(b for b in BANDS if b["year"] == year)
    return next(b for b in BANDS if b["key"] == "between")


def when(year, month, day):
    """(column, y) of a date: day 1 at the top of its month."""
    b = band_of(year)
    if b["key"] == "between":
        t = (year - 3 + ((month or 1) - 1) / 12) / 37
        return b["col"], b["y0"] + t * 3 * U
    return b["col"], b["y0"] + ((month or 1) - 1) * U + ((day or 1) - 1) / 30 * U


def axis_x(col):
    return COLS[col] + AXIS


def strip_marks():
    """The dated verses in time order, each with its column, y and label
    spot, stacked so that the labels never touch: [dict]."""
    ds = sorted(WD.DATES, key=lambda d: (d.year, d.month or 99, d.day or 0))
    out = []
    last = {}                               # col -> the last diamond: (y, its place in its run)
    for d in ds:
        col, y = when(d.year, d.month, d.day)
        if d.month is None:
            # Moses' death: the eleventh or twelfth month
            col, y = when(d.year, 11, 1)
        n = 0
        if d.day is not None and d.month is not None:
            # a diamond that would touch the last one stands beside it, and
            # the run goes on while each touches the one before
            if col in last and y - last[col][0] < MARK_GAP:
                n = last[col][1] + 1
            last[col] = (y, n)
        out.append(dict(d=d, col=col, y=y, x=axis_x(col) + 22 + MARK_STEP * n))
    last = {0: -1e9, 1: -1e9}
    for m in out:
        ly = max(m["y"], last[m["col"]] + FS_MARK + 10)
        m["ly"] = ly
        last[m["col"]] = ly
    return out


def span_of(sp):
    """(column, y0, y1) pieces of a dated span's bar, with which ends are
    dashed: [(col, y0, y1, dashed_top, dashed_bottom)]."""
    if not sp.start:
        return []
    y0c = when(*sp.start)
    endd = sp.end or None
    if not endd:
        return []
    y1c = when(*endd)
    if y0c[0] == y1c[0]:
        return [(y0c[0], y0c[1], y1c[1])]
    # across the columns: to the foot of the first, from the head of the second
    foot = BANDS[1]["y0"] + 12 * U
    head = BANDS[2]["y0"]
    return [(0, y0c[1], foot), (1, head, y1c[1])]


LONG = {"Josh 5:6": 5, "Exod 16:35": 4}     # the forty years' bars, outermost


def dated_spans():
    """[(span, [(col, y0, y1)], lane)] for the spans with dates, packed in
    lanes left of the time line so their turned labels don't touch."""
    out = []
    used = {0: {}, 1: {}}                  # col -> lane -> [(y0, y1)]
    for sp in WD.SPANS:
        pieces = span_of(sp)
        if sp.ref == "Deut 2:14":
            pieces = thirty_eight()
        if not pieces:
            continue
        if sp.ref in LONG:
            lane = LONG[sp.ref]
        elif sp.ref == "Deut 2:14":
            lane = 3
        else:
            lane = None
            lab = span_label(sp)
            ext = [(col, y0, max(y1, y0 + ink(lab, FS_SPAN, False, False, "lm")[2] + 16))
                   for col, y0, y1, *_ in pieces]
            for ln in range(3):
                if all(not any(a < y1 + 6 and y0 - 6 < b for a, b in used[col].get(ln, []))
                       for col, y0, y1 in ext):
                    lane = ln
                    for col, y0, y1 in ext:
                        used[col].setdefault(ln, []).append((y0, y1))
                    break
        out.append((sp, pieces, lane))
    return out


def thirty_eight():
    """Deuteronomy 2:14's thirty-eight years: from Kadesh Barnea after the
    spies (year 2, from about the fourth month, not dated) to the Zered
    (after Aaron's death, before the eleventh month of year 40, not dated);
    the undated ends dashed."""
    _c, a = when(2, 4, 1)
    foot = BANDS[1]["y0"] + 12 * U
    head = BANDS[2]["y0"]
    _c, b = when(40, 5, 1)
    _c, e = when(40, 11, 1)
    return [(0, a, foot, True), (1, head, b, False), (1, b, e, True)]


def span_label(sp):
    """Its label, with its length where the label doesn't give it."""
    if re.search(r"\b(days?|months?|years?)\b", sp.label):
        return sp.label
    return f"{sp.label} · {sp.length}"


def lane_x(col, lane):
    return axis_x(col) - 52 - LANE * lane


def undated_spans():
    """The lengths with no date, less those counted in years, which are the
    forty years' own (Numbers 14:33-34 is on the forty years' card)."""
    return [sp for sp in WD.SPANS if not span_of(sp) and sp.ref != "Deut 2:14"
            and not sp.years]


UNDATED_TOP = STRIP_H + 40
UNDATED_ROW = 54


def draw_strip(c, marks, spans):
    """The forty years, in the right column."""
    c.rect(X0, 0, COL_W, H, fill=PANEL)
    c.line((X0, 0), (X0, H), SAND_DIM, 3)
    with c.group(data={"fs": 64}):
        text(c, (X0 + 60, 80), "The forty years", 64, TEXT, "lm", bold=True)
    with c.group(data={"fs": 28}):
        text(c, (X0 + 62, 150), "the text's own dates, counted from the exodus as year 1",
             28, TEXT_DIM, "lm", italic=True)
    boxes = {}
    for b in BANDS:
        cx = COLS[b["col"]]
        ax = cx + AXIS
        y0, y1 = b["y0"], b["y0"] + b["months"] * U
        with c.group(data={"fs": FS_YEAR}):
            text(c, (ax + 30, y0 - 22), b["label"], FS_YEAR, TEXT, "ld", bold=True)
        boxes[b["key"]] = box_of(b["label"], FS_YEAR, (ax + 30, y0 - 22), "ld", bold=True)
        if b["key"] == "between":
            c.rect(cx, y0, 880, y1 - y0, fill=(30, 30, 44), rx=10)
            # the break in the line: two slants
            for dy in (-8, 8):
                ym = (y0 + y1) / 2 + dy
                c.line((ax - 14, ym + 6), (ax + 14, ym - 6), SAND, 3)
            with c.group(data={"fs": 26}):
                text(c, (cx + 600, (y0 + y1) / 2), "not dated", 26, TEXT_DIM, "lm",
                     italic=True)
            c.line((ax, y0), (ax, (y0 + y1) / 2 - 16), SAND, 3)
            c.line((ax, (y0 + y1) / 2 + 16), (ax, y1), SAND, 3)
            continue
        c.line((ax, y0), (ax, y1), SAND, 3)
        with c.group(data={"fs": FS_MONTH}):
            for m in range(b["months"]):
                y = y0 + m * U
                c.line((ax - 10, y), (ax + 10, y), SAND, 2)
                text(c, (cx + 110, y + U / 2), f"month {m + 1}", FS_MONTH, TEXT_DIM, "rm")
            c.line((ax - 16, y1), (ax + 16, y1), SAND, 3)
    # the spans: bars in lanes, the undated ends dashed, labels turned along them
    span_boxes = {}
    if True:
        for sp, pieces, lane in spans:
            bs = []
            for piece in pieces:
                col, y0, y1 = piece[:3]
                dashed = len(piece) > 3 and piece[3]
                x = lane_x(col, lane)
                col_ = DERIVED if sp.derived else ROUTE
                if dashed:
                    stroke(c, f"M{_fmt(x)},{_fmt(y0)} L{_fmt(x)},{_fmt(y1)}", col_, 7, "10 8")
                else:
                    c.line((x, y0), (x, max(y1, y0 + 4)), col_, 7)
                bs.append((x - 5, y0, x + 26, max(y1, y0 + 4)))
            lab = span_label(sp)
            # its words at the head of each column it runs in
            for col, y0 in {p[0]: p[1] for p in reversed(pieces)}.items():
                x = lane_x(col, lane)
                with c.group(data={"fs": FS_SPAN}):
                    rtext(c, (x + 10, y0 + 4), lab, FS_SPAN, TEXT, 90, "ld")
                bs.append((x + 6, y0 + 4, x + 12 + FS_SPAN + 2,
                           y0 + 8 + ink(lab, FS_SPAN, False, False, "lm")[2]))
            span_boxes[sp.ref] = bs
    # the dated verses
    mark_boxes = {}
    for m in marks:
        d = m["d"]
        ax = axis_x(m["col"])
        x, y, ly = m["x"], m["y"], m["ly"]
        cx = COLS[m["col"]]
        if d.month is None:
            # not dated: the months it must fall in, worked out (Moses' death)
            mo = 2
            c._emit(f'<rect x="{_fmt(ax - 6)}" y="{_fmt(y + 2)}" width="12" '
                    f'height="{_fmt(mo * U - 4)}" rx="5" fill="{_rgb(PANEL)}" '
                    f'stroke="{_rgb(ROUTE_TXT)}" stroke-width="2.5" stroke-dasharray="7 6"/>')
            gx = ax
            mb = (ax - 8, y, ax + 8, y + mo * U)
        elif d.day is None:
            # only the month is given
            c.rect(ax - 6, y + 2, 12, U - 4, fill=PANEL, stroke=ROUTE_TXT, width=2.5, rx=5)
            gx = ax
            mb = (ax - 8, y, ax + 8, y + U)
        else:
            gx = x
            mb = (x - 11, y - 11, x + 11, y + 11)
        m["gx"] = gx
        mark_boxes[id(m)] = mb
    # the leaders under the diamonds, so a run's leaders pass beneath its
    # later diamonds
    with c.group(data={"fs": FS_MARK}):
        for m in marks:
            d = m["d"]
            cx = COLS[m["col"]]
            ly = m["ly"]
            c.line((m["gx"] + 12, m["y"]), (cx + 536, ly), TEXT_DIM, 1.5)
            if d.day:
                text(c, (cx + 591, ly), str(d.day), FS_MARK, TEXT_DIM, "rm")
            text(c, (cx + 606, ly), d.label, FS_MARK, TEXT if d.stated else (214, 204, 176), "lm",
                 italic=not d.stated)
            lb = box_of(d.label, FS_MARK, (cx + 606, ly), "lm", italic=not d.stated)
            db = box_of(str(d.day or ""), FS_MARK, (cx + 591, ly), "rm") if d.day else lb
            mark_boxes[id(m)] = (mark_boxes[id(m)], (min(db[0], lb[0]), lb[1], lb[2], lb[3]))
    for m in marks:
        if m["d"].month is not None and m["d"].day is not None:
            diamond(c, m["x"], m["y"], 9, ROUTE_TXT, hollow=not m["d"].stated)
    # the lengths of time the text doesn't date
    und = undated_spans()
    ux = X0 + 60
    with c.group(data={"fs": 40}):
        text(c, (ux, UNDATED_TOP + 30), "Lengths of time, not dated", 40, TEXT, "lm", bold=True)
    und_boxes = {}
    y = UNDATED_TOP + 100
    for sp in und:
        bx = ux + 420
        if sp.days:
            L = max(5, sp.days / 30 * U)
            c.line((bx, y), (bx + L, y), ROUTE, 9)
        else:
            L = 130
            stroke(c, f"M{_fmt(bx)},{_fmt(y)} L{_fmt(bx + L)},{_fmt(y)}", ROUTE, 9, "2 12")
        lab = span_label(sp)
        with c.group(data={"fs": 28}):
            where = label_text(sp.station) if sp.station in WD.STATION else ""
            text(c, (ux + 400, y), where, 28, TEXT_DIM, "rm", italic=True)
            text(c, (bx + L + 20, y), lab, 28, TEXT, "lm")
        lb = box_of(lab, 28, (bx + L + 20, y), "lm")
        und_boxes[sp.ref] = (ux, y - 20, lb[2], y + 20)
        y += UNDATED_ROW
    return boxes, span_boxes, mark_boxes, und_boxes


# ---------------------------------------------------------------------------
# The sheet
# ---------------------------------------------------------------------------

def region_lod(key):
    """(fs, fmax) of a land's name group: a wilderness's two lines come in
    and fade together, as its smaller line can be read, so that its name
    never stands alone ("SIN")."""
    two = len(region_spot(key)) > 1
    fs = FS_REGION_SMALL if two else FS_REGION
    return fs, round(REGION_FADE * fs / FS_REGION, 2)


def draw_regions(c):
    lods = sorted({region_lod(k) for k in WD.REGIONS})
    for lod in lods:
        with c.group(data={"fs": lod[0], "fmax": lod[1]}):
            for key in WD.REGIONS:
                if region_lod(key) != lod:
                    continue
                for s, f, xy, anchor, _b in region_spot(key):
                    text(c, xy, s, f, REGION_TXT, anchor, spacing=f * 0.16, opacity=0.8)


def draw_waters(c, spots):
    by_fs = {}
    for key, (xy, fs, anchor, rot, _b) in spots.items():
        by_fs.setdefault(fs, []).append((key, xy, anchor, rot))
    for fs in sorted(by_fs):
        with c.group(data={"fs": fs}):
            for key, xy, anchor, rot in by_fs[fs]:
                col = (92, 112, 136) if key in MODERN else WATER_TXT
                rtext(c, xy, WATER_TEXT[key], fs, col, rot, anchor, italic=True)


def draw_route(c, mp):
    R = mp.route
    for part in R.parts:
        stroke(c, route_path(part["pts"]), ROUTE, 5, "18 12")
    # the crossing, over the water
    (x0, y0), (x1, y1) = R.span[0], R.span[-1]
    stroke(c, f"M{_fmt(x0)},{_fmt(y0)} L{_fmt(x1)},{_fmt(y1)}", SPAN_COL, 7, "4 12")
    # the plains of Moab, a bar between its two ends
    (ax, ay), (bx, by) = mp.bar
    c.line((ax, ay), (bx, by), ROUTE, 10, linecap="round")


def draw_camps(c, mp):
    R = mp.route
    for s in WD.STATIONS:
        if not s.site and not s.ends:
            draw_bead(c, *R.xy(s.key))
    for k, s in WD.ENDS.items():
        (x, y), r = mp.dots[k]
        draw_dot(c, x, y, r, s.site.certainty)
    for s in WD.STATIONS:
        if s.site:
            (x, y), r = mp.dots[s.key]
            draw_dot(c, x, y, r, s.site.certainty)
    for k in LANDMARKS:
        (x, y), r = mp.dots["lm-" + k]
        c.circle(x, y, r, fill=LANDMARK, stroke=BG, width=1.5)
    with c.group(data={"fs": FS_NUM}):
        for s in WD.STATIONS:
            (x, y), _b = mp.numbers[s.key]
            text(c, (x, y), str(order_of(s.key)), FS_NUM, ROUTE_TXT, "mm", bold=True)
    # the names, smallest first so the big ones are on top
    groups = {}
    for key, spot in mp.spots.items():
        if key == "crossing":
            fs, col, it, bold = TIERS["D"][0], SPAN_COL, True, False
        elif key.startswith("lm-"):
            fs, col, it, bold = FS_LANDMARK, LANDMARK_TXT, True, False
        elif key in WD.ENDS:
            fs, col, it, bold = TIERS["D"][0], TEXT, False, False
        else:
            t = tier(key)
            fs, col, it, bold = TIERS[t][0], (240, 228, 196) if t == "B" else TEXT, False, t == "B"
        groups.setdefault(fs, []).append((key, spot, col, it, bold))
    for fs in sorted(groups):
        with c.group(data={"fs": fs}):
            for key, spot, col, it, bold in groups[fs]:
                if spot[3]:
                    leader(c, mp, key, spot, fs)
                if key == "crossing":
                    s = "through the middle of the sea"
                elif key.startswith("lm-"):
                    s = GZ.SITES[key[3:]].name
                elif key in WD.ENDS:
                    s = WD.ENDS[key].name
                else:
                    s = label_text(key)
                text(c, spot[1:3], s, fs, col, spot[0], bold=bold, italic=it)


def anchor_of(mp, key):
    if key == "crossing":
        s = mp.route.span
        return ((s[0][0] + s[-1][0]) / 2, (s[0][1] + s[-1][1]) / 2), 6
    if key in mp.dots:
        return mp.dots[key]
    return mp.route.xy(key), BEAD_R


def leader(c, mp, key, spot, fs):
    (px, py), r = anchor_of(mp, key)
    x0, y0, x1, y1 = spot[4]
    tx_ = min(max(px, x0), x1)
    ty_ = min(max(py, y0), y1)
    dx, dy = tx_ - px, ty_ - py
    m = math.hypot(dx, dy) or 1
    c.line((px + dx / m * (r + 2), py + dy / m * (r + 2)), (tx_ - dx / m * 2, ty_ - dy / m * 2),
           TEXT_DIM, max(1, fs / 18))


def draw_events(c, mp):
    """Each list, its marks and a thin leader to its camp, come in with its
    words."""
    with c.group(data={"layer": "events"}):
        with c.group(data={"fs": FS_EVENT}):
            for at, ((ax, ay), rows_, bx) in mp.events.items():
                tx_ = min(max(ax, bx[0]), bx[2])
                ty_ = min(max(ay, bx[1]), bx[3])
                own = mp.spots.get(at) if isinstance(at, str) else None
                # no leader through the camp's own name: the list hangs under it
                through = own and seg_hits_rect((ax, ay), (tx_, ty_), own[4])
                if math.dist((ax, ay), (tx_, ty_)) > 14 and not through:
                    m = math.dist((ax, ay), (tx_, ty_))
                    c.line((ax + (tx_ - ax) / m * 9, ay + (ty_ - ay) / m * 9), (tx_, ty_),
                           (170, 112, 98), 1.5)
                for e, (x, y), _b in rows_:
                    diamond(c, x + 8, y, 6, EVENT)
                    text(c, (x + 22, y), e.label, FS_EVENT, EVENT_TXT, "lm")


def draw_variants(c, mp):
    with c.group(data={"layer": "variants"}):
        with c.group(data={"fs": 34}):
            text(c, mp.vhead, "Other itineraries", 34, VARIANT_TXT, "lm", bold=True)
        for fs in sorted({fs for _v, placed, _b in mp.vblocks for _t, fs, _bo, _xy in placed}):
            with c.group(data={"fs": fs}):
                for _v, placed, _b in mp.vblocks:
                    for t, f, bold, xy in placed:
                        if f == fs:
                            text(c, xy, t, fs, VARIANT_TXT if bold else (190, 182, 156), "lm",
                                 bold=bold, italic=not bold)


def draw_masthead(c):
    # big enough to read on a phone's first, whole-map frame
    with c.group(data={"fs": FS_TITLE}):
        text(c, (MAST[0] + 20, MAST[1] + 60), TITLE, FS_TITLE, TEXT, "lm", bold=True)
    with c.group(data={"fs": 40}):
        text(c, (MAST[0] + 24, MAST[1] + 160),
             "Numbers 33: the camps from Rameses to the plains of Moab", 40, TEXT_DIM, "lm",
             italic=True)
    with c.group(data={"fs": 30}):
        text(c, (MAST[0] + 24, MAST[1] + 230),
             "on the traditional southern route; most camps are not identified",
             30, TEXT_DIM, "lm")


KEY_TOP = UNDATED_TOP + 100 + UNDATED_ROW * 14 + 90


def draw_key(c):
    """The map's key and the strip's, at the foot of the right column."""
    x0, y = X0 + 60, KEY_TOP
    fs = FS_KEY
    with c.group(data={"fs": 40}):
        text(c, (x0, y), "Key", 40, TEXT, "lm", bold=True)
    y += 70
    boxes = {}
    with c.group(data={"fs": fs}):
        stroke(c, f"M{_fmt(x0)},{_fmt(y)} L{_fmt(x0 + 100)},{_fmt(y)}", ROUTE, 5, "18 12")
        text(c, (x0 + 125, y), "the traditional route (the line between camps is ours)", fs,
             TEXT, "lm")
        boxes["route"] = (x0 - 10, y - 24, X0 + COL_W - 30, y + 24)
        y += 54
        stroke(c, f"M{_fmt(x0)},{_fmt(y)} L{_fmt(x0 + 100)},{_fmt(y)}", SPAN_COL, 7, "4 12")
        text(c, (x0 + 125, y), "through the sea, where tradition puts it", fs, TEXT, "lm")
        y += 58
        x = x0 + 12
        for cert, word in ((WD.KNOWN, "known site"), (WD.PROBABLE, "probable"),
                           (WD.POSSIBLE, "possible"), (WD.TRADITIONAL, "traditional")):
            draw_dot(c, x, y, 12, cert)
            text(c, (x + 24, y), word, fs, TEXT, "lm")
            x += 76 + ink(word, fs, False, False, "lm")[2]
        y += 58
        draw_bead(c, x0 + 12, y)
        text(c, (x0 + 36, y), "a camp not identified, drawn in its order on the line", fs,
             TEXT, "lm")
        y += 54
        text(c, (x0 + 12, y), "12", FS_NUM + 4, ROUTE_TXT, "mm", bold=True)
        text(c, (x0 + 36, y), "its place in Numbers 33", fs, TEXT, "lm")
        y += 54
        c.line((x0, y), (x0 + 60, y), ROUTE, 10, linecap="round")
        text(c, (x0 + 80, y), "a camp from one place to another (the plains of Moab)", fs,
             TEXT, "lm")
        y += 54
        diamond(c, x0 + 12, y, 7, EVENT)
        text(c, (x0 + 36, y), "what happened there (Events)", fs, TEXT, "lm")
        y += 54
        c.circle(x0 + 12, y, 6, fill=LANDMARK, stroke=BG, width=1.5)
        text(c, (x0 + 36, y), "another place, for bearings", fs, TEXT, "lm")
        y += 54
        text(c, (x0, y), "the coasts as they are today; the Salt Sea at its high water", fs,
             TEXT_DIM, "lm", italic=True)
        y += 80
        # the strip's marks
        diamond(c, x0 + 12, y, 9, ROUTE_TXT)
        text(c, (x0 + 36, y), "a date the verse gives in full", fs, TEXT, "lm")
        diamond(c, x0 + 812, y, 9, ROUTE_TXT, hollow=True)
        text(c, (x0 + 836, y), "a date partly inferred", fs, TEXT, "lm")
        y += 54
        c.rect(x0 + 6, y - 22, 12, 44, fill=PANEL, stroke=ROUTE_TXT, width=2.5, rx=5)
        text(c, (x0 + 36, y), "only the month given", fs, TEXT, "lm")
        c.line((x0 + 812, y), (x0 + 862, y), ROUTE, 7)
        text(c, (x0 + 880, y), "a length the text gives", fs, TEXT, "lm")
        y += 54
        c.line((x0, y), (x0 + 50, y), DERIVED, 7)
        text(c, (x0 + 70, y), "a length worked out from two dates", fs, TEXT, "lm")
        stroke(c, f"M{_fmt(x0 + 812)},{_fmt(y)} L{_fmt(x0 + 870)},{_fmt(y)}", ROUTE, 7, "10 8")
        text(c, (x0 + 890, y), "an end not dated", fs, TEXT, "lm")
        y += 54
        c._emit(f'<rect x="{_fmt(x0 + 6)}" y="{_fmt(y - 22)}" width="12" height="44" rx="5" '
                f'fill="{_rgb(PANEL)}" stroke="{_rgb(ROUTE_TXT)}" stroke-width="2.5" '
                f'stroke-dasharray="7 6"/>')
        text(c, (x0 + 36, y), "not dated: the months it must fall in, worked out", fs, TEXT,
             "lm")
        # the scale
        y += 90
        km = 100
        c.line((x0, y), (x0 + km * KM, y), SAND, 5)
        for i in range(0, km + 1, 25):
            xx = x0 + i * KM
            c.line((xx, y - 12), (xx, y), SAND, 3)
            text(c, (xx, y + 10), str(i), 26, TEXT_DIM, "ma")
        text(c, (x0 + km * KM + 20, y), "km", 26, TEXT_DIM, "lm")
        mi = 50
        xs = x0 + 1000
        c.line((xs, y), (xs + mi * 1.609344 * KM, y), SAND, 5)
        for i in range(0, mi + 1, 25):
            xx = xs + i * 1.609344 * KM
            c.line((xx, y - 12), (xx, y), SAND, 3)
            text(c, (xx, y + 10), str(i), 26, TEXT_DIM, "ma")
        text(c, (xs + mi * 1.609344 * KM + 20, y), "miles", 26, TEXT_DIM, "lm")
    return boxes


def build_svg(mp, marks, spans):
    c = SvgCanvas(W, H, bg=SEA)
    with c.group(clip=(MAP_W, H)):
        draw_base(c)
        draw_regions(c)
        draw_waters(c, mp.waters)
        draw_route(c, mp)
        draw_variants(c, mp)
        draw_camps(c, mp)
        draw_events(c, mp)
        draw_masthead(c)
    strip = draw_strip(c, marks, spans)
    keyb = draw_key(c)
    return c.tostring().replace(
        "<svg ", f'<svg data-kind="map" data-title="{TITLE}" ', 1), strip, keyb


# ---------------------------------------------------------------------------
# The sidecar
# ---------------------------------------------------------------------------

def cap(s):
    return s[:1].upper() + s[1:]


def singles(ref):
    return rows(verses(ref))


def naming_rows(s):
    """A camp's own verses as single rows: its Numbers 33 verses that name
    it (the rest of its Numbers 33 ref as a range), its refs and its other
    verse groups."""
    text = lambda v: TEXT_WEB[("Numbers", 33, v)]
    pat = re.compile(r"\b(%s)\b" % "|".join(re.escape(n) for n in (s.name,) + tuple(s.aka)))
    named = [("Numbers", 33, v) for v in WD.num33_verses(s) if pat.search(text(v))]
    out = rows(named + verses(s.refs) + [v for _l, r in s.more for v in verses(r)])
    if len(named) < len(WD.num33_verses(s)):
        out += range_rows(s.num33)
    return out


def fr_round(x, y, half=450):
    return [round(x - half), round(y - half * 0.75), 2 * half, round(1.5 * half)]


def station_card(s, mp, idx, legs_of, dates_of, events_of):
    route = mp.route
    x, y = route.xy(s.key)
    t = tier(s.key)
    fs, r = TIERS[t]
    n = order_of(s.key)
    item = {"id": s.key.replace("_", "-"), "n": label_text(s.key),
            "s": f"camp {n} of 42 · Numbers {s.num33.replace('Num ', '')}",
            "a": [a for a in s.aka]}
    tx = []
    if s.site:
        item["dims"] = [["Identified with", s.site.name, s.site.certainty, []]]
        if s.site.why:
            tx.append(["Why this site", s.site.why])
        if s.site.since:
            tx.append(["Held since", s.site.since])
    elif s.ends:
        a, b = (WD.ENDS[k].name for k in s.ends)
        tx.append(["Where", f"From {a} to {b} (Numbers 33:49): drawn as a bar between them."])
    else:
        a, b = anchors_beside(s.key)
        where = (f"Not identified; drawn in its order between {in_words(a)} and "
                 f"{in_words(b)}, not at a place.")
        order = nodes()
        if (a, b) in WD.ROUTE_BREAKS and s.key in \
                order[order.index(a):order.index(WD.ROUTE_BREAKS[(a, b)][1]) + 1]:
            where += (" It is drawn before the Zered, which Numbers 21:11-12 reaches after "
                      "Iyeabarim.")
        tx.append(["Where", where])
        if s.proposed:
            tx.append(["Proposed", s.proposed])
    if s.site and s.proposed:
        tx.append(["Also proposed", s.proposed])
    if s.differs:
        tx.append(["Numbers 33 and the narrative", s.differs])
    if s.namesakes:
        tx.append(["Namesakes", s.namesakes])
    if dates_of.get(s.key):
        tx.append(["Dates", "; ".join(date_words(d) for d in dates_of[s.key])])
    if s.site:
        src = s.site.qid and f"Wikidata {s.site.qid}" or \
            f"Wikipedia ({s.site.wiki.split(':')[0]}), the article on {s.name}"
        if s.site.gazetteer:
            src += ", as on the Land of Israel page"
        tx.append(["Map point", src])
    item["tx"] = tx
    item["note"] = s.card
    rg = [["Numbers 33", range_rows(s.num33)]]
    own = rows(verses(s.refs))
    if own:
        rg.append(["Named in" if len(own) <= 30 else "Named first in each book",
                   own if len(own) <= 30 else shown_rows(own)])
    for label, ref in s.more:
        rs = rows(verses(ref))
        rg.append([label, rs if len(rs) <= 30 else shown_rows(rs)])
    if s.story:
        rg.append(["The narrative", range_rows(s.story)])
    item["rg"] = rg
    item["r"] = naming_rows(s) + (range_rows(s.story) if s.story else [])
    see = list(legs_of.get(s.key, [])) + \
        [idx[("event", e.key)] for e in events_of.get(s.key, [])] + \
        [idx[("date", d.ref)] for d in dates_of.get(s.key, [])]
    see += [idx[k] for k in s.ends]
    item["see"] = see
    if s.site and s.site.gazetteer:
        item["ln"] = [["On the Land of Israel page", atlas_link(s.site.gazetteer)]]
    # tapped on its dot (or bead) and its name and number
    if s.key in mp.dots:
        (dx, dy), dr = mp.dots[s.key]
    else:
        (dx, dy), dr = (x, y), (12 if s.ends else BEAD_R)
    dotb = (dx - dr, dy - dr, dx + dr, dy + dr)
    lb = mp.spots[s.key][4]
    nb = mp.numbers[s.key][1]
    u = (min(dotb[0], lb[0], nb[0]), min(dotb[1], lb[1], nb[1]),
         max(dotb[2], lb[2], nb[2]), max(dotb[3], lb[3], nb[3]))
    item["b"] = _bx(u)
    item["t"] = [_bx(dotb, 6), _bx(lb, 2), _bx(nb, 2)]
    if s.ends:
        (ax, ay), (bx, by) = mp.bar
        item["t"].append(_bx((min(ax, bx), min(ay, by), max(ax, bx), max(ay, by)), 6))
    item["fs"] = fs if t == "B" else min(fs, FS_NUM)
    item["fr"] = fr_round(x, y)
    return item


def atlas_link(key):
    """A gazetteer place's card on the Land of Israel page."""
    return "/visuals/reference/Land_of_Israel.html#id=" + key.replace("_", "-")


def date_words(d):
    out = f"year {d.year}"
    if d.month:
        out += f", month {d.month}"
    if d.day:
        out += f", day {d.day}" + (f" to {d.end_day}" if d.end_day else "")
    if d.month is None:
        out += ", month 11 or 12"
    return f"{d.label}, {out} ({d.ref})"


def end_card(k, mp):
    s = WD.ENDS[k]
    (x, y), r = mp.dots[k]
    lb = mp.spots[k][4]
    dotb = (x - r, y - r, x + r, y + r)
    item = {"id": k.replace("_", "-"), "n": s.name, "s": "an end of the plains of Moab",
            "a": list(s.aka),
            "dims": [["Identified with", s.site.name, s.site.certainty, []]],
            "tx": [["Why this site", s.site.why]] +
                  ([["Namesakes", s.namesakes]] if s.namesakes else []) +
                  [["Map point", f"Wikidata {s.site.qid}, as on the Land of Israel page"]],
            "note": s.card,
            "rg": [["Numbers 33", range_rows(s.num33)], ["Named in", rows(verses(s.refs))]],
            "r": rows(verses(s.refs)),
            "ln": [["On the Land of Israel page", atlas_link(s.site.gazetteer)]],
            "b": _bx((min(dotb[0], lb[0]), min(dotb[1], lb[1]), max(dotb[2], lb[2]),
                      max(dotb[3], lb[3]))),
            "t": [_bx(dotb, 5), _bx(lb, 2)], "fs": TIERS["D"][0], "fr": fr_round(x, y)}
    return item


def crossing_card(mp, idx):
    cr = WD.CROSSING
    R = mp.route
    lb = mp.spots["crossing"][4]
    pts = R.span
    xs, ys = zip(*pts)
    sb = (min(xs), min(ys) - 10, max(xs), max(ys) + 10)
    item = {"id": "the-sea", "n": "Through the middle of the sea",
            "s": "the crossing · Numbers 33:8",
            "a": ["Red Sea crossing", "the sea"],
            "dims": [["Tradition puts it", cr.site.name, cr.site.certainty, []]],
            "tx": [["Held since", cr.site.since],
                   ["The landing", cr.landing.name + ". " + cr.landing.why],
                   ["Other proposals", " ".join(f"{n}: {w}" for n, w in cr.proposals)],
                   ["Numbers 33 and the narrative", cr.differs],
                   ["Drawn", "Across Suez Bay, from under Jebel Ataqa to 'Uyun Musa: where the "
                             "tradition puts it, not a known place."]],
            "note": cr.card,
            "rg": [["Numbers 33", range_rows(cr.num33)], ["Named in", range_rows(cr.refs)],
                   ["The narrative", range_rows(cr.story)]],
            "r": range_rows(cr.story) + rows(verses("Num 33:8")),
            "b": _bx((min(sb[0], lb[0]), min(sb[1], lb[1]), max(sb[2], lb[2]), max(sb[3], lb[3]))),
            "t": [_bx(lb, 2)], "lo": along(pts), "pth": [round(v) for p in pts for v in p]}
    item["fr"] = [round(min(xs) - 300), round(min(ys) - 300), round(max(xs) - min(xs) + 600),
                  round(max(ys) - min(ys) + 600)]
    item["see"] = [idx[("event", e.key)] for e in WD.EVENTS if e.at == "crossing"]
    return item


def along(pts, step=20, size=26):
    out = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = max(1, int(math.hypot(x1 - x0, y1 - y0) / step))
        out += [[round(x0 + (x1 - x0) * i / n - size / 2, 1),
                 round(y0 + (y1 - y0) * i / n - size / 2, 1), size, size] for i in range(n)]
    x, y = pts[-1]
    out.append([round(x - size / 2, 1), round(y - size / 2, 1), size, size])
    return out


def thin(pts, step=12):
    out = [pts[0]]
    for p in pts[1:-1]:
        if math.dist(p, out[-1]) >= step:
            out.append(p)
    return out + [pts[-1]]


def leg_card(a, b, n, mp):
    pts = thin(mp.route.line(a, b))
    xs, ys = zip(*pts)
    sa, sb = WD.STATION[a], WD.STATION[b]
    item = {"id": f"leg-{a}-{b}".replace("_", "-"),
            "n": f"{label_text(a)} to {label_text(b)}",
            "s": f"leg {n} of 41 · camps {order_of(a)} to {order_of(b)}",
            "b": _bx((min(xs), min(ys), max(xs), max(ys)), 0), "t": [],
            "lo": along(pts), "pth": [round(v) for p in pts for v in p]}
    pad = 260
    item["fr"] = [round(min(xs) - pad), round(min(ys) - pad), round(max(xs) - min(xs) + 2 * pad),
                  round(max(ys) - min(ys) + 2 * pad)]
    first = WD.num33_verses(sb)[0]
    tx = []
    if not sa.site and not sa.ends or not sb.site and not sb.ends:
        tx.append(["The line", "Ours. A camp that is not identified is drawn in its order on "
                               "the traditional route, spaced evenly between the camps with "
                               "sites either side."])
    else:
        tx.append(["The line", "Ours: it joins the two sites and keeps to the land."])
    if a == "pihahiroth":
        tx.append(["The sea", "The dashed span over the water is the crossing where "
                              "tradition puts it (Numbers 33:8)."])
    km = km_along(pts)
    tx.append(["As drawn", f"about {km:,.0f} km ({km / 1.609344:,.0f} miles)"])
    item["tx"] = tx
    rg = [["Numbers 33", singles(f"Num 33:{first}")]]
    if (a, b) in WD.LEG_REFS:
        rg.append(["The narrative", rows(verses(WD.LEG_REFS[(a, b)]))])
    item["rg"] = rg
    item["r"] = singles(f"Num 33:{first}") + (rows(verses(WD.LEG_REFS[(a, b)]))
                                              if (a, b) in WD.LEG_REFS else [])
    return item


def event_card(e, mp, idx, rowxy):
    _e, (x, y), box = rowxy
    at = e.at
    if at == "crossing":
        where, see = "at the crossing of the sea", [idx["crossing"]]
    elif isinstance(at, tuple):
        where = f"between {in_words(at[0])} and {in_words(at[1])}"
        see = [idx[at[0]], idx[at[1]]]
    else:
        where, see = f"at {in_words(at)}", [idx[at]]
    item = {"id": "event-" + e.key, "n": cap(e.label), "s": where, "ly": "events",
            "b": _bx(box, 2), "fs": FS_EVENT, "note": e.note,
            "rg": [["Told in", range_rows(e.refs)]], "r": range_rows(e.refs), "see": see}
    ax, ay = mp.events[at][0]
    bx = mp.events[at][2]
    item["fr"] = [round(min(ax, bx[0]) - 200), round(min(ay, bx[1]) - 200),
                  round(max(ax, bx[2]) - min(ax, bx[0]) + 400),
                  round(max(ay, bx[3]) - min(ay, bx[1]) + 400)]
    if isinstance(at, tuple):
        item["tx"] = [["Where", f"Not at a camp: the mark stands halfway along the line "
                                f"{where}."]]
    return item


def landmark_card(k, mp):
    g = GZ.SITES[k]
    (x, y), r = mp.dots["lm-" + k]
    lb = mp.spots["lm-" + k][4]
    dotb = (x - r, y - r, x + r, y + r)
    every = rows(verses(g.refs))
    return {"id": "place-" + k.replace("_", "-"), "n": g.name, "s": "for bearings",
            "a": list(g.aka),
            "dims": [["Identified with", g.modern, g.certainty, []]],
            "tx": [["Why this site", g.why]] if g.why else [],
            "rg": [["Named in", every]], "r": [],
            "ln": [["On the Land of Israel page", atlas_link(k)]],
            "b": _bx((min(dotb[0], lb[0]), min(dotb[1], lb[1]), max(dotb[2], lb[2]),
                      max(dotb[3], lb[3]))),
            "t": [_bx(dotb, 5), _bx(lb, 2)], "fs": FS_LANDMARK}


WATER_CARDS = {
    "great_sea": ("The great sea", r"\b[Gg]reat [Ss]ea\b", "Dan 7:2",
                  "The Mediterranean, the great sea of Numbers 34:6."),
    "red_sea": ("Red Sea", r"\bRed Sea\b", "",
                "In the WEB both gulfs are the Red Sea: the sea crossed in Exodus 15:4 and "
                "15:22, and the sea by Ezion Geber in Numbers 21:4 and 1 Kings 9:26."),
    "gulf_suez": ("Gulf of Suez", "", "",
                  "The modern name. The WEB calls it the Red Sea: Israel crossed it, by "
                  "tradition, at its head, and camped “by the Red Sea” after Elim "
                  "(Numbers 33:10)."),
    "gulf_aqaba": ("Gulf of Aqaba", "", "",
                   "The modern name. The WEB calls it the Red Sea: Ezion Geber stood on its "
                   "shore (1 Kings 9:26), and Israel went “by the way to the Red Sea” to "
                   "go round Edom (Numbers 21:4)."),
    "salt_sea": ("Salt Sea", r"\bSalt Sea\b|\bsea of the Arabah\b", "",
                 "Drawn at its high water of about 1900. The southern basin is now dry."),
    "nile": ("Nile", r"\bNile\b", "",
             "Drawn by the towns on its banks, down the Damietta branch from the head of the "
             "delta."),
    "jordan": ("Jordan", r"\bJordan\b", "", "The plains of Moab lie on its east bank, across "
                                            "from Jericho (Numbers 33:48-49)."),
    "arnon": ("Arnon", r"\bArnon\b", "", "Moab's northern border (Numbers 21:13)."),
    "zered": ("Zered", r"\bZered\b", "", "Thirty-eight years after Kadesh Barnea they crossed "
                                         "it (Deuteronomy 2:13-14)."),
    "brook_of_egypt": ("brook of Egypt", r"\bbrook of Egypt\b", "",
                       "The land's south-western border (Numbers 34:5)."),
    "timsah": ("Lake Timsah", "", "", "The modern name; the Bible doesn't name it. One of the "
                                      "proposed places of the crossing (Haynes, 1896)."),
    "bitter": ("Bitter Lakes", "", "", "The modern name; the Bible doesn't name them. Some put "
                                       "the crossing here, on the isthmus."),
    "bardawil": ("Lake Bardawil", "", "", "Ancient Sirbonis, a lagoon behind a bar of sand; the "
                                          "Bible doesn't name it. Some put the crossing here "
                                          "(Schleiden, Brugsch)."),
}


def water_card(key, spot):
    name, find, skip, note = WATER_CARDS[key]
    found = rows(finds(find, skip)) if find else []
    _xy, fs, _anchor, _rot, b = spot
    item = {"id": "water-" + key.replace("_", "-"), "n": name, "s": "modern name" if key in MODERN
            else "sea" if "sea" in key else "lake" if key in ("salt_sea",) else "river",
            "b": _bx(b), "fs": fs, "note": note, "r": []}
    if found:
        item["rg"] = [["Named in" if len(found) <= 24 else "Named first in each book",
                       shown_rows(found)]]
        item["tx"] = [["The WEB names it", f"in {len(found)} verses"]]
    return item


def region_card(key):
    r = WD.REGIONS[key]
    found = rows(finds(r.find, r.skip)) if r.find else []
    spots = region_spot(key)
    item = {"id": "land-" + key, "n": r.name, "s": "land", "a": list(r.aka),
            "b": _bx(region_box(key)), "fs": region_lod(key)[0], "fx": region_lod(key)[1],
            "r": [],
            "t": [_bx(b, 4) for *_x, b in spots]}
    if r.note:
        item["note"] = r.note
    if found:
        item["rg"] = [["Named in" if len(found) <= 24 else "Named first in each book",
                       shown_rows(found)]]
        if len(found) > 24:
            item["tx"] = [["The WEB names it", f"in {len(found)} verses"]]
    return item


def variant_card(v, placed, box):
    return {"id": "list-" + v.key, "n": f"The route in {v.title}", "s": v.ref.replace(
            "Num", "Numbers").replace("Deut", "Deuteronomy").replace("Judg", "Judges"),
            "ly": "variants", "b": _bx(box, 4), "fs": FS_VARIANT,
            "tx": [["Its names, in order", " · ".join(v.names)]], "note": v.note,
            "rg": [["The passage", range_rows(v.ref)]], "r": range_rows(v.ref),
            "fr": [round(box[0] - 120), round(box[1] - 120), round(box[2] - box[0] + 240),
                   round(box[3] - box[1] + 240)]}


def date_card(d, m, boxes, idx):
    mb, lb = boxes
    when_ = f"year {d.year}" + (f", month {d.month}" if d.month else ", month 11 or 12") + \
        (f", day {d.day}" + (f" to {d.end_day}" if d.end_day else "") if d.day else "")
    where = d.station
    if where == "gilgal":
        see, wname = [idx["lm-gilgal_jericho"]], "Gilgal"
    else:
        see, wname = [idx[where]], label_text(where)
    item = {"id": "date-" + re.sub(r"[^a-z0-9]+", "-", d.ref.lower()).strip("-"),
            "n": cap(d.label), "s": f"{when_} · {wname}",
            "dims": [["Date", when_, "stated" if d.stated else "inferred", []]],
            "tx": ([["How it is worked out", d.inferred]] if d.inferred else [])
            + [["Camp", wname]],
            "note": d.card,
            "rg": [["The verse", rows(verses(d.ref))]] +
                  ([["See also", rows(verses(d.also))]] if d.also else []),
            "r": [], "see": see, "fs": FS_MARK,
            "b": _bx((min(mb[0], lb[0]), min(mb[1], lb[1]), max(mb[2], lb[2]), max(mb[3], lb[3]))),
            "t": [_bx(mb, 6), _bx(lb, 3)]}
    cx = COLS[m["col"]]
    item["fr"] = [cx - 20, round(m["y"] - 300), 900, 600]
    return item


def span_card(sp, boxes, idx, dated):
    bs = boxes
    item = {"id": "span-" + re.sub(r"[^a-z0-9]+", "-", sp.label.lower()).strip("-"),
            "n": cap(sp.label), "s": sp.length + (" · worked out" if sp.derived else "")
            + (" · its start inferred" if sp.placed else "")
            + (" · not dated" if not dated else ""),
            "b": _bx((min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs),
                      max(b[3] for b in bs))), "t": [_bx(b, 3) for b in bs],
            "note": sp.card, "fs": FS_SPAN if dated else 28, "r": []}
    tx = []
    if sp.start:
        a = sp.start
        tx.append(["From", f"year {a[0]}, month {a[1]}" + (f", day {a[2]}" if a[2] else "")])
    if sp.end:
        a = sp.end
        tx.append(["To", f"year {a[0]}, month {a[1]}" + (f", day {a[2]}" if a[2] else "")])
    if sp.note:
        tx.append(["Note", sp.note])
    if sp.station in WD.STATION:
        tx.append(["Camp", label_text(sp.station)])
        item["see"] = [idx[sp.station]]
    item["tx"] = tx
    item["rg"] = [["The verse", range_rows(sp.ref)]] + \
        ([["See also", range_rows(sp.also)]] if sp.also else [])
    return item


def uniq(rows_):
    """Rows less repeats, in their order."""
    seen, out = set(), []
    for r in rows_:
        if tuple(r) not in seen:
            seen.add(tuple(r))
            out.append(r)
    return out


def band_card(key, b):
    if key == "between":
        ref, note = WD.YEARS["between"]
        return {"id": "years-3-39", "n": "Years 3 to 39", "s": "not dated",
                "b": _bx(b), "fs": FS_YEAR, "note": note,
                "rg": [["Passages", range_rows(ref)]], "r": range_rows("Num 15-19")}
    if key == "year1":
        ref, note = WD.YEARS["count"]
        return {"id": "year-1", "n": "Year 1", "s": "the exodus year", "b": _bx(b),
                "fs": FS_YEAR, "note": note, "rg": [["Passages", range_rows(ref)]], "r": []}
    if key == "year41":
        ref, note = WD.YEARS["forty"]
        ref2, note2 = WD.YEARS["plains"]
        return {"id": "year-41", "n": "Year 41", "s": "the end of the forty years", "b": _bx(b),
                "fs": FS_YEAR, "note": note, "tx": [["The plains of Moab", note2]],
                "rg": [["Passages", uniq(range_rows(ref + "; " + ref2))]], "r": []}
    return None


def sidecar(mp, marks, spans, strip, keyb):
    band_boxes, span_boxes, mark_boxes, und_boxes = strip
    items, idx = [], {}

    def reserve(key):
        idx[key] = len(items)
        items.append(None)
    # the indexes first, so the cards can link to one another
    for s in WD.STATIONS:
        reserve(s.key)
    reserve("crossing")
    for k in WD.ENDS:
        reserve(k)
    order = [s.key for s in WD.STATIONS]
    leg_pairs = list(zip(order, order[1:]))
    for a, b in leg_pairs:
        reserve(("leg", a, b))
    for e in WD.EVENTS:
        reserve(("event", e.key))
    for k in LANDMARKS:
        reserve("lm-" + k)
    for m in marks:
        reserve(("date", m["d"].ref))
    legs_of = {}
    for a, b in leg_pairs:
        for k in (a, b):
            legs_of.setdefault(k, []).append(idx[("leg", a, b)])
    events_of, dates_of = {}, {}
    for e in WD.EVENTS:
        if isinstance(e.at, str) and e.at in WD.STATION:
            events_of.setdefault(e.at, []).append(e)
    for d in WD.DATES:
        dates_of.setdefault(d.station, []).append(d)
    for s in WD.STATIONS:
        items[idx[s.key]] = station_card(s, mp, idx, legs_of, dates_of, events_of)
    items[idx["crossing"]] = crossing_card(mp, idx)
    for k in WD.ENDS:
        it = end_card(k, mp)
        it["see"] = [idx["plains_of_moab"]]
        items[idx[k]] = it
    for n, (a, b) in enumerate(leg_pairs, 1):
        it = leg_card(a, b, n, mp)
        it["st"] = [idx[("leg", *leg_pairs[n - 2])] if n > 1 else None,
                    idx[("leg", *leg_pairs[n])] if n < len(leg_pairs) else None]
        it["see"] = [idx[a], idx[b]] + ([idx["crossing"]] if a == "pihahiroth" else [])
        items[idx[("leg", a, b)]] = it
    for at, (_a, rows_, _bx_) in mp.events.items():
        for row in rows_:
            items[idx[("event", row[0].key)]] = event_card(row[0], mp, idx, row)
    for k in LANDMARKS:
        it = landmark_card(k, mp)
        if k == "gilgal_jericho":
            it["see"] = [idx[("date", d.ref)] for d in WD.DATES if d.station == "gilgal"]
            it["tx"] = it["tx"] + [["Dates", "; ".join(date_words(d) for d in WD.DATES
                                                       if d.station == "gilgal")]]
        items[idx["lm-" + k]] = it
    for m in marks:
        items[idx[("date", m["d"].ref)]] = date_card(m["d"], m, mark_boxes[id(m)], idx)
    # the rest link to nothing
    for key, spot in mp.waters.items():
        items.append(water_card(key, spot))
    for key in WD.REGIONS:
        items.append(region_card(key))
    for v, placed, box in mp.vblocks:
        items.append(variant_card(v, placed, box))
    for sp, _pieces, _lane in spans:
        it = span_card(sp, span_boxes[sp.ref], idx, True)
        if sp.ref == "Josh 5:6":
            # the other spans counted in years are this one's
            for o in WD.SPANS:
                if o.years == 40 and o.ref not in LONG:
                    it["tx"].append([cap(o.label) + f" ({o.ref.replace('Num', 'Numbers')})",
                                     o.card + (" " + o.note if o.note else "")])
                    it["rg"].append([cap(o.label), range_rows(o.ref)])
        items.append(it)
    for sp in undated_spans():
        items.append(span_card(sp, [und_boxes[sp.ref]], idx, False))
    for key, b in band_boxes.items():
        it = band_card(key, b)
        if it:
            items.append(it)
    # the verses' books, numbered as the sheet uses them
    lists = lambda it: ([it.get("r", [])] + [rs for _g, rs in it.get("rg", [])]
                        + [d[3] for d in it.get("dims", [])])
    used = sorted({r[0] for it in items for rs in lists(it) for r in rs})
    remap = {b: i for i, b in enumerate(used)}
    done = set()
    for it in items:
        for r in (r for rs in lists(it) for r in rs):
            if id(r) not in done:
                done.add(id(r))
                r[0] = remap[r[0]]
    ids = [it["id"] for it in items]
    assert len(set(ids)) == len(ids), "ids collide"
    tours = []
    sheet_rows = lambda rs: [[remap[r[0]]] + r[1:] for rs_ in [rs] for r in rs_]
    for tid, label, a, b in (("egypt", "Egypt to Sinai", "rameses", "wilderness_of_sinai"),
                             ("paran", "Sinai to Kadesh", "wilderness_of_sinai", "kadesh"),
                             ("jordan", "Kadesh to the Jordan", "kadesh", "plains_of_moab")):
        tours.append({"id": tid, "label": label, "build": False,
                      "stops": tour_stops(a, b, idx, sheet_rows)})
    for it in items:
        if "fr" in it:
            it["fr"] = on_sheet(it["fr"])
    return {"version": 1, "card": "parts", "noun": ["camp or event", "camps and events"],
            "chapter": True, "tap": "inside", "step": "Camp to camp",
            "books": [BOOK_NAMES[b] for b in used],
            "views": [{"id": "map", "label": "Map", "fr": [0, 0, MAP_W, MAP_H]}] + year_views(),
            "layers": [{"id": "events", "label": "Events", "on": True},
                       {"id": "variants", "label": "Other itineraries", "on": False,
                        "fr": variant_frame(mp)}],
            "tours": tours, "items": items}


def on_sheet(fr):
    """A frame moved (and, if it must, cut) to lie on the sheet."""
    x, y, w, h = fr
    w, h = min(w, W), min(h, H)
    return [round(min(max(x, 0), W - w)), round(min(max(y, 0), H - h)), round(w), round(h)]


def year_views():
    """The forty years in two views, a column each, so that a phone opens
    on its months and its lengths' names: years 1 and 2, and years 3 to 41."""
    _c, foot0 = when(2, 12, 30)
    foot1 = max([m["ly"] for m in strip_marks() if m["col"] == 1]
                + [BANDS[-1]["y0"] + BANDS[-1]["months"] * U]) + 60
    return [{"id": "years", "label": "Years 1–2", "fr": [X0, 0, COLS[1] - X0 - 30, round(foot0 + 80)]},
            {"id": "years-3-41", "label": "Years 3–41",
             "fr": [COLS[1] - 50, 0, X0 + COL_W - COLS[1] + 50, round(foot1)]}]


def variant_frame(mp):
    bs = [b for _v, _p, b in mp.vblocks]
    x0, y0 = min(b[0] for b in bs) - 120, mp.vhead[1] - 140
    x1, y1 = max(b[2] for b in bs) + 120, max(b[3] for b in bs) + 120
    return [round(x0), round(y0), round(x1 - x0), round(y1 - y0)]


def tour_stops(a, b, idx, sheet_rows):
    """The camps from a to b that have a site or something that happened,
    and the events told between camps, in order."""
    order = [s.key for s in WD.STATIONS]
    keys = order[order.index(a):order.index(b) + 1]
    stops = []
    for k in keys:
        s = WD.STATION[k]
        evs = [e for e in WD.EVENTS if e.at == k]
        if s.site or s.ends or evs or k == a:
            r = range_rows(s.num33) + [r for e in evs for r in range_rows(e.refs)]
            stops.append({"i": idx[k], "r": sheet_rows(r)})
        if k == "pihahiroth":
            stops.append({"i": idx["crossing"],
                          "r": sheet_rows(range_rows("Num 33:8; Exod 14:21-31"))})
        for e in WD.EVENTS:
            if isinstance(e.at, tuple) and e.at[0] == k and e.at[1] in keys:
                stops.append({"i": idx[("event", e.key)], "r": sheet_rows(range_rows(e.refs))})
    return stops




def viewer_page():
    return reference_viewer.page(STEM, _fmt(W), _fmt(H), TITLE, data=True,
                                 placeholder="find a camp \u2014 Elim, Kadesh, Mount Hor\u2026")


def build():
    """Everything the generator writes, built in memory:
    {map, marks, spans, svg, data, html}."""
    bad = WD.misspelled()
    assert not bad, f"not spelled as Numbers 33 spells them: {bad}"
    mp = Map()
    marks = strip_marks()
    spans = dated_spans()
    svg, strip, keyb = build_svg(mp, marks, spans)
    data = sidecar(mp, marks, spans, strip, keyb)
    return dict(map=mp, marks=marks, spans=spans, svg=svg, data=data, html=viewer_page())


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    b = build()
    path = os.path.join(OUT_DIR, STEM + ".svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(b["svg"])
    dp = os.path.join(OUT_DIR, STEM + ".json")
    with open(dp, "w", encoding="utf-8") as f:
        json.dump(b["data"], f, ensure_ascii=False, separators=(",", ":"))
    vp = os.path.join(OUT_DIR, STEM + ".html")
    with open(vp, "w", encoding="utf-8") as f:
        f.write(b["html"])
    mp = b["map"]
    print(path)
    print(f"  {W} x {H} px \u00b7 {os.path.getsize(path) / 1024:.0f} KB \u00b7 "
          f"{len(mp.crowded)} names on leaders"
          + (f" ({', '.join(mp.crowded)})" if mp.crowded else ""))
    print(dp)
    print(f"  {len(b['data']['items'])} cards \u00b7 {os.path.getsize(dp) / 1024:.0f} KB")
    print(vp)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
