"""Generate per-verse map animations for Numbers 32 and Numbers 34.

Three map visualizations, one animated WebP per verse into visuals/:

* Numbers 34:1-15  — a wide "Greater Canaan" map. The border of the land is
  traced segment by segment as the verses describe it (south, west = the
  Great Sea, north, east), with landmark dots appearing as they are named
  and a side panel giving the modern scholarly identification of each
  (Kadesh-barnea = Ein el-Qudeirat, Brook of Egypt = Wadi el-Arish,
  Lebo-hamath = Labweh, Zedad = Sadad ...). The northern reach follows the
  mainstream view (Mazar, Aharoni) that these borders preserve Egypt's
  Late Bronze Age province of Canaan.

* Numbers 34:16-29 — a zoomed twelve-tribe allotment map (the territories
  as later described in Joshua 13-19); as each tribal prince is named
  (vv 19-28) his tribe's territory lights up.

* Numbers 32 (all 42 verses) — a Transjordan map: the lands of Jazer and
  Gilead, the kingdoms of Sihon and Og, and the cities Gad and Reuben
  rebuilt, highlighted verse by verse.

All coordinates are approximate scholarly reconstructions — the ancient
landmarks are only partly identifiable, and every frame says so in the
footer. Geometry is hand-encoded lat/lon simplified from standard Bible
atlas reconstructions. Label positions are hand-tuned; if you move a dot,
re-extract the affected verse's final frame and check for collisions.

Follows the house animation rules: text fully opaque in every frame, the
animation plays ONCE and holds (loop=1), <=24 frames, no pulsing.

Run inside the project venv:  .venv\\Scripts\\python.exe generate_tribal_maps.py
"""

import math
import os

from PIL import Image, ImageDraw

from generate_tabernacle import (W, H, BG, PANEL, SAND, SAND_DIM, TEXT,
                                 TEXT_DIM, HL, F_TITLE, F_LABEL, F_SMALL,
                                 F_DIM, F_VERSE, font, ease, g, dashed_line,
                                 out_path)

G_FRAMES = 24
G_FRAME_MS = 120

SEA = (24, 36, 54)             # water fill
LAND = (34, 35, 29)            # land fill
RIVER = (78, 112, 148)
RIVER_DIM = (52, 72, 94)
WATER_TXT = (110, 132, 158)

F_MAP = font(14)               # map labels — upright (small italics blur)
F_MAP_B = font(14, bold=True)
F_WATER = font(14, italic=True)
F_TRIBE = font(14, bold=True)
F_BIG = font(30, bold=True)

# Muted per-tribe fills (drawn at low alpha over LAND)
TRIBE_COL = {
    "JUDAH": (176, 112, 88), "SIMEON": (150, 140, 82),
    "BENJAMIN": (116, 148, 172), "DAN": (176, 152, 92),
    "EPHRAIM": (108, 160, 118), "MANASSEH_W": (92, 142, 152),
    "ISSACHAR": (162, 118, 150), "ZEBULUN": (128, 128, 182),
    "ASHER": (98, 162, 158), "NAPHTALI": (152, 162, 98),
    "REUBEN": (150, 116, 84), "GAD": (112, 146, 108),
    "MANASSEH_E": (92, 142, 152),
}

# ---------------------------------------------------------------------------
# Geometry (lat, lon) — approximate, simplified from atlas reconstructions
# ---------------------------------------------------------------------------

COAST = [(30.95, 33.35), (31.05, 33.55), (31.16, 33.80), (31.29, 34.23),
         (31.52, 34.43), (31.67, 34.55), (31.80, 34.63), (32.05, 34.74),
         (32.28, 34.83), (32.50, 34.89), (32.62, 34.92), (32.83, 34.96),
         (32.79, 35.03), (32.92, 35.07), (33.04, 35.10), (33.09, 35.11),
         (33.27, 35.19), (33.45, 35.29), (33.56, 35.37), (33.90, 35.48),
         (34.12, 35.65), (34.30, 35.73), (34.45, 35.85), (34.70, 35.97),
         (34.95, 36.05), (35.20, 36.10)]

# Land = everything east/south of the coastline (generous outer corners;
# the map image clips whatever falls outside its own bounding box).
LAND_POLY = COAST + [(35.4, 38.4), (29.2, 38.4), (29.2, 33.0)]

DEAD_SEA = [(31.77, 35.50), (31.76, 35.56), (31.60, 35.58), (31.45, 35.57),
            (31.25, 35.56), (31.10, 35.52), (31.03, 35.46), (31.12, 35.42),
            (31.30, 35.41), (31.50, 35.40), (31.65, 35.43), (31.72, 35.46)]
GALILEE = [(32.90, 35.58), (32.86, 35.63), (32.78, 35.64), (32.71, 35.60),
           (32.70, 35.56), (32.76, 35.52), (32.85, 35.53)]
HULEH = [(33.10, 35.59), (33.06, 35.62), (33.02, 35.60), (33.05, 35.57)]
LAKES = (DEAD_SEA, GALILEE, HULEH)

JORDAN_UP = [(33.25, 35.63), (33.10, 35.60), (32.90, 35.58)]
JORDAN_LOW = [(32.70, 35.57), (32.55, 35.55), (32.40, 35.56), (32.25, 35.54),
              (32.10, 35.54), (31.95, 35.52), (31.77, 35.51)]
ARNON = [(31.47, 35.57), (31.44, 35.80), (31.47, 36.05), (31.40, 36.25)]
JABBOK = [(32.19, 35.56), (32.17, 35.72), (32.08, 35.88), (31.99, 35.98),
          (32.05, 36.08)]
YARMOUK = [(32.68, 35.57), (32.71, 35.75), (32.76, 35.95), (32.73, 36.15)]

# --- Numbers 34 border, one entry per border verse, in reading order ------
BORDER_SEGS = [
    (3, [(31.03, 35.46), (30.90, 35.15)]),                    # Salt Sea->Akrabbim
    (4, [(30.90, 35.15), (30.78, 34.90), (30.63, 34.42),      # ->Zin->Kadesh
         (30.70, 34.32), (30.85, 34.20)]),                    # ->Hazar-addar->Azmon
    (5, [(30.85, 34.20), (30.95, 34.00), (31.16, 33.80)]),    # ->Brook of Egypt->sea
    (6, [(31.16, 33.80), (31.29, 34.23), (31.52, 34.43),      # the Great Sea
         (31.67, 34.55), (31.80, 34.63), (32.05, 34.74),
         (32.28, 34.83), (32.50, 34.89), (32.62, 34.92),
         (32.83, 34.96), (32.79, 35.03), (32.92, 35.07),
         (33.04, 35.10), (33.09, 35.11), (33.27, 35.19),
         (33.45, 35.29), (33.56, 35.37), (33.90, 35.48),
         (34.12, 35.65), (34.30, 35.73), (34.45, 35.85)]),
    (7, [(34.45, 35.85), (34.30, 35.95)]),                    # sea->Mount Hor
    (8, [(34.30, 35.95), (34.20, 36.35), (34.31, 36.92)]),    # ->Lebo-hamath->Zedad
    (9, [(34.31, 36.92), (34.36, 37.10), (34.23, 37.24)]),    # ->Ziphron->Hazar-enan
    (10, [(34.23, 37.24), (33.80, 36.60)]),                   # ->Shepham
    (11, [(33.80, 36.60), (33.40, 36.30), (32.85, 35.65)]),   # ->Riblah->Chinnereth
    (12, [(32.85, 35.65), (32.70, 35.60), (32.55, 35.57),     # ->Jordan->Salt Sea
          (32.40, 35.58), (32.25, 35.56), (32.10, 35.56),
          (31.95, 35.54), (31.77, 35.56), (31.60, 35.58),
          (31.45, 35.57), (31.25, 35.56), (31.10, 35.52),
          (31.03, 35.46)]),
]
CANAAN_POLY = [p for _, seg in BORDER_SEGS for p in seg[:-1]]

# (label, lat, lon, first verse, (dx, dy, PIL anchor), leader, uncertain)
# Offsets are hand-tuned against the Frame A projection — QC after moving.
# (Azmon and Hazar-addar get dots via the border itself; their labels would
# not fit in the crowded southwest pocket — the side panel names them.)
LANDMARKS34 = [
    ("ascent of Akrabbim", 30.90, 35.15, 3, (14, 8, "lm"), False, False),
    ("Kadesh-barnea", 30.63, 34.42, 4, (0, 20, "mt"), False, False),
    ("Mount Hor", 34.30, 35.95, 7, (-8, -14, "rm"), False, True),
    ("Lebo-hamath", 34.20, 36.35, 8, (-8, 8, "rm"), False, False),
    ("Zedad", 34.31, 36.92, 8, (-4, -12, "mb"), False, False),
    ("Ziphron", 34.36, 37.10, 9, (10, -28, "mb"), True, True),
    ("Hazar-enan", 34.23, 37.24, 9, (0, 9, "mt"), False, True),
    ("Shepham", 33.80, 36.60, 10, (8, 0, "lm"), False, True),
    ("Riblah", 33.40, 36.30, 11, (-8, 0, "rm"), False, True),
    ("Jericho", 31.87, 35.44, 15, (-8, 0, "rm"), False, False),
]

# --- Tribal territories (Joshua 13-19, standard atlas approximation) ------
TRIBES = {
    "JUDAH": ("Judah",
              [(31.16, 33.80), (31.45, 34.35), (31.78, 34.62), (31.80, 34.90),
               (31.75, 35.08), (31.72, 35.20), (31.78, 35.38), (31.76, 35.46),
               (31.55, 35.40), (31.30, 35.41), (31.03, 35.45), (30.90, 35.15),
               (30.78, 34.90), (30.63, 34.42), (30.85, 34.20), (30.95, 34.00)],
              (31.35, 34.85)),
    "SIMEON": ("Simeon",
               [(31.45, 34.40), (31.42, 34.95), (31.28, 35.05), (31.05, 34.90),
                (31.00, 34.50), (31.20, 34.30)],
               (31.12, 34.62)),
    "BENJAMIN": ("Benjamin",
                 [(31.75, 35.08), (31.93, 35.12), (31.95, 35.32),
                  (31.88, 35.50), (31.78, 35.47), (31.72, 35.20)],
                 (31.85, 35.36)),
    "DAN": ("Dan",
            [(31.78, 34.62), (32.05, 34.74), (32.02, 35.05), (31.93, 35.12),
             (31.75, 35.08), (31.80, 34.90)],
            (31.92, 34.86)),
    "EPHRAIM": ("Ephraim",
                [(32.05, 34.74), (32.30, 34.86), (32.32, 35.15),
                 (32.22, 35.40), (32.12, 35.52), (31.95, 35.50),
                 (31.95, 35.32), (31.93, 35.12), (32.02, 35.05)],
                (32.15, 35.12)),
    "MANASSEH_W": ("Manasseh",
                   [(32.30, 34.86), (32.62, 34.92), (32.83, 34.96),
                    (32.78, 35.05), (32.65, 35.18), (32.55, 35.30),
                    (32.50, 35.42), (32.48, 35.54), (32.40, 35.55),
                    (32.12, 35.52), (32.22, 35.40), (32.32, 35.15)],
                   (32.42, 35.06)),
    "ISSACHAR": ("Issachar",
                 [(32.55, 35.30), (32.70, 35.33), (32.75, 35.45),
                  (32.70, 35.55), (32.60, 35.56), (32.48, 35.54),
                  (32.50, 35.42)],
                 (32.56, 35.45)),
    "ZEBULUN": ("Zebulun",
                [(32.75, 35.12), (32.95, 35.18), (32.98, 35.35),
                 (32.85, 35.42), (32.75, 35.45), (32.70, 35.33),
                 (32.68, 35.20)],
                (32.85, 35.27)),
    "ASHER": ("Asher",
              [(32.83, 34.96), (32.92, 35.07), (33.09, 35.11), (33.27, 35.19),
               (33.42, 35.30), (33.35, 35.45), (33.10, 35.40), (32.98, 35.35),
               (32.95, 35.18), (32.75, 35.12), (32.78, 35.05)],
              (33.05, 35.20)),
    "NAPHTALI": ("Naphtali",
                 [(32.85, 35.42), (32.98, 35.35), (33.10, 35.40),
                  (33.35, 35.45), (33.30, 35.62), (33.05, 35.63),
                  (32.88, 35.57), (32.80, 35.52), (32.75, 35.45)],
                 (33.15, 35.55)),
    "REUBEN": ("Reuben",
               [(31.88, 35.53), (31.90, 36.05), (31.45, 36.05), (31.44, 35.80),
                (31.47, 35.57), (31.70, 35.58), (31.77, 35.53)],
               (31.30, 35.95)),
    "GAD": ("Gad",
            [(31.88, 35.53), (32.10, 35.54), (32.35, 35.56), (32.68, 35.58),
             (32.55, 35.75), (32.40, 35.92), (32.30, 36.05), (31.90, 36.05)],
            (32.13, 35.82)),
    "MANASSEH_E": ("Manasseh",
                   [(32.68, 35.58), (32.90, 35.62), (33.25, 35.65),
                    (33.25, 35.95), (33.10, 36.45), (32.70, 36.65),
                    (32.60, 36.15), (32.40, 35.92), (32.55, 35.75)],
                   (32.90, 36.10)),
}
WEST_TRIBES = ["JUDAH", "SIMEON", "BENJAMIN", "DAN", "EPHRAIM", "MANASSEH_W",
               "ISSACHAR", "ZEBULUN", "ASHER", "NAPHTALI"]
EAST_TRIBES = ["REUBEN", "GAD", "MANASSEH_E"]

# --- Numbers 32 regions & cities ------------------------------------------
JAZER_GILEAD = [(32.55, 35.62), (32.40, 35.95), (32.05, 36.02), (31.70, 36.00),
                (31.45, 35.95), (31.45, 35.65), (31.70, 35.60), (32.10, 35.58),
                (32.40, 35.58)]
SIHON_POLY = [(31.77, 35.53), (31.70, 35.58), (31.47, 35.57), (31.44, 35.80),
              (31.45, 36.05), (32.00, 36.08), (32.18, 35.90), (32.19, 35.56),
              (32.10, 35.53), (31.90, 35.52)]
OG_POLY = [(32.19, 35.56), (32.18, 35.90), (32.10, 36.15), (32.62, 36.15),
           (32.70, 36.65), (33.10, 36.45), (33.25, 35.95), (33.25, 35.65),
           (32.90, 35.62), (32.70, 35.58), (32.35, 35.55)]
N_GILEAD = [(32.68, 35.60), (32.55, 35.75), (32.40, 35.92), (32.30, 36.05),
            (32.62, 36.15), (32.90, 36.10), (32.90, 35.62)]
HAVVOTH_JAIR = [(32.35, 35.98), (32.42, 36.08), (32.30, 36.12), (32.45, 35.92)]

# key: (v3 name, lat, lon, anchor, modern id or None)
CITIES32 = {
    "Dibon": ("Dibon", 31.50, 35.78, "r", "Dhiban"),
    "Ataroth": ("Ataroth", 31.57, 35.66, "l", "Kh. Attarus"),
    "Aroer": ("Aroer", 31.44, 35.87, "b", "Arair, on the Arnon rim"),
    "Atroth-shophan": ("Atroth-shophan", 31.67, 35.83, "r", None),
    "Jazer": ("Jazer", 32.00, 35.70, "l", "near es-Salt (uncertain)"),
    "Jogbehah": ("Jogbehah", 32.03, 35.87, "r", "Jubeiha"),
    "Beth-nimrah": ("Nimrah", 31.90, 35.62, "l", "Tell Nimrin"),
    "Beth-haran": ("Beth-haran", 31.81, 35.59, "l", "Tell er-Rameh"),
    "Heshbon": ("Heshbon", 31.80, 35.81, "r", "Tell Hesban"),
    "Elealeh": ("Elealeh", 31.85, 35.85, "a", "el-Al"),
    "Kiriathaim": ("Kiriathaim", 31.62, 35.70, "r", "Kh. el-Qureiyat (unc.)"),
    "Nebo": ("Nebo", 31.77, 35.74, "l", "Kh. el-Mukhayyat"),
    "Baal-meon": ("Beon", 31.68, 35.73, "l", "Ma'in"),
    "Sibmah": ("Sebam", 31.72, 35.83, "r", None),
    "Kenath": ("Kenath", 32.76, 36.61, "b", "Qanawat, in the Hauran"),
}
V3_CITIES = ["Ataroth", "Dibon", "Jazer", "Beth-nimrah", "Heshbon",
             "Elealeh", "Sibmah", "Nebo", "Baal-meon"]


# ---------------------------------------------------------------------------
# Projection & drawing helpers
# ---------------------------------------------------------------------------

class MapFrame:
    """Equirectangular lat/lon window rendered into its own image (so
    geometry outside the window clips cleanly), pasted onto the canvas."""

    def __init__(self, lat0, lat1, lon0, lon1, rect):
        self.lat0, self.lat1, self.lon0, self.lon1 = lat0, lat1, lon0, lon1
        x0, y0, x1, y1 = rect
        self.eff = math.cos(math.radians((lat0 + lat1) / 2))
        s = min((x1 - x0) / ((lon1 - lon0) * self.eff),
                (y1 - y0) / (lat1 - lat0))
        self.s = s
        self.mw = int((lon1 - lon0) * self.eff * s)
        self.mh = int((lat1 - lat0) * s)
        self.px = int(x0 + ((x1 - x0) - self.mw) / 2)
        self.py = int(y0 + ((y1 - y0) - self.mh) / 2)

    def pt(self, lat, lon):
        return ((lon - self.lon0) * self.eff * self.s,
                (self.lat1 - lat) * self.s)

    def pts(self, seq):
        return [self.pt(la, lo) for la, lo in seq]


def seg_partial(pts, frac):
    """Truncate a pixel polyline to the leading `frac` of its length."""
    if frac >= 1.0 or len(pts) < 2:
        return pts
    lens = [math.hypot(b[0] - a[0], b[1] - a[1])
            for a, b in zip(pts, pts[1:])]
    total = sum(lens) or 1.0
    target = total * max(frac, 0.0)
    out = [pts[0]]
    run = 0.0
    for a, b, ln in zip(pts, pts[1:], lens):
        if run + ln >= target:
            f = (target - run) / (ln or 1.0)
            out.append((a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f))
            return out
        out.append(b)
        run += ln
    return out


def dashed_poly(d, pts, fill, width=2):
    for a, b in zip(pts, pts[1:]):
        dashed_line(d, a, b, fill, width)


ANCHORS = {"r": (8, 0, "lm"), "l": (-8, 0, "rm"),
           "a": (0, -7, "mb"), "b": (0, 7, "mt")}


def label_dot(d, xy, name, place="r", fill=TEXT, fnt=None, dot=SAND, r=3,
              unc=False, leader=False):
    """Dot + label. `place` is 'l'/'r'/'a'/'b' or an explicit
    (dx, dy, PIL-anchor) triple; `leader` draws a thin line to the text."""
    x, y = xy
    fnt = fnt or F_MAP
    if dot:
        d.ellipse([x - r, y - r, x + r, y + r], outline=dot, width=2)
    dx, dy, anch = ANCHORS[place] if isinstance(place, str) else place
    if leader:
        lx = x + dx * 0.75
        ly = y + dy * 0.75
        d.line([(x + (2 if dx >= 0 else -2), y - 3), (lx, ly)],
               fill=SAND_DIM, width=1)
    txt = name + " ?" if unc else name
    d.text((x + dx, y + dy), txt, font=fnt, fill=fill, anchor=anch)


def draw_base(md, fr, dim=False):
    """Sea, land, lakes and rivers for one map window."""
    river = RIVER_DIM if dim else RIVER
    md.polygon(fr.pts(LAND_POLY), fill=LAND)
    md.line(fr.pts(COAST), fill=SAND_DIM, width=2)
    for lake in LAKES:
        md.polygon(fr.pts(lake), fill=SEA, outline=SAND_DIM)
    for rv in (JORDAN_UP, JORDAN_LOW, ARNON, JABBOK, YARMOUK):
        md.line(fr.pts(rv), fill=river, width=2)


def redraw_lakes(od, fr):
    """Region fills live on the overlay and would tint the lakes — repaint
    the water on top of them (highlight lines are drawn after this)."""
    for lake in LAKES:
        od.polygon(fr.pts(lake), fill=SEA + (255,),
                   outline=SAND_DIM + (255,))


def compass_scale(md, fr):
    """North arrow (drawn with lines — no glyph arrows) + 50 km bar,
    stacked bottom-right, where all three map windows are empty."""
    x, y = fr.mw - 24, fr.mh - 62
    md.line([(x, y + 22), (x, y)], fill=TEXT_DIM, width=2)
    md.line([(x - 5, y + 8), (x, y)], fill=TEXT_DIM, width=2)
    md.line([(x + 5, y + 8), (x, y)], fill=TEXT_DIM, width=2)
    md.text((x - 10, y + 2), "N", font=F_MAP, fill=TEXT_DIM, anchor="rm")
    bar = 50 * fr.s / 111.0
    bx, by = fr.mw - 16 - bar, fr.mh - 16
    md.line([(bx, by), (bx + bar, by)], fill=TEXT_DIM, width=2)
    md.line([(bx, by - 3), (bx, by + 3)], fill=TEXT_DIM, width=2)
    md.line([(bx + bar, by - 3), (bx + bar, by + 3)], fill=TEXT_DIM, width=2)
    md.text((bx + bar / 2, by - 6), "50 km", font=F_SMALL, fill=TEXT_DIM,
            anchor="mb")


def flatten(m, mo):
    """Composite the overlay, then hand back a draw for the TEXT PASS —
    every label is drawn after fills/repaints/lines so nothing can paint
    over a word."""
    flat = Image.alpha_composite(m.convert("RGBA"), mo).convert("RGB")
    return flat, ImageDraw.Draw(flat)


def paste_map(img, flat, fr):
    img.paste(flat, (fr.px, fr.py))
    ImageDraw.Draw(img).rectangle(
        [fr.px - 1, fr.py - 1, fr.px + fr.mw, fr.py + fr.mh],
        outline=SAND_DIM, width=1)


def panel_lines(d, x, y, lines, gap=22):
    for ln in lines:
        dimmed = ln.startswith(" ")
        d.text((x, y), ln.strip(), font=F_SMALL if dimmed else F_LABEL,
               fill=TEXT_DIM if dimmed else TEXT)
        y += gap
    return y


FOOTER = "borders are approximate scholarly reconstructions"


# ---------------------------------------------------------------------------
# Numbers 34, verses 1-15 — tracing the border of Greater Canaan
# ---------------------------------------------------------------------------

FRAME_A = None

CAPTIONS_34A = {
    1: "instructions for the land you are entering",
    2: "this is the land of Canaan by its borders",
    3: "the south side: from the wilderness of Zin along Edom",
    4: "south of Kadesh-barnea, on to Hazar-addar and Azmon",
    5: "along the Brook of Egypt, out to the sea",
    6: "the west border: the Great Sea",
    7: "from the Great Sea, mark out Mount Hor",
    8: "from Mount Hor to Lebo-hamath, and on to Zedad",
    9: "to Ziphron, ending at Hazar-enan — the north border",
    10: "the east border: from Hazar-enan to Shepham",
    11: "down past Riblah to the slopes east of Chinnereth",
    12: "down the Jordan to the Salt Sea — the whole border",
    13: "this land falls by lot to the nine and a half tribes",
    14: "Reuben, Gad, and half of Manasseh already have theirs",
    15: "beyond the Jordan, opposite Jericho, toward the sunrise",
}

PANEL_34A = {
    2: ["the same outline as the", "Egyptian province of", "Canaan in the Late",
        "Bronze Age", " (B. Mazar; Y. Aharoni)"],
    3: ["Salt Sea = the Dead Sea", "ascent of Akrabbim =", " a pass SW of the Dead Sea"],
    4: ["Kadesh-barnea =", " the Ein el-Qudeirat oasis", "Hazar-addar, Azmon:",
        " nearby, uncertain"],
    5: ["Brook of Egypt =", " Wadi el-Arish"],
    6: ["the Great Sea =", " the Mediterranean"],
    7: ["Mount Hor: a peak in the", "Lebanon range, unknown", " (not Aaron's Mount Hor)"],
    8: ["Lebo-hamath = Labweh,", " in Lebanon's Beqaa Valley", "Zedad = Sadad, Syria"],
    9: ["Ziphron and Hazar-enan:", " east of the Anti-Lebanon,", " uncertain"],
    10: ["Shepham: unknown"],
    11: ["Riblah here: uncertain", "sea of Chinnereth =", " the Sea of Galilee"],
    12: ["the border closes: down", "the Jordan to the Dead Sea", "",
         "far larger than Israel", "ever held — a promise,", "not a census"],
    13: ["nine and a half tribes", "will draw lots west of", "the Jordan"],
    14: ["two and a half tribes", "chose land east of the", "Jordan (Numbers 32)"],
    15: ["their inheritance faces", "Jericho, toward the", "sunrise"],
}


def draw_34_wide(img, verse, grow):
    global FRAME_A
    if FRAME_A is None:
        FRAME_A = MapFrame(29.7, 35.0, 33.3, 37.9, (36, 86, 410, 556))
    fr = FRAME_A
    m = Image.new("RGB", (fr.mw, fr.mh), SEA)
    md = ImageDraw.Draw(m)
    mo = Image.new("RGBA", (fr.mw, fr.mh), (0, 0, 0, 0))
    od = ImageDraw.Draw(mo)

    draw_base(md, fr)

    # faint tint of the whole land from v2 on; Transjordan tint on 14-15
    if verse >= 2:
        od.polygon(fr.pts(CANAAN_POLY), fill=HL + (16,))
    if verse in (14, 15):
        for key in EAST_TRIBES:
            od.polygon(fr.pts(TRIBES[key][1]), fill=TRIBE_COL[key] + (80,))
    redraw_lakes(od, fr)

    # border segments (on the overlay, above the lake repaint — the east
    # border runs along the Jordan and the Dead Sea shore):
    # past = solid sand, current = growing highlight, future = dashed dim
    for v, seg in BORDER_SEGS:
        pts = fr.pts(seg)
        if verse > v or verse >= 13:
            od.line(pts, fill=SAND + (255,), width=3)
        elif verse == v:
            dashed_poly(od, pts, SAND_DIM + (255,), 1)
            lead = seg_partial(pts, grow)
            if len(lead) > 1:
                od.line(lead, fill=g(0.95), width=4)
        else:
            dashed_poly(od, pts, SAND_DIM + (255,), 1)

    # ---- text pass ----
    flat, fd = flatten(m, mo)
    fd.text(fr.pt(32.90, 34.15), "The Great Sea", font=F_WATER,
            fill=WATER_TXT, anchor="mm")
    fd.text(fr.pt(31.22, 35.66), "Salt Sea", font=F_WATER,
            fill=WATER_TXT, anchor="lm")
    fd.text(fr.pt(32.82, 35.72), "Chinnereth", font=F_WATER,
            fill=WATER_TXT, anchor="lm")
    fd.text(fr.pt(30.50, 35.80), "EDOM", font=F_MAP, fill=TEXT_DIM,
            anchor="mm")
    fd.text(fr.pt(30.05, 34.60), "wilderness of Zin", font=F_SMALL,
            fill=TEXT_DIM, anchor="mm")
    label_dot(fd, fr.pt(33.51, 36.29), "Damascus", "r", TEXT_DIM,
              F_SMALL, SAND_DIM)
    label_dot(fd, fr.pt(31.78, 35.23), "Jerusalem", "l", TEXT_DIM,
              F_SMALL, SAND_DIM)
    if verse >= 5:
        fd.text(fr.pt(30.55, 33.42), "Brook of Egypt", font=F_SMALL,
                fill=TEXT if verse == 5 else TEXT_DIM, anchor="lm")

    for name, la, lo, v0, place, leader, unc in LANDMARKS34:
        if verse < v0:
            continue
        cur = (verse == v0)
        label_dot(fd, fr.pt(la, lo), name, place,
                  HL if cur else TEXT, F_MAP_B if cur else F_MAP,
                  HL if cur else SAND, unc=unc, leader=leader)

    compass_scale(fd, fr)
    paste_map(img, flat, fr)


# ---------------------------------------------------------------------------
# Numbers 34, verses 16-29 — the allotment, tribe by tribe
# ---------------------------------------------------------------------------

FRAME_B = None

# verse -> (tribe key, prince, [blurb lines], [(city, lat, lon, place)])
PRINCES = {
    19: ("JUDAH", "Caleb son of Jephunneh",
         ["the southern hill country", "and the Negev"],
         [("Hebron", 31.53, 35.10, "r")]),
    20: ("SIMEON", "Shemuel son of Ammihud",
         ["an enclave inside Judah,", "around Beersheba"],
         [("Beersheba", 31.25, 34.79, "r")]),
    21: ("BENJAMIN", "Elidad son of Chislon",
         ["a narrow strip between", "Jericho and Jerusalem"],
         [("Jericho", 31.87, 35.44, (7, -12, "lm"))]),
    22: ("DAN", "Bukki son of Jogli",
         ["foothills west of Benjamin;", "later the tribe migrated",
          "north to Laish (Judges 18)"],
         [("Zorah", 31.77, 34.98, "b"), ("Laish / Dan", 33.25, 35.65, "r")]),
    23: ("MANASSEH_W", "Hanniel son of Ephod",
         ["from the coast to the Jordan,", "plus half the tribe east in",
          "Gilead and Bashan (Num 32)"],
         [("Megiddo", 32.58, 35.18, "a")]),
    24: ("EPHRAIM", "Kemuel son of Shiphtan",
         ["the central hill country —", "Shechem, Shiloh, Bethel"],
         [("Shiloh", 32.06, 35.29, "b")]),
    25: ("ZEBULUN", "Elizaphan son of Parnach",
         ["the lower Galilee hills,", "landlocked"],
         []),
    26: ("ISSACHAR", "Paltiel son of Azzan",
         ["the eastern Jezreel Valley,", "below Mount Tabor"],
         [("Mt Tabor", 32.69, 35.39, "r")]),
    27: ("ASHER", "Ahihud son of Shelomi",
         ["the coastal plain of Acco,", "north toward Tyre and Sidon"],
         [("Acco", 32.92, 35.07, "l")]),
    28: ("NAPHTALI", "Pedahel son of Ammihud",
         ["the eastern Galilee, west", "of the lake, with Hazor"],
         [("Hazor", 33.02, 35.57, "r")]),
}

CAPTIONS_34B = {
    16: "Yahweh names the men who will divide the land",
    17: "Eleazar the priest and Joshua son of Nun",
    18: "and one prince from every tribe",
    29: "these are they who divided the inheritance in Canaan",
}


def draw_34_zoom(img, verse, grow):
    global FRAME_B
    if FRAME_B is None:
        FRAME_B = MapFrame(30.5, 33.5, 34.2, 36.7, (36, 86, 410, 556))
    fr = FRAME_B
    m = Image.new("RGB", (fr.mw, fr.mh), SEA)
    md = ImageDraw.Draw(m)
    mo = Image.new("RGBA", (fr.mw, fr.mh), (0, 0, 0, 0))
    od = ImageDraw.Draw(mo)

    draw_base(md, fr)

    focus = PRINCES.get(verse)
    focus_key = focus[0] if focus else None
    labels, dim_lines, outlines = [], [], []

    for key in WEST_TRIBES + EAST_TRIBES:
        label, poly, lab = TRIBES[key]
        east = key in EAST_TRIBES
        cur = (key == focus_key or
               (verse == 23 and key == "MANASSEH_E"))
        done = verse == 29 and not east
        if cur:
            od.polygon(fr.pts(poly),
                       fill=TRIBE_COL[key] + (int(60 + 90 * grow),))
            outlines.append(seg_partial(fr.pts(poly + poly[:1]), grow))
            fnt, fill = F_TRIBE, HL
        else:
            od.polygon(fr.pts(poly), fill=TRIBE_COL[key] + (26 if east else 42,))
            dim_lines.append((fr.pts(poly + poly[:1]),
                              SAND if done else SAND_DIM))
            fnt = F_TRIBE if done else F_MAP
            fill = TEXT if done else (TEXT_DIM if east else TEXT)
        labels.append((fr.pt(*lab), label, fnt, fill))

    redraw_lakes(od, fr)
    for pts, col in dim_lines:          # borders above the water repaint
        od.line(pts, fill=col + (255,), width=1)
    for pts in outlines:
        if len(pts) > 1:
            od.line(pts, fill=g(0.95), width=3)

    # ---- text pass ----
    flat, fd = flatten(m, mo)
    for xy, label, fnt, fill in labels:
        fd.text(xy, label, font=fnt, fill=fill, anchor="mm")
    if focus:
        for name, la, lo, place in focus[3]:
            label_dot(fd, fr.pt(la, lo), name, place, HL, F_MAP, HL, r=2)
    fd.text(fr.pt(32.08, 34.60), "The Great Sea", font=F_WATER,
            fill=WATER_TXT, anchor="mm")
    fd.text(fr.pt(30.95, 35.62), "Salt Sea", font=F_WATER,
            fill=WATER_TXT, anchor="lm")
    compass_scale(fd, fr)
    paste_map(img, flat, fr)


# ---------------------------------------------------------------------------
# Numbers 32 — Reuben, Gad, and half-Manasseh east of the Jordan
# ---------------------------------------------------------------------------

FRAME_C = None

# stage: survey | cities3 | rebuke | pledge | grant | build | machir | jair
#        | nobah
SPECS_32 = {
    1: ("survey", "Reuben and Gad, rich in livestock, see Jazer and Gilead",
        ["the plateau east of the", "Jordan — high, well-watered", "grazing country"]),
    2: ("survey", "they come to Moses, Eleazar, and the princes",
        None),
    3: ("cities3", "Ataroth, Dibon, Jazer, Nimrah, Heshbon, Elealeh...",
        ["nine cities of the plateau,", "Arnon gorge to the Jabbok"]),
    4: ("survey", "...the land Yahweh struck before Israel — good for livestock",
        ["the conquest of Sihon and", "Og: Numbers 21"]),
    5: ("survey", "“give us this land; do not take us over the Jordan”",
        None),
    6: ("rebuke", "“shall your brothers go to war while you sit here?”",
        None),
    7: ("rebuke", "“why discourage Israel from crossing over?”",
        None),
    8: ("rebuke", "“your fathers did this when I sent them from Kadesh-barnea”",
        ["the spies' failure:", "Numbers 13-14"]),
    9: ("rebuke", "“they saw the valley of Eshcol and discouraged Israel”",
        None),
    10: ("rebuke", "“Yahweh's anger burned that day”", None),
    11: ("rebuke", "“none twenty or older shall see the land I swore...”",
         None),
    12: ("rebuke", "“...except Caleb and Joshua, who wholly followed Yahweh”",
         None),
    13: ("rebuke", "forty years wandering, until that generation was gone",
         None),
    14: ("rebuke", "“and now you rise in your fathers' place”", None),
    15: ("rebuke", "“if you turn away, he will abandon them in the wilderness”",
         None),
    16: ("pledge", "“we will build sheepfolds here, and cities for our little ones”",
         None),
    17: ("pledge", "“but we will go armed, ahead of Israel”",
         ["the vanguard pledge:", "east-bank soldiers first", "across the river"]),
    18: ("pledge", "“we will not return until every Israelite has his inheritance”",
         None),
    19: ("pledge", "“our inheritance has come to us east of the Jordan”",
         None),
    20: ("pledge", "Moses: “if you arm yourselves before Yahweh for the war...”",
         None),
    21: ("pledge", "“...and every armed man of you crosses the Jordan...”",
         None),
    22: ("pledge", "“...then afterward this land shall be your possession”",
         None),
    23: ("pledge", "“but if not — be sure your sin will find you out”",
         None),
    24: ("pledge", "“build your cities and folds — and do what you promised”",
         None),
    25: ("pledge", "“your servants will do as my lord commands”", None),
    26: ("pledge", "“our children, wives, and flocks will stay in the cities of Gilead”",
         None),
    27: ("pledge", "“but your servants will cross over, every man armed for war”",
         None),
    28: ("pledge", "Moses gives charge to Eleazar and Joshua", None),
    29: ("pledge", "“if they cross armed, give them the land of Gilead”",
         None),
    30: ("pledge", "“if not, they inherit among you in Canaan”", None),
    31: ("pledge", "“as Yahweh has said, so will we do”", None),
    32: ("pledge", "“we will cross armed — and our inheritance stays here”",
         None),
    33: ("grant", "Moses grants the kingdoms of Sihon and Og",
         ["Sihon the Amorite ruled", "from Heshbon; Og ruled", "Bashan, in the north"]),
    34: ("build", "Gad rebuilds Dibon, Ataroth, and Aroer", None),
    35: ("build", "Atroth-shophan, Jazer, and Jogbehah", None),
    36: ("build", "Beth-nimrah and Beth-haran — fortified cities and folds",
         None),
    37: ("build", "Reuben rebuilds Heshbon, Elealeh, and Kiriathaim", None),
    38: ("build", "Nebo, Baal-meon (their names changed), and Sibmah",
         ["renamed: Nebo and Baal-meon", "carried pagan divine names"]),
    39: ("machir", "the sons of Machir son of Manasseh take Gilead", None),
    40: ("machir", "Moses gives Gilead to Machir", None),
    41: ("jair", "Jair takes their villages: Havvoth-jair",
         ["“the villages of Jair” —", "tent-settlements in Bashan"]),
    42: ("nobah", "Nobah takes Kenath and names it after himself", None),
}

BUILD_VERSES = {34: ("GAD", ["Dibon", "Ataroth", "Aroer"]),
                35: ("GAD", ["Atroth-shophan", "Jazer", "Jogbehah"]),
                36: ("GAD", ["Beth-nimrah", "Beth-haran"]),
                37: ("REUBEN", ["Heshbon", "Elealeh", "Kiriathaim"]),
                38: ("REUBEN", ["Nebo", "Baal-meon", "Sibmah"])}


def draw_32(img, verse, grow):
    global FRAME_C
    if FRAME_C is None:
        FRAME_C = MapFrame(31.0, 33.4, 35.0, 36.9, (36, 86, 410, 556))
    fr = FRAME_C
    m = Image.new("RGB", (fr.mw, fr.mh), SEA)
    md = ImageDraw.Draw(m)
    mo = Image.new("RGBA", (fr.mw, fr.mh), (0, 0, 0, 0))
    od = ImageDraw.Draw(mo)

    stage, caption, notes = SPECS_32[verse]
    draw_base(md, fr, dim=(stage == "rebuke"))

    # ---- overlay pass: fills, water repaint, highlight lines ----
    if stage in ("survey", "cities3"):
        od.polygon(fr.pts(JAZER_GILEAD), fill=HL + (40,))
        redraw_lakes(od, fr)
        lead = seg_partial(fr.pts(JAZER_GILEAD + JAZER_GILEAD[:1]), grow)
        if len(lead) > 1:
            od.line(lead, fill=g(0.9), width=3)

    elif stage == "rebuke":
        # the point of the rebuke: Canaan, west of the river, still waits
        west = [(32.4, 35.0), (32.4, 35.55), (31.9, 35.5), (31.77, 35.5),
                (31.6, 35.4), (31.1, 35.4), (31.1, 35.0)]
        od.polygon(fr.pts(west), fill=TRIBE_COL["EPHRAIM"] + (26,))
        redraw_lakes(od, fr)
        if verse == 8:
            x, y = fr.pt(31.06, 35.06)
            od.line([(x + 46, y - 14), (x, y)], fill=g(0.85), width=2)
            od.line([(x + 10, y - 2), (x, y)], fill=g(0.85), width=2)
            od.line([(x + 4, y - 12), (x, y)], fill=g(0.85), width=2)

    elif stage == "pledge":
        od.polygon(fr.pts(JAZER_GILEAD), fill=HL + (28,))
        redraw_lakes(od, fr)
        # arrow: armed men cross the Jordan ahead of Israel
        a0, a1 = fr.pt(31.98, 35.72), fr.pt(31.95, 35.32)
        lead = seg_partial([a0, a1], grow)
        if len(lead) > 1:
            od.line(lead, fill=g(0.9), width=3)
            if grow > 0.9:
                x, y = a1
                od.line([(x + 10, y - 7), (x, y)], fill=g(0.9), width=3)
                od.line([(x + 11, y + 5), (x, y)], fill=g(0.9), width=3)

    elif stage == "grant":
        for poly in (SIHON_POLY, OG_POLY):
            od.polygon(fr.pts(poly), fill=HL + (34,))
        redraw_lakes(od, fr)
        for poly in (SIHON_POLY, OG_POLY):
            lead = seg_partial(fr.pts(poly + poly[:1]), grow)
            if len(lead) > 1:
                od.line(lead, fill=g(0.95), width=3)

    elif stage == "build":
        tribe, cities = BUILD_VERSES[verse]
        od.polygon(fr.pts(TRIBES[tribe][1]),
                   fill=TRIBE_COL[tribe] + (60,))
        redraw_lakes(od, fr)

    elif stage in ("machir", "jair"):
        od.polygon(fr.pts(N_GILEAD), fill=TRIBE_COL["MANASSEH_E"] + (70,))
        redraw_lakes(od, fr)
        lead = seg_partial(fr.pts(N_GILEAD + N_GILEAD[:1]), grow)
        if len(lead) > 1:
            od.line(lead, fill=g(0.9), width=3)
        if stage == "jair":
            for la, lo in HAVVOTH_JAIR:
                x, y = fr.pt(la, lo)
                od.ellipse([x - 3, y - 3, x + 3, y + 3], outline=g(0.95),
                           width=2)

    elif stage == "nobah":
        od.polygon(fr.pts(OG_POLY), fill=TRIBE_COL["MANASSEH_E"] + (40,))
        redraw_lakes(od, fr)
        x, y = fr.pt(*CITIES32["Kenath"][1:3])
        od.ellipse([x - 3, y - 3, x + 3, y + 3], outline=g(0.95), width=2)

    # ---- text pass ----
    flat, fd = flatten(m, mo)
    fd.text(fr.pt(31.15, 35.60), "Salt Sea", font=F_WATER,
            fill=WATER_TXT, anchor="lm")
    fd.text(fr.pt(32.82, 35.68), "Chinnereth", font=F_WATER,
            fill=WATER_TXT, anchor="lm")
    fd.text(fr.pt(32.30, 35.48), "Jordan", font=F_WATER,
            fill=WATER_TXT, anchor="rm")
    fd.text(fr.pt(31.36, 36.20), "Arnon", font=F_WATER,
            fill=WATER_TXT, anchor="lm")
    fd.text(fr.pt(32.06, 35.94), "Jabbok", font=F_WATER,
            fill=WATER_TXT, anchor="lt")
    if stage != "grant":
        # region words yield to the kingdom names on the grant verse
        fd.text(fr.pt(31.20, 36.20), "MOAB", font=F_MAP, fill=TEXT_DIM,
                anchor="mm")
        fd.text(fr.pt(31.85, 36.45), "AMMON", font=F_MAP, fill=TEXT_DIM,
                anchor="mm")
        fd.text(fr.pt(32.95, 36.25), "BASHAN", font=F_MAP, fill=TEXT_DIM,
                anchor="mm")
        fd.text(fr.pt(32.25, 35.72), "GILEAD", font=F_MAP, fill=TEXT_DIM,
                anchor="lm")
    fd.text(fr.pt(31.70, 35.20), "CANAAN", font=F_MAP, fill=TEXT_DIM,
            anchor="mm")
    label_dot(fd, fr.pt(31.87, 35.44), "Jericho", (-8, 10, "rm"), TEXT_DIM,
              F_SMALL, SAND_DIM)

    if stage == "survey":
        fd.text(fr.pt(31.98, 35.66), "Jazer", font=F_MAP, fill=TEXT,
                anchor="rm")
    elif stage == "cities3":
        for key in V3_CITIES:
            disp, la, lo, place, _ = CITIES32[key]
            label_dot(fd, fr.pt(la, lo), disp, place, HL, F_MAP, HL, r=2)
    elif stage == "rebuke" and verse == 8:
        x, y = fr.pt(31.06, 35.06)
        fd.text((x + 50, y - 16), "to Kadesh-barnea", font=F_SMALL,
                fill=TEXT, anchor="lm")
    elif stage == "pledge":
        fd.text(fr.pt(32.08, 35.52), "armed, ahead of Israel",
                font=F_SMALL, fill=TEXT, anchor="mb")
    elif stage == "grant":
        fd.text(fr.pt(31.62, 35.82), "kingdom of SIHON", font=F_MAP_B,
                fill=HL, anchor="mm")
        fd.text(fr.pt(32.93, 36.10), "kingdom of OG", font=F_MAP_B,
                fill=HL, anchor="mm")
        fd.text(fr.pt(31.35, 35.85), "Reuben", font=F_TRIBE, fill=TEXT,
                anchor="mm")
        fd.text(fr.pt(32.13, 35.82), "Gad", font=F_TRIBE, fill=TEXT,
                anchor="mm")
        fd.text(fr.pt(33.05, 35.85), "half-Manasseh", font=F_TRIBE,
                fill=TEXT, anchor="mm")
    elif stage == "build":
        tribe, cities = BUILD_VERSES[verse]
        fd.text(fr.pt(*TRIBES[tribe][2]), TRIBES[tribe][0], font=F_TRIBE,
                fill=TEXT, anchor="mm")
        # earlier-built cities of the same tribe stay, in plain sand
        for v in range(34, verse):
            if v in BUILD_VERSES and BUILD_VERSES[v][0] == tribe:
                for key in BUILD_VERSES[v][1]:
                    _, la, lo, place, _ = CITIES32[key]
                    label_dot(fd, fr.pt(la, lo), key, place, TEXT, F_SMALL,
                              SAND, r=2)
        for key in cities:
            _, la, lo, place, _ = CITIES32[key]
            label_dot(fd, fr.pt(la, lo), key, place, HL, F_MAP_B, HL, r=3)
    elif stage in ("machir", "jair"):
        fd.text(fr.pt(32.62, 36.00), "Machir (Manasseh)", font=F_TRIBE,
                fill=HL, anchor="mm")
        if stage == "jair":
            fd.text(fr.pt(32.22, 36.04), "Havvoth-jair", font=F_MAP_B,
                    fill=HL, anchor="lt")
    elif stage == "nobah":
        x, y = fr.pt(*CITIES32["Kenath"][1:3])
        fd.text((x, y + 7), "Kenath", font=F_MAP_B, fill=HL, anchor="mt")
        fd.text((x, y + 23), "(Nobah)", font=F_MAP, fill=HL, anchor="mt")

    compass_scale(fd, fr)
    paste_map(img, flat, fr)


# ---------------------------------------------------------------------------
# Frame assembly
# ---------------------------------------------------------------------------

PANEL_X = 440


def canvas(title, verse, caption):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((28, 18), title, font=F_TITLE, fill=TEXT)
    d.text((28, 52), f"verse {verse} — {caption}", font=F_VERSE, fill=HL)
    d.text((28, H - 24), FOOTER, font=F_SMALL, fill=TEXT_DIM)
    return img, d


def render_34(verse, t):
    grow = ease(min(1.0, t / 0.92))
    if verse <= 15:
        caption = CAPTIONS_34A[verse]
        img, d = canvas("The Borders of the Land — Numbers 34", verse,
                        caption)
        draw_34_wide(img, verse, grow)
        lines = PANEL_34A.get(verse)
        if lines:
            d.text((PANEL_X, 120), "the ancient landmarks", font=F_DIM,
                   fill=TEXT_DIM)
            panel_lines(d, PANEL_X, 150, lines)
    else:
        focus = PRINCES.get(verse)
        if focus:
            caption = f"for the tribe of {TRIBES[focus[0]][0]}: {focus[1]}"
        else:
            caption = CAPTIONS_34B[verse]
        img, d = canvas("Dividing the Inheritance — Numbers 34", verse,
                        caption)
        draw_34_zoom(img, verse, grow)
        if focus:
            d.text((PANEL_X, 130), TRIBES[focus[0]][0], font=F_BIG, fill=HL)
            d.text((PANEL_X, 176), f"prince: {focus[1]}", font=F_LABEL,
                   fill=TEXT)
            panel_lines(d, PANEL_X, 212, focus[2])
            d.text((PANEL_X, 330),
                   "territory as described in Joshua 13-19", font=F_SMALL,
                   fill=TEXT_DIM)
            d.text((PANEL_X, 352),
                   "Reuben, Gad, half-Manasseh: already", font=F_SMALL,
                   fill=TEXT_DIM)
            d.text((PANEL_X, 372),
                   "settled east of the Jordan (Num 32)", font=F_SMALL,
                   fill=TEXT_DIM)
        elif verse == 17:
            panel_lines(d, PANEL_X, 130,
                        ["Eleazar casts the lots;", "Joshua leads the conquest",
                         "", " the division itself is told", " in Joshua 13-19"])
        elif verse == 18:
            panel_lines(d, PANEL_X, 130,
                        ["ten princes for ten tribes —", "Levi receives cities,",
                         "not territory (Num 35)"])
    return img


def render_32(verse, t):
    grow = ease(min(1.0, t / 0.92))
    stage, caption, notes = SPECS_32[verse]
    img, d = canvas("East of the Jordan — Numbers 32", verse, caption)
    draw_32(img, verse, grow)
    y = 120
    if notes:
        y = panel_lines(d, PANEL_X, y, notes) + 14
    if verse in BUILD_VERSES:
        d.text((PANEL_X, y), "modern identifications", font=F_DIM,
               fill=TEXT_DIM)
        y += 28
        for key in BUILD_VERSES[verse][1]:
            modern = CITIES32[key][4]
            line = f"{key} — {modern}" if modern else f"{key} — site unknown"
            d.text((PANEL_X, y), line, font=F_SMALL, fill=TEXT)
            y += 22
    if verse == 3:
        d.text((PANEL_X, y), "identified sites include", font=F_DIM,
               fill=TEXT_DIM)
        y += 28
        for key in ("Dibon", "Heshbon", "Nebo", "Baal-meon"):
            d.text((PANEL_X, y), f"{CITIES32[key][0]} — {CITIES32[key][4]}",
                   font=F_SMALL, fill=TEXT)
            y += 22
    return img


# ---------------------------------------------------------------------------

def render_chapter(book, chapter, n_verses, renderer):
    total = 0
    for verse in range(1, n_verses + 1):
        frames = [renderer(verse, i / (G_FRAMES - 1)) for i in range(G_FRAMES)]
        out = out_path(book, chapter, f"{book}_{chapter}_{verse}.webp")
        frames[0].save(out, save_all=True, append_images=frames[1:],
                       duration=G_FRAME_MS, loop=1, quality=82, method=4)
        total += os.path.getsize(out)
    print(f"{book} {chapter}: {n_verses} files, {total/1e6:.1f} MB")
    return total


if __name__ == "__main__":
    grand = render_chapter("Numbers", 34, 29, render_34)
    grand += render_chapter("Numbers", 32, 42, render_32)
    print(f"TOTAL {grand/1e6:.1f} MB")
