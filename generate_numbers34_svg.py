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

import math
import os
from xml.sax.saxutils import escape

from PIL import ImageFont

from config import WEB_AUDIO_DIR
from passages import verse_numbers
from svg_surface import _fmt, FONT_FAMILY
from svg_chronicles_world import (AUDIO_SLACK, CAM_FPS, EASE, _mp3_seconds,
                                  _smooth, _vw)
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

K = 100.0
LAT_TOP, LON_LEFT = 36.0, 30.0
EFF = math.cos(math.radians(32.3))


def P(lat, lon):
    return ((lon - LON_LEFT) * EFF * K, (LAT_TOP - lat) * K)


def PS(seq):
    return [P(a, b) for a, b in seq]


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
# Camera (svg_chronicles_world._vw, van Wijk & Nuij's pan-zoom arc, as in
# 1 Chronicles) -- cam = (s, wx, wy): world point (wx, wy) sits at the
# screen centre at scale s.
# ---------------------------------------------------------------------------

def ease_y(u):                       # the y of cubic-bezier(.42,0,.58,1)
    return 3 * u * u - 2 * u ** 3


def ease_x(u):
    return 3 * (1 - u) ** 2 * u * 0.42 + 3 * (1 - u) * u * u * 0.58 + u ** 3


def ease(t):
    """Progress at time fraction t under keySplines EASE."""
    lo, hi = 0.0, 1.0
    for _ in range(40):
        m = (lo + hi) / 2
        if ease_x(m) < t:
            lo = m
        else:
            hi = m
    return ease_y((lo + hi) / 2)


def ease_inv(f):
    """Time fraction at which an EASE-d animation reaches progress f."""
    lo, hi = 0.0, 1.0
    for _ in range(40):
        m = (lo + hi) / 2
        if ease_y(m) < f:
            lo = m
        else:
            hi = m
    return ease_x((lo + hi) / 2)


def cam_T(cam):
    s, wx, wy = cam
    return W / 2 - s * wx, H / 2 - s * wy


def _same(a, b):
    return abs(a[0] - b[0]) < 1e-9 and math.hypot(a[1] - b[1],
                                                  a[2] - b[2]) < 1e-6


class Leg:
    def __init__(self, camA, camB, dur, kind):
        self.camA, self.camB, self.dur, self.kind = camA, camB, dur, kind
        if kind == "zoom":
            self.f, _apex = _vw(camA, camB)

    def at(self, u):
        if self.kind == "hold":
            return self.camA
        if self.kind == "pan":
            e = ease(u)
            a, b = self.camA, self.camB
            return (a[0], a[1] + (b[1] - a[1]) * e, a[2] + (b[2] - a[2]) * e)
        return self.f(_smooth(u))


class Flight:
    """One verse's camera: static, a single eased pan (two keyframes and a
    spline, exact), or legs (holds, van Wijk zooms, pans) baked at CAM_FPS
    into one uniformly spaced keyframe list."""

    def __init__(self, cam0, legs):
        self.cam0 = cam0
        self.legs = []
        cam = cam0
        for kind, target, dur in legs:
            if kind == "hold":
                if dur > 0:
                    self.legs.append(Leg(cam, cam, dur, "hold"))
                continue
            if _same(cam, target) or dur <= 0:
                continue
            k = "pan" if abs(cam[0] - target[0]) < 1e-9 else "zoom"
            self.legs.append(Leg(cam, target, dur, k))
            cam = target
        self.cam1 = cam
        moving = [lg for lg in self.legs if lg.kind != "hold"]
        self.static = not moving
        self.pure_pan = (not self.static and len(self.legs) == 1
                         and moving[0].kind == "pan")
        if self.static:
            self.dur, self.cams = 0.0, [cam]
        elif self.pure_pan:
            self.dur, self.cams = self.legs[0].dur, [cam0, cam]
        else:
            self.dur = sum(lg.dur for lg in self.legs)
            n = max(6, int(round(self.dur * CAM_FPS)))
            cams = [self.exact(self.dur * i / n) for i in range(n + 1)]
            cams[0], cams[-1] = cam0, cam
            self.cams = [(float("%.6f" % c[0]), c[1], c[2]) for c in cams]

    def exact(self, t):
        t0 = 0.0
        for lg in self.legs:
            if t <= t0 + lg.dur:
                return lg.at((t - t0) / lg.dur)
            t0 += lg.dur
        return self.cam1

    def at(self, t):
        """Camera at time t (seconds), as the browser plays it."""
        if self.static or t >= self.dur:
            return self.cam1
        if t <= 0:
            return self.cam0
        if self.pure_pan:
            return self.legs[0].at(t / self.dur)
        n = len(self.cams) - 1
        f = t / self.dur * n
        i = min(n - 1, int(f))
        a, b, r = self.cams[i], self.cams[i + 1], f - i
        # SMIL interpolates translate and scale separately and linearly
        s = a[0] + (b[0] - a[0]) * r
        ta, tb = cam_T(a), cam_T(b)
        tx = ta[0] + (tb[0] - ta[0]) * r
        ty = ta[1] + (tb[1] - ta[1]) * r
        return (s, (W / 2 - tx) / s, (H / 2 - ty) / s)

    def min_scale(self):
        return min(c[0] for c in self.cams)

    def max_scale(self):
        return max(c[0] for c in self.cams)

    # -- emission -----------------------------------------------------------

    def _anim(self, attr, vals, typ=None):
        if self.static or len(set(vals)) == 1:
            return ""
        kind = "animateTransform" if typ else "animate"
        t = f' type="{typ}"' if typ else ""
        extra = (f' calcMode="spline" keyTimes="0;1" keySplines="{EASE}"'
                 if self.pure_pan else "")
        return (f'<{kind} attributeName="{attr}"{t} values="{";".join(vals)}"'
                f' dur="{self.dur:.2f}s" begin="0s" fill="freeze"{extra}/>')

    def open_camera(self):
        cams = self.cams
        tv = [f"{_fmt(cam_T(c)[0])} {_fmt(cam_T(c)[1])}" for c in cams]
        sv = [("%.6f" % c[0]).rstrip("0").rstrip(".") for c in cams]
        return (f'<g transform="translate({tv[0]})">'
                + self._anim("transform", tv, "translate")
                + f'<g transform="scale({sv[0]})">'
                + self._anim("transform", sv, "scale"))

    def inverse(self, attr, px, fmt="%.3f", text=False):
        """An inherited attribute held at `px` screen pixels: px / s(t).
        Text (text = its grow cap) also grows gently as the camera closes
        in."""
        vals = [(fmt % (px * (grow(c[0], text) if text else 1.0) / c[0]))
                for c in self.cams]
        return f'{attr}="{vals[0]}"', self._anim(attr, vals)

    def inverse_dash(self, a_px, b_px):
        vals = [f"{a_px / c[0]:.3f},{b_px / c[0]:.3f}" for c in self.cams]
        return f'stroke-dasharray="{vals[0]}"', self._anim("stroke-dasharray",
                                                            vals)


GROW_FROM, GROW_POW, GROW_MAX = 1.9, 0.5, 1.4


def grow(s, gmax=None):
    """Text is a constant screen size up to the wide shots' scale and grows
    gently (sqrt) past it: a close-up's names are larger, for the phone."""
    return min(gmax or GROW_MAX, max(1.0, (s / GROW_FROM) ** GROW_POW))


def to_screen(cam, xy):
    s, wx, wy = cam
    return (W / 2 + s * (xy[0] - wx), H / 2 + s * (xy[1] - wy))


def unproject(cam, sx, sy):
    s, wx, wy = cam
    x = (sx - W / 2) / s + wx
    y = (sy - H / 2) / s + wy
    return LAT_TOP - y / K, x / (EFF * K) + LON_LEFT


def shot(lat, lon, pxdeg, sx=W / 2, sy=H / 2):
    """Rest camera that puts (lat, lon) at screen (sx, sy) at pxdeg px/deg."""
    s = pxdeg / K
    x, y = P(lat, lon)
    return (s, x - (sx - W / 2) / s, y - (sy - H / 2) / s)


def fit(lat0, lat1, lon0, lon1, box=(0, 12, W, H - 12), cap=None):
    x0, y0, x1, y1 = box
    pxdeg = min((x1 - x0) / ((lon1 - lon0) * EFF), (y1 - y0) / (lat1 - lat0))
    if cap:
        pxdeg = min(cap, pxdeg)
    return shot((lat0 + lat1) / 2, (lon0 + lon1) / 2, round(pxdeg, 1),
                (x0 + x1) / 2, (y0 + y1) / 2)


def visible_world(cam, pad=0):
    s, wx, wy = cam
    hw, hh = W / 2 / s + pad, H / 2 / s + pad
    return wx - hw, wy - hh, wx + hw, wy + hh


# ---------------------------------------------------------------------------
# Text measurement (Georgia, the face the SVG asks for) for the label QC
# ---------------------------------------------------------------------------

_FONTS = {}
PIL_V = {"a": "a", "t": "a", "m": "m", "s": "s", "b": "d", "d": "d"}
SVG_H = {"l": "start", "m": "middle", "r": "end"}
SVG_V = {"a": "text-before-edge", "t": "text-before-edge", "m": "central",
         "s": "alphabetic", "b": "text-after-edge", "d": "text-after-edge"}


def _font(size, bold, italic):
    k = (int(round(size)), bold, italic)
    if k not in _FONTS:
        name = "georgia" + ("z" if bold and italic else "b" if bold
                            else "i" if italic else "")
        _FONTS[k] = ImageFont.truetype(name + ".ttf", k[0])
    return _FONTS[k]


def ink(text, size, bold, italic, anchor):
    """Ink box of `text` relative to its anchor point (screen px)."""
    return _font(size, bold, italic).getbbox(
        text, anchor=anchor[0] + PIL_V[anchor[1]])


# ---------------------------------------------------------------------------
# Small geometry helpers
# ---------------------------------------------------------------------------

def union(rs):
    return (min(r[0] for r in rs), min(r[1] for r in rs),
            max(r[2] for r in rs), max(r[3] for r in rs))


def inflate(r, d):
    return (r[0] - d, r[1] - d, r[2] + d, r[3] + d)


def rr_hit(a, b):
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


def seg_hits_rect(p, q, r):
    """Does segment pq intersect rect r? (Liang-Barsky)"""
    x0, y0, x1, y1 = r
    dx, dy = q[0] - p[0], q[1] - p[1]
    t0, t1 = 0.0, 1.0
    for pp, qq in ((-dx, p[0] - x0), (dx, x1 - p[0]),
                   (-dy, p[1] - y0), (dy, y1 - p[1])):
        if abs(pp) < 1e-12:
            if qq < 0:
                return False
        else:
            t = qq / pp
            if pp < 0:
                t0 = max(t0, t)
            else:
                t1 = min(t1, t)
            if t0 > t1:
                return False
    return True


def poly_hits_rect(pts, r):
    for p, q in zip(pts, pts[1:]):
        if seg_hits_rect(p, q, r):
            return True
    return False


def seg_x(p, q, a, b):
    """Intersection point of segments pq and ab, or None."""
    d = (q[0] - p[0]) * (b[1] - a[1]) - (q[1] - p[1]) * (b[0] - a[0])
    if abs(d) < 1e-12:
        return None
    t = ((a[0] - p[0]) * (b[1] - a[1]) - (a[1] - p[1]) * (b[0] - a[0])) / d
    u = ((a[0] - p[0]) * (q[1] - p[1]) - (a[1] - p[1]) * (q[0] - p[0])) / d
    if 0 <= t <= 1 and 0 <= u <= 1:
        return (p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1]))
    return None


def seg_dist(pt, a, b):
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    L = dx * dx + dy * dy
    t = 0 if L == 0 else max(0, min(1, ((pt[0] - ax) * dx +
                                        (pt[1] - ay) * dy) / L))
    return math.hypot(pt[0] - ax - t * dx, pt[1] - ay - t * dy)


def ring_dist(pt, ring):
    return min(seg_dist(pt, a, b) for a, b in zip(ring, ring[1:] + ring[:1]))


def rect_dist(c, r):
    cx = min(max(c[0], r[0]), r[2])
    cy = min(max(c[1], r[1]), r[3])
    return math.hypot(c[0] - cx, c[1] - cy)


def circle_hits_rect(c, rad, r):
    cx = min(max(c[0], r[0]), r[2])
    cy = min(max(c[1], r[1]), r[3])
    return math.hypot(c[0] - cx, c[1] - cy) < rad


def pip(pt, poly):
    x, y = pt
    inside_ = False
    for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]):
        if (y0 > y) != (y1 > y):
            if x < x0 + (y - y0) * (x1 - x0) / (y1 - y0):
                inside_ = not inside_
    return inside_


def in_rings(pt, rings):
    """Inside the first ring and outside the others (holes)."""
    return pip(pt, rings[0]) and not any(pip(pt, h) for h in rings[1:])


# ---------------------------------------------------------------------------
# HUD (screen space, never scaled)
# ---------------------------------------------------------------------------

TITLE_PX = 20
SAFE = (12, 10, W - 12, H - 10)
SCALE_KM = 50
INSET_RECT = (14, H - 14 - 168, 14 + 118, H - 14)   # x0, y0, x1, y1


def title_rect(title):
    l, t, r, b = ink(title, TITLE_PX, True, False, "la")
    return (6, 4, 18 + r + 10, 14 + b + 7)


def compass_rect(s):
    bar = SCALE_KM / 111.0 * K * s
    return (W - 26 - max(bar, 64) - 8, H - 84, W, H)


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
    hud = [("title", title_rect(title)), ("compass", compass_rect(cam[0]))]
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


def cam_duration(cam0, cam1):
    if _same(cam0, cam1):
        return 0.0
    s0, s1 = cam0[0], cam1[0]
    travel = math.hypot(cam1[1] - cam0[1], cam1[2] - cam0[2]) * max(s0, s1)
    if abs(s0 - s1) < 1e-9:
        return min(2.4, max(1.1, 0.8 + travel / 330.0))
    zoom = max(s0 / s1, s1 / s0)
    return min(3.0, max(1.3, 1.25 + 0.7 * math.log2(zoom) + travel / 1100.0))


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
# Labels
# ---------------------------------------------------------------------------

S_OTHER, S_AREA, S_CUR, S_SUB = 16, 18, 20, 16
OFF = {"r": (9, 0, "lm"), "l": (-9, 0, "rm"), "a": (0, -8, "mb"),
       "b": (0, 8, "mt"), "ar": (7, -5, "lb"), "al": (-7, -5, "rb"),
       "br": (7, 5, "lt"), "bl": (-7, 5, "rt"), "c": (0, 0, "mm")}
for _k in list(OFF):
    if _k != "c":
        _dx, _dy, _a = OFF[_k]
        OFF[_k + "+"] = (_dx * 1.7, _dy * 1.9, _a)
DOT_CODES = ["r", "l", "a", "b", "ar", "al", "br", "bl"]


class Unit:
    """A label: a main name (+ optional dim italic sub-label below it), an
    optional dot, and candidate placements tried in order.

    cands: (lat, lon, code) or (lat, lon, code, home, True) where home =
    (lat, lon) the leader line points at (a rest-bound placement).
    bases: font sizes to try (largest first); rest px = base * grow(s).
    """

    def __init__(self, key, text, bases, fill, bold=False, italic=False,
                 cands=(), sub=None, dot=None, prio=5, new=False,
                 must=False, home=None, rings=None, gmax=GROW_MAX,
                 min_px=16, inside=False, dyn=None, on_ok=(), cross_ok=(),
                 sea_ok=False, in_sea=False, out_poly=None, ring=True,
                 dot_optional=True):
        self.key, self.text, self.fill = key, text, fill
        self.bases = list(bases)
        self.size = self.bases[0]
        self.bold, self.italic, self.cands = bold, italic, list(cands)
        self.sub, self.dot, self.prio, self.new = sub, dot, prio, new
        self.must, self.home, self.rings = must, home, rings
        self.gmax, self.min_px, self.inside = gmax, min_px, inside
        self.dyn, self.on_ok, self.cross_ok = dyn, set(on_ok), set(cross_ok)
        self.sea_ok, self.in_sea, self.out_poly = sea_ok, in_sea, out_poly
        self.ring, self.dot_optional = ring, dot_optional
        self.sub_size = S_SUB
        self.place = None

    def auto_cands(self, cam):
        """Fallbacks after the hand-given candidates: every side of a dot at
        two distances; a jitter round an area label's anchors; a ring of
        leader positions round `home`, nearest first."""
        out = []
        if self.dot:
            la, lo = self.cands[0][:2]
            for m in ("", "+"):
                for code in DOT_CODES:
                    c = (la, lo, code + m)
                    if c not in self.cands:
                        out.append(c)
        elif not self.inside:
            for cand in self.cands[:4]:
                if len(cand) > 4:
                    continue
                ax, ay = to_screen(cam, P(cand[0], cand[1]))
                for ddx, ddy in ((0, -14), (0, 14), (-24, 0), (24, 0),
                                 (-24, -14), (24, -14), (-24, 14), (24, 14),
                                 (0, -28), (0, 28), (-48, 0), (48, 0)):
                    la, lo = unproject(cam, ax + ddx, ay + ddy)
                    out.append((la, lo, cand[2]))
        if self.home and self.ring:
            hx, hy = to_screen(cam, P(*self.home))
            if not (40 < hx < W - 40 and 40 < hy < H - 40):
                return out
            ring = []
            for dist in ((30, 42, 56) if self.dot else
                         (36, 48, 60, 74, 90, 110)):
                for ang in range(0, 360, 15):
                    a = math.radians(ang)
                    px, py = hx + dist * math.cos(a), hy + dist * math.sin(a)
                    ca = math.cos(a)
                    code = "r" if ca > 0.3 else "l" if ca < -0.3 else "c"
                    if code == "c":
                        py += 10 * (1 if math.sin(a) > 0 else -1)
                    la, lo = unproject(cam, px, py)
                    ring.append((dist, (la, lo, code, self.home, True)))
            out += [c for _d, c in ring]
        return out

    def style(self):
        return (self.text, round(self.size, 2), self.fill, self.bold,
                self.italic, self.sub, self.dot, round(self.sub_size, 2))

    def parts(self, cand):
        """[(text, size, fill, bold, italic, dx, dy, anchor)] for cand. A
        sub-label always sits UNDER its name: for a placement above the
        point the name moves up to make room."""
        code = cand[2]
        dx, dy, anc = OFF[code]
        k = 1.15 if self.size > 18 else 1.0
        dx, dy = dx * k, dy * k
        if not self.sub:
            return [(self.text, self.size, self.fill, self.bold, self.italic,
                     dx, dy, anc)]
        v = anc[1]
        if v in ("b", "d"):
            sa = anc[0] + "d"
            sb = ink(self.sub, self.sub_size, False, True, sa)
            ma = anc[0] + "d"
            mb = ink(self.text, self.size, self.bold, self.italic, ma)
            mdy = dy + sb[1] - 3 - mb[3]
            return [(self.text, self.size, self.fill, self.bold, self.italic,
                     dx, mdy, ma),
                    (self.sub, self.sub_size, TEXT_DIM, False, True, dx, dy,
                     sa)]
        mb = ink(self.text, self.size, self.bold, self.italic, anc)
        sa = anc[0] + "a"
        sb = ink(self.sub, self.sub_size, False, True, sa)
        sdy = dy + mb[3] + 3 - sb[1]
        return [(self.text, self.size, self.fill, self.bold, self.italic,
                 dx, dy, anc),
                (self.sub, self.sub_size, TEXT_DIM, False, True, dx, sdy, sa)]

    def rects(self, cam, cand):
        """Screen ink rects of every text part, and the leader segment."""
        ax, ay = to_screen(cam, P(cand[0], cand[1]))
        rs = []
        g = grow(cam[0], self.gmax)
        for text, size, _f, bold, italic, dx, dy, anc in self.parts(cand):
            l, t, r, b = ink(text, size * g, bold, italic, anc)
            dx, dy = dx * g, dy * g
            rs.append((ax + dx + l, ay + dy + t, ax + dx + r, ay + dy + b))
        lead = None
        if len(cand) > 4 and cand[4]:
            hx, hy = to_screen(cam, P(*cand[3]))
            bx0, by0, bx1, by1 = union(rs)
            px = min(max(hx, bx0 - 3), bx1 + 3)
            py = min(max(hy, by0 - 3), by1 + 3)
            lead = ((hx, hy), (px, py))
        return rs, lead


# ---------------------------------------------------------------------------
# Inside-the-territory candidates: the points deepest inside the visible part
# of a territory (distance measured with horizontal distances counted at
# 40%, since a name is wide), best first.
# ---------------------------------------------------------------------------

def inner_points(rings_w, cam, hud, k=14, step=6, minsep=22):
    rings = [[to_screen(cam, P(a, b)) for a, b in r] for r in rings_w]
    xs = [p[0] for p in rings[0]]
    ys = [p[1] for p in rings[0]]
    x0, x1 = max(min(xs), SAFE[0] + 20), min(max(xs), SAFE[2] - 20)
    y0, y1 = max(min(ys), SAFE[1] + 12), min(max(ys), SAFE[3] - 12)
    if x1 <= x0 or y1 <= y0:
        return []
    scored = []
    edges = [(a, b) for r in rings for a, b in zip(r, r[1:] + r[:1])]
    yy = y0
    while yy <= y1:
        xx = x0
        while xx <= x1:
            pt = (xx, yy)
            if in_rings(pt, rings) and not any(
                    rr_hit((xx - 1, yy - 1, xx + 1, yy + 1), inflate(hr, 14))
                    for _k, hr in hud):
                d = min(_aniso(pt, a, b) for a, b in edges)
                d = min(d, (xx - SAFE[0]) * 0.4, (SAFE[2] - xx) * 0.4,
                        yy - SAFE[1], SAFE[3] - yy)
                scored.append((d, pt))
            xx += step
        yy += step
    scored.sort(key=lambda t: -t[0])
    out = []
    for d, pt in scored:
        if all(math.hypot(pt[0] - q[0], pt[1] - q[1]) >= minsep
               for q in out):
            out.append(pt)
        if len(out) >= k:
            break
    return [unproject(cam, x, y) for x, y in out]


def _aniso(pt, a, b, kx=0.4):
    p = (pt[0] * kx, pt[1])
    return seg_dist(p, (a[0] * kx, a[1]), (b[0] * kx, b[1]))


def pole_world(rings_w):
    """A territory's deepest point (isotropic), for leader homes."""
    pts = [P(a, b) for a, b in rings_w[0]]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    best = None
    rings = [[P(a, b) for a, b in r] for r in rings_w]
    n = 60
    for i in range(n + 1):
        for j in range(n + 1):
            x = min(xs) + (max(xs) - min(xs)) * i / n
            y = min(ys) + (max(ys) - min(ys)) * j / n
            if in_rings((x, y), rings):
                d = min(ring_dist((x, y), r) for r in rings)
                if best is None or d > best[0]:
                    best = (d, x, y)
    _d, x, y = best
    return LAT_TOP - y / K, x / (EFF * K) + LON_LEFT


POLE = {k: pole_world(r) for k, r in TRIBE_RINGS.items()}


# ---------------------------------------------------------------------------
# Section A units (vv1-15)
# ---------------------------------------------------------------------------

LM_PRIO = {"kadesh": 3, "lebo": 3, "mount_hor": 4, "hazar_enan": 4,
           "akrabbim": 4, "riblah": 5, "zedad": 6, "ziphron": 6,
           "shepham": 6, "azmon": 7, "hazar_addar": 7}


def tribe_cands(rings):
    return lambda cam, hud: [(a, b, "c") for a, b in
                             inner_points(rings, cam, hud)]


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


def ptsstr(pts):
    return " ".join(f"{_fmt(x)},{_fmt(y)}" for x, y in pts)


def rgb(c):
    return f"rgb({int(c[0])},{int(c[1])},{int(c[2])})"


def paint_fill(c):
    a = f'fill="{rgb(c)}"'
    if len(c) > 3 and c[3] < 255:
        a += f' fill-opacity="{c[3] / 255:.3f}"'
    return a


def poly_el(pts, fill=None, stroke=None, closed=False, extra=""):
    tag = "polygon" if closed else "polyline"
    a = [f'points="{ptsstr(pts)}"']
    a.append(paint_fill(fill) if fill else 'fill="none"')
    if stroke:
        a.append(f'stroke="{rgb(stroke)}"')
        if len(stroke) > 3 and stroke[3] < 255:
            a.append(f'stroke-opacity="{stroke[3] / 255:.3f}"')
    return f"<{tag} {' '.join(a)}{extra}/>"


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


def fade(begin, dur=0.5, out=False):
    v = "1;0" if out else "0;1"
    return (f'<animate attributeName="opacity" values="{v}" '
            f'begin="{begin:.2f}s" dur="{dur:.2f}s" fill="freeze" '
            f'calcMode="spline" keyTimes="0;1" keySplines="{EASE}"/>')


def op_anim(lo, hi, begin, dur):
    return (f'<animate attributeName="fill-opacity" values="{lo:.3f};{hi:.3f}"'
            f' dur="{dur:.2f}s" begin="{begin:.2f}s" fill="freeze" '
            f'calcMode="spline" keyTimes="0;1" keySplines="{EASE}"/>')


def traced_el(pts, stroke, begin, dur, closed=False):
    pts = pts + pts[:1] if closed else pts
    L = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))
    return (f'<polyline points="{ptsstr(pts)}" fill="none" '
            f'stroke-linejoin="round" stroke="{rgb(stroke)}" '
            f'stroke-dasharray="{_fmt(L)} {_fmt(L * 4)}" '
            f'stroke-dashoffset="{_fmt(L)}">'
            f'<animate attributeName="stroke-dashoffset" '
            f'values="{_fmt(L)};0" dur="{dur:.2f}s" begin="{begin:.2f}s" '
            f'fill="freeze" calcMode="spline" keyTimes="0;1" '
            f'keySplines="{EASE}"/></polyline>'), L


def seg_len(pts):
    return sum(math.hypot(b[0] - a[0], b[1] - a[1])
               for a, b in zip(pts, pts[1:]))


def frac_along(pts, target):
    """Arc-length fraction of the vertex nearest `target` along pts."""
    best, acc, at = 1e18, 0.0, 0.0
    total = seg_len(pts)
    for i, p in enumerate(pts):
        if i:
            acc += math.hypot(p[0] - pts[i - 1][0], p[1] - pts[i - 1][1])
        d = math.hypot(p[0] - target[0], p[1] - target[1])
        if d < best:
            best, at = d, acc
    return at / total if total else 1.0


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
                sc.qc.append((PS(r + r[:1]), "tribe", key))
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
            sc.qc.append((PS(r + r[:1]), "tribe", key))
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
    if not els:
        return ""
    a, anim = fl.inverse("stroke-width", CLS_PX[name])
    if name == "dash":
        da, danim = fl.inverse_dash(*DASH)
        a += " " + da
        anim += danim
    return (f'<g {a} stroke-linejoin="round"{extra}>{anim}'
            + "".join(els) + "</g>")


# ---------------------------------------------------------------------------
# Label layout at the rest camera
# ---------------------------------------------------------------------------

AIR_LABEL, AIR_LINE, AIR_DOT = 12.0, 3.0, 3.0
DOT_R = 4.5
DOT_IN = 8          # a dot's centre stays this far inside SAFE at rest


def dot_state(xy, hud):
    x, y = xy
    if x < -8 or x > W + 8 or y < -8 or y > H + 8:
        return "off"
    if (SAFE[0] + DOT_IN <= x <= SAFE[2] - DOT_IN and
            SAFE[1] + DOT_IN <= y <= SAFE[3] - DOT_IN and
            not any(circle_hits_rect(xy, DOT_R + 4, hr) for _k, hr in hud)):
        return "in"
    return "cut"


class Ctx:
    """Everything the clash test needs about the rest frame."""

    def __init__(self, cam, lines, dots, hud, focus, sec, tribes_a=False):
        self.cam, self.lines, self.dots, self.hud = cam, lines, dots, hud
        self.focus, self.sec = focus, sec
        rs = TRIBE_RINGS if sec == "B" else (
            {k: RINGS_A[k] for k in EAST_TRIBES} if tribes_a else {})
        self.tribes = {k: [[to_screen(cam, P(a, b)) for a, b in r]
                           for r in rings] for k, rings in rs.items()}
        self.land = [to_screen(cam, P(a, b)) for a, b in WORLD_LAND]
        self.canaan = [to_screen(cam, P(a, b)) for a, b in CANAAN_POLY]


def layout(units, ctx, prev):
    """Choose a size and a placement per unit (prio order; the previous
    verse's choice first when it is still clean)."""
    cam = ctx.cam
    placed, taken, leaders = [], [], []
    dropped, problems = [], []
    pplace = prev["place"] if prev else {}
    pbase = prev["base"] if prev else {}
    for u in sorted(units, key=lambda u: u.prio):
        cands = list(u.cands)
        if u.dyn:
            cands = u.dyn(cam, ctx.hud) + cands
        order = cands + u.auto_cands(cam)
        was_cur = prev and prev["units"].get(u.key, {}).get("cur")
        if u.key in pplace and not (len(pplace[u.key]) > 4 and
                                    abs(prev["cam1"][0] - cam[0]) > 1e-9) \
                and not (u.inside and (u.new or was_cur)):
            pp = pplace[u.key]
            if pp in order:
                order.remove(pp)
            order.insert(0, pp)
        g = grow(cam[0], u.gmax)
        bases = [b for b in u.bases if b * g >= u.min_px - 0.05] \
            or u.bases[:1]
        if bool(u.new) != bool(was_cur):
            pass                 # promoted or demoted: its own size now
        elif u.key in pbase and pbase[u.key] not in bases and \
                u.min_px - 0.05 <= pbase[u.key] * g <= \
                max(u.bases) * g + 0.05:
            bases = [pbase[u.key]] + bases
        elif u.key in pbase and pbase[u.key] in bases:
            bases.remove(pbase[u.key])
            bases.insert(0, pbase[u.key])
        if u.sub:
            u.sub_size = S_SUB / max(1.0, g) * (1.0 if g <= 1.2 else 1.15)
        chosen = None
        # a territory's name: inside it at any size before any leader
        passes = ([False, True] if u.inside else [None])
        for with_leaders in passes:
            for base in bases:
                u.size = base
                for cand in order:
                    is_lead = len(cand) > 4
                    if u.inside and is_lead and (not with_leaders
                                                 or not u.ring):
                        continue
                    if u.inside and not is_lead and with_leaders:
                        continue
                    rs, lead = u.rects(cam, cand)
                    if not clash(u, cand, rs, lead, ctx, taken, leaders):
                        chosen = (cand, rs, lead)
                        break
                if chosen:
                    break
            if chosen:
                break
        if chosen is None:
            if not u.must:
                dropped.append(u.key)
                # its dot is not drawn either, so it no longer blocks others
                ctx.dots = [(k, c) for k, c in ctx.dots if k != u.key]
                continue
            u.size = bases[-1]
            for cand in order:
                rs, lead = u.rects(cam, cand)
                if inside(union(rs)):
                    chosen = (cand, rs, lead)
                    break
            if chosen is None:
                dropped.append(u.key)
                continue
            problems.append((u.key, clash(u, chosen[0], chosen[1],
                                          chosen[2], ctx, taken, leaders)))
        cand, rs, lead = chosen
        u.place, u.rest_rects, u.lead = cand, rs, lead
        placed.append(u)
        taken += [(u.key, r) for r in rs]
        if lead:
            leaders.append((u.key, lead))
    return placed, dropped, problems


def inside(r):
    return (r[0] >= SAFE[0] and r[1] >= SAFE[1] and r[2] <= SAFE[2]
            and r[3] <= SAFE[3])


def clash(u, cand, rs, lead, ctx, taken, leaders):
    why = []
    cam = ctx.cam
    if u.dot:
        dxy = to_screen(cam, P(cand[0], cand[1]))
        if dot_state(dxy, ctx.hud) != "in":
            why.append("dot-cut")
        # a name must sit nearer its own dot than any other dot
        if not lead:
            ubox = union(rs)
            d_own = rect_dist(dxy, ubox)
            cx = (ubox[0] + ubox[2]) / 2
            for k, c in ctx.dots:
                # a dot at the same end of the name as its own is the
                # ambiguous case: it must be clearly farther away
                same_end = (c[0] - cx) * (dxy[0] - cx) > 0
                if k != u.key and rect_dist(c, ubox) < \
                        d_own + (12 if same_end else 4):
                    why.append("nearer-dot:" + k)
    ub = union(rs)
    centre = ((ub[0] + ub[2]) / 2, (ub[1] + ub[3]) / 2)
    if u.rings and not lead:
        rings = [[to_screen(cam, P(a, b)) for a, b in r] for r in u.rings]
        if not in_rings(centre, rings):
            why.append("outside-own-territory")
    if u.in_sea and pip(centre, ctx.land):
        why.append("sea-label-on-land")
    if not u.rings:
        # a place or water name never sits on a territory's tint
        for tk, trs in ctx.tribes.items():
            if in_rings(centre, trs):
                why.append("on-territory-" + tk)
    if u.out_poly is not None and pip(centre, ctx.canaan):
        why.append("inside-canaan")
    for r in rs:
        if not inside(r):
            why.append("edge")
        for hk, hr in ctx.hud:
            if rr_hit(inflate(r, 4), hr):
                why.append("hud:" + hk)
        for k, t in taken:
            if rr_hit((r[0] - 12, r[1] - AIR_LABEL, r[2] + 12,
                       r[3] + AIR_LABEL), t):
                why.append("label:" + k)
            # two names stacked one over the other read as name + gloss
            ov = min(r[2], t[2]) - max(r[0], t[0])
            if ov > 0.3 * min(r[2] - r[0], t[2] - t[0]) and \
                    max(t[1] - r[3], r[1] - t[3]) < 20:
                why.append("stacked:" + k)
        for k, (p, q) in leaders:
            if seg_hits_rect(p, q, inflate(r, 3)):
                why.append("leader:" + k)
        for pts, wpx, _kind, _key in ctx.lines:
            if poly_hits_rect(pts, inflate(r, AIR_LINE + wpx / 2)):
                why.append("line:" + _kind)
                break
        for k, c in ctx.dots:
            if circle_hits_rect(c, DOT_R + AIR_DOT, r):
                why.append("dot:" + k)
    if lead:
        why += leader_problems(u, lead, rs, centre, ctx, taken, leaders)
    return sorted(set(why))


def leader_problems(u, lead, rs, centre, ctx, taken, leaders):
    why = []
    own = u.key[2:] if u.key.startswith("t_") else None
    # the name may not sit on another territory (unless allowed)
    for tk, rings in ctx.tribes.items():
        if tk == own or tk in u.on_ok:
            continue
        if in_rings(centre, rings):
            why.append("label-on-" + tk)
    if own and own in ctx.tribes and in_rings(centre, ctx.tribes[own]):
        why.append("leader-label-inside-own")
    if not u.sea_ok and pip(centre, ctx.land) is False and own:
        why.append("label-in-sea")
    p, q = lead
    own_rings = ctx.tribes.get(own, [])
    for pts, _w, kind, key in ctx.lines:
        for a, b in zip(pts, pts[1:]):
            x = seg_x(p, q, a, b)
            if x is None or math.hypot(x[0] - p[0], x[1] - p[1]) < 7:
                continue          # (a landmark's own line, at its dot)
            if kind in ("river", "lake"):
                why.append("leader-x-water")
            elif kind == "coast":
                if not u.sea_ok:
                    why.append("leader-x-coast")
            elif kind == "tribe" and key != own:
                on_own = any(ring_dist(x, r) < 1.0 for r in own_rings)
                if on_own:
                    continue
                if key in ctx.focus:
                    why.append("leader-x-highlight")
                elif key not in u.cross_ok:
                    why.append("leader-x-" + key)
            elif kind == "border":
                why.append("leader-x-border")
    for k, t in taken:
        if seg_hits_rect(p, q, inflate(t, 2)):
            why.append("leader-x-label:" + k)
    for k, (a, b) in leaders:
        if seg_x(p, q, a, b):
            why.append("leader-x-leader:" + k)
    for k, c in ctx.dots:
        if seg_dist(c, p, q) < DOT_R + 2:
            why.append("leader-x-dot:" + k)
    return why


# ---------------------------------------------------------------------------
# Emission of labels and dots (screen-constant inside the camera group)
# ---------------------------------------------------------------------------

def text_el(x, y, part, op_anim_="", op0=None):
    text, size, fill, bold, italic, dx, dy, anc = part
    a = [f'x="{_fmt(x)}"', f'y="{_fmt(y)}"']
    if dx:
        a.append(f'dx="{dx / size:.3f}em"')
    if dy:
        a.append(f'dy="{dy / size:.3f}em"')
    a.append(f'text-anchor="{SVG_H[anc[0]]}"')
    a.append(f'dominant-baseline="{SVG_V[anc[1]]}"')
    a.append(f'fill="{rgb(fill)}"')
    if bold:
        a.append('font-weight="bold"')
    if italic:
        a.append('font-style="italic"')
    if op0 is not None:
        a.append(f'opacity="{op0}"')
    return f"<text {' '.join(a)}>{escape(text)}{op_anim_}</text>"


def label_elements(u, cand, op_anim_, op0, by_size, lead_els, cam_rest,
                   dip=""):
    x, y = P(cand[0], cand[1])
    for part in u.parts(cand):
        el = text_el(x, y, part, op_anim_, op0)
        if dip:
            el = f"<g>{dip}{el}</g>"
        by_size.setdefault((round(part[1], 2), u.gmax), []).append(el)
    if len(cand) > 4 and cand[4]:
        # rest-bound leader, sized for the rest camera
        rs, lead = u.rects(cam_rest, cand)
        s = cam_rest[0]
        (hx, hy), (px, py) = lead
        T = cam_T(cam_rest)
        w0 = ((hx - T[0]) / s, (hy - T[1]) / s)
        w1 = ((px - T[0]) / s, (py - T[1]) / s)
        o = f' opacity="{op0}"' if op0 is not None else ""
        lead_els.append(
            f'<g{o}>{op_anim_}<line x1="{_fmt(w0[0])}" y1="{_fmt(w0[1])}" '
            f'x2="{_fmt(w1[0])}" y2="{_fmt(w1[1])}" stroke="{rgb(TEXT_DIM)}" '
            f'stroke-width="{1.2 / s:.3f}"/>'
            f'<circle cx="{_fmt(w0[0])}" cy="{_fmt(w0[1])}" r="{2.6 / s:.3f}" '
            f'fill="{rgb(TEXT_DIM)}"/></g>')


def dot_elements(lat, lon, color, op_anim_, op0, halo, core):
    x, y = P(lat, lon)
    o = f' opacity="{op0}"' if op0 is not None else ""
    d = f'M{_fmt(x)} {_fmt(y)}h0'
    halo.append(f'<path d="{d}" stroke="{rgb(BG)}" stroke-opacity="0.85"{o}>'
                f'{op_anim_}</path>')
    core.append(f'<path d="{d}" stroke="{rgb(color)}"{o}>{op_anim_}</path>')


def hud_dip(u, fl, v, t_show):
    """While a name slides under a HUD plate mid-flight it dips out and comes
    back once clear (one dip per pass); returns the <animate>s."""
    if fl.static:
        return "", []
    step = 1 / 20
    n = int(fl.dur / step) + 1
    hits = []
    for i in range(n + 1):
        t = min(fl.dur, i * step)
        if t < t_show:
            continue
        cam = fl.at(t)
        hud = hud_rects(v, cam)
        rs, _ = u.rects(cam, u.place)
        if not any(rr_hit(r, (0, 0, W, H)) for r in rs):
            continue
        if any(rr_hit(inflate(r, 3), hr) for r in rs for _k, hr in hud):
            hits.append(t)
    if not hits:
        return "", []
    spans = []
    for t in hits:
        if spans and t - spans[-1][1] <= 0.5:
            spans[-1][1] = t
        else:
            spans.append([t, t])
    out = []
    for a, b in spans:
        t0 = a - 0.3
        t1 = b + 0.3
        if t0 < t_show + 0.01:
            # under the plate from the moment it shows, or too soon after to
            # fade out first: start hidden, so it never shows and dips
            out.append(f'<set attributeName="opacity" to="0" begin="0s"/>'
                       f'<animate attributeName="opacity" values="0;1" '
                       f'begin="{b:.2f}s" dur="0.30s" fill="freeze"/>')
        else:
            d = t1 - t0
            k1 = 0.3 / d
            k2 = (b - t0) / d
            assert 0 <= k1 <= k2 <= 1, (u.key, a, b, t_show)
            out.append(f'<animate attributeName="opacity" values="1;0;0;1" '
                       f'keyTimes="0;{k1:.3f};{k2:.3f};1" '
                       f'begin="{t0:.2f}s" dur="{d:.2f}s" fill="freeze"/>')
    return "".join(out), spans


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
        dots = []
        for u in units:
            if u.dot:
                xy = to_screen(cam1, P(*u.cands[0][:2]))
                if dot_state(xy, hud) == "in":
                    dots.append((u.key, xy))
        fk = focus_keys(v) if sec == "B" else set()
        ctx = Ctx(cam1, lines, dots, hud, fk, sec, tribes_a=v in (14, 15))
        same_sec = prev is not None and prev["sec"] == sec
        placed, dropped, problems = layout(units, ctx,
                                           prev if same_sec else None)
        placed_keys = {u.key for u in placed}

        prev_units = prev["units"] if same_sec else {}
        cur_ident = {}
        for u in placed:
            cur_ident[u.key] = (u.style(), u.place,
                                (round(cam1[0], 6) if len(u.place) > 4
                                 else None))

        # appear times for new content: when the trace reaches it, or landing
        for u in units:
            u.t_in = None
            pu = prev_units.get(u.key)
            if u.key in cur_ident and pu is not None and \
                    pu["ident"] == cur_ident[u.key]:
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

        by_size, lead_els, halo, core = {}, [], [], []
        dips = []
        for u in placed:
            ident = cur_ident[u.key]
            pu = prev_units.get(u.key)
            persist = pu is not None and pu["ident"] == ident
            op0, anim = None, ""
            if u.t_in is not None:
                op0, anim = "0", fade(u.t_in)
                u.t_show = u.t_in
            elif persist:
                u.t_show = 0.0
            else:
                rs0, _ = u.rects(cam0, u.place)
                onscreen0 = any(rr_hit(r, (0, 0, W, H)) for r in rs0)
                if not onscreen0 and len(u.place) <= 4 and not fl.static:
                    u.t_show = 0.0               # slides in with the pan
                elif pu is not None and pu["cur"] and (len(u.place) <= 4 or
                                                       fl.static):
                    # demoted: the old one leaves first, then this arrives,
                    # unless the camera is still too wide for it there
                    early = not touches_lines(u, fl, lines_w, 0.35, 0.75)
                    t = 0.35 if early else t_land
                    op0, anim = "0", fade(t, 0.4 if early else 0.5)
                    u.t_show = t
                else:
                    op0, anim = "0", fade(t_land)
                    u.t_show = t_land
            dip, spans = ("", []) if len(u.place) > 4 else \
                hud_dip(u, fl, v, u.t_show)
            if spans:
                dips.append((u.key, [(round(a, 2), round(b, 2))
                                     for a, b in spans]))
            label_elements(u, u.place, anim, op0, by_size, lead_els, cam1,
                           dip)

        # dots: a landmark's dot shows with its name (or as the verse's own),
        # and never cut by the frame or under a plate at rest
        cur_dots = {}
        for u in units:
            if not u.dot:
                continue
            la, lo = u.cands[0][:2]
            st = dot_state(to_screen(cam1, P(la, lo)), hud)
            if u.key not in placed_keys and not (u.must and st == "in"):
                continue
            if st == "cut":
                problems.append((u.key, ["dot cut at rest"]))
                continue
            cur_dots[u.key] = (la, lo, u.dot, u)
        prev_dots = prev["dots"] if same_sec else {}
        dot_t = {}
        for key, (la, lo, col, u) in cur_dots.items():
            pd = prev_dots.get(key)
            if pd is not None and pd == (la, lo, col):
                da, d0, t = "", None, 0.0
            elif u.t_in is not None and pd is None:
                da, d0, t = fade(u.t_in), "0", u.t_in
            elif pd is not None:
                t = getattr(u, "t_show", None)
                t = 0.15 if t is None else t
                if u.t_in is not None:
                    t = u.t_in
                da, d0 = fade(t), "0"
            else:
                c0 = to_screen(cam0, P(la, lo))
                if not fl.static and not (-10 < c0[0] < W + 10 and
                                          -10 < c0[1] < H + 10):
                    da, d0, t = "", None, 0.0
                else:
                    da, d0, t = fade(t_land), "0", t_land
            dot_t[key] = t
            dot_elements(la, lo, col, da, d0, halo, core)

        # the old versions of changed/removed labels and dots fade out
        old_by_size, old_lead, old_halo, old_core = {}, [], [], []
        exiting = []
        for key, pu in (prev["units"] if prev else {}).items():
            if same_sec and key in cur_ident and cur_ident[key] == pu["ident"]:
                continue
            uo = pu["unit"]
            rs0, _ = uo.rects(cam0, uo.place)
            if not any(rr_hit(r, (0, 0, W, H)) for r in rs0):
                continue
            nu = next((u for u in placed if u.key == key), None)
            if not same_sec:
                nu = None
            # never two versions of a name at once: the old one is gone
            # before the new one starts to show
            t_out = 0.0 if nu is None else max(0.0, nu.t_show - 0.35)
            if nu is not None and nu.place[:3] != uo.place[:3]:
                t_out = 0.0          # moved: leave now, the new one lands
            if len(uo.place) > 4 and not fl.static:
                t_out = 0.0          # a leader is drawn for one scale only
            d_out = 0.3 if nu is not None else 0.45
            label_elements(uo, uo.place, fade(t_out, d_out, out=True), None,
                           old_by_size, old_lead, prev["cam1"])
            exiting.append((uo, t_out + d_out))
        for key, pd in (prev["dots"] if prev else {}).items():
            if same_sec and cur_dots.get(key) and cur_dots[key][:3] == pd:
                continue
            c0 = to_screen(cam0, P(pd[0], pd[1]))
            if not (-10 < c0[0] < W + 10 and -10 < c0[1] < H + 10):
                continue
            t_out = max(0.0, dot_t.get(key, 0.05) - 0.05)
            dot_elements(pd[0], pd[1], pd[2], fade(t_out, 0.45, out=True),
                         None, old_halo, old_core)

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
        # dots
        for (h_els, c_els) in ((old_halo, old_core), (halo, core)):
            if h_els:
                a, an = fl.inverse("stroke-width", 10.0)
                svg.append(f'<g {a} stroke-linecap="round">{an}'
                           + "".join(h_els) + "</g>")
                a, an = fl.inverse("stroke-width", 7.0)
                svg.append(f'<g {a} stroke-linecap="round">{an}'
                           + "".join(c_els) + "</g>")
        svg += old_lead + lead_els
        for groups in (old_by_size, by_size):
            for size, gm in sorted(groups):
                a, an = fl.inverse("font-size", float(size), text=gm)
                svg.append(f'<g {a}>{an}' + "".join(groups[(size, gm)])
                           + "</g>")
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
        mid = midflight_qc(fl, placed, exiting)
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
            problems=problems, mid=mid, dips=dips,
            minpx=min(rest_px) if rest_px else None,
            ext=extent_check(fl)))

        prev = dict(sec=sec, cam1=cam1,
                    place={u.key: u.place for u in placed},
                    base={u.key: u.size for u in placed},
                    units={u.key: dict(ident=cur_ident[u.key], unit=u,
                                       cur=u.new)
                           for u in placed},
                    dots={k: d[:3] for k, d in cur_dots.items()})
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
    out = []
    tr = title_rect(title)
    out.append(f'<rect x="{tr[0]}" y="{tr[1]}" width="{_fmt(tr[2] - tr[0])}" '
               f'height="{_fmt(tr[3] - tr[1])}" rx="8" fill="{rgb(BG)}" '
               f'fill-opacity="0.82"/>')
    out.append(f'<text x="18" y="14" font-size="{TITLE_PX}" '
               f'font-weight="bold" fill="{rgb(TEXT)}" '
               f'dominant-baseline="text-before-edge">{escape(title)}</text>')

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
    # compass and scale bar sit on the map, so each mark is drawn twice: a
    # dark casing first (a halo, as on a printed map), then the mark, and no
    # map line runs through them
    x, y = W - 30, H - 82
    xr, yb = W - 18, H - 20
    lens = [SCALE_KM / 111.0 * K * cm[0] for cm in fl.cams]   # rides the
    xs = [f"{xr - L:.1f}" for L in lens]                       # camera
    tvals = [f"{xr - L:.1f} 0" for L in lens]
    halo = (f'stroke="{rgb(BG)}" stroke-opacity="0.85" '
            f'stroke-linecap="round" stroke-linejoin="round"')
    for paint, w in ((halo, 6), (f'stroke="{rgb(TEXT_DIM)}"', 2)):
        out.append(f'<g {paint} stroke-width="{w}" fill="none">'
                   f'<line x1="{x}" y1="{y + 24}" x2="{x}" y2="{y}"/>'
                   f'<polyline points="{x - 5},{y + 8} {x},{y} '
                   f'{x + 5},{y + 8}"/>'
                   f'<line x1="{xs[0]}" y1="{yb}" x2="{xr}" y2="{yb}">'
                   f'{fl._anim("x1", xs)}</line>'
                   f'<line x1="{xr}" y1="{yb - 4}" x2="{xr}" y2="{yb + 4}"/>'
                   f'<g transform="translate({tvals[0]})">'
                   f'{fl._anim("transform", tvals, "translate")}'
                   f'<line x1="0" y1="{yb - 4}" x2="0" y2="{yb + 4}"/></g>'
                   f'</g>')
    c = rgb(TEXT_DIM)
    text_halo = (f'stroke="{rgb(BG)}" stroke-opacity="0.85" '
                 f'stroke-width="4" stroke-linejoin="round" '
                 f'paint-order="stroke"')
    out.append(f'<text x="{x - 10}" y="{y + 4}" font-size="16" fill="{c}" '
               f'{text_halo} text-anchor="end" '
               f'dominant-baseline="central">N</text>'
               f'<text x="{xr}" y="{yb - 8}" font-size="16" fill="{c}" '
               f'{text_halo} font-style="italic" text-anchor="end" '
               f'dominant-baseline="text-after-edge">{SCALE_KM} km</text>')
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

    def view(cam):
        s, wx, wy = cam
        lon_c = wx / (EFF * K) + LON_LEFT
        lat_c = LAT_TOP - wy / K
        hw = W / 2 / s / (EFF * K)
        hh = H / 2 / s / K
        a = ip(lat_c + hh, lon_c - hw)
        b = ip(lat_c - hh, lon_c + hw)
        return a[0], a[1], b[0] - a[0], b[1] - a[1]
    vs = [view(c) for c in fl.cams]
    xv = [f"{q[0]:.1f}" for q in vs]
    yv = [f"{q[1]:.1f}" for q in vs]
    wv = [f"{q[2]:.1f}" for q in vs]
    hv = [f"{q[3]:.1f}" for q in vs]
    out.append(f'<rect x="{xv[0]}" y="{yv[0]}" width="{wv[0]}" '
               f'height="{hv[0]}" fill="{rgb(HL)}" fill-opacity="0.10" '
               f'stroke="{rgb(HL)}" stroke-width="1.5">'
               + fl._anim("x", xv) + fl._anim("y", yv)
               + fl._anim("width", wv) + fl._anim("height", hv)
               + "</rect>")
    return out


# ---------------------------------------------------------------------------
# QC helpers
# ---------------------------------------------------------------------------

def midflight_qc(fl, placed, exiting):
    """Label/label overlaps while the camera moves (visible labels only)."""
    if fl.static:
        return []
    hits = set()
    n = max(24, int(fl.dur * 8))
    for i in range(1, n):
        t = fl.dur * i / n
        cam = fl.at(t)
        vis = []
        for u in placed:
            if getattr(u, "t_show", 0) <= t and len(u.place) <= 4:
                rs, _ = u.rects(cam, u.place)
                vis += [(u.key, r) for r in rs]
        for uo, t_gone in exiting:
            if t < t_gone:
                rs, _ = uo.rects(cam, uo.place)
                vis += [("old:" + uo.key, r) for r in rs]
        vis = [(k, r) for k, r in vis if rr_hit(r, (0, 0, W, H))]
        for a in range(len(vis)):
            for b in range(a + 1, len(vis)):
                ka, kb = vis[a][0], vis[b][0]
                if ka.replace("old:", "") == kb.replace("old:", ""):
                    continue
                if rr_hit(vis[a][1], vis[b][1]):
                    hits.add((ka, kb, round(t, 1)))
    pairs = {}
    for ka, kb, t in hits:
        pairs.setdefault((ka, kb), []).append(t)
    return [(a, b, min(ts), max(ts)) for (a, b), ts in sorted(pairs.items())]


def touches_lines(u, fl, lines_w, t0, t1):
    """Whether a name at its rest place would touch a coast, river, lake,
    border or territory line at some moment between t0 and t1 of the
    flight (at a wider camera a name covers more of the map than at rest).
    lines_w: [(world polyline, width at rest in px)]."""
    steps = 8
    for i in range(steps + 1):
        cam = fl.at(t0 + (t1 - t0) * i / steps)
        rs, _ = u.rects(cam, u.place)
        for r in rs:
            if not rr_hit(r, (0, 0, W, H)):
                continue
            for pts, wpx in lines_w:
                screen = [to_screen(cam, p) for p in pts]
                if poly_hits_rect(screen, inflate(r, AIR_LINE + wpx / 2)):
                    return True
    return False


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


def extent_check(fl):
    """Is the world's drawn area ever visible past its edge?"""
    x0, y0 = P(WORLD_LAT[1], WORLD_LON[0])
    x1, y1 = P(WORLD_LAT[0], WORLD_LON[1])
    worst = None
    cams = list(fl.cams)
    if fl.pure_pan:
        cams = [fl.at(fl.dur * i / 20) for i in range(21)]
    for c in cams:
        a, b, cc, d = visible_world(c)
        if a < x0 or b < y0 or cc > x1 or d > y1:
            worst = "edge visible"
    return worst


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
