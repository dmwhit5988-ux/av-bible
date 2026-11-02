"""What must be clear before garden_stage.write_story writes a file of Genesis 2-3.

    problems, report = garden_qc.run(story, files)      # files: {ref: svg}, the whole story

Each check names the verse and what failed. Nothing is written if any of them has anything to say.
All of it reads what is really there, the files as they would be written and the Flight each was
drawn on, and every number is a rule of the design:

    name_air            At a verse's rest, and on the frames a name is first and last whole: its ink
                        box (the real Georgia advance) inside the frame by 2 px, or wholly out of
                        it, clear of the title plate, and 3 px clear of every other name and of
                        every shown person's points, unless a plate is over them. So a name a camera
                        leaves goes before it is cut.
    figures_in_frame    At a rest, every shown person and creature is in frame, or a plate is over
                        them. AWAY is who the camera has left behind on purpose; CLOSE_SHOT says how
                        much of a person a close shot must hold, so a man lying across 2:21's frame
                        is only his chest.
    the_floor           Every .05 s along the flight, anyone shown and in frame, at z under 4.5, is
                        at least 40 px: the card's people (PEOPLE), and those drawn by hand, the
                        stone and the living (the Flight's figures), anywhere along their way.
    budget              Under 350 KB, 130 animations and 268 <text> a file.
    still_time          Seconds after the last finite animation. The chapters may not pass 10% not
                        counting the water, nor a verse 1.5 s, but NAMED_STILL.
    stills_anywhere     The longest time anywhere in a verse with nothing moving, the water aside
                        and the camera counting, under 2 s, but NAMED_STILL.
    camera_speed        From the baked keys: no verse's camera peaks over 1200 px/s across the
                        screen or 3.3/s in zoom. A cut is an edit, not a move.
    camera_legs         No leg runs backward, begins before the last one ends, or ends after the
                        narration: a leg by hand that a re-rendered word has crossed. Only a cut
                        takes no time.
    one_loop            repeatCount="indefinite" in 3:24 and nowhere else, and no finite animation
                        ends after the narration.
    his_name            From .3 s before "Yahweh" or "God" until the next word, no animation and no
                        camera leg or cut begins, nothing that has held or is going one way sets off
                        again or turns back, and nothing comes or goes by a <set> or a switch, a
                        plate's among them. What is baked on the camera's keys moves with it, and
                        its legs answer for that. A wave already under way may carry on
                        (UNDER_WAY), and so may a walk carried over the seam from the verse before.
    poses_on_the_list   Every pose of the pair and the stone men is on POSES, and everything on
                        POSES is there. A stride's own start and stop aren't listed: the walk is the
                        event. With a clock, a pose is also within POSE_WORD_S of its word.
    file_rules          No filter, mask, script, style, image, tspan, xlink or external reference;
                        ids unique; every href and url() resolves; the head of the file; it parses.
    key_times           Non-decreasing, first 0, last 1 unless discrete; values (and keyPoints) and
                        keyTimes the same length; keySplines one fewer; no negative time, which is
                        what a fixed length that no longer fits between two words comes to.

Man's size is reported, not failed. The rest wants real frames and is run by hand: the seams between
verses, and the names by pixel difference, for what geometry can't see, are
tools/garden_seams.py.

POSES is for the owner to read. A change to it is a change to the design.
"""

import math
import re
import statistics
from collections import Counter, namedtuple
from xml.dom import minidom

import garden_stage as S
import svg_map_camera as C
import svg_scene_card as SC

W, H = C.W, C.H
AIR = 3.0                   # px of air round a name
NAME_IN_S = S.NAME_IN_S     # how long a name takes to come in: `name_at`
FRAME_MARGIN = 2.0          # how far inside the frame a name must be
MAX_KB, MAX_ANIMS, MAX_TEXTS = 350, 130, 268
STILL_SHARE, STILL_VERSE_S, STILL_ANYWHERE_S = .10, 1.5, 2.0
NAMED_STILL = {"2:2"}       # he rested: the wheel stops on the word, and nothing moves after it
PAN_MAX, ZOOM_MAX = 1200.0, 3.3
FLOOR_PX, MAN_PX = 40.0, 110.0
PLATE_Z = 4.5               # the floor's limit: past this what you see is a plate, or bare ground
NAME_LEAD = .3              # a beginning just before his name still reads as answering it
POSE_WORD_S = 1.0           # how far a pose may be from the word POSES hangs it on
PEOPLE = ("man", "wom", "dig", "lest")

# The camera has followed the crack east to the stone man, and they stand behind it at his plot
AWAY = {"3:17": ("man", "wom"), "3:18": ("man", "wom")}
CLOSE_SHOT = 2.0            # from this zoom a person must be in frame from the hips up: rule 12
HIPS = .5                   # how far up a person the hips are
# Rule 9's wave, already going when his name is said: 2:9's plain trees rising, by their drawings.
# The other thing that may carry on, 2:21's beasts walking off, is a walk carried over a seam, which
# `_under_way` finds on the card. Nothing else may begin there
UNDER_WAY = {"2:9": ("s", "o", "f", "p", "c", "g")}

# Every pose of the pair and the stone men: (verse, who, what changes, the word it hangs on)
POSES = (
    ("2:7", "man", "arms lifted, head +12", "soul"),
    ("2:15", "man", "arms dig1, lean 14", "cultivate"),
    ("2:15", "man", "arms dig2, lean 14", "cultivate"),
    ("2:15", "man", "arms down, lean 0", "keep"),
    ("2:16", "man", "head +12", "commanded"),
    ("2:16", "man", "arms takeup, head +14", "You"),
    ("2:16", "man", "arms eat, head +0", "eat"),
    ("2:16", "man", "arms down", "every"),
    ("2:17", "man", "turns E", "evil"),
    ("2:17", "man", "arms take", "for"),
    ("2:17", "man", "arms down", "you"),
    ("2:19", "man", "arms point, head +4", "call"),
    ("2:20", "man", "turns W", "The"),
    ("2:20", "man", "turns E", "birds"),
    ("2:20", "man", "arms down, head +0", "but"),
    ("2:21", "man", "kneel2, arms down, head +0", "fall"),
    ("2:21", "man", "lying, stand", "fall"),
    ("2:21", "man", "breath 1.5", "As"),
    ("2:21", "man", "breath 0", "slept"),
    ("2:22", "wom", "turns W", "man"),
    ("2:23", "man", "side, kneel2, arms down, head +8", "said"),
    ("2:23", "man", "side, stand, arms down, head +8", "said"),
    ("2:23", "man", "side, stand, arms join, head +2", "This"),
    ("2:23", "wom", "stand, arms join", "This"),
    ("2:25", "man", "head +8", "not"),
    ("2:25", "wom", "head +8", "not"),
    ("3:1", "wom", "arms down, head +14, turns E", "He"),
    ("3:1", "man", "arms down, head +6", "He"),
    ("3:2", "wom", "arms openlow, head +14", "We"),
    ("3:2", "wom", "arms down, head +10", "garden"),
    ("3:3", "wom", "arms take, head +2", "has"),
    ("3:3", "wom", "arms down, head +0", "die"),
    ("3:4", "wom", "head +14", "woman"),
    ("3:5", "wom", "head +24", "opened"),
    ("3:6", "wom", "head +4", "good"),
    ("3:6", "wom", "head +8", "delight"),
    ("3:6", "wom", "arms take, head +12", "desired"),
    ("3:6", "wom", "arms eat, head +0", "ate"),
    ("3:6", "wom", "arms held, head +0", "ate"),
    ("3:6", "wom", "arms give, turns W", "she"),
    ("3:6", "man", "arms give, head +0", "gave"),
    ("3:6", "wom", "arms down", "husband"),
    ("3:6", "man", "arms eat", "he"),
    ("3:6", "man", "arms down", "too"),
    ("3:7", "man", "head +16", "opened"),
    ("3:7", "wom", "head +16", "opened"),
    ("3:7", "man", "arms down, head -16", "knew"),
    ("3:7", "wom", "arms down, head -16", "knew"),
    ("3:7", "man", "arms cover, head -20, turns W", "naked"),
    ("3:7", "wom", "arms cover, head -20, turns E", "naked"),
    ("3:7", "wom", "arms sew, head -22", "They"),
    ("3:7", "man", "arms sew, head -22", "They"),
    ("3:7", "man", "arms cover, head -12", "coverings"),
    ("3:7", "wom", "arms cover, head -12", "coverings"),
    ("3:7", "man", "leaves", "coverings"),
    ("3:7", "wom", "leaves", "coverings"),
    ("3:8", "man", "arms shrink, turns W", "heard"),
    ("3:8", "wom", "arms shrink, turns W", "heard"),
    ("3:8", "man", "head +12", "voice"),
    ("3:8", "wom", "head +12", "voice"),
    ("3:8", "man", "kneel2, arms shrink, head -6", "among"),
    ("3:8", "wom", "kneel2, arms shrink, head -6", "among"),
    ("3:10", "man", "stand, arms shrink, head +4", "said"),
    ("3:10", "man", "head -8, lean 8", "afraid"),
    ("3:10", "man", "arms cover, head -16, lean 4", "naked"),
    ("3:11", "man", "head -30, lean 18", "Who"),
    ("3:12", "wom", "stand, arms shrink, head -4", "said"),
    ("3:12", "man", "arms cover, head +2, lean 0, turns E", "woman"),
    ("3:12", "man", "arms pointlow, head +2", "woman"),
    ("3:12", "man", "arms down, head -16", "ate"),
    ("3:13", "wom", "arms point, head +4", "serpent"),
    ("3:13", "wom", "arms down, head -6", "ate"),
    ("3:16", "wom", "stand, arms wrap, head -10, lean 10", "pain"),
    ("3:16", "wom", "head -14, lean 16", "In"),
    ("3:16", "wom", "arms down, head +2, lean 0, turns E", "Your"),
    ("3:16", "wom", "stand, arms reach", "husband"),
    ("3:16", "man", "head +0, turns W", "husband"),
    ("3:16", "man", "stand, arms reach, head +0", "and"),
    ("3:17", "man", "arms down, head +0, lean 0", "Adam"),
    ("3:17", "wom", "arms down, head +0", "Adam"),
    ("3:17", "man", "head +6", "wife’s"),
    ("3:17", "man", "head -10, turns E", "ground"),
    ("3:17", "dig", "arms dig2, lean 14", "of"),
    ("3:17", "dig", "arms dig1, lean 14", "life"),
    ("3:18", "dig", "arms dig2, lean 14", "It"),
    ("3:18", "dig", "arms dig1, lean 14", "thorns"),
    ("3:18", "dig", "arms dig2, lean 14", "thorns"),
    ("3:18", "dig", "arms dig1, lean 14", "thorns"),
    ("3:18", "dig", "arms dig2, lean 14", "to"),
    ("3:18", "dig", "kneel2, arms reach, lean 0", "you"),
    ("3:18", "dig", "arms take", "herb"),
    ("3:18", "dig", "arms eat", "herb"),
    ("3:19", "dig", "stand, arms brow", "sweat"),
    ("3:19", "dig", "arms eat", "bread"),
    ("3:19", "dig", "kneel2, arms down, lean 10", "ground"),
    ("3:20", "man", "head +2, lean 0, turns W", "called"),
    ("3:20", "man", "arms point", "called"),
    ("3:20", "man", "arms down, head +0", "because"),
    ("3:21", "man", "skins, arms down, head +0", "Adam"),
    ("3:21", "wom", "skins, arms down, head +0", "them"),
    ("3:22", "lest", "arms takeup, head +16", "reach"),
)


# ---------------------------------------------------------------------------
# What is where, at a time
# ---------------------------------------------------------------------------

def state_then(card, ref, t):
    """Every actor's state t seconds into the verse. A move under way is carried in proportion, a
    show counts from its start, and anything else from its end."""
    st = card.state_at(ref)
    for kind, key, t0, d, val in sorted(card.events.get(ref, []), key=lambda e: e[2]):
        if kind == "show" and t0 <= t or t0 + d <= t:
            SC.apply_event(st[key], kind, val)
        elif kind == "move" and t0 <= t:
            u = (t - t0) / d
            st[key]["x"] += val[0] * u
            st[key]["y"] += val[1] * u
    return st


def ink_of(card, key, s):
    """(a shown figure's points in world px, how tall it stands), or ([], 0) for a thing."""
    a = card.actors[key]
    pose = {k: v for k, v in s["pose"].items() if k != "_morph"}
    parts = a.parts(pose)
    if not parts:
        return [], 0.0
    pts = SC.ink_points(parts, s["x"], s["y"], a.h / a.unit_h * s.get("scale", 1.0),
                        pose.get("_flip", s["flip"]))[0]
    return pts, a.h


def on_screen(cam, x, y):
    z, cx, cy = cam
    return (x - cx) * z + W / 2, (y - cy) * z + H / 2


def name_box(name, cam):
    """A name's ink on the screen."""
    sx, sy = on_screen(cam, name.x, name.y)
    sx, sy = sx + name.off[0], sy + name.off[1]
    a, b, c, d = C.ink(name.text, name.px, False, name.italic, "mm")
    return sx + a, sy + b, sx + c, sy + d


def gap(a, b):
    """The px between two boxes, 0 if they touch."""
    return math.hypot(max(a[0] - b[2], b[0] - a[2], 0), max(a[1] - b[3], b[1] - a[3], 0))


def _clear(box, pts):
    """Whether no point is within AIR of the box."""
    l, t, r, b = box[0] - AIR, box[1] - AIR, box[2] + AIR, box[3] + AIR
    return not any(l <= x <= r and t <= y <= b for x, y in pts)


# ---------------------------------------------------------------------------
# Name air, figures in frame, the floor, man's size
# ---------------------------------------------------------------------------

def name_air(story, ref):
    fl = story.drawn[ref]
    dur = story.verses[ref].dur
    title = C.title_rect(S.TITLE.format(S.cv(ref)[0]))
    names = fl.names

    def showing(n, t):
        return (n.t is None or t >= n.t) and (n.gone is None or t < sum(n.gone))

    def whole(n, t):
        return (n.t is None or t >= n.t + NAME_IN_S) and (n.gone is None or t <= n.gone[0])

    moments = {dur}
    for n in names:
        moments.add(0.0 if n.t is None else n.t + NAME_IN_S)
        if n.gone:
            moments.add(n.gone[0])
    found = set()
    for t in sorted(moments):
        cam = fl.at(t)
        st = state_then(story.card, ref, t)
        figures = []
        if not fl.covered(t):
            figures = [(key, [on_screen(cam, x, y) for x, y in ink_of(story.card, key, st[key])[0]])
                       for key in PEOPLE if st[key]["shown"]]
        for n in names:
            if not whole(n, t):
                continue
            box = name_box(n, cam)
            if box[2] <= 0 or box[0] >= W or box[3] <= 0 or box[1] >= H:
                continue                # wholly out of frame: the camera has left it
            if (box[0] < FRAME_MARGIN or box[1] < FRAME_MARGIN or box[2] > W - FRAME_MARGIN
                    or box[3] > H - FRAME_MARGIN):
                found.add(f"{ref}: {n.text} is cut by the frame at {t:.2f}")
            if gap(box, title) < AIR:
                found.add(f"{ref}: {n.text} is under the title at {t:.2f}")
            for o in names:
                if o is not n and showing(o, t) and gap(box, name_box(o, cam)) < AIR:
                    found.add(f"{ref}: {n.text} touches {o.text} at {t:.2f}")
            for key, pts in figures:
                if not _clear(box, pts):
                    found.add(f"{ref}: {n.text} touches {key} at {t:.2f}")
    return sorted(found)


def _serpent_rest(svg):
    """How far along the road the serpent's nose rests, in a verse that moves him: the one
    animateMotion in a file is his. None if he stays where he is."""
    m = re.search(r'<animateMotion\b[^>]*\bkeyPoints="([^"]*)"', svg)
    return float(m.group(1).split(";")[-1]) * S.SN.L if m else None


def figures_in_frame(story, ref, svg):
    fl = story.drawn[ref]
    dur = story.verses[ref].dur
    if fl.covered(dur):
        return []
    cam = fl.cam1
    st = state_then(story.card, ref, dur)
    out = []
    for key, s in st.items():
        pts, tall = ink_of(story.card, key, s) if s["shown"] else ([], 0.0)
        if not pts or key in AWAY.get(ref, ()):
            continue
        if cam[0] >= CLOSE_SHOT:
            pts = [p for p in pts if p[1] <= s["y"] - tall * HIPS]
        for x, y in pts:
            sx, sy = on_screen(cam, x, y)
            if not (0 <= sx <= W and 0 <= sy <= H):
                out.append(f"{ref}: {key} is not wholly in frame at rest")
                break
    rest = _serpent_rest(svg)
    if rest is not None:
        sx, sy = on_screen(cam, *S.SN.at(rest)[:2])
        if not (0 <= sx <= W and 0 <= sy <= H):
            out.append(f"{ref}: the serpent is out of frame at rest")
    return out


def the_floor(story, ref):
    """-> (problems, (smallest px, who, when) or None). A figure drawn by hand counts wherever along
    its way it might be, so a walk is measured for as long as any of it is in frame."""
    fl = story.drawn[ref]
    dur = story.verses[ref].dur
    least, found = None, set()
    for i in range(int(dur / .05) + 1):
        t = i * .05
        cam = fl.at(t)
        if cam[0] >= PLATE_Z:
            continue
        x0, y0, x1, y1 = C.visible_world(cam)
        st = state_then(story.card, ref, t)
        shown = [(key, st[key]["x"], st[key]["x"], st[key]["y"], 1.0)
                 for key in PEOPLE if st[key]["shown"]]
        shown += [(f.who, f.x0, f.x1, f.y, f.k) for f in fl.figures
                  if (f.t is None or t >= f.t) and (f.gone is None or t < f.gone)]
        for who, a, b, y, k in shown:
            if x0 - 20 < b and a < x1 + 20 and y0 < y and y - MAN_PX * k < y1:
                px = cam[0] * MAN_PX * k
                if least is None or px < least[0]:
                    least = (px, who, round(t, 2))
                if px < FLOOR_PX:
                    found.add(f"{ref}: {who} is {px:.0f} px at {t:.2f}, under the floor")
    return sorted(found), least


def man_at_rest(story, ref):
    """A person's height in px at the verse's rest, if anyone shown is in frame then."""
    fl = story.drawn[ref]
    dur = story.verses[ref].dur
    x0, y0, x1, y1 = C.visible_world(fl.cam1)
    st = state_then(story.card, ref, dur)
    seen = any(st[k]["shown"] and x0 < st[k]["x"] < x1 and y0 < st[k]["y"] - MAN_PX < y1
               for k in PEOPLE)
    return fl.cam1[0] * MAN_PX if seen and not fl.covered(dur) else None


# ---------------------------------------------------------------------------
# Reading the animations in a file
# ---------------------------------------------------------------------------

_ANIM = re.compile(r"<(?:animate|animateTransform|animateMotion|set)\b[^>]*?>")
# The one spline the river's slivers use, and nothing else: garden_art._sliver_anim
_WATER = 'keySplines=".35 0 .4 1"'
_CAMERA = re.compile(r'^<svg\b[^>]*><rect\b[^>]*/><g transform="translate\([^)]*\)">'
                     r'(<animateTransform\b[^>]*/>)?<g transform="scale\([^)]*\)">'
                     r'(<animateTransform\b[^>]*/>)?')


def _attr(a, name):
    m = re.search(r"\b" + name + r'="([^"]*)"', a)
    return m.group(1) if m else None


def _begin(a):
    m = re.search(r'begin="([\d.]+)s?"', a)
    return float(m.group(1)) if m else 0.0


def _dur(a):
    m = re.search(r'\bdur="([\d.]+)s?"', a)
    return float(m.group(1)) if m else 0.0


def _end(a):
    """When a finite animation ends."""
    m = re.search(r'repeatCount="([\d.]+)"', a)
    return _begin(a) + _dur(a) * (float(m.group(1)) if m else 1.0)


def _camera_anims(svg):
    """The camera's two animations, as they open the file; None for a camera that stays."""
    m = _CAMERA.match(svg)
    return (m.group(1), m.group(2)) if m else (None, None)


def _moving(a):
    """The stretches, as (from, to), in which an animation really changes something. A key list that
    starts by holding hasn't begun. A discrete swap only moves for as long as it repeats, a stride
    or a wing, and a <set> is an instant."""
    if a.startswith("<set"):
        return []
    b, d = _begin(a), _dur(a)
    vals = _attr(a, "values")
    keys = _attr(a, "keyTimes")
    if vals is None:
        if _attr(a, "from") is not None and _attr(a, "from") == _attr(a, "to"):
            return []
        points = _attr(a, "keyPoints")
        if points and keys:
            ps, ks = points.split(";"), [float(k) for k in keys.split(";")]
            return [(b + ks[i] * d, b + ks[i + 1] * d) for i in range(len(ks) - 1)
                    if float(ps[i]) != float(ps[i + 1])]
        return [(b, b + d)]
    vs = vals.split(";")
    ks = ([float(k) for k in keys.split(";")] if keys
          else [i / max(1, len(vs) - 1) for i in range(len(vs))])
    if 'calcMode="discrete"' in a:
        return [(b, _end(a))] if _attr(a, "repeatCount") else []
    return [(b + ks[i] * d, b + ks[i + 1] * d) for i in range(min(len(vs), len(ks)) - 1)
            if vs[i].strip() != vs[i + 1].strip()]


# What an animation can move, as opposed to its paint: only these turn back or set off again inside
# one key list as a new beat. A fade in, a hold and a fade out are one beat
_PAINT = ("opacity", "fill-opacity", "stroke-opacity", "fill", "stroke", "visibility")
_NUM = re.compile(r"-?\d*\.?\d+(?:e-?\d+)?")


def _keys(a, vs):
    """An animation's keyTimes, or the even ones its values `vs` imply."""
    keys = _attr(a, "keyTimes")
    return ([float(k) for k in keys.split(";")] if keys
            else [i / max(1, len(vs) - 1) for i in range(len(vs))])


def _onsets(a):
    """When an animation sets something going: its first moving stretch, and, for one that moves a
    thing, each later stretch that follows a hold or turns back the way it came. A key list that
    starts by holding hasn't begun. A <set> sets something at its begin, and a switch that doesn't
    repeat, at each of its changes."""
    b, d = _begin(a), _dur(a)
    if a.startswith("<set"):
        return [b]
    if 'calcMode="discrete"' in a and not _attr(a, "repeatCount"):
        vs = (_attr(a, "values") or "").split(";")
        ks = _keys(a, vs)
        return [b + ks[i] * d for i in range(1, min(len(vs), len(ks))) if vs[i] != vs[i - 1]]
    spans = _moving(a)
    name = _attr(a, "attributeName") or "motion"
    if not spans or name in _PAINT or 'calcMode="discrete"' in a:
        return [s[0] for s in spans[:1]]
    vals = _attr(a, "values")
    vs = (vals.split(";") if vals is not None else (_attr(a, "keyPoints") or "").split(";"))
    ks = _keys(a, vs)
    pts = [[float(n) for n in _NUM.findall(v)] for v in vs]
    out, last = [], None            # last: (when it stopped, which way it went)
    for i in range(min(len(pts), len(ks)) - 1):
        step = [q - p for p, q in zip(pts[i], pts[i + 1])]
        if len(pts[i]) != len(pts[i + 1]) or not any(abs(s) > 1e-9 for s in step):
            continue
        t0, t1 = b + ks[i] * d, b + ks[i + 1] * d
        if (last is None or t0 > last[0] + 1e-6
                or sum(p * q for p, q in zip(last[1], step)) < 0):
            out.append(t0)
        last = (t1, step)
    return out or [spans[0][0]]


def _union(spans):
    out = []
    for a, b in sorted(s for s in spans if s[1] > s[0]):
        if out and a <= out[-1][1] + .001:
            out[-1][1] = max(out[-1][1], b)
        else:
            out.append([a, b])
    return out


def _holes(spans, dur):
    """The stretches of a verse outside these, longest first, as (length, from, to)."""
    holes, p = [], 0.0
    for a, b in _union(spans):
        if a - p > .001:
            holes.append((round(a - p, 2), round(p, 2), round(a, 2)))
        p = max(p, b)
    if dur - p > .001:
        holes.append((round(dur - p, 2), round(p, 2), round(dur, 2)))
    return sorted(holes, reverse=True)


# ---------------------------------------------------------------------------
# Budget, still time, stills anywhere, camera speed, one loop
# ---------------------------------------------------------------------------

def budget(ref, svg):
    kb = len(svg.encode("utf-8")) / 1024
    anims = len(_ANIM.findall(svg))
    texts = len(re.findall(r"<text\b", svg))
    out = []
    if kb >= MAX_KB:
        out.append(f"{ref}: {kb:.0f} KB, over {MAX_KB}")
    if anims >= MAX_ANIMS:
        out.append(f"{ref}: {anims} animations, over {MAX_ANIMS}")
    if texts >= MAX_TEXTS:
        out.append(f"{ref}: {texts} <text>, over {MAX_TEXTS}")
    return out, kb, anims


def still_time(svg, dur):
    """-> (seconds after the last animation, the same not counting the water). A verse with a loop
    doesn't stop."""
    last = lastw = 0.0
    for a in _ANIM.findall(svg):
        if 'repeatCount="indefinite"' in a:
            return 0.0, 0.0
        vals = _attr(a, "values")
        if vals and len(set(vals.split(";"))) == 1:
            continue
        last = max(last, _end(a))
        if _WATER not in a:
            lastw = max(lastw, _end(a))
    return max(0.0, dur - last), max(0.0, dur - lastw)


def stills_anywhere(svg, dur):
    """-> (the holes in the verse with nothing moving, the holes with only the camera moving or
    nothing): the water, line weight and a plate's switching aside."""
    cam = _camera_anims(svg)
    story, camera = [], []
    for a in _ANIM.findall(svg):
        if a in cam:
            camera += _moving(a)
        elif 'repeatCount="indefinite"' in a:
            story.append((_begin(a), math.inf))
        elif not (_WATER in a or 'attributeName="stroke-width"' in a
                  or ('attributeName="visibility"' in a and "repeatCount" not in a)):
            story += _moving(a)
    return _holes(story + camera, dur), _holes(story, dur)


def camera_peak(fl):
    """-> (peak pan across the screen in px/s, when; peak zoom d ln z / dt, when), from a Flight's
    baked keys. A pan on its own bakes to two keys and an ease, so it is sampled. A cut is an edit,
    not a move: the keys either side of it are not a step."""
    if fl.static:
        return 0.0, 0.0, 0.0, 0.0
    cams = fl.cams
    if fl.pure_pan:
        cams = [fl.at(fl.dur * i / 60) for i in range(61)]
    dt = fl.dur / (len(cams) - 1)
    cuts = set(getattr(fl, "cut_keys", ()))
    pan = zoom = (0.0, 0.0)
    for i, ((z0, x0, y0), (z1, x1, y1)) in enumerate(zip(cams, cams[1:])):
        if i in cuts:
            continue
        pan = max(pan, (math.hypot(x1 - x0, y1 - y0) * math.sqrt(z0 * z1) / dt, i * dt))
        zoom = max(zoom, (abs(math.log(z1 / z0)) / dt, i * dt))
    return (*pan, *zoom)


def camera_speed(ref, fl):
    pan, t_pan, zoom, t_zoom = camera_peak(fl)
    out = []
    if pan > PAN_MAX:
        out.append(f"{ref}: the camera pans at {pan:.0f} px/s at {t_pan:.2f}, over {PAN_MAX:.0f}")
    if zoom > ZOOM_MAX:
        out.append(f"{ref}: the camera zooms at {zoom:.2f}/s at {t_zoom:.2f}, over {ZOOM_MAX}")
    return out


def camera_legs(ref, keys, dur, cuts=()):
    """`keys` is the verse's camera, [(from, to, cam)], and `cuts` the times of those that are
    cuts, which take no time."""
    out, last = [], 0.0
    for t0, t1, _cam in sorted(keys, key=lambda k: k[:2]):
        if t1 < t0 or (t1 == t0 and t0 not in cuts):
            out.append(f"{ref}: a camera leg runs backward, {t0:.2f} to {t1:.2f}")
        if t0 < last - 1e-6:
            out.append(f"{ref}: a camera leg begins at {t0:.2f}, before the last ends, {last:.2f}")
        if t1 > dur + .011:
            out.append(f"{ref}: a camera leg ends at {t1:.2f}, after the narration's {dur:.2f}")
        last = max(last, t1)
    return out


def one_loop(ref, svg, dur):
    """Rule 5. The narration's length is rounded to .01, and so are the times."""
    out = []
    loops = svg.count('repeatCount="indefinite"')
    if ref == "3:24" and not loops:
        out.append(f"{ref}: the wheel doesn't turn")
    elif ref != "3:24" and loops:
        out.append(f"{ref}: loops forever")
    last = max((_end(a) for a in _ANIM.findall(svg) if 'repeatCount="indefinite"' not in a),
               default=0.0)
    if last > dur + .011:
        out.append(f"{ref}: an animation runs to {last:.2f}, after the narration's {dur:.2f}")
    return out


# ---------------------------------------------------------------------------
# Nothing on his name
# ---------------------------------------------------------------------------

def name_words(ref):
    """Where the verse says "Yahweh", "Yahweh God" or "God": [(its offset, the next word's offset,
    or None if it ends the verse)]."""
    words = [(m.group(0), m.start()) for m in S._WORD.finditer(S.verse_text(ref))]
    out, i = [], 0
    while i < len(words):
        w = words[i][0]
        if w == "Yahweh" or w.startswith("God"):
            j = i + 1
            if w == "Yahweh" and j < len(words) and words[j][0].startswith("God"):
                j += 1
            out.append((words[i][1], words[j][1] if j < len(words) else None))
            i = j
        else:
            i += 1
    return out


def name_windows(ref):
    """[(from, to)]: his name said, in seconds, from the clock."""
    clock = S._clock(ref)
    dur = S.verse_dur(ref)
    return [(round(clock(a), 2), dur if b is None else round(clock(b), 2))
            for a, b in name_words(ref)]


def _baked(a, fl):
    """Whether an animation is baked on the camera's keys and moves only as the camera does, as the
    Flight bakes the camera itself, a person's line weight or a name's size: it begins with the
    verse, lasts as long as the flight, and has a key only where the camera has one. A switch is
    not: what it shows or takes away is new, a plate's among them, and the cut that goes with a
    plate is a leg of the camera's, which answers for its own time."""
    if (fl.static or 'calcMode="discrete"' in a or _begin(a) != 0
            or f'dur="{fl.dur:.2f}s"' not in a):
        return False
    n = len(fl.cams) - 1
    if _attr(a, "keyTimes") is None:
        return len((_attr(a, "values") or "").split(";")) == n + 1
    return all(abs(k * n - round(k * n)) < .3 for k in _keys(a, []))


_GROWS = re.compile(r'<use href="#([^"]+)"[^>]*>(<animateTransform\b[^>]*>)')


def _under_way(story, ref, svg):
    """What may carry on through his name, as it is written: the wave of UNDER_WAY's drawings rising,
    and each walk carried over the seam from the verse before, a steady move that begins with this
    verse where one ended with the last."""
    ids = UNDER_WAY.get(ref, ())
    out = {m.group(2) for m in _GROWS.finditer(svg) if m.group(1) in ids}
    refs = story.card.refs
    if ref in refs[1:]:
        prev = refs[refs.index(ref) - 1]
        end = story.verses[prev].dur - .02
        going = {key for kind, key, t, d, val in story.card.events.get(prev, [])
                 if kind == "move" and val[2:] and t + d >= end}
        out |= {S.Stage.move_anim(t, d, val)
                for kind, key, t, d, val in story.card.events.get(ref, [])
                if kind == "move" and val[2:] and key in going and t <= .02}
    return out


def his_name(story, ref, svg, windows):
    """`windows`: when his name is said in the verse, [(from, to)]."""
    if not windows:
        return []
    fl, legs = story.drawn[ref], story.verses[ref].keys
    carried = _under_way(story, ref, svg)
    begins = Counter()
    for a in _ANIM.findall(svg):
        if _WATER in a or a in carried or _baked(a, fl):
            continue
        for t in _onsets(a):
            if any(w0 - NAME_LEAD <= t < w1 - .011 for w0, w1 in windows):
                begins[f"{_attr(a, 'attributeName') or 'motion'} at {t:.2f}"] += 1
    out = []
    if begins:
        first = ", ".join(f"{k} x{n}" for k, n in sorted(begins.items())[:4])
        out.append(f"{ref}: begins on his name: {first}")
    for t0, _t1, _c in legs:
        if any(w0 - NAME_LEAD <= t0 < w1 for w0, w1 in windows):
            out.append(f"{ref}: a camera leg begins on his name, at {t0:.2f}")
    return out


# ---------------------------------------------------------------------------
# The pose list
# ---------------------------------------------------------------------------

def pose_change(val):
    """A pose's value, as POSES says it."""
    says = []
    for k, fmt in (("view", "{}"), ("covering", "{}"), ("legs", "{}"), ("arms", "arms {}"),
                   ("up", "head {:+g}"), ("lean", "lean {:g}"), ("breath", "breath {:g}")):
        if k in val:
            says.append(fmt.format(val[k]))
    if "_flip" in val:
        says.append("turns E" if val["_flip"] > 0 else "turns W")
    return ", ".join(says)


def pose_events(card):
    """Every pose of the pair and the stone men, in the order they are told: (verse, who, what
    changes, when). A stride's own start and stop are left out."""
    walking, out = {}, []
    for ref in card.refs:
        for kind, key, t, _d, val in sorted(card.events.get(ref, []), key=lambda e: e[2]):
            if kind != "pose" or key not in PEOPLE:
                continue
            if val.get("legs") == "walk":
                walking[key] = True
            elif val.get("legs") == "stand" and walking.get(key):
                walking[key] = False
            elif pose_change(val):
                out.append((ref, key, pose_change(val), t))
    return out


def poses_on_the_list(card, word_times=None):
    """`word_times(ref, word)` is when the verse says a word, for a build on the clock: then a pose
    must also be near its word."""
    told = pose_events(card)
    listed = Counter(p[:3] for p in POSES)
    there = Counter(p[:3] for p in told)
    out = [f"{r}: {k}'s pose is not on the list: {c}" for r, k, c in there - listed]
    out += [f"{r}: {k}'s pose is on the list and isn't told: {c}" for r, k, c in listed - there]
    if word_times:
        words = {}
        for r, k, c, w in POSES:
            words.setdefault((r, k, c), []).append(w)
        for r, k, c, t in told:
            ws = words.get((r, k, c), [])
            if ws and not any(abs(t - said) <= POSE_WORD_S for w in ws
                              for said in word_times(r, w)):
                out.append(f"{r}: {k}'s {c}, at {t:.2f}, is not near {' or '.join(ws)}")
    return out


# ---------------------------------------------------------------------------
# The file itself
# ---------------------------------------------------------------------------

_HEAD = '<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="576"'
_BANNED = ("<filter", "<mask", "<script", "<style", "<image", "<tspan", "xlink")


def file_rules(ref, svg, fl=None):
    out = []
    try:
        minidom.parseString(svg.encode("utf-8"))
    except Exception as e:      # the parser's own kinds of error, whichever it raises
        out.append(f"{ref}: does not parse: {e}")
    if not svg.startswith(_HEAD):
        out.append(f"{ref}: the wrong head on the file")
    for word in _BANNED:
        if word in svg:
            out.append(f"{ref}: has {word}")
    ids = re.findall(r'\bid="([^"]+)"', svg)
    for dup in sorted(k for k, n in Counter(ids).items() if n > 1)[:6]:
        out.append(f"{ref}: the id {dup} is used twice")
    known = set(ids)
    for href in sorted(set(re.findall(r'href="([^"]*)"', svg))):
        if not href.startswith("#"):
            out.append(f"{ref}: refers outside the file: {href[:60]}")
        elif href[1:] not in known:
            out.append(f"{ref}: nothing has the id of href {href}")
    for url in sorted(set(re.findall(r"url\(([^)]*)\)", svg))):
        if not url.startswith("#"):
            out.append(f"{ref}: refers outside the file: {url[:60]}")
        elif url[1:] not in known:
            out.append(f"{ref}: nothing has the id of url({url})")
    if svg.replace(_HEAD, "", 1).count("http") or "@font-face" in svg:
        out.append(f"{ref}: refers outside the file")
    texts = len(re.findall(r"<text\b", svg))
    if fl is not None and texts != len(fl.names) + 1:
        out.append(f"{ref}: {texts} <text>, and {len(fl.names)} names and the title")
    return out


def key_times(ref, svg):
    out = []
    for a in _ANIM.findall(svg):
        if re.search(r'\b(?:begin|dur)="-', a):
            out.append(f"{ref}: a negative time: {a[:80]}")
        keys = _attr(a, "keyTimes")
        if not keys:
            continue
        ks = [float(k) for k in keys.split(";")]
        discrete = 'calcMode="discrete"' in a
        if (any(q < p for p, q in zip(ks, ks[1:])) or ks[0] != 0
                or (not discrete and abs(ks[-1] - 1) > 1e-6)):
            out.append(f"{ref}: keyTimes {keys[:60]}")
        for name in ("values", "keyPoints"):
            vals = _attr(a, name)
            if vals is not None and len(vals.split(";")) != len(ks):
                out.append(f"{ref}: {name} and keyTimes differ in length: {keys[:40]}")
        splines = _attr(a, "keySplines")
        if splines is not None and len(splines.split(";")) != len(ks) - 1:
            out.append(f"{ref}: keySplines isn't one fewer than keyTimes: {keys[:40]}")
    return out


# ---------------------------------------------------------------------------
# All of it
# ---------------------------------------------------------------------------

Measured = namedtuple("Measured", "dur still still_story holds world pan zoom least man kb anims")


def word_times(ref, word):
    """When the verse says a word, from the clock."""
    clock = S._clock(ref)
    return [clock(at) for at in S.occurrences(ref, word)]


def check_verse(story, ref, svg, windows):
    """-> (problems, Measured): every check of one verse, as drawn on story.drawn[ref]."""
    v, fl = story.verses[ref], story.drawn[ref]
    dur = v.dur
    over, kb, anims = budget(ref, svg)
    after, after_story = still_time(svg, dur)
    nothing, world = stills_anywhere(svg, dur)
    pan, _t_pan, zoom, _t_zoom = camera_peak(fl)
    floor_bad, least = the_floor(story, ref)
    problems = over
    if after_story > STILL_VERSE_S and ref not in NAMED_STILL:
        problems.append(f"{ref}: {after_story:.2f} s still after its last motion, over "
                        f"{STILL_VERSE_S}")
    if nothing and nothing[0][0] >= STILL_ANYWHERE_S and ref not in NAMED_STILL:
        problems.append(f"{ref}: nothing moves from {nothing[0][1]:.2f} to {nothing[0][2]:.2f}, "
                        f"{STILL_ANYWHERE_S} s or more")
    problems += (name_air(story, ref) + figures_in_frame(story, ref, svg) + floor_bad
                 + camera_speed(ref, fl) + camera_legs(ref, v.keys, dur, v.cuts)
                 + one_loop(ref, svg, dur)
                 + his_name(story, ref, svg, windows) + file_rules(ref, svg, fl)
                 + key_times(ref, svg))
    return problems, Measured(dur, after, after_story, nothing, world, pan, zoom, least,
                              man_at_rest(story, ref), kb, anims)


def report_lines(measured):
    """The table to read, from {ref: Measured}."""
    rows = [f"{ref:5s} {m.dur:6.2f} s  still {m.still:5.2f}, {m.still_story:5.2f} not counting "
            f"water  longest hold {m.holds[0][0] if m.holds else 0:5.2f}  camera {m.pan:5.0f} px/s "
            f"{m.zoom:4.2f}/s  man {m.man or 0:4.0f} px  {m.kb:6.1f} KB {m.anims:4d} animations"
            for ref, m in measured.items()]
    total = sum(m.dur for m in measured.values())
    still_all = sum(m.still for m in measured.values())
    still_story = sum(m.still_story for m in measured.values())
    held = sum(h[0] for m in measured.values() for h in m.holds)
    camera_only = sum(h[0] for m in measured.values() for h in m.world)
    rows += [f"Still time: {still_all:.2f} s of {total:.2f} s ({still_all / total:.1%}), "
             f"{still_story:.2f} s ({still_story / total:.1%}) not counting the water",
             f"Stills anywhere: nothing moving {held:.1f} s ({held / total:.0%}), only the camera "
             f"or nothing {camera_only:.1f} s ({camera_only / total:.0%})"]
    holds = [(m.holds[0], ref) for ref, m in measured.items()
             if m.holds and ref not in NAMED_STILL]
    if holds:
        (length, a, b), ref = max(holds)
        rows.append(f"Longest hold but the named: {length:.2f} s ({ref}, {a:.2f}-{b:.2f})")
    sizes = [m.man for m in measured.values() if m.man]
    if sizes:
        rows.append(f"Man's size at rest: median {statistics.median(sizes):.0f} px, "
                    f"from {min(sizes):.0f} to {max(sizes):.0f}")
    least = [(*m.least, ref) for ref, m in measured.items() if m.least]
    if least:
        px, who, t, ref = min(least)
        rows.append(f"The floor: smallest {px:.0f} px ({who}, {ref} at {t:.2f})")
    kb, big = max((m.kb, ref) for ref, m in measured.items())
    anims, many = max((m.anims, ref) for ref, m in measured.items())
    pan, fast = max((m.pan, ref) for ref, m in measured.items())
    zoom, deep = max((m.zoom, ref) for ref, m in measured.items())
    rows += [f"Largest file {big} {kb:.1f} KB; most animations {many} {anims}",
             f"Fastest camera: {pan:.0f} px/s ({fast}), {zoom:.2f}/s ({deep})"]
    return rows


def run(story, files, windows=name_windows, word_times=word_times):
    """-> (problems, report): every check over `files`, {ref: svg}, as just drawn from `story`, and
    a table to read. `windows(ref)` says when his name is said and `word_times(ref, word)` when a
    word is. Both go by the clock, and `word_times` may be None, which leaves that check out."""
    problems, measured = [], {}
    for ref, svg in files.items():
        found, measured[ref] = check_verse(story, ref, svg, windows(ref))
        problems += found
    total = sum(m.dur for m in measured.values())
    still_story = sum(m.still_story for m in measured.values())
    if still_story >= total * STILL_SHARE:
        problems.append(f"the chapters: {still_story:.2f} s of {total:.2f} still after the last "
                        f"motion, {STILL_SHARE:.0%} or more")
    return problems + poses_on_the_list(story.card, word_times), report_lines(measured)
