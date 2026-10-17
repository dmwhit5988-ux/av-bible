# -*- coding: utf-8 -*-
"""Layout lab: does a different tree layout remove the wide shots?

The question (user, 2026-08-20): the wall-chart layout was designed for a
wall chart. Now that the same sheet is the world for two per-verse camera
readings — 1 Chronicles 1-9 and Matthew 1 — is it the wrong shape, and would
a different one let the camera stay at reading scale?

WHAT THE CURRENT LAYOUT DOES. `generate_ot_family_tree_svg.arrange/place` is
a classic tidy tree: every subtree gets a slot as wide as itself, and a
parent is centred over the whole span of its descendants. Measured on the
real sheet, that means:

    median parent->child horizontal offset      50 px
    75th percentile                            162 px
    99th percentile                          8,278 px
    max                    9,697 px  (Eve, from Adam)

So three quarters of the tree is already tight and the damage is all in the
tail — and the tail is at the TOP of the tree, where a node's children each
carry an enormous subtree: Shem's 9 children span 17,685 px, Abraham's 5
span 15,221, Israel's 18 span 12,099. A node's x encodes how many
descendants it has, not anything about the node.

THE VARIANTS MEASURED HERE. Each is a drop-in replacement for arrange/place.

    V0  current            parent centred over the span of all descendants
    V1  spine              parent sits over its FIRST child, so any chain of
                           single children is a straight vertical line
    V2  spine + packing    V1, and consecutive LIGHT children (no descendants
                           to speak of) are packed into a compact grid block
                           instead of each taking a full-width slot. Birth
                           order is preserved — the block reads left to
                           right, top to bottom, like a paragraph of names.
    V3  V2 + heavy last    V2, but each family's heavy children are moved to
                           the end so the parent sits against the compact
                           side. BREAKS BIRTH ORDER; measured to find out
                           what order is worth.

The score is the only thing that matters: what fraction of the 334 named
verses of 1 Chronicles 1-9, and the 17 of Matthew 1, fit in one frame at
reading scale (0.52) — because a verse that fits needs no wide shot, no
veil, no card and no dropped name.

    python tools/layout_lab.py
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import generate_ot_family_tree_svg as OT
from generate_ot_family_tree_svg import (ASPECT, DROP, ROW_GAP, SIB_GAP,
                                         SPINE, measure)

READABLE = 0.52
VIEW_W, VIEW_H = 1024, 530          # the camera's viewport, minus the HUD
PAD = 70

LIGHT = 260         # a child whose whole subtree is no wider than this is
                    # "light": a name, or a name with a couple under it
GRID_W = 1500       # how wide a packed block of light children may run


# ---------------------------------------------------------------------------
# V1 / V2 / V3
# ---------------------------------------------------------------------------

def _runs(kids, pack):
    """Split a family into consecutive runs of light and heavy children.

    Consecutive is the point: keeping the runs in order is what lets a
    packed block preserve birth order. -> [(is_light, [kid, ...]), ...]
    """
    out = []
    for k in kids:
        light = pack and k.sw <= LIGHT
        if out and out[-1][0] == light:
            out[-1][1].append(k)
        else:
            out.append((light, [k]))
    return out


def _grid(run):
    """Lay a run of light children into rows no wider than GRID_W.
    -> (rows, width, height)."""
    rows, row, w = [], [], 0.0
    for k in run:
        step = k.sw + (SIB_GAP if row else 0)
        if row and w + step > GRID_W:
            rows.append(row)
            row, w, step = [], 0.0, k.sw
        row.append(k)
        w += step
    if row:
        rows.append(row)

    def row_w(r):
        return sum(k.sw for k in r) + SIB_GAP * (len(r) - 1)

    return (rows, max(row_w(r) for r in rows),
            sum(max(k.sh for k in r) for r in rows)
            + ROW_GAP * (len(rows) - 1))


PLAN = {}       # id(node) -> [(kind, payload)]; N has __slots__, so the
                # plan cannot live on the node


def arrange_v(n, notes=True, pack=True, heavy_last=False, heir_first=False):
    """Bottom-up footprint. PLAN[id(n)] is the recipe for `place_v`.

    Same wrapping rule as the live layout — a family too wide to sit in one
    row breaks into rows under a left rail — because dropping it was not a
    layout variant, it was a bug: with every family forced into one row the
    sheet came out 263,000 px wide and scored WORSE than the thing it was
    meant to beat. What varies here is only what the variants claim to vary:
    where the parent stands, and whether runs of leaf children get packed.
    """
    measure(n, notes)
    for k in n.kids:
        arrange_v(k, notes, pack, heavy_last, heir_first)
    n.rows = []
    plan = PLAN[id(n)] = []
    if not n.kids:
        n.sw, n.sh = n.w, n.h
        return n

    kids = list(n.kids)
    if heir_first and len(kids) > 1:
        # The HEIR — the child carrying the biggest descent — goes directly
        # under the parent, and the rest pack alongside. This is the one
        # arrangement that can beat the geometry on a verse like 1:17
        # (Shem and all nine of his sons): Arpachshad's subtree is the rest
        # of the Bible, so wherever else he is put, his own node sits at
        # the centre of 17,000 px and the verse cannot close. Under his
        # father he is at zero, and his eight brothers pack beside him.
        heir = max(kids, key=lambda k: k.sw)
        kids = [heir] + [k for k in kids if k is not heir]
    if heavy_last:
        # stable: light ones keep their order, heavy ones keep theirs, and
        # the light block comes first so the parent stands against it
        light_first = [k for k in kids if k.sw <= LIGHT and not k.kids]
        kids = light_first + [k for k in kids if k not in light_first]

    # One ITEM per thing that has to be placed: a single child, or a packed
    # block of consecutive leaf children.
    items = []
    for light, run in _runs(kids, pack):
        if light and len(run) > 1:
            rows, gw, gh = _grid(run)
            items.append(("grid", rows, gw, gh, run[0]))
        else:
            for k in run:
                items.append(("one", k, k.sw, k.sh, k))

    flat = sum(i[2] for i in items) + SIB_GAP * (len(items) - 1)
    widest = max(i[2] for i in items)
    area = sum((i[2] + SIB_GAP) * i[3] for i in items)
    cap = max(widest, math.sqrt(area * ASPECT))
    if flat <= cap * 1.05:
        bands = [list(items)]
    else:
        bands, band, bw = [], [], 0.0
        for i in items:
            step = i[2] + (SIB_GAP if band else 0)
            if band and bw + step > cap:
                bands.append(band)
                band, bw = [i], i[2]
            else:
                band.append(i)
                bw += step
        if band:
            bands.append(band)

    def band_w(b):
        return sum(i[2] for i in b) + SIB_GAP * (len(b) - 1)

    for b in bands:
        plan.append(b)
    # `draw_edges` on the wall chart walks n.rows, so give it one: with
    # packing off (which is V6) every item is a single child and the bands
    # ARE the rows. That is what lets the whole sheet render under a
    # variant layout without touching the drawing code.
    n.rows = [[i[1] for i in b if i[0] == "one"] for b in bands]
    n.rows = [r for r in n.rows if r]
    block_w = max(band_w(b) for b in bands)
    if len(bands) > 1:
        block_w += SPINE
    n.sw = max(n.w, block_w)
    n.sh = (n.h + DROP + sum(max(i[3] for i in b) for b in bands)
            + ROW_GAP * (len(bands) - 1))
    return n


def place_v(n, cx, top, spine=True):
    """Absolute positions. With `spine`, the parent sits over its FIRST
    child instead of over the centre of everything below it.

    That is the whole of V1. In the live layout a parent's x is the centre
    of its entire descent, so a father with one huge son and one small one
    stands between two subtrees and is next to neither — and a chain of
    single children zig-zags, because each link is re-centred over a
    different amount of progeny. Standing him over the first thing he begot
    makes a chain a straight column, which is what a genealogy mostly is.
    """
    n.x = cx - n.w / 2
    n.y = top
    if not n.kids:
        return
    bands = PLAN[id(n)]
    y = top + n.h + DROP
    block_w = n.sw
    if spine:
        head = bands[0][0]
        left = cx - head[2] / 2
    else:
        left = cx - block_w / 2 + (SPINE if len(bands) > 1 else 0)

    for b in bands:
        x = left if spine or len(bands) > 1 else cx - band_w_of(b) / 2
        for kind, payload, iw, ih, _head in b:
            if kind == "one":
                place_v(payload, x + iw / 2, y, spine)
            else:
                ry = y
                for r in payload:
                    rx = x
                    for k in r:
                        place_v(k, rx + k.sw / 2, ry, spine)
                        rx += k.sw + SIB_GAP
                    ry += max(k.sh for k in r) + ROW_GAP
            x += iw + SIB_GAP
        y += max(i[3] for i in b) + ROW_GAP


def band_w_of(b):
    return sum(i[2] for i in b) + SIB_GAP * (len(b) - 1)


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def fit_scale(nodes):
    x0 = min(n.x for n in nodes)
    y0 = min(n.y for n in nodes)
    x1 = max(n.x + n.w for n in nodes)
    y1 = max(n.y + n.h for n in nodes)
    w, h = max(x1 - x0, 1.0) + 2 * PAD, max(y1 - y0, 1.0) + 2 * PAD
    return min(VIEW_W / w, VIEW_H / h, 1.25)


def score(label, root, verse_sets, nodes):
    ok = sum(1 for s in verse_sets if fit_scale(s) >= READABLE)
    xs0 = min(n.x for n in nodes)
    xs1 = max(n.x + n.w for n in nodes)
    ys0 = min(n.y for n in nodes)
    ys1 = max(n.y + n.h for n in nodes)
    edges = [abs((n.x + n.w / 2) - (n.parent.x + n.parent.w / 2))
             for n in nodes if n.parent is not None]
    edges.sort()
    return dict(label=label, ok=ok, total=len(verse_sets),
                pct=100.0 * ok / max(len(verse_sets), 1),
                w=xs1 - xs0, h=ys1 - ys0,
                med=edges[len(edges) // 2],
                p90=edges[int(len(edges) * 0.90)],
                p99=edges[int(len(edges) * 0.99)])


def main():
    import chronicles_tree as CT
    import matthew_tree as MT
    from chronicles_tree import walk
    from generate_1chronicles import CHAPTERS, assign, web_verses

    # Build both worlds' verse->rows mapping ONCE, off node identity, so
    # every layout is scored on exactly the same sets of people.
    def chron_sets(tree):
        from svg_chronicles_world import World
        return None

    PLAN.clear()
    variants = [
        ("V0 current      ", lambda r: (OT.arrange(r, notes=False),
                                        OT.place(r, 0, 0))),
        ("V1 spine        ", lambda r: (arrange_v(r, False, pack=False),
                                        place_v(r, 0, 0, spine=True))),
        ("V2 spine+pack   ", lambda r: (arrange_v(r, False, pack=True),
                                        place_v(r, 0, 0, spine=True))),
        ("V3 pack, centred", lambda r: (arrange_v(r, False, pack=True),
                                        place_v(r, 0, 0, spine=False))),
        ("V4 V2+heavy last", lambda r: (arrange_v(r, False, pack=True,
                                                  heavy_last=True),
                                        place_v(r, 0, 0, spine=True))),
        ("V5 heir under dad", lambda r: (arrange_v(r, False, pack=True,
                                                   heir_first=True),
                                         place_v(r, 0, 0, spine=True))),
        ("V6 heir, no pack ", lambda r: (arrange_v(r, False, pack=False,
                                                   heir_first=True),
                                         place_v(r, 0, 0, spine=True))),
    ]

    print("=" * 78)
    print("1 CHRONICLES 1-9   (334 verses that name somebody)")
    print("=" * 78)
    rows = []
    for label, lay in variants:
        import svg_chronicles_world as CW
        w = CW.World.__new__(CW.World)
        w.tree = CT.build(ot=True)
        w.root = w.tree.root
        lay(w.root)
        w.by_src = {}
        for n in walk(w.root):
            if n.src is not None:
                w.by_src[n.src] = n
        w.nodes = list(walk(w.root))
        w.world_box = (min(n.x for n in w.nodes), min(n.y for n in w.nodes),
                       max(n.x + n.w for n in w.nodes),
                       max(n.y + n.h for n in w.nodes))
        w.order, w.arrivals, w.lit, w.first_of = [], {}, {}, {}
        w._read_scenes()
        sets = [v for v in (w.lit.get(k) for k in
                            [(c, vv) for c, vv, _s in w.order]) if v]
        rows.append(score(label, w.root, sets, w.nodes))
    _table(rows)

    print()
    print("=" * 78)
    print("MATTHEW 1:1-17")
    print("=" * 78)
    rows = []
    for label, lay in variants:
        tree, at = MT.build()
        lay(tree.root)
        nodes = list(walk(tree.root))
        line = MT.MatthewLine(tree, at)
        sets = [line.lit[v] for v, _n in MT.READING]
        rows.append(score(label, tree.root, sets, nodes))
    _table(rows)


def _table(rows):
    print(f"{'layout':18} {'fit at reading scale':>22}  {'sheet':>17}  "
          f"{'parent->child offset':>26}")
    print(f"{'':18} {'':>22}  {'':>17}  "
          f"{'median':>8}{'p90':>9}{'p99':>9}")
    for r in rows:
        print(f"{r['label']:18} {r['ok']:5d}/{r['total']:<4d} "
              f"({r['pct']:5.1f}%)      "
              f"{r['w']/1000:6.1f}k x{r['h']/1000:6.1f}k  "
              f"{r['med']:8.0f}{r['p90']:9.0f}{r['p99']:9.0f}")


if __name__ == "__main__":
    main()
