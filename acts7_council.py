"""Jerusalem in Stephen's day (Acts 6:8-7:1, 7:52-8:3) as a scene card the
camera dives into.

A side view of the city: the council's hall at the left, cut away so its
seats show, the council in a semicircle with the high priest at its back
(the Mishnah's half circle, so that they could see one another); the law
on its stand; the Temple on its rise; the street with its houses and
people; the city wall and its north gate (where the Byzantine tradition puts
the stoning); and the open ground outside the wall. The prepared throne
(svg_figures.prepared_throne, God's presence, never God drawn) waits in the
sky over the hall, with the Chi-Rho (Jesus, never drawn as a man) on its
cloud at its right hand.

The story is acted, not captioned: Stephen among the people, the men of the
synagogue disputing and falling back, the men who are put up to it, the
crowd stirred and Stephen seized and brought in, the false witnesses, his
face shining, the high priest's question; and after the speech, the council
gnashing, the roof drawn back on the throne with the Chi-Rho standing, the
rush, the gate, a few stones, the garments at Saul's feet, Stephen kneeling
and lying still; and Saul going from house to house. The stoning is drawn
lightly (the owner's word): three stones, then three, and no more.

Card px: x from -800 to 3600, y 0 to 2200, the ground at y 1400. A man is
110 px tall. generate_acts7_svg.py flies it.
"""

import svg_figures as F
from svg_scene_card import Actor, Card, MAN_H, person, static
from svg_map_camera import fade, rgb
from svg_surface import _fmt
from generate_tabernacle import BG, SAND, SAND_DIM, TEXT, TEXT_DIM, HL
import temple as TM
from acts1314_lystra import (MAN, SKY, EARTH, PAVE, HILL, S_CARD, scaled_h,
                             figure_svg_at)

GROUND = 1400
ANCHOR = (850, 1250)            # the card point hung on Jerusalem's dot
ORIGIN = (-800, 0)
SIZE = (4400, 2200)
WALL = (42, 42, 34)
STONE_DARK = (30, 30, 26)
CUSHION = (196, 86, 82)

HX = 250                        # the hall's middle: the high priest, Stephen
HALL = (-560, 1060)             # its walls
ROOF_Y = 1000                   # the underside of its roof
FRONT = 1452                    # where Stephen stands before the council
TEMPLE_X = 1180
HOUSES = (1440, 1700)
GATE_X = 1960
OUT_X = 2460                    # where Stephen falls, outside the gate
SAUL_X = 2720

# the prepared throne over the hall: its cloud's base, and its size
TH_Y = 880
TH_H = 240.0                    # card px for the figure's 160 units
TH_UNITS = 160.0
TH_K = TH_H / TH_UNITS
CHIRHO_UNITS = F.bbox((F.chi_rho(), 0))[3]
CHIRHO_H = 0.9 * CHIRHO_UNITS * TH_K
RX, RY = F.PREPARED_THRONE_RIGHT
GX, GY = F.PREPARED_THRONE_GLORY
TO_OUT = OUT_X - HX             # how far Stephen is taken, and the vision with him


def member_spots():
    """The council's seats in a half circle, back to front: (x, y)."""
    import math
    out = []
    for k in range(12):
        a = math.radians(-78 + k * (156 / 11))
        out.append((HX + 560 * math.sin(a), GROUND - 96 * math.cos(a) + 6))
    out.sort(key=lambda p: p[1])
    return out


def slab(w, right=False):
    """A roof slab w card px long, 40 thick, its origin at the end that stays
    (the left end of the left slab, the right end of the right one)."""
    pts = ([(-w, 0), (0, 0), (0, 40), (-w, 40)] if right
           else [(0, 0), (w, 0), (w, 40), (0, 40)])
    return [("fill", pts, "stone"),
            ("line", [(p[0], 20) for p in pts[:2]], "rule")]


def garments():
    """The witnesses' cloaks, laid in a heap."""
    return [("fill", F.smooth([(-26, 0), (-30, 8), (-12, 16), (10, 14),
                               (28, 6), (24, 0)], n=3), "cloth"),
            ("fill", F.smooth([(-16, 10), (-8, 22), (12, 20), (18, 12)], n=3),
             "mantle"),
            ("line", [(-18, 6), (16, 9)], "rule")]


def build(town_xy):
    c = Card("jer7", town_xy, ANCHOR, SIZE, S_CARD, page=EARTH, sky=SKY,
             ground_y=GROUND, origin=ORIGIN)
    c.share_bodies = True
    c.names_at = (0.40, 0.48)
    X0, X1 = ORIGIN[0], ORIGIN[0] + SIZE[0]
    sc = c.scenery
    g = GROUND

    # -- scenery ----------------------------------------------------------
    hills = [(X0, 1210), (-300, 1170), (500, 1200), (1300, 1150),
             (2000, 1190), (2600, 1140), (X1, 1180), (X1, g), (X0, g)]
    sc.append('<polygon points="' + " ".join(f"{x},{y}" for x, y in hills)
              + f'" fill="{rgb(HILL)}" stroke="{rgb(SAND_DIM)}" '
              f'stroke-width="2"/>')
    sc.append(f'<rect x="{X0}" y="{g}" width="{X1 - X0}" '
              f'height="{SIZE[1] - g}" fill="{rgb(EARTH)}"/>')
    sc.append(f'<rect x="{HALL[1]}" y="{g}" width="{GATE_X - HALL[1]}" '
              f'height="44" fill="{rgb(PAVE)}"/>')
    sc.append(f'<line x1="{X0}" y1="{g}" x2="{X1}" y2="{g}" '
              f'stroke="{rgb(SAND_DIM)}" stroke-width="2"/>')
    # the Temple on its rise, behind the street
    sc.append(f'<path d="M{TEMPLE_X - 230} {g} C{TEMPLE_X - 160} {g - 90} '
              f'{TEMPLE_X + 160} {g - 90} {TEMPLE_X + 230} {g}Z" '
              f'fill="{rgb(HILL)}" stroke="{rgb(SAND_DIM)}" stroke-width="2"/>')
    # the houses of the street
    for k, x in enumerate(HOUSES):
        sc.append(figure_svg_at(F.house(), x, g, scaled_h("house") * (0.82 if k
                                                                      else 0.9),
                                SAND_DIM, unit_h=MAN_H * F.UNIT["house"]))
    # the hall: its back wall, its floor, its piers
    x0, x1 = HALL
    sc.append(f'<rect x="{x0}" y="{ROOF_Y}" width="{x1 - x0}" '
              f'height="{g - 110 - ROOF_Y}" fill="{rgb(STONE_DARK)}" '
              f'stroke="{rgb(SAND_DIM)}" stroke-width="2"/>')
    for k in range(1, 5):
        y = ROOF_Y + k * 58
        sc.append(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" '
                  f'stroke="{rgb(WALL)}" stroke-width="2"/>')
    sc.append(f'<rect x="{x0}" y="{g - 110}" width="{x1 - x0}" height="170" '
              f'fill="{rgb(PAVE)}" stroke="{rgb(SAND_DIM)}" stroke-width="2"/>')
    for px in (x0, x1 - 60):
        sc.append(f'<rect x="{px}" y="{ROOF_Y}" width="60" '
                  f'height="{g + 60 - ROOF_Y}" fill="{rgb(WALL)}" '
                  f'stroke="{rgb(SAND_DIM)}" stroke-width="2"/>')
    # the half circle of seats, a low stone bench behind the council
    import math
    bench = []
    for k in range(25):
        a = math.radians(-82 + k * (164 / 24))
        bench.append((HX + 580 * math.sin(a), g - 100 * math.cos(a) - 30))
    sc.append('<polyline points="'
              + " ".join(f"{_fmt(x)},{_fmt(y)}" for x, y in bench)
              + f'" fill="none" stroke="{rgb(WALL)}" stroke-width="34" '
              f'stroke-linecap="round"/>')
    sc.append('<polyline points="'
              + " ".join(f"{_fmt(x)},{_fmt(y - 17)}" for x, y in bench)
              + f'" fill="none" stroke="{rgb(SAND_DIM)}" stroke-width="2"/>')
    # the city wall either side of the north gate
    for a, b in ((GATE_X - 150, GATE_X - 90), (GATE_X + 90, GATE_X + 150)):
        sc.append(f'<rect x="{a}" y="{g - 280}" width="{b - a}" height="280" '
                  f'fill="{rgb(WALL)}" stroke="{rgb(SAND_DIM)}" '
                  f'stroke-width="2"/>')
    sc.append(figure_svg_at(F.gate(), GATE_X, g, scaled_h("gate") * 0.85,
                            SAND_DIM, unit_h=MAN_H * F.UNIT["gate"]))

    # -- the cast, back to front -------------------------------------------
    c.add(Actor("roof_l", static(slab, (x1 - x0) / 2), x0, ROOF_Y, h=1,
                unit_h=1, ink=SAND_DIM, shown=True))
    c.add(Actor("roof_r", static(slab, (x1 - x0) / 2, True), x1, ROOF_Y, h=1,
                unit_h=1, ink=SAND_DIM, shown=True))
    c.add(Actor("throne", static(F.prepared_throne, cushion=False), HX, TH_Y,
                h=TH_H, unit_h=TH_UNITS, ink=HL))
    c.add(Actor("cushion", static(F.prepared_throne_cushion), HX, TH_Y,
                h=TH_H, unit_h=TH_UNITS, ink=CUSHION))
    c.add(Actor("chirho", static(F.chi_rho), HX + RX * TH_K, TH_Y - RY * TH_K,
                h=CHIRHO_H, unit_h=CHIRHO_UNITS, ink=HL,
                label_y=-(CHIRHO_H + 26)))
    # the Temple: the house as temple.py has it (Herod's stood on its plan)
    c.add(Actor("temple", static(F.temple_house), TEMPLE_X, g - 84, h=170,
                unit_h=TM.HOUSE_HEIGHT, ink=SAND, shown=True))
    c.add(Actor("stand", static(F.table, span=0.35), x0 + 150, g - 40,
                h=scaled_h("table"), unit_h=MAN_H * F.UNIT["table"], ink=SAND,
                shown=True))
    top = 35 * F.UNIT["table"] * MAN / MAN_H
    c.add(Actor("law", static(F.scroll), x0 + 150, g - 40 - top,
                h=scaled_h("scroll") * 0.8, unit_h=MAN_H * F.UNIT["scroll"],
                ink=SAND, shown=True))
    c.add(Actor("hp_seat", static(F.throne), HX, g - 100,
                h=scaled_h("throne") * 0.8, unit_h=MAN_H * F.UNIT["throne"],
                ink=SAND_DIM, shown=True))
    c.add(Actor("high_priest", person("priest"), HX, g - 100 + 6, ink=SAND,
                pose={"pose": "sit"}, shown=True, label_y=-118))
    members = []
    for k, (x, y) in enumerate(member_spots()):
        members.append(c.add(Actor(f"member{k}", person("man"), x, y,
                                   ink=SAND, pose={"pose": "sit"},
                                   flip=1 if x < HX else -1, shown=True)))
    c.add(Actor("council_name", static(lambda: []), HX + 330, g - 60, h=1,
                unit_h=1, label_y=-140, shown=True))
    # the street's people
    crowd = []
    kinds = ["man", "woman", "man", "child", "woman", "man", "man", "woman",
             "man", "child"]
    for k, kind in enumerate(kinds):
        x = HOUSES[0] - 220 + k * 52 + (k % 3) * 8
        crowd.append(c.add(Actor(f"crowd{k}", person(kind), x,
                                 g + 10 + (k % 3) * 12, ink=SAND,
                                 flip=-1 if k % 3 else 1, shown=True)))
    disputers = []
    for k in range(4):
        disputers.append(c.add(Actor(f"disputer{k}", person("man"),
                                     GATE_X - 60 + k * 40, g + 14 + (k % 2) * 10,
                                     ink=SAND, flip=-1)))
    put_up = [c.add(Actor(f"putup{k}", person("man"), GATE_X + 40 + k * 40,
                          g + 18, ink=SAND, flip=-1)) for k in range(2)]
    seizers = [c.add(Actor(f"seizer{k}", person("man", staff=k == 1),
                           GATE_X - 160 + k * 46, g + 12 + k % 2 * 8,
                           ink=SAND, flip=-1)) for k in range(3)]
    witnesses = [c.add(Actor(f"witness{k}", person("man"), HX - 210 + k * 50,
                             FRONT + 4 + k * 6, ink=SAND, flip=1))
                 for k in range(2)]
    c.add(Actor("stephen", person("man"), HOUSES[0] + 30, g + 22, ink=TEXT,
                flip=-1, label_y=-(MAN + 30)))
    c.add(Actor("saul", person("man"), SAUL_X, g + 20, ink=SAND, flip=-1,
                label_y=-(MAN + 26)))
    c.add(Actor("garments", static(garments), SAUL_X - 48, g + 24, h=MAN,
                unit_h=MAN_H, ink=SAND))
    for k in range(6):
        c.add(Actor(f"stone{k}", static(F.stone), OUT_X - 230 + (k % 3) * 40,
                    g - 40 - (k % 2) * 30, h=scaled_h("stone") * 0.35,
                    unit_h=MAN_H * F.UNIT["stone"], ink=SAND))
    # 8:3, the people Saul drags off: two at each house
    taken = []
    for j, hx in enumerate(HOUSES):
        for k, kind in enumerate(("man", "woman")):
            taken.append(c.add(Actor(f"taken{j}{k}", person(kind),
                                     hx - 20 + k * 36, g + 16 + k * 8,
                                     ink=SAND, flip=-1)))

    c.refs = ([(6, v) for v in range(8, 16)] + [(7, v) for v in range(1, 61)]
              + [(8, v) for v in (1, 2, 3)])
    events(c, crowd, disputers, put_up, seizers, witnesses, members, taken)
    effects(c)
    return c


def events(c, crowd, disputers, put_up, seizers, witnesses, members, taken):
    on = c.on
    g = GROUND
    st_x = HOUSES[0] + 30
    # 6:8 Stephen, full of faith and power, among the people
    on((6, 8), ("show", "stephen", 1.0, 0.6, None),
       ("label", "stephen", 1.4, 0, "Stephen"),
       ("pose", "stephen", 3.0, 0.3, {"arms": "open"}))
    # 6:9 the men of the synagogue come in from the gate and dispute (the
    # camera is away over the map for most of the verse)
    for k, a in enumerate(disputers):
        on((6, 9), ("show", a.key, 3.6 + k * 0.15, 0.4, None),
           ("pose", a.key, 3.6, 0.1, {"pose": "walk"}),
           ("move", a.key, 3.6 + k * 0.15, 2.2,
            (st_x + 110 + k * 46 - a.start["x"], 0)),
           ("pose", a.key, 5.9 + k * 0.15, 0.2, {"pose": "stand"}),
           ("pose", a.key, 9.4, 0.3, {"arms": "point_l"}))
    # 6:10 they could not withstand the wisdom and the Spirit: they fall back
    for k, a in enumerate(disputers):
        on((6, 10), ("pose", a.key, 1.8, 0.3, {"arms": "down"}),
           ("move", a.key, 2.0 + k * 0.1, 0.8, (40 + k * 6, 0)))
    on((6, 10), ("pose", "stephen", 0.2, 0.3, {"arms": "open"}))
    # 6:11 men put up to say they heard blasphemy
    for k, a in enumerate(put_up):
        on((6, 11), ("show", a.key, 0.8 + k * 0.2, 0.4, None),
           ("pose", a.key, 0.8, 0.1, {"pose": "walk"}),
           ("move", a.key, 0.8 + k * 0.2, 1.8, (-(260 - k * 30), 0)),
           ("pose", a.key, 2.6 + k * 0.2, 0.2, {"pose": "stand"}),
           ("pose", a.key, 3.6, 0.3, {"arms": "point_l"}))
    # 6:12 the people stirred up; the elders and scribes; seized and brought
    # in to the council
    for k, a in enumerate(crowd):
        on((6, 12), ("pose", a.key, 0.8 + k * 0.05, 0.3, {"arms": "up"}))
    for k, a in enumerate(seizers):
        on((6, 12), ("show", a.key, 2.4 + k * 0.2, 0.4, None),
           ("pose", a.key, 2.4, 0.1, {"pose": "walk"}),
           ("move", a.key, 2.4 + k * 0.2, 1.8,
            (st_x + 60 + k * 40 - a.start["x"], 0)))
    lead = (HX - st_x, FRONT - (g + 22))
    on((6, 12), ("pose", "stephen", 4.2, 0.2, {"arms": "down", "pose": "walk"}),
       ("move", "stephen", 4.6, 2.3, lead),
       ("pose", "stephen", 6.9, 0.2, {"pose": "stand"}),
       ("label", "council_name", 6.8, 0, "council"))
    for k, a in enumerate(seizers):
        on((6, 12), ("move", a.key, 4.6, 2.3,
                     (HX + 120 + k * 48 - (st_x + 60 + k * 40), FRONT + 6 - g)),
           ("pose", a.key, 6.9, 0.2, {"pose": "stand"}),
           ("flip", a.key, 6.9, 0.2, -1))
    for a in crowd:
        on((6, 12), ("pose", a.key, 4.2, 0.3, {"arms": "down"}))
    # 6:13 the false witnesses: this holy place, and the law
    for k, a in enumerate(witnesses):
        on((6, 13), ("show", a.key, 0.8 + k * 0.2, 0.5, None),
           ("pose", a.key, 1.8, 0.3, {"arms": "point_r"}))
    on((6, 13), ("pulse", "temple", 5.0, 0.8, None),
       ("pulse", "law", 6.2, 0.8, None))
    # 6:14 this Jesus of Nazareth will destroy this place, and change the
    # customs Moses delivered
    on((6, 14), ("pulse", "temple", 3.8, 0.8, None),
       ("pulse", "law", 6.4, 0.8, None))
    for a in witnesses:
        on((6, 14), ("pose", a.key, 0.2, 0.3, {"arms": "down"}))
    # 6:15 his face like an angel's (the light is an effect)
    # 7:1 the high priest: Are these things so?
    on((7, 1), ("label", "high_priest", 0.3, 0, "high priest"),
       ("pulse", "high_priest", 0.6, 0.8, None))
    # while the camera is over the map (7:2), the street empties
    for a in crowd + disputers + put_up:
        on((7, 2), ("hide", a.key, 3.4, 0.2, None))
    # 7:53 the law, received and not kept
    on((7, 53), ("pulse", "law", 1.2, 0.8, None))
    # 7:54 cut to the heart; they gnash at him
    for k, a in enumerate(members):
        on((7, 54), ("pose", a.key, 2.2 + (k % 4) * 0.1, 0.3,
                     {"arms": "point_r" if a.start["x"] < HX else "point_l"}))
    # 7:55 he looks up; the roof is drawn back on the glory of God, and Jesus
    # standing at God's right hand
    on((7, 55), ("pose", "stephen", 1.2, 0.4, {"arms": "up"}),
       ("move", "roof_l", 3.0, 1.4, (-560, 0)), ("hide", "roof_l", 3.2, 1.2,
                                                None),
       ("move", "roof_r", 3.0, 1.4, (560, 0)), ("hide", "roof_r", 3.2, 1.2,
                                               None),
       ("show", "throne", 4.6, 1.0, None), ("show", "cushion", 4.6, 1.0, None),
       ("show", "chirho", 6.8, 0.8, None),
       ("label", "chirho", 8.0, 0, "Jesus"))
    for a in members:
        on((7, 55), ("pose", a.key, 0.4, 0.3, {"arms": "down"}))
    # 7:56 Behold, I see the heavens opened
    on((7, 56), ("pose", "stephen", 0.3, 0.3, {"arms": "open"}))
    # 7:57 they cry out, stop their ears, and rush at him
    rushers = members[-6:]
    for k, a in enumerate(members):
        on((7, 57), ("pose", a.key, 1.4 + (k % 3) * 0.1, 0.3, {"arms": "up"}))
    for k, a in enumerate(rushers):
        on((7, 57), ("pose", a.key, 3.0, 0.2, {"pose": "walk", "arms": "down"}),
           ("move", a.key, 3.0 + k * 0.08, 1.6,
            ((HX - 170 + k * 64) - a.start["x"], FRONT - 10 - a.start["y"])))
    # 7:58 out of the city: Stephen, the vision with him, and the crowd; a
    # few stones; the garments laid at the feet of a young man named Saul
    out_dx = (TO_OUT, (g + 30) - FRONT)
    on((7, 58), ("pose", "stephen", 0.2, 0.2, {"pose": "walk", "arms": "down"}),
       ("move", "stephen", 0.3, 2.4, out_dx),
       ("pose", "stephen", 2.7, 0.2, {"pose": "stand"}),
       ("move", "throne", 0.3, 2.4, (TO_OUT, 0)),
       ("move", "cushion", 0.3, 2.4, (TO_OUT, 0)),
       ("move", "chirho", 0.3, 2.4, (TO_OUT, 0)))
    goers = rushers + witnesses + seizers
    for k, a in enumerate(goers):
        sx, sy = a.start["x"], a.start["y"]
        if a in rushers:
            sx, sy = HX - 170 + rushers.index(a) * 64, FRONT - 10
        elif a in seizers:
            sx, sy = HX + 120 + seizers.index(a) * 48, FRONT + 6
        tx = OUT_X - 380 + (k % 6) * 44
        on((7, 58), ("pose", a.key, 0.4, 0.2, {"pose": "walk",
                                               "arms": "down"}),
           ("flip", a.key, 0.4, 0.2, 1),
           ("move", a.key, 0.4 + (k % 5) * 0.06, 2.4,
            (tx - sx, g + 6 + (k % 3) * 12 - sy)),
           ("pose", a.key, 2.9, 0.2, {"pose": "stand"}))
    for k in range(3):
        on((7, 58), ("show", f"stone{k}", 3.0 + k * 0.2, 0.1, None),
           ("move", f"stone{k}", 3.0 + k * 0.2, 0.5,
            (190 + (2 - k) * 6, g + 40 - (g - 40)
             + k * 6)))
    on((7, 58), ("show", "saul", 3.8, 0.5, None),
       ("show", "garments", 4.6, 0.5, None),
       ("label", "saul", 5.6, 0, "Saul"))
    for a in witnesses:
        on((7, 58), ("pose", a.key, 4.2, 0.3, {"arms": "hold_r"}),
           ("pose", a.key, 5.0, 0.3, {"arms": "down"}))
    # 7:59 They stoned Stephen as he called out, Lord Jesus, receive my spirit
    for k in range(3, 6):
        on((7, 59), ("show", f"stone{k}", 0.3 + (k - 3) * 0.2, 0.1, None),
           ("move", f"stone{k}", 0.3 + (k - 3) * 0.2, 0.5,
            (190 + (k - 3) * 10, 70 + (k - 3) * 6)))
    on((7, 59), ("pose", "stephen", 2.0, 0.4, {"arms": "up"}))
    # 7:60 he kneels, cries out, and falls asleep
    on((7, 60), ("pose", "stephen", 0.3, 0.4, {"pose": "kneel",
                                                "arms": "open"}),
       ("rot", "stephen", 6.8, 0.8, -90), ("ink", "stephen", 6.8, 0.8,
                                          SAND))
    # 8:1 Saul consenting; the vision goes with the day
    on((8, 1), ("pulse", "saul", 0.6, 0.8, None),
       ("hide", "throne", 1.8, 1.0, None), ("hide", "cushion", 1.8, 1.0, None),
       ("hide", "chirho", 1.8, 1.0, None))
    # 8:3 Saul goes into the houses and drags men and women off to prison
    on((8, 3), ("move", "saul", 0.1, 0.1,
                (HOUSES[1] + 140 - SAUL_X, 0)),
       ("pose", "saul", 2.0, 0.1, {"pose": "walk"}),
       ("move", "saul", 2.0, 1.0, (-120, 0)),
       ("pose", "saul", 3.0, 0.2, {"pose": "stand", "arms": "point_l"}))
    for k, a in enumerate(taken[2:] + taken[:2]):
        house = 1 if k < 2 else 0
        t = 3.0 + (k % 2) * 0.15 + (0 if house else 0.9)
        on((8, 3), ("show", a.key, t, 0.4, None),
           ("pose", a.key, t + 0.4, 0.1, {"pose": "walk"}),
           ("move", a.key, t + 0.4, 2.0, (-480, 0)),
           ("hide", a.key, t + 1.8, 0.5, None))
    on((8, 3), ("pose", "saul", 4.4, 0.2, {"pose": "walk", "arms": "down"}),
       ("move", "saul", 4.4, 1.8, (-280, 0)),
       ("pose", "saul", 6.2, 0.2, {"pose": "stand"}))


def effects(c):
    g = GROUND
    # 6:8 wonders and signs: rings of light about him, twice
    st = (HOUSES[0] + 30, g + 22 - MAN * 0.55)
    rings = "".join(
        f'<circle cx="{_fmt(st[0])}" cy="{_fmt(st[1])}" r="40" fill="none" '
        f'stroke="{rgb(HL)}" stroke-width="3" opacity="0">'
        f'<animate attributeName="r" values="40;130" begin="{t}s" dur="1.2s" '
        f'fill="freeze"/><animate attributeName="opacity" values="0;0.9;0" '
        f'begin="{t}s" dur="1.2s" fill="freeze"/></circle>'
        for t in (3.4, 4.2))
    c.effect((6, 8), rings)
    # 6:15 his face like the face of an angel: a light about his head, which
    # stays while he speaks
    head = (HX, FRONT - MAN * 0.9)
    glow_d = (f'<radialGradient id="face7"><stop offset="0" '
              f'stop-color="{rgb(HL)}" stop-opacity="0.75"/><stop offset="1" '
              f'stop-color="{rgb(HL)}" stop-opacity="0"/></radialGradient>')
    face = (f'<circle cx="{_fmt(head[0])}" cy="{_fmt(head[1])}" r="44" '
            f'fill="url(#face7)"')
    c.effect((6, 15), f'<defs>{glow_d}</defs>{face} opacity="0">'
                      f'{fade(4.0, 1.2)}</circle>')
    for r in [(7, 1)] + [(7, v) for v in range(52, 58)]:
        c.effect(r, f'<defs>{glow_d}</defs>{face}/>')
    # it goes as he is taken out (7:58)
    c.effect((7, 58), f'<defs>{glow_d}</defs>{face}>'
                      f'{fade(0.0, 0.4, out=True)}</circle>')
    # the throne's glory: a soft light behind it from 7:55, which goes out
    # with him at 7:58 and fades with the vision at 8:1
    cx, cy = HX + GX * TH_K, TH_Y - GY * TH_K
    gd = (f'<radialGradient id="glory7"><stop offset="0" '
          f'stop-color="rgb(255,236,160)" stop-opacity="0.55"/><stop '
          f'offset="1" stop-color="rgb(255,236,160)" stop-opacity="0"/>'
          f'</radialGradient>')
    glow = (f'<circle cx="{_fmt(cx)}" cy="{_fmt(cy)}" r="300" '
            f'fill="url(#glory7)"')
    c.effect((7, 55), f'<defs>{gd}</defs>{glow} opacity="0">'
                      f'{fade(4.4, 1.4)}</circle>', under=True)
    c.effect((7, 56), f'<defs>{gd}</defs>{glow}/>', under=True)
    c.effect((7, 57), f'<defs>{gd}</defs>{glow}/>', under=True)
    moved = (f'<circle cx="{_fmt(cx + TO_OUT)}" cy="{_fmt(cy)}" r="300" '
             f'fill="url(#glory7)"')
    c.effect((7, 58), f'<defs>{gd}</defs><g>{glow}/>'
                      f'<animateTransform attributeName="transform" '
                      f'type="translate" values="0 0;{TO_OUT} 0" begin="0.3s" '
                      f'dur="2.4s" fill="freeze"/></g>', under=True)
    for r in ((7, 59), (7, 60)):
        c.effect(r, f'<defs>{gd}</defs>{moved}/>', under=True)
    c.effect((8, 1), f'<defs>{gd}</defs>{moved}>'
                     f'{fade(1.8, 1.0, out=True)}</circle>', under=True)


# camera shots inside the card: (x, y, zoom)
STREET = (HOUSES[0] + 40, 1250, 0.8)
HALL_SHOT = (HX + 180, 1240, 0.6)
GLORY = (HX + 60, 1010, 0.5)
OUTSIDE = (OUT_X + 60, 1050, 0.5)
SHOTS = {
    (6, 8): STREET, (6, 9): (HOUSES[0] + 120, 1250, 0.8),
    (6, 10): (HOUSES[0] + 120, 1250, 0.8), (6, 11): (HOUSES[0] + 160, 1250, 0.8),
    (6, 12): HALL_SHOT, (6, 13): (HX + 420, 1230, 0.62),
    (6, 14): (HX + 420, 1230, 0.62), (6, 15): (HX, 1330, 1.15),
    (7, 1): (HX, 1300, 0.9),
    (7, 52): HALL_SHOT, (7, 53): HALL_SHOT, (7, 54): HALL_SHOT,
    (7, 55): GLORY, (7, 56): GLORY, (7, 57): (HX + 60, 1040, 0.5),
    (7, 58): OUTSIDE, (7, 59): OUTSIDE, (7, 60): (OUT_X, 1150, 0.62),
    (8, 3): (HOUSES[0] + 60, 1260, 0.72),
}
# shots on the way: (verse) -> [(kind, (x, y, z) or None, seconds)]
LEGS = {
    (6, 12): [("hold", None, 4.6), ("to", HALL_SHOT, 2.6)],
    (6, 15): [("hold", None, 2.0), ("to", (HX, 1330, 1.15), 2.0)],
    (7, 55): [("hold", None, 2.4), ("to", GLORY, 2.2)],
    (7, 58): [("hold", None, 0.2), ("to", (1500, 1100, 0.42), 1.2),
              ("to", OUTSIDE, 1.4)],
    (7, 60): [("hold", None, 5.2), ("to", (OUT_X, 1150, 0.62), 1.6)],
}
DUR = {(6, 8): 1.0, (6, 11): 1.0, (6, 13): 1.2, (7, 1): 1.0, (7, 53): 0.0, (7, 54): 0.0,
       (7, 56): 0.0, (7, 57): 1.2, (7, 59): 0.0}
