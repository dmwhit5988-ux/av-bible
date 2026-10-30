"""The lines that join a family, for the camera-read genealogy worlds.

1 Chronicles 1-9 is read as a camera over one laid-out tree
(`svg_chronicles_world`), and Matthew 1:1-17 as a camera over the same tree
on the spine layout (`svg_matthew_world`). Every box there stands where the
layout put it; this module decides how the lines between them run. It draws
a FAMILY, not one line per child, the way the wall chart
(`generate_ot_family_tree_svg.draw_edges`) does:

* A family whose children stand on one row gets a STEM from the parent's
  bottom centre, a BUS just above the row and a DROP into each child.
* A family whose children stand on several rows (a big family wraps) gets a
  RAIL down the left of the block, a SHELF out to each row and a drop into
  each child. A one-child row with almost no air above it is ENTERED from
  the side instead.
* A wife standing on her husband's row is joined by a MARRIAGE BAR between
  the facing edges; a second or third wife on the same side hangs from a
  COMB over the row, so no bar runs behind the wife nearer to him. Her
  children drop from her own box. A wife is `layout_regions.is_wife`, the
  one rule the regions layout also packs and rows her by; that layout
  stands every wife beside her husband. (The centred and spine layouts
  stand a wife in her sons' row, as a child of her husband, so they draw
  no bars: her drop is doubled in rose instead.)
* A child that is not below its parent at all gets a SIDE LINK (an elbow
  from the parent's facing side). None of the layouts produces any.

Rows are read from where the boxes stand (`rows_of`), never from a layout's
own bookkeeping, so any layout that places boxes can be drawn. Two things a
layout can say that positions cannot, both from the regions layout's Plan
(`layout_regions`), and both empty for the centred and spine layouts:

* LABELS. A house drawn as a small label, not a box, stands in the gap
  above the row of the people it gathers. It counts as standing in THAT row
  when its parent's family is sorted into rows, so a parent whose children
  are a mix of sons and labels gets one bus over the labels; the drop runs
  into the label's top and its own stem leaves from its bottom, so the
  label sits on the line. A label that heads a panel (it has a route) has
  its people in the panel, so it counts as standing in the row it hangs
  over, its parent's other children's.
* ROUTES. A panel head stands in the fan, far above the children in his
  panel. His stem runs from his box down to each waypoint's y and across to
  its x in turn, then down to the bus over his children. The layout puts
  the waypoints of different heads on shared lines (the trunk under the
  fan, a corridor's centre line, the line over a shelf), and here the
  stems are cut where they meet and drawn as ONE line system, a bus that
  branches off to each panel (Geometry._share_routes). Each piece is part
  of the path of every child beyond it, so it is drawn once in the
  brightest look among them, and an arrival traces his father's own way
  along it (trace_els: a long path draws its far part fast).

WHERE A RAIL GOES. Left of the whole block over its height: left of the
leftmost box among the children AND their descendants between the rail's
top and bottom, and left of any rail nested inside that span. The wall
chart's rule, left of the leftmost child, lands inside the block whenever
the first child is centred over a wide subtree — on the verse frames' sheet
it puts Ham's rail behind Dedan and Nimrod — and a parent's rail on the same
x as a nested family's merges the two, so Canaan would seem to hang off
Cush's rail. Rails are therefore placed deepest family first.

Every drawn piece is a `Seg` that knows which children's paths use it
(`serves`), so a verse can draw a shared bus once in the brightest look of
the people it leads to, and trace one arrival's own path from the parent
(`Geometry.chain`) on top.
"""

import math

from generate_ot_family_tree_svg import BG, DROP, FEMALE, SAND_DIM, dim
from layout_regions import LABEL_BOTTOM, is_wife
from svg_surface import _fmt, _opacity, _rgb

RAIL_OFF = 18       # a rail sits this far left of the leftmost box in its
                    # block (the layout leaves a 26 px gutter, SPINE)
RAIL_GAP = 8        # and at least this far left of a rail nested inside it
TRAY_GAP = 12       # a one-child row with less air than this above it is
                    # entered from the side
ROW_TOL = 1.0       # |dy| under which a wife stands on her husband's row
ARCH_LIFT = 8.0     # a comb to a 2nd, 3rd ... wife runs this far above the
                    # row (a bus runs DROP/2 above its row)
INSET = 1.0         # a line must reach this far into a box to count as
                    # passing behind it

STRAND_DX = 3.5     # the second strand of a wife's drop: the wall chart's
STRAND_DY = 5.0     # doubled line, offset right and starting lower
BEAD_R = 2.4        # the open bead on an implied (dashed) join,
BEAD_UP = 6.0       # this far above the child's box
DASH = "4 4"
TRACE_NEAR = 600.0  # the last this-many units of a long arrival path (the
TRACE_FAR = 0.5     # bus and drop the camera rests on) take the second half
                    # of its trace; everything before them, the first half


class Seg:
    """One axis-aligned piece of line.

    role: stem | bus | head | rail | shelf | drop | entry | side | bar |
    arch | route | trunk. style: solid | dash | wife | bar. fam: the parent
    whose family it belongs to (for a trunk, the first family sharing it).
    serves: the children whose path from the parent uses it. bead: an open
    bead at the child end (a dashed drop or entry)."""

    __slots__ = ("x0", "y0", "x1", "y1", "role", "style", "fam", "serves",
                 "bead")

    def __init__(self, x0, y0, x1, y1, role, style, fam, serves, bead=False):
        self.x0, self.y0, self.x1, self.y1 = x0, y0, x1, y1
        self.role, self.style, self.fam = role, style, fam
        self.serves = serves
        self.bead = bead

    @property
    def horizontal(self):
        return abs(self.y1 - self.y0) < 1e-6

    def bbox(self):
        return (min(self.x0, self.x1), min(self.y0, self.y1),
                max(self.x0, self.x1), max(self.y0, self.y1))

    def length(self):
        return abs(self.x1 - self.x0) + abs(self.y1 - self.y0)


def _shared_style(kids):
    """A piece shared only by dashed joins is dashed, one shared only by
    wives is a wife's; anything mixed is solid."""
    links = {k.link for k in kids}
    if links == {"dash"}:
        return "dash"
    if links == {"wife"}:
        return "wife"
    return "solid"


def _box_span(k):
    return k.y, k.y + k.h


def rows_of(kids, span=_box_span):
    """Boxes clustered into visual rows (at least half the shorter box's
    height shared with the row's first box), rows top to bottom, each left
    to right. `span(k)` -> (top, bottom) is where k counts as standing:
    its own box, or for a label the row it gathers (Geometry._span)."""
    sp = {k: span(k) for k in kids}

    def vov(a, b):
        (a0, a1), (b0, b1) = sp[a], sp[b]
        o = min(a1, b1) - max(a0, b0)
        return o / max(1e-9, min(a1 - a0, b1 - b0)) if o > 0 else 0.0
    rows = []
    for k in sorted(kids, key=lambda k: (sp[k][0], k.x)):
        for r in rows:
            if vov(r[0], k) >= 0.5:
                r.append(k)
                break
        else:
            rows.append([k])
    rows.sort(key=lambda r: min(sp[k][0] for k in r))
    for r in rows:
        r.sort(key=lambda k: k.x)
    return rows


def same_row(a, b, tol=ROW_TOL):
    return (abs(a.y - b.y) < tol or
            abs((a.y + a.h / 2) - (b.y + b.h / 2)) < tol)


def _depth(n):
    d = 0
    while n.parent is not None:
        n, d = n.parent, d + 1
    return d


class Geometry:
    """Every family's lines in a laid-out world, from positions only.

    `segs` is every piece in draw order; `node_segments[k]` the pieces on
    k's path from its parent. Built once per laid-out world: nothing here
    depends on the verse.

    `labels`: houses drawn as labels (they count as standing in the row
    they gather). `routes`: {parent: [(y, x), ...]}, the waypoints of a
    routed stem. Both come from the regions layout's Plan; the centred and
    spine layouts pass neither."""

    def __init__(self, nodes, labels=(), routes=None):
        self.nodes = list(nodes)
        self.labels = set(labels)
        self.routes = dict(routes or {})
        self.segs = []
        self.node_segments = {}
        self.families = {}          # parent -> plan (kind, rows, ...)
        self.bars = []              # (husband, wife, seg)
        self.side_links = []        # (parent, child)
        self._spans = {}
        self._routed = []           # (parent, stem polyline, children)
        for p in self.nodes:
            if not p.kids:
                continue
            beside = [k for k in p.kids
                      if is_wife(k) and same_row(p, k)
                      and (k.x >= p.x + p.w - 0.5 or k.x + k.w <= p.x + 0.5)]
            right = sorted((k for k in beside if k.x >= p.x + p.w - 0.5),
                           key=lambda k: k.x)
            left = sorted((k for k in beside if k not in right),
                          key=lambda k: -k.x)
            for side, ws in ((1, right), (-1, left)):
                if ws:
                    self._bar(p, ws[0])
                if len(ws) > 1:
                    self._comb(p, ws[1:], side)
            rest = [k for k in p.kids if k not in beside]
            if rest:
                self._family(p, rest)
        self._place_rails()
        for p, info in self.families.items():
            self._emit(p, info)
        self._share_routes()
        for s in self.segs:
            for k in s.serves:
                self.node_segments.setdefault(k, []).append(s)

    def _span(self, k):
        """Where k counts as standing when its family is sorted into rows:
        its box, or for a label the rows of the people it gathers. A label
        with a routed stem (a panel head drawn as a label) gathers nobody
        nearby, since its people are in its panel: it counts as standing in
        the row it hangs over, LABEL_BOTTOM under its own bottom."""
        if k not in self.labels or not k.kids:
            return k.y, k.y + k.h
        if k in self.routes:
            y = k.y + k.h + LABEL_BOTTOM
            return y, y + 1.0
        if k not in self._spans:
            ss = [self._span(c) for c in k.kids]
            self._spans[k] = (min(a for a, _b in ss), max(b for _a, b in ss))
        return self._spans[k]

    # -- pieces --------------------------------------------------------------

    def _add(self, *a, **kw):
        s = Seg(*a, **kw)
        if s.length() > 1e-6:
            self.segs.append(s)
        return s

    def _bar(self, p, wv):
        ym = (max(p.y, wv.y) + min(p.y + p.h, wv.y + wv.h)) / 2
        if wv.x >= p.x + p.w - 0.5:
            x0, x1 = p.x + p.w, wv.x
        else:
            x0, x1 = wv.x + wv.w, p.x
        s = self._add(x0, ym, x1, ym, "bar", "bar", p, frozenset([wv]))
        self.bars.append((p, wv, s))

    def _comb(self, p, ws, side):
        """The second, third ... wife on one side of her husband. A straight
        bar to her would run behind the wife between them and read as a
        marriage between the two women, so they are joined OVER the row: a
        line rises from the top of the husband's box (on their side, clear
        of the drop into his top centre), runs ARCH_LIFT above the row and
        drops into the top of each of them."""
        top = min([p.y] + [wv.y for wv in ws])
        y = top - ARCH_LIFT
        if side > 0:
            hx = max(p.x + p.w / 2 + 8, p.x + p.w - 10)
        else:
            hx = min(p.x + p.w / 2 - 8, p.x + 10)
        self._add(hx, p.y, hx, y, "arch", "bar", p, frozenset(ws))
        tg = [(wv.x + wv.w / 2, wv) for wv in ws]
        xs = sorted({hx} | {x for x, _w in tg})
        for a, b in zip(xs, xs[1:]):
            sv = frozenset(wv for x, wv in tg
                           if (x >= b if b > hx else x <= a))
            if sv:
                self._add(a, y, b, y, "arch", "bar", p, sv)
        for x, wv in tg:
            s = self._add(x, y, x, wv.y, "arch", "bar", p, frozenset([wv]))
            self.bars.append((p, wv, s))

    def _hline_pieces(self, y, x_from, targets, role, fam, extra=(),
                      far=None):
        """A horizontal line at y from x_from out to every target x, cut at
        each target. targets: [(x, node)]. A piece serves every node lying
        beyond it as seen from x_from; `extra` nodes ride every piece between
        x_from and `far` (the traffic bound for a rail)."""
        xs = sorted({x_from} | {x for x, _k in targets} |
                    ({far} if far is not None else set()))
        for a, b in zip(xs, xs[1:]):
            if b <= x_from:
                sv = {k for x, k in targets if x <= a}
            else:
                sv = {k for x, k in targets if x >= b}
            if far is not None and min(x_from, far) <= a and \
                    b <= max(x_from, far):
                sv |= set(extra)
            if not sv:
                continue
            self._add(a, y, b, y, role, _shared_style(sv), fam,
                      frozenset(sv))

    def _drop(self, k, x, y_from, fam):
        self._add(x, y_from, x, k.y, "drop", k.link, fam, frozenset([k]),
                  bead=(k.link == "dash"))

    def _family(self, p, kids):
        """Plan one family: its rows, bus or rail, and the height each row
        is entered at. Nothing is emitted yet, because a rail's x depends
        on the rails of the families nested inside it."""
        pb = p.y + p.h
        side = [k for k in kids if k.y < pb + 2]
        below = [k for k in kids if k not in side]
        for k in side:
            self._side(p, k)
        if not below:
            return
        rows = rows_of(below, self._span) if self.labels else rows_of(below)
        info = dict(rows=rows, kind="bus", below=below)
        self.families[p] = info
        if len(rows) == 1:
            top = min(k.y for k in rows[0])
            info["bus_y"] = top - min(DROP / 2, (top - pb) / 2)
            return
        info["kind"] = "rail"
        prev_bottom = pb
        entries = []                     # (y, row, mode)
        for r in rows:
            top = min(k.y for k in r)
            air = top - prev_bottom
            if len(r) == 1 and air < TRAY_GAP:
                k = r[0]
                entries.append((k.y + k.h / 2, r, "entry"))
            else:
                entries.append((top - min(DROP / 2, max(air, 0) / 2), r,
                                "shelf"))
            prev_bottom = max(k.y + k.h for k in r)
        top0 = min(k.y for k in rows[0])
        head = top0 - min(DROP / 2, (top0 - pb) / 2)
        if entries[0][2] == "shelf":
            head = entries[0][0]
        info["entries"] = entries
        info["head_y"] = head

    def _place_rails(self):
        """Each rail's x, deepest family first (see the module docstring)."""
        fams = sorted((p for p, f in self.families.items()
                       if f["kind"] == "rail"), key=lambda p: -_depth(p))
        for p in fams:
            info = self.families[p]
            lo, hi = info["head_y"], info["entries"][-1][0]
            xs = [k.x - RAIL_OFF for k in info["below"]]
            stack = list(info["below"])
            while stack:
                q = stack.pop()
                if q.y < hi and q.y + q.h > lo:
                    xs.append(q.x - RAIL_OFF)
                f = self.families.get(q)
                if f is not None and f["kind"] == "rail" and \
                        f["head_y"] < hi and f["entries"][-1][0] > lo:
                    xs.append(f["rail_x"] - RAIL_GAP)
                if q.y < hi:
                    stack.extend(q.kids)
            info["rail_x"] = min(xs)

    def _emit(self, p, info):
        pb, pcx = p.y + p.h, p.x + p.w / 2
        below = info["below"]
        route = self.routes.get(p)
        if route:
            # a panel's children stand on one generation row, so a routed
            # family is always a bus; anything else is a layout change that
            # must be looked at
            assert info["kind"] == "bus", \
                f"{p.label}'s routed family is not one row"
        if info["kind"] == "bus":
            row = info["rows"][0]
            bus = info["bus_y"]
            if route:
                # the stem's pieces are cut and shared with the other
                # routed stems once every family is planned (_share_routes)
                pts = [(pcx, pb)]
                for ly, lx in route:
                    pts += [(pts[-1][0], ly), (lx, ly)]
                pts.append((pts[-1][0], bus))
                self._routed.append((p, pts, frozenset(row)))
                pcx = pts[-1][0]
            else:
                self._add(pcx, pb, pcx, bus, "stem", _shared_style(row), p,
                          frozenset(row))
            tg = [(k.x + k.w / 2, k) for k in row]
            self._hline_pieces(bus, pcx, tg, "bus", p)
            for x, k in tg:
                self._drop(k, x, bus, p)
            return
        entries, head, rail_x = (info["entries"], info["head_y"],
                                 info["rail_x"])
        self._add(pcx, pb, pcx, head, "stem", _shared_style(below), p,
                  frozenset(below))
        rail_kids = set(below)
        if entries[0][2] == "shelf":
            r0 = entries[0][1]
            tg = [(k.x + k.w / 2, k) for k in r0]
            rail_kids -= set(r0)
            self._hline_pieces(head, pcx, tg, "head", p,
                               extra=rail_kids, far=rail_x)
            for x, k in tg:
                self._drop(k, x, head, p)
            later = entries[1:]
        else:
            self._hline_pieces(head, pcx, [], "head", p,
                               extra=rail_kids, far=rail_x)
            later = entries
        ys = [head] + [y for y, _r, _m in later]
        for i, (a, b) in enumerate(zip(ys, ys[1:])):
            sv = set()
            for _y, r, _m in later[i:]:
                sv |= set(r)
            self._add(rail_x, a, rail_x, b, "rail", _shared_style(sv), p,
                      frozenset(sv))
        for y, r, mode in later:
            if mode == "entry":
                k = r[0]
                self._add(rail_x, y, k.x, y, "entry", k.link, p,
                          frozenset([k]), bead=(k.link == "dash"))
            else:
                tg = [(k.x + k.w / 2, k) for k in r]
                self._hline_pieces(y, rail_x, tg, "shelf", p)
                for x, k in tg:
                    self._drop(k, x, y, p)

    def _side(self, p, k):
        self.side_links.append((p, k))
        pm, km = p.y + p.h / 2, k.y + k.h / 2
        sv = frozenset([k])
        if k.x >= p.x + p.w:
            x0, x1 = p.x + p.w, k.x
        elif k.x + k.w <= p.x:
            x0, x1 = p.x, k.x + k.w
        else:                                   # overlapping in x: from below
            x = k.x + k.w / 2
            self._add(x, p.y + p.h, x, k.y, "side", k.link, p, sv)
            return
        xm = (x0 + x1) / 2
        self._add(x0, pm, xm, pm, "side", k.link, p, sv)
        self._add(xm, pm, xm, km, "side", k.link, p, sv)
        self._add(xm, km, x1, km, "side", k.link, p, sv,
                  bead=(k.link == "dash"))

    def _share_routes(self):
        """The routed stems, drawn as one line system: THE TRUNK.

        The regions layout runs its routes on shared lines (one under the
        fan, one down each corridor, one over each shelf), so two stems that
        run together lie on exactly the same line. Every line a stem uses
        is cut wherever any stem joins or leaves it, and each piece is one
        Seg serving every child whose path crosses it, as a bus serves the
        brothers beyond each cut. So a shared stretch is drawn once, in the
        brightest look of the people it leads to, and a wide shot shows one
        thin line where parallel lanes would make a cable. A piece one stem
        alone uses keeps role "route"; one several share is "trunk", and
        its `fam` is the first of them, for the audit's wording. A child's
        path is still exactly his parent's stem, so his arrival traces from
        his father's box along the trunk to him."""
        lines = {}
        for p, pts, kids in self._routed:
            for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
                if abs(x1 - x0) + abs(y1 - y0) < 1e-6:
                    continue
                if abs(y1 - y0) < 1e-6:
                    key, lo, hi = ("h", y0), min(x0, x1), max(x0, x1)
                else:
                    key, lo, hi = ("v", x0), min(y0, y1), max(y0, y1)
                lines.setdefault(key, []).append((lo, hi, p, kids))
        for (axis, c), spans in lines.items():
            cuts = sorted({v for lo, hi, _p, _k in spans for v in (lo, hi)})
            pieces = []                     # [a, b, families, children]
            for a, b in zip(cuts, cuts[1:]):
                on = [(p, k) for lo, hi, p, k in spans if lo <= a and b <= hi]
                if not on:
                    continue
                fams = list(dict.fromkeys(p for p, _k in on))
                sv = frozenset().union(*(k for _p, k in on))
                if pieces and pieces[-1][1] == a and pieces[-1][3] == sv:
                    pieces[-1][1] = b
                else:
                    pieces.append([a, b, fams, sv])
            for a, b, fams, sv in pieces:
                role = "route" if len(fams) == 1 else "trunk"
                ends = (a, c, b, c) if axis == "h" else (c, a, c, b)
                self._add(*ends, role, _shared_style(sv), fams[0], sv)

    # -- one child's path ----------------------------------------------------

    def chain(self, n):
        """n's path from its parent, in order: [(seg, start, end)], each
        piece oriented away from the parent."""
        segs = list(self.node_segments.get(n, []))
        if not segs or n.parent is None:
            return []
        p = n.parent
        px, py = p.x + p.w / 2, p.y + p.h / 2

        def ends(s):
            return (s.x0, s.y0), (s.x1, s.y1)

        def dist(a, b):
            return math.hypot(a[0] - b[0], a[1] - b[1])

        first = min(segs, key=lambda s: min(dist(e, (px, py))
                                            for e in ends(s)))
        segs.remove(first)
        a, b = ends(first)
        if dist(b, (px, py)) < dist(a, (px, py)):
            a, b = b, a
        out = [(first, a, b)]
        cur = b
        while segs:
            nxt = min(segs, key=lambda s: min(dist(e, cur) for e in ends(s)))
            segs.remove(nxt)
            a, b = ends(nxt)
            if dist(b, cur) < dist(a, cur):
                a, b = b, a
            out.append((nxt, a, b))
            cur = b
        return out

    def node_polyline(self, n):
        """n's path from its parent as one polyline -> [(x, y), ...]."""
        return [pt for run in _runs(self.chain(n), lambda s: 0)
                for pt in run[1]]


# ===========================================================================
# What a path passes behind
# ===========================================================================

class _BoxIndex:
    def __init__(self, nodes, cell=256.0):
        self.cell = cell
        self.grid = {}
        for n in nodes:
            for key in self._cells(n.x, n.y, n.x + n.w, n.y + n.h):
                self.grid.setdefault(key, []).append(n)

    def _cells(self, x0, y0, x1, y1):
        c = self.cell
        for i in range(int(math.floor(x0 / c)), int(math.floor(x1 / c)) + 1):
            for j in range(int(math.floor(y0 / c)),
                           int(math.floor(y1 / c)) + 1):
                yield i, j

    def query(self, x0, y0, x1, y1):
        out = []
        seen = set()
        for key in self._cells(x0, y0, x1, y1):
            for n in self.grid.get(key, ()):
                if id(n) not in seen:
                    seen.add(id(n))
                    out.append(n)
        return out


def _line_hits_box(x0, y0, x1, y1, n, e=INSET):
    bx0, by0, bx1, by1 = n.x + e, n.y + e, n.x + n.w - e, n.y + n.h - e
    if bx0 >= bx1 or by0 >= by1:
        return False
    if abs(y1 - y0) < 1e-6:
        return by0 < y0 < by1 and min(x0, x1) < bx1 and max(x0, x1) > bx0
    return (bx0 < x0 < bx1 and min(y0, y1) < by1
            and max(y0, y1) > by0)


def strands(s):
    """The second strand drawn beside a wife's drop or entry, as a line
    (x0, y0, x1, y1), or None."""
    if s.style != "wife" or s.role not in ("drop", "entry"):
        return None
    if s.horizontal:
        return (s.x0 + STRAND_DY, s.y0 + STRAND_DX, s.x1, s.y1 + STRAND_DX)
    return (s.x0 + STRAND_DX, min(s.y0, s.y1) + STRAND_DY,
            s.x1 + STRAND_DX, max(s.y0, s.y1))


def through_boxes(geom, nodes=None, segs=None):
    """Every drawn line (pieces, the second strand of a wife's drop, and the
    second strand of a marriage bar or comb) that passes behind a box
    -> [(seg, box node)]. Boxes are drawn over lines, so a line through a
    box seems to leave from, or arrive at, the box it passes behind.
    `nodes` and `segs` narrow it to the boxes and pieces one file draws
    (the whole world's by default)."""
    nodes = geom.nodes if nodes is None else list(nodes)
    idx = _BoxIndex(nodes)
    hits = []
    for s in (geom.segs if segs is None else segs):
        for ln in _drawn_lines(s):
            bb = (min(ln[0], ln[2]), min(ln[1], ln[3]),
                  max(ln[0], ln[2]), max(ln[1], ln[3]))
            for n in idx.query(*bb):
                if _line_hits_box(*ln, n):
                    hits.append((s, n))
    return hits


def _drawn_lines(s):
    """A piece's ink as lines: the piece, and the second strand of a wife's
    drop or of a marriage bar or comb."""
    out = [(s.x0, s.y0, s.x1, s.y1)]
    st = strands(s)
    if st:
        out.append(st)
    if s.style == "bar":
        out.append(_bar_strand(s))
    return out


def overlapping(geom, tol=0.5, segs=None):
    """Pairs of different pieces lying on one line and sharing more than
    `tol` of it -> [(seg, seg)]. Two pieces on one stretch draw as one line
    and read as one family's: the routed stems' trunk is the one place
    lines are meant to be shared, and _share_routes makes each shared
    stretch a single piece, so on a sound drawing this is empty. `segs`
    narrows it to the pieces one file draws (the whole world's by
    default)."""
    on_line = {}
    for s in (geom.segs if segs is None else segs):
        for x0, y0, x1, y1 in _drawn_lines(s):
            if abs(y1 - y0) < 1e-6:
                key, lo, hi = ("h", round(y0, 2)), min(x0, x1), max(x0, x1)
            elif abs(x1 - x0) < 1e-6:
                key, lo, hi = ("v", round(x0, 2)), min(y0, y1), max(y0, y1)
            else:
                continue
            on_line.setdefault(key, []).append((lo, hi, s))
    out = []
    for spans in on_line.values():
        spans.sort(key=lambda t: t[0])
        for i, (lo, hi, s) in enumerate(spans):
            for lo2, hi2, s2 in spans[i + 1:]:
                if lo2 >= hi - tol:
                    break
                if s2 is not s and min(hi, hi2) - lo2 > tol:
                    out.append((s, s2))
    return out


# ===========================================================================
# Drawing
# ===========================================================================

def _colour(style):
    return FEMALE if style in ("wife", "bar") else SAND_DIM


def _runs(chain, key):
    """Chain pieces -> [(key, [points])], consecutive pieces with the same
    key joined into one polyline, collinear corners dropped."""
    out = []
    for s, a, b in chain:
        k = key(s)
        if not out or out[-1][0] != k:
            out.append((k, [a]))
        pts = out[-1][1]
        if math.hypot(a[0] - pts[-1][0], a[1] - pts[-1][1]) > 0.5:
            pts.append(a)
        pts.append(b)
    for _k, pts in out:
        i = 1
        while i < len(pts) - 1:
            (ax, ay), (bx, by), (cx, cy) = pts[i - 1], pts[i], pts[i + 1]
            if abs((bx - ax) * (cy - by) - (by - ay) * (cx - bx)) < 1e-6:
                del pts[i]
            else:
                i += 1
    return out


def _merged(lines):
    """Axis-aligned lines -> the same ink with collinear touching pieces
    joined, as path data."""
    hz, vt = {}, {}
    for x0, y0, x1, y1 in lines:
        if abs(y1 - y0) < 1e-6:
            hz.setdefault(_fmt(y0), []).append((min(x0, x1), max(x0, x1)))
        else:
            vt.setdefault(_fmt(x0), []).append((min(y0, y1), max(y0, y1)))
    d = []
    for table, horiz in ((hz, True), (vt, False)):
        for c, spans in table.items():
            spans.sort()
            joined = [list(spans[0])]
            for a, b in spans[1:]:
                if a <= joined[-1][1] + 0.01:
                    joined[-1][1] = max(joined[-1][1], b)
                else:
                    joined.append([a, b])
            for a, b in joined:
                d.append(f"M{_fmt(a)} {c}H{_fmt(b)}" if horiz
                         else f"M{c} {_fmt(a)}V{_fmt(b)}")
    return "".join(d)


def _bar_strand(s):
    """The second strand of a marriage bar or comb piece, as a line."""
    off = STRAND_DX
    return ((s.x0, s.y0 + off, s.x1, s.y1 + off) if s.horizontal
            else (s.x0 + off, s.y0, s.x1 + off, s.y1))


def static_els(segs, look_of, alpha, bead_fill=None):
    """The standing lines of one verse, each piece drawn ONCE.

    segs: the pieces to draw; look_of(seg) -> a look name; alpha: look ->
    opacity. One <path> per look and style, so a bus serving a dozen
    brothers is one stroke at one opacity rather than a dozen overlapping
    ones. -> (lines, fine): `lines` carry no stroke-width and inherit the
    connector width from their group; `fine` (the second strand of a
    wife's line, and the open beads, which must lie over the dashes) inherit
    a thinner one. bead_fill(x, y) -> the colour an open bead is filled
    with there (the background unless it says otherwise: inside a panel it
    is the panel's)."""
    main, second, beads = {}, {}, []
    for s in segs:
        look = look_of(s)
        main.setdefault((look, s.style), []).append(
            (s.x0, s.y0, s.x1, s.y1))
        st = strands(s)
        if st:
            second.setdefault(look, []).append(st)
        if s.style == "bar":
            # a marriage is doubled too, the second strand below the first
            second.setdefault(look, []).append(_bar_strand(s))
        if s.bead:
            col = dim(_colour(s.style), alpha[look])
            if s.horizontal:
                bx, by = s.x1 - BEAD_UP, s.y1
            else:
                bx, by = s.x1, max(s.y0, s.y1) - BEAD_UP
            fill = (bead_fill(bx, by) if bead_fill else None) or BG
            beads.append(
                f'<circle cx="{_fmt(bx)}" cy="{_fmt(by)}" r="{_fmt(BEAD_R)}" '
                f'fill="{_rgb(fill)}" stroke="{_rgb(col)}" '
                f'stroke-opacity="{_opacity(col):.3f}"/>')

    def path(d, col, dash=None):
        a = (f'<path d="{d}" fill="none" stroke="{_rgb(col)}" '
             f'stroke-opacity="{_opacity(col):.3f}"')
        if dash:
            a += f' stroke-dasharray="{dash}"'
        return a + "/>"

    lines = []
    for (look, style), ls in main.items():
        lines.append(path(_merged(ls), dim(_colour(style), alpha[look]),
                          DASH if style == "dash" else None))
    fine = [path(_merged(ls), dim(FEMALE, alpha[look]))
            for look, ls in second.items()]
    return lines, fine + beads


_EASE = "0.42 0 0.58 1"


def _traced(pts, col, width, total, d0, dur, split=None, begin="0s"):
    """A polyline revealed as the part of a longer path that starts d0
    along it: dash and gap of the whole path's length `total`, offset run
    from total + d0 down to d0 on the house ease, from `begin` (hidden
    until then).

    split = (R, f): the first R of the path is revealed by time fraction f
    (easing in) and the rest over the remainder (easing out), for a long
    path whose far part would otherwise take most of the time."""
    a = [f'points="{" ".join(f"{_fmt(x)},{_fmt(y)}" for x, y in pts)}"',
         'fill="none"', 'stroke-linejoin="round"',
         f'stroke="{_rgb(col)}"', f'stroke-width="{_fmt(width)}"',
         f'stroke-dasharray="{_fmt(total)}"',
         f'stroke-dashoffset="{_fmt(total + d0)}"']
    if _opacity(col) < 1:
        a.append(f'stroke-opacity="{_opacity(col):.3f}"')
    if split is None:
        anim = (f'<animate attributeName="stroke-dashoffset" '
                f'values="{_fmt(total + d0)};{_fmt(d0)}" dur="{dur}" '
                f'begin="{begin}" fill="freeze" calcMode="spline" '
                f'keyTimes="0;1" keySplines="{_EASE}"/>')
    else:
        r, f = split
        anim = (f'<animate attributeName="stroke-dashoffset" '
                f'values="{_fmt(total + d0)};{_fmt(total + d0 - r)};'
                f'{_fmt(d0)}" dur="{dur}" begin="{begin}" fill="freeze" '
                f'calcMode="spline" keyTimes="0;{f:.3f};1" '
                f'keySplines="0.42 0 1 1;0 0 0.58 1"/>')
    return f"<polyline {' '.join(a)}>{anim}</polyline>"


def trace_els(geom, n, alpha, width, fine_width, dur, begin="0s"):
    """n's path from its parent, drawing itself once over `dur`, from
    `begin` (a scene card lights a name mid-verse, as it is said).

    The path is cut where its colour changes — the stem and bus a wife
    shares with her husband's sons are sand, her own drop is rose — and
    every piece is revealed against the WHOLE path's length, so the pieces
    draw on as one continuous stroke. A piece starting d0 along a path of
    length L runs its dash offset from L + d0 down to d0 with a dash of L:
    exactly what one polyline over the whole path would show at every
    moment (and, for a path of one colour, exactly SvgCanvas.traced). The
    second strand of a wife's drop, and of a marriage bar or comb, draws
    with the piece it doubles.

    A LONG path draws its far part in the first half of the time and its
    last TRACE_NEAR units in the second. A panel head's routed stem runs
    over 10,000 px, and a head's bus across his panel thousands more; drawn
    at one speed, the drops into the boxes the camera rests on appeared
    only in the last instant."""
    chain = geom.chain(n)
    runs = _runs(chain, lambda s: _colour(s.style))
    total = sum(math.hypot(b[0] - a[0], b[1] - a[1])
                for _c, pts in runs for a, b in zip(pts, pts[1:]))
    split = None
    if total * (1 - TRACE_FAR) > TRACE_NEAR:
        split = (total - TRACE_NEAR, TRACE_FAR)
    out, d0 = [], 0.0
    for colour, pts in runs:
        out.append(_traced(pts, dim(colour, alpha), width, total, d0, dur,
                           split, begin))
        d0 += sum(math.hypot(b[0] - a[0], b[1] - a[1])
                  for a, b in zip(pts, pts[1:]))
    along = 0.0
    for s, a, b in chain:
        st = strands(s)
        if st:
            out.append(_traced([st[:2], st[2:]], dim(FEMALE, alpha),
                               fine_width, total, along + STRAND_DY, dur,
                               split, begin))
        elif s.style == "bar":
            ox, oy = (0.0, STRAND_DX) if s.horizontal else (STRAND_DX, 0.0)
            out.append(_traced([(a[0] + ox, a[1] + oy),
                                (b[0] + ox, b[1] + oy)], dim(FEMALE, alpha),
                               fine_width, total, along, dur, split, begin))
        along += math.hypot(b[0] - a[0], b[1] - a[1])
    return out
