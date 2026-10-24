"""The map camera: one large lat/lon map seen through a moving SMIL camera.

Shared by the camera-tour maps (generate_numbers34_svg.py,
generate_acts1314_svg.py). A generator draws its whole map once per verse in
world units and wraps it in a camera group whose translate and scale are
animated (an animateTransform pair), the way 1 Chronicles 1-9 flies over its
family tree. Each verse opens on the previous verse's rest camera and flies to
its own, so played in order a chapter is one continuous flight.

What lives here:

* Projection: lat/lon to world units (K per degree of latitude), and the
  rest cameras (`shot`, `fit`) built on it.
* Flight: one verse's camera -- holds, van Wijk & Nuij pan-zoom arcs (the arc
  and the MP3 timer come from svg_chronicles_world) and eased pans -- baked
  into keyframes, plus the inverse-scale animations that keep a stroke, a
  dash or a name a constant screen size while the camera zooms (`inverse`).
  Text grows gently past a map's wide-shot scale (`Grow`).
* Unit, layout, clash: labels placed at each verse's rest camera by a clash
  test on Georgia ink boxes measured with PIL. A name never touches another
  name, a line, a dot, the frame edge or a plate; an area's name sits inside
  its own area when it fits. A generator adds its own rules through
  `Ctx.extra` and `Ctx.leader_extra`.
* Emission helpers (polylines, traced lines, fades, labels, dots), the HUD's
  title plate and compass/scale bar, the overview inset's view box, and the
  QC checks (`hud_dip`, `midflight_qc`, `touches_lines`, `extent_check`).

Everything is screen space at the rest camera except where a function says it
takes world or lat/lon coordinates. A camera is (s, wx, wy): world point
(wx, wy) sits at the screen centre at scale s.
"""

import math
from xml.sax.saxutils import escape

from PIL import ImageFont

from svg_surface import _fmt
from svg_chronicles_world import CAM_FPS, EASE, _smooth, _vw
from generate_tabernacle import W, H, BG, TEXT_DIM


# ---------------------------------------------------------------------------
# Projection: one world, K world units per degree of latitude, so a camera
# scale s shows the map at K*s px per degree.
# ---------------------------------------------------------------------------

class Projection:
    """Equirectangular, with longitude shrunk by cos(lat_ref)."""

    def __init__(self, lat_top, lon_left, lat_ref, k=100.0):
        self.lat_top, self.lon_left, self.k = lat_top, lon_left, k
        self.eff = math.cos(math.radians(lat_ref))

    def P(self, lat, lon):
        return ((lon - self.lon_left) * self.eff * self.k,
                (self.lat_top - lat) * self.k)

    def PS(self, seq):
        return [self.P(a, b) for a, b in seq]

    def latlon(self, x, y):
        """World point back to (lat, lon)."""
        return (self.lat_top - y / self.k,
                x / (self.eff * self.k) + self.lon_left)

    def unproject(self, cam, sx, sy):
        s, wx, wy = cam
        x = (sx - W / 2) / s + wx
        y = (sy - H / 2) / s + wy
        return self.latlon(x, y)

    def shot(self, lat, lon, pxdeg, sx=W / 2, sy=H / 2):
        """Rest camera that puts (lat, lon) at screen (sx, sy) at pxdeg
        px/deg."""
        s = pxdeg / self.k
        x, y = self.P(lat, lon)
        return (s, x - (sx - W / 2) / s, y - (sy - H / 2) / s)

    def fit(self, lat0, lat1, lon0, lon1, box=(0, 12, W, H - 12), cap=None):
        x0, y0, x1, y1 = box
        pxdeg = min((x1 - x0) / ((lon1 - lon0) * self.eff),
                    (y1 - y0) / (lat1 - lat0))
        if cap:
            pxdeg = min(cap, pxdeg)
        return self.shot((lat0 + lat1) / 2, (lon0 + lon1) / 2,
                         round(pxdeg, 1), (x0 + x1) / 2, (y0 + y1) / 2)

    def pole(self, rings_w):
        """An area's deepest point (isotropic), for leader homes."""
        pts = [self.P(a, b) for a, b in rings_w[0]]
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        best = None
        rings = [[self.P(a, b) for a, b in r] for r in rings_w]
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
        return self.latlon(x, y)


# ---------------------------------------------------------------------------
# Camera (svg_chronicles_world._vw, van Wijk & Nuij's pan-zoom arc, as in
# 1 Chronicles)
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


class Grow:
    """Text is a constant screen size up to a map's wide-shot scale `frm`
    and grows gently (sqrt) past it: a close-up's names are larger, for the
    phone. Called as grow(s) or grow(s, cap)."""

    def __init__(self, frm=1.9, pw=0.5, mx=1.4):
        self.frm, self.pw, self.mx = frm, pw, mx

    def __call__(self, s, gmax=None):
        return min(gmax or self.mx, max(1.0, (s / self.frm) ** self.pw))


GROW_MAX = 1.4
grow = Grow(1.9, 0.5, GROW_MAX)      # Numbers 34's wide shots are 190 px/deg


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
    into one uniformly spaced keyframe list.

    legs: [("hold", None, seconds) | ("to", cam, seconds)]. A subclass sets
    `grow` to its map's text growth."""

    grow = grow

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
        vals = [(fmt % (px * (self.grow(c[0], text) if text else 1.0)
                        / c[0]))
                for c in self.cams]
        return f'{attr}="{vals[0]}"', self._anim(attr, vals)

    def inverse_dash(self, a_px, b_px):
        vals = [f"{a_px / c[0]:.3f},{b_px / c[0]:.3f}" for c in self.cams]
        return f'stroke-dasharray="{vals[0]}"', self._anim("stroke-dasharray",
                                                            vals)


def cam_duration(cam0, cam1):
    """How long a flight from cam0 to cam1 takes (seconds) by default."""
    if _same(cam0, cam1):
        return 0.0
    s0, s1 = cam0[0], cam1[0]
    travel = math.hypot(cam1[1] - cam0[1], cam1[2] - cam0[2]) * max(s0, s1)
    if abs(s0 - s1) < 1e-9:
        return min(2.4, max(1.1, 0.8 + travel / 330.0))
    zoom = max(s0 / s1, s1 / s0)
    return min(3.0, max(1.3, 1.25 + 0.7 * math.log2(zoom) + travel / 1100.0))


def to_screen(cam, xy):
    s, wx, wy = cam
    return (W / 2 + s * (xy[0] - wx), H / 2 + s * (xy[1] - wy))


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


def title_rect(title):
    l, t, r, b = ink(title, TITLE_PX, True, False, "la")
    return (6, 4, 18 + r + 10, 14 + b + 7)


def compass_rect(proj, s, scale_km):
    bar = scale_km / 111.0 * proj.k * s
    return (W - 26 - max(bar, 64) - 8, H - 84, W, H)


def plate_rect_svg(r, extra=""):
    """A HUD plate: a dark rounded rect at 82% under its text."""
    return (f'<rect x="{_fmt(r[0])}" y="{_fmt(r[1])}" '
            f'width="{_fmt(r[2] - r[0])}" height="{_fmt(r[3] - r[1])}" '
            f'rx="8" fill="{rgb(BG)}" fill-opacity="0.82"{extra}/>')


def title_svg(title, fill):
    tr = title_rect(title)
    return (f'<rect x="{tr[0]}" y="{tr[1]}" width="{_fmt(tr[2] - tr[0])}" '
            f'height="{_fmt(tr[3] - tr[1])}" rx="8" fill="{rgb(BG)}" '
            f'fill-opacity="0.82"/>'
            f'<text x="18" y="14" font-size="{TITLE_PX}" '
            f'font-weight="bold" fill="{rgb(fill)}" '
            f'dominant-baseline="text-before-edge">{escape(title)}</text>')


def compass_scale_svg(fl, proj, scale_km):
    """North arrow and a scale bar that rides the camera. They sit on the
    map, so each mark is drawn twice: a dark casing first (a halo, as on a
    printed map), then the mark, and no map line runs through them."""
    out = []
    x, y = W - 30, H - 82
    xr, yb = W - 18, H - 20
    lens = [scale_km / 111.0 * proj.k * cm[0] for cm in fl.cams]
    xs = [f"{xr - L:.1f}" for L in lens]
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
               f'dominant-baseline="text-after-edge">{scale_km} km</text>')
    return "".join(out)


def inset_view_rect(fl, proj, ip, stroke, fill_op=0.10, min_px=0):
    """The overview inset's box round the camera's view, moving in lockstep
    with the camera. ip(lat, lon) maps into the inset. A view smaller than
    min_px (a deep close-up) is drawn as a min_px square on its centre."""
    def view(cam):
        s, wx, wy = cam
        lat_c, lon_c = proj.latlon(wx, wy)
        hw = W / 2 / s / (proj.eff * proj.k)
        hh = H / 2 / s / proj.k
        a = ip(lat_c + hh, lon_c - hw)
        b = ip(lat_c - hh, lon_c + hw)
        w, h = b[0] - a[0], b[1] - a[1]
        if min_px and w < min_px:
            cx, cy = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
            return cx - min_px / 2, cy - min_px / 2, min_px, min_px
        return a[0], a[1], w, h
    vs = [view(c) for c in fl.cams]
    xv = [f"{q[0]:.1f}" for q in vs]
    yv = [f"{q[1]:.1f}" for q in vs]
    wv = [f"{q[2]:.1f}" for q in vs]
    hv = [f"{q[3]:.1f}" for q in vs]
    return (f'<rect x="{xv[0]}" y="{yv[0]}" width="{wv[0]}" '
            f'height="{hv[0]}" fill="{rgb(stroke)}" '
            f'fill-opacity="{fill_op:.2f}" '
            f'stroke="{rgb(stroke)}" stroke-width="1.5">'
            + fl._anim("x", xv) + fl._anim("y", yv)
            + fl._anim("width", wv) + fl._anim("height", hv)
            + "</rect>")


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
    A subclass sets `proj` (its map's Projection) and `grow`.
    """

    proj = None
    grow = grow

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
        P = self.proj.P
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
                    la, lo = self.proj.unproject(cam, ax + ddx, ay + ddy)
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
                    la, lo = self.proj.unproject(cam, px, py)
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
        P = self.proj.P
        ax, ay = to_screen(cam, P(cand[0], cand[1]))
        rs = []
        g = self.grow(cam[0], self.gmax)
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
# Inside-an-area candidates: the points deepest inside the visible part of an
# area (distance measured with horizontal distances counted at 40%, since a
# name is wide), best first.
# ---------------------------------------------------------------------------

def inner_points(proj, rings_w, cam, hud, k=14, step=6, minsep=22):
    rings = [[to_screen(cam, proj.P(a, b)) for a, b in r] for r in rings_w]
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
    return [proj.unproject(cam, x, y) for x, y in out]


def _aniso(pt, a, b, kx=0.4):
    p = (pt[0] * kx, pt[1])
    return seg_dist(p, (a[0] * kx, a[1]), (b[0] * kx, b[1]))


# ---------------------------------------------------------------------------
# SVG emission helpers (world units inside the camera group)
# ---------------------------------------------------------------------------

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


def curve_d(pts, closed=False):
    """A path through pts as a Catmull-Rom curve (cubic Beziers), so a
    coast traced at a few km per point stays round in a close-up. World
    units to one decimal: a hundredth of a degree is well under a pixel in
    any close-up."""
    n = len(pts)

    def f(v):
        return f"{v:.1f}".rstrip("0").rstrip(".")
    if n < 3:
        return "M" + " L".join(f"{f(x)} {f(y)}" for x, y in pts)

    def at(i):
        if closed:
            return pts[i % n]
        return pts[max(0, min(n - 1, i))]
    out = [f"M{f(pts[0][0])} {f(pts[0][1])}"]
    for i in range(n if closed else n - 1):
        p0, p1, p2, p3 = at(i - 1), at(i), at(i + 1), at(i + 2)
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        out.append(f"C{f(c1[0])} {f(c1[1])} {f(c2[0])} {f(c2[1])} "
                   f"{f(p2[0])} {f(p2[1])}")
    if closed:
        out.append("Z")
    return "".join(out)


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


def emit_class(fl, px, els, extra="", dash=None):
    """A group of world elements whose stroke holds `px` screen pixels (and
    its dashes `dash` = (on, off) screen pixels) through the flight."""
    if not els:
        return ""
    a, anim = fl.inverse("stroke-width", px)
    if dash:
        da, danim = fl.inverse_dash(*dash)
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
    """Everything the clash test needs about the rest frame.

    lines: [(screen polyline, width px, kind, key)], kind one of coast,
    river, lake, border, area, route. dots: [(key, screen xy)]. hud:
    [(key, screen rect)]. areas: {key: screen rings} -- no name but an
    area's own may sit on one. land: the screen polygon of land, for a sea
    name. focus: the areas highlighted this verse. extra(u, cand, rs, lead,
    centre) and leader_extra(u, lead, rs, centre) return a map's own
    reasons a placement fails."""

    def __init__(self, proj, cam, lines, dots, hud, focus=(), areas=None,
                 land=None, extra=None, leader_extra=None):
        self.proj, self.cam, self.lines = proj, cam, lines
        self.dots, self.hud, self.focus = dots, hud, set(focus)
        self.areas = areas or {}
        self.land = land
        self.extra, self.leader_extra = extra, leader_extra


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
        g = u.grow(cam[0], u.gmax)
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
        # an area's name: inside it at any size before any leader
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
    P = ctx.proj.P
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
            why.append("outside-own-area")
    if u.in_sea and ctx.land is not None and pip(centre, ctx.land):
        why.append("sea-label-on-land")
    if not u.rings:
        # a place or water name never sits on an area's tint
        for tk, trs in ctx.areas.items():
            if in_rings(centre, trs):
                why.append("on-area-" + tk)
    if ctx.extra:
        why += ctx.extra(u, cand, rs, lead, centre)
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
    # the name may not sit on another area (unless allowed)
    for tk, rings in ctx.areas.items():
        if tk == own or tk in u.on_ok:
            continue
        if in_rings(centre, rings):
            why.append("label-on-" + tk)
    if own and own in ctx.areas and in_rings(centre, ctx.areas[own]):
        why.append("leader-label-inside-own")
    if not u.sea_ok and ctx.land is not None and \
            pip(centre, ctx.land) is False and own:
        why.append("label-in-sea")
    p, q = lead
    own_rings = ctx.areas.get(own, [])
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
            elif kind == "area" and key != own:
                on_own = any(ring_dist(x, r) < 1.0 for r in own_rings)
                if on_own:
                    continue
                if key in ctx.focus:
                    why.append("leader-x-highlight")
                elif key not in u.cross_ok:
                    why.append("leader-x-" + key)
            elif kind in ("border", "route"):
                why.append("leader-x-" + kind)
    for k, t in taken:
        if seg_hits_rect(p, q, inflate(t, 2)):
            why.append("leader-x-label:" + k)
    for k, (a, b) in leaders:
        if seg_x(p, q, a, b):
            why.append("leader-x-leader:" + k)
    for k, c in ctx.dots:
        if seg_dist(c, p, q) < DOT_R + 2:
            why.append("leader-x-dot:" + k)
    if ctx.leader_extra:
        why += ctx.leader_extra(u, lead, rs, centre)
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
    x, y = u.proj.P(cand[0], cand[1])
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


def dot_elements(proj, lat, lon, color, op_anim_, op0, halo, core):
    x, y = proj.P(lat, lon)
    o = f' opacity="{op0}"' if op0 is not None else ""
    d = f'M{_fmt(x)} {_fmt(y)}h0'
    halo.append(f'<path d="{d}" stroke="{rgb(BG)}" stroke-opacity="0.85"{o}>'
                f'{op_anim_}</path>')
    core.append(f'<path d="{d}" stroke="{rgb(color)}"{o}>{op_anim_}</path>')


def hud_dip(u, fl, hud_at, t_show):
    """While a name slides under a HUD plate mid-flight it dips out and comes
    back once clear (one dip per pass); returns the <animate>s and the spans.
    hud_at(cam) gives the HUD rects at a camera."""
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
        hud = hud_at(cam)
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
            k2 = max(k1, (b - t0) / d)      # (one hit: a == b, k2 == k1)
            assert 0 <= k1 <= k2 <= 1, (u.key, a, b, t_show)
            out.append(f'<animate attributeName="opacity" values="1;0;0;1" '
                       f'keyTimes="0;{k1:.3f};{k2:.3f};1" '
                       f'begin="{t0:.2f}s" dur="{d:.2f}s" fill="freeze"/>')
    return "".join(out), spans


# ---------------------------------------------------------------------------
# One verse's labels: what stays, what fades in, what fades out
#
# A generator lays out its units (layout), sets u.t_in on the units that are
# new or changed and should appear at a set time (None = the default rules
# below), then calls emit_labels and writes emit_label_layers(...) inside the
# camera group. prev is the previous verse's state (prev_state) or None.
# ---------------------------------------------------------------------------

def rest_dots(proj, units, cam1, hud):
    """[(key, screen xy)] of the dots that rest in frame."""
    dots = []
    for u in units:
        if u.dot:
            xy = to_screen(cam1, proj.P(*u.cands[0][:2]))
            if dot_state(xy, hud) == "in":
                dots.append((u.key, xy))
    return dots


def identities(placed, cam1):
    """A placed name's identity: same style and place (and, for a leader,
    the same scale) means it simply stays from the verse before."""
    return {u.key: (u.style(), u.place,
                    (round(cam1[0], 6) if len(u.place) > 4 else None))
            for u in placed}


def unchanged(u, cur_ident, prev_units):
    pu = prev_units.get(u.key)
    return (u.key in cur_ident and pu is not None and
            pu["ident"] == cur_ident[u.key])


def emit_labels(proj, units, placed, cur_ident, prev, same_sec, cam0, cam1,
                fl, t_land, hud, hud_at, lines_w, problems):
    """Label, leader and dot elements for one verse, the outgoing versions
    of the previous verse's, and the bookkeeping the QC and the next verse
    need. Returns a dict (see the keys at the end)."""
    placed_keys = {u.key for u in placed}
    prev_units = prev["units"] if same_sec else {}
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
            hud_dip(u, fl, hud_at, u.t_show)
        if spans:
            dips.append((u.key, [(round(a, 2), round(b, 2))
                                 for a, b in spans]))
        label_elements(u, u.place, anim, op0, by_size, lead_els, cam1,
                       dip)

    # dots: a place's dot shows with its name (or as the verse's own), and
    # never cut by the frame or under a plate at rest
    cur_dots = {}
    for u in units:
        if not u.dot:
            continue
        la, lo = u.cands[0][:2]
        st = dot_state(to_screen(cam1, proj.P(la, lo)), hud)
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
            c0 = to_screen(cam0, proj.P(la, lo))
            if not fl.static and not (-10 < c0[0] < W + 10 and
                                      -10 < c0[1] < H + 10):
                da, d0, t = "", None, 0.0
            else:
                da, d0, t = fade(t_land), "0", t_land
        dot_t[key] = t
        dot_elements(proj, la, lo, col, da, d0, halo, core)

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
        c0 = to_screen(cam0, proj.P(pd[0], pd[1]))
        if not (-10 < c0[0] < W + 10 and -10 < c0[1] < H + 10):
            continue
        t_out = max(0.0, dot_t.get(key, 0.05) - 0.05)
        dot_elements(proj, pd[0], pd[1], pd[2], fade(t_out, 0.45, out=True),
                     None, old_halo, old_core)
    return dict(by_size=by_size, lead_els=lead_els, halo=halo, core=core,
                old_by_size=old_by_size, old_lead=old_lead,
                old_halo=old_halo, old_core=old_core, exiting=exiting,
                dips=dips, cur_dots=cur_dots)


def emit_label_layers(fl, lab, dot_px=(10.0, 7.0)):
    """The dots (a dark halo under a core), the leaders and the names, each
    held at its screen size, outgoing versions first."""
    svg = []
    for (h_els, c_els) in ((lab["old_halo"], lab["old_core"]),
                           (lab["halo"], lab["core"])):
        if h_els:
            a, an = fl.inverse("stroke-width", dot_px[0])
            svg.append(f'<g {a} stroke-linecap="round">{an}'
                       + "".join(h_els) + "</g>")
            a, an = fl.inverse("stroke-width", dot_px[1])
            svg.append(f'<g {a} stroke-linecap="round">{an}'
                       + "".join(c_els) + "</g>")
    svg += lab["old_lead"] + lab["lead_els"]
    for groups in (lab["old_by_size"], lab["by_size"]):
        for size, gm in sorted(groups, key=lambda k: (k[0], k[1] or 0)):
            a, an = fl.inverse("font-size", float(size), text=gm)
            svg.append(f'<g {a}>{an}' + "".join(groups[(size, gm)])
                       + "</g>")
    return svg


def prev_state(cam1, placed, cur_ident, cur_dots, **extra):
    """What the next verse needs to know about this one."""
    return dict(cam1=cam1,
                place={u.key: u.place for u in placed},
                base={u.key: u.size for u in placed},
                units={u.key: dict(ident=cur_ident[u.key], unit=u,
                                   cur=u.new)
                       for u in placed},
                dots={k: d[:3] for k, d in cur_dots.items()}, **extra)


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
    border or area line at some moment between t0 and t1 of the flight (at a
    wider camera a name covers more of the map than at rest).
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


def extent_check(fl, proj, lat_range, lon_range):
    """Is the world's drawn area (lat_range x lon_range) ever visible past
    its edge?"""
    x0, y0 = proj.P(lat_range[1], lon_range[0])
    x1, y1 = proj.P(lat_range[0], lon_range[1])
    worst = None
    cams = list(fl.cams)
    if fl.pure_pan:
        cams = [fl.at(fl.dur * i / 20) for i in range(21)]
    for c in cams:
        a, b, cc, d = visible_world(c)
        if a < x0 or b < y0 or cc > x1 or d > y1:
            worst = "edge visible"
    return worst
