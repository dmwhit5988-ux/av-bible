"""Render Acts 15-18 (Paul's Second Missionary Journey) as per-verse vector
SVGs.

The first-journey generator could hold one map for eighty verses because the
party kept moving. These four chapters do not: of their 143 verses only about
thirty are travel. The rest are five long stops where the map would sit
frozen — the council at Jerusalem, the night at Philippi, the two synagogues
of Thessalonica and Beroea, the Areopagus, and a year and a half at Corinth.

So the map is the spine, not the whole graphic. It carries every verse that
actually moves, and at each long stop it steps aside and the window gives
that stop its own picture:

    15:1-35   the council            question up, decree down, letter out
    16:13-40  Philippi               four places, one night
    17:2-14   Thessalonica, Beroea   two synagogues, one word, two answers
    17:16-34  the Areopagus          an altar, and the argument built on it
    18:2-17   Corinth                the synagogue and the house next door

Every view shares the same window, the same itinerary panel down the right,
and the same grammar the maps use — what is still ahead is dim and dashed,
what is past is solid, what is happening now traces itself in gold. Text
budget follows the house rule: named parts and numbers, no sentences, and one
word for the verse being read.

Words on the graphic are taken from the WEB text of their own verse (the
app's default translation), since one drawing serves every translation.

Coordinates are approximate and the coastline is a stylised atlas trace.
A few sites are nudged apart where the scale would otherwise merge them
(Neapolis with Philippi, Cenchreae with Corinth); site identifications for
Derbe and Lystra are scholarly reconstructions.

Run inside the project venv:
    .venv\\Scripts\\python.exe generate_acts1518_svg.py
"""

import math
import os

from svg_surface import SvgCanvas
from generate_tabernacle import (W, H, BG, PANEL, SAND, SAND_DIM, TEXT,
                                 TEXT_DIM, HL, RED, out_path)
from generate_tribal_maps import MapFrame, SEA, LAND, WATER_TXT

BOOK = "Acts"

# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

MAP_RECT = (24, 92, 636, 556)            # the window, map or set-piece
MF = MapFrame(31.20, 41.50, 20.60, 37.20, MAP_RECT)
PANEL_X = 648

DASH_UP = "5,6"          # not yet travelled
DASH_SEA = "2,6"         # a travelled sea crossing
DASH_OTHER = "1,5"       # someone else's road (Barnabas, Apollos)

CH_LEN = {15: 41, 16: 40, 17: 34, 18: 28}
_OFFSET, _run = {}, 0
for _ch in (15, 16, 17, 18):
    _OFFSET[_ch] = _run
    _run += CH_LEN[_ch]


def P(ch, v):
    """Reading position — one number across all four chapters."""
    return _OFFSET[ch] + v


def g(alpha):
    return HL + (int(255 * alpha),)


def dim(col, a):
    """The palette colour at `a` opacity."""
    return (col[0], col[1], col[2], int(255 * a))


# ---------------------------------------------------------------------------
# Geography — the Mediterranean and Aegean traced as one sea over a land
# fill, with the islands laid back on top. Simplified from standard atlas
# coastlines; the Aegean keeps only the features the journey needs to read.
# ---------------------------------------------------------------------------

# The Peloponnese is drawn back on top as its own landmass (below), which
# keeps this trace a simple curve instead of a self-touching one.
MED = [
    # the Ionian coast of Epirus, south from the west edge of the frame
    (39.10, 20.60), (38.95, 20.75), (38.85, 20.95), (38.60, 21.10),
    (38.35, 21.15),
    # east along the northern shore of the Gulf of Corinth. The gulf and the
    # Saronic below it are opened a little wider than life: at 45 px to the
    # degree the true straits close to a hairline, and the isthmus Corinth
    # sits on is the point of this part of the map.
    (38.42, 21.50), (38.48, 22.05), (38.52, 22.60), (38.30, 23.00),
    # round the Saronic gulf and out to Sounion
    (38.10, 23.22), (38.05, 23.50), (37.96, 23.62), (37.90, 23.72),
    (37.75, 23.90), (37.65, 24.03),
    # north along Attica and the Euboean gulf into Thessaly
    (37.90, 24.05), (38.10, 24.05), (38.30, 23.90), (38.45, 23.60),
    (38.60, 23.30), (38.80, 23.10), (39.00, 23.10), (39.20, 23.00),
    (39.35, 22.90), (39.25, 23.20), (39.20, 23.35), (39.45, 23.05),
    (39.60, 22.90), (39.90, 22.75), (40.10, 22.65), (40.30, 22.60),
    # the Thermaic gulf, then out along the three fingers of Chalcidice
    (40.45, 22.70), (40.55, 22.85), (40.65, 23.00), (40.50, 23.10),
    (40.30, 23.30), (40.10, 23.45), (40.30, 23.55), (40.20, 23.80),
    (40.35, 23.90), (40.15, 24.15), (40.40, 24.20),
    # the Thracian coast east to the Dardanelles
    (40.60, 24.05), (40.80, 23.90), (40.85, 24.20), (40.90, 24.40),
    (40.85, 24.80), (40.90, 25.20), (40.85, 25.60), (40.80, 26.00),
    (40.60, 26.10),
    # up the strait, round the Sea of Marmara, and back down the far shore
    (40.40, 26.30), (40.30, 26.55), (40.40, 26.90), (40.60, 27.30),
    (40.75, 27.80), (40.85, 28.40), (40.98, 28.95), (40.80, 29.30),
    (40.77, 29.90), (40.72, 29.30), (40.45, 28.90), (40.38, 28.30),
    (40.35, 27.60), (40.40, 27.00), (40.25, 26.70), (40.10, 26.35),
    (40.00, 26.20),
    # the Asian shore of the Aegean, south past Troas, Smyrna and Miletus
    (39.80, 26.10), (39.60, 26.20), (39.50, 26.35), (39.30, 26.55),
    (39.10, 26.70), (38.95, 26.85), (38.80, 26.90), (38.65, 26.75),
    (38.45, 26.55), (38.35, 26.30), (38.40, 26.85), (38.42, 27.15),
    (38.30, 26.90), (38.20, 26.75), (38.05, 26.90), (37.95, 27.20),
    (37.85, 27.05), (37.70, 27.15), (37.55, 27.25), (37.40, 27.25),
    (37.20, 27.35), (37.05, 27.42), (36.95, 27.30), (36.80, 27.40),
    (36.70, 27.70), (36.72, 28.10), (36.80, 28.25), (36.75, 28.60),
    (36.60, 28.90), (36.55, 29.10),
    # the southern coast of Asia Minor — the first journey's own trace
    (36.44, 29.60), (36.49, 30.08), (36.60, 30.40), (36.80, 30.54),
    (36.93, 30.74), (36.82, 30.90), (36.62, 30.98), (36.47, 31.24),
    (36.37, 31.62), (36.24, 32.02), (36.11, 32.42), (36.02, 32.80),
    (36.10, 33.10), (36.24, 33.55), (36.36, 33.98), (36.53, 34.42),
    (36.70, 34.72), (36.80, 35.05), (36.87, 35.55), (36.80, 36.02),
    (36.60, 36.16), (36.48, 35.98), (36.30, 36.02), (36.10, 35.98),
    (35.95, 35.95), (35.75, 35.82), (35.40, 35.78), (35.00, 35.80),
    (34.60, 35.88), (34.20, 35.90),
    # down the Levant to Gaza
    (33.90, 35.48), (33.56, 35.36), (33.27, 35.20), (32.92, 35.07),
    (32.50, 34.89), (32.08, 34.75), (31.80, 34.65), (31.52, 34.47),
    (31.20, 34.30),
    # west along the African shore, up over Cyrenaica, out at the west edge
    (31.10, 30.00), (31.10, 25.00), (31.60, 23.50), (32.20, 22.80),
    (32.85, 22.30), (32.90, 21.80), (32.60, 21.20), (32.30, 20.60),
]

# The Peloponnese, laid back over the sea: its north edge makes the southern
# shore of the Gulf of Corinth, and its neck touches Attica at the isthmus,
# where Corinth and its two ports sit.
PELOPONNESE = [
    (38.05, 21.35), (38.05, 21.60), (38.08, 22.00), (38.02, 22.45),
    (37.96, 22.85), (37.99, 23.04), (37.86, 23.12),          # the isthmus
    (37.75, 23.15), (37.60, 23.15), (37.35, 23.15), (37.10, 23.15),
    (36.80, 23.05), (36.43, 23.20), (36.75, 22.90), (36.60, 22.65),
    (36.40, 22.48), (36.63, 22.25), (36.80, 22.15), (36.75, 21.90),
    (37.05, 21.65), (37.30, 21.55), (37.60, 21.35), (37.85, 21.30),
]

CYPRUS = [
    (34.90, 32.32), (35.05, 32.30), (35.42, 32.60), (35.28, 33.00),
    (35.36, 33.35), (35.42, 33.75), (35.55, 34.24), (35.70, 34.58),
    (35.52, 34.20), (35.28, 34.00), (35.12, 33.90), (34.95, 33.70),
    (34.80, 33.45), (34.62, 33.02), (34.68, 32.62), (34.70, 32.42),
    (34.82, 32.33),
]

ISLANDS = [
    # Crete
    [(35.25, 23.52), (35.42, 23.75), (35.50, 24.10), (35.40, 24.70),
     (35.35, 25.20), (35.42, 25.75), (35.30, 26.30), (35.05, 26.10),
     (34.92, 25.70), (34.98, 25.10), (35.00, 24.60), (35.15, 24.10),
     (35.10, 23.60)],
    # Euboea
    [(38.15, 24.10), (38.45, 23.70), (38.70, 23.30), (38.95, 23.15),
     (39.05, 23.20), (38.85, 23.55), (38.60, 23.90), (38.35, 24.25),
     (38.15, 24.30)],
    # Lesbos
    [(39.38, 26.00), (39.42, 26.35), (39.28, 26.60), (39.05, 26.55),
     (38.98, 26.25), (39.15, 26.05)],
    # Chios
    [(38.60, 25.95), (38.58, 26.15), (38.30, 26.20), (38.22, 26.00),
     (38.40, 25.90)],
    # Samos
    [(37.80, 26.60), (37.82, 27.05), (37.70, 27.05), (37.68, 26.65)],
    # Rhodes
    [(36.45, 28.20), (36.28, 28.25), (36.10, 27.95), (36.20, 27.70)],
    # Thasos
    [(40.78, 24.60), (40.78, 24.78), (40.60, 24.78), (40.60, 24.60)],
    # a handful of Cyclades, for the texture of the Aegean
    [(37.85, 24.90), (37.78, 25.05), (37.68, 24.92), (37.78, 24.80)],
    [(37.20, 25.55), (37.05, 25.60), (37.00, 25.40), (37.15, 25.38)],
    [(36.75, 24.45), (36.68, 24.60), (36.62, 24.42), (36.72, 24.35)],
]

# Samothrace is small enough to vanish at this scale, but the text names it,
# so it is drawn a touch large and carries a waypoint of its own.
SAMOTHRACE_I = [(40.55, 25.38), (40.57, 25.68), (40.40, 25.72), (40.38, 25.40)]

REGIONS = [
    (40.30, 20.90, "MACEDONIA", "lm"),
    (37.60, 22.10, "ACHAIA", "mm"),
    (41.20, 25.90, "THRACE", "mm"),
    (40.60, 30.80, "BITHYNIA", "mm"),
    (38.05, 28.10, "ASIA", "mm"),
    (39.40, 33.20, "GALATIA", "mm"),
    (38.75, 30.40, "PHRYGIA", "mm"),
    (37.15, 34.20, "CILICIA", "mm"),
    (35.10, 36.70, "SYRIA", "mm"),
    (34.88, 33.10, "CYPRUS", "mm"),
    (35.12, 24.60, "CRETE", "mm"),
    (32.10, 35.75, "JUDEA", "mm"),
]
WATERS = [
    (33.60, 26.60, "The Great Sea", "mm"),
    (38.70, 25.05, "Aegean", "mm"),
]

# ---------------------------------------------------------------------------
# Cities  key -> (label, lat, lon, (dx, dy, anchor), major)
# Minor sites are drawn as dots and named only while they are the focus, so
# the crowded Macedonian coast stays readable.
# ---------------------------------------------------------------------------

CITIES = {
    "ANTIOCH":   ("Antioch",      36.20, 36.16, (-10, -3, "rm"), True),
    "JERUSALEM": ("Jerusalem",    31.78, 35.23, (0, 13, "mt"), True),
    "TARSUS":    ("Tarsus",       36.92, 34.63, (0, -11, "mb"), False),
    "DERBE":     ("Derbe",        37.35, 33.35, (8, 8, "lm"), False),
    "LYSTRA":    ("Lystra",       37.58, 32.30, (-8, 6, "rm"), True),
    "ICONIUM":   ("Iconium",      37.87, 32.49, (8, -4, "lm"), False),
    "PIS_ANT":   ("Antioch in Pisidia", 38.30, 31.19, (-8, -2, "rm"), False),
    "MYSIA":     ("Mysia",        39.60, 27.90, (8, 4, "lm"), False),
    "TROAS":     ("Troas",        39.75, 26.16, (-8, -2, "rm"), True),
    "SAMOTHRACE": ("Samothrace",  40.47, 25.53, (0, -11, "mb"), False),
    "NEAPOLIS":  ("Neapolis",     40.86, 24.62, (9, 5, "lm"), False),
    "PHILIPPI":  ("Philippi",     41.01, 24.29, (0, -11, "mb"), True),
    "AMPHIPOLIS": ("Amphipolis",  40.82, 23.84, (0, 12, "mt"), False),
    "APOLLONIA": ("Apollonia",    40.61, 23.44, (0, 12, "mt"), False),
    "THESS":     ("Thessalonica", 40.64, 22.94, (10, 8, "lm"), True),
    "BEREA":     ("Beroea",       40.42, 22.20, (0, 12, "mt"), True),
    "ATHENS":    ("Athens",       37.98, 23.73, (9, -3, "lm"), True),
    "CORINTH":   ("Corinth",      37.88, 22.90, (-9, -2, "rm"), True),
    "CENCHREAE": ("Cenchreae",    37.80, 23.14, (0, 12, "mt"), False),
    "EPHESUS":   ("Ephesus",      37.95, 27.37, (9, 4, "lm"), True),
    "CAESAREA":  ("Caesarea",     32.50, 34.89, (-9, -2, "rm"), True),
    "SALAMIS":   ("Salamis",      35.18, 33.90, (8, 4, "lm"), False),
}


def cpt(key):
    return MF.pt(CITIES[key][1], CITIES[key][2])


# ---------------------------------------------------------------------------
# The twelve stages of the journey — the side panel's rows, and the coarse
# "where are we" that every view (map or set-piece) agrees on.
# key, label, tag, (chapter, verse) it begins at
# ---------------------------------------------------------------------------

STAGES = [
    ("ANTIOCH_A", "Antioch in Syria", "the council",      (15, 1)),
    ("SYR_CIL",   "Syria & Cilicia",  "strengthening",    (15, 41)),
    ("GALATIA",   "Derbe & Lystra",   "Timothy joins",    (16, 1)),
    ("PHRYGIA",   "Phrygia & Galatia", "two doors shut",  (16, 6)),
    ("TROAS",     "Troas",            "the vision",       (16, 8)),
    ("PHILIPPI",  "Philippi",         "into Macedonia",   (16, 11)),
    ("THESS",     "Thessalonica & Beroea", "three Sabbaths", (17, 1)),
    ("ATHENS",    "Athens",           "the Areopagus",    (17, 15)),
    ("CORINTH",   "Corinth",          "eighteen months",  (18, 1)),
    ("EPHESUS",   "Ephesus & the sea", "the voyage home", (18, 18)),
    ("CAESAREA",  "Caesarea & Jerusalem", "the feast",    (18, 22)),
    ("ANTIOCH_B", "Antioch — and out again", "the next road", (18, 23)),
]
SEA_ROWS = {5, 9, 10}    # a sea crossing carries us out of these rows


def stage_row(ch, v):
    p = P(ch, v)
    row = 1
    for i, (_, _, _, (sch, sv)) in enumerate(STAGES, start=1):
        if P(sch, sv) <= p:
            row = i
    return row


# ---------------------------------------------------------------------------
# Journey legs  (from, to, mode, trigger, waypoints)
# ---------------------------------------------------------------------------

# offshore waypoints keep a sea leg over water instead of cutting a headland
AEGEAN_RUN = [(39.20, 25.40), (38.60, 24.60)]          # Beroea's coast to Athens
HOME_RUN = [(37.20, 27.60), (36.10, 29.20), (35.60, 31.60), (35.30, 33.60)]
EPH_TO_CAES = [(36.60, 28.60), (35.20, 32.40), (33.60, 34.60)]

LEGS = [
    ("ANTIOCH", "JERUSALEM", "land", P(15, 3), []),        # up to the council
    ("JERUSALEM", "ANTIOCH", "land", P(15, 30), []),       # the letter carried
    ("ANTIOCH", "TARSUS", "land", P(15, 41), []),
    ("TARSUS", "DERBE", "land", P(16, 1), []),
    ("DERBE", "LYSTRA", "land", P(16, 1), []),
    ("LYSTRA", "PIS_ANT", "land", P(16, 6), [(38.05, 31.80)]),
    ("PIS_ANT", "MYSIA", "land", P(16, 7), [(38.90, 29.60)]),
    ("MYSIA", "TROAS", "land", P(16, 8), []),
    ("TROAS", "SAMOTHRACE", "sea", P(16, 11), []),
    ("SAMOTHRACE", "NEAPOLIS", "sea", P(16, 11), []),
    ("NEAPOLIS", "PHILIPPI", "land", P(16, 12), []),
    ("PHILIPPI", "AMPHIPOLIS", "land", P(17, 1), []),
    ("AMPHIPOLIS", "APOLLONIA", "land", P(17, 1), []),
    ("APOLLONIA", "THESS", "land", P(17, 1), []),
    ("THESS", "BEREA", "land", P(17, 10), []),
    ("BEREA", "ATHENS", "sea", P(17, 15), AEGEAN_RUN),
    ("ATHENS", "CORINTH", "land", P(18, 1), []),
    ("CORINTH", "CENCHREAE", "land", P(18, 18), []),
    ("CENCHREAE", "EPHESUS", "sea", P(18, 19), [(37.40, 25.20)]),
    ("EPHESUS", "CAESAREA", "sea", P(18, 22), EPH_TO_CAES),
    ("CAESAREA", "JERUSALEM", "land", P(18, 22), []),
    ("JERUSALEM", "ANTIOCH", "land", P(18, 22), [(34.20, 36.40)]),
    ("ANTIOCH", "PIS_ANT", "land", P(18, 23), [(37.60, 34.00)]),
]

# Roads that are not Paul's — drawn thinner, dotted, and never in gold.
OTHER_ROADS = [
    ("ANTIOCH", "SALAMIS", P(15, 39), [(35.80, 35.40)], "Barnabas & Mark"),
    ("EPHESUS", "CORINTH", P(18, 27), [(37.30, 25.00)], "Apollos"),
]

# The two doors the Spirit shut, drawn as a road that starts and is barred.
# They point at the region labels already on the map, so they need no words
# of their own.  (from city, toward lat, lon, trigger)
SHUT_DOORS = [
    ("PIS_ANT", 38.05, 28.60, P(16, 6)),
    ("MYSIA", 40.45, 30.30, P(16, 7)),
]


def leg_pts(frm, to, way=()):
    return [cpt(frm)] + [MF.pt(la, lo) for la, lo in way] + [cpt(to)]


# ---------------------------------------------------------------------------
# Per-verse focus on the map.  (chapter, from-verse) -> city key
# Only the verses the map actually shows need an entry; the set-pieces below
# cover the rest.
# ---------------------------------------------------------------------------

FOCUS_RUNS = [
    ((15, 36), "ANTIOCH"), ((15, 41), "TARSUS"),
    ((16, 1), "LYSTRA"), ((16, 6), "PIS_ANT"), ((16, 7), "MYSIA"),
    ((16, 8), "TROAS"), ((16, 11), "NEAPOLIS"), ((16, 12), "PHILIPPI"),
    ((17, 1), "THESS"), ((17, 15), "ATHENS"),
    ((18, 1), "CORINTH"), ((18, 18), "CENCHREAE"), ((18, 19), "EPHESUS"),
    ((18, 22), "ANTIOCH"), ((18, 23), "PIS_ANT"), ((18, 24), "EPHESUS"),
]


def focus_city(ch, v):
    p, key = P(ch, v), "ANTIOCH"
    for (fch, fv), k in FOCUS_RUNS:
        if P(fch, fv) <= p:
            key = k
    return key


# The one word the map's current verse gets, same budget as the set-pieces.
MAP_WORDS = {
    (15, 36): "Let’s return", (15, 37): "Mark", (15, 38): "Withdrew",
    (15, 39): "They parted", (15, 40): "Silas", (15, 41): "Strengthening",
    (16, 1): "Timothy", (16, 2): "Well spoken of", (16, 3): "Circumcised him",
    (16, 4): "The decrees", (16, 5): "Increased daily",
    (16, 6): "Forbidden", (16, 7): "Not allowed", (16, 8): "Troas",
    (16, 9): "Come over", (16, 10): "We sought to go",
    (16, 11): "A straight course", (16, 12): "A Roman colony",
    (17, 1): "Thessalonica", (17, 15): "Athens",
    (18, 1): "Corinth", (18, 18): "A vow", (18, 19): "Ephesus",
    (18, 20): "He declined", (18, 21): "If God wills",
    (18, 22): "Down to Antioch", (18, 23): "In order",
    (18, 24): "Apollos", (18, 25): "Fervent", (18, 26): "More accurately",
    (18, 27): "Over into Achaia", (18, 28): "Powerfully",
}


# ---------------------------------------------------------------------------
# Drawing helpers
# ---------------------------------------------------------------------------

def _len(pts):
    return sum(math.hypot(b[0] - a[0], b[1] - a[1])
               for a, b in zip(pts, pts[1:]))


def point_dir(pts, frac):
    total = _len(pts) or 1.0
    target, run = total * frac, 0.0
    for a, b in zip(pts, pts[1:]):
        seg = math.hypot(b[0] - a[0], b[1] - a[1])
        if run + seg >= target and seg > 0:
            t = (target - run) / seg
            return ((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t),
                    ((b[0] - a[0]) / seg, (b[1] - a[1]) / seg))
        run += seg
    a, b = pts[-2], pts[-1]
    seg = math.hypot(b[0] - a[0], b[1] - a[1]) or 1.0
    return b, ((b[0] - a[0]) / seg, (b[1] - a[1]) / seg)


def arrow(c, pts, color, frac=0.55, size=6):
    (px, py), (ux, uy) = point_dir(pts, frac)
    nx, ny = -uy, ux
    tip = (px + ux * size, py + uy * size)
    back = (px - ux * size * 0.6, py - uy * size * 0.6)
    c.polygon([tip, (back[0] + nx * size * 0.6, back[1] + ny * size * 0.6),
               (back[0] - nx * size * 0.6, back[1] - ny * size * 0.6)],
              fill=color)


def word_label(c, x, y, s, x0lim, x1lim, size=21, col=None, bg=None):
    """The one word this verse gets, on a halo so it stays legible over
    whatever it lands on."""
    w = 0.56 * size * len(s) + 14
    if x - w / 2 < x0lim:
        anch, bx = "lm", x - 7
    elif x + w / 2 > x1lim:
        anch, bx = "rm", x - w + 7
    else:
        anch, bx = "mm", x - w / 2
    c.rect(bx, y - 14, w, 28, fill=bg or PANEL)
    c.text((x, y), s, size, col or HL, anch, bold=True)


# ---------------------------------------------------------------------------
# The map
# ---------------------------------------------------------------------------

def draw_legs(c, ch, v):
    p = P(ch, v)
    current = None
    for frm, to, mode, trig, way in LEGS:
        pts = leg_pts(frm, to, way)
        if trig > p:
            # the road ahead, faint — at this scale the whole remaining
            # circuit drawn brightly would cross the Aegean twice and swamp
            # the leg being read
            c.polyline(pts, stroke=dim(SAND_DIM, 0.5), width=1.2,
                       dash=DASH_UP)
        elif trig < p:
            if mode == "sea":
                c.polyline(pts, stroke=dim(WATER_TXT, 0.95), width=2.2,
                           dash=DASH_SEA)
            else:
                c.polyline(pts, stroke=SAND + (255,), width=2.6)
                arrow(c, pts, SAND, size=5)
        else:
            current = (pts, mode)
    for frm, to, trig, way, _label in OTHER_ROADS:
        if trig <= p:
            c.polyline(leg_pts(frm, to, way), stroke=dim(SAND_DIM, 0.9),
                       width=1.8, dash=DASH_OTHER)
    if current:
        pts, _mode = current
        c.polyline(pts, stroke=SAND_DIM + (255,), width=1, dash=DASH_UP)
        c.traced(pts, stroke=g(0.95), width=3.4, dur="2.4s")


def draw_shut_doors(c, ch, v):
    """The two closed doors of 16:6-7 — an arrow that starts and is barred."""
    p = P(ch, v)
    for frm, la, lo, trig in SHUT_DOORS:
        if trig > p:
            continue
        x0, y0 = cpt(frm)
        x1, y1 = MF.pt(la, lo)
        ux, uy = x1 - x0, y1 - y0
        d = math.hypot(ux, uy) or 1.0
        ux, uy = ux / d, uy / d
        ax, ay = x0 + ux * d, y0 + uy * d
        col = dim(RED, 0.95) if trig == p else dim(RED, 0.55)
        c.line((x0 + ux * 10, y0 + uy * 10), (ax, ay), col, 1.8, dash="4,4")
        nx, ny = -uy, ux
        c.line((ax + nx * 8, ay + ny * 8), (ax - nx * 8, ay - ny * 8),
               col, 2.6)


def draw_cities(c, ch, v):
    p, cur_key = P(ch, v), focus_city(ch, v)
    reached = {"ANTIOCH"}
    for frm, to, _mode, trig, _way in LEGS:
        if trig <= p:
            reached.add(frm)
            reached.add(to)
    for key, (label, la, lo, (dx, dy, anch), major) in CITIES.items():
        x, y = MF.pt(la, lo)
        cur = (key == cur_key)
        if cur:
            c.circle(x, y, 6, fill=HL, stroke=BG, width=1.5)
            c.circle(x, y, 10, stroke=g(0.9), width=1.8)
        elif key in reached:
            c.circle(x, y, 3.4, fill=SAND, stroke=BG, width=1)
        else:
            c.circle(x, y, 3, fill=SEA, stroke=SAND_DIM, width=1.3)
        if cur or (major and key in reached) or (major and key == "ANTIOCH"):
            # push the label clear of the focus ring when this is the lit one
            k = 1.5 if cur else 1.0
            c.text((x + dx * k, y + dy * k), label, 14 if cur else 13,
                   HL if cur else TEXT, anch, bold=cur)


def compass_scale(c):
    x, y = MF.mw - 26, 34
    c.line((x, y + 22), (x, y), TEXT_DIM, 2)
    c.line((x - 5, y + 8), (x, y), TEXT_DIM, 2)
    c.line((x + 5, y + 8), (x, y), TEXT_DIM, 2)
    c.text((x - 10, y + 2), "N", 14, TEXT_DIM, "rm")
    bar = 200 * MF.s / 111.0
    bx, by = MF.mw - 18 - bar, 78
    c.line((bx, by), (bx + bar, by), TEXT_DIM, 2)
    c.line((bx, by - 3), (bx, by + 3), TEXT_DIM, 2)
    c.line((bx + bar, by - 3), (bx + bar, by + 3), TEXT_DIM, 2)
    c.text((bx + bar / 2, by - 6), "200 km", 13, TEXT_DIM, "mb", italic=True)


def draw_map(c, ch, v):
    with c.group(MF.px, MF.py, clip=(MF.mw, MF.mh)):
        c.rect(0, 0, MF.mw, MF.mh, fill=LAND)
        c.polygon(MF.pts(MED), fill=SEA, stroke=SAND_DIM, width=1.6)
        for poly in [PELOPONNESE] + ISLANDS + [CYPRUS, SAMOTHRACE_I]:
            c.polygon(MF.pts(poly), fill=LAND, stroke=SAND_DIM, width=1.2)
        for la, lo, txt, anch in REGIONS:
            c.text(MF.pt(la, lo), txt, 12, TEXT_DIM, anch)
        for la, lo, txt, anch in WATERS:
            c.text(MF.pt(la, lo), txt, 13, WATER_TXT, anch, italic=True)
        draw_legs(c, ch, v)
        draw_shut_doors(c, ch, v)
        draw_cities(c, ch, v)
        compass_scale(c)
    # The word sits in the same corner every time rather than following the
    # lit city — the Macedonian coast is too crowded for a floating label,
    # and a fixed place is one less thing moving per verse.
    word = MAP_WORDS.get((ch, v))
    if word:
        c.text((MF.px + 16, MF.py + MF.mh - 30), word, 21, HL, "lm",
               bold=True)


# ---------------------------------------------------------------------------
# The side panel — the twelve stages, the current one lit
# ---------------------------------------------------------------------------

ROW0, ROWH = 176, 27      # clear of the panel's own heading


def draw_panel(c, ch, v):
    cur_row = stage_row(ch, v)
    c.text((PANEL_X, 108), "PAUL’S SECOND JOURNEY", 19, TEXT, "la", bold=True)
    c.text((PANEL_X, 132), "Acts 15–18  ·  about AD 49–52", 13, TEXT_DIM,
           "la", italic=True)

    dot_x, name_x = PANEL_X + 9, PANEL_X + 26
    top_y = ROW0
    bot_y = ROW0 + (len(STAGES) - 1) * ROWH
    c.line((dot_x, top_y), (dot_x, bot_y), SAND_DIM, 2)

    for i, (_key, label, tag, _at) in enumerate(STAGES, start=1):
        y = ROW0 + (i - 1) * ROWH
        cur = (i == cur_row)
        if i in SEA_ROWS:
            c.line((dot_x, y + 4), (dot_x, y + ROWH - 4),
                   dim(WATER_TXT, 0.95), 2, dash="2,4")
        if cur:
            c.circle(dot_x, y, 6, fill=HL, stroke=BG, width=1)
        else:
            c.circle(dot_x, y, 4, fill=SAND if i < cur_row else SEA,
                     stroke=SAND_DIM, width=1.5)
        c.text((name_x, y - 6), label, 14 if cur else 13,
               HL if cur else TEXT, "lm", bold=cur)
        c.text((name_x, y + 8), tag, 11, TEXT_DIM, "lm", italic=True)


# ---------------------------------------------------------------------------
# The set-pieces — shared furniture
#
# Each one takes over the same window the map uses and works the same way:
# what has happened is solid, what has not is dim, the beat being read is
# gold, and the verse gets exactly one word, always in the same corner.
# ---------------------------------------------------------------------------

WX0, WY0 = MF.px, MF.py
WX1, WY1 = MF.px + MF.mw, MF.py + MF.mh
WCX = (WX0 + WX1) / 2


def stage(c):
    c.rect(WX0, WY0, MF.mw, MF.mh, fill=PANEL)


def verse_word(c, word):
    """The verse's one word, in the corner every view puts it in."""
    if word:
        c.text((WX0 + 16, WY1 - 28), word, 21, HL, "lm", bold=True)


def caps(c, xy, s, anchor="lm"):
    c.text(xy, s, 12, TEXT_DIM, anchor, bold=True)


def beat_list(c, x, y0, dy, rows, v, active=True):
    """A column of beats — (verse, label) — with the one being read lit.
    The workhorse of three of the five set-pieces. With `active` false the
    whole column reads as finished business and nothing in it is lit, which
    is what a city we have already left should look like."""
    cur_i = 0
    for i, (bv, _l) in enumerate(rows):
        if v >= bv:
            cur_i = i
    for i, (bv, label) in enumerate(rows):
        y = y0 + i * dy
        cur = (i == cur_i) and active
        done = (i < cur_i) or (not active and i <= cur_i)
        col = HL if cur else (dim(SAND, 0.9) if done else dim(SAND_DIM, 0.95))
        if cur:
            c.circle(x, y, 6, fill=HL, stroke=PANEL, width=1.5)
            c.pulse_ellipse(x, y, 11, 11, g(0.85), width=1.8, first=(v == bv))
        else:
            c.circle(x, y, 4, fill=col if done else PANEL, stroke=col,
                     width=1.4)
        c.text((x + 20, y), label, 15 if cur else 14,
               HL if cur else (TEXT if done else TEXT_DIM), "lm", bold=cur)
    return cur_i


def bead_rail(c, x0, x1, y, first, last, v):
    """One bead per verse of the episode — the per-verse pulse for the views
    whose drawing only changes at the beats."""
    n = last - first + 1
    step = (x1 - x0) / max(1, n - 1)
    c.line((x0, y), (x1, y), dim(SAND_DIM, 0.8), 1)
    for i in range(n):
        x = x0 + i * step
        if first + i < v:
            c.circle(x, y, 3, fill=dim(SAND, 0.65))
        elif first + i > v:
            c.circle(x, y, 2.6, stroke=dim(SAND_DIM, 0.95), width=1)
    x = x0 + (v - first) * step
    c.circle(x, y, 5.5, fill=HL)
    c.pulse_ellipse(x, y, 11, 11, g(0.85), width=1.6, first=True)
    c.text((x, y + 17), str(v), 11, TEXT_DIM, "mm")


def scroll(c, x, y, col):
    """The unrolled scroll the first-journey sermon uses for a scripture —
    the same mark, so the two graphics agree on what it means."""
    w, lw = 6.2, 1.1
    yt, yb = y - 6.2, y + 6.2

    def p(d):
        c.path(d, stroke=col, width=lw, linecap="round")

    c.line((x - w, yt), (x - w, yb), col, lw)
    c.line((x + w, yt), (x + w, yb), col, lw)
    for dy, f in ((-3.2, 0.66), (0.0, 0.66), (3.2, 0.42)):
        c.line((x - w * 0.66, y + dy), (x - w * 0.66 + 2 * w * f, y + dy),
               col, lw * 0.75)
    p(f"M {x - w:.1f} {yt:.1f} C {x - w:.1f} {yt - 3.7:.1f}, "
      f"{x + w:.1f} {yt - 3.7:.1f}, {x + w:.1f} {yt:.1f}")
    p(f"M {x - w:.1f} {yt:.1f} C {x - w - 2.2:.1f} {yt - 1.4:.1f}, "
      f"{x - w - 1.4:.1f} {yt - 3.4:.1f}, {x - w + 1.6:.1f} {yt - 2.6:.1f}")
    p(f"M {x + w:.1f} {yb:.1f} C {x + w:.1f} {yb + 3.7:.1f}, "
      f"{x - w:.1f} {yb + 3.7:.1f}, {x - w:.1f} {yb:.1f}")
    p(f"M {x + w:.1f} {yb:.1f} C {x + w + 2.2:.1f} {yb + 1.4:.1f}, "
      f"{x + w + 1.4:.1f} {yb + 3.4:.1f}, {x + w - 1.6:.1f} {yb + 2.6:.1f}")


def figure(c, x, y, s, col, lw=1.6):
    """A person, small: head, body, arms, legs."""
    c.circle(x, y - s * 0.42, s * 0.16, stroke=col, width=lw)
    c.line((x, y - s * 0.26), (x, y + s * 0.16), col, lw)
    c.line((x - s * 0.22, y - s * 0.10), (x + s * 0.22, y - s * 0.10), col, lw)
    c.line((x, y + s * 0.16), (x - s * 0.18, y + s * 0.48), col, lw)
    c.line((x, y + s * 0.16), (x + s * 0.18, y + s * 0.48), col, lw)


def building(c, x, y, w, h, col, lw=2.0, door=True, pitched=False):
    """A plain building — the synagogues, the houses, the workshop."""
    c.rect(x, y, w, h, stroke=col, width=lw)
    if pitched:
        c.polyline([(x - 6, y), (x + w / 2, y - h * 0.34), (x + w + 6, y)],
                   col, lw)
    if door:
        dw, dh = w * 0.22, h * 0.42
        c.rect(x + (w - dw) / 2, y + h - dh, dw, dh, stroke=col, width=lw * 0.8)


# ---------------------------------------------------------------------------
# 15:1-35 — the council at Jerusalem
#
# A road with a bar across it. The question is whether the Gentiles may come
# this way at all; the council is argued above it; the bar comes up at the
# judgment, and the letter that lifts it goes out along the road.
# ---------------------------------------------------------------------------

COUNCIL_ROWS = [
    (1,  "Unless circumcised"),
    (5,  "Keep the law of Moses"),
    (7,  "Peter — no distinction"),
    (12, "Signs and wonders"),
    (13, "James — my judgment"),
    (19, "Don’t trouble them"),
]
DECREE = ["Idols", "Blood", "Strangled", "Sexual immorality"]
ROAD_Y, BAR_X = 470, 300


def draw_council(c, v):
    stage(c)
    caps(c, (WX0 + 30, 152), "IN COUNCIL")
    beat_list(c, WX0 + 36, 190, 44, COUNCIL_ROWS, v)

    # the letter, written at the judgment and carried from verse 30
    lx, ly, lw_, lh = 372, 172, 226, 228
    written = v >= 20
    col = HL if v in (20, 28, 29) else (dim(SAND, 0.9) if written
                                        else dim(SAND_DIM, 0.8))
    if written:
        c.rect(lx, ly, lw_, lh, fill=dim(SEA, 0.55), stroke=col, width=2)
        c.polyline([(lx + lw_ - 22, ly), (lx + lw_ - 22, ly + 22),
                    (lx + lw_, ly + 22)], col, 1.6)
        caps(c, (lx + 18, ly + 30), "THE DECREE")
        for i, item in enumerate(DECREE):
            iy = ly + 62 + i * 32
            lit = v >= 29
            ic = HL if lit else dim(SAND, 0.85)
            c.line((lx + 18, iy), (lx + 26, iy + 7), ic, 2)
            c.line((lx + 26, iy + 7), (lx + 38, iy - 8), ic, 2)
            c.text((lx + 48, iy), item, 15, TEXT if not lit else HL, "lm",
                   bold=lit)
    else:
        c.rect(lx, ly, lw_, lh, stroke=dim(SAND_DIM, 0.7), width=1.4,
               rx=2)
        c.text((lx + lw_ / 2, ly + lh / 2), "?", 46, dim(SAND_DIM, 0.95),
               "mm", bold=True)

    # the road, and the bar across it
    c.line((WX0 + 22, ROAD_Y - 13), (WX1 - 22, ROAD_Y - 13),
           dim(SAND_DIM, 0.9), 1.5)
    c.line((WX0 + 22, ROAD_Y + 13), (WX1 - 22, ROAD_Y + 13),
           dim(SAND_DIM, 0.9), 1.5)
    open_road = v >= 28
    for i in range(9):
        rx = WX0 + 40 + i * 62
        if rx > BAR_X - 18 and not open_road:
            break
        c.line((rx, ROAD_Y), (rx + 26, ROAD_Y),
               dim(SAND, 0.7) if rx < BAR_X else dim(HL, 0.65), 2)
    if open_road:
        bar_col = HL if v == 28 else dim(SAND, 0.9)
        c.line((BAR_X, ROAD_Y - 46), (BAR_X, ROAD_Y + 16), bar_col, 3)
        c.line((BAR_X, ROAD_Y - 46), (BAR_X + 54, ROAD_Y - 58), bar_col, 3.5)
    else:
        bar_col = dim(RED, 0.95) if v in (1, 5, 10) else dim(RED, 0.75)
        tilt = 10 if v >= 19 else 0
        c.line((BAR_X - 4 - tilt, ROAD_Y - 34), (BAR_X + 4, ROAD_Y + 22),
               bar_col, 3.5)
        c.line((BAR_X, ROAD_Y + 16), (BAR_X, ROAD_Y + 22), bar_col, 3)
    # Judas and Silas carry the letter along that road, so they travel it
    # rather than standing on it
    if v >= 22:
        far = v >= 30
        base = 528 if far else 340
        col = HL if v in (22, 27, 30) else dim(SAND, 0.9)
        if v == 30:
            c.traced([(352, ROAD_Y - 30), (base - 8, ROAD_Y - 30)],
                     stroke=g(0.8), width=2, dur="1.4s")
        for i, name in enumerate(("Judas", "Silas")):
            fx = base + i * 48
            figure(c, fx, ROAD_Y - 30, 30, col)
            c.text((fx, ROAD_Y - 52), name, 12, TEXT_DIM, "mm")
    if v >= 23:
        c.text((WX1 - 26, ROAD_Y + 34), "Antioch · Syria · Cilicia", 13,
               HL if v >= 30 else TEXT_DIM, "rm", italic=True)


COUNCIL_WORDS = {
    1: "Unless", 2: "Up to Jerusalem", 3: "Great joy", 4: "Received",
    5: "It is necessary", 6: "Gathered", 7: "By my mouth", 8: "He testified",
    9: "No distinction", 10: "A yoke", 11: "Through grace", 12: "Silence",
    13: "James", 14: "A people", 15: "The prophets", 16: "I will return",
    17: "All the Gentiles", 18: "From eternity", 19: "My judgment",
    20: "That we write", 21: "Every Sabbath", 22: "Chosen men",
    23: "Greetings", 24: "No commandment", 25: "One accord",
    26: "Risked their lives", 27: "By word of mouth", 28: "And to us",
    29: "Farewell", 30: "Delivered", 31: "They rejoiced", 32: "Strengthened",
    33: "Sent back", 34: "", 35: "Stayed in Antioch",
}


# ---------------------------------------------------------------------------
# 16:13-40 — Philippi: four places, one night
# ---------------------------------------------------------------------------

PLACES = [
    ("The riverside",   55, 185),
    ("The street",     200, 320),
    ("The marketplace", 335, 455),
    ("The prison",     470, 612),
]
PLACE_AT = [(13, 0), (16, 1), (19, 2), (23, 3), (35, 2), (40, 0)]
BOX_Y, BOX_H = 250, 206


def _place_index(v):
    idx = 0
    for bv, i in PLACE_AT:
        if v >= bv:
            idx = i
    return idx


def em_river(c, x, y, col):
    for i, dy in enumerate((-6, 2, 10)):
        c.path(f"M {x-34} {y+dy} q 11 -7 22 0 q 11 7 22 0 q 11 -7 22 0",
               stroke=col, width=1.8)
    c.polyline([(x - 16, y - 44), (x + 16, y - 44), (x + 10, y - 18),
                (x - 10, y - 18)], col, 2, closed=True)


def em_street(c, x, y, col):
    figure(c, x - 18, y, 46, col)
    figure(c, x + 16, y + 4, 40, dim(col, 0.75))


def em_market(c, x, y, col):
    c.rect(x - 32, y + 8, 64, 16, stroke=col, width=2)
    c.line((x - 24, y + 24), (x - 24, y + 34), col, 1.6)
    c.line((x + 24, y + 24), (x + 24, y + 34), col, 1.6)
    c.line((x - 20, y - 30), (x + 12, y + 2), col, 2)
    c.line((x + 20, y - 30), (x - 12, y + 2), col, 2)


def em_prison(c, x, y, col, opened):
    c.rect(x - 34, y - 40, 68, 78, stroke=col, width=2.2)
    if opened:
        c.polyline([(x + 34, y - 40), (x + 62, y - 28), (x + 62, y + 26),
                    (x + 34, y + 38)], col, 2)
        c.circle(x - 16, y + 52, 5, stroke=col, width=1.6)
        c.circle(x + 2, y + 52, 5, stroke=col, width=1.6)
    else:
        for dx in (-17, 0, 17):
            c.line((x + dx, y - 34), (x + dx, y + 32), col, 1.8)
        c.line((x - 22, y + 52), (x + 22, y + 52), col, 2)
        c.circle(x - 10, y + 52, 5, fill=col)
        c.circle(x + 10, y + 52, 5, fill=col)


def draw_philippi(c, v):
    stage(c)
    caps(c, (WX0 + 30, 148), "ONE NIGHT IN PHILIPPI")
    bead_rail(c, WX0 + 34, WX1 - 34, 186, 13, 40, v)
    cur = _place_index(v)
    for i, (name, x0, x1) in enumerate(PLACES):
        w = x1 - x0
        lit = (i == cur)
        col = HL if lit else dim(SAND_DIM, 0.95)
        seen = any(v >= bv for bv, j in PLACE_AT if j == i)
        if not lit and seen:
            col = dim(SAND, 0.85)
        c.rect(x0, BOX_Y, w, BOX_H, stroke=col, width=2 if lit else 1.3, rx=3)
        if lit:
            c.pulse_rect(x0, BOX_Y, w, BOX_H, g(0.8), width=2, rx=3,
                         first=any(v == bv for bv, j in PLACE_AT if j == i))
        cx, cy = x0 + w / 2, BOX_Y + BOX_H / 2 - 6
        if i == 0:
            em_river(c, cx, cy, col)
        elif i == 1:
            em_street(c, cx, cy, col)
        elif i == 2:
            em_market(c, cx, cy, col)
        else:
            em_prison(c, cx, cy - 6, col, v >= 26)
        c.text((cx, BOX_Y + BOX_H + 20), name, 15 if lit else 14,
               HL if lit else (TEXT if seen else TEXT_DIM), "mm", bold=lit)
    if v >= 26:
        c.text((WX1 - 30, BOX_Y - 16), "midnight — the earthquake", 13,
               HL if v == 26 else TEXT_DIM, "rm", italic=True)


PHILIPPI_WORDS = {
    13: "A riverside", 14: "Lydia", 15: "She persuaded us",
    16: "A spirit", 17: "Servants of God", 18: "Come out of her",
    19: "Their gain gone", 20: "Agitating our city", 21: "Being Romans",
    22: "Beaten with rods", 23: "Into prison", 24: "The stocks",
    25: "Singing hymns", 26: "An earthquake", 27: "His sword",
    28: "We are all here", 29: "Trembling", 30: "What must I do",
    31: "Believe", 32: "The word", 33: "Washed their stripes",
    34: "Set food before them", 35: "Let those men go", 36: "Go in peace",
    37: "We are Romans", 38: "They were afraid", 39: "They begged them",
    40: "Lydia’s house",
}


# ---------------------------------------------------------------------------
# 17:2-14 — Thessalonica and Beroea: one word, two answers
# ---------------------------------------------------------------------------

THESS_ROWS = [
    (2, "Three Sabbaths"), (3, "Had to suffer"), (4, "Some persuaded"),
    (5, "An uproar"), (6, "Upside down"), (7, "Another king"),
    (8, "Troubled"), (9, "Security taken"),
]
BEREA_ROWS = [
    (10, "Away by night"), (11, "More noble"), (12, "Many believed"),
    (13, "They came there too"), (14, "As far as the sea"),
]
COL_L, COL_R = WX0 + 44, WCX + 44


def draw_two_cities(c, v):
    stage(c)
    left_live = v < 10
    for x, name, live in ((COL_L + 74, "THESSALONICA", left_live),
                          (COL_R + 60, "BEROEA", not left_live)):
        col = HL if live else dim(SAND, 0.8)
        building(c, x - 46, 168, 92, 62, col, lw=2.0, pitched=True)
        c.text((x, 252), name, 15, HL if live else TEXT, "mm", bold=live)
    # the scriptures both are measured against, between the two
    scroll(c, WCX, 200, g(0.9) if v in (2, 11) else dim(SAND, 0.85))
    c.text((WCX, 224), "the Scriptures", 12, TEXT_DIM, "mm", italic=True)

    beat_list(c, COL_L, 286, 29, THESS_ROWS, v if v < 10 else 9,
              active=(v < 10))
    if v >= 10:
        beat_list(c, COL_R, 286, 29, BEREA_ROWS, v)
    else:
        for i, (_bv, label) in enumerate(BEREA_ROWS):
            y = 286 + i * 29
            c.circle(COL_R, y, 4, stroke=dim(SAND_DIM, 0.9), width=1.4)
            c.text((COL_R + 20, y), label, 14, TEXT_DIM, "lm")
    # the agitators follow from one city to the other
    if v >= 13:
        col = dim(RED, 0.95) if v == 13 else dim(RED, 0.6)
        c.path(f"M {COL_L + 150} 270 Q {WCX} 250 {COL_R - 14} 300",
               stroke=col, width=2, linecap="round")
        c.polygon([(COL_R - 12, 302), (COL_R - 24, 292), (COL_R - 22, 306)],
                  fill=col)


TWO_CITY_WORDS = {
    2: "Reasoned", 3: "The Christ", 4: "Not a few", 5: "An uproar",
    6: "Upside down", 7: "Another king", 8: "Troubled", 9: "They let them go",
    10: "By night", 11: "Examining daily", 12: "Many believed",
    13: "Agitating", 14: "To the sea",
}


# ---------------------------------------------------------------------------
# 17:16-34 — the Areopagus: a city of idols, one altar, and the argument
# built up from it. The same rising profile the first-journey sermon uses,
# so the two addresses read as the same kind of thing.
# ---------------------------------------------------------------------------

AREO = {
    16: ("Full of idols", 0.05), 17: ("In the marketplace", 0.10),
    18: ("Babbler", 0.15), 19: ("The Areopagus", 0.21),
    20: ("Strange things", 0.26), 21: ("Some new thing", 0.31),
    22: ("Very religious", 0.37), 23: ("An altar", 0.44),
    24: ("Made the world", 0.53), 25: ("Needs nothing", 0.58),
    26: ("One blood", 0.64), 27: ("Seek him", 0.70),
    28: ("His offspring", 0.76), 29: ("Not gold or stone", 0.81),
    30: ("Repent", 0.88), 31: ("A day appointed", 0.95),
}
# each ending gets its own direction off the last step: mocked falls
# away, he goes straight out, the believers rise
BRANCH = {32: ("Some mocked", 46), 33: ("He went out", 0),
          34: ("Dionysius, Damaris", -46)}
AX0, AX1 = WX0 + 52, WX1 - 152
ABASE, ARISE = WY1 - 96, 272
IDOLS = [(96, 214), (168, 176), (262, 200), (352, 168), (438, 196),
         (520, 164), (592, 206), (128, 300), (300, 268), (472, 262),
         (232, 356), (400, 330), (556, 300), (150, 402)]


def anode(v):
    lvl = AREO[v][1]
    return (AX0 + (v - 16) * (AX1 - AX0) / 15, ABASE - lvl * ARISE)


def em_idol(c, x, y, col, s=1.0):
    c.line((x - 6 * s, y + 10 * s), (x + 6 * s, y + 10 * s), col, 1.6)
    c.line((x, y + 10 * s), (x, y - 2 * s), col, 1.6)
    c.circle(x, y - 7 * s, 4.4 * s, stroke=col, width=1.6)


def draw_areopagus(c, v):
    stage(c)
    caps(c, (WX0 + 30, 146), "THE CITY FULL OF IDOLS")
    for ix, iy in IDOLS:
        em_idol(c, ix, iy, dim(SAND_DIM, 0.95 if v > 16 else 0.7), 1.3)

    pts = [anode(i) for i in range(16, 32)]
    c.polyline(pts, stroke=dim(SAND_DIM, 0.75), width=1.4, dash=DASH_UP)
    said = pts[:max(0, min(v, 31) - 16)]
    if len(said) > 1:
        c.polyline(said, stroke=SAND + (255,), width=3)
    if 16 < v <= 31:
        c.traced([anode(v - 1), anode(v)], stroke=g(0.95), width=4,
                 dur="1.2s")

    # the altar sits on the verse that finds it
    ax, ay = anode(23)
    acol = HL if v == 23 else (dim(SAND, 0.9) if v > 23
                               else dim(SAND_DIM, 0.95))
    c.rect(ax - 30, ay - 34, 60, 26, stroke=acol, width=2)
    c.rect(ax - 22, ay - 8, 44, 8, stroke=acol, width=1.6)
    if v >= 23:
        c.text((ax, ay - 44), "TO AN UNKNOWN GOD", 11,
               HL if v == 23 else TEXT_DIM, "mb", bold=(v == 23))

    for i in range(16, 32):
        x, y = anode(i)
        if i == v:
            continue
        if i < v:
            c.circle(x, y, 4, fill=SAND, stroke=PANEL, width=1)
        else:
            c.circle(x, y, 3.5, fill=PANEL, stroke=SAND_DIM, width=1.5)

    # the three ways it ended, branching off the last step
    bx, by = anode(31)
    for bv, (label, dy) in BRANCH.items():
        ex, ey = bx + 72, by + dy
        live, done = (v == bv), (v > bv)
        col = HL if live else (dim(SAND, 0.85) if done
                               else dim(SAND_DIM, 0.9))
        c.line((bx + 8, by), (ex, ey), col, 2.4 if live else 1.5,
               dash=None if (live or done) else DASH_UP)
        c.circle(ex, ey, 5 if live else 3.4,
                 fill=HL if live else (SAND if done else PANEL),
                 stroke=col, width=1.4)
        # labelled above or below its own dot, so a long name has the whole
        # width of the window to sit in instead of running into the panel
        c.text((ex, ey + (-16 if dy < 0 else 18)), label, 14 if live else 13,
               HL if live else (TEXT if done else TEXT_DIM), "mm", bold=live)

    if v <= 31:
        x, y = anode(v)
        c.circle(x, y, 7, fill=HL, stroke=PANEL, width=2)
        c.pulse_ellipse(x, y, 11, 11, g(0.9), width=2, first=True)


AREO_WORDS = {v: w for v, (w, _l) in AREO.items()}
AREO_WORDS.update({32: "Some mocked", 33: "He went out",
                   34: "Certain men believed"})


# ---------------------------------------------------------------------------
# 18:2-17 — Corinth: the synagogue, and the house next door to it
# ---------------------------------------------------------------------------

CORINTH_AT = [(2, 0), (4, 1), (7, 2), (9, 2), (11, 2), (12, 3)]
CB_Y, CB_H = 288, 138
SHOPS = [("The tentmakers", 58, 176), ("The synagogue", 210, 372),
         ("The house of Justus", 372, 492), ("The judgment seat", 516, 596)]


def _corinth_index(v):
    idx = 0
    for bv, i in CORINTH_AT:
        if v >= bv:
            idx = i
    return idx


def draw_corinth(c, v):
    stage(c)
    caps(c, (WX0 + 30, 148), "A YEAR AND SIX MONTHS AT CORINTH")
    bead_rail(c, WX0 + 34, WX1 - 34, 186, 2, 17, v)

    cur = _corinth_index(v)
    for i, (name, x0, x1) in enumerate(SHOPS):
        w = x1 - x0
        lit = (i == cur)
        seen = any(v >= bv for bv, j in CORINTH_AT if j == i)
        col = HL if lit else (dim(SAND, 0.85) if seen
                              else dim(SAND_DIM, 0.95))
        if i == 0:                                   # the workshop, an awning
            c.rect(x0, CB_Y + 24, w, CB_H - 24, stroke=col, width=2)
            c.polyline([(x0 - 8, CB_Y + 24), (x0 + w / 2, CB_Y - 6),
                        (x0 + w + 8, CB_Y + 24)], col, 2)
            for k in range(3):
                c.line((x0 + 18 + k * 28, CB_Y + 52),
                       (x0 + 18 + k * 28, CB_Y + CB_H - 14), col, 1.4)
        elif i == 3:                                 # the bema, on its steps
            c.rect(x0, CB_Y + 44, w, 46, stroke=col, width=2)
            c.rect(x0 + 10, CB_Y + 90, w - 20, 14, stroke=col, width=1.6)
            c.rect(x0 + 20, CB_Y + 104, w - 40, 14, stroke=col, width=1.6)
        else:
            building(c, x0, CB_Y, w, CB_H, col, lw=2.0,
                     pitched=(i == 1))
        c.text((x0 + w / 2, CB_Y + CB_H + 22), name, 15 if lit else 13,
               HL if lit else (TEXT if seen else TEXT_DIM), "mm", bold=lit)
        if lit:
            c.pulse_rect(x0 - 6, CB_Y - 14, w + 12, CB_H + 26, g(0.8),
                         width=2, rx=3,
                         first=any(v == bv for bv, j in CORINTH_AT if j == i))

    # the two buildings share a wall — "next door to the synagogue"
    if v >= 7:
        c.line((372, CB_Y - 6), (372, CB_Y + CB_H + 6),
               HL if v == 7 else dim(SAND, 0.8), 2.5)

    # the night vision over the house — stars and a name for it, not the
    # sentence: the verse is being read aloud as this is on screen
    if v >= 9:
        col = HL if v in (9, 10) else dim(SAND, 0.8)
        for k, (sx, sy) in enumerate(((396, 252), (424, 238), (454, 254),
                                      (478, 240))):
            c.circle(sx, sy, 3.2 if k % 2 else 2.2, fill=col)
        c.text((434, 222), "the night vision", 12, col, "mm", italic=True)

    # eighteen months, ticked off beneath the two buildings they were spent
    # in — above them it would cut through the synagogue roof
    if v >= 11:
        bx0, bx1, by = 210, 492, CB_Y + CB_H + 48
        c.line((bx0, by), (bx1, by), dim(SAND, 0.8), 1.4)
        for k in range(18):
            x = bx0 + k * (bx1 - bx0) / 17
            c.line((x, by - 5), (x, by + 5),
                   HL if v == 11 else dim(SAND, 0.85), 1.6)


CORINTH_WORDS = {
    2: "Aquila and Priscilla", 3: "Tent makers", 4: "Every Sabbath",
    5: "Silas and Timothy", 6: "Your own heads", 7: "Next door",
    8: "Crispus", 9: "Don’t be afraid", 10: "Many people",
    11: "A year and six months", 12: "Gallio", 13: "Contrary to the law",
    14: "About to open his mouth", 15: "Look to it yourselves",
    16: "He drove them", 17: "Sosthenes",
}


# ---------------------------------------------------------------------------
# Which view owns which verses
# (first, last, title, subtitle, draw fn, words)
# ---------------------------------------------------------------------------

BREAKS = [
    ((15, 1), (15, 35), "The Council at Jerusalem",
     "Acts 15:1–35  ·  the question, the judgment, the letter",
     draw_council, COUNCIL_WORDS),
    ((16, 13), (16, 40), "Philippi",
     "Acts 16  ·  a riverside, a street, a market, a prison",
     draw_philippi, PHILIPPI_WORDS),
    ((17, 2), (17, 14), "Thessalonica and Beroea",
     "Acts 17  ·  the same word, two answers",
     draw_two_cities, TWO_CITY_WORDS),
    ((17, 16), (17, 34), "The Areopagus at Athens",
     "Acts 17  ·  an altar, and the argument built on it",
     draw_areopagus, AREO_WORDS),
    ((18, 2), (18, 17), "Corinth",
     "Acts 18  ·  the synagogue and the house next door",
     draw_corinth, CORINTH_WORDS),
]


def break_for(ch, v):
    p = P(ch, v)
    for first, last, title, sub, fn, words in BREAKS:
        if P(*first) <= p <= P(*last):
            return title, sub, fn, words
    return None


# ---------------------------------------------------------------------------
# Assemble one verse
# ---------------------------------------------------------------------------

def render(ch, v):
    c = SvgCanvas(W, H, bg=BG)
    brk = break_for(ch, v)
    if brk:
        title, sub, fn, words = brk
        c.text((28, 24), f"{title} — Acts {ch}", 24, TEXT, "la", bold=True)
        c.text((28, 54), sub, 13, TEXT_DIM, "la", italic=True)
        fn(c, v)
        verse_word(c, words.get(v, ""))
    else:
        c.text((28, 24), f"Paul’s Second Missionary Journey — Acts {ch}",
               24, TEXT, "la", bold=True)
        draw_map(c, ch, v)
    c.rect(MF.px - 1, MF.py - 1, MF.mw + 1, MF.mh + 1, stroke=SAND_DIM,
           width=1)
    draw_panel(c, ch, v)
    return c


def main():
    total = count = 0
    for ch in (15, 16, 17, 18):
        for v in range(1, CH_LEN[ch] + 1):
            out = out_path(BOOK, ch, f"Acts_{ch}_{v}.svg")
            render(ch, v).save(out)
            total += os.path.getsize(out)
            count += 1
    print(f"Acts 15-18: {count} SVG files, {total/1e3:.0f} KB")


if __name__ == "__main__":
    main()
