"""Leviticus 1:1-17, the burnt offering, on the workbench (section s1).

The reference section: every other section is built the same way, on the
engine's helpers (leviticus17_bench's SECTION CONTRACT). It starts on an
empty workshop (the plan strip, an empty bench, the dock's burnt column of
bars under five veiled tabs) and leaves the s1|s2 boundary: the places it
named (Tent of Meeting, door, north, altar, place of the ashes), the altar
set (the altar, its wood, its fire), and the burnt column lit in the dock
with the burnt tab active.

Moves (QC's budget): no camera; chip flights at 1:5, 1:9 and 1:17; bench
moves at 1:8, 1:12, 1:15 and 1:17; a short token walk at 1:16; the filing
glide at 1:17.
"""

import svg_figures as F
import leviticus17_bench as B
import leviticus17_dock as D
import leviticus17_parts as P
import leviticus17_art as ART
from leviticus17_bench import El, add, cue, at, fit, pulse_el, traced_el, glide, rect_pts
from leviticus17_parts import S, BLOOD

STUB = False
VERSES = [(1, v) for v in range(1, 18)]


def build():
    E = B.ELS
    road = S["road_y"]

    # ---- 1:1  Moses, the Tent of Meeting -------------------------------
    t = cue(1, 1, "Moses")
    mx = S["outside"][0]
    add(El("s1.moses", "strip",
           P.token(F.man(staff=True), mx, road, 36) + B.halo_text("Moses", mx, road - 48, 13),
           z=30, texts=[(B.tbox("Moses", mx, road - 48, 13), 13, "strip chip")]))
    E["s1.moses"].ev("in", t, 0.6)
    P.place("tent", cue(1, 1, "Tent of Meeting"))

    # ---- 1:2  anyone; the herd and the flock into the pen ---------------
    t = cue(1, 2, "anyone")
    D.light("burnt.by", t)
    E["s1.moses"].ev("out", t + 0.85, 0.6)
    ox = P.Beast("bull", P.OX_X, P.PEN_G, P.OX_K)
    ram1_x, goat1_x = 85, 245
    P.figure_el("pen.ox", F.ox(), P.OX_X, P.PEN_G, P.OX_K, cue(1, 2, "herd"))
    t = cue(1, 2, "flock")
    d = fit(t, 0.5)
    P.figure_el("pen.ram1", F.sheep(ram=True), ram1_x, P.PEN_BACK_G, P.BACK_K, t, z=18, dur=d,
                group="flock")
    P.figure_el("pen.goat1", F.goat(), goat1_x, P.PEN_BACK_G, P.BACK_K, t, z=18, dur=d,
                group="flock")

    # ---- 1:3  burnt offering; the herd; male; the door ------------------
    D.switch("burnt", cue(1, 3, "burnt offering"))          # names the tab and its header
    t = cue(1, 3, "herd")
    E["pen.ram1"].ev("out", t, 0.6, group="herd")
    E["pen.goat1"].ev("out", t, 0.6, group="herd")
    t2 = t + 0.32
    ox_line = F.outline(F.ox(), P.OX_X, P.PEN_G, P.OX_K)
    D.light("burnt.thing:bull", t2, link=[("bench", ox_line, True)], group="icon.bull")
    case_herd = D.case_outline(["burnt.thing:bull"], t2 + 0.6)
    P.bench_chip("pen.male1", "male", P.OX_X + 20, P.PEN_G + 21, cue(1, 3, "male"),
                 out=cue(1, 6, "flay"))
    t = cue(1, 3, "door")
    P.place("door", t, group="door")
    pulse_el("pen.ox.door", "bench", ox_line, t, group="door")

    # ---- 1:4  the hand on the head --------------------------------------
    reach = F.side_person(arms="reach")
    hpx, _hpy = ART.hand_pt(reach)
    hx, _hy = ox.anchor["head"]
    man_x = hx + hpx * P.OX_K + 15
    P.figure_el("pen.offerer", reach, man_x, P.PEN_G, P.OX_K, cue(1, 4, "hand"), flip=-1, z=22,
                dur=0.5)
    pulse_el("pen.head.p", "bench", ox.outline("head")[0][0], cue(1, 4, "head"))

    # ---- 1:5  Aaron's sons; the ring; the altar -------------------------
    E["pen.offerer"].ev("out", cue(1, 5, "kill"), 0.5)
    a = S["altar"]
    P.priests_el("s1.priests", [a[0] - 14, a[0] + 8], cue(1, 5, "Aaron's"))
    traced_el("s1.ring", "strip", rect_pts(a[0] - 4, a[1] - 4, a[2] + 4, a[3] + 4), BLOOD, 2.4,
              cue(1, 5, "around"), 1.2, z=35, closed=True)
    t_alt = cue(1, 5, "altar")
    P.body_in(t_alt)
    D.fly("around the altar", (a[0] - 12, a[1] - 13), "burnt.blood:around the altar", t_alt + 0.32)

    # ---- 1:6  flay; pieces ----------------------------------------------
    t = cue(1, 6, "flay")
    E["pen.ox"].ev("out", t, 0.6, group="flay")
    P.cutaway(ox, "bull", t, group="flay")
    pulse_el("cut.bull.skin.p", "bench", ox.outline("skin")[0][0], t + 0.05, group="flay")
    band, bx = P.CHIP_BAND_Y, P.CHIP_BAND_X
    ox_chip = {"skin": (bx[0], band), "pieces": (bx[1], band), "head": (bx[2], band),
               "fat": (bx[0], band), "innards": (bx[0], band), "legs": (bx[1], band),
               "water": (bx[2], band)}
    P.bench_chip("chip.bull.skin", "skin", *ox_chip["skin"], t + 0.05, lead=ox.anchor["skin"],
                 out=at(1, 7, 0.3), group="flay")
    t = cue(1, 6, "pieces")
    for i, ln in enumerate(ox.lines("pieces")):
        traced_el(f"cut.bull.pieces.{i}", "bench", ln, B.TEXT, 2.4, t + i * 0.03, 0.38, z=26)
    P.bench_chip("chip.bull.pieces", "pieces", *ox_chip["pieces"], t, lead=ox.anchor["pieces"],
                 dur=fit(t, 0.5), out=cue(1, 8, "wood"))

    # ---- 1:7  fire; wood --------------------------------------------------
    t = cue(1, 7, "fire")
    P.fire_in(t)
    P.bench_chip("chip.fire", "fire", P.WOOD_X[0] - 30, P.A_TOP - 70, t + 0.1,
                 lead=(P.FIRE_XS[0] - 4, P.A_TOP - 22), group="fire")
    P.place("altar", cue(1, 7, "altar"))
    t = cue(1, 7, "wood")
    P.wood_in(t)
    P.bench_chip("chip.wood", "wood", P.WOOD_X[0] - 30, P.A_TOP - 18, t + 0.25,
                 lead=(P.WOOD_X[0] + 4, P.A_TOP - 8), group="wood")

    # ---- 1:8  pieces, head, fat; onto the wood ----------------------------
    for word in ("pieces", "head", "fat"):
        t = cue(1, 8, word)
        P.part_pulse(ox, "bull", word, t, tag="8")
        if word != "pieces":                    # its chip is 1:6's
            P.bench_chip(f"chip.bull.{word}", word, *ox_chip[word], t, lead=ox.anchor[word],
                         out=cue(1, 8, "wood"), group=f"pbull{word}")
    P.to_wood(ox, "bull", {"pieces": ox.anchor["meat"], "head": ox.anchor["head"],
                           "fat": ox.anchor["fat"]}, cue(1, 8, "wood"), ["pieces", "head", "fat"])

    # ---- 1:9  innards, legs, water; burn; the whole; no one; case clear ---
    for word in ("innards", "legs"):
        t = cue(1, 9, word)
        P.part_pulse(ox, "bull", word, t, tag="9")
        P.bench_chip(f"chip.bull.{word}", word, *ox_chip[word], t, lead=ox.anchor[word],
                     out=cue(1, 9, "burn"), group=f"pbull{word}")
    t = cue(1, 9, "water")
    P.water(ox, "bull", t)
    lx, ly = ox.anchor["legs"]
    P.bench_chip("chip.bull.water", "water", *ox_chip["water"], t + 0.1, lead=(lx + 30, ly),
                 out=cue(1, 9, "burn"), group="water.bull.0")
    t = cue(1, 9, "burn")
    P.burn(ox, "bull", t)
    land = D.fly("the whole", (P.FIRE_XS[1] - 4, P.A_TOP - 96), "burnt.burns:the whole", t + 0.8)
    D.light("burnt.eaten:no one", land + 0.4)
    P.case_clear(cue(1, 9, "pleasant aroma"))

    # ---- 1:10  the flock: ram, goat; male ---------------------------------
    ram = P.Beast("ram", P.RAM_X, P.PEN_G, P.RAM_K)
    goat2_x = 262
    P.figure_el("pen.ram2", F.sheep(ram=True), P.RAM_X, P.PEN_G, P.RAM_K, cue(1, 10, "sheep"))
    P.figure_el("pen.goat2", F.goat(), goat2_x, P.PEN_BACK_G, P.BACK_K, cue(1, 10, "goats"), z=18)
    t = cue(1, 10, "male")
    P.bench_chip("pen.male2", "male", P.RAM_X + 10, P.PEN_G + 21, t, out=cue(1, 12, "pieces"))
    t2 = t + 0.32
    ram_line = F.outline(F.sheep(ram=True), P.RAM_X, P.PEN_G, P.RAM_K)
    goat_line = F.outline(F.goat(), goat2_x, P.PEN_BACK_G, P.BACK_K)
    D.light("burnt.thing:male sheep", t2, link=[("bench", ram_line, True)], group="icon.flock")
    D.light("burnt.thing:male goat", t2, link=[("bench", goat_line, True)], group="icon.flock")
    case_herd.ev("out", t2 + 0.5, 0.35)
    case_flock = D.case_outline(["burnt.thing:male sheep", "burnt.thing:male goat"], t2 + 0.5)

    # ---- 1:11  north; around ------------------------------------------------
    t = cue(1, 11, "north")
    P.place("north", t, group="north")
    pulse_el("pen.ram2.north", "bench", ram_line, t, group="north")
    t = cue(1, 11, "around")
    B.steady_el("s1.ring.steady", "strip", rect_pts(a[0] - 1, a[1] - 1, a[2] + 1, a[3] + 1), t,
                at(1, 12, 0.4))
    D.light("burnt.blood:around the altar", t + 0.32, steady_out=at(1, 12, 0.75))

    # ---- 1:12  the ram's pieces, head, fat; in order on the wood -----------
    t = cue(1, 12, "pieces")
    E["pen.goat2"].ev("out", t, 0.6, group="ram12")
    E["pen.ram2"].ev("out", t, 0.6, group="ram12")
    P.cutaway(ram, "ram", t, group="ram12")
    for i, ln in enumerate(ram.lines("pieces")):
        traced_el(f"cut.ram.pieces.{i}", "bench", ln, B.TEXT, 2.4, t + 0.3 + i * 0.08, 0.45, z=26)
    ram_chip = dict(ox_chip)
    ram_chip.update({"pieces": (bx[1], band), "head": (bx[2], band), "fat": (bx[0], band)})
    P.bench_chip("chip.ram.pieces", "pieces", *ram_chip["pieces"], t + 0.3,
                 lead=ram.anchor["pieces"], out=cue(1, 12, "order"), group="ram12")
    for word in ("head", "fat"):
        t = cue(1, 12, word)
        P.part_pulse(ram, "ram", word, t, tag="12")
        P.bench_chip(f"chip.ram.{word}", word, *ram_chip[word], t, lead=ram.anchor[word],
                     out=cue(1, 12, "order"), group=f"pram{word}")
    P.to_wood(ram, "ram", {"pieces": ram.anchor["meat"], "head": ram.anchor["head"],
                           "fat": ram.anchor["fat"]}, cue(1, 12, "order"), ["pieces", "head", "fat"])

    # ---- 1:13  innards, legs, water; the whole; burn; case clear ------------
    for word in ("innards", "legs"):
        t = cue(1, 13, word)
        P.part_pulse(ram, "ram", word, t, tag="13")
        P.bench_chip(f"chip.ram.{word}", word, *ram_chip[word], t, lead=ram.anchor[word],
                     out=cue(1, 13, "burn"), group=f"pram{word}")
    t = cue(1, 13, "water")
    P.water(ram, "ram", t)
    lx, ly = ram.anchor["legs"]
    P.bench_chip("chip.ram.water", "water", *ram_chip["water"], t + 0.1, lead=(lx + 30, ly),
                 out=cue(1, 13, "burn"), group="water.ram.0")
    t = cue(1, 13, "whole")
    P.bench_chip("chip.whole13", "the whole", P.FIRE_XS[1] - 4, P.A_TOP - 96, t, anchor="lm",
                 group="whole13")
    D.light("burnt.burns:the whole", t + 0.32, steady_out=cue(1, 13, "pleasant aroma", d=0.35))
    P.burn(ram, "ram", cue(1, 13, "burn"))
    P.case_clear(cue(1, 13, "pleasant aroma"))

    # ---- 1:14  turtledoves, pigeons -------------------------------------------
    dv = P.Dove()
    add(El("pen.dove1.body", "bench", dv.svg("body", P.DOVE_X[1]), z=20))
    add(El("pen.dove1.head", "bench", dv.svg("head", P.DOVE_X[1]), z=21))
    add(El("pen.dove2", "bench", dv.svg("all", P.DOVE_X[0]), z=20))
    t = cue(1, 14, "turtledoves")
    E["pen.dove1.body"].ev("in", t, 0.5, group="icon.td")
    E["pen.dove1.head"].ev("in", t, 0.5, group="icon.td")
    t2 = t + 0.32
    D.light("burnt.thing:turtledove", t2, link=[("bench", dv.outline(P.DOVE_X[1]), True)],
            group="icon.td")
    case_flock.ev("out", t2 + 0.5, 0.35)
    case_birds = D.case_outline(["burnt.thing:turtledove", "burnt.thing:pigeon"], t2 + 0.5)
    t = cue(1, 14, "pigeons")
    d = fit(t, 0.5)
    E["pen.dove2"].ev("in", t, d, group="icon.pg")
    D.light("burnt.thing:pigeon", t, group="icon.pg", pulse=False, dur=d)

    # ---- 1:15  to the altar; wring; head; burn; drained; side ---------------
    t = cue(1, 15, "bring")
    rel = (dv.bay_x - P.DOVE_X[1], dv.bay_g - dv.ground)
    b_el, h_el = E["pen.dove1.body"], E["pen.dove1.head"]
    glide(b_el, t, B.arc_path((0, 0), rel, 0.45), 1.0, "dove to the bird bay", "bench move",
          quad=True, group="dovebay")
    h_el.ev("move", t, 1.0, path=B.arc_path((0, 0), rel, 0.45), quad=True, group="dovebay")
    DP = dv.DP
    traced_el("bay.neck", "bench", [DP((8.4, 4.6)), DP((7.4, -0.6))], BLOOD, 3,
              cue(1, 15, "wring"), 0.5, z=27)
    t = cue(1, 15, "head")
    h_el.ev("move", t, 0.5, path=[(0, 0), (-8, -10)], group="headoff")
    P.bench_chip("chip.dove.head", "head", DP((9, 2))[0] - 4, P.A_TOP - 70, t + 0.1,
                 lead=(DP((9.5, 2.5))[0] - 8, DP((9.5, 2.5))[1] - 12), out=cue(1, 15, "burn"),
                 group="headoff")
    t = cue(1, 15, "burn")
    hx_, hy_ = DP((9.1, 2.2))
    to = (P.FIRE_XS[3] - (hx_ - 8), (P.A_TOP - 34) - (hy_ - 10))
    glide(h_el, t, B.arc_path((0, 0), to, 0.25), 0.9, "the head to the fire", "bench move",
          quad=True, group="headfire")
    P.flare(t + 0.92, 1.22, 0.9, group="headfire2")
    A = P.A_BODY
    run = [(A[2] - 4, P.A_TOP + 4), (A[2] - 6, P.A_TOP + 40), (A[2] - 3, P.A_TOP + 80),
           (A[2] - 5, P.A_TOP + 112), (A[2] - 4, A[3] - 3)]
    traced_el("bay.run", "bench", run, BLOOD, 4.5, cue(1, 15, "drained"), 0.8, z=27)
    # "on the side of the altar": the slot unveils in place, with a link pulse
    D.light("burnt.blood:the altar's side", cue(1, 15, "side"),
            link=[("bench", [(x + 0.5, y) for x, y in run], False)], group="side")

    # ---- 1:16  crop; east; the place of the ashes -----------------------------
    t = cue(1, 16, "crop")
    ax, ay = S["altar_c"]
    crop = add(El("s1.crop", "strip",
                  f'<ellipse cx="{B.f2(ax)}" cy="{B.f2(ay + 1)}" rx="5" ry="3.6" '
                  f'fill="rgb(150,110,70)" stroke="{B.rgb(B.TEXT)}" stroke-width="1"/>'
                  + B.halo_text("crop", ax + 8, ay + 1, 13, anchor="lm"),
                  z=31, texts=[(B.tbox("crop", ax + 8, ay + 1, 13, "lm"), 13, "strip chip")]))
    crop.ev("in", t, 0.5)
    P.walk(crop, cue(1, 16, "east"), [(0, 0), (S["ashes"][0] - ax, 0)], 1.2, "crop east")
    t = cue(1, 16, "ashes")
    P.place("ashes", t, dur=fit(t, 0.6), pulse=False)

    # ---- 1:17  wings; not divided; burn; the whole bird; the file view ---------
    t = cue(1, 17, "wings")
    wing = [DP((-1.5, 9.5)), DP((2.5, 4.5)), DP((4.5, 0.5))]
    traced_el("bay.wings", "bench", wing, B.HL, 2.6, t, 0.7, z=27)
    P.bench_chip("chip.wings", "wings", wing[0][0] + 6, P.A_TOP - 92, t + 0.1, lead=wing[0],
                 group="bay.wings")
    P.bench_chip("chip.notdiv", "not divided", P.BAY[0] - 12, P.A_TOP - 124, cue(1, 17, "divide"))
    t = cue(1, 17, "burn")
    onto = (P.FIRE_XS[2] + 12 - dv.bay_x, -14)
    glide(b_el, t, B.arc_path((0, 0), onto, 0.25), 0.9, "the bird onto the wood", "bench move",
          quad=True, group="burn17")
    for nm in ("bay.neck", "bay.wings"):
        E[nm].ev("out", t, 0.4, group="burn17")
    P.flare(t + 0.92, 1.3, 0.8, group="burn17b")
    land = D.fly("the whole bird", (P.FIRE_XS[0] - 8, P.A_TOP - 96), "burnt.burns:the whole bird",
                 t + 1.42)
    # the file view on "burnt offering"; everything of s1 still on clears
    # under its crossfade (the boundary: places, the altar set, the dock)
    t_fv = cue(1, 17, "burnt offering")
    assert t_fv >= land + 0.3, (t_fv, land)
    P.section_clear(t_fv, group="fileview")
    D.file_view("burnt", t_fv, T_back=B.limit(1, 17) - 1.0)
