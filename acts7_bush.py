"""The bush at Mount Sinai (Acts 7:31-34) as a scene card the camera dives
into, built like the Jerusalem card (acts7_council.py).

A side view at the mountain's foot: the granite massif behind, the
wilderness ground, a small flock (Exodus 3:1, where Moses is keeping
Jethro's sheep), and the thornbush burning. The flame is the appearing
(7:30, "an angel of the Lord ... in a flame of fire in a bush"); no angel
and no figure of God is drawn. The voice of the Lord is drawn as arcs
going out from the bush, as the verse says it comes.

The story is acted, not captioned: Moses comes close to see (7:31); hearing "I
am the God of your fathers" he trembles and goes down on his knees (7:32);
his sandals come off and are set by him, and the ground about the bush
lights, holy ground (7:33); a light comes down on the bush at "I have come
down", and at "Now come, I will send you" he stands (7:34). 7:35 flies
out to the map, where he goes back to Egypt.

Card px: x from -600 to 3600, y 0 to 2200, the ground at y 1400. A man is
110 px tall. generate_acts7_svg.py flies it.
"""

import math

import svg_figures as F
from svg_scene_card import (Actor, Card, MAN_H, figure_svg, person,
                            static)
from svg_map_camera import fade, rgb
from svg_surface import _fmt
from generate_tabernacle import SAND, SAND_DIM, TEXT, HL
from acts1314_lystra import (MAN, SKY, EARTH, HILL, S_CARD, scaled_h,
                             figure_svg_at)

GROUND = 1400
BX = 1500                       # the bush
ANCHOR = (BX, GROUND - 60)      # the card point hung on Mount Sinai's dot
ORIGIN = (-600, 0)
SIZE = (4200, 2200)
GRANITE = (46, 36, 32)          # Jebel Musa's red granite, in the dark
RIDGE = (64, 50, 42)
BUSH_INK = (150, 162, 104)      # the one green thing on the card
SUMMIT = (1920, 690)

MOSES_X = BX - 620              # where he stands with the flock
CLOSE_X = BX - 240              # where he comes to (7:31)
SANDALS_X = CLOSE_X + 52


def mountain(X0, X1, g):
    """The massif: its outline, and the seams down its faces."""
    outline = [(X0, 1250), (-200, 1180), (300, 1090), (700, 960),
               (950, 1000), (1200, 870), (1450, 810), (1700, 730), SUMMIT,
               (2080, 760), (2250, 735), (2500, 880), (2800, 960),
               (3100, 1060), (X1, 1150), (X1, g), (X0, g)]
    seams = [[SUMMIT, (1880, 860), (1760, 1010), (1700, 1180)],
             [(2250, 735), (2280, 900), (2380, 1080)],
             [(1450, 810), (1400, 960), (1300, 1120)],
             [(1200, 870), (1120, 1020)],
             [(700, 960), (760, 1120)]]
    out = ['<polygon points="' + " ".join(f"{x},{y}" for x, y in outline)
           + f'" fill="{rgb(GRANITE)}" stroke="{rgb(SAND_DIM)}" '
           f'stroke-width="2"/>']
    for s in seams:
        out.append('<polyline points="' + " ".join(f"{x},{y}" for x, y in s)
                   + f'" fill="none" stroke="{rgb(RIDGE)}" stroke-width="3" '
                   f'stroke-linecap="round" stroke-linejoin="round"/>')
    return out


def build(town_xy):
    c = Card("bush7", town_xy, ANCHOR, SIZE, S_CARD, page=EARTH, sky=SKY,
             ground_y=GROUND, origin=ORIGIN)
    c.share_bodies = True
    c.names_at = (0.40, 0.48)
    X0, X1 = ORIGIN[0], ORIGIN[0] + SIZE[0]
    sc = c.scenery
    g = GROUND

    # -- scenery ----------------------------------------------------------
    far = [(X0, 1150), (200, 1100), (900, 1130), (2600, 1090), (3300, 1120),
           (X1, 1100), (X1, g), (X0, g)]
    sc.append('<polygon points="' + " ".join(f"{x},{y}" for x, y in far)
              + f'" fill="{rgb(HILL)}"/>')
    sc.extend(mountain(X0, X1, g))
    sc.append(f'<rect x="{X0}" y="{g}" width="{X1 - X0}" '
              f'height="{SIZE[1] - g}" fill="{rgb(EARTH)}"/>')
    sc.append(f'<line x1="{X0}" y1="{g}" x2="{X1}" y2="{g}" '
              f'stroke="{rgb(SAND_DIM)}" stroke-width="2"/>')
    # rocks fallen from the mountain
    for x, k in ((300, 0.7), (760, 0.5), (1980, 0.8), (2240, 0.5),
                 (2700, 0.9), (3100, 0.6)):
        sc.append(figure_svg_at(F.stone(), x, g + 6, scaled_h("stone") * k,
                                SAND_DIM, unit_h=MAN_H * F.UNIT["stone"]))
    # the flock
    for x, lamb, flip in ((MOSES_X - 330, False, 1), (MOSES_X - 230, True, -1),
                          (MOSES_X - 150, False, -1), (MOSES_X - 420, False, 1)):
        sc.append(figure_svg_at(F.sheep(lamb=lamb), x, g + 10, MAN, SAND,
                                flip=flip))
    # the bush's stems and back leaves (its flames, and the front leaves
    # they stand behind, are drawn over these as effects, so they can move)
    sc.append(figure_svg_at(F.bush("back"), BX, g, MAN, BUSH_INK))

    # -- the cast ---------------------------------------------------------
    c.add(Actor("mount_name", static(lambda: []), 1560, 900, h=1,
                unit_h=1, label="Mount Sinai", shown=True, label_y=-20))
    # drawn a third over true size, so a pair reads at this distance
    c.add(Actor("sandals", static(F.sandals), CLOSE_X, g + 18, h=MAN * 1.35,
                unit_h=MAN_H, ink=SAND))
    c.add(Actor("moses", person("man", staff=True), MOSES_X, g + 14,
                ink=TEXT, flip=1, shown=True, label="Moses",
                label_y=-(MAN + 30)))

    c.refs = [(7, v) for v in range(30, 36)]
    events(c)
    effects(c)
    return c


def events(c):
    on = c.on
    # 7:31 he sees it and wonders; he comes close to see
    on((7, 31), ("pose", "moses", 3.1, 0.1, {"pose": "walk"}),
       ("move", "moses", 3.1, 1.3, (CLOSE_X - MOSES_X, 0)),
       ("pose", "moses", 4.4, 0.2, {"pose": "stand"}))
    # 7:32 I am the God of your fathers ... Moses trembled, and dared not
    # look: a shiver, and he goes down on his knees (a figure drawn facing
    # us cannot turn its face away, so the fear is told by the kneeling)
    for k, dx in enumerate((5, -10, 10, -10, 5)):
        on((7, 32), ("move", "moses", 6.0 + k * 0.12, 0.12, (dx, 0)))
    on((7, 32), ("pose", "moses", 7.0, 0.4, {"pose": "kneel"}))
    # 7:33 Take off your sandals: they come off his feet and are set by him;
    # for the place where you stand is holy ground
    on((7, 33), ("show", "sandals", 2.4, 0.3, None),
       ("move", "sandals", 2.6, 0.6, (SANDALS_X - CLOSE_X, 0)))
    # 7:34 ... Now come, I will send you into Egypt: he stands, and is sent
    on((7, 34), ("pose", "moses", 6.8, 0.4, {"pose": "stand"}),
       ("pulse", "moses", 7.9, 0.8, None))


def flames(phase=0.0):
    """The flame in the bush, its two halves swaying out of step, slowly,
    each about its root: a fire that keeps burning, never a flicker."""
    out = []
    for which, dur, vals in ((0, 2.6, "1 1;1.05 1.08;0.97 0.96;1 1"),
                             (1, 3.4, "1 1;0.96 1.05;1.04 0.97;1 1")):
        fig = figure_svg(F.bush_flames(which), MAN, HL, EARTH)
        out.append(f'<g transform="translate({BX} {GROUND})"><g>'
                   f'<animateTransform attributeName="transform" type="scale" '
                   f'values="{vals}" dur="{dur}s" begin="{-phase:.2f}s" '
                   f'repeatCount="indefinite"/>{fig}</g></g>')
    return "".join(out)


def voice(t):
    """The voice of the Lord going out from the bush toward Moses: three
    arcs on its near side, each widening and fading once (drawn at the
    origin and moved to the bush, so each scales about it)."""
    cx, cy = BX - 20, GROUND - 70
    out = []
    for k in range(3):
        b = t + k * 0.35
        a0, a1 = math.radians(150), math.radians(210)
        p0 = (40 * math.cos(a0), 40 * math.sin(a0))
        p1 = (40 * math.cos(a1), 40 * math.sin(a1))
        out.append(
            f'<g opacity="0"><animate attributeName="opacity" '
            f'values="0;0.9;0" begin="{b:.2f}s" dur="1.4s" fill="freeze"/>'
            f'<path d="M{_fmt(p0[0])} {_fmt(p0[1])} A40 40 0 0 1 '
            f'{_fmt(p1[0])} {_fmt(p1[1])}" fill="none" stroke="{rgb(HL)}" '
            f'stroke-width="2.2" stroke-linecap="round" '
            f'vector-effect="non-scaling-stroke">'
            f'<animateTransform attributeName="transform" type="scale" '
            f'values="1;4" begin="{b:.2f}s" dur="1.4s" fill="freeze"/>'
            f'</path></g>')
    return f'<g transform="translate({cx} {cy})">' + "".join(out) + "</g>"


GLOW_DEF = (f'<radialGradient id="bush7"><stop offset="0" '
            f'stop-color="rgb(255,226,150)" stop-opacity="0.42"/><stop '
            f'offset="1" stop-color="rgb(255,226,150)" stop-opacity="0"/>'
            f'</radialGradient>')
GROUND_DEF = (f'<radialGradient id="holy7"><stop offset="0" '
              f'stop-color="{rgb(HL)}" stop-opacity="0.45"/><stop '
              f'offset="1" stop-color="{rgb(HL)}" stop-opacity="0"/>'
              f'</radialGradient>')


def effects(c):
    g = GROUND
    glow = (f'<defs>{GLOW_DEF}</defs><circle cx="{BX}" cy="{g - 70}" r="170" '
            f'fill="url(#bush7)"/>')
    holy = (f'<ellipse cx="{BX - 110}" cy="{g + 16}" rx="420" ry="46" '
            f'fill="url(#holy7)"')
    front = figure_svg_at(F.bush("front"), BX, g, MAN, BUSH_INK)
    for k, r in enumerate([(7, v) for v in range(30, 36)]):
        c.effect(r, glow, under=True)
        c.effect(r, flames(phase=0.7 * k) + front, under=True)
    c.effect((7, 31), voice(4.8), under=True)
    c.effect((7, 32), voice(0.2), under=True)
    c.effect((7, 33), voice(0.2), under=True)
    c.effect((7, 34), voice(0.1), under=True)
    # 7:33 holy ground: the ground about the bush lights, and stays lit
    c.effect((7, 33), f'<defs>{GROUND_DEF}</defs>{holy} opacity="0">'
                      f'{fade(4.5, 1.2)}</ellipse>', under=True)
    for r in ((7, 34), (7, 35)):
        c.effect(r, f'<defs>{GROUND_DEF}</defs>{holy}/>', under=True)
    # 7:34 I have come down to deliver them: a light comes down on the bush
    c.effect((7, 34),
             f'<circle cx="{BX}" cy="{g - 60}" r="90" fill="url(#bush7)" '
             f'opacity="0"><animate attributeName="opacity" '
             f'values="0;1;1;0" keyTimes="0;0.2;0.7;1" begin="5.0s" '
             f'dur="2.0s" fill="freeze"/><animateTransform '
             f'attributeName="transform" type="translate" values="0 -520;0 0" '
             f'begin="5.0s" dur="1.2s" fill="freeze"/></circle>', under=True)


# camera shots inside the card: (x, y, zoom)
WIDE_IN = (BX - 300, 1180, 0.55)
NEAR = (BX - 120, 1290, 1.0)
WIDE_OUT = (BX - 220, 1200, 0.62)
SHOTS = {(7, 31): NEAR, (7, 32): NEAR, (7, 33): NEAR, (7, 34): WIDE_OUT}
# shots on the way: (verse) -> [(kind, (x, y, z) or None, seconds)]
LEGS = {
    (7, 31): [("hold", None, 0.1), ("to", WIDE_IN, 2.7), ("to", NEAR, 1.6)],
    (7, 34): [("hold", None, 6.2), ("to", WIDE_OUT, 2.0)],
}
DUR = {(7, 32): 0.0, (7, 33): 0.0}
