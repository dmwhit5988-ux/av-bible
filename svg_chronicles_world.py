"""The 1 Chronicles 1-9 genealogies, read against the whole-canon tree.

The old per-verse renderer (`svg_1chronicles_render.py`) laid each chapter
out as its own world of side-by-side scenes. That reads well chapter by
chapter and hides the thing the genealogies are actually for: it is ONE
descent, and chapter 4 re-roots on a Judah the reader already met in chapter
2. This world is the welded tree from `chronicles_tree.py` instead — laid out
once, name-only — and every verse of all nine chapters is a camera move over
that single map.

Three consequences worth knowing:

* THE TREE ACCUMULATES. `read` is global across chapters 1-9 in reading
  order, not per chapter. Judah lights up at 2:1 and is still lit when 4:1
  comes back to him, so by chapter 9 the whole thing is standing.
* NEW NAMES GROW IN. A name first read in this verse arrives: its connector
  draws itself from the parent, its box wipes open, its name fades up. That
  is what makes a family spread across a wide row read as one family — you
  watch the branch reach each sibling.
* BREAKS PULL BACK. When the next name is a long way from the last, or the
  passage changes subject, the camera goes out through a wide mid-keyframe
  before coming back in, so the jump is seen as a move across one tree
  rather than a cut to somewhere else.

Verse matching is NOT redone here. `generate_1chronicles.assign()` is still
the authority; the bridge is the `src` stamp that `chronicles_tree` puts on
every node it lifts out of the scene data — (chapter, scene title, flatten
index) — which is exactly the key `assign()` returns.

Rendered by generate_1chronicles_tree_svg.py.
"""

import math
import os
import struct

import chronicles_tree as CT
from chronicles_tree import walk
from generate_1chronicles import (CHAPTERS, assign, flatten,
                                  web_verses)
from generate_ot_family_tree_svg import (BG, FAINT, HL, HOUSE, PANEL,
                                         PRIESTLY, ROYAL, SAND_DIM, TEXT,
                                         TEXT_DIM, FEMALE, ICON_H, MIN_W,
                                         NAME_H, PAD_X, PAD_Y, _crown, _icon,
                                         accent, arrange, arrange_spine, dim,
                                         place, place_spine)
from generate_tabernacle import W, H, F_TITLE, font
from svg_surface import SvgCanvas, SvgLayer, _fmt

# -- viewport ---------------------------------------------------------------

HUD_H = 46
VIEW_TOP, VIEW_BOT = HUD_H + 14, H - 20
S_MIN, S_MAX = 0.05, 1.25
OPEN_S_MIN = 0.11
FOCUS_MIN_W, FOCUS_MIN_H = 460, 250
READABLE = 0.52             # below this a 15px name is not worth framing for
MAX_NODES = 260             # per-verse ceiling, so one wide shot cannot
                            # balloon the file
DWELL_SHARE = 0.45          # of that ceiling, reserved for the frame the
                            # verse OPENS on before the rest is spent
TEXT_MIN_SCALE = 0.34       # below this a name is drawn as its box alone
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

REPO = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(REPO, "deploy_bundle", "audio")

# -- which layout the world is laid out in ----------------------------------
#
# "centred" is the wall chart's rule — a parent over the whole span of its
# descendants. "spine" puts the heir directly under its parent, so a line of
# descent is a straight vertical column.
#
# CHRONICLES USES CENTRED, AND THE SPINE WAS TRIED AND REJECTED HERE
# (2026-08-21). Matthew 1 is nothing but a line of descent and the spine
# transformed it; these nine chapters are mostly FANS — "the sons of X" — and
# a fan is tightest when the parent is centred over its children, because the
# spine cascades every sibling to one side of the heir.
#
# The count of wide rests barely moved (66 -> 75 over the whole reading, and
# 13 -> 13 across chapters 1-2). What moved was HOW WIDE they are, which is
# what a viewer actually feels: across chapters 1-2 the mean rest scale of the
# wide verses went 0.147 -> 0.117, and the ones that matter roughly halved —
# 1:4 (the sons of Noah) 0.101 -> 0.053, 1:28 (Abraham, Isaac and Ishmael)
# 0.134 -> 0.066, 1:34 (Isaac, Jacob and Esau) 0.137 -> 0.073. The front of
# the book is where the fans are widest and the spine is worst.
#
# The switch stays because the comparison is worth being able to re-run:
# `--spine` on the driver, `LAYOUT` here, or `World(layout=...)`. Matthew calls
# arrange_spine directly and is unaffected by this setting.
LAYOUT = "centred"
LAYOUTS = {"spine": (arrange_spine, place_spine),
           "centred": (arrange, place)}


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


def _cam_schedule(cam0, cam1, arc_at, dur):
    """The scale-over-time the camera will fly — None for a pure pan.
    Keep the sample count in lockstep with _camera_group."""
    if abs(cam1[0] - cam0[0]) <= 1e-9:
        return None
    n = max(6, int(round(dur * CAM_FPS)))
    return [arc_at(_smooth(i / n))[0] for i in range(n + 1)]


def _ride_r(nd, s, floor):
    """Highlight radius in world units at camera scale s: hugs the node's
    box while the camera is close, floors at a constant screen size once
    the node is small."""
    hug = math.hypot(nd.w, nd.h) / 2 + 10
    return max(floor, hug * s) / s


def _anim(attr, vals, dur):
    return (f'<animate attributeName="{attr}" values='
            f'"{";".join("%.2f" % v for v in vals)}" dur="{dur}s" '
            f'begin="0s" fill="freeze"/>')


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
    """
    hlrgb = "rgb(%d,%d,%d)" % HL[:3]
    bgrgb = "rgb(%d,%d,%d)" % BG[:3]
    holes, rings = [], []
    for nd in named:
        cx, cy = nd.x + nd.w / 2, nd.y + nd.h / 2
        if scales is None:
            hr = _ride_r(nd, s_end, HOLE_MIN) + 8
            holes.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" '
                         f'r="{hr:.1f}" fill="black"/>')
            rr = _ride_r(nd, s_end, RING_MIN)
            rings.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" '
                         f'r="{rr:.1f}" fill="none" stroke="{hlrgb}" '
                         f'stroke-opacity="0.85" '
                         f'stroke-width="{2.2 / s_end:.2f}"/>')
        else:
            hv = [_ride_r(nd, sc, HOLE_MIN) + 8 for sc in scales]
            holes.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" '
                         f'r="{hv[0]:.1f}" fill="black">'
                         + _anim("r", hv, dur) + '</circle>')
            rv = [_ride_r(nd, sc, RING_MIN) for sc in scales]
            wv = [2.2 / sc for sc in scales]
            rings.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" '
                         f'r="{rv[0]:.1f}" fill="none" stroke="{hlrgb}" '
                         f'stroke-opacity="0.85" '
                         f'stroke-width="{wv[0]:.2f}">'
                         + _anim("r", rv, dur)
                         + _anim("stroke-width", wv, dur) + '</circle>')
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
# names only inside the frame it ends on, and bare boxes inside the wider
# frames the camera passes through — at those scales a name is under six
# pixels tall anyway, and the boxes alone are what carry "this is still the
# same tree".

DETAIL_PAD = 1.35           # frame expansion for full-detail nodes
SKELETON_PAD = 1.15

F_NODE = font(15)
F_NODE_B = font(15, bold=True)


# ===========================================================================
# Geometry helpers (the camera math of svg_1chronicles_render, restated for
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


# ===========================================================================
# The world
# ===========================================================================

class World:
    """The welded tree, laid out name-only, plus the per-verse reading order.

    `order` is every (chapter, verse) of 1 Chronicles 1-9 in reading order.
    `arrivals[(ch, v)]` are the nodes first read in that verse; `focus` is
    what the camera should frame for it.
    """

    def __init__(self, ot=True, layout=None):
        self.tree = CT.build(ot=ot)
        self.root = self.tree.root
        lay = LAYOUTS[layout or LAYOUT]
        lay[0](self.root, notes=False)
        lay[1](self.root, 0, 0)

        self.by_src = {}
        for n in walk(self.root):
            if n.src is not None:
                self.by_src[n.src] = n
        self.nodes = list(walk(self.root))
        self.world_box = (min(n.x for n in self.nodes),
                          min(n.y for n in self.nodes),
                          max(n.x + n.w for n in self.nodes),
                          max(n.y + n.h for n in self.nodes))

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
        walked, 9:35-44 retells the house of Saul from chapter 8 — and those
        fall back to the name. Chronicles has ten Azariahs, so a name alone
        is a guess.

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
        what its neighbours in the same passage already do.

        Only the fallback goes. A row the tree DID lift still resolves
        through its `src` stamp, so if the chart ever grows a town the verse
        finds it.
        """
        fixed, open_ = [], []
        home = self.scene_home.get((ch, title))
        for k in idxs:
            n = self.by_src.get((ch, title, k))
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
            fixed_ns = [chosen[k] for k, _ in fixed] or list(chosen.values())
            sibs, kin = set(), set()
            for m in fixed_ns:
                if m.parent is not None:
                    sibs.update(m.parent.kids)
                    kin.add(m.parent)
                kin.update(m.kids)
            sibs.difference_update(fixed_ns)

            def rank(c):
                return 0 if c in sibs else 1 if c in kin else 2

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
        # Exact names first; then the halves of a doubled label, because the
        # tree renames a few people the scenes know by one name only —
        # "Abraham" there is "Abram · Abraham" here, and 1:28 was naming a
        # father the chart could not find.
        self.by_label, self.by_alias = {}, {}
        for n in self.nodes:
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
                    named = []
                    for n in self._resolve_verse(ch, title,
                                                 highlights.get(v, []),
                                                 rows, anchor,
                                                 scene.get("places")):
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
        """
        arriving = self.arrivals.get((ch, v)) or []
        lit = self.lit.get((ch, v)) or []
        core = arriving or lit
        if not core:
            return None, "quiet"
        box = None
        for n in core:
            b = node_box(n)
            box = b if box is None else _union(box, b)
        wide = box
        for n in core:
            if n.parent is not None:
                wide = _union(wide, node_box(n.parent))
        for n in lit:
            wide = _union(wide, node_box(n))
        if _fit(_grow_min(wide), pad=70)[0] >= READABLE:
            return _grow_min(wide), "tight"
        if _fit(_grow_min(box), pad=70)[0] >= READABLE:
            return _grow_min(box), "tight"
        return _grow_min(wide), "card"


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
    def fmt_s(v):
        return ("%.6f" % v).rstrip("0").rstrip(".")
    return (
        f'<g transform="translate({_fmt(t0[0])} {_fmt(t0[1])})">'
        f'<animateTransform attributeName="transform" '
        f'attributeType="XML" type="translate" values="{tvals}" '
        f'{mode} dur="{dur}s" begin="0s" fill="freeze"/>'
        f'<g transform="scale({fmt_s(s0)})">'
        f'<animateTransform attributeName="transform" '
        f'attributeType="XML" type="scale" values="{svals}" '
        f'{mode} dur="{dur}s" begin="0s" fill="freeze"/>'
        + "".join(els) + "</g></g>")


def _fade_group(els, begin, dur=GROW_DUR):
    return (f'<g opacity="0">{"".join(els)}'
            f'<animate attributeName="opacity" values="0;1" dur="{dur}" '
            f'begin="{begin}" fill="freeze" calcMode="spline" '
            f'keyTimes="0;1" keySplines="{EASE}"/></g>')


class VerseFrame:
    """One verse's SVG: the world seen through a moving camera."""

    # Per-frame, so a book whose wide shots are meant to show the WHOLE
    # tree can spend more on them (Matthew 1:1 and 1:17) without changing
    # what an ordinary verse costs.
    max_nodes = MAX_NODES
    veil_alpha = VEIL_ALPHA

    def __init__(self, world):
        self.world = world
        self.camera = Camera(world)
        self.read = set(world.context_nodes())

    def render(self, ch, v, scene, first):
        w = self.world
        focus, mode = w.focus_box(ch, v)
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
        # Text is carried wherever the viewer DWELLS: the frame the verse
        # ends on, and the frame it starts from — which is where they are
        # looking the instant the file loads. Giving text to the destination
        # frame alone made every verse open on bare boxes where the previous
        # verse had just written names (the 1:3 / 1:13 "blanking").
        text_frames = [_frame(cam, DETAIL_PAD)
                       for cam in (cam0, apex, cam1)
                       if cam[0] >= TEXT_MIN_SCALE]
        detail = _frame(cam1, DETAIL_PAD)
        skeleton = detail
        for cam in (cam0, apex):
            skeleton = _union(skeleton, _frame(cam, SKELETON_PAD))

        # Everything the camera passes over, capped: a wide pull-back can
        # otherwise sweep in half the canon.
        #
        # The budget is spent on the two frames the viewer DWELLS in — the
        # one the verse opens on and the one it lands on — before anything
        # else. Spending it all on "nearest the destination" emptied the
        # START frame of six chapter 9 verses outright: the file opened on
        # blank space, and the pull-out then revealed that it had been
        # pointed at nothing. Whatever budget is left over goes to the
        # in-between, nearest the destination first, which is only ever
        # context glimpsed in passing.
        shown = [n for n in w.nodes if _hits(node_box(n), skeleton)]
        if len(shown) > self.max_nodes:
            def near(cam, pool):
                cxx, cyy = cam[1], cam[2]
                return sorted(pool, key=lambda n: math.hypot(
                    n.x + n.w / 2 - cxx, n.y + n.h / 2 - cyy))

            keep = set(arriving) | set(lit)
            for cam, share in ((cam0, DWELL_SHARE), (cam1, 1.0)):
                fr = _frame(cam, DETAIL_PAD)
                room = int(self.max_nodes * share) - len(keep)
                if room > 0:
                    keep |= set(near(cam, [n for n in shown
                                           if n not in keep
                                           and _hits(node_box(n), fr)])[:room])
            room = self.max_nodes - len(keep)
            if room > 0:
                keep |= set(near(cam1, [n for n in shown
                                        if n not in keep])[:room])
            shown = [n for n in w.nodes if n in keep]

        c = SvgCanvas(W, H, bg=BG)
        # Four layers, and the order is the point: a connector drawn while
        # walking the tree crosses boxes that were drawn earlier, so all the
        # lines go down first and all the boxes sit on top of them. A line
        # behind a name reads; a line across one does not.
        lines, lines_new, boxes, boxes_new = [], [], [], []
        for n in shown:
            nbox = node_box(n)
            full = any(_hits(nbox, fr) for fr in text_frames)
            state = ("new" if n in arriving else
                     "lit" if n in lit else
                     "read" if n in self.read else "ahead")
            self._draw(lines, lines_new, boxes, boxes_new, n, state, full,
                       dur)

        lines[0:0] = self._extra_world_els(ch, v, dur, shown)

        named = list(w.lit.get((ch, v), []))       # verse reading order
        self.read |= arriving

        els_all = lines + lines_new + boxes + boxes_new
        veil_screen = []
        if mode == "card" and named and cam1[0] < READABLE:
            # the camera group has to be built first: the veil's mask holes
            # reuse its transform tracks so they ride the same flight
            probe = self._camera_group(cam0, cam1, arc_at, dur, [])
            rings, veil_screen = _ride_els(
                named, _cam_schedule(cam0, cam1, arc_at, dur), cam1[0],
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
        """Box and name for one node, in one of the three looks."""
        alpha, edge_kind, wdt, tint = self.LOOK[look]
        col = accent(n)
        edge = HL if edge_kind == "hl" else dim(col, alpha)
        sub = SvgCanvas(W, H)
        sub.rect(n.x, n.y, n.w, n.h, fill=dim(PANEL, alpha), stroke=edge,
                 width=wdt, rx=12 if n.kind == "woman" else 4)
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
        """
        if state != "new":
            lines.append(self._connector(n, state))
            boxes.extend(self._node_els(n, state, full))
            return
        gdur, gbegin = _grow_timing(dur)
        lines.append(self._connector(n, "ahead"))
        boxes.extend(self._node_els(n, "ahead", full))
        lines_new.append(self._connector(n, "lit", gdur, trace=True))
        boxes_new.append(_fade_group(self._node_els(n, "lit", full),
                                     gbegin, gdur))

    def _connector(self, n, look, gdur=None, trace=False):
        p = n.parent
        if p is None:
            return ""
        alpha = {"lit": 0.95, "read": 0.8, "ahead": 0.2}[look]
        col = dim(FEMALE if n.link == "wife" else SAND_DIM, alpha)
        px, py = p.x + p.w / 2, p.y + p.h
        nx, ny = n.x + n.w / 2, n.y
        bus = (py + ny) / 2
        pts = [(px, py), (px, bus), (nx, bus), (nx, ny)]
        sub = SvgCanvas(W, H)
        if trace:
            sub.traced(pts, col, 1.6, dur=gdur or GROW_DUR)
        else:
            sub.polyline(pts, col, 1.5,
                         dash="4 4" if n.link == "dash" else None)
        return "".join(sub._els)

    # -- the cutaway card ---------------------------------------------------

    CARD_W_MAX = 880

    def card_pos(self, cw, ch_, pad):
        """Where the cutaway card sits. Bottom-centre unless a book moves
        it — Matthew's two panorama verses put it out of the way of the
        highlights, which on those shots run down the middle of the sheet."""
        return (W - cw) / 2, VIEW_BOT - ch_ - pad * 2 - 10

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
        def anc(a, b, k=3):
            q = b.parent
            while q is not None and k:
                if q is a:
                    return True
                q, k = q.parent, k - 1
            return False

        head, rest = named[0], named[1:]
        star = (len(named) > 2 and all(anc(head, n) for n in rest)
                and not any(anc(a, b) for a in rest for b in rest
                            if a is not b))

        BH = 27                                    # box height on the card

        def bw(n):
            fnt = F_NODE_B if n.kind in ("king", "priest") else F_NODE
            w_ = fnt.getlength(n.label) + 2 * PAD_X
            return w_ + (16 if n.kind == "king" else 0)

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
            rows, row, x = [], [], 0.0
            for n in rest:
                step = bw(n) + (14 if row else 0)
                if row and x + step > self.CARD_W_MAX:
                    rows.append(row)
                    row, x, step = [], 0.0, bw(n)
                row.append((n, x + (14 if row else 0)))
                x += step
            if row:
                rows.append(row)
            row_ws = [r[-1][1] + bw(r[-1][0]) for r in rows]
            cw = max(max(row_ws), bw(head))
            ch_ = BH + 22 + len(rows) * BH + (len(rows) - 1) * 24
            pad = 16
            px, py = self.card_pos(cw, ch_, pad)
            sub.rect(px - pad, py - pad, cw + 2 * pad, ch_ + 2 * pad,
                     fill=BG + (234,), stroke=dim(SAND_DIM, 0.95),
                     width=1.1, rx=10)
            hx = px + cw / 2 - bw(head) / 2
            draw_box(sub, head, hx, py)
            bus = py + BH + 11
            sub.line((px + cw / 2, py + BH), (px + cw / 2, bus),
                     dim(SAND_DIM, 0.95), 1.5)
            y = bus + 11
            prev_rail = None
            for ri, r in enumerate(rows):
                rw = r[-1][1] + bw(r[-1][0])
                rx0 = px + (cw - rw) / 2
                cxs = [rx0 + off + bw(n) / 2 for n, off in r]
                by = y - 11
                if ri == 0:
                    sub.line((min(cxs + [px + cw / 2]), bus),
                             (max(cxs + [px + cw / 2]), bus),
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
            rows, row, x = [], [], 0.0
            for i2, n in enumerate(named):
                joint = None
                if row:
                    joint = "line" if anc(named[i2 - 1], n) else "dot"
                gap = 22 if joint else 0
                step = bw(n) + gap
                if row and x + step > self.CARD_W_MAX:
                    rows.append(row)
                    row, x, joint, step = [], 0.0, None, bw(n)
                row.append((n, x + gap, joint))
                x += step
            if row:
                rows.append(row)
            row_ws = [r[-1][1] + bw(r[-1][0]) for r in rows]
            cw = max(row_ws)
            ch_ = len(rows) * BH + (len(rows) - 1) * 16
            pad = 16
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
        def fmt_s(v):
            return ("%.6f" % v).rstrip("0").rstrip(".")

        pure_pan = abs(cam1[0] - cam0[0]) <= 1e-9
        if pure_pan:
            cams, times = [cam0, cam1], [0.0, 1.0]
            mode_extra = 'calcMode="spline" keySplines="%s"' % EASE
        else:
            n = max(6, int(round(dur * CAM_FPS)))
            cams = [arc_at(_smooth(i / n)) for i in range(n + 1)]
            cams[0], cams[-1] = cam0, cam1
            times = [i / n for i in range(n + 1)]
            mode_extra = ""

        cams = [(float(fmt_s(sc)), cx_, cy_) for sc, cx_, cy_ in cams]
        tvals = ";".join("%s %s" % (_fmt(_cam_T(cm)[0]), _fmt(_cam_T(cm)[1]))
                         for cm in cams)
        svals = ";".join(fmt_s(cm[0]) for cm in cams)
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
