"""The 1 Chronicles 1-9 genealogies, read against the whole-canon tree.

The old per-verse renderer (v2, since deleted; its output is archived in
config.ARCHIVE_DIR, backups/1_Chronicles_svg_v2_camera) laid each chapter
out as its own world of side-by-side scenes. That reads well chapter by
chapter and hides the thing the genealogies are actually for: it is ONE
descent, and chapter 4 re-roots on a Judah the reader already met in
chapter 2. This world is the welded tree from `chronicles_tree.py` instead
— laid out once, name-only — and every verse of all nine chapters is a
camera move over that single map.

The tree is laid out in REGIONS (`layout_regions`): Adam to Israel's sons
is one fan in strict generation rows, and each son's descendants (and
Esau's, as EDOM) stand under it in a faint titled panel, reached by a
routed line from the son's box. A wife stands beside her husband on a
marriage bar, and a house that gathers people is a small italic label on
the line rather than a box.

Four consequences worth knowing:

* THE TREE ACCUMULATES. `read` is global across chapters 1-9 in reading
  order, not per chapter. Judah lights up at 2:1 and is still lit when 4:1
  comes back to him, so by chapter 9 the whole thing is standing.
* WHAT IS STILL TO COME IS A BLOCK. A branch the reading has not reached
  yet stands as one faint block under its first person, and a tribe's
  panel nobody has been read in yet as its titled panel alone
  (`svg_silhouettes`); when the reading gets there, the block gives way to
  its boxes.
* NEW NAMES GROW IN. A name first read in this verse arrives: its connector
  draws itself from the parent while its box, already standing faint,
  brightens. That is what makes a family spread across a wide row read as
  one family — you watch the branch reach each sibling.
* BREAKS PULL BACK. When the next name is a long way from the last, the
  camera's van Wijk & Nuij arc lifts out and comes back in, so the jump is
  seen as a move across one tree rather than a cut to somewhere else. Every
  box the flight shows at a readable size carries its name.

Verse matching is NOT redone here. `generate_1chronicles.assign()` is still
the authority; the bridge is the `src` stamp that `chronicles_tree` puts on
every node it lifts out of the scene data — (chapter, scene title, flatten
index) — which is exactly the key `assign()` returns. A row the tree retells
instead of lifting (4:1, 6:33-38, 9:20) reaches its node through the tree's
binding table, `Tree.bind`, under the same key.

Rendered by generate_1chronicles_tree_svg.py.
"""

import math
import os
import struct
from xml.sax.saxutils import escape

import chronicles_tree as CT
import layout_regions
import svg_family_lines as FL
import svg_silhouettes as SIL
from chronicles_tree import walk
from config import WEB_AUDIO_DIR
from generate_1chronicles import (CHAPTERS, assign, flatten,
                                  web_verses)
from generate_ot_family_tree_svg import (BG, FAINT, HL, HOUSE, PANEL,
                                         PRIESTLY, ROYAL, SAND, SAND_DIM,
                                         TEXT, TEXT_DIM, FEMALE, ICON_H, MIN_W,
                                         NAME_H, PAD_X, PAD_Y, _crown, _icon,
                                         accent, arrange, arrange_spine, dim,
                                         draw_chip, place, place_spine)
from generate_tabernacle import W, H, F_TITLE, font
from svg_surface import SvgCanvas, SvgLayer, _fmt, _rgb

# -- viewport ---------------------------------------------------------------

HUD_H = 46
VIEW_TOP, VIEW_BOT = HUD_H + 14, H - 20
S_MIN, S_MAX = 0.05, 1.25
OPEN_S_MIN = 0.11
FOCUS_MIN_W, FOCUS_MIN_H = 460, 250
READABLE = 0.52             # below this a 15px name is not worth framing for
MAX_NODES = 260             # per-verse ceiling, so one wide shot cannot
                            # balloon the file — it bounds names too, since
                            # only a drawn box carries one
DWELL_SHARE = 0.45          # of that ceiling, reserved for the frame the
                            # verse OPENS on before the rest is spent
TEXT_MIN_SCALE = 0.34       # below this a 15px name is under 5px: quiet
                            # breathe-outs stop here, and the cull pays for
                            # what the flight shows at this scale first
NAME_MIN_SCALE = 0.12       # a box on screen at this scale or closer at any
                            # moment carries its name; below it a box is a
                            # speck under 10px
SEEN_MARGIN = 4.0           # screen px of slack round the visible area, for
                            # antialiasing and the 2-dp translate rounding
STROKE_HOLD_SCALE = 0.68    # below this camera scale box edges and connectors
STROKE_MIN_PX = 1.0         # stop thinning: each keeps its width at this
                            # scale, never under 1px, so a wide pull-back
                            # still shows the shape of the tree
RHO = 1.35                  # van Wijk & Nuij's zoom/pan trade-off: higher
                            # lifts further on long pans, lower flies flatter
CAM_FPS = 30                # keyframes per second when baking the arc
QUIET_STEP = 1.75           # how much wider each verse with no name goes
QUIET_MAX = 9.0             # and how far out that is allowed to run

EASE = "0.42 0 0.58 1"
DUR_MIN, DUR_MAX = 3.4, 6.4  # seconds of camera move
GROW_DUR = "1.6s"            # fallback when a caller has no per-verse pace
AUDIO_SLACK = 0.35           # the animation lands this long before the MP3
GROW_TAIL = 1.06             # arrivals finish at this multiple of the move
                             # (grow begins at 0.60 and runs 0.46 — see
                             # _grow_timing; keep the three in agreement)

AUDIO_DIR = WEB_AUDIO_DIR      # the narration MP3s that pace each verse

# -- which layout the world is laid out in ----------------------------------
#
# CHRONICLES USES "regions" (layout_regions). It keeps the tree one tree
# with honest rows: Adam to Israel's sons is one fan in strict generation
# rows, so 2:1-2 see the twelve sons together on one row, and each son's
# descendants stand in a titled panel under the fan, reached by a routed
# line. Inside a panel a row is a generation too, a wife stands beside her
# husband and a house is a label on the line. Its place() returns a Plan
# (labels, routes, panels), kept as `World.plan`, which the frames draw. The
# front of the book's fans rest far tighter than under either tree layout
# below (1:17, 2:1 and 2:2 at reading size). A verse whose head stands in
# the fan far above his panel rests on the panel, with the panel's title
# standing in for him (World.focus_box).
#
# The two tree layouts stay selectable for comparison — `--centred` or
# `--spine` on the driver, or `World(layout=...)`:
#
# "centred" is the wall chart's rule — a parent over the whole span of its
# descendants — and was the live layout before regions. Two brothers each
# carrying a house of hundreds cannot both stand near their father in it,
# and a wrapped family stands later brothers beside an earlier brother's
# grandsons, so boxes level with each other were not one generation.
#
# "spine" puts the heir directly under its parent, so a line of descent is a
# straight vertical column. It was tried here and rejected (2026-08-21):
# these nine chapters are mostly FANS — "the sons of X" — and a fan is
# tightest when the parent is centred over its children, because the spine
# cascades every sibling to one side of the heir. The front of the book's
# wide rests roughly halved in scale: 1:4 (the sons of Noah) 0.101 -> 0.053,
# 1:28 (Abraham, Isaac and Ishmael) 0.134 -> 0.066, 1:34 (Isaac, Jacob and
# Esau) 0.137 -> 0.073.
#
# Matthew calls arrange_spine directly and is unaffected by this setting.
LAYOUT = "regions"
LAYOUTS = {"spine": (arrange_spine, place_spine),
           "centred": (arrange, place),
           "regions": (layout_regions.arrange, layout_regions.place)}


def _mp3_seconds(path):
    """Duration of one narration MP3, without an audio library.

    The WEB verse files are edge-tts output: MPEG-2 Layer III, constant
    bitrate, no tags — so size*8/bitrate is exact. The Xing/Info branch is
    there in case a re-render ever produces VBR files instead.
    """
    try:
        with open(path, "rb") as f:
            d = f.read()
    except OSError:
        return None
    i = 0
    if d[:3] == b"ID3":
        i = 10 + (((d[6] & 0x7F) << 21) | ((d[7] & 0x7F) << 14) |
                  ((d[8] & 0x7F) << 7) | (d[9] & 0x7F))
    while i < len(d) - 4 and not (d[i] == 0xFF and (d[i + 1] & 0xE0) == 0xE0):
        i += 1
    if i >= len(d) - 4:
        return None
    b1, b2, b3 = d[i + 1], d[i + 2], d[i + 3]
    ver, layer = (b1 >> 3) & 3, (b1 >> 1) & 3
    if layer != 1:                                  # Layer III only
        return None
    BR = {3: [0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256,
              320]}
    br_tbl = BR.get(ver, [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112,
                          128, 144, 160])
    SR = {3: [44100, 48000, 32000], 2: [22050, 24000, 16000],
          0: [11025, 12000, 8000]}
    br = br_tbl[(b2 >> 4) & 0xF] * 1000
    sr = SR.get(ver, SR[2])[(b2 >> 2) & 3]
    if not br or not sr:
        return None
    mono = ((b3 >> 6) & 3) == 3
    side = ((17 if mono else 32) if ver == 3 else (9 if mono else 17))
    tag_at = i + 4 + side
    if d[tag_at:tag_at + 4] in (b"Xing", b"Info"):
        flags = struct.unpack(">I", d[tag_at + 4:tag_at + 8])[0]
        if flags & 1:
            frames = struct.unpack(">I", d[tag_at + 8:tag_at + 12])[0]
            return frames * (1152 if ver == 3 else 576) / sr
    return (len(d) - i) * 8 / br


def _pace(cam0, cam1, apex_scale):
    """How long this verse's move should take.

    A short nudge between two brothers and a pull back across four tribes
    are not the same event, and giving them the same 2.6 s made every long
    move feel thrown. Duration grows with how far the camera travels and
    with how many octaves the zoom spans — measured to the arc's own apex,
    since the flight goes as wide as van Wijk & Nuij says, not as wide as a
    hand-placed overview used to.
    """
    zoom = max(cam1[0] / cam0[0], cam0[0] / cam1[0],
               cam0[0] / apex_scale, cam1[0] / apex_scale)
    travel = math.hypot(cam1[1] - cam0[1], cam1[2] - cam0[2])         * max(cam0[0], cam1[0])
    d = DUR_MIN + 0.85 * math.log2(max(zoom, 1.0)) + travel / 950.0
    return round(min(DUR_MAX, d), 2)


RING_MIN = 16.0             # screen px a ring keeps once its node is tiny
HOLE_MIN = 26.0             # likewise for a veil hole
VEIL_ALPHA = 0.62


def _cam_n(dur):
    """How many intervals a zooming flight is baked into. _camera_group and
    _cam_schedule both count with this, which keeps them in lockstep."""
    return max(6, int(round(dur * CAM_FPS)))


def _fmt_s(v):
    return ("%.6f" % v).rstrip("0").rstrip(".")


def _cam_schedule(cam0, cam1, arc_at, dur):
    """The scale-over-time the camera will fly — None for a pure pan."""
    if abs(cam1[0] - cam0[0]) <= 1e-9:
        return None
    n = _cam_n(dur)
    return [arc_at(_smooth(i / n))[0] for i in range(n + 1)]


def _ride_r(w, h, s, floor):
    """Highlight radius in world units at camera scale s: hugs a w x h box
    while the camera is close, floors at a constant screen size once the
    box is small."""
    hug = math.hypot(w, h) / 2 + 10
    return max(floor, hug * s) / s


def _spot(nd, s):
    """-> (cx, cy, w, h) of what a highlight rides at camera scale s: a
    node's box, or a panel title standing in for its head, which grows from
    its corner as the camera pulls out."""
    if isinstance(nd, PanelTitle):
        x0, y0, x1, y1 = nd.box_at(s)
        return (x0 + x1) / 2, (y0 + y1) / 2, x1 - x0, y1 - y0
    return nd.x + nd.w / 2, nd.y + nd.h / 2, nd.w, nd.h


def _anim(attr, vals, dur):
    return (f'<animate attributeName="{attr}" values='
            f'"{";".join("%.2f" % v for v in vals)}" dur="{dur}s" '
            f'begin="0s" fill="freeze"/>')


CONNECTOR_W = 1.5           # a static connector's stroke, in world units
FINE_W = 1.0                # the second strand of a wife's line, and beads
TRACE_W = 1.6               # an arrival's line as it draws itself
TRACE_FINE_W = 1.1          # and the second strand of a wife's drop
LINE_ALPHA = {"lit": 0.95, "read": 0.8, "ahead": 0.2}

# -- the regions layout's panels, titles and labels --------------------------
#
# A panel is a faint rounded rectangle drawn in WORLD space, inside the
# camera group, as a plain rect: no mask, filter or clip, because one whose
# region is world-sized is rasterised at that size every frame (the veil
# once asked an iPad for 512 megapixels). Its edge sits in a stroke-floor
# group like the boxes'.
PANEL_RX = 18
PANEL_FILL_ALPHA = 0.55
PANEL_EDGE = (52, 50, 64)
PANEL_EDGE_ALPHA = 0.9
PANEL_EDGE_W = 1.2
PANEL_BLEND = tuple(int(round(BG[i] + (PANEL[i] - BG[i]) * PANEL_FILL_ALPHA))
                    for i in range(3))      # the panel's colour, seen flat
TITLE_PX = 26               # a title's size in world units, where its room
TITLE_MIN_PX = 11           # (the corner the entering lines leave) allows
TITLE_ALPHA = 0.62          # sand at this alpha over the panel, painted
TITLE_INK = tuple(int(round(PANEL_BLEND[i] + (SAND[i] - PANEL_BLEND[i])
                            * TITLE_ALPHA)) for i in range(3))   # opaque
TITLE_HOLD_PX = 16          # screen px a full-size tribe title holds as the
TITLE_HOLD_MIN = 11         # camera pulls out; a smaller one holds less
TITLE_HALO = 0.22           # a growing title's halo in the panel's colour,
                            # as a fraction of its size
F_PANEL = font(TITLE_PX, bold=True)
LABEL_PX = layout_regions.LABEL_PX      # a house label's italic text
# A branch nobody has read yet stands as one quiet block (svg_silhouettes):
# a plain rounded rect in world space like the panels, no mask, filter or
# clip, its edge in a stroke-floor group. When the reading reaches it, it
# fades out while the boxes it held fade in, from OPEN_AT of the move over
# OPEN_LEN, so the boxes stand before the arriving names brighten (0.60).
BLOCK_RX = 10
BLOCK_FILL = dim(SAND_DIM, 0.07)
BLOCK_EDGE = dim(SAND_DIM, 0.40)
BLOCK_EDGE_W = 1.0
OPEN_AT, OPEN_LEN = 0.30, 0.30
FLOOR_MARGIN = 1.25         # every focus box must fit at this multiple of
                            # S_MIN, so no ARRIVING box rests off screen
                            # (a re-named person outside the focus box can:
                            # a tribe head left in the fan is shown by his
                            # panel's title only where it can come into
                            # the frame, see World.focus_box)
IPAD_BOX_RECTS = 1050       # <rect> and <text> elements in a whole file:
IPAD_NAMES = 268            # about the most proven smooth on the owner's
                            # iPad (the centred files peaked at 1,052 rects
                            # in 2:2 and 268 texts in 2:9 and 6:1). The
                            # node cap keeps the names within it by
                            # construction (render); the rects are counted
                            # in each file as written


def _unwidth(el, width):
    """Drop an element's own stroke-width so it inherits its group's."""
    attr = ' stroke-width="%s"' % _fmt(width)
    assert attr in el, el
    return el.replace(attr, "", 1)


def _stroke_group(els, width, scales, s_end, dur):
    """Wrap world strokes of one nominal `width` in a group whose
    stroke-width they inherit, held at a screen-pixel floor as the camera
    pulls out — on the camera's own schedule, like the rings. At 0.1 scale a
    1.5-unit line is 0.15px and the tree simply dissolves; with the floor
    its outline stays.

    The width depends only on the scale, so a verse ends at exactly the
    width the next one opens with."""
    if not els:
        return ""
    px = max(STROKE_MIN_PX, width * STROKE_HOLD_SCALE)
    vals = [max(width, px / s) for s in (scales or [s_end])]
    anim = (_anim("stroke-width", vals, dur)
            if any(round(v, 2) != round(vals[0], 2) for v in vals) else "")
    return (f'<g stroke-width="{vals[0]:.2f}">{anim}' + "".join(els)
            + "</g>")


def _title_w(t, px):
    """A panel title's width at px world units, letter-spaced 1."""
    return F_PANEL.getlength(t) * px / TITLE_PX + len(t)


class PanelTitle:
    """How one panel's title is set.

    TITLE_PX on one line where the corner the entering lines leave
    (`Panel.title_room`) allows it, smaller in a narrow panel, and on two
    lines under 14 px when the title is a long house name. It hangs from
    the panel's top edge in that corner, in the band above the panel's
    first row.

    A tribe's title (its head is a person: EDOM, REUBEN ... ASHER) GROWS as
    the camera pulls out, holding about TITLE_HOLD_PX on screen, up to what
    the panel can hold, so a wide shot can still tell the panels apart. It
    reaches the panel's first row only below scale ~0.25, where those names
    are specks; it is painted opaque (sand as it looks at TITLE_ALPHA on
    the panel) and haloed in the panel's colour, so the faint and read
    specks it covers do not cut it up. The verse's lit and arriving boxes
    are drawn over it. A house's title (the kings of Israel, the first to live
    again in their cities) stays at its own size, like the house labels:
    its words are never the largest thing on a wide shot. The size depends
    only on the camera's scale, so a verse ends at exactly the size the
    next one opens with.

    A title can STAND IN for its head (World.focus_box): when a verse rests
    on the panel and leaves the head's box in the fan out of the frame, the
    title is drawn in the lit colour, and on a wide card rest it gets a
    ring, so the name the narrator reads is on screen."""

    def __init__(self, p):
        x0, y0, x1, y1 = p.rect
        t, room = p.title, p.title_room

        def fit(lines):
            w = max(_title_w(L, TITLE_PX) - len(L) for L in lines)
            n = max(len(L) for L in lines)
            return min(TITLE_PX, TITLE_PX * (room - n - 4) / max(w, 1.0))
        px = fit([t])
        lines = [t]
        if px < 14.0 and " " in t:
            words = t.split()
            best = max(((fit([" ".join(words[:i]), " ".join(words[i:])]),
                         [" ".join(words[:i]), " ".join(words[i:])])
                        for i in range(1, len(words))), key=lambda b: b[0])
            px, lines = min(best[0], 15.0), best[1]
        self.px = max(TITLE_MIN_PX, px)
        self.lines = lines
        self.anchor = "start" if p.title_side == "left" else "end"
        self.x = x0 + 20 if p.title_side == "left" else x1 - 20
        self.y = y0 + 12
        self.grows = not layout_regions.is_house(p.head)
        if self.grows:
            self.px_max = max(self.px, min(
                (x1 - x0 - 40 - len(t)) * TITLE_PX / F_PANEL.getlength(t),
                (y1 - y0 - 24) * 0.5))
            self.hold = max(TITLE_HOLD_MIN, TITLE_HOLD_PX * self.px / TITLE_PX)
        else:
            self.px_max = self.px
        self.box = self._box(self.px_max)       # as large as it ever grows

    def _box(self, px):
        w = max(_title_w(L, px) for L in self.lines)
        h = px * (1.2 + 1.15 * (len(self.lines) - 1))
        bx0 = self.x if self.anchor == "start" else self.x - w
        return (bx0, self.y, bx0 + w, self.y + h)

    def size(self, s):
        if not self.grows:
            return self.px
        return min(self.px_max, max(self.px, self.hold / s))

    def box_at(self, s):
        """Where the title stands at camera scale s: it grows from its
        anchor corner as the camera pulls out."""
        return self._box(self.size(s))

    def els(self, scales, s_end, dur, lit=False):
        vals = [self.size(s) for s in (scales or [s_end])]
        moves = any(round(v, 2) != round(vals[0], 2) for v in vals)
        anim = _anim("font-size", vals, dur) if moves else ""
        halo = ""
        if self.grows:
            halo = (f' stroke="{_rgb(PANEL_BLEND)}" stroke-width='
                    f'"{TITLE_HALO * vals[0]:.2f}" stroke-linejoin="round" '
                    f'paint-order="stroke"')
            if moves:
                anim += _anim("stroke-width", [TITLE_HALO * v for v in vals],
                              dur)
        out = []
        for i, line in enumerate(self.lines):
            y = self.y + i * self.px * 1.15
            out.append(
                f'<text x="{_fmt(self.x)}" y="{_fmt(y)}" '
                f'font-size="{vals[0]:.2f}" text-anchor="{self.anchor}" '
                f'dominant-baseline="text-before-edge" '
                f'fill="{_rgb(HL if lit else TITLE_INK)}"{halo} '
                f'font-weight="bold" letter-spacing="1">'
                f'{escape(line)}{anim}</text>')
        return out


def _ride_els(named, scales, s_end, dur, uid, tracks,
              veil_alpha=VEIL_ALPHA):
    """Wide-rest highlights that RIDE their nodes (wide lab E).

    Returns (world_els, screen_els). Rings go in the camera group and are
    plain strokes. The VEIL cannot: a mask is rasterised into a buffer the
    size of its region in DEVICE pixels, and a region covering the whole
    world, sitting inside a group the camera scales up to 1.25, asked for a
    512-megapixel buffer at the start of every wide flight — imperceptible
    on a desktop GPU, and the reason the iPhone and iPad crawled.

    So the veil is drawn in SCREEN space at exactly viewport size (0.54 MP,
    a thousandfold less), and only its mask HOLES carry a second copy of the
    camera transform so they still ride their nodes in world coordinates.
    Same values, same keyTimes, same duration: SMIL drives both copies in
    lockstep.

    `named` may hold a PanelTitle standing in for its head: its ring and
    hole follow the title's box as it grows, so they move as well as size.
    """
    hlrgb = "rgb(%d,%d,%d)" % HL[:3]
    bgrgb = "rgb(%d,%d,%d)" % BG[:3]
    holes, rings = [], []
    for nd in named:
        if scales is None:
            cx, cy, bw, bh = _spot(nd, s_end)
            hr = _ride_r(bw, bh, s_end, HOLE_MIN) + 8
            holes.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" '
                         f'r="{hr:.1f}" fill="black"/>')
            rr = _ride_r(bw, bh, s_end, RING_MIN)
            rings.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" '
                         f'r="{rr:.1f}" fill="none" stroke="{hlrgb}" '
                         f'stroke-opacity="0.85" '
                         f'stroke-width="{2.2 / s_end:.2f}"/>')
        else:
            spots = [_spot(nd, sc) for sc in scales]
            cx, cy = spots[0][0], spots[0][1]
            move = ""
            for i, attr in ((0, "cx"), (1, "cy")):
                vals = [sp[i] for sp in spots]
                if any(round(v, 2) != round(vals[0], 2) for v in vals):
                    move += _anim(attr, vals, dur)
            hv = [_ride_r(sp[2], sp[3], sc, HOLE_MIN) + 8
                  for sp, sc in zip(spots, scales)]
            holes.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" '
                         f'r="{hv[0]:.1f}" fill="black">'
                         + _anim("r", hv, dur) + move + '</circle>')
            rv = [_ride_r(sp[2], sp[3], sc, RING_MIN)
                  for sp, sc in zip(spots, scales)]
            wv = [2.2 / sc for sc in scales]
            rings.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" '
                         f'r="{rv[0]:.1f}" fill="none" stroke="{hlrgb}" '
                         f'stroke-opacity="0.85" '
                         f'stroke-width="{wv[0]:.2f}">'
                         + _anim("r", rv, dur)
                         + _anim("stroke-width", wv, dur) + move
                         + '</circle>')
    vy, vh = HUD_H, H - HUD_H
    mask = (f'<defs><mask id="{uid}" maskUnits="userSpaceOnUse" '
            f'x="0" y="{vy}" width="{W}" height="{vh}">'
            f'<rect x="0" y="{vy}" width="{W}" height="{vh}" fill="white"/>'
            + _cam_wrap(tracks, dur, holes) + '</mask></defs>')
    veil = (f'<rect x="0" y="{vy}" width="{W}" height="{vh}" '
            f'fill="{bgrgb}" fill-opacity="{veil_alpha}" '
            f'mask="url(#{uid})"/>')
    screen = [_fade_group([mask + veil], "%.2fs" % (dur * 0.45),
                          "%.2fs" % (dur * 0.30))]
    world = [_fade_group(rings, "0s", "0.4s")]
    return world, screen


def _grow_timing(dur):
    """A name arrives as the camera settles, and takes its time doing it."""
    return f"{dur * 0.46:.2f}s", f"{dur * 0.60:.2f}s"


def _smooth(t):
    return t * t * (3 - 2 * t)


def _vw(cam0, cam1):
    """van Wijk & Nuij's optimal pan-zoom path, chosen by the user over the
    three-leg decomposition and the plain blended arc (camera lab,
    2026-08-14).

    Pan and zoom are fused into one hyperbolic arc along which PERCEIVED
    speed is constant — the camera crosses ground quickly only while it is
    wide, so there is no separate pan phase to be jarringly fast, and long
    moves lift off the ground on their own without a hand-placed overview
    keyframe.

    Returns (at, apex_scale): `at(p)` is the camera at path fraction
    p in [0, 1]; `apex_scale` is the widest scale the arc reaches, which
    the CULLER and the PACER need — a node visible at the arc's top must be
    in the skeleton or the apex shows blank space, and the duration must
    know how far out the flight really goes.
    """
    w0, w1 = W / cam0[0], W / cam1[0]
    dx, dy = cam1[1] - cam0[1], cam1[2] - cam0[2]
    u1 = math.hypot(dx, dy)
    if u1 < 1e-6:                       # zoom in place (quiet breathe-outs)
        def at(p):
            wv = w0 * (w1 / w0) ** p if w1 != w0 else w0
            return (W / wv, cam0[1], cam0[2])
        return at, min(cam0[0], cam1[0])
    ux, uy = dx / u1, dy / u1
    r2 = RHO * RHO
    b0 = (w1 * w1 - w0 * w0 + r2 * r2 * u1 * u1) / (2 * w0 * r2 * u1)
    b1 = (w1 * w1 - w0 * w0 - r2 * r2 * u1 * u1) / (2 * w1 * r2 * u1)
    r0 = math.log(-b0 + math.sqrt(b0 * b0 + 1))
    r1 = math.log(-b1 + math.sqrt(b1 * b1 + 1))
    S = (r1 - r0) / RHO
    ch0 = math.cosh(r0)
    w_apex = w0 * ch0 if r0 < 0 < r1 else max(w0, w1)

    def at(p):
        sp = S * p
        u = (w0 / r2) * ch0 * math.tanh(RHO * sp + r0) \
            - (w0 / r2) * math.sinh(r0)
        wv = w0 * ch0 / math.cosh(RHO * sp + r0)
        return (W / wv, cam0[1] + ux * u, cam0[2] + uy * u)
    return at, W / w_apex

# -- how much of the world each verse is allowed to carry -------------------
#
# The whole tree is far too much SVG to repeat 407 times. Each verse emits
# the boxes inside the frames it opens on, flies through and lands on, capped
# at MAX_NODES, and a box carries its name only if the viewer can see it at
# NAME_MIN_SCALE or closer at some moment of the flight (_flight_seen). A box
# the camera only ever passes far above stays bare, because at that size it
# is a speck and its name would be noise.

DETAIL_PAD = 1.35           # frame expansion the cull pays for at both ends
SKELETON_PAD = 1.15

F_NODE = font(15)
F_NODE_B = font(15, bold=True)


# ===========================================================================
# Geometry helpers (the camera math of the retired v2 renderer, restated for
# this viewport)
# ===========================================================================

def _union(a, b):
    return (min(a[0], b[0]), min(a[1], b[1]),
            max(a[2], b[2]), max(a[3], b[3]))


def _grow_min(box):
    x0, y0, x1, y1 = box
    if x1 - x0 < FOCUS_MIN_W:
        cx = (x0 + x1) / 2
        x0, x1 = cx - FOCUS_MIN_W / 2, cx + FOCUS_MIN_W / 2
    if y1 - y0 < FOCUS_MIN_H:
        cy = (y0 + y1) / 2
        y0, y1 = cy - FOCUS_MIN_H / 2, cy + FOCUS_MIN_H / 2
    return x0, y0, x1, y1


def _fit(box, pad=70):
    x0, y0, x1, y1 = box
    x0, y0, x1, y1 = x0 - pad, y0 - pad, x1 + pad, y1 + pad
    bw, bh = max(x1 - x0, 1), max(y1 - y0, 1)
    vw, vh = W, VIEW_BOT - VIEW_TOP
    s = min(S_MAX, max(S_MIN, min(vw / bw, vh / bh)))
    return s, (x0 + x1) / 2, (y0 + y1) / 2


def _cam_T(cam):
    s, wx, wy = cam
    return W / 2 - s * wx, (VIEW_TOP + VIEW_BOT) / 2 - s * wy


def _frame(cam, pad=1.0):
    """The world rectangle a camera sees, expanded by `pad`."""
    s, wx, wy = cam
    hw = W / s / 2 * pad
    hh = (VIEW_BOT - VIEW_TOP) / s / 2 * pad
    return wx - hw, wy - hh, wx + hw, wy + hh


def _hits(box, f):
    return not (box[2] < f[0] or box[0] > f[2]
                or box[3] < f[1] or box[1] > f[3])


def node_box(n):
    return n.x, n.y, n.x + n.w, n.y + n.h


def _flight(cam0, cam1, arc_at, dur):
    """The keyframes _camera_group writes -> (cams, keyTimes, pure_pan),
    each scale already rounded to the six places it is written with, so
    anything measured from these is measured on the flight the browser
    actually plays."""
    pure_pan = abs(cam1[0] - cam0[0]) <= 1e-9
    if pure_pan:
        cams, times = [cam0, cam1], [0.0, 1.0]
    else:
        n = _cam_n(dur)
        cams = [arc_at(_smooth(i / n)) for i in range(n + 1)]
        cams[0], cams[-1] = cam0, cam1
        times = [i / n for i in range(n + 1)]
    cams = [(float(_fmt_s(sc)), cx_, cy_) for sc, cx_, cy_ in cams]
    return cams, times, pure_pan


def _on_screen(cam, margin=SEEN_MARGIN):
    """The world rectangle the viewer actually sees at `cam`: the full width,
    and from under the HUD band to the bottom edge. `_frame` measures the
    framing area, VIEW_TOP..VIEW_BOT, which is a little smaller."""
    s = cam[0]
    tx, ty = _cam_T(cam)
    return ((-margin - tx) / s, (HUD_H - margin - ty) / s,
            (W + margin - tx) / s, (H + margin - ty) / s)


def _flight_seen(cam0, cam1, arc_at, dur):
    """Everything the flight shows, as [(world box, scale)] — one entry per
    keyframe interval: the box spanning the screens at its two ends, and the
    larger of their two scales. The last end is the frame the verse rests on.

    The box is exact, not a sample. SMIL interpolates translate and scale
    separately and linearly between keyframes, so each edge of the visible
    world, (k - T) / s, is monotone across an interval, and every frame
    between two keyframes lies inside the box spanning them. A pure pan is
    written as two keyframes and a spline that only re-times them, so its
    straight line is cut into as many steps as a zoom of that length gets.
    """
    cams, _times, pure_pan = _flight(cam0, cam1, arc_at, dur)
    if pure_pan:
        (s, x0, y0), (_s, x1, y1) = cams
        n = _cam_n(dur)
        cams = [(s, x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n)
                for i in range(n + 1)]
    return [(_union(_on_screen(a), _on_screen(b)), max(a[0], b[0]))
            for a, b in zip(cams, cams[1:])]


def _seen_scale(nodes, intervals, min_scale=NAME_MIN_SCALE):
    """node -> the largest scale it is on screen at, for the nodes the
    flight shows at `min_scale` or closer."""
    legible = sorted((iv for iv in intervals if iv[1] >= min_scale),
                     key=lambda iv: -iv[1])
    if not legible:
        return {}
    reach = legible[0][0]
    for box, _s in legible[1:]:
        reach = _union(reach, box)
    seen = {}
    for n in nodes:
        nb = node_box(n)
        if not _hits(nb, reach):
            continue
        for box, s in legible:
            if _hits(nb, box):
                seen[n] = s
                break
    return seen


# -- where a verse rests ------------------------------------------------------

TITLE_COST = 0.75           # a card rest takes in the panel title standing
                            # for its head only if it keeps this much of
                            # its scale (7:6's BENJAMIN stands at the far
                            # corner of its panel, and would cost 3/4)
NEAR = 0.01                 # a card keeps its frame unless leaving the fan
                            # out rests it at least this much closer


def _bbox(nodes):
    box = None
    for n in nodes:
        b = node_box(n)
        box = b if box is None else _union(box, b)
    return box


def _parts(core, lit, leave=()):
    """-> (wide, box): what a verse can frame. `box` is the core (the
    arrivals, or everyone named when nobody arrives); `wide` adds each core
    person's father and everyone else the verse names. A father in `leave`
    is not pulled in."""
    box = _bbox(core)
    wide = box
    for n in core:
        if n.parent is not None and n.parent not in leave:
            wide = _union(wide, node_box(n.parent))
    for n in lit:
        wide = _union(wide, node_box(n))
    return wide, box


def _ladder(wide, box):
    """The ordinary rest: the whole family if it reads, else the core if
    that reads, else a card resting wide on the whole family."""
    if _fit(_grow_min(wide), pad=70)[0] >= READABLE:
        return _grow_min(wide), "tight"
    if _fit(_grow_min(box), pad=70)[0] >= READABLE:
        return _grow_min(box), "tight"
    return _grow_min(wide), "card"


def _with_title(raw, tl, floor):
    """`raw` and the panel title `tl` framed together -> the focus box, or
    None if it would rest under `floor`. A tribe's title grows as the camera
    pulls out, so its box is taken at the scale the frame rests at."""
    s, b = S_MAX, None
    for _ in range(8):
        b = _grow_min(_union(raw, tl.box_at(s)))
        s2 = _fit(b, pad=70)[0]
        if abs(s2 - s) < 1e-6:
            break
        s = s2
    return b if s2 >= floor else None


def _in_shot(focus, rects):
    """Every rect wholly on screen at the rest `focus` gives."""
    x0, y0, x1, y1 = _on_screen(_fit(focus, pad=70), margin=0.0)
    return all(r[0] >= x0 and r[1] >= y0 and r[2] <= x1 and r[3] <= y1
               for r in rects)


# -- the cutaway card's size, which a card rest keeps its people clear of ----

CARD_BH = 27                # box height on the card
CARD_WG = 18                # husband to wife on the card
CARD_PAD = 16               # the card's plate round its boxes
CARD_GAP = 8                # screen px between a card rest's people and it


def _card_anc(a, b, k=3):
    """a is b's father, grandfather or great-grandfather."""
    q = b.parent
    while q is not None and k:
        if q is a:
            return True
        q, k = q.parent, k - 1
    return False


def _card_bw(n):
    """A box's width on the card."""
    fnt = F_NODE_B if n.kind in ("king", "priest") else F_NODE
    w_ = fnt.getlength(n.label) + 2 * PAD_X
    return w_ + (16 if n.kind == "king" else 0)


def card_layout(named, wives_beside, w_max):
    """How the cutaway card sets the people a verse names -> (star, head,
    wives, kids, rows, cw, ch_, hw): rows of (node, x offset) for a star,
    (node, x offset, joint) for a recital, and the card's content width,
    height and (a star's) head-row width. VerseFrame._card draws it; a card
    rest measures it to keep its people clear of it (_card_clear)."""
    anc, bw, BH = _card_anc, _card_bw, CARD_BH
    head, rest = named[0], named[1:]
    # The head's wives stand beside him on a short bar, as they do in the
    # tree, not in the row of his children; the children of one wife drop
    # from her.
    wives = ([n for n in rest if n.parent is head and
              layout_regions.is_wife(n)]
             if wives_beside else [])
    kids = [n for n in rest if n not in wives]
    star = (len(named) > 2 and kids and all(anc(head, n) for n in kids)
            and not any(anc(a, b) for a in kids for b in kids
                        if a is not b))
    rows, row, x = [], [], 0.0
    if star:
        for n in kids:
            step = bw(n) + (14 if row else 0)
            if row and x + step > w_max:
                rows.append(row)
                row, x, step = [], 0.0, bw(n)
            row.append((n, x + (14 if row else 0)))
            x += step
        if row:
            rows.append(row)
        row_ws = [r[-1][1] + bw(r[-1][0]) for r in rows]
        hw = bw(head) + sum(CARD_WG + bw(wv) for wv in wives)
        cw = max(max(row_ws), hw)
        ch_ = BH + 22 + len(rows) * BH + (len(rows) - 1) * 24
    else:
        for i2, n in enumerate(named):
            joint = None
            if row:
                joint = "line" if anc(named[i2 - 1], n) else "dot"
            gap = 22 if joint else 0
            step = bw(n) + gap
            if row and x + step > w_max:
                rows.append(row)
                row, x, joint, step = [], 0.0, None, bw(n)
            row.append((n, x + gap, joint))
            x += step
        if row:
            rows.append(row)
        row_ws = [r[-1][1] + bw(r[-1][0]) for r in rows]
        hw = None
        cw = max(row_ws)
        ch_ = len(rows) * BH + (len(rows) - 1) * 16
    return star, head, wives, kids, rows, cw, ch_, hw


def _card_pos(cw, ch_, pad):
    """The card's content corner at its usual place, bottom-centre."""
    return (W - cw) / 2, VIEW_BOT - ch_ - pad * 2 - 10


def _card_clear(focus, marks, named):
    """A card rest that keeps the people it names clear of its card.

    `marks` are the world rects the rest must show (the named boxes, and a
    title standing in for a head). If the rest `focus` gives puts any of
    them under the card's plate, the frame is fitted into the part of the
    screen above the card instead -> the focus box Camera.move turns into
    exactly that rest. Otherwise `focus` comes back unchanged."""
    _st, _h, _wv, _k, _rows, cw, ch_, _hw = card_layout(
        named, VerseFrame.card_wives_beside, VerseFrame.CARD_W_MAX)
    px, py = _card_pos(cw, ch_, CARD_PAD)
    plate = (px - CARD_PAD, py - CARD_PAD, px + cw + CARD_PAD,
             py + ch_ + CARD_PAD)
    s, cx, cy = _fit(focus, pad=70)
    tx, ty = _cam_T((s, cx, cy))
    hidden = False
    for r in marks:
        x0, y0 = tx + s * r[0], ty + s * r[1]
        x1, y1 = tx + s * r[2], ty + s * r[3]
        if x0 < plate[2] and x1 > plate[0] and y0 < plate[3] \
                and y1 > plate[1]:
            hidden = True
    if not hidden:
        return focus
    top = plate[1] - CARD_GAP                 # the screen above the card
    fw, fh = focus[2] - focus[0], focus[3] - focus[1]
    vh = VIEW_BOT - VIEW_TOP
    s2 = min(S_MAX, max(S_MIN, min(W / (fw + 140),
                                   (top - VIEW_TOP) / (fh + 140))))
    # centred in [VIEW_TOP, top] rather than [VIEW_TOP, VIEW_BOT], with a
    # height _fit reads back as exactly s2
    cy2 = cy + (VIEW_BOT - top) / 2 / s2
    hh = (vh / s2 - 140) / 2
    return (focus[0], cy2 - hh, focus[2], cy2 + hh)


# ===========================================================================
# The world
# ===========================================================================

class World:
    """The welded tree, laid out name-only, plus the per-verse reading order.

    `order` is every (chapter, verse) of 1 Chronicles 1-9 in reading order.
    `arrivals[(ch, v)]` are the nodes first read in that verse; `focus` is
    what the camera should frame for it. `plan` is what the layout's place()
    returned: a layout_regions.Plan, or None for the centred and spine
    layouts.
    """

    def __init__(self, ot=True, layout=None):
        self.tree = CT.build(ot=ot)
        self.root = self.tree.root
        lay = LAYOUTS[layout or LAYOUT]
        lay[0](self.root, notes=False)
        self.plan = lay[1](self.root, 0, 0)

        self.by_src = {}
        for n in walk(self.root):
            if n.src is not None:
                self.by_src[n.src] = n
        self.nodes = list(walk(self.root))
        self.world_box = (min(n.x for n in self.nodes),
                          min(n.y for n in self.nodes),
                          max(n.x + n.w for n in self.nodes),
                          max(n.y + n.h for n in self.nodes))
        # How each panel's title is set, and which verses rest on a panel
        # with its title standing in for a head left out of the frame
        # (focus_box): (ch, v) -> Panel.
        self.panel_titles, self.title_stands = {}, {}
        if self.plan is not None:
            # the panels reach past their boxes, and the opening shot and
            # the quiet breathe-outs must frame them whole
            for p in self.plan.panels:
                self.world_box = _union(self.world_box, p.rect)
            self.panel_titles = {p: PanelTitle(p) for p in self.plan.panels}

        self.order = []             # [(chapter, verse, scene)]
        self.arrivals = {}          # (ch, v) -> [node]  first read here
        self.lit = {}               # (ch, v) -> [node]  named in this verse
        self.first_of = {}          # node -> (ch, v)
        # Rows the tree deliberately does not carry (city lists, the duty
        # roster) leave their verses with nothing to light; the camera holds
        # where it is rather than cutting somewhere arbitrary.
        self._read_scenes()

    # -- verse matching, borrowed wholesale --------------------------------

    def _resolve_verse(self, ch, title, idxs, rows, anchor,
                       places=False):
        """Every name in one verse, settled TOGETHER.

        The `src` stamp handles most rows outright. What it cannot handle is
        a row the tree dropped on purpose — 4:1 recites a descent already
        walked, 9:35-44 retells the house of Saul from chapter 8. Where the
        tree knows whom such a row means it says so in its binding table
        (`Tree.bind`, read into `self.bound`): 4:1's Hezron is Perez's son,
        9:20's Phinehas is Eleazar's. A binding is as certain as a stamp,
        and one bound to None lights nothing, for a row the tree has no
        right box for yet. Rows neither stamped nor bound fall back to the
        name. Chronicles has ten Azariahs, so a name alone is a guess.

        Resolving each guess independently against the previous verse's
        anchor was what made chapters 5, 6 and 9 lurch: 9:37 put Gedor in
        Judah and Ahio in Elpaal's house while the verse's certain names sat
        in Gibeon, so the focus box spanned the tree and the camera flew
        across it and back. Certainty is contagious instead — the rows that
        ARE certain set the anchor, every guess goes to the candidate
        nearest it, and a second pass re-anchors on the result. A verse's
        names now land together or not at all.

        `places` turns the fallback OFF. Six of these scenes are allotment
        lists — where Simeon settled, and the five lots of Levitical cities
        — whose rows are towns. The tree carries no towns, so most of those
        verses already light nothing; the flag is for the handful whose town
        collides with a person, where "they gave them Hebron" was lighting
        Hebron the son of Kohath and "Shechem in the hill country of
        Ephraim" was lighting Shechem the son of Gilead. A verse about a
        place should light nothing and let the camera breathe out, which is
        what its neighbours in the same passage already do. A scene that
        turns to towns partway through flags only those verses (sc()), so
        the caller passes the flag as it stands for this one verse.

        Only the fallback goes. A row the tree DID lift still resolves
        through its `src` stamp (or its binding), so if the chart ever grows
        a town the verse finds it.
        """
        fixed, open_ = [], []
        home = self.scene_home.get((ch, title))
        for k in idxs:
            n = self.by_src.get((ch, title, k))
            if n is None and (ch, title, k) in self.bound:
                n = self.bound[(ch, title, k)]
                if n is None:               # bound to "lights nothing"
                    continue
            if n is not None:
                fixed.append((k, n))
                continue
            label = rows[k].label
            if label.startswith("~"):
                continue
            # Aliases are extra CANDIDATES, not a fallback. Preferring
            # exact matches outright meant "Jeiel" always found the
            # Reubenite and never "Jeiel, the father of Gibeon", whose
            # whole family the verse was about. Let the anchor choose.
            if places:
                continue
            cands = list(self.by_label.get(label, []))
            for m in self.by_alias.get(label, []):
                if m not in cands:
                    cands.append(m)
            if not cands:
                continue
            if len(cands) == 1:
                fixed.append((k, cands[0]))
            else:
                open_.append((k, cands))

        def centre(ns):
            return (sum(m.x + m.w / 2 for m in ns) / len(ns),
                    sum(m.y + m.h / 2 for m in ns) / len(ns))

        chosen = dict(fixed)
        for _pass in range(2):
            base = [chosen[k] for k, _ in fixed] or list(chosen.values())
            # A verse whose every name is a guess has nothing of its own to
            # anchor on, and following the previous verse walks it straight
            # off a subject change: 9:35 opens the house of Saul with two
            # ambiguous names, and inheriting 9:34's Levite position put
            # Jeiel among the Levites. The SCENE's own certain rows are the
            # right anchor there — a passage knows where it lives even when
            # one of its verses does not.
            a = centre(base) if base else (home or anchor)
            # KIN BEFORE DISTANCE, AND A BROTHER BEFORE A SON. A guess
            # that stands in a known relation to somebody this verse has
            # already settled for certain is not really a guess: the verse
            # says in words what the tree can confirm. Distance alone got
            # 6:43 right only by luck of the layout — "the son of Jahath,
            # the son of Gershom, the son of Levi" picked Levi's Gershom
            # while the sheet was drawn one way and MOSES' Gershom when it
            # was drawn another, because Moses sits inside Kohath's subtree
            # and Kohath is where the layout puts its weight.
            #
            # The two ranks are not interchangeable. A "sons of X" verse is
            # a row of BROTHERS, so a candidate sharing a parent with a
            # settled name beats one that is a settled name's child: 9:36
            # lists Jeiel's sons "Abdon, Zur, Kish, Baal, Ner, Nadab", and
            # ranking kinship flat pulled Kish down a generation to the
            # other Kish, the one 9:39 gives to Ner — who is standing right
            # there in the same verse as his brother.
            #
            # Ahead of both: a candidate who is the son of one settled name
            # and the father of another is the link the verse is spelling
            # out. 9:39 "Ner became the father of Kish. Kish became the
            # father of Saul" settles Ner and Saul, and the brother rule
            # alone lit Ner's brother Kish beside a Saul hanging under the
            # other one.
            fixed_ns = [chosen[k] for k, _ in fixed] or list(chosen.values())
            sibs, kin = set(), set()
            for m in fixed_ns:
                if m.parent is not None:
                    sibs.update(m.parent.kids)
                    kin.add(m.parent)
                kin.update(m.kids)
            sibs.difference_update(fixed_ns)

            def rank(c):
                return -1 if (c.parent in fixed_ns and
                              any(k in fixed_ns for k in c.kids)) \
                    else 0 if c in sibs else 1 if c in kin else 2

            if a is None:
                for k, cands in open_:
                    chosen.setdefault(k, min(cands, key=rank))
                break
            for k, cands in open_:
                chosen[k] = min(cands, key=lambda m: (
                    rank(m), math.hypot(m.x + m.w / 2 - a[0],
                                        m.y + m.h / 2 - a[1])))
            if not fixed:                      # let the guesses re-anchor
                fixed = [(k, chosen[k]) for k, _ in open_[:1]]
        return [chosen[k] for k in idxs if k in chosen]

    def _read_scenes(self):
        # The tree's bindings for rows it retells or drops (Tree.bind). Read
        # here rather than in __init__ so tools/layout_lab.py, which builds
        # its own by_src and then calls this, gets them too. They stay out
        # of scene_home: a retold row must not drag its passage's home
        # across the sheet (9:20's Phinehas would pull the gatekeepers'
        # ~760 px west).
        self.bound = dict(getattr(self.tree, "bind", {}))
        present = set(self.nodes)
        lost = [k for k, n in self.bound.items()
                if n is not None and n not in present]
        assert not lost, \
            f"rows bound to nodes no longer in the tree: {lost}"
        shadowed = [k for k in self.bound if k in self.by_src]
        assert not shadowed, \
            f"rows both stamped and bound (the binding would never be " \
            f"read): {shadowed}"
        # Exact names first; then the halves of a doubled label, because the
        # tree renames a few people the scenes know by one name only —
        # "Abraham" there is "Abram · Abraham" here, and 1:28 was naming a
        # father the chart could not find.
        #
        # A reference chip is never a candidate: it only points at the
        # woman's real box, which is the one a verse naming her lights.
        self.by_label, self.by_alias = {}, {}
        for n in self.nodes:
            if n.chip is not None:
                continue
            self.by_label.setdefault(n.label, []).append(n)
            for part in n.label.split(" · "):
                part = part.strip()
                if part != n.label:
                    self.by_alias.setdefault(part, []).append(n)
                # "Jeiel, the father of Gibeon" is the tree's own wording for
                # a man the verses simply call Jeiel; without this the whole
                # Gibeon family was invisible to 9:35 and the passage
                # anchored itself on a Reubenite of the same name.
                if ", " in part:
                    self.by_alias.setdefault(part.split(", ")[0], []).append(n)
        # Where each passage lives: the centre of everything in it that the
        # src stamp places for certain. Ambiguous names fall back to this
        # before they fall back to the previous verse.
        self.scene_home = {}
        for ch in sorted(CHAPTERS):
            for scene in CHAPTERS[ch]:
                title = scene["title"]
                sure = [self.by_src[k] for k in self.by_src
                        if k[0] == ch and k[1] == title]
                # A passage that is entirely a RE-TELLING has no src rows at
                # all — 9:35-44 gives the house of Saul a second time and the
                # tree kept only chapter 8's copy — so it would have no home
                # and every name in it would chase the previous verse across
                # the map. Its unrepeated names still pin it: Saul, Jonathan,
                # Merib Baal and Azel are unique in the canon even though
                # Jeiel, Kish and Mikloth are not.
                if not sure and not scene.get("places"):
                    # A places scene must not claim a home built out of
                    # people who merely share a name with its towns; nothing
                    # in it resolves, so the home would only mislead.
                    for row in flatten(scene):
                        if row.label.startswith("~"):
                            continue
                        c = (self.by_label.get(row.label) or
                             self.by_alias.get(row.label) or [])
                        if len(c) == 1:
                            sure.append(c[0])
                if sure:
                    self.scene_home[(ch, title)] = (
                        sum(m.x + m.w / 2 for m in sure) / len(sure),
                        sum(m.y + m.h / 2 for m in sure) / len(sure))

        seen = set()
        anchor = None
        self.narr = {}          # (ch, v) -> narration seconds, the pacing clock
        for ch in sorted(CHAPTERS):
            texts = dict(web_verses(ch))
            for scene in CHAPTERS[ch]:
                rows, _first_read, highlights = assign(scene, texts)
                title = scene["title"]
                lo, hi = scene["verses"]
                for v in range(lo, hi + 1):
                    self.order.append((ch, v, scene))
                    if (ch, v) not in self.narr:
                        sec = _mp3_seconds(os.path.join(
                            AUDIO_DIR, "1_Chronicles_%d_%d.mp3" % (ch, v)))
                        if sec is None:     # no MP3 yet: ~150 wpm estimate
                            sec = 0.40 * len(texts.get(v, "").split()) + 0.7
                        self.narr[(ch, v)] = sec
                    # `places` is a whole scene's flag, or the set of
                    # verses where a scene turns to towns (sc()).
                    p = scene.get("places")
                    p = (v in p) if isinstance(p, (set, frozenset)) \
                        else bool(p)
                    named = []
                    for n in self._resolve_verse(ch, title,
                                                 highlights.get(v, []),
                                                 rows, anchor, p):
                        if n not in named:
                            named.append(n)
                    new = [n for n in named if n not in seen]
                    seen.update(new)
                    for n in new:
                        self.first_of.setdefault(n, (ch, v))
                    self.arrivals[(ch, v)] = new
                    self.lit[(ch, v)] = named
                    if named:
                        anchor = (sum(n.x + n.w / 2 for n in named) / len(named),
                                  sum(n.y + n.h / 2 for n in named) / len(named))

    # -- what the live layout must satisfy ----------------------------------

    def audit(self):
        """-> [problem]: what must hold before a frame is written. The
        driver stops on any for the live layout.

        * No two boxes (or labels) overlap.
        * Israel, Esau and Judah stand in the tree, and Israel has the
          twelve sons of 2:1-2 (`layout_regions.landmarks`).
        * Every verse's focus box fits at FLOOR_MARGIN x S_MIN or closer:
          the camera clamps at S_MIN, so a focus wider than that would rest
          with named boxes off screen.
        * No verse lights a reference chip: the woman's real box lights.
        """
        out = []
        for n, (ch, v) in self.first_of.items():
            if n.chip is not None:
                out.append(f"{ch}:{v} lights the chip {n.label} under "
                           f"{n.parent.label}, not her box")
        clash = layout_regions.overlaps(self.nodes)
        if clash:
            out.append(f"{len(clash)} boxes overlap: " + ", ".join(
                f"{a.label} / {b.label}" for a, b in clash[:6]))
        try:
            layout_regions.landmarks(self.root)
        except AssertionError as e:
            out.append(f"landmarks: {e}")
        vh = VIEW_BOT - VIEW_TOP
        for ch, v, _scene in self.order:
            focus, _mode = self.focus_box(ch, v)
            if focus is None:
                continue
            x0, y0, x1, y1 = focus
            s = min(W / max(x1 - x0 + 140, 1), vh / max(y1 - y0 + 140, 1))
            if s < FLOOR_MARGIN * S_MIN:
                out.append(f"{ch}:{v} focus fits at {s / S_MIN:.2f} x S_MIN "
                           f"(under {FLOOR_MARGIN})")
        return out

    # -- what is standing at a given point in the reading -------------------

    def context_nodes(self):
        """Nodes drawn as already-there from the first frame: everything the
        nine chapters never name (the rest of the canon, and rows the tree
        keeps for structure but no verse reads)."""
        return [n for n in self.nodes if n not in self.first_of]

    def focus_box(self, ch, v):
        """What the camera frames, and how the verse is presented.

        "tight": the named people (with their parent when it still reads)
        fit a legible frame — the ordinary verse.  "card": they are spread
        past reading scale, and the camera now RESTS WIDE on the whole
        family again — the user chose this over the tight-anchored rest
        once the highlights learned to ride their nodes (wide lab E,
        2026-08-14): a veil dims the world with holes over the named
        people, gold rings hold them, and the card still carries the names.
        "quiet": nothing named; the camera breathes out.

        THE PANEL TITLE STANDS IN FOR A FAR HEAD (regions layout). A
        panel's head stands in the fan, and his family thousands of px below
        in his panel, so the ordinary rest of a verse that names both ("the
        sons of Levi: Gershon, Kohath and Merari") is a card wide enough to
        take in the fan and the panel at once (6:1 at 0.096), or the sons
        alone with the head off screen (4:24, 7:30). When
        everything else the frame takes in stands in that one panel, and
        the fan boxes it takes in are only the head, his wife or the
        forefathers above him, none of them arriving (_far_head), the frame
        leaves the fan out and rests on the panel, and the panel's TITLE
        stands in for the head (`title_stands`, which the frame draws lit,
        and ringed on a wide card rest):
          * a verse that names the head, and nobody else in the fan, rests
            tight on the panel with the title in frame whenever that still
            reads (READABLE);
          * otherwise a tight verse keeps its ordinary rest;
          * a card verse rests on the panel at whatever scale that takes,
            taking the title in when that keeps TITLE_COST of its scale,
            and keeps its card if the frame leaves out anybody it names
            (the card names everyone, as Matthew's dropped names do), even
            at a close rest (6:38, which also names Israel).
        A fan box that ARRIVES is never left out (Tamar, beside Judah at
        2:4), and a card that leaving the fan out would not bring closer
        is kept (4:1, where Judah stands over his panel).

        A CARD REST KEEPS ITS PEOPLE CLEAR OF THE CARD (regions layout): if
        the rest would put a named box, or the title standing in for one,
        under the card's plate, it is fitted into the screen above the card
        instead (_card_clear; 9:16's two lines fill the screen's height).
        """
        box, mode = self._rest(ch, v)
        if mode == "card" and self.plan is not None:
            named = self.lit[(ch, v)]
            stand = self.title_stands.get((ch, v))
            marks = [node_box(n) for n in named
                     if stand is None or n is not stand.head]
            if stand is not None:
                tl = self.panel_titles[stand]
                marks.append(tl.box_at(_fit(box, pad=70)[0]))
            box = _card_clear(box, marks, named)
        return box, mode

    def _rest(self, ch, v):
        """focus_box before the card is cleared."""
        arriving = self.arrivals.get((ch, v)) or []
        lit = self.lit.get((ch, v)) or []
        core = arriving or lit
        if not core:
            return None, "quiet"
        box, mode = _ladder(*_parts(core, lit))
        if self.plan is None:
            return box, mode
        self.title_stands.pop((ch, v), None)
        far = self._far_head(arriving, core, lit)
        if far is None:
            return box, mode
        p, above = far
        named = [n for n in above if n in lit]
        if mode == "tight" and _in_shot(box, [node_box(n) for n in named]):
            return box, mode                 # the head is in shot already
        tl = self.panel_titles[p]
        core2 = [n for n in core if n not in above]
        lit2 = [n for n in lit if n not in above]
        wide2, box2 = _parts(core2, lit2, leave=above)
        stands = named == [p.head]           # the title can stand for all
        if stands:
            for raw in (wide2, box2):
                b = _with_title(raw, tl, READABLE)
                if b is not None:
                    self.title_stands[(ch, v)] = p
                    return b, "tight"
        if mode == "tight":
            return box, mode
        new, mode2 = _ladder(wide2, box2)
        if mode2 == "tight" and named:
            mode2 = "card"
        if mode2 == "card" and stands:
            b = _with_title(wide2, tl, TITLE_COST * _fit(new, pad=70)[0])
            if b is not None:
                new = b
        s_new = _fit(new, pad=70)[0]
        if s_new <= _fit(box, pad=70)[0] * (1 + NEAR):
            return box, mode
        if stands and _in_shot(new, [tl.box_at(s_new)]):
            self.title_stands[(ch, v)] = p
        return new, mode2

    def _far_head(self, arriving, core, lit):
        """-> (panel, above) when this verse's frame would take in a panel
        head standing in the fan as well as his panel, else None.

        `above` is every fan box the ordinary frame takes in: the head
        (named, or pulled in as a named son's father), his wife, and the
        forefathers above him that a recital climbs through. Everything
        else it takes in must stand in that one panel, and none of `above`
        may be arriving: an arrival always rests on screen."""
        plan = self.plan
        take = []
        for n in (list(core) + [m.parent for m in core if m.parent]
                  + list(lit)):
            if n not in take:
                take.append(n)
        below = [n for n in take if n in plan.panel_of]
        above = [n for n in take if n not in plan.panel_of]
        if not below or not above:
            return None
        panels = {plan.panel_of[n] for n in below}
        if len(panels) != 1:
            return None
        p = panels.pop()
        line = {p.head} | {k for k in p.head.kids if layout_regions.is_wife(k)}
        q = p.head.parent
        while q is not None:
            line.add(q)
            q = q.parent
        if any(n not in line for n in above):
            return None
        if any(n in arriving for n in above):
            return None
        return p, above


class Camera:
    """Carries between verses: each move starts where the last one stopped."""

    def __init__(self, world):
        self.world = world
        self.cam = None
        self.focus = None
        self.scene = None
        self.quiet = 0          # consecutive verses with no name to light

    def opening(self, box):
        s, wx, wy = _fit(self.world.world_box, pad=60)
        if s >= OPEN_S_MIN:
            return s, wx, wy
        return OPEN_S_MIN, (box[0] + box[2]) / 2, (box[1] + box[3]) / 2

    def move(self, focus, scene, first):
        """-> (cam0, cam1). The overview between them is no longer a
        hand-placed keyframe: the van Wijk arc lifts on its own, so this
        only decides where a verse RESTS.

        A verse with no name in it — a city allotment, the Hagrite war, the
        gatekeepers' duty roster — is a break in the listing, and the camera
        uses it to breathe out: it eases back from where it was, a little
        further on each quiet verse up to a limit, so the branch just read is
        seen sitting in the rest of the tree. When the names resume it comes
        straight back in.
        """
        if focus is None:
            self.quiet += 1
            base = self.focus or self.world.world_box
            k = min(QUIET_MAX, QUIET_STEP ** self.quiet)
            cx, cy = (base[0] + base[2]) / 2, (base[1] + base[3]) / 2
            hw, hh = (base[2] - base[0]) / 2 * k, (base[3] - base[1]) / 2 * k
            focus = (cx - hw, cy - hh, cx + hw, cy + hh)
            cam1 = _fit(focus, pad=70)
            if cam1[0] < TEXT_MIN_SCALE:
                # breathe out only as far as the names survive — a rest
                # frame with the type gone was the other face of the wide-
                # shot problem
                cam1 = (TEXT_MIN_SCALE, cam1[1], cam1[2])
            cam0 = self.opening(focus) if (first or self.cam is None)                 else self.cam
            self.cam, self.scene = cam1, scene
            return cam0, cam1
        self.quiet = 0
        cam1 = _fit(focus, pad=70)
        cam0 = self.opening(focus) if (first or self.cam is None) else self.cam
        self.cam, self.focus, self.scene = cam1, focus, scene
        return cam0, cam1


def _cam_wrap(tracks, dur, els):
    """Wrap elements in the camera's nested translate+scale pair.

    Shared, because the veil needs a SECOND copy of exactly this transform
    (see `_ride_els`): identical values, keyTimes and duration, so SMIL
    drives both in lockstep.
    """
    tvals, svals, mode, t0, s0 = tracks
    return (
        f'<g transform="translate({_fmt(t0[0])} {_fmt(t0[1])})">'
        f'<animateTransform attributeName="transform" '
        f'attributeType="XML" type="translate" values="{tvals}" '
        f'{mode} dur="{dur}s" begin="0s" fill="freeze"/>'
        f'<g transform="scale({_fmt_s(s0)})">'
        f'<animateTransform attributeName="transform" '
        f'attributeType="XML" type="scale" values="{svals}" '
        f'{mode} dur="{dur}s" begin="0s" fill="freeze"/>'
        + "".join(els) + "</g></g>")


def _fade_group(els, begin, dur=GROW_DUR, out=False):
    """Elements fading in (or, `out`, fading away) together."""
    a, b = ("1", "0") if out else ("0", "1")
    return (f'<g opacity="{a}">{"".join(els)}'
            f'<animate attributeName="opacity" values="{a};{b}" dur="{dur}" '
            f'begin="{begin}" fill="freeze" calcMode="spline" '
            f'keyTimes="0;1" keySplines="{EASE}"/></g>')


class VerseFrame:
    """One verse's SVG: the world seen through a moving camera."""

    # Per-frame, so a book whose wide shots are meant to show the WHOLE
    # tree can spend more on them (Matthew 1:1 and 1:17), up to IPAD_NAMES
    # (render), without changing what an ordinary verse costs.
    max_nodes = MAX_NODES
    veil_alpha = VEIL_ALPHA
    # How a family is joined. True: the wall chart's drawing, one family at
    # a time (svg_family_lines) — a stem and a bus over a row, a rail with a
    # shelf to each row of a wrapped family, nothing behind anybody else's
    # box. False: the older elbow, one per child, from the parent down to a
    # bus halfway and on down to the child, which in a wrapped family ran
    # behind the brothers and nephews in between (399 of them on this
    # tree) so that a son seemed to hang from his brother. 1 Chronicles and
    # Matthew 1 both draw families; False is kept for comparison runs.
    family_lines = True
    # The cutaway card's star layout stands the head's wives beside him on
    # a short bar rather than among his children (False: the older card,
    # for comparison runs).
    card_wives_beside = True
    # The node cap also pays for the names a file writes outside the world
    # (the cutaway card's and the HUD's title), so it bounds the names in
    # the whole FILE, which is what the iPad was proven on (False: the
    # older cap, over the world's boxes only, for comparison runs).
    cap_pays_outside = True
    # A branch nobody has read yet (someone will, later in 1-9) is drawn as
    # one faint block under its first person, and a tribe's panel nobody
    # has been read in yet as its panel alone (svg_silhouettes). Only under
    # the regions layout: Matthew 1's spine world and the comparison
    # layouts have no plan, and draw every box.
    silhouettes = True

    def __init__(self, world):
        self.world = world
        self.camera = Camera(world)
        self.read = set(world.context_nodes())
        self.lines = None
        plan = getattr(world, "plan", None)
        # The regions layout's houses drawn as labels on the line, and its
        # panels' titles; both empty for the tree layouts and for Matthew.
        self.labels = set(plan.labels) if plan is not None else set()
        self.titles = dict(world.panel_titles) if plan is not None else {}
        # Boxes are drawn over lines, so a line through somebody else's box
        # seems to leave from it or arrive at it: the picture would say that
        # a man is the father of his brother. The driver stops on any.
        self.lines_behind = []
        if self.family_lines:
            self.lines = FL.Geometry(
                world.nodes, labels=self.labels,
                routes=plan.routes if plan is not None else None)
            self.lines_behind = FL.through_boxes(self.lines)
        self.sil = None
        if self.silhouettes and plan is not None and self.lines is not None:
            self.sil = SIL.Silhouettes(world, self.lines)

    def audit(self):
        """-> [problem] in the frames' own drawing, for the driver: lines
        behind boxes, two lines on one stretch, a silhouette block over
        another branch (svg_silhouettes), and THE ONE WIFE RULE. The
        regions layout packs and rows a wife by `layout_regions.is_wife`,
        and svg_family_lines draws a marriage bar by the same rule, so under
        that layout every wife must come out on a bar beside her husband:
        one standing anywhere else means two rules have drifted apart,
        which is what once overlapped twelve boxes."""
        out = [f"the {s.role} of {s.fam.label}'s family runs behind "
               f"{n.label}" for s, n in self.lines_behind]
        if self.sil is not None:
            # a block over another branch's box, line or block (the sweep
            # opens such a head a generation further, so this is empty
            # unless it failed to)
            out += self.sil.problems
        if self.lines is not None:
            # two pieces on one stretch draw as one line: only the routed
            # stems' trunk is shared, and it is drawn as single pieces
            out += [f"the {a.role} of {a.fam.label}'s family runs along the "
                    f"{b.role} of {b.fam.label}'s"
                    for a, b in FL.overlapping(self.lines)]
        if self.world.plan is not None and self.lines is not None:
            wives = {n for n in self.world.nodes if layout_regions.is_wife(n)}
            barred = {wv for _p, wv, _s in self.lines.bars}
            for n in sorted(wives - barred, key=lambda n: (n.y, n.x)):
                out.append(f"wife {n.label} ({n.parent.label}) is not on a "
                           f"bar beside her husband")
            for n in sorted(barred - wives, key=lambda n: (n.y, n.x)):
                out.append(f"{n.label} has a marriage bar but is no wife")
        return out

    def _bead_fill(self, x, y):
        """An open bead inside a panel is filled with the panel's colour:
        the background's would read as a dark hole in it."""
        for p in self.titles:
            x0, y0, x1, y1 = p.rect
            if x0 <= x <= x1 and y0 <= y <= y1:
                return PANEL_BLEND
        return None

    def _panel_els(self, flight, scales, s_end, dur, stand=None):
        """The regions layout's panels on screen at some moment of this
        flight or its rest -> (rects, titles).

        The rects go behind everything else in the world. The titles go
        over the faint and read boxes: in a wide shot a grown title reaches
        down over the panel's first rows, and drawn under them it was cut up
        by a row of specks. By the scale it gets there (~0.2) those names
        are under 3 px, and closer in it stays in the band above the first
        row. A lit or arriving box is drawn over the title (render), so the
        names a verse reads are never hidden behind one. The title of
        `stand`, the panel whose title stands in for its head this verse
        (World.focus_box), is drawn in the lit colour, like a box the verse
        names again."""
        boxes = [b for b, _s in flight]
        rects, titles = [], []
        for p, tl in self.titles.items():
            if not any(_hits(p.rect, b) for b in boxes):
                continue
            x0, y0, x1, y1 = p.rect
            sub = SvgCanvas(W, H)
            sub.rect(x0, y0, x1 - x0, y1 - y0,
                     fill=dim(PANEL, PANEL_FILL_ALPHA),
                     stroke=dim(PANEL_EDGE, PANEL_EDGE_ALPHA),
                     width=PANEL_EDGE_W, rx=PANEL_RX)
            rects.append(_unwidth(sub._els[0], PANEL_EDGE_W))
            if any(_hits(tl.box, b) for b in boxes):
                titles.extend(tl.els(scales, s_end, dur, lit=p is stand))
        return rects, titles

    def render(self, ch, v, scene, first):
        w = self.world
        focus, mode = w.focus_box(ch, v)
        # the panel whose title stands in for a head the frame leaves out
        stand = w.title_stands.get((ch, v)) if self.titles else None
        cam0, cam1 = self.camera.move(focus, scene, first)
        arc_at, apex_scale = _vw(cam0, cam1)
        apex = arc_at(0.5)

        arriving = set(w.arrivals.get((ch, v), []))
        lit = set(w.lit.get((ch, v), []))
        # A move may take its time only when the narration does. The WEB MP3
        # is the clock: camera, tracing and arrivals must all land a beat
        # (AUDIO_SLACK) before it runs out — "Adam, Seth, Enosh" is two
        # seconds of audio, and the old flat floor was still gliding after
        # the reader had finished. Long moves keep their length wherever the
        # verse is long enough to afford them.
        dur = _pace(cam0, cam1, apex_scale)
        narr = w.narr.get((ch, v))
        if narr:
            dur = min(dur, max(1.1, (narr - AUDIO_SLACK) / GROW_TAIL))
        dur = round(dur, 2)
        # A box carries its name exactly when the viewer can see it: on
        # screen at NAME_MIN_SCALE or closer at any moment of the flight
        # the file bakes, or of the rest it freezes on. Three frames used
        # to stand in for the flight — start, the arc's midpoint and the
        # end — and every box the camera swept past between them, or past
        # all of the midpoint once a wide one fell below TEXT_MIN_SCALE and
        # was dropped, flew by empty (66 verses, 7:13 the worst).
        flight = _flight_seen(cam0, cam1, arc_at, dur)
        # Silhouettes: the boxes this verse rests with folded into blocks
        # are not drawn, and the boxes the verse opened on folded and rests
        # with standing (`opened`) fade in while their blocks fade out.
        pool, opened, sil = w.nodes, frozenset(), None
        if self.sil is not None:
            i = self.sil.pos[(ch, v)]
            cur = self.sil.state(i)
            prev = cur if first else self.sil.state(i - 1)
            pool = [n for n in w.nodes if n not in cur.hidden]
            opened = prev.hidden - cur.hidden
            sil = (prev, cur, self._blocks_seen(prev, cur, flight))
        seen = _seen_scale(pool, flight)
        detail = _frame(cam1, DETAIL_PAD)
        skeleton = detail
        for cam in (cam0, apex):
            skeleton = _union(skeleton, _frame(cam, SKELETON_PAD))

        # The regions layout's panels on screen in this flight. Their titles
        # are names too, and so are the cutaway card's and the HUD's title:
        # all of them are paid for out of the node cap, which is what keeps
        # a file's names within what the iPad has been proven on.
        scales = _cam_schedule(cam0, cam1, arc_at, dur)
        panels, titles = self._panel_els(flight, scales, cam1[0], dur, stand)
        named = list(w.lit.get((ch, v), []))       # verse reading order
        outside = 0
        if self.cap_pays_outside:
            outside = 1 + (len(named) if mode == "card" and named else 0)
        max_nodes = self.max_nodes - len(titles) - outside
        if sil is not None:
            # a block is one item, like a box (a whole panel's block is
            # the panel, drawn anyway)
            max_nodes -= sum(1 for b in sil[2] if b.panel is None)
        if self.cap_pays_outside:
            # An arriving name is written twice — the faint box it stood as
            # and the lit one that fades in over it — so the names in the
            # whole file stay within IPAD_NAMES by construction: each drawn
            # box writes at most one name, an arrival one more, and the
            # titles, the card and the HUD are counted above.
            max_nodes = min(max_nodes, IPAD_NAMES - len(titles) - outside
                            - len(arriving))

        # Everything the camera passes over, capped: a wide pull-back can
        # otherwise sweep in half the canon.
        #
        # The budget goes first to the frame the verse OPENS on, up to
        # DWELL_SHARE — spending it all on "nearest the destination"
        # emptied the start frame of six chapter 9 verses outright, and the
        # pull-out then revealed it had been pointed at nothing. Next come
        # the boxes the flight shows at a legible scale, largest first, then
        # the frame the verse rests on, then the rest of what the flight
        # shows; only what is left goes to margin and filler, nearest the
        # destination first. A box on screen mid-flight is in the pool even
        # outside the skeleton's bounding box, which never quite held the
        # whole arc.
        shown = [n for n in pool
                 if n in seen or _hits(node_box(n), skeleton)]
        if len(shown) > max_nodes:
            def near(cam, pool):
                cxx, cyy = cam[1], cam[2]
                return sorted(pool, key=lambda n: math.hypot(
                    n.x + n.w / 2 - cxx, n.y + n.h / 2 - cyy))

            def biggest(pool):
                return sorted(pool, key=lambda n: (-seen[n], math.hypot(
                    n.x + n.w / 2 - cam1[1], n.y + n.h / 2 - cam1[2])))

            keep = set(arriving) | set(lit)
            if len(keep) > max_nodes:
                raise ValueError(f"{ch}:{v} names {len(keep)} people, more "
                                 f"than its node cap of {max_nodes}")

            def take(ordered, cap=max_nodes):
                room = cap - len(keep)
                if room > 0:
                    keep.update([n for n in ordered if n not in keep][:room])

            fr0, rest = _frame(cam0, DETAIL_PAD), _on_screen(cam1)
            take(near(cam0, [n for n in shown if _hits(node_box(n), fr0)]),
                 int(max_nodes * DWELL_SHARE))
            take(biggest([n for n in shown
                          if seen.get(n, 0) >= TEXT_MIN_SCALE]))
            take(near(cam1, [n for n in shown if _hits(node_box(n), rest)]))
            take(biggest([n for n in shown if n in seen]))
            take(near(cam1, [n for n in shown
                             if _hits(node_box(n), detail)]))
            take(near(cam1, shown))
            shown = [n for n in pool if n in keep]

        # The cap keeps the file to what can be NAMED. Past it, every other
        # box the flight puts on screen is drawn as an outline only — box
        # and connector, no name, no icon — so a wide pull-back still shows
        # the whole shape of the tree instead of two lit patches with
        # nothing between them (5:19, 9:10, 9:35 drew nothing at the apex).
        kept = set(shown)
        outline = {n for n in _seen_scale(pool, flight, 0.0)
                   if n not in kept}
        if outline:
            shown = [n for n in pool if n in kept or n in outline]

        c = SvgCanvas(W, H, bg=BG)
        # Four layers, and the order is the point: a connector drawn while
        # walking the tree crosses boxes that were drawn earlier, so all the
        # lines go down first and all the boxes sit on top of them. A line
        # behind a name reads; a line across one does not.
        #
        # Box edges and static connectors carry no stroke-width of their
        # own: they inherit it from one group per nominal width, which
        # holds a screen-pixel floor through the zoom (_stroke_group).
        # Boxes do not overlap, so grouping them by width costs no order.
        lines, lines_new, boxes, boxes_new = [], [], {}, []
        boxes_open = {}             # boxes standing up out of a block
        for n in shown:
            state = ("new" if n in arriving else
                     "lit" if n in lit else
                     "read" if n in self.read else "ahead")
            self._draw(lines, lines_new, boxes_open if n in opened else boxes,
                       boxes_new, n, state, n in seen and n not in outline,
                       dur)
        fine = []
        sil_els = None
        if self.lines is not None:
            lines, fine, lines_new, sil_els = self._family_lines(
                shown, arriving, lit, dur, sil, opened, flight)

        self.read |= arriving

        # Panel titles go over the faint and read boxes (a grown title
        # reaches the panel's first rows only where their names are specks)
        # but under the lit and arriving ones, so a box the verse names, and
        # the ring that rides it, are never hidden behind a tribe's name.
        lit_w = self.LOOK["lit"][2]

        # The blocks lie over the panels and under every line and box. The
        # ones this verse opens fade out, the ones it leaves fade in, and so
        # do their lines and the boxes standing up out of them; each fade is
        # a group inside the stroke group of its width, so a verse that
        # opens a block adds no stroke-width animation.
        o_begin, o_dur = "%.2fs" % (dur * OPEN_AT), "%.2fs" % (dur * OPEN_LEN)

        def fade(els, out=False):
            return [_fade_group(els, o_begin, o_dur, out)] if els else []

        def stroked(els, wd, gone=(), come=()):
            return _stroke_group(list(els) + fade(gone, out=True)
                                 + fade(come), wd, scales, cam1[0], dur)

        def box_groups(wds):
            return [stroked(boxes.get(wd, ()), wd, come=boxes_open.get(wd, ()))
                    for wd in wds]

        b_keep = b_gone = b_new = l_gone = f_gone = l_new = f_new = ()
        if sil_els is not None:
            (b_keep, b_gone, b_new, l_gone, f_gone, l_new, f_new) = sil_els
        widths = sorted(set(boxes) | set(boxes_open))
        els_all = (([_stroke_group(panels, PANEL_EDGE_W, scales, cam1[0],
                                   dur)] if panels else [])
                   + [stroked(b_keep, BLOCK_EDGE_W, b_gone, b_new)]
                   + self._extra_world_els(ch, v, dur, shown)
                   + [stroked(lines, CONNECTOR_W, l_gone, l_new)]
                   + [stroked(fine, FINE_W, f_gone, f_new)]
                   + lines_new
                   + box_groups([wd for wd in widths if wd < lit_w])
                   + titles
                   + box_groups([wd for wd in widths if wd >= lit_w])
                   + [_stroke_group(boxes_new, lit_w, scales, cam1[0], dur)])
        veil_screen = []
        if mode == "card" and named and cam1[0] < READABLE:
            # the camera group has to be built first: the veil's mask holes
            # reuse its transform tracks so they ride the same flight
            probe = self._camera_group(cam0, cam1, arc_at, dur, [])
            ridden = named
            if stand is not None:
                # the head's ring moves onto the title standing in for him
                ridden = ([n for n in named if n is not stand.head]
                          + [self.titles[stand]])
            rings, veil_screen = _ride_els(
                ridden, scales, cam1[0],
                dur, "veil%d_%d" % (ch, v), self.cam_tracks,
                veil_alpha=self.veil_alpha)
            els_all = els_all + rings
        world_g = self._camera_group(cam0, cam1, arc_at, dur, els_all)
        c.raw([world_g] + veil_screen)
        if mode == "card" and named:
            self._card(c, named, dur)
        self._hud(c, ch, v, scene)
        return c

    def _extra_world_els(self, ch, v, dur, shown):
        """Anything else this book draws in world space, under the boxes.

        Chronicles draws nothing; Matthew draws the gold arc of a claim one
        book makes about another's tree (see svg_matthew_world).
        """
        return []

    # -- one node ----------------------------------------------------------

    LOOK = {                     # box alpha, edge, stroke width, text
        "lit":   (1.00, "hl",  2.2, HL),
        "read":  (0.82, "own", 1.3, TEXT),
        "ahead": (0.24, "own", 1.2, dim(TEXT_DIM, 0.7)),
    }

    def _node_els(self, n, look, full):
        """Box and name for one node, in one of the three looks. A
        reference chip is the wall chart's pill (draw_chip): never lit,
        since it carries no src and the World's name lookup leaves it out,
        so the woman's real box is the one a verse lights."""
        alpha, edge_kind, wdt, tint = self.LOOK[look]
        col = accent(n)
        edge = HL if edge_kind == "hl" else dim(col, alpha)
        sub = SvgCanvas(W, H)
        if n.chip is not None:
            draw_chip(sub, n, edge, tint, dim(ROYAL, alpha),
                      fill=dim(PANEL, alpha), width=wdt, name=full)
            sub._els[0] = _unwidth(sub._els[0], wdt)
            return sub._els
        sub.rect(n.x, n.y, n.w, n.h, fill=dim(PANEL, alpha), stroke=edge,
                 width=wdt, rx=12 if n.kind == "woman" else 4)
        # the edge's width comes from its _stroke_group
        sub._els[0] = _unwidth(sub._els[0], wdt)
        ty = n.y + PAD_Y
        if n.icon and full and look != "ahead":
            _icon(sub, n, n.x + n.w / 2, ty + ICON_H)
            ty += ICON_H + 2
        if full:
            if n.kind == "king":
                _crown(sub, n.x + PAD_X + 1, ty + NAME_H / 2)
            # Weight never changes with state: bolding a lit name made the
            # glyphs step wider than the box that was measured for the
            # regular face, and Togarmah clipped (1:6). Colour and the box
            # stroke carry the highlight.
            sub.text((n.x + PAD_X + (16 if n.kind == "king" else 0),
                      ty + NAME_H / 2), n.label, 15, tint, anchor="lm",
                     bold=n.kind in ("king", "priest"),
                     italic=n.kind == "house")
        return sub._els

    def _draw(self, lines, lines_new, boxes, boxes_new, n, state, full, dur):
        """A name that arrives this verse BRIGHTENS. It is not rebuilt.

        The first cut wiped each arriving box open from zero width over a
        ghost that had been standing there since the chapter began, so every
        arrival read as the ghost vanishing and a box being constructed in
        its place: the same name twice, for no gain. Now the ghost stays
        exactly where it was and the lit version cross-fades on top of it
        while the connector traces out. Nothing disappears; the branch
        lights up.

        With `family_lines` the lines are drawn per family afterwards
        (_family_lines) and this draws the boxes only. A house the layout
        draws as a label is its italic name alone (_label_els), and
        brightens the same way.
        """
        elbow = self.lines is None
        els = self._label_els if n in self.labels else self._node_els
        if state != "new":
            if elbow:
                lines.append(self._connector(n, state))
            boxes.setdefault(self.LOOK[state][2], []).extend(
                els(n, state, full))
            return
        gdur, gbegin = _grow_timing(dur)
        if elbow:
            lines.append(self._connector(n, "ahead"))
        boxes.setdefault(self.LOOK["ahead"][2], []).extend(
            els(n, "ahead", full))
        if elbow:
            lines_new.append(self._connector(n, "lit", gdur, trace=True))
        lit_els = els(n, "lit", full)
        if lit_els:
            boxes_new.append(_fade_group(lit_els, gbegin, gdur))

    def _label_els(self, n, look, full):
        """A house the regions layout draws as a label: its name, small and
        italic, in the gap above the row it gathers, with no box. The line
        from the parent runs into its top and its own stem leaves its
        bottom, so it sits on the line. It is a name like any other: shown
        whenever a box there would be, in the same three looks. Past the
        node cap (`full` off) a box keeps its outline; a label has none, so
        it draws nothing."""
        if not full:
            return []
        sub = SvgCanvas(W, H)
        sub.text((n.x + n.w / 2, n.y + n.h / 2), n.label, LABEL_PX,
                 self.LOOK[look][3], anchor="mm", italic=True)
        return sub._els

    def _blocks_seen(self, prev, cur, flight):
        """The silhouettes this verse's file draws: every block of the state
        it opens on or the one it rests on that the flight puts on screen at
        any scale, as a past-the-cap outline would be."""
        boxes = [b for b, _s in flight]
        out = {}
        for st in (prev, cur):
            for k, b in st.blocks.items():
                if k not in out and any(_hits(b.reach, fb)
                                        for fb in boxes):
                    out[k] = b
        return list(out.values())

    def _block_els(self, blocks):
        """Block rects, their edges' width left to a stroke group."""
        sub = SvgCanvas(W, H)
        for b in blocks:
            if b.panel is not None:
                continue                    # the panel itself stands for it
            x0, y0, x1, y1 = b.rect
            sub.rect(x0, y0, x1 - x0, y1 - y0, fill=BLOCK_FILL,
                     stroke=BLOCK_EDGE, width=BLOCK_EDGE_W, rx=BLOCK_RX)
        return [_unwidth(e, BLOCK_EDGE_W) for e in sub._els]

    def _family_lines(self, shown, arriving, lit, dur, sil=None,
                      opened=frozenset(), flight=()):
        """This verse's lines, one family at a time -> (static, fine,
        growing, silhouettes).

        Every piece leading to a drawn box is drawn ONCE, in the brightest
        look of the people it leads to: a bus that serves a lit brother and
        three faint ones is lit as far as the lit one and faint beyond him.
        A name arriving here stands faint like its box (its lines in the
        "ahead" look), and its own path from the parent — stem, bus or
        rail and shelf, drop — then draws itself over them in the lit look,
        on the old trace's timing, while the box brightens. Arrivals that
        share a stem each trace it; the standing stem is still drawn once.

        `sil` = (state opened on, state rested on, blocks drawn), or None.
        A block's stem is drawn with it. The lines of the boxes standing up
        out of a block this verse (`opened`), and the stems of the blocks
        the verse leaves, fade in; the stems of the blocks it opens fade
        out. `silhouettes` is then (blocks kept, blocks going, blocks
        coming, lines going, fine going, lines coming, fine coming), else
        None.

        A piece toward boxes the flight never shows is drawn too wherever
        the flight (`flight`, as _flight_seen gives it) crosses it, so a
        family's line runs on off the edge instead of stopping at the last
        box drawn: Kohath's bus to Amram, off screen left at 6:38. A piece
        that leads only into blocks is theirs to draw.
        """
        rank = ("ahead", "read", "lit")
        # a box folded into a block is not standing: the stem into the
        # block is in the faint look unless a box it leads to stands. The
        # stems of the blocks this verse opens keep the look they had in
        # the state it opened on.
        folded = sil[1].hidden if sil is not None else frozenset()
        was = sil[0].hidden if sil is not None else frozenset()

        def standing(k, hid):
            if k in arriving or k in hid:
                return 0
            if k in lit:
                return 2
            return 1 if k in self.read else 0

        def look(s):
            return rank[max(standing(k, folded) for k in s.serves)]

        def look_was(s):
            return rank[max(standing(k, was) for k in s.serves)]

        bead = self._bead_fill if self.titles else None
        segs, taken = [], set()
        rose = []                   # pieces of the boxes standing up
        for n in shown:
            for s in self.lines.node_segments.get(n, ()):
                if id(s) not in taken:
                    taken.add(id(s))
                    segs.append(s)
        # pieces toward boxes never on screen: standing, or fading in with
        # boxes that stand up out of a block off screen
        crossing, rising = [], []
        folding = folded | was
        for s in self.lines.segs:
            if id(s) in taken or not any(_hits(s.bbox(), fb)
                                         for fb, _sc in flight):
                continue
            if any(k not in folding for k in s.serves):
                crossing.append(s)
            elif any(k not in folded for k in s.serves):
                rising.append(s)
            else:
                continue
            taken.add(id(s))
        silhouettes = None
        if sil is not None:
            prev, cur, drawn = sil
            # a piece stands from the start if a box it leads to does
            stood = {id(s) for n in shown if n not in opened
                     for s in self.lines.node_segments.get(n, ())}
            rose = [s for s in segs if id(s) not in stood]
            segs = [s for s in segs if id(s) in stood]
            keep, gone, come = [], [], []
            for b in drawn:
                (keep if b.key in prev.blocks and b.key in cur.blocks else
                 gone if b.key in prev.blocks else come).append(b)
            stem = {}
            for group, b_list in ((0, keep), (1, gone), (2, come)):
                for b in b_list:
                    for s in b.stubs:
                        if id(s) in taken:
                            continue
                        g = stem.get(id(s), (group, s))[0]
                        stem[id(s)] = (0 if g != group else group, s)
            segs += [s for g, s in stem.values() if g == 0]
            l_gone, f_gone = FL.static_els(
                [s for g, s in stem.values() if g == 1], look_was,
                LINE_ALPHA, bead_fill=bead)
            l_new, f_new = FL.static_els(
                rose + rising + [s for g, s in stem.values() if g == 2], look,
                LINE_ALPHA, bead_fill=bead)
            silhouettes = (self._block_els(keep), self._block_els(gone),
                           self._block_els(come), l_gone, f_gone, l_new,
                           f_new)
        segs += crossing
        lines, fine = FL.static_els(segs, look, LINE_ALPHA, bead_fill=bead)
        gdur, _gbegin = _grow_timing(dur)
        growing = []
        for n in shown:
            if n in arriving:
                growing.extend(FL.trace_els(self.lines, n, LINE_ALPHA["lit"],
                                            TRACE_W, TRACE_FINE_W, gdur))
        return lines, fine, growing, silhouettes

    def _connector(self, n, look, gdur=None, trace=False):
        """The older elbow from the parent to one child (family_lines
        off)."""
        p = n.parent
        if p is None:
            return ""
        alpha = LINE_ALPHA[look]
        col = dim(FEMALE if n.link == "wife" else SAND_DIM, alpha)
        px, py = p.x + p.w / 2, p.y + p.h
        nx, ny = n.x + n.w / 2, n.y
        bus = (py + ny) / 2
        pts = [(px, py), (px, bus), (nx, bus), (nx, ny)]
        sub = SvgCanvas(W, H)
        if trace:
            sub.traced(pts, col, 1.6, dur=gdur or GROW_DUR)
        else:
            sub.polyline(pts, col, CONNECTOR_W,
                         dash="4 4" if n.link == "dash" else None)
            sub._els[0] = _unwidth(sub._els[0], CONNECTOR_W)
        return "".join(sub._els)

    # -- the cutaway card ---------------------------------------------------

    CARD_W_MAX = 880

    def card_pos(self, cw, ch_, pad):
        """Where the cutaway card sits. Bottom-centre unless a book moves
        it — Matthew's two panorama verses put it out of the way of the
        highlights, which on those shots run down the middle of the sheet."""
        return _card_pos(cw, ch_, pad)

    def _card(self, c, named, dur):
        """The verse, drawn as its own close-up when the tree cannot hold it.

        Noah's three sons span a third of the sheet; Judah's twelve span all
        of it.  Framing them in the world meant a shot no name survived, and
        every dressing tried on that shot — rings, numbered rings, a chip
        strip — still left the viewer resting on an illegible field.  So the
        wide rest is gone: the camera settles somewhere readable, and the
        verse itself appears as a small purpose-built diagram, in the house
        box style, floating over the tree.  A "sons of" verse draws parent
        over children with real connectors; a recital draws the chain in
        reading order, a joint where the text steps down a generation, a
        gap-dot where it moves to the next brother.  The next verse dives
        back into the tree and the card is gone.
        """
        star, head, wives, kids, rows, cw, ch_, hw = card_layout(
            named, self.card_wives_beside, self.CARD_W_MAX)
        bw, BH, WG, pad = _card_bw, CARD_BH, CARD_WG, CARD_PAD

        def draw_box(sub, n, x, y):
            sub.rect(x, y, bw(n), BH, fill=dim(PANEL, 1.0), stroke=HL,
                     width=1.8, rx=12 if n.kind == "woman" else 4)
            tx = x + PAD_X
            if n.kind == "king":
                _crown(sub, tx, y + BH / 2)
                tx += 16
            sub.text((tx, y + BH / 2), n.label, 15, HL, anchor="lm",
                     bold=n.kind in ("king", "priest"),
                     italic=n.kind == "house")

        sub = SvgCanvas(W, H)
        if star:
            px, py = self.card_pos(cw, ch_, pad)
            sub.rect(px - pad, py - pad, cw + 2 * pad, ch_ + 2 * pad,
                     fill=BG + (234,), stroke=dim(SAND_DIM, 0.95),
                     width=1.1, rx=10)
            hx = px + cw / 2 - hw / 2
            draw_box(sub, head, hx, py)
            sx = px + cw / 2                       # where the stem leaves
            if wives:
                sx = hx + bw(head) / 2
                wx = hx + bw(head)
                for i, wv in enumerate(wives):
                    wx += WG
                    bar = dim(FEMALE, 0.95)
                    if i == 0:                     # a doubled bar to her
                        for dy, wd in ((-1.5, 1.5), (1.5, 1.0)):
                            sub.line((wx - WG, py + BH / 2 + dy),
                                     (wx, py + BH / 2 + dy), bar, wd)
                    else:
                        # a later wife hangs from a comb over the row: a
                        # bar to her would run behind the first wife and
                        # read as a marriage between the two women
                        cx_ = wx + bw(wv) / 2
                        ax = hx + bw(head) - 10
                        for dx, wd in ((0.0, 1.5), (3.0, 1.0)):
                            sub.polyline([(ax + dx, py),
                                          (ax + dx, py - 8 + dx),
                                          (cx_ + dx, py - 8 + dx),
                                          (cx_ + dx, py)], bar, wd)
                    draw_box(sub, wv, wx, py)
                    if all(k.parent is wv for k in kids):
                        sx = wx + bw(wv) / 2
                    wx += bw(wv)
            bus = py + BH + 11
            sub.line((sx, py + BH), (sx, bus),
                     dim(SAND_DIM, 0.95), 1.5)
            y = bus + 11
            prev_rail = None
            for ri, r in enumerate(rows):
                rw = r[-1][1] + bw(r[-1][0])
                rx0 = px + (cw - rw) / 2
                cxs = [rx0 + off + bw(n) / 2 for n, off in r]
                by = y - 11
                if ri == 0:
                    sub.line((min(cxs + [sx]), bus),
                             (max(cxs + [sx]), bus),
                             dim(SAND_DIM, 0.95), 1.5)
                    by = bus
                    prev_rail = min(cxs) - 12
                else:
                    sub.line((prev_rail, bus), (prev_rail, by),
                             dim(SAND_DIM, 0.9), 1.3)
                    sub.line((prev_rail, by), (max(cxs), by),
                             dim(SAND_DIM, 0.9), 1.3)
                for (n, off), cx_ in zip(r, cxs):
                    sub.line((cx_, by), (cx_, y), dim(SAND_DIM, 0.95), 1.4)
                    draw_box(sub, n, rx0 + off, y)
                y += BH + 24
        else:
            px, py = self.card_pos(cw, ch_, pad)
            sub.rect(px - pad, py - pad, cw + 2 * pad, ch_ + 2 * pad,
                     fill=BG + (234,), stroke=dim(SAND_DIM, 0.95),
                     width=1.1, rx=10)
            y = py
            for r in rows:
                rx0 = px + (cw - (r[-1][1] + bw(r[-1][0]))) / 2
                for n, off, joint in r:
                    gx = rx0 + off
                    if joint == "line":
                        sub.line((gx - 22, y + BH / 2), (gx, y + BH / 2),
                                 dim(SAND_DIM, 0.95), 1.5)
                    elif joint == "dot":
                        sub.circle(gx - 11, y + BH / 2, 2.0,
                                   fill=dim(TEXT_DIM, 0.9), stroke=None)
                    draw_box(sub, n, gx, y)
                y += BH + 16
        c._emit(_fade_group(sub._els, "%.2fs" % (dur * 0.50),
                            "%.2fs" % (dur * 0.35)))

    # -- the camera --------------------------------------------------------

    def _camera_group(self, cam0, cam1, arc_at, dur, els):
        """Emit the flight `arc_at` describes, baked at CAM_FPS.

        Two cases, from the camera lab the user judged (2026-08-14):

        * The scale does not change: the path is a straight line, which two
          keyframes and a spline ease describe EXACTLY — the browser
          evaluates it analytically, and this is the pure-pan behaviour the
          user signed off ("worked really well for all pure pans").
        * Anything else flies the van Wijk arc, sampled at CAM_FPS with the
          ease baked into the placement and uniform keyTimes. At ~33 ms per
          interval the piecewise linearity sits below perception — this is
          lab variant C, chosen over the three-leg decomposition (exact but
          three visible gestures, sprinting pan) and over sparse placed
          keyframes with spline timing (variant D).
        """
        cams, times, pure_pan = _flight(cam0, cam1, arc_at, dur)
        mode_extra = ('calcMode="spline" keySplines="%s"' % EASE
                      if pure_pan else "")
        tvals = ";".join("%s %s" % (_fmt(_cam_T(cm)[0]), _fmt(_cam_T(cm)[1]))
                         for cm in cams)
        svals = ";".join(_fmt_s(cm[0]) for cm in cams)
        ktimes = ";".join(("%.5f" % t).rstrip("0").rstrip(".") or "0"
                          for t in times)
        mode = ('keyTimes="%s" %s' % (ktimes, mode_extra)).strip()
        self.cam_tracks = (tvals, svals, mode, _cam_T(cams[0]), cams[0][0])
        return _cam_wrap(self.cam_tracks, dur, els)

    # -- the fixed band ----------------------------------------------------

    def _hud(self, c, ch, v, scene):
        hud = SvgLayer()
        hud.rectangle([0, 0, W, HUD_H], fill=BG + (236,))
        hud.text((28, 20), f"{scene['title']} — 1 Chronicles {ch}",
                 font=F_TITLE, fill=TEXT)
        c.raw(hud.elements())
        c.line((0, HUD_H), (W, HUD_H), dim(SAND_DIM, 0.6), 1.0)
