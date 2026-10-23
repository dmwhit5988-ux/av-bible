"""Shared map data for Numbers 32 and 34, and the map projection.

A library: generate_numbers34_svg.py and generate_numbers32_svg.py draw the
maps from it, and eight more generators (Genesis 1, 2, 6-9, 10 and 11,
Numbers 1-2, Acts 13-14 and 15-18) take its water and land colours or its
MapFrame projection. What it holds:

* The land: coast, lakes and rivers, plus the wider world (the Sinai and
  Delta coast, the Syrian coast, the gulfs) that the Numbers 34 camera shows
  when it pulls back. Context only, never labelled.

* Numbers 34:1-15 — "Greater Canaan". The border of the land, one segment
  per border verse in reading order (south, west = the Great Sea, north,
  east), built from the same coast, river and shore points so the Jordan
  stretch runs on the river. The landmarks named along it carry their WEB
  names, and the current verse's landmark its modern identification
  (Kadesh Barnea = Ein el-Qudeirat, Brook of Egypt = Wadi el-Arish ...).
  The northern reach follows the mainstream view (Mazar, Aharoni) that these
  borders preserve Egypt's Late Bronze Age province of Canaan.

* Numbers 34:16-29 — the twelve tribal territories (as later described in
  Joshua 13-19) and the prince named for each tribe (vv 19-28). The
  territories are a SHARED-EDGE partition: every boundary between two
  neighbours is written once and both use it, and the coast and the Jordan
  and lake shores are their outer edges, so no gap or overlap opens however
  far the camera zooms in.

* Numbers 32 (all 42 verses) — the Transjordan: the lands of Jazer and
  Gilead, the kingdoms of Sihon and Og, and the cities Gad and Reuben
  rebuilt, with a stage per verse saying what that verse shows.

All coordinates are approximate scholarly reconstructions — the ancient
landmarks are only partly identifiable. Geometry is hand-encoded lat/lon
simplified from standard Bible atlas reconstructions.
"""

import math

SEA = (24, 36, 54)             # water fill
LAND = (34, 35, 29)            # land fill
RIVER = (78, 112, 148)
RIVER_DIM = (52, 72, 94)
WATER_TXT = (110, 132, 158)

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

# Coast, south to north. Carmel is a rounded Haifa bay; (33.43, 35.279) is
# Asher's north end, on the coast.
COAST = [(30.95, 33.35), (31.05, 33.55), (31.16, 33.80), (31.29, 34.23),
         (31.52, 34.43), (31.67, 34.55), (31.80, 34.63), (32.05, 34.74),
         (32.28, 34.83), (32.50, 34.89), (32.62, 34.92), (32.83, 34.96),
         (32.818, 34.995), (32.808, 35.03), (32.83, 35.058),
         (32.875, 35.071), (32.92, 35.075), (33.04, 35.10), (33.09, 35.11),
         (33.27, 35.19), (33.43, 35.279), (33.45, 35.29), (33.56, 35.37),
         (33.90, 35.48), (34.12, 35.65), (34.30, 35.73), (34.45, 35.85),
         (34.70, 35.97), (34.95, 36.05), (35.20, 36.10)]

# Land = everything east/south of the coastline (generous outer corners;
# the map window clips whatever falls outside it).
LAND_POLY = COAST + [(35.4, 38.4), (29.2, 38.4), (29.2, 33.0)]

# The Dead Sea carries the Jordan mouth (31.77, 35.51) and the Arnon mouth
# (31.47, 35.5713) as vertices, and Galilee its outlet (32.70, 35.57), so
# the territories and the border can share them.
DEAD_SEA = [(31.77, 35.50), (31.77, 35.51), (31.76, 35.56), (31.60, 35.58),
            (31.47, 35.5713), (31.45, 35.57), (31.25, 35.56), (31.10, 35.52),
            (31.03, 35.46), (31.12, 35.42), (31.30, 35.41), (31.50, 35.40),
            (31.65, 35.43), (31.72, 35.46)]
GALILEE = [(32.90, 35.58), (32.86, 35.63), (32.78, 35.64), (32.71, 35.60),
           (32.70, 35.57), (32.76, 35.52), (32.85, 35.53)]
HULEH = [(33.10, 35.59), (33.06, 35.62), (33.02, 35.60), (33.05, 35.57)]
LAKES = (DEAD_SEA, GALILEE, HULEH)

# The lower Jordan carries every junction the territories use.
JORDAN_UP = [(33.25, 35.63), (33.10, 35.60), (32.90, 35.58)]
JORDAN_LOW = [(32.70, 35.57), (32.68, 35.567), (32.55, 35.55),
              (32.48, 35.555), (32.40, 35.56), (32.25, 35.54),
              (32.12, 35.54), (32.10, 35.54), (31.95, 35.52),
              (31.88, 35.516), (31.77, 35.51)]
ARNON = [(31.47, 35.5713), (31.44, 35.80), (31.47, 36.05), (31.40, 36.25)]
JABBOK = [(32.19, 35.54), (32.17, 35.72), (32.08, 35.88), (31.99, 35.98),
          (32.05, 36.08)]
YARMOUK = [(32.68, 35.567), (32.71, 35.75), (32.76, 35.95), (32.73, 36.15)]
RIVERS = (JORDAN_UP, JORDAN_LOW, ARNON, JABBOK, YARMOUK)

# --- The wider world, for the Numbers 34 camera's wide shots ---------------
# Coarse on purpose: context, never labelled.
COAST_WEST = [(30.85, 27.5), (30.95, 29.0), (31.20, 29.90), (31.45, 30.35),
              (31.52, 30.80), (31.58, 31.30), (31.52, 31.85), (31.35, 32.10),
              (31.26, 32.30), (31.12, 32.65), (31.08, 32.95), (31.00, 33.20)]
COAST_NORTH = [(35.52, 35.77), (35.88, 35.86), (36.22, 35.94), (36.58, 36.17),
               (36.85, 36.02), (36.76, 35.56), (36.80, 34.64), (36.32, 33.95),
               (36.08, 32.85), (36.30, 32.20), (36.62, 31.40), (36.88, 30.70)]
WORLD_COAST = COAST_WEST + COAST + COAST_NORTH
WORLD_LAND = (WORLD_COAST + [(38.5, 30.2), (38.5, 46.0), (24.0, 46.0),
                             (24.0, 27.0), (30.8, 27.0)])
GULF_SUEZ = [(29.97, 32.55), (29.80, 32.62), (29.40, 32.78), (28.90, 33.02),
             (28.40, 33.40), (27.90, 33.80), (27.60, 34.15), (27.30, 33.95),
             (27.70, 33.45), (28.30, 33.00), (28.90, 32.75), (29.50, 32.45),
             (29.88, 32.45)]
GULF_AQABA = [(29.55, 34.96), (29.40, 35.00), (29.00, 34.86), (28.50, 34.72),
              (28.00, 34.58), (27.70, 34.40), (27.90, 34.30), (28.40, 34.45),
              (28.90, 34.62), (29.35, 34.85)]
RED_SEA = [(27.60, 34.15), (27.70, 34.40), (27.00, 35.50), (24.0, 37.5),
           (24.0, 33.5), (27.30, 33.95)]
WORLD_SEAS = (GULF_SUEZ, GULF_AQABA, RED_SEA)
WORLD_LAT = (24.5, 38.0)       # the drawn world; no shot may see past it
WORLD_LON = (27.0, 45.5)


def _run(seq, a, b):
    """The stretch of `seq` from point a to point b, in that direction."""
    ia, ib = seq.index(a), seq.index(b)
    return seq[ia:ib + 1] if ia <= ib else seq[ib:ia + 1][::-1]


def _coast(a, b):
    return _run(COAST, a, b)


def _jordan(a, b):
    return _run(JORDAN_LOW, a, b)


def _chain(*parts):
    """Join runs into one ring, dropping the repeated joint points."""
    out = []
    for part in parts:
        for p in part:
            if not out or out[-1] != p:
                out.append(p)
    if len(out) > 1 and out[0] == out[-1]:
        out.pop()
    return out


def _rev(seq):
    return list(reversed(seq))


# --- Numbers 34 border, one entry per border verse, in reading order ------
_DS_EAST = [(31.77, 35.51), (31.76, 35.56), (31.60, 35.58), (31.47, 35.5713),
            (31.45, 35.57), (31.25, 35.56), (31.10, 35.52), (31.03, 35.46)]
BORDER_SEGS = [
    (3, [(31.03, 35.46), (30.90, 35.15)]),                    # Salt Sea->Akrabbim
    (4, [(30.90, 35.15), (30.78, 34.90), (30.63, 34.42),      # ->Zin->Kadesh
         (30.70, 34.32), (30.85, 34.20)]),                    # ->Hazar Addar->Azmon
    (5, [(30.85, 34.20), (30.95, 34.00), (31.16, 33.80)]),    # ->Brook of Egypt->sea
    (6, _coast((31.16, 33.80), (34.45, 35.85))),              # the Great Sea
    (7, [(34.45, 35.85), (34.30, 35.95)]),                    # sea->Mount Hor
    (8, [(34.30, 35.95), (34.20, 36.35), (34.31, 36.92)]),    # ->Hamath->Zedad
    (9, [(34.31, 36.92), (34.36, 37.10), (34.23, 37.24)]),    # ->Ziphron->Hazar Enan
    (10, [(34.23, 37.24), (33.80, 36.60)]),                   # ->Shepham
    (11, [(33.80, 36.60), (33.40, 36.30), (32.85, 35.65)]),   # ->Riblah->Chinnereth
    # down the lake's east shore, ON the Jordan, then the Salt Sea's shore
    (12, _chain([(32.85, 35.65), (32.78, 35.64), (32.71, 35.60)],
                JORDAN_LOW, _DS_EAST)),
]
CANAAN_POLY = [p for _, seg in BORDER_SEGS for p in seg[:-1]]

# --- Tribal territories (Joshua 13-19, standard atlas approximation) ------
# A shared-edge partition: each boundary below is written once and used by
# both neighbours.
_JUDAH_DAN = [(31.80, 34.63), (31.80, 34.90), (31.75, 35.08)]
_JUDAH_BEN = [(31.75, 35.08), (31.755, 35.23), (31.78, 35.38), (31.79, 35.45),
              (31.77, 35.51)]
_DAN_BEN = [(31.75, 35.08), (31.93, 35.12)]
_DAN_EPH = [(31.93, 35.12), (32.02, 35.05), (32.05, 34.74)]
_BEN_EPH = [(31.93, 35.12), (31.95, 35.32), (31.95, 35.52)]
_EPH_MAN = [(32.28, 34.83), (32.32, 35.15), (32.22, 35.40), (32.12, 35.54)]
_MAN_ISS = [(32.48, 35.555), (32.50, 35.42), (32.55, 35.30), (32.66, 35.24)]
_MAN_ZEB = [(32.66, 35.24), (32.70, 35.18), (32.75, 35.12)]
_MAN_ASH = [(32.75, 35.12), (32.78, 35.05), (32.83, 34.96)]
_ZEB_ISS = [(32.66, 35.24), (32.70, 35.33), (32.75, 35.45)]
_ZEB_ASH = [(32.75, 35.12), (32.95, 35.18), (32.98, 35.35)]
_ZEB_NAP = [(32.98, 35.35), (32.85, 35.42), (32.75, 35.45)]
_ISS_NAP = [(32.75, 35.45), (32.76, 35.52)]
_ASH_NAP = [(32.98, 35.35), (33.10, 35.40), (33.36, 35.45)]
_REU_GAD = [(31.88, 35.516), (31.89, 35.75), (31.90, 36.05)]
_GAD_MAN = [(32.68, 35.567), (32.55, 35.75), (32.40, 35.92)]
_DS_JUDAH = [(31.77, 35.51), (31.77, 35.50), (31.72, 35.46), (31.65, 35.43),
             (31.50, 35.40), (31.30, 35.41), (31.12, 35.42), (31.03, 35.46)]
_SOUTH = [(31.03, 35.46), (30.90, 35.15), (30.78, 34.90), (30.63, 34.42),
          (30.70, 34.32), (30.85, 34.20), (30.95, 34.00), (31.16, 33.80)]
_SIMEON = [(31.42, 34.45), (31.42, 34.95), (31.28, 35.05), (31.05, 34.90),
           (31.00, 34.50), (31.20, 34.30)]

# key -> [outer ring, holes...]. Judah carries Simeon as a hole: Simeon is
# an enclave inside it.
TRIBE_RINGS = {
    "JUDAH": [_chain(_coast((31.16, 33.80), (31.80, 34.63)), _JUDAH_DAN,
                     _JUDAH_BEN, _DS_JUDAH, _SOUTH), _SIMEON],
    "SIMEON": [_SIMEON],
    "BENJAMIN": [_chain(_BEN_EPH, _jordan((31.95, 35.52), (31.77, 35.51)),
                        _rev(_JUDAH_BEN), _DAN_BEN)],
    "DAN": [_chain(_coast((31.80, 34.63), (32.05, 34.74)), _rev(_DAN_EPH),
                   _rev(_DAN_BEN), _rev(_JUDAH_DAN))],
    "EPHRAIM": [_chain(_coast((32.05, 34.74), (32.28, 34.83)), _EPH_MAN,
                       _jordan((32.12, 35.54), (31.95, 35.52)),
                       _rev(_BEN_EPH), _DAN_EPH)],
    "MANASSEH_W": [_chain(_coast((32.28, 34.83), (32.83, 34.96)),
                          _rev(_MAN_ASH), _rev(_MAN_ZEB), _rev(_MAN_ISS),
                          _jordan((32.48, 35.555), (32.12, 35.54)),
                          _rev(_EPH_MAN))],
    "ISSACHAR": [_chain(_ZEB_ISS, _ISS_NAP, [(32.76, 35.52), (32.70, 35.57)],
                        _jordan((32.70, 35.57), (32.48, 35.555)), _MAN_ISS)],
    "ZEBULUN": [_chain(_ZEB_ASH, _ZEB_NAP, _rev(_ZEB_ISS), _MAN_ZEB)],
    "ASHER": [_chain(_coast((32.83, 34.96), (33.43, 35.279)), [(33.36, 35.45)],
                     _rev(_ASH_NAP), _rev(_ZEB_ASH), _MAN_ASH)],
    "NAPHTALI": [_chain([(32.76, 35.52), (32.85, 35.53), (32.90, 35.58)],
                        _rev(JORDAN_UP), [(33.32, 35.62), (33.36, 35.45)],
                        _rev(_ASH_NAP), _ZEB_NAP, _ISS_NAP)],
    "REUBEN": [_chain([(31.77, 35.51)], _REU_GAD, [(31.47, 36.05)],
                      _rev(ARNON[:3]), [(31.60, 35.58), (31.76, 35.56)])],
    "GAD": [_chain(_jordan((31.88, 35.516), (32.68, 35.567)), _GAD_MAN,
                   [(32.30, 36.05)], _rev(_REU_GAD))],
    "MANASSEH_E": [_chain([(32.68, 35.567), (32.70, 35.57), (32.71, 35.60),
                           (32.78, 35.64), (32.86, 35.63), (32.90, 35.58)],
                          JORDAN_UP[::-1],
                          [(33.25, 35.95), (33.10, 36.45), (32.70, 36.65),
                           (32.60, 36.15)], _rev(_GAD_MAN))],
}

# TRIBES: key -> (name, outer ring, label point). The label point is for
# Numbers 32's fixed map; Numbers 34 finds room for each name at its own
# camera.
_LABEL_AT = {
    "JUDAH": ("Judah", (31.58, 34.95)), "SIMEON": ("Simeon", (31.12, 34.62)),
    "BENJAMIN": ("Benjamin", (31.85, 35.36)), "DAN": ("Dan", (31.92, 34.86)),
    "EPHRAIM": ("Ephraim", (32.15, 35.12)),
    "MANASSEH_W": ("Manasseh", (32.42, 35.06)),
    "ISSACHAR": ("Issachar", (32.56, 35.45)),
    "ZEBULUN": ("Zebulun", (32.85, 35.27)), "ASHER": ("Asher", (33.05, 35.20)),
    "NAPHTALI": ("Naphtali", (33.15, 35.55)),
    "REUBEN": ("Reuben", (31.30, 35.95)), "GAD": ("Gad", (32.13, 35.82)),
    "MANASSEH_E": ("Manasseh", (32.90, 36.10)),
}
TRIBES = {key: (name, TRIBE_RINGS[key][0], at)
          for key, (name, at) in _LABEL_AT.items()}
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
# Projection & label anchors
# ---------------------------------------------------------------------------

class MapFrame:
    """Equirectangular lat/lon window fitted (centred) into `rect` =
    (x0, y0, x1, y1) on the canvas. pt()/pts() give coordinates local to
    the window, which is mw x mh with its top-left at (px, py); callers
    draw inside a group clipped to it, so geometry outside clips cleanly."""

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


# a label's offset from its dot, (dx, dy, text anchor), by place:
# right, left, above, below
ANCHORS = {"r": (8, 0, "lm"), "l": (-8, 0, "rm"),
           "a": (0, -7, "mb"), "b": (0, 7, "mt")}

PANEL_X = 440                  # left edge of the side panel, beside the map



# ---------------------------------------------------------------------------
# Numbers 34, verses 1-15 — tracing the border of Greater Canaan
# ---------------------------------------------------------------------------

# (key, name as WEB has it, lat, lon, first verse, label placements to try
# first, uncertain). Placements are the camera layout's codes, nearest-first:
# r / l / a / b = right, left, above, below; ar, br ... the corners.
LANDMARKS34 = [
    ("akrabbim", "ascent of Akrabbim", 30.90, 35.15, 4, ["br", "r", "b"], 0),
    ("kadesh", "Kadesh Barnea", 30.63, 34.42, 4, ["br", "b", "r", "bl"], 0),
    ("hazar_addar", "Hazar Addar", 30.70, 34.32, 4, ["l", "bl", "al"], 1),
    ("azmon", "Azmon", 30.85, 34.20, 4, ["ar", "a", "al", "l"], 1),
    ("mount_hor", "Mount Hor", 34.30, 35.95, 7, ["ar", "a", "a+", "br"], 1),
    ("lebo", "entrance of Hamath", 34.20, 36.35, 8, ["b", "bl", "br"], 0),
    ("zedad", "Zedad", 34.31, 36.92, 8, ["a", "al", "b", "bl"], 0),
    ("ziphron", "Ziphron", 34.36, 37.10, 9, ["ar", "a", "r"], 1),
    ("hazar_enan", "Hazar Enan", 34.23, 37.24, 9, ["r", "br", "b"], 1),
    ("shepham", "Shepham", 33.80, 36.60, 10, ["r", "br", "ar"], 1),
    ("riblah", "Riblah", 33.40, 36.30, 11, ["br", "r", "b"], 1),
    ("jericho", "Jericho", 31.87, 35.44, 15, ["l", "al", "bl"], 0),
]

# The names each verse is about, drawn in HL: landmark keys, the water and
# area names (salt, chin, sea, jordan, edom, zin, brook), and the east-bank
# tribes as "t_<KEY>".
CURRENT34 = {3: {"salt", "edom", "zin"},
             4: {"akrabbim", "zin", "kadesh", "hazar_addar", "azmon"},
             5: {"brook"}, 6: {"sea"}, 7: {"mount_hor"},
             8: {"lebo", "zedad"}, 9: {"ziphron", "hazar_enan"},
             10: {"shepham"}, 11: {"riblah", "chin"}, 12: {"jordan", "salt"},
             14: {"t_REUBEN", "t_GAD", "t_MANASSEH_E"},
             15: {"jericho", "t_REUBEN", "t_GAD", "t_MANASSEH_E"}}

# The modern identification shown under a name on the verse that names it
MODERN34 = {("salt", 3): "Dead Sea", ("kadesh", 4): "Ein el-Qudeirat",
            ("brook", 5): "Wadi el-Arish", ("sea", 6): "Mediterranean",
            ("lebo", 8): "Labweh", ("zedad", 8): "Sadad",
            ("chin", 11): "Sea of Galilee"}


# ---------------------------------------------------------------------------
# Numbers 34, verses 16-29 — the allotment, tribe by tribe
# ---------------------------------------------------------------------------

# verse -> (tribe key, prince)
PRINCES = {
    19: ("JUDAH", "Caleb son of Jephunneh"),
    20: ("SIMEON", "Shemuel son of Ammihud"),
    21: ("BENJAMIN", "Elidad son of Chislon"),
    22: ("DAN", "Bukki son of Jogli"),
    23: ("MANASSEH_W", "Hanniel son of Ephod"),
    24: ("EPHRAIM", "Kemuel son of Shiphtan"),
    25: ("ZEBULUN", "Elizaphan son of Parnach"),
    26: ("ISSACHAR", "Paltiel son of Azzan"),
    27: ("ASHER", "Ahihud son of Shelomi"),
    28: ("NAPHTALI", "Pedahel son of Ammihud"),
}


# ---------------------------------------------------------------------------
# Numbers 32 — Reuben, Gad, and half-Manasseh east of the Jordan
# ---------------------------------------------------------------------------

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
