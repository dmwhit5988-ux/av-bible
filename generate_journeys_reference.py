"""Paul's journeys: the four journeys of Acts on one sheet, from Rome to
Jerusalem, with the places they name at the sites they are identified with,
and layers for the seven assemblies of Revelation 2-3 and the letters.

Writes web/visuals/reference/Pauls_journeys.svg, its sidecar
Pauls_journeys.json and the viewer page Pauls_journeys.html
(reference_viewer.page). The web app's Reference list opens it
(web/js/app.js REFERENCES). The coasts are point facts: mediterranean.py's
north, acts_geography's southern Asia Minor, Syria and Cyprus, and
gazetteer's Levant; the places, roads and sea courses are journeys.py's.
No line is traced from a map.

The sheet, north up, 360 px a degree of latitude:

- **The base.** The sea, the land, the Anatolian and Jordan lakes, the
  lands' names Acts and the letters use, the faint roads, and the places: a
  dot for each (filled where the site is known, a thick ring where it is
  probable, a thin ring where it is only possible).
- **The journeys** (a layer each, on): each in its own colour, a solid line
  by land, dashes by sea, dots where the way (or the stop) isn't stated,
  with an arrow on each leg. Where two journeys share a road their lines
  run side by side.
- **The seven assemblies** (a layer, off): Revelation's seven, numbered in
  the order of its letters, and Patmos, where it was written.
- **The letters** (a layer, off): what each of Paul's letters to a place is
  addressed to, and where 1 Corinthians says it was written.

A place's card gives the site, how sure it is and why, its journeys, its
letters and its verses in the New Testament. A leg's card gives what Acts
says, the road or course, and steps to the leg before and after. Opened
from a verse, the sheet starts on the places and legs that verse names, or
failing those the legs and letters whose passage it falls in.

    .venv\\Scripts\\python.exe generate_journeys_reference.py
"""

import json
import math
import os
import re

import acts_geography as G
import gazetteer as GZ
import journeys as J
import mediterranean as M
import reference_viewer
from books import BOOK_NAMES
from config import VISUALS_DIR
from generate_israel_atlas import (COAST_LINE, DOT, GRID, LAKE, TEXT_WEB, _bx, box_of,
                                   hits, inside, overlap, range_rows, rows, shown_rows,
                                   smooth, text, verses, word_verses, in_web)
from generate_tabernacle import BG, SAND, SAND_DIM, TEXT, TEXT_DIM
from generate_tribal_maps import LAND, SEA, WATER_TXT
from svg_map_camera import Projection, ink
from svg_surface import SvgCanvas, _fmt, _rgb

OUT_DIR = os.path.join(VISUALS_DIR, "reference")
STEM = "Pauls_journeys"
TITLE = "Paul's journeys"

LAT_TOP, LAT_BOT, LON_L, LON_R = 42.15, 31.10, 11.56, 36.95
K = 360                                     # px per degree of latitude
PROJ = Projection(LAT_TOP, LON_L, (LAT_TOP + LAT_BOT) / 2, K)
W = round((LON_R - LON_L) * PROJ.eff * K)
H = round((LAT_TOP - LAT_BOT) * K)
KM = K / 111.2                              # px per km

NT = BOOK_NAMES.index("Matthew")

# each journey's colour, and how far its line sits off a shared road
JOURNEY_COL = {"journey1": (236, 182, 82), "journey2": (98, 200, 224),
               "journey3": (236, 116, 128), "rome": (184, 160, 240)}
JOURNEY_OFF = {"journey1": -9, "journey2": -3, "journey3": 3, "rome": 9}
JOURNEY_SHORT = {"journey1": "First journey", "journey2": "Second journey",
                 "journey3": "Third journey", "rome": "To Rome"}
ROUTE_W = 5
ROAD = (92, 86, 66)
RING_REV = (240, 214, 120)
RING = 17                   # an assembly's ring, round its dot
LETTER_TXT = (226, 206, 150)

# (font, dot radius) by tier: the chief cities, the journeys' stops, the rest
TIERS = {"B": (40, 9), "C": (26, 6), "D": (17, 4)}
MAJOR = {"jerusalem", "antioch_syria", "rome", "ephesus", "corinth", "athens",
         "philippi", "thessalonica", "tarsus", "caesarea", "damascus"}
FS_REGION = 58
REGION_FADE = 70            # a land's name hides once it is this big on screen
FS_SEA = 30
FS_LETTER = 18
FS_NUMBER = 22              # an assembly's number
FS_KEY = 30                 # the key's text

MAST = (40, 800, 1000, 1150)      # x0, y0, x1, y1: the title, in the Tyrrhenian sea
LEGEND = (1430, 2560, 2870, 3290)  # the key, in the sea south of Sicily


def P(lat, lon):
    return PROJ.P(lat, lon)


# ---------------------------------------------------------------------------
# The land
# ---------------------------------------------------------------------------

def land_rings():
    """The mainlands as closed rings, each run off the sheet's edge and round
    its far side, and the islands."""
    out = []
    east = (M.ASIA_NORTH + M.ASIA_WEST[1:] + G.MAIN_COAST[1:] + GZ.COAST_SOUTH
            + M.AFRICA[1:])
    out.append(east + [(LAT_BOT - 1, LON_L - 1), (LAT_BOT - 1, LON_R + 1),
                       (LAT_TOP + 1, LON_R + 1), (LAT_TOP + 1, east[0][1])])
    greece = M.GREECE_WEST + M.GREECE_EAST
    out.append(greece + [(LAT_TOP + 1, greece[-1][1]), (LAT_TOP + 1, greece[0][1])])
    out.append(M.ITALY + [(LAT_TOP + 1, M.ITALY[-1][1]), (LAT_TOP + 1, M.ITALY[0][1])])
    return out


COASTS = [M.ASIA_NORTH, M.ASIA_WEST, G.MAIN_COAST, GZ.COAST_SOUTH, M.AFRICA,
          M.GREECE_WEST, M.GREECE_EAST, M.ITALY]
ISLANDS = list(M.ISLANDS.values()) + [G.CYPRUS]
LAKES = list(G.ANATOLIA_LAKES.values()) + [GZ.LAKES["galilee"], GZ.LAKES["salt_sea"]]


def draw_base(c):
    with c.group(data={"fs": 30}):
        for lat in range(32, 42, 2):
            y = P(lat, LON_L)[1]
            c.line((0, y), (W, y), GRID, 1.5)
            text(c, (W - 14, y - 8), f"{lat}°N", 30, GRID, "rd")
        for lon in range(12, 37, 2):
            x = P(LAT_TOP, lon)[0]
            c.line((x, 0), (x, H), GRID, 1.5)
            text(c, (x + 10, H - 14), f"{lon}°E", 30, GRID, "ld")
    for ring in land_rings():
        c.path(smooth(PROJ.PS(ring), closed=True), fill=LAND)
    for ring in ISLANDS:
        c.path(smooth(PROJ.PS(ring), closed=True), fill=LAND, stroke=COAST_LINE, width=2)
    for line in COASTS:
        c.path(smooth(PROJ.PS(line)), stroke=COAST_LINE, width=2.5)
    for ring in LAKES:
        c.path(smooth(PROJ.PS(ring), closed=True), fill=LAKE, stroke=COAST_LINE, width=1.5)
    # the roads, faint, under the journeys
    for road in J.ROADS.values():
        c.path(smooth(PROJ.PS(road.points)), stroke=ROAD, width=3, linecap="round")


# ---------------------------------------------------------------------------
# The verses
# ---------------------------------------------------------------------------

def nt_only(vs):
    return {v for v in vs if BOOK_NAMES.index(v[0]) >= NT}


def order(vs):
    return sorted(vs, key=lambda x: (BOOK_NAMES.index(x[0]), x[1], x[2]))


def place_names(p):
    """The words a place goes by in the WEB."""
    return list(dict.fromkeys([p.name] + [a for a in p.aka if in_web(a)]))


_PLACE_VERSES = {}


def place_verses(key):
    """Every New Testament verse that names the place: what its names find,
    less its `skip`, with its checked refs; only the refs where its name is
    another place's too (`search`)."""
    if key not in _PLACE_VERSES:
        p = J.PLACES[key]
        found = set()
        if p.search:
            found = nt_only({v for n in place_names(p) for v in word_verses(n)})
            found -= set(verses(p.skip))
        _PLACE_VERSES[key] = order(found | set(verses(p.refs)))
    return _PLACE_VERSES[key]


def finds_nt(pattern):
    pat = re.compile(pattern)
    return order(k for k, t in TEXT_WEB.items() if BOOK_NAMES.index(k[0]) >= NT
                 and pat.search(t))


def chapters(book):
    return max(c for b, c, _v in TEXT_WEB if b == book)


# ---------------------------------------------------------------------------
# The legs
# ---------------------------------------------------------------------------

def short(j):
    """'The first journey' -> 'First journey'."""
    n = j.name[4:] if j.name.startswith("The ") else j.name
    return n[:1].upper() + n[1:]


def stop_point(s):
    if s.place in J.REGIONS:
        r = J.REGIONS[s.place]
        return (r.lat, r.lon)
    p = J.PLACES[s.place]
    return (p.lat, p.lon)


def stop_name(s):
    return (J.REGIONS[s.place] if s.place in J.REGIONS else J.PLACES[s.place]).name


def road_between(points, a, b):
    """The stretch of a road from near `a` to near `b`, with a and b as its
    ends."""
    near = [min(range(len(points)), key=lambda i: math.dist(points[i], q)) for q in (a, b)]
    i, j = near
    mid = points[i + 1:j] if i <= j else list(reversed(points[j + 1:i]))
    return [a] + mid + [b]


def leg_line(s, a):
    """The leg to stop s from point a, in (lat, lon)."""
    b = s.at or stop_point(s)
    if s.via in J.ROADS:
        return road_between(J.ROADS[s.via].points, a, b)
    if s.via in J.COURSES:
        return [a] + J.COURSES[s.via] + [b]
    return [a, b]


def legs():
    """[(journey key, index from 1, stop before, stop, line)] in order."""
    out = []
    for jk, j in J.JOURNEYS.items():
        a = None
        for i, s in enumerate(j.stops):
            if s.by == "start":
                a = s.at or stop_point(s)
                prev = s
                continue
            line = leg_line(s, a)
            out.append((jk, i, prev, s, line))
            a, prev = line[-1], s
    return out


def offset(pts, d):
    """The line moved d px to its left, each point along the mean of its
    segments' normals, but for its ends, which stay on their stops."""
    if not d or len(pts) < 3:
        return pts
    out = [pts[0]]
    for i, (x, y) in enumerate(pts[1:-1], 1):
        ns, segs = [], []
        if i:
            segs.append((pts[i - 1], pts[i]))
        if i < len(pts) - 1:
            segs.append((pts[i], pts[i + 1]))
        for p, q in segs:
            dx, dy = q[0] - p[0], q[1] - p[1]
            m = math.hypot(dx, dy) or 1
            ns.append((dy / m, -dx / m))
        nx, ny = sum(n[0] for n in ns) / len(ns), sum(n[1] for n in ns) / len(ns)
        m = math.hypot(nx, ny) or 1
        out.append((x + nx / m * d, y + ny / m * d))
    return out + [pts[-1]]


_SHARED = None


def shared():
    """{(journey, stop index)} of the legs that share a stretch of their
    line with another journey's: only they run beside each other."""
    global _SHARED
    if _SHARED is None:
        key = lambda p: (round(p[0], 3), round(p[1], 3))
        by = {}
        all_legs = legs()
        for jk, _i, _a, _s, line in all_legs:
            for p in line[1:-1]:
                by.setdefault(key(p), set()).add(jk)
        _SHARED = {(jk, i) for jk, i, _a, _s, line in all_legs
                   if sum(len(by[key(p)]) > 1 for p in line[1:-1]) >= 2}
    return _SHARED


def drawn(jk, i, line):
    """The leg's line as the sheet draws it, in px."""
    return offset(PROJ.PS(line), JOURNEY_OFF[jk] if (jk, i) in shared() else 0)


def km_along(line):
    tot = 0
    for (la1, lo1), (la2, lo2) in zip(line, line[1:]):
        a = math.sin(math.radians(la2 - la1) / 2) ** 2 + math.cos(math.radians(la1)) * \
            math.cos(math.radians(la2)) * math.sin(math.radians(lo2 - lo1) / 2) ** 2
        tot += 2 * 6371 * math.asin(math.sqrt(a))
    return tot


def style(s):
    return "way" if not s.certain else s.by


DASH = {"land": None, "sea": "16 10", "way": "1 11"}


def stroke(c, d, col, width, dash=None, opacity=1.0):
    """A line with a dash pattern, which SvgCanvas.path has no word for."""
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    if opacity < 1:
        extra += f' opacity="{opacity:.2f}"'
    c._emit(f'<path d="{d}" fill="none" stroke="{_rgb(col)}" stroke-width="{_fmt(width)}" '
            f'stroke-linecap="round" stroke-linejoin="round"{extra}/>')


def arrow(c, pts, col):
    """A small arrowhead halfway along the line, pointing on."""
    seg = [math.dist(p, q) for p, q in zip(pts, pts[1:])]
    half = sum(seg) / 2
    if half < 40:
        return
    for (p, q), L in zip(zip(pts, pts[1:]), seg):
        if half <= L:
            t = half / L
            x, y = p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t
            ux, uy = (q[0] - p[0]) / L, (q[1] - p[1]) / L
            s = 13
            c.polygon([(x + ux * s, y + uy * s),
                       (x - ux * s * 0.7 - uy * s * 0.75, y - uy * s * 0.7 + ux * s * 0.75),
                       (x - ux * s * 0.7 + uy * s * 0.75, y - uy * s * 0.7 - ux * s * 0.75)],
                      fill=col, stroke=BG, width=1.5)
            return
        half -= L


def draw_journeys(c, all_legs):
    for jk in J.JOURNEYS:
        col = JOURNEY_COL[jk]
        with c.group(data={"layer": jk}):
            for _jk, i, _a, s, line in (x for x in all_legs if x[0] == jk):
                pts = drawn(jk, i, line)
                st = style(s)
                stroke(c, smooth(pts), col, ROUTE_W + (1.5 if st == "way" else 0), DASH[st])
                arrow(c, pts, col)


# ---------------------------------------------------------------------------
# The places
# ---------------------------------------------------------------------------

def stops_at():
    out = {}
    for jk, j in J.JOURNEYS.items():
        for s in j.stops:
            out.setdefault(s.place, set()).add(jk)
    return out


def tier(key):
    if key in MAJOR:
        return "B"
    if key in STOPS or key in REV:
        return "C"
    return "D"


STOPS = stops_at()
REV = {k for k, _r in J.ASSEMBLIES} | {"patmos"}
REV_LETTER = dict(J.ASSEMBLIES)


def draw_dot(c, x, y, r, certainty):
    if certainty == J.POSSIBLE:
        c.circle(x, y, r * 0.8, fill=LAND, stroke=DOT, width=r * 0.4)
    else:
        c.circle(x, y, r, fill=DOT, stroke=BG, width=r * 0.2)
        if certainty == J.PROBABLE:
            c.circle(x, y, r * 0.42, fill=LAND)


def places_of():
    out = []
    for key, p in J.PLACES.items():
        t = tier(key)
        fs, r = TIERS[t]
        x, y = P(p.lat, p.lon)
        out.append(dict(key=key, tier=t, fs=fs, r=r, x=x, y=y, text=p.name,
                        pad=RING if key in REV else r,
                        bold=t == "B", nref=len(place_verses(key))))
    return out


def candidates(x, y, r, fs):
    """Label spots round a dot, nearest first: eight at the dot, then further
    out with a leader line."""
    out = []
    for i, f in enumerate((1.0, 2.2, 3.6)):
        g = (r + 0.32 * fs) * f
        d = g * 0.72
        for anchor, dx, dy in (("lm", g, 0), ("rm", -g, 0), ("md", 0, -g),
                               ("ma", 0, g), ("ld", d, -d), ("la", d, d),
                               ("rd", -d, -d), ("ra", -d, d)):
            out.append((anchor, x + dx, y + dy, i > 0))
    return out


def road_marks(step=14):
    """Small boxes along the faint roads."""
    out = []
    for road in J.ROADS.values():
        pts = PROJ.PS(road.points)
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            n = max(1, int(math.hypot(x1 - x0, y1 - y0) / step))
            out += [(x0 + (x1 - x0) * i / n - 3, y0 + (y1 - y0) * i / n - 3,
                     x0 + (x1 - x0) * i / n + 3, y0 + (y1 - y0) * i / n + 3) for i in range(n)]
    return out


def route_marks(all_legs, step=14):
    """Small boxes along every journey's line, for the names to keep off."""
    out = []
    for jk, i, _a, _s, line in all_legs:
        pts = drawn(jk, i, line)
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            n = max(1, int(math.hypot(x1 - x0, y1 - y0) / step))
            for i in range(n):
                x, y = x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n
                out.append((x - 4, y - 4, x + 4, y + 4))
    return out


def place_labels(places, fixed, marks):
    """Greedy, the biggest names first: each at the first spot that touches
    no other name, no dot and nothing fixed, and crosses the fewest route
    lines; failing that, the spot that touches least."""
    dots = [(p["x"] - p["r"] - 2, p["y"] - p["r"] - 2, p["x"] + p["r"] + 2,
             p["y"] + p["r"] + 2) for p in places]
    taken = list(fixed)
    out, crowded = {}, []
    for p in sorted(places, key=lambda p: (-p["fs"], -p["nref"], p["key"])):
        own = (p["x"] - p["r"] - 2, p["y"] - p["r"] - 2, p["x"] + p["r"] + 2,
               p["y"] + p["r"] + 2)
        best, best_cost = None, None
        for anchor, x, y, leader in candidates(p["x"], p["y"], p["pad"], p["fs"]):
            b = box_of(p["text"], p["fs"], (x, y), anchor, p["bold"])
            if b[0] < 8 or b[1] < 8 or b[2] > W - 8 or b[3] > H - 8:
                continue
            cost = sum(overlap(b, t) + 1 for t in taken if hits(b, t, 3)) * 10
            cost += sum(overlap(b, d) + 1 for d in dots if d != own and hits(b, d, 2)) * 10
            cost += sum(1 for m in marks if hits(b, m)) * 3
            cost += 40 if leader else 0
            if best_cost is None or cost < best_cost:
                best, best_cost = (anchor, x, y, leader, b), cost
            if cost == 0:
                break
        if best_cost and best_cost >= 10:
            crowded.append(p["key"])
        out[p["key"]] = best
        taken.append(best[4])
    return out, crowded


def leader_line(c, p, spot, fs):
    x0, y0, x1, y1 = spot[4]
    tx_ = min(max(p["x"], x0), x1)
    ty_ = min(max(p["y"], y0), y1)
    dx, dy = tx_ - p["x"], ty_ - p["y"]
    m = math.hypot(dx, dy) or 1
    sx, sy = p["x"] + dx / m * (p["r"] + 2), p["y"] + dy / m * (p["r"] + 2)
    c.line((sx, sy), (tx_ - dx / m * 2, ty_ - dy / m * 2), TEXT_DIM, max(1, fs / 18))


# ---------------------------------------------------------------------------
# Lands, waters, letters and the assemblies
# ---------------------------------------------------------------------------

_REGION_AT = {}


def place_regions(marks):
    """Each land's name at its spot, or nudged a little where that crosses
    fewer of the journeys' lines, and kept inside the sheet."""
    for key, r in J.REGIONS.items():
        x0, y0 = P(r.lat, r.lon)
        s = r.name.upper()
        best = None
        for dx, dy in ((0, 0), (0, -70), (0, 70), (-140, 0), (140, 0), (-140, -70),
                       (140, -70), (-140, 70), (140, 70), (0, -140), (0, 140)):
            b = box_of(s, FS_REGION, (x0 + dx, y0 + dy), "mm", spacing=FS_REGION * 0.18)
            shift = max(0, 12 - b[0]) - max(0, b[2] - (W - 12))
            b = (b[0] + shift, b[1], b[2] + shift, b[3])
            cost = sum(1 for m in marks if hits(b, m)) + (abs(dx) + abs(dy)) / 140
            if best is None or cost < best[0]:
                best = (cost, (x0 + dx + shift, y0 + dy))
        _REGION_AT[key] = best[1]


def region_box(key):
    r = J.REGIONS[key]
    xy = _REGION_AT.get(key) or P(r.lat, r.lon)
    s = r.name.upper()
    return xy, s, box_of(s, FS_REGION, xy, "mm", spacing=FS_REGION * 0.18)


def water_box(key):
    r = J.WATERS[key]
    xy = P(r.lat, r.lon)
    s = r.name[:1].upper() + r.name[1:]
    return xy, s, box_of(s, FS_SEA, xy, "mm", italic=True)


def letters_by_place():
    """{place or region key: [(letter, 'to' | 'from')]}, in the canon's order."""
    out = {}
    for lt in J.LETTERS:
        if lt.name == "Revelation":
            continue
        for k in lt.to:
            out.setdefault(k, []).append((lt, "to"))
        if lt.written:
            out.setdefault(lt.written, []).append((lt, "from"))
    return out


def letter_line(lt, way):
    return lt.name if way == "to" else f"{lt.name}, written here"


def letter_blocks(spots, taken, marks):
    """{key: [(letter, way, (x, y), box)]}: each place's letters stacked
    under (or beside) its name, where they touch least."""
    out = {}
    for key, lts in letters_by_place().items():
        lines = [letter_line(lt, w) for lt, w in lts]
        if key in J.REGIONS:
            (x, y), _s, b = region_box(key)
            spots_try = [((b[0] + b[2]) / 2, b[3] + 8, "ma")]
        else:
            b = spots[key][4]
            p = J.PLACES[key]
            px, py = P(p.lat, p.lon)
            spots_try = [((b[0] + b[2]) / 2, b[3] + 4, "ma"), ((b[0] + b[2]) / 2, b[1] - 4 - 22 * (len(lines) - 1) - FS_LETTER, "ma"),
                         (b[2] + 10, py - 11 * (len(lines) - 1), "lm"),
                         (b[0] - 10, py - 11 * (len(lines) - 1), "rm")]
        best, best_cost = None, None
        for x, y, anchor in spots_try:
            boxes = [box_of(s, FS_LETTER, (x, y + i * 22), anchor, italic=True)
                     for i, s in enumerate(lines)]
            cost = sum(overlap(bb, t) + 1 for bb in boxes for t in taken if hits(bb, t, 2)) * 10
            cost += sum(1 for bb in boxes for m in marks if hits(bb, m)) * 3
            if best_cost is None or cost < best_cost:
                best, best_cost = [(lt, w, (x, y + i * 22), anchor, boxes[i])
                                   for i, (lt, w) in enumerate(lts)], cost
        out[key] = best
        taken += [x[4] for x in best]
    return out


def draw_regions(c):
    with c.group(data={"fs": FS_REGION, "fmax": REGION_FADE}):
        for key in J.REGIONS:
            xy, s, _b = region_box(key)
            text(c, xy, s, FS_REGION, (150, 138, 104), "mm", spacing=FS_REGION * 0.18,
                 opacity=0.8)
    with c.group(data={"fs": FS_SEA}):
        for key in J.WATERS:
            xy, s, _b = water_box(key)
            text(c, xy, s, FS_SEA, WATER_TXT, "mm", italic=True)


def draw_assemblies(c):
    with c.group(data={"layer": "assemblies"}):
        pts = [P(J.PLACES[k].lat, J.PLACES[k].lon) for k, _r in J.ASSEMBLIES]
        stroke(c, smooth(pts), RING_REV, 3, "2 9", 0.8)
        for n, (x, y) in enumerate(pts, 1):
            c.circle(x, y, RING, stroke=RING_REV, width=3.5)
        px, py = P(J.PLACES["patmos"].lat, J.PLACES["patmos"].lon)
        c.circle(px, py, RING, stroke=RING_REV, width=3.5)
        c.circle(px, py, RING + 7, stroke=RING_REV, width=2)
        with c.group(data={"fs": FS_NUMBER}):
            for n, (x, y) in enumerate(pts, 1):
                c.circle(x - 21, y - 21, 13, fill=RING_REV, stroke=BG, width=2)
                text(c, (x - 21, y - 20.5), str(n), 20, BG, "mm", bold=True)


def number_box(key):
    p = J.PLACES[key]
    x, y = P(p.lat, p.lon)
    return (x - 34, y - 34, x - 8, y - 8)


def draw_letters(c, blocks):
    with c.group(data={"layer": "letters"}):
        with c.group(data={"fs": FS_LETTER}):
            for key, block in blocks.items():
                for lt, way, xy, anchor, _b in block:
                    text(c, xy, letter_line(lt, way), FS_LETTER, LETTER_TXT, anchor,
                         italic=True)
        for key, block in blocks.items():
            if key in J.PLACES and any(w == "from" for _lt, w, *_ in block):
                x, y = P(J.PLACES[key].lat, J.PLACES[key].lon)
                c.rect(x - 15, y - 15, 30, 30, stroke=LETTER_TXT, width=3)


def draw_masthead(c):
    with c.group(data={"fs": 100}):
        text(c, (MAST[0] + 20, MAST[1] + 60), TITLE, 100, TEXT, "lm", bold=True)
    with c.group(data={"fs": 40}):
        text(c, (MAST[0] + 24, MAST[1] + 160), "Acts 13-28, and the letters", 40, TEXT_DIM,
             "lm", italic=True)
    with c.group(data={"fs": 30}):
        text(c, (MAST[0] + 24, MAST[1] + 230),
             f"{len(J.PLACES)} places, at the sites they are identified with",
             30, TEXT_DIM, "lm")


def draw_legend(c):
    x0, y0 = LEGEND[0] + 34, LEGEND[1] + 50
    fs = FS_KEY
    boxes = {}
    with c.group(data={"fs": fs}):
        c.rect(LEGEND[0], LEGEND[1], LEGEND[2] - LEGEND[0], LEGEND[3] - LEGEND[1],
               fill=(SEA[0] - 6, SEA[1] - 8, SEA[2] - 10), stroke=SAND_DIM, width=2, rx=18)
        y = y0
        for jk, j in J.JOURNEYS.items():
            c.line((x0, y), (x0 + 90, y), JOURNEY_COL[jk], ROUTE_W + 1)
            text(c, (x0 + 110, y), short(j), fs, TEXT, "lm")
            text(c, (x0 + 560, y), j.refs, fs, TEXT_DIM, "lm")
            boxes[jk] = (x0 - 10, y - 24, LEGEND[2] - 30, y + 24)
            y += 56
        y += 16
        for st, word in (("land", "by land"), ("sea", "by sea"), ("way", "the way, or the stop, not stated")):
            stroke(c, f"M{_fmt(x0)},{_fmt(y)} L{_fmt(x0 + 90)},{_fmt(y)}", SAND,
                   ROUTE_W + (1.5 if st == "way" else 0), DASH[st])
            text(c, (x0 + 110, y), word, fs, TEXT, "lm")
            y += 50
        c.line((x0, y), (x0 + 90, y), ROAD, 3)
        text(c, (x0 + 110, y), "a road", fs, TEXT, "lm")
        y += 50
        y += 14
        x = x0 + 12
        for cert, word in ((J.KNOWN, "known site"), (J.PROBABLE, "probable"),
                           (J.POSSIBLE, "possible")):
            draw_dot(c, x, y, 11, cert)
            text(c, (x + 24, y), word, fs, TEXT, "lm")
            x += 70 + ink(word, fs, False, False, "lm")[2]
        y += 56
        text(c, (x0, y), "the coasts as they are today", fs, TEXT_DIM, "lm", italic=True)
        # the scale
        y += 70
        km = 200
        c.line((x0, y), (x0 + km * KM, y), SAND, 5)
        for i in range(0, km + 1, 50):
            xx = x0 + i * KM
            c.line((xx, y - 12), (xx, y), SAND, 3)
            text(c, (xx, y + 10), str(i), 26, TEXT_DIM, "ma")
        text(c, (x0 + km * KM + 20, y), "km", 26, TEXT_DIM, "lm")
        mi = 100
        xs = x0 + 720
        c.line((xs, y), (xs + mi * 1.609344 * KM, y), SAND, 5)
        for i in range(0, mi + 1, 50):
            xx = xs + i * 1.609344 * KM
            c.line((xx, y - 12), (xx, y), SAND, 3)
            text(c, (xx, y + 10), str(i), 26, TEXT_DIM, "ma")
        text(c, (xs + mi * 1.609344 * KM + 20, y), "miles", 26, TEXT_DIM, "lm")
    return boxes


def build_svg(places, spots, all_legs, blocks):
    c = SvgCanvas(W, H, bg=SEA)
    draw_base(c)
    draw_regions(c)
    draw_journeys(c, all_legs)
    draw_assemblies(c)
    by_tier = {t: [p for p in places if p["tier"] == t] for t in "DCB"}
    for t in "DCB":
        fs, r = TIERS[t]
        with c.group(data={"fs": fs}):
            for p in by_tier[t]:
                spot = spots[p["key"]]
                if spot[3]:
                    leader_line(c, p, spot, fs)
                draw_dot(c, p["x"], p["y"], p["r"], J.PLACES[p["key"]].certainty)
                text(c, spot[1:3], p["text"], fs, TEXT if t != "B" else (240, 228, 196),
                     spot[0], bold=p["bold"])
    draw_letters(c, blocks)
    draw_masthead(c)
    boxes = draw_legend(c)
    return c.tostring().replace(
        "<svg ", f'<svg data-kind="map" data-title="{TITLE}" ', 1), boxes


# ---------------------------------------------------------------------------
# The sidecar
# ---------------------------------------------------------------------------

def along(pts, step=20, size=26):
    out = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = max(1, int(math.hypot(x1 - x0, y1 - y0) / step))
        out += [[round(x0 + (x1 - x0) * i / n - size / 2, 1),
                 round(y0 + (y1 - y0) * i / n - size / 2, 1), size, size] for i in range(n)]
    x, y = pts[-1]
    out.append([round(x - size / 2, 1), round(y - size / 2, 1), size, size])
    return out


def bbox(pts, pad=6):
    xs, ys = zip(*pts)
    return (min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad)


def first_clause(s):
    for sep in (" (", ";", ","):
        s = s.split(sep)[0]
    return s.strip()


def place_card(key, p, spot, leg_ids):
    sub = [first_clause(p.region)] if p.region else []
    item = {"id": key.replace("_", "-"), "n": p.name, "s": " · ".join(sub),
            "a": list(p.aka),
            "dims": [["Identified with", p.modern, p.certainty, []]],
            "fs": TIERS[tier(key)][0]}
    tx = []
    if p.why:
        tx.append(["Why this site", p.why])
    others = [a for a in p.aka if a != p.name]
    if others:
        tx.append(["Other names", ", ".join(others)])
    if p.region and p.region != item["s"]:
        tx.append(["Where", p.region])
    if p.letters:
        tx.append(["Letters", p.letters])
    tx.append(["Map point", p.point[:1].upper() + p.point[1:] if p.point else f"Wikidata {p.qid}"])
    item["tx"] = tx
    if p.note:
        item["note"] = p.note
    every = place_verses(key)
    rg = []
    for jk, j in J.JOURNEYS.items():
        refs = "; ".join(s.ref for s in j.stops if s.place == key)
        if refs:
            rg.append([short(j), range_rows(refs)])
    shown = rows(every) if len(every) <= 24 else shown_rows(rows(every))
    rg.append(["Named in" if len(every) <= 24 else "Named first in each book", shown])
    item["rg"] = rg
    if len(every) > 24:
        tx.insert(1 if p.why else 0, ["The New Testament names it", f"in {len(every)} verses"])
    # an assembly's letter in Revelation 2-3 finds it from any of its verses
    item["r"] = rows(every) + range_rows(REV_LETTER[key]) if key in REV_LETTER else rows(every)
    item["see"] = leg_ids
    x, y = P(p.lat, p.lon)
    r = TIERS[tier(key)][1]
    dotb = (x - r, y - r, x + r, y + r)
    lb = spot[4]
    u = (min(dotb[0], lb[0]), min(dotb[1], lb[1]), max(dotb[2], lb[2]), max(dotb[3], lb[3]))
    item["b"] = _bx(u)
    item["t"] = [_bx(dotb, 5), _bx(lb, 2)]
    return item


def leg_card(jk, i, a, s, line, n_legs, number, repeat=1):
    j = J.JOURNEYS[jk]
    how = {"land": "by land", "sea": "by sea"}[s.by]
    sub = [short(j), f"leg {number} of {n_legs}", how]
    if not s.certain:
        sub.append("not all stated")
    pts = drawn(jk, i, line)
    # named by its ends, so a shared link outlives a stop added before it
    lid = f"{jk}-{a.place}-{s.place}".replace("_", "-") + (f"-{repeat}" if repeat > 1 else "")
    item = {"id": lid, "n": f"{stop_name(a)} to {stop_name(s)}",
            "s": " · ".join(sub), "ly": jk, "b": _bx(bbox(pts), 0), "t": [],
            "lo": along(pts), "pth": [round(v) for xy in pts for v in xy]}
    tx = []
    if s.via in J.ROADS:
        road = J.ROADS[s.via]
        tx.append(["The road", f"{road.name}. {road.why}"])
    elif s.via in J.COURSES:
        tx.append(["The line", "Ours: it keeps to the sea, past the capes and islands on "
                               "the way." if s.by == "sea" else
                   "Ours: the text doesn't give the way, and the line only keeps "
                   "to the land."])
    d = km_along(line)
    tx.append(["As drawn", f"about {d:,.0f} km ({d / 1.609344:,.0f} miles)"])
    item["tx"] = tx
    if s.note:
        item["note"] = s.note
    rs = range_rows(s.ref)
    acts = BOOK_NAMES.index("Acts")
    item["rg"] = [[label, part] for label, part in
                  (("Acts says", [r for r in rs if r[0] == acts]),
                   ("Paul writes", [r for r in rs if r[0] != acts])) if part]
    item["r"] = [r[:] for r in rs]
    return item


def region_card(key, r, b, kind):
    found = rows(finds_nt(r.find)) if r.find else []
    item = {"id": f"{kind}-{key.replace('_', '-')}", "n": r.name[:1].upper() + r.name[1:],
            "s": "land" if kind == "land" else "sea", "a": list(r.aka), "b": _bx(b),
            "r": found}
    if kind == "land":
        item.update(fs=FS_REGION, fx=REGION_FADE)
    else:
        item["fs"] = FS_SEA
    if r.note:
        item["note"] = r.note
    if found:
        item["rg"] = [["Named in" if len(found) <= 24 else "Named first in each book",
                       shown_rows(found)]]
        if len(found) > 24:
            item["tx"] = [["The New Testament names it", f"in {len(found)} verses"]]
    return item


def letter_card(lt, boxes, index):
    b = BOOK_NAMES.index(lt.name)
    to = [(J.PLACES[k] if k in J.PLACES else J.REGIONS[k]).name for k in lt.to]
    item = {"id": "letter-" + lt.name.lower().replace(" ", "-"), "n": lt.name,
            "s": "a letter to " + (", ".join(to) if len(to) < 3 else "the seven assemblies"),
            "ly": "assemblies" if lt.name == "Revelation" else "letters",
            "b": _bx(boxes[0]), "t": [_bx(x) for x in boxes],
            "fs": FS_NUMBER if lt.name == "Revelation" else FS_LETTER}
    tx = [["To", ", ".join(to)]]
    tx.append(["Written", J.PLACES[lt.written].name if lt.written else
               "where, the letter doesn't say"])
    item["tx"] = tx
    if lt.note:
        item["note"] = lt.note
    rg = [["To", range_rows(lt.to_ref)]]
    if lt.written_ref:
        rg.append(["Written", range_rows(lt.written_ref)])
    item["rg"] = rg
    item["r"] = [[b, 1, 0, chapters(lt.name), 0]] + range_rows(lt.to_ref) + \
        (range_rows(lt.written_ref) if lt.written_ref else [])
    item["see"] = [index[k] for k in lt.to + ((lt.written,) if lt.written else ())
                   if k in index]
    return item


def journey_card(jk, j, box, leg_ids, all_legs):
    d = sum(km_along(line) for k, _i, _a, _s, line in all_legs if k == jk)
    stops = j.stops
    item = {"id": f"route-{jk}", "n": short(j), "s": j.refs, "b": _bx(box, 0),
            "ly": jk, "nos": True, "fs": FS_KEY,
            "tx": [["Stops", f"{len(stops) - 1} legs, from {stop_name(stops[0])} "
                             f"to {stop_name(stops[-1])}"],
                   ["As drawn", f"about {d:,.0f} km ({d / 1.609344:,.0f} miles)"]],
            "rg": [["Acts", range_rows(j.refs)]],
            "r": range_rows(j.refs), "st": [None, leg_ids[0]]}
    return item


def sidecar(places, spots, all_legs, blocks, legend_boxes):
    items, index = [], {}
    # the legs first, so the places can link to them
    leg_index = {}
    n_of = {jk: sum(1 for x in all_legs if x[0] == jk) for jk in J.JOURNEYS}
    num, pairs = {}, {}
    for jk, i, a, s, line in all_legs:
        num[jk] = num.get(jk, 0) + 1
        pair = (jk, a.place, s.place)
        pairs[pair] = pairs.get(pair, 0) + 1
        leg_index[(jk, i)] = len(items)
        items.append(leg_card(jk, i, a, s, line, n_of[jk], num[jk], pairs[pair]))
    for jk in J.JOURNEYS:
        ids = [leg_index[(k, i)] for k, i, *_ in all_legs if k == jk]
        for n, li in enumerate(ids):
            items[li]["st"] = [ids[n - 1] if n else None, ids[n + 1] if n + 1 < len(ids) else None]
    touching = {}
    for jk, i, a, s, line in all_legs:
        for k in (a.place, s.place):
            touching.setdefault(k, []).append(leg_index[(jk, i)])
    for key, p in J.PLACES.items():
        index[key] = len(items)
        items.append(place_card(key, p, spots[key], sorted(set(touching.get(key, [])))))
    for jk, j in J.JOURNEYS.items():
        ids = [leg_index[(k, i)] for k, i, *_ in all_legs if k == jk]
        items.append(journey_card(jk, j, legend_boxes[jk], ids, all_legs))
    for key, r in J.REGIONS.items():
        index[key] = len(items)
        items.append(region_card(key, r, region_box(key)[2], "land"))
    for key, r in J.WATERS.items():
        items.append(region_card(key, r, water_box(key)[2], "water"))
    # the letters: each line under its place, and Revelation's numbers
    lines_of = {}
    for key, block in blocks.items():
        for lt, way, _xy, _a, b in block:
            lines_of.setdefault(lt.name, []).append(b)
    lines_of["Revelation"] = [number_box(k) for k, _r in J.ASSEMBLIES]
    for lt in J.LETTERS:
        items.append(letter_card(lt, lines_of[lt.name], index))
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
    return {"version": 1, "card": "parts", "noun": ["place or leg", "places and legs"],
            "chapter": True, "tap": "inside", "step": "Legs", "books": [BOOK_NAMES[b] for b in used],
            "layers": [{"id": jk, "label": JOURNEY_SHORT[jk], "on": True}
                       for jk in J.JOURNEYS]
            + [{"id": "assemblies", "label": "The seven assemblies", "on": False},
               {"id": "letters", "label": "The letters", "on": False}],
            "items": items}


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    all_legs = legs()
    places = places_of()
    marks = route_marks(all_legs)
    place_regions(marks)
    region_boxes = [region_box(k)[2] for k in J.REGIONS] + [water_box(k)[2] for k in J.WATERS]
    fixed = [MAST, LEGEND] + region_boxes
    spots, crowded = place_labels(places, fixed, marks)
    taken = fixed + [s[4] for s in spots.values()] + \
        [(p["x"] - p["r"], p["y"] - p["r"], p["x"] + p["r"], p["y"] + p["r"]) for p in places]
    blocks = letter_blocks(spots, taken, marks + road_marks())
    svg, legend_boxes = build_svg(places, spots, all_legs, blocks)
    path = os.path.join(OUT_DIR, STEM + ".svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    data = sidecar(places, spots, all_legs, blocks, legend_boxes)
    dp = os.path.join(OUT_DIR, STEM + ".json")
    with open(dp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    vp = os.path.join(OUT_DIR, STEM + ".html")
    with open(vp, "w", encoding="utf-8") as f:
        f.write(reference_viewer.page(
            STEM, _fmt(W), _fmt(H), TITLE, data=True,
            placeholder="find a place — Troas, Lystra, Malta…"))
    print(path)
    print(f"  {W} x {H} px · {os.path.getsize(path) / 1024:.0f} KB · "
          f"{len(places)} places · {len(all_legs)} legs · {len(crowded)} names crowded"
          + (f" ({', '.join(crowded)})" if crowded else ""))
    print(dp)
    print(f"  {len(data['items'])} cards · "
          f"{sum(len(it.get('r', [])) for it in data['items'])} verse refs · "
          f"{os.path.getsize(dp) / 1024:.0f} KB")
    print(vp)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
