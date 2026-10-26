"""The 1 Chronicles 1-9 world laid out in REGIONS: one fan, then a panel
per son of Israel.

The centred layout (the wall chart's, `generate_ot_family_tree_svg.
arrange/place`) hangs every family under its father and wraps a big family
into stacked rows. On the camera's world that has two costs. Israel's sons
each carry a house of hundreds, so in any centred tree they stand thousands
of px apart and 2:1-2 rests on a strip of specks. And boxes that stand
level read as one generation when they are not: a wrapped row puts later
brothers beside an earlier brother's grandsons.

This layout keeps one tree and makes its rows honest:

* THE FAN. Adam to Israel and his sons, with chapter 1's side branches, is
  one tidy tree in strict generation rows: every box stands on the row of
  its generation from Adam, so two boxes level with each other in the fan
  are the same generation.
* PANELS. Each of Israel's sons, the two houses his list ends with (the
  first to live again in their cities, the kings of Israel) and Esau are
  PANEL HEADS. A head's box stays in the fan, so 2:1-2 see the twelve
  together, and everything below him is laid out in his own panel, a
  rectangle titled with his name (EDOM for Esau). A routed line runs from
  the head down the gutters into his panel.
* INSIDE A PANEL the rows are generations too, counted on the same table as
  the fan. Brothers keep birth order on one row. A wife stands beside her
  husband (see COUPLES below), and a wife's children hang under her. A
  house that gathers people ("the kings of Edom", "princes in their
  families") is a small italic LABEL over the row of the people it
  gathers, not a box with a row of its own.
* PANELS ARE PACKED under the fan in three segments split by two
  corridors down Judah's flanks: Judah directly under the sons, the
  middle-born panels in shelves under Judah, and the elder and younger
  sons' panels in shelves to either side, in birth order. The first shelf
  of panels starts on the generation row after the sons, so across the fan
  and that shelf a row is a generation even across a panel border.

Horizontal packing everywhere is contour packing (Reingold and Tilford):
each subtree is packed against its left neighbour row by row, so a small
family slides under a big neighbour's overhang.

COUPLES are compact: a wife stands one marriage bar (WIFE_GAP) from her
husband, or from the wife before her on that side, whenever the buses of
the couple's children can still be kept apart. Otherwise each wife moves to
the near end of her own children's group, the husband stays over his, and
the bar grows. BAR_W prices a px of longer bar against a px of the husband
sliding off the middle of his own children. At 1.0 every couple on the tree
is compact except Caleb's: Hur's house under Ephrath is too wide for a
compact row to keep the buses of his four wives' children apart, so those
wives stand over their own children, up to about 3,500 px from him.

ONE RULE FOR A WIFE. `is_wife` (link "wife") decides both where a node is
packed and which row it stands on. Taking rows from one rule and packing
from another stands a wife on her husband's row while packing her as his
child, and the boxes overlap.

A REFERENCE CHIP (chronicles_tree.Tree.chip, a woman's name again in a
second family) goes by the same rule, through the link it keeps: under her
father it is one of his children, in his children's row (Leah and Rachel
under Laban, Milcah under Haran); under her first husband it is a wife on a
bar beside him (Ruth beside Mahlon). It is a leaf, and a smaller box
(`measure`) standing a little below its row's top so its middle is on the
row's name line (`top_of`); nothing else about it needs a rule here.

THE CONTRACT. `svg_chronicles_world.World` calls `arrange(root,
notes=False)` and then `place(root, 0, 0)`, as for every entry in its
LAYOUTS. Every node gets x, y, w, h; the root is centred on x = cx with its
top at y = top. What positions alone cannot say comes back from place() as
a `Plan`, which World keeps as `world.plan` (None under the centred and
spine layouts):

  plan.labels    houses drawn as a label on the line, not a box. Their w
                 and h are the label's (12 px italic, LABEL_H high), and
                 they stand in the gap above the row of the people they
                 gather; a family whose children are a mix of people and
                 labels is still one row.
  plan.routes    {node: [(y, x), ...]}: a panel head, or a head's wife whose
                 children are in the panel. Its stem leaves the box's bottom
                 centre, runs down to y and across to x for each point in
                 turn, and then down to the bus over its children.
  plan.panels    [Panel], each with its head, title, rect (x0, y0, x1, y1),
                 shelf, nodes, and title_side / title_room: the top corner
                 the entering lines leave free, and how wide it is.
  plan.panel_of  {node: Panel}, for every node in a panel; fan nodes are
                 not in it.
  plan.fan_box   the fan's bounding box.

A wife beside her husband needs no entry: she is link "wife", on his row
and clear of his box, which is how `svg_family_lines` finds a marriage
bar.

place() asserts what it assumes, so a change to the tree fails loudly here
instead of drawing nonsense: Isaac with Esau and Israel, Israel with the
twelve sons of 2:1-2 and a Judah, no "~heading" rows, every node placed
exactly once, and no two boxes or labels overlapping.
"""

import math

from chronicles_tree import walk
from generate_ot_family_tree_svg import measure, top_of
from generate_tabernacle import font

LABEL_PX = 12       # a house label's text: italic, this size
F_LABEL = font(LABEL_PX, italic=True)

SIB = 20            # gap between brothers in a row
GROUP_GAP = 40      # between one wife's children and the next group, and on
                    # either side of a house label
COUSIN = 44         # between different families' boxes in deeper rows
WIFE_GAP = 18       # husband to wife: the marriage bar
BUS_GAP = 16        # least gap between two parents' buses on one row
BAR_W = 1.0         # a px of longer marriage bar, priced against a px of the
                    # husband sliding off the middle of his children:
                    # COMPACT COUPLES (at 0.6 Leah stands about 1,000 px
                    # from Israel and Keturah 1,150 from Abraham)
DROP = 30           # a row's bottom to the next row's top, before labels
LABEL_H = 16
LABEL_PAD = 14      # label width over its text
LABEL_STEP = 30     # extra drop per level of labels over a row
LABEL_BOTTOM = 24   # a label's bottom to the top of the row it gathers
HEAD_COLUMN = 3     # rows kept clear under a head for his routed stem
COLUMN_PAD = 14     # half-width of that clear column
PANEL_PAD = 34      # a panel's rect round its content, sides and bottom
PANEL_TOP = 64      # and above its first row (title and bus)
GUTTER = 90         # clear gutter between panels
LANE = 9            # spacing of routed lanes
FAN_GAP = 70        # the fan's lowest box to the first routing lane
CORRIDOR_PAD = 26   # each side of a corridor's lanes
ASPECT = 1.75       # target width:height of the whole sheet
BALANCE_W = 1.0     # penalty for unequal left and right segments
SIDE_WIDTHS = [1500.0 + 500 * i for i in range(24)]   # tried for a segment

# Israel's sons, as 2:1-2 lists them. place() checks the tree against this:
# a son added, renamed or lost must be looked at, not silently laid out.
SONS = ("Reuben", "Simeon", "Levi", "Judah", "Issachar", "Zebulun", "Dan",
        "Joseph", "Benjamin", "Naphtali", "Gad", "Asher")


# =============================================================================
# What a node is
# =============================================================================

def is_wife(n):
    """A wife, or the mother a line is reckoned through: she stands beside
    her husband, on his row, and her children hang under her. The one rule
    both packing and rows use."""
    return n.parent is not None and n.link == "wife"


def is_house(n):
    """A house or company rather than one person."""
    return n.kind == "house"


def band_gen(root):
    """node -> its generation row, Adam = 0: one row down for each step
    from parent to child, none into a wife or a house (a house gathers
    people of its parent's children's generation)."""
    gen = {root: 0}
    stack = [root]
    while stack:
        p = stack.pop()
        for k in p.kids:
            gen[k] = gen[p] + (0 if is_wife(k) or is_house(k) else 1)
            stack.append(k)
    return gen


def label_w(n):
    return F_LABEL.getlength(n.label) + LABEL_PAD


def landmarks(root):
    """(Israel, Esau, Judah), found by where they stand, not by key: Isaac
    is the one man with sons named Esau and Israel."""
    isaacs = [n for n in walk(root) if n.label == "Isaac"
              and {"Esau", "Israel"} <= {k.label for k in n.kids}]
    assert len(isaacs) == 1, \
        f"expected one Isaac with sons Esau and Israel, found {len(isaacs)}"
    isaac = isaacs[0]

    def son(p, label):
        hits = [k for k in p.kids if k.label == label and not is_wife(k)]
        assert len(hits) == 1, \
            f"expected one {label} under {p.label}, found {len(hits)}"
        return hits[0]
    israel, esau = son(isaac, "Israel"), son(isaac, "Esau")
    sons = [k.label for k in israel.kids
            if not is_wife(k) and not is_house(k)]
    assert sorted(sons) == sorted(SONS), \
        f"Israel's sons are not the twelve of 2:1-2: {sons}"
    return israel, esau, son(israel, "Judah")


# =============================================================================
# Contour items
# =============================================================================

class Item:
    """A laid-out subtree with its anchor (centre x) at local 0.

    kind: "unit" (a person with the wives beside him) or "label" (a house
    drawn as a label). contour[d] = [left, right] of everything d rows below
    the item's own row (d = 0 is that row); kids = [(item, local anchor)];
    row = [(box node, local centre x)] for a unit."""

    __slots__ = ("node", "kind", "contour", "kids", "row")

    def __init__(self, node, kind):
        self.node, self.kind = node, kind
        self.contour = []
        self.kids = []
        self.row = []


def _merge(acc, cont, dx):
    for d, (lo, hi) in enumerate(cont):
        while len(acc) <= d:
            acc.append([math.inf, -math.inf])
        acc[d][0] = min(acc[d][0], lo + dx)
        acc[d][1] = max(acc[d][1], hi + dx)


def pack(items, gaps):
    """Contour-pack items left to right -> their anchors (the first at 0).
    gaps[i] separates item i from i-1 in the items' own row; deeper rows
    keep COUSIN."""
    acc, anchors = [], []
    for i, it in enumerate(items):
        if not anchors:
            x = 0.0
        else:
            x = -math.inf
            for d, (lo, _hi) in enumerate(it.contour):
                if d < len(acc) and acc[d][1] > -math.inf:
                    sep = gaps[i] if d == 0 else COUSIN
                    x = max(x, acc[d][1] + sep - lo)
            if x == -math.inf:
                x = anchors[-1]
        anchors.append(x)
        _merge(acc, it.contour, x)
    if len(items) > 2:
        _spread_leaves(items, gaps, anchors)
    return anchors


def _spread_leaves(items, gaps, anchors):
    """Childless brothers packed hard left before the first brother with
    children move right against him (Reingold and Tilford's apportioning,
    for the case that shows). Only the items' own row moves, so nothing can
    collide. A run BETWEEN two brothers with children stays packed against
    the left one: spreading it pulled 2:5's Hamul away from Hezron."""
    leaf = [len(it.contour) == 1 for it in items]
    n = len(items)
    i = 0
    while i < n:
        if not leaf[i]:
            i += 1
            continue
        j = i
        while j < n and leaf[j]:
            j += 1
        if j < n and i == 0:
            right_lim = anchors[j] + items[j].contour[0][0] - gaps[j]
            slack = right_lim - (anchors[j - 1] + items[j - 1].contour[0][1])
            if slack > 0.5:
                for k in range(i, j):
                    anchors[k] += slack
        i = j


def _group_gaps(groups):
    """A sequence of groups -> (flat items, gaps): SIB between brothers,
    GROUP_GAP between groups and either side of a label."""
    items, gaps = [], []
    for g in groups:
        for j, it in enumerate(g):
            items.append(it)
            if j == 0:
                gaps.append(GROUP_GAP if items[:-1] else 0)
            else:
                gaps.append(GROUP_GAP if (it.kind == "label" or
                                          g[j - 1].kind == "label")
                            else SIB)
    return items, gaps


def _side_configs(n):
    """Which side each wife with children stands on (+1 right, -1 left):
    all right, alternating (first right), all left."""
    if n == 0:
        return [[]]
    out = [[1] * n, [1 if i % 2 == 0 else -1 for i in range(n)], [-1] * n]
    seen, res = set(), []
    for c in out:
        if tuple(c) not in seen:
            seen.add(tuple(c))
            res.append(c)
    return res


def _end_anchored(P, row, owners, spans, want):
    """Row positions (group coordinates) when the compact row cannot keep
    the buses apart: P over the middle of his own group (or between his
    wives' groups), a wife with children over the near end of hers,
    childless wives against her husband; groups shift outward where a box
    would collide. -> (pos, group shift)."""
    gshift = [0.0] * len(owners)
    oi = {o: i for i, o in enumerate(owners)}
    ip = row.index(P)
    pos = {}
    if P in oi:
        s_ = spans[oi[P]]
        pos[P] = (s_[0] + s_[1]) / 2
    else:
        lefts = [o for o in owners if row.index(o) < ip]
        rights = [o for o in owners if row.index(o) > ip]
        if lefts and rights:
            pos[P] = (spans[oi[lefts[-1]]][1] + spans[oi[rights[0]]][0]) / 2
        else:
            pos[P] = want
    sh, prev = 0.0, pos[P] + P.w / 2
    for b in row[ip + 1:]:
        need = prev + WIFE_GAP + b.w / 2
        if b in oi:
            c = spans[oi[b]][0] + sh
            if c < need:
                sh += need - c
                c = need
            for j in range(oi[b], len(owners)):
                if row.index(owners[j]) > ip:
                    gshift[j] = sh
        else:
            c = need
        pos[b] = c
        prev = c + b.w / 2
    sh, prev = 0.0, pos[P] - P.w / 2
    for b in reversed(row[:ip]):
        need = prev - WIFE_GAP - b.w / 2
        if b in oi:
            c = spans[oi[b]][1] + sh
            if c > need:
                sh += need - c
                c = need
            for j in range(0, oi[b] + 1):
                if row.index(owners[j]) < ip:
                    gshift[j] = sh
        else:
            c = need
        pos[b] = c
        prev = c - b.w / 2
    return pos, gshift


def _place_item(it, cx, out):
    """Absolute x for an item and everything under it; appends each node."""
    if it.kind == "label":
        it.node.x = cx - it.node.w / 2
        out.append(it.node)
    else:
        for b, c in it.row:
            b.x = cx + c - b.w / 2
            out.append(b)
    for ch, a in it.kids:
        _place_item(ch, cx + a, out)


# =============================================================================
# The plan
# =============================================================================

class Panel:
    """One panel: a head's descendants, in a titled rectangle."""

    __slots__ = ("head", "title", "nodes", "owners", "rect_local", "rect",
                 "shelf", "corridor", "title_side", "title_room")

    def __init__(self, head, title, nodes, owners):
        self.head, self.title = head, title
        self.nodes = nodes          # every node in the panel
        self.owners = owners        # [(head or his wife, her children)]
        self.rect_local = self.rect = None
        self.shelf = self.corridor = None   # corridor: "L", "R" or None
        self.title_side, self.title_room = "left", 0.0

    def __repr__(self):
        return f"<Panel {self.title} shelf {self.shelf}>"


class Plan:
    """What the layout knows that positions cannot say (see the module
    docstring)."""

    __slots__ = ("labels", "routes", "panels", "panel_of", "fan_box")

    def __init__(self):
        self.labels = set()
        self.routes = {}
        self.panels = []
        self.panel_of = {}
        self.fan_box = None


# =============================================================================
# The layout
# =============================================================================

class Layout:
    """One run of the layout over a measured tree. All state is on the
    instance."""

    def __init__(self, root):
        tilde = [n.label for n in walk(root) if n.label.startswith("~")]
        assert not tilde, f"heading rows left in the tree: {tilde}"
        self.root = root
        self.gen_all = band_gen(root)
        self.israel, self.esau, self.judah = landmarks(root)
        self.heads = [self.esau] + [k for k in self.israel.kids
                                    if not is_wife(k)]
        self.head_set = set(self.heads)
        self.plan = Plan()

    # -- rows ------------------------------------------------------------------

    def gen(self, n):
        """The generation row a node stands on. A house BOX (a house with
        nobody under it, or a head) stands in its parent's children's row;
        a label is placed from the row it gathers, gen + 1."""
        g = self.gen_all[n]
        if is_house(n) and (not n.kids or n in self.head_set):
            g += 1
        return g

    # -- items -----------------------------------------------------------------

    def child_items(self, P):
        return [self.make_item(k) for k in P.kids if not is_wife(k)]

    def make_item(self, k):
        if is_house(k) and k.kids and k not in self.head_set:
            return self.label_item(k)
        return self.unit_item(k)

    def label_item(self, H):
        it = Item(H, "label")
        items, gaps = _group_gaps([self.child_items(H)])
        anchors = pack(items, gaps)
        H.w, H.h = label_w(H), LABEL_H
        self.plan.labels.add(H)
        mid = (anchors[0] + anchors[-1]) / 2 if anchors else 0.0
        cont = [[-H.w / 2, H.w / 2]]
        for a, ch in zip(anchors, items):
            _merge(cont, ch.contour, a - mid)
            it.kids.append((ch, a - mid))
        it.contour = cont
        return it

    def unit_item(self, P):
        """A person with the wives who stand beside him, and the row of
        children under them. A head gets his row only: his children go to
        his panel.

        Wives with children are tried all right, alternating (first right)
        and all left; childless wives fill in nearest the husband,
        balancing the sides. Each wife's children are a group under her
        and P's own a group under him, groups in the row's order. Two
        candidates per arrangement: the COMPACT row (bars WIFE_GAP long,
        P free to slide off the middle of his children while every bus
        stays clear of the next), and the END row (each wife over the near
        end of her own group, P centred over his). The cheaper wins: the
        slide in px, or the extra bar length times BAR_W."""
        it = Item(P, "unit")
        wives = [k for k in P.kids if is_wife(k)]
        head = P in self.head_set
        own = [] if head else self.child_items(P)
        wg = {wv: ([] if head else self.child_items(wv)) for wv in wives}
        kidw = [wv for wv in wives if wg[wv]]
        nokid = [wv for wv in wives if not wg[wv]]
        best = None
        for cfg_i, sides in enumerate(_side_configs(len(kidw))):
            R = [wv for wv, sd in zip(kidw, sides) if sd > 0]
            L = [wv for wv, sd in zip(kidw, sides) if sd < 0]
            nr, nl = [], []
            for wv in nokid:
                if len(L) + len(nl) < len(R) + len(nr):
                    nl.append(wv)
                else:
                    nr.append(wv)
            row = list(reversed(nl + L)) + [P] + nr + R
            rc, x = {}, 0.0
            for i, b_ in enumerate(row):
                if i:
                    x += row[i - 1].w / 2 + WIFE_GAP + b_.w / 2
                rc[b_] = x
            p0 = rc[P]
            for b_ in row:
                rc[b_] -= p0
            owners = list(reversed(L)) + ([P] if own else []) + R
            groups = [own if o is P else wg[o] for o in owners]
            items, gaps = _group_gaps(groups)
            if not items:
                best = (0, 0, row, rc, owners, groups, [], [], None)
                break
            anchors = pack(items, gaps)
            spans, k = [], 0
            for g in groups:
                spans.append([anchors[k], anchors[k + len(g) - 1]])
                k += len(g)
            lo, hi = -math.inf, math.inf
            for i in range(len(owners) - 1):
                oi, oj = owners[i], owners[i + 1]
                lo = max(lo, spans[i][1] + BUS_GAP - rc[oj])
                hi = min(hi, spans[i + 1][0] - BUS_GAP - rc[oi])
            if P in owners:
                s_ = spans[owners.index(P)]
                want = (s_[0] + s_[1]) / 2
            else:
                want = (anchors[0] + anchors[-1]) / 2
            cands = []
            if lo <= hi:
                t = min(max(want, lo), hi)
                cands.append((abs(t - want) + 0.5 * cfg_i, ("compact", t)))
            pos, gsh = _end_anchored(P, row, owners, spans, want)
            extra = sum(abs(pos[b_] - pos[P]) - abs(rc[b_])
                        for b_ in row if b_ is not P)
            # A wife pushed out along the row must not land among her
            # husband's brothers (under their father's bus she reads as his
            # sister, as Leah did under Isaac's): only on a side where P
            # has no brothers.
            sib = [k for k in (P.parent.kids if P.parent is not None else [])
                   if not is_wife(k)]
            ip = sib.index(P) if P in sib else 0
            safe_l, safe_r = ip == 0, ip == len(sib) - 1
            moved_bad = any(
                abs(pos[b_] - pos[P]) - abs(rc[b_]) > 40 and
                ((pos[b_] < pos[P] and not safe_l) or
                 (pos[b_] > pos[P] and not safe_r))
                for b_ in row if b_ is not P)
            if not moved_bad or not cands:
                cands.append((BAR_W * max(0.0, extra) + 0.5 * cfg_i + 1.0
                              + (1e6 if moved_bad else 0.0),
                              ("end", pos, gsh)))
            for cost, sol in cands:
                if best is None or cost < best[0]:
                    best = (cost, cfg_i, row, rc, owners, groups, anchors,
                            spans, sol)
        _c, _ci, row, rc, owners, groups, anchors, spans, sol = best
        if sol is not None:
            gshift = [0.0] * len(groups)
            if sol[0] == "compact":
                t = sol[1]
                pos = {b_: rc[b_] + t for b_ in row}
            else:
                pos, gshift = sol[1], sol[2]
                t = pos[P]
            k, acc = 0, []
            for gi, g in enumerate(groups):
                for ch in g:
                    a_ = anchors[k] + gshift[gi] - t
                    it.kids.append((ch, a_))
                    _merge(acc, ch.contour, a_)
                    k += 1
            rc = {b_: pos[b_] - t for b_ in row}
            it.contour = [[min(rc[b_] - b_.w / 2 for b_ in row),
                           max(rc[b_] + b_.w / 2 for b_ in row)]] + acc
        else:
            it.contour = [[min(rc[b_] - b_.w / 2 for b_ in row),
                           max(rc[b_] + b_.w / 2 for b_ in row)]]
        if head:
            # a clear column under the head (and under each wife whose
            # children are in the panel): the routed stem drops through it
            # to the lanes under the fan
            cols = [rc[P]] + [rc[wv] for wv in wives
                              if any(not is_wife(k) for k in wv.kids)]
            lo_c, hi_c = min(cols) - COLUMN_PAD, max(cols) + COLUMN_PAD
            for _d in range(HEAD_COLUMN):
                it.contour.append([lo_c, hi_c])
        it.row = [(b, rc[b]) for b in row]
        return it

    # -- the run ---------------------------------------------------------------

    def run(self):
        fan = self.unit_item(self.root)
        self.fan_nodes = []
        _place_item(fan, 0.0, self.fan_nodes)
        self.panels = []
        for hd in self.heads:
            groups = [(o, g) for o, g in
                      [(hd, self.child_items(hd))] +
                      [(wv, self.child_items(wv)) for wv in hd.kids
                       if is_wife(wv)]
                      if g]
            if not groups:
                continue
            items, gaps = _group_gaps([g for _o, g in groups])
            anchors = pack(items, gaps)
            nodes, owners, k = [], [], 0
            for o, g in groups:
                for ch in g:
                    _place_item(ch, anchors[k], nodes)
                    k += 1
                owners.append(o)
            title = "EDOM" if hd is self.esau else hd.label.upper()
            self.panels.append(Panel(hd, title, nodes, owners))
        self._bands()
        self._y_fan()
        self._pack()
        self._route()
        return self

    # -- the band table --------------------------------------------------------

    def _label_level(self, n):
        lv = 0
        for k in n.kids:
            if k in self.plan.labels:
                lv = max(lv, self._label_level(k))
        return lv + 1

    def _bands(self):
        """One height per generation over the whole world: a row is as tall
        as its tallest box, and the drop into it grows by LABEL_STEP for
        each level of labels over it."""
        rowh, lv = {}, {}
        for n in self.fan_nodes + [n for p in self.panels for n in p.nodes]:
            if n in self.plan.labels:
                g = self.gen(n) + 1
                lv[g] = max(lv.get(g, 0), self._label_level(n))
            else:
                g = self.gen(n)
                rowh[g] = max(rowh.get(g, 0), n.h)
        gmin, gmax = min(rowh), max(rowh)
        self.head_gen = max(self.gen(h) for h in self.heads
                            if not is_house(h))
        Y = {gmin: 0.0}
        for g in range(gmin + 1, gmax + 2):
            Y[g] = (Y[g - 1] + rowh.get(g - 1, 35) + DROP
                    + LABEL_STEP * lv.get(g, 0))
        self.Y = Y

    def _y_node(self, n, y_of_gen):
        if n in self.plan.labels:
            n.y = (y_of_gen(self.gen(n) + 1) - LABEL_BOTTOM - LABEL_H
                   - (self._label_level(n) - 1) * LABEL_STEP)
        else:
            n.y = top_of(n, y_of_gen(self.gen(n)))

    def _y_fan(self):
        for n in self.fan_nodes:
            self._y_node(n, lambda g: self.Y[g])
        self.fan_bottom = max(n.y + n.h for n in self.fan_nodes)
        self.fan_box = (min(n.x for n in self.fan_nodes),
                        min(n.y for n in self.fan_nodes),
                        max(n.x + n.w for n in self.fan_nodes),
                        self.fan_bottom)

    # -- panels ----------------------------------------------------------------

    def _panel_local(self, p):
        """A panel's content on the global band table, local y = 0 on the
        row of ref_gen (the tribes' first row), so every panel of a shelf
        shares one generation grid. Edom and the kings of Israel, whose
        first row is a generation higher, start one row higher."""
        base = self.Y[self.ref_gen]
        for n in p.nodes:
            self._y_node(n, lambda g: self.Y[g] - base)
        x0 = min(n.x for n in p.nodes)
        x1 = max(n.x + n.w for n in p.nodes)
        y0 = min(n.y for n in p.nodes)
        y1 = max(n.y + n.h for n in p.nodes)
        p.rect_local = (x0 - PANEL_PAD, y0 - PANEL_TOP, x1 + PANEL_PAD,
                        y1 + PANEL_PAD)

    @staticmethod
    def _W(p):
        return p.rect_local[2] - p.rect_local[0]

    @staticmethod
    def _H(p):
        return p.rect_local[3] - p.rect_local[1]

    @staticmethod
    def _hx(p):
        return p.head.x + p.head.w / 2

    def _fill(self, side, width):
        shelves, cur, cw = [], [], 0.0
        for p in side:
            step = self._W(p) + (GUTTER if cur else 0)
            if cur and cw + step > width:
                shelves.append(cur)
                cur, cw = [p], self._W(p)
            else:
                cur.append(p)
                cw += step
        if cur:
            shelves.append(cur)
        return shelves

    def _put(self, p, x, row0, shelf):
        rl = p.rect_local
        dx = x - rl[0]
        for n in p.nodes:
            n.x += dx
            n.y += row0
        p.rect = (x, row0 + rl[1], x + rl[2] - rl[0], row0 + rl[3])
        p.shelf = shelf

    def _pack(self):
        """THREE SEGMENTS under the fan, split by two CORRIDORS that run
        straight down Judah's flanks.

        Middle: JUDAH directly under the sons (chapters 2-4 sit right below
        the fan, and 2:4's Tamar is close to her sons), then the middle-born
        panels in birth order in shelves no wider than Judah. Left: a prefix
        of the birth order (Edom, Reuben ...) in shelves ending at the left
        corridor. Right: a suffix (... Asher, the kings of Israel) in
        shelves starting at the right corridor. A route to the first shelf
        of any segment goes straight down from the lanes under the fan; a
        route to a lower shelf goes down the corridor on its side and
        across the gutter above its shelf, so no corridor crosses a panel.
        The split and the side width are searched for a small sheet near
        ASPECT."""
        self.ref_gen = self.head_gen + 1
        for p in self.panels:
            self._panel_local(p)
        W, Hh = self._W, self._H
        order = sorted(self.panels, key=self._hx)
        jud = [p for p in order if p.head is self.judah]
        assert len(jud) == 1, "Judah has no panel"
        jud = jud[0]
        ji = order.index(jud)
        n_routes = sum(len(p.owners) for p in self.panels)
        corr_w = 2 * CORRIDOR_PAD + n_routes * LANE
        lane_band0 = n_routes * LANE + 30

        def band(k):
            return max(1, k) * LANE + 36
        fan_h = self.fan_bottom - self.fan_box[1]
        Wj = W(jud)

        def seg_height(shelves, top_shared=True):
            h = 0.0
            for i, s in enumerate(shelves):
                nr = sum(len(p.owners) for p in s)
                if i or not top_shared:
                    h += band(nr) + GUTTER
                h += max(Hh(p) for p in s)
            return h

        def width_of(shelves):
            return max([sum(W(p) for p in s) + GUTTER * (len(s) - 1)
                        for s in shelves] or [0.0])
        best = None
        pre, suf = order[:ji], order[ji + 1:]
        for kl in range(0, len(pre) + 1):
            for kr in range(0, len(suf) + 1):
                L = pre[:kl]
                R = suf[len(suf) - kr:] if kr else []
                M = pre[kl:] + suf[:len(suf) - kr]
                if any(W(p) > Wj for p in M):
                    continue
                for ws in [0.0] + SIDE_WIDTHS:
                    if (L or R) and ws == 0.0:
                        continue
                    if any(W(p) > ws for p in L + R):
                        continue
                    sl = self._fill(L, ws) if L else []
                    sr = self._fill(R, ws) if R else []
                    sm = self._fill(M, Wj) if M else []
                    hm = Hh(jud) + (seg_height(sm, top_shared=False)
                                    if sm else 0.0)
                    wl, wr = width_of(sl), width_of(sr)
                    width = max(Wj + 2 * corr_w + wl + wr,
                                self.fan_box[2] - self.fan_box[0])
                    height = fan_h + FAN_GAP + lane_band0 + \
                        max(seg_height(sl), seg_height(sr), hm)
                    # the fan sits over Judah: keep the two sides level so
                    # the sheet is not lopsided under it
                    bal = abs(wl - wr) / max(width, 1.0)
                    score = width * height * (
                        1 + 1.5 * abs(math.log(width / height / ASPECT))
                        + BALANCE_W * bal)
                    if best is None or score < best[0]:
                        best = (score, sl, sr, sm)
        _s, sl, sr, sm = best
        y_top = self.fan_bottom + FAN_GAP + lane_band0
        self.shelf_lane_top = {0: self.fan_bottom + FAN_GAP}
        # Judah, placed so that his own children sit under him
        kx = [k.x + k.w / 2 for k in jud.nodes
              if k.parent is jud.head or (
                  k.parent is not None and k.parent.parent is jud.head
                  and is_wife(k.parent))]
        kmid = (min(kx) + max(kx)) / 2 if kx else \
            (jud.rect_local[0] + jud.rect_local[2]) / 2
        jx0 = self._hx(jud) - (kmid - jud.rect_local[0])
        first = [jud] + (sl[0] if sl else []) + (sr[0] if sr else [])
        row0 = y_top + max(-p.rect_local[1] for p in first)
        self._put(jud, jx0, row0, 0)
        lc = jx0 - corr_w / 2
        rc = jud.rect[2] + corr_w / 2
        self.corridors = {"L": lc, "R": rc}
        self.shelves = []
        shelf_id = 0

        def put_shelf(s, xs, y_top_, cid, sid):
            r0 = y_top_ + max(-p.rect_local[1] for p in s)
            for p, x in zip(s, xs):
                self._put(p, x, r0, sid)
                p.corridor = cid
            return max(p.rect[3] for p in s)

        def left_xs(s):
            tw = sum(W(p) for p in s) + GUTTER * (len(s) - 1)
            x, out = lc - corr_w / 2 - tw, []
            for p in s:
                out.append(x)
                x += W(p) + GUTTER
            return out

        def right_xs(s):
            x, out = rc + corr_w / 2, []
            for p in s:
                out.append(x)
                x += W(p) + GUTTER
            return out

        def mid_xs(s):
            tw = sum(W(p) for p in s) + GUTTER * (len(s) - 1)
            x, out = (lc + rc) / 2 - tw / 2, []
            for p in s:
                out.append(x)
                x += W(p) + GUTTER
            return out
        shelf0 = [jud]
        for seg, shelves, xs_f in (("L", sl, left_xs), ("R", sr, right_xs)):
            yb = None
            for i, s in enumerate(shelves):
                s = sorted(s, key=self._hx)      # birth order on the shelf
                if i == 0:
                    for p, x in zip(s, xs_f(s)):
                        self._put(p, x, row0, 0)
                    shelf0 += s
                    yb = max(p.rect[3] for p in s)
                    continue
                shelf_id += 1
                nr = sum(len(p.owners) for p in s)
                lt = yb + GUTTER
                self.shelf_lane_top[shelf_id] = lt
                yb = put_shelf(s, xs_f(s), lt + band(nr), seg, shelf_id)
                self.shelves.append(list(s))
        yb = jud.rect[3]
        for s in sm:
            shelf_id += 1
            nr = sum(len(p.owners) for p in s)
            lt = yb + GUTTER
            self.shelf_lane_top[shelf_id] = lt
            yb = put_shelf(s, mid_xs(s), lt + band(nr), None, shelf_id)
            for p in s:                         # the nearer corridor
                cxp = p.rect[0] + W(p) / 2
                p.corridor = "L" if cxp < (lc + rc) / 2 else "R"
            self.shelves.append(list(s))
        self.shelves.insert(0, sorted(shelf0, key=lambda p: p.rect[0]))

    # -- routes ----------------------------------------------------------------

    def _route(self):
        """Every head (and wife of a head) whose children are in a panel
        gets a route: down from the box to its own lane under the fan,
        across to the panel (first shelf) or to its own lane in a
        corridor, down the corridor, across its own lane in the gutter
        above its shelf, and down into the panel's bus.

        Lanes are ordered so that routes do not cross where the geometry
        allows: in a corridor, routes branching left sit left (shallower
        shelf further left; same shelf by target x) and routes branching
        right sit right (shallower further right); in a shelf's gutter a
        route branching further out turns higher; under the fan, leftward
        routes give the higher lane to the source further left, and
        rightward ones mirror that."""
        lane0 = self.fan_bottom + FAN_GAP
        reqs = []
        for p in self.panels:
            pn = set(p.nodes)
            for o in p.owners:
                kids = [k for k in o.kids if not is_wife(k) and k in pn]
                kxs = [k.x + k.w / 2 for k in kids]
                sx = o.x + o.w / 2
                kmin, kmax = min(kxs), max(kxs)
                if p.corridor is None:          # straight down if it can
                    ex = min(max(sx, kmin), kmax)
                else:                           # the end nearest the corridor
                    cx = self.corridors[p.corridor]
                    ex = kmin if cx < kmin else (kmax if cx > kmax else cx)
                reqs.append(dict(o=o, p=p, sx=sx, ex=ex))
        for cid, cx in self.corridors.items():
            rs = [r for r in reqs if r["p"].corridor == cid]
            lb = sorted([r for r in rs if r["ex"] < cx],
                        key=lambda r: (r["p"].shelf, r["ex"]))
            rb = sorted([r for r in rs if r["ex"] >= cx],
                        key=lambda r: (-r["p"].shelf, r["ex"]))
            seq = lb + rb
            for i, r in enumerate(seq):
                r["x1"] = cx + (i - (len(seq) - 1) / 2) * LANE
        for r in reqs:
            if r["p"].corridor is None:
                r["x1"] = r["ex"]
        left = sorted([r for r in reqs if r["x1"] < r["sx"]],
                      key=lambda r: r["sx"])
        right = sorted([r for r in reqs if r["x1"] >= r["sx"]],
                       key=lambda r: -r["sx"])
        for i, r in enumerate(left + right):
            r["lane"] = lane0 + i * LANE
        for s in range(1, len(self.shelves)):
            rs = [r for r in reqs if r["p"].shelf == s]
            lt = self.shelf_lane_top[s] + 6
            lft = sorted([r for r in rs if r["ex"] < r["x1"]],
                         key=lambda r: r["ex"])
            rgt = sorted([r for r in rs if r["ex"] >= r["x1"]],
                         key=lambda r: -r["ex"])
            for i, r in enumerate(lft):
                r["lane2"] = lt + i * LANE
            for i, r in enumerate(rgt):
                r["lane2"] = lt + i * LANE
        for r in reqs:
            if r["p"].corridor is None:
                route = [(r["lane"], r["ex"])]
            else:
                route = [(r["lane"], r["x1"]), (r["lane2"], r["ex"])]
            self.plan.routes[r["o"]] = route
        # a title goes in the top corner the entering lines leave free, and
        # is sized by the renderer to fit that room
        for p in self.panels:
            exs = [r["ex"] for r in reqs if r["p"] is p]
            x0, _y0, x1, _y1 = p.rect
            room_l = (min(exs) - 18) - (x0 + 20) if exs else x1 - x0 - 40
            room_r = (x1 - 20) - (max(exs) + 18) if exs else 0
            if room_l >= room_r:
                p.title_side, p.title_room = "left", max(room_l, 0.0)
            else:
                p.title_side, p.title_room = "right", max(room_r, 0.0)

    # -- the result ------------------------------------------------------------

    def finish(self, cx, top):
        """Move everything so the root is centred on cx with its top at
        `top`, fill the plan and check it."""
        dx = cx - (self.root.x + self.root.w / 2)
        dy = top - self.root.y
        plan = self.plan
        if dx or dy:
            for n in walk(self.root):
                n.x += dx
                n.y += dy
            for p in self.panels:
                x0, y0, x1, y1 = p.rect
                p.rect = (x0 + dx, y0 + dy, x1 + dx, y1 + dy)
            for o, route in plan.routes.items():
                plan.routes[o] = [(y + dy, x + dx) for y, x in route]
            x0, y0, x1, y1 = self.fan_box
            self.fan_box = (x0 + dx, y0 + dy, x1 + dx, y1 + dy)
        plan.panels = list(self.panels)
        plan.panel_of = {n: p for p in self.panels for n in p.nodes}
        plan.fan_box = self.fan_box
        self._check()
        return plan

    def _check(self):
        placed = self.fan_nodes + [n for p in self.panels for n in p.nodes]
        every = list(walk(self.root))
        assert len(placed) == len(set(placed)), "a node was placed twice"
        missing = [n.label for n in every if n not in set(placed)]
        assert not missing, f"nodes the layout never placed: {missing[:8]}"
        clash = overlaps(every)
        assert not clash, "boxes overlap: " + ", ".join(
            f"{a.label} / {b.label}" for a, b in clash[:8])
        rects = [p.rect for p in self.panels]
        for i, a in enumerate(rects):
            for b in rects[i + 1:]:
                assert not _rects_meet(a, b), "two panels overlap"
        fb = self.fan_box
        assert not any(_rects_meet(fb, r) for r in rects), \
            "a panel reaches into the fan"


def _rects_meet(a, b):
    return min(a[2], b[2]) > max(a[0], b[0]) and \
        min(a[3], b[3]) > max(a[1], b[1])


def overlaps(nodes):
    """Pairs of boxes (or labels) that overlap by more than a quarter px
    each way."""
    srt = sorted(nodes, key=lambda n: n.x)
    out = []
    for i, a in enumerate(srt):
        ax1 = a.x + a.w
        for b in srt[i + 1:]:
            if b.x >= ax1:
                break
            if min(ax1, b.x + b.w) - max(a.x, b.x) > 0.25 and \
                    min(a.y + a.h, b.y + b.h) - max(a.y, b.y) > 0.25:
                out.append((a, b))
    return out


# =============================================================================
# The World's two calls
# =============================================================================

def arrange(root, notes=False):
    """Name-only boxes for every node (the reading worlds never draw
    notes); the shape is decided in place()."""
    for n in walk(root):
        measure(n, notes=False)
    return root


def place(root, cx, top):
    """Lay the measured tree out in regions -> the Plan."""
    return Layout(root).run().finish(cx, top)
