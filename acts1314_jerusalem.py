"""Jerusalem (Acts 13:27-37) as a scene card the camera dives into.

The middle of Paul's sermon happened in one city, so the camera goes there:
the City of David's hill with the royal tombs cut in its face, the city and
the Temple, a scroll on its stand, Pilate's seat between two pillars, the
gate, the mound outside it, the garden and its tomb, and the road north to
Galilee. The light (who is Jesus, never drawn as a man) stands before the
rulers, is taken out through the gate to the cross and down from it, goes
into the tomb, the stone rolls shut, and at 13:30 rolls back as the light
rises out; the witnesses come down the road from Galilee. Then the proof
from the psalms: David's sealed tomb beside the open one, the one cracking
and growing over ("saw decay"), the other open ("no decay").

Card px: x from -1000 to 3000, y 0 to 2200, the ground at y 1400. A man is
110 px tall.
"""

import svg_figures as F
from svg_scene_card import Actor, Card, MAN_H
from svg_map_camera import rgb, traced_el
from svg_surface import _fmt
from generate_tabernacle import SAND, SAND_DIM, TEXT_DIM, HL
from acts1314_lystra import (MAN, SKY, EARTH, PAVE, HILL, S_CARD, person,
                             static, scaled_h, figure_svg_at, shifted)

GROUND = 1400
ANCHOR = (1180, 1260)
ORIGIN = (-1000, 0)
SIZE = (4000, 2200)
WALL = (42, 42, 34)
K = MAN / MAN_H                 # card px per figure unit, at true size
TOMB_F = 0.55                   # the tombs drawn a little over half size
MOUND = (1480, 1690, 1352)      # Golgotha: from, to, its top
GARDEN_TOMB = 1880
CROSS_X = 1580


def tomb_parts():
    """The tomb without its stone, and the stone alone centred on (0, 0),
    so the stone can roll (svg_figures.tomb draws them together)."""
    p = F.tomb()
    body, stone = p[:6], p[6:]
    u = F.UNIT["tomb"]
    return body, shifted(stone, -30 * u, -26 * u)


TOMB_BODY, TOMB_STONE = tomb_parts()
STONE_R = 25 * F.UNIT["tomb"]               # the stone's radius, units
STONE_ASIDE = 30 * F.UNIT["tomb"]           # its centre, units from the tomb
STONE_SHUT = -10 * F.UNIT["tomb"]           # the door's centre
STONE_Y = 26 * F.UNIT["tomb"]


def priest_make(**pose):
    return F.priest(**pose)


def build(town_xy):
    c = Card("jer", town_xy, ANCHOR, SIZE, S_CARD, page=EARTH, sky=SKY,
             ground_y=GROUND, origin=ORIGIN)
    X0, X1 = ORIGIN[0], ORIGIN[0] + SIZE[0]
    sc = c.scenery

    hills = [(X0, 1230), (-400, 1180), (200, 1220), (900, 1160),
             (1500, 1200), (2100, 1150), (2600, 1170), (X1, 1180),
             (X1, GROUND), (X0, GROUND)]
    sc.append(f'<polygon points="' + " ".join(f"{x},{y}" for x, y in hills)
              + f'" fill="{rgb(HILL)}" stroke="{rgb(SAND_DIM)}" '
              f'stroke-width="2"/>')
    sc.append(f'<rect x="{X0}" y="{GROUND}" width="{X1 - X0}" '
              f'height="{SIZE[1] - GROUND}" fill="{rgb(EARTH)}"/>')
    sc.append(f'<line x1="{X0}" y1="{GROUND}" x2="{X1}" y2="{GROUND}" '
              f'stroke="{rgb(SAND_DIM)}" stroke-width="2"/>')
    # the road north, from the garden to the horizon
    sc.append(f'<path d="M1990 {GROUND} C2300 {GROUND - 40} 2650 1260 '
              f'3000 1182 L3000 1190 C2650 1270 2300 {GROUND - 30} 2060 '
              f'{GROUND}Z" fill="{rgb(PAVE)}"/>')
    # the City of David's hill, its face cut for the royal tombs
    sc.append(f'<path d="M150 {GROUND} C180 1300 260 1250 420 1240 '
              f'C560 1232 680 1260 740 {GROUND}Z" fill="{rgb(HILL)}" '
              f'stroke="{rgb(SAND_DIM)}" stroke-width="2"/>')
    # the city and the Temple behind it
    sc.append(f'<rect x="900" y="1180" width="330" height="220" '
              f'fill="{rgb(WALL)}" stroke="{rgb(SAND_DIM)}" '
              f'stroke-width="2"/>')
    sc.append(f'<rect x="960" y="1080" width="210" height="100" '
              f'fill="{rgb(WALL)}" stroke="{rgb(SAND_DIM)}" '
              f'stroke-width="2"/>')
    sc.append(f'<rect x="1030" y="1110" width="70" height="70" '
              f'fill="{rgb(SKY)}" stroke="{rgb(SAND_DIM)}" stroke-width="2"/>')
    for k, x in enumerate((760, 1260)):
        sc.append(figure_svg_at(F.house(), x, GROUND,
                                scaled_h("house") * (0.7 if k else 0.8),
                                SAND_DIM, unit_h=MAN_H * F.UNIT["house"]))
    # the city wall and its gate
    for x0, x1 in ((1250, 1330), (1410, 1460)):
        sc.append(f'<rect x="{x0}" y="{GROUND - 260}" width="{x1 - x0}" '
                  f'height="260" fill="{rgb(WALL)}" stroke="{rgb(SAND_DIM)}" '
                  f'stroke-width="2"/>')
    sc.append(figure_svg_at(F.gate(), 1370, GROUND, scaled_h("gate") * 0.8,
                            SAND_DIM, unit_h=MAN_H * F.UNIT["gate"]))
    # the mound outside the gate
    m0, m1, mt = MOUND
    sc.append(f'<path d="M{m0} {GROUND} C{m0 + 60} {mt} {m1 - 60} {mt} '
              f'{m1} {GROUND}Z" fill="{rgb(HILL)}" stroke="{rgb(SAND_DIM)}" '
              f'stroke-width="2"/>')

    # -- the cast, in drawing order ----------------------------------------
    for k, x in enumerate((360, 480, 600)):
        c.add(Actor(f"rtomb{k}", static(lambda: TOMB_BODY), x, GROUND,
                    h=MAN * TOMB_F, unit_h=MAN_H, ink=SAND_DIM, shown=True,
                    label_y=-TOMB_F * 140 - 24))
        c.add(Actor(f"rstone{k}", static(lambda: TOMB_STONE),
                    x + STONE_SHUT * K * TOMB_F,
                    GROUND - STONE_Y * K * TOMB_F, h=MAN * TOMB_F,
                    unit_h=MAN_H, ink=SAND_DIM, shown=True))
    for k in range(3):
        c.add(Actor(f"grass{k}", static(F.grass),
                    480 + (k - 1) * 22 + STONE_SHUT * K * TOMB_F, GROUND,
                    h=scaled_h("grass") * 0.8,
                    unit_h=MAN_H * F.UNIT["grass"], ink=SAND))
    c.add(Actor("stand", static(F.table, span=0.35), 780, GROUND,
                h=scaled_h("table"), unit_h=MAN_H * F.UNIT["table"],
                ink=SAND, shown=True))
    top = 35 * F.UNIT["table"] * K
    c.add(Actor("stand_scroll", static(F.scroll), 780, GROUND - top,
                h=scaled_h("scroll") * 0.8, unit_h=MAN_H * F.UNIT["scroll"],
                ink=SAND, shown=True))
    for k, x in enumerate((1110, 1210)):
        c.add(Actor(f"pillar{k}", static(F.pillar), x, GROUND,
                    h=scaled_h("pillar") * 0.85,
                    unit_h=MAN_H * F.UNIT["pillar"], ink=SAND_DIM,
                    shown=True))
    c.add(Actor("seat", static(F.throne), 1160, GROUND,
                h=scaled_h("throne") * 0.9, unit_h=MAN_H * F.UNIT["throne"],
                ink=SAND, shown=True))
    c.add(Actor("pilate", person("man"), 1160, GROUND - 6, ink=SAND,
                pose={"pose": "sit"}, flip=-1, label_y=-100))
    c.add(Actor("scales", static(F.scales), 1240, GROUND,
                h=scaled_h("scales"), unit_h=MAN_H * F.UNIT["scales"],
                ink=SAND))
    for k, (kind, x) in enumerate((("priest", 830), ("man", 868),
                                   ("man", 904))):
        maker = priest_make if kind == "priest" else person("man")
        c.add(Actor(f"ruler{k}", maker, x, GROUND, ink=SAND, flip=1))
    c.add(Actor("rulers_name", static(lambda: []), 868, GROUND, h=1,
                unit_h=1, label_y=-140, shown=True))
    c.add(Actor("cross", static(F.cross), CROSS_X, mt, h=scaled_h("cross"),
                unit_h=MAN_H * F.UNIT["cross"], ink=SAND))
    for k, x in enumerate((1700, 1765)):
        c.add(Actor(f"tree{k}", static(F.tree), x, GROUND,
                    h=scaled_h("tree") * 0.6, unit_h=MAN_H * F.UNIT["tree"],
                    ink=SAND_DIM, shown=True))
    c.add(Actor("tomb", static(lambda: TOMB_BODY), GARDEN_TOMB, GROUND,
                h=MAN, unit_h=MAN_H, ink=SAND, shown=True))
    c.add(Actor("light", static(F.light), 950, GROUND, h=70, unit_h=74.5,
                ink=HL, label_y=-96))
    c.add(Actor("stone", static(lambda: TOMB_STONE),
                GARDEN_TOMB + STONE_ASIDE * K, GROUND - STONE_Y * K, h=MAN,
                unit_h=MAN_H, ink=SAND, shown=True))
    witnesses = []
    for k, kind in enumerate(("man", "woman", "man", "woman", "man")):
        a = c.add(Actor(f"witness{k}", person(kind), 2780 + k * 40,
                        1222 + k * 4, ink=SAND, flip=-1))
        a.start["scale"] = 0.45
        witnesses.append(a)
    c.add(Actor("galilee", static(lambda: []), 2560, 1236, h=1, unit_h=1,
                label_y=-24, label_fill=TEXT_DIM, label_italic=True,
                shown=True))
    c.add(Actor("witness_name", static(lambda: []), 2070, GROUND, h=1,
                unit_h=1, label_y=-146, shown=True))
    c.add(Actor("place_name", static(lambda: []), 1370, GROUND, h=1,
                unit_h=1, label_y=-scaled_h("gate") * 0.8 * 1.36 - 30,
                shown=True))

    c.refs = [(13, v) for v in range(27, 38)]
    events(c, witnesses)
    effects(c)
    return c


def events(c, witnesses):
    on = c.on
    m0, m1, mt = MOUND
    roll = (STONE_SHUT - STONE_ASIDE) * K           # card px, leftward
    turn = roll / (STONE_R * K) * 57.2958           # degrees, rolling
    # 13:27 the rulers, the light before them, the prophets read
    on((13, 27), ("label", "place_name", 4.4, 0, "Jerusalem"),
       ("show", "ruler0", 4.6, 0.6, None), ("show", "ruler1", 4.7, 0.6, None),
       ("show", "ruler2", 4.8, 0.6, None),
       ("label", "rulers_name", 5.2, 0, "rulers"),
       ("show", "light", 5.8, 0.6, None), ("move", "light", 5.8, 0.6, (0, -8)),
       ("pulse", "stand_scroll", 7.0, 0.8, None))
    for k in range(3):
        on((13, 27), ("pose", f"ruler{k}", 8.2, 0.4, {"arms": "point_r"}))
    # 13:28 no cause for death; Pilate; the cross
    on((13, 28), ("show", "scales", 0.4, 0.6, None),
       ("show", "pilate", 1.4, 0.6, None),
       ("label", "pilate", 2.0, 0, "Pilate"),
       ("show", "cross", 2.6, 0.3, None), ("grow", "cross", 2.6, 0.8, None))
    # 13:29 out through the gate to the cross; taken down; into the tomb;
    # the stone rolled to the door
    beams = 0.70 * F.bbox((F.cross(), 0))[3] * K   # where the beams cross
    on((13, 29),
       ("move", "light", 0.2, 1.0, (1370 - 950, 8)),
       ("move", "light", 1.2, 1.0, (CROSS_X - 1370, mt - GROUND - beams
                                    + 30)),
       ("move", "light", 2.8, 0.8, (0, beams - 30)),
       ("move", "light", 3.6, 1.0, (GARDEN_TOMB + STONE_SHUT * K - CROSS_X,
                                    GROUND - mt)),
       ("hide", "light", 4.0, 0.6, None),
       ("move", "stone", 4.6, 1.0, (roll, 0)),
       ("rot", "stone", 4.6, 1.0, turn))
    # 13:30 But God raised him from the dead
    on((13, 30), ("move", "stone", 0.1, 0.7, (-roll, 0)),
       ("rot", "stone", 0.1, 0.7, -turn),
       ("show", "light", 0.6, 0.4, None),
       ("move", "light", 0.6, 0.8, (0, -170)),
       ("scale", "light", 0.6, 0.8, 1.3))
    # 13:31 seen by those who came up with him from Galilee
    on((13, 31), ("label", "galilee", 1.2, 0, "Galilee"))
    for k, a in enumerate(witnesses):
        t = 1.4 + k * 0.15
        on((13, 31), ("show", a.key, t, 0.4, None),
           ("pose", a.key, t, 0.1, {"pose": "walk"}),
           ("move", a.key, t, 2.4, (1990 + k * 34 - a.start["x"],
                                    GROUND + k % 2 * 8 - a.start["y"])),
           ("scale", a.key, t, 2.4, 1 / 0.45),
           ("pose", a.key, t + 2.4, 0.2, {"pose": "stand"}))
    on((13, 31), ("label", "witness_name", 4.4, 0, "witnesses"))
    # 13:33 he raised up Jesus
    on((13, 33), ("label", "light", 3.6, 0, "Jesus"))
    # 13:34 the sure blessings of David
    on((13, 34), ("label", "rtomb1", 8.2, 0, "David"))
    # 13:36 David saw decay: his tomb cracks and grows over
    for k in range(3):
        on((13, 36), ("show", f"grass{k}", 6.6 + k * 0.2, 0.3, None),
           ("grow", f"grass{k}", 6.6 + k * 0.2, 0.8, None))
    # 13:37 he whom God raised up saw no decay
    on((13, 37), ("pulse", "stone", 1.3, 0.7, None))


def effects(c):
    g = GROUND
    # 13:35 David's psalm of the Holy One: an arc from his tomb to the light
    arc = [(480, g - 80)]
    for i in range(1, 24):
        t = i / 24
        x = 480 + (GARDEN_TOMB - 480) * t
        y = (g - 80) * (1 - t) + (g - 250) * t - 420 * 4 * t * (1 - t)
        arc.append((x, y))
    el, _L = traced_el(arc, HL, 2.2, 2.2)
    dim = ("<polyline points=\"" + " ".join(f"{_fmt(x)},{_fmt(y)}"
                                            for x, y in arc)
           + f'" fill="none" stroke="{rgb(TEXT_DIM)}" stroke-width="2.5"/>')
    c.effect((13, 35), f'<g stroke-width="3">{el}</g>', dim)
    # 13:36 the cracks across David's tomb face
    face = 480
    cracks = [[(face - 30, g - 70), (face - 18, g - 52), (face - 24, g - 36),
               (face - 10, g - 20)],
              [(face + 20, g - 74), (face + 10, g - 58), (face + 22, g - 40)],
              [(face - 2, g - 66), (face + 6, g - 50)]]
    now, after = [], []
    for k, pts in enumerate(cracks):
        el, _L = traced_el(pts, SAND, 5.6 + k * 0.3, 0.6)
        now.append(el)
        after.append("<polyline points=\""
                     + " ".join(f"{_fmt(x)},{_fmt(y)}" for x, y in pts)
                     + f'" fill="none" stroke="{rgb(SAND)}"/>')
    c.effect((13, 36), '<g stroke-width="2">' + "".join(now) + "</g>",
             '<g stroke-width="2">' + "".join(after) + "</g>")


# camera shots inside the card: (x, y, zoom)
TWO = (1180, 1200, 0.55)
SHOTS = {
    (13, 27): (900, 1240, 0.9), (13, 28): (1180, 1240, 0.9),
    (13, 29): (1660, 1240, 0.9), (13, 30): (1660, 1240, 0.9),
    (13, 31): (2000, 1220, 0.85), (13, 32): (1500, 1220, 0.62),
    (13, 33): (1880, 1180, 1.08), (13, 34): (540, 1180, 1.08),
    (13, 35): TWO, (13, 36): (520, 1260, 1.0), (13, 37): TWO,
}
LEGS = {
    (13, 33): [("to", (1880, 1180, 1.0), 1.8), ("hold", None, 4.2),
               ("to", (1880, 1180, 1.08), 3.6)],
    (13, 34): [("hold", None, 0.8), ("to", (540, 1180, 1.08), 5.4)],
    (13, 35): [("hold", None, 0.3), ("to", TWO, 2.7)],
}
DUR = {(13, 27): 4.2, (13, 28): 1.2, (13, 29): 1.6, (13, 31): 1.2,
       (13, 32): 2.0, (13, 36): 2.2, (13, 37): 1.3}
