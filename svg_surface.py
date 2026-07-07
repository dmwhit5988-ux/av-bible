"""A tiny SVG canvas, shaped to mirror the subset of PIL's ImageDraw that the
verse-graphic generators use, so their hand-tuned geometry can be re-emitted
as vector SVG instead of rasterised WebP.

Design notes
------------
* Colours are the same (r, g, b) or (r, g, b, a) tuples the PIL generators
  already pass around; alpha becomes an SVG ``*-opacity`` attribute.
* Text anchors use PIL's two-letter form (e.g. ``"mm"``, ``"lm"``, ``"mb"``)
  and are mapped to ``text-anchor`` + ``dominant-baseline`` here, so callers
  can pass the exact anchor strings the raster code used.
* ``group()`` is a context manager for a translated + clipped ``<g>``, which
  stands in for the raster trick of rendering a map into its own sub-image
  and pasting it at an offset (geometry outside the window is clipped).

Only what the generators need is implemented — this is a dev tool, not a
general SVG library.
"""

import math
from contextlib import contextmanager
from xml.sax.saxutils import escape

FONT_FAMILY = "Georgia, 'Times New Roman', serif"

# PIL anchor (2 chars): horizontal l/m/r, vertical a/t (top), m (middle),
# s (baseline), b/d (bottom). Mapped to SVG text-anchor + dominant-baseline.
_HALIGN = {"l": "start", "m": "middle", "r": "end"}
_VALIGN = {"a": "text-before-edge", "t": "text-before-edge", "m": "central",
           "s": "alphabetic", "b": "text-after-edge", "d": "text-after-edge"}


def _rgb(c):
    return f"rgb({int(c[0])},{int(c[1])},{int(c[2])})"


def _opacity(c):
    return c[3] / 255.0 if len(c) > 3 else 1.0


def _fmt(v):
    """Compact number: drop trailing zeros, integers print without a dot."""
    return f"{v:.2f}".rstrip("0").rstrip(".")


def _pts(points):
    return " ".join(f"{_fmt(x)},{_fmt(y)}" for x, y in points)


# Shared easing + polyline length, used by the "draw once, then hold" reveals
# (SvgCanvas.traced/grown and SvgAnimLayer below).
_EASE = "0.42 0 0.58 1"


def _poly_length(points):
    return sum(math.hypot(b[0] - a[0], b[1] - a[1])
              for a, b in zip(points, points[1:]))


def _fill_stroke(fill, stroke, width):
    """Shared fill/stroke attribute list for (r,g,b[,a]) tuples."""
    a = []
    if fill is not None:
        a.append(f'fill="{_rgb(fill)}"')
        op = _opacity(fill)
        if op < 1:
            a.append(f'fill-opacity="{op:.3f}"')
    else:
        a.append('fill="none"')
    if stroke is not None:
        a.append(f'stroke="{_rgb(stroke)}"')
        a.append(f'stroke-width="{_fmt(width)}"')
        op = _opacity(stroke)
        if op < 1:
            a.append(f'stroke-opacity="{op:.3f}"')
    return a


def _box(box):
    """Normalise PIL's two box forms -> (x0, y0, x1, y1). PIL accepts both
    [(x0, y0), (x1, y1)] and [x0, y0, x1, y1]."""
    if len(box) == 2:
        (x0, y0), (x1, y1) = box
        return x0, y0, x1, y1
    return box[0], box[1], box[2], box[3]


def _font_meta(font):
    """(size, bold, italic) from a PIL ImageFont, so the reused raster
    drawing code can pass its F_* fonts straight through to SVG text."""
    size = getattr(font, "size", 14) if font is not None else 14
    bold = italic = False
    if font is not None:
        try:
            _, style = font.getname()
            style = style or ""
            bold = "Bold" in style
            italic = "Italic" in style or "Oblique" in style
        except Exception:
            pass
    return size, bold, italic


class SvgCanvas:
    def __init__(self, w, h, bg=None):
        self.w, self.h = w, h
        self._els = []
        self._defs = []
        self._clip_id = 0
        if bg is not None:
            self.rect(0, 0, w, h, fill=bg)

    # -- primitives ---------------------------------------------------------

    def _emit(self, s):
        self._els.append(s)

    def raw(self, elements):
        """Inject pre-built element strings (e.g. from an SvgLayer)."""
        self._els.extend(elements)

    def rect(self, x, y, w, h, fill=None, stroke=None, width=1, rx=None):
        a = [f'x="{_fmt(x)}"', f'y="{_fmt(y)}"',
             f'width="{_fmt(w)}"', f'height="{_fmt(h)}"']
        if rx is not None:
            a.append(f'rx="{_fmt(rx)}"')
        a += self._paint(fill, stroke, width)
        self._emit(f"<rect {' '.join(a)}/>")

    def line(self, p0, p1, stroke, width=1, dash=None, linecap="butt"):
        a = [f'x1="{_fmt(p0[0])}"', f'y1="{_fmt(p0[1])}"',
             f'x2="{_fmt(p1[0])}"', f'y2="{_fmt(p1[1])}"',
             f'stroke="{_rgb(stroke)}"', f'stroke-width="{_fmt(width)}"']
        op = _opacity(stroke)
        if op < 1:
            a.append(f'stroke-opacity="{op:.3f}"')
        if dash:
            a.append(f'stroke-dasharray="{dash}"')
        if linecap != "butt":
            a.append(f'stroke-linecap="{linecap}"')
        self._emit(f"<line {' '.join(a)}/>")

    def polyline(self, points, stroke, width=1, dash=None, closed=False,
                 fill=None, linejoin="round"):
        tag = "polygon" if closed else "polyline"
        a = [f'points="{_pts(points)}"', f'stroke-linejoin="{linejoin}"']
        a += self._paint(fill, stroke, width)
        if dash:
            a.append(f'stroke-dasharray="{dash}"')
        self._emit(f"<{tag} {' '.join(a)}/>")

    def polygon(self, points, fill=None, stroke=None, width=1):
        a = [f'points="{_pts(points)}"']
        a += self._paint(fill, stroke, width)
        self._emit(f"<polygon {' '.join(a)}/>")

    def circle(self, cx, cy, r, fill=None, stroke=None, width=1):
        a = [f'cx="{_fmt(cx)}"', f'cy="{_fmt(cy)}"', f'r="{_fmt(r)}"']
        a += self._paint(fill, stroke, width)
        self._emit(f"<circle {' '.join(a)}/>")

    def ellipse(self, cx, cy, rx, ry, fill=None, stroke=None, width=1):
        a = [f'cx="{_fmt(cx)}"', f'cy="{_fmt(cy)}"',
             f'rx="{_fmt(rx)}"', f'ry="{_fmt(ry)}"']
        a += self._paint(fill, stroke, width)
        self._emit(f"<ellipse {' '.join(a)}/>")

    def path(self, d, fill=None, stroke=None, width=1, linecap="butt"):
        a = [f'd="{d}"']
        a += self._paint(fill, stroke, width)
        if linecap != "butt":
            a.append(f'stroke-linecap="{linecap}"')
        self._emit(f"<path {' '.join(a)}/>")

    def text(self, xy, s, size, fill, anchor="lm", bold=False, italic=False):
        if s == "":
            return
        ta = _HALIGN[anchor[0]]
        db = _VALIGN[anchor[1]] if len(anchor) > 1 else "alphabetic"
        a = [f'x="{_fmt(xy[0])}"', f'y="{_fmt(xy[1])}"',
             f'font-size="{_fmt(size)}"', f'text-anchor="{ta}"',
             f'dominant-baseline="{db}"', f'fill="{_rgb(fill)}"',
             f'font-family="{FONT_FAMILY}"']
        op = _opacity(fill)
        if op < 1:
            a.append(f'fill-opacity="{op:.3f}"')
        if bold:
            a.append('font-weight="bold"')
        if italic:
            a.append('font-style="italic"')
        self._emit(f"<text {' '.join(a)}>{escape(s)}</text>")

    # -- SMIL animation helpers --------------------------------------------
    #
    # Two motion styles, matching the two raster generators:
    #  * traced()/grown() — the tribal maps' "draw once, then hold": a stroke
    #    reveals itself (dash-offset) / a fill grows in, then freezes.
    #  * group(pulse=...)  — the tabernacle's perpetual breathing glow: the
    #    whole highlight layer's opacity oscillates forever (in the raster
    #    version every overlay element shares one pulsing alpha, so a single
    #    group-opacity animation reproduces it exactly).

    _EASE = "0.42 0 0.58 1"

    @staticmethod
    def _polylen(points):
        return sum(math.hypot(b[0] - a[0], b[1] - a[1])
                   for a, b in zip(points, points[1:]))

    def traced(self, points, stroke, width=1, dur="2.4s", closed=False):
        """Polyline that draws itself once (stroke reveal), then freezes."""
        pts = points + points[:1] if closed else points
        length = self._polylen(pts)
        a = [f'points="{_pts(pts)}"', 'fill="none"', 'stroke-linejoin="round"',
             f'stroke="{_rgb(stroke)}"', f'stroke-width="{_fmt(width)}"',
             f'stroke-dasharray="{_fmt(length)}"',
             f'stroke-dashoffset="{_fmt(length)}"']
        op = _opacity(stroke)
        if op < 1:
            a.append(f'stroke-opacity="{op:.3f}"')
        anim = (f'<animate attributeName="stroke-dashoffset" '
                f'values="{_fmt(length)};0" dur="{dur}" begin="0s" '
                f'fill="freeze" calcMode="spline" keyTimes="0;1" '
                f'keySplines="{self._EASE}"/>')
        self._emit(f"<polyline {' '.join(a)}>{anim}</polyline>")

    def grown(self, points, fill, lo, hi, dur="2.4s"):
        """Filled polygon whose opacity grows from lo to hi once, then holds."""
        a = [f'points="{_pts(points)}"', f'fill="{_rgb(fill)}"',
             'stroke="none"', f'fill-opacity="{lo:.3f}"']
        anim = (f'<animate attributeName="fill-opacity" '
                f'values="{lo:.3f};{hi:.3f}" dur="{dur}" begin="0s" '
                f'fill="freeze" calcMode="spline" keyTimes="0;1" '
                f'keySplines="{self._EASE}"/>')
        self._emit(f"<polygon {' '.join(a)}>{anim}</polygon>")

    # -- fill/stroke attribute helper --------------------------------------

    def _paint(self, fill, stroke, width):
        a = []
        if fill is not None:
            a.append(f'fill="{_rgb(fill)}"')
            op = _opacity(fill)
            if op < 1:
                a.append(f'fill-opacity="{op:.3f}"')
        else:
            a.append('fill="none"')
        if stroke is not None:
            a.append(f'stroke="{_rgb(stroke)}"')
            a.append(f'stroke-width="{_fmt(width)}"')
            op = _opacity(stroke)
            if op < 1:
                a.append(f'stroke-opacity="{op:.3f}"')
        return a

    # -- grouping (translate + clip window) --------------------------------

    @contextmanager
    def group(self, tx=0, ty=0, clip=None, pulse=None):
        """A <g>. `clip` clips to a (w, h) window; `pulse` = (lo, hi, dur)
        oscillates the group opacity forever (the tabernacle breathing glow)."""
        attrs = ""
        if clip is not None:
            self._clip_id += 1
            cid = f"clip{self._clip_id}"
            cw, ch = clip
            self._defs.append(
                f'<clipPath id="{cid}">'
                f'<rect x="0" y="0" width="{_fmt(cw)}" height="{_fmt(ch)}"/>'
                f'</clipPath>')
            attrs += f' clip-path="url(#{cid})"'
        if tx or ty:
            attrs += f' transform="translate({_fmt(tx)},{_fmt(ty)})"'
        if pulse is not None:
            attrs += f' opacity="{pulse[0]}"'
        self._emit(f"<g{attrs}>")
        if pulse is not None:
            lo, hi, dur = pulse
            self._emit(
                f'<animate attributeName="opacity" '
                f'values="{lo};{hi};{lo}" dur="{dur}" begin="0s" '
                f'repeatCount="indefinite" calcMode="spline" '
                f'keyTimes="0;0.5;1" '
                f'keySplines="0.4 0 0.6 1;0.4 0 0.6 1"/>')
        yield self
        self._emit("</g>")

    # -- output -------------------------------------------------------------

    def tostring(self):
        defs = f"<defs>{''.join(self._defs)}</defs>" if self._defs else ""
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 0 {self.w} {self.h}" '
            f'width="{self.w}" height="{self.h}" '
            f'font-family="{FONT_FAMILY}">'
            f"{defs}{''.join(self._els)}</svg>"
        )

    def save(self, path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.tostring())


class SvgLayer:
    """A drop-in stand-in for PIL's ImageDraw.Draw that records the subset of
    calls the tabernacle/altar generators make and emits SVG element strings.

    This lets the existing, hand-tuned raster drawing functions (draw_plan,
    inset_*, hl_*) run unchanged against SVG: pass one SvgLayer as their base
    ``d`` and another as their overlay ``od``, then hand ``.elements()`` to an
    SvgCanvas (the overlay inside a pulsing group, matching the raster
    generator's alpha-composited, breathing highlight layer).
    """

    def __init__(self):
        self._els = []

    def elements(self):
        return self._els

    # -- ImageDraw-compatible surface --------------------------------------

    def line(self, xy, fill=None, width=1, joint=None):
        # xy: a sequence of (x, y) points (the generators never use the flat
        # [x0, y0, x1, y1] form). joint="curve" is a raster antialias hint —
        # irrelevant to SVG.
        # PIL's `fill` on a line is the stroke colour; _fill_stroke adds the
        # single fill="none".
        self._els.append(
            f'<polyline points="{_pts(xy)}" '
            f'stroke-linejoin="round" stroke-linecap="round" '
            + " ".join(_fill_stroke(None, fill, width)) + "/>")

    def rectangle(self, box, fill=None, outline=None, width=1):
        x0, y0, x1, y1 = _box(box)
        a = [f'x="{_fmt(x0)}"', f'y="{_fmt(y0)}"',
             f'width="{_fmt(x1 - x0)}"', f'height="{_fmt(y1 - y0)}"']
        a += _fill_stroke(fill, outline, width)
        self._els.append(f"<rect {' '.join(a)}/>")

    def rounded_rectangle(self, box, radius=0, fill=None, outline=None,
                          width=1):
        x0, y0, x1, y1 = _box(box)
        a = [f'x="{_fmt(x0)}"', f'y="{_fmt(y0)}"',
             f'width="{_fmt(x1 - x0)}"', f'height="{_fmt(y1 - y0)}"',
             f'rx="{_fmt(radius)}"']
        a += _fill_stroke(fill, outline, width)
        self._els.append(f"<rect {' '.join(a)}/>")

    def ellipse(self, box, fill=None, outline=None, width=1):
        x0, y0, x1, y1 = _box(box)
        a = [f'cx="{_fmt((x0 + x1) / 2)}"', f'cy="{_fmt((y0 + y1) / 2)}"',
             f'rx="{_fmt((x1 - x0) / 2)}"', f'ry="{_fmt((y1 - y0) / 2)}"']
        a += _fill_stroke(fill, outline, width)
        self._els.append(f"<ellipse {' '.join(a)}/>")

    def polygon(self, xy, fill=None, outline=None, width=1):
        a = [f'points="{_pts(xy)}"']
        a += _fill_stroke(fill, outline, width)
        self._els.append(f"<polygon {' '.join(a)}/>")

    def arc(self, box, start, end, fill=None, width=1):
        x0, y0, x1, y1 = _box(box)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        rx, ry = (x1 - x0) / 2, (y1 - y0) / 2
        a0, a1 = math.radians(start), math.radians(end)
        p0 = (cx + rx * math.cos(a0), cy + ry * math.sin(a0))
        p1 = (cx + rx * math.cos(a1), cy + ry * math.sin(a1))
        span = (end - start) % 360
        large = 1 if span > 180 else 0
        # PIL sweeps clockwise from start to end; in SVG's y-down space that
        # is sweep-flag 1.
        d = (f"M{_fmt(p0[0])},{_fmt(p0[1])} "
             f"A{_fmt(rx)},{_fmt(ry)} 0 {large} 1 "
             f"{_fmt(p1[0])},{_fmt(p1[1])}")
        a = [f'd="{d}"'] + _fill_stroke(None, fill, width)
        self._els.append(f"<path {' '.join(a)}/>")

    def text(self, xy, s, font=None, fill=(0, 0, 0), anchor=None):
        if s == "":
            return
        anchor = anchor or "la"
        size, bold, italic = _font_meta(font)
        ta = _HALIGN[anchor[0]]
        db = _VALIGN[anchor[1]] if len(anchor) > 1 else "alphabetic"
        a = [f'x="{_fmt(xy[0])}"', f'y="{_fmt(xy[1])}"',
             f'font-size="{_fmt(size)}"', f'text-anchor="{ta}"',
             f'dominant-baseline="{db}"', f'fill="{_rgb(fill)}"',
             f'font-family="{FONT_FAMILY}"']
        op = _opacity(fill)
        if op < 1:
            a.append(f'fill-opacity="{op:.3f}"')
        if bold:
            a.append('font-weight="bold"')
        if italic:
            a.append('font-style="italic"')
        self._els.append(f"<text {' '.join(a)}>{escape(s)}</text>")

    def textlength(self, s, font=None):
        """Pixel advance width, so the reused raster code that positions one
        element after a name (the Genesis 5:32 trio connector) lands the same.
        The real PIL font is passed straight through, so this matches exactly.
        """
        if font is not None:
            try:
                return font.getlength(s)
            except Exception:
                pass
        size, _, _ = _font_meta(font)
        return len(s) * size * 0.5


class SvgAnimLayer(SvgLayer):
    """An overlay SvgLayer for the genealogy-family SVGs whose growing pieces
    animate themselves in once and then hold — reproducing the raster loop's
    "play once, then freeze" reveal with no re-derived geometry.

    In those generators the overlay (``od``) carries exactly the elements that
    grow: every ``line`` is a stroke that extends (a chain edge, a connector),
    and every ``rectangle`` is a lifespan bar that fills rightward. So here a
    line becomes a self-drawing stroke (dash-offset) and a rectangle a
    left-to-right wipe (width 0 -> full); ellipses/text (the steady focus
    ring, the year labels) stay static via the inherited SvgLayer methods.
    """

    def __init__(self, dur="2.4s"):
        super().__init__()
        self.dur = dur

    def line(self, xy, fill=None, width=1, joint=None):
        length = _poly_length(xy)
        if length <= 0 or fill is None:
            return super().line(xy, fill=fill, width=width, joint=joint)
        a = [f'points="{_pts(xy)}"', 'fill="none"',
             'stroke-linejoin="round"', 'stroke-linecap="round"',
             f'stroke="{_rgb(fill)}"', f'stroke-width="{_fmt(width)}"',
             f'stroke-dasharray="{_fmt(length)}"',
             f'stroke-dashoffset="{_fmt(length)}"']
        op = _opacity(fill)
        if op < 1:
            a.append(f'stroke-opacity="{op:.3f}"')
        anim = (f'<animate attributeName="stroke-dashoffset" '
                f'values="{_fmt(length)};0" dur="{self.dur}" begin="0s" '
                f'fill="freeze" calcMode="spline" keyTimes="0;1" '
                f'keySplines="{_EASE}"/>')
        self._els.append(f"<polyline {' '.join(a)}>{anim}</polyline>")

    def rectangle(self, box, fill=None, outline=None, width=1):
        x0, y0, x1, y1 = _box(box)
        full = x1 - x0
        if full <= 0:
            return super().rectangle(box, fill=fill, outline=outline,
                                     width=width)
        a = [f'x="{_fmt(x0)}"', f'y="{_fmt(y0)}"',
             f'width="{_fmt(full)}"', f'height="{_fmt(y1 - y0)}"']
        a += _fill_stroke(fill, outline, width)
        anim = (f'<animate attributeName="width" values="0;{_fmt(full)}" '
                f'dur="{self.dur}" begin="0s" fill="freeze" '
                f'calcMode="spline" keyTimes="0;1" keySplines="{_EASE}"/>')
        self._els.append(f"<rect {' '.join(a)}>{anim}</rect>")
