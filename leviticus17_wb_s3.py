"""Leviticus 3:1-17 and the 4:1-2 range, the peace offering, on the workbench (section s3).

Starts on the s2|s3 boundary (the meal column in the dock, meal's file view
crossing back by 3:1 t = 1.5 s, the altar set on the bench) and leaves the
s3|s4 boundary: the places, the altar set, and the peace column lit in the
dock with the peace tab active.

Three cases on the animal set (leviticus17_spec.CASES 3:1, 3:6, 3:12), each
the same work: the beast in the pen and its BROUGHT icon lit with a link
pulse; the hand on the head; the place of the killing pulsed on the strip
(the door, the Tent of Meeting) and the priests at the strip's altar; the
blood ring traced round it; the beast opened (beast_parts) and the parts
the verse names pulsed with their chips (offerings.CUT's words, 3:9 in its
own: "fat on the inwards"), the other parts dimmed; on "burn" the taken
parts glide onto the wood together (one bench move) and the entry flies to
ON THE ALTAR (3:16: it is lit, so its who-line, "from the herd, or a goat",
unveils in place). 3:17 is the bans in the pen half: "dwellings", the fat and
the blood under the not-mark, and NOT EATEN's "the fat, the blood" unveils
on "blood" (3:17's last word: no time to fly). The 4:1-2 range files the
peace column (its formula and 4:2 name nothing new); on "sins" the sin
column's place in the table pulses, still veiled.

THE BLOOD's "around the altar" lifts in place on 3:2's "around", with a
link pulse on the strip's ring (it is said there, and a flight would land
too late); 3:8 and 3:13 name it again.

Moves (QC's budget): no camera; chip flights at 3:5 ("the fat") and 3:11
("the fat, the tail");
bench moves at 3:5, 3:11 and 3:16; the filing glide in 4:1-2.
"""

import offerings as OF
import svg_figures as F
import leviticus17_bench as B
import leviticus17_dock as D
import leviticus17_parts as P
import leviticus17_art as ART
from generate_tabernacle import PANEL, SAND
from leviticus17_bench import El, add, cue, at, pulse_el, traced_el, rect_pts
from leviticus17_parts import S, BLOOD

STUB = False
VERSES = [(3, v) for v in range(1, 18)] + [(4, 1), (4, 2)]

REACH = {}
EXCUSED = {}

# the parts a peace offering takes (Lev 3:3-4, 9-10, 14-15) and the
# beast_parts keys that stay bright on the opened beast
TAKEN = ("fat_cover", "fat_on", "kidneys", "kidney_fat", "loins", "liver_cover", "tail_fat",
         "backbone", "silhouette")
FAT_PARTS = ("fat_cover", "fat_on", "kidney_fat")

# chip places ("mm" centres) over each opened beast, in three rows in the
# bench's top band, placed so that no leader crosses another chip's plate
CHIP_ROW = (262, 304, 346)


def _chips(kind):
    """{part: (x, y)} for each beast's chips."""
    r1, r2, r3 = CHIP_ROW
    if kind == "bull":
        return {"fat_cover": (82, r1), "fat_on": (232, r1),
                "kidneys": (70, r1), "kidney_fat": (190, r2), "liver_cover": (268, r3)}
    if kind == "sheep":
        return {"tail_fat": (88, r1), "fat_on": (240, r1), "fat_cover": (118, r2),
                "backbone": (275, r3),
                "kidneys": (70, r1), "kidney_fat": (200, r2), "liver_cover": (270, r3)}
    return {"fat_cover": (86, r1), "fat_on": (236, r1),
            "kidneys": (70, r1), "kidney_fat": (200, r2), "liver_cover": (270, r3)}


def _label(part, cv=None):
    words = {(3, 9): {"fat_on": "fat on the inwards"}}
    if cv in words and part in words[cv]:
        return words[cv][part]
    return OF.CUT[part].label


def _offerer(key, beast, T, T_out):
    """The offerer's hand on the beast's head (1:4's pose), scaled so the hand
    meets the head."""
    reach = F.side_person(arms="reach")
    hpx, hpy = ART.hand_pt(reach)
    hx, hy = beast.anchor["head"]
    k = max(1.7, min(2.35, (P.PEN_G - hy) / hpy))
    man_x = hx + hpx * k + 15
    el = P.figure_el(key, reach, man_x, P.PEN_G, k, T, flip=-1, z=22, dur=0.5)
    el.ev("out", T_out, 0.5)
    return el


def _open(beast, figure_key, name, T, group):
    """The beast in the pen opens into its parts (beast_parts), in place."""
    B.ELS[figure_key].ev("out", T, 0.6, group=group)
    P.cutaway(beast, name, T, group=group)


def _dim_others(beast, name, T, group):
    """Every part the offering doesn't take dims, so the fat stands out."""
    for k in P.CUT_ORDER:
        if k in beast.parts and k not in TAKEN:
            B.ELS[f"cut.{name}.{k}"].ev("dim", T, 0.6, to=0.3, group=group)


def _part(beast, name, part, T, xy, out, cv, tag, t_chip=None):
    """A named part pulses with its chip (leader to the part); the chip waits
    for t_chip when its words end later than the part's first word."""
    P.part_pulse(beast, name, part, T, tag=tag, group=f"s3p{name}{part}{tag}")
    tc = T if t_chip is None else t_chip
    return P.bench_chip(f"s3.chip.{name}.{part}", _label(part, cv), xy[0], xy[1], tc,
                        lead=beast.anchor[part], out=out,
                        group=f"s3p{name}{part}{tag}" if t_chip is None else None)


def _to_wood(beast, name, items, T, dur=1.0):
    """The taken parts lift off the opened beast and glide together onto the
    wood (parts.to_wood: one bench move): items [(word, (x, y), [part
    keys])], their parts dimmed behind them. Returns the landing T."""
    P.to_wood(beast, name, {w: xy for w, xy, _d in items}, T, [w for w, *_r in items], dur=dur,
              dims={w: d for w, _xy, d in items}, dim_to=0.3, kinds={"kidneys": "inn"})
    return T + 0.1 + dur


def _herd_case_parts(beast, name, c, v3, v4, chips):
    """3:3-4 (and 3:14-15): the fat, then the kidneys and the liver's cover,
    each pulsed with its chip; 3:3's chips retire on 3:4's 'kidneys'."""
    t_k = cue(c, v4, "kidneys")
    _part(beast, name, "fat_cover", cue(c, v3, "covers"), chips["fat_cover"], t_k - 0.0,
          (c, v3), "a")
    _part(beast, name, "fat_on", cue(c, v3, "all the fat"), chips["fat_on"], t_k, (c, v3), "a",
          t_chip=cue(c, v3, "innards", 1))             # "...that is on the innards"


def _kidney_parts(beast, name, c, v, chips, out):
    """3:4, 3:10, 3:15: the two kidneys, the fat by the loins, the liver's cover."""
    _part(beast, name, "kidneys", cue(c, v, "kidneys"), chips["kidneys"], out, (c, v), "b")
    t = cue(c, v, "loins")
    P.part_pulse(beast, name, "loins", t + 0.05, tag="b", group=f"s3p{name}kidney_fatb")
    _part(beast, name, "kidney_fat", t, chips["kidney_fat"], out, (c, v), "b")
    _part(beast, name, "liver_cover", cue(c, v, "liver"), chips["liver_cover"], out, (c, v), "b")


def _ring(key, T, dur, group=None):
    a = S["altar"]
    return traced_el(key, "strip", rect_pts(a[0] - 4, a[1] - 4, a[2] + 4, a[3] + 4), BLOOD, 2.4,
                     T, dur, z=35, closed=True, group=group)


def _priests(key, T):
    a = S["altar"]
    return P.priests_el(key, [a[0] - 14, a[0] + 8], T)


def build():
    E = B.ELS
    band_src = (P.FIRE_XS[0] - 6, P.A_TOP - 96)        # a flight's chip over the stack

    # =====================================================================
    # Case 1: the herd (3:1-3:5)
    # =====================================================================
    # ---- 3:1  peace offerings; anyone; the herd; male or female ---------
    D.switch("peace", cue(3, 1, "peace offerings"))      # the tab and header named 0.9 s on
    D.light("peace.by", cue(3, 1, "offers"))
    ox = P.Beast("bull", P.OX_X, P.PEN_G, P.OX_K)
    ox_line = F.outline(F.ox(), P.OX_X, P.PEN_G, P.OX_K)
    t = cue(3, 1, "herd")
    P.figure_el("s3.ox", F.ox(), P.OX_X, P.PEN_G, P.OX_K, t)
    D.light("peace.thing:herd", t + 0.32, link=[("bench", ox_line, True)], group="s3icon.herd")
    case_herd = D.case_outline(["peace.thing:herd"], t + 0.92)
    P.bench_chip("s3.mf1", "male or female", P.OX_X + 20, P.PEN_G + 21, cue(3, 1, "female"),
                 out=cue(3, 3, "offering"))

    # ---- 3:2  the hand on the head; the door; Aaron's sons; the ring --------
    _offerer("s3.offerer1", ox, cue(3, 2, "hand"), cue(3, 2, "kill"))
    pulse_el("s3.ox.head.p", "bench", ox.outline("head")[0][0], cue(3, 2, "head"))
    t = cue(3, 2, "door")
    P.place("door", t, group="s3door1")
    pulse_el("s3.ox.door", "bench", ox_line, t, group="s3door1")
    _priests("s3.priests1", cue(3, 2, "Aaron's"))
    _ring("s3.ring1", cue(3, 2, "blood"), 1.0, group="s3around2")
    # "around on the altar": THE BLOOD's entry lifts in place, the ring pulsed
    a = S["altar"]
    ring_pts = rect_pts(a[0] - 4, a[1] - 4, a[2] + 4, a[3] + 4)
    D.light("peace.blood:around the altar", cue(3, 2, "around"),
            link=[("strip", ring_pts, True)], group="s3around2")

    # ---- 3:3  an offering made by fire: the ox opens; the fat ---------------
    t = cue(3, 3, "offering")                         # "an offering made by fire"
    _open(ox, "s3.ox", "s3bull", t, "s3open1")
    _dim_others(ox, "s3bull", cue(3, 3, "fat"), "s3dim1")
    ch = _chips("bull")
    _herd_case_parts(ox, "s3bull", 3, 3, 4, ch)

    # ---- 3:4  the two kidneys, the fat by the loins, the liver's cover ------
    t_burn = cue(3, 5, "burn")
    _kidney_parts(ox, "s3bull", 3, 4, ch, t_burn)

    # ---- 3:5  burn it on the altar: the fat onto the wood; "the fat" flies --
    a = ox.anchor
    land = _to_wood(ox, "s3bull", [
        ("fat", a["fat_cover"], ["fat_cover", "fat_on", "kidney_fat"]),
        ("kidneys", a["kidneys"], ["kidneys"]),
        ("cover", a["liver_cover"], ["liver_cover"])], t_burn)
    t_fly = D.fly("the fat", band_src, "peace.burns:the fat", land + 0.4)
    P.flare(cue(3, 5, "fire"), 1.3, 1.0, group="s3flare5")
    assert t_fly < cue(3, 5, "fire")
    P.case_clear(cue(3, 5, "pleasant aroma"), regions=("bench", "strip"))

    # =====================================================================
    # Case 2: the flock, a lamb (3:6-3:11)
    # =====================================================================
    # ---- 3:6  the flock: a lamb and a goat; male or female -------------------
    t = cue(3, 6, "flock")
    case_herd.ev("out", t, 0.35)
    lamb = P.Beast("sheep", P.RAM_X, P.PEN_G, P.RAM_K)
    lamb_line = F.outline(F.sheep(), P.RAM_X, P.PEN_G, P.RAM_K)
    goat_bx = 262
    t2 = t + 0.32
    P.figure_el("s3.lamb", F.sheep(), P.RAM_X, P.PEN_G, P.RAM_K, t2, group="s3flock")
    P.figure_el("s3.goat1", F.goat(), goat_bx, P.PEN_BACK_G, P.BACK_K, t2, z=18,
                group="s3flock")
    P.bench_chip("s3.mf2", "male or female", P.RAM_X + 10, P.PEN_G + 21, cue(3, 6, "female"),
                 out=cue(3, 9, "offering"))

    # ---- 3:7  a lamb -----------------------------------------------------------
    t = cue(3, 7, "lamb")
    E["s3.goat1"].ev("out", t, 0.6, group="s3lamb7")
    t2 = t + 0.32
    D.light("peace.thing:lamb", t2, link=[("bench", lamb_line, True)], group="s3icon.lamb")
    case_flock = D.case_outline(["peace.thing:lamb"], t2 + 0.6)

    # ---- 3:8  the hand; before the Tent of Meeting; the ring flies ---------------
    _offerer("s3.offerer2", lamb, cue(3, 8, "hand"), cue(3, 8, "kill"))
    pulse_el("s3.lamb.head.p", "bench", lamb.outline("head")[0][0], cue(3, 8, "head"))
    t = cue(3, 8, "Tent of Meeting")
    P.place("tent", t, group="s3tent8")
    pulse_el("s3.lamb.tent", "bench", lamb_line, t, group="s3tent8")
    _priests("s3.priests2", cue(3, 8, "Aaron's"))
    _ring("s3.ring2", cue(3, 8, "blood"), 0.7, group="s3around8")
    D.current("peace.blood:around the altar", cue(3, 8, "around"),
              link=[("strip", ring_pts, True)], group="s3around8")

    # ---- 3:9  the lamb opens; its fat, the tail, the backbone, the fat ----------
    t = cue(3, 9, "offering")
    _open(lamb, "s3.lamb", "s3lamb", t, "s3open2")
    _dim_others(lamb, "s3lamb", cue(3, 9, "fat"), "s3dim2")
    ch = _chips("sheep")
    t_k = cue(3, 10, "kidneys")
    _part(lamb, "s3lamb", "tail_fat", cue(3, 9, "tail fat"), ch["tail_fat"], t_k, (3, 9), "a")
    _part(lamb, "s3lamb", "backbone", cue(3, 9, "backbone"), ch["backbone"], t_k, (3, 9), "a")
    _part(lamb, "s3lamb", "fat_cover", cue(3, 9, "covers"), ch["fat_cover"], t_k, (3, 9), "a")
    _part(lamb, "s3lamb", "fat_on", cue(3, 9, "all the fat"), ch["fat_on"], t_k, (3, 9), "a",
          t_chip=cue(3, 9, "inwards", 1))

    # ---- 3:10  the kidneys, the fat by the loins, the liver's cover ---------------
    t_burn = cue(3, 11, "burn")
    _kidney_parts(lamb, "s3lamb", 3, 10, ch, t_burn)

    # ---- 3:11  the priest burns it: onto the wood; "the fat, the tail" flies -------
    a = lamb.anchor
    land = _to_wood(lamb, "s3lamb", [
        ("tail", a["tail_fat"], ["tail_fat"]),
        ("fat", a["fat_cover"], ["fat_cover", "fat_on", "kidney_fat", "liver_cover"]),
        ("kidneys", a["kidneys"], ["kidneys"])], t_burn)
    P.flare(land - 0.05, 1.25, 0.8, group="s3wood.s3lamb")
    D.fly("the fat, the tail", band_src, "peace.burns:the fat, the tail", land + 0.45)
    P.case_clear(cue(3, 11, "fire"), regions=("bench", "strip"))

    # =====================================================================
    # Case 3: a goat (3:12-3:16)
    # =====================================================================
    # ---- 3:12  a goat ----------------------------------------------------------------
    t = cue(3, 12, "goat")
    gk, gx = 2.6, 140
    goat = P.Beast("goat", gx, P.PEN_G, gk)
    goat_line = F.outline(F.goat(), gx, P.PEN_G, gk)
    P.figure_el("s3.goat", F.goat(), gx, P.PEN_G, gk, t)
    t2 = t + 0.32
    D.light("peace.thing:goat", t2, link=[("bench", goat_line, True)], group="s3icon.goat")
    case_flock.ev("out", t2 + 0.6, 0.35)
    case_goat = D.case_outline(["peace.thing:goat"], t2 + 0.6)

    # ---- 3:13  the hand; before the Tent of Meeting; the ring, current again ----------
    _offerer("s3.offerer3", goat, cue(3, 13, "hand"), cue(3, 13, "kill"))
    pulse_el("s3.goat.head.p", "bench", goat.outline("head")[0][0], cue(3, 13, "head"))
    t = cue(3, 13, "Tent of Meeting")
    P.place("tent", t, group="s3tent13")
    pulse_el("s3.goat.tent", "bench", goat_line, t, group="s3tent13")
    _priests("s3.priests3", cue(3, 13, "Aaron"))
    _ring("s3.ring3", cue(3, 13, "blood"), 0.9)
    D.light("peace.blood:around the altar", cue(3, 13, "around"))

    # ---- 3:14  the goat opens; the fat --------------------------------------------------
    t = cue(3, 14, "offering", 1)
    _open(goat, "s3.goat", "s3goat", t, "s3open3")
    _dim_others(goat, "s3goat", cue(3, 14, "fat"), "s3dim3")
    ch = _chips("goat")
    _herd_case_parts(goat, "s3goat", 3, 14, 15, ch)

    # ---- 3:15  the kidneys, the fat by the loins, the liver's cover ----------------------
    t_burn = cue(3, 16, "burn")
    _kidney_parts(goat, "s3goat", 3, 15, ch, t_burn)

    # ---- 3:16  burn them: onto the wood; "from the herd, or a goat"; all the fat ---------
    a = goat.anchor
    land = _to_wood(goat, "s3goat", [
        ("fat", a["fat_cover"], ["fat_cover", "fat_on", "kidney_fat"]),
        ("kidneys", a["kidneys"], ["kidneys"]),
        ("cover", a["liver_cover"], ["liver_cover"])], t_burn)
    P.flare(land - 0.05, 1.25, 0.8, group="s3wood.s3goat")
    # the entry's who-line names the goat: it unveils now (REACH 3:16)
    D.light("peace.burns:the fat/who", cue(3, 16, "food"))
    D.steady("peace.burns:the fat", cue(3, 16, "all the fat"), B.limit(3, 16))

    # =====================================================================
    # 3:17: the bans (the pen half); "the fat, the blood"
    # =====================================================================
    t = at(3, 17, 0.2)                         # the goat's case ends as the bans begin
    P.case_clear(t, regions=("bench", "strip"))
    case_goat.ev("out", t, 0.35, group="clear")
    tent = F.tent()
    tk, tx, tg = 0.5, 172, 512
    t = cue(3, 17, "dwellings")
    add(El("s3.dwell", "bench", B.fig(tent, tx, tg, tk, SAND, PANEL, tol=0.9), z=20)).ev(
        "in", t, 0.6, group="s3dwell")
    P.bench_chip("s3.dwell.chip", "dwellings", tx, tg + 26, t + 0.15, group="s3dwell")
    fx, fy, bx_, by_, r = 106, 340, 238, 340, 46
    t = cue(3, 17, "fat")
    add(El("s3.ban.fat", "bench", ART.fat_svg(fx, fy, 84, 48), z=20)).ev("in", t, 0.4,
                                                                          group="s3ban.fat")
    P.bench_chip("s3.ban.fat.chip", "fat", fx, fy + r + 18, t, group="s3ban.fat")
    P.not_el("s3.ban.fat.not", "bench", (fx, fy), r, t, 0.55, group="s3ban.fat")
    t = cue(3, 17, "blood")
    add(El("s3.ban.blood", "bench", ART.drop_svg(bx_, by_, 66), z=20)).ev("in", t, 0.35,
                                                                           group="s3ban.blood")
    P.bench_chip("s3.ban.blood.chip", "blood", bx_, by_ + r + 18, t, dur=0.35,
                 group="s3ban.blood")
    P.not_el("s3.ban.blood.not", "bench", (bx_, by_), r, t, 0.6, group="s3ban.blood")
    # NOT EATEN's entry unveils in place with them: "blood" is 3:17's last
    # word, no time to fly
    D.light("peace.not_eaten:the fat, the blood", t, pulse=False, dur=0.35, group="s3ban.blood")

    # =====================================================================
    # 4:1-2: the peace column filed; the sin column's place pulses on "sins"
    # =====================================================================
    t_fv = at(4, 1, 0.3)
    P.section_clear(t_fv, group="fileview")
    t_back = cue(4, 2, "things")
    fv = D.file_view("peace", t_fv, T_back=t_back)
    fv.pulse_column("sin", cue(4, 2, "sins"))
