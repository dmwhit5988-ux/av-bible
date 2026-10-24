"""Render Numbers 34 as per-verse vector SVGs: a camera tour of the land.

One large map is drawn in every verse and seen through a moving camera (SMIL
animateTransform translate + scale on the world group), the way 1 Chronicles
1-9 flies over its family tree. Each verse opens on the previous verse's
rest camera and flies to its own, so played in order the chapter is one
continuous flight (SHOTS and plan() are the shot list):

* vv1-15 trace the border of Greater Canaan, one stretch per verse, in
  close-up. The whole land is the wide shot at vv1-2 and again once the
  border closes (vv12-13); vv2 and 13 first sweep slowly along the land.
  vv14-15 show the two and a half tribes east of the Jordan.
* vv16-29 the twelve tribal territories: all twelve at vv17-18 and 29, and
  on each prince's verse a close-up of his tribe, its land growing in and
  its border tracing round, with the prince on a plate at top right.

A fixed overview inset (bottom left) shows the whole territory, with the
camera's view boxed, whenever the camera is in close; it fades away in the
wide shots.

What stays a constant screen size while the camera zooms (one inverse-scale
animation per class, which the children inherit): stroke widths, the dashed
underlay's dashes, the dots, and the names (font-size animates as
base * grow(s) / s, offsets in em), so no name balloons mid-flight.

Names are laid out at each verse's rest camera by a clash test on Georgia
ink boxes measured with PIL: a name never touches another name, a line, a
dot, the frame edge or a plate, and a tribe's name sits inside its own land
when it fits. A name that would slide under the title or scale plate
mid-flight dips out once and comes back. Everything lands before the verse's
narration ends: the pacing comes from the MP3s in web/audio.

The geometry, border, territories, landmarks and princes come from
generate_tribal_maps.py; the camera arc and the MP3 timer from
svg_chronicles_world.py.

Run inside the project venv:
    .venv\\Scripts\\python.exe generate_numbers34_svg.py
It prints any name it had to drop or force, and anything that would land
after the narration.
"""

import os
from xml.sax.saxutils import escape

from config import WEB_AUDIO_DIR
from passages import verse_numbers
from svg_surface import _fmt, FONT_FAMILY
from svg_chronicles_world import AUDIO_SLACK, _mp3_seconds
from svg_map_camera import (
    Projection, Flight, Unit as MapUnit, Ctx, GROW_MAX, grow, cam_duration,
    ease_inv, _same, to_screen, ink, title_rect, compass_rect, title_svg,
    compass_scale_svg, inset_view_rect, inner_points, rr_hit, pip, poly_el,
    ptsstr, rgb, fade, op_anim, traced_el, frac_along, emit_class as emit_px,
    layout, rest_dots, identities, unchanged, emit_labels, emit_label_layers,
    prev_state, midflight_qc, extent_check, S_OTHER, S_AREA, S_CUR,
)
from generate_tabernacle import (W, H, BG, SAND, SAND_DIM, TEXT, TEXT_DIM, HL,
                                 out_path)
from generate_tribal_maps import (
    TRIBES, TRIBE_RINGS, WEST_TRIBES, EAST_TRIBES, TRIBE_COL, PRINCES,
    SEA, LAND, RIVER, WATER_TXT, LAKES, RIVERS, BORDER_SEGS, CANAAN_POLY,
    WORLD_COAST, WORLD_LAND, WORLD_SEAS, WORLD_LAT, WORLD_LON,
    LANDMARKS34, CURRENT34, MODERN34,
)


VERSES = verse_numbers("Numbers", 34)
NARR_FALLBACK = 6.0            # seconds, for a verse with no MP3 yet


def _narration(v):
    """The verse's narration in seconds, to a tenth: a re-render that moves
    a clip by a few milliseconds leaves the pictures unchanged."""
    sec = _mp3_seconds(os.path.join(WEB_AUDIO_DIR, f"Numbers_34_{v}.mp3"))
    return round(sec, 1) if sec else None


NARR = {v: _narration(v) or NARR_FALLBACK for v in VERSES}

# ---------------------------------------------------------------------------
# Projection: one world, 100 world units per degree of latitude, so a camera
# scale s shows the map at 100*s px per degree.
# ---------------------------------------------------------------------------

PROJ = Projection(36.0, 30.0, 32.3)
K, EFF = PROJ.k, PROJ.eff
P, PS = PROJ.P, PROJ.PS
shot, fit, unproject = PROJ.shot, PROJ.fit, PROJ.unproject


def _clip_half(poly, a, b, keep):
    """Sutherland-Hodgman: the part of poly on keep's side of line a-b."""
    def side(p):
        pa, pb, pp = P(*a), P(*b), P(*p)
        return ((pb[0] - pa[0]) * (pp[1] - pa[1])
                - (pb[1] - pa[1]) * (pp[0] - pa[0]))
    sk = side(keep) > 0
    out = []
    for i, cur in enumerate(poly):
        nxt = poly[(i + 1) % len(poly)]
        sc, sn = side(cur), side(nxt)
        cin, nin = (sc > 0) == sk, (sn > 0) == sk
        if cin:
            out.append(cur)
        if cin != nin:
            t = sc / (sc - sn)
            out.append((cur[0] + t * (nxt[0] - cur[0]),
                        cur[1] + t * (nxt[1] - cur[1])))
    return out


# vv14-15 show east Manasseh against the Numbers 34 border: clipped to the
# east of the Riblah - Chinnereth line, so it never spills into Canaan.
RINGS_A = dict(TRIBE_RINGS)
RINGS_A["MANASSEH_E"] = [_clip_half(TRIBE_RINGS["MANASSEH_E"][0],
                                    (32.85, 35.65), (33.40, 36.30),
                                    (32.60, 36.15))]

# ---------------------------------------------------------------------------
# HUD (screen space, never scaled)
# ---------------------------------------------------------------------------

SCALE_KM = 50
INSET_RECT = (14, H - 14 - 168, 14 + 118, H - 14)   # x0, y0, x1, y1


def prince_lines(v):
    key, prince = PRINCES[v][0], PRINCES[v][1]
    return TRIBES[key][0], "prince: " + prince


def prince_rect(v):
    """One plate size for all ten princes, so the HUD never changes size."""
    wmax = 0
    for pv in PRINCES:
        t1, t2 = prince_lines(pv)
        r1 = ink(t1, 26, True, False, "ra")
        r2 = ink(t2, 20, False, False, "ra")
        wmax = max(wmax, -r1[0], -r2[0])
    return (W - 18 - wmax - 14, 4, W - 4, 4 + 14 + 30 + 26 + 8)


TITLE_A = "The Borders of the Land — Numbers 34"
TITLE_B = "Dividing the Inheritance — Numbers 34"


def section(v):
    return "A" if v <= 15 else "B"


# inset (optional variant): the inset shows only while the camera is in
# close: hidden when the view covers most of the inset's own box
INSET_BOX_A = (30.45, 34.62, 33.6, 37.4)    # lat0, lat1, lon0, lon1
INSET_BOX_B = (30.50, 33.50, 33.7, 36.8)
INSET_OFF, INSET_RAMP = 0.82, 0.07     # hidden once the view is this tall a
                                       # share of the box; full below by RAMP


def inset_opacity(cam, sec):
    la0, la1, _a, _b = INSET_BOX_A if sec == "A" else INSET_BOX_B
    hfrac = (H / cam[0] / K) / (la1 - la0)
    # every rest shot falls outside the ramp (build_all checks), so the
    # inset is wholly on or off whenever the camera is still
    return max(0.0, min(1.0, (INSET_OFF - hfrac) / INSET_RAMP))


def hud_rects(v, cam):
    sec = section(v)
    title = TITLE_A if sec == "A" else TITLE_B
    hud = [("title", title_rect(title)),
           ("compass", compass_rect(PROJ, cam[0], SCALE_KM))]
    if v in PRINCES:
        hud.append(("prince", prince_rect(v)))
    if inset_opacity(cam, sec) > 0.05:
        hud.append(("inset", INSET_RECT))
    return hud


# ---------------------------------------------------------------------------
# The shot list
# ---------------------------------------------------------------------------

# whole border, tight: the land (lat 30.63-34.45) fills the frame height
WIDE_A1 = fit(30.63, 34.45, 33.80, 37.24, (0, 12, W, H - 12))
# whole border with every landmark named (v12 rests here, v13 holds it):
# a little headroom for the north names
WIDE_A2 = fit(30.45, 34.47, 33.80, 37.24, (0, 10, W, H - 10))
OPEN_A = shot(32.54, 35.52, 126)            # v1 opens a little wider
COAST_A = fit(31.10, 34.50, 33.60, 36.0, (0, 12, W, H - 12))   # west border
CLOSE = 400                                  # border close-ups, px/deg
SURVEY = 240                                 # survey legs in v2 / v13
SURV_N = shot(33.33, 36.15, SURVEY)
SURV_S = shot(31.72, 34.80, SURVEY)
EAST = shot(32.36, 35.98, 262)               # the east bank, vv14-16
# all twelve territories (lat 30.63-33.43), room above for Naphtali's name
WIDE_B = fit(30.60, 33.47, 33.80, 36.65, (0, 10, W, H - 10))

SHOTS_A = {
    1: WIDE_A1, 2: WIDE_A1,
    3: shot(30.92, 35.32, CLOSE),
    4: shot(30.84, 34.72, CLOSE),
    5: shot(30.96, 34.12, CLOSE),
    6: COAST_A,
    7: shot(34.20, 36.12, CLOSE),
    8: shot(34.20, 36.50, CLOSE),
    9: shot(34.20, 36.86, CLOSE),
    10: shot(33.96, 36.86, CLOSE),
    11: shot(33.24, 36.0, CLOSE),
    12: WIDE_A2,
    13: WIDE_A2,
    14: EAST,
    15: EAST,
}

B_VIEW = (40, 96, W - 40, H - 24)           # framing area under the HUD
B_CAP = {"ISSACHAR": 580.0, "NAPHTALI": 650.0, "ZEBULUN": 600.0,
         "BENJAMIN": 560.0, "SIMEON": 560.0}


def tribe_shot(keys):
    pts = [p for k in keys for p in TRIBE_RINGS[k][0]]
    lats = [p[0] for p in pts]
    lons = [p[1] for p in pts]
    la0, la1, lo0, lo1 = min(lats), max(lats), min(lons), max(lons)
    bw = (lo1 - lo0) * EFF + 0.25
    bh = (la1 - la0) + 0.18
    vx0, vy0, vx1, vy1 = B_VIEW
    pxdeg = min((vx1 - vx0) / bw, (vy1 - vy0) / bh)
    pxdeg = max(360.0, min(B_CAP.get(keys[0], 480.0), pxdeg))
    return shot((la0 + la1) / 2, (lo0 + lo1) / 2, round(pxdeg),
                (vx0 + vx1) / 2, (vy0 + vy1) / 2)


SHOTS_B = {16: EAST, 17: WIDE_B, 18: WIDE_B, 29: WIDE_B}
for _v, (_k, *_rest) in PRINCES.items():
    SHOTS_B[_v] = tribe_shot([_k] + (["MANASSEH_E"] if _v == 23 else []))
SHOTS = {**SHOTS_A, **SHOTS_B}
WIDE_VERSES_B = (17, 18, 29)


NEED_AFTER = {1: 0.5, 13: 0.5, 15: 0.6, 16: 0.4, 17: 1.0, 18: 0.4,
              29: 1.0}


def plan(v, cam0):
    """The verse's camera legs."""
    cam1 = SHOTS[v]
    narr = NARR[v]
    if v == 2:        # survey north -> south, then settle on the whole land
        legs = [("hold", None, 0.4), ("to", SURV_N, 1.7),
                ("hold", None, 0.3), ("to", SURV_S, 3.4),
                ("hold", None, 0.3), ("to", cam1, 1.9)]
    elif v == 13:     # survey south -> north, then settle
        legs = [("hold", None, 0.3), ("to", SURV_S, 1.8),
                ("hold", None, 0.3), ("to", SURV_N, 3.4),
                ("hold", None, 0.3), ("to", cam1, 1.9)]
    elif v == 12:     # pull back to the closed border while the Jordan traces
        legs = [("to", cam1, 3.0)]
    else:
        D = cam_duration(cam0, cam1)
        need = NEED_AFTER.get(v, 1.4)
        if D:
            D = round(max(0.9, min(D, narr - AUDIO_SLACK - need)), 2)
        legs = [("to", cam1, D)]
    return Flight(cam0, legs)


# ---------------------------------------------------------------------------
# Labels (svg_map_camera.Unit, on this map's projection)
# ---------------------------------------------------------------------------

class Unit(MapUnit):
    proj = PROJ


POLE = {k: PROJ.pole(r) for k, r in TRIBE_RINGS.items()}



# ---------------------------------------------------------------------------
# Section A units (vv1-15)
# ---------------------------------------------------------------------------

LM_PRIO = {"kadesh": 3, "lebo": 3, "mount_hor": 4, "hazar_enan": 4,
           "akrabbim": 4, "riblah": 5, "zedad": 6, "ziphron": 6,
           "shepham": 6, "azmon": 7, "hazar_addar": 7}


def tribe_cands(rings):
    return lambda cam, hud: [(a, b, "c") for a, b in
                             inner_points(PROJ, rings, cam, hud)]


def units_A(v):
    cur = CURRENT34.get(v, set())
    U = []

    def style(key, fill, italic=False, base=S_OTHER, gmax=GROW_MAX):
        if key in cur:
            return dict(bases=[S_CUR], fill=HL, bold=True, italic=italic,
                        new=True, prio=1, must=True, min_px=20)
        return dict(bases=[base], fill=fill, bold=False, italic=italic,
                    prio=5, gmax=gmax)

    def area(key, text, fill, cands, italic=True, prio=6, **kw):
        st = style(key, fill, italic, base=S_AREA, gmax=1.25)
        if prio is not None and key not in cur:
            st["prio"] = prio
        U.append(Unit(key, text, cands=[(a, b, c) for a, b, c in cands],
                      sub=MODERN34.get((key, v)), **st, **kw))

    area("sea", "The Great Sea", WATER_TXT,
         [(32.70, 34.25, "c"), (32.20, 34.35, "c"), (33.40, 34.70, "c"),
          (31.75, 34.10, "c"), (34.00, 35.15, "c"), (31.45, 33.80, "c"),
          (32.90, 34.50, "c")], in_sea=True, prio=5)
    area("salt", "Salt Sea", WATER_TXT,
         [(31.30, 35.57, "r"), (31.45, 35.58, "r"), (31.15, 35.53, "r"),
          (31.40, 35.40, "l")])
    area("chin", "Chinnereth", WATER_TXT,
         [(32.80, 35.64, "r"), (32.86, 35.64, "r"), (32.72, 35.62, "r"),
          (32.80, 35.52, "l")])
    area("edom", "EDOM", TEXT_DIM,
         [(30.80, 35.80, "c"), (30.95, 35.95, "c"), (30.62, 35.90, "c"),
          (31.10, 36.05, "c"), (30.62, 35.75, "c"), (30.52, 35.55, "c")],
         italic=False, out_poly=CANAAN_POLY, prio=7)
    area("zin", "wilderness of Zin", TEXT_DIM,
         [(30.62, 35.40, "c"), (30.55, 35.10, "c"), (30.70, 35.55, "c"),
          (30.75, 35.70, "c"), (30.58, 35.25, "c"), (30.52, 34.95, "c"),
          (30.45, 34.80, "c")], out_poly=CANAAN_POLY)
    if v >= 5:
        area("brook", "Brook of Egypt", TEXT_DIM if v != 5 else TEXT,
             [(30.95, 34.00, "bl"), (30.95, 34.00, "l"),
              (31.05, 33.90, "al"), (30.85, 33.95, "bl")], italic=True)
    if v >= 12:
        area("jordan", "Jordan", WATER_TXT,
             [(32.30, 35.53, "l"), (32.45, 35.54, "l"), (32.15, 35.53, "l"),
              (32.30, 35.58, "r")])
    for key, text, la, lo, cands in (
            ("damascus", "Damascus", 33.51, 36.29, ["l", "al", "bl", "a"]),
            ("jerusalem", "Jerusalem", 31.78, 35.23, ["l", "al", "bl"])):
        if key == "jerusalem" and v == 15:
            continue           # beside Jericho it would read as its gloss
        U.append(Unit(key, text, [S_OTHER], TEXT_DIM, italic=True,
                      cands=[(la, lo, c) for c in cands], dot=SAND_DIM,
                      prio=7))
    for key, name, la, lo, v0, cands, unc in LANDMARKS34:
        if v < v0:
            continue
        txt = name + " ?" if unc else name
        st = style(key, TEXT)
        if key not in cur:
            st["prio"] = LM_PRIO.get(key, 5)
        U.append(Unit(key, txt, cands=[(la, lo, c) for c in cands],
                      dot=HL if key in cur else SAND, home=(la, lo),
                      sub=MODERN34.get((key, v)), **st))
    if v in (14, 15):
        for k in EAST_TRIBES:
            key = "t_" + k
            st = style(key, TEXT_DIM)
            if key in cur:
                st["bases"] = [S_CUR, 18.4]
            else:
                st["bases"] = [S_OTHER, 14.0]
            U.append(Unit(key, TRIBES[k][0], rings=RINGS_A[k], inside=True,
                          dyn=tribe_cands(RINGS_A[k]), **st))
    return U


# ---------------------------------------------------------------------------
# Section B units (vv16-29)
# ---------------------------------------------------------------------------

SMALL = ("BENJAMIN", "ISSACHAR", "ZEBULUN", "ASHER", "NAPHTALI")
# wide shots: where the five small territories' names go, with a leader
B_LEADERS = {
    "BENJAMIN": dict(cands=[(31.665, 35.30, "c")], on_ok={"JUDAH"}),
    "NAPHTALI": dict(cands=[(33.37, 35.71, "r"), (33.40, 35.85, "c")]),
    "ASHER": dict(cands=[(33.15, 34.99, "l")], sea_ok=True),
    "ZEBULUN": dict(cands=[(32.92, 34.93, "l")], sea_ok=True,
                    cross_ok={"ASHER"}),
    "ISSACHAR": dict(cands=[(32.64, 34.84, "l")], sea_ok=True,
                     cross_ok={"MANASSEH_W"}),
}


def focus_keys(v):
    f = PRINCES.get(v)
    if not f:
        return set()
    return {f[0]} | ({"MANASSEH_E"} if v == 23 else set())


def units_B(v):
    fkeys = focus_keys(v)
    wide = v in WIDE_VERSES_B
    U = []
    for key in WEST_TRIBES + EAST_TRIBES:
        label = TRIBES[key][0]
        east = key in EAST_TRIBES
        rings = TRIBE_RINGS[key]
        kw = dict(rings=rings, inside=True, dyn=tribe_cands(rings),
                  home=POLE[key], ring=False)
        if key in fkeys:
            U.append(Unit("t_" + key, label, [20.0, 18.34, 16.67], HL,
                          bold=True, prio=1, new=True, must=True, gmax=1.2,
                          min_px=20, **kw))
            U[-1].ring = True          # a leader only as the last resort
        else:
            done = v == 29 and not east
            fill = TEXT if not east else TEXT_DIM
            if wide:
                bases, prio = [18.0, 16.0], 3
                must = True
            else:
                bases, prio, must = [16.0, 14.0, 12.0], 4, False
            if wide and key in SMALL:
                lk = B_LEADERS[key]
                kw["cands"] = [c + (POLE[key], True) for c in lk["cands"]]
                kw["on_ok"] = lk.get("on_ok", ())
                kw["cross_ok"] = lk.get("cross_ok", ())
                kw["sea_ok"] = lk.get("sea_ok", False)
                kw["ring"] = True
                prio = 2
            U.append(Unit("t_" + key, label, bases, fill, bold=done,
                          prio=prio, must=must, **kw))
    U.append(Unit("sea", "The Great Sea", [S_AREA + 2, S_AREA], WATER_TXT,
                  italic=True, gmax=1.25,
                  cands=[(32.10, 34.05, "c"), (31.75, 33.90, "c"),
                         (32.50, 34.30, "c"), (32.08, 34.45, "c"),
                         (33.30, 34.70, "c"), (32.40, 34.60, "c"),
                         (32.95, 34.75, "c"), (31.55, 34.00, "c")],
                  prio=6, in_sea=True))
    U.append(Unit("salt", "Salt Sea", [S_AREA, S_OTHER], WATER_TXT,
                  italic=True, gmax=1.25,
                  cands=[(31.12, 35.57, "r"), (31.28, 35.57, "r"),
                         (31.40, 35.58, "r"), (31.20, 35.42, "l")], prio=6))
    return U


# ---------------------------------------------------------------------------
# Geometry per verse: world elements by stroke class, and the lines the label
# QC keeps clear of (kind, key) -- kinds: coast, river, lake, border, tribe
# ---------------------------------------------------------------------------

DASH = (6, 5)

def shape_el(rings, col, op, anim=""):
    """A territory's fill: a polygon, or an even-odd path when it has a
    hole (Judah round Simeon)."""
    if len(rings) == 1:
        head = f'<polygon points="{ptsstr(PS(rings[0]))}"'
    else:
        d = " ".join("M" + " ".join(f"{_fmt(x)},{_fmt(y)}" for x, y in PS(r))
                     + "Z" for r in rings)
        head = f'<path d="{d}" fill-rule="evenodd"'
    head += f' fill="{rgb(col)}" fill-opacity="{op:.3f}"'
    return head + (f">{anim}</{'polygon' if len(rings) == 1 else 'path'}>"
                   if anim else "/>")


def base_world():
    x0, y0 = P(WORLD_LAT[1], WORLD_LON[0])
    els = [f'<rect x="{_fmt(x0)}" y="{_fmt(y0)}" '
           f'width="{_fmt((WORLD_LON[1] - WORLD_LON[0]) * EFF * K)}" '
           f'height="{_fmt((WORLD_LAT[1] - WORLD_LAT[0]) * K)}" '
           f'fill="{rgb(SEA)}"/>',
           poly_el(PS(WORLD_LAND), fill=LAND, closed=True)]
    for sea in WORLD_SEAS:
        els.append(poly_el(PS(sea), fill=SEA, closed=True))
    return els


def lakes_fill():
    return [poly_el(PS(lk), fill=SEA, closed=True) for lk in LAKES]


class Scene:
    """World elements grouped by stroke class, plus QC lines."""

    def __init__(self):
        self.fills = []
        self.fills_after = []
        self.tribe_layer = []
        self.cls = {c: [] for c in CLS_PX}
        self.qc = []              # (world polyline, kind, key)
        self.ends = [0.0]


def water_lines(sc):
    for lake in LAKES:
        sc.cls["w1"].append(poly_el(PS(lake), stroke=SAND_DIM, closed=True))
        sc.qc.append((PS(lake + lake[:1]), "lake", None))
    sc.cls["w2"].append(poly_el(PS(WORLD_COAST), stroke=SAND_DIM))
    sc.qc.append((PS(WORLD_COAST), "coast", None))


def river_lines(sc, cls):
    for rv in RIVERS:
        sc.cls[cls].append(poly_el(PS(rv), stroke=RIVER))
        sc.qc.append((PS(rv), "river", None))


def scene_A(v, t_tr0, D_tr):
    sc = Scene()
    sc.fills += base_world()
    if v >= 2:
        canaan = PS(CANAAN_POLY)
        if v == 2:
            sc.fills.append(
                f'<polygon points="{ptsstr(canaan)}" fill="{rgb(HL)}" '
                f'fill-opacity="0">{op_anim(0, 16 / 255, t_tr0, D_tr)}'
                f'</polygon>')
            sc.ends.append(t_tr0 + D_tr)
        else:
            sc.fills.append(poly_el(canaan, fill=HL + (16,), closed=True))
    if v == 14:
        for key in EAST_TRIBES:
            sc.fills.append(shape_el(RINGS_A[key], TRIBE_COL[key], 0.0,
                                     op_anim(0, 80 / 255, t_tr0, D_tr)))
        sc.ends.append(t_tr0 + D_tr)
    elif v == 15:
        for key in EAST_TRIBES:
            sc.fills.append(shape_el(RINGS_A[key], TRIBE_COL[key], 80 / 255))
    if v in (14, 15):
        for key in EAST_TRIBES:
            for r in RINGS_A[key]:
                sc.cls["w1b"].append(poly_el(PS(r + r[:1]), stroke=SAND_DIM))
                sc.qc.append((PS(r + r[:1]), "area", key))
    sc.fills += lakes_fill()
    water_lines(sc)
    trace = None
    for sv, seg in BORDER_SEGS:
        pts = PS(seg)
        sc.qc.append((pts, "border", None))
        if sv == v - 1:
            sc.cls["w4f"].append(poly_el(pts, stroke=HL + (242,))[:-2]
                                 + ">" + fade(0.0, LET_GO, out=True)
                                 + "</polyline>")
        if v > sv or v >= 13:
            sc.cls["w3"].append(poly_el(pts, stroke=SAND))
        elif v == sv:
            sc.cls["dash"].append(poly_el(pts, stroke=SAND_DIM))
            el, _L = traced_el(pts, HL + (242,), t_tr0, D_tr)
            sc.cls["w4"].append(el)
            sc.ends.append(t_tr0 + D_tr)
            trace = (seg, t_tr0, D_tr)
        else:
            sc.cls["dash"].append(poly_el(pts, stroke=SAND_DIM))
    # the Jordan is drawn over the border that now runs on it
    river_lines(sc, "w2r")
    return sc, trace


FOCUS_FILL = 0.30            # the highlighted territory's tint (capped)


def base_alpha(key):
    return (26 if key in EAST_TRIBES else 42) / 255


def scene_B(v, t_tr0, D_tr):
    sc = Scene()
    sc.fills += base_world()
    fkeys = focus_keys(v)
    pkeys = focus_keys(v - 1)
    for key in WEST_TRIBES + EAST_TRIBES:
        rings = TRIBE_RINGS[key]
        east = key in EAST_TRIBES
        done = v == 29 and not east
        ba = base_alpha(key)
        if key in fkeys:
            sc.tribe_layer.append(shape_el(rings, TRIBE_COL[key], ba,
                                           op_anim(ba, FOCUS_FILL, t_tr0,
                                                   D_tr)))
            for r in rings:
                el, _ = traced_el(PS(r), HL + (242,), t_tr0, D_tr,
                                  closed=True)
                sc.cls["w3b"].append(el)
            sc.ends.append(t_tr0 + D_tr)
        elif key in pkeys:
            sc.tribe_layer.append(shape_el(rings, TRIBE_COL[key], FOCUS_FILL,
                                           op_anim(FOCUS_FILL, ba, 0.0,
                                                   LET_GO)))
            for r in rings:
                sc.cls["w3f"].append(
                    poly_el(PS(r + r[:1]), stroke=HL + (242,))[:-2]
                    + ">" + fade(0.0, LET_GO, out=True) + "</polyline>")
        else:
            sc.tribe_layer.append(shape_el(rings, TRIBE_COL[key], ba))
        for r in rings:
            sc.cls["w1b"].append(poly_el(PS(r + r[:1]), stroke=SAND_DIM))
            if done:
                sc.cls["w1c"].append(poly_el(PS(r + r[:1]), stroke=SAND))
            sc.qc.append((PS(r + r[:1]), "area", key))
    sc.fills_after = lakes_fill()
    water_lines(sc)
    river_lines(sc, "w2r")      # as in vv1-15, so v16 hands over cleanly
    return sc


# screen widths of each stroke class
CLS_PX = {"w1": 1.0, "w1b": 1.0, "w2": 2.0, "dash": 1.0, "w3": 3.0,
          "w4": 4.0, "w3b": 3.0, "w1c": 1.0, "w3f": 3.0, "w4f": 4.0,
          "w2r": 1.6}
LET_GO = 0.8        # how long the last verse's highlight takes to settle


def emit_class(fl, name, els, extra=""):
    return emit_px(fl, CLS_PX[name], els, extra,
                   DASH if name == "dash" else None)


# ---------------------------------------------------------------------------
# Label layout at the rest camera (svg_map_camera.layout); this map's own
# rule: a name kept out of Canaan stays out of it
# ---------------------------------------------------------------------------

def make_ctx(cam, lines, dots, hud, focus, sec, tribes_a=False):
    rs = TRIBE_RINGS if sec == "B" else (
        {k: RINGS_A[k] for k in EAST_TRIBES} if tribes_a else {})
    areas = {k: [[to_screen(cam, P(a, b)) for a, b in r] for r in rings]
             for k, rings in rs.items()}
    land = [to_screen(cam, P(a, b)) for a, b in WORLD_LAND]
    canaan = [to_screen(cam, P(a, b)) for a, b in CANAAN_POLY]

    def extra(u, cand, rs_, lead, centre):
        if u.out_poly is not None and pip(centre, canaan):
            return ["inside-canaan"]
        return []
    return Ctx(PROJ, cam, lines, dots, hud, focus, areas, land, extra)


# ---------------------------------------------------------------------------
# Verse assembly
# ---------------------------------------------------------------------------

def build_all():
    prev = None          # state of the previous verse
    report = []
    for v in VERSES:
        sec = section(v)
        cam1 = SHOTS[v]
        cam0 = OPEN_A if v == 1 else prev["cam1"]
        narr = NARR[v]
        fl = plan(v, cam0)
        assert _same(fl.cam1, cam1), v
        t_land = fl.dur
        # when the trace / grow starts and how long it takes
        if v == 2:
            t_tr0, D_tr = 0.6, 3.6
        elif v == 12:
            t_tr0, D_tr = 0.5, 3.8
        elif v == 16:
            t_tr0, D_tr = 0.0, 1.4
        else:
            t_tr0 = t_land + 0.1
            D_tr = round(max(1.2, min(3.2, narr - AUDIO_SLACK - t_land
                                      - 0.6)), 2)
        if sec == "A":
            sc, trace = scene_A(v, t_tr0, D_tr)
        else:
            trace = None
            sc = scene_B(v, t_tr0, D_tr)
        units = units_A(v) if sec == "A" else units_B(v)

        # screen geometry at rest for the QC / layout
        lines, lines_w = [], []
        for pts, kind, key in sc.qc:
            wpx = 3.0 if kind in ("border",) else 2.0
            lines.append(([to_screen(cam1, p) for p in pts], wpx, kind, key))
            lines_w.append((pts, wpx))
        hud = hud_rects(v, cam1)
        assert inset_opacity(cam1, sec) in (0.0, 1.0), \
            f"v{v}: the inset would rest half-faded"
        dots = rest_dots(PROJ, units, cam1, hud)
        fk = focus_keys(v) if sec == "B" else set()
        ctx = make_ctx(cam1, lines, dots, hud, fk, sec, tribes_a=v in (14, 15))
        same_sec = prev is not None and prev["sec"] == sec
        placed, dropped, problems = layout(units, ctx,
                                           prev if same_sec else None)
        prev_units = prev["units"] if same_sec else {}
        cur_ident = identities(placed, cam1)

        # appear times for new content: when the trace reaches it, or landing
        for u in units:
            u.t_in = None
            if unchanged(u, cur_ident, prev_units):
                continue                 # unchanged: it simply stays
            if u.new:
                t = t_land + 0.05
                if trace:
                    seg, tb, td = trace
                    f = frac_along(PS(seg), P(*u.cands[0][:2])) \
                        if u.cands else 1.0
                    t = tb + td * ease_inv(min(1.0, f)) - 0.15
                    t = max(t, t_land * 0.6 if v != 12 else 0.4)
                u.t_in = round(max(0.0, t), 2)
            if v == 16:
                u.t_in = 1.0

        lab = emit_labels(PROJ, units, placed, cur_ident, prev, same_sec,
                          cam0, cam1, fl, t_land, hud,
                          lambda cam, v=v: hud_rects(v, cam), lines_w,
                          problems)

        # -------- assemble the SVG ------------------------------------
        svg = []
        svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" '
                   f'viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
                   f'font-family="{FONT_FAMILY}">')
        svg.append(f'<rect width="{W}" height="{H}" fill="{rgb(BG)}"/>')
        svg.append(fl.open_camera())
        svg += sc.fills
        a_border = ""
        if sec == "B":
            if v == 16:
                # the border map hands over to the territories (camera holds)
                a_fills, a_border = section_a_layer(fl)
                svg.append(f'<g>{a_fills}{fade(0.0, 1.2, out=True)}</g>')
                svg.append(f'<g opacity="0">{fade(0.2, 1.2)}'
                           + "".join(sc.tribe_layer)
                           + emit_class(fl, "w1b", sc.cls["w1b"]) + "</g>")
            else:
                svg += sc.tribe_layer
                svg.append(emit_class(fl, "w1b", sc.cls["w1b"]))
            svg += sc.fills_after
        else:
            if sc.cls["w1b"]:
                if v == 14:
                    svg.append(f'<g opacity="0">{fade(t_tr0, D_tr)}'
                               + emit_class(fl, "w1b", sc.cls["w1b"])
                               + "</g>")
                else:
                    svg.append(emit_class(fl, "w1b", sc.cls["w1b"]))
        if sc.cls["w1c"]:
            svg.append(f'<g opacity="0">{fade(t_land, 0.6)}'
                       + emit_class(fl, "w1c", sc.cls["w1c"]) + "</g>")
        for name in ("w1", "w2", "dash", "w3", "w4f", "w4", "w2r", "w3f",
                     "w3b"):
            svg.append(emit_class(fl, name, sc.cls[name]))
            if name == "w2" and v == 16:
                svg.append(f'<g>{a_border}{fade(0.0, 1.2, out=True)}</g>')
        svg += emit_label_layers(fl, lab)
        svg.append("</g></g>")
        title = TITLE_A if sec == "A" else TITLE_B
        svg.append(hud_svg(v, sec, fl, title))
        svg.append(inset_svg(v, sec, fl))
        svg.append("</svg>")
        text = "".join(svg)
        path = out_path("Numbers", 34, f"Numbers_34_{v}.svg")
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)

        # -------- QC ---------------------------------------------------
        mid = midflight_qc(fl, placed, lab["exiting"])
        ends = sc.ends + [getattr(u, "t_show", 0) + 0.5 for u in placed
                          if getattr(u, "t_show", 0) > 0]
        end = max(ends + [fl.dur])
        rest_px = []
        for u in placed:
            if not any(rr_hit(r, (0, 0, W, H)) for r in u.rest_rects):
                continue
            g = grow(cam1[0], u.gmax)
            for p in u.parts(u.place):
                rest_px.append((round(p[1] * g, 1), u.key))
        report.append(dict(
            v=v, pxdeg=round(cam1[0] * K, 1), cam=round(fl.dur, 2),
            tr=D_tr, end=round(end, 2), narr=narr,
            minscale=round(fl.min_scale() * K, 1),
            maxscale=round(fl.max_scale() * K, 1),
            kb=round(len(text.encode()) / 1024, 1),
            dropped=[u.key for u in units
                     if u.key in dropped and anchor_on_screen(u, cam1)],
            problems=problems, mid=mid, dips=lab["dips"],
            minpx=min(rest_px) if rest_px else None,
            ext=extent_check(fl, PROJ, WORLD_LAT, WORLD_LON)))

        prev = prev_state(cam1, placed, cur_ident, lab["cur_dots"],
                          sec=sec)
    return report


def section_a_layer(fl):
    """vv1-15's closed border, tint and east-bank fills (as v15 rests),
    for the hand-over at v16."""
    els = [poly_el(PS(CANAAN_POLY), fill=HL + (16,), closed=True)]
    for key in EAST_TRIBES:
        els.append(shape_el(RINGS_A[key], TRIBE_COL[key], 80 / 255))
    border = [poly_el(PS(seg), stroke=SAND) for _v, seg in BORDER_SEGS]
    outl = [poly_el(PS(r + r[:1]), stroke=SAND_DIM)
            for key in EAST_TRIBES for r in RINGS_A[key]]
    return "".join(els), (emit_class(fl, "w1b", outl)
                          + emit_class(fl, "w3", border))


def hud_svg(v, sec, fl, title):
    out = [title_svg(title, TEXT)]

    def prince_texts(pv):
        t1, t2 = prince_lines(pv)
        return (f'<text x="{W - 18}" y="14" font-size="26" '
                f'font-weight="bold" fill="{rgb(HL)}" text-anchor="end" '
                f'dominant-baseline="text-before-edge">{escape(t1)}</text>'
                f'<text x="{W - 18}" y="50" font-size="20" '
                f'fill="{rgb(TEXT)}" text-anchor="end" '
                f'dominant-baseline="text-before-edge">{escape(t2)}</text>')
    if v in PRINCES:
        pr = prince_rect(v)
        plate = (f'<rect x="{_fmt(pr[0])}" y="{_fmt(pr[1])}" '
                 f'width="{_fmt(pr[2] - pr[0])}" '
                 f'height="{_fmt(pr[3] - pr[1])}" rx="8" fill="{rgb(BG)}" '
                 f'fill-opacity="0.82"/>')
        if v - 1 in PRINCES:
            out.append(plate)
            out.append(f'<g>{fade(0.0, 0.35, out=True)}'
                       + prince_texts(v - 1) + "</g>")
            out.append(f'<g opacity="0">{fade(0.25, 0.5)}'
                       + prince_texts(v) + "</g>")
        else:
            out.append(f'<g opacity="0">{fade(0.0, 0.6)}' + plate
                       + prince_texts(v) + "</g>")
    elif v - 1 in PRINCES:
        pr = prince_rect(v - 1)
        out.append(f'<g>{fade(0.0, 0.5, out=True)}'
                   f'<rect x="{_fmt(pr[0])}" y="{_fmt(pr[1])}" '
                   f'width="{_fmt(pr[2] - pr[0])}" '
                   f'height="{_fmt(pr[3] - pr[1])}" rx="8" fill="{rgb(BG)}" '
                   f'fill-opacity="0.82"/>' + prince_texts(v - 1) + "</g>")
    out.append(compass_scale_svg(fl, PROJ, SCALE_KM))
    return "".join(out)


# ---------------------------------------------------------------------------
# Overview inset: the whole territory, fixed, with the camera's view drawn as
# a rectangle moving in lockstep with the camera. Shown only in close-ups: it
# fades out as the camera pulls back to a whole-land shot.
# ---------------------------------------------------------------------------

def inset_svg(v, sec, fl):
    x0, y0, x1, y1 = INSET_RECT
    ops = [f"{inset_opacity(c, sec):.2f}" for c in fl.cams]
    out = [f'<g opacity="{ops[0]}">{fl._anim("opacity", ops)}',
           f'<defs><clipPath id="insetclip"><rect x="{x0}" y="{y0}" '
           f'width="{x1 - x0}" height="{y1 - y0}" rx="6"/></clipPath></defs>',
           f'<g clip-path="url(#insetclip)">',
           f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" '
           f'fill="{rgb(SEA)}"/>']
    if sec != section(v - 1) and v - 1 in VERSES:
        # the hand-over at v16 swaps the inset's map with the main one's
        out.append(f'<g>{fade(0.0, 1.2, out=True)}'
                   + "".join(inset_map(section(v - 1), fl)) + "</g>")
        out.append(f'<g opacity="0">{fade(0.2, 1.2)}'
                   + "".join(inset_map(sec, fl)) + "</g>")
    else:
        out += inset_map(sec, fl)
    out.append("</g>")
    out.append(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" '
               f'height="{y1 - y0}" rx="6" fill="none" '
               f'stroke="{rgb(SAND_DIM)}" stroke-width="1.5"/>')
    out.append("</g>")
    return "".join(out)


def inset_map(sec, fl):
    """The inset's map for a section, at that section's scale, with the
    camera's view boxed."""
    x0, y0, x1, y1 = INSET_RECT
    la0, la1, lo0, lo1 = INSET_BOX_A if sec == "A" else INSET_BOX_B
    iw, ih = x1 - x0 - 8, y1 - y0 - 8
    k = min(iw / ((lo1 - lo0) * EFF), ih / (la1 - la0))
    ox = x0 + 4 + (iw - (lo1 - lo0) * EFF * k) / 2
    oy = y0 + 4 + (ih - (la1 - la0) * k) / 2

    def ip(lat, lon):
        return (ox + (lon - lo0) * EFF * k, oy + (la1 - lat) * k)

    def ips(seq):
        return [ip(a, b) for a, b in seq]

    out = [poly_el(ips(WORLD_LAND), fill=LAND, closed=True)]
    for lk in LAKES:
        out.append(poly_el(ips(lk), fill=SEA, closed=True))
    if sec == "A":
        out.append(poly_el(ips(CANAAN_POLY), fill=HL + (30,), stroke=SAND,
                           closed=True, extra=' stroke-width="1"'))
    else:
        for key in WEST_TRIBES + EAST_TRIBES:
            out.append(poly_el(ips(TRIBE_RINGS[key][0]),
                               fill=TRIBE_COL[key] + (90,), stroke=SAND_DIM,
                               closed=True, extra=' stroke-width="0.6"'))

    out.append(inset_view_rect(fl, PROJ, ip, HL))
    return out


# ---------------------------------------------------------------------------
# QC helpers
# ---------------------------------------------------------------------------

def anchor_on_screen(u, cam):
    """Whether a name's place (a landmark's dot, a territory's deepest
    point, an area name's first spot) is in the rest frame: a dropped name
    the camera simply isn't looking at is no loss worth reporting."""
    if u.rings:
        at = POLE.get(u.key[2:])
    else:
        at = u.cands[0][:2] if u.cands else None
    if at is None:
        return False
    x, y = to_screen(cam, P(*at))
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
        for n in notes:
            print(f"  v{r['v']}: {n}")
    missing = [v for v in VERSES if _narration(v) is None]
    if missing:
        print(f"  no MP3 for v{missing}: paced at {NARR_FALLBACK}s")
    kb = [r["kb"] for r in report]
    print(f"Numbers 34: {len(report)} SVG files, {sum(kb):.0f} KB "
          f"(largest {max(kb)} KB)")


if __name__ == "__main__":
    main()
