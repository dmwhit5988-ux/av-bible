"""Leviticus 4:3-4:35, the sin offering, on the workbench (section s4).

Five cases, each its own (leviticus17_spec.CASES): the anointed priest's
bull (4:3-12), the congregation's bull (4:13-21), the ruler's male goat
(4:22-26), the common person's female goat (4:27-31) and lamb (4:32-35).

It starts on the s3|s4 boundary (the peace column showing, the altar set,
the places tent, door, altar, north, ashes) and leaves the s4|s5 boundary:
the sin column showing with every unit it lit, the altar set alone on the
bench, and on the strip the places it named (veil, altar of incense,
outside the camp, clean place) beside s1's.

Sets on the bench (crossfades inside the bench, 0.6 s):
- the animal set: the pen (x 8-338) and the altar (the shared altar set);
- the holy place (4:5-7, 4:16-18): the veil (generate_tabernacle's veil
  inset) with the seven numbered drops before it, and the altar of incense
  (its inset) with its horns, in the pen's half; the bronze altar stays;
- the clean place (4:12, 4:21): the heap where the ashes are poured out,
  wood, the whole bull on it, and fire, in the pen's half.

Each bull opens into its cutaway on the word that names its fat (4:8, 4:19)
and its fat glides onto the wood off the cutaway (parts.to_wood); the
goats' and the lamb's fat (4:26, 4:31, 4:35) is a slab off the whole beast.

The strip: the blood's path from the door to the veil (4:5, 4:16), the
bull carried from the altar out through the gate to the clean place (4:12,
4:21), the north side current again (4:24, 4:29, 4:33).

Moves (QC's budget): no camera; chip flights at 4:10 (the fat), 4:12 (the
bull: outside the camp) and 4:25 (on the altar's horns), 4:26 (the fat);
bench moves (the fat onto the wood) at 4:10, 4:19, 4:26, 4:31, 4:35; token
walks (the carried bull) at 4:12 and 4:21.
"""

import generate_tabernacle as GT
import svg_figures as F
import leviticus17_bench as B
import leviticus17_dock as D
import leviticus17_parts as P
import leviticus17_art as ART
from generate_tabernacle import PANEL, TEXT
from svg_vocab import mix
from leviticus17_bench import (El, add, cue, at, fit, pulse_el, traced_el, glide, rect_pts,
                               f2, rgb)
from leviticus17_parts import S, BLOOD

STUB = False
VERSES = [(4, v) for v in range(3, 36)]

REACH = {}
EXCUSED = {}

# ---------------------------------------------------------------------------
# Geometry (bench px)
# ---------------------------------------------------------------------------

G0 = P.PEN_G                          # the pen's ground
MAN_K = 2.0                           # people and the bull: one scale
PRIEST_K = 1.6                        # the front-view priest (he is drawn taller)
GOAT_K, GOAT_X = 2.4, 140
LAMB_X = 140
LAMB_BK = 2.0                         # the lamb's head ring: the sheep's parts at this k
LAMB_DRAW = LAMB_BK * 47.0 / 28.1     # svg_figures' lamb drawn up to match (as the cast does)

# the holy place: the veil inset (its curtain's top-left at 24, 262) and
# the altar of incense inset (centred at x 272, its feet on y 520)
HVK = 0.82
HV_AT = (24 - 68 * HVK, 262 - 84 * HVK)
HNK = 0.85
HN_AT = (264 - (GT.ICX - GT.IX) * HNK, 520 - (GT.NY1 - GT.IY) * HNK)


def _hv(p):
    return ART.inset_pt(p, HVK, HV_AT)


def _hn(p):
    return ART.inset_pt(p, HNK, HN_AT)


VEIL_R = _hv((GT.IX + 68, GT.IY + 84)) + _hv((GT.IX + 68 + 220, GT.IY + 84 + 150))
DROPS_Y = _hv((0, GT.IY + 84 + 150 + 46))[1] + 30
DROPS_X = [VEIL_R[0] + 16 + i * (VEIL_R[2] - VEIL_R[0] - 32) / 6 for i in range(7)]
INC_BOX = _hn((GT.NX0, GT.NY0 - 13)) + _hn((GT.NX0 + GT.NW, GT.NY1))
INC_HORNS = [[_hn(p) for p in GT.horn_points(hx0, hy0, hx1, hy1, -1 if hx0 < GT.NX0 else 1)]
             for hx0, hy0, hx1, hy1 in GT._incense_horns()]
# the bronze altar's horns (the altar set's inset at the parts module's scale)
A_HORNS = [[P._a(p) for p in GT.horn_points(*h, -1 if h[0] < GT.AX else 1)] for h in ART.A_HORNS]
A = P.A_BODY

# chip places
ROW_A, ROW_B = P.BENCH[1] + 26, P.BENCH[1] + 60          # two chip rows over the pen
HORNS_CHIP = (652, 362)
BASE_CHIP = (652, 548)


def _poly(pts, fill, op=0.92):
    return (f'<polygon points="{B.pts_str(pts)}" fill="{rgb(fill)}" fill-opacity="{op}" '
            f'stroke="{rgb(BLOOD)}" stroke-width="1"/>')


# ---------------------------------------------------------------------------
# Small helpers on the public API
# ---------------------------------------------------------------------------

class Person:
    """A man (side view, facing the beast at his left) whose hand comes down
    on the beast's head: `.down` and `.reach` elements, crossfaded on the
    hand's word."""

    def __init__(self, key, head, pose=("reach", "stand", 0), k=MAN_K, dx=15, gy=G0, z=22):
        arms, legs, lean = pose
        self.down = F.side_person(arms="down", legs=legs, lean=lean)
        self.reach = F.side_person(arms=arms, legs=legs, lean=lean)
        hpx, _hpy = ART.hand_pt(self.reach)
        self.x, self.gy, self.k = head[0] + hpx * k + dx, gy, k
        self.key = key
        self.d = P.figure_el(key + ".down", self.down, self.x, gy, k, None, flip=-1, z=z)
        self.r = P.figure_el(key + ".reach", self.reach, self.x, gy, k, None, flip=-1, z=z)

    def line(self, which="down"):
        parts = self.down if which == "down" else self.reach
        return F.outline(parts, self.x, self.gy, self.k, flip=-1)

    def come(self, T, group=None, reach=False):
        (self.r if reach else self.d).ev("in", T, 0.6, group=group)

    def hand(self, T, group=None):
        self.d.ev("out", T, 0.35, group=group)
        self.r.ev("in", T, 0.35, group=group)


class Priest:
    """The anointed priest (svg_figures.priest, mitre and breastplate),
    front view, at the bull's head: arms down, then the hand out on it."""

    def __init__(self, key, head, k=PRIEST_K, gy=G0, z=22):
        self.down = F.priest(arms="down")
        self.reach = F.priest(arms="point_r")
        hpx, _hpy = ART.hand_pt(self.reach)
        self.x, self.gy, self.k = head[0] + hpx * k + 4, gy, k
        self.d = P.figure_el(key + ".down", self.down, self.x, gy, k, None, flip=-1, z=z)
        self.r = P.figure_el(key + ".reach", self.reach, self.x, gy, k, None, flip=-1, z=z)

    def line(self):
        return F.outline(self.down, self.x, self.gy, self.k, flip=-1)

    def hand(self, T, group=None):
        self.d.ev("out", T, 0.35, group=group)
        self.r.ev("in", T, 0.35, group=group)


def fat_slab(key, src, T_in, group, i=1):
    """A slab of fat on the beast at src (comes in at T_in); .go(T) glides it
    onto the wood (one bench move)."""
    sb = P.slot_box(i)
    cx, cy = (sb[0] + sb[2]) / 2, (sb[1] + sb[3]) / 2
    el = add(El(key, "bench", P.slab_svg("fat", sb), z=30,
                off0=(round(src[0] - cx, 1), round(src[1] - cy, 1))))
    el.ev("in", T_in, 0.4, group=group)
    el.to = (cx - src[0], cy - src[1])
    el.top = (sb[0], sb[1] - 14)
    return el


def to_wood(el, T, group, dur=1.1):
    glide(el, T, B.arc_path((0, 0), el.to, 0.2), dur, "the fat onto the wood", "bench move",
          quad=True, group=group)
    return T + dur


def horns_el(key, T, group, chip_key):
    """Blood on the bronze altar's horns, with its chip."""
    el = add(El(key, "bench", "".join(_poly(h, BLOOD) for h in A_HORNS), z=32))
    el.ev("in", T, 0.5, group=group)
    lead = A_HORNS[1][len(A_HORNS[1]) // 2]
    P.bench_chip(chip_key, "horns", *HORNS_CHIP, T, lead=lead, group=group)
    return el


def base_el(key, T, chip_key, group):
    """The rest of the blood poured out at the altar's base, with its chip."""
    y = A[3] - 2.5
    pts = [(A[0] + 6, y), (A[0] + 60, y - 1), (A[0] + 124, y), (A[0] + 186, y - 1), (A[2] - 6, y)]
    el = traced_el(key, "bench", pts, BLOOD, 5, T, 0.8, z=33, group=group)
    P.bench_chip(chip_key, "base", *BASE_CHIP, T, lead=(A[2] - 8, y), group=group)
    return el


def clear(T, group, regions=("bench",), dock=False, dur=0.8):
    """Everything of this section still on at T in `regions` fades (and its
    dock outlines with dock=True): parts.case_clear."""
    return P.case_clear(T, regions=regions, dur=dur, group=group, dock=dock)


def carcass(key, T, group):
    """The whole bull, carried (a bundle: meat in its skin), at the strip's altar."""
    ax, ay = S["altar_c"]
    svg = (B.slab(ax - 14, ay - 6, ax + 14, ay + 6, P.MEAT, TEXT, 5)
           + f'<line x1="{f2(ax - 8)}" y1="{f2(ay - 6)}" x2="{f2(ax - 8)}" y2="{f2(ay + 6)}" '
             f'stroke="{rgb(TEXT)}" stroke-width="1"/>'
           + f'<line x1="{f2(ax + 8)}" y1="{f2(ay - 6)}" x2="{f2(ax + 8)}" y2="{f2(ay + 6)}" '
             f'stroke="{rgb(TEXT)}" stroke-width="1"/>')
    el = add(El(key, "strip", svg, z=40))
    el.ev("in", T, 0.5, group=group)
    return el


def carry_out(el, T, group):
    """The bundle from the altar through the gate to the clean place (a
    token walk)."""
    pts = P.route("altar", "gate", "clean")
    rel = [(x - pts[0][0], y - pts[0][1] - 2) for x, y in pts]
    return P.walk(el, T, rel, 2.0, "the bull carried to the clean place", group=group)


CP_X, CP_G = 168, 530                  # the clean place on the bench: the heap's centre, ground


def clean_set(tag):
    """The clean place at bench size, in the pen's half: the heap where the
    ashes are poured out, wood on it, the whole bull (the bundle) on the
    wood, and fire. Returns {part: El} (none shown yet)."""
    from leviticus17_art import ASH
    heap = add(El(f"s4.{tag}.heap", "bench", ART.heap(CP_X, CP_G, 250, 52, col=ASH), z=26,
                  hidden0=True))
    wy = CP_G - 50
    wood = "".join(B.slab(CP_X - 96 + i * 66, wy - 10 * r, CP_X - 96 + i * 66 + 60, wy - 10 * r + 10,
                          mix(PANEL, GT.ACACIA, .75), GT.ACACIA, 3)
                   for r, row in enumerate((3, 2)) for i in range(row) if r == 0 or i < 2)
    wood = add(El(f"s4.{tag}.wood", "bench", wood, z=27, hidden0=True))
    by0, by1 = wy - 52, wy - 18
    bundle = (B.slab(CP_X - 74, by0, CP_X + 74, by1, P.MEAT, TEXT, 12)
              + "".join(f'<line x1="{f2(CP_X + dx)}" y1="{f2(by0 + 2)}" x2="{f2(CP_X + dx)}" '
                        f'y2="{f2(by1 - 2)}" stroke="{rgb(TEXT)}" stroke-width="1.4"/>'
                        for dx in (-44, 0, 44)))
    bundle = add(El(f"s4.{tag}.bundle", "bench", bundle, z=28, hidden0=True))
    xs = [CP_X - 60, CP_X - 30, CP_X, CP_X + 30, CP_X + 60]
    fire = add(El(f"s4.{tag}.fire", "bench", ART.flames(xs, by0 + 6, [36, 50, 58, 48, 36]), z=29,
                  hidden0=True))
    return dict(heap=heap, wood=wood, bundle=bundle, fire=fire, fire_at=(CP_X, by0 + 6),
                heap_lead=(CP_X + 90, CP_G - 12), wood_lead=(CP_X + 96, wy - 4),
                bundle_box=(CP_X - 74, by0, CP_X + 74, by1))


def clean_fire(key, T, group, dur=0.6):
    cx, cy = S["clean"]
    el = add(El(key, "strip", ART.flames([cx - 9, cx, cx + 9], cy - 1, [12, 17, 12]), z=42))
    el.ev("in", T, dur, how="grow", about=(cx, cy - 1), group=group)
    return el


# ---------------------------------------------------------------------------
# The build
# ---------------------------------------------------------------------------

def build():
    E = B.ELS

    # the cast's drawings
    ox = P.Beast("bull", P.OX_X, G0, P.OX_K)
    ox_parts = F.ox()
    ox_line = F.outline(ox_parts, P.OX_X, G0, P.OX_K)
    head_ring = ox.outline("head")[0][0]
    goat = P.Beast("goat", GOAT_X, G0, GOAT_K)
    lamb = P.Beast("sheep", LAMB_X, G0, LAMB_BK)

    # the holy place set: the veil and the altar of incense (both laid out
    # once; shown for 4:5-7 and again for 4:16-18)
    veil = add(El("s4.hp.veil", "bench", ART.inset_svg("veil", HVK, HV_AT), z=16, hidden0=True))
    inc = add(El("s4.hp.incense", "bench", ART.inset_svg("incense", HNK, HN_AT), z=16,
                 hidden0=True))
    vr = VEIL_R
    veil_line = rect_pts(vr[0] - 4, vr[1] - 4, vr[2] + 4, vr[3] + 4)
    ib = INC_BOX
    inc_line = rect_pts(ib[0] - 8, ib[1] - 6, ib[2] + 8, ib[3] + 4)
    drops_line = rect_pts(DROPS_X[0] - 14, DROPS_Y - 12, DROPS_X[-1] + 14, DROPS_Y + 34)

    def drops(tag, T):
        """The seven drops before the veil, numbered, one by one."""
        els = []
        for i, x in enumerate(DROPS_X):
            ti = T + i * 0.3
            svg = (f'<circle cx="{f2(x)}" cy="{f2(DROPS_Y)}" r="6.5" fill="{rgb(BLOOD)}"/>'
                   + B.text(str(i + 1), x, DROPS_Y + 22, 14, TEXT, "mm"))
            el = add(El(f"s4.{tag}.drop{i}", "bench", svg, z=34,
                        texts=[(B.tbox(str(i + 1), x, DROPS_Y + 22, 14, "mm"), 14, "drop")]))
            el.ev("in", ti, 0.25, how="grow", about=(x, DROPS_Y), group=f"s4.{tag}.drops")
            els.append(el)
        return els

    def inc_horns(key, T, group):
        el = add(El(key, "bench", "".join(_poly(h, BLOOD) for h in INC_HORNS), z=34))
        el.ev("in", T, 0.5, group=group)
        return el

    # ================= the anointed priest (4:3-12) =========================

    # ---- 4:3  the sin column; the anointed priest; a young bull; sin offering
    D.switch("sin", at(4, 3, 0.0), name=False)
    t = cue(4, 3, "anointed priest")
    pr = Priest("s4.priest", ox.anchor["head"])
    pr.d.ev("in", t, 0.6, group="s4.who.priest")
    D.light("sin.who:the anointed priest", t, link=[("bench", pr.line(), True)],
            group="s4.who.priest")
    case1 = D.case_outline(["sin.who:the anointed priest"], t + 1.6, pad=1)
    t = cue(4, 3, "young bull")
    bull1 = P.figure_el("s4.bull1", ox_parts, P.OX_X, G0, P.OX_K, t, group="s4.icon.bull")
    D.light("sin.icon1:bull", t, link=[("bench", ox_line, True)], group="s4.icon.bull")
    D.light("sin.rank1", t, group="s4.icon.bull", pulse=False)
    D.name("sin", cue(4, 3, "sin offering"))

    # ---- 4:4  to the door; the hand on the head ------------------------
    t = cue(4, 4, "door")
    P.place("door", t, group="s4.door4")
    pulse_el("s4.bull1.door", "bench", ox_line, t, group="s4.door4")
    pr.hand(cue(4, 4, "hand"), group="s4.hand4")
    pulse_el("s4.bull1.head", "bench", head_ring, cue(4, 4, "head"))

    # ---- 4:5  the blood to the Tent of Meeting: its path; the holy place --
    t = cue(4, 5, "bring")
    path = P.route("door", "veil")
    path1 = traced_el("s4.path1", "strip", path, BLOOD, 3, t, 1.0, z=36)
    t = cue(4, 5, "Tent of Meeting")
    P.set_change(["s4.priest.reach", "s4.bull1"], ["s4.hp.veil", "s4.hp.incense"], t,
                 group="s4.hp5")

    # ---- 4:6  seven times before the veil ---------------------------------
    drops1 = drops("hp1", cue(4, 6, "seven times"))
    t = cue(4, 6, "veil")
    P.place("veil", t, dur=fit(t, 0.5), group="s4.veil6")
    chip_veil = P.bench_chip("s4.chip.veil", "veil", vr[2] + 16, vr[1] + 22, t, anchor="lm",
                             lead=(vr[2] + 1, vr[1] + 30), group="s4.veil6", dur=fit(t, 0.5))

    # ---- 4:7  the horns of the altar of incense; before the veil; the base -
    t = cue(4, 7, "horns")
    h1 = inc_horns("s4.hp1.horns", t, "s4.ih7")
    ih_chip = (ib[2] + 26, ib[1] - 30)
    P.bench_chip("s4.chip.ihorns", "horns", *ih_chip, t, lead=INC_HORNS[1][2], group="s4.ih7")
    t = cue(4, 7, "incense")
    P.place("incense", t, group="s4.inc7")
    pulse_el("s4.inc7.link", "bench", inc_line, t, group="s4.inc7")
    t = cue(4, 7, "before")
    D.light("sin.blood:before the veil", t, link=[("bench", drops_line, True)], group="s4.bv7")
    pool1 = base_el("s4.pool1", cue(4, 7, "base"), "s4.chip.base1", "s4.base7")

    # ---- 4:8  the bull opened: the fat that covers, the fat on the innards -
    t = cue(4, 8, "fat")
    hp_out = (["s4.hp.veil", "s4.hp.incense", "s4.hp1.horns", "s4.chip.veil", "s4.chip.ihorns",
               "s4.chip.base1"] + [e.key for e in drops1])
    P.set_change(hp_out, [], t, group="s4.set8")
    path1.ev("out", t, 0.6, group="s4.set8")
    P.cutaway(ox, "s4bull", t, group="s4.set8")
    chips = {}

    def part(beast, name, word, key, label, xy, T, out, tag):
        late = T + 0.95 > B.file_limit(T)            # no room for a pulse: the chip alone
        if not late:
            P.part_pulse(beast, name, key, T, group=f"s4.p{tag}{key}", tag=tag)
        chips[key] = P.bench_chip(f"s4.chip.{name}.{key}{tag}", label, *xy, T,
                                  lead=beast.anchor[key], out=out, group=f"s4.p{tag}{key}",
                                  out_dur=0.3, dur=fit(T, 0.5))

    t9 = cue(4, 9, "two kidneys")
    part(ox, "s4bull", "fat", "fat_cover", "fat that covers", (92, ROW_A),
         cue(4, 8, "fat that covers"), t9 - 0.35, "8")
    part(ox, "s4bull", "fat", "fat_on", "fat on the innards", (250, ROW_A),
         cue(4, 8, "fat", 2), t9 - 0.35, "8")

    # ---- 4:9  the two kidneys, the fat by the loins, the cover on the liver
    t10 = cue(4, 10, "taken")
    part(ox, "s4bull", "kidneys", "kidneys", "the two kidneys", (82, ROW_A), t9, t10, "9")
    part(ox, "s4bull", "fat", "kidney_fat", "fat by the loins", (246, ROW_A),
         cue(4, 9, "fat"), t10, "9")
    part(ox, "s4bull", "liver", "liver_cover", "cover on the liver", (164, ROW_B),
         cue(4, 9, "liver"), t10, "9")

    # ---- 4:10  taken from it onto the wood; burned: the fat ----------------
    P.to_wood(ox, "s4bull", {"fat": ox.anchor["fat"]}, t10, ["fat"])
    for k_ in ("kidneys", "liver_cover"):
        E[f"cut.s4bull.{k_}"].ev("dim", t10, 0.6, to=0.35, group="wood.s4bull")
    t = cue(4, 10, "burn")
    P.flare(t, 1.3, 0.75, group="s4.burn10")
    sb = P.slot_box(0)
    D.fly("the fat", (sb[0] - 6, sb[1] - 16), "sin.burns:the fat|a bull", t, T_go=t + 0.75)

    # ---- 4:11  the skin, all its meat, head, legs, innards, dung ------------
    slots11 = [(80, ROW_A), (240, ROW_A), (160, ROW_B)]
    words11 = [("skin", "skin", "skin"), ("meat", "meat", "all its meat"),
               ("head", "head", "head"), ("legs", "legs", "legs"),
               ("innards", "innards", "innards"), ("dung", "dung", "its dung")]
    t12 = cue(4, 12, "carry")
    ts = [cue(4, 11, w) for w, _k, _l in words11]
    for i, (w, key, label) in enumerate(words11):
        out = ts[i + 3] - 0.35 if i + 3 < len(ts) else None
        part(ox, "s4bull", w, key, label, slots11[i % 3], ts[i], out, "11")

    # ---- 4:12  carried out of the camp to a clean place; burned there --------
    clear(t12, "s4.carry12")
    bundle1 = carcass("s4.carry1", t12, "s4.carry12")
    t = cue(4, 12, "outside of the camp")
    carry_out(bundle1, t, "s4.walk12")
    P.place("camp", cue(4, 12, "camp"), group="s4.walk12")
    P.place("clean", cue(4, 12, "clean place"), group="s4.walk12")
    cp1 = clean_set("cp1")
    t = cue(4, 12, "ashes")
    cp1["heap"].ev("in", t, 0.6, group="s4.ash12")
    P.bench_chip("s4.chip.ashes12", "ashes", CP_X + 128, CP_G - 70, t, lead=cp1["heap_lead"],
                 group="s4.ash12")
    cp1["bundle"].ev("in", cue(4, 12, "burn"), 0.5, how="lift", lift=10)
    t = cue(4, 12, "wood")
    cp1["wood"].ev("in", t, 0.4, group="s4.wood12")
    P.bench_chip("s4.chip.wood12", "wood", CP_X + 128, CP_G - 104, t, lead=cp1["wood_lead"],
                 group="s4.wood12")
    t = cue(4, 12, "fire")
    cp1["fire"].ev("in", t, 0.8, how="grow", about=cp1["fire_at"], group="s4.fire12")
    fire1 = clean_fire("s4.fire1", t, "s4.fire12")
    land = D.fly("the bull: outside the camp", (488, 178),
                 "sin.not_eaten:the bull: outside the camp", t + 0.9)
    t = cue(4, 12, "burned")
    assert t >= land + 0.3, (B.local(t), B.local(land))
    clear(t, "s4.out12", regions=("bench", "strip"))

    # ================= the whole congregation (4:13-21) =======================

    # ---- 4:13  the whole congregation ----------------------------------------
    t = cue(4, 13, "whole congregation")
    man_def = B.define("s4_man", B.fig(F.man(), 0, 0, 0.85, TEXT, PANEL))
    xs = [44, 104, 164, 224, 284]
    crowd = add(El("s4.crowd", "bench", "".join(B.use(man_def, x, P.PEN_BACK_G) for x in xs),
                   z=18))
    crowd.ev("in", t, 0.6, group="s4.who.cong")
    crowd_line = rect_pts(xs[0] - 20, P.PEN_BACK_G - 88, xs[-1] + 20, P.PEN_BACK_G + 3)
    D.light("sin.who:the whole congregation", t, link=[("bench", crowd_line, True)],
            group="s4.who.cong")
    D.light("sin.rank1", t + 0.3, group="s4.who.cong")
    case1.ev("out", t + 1.4, 0.35)
    case2 = D.case_outline(["sin.who:the whole congregation"], t + 1.4, pad=1)

    # ---- 4:14  a young bull; before the Tent of Meeting ----------------------
    t = cue(4, 14, "young bull")
    bull2 = P.figure_el("s4.bull2", ox_parts, P.OX_X, G0, P.OX_K, t, group="s4.icon14")
    D.light("sin.icon1:bull", t, link=[("bench", ox_line, True)], group="s4.icon14")
    t = cue(4, 14, "before")
    P.place("door", t, group="s4.door14")
    pulse_el("s4.bull2.door", "bench", ox_line, t, group="s4.door14")

    # ---- 4:15  the elders lay their hands on its head --------------------------
    t = cue(4, 15, "elders")
    e1 = Person("s4.elder1", ox.anchor["head"])
    e2 = Person("s4.elder2", ox.anchor["head"], k=MAN_K * 0.92, dx=15 - 34, gy=G0 - 7, z=21)
    crowd.ev("out", t, 0.6, group="s4.elders")
    e1.come(t, "s4.elders")
    e2.come(t, "s4.elders")
    chip_eld = P.bench_chip("s4.chip.elders", "elders", e1.x - 34, ROW_B - 4, t,
                            lead=(e1.x - 30, G0 - 186), group="s4.elders")
    t = cue(4, 15, "hands")
    e1.hand(t, "s4.hands15")
    e2.hand(t, "s4.hands15")
    pulse_el("s4.bull2.head", "bench", head_ring, cue(4, 15, "head"))

    # ---- 4:16  the blood to the Tent of Meeting; the holy place ---------------
    t = cue(4, 16, "bring")
    path2 = traced_el("s4.path2", "strip", path, BLOOD, 3, t, 1.0, z=36)
    t = cue(4, 16, "bull")
    D.light("sin.blood:before the veil/who", t, link=[("strip", path, False)], group="s4.hp16")
    t = cue(4, 16, "Tent of Meeting")
    P.set_change(["s4.bull2", "s4.elder1.reach", "s4.elder2.reach", "s4.chip.elders"],
                 ["s4.hp.veil", "s4.hp.incense"], t, group="s4.hp16")

    # ---- 4:17  seven times before the veil -------------------------------------
    drops2 = drops("hp2", cue(4, 17, "seven"))
    t = cue(4, 17, "veil")
    P.bench_chip("s4.chip.veil2", "veil", vr[2] + 16, vr[1] + 22, t, anchor="lm",
                 lead=(vr[2] + 1, vr[1] + 30), group="s4.veil17", dur=fit(t, 0.4))

    # ---- 4:18  the horns of the altar in the Tent; the base -----------------------
    t = cue(4, 18, "horns")
    inc_horns("s4.hp2.horns", t, "s4.ih18")
    P.bench_chip("s4.chip.ihorns2", "horns", *ih_chip, t, lead=INC_HORNS[1][2], group="s4.ih18")
    t = cue(4, 18, "Tent of Meeting")
    P.place("incense", t, group="s4.inc18")
    pulse_el("s4.inc18.link", "bench", inc_line, t, group="s4.inc18")
    base_el("s4.pool2", cue(4, 18, "base"), "s4.chip.base2", "s4.base18")
    t = cue(4, 18, "door")
    hp_out = (["s4.hp.veil", "s4.hp.incense", "s4.hp2.horns", "s4.chip.veil2",
               "s4.chip.ihorns2", "s4.chip.base2"] + [e.key for e in drops2])
    P.set_change(hp_out, ["s4.bull2"], t, group="s4.set18")
    path2.ev("out", t, 0.6, group="s4.set18")

    # ---- 4:19  all its fat on the fire: the bull opens, as the priest's did -------
    t = cue(4, 19, "All its fat")
    bull2.ev("out", t, 0.6, group="s4.fat19")
    cut2 = P.cutaway(ox, "s4bull2", t, group="s4.fat19")
    P.part_pulse(ox, "s4bull2", "fat", t + 0.1, group="s4.fat19")
    P.bench_chip("s4.chip.fat19", "all its fat", ox.anchor["fat"][0] - 40, 363 - 26, t,
                 lead=ox.anchor["fat"],
                 out=cue(4, 19, "take"), group="s4.fat19", out_dur=0.3)
    fat2 = P.to_wood(ox, "s4bull2", {"fat": ox.anchor["fat"]}, cue(4, 19, "take"), ["fat"])[0]
    t = cue(4, 19, "burn")
    P.flare(t, 1.3, 0.8, group="s4.burn19")
    D.light("sin.burns:the fat|a bull", t, group="s4.burn19")

    # ---- 4:20  as with the bull of the sin offering; forgiven ---------------------
    D.pulse("sin.who:the anointed priest", cue(4, 20, "as he did"))
    D.pulse("sin.who:the whole congregation", cue(4, 20, "with this"))
    D.forgiven("sin", cue(4, 20, "forgiven"))

    # ---- 4:21  carried out and burned as the first --------------------------------
    t = cue(4, 21, "carry")
    P.outs(cut2 + [fat2], t, 0.6, group="s4.carry21")
    E["s4.pool2"].ev("out", t, 0.6, group="s4.carry21")
    bundle2 = carcass("s4.carry2", t, "s4.carry21")
    t = cue(4, 21, "outside the camp")
    carry_out(bundle2, t, "s4.walk21")
    P.place("camp", cue(4, 21, "camp"), group="s4.walk21")
    t = max(cue(4, 21, "burned"), cue(4, 21, "outside the camp") + 2.05)
    cp2 = clean_set("cp2")
    for k_ in ("heap", "wood", "bundle"):
        cp2[k_].ev("in", t, 0.6, group="s4.fire21")
    cp2["fire"].ev("in", t, 0.8, how="grow", about=cp2["fire_at"], group="s4.fire21")
    fire2 = clean_fire("s4.fire2", t, "s4.fire21")
    D.light("sin.not_eaten:the bull: outside the camp", cue(4, 21, "first bull"),
            group="s4.nb21")
    t = cue(4, 21, "sin offering")
    for el in (bundle2, fire2):
        el.ev("out", t, 0.8, group="s4.clear21")
    case2.ev("out", t, 0.35, group="s4.clear21")
    clear(t, "s4.clear21", regions=("bench", "strip"))

    # ================= a ruler (4:22-26) ============================================

    # ---- 4:22  a ruler ---------------------------------------------------------------
    t = cue(4, 22, "ruler")
    ruler = Person("s4.ruler", goat.anchor["head"], pose=ART.C_POSE["goat"])
    ruler.come(t, "s4.who.ruler")
    D.light("sin.who:a ruler", t, link=[("bench", ruler.line(), True)], group="s4.who.ruler")
    case3 = D.case_outline(["sin.who:a ruler", "sin.rank2", "sin.icon2:male goat"], t + 1.4,
                           pad=2)

    # ---- 4:23  a goat, a male --------------------------------------------------------
    t = cue(4, 23, "goat")
    g_parts = F.goat()
    g_line = F.outline(g_parts, GOAT_X, G0, GOAT_K)
    goat1 = P.figure_el("s4.goat1", g_parts, GOAT_X, G0, GOAT_K, t, group="s4.icon.goat")
    D.light("sin.icon2:male goat", t, link=[("bench", g_line, True)], group="s4.icon.goat")
    t = cue(4, 23, "male")
    D.light("sin.rank2", t, group="s4.icon.goat")
    P.bench_chip("s4.chip.male23", "male", GOAT_X + 20, G0 + 21, t, group="s4.icon.goat")
    g_head = goat.outline("head")[0][0]

    # ---- 4:24  the hand on its head; killed where the burnt offering is killed --------
    ruler.hand(cue(4, 24, "hand"), "s4.hand24")
    pulse_el("s4.goat1.head", "bench", g_head, cue(4, 24, "head"))
    t = cue(4, 24, "place")
    P.place("north", t, group="s4.north24")
    pulse_el("s4.goat1.north", "bench", g_line, t, group="s4.north24")

    # ---- 4:25  the horns of the altar of burnt offering; the base --------------------
    t = cue(4, 25, "horns")
    horns_el("s4.r.horns", t, "s4.horns25", "s4.chip.horns25")
    lh = A_HORNS[0]
    D.fly("on the altar's horns", (lh[0][0] - 8, lh[0][1] - 18),
          "sin.blood:on the altar's horns", t + 0.6)
    base_el("s4.r.pool", cue(4, 25, "base"), "s4.chip.base25", "s4.base25")

    # ---- 4:26  all its fat burned: the fat; forgiven ---------------------------------
    t = cue(4, 26, "All its fat")
    fat3 = fat_slab("s4.fat3", goat.anchor["fat"], t, "s4.fat26")
    P.bench_chip("s4.chip.fat26", "all its fat", goat.anchor["fat"][0] - 40, 377 - 26, t,
                 lead=goat.anchor["fat"],
                 out=cue(4, 26, "burn"), group="s4.fat26", out_dur=0.3)
    t_end = to_wood(fat3, cue(4, 26, "burn"), "s4.fat26w")
    P.flare(t_end + 0.05, 1.3, 0.8, group="s4.burn26")
    sb = P.slot_box(1)
    D.fly("the fat", (sb[0] - 6, sb[1] - 16), "sin.burns:the fat|a goat or a lamb",
          t_end + 0.05, T_go=t_end + 0.85)
    t = cue(4, 26, "atonement")
    case3.ev("out", t, 0.35, group="s4.clear26")
    clear(t, "s4.clear26", regions=("bench", "strip"))
    D.forgiven("sin", cue(4, 26, "forgiven"))

    # ================= one of the common people (4:27-31) ===========================

    # ---- 4:27  one of the common people --------------------------------------------
    t = cue(4, 27, "common people")
    fg_parts = F.goat(female=True)
    fg_line = F.outline(fg_parts, GOAT_X, G0, GOAT_K)
    person = Person("s4.person", goat.anchor["head"], pose=ART.C_POSE["fgoat"])
    person.come(t, "s4.who.common")
    D.light("sin.who:one of the common people", t, link=[("bench", person.line(), True)],
            group="s4.who.common")
    case4 = D.case_outline(["sin.who:one of the common people", "sin.icon3:female goat",
                            "sin.rank3"], t + 1.4, pad=2)

    # ---- 4:28  a goat, a female --------------------------------------------------------
    t = cue(4, 28, "goat")
    P.figure_el("s4.goat2", fg_parts, GOAT_X, G0, GOAT_K, t)
    t = cue(4, 28, "female")
    D.light("sin.icon3:female goat", t, link=[("bench", fg_line, True)], group="s4.female28")
    P.bench_chip("s4.chip.female28", "female", GOAT_X + 20, G0 + 21, t, group="s4.female28")

    # ---- 4:29  the hand; killed in the place of burnt offering ----------------------
    person.hand(cue(4, 29, "hand"), "s4.hand29")
    pulse_el("s4.goat2.head", "bench", g_head, cue(4, 29, "head"))
    t = cue(4, 29, "place")
    P.place("north", t, group="s4.north29")
    pulse_el("s4.goat2.north", "bench", fg_line, t, group="s4.north29")

    # ---- 4:30  the horns; the base ------------------------------------------------------
    t = cue(4, 30, "horns")
    horns_el("s4.c.horns", t, "s4.horns30", "s4.chip.horns30")
    D.light("sin.blood:on the altar's horns/who", t,
            link=[("bench", h, True) for h in A_HORNS], group="s4.horns30")
    D.light("sin.blood:on the altar's horns", t, group="s4.horns30")
    base_el("s4.c.pool", cue(4, 30, "base"), "s4.chip.base30", "s4.base30")

    # ---- 4:31  all its fat; burned; a pleasant aroma; forgiven ------------------------
    t = cue(4, 31, "All its fat")
    fat4 = fat_slab("s4.fat4", goat.anchor["fat"], t, "s4.fat31")
    P.bench_chip("s4.chip.fat31", "all its fat", goat.anchor["fat"][0] - 40, 377 - 26, t,
                 lead=goat.anchor["fat"],
                 out=cue(4, 31, "burn"), group="s4.fat31", out_dur=0.3)
    t_end = to_wood(fat4, cue(4, 31, "burn"), "s4.fat31w")
    P.flare(t_end + 0.05, 1.3, 0.8, group="s4.burn31")
    D.light("sin.burns:the fat|a goat or a lamb", t_end + 0.05, group="s4.burn31")
    t = cue(4, 31, "pleasant aroma")
    P.bench_chip("s4.chip.aroma31", "pleasant aroma", P.FIRE_C[0], P.A_TOP - 96, t,
                 group="s4.burn31")
    t = cue(4, 31, "atonement")
    case4.ev("out", t, 0.35, group="s4.clear31")
    clear(t, "s4.clear31", regions=("bench", "strip"))
    D.forgiven("sin", cue(4, 31, "forgiven"))

    # ================= a lamb (4:32-35) ============================================

    # ---- 4:32  a lamb; a female ----------------------------------------------------------
    t = cue(4, 32, "lamb")
    l_parts = F.sheep(lamb=True)
    l_line = F.outline(l_parts, LAMB_X, G0, LAMB_DRAW)
    P.figure_el("s4.lamb", l_parts, LAMB_X, G0, LAMB_DRAW, t, group="s4.icon.lamb")
    D.light("sin.icon3:lamb", t, link=[("bench", l_line, True)], group="s4.icon.lamb")
    D.light("sin.who:one of the common people", t, group="s4.icon.lamb")
    case5 = D.case_outline(["sin.who:one of the common people", "sin.icon3:lamb", "sin.rank3"],
                           t + 1.4, pad=2)
    t = cue(4, 32, "female")
    D.light("sin.rank3", t, group="s4.female32")
    P.bench_chip("s4.chip.female32", "female", LAMB_X + 14, G0 + 21, t, group="s4.female32")

    # ---- 4:33  the hand; killed where the burnt offering is killed ---------------------
    t = cue(4, 33, "hand")
    man5 = Person("s4.man5", lamb.anchor["head"], pose=ART.C_POSE["lamb"])
    man5.come(t, "s4.hand33", reach=True)
    pulse_el("s4.lamb.head", "bench", lamb.outline("head")[0][0], cue(4, 33, "head"))
    t = cue(4, 33, "place")
    P.place("north", t, group="s4.north33")
    pulse_el("s4.lamb.north", "bench", l_line, t, group="s4.north33")

    # ---- 4:34  the horns; the base --------------------------------------------------------
    t = cue(4, 34, "horns")
    horns_el("s4.l.horns", t, "s4.horns34", "s4.chip.horns34")
    D.light("sin.blood:on the altar's horns", t, link=[("bench", h, True) for h in A_HORNS],
            group="s4.horns34")
    base_el("s4.l.pool", cue(4, 34, "base"), "s4.chip.base34", "s4.base34")

    # ---- 4:35  all its fat, like the lamb's; burned by fire; forgiven ---------------------
    t = cue(4, 35, "All its fat")
    fat5 = fat_slab("s4.fat5", lamb.anchor["fat"], t, "s4.fat35")
    P.bench_chip("s4.chip.fat35", "all its fat", lamb.anchor["fat"][0] - 40, 438 - 26, t,
                 lead=lamb.anchor["fat"],
                 out=cue(4, 35, "burn"), group="s4.fat35", out_dur=0.3)
    t = cue(4, 35, "lamb")
    D.light("sin.burns:the fat|a goat or a lamb/who", t, link=[("bench", l_line, True)],
            group="s4.lamb35")
    to_wood(fat5, cue(4, 35, "burn"), "s4.fat35w")
    t = cue(4, 35, "fire")
    t_at = cue(4, 35, "atonement")
    P.flare(t, 1.3, 0.9, group="s4.fire35")
    D.light("sin.burns:the fat|a goat or a lamb", t, group="s4.fire35", steady_out=t_at - 0.45)
    case5.ev("out", t_at, 0.35, group="s4.end")
    clear(t_at, "s4.end", regions=("bench", "strip"), dock=True)
    D.forgiven("sin", cue(4, 35, "forgiven"))
