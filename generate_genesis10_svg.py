"""Render Genesis 10 (the Table of Nations) as per-verse vector SVGs.

The chapter is a genealogy that is also a geography: seventy names in three
lines — Japheth's fourteen, Ham's thirty, Shem's twenty-six — spread over the
known ancient world. So the graphic is both. A map of that world holds the
three lines as broad bands (Japheth north, Ham south and west, Shem east) with
the son-level peoples plotted as dots coloured by line; a side panel carries
the running list — the current father and the names given for him — plus the
per-line tallies that add up to the chapter's seventy.

Where the text drops into a cluster whose members cannot be separately placed
(Mizraim's seven families, Canaan's eleven, Joktan's thirteen, the four cities
in Shinar), the map highlights the *region* and the panel carries the names.
Verse 19's Canaanite border is traced as a line, Sidon down to Gaza and the
cities of the plain. Regions and dots trace themselves in once and then hold,
per the house animation rules.

Placements follow the traditional identifications and are approximate; several
are disputed and a few (Lud in Anatolia, for one) fall outside their own line's
band — the dot colours keep that visible rather than tidying it away.

Run inside the project venv:
    .venv\\Scripts\\python.exe generate_genesis10_svg.py
"""

import os

from svg_surface import SvgCanvas
from generate_tabernacle import (W, H, BG, PANEL, SAND, SAND_DIM, TEXT,
                                 TEXT_DIM, GOLD, HL, out_path)
from generate_tribal_maps import MapFrame, SEA, LAND, WATER_TXT


# one hue per line of Noah's sons
C_JAPHETH = (122, 148, 200)
C_HAM = (196, 132, 92)
C_SHEM = (132, 176, 132)
LINE_COLORS = {"JAPHETH": C_JAPHETH, "HAM": C_HAM, "SHEM": C_SHEM}


def g(alpha):
    return HL + (int(255 * alpha),)


def dim(color, a):
    """`color` with an 0-255 alpha, in the (r, g, b, a) form SvgCanvas takes
    (it turns the fourth element into a fill-/stroke-opacity)."""
    return color + (int(a),)


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

MAP_RECT = (24, 96, 660, 556)
MF = MapFrame(10.0, 48.0, 0.0, 62.0, MAP_RECT)
PANEL_X = 676

# ---------------------------------------------------------------------------
# Water bodies (lat, lon), drawn over the land fill
# ---------------------------------------------------------------------------

# North edge kept south of Greece and of the Anatolian coast, so Javan and
# Tiras sit on land where the traditional identifications put them.
MEDITERRANEAN = [
    (31.0, 0.0), (37.0, 0.0), (37.4, 8.0), (38.4, 12.0), (39.6, 15.5),
    (40.2, 18.0), (38.6, 20.0), (37.2, 22.5), (36.6, 25.0), (36.4, 28.0),
    (36.4, 32.0), (36.2, 35.0), (36.0, 35.8), (33.0, 35.0), (31.4, 34.2),
    (31.0, 30.0), (30.6, 24.0), (30.4, 18.0), (31.0, 10.0), (30.6, 4.0),
]
RED_SEA = [
    (30.0, 32.6), (28.0, 33.6), (24.0, 36.4), (20.0, 38.8), (16.0, 41.0),
    (12.6, 43.4), (12.0, 44.6), (14.2, 43.0), (18.0, 40.4), (22.5, 38.0),
    (27.0, 34.8), (29.6, 33.4),
]
PERSIAN_GULF = [
    (30.4, 47.8), (29.4, 48.4), (27.0, 51.0), (24.6, 53.6), (24.2, 55.4),
    (26.0, 54.4), (28.6, 50.6), (30.2, 48.8),
]
SOUTH_SEA = [
    (10.0, 42.0), (10.0, 62.0), (14.0, 62.0), (13.6, 56.0), (12.4, 50.0),
    (12.0, 45.0), (11.0, 42.0),
]
# (lat, lon, rx_lon, ry_lat) inland seas
BLACK_SEA = (43.4, 34.5, 6.4, 2.3)
CASPIAN = (41.0, 51.0, 2.2, 4.2)

WATERS = [
    (34.4, 18.0, "The Great Sea", "mm"),
    (18.0, 39.5, "Red Sea", "mm"),
    (43.6, 34.5, "Black Sea", "mm"),
    (26.4, 51.6, "Persian Gulf", "mm"),
]

# ---------------------------------------------------------------------------
# The three bands — Japheth north, Ham south and west, Shem east
# ---------------------------------------------------------------------------

BANDS = {
    "JAPHETH": ([(37.0, 0.0), (48.0, 0.0), (48.0, 62.0), (37.0, 62.0)],
                (45.6, 12.0, "JAPHETH")),
    "SHEM":    ([(24.0, 38.0), (37.0, 38.0), (37.0, 62.0), (24.0, 62.0)],
                (33.0, 55.0, "SHEM")),
    "HAM":     ([(10.0, 0.0), (37.0, 0.0), (37.0, 38.0), (10.0, 38.0)],
                (13.0, 8.0, "HAM")),
}

# ---------------------------------------------------------------------------
# Son-level anchors:  key -> (label, lat, lon, (dx, dy, anchor), line, verse)
# ---------------------------------------------------------------------------

ANCHORS = {
    "Gomer":      (44.8, 30.0, (0, -11, "mb"), "JAPHETH", 2),
    "Magog":      (45.2, 44.0, (0, -11, "mb"), "JAPHETH", 2),
    "Madai":      (37.8, 50.0, (9, 3, "lm"), "JAPHETH", 2),
    "Javan":      (38.6, 22.0, (-9, 2, "rm"), "JAPHETH", 2),
    "Tubal":      (39.4, 38.5, (9, 2, "lm"), "JAPHETH", 2),
    "Meshech":    (39.6, 34.5, (-2, 12, "mt"), "JAPHETH", 2),
    "Tiras":      (40.8, 26.5, (-9, -2, "rm"), "JAPHETH", 2),
    "Cush":       (19.0, 33.0, (0, 12, "mt"), "HAM", 6),
    "Mizraim":    (27.2, 30.4, (-9, 2, "rm"), "HAM", 6),
    "Put":        (30.2, 19.0, (0, 12, "mt"), "HAM", 6),
    "Canaan":     (32.4, 35.4, (10, -4, "lm"), "HAM", 6),
    "Elam":       (32.0, 49.0, (9, 4, "lm"), "SHEM", 22),
    "Asshur":     (35.4, 43.4, (-9, 2, "rm"), "SHEM", 22),
    "Arpachshad": (34.6, 45.6, (9, 6, "lm"), "SHEM", 22),
    "Lud":        (38.6, 28.6, (0, -11, "mb"), "SHEM", 22),
    "Aram":       (34.6, 38.6, (-9, -4, "rm"), "SHEM", 22),
}

# Two cities famous enough to name on the map; the rest stay in the panel.
CITIES = {
    "Babel":   (32.5, 44.4, (8, 6, "lm"), 10),
    "Nineveh": (36.35, 43.15, (8, 4, "lm"), 11),
}

# ---------------------------------------------------------------------------
# Regions a verse highlights.  key -> (lat, lon, rx_lon, ry_lat, label, line)
# ---------------------------------------------------------------------------

REGIONS = {
    "GOMER":     (42.0, 38.0, 10.0, 3.4, "Gomer’s sons", "JAPHETH"),
    "JAVAN":     (36.8, 24.0, 9.0, 2.8, "Javan’s sons — the isles", "JAPHETH"),
    "ISLES":     (36.8, 20.0, 13.0, 3.4, "the isles of the nations", "JAPHETH"),
    "CUSH_SONS": (16.5, 44.0, 7.0, 4.6, "Cush’s sons", "HAM"),
    "SHINAR":    (32.2, 45.0, 3.0, 2.0, "the land of Shinar", "HAM"),
    "ASSYRIA":   (36.0, 43.4, 2.6, 1.9, "Assyria", "HAM"),
    "MIZRAIM":   (27.0, 30.6, 2.8, 4.0, "Mizraim’s families", "HAM"),
    "CANAAN_F":  (33.0, 35.7, 1.5, 3.0, "Canaan’s families", "HAM"),
    "ARAM":      (34.6, 38.8, 3.0, 2.0, "Aram’s sons", "SHEM"),
    "JOKTAN":    (16.5, 47.0, 6.0, 4.2, "Joktan’s sons", "SHEM"),
}

# The Canaanite border of verse 19 (lat, lon) with the labelled ends.
BORDER = [(33.56, 35.38), (32.5, 34.9), (31.52, 34.47), (31.2, 35.4),
          (30.8, 35.6)]
BORDER_LABELS = [(0, "Sidon", (-9, -2, "rm")), (2, "Gaza", (-9, 6, "rm")),
                 (3, "the cities of the plain", (9, 0, "lm")),
                 (4, "Lasha", (0, 12, "mt"))]

# ---------------------------------------------------------------------------
# Per verse:  (father, [names], region key, note)
# ---------------------------------------------------------------------------

VERSES = {
    1: ("Noah", ["Shem", "Ham", "Japheth"], None,
        "sons were born to them after the flood"),
    2: ("Japheth", ["Gomer", "Magog", "Madai", "Javan", "Tubal", "Meshech",
                    "Tiras"], "JAPHETH", None),
    3: ("Gomer", ["Ashkenaz", "Riphath", "Togarmah"], "GOMER", None),
    4: ("Javan", ["Elishah", "Tarshish", "Kittim", "Dodanim"], "JAVAN", None),
    5: (None, [], "ISLES",
        "divided in their lands, each after his language"),
    6: ("Ham", ["Cush", "Mizraim", "Put", "Canaan"], "HAM", None),
    7: ("Cush", ["Seba", "Havilah", "Sabtah", "Raamah", "Sabteca"],
        "CUSH_SONS", "Raamah’s sons: Sheba and Dedan"),
    8: ("Cush", ["Nimrod"], "SHINAR", "he began to be a mighty one in the earth"),
    9: (None, [], "SHINAR", "“like Nimrod, a mighty hunter before Yahweh”"),
    10: ("Nimrod’s kingdom", ["Babel", "Erech", "Accad", "Calneh"], "SHINAR",
         "in the land of Shinar"),
    11: ("out into Assyria", ["Nineveh", "Rehoboth Ir", "Calah"], "ASSYRIA",
         None),
    12: ("and", ["Resen"], "ASSYRIA", "between Nineveh and the great city Calah"),
    13: ("Mizraim", ["Ludim", "Anamim", "Lehabim", "Naphtuhim"], "MIZRAIM",
         None),
    14: ("Mizraim", ["Pathrusim", "Casluhim", "Caphtorim"], "MIZRAIM",
         "the Philistines descended from Casluhim"),
    15: ("Canaan", ["Sidon", "Heth"], "CANAAN_F", "Sidon his firstborn"),
    16: ("Canaan", ["the Jebusites", "the Amorites", "the Girgashites"],
         "CANAAN_F", None),
    17: ("Canaan", ["the Hivites", "the Arkites", "the Sinites"], "CANAAN_F",
         None),
    18: ("Canaan", ["the Arvadites", "the Zemarites", "the Hamathites"],
         "CANAAN_F", "afterward the families were spread abroad"),
    19: ("the border", ["Sidon", "Gerar", "Gaza", "Sodom", "Gomorrah",
                        "Admah", "Zeboiim", "Lasha"], "BORDER", None),
    20: (None, [], "HAM",
         "these are the sons of Ham — families, languages, lands, nations"),
    21: ("Shem", [], "SHEM",
         "the father of all the children of Eber, Japheth’s elder brother"),
    22: ("Shem", ["Elam", "Asshur", "Arpachshad", "Lud", "Aram"], "SHEM",
         None),
    23: ("Aram", ["Uz", "Hul", "Gether", "Mash"], "ARAM", None),
    24: ("Arpachshad", ["Shelah", "Eber"], "SHEM",
         "Shelah became the father of Eber"),
    25: ("Eber", ["Peleg", "Joktan"], "SHEM",
         "in Peleg’s days the earth was divided"),
    26: ("Joktan", ["Almodad", "Sheleph", "Hazarmaveth", "Jerah"], "JOKTAN",
         None),
    27: ("Joktan", ["Hadoram", "Uzal", "Diklah"], "JOKTAN", None),
    28: ("Joktan", ["Obal", "Abimael", "Sheba"], "JOKTAN", None),
    29: ("Joktan", ["Ophir", "Havilah", "Jobab"], "JOKTAN",
         "all these were the sons of Joktan"),
    30: (None, [], "JOKTAN",
         "from Mesha toward Sephar, the mountain of the east"),
    31: (None, [], "SHEM",
         "these are the sons of Shem — families, languages, lands, nations"),
    32: (None, [], None,
         "the nations divided from these in the earth after the flood"),
}

# Which line the verse belongs to (None = all three)
def line_of(v):
    if 2 <= v <= 5:
        return "JAPHETH"
    if 6 <= v <= 20:
        return "HAM"
    if 21 <= v <= 31:
        return "SHEM"
    return None


LINE_ROWS = [("JAPHETH", "Japheth", 14, "the north and the isles"),
             ("HAM", "Ham", 30, "Egypt, Cush, Canaan, Shinar"),
             ("SHEM", "Shem", 26, "Elam, Asshur, Aram, Arabia")]


# ---------------------------------------------------------------------------
# Map drawing (all inside the MapFrame group, so coordinates are map-local)
# ---------------------------------------------------------------------------

def ell(c, spec, fill=None, stroke=None, width=1.5):
    lat, lon, rx, ry = spec
    cx, cy = MF.pt(lat, lon)
    c.ellipse(cx, cy, rx * MF.eff * MF.s, ry * MF.s, fill=fill, stroke=stroke,
              width=width)


def draw_bands(c, v):
    active = line_of(v)
    for key, (poly, (llat, llon, label)) in BANDS.items():
        col = LINE_COLORS[key]
        live = (active == key) or active is None
        c.polygon(MF.pts(poly), fill=dim(col, 26 if live else 12),
                  stroke=dim(col, 130 if live else 60), width=1.5)
        c.text(MF.pt(llat, llon), label, 17,
               dim(col, 235) if live else dim(col, 110), "lm", bold=True)


def draw_water(c):
    for poly in (MEDITERRANEAN, RED_SEA, PERSIAN_GULF, SOUTH_SEA):
        c.polygon(MF.pts(poly), fill=SEA, stroke=dim(WATER_TXT, 120),
                  width=1.2)
    for spec in (BLACK_SEA, CASPIAN):
        ell(c, spec, fill=SEA, stroke=dim(WATER_TXT, 120), width=1.2)
    for lat, lon, txt, anch in WATERS:
        c.text(MF.pt(lat, lon), txt, 12, WATER_TXT, anch, italic=True)


def draw_region(c, v):
    """The region this verse's cluster belongs to: a translucent zone whose
    outline brightens when the region changes. A cluster can hold for several
    verses (Canaan's families run 15-18, Joktan's 26-30), and re-drawing the
    ring on each of them is a distraction, so the pulse fires only on the
    verse the region becomes current."""
    _f, _n, key, _note = VERSES[v]
    if key is None or key == "BORDER" or key in BANDS:
        return
    prev = VERSES.get(v - 1, (None, None, None, None))[2]
    lat, lon, rx, ry, label, line = REGIONS[key]
    col = LINE_COLORS[line]
    cx, cy = MF.pt(lat, lon)
    rxp, ryp = rx * MF.eff * MF.s, ry * MF.s
    c.ellipse(cx, cy, rxp, ryp, fill=dim(col, 60))
    c.pulse_ellipse(cx, cy, rxp, ryp, g(0.85), width=2.5,
                    first=(key != prev))
    c.text((cx, cy - ryp - 8), label, 14, HL, "mb", bold=True)


def draw_border(c, v):
    if v != 19:
        return
    pts = MF.pts(BORDER)
    c.traced(pts, stroke=g(0.95), width=3.5, dur="2.4s")
    for i, label, (dx, dy, anch) in BORDER_LABELS:
        x, y = pts[i]
        c.circle(x, y, 5, fill=HL, stroke=BG, width=1.5)
        c.text((x + dx, y + dy), label, 13, HL, anch, bold=True)


def draw_anchors(c, v):
    active = line_of(v)
    names_here = set(VERSES[v][1])
    for label, (lat, lon, (dx, dy, anch), line, verse) in ANCHORS.items():
        if v < verse:
            continue
        col = LINE_COLORS[line]
        cur = label in names_here
        x, y = MF.pt(lat, lon)
        if cur:
            c.circle(x, y, 6, fill=HL, stroke=BG, width=1.5)
            c.circle(x, y, 10.5, stroke=g(0.9), width=2)
        else:
            c.circle(x, y, 4, fill=col if line == active else dim(col, 150),
                     stroke=BG, width=1)
        fill = HL if cur else (TEXT if line == active else TEXT_DIM)
        c.text((x + dx, y + dy), label, 14 if cur else 12.5, fill, anch,
               bold=cur)
    for label, (lat, lon, (dx, dy, anch), verse) in CITIES.items():
        if v < verse:
            continue
        cur = label in names_here
        x, y = MF.pt(lat, lon)
        c.rect(x - 3.5, y - 3.5, 7, 7, fill=HL if cur else dim(C_HAM, 190),
               stroke=BG, width=1)
        c.text((x + dx, y + dy), label, 13 if cur else 12,
               HL if cur else TEXT_DIM, anch, bold=cur, italic=not cur)


def compass_scale(c):
    x, y = MF.mw - 30, 34
    c.line((x, y + 22), (x, y), TEXT_DIM, 2)
    c.line((x - 5, y + 8), (x, y), TEXT_DIM, 2)
    c.line((x + 5, y + 8), (x, y), TEXT_DIM, 2)
    c.text((x - 10, y + 4), "N", 13, TEXT_DIM, "rm")
    bar = 500 * MF.s / 111.0
    bx, by = MF.mw - 20 - bar, MF.mh - 16
    c.line((bx, by), (bx + bar, by), TEXT_DIM, 2)
    c.line((bx, by - 3), (bx, by + 3), TEXT_DIM, 2)
    c.line((bx + bar, by - 3), (bx + bar, by + 3), TEXT_DIM, 2)
    c.text((bx + bar / 2, by - 6), "500 km", 12, TEXT_DIM, "mb", italic=True)


# ---------------------------------------------------------------------------
# Side panel: the three lines, then the current father and his names
# ---------------------------------------------------------------------------

def draw_panel(c, v):
    active = line_of(v)
    father, names, _key, note = VERSES[v]

    c.text((PANEL_X, 92), "THE TABLE OF NATIONS", 19, TEXT, "la", bold=True)

    y = 142
    for key, label, count, blurb in LINE_ROWS:
        live = (active == key) or active is None
        col = LINE_COLORS[key]
        c.rect(PANEL_X, y, W - PANEL_X - 16, 42,
               fill=PANEL if live else BG,
               stroke=dim(col, 220) if live else SAND_DIM, width=1.5, rx=4)
        c.rect(PANEL_X, y, 5, 42, fill=col, rx=2)
        c.text((PANEL_X + 14, y + 15), label, 16,
               HL if live else TEXT_DIM, "lm", bold=live)
        c.text((W - 26, y + 15), f"{count}", 16,
               dim(col, 240) if live else TEXT_DIM, "rm", bold=True)
        y += 50

    # the current group
    cy = y + 12
    c.line((PANEL_X, cy), (W - 16, cy), SAND_DIM, 1)
    cy += 22
    if father:
        c.text((PANEL_X, cy), father, 18, GOLD, "la", bold=True)
        c.text((PANEL_X + 4, cy + 24), "→", 14, TEXT_DIM, "la")
        cy += 24
    else:
        c.text((PANEL_X, cy), "…", 18, GOLD, "la", bold=True)
        cy += 24

    col_x = (PANEL_X + 24, PANEL_X + 172)
    for i, name in enumerate(names):
        x = col_x[i // 7]
        ny = cy + (i % 7) * 21
        c.circle(x - 10, ny, 2.6, fill=GOLD)
        c.text((x, ny), name, 14, HL, "lm")
    if names:
        cy += (min(len(names), 7)) * 21 + 6




def _wrap(text, width):
    out, line = [], ""
    for word in text.split():
        if len(line) + len(word) + 1 > width:
            out.append(line)
            line = word
        else:
            line = f"{line} {word}".strip()
    if line:
        out.append(line)
    return out


# ---------------------------------------------------------------------------
# Assemble one verse
# ---------------------------------------------------------------------------

def render(v):
    c = SvgCanvas(W, H, bg=BG)
    c.text((28, 24), "Genesis 10 · The Table of Nations", 22, TEXT, "la",
           bold=True)

    with c.group(MF.px, MF.py, clip=(MF.mw, MF.mh)):
        c.rect(0, 0, MF.mw, MF.mh, fill=LAND)
        draw_bands(c, v)
        draw_water(c)
        draw_region(c, v)
        draw_anchors(c, v)
        draw_border(c, v)
        compass_scale(c)
    c.rect(MF.px - 1, MF.py - 1, MF.mw + 1, MF.mh + 1, stroke=SAND_DIM,
           width=1)

    draw_panel(c, v)
    return c


def main():
    total = count = 0
    for v in range(1, 33):
        c = render(v)
        out = out_path("Genesis", 10, f"Genesis_10_{v}.svg")
        c.save(out)
        total += os.path.getsize(out)
        count += 1
    print(f"Genesis 10: {count} SVG files, {total/1e3:.0f} KB")


if __name__ == "__main__":
    main()
