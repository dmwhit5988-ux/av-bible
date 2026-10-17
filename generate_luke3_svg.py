"""Render Luke 3:23-38 as per-verse vector SVGs — the vector twin of the
taproot-descent WebP animations (generate_luke3.py).

Luke's motion is a camera descending one long taproot from the tree at the
surface (Jesus) down through era strata to the light at "of God". That
descent lives in the coordinate mapping, so the whole root world — strata,
tree, root line, every node and name, the glow — is drawn once in root
space inside a <g>, and that group's translate slides from the verse's
starting camera to its resting camera and freezes. Because the root wanders
side to side, the screen-fixed overlays that must track its tip (the bright
"just travelled" sweep, the traveler ring, the depth-gauge progress) are
animated with sampled value lists computed from the same eased trajectory
as the raster frames, keeping everything in lockstep with the dolly.
Names/geometry, fonts and colours are the WebP's own.

Run inside the project venv:
    .venv\\Scripts\\python.exe generate_luke3_svg.py
"""

import math
import os
import time

import svg_figures as F

from svg_surface import SvgCanvas, SvgLayer, _rgb, _fmt
from generate_tabernacle import (W, H, BG, SAND, SAND_DIM, TEXT, TEXT_DIM, HL,
                                 GOLD, RED, GRAY, ease, out_path)
from generate_luke3 import (
    extract_line, build_grid, era_of, strata_bands, root_x,
    CY, SPACING, ROOT_FREQ, SURFACE, TOP_STRIP, BOT_STRIP,
    GA_X, GA_Y0, GA_Y1, V23_LIFT, STRATA_LINE, STRATA,
    F_ROOT, F_ROOT_B, F_ERA,
)
from passages import PassageError, TRANSLATIONS

DUR = "5.5s"                        # slow crawl — most of a verse's narration
SAMPLES = 25                        # keyframes for tip-tracking animations


def _op(color):
    return color[3] / 255.0 if len(color) > 3 else 1.0


def _stroke_attrs(color, width, linecap="round"):
    a = (f'stroke="{_rgb(color)}" stroke-width="{_fmt(width)}" '
         f'stroke-linecap="{linecap}"')
    op = _op(color)
    if op < 1:
        a += f' stroke-opacity="{op:.3f}"'
    return a


def _keytimes():
    return ";".join(f"{k / (SAMPLES - 1):.4f}" for k in range(SAMPLES))


def _anim_seq(attr, values):
    vals = ";".join(_fmt(v) for v in values)
    return (f'<animate attributeName="{attr}" values="{vals}" '
            f'keyTimes="{_keytimes()}" dur="{DUR}" begin="0s" '
            f'fill="freeze" calcMode="linear"/>')


def tip_track(verse, prev, end):
    """The camera's eased tip positions (px, root space), one per sample —
    the same trajectory the raster frames follow."""
    tip0 = prev * SPACING - (V23_LIFT if verse == 23 else 0)
    tip1 = (end - 1) * SPACING
    return [tip0 + (tip1 - tip0) * ease(min(1.0, (k / (SAMPLES - 1)) / 0.92))
            for k in range(SAMPLES)]


def root_pts(s0, s1, ys, step=0.25):
    pts, s = [], s0
    while s < s1:
        pts.append((root_x(s), ys(s * SPACING)))
        s += step
    pts.append((root_x(s1), ys(s1 * SPACING)))
    return pts


# ---------------------------------------------------------------------------
# One plant, two halves
# ---------------------------------------------------------------------------
#
# The chapter's first half stands above ground and its second half descends
# the root, so the tree and the root have to be the SAME tree and the same
# root across the handover at 3:22 -> 3:23. Both halves therefore draw them
# from here: the vocabulary's tree, and a taproot built the way every limb in
# svg_figures is built — a taper that leaves the trunk at the trunk's own
# width and thins with depth. The 3px line this replaces read as a wire the
# camera slid down rather than as the thing the axe was laid against.

TRUNK_W = 17.0                      # svg_figures' trunk base, in local units
ROOT_W0 = 34.0                      # px where the root leaves the trunk
ROOT_W1 = 7.0                       # px by the time it reaches Adam
TREE_H = 236                        # the tree, both halves
ROOT_FILL = (108, 86, 58)           # the root's wood


def _mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def blit(layer, parts, x, gy, s, ink, page=BG, flip=1):
    """svg_figures parts onto a PIL-shaped SvgLayer. The vocabulary emits for
    an SvgCanvas; the root world is drawn on a layer so it can be dollied as
    one group, so the two have to be bridged."""
    sheet = F.palette(tuple(ink[:3]), page)
    for kind, data, mat in parts:
        fill, stroke, wd = sheet.get(mat, sheet["rule"])
        w = max(1, int(round(wd)))
        if kind == "dot":
            (cx, cy), = F.place([(data[0], data[1])], x, gy, s, flip)
            r = data[2] * s
            layer.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill,
                          outline=stroke, width=w)
        elif kind == "fill":
            layer.polygon(F.place(data, x, gy, s, flip), fill=fill,
                          outline=stroke, width=w)
        else:
            layer.line(F.place(data, x, gy, s, flip), fill=stroke, width=w)


def tree_scale(height):
    parts = F.tree()
    y0, y1 = F.bbox((parts, 0))[2:]
    return height / (y1 - y0)


def draw_tree_on(layer, x, gy, height, fruit=0, bare=False, col=SAND):
    """The tree at the surface. Returns the trunk's base width in pixels, so
    the root below can leave it at exactly the thickness it arrives with."""
    parts = F.tree(fruit=fruit, bare=bare)
    sc = tree_scale(height)
    blit(layer, parts, x, gy, sc, col)
    return TRUNK_W * sc


def root_width(s, s_end):
    """Thickness of the taproot at generation `s`.

    It falls away FAST — most of the way from the trunk's width to its
    running width inside two generations — for the same reason a real
    taproot does, and for one this drawing needs: below the surface the root
    carries seventy-six names beside it, and a mass thirty pixels wide
    swallows them. Thick where it leaves the trunk so the handover from the
    chapter's first half is seamless, slim everywhere a name has to be read.
    """
    return ROOT_W1 + (ROOT_W0 - ROOT_W1) * math.exp(-max(0.0, s) / 1.4)


def root_taper(s0, s1, ys, s_end, step=0.25):
    """The root between two generations, as a tapered mass."""
    pts, widths, s = [], [], s0
    while s < s1:
        pts.append((root_x(s), ys(s * SPACING)))
        widths.append(root_width(s, s_end))
        s += step
    pts.append((root_x(s1), ys(s1 * SPACING)))
    widths.append(root_width(s1, s_end))
    if len(pts) < 2:
        return None
    return F.taper(pts, widths, round_end=False)


# ---------------------------------------------------------------------------
# 3:1-22 — the chapter above ground
# ---------------------------------------------------------------------------
#
# One continuous scene, held for twenty-two verses. Nothing cuts: things
# arrive, light on their own verse, and stay. It exists to reach 3:9 — the
# tree gains fruit at 3:8 and the AXE IS LAID AT ITS ROOT at 3:9 — so that
# when 3:23 drops below ground the listener has already been told the root is
# the thing to look at, and the genealogy is the answer to what the axe was
# laid against rather than a list appended to a sermon.
#
# The register is emblematic, and strictly so: the tree is Jesus, so no human
# figure appears anywhere. Only what the chapter itself makes an image of is
# drawn — the rulers' sky, the levelling ground, the cry over the Jordan, the
# fruit, the axe, the floor, the bars, the dove. "The crowds asked him" is
# narrative, not an image, and its answers hang on the tree as the fruit they
# are called.
#
# GY and TRUNK_X are the frame 3:23's dolly BEGINS on, so the handover is
# seamless — the last above-ground frame and the first below-ground one show
# the same tree in the same place.

GY = CY + SURFACE + V23_LIFT        # 434.4
TRUNK_X = root_x(SURFACE / SPACING)  # 483.8
SKY_Y = 96
RIVER_X0, VOICE_X = 40, 150
FLOOR_X = 800
WATER = (96, 122, 152)
FIRE = (216, 124, 58)

RULERS = [("Tiberius Caesar", 1), ("Pontius Pilate", 1), ("Herod", 1),
          ("Philip", 1), ("Lysanias", 1), ("Annas", 2), ("Caiaphas", 2)]
JOHN_SAYS = {3: "BAPTISM OF REPENTANCE", 4: "THE VOICE OF ONE CRYING",
             6: "ALL FLESH SHALL SEE IT", 7: "GENERATION OF VIPERS",
             16: "ONE MIGHTIER THAN I COMES"}
ANSWERS = {10: "WHAT SHALL WE DO?", 11: "two coats — give one",
           12: "what shall we do?", 13: "exact no more",
           14: "be content with your wages"}
FRUIT_AT = (8, 11, 13, 14)          # 3:10-14 answers ARE the fruit of 3:8


def _dim(col, a):
    return (col[0], col[1], col[2], int(255 * a))


def _put_h(c, parts, x, gy, h, col, flip=1):
    y0, y1 = F.bbox((parts, 0))[2:]
    F.draw(c, parts, x, gy, h / (y1 - y0), col, BG, flip=flip)


def _put_w(c, parts, x, gy, w, col, flip=1):
    x0, x1 = F.bbox((parts, 0))[:2]
    F.draw(c, parts, x, gy, w / (x1 - x0), col, BG, flip=flip)


def render_above_svg(verse):
    """One frame of 3:1-22."""
    v = verse
    c = SvgCanvas(W, H, bg=BG)
    c.text((28, 26), "The Word Came to John — Luke 3", 22, TEXT, "la",
           bold=True)
    c.text((28, 54), f"v{v}", 13, _dim(TEXT_DIM, 0.85), "la", italic=True)

    # 3:1-2 — seven men named to date one year, dimmed once the word comes
    for i, (name, at) in enumerate(RULERS):
        if v < at:
            continue
        x = 92 + i * 140
        live = v <= 2
        col = HL if v == at else (_dim(TEXT, 0.9) if live
                                  else _dim(TEXT_DIM, 0.5))
        c.text((x, SKY_Y), name, 12.5, col, "mm", bold=(v == at))
        c.line((x - 30, SKY_Y + 12), (x + 30, SKY_Y + 12),
               _dim(SAND_DIM, 0.9 if live else 0.45), 1)
    if v >= 2:
        c.text((W / 2, SKY_Y + 34), "the word of God came to John", 12,
               HL if v == 2 else _dim(TEXT_DIM, 0.9), "mm", italic=True)

    # 3:5 — every valley filled and every mountain brought low; the ground
    # is rough until the voice asks for it, then settles over two verses
    k = 1.0 if v < 5 else max(0.0, 1.0 - (v - 4) / 2.0)
    pts = [(x, GY - (18 * math.sin(x * 0.017)
                     + 11 * math.sin(x * 0.041 + 1.2)) * k)
           for x in range(0, W + 1, 8)]
    c.polygon(pts + [(W, H), (0, H)], fill=STRATA[0])
    c.polyline(pts, _dim(SAND_DIM, 0.95), 2)

    # the taproot, showing from the first verse — what the second half runs
    prev_pts, widths = [], []
    for j in range(9):
        s = j * 0.32
        prev_pts.append((TRUNK_X + root_x(s) - root_x(0), GY + s * SPACING))
        widths.append(root_width(s, 75))
    c.polygon(F.taper(prev_pts, widths, round_end=False),
              fill=_mix(BG, ROOT_FILL, 0.55), stroke=_dim(SAND, 0.9), width=2)
    for j in (2, 4, 6):
        jx, jy = prev_pts[j]
        pw = widths[j]
        for sx in (-1, 1):
            c.polygon(F.taper([(jx, jy), (jx + sx * 17, jy + 9),
                               (jx + sx * 36, jy + 20)],
                              [pw * 0.52, pw * 0.30, pw * 0.12],
                              round_end=False),
                      fill=_mix(BG, ROOT_FILL, 0.46),
                      stroke=_dim(SAND_DIM, 0.9), width=1)

    # the Jordan, and the voice over it — no figure: Luke's own quotation
    # calls John a VOICE, and in a scene where the tree is Jesus a literal
    # man beside it mixes the two registers
    if v >= 3:
        for dy in (-16, -6, 4):
            c.path(f"M{RIVER_X0},{GY + dy} q34,-9 68,0 q34,9 68,0 "
                   f"q34,-9 64,0", stroke=_dim(WATER, 0.8), width=2.2)
        c.text((140, GY + 30), "THE JORDAN", 11.5, _dim(TEXT_DIM, 0.95), "mm")
    if 3 <= v < 20:
        speaks = v in JOHN_SAYS
        col = HL if speaks else _dim(SAND, 0.5)
        for j in range(4):
            r = 26 + j * 20
            c.path(f"M{VOICE_X - r * 0.35},{GY - 30 - r} "
                   f"a{r},{r} 0 0 1 {r * 0.70},0",
                   stroke=_dim(col, 0.9 - j * 0.18), width=1.8)
        if speaks:
            c.text((VOICE_X, GY - 150), JOHN_SAYS[v], 13, HL, "mm", bold=True)

    # the tree — the same tree, in the same place, that 3:23 descends from
    fruit = sum(1 for at in FRUIT_AT if v >= at)
    parts = F.tree(fruit=fruit)
    F.draw(c, parts, TRUNK_X, GY, tree_scale(TREE_H),
           HL if v in (8, 9) else SAND, BG)
    if v == 8:
        c.text((TRUNK_X, GY - TREE_H - 20), "FRUITS WORTHY OF REPENTANCE",
               13, HL, "mm", bold=True)
    if v in ANSWERS:
        c.text((TRUNK_X + 168, GY - TREE_H * 0.62), ANSWERS[v], 13, HL, "lm",
               bold=True)

    # 3:9 — and even now the axe lies at the root of the trees
    if v >= 9:
        _put_w(c, F.axe(), TRUNK_X - 34, GY + 8, 96,
               HL if v == 9 else _dim(SAND, 0.8), flip=-1)
        c.text((TRUNK_X - 96, GY + 46), "THE AXE AT THE ROOT", 12,
               HL if v == 9 else _dim(TEXT_DIM, 0.95), "mm", bold=v == 9)

    # 3:17 — the floor purged, the wheat gathered, the chaff burnt
    if v >= 17:
        c.ellipse(FLOOR_X, GY + 10, 112, 20, stroke=_dim(SAND, 0.9), width=1.8)
        c.text((FLOOR_X, GY + 46), "THE THRESHING FLOOR", 11.5,
               HL if v == 17 else _dim(TEXT_DIM, 0.95), "mm", bold=v == 17)
        for dx in (-52, -22, 8):
            _put_h(c, F.herb(), FLOOR_X + dx, GY + 4, 34, _dim(GOLD, 0.9))
        for j in range(5):
            fx, fy = FLOOR_X + 54 + (j % 3) * 13, GY - 6 - j * 9
            c.polygon([(fx - 6, fy + 8), (fx, fy - 10), (fx + 6, fy + 8)],
                      fill=_dim(FIRE, 0.75 - j * 0.1))
        c.text((FLOOR_X + 70, GY - 66), "UNQUENCHABLE", 11, _dim(FIRE, 0.95),
               "mm", bold=v == 17)

    # 3:19-20 — Herod added this above all: he shut John up in prison. The
    # bars close over the empty river, because there was never a man drawn
    # in it to shut up.
    if v >= 19:
        col = RED if v == 20 else _dim(GRAY, 0.85)
        if v >= 20:
            c.rect(VOICE_X - 44, GY - 96, 88, 92, fill=_dim(BG, 0.85),
                   stroke=col, width=2.2)
            for j in range(5):
                bx = VOICE_X - 32 + j * 16
                c.line((bx, GY - 96), (bx, GY - 4), col, 2)
            c.text((VOICE_X, GY + 46), "SHUT UP IN PRISON", 11.5,
                   HL if v == 20 else _dim(TEXT_DIM, 0.95), "mm", bold=v == 20)
        else:
            c.text((VOICE_X, GY + 46), "HEROD REPROVED", 11.5,
                   _dim(RED, 0.95), "mm", bold=True)

    # 3:21-22 — the heaven opened, and the Spirit descended like a dove
    if v >= 21:
        for j, r in enumerate((34, 62, 92)):
            c.ellipse(TRUNK_X, SKY_Y + 58, r * 1.5, r * 0.5,
                      stroke=_dim(GOLD, 0.45 - j * 0.12), width=1.6)
    if v >= 22:
        _put_w(c, F.dove(descending=True), TRUNK_X + 30,
               GY - TREE_H - 40, 78, GOLD, flip=-1)
        # beside the dove, not above it: the "word of God came to John" line
        # from 3:2 is still on the sky at that height
        c.text((TRUNK_X + 96, GY - TREE_H - 34), "LIKE A DOVE", 12, HL, "lm",
               bold=True)
        c.text((W / 2, H - 26), "THOU ART MY BELOVED SON", 19, HL, "mm",
               bold=True)
    return c


def _arc_table(s0, s1, step=0.05):
    """[(s, cumulative arc length along the root from s0)]"""
    table, total, s = [(s0, 0.0)], 0.0, s0
    px, py = root_x(s0), s0 * SPACING
    while s < s1:
        s = min(s + step, s1)
        x, y = root_x(s), s * SPACING
        total += math.hypot(x - px, y - py)
        table.append((s, total))
        px, py = x, y
    return table


def _arc_at(table, s):
    for (sa, la), (sb, lb) in zip(table, table[1:]):
        if s <= sb:
            f = 0.0 if sb == sa else (s - sa) / (sb - sa)
            return la + (lb - la) * f
    return table[-1][1]


def render_verse_svg(verse, slots, ranges):
    n = len(slots)
    start, end = ranges[verse]
    prev = max(start - 1, 0)
    tips = tip_track(verse, prev, end)
    tip1 = tips[-1]

    def ys(s):                      # root-space px -> screen y, at rest
        return CY + s - tip1

    c = SvgCanvas(W, H, bg=BG)

    # ---- the root world: everything root-fixed, drawn once, then dollied ----
    root = SvgLayer()
    for top, bot, tone in strata_bands(slots):
        y0 = ys(top)
        y1 = ys(bot) if bot is not None else ys((n - 1) * SPACING) + 900
        root.rectangle([0 - 40, y0, W + 40, y1], fill=tone)
        if bot is not None:
            root.line([(0 - 40, y1), (W + 40, y1)], fill=STRATA_LINE, width=2)

    # ground level and the tree whose root this is — the fractal segments
    # are grouped into one path per depth so each level keeps its taper
    gy = ys(SURFACE)
    xt = root_x(SURFACE / SPACING)      # trunk grows where the root emerges
    root.line([(0 - 40, gy), (W + 40, gy)], fill=SAND, width=3)
    for tx in range(60, W, 90):
        if abs(tx - xt) > 60:
            root.line([(tx, gy - 5), (tx + 6, gy - 12)], fill=SAND_DIM,
                      width=2)
    tree = ""                       # drawn from the vocabulary, onto `root`
    draw_tree_on(root, xt, gy, TREE_H)

    # the soil gives way to light around "of God"
    ggx, ggy = root_x(n - 1), ys((n - 1) * SPACING)
    for r, a in ((130, 16), (104, 11), (80, 13), (58, 19), (40, 25),
                 (26, 31)):
        root.ellipse([ggx - r, ggy - r, ggx + r, ggy + r], fill=HL + (a,))

    # the root line: dim ahead, plain behind
    s_end = n - 1
    whole = root_taper(SURFACE / SPACING, s_end, ys, s_end)
    if whole:
        root.polygon(whole, fill=_mix(BG, ROOT_FILL, 0.55),
                     outline=SAND_DIM, width=2)
    behind = root_taper(SURFACE / SPACING, max(prev, SURFACE / SPACING + 0.01),
                        ys, s_end)
    if behind:
        root.polygon(behind, fill=_mix(BG, ROOT_FILL, 0.72), outline=SAND,
                     width=2)

    for i, (name, _v) in enumerate(slots):
        y = ys(i * SPACING)
        x = root_x(i)
        era = era_of(name, i)
        cur = start <= i < end
        read = i < start
        side = 1 if math.cos(i * ROOT_FREQ) > 0 else -1
        # The offshoots taper too. A 2px line off a tapered trunk reads as a
        # wire soldered to a root; a side root leaves the parent at a
        # fraction of the parent's own thickness and thins to nothing, which
        # is the same rule the taproot itself follows.
        pw = root_width(i, n - 1)
        root.polygon(
            F.taper([(x, y), (x + side * 17, y + 9), (x + side * 36, y + 20)],
                    [pw * 0.52, pw * 0.30, pw * 0.12], round_end=False),
            fill=_mix(BG, ROOT_FILL, 0.46), outline=SAND_DIM, width=1)
        r = 8 if era else 5
        root.ellipse([x - r, y - r, x + r, y + r], fill=BG,
                     outline=SAND if (read or cur) else SAND_DIM, width=2)
        fill = HL if cur else TEXT if read else TEXT_DIM
        tx = x - side * 20
        anchor = "rm" if side > 0 else "lm"
        root.text((tx, y), name, font=F_ROOT_B if era else F_ROOT, fill=fill,
                  anchor=anchor)
        if era:
            root.text((tx, y + 20), era, font=F_ERA, fill=TEXT_DIM,
                      anchor=anchor)

    # the bright "just travelled" sweep: a draw-on path inside the group,
    # eased with the same trajectory as the dolly so its tip stays centred
    sweep = ""
    if tip1 > prev * SPACING:
        pts = root_pts(prev, (end - 1), ys, step=0.1)
        d_attr = "M " + " L ".join(f"{_fmt(x)} {_fmt(y)}" for x, y in pts)
        table = _arc_table(prev, end - 1)
        L = table[-1][1]
        offs = [max(0.0, L - _arc_at(table, max(prev, t / SPACING)))
                for t in tips]
        sweep = (f'<path d="{d_attr}" fill="none" '
                 f'{_stroke_attrs(HL + (242,), 5)} '
                 f'stroke-dasharray="{_fmt(L)}" '
                 f'stroke-dashoffset="{_fmt(offs[0])}">'
                 + _anim_seq("stroke-dashoffset", offs) + "</path>")

    dys = [tip1 - t for t in tips]
    trans_vals = ";".join(f"0 {_fmt(dy)}" for dy in dys)
    grp = (f'<g><animateTransform attributeName="transform" '
           f'attributeType="XML" type="translate" values="{trans_vals}" '
           f'keyTimes="{_keytimes()}" dur="{DUR}" begin="0s" fill="freeze" '
           f'calcMode="linear"/>'
           + "".join(root.elements()) + tree + sweep + "</g>")
    c.raw([grp])

    # ---- screen-fixed overlays on top ----
    # the traveler: a ring at the centre of the view, riding the root's
    # side-to-side wander (clamped to the trunk base while v23 is above
    # ground)
    rxs = [root_x(max(SURFACE / SPACING, t / SPACING)) for t in tips]
    c.raw([f'<circle cx="{_fmt(rxs[0])}" cy="{CY}" r="10" fill="none" '
           f'stroke="{_rgb(HL)}" stroke-width="3">'
           + _anim_seq("cx", rxs) + "</circle>"])

    # title/footer strips so the root world never slides through the chrome
    c.rect(0, 0, W, TOP_STRIP, fill=BG)
    c.rect(0, BOT_STRIP, W, H - BOT_STRIP, fill=BG)
    c.text((28, 20), "From Jesus down to the root — Luke 3", 24, TEXT, "la",
           bold=True)

    # ---- the depth gauge: the whole root at a glance ----
    span = (n - 1) * SPACING

    def gy_(s):
        return GA_Y0 + (GA_Y1 - GA_Y0) * max(0.0, min(1.0, s / span))

    c.line((GA_X, GA_Y0), (GA_X, GA_Y1), SAND_DIM, 2)
    gys = [gy_(t) for t in tips]
    c.raw([f'<line x1="{GA_X}" y1="{GA_Y0}" x2="{GA_X}" '
           f'y2="{_fmt(gys[0])}" {_stroke_attrs(SAND, 2, "butt")}>'
           + _anim_seq("y2", gys) + "</line>"])
    for i, (name, _v) in enumerate(slots):
        if not era_of(name, i):
            continue
        y = gy_(i * SPACING)
        c.line((GA_X - 4, y), (GA_X + 4, y), SAND, 2)
        dy = -6 if name == "Adam" else 8 if name == "God" else 0
        c.text((GA_X - 10, y + dy), name, 13, TEXT_DIM, "rm", italic=True)
    c.raw([f'<circle cx="{GA_X}" cy="{_fmt(gys[0])}" r="4" '
           f'fill="{_rgb(HL)}">' + _anim_seq("cy", gys) + "</circle>"])

    if end >= n:
        counter = f"all {n - 1} generations — back to the beginning"
    else:
        counter = f"generation {end - 1} of {n - 1}"
    c.text((W - 28, H - 26), counter, 14, TEXT, "ra", italic=True)
    c.text((28, H - 26),
           "Luke traces the line backward — from Jesus to Adam, "
           "“the son of God”", 14, TEXT_DIM, "la", italic=True)
    return c


def render_chapter(line, suffix):
    slots, ranges = build_grid(line)
    total = 0
    # 3:1-22 above ground, 3:23-38 down the root — one chapter, one plant
    for verse in range(1, 23):
        c = render_above_svg(verse)
        out = out_path("Luke", 3, f"Luke_3_{verse}{suffix}.svg")
        c.save(out)
        total += os.path.getsize(out)
    for verse in sorted(ranges):
        c = render_verse_svg(verse, slots, ranges)
        out = out_path("Luke", 3, f"Luke_3_{verse}{suffix}.svg")
        c.save(out)
        total += os.path.getsize(out)
    return len(ranges) + 22, total


def main():
    codes = [code for code, *_ in TRANSLATIONS]
    resolved = {}
    for code in codes:
        try:
            resolved[code] = extract_line(code)
        except (ValueError, PassageError) as e:
            print(f"{code}: extraction failed ({e}) — will use generic")
            resolved[code] = None
        time.sleep(0.2)

    generic = resolved["WEB"]
    if generic is None:
        raise SystemExit("WEB extraction failed; cannot build generic set")
    grand_files, grand_bytes = render_chapter(generic, "")
    print(f"Luke 3 generic: {grand_files} files")
    for code in codes:
        if code == "WEB" or resolved[code] is None:
            continue
        if resolved[code] == generic:
            print(f"  {code}: matches generic — skipped")
            continue
        n_files, n_bytes = render_chapter(resolved[code], f".{code}")
        grand_files += n_files
        grand_bytes += n_bytes
        print(f"  {code}: {n_files} translation-specific files")
    print(f"TOTAL: {grand_files} SVG files, {grand_bytes/1e3:.0f} KB")


if __name__ == "__main__":
    main()
