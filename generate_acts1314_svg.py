"""Render Acts 13-14 (Paul's first missionary journey) as per-verse SVGs: a
camera tour.

One large map of Syria, Cyprus and southern Asia Minor fills the frame in
every verse and is seen through a moving SMIL camera (svg_map_camera), as in
Numbers 34: each verse opens on the previous verse's rest camera and flies to
its own, so played in order the two chapters are one continuous flight. The
road ahead is a faint dashed line; each leg the text travels traces itself in
gold on its verse and then holds, land legs solid and sea legs dotted, and the
road home (14:21-26) runs beside the road out as a double line. Close-ups land
on the town the verse is in; wide shots show the whole circuit at the start,
on the return and at the end. A small overview inset (bottom left) shows the
camera's view during close-ups. Names keep their screen size through a flight
and are placed by a clash test at each rest; a plate at top right carries the
names a verse is about (the prophets and teachers, the proconsul and the
sorcerer). Everything lands before the verse's narration ends: the pacing
comes from the MP3s in web/audio.

The long stops are told without leaving the flight. Paul's sermon tells
Israel's story, and the camera flies it over the same map (13:17-26,
story_beats): Egypt, the wilderness, the land filling tribe by tribe, the
judges, Samuel, Saul, David, John at the Jordan and the light (Jesus, never
drawn as a man) coming down the valley to him, then the word running from
Jerusalem to Antioch. At Lystra (14:8-20) the camera dives from the town's
dot into a side-view scene card of the town (acts1314_lystra.py) and
surfaces at 14:20 for the road to Derbe. The synagogue and Jerusalem cards
are still to come; until then those verses hold on the map with their
plates (docs/design/acts-13-14.md).

The geography (coasts, lakes, rivers, sites, roads, the sermon's places) is
in acts_geography.py; the camera, labels, inset and QC in svg_map_camera.py;
the scene cards in svg_scene_card.py.

Coordinates are approximate; Lystra and Derbe are scholarly identifications.

Run inside the project venv:
    .venv\\Scripts\\python.exe generate_acts1314_svg.py
It prints any name it had to drop or force, and anything that would land
after the narration.
"""

import math
import os
import time
from xml.sax.saxutils import escape

import svg_figures as F
from svg_surface import SvgCanvas

from config import WEB_AUDIO_DIR
from passages import verse_numbers
from svg_surface import _fmt, FONT_FAMILY
from svg_chronicles_world import AUDIO_SLACK, _mp3_seconds
from svg_map_camera import (
    Projection, Flight as MapFlight, Unit as MapUnit, Ctx, Grow, EASE,
    cam_duration, _same, to_screen, ink, title_rect, compass_rect, title_svg,
    compass_scale_svg, inset_view_rect, plate_rect_svg, poly_el, ptsstr, rgb,
    fade, op_anim, traced_el, seg_len, emit_class, curve_d, layout,
    rest_dots, identities, unchanged, emit_labels, emit_label_layers,
    label_elements, prev_state, midflight_qc, extent_check, S_OTHER, S_AREA,
    S_CUR,
)
from generate_tabernacle import (W, H, BG, SAND, SAND_DIM, TEXT, TEXT_DIM, HL,
                                 out_path)
from generate_tribal_maps import SEA, LAND, RIVER, WATER_TXT
import acts_geography as G
import acts1314_lystra as LY

REFS = [(ch, v) for ch in (13, 14) for v in verse_numbers("Acts", ch)]
IDX = {r: i for i, r in enumerate(REFS)}
NARR_FALLBACK = 6.0            # seconds, for a verse with no MP3 yet


def _narration(ref):
    """The verse's narration in seconds, to a tenth: a re-render that moves
    a clip by a few milliseconds leaves the pictures unchanged."""
    ch, v = ref
    sec = _mp3_seconds(os.path.join(WEB_AUDIO_DIR, f"Acts_{ch}_{v}.mp3"))
    return round(sec, 1) if sec else None


NARR = {r: _narration(r) or NARR_FALLBACK for r in REFS}


def prev_ref(ref):
    i = IDX[ref]
    return REFS[i - 1] if i else None


def span(a, b):
    """Every ref from a to b inclusive, in reading order."""
    return REFS[IDX[a]:IDX[b] + 1]


# ---------------------------------------------------------------------------
# Projection: 100 world units per degree of latitude; a camera scale s shows
# the map at 100*s px per degree. The wide shots of the whole circuit are
# about 140 px/deg, so names grow (gently) past that.
# ---------------------------------------------------------------------------

PROJ = Projection(40.0, 28.0, 36.5)
K, EFF = PROJ.k, PROJ.eff
P, PS = PROJ.P, PROJ.PS
shot, fit = PROJ.shot, PROJ.fit
GROW = Grow(1.4, 0.5, 1.4)


class Unit(MapUnit):
    proj = PROJ
    grow = GROW


class Flight(MapFlight):
    grow = GROW


# the drawn world; no shot may see past it
WORLD_LAT = (27.5, 41.5)
WORLD_LON = (22.6, 44.0)


# ---------------------------------------------------------------------------
# Places. key -> (name as WEB spells it, lat, lon, modern name or None)
# ---------------------------------------------------------------------------

CITIES = {
    "antioch":  ("Antioch", *G.SITES["antioch"], "Antakya"),
    "seleucia": ("Seleucia", *G.SITES["seleucia"], None),
    "salamis":  ("Salamis", *G.SITES["salamis"], None),
    "paphos":   ("Paphos", *G.SITES["paphos"], None),
    "perga":    ("Perga", *G.SITES["perga"], None),
    "pantioch": ("Antioch of Pisidia", *G.SITES["pantioch"], "Yalvaç"),
    "iconium":  ("Iconium", *G.SITES["iconium"], "Konya"),
    "lystra":   ("Lystra", *G.SITES["lystra"], None),
    "derbe":    ("Derbe", *G.SITES["derbe"], None),
    "attalia":  ("Attalia", *G.SITES["attalia"], "Antalya"),
    "jerusalem": ("Jerusalem", *G.SITES["jerusalem"], None),
}
OFF_ROUTE = {"jerusalem"}      # named, never reached on this journey


def city_pt(key):
    return CITIES[key][1:3]


# ---------------------------------------------------------------------------
# The route. Each leg: (key, from, to, "land" | "sea", the ref it is
# travelled on, the road between, outbound or the road home)
# ---------------------------------------------------------------------------

def road(name, frm, to):
    """A road's points from `frm` to `to`, the road's own interior points
    from acts_geography when it has them, else a straight line."""
    pts = G.ROADS.get(name)
    a, b = city_pt(frm), city_pt(to)
    if not pts:
        return [a, b]
    pts = list(pts)
    if math.dist(pts[0], a) > math.dist(pts[-1], a):
        pts.reverse()
    return [a] + pts[1:-1] + [b]


def sea(frm, to, way=()):
    return [city_pt(frm)] + list(way) + [city_pt(to)]


# John's road home (13:13): down the Cestrus to the sea, past Cyprus to
# Caesarea, and up to Jerusalem
JOHN_WAY = [(36.84, 30.97), (36.30, 31.40), (35.10, 31.95), (33.70, 33.60),
            (32.55, 34.70), (32.50, 34.89), (32.05, 35.05)]

# the run home passes between Cyprus and the mainland
HOME_WAY = [(36.55, 31.30), (36.15, 32.40), (35.95, 33.40), (35.95, 34.40),
            (36.05, 35.30)]

LEGS = [
    ("a_s", "antioch", "seleucia", "land", (13, 4),
     road("ORONTES_ROAD", "antioch", "seleucia"), False),
    ("s_sa", "seleucia", "salamis", "sea", (13, 4),
     sea("seleucia", "salamis"), False),
    ("sa_p", "salamis", "paphos", "land", (13, 6),
     road("CYPRUS_ROAD", "salamis", "paphos"), False),
    ("p_pe", "paphos", "perga", "sea", (13, 13),
     sea("paphos", "perga", [(36.80, 30.95)]), False),
    ("john", "perga", "jerusalem", "john", (13, 13),
     sea("perga", "jerusalem", JOHN_WAY), False),
    ("pe_pa", "perga", "pantioch", "land", (13, 14),
     road("PERGA_ANTIOCH", "perga", "pantioch"), False),
    ("pa_i", "pantioch", "iconium", "land", (13, 51),
     road("ANTIOCH_ICONIUM", "pantioch", "iconium"), False),
    ("i_l", "iconium", "lystra", "land", (14, 6),
     road("ICONIUM_LYSTRA", "iconium", "lystra"), False),
    ("l_d", "lystra", "derbe", "land", (14, 20),
     road("LYSTRA_DERBE", "lystra", "derbe"), False),
    ("d_l", "derbe", "lystra", "land", (14, 21),
     road("LYSTRA_DERBE", "derbe", "lystra"), True),
    ("l_i", "lystra", "iconium", "land", (14, 21),
     road("ICONIUM_LYSTRA", "lystra", "iconium"), True),
    ("i_pa", "iconium", "pantioch", "land", (14, 21),
     road("ANTIOCH_ICONIUM", "iconium", "pantioch"), True),
    ("pa_pe", "pantioch", "perga", "land", (14, 24),
     road("PERGA_ANTIOCH", "pantioch", "perga"), True),
    ("pe_at", "perga", "attalia", "land", (14, 25),
     road("PERGA_ATTALIA", "perga", "attalia"), False),
    ("at_s", "attalia", "seleucia", "sea", (14, 26),
     sea("attalia", "seleucia", HOME_WAY), False),
    ("s_a", "seleucia", "antioch", "land", (14, 26),
     road("ORONTES_ROAD", "seleucia", "antioch"), True),
]


def leg_state(leg, ref):
    """'done', 'now' or 'ahead' for this verse."""
    i, j = IDX[leg[4]], IDX[ref]
    return "done" if i < j else "now" if i == j else "ahead"


def reached(ref):
    """The places the route has reached by this verse (Antioch from the
    start)."""
    out = {"antioch"}
    for leg in LEGS:
        if IDX[leg[4]] <= IDX[ref] and leg[3] != "john":
            out |= {leg[1], leg[2]}
    return out


# ---------------------------------------------------------------------------
# The base map, in world units: sea, land, lakes, coasts, rivers
# ---------------------------------------------------------------------------

def land_ring():
    """The mainland as one ring: the coast from the west edge round to
    Egypt, closed through the world's far corners."""
    coast = G.MAINLAND
    s, n = WORLD_LAT[0] - 2, WORLD_LAT[1] + 2
    w, e = WORLD_LON[0] - 2, WORLD_LON[1] + 2
    return (coast + [(s, coast[-1][1]), (s, e), (n, e), (n, w),
                     (coast[0][0], w)])


LAND_RING = land_ring()


def simplify(pts, tol):
    """Douglas-Peucker in degrees: the inset needs the shape, not the
    detail."""
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
    """A closed ring simplified as two halves split at its far point, so
    the chord the first split measures against is never degenerate."""
    k = max(range(len(ring)), key=lambda i: math.dist(ring[0], ring[i]))
    return (simplify(ring[:k + 1], tol)[:-1]
            + simplify(ring[k:] + ring[:1], tol)[:-1])


DRAW_TOL = 0.006      # degrees: under 5 px in the closest close-up


def base_layers():
    """The sea, and the shores as filled and stroked paths, each in the
    stroke class that holds its line width: [(class or None, element)];
    and the QC lines."""
    x0, y0 = P(WORLD_LAT[1] + 2, WORLD_LON[0] - 2)
    x1, y1 = P(WORLD_LAT[0] - 2, WORLD_LON[1] + 2)
    els = [(None, f'<rect x="{_fmt(x0)}" y="{_fmt(y0)}" '
                  f'width="{_fmt(x1 - x0)}" height="{_fmt(y1 - y0)}" '
                  f'fill="{rgb(SEA)}"/>')]
    qc = []
    shore = f'stroke="{rgb(SAND_DIM)}"'
    def ring_d(ring):
        return curve_d(PS(simplify_ring(ring, DRAW_TOL)), closed=True)
    els.append(("coast", f'<path d="{ring_d(LAND_RING)}" '
                         f'fill="{rgb(LAND)}" {shore}/>'))
    qc.append((PS(G.MAINLAND), "coast", None))
    for ring in G.ISLANDS:
        els.append(("coast", f'<path d="{ring_d(ring)}" '
                             f'fill="{rgb(LAND)}" {shore}/>'))
        qc.append((PS(ring + ring[:1]), "coast", None))
    for ring in G.GULFS:
        els.append(("coast", f'<path d="{curve_d(PS(ring), closed=True)}" '
                             f'fill="{rgb(SEA)}" {shore}/>'))
        qc.append((PS(ring + ring[:1]), "coast", None))
    for ring in G.LAKES.values():
        els.append(("lake", f'<path d="{ring_d(ring)}" '
                            f'fill="{rgb(SEA)}" {shore}/>'))
        qc.append((PS(ring + ring[:1]), "lake", None))
    for rv in G.RIVERS.values():
        d = curve_d(PS(simplify(rv, DRAW_TOL)))
        els.append(("river", f'<path d="{d}" fill="none" '
                             f'stroke="{rgb(RIVER)}"/>'))
        qc.append((PS(rv), "river", None))
    return els, qc


RIDGE_STEP, RIDGE_W, RIDGE_H = 0.13, 0.075, 0.05    # degrees


def relief():
    """Mountain ranges as rows of little peaks along their crest lines, the
    old way, in world units: they grow with the close-ups like the land."""
    els = []
    for crest in G.RELIEF.values():
        w = PS(crest)
        L = sum(math.dist(a, b) for a, b in zip(w, w[1:]))
        n = max(1, int(L / (RIDGE_STEP * K)))
        for i in range(n + 1):
            t = (i + 0.5) / (n + 1) * L
            run = 0.0
            for a, b in zip(w, w[1:]):
                seg = math.dist(a, b)
                if run + seg >= t:
                    f = (t - run) / seg
                    x = a[0] + (b[0] - a[0]) * f
                    y = a[1] + (b[1] - a[1]) * f
                    break
                run += seg
            # alternate a little either side of the crest
            nx, ny = -(b[1] - a[1]) / seg, (b[0] - a[0]) / seg
            off = (0.022 if i % 2 else -0.022) * K
            x, y = x + nx * off, y + ny * off
            hw, hh = RIDGE_W * K / 2, RIDGE_H * K
            els.append(f"M{_fmt(x - hw)} {_fmt(y + hh / 2)}"
                       f"L{_fmt(x)} {_fmt(y - hh / 2)}"
                       f"L{_fmt(x + hw)} {_fmt(y + hh / 2)}")
    if not els:
        return []
    return [f'<path d="{"".join(els)}" fill="none" '
            f'stroke="{rgb(SAND_DIM)}" stroke-linejoin="round"/>']


# ---------------------------------------------------------------------------
# The route, drawn per verse: the road ahead dashed, legs travelled solid
# (land) or dotted (sea), the road home a double line beside the road out,
# and this verse's legs tracing themselves in gold, one after another.
# ---------------------------------------------------------------------------

# screen widths of each stroke class
CLS_PX = {"coast": 1.6, "lake": 1.0, "river": 1.4, "relief": 1.1,
          "ahead": 1.2,
          "land": 3.0, "sea": 2.4, "home": 7.0, "home_in": 3.0,
          "trace": 4.0, "let_go": 4.0, "john": 1.6, "trace_john": 2.0}
CLS_DASH = {"ahead": (6, 5), "sea": (0.1, 6.5), "john": (5, 5)}
CLS_EXTRA = {"sea": ' stroke-linecap="round"'}
LET_GO = 0.8        # how long the last verse's gold takes to settle


def emit(fl, name, els, extra=""):
    return emit_class(fl, CLS_PX[name], els,
                      CLS_EXTRA.get(name, "") + extra, CLS_DASH.get(name))


def leg_len_px(leg, cam):
    pts = [to_screen(cam, p) for p in PS(leg[5])]
    return sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))


def route_layers(ref, cam1, t0, D):
    """{class: [elements]}, the QC lines, the traces [(leg, begin, dur)]
    and when the last one ends."""
    cls = {k: [] for k in CLS_PX}
    qc = []
    now = [lg for lg in LEGS if leg_state(lg, ref) == "now"]
    total = sum(leg_len_px(lg, cam1) for lg in now) or 1.0
    traces, t = [], t0
    for lg in now:
        d = D * leg_len_px(lg, cam1) / total
        traces.append((lg, round(t, 2), round(d, 2)))
        t += d
    when = {lg[0]: (b, d) for lg, b, d in traces}
    pr = prev_ref(ref)
    for lg in LEGS:
        key, _a, _b, mode, _r, pts, home = lg
        st = leg_state(lg, ref)
        w = PS(pts)
        qc.append((w, "route", key))
        if mode == "john":
            if st == "now":
                b, d = when[key]
                cls["trace_john"].append(traced_el(w, TEXT, b, d)[0])
            elif st == "done":
                cls["john"].append(poly_el(w, stroke=TEXT_DIM))
            continue
        if st == "ahead":
            if not home:
                cls["ahead"].append(poly_el(w, stroke=SAND_DIM))
            continue
        if st == "now":
            b, d = when[key]
            if not home:
                cls["ahead"].append(poly_el(w, stroke=SAND_DIM))
            if home and mode == "land":
                cls["home"].append(traced_el(w, HL + (242,), b, d)[0])
                cls["home_in"].append(traced_el(w, LAND, b, d)[0])
            else:
                cls["trace"].append(traced_el(w, HL + (242,), b, d)[0])
            continue
        # done
        if home and mode == "land":
            cls["home"].append(poly_el(w, stroke=SAND))
            cls["home_in"].append(poly_el(w, stroke=LAND))
        elif mode == "sea":
            cls["sea"].append(poly_el(w, stroke=RIVER))
        else:
            cls["land"].append(poly_el(w, stroke=SAND))
        if pr is not None and lg[4] == pr:
            # travelled last verse: its gold settles into the done style
            cls["let_go"].append(poly_el(w, stroke=HL + (242,))[:-2] + ">"
                                 + fade(0.0, LET_GO, out=True)
                                 + "</polyline>")
    end = max([b + d for _lg, b, d in traces] + [0.0])
    return cls, qc, traces, end


ROUTE_ORDER = ("ahead", "john", "land", "sea", "home", "home_in", "let_go",
               "trace_john", "trace")


# ---------------------------------------------------------------------------
# Labels
# ---------------------------------------------------------------------------

# region names: (key, NAME, lat/lon candidates, the refs it is lit on)
REGIONS = [
    ("cyprus", "CYPRUS", [(35.10, 33.15), (35.18, 33.45), (34.98, 32.90),
                          (35.25, 33.70), (35.42, 34.05), (35.30, 33.85),
                          (35.55, 34.35)], (13, 4), (13, 4)),
    ("pamphylia", "PAMPHYLIA", [(37.08, 31.20), (37.02, 31.50),
                                (37.15, 30.95), (36.95, 31.75),
                                (37.30, 31.55), (37.20, 32.00),
                                (36.80, 31.70), (37.05, 32.45),
                                (37.45, 31.20), (36.95, 32.85)],
     (14, 24), (14, 24)),
    ("pisidia", "PISIDIA", [(37.75, 30.85), (37.95, 30.70), (37.55, 31.10),
                            (38.05, 31.55)], (13, 14), (13, 14)),
    ("lycaonia", "LYCAONIA", [(37.55, 33.05), (37.70, 32.95),
                              (37.40, 32.75), (37.95, 33.10)],
     (14, 6), (14, 6)),
    ("cilicia", "CILICIA", [(37.05, 34.70), (37.10, 35.20), (36.95, 34.20)],
     None, None),
    ("syria", "SYRIA", [(35.55, 36.55), (35.80, 36.70), (35.25, 36.45)],
     None, None),
]
SEA_CANDS = [(35.55, 31.35), (35.30, 31.90), (35.85, 30.95), (34.70, 31.60),
             (35.65, 32.60), (34.45, 33.80), (35.60, 34.85), (35.95, 31.80)]


CROWD_PX = 34        # a lesser town this near the verse's own is left out


def units(ref):
    st = STAGE[ref]
    cur = st["city"]
    rch = reached(ref)
    cam = st["cam"]
    here = to_screen(cam, P(*city_pt(cur)))
    U = []
    for key, (name, la, lo, modern) in CITIES.items():
        if key != cur and math.dist(to_screen(cam, P(la, lo)), here) < \
                CROWD_PX:
            continue
        if key in OFF_ROUTE:
            if IDX[ref] >= IDX[(13, 13)] and ref != (13, 26):
                U.append(Unit(key, name, [S_OTHER], TEXT_DIM, italic=True,
                              cands=[(la, lo, c) for c in "lrab"],
                              dot=SAND_DIM, prio=4))
            continue
        if key == cur:
            U.append(Unit(key, name, [S_CUR], HL, bold=True,
                          cands=[(la, lo, c) for c in st.get("side", "rlab")],
                          dot=HL, prio=1, new=True, must=True, min_px=20,
                          sub=modern if st.get("modern") else None))
        elif key in rch:
            U.append(Unit(key, name, [S_OTHER], TEXT,
                          cands=[(la, lo, "r"), (la, lo, "l")], dot=SAND,
                          prio=3))
        else:
            U.append(Unit(key, name, [S_OTHER], TEXT_DIM,
                          cands=[(la, lo, "r"), (la, lo, "l")], dot=SAND_DIM,
                          prio=5))
    for key, name, cands, r0, r1 in REGIONS:
        lit = r0 is not None and IDX[r0] <= IDX[ref] <= IDX[r1]
        U.append(Unit("rg_" + key, name, [S_AREA, S_OTHER],
                      HL if lit else TEXT_DIM, bold=lit,
                      cands=[(a, b, "c") for a, b in cands],
                      prio=2 if lit else 6, new=lit))
    if ref == (13, 13):
        U.append(Unit("john", "John", [S_OTHER], TEXT, italic=True,
                      cands=[(34.45, 32.95, "r"), (34.85, 32.45, "r"),
                             (34.05, 33.40, "r"), (34.45, 32.75, "l")],
                      prio=2, new=True, must=True))
    U.append(Unit("sea", "The Great Sea", [S_AREA, S_OTHER], WATER_TXT,
                  italic=True, gmax=1.25,
                  cands=[(a, b, "c") for a, b in SEA_CANDS], prio=7,
                  in_sea=True))
    return U


def make_ctx(cam, lines, dots, hud):
    land = [to_screen(cam, P(a, b)) for a, b in LAND_RING]
    return Ctx(PROJ, cam, lines, dots, hud, land=land)


# ---------------------------------------------------------------------------
# HUD (screen space, never scaled): the title, the plate at top right, the
# compass and scale bar, the overview inset
# ---------------------------------------------------------------------------

SCALE_KM = 50
INSET_RECT = (14, H - 14 - 132, 14 + 176, H - 14)       # x0, y0, x1, y1
INSET_BOX = (34.35, 38.75, 29.75, 36.65)               # lat0, lat1, lon0, lon1
INSET_OFF, INSET_RAMP = 0.82, 0.07
PLATE_TOP, PLATE_LINE = 14, (26, 20)                   # first line, the rest


def title_of(ref):
    return (STAGE[ref].get("title")
            or f"Paul’s First Journey — Acts {ref[0]}")


SERMON_BOX = (29.3, 38.9, 25.7, 41.8)
SERMON_INSET = span((13, 17), (13, 37))


def inset_box(ref):
    return SERMON_BOX if ref in SERMON_INSET else INSET_BOX


def inset_opacity(cam, ref=None):
    la0, la1, _a, _b = inset_box(ref) if ref else INSET_BOX
    hfrac = (H / cam[0] / K) / (la1 - la0)
    return max(0.0, min(1.0, (INSET_OFF - hfrac) / INSET_RAMP))


def plate_lines(ref):
    """[(text, px, fill, bold, italic)] for the plate, or []."""
    return STAGE[ref].get("plate") or []


def plate_rect(ref):
    """One plate size for a run of plated verses, so it never changes size
    while it stays up."""
    run = [ref]
    r = prev_ref(ref)
    while r and plate_lines(r):
        run.append(r)
        r = prev_ref(r)
    i = IDX[ref] + 1
    while i < len(REFS) and plate_lines(REFS[i]):
        run.append(REFS[i])
        i += 1
    wmax, nmax = 0, 0
    for r in run:
        lines = plate_lines(r)
        nmax = max(nmax, len(lines))
        for text, px, _f, bold, italic in lines:
            box = ink(text, px, bold, italic, "ra")
            wmax = max(wmax, -box[0])
    h = 14 + sum(PLATE_LINE[0] if i == 0 else PLATE_LINE[1]
                 for i in range(nmax)) + 14 + 8
    return (W - 18 - wmax - 14, 4, W - 4, 4 + h)


def plate_texts(ref):
    out = []
    y = PLATE_TOP
    for i, (text, px, fill, bold, italic) in enumerate(plate_lines(ref)):
        a = ' font-weight="bold"' if bold else ""
        a += ' font-style="italic"' if italic else ""
        out.append(f'<text x="{W - 18}" y="{y}" font-size="{px}" '
                   f'fill="{rgb(fill)}" text-anchor="end"{a} '
                   f'dominant-baseline="text-before-edge">{escape(text)}'
                   f'</text>')
        y += (PLATE_LINE[0] if i == 0 else PLATE_LINE[1]) + 8
    return "".join(out)


def hud_rects(ref, cam):
    hud = [("title", title_rect(title_of(ref))),
           ("compass", compass_rect(PROJ, min(cam[0], 6.0), SCALE_KM))]
    if plate_lines(ref):
        hud.append(("plate", plate_rect(ref)))
    if inset_opacity(cam, ref) > 0.05:
        hud.append(("inset", INSET_RECT))
    return hud


def hud_svg(ref, fl, zs=None):
    out = [title_svg(title_of(ref), TEXT)]
    pr = prev_ref(ref)
    had = pr is not None and plate_lines(pr)
    if plate_lines(ref):
        rect = plate_rect_svg(plate_rect(ref))
        t_new = STAGE[ref].get("plate_at")
        if had and plate_lines(pr) != plate_lines(ref) and t_new and \
                t_new > 1.0:
            # the new words come late in the verse: the old plate goes now
            # and the new one comes whole, so no empty plate waits
            out.append(f'<g>{fade(0.0, 0.5, out=True)}'
                       + plate_rect_svg(plate_rect(pr)) + plate_texts(pr)
                       + "</g>")
            out.append(f'<g opacity="0">{fade(t_new, 0.6)}' + rect
                       + plate_texts(ref) + "</g>")
        elif had and plate_lines(pr) != plate_lines(ref):
            out.append(rect)
            out.append(f'<g>{fade(0.0, 0.35, out=True)}' + plate_texts(pr)
                       + "</g>")
            out.append(f'<g opacity="0">{fade(0.25, 0.5)}'
                       + plate_texts(ref) + "</g>")
        elif had:
            out.append(rect + plate_texts(ref))
        else:
            t = STAGE[ref].get("plate_at", 0.0)
            out.append(f'<g opacity="0">{fade(t, 0.6)}' + rect
                       + plate_texts(ref) + "</g>")
    elif had:
        out.append(f'<g>{fade(0.0, 0.5, out=True)}'
                   + plate_rect_svg(plate_rect(pr)) + plate_texts(pr)
                   + "</g>")
    ops = [1.0 - card_op(z) for z in (zs or [0.0])]
    if max(ops) > 0:
        tag = [f"{o:.2f}" for o in ops]
        capped = Flight(fl.cam0, [])
        capped.cams = [(min(c[0], 6.0), c[1], c[2]) for c in fl.cams]
        capped.static, capped.pure_pan = fl.static, fl.pure_pan
        capped.dur = fl.dur
        out.append(f'<g opacity="{tag[0]}">{fl._anim("opacity", tag)}'
                   + compass_scale_svg(capped, PROJ, SCALE_KM) + "</g>")
    return "".join(out)


INSET_TOL = 0.12          # degrees: about 3 px in the circuit inset
INSET_LAND = simplify_ring(LAND_RING, INSET_TOL)
INSET_ISLANDS = [simplify_ring(r, INSET_TOL) for r in G.ISLANDS]


def inset_map(ref, fl, box):
    """The inset's map for one box, with the route and Israel's roads so
    far and the camera's view boxed."""
    x0, y0, x1, y1 = INSET_RECT
    la0, la1, lo0, lo1 = box
    iw, ih = x1 - x0 - 8, y1 - y0 - 8
    k = min(iw / ((lo1 - lo0) * EFF), ih / (la1 - la0))
    ox = x0 + 4 + (iw - (lo1 - lo0) * EFF * k) / 2
    oy = y0 + 4 + (ih - (la1 - la0) * k) / 2

    def ip(lat, lon):
        return (ox + (lon - lo0) * EFF * k, oy + (la1 - lat) * k)

    out = [poly_el([ip(a, b) for a, b in INSET_LAND], fill=LAND,
                   closed=True)]
    for isl in INSET_ISLANDS:
        if len(isl) > 2:
            out.append(poly_el([ip(a, b) for a, b in isl], fill=LAND,
                               closed=True))
    for name, pts in G.STORY.items():
        if story_state(name, ref) == "done":
            out.append(poly_el([ip(a, b) for a, b in pts], stroke=ROSE,
                               extra=' stroke-width="1"'))
    for lg in LEGS:
        if leg_state(lg, ref) == "done" and lg[3] != "john":
            out.append(poly_el([ip(a, b) for a, b in lg[5]],
                               stroke=RIVER if lg[3] == "sea" else SAND,
                               extra=' stroke-width="1.2"'))
    out.append(inset_view_rect(fl, PROJ, ip, HL, min_px=6))
    return out


def inset_svg(ref, fl):
    x0, y0, x1, y1 = INSET_RECT
    ops = [f"{inset_opacity(c, ref):.2f}" for c in fl.cams]
    out = [f'<g opacity="{ops[0]}">{fl._anim("opacity", ops)}',
           f'<defs><clipPath id="insetclip"><rect x="{x0}" y="{y0}" '
           f'width="{x1 - x0}" height="{y1 - y0}" rx="6"/></clipPath></defs>',
           f'<g clip-path="url(#insetclip)">',
           f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" '
           f'fill="{rgb(SEA)}"/>']
    pr = prev_ref(ref)
    box, pbox = inset_box(ref), inset_box(pr) if pr else None
    if pbox and pbox != box:
        t = STAGE[ref].get("inset_swap", 1.0)
        out.append(f'<g>{fade(t, 1.2, out=True)}'
                   + "".join(inset_map(pr, fl, pbox)) + "</g>")
        out.append(f'<g opacity="0">{fade(t, 1.2)}'
                   + "".join(inset_map(ref, fl, box)) + "</g>")
    else:
        out += inset_map(ref, fl, box)
    out.append("</g>")
    out.append(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" '
               f'height="{y1 - y0}" rx="6" fill="none" '
               f'stroke="{rgb(SAND_DIM)}" stroke-width="1.5"/>')
    out.append("</g>")
    return "".join(out)


# ---------------------------------------------------------------------------
# The shot list: per verse, the town it is in, its rest camera, and what the
# plate says. STAGE[ref] keys: city, cam, legs (a camera plan in place of the
# default single flight), plate, plate_at, title, modern, side.
# ---------------------------------------------------------------------------

CLOSE = 460                                   # a town close-up, px/deg
WIDE = fit(34.45, 38.55, 30.45, 36.35, (60, 70, 1000, 560))   # the circuit
OPEN = fit(33.6, 39.2, 29.5, 37.3)            # 13:1 opens wider still


def at(key, pxdeg=CLOSE, sx=W / 2, sy=H / 2 + 20):
    la, lo = city_pt(key)
    return shot(la, lo, pxdeg, sx, sy)


def frame(keys, box=(80, 90, W - 80, H - 60), cap=CLOSE, extra=()):
    pts = [city_pt(k) for k in keys] + list(extra)
    lats = [p[0] for p in pts]
    lons = [p[1] for p in pts]
    pad_la, pad_lo = 0.12, 0.15
    return fit(min(lats) - pad_la, max(lats) + pad_la,
               min(lons) - pad_lo, max(lons) + pad_lo, box, cap)


def names(*rows):
    """Plate lines: the first is the plate's heading."""
    out = []
    for i, r in enumerate(rows):
        text, fill = (r, None) if isinstance(r, str) else r
        if i == 0:
            out.append((text, PLATE_LINE[0], fill or HL, True, False))
        else:
            out.append((text, PLATE_LINE[1], fill or TEXT, False, False))
    return out


STAGE = {}


def stage(first, last, **kw):
    for r in span(first, last):
        STAGE[r] = dict(STAGE.get(r, {}), **kw)


stage((13, 1), (14, 28), city="antioch")
stage((13, 1), (13, 3), city="antioch", cam=at("antioch"), modern=True)
stage((13, 1), (13, 1), plate=names("prophets and teachers", "Barnabas",
                                    "Simeon Niger", "Lucius of Cyrene",
                                    "Manaen", "Saul"))
stage((13, 2), (13, 3), plate=names("prophets and teachers",
                                    "Barnabas", ("Simeon Niger", TEXT_DIM),
                                    ("Lucius of Cyrene", TEXT_DIM),
                                    ("Manaen", TEXT_DIM), "Saul"))
stage((13, 4), (13, 4), city="seleucia",
      cam=frame(["antioch", "seleucia", "salamis"], box=(230, 90, W - 80,
                                                         H - 60),
                extra=[(35.05, 33.55)]))
stage((13, 5), (13, 5), city="salamis", cam=at("salamis"))
stage((13, 6), (13, 12), city="paphos", cam=at("paphos"))
stage((13, 6), (13, 6), cam=frame(["salamis", "paphos"]))
stage((13, 7), (13, 8), plate=names("Paphos", "Sergius Paulus, proconsul",
                                    "Bar Jesus, sorcerer"))
stage((13, 9), (13, 12), plate=names("Paphos", "Sergius Paulus, proconsul",
                                     "Elymas, sorcerer"))
stage((13, 13), (13, 13), city="perga",
      cam=frame(["paphos", "perga", "jerusalem"]))
stage((13, 14), (13, 50), city="pantioch", cam=at("pantioch"))
stage((13, 14), (13, 14), cam=frame(["perga", "pantioch"]), modern=True)
stage((13, 51), (13, 51), city="iconium", cam=frame(["pantioch", "iconium"]),
      modern=True)
stage((13, 52), (14, 5), city="iconium", cam=at("iconium"))
stage((14, 6), (14, 6), city="lystra",
      cam=frame(["iconium", "lystra", "derbe"]))
stage((14, 7), (14, 19), city="lystra", cam=at("lystra"))
stage((14, 20), (14, 20), city="derbe", cam=frame(["lystra", "derbe"]))
stage((14, 21), (14, 23), city="pantioch",
      cam=frame(["derbe", "lystra", "iconium", "pantioch"], cap=300))
_PA_PE = frame(["pantioch", "perga"])
stage((14, 24), (14, 24), city="perga", cam=_PA_PE,
      legs=[("to", _PA_PE, 1.3)], trace_at=(0.9, 1.2))
_PE_AT = frame(["perga", "attalia"], cap=CLOSE)
stage((14, 25), (14, 25), city="attalia", cam=_PE_AT, modern=True,
      legs=[("to", _PE_AT, 1.4)], trace_at=(1.0, 1.3))
stage((14, 26), (14, 26), city="antioch", cam=WIDE)
stage((14, 27), (14, 28), city="antioch", cam=WIDE)


# the sermon (13:15-41) and the two Sabbaths (13:42-50). The synagogue and
# Jerusalem scenes are still to come: until then those verses hold on the
# map at Antioch of Pisidia and Jerusalem, with the plates.
EGYPT = shot(30.55, 33.25, 145)
WILD = shot(30.20, 34.15, 145)
CANAAN = fit(30.60, 33.47, 33.80, 36.65, (0, 50, W, H - 10))
JUDGES_SHOT = shot(32.02, 35.25, 230)
BENJAMIN = shot(31.86, 35.25, 620)
BETHLEHEM = shot(31.74, 35.22, 660)
JORDAN = shot(31.80, 35.42, 620)
JORDAN_N = shot(32.12, 35.52, 460)
WW = shot(35.2, 33.4, 66)                   # the whole eastern sea
JERUSALEM = shot(31.80, 35.25, 560)
T_SERMON = "Paul’s Sermon in Antioch of Pisidia — Acts 13"
T_SABBATHS = "Two Sabbaths in Antioch of Pisidia — Acts 13"
T_LYSTRA = "Taken for Gods at Lystra — Acts 14"

stage((13, 15), (13, 41), title=T_SERMON)
stage((13, 42), (13, 50), title=T_SABBATHS)
stage((14, 8), (14, 19), title=T_LYSTRA)
stage((13, 17), (13, 17), cam=EGYPT,
      legs=[("hold", None, 0.2), ("to", EGYPT, 3.8)], inset_swap=1.0)
stage((13, 18), (13, 18), cam=WILD, legs=[("to", WILD, 2.8)],
      plate=names("40 years"), plate_at=1.0)
stage((13, 19), (13, 19), cam=CANAAN, legs=[("to", CANAAN, 1.8)],
      plate=names("450 years"), plate_at=5.8)
stage((13, 20), (13, 20), cam=JUDGES_SHOT, legs=[("to", JUDGES_SHOT, 1.2)])
stage((13, 21), (13, 21), cam=BENJAMIN, legs=[("to", BENJAMIN, 1.8)],
      plate=names("40 years"), plate_at=6.2)
_BETH2 = shot(31.725, 35.21, 700)
stage((13, 22), (13, 22), cam=_BETH2,
      legs=[("hold", None, 0.8), ("to", BETHLEHEM, 1.6),
            ("hold", None, 1.6), ("to", _BETH2, 6.4)])
_BETH3 = shot(31.715, 35.21, 740)
stage((13, 23), (13, 23), cam=_BETH3, legs=[("to", _BETH3, 3.0)])
stage((13, 24), (13, 24), cam=JORDAN, legs=[("to", JORDAN, 1.8)])
stage((13, 25), (13, 25), cam=JORDAN_N, legs=[("to", JORDAN_N, 2.0)])
stage((13, 26), (13, 26), cam=WW, legs=[("to", WW, 3.0)], city_at=6.2)
stage((13, 27), (13, 37), cam=JERUSALEM)
stage((13, 27), (13, 27), legs=[("to", JERUSALEM, 3.4)])
stage((13, 32), (13, 32), plate=names("fathers"), plate_at=0.4)
stage((13, 33), (13, 33), plate=names("second psalm"), plate_at=5.4)
stage((13, 35), (13, 35), plate=names("another psalm"), plate_at=0.3)
stage((13, 38), (13, 50), cam=at("pantioch"))
stage((13, 38), (13, 38), legs=[("to", at("pantioch"), 5.4)],
      inset_swap=2.0)
stage((13, 39), (13, 39), plate=names("law of Moses"), plate_at=5.2)
stage((13, 40), (13, 41), plate=names("the prophets"), plate_at=2.6)
stage((13, 47), (13, 47), cam=WW,
      legs=[("hold", None, 2.4), ("to", WW, 4.0)])
stage((13, 48), (13, 48), legs=[("to", at("pantioch"), 3.6)])
_PA_IC = frame(["pantioch", "iconium"])
stage((13, 50), (13, 50), cam=_PA_IC,
      legs=[("hold", None, 6.4), ("to", _PA_IC, 2.6)])
stage((13, 51), (13, 51), cam=_PA_IC, legs=[], trace_at=(0.8, 2.8))


# Lystra (14:8-20): the camera dives from Lystra's dot into the scene card
# (acts1314_lystra) and surfaces at 14:20 for the road to Derbe
LYS = LY.build(P(*city_pt("lystra")))
CARD_IN = (0.06, 0.16)   # zooms over which the card fades in over the map
CARD_COVER = 0.4         # at this zoom the card fills the frame


def card_cam(xyz):
    return LYS.cam(*xyz)


for _r, _xyz in LY.SHOTS.items():
    if _r == (14, 20):
        continue
    _legs = LY.LEGS.get(_r)
    if _legs:
        stage(_r, _r, cam=card_cam(_xyz),
              legs=[(k, card_cam(x) if x else None, d) for k, x, d in _legs])
    else:
        stage(_r, _r, cam=card_cam(_xyz),
              legs=[("to", card_cam(_xyz), LY.DUR.get(_r, 0.0))])
_LY_DE = frame(["lystra", "derbe"])
stage((14, 20), (14, 20), cam=_LY_DE,
      legs=[("hold", None, 3.0), ("to", _LY_DE, 2.4)], trace_at=(5.4, 1.6))


def card_op(z):
    return max(0.0, min(1.0, (z - CARD_IN[0]) / (CARD_IN[1] - CARD_IN[0])))


NEED_AFTER = 1.4      # seconds a verse holds still after its flight, at least


def plan(ref, cam0):
    """The verse's camera legs."""
    st = STAGE[ref]
    cam1 = st["cam"]
    if "legs" in st:
        legs = st["legs"]
        if ref == (14, 20):
            # it opens where 14:19 rested, in the card
            legs = [("hold", None, 3.0), ("to", st["cam"], 2.4)]
        return Flight(cam0, legs)
    D = cam_duration(cam0, cam1)
    if D:
        D = round(max(0.9, min(D, NARR[ref] - AUDIO_SLACK - NEED_AFTER)), 2)
    return Flight(cam0, [("to", cam1, D)])


# ---------------------------------------------------------------------------
# The sermon's story on the map (13:17-26)
#
# Paul tells Israel's story from Egypt to David's son, and it happened on
# this map, so the camera leaves the synagogue and flies it: the fathers at
# Hebron, the people going down to Egypt and out of it, the wilderness, the
# crossing, the land filling tribe by tribe, the judges, Samuel, Saul, David,
# John at the Jordan, and the light (Jesus, never drawn as a man) coming down
# the valley to him. At 13:26 the camera rises to the whole eastern sea and
# the word runs from Jerusalem to Antioch: "to you".
#
# People are pinned figures that keep one screen size (pin_svg); the story's
# roads are a rose dashed line, each traced in gold on its own verse with a
# band of twelve dots riding its head (rider_svg).
# ---------------------------------------------------------------------------

# Saul's pin stands a little north of Gibeah itself (Tell el-Ful), so that
# at Bethlehem, three miles south, David's figure leaves his dot clear
S = dict(G.SERMON_SITES, gibeah_pin=(31.848, 35.233))
ROSE = (196, 128, 104)                 # Israel's roads, never Paul's
CLS_PX.update({"story": 2.6, "story_trace": 4.0, "story_let": 4.0,
               "tribe": 1.0, "tribe_hl": 2.5, "glint": 4.0,
               "terr": 1.6, "terr_trace": 2.5})
CLS_DASH.update({"story": (9, 5), "terr": (7, 5), "terr_trace": (7, 5)})
STORY_ON = {"going_down": (13, 17), "exodus": (13, 17),
            "wilderness": (13, 18), "crossing": (13, 19),
            "john_course": (13, 25), "word": (13, 26)}
STORY_T = {"going_down": (4.6, 0.8), "exodus": (6.4, 2.2),
           "wilderness": (0.2, 2.8), "crossing": (1.2, 0.8),
           "john_course": (2.0, 2.0), "word": (3.2, 1.4)}
FIG_PX = 84                                  # a pinned person, screen px
MAN_H = 97.0                                 # a man's height in units


def fig_svg(parts, h_px, ink, page=LAND, flip=1, unit_h=MAN_H):
    """A figure from svg_figures in screen px, feet at (0, 0): a figure
    unit_h units tall comes out h_px tall."""
    c = SvgCanvas(10, 10)
    F.draw(c, parts, 0, 0, h_px / unit_h, ink, page, flip=flip)
    return "".join(c._els)


def lift_in(inner, t, dur=0.6, lift=6):
    """Fade in while rising `lift` px onto its place."""
    return (f'<g opacity="0">{fade(t, dur)}'
            f'<g transform="translate(0 {lift})">'
            f'<animateTransform attributeName="transform" type="translate" '
            f'values="0 {lift};0 0" begin="{t:.2f}s" dur="{dur:.2f}s" '
            f'fill="freeze" calcMode="spline" keyTimes="0;1" '
            f'keySplines="{EASE}"/>{inner}</g></g>')


def inv_scale(fl):
    """A scale(1/s) that rides the camera: screen px inside a world group."""
    ks = [f"{1 / c[0]:.5g}" for c in fl.cams]
    return f'scale({ks[0]})', fl._anim("transform", ks, "scale")


def pin_svg(fl, lat, lon, inner):
    """`inner` (screen px, origin at the anchor) pinned at (lat, lon), one
    screen size through the flight."""
    x, y = P(lat, lon)
    sc, anim = inv_scale(fl)
    return (f'<g transform="translate({_fmt(x)} {_fmt(y)})">'
            f'<g transform="{sc}">{anim}{inner}</g></g>')


def rider_svg(fl, pts_w, begin, dur, inner, t_show=None, t_hide=None):
    """`inner` (screen px) riding a world polyline from begin to begin+dur
    on the trace's own easing, so it stays at the head of the gold line.
    Hidden until t_show (default: begin)."""
    d = "M" + " L".join(f"{_fmt(x)} {_fmt(y)}" for x, y in pts_w)
    sc, anim = inv_scale(fl)
    t_show = begin if t_show is None else t_show
    out = (f'<g opacity="0"><set attributeName="opacity" to="1" '
           f'begin="{t_show:.2f}s"/>')
    if t_hide is not None:
        out += fade(t_hide, 0.5, out=True)
    return (out + f'<g><animateMotion path="{d}" begin="{begin:.2f}s" '
            f'dur="{dur:.2f}s" fill="freeze" calcMode="spline" '
            f'keyPoints="0;1" keyTimes="0;1" keySplines="{EASE}"/>'
            f'<g transform="{sc}">{anim}{inner}</g></g></g>')


def band_dots(n, col=TEXT):
    """A people of n: a little cluster of dots on a dark halo."""
    cols = 4 if n > 4 else n
    pts = []
    for i in range(n):
        r, c = divmod(i, cols)
        pts.append(((c - (cols - 1) / 2) * 7, -r * 7 - 4))
    return ("".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.4" '
                    f'fill="{rgb(BG)}" fill-opacity="0.85"/>'
                    for x, y in pts)
            + "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" '
                      f'fill="{rgb(col)}"/>' for x, y in pts))


def story_state(name, ref):
    i, j = IDX[STORY_ON[name]], IDX[ref]
    return "done" if i < j else "now" if i == j else "ahead"


# pinned people and emblems: key -> (place, the verse it rises on, when, the
# verse it settles to a dot and its name on (None: an emblem simply goes),
# the last verse it is shown, its name)
PINS = {
    "fathers": ("hebron", (13, 17), 4.0, (13, 18), (13, 25), "fathers"),
    "samuel": ("ramathaim", (13, 20), 2.0, (13, 21), (13, 25), "Samuel"),
    "saul": ("gibeah_pin", (13, 21), 2.2, (13, 22), (13, 25), "Saul"),
    "david": ("bethlehem", (13, 22), 2.6, (13, 24), (13, 25), "David"),
    "manger": ("bethlehem", (13, 23), 0.8, None, (13, 23), None),
    "john": ("bethany_jordan", (13, 24), 2.0, (13, 26), (13, 26), "John"),
}
# each pin's box round its anchor, screen px (x0, y0, x1, y1)
PIN_BOX = {"fathers": (-48, -86, 48, 0), "samuel": (-24, -86, 24, 0),
           "saul": (-24, -86, 24, 0), "david": (-24, -86, 50, 0),
           "manger": (-70, -36, -4, 0), "john": (-36, -86, 36, 0)}


def pin_figure(key, ink, kneel=False):
    if key == "fathers":
        one = F.man(staff=True)
        return (f'<g transform="translate(-26 0)">{fig_svg(one, 76, ink)}'
                f'</g>{fig_svg(one, 84, ink)}'
                f'<g transform="translate(26 0)">'
                f'{fig_svg(one, 76, ink, flip=-1)}</g>')
    if key == "samuel":
        return fig_svg(F.man(staff=True), FIG_PX, ink)
    if key in ("saul", "david"):
        out = fig_svg(F.king(), FIG_PX, ink)
        if key == "david":
            u = F.UNIT["harp"]
            out += (f'<g transform="translate(30 0)">'
                    f'{fig_svg(F.harp(), FIG_PX * u, ink, unit_h=MAN_H * u)}'
                    f'</g>')
        return out
    if key == "manger":
        u = F.UNIT["manger"]
        return (f'<g transform="translate(-38 0)">'
                f'{fig_svg(F.manger(), 50, ink, unit_h=MAN_H * u)}</g>')
    if key == "john":
        if kneel:
            return fig_svg(F.man(pose="kneel", arms="open"), FIG_PX, ink)
        return fig_svg(F.man(arms="open"), FIG_PX, ink)
    raise KeyError(key)


class Beats:
    """What a verse adds to the map beyond the route: world elements by
    stroke class, fills under the lakes, pinned figures, labels, screen
    rects the names keep clear of, screen-space overlays drawn over the
    map at the rest camera, and when each thing ends."""

    def __init__(self):
        self.cls = {k: [] for k in CLS_PX}
        self.fills, self.pins, self.units = [], [], []
        self.obstacles, self.overlay, self.ends = [], [], []
        self.qc = []


def tribe_alpha(key):
    return (26 if key in G.EAST_TRIBES else 42) / 255


TRIBE_FOCUS = 0.30
TRIBES_ALL = G.WEST_TRIBES + G.EAST_TRIBES
_POLES = {k: PROJ.pole(r) for k, r in G.TRIBE_RINGS.items()}


def tribe_path(rings, col, op, anim=""):
    d = "".join("M" + " ".join(f"{_fmt(x)},{_fmt(y)}" for x, y in PS(r))
                + "Z" for r in rings)
    return (f'<path d="{d}" fill-rule="evenodd" fill="{rgb(col)}" '
            f'fill-opacity="{op:.3f}">{anim}</path>')


def pulse_once(begin, dur=0.8, hi=1.0):
    return (f'<animate attributeName="opacity" values="0;{hi};{hi};0" '
            f'keyTimes="0;0.3;0.6;1" begin="{begin:.2f}s" dur="{dur:.2f}s" '
            f'fill="freeze"/>')


def screen_ring(xy, begin, r0, r1, dur, col=HL, width=2.0):
    """An expanding ring in screen px that fades as it grows."""
    x, y = xy
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r0}" fill="none" '
            f'stroke="{rgb(col)}" stroke-width="{width}" opacity="0">'
            f'<set attributeName="opacity" to="1" begin="{begin:.2f}s"/>'
            f'<animate attributeName="r" values="{r0};{r1}" '
            f'begin="{begin:.2f}s" dur="{dur:.2f}s" fill="freeze"/>'
            f'<animate attributeName="stroke-opacity" values="1;0" '
            f'begin="{begin:.2f}s" dur="{dur:.2f}s" fill="freeze"/></circle>')


def at_rest(cam1, lat, lon):
    return to_screen(cam1, P(lat, lon))


def pin_label(key, text, lat, lon, cam1, fill, bold, prio, new, must):
    """A pinned figure's name beside its box (right, left, above), placed
    by the clash test."""
    ax, ay = at_rest(cam1, lat, lon)
    x0, y0, x1, _y1 = PIN_BOX[key]
    cands = []
    for sx, sy, code in ((ax + x1 + 2, ay + y0 * 0.55, "r"),
                         (ax + x0 - 2, ay + y0 * 0.55, "l"),
                         (ax, ay + y0 - 2, "a"),
                         (ax + x1 + 2, ay + y0 * 0.2, "r"),
                         (ax + x0 - 2, ay + y0 * 0.2, "l")):
        la, lo = PROJ.unproject(cam1, sx, sy)
        cands.append((la, lo, code))
    return Unit("pin_" + key, text, [S_CUR if bold else S_OTHER], fill,
                bold=bold, cands=cands, prio=prio, new=new, must=must)


LIGHT_PX = 44


def light_svg(ink=HL):
    if hasattr(F, "light"):
        return fig_svg(F.light(), LIGHT_PX, ink, unit_h=60.0)
    # until the vocabulary has its light: the manger's lens, standing
    return (f'<path d="M0 0 C-14 -12 -14 -32 0 -44 C14 -32 14 -12 0 0Z" '
            f'fill="{rgb(HL)}" stroke="{rgb(BG)}" stroke-width="1.2"/>')


def story_beats(ref, fl, cam1, t_land):
    b = Beats()
    i = IDX[ref]
    pr = prev_ref(ref)

    # Israel's roads: traced in gold on their verse, rose and dashed after
    for name, pts in G.STORY.items():
        st = story_state(name, ref)
        if st == "ahead":
            continue
        w = PS(pts)
        if st == "now":
            t0, d = STORY_T[name]
            b.cls["story_trace"].append(traced_el(w, HL + (242,), t0, d)[0])
            b.ends.append(t0 + d)
        else:
            b.cls["story"].append(poly_el(w, stroke=ROSE))
            if STORY_ON[name] == pr:
                b.cls["story_let"].append(
                    poly_el(w, stroke=HL + (242,))[:-2] + ">"
                    + fade(0.0, LET_GO, out=True) + "</polyline>")
        b.qc.append((w, "route", "story_" + name))

    # the people riding the heads of the roads
    def band_on(name, n, t_show=None, t_hide=None):
        t0, d = STORY_T[name]
        b.pins.append(rider_svg(fl, PS(G.STORY[name]), t0, d, band_dots(n),
                                t_show=t_show, t_hide=t_hide))
    if ref == (13, 17):
        band_on("going_down", 3, t_hide=5.4)
        band_on("exodus", 12, t_show=5.4)
    elif ref == (13, 18):
        band_on("wilderness", 12, t_show=0.0)
    elif ref == (13, 19):
        band_on("crossing", 12, t_show=0.0, t_hide=3.8)

    # the land fills, tribe by tribe, as the people reach it (13:19)
    if IDX[ref] >= IDX[(13, 19)]:
        gil = P(*S["gilgal"])
        for k, key in enumerate(TRIBES_ALL):
            rings = G.TRIBE_RINGS[key]
            col = G.TRIBE_COL[key]
            base = tribe_alpha(key)
            if ref == (13, 19):
                t = 3.8 + k * 0.12
                pole = P(*_POLES[key])
                b.pins.append(rider_svg(fl, [gil, pole], t, 0.9,
                                        band_dots(1), t_hide=t + 0.9))
                b.fills.append(tribe_path(rings, col, 0.0,
                                          op_anim(0.0, TRIBE_FOCUS, t + 0.8,
                                                  0.5)))
                b.ends.append(t + 1.3)
            elif ref == (13, 20):
                b.fills.append(tribe_path(rings, col, TRIBE_FOCUS,
                                          op_anim(TRIBE_FOCUS, base, 0.0,
                                                  0.8)))
            elif key == "BENJAMIN" and ref == (13, 21):
                b.fills.append(tribe_path(rings, col, base,
                                          op_anim(base, TRIBE_FOCUS, 4.4,
                                                  0.8)))
            elif key == "BENJAMIN" and ref == (13, 22):
                b.fills.append(tribe_path(rings, col, TRIBE_FOCUS,
                                          op_anim(TRIBE_FOCUS, base, 0.0,
                                                  0.8)))
            else:
                b.fills.append(tribe_path(rings, col, base))
            for r in rings:
                b.cls["tribe"].append(poly_el(PS(r + r[:1]),
                                              stroke=SAND_DIM))
                b.qc.append((PS(r + r[:1]), "area", key))
        if ref == (13, 21):
            for r in G.TRIBE_RINGS["BENJAMIN"]:
                b.cls["tribe_hl"].append(
                    f'<polyline points="{ptsstr(PS(r + r[:1]))}" '
                    f'fill="none" stroke="{rgb(HL)}" opacity="0">'
                    f'{pulse_once(4.4)}</polyline>')
            b.units.append(Unit("benjamin", "Benjamin", [S_OTHER], TEXT,
                                italic=True,
                                cands=[(31.92, 35.12, "c"),
                                       (31.80, 35.11, "c"),
                                       (31.96, 35.20, "c"),
                                       (31.88, 35.08, "c"),
                                       (31.98, 35.33, "c"),
                                       (31.76, 35.36, "c")],
                                prio=2, new=True, must=True))

    # seven towers stand and fall in the hill country (13:19)
    if ref == (13, 19):
        tw = fig_svg(F.tower(), 36, SAND, unit_h=MAN_H * F.UNIT["tower"])
        for k, (la, lo) in enumerate(G.TOWERS):
            t_up, t_fall = 1.8 + k * 0.05, 2.4 + k * 0.15
            inner = (f'<g opacity="0">{fade(t_up, 0.4)}'
                     f'{fade(t_fall + 0.9, 0.5, out=True)}<g>'
                     f'<animateTransform attributeName="transform" '
                     f'type="rotate" values="0;80" begin="{t_fall:.2f}s" '
                     f'dur="0.6s" fill="freeze" calcMode="spline" '
                     f'keyTimes="0;1" keySplines="{EASE}"/>{tw}</g></g>')
            b.pins.append(pin_svg(fl, la, lo, inner))
        b.ends.append(2.4 + 6 * 0.15 + 1.4)

    # the judges: a spark in each of six towns (13:20)
    if ref == (13, 20):
        t0 = max(t_land, 0.2) + 0.1
        for k, key in enumerate(G.JUDGES):
            xy = at_rest(cam1, *S[key])
            t = t0 + k * 0.22
            b.overlay.append(f'<circle cx="{xy[0]:.1f}" cy="{xy[1]:.1f}" '
                             f'r="4" fill="{rgb(SAND)}" stroke="{rgb(BG)}" '
                             f'stroke-width="1.5" opacity="0">'
                             f'{fade(t, 0.3)}</circle>')
            b.overlay.append(screen_ring(xy, t, 5, 26, 0.8))
            b.obstacles.append(("spark", (xy[0] - 7, xy[1] - 7,
                                          xy[0] + 7, xy[1] + 7)))
        b.units.append(Unit("judges", "judges", [S_OTHER], TEXT,
                            italic=True,
                            cands=[(32.30, 34.80, "c"), (31.62, 34.72, "c"),
                                   (32.42, 35.00, "c"), (31.95, 34.88, "c"),
                                   (32.15, 35.95, "c")],
                            prio=2, new=True, must=True))
        b.ends.append(t0 + 5 * 0.22 + 0.8)

    # the pinned people and emblems
    for key, (site, r_in, t_in, r_settle, r_last, name) in PINS.items():
        la, lo = S[site]
        if i < IDX[r_in]:
            continue
        last = IDX[r_last]
        settle = IDX[r_settle] if r_settle else None
        if ref == r_in:
            b.pins.append(pin_svg(fl, la, lo,
                                  lift_in(pin_figure(key, TEXT), t_in)))
            ax, ay = at_rest(cam1, la, lo)
            x0, y0, x1, y1 = PIN_BOX[key]
            b.obstacles.append(("pin", (ax + x0, ay + y0, ax + x1, ay + y1)))
            b.ends.append(t_in + 0.6)
            if name:
                b.units.append(pin_label(key, name, la, lo, cam1, HL, True,
                                         1, True, True))
                b.units[-1].t_want = t_in + 0.4
        elif settle is None or i < settle:
            # held as a figure (with a narrated change of pose)
            if key == "john" and ref == (13, 25):
                b.pins.append(pin_svg(fl, la, lo,
                                      f'<g>{fade(9.6, 0.6, out=True)}'
                                      + pin_figure(key, TEXT) + "</g>"
                                      + f'<g opacity="0">{fade(9.6, 0.6)}'
                                      + pin_figure(key, TEXT, kneel=True)
                                      + "</g>"))
                b.ends.append(10.2)
            elif key == "manger" and i == IDX[r_last] + 1:
                b.pins.append(pin_svg(fl, la, lo,
                                      f'<g>{fade(0.0, 0.6, out=True)}'
                                      + pin_figure(key, TEXT) + "</g>"))
            elif i <= last:
                b.pins.append(pin_svg(fl, la, lo, pin_figure(key, TEXT)))
            if i <= last:
                ax, ay = at_rest(cam1, la, lo)
                x0, y0, x1, y1 = PIN_BOX[key]
                b.obstacles.append(("pin", (ax + x0, ay + y0, ax + x1,
                                            ay + y1)))
                if name:
                    b.units.append(pin_label(key, name, la, lo, cam1, HL,
                                             True, 1, True, True))
        else:
            # settled: the figure goes, a dot and its name stay
            if i == settle:
                kneel = key == "john"
                b.pins.append(pin_svg(fl, la, lo,
                                      f'<g>{fade(0.0, 0.6, out=True)}'
                                      + pin_figure(key, TEXT, kneel=kneel)
                                      + "</g>"))
            if name and i <= last:
                b.units.append(Unit("pin_" + key, name, [S_OTHER],
                                    TEXT_DIM, italic=True,
                                    cands=[(la, lo, c) for c in "rlab"],
                                    dot=SAND, prio=4))

    # 13:23 the manger beside David: an emblem, gold, never pulsed
    # (drawn by PINS); 13:24 the Jordan where John baptizes
    if ref == (13, 24):
        jr = [q for q in G.RIVERS["jordan"] if 31.72 <= q[0] <= 31.98]
        b.cls["story_trace"].append(
            f'<polyline points="{ptsstr(PS(jr))}" fill="none" '
            f'stroke="{rgb(HL)}" opacity="0">{pulse_once(2.8)}</polyline>')
        b.ends.append(3.6)

    # 13:25 the light comes down the valley to John; 13:26 it goes
    j_at = (31.86, 35.66)
    if ref == (13, 25):
        down = [q for q in G.RIVERS["jordan"] if q[0] >= 31.95]
        path = ([(32.72, 35.57)] + [q for q in down if q[0] < 32.70]
                + [(31.90, 35.58), j_at])
        b.pins.append(rider_svg(fl, PS(path), 7.0, 2.4, light_svg()))
        b.ends.append(9.4)
    elif ref == (13, 26):
        b.pins.append(pin_svg(fl, *j_at, f'<g>{fade(0.0, 0.8, out=True)}'
                              + light_svg() + "</g>"))

    # 13:26 Jerusalem relights, where the word starts
    if ref == (13, 26):
        la, lo = city_pt("jerusalem")
        b.units.append(Unit("jerusalem", "Jerusalem", [S_CUR], HL, bold=True,
                            cands=[(la, lo, c) for c in "lrab"], dot=HL,
                            prio=1, new=True, must=True, min_px=20))
        b.units[-1].t_want = 3.0

    # 13:26 one glint runs along the journey already travelled
    if ref == (13, 26):
        out = []
        for lg in LEGS:
            if IDX[lg[4]] <= IDX[(13, 14)] and lg[3] != "john":
                pts = lg[5] if not out else lg[5][1:]
                out += pts
        w = PS(out)
        L = seg_len(w)
        gl = 40 / cam1[0]
        b.cls["glint"].append(
            f'<polyline points="{ptsstr(w)}" fill="none" '
            f'stroke="{rgb(HL)}" stroke-linecap="round" '
            f'stroke-dasharray="{_fmt(gl)} {_fmt(L * 2)}" '
            f'stroke-dashoffset="{_fmt(gl)}" opacity="0">'
            f'<set attributeName="opacity" to="1" begin="4.6s"/>'
            f'<animate attributeName="stroke-dashoffset" '
            f'values="{_fmt(gl)};{_fmt(-L)}" begin="4.6s" dur="1.6s" '
            f'fill="freeze" calcMode="spline" keyTimes="0;1" '
            f'keySplines="{EASE}"/></polyline>')
        b.ends.append(6.2)

    # the story's own region names: lit on their verse, dim after
    for key, text, cands, r0 in (
            ("egypt", "EGYPT", [(30.30, 31.00), (30.55, 30.55),
                                (29.95, 31.45), (30.35, 31.55)], (13, 17)),
            ("wild", "WILDERNESS", [(29.55, 33.85), (29.85, 33.65),
                                    (29.35, 34.20), (29.95, 34.10)],
             (13, 18))):
        if IDX[r0] <= i <= IDX[(13, 41)]:
            lit = ref == r0
            b.units.append(Unit("rg_" + key, text, [S_AREA, S_OTHER],
                                HL if lit else TEXT_DIM, bold=lit,
                                cands=[(a, c, "c") for a, c in cands],
                                prio=2 if lit else 6, new=lit, must=lit))
            if lit:
                b.units[-1].t_want = 3.8 if key == "egypt" else 2.2

    # 13:47 a light for the Gentiles, to the uttermost parts of the earth
    if ref == (13, 47):
        xy = at_rest(cam1, *city_pt("pantioch"))
        for k in range(3):
            b.overlay.append(screen_ring(xy, 6.6 + k * 0.4, 8, 760, 2.0,
                                         width=2.5))
        b.ends.append(8.6)

    # 13:50 thrown out of their borders: Antioch's territory, held after
    if i >= IDX[(13, 50)]:
        ring = PS(G.ANTIOCH_TERRITORY + G.ANTIOCH_TERRITORY[:1])
        if ref == (13, 50):
            b.cls["terr_trace"].append(traced_el(ring, HL + (242,), 7.8,
                                                 1.4)[0])
            b.ends.append(9.2)
        else:
            b.cls["terr"].append(poly_el(ring, stroke=SAND_DIM))
            if ref == (13, 51):
                b.cls["story_let"].append(
                    poly_el(ring, stroke=HL + (242,))[:-2] + ">"
                    + fade(0.0, LET_GO, out=True) + "</polyline>")

    # 13:51 they shook off the dust of their feet
    if ref == (13, 51):
        road_ = next(lg for lg in LEGS if lg[0] == "pa_i")[5]
        at = crossing_pt(road_, G.ANTIOCH_TERRITORY)
        xy = at_rest(cam1, *at)
        for k in range(6):
            a = math.radians(k * 60 + 15)
            x1, y1 = xy[0] + 14 * math.cos(a), xy[1] + 14 * math.sin(a)
            b.overlay.append(
                f'<circle cx="{xy[0]:.1f}" cy="{xy[1]:.1f}" r="2" '
                f'fill="{rgb(SAND)}" opacity="0">'
                f'<set attributeName="opacity" to="1" begin="0.2s"/>'
                f'<animate attributeName="cx" values="{xy[0]:.1f};{x1:.1f}" '
                f'begin="0.2s" dur="0.6s" fill="freeze"/>'
                f'<animate attributeName="cy" values="{xy[1]:.1f};{y1:.1f}" '
                f'begin="0.2s" dur="0.6s" fill="freeze"/>'
                f'{fade(0.5, 0.3, out=True)}</circle>')
        b.ends.append(0.8)

    # the interim light at Jerusalem (13:30-37), until the Jerusalem card
    if IDX[(13, 30)] <= i <= IDX[(13, 38)]:
        la, lo = city_pt("jerusalem")
        inner = light_svg()
        if ref == (13, 30):
            inner = lift_in(inner, 0.2, 0.6, 10)
            b.ends.append(0.8)
        elif ref == (13, 38):
            inner = f'<g>{fade(0.0, 0.6, out=True)}{inner}</g>'
        b.pins.append(pin_svg(fl, la + 0.012, lo + 0.03, inner))
        ax, ay = at_rest(cam1, la + 0.012, lo + 0.03)
        b.obstacles.append(("pin", (ax - 16, ay - LIGHT_PX - 4, ax + 16,
                                    ay + 2)))
    return b


def crossing_pt(path, ring):
    """Where a road (lat/lon) first crosses a ring's edge."""
    from svg_map_camera import seg_x
    rp = PS(ring + ring[:1])
    pw = PS(path)
    for p0, p1 in zip(pw, pw[1:]):
        for a, c in zip(rp, rp[1:]):
            x = seg_x(p0, p1, a, c)
            if x:
                return PROJ.latlon(*x)
    return path[len(path) // 2]


# ---------------------------------------------------------------------------
# Verse assembly
# ---------------------------------------------------------------------------

def build_all():
    prev = None          # the names of the last verse that placed any
    last_cam = None      # where the last verse's camera rested
    report = []
    shore, shore_qc = base_layers()
    shore += [("relief", el) for el in relief()]
    for ref in REFS:
        ch, v = ref
        cam1 = STAGE[ref]["cam"]
        cam0 = OPEN if last_cam is None else last_cam
        narr = NARR[ref]
        fl = plan(ref, cam0)
        assert _same(fl.cam1, cam1), ref
        last_cam = cam1
        t_land = fl.dur
        t_tr0 = t_land + 0.1
        D_tr = round(max(1.2, min(4.0, narr - AUDIO_SLACK - t_land - 0.6)),
                     2)
        st = STAGE[ref]
        if "trace_at" in st:
            t_tr0, D_tr = st["trace_at"]
        cls, route_qc, traces, tr_end = route_layers(ref, cam1, t_tr0, D_tr)
        sea_rect = [el for name, el in shore if name is None]
        for name, el in shore:
            if name:
                cls[name].append(el)
        zs = [c[0] / LYS.S for c in fl.cams]
        in_card = zs[-1] >= 0.2               # it rests inside the card
        show_map = min(zs) < CARD_COVER       # the map is seen at all
        show_card = max(zs) >= CARD_IN[0]
        bt = story_beats(ref, fl, cam1, t_land)
        for name, els in bt.cls.items():
            cls.setdefault(name, []).extend(els)
        units_ = units(ref) + bt.units

        # screen geometry at rest for the QC / layout
        lines, lines_w = [], []
        for pts, kind, key in shore_qc + route_qc + bt.qc:
            if kind == "river":
                continue          # a name may cross a river, as on a map
            wpx = 3.0 if kind == "route" else 2.0
            lines.append(([to_screen(cam1, p) for p in pts], wpx, kind, key))
            lines_w.append((pts, wpx))
        hud = hud_rects(ref, cam1) + bt.obstacles
        half = inset_opacity(cam1, ref) not in (0.0, 1.0)
        if in_card:
            # no names to place on a map nobody sees: the last verse's stay
            # as they were until the card covers them
            placed, dropped, problems = [], [], []
            card_names = prev if show_map else None
            ends_card = card_ends(ref)
            sea_rect = sea_rect if show_map else []
            if not show_map:
                cls = {k: [] for k in cls}
                bt.fills, bt.pins, bt.overlay = [], [], []
            text = assemble(ref, fl, cls, bt, sea_rect, None, card_names,
                            show_card, show_map, zs)
            write(ref, text)
            report.append(dict(
                ref=ref, pxdeg=round(cam1[0] * K, 1), cam=round(fl.dur, 2),
                end=round(max([fl.dur] + ends_card), 2), narr=narr,
                kb=round(len(text.encode()) / 1024, 1), dropped=[],
                problems=[], mid=[], dips=[], half=False, ext=card_extent(fl)))
            continue
        dots = rest_dots(PROJ, units_, cam1, hud)
        ctx = make_ctx(cam1, lines, dots, hud)
        placed, dropped, problems = layout(units_, ctx, prev)
        prev_units = prev["units"] if prev else {}
        cur_ident = identities(placed, cam1)

        # new names arrive with the route: a town as its leg reaches it
        arrive = {}
        for lg, b, d in traces:
            if lg[3] == "john":
                arrive["john"] = b + d * 0.6
            else:
                arrive[lg[2]] = b + d - 0.15
        for u in units_:
            u.t_in = None
            if unchanged(u, cur_ident, prev_units):
                continue
            if u.new:
                t = arrive.get(u.key, t_land + 0.05)
                if u.key == st["city"] and "city_at" in st:
                    t = st["city_at"]
                t = getattr(u, "t_want", t)
                u.t_in = round(max(0.0, t), 2)

        lab = emit_labels(PROJ, units_, placed, cur_ident, prev,
                          prev is not None, cam0, cam1, fl, t_land, hud,
                          lambda cam, ref=ref: hud_rects(ref, cam), lines_w,
                          problems)

        text = assemble(ref, fl, cls, bt, sea_rect, lab, None, show_card,
                        True, zs)
        write(ref, text)

        # -------- QC ---------------------------------------------------
        mid = midflight_qc(fl, placed, lab["exiting"])
        ends = [tr_end] + bt.ends + [getattr(u, "t_show", 0) + 0.5
                                     for u in placed
                                     if getattr(u, "t_show", 0) > 0]
        end = max(ends + [fl.dur])
        report.append(dict(
            ref=ref, pxdeg=round(cam1[0] * K, 1), cam=round(fl.dur, 2),
            end=round(end, 2), narr=narr,
            kb=round(len(text.encode()) / 1024, 1),
            dropped=[u.key for u in units_
                     if u.key in dropped and anchor_on_screen(u, cam1)],
            problems=problems, mid=mid, dips=lab["dips"], half=half,
            ext=extent_check(fl, PROJ, WORLD_LAT, WORLD_LON)))
        prev = prev_state(cam1, placed, cur_ident, lab["cur_dots"])
    return report


def assemble(ref, fl, cls, bt, sea_rect, lab, held, show_card, show_map, zs):
    """One verse's SVG: the map in the camera group (hidden whenever the
    card fills the frame), the card over it, then the HUD."""
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" '
           f'viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
           f'font-family="{FONT_FAMILY}">',
           f'<rect width="{W}" height="{H}" fill="{rgb(BG)}"/>',
           fl.open_camera()]
    if show_map:
        vis = ["hidden" if z >= CARD_COVER else "visible" for z in zs]
        svg.append(f'<g visibility="{vis[0]}">'
                   + discrete(fl, "visibility", vis))
        svg += sea_rect
        svg.append(emit(fl, "coast", cls["coast"]))
        svg += bt.fills
        for name in ("tribe", "lake", "relief", "river", "story",
                     "story_let", "terr", "tribe_hl") + ROUTE_ORDER + (
                         "terr_trace", "story_trace", "glint"):
            svg.append(emit(fl, name, cls[name]))
        svg += bt.pins
        if lab is not None:
            svg += emit_label_layers(fl, lab)
        elif held:
            svg += held_labels(fl, held)
        svg.append("</g>")
    if show_card:
        ops = [f"{card_op(z):.2f}" for z in zs]
        svg.append(f'<g opacity="{ops[0]}">{fl._anim("opacity", ops)}'
                   + LYS.svg(ref, fl, 18, TEXT, HL) + "</g>")
    svg.append("</g></g>")
    if show_map:
        svg += bt.overlay
    svg.append(hud_svg(ref, fl, zs))
    svg.append(inset_svg(ref, fl))
    svg.append("</svg>")
    return "".join(svg)


def discrete(fl, attr, vals):
    """A non-numeric attribute switched at the camera's keyframes."""
    if fl.static or len(set(vals)) == 1:
        return ""
    n = len(vals) - 1
    kt = ";".join(f"{i / n:.4f}" for i in range(n + 1))
    return (f'<animate attributeName="{attr}" values="{";".join(vals)}" '
            f'keyTimes="{kt}" calcMode="discrete" dur="{fl.dur:.2f}s" '
            f'begin="0s" fill="freeze"/>')


def held_labels(fl, prev):
    """The previous verse's names, still, until the card covers them."""
    by_size, lead, halo, core = {}, [], [], []
    for pu in prev["units"].values():
        u = pu["unit"]
        label_elements(u, u.place, "", None, by_size, lead, prev["cam1"])
    lab = dict(by_size=by_size, lead_els=lead, halo=halo, core=core,
               old_by_size={}, old_lead=[], old_halo=[], old_core=[])
    return emit_label_layers(fl, lab)


def write(ref, text):
    """Write a verse's SVG. A file another program has open for a moment
    (a virus scan, a preview) fails on Windows with EINVAL: try again."""
    ch, v = ref
    path = out_path("Acts", ch, f"Acts_{ch}_{v}.svg")
    for attempt in range(5):
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            return
        except OSError:
            if attempt == 4:
                raise
            time.sleep(0.3)


def card_ends(ref):
    return [t + d for _k, _a, t, d, _v in LYS.events.get(ref, [])]


def card_extent(fl):
    """Inside the card, is its edge ever in frame?"""
    w, h = LYS.size
    x0, y0 = LYS.origin
    ax, ay = LYS.anchor
    tx, ty = LYS.town_xy
    for c in fl.cams:
        z = c[0] / LYS.S
        if z < CARD_COVER:
            continue
        cx = ax + (c[1] - tx) * LYS.S
        cy = ay + (c[2] - ty) * LYS.S
        hw, hh = W / 2 / z, H / 2 / z
        if cx - hw < x0 or cy - hh < y0 or cx + hw > x0 + w or \
                cy + hh > y0 + h:
            return "card edge visible"
    return None


def anchor_on_screen(u, cam):
    """Whether a name's place is in the rest frame: a dropped name the
    camera simply isn't looking at is no loss worth reporting."""
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
            notes.append("WORLD EDGE visible")
        if r["half"]:
            notes.append("the inset rests half-faded")
        ch, v = r["ref"]
        for n in notes:
            print(f"  {ch}:{v}: {n}")
    missing = [r for r in REFS if _narration(r) is None]
    if missing:
        print(f"  no MP3 for {missing}: paced at {NARR_FALLBACK}s")
    kb = [r["kb"] for r in report]
    print(f"Acts 13-14: {len(report)} SVG files, {sum(kb):.0f} KB "
          f"(largest {max(kb)} KB)")


if __name__ == "__main__":
    main()
