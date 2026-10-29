"""The Land of Israel atlas: the land from Sidon to Kadesh Barnea, with the
places the WEB names at the sites they are identified with, and a card for
each place, water and land.

Writes web/visuals/reference/Land_of_Israel.svg, its sidecar
Land_of_Israel.json and the viewer page Land_of_Israel.html
(reference_viewer.page). The web app's Reference list opens it
(web/js/app.js REFERENCES). Everything drawn comes from gazetteer.py, whose
lines and sites are point facts; no line is traced from a map.

The sheet, north up, 2,400 px a degree of latitude (about 21.6 px a km):

- **The base.** The sea, the land, the lakes at high water, the rivers, the
  lands' and waters' names, and the places: a dot for each (filled where the
  site is known, a thick ring where it is probable, a thin ring where it is
  only possible), a triangle for a mountain.
- **Text by size.** Names are grouped by size (`<g data-fs>`), and the
  viewer draws a group only once its text can be read: the lands and the
  Great Sea at first, then the chief cities, the larger towns, and the rest
  as you zoom in. The lands' and the tribes' names fade out as the towns
  come in.
- **The tribes** (a layer, off): each tribe's towns from Joshua 13-21 under
  one soft colour, its name at their middle, and rings for the Levites'
  cities and the cities of refuge. No border is drawn.
- **In Jesus' day** (a layer, off): a ring round each place the Gospels or
  Acts name, and the names Judea, Phoenicia and the Decapolis.

A place's card gives the site it is identified with and how sure that is,
why, its other names, its tribe, how far it lies from Jerusalem, where the
point comes from, its namesakes, and its verses. Opened from a verse, the
sheet starts on the places that verse names, or failing those the
chapter's.

    .venv\\Scripts\\python.exe generate_israel_atlas.py
"""

import bisect
import itertools
import json
import math
import os
import re

import gazetteer as GZ
import reference_viewer
import verse_refs
from books import BOOK_NAMES
from config import BIBLES_DIR, VISUALS_DIR
from generate_tabernacle import BG, GOLD, SAND, SAND_DIM, TEXT, TEXT_DIM
from generate_tribal_maps import LAND, RIVER, SEA, TRIBE_COL, WATER_TXT
from svg_map_camera import Projection, ink
from svg_surface import FONT_FAMILY, SvgCanvas, _fmt, _rgb

OUT_DIR = os.path.join(VISUALS_DIR, "reference")
STEM = "Land_of_Israel"
TITLE = "The Land of Israel"

LAT_TOP, LAT_BOT, LON_L, LON_R = 33.65, 30.45, 33.80, 36.80
K = 2400                                    # px per degree of latitude
PROJ = Projection(LAT_TOP, LON_L, (LAT_TOP + LAT_BOT) / 2, K)
W = round((LON_R - LON_L) * PROJ.eff * K)
H = round((LAT_TOP - LAT_BOT) * K)
KM = K / 111.2                              # px per km

LAKE = (28, 48, 72)
COAST_LINE = (70, 100, 132)
DOT = (236, 224, 196)
MOUNT = (176, 156, 118)
REGION = (132, 122, 96)
GRID = (60, 66, 70)
RING_NT = GOLD
RING_LEV = (200, 182, 130)

# Text sizes (px on the sheet). The viewer shows a size once it is 7.5 px
# on screen: the lands at the whole sheet, the chief cities from about
# twice that zoom, the rest as you come in.
FS_REGION, FS_SEA = 130, 150        # 130: readable at the whole sheet on a 375-px phone
TIERS = {"B": (60, 12), "C": (34, 8), "D": (19, 5)}     # (font, dot radius)
REGION_FADE = 40            # a land's name hides once it is this big on screen
# a tribe's name, under the places' names and gone before the larger towns'
# come in
TRIBE_FS, TRIBE_FADE = 70, 15
# the narrow lands' names are smaller, to fit them
REGION_FS = {"sharon": 80, "philistia": 90, "arabah": 80, "zin": 90,
             "phoenicia": 90, "decapolis": 90}

# the chief cities, named from the whole land
MAJOR = {
    "jerusalem", "damascus", "tyre", "sidon", "samaria", "shechem", "hebron",
    "beersheba", "dan", "gaza", "joppa", "caesarea", "jericho", "capernaum",
    "nazareth", "bethlehem_judah", "megiddo", "rabbah_ammon", "bethel",
    "shiloh", "hazor_naphtali", "kadesh_barnea", "heshbon", "ashkelon",
    "beth_shean", "en_gedi", "mount_hermon", "mount_carmel", "lachish",
    "dibon",
}
MOUNT_LABEL = {"Carmel": "Mount Carmel", "Gilboa": "Mount Gilboa",
               "Hermon": "Mount Hermon", "Tabor": "Mount Tabor"}
VALLEY_LABEL = {"valley_of_elah": "valley of Elah"}        # 1 Sam 17:2

# where the waters' names sit: (lat, lon, size, anchor). Huleh and the
# Yarmuk, which the Bible doesn't name, are left unnamed on the sheet; a tap
# on them still opens their cards.
WATER_LABELS = {
    "great_sea": (32.55, 34.20, FS_SEA, "mm"),
    "salt_sea": (31.50, 35.475, 56, "mm"),
    "galilee": (32.815, 35.590, 24, "mm"),
    "jordan": (32.30, 35.585, 40, "lm"),
    "jabbok": (32.175, 35.835, 28, "ma"),
    "arnon": (31.418, 35.720, 28, "ma"),
    "zered": (30.950, 35.730, 28, "ma"),
    "kishon": (32.640, 35.205, 24, "lm"),
    "yarkon": (32.122, 34.860, 22, "md"),
    "brook_of_egypt": (30.985, 33.990, 26, "lm"),
}
RIVER_WIDTH = {"jordan_upper": 5, "jordan_lower": 5}

# The tribes' allotments, for the tribes' own cards (#at lights the tribe
# while you read its chapter). Manasseh's two halves have one each.
ALLOTMENT = {
    "Reuben": "Josh 13:15-23", "Gad": "Josh 13:24-28",
    "Manasseh east": "Josh 13:29-31", "Manasseh west": "Josh 17:1-13",
    "Judah": "Josh 15:1-63",
    "Ephraim": "Josh 16:1-10", "Benjamin": "Josh 18:11-28",
    "Simeon": "Josh 19:1-9", "Zebulun": "Josh 19:10-16",
    "Issachar": "Josh 19:17-23", "Asher": "Josh 19:24-31",
    "Naphtali": "Josh 19:32-39", "Dan": "Josh 19:40-48",
}
NT_FIRST, NT_LAST = BOOK_NAMES.index("Matthew"), BOOK_NAMES.index("Romans")
TRIBE_NAMES = {k.split()[0] for k in ALLOTMENT}


def P(lat, lon):
    return PROJ.P(lat, lon)


# ---------------------------------------------------------------------------
# The WEB, for the verses that name a place
# ---------------------------------------------------------------------------

def _web():
    out = {}
    for b in BOOK_NAMES:
        c = 1
        while True:
            path = os.path.join(BIBLES_DIR, "WEB", f"{b.replace(' ', '_')}_{c}.json")
            if not os.path.exists(path):
                break
            for n, t in json.load(open(path, encoding="utf-8"))["verses"]:
                out[(b, c, int(n))] = t
            c += 1
    return out


TEXT_WEB = _web()


def finds(pattern, skip=""):
    """[(book, c, v)] of every WEB verse the pattern finds, in order."""
    pat = re.compile(pattern)
    out = [k for k, t in TEXT_WEB.items() if pat.search(t)]
    gone = {v for r in verse_refs.parse(skip, "Genesis") for v in r.verses()} if skip else set()
    return [k for k in out if k not in gone]


def verses(ref):
    return [v for r in verse_refs.parse(ref, "Genesis") for v in r.verses()] if ref else []


def rows(vs):
    """[(book, c, v)] -> sidecar rows [book index, c, v, 0, 0]."""
    return [[BOOK_NAMES.index(b), c, v, 0, 0] for b, c, v in
            sorted(set(vs), key=lambda x: (BOOK_NAMES.index(x[0]), x[1], x[2]))]


def range_rows(ref):
    """A ref string as its ranges [book index, c1, v1, c2, v2] (0 = none),
    so that a verse inside one finds it only when no place is named."""
    return [[BOOK_NAMES.index(r.book), r.c1, r.v1 or 0, r.c2 or 0, r.v2 or 0]
            for r in verse_refs.parse(ref, "Genesis")]


def shown_rows(rs, most=24):
    """All of a card's verses when there are few; else the first in each book."""
    if len(rs) <= most:
        return rs
    out, seen = [], set()
    for r in rs:
        if r[0] not in seen:
            seen.add(r[0])
            out.append(r)
    return out[:most]


def site_names(s):
    """The words a place goes by in the WEB: its name, its label's names
    (Lod · Lydda) and the other names the WEB uses for it."""
    out = [s.name] + [x.strip() for x in s.label.split("·") if x.strip()]
    out += [a for a in s.aka if in_web(a)]
    return list(dict.fromkeys(out))


def names_pattern(names):
    return r"\b(" + "|".join(re.escape(n) for n in sorted(names, key=len, reverse=True)) + r")\b"


_PLACE_VERSES = {}


def place_verses(s):
    """Every verse that names the place: what its names find, less its
    `skip` (a namesake's, a person's, a word's), with its checked refs."""
    if s not in _PLACE_VERSES:
        gone = set(verses(s.skip))
        found = {v for n in site_names(s) for v in word_verses(n)} - gone
        _PLACE_VERSES[s] = sorted(found | set(verses(s.refs)),
                                  key=lambda x: (BOOK_NAMES.index(x[0]), x[1], x[2]))
    return _PLACE_VERSES[s]


# ---------------------------------------------------------------------------
# Drawing helpers
# ---------------------------------------------------------------------------

def smooth(pts, closed=False):
    """A path through the points, its curve eased at each one (the tangent
    runs from the point before to the point after, each handle a third of
    its own segment, so the curve never loops past a close pair)."""
    n = len(pts)
    if n < 3:
        return "M" + " L".join(f"{_fmt(x)},{_fmt(y)}" for x, y in pts)

    def tangent(i):
        a = pts[(i - 1) % n] if closed or i > 0 else pts[i]
        b = pts[(i + 1) % n] if closed or i < n - 1 else pts[i]
        dx, dy = b[0] - a[0], b[1] - a[1]
        m = math.hypot(dx, dy) or 1
        return dx / m, dy / m

    d = [f"M{_fmt(pts[0][0])},{_fmt(pts[0][1])}"]
    segs = n if closed else n - 1
    for i in range(segs):
        p, q = pts[i], pts[(i + 1) % n]
        L = math.hypot(q[0] - p[0], q[1] - p[1]) / 3
        t0, t1 = tangent(i), tangent((i + 1) % n)
        c0 = (p[0] + t0[0] * L, p[1] + t0[1] * L)
        c1 = (q[0] - t1[0] * L, q[1] - t1[1] * L)
        d.append(f"C{_fmt(c0[0])},{_fmt(c0[1])} {_fmt(c1[0])},{_fmt(c1[1])} "
                 f"{_fmt(q[0])},{_fmt(q[1])}")
    if closed:
        d.append("Z")
    return " ".join(d)


def text(c, xy, s, size, fill, anchor="lm", bold=False, italic=False,
         spacing=0, opacity=1.0):
    """SVG text, with letter spacing where c.text has none."""
    ta = {"l": "start", "m": "middle", "r": "end"}[anchor[0]]
    db = {"a": "text-before-edge", "m": "central",
          "d": "text-after-edge", "s": "alphabetic"}[anchor[1]]
    a = [f'x="{_fmt(xy[0])}"', f'y="{_fmt(xy[1])}"', f'font-size="{_fmt(size)}"',
         f'text-anchor="{ta}"', f'dominant-baseline="{db}"', f'fill="{_rgb(fill)}"']
    if bold:
        a.append('font-weight="bold"')
    if italic:
        a.append('font-style="italic"')
    if spacing:
        a.append(f'letter-spacing="{_fmt(spacing)}"')
    if opacity < 1:
        a.append(f'fill-opacity="{opacity:.2f}"')
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    c._emit(f"<text {' '.join(a)}>{s}</text>")


def box_of(s, size, xy, anchor, bold=False, italic=False, spacing=0):
    """The ink box (x0, y0, x1, y1) of text drawn at xy."""
    x0, y0, x1, y1 = ink(s, size, bold, italic, anchor)
    extra = spacing * (len(s) - 1)
    if anchor[0] == "m":
        x0, x1 = x0 - extra / 2, x1 + extra / 2
    elif anchor[0] == "r":
        x0 -= extra
    else:
        x1 += extra
    return (xy[0] + x0, xy[1] + y0, xy[0] + x1, xy[1] + y1)


def hits(a, b, pad=0):
    return not (a[2] + pad <= b[0] or b[2] + pad <= a[0] or
                a[3] + pad <= b[1] or b[3] + pad <= a[1])


def overlap(a, b):
    w = min(a[2], b[2]) - max(a[0], b[0])
    h = min(a[3], b[3]) - max(a[1], b[1])
    return w * h if w > 0 and h > 0 else 0


# ---------------------------------------------------------------------------
# The places: tiers, glyphs and labels
# ---------------------------------------------------------------------------

def tier(key, s):
    if key in MAJOR:
        return "B"
    if s.kind == "mount" or len(verses(s.refs)) >= 8:
        return "C"
    return "D"


def label_text(key, s):
    if s.label:
        return s.label
    if s.kind == "mount":
        return MOUNT_LABEL.get(s.name, s.name)
    return VALLEY_LABEL.get(key, s.name)


def has_dot(s):
    return s.kind not in ("valley", "plain")


def candidates(x, y, r, fs, dot):
    """Label spots round a dot, nearest first: eight at the dot, then eight
    further out with a leader line."""
    out = []
    if not dot:
        out.append(("mm", x, y, False))
    for i, f in enumerate((1.0, 2.3, 3.8)):
        g = (r + 0.32 * fs) * f
        d = g * 0.72
        for anchor, dx, dy in (("lm", g, 0), ("rm", -g, 0), ("md", 0, -g),
                               ("ma", 0, g), ("ld", d, -d), ("la", d, d),
                               ("rd", -d, -d), ("ra", -d, d)):
            out.append((anchor, x + dx, y + dy, i > 0))
    return out


def place_labels(places, fixed, lands):
    """Greedy: the biggest names first, each at the first spot that touches
    no other name, no dot and nothing fixed; failing that, the spot that
    touches least. The chief cities, shown while the lands' names are,
    keep clear of those too. -> {key: (anchor, x, y, leader, box)}, crowded
    keys."""
    dots = [(p["x"] - p["r"] - 2, p["y"] - p["r"] - 2, p["x"] + p["r"] + 2,
             p["y"] + p["r"] + 2) for p in places if p["dot"]]
    taken = list(fixed)
    out, crowded = {}, []
    order = sorted(places, key=lambda p: (-p["fs"], -p["nref"], p["key"]))
    for p in order:
        if p["tier"] != "B" and lands:
            lands = []                       # the chief cities come first
        avoid = taken + lands
        own = (p["x"] - p["r"] - 2, p["y"] - p["r"] - 2, p["x"] + p["r"] + 2,
               p["y"] + p["r"] + 2)
        best, best_cost = None, None
        for anchor, x, y, leader in candidates(p["x"], p["y"], p["r"], p["fs"], p["dot"]):
            b = box_of(p["text"], p["fs"], (x, y), anchor, p["bold"], p["italic"])
            if b[0] < 8 or b[1] < 8 or b[2] > W - 8 or b[3] > H - 8:
                continue
            cost = sum(overlap(b, t) + 1 for t in avoid if hits(b, t, 3))
            cost += sum(overlap(b, d) + 1 for d in dots if d != own and hits(b, d, 2))
            if best_cost is None or cost < best_cost:
                best, best_cost = (anchor, x, y, leader, b), cost
            if cost == 0:
                break
        if best_cost:
            crowded.append(p["key"])
        out[p["key"]] = best
        taken.append(best[4])
    return out, crowded


def draw_dot(c, x, y, r, certainty, kind):
    if kind == "mount":
        h = r * 2.1
        c.polygon([(x - h * 0.6, y + h * 0.42), (x, y - h * 0.58),
                   (x + h * 0.6, y + h * 0.42)], fill=MOUNT, stroke=BG, width=r * 0.25)
        return
    if certainty == GZ.POSSIBLE:
        c.circle(x, y, r * 0.8, fill=LAND, stroke=DOT, width=r * 0.4)
    else:
        c.circle(x, y, r, fill=DOT, stroke=BG, width=r * 0.2)
        if certainty == GZ.PROBABLE:
            c.circle(x, y, r * 0.42, fill=LAND)


def leader_line(c, p, spot, fs):
    """From the dot's edge toward the label's nearest edge."""
    x0, y0, x1, y1 = spot[4]
    tx_ = min(max(p["x"], x0), x1)
    ty_ = min(max(p["y"], y0), y1)
    dx, dy = tx_ - p["x"], ty_ - p["y"]
    m = math.hypot(dx, dy) or 1
    sx, sy = p["x"] + dx / m * (p["r"] + 2), p["y"] + dy / m * (p["r"] + 2)
    c.line((sx, sy), (tx_ - dx / m * 2, ty_ - dy / m * 2), TEXT_DIM, max(1, fs / 18))


# ---------------------------------------------------------------------------
# The sheet
# ---------------------------------------------------------------------------

MAST = (90, 90, 1760, 470)            # x0, y0, x1, y1: the title block, in the sea
LEGEND = (90, 2930, 1330, 3790)       # the key and the scale, in the sea


def land_ring():
    """The land as one ring: the coast, then out round the sheet's far side."""
    last = GZ.COAST[-1]
    return (GZ.COAST + [(last[0], LON_L - 0.2), (LAT_BOT - 0.2, LON_L - 0.2),
                        (LAT_BOT - 0.2, LON_R + 0.2), (LAT_TOP + 0.3, LON_R + 0.2),
                        (LAT_TOP + 0.3, GZ.COAST[0][1])])


def draw_base(c):
    # a degree grid, every half degree
    with c.group(data={"fs": 30}):
        lat = math.ceil(LAT_BOT * 2) / 2
        while lat <= LAT_TOP:
            y = P(lat, LON_L)[1]
            c.line((0, y), (W, y), GRID, 1.5)
            text(c, (W - 14, y - 8), f"{lat:g}°N", 30, GRID, "rd")
            lat += 0.5
        lon = math.ceil(LON_L * 2) / 2
        while lon <= LON_R:
            x = P(LAT_TOP, lon)[0]
            c.line((x, 0), (x, H), GRID, 1.5)
            text(c, (x + 10, H - 14), f"{lon:g}°E", 30, GRID, "ld")
            lon += 0.5
    c.path(smooth(PROJ.PS(land_ring())), fill=LAND)
    c.path(smooth(PROJ.PS(GZ.COAST)), stroke=COAST_LINE, width=3)
    for key, line in GZ.RIVERS.items():
        c.path(smooth(PROJ.PS(line)), stroke=RIVER,
               width=RIVER_WIDTH.get(key, 3.5), linecap="round")
    for ring in GZ.LAKES.values():
        c.path(smooth(PROJ.PS(ring), closed=True), fill=LAKE, stroke=COAST_LINE,
               width=2.5)


def water_label_boxes():
    out = {}
    for key, (lat, lon, fs, anchor) in WATER_LABELS.items():
        xy = P(lat, lon)
        out[key] = (xy, fs, anchor, box_of(water_text(key), fs, xy, anchor, italic=True))
    return out


def water_text(key):
    """The name as the map writes it: WEB's words, capitalised."""
    if key == "great_sea":
        return "The Great Sea"
    n = GZ.WATERS[key].name
    return n[:1].upper() + n[1:]


def draw_water_names(c, boxes):
    by_fs = {}
    for key, (xy, fs, anchor, _b) in boxes.items():
        by_fs.setdefault(fs, []).append((key, xy, anchor))
    for fs in sorted(by_fs):
        data = {"fs": fs}
        if fs == FS_SEA:
            data["fmax"] = 120
        with c.group(data=data):
            for key, xy, anchor in by_fs[fs]:
                text(c, xy, water_text(key), fs, WATER_TXT, anchor, italic=True)


def region_box(key):
    r = GZ.REGIONS[key]
    fs = REGION_FS.get(key, FS_REGION)
    xy = P(r.lat, r.lon)
    s = r.name.upper()
    return xy, s, fs, box_of(s, fs, xy, "mm", spacing=fs * 0.18)


def draw_regions(c, nt):
    keys = [k for k, r in GZ.REGIONS.items() if r.nt == nt]
    for fs in sorted({REGION_FS.get(k, FS_REGION) for k in keys}):
        with c.group(data={"fs": fs, "fmax": REGION_FADE}):
            for k in keys:
                xy, s, f, _b = region_box(k)
                if f == fs:
                    text(c, xy, s, fs, REGION if not nt else (176, 150, 96), "mm",
                         spacing=fs * 0.18, opacity=0.8)


def draw_masthead(c, n_places):
    with c.group(data={"fs": 130}):
        text(c, (MAST[0] + 20, MAST[1] + 70), TITLE, 130, TEXT, "lm", bold=True)
    with c.group(data={"fs": 56}):
        text(c, (MAST[0] + 24, MAST[1] + 190), "from Dan to Beersheba, and beyond the Jordan",
             56, TEXT_DIM, "lm", italic=True)
    with c.group(data={"fs": 40}):
        text(c, (MAST[0] + 24, MAST[1] + 290),
             f"{n_places} places the WEB names, at the sites they are identified with",
             40, TEXT_DIM, "lm")


def draw_legend(c):
    x0, y0 = LEGEND[0] + 30, LEGEND[1] + 40
    fs = 36
    with c.group(data={"fs": fs}):
        c.rect(LEGEND[0], LEGEND[1], LEGEND[2] - LEGEND[0], LEGEND[3] - LEGEND[1],
               fill=(SEA[0] - 6, SEA[1] - 8, SEA[2] - 10), stroke=SAND_DIM, width=2, rx=18)
        y = y0 + 20
        x = x0 + 20
        for cert, word in ((GZ.KNOWN, "known site"), (GZ.PROBABLE, "probable"),
                           (GZ.POSSIBLE, "possible")):
            draw_dot(c, x, y, 12, cert, "town")
            text(c, (x + 26, y), word, fs, TEXT, "lm")
            x += 70 + ink(word, fs, False, False, "lm")[2]
        y += 70
        draw_dot(c, x0 + 20, y, 13, GZ.KNOWN, "mount")
        text(c, (x0 + 46, y), "mountain", fs, TEXT, "lm")
        y += 70
        text(c, (x0, y), "the coast as today; the lakes", fs, TEXT_DIM, "lm", italic=True)
        y += 48
        text(c, (x0, y), "at their high water", fs, TEXT_DIM, "lm", italic=True)
        # the scale
        y += 100
        km = 50
        c.line((x0, y), (x0 + km * KM, y), SAND, 5)
        for i in range(0, km + 1, 10):
            xx = x0 + i * KM
            c.line((xx, y - 14), (xx, y), SAND, 3)
            text(c, (xx, y + 12), str(i), 30, TEXT_DIM, "ma")
        text(c, (x0 + km * KM + 20, y), "km", 30, TEXT_DIM, "lm")
        y += 90
        mi = 30
        c.line((x0, y), (x0 + mi * 1.609344 * KM, y), SAND, 5)
        for i in range(0, mi + 1, 10):
            xx = x0 + i * 1.609344 * KM
            c.line((xx, y - 14), (xx, y), SAND, 3)
            text(c, (xx, y + 12), str(i), 30, TEXT_DIM, "ma")
        text(c, (x0 + mi * 1.609344 * KM + 20, y), "miles", 30, TEXT_DIM, "lm")
    return y + 110


def draw_layer_legends(c, y):
    x0, fs = LEGEND[0] + 30, 36
    with c.group(data={"layer": "tribes"}):
        with c.group(data={"fs": fs}):
            c.circle(x0 + 20, y, 13, fill=DOT, stroke=BG, width=2)
            c.circle(x0 + 20, y, 21, stroke=RING_LEV, width=3)
            text(c, (x0 + 52, y), "a Levite city", fs, TEXT, "lm")
            c.circle(x0 + 380, y, 13, fill=DOT, stroke=BG, width=2)
            c.circle(x0 + 380, y, 21, stroke=RING_LEV, width=3)
            c.circle(x0 + 380, y, 29, stroke=RING_LEV, width=3)
            text(c, (x0 + 420, y), "a city of refuge", fs, TEXT, "lm")
            text(c, (x0, y + 66), "colour: the towns given to each tribe", fs, TEXT_DIM,
                 "lm", italic=True)
    with c.group(data={"layer": "nt"}):
        with c.group(data={"fs": fs}):
            yy = y + 140
            c.circle(x0 + 20, yy, 13, fill=DOT, stroke=BG, width=2)
            c.circle(x0 + 20, yy, 22, stroke=RING_NT, width=3.5)
            text(c, (x0 + 52, yy), "named in the Gospels or Acts", fs, TEXT, "lm")


def places_of(sites):
    out = []
    for key, s in sites.items():
        t = tier(key, s)
        fs, r = TIERS[t]
        x, y = P(s.lat, s.lon)
        dot = has_dot(s)
        out.append(dict(key=key, site=s, tier=t, fs=fs, r=r if dot else 0,
                        x=x, y=y, dot=dot, text=label_text(key, s),
                        bold=t == "B", italic=not dot or s.kind == "mount",
                        nref=len(verses(s.refs))))
    return out


def tribe_clusters(sites):
    """{tribe: [[keys]]}: a tribe's towns, split where they lie far apart
    (Manasseh either side of the Jordan; Dan's own city in the north)."""
    out = {}
    for k, s in sites.items():
        for t in s.tribe:
            out.setdefault(t, []).append(k)
    clusters = {}
    for t, keys in out.items():
        if t == "Manasseh":
            groups = [[k for k in keys if sites[k].lon < 35.56],
                      [k for k in keys if sites[k].lon >= 35.56]]
        elif t == "Dan":
            groups = [[k for k in keys if sites[k].lat < 32.5],
                      [k for k in keys if sites[k].lat >= 32.5]]
        else:
            groups = [keys]
        clusters[t] = [g for g in groups if g]
    return clusters


def tribe_colour(t, keys, sites):
    if t == "Manasseh":
        return TRIBE_COL["MANASSEH_E" if sites[keys[0]].lon >= 35.56 else "MANASSEH_W"]
    return TRIBE_COL[t.upper()]


def lighten(col, f=0.45):
    return tuple(round(v + (255 - v) * f) for v in col)


def build_svg(sites, places, spots, clusters):
    c = SvgCanvas(W, H, bg=SEA)
    draw_base(c)
    # the tribes' colour, under everything else
    with c.group(data={"layer": "tribes"}):
        for t, groups in clusters.items():
            for keys in groups:
                col = tribe_colour(t, keys, sites)
                c._emit('<g opacity="0.24">')
                for k in keys:
                    x, y = P(sites[k].lat, sites[k].lon)
                    c.circle(x, y, 5.5 * KM, fill=col)
                c._emit("</g>")
        # the tribes' names, under the places' names
        with c.group(data={"fs": TRIBE_FS, "fmax": TRIBE_FADE}):
            for t, groups in clusters.items():
                for keys in groups:
                    if len(keys) < 2:
                        continue
                    x = sum(P(sites[k].lat, sites[k].lon)[0] for k in keys) / len(keys)
                    y = sum(P(sites[k].lat, sites[k].lon)[1] for k in keys) / len(keys)
                    text(c, (x, y), t.upper(), TRIBE_FS, lighten(tribe_colour(t, keys, sites)),
                         "mm", bold=True, italic=True, spacing=8, opacity=0.95)
    wboxes = water_label_boxes()
    draw_water_names(c, wboxes)
    draw_regions(c, nt=False)
    with c.group(data={"layer": "nt"}):
        draw_regions(c, nt=True)
    by_tier = {t: [p for p in places if p["tier"] == t] for t in "DCB"}
    for t in "DCB":
        fs, r = TIERS[t]
        with c.group(data={"fs": fs}):
            for p in by_tier[t]:
                spot = spots[p["key"]]
                if spot[3] and p["dot"]:
                    leader_line(c, p, spot, fs)
                if p["dot"]:
                    draw_dot(c, p["x"], p["y"], p["r"], p["site"].certainty, p["site"].kind)
                text(c, spot[1:3], p["text"], fs, TEXT if t != "B" else (240, 228, 196),
                     spot[0], bold=p["bold"], italic=p["italic"])
    # the tribes' rings and names
    with c.group(data={"layer": "tribes"}):
        for t in "DCB":
            fs, r = TIERS[t]
            with c.group(data={"fs": fs}):
                for p in by_tier[t]:
                    s = p["site"]
                    if not p["dot"] or not (s.levitical or s.refuge):
                        continue
                    w = max(2, r * 0.28)
                    c.circle(p["x"], p["y"], r + w * 2.4, stroke=RING_LEV, width=w)
                    if s.refuge:
                        c.circle(p["x"], p["y"], r + w * 5, stroke=RING_LEV, width=w)
    with c.group(data={"layer": "nt"}):
        for t in "DCB":
            fs, r = TIERS[t]
            with c.group(data={"fs": fs}):
                for p in by_tier[t]:
                    if p["dot"] and nt_named(p["site"]):
                        w = max(2.2, r * 0.3)
                        c.circle(p["x"], p["y"], r + w * 2.6, stroke=RING_NT, width=w)
    draw_masthead(c, len(places))
    y = draw_legend(c)
    draw_layer_legends(c, y)
    return c.tostring().replace(
        "<svg ", f'<svg data-kind="map" data-title="{TITLE}" ', 1)


def nt_named(s):
    """Named in the Gospels or Acts, as the layer's legend says."""
    return any(NT_FIRST <= BOOK_NAMES.index(b) < NT_LAST for b, _c, _v in place_verses(s))


# ---------------------------------------------------------------------------
# The sidecar
# ---------------------------------------------------------------------------

JERUSALEM = (GZ.SITES["jerusalem"].lat, GZ.SITES["jerusalem"].lon)
COMPASS = ["north", "north-east", "east", "south-east", "south", "south-west",
           "west", "north-west"]


def from_jerusalem(lat, lon):
    la1, lo1, la2, lo2 = map(math.radians, (*JERUSALEM, lat, lon))
    d = 2 * 6371 * math.asin(math.sqrt(
        math.sin((la2 - la1) / 2) ** 2 +
        math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2))
    y = math.sin(lo2 - lo1) * math.cos(la2)
    x = math.cos(la1) * math.sin(la2) - math.sin(la1) * math.cos(la2) * math.cos(lo2 - lo1)
    bearing = (math.degrees(math.atan2(y, x)) + 360) % 360
    way = COMPASS[round(bearing / 45) % 8]
    return d, way


def web_names(s):
    """The site's other names that the WEB uses for it: those with a verse
    left once its skips are taken out (Luz for Bethel, but not the other
    Luz's verse)."""
    gone = set(verses(s.skip))
    return [a for a in s.aka if word_verses(a) - gone]


_ALL_WEB = "\n".join(TEXT_WEB.values())
_IN_WEB = {}


def in_web(name):
    """Whether the WEB uses the name anywhere, as a word."""
    if name not in _IN_WEB:
        _IN_WEB[name] = bool(word_verses(name))
    return _IN_WEB[name]


_STARTS = list(itertools.accumulate([0] + [len(v) + 1 for v in TEXT_WEB.values()]))[:-1]
_KEYS = list(TEXT_WEB)
_WORD_VERSES = {}


def _word(ch):
    return ch.isalnum() or ch == "_"


def word_verses(name):
    """The verses that have the name as a word: str.find, then a look either
    side, since a regex word search through the whole Bible is slow."""
    if name not in _WORD_VERSES:
        out, i = set(), _ALL_WEB.find(name)
        while i >= 0:
            j = i + len(name)
            if not (i and _word(_ALL_WEB[i - 1])) and \
                    not (j < len(_ALL_WEB) and _word(_ALL_WEB[j])):
                out.add(_KEYS[bisect.bisect_right(_STARTS, i) - 1])
            i = _ALL_WEB.find(name, i + 1)
        _WORD_VERSES[name] = out
    return _WORD_VERSES[name]


def _bx(b, pad=3):
    return [round(b[0] - pad, 1), round(b[1] - pad, 1),
            round(b[2] - b[0] + 2 * pad, 1), round(b[3] - b[1] + 2 * pad, 1)]


def site_card(key, s, p, spot):
    tribe = ", ".join(s.tribe)
    region = s.region if s.region not in (s.name, label_text(key, s)) else ""
    # a region named for a tribe would read as the place's tribe, which it
    # may not be (Beth Horon stands in Benjamin's hills but was Ephraim's)
    if region in TRIBE_NAMES:
        region = f"tribe of {tribe}" if tribe else f"the land of {region}"
    sub = [{"town": "", "mount": "mountain", "valley": "valley", "plain": "plain",
            "cave": "cave", "well": "well", "spring": "spring", "pool": "pool"}[s.kind], region]
    item = {"id": key.replace("_", "-"), "n": label_text(key, s),
            "s": " · ".join(x for x in sub if x), "a": list(s.aka),
            "dims": [["Identified with", s.modern, s.certainty, []]],
            "fs": p["fs"]}
    every = place_verses(s)
    tx = []
    if s.why:
        tx.append(["Why this site", s.why])
    parts = {x.strip() for x in item["n"].split("·")}
    also = [a for a in web_names(s) if a not in parts]
    if also:
        tx.append(["Also called", ", ".join(also)])
    given = []
    if tribe:
        given.append(f"given to {tribe}")
    if s.refuge:
        given.append("a city of refuge")
    if s.levitical:
        given.append("a Levite city")
    if given:
        tx.append(["In Joshua", "; ".join(given)])
    if key != "jerusalem":
        d, way = from_jerusalem(s.lat, s.lon)
        if d >= 2:
            tx.append(["From Jerusalem", f"{d:.0f} km ({d / 1.609344:.0f} miles) {way}, "
                                          "as the crow flies"])
    if s.namesakes:
        tx.append(["Namesakes", s.namesakes])
    tx.append(["Map point", f"{s.point} (Wikidata {s.qid})" if s.point else f"Wikidata {s.qid}"])
    item["tx"] = tx
    # the card lists every verse when there are few, else the checked ones
    shown = every if len(every) <= 24 else verses(s.refs)
    item["rg"] = [["Named in", rows(shown)]]
    if len(every) > len(shown):
        tx.insert(1 if s.why else 0, ["The WEB names it", f"in {len(every)} verses"])
    item["r"] = rows(every)
    # framed and outlined as one box; tapped on the dot or the name only, so
    # a name set off on a leader doesn't cover a neighbour's dot
    lb = spot[4]
    if p["dot"]:
        r = p["r"]
        dotb = (p["x"] - r, p["y"] - r, p["x"] + r, p["y"] + r)
        u = (min(dotb[0], lb[0]), min(dotb[1], lb[1]), max(dotb[2], lb[2]), max(dotb[3], lb[3]))
        item["b"] = _bx(u)
        item["t"] = [_bx(dotb, 4), _bx(lb, 2)]
    else:
        item["b"] = _bx(lb)
    return item


def inside(x, y, ring):
    """Whether (x, y) is inside the polygon (even-odd)."""
    hit = False
    for (x0, y0), (x1, y1) in zip(ring, ring[1:] + ring[:1]):
        if (y0 > y) != (y1 > y) and x < x0 + (y - y0) * (x1 - x0) / (y1 - y0):
            hit = not hit
    return hit


LAKE_RINGS = [PROJ.PS(r) for r in GZ.LAKES.values()]


def along(pts, step=22, size=28):
    """Hit boxes every `step` px along a line, so a river can be tapped
    anywhere on its course, except where it runs through a lake (the
    Jordan through Huleh), which is the lake's to answer."""
    out = []
    spots = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = max(1, int(math.hypot(x1 - x0, y1 - y0) / step))
        spots += [(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n) for i in range(n)]
    spots.append(pts[-1])
    for x, y in spots:
        if not any(inside(x, y, ring) for ring in LAKE_RINGS):
            out.append([round(x - size / 2, 1), round(y - size / 2, 1), size, size])
    return out


def water_card(key, w, wbox):
    found = rows(finds(w.find, w.skip)) if w.find else []
    item = {"id": "water-" + key.replace("_", "-"), "n": water_text(key),
            "s": "sea" if key == "great_sea" else "lake" if w.lines and w.lines[0] in GZ.LAKES
            else "river", "a": list(w.aka), "r": found}
    # a tap on the line or the lake counts only where no place is under the
    # finger (`lo`): the towns stand on the rivers and lake shores
    lo, bbox = [], None
    for ln in w.lines:
        pts = PROJ.PS(GZ.LAKES.get(ln) or GZ.RIVERS.get(ln))
        xs, ys = zip(*pts)
        bb = (min(xs), min(ys), max(xs), max(ys))
        bbox = bb if bbox is None else (min(bbox[0], bb[0]), min(bbox[1], bb[1]),
                                        max(bbox[2], bb[2]), max(bbox[3], bb[3]))
        lo += [_bx(bb, 0)] if ln in GZ.LAKES else along(pts)
    if lo:
        item["lo"] = lo
    if wbox:
        xy, fs, anchor, b = wbox
        item["b"], item["fs"] = _bx(b), fs
    else:
        # a water the sheet leaves unnamed (Huleh, the Yarmuk): framed by its
        # line, tapped only on it
        item["b"], item["t"] = _bx(bbox, 0), []
    if key == "great_sea":
        item["fx"] = 120
    if w.note:
        item["note"] = w.note
    if found:
        item["rg"] = [["Named in" if len(found) <= 24 else "Named first in each book",
                       shown_rows(found)]]
        if len(found) > 24:
            item["tx"] = [["The WEB names it", f"in {len(found)} verses"]]
    return item


def region_card(key, r):
    xy, s, fs, b = region_box(key)
    found = rows(finds(r.find, r.skip)) if r.find else []
    item = {"id": "land-" + key, "n": r.name, "s": "in Jesus' day" if r.nt else "land",
            "a": list(r.aka), "b": _bx(b), "fs": fs, "fx": REGION_FADE, "r": found}
    if r.nt:
        item["ly"] = "nt"
    if r.note:
        item["note"] = r.note
    if found:
        item["rg"] = [["Named in" if len(found) <= 24 else "Named first in each book",
                       shown_rows(found)]]
        if len(found) > 24:
            item["tx"] = [["The WEB names it", f"in {len(found)} verses"]]
    return item


def sidecar(sites, places, spots, clusters):
    items, index = [], {}
    pl = {p["key"]: p for p in places}
    for key, s in sites.items():
        index[key] = len(items)
        items.append(site_card(key, s, pl[key], spots[key]))
    # namesakes on the map link to each other
    by_name = {}
    for key, s in sites.items():
        by_name.setdefault(s.name, []).append(key)
    for keys in by_name.values():
        for k in keys:
            if len(keys) > 1:
                items[index[k]]["see"] = [index[o] for o in keys if o != k]
    wboxes = water_label_boxes()
    for key, w in GZ.WATERS.items():
        items.append(water_card(key, w, wboxes.get(key)))
    for key, r in GZ.REGIONS.items():
        if r.find or r.note:
            items.append(region_card(key, r))
    for t, groups in clusters.items():
        for gi, keys in enumerate(groups):
            if len(keys) < 2:
                continue
            x = sum(P(sites[k].lat, sites[k].lon)[0] for k in keys) / len(keys)
            y = sum(P(sites[k].lat, sites[k].lon)[1] for k in keys) / len(keys)
            b = box_of(t.upper(), TRIBE_FS, (x, y), "mm", True, True, spacing=8)
            half = ""
            if t == "Manasseh":
                half = "east" if sites[keys[0]].lon >= 35.56 else "west"
            items.append({
                "id": f"tribe-{t.lower()}" + (f"-{half}" if half else ""),
                "n": t + (f" ({half} of the Jordan)" if half else ""), "s": "tribe",
                "ly": "tribes", "b": _bx(b), "fs": TRIBE_FS, "fx": TRIBE_FADE, "a": [t],
                "tx": [["Its towns on the map", ", ".join(sorted(sites[k].name for k in keys))]],
                "note": "The colour gathers the towns Joshua gives the tribe. "
                        "No border is drawn: the text names towns and landmarks, "
                        "not lines.",
                "rg": [["Its land", range_rows(ALLOTMENT[(t + " " + half).strip()])]],
                "r": range_rows(ALLOTMENT[(t + " " + half).strip()])})
    # the verses' books, numbered as the sheet uses them
    used = sorted({r[0] for it in items for r in it.get("r", [])}
                  | {r[0] for it in items for _g, rs in it.get("rg", []) for r in rs})
    remap = {b: i for i, b in enumerate(used)}
    # a water's or land's shown rows are its own `r` rows, so each row is
    # renumbered once
    done = set()
    for it in items:
        lists = [it["r"]] + [rs for _g, rs in it.get("rg", [])] + \
            [d[3] for d in it.get("dims", [])]
        for r in (r for rs in lists for r in rs):
            if id(r) not in done:
                done.add(id(r))
                r[0] = remap[r[0]]
    ids = [it["id"] for it in items]
    assert len(set(ids)) == len(ids), "ids collide"
    return {"version": 1, "card": "parts", "noun": ["place", "places"],
            "chapter": True, "tap": "inside", "books": [BOOK_NAMES[b] for b in used],
            "layers": [{"id": "tribes", "label": "The tribes", "on": False},
                       {"id": "nt", "label": "In Jesus' day", "on": False}],
            "items": items}


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    sites = GZ.SITES
    places = places_of(sites)
    # the lands' names fade before the towns' come in, so only the title,
    # the key and the waters' names are in the towns' way
    fixed = [MAST, LEGEND] + [b for (_xy, _fs, _a, b) in water_label_boxes().values()]
    lands = [region_box(k)[3] for k in GZ.REGIONS]
    spots, crowded = place_labels(places, fixed, lands)
    clusters = tribe_clusters(sites)
    svg = build_svg(sites, places, spots, clusters)
    path = os.path.join(OUT_DIR, STEM + ".svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    data = sidecar(sites, places, spots, clusters)
    dp = os.path.join(OUT_DIR, STEM + ".json")
    with open(dp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    vp = os.path.join(OUT_DIR, STEM + ".html")
    with open(vp, "w", encoding="utf-8") as f:
        f.write(reference_viewer.page(
            STEM, _fmt(W), _fmt(H), TITLE, data=True,
            placeholder="find a place — Bethel, Luz, Capernaum…"))
    print(path)
    print(f"  {W} x {H} px · {os.path.getsize(path) / 1024:.0f} KB · "
          f"{len(places)} places · {len(crowded)} names crowded"
          + (f" ({', '.join(crowded)})" if crowded else ""))
    print(dp)
    print(f"  {len(data['items'])} cards · "
          f"{sum(len(it['r']) for it in data['items'])} verse refs · "
          f"{os.path.getsize(dp) / 1024:.0f} KB")
    print(vp)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
