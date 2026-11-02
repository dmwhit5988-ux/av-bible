"""The stage of Genesis 2-3: the card the garden is hosted on, everything both chapters share, and
the build.

garden_art.py is the place and svg_figures.py the people; genesis2_garden.py and genesis3_garden.py
are the story, one function a verse. This module is what stands between them.

The host
    One svg_scene_card card with no map under it: town_xy (0, 0), S 1, so world px are card px and a
    camera is (zoom, x, y). `Stage` subclasses garden_art's card and draws its own group, with no
    clip and no border, because the card is the world, its edge is never in frame, and a clip over
    everything is paint on every frame. The shared card in svg_scene_card.py doesn't change for any
    of this: Joshua's and Acts' bytes hang on it.

Marks and shots
    x says where anything is, east is right, and feet go on `gy(x)`. The marks below are the
    stage's, and SHOTS are the cameras, (x, y, zoom), named. A frame the viewer has seen before is
    the same shot by name, so that what is gone from it shows: `pair`, `every`, `plot`, `fruit` and
    `alone` must stay exact. `Verse.settle` arrives a little wide of a shot and creeps in to its
    exact value, and `Verse.creep` is a hold that doesn't stand still.

A verse
    A function registered with @verse(ref), taking its Verse and the Stage. It says the camera's
    legs on v, the cast's events on the card, and what is drawn by hand as functions of the Flight:

        @verse("2:18")
        def alone(v, c):
            v.cut("to_fruit", 1.0)
            v.cam("alone", 1.0, 6.3)
            v.scene = lambda fl: garden(fl, v.ref)
            v.over.append(lambda fl: fruit_plate(fl))

    `v.t(word, today, lead, n)` is a beat on its cue: `lead` before the word is said, from
    narration_clock against the verse's MP3, or `today`, what that comes to on today's MP3, when
    there's no clock. All of a verse's cues are taken as its function runs, none as it draws, so a
    `say` that records them sees every one. A verse opens on the last verse's rest. `v.under` is
    drawn under the cast and `v.over` over it and over Scene.front. A verse with `v.plan` hangs the
    side view over the plan, and `v.plan_only` is on the plan alone.

The cast
    `person_actor` is a person in profile. Their keyline and contour inherit a stroke-width that
    rides the camera (`key_w`, `body_w`), so a figure's lines stay thin at zoom 6. An event's pose
    carries on until changed, and `_flip` says which way they face. A change of the arms or the head
    alone is a limb, written with `_morph`: the drawing's own paths animate through a mid-pose by the
    joints' angles, with no fade at all (`Stage._morph_drawing`), since an arm faded in over the old
    one would be a second arm, seen through. Any other pose is a new look fading in over the old, so
    a body is never see-through, and one that turns them round, takes them down or up, or sets them
    walking or stops them, comes in at once (TURN_S), since the two barely overlap. A walk is `walk`
    and `walk2` alternating for the length of a move and no longer. A move written (dx, dy, STEADY)
    goes at a steady speed, so that it carries over a verse's seam without slowing and its feet
    don't skate. `paint` is live, dust, bone or stone; stone is what is only spoken of.

Plates
    What a camera at z 5 to z 9 sees is a drawing in world px with its own opaque ground (`plate`).
    It comes and goes by an edit: the camera holds on the world, and on a word it is on the plate's
    rest at once, and out of it the same way (`Verse.cut`), never by a dissolve, which would show a
    person through it, nor by a zoom that swaps the picture under it half way. So the world under
    it can be anywhere: a plate is hung by the shots the verse cuts between, since the scenery a
    verse draws reaches as far as its camera's keys. While a plate is in, the scene under it is
    switched off (`VerseFlight.scene_visibility`), so that a close-up costs only its own drawing.

The ground
    `garden(fl, ref)` is the planted side view as a verse's place in the story has it: where the
    water runs, what has been taken, what stays after the curse, the thorns, the leaves left at
    their feet, and the light going once at 3:8. It is the only place those rules are. It is
    trimmed to what the verse's camera can see (`seen`): anything else it draws is paid for on
    every frame that anything moves.

The build
    `build_story()` imports the chapters' modules and runs their verses in order on one Stage,
    because a verse's state is what the verses before it left. `write_story()` draws the whole
    story, puts it through garden_qc.py, and writes both chapters' files through
    generate_tabernacle.out_path, or nothing at all if anything has failed: either generator writes
    both. Importing this runs nothing and writes nothing.
"""

import functools
import importlib
import math
import os
import random
import re
from collections import namedtuple

import soundfile as sf

import config
import garden_art as G
import narration_clock
import passages
import svg_figures as F
import svg_map_camera as C
import svg_scene_card as SC
from generate_tabernacle import feathered_wing, out_path
from svg_surface import SvgCanvas, _fmt

BOOK = "Genesis"
CHAPTERS = {2: "genesis2_garden", 3: "genesis3_garden"}
TITLE = "The Garden in Eden — Genesis {}"
HL, NAME_INK, PXU = G.HL, G.NAME_INK, G.PXU
HALO = (22, 24, 20)
SIDE_KEEP = ("kf", "fn", "sa")      # what a verse places by hand on the side view
# the camera before the first verse, over the heavens
OPENING = (.07, 1200, -2300)
STEADY = "steady"           # the third item of a move at a steady speed
SEEN_MARGIN = 8             # world px round a frame that a trim keeps: the keys are not every frame


def cv(ref):
    """"2:15" -> (2, 15)."""
    c, v = ref.split(":")
    return int(c), int(v)


def clamp(v):
    return max(0.0, min(1.0, v))


def gy(x, woman=False):
    """Where a person's feet go on the people's line."""
    return G.ground_y(x) + (6 if woman else 2)


def seen(fl, hung=False):
    """All of the side view a flight's camera can see, (x0, y0, x1, y1), world px: the frame's edges
    over its keys, but for a verse `hung` in the plan its keys on the plan, when the side view has
    gone."""
    a = [C.visible_world(c, SEEN_MARGIN) for c in fl.cams if not hung or G.side_op(c[0]) > 0]
    return (min(q[0] for q in a), min(q[1] for q in a), max(q[2] for q in a), max(q[3] for q in a))


# ---------------------------------------------------------------------------
# The clock
# ---------------------------------------------------------------------------

_WORD = re.compile(r"[\w’'\-]+")


def chapter_refs(chapter):
    return [f"{chapter}:{v}" for v in passages.verse_numbers(BOOK, chapter)]


def _mp3(ref):
    c, v = cv(ref)
    return os.path.join(str(config.WEB_AUDIO_DIR), f"{BOOK}_{c}_{v}.mp3")


def verse_text(ref):
    c, v = cv(ref)
    return next(text for num, text in passages.load_chapter(BOOK, c).verses if int(num) == v)


@functools.cache
def verse_dur(ref):
    """The narration's length, seconds."""
    return round(sf.info(_mp3(ref)).duration, 2)


@functools.cache
def occurrences(ref, word):
    """Where the verse's text has `word`, in order, as offsets into it. A capital means that very
    word, capital and all; a small letter matches the word in either case. Only the whole word:
    "he" is never "her", and a misspelt cue finds nothing."""
    words = [(m.group(0), m.start()) for m in _WORD.finditer(verse_text(ref))]
    if word[0].isupper():
        return [at for w, at in words if w == word]
    return [at for w, at in words if w.lower() == word]


@functools.cache
def _clock(ref):
    return narration_clock.clock(verse_text(ref), _mp3(ref))


def say(ref, word, n=0, lead=.1):
    """When `word` (the nth time in the verse) is said, less `lead` seconds, or None if the verse
    has no clock. KeyError if the verse doesn't say it that often: a misspelt cue must not build."""
    hits = occurrences(ref, word)
    if n >= len(hits):
        raise KeyError((ref, word, n))
    clock = _clock(ref)
    if clock is None:
        return None
    return round(max(0.0, round(clock(hits[n]), 2) - lead), 2)


def cue(say, ref, word, today, lead=.1, n=0):
    """When a beat answering `word` starts: `lead` before it's said, or `today` (today's MP3) when
    there's no clock."""
    t = say(ref, word, n, 0.0) if say else None
    return today if t is None else round(max(0.0, t - lead), 2)


# ---------------------------------------------------------------------------
# The marks. x is the only thing that says where anything is
# ---------------------------------------------------------------------------

MF = G.MAN_FIRST                    # he is formed here, on Eden's dry shoulder
LIFE, KNOW = G.LIFE_XY, G.KNOWLEDGE_XY
# the fruit a hand can reach: the stem's top
FRUIT_X, FRUIT_Y = G.knowledge_reach()[0][1:3]
FRUIT_C = (FRUIT_X, FRUIT_Y + 10.6)                      # its body's middle
FRUIT4, FRUIT5 = G.knowledge_reach()[1], G.knowledge_reach()[2]

M0, W0 = -150.0, -86.0              # the pair's marks: 2:23, 2:25, 3:1
W_REACH = -68.0                     # she can reach the low fruit
M_BY = -128.0                       # he stands by her to take it, 3:6
M_APART, W_APART = -150.0, -48.0    # 3:7: the same camera as 2:25, a little further apart
M_REACH = -70.0                     # 2:17: where he stands to reach, and stop short
SLEEP_X = -190.0                    # 2:17's end to 2:22
M_FIG = 262.0                       # 2:16: he eats from the near fig, facing west
M_PLOT = 620.0                      # 2:15, and the trial's mark, 3:12-3:22
SHOOT_X = 652.0                     # what he raises at 2:15, and what wilts at 3:17
HIDE_M, HIDE_W = 985, 1048          # behind the shrubs, 3:8
M_OUT = 812.0                       # 3:10
W_OUT, W_FRONT, W_T, W_RULE = 805.0, 500.0, 520.0, 558.0    # 3:12, 3:13, 3:15, 3:16
HEAD_X = 430.0                      # the serpent's nose at the end of 3:14
CH_W, CH_E, WHEEL_X = 2380, 2660, 2520      # 3:24
DIG_X = 2620.0                      # the stone man, 3:17-19
LEST_X = -350.0                     # the stone man at the tree of life, 3:22, facing east
GO_M, GO_W = 1620.0, 1570.0         # where they are as the plate of 3:22 lifts: he leads


def on_him(x, y):
    """Where a point of svg_figures.lying's drawing is, as he sleeps, in world px."""
    return SLEEP_X + x * PXU, gy(SLEEP_X) - y * PXU


SLIT_UNITS = ((-20, 8.6), (1.6, 2.6))               # the line on his side, 2:21: its two ends
SLIT = (on_him(*SLIT_UNITS[0]), on_him(*SLIT_UNITS[1]))
RIB_FROM = (SLIT[0][0] + 1, SLIT[0][1] - 1.8)     # where the rib's knuckle starts, inside him
RIB_AT = (RIB_FROM[0], 1411.0)      # where the rib lies, at his side
W_RISE = (RIB_AT[0] + 13, gy(RIB_AT[0] + 13, True) - 12)    # she rises there, behind him
ACROSS_Y = 1652                     # the near bank, on the viewer's side of the river: 2:24
SINK = 9.0                          # how far their heads go down behind the shrub, 3:9
WALK_V = 155.0                      # a walk's one pace, world px/s
# A verse that opens on a plate's rest and cuts out of it hangs the plate by the shot it cuts to,
# since the scenery a verse draws reaches as far as its camera's keys (`seen`). 3:20 opens on the
# mound's rest, hung here under its camera as `mound` has it, by `eve`
MOUND_HUNG = (810, 1397)
# 3:19's mound, where he sank, on a whole px as the hung one is, so that the two draw alike
MOUND_Y = round(gy(DIG_X))
# 3:23 opens on the spray's rest, hung here under its camera as `spray` has it, in clear sky over
# the worn way, by `going`
SPRAY_HUNG = (1990, 900)
HAND_OUT = (-112, 46)               # how far her hand goes, out of the fruit's frame, 3:3


# Hand in hand at the pair's marks she stands a step lower than he does, on ground that falls to the
# east, so her arms come up to his hands where his go down to hers: her "join", in svg_figures'
# units, her near hand on his
HER_JOIN = ([(0.5, 76), (12.8, 66.7), (28.3, 70.1)], [(-0.5, 76), (10.8, 64.7), (25.3, 68.1)])


def arms_of(woman, arms):
    """A pose's arms as svg_figures' chains, (near, far): SIDE_ARMS', but hers hand in hand."""
    if not isinstance(arms, str):
        return arms
    return HER_JOIN if woman and arms == "join" else F.SIDE_ARMS[arms]


def hand_xy(woman, arms, x, y, flip=1):
    """Where a person's near wrist is, in world px, standing at (x, y), and the direction the
    forearm runs there (degrees, screen, 0 = east)."""
    k = F.UNIT["woman" if woman else "man"]
    a, b = arms_of(woman, arms)[0][-2:]
    ang = math.degrees(math.atan2(-(b[1] - a[1]), flip * (b[0] - a[0])))
    return x + flip * b[0] * k * PXU, y - b[1] * k * PXU, ang


def p_at(woman, arms, x, flip=1):
    """Where the near hand's middle is, in world px."""
    wx, wy, ang = hand_xy(woman, arms, x, gy(x, woman), flip=flip)
    a = math.radians(ang)
    return wx + 2.4 * math.cos(a), wy + 2.4 * math.sin(a)


def fruit_on(woman, arms, x, flip=1):
    """Where the fruit's origin (its stem's top) goes, for it to sit in that hand."""
    hx, hy = p_at(woman, arms, x, flip)
    return hx + flip * 2.0, hy - 11.5


# ---------------------------------------------------------------------------
# The serpent's road: along the underside of the crown from its east side, past the trunk, along
# the west bough, out past its tip into clear air, over and down to the ground, then east along
# it. One road, so a verse only says how far along it the nose is
# ---------------------------------------------------------------------------

SNAKE_BODY, SNAKE_DEEP = (150, 142, 70), (50, 50, 26)


def dense(pts, step=6.0):
    """A dense polyline along a Catmull-Rom curve through pts."""
    sm = F.smooth(pts, closed=False, n=8)
    out = [sm[0]]
    for p in sm[1:]:
        if math.hypot(p[0] - out[-1][0], p[1] - out[-1][1]) >= step:
            out.append(p)
    if out[-1] != sm[-1]:
        out.append(sm[-1])
    return out


def poly_len(pts):
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))


def poly_d(pts):
    return "M" + " ".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def _crawl():
    pts, x = [], 10.0
    while x <= HEAD_X:
        pts.append((x, G.ground_y(x) + 8 + 3.6 * math.sin((x + 62) / 40)))
        x += 20
    return pts


_CRAWL = _crawl()
_CX, _CY = _CRAWL[-1]
# where he lies as 3:1 opens, under the east side of the crown, beyond the frame 2:25 rests on: he
# comes into sight by moving, and never fades in
_UNDER_CROWN = [(668, 1146), (638, 1146), (608, 1148), (578, 1152), (548, 1154), (518, 1152),
                (490, 1154), (462, 1160), (436, 1170), (412, 1180), (392, 1188)]
ROAD = dense(_UNDER_CROWN, 7.0)[:-1] + dense(
    [(392, 1188), (345, 1212), (305, 1172), (262, 1168), (222, 1138), (175, 1150),
     (130, 1140), (90, 1170), (58, 1184), (36, 1222), (14, 1232), (8, 1254), (-8, 1270),
     (-30, 1264), (-48, 1262), (-60, 1268), (-60, 1284), (-50, 1302), (-40, 1336),
     (-26, 1370), (-6, 1404)]
    + _CRAWL + [(_CX + 11, _CY - 4), (_CX + 21, _CY - 18), (_CX + 26, _CY - 36),
                (_CX + 28, _CY - 52)], 7.0)
# His head, svg_figures.viper_head, in its paint: a step darker than the body, a dark cap, and the
# chevron on his nape a dull light tone of his body's, where it reads as a marking and nothing else
_VIPER = {mat: pts for _kind, pts, mat in F.viper_head(s=PXU)}
_VIPER_PAINT = {"muzzle": (120, 114, 56), "hair": (58, 56, 30), "horn": (176, 168, 110)}
SNOUT = max(x for x, _y in _VIPER["muzzle"])    # how far his snout is ahead of his nose's place


class Snake2:
    """The serpent on one road: a path he slides along, tail behind. `body` is his length. The head
    rides an <animateMotion rotate="auto">; the body is a set of dashes on the same path, thick near
    the head and thin at the tail, whose offsets move in step. Keys are [(t, s)], s how many px
    along the road the nose is. The head is a real viper's, 26 px long, jaw 12 wide, neck 8, snout
    6, in world px whatever the zoom, with no eye. Local -y is the top of the head, and going west
    that is upside down under rotate="auto", so it turns over where the road goes straight down."""

    def __init__(self, pts, body, girth):
        self.pts, self.body, self.girth = pts, body, girth
        self.L = poly_len(pts)

    def at(self, s):
        """(x, y, heading in degrees) at s px along the road."""
        acc = 0.0
        for a, b in zip(self.pts, self.pts[1:]):
            L = math.hypot(b[0] - a[0], b[1] - a[1])
            if acc + L >= s or b is self.pts[-1]:
                u = (s - acc) / L if L else 0
                return (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u,
                        math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])))
            acc += L
        return self.pts[-1][0], self.pts[-1][1], 0.0

    def _west(self, s):
        return math.cos(math.radians(self.at(max(0.0, s))[2])) < 0

    def head_svg(self, flicks=()):
        deep = G._hex(SNAKE_DEEP)

        def d(mat):
            return G._d([(x, -y) for x, y in _VIPER[mat]])
        mouth = "L".join(f"{x:g} {-y:g}" for x, y in _VIPER["rule"])
        o = (f'<path d="{d("muzzle")}" fill="{G._hex(_VIPER_PAINT["muzzle"])}" stroke="{deep}" '
             'stroke-width=".9" stroke-linejoin="round"/>'
             f'<path d="{d("hair")}" fill="{G._hex(_VIPER_PAINT["hair"])}"/>'
             f'<path d="{d("horn")}" fill="{G._hex(_VIPER_PAINT["horn"])}"/>'
             f'<path d="M{mouth}" fill="none" stroke="{deep}" stroke-width=".55"/>')
        if flicks:
            an = "".join('<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.2;.65;1" '
                         f'begin="{t:.2f}s" dur=".42s" fill="freeze"/>'
                         for t in flicks)
            o = (f'<g opacity="0">{an}<path d="M20 .4h7l3 -2.2M27 .4l3 2" fill="none" '
                 'stroke="#d05a3c" stroke-width=".7"/></g>') + o
        return o

    def svg(self, keys, flicks=()):
        ts, ss = [k[0] for k in keys], [k[1] for k in keys]
        t0, t1 = ts[0], ts[-1]
        dur = max(.01, t1 - t0)
        kt = ";".join(f"{(t - t0) / dur:.4f}" for t in ts)
        spl = ";".join([".42 0 .58 1"] * (len(ts) - 1))
        moving = len(set(ss)) > 1 and dur > .02
        d = poly_d(self.pts)
        L, B, W = self.L, self.body, self.girth
        out = ""
        # tail to head, each layer a dash of its own length ending at the nose
        layers = [(1.0, W * .42, 0), (.72, W * .66, 0), (.46, W * .9, 9), (.24, W, 15)]

        def dash(frac, w, stroke, back=0.0):
            len_ = B * frac
            vals = ";".join(f"{len_ - s + back:.1f}" for s in ss)
            a = (f'<animate attributeName="stroke-dashoffset" values="{vals}" keyTimes="{kt}" '
                 f'begin="{t0:.2f}s" dur="{dur:.2f}s" '
                 f'fill="freeze" calcMode="spline" keySplines="{spl}"/>') if moving else ""
            return (f'<path fill="none" d="{d}" stroke="{G._hex(stroke)}" stroke-width="{w:.2f}" '
                    f'stroke-dasharray="{len_:.1f} {L + B * 2:.1f}" '
                    f'stroke-dashoffset="{len_ - ss[0] + back:.1f}">{a}</path>')
        for frac, w, bk in layers:
            out += dash(frac, w + 1.8, SNAKE_DEEP, bk)
        for frac, w, bk in layers:
            out += dash(frac, w, SNAKE_BODY, bk)
        # his bands: a run of short dashes along the body, which slide with it
        on, off = 3.4, 8.2
        n = int(B * .62 / (on + off))
        tot = n * (on + off)
        arr = " ".join([f"{on} {off}"] * (n - 1)) + f" {on} {L + B * 2:.0f}"
        vals = ";".join(f"{tot - s + 13:.1f}" for s in ss)
        a_ = (f'<animate attributeName="stroke-dashoffset" values="{vals}" keyTimes="{kt}" '
              f'begin="{t0:.2f}s" dur="{dur:.2f}s" fill="freeze" '
              f'calcMode="spline" keySplines="{spl}"/>') if moving else ""
        out += (f'<path fill="none" d="{d}" stroke="{G._hex(SNAKE_DEEP)}" '
                f'stroke-width="{W * .62:.2f}" stroke-linecap="butt" stroke-dasharray="{arr}" '
                f'stroke-dashoffset="{tot - ss[0] + 13:.1f}">{a_}</path>')
        head = self.head_svg(flicks)
        if not moving:
            x, y, ang = self.at(ss[0])
            sc = ' scale(1 -1)' if self._west(ss[0]) else ""
            return (out + f'<g transform="translate({x:.1f} {y:.1f}) '
                          f'rotate({ang:.1f}){sc}">{head}</g>')
        kp = ";".join(f"{min(1, max(0, s / L)):.5f}" for s in ss)
        motion = (f'<animateMotion path="{d}" keyPoints="{kp}" keyTimes="{kt}" begin="{t0:.2f}s" '
                  f'dur="{dur:.2f}s" fill="freeze" '
                  f'calcMode="spline" keySplines="{spl}" rotate="auto"/>')
        # which way up, along the way
        turns = []
        was = self._west(ss[0])
        for a, b, sa, sb in zip(ts, ts[1:], ss, ss[1:]):
            for i in range(1, 25):
                u = i / 24
                w = self._west(sa + (sb - sa) * u)
                if w != was:
                    turns.append(((a + (b - a) * u - t0) / dur, w))
                    was = w
        sc0 = "1 -1" if self._west(ss[0]) else "1 1"
        ta = ""
        if turns:
            vals_ = [sc0] + ["1 -1" if w else "1 1" for _u, w in turns]
            kts = ["0"] + [f"{u:.4f}" for u, _w in turns]
            ta = ('<animateTransform attributeName="transform" type="scale" '
                  f'values="{";".join(vals_)}" keyTimes="{";".join(kts)}" calcMode="discrete" '
                  f'begin="{t0:.2f}s" dur="{dur:.2f}s" fill="freeze"/>')
        return out + f'<g>{motion}<g transform="scale({sc0})">{ta}{head}</g></g>'


SN = Snake2(ROAD, body=214, girth=8.4)


def s_at(pt):
    """How far along the road the point of it nearest `pt` is."""
    best, acc, s = 1e9, 0.0, 0.0
    for a, b in zip(ROAD, ROAD[1:]):
        d = math.hypot(a[0] - pt[0], a[1] - pt[1])
        if d < best:
            best, s = d, acc
        acc += math.hypot(b[0] - a[0], b[1] - a[1])
    return s


S_IN = s_at((448, 1164))            # beyond the frame of 2:25, all of him, as 3:1 opens
S_NAMED = s_at((290, 1170))         # 3:1: out past the trunk, his head by his name as it is said
# in clear air, at the height of a face and away from the low leaves
S_OUT = s_at((-48, 1262))
S_CLOSE = s_at((-60, 1276))         # 3:4: down by her face
S_FELL = s_at((215, G.ground_y(215) + 8))
S_END = s_at((_CX, _CY))
S_REAR = S_END + 58
HEAD_AT = SN.at(S_END)


def snake(keys, flicks=(), fade=None, gone=None):
    """The serpent at keys [(t, s)], or resting at s."""
    o = SN.svg([(0, keys)] if isinstance(keys, (int, float)) else keys, flicks)
    if fade or gone:
        an = (C.fade(*fade) if fade else "") + (C.fade(gone[0], gone[1], out=True) if gone else "")
        return f'<g{" opacity=" + chr(34) + "0" + chr(34) if fade else ""}>{an}{o}</g>'
    return o


# ---------------------------------------------------------------------------
# The shots: (x, y, zoom), the middle of the frame. A man is 110 x zoom px
# ---------------------------------------------------------------------------

_HANDS_X = (hand_xy(False, "join", M0, gy(M0))[0]
            + hand_xy(True, "join", W0, gy(W0, True), flip=-1)[0]) / 2
_HANDS_Y = (hand_xy(False, "join", M0, gy(M0))[1]
            + hand_xy(True, "join", W0, gy(W0, True), flip=-1)[1]) / 2
SPRAY_X, SPRAY_Y = G.TWIG_FRUIT[0] * 1.0, G.TWIG_FRUIT[1] * 1.0

SHOTS = {
    "heavens": (1200, 300, .07), "heavens2": (1150, 250, .078), "descent": (400, 950, .115),
    "landline": (0, 1190, .17), "whole": (0, 1000, .17),
    "foot_life": (-420, 1320, 1.0), "foot_know": (370, 1320, 1.0), "sky_dry": (-200, 880, .34),
    "pair": (-90, 1312, 1.0),                   # 2:5's end, 2:25, 3:7; 3:8's frame
    "mist_low": (-900, 1250, .36),
    "handful": (MF[0] + 2, MF[1] - 5, 7.0), "comes_up": (MF[0] + 4, MF[1] - 44, 2.5),
    "head_chest": (-1690, 1320, 6.0), "formed": (MF[0], MF[1] - 112, 1.0),
    "garden_rises": (-880, 1180, .42), "garden_on": (-800, 1180, .42),
    "every": (-20, 1176, .5),                   # 2:9's rest, 2:16, 3:2, 3:22
    "tilt": (-260, 510, .38), "course_head": (-1450, 1180, .165), "course": (-600, 1180, .165),
    "plan": (3000, 1400, .0575), "pishon": (6100, -1500, .105), "gold": (7400, -1520, .4),
    # these two leave gold's name, held from 2:11, wholly over the frame's top: it is never cut
    "bdellium": (8780, -1560, .31), "gihon": (5400, 850, .16), "cush": (8100, 850, .16),
    "hiddekel": (5900, 1900, .2), "tower": (5840, 1640, .4),
    "put": (470, 1310, .9),
    "plot": (640, 1312, 1.4),                   # 2:15, 3:17
    "to_fig": (185, 1290, 3.5), "to_fruit": (-60, 1300, 1.3),
    "fruit": (FRUIT_X - 12, FRUIT_Y + 6, 9.0),  # 2:17, 3:3, 3:6
    "alone": (-100, 1100, .4),                  # 2:18, 2:20's end
    "naming": (-110, 1262, .6),
    "sleep": (-198, 1336, 1.45), "chest": (-240, 1373, 6.5), "made": (-126, 1330, 1.2),
    "hands": (_HANDS_X, _HANDS_Y - 2, 8.2), "names": (-120, 1326, 1.25), "flesh": (-110, 1322, .82),
    "crown": (225, 1190, 1.3), "bough": (70, 1232, 1.6), "two_heads": (-62, 1272, 3.4),
    "she_fruit": (-50, 1300, 2.0), "her_face": (-32, 1296, 2.4), "tree_whole": (120, 1110, .56),
    # `mouth` is hips up: its foot is at about `two_heads`'
    "push": (-42, 1296, 2.4), "mouth": (-62, 1280, 4.0), "gives": (-100, 1332, 1.5),
    # hung in the air over the gap between their heads, by `pair`, which it cuts from and back to
    "stitch": (-125, 1090, 7.2), "hid_wide": (1015, 1272, .74),
    "found": (900, 1302, 1.02), "accused": (850, 1296, 1.26), "stem": (930, 1300, 9.0),
    "blame": (800, 1296, .98), "her": (700, 1296, 1.12), "she_points": (270, 1240, 1.2),
    "cursed": (150, 1264, .85), "crawl": (400, 1322, 1.0), "enmity": (540, 1322, 1.1),
    "heel": (HEAD_AT[0] - 2, HEAD_AT[1] - 28, 7.0), "pain": (580, 1296, 1.12),
    "rule": ((M_PLOT + W_RULE) / 2,
             (hand_xy(False, "reach", M_PLOT, gy(M_PLOT), flip=-1)[1]
              + hand_xy(True, "reach", W_RULE, gy(W_RULE, True))[1]) / 2 - 2, 8.2),
    "tree_again": (530, 1240, .62), "beyond": (2620, 1222, .95), "toil": (2620, 1218, 1.12),
    "return": (2620, 1266, 1.34), "mound": (DIG_X + 2, MOUND_Y - 5, 7.0),
    "eve": (810, 1320, .96), "coats": (590, 1296, 1.16), "life": (-330, 1238, .86),
    # on a whole px, as the hung spray of 3:23 is, so that the two draw alike
    "spray": (SPRAY_X - 12, round(SPRAY_Y + 8), 9.0), "going": (1900, 1240, .8),
    "going2": (2150, 1240, .8), "gate": (2640, 1202, .84), "last": (1040, 1124, .28),
}
STEM_DX, STEM_DY = SHOTS["stem"][0] - (FRUIT_X - 4), SHOTS["stem"][1] - (FRUIT_Y + 11)


def camera(shot):
    """A Flight's camera, (zoom, x, y), from a shot's name."""
    x, y, z = SHOTS[shot]
    return (z, x, y)


# ---------------------------------------------------------------------------
# The paints. Stone is what is only spoken of, the pair's own drawing, the head lighter than the
# body so that a cap and a beard never read as a hood. Bone is what she is as she rises, the rib's
# own colour. Dust is what he is before the breath: the ground's colour, a line a little lighter
# ---------------------------------------------------------------------------

_CLOTH = {"hair": ((96, 72, 50), (206, 188, 150), .8), "hair_line": (None, (84, 62, 44), .6),
          "hair_fine": ((96, 72, 50), (206, 188, 150), .3), "crease": (None, (120, 100, 74), .3),
          "fleece": ((104, 138, 66), (222, 228, 170), .7),
          "hide": ((122, 96, 66), (236, 222, 188), .9),
          "rule": (None, (70, 54, 38), .7)}
PAINTS = {
    "live": dict(_CLOTH, ink=(250, 238, 204), skin=(188, 166, 128), far=(150, 130, 100),
                 near=(196, 174, 136), key=(20, 24, 16)),
    "dust": dict(_CLOTH, ink=(160, 142, 110), skin=(112, 98, 74), far=(98, 84, 64),
                 near=(116, 102, 78), key=(58, 50, 38),
                 hair=((84, 72, 54), (130, 114, 88), .8),
                 fleece=((84, 72, 54), (130, 114, 88), .7)),
    "stone": dict(ink=(240, 234, 220), skin=(172, 164, 146), far=(146, 138, 122),
                  near=(182, 174, 156), key=(44, 40, 34),
                  hair=((204, 196, 178), (240, 234, 220), .8), hair_line=(None, (120, 112, 98), .6),
                  fleece=((150, 146, 124), (226, 222, 204), .7),
                  hide=((158, 150, 132), (236, 230, 214), .9),
                  rule=(None, (92, 86, 74), .7)),
    "bone": dict(ink=(250, 246, 232), skin=(228, 220, 198), far=(198, 190, 170),
                 near=(234, 226, 206), key=(96, 86, 66),
                 hair=((236, 228, 208), (250, 246, 232), .8), hair_line=(None, (140, 130, 110), .6),
                 fleece=((228, 220, 198), (250, 246, 232), .7),
                 hide=((228, 220, 198), (250, 246, 232), .9),
                 rule=(None, (140, 130, 110), .7)),
}
HER_SKIN = (204, 184, 148)          # a step lighter than his, so two hands are told apart


def person_layers(parts, flip=1, s=PXU, paint="live"):
    """(keyline svg, body svg): the keyline round the whole silhouette, then one contour per run of
    one material of skin, so that a near arm reads across the body. No stroke-width is written on
    the skin's contours or the keyline: they inherit the Stage's, which holds them near constant on
    the screen as the camera closes in. Hair and coverings keep their own thin lines."""
    pa = PAINTS[paint]
    tone = {"skin": pa["skin"], "skin_far": pa["far"], "skin_near": pa["near"]}

    def union(run):
        d = G._D(1)
        for k, dat, _m in run:
            if k == "dot":
                d.dot(dat[0] * s * flip, -dat[1] * s, dat[2] * s)
            elif k == "fill":
                pts = [(px * s * flip, -py * s) for px, py in dat]
                if G._area(pts) < 0:
                    pts = pts[::-1]
                if len(pts) > 11:
                    d.closed_curve(pts[::2])
                else:
                    d.poly(pts, True)
        return d.text()

    key = union([q for q in parts if q[0] != "line"])
    keyl = f'<path fill="{G._hex(pa["key"])}" stroke="{G._hex(pa["key"])}" d="{key}"/>'
    body = ""
    i, n = 0, len(parts)
    while i < n:
        mat = parts[i][2]
        j = i
        if mat in tone:
            while j < n and parts[j][2] == mat:
                j += 1
            d = union(parts[i:j])
            body += (f'<path fill="{G._hex(tone[mat])}" stroke="{G._hex(pa["ink"])}" d="{d}"/>'
                     f'<path fill="{G._hex(tone[mat])}" d="{d}"/>')
        else:
            while j < n and parts[j][2] not in tone:
                j += 1
            body += G.render(parts[i:j], pa, s=s, flip=flip, curve=False, prec=1)
        i = j
    return keyl, body


SHADOW_BACK = 26            # how far behind a standing person's feet their shadow reaches, units


def shadow(s=PXU):
    return (f'<path fill="#101810" fill-opacity=".5" d="M{-SHADOW_BACK * s:.0f} 1q{26 * s:.0f}-7 '
            f'{56 * s:.0f}-1q{-22 * s:.0f} 8 {-56 * s:.0f} 1z"/>')


def shadow_lying(s=PXU):
    """The ground under a person asleep, the length of him."""
    return (f'<path fill="#101810" fill-opacity=".5" d="M{-48 * s:.0f} 2q{50 * s:.0f}-6 '
            f'{102 * s:.0f}-1q{-48 * s:.0f} 9 {-102 * s:.0f} 1z"/>')


def key_w(z):
    """A keyline's width in world px at camera zoom z."""
    return 4.6 if z <= 1 else 4.6 / z ** .86


def body_w(z):
    """A contour's width in world px at camera zoom z."""
    return 2.1 if z <= 1 else 2.1 / z ** .82


def coarse(fl, fn):
    """(first value, an animate of stroke-width) over a fifth of the camera's keys, and the two
    either side of each cut."""
    vals = [fn(c[0]) for c in fl.cams]
    if fl.static or len({round(v, 3) for v in vals}) == 1:
        return f"{vals[0]:.3g}", ""
    n = len(vals) - 1
    idx = list(range(0, n, 5)) + [n]
    if getattr(fl, "cut_keys", None):
        idx = sorted(set(idx) | {i + d for i in fl.cut_keys for d in (0, 1)})
    v = ";".join(f"{vals[i]:.3g}" for i in idx)
    kt = ";".join(f"{i / n:.3f}" for i in idx)
    return (f"{vals[0]:.3g}", f'<animate attributeName="stroke-width" values="{v}" keyTimes="{kt}" '
                              f'dur="{fl.dur:.2f}s" begin="0s" fill="freeze"/>')


def stroke_groups(fl, key, body):
    """A person drawn by hand into a verse, with the Stage's widths."""
    k0, ka = coarse(fl, key_w)
    b0, ba = coarse(fl, body_w)
    return (f'<g stroke-width="{k0}" stroke-linecap="round" stroke-linejoin="round">{ka}{key}</g>'
            f'<g stroke-width="{b0}" stroke-linecap="round" stroke-linejoin="round">{ba}{body}</g>')


_POSE_ONLY = ("paint", "_flip", "per", "tool", "lift")
_STRIDE_SWAP = {"swing": "swing2", "swing2": "swing"}
# A look that turns a person round, takes them down to their knees or up again, or sets them walking
# or stops them, comes in at once: the old body and the new barely overlap, and a fade between them
# would be two people, or two pairs of legs
TURN_S = .04
_DOWN = ("kneel", "kneel2")


def whole_body(p0, f0, p1, f1):
    """Whether a change of look, from pose p0 facing f0 to p1 facing f1, turns the body round,
    takes it down or up, or starts or ends a stride."""
    return (p0.get("_flip", f0) != p1.get("_flip", f1)
            or p0.get("view", "side") != p1.get("view", "side")
            or (p0.get("legs") in _DOWN) != (p1.get("legs") in _DOWN)
            or (p0.get("legs") == "walk") != (p1.get("legs") == "walk"))


def person_actor(key, woman=False, x=0.0, y=None, pose=None):
    """A person on the Stage. Pose keys: view ("side", "lying"), arms, legs, covering, lean, up,
    breath; paint; _flip; per (how long a stride takes, .5 by default); tool and lift (the digging
    stick, and how far its tip is off the ground)."""
    def make(**p):
        p = dict(p)
        v = p.pop("view", "side")
        breath = p.pop("breath", 0.0)
        for q in _POSE_ONLY:
            p.pop(q, None)
        if v == "lying":
            return F.lying(breath)
        return F.side_person(woman, **dict(p, arms=arms_of(woman, p.get("arms", "down"))))

    def stage(pose_, flip_, s):
        k, b = person_layers(make(**pose_), flip=flip_, s=s, paint=pose_.get("paint", "live"))
        if pose_.get("tool"):
            stick = F.digging_stick(pose_["arms"], pose_.get("lean", 0.0), pose_.get("lift", 18.0))
            b = (G.render(stick, G.STICK_KEY_PAINT, s=s, flip=flip_, prec=1, curve=False)
                 + G.render(stick, G.STICK_PAINT, s=s, flip=flip_, prec=1, curve=False) + b)
        return (shadow_lying(s) if pose_.get("view") == "lying" else shadow(s)) + k, b
    make.stage, make.woman = stage, woman
    return SC.Actor(key, make, x, gy(x, woman) if y is None else y, h=G.MAN, unit_h=G.MAN_H,
                    pose=pose)


STAND_S = .45               # a stone figure standing up out of the ground, or going back into it


def stand_up(inner, t=None, k=1.0, down=None):
    """`inner`, its feet at the origin, at scale k: standing up out of the ground from `t`, and
    going back down into it from `down`, in its height alone. Never faded in plain view: in the
    hundredths in which it comes in it is a sliver on the ground, and once it has gone down it is
    switched off."""
    an, op, ky = "", "", k
    if t is not None:
        op, ky = ' opacity="0"', ".02"
        an += (f'{C.fade(t, .12)}<animateTransform attributeName="transform" type="scale" '
               f'values="{k} .02;{k} {k}" begin="{t:.2f}s" dur="{STAND_S:.2f}s" '
               f'fill="freeze" calcMode="spline" keyTimes="0;1" keySplines="{C.EASE}"/>')
    if down is not None:
        an += (f'<animateTransform attributeName="transform" type="scale" '
               f'values="{k} {k};{k} .02" begin="{down:.2f}s" dur="{STAND_S:.2f}s" '
               f'fill="freeze" calcMode="spline" keyTimes="0;1" keySplines="{C.EASE}"/>'
               f'<set attributeName="visibility" to="hidden" begin="{down + STAND_S:.2f}s"/>')
    return f'<g transform="scale({k} {ky})"{op}>{an}{inner}</g>'


def stone_use(fl, defs_id, x, y, t=None, k=1.0, down=None, who="stone"):
    """A person only spoken of: one <use> of a stone drawing, standing up out of the ground as they
    are said (`t`), and going back into it (`down`): `stand_up`. Kept on the flight as `who`, for
    the floor (`drawn_figure`)."""
    drawn_figure(fl, who, x, x, y, k, t, None if down is None else down + STAND_S)
    use = f'<use href="#{defs_id}"/>'
    return f'<g transform="translate({x} {y:.1f})">{stand_up(use, t, k, down)}</g>'


def drawn_figure(fl, who, x0, x1, y, k=1.0, t=None, gone=None):
    """Keeps a person drawn by hand, not on the card, on the flight, for garden_qc's floor: their
    feet at y, somewhere from x0 to x1, at k of a man's size, shown from t (None: from the start)
    until `gone` (None: to the end)."""
    fl.figures.append(Figure(who, x0, x1, y, k, t, gone))


def striding(stand, walk, walk2, t, dur):
    """One figure drawn by hand, by the ids of its three drawings, as it walks from t for dur
    seconds: the stride's two alternating every half stride, and standing before and after. The
    move is the caller's."""
    n = max(1, round(dur / .5))
    each = (f'dur="{dur / n:.3f}s" begin="{t:.2f}s" repeatCount="{n}" calcMode="discrete" '
            'fill="freeze"')
    off = f'<set attributeName="visibility" to="hidden" begin="{t + dur:.2f}s"/>'
    return (f'<g><set attributeName="visibility" to="hidden" begin="{t:.2f}s"/>'
            f'<set attributeName="visibility" to="visible" begin="{t + dur:.2f}s"/>'
            f'<use href="#{stand}"/></g>'
            '<g visibility="hidden"><animate attributeName="visibility" values="visible;hidden" '
            f'keyTimes="0;.5" {each}/>{off}<use href="#{walk}"/></g>'
            '<g visibility="hidden"><animate attributeName="visibility" values="hidden;visible" '
            f'keyTimes="0;.5" {each}/>{off}<use href="#{walk2}"/></g>')


def stone_defs(fl, pre="sv", kinds=None, paint="stone", arms="down", legs="stand"):
    """Father, mother, son, child, each the pair's own profile drawing in a coat, in stone. One
    treatment. `arms` and `legs` put them in another pose: a stride, for the living walking off."""
    kinds = kinds or {"m": (False, 1), "w": (True, 1), "mw": (False, -1), "ww": (True, -1),
                      "c": (False, 1), "cw": (True, -1)}
    o = "<defs>"
    for name, (woman, flip) in kinds.items():
        k, b = person_layers(F.side_person(woman, arms, legs, "skins"), flip=flip, paint=paint)
        o += f'<g id="{pre}{name}">{shadow()}{stroke_groups(fl, k, b)}</g>'
    return o + "</defs>"


# ---------------------------------------------------------------------------
# The creatures, in earth colours: an outline over the green reads as a wire model. Their faces
# are blank
# ---------------------------------------------------------------------------

_BEAST_INK = (232, 224, 192)
_COAT = {"lion": dict(hide=(182, 146, 88), far=(120, 96, 58), hair=(112, 78, 44),
                      muzzle=(196, 166, 112), hoof=(84, 66, 44)),
         "wolf": dict(hide=(138, 134, 122), far=(92, 90, 82), hair=(88, 86, 78),
                      muzzle=(160, 156, 144), hoof=(70, 68, 62)),
         "ox": dict(hide=(136, 94, 60), far=(92, 64, 42), hair=(88, 60, 38),
                    muzzle=(156, 116, 84), hoof=(62, 46, 32), horn=(232, 224, 196)),
         "sheep": dict(fleece=(222, 214, 188), far=(150, 144, 124), hair=(104, 94, 76),
                       muzzle=(138, 126, 104), hoof=(72, 64, 52)),
         "donkey": dict(hide=(130, 120, 106), far=(90, 84, 74), hair=(84, 78, 68),
                        muzzle=(168, 158, 142), hoof=(60, 56, 50), mane=(58, 52, 46)),
         "bird": dict(wing=(206, 200, 176), hide=(206, 200, 176), far=(150, 146, 128),
                      hair=(150, 146, 128), fleece=(206, 200, 176))}


def _drawn_parts(parts):
    """A creature's parts as the garden draws them: no eye, since faces are blank, and no line
    twice or of no length, which WebKit paints as a dot under a round cap."""
    out, lines = [], set()
    for q in parts:
        if q[2] in ("eye", "sclera"):
            continue
        if q[0] == "line":
            pts = tuple(tuple(p) for p in q[1])
            if len(set(pts)) < 2 or (q[2], pts) in lines:
                continue
            lines.add((q[2], pts))
        out.append(q)
    return out


def creature_svg(parts, kind, flip, s, with_shadow=True):
    """A creature in its coat, feet at (0, 0)."""
    page = G.GARDEN_NEAR[0]
    style = dict(F.palette(_BEAST_INK, page))
    for m, col in _COAT[kind].items():
        style[m] = (col, _BEAST_INK, 1.2)
    c = SvgCanvas(10, 10)
    F.draw(c, _drawn_parts(parts), 0, 0, s, _BEAST_INK, page, flip=flip, style=style)
    sh = (f'<path fill="#101810" fill-opacity=".45" d="M{-50 * s:.0f} '
          f'1q{50 * s:.0f}-6 {100 * s:.0f} 0q{-50 * s:.0f} 7 '
          f'{-100 * s:.0f} 0z"/>') if with_shadow else ""
    return sh + "".join(c._els)


def _beast_maker(fn, kind):
    make = SC.static(fn)
    make.garden_svg = lambda _p, flip, s: creature_svg(fn(), kind, flip, s)
    return make


# one maker per kind of creature, so a pair shares its drawing
_BEAST = {kind: _beast_maker(fn, kind)
          for kind, fn in (("ox", F.ox), ("sheep", F.sheep), ("donkey", F.donkey), ("lion", F.lion),
                           ("wolf", F.wolf))}


def _bird_make(**p):
    return F.bird(pose=p.get("wing", "glide"), view="profile")


def _bird_svg(p, flip, s):
    return creature_svg(_bird_make(**p), "bird", flip, s, with_shadow=False)


_bird_make.garden_svg = _bird_svg


def beast(key, kind, x, flip=1):
    """A beast on the near side of the line."""
    return SC.Actor(key, _BEAST[kind], x, G.ground_y(x) + 26, h=G.MAN, unit_h=G.MAN_H, flip=flip)


def flyer(key, x, y, flip=1):
    return SC.Actor(key, _bird_make, x, y, h=G.MAN, unit_h=G.MAN_H, flip=flip)


# ---------------------------------------------------------------------------
# The Stage: the card, with people who keep thin lines at any zoom
# ---------------------------------------------------------------------------

_PATH = re.compile(r'<path\b([^>]*?)\bd="([^"]*)"([^>]*?)/>')


def morph_strings(frames, t, dur):
    """One drawing at three moments -> the first, with each path that changes carrying an <animate>
    of its d."""
    lists = [_PATH.findall(f) for f in frames]
    assert len({len(q) for q in lists}) == 1, "a morph's drawings differ in their paths"
    idx = [-1]

    def sub(m):
        idx[0] += 1
        ds = [q[idx[0]][1] for q in lists]
        if len(set(ds)) == 1:
            return m.group(0)
        letters = {re.sub(r"[-\d.\s,]+", "", d) for d in ds}
        assert len(letters) == 1, "a morph's paths differ in their commands"
        return (f'<path{m.group(1)}d="{ds[0]}"{m.group(3)}><animate attributeName="d" '
                f'values="{";".join(ds)}" keyTimes="0;.5;1" begin="{t:.2f}s" dur="{dur:.2f}s" '
                f'fill="freeze" calcMode="spline" keySplines=".42 0 .7 .6;.3 .4 .58 1"/></path>')
    return _PATH.sub(sub, frames[0])


def _chain(c0, c1, u):
    """A limb between two poses: by its joints' angles about the joint above, so it rotates and
    doesn't shrink."""
    out = [c0[0]]
    for i in range(1, len(c0)):
        ax, ay = c0[i][0] - c0[i - 1][0], c0[i][1] - c0[i - 1][1]
        bx, by = c1[i][0] - c1[i - 1][0], c1[i][1] - c1[i - 1][1]
        la, aa = math.hypot(ax, ay), math.atan2(ay, ax)
        lb, ab = math.hypot(bx, by), math.atan2(by, bx)
        da = (ab - aa + math.pi) % (2 * math.pi) - math.pi
        L, A = la + (lb - la) * u, aa + da * u
        out.append((out[-1][0] + L * math.cos(A), out[-1][1] + L * math.sin(A)))
    return out


def lerp_pose(p0, p1, u, woman=False):
    """The pose a part of the way from p0 to p1: the arms by their joints, and the head, the lean,
    the stick and the breath by their numbers."""
    q = dict(p1)
    a0, a1 = p0.get("arms", "down"), p1.get("arms", "down")
    if a0 != a1:
        n0, f0 = arms_of(woman, a0)
        n1, f1 = arms_of(woman, a1)
        q["arms"] = (_chain(n0, n1, u), _chain(f0, f1, u))
    for k in ("up", "lean", "lift", "breath"):
        if k in p0 or k in p1:
            dflt = 18.0 if k == "lift" else 0.0
            b = p1.get(k, p0.get(k, dflt))
            a = p0.get(k, b if k == "lift" else dflt)
            q[k] = a + (b - a) * u
    return q


class Stage(G.GardenCard):
    """The garden's card. Its cast is `add_cast`'s: people with a `stage` maker, and things and
    beasts with a `garden_svg`, drawn in the order they were added, but for those a verse draws
    first (`first`). Only the kinds of event the garden uses are drawn: show, hide, move, grow,
    pulse, pose and flip."""

    def __init__(self):
        super().__init__(**G.card_kwargs())
        self.x_of = {}          # where the beasts have got to, as the verses are told: see `trot`
        self.went = {}          # how far on the walk out is: see `walk_from`
        self.stick_up = True    # whether the stone man's stick is up: see `dig_strokes`
        self.first = {}         # {ref: the actors drawn under the rest of the cast in that verse}

    def state_at(self, ref):
        """Every actor's state as `ref` opens: each verse's events replay in the order of their
        times, as they are drawn."""
        st = {k: dict(a.start, pose=dict(a.start["pose"])) for k, a in self.actors.items()}
        for r in self.refs:
            if r == ref:
                break
            for kind, key, _t, _d, val in sorted(self.events.get(r, []), key=lambda e: e[2]):
                SC.apply_event(st[key], kind, val)
        for s in st.values():
            s["pose"].pop("_morph", None)
        return st

    def verse_svg(self, ref, fl, scene, over=""):
        """The card's group in world units for this verse: Scene.behind and Scene.outside, the cast
        as the verse opens with this verse's events animated, Scene.front, then `over`."""
        st = self.state_at(ref)
        evs = sorted(self.events.get(ref, []), key=lambda e: e[2])
        self._wk, self._wb = coarse(fl, key_w), coarse(fl, body_w)
        self._syms, self._sym_defs = {}, []
        cast = ""
        first = self.first.get(ref, ())
        for key in sorted(self.actors, key=lambda k: k not in first):
            mine = [e for e in evs if e[1] == key]
            if st[key]["shown"] or any(e[0] == "show" for e in mine):
                cast += self._actor(self.actors[key], st[key], mine)
        syms = "<defs>" + "".join(self._sym_defs) + "</defs>" if self._sym_defs else ""
        (tx, ty), (ax, ay), (x0, y0), (w, h) = self.town_xy, self.anchor, self.origin, self.size
        first, switch = fl.scene_visibility()
        hidden = f' visibility="{first}"' if first != "visible" else ""
        return (f'<g transform="translate({_fmt(tx)} {_fmt(ty)}) scale({1 / self.S:.6g}) '
                f'translate({-ax} {-ay})"><g>'
                f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="{C.rgb(self.sky)}"/>'
                f"<defs>{scene.defs}</defs><g{hidden}>{switch}{scene.behind}{scene.outside}{syms}"
                f"{cast}{scene.front}</g>{over}</g></g>")

    def _actor(self, a, s0, evs):
        """One actor: <g translate(x, y)> with its moves summed on top, and one layer per look it
        shows this verse. The new look fades in over the old, and the old goes when the new is
        whole, or when a later look is, if that is sooner, so a body is never see-through and never
        two; one that turns them round, takes them down or up, or starts or ends a stride, comes in
        at once (TURN_S). A hide at that same moment waits for it too."""
        evs = self._turns_at_once(s0, evs)
        swaps = {(t, d) for kind, _k, t, d, _v in evs if kind in ("pose", "flip")}

        def gone(t, d):
            return C.fade(t + d, .01, out=True) if (t, d) in swaps else C.fade(t, d, out=True)

        shown, moves, grows = "", "", ""
        # [(pose, flip, morph), (t_in, d_in), (t_out, d_out)]
        segs = [[(dict(s0["pose"]), s0["flip"], None), None, None]]
        for kind, _k, t, d, val in evs:
            if kind == "move":
                moves += self.move_anim(t, d, val)
            elif kind == "grow":
                grows += ('<animateTransform attributeName="transform" type="scale" '
                          'values="1 0.02;1 1" additive="sum" '
                          f'begin="{t:.2f}s" dur="{d:.2f}s" fill="freeze" calcMode="spline" '
                          f'keyTimes="0;1" keySplines="{C.EASE}"/>')
            elif kind == "show":
                shown += C.fade(t, d)
            elif kind == "hide":
                shown += gone(t, d)
            elif kind in ("pose", "flip"):
                pose, flip, _m = segs[-1][0]
                if kind == "pose":
                    pose = {k: v for k, v in dict(pose, **val).items() if k != "_morph"}
                    look = (pose, flip, val.get("_morph"))
                else:
                    look = (pose, val, None)
                segs[-1][2] = (t, d)
                segs.append([look, (t, d), None])
        pulses = [(t, d) for kind, _k, t, d, _v in evs if kind == "pulse"]
        # when each look is whole: a look goes at the first of these after its own, which is not
        # always the next one's, since a look that comes in at once can overtake one still fading in
        whole = [t_in[0] + t_in[1] if t_in else 0.0 for _look, t_in, _t_out in segs]
        layers, was = "", None
        for i, ((pose, flip, morph), t_in, t_out) in enumerate(segs):
            seg = (t_in[0] if t_in else None, t_out[0] if t_out else None)
            body = self._drawing(a, pose, flip, seg, was, morph, pulses)
            was = pose
            cut = min(whole[i + 1:], default=None)
            anim = ((C.fade(*t_in) if t_in else "")
                    + (C.fade(cut, .01, out=True) if cut is not None else ""))
            layers += f'<g opacity="{"0" if t_in else "1"}">{anim}{body}</g>'
        return (f'<g transform="translate({_fmt(s0["x"])} {_fmt(s0["y"])})" '
                f'opacity="{"1" if s0["shown"] else "0"}">'
                f"{shown}{moves}<g>{grows}{layers}</g></g>")

    @staticmethod
    def move_anim(t, d, val):
        """What a move event is written as: eased, or at a steady speed (STEADY)."""
        ease = "" if val[2:] else f' calcMode="spline" keyTimes="0;1" keySplines="{C.EASE}"'
        return ('<animateTransform attributeName="transform" type="translate" '
                f'values="0 0;{_fmt(val[0])} {_fmt(val[1])}" additive="sum" '
                f'begin="{t:.2f}s" dur="{d:.2f}s" fill="freeze"{ease}/>')

    @staticmethod
    def _turns_at_once(s0, evs):
        """The events, with each look that turns the body round or takes it down or up shortened
        to TURN_S. A limb's move (`_morph`) is not a new look."""
        pose, flip, out = dict(s0["pose"]), s0["flip"], []
        for e in evs:
            kind, key, t, d, val = e
            if kind == "pose":
                new = {k: v for k, v in dict(pose, **val).items() if k != "_morph"}
                if "_morph" not in val and whole_body(pose, flip, new, flip):
                    e = (kind, key, t, min(d, TURN_S), val)
                pose = new
            elif kind == "flip":
                if whole_body(pose, flip, pose, val):
                    e = (kind, key, t, min(d, TURN_S), val)
                flip = val
            out.append(e)
        return out

    def _drawing(self, a, pose, flip, seg, was, morph, pulses):
        """One look of an actor: a stride's two drawings alternating, a bird's two wings, a limb's
        morph, or a <use>. Under it, each pulse in this look: the whole silhouette, stroked, so that
        only its outline shows."""
        if pose.get("flap"):
            return self._flap(a, pose, flip)
        flip = pose.get("_flip", flip)
        under = self._pulse_under(a, pose, flip, seg, pulses)
        if not hasattr(a.make, "stage"):
            return under + super()._drawing(a, pose, None, flip)
        if morph and seg[0] is not None:
            return under + self._morph_drawing(a, was or pose, pose, seg[0], morph, flip)
        if pose.get("legs") == "walk" and seg[0] is not None and seg[1] is not None:
            return under + self._stride(a, pose, flip, seg)
        return under + self._person_use(*self._sym(a, pose, flip))

    def _sym(self, a, pose, flip):
        """A person's keyline and contours in this look, drawn once a file, as (keyline's id, body's
        id)."""
        k = ("stage", id(a.make), tuple(sorted(pose.items())), a.h, flip)
        if k not in self._syms:
            key, body = a.make.stage(pose, flip, a.h / a.unit_h)
            kid, bid = f"{self.key}{len(self._sym_defs)}k", f"{self.key}{len(self._sym_defs)}b"
            self._sym_defs.append(f'<g id="{kid}" stroke-linecap="round" '
                                  f'stroke-linejoin="round">{key}</g>'
                                  f'<g id="{bid}" stroke-linecap="round" '
                                  f'stroke-linejoin="round">{body}</g>')
            self._syms[k] = (kid, bid)
        return self._syms[k]

    def _person_use(self, key_id, body_id):
        return (f'<g stroke-width="{self._wk[0]}">{self._wk[1]}<use href="#{key_id}"/></g>'
                f'<g stroke-width="{self._wb[0]}">{self._wb[1]}<use href="#{body_id}"/></g>')

    def _stride(self, a, pose, flip, seg):
        """A walk: its two drawings alternating for as long as the look lasts."""
        arms = pose.get("arms", "swing")
        one = self._sym(a, pose, flip)
        other = self._sym(a, dict(pose, legs="walk2", arms=_STRIDE_SWAP.get(arms, arms)), flip)
        t0, t1 = seg
        n = max(1, round((t1 - t0) / pose.get("per", .5)))
        common = (f'dur="{(t1 - t0) / n:.3f}s" begin="{t0:.2f}s" repeatCount="{n}" '
                  'calcMode="discrete" fill="freeze"')
        return ('<g><animate attributeName="visibility" values="visible;hidden" '
                f'keyTimes="0;.5" {common}/>'
                + self._person_use(*one) + '</g><g visibility="hidden">'
                '<animate attributeName="visibility" values="hidden;visible" '
                f'keyTimes="0;.5" {common}/>'
                + self._person_use(*other) + "</g>")

    def _flap(self, a, pose, flip):
        """A bird's wings, beating by a discrete swap."""
        t0, t1, per = pose["flap"]
        n = max(1, int(round((t1 - t0) / per)))

        def one(wing):
            return creature_svg(F.bird(pose=wing, view="profile"), "bird", flip, a.h / a.unit_h,
                                with_shadow=False)

        def swap(vals):
            return (f'<animate attributeName="opacity" values="{vals}" calcMode="discrete" '
                    f'dur="{per:g}s" '
                    f'begin="{t0:.2f}s" repeatCount="{n}" fill="freeze"/>')
        return f'<g>{swap("1;0")}{one("up")}</g><g opacity="0">{swap("0;1")}{one("down")}</g>'

    def _morph_drawing(self, a, p0, p1, t, dur, flip):
        """A limb's move: the drawing's own paths, through a mid-pose, with no fade at all. It takes
        the head and the stick with it."""
        s = a.h / a.unit_h
        frames = [a.make.stage(lerp_pose(p0, p1, u, a.make.woman), flip, s)
                  for u in (0.0, .5, 1.0)]
        key = morph_strings([f[0] for f in frames], t, dur)
        body = morph_strings([f[1] for f in frames], t, dur)
        cap = 'stroke-linecap="round" stroke-linejoin="round"'
        return (f'<g stroke-width="{self._wk[0]}" {cap}>{self._wk[1]}{key}</g>'
                f'<g stroke-width="{self._wb[0]}" {cap}>{self._wb[1]}{body}</g>')

    def _pulse_under(self, a, pose, flip, seg, pulses):
        here = [(t, d) for t, d in pulses
                if (seg[0] is None or t >= seg[0]) and (seg[1] is None or t < seg[1])]
        if not here:
            return ""
        s = a.h / a.unit_h
        d_ = G._D(1)
        for kind, dat, _m in a.parts(pose):
            if kind == "dot":
                d_.dot(dat[0] * s * flip, -dat[1] * s, dat[2] * s)
            elif kind == "fill":
                pts = [(x * s * flip, -y * s) for x, y in dat]
                if G._area(pts) < 0:
                    pts = pts[::-1]
                d_.poly(pts, True)
        an = "".join('<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.3;.6;1" '
                     f'begin="{t:.2f}s" dur="{d:.2f}s" fill="freeze"/>'
                     for t, d in here)
        return (f'<path d="{d_.text()}" fill="{C.rgb(HL)}" stroke="{C.rgb(HL)}" stroke-width="6" '
                f'stroke-linejoin="round" opacity="0">{an}</path>')


def add_cast(c):
    """The cast of both chapters, in the order they are drawn, with their first places."""
    c.add(person_actor("man", False, MF[0], pose={"arms": "down"}))
    c.add(person_actor("wom", True, W_RISE[0], W_RISE[1], pose={"arms": "down"}))
    c.add(G.thing_actor("fruit", G.fruit_macro(lw=.5), *fruit_on(True, "take", W_REACH)))
    c.add(person_actor("dig", False, DIG_X, pose={"paint": "stone", "covering": "leaves", "tool": 1,
                                                  "arms": "dig1", "lift": 18.0, "lean": 14.0}))
    c.add(person_actor("lest", False, LEST_X, pose={"paint": "stone", "covering": "skins"}))
    # the shoot stands just in front of the people's line, and the beasts further in front of it
    sprout = G.render(F.sprout(s=PXU), G.SPROUT_PAINT, s=1, prec=2, curve=False)
    c.add(G.thing_actor("shoot", f'<g transform="scale(2.2)">{sprout}</g>', SHOOT_X,
                        gy(SHOOT_X) + 4))
    for key, kind, x, flip in (("lion1", "lion", 330, -1), ("lion2", "lion", 430, -1),
                               ("wolf1", "wolf", 545, -1), ("wolf2", "wolf", 640, -1),
                               ("ox1", "ox", -1120, 1), ("ox2", "ox", -1240, 1),
                               ("sheep1", "sheep", -1010, 1), ("sheep2", "sheep", -1070, 1),
                               ("don1", "donkey", -1340, 1), ("don2", "donkey", -1440, 1)):
        c.add(beast(key, kind, x, flip))
        c.x_of[key] = x
    for i, (x, y) in enumerate(((360, 1290), (470, 1300), (560, 1296), (640, 1304))):
        c.add(flyer(f"bird{i}", x, y, -1))
    # the small snakes of 3:15, in a file west of the frame they come into, the leader east
    small = G.render(F.small_snake(s=PXU), G.SMALL_SNAKE_PAINT, s=1, prec=2, curve=False)
    for key, x, drop in (("sm0", -110, 34), ("sm1", -30, 38), ("sm2", 45, 42)):
        c.add(G.thing_actor(key, small, x, G.ground_y(x) + drop))
    herb = G.render(G.herb(random.Random(4), 46), G.PLANT_PAINT, s=1, prec=0)
    c.add(G.thing_actor("herb", herb, DIG_X + 58, G.ground_y(DIG_X + 58) + 12))
    c.add(G.thing_actor("figd", G.FIG_SVG, *G.FIG_A))


def pose(c, ref, key, t, d=.2, **p):
    """A change of pose: `_morph`, in `p`, makes it a limb's move, of that length, as a change of
    the arms or the head alone must be (test_garden.Looks)."""
    c.on(ref, ("pose", key, round(t, 2), d, p))


def trot(c, ref, key, t, dur, x1, steady=False):
    """A beast goes to x1, along the line: at a steady speed if `steady`, so that it carries over a
    verse's seam."""
    dx = x1 - c.x_of[key]
    c.on(ref, ("move", key, round(t, 2), round(dur, 2), (dx, 0, STEADY) if steady else (dx, 0)))
    c.x_of[key] = x1


def walk_events(c, ref, key, x0, x1, t, dur, flip=None, end_arms="down", keep=None):
    """They walk from x0 to x1 along the ground, from t for dur seconds: the pose, the move, and
    standing again. `flip` faces them first, `keep` is what the pose keeps."""
    keep = keep or {}
    faces = {"_flip": flip} if flip is not None else {}
    c.on(ref, ("pose", key, t, .12, {"legs": "walk", "arms": "swing", **faces, **keep}),
         ("move", key, t, dur, (x1 - x0, G.ground_y(x1) - G.ground_y(x0))),
         ("pose", key, round(t + dur, 2), .14, {"legs": "stand", "arms": end_arms, **keep}))


_WALK_POSE = {"legs": "walk", "arms": "swing", "up": 0, "per": .5, "covering": "skins", "_flip": 1,
              "lean": 0}


def walk_from(c, ref, key, x0, t0, dur):
    """Warped under an opaque plate's rest to x0, and walking east at the one steady pace to the
    verse's end."""
    woman = key == "wom"
    was = W_RULE if woman else M_PLOT
    x1 = x0 + WALK_V * (dur - .03)
    c.on(ref, ("pose", key, round(t0, 2), .01, dict(_WALK_POSE)),
         ("move", key, round(t0, 2), .01, (x0 - was, gy(x0, woman) - gy(was, woman))))
    c.on(ref, ("move", key, round(t0 + .02, 2), round(dur - .03, 2),
               (x1 - x0, gy(x1, woman) - gy(x0, woman), STEADY)))
    c.on(ref, ("pose", key, round(t0 + dur - .03, 2), .01, dict(_WALK_POSE)))
    c.went[key] = x1


def walk_on(c, v, key, t0):
    """The same walk, on through the verse and out of the frame. It never stops: they are gone at
    the first .02 s at which all of them, their shadow too, is past the right edge of the frame the
    verse's camera has by then, so that wherever a re-rendered MP3 leaves them they are never
    switched off in sight. A walk the frame never loses doesn't build."""
    woman = key == "wom"
    x0 = c.went[key]
    t1 = round(t0 + .01, 2)
    fl = v.flight()
    # how far behind their feet the last of them is: the stride's back, its keyline, or the shadow
    stride = min(p[0] for arms, legs in (("swing", "walk"), ("swing2", "walk2"))
                 for part, pts, _m in F.side_person(woman, arms, legs, "skins")
                 if part == "fill" for p in pts)
    rear = min(stride * PXU - key_w(1) / 2, -SHADOW_BACK * PXU)
    grid = [round(t1 + i * .02, 2) for i in range(int((v.dur - t1) / .02) + 1)]
    t_off = next((t for t in grid if x0 + rear + WALK_V * (t - t1) > C.visible_world(fl.at(t))[2]),
                 None)
    if t_off is None:
        raise ValueError(f"{v.ref}: {key} walks on and is still in the frame as the verse ends")
    d1 = round(t_off - t1, 2)
    x1 = x0 + WALK_V * d1
    c.on(v.ref, ("pose", key, t1, .01, dict(_WALK_POSE)),
         ("move", key, t1, d1, (x1 - x0, gy(x1, woman) - gy(x0, woman), STEADY)))
    c.on(v.ref, ("pose", key, t_off, .01, dict(_WALK_POSE)), ("hide", key, t_off, .01, None))


def dig_strokes(c, v, ref, t0, t1, seed):
    """About a stroke a second: the stick driven in, and raised again, moving as a limb; dust at
    each strike."""
    tt, i = t0, 0
    while tt < t1:
        if c.stick_up:
            if tt + .22 > t1:
                break
            pose(c, ref, "dig", tt, .01, arms="dig2", tool=1, lift=-2.0, lean=14.0, _morph=.22)
            v.over.append((lambda t, sd: lambda fl: puff_fx(
                DIG_X + 36, G.ground_y(DIG_X) + 4, t, .6, seed=sd))(tt + .18, seed + i))
            c.stick_up = False
            tt += .4
        else:
            if tt + .45 > t1:
                break
            pose(c, ref, "dig", tt, .01, arms="dig1", tool=1, lift=18.0, lean=14.0, _morph=.45)
            c.stick_up = True
            tt += .6
        i += 1


# ---------------------------------------------------------------------------
# A verse
# ---------------------------------------------------------------------------

VERSES = {}
# A name pinned on a flight: its world point, its text, when it comes in (None: it is in from the
# start), its screen size, (when, how long) it goes, and how far it sits from its point on the
# screen, px
Name = namedtuple("Name", "x y text t px italic gone off", defaults=((0, 0),))
# A person drawn by hand on a flight: `drawn_figure`
Figure = namedtuple("Figure", "who x0 x1 y k t gone")
NAME_IN_S = .5              # how long a name takes to come in


class _Cut:
    """A cut among a Flight's legs: it takes no time, and from it on the camera is on its shot."""
    dur = 0.0

    def __init__(self, cam):
        self.camB = cam


class VerseFlight(C.Flight):
    """A verse's Flight, which keeps what garden_qc.py asks of it as the verse is drawn: the names
    pinned on it, the plates hung over it, and the people drawn on it by hand.

    Its legs may also be ("cut", cam, 0): an edit, the camera on another shot at once, which is how
    a plate comes and goes. The keys are baked as ever, at even steps; a cut falls between two of
    them, `cut_keys` names the first, and the camera holds that key's shot until the next and is on
    the next at once. Everything baked on the keys is written so (`_anim`), so that the camera, a
    name's size and a sliver's opacity all jump together, with no frame between."""

    def __init__(self, cam0, legs):
        self._cuts = [c for c in legs if c[0] == "cut"]
        if self._cuts:
            self._bake_with_cuts(cam0, legs)
        else:
            super().__init__(cam0, legs)
            self.cut_keys = []
        self.names, self.plates = [], []        # plates: (zin, off_after, on_after)
        self.figures = []                       # the people drawn by hand: Figure

    def _bake_with_cuts(self, cam0, legs):
        """Flight's own baking, with a cut as a leg of no length."""
        self.cam0, self.legs, cut_at = cam0, [], []
        cam, t = cam0, 0.0
        for kind, target, dur in legs:
            if kind == "cut":
                self.legs.append(_Cut(target))
                cut_at.append(t)
                cam = target
            elif kind == "hold":
                if dur > 0:
                    self.legs.append(C.Leg(cam, cam, dur, "hold"))
                    t += dur
            elif not (C._same(cam, target) or dur <= 0):
                k = "pan" if abs(cam[0] - target[0]) < 1e-9 else "zoom"
                self.legs.append(C.Leg(cam, target, dur, k))
                cam, t = target, t + dur
        self.cam1, self.static, self.pure_pan, self.dur = cam, False, False, t
        n = max(6, int(round(t * C.CAM_FPS)))
        cams = [self.exact(t * i / n) for i in range(n + 1)]
        cams[0], cams[-1] = cam0, cam
        self.cams = [(float("%.6f" % c[0]), c[1], c[2]) for c in cams]
        self.cut_keys = sorted({max(i for i in range(n) if t * i / n <= tc + 1e-7)
                                for tc in cut_at})

    def exact(self, t):
        """The camera at t. A key at the moment of a cut is the shot before it."""
        if not self._cuts:
            return super().exact(t)
        t0, cam = 0.0, self.cam0
        for lg in self.legs:
            if not lg.dur:
                cam = lg.camB
                continue
            if t <= t0 + lg.dur + 1e-7:
                return lg.at(min(1.0, (t - t0) / lg.dur))
            t0, cam = t0 + lg.dur, lg.camB
        return cam

    def at(self, t):
        """The camera at t, as the browser plays it: across a cut, the key before it."""
        if self.cut_keys and 0 < t < self.dur:
            n = len(self.cams) - 1
            i = min(n - 1, int(t / self.dur * n))
            if i in self.cut_keys:
                return self.cams[i]
        return super().at(t)

    def _anim(self, attr, vals, typ=None):
        """Flight's animation of something baked on the keys. Across a cut it holds the key before
        the cut until the next key's time, and the next comes in at that same time, so that it
        jumps when the camera does. With its times written out, a run of one value needs only its
        ends."""
        if not self.cut_keys or len(set(vals)) == 1:
            return super()._anim(attr, vals, typ)
        n = len(vals) - 1
        keys = []
        for i, v in enumerate(vals):
            when = f"{i / n:.4f}".rstrip("0").rstrip(".")
            if i - 1 in self.cut_keys:
                keys.append((vals[i - 1], when))
            keys.append((v, when))
        keys = [k for i, k in enumerate(keys)
                if not 0 < i < len(keys) - 1 or not keys[i - 1][0] == k[0] == keys[i + 1][0]]
        vs, kt = [k[0] for k in keys], [k[1] for k in keys]
        kind = "animateTransform" if typ else "animate"
        ty = f' type="{typ}"' if typ else ""
        return (f'<{kind} attributeName="{attr}"{ty} values="{";".join(vs)}" '
                f'keyTimes="{";".join(kt)}" dur="{self.dur:.2f}s" begin="0s" fill="freeze"/>')

    def keys_in(self, plate):
        """Whether a plate is in from each of the camera's keys to the next: the camera at its zoom
        or closer, and the verse's time its own, at both of them, or across a cut at the key before
        it, which the camera holds. So it is never in while the camera is wider than its zoom, and
        it comes and goes with a cut at once."""
        zin, off, on = plate
        n = len(self.cams) - 1
        at = [c[0] >= zin and (off is None or t <= off) and (on is None or t >= on)
              for c, t in zip(self.cams, [i / n * self.dur for i in range(n + 1)] if n else [0.0])]
        ins = [a and b for a, b in zip(at, at[1:] + at[-1:])]
        for k in self.cut_keys:
            ins[k] = at[k]
        return ins

    def covered(self, t):
        """Whether a plate is in at t, so that nothing under it is seen."""
        n = len(self.cams) - 1
        i = min(n, int(t / self.dur * n + 1e-9)) if n else 0
        return any(self.keys_in(p)[i] for p in self.plates)

    def switch(self, shown, attr="visibility"):
        """An attribute that shows something, or doesn't, from each of the camera's keys to the
        next, as (its first value, its animation): `visibility`, or `opacity` 1 or 0. Only the
        changes are written."""
        vals = [("visible" if s else "hidden") if attr == "visibility" else ("1" if s else "0")
                for s in shown]
        at = [i for i, v in enumerate(vals) if i == 0 or v != vals[i - 1]]
        if len(at) == 1:
            return vals[0], ""
        kt = ";".join(f"{i / (len(vals) - 1):.4f}" for i in at)
        return vals[0], (f'<animate attributeName="{attr}" '
                         f'values="{";".join(vals[i] for i in at)}" keyTimes="{kt}" '
                         f'calcMode="discrete" dur="{self.dur:.2f}s" begin="0s" fill="freeze"/>')

    def scene_visibility(self):
        """The scene's `visibility`, as (its first value, its animation): hidden while a plate is
        in, from the key after it comes in to the key before it goes, so that a close-up pays
        nothing for the world under it and the world is never off while the plate is."""
        n = len(self.cams) - 1
        ins = [any(q) for q in zip(*(self.keys_in(p) for p in self.plates))] or [False] * (n + 1)
        return self.switch([not (ins[max(i - 1, 0)] and ins[i] and ins[min(i + 1, n)])
                            for i in range(n + 1)])


def verse(ref):
    """Registers a verse's function, in a chapter's module."""
    def deco(fn):
        VERSES[ref] = fn
        return fn
    return deco


class Verse:
    """One verse's camera as absolute times, its scene, and what is drawn by hand, each a function
    of the Flight."""

    def __init__(self, ref, cam0, say=say):
        self.ref, self.cam0, self._say = ref, cam0, say
        self.dur = verse_dur(ref)
        self.keys = []              # (t0, t1, cam); a cut is (t, t, cam), and its t is in `cuts`
        self.cuts = set()
        self.scene = None           # fn(fl) -> Scene; by default `garden`
        self.under = []             # fn(fl) -> svg, under the cast
        self.over = []              # fn(fl) -> svg, over Scene.front
        self.plan = None            # fn(fl) -> the plan, for a verse hung in it
        self.plan_only = False      # the plan alone: no side view at all
        self.world_over = None      # fn(fl) -> svg, over the plan and the side view

    def t(self, word, today, lead=.1, n=0):
        """When a beat answering `word` starts, on its cue: `lead` before it's said (the nth time in
        the verse), or `today`, what that comes to on today's MP3, when there's no clock."""
        return cue(self._say, self.ref, word, today, lead, n)

    def cam(self, shot, t0, t1):
        """The camera goes to `shot` between t0 and t1."""
        self.keys.append((t0, t1, camera(shot)))

    def cut(self, shot, t, wide=0.0):
        """The camera is on `shot` at t at once: an edit, not a move, and the way a plate comes and
        goes. `wide`: that much wider than the shot, for a creep in to it after."""
        z, x, y = camera(shot)
        self.keys.append((t, t, (z * (1 - wide), x, y)))
        self.cuts.add(t)

    def creep(self, t0, t1, frac=.03):
        """A very slow push from wherever the camera is at t0: nothing stands still for long."""
        cam = self.cam0
        for _a, b, c_ in sorted(self.keys, key=lambda k: k[0]):
            if b <= t0 + 1e-6:
                cam = c_
        self.keys.append((t0, t1, (cam[0] * (1 + frac), cam[1], cam[2])))

    def settle(self, shot, t0, t1, t2, frac=.03):
        """To a shot's value at t2, arriving a little wide of it at t1 and creeping in: a re-shot
        stays exact, and doesn't stand still."""
        c_ = camera(shot)
        self.keys.append((t0, t1, (c_[0] * (1 - frac), c_[1], c_[2])))
        self.keys.append((t1, t2, c_))

    def flight(self):
        legs, t = [], 0.0
        for t0, t1, cam in sorted(self.keys, key=lambda k: k[:2]):
            if t0 > t + 1e-3:
                legs.append(("hold", None, round(t0 - t, 3)))
            if t1 == t0 and t0 in self.cuts:
                legs.append(("cut", cam, 0.0))
            else:
                legs.append(("to", cam, round(t1 - t0, 3)))
            t = t1
        return VerseFlight(self.cam0, legs)


def name_at(fl, x, y, text, t=None, px=16, fill=NAME_INK, italic=False, gone=None, fill_to=None,
            fill_at=None, off=(0, 0)):
    """A name at one screen size pinned to a world point: opaque once in. No em offsets, so WebKit's
    trap does not apply. `gone` = (t, dur) takes it out; `fill_to` shifts its colour over `fill_at`
    = (t, dur). `off` sets it that many screen px from its point, so that a name hung by what it
    names, on the plan, keeps by it whether the camera is near or far."""
    st = ' font-style="italic"' if italic else ""
    fa = ""
    if fill_to is not None:
        a, b = fill_at
        fa = (f'<animate attributeName="fill" values="{C.rgb(fill)};{C.rgb(fill_to)}" '
              f'begin="{a:.2f}s" dur="{b:.2f}s" fill="freeze"/>')
    text_el = (f'<text x="{_fmt(off[0])}" y="{_fmt(off[1])}" font-size="{px}" '
               'font-family="Georgia,serif" '
               'text-anchor="middle" dominant-baseline="central" '
               f'fill="{C.rgb(fill)}" stroke="{C.rgb(HALO)}" stroke-width="3.5" '
               f'stroke-opacity=".85" paint-order="stroke"{st}>'
               f'{fa}{text}</text>')
    an = op = ""
    if t is not None:
        op = ' opacity="0"'
        an += C.fade(t, NAME_IN_S)
    if gone:
        an += C.fade(gone[0], gone[1], out=True)
    fl.names.append(Name(x, y, text, t, px, italic, gone, off))
    return C.pin(fl, (x, y), f'<g{op}>{an}{text_el}</g>')


def plate(fl, inner, zin=4.0, off_after=None, on_after=None):
    """A close-up's own drawing, in world px, over the scene: the opaque ground it brings, first in
    `inner`, takes the place of the coarse drawing the camera has magnified. It is in, whole, while
    the camera is at zoom `zin` or closer, which it is from the camera's cut to it to the cut out
    (`Verse.cut`), and never faded, since anything faded between the world and a plate would be a
    person seen through. So its ground must cover the frame from that zoom on. Its opacity goes
    with its visibility, which alone a part of it shown by a <set> of its own would override. A
    verse with two closes gives each plate its time: on_after, off_after."""
    fl.plates.append((zin, off_after, on_after))
    ins = fl.keys_in(fl.plates[-1])
    (op, op_an), (vis, vis_an) = fl.switch(ins, "opacity"), fl.switch(ins)
    return f'<g opacity="{op}" visibility="{vis}">{op_an}{vis_an}{inner}</g>'


# ---------------------------------------------------------------------------
# Effects
# ---------------------------------------------------------------------------

def slide(values, begin, dur, key_times=None):
    """A translate along `values` [(dx, dy), ...], eased."""
    n = len(values) - 1
    kt = key_times or [i / n for i in range(n + 1)]
    return ('<animateTransform attributeName="transform" type="translate" '
            f'values="{";".join(f"{a:.1f} {b:.1f}" for a, b in values)}" '
            f'keyTimes="{";".join(f"{x:.3f}" for x in kt)}" begin="{begin:.2f}s" dur="{dur:.2f}s" '
            'fill="freeze" calcMode="spline" '
            f'keySplines="{";".join([".42 0 .58 1"] * n)}"/>')


def sway(t, dur, deg=7):
    """A fruit swinging on its stem and coming to rest (about the stem's top, in its own group)."""
    vals = ";".join(f"{deg * k:.1f}" for k in (0, 1, -.7, .45, -.25, .1, 0))
    return (f'<animateTransform attributeName="transform" type="rotate" values="{vals}" '
            f'begin="{t:.2f}s" dur="{dur:.2f}s" fill="freeze"/>')


def clip_rise(cid, x0, x1, y_top, y_bot, t, dur):
    """A clip rect that grows from y_bot up to y_top."""
    h = y_bot - y_top
    return (f'<defs><clipPath id="{cid}"><rect x="{x0}" y="{y_bot}" width="{x1 - x0}" height="0">'
            f'<animate attributeName="y" values="{y_bot};{y_top}" begin="{t:.2f}s" '
            f'dur="{dur:.2f}s" fill="freeze" calcMode="spline" keyTimes="0;1" '
            'keySplines=".3 0 .6 1"/>'
            f'<animate attributeName="height" values="0;{h}" begin="{t:.2f}s" dur="{dur:.2f}s" '
            'fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".3 0 .6 1"/>'
            '</rect></clipPath></defs>')


def clip_fall(cid, x0, x1, y_top, y_bot, t, dur):
    """A clip rect that grows from y_top down to y_bot."""
    h = y_bot - y_top
    return (f'<defs><clipPath id="{cid}"><rect x="{x0}" y="{y_top}" width="{x1 - x0}" height="0">'
            f'<animate attributeName="height" values="0;{h}" begin="{t:.2f}s" dur="{dur:.2f}s" '
            'fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".3 0 .6 1"/>'
            '</rect></clipPath></defs>')


def grains(rng, n, x0, x1, y0, y1, r=(.35, .9), col="#c2ac80"):
    """A path of little grains: round dots in a box. One element, however many grains."""
    d = G._D(1)
    for _ in range(n):
        d.dot(rng.uniform(x0, x1), rng.uniform(y0, y1), rng.uniform(*r))
    return f'<path fill="{col}" d="{d.text()}"/>'


def grain_rise(rng, x, y0, y1, t, dur, spread=8, n=7, col="#c6b088", r=(.5, 1.1)):
    """A pinch of grains going up from the ground into the body."""
    g = grains(rng, n, x - spread, x + spread, y0 - 3, y0 + 3, r, col)
    return ('<g opacity="0"><animate attributeName="opacity" values="0;1;1;0" '
            f'keyTimes="0;.15;.8;1" begin="{t:.2f}s" dur="{dur:.2f}s" fill="freeze"/>'
            '<g><animateTransform attributeName="transform" type="translate" '
            f'values="0 0;0 {y1 - y0}" begin="{t:.2f}s" dur="{dur:.2f}s" fill="freeze" '
            f'calcMode="spline" keyTimes="0;1" keySplines=".3 .1 .5 1"/>{g}</g></g>')


def grains_fx(cx, y, t0, dur, n=18, spread=170, seed=3, inward=True, lift=70, col="#b09a70"):
    """Dust moving on the ground: grains drawn to a point, or falling from it."""
    r = random.Random(seed)
    out = ""
    for _ in range(n):
        dx = r.uniform(-spread, spread)
        dy = r.uniform(-8, 20)
        tx, ty = r.uniform(-16, 16), -r.uniform(0, lift)
        a, b = f"{dx:.0f} {dy:.0f}", f"{tx:.0f} {ty:.0f}"
        if not inward:
            a, b = b, a
        begin = t0 + r.uniform(0, dur * .4)
        d = dur * r.uniform(.5, .6)
        out += (f'<circle r="{r.uniform(1.4, 2.8):.1f}" fill="{col}" opacity="0">'
                f'<animate attributeName="opacity" values="0;1;1;{0 if inward else .0}" '
                f'keyTimes="0;.15;.8;1" begin="{begin:.2f}s" '
                f'dur="{d:.2f}s" fill="freeze"/>'
                f'<animateTransform attributeName="transform" type="translate" values="{a};{b}" '
                f'begin="{begin:.2f}s" '
                f'dur="{d:.2f}s" fill="freeze" calcMode="spline" keyTimes="0;1" '
                f'keySplines="{C.EASE}"/></circle>')
    return f'<g transform="translate({cx:g} {y:g})">{out}</g>'


def puff_fx(x, y, t, k=1.0, seed=1):
    """A little dust thrown up: he hits the ground, or eats it."""
    r = random.Random(seed)
    out = ""
    for _ in range(5):
        dx, dy = r.uniform(-26, 26) * k, -r.uniform(8, 26) * k
        out += (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(3, 6) * k:.1f}" fill="#a48f68" '
                'opacity="0">'
                f'<animate attributeName="opacity" values="0;.8;0" begin="{t:.2f}s" dur=".7s" '
                'fill="freeze"/>'
                '<animateTransform attributeName="transform" type="translate" '
                f'values="0 0;{dx:.0f} {dy:.0f}" '
                f'begin="{t:.2f}s" dur=".7s" fill="freeze"/></circle>')
    return out


def wind(rng, x0, x1, y0, y1, t, dur, dx, n=26, r=(.35, .9), col="#cdb88e", dy=-3):
    """Dust going over dry ground, a short way, and settling."""
    g = grains(rng, n, x0, x1, y0, y1, r, col)
    return ('<g opacity="0"><animate attributeName="opacity" values="0;.95;.95;0" '
            f'keyTimes="0;.2;.7;1" begin="{t:.2f}s" dur="{dur:.2f}s" fill="freeze"/>'
            '<g><animateTransform attributeName="transform" type="translate" '
            f'values="0 0;{dx} {dy}" begin="{t:.2f}s" dur="{dur:.2f}s" fill="freeze"/>'
            f'{g}</g></g>')


MIST_DEF = ('<linearGradient id="mistg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" '
            'stop-color="#c4d0d0" stop-opacity="0"/>'
            '<stop offset=".55" stop-color="#c4d0d0" stop-opacity=".9"/><stop offset="1" '
            'stop-color="#c4d0d0" stop-opacity="0"/></linearGradient>')


def mist_band(rng, x, y, w, h, t, rise, dur, op=.3):
    """A long low wisp, soft top and bottom by a gradient on the one shape (MIST_DEF), going up and
    thinning."""
    n = 10
    ph = rng.uniform(0, 6)
    top = [(x - w / 2 + w * i / n,
            y - h * math.sin(math.pi * i / n) ** .6 * (1 + .18 * math.sin(i * 1.7 + ph)))
           for i in range(n + 1)]
    bot = [(x + w / 2 - w * i / n,
            y + h * .32 * math.sin(math.pi * i / n) ** .8 * (1 + .2 * math.sin(i * 1.3 + ph)))
           for i in range(1, n)]
    d = G._D(0)
    pts = top + bot
    d.closed_curve(pts[::-1] if G._area(pts) < 0 else pts)
    return (f'<path d="{d.text()}" fill="url(#mistg)" opacity="0">'
            f'<animate attributeName="opacity" values="0;{op};{op};0" keyTimes="0;.3;.65;1" '
            f'begin="{t:.2f}s" dur="{dur:.2f}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" values="0 0;0 {-rise}" '
            f'begin="{t:.2f}s" dur="{dur:.2f}s" fill="freeze"/></path>')


# The star wheel of 2:1-2:4, about POLE, in three sizes of pip
POLE = (1200, -700)
WHEEL_AFTER_2_1, WHEEL_AT_REST = 7.0, 13.0      # its angle after 2:1, and from "rested" at 2:2 on


@functools.cache
def _star_paths():
    """Three sizes of star as three paths of pips, thick in a band across the heavens, none of them
    low enough at the wheel's last angle to be in frame on the whole shot."""
    rng = random.Random(21)
    th = math.radians(WHEEL_AT_REST)
    groups = {0: "", 1: "", 2: ""}
    n = 0
    while n < 620:
        if rng.random() < .45:              # the band
            u = rng.uniform(-9000, 11000)
            x = u
            y = -2500 + (u - 1200) * .28 + rng.gauss(0, 620)
        else:
            x = rng.uniform(-9000, 11000)
            y = rng.uniform(-8200, 1050)
        dx, dy = x - POLE[0], y - POLE[1]
        yy = POLE[1] + dx * math.sin(th) + dy * math.cos(th)
        if yy > -780 and y > -780:
            continue
        i = rng.choices((0, 1, 2), (8, 3, 1))[0]
        groups[i] += f"M{x:.0f} {y:.0f}h.001"
        n += 1
    return groups


def stars(a0, a1, begin=0, dur=0, spline=".2 .6 .3 1", groups_in=None):
    """The heavens' array. It turns about POLE from a0 to a1: `groups_in` = {i: (t, dur)} brings a
    size in."""
    anim = ""
    if a0 != a1:
        anim = ('<animateTransform attributeName="transform" type="rotate" '
                f'values="{a0} {POLE[0]} {POLE[1]};{a1} {POLE[0]} {POLE[1]}" '
                f'begin="{begin:.2f}s" dur="{dur:.2f}s" fill="freeze" calcMode="spline" '
                f'keyTimes="0;1" keySplines="{spline}"/>')
    o = f'<g transform="rotate({a0} {POLE[0]} {POLE[1]})" stroke-linecap="round" fill="none">{anim}'
    for i, (w, col) in enumerate(((17, "#a4aab8"), (27, "#d6d8d8"), (44, "#f6f0d8"))):
        g = groups_in.get(i) if groups_in else None
        op = ' opacity="0"' if g else ""
        o += (f'<path d="{_star_paths()[i]}" stroke="{col}" '
              f'stroke-width="{w}"{op}>{C.fade(*g) if g else ""}</path>')
    return o + "</g>"


def far_stars(fade_in):
    """The stars of 3:24, over the far ranges, as in 2:1's sky: 96 pips coming out one group after
    another, `fade_in` = (t, dur)."""
    r = random.Random(1907)
    groups = [[], [], [], []]
    for _ in range(96):
        x, y = r.uniform(-2500, 2500), r.uniform(-1300, 760)
        groups[r.randrange(4)].append(f"M{x:.0f} {y:.0f}h.001")
    out = ""
    for i, (g, w) in enumerate(zip(groups, (9, 7, 11, 6))):
        p = (f'<path fill="none" stroke="#e6e2c8" stroke-width="{w}" stroke-linecap="round" '
             f'd="{"".join(g)}"/>')
        out += f'<g opacity="0">{C.fade(fade_in[0] + fade_in[1] * i / 4, .5)}{p}</g>'
    return out


# ---------------------------------------------------------------------------
# Dusk: the light goes once, on "cool" in 3:8, and it is dusk for every verse after
# ---------------------------------------------------------------------------

_DUSK = "#0e1226"
_DUSK_OP = .3
_DUSK_RGB = (14, 18, 38)
_DUSK_S = 1.5                       # the light going, 3:8


def dimmed(svg):
    """The scenery at dusk: every colour in it mixed toward the dusk. Costs no overdraw, and leaves
    the people, drawn after it, at their full brightness."""
    return G.tinted(svg, _DUSK_RGB, _DUSK_OP)


def dusk_svg(t):
    """3:8's rect under the cast, from t = (begin, dur), so that they stay bright."""
    x0, w = G.CARD_X[0], G.CARD_X[1] - G.CARD_X[0]
    y0, h = G.CARD_Y[0], G.CARD_Y[1] - G.CARD_Y[0]
    return (f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="{_DUSK}" '
            f'fill-opacity="{_DUSK_OP}" opacity="0">'
            f'{C.fade(*t)}</rect>')


_TAG = re.compile(r"<(/?)[\w:]+\b[^>]*?(/?)>")
_REF = re.compile(r'(href="#|url\(#)([^")]+)')
_ID = re.compile(r'\bid="([^"]+)"')


def _by_id(defs):
    """{id: element}, in order, for each element at the top of a run of svg that has one."""
    out, depth, start = {}, 0, 0
    for m in _TAG.finditer(defs):
        if m.group(1):
            depth -= 1
            end = m.end() if depth == 0 else None
        elif m.group(2):
            end = m.end() if depth == 0 else None
            start = m.start() if depth == 0 else start
        else:
            start = m.start() if depth == 0 else start
            depth += 1
            end = None
        if end is not None:
            el = defs[start:end]
            i = _ID.search(el[:el.index(">")])
            if i:
                out[i.group(1)] = el
    return out


def _front_at_dusk(defs, front):
    """Scene.front as the dusk has it, dimmed, and the drawings it uses from the defs, dimmed under
    ids of their own: (those defs, that front). The front itself, under it, keeps its ids."""
    have = _by_id(defs)
    need, todo = set(), [r for _k, r in _REF.findall(front)]
    while todo:
        i = todo.pop()
        if i in have and i not in need:
            need.add(i)
            todo += [r for _k, r in _REF.findall(have[i])]
    ids = need | set(_ID.findall(front))

    def renamed(s):
        s = _ID.sub(lambda m: f'id="{m.group(1)}-d"' if m.group(1) in ids else m.group(0), s)
        return _REF.sub(lambda m: m.group(1) + m.group(2) + ("-d" if m.group(2) in ids else ""), s)
    return (dimmed(renamed("".join(el for i, el in have.items() if i in need))),
            dimmed(renamed(front)))


# ---------------------------------------------------------------------------
# What stays at his plot once the ground is cursed
# ---------------------------------------------------------------------------

_DRY_DEF = ('<radialGradient id="dryg"><stop offset="0" stop-color="#5c4c30" stop-opacity=".95"/>'
            '<stop offset=".55" stop-color="#5c4c30" stop-opacity=".78"/>'
            '<stop offset="1" stop-color="#5c4c30" stop-opacity="0"/></radialGradient>')
_MOUND_CRACKS = ("M0 0C-14 3 -30 2 -46 8C-60 13 -78 12 -96 18",
                 "M0 0C10 4 24 5 40 12C52 18 70 18 88 26",
                 "M0 0C-6 -3 -20 -6 -34 -6C-44 -6 -60 -10 -74 -9",
                 "M0 0C8 -3 22 -5 34 -4C48 -3 56 -7 72 -7", "M-46 8C-52 18 -48 26 -58 34")


def plot_mark(t=None):
    """Where the stick went in: a small dark mark in the ground, and it stays."""
    m = f'<path d="M{SHOOT_X - 9} {gy(SHOOT_X) + 6:.0f}q9 -4 18 0q-9 5 -18 0z" fill="#2a2418"/>'
    if t is None:
        return m
    return f'<g opacity="0">{C.fade(t, .12)}{m}</g>'


def dry_patch(t=None):
    """A dry patch about his plot: the ground's own colour, one gradient on one shape, under the
    cast. The garden goes on being green beyond it. With `t` it spreads."""
    x, y = SHOOT_X - 20, gy(SHOOT_X) + 26
    el = '<ellipse cx="0" cy="0" rx="420" ry="74" fill="url(#dryg)"/>'
    if t is None:
        return f'<defs>{_DRY_DEF}</defs><g transform="translate({x} {y:.0f})">{el}</g>'
    return (f'<defs>{_DRY_DEF}</defs><g transform="translate({x} {y:.0f})"><g transform="scale(0)">'
            '<animateTransform attributeName="transform" type="scale" values="0;1" '
            f'begin="{t:.2f}s" dur="2.60s" fill="freeze" calcMode="spline" keyTimes="0;1" '
            f'keySplines=".2 .5 .4 1"/>{el}</g></g>')


CRACK_REACH = 230                   # how far a crack can reach from its x


def _crack_run(x0, x1):
    """The cracks east from his plot: (x, drawn where it lies), one a little after another."""
    r = random.Random(17)
    paint = {"crack": (None, (30, 24, 18), 2.2)}
    x = x0
    while x < x1:
        y = G.ground_y(x) + r.uniform(-34, 62)
        art = G.render(G.cracks(r, r.uniform(170, 260)), paint, s=1, prec=0)
        yield x, f'<g transform="translate({x:.0f} {y:.0f})">{art}</g>'
        x += r.uniform(70, 130)


def cracks_wave(fl, t0, x0, x1):
    """3:17: the cracks, each coming when the crack head reaches its x. The head goes slowly while
    the camera holds on his plot, then runs ahead of the camera, so that the camera follows it."""
    def head(t):
        return max(x0 + 230 * (t - t0), fl.at(t)[1] + 260)
    grid = [t0 + i * .02 for i in range(int((fl.dur + 1 - t0) / .02))]
    out = ""
    for x, art in _crack_run(x0, x1):
        t = next((q for q in grid if head(q) >= x), grid[-1])
        out += f'<g opacity="0">{C.fade(t, .35)}{art}</g>'
    return out


def dead_sprout(t=None):
    """The shoot of 2:15 with its foot at the origin, at life: lying over, dry, or with `t` wilting
    where it stands, over a second."""
    if t is None:
        return G.render(F.sprout(False, s=PXU), G.DEAD_SPROUT_PAINT, s=1, prec=2, curve=False)
    live_s, live_f = G.SPROUT_PAINT["stem"][1], G.SPROUT_PAINT["leaf"][0]
    dry_s, dry_f = G.DEAD_SPROUT_PAINT["stem"][1], G.DEAD_SPROUT_PAINT["leaf"][0]
    dry_edge = G.DEAD_SPROUT_PAINT["leaf"][1]
    timing = f'begin="{t:.2f}s" dur="1.00s" fill="freeze"'
    parts = F.sprout(s=PXU)
    stem = G.render(parts[:1], {"stem": (None, live_s, 1.0)}, s=1, prec=2, curve=False)
    leaves = G.render(parts[1:], {"leaf": (live_f, live_s, .5)}, s=1, prec=2, curve=False)
    body = (stem[:-2] + '><animate attributeName="stroke" '
                        f'values="{G._hex(live_s)};{G._hex(dry_s)}" {timing}/></path>'
            + leaves[:-2] + '><animate attributeName="fill" '
                            f'values="{G._hex(live_f)};{G._hex(dry_f)}" {timing}/>'
                            '<animate attributeName="stroke" '
                            f'values="{G._hex(live_s)};{G._hex(dry_edge)}" {timing}/></path>')
    return ('<g><animateTransform attributeName="transform" type="rotate" values="0;-30;-22;-62" '
            f'keyTimes="0;.4;.6;1" {timing}/>{body}</g>')


# Where they stood as the leaves came off, 3:21: (x, y, how far each lands from the middle of them)
FALLEN = ((M_PLOT, gy(M_PLOT), -7), (M_PLOT, gy(M_PLOT), 6),
          (W_RULE, gy(W_RULE, True), -6), (W_RULE, gy(W_RULE, True), 5))


def fig_leaf(r, edge, vein, curve=True):
    """A leaf of the near fig: at z 7 in 3:7's hands, and small as it comes off them at 3:21."""
    paint = {"leaf": ((88, 126, 62), (216, 226, 164), edge), "vein": (None, (190, 208, 140), vein)}
    return G.render(G.fig_leaf(r), paint, s=1, curve=curve, prec=1)


def fallen_at(px, py, dx):
    """Where a leaf that came off at (px, py) lies, just in front of their feet, and its turn."""
    return (px + dx + (4 * (dx > 0) - 2), py + 4), 180 + dx * 3


def fallen_leaves(rect):
    """What 3:21 leaves on the ground at their feet, at dusk, and it stays: the leaves a camera over
    `rect` can see."""
    leaf = dimmed(fig_leaf(9, .4, .3, curve=False))
    o = ""
    for px, py, dx in FALLEN:
        (x, y), rot = fallen_at(px, py, dx)
        if G._meets(rect, x - 12, y - 12, x + 12, y + 12):
            o += f'<g transform="translate({x} {y})"><g transform="rotate({rot})">{leaf}</g></g>'
    return o


def after_curse(rect=None):
    """What stays at his plot from 3:17 on: the patch, the cracks, the shoot lying over. The cracks
    a camera over `rect` can't reach are left out."""
    x0, x1 = (rect[0] - CRACK_REACH, rect[2] + CRACK_REACH) if rect else (SHOOT_X, 2800)
    return (dry_patch() + "".join(art for x, art in _crack_run(SHOOT_X, 2800) if x0 <= x <= x1)
            + f'<g transform="translate({SHOOT_X} {gy(SHOOT_X) + 4:.1f}) '
              f'scale(2.2)">{dead_sprout()}</g>')


def way_ribbon(t, d):
    """3:24: the worn way itself warms, from the wheel back to the foot of the tree of life, a
    tapered shape on the ground under the trunks. Not a line laid over the picture."""
    xs = list(range(int(WHEEL_X), -360, -160)) + [-360]
    n = len(xs) - 1
    o = ""
    for i in range(n):
        a, b = xs[i], xs[i + 1]
        wa, wb = 30 - 16 * i / n, 30 - 16 * (i + 1) / n
        ya, yb = G.ground_y(a) + 12, G.ground_y(b) + 12
        o += (f'<path d="M{a + 1} {ya - wa / 2:.1f}L{b} {yb - wb / 2:.1f}L{b} {yb + wb / 2:.1f}'
              f'L{a + 1} {ya + wa / 2:.1f}Z" fill="#c8b478" opacity="0">'
              f'{C.fade(t + d * i / n, .35)}</path>')
    return o


# ---------------------------------------------------------------------------
# The hands. One hand, one fruit, four times
# ---------------------------------------------------------------------------

def hand_svg(track, skin, lw, reach=0.0):
    """A hand as paths that morph along `track`: [(0, pose), (t, dur, pose), ...], holding each pose
    until its t. Returns (behind, front), so that a fruit can go between the palm and the fingers.
    No line across the wrist: a patch of the skin over the join. `reach` draws the forearm that
    much longer, so that its end is past the frame's edge."""
    shapes0 = F.hand(track[0][-1], s=PXU)
    shapes0["arm"] = [(x - reach if x < -60 else x, y) for x, y in shapes0["arm"]]
    out = {}
    for name in ("arm", "palm", "th", "f0", "f1", "f2", "f3"):
        d0 = G._d([(x, -y) for x, y in shapes0[name]])
        anim = ""
        prev = d0
        for t, dur, pose_ in track[1:]:
            d1 = G._d([(x, -y) for x, y in F.hand(pose_, s=PXU)[name]])
            if name != "arm" and d1 != prev:
                anim += (f'<animate attributeName="d" values="{prev};{d1}" begin="{t:.2f}s" '
                         f'dur="{dur:.2f}s" fill="freeze" calcMode="spline" keyTimes="0;1" '
                         'keySplines=".42 0 .58 1"/>')
            prev = d1
        out[name] = (f'<path fill="{G._hex(skin)}" stroke="{G._hex(PAINTS["live"]["ink"])}" '
                     f'stroke-width="{lw}" '
                     'stroke-linejoin="round" '
                     f'd="{d0}">{anim}</path>')
    patch = "M" + "L".join(f"{x:g} {-y:g}" for x, y in shapes0["patch"]) + "Z"
    return (out["arm"] + out["palm"] + f'<path d="{patch}" fill="{G._hex(skin)}"/>',
            out["f3"] + out["f2"] + out["f1"] + out["f0"] + out["th"])


def hand_at(wx, wy, ang, track, moves="", flip=1, skin=PAINTS["live"]["skin"], k=1.0, vflip=False,
            tilt="", reach=0.0):
    """A morphing hand with its wrist at (wx, wy), its forearm running at `ang` degrees (screen) ->
    (behind, front). `moves` is an animateTransform for a whole-hand move. `flip` -1 mirrors it (a
    hand coming from the east). `k` narrows it (hers is .88). `vflip` turns it palm down. `tilt`
    rotates it about the wrist. `reach` lengthens the forearm (`hand_svg`)."""
    sc = f" scale({flip} 1)" if flip != 1 else ""
    sk = f"scale({k:g} {-k if vflip else k:g})" if (k != 1.0 or vflip) else ""
    b, f_ = hand_svg(track, skin, .3 / k, reach)
    tf = f"translate({wx:.2f} {wy:.2f}){sc} rotate({ang:.1f})"

    def placed(s):
        s = f'<g transform="{sk}">{s}</g>' if sk else s
        s = f'<g>{tilt}{s}</g>' if tilt else s
        return f'<g>{moves}<g transform="{tf}">{s}</g></g>'
    return placed(b), placed(f_)


def reach_hand(woman, x, moves, track, ang_add=-2):
    """The hand of one standing at x, reaching for the low fruit."""
    wx, wy, ang = hand_xy(woman, "take", x, gy(x, woman))
    if woman:
        return hand_at(wx, wy, ang + ang_add, track, moves, k=.88, skin=HER_SKIN)
    return hand_at(wx, wy, ang + ang_add, track, moves)


# ---------------------------------------------------------------------------
# The plates
# ---------------------------------------------------------------------------

_MBG = ('<linearGradient id="mbg" gradientUnits="userSpaceOnUse" x1="0" y1="1262" x2="0" y2="1392">'
        '<stop offset="0" stop-color="#4c504e"/>'
        '<stop offset=".26" stop-color="#4e5650"/><stop offset=".42" stop-color="#3e5a3c"/><stop '
        'offset="1" stop-color="#355034"/></linearGradient>')


def fruit_plate(fl, hands="", with_fruit=True, fruit_extra="", front=""):
    """All that a camera at `fruit` can see, drawn again with thin lines: the air and the grass
    behind, the bough's tip and its leaves, the three low fruit, what the hand is doing. `hands` =
    (behind the fruit, in front of it). `fruit_extra` animates the fruit in its group. 2:17, 3:3,
    3:6 and, bare, 3:11."""
    x0, y0, x1, y1 = FRUIT_X - 130, 1262, FRUIT_X + 120, 1392
    bg = (f'<defs>{_MBG}</defs><rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" '
          'fill="url(#mbg)"/>'
          f'<path d="M{x0} 1330C{x0 + 60} 1327 {x0 + 120} 1334 {x1} 1331M{x0} 1357C{x0 + 90} '
          f'1353 {x0 + 160} 1361 {x1} 1358M{x0} 1299C{x0 + 80} 1297 {x0 + 170} 1302 {x1} 1300" '
          f'fill="none" stroke="#7c8460" stroke-width=".35"/>')
    tips = G.knowledge_tips(FRUIT_X - 40, FRUIT_X + 90, 1260, 1330)
    others = "".join(f'<g transform="translate({q[1]:.2f} {q[2]:.2f})">{G.fruit_macro()}</g>'
                     for q in (FRUIT4, FRUIT5))
    back, fr = hands if hands else ("", "")
    main = ""
    if with_fruit:
        main = (f'<g transform="translate({FRUIT_X:.2f} {FRUIT_Y:.2f})">'
                f'<g>{fruit_extra}{G.fruit_macro()}</g></g>')
    return plate(fl, bg + tips + others + back + main + fr + front, 5.8)


def stem_plate(fl, t_cmd=None):
    """The bare stem, hung by him (`stem`): pale on a dark keyline so that it stands off the leaf,
    with the outline of what was there, held at the floor to the verse's end, and going with the
    plate. It says: this one is gone. `dimmed` leaves the outline's highlight as it is."""
    fx = sway(t_cmd + .1, 1.8, 9) if t_cmd is not None else ""
    if t_cmd is None:
        gone = (f'<circle cx="{FRUIT_C[0]:.1f}" cy="{FRUIT_C[1]:.1f}" r="8.2" fill="none" '
                f'stroke="{C.rgb(HL)}" stroke-width=".7" opacity=".6"/>')
    else:
        gone = (f'<circle cx="{FRUIT_C[0]:.1f}" cy="{FRUIT_C[1]:.1f}" r="8.2" fill="none" '
                f'stroke="{C.rgb(HL)}" stroke-width=".7" opacity="0">'
                '<animate attributeName="opacity" values="0;1;1;.6" keyTimes="0;.25;.6;1" '
                f'begin="{t_cmd:.2f}s" dur="1.4s" fill="freeze"/></circle>')
    stem = (f'<g transform="translate({FRUIT_X:.2f} {FRUIT_Y:.2f})"><g>{fx}'
            '<path d="M0 0Q1.2 5 .3 11.5" fill="none" stroke="#1c1610" stroke-width="2.1"/>'
            '<path d="M0 0Q1.2 5 .3 11.5" fill="none" stroke="#f0e2b8" stroke-width="1.15"/>'
            '<path d="M-.9 11.2L1.4 12.2" fill="none" stroke="#f0e2b8" stroke-width=".7"/></g></g>')
    return (f'<g transform="translate({STEM_DX:.1f} {STEM_DY:.1f})">'
            + dimmed(fruit_plate(fl, with_fruit=False, front=stem + gone)) + "</g>")


_RULE_HER = ((2.0, 13.0), 16.0)     # where hers ends: down, and its wrist dropped
RULE_ON = 3.0                       # 3:16: the camera is on neither plate, and they change over
_RULE_HIS = (-23.0, 8.0)
_HIS_FROM, HIS_IN_S = (60.0, 8.0), .3   # his hand comes in from past the frame's edge, on "and"


def hands_ground(mid, hy, half, fill):
    """The ground of a plate of two hands, 2:23 and 3:16: flat, with two faint lines of the land."""
    x0, y0, x1, y1 = mid - 120, hy - half, mid + 120, hy + half
    return (f'<rect x="{x0}" y="{y0:.0f}" width="{x1 - x0}" height="{y1 - y0:.0f}" fill="{fill}"/>'
            f'<path d="M{x0} {hy + 22:.0f}C{x0 + 60} {hy + 19:.0f} {x0 + 150} {hy + 26:.0f} {x1} '
            f'{hy + 22:.0f}M{x0} {hy - 28:.0f}C{x0 + 90} {hy - 31:.0f} {x0 + 160} {hy - 25:.0f} '
            f'{x1} {hy - 28:.0f}" fill="none" stroke="#7c8460" stroke-width=".3"/>')


def _rule_ground(mid, hy):
    return dimmed(hands_ground(mid, hy, 66, "#39543a"))


def rule_plate(fl, t_and, t_rule, dur):
    """3:16. Her hand palm up, narrower and lighter, already out and level as the camera cuts to
    it. His palm down, coming in on "and". On "rule" his goes over and down on hers, all its
    fingers over hers, and hers goes down under it, slowly. Hers is drawn first: none of it shows
    above his."""
    mid, hy = (M_PLOT + W_RULE) / 2, SHOTS["rule"][1] + 2
    her_mv = slide([(0, 0), _RULE_HER[0]], t_rule, dur - .1 - t_rule)
    tilt = ('<animateTransform attributeName="transform" type="rotate" '
            f'values="0;0;{_RULE_HER[1]}" keyTimes="0;.15;1" begin="{t_rule - .1:.2f}s" '
            f'dur="{dur - t_rule - .05:.2f}s" fill="freeze"/>')
    her = hand_at(mid - 26, hy + 4, -6, [(0, "open"), (t_rule - .1, .6, "under")], her_mv, k=.88,
                  skin=HER_SKIN, tilt=tilt)
    # held out of the frame from the verse's start, since before its begin a move is no move at all
    D, came = dur - .1, min(HIS_IN_S, .6 * (t_rule - t_and))
    his_mv = slide([_HIS_FROM, _HIS_FROM, (0, 0), (5, -6), _RULE_HIS], 0, D,
                   [0, t_and / D, (t_and + came) / D, t_rule / D, 1])
    his = hand_at(mid + 26, hy + 4, -6, [(0, "rest"), (t_rule, .6, "cup")], his_mv, flip=-1,
                  vflip=True)
    return plate(fl, _rule_ground(mid, hy) + her[0] + her[1] + his[0] + his[1], 5.0,
                 on_after=RULE_ON)


def rule_rest(fl):
    """3:16's rest, carried so that 3:17 opens on it."""
    mid, hy = (M_PLOT + W_RULE) / 2, SHOTS["rule"][1] + 2
    tilt = ('<animateTransform attributeName="transform" type="rotate" '
            f'values="{_RULE_HER[1]};{_RULE_HER[1]}" dur=".01s" fill="freeze"/>')
    her = hand_at(mid - 26, hy + 4, -6, [(0, "under")], "", k=.88, skin=HER_SKIN, tilt=tilt)
    his = hand_at(mid + 26, hy + 4, -6, [(0, "cup")], "", flip=-1, vflip=True)

    def wrap(q, dx, dy):
        return f'<g transform="translate({dx} {dy})">{q[0]}{q[1]}</g>'
    return plate(fl, _rule_ground(mid, hy) + wrap(her, *_RULE_HER[0]) + wrap(his, *_RULE_HIS), 5.0)


def heel_ground(hx, hy):
    """The heel's plate's own ground, 3:15."""
    x0, y0, x1, y1 = hx - 120, hy - 110, hx + 120, hy + 50
    return (f'<rect x="{x0:.0f}" y="{y0:.0f}" width="{x1 - x0:.0f}" height="{y1 - y0:.0f}" '
            'fill="#47533a"/>'
            f'<path d="M{x0:.0f} {hy - 44:.0f}C{x0 + 70:.0f} {hy - 47:.0f} {x0 + 160:.0f} '
            f'{hy - 41:.0f} {x1:.0f} {hy - 45:.0f}M{x0:.0f} {hy - 18:.0f}C{x0 + 60:.0f} '
            f'{hy - 16:.0f} {x0 + 170:.0f} {hy - 22:.0f} {x1:.0f} {hy - 19:.0f}M{x0:.0f} '
            f'{hy + 16:.0f}C{x0 + 50:.0f} {hy + 14:.0f} {x0 + 150:.0f} {hy + 20:.0f} {x1:.0f} '
            f'{hy + 16:.0f}" fill="none" stroke="#7c8056" stroke-width=".35"/>')


def mound_art(x, y):
    """The mound of 2:7 and 3:19, where it lies, its base near y + 10."""
    parts = F.mound(s=PXU)
    g = G._D(1)
    for kind, data, _m in parts:
        if kind == "dot":
            g.dot(x + data[0], y + 10 - data[1], data[2])
    fill, line, _w = G.MOUND_PAINT["mound"]
    return (f'<path d="{G._d([(x + a, y + 10 - c) for a, c in parts[0][1]])}" '
            f'fill="{G._hex(fill)}" stroke="{G._hex(line)}" stroke-width=".4"/>'
            f'<path d="{G._d([(x + a, y + 10 - c) for a, c in parts[1][1]])}" '
            f'fill="{G._hex(G.MOUND_PAINT["mound_lit"][0])}"/>'
            f'<path fill="{G._hex(G.MOUND_PAINT["grain"][0])}" d="{g.text()}"/>')


# How far the mound's plate's own ground reaches from it: either side, up and down, world px. It
# holds the whole frame from z 4 on, and its land lines run on straight to its edges
MOUND_REACH = (140, 90, 80)


def mound_plate(fl, x, y, t=None):
    """The last of 3:19, and the first of 2:7: dust, a crack, the mound and a few grains, at z 7.
    Its own ground, because closer than z 1.6 the thorns would be all there is: 3:19 cuts to it
    from above them. Shared by 3:20's opening, hung where that verse's camera is. With `t` the mound
    comes up then, the grains falling on it one after another. (x, y) on a whole px."""
    side, up, down = MOUND_REACH
    x0, y0, x1, y1 = x - side, y - up, x + side, y + down
    r = random.Random(19)
    bg = (f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="#544730"/>'
          f'<path d="M{x0} {y + 16}L{x - 110} {y + 16}C{x - 40} {y + 13} {x + 40} {y + 19} '
          f'{x + 110} {y + 16}L{x1} {y + 16}M{x0} {y - 30}L{x - 110} {y - 30}C{x - 30} {y - 33} '
          f'{x + 50} {y - 28} {x + 110} {y - 31}L{x1} {y - 31}" fill="none" stroke="#7a6a48" '
          'stroke-width=".35"/>')
    bg += (f'<g transform="translate({x - 24} {y + 4})" fill="none" stroke="#2c2214" '
           'stroke-width=".8">' + "".join(f'<path d="{c_}"/>' for c_ in _MOUND_CRACKS) + "</g>")
    m = mound_art(x, y)
    if t is not None:
        m = (f'<g transform="translate(0 {y + 8})"><g transform="scale(1 .01)"><animateTransform '
             f'attributeName="transform" type="scale" values="1 .01;1 1" begin="{t:.2f}s" '
             'dur=".7s" fill="freeze"/>'
             f'<g transform="translate(0 {-(y + 8)})">{m}</g></g></g>')
        for i in range(10):
            m += grain_rise(r, x + r.uniform(-24, 28), y - r.uniform(8, 26), y + 4, t - .1
                            + i * .04, .7, spread=5, n=6, col="#c6b088", r=(.35, .8))
    return plate(fl, dimmed(bg) + m, 4.0)


# ---------------------------------------------------------------------------
# The cherubim and the wheel, 3:24
# ---------------------------------------------------------------------------

_CH_BODY = [(-7, 0), (-5.4, 6), (-4.0, 12), (-3.6, 16), (-5.4, 21), (-4.6, 23.5), (-1.8, 25),
            (1.8, 25), (4.6, 23.5), (5.4, 21),
            (3.6, 16), (4.0, 12), (5.4, 6), (7, 0)]
_CH_WING = dict(root=(2, 23), lc1=(6, 36), lc2=(16, 50), tip=(22, 54), tc1=(17, 34), tc2=(8, 22),
                heel=(3, 15),
                feathers=6, lobe=1.1, quills=(2, 4))
_SILVER_LINE, _SILVER_FILL, _SILVER_DEEP = (212, 214, 216), (116, 122, 132), (70, 76, 90)


def cherub_svg(h=176.0):
    """A cherub on the Exodus 25 wing, feet at the origin, about h tall, face on, its head bowed and
    hooded."""
    k = h / 56.0
    outline, quills = feathered_wing(**_CH_WING)

    def P(pts, sx=1):
        return " ".join(f"{sx * x * k:.1f},{-y * k:.1f}" for x, y in pts)
    o = ""
    for sx in (-1, 1):
        o += (f'<polygon points="{P(outline, sx)}" fill="{G._hex(_SILVER_DEEP)}" '
              f'stroke="{G._hex(_SILVER_LINE)}" stroke-width="1.6" '
              f'stroke-linejoin="round"/>')
        for q in quills:
            o += (f'<polyline points="{P(q, sx)}" fill="none" stroke="{G._hex(_SILVER_LINE)}" '
                  'stroke-width="1.1"/>')
    o += (f'<polygon points="{P(_CH_BODY)}" fill="{G._hex(_SILVER_FILL)}" '
          f'stroke="{G._hex(_SILVER_LINE)}" stroke-width="1.6" '
          f'stroke-linejoin="round"/>')
    # the head bowed under a hood: a cowl taller than it is wide, its back running down onto the
    # shoulders, its front edge drawn down over the place of the face, and only shade under that
    hood = F.smooth([(-5.0, 21.4), (-5.8, 25.4), (-5.4, 30.2), (-3.8, 34.4), (-1.4, 36.8),
                     (1.4, 36.8), (3.8, 34.4), (5.4, 30.2), (5.8, 25.4), (5.0, 21.4), (0, 22.4)],
                    n=3)
    shade = F.smooth([(-3.4, 30.6), (0, 27.4), (3.4, 30.6), (2.8, 27.0), (0, 24.6), (-2.8, 27.0)],
                     n=3)
    brim = F.smooth([(-4.4, 32.4), (-2.0, 29.2), (0, 27.4), (2.0, 29.2), (4.4, 32.4)],
                    closed=False, n=3)

    def d(pts):
        return G._d([(x * k, -y * k) for x, y in pts])
    o += (f'<path d="{d(hood)}" fill="{G._hex(_SILVER_FILL)}" stroke="{G._hex(_SILVER_LINE)}" '
          'stroke-width="1.5" stroke-linejoin="round"/>'
          f'<path d="{d(shade)}" fill="{G._hex(_SILVER_DEEP)}"/>'
          '<path d="M' + "L".join(f"{x * k:.1f} {-y * k:.1f}" for x, y in brim)
          + f'" fill="none" stroke="{G._hex(_SILVER_LINE)}" stroke-width="1.1" '
            'stroke-opacity=".8"/>')
    for pts in ([(-5.2, 21.5), (0, 19.8), (5.2, 21.5)], [(-4.0, 14), (0, 13.4), (4.0, 14)],
                [(-2.2, 13), (-2.6, 6), (-2.2, .6)], [(2.2, 13), (2.6, 6), (2.2, .6)]):
        o += (f'<polyline points="{P(pts)}" fill="none" stroke="{G._hex(_SILVER_LINE)}" '
              'stroke-width="1.1" stroke-opacity=".8"/>')
    return o


def _tongue(a_deg, r0, r1, sweep, half):
    def pol(r, deg):
        rad = math.radians(deg)
        return r * math.cos(rad), r * math.sin(rad)

    def f(p):
        return f"{p[0]:.1f} {p[1]:.1f}"
    b1, b2 = pol(r0, a_deg - half), pol(r0, a_deg + half)
    tip = pol(r1, a_deg + sweep)
    c1 = pol((r0 + r1) * .55, a_deg + sweep * .3 - half * .7)
    c2 = pol((r0 + r1) * .55, a_deg + sweep * .8 + half * .9)
    return f"M{f(b1)}Q{f(c1)} {f(tip)}Q{f(c2)} {f(b2)}Z"


_FLAME_RED, _FLAME_GOLD = (214, 86, 40), (246, 178, 76)


def wheel_svg(r, period, begin):
    """The flaming sword of 3:24, a wheel of flame turning forever: the one loop in the chapters.
    Never a blade. Seven long uneven tongues, five bright inner ones and a bright core."""
    o = ('<animateTransform attributeName="transform" type="rotate" values="0;360" '
         f'dur="{period:g}s" begin="{begin:g}s" '
         f'repeatCount="indefinite" additive="sum"/>')
    for k in range(7):
        r1 = 40 if k % 2 == 0 else 29
        o += (f'<path d="{_tongue(k * 360 / 7, 12, r1, 42, 7)}" fill="{G._hex(_FLAME_RED)}" '
              f'stroke="{G._hex(_FLAME_GOLD)}" stroke-width="1.2"/>')
    for k in range(5):
        o += (f'<path d="{_tongue(k * 72 + 18, 6, 21, 34, 6)}" fill="{G._hex(_FLAME_GOLD)}" '
              f'stroke="{G._hex(HL)}" stroke-width="1"/>')
    o += f'<circle r="6.5" fill="{G._hex(HL)}" stroke="{G._hex(_FLAME_GOLD)}" stroke-width="1.5"/>'
    return f'<g transform="scale({r:g})"><g>{o}</g></g>'


# ---------------------------------------------------------------------------
# The ground under each verse
# ---------------------------------------------------------------------------

def water(ref):
    """Rule 24: the water runs for the length of each verse from 2:15 to 3:5, and only the near
    reach does. A verse with a water of its own, 3:6's stop and 3:20's once more, hands `garden` its
    `flow`."""
    if (2, 15) <= cv(ref) <= (3, 5):
        return (0.0, round(verse_dur(ref), 2))
    return None


def bind_slivers(s, fl):
    """The side view's slivers are detail: they come in with the camera over z .42-.54, and aren't
    in the file if the verse stays wider."""
    ops = [clamp((c[0] - .42) / .12) for c in fl.cams]

    def fix(text):
        if not text or 'data-sl="1"' not in text:
            return text
        if max(ops) <= 0:
            return re.sub(r'<g data-sl="1">.*?</g>', "", text, flags=re.S)
        if min(ops) >= 1:
            return text.replace('<g data-sl="1">', "<g>")
        vals = [f"{o:.2f}" for o in ops]
        return text.replace('<g data-sl="1">',
                            f'<g opacity="{vals[0]}">{fl._anim("opacity", vals)}')
    return G.Scene(fix(s.defs), fix(s.behind), fix(s.front), fix(s.outside))


_FAR_THORNS_S = 1.5                 # the far land coming up thorny, 3:18


def fig_and_twig(ref):
    """The low bough on the tree of life, the near fig and its figs: two from 2:16 on."""
    return G.life_twig_svg() + G.fig_near_svg() + G.figs_svg(taken=cv(ref) >= (2, 16))


@functools.lru_cache(maxsize=8)
def _planted(flow, thorns):
    return G.panorama("planted", lean=True, heroes=False, flow=flow, flow_reaches=("near",),
                      thorns_too=thorns)


def garden(fl, ref, extra="", under_heroes="", flow=None, fruit_off=None, light_goes=None,
           thorns_in=None, hung=False):
    """The planted side view for a verse: trimmed to its flight, the two trees, the near fig, the
    low bough, the shrubs in front. Running water as `water` says, or as `flow` says; his plot's
    mark from 2:15; the bare stem from 3:6; what stays after the curse from 3:17; the thorns from
    3:18; the fig leaves where they fell at their feet, from 3:22, in front of them; the light going
    once, at 3:8, and dusk from 3:9 by mixing the scenery's colours, so the cast stays bright.
    `extra` goes after the near fig, and `under_heroes` before the two trees.
    The three that happen here are the verse's to time, on its cues: `fruit_off`, when the fruit
    leaves the tree (3:6); `light_goes`, when the light starts to go (3:8); `thorns_in`, when the
    far land, the near thorns and the thistles come up (3:18). `hung`: the verse hangs in the plan
    (`seen`)."""
    at = cv(ref)
    thorns = at >= (3, 18)
    land = _planted(flow or water(ref), thorns)
    rect = seen(fl, hung)
    t = bind_slivers(land.trimmed(rect, keep=SIDE_KEEP + ("ta", "tb")), fl)
    t.behind += under_heroes
    if (2, 15) < at <= (3, 17):
        t.behind += plot_mark()
    if fruit_off is not None:
        keep_kf = G.place("kf", FRUIT_X, FRUIT_Y)
        t.behind += (G.in_frame(G.heroes_svg(taken=(G.TAKE_FRUIT,)), rect, land.defs)
                     + f'<g>{keep_kf}<set attributeName="visibility" to="hidden" '
                       f'begin="{fruit_off:.2f}s"/></g>')
    else:
        t.behind += G.in_frame(G.heroes_svg(taken=(G.TAKE_FRUIT,) if at > (3, 6) else ()), rect,
                               land.defs)
    t.behind += fig_and_twig(ref) + extra
    if at > (3, 17):
        t.behind += after_curse(rect)
    if thorns_in is not None:
        far, near, thistles = thorns_in
        # hidden until it comes in, not only transparent: Chromium paints whatever lies over a
        # group at opacity 0 a little softer, and the stone man would change at the seam with 3:17
        t.outside = (f'<g opacity="0" visibility="hidden">{C.fade(far, _FAR_THORNS_S)}'
                     f'<set attributeName="visibility" to="visible" begin="{far:.2f}s"/>'
                     f'{t.outside}</g>' + G.thorns_near(near, thistles))
    elif thorns:
        t.outside += G.thorns_near()
    t.front += G.shrubs_svg()
    if light_goes is not None:
        # under the cast a rect, so that they stay bright; over it, the front as the dusk has it
        # comes in over the front, which goes when it is whole: the last frame is 3:9's first
        t.behind += dusk_svg((light_goes, _DUSK_S))
        defs, front = _front_at_dusk(t.defs, t.front)
        t.defs += defs
        t.front = (f'<g><set attributeName="visibility" to="hidden" '
                   f'begin="{light_goes + _DUSK_S:.2f}s"/>{t.front}</g>'
                   f'<g opacity="0">{C.fade(light_goes, _DUSK_S)}{front}</g>')
    elif at >= (3, 9):
        t.defs, t.behind, t.outside, t.front = (dimmed(t.defs), dimmed(t.behind),
                                                dimmed(t.outside), dimmed(t.front))
    if at > (3, 21):
        t.front += fallen_leaves(rect)
    return t


# ---------------------------------------------------------------------------
# The build
# ---------------------------------------------------------------------------

class Story:
    """The chapters built so far, on one card: all their events are on it, so that a verse's state
    is what the ones before it left."""

    def __init__(self, card, verses):
        self.card, self.verses = card, verses
        self.drawn = {}             # {ref: the Flight it was last drawn on}: see VerseFlight

    def verse_file(self, ref):
        """The verse's whole SVG."""
        v = self.verses[ref]
        fl = self.drawn[ref] = v.flight()
        if v.plan_only:
            body = v.plan(fl)
        else:
            sc = v.scene(fl) if v.scene else garden(fl, ref)
            under = "".join(f(fl) for f in v.under)
            over = "".join(f(fl) for f in v.over)
            scene = G.Scene(sc.defs, sc.behind + under, sc.front, sc.outside)
            body = self.card.verse_svg(ref, fl, scene, over)
            if v.plan:
                body = G.hang_in_plan(fl, v.plan(fl), body)
            if v.world_over:
                body += v.world_over(fl)
        return ('<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="576" '
                'viewBox="0 0 1024 576" font-family="Georgia,serif" '
                'stroke-linecap="round" stroke-linejoin="round"><rect width="1024" height="576" '
                f'fill="{G._hex(G.SKY_TOP)}"/>'
                + fl.open_camera() + body + "</g></g>"
                + C.title_svg(TITLE.format(cv(ref)[0]), NAME_INK) + "</svg>")


def build_story(say=say):
    """Both chapters' verses in order, on one Stage. Each chapter's module registers its verses as
    it is imported, and each verse opens on the last one's rest, so that the chapters play as one
    flight. Nothing is drawn yet: that is Story.verse_file. `say` is what the verses' cues ask for a
    word's time: one that returns None, or None itself, leaves each beat at its value on today's
    MP3."""
    card = Stage()
    add_cast(card)
    verses, cam = {}, OPENING
    for chapter, module in CHAPTERS.items():
        importlib.import_module(module)
        for ref in chapter_refs(chapter):
            v = Verse(ref, cam, say)
            VERSES[ref](v, card)
            verses[ref] = v
            cam = v.flight().cam1
    card.refs = list(verses)
    return Story(card, verses)


def write_story(out_dir=None):
    """Draws the whole story and puts it through garden_qc.py, printing its report and each
    failure's verse and what failed. If all of it is clear, writes every verse of both chapters,
    each through generate_tabernacle.out_path into its chapter's folder, or all into `out_dir`, and
    returns their paths. Both, always: chapter 3 opens where chapter 2 ends and shares its shots, so
    a change to either can move the other. If anything has failed, writes nothing and returns []."""
    import garden_qc
    story = build_story()
    files = {ref: story.verse_file(ref) for ref in story.verses}
    problems, report = garden_qc.run(story, files)
    for line in report + problems:
        print(line, flush=True)
    if problems:
        print(f"{len(problems)} QC failures: nothing written")
        return []
    paths = []
    for n in CHAPTERS:
        written = []
        for ref in chapter_refs(n):
            name = f"{BOOK}_{n}_{cv(ref)[1]}.svg"
            path = os.path.join(out_dir, name) if out_dir else out_path(BOOK, n, name)
            with open(path, "w", encoding="utf-8") as f:
                f.write(files[ref])
            written.append(path)
        print(f"{BOOK} {n}: {len(written)} SVG files, "
              f"{sum(os.path.getsize(p) for p in written) / 1024:.0f} KB")
        paths += written
    return paths
