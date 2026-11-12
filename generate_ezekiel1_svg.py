"""Ezekiel 1: the vision by the river Chebar, one drawing that assembles.

One still frame for the whole chapter (no camera). Each verse brings in the
part it names, on its word, and the part then holds: the storm cloud out of
the north (1:4), the four living creatures (1:5) with their faces and wings
(1:6), hooves (1:7) and hands (1:8), the fire among them (1:13), a wheel
beside each (1:15), the wheel within it (1:16) and the eyes in the rims
(1:18), the expanse over their heads (1:22), the throne (1:26), the fire on
it (1:27) and the brightness like the rainbow (1:28). A name or number
stands only on the verse that says it.

What is drawn, and from where:

* The beings are the owner's merged cast (2026-11-11): the creatures'
  wings are feathered and, with the folded wings and the hands, full of
  eyes; the wheels are gold and winged. Ezekiel 1 itself puts eyes only on
  the wheels and gives the wheels no wings.
* The creatures and wheels are svg_figures' `living_creature_layers` and
  `wheel_in_wheel_layers`. The four stand in a square seen from the front:
  two near, two smaller behind, their raised wings touching (1:9, 1:11).
  A creature shows the three faces one sees from in front, plainly; at
  1:10 a card comes up over them (`faces_card`): one head turning as a
  solid block, each face coming to the front as it is said, narrowed and
  shaded by where its side stands, and the head from above with each face
  named on its side.
* The throne is svg_figures.prepared_throne's own throne, in sapphire. God
  is never drawn (docs/visuals.md, "God's presence"): the likeness on the
  throne (1:26-27) is a flame, glowing metal above and fire below, with no
  figure in it (the owner's pick, 2026-11-09).
* 1:13 says two things, and both are drawn: the creatures' own appearance
  is like burning coals, so from that verse they are redrawn hot (HOT)
  in a glow of their own; and a fire goes up and down among them
  (`fire_svg`), rising and sinking between them once before it comes to
  rest at their middle. It stands on nothing: it is not a fire on the
  ground.
* Lightning (1:4, 1:13, 1:14) draws itself once and goes; nothing flashes.
  The one loop is the fire's slow sway, like the bush's in Acts 7.
* The creatures and wheels rise at 1:19 and stand again at 1:21; the wings
  are let down at 1:24 and stay down.

Timing: a reveal begins just before its word (narration_clock, from the
verse's MP3). Where a verse has no MP3 yet the word's time is estimated from
its place in the text (RATE); re-run this after the audio is rendered.

Run:  .venv\\Scripts\\python.exe generate_ezekiel1_svg.py
"""

import json
import math
import os

import config
import narration_clock
import svg_figures as F
from passages import verse_numbers
from svg_surface import SvgCanvas, FONT_FAMILY
from generate_tabernacle import (BG, PANEL, SAND, SAND_DIM, TEXT, TEXT_DIM, HL,
                                 W, H, out_path)

BOOK, CHAPTER = "Ezekiel", 1

CREATURE = (226, 188, 122)      # burnished, like the feet (1:7)
FAR = (150, 128, 92)            # the two behind
HOT = (255, 208, 124)           # the same, like burning coals (1:13)
HOT_FAR = (212, 154, 92)
FIRE_Y = 424                    # where the fire among them comes to rest
BERYL = (118, 204, 172)         # sea-green, one reading of the wheels' stone
BERYL_FAR = (84, 140, 122)
WHEEL = (236, 196, 92)          # the wheels (1:16): tarshish as a golden stone
WHEEL_FAR = (164, 138, 72)
CRYSTAL = (196, 228, 242)       # the expanse (1:22)
SAPPHIRE = (92, 132, 236)       # the throne (1:26)
FIRE = (255, 176, 84)
CLOUD = (70, 72, 92)
WATER = (96, 132, 168)
RAINBOW = ((204, 84, 74), (224, 146, 66), (232, 204, 96), (112, 184, 116),
           (84, 136, 214), (136, 106, 196))

CX = W // 2
G_FRONT, G_BACK = 500, 452      # where the near and the far pair stand
S_FRONT, S_BACK = 1.5, 1.12     # px a unit
X_FRONT, X_BACK = 212, 70       # each pair's distance from the middle
WX_FRONT, WX_BACK = 352, 152    # their wheels'
EXP_Y = 300                     # the expanse
S_T = 1.18                      # the throne
BASE = EXP_Y - 2
THRONE_Y = BASE + 26 * S_T
SEAT = THRONE_Y - 60 * S_T
GLORY = (CX, BASE - 78)
STRIP = 568                     # the ground Ezekiel stands on
EZ_X = 952
LIFT = -26                      # how far they rise (1:19)
TOP1, TOP2 = 236, 258           # two lines for a verse's words, over the four

RATE = 14.0                     # letters a second, where a verse has no MP3
LEAD = 0.1


def rgb(c):
    return f"rgb({c[0]},{c[1]},{c[2]})"


def _text():
    path = os.path.join(config.BIBLES_DIR, "WEB", f"{BOOK}_{CHAPTER}.json")
    with open(path, encoding="utf-8") as f:
        return {v: t for v, t in json.load(f)["verses"]}


def _letters(s):
    return sum(ch.isalnum() for ch in s)


class Say:
    """When the verse's narration reaches a phrase."""

    def __init__(self, v, text):
        self.v, self.text = v, text
        mp3 = os.path.join(config.WEB_AUDIO_DIR, f"{BOOK}_{CHAPTER}_{v}.mp3")
        self.clock = narration_clock.clock(text, mp3)

    def _t(self, i):
        if self.clock:
            return self.clock(i)
        return 0.3 + _letters(self.text[:i]) / RATE

    def at(self, phrase, nth=0):
        i = -1
        for _ in range(nth + 1):
            i = self.text.find(phrase, i + 1)
            if i < 0:
                raise ValueError(f"{BOOK} {CHAPTER}:{self.v} doesn't say "
                                 f"{phrase!r}")
        return round(max(0.0, self._t(i) - LEAD), 2)

    def end(self):
        return self._t(len(self.text))


# ---------------------------------------------------------------------------
# Pieces
# ---------------------------------------------------------------------------

def fade(t, d=0.8, out=False):
    a, b = ("1", "0") if out else ("0", "1")
    return (f'<animate attributeName="opacity" values="{a};{b}" '
            f'begin="{t:.2f}s" dur="{d:.2f}s" fill="freeze"/>')


def fig(parts, s, ink, x=0, gy=0, page=BG):
    """A figure's SVG, its origin at (x, gy). The wings a step lighter
    than the vocabulary's, so two folded over a body don't close into one
    dark mass."""
    c = SvgCanvas(10, 10)
    sheet = dict(F.palette(ink, page))
    sheet["wing"] = (F._mix(page, ink, 0.36), ink, 1.3)
    sheet["robe"] = (F._mix(page, ink, 0.2), ink, 1.3)
    # an eye's white, and its lids: the lightest and darkest things on a rim
    sheet["sclera"] = ((240, 250, 246), F._mix(page, ink, 0.12), 1.0)
    F.draw(c, parts, x, gy, s, ink, page, style=sheet)
    return "".join(c._els)


def use(sid, x, y):
    return f'<use href="#{sid}" x="{x}" y="{y}"/>'


def label(x, y, text, size=16, fill=TEXT, anchor="middle", italic=False):
    it = ' font-style="italic"' if italic else ""
    return (f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" '
            f'dominant-baseline="central" fill="{rgb(fill)}" '
            f'stroke="{rgb(BG)}" stroke-width="3.5" stroke-opacity="0.85" '
            f'paint-order="stroke"{it}>{text}</text>')


def leader(p0, p1):
    return (f'<line x1="{p0[0]:.1f}" y1="{p0[1]:.1f}" x2="{p1[0]:.1f}" '
            f'y2="{p1[1]:.1f}" stroke="{rgb(TEXT_DIM)}" stroke-width="1"/>')


def ring(cx, cy, rx, ry, t, d=1.8):
    """One gold pulse round a part, on its word."""
    return (f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" '
            f'fill="none" stroke="{rgb(HL)}" stroke-width="2.5" opacity="0">'
            f'<animate attributeName="opacity" values="0;1;1;0" '
            f'keyTimes="0;0.25;0.7;1" begin="{t:.2f}s" dur="{d:.2f}s" '
            f'fill="freeze"/></ellipse>')


def bolt(pts, t):
    """Lightning: it draws itself once and goes."""
    L = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))
    p = " ".join(f"{x},{y}" for x, y in pts)
    return (f'<polyline points="{p}" fill="none" stroke="{rgb(HL)}" '
            f'stroke-width="2.2" stroke-linejoin="round" '
            f'stroke-dasharray="{L:.0f}" stroke-dashoffset="{L:.0f}">'
            f'<animate attributeName="stroke-dashoffset" values="{L:.0f};0" '
            f'begin="{t:.2f}s" dur="0.45s" fill="freeze"/>'
            f'<animate attributeName="opacity" values="1;0" '
            f'begin="{t + 1.0:.2f}s" dur="0.6s" fill="freeze"/></polyline>')


def arcs(cx, cy, deg, t, n=2, r=26, grow=3.2, ink=HL):
    """A sound going out from (cx, cy) toward `deg`: arcs that widen and
    fade once."""
    out = []
    a0, a1 = math.radians(deg - 32), math.radians(deg + 32)
    p0 = (r * math.cos(a0), r * math.sin(a0))
    p1 = (r * math.cos(a1), r * math.sin(a1))
    for k in range(n):
        b = t + k * 0.35
        out.append(
            f'<g opacity="0"><animate attributeName="opacity" values="0;0.9;0" '
            f'begin="{b:.2f}s" dur="1.5s" fill="freeze"/>'
            f'<path d="M{p0[0]:.1f} {p0[1]:.1f} A{r} {r} 0 0 1 {p1[0]:.1f} '
            f'{p1[1]:.1f}" fill="none" stroke="{rgb(ink)}" stroke-width="2.2" '
            f'stroke-linecap="round" vector-effect="non-scaling-stroke">'
            f'<animateTransform attributeName="transform" type="scale" '
            f'values="1;{grow}" begin="{b:.2f}s" dur="1.5s" fill="freeze"/>'
            f'</path></g>')
    return f'<g transform="translate({cx} {cy})">' + "".join(out) + "</g>"


def arrow(p0, p1):
    ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    h = [(p1[0] - 8 * math.cos(ang + s * 0.45), p1[1] - 8 * math.sin(ang + s * 0.45))
         for s in (-1, 1)]
    return (f'<path d="M{p0[0]:.1f} {p0[1]:.1f} L{p1[0]:.1f} {p1[1]:.1f} '
            f'M{h[0][0]:.1f} {h[0][1]:.1f} L{p1[0]:.1f} {p1[1]:.1f} '
            f'L{h[1][0]:.1f} {h[1][1]:.1f}" fill="none" stroke="{rgb(HL)}" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')


def _tongue(cx, w, h, lean):
    """One tongue of flame, its foot at (cx, 0), rising h and leaning."""
    tx = cx + lean
    return (f'M{cx - w / 2:.1f} 0 C{cx - w * 0.72:.1f} {-h * 0.42:.1f} '
            f'{tx - w * 0.12:.1f} {-h * 0.66:.1f} {tx:.1f} {-h:.1f} '
            f'C{tx + w * 0.16:.1f} {-h * 0.62:.1f} {cx + w * 0.78:.1f} '
            f'{-h * 0.4:.1f} {cx + w / 2:.1f} 0 Q{cx:.1f} {w * 0.34:.1f} '
            f'{cx - w / 2:.1f} 0 Z')


def fire_svg():
    """The fire that goes up and down among the creatures (1:13), about
    its own foot: three flat layers, deep orange outside to pale at the
    heart, the outer and inner swaying out of step, slowly, in a soft
    light of its own."""
    layers = (("rgb(232,104,48)", ((-17, 26, 58, -6), (0, 34, 92, 5),
                                   (18, 26, 66, 9)), 3.4,
               "1 1;1.05 1.07;0.96 0.95;1 1"),
              ("rgb(255,170,70)", ((-11, 18, 38, -3), (1, 24, 64, 3),
                                   (13, 17, 42, 5)), 2.7,
               "1 1;0.95 1.08;1.05 0.96;1 1"),
              ("rgb(255,238,176)", ((-3, 11, 22, -1), (5, 12, 34, 2)), 2.2,
               "1 1;1.06 1.1;0.96 0.94;1 1"))
    out = ['<circle cx="0" cy="-34" r="78" fill="url(#ember)"/>']
    for fill, tongues, dur, vals in layers:
        d = " ".join(_tongue(*t) for t in tongues)
        out.append(f'<g><animateTransform attributeName="transform" '
                   f'type="scale" values="{vals}" dur="{dur}s" '
                   f'repeatCount="indefinite"/><path d="{d}" fill="{fill}"/></g>')
    return "".join(out)


def throne_parts():
    """The prepared throne's own throne, without its cloud and sunburst."""
    out = []
    for kind, data, mat in F.prepared_throne(cushion=False):
        if mat in ("cloud", "fire"):
            continue
        if kind == "line" and max(p[1] for p in data) < 40:
            continue                                  # the cloud's seams
        out.append((kind, data, mat))
    return out


def flame_path():
    top = SEAT - 104
    return (f'M{CX} {top:.1f} C{CX + 34} {top + 30:.1f} {CX + 30} '
            f'{SEAT - 22:.1f} {CX + 20} {SEAT:.1f} L{CX - 20} {SEAT:.1f} '
            f'C{CX - 30} {SEAT - 22:.1f} {CX - 34} {top + 30:.1f} {CX} '
            f'{top:.1f} Z')


DEFS = (
    '<radialGradient id="storm"><stop offset="0" stop-color="rgb(255,214,140)" '
    'stop-opacity="0.5"/><stop offset="0.5" stop-color="rgb(255,170,80)" '
    'stop-opacity="0.16"/><stop offset="1" stop-color="rgb(255,170,80)" '
    'stop-opacity="0"/></radialGradient>'
    '<radialGradient id="glory"><stop offset="0" stop-color="rgb(255,244,190)" '
    'stop-opacity="0.75"/><stop offset="0.55" stop-color="rgb(255,226,150)" '
    'stop-opacity="0.2"/><stop offset="1" stop-color="rgb(255,226,150)" '
    'stop-opacity="0"/></radialGradient>'
    '<radialGradient id="core"><stop offset="0" stop-color="rgb(255,246,204)"/>'
    '<stop offset="0.5" stop-color="rgb(255,206,110)"/>'
    '<stop offset="1" stop-color="rgb(255,170,80)" stop-opacity="0"/>'
    '</radialGradient>'
    '<radialGradient id="ember"><stop offset="0" stop-color="rgb(255,150,60)" '
    'stop-opacity="0.5"/><stop offset="0.6" stop-color="rgb(255,120,50)" '
    'stop-opacity="0.16"/><stop offset="1" stop-color="rgb(255,120,50)" '
    'stop-opacity="0"/></radialGradient>'
    '<linearGradient id="him" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="rgb(255,250,214)"/>'
    '<stop offset="0.45" stop-color="rgb(255,222,128)"/>'
    '<stop offset="0.6" stop-color="rgb(255,170,70)"/>'
    '<stop offset="1" stop-color="rgb(226,92,48)"/></linearGradient>'
    '<linearGradient id="ice" x1="0" y1="0" x2="1" y2="0">'
    '<stop offset="0" stop-color="rgb(196,228,242)" stop-opacity="0.2"/>'
    '<stop offset="0.5" stop-color="rgb(226,244,252)" stop-opacity="0.5"/>'
    '<stop offset="1" stop-color="rgb(196,228,242)" stop-opacity="0.2"/>'
    '</linearGradient>')


CARD = (300, 22, 424, 242)      # the faces card of 1:10: x, y, w, h
FACE_SAID = (("man", "face of a man"), ("lion", "face of a lion"),
             ("ox", "face of an ox"), ("eagle", "face of an eagle"))


# The head of 1:10 as a turning block: each face's bearing round it when the
# man's is in front (degrees, clockwise from above), and the turns that
# bring each to the front as it is said, by the short way that passes no
# face not yet named: (face, the head's angle then, seconds the turn takes).
FACE_BEARING = {"man": 0, "lion": -90, "ox": 90, "eagle": 180}
FACE_TURNS = (("lion", 90, 0.9), ("ox", -90, 1.5), ("eagle", -180, 0.9))
HEAD_R = 11.5                   # the head's half width, in figure units
FACE_S = 4.4                    # px a unit on the card


def _clip_shapes(parts, s):
    """A figure's masses as bare shapes, for a clip."""
    out = []
    for kind, data, _m in parts:
        if kind == "fill":
            out.append('<polygon points="' + " ".join(
                f"{x:.1f},{y:.1f}" for x, y in F.place(data, 0, 0, s)) + '"/>')
        elif kind == "dot":
            out.append(f'<circle cx="{data[0] * s:.1f}" cy="{-data[1] * s:.1f}" '
                       f'r="{data[2] * s:.1f}"/>')
    return "".join(out)


def _head_keys(times):
    """The head's angle through the verse: [(t, degrees)], held between the
    turns and eased within each, a key every 1/25 s of a turn."""
    keys, phi = [(0.0, 0.0)], 0.0
    for (_face, to, dur), t1 in zip(FACE_TURNS, times[1:]):
        t0 = t1 - dur * 0.75             # most of the way round on its word
        keys.append((t0, phi))
        n = max(2, int(dur * 25))
        for i in range(1, n + 1):
            u = i / n
            e = u * u * (3 - 2 * u)
            keys.append((t0 + dur * u, phi + (to - phi) * e))
        phi = to
    return keys


def faces_card(cue):
    """1:10 close up: one creature's head turning as a solid thing, each
    face coming round to the front as it is said, and beside it the head
    seen from above with each face named on the side it looks out from: the
    man's in front, the lion's at its right hand, the ox's at its left, the
    eagle's behind.

    The turn is drawn, not faked by a fade: the four faces are the four
    sides of one block, each placed and narrowed by where its side stands
    (x = R sin a, width cos a), a little smaller as it goes back, and
    shaded in two flat steps as it turns from the light. Each face carries
    a flat shadow down its off side, and a dark core fills the gap behind. -> (svg, when its last motion ends)."""
    x0, y0, w, h = CARD
    t0 = cue("likeness of their faces")
    times = []
    for _kind, phrase in FACE_SAID:
        t = cue(phrase)
        times.append(max(t, times[-1] + 1.7) if times else max(t, t0 + 0.3))
    bx, by, s = x0 + 118, y0 + 106, FACE_S
    R = HEAD_R * s
    keys = _head_keys(times)
    end = keys[-1][0]
    kt = ";".join(f"{t / end:.4f}" for t, _p in keys)
    out = [f'<defs><clipPath id="fcard"><rect x="{x0}" y="{y0}" width="{w}" '
           f'height="{h}" rx="14"/></clipPath></defs>'
           f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="14" '
           f'fill="{rgb(PANEL)}" stroke="{rgb(SAND_DIM)}" stroke-width="1.5"/>']
    bust = [("fill", F.smooth([(-23, -29.2), (-18, -17), (-6, -13), (6, -13),
                               (18, -17), (23, -29.2)]), "robe"),
            ("fill", F.taper([(0, -15), (0, -7)], [8.5, 8], round_end=False),
             "skin")]
    out.append(fig(bust, s, CREATURE, bx, by, page=PANEL))
    # the shadow the head throws on the neck, and the block the faces are on
    out.append(f'<ellipse cx="{bx}" cy="{by + 10.6 * s:.1f}" rx="{4.4 * s:.1f}" '
               f'ry="{1.3 * s:.1f}" fill="rgb(0,0,0)" fill-opacity="0.3"/>')
    core = F._mix(PANEL, CREATURE, 0.1)
    out.append(f'<ellipse cx="{bx}" cy="{by}" rx="{8.4 * s:.1f}" '
               f'ry="{9.2 * s:.1f}" fill="{rgb(core)}"/>')
    for kind, _phrase in FACE_SAID:
        xs, sc, sh = [], [], []
        for _t, phi in keys:
            a = math.radians(FACE_BEARING[kind] + phi)
            c = max(0.0, math.cos(a))
            depth = 0.9 + 0.1 * c                # smaller as it goes back
            xs.append(f"{R * math.sin(a) * (1 if c else 0):.1f} 0")
            sc.append(f"{c * depth:.3f} {depth:.3f}")
            sh.append("0" if c > 0.86 else "0.2" if c > 0.5 else "0.4")
        parts = F.creature_face(kind)
        clip = f"fc_{kind}"
        out.append(
            f'<defs><clipPath id="{clip}">{_clip_shapes(parts, s)}</clipPath>'
            f'</defs><g transform="translate({bx} {by})">'
            f'<g transform="translate({xs[0]})"><animateTransform '
            f'attributeName="transform" type="translate" values="{";".join(xs)}" '
            f'keyTimes="{kt}" dur="{end:.2f}s" fill="freeze"/>'
            f'<g transform="scale({sc[0]})"><animateTransform '
            f'attributeName="transform" type="scale" values="{";".join(sc)}" '
            f'keyTimes="{kt}" dur="{end:.2f}s" fill="freeze"/>'
            f'{fig(parts, s, CREATURE, page=PANEL)}'
            f'<g clip-path="url(#{clip})">'
            # the flat shadow down its off side
            f'<ellipse cx="{R * 1.5:.1f}" cy="{-2 * s:.1f}" rx="{R * 1.06:.1f}" '
            f'ry="{R * 1.7:.1f}" fill="rgb(0,0,0)" fill-opacity="0.24"/>'
            # and the shade it takes as it turns from the light
            f'<rect x="{-R * 1.6:.1f}" y="{-R * 1.6:.1f}" width="{R * 3.2:.1f}" '
            f'height="{R * 3.2:.1f}" fill="rgb(0,0,0)" opacity="{sh[0]}">'
            f'<animate attributeName="opacity" values="{";".join(sh)}" '
            f'keyTimes="{kt}" dur="{end:.2f}s" fill="freeze"/></rect>'
            f'</g></g></g></g>')
    # the head from above: where each face looks out
    px, py, PR = x0 + 300, y0 + 122, 46
    out.append(f'<circle cx="{px}" cy="{py}" r="{PR}" fill="none" '
               f'stroke="{rgb(SAND_DIM)}" stroke-width="1.5"/>'
               f'<circle cx="{px}" cy="{py}" r="9" fill="{rgb(FAR)}"/>')
    spots = {"man": (0, 1, "middle", 0, 20), "lion": (-1, 0, "end", -12, 0),
             "ox": (1, 0, "start", 12, 0), "eagle": (0, -1, "middle", 0, -20)}
    for (kind, _phrase), t in zip(FACE_SAID, times):
        dx, dy, anc, lx, ly = spots[kind]
        cx, cy = px + dx * PR, py + dy * PR
        out.append(f'<g opacity="0">{fade(t, 0.5)}<circle cx="{cx}" cy="{cy}" '
                   f'r="6" fill="{rgb(HL)}"/>'
                   + label(cx + lx, cy + ly, kind, 18, anchor=anc) + '</g>')
    return (f'<g opacity="0">{fade(t0, 0.6)}' + "".join(out) + '</g>',
            max(end, times[-1] + 0.5))


# when each layer of a creature first shows: (verse, phrase)
CREATURE_IN = {"wings_up": (6, "four wings"), "wings_down": (24, "let down"),
               "hands": (8, "hands of a man"),
               "body": (5, "four living creatures"), "hooves": (7, "calf"),
               "cover": (6, "four wings"), "lion": (6, "four faces"),
               "ox": (6, "four faces"), "man": (5, "four living creatures")}
WHEEL_IN = {"wings": (15, "one wheel"),
            "outer": (15, "one wheel"), "inner": (16, "a wheel within a wheel"),
            "eyes": (18, "full of eyes")}


def face_xy(x0, name, s=S_FRONT, g=G_FRONT):
    fx, fy, r = F.LIVING_CREATURE_FACES[name]
    return x0 + fx * s, g - fy * s, r * s


# ---------------------------------------------------------------------------
# A verse
# ---------------------------------------------------------------------------

def frame(v, text):
    say = Say(v, text)
    ends = []

    def cue(phrase, nth=0):
        """Just before the phrase is said, and early enough to finish."""
        return max(0.0, min(say.at(phrase, nth), round(say.end() - 2.0, 2)))

    def show(v_in, svg, phrase=None, d=0.8, v_out=None, nth=0):
        """`svg` from the verse that says it on: fading in on its word that
        verse, held after, and gone after `v_out`."""
        if v < v_in:
            return ""
        if v_out is not None and v > v_out:
            if v == v_out + 1:
                ends.append(0.6)
                return f'<g>{fade(0, 0.6, out=True)}{svg}</g>'
            return ""
        if v > v_in:
            return svg
        t = cue(phrase, nth) if phrase else 0.0
        ends.append(t + d)
        return f'<g opacity="0">{fade(t, d)}{svg}</g>'

    def only(svg, phrase=None, d=0.6, nth=0):
        """A name or mark for this verse alone, in on its word."""
        t = cue(phrase, nth) if phrase else 0.2
        ends.append(t + d)
        return f'<g opacity="0">{fade(t, d)}{svg}</g>'

    def pulse(cx, cy, rx, ry, phrase, nth=0):
        t = cue(phrase, nth)
        ends.append(t + 1.8)
        return ring(cx, cy, rx, ry, t)

    o = [f'<rect width="{W}" height="{H}" fill="{rgb(BG)}"/>']

    # -- the heavens opened (1:1), until the cloud comes ---------------------
    o.append(show(1, f'<ellipse cx="{CX}" cy="150" rx="250" ry="54" '
                     f'fill="url(#glory)"/><line x1="{CX - 190}" y1="150" '
                     f'x2="{CX + 190}" y2="150" stroke="{rgb(HL)}" '
                     f'stroke-width="1.6" stroke-opacity="0.8"/>',
                  "heavens were opened", d=1.4, v_out=3))
    if v == 3:                                  # Yahweh's hand was on him
        o.append(only(f'<polygon points="{CX + 120},168 {CX + 190},158 '
                      f'{EZ_X + 26},{STRIP - 58} {EZ_X - 26},{STRIP - 58}" '
                      f'fill="url(#glory)" opacity="0.5"/>', "hand", d=1.2))

    # -- the great cloud out of the north (1:4) ------------------------------
    cloud = F.cloud()
    x0, x1, y0, y1 = F.bbox((cloud, 0))
    kx, ky = 880 / (x1 - x0), 250 / (y1 - y0)
    big = [(k, [(x * kx - (x0 + x1) / 2 * kx, y * ky) for x, y in d], m)
           for k, d, m in cloud]
    cl = fig(big, 1.0, CLOUD)
    if v == 4:
        t = cue("great cloud")
        ends.append(t + 2.4)
        o.append(f'<g transform="translate({CX} 512)" opacity="0">'
                 f'{fade(t, 1.2)}<g><animateTransform attributeName="transform" '
                 f'type="scale" values="0.3;1" begin="{t:.2f}s" dur="2.4s" '
                 f'fill="freeze" calcMode="spline" keyTimes="0;1" '
                 f'keySplines="0.2 0 0.2 1"/>{cl}</g></g>')
    elif v > 4:
        o.append(f'<g transform="translate({CX} 512)">{cl}</g>')
    o.append(show(4, f'<ellipse cx="{CX}" cy="430" rx="330" ry="150" '
                     f'fill="url(#storm)"/>', "brightness", d=1.4))
    o.append(show(4, f'<circle cx="{CX}" cy="440" r="34" fill="url(#core)"/>',
                  "glowing metal", d=1.0, v_out=12))

    # -- the ground, the river and the people by it --------------------------
    o.append(f'<line x1="60" y1="{G_FRONT + 16}" x2="{W - 60}" '
             f'y2="{G_FRONT + 16}" stroke="{rgb(SAND_DIM)}" stroke-width="1"/>')
    waves = []
    c = SvgCanvas(10, 10)
    for k in range(3):
        y = 542 + k * 8
        pts = [(380 + i * 12, y + (2.4 if i % 2 else -2.4)) for i in range(23)]
        c.polyline(F.smooth(pts, closed=False, n=4), stroke=WATER, width=1.3)
    waves = "".join(c._els)
    o.append(show(1, waves, "river Chebar"))
    people = "".join(fig(mk, 0.5, SAND, x, STRIP)
                     for x, mk in ((70, F.man()), (112, F.woman()),
                                   (146, F.child()), (188, F.man(staff=True))))
    o.append(show(1, people, "captives", v_out=3))
    if v < 28:
        o.append(fig(F.man(), 0.55, TEXT, EZ_X, STRIP))
    else:                                       # I fell on my face
        t = cue("fell on my face")
        ends.append(t + 0.5)
        o.append(f'<g>{fade(t, 0.3, out=True)}'
                 f'{fig(F.man(), 0.55, TEXT, EZ_X, STRIP)}</g>'
                 f'<g opacity="0">{fade(t, 0.3)}'
                 f'{fig(F.man(pose="kneel"), 0.55, TEXT, EZ_X, STRIP)}</g>')

    # -- the four, and their wheels ------------------------------------------
    def host(inner):
        """They rise from the earth (1:19) and stand again (1:21)."""
        mv = ""
        dy = LIFT if v == 20 else 0
        if v == 19:
            t = cue("lifted up")
            ends.append(t + 1.6)
            mv = (f'<animateTransform attributeName="transform" '
                  f'type="translate" values="0 0;0 {LIFT}" begin="{t:.2f}s" '
                  f'dur="1.6s" fill="freeze" calcMode="spline" keyTimes="0;1" '
                  f'keySplines="0.42 0 0.58 1"/>')
        elif v == 21:
            dy = LIFT
            t = cue("stood")
            ends.append(t + 1.6)
            mv = (f'<animateTransform attributeName="transform" '
                  f'type="translate" values="0 {LIFT};0 0" begin="{t:.2f}s" '
                  f'dur="1.6s" fill="freeze" calcMode="spline" keyTimes="0;1" '
                  f'keySplines="0.42 0 0.58 1"/>')
        elif v == 14:                           # ran and returned
            t = cue("ran")
            ends.append(t + 0.7)
            mv = (f'<animateTransform attributeName="transform" '
                  f'type="translate" values="0 0;44 0;0 0" begin="{t:.2f}s" '
                  f'dur="0.7s" fill="freeze" calcMode="spline" '
                  f'keyTimes="0;0.4;1" keySplines="0.3 0 0.2 1;0.4 0 0.6 1"/>')
        return f'<g transform="translate(0 {dy})">{mv}{inner}</g>'

    def row(tag, xs, g, wxs, wg, s):
        # the glow each of them gives off, like a coal
        out = [show(13, "".join(
            f'<ellipse cx="{CX + sx * xs}" cy="{g - 62 * s:.0f}" '
            f'rx="{58 * s:.0f}" ry="{84 * s:.0f}" fill="url(#ember)"/>'
            for sx in (-1, 1)), "burning coals", d=1.6)]
        for k in F.WHEEL_IN_WHEEL_LAYERS:
            v_in, phrase = WHEEL_IN[k]
            out.append(show(v_in, "".join(use(f"{tag}w_{k}", CX + sx * wxs, wg)
                                          for sx in (-1, 1)), phrase))
        for k in F.LIVING_CREATURE_LAYERS:
            v_in, phrase = CREATURE_IN[k]

            def uses(t, k=k):
                return "".join(use(f"{t}_{k}", CX + sx * xs, g)
                               for sx in (-1, 1))
            if v > 13:                          # like burning coals of fire
                both = uses(tag + "h")
            elif v == 13:                       # the heat comes up over them
                tc = cue("burning coals")
                ends.append(tc + 1.6)
                both = (uses(tag) + f'<g opacity="0">{fade(tc, 1.6)}'
                        f'{uses(tag + "h")}</g>')
            else:
                both = uses(tag)
            if k == "wings_up":                 # let down at 1:24
                if v == 24:
                    t = cue("let down")
                    ends.append(t + 0.8)
                    out.append(f'<g>{fade(t, 0.8, out=True)}{both}</g>')
                elif v < 24:
                    out.append(show(v_in, both, phrase))
            else:
                out.append(show(v_in, both, phrase))
        return "".join(out)

    o.append(host(row("b", X_BACK, G_BACK, WX_BACK, G_BACK + 4, S_BACK)))

    # the fire that went up and down among them (1:13): it comes in low,
    # goes up between them, down, and comes to rest at their middle
    if v == 13:
        t = cue("The fire went up and down")
        ends.append(t + 3.0)
        o.append(f'<g transform="translate({CX} {G_FRONT - 8})" opacity="0">'
                 f'{fade(t, 0.5)}<animateTransform attributeName="transform" '
                 f'type="translate" values="{CX} {G_FRONT - 8};{CX} 372;'
                 f'{CX} {G_FRONT - 14};{CX} {FIRE_Y}" keyTimes="0;0.36;0.74;1" '
                 f'begin="{t:.2f}s" dur="3.0s" fill="freeze" calcMode="spline" '
                 f'keySplines="0.42 0 0.58 1;0.42 0 0.58 1;0.42 0 0.58 1"/>'
                 f'{fire_svg()}</g>')
    elif v > 13:
        o.append(f'<g transform="translate({CX} {FIRE_Y})">{fire_svg()}</g>')

    o.append(host(row("f", X_FRONT, G_FRONT, WX_FRONT, G_FRONT + 6, S_FRONT)))

    # -- lightning: once, and gone -------------------------------------------
    b1 = [(CX - 14, 372), (CX - 40, 352), (CX - 24, 346), (CX - 62, 322)]
    b2 = [(CX + 16, 376), (CX + 42, 356), (CX + 28, 350), (CX + 64, 326)]
    if v == 4:
        t = cue("flashing lightning")
        o.append(bolt([(CX - 150, 300), (CX - 170, 336), (CX - 150, 342),
                       (CX - 176, 384)], t))
        o.append(bolt([(CX + 170, 310), (CX + 150, 344), (CX + 168, 350),
                       (CX + 146, 390)], t + 0.4))
        ends.append(t + 2.0)
    if v == 13:
        t = cue("lightning went out")
        o.append(bolt(b1, t) + bolt(b2, t + 0.3))
        ends.append(t + 1.9)
    if v == 14:
        t = cue("flash of lightning")
        o.append(bolt([(CX - 150, 430), (CX - 60, 410), (CX - 20, 428),
                       (CX + 150, 404)], t))
        ends.append(t + 1.6)

    # -- the expanse over their heads (1:22) ---------------------------------
    exp = (f'<ellipse cx="0" cy="0" rx="372" ry="20" fill="url(#ice)" '
           f'stroke="{rgb(CRYSTAL)}" stroke-width="1.6"/>'
           f'<ellipse cx="0" cy="-3" rx="352" ry="13" fill="none" '
           f'stroke="{rgb(CRYSTAL)}" stroke-opacity="0.45" stroke-width="1"/>'
           + "".join(f'<line x1="{k * 62 - 9}" y1="9" x2="{k * 62 + 9}" y2="-9" '
                     f'stroke="{rgb(CRYSTAL)}" stroke-opacity="0.4" '
                     f'stroke-width="1"/>' for k in range(-5, 6)))
    if v == 22:
        t = cue("expanse")
        ends.append(t + 1.8)
        o.append(f'<g transform="translate({CX} {EXP_Y})" opacity="0">'
                 f'{fade(t, 0.6)}<g><animateTransform attributeName="transform" '
                 f'type="scale" values="0.1 1;1 1" begin="{t:.2f}s" dur="1.8s" '
                 f'fill="freeze" calcMode="spline" keyTimes="0;1" '
                 f'keySplines="0.2 0 0.2 1"/>{exp}</g></g>')
    elif v > 22:
        o.append(f'<g transform="translate({CX} {EXP_Y})">{exp}</g>')

    # -- the throne, the fire on it and the brightness (1:26-28) -------------
    o.append(show(27, f'<circle cx="{GLORY[0]}" cy="{GLORY[1]}" r="190" '
                      f'fill="url(#glory)"/>', "brightness", d=1.6))
    if v == 28:
        t = cue("rainbow")
        dy = BASE - 8 - GLORY[1]
        for i, col in enumerate(RAINBOW):
            r = 166 - i * 5.5
            dx = math.sqrt(r * r - dy * dy)
            L = 2 * math.pi * r
            o.append(f'<path d="M{CX - dx:.1f} {BASE - 8} A{r} {r} 0 1 1 '
                     f'{CX + dx:.1f} {BASE - 8}" fill="none" stroke="{rgb(col)}" '
                     f'stroke-width="5" stroke-opacity="0.7" '
                     f'stroke-dasharray="{L:.0f}" stroke-dashoffset="{L:.0f}">'
                     f'<animate attributeName="stroke-dashoffset" '
                     f'values="{L:.0f};0" begin="{t + i * 0.14:.2f}s" dur="1.2s" '
                     f'fill="freeze"/></path>')
        ends.append(t + 1.9)
    o.append(show(26, fig(throne_parts(), S_T, SAPPHIRE, CX, THRONE_Y),
                  "likeness of a throne", d=1.2))
    o.append(show(26, f'<path d="{flame_path()}" fill="rgb(255,236,170)" '
                      f'stroke="{rgb(HL)}" '
                      f'stroke-width="1.4"/>', "a likeness as", d=1.4))
    o.append(show(27, f'<path d="{flame_path()}" fill="url(#him)" '
                      f'stroke="{rgb(HL)}" stroke-width="1.4"/>',
                  "glowing metal", d=1.4))

    # -- this verse's names, numbers and marks -------------------------------
    def top(line, text_, phrase, dim=False, nth=0, size=None):
        y = TOP1 if line == 1 else TOP2
        if v >= 26:
            y -= 208                          # over the brightness
        elif v >= 22:
            y -= 40                           # over the expanse
        return only(label(CX, y, text_, size or (15 if dim else 18),
                          TEXT_DIM if dim else TEXT, italic=dim), phrase,
                    nth=nth)

    fl, fr = CX - X_FRONT, CX + X_FRONT
    joints = ((CX - 132, 318), (CX, 316), (CX + 132, 318))
    if v == 1:
        o.append(only(label(CX, 300, "year 30 · month 4 · day 5", 22),
                      "thirtieth year"))
        o.append(only(label(160, 500, "captives", 14, TEXT_DIM, italic=True),
                      "captives"))
        o.append(only(label(CX, 528, "river Chebar", 14, TEXT_DIM, italic=True),
                      "river Chebar"))
    elif v == 2:
        o.append(only(label(CX, 280, "day 5", 22), "fifth of the month"))
        o.append(only(label(CX, 312, "Jehoiachin’s captivity · year 5",
                            20), "fifth year"))
    elif v == 3:
        o.append(only(label(EZ_X + 50, 484, "Ezekiel", 16, anchor="end"),
                      "Ezekiel"))
        o.append(only(label(EZ_X - 60, 548, "the priest · son of Buzi", 13,
                            TEXT_DIM, anchor="end", italic=True), "the priest"))
        o.append(only(label(CX, 528, "land of the Chaldeans", 14, TEXT_DIM,
                            italic=True), "land of the Chaldeans"))
    elif v == 4:
        o.append(only(label(CX, 226, "out of the north", 18), "north"))
        o.append(only(label(CX, 486, "glowing metal", 14, TEXT_DIM,
                            italic=True), "glowing metal"))
    elif v == 5:
        o.append(top(1, "4 living creatures", "four living creatures"))
        o.append(top(2, "the likeness of a man", "likeness of a man", dim=True))
    elif v == 6:
        o.append(top(1, "4 faces", "four faces"))
        o.append(top(2, "4 wings", "four wings", size=18))
    elif v == 7:
        for x in (fl, fr):
            o.append(pulse(x, G_FRONT - 4, 22, 11, "calf"))
        o.append(top(1, "a calf’s foot", "calf"))
        o.append(top(2, "like burnished brass", "burnished brass", dim=True))
    elif v == 8:
        for x in (fl, fr):
            for sx in (-1, 1):
                o.append(pulse(x + sx * 44, G_FRONT - 70, 12, 14,
                               "hands of a man"))
        o.append(top(1, "hands of a man", "hands of a man"))
        o.append(top(2, "under their wings", "under their wings", dim=True))
    elif v == 9:
        for x, y in joints:
            o.append(pulse(x, y, 16, 12, "joined"))
        o.append(top(1, "wings joined", "joined"))
        o.append(top(2, "straight forward", "straight forward", dim=True))
    elif v == 10:
        card, last = faces_card(cue)
        ends.append(last)
        o.append(card)
        for name, phrase in FACE_SAID[:3]:
            for x0 in (fl, fr):
                x, y, r = face_xy(x0, name)
                o.append(pulse(x, y, r, r, phrase))
    elif v == 11:
        for x, y in joints:
            o.append(pulse(x, y, 16, 12, "touched"))
        for x in (fl, fr):
            o.append(pulse(x, G_FRONT - 70, 30, 44, "covered"))
        o.append(top(1, "2 touching", "touched"))
        o.append(top(2, "2 covering", "covered", size=18))
    elif v == 12:
        o.append(top(1, "the spirit", "spirit"))
        o.append(top(2, "straight forward", "straight forward", dim=True))
    elif v == 13:
        o.append(top(1, "like burning coals", "burning coals"))
        o.append(top(2, "like torches", "torches", size=18))
    elif v == 14:
        o.append(top(1, "as a flash of lightning", "flash of lightning"))
    elif v == 15:
        o.append(top(1, "4 wheels", "one wheel"))
        o.append(top(2, "on the earth", "on the earth", dim=True))
    elif v == 16:
        o.append(top(1, "beryl", "beryl"))
        o.append(top(2, "a wheel within a wheel", "a wheel within a wheel",
                     size=18))
        for sx in (-1, 1):
            o.append(pulse(CX + sx * WX_FRONT, G_FRONT + 6 - 72, 30, 74,
                           "a wheel within a wheel"))
    elif v == 17:
        wx, wy = CX - WX_FRONT, G_FRONT + 6 - 72
        t = cue("four directions")
        ends.append(t + 0.6)
        arr = "".join(arrow((wx + dx * 20, wy + dy * 20),
                            (wx + dx * 56, wy + dy * 56))
                      for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        o.append(f'<g opacity="0">{fade(t, 0.6)}{arr}</g>')
        o.append(top(1, "4 directions", "four directions"))
    elif v == 18:
        for sx in (-1, 1):
            o.append(pulse(CX + sx * WX_FRONT, G_FRONT + 6 - 72, 76, 76,
                           "full of eyes"))
        o.append(top(1, "rims high", "high"))
        o.append(top(2, "full of eyes", "full of eyes", size=18))
    elif v == 19:
        o.append(top(1, "lifted up", "lifted up"))
    elif v == 20:
        o.append(top(1, "the spirit", "spirit of the living creature"))
        o.append(top(2, "in the wheels", "in the wheels", dim=True))
    elif v == 21:
        o.append(top(1, "went · stood · lifted up", "When those went"))
    elif v == 22:
        o.append(top(1, "expanse", "expanse"))
        o.append(top(2, "like crystal", "crystal", dim=True))
    elif v == 23:
        for x in (fl, fr):
            o.append(pulse(x, G_FRONT - 70, 30, 44, "covered"))
        o.append(top(1, "under the expanse", "Under the expanse"))
        o.append(top(2, "2 covering", "covered", dim=True))
    elif v == 24:
        t = cue("noise of their wings")
        for x, g, s in ((fl, G_FRONT, S_FRONT), (fr, G_FRONT, S_FRONT)):
            for sx in (-1, 1):
                o.append(arcs(x + sx * 40 * s, g - 96 * s,
                              -90 + sx * 40, t, r=14, grow=2.6))
        ends.append(t + 1.85)
        o.append(top(1, "the noise of their wings", "noise of their wings"))
        o.append(top(2, "like great waters", "great waters", dim=True))
    elif v == 25:
        t = cue("voice")
        o.append(arcs(CX, 150, 90, t, r=22, grow=3.4))
        ends.append(t + 1.85)
        o.append(top(1, "a voice", "voice"))
        o.append(top(2, "above the expanse", "above the expanse", dim=True))
    elif v == 26:
        o.append(only(label(CX + 78, SEAT - 20, "throne", 18, anchor="start"),
                      "likeness of a throne"))
        o.append(only(label(CX + 78, SEAT, "like sapphire", 14, TEXT_DIM,
                            anchor="start", italic=True), "sapphire"))
    elif v == 27:
        o.append(only(leader((CX - 24, SEAT - 76), (CX - 144, SEAT - 76))
                      + label(CX - 150, SEAT - 76, "glowing metal", 17,
                              anchor="end"), "glowing metal"))
        o.append(only(leader((CX - 26, SEAT - 16), (CX - 144, SEAT - 16))
                      + label(CX - 150, SEAT - 16, "fire", 17, anchor="end"),
                      "downward"))
        o.append(only(label(CX + 150, SEAT - 76, "brightness", 17,
                            anchor="start"), "brightness"))
    elif v == 28:
        o.append(only(label(CX + 196, 110, "like the rainbow", 16,
                            anchor="start"), "rainbow"))
        o.append(only(label(CX, 30, "Yahweh’s glory", 20), "glory"))
        t = cue("voice of one")
        o.append(arcs(CX + 60, 190, 30, t, r=22, grow=3.4))
        ends.append(t + 1.85)

    body = "".join(x for x in o if x)
    svg =(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
           f'width="{W}" height="{H}" font-family="{FONT_FAMILY}" '
           f'data-kind="diagram"><defs>{DEFS}{_symbols_used(body)}</defs>'
           f'{body}</svg>')
    return svg, say, max(ends or [0.0])


def _symbols_used(body):
    """The creature and wheel layers this verse draws."""
    LC, WH = F.living_creature_layers(), F.wheel_in_wheel_layers()
    out = []
    for row, s, ink, wink in (("b", S_BACK, FAR, WHEEL_FAR),
                              ("f", S_FRONT, CREATURE, WHEEL),
                              ("bh", S_BACK, HOT_FAR, None),
                              ("fh", S_FRONT, HOT, None)):
        for k, parts in LC.items():
            if f'href="#{row}_{k}"' in body:
                out.append(f'<g id="{row}_{k}">{fig(parts, s, ink)}</g>')
        if wink is None:
            continue
        for k, parts in WH.items():
            if f'href="#{row}w_{k}"' in body:
                out.append(f'<g id="{row}w_{k}">{fig(parts, s, wink)}</g>')
    return "".join(out)


def main():
    import xml.dom.minidom
    texts = _text()
    problems = []
    files = {}
    for v in verse_numbers(BOOK, CHAPTER):
        svg, say, last = frame(v, texts[v])
        xml.dom.minidom.parseString(svg)        # an <img> shows nothing else
        end = say.end()
        if last > end + 0.05:
            problems.append(f"1:{v}: motion ends at {last:.1f}s, the verse "
                            f"at {end:.1f}s")
        files[v] = svg
        print(f"1:{v:<2} {len(svg) // 1024:>3} KB  ends {last:5.1f}s of "
              f"{end:5.1f}s  {'clock' if say.clock else 'estimated'}")
    for p in problems:
        print("[WARN]", p)
    for v, svg in files.items():
        with open(out_path(BOOK, CHAPTER, f"{BOOK}_{CHAPTER}_{v}.svg"), "w",
                  encoding="utf-8") as f:
            f.write(svg)
    print(f"[OK] {len(files)} files")


if __name__ == "__main__":
    main()
