"""Drawing vocabulary shared by the per-verse book generators.

The generators are otherwise self-contained — each owns its own layout,
palette extras and scene functions — but the small marks they all make
(a stick figure, an arrow, a struck-out label, a tally row) were being
copied from book to book, and a copy drifts. This module holds the ones
that are genuinely book-independent, plus the text metrics every measured
box needs.

Nothing here knows about a canvas size, a palette or a chapter: callers
pass colours and coordinates. Used by generate_2peter_svg.py and
generate_zephaniah_svg.py; the older generators still carry their own
copies and are left alone.
"""

import math
import os

# ---------------------------------------------------------------------------
# Colour helpers
# ---------------------------------------------------------------------------


def dim(col, a):
    """The palette colour at `a` opacity, in the (r, g, b, a) form SvgCanvas
    takes (it turns the fourth element into a fill-/stroke-opacity)."""
    return (col[0], col[1], col[2], int(255 * a))


def mix(a, b, t):
    """Linear blend of two palette colours."""
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


# ---------------------------------------------------------------------------
# Text metrics
# ---------------------------------------------------------------------------
#
# Boxes, rings and strike-throughs are sized from the label's real advance
# width in the canvas font (Georgia — see svg_surface.FONT_FAMILY), never from
# a characters-times-a-guess estimate, which under-measures caps in a serif
# face and crops the ends of engraved phrases.

_FONT_FILES = {(False, False): "georgia.ttf", (True, False): "georgiab.ttf",
               (False, True): "georgiai.ttf", (True, True): "georgiaz.ttf"}
_FONT_DIR = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
_font_cache, _width_cache = {}, {}

_PROBE = 64          # measure once at this size, scale linearly


def _font(bold, italic):
    key = (bold, italic)
    if key not in _font_cache:
        try:
            from PIL import ImageFont
            _font_cache[key] = ImageFont.truetype(
                os.path.join(_FONT_DIR, _FONT_FILES[key]), _PROBE)
        except Exception:
            _font_cache[key] = None
    return _font_cache[key]


def text_w(s, size, bold=False, italic=False):
    """Rendered width of `s` at `size`, in canvas units."""
    key = (s, bold, italic)
    if key not in _width_cache:
        f = _font(bold, italic)
        _width_cache[key] = (f.getlength(s) / _PROBE if f
                             else len(s) * 0.66)      # safe over-estimate
    return _width_cache[key] * size


# ---------------------------------------------------------------------------
# Reading position
# ---------------------------------------------------------------------------


def reading_position(ch_len):
    """Build the (P, since) pair a book uses to place elements in time.

    P(ch, v) is one running number across the whole book; since(pos, ch, v)
    returns (shown, first) for an element that appears at ch:v, where `first`
    marks the single verse it animates on — the house "draw once, then hold"
    rule. Returning closures keeps each book's chapter lengths private.
    """
    offset, run = {}, 0
    for ch in sorted(ch_len):
        offset[ch] = run
        run += ch_len[ch]

    def P(ch, v):
        return offset[ch] + v

    def since(pos, ch, v):
        p = P(ch, v)
        return pos >= p, pos == p

    return P, since


# ---------------------------------------------------------------------------
# Marks
# ---------------------------------------------------------------------------


def figure(c, x, gy, h, col, width=2, arms="down", legs="stand", lean=0.0):
    """A stick figure standing on ground line gy, total height h. `lean`
    shifts the head sideways as a fraction of h (leaning forward)."""
    r = h * 0.14
    hy = gy - h + r                       # head centre
    ny = hy + r                           # neck
    hip = gy - h * 0.42
    dx = lean * h
    c.circle(x + dx, hy, r, stroke=col, width=width)
    c.line((x + dx, ny), (x, hip), col, width)
    ay = ny + h * 0.14                    # shoulder
    ax = x + dx * 0.6
    if arms == "down":
        c.line((ax, ay), (ax - h * 0.16, ay + h * 0.24), col, width)
        c.line((ax, ay), (ax + h * 0.16, ay + h * 0.24), col, width)
    elif arms == "open":
        c.line((ax, ay), (ax - h * 0.26, ay - h * 0.10), col, width)
        c.line((ax, ay), (ax + h * 0.26, ay - h * 0.10), col, width)
    elif arms == "up":
        c.line((ax, ay), (ax - h * 0.20, ay - h * 0.28), col, width)
        c.line((ax, ay), (ax + h * 0.20, ay - h * 0.28), col, width)
    elif arms == "point_r":
        c.line((ax, ay), (ax - h * 0.14, ay + h * 0.22), col, width)
        c.line((ax, ay), (ax + h * 0.36, ay - h * 0.06), col, width)
    elif arms == "point_l":
        c.line((ax, ay), (ax + h * 0.14, ay + h * 0.22), col, width)
        c.line((ax, ay), (ax - h * 0.36, ay - h * 0.06), col, width)
    elif arms == "hold_r":                # holding something out to the right
        c.line((ax, ay), (ax - h * 0.15, ay + h * 0.22), col, width)
        c.line((ax, ay), (ax + h * 0.30, ay + h * 0.06), col, width)
    elif arms == "grope":                 # both hands out, feeling the way
        c.line((ax, ay), (ax + h * 0.30, ay - h * 0.02), col, width)
        c.line((ax, ay), (ax + h * 0.24, ay + h * 0.16), col, width)
    if legs == "stand":
        c.line((x, hip), (x - h * 0.14, gy), col, width)
        c.line((x, hip), (x + h * 0.14, gy), col, width)
    elif legs == "walk":
        c.line((x, hip), (x - h * 0.20, gy), col, width)
        c.line((x, hip), (x + h * 0.16, gy - h * 0.04), col, width)
    elif legs == "kneel":
        c.line((x, hip), (x - h * 0.22, gy), col, width)
        c.line((x, hip), (x + h * 0.18, gy - h * 0.02), col, width)
        c.line((x - h * 0.22, gy), (x + h * 0.04, gy), col, width)
    else:                                 # fall — legs swept up
        c.line((x, hip), (x - h * 0.24, gy - h * 0.14), col, width)
        c.line((x, hip), (x + h * 0.10, gy), col, width)


def beast(c, x, gy, ln, col, width=1.8, head_low=False, tail=True):
    """A four-footed silhouette. Deliberately generic — only the label names
    it, so the same mark serves a donkey, a dog, a sow, a lion, a flock."""
    bh = ln * 0.42
    by = gy - bh * 1.5
    c.ellipse(x, by, ln * 0.46, bh * 0.52, stroke=col, width=width)
    for dx in (-0.32, -0.14, 0.16, 0.34):
        c.line((x + ln * dx, by + bh * 0.42), (x + ln * dx, gy), col, width)
    hx = x + ln * 0.50
    hy = by + (bh * 0.42 if head_low else -bh * 0.30)
    c.line((x + ln * 0.34, by - bh * 0.18), (hx, hy), col, width)
    c.circle(hx, hy, bh * 0.30, stroke=col, width=width)
    c.line((hx + bh * 0.24, hy + bh * 0.06),
           (hx + bh * 0.24 + ln * 0.13, hy + bh * 0.14), col, width)
    if tail:
        c.line((x - ln * 0.46, by - bh * 0.10),
               (x - ln * 0.62, by - bh * 0.44), col, width)


def lying_beast(c, x, gy, ln, col, width=1.8):
    """A beast lying down — the posture Zephaniah gives both to the animals
    in ruined Nineveh and to the remnant that no one makes afraid."""
    bh = ln * 0.34
    by = gy - bh * 0.60
    c.ellipse(x, by, ln * 0.46, bh * 0.50, stroke=col, width=width)
    hx = x + ln * 0.48
    hy = by - bh * 0.44
    c.line((x + ln * 0.30, by - bh * 0.24), (hx, hy), col, width)
    c.circle(hx, hy, bh * 0.32, stroke=col, width=width)
    c.line((x - ln * 0.30, gy), (x + ln * 0.16, gy), col, width)


def bird(c, x, y, w, col, width=1.8):
    """A bird on the wing, facing right: two swept wings, a body and a head.
    The bare two-arc gull glyph reads as a squiggle at this size, so the body
    and head are drawn — they are what make it a bird rather than a mark."""
    c.ellipse(x, y, w * 0.11, w * 0.055, stroke=col, width=width)
    c.path(f"M{x - w * 0.06},{y - w * 0.03} "
           f"Q{x - w * 0.24},{y - w * 0.26} {x - w * 0.50},{y - w * 0.20}",
           stroke=col, width=width)
    c.path(f"M{x + w * 0.02},{y - w * 0.03} "
           f"Q{x - w * 0.06},{y - w * 0.28} {x - w * 0.22},{y - w * 0.34}",
           stroke=col, width=width)
    c.circle(x + w * 0.15, y - w * 0.035, w * 0.045, stroke=col, width=width)
    c.line((x + w * 0.19, y - w * 0.035), (x + w * 0.26, y - w * 0.01),
           col, width)
    c.line((x - w * 0.11, y + w * 0.03), (x - w * 0.24, y + w * 0.10),
           col, width)                                  # tail


def fish(c, x, y, ln, col, width=1.6):
    """A fish facing right: a pointed body, a forked tail behind it, a dorsal
    fin and an eye. The eye is what settles which end is the head."""
    c.path(f"M{x - ln * 0.30},{y} "
           f"Q{x - ln * 0.04},{y - ln * 0.23} {x + ln * 0.42},{y} "
           f"Q{x - ln * 0.04},{y + ln * 0.23} {x - ln * 0.30},{y} Z",
           stroke=col, width=width)
    c.polyline([(x - ln * 0.30, y), (x - ln * 0.50, y - ln * 0.17),
                (x - ln * 0.43, y), (x - ln * 0.50, y + ln * 0.17),
                (x - ln * 0.30, y)], col, width)         # forked tail
    c.polyline([(x - ln * 0.02, y - ln * 0.17), (x + ln * 0.10, y - ln * 0.30),
                (x + ln * 0.15, y - ln * 0.13)], col, width)   # dorsal fin
    c.circle(x + ln * 0.25, y - ln * 0.04, ln * 0.035, fill=col)


def arrow(c, p0, p1, col, width=2.0, head=9.0, dash=None):
    """A straight arrow from p0 to p1."""
    c.line(p0, p1, col, width, dash=dash)
    ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    for s in (+1, -1):
        a = ang + math.pi + s * 0.42
        c.line(p1, (p1[0] + head * math.cos(a), p1[1] + head * math.sin(a)),
               col, width)


def cross(c, x, y, r, col, width=2.6):
    """The mark that cancels a thing."""
    c.line((x - r, y - r), (x + r, y + r), col, width)
    c.line((x - r, y + r), (x + r, y - r), col, width)


def struck(c, xy, s, size, col, rule, bold=False):
    """A label with a rule through it, measured off the text so the strike
    neither overshoots nor stops short."""
    c.text(xy, s, size, col, "mm", bold=bold)
    w = text_w(s, size, bold=bold)
    c.line((xy[0] - w / 2 - 7, xy[1]), (xy[0] + w / 2 + 7, xy[1]), rule, 2.2)


def tick_row(c, x0, y, n, step, col, width=1.6, h=11):
    """A row of tally marks."""
    for i in range(n):
        c.line((x0 + i * step, y), (x0 + i * step, y - h), col, width)


def hatch(c, x0, y0, x1, y1, col, step=13, width=1.0):
    """Diagonal fill for a dead region: a pit, a dry shaft, a mire, a drop."""
    span = (x1 - x0) + (y1 - y0)
    i = 0
    while i * step < span:
        d = i * step
        ax, ay = x0 + d, y0
        bx, by = x0, y0 + d
        if ax > x1:
            ay += ax - x1
            ax = x1
        if by > y1:
            bx += by - y1
            by = y1
        if ay <= y1 and bx <= x1:
            c.line((ax, ay), (bx, by), col, width)
        i += 1


def flame(c, x, gy, h, col):
    """One tongue of fire standing on gy."""
    c.path(f"M{x},{gy} q{-h * 0.30},{-h * 0.52} {h * 0.10},{-h} "
           f"q{h * 0.06},{h * 0.36} {h * 0.24},{h * 0.50} "
           f"q{h * 0.10},{-h * 0.26} {h * 0.02},{-h * 0.48} "
           f"q{h * 0.34},{h * 0.52} {h * 0.06},{h * 0.98} z", fill=col)
