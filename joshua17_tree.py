"""Zelophehad's daughters (Joshua 17:2-5) as a scene card the camera dives
into: Manasseh's branch of the Old Testament family tree, with a bare stage
under it.

The branch is the one the listener met in 1 Chronicles 7, lifted out whole:
the reading world's own boxes where they stand (svg_chronicles_world.World,
the regions layout, names only), its own lines (svg_family_lines) and its
three looks (lit, read, ahead). Only the people Joshua 17:1-6 names are
boxes, with the forebear that joins them: Manasseh, Machir, Gilead, the six
clans (Abiezer, Helek, Asriel, Shechem, Hepher and Shemida), Zelophehad and
his five daughters, and Hammolecheth, under whom 1 Chronicles 7:18 hangs
Abiezer. No name is shown that the text doesn't say, except Hammolecheth,
the forebear who joins Abiezer. Everyone else in the branch stands as a
blank block over the boxes it hides, hung from its line the way 1
Chronicles shows a branch not read yet (svg_silhouettes): Maacah's sons
and theirs, the heads in Bashan and their house's name, Pedahzur and Susi,
the second Gilead and Jephthah, Shemida's sons, and Joash, Gideon and
Abimelech. As in 1 Chronicles, a block folds at least two boxes
(svg_silhouettes.MIN_FOLD), because a block the size of one box reads as an
empty name box. So whoever would stand alone in one is not drawn, and
neither is the line to him: Manasseh's and Machir's wives (the Aramitess
and Maacah), and Hammolecheth's other two, Ishhod and her Mahlah. Her line
runs straight down to Abiezer, and Maacah's sons hang from Machir's own
line, as his sons (1 Chronicles 7:16). No line runs to nothing. The tree
follows 1 Chronicles 7 and the wall chart, so Asriel is Manasseh's son and
Abiezer Hammolecheth's, and the six clans light on three rows.

The card hangs at the hill country of west Manasseh (gazetteer.REGIONS
['samaria']), which has no dot to dive from. Beat by beat:
- 17:2 the camera dives from Bashan, over the Jordan, into the hill country
  as "the rest of the children of Manasseh" is said, and the branch opens
  out of the land. Machir and Gilead stand read, because 17:1 named them,
  and Manasseh lights as the camera lands. As each clan is said, its own
  line from its parent draws itself and its box lights: Asriel from
  Manasseh, Abiezer from Hammolecheth, and Helek, Shechem, Hepher and
  Shemida from Gilead.
- 17:3 the clans let go as the camera moves onto Manasseh's line.
  Zelophehad lights, then Hepher, Gilead, Machir and Manasseh, each at its
  "son of". No line is drawn up the tree: the boxes light where they
  stand. At "had no sons" the camera comes down to him and the empty row
  under him. At "but daughters" his line draws down to five boxes, and
  each lights as she is named.
- 17:4 his forebears let go as the camera goes down to the stage under the
  tree. Five women come in under the daughters' boxes. They carry no names,
  because their names are the boxes. They walk to Eleazar the priest,
  Joshua and three princes, who come in as they are named. The first woman
  opens her arms at "saying", and Joshua raises his free hand at "he gave"
  (the staff is in his other one). The women walk back under their names,
  and the camera rises to the five lit boxes.
- 17:5 at "Ten parts" the camera rises to the ten who share the lot: the
  five other clans (Abiezer, Helek, Asriel, Shechem and Shemida), which
  light as it is said, and the five daughters, lit already. The text's own
  number, "10", stands among them, and the camera rises out of the card to
  the map.
What is inferred: the stage. 17:4 names no place, so none is drawn, and
there is no Tent of Meeting. Also inferred are the leaders' and the women's
figures, the princes' number, the women's walk, where the "10" stands, and
which ten the parts are: the six clans of 17:2 less Hepher, whose part
went to the daughters (17:3-4), and the five daughters.
generate_joshua1319_svg.py flies the camera; svg_scene_card.py draws the
card.

Card px are the tree's own (1 Chronicles' world px), with Manasseh's branch
from (0, 0). The stage's ground is at y 940, and a man is 110 px tall, so
a box is about a third of a man. Every rest keeps the tree's 15 px names at
13 px or more on screen (zoom 0.87 or closer), and shows the cast's names
whole (NAMES).
"""

import math

import svg_chronicles_world as SCW
import svg_family_lines as FL
import svg_figures as F
import svg_silhouettes as SIL
from chronicles_tree import walk
from generate_tabernacle import H, HL, SAND, TEXT, W
from svg_map_camera import fade, ink, rgb
from svg_scene_card import Actor, Card, person, static
from svg_surface import _fmt

S_CARD = 200                    # camera scale at the card's zoom 1, as in Acts
MAN = 110.0                     # a man, card px
GROUND = 940                    # the stage's ground line, card px
SKY = SCW.PANEL_BLEND           # 1 Chronicles' panel, behind the tree
EARTH = (34, 35, 29)            # the Acts and Shiloh cards' earth
ORIGIN = (-1100, -1000)         # the card's top left, and its size
SIZE = (4600, 3200)
ANCHOR = (790, 230)             # the card point hung on the region's point
NAME_PX = 15                    # the tree's names, world-scaled
MIN_NAME_PX = 13                # the least they may be on screen at a rest
FONT_PX = 18                    # the cast's names, screen px (the tour's)
# The zooms the leaders' names come in over: they hold a screen size while
# the figures shrink, so they go before the figures crowd them. Every rest
# that shows them is at NAMES[1] or closer.
NAMES = (0.75, 0.85)
# the leaders' names, one line over all three, clear of Joshua's staff tip
# (126 px up) and Eleazar's mitre
LABEL_Y = -(MAN + 34)
NAME_GAP = 6                    # screen px between two cast names
FIGURE_GAP = 6                  # and between a name and any figure's ink

DAUGHTERS = ["Mahlah", "Noah", "Hoglah", "Milcah", "Tirzah"]
CLANS = ["Abiezer", "Helek", "Asriel", "Shechem", "Hepher", "Shemida"]
# 17:5's ten parts: the clans but Hepher, whose part went to his son's
# daughters, and the daughters
OTHERS = [k for k in CLANS if k != "Hepher"]
CHAIN = ["Zelophehad", "Hepher", "Gilead", "Machir", "Manasseh"]
RANK = {"ahead": 0, "read": 1, "lit": 2}
LIGHT = 0.5                     # a box brightening
LET_GO = 0.8                    # a lit box going back to read
TRACE = 0.8                     # a line drawing itself from the parent
LEAD = 0.1                      # a beat starts this long before its word

# What 17:1 has already named, as 17:2 opens: read. Everyone else on the
# card stands faint, and the daughters' row is empty.
OPEN = dict({k: "ahead" for k in CLANS + ["Zelophehad", "Hammolecheth"]},
            Manasseh="read", Machir="read", Gilead="read")


class Branch:
    """Manasseh's branch of the 1 Chronicles reading world: the named boxes
    (by node, so the second Gilead, Shechem and Mahlah are never lit), the
    blocks the rest fold into, and the lines."""

    def __init__(self):
        w = SCW.World()
        self.geom = FL.Geometry(w.nodes, labels=w.plan.labels,
                                routes=w.plan.routes)
        man = next(n for n in w.nodes if n.label == "Manasseh"
                   and any(k.label == "Machir" for k in n.kids))
        self.all = list(walk(man))
        self.x0 = min(n.x for n in self.all)
        self.y0 = min(n.y for n in self.all)

        def kid(p, label):
            ks = [k for k in p.kids if k.label == label]
            assert len(ks) == 1, (p.label, label)
            return ks[0]
        machir = kid(man, "Machir")
        gilead = kid(machir, "Gilead")
        ham = kid(machir, "Hammolecheth")
        hepher = kid(gilead, "Hepher")
        zel = kid(hepher, "Zelophehad")
        self.node = {"Manasseh": man, "Machir": machir, "Gilead": gilead,
                     "Hammolecheth": ham, "Asriel": kid(man, "Asriel"),
                     "Abiezer": kid(ham, "Abiezer"),
                     "Helek": kid(gilead, "Helek"),
                     "Shechem": kid(gilead, "Shechem"), "Hepher": hepher,
                     "Shemida": kid(gilead, "Shemida"), "Zelophehad": zel}
        for d in DAUGHTERS:
            self.node[d] = kid(zel, d)
        self.key = {n: k for k, n in self.node.items()}
        self.kept = set(self.node.values())
        self.labels = set(w.plan.labels)
        # the lines that lead to a named box, each piece once
        segs, seen = [], set()
        for n in self.node.values():
            if n is man:
                continue            # his own line comes down from Joseph
            for s in self.geom.node_segments.get(n, ()):
                if id(s) not in seen:
                    seen.add(id(s))
                    segs.append(s)
        self.segs = segs
        self._seg_ids = seen
        self.blocks = self._fold()

    # -- card px ---------------------------------------------------------

    def box(self, key):
        n = self.node[key]
        return (n.x - self.x0, n.y - self.y0, n.x - self.x0 + n.w,
                n.y - self.y0 + n.h)

    def mid(self, key):
        x0, y0, x1, y1 = self.box(key)
        return (x0 + x1) / 2, (y0 + y1) / 2

    def card_rects(self):
        """Every box and block on the card, in card px."""
        dx, dy = self.x0, self.y0
        out = [self.box(k) for k in self.node]
        out += [(r[0] - dx, r[1] - dy, r[2] - dx, r[3] - dy)
                for r, _f, _l in self.blocks]
        return out

    # -- blocks ----------------------------------------------------------

    def _rect(self, folded):
        return (min(q.x for q in folded) - SIL.PAD,
                min(q.y for q in folded) - SIL.PAD_TOP,
                max(q.x + q.w for q in folded) + SIL.PAD,
                max(q.y + q.h for q in folded) + SIL.PAD)

    def _clear(self, rect, others):
        """A block's rect meets no named box, no line to one, and no other
        block."""
        e = SIL.INSET
        for n in self.kept:
            if SIL._meet(rect, (n.x, n.y, n.x + n.w, n.y + n.h), e):
                return False
        for s in self.segs:
            if any(SIL._line_in(ln, rect) for ln in FL._drawn_lines(s)):
                return False
        return not any(SIL._meet(rect, r, e) for r in others)

    def _boxes(self, fold):
        return sum(1 for q in fold if q not in self.labels)

    def _fold(self):
        """-> [(rect, folded nodes, the line into it)], world px. A wife
        beside a named man is her own block, joined by her marriage bar, and
        her children another under her; the other children of a named
        parent fold a branch each, and brothers' branches side by side
        share one block wherever it would cover nothing. A block holding
        all of a parent's children takes 1 Chronicles' one stem into its
        top (svg_silhouettes); one holding some of them, that family's
        drops, cut at its edge. A block that would fold fewer than
        svg_silhouettes.MIN_FOLD boxes is not drawn, nor its line: a block
        the size of one box reads as an empty box. Her children's block
        then hangs from her husband's own line."""
        groups = []                         # (parent, roots, kind)
        for p in sorted(self.kept, key=lambda n: (n.y, n.x)):
            kids = [k for k in p.kids if k not in self.kept]
            for k in [k for k in kids if SIL._beside(p, k)]:
                groups.append((p, [k], "wife"))
                if k.kids:
                    groups.append((k, list(k.kids), "kids"))
            rest = sorted((k for k in kids if not SIL._beside(p, k)),
                          key=lambda k: k.x)
            if rest:
                groups.append((p, rest, "kids"))
        out = []
        placed = []
        wives = set()                       # the wives whose block is drawn
        for p, roots, kind in groups:
            if kind == "wife":
                runs = [[roots[0]]]
            else:
                # brothers side by side, one block where it covers nothing
                runs = []
                for k in roots:
                    if runs:
                        trial = runs[-1] + [k]
                        fold = {q for r in trial for q in walk(r)}
                        if self._clear(self._rect(fold), placed):
                            runs[-1] = trial
                            continue
                    runs.append([k])
            for run in runs:
                fold = ({run[0]} if kind == "wife"
                        else {q for r in run for q in walk(r)})
                if self._boxes(fold) < SIL.MIN_FOLD:
                    continue
                rect = self._rect(fold)
                assert self._clear(rect, placed), (p.label, run[0].label)
                placed.append(rect)
                if kind == "wife":
                    wives.add(run[0])
                info = self.geom.families.get(p)
                whole = (kind == "kids" and info is not None
                         and set(info["below"]) == set(run))
                out.append((rect, frozenset(fold), (p, run, whole)))
        # each block's line in: one stem, or the family's own pieces, cut at
        # the blocks, each piece once
        rects = [r for r, _f, _l in out]

        def cut(s):
            pieces = [s]
            for r in rects:
                pieces = [c for q in pieces for c in SIL._clip_out(q, r)]
            return pieces
        blocks, seen = [], set()
        for rect, fold, (p, run, whole) in out:
            if whole and p not in self.kept and p not in wives:
                # her own block isn't drawn: from her husband's line
                lines = self._hang(p.parent, rect, run)
            elif whole:
                # 1 Chronicles' own stem into a block (it reads only
                # self.geom, which a Branch has too)
                lines = [c for s in SIL.Silhouettes._stubs(self, p, rect, fold)
                         for c in cut(s)]
            else:
                lines = []
                for k in run:
                    for s in self.geom.node_segments.get(k, ()):
                        if id(s) in self._seg_ids or id(s) in seen:
                            continue        # drawn already
                        seen.add(id(s))
                        lines += cut(s)
            blocks.append((rect, fold, lines))
        return blocks

    def _hang(self, man, rect, kids):
        """The line into a block of a man's sons by a wife whose own block
        isn't drawn: on along his family's bus from its nearer end, and down
        into the block's top, STUB_IN in from its side (svg_silhouettes'
        rule)."""
        bus = self.geom.families[man]["bus_y"]
        ends = [x for s in self.segs if s.fam is man and s.horizontal
                and abs(s.y0 - bus) < 1e-6 for x in (s.x0, s.x1)]
        pcx = man.x + man.w / 2
        lo, hi = rect[0] + SIL.STUB_IN, rect[2] - SIL.STUB_IN
        xc = min(max(pcx, lo), hi)
        if ends:
            pts = [(min(ends, key=lambda x: abs(x - xc)), bus)]
        else:
            pts = [(pcx, man.y + man.h), (pcx, bus)]
        pts += [(xc, bus), (xc, rect[1])]
        style = FL._shared_style(kids)
        return [FL.Seg(a[0], a[1], b[0], b[1], "stub", style, man,
                       frozenset(kids))
                for a, b in zip(pts, pts[1:])
                if abs(b[0] - a[0]) + abs(b[1] - a[1]) > 1e-6]


_BRANCH = None


def branch():
    global _BRANCH
    if _BRANCH is None:
        _BRANCH = Branch()
    return _BRANCH


# ---------------------------------------------------------------------------
# The beats: each verse's looks, from the one it opens on
# ---------------------------------------------------------------------------

def cue(say, ref, word, default, lead=LEAD):
    """When a beat answering `word` starts: just before it's said, or
    `default` (today's MP3) when there's no clock."""
    t = say(ref, word) if say else None
    return default if t is None else round(max(0.0, t - lead), 2)


def beats(say=None):
    """{ref: [(t, key, look, how)]}: a box takes `look` at t, by `how`:
    "light" (brightens over LIGHT), "let" (back to read over LET_GO),
    "trace" (its line from its parent draws itself over TRACE as it
    brightens) or "appear" (its line draws itself and the box comes in
    faint)."""
    out = {}
    land = sum(d for _k, _t, d in LEGS[(17, 2)])
    b2 = [(land, "Manasseh", "lit", "light")]
    defaults = dict(Abiezer=5.52, Helek=7.21, Asriel=8.8, Shechem=10.33,
                    Hepher=11.86, Shemida=13.54)
    for clan in CLANS:
        b2.append((max(land, cue(say, (17, 2), clan, defaults[clan])), clan,
                   "lit", "trace"))
    out[(17, 2)] = b2
    b3 = [(0.0, k, "read", "let") for k in ["Manasseh"] + CLANS]
    defaults = dict(Zelophehad=0.28, Hepher=1.89, Gilead=3.21, Machir=4.51,
                    Manasseh=5.85)
    # the recital climbs the tree: "But Zelophehad, the son of Hepher, the
    # son of Gilead, ..." (each name's first time in the verse)
    for k in CHAIN:
        b3.append((cue(say, (17, 3), k, defaults[k]), k, "lit", "light"))
    t = cue(say, (17, 3), "but daughters", 8.0)
    b3 += [(t, d, "ahead", "appear") for d in DAUGHTERS]
    defaults = dict(Mahlah=10.91, Noah=11.68, Hoglah=12.38, Milcah=13.19,
                    Tirzah=14.09)
    for d in DAUGHTERS:
        b3.append((cue(say, (17, 3), d, defaults[d]), d, "lit", "light"))
    out[(17, 3)] = b3
    out[(17, 4)] = [(0.0, k, "read", "let") for k in CHAIN]
    # "Ten parts": the five other clans light as the camera brings them in
    # (the daughters are lit already)
    t = max(cue(say, (17, 5), "Ten", 0.05), round(0.4 * ten_legs()[0], 2))
    out[(17, 5)] = [(t, k, "lit", "light") for k in OTHERS]
    return out


def looks_at(ref, plan):
    """Every box's look as `ref` opens (None: not drawn yet)."""
    cur = dict(OPEN, **{d: None for d in DAUGHTERS})
    for r in REFS:
        if r == ref:
            return cur
        for _t, k, look, _how in plan[r]:
            cur[k] = look
    return cur


# ---------------------------------------------------------------------------
# Drawing the tree (world px, under one translate onto the card)
# ---------------------------------------------------------------------------

_VF = SCW.VerseFrame.__new__(SCW.VerseFrame)      # its looks, nothing else
UNDER = 0.25        # a dimmer look comes in under the last over this


def _on(t, d, out=False):
    """Opacity in (or out) over d from t, or at once when d is 0."""
    if d <= 0:
        return (f'<set attributeName="opacity" to="{0 if out else 1}" '
                f'begin="{t:.2f}s"/>')
    return fade(t, d, out=out)


def _layers(timeline):
    """A thing's looks through a verse, [(t, look, dur)] (the first t None,
    its look as the verse opens, or None), as stacked layers: a brighter
    look fades in over the last, which then goes (both at once when dur is
    0); a dimmer one comes in under the last over UNDER, which fades off it,
    so the verse's first frame is the last verse's last. -> [(look, [anim],
    shown as the verse opens)], bottom first."""
    stack = []
    cur = None
    for t, look, d in timeline:
        if look is None:
            continue
        lay = [look, [], t is None]
        if t is None:
            stack.append(lay)
        elif cur is None:
            lay[1].append(_on(t, d))
            stack.append(lay)
        elif RANK[look] > RANK[cur[0]]:
            lay[1].append(_on(t, d))
            cur[1].append(_on(t + d, 0.3 if d else 0, out=True))
            stack.insert(stack.index(cur) + 1, lay)
        else:
            lay[1].append(_on(t, min(d, UNDER)))
            cur[1].append(_on(t, d, out=True))
            stack.insert(stack.index(cur), lay)
        cur = lay
    return stack


def _group(anims, inner, start_shown):
    op = "1" if start_shown else "0"
    return f'<g opacity="{op}">{"".join(anims)}{inner}</g>'


def tree_svg(ref, plan):
    """The tree in `ref`'s file: its lines and boxes as the verse opens,
    each change as it is said, and each line that draws itself."""
    b = branch()
    open_ = looks_at(ref, plan)
    evs = sorted(plan[ref], key=lambda e: e[0])
    durs = {"light": LIGHT, "let": LET_GO}
    # a box's looks through the verse
    box_tl = {k: [(None, open_.get(k), 0)] for k in b.node}
    traces = []
    for t, k, look, how in evs:
        if how in ("light", "let"):
            box_tl[k].append((t, look, durs[how]))
        elif how == "trace":
            box_tl[k].append((round(t + TRACE - LIGHT, 2), look, LIGHT))
            traces.append((t, k))
        else:                                   # appear
            box_tl[k].append((round(t + TRACE * 0.6, 2), look, 0.4))
            traces.append((t, k))
    # a line's looks follow the boxes it leads to; a name whose line draws
    # itself this verse keeps its old look under the trace until its box is
    # lit, when the trace hands over: it goes, and the line takes the lit
    # look at once (so the verse ends on standing lines, as the next opens)
    done = {}
    for t, k in traces:
        lit = [t1 + d1 for t1, look, d1 in box_tl[k][1:]
               if look == "lit" and t1 >= t]
        if lit:
            done[k] = round(max(t + TRACE, min(lit)), 2)

    def look_of(tl, t):
        return [e[1] for e in tl if e[0] is None or e[0] <= t][-1]
    line_rank = {}
    for k, tl in box_tl.items():
        pts = [(None, tl[0][1])]
        if not any(tk == k for _t, tk in traces):
            pts += tl[1:]
        elif k in done:
            pts.append((done[k], look_of(tl, done[k]), 0))
            pts += [e for e in tl[1:] if e[0] > done[k]]
        line_rank[k] = pts
    groups = {}
    for s in b.segs:
        served = [b.key[n] for n in s.serves if n in b.key]
        times = sorted({t for k in served for t, *_r in line_rank[k][1:]})

        def at(t, served=served):
            best = None
            for k in served:
                look = None
                for e in line_rank[k]:
                    if e[0] is None or (t is not None and e[0] <= t):
                        look = e[1]
                if look is not None and (best is None
                                         or RANK[look] > RANK[best]):
                    best = look
            return best
        tl = [(None, at(None), 0)]
        for t in times:
            d = max(e[2] for k in served for e in line_rank[k][1:]
                    if e[0] == t)
            if at(t) != tl[-1][1]:
                tl.append((t, at(t), d))
        groups.setdefault(tuple(tl), []).append(s)

    lines, fine = [], []
    bead = (lambda x, y: SKY)
    for tl, segs in groups.items():
        for look, anims, start in _layers(list(tl)):
            ls, fs = FL.static_els(segs, lambda s, lk=look: lk,
                                   SCW.LINE_ALPHA, bead_fill=bead)
            if ls:
                lines.append(_group(anims, "".join(ls), start))
            if fs:
                fine.append(_group(anims, "".join(fs), start))
    grow = []
    for t, k in traces:
        els = "".join(FL.trace_els(b.geom, b.node[k], SCW.LINE_ALPHA["lit"],
                                   SCW.TRACE_W, SCW.TRACE_FINE_W,
                                   f"{TRACE:.2f}s", begin=f"{t:.2f}s"))
        if k in done:
            els = f'<g>{_on(done[k], 0, out=True)}{els}</g>'
        grow.append(els)
    boxes = []
    for k, tl in box_tl.items():
        n = b.node[k]
        for look, anims, start in _layers(tl):
            els = _VF._node_els(n, look, True)
            wd = _fmt(_VF.LOOK[look][2])
            boxes.append(_group(anims, f'<g stroke-width="{wd}">'
                                + "".join(els) + "</g>", start))
    return (f'<g transform="translate({_fmt(-b.x0)} {_fmt(-b.y0)})">'
            f'<g stroke-width="{_fmt(SCW.CONNECTOR_W)}">{"".join(lines)}</g>'
            f'<g stroke-width="{_fmt(SCW.FINE_W)}">{"".join(fine)}</g>'
            + "".join(grow) + "".join(boxes) + "</g>")


def blocks_svg():
    """The blocks and their lines in: they never change."""
    b = branch()
    rects = "".join(
        f'<rect x="{_fmt(r[0])}" y="{_fmt(r[1])}" width="{_fmt(r[2] - r[0])}" '
        f'height="{_fmt(r[3] - r[1])}" rx="{SCW.BLOCK_RX}" '
        f'fill="{rgb(SCW.BLOCK_FILL)}" '
        f'fill-opacity="{SCW.BLOCK_FILL[3] / 255:.3f}" '
        f'stroke="{rgb(SCW.BLOCK_EDGE)}" '
        f'stroke-opacity="{SCW.BLOCK_EDGE[3] / 255:.3f}"/>'
        for r, _f, _l in b.blocks)
    segs = [s for _r, _f, ls in b.blocks for s in ls]
    ls, fs = FL.static_els(segs, lambda s: "ahead", SCW.LINE_ALPHA,
                           bead_fill=lambda x, y: SKY)
    return (f'<g transform="translate({_fmt(-b.x0)} {_fmt(-b.y0)})">'
            f'<g stroke-width="{_fmt(SCW.BLOCK_EDGE_W)}">{rects}</g>'
            f'<g stroke-width="{_fmt(SCW.CONNECTOR_W)}">{"".join(ls)}</g>'
            f'<g stroke-width="{_fmt(SCW.FINE_W)}">{"".join(fs)}</g></g>')


# ---------------------------------------------------------------------------
# The stage
# ---------------------------------------------------------------------------

def tree_right():
    """The right edge of the tree's lowest rows, over the stage: whoever
    stands right of it stands under no box."""
    b = branch()
    low = b.box("Mahlah")[1]
    return max(r[2] for r in b.card_rects() if r[3] > low)


def stage():
    """Where the cast stands, card px: the five women under the daughters'
    boxes, where they stop before the leaders, and the leaders right of the
    tree's last column."""
    b = branch()
    under = [b.mid(d)[0] for d in DAUGHTERS]
    right = tree_right()
    # close enough to the tree that the five lit boxes, the women under them
    # and the leaders make one shot with Zelophehad's line clear of the
    # title (SHOTS["daughters"])
    eleazar = right + 30
    joshua = eleazar + 86
    princes = [joshua + 80 + 40 * i for i in range(3)]
    before = [eleazar - 76 - 50 * (4 - i) for i in range(5)]
    return dict(under=under, before=before, eleazar=eleazar, joshua=joshua,
                princes=princes)


def build(town_xy, say=None):
    """The card hung at the region's world point. `say(ref, word)` is when
    the narration says a word (seconds, or None), which times the beats."""
    c = Card("zel", town_xy, ANCHOR, SIZE, S_CARD, page=EARTH, sky=SKY,
             ground_y=GROUND, origin=ORIGIN)
    X0, Y0 = ORIGIN
    c.scenery.append(f'<rect x="{X0}" y="{GROUND}" width="{SIZE[0]}" '
                     f'height="{Y0 + SIZE[1] - GROUND}" fill="{rgb(EARTH)}"/>')
    c.scenery.append(f'<line x1="{X0}" y1="{GROUND}" x2="{X0 + SIZE[0]}" '
                     f'y2="{GROUND}" stroke="{rgb(SAND)}" stroke-width="2" '
                     f'stroke-opacity="0.5"/>')
    c.scenery.append(blocks_svg())
    st = stage()
    for i, x in enumerate(st["under"]):
        c.add(Actor(f"w{i}", person("woman"), x, GROUND, ink=TEXT))
    c.add(Actor("eleazar", person("priest"), st["eleazar"], GROUND, ink=TEXT,
                flip=-1, label_y=LABEL_Y, names_at=NAMES))
    c.add(Actor("joshua", person("man", staff=True), st["joshua"], GROUND,
                ink=TEXT, label_y=LABEL_Y, names_at=NAMES))
    for i, x in enumerate(st["princes"]):
        c.add(Actor(f"prince{i}", person("man"), x, GROUND, ink=SAND,
                    flip=-1))
    # the princes' one name, on no figure of its own
    c.add(Actor("princes", static(list), st["princes"][1], GROUND,
                label_y=LABEL_Y, names_at=NAMES))
    c.refs = list(REFS)
    plan = beats(say)
    for ref in REFS:
        c.effect(ref, tree_svg(ref, plan))
    # the tree is drawn as each verse's effect, not by actors; its beats
    # ride a figure that is never shown, so the tour's timing check
    # (svg_scene_card.card_ends) sees when they end
    c.add(Actor("tree", static(list), 0, 0))
    ends = {"light": LIGHT, "let": LET_GO, "trace": TRACE,
            "appear": TRACE * 0.6 + 0.4}
    for ref in REFS:
        for t, _k, _look, how in plan[ref]:
            c.on(ref, ("beat", "tree", t, ends[how], None))
    events(c, say)
    return c


def events(c, say=None):
    on = c.on
    st = stage()
    ref = (17, 4)
    land = LEGS[ref][0][2]
    # they came: the women come in under their names as the camera goes
    # down, and walk to the leaders
    for i in range(5):
        dx = st["before"][i] - st["under"][i]
        on(ref, ("show", f"w{i}", 0.2, 0.6, None),
           ("pose", f"w{i}", 0.8, 0.2, {"pose": "walk"}),
           ("move", f"w{i}", 0.8, 3.6, (dx, 0)),
           ("pose", f"w{i}", 4.4, 0.2, {"pose": "stand"}))
    t = cue(say, ref, "Eleazar", 0.76)
    on(ref, ("show", "eleazar", t, 0.5, None),
       ("label", "eleazar", max(t, land), 0, "Eleazar"))
    t = cue(say, ref, "Joshua", 2.52)
    on(ref, ("show", "joshua", t, 0.5, None),
       ("label", "joshua", t, 0, "Joshua"))
    t = cue(say, ref, "princes", 4.68)
    for i in range(3):
        on(ref, ("show", f"prince{i}", t, 0.5, None))
    on(ref, ("show", "princes", t, 0.5, None),
       ("label", "princes", t, 0, "princes"))
    # "saying": the first of them, nearest the priest, opens her arms
    on(ref, ("pose", "w4", cue(say, ref, "saying", 5.24), 0.3,
             {"arms": "open"}))
    # "he gave": Joshua raises his free hand (svg_figures draws only the arm
    # the staff leaves free); a hand held out would point at the priest
    on(ref, ("pose", "joshua", cue(say, ref, "gave", 12.61), 0.3,
             {"arms": "up"}))
    # "among the brothers of their father": back under their names
    t = cue(say, ref, "an inheritance among the brothers", 13.12)
    for i in range(5):
        dx = st["under"][i] - st["before"][i]
        on(ref, ("flip", f"w{i}", t, 0.2, -1),
           ("pose", f"w{i}", t, 0.2, {"pose": "walk", "arms": "down"}),
           ("move", f"w{i}", t, 2.2, (dx, 0)),
           ("pose", f"w{i}", round(t + 2.2, 2), 0.2, {"pose": "stand"}),
           ("flip", f"w{i}", round(t + 2.2, 2), 0.2, 1))
    # 17:5 "Ten parts": the text's own number among the ten, as the camera
    # settles on them
    x, y = ten_xy()
    t = ten_in(say)
    c.on((17, 5), ("beat", "tree", t, TEN_FADE, None))
    c.effect((17, 5),
             f'<g opacity="0">{fade(t, TEN_FADE)}<text x="{_fmt(x)}" '
             f'y="{_fmt(y)}" font-size="{TEN_PX}" font-weight="bold" '
             f'fill="{rgb(HL)}" text-anchor="middle" '
             f'dominant-baseline="central">10</text></g>')


TEN_PX = 46                     # the "10", card px
TEN_FADE = 0.4
TEN_HOLD = 1.5                  # seconds the "10" stands whole before the rise
# 17:5 opens on the daughters' shot, where the "10" would stand under the
# title; by this the camera has carried it clear
TEN_CLEAR = 0.15


def ten_legs():
    """17:5's legs: to the ten, the hold, the rise (seconds)."""
    return tuple(d for _k, _t, d in LEGS[(17, 5)])


def ten_in(say=None):
    """When the "10" comes in: as "Ten" is said, once it's clear of the
    title."""
    return max(cue(say, (17, 5), "Ten", 0.05), TEN_CLEAR)


def ten_xy():
    """Where the "10" stands, card px: over the ten boxes' middle, halfway
    between the row over the daughters and their line."""
    b = branch()
    ten = OTHERS + DAUGHTERS
    x = sum(b.mid(k)[0] for k in ten) / len(ten)
    bus = b.geom.families[b.node["Zelophehad"]]["bus_y"] - b.y0
    above = max(r[3] for r in b.card_rects()
                if r[3] < bus and r[0] < x + TEN_PX and x - TEN_PX < r[2])
    return round(x, 1), round((above + bus) / 2, 1)


# Camera shots inside the card, (x, y, zoom), and each verse's legs. A leg's
# target is a shot here, or "map" (the verse's own camera on the map).
REFS = [(17, 2), (17, 3), (17, 4), (17, 5)]
SHOTS = {
    "clans": (790, 230, 0.92),      # Manasseh, the six clans, Zelophehad
    "chain": (915, 240, 1.0),       # Manasseh down to Zelophehad
    "nosons": (792, 548, 1.0),      # Hepher, Zelophehad and the empty row
    "stage": (1260, 870, 1.25),     # the stage, under the tree's last rows
    "daughters": (1012, 815, 0.87), # the five lit, the women, the leaders
    "ten": (784, 312, 0.87),        # Manasseh over the ten: the other five
                                    # clans and the daughters
}
LEGS = {
    (17, 2): [("to", "clans", 3.0)],
    (17, 3): [("to", "chain", 1.2), ("hold", None, 5.4),
              ("to", "nosons", 1.2)],
    (17, 4): [("to", "stage", 1.6), ("hold", None, 11.5),
              ("to", "daughters", 2.3)],
    # "Ten parts" (0.15 s) to the ten; the "10" stands whole TEN_HOLD; the
    # card has left the frame (about 0.63 of the rise) by 3.19 s, before
    # "Gilead" (3.28 s), which the map leaves out if said while the card
    # shows; it lands at 3.85 s, and the map's names end by 5.85 s
    (17, 5): [("to", "ten", 0.8), ("hold", None, 1.25), ("to", "map", 1.8)],
}


# ---------------------------------------------------------------------------
# QC
# ---------------------------------------------------------------------------

def air():
    """The tree's own air between one row of named boxes and the next."""
    b = branch()
    rows = sorted({b.box(k)[1:4:2] for k in b.node})
    return min(r2[0] - r1[1] for r1, r2 in zip(rows, rows[1:])
               if r2[0] > r1[1])


TITLE = "The lot of Manasseh — Joshua 17"   # the tour's title over the card
CAST_SHOTS = ("stage", "daughters")         # the rests the leaders' names show at
TEN_AIR = 24                                # card px round the "10"
TOUCH = 0.6                                 # a line's end on what it joins


def _gap(a, b):
    """The distance between two rects (0 where they meet)."""
    return math.hypot(max(a[0] - b[2], b[0] - a[2], 0),
                      max(a[1] - b[3], b[1] - a[3], 0))


def _within(a, b):
    """Rect a lies inside rect b."""
    return b[0] < a[0] and a[2] < b[2] and b[1] < a[1] and a[3] < b[3]


def _shot_rect(shot, r):
    """A screen rect at a shot, in card px."""
    x, y, z = shot
    return (x + (r[0] - W / 2) / z, y + (r[1] - H / 2) / z,
            x + (r[2] - W / 2) / z, y + (r[3] - H / 2) / z)


def _box(ln):
    return (min(ln[0], ln[2]), min(ln[1], ln[3]),
            max(ln[0], ln[2]), max(ln[1], ln[3]))


def drawn():
    """Every piece of line the card draws, card px, as (x0, y0, x1, y1):
    the named boxes' lines and the blocks'. -> (pieces, every strand)."""
    b = branch()
    segs = list(b.segs) + [s for _r, _f, ls in b.blocks for s in ls]

    def card(ln):
        return (ln[0] - b.x0, ln[1] - b.y0, ln[2] - b.x0, ln[3] - b.y0)
    return ([card((s.x0, s.y0, s.x1, s.y1)) for s in segs],
            [card(ln) for s in segs for ln in FL._drawn_lines(s)])


def _ink(actor, x, pose, flip):
    """A figure's ink, card px: every outline of its parts (staff, arms,
    headgear and all), sampled each px. -> (points, bbox)."""
    s = actor.h / actor.unit_h
    y = actor.start["y"]
    pts = []
    for kind, data, _m in actor.parts(dict(pose)):
        if kind == "dot":
            (cx, cy), = F.place([data[:2]], x, y, s, flip)
            r = data[2] * s
            pts += [(cx + r * math.cos(i * math.pi / 8),
                     cy + r * math.sin(i * math.pi / 8)) for i in range(16)]
            continue
        q = F.place(data, x, y, s, flip)
        if kind == "fill":
            q = q + q[:1]
        for (ax, ay), (bx, by) in zip(q, q[1:]):
            n = max(1, int(math.hypot(bx - ax, by - ay)))
            pts += [(ax + (bx - ax) * i / n, ay + (by - ay) * i / n)
                    for i in range(n)]
        pts.append(q[-1])
    if not pts:
        return [], None
    return pts, (min(p[0] for p in pts), min(p[1] for p in pts),
                 max(p[0] for p in pts), max(p[1] for p in pts))


def looks(card):
    """Every look each figure takes on the card: {key: [(x, pose, flip)]},
    a walk sampled along its way."""
    from svg_scene_card import apply_event
    out = {}
    for key, a in card.actors.items():
        if not a.parts(dict(a.start["pose"])):
            continue                            # a name on no figure
        s = dict(a.start, pose=dict(a.start["pose"]))

        def now(x=None, s=s):
            return (s["x"] if x is None else x,
                    tuple(sorted(s["pose"].items())), s["flip"])
        seen = [now()]
        for ref in card.refs:
            for kind, k, _t, _d, val in sorted(card.events.get(ref, []),
                                               key=lambda e: e[2]):
                if k != key:
                    continue
                if kind == "move":
                    seen += [now(s["x"] + val[0] * i / 8) for i in range(1, 8)]
                apply_event(s, kind, val)
                seen.append(now())
        out[key] = list(dict.fromkeys(seen))
    return out


def cast_names(card):
    """[(actor key, text, x, y, names_at)]: every cast name, card px."""
    out = []
    for key, a in card.actors.items():
        texts = [a.start["label"]] if a.start.get("label") else []
        texts += [v for r in card.refs for kind, k, _t, _d, v
                  in card.events.get(r, []) if k == key and kind == "label"]
        for text in texts:
            out.append((key, text, a.start["x"], a.start["y"] + a.label_y,
                        a.names_at or card.names_at))
    return out


def qc(card):
    """-> [problem]: a rest whose tree names fall under MIN_NAME_PX; a tree
    box, block or line under the title; a cast name, at any zoom it shows
    at up to the closest rest, within the tree's air of a box, within
    NAME_GAP of another name or FIGURE_GAP of any figure's ink (its own,
    staff included); a cast name or leader out of frame at a rest that
    shows them; a leader standing under a box; a line into a box or block,
    or one running to nothing; and the "10" crowding a box, line or name,
    out of its shot, under the title, or whole for less than TEN_HOLD
    before the camera leaves."""
    from svg_map_camera import title_rect
    out = []
    b = branch()
    rects = b.card_rects()
    pieces, strands = drawn()
    gap = air()
    ten = ink("10", TEN_PX, True, False, "mm")
    tx, ty = ten_xy()
    ten_r = (tx + ten[0], ty + ten[1], tx + ten[2], ty + ten[3])
    for name, shot in SHOTS.items():
        z = shot[2]
        if z * NAME_PX < MIN_NAME_PX:
            out.append(f"{name}: tree names {z * NAME_PX:.1f} px")
        tr = _shot_rect(shot, title_rect(TITLE))
        for r in rects:
            if _gap(r, tr) <= 0:
                out.append(f"{name}: a tree box under the title at {r}")
        for ln in strands:
            if _gap(_box(ln), tr) < 2 / z:
                out.append(f"{name}: a line under the title at {ln}")
        if name == "ten" and _gap(ten_r, tr) < 2 / z:
            out.append(f"{name}: the 10 under the title")
    # the cast's names, at every zoom they show at up to the closest rest
    figs = {key: [_ink(card.actors[key], x, pose, flip)
                  for x, pose, flip in ls]
            for key, ls in looks(card).items()}
    names = cast_names(card)
    zmax = max(SHOTS[n][2] for n in CAST_SHOTS)
    hit = {}

    def rect_at(n, z):
        _k, text, x, y, _at = n
        bx = ink(text, FONT_PX, False, False, "mm")
        return (x + bx[0] / z, y + bx[1] / z, x + bx[2] / z, y + bx[3] / z)
    for n in names:
        z = n[4][0]
        while z <= zmax + 1e-9:
            r = rect_at(n, z)
            for m in names:
                if m is not n and _gap(r, rect_at(m, z)) < NAME_GAP / z:
                    hit.setdefault((n[1], m[1]), z)
            for key, ls in figs.items():
                for pts, bb in ls:
                    # + 1: the outline's half width
                    if bb is None or _gap(r, bb) >= FIGURE_GAP / z + 1:
                        continue
                    d = min(math.hypot(max(r[0] - px, px - r[2], 0),
                                       max(r[1] - py, py - r[3], 0))
                            for px, py in pts)
                    if d < FIGURE_GAP / z + 1:
                        hit.setdefault((n[1], key), z)
            for t in rects:
                if _gap(r, t) < gap:
                    hit.setdefault((n[1], t), z)
            z = round(z + 0.01, 2)
    for (text, what), z in hit.items():
        out.append(f"{text} crowds {what} at zoom {z:.2f}")
    # whole in frame at the rests that show them
    for name in CAST_SHOTS:
        shot = SHOTS[name]
        fr = _shot_rect(shot, (2, 2, W - 2, H - 2))
        for n in names:
            if not _within(rect_at(n, shot[2]), fr):
                out.append(f"{name}: {n[1]} out of frame")
        for key in ["eleazar", "joshua"] + [f"prince{i}" for i in range(3)]:
            if not all(_within(bb, fr) for _p, bb in figs[key]):
                out.append(f"{name}: {key} out of frame")
    right = tree_right()
    half = 22                                   # a figure's half width
    for key in ["eleazar", "joshua"] + [f"prince{i}" for i in range(3)]:
        if card.actors[key].start["x"] - half <= right:
            out.append(f"{key} stands under the tree's last column")
    # every line ends on a box, a block or another line, and none runs in
    for ln in pieces:
        for r in rects:
            if SIL._line_in(ln, r):
                out.append(f"a line runs into {r}: {ln}")
        for p in (ln[:2], ln[2:]):
            pt = (p[0], p[1], p[0], p[1])
            if not (any(_gap(pt, r) <= TOUCH for r in rects) or
                    any(m is not ln and _gap(pt, _box(m)) <= TOUCH
                        for m in pieces)):
                out.append(f"a line runs to nothing at {p}")
    # the "10"
    for r in rects:
        if _gap(ten_r, r) < TEN_AIR:
            out.append(f"the 10 within {TEN_AIR} px of {r}")
    for ln in strands:
        if _gap(ten_r, _box(ln)) < TEN_AIR:
            out.append(f"the 10 within {TEN_AIR} px of a line {ln}")
    for n in names:
        if _gap(ten_r, rect_at(n, SHOTS["ten"][2])) < TEN_AIR:
            out.append(f"the 10 within {TEN_AIR} px of {n[1]}")
    if not _within(ten_r, _shot_rect(SHOTS["ten"], (40, 40, W - 40, H - 40))):
        out.append("the 10 out of its shot")
    move, hold, _rise = ten_legs()
    whole = move + hold - (ten_in() + TEN_FADE)
    if whole < TEN_HOLD - 1e-6:
        out.append(f"the 10 whole {whole:.2f} s")
    return out
