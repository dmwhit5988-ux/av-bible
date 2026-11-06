"""Render Acts 6:8-8:3 (Stephen) as per-verse SVGs: a camera tour.

Stephen is charged with speaking "against this holy place" (6:13), and his
answer is a tour of every place God met his people outside it. So the
speech is flown over one large map of the Near East, the way Acts 13-14
flies Paul's journey (svg_map_camera): each verse opens on the last verse's
rest camera and flies to its own, so played in order the passage is one
continuous flight.

What it shows (docs/design/acts-6-8.md):

* The council card (acts7_council.py): Stephen among the people, disputed,
  seized and brought in, the witnesses, his face shining, the high priest's
  question (6:8-7:1). At 6:9 the camera rises to the eastern sea for the men
  of the synagogue and where they came from, and comes back down.
* The speech on the map (7:2-7:51): Ur and Haran and the road to Canaan; the
  foot of ground never given; the 400 years; the fathers and the twelve;
  Joseph sold into Egypt; the famine and the two journeys for grain; the 75
  going down; the bones brought back to Shechem; the people growing; Moses
  born, raised in Pharaoh's house, rejected, fled to Midian; the bush at
  Sinai; sent back; the exodus and the forty years; the calf, the host of
  heaven, Moloch's tent and Rephan's star, and the arc to beyond Babylon;
  the tent of the testimony brought in with Joshua to Shiloh; David; and
  Solomon's house. Then the camera rises over all of it, and the prepared
  throne (svg_figures.prepared_throne: God's presence, never God drawn)
  stands over the earth (7:49).
* Two things run through the speech. A gold throne mark stays at each place
  where God appears (Ur, Egypt, Sinai), so by 7:48 Jerusalem is one dot
  among many. And a tally under the title fills with the deliverers the
  fathers rejected (Joseph, Moses, the prophets, the Righteous One), and at
  7:51 the council is the next. A bar of Moses' 120 years in three forties
  (Egypt, Midian, the wilderness) fills from 7:20 to 7:36.
* Back in the card (7:52-8:3): the council gnashing, the roof drawn back on
  the throne with the Chi-Rho (Jesus, never drawn as a man) standing at its
  right hand, the rush, the gate, a few stones, the garments at Saul's feet,
  Stephen kneeling and lying still. At 8:1 the camera rises over Judea and
  Samaria as the assembly scatters, and at 8:3 comes down into the street
  where Saul goes from house to house.

The bush at Sinai (7:30-34) is held on the map for now; its own scene card
is the next step.

The land is point facts: mediterranean.py's coasts, acts_geography's
southern Asia Minor and Cyprus, gazetteer.py's Levant, near_east.py's Nile,
Red Sea, Sinai, rivers of Mesopotamia and Persian Gulf. Israel's roads are
schematic, as every atlas's are; the exodus and the wilderness are Acts 13's
own (acts_geography.STORY), so the two speeches tell one story.

Run inside the project venv:
    .venv\\Scripts\\python.exe generate_acts7_svg.py
It prints any name it had to drop or force, and anything that would land
after the narration.
"""

import math
import os
import time
from xml.sax.saxutils import escape

import svg_figures as F
from svg_surface import SvgCanvas, _fmt, FONT_FAMILY

from config import WEB_AUDIO_DIR
from passages import verse_numbers
from svg_chronicles_world import AUDIO_SLACK, _mp3_seconds
from svg_map_camera import (
    Projection, Flight as MapFlight, Unit as MapUnit, Ctx, Grow, EASE,
    cam_duration, _same, to_screen, ink, title_rect, compass_rect, title_svg,
    compass_scale_svg, inset_view_rect, plate_rect_svg, poly_el, rgb,
    fade, op_anim, traced_el, emit_class, curve_d, layout,
    rest_dots, identities, unchanged, emit_labels, emit_label_layers,
    prev_state, midflight_qc, extent_check, S_OTHER, S_AREA,
    S_CUR, discrete, held_labels, screen_ring, band_dots, lift_in, pin, rider,
)
from svg_scene_card import (CARD_COVER, card_op, card_ends,
                            cards_seen as _cards_seen,
                            card_extent as _card_extent)
from generate_tabernacle import (W, H, BG, SAND, SAND_DIM, TEXT, TEXT_DIM, HL,
                                 out_path)
from generate_tribal_maps import SEA, LAND, RIVER, WATER_TXT
import acts_geography as G
import gazetteer as GZ
import journeys as J
import mediterranean as M
import near_east as NE
import sanctuary as SN
import temple as TP
import acts7_council as CO
import acts7_bush as BU

BOOK = "Acts"
REFS = ([(6, v) for v in verse_numbers(BOOK, 6) if v >= 8]
        + [(7, v) for v in verse_numbers(BOOK, 7)]
        + [(8, v) for v in verse_numbers(BOOK, 8) if v <= 3])
IDX = {r: i for i, r in enumerate(REFS)}
NARR_FALLBACK = 6.0


def _narration(ref):
    ch, v = ref
    sec = _mp3_seconds(os.path.join(WEB_AUDIO_DIR, f"Acts_{ch}_{v}.mp3"))
    return round(sec, 1) if sec else None


NARR = {r: _narration(r) or NARR_FALLBACK for r in REFS}


def prev_ref(ref):
    i = IDX[ref]
    return REFS[i - 1] if i else None


def span(a, b):
    return REFS[IDX[a]:IDX[b] + 1]


def within(ref, a, b):
    return IDX[a] <= IDX[ref] <= IDX[b]


# ---------------------------------------------------------------------------
# Projection and the drawn world
# ---------------------------------------------------------------------------

PROJ = Projection(41.6, 20.0, 32.5)
K, EFF = PROJ.k, PROJ.eff
P, PS = PROJ.P, PROJ.PS
shot, fit = PROJ.shot, PROJ.fit
GROW = Grow(1.6, 0.5, 1.4)


class Unit(MapUnit):
    proj = PROJ
    grow = GROW


class Flight(MapFlight):
    grow = GROW


WORLD_LAT = (26.4, 41.5)
WORLD_LON = (18.8, 49.2)


# ---------------------------------------------------------------------------
# The base map: the Mediterranean shores, the Red Sea and the Persian Gulf
# cut into the land, lakes, rivers
# ---------------------------------------------------------------------------

def land_rings():
    east = (M.ASIA_NORTH + M.ASIA_WEST[1:] + G.MAIN_COAST[1:] + GZ.COAST_SOUTH
            + M.AFRICA[1:])
    out = [east + [(18.0, 8.0), (18.0, 56.0), (46.0, 56.0),
                   (46.0, east[0][1])]]
    greece = M.GREECE_WEST + M.GREECE_EAST
    out.append(greece + [(46.0, greece[-1][1]), (46.0, greece[0][1])])
    return out


RED_SEA_RING = (NE.RED_SEA_WEST + NE.RED_SEA_EAST[1:]
                + [(18.0, 40.0), (18.0, 36.0)])
GULF_RING = NE.GULF_HEAD + [(29.0, 54.0), (22.0, 54.0), (22.0, 50.0)]
ISLANDS = list(M.ISLANDS.values()) + [G.CYPRUS]
LAKES = (list(G.ANATOLIA_LAKES.values())
         + [GZ.LAKES[k] for k in ("galilee", "huleh", "salt_sea")])
RIVERS = ([G.ORONTES, G.CESTRUS, G.EURYMEDON, G.MELAS, G.CALYCADNUS,
           G.CYDNUS, G.SARUS, G.PYRAMUS]
          + list(GZ.RIVERS.values())
          + list(NE.RIVERS.values()))
COASTS = [M.ASIA_WEST, G.MAIN_COAST, GZ.COAST_SOUTH, M.AFRICA,
          M.GREECE_WEST, M.GREECE_EAST, NE.RED_SEA_WEST, NE.RED_SEA_EAST,
          NE.GULF_HEAD]


def simplify(pts, tol):
    if len(pts) < 3:
        return list(pts)
    a, b = pts[0], pts[-1]
    dmax, k = 0.0, 0
    for i in range(1, len(pts) - 1):
        p = pts[i]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1e-12
        d = abs(dx * (p[1] - a[1]) - dy * (p[0] - a[0])) / L
        if d > dmax:
            dmax, k = d, i
    if dmax <= tol:
        return [a, b]
    return simplify(pts[:k + 1], tol)[:-1] + simplify(pts[k:], tol)


def simplify_ring(ring, tol):
    k = max(range(len(ring)), key=lambda i: math.dist(ring[0], ring[i]))
    return (simplify(ring[:k + 1], tol)[:-1]
            + simplify(ring[k:] + ring[:1], tol)[:-1])


DRAW_TOL = 0.006


def base_layers():
    x0, y0 = P(WORLD_LAT[1] + 3, WORLD_LON[0] - 3)
    x1, y1 = P(WORLD_LAT[0] - 3, WORLD_LON[1] + 3)
    els = [(None, f'<rect x="{_fmt(x0)}" y="{_fmt(y0)}" '
                  f'width="{_fmt(x1 - x0)}" height="{_fmt(y1 - y0)}" '
                  f'fill="{rgb(SEA)}"/>')]
    qc = []
    shore = f'stroke="{rgb(SAND_DIM)}"'

    def ring_d(ring):
        return curve_d(PS(simplify_ring(ring, DRAW_TOL)), closed=True)
    for ring in land_rings():
        els.append(("coast", f'<path d="{ring_d(ring)}" fill="{rgb(LAND)}" '
                             f'stroke="none"/>'))
    for ring in (RED_SEA_RING, GULF_RING):
        els.append(("coast", f'<path d="{ring_d(ring)}" fill="{rgb(SEA)}" '
                             f'stroke="none"/>'))
    for line in COASTS:
        els.append(("coast", f'<path d="{curve_d(PS(simplify(line, DRAW_TOL)))}" '
                             f'fill="none" {shore}/>'))
        qc.append((PS(line), "coast", None))
    for ring in ISLANDS:
        els.append(("coast", f'<path d="{ring_d(ring)}" fill="{rgb(LAND)}" '
                             f'{shore}/>'))
        qc.append((PS(ring + ring[:1]), "coast", None))
    for ring in LAKES:
        els.append(("lake", f'<path d="{ring_d(ring)}" fill="{rgb(SEA)}" '
                            f'{shore}/>'))
        qc.append((PS(ring + ring[:1]), "lake", None))
    for rv in RIVERS:
        d = curve_d(PS(simplify(rv, DRAW_TOL)))
        els.append(("river", f'<path d="{d}" fill="none" '
                             f'stroke="{rgb(RIVER)}"/>'))
        qc.append((PS(rv), "river", None))
    return els, qc


def land_screen(cam):
    return [to_screen(cam, P(a, b)) for a, b in land_rings()[0]]


# ---------------------------------------------------------------------------
# Places: key -> (name, lat, lon, first ref, last ref, lit refs)
# ---------------------------------------------------------------------------

def _gz(k):
    s = GZ.SITES[k]
    return s.lat, s.lon


def _ne(k):
    s = NE.SITES[k]
    return s.lat, s.lon


WHOLE_ON = ((7, 48), (7, 51))      # the places of the speech, seen together

PLACES = {
    "jerusalem": ("Jerusalem", *_gz("jerusalem"), (6, 8), (8, 3),
                  [(7, 43), (7, 46), (7, 47)] + span((7, 48), (7, 51))
                  + [(8, 1)]),
    "ur": ("Ur", *_ne("ur"), (7, 2), (7, 8), span((7, 2), (7, 4))),
    "haran": ("Haran", *_ne("haran"), (7, 2), (7, 8), [(7, 2), (7, 4)]),
    "shechem": ("Shechem", *_gz("shechem"), (7, 4), (7, 16),
                [(7, 4), (7, 5), (7, 16)]),
    "hebron": ("Hebron", *_gz("hebron"), (7, 8), (7, 16),
               [(7, 8), (7, 12), (7, 14), (7, 15)]),
    "dothan": ("Dothan", *_gz("dothan"), (7, 9), (7, 9), []),
    "on": ("On", *_ne("on"), (7, 9), (7, 16), []),
    "rameses": ("Rameses", *_ne("rameses"), (7, 17), (7, 35), []),
    "mount_sinai": ("Mount Sinai", *_ne("mount_sinai"), (7, 30), (7, 47),
                    [(7, 30), (7, 38)]),
    "kadesh": ("Kadesh", *_ne("kadesh"), (7, 45), (7, 45), []),
    "shiloh": ("Shiloh", *_gz("shiloh"), (7, 45), (7, 46), [(7, 45)]),
    "babylon": ("Babylon", *_ne("babylon"), (7, 43), (7, 43), [(7, 43)]),
}
# the places named again over the whole map at 7:48-51
AGAIN = {"ur", "haran", "mount_sinai", "babylon"}


def place_pt(key):
    return PLACES[key][1:3]


def place_shown(key, ref):
    _n, _la, _lo, r0, r1, _lit = PLACES[key]
    if within(ref, r0, r1):
        return True
    return key in AGAIN and within(ref, *WHOLE_ON)


# region and water names: key -> (NAME, [(lat, lon)], shown from, to, lit)
REGIONS = {
    "mesopotamia": ("MESOPOTAMIA", [(35.30, 41.40), (34.80, 41.90),
                                    (35.60, 40.80)], (7, 2), (7, 8),
                    [(7, 2)]),
    "chaldea": ("CHALDEA", [(31.55, 45.40), (31.85, 45.10)], (7, 4), (7, 8),
                [(7, 4)]),
    "canaan": ("CANAAN", [(31.55, 34.95), (31.30, 35.00), (32.70, 35.40)],
               (7, 3), (7, 16), [(7, 3), (7, 5), (7, 7)]),
    "egypt": ("EGYPT", [(29.40, 30.55), (29.70, 30.40), (30.50, 30.20)],
              (7, 6), (7, 47), [(7, 6), (7, 9), (7, 10), (7, 36)]),
    "goshen": ("GOSHEN", [(30.62, 31.55), (30.55, 31.75)], (7, 17), (7, 28),
               [(7, 17)]),
    "midian": ("MIDIAN", [(28.45, 35.35), (28.70, 35.50), (28.30, 35.55)],
               (7, 29), (7, 35),
               [(7, 29)]),
    "judea": ("JUDEA", [(31.55, 35.00), (31.45, 35.15)], (8, 1), (8, 2),
              [(8, 1)]),
    "samaria": ("SAMARIA", [(32.30, 35.12), (32.20, 35.30)], (8, 1), (8, 2),
                [(8, 1)]),
}
WATERS = {
    "great_sea": ("The Great Sea", [(33.6, 31.0), (34.3, 29.5), (33.2, 32.4),
                                    (34.6, 27.0), (33.4, 26.0)]),
    "red_sea": ("Red Sea", [(27.40, 34.55), (27.10, 34.80), (28.60, 33.10)]),
}


# ---------------------------------------------------------------------------
# Israel's roads (schematic): key -> (points, the verse it is travelled on,
# when it starts and how long, the last verse it is kept, how it is drawn)
# ---------------------------------------------------------------------------

S = G.SERMON_SITES
UR, HARAN = _ne("ur"), _ne("haran")
JERUS, HEBRON, SHECHEM = _gz("jerusalem"), _gz("hebron"), _gz("shechem")
DOTHAN, BEERSHEBA = _gz("dothan"), _gz("beersheba")
ON, RAMESES, SINAI = _ne("on"), _ne("rameses"), _ne("mount_sinai")
GOSHEN = (NE.REGIONS["goshen"].lat, NE.REGIONS["goshen"].lon)
# where Moses stands among his people, just north of their dots
GOSHEN_N = (GOSHEN[0] + 0.11, GOSHEN[1])
# where the mark of "God was with him" stands, beside Joseph at On
EGYPT_MARK = (29.90, 31.02)
MIDIAN = _ne("bad")
BABYLON = _ne("babylon")
DAMASCUS = (J.PLACES["damascus"].lat, J.PLACES["damascus"].lon)
GILGAL, SHILOH = _gz("gilgal_jericho"), _gz("shiloh")


def _river_between(river, a, b):
    """A river's points from the one nearest a to the one nearest b."""
    i = min(range(len(river)), key=lambda k: math.dist(river[k], a))
    j = min(range(len(river)), key=lambda k: math.dist(river[k], b))
    return river[i:j + 1] if i <= j else river[j:i + 1][::-1]


_UP_EUPHRATES = _river_between(NE.EUPHRATES, (31.04, 46.26), (35.95, 39.01))
_WILD = G.STORY["wilderness"]
_AT_SINAI = _WILD.index(S["sinai"])

ROADS = {
    # 7:4 from Ur up the Euphrates and the Balikh to Haran, then to Canaan
    "ur_haran": ([UR] + _UP_EUPHRATES + NE.BALIKH[::-1][1:] + [HARAN],
                 (7, 4), (0.6, 2.8), (7, 8), "story"),
    "haran_canaan": ([HARAN, (36.83, 38.02), (35.60, 37.30), (34.50, 36.70),
                      DAMASCUS, (32.95, 35.75), (32.55, 35.45), SHECHEM],
                     (7, 4), (6.0, 2.6), (7, 8), "story"),
    # 7:9 Joseph, sold at Dothan, down the coast road to Egypt
    "joseph": ([DOTHAN, (32.05, 34.95), (31.60, 34.55), (31.30, 34.25),
                (31.12, 33.80), (30.95, 32.80), (30.60, 31.90), ON],
               (7, 9), (2.6, 1.8), (7, 16), "story"),
    # 7:12-13 the fathers' two journeys for grain, and 7:14 the summons
    "grain1": ([HEBRON, BEERSHEBA, (30.90, 33.40), (30.55, 32.20), ON],
               (7, 12), (2.4, 1.6), (7, 13), "story"),
    "grain2": ([HEBRON, (31.20, 34.70), (30.80, 33.30), (30.45, 32.25), ON],
               (7, 13), (0.3, 1.8), (7, 14), "story"),
    "summons": ([ON, (30.55, 32.20), (30.90, 33.40), BEERSHEBA, HEBRON],
                (7, 14), (0.6, 1.6), (7, 14), "word"),
    # 7:15 Jacob goes down; 7:16 the bones carried back to Shechem
    "going_down": ([HEBRON, BEERSHEBA, (30.95, 33.20), (30.85, 32.40),
                    GOSHEN], (7, 15), (0.2, 1.8), (7, 16), "story"),
    "bones": ([GOSHEN, (30.95, 32.60), (31.12, 33.80), (31.40, 34.35),
               (31.85, 34.75), (32.10, 35.05), SHECHEM],
              (7, 16), (0.4, 2.2), (7, 16), "story"),
    # 7:21, 7:23 Moses to Pharaoh's house and back to his people
    "to_court": ([GOSHEN, RAMESES], (7, 21), (1.6, 1.4), (7, 21), "word"),
    "to_people": ([RAMESES, GOSHEN_N], (7, 23), (3.4, 1.4), (7, 23), "word"),
    # 7:29 his flight to Midian; 7:30 to the mountain; 7:35 sent to Egypt
    "flight": ([GOSHEN_N, (30.45, 32.25), (29.98, 32.56), (29.95, 33.50),
                (29.80, 34.30), (29.53, 34.98), (29.10, 35.02), MIDIAN],
               (7, 29), (1.0, 2.8), (7, 35), "story"),
    "to_horeb": ([MIDIAN, (29.15, 34.95), (28.95, 34.55), (28.72, 34.20),
                  SINAI], (7, 30), (1.4, 2.2), (7, 35), "story"),
    "to_egypt": ([SINAI, (28.95, 33.25), (29.60, 32.85), (29.98, 32.56),
                  (30.45, 32.25), RAMESES], (7, 35), (5.4, 2.2), (7, 35),
                 "story"),
    # 7:36 the exodus and the wilderness (Acts 13's routes)
    "exodus": (G.STORY["exodus"], (7, 36), (0.6, 2.0), (7, 45), "story"),
    "wilderness": (_WILD[:_AT_SINAI + 1], (7, 36), (4.6, 2.2), (7, 45),
                   "story"),
    # 7:39 their hearts turned back to Egypt
    "turned_back": ([SINAI, (29.00, 33.20), (29.60, 32.75), (29.98, 32.56),
                     (30.40, 32.25)], (7, 39), (3.6, 1.8), (7, 39), "word"),
    # 7:43 carried away beyond Babylon
    "exile": ([JERUS, (32.40, 35.90), DAMASCUS, (34.40, 38.40),
               (34.45, 40.92), (34.14, 42.37), (33.35, 43.78), BABYLON,
               (32.10, 45.10)], (7, 43), (6.4, 2.2), (7, 43), "story"),
    # 7:45 the tent brought in with Joshua: the wilderness from Sinai, the
    # crossing, and Gilgal to Shiloh
    "tent_in": (_WILD[_AT_SINAI:] + [GILGAL], (7, 45), (0.6, 3.0), (7, 45),
                "story"),
    "to_shiloh": ([GILGAL, (31.95, 35.36), SHILOH], (7, 45), (5.0, 1.0),
                  (7, 45), "story"),
}


def road_state(key, ref):
    _pts, on, _t, last, _kind = ROADS[key]
    if IDX[ref] < IDX[on] or IDX[ref] > IDX[last]:
        return None
    return "now" if ref == on else "done"


# 7:5 the land promised, a dashed line round it: Dan to Beersheba
PROMISE = [(33.25, 35.65), (33.05, 35.15), (32.40, 34.90), (31.60, 34.50),
           (31.22, 34.30), (30.95, 34.75), (31.10, 35.40), (31.75, 35.55),
           (32.60, 35.62), (33.25, 35.65)]


# ---------------------------------------------------------------------------
# Drawings pinned on the map
# ---------------------------------------------------------------------------

MAN_H = 97.0
FIG_PX = 66


def fig_svg(parts, h_px, ink_, page=LAND, flip=1, unit_h=MAN_H):
    c = SvgCanvas(10, 10)
    F.draw(c, parts, 0, 0, h_px / unit_h, ink_, page, flip=flip)
    return "".join(c._els)


def man(ink_=TEXT, **kw):
    return fig_svg(F.man(**kw), FIG_PX, ink_)


def king(ink_=TEXT, harp=False):
    out = fig_svg(F.king(), FIG_PX, ink_)
    if harp:
        u = F.UNIT["harp"]
        out += (f'<g transform="translate(24 0)">'
                f'{fig_svg(F.harp(), FIG_PX * u, ink_, unit_h=MAN_H * u)}</g>')
    return out


def fathers(ink_=TEXT):
    one = F.man(staff=True)
    return (f'<g transform="translate(-22 0)">{fig_svg(one, 58, ink_)}</g>'
            f'{fig_svg(one, 66, ink_)}'
            f'<g transform="translate(22 0)">'
            f'{fig_svg(one, 58, ink_, flip=-1)}</g>')


THRONE_UNITS = 160.0
FAMINE_DEFS = ('<radialGradient id="famine"><stop offset="0.3" '
               'stop-color="rgb(8,6,4)" stop-opacity="0.5"/><stop '
               'offset="1" stop-color="rgb(8,6,4)" stop-opacity="0"/>'
               '</radialGradient>')
GLORY_DEFS = ('<radialGradient id="glory"><stop offset="0" '
              'stop-color="rgb(255,236,160)" stop-opacity="0.6"/><stop '
              'offset="1" stop-color="rgb(255,236,160)" stop-opacity="0"/>'
              '</radialGradient>')


def throne_mark(px=34):
    """The prepared throne at map size: the mark left where God appears."""
    k = px / THRONE_UNITS
    gx, gy = F.PREPARED_THRONE_GLORY
    return (f'<circle cx="{_fmt(gx * k)}" cy="{_fmt(-gy * k)}" '
            f'r="{_fmt(px * 0.85)}" fill="url(#glory)"/>'
            + fig_svg(F.prepared_throne(small=True), px, HL,
                      unit_h=THRONE_UNITS))


def great_throne(px):
    """The prepared throne over the earth (7:49), its cushion in its colour,
    in screen px with its cloud's base at (0, 0)."""
    k = px / THRONE_UNITS
    gx, gy = F.PREPARED_THRONE_GLORY
    return (f'<circle cx="{_fmt(gx * k)}" cy="{_fmt(-gy * k)}" '
            f'r="{_fmt(px * 0.95)}" fill="url(#glory)"/>'
            + fig_svg(F.prepared_throne(cushion=False), px, HL, page=SEA,
                      unit_h=THRONE_UNITS)
            + fig_svg(F.prepared_throne_cushion(), px, CO.CUSHION, page=SEA,
                      unit_h=THRONE_UNITS))


def foot_outline():
    """7:5 not so much as to set his foot on: a foot's outline, empty."""
    return ('<path d="M-6,-2 C-9,-12 -8,-24 -3,-28 C2,-31 7,-26 7,-18 '
            'C7,-10 6,-4 3,-1 C1,1 -4,1 -6,-2Z" fill="none" '
            f'stroke="{rgb(HL)}" stroke-width="1.6" '
            'stroke-dasharray="3 2.4"/>')


def temple_side(px=40):
    """Solomon's house from the south (svg_figures.temple_house, from
    temple.py), px tall."""
    return fig_svg(F.temple_house(), px, SAND, unit_h=TP.HOUSE_HEIGHT)


def tabernacle_east(px=26):
    """The tabernacle from the east, from sanctuary.py in cubits: the court's
    east side with its gate screen, and the tent rising behind it."""
    cw = SN.COURT[3] - SN.COURT[1]
    hh = SN.HANGING_HEIGHT
    t0, t1 = SN.TENT[1], SN.TENT[3]
    g0, g1 = SN.GATE
    mid = cw / 2
    parts = [
        ("fill", [(t0 - mid, 0), (t1 - mid, 0), (t1 - mid, SN.TENT_HEIGHT),
                  (t0 - mid, SN.TENT_HEIGHT)], "hide"),
        ("fill", [(-mid, 0), (mid, 0), (mid, hh), (-mid, hh)], "cloth"),
        ("fill", [(g0 - mid, 0), (g1 - mid, 0), (g1 - mid, hh),
                  (g0 - mid, hh)], "mantle"),
    ]
    for k in range(0, 11):
        x = -mid + k * cw / 10
        parts.append(("line", [(x, 0), (x, hh)], "rule"))
    return fig_svg(parts, px, SAND, unit_h=SN.TENT_HEIGHT)


def calf():
    """7:41 the calf on its plinth, in gold."""
    pl = F.plinth()
    top = F.PLINTH_TOP
    ox = [(kd, ([(x * 0.7, y * 0.7 + top) for x, y in d] if kd != "dot" else
                (d[0] * 0.7, d[1] * 0.7 + top, d[2] * 0.7)), m)
          for kd, d, m in F.ox()]
    return pl + ox


def tomb_glyph():
    return fig_svg(F.tomb(), 26, SAND, unit_h=MAN_H * F.UNIT["tomb"])


def coffin():
    return (f'<rect x="-9" y="-8" width="18" height="7" rx="1.5" '
            f'fill="{rgb(SAND)}" stroke="{rgb(BG)}" stroke-width="1.2"/>')


def dot_svg(col=HL, r=4.2):
    return (f'<circle cx="0" cy="-4" r="{r + 2}" fill="{rgb(BG)}" '
            f'fill-opacity="0.85"/><circle cx="0" cy="-4" r="{r}" '
            f'fill="{rgb(col)}"/>')


# pinned figures: key -> (where, (dx, dy) screen px from it, maker(ink),
# box (x0, y0, x1, y1) round the anchor, the verse it comes in on, when (None:
# a rider brings it), the last verse it is shown, its name)
PINS = {
    "abraham": (UR, (0, 0), lambda i: man(i, staff=True),
                (-22, -FIG_PX, 22, 0), (7, 2), 5.0, (7, 3), "Abraham"),
    "abraham_c": (SHECHEM, (0, 0), lambda i: man(i, staff=True),
                  (-22, -FIG_PX, 22, 0), (7, 4), None, (7, 7), "Abraham"),
    "fathers": (HEBRON, (-14, 0), fathers, (-54, -FIG_PX, 26, 0), (7, 8),
                5.0, (7, 8), None),
    "twelve": (HEBRON, (46, 0), lambda i: band_dots(12, i), (32, -26, 60, 0),
               (7, 8), 11.2, (7, 11), "twelve"),
    "joseph": (ON, (-18, 0), lambda i: man(i), (-40, -FIG_PX, 4, 0), (7, 10),
               1.0, (7, 16), "Joseph"),
    "pharaoh": (ON, (18, 0), lambda i: king(i), (-4, -FIG_PX, 40, 0),
                (7, 10), 5.2, (7, 13), "Pharaoh"),
    "seventy_five": (HEBRON, (0, 0), lambda i: band_dots(75, i, cols=15,
                                                          step=6, r=2.2),
                     (-46, -34, 46, 0), (7, 14), 4.6, (7, 14), None),
    "people": (GOSHEN, (0, 0), lambda i: band_dots(75, i, cols=15, step=6,
                                                   r=2.2),
               (-46, -34, 46, 0), (7, 15), None, (7, 16), None),
    "tomb": (SHECHEM, (16, 0), lambda i: tomb_glyph(), (2, -26, 32, 0),
             (7, 16), 3.2, (7, 16), None),
    "many": (GOSHEN, (0, 0), lambda i: band_dots(150, i, cols=25, step=5,
                                                 r=1.9),
             (-62, -34, 62, 0), (7, 17), 4.2, (7, 35), None),
    "king2": (RAMESES, (0, 0), lambda i: king(i), (-22, -FIG_PX, 22, 0),
              (7, 18), 0.4, (7, 22), "another king"),
    "moses_baby": (GOSHEN, (0, -40), lambda i: dot_svg(HL, 3.4),
                   (-8, -50, 8, -32), (7, 20), 1.2, (7, 20), "Moses"),
    "daughter": (RAMESES, (24, 0), lambda i: fig_svg(F.woman(), FIG_PX * 0.94,
                                                     i),
                 (6, -FIG_PX, 42, 0), (7, 21), 1.0, (7, 21),
                 "Pharaoh's daughter"),
    "moses_court": (RAMESES, (26, 0), lambda i: man(i), (6, -FIG_PX, 46, 0),
                    (7, 22), 0.4, (7, 22), "Moses"),
    "moses_g": (GOSHEN_N, (0, 0), lambda i: man(i), (-22, -FIG_PX, 22, 0),
                (7, 23), None, (7, 28), "Moses"),
    "aaron": (SINAI, (-34, 30), lambda i: man(i, staff=True),
              (-56, -FIG_PX + 30, -12, 30), (7, 40), 1.0, (7, 41), "Aaron"),
    "calf": (SINAI, (8, 30), lambda i: fig_svg(calf(), 34, HL,
                                                unit_h=F.PLINTH_TOP + 60),
             (-12, -6, 28, 30), (7, 41), 1.2, (7, 42), None),
    "moloch": (SINAI, (-40, 34), lambda i: fig_svg(
        F.tent(), 32, SAND, unit_h=MAN_H * F.UNIT["tent"]),
        (-70, 2, -10, 34), (7, 43), 1.4, (7, 43), None),
    "rephan": (SINAI, (30, 6), lambda i: fig_svg(
        F.star(), 26, SAND, unit_h=MAN_H * F.UNIT["star"]),
        (16, -22, 44, 6), (7, 43), 3.0, (7, 43), None),
    "tabernacle": (SINAI, (0, 34), lambda i: tabernacle_east(),
                   (-66, 6, 66, 34), (7, 44), 2.6, (7, 44), "tabernacle"),
    "tabernacle_s": (SHILOH, (0, 0), lambda i: tabernacle_east(),
                     (-66, -26, 66, 0), (7, 45), None, (7, 46), "tabernacle"),
    "joshua": (GILGAL, (26, 0), lambda i: man(i, staff=True),
               (4, -FIG_PX, 48, 0), (7, 45), 3.4, (7, 45), "Joshua"),
    "david": (JERUS, (-30, 0), lambda i: king(i, harp=True),
              (-56, -FIG_PX, 10, 0), (7, 46), 1.2, (7, 46), "David"),
    "solomon": (JERUS, (-34, 0), lambda i: king(i),
                (-56, -FIG_PX, -12, 0), (7, 47), 0.2, (7, 47), "Solomon"),
    "house": (JERUS, (26, 0), lambda i: temple_side(),
              (-8, -40, 74, 0), (7, 47), 0.4, (7, 47), None),
    "house_small": (JERUS, (10, 0), lambda i: temple_side(12),
                    (2, -12, 26, 0), (7, 48), 0.3, (7, 51), None),
    "apostles": (JERUS, (0, 0), lambda i: band_dots(12, HL),
                 (-14, -26, 14, 0), (8, 1), 11.6, (8, 2), "apostles"),
    "burial": (JERUS, (0, -30), lambda i: tomb_glyph(), (-16, -56, 16, -30),
               (8, 2), 0.6, (8, 2), None),
}

# where God appears: the throne marks that stay
MARKS = {
    "ur": (UR, (7, 2), 4.6),
    "egypt": (EGYPT_MARK, (7, 9), 4.8),
    "sinai": (SINAI, (7, 30), 5.4),
}
MARK_LAST = (7, 52)
MARK_PX = 34


# the deliverers rejected: (name, the verse, when)
TALLY = [("Joseph", (7, 9), 3.6), ("Moses", (7, 27), 1.8),
         ("the prophets", (7, 52), 2.4), ("the Righteous One", (7, 52), 5.6),
         ("the council", (7, 51), 7.4)]
TALLY_PULSE = {(7, 35): [("Moses", 1.6)], (7, 39): [("Moses", 2.4)],
               (7, 51): [(n, 5.8) for n, _r, _t in TALLY[:2]]}
TALLY_ON = ((7, 9), (7, 52))
TALLY_ORDER = ["Joseph", "Moses", "the prophets", "the Righteous One",
               "the council"]

# Moses' 120 years: three forties, each filled from (verse, t, fraction)
BAR_ON = ((7, 20), (7, 45))
BAR_FILL = {
    (7, 20): [(0, 2.0, 5.8, 0.0, 0.15)],
    (7, 21): [(0, 0.8, 4.2, 0.15, 0.3)],
    (7, 22): [(0, 0.4, 5.4, 0.3, 0.8)],
    (7, 23): [(0, 0.2, 2.2, 0.8, 1.0)],
    (7, 29): [(1, 1.0, 6.4, 0.0, 0.6)],
    (7, 30): [(1, 0.2, 1.8, 0.6, 1.0)],
    (7, 36): [(2, 4.6, 2.6, 0.0, 1.0)],
}
BAR_NAMES = ("Egypt", "Midian", "wilderness")


# ---------------------------------------------------------------------------
# The shot list
# ---------------------------------------------------------------------------

STAGE = {}


def stage(first, last, **kw):
    for r in span(first, last):
        STAGE[r] = dict(STAGE.get(r, {}), **kw)


PLATE_TOP, PLATE_LINE = 14, (26, 20)


def names(*rows):
    out = []
    for i, r in enumerate(rows):
        text, fill = (r, None) if isinstance(r, str) else r
        if i == 0:
            out.append((text, PLATE_LINE[0], fill or HL, True, False))
        else:
            out.append((text, PLATE_LINE[1], fill or TEXT, False, False))
    return out


CARD = CO.build(P(*JERUS))
S_CARD = CO.S_CARD
BUSH = BU.build(P(*SINAI))
CARDS = [(CARD, CO), (BUSH, BU)]

T_SEIZED = "Stephen Seized — Acts 6"
T_SPEECH = "Stephen’s Speech to the Council — Acts 7"
T_STONED = "Stephen Stoned — Acts 7"
T_SCATTER = "The Assembly Scattered — Acts 8"

MED = fit(30.6, 38.6, 21.6, 36.6, (40, 50, W - 40, H - 30))
MESO = fit(30.3, 37.4, 34.0, 46.4, (30, 50, W - 30, H - 30))
BOX = (200, 60, W - 24, H - 64)     # the frame less the tally and the bar
CANAAN = fit(30.95, 33.0, 34.15, 36.25, (0, 50, W, H - 20))
HEBRON_SHOT = shot(31.60, 35.05, 380)
EG_CAN = fit(29.85, 32.75, 30.9, 35.7, BOX)
GOSHEN_SHOT = shot(30.80, 31.66, 330, sx=W / 2 + 70)
MIDIAN_SHOT = fit(28.2, 31.1, 31.4, 35.4, BOX)
SINAI_SHOT = shot(28.80, 34.20, 260, sx=W / 2 + 60)
EG_SINAI = fit(28.3, 31.0, 31.4, 35.3, BOX)
WILD_SHOT = fit(28.3, 32.0, 31.5, 36.0, BOX)
SINAI_W = shot(29.05, 33.80, 240, sx=W / 2 + 60)
EXILE = fit(28.3, 34.8, 32.8, 45.4, BOX)
JOSHUA_SHOT = fit(28.3, 32.9, 33.5, 36.1, BOX)
JER_SHOT = shot(31.86, 35.20, 640)
HEAVEN = shot(32.8, 36.0, 50, sy=H / 2 + 40)     # the whole speech, 7:48-51
SCATTER = fit(31.25, 32.55, 34.60, 35.90, (0, 50, W, H - 20))
JER_DOT = shot(31.80, 35.22, 900)


def card_cam(ref):
    return CARD.cam(*CO.SHOTS[ref])


stage((6, 8), (6, 15), title=T_SEIZED)
stage((7, 1), (7, 53), title=T_SPEECH)
stage((7, 54), (7, 60), title=T_STONED)
stage((8, 1), (8, 3), title=T_SCATTER)

# the card verses: their shots and camera plans
for _card, _mod in CARDS:
    for _r, _xyz in _mod.SHOTS.items():
        _legs = _mod.LEGS.get(_r)
        if _legs:
            stage(_r, _r, cam=_card.cam(*_xyz),
                  legs=[(k, _card.cam(*x) if x else None, d)
                        for k, x, d in _legs])
        else:
            stage(_r, _r, cam=_card.cam(*_xyz),
                  legs=[("to", _card.cam(*_xyz), _mod.DUR.get(_r, 0.0))])

OPEN = card_cam((6, 8))
# 6:9 up to the eastern sea for the synagogue's men, and back down
stage((6, 9), (6, 9), legs=[("hold", None, 0.2), ("to", MED, 2.6),
                            ("hold", None, 5.2), ("to", card_cam((6, 9)), 2.0)],
      plate=names("synagogue", "Libertines"), plate_at=2.8)
# 7:2 out of the hall to Mesopotamia
stage((7, 2), (7, 2), cam=MESO, legs=[("hold", None, 1.0), ("to", MESO, 3.8)])
stage((7, 3), (7, 4), cam=MESO)
stage((7, 5), (7, 5), cam=CANAAN, legs=[("to", CANAAN, 1.8)])
stage((7, 6), (7, 7), cam=EG_CAN)
stage((7, 6), (7, 6), legs=[("to", EG_CAN, 1.8)], plate=names("400 years"),
      plate_at=7.8)
stage((7, 8), (7, 8), cam=HEBRON_SHOT, legs=[("to", HEBRON_SHOT, 1.8)],
      plate=names("fathers", "Abraham", "Isaac", "Jacob",
                  "twelve patriarchs"), plate_at=4.6)
stage((7, 9), (7, 16), cam=EG_CAN)
stage((7, 9), (7, 9), legs=[("to", EG_CAN, 1.8)])
stage((7, 14), (7, 14), plate=names("75 souls"), plate_at=4.4)
stage((7, 17), (7, 28), cam=GOSHEN_SHOT)
stage((7, 17), (7, 17), legs=[("to", GOSHEN_SHOT, 1.8)])
stage((7, 20), (7, 20), plate=names("3 months"), plate_at=5.0)
stage((7, 29), (7, 29), cam=MIDIAN_SHOT,
      legs=[("hold", None, 0.4), ("to", MIDIAN_SHOT, 2.2)])
stage((7, 30), (7, 30), cam=SINAI_SHOT)
stage((7, 30), (7, 30), legs=[("hold", None, 1.0), ("to", SINAI_SHOT, 2.6)])
stage((7, 32), (7, 32), plate=names("God of the fathers", "Abraham", "Isaac",
                                    "Jacob"), plate_at=1.4)
# 7:35 out of the bush's card to the map, and back to Egypt
stage((7, 35), (7, 35), cam=EG_SINAI,
      legs=[("hold", None, 0.2), ("to", EG_SINAI, 3.4)])
stage((7, 36), (7, 37), cam=WILD_SHOT)
stage((7, 36), (7, 36), legs=[("to", WILD_SHOT, 1.6)],
      plate=names("40 years"), plate_at=6.4)
stage((7, 38), (7, 42), cam=SINAI_W)
stage((7, 38), (7, 38), legs=[("to", SINAI_W, 1.8)])
stage((7, 42), (7, 42), plate=names("the prophets"), plate_at=5.6,
      plate_icon=(F.scroll, {}, F.UNIT["scroll"]))
stage((7, 43), (7, 43), cam=EXILE,
      legs=[("hold", None, 5.0), ("to", EXILE, 2.4)],
      plate=names("Moloch", "Rephan"), plate_at=1.4)
stage((7, 44), (7, 44), cam=SINAI_W, legs=[("to", SINAI_W, 2.2)])
stage((7, 45), (7, 45), cam=JOSHUA_SHOT, legs=[("to", JOSHUA_SHOT, 1.6)])
stage((7, 46), (7, 47), cam=JER_SHOT)
stage((7, 46), (7, 46), legs=[("to", JER_SHOT, 1.8)])
stage((7, 48), (7, 51), cam=HEAVEN)
stage((7, 48), (7, 48), legs=[("to", HEAVEN, 3.4)])
_HALL = card_cam((7, 52))
stage((7, 52), (7, 52), legs=[("hold", None, 6.0), ("to", _HALL, 3.4)])
_OUT = card_cam((7, 60))
stage((8, 1), (8, 1), cam=SCATTER,
      legs=[("hold", None, 2.6), ("to", SCATTER, 3.2)])
stage((8, 2), (8, 2), cam=SCATTER)
stage((8, 3), (8, 3), legs=[("to", card_cam((8, 3)), 2.4)])

NEED_AFTER = 1.4


def plan(ref, cam0):
    st = STAGE[ref]
    cam1 = st["cam"]
    if "legs" in st:
        return Flight(cam0, st["legs"])
    D = cam_duration(cam0, cam1)
    if D:
        D = round(max(0.9, min(D, NARR[ref] - AUDIO_SLACK - NEED_AFTER)), 2)
    return Flight(cam0, [("to", cam1, D)])


# fill in the cameras the stage list left to the legs
for _r in REFS:
    _st = STAGE.setdefault(_r, {})
    if "cam" not in _st and "legs" in _st:
        _st["cam"] = [x for k, x, _d in _st["legs"] if k == "to"][-1]
    assert "cam" in _st, _r


def in_card(cam):
    return cam[0] / S_CARD >= 0.2


# ---------------------------------------------------------------------------
# HUD: title, plate, tally, Moses' years, compass, inset
# ---------------------------------------------------------------------------

SCALE_KM = 100
INSET_RECT = (14, H - 14 - 116, 14 + 176, H - 14)
INSET_BOX = (26.8, 38.6, 24.0, 48.6)
INSET_OFF, INSET_RAMP = 0.165, 0.01   # close-ups only
ICON_PX = 44


def title_of(ref):
    return STAGE[ref]["title"]


def inset_opacity(cam):
    if in_card(cam):
        return 0.0
    la0, la1, _a, _b = INSET_BOX
    hfrac = (H / cam[0] / K) / (la1 - la0)
    return max(0.0, min(1.0, (INSET_OFF - hfrac) / INSET_RAMP))


def plate_lines(ref):
    return STAGE[ref].get("plate") or []


def plate_icon(ref):
    ic = STAGE[ref].get("plate_icon")
    if not ic or not plate_lines(ref):
        return None, 0
    make, kw, _unit = ic
    parts = make(**kw)
    x0, x1, _y0, y1 = F.bbox((parts, 0))
    k = ICON_PX / max(y1, 1)
    return fig_svg(parts, ICON_PX, HL, page=BG, unit_h=y1), (x1 - x0) * k


def plate_rect(ref):
    run = [ref]
    r = prev_ref(ref)
    while r and plate_lines(r) == plate_lines(ref):
        run.append(r)
        r = prev_ref(r)
    wmax, nmax = 0, 0
    for r in run:
        lines = plate_lines(r)
        nmax = max(nmax, len(lines))
        icw = plate_icon(r)[1]
        for text, px, _f, bold, italic in lines:
            box = ink(text, px, bold, italic, "ra")
            wmax = max(wmax, -box[0] + (icw + 12 if icw else 0))
    nmax = max(nmax, 2 if any(plate_icon(r)[0] for r in run) else 1)
    h = 14 + sum(PLATE_LINE[0] if i == 0 else PLATE_LINE[1]
                 for i in range(nmax)) + 14 + 8 * (nmax - 1)
    return (W - 18 - wmax - 14, 4, W - 4, 4 + h)


def plate_texts(ref):
    out = []
    y = PLATE_TOP
    icon, icw = plate_icon(ref)
    if icon:
        x0 = plate_rect(ref)[0] + 14
        out.append(f'<g transform="translate({_fmt(x0 + icw / 2)} '
                   f'{PLATE_TOP + ICON_PX + 4})">{icon}</g>')
    for i, (text, px, fill, bold, italic) in enumerate(plate_lines(ref)):
        a = ' font-weight="bold"' if bold else ""
        a += ' font-style="italic"' if italic else ""
        out.append(f'<text x="{W - 18}" y="{y}" font-size="{px}" '
                   f'fill="{rgb(fill)}" text-anchor="end"{a} '
                   f'dominant-baseline="text-before-edge">{escape(text)}'
                   f'</text>')
        y += (PLATE_LINE[0] if i == 0 else PLATE_LINE[1]) + 8
    return "".join(out)


def plate_svg(ref):
    """A verse's plate comes in at plate_at and goes as the next verse
    opens (plates here belong to their verse)."""
    out = []
    pr = prev_ref(ref)
    if pr and plate_lines(pr) and plate_lines(pr) != plate_lines(ref):
        out.append(f'<g>{fade(0.0, 0.5, out=True)}'
                   + plate_rect_svg(plate_rect(pr)) + plate_texts(pr) + "</g>")
    if plate_lines(ref):
        if pr and plate_lines(pr) == plate_lines(ref):
            out.append(plate_rect_svg(plate_rect(ref)) + plate_texts(ref))
        else:
            t = STAGE[ref].get("plate_at", 0.0)
            out.append(f'<g opacity="0">{fade(t, 0.6)}'
                       + plate_rect_svg(plate_rect(ref)) + plate_texts(ref)
                       + "</g>")
    return "".join(out)


TALLY_X, TALLY_Y, TALLY_STEP = 16, 50, 21


def tally_entries(ref):
    """[(name, t or None if already there, is_new)] shown this verse."""
    out = []
    for name in TALLY_ORDER:
        _n, r, t = next(e for e in TALLY if e[0] == name)
        if IDX[r] < IDX[ref]:
            out.append((name, None))
        elif r == ref:
            out.append((name, t))
    return out


def tally_rect(ref):
    if not within(ref, *TALLY_ON) or not tally_entries(ref):
        return None
    w = max(ink(n, 15, True, False, "la")[2] for n in TALLY_ORDER)
    last = max(TALLY_ORDER.index(n) for n, _t in tally_entries(ref))
    return (8, TALLY_Y - 8, TALLY_X + 24 + w + 10,
            TALLY_Y + 24 + (last + 1) * TALLY_STEP)


def tally_svg(ref, ops):
    if not within(ref, *TALLY_ON) or not tally_entries(ref):
        return ""
    r0 = tally_rect(ref)
    pr = prev_ref(ref)
    first = pr is None or not within(pr, *TALLY_ON) or not tally_entries(pr)
    out = [plate_rect_svg(r0),
           f'<text x="{TALLY_X}" y="{TALLY_Y}" font-size="14" '
           f'fill="{rgb(TEXT_DIM)}" font-style="italic" '
           f'dominant-baseline="text-before-edge">rejected</text>']
    pulses = dict(TALLY_PULSE.get(ref, []))
    for i, name in enumerate(TALLY_ORDER):
        hit = [t for n, t in tally_entries(ref) if n == name]
        if not hit:
            continue
        t = hit[0]
        y = TALLY_Y + 18 + i * TALLY_STEP
        fill = HL if t is not None else TEXT
        cr = ""
        if name == "the Righteous One":
            cr = (f'<g transform="translate({TALLY_X + 6} {y + 16})">'
                  + fig_svg(F.chi_rho(), 16, HL, page=BG,
                            unit_h=F.bbox((F.chi_rho(), 0))[3]) + "</g>")
        el = (f'{cr}<text x="{TALLY_X + 18}" y="{y}" font-size="15" '
              f'fill="{rgb(fill)}" dominant-baseline="text-before-edge"'
              f'{" font-weight=\"bold\"" if t is not None else ""}>'
              f'{escape(name)}</text>')
        if t is not None:
            el = f'<g opacity="0">{fade(t, 0.6)}{el}</g>'
        if name in pulses:
            bw = ink(name, 15, False, False, "la")[2]
            el += (f'<rect x="{TALLY_X + 12}" y="{y - 3}" width="{bw + 12}" '
                   f'height="22" rx="6" fill="none" stroke="{rgb(HL)}" '
                   f'stroke-width="1.6" opacity="0">'
                   f'<animate attributeName="opacity" values="0;1;1;0" '
                   f'keyTimes="0;0.3;0.6;1" begin="{pulses[name]:.2f}s" '
                   f'dur="1.0s" fill="freeze"/></rect>')
        out.append(el)
    body = "".join(out)
    if first:
        body = f'<g opacity="0">{fade(0.0, 0.6)}{body}</g>'
    return (f'<g opacity="{ops[0]}">{ops[1]}{body}</g>')


BAR = (318, H - 44, 706, H - 18)       # x0, y0, x1, y1 of the three bars


def bar_rect(ref):
    if not within(ref, *BAR_ON):
        return None
    x0, y0, x1, y1 = BAR
    return (x0 - 10, y0 - 22, x1 + 10, y1 + 6)


def bar_state(ref):
    """Each forty's fill as the verse opens."""
    fill = [0.0, 0.0, 0.0]
    for r in REFS:
        if r == ref:
            break
        for seg, _t, _d, _a, b in BAR_FILL.get(r, []):
            fill[seg] = b
    return fill


def bar_svg(ref, ops):
    if not within(ref, *BAR_ON):
        return ""
    x0, y0, x1, y1 = BAR
    w = (x1 - x0 - 16) / 3
    fill = bar_state(ref)
    now = {seg: (t, d, a, b) for seg, t, d, a, b in BAR_FILL.get(ref, [])}
    out = [plate_rect_svg(bar_rect(ref))]
    for k in range(3):
        sx = x0 + k * (w + 8)
        out.append(f'<rect x="{_fmt(sx)}" y="{y0}" width="{_fmt(w)}" '
                   f'height="{y1 - y0}" rx="3" fill="none" '
                   f'stroke="{rgb(SAND_DIM)}" stroke-width="1.4"/>')
        f0 = fill[k]
        anim = ""
        f1 = f0
        if k in now:
            t, d, a, b = now[k]
            f1 = b
            anim = (f'<animate attributeName="width" '
                    f'values="{_fmt(w * a)};{_fmt(w * b)}" begin="{t:.2f}s" '
                    f'dur="{d:.2f}s" fill="freeze"/>')
        out.append(f'<rect x="{_fmt(sx)}" y="{y0}" width="{_fmt(w * f0)}" '
                   f'height="{y1 - y0}" rx="3" fill="{rgb(SAND)}" '
                   f'fill-opacity="0.85">{anim}</rect>')
        lit = k in now
        out.append(f'<text x="{_fmt(sx + 4)}" y="{y0 - 4}" font-size="13" '
                   f'fill="{rgb(HL if lit else TEXT_DIM)}" '
                   f'{"font-weight=\"bold\" " if lit else ""}'
                   f'font-style="italic">{BAR_NAMES[k]}</text>')
        if f1 >= 1.0:
            t40 = (now[k][0] + now[k][1]) if k in now and f0 < 1.0 else None
            el = (f'<text x="{_fmt(sx + w / 2)}" y="{(y0 + y1) / 2:.1f}" '
                  f'font-size="15" font-weight="bold" fill="{rgb(BG)}" '
                  f'text-anchor="middle" dominant-baseline="central">40</text>')
            out.append(f'<g opacity="0">{fade(t40, 0.4)}{el}</g>'
                       if t40 is not None else el)
    pr = prev_ref(ref)
    body = "".join(out)
    if pr is None or not within(pr, *BAR_ON):
        body = f'<g opacity="0">{fade(1.6, 0.6)}{body}</g>'
    return f'<g opacity="{ops[0]}">{ops[1]}{body}</g>'


def bar_out(ref):
    """The bar and tally leave on the verse after their last."""
    pr = prev_ref(ref)
    if pr and within(pr, *BAR_ON) and not within(ref, *BAR_ON):
        return (f'<g>{fade(0.0, 0.6, out=True)}' + bar_svg(pr, ("1", ""))
                + "</g>")
    return ""


def hud_rects(ref, cam):
    hud = [("title", title_rect(title_of(ref))),
           ("compass", compass_rect(PROJ, min(cam[0], 6.0), SCALE_KM))]
    if plate_lines(ref):
        hud.append(("plate", plate_rect(ref)))
    if tally_rect(ref):
        hud.append(("tally", tally_rect(ref)))
    if bar_rect(ref):
        hud.append(("bar", bar_rect(ref)))
    if inset_opacity(cam) > 0.05:
        hud.append(("inset", INSET_RECT))
    return hud


def hud_svg(ref, fl, zs):
    out = [title_svg(title_of(ref), TEXT), plate_svg(ref)]
    vals = [f"{1.0 - card_op(z):.2f}" for z in zs]
    ops = (vals[0], fl._anim("opacity", vals))
    out.append(tally_svg(ref, ops))
    out.append(bar_svg(ref, ops))
    out.append(bar_out(ref))
    if max(float(v) for v in vals) > 0:
        capped = Flight(fl.cam0, [])
        capped.cams = [(min(c[0], 6.0), c[1], c[2]) for c in fl.cams]
        capped.static, capped.pure_pan = fl.static, fl.pure_pan
        capped.dur = fl.dur
        out.append(f'<g opacity="{vals[0]}">{fl._anim("opacity", vals)}'
                   + compass_scale_svg(capped, PROJ, SCALE_KM) + "</g>")
    return "".join(out)


INSET_TOL = 0.12


def inset_svg(ref, fl):
    x0, y0, x1, y1 = INSET_RECT
    ops = [f"{inset_opacity(c):.2f}" for c in fl.cams]
    if max(float(o) for o in ops) == 0:
        return ""
    la0, la1, lo0, lo1 = INSET_BOX
    iw, ih = x1 - x0 - 8, y1 - y0 - 8
    k = min(iw / ((lo1 - lo0) * EFF), ih / (la1 - la0))
    ox = x0 + 4 + (iw - (lo1 - lo0) * EFF * k) / 2
    oy = y0 + 4 + (ih - (la1 - la0) * k) / 2

    def ip(lat, lon):
        return (ox + (lon - lo0) * EFF * k, oy + (la1 - lat) * k)
    out = [f'<g opacity="{ops[0]}">{fl._anim("opacity", ops)}',
           f'<defs><clipPath id="insetclip"><rect x="{x0}" y="{y0}" '
           f'width="{x1 - x0}" height="{y1 - y0}" rx="6"/></clipPath></defs>',
           f'<g clip-path="url(#insetclip)">',
           f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" '
           f'fill="{rgb(SEA)}"/>']
    for ring in land_rings():
        out.append(poly_el([ip(a, b) for a, b in
                            simplify_ring(ring, INSET_TOL)], fill=LAND,
                           closed=True))
    for ring in (RED_SEA_RING, GULF_RING):
        out.append(poly_el([ip(a, b) for a, b in
                            simplify_ring(ring, INSET_TOL)], fill=SEA,
                           closed=True))
    for ring in ISLANDS:
        sr = simplify_ring(ring, INSET_TOL)
        if len(sr) > 2:
            out.append(poly_el([ip(a, b) for a, b in sr], fill=LAND,
                               closed=True))
    out.append(inset_view_rect(fl, PROJ, ip, HL, min_px=6))
    out.append("</g>")
    out.append(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" '
               f'height="{y1 - y0}" rx="6" fill="none" '
               f'stroke="{rgb(SAND_DIM)}" stroke-width="1.5"/>')
    out.append("</g>")
    return "".join(out)


# ---------------------------------------------------------------------------
# Stroke classes
# ---------------------------------------------------------------------------

ROSE = (196, 128, 104)
CLS_PX = {"coast": 1.6, "lake": 1.0, "river": 1.4, "story": 2.6,
          "story_trace": 4.0, "story_let": 4.0, "word": 2.0,
          "word_trace": 2.4, "promise": 2.0, "ahead": 1.4, "scatter": 2.0}
CLS_DASH = {"story": (9, 5), "word": (5, 5), "word_trace": (5, 5),
            "promise": (6, 5), "ahead": (6, 5)}
CLS_EXTRA = {}
LET_GO = 0.8
DRAW_ORDER = ("lake", "river", "promise", "ahead", "story", "story_let",
              "word", "word_trace", "scatter", "story_trace")


def emit(fl, name, els, extra=""):
    return emit_class(fl, CLS_PX[name], els,
                      CLS_EXTRA.get(name, "") + extra, CLS_DASH.get(name))


class Beats:
    def __init__(self):
        self.cls = {k: [] for k in CLS_PX}
        self.pins, self.units = [], []
        self.obstacles, self.overlay, self.ends, self.qc = [], [], [], []
        self.defs = []


def at_rest(cam1, lat, lon):
    return to_screen(cam1, P(lat, lon))


def pin_label(key, text, anchor, cam1, box, fill=HL, bold=True, prio=1,
              new=True, must=True):
    ax, ay = at_rest(cam1, *anchor)
    x0, y0, x1, _y1 = box
    cands = []
    for sx, sy, code in ((ax + x1 + 2, ay + y0 * 0.55, "r"),
                         (ax + x0 - 2, ay + y0 * 0.55, "l"),
                         (ax + (x0 + x1) / 2, ay + y0 - 2, "a"),
                         (ax + x1 + 2, ay + y0 * 0.2, "r"),
                         (ax + x0 - 2, ay + y0 * 0.2, "l"),
                         (ax + (x0 + x1) / 2, ay + 4, "b")):
        la, lo = PROJ.unproject(cam1, sx, sy)
        cands.append((la, lo, code))
    return Unit("pin_" + key, text, [S_CUR if bold else S_OTHER], fill,
                bold=bold, italic=not bold, cands=cands, prio=prio, new=new,
                must=must)


def pin_box_rest(cam1, anchor, box):
    """A pin's box (relative to its anchor, offset included) at rest."""
    ax, ay = at_rest(cam1, *anchor)
    x0, y0, x1, y1 = box
    return (ax + x0, ay + y0, ax + x1, ay + y1)


def moved(inner, off):
    if off == (0, 0):
        return inner
    return f'<g transform="translate({off[0]} {off[1]})">{inner}</g>'


def road_svg_now(b, fl, key, ink_=HL):
    pts, _on, (t0, d), _last, kind = ROADS[key]
    w = PS(pts)
    cls = "story_trace" if kind == "story" else "word_trace"
    col = ink_ + (242,) if kind == "story" else TEXT
    b.cls[cls].append(traced_el(w, col, t0, d)[0])
    b.ends.append(t0 + d)
    return w


def beats(ref, fl, cam1, t_land):
    b = Beats()
    i = IDX[ref]
    pr = prev_ref(ref)

    # -- Israel's roads ---------------------------------------------------
    for key, (pts, on, (t0, d), last, kind) in ROADS.items():
        st = road_state(key, ref)
        if st is None:
            if pr and road_state(key, pr) is not None:
                # it leaves with the verse after its last
                w = PS(pts)
                cls = "story" if kind == "story" else "word"
                col = ROSE if kind == "story" else TEXT_DIM
                b.cls[cls].append(poly_el(w, stroke=col)[:-2] + ">"
                                  + fade(0.0, 0.6, out=True) + "</polyline>")
            continue
        w = PS(pts)
        b.qc.append((w, "route", key))
        if st == "now":
            road_svg_now(b, fl, key)
        elif kind == "story":
            b.cls["story"].append(poly_el(w, stroke=ROSE))
            if on == pr:
                b.cls["story_let"].append(
                    poly_el(w, stroke=HL + (242,))[:-2] + ">"
                    + fade(0.0, LET_GO, out=True) + "</polyline>")
        else:
            b.cls["word"].append(poly_el(w, stroke=TEXT_DIM))

    # 6:9 the men of the synagogue and where they came from: while the
    # camera holds over the eastern sea (2.8-8.0 s) their places light, and
    # a line runs from each to Jerusalem
    if ref == (6, 9):
        b.overlay.append(synagogue_overlay())
        b.ends.append(8.6)

    # 7:3 the road ahead from Ur, through Haran, into the land: dashed
    if ref == (7, 3):
        for key in ("ur_haran", "haran_canaan"):
            w = PS(ROADS[key][0])
            b.cls["ahead"].append(poly_el(w, stroke=SAND_DIM)[:-2] + ' opacity="0">'
                                  + fade(1.4, 0.8) + "</polyline>")
        b.ends.append(2.2)
    if ref == (7, 4):
        for key in ("ur_haran", "haran_canaan"):
            w = PS(ROADS[key][0])
            b.cls["ahead"].append(poly_el(w, stroke=SAND_DIM))

    # 7:5 the land promised; 7:7 out of Egypt, to serve me in this place
    if ref == (7, 5):
        w = PS(PROMISE)
        b.cls["promise"].append(poly_el(w, stroke=SAND)[:-2] + ' opacity="0">'
                                + fade(5.4, 1.2) + "</polyline>")
        b.ends.append(6.6)
    elif within(ref, (7, 6), (7, 7)):
        b.cls["promise"].append(poly_el(PS(PROMISE), stroke=SAND))
    if ref == (7, 7):
        w = PS([ON, (30.55, 32.20), (30.90, 33.40), BEERSHEBA, (31.60, 35.00)])
        b.cls["word_trace"].append(traced_el(w, TEXT, 4.4, 1.6)[0])
        b.ends.append(6.0)

    # -- riders: the people and the person at the head of a road ----------
    def ride(key, inner, t_show=None, t_hide=None):
        pts, _on, (t0, d), _l, _k = ROADS[key]
        b.pins.append(rider(fl, PS(pts), t0, d, inner, t_show=t_show,
                            t_hide=t_hide))
    if ref == (7, 4):
        ride("ur_haran", man(TEXT, staff=True), t_hide=5.6)
        ride("haran_canaan", man(TEXT, staff=True), t_show=5.6)
    elif ref == (7, 9):
        ride("joseph", dot_svg(HL, 3.6))
    elif ref == (7, 12):
        ride("grain1", band_dots(10))
    elif ref == (7, 13):
        ride("grain2", band_dots(10))
    elif ref == (7, 15):
        ride("going_down", band_dots(75, cols=15, step=6, r=2.2))
    elif ref == (7, 16):
        ride("bones", coffin(), t_hide=3.0)
    elif ref == (7, 21):
        ride("to_court", dot_svg(HL, 3.4))
    elif ref == (7, 23):
        ride("to_people", man(TEXT))
    elif ref == (7, 29):
        ride("flight", man(TEXT))
    elif ref == (7, 30):
        ride("to_horeb", man(TEXT))
    elif ref == (7, 35):
        ride("to_egypt", man(TEXT))
    elif ref == (7, 36):
        ride("exodus", band_dots(12), t_hide=4.6)
        ride("wilderness", band_dots(12), t_show=4.6)
    elif ref == (7, 45):
        ride("tent_in", tabernacle_east(), t_hide=5.0)
        ride("to_shiloh", tabernacle_east(), t_show=5.0)
    # Moses, at Midian (7:29-30 his sons) and Sinai (7:30-34) and Egypt (7:35)
    if within(ref, (7, 30), (7, 34)) and ref != (7, 30):
        b.pins.append(pin(fl, P(*SINAI), moved(man(TEXT), (-26, 0))))
    if ref == (7, 29):
        for k in range(2):
            b.pins.append(pin(fl, P(*MIDIAN), moved(lift_in(
                fig_svg(F.child(), FIG_PX * 0.62, TEXT), 5.6 + k * 0.3),
                (22 + k * 18, 0))))
        b.ends.append(6.5)
        ax, ay = at_rest(cam1, *MIDIAN)
        b.obstacles.append(("sons", (ax - 24, ay - FIG_PX, ax + 52, ay)))
    if ref == (7, 30):
        for k in range(2):
            b.pins.append(pin(fl, P(*MIDIAN), moved(
                f'<g>{fade(0.6, 0.6, out=True)}'
                + fig_svg(F.child(), FIG_PX * 0.62, TEXT) + "</g>",
                (22 + k * 18, 0))))

    # -- the bush on the map (7:30, and 7:31 until the card covers it) ---
    if within(ref, (7, 30), (7, 34)):
        bush = fig_svg(F.herb(), 40, HL, unit_h=MAN_H * F.UNIT["herb"])
        bush = (f'<circle cx="0" cy="-20" r="30" fill="url(#glory)"/>'
                + bush)
        inner = lift_in(bush, 7.4) if ref == (7, 30) else bush
        b.pins.append(pin(fl, P(*SINAI), moved(inner, (24, 0))))
        ax, ay = at_rest(cam1, *SINAI)
        b.obstacles.append(("bush", (ax + 4, ay - 46, ax + 46, ay)))
        if ref == (7, 30):
            b.ends.append(8.0)

    # -- pinned figures -----------------------------------------------------
    for key, (where, off, make, box, r_in, t_in, r_last, name) in PINS.items():
        if i < IDX[r_in]:
            continue
        last = IDX[r_last]
        if i > last + 1:
            continue
        anchor_box = pin_box_rest(cam1, where, box)
        if i == last + 1:
            b.pins.append(pin(fl, P(*where), moved(
                f'<g>{fade(0.0, 0.6, out=True)}' + make(TEXT) + "</g>", off)))
            continue
        if ref == r_in and t_in is not None:
            inner = lift_in(make(TEXT), t_in)
            b.ends.append(t_in + 0.6)
        elif ref == r_in:
            # a rider brings it: it appears where the rider stops
            rd = next(k for k, v in ROADS.items() if v[1] == ref and
                      math.dist(v[0][-1], where) < 1e-6)
            t_end = sum(ROADS[rd][2])
            inner = (f'<g opacity="0"><set attributeName="opacity" to="1" '
                     f'begin="{t_end:.2f}s"/>{make(TEXT)}</g>')
        else:
            inner = make(TEXT)
        b.pins.append(pin(fl, P(*where), moved(inner, off)))
        ax, ay = at_rest(cam1, *where)
        if anchor_box[0] < ax + 9 and ax - 9 < anchor_box[2] and                 anchor_box[3] > ay - 9:
            anchor_box = anchor_box[:3] + (ay - 9,)
        b.obstacles.append(("pin_" + key, anchor_box))
        if name:
            ax, ay = at_rest(cam1, *where)
            la, lo = PROJ.unproject(cam1, ax + off[0], ay + off[1])
            rel = (box[0] - off[0], box[1] - off[1], box[2] - off[0],
                   box[3] - off[1])
            u = pin_label(key, name, (la, lo), cam1, rel,
                          fill=HL if ref == r_in else TEXT,
                          bold=ref == r_in, prio=1 if ref == r_in else 3,
                          new=ref == r_in, must=ref == r_in)
            if ref == r_in:
                u.t_want = (t_in + 0.3) if t_in is not None else (
                    sum(ROADS[next(k for k, v in ROADS.items()
                                   if v[1] == ref and
                                   math.dist(v[0][-1], where) < 1e-6)][2]))
            b.units.append(u)

    # Moses at Goshen (7:24-28): the Egyptian, the brothers fighting
    if ref == (7, 24):
        eg = (f'<g opacity="0">{fade(1.6, 0.5)}{fade(5.4, 0.8, out=True)}'
              + fig_svg(F.man(), FIG_PX * 0.9, SAND_DIM) + "</g>")
        isr = (f'<g opacity="0">{fade(1.6, 0.5)}'
               + fig_svg(F.man(), FIG_PX * 0.9, SAND) + "</g>")
        b.pins.append(pin(fl, P(*GOSHEN_N), moved(eg, (34, 0))))
        b.pins.append(pin(fl, P(*GOSHEN_N), moved(isr, (-34, 0))))
        b.ends.append(6.2)
    if within(ref, (7, 25), (7, 25)):
        b.pins.append(pin(fl, P(*GOSHEN_N), moved(
            f'<g>{fade(0.0, 0.6, out=True)}'
            + fig_svg(F.man(), FIG_PX * 0.9, SAND) + "</g>", (-34, 0))))
    if within(ref, (7, 26), (7, 28)):
        arms = {(7, 26): ("down", "down"), (7, 27): ("point_r", "down"),
                (7, 28): ("point_r", "down")}[ref]
        for k, (dx, fl_) in enumerate(((-40, 1), (40, -1))):
            body = fig_svg(F.man(arms=arms[k]), FIG_PX * 0.9, SAND, flip=fl_)
            if ref == (7, 26):
                body = lift_in(body, 2.4 + k * 0.2)
            b.pins.append(pin(fl, P(*GOSHEN_N), moved(body, (dx, 0))))
        if ref == (7, 26):
            b.ends.append(3.2)
        ax, ay = at_rest(cam1, *GOSHEN_N)
        b.obstacles.append(("brothers", (ax - 66, ay - FIG_PX, ax + 66, ay)))

    # -- throne marks where God appears -----------------------------------
    if within(ref, (7, 2), MARK_LAST):
        b.defs.append(GLORY_DEFS)
    for key, (where, r_on, t) in MARKS.items():
        if i < IDX[r_on] or i > IDX[MARK_LAST]:
            continue
        mk = throne_mark(MARK_PX)
        if ref == r_on:
            mk = lift_in(mk, t, 0.9)
            b.ends.append(t + 0.9)
        b.pins.append(pin(fl, P(*where), moved(mk, (0, -10))))
        ax, ay = at_rest(cam1, *where)
        b.obstacles.append(("mark_" + key, (ax - 22, ay - 10 - MARK_PX - 4,
                                            ax + 22, ay - 10)))
        if ref == (7, 48):
            b.overlay.append(screen_ring((ax, ay - 20), 3.4, 10, 46, 1.0, HL))
            b.ends.append(4.4)
        if ref == (7, 35) and key == "sinai":
            b.overlay.append(screen_ring((ax, ay - 20), 9.6, 10, 40, 1.0, HL))
            b.ends.append(10.6)
        if ref == (7, 38) and key == "sinai":
            b.overlay.append(screen_ring((ax, ay - 20), 5.0, 10, 40, 1.0, HL))
            b.ends.append(6.0)

    # 7:5 a foot's breadth: the outline of a foot, never filled
    if ref == (7, 5):
        b.pins.append(pin(fl, P(*SHECHEM), moved(lift_in(foot_outline(), 2.6),
                                                 (30, 0))))
        ax, ay = at_rest(cam1, *SHECHEM)
        b.obstacles.append(("foot", (ax + 20, ay - 32, ax + 40, ay + 2)))
        b.ends.append(3.2)

    # 7:11 famine over Egypt and Canaan: the land darkens
    for k, (la, lo, rx, ry) in enumerate(((30.0, 31.0, 1.5, 1.1),
                                          (31.7, 35.0, 0.9, 1.0))):
        if not within(ref, (7, 11), (7, 14)):
            continue
        x, y = P(la, lo)
        anim = fade(1.2 + k * 0.8, 1.2) if ref == (7, 11) else ""
        op = ' opacity="0"' if ref == (7, 11) else ""
        b.cls["coast"].append(
            f'<ellipse cx="{_fmt(x)}" cy="{_fmt(y)}" rx="{_fmt(rx * K * EFF)}" '
            f'ry="{_fmt(ry * K)}" fill="url(#famine)" '
            f'stroke="none"{op}>{anim}</ellipse>')
        b.defs.append(FAMINE_DEFS)
    if ref == (7, 15):
        for la, lo, rx, ry in ((30.0, 31.0, 1.5, 1.1), (31.7, 35.0, 0.9, 1.0)):
            x, y = P(la, lo)
            b.cls["coast"].append(
                f'<ellipse cx="{_fmt(x)}" cy="{_fmt(y)}" '
                f'rx="{_fmt(rx * K * EFF)}" ry="{_fmt(ry * K)}" '
                f'fill="url(#famine)" stroke="none">'
                f'{fade(0.0, 0.8, out=True)}</ellipse>')
            b.defs.append(FAMINE_DEFS)
    if ref == (7, 11):
        b.ends.append(3.2)

    # 7:12-13 the two journeys numbered
    for key, num, r in (("grain1", "1", (7, 12)), ("grain2", "2", (7, 13))):
        if within(ref, r, (7, 13)):
            pts = ROADS[key][0]
            mid = pts[len(pts) // 2]
            xy = at_rest(cam1, *mid)
            t = sum(ROADS[key][2]) if ref == r else None
            el = (f'<circle cx="{xy[0]:.1f}" cy="{xy[1]:.1f}" r="10" '
                  f'fill="{rgb(BG)}" stroke="{rgb(ROSE)}" stroke-width="1.5"/>'
                  f'<text x="{xy[0]:.1f}" y="{xy[1]:.1f}" font-size="13" '
                  f'font-weight="bold" fill="{rgb(HL)}" text-anchor="middle" '
                  f'dominant-baseline="central">{num}</text>')
            if t is not None:
                el = f'<g opacity="0">{fade(t, 0.4)}{el}</g>'
                b.ends.append(t + 0.4)
            b.overlay.append(el)
            b.obstacles.append(("num" + num, (xy[0] - 12, xy[1] - 12,
                                              xy[0] + 12, xy[1] + 12)))
    # 7:13 Joseph made known: a ring round him; Pharaoh learns of them
    if ref == (7, 13):
        for where, off, t in ((ON, (-18, -30), 2.6), (ON, (18, -30), 4.6)):
            ax, ay = at_rest(cam1, *where)
            b.overlay.append(screen_ring((ax + off[0], ay + off[1]), t, 12, 40,
                                         0.9, HL))
        b.ends.append(5.5)
    # 7:17 they grew and multiplied (the 75 give way to the many)
    # 7:20 Moses born: a light among them (PINS); 7:22 mighty in words and
    # works; 7:36 wonders in Egypt, at the Red Sea, in the wilderness
    if ref == (7, 36):
        for where, t in ((RAMESES, 2.8), (S["crossing"], 4.2)):
            ax, ay = at_rest(cam1, *where)
            b.overlay.append(screen_ring((ax, ay), t, 8, 34, 0.9, HL))
        b.ends.append(5.1)
    # 7:37 a prophet like me: the Chi-Rho at Jerusalem, for a moment
    if ref == (7, 37):
        cr = fig_svg(F.chi_rho(), 40, HL, unit_h=F.bbox((F.chi_rho(), 0))[3])
        b.pins.append(pin(fl, P(*JERUS), f'<g opacity="0">{fade(5.4, 0.8)}'
                          f'{fade(7.6, 0.8, out=True)}{cr}</g>'))
        b.ends.append(8.4)
    # 7:39 turned back in their hearts to Egypt (ROADS); 7:41 the calf
    # (PINS) and its sacrifice
    if ref == (7, 41):
        alt = fig_svg(F.altar("stone", fire=True), 26, SAND,
                      unit_h=MAN_H * F.UNIT["altar_stone"])
        b.pins.append(pin(fl, P(*SINAI), moved(lift_in(alt, 3.2), (40, 30))))
        b.ends.append(3.8)
    # 7:42 given up to serve the army of the sky: stars come out over the
    # wilderness
    if ref in ((7, 42),):
        import random
        rnd = random.Random(742)
        for k in range(26):
            x = rnd.uniform(90, W - 90)
            y = rnd.uniform(70, H * 0.55)
            t = 2.4 + rnd.uniform(0, 2.0)
            r = rnd.uniform(1.2, 2.4)
            b.overlay.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" '
                             f'fill="{rgb(TEXT)}" opacity="0">'
                             f'{fade(t, 0.6)}</circle>')
        b.ends.append(5.0)
    if ref == (7, 43):
        import random
        rnd = random.Random(742)
        for k in range(26):
            x = rnd.uniform(90, W - 90)
            y = rnd.uniform(70, H * 0.55)
            rnd.uniform(0, 2.0)
            r = rnd.uniform(1.2, 2.4)
            b.overlay.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" '
                             f'fill="{rgb(TEXT)}">{fade(0.0, 0.8, out=True)}'
                             f'</circle>')

    # 7:49 heaven my throne, the earth my footstool
    if within(ref, (7, 49), (7, 51)):
        x, y, px = W * 0.30, H * 0.47, 210
        th = great_throne(px)
        el = f'<g transform="translate({x:.0f} {y:.0f})">{th}</g>'
        heaven = (f'<text x="{x:.0f}" y="{y - px * 1.02:.0f}" font-size="20" '
                  f'fill="{rgb(HL)}" font-style="italic" text-anchor="middle">'
                  f'heaven</text>')
        if ref == (7, 49):
            el = f'<g opacity="0">{fade(1.0, 1.2)}{el}</g>'
            heaven = f'<g opacity="0">{fade(1.6, 0.6)}{heaven}</g>'
            b.ends.append(2.2)
        elif ref == (7, 51):
            el = f'<g>{fade(0.6, 1.0, out=True)}{el}</g>'
            heaven = f'<g>{fade(0.6, 1.0, out=True)}{heaven}</g>'
        b.overlay.append(el + heaven)
        b.obstacles.append(("great_throne", (x - px * 0.7, y - px * 1.1,
                                             x + px * 0.5, y + 4)))
        if ref != (7, 51):
            b.units.append(Unit("earth", "earth", [S_AREA], HL, italic=True,
                                cands=[(29.6, 40.8, "c"), (30.4, 39.6, "c"),
                                       (29.0, 42.0, "c")], prio=1, new=True,
                                must=True))
            if ref == (7, 49):
                b.units[-1].t_want = 3.6
    # the little house at Jerusalem, at 7:49 "what kind of house"
    if ref == (7, 49):
        ax, ay = at_rest(cam1, *JERUS)
        b.overlay.append(screen_ring((ax + 14, ay - 6), 5.6, 8, 30, 0.9, HL))
        b.ends.append(6.5)

    # 8:1 scattered through Judea and Samaria, all but the apostles
    if ref == (8, 1):
        import random
        rnd = random.Random(81)
        ax, ay = at_rest(cam1, *JERUS)
        b.overlay.append(screen_ring((ax, ay), 6.0, 8, 60, 1.0, HL))
        for k in range(18):
            la = rnd.uniform(31.30, 32.50)
            lo = rnd.uniform(34.75, 35.45)
            if math.dist((la, lo), JERUS) < 0.12:
                continue
            path = PS([JERUS, ((JERUS[0] + la) / 2 + rnd.uniform(-.05, .05),
                               (JERUS[1] + lo) / 2), (la, lo)])
            t = 7.2 + rnd.uniform(0, 1.6)
            b.pins.append(rider(fl, path, t, 2.0, band_dots(1)))
        b.ends.append(10.8)
    if ref == (8, 2):
        import random
        rnd = random.Random(81)
        for k in range(18):
            la = rnd.uniform(31.30, 32.50)
            lo = rnd.uniform(34.75, 35.45)
            if math.dist((la, lo), JERUS) < 0.12:
                continue
            rnd.uniform(-.05, .05)
            rnd.uniform(0, 1.6)
            b.pins.append(pin(fl, P(la, lo), band_dots(1)))
    return b


SYN_HOLD = (2.8, 8.0)      # 6:9: the camera rests over the eastern sea
SYN_PLACES = [             # (name, lat, lon, when, side, is a land)
    ("Jerusalem", *JERUS, 2.8, "r", False),
    ("Cyrene", *_ne("cyrene"), 4.4, "r", False),
    ("Alexandria", *_ne("alexandria"), 5.6, "l", False),
    ("Cilicia", J.PLACES["tarsus"].lat, J.PLACES["tarsus"].lon, 7.0, "a",
     True),
    ("Asia", J.PLACES["ephesus"].lat, J.PLACES["ephesus"].lon, 7.8, "r",
     True),
]


def synagogue_overlay():
    """6:9 in screen space at the MED rest: each place's dot and name, and
    a line to Jerusalem, in on the word and out as the camera goes back
    down. A name for a land (Cilicia, Asia) is set in capitals."""
    t_out = SYN_HOLD[1] - 0.2
    jx, jy = to_screen(MED, P(*JERUS))
    out = []
    for name, la, lo, t, side, land in SYN_PLACES:
        x, y = to_screen(MED, P(la, lo))
        g = []
        if name != "Jerusalem":
            el, _L = traced_el([(x, y), (jx, jy)], HL + (200,), t + 0.2, 0.9)
            g.append(f'<g stroke-width="1.8" stroke-dasharray="5 4">{el}</g>')
        g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{rgb(BG)}" '
                 f'fill-opacity="0.85"/><circle cx="{x:.1f}" cy="{y:.1f}" '
                 f'r="4" fill="{rgb(HL)}"/>')
        text = name.upper() if land else name
        dx, dy, anc = {"r": (10, 5, "start"), "l": (-10, 5, "end"),
                       "a": (0, -12, "middle")}[side]
        g.append(f'<text x="{x + dx:.1f}" y="{y + dy:.1f}" font-size="18" '
                 f'font-weight="bold" fill="{rgb(HL)}" text-anchor="{anc}" '
                 f'stroke="{rgb(BG)}" stroke-width="4" stroke-opacity="0.8" '
                 f'paint-order="stroke">{escape(text)}</text>')
        out.append(f'<g opacity="0">{fade(t, 0.5)}'
                   f'{fade(t_out, 0.5, out=True)}{"".join(g)}</g>')
    return "".join(out)


# ---------------------------------------------------------------------------
# Labels
# ---------------------------------------------------------------------------

CROWD_PX = 30


def units(ref):
    cam = STAGE[ref]["cam"]
    U = []
    for key, (name, la, lo, r0, r1, lit) in PLACES.items():
        if not place_shown(key, ref):
            continue
        is_lit = ref in lit
        if key == "jerusalem" and not is_lit:
            U.append(Unit(key, name, [S_OTHER], TEXT,
                          cands=[(la, lo, c) for c in "rlab"], dot=SAND,
                          prio=3))
            continue
        if is_lit:
            u = Unit(key, name, [S_CUR], HL, bold=True,
                     cands=[(la, lo, c) for c in "rlab"], dot=HL, prio=1,
                     new=True, must=True, min_px=18)
            u.t_want = LIT_AT.get((key, ref), None)
            if u.t_want is None:
                del u.t_want
            U.append(u)
        else:
            U.append(Unit(key, name, [S_OTHER], TEXT_DIM,
                          cands=[(la, lo, c) for c in "rlab"], dot=SAND_DIM,
                          prio=4))
    for key, (name, cands, r0, r1, lit) in REGIONS.items():
        if not within(ref, r0, r1):
            continue
        is_lit = ref in lit
        u = Unit("rg_" + key, name, [S_AREA, S_OTHER],
                 HL if is_lit else TEXT_DIM, bold=is_lit,
                 cands=[(a, c, "c") for a, c in cands],
                 prio=2 if is_lit else 6, new=is_lit, must=is_lit)
        if is_lit and (key, ref) in LIT_AT:
            u.t_want = LIT_AT[(key, ref)]
        U.append(u)
    for key, (name, cands) in WATERS.items():
        if key == "great_sea" and within(ref, (7, 49), (7, 51)):
            continue                      # the throne stands over it
        lit = key == "red_sea" and ref == (7, 36)
        u = Unit("w_" + key, name, [S_AREA, S_OTHER],
                 HL if lit else WATER_TXT, italic=True, bold=lit, gmax=1.25,
                 cands=[(a, c, "c") for a, c in cands], prio=2 if lit else 7,
                 in_sea=True, new=lit)
        if lit:
            u.t_want = 4.2
        U.append(u)
    return U


# when a lit name comes in: (key, ref) -> seconds
LIT_AT = {
    ("ur", (7, 2)): 5.2, ("mesopotamia", (7, 2)): 6.8, ("haran", (7, 2)): 8.4,
    ("canaan", (7, 3)): 4.8, ("chaldea", (7, 4)): 0.8, ("haran", (7, 4)): 3.4,
    ("shechem", (7, 4)): 8.6, ("canaan", (7, 5)): 5.6,
    ("egypt", (7, 6)): 3.6, ("canaan", (7, 7)): 6.6,
    ("hebron", (7, 8)): 5.0, ("egypt", (7, 9)): 4.2, ("egypt", (7, 10)): 9.0,
    ("hebron", (7, 12)): 2.4, ("hebron", (7, 14)): 1.8,
    ("hebron", (7, 15)): 0.2, ("shechem", (7, 16)): 2.6,
    ("goshen", (7, 17)): 4.6, ("midian", (7, 29)): 3.8,
    ("mount_sinai", (7, 30)): 5.6, ("mount_sinai", (7, 38)): 5.4,
    ("babylon", (7, 43)): 8.2, ("jerusalem", (7, 48)): 3.2,
    ("shiloh", (7, 45)): 5.8, ("jerusalem", (7, 43)): 6.0,
    ("jerusalem", (7, 46)): 1.0, ("jerusalem", (7, 47)): 0.2,
    ("egypt", (7, 36)): 3.0, ("jerusalem", (8, 1)): 5.8,
    ("judea", (8, 1)): 9.2, ("samaria", (8, 1)): 9.8,
}


def make_ctx(cam, lines, dots, hud):
    return Ctx(PROJ, cam, lines, dots, hud, land=land_screen(cam))


# ---------------------------------------------------------------------------
# Verse assembly
# ---------------------------------------------------------------------------

def cards_seen(fl):
    return _cards_seen(fl, [c for c, _m in CARDS], S_CARD)


def card_extent(fl, cards):
    return _card_extent(fl, cards, S_CARD)


def build_all():
    prev, last_cam, last_lab = None, None, None
    report = []
    shore, shore_qc = base_layers()
    for ref in REFS:
        cam1 = STAGE[ref]["cam"]
        cam0 = OPEN if last_cam is None else last_cam
        narr = NARR[ref]
        fl = plan(ref, cam0)
        assert _same(fl.cam1, cam1), ref
        last_cam = cam1
        t_land = fl.dur
        cls = {k: [] for k in CLS_PX}
        sea_rect = [el for name, el in shore if name is None]
        for name, el in shore:
            if name:
                cls[name].append(el)
        zs = [c[0] / S_CARD for c in fl.cams]
        rests_in_card = zs[-1] >= 0.2
        show_map = min(zs) < CARD_COVER
        show_card = cards_seen(fl)
        bt = beats(ref, fl, cam1, t_land)
        for name, els in bt.cls.items():
            cls.setdefault(name, []).extend(els)
        units_ = units(ref) + bt.units

        lines, lines_w = [], []
        for pts, kind, key in shore_qc + bt.qc:
            if kind == "river":
                continue
            wpx = 3.0 if kind == "route" else 2.0
            lines.append(([to_screen(cam1, p) for p in pts], wpx, kind, key))
            lines_w.append((pts, wpx))
        hud = hud_rects(ref, cam1) + bt.obstacles
        if rests_in_card:
            card_names = prev if show_map and prev_ref(ref) == last_lab \
                else None
            ends_card = card_ends(ref, show_card)
            sea_rect = sea_rect if show_map else []
            if not show_map:
                cls = {k: [] for k in cls}
                bt.pins, bt.overlay = [], []
            text = assemble(ref, fl, cls, bt, sea_rect, None, card_names,
                            show_card, show_map, zs)
            write(ref, text)
            report.append(dict(
                ref=ref, pxdeg=round(cam1[0] * K, 1), cam=round(fl.dur, 2),
                end=round(max([fl.dur] + ends_card + bt.ends), 2), narr=narr,
                kb=round(len(text.encode()) / 1024, 1), dropped=[],
                problems=[], mid=[], dips=[], half=False,
                ext=card_extent(fl, show_card)))
            continue
        if prev_ref(ref) != last_lab:
            prev = None
        dots = rest_dots(PROJ, units_, cam1, hud)
        ctx = make_ctx(cam1, lines, dots, hud)
        placed, dropped, problems = layout(units_, ctx, prev)
        prev_units = prev["units"] if prev else {}
        cur_ident = identities(placed, cam1)
        for u in units_:
            u.t_in = None
            if unchanged(u, cur_ident, prev_units):
                continue
            if u.new:
                t = getattr(u, "t_want", t_land + 0.05)
                u.t_in = round(max(0.0, t), 2)
        lab = emit_labels(PROJ, units_, placed, cur_ident, prev,
                          prev is not None, cam0, cam1, fl, t_land, hud,
                          lambda cam, ref=ref: hud_rects(ref, cam), lines_w,
                          problems)
        text = assemble(ref, fl, cls, bt, sea_rect, lab, None, show_card,
                        True, zs)
        write(ref, text)
        mid = midflight_qc(fl, placed, lab["exiting"])
        ends = bt.ends + card_ends(ref, show_card) + [
            getattr(u, "t_show", 0) + 0.5 for u in placed
            if getattr(u, "t_show", 0) > 0]
        end = max(ends + [fl.dur])
        report.append(dict(
            ref=ref, pxdeg=round(cam1[0] * K, 1), cam=round(fl.dur, 2),
            end=round(end, 2), narr=narr,
            kb=round(len(text.encode()) / 1024, 1),
            dropped=[u.key for u in units_
                     if u.key in dropped and anchor_on_screen(u, cam1)],
            problems=problems, mid=mid, dips=lab["dips"],
            half=inset_opacity(cam1) not in (0.0, 1.0),
            ext=extent_check(fl, PROJ, WORLD_LAT, WORLD_LON)))
        prev = prev_state(cam1, placed, cur_ident, lab["cur_dots"])
        last_lab = ref
    return report


def assemble(ref, fl, cls, bt, sea_rect, lab, held, show_card, show_map, zs):
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" '
           f'viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
           f'font-family="{FONT_FAMILY}">',
           f'<rect width="{W}" height="{H}" fill="{rgb(BG)}"/>']
    if bt.defs:
        svg.append("<defs>" + "".join(dict.fromkeys(bt.defs)) + "</defs>")
    svg.append(fl.open_camera())
    if show_map:
        vis = ["hidden" if z >= CARD_COVER else "visible" for z in zs]
        svg.append(f'<g visibility="{vis[0]}">'
                   + discrete(fl, "visibility", vis))
        svg += sea_rect
        svg.append(emit(fl, "coast", cls["coast"]))
        for name in DRAW_ORDER:
            svg.append(emit(fl, name, cls[name]))
        svg += bt.pins
        if lab is not None:
            svg += emit_label_layers(fl, lab)
        elif held:
            svg += held_labels(fl, held)
        svg.append("</g>")
    if show_card:
        ops = [f"{card_op(z):.2f}" for z in zs]
        for card in show_card:
            svg.append(f'<g opacity="{ops[0]}">{fl._anim("opacity", ops)}'
                       + card.svg(ref, fl, 18, TEXT, HL) + "</g>")
    svg.append("</g></g>")
    if show_map and bt.overlay:
        vals = [f"{1.0 - card_op(z):.2f}" for z in zs]
        svg.append(f'<g opacity="{vals[0]}">{fl._anim("opacity", vals)}'
                   + "".join(bt.overlay) + "</g>")
    svg.append(hud_svg(ref, fl, zs))
    svg.append(inset_svg(ref, fl))
    svg.append("</svg>")
    return "".join(svg)


def write(ref, text):
    ch, v = ref
    path = out_path(BOOK, ch, f"Acts_{ch}_{v}.svg")
    for attempt in range(5):
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            return
        except OSError:
            if attempt == 4:
                raise
            time.sleep(0.3)


def anchor_on_screen(u, cam):
    if not u.cands:
        return False
    x, y = to_screen(cam, P(*u.cands[0][:2]))
    return 0 <= x <= W and 0 <= y <= H


def main():
    report = build_all()
    for r in report:
        notes = []
        if r["dropped"]:
            notes.append("dropped " + ", ".join(r["dropped"]))
        for k, why in r["problems"]:
            notes.append(f"FORCED {k}: {', '.join(why)}")
        for a, b, t0, t1 in r["mid"]:
            notes.append(f"mid-flight overlap {a} x {b} at {t0}-{t1}s")
        if r["end"] > r["narr"] - 0.2:
            notes.append(f"LATE: lands at {r['end']}s, narration {r['narr']}s")
        if r["ext"]:
            notes.append(f"EDGE: {r['ext']}" if isinstance(r["ext"], str)
                         else "WORLD EDGE visible")
        if r["half"]:
            notes.append("the inset rests half-faded")
        ch, v = r["ref"]
        for n in notes:
            print(f"  {ch}:{v}: {n}")
    missing = [r for r in REFS if _narration(r) is None]
    if missing:
        print(f"  no MP3 for {missing}: paced at {NARR_FALLBACK}s")
    kb = [r["kb"] for r in report]
    print(f"Acts 6:8-8:3: {len(report)} SVG files, {sum(kb):.0f} KB "
          f"(largest {max(kb)} KB)")


if __name__ == "__main__":
    main()
