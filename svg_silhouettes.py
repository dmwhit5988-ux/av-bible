"""Silhouettes: a branch nobody has read yet stands as one faint block.

1 Chronicles 1-9 is read as a camera over one laid-out tree
(`svg_chronicles_world`), and every box in it stands from the first verse:
read boxes bright, boxes still to come faint. In the early wide shots that
put hundreds of people nobody has read yet on some row of the sheet, beside
people they have nothing to do with. So a BRANCH the reading has not reached
is drawn, in that verse's file, as ONE quiet block instead of its boxes:

* A branch is UNOPENED at a verse when nobody in it has been read yet and
  somebody in it will be, later in chapters 1-9. Its first person, the HEAD,
  keeps his box and his name; everything under him (his children and theirs,
  and the children of the wives beside him) folds into one rounded block
  over the boxes it stands for, hung from his line by its stem, when
  somebody under him will be read. The wives beside him keep their boxes:
  they stand on his row, not under him.
* A whole tribe's panel that nobody has been read in yet is one block: the
  panel itself, under its title, with its contents folded. Its head's routed
  line still runs to it, as far as its top.
* A branch with nothing in it to read later (never named in 1-9, context) is
  drawn as it always was, and so is everything already read. A context box
  inside a branch that will be read folds with it.
* Nothing moves: the camera, the rest frames and the lit sets do not depend
  on this. A block is only drawn instead of boxes, and counts as one item
  against the frame's node cap.

When the reading reaches a branch, its block gives way to its boxes: in that
verse's file the block fades out while the boxes it held (and the smaller
blocks under the people now standing) fade in, as part of the arrival. The
arriving names still brighten over their faint boxes, as every arrival does.

A BLOCK NEVER COVERS ANOTHER BRANCH. Its rect is the bounding box of what it
folds, and the layout's contour packing slides a small family under a big
neighbour's overhang, so a big branch's box can reach over a cousin's names
or lines. `Silhouettes` sweeps every verse's state: a block over a drawn box
or label, over a line it does not own, over another block, or across a
panel's edge (a block is in one panel or in the fan) does not fold, and its
head's children become the heads instead, each with his own block. It
repeats until no verse has a collision, so the set of heads that open a
generation further (`split`) is one rule for the whole reading. A block that
would hide fewer than MIN_FOLD boxes does not fold either: a block the size
of one box reads as an empty box.
"""

import math

from chronicles_tree import walk
from layout_regions import is_wife
from svg_family_lines import Seg, _drawn_lines, _shared_style, same_row

INF = 10 ** 9
PAD = 6.0           # a block's edge round the boxes it folds
PAD_TOP = 4.0       # and over their row: the family's bus runs 15 px above
MIN_FOLD = 2        # boxes a block must fold (labels are not boxes)
STUB_IN = 12.0      # a stem enters a block at least this far from its side
INSET = 0.5         # overlap a collision must exceed, in world px


def _beside(p, k):
    """A wife standing on her husband's row, clear of his box: the marriage
    bars' rule in svg_family_lines.Geometry."""
    return (is_wife(k) and same_row(p, k)
            and (k.x >= p.x + p.w - 0.5 or k.x + k.w <= p.x + 0.5))


def _meet(a, b, e=INSET):
    return (min(a[2], b[2]) - max(a[0], b[0]) > e and
            min(a[3], b[3]) - max(a[1], b[1]) > e)


def _inside(a, b):
    """Rect a lies within rect b."""
    return (a[0] >= b[0] - 1e-6 and a[1] >= b[1] - 1e-6 and
            a[2] <= b[2] + 1e-6 and a[3] <= b[3] + 1e-6)


def _line_in(ln, r, e=1.0):
    """An axis-aligned line passes into rect r's interior (inset e)."""
    x0, y0, x1, y1 = ln
    bx0, by0, bx1, by1 = r[0] + e, r[1] + e, r[2] - e, r[3] - e
    if abs(y1 - y0) < 1e-6:
        return by0 < y0 < by1 and min(x0, x1) < bx1 and max(x0, x1) > bx0
    return bx0 < x0 < bx1 and min(y0, y1) < by1 and max(y0, y1) > by0


def _clip_out(s, r):
    """The parts of piece s outside rect r -> [Seg]; s itself if it never
    enters r."""
    if not _line_in((s.x0, s.y0, s.x1, s.y1), r, e=0.0):
        return [s]
    out = []
    if abs(s.y1 - s.y0) < 1e-6:
        lo, hi = min(s.x0, s.x1), max(s.x0, s.x1)
        for a, b in ((lo, min(hi, r[0])), (max(lo, r[2]), hi)):
            if b - a > 1e-6:
                out.append(Seg(a, s.y0, b, s.y0, s.role, s.style, s.fam,
                               s.serves))
    else:
        lo, hi = min(s.y0, s.y1), max(s.y0, s.y1)
        for a, b in ((lo, min(hi, r[1])), (max(lo, r[3]), hi)):
            if b - a > 1e-6:
                out.append(Seg(s.x0, a, s.x0, b, s.role, s.style, s.fam,
                               s.serves))
    return out


class Block:
    """One silhouette: what it folds, where it stands, and the line into it.

    key: ("panel", title) or ("branch", head key). head: the person whose
    line it hangs from (his box stays drawn). panel: the Panel it is, for a
    whole unopened panel (its rect and title are the panel's own), else
    None. folded: the nodes it hides. rect: (x0, y0, x1, y1). stubs: the
    pieces that run from the head's family into its top (Seg objects, role
    "stub" or the routed stem's own pieces, cut at the panel's edge).
    boxes: how many boxes it folds. reach: the bounding box of its rect and
    stubs."""

    __slots__ = ("key", "head", "panel", "folded", "rect", "stubs", "boxes",
                 "reach")

    def __init__(self, key, head, panel, folded, rect, stubs, boxes):
        self.key, self.head, self.panel = key, head, panel
        self.folded, self.rect, self.stubs = folded, rect, stubs
        self.boxes = boxes
        # everything it draws, its rect and its stems
        x0, y0, x1, y1 = rect
        for s in stubs:
            b = s.bbox()
            x0, y0 = min(x0, b[0]), min(y0, b[1])
            x1, y1 = max(x1, b[2]), max(y1, b[3])
        self.reach = (x0, y0, x1, y1)

    def __repr__(self):
        return f"<Block {self.key[1]} {len(self.folded)}>"


class State:
    """The silhouettes at one point in the reading: `hidden` nodes, and the
    blocks drawn for them by key."""

    __slots__ = ("hidden", "blocks")

    def __init__(self, hidden, blocks):
        self.hidden, self.blocks = hidden, blocks


class Silhouettes:
    """Which branches stand as blocks at each verse of a World's reading.

    `state(i)` is the state the i-th verse (World.order) RESTS on, once its
    names are read; the verse's file opens on `state(i - 1)`. Built from the
    World's tree, its regions Plan (panels, labels, routes) and the frames'
    family-line Geometry; nothing here depends on the camera."""

    def __init__(self, world, geom):
        self.world, self.geom = world, geom
        plan = world.plan
        self.labels = set(plan.labels)
        self.panels = list(plan.panels)
        self.head_panel = {p.head: p for p in self.panels}
        self.panel_of = plan.panel_of
        order = {(c, v): i for i, (c, v, _s) in enumerate(world.order)}
        self.pos = order
        fp = {n: order[cv] for n, cv in world.first_of.items()}
        self.fp = fp
        # smin: the first verse anybody in n's subtree is read; dmin: the
        # same over what n's block would fold (his descendants, not the
        # wives beside him); mixed: n's block would fold boxes of another
        # region than his own (a fan block never reaches into the panels,
        # which are blocks of their own)
        self.smin, self.dmin, self.fold, self.nboxes = {}, {}, {}, {}
        for n in reversed(world.nodes):          # children before parents
            m = fp.get(n, INF)
            for k in n.kids:
                m = min(m, self.smin[k])
            self.smin[n] = m
        for n in world.nodes:
            f = []
            for k in n.kids:
                if _beside(n, k):
                    for kk in k.kids:
                        f.extend(walk(kk))
                else:
                    f.extend(walk(k))
            self.fold[n] = frozenset(f)
            self.dmin[n] = min((fp.get(q, INF) for q in f), default=INF)
            self.nboxes[n] = sum(1 for q in f if q not in self.labels)
        self.pmin = {p: min((fp.get(q, INF) for q in p.nodes), default=INF)
                     for p in self.panels}
        home = {n: self.panel_of.get(n) for n in world.nodes}
        self.mixed = {n for n in world.nodes
                      if any(home[q] is not home[n] for q in self.fold[n])}
        self._blocks = {}
        self.split = set()
        self.problems = []
        self._settle()

    # -- one block -----------------------------------------------------------

    def _block(self, key, head, panel):
        b = self._blocks.get(key)
        if b is not None:
            return b
        folded = frozenset(panel.nodes) if panel else self.fold[head]
        if panel is not None:
            rect = panel.rect
        else:
            xs0 = [q.x for q in folded]
            ys0 = [q.y for q in folded]
            xs1 = [q.x + q.w for q in folded]
            ys1 = [q.y + q.h for q in folded]
            rect = (min(xs0) - PAD, min(ys0) - PAD_TOP,
                    max(xs1) + PAD, max(ys1) + PAD)
        stubs = self._stubs(head, rect, folded)
        b = Block(key, head, panel, folded, rect, stubs,
                  sum(1 for q in folded if q not in self.labels))
        self._blocks[key] = b
        return b

    def _stubs(self, head, rect, folded):
        """The line from the head's family into the block's top: for each
        parent among the head and the wives beside him whose children it
        folds, his stem down to his bus, along it to over the block, and
        down into the block's top edge; a routed stem (a panel head's, or
        his wife's) is his own route, cut where it enters the panel."""
        g = self.geom
        out = []
        parents = [head] + [k for k in head.kids if _beside(head, k)]
        for f in parents:
            info = g.families.get(f)
            if info is None or not (set(info["below"]) & folded):
                continue
            kids = frozenset(info["below"])
            if f in g.routes:
                seen = set()
                for k in kids:
                    for s in g.node_segments.get(k, ()):
                        if s.role in ("route", "trunk") and id(s) not in seen:
                            seen.add(id(s))
                            out.extend(_clip_out(s, rect))
                continue
            style = _shared_style(kids)
            pcx, pb = f.x + f.w / 2, f.y + f.h
            bus = info["bus_y"]
            lo, hi = rect[0] + STUB_IN, rect[2] - STUB_IN
            xc = min(max(pcx, lo), hi) if lo <= hi else (rect[0] + rect[2]) / 2
            top = rect[1]
            yh = bus if bus < top - 0.5 else (pb + top) / 2
            if abs(xc - pcx) < 0.5:
                pts = [(pcx, pb), (pcx, top)]
            else:
                pts = [(pcx, pb), (pcx, yh), (xc, yh), (xc, top)]
            for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
                if abs(x1 - x0) + abs(y1 - y0) > 1e-6:
                    out.append(Seg(x0, y0, x1, y1, "stub", style, f, kids))
        return out

    # -- one verse's state ---------------------------------------------------

    def _walk(self, i, split):
        """The state the i-th verse rests on, opening the heads in `split`
        a generation further."""
        hidden, blocks = set(), {}
        stack = [self.world.root]
        while stack:
            n = stack.pop()
            p = self.head_panel.get(n)
            if p is not None and i < self.pmin[p] < INF:
                b = self._block(("panel", p.title), n, p)
                blocks[b.key] = b
                hidden |= b.folded
                continue
            if (i < self.smin[n] < INF and n.parent is not None
                    and not _beside(n.parent, n) and n not in split
                    and n not in self.mixed and self.dmin[n] < INF
                    and self.nboxes[n] >= MIN_FOLD):
                b = self._block(("branch", n.key), n, None)
                blocks[b.key] = b
                hidden |= b.folded
                continue
            stack.extend(n.kids)
        return State(frozenset(hidden), blocks)

    def _near(self, b):
        """What could collide with block b in some state, cached: the boxes
        and labels its rect meets, the pieces of line whose ink enters it
        (beside its own family's, which it folds), and whether it crosses a
        panel's edge."""
        c = self._near_cache.get(b.key)
        if c is not None:
            return c
        r = b.rect
        nodes = [n for n in self._box_index.query(*r)
                 if n not in b.folded
                 and _meet(r, (n.x, n.y, n.x + n.w, n.y + n.h))]
        segs = []
        for s in self._seg_index.query(*r):
            if s.serves <= b.folded:
                continue
            if any(_line_in(ln, r) for ln in _drawn_lines(s)):
                segs.append(s)
        edge = None
        if b.panel is None:
            for p in self.panels:
                if _meet(r, p.rect) and not _inside(r, p.rect):
                    edge = p.title
                    break
        c = (nodes, segs, edge)
        self._near_cache[b.key] = c
        return c

    def _pair(self, b, b2):
        """-> what of block b2 block b covers: "block", "stem" or None,
        cached."""
        key = (b.key, b2.key)
        if key in self._pair_cache:
            return self._pair_cache[key]
        out = None
        if b.panel is None and _meet(b.rect, b2.rect) and \
                not (b2.panel is not None and _inside(b.rect, b2.rect)):
            out = "block"
        elif any(_line_in((s.x0, s.y0, s.x1, s.y1), b.rect)
                 and not (s.serves <= b.folded) for s in b2.stubs):
            out = "stem"
        self._pair_cache[key] = out
        return out

    def collisions(self, st):
        """-> [(block, what it covers)] in one state: a drawn box or label,
        a drawn line it does not own (another family's piece, or another
        block's stem), another block, or a panel's edge."""
        out = []
        hidden = st.hidden
        blocks = list(st.blocks.values())
        for b in blocks:
            nodes, segs, edge = self._near(b)
            for n in nodes:
                if n not in hidden:
                    out.append((b, n.label))
            for s in segs:
                if not (s.serves <= hidden):
                    out.append((b, f"the {s.role} of {s.fam.label}"))
            if edge is not None:
                out.append((b, f"the edge of {edge}"))
            for b2 in blocks:
                if b2 is not b:
                    what = self._pair(b, b2)
                    if what == "block":
                        out.append((b, f"the block under {b2.head.label}"))
                    elif what == "stem":
                        out.append((b, f"the stem into the block under "
                                       f"{b2.head.label}"))
        return out

    def _bad(self, st):
        """The heads whose block covers something in this state. Of two
        blocks over each other, the one folding more boxes opens (both, if
        they fold as many)."""
        bad = set()
        hidden = st.hidden
        blocks = [b for b in st.blocks.values()]
        for b in blocks:
            if b.panel is not None:
                continue
            nodes, segs, edge = self._near(b)
            if edge is not None or any(n not in hidden for n in nodes) or \
                    any(not (s.serves <= hidden) for s in segs):
                bad.add(b.head)
                continue
            for b2 in blocks:
                if b2 is b:
                    continue
                what = self._pair(b, b2)
                if what == "stem" or (what == "block" and (
                        b2.panel is not None or b.boxes >= b2.boxes)):
                    bad.add(b.head)
                    break
        return bad

    def _settle(self):
        """Every verse's state, opening a head a generation further wherever
        his block would cover another branch, until no verse has one."""
        from svg_family_lines import _BoxIndex
        self._box_index = _BoxIndex(self.world.nodes)
        self._seg_index = _SegIndex(self.geom.segs)
        self._near_cache, self._pair_cache = {}, {}
        # a verse that reads nobody new rests on the state before it
        marks = sorted({0} | {i for i in self.fp.values()})
        for self.rounds in range(1, 65):
            bad = set()
            states = {}
            for i in marks:
                st = self._walk(i, self.split)
                states[i] = st
                bad |= self._bad(st)
            if not bad:
                break
            self.split |= bad
        else:
            raise RuntimeError("silhouettes did not settle")
        self._states = []
        cur = states[0]
        for i in range(len(self.world.order)):
            cur = states.get(i, cur)
            self._states.append(cur)
        for i in marks:
            for b, what in self.collisions(states[i]):
                c, v, _s = self.world.order[i]
                self.problems.append(f"{c}:{v} the block under "
                                     f"{b.head.label} covers {what}")

    def state(self, i):
        return self._states[max(0, min(i, len(self._states) - 1))]


class _SegIndex:
    """Pieces of line by grid cell, for the sweep."""

    def __init__(self, segs, cell=256.0):
        self.cell = cell
        self.grid = {}
        for s in segs:
            for key in self._cells(*self._bb(s)):
                self.grid.setdefault(key, []).append(s)

    @staticmethod
    def _bb(s):
        x0, y0, x1, y1 = s.bbox()
        # a wife's second strand and a bar's lie a few px off the piece
        return x0 - 6, y0 - 6, x1 + 6, y1 + 6

    def _cells(self, x0, y0, x1, y1):
        c = self.cell
        for i in range(int(math.floor(x0 / c)), int(math.floor(x1 / c)) + 1):
            for j in range(int(math.floor(y0 / c)),
                           int(math.floor(y1 / c)) + 1):
                yield i, j

    def query(self, x0, y0, x1, y1):
        out, seen = [], set()
        for key in self._cells(x0, y0, x1, y1):
            for s in self.grid.get(key, ()):
                if id(s) not in seen:
                    seen.add(id(s))
                    out.append(s)
        return out
