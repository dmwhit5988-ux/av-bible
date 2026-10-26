"""Matthew 1:1-17 as a camera over the Old Testament family tree.

The same world, the same camera and the same frame as 1 Chronicles 1-9 —
`svg_chronicles_world.VerseFrame` does the drawing here, keeping the older
per-child elbow for its lines (`MatthewFrame.family_lines`), the older
cutaway card (`MatthewFrame.card_wives_beside`) and the older node cap
(`MatthewFrame.cap_pays_outside`) — with two differences that
come from what Matthew is doing:

  * THE OLD TESTAMENT IS ALREADY STANDING. In Chronicles a name arrives when
    the verse first reads it, because the reader is watching the family be
    built. Matthew is not building it; he is tracing a line down something
    finished. So every node the Old Testament carries is context from frame
    one, and only the fifteen names Matthew adds — Rahab, Bathsheba, Uriah
    and the twelve past Zerubbabel — grow in. When the line runs off the
    bottom of the Old Testament at verse 13 the sheet visibly extends, and
    that is the chapter's argument in one gesture.

  * THE CAMERA IS WALKING A LINE, NOT SURVEYING A FAMILY. Chronicles' verses
    are mostly "the sons of X" — wide rows, which is why the card and the
    veil exist. Matthew's are a descent: three or four boxes, one under the
    next, and the frame is nearly always tight. The wide machinery is still
    reached for by verses 1 and 17, which span the whole line on purpose.

  * AND SO IT USES THE SPINE LAYOUT (`arrange_spine`/`place_spine`), not the
    wall chart's centred one. A parent centred over its whole descent puts a
    line of descent on a sideways drift — every generation shifts by however
    much progeny the last man had — and the camera spends the chapter
    chasing a column that will not stand still. With the heir directly under
    his father the line is a straight vertical run: verse 3 went from a
    3,224 px flight to a 251 px nudge, the panoramas rest at 0.141 instead
    of 0.080, and no verse has to drop a name any more. 1 Chronicles and the
    wall chart still use the centred layout — see `arrange_spine` for what
    the spine costs (birth order).

Verse matching is not a resolver here. Matthew names forty-two people in
seventeen verses and `matthew_tree.READING` lists them; the hard part —
which Hezron, which Abijah — is settled in `matthew_tree.build()` by walking
the chain rather than searching for a label.

Rendered by generate_matthew1_svg.py.
"""

import os

import matthew_tree as MT
from chronicles_tree import walk
from generate_ot_family_tree_svg import (DROP, SIB_GAP, arrange_spine,
                                         place_spine)
from generate_tabernacle import W, H, F_TITLE, font
from svg_chronicles_world import (AUDIO_DIR, BG, HL, HUD_H, READABLE,
                                  SAND_DIM, TEXT, VIEW_BOT, VerseFrame,
                                  World, _fade_group, _fit, _grow_min,
                                  _mp3_seconds, _union, dim, node_box)
from passages import load_chapter
from svg_surface import SvgCanvas, SvgLayer, _fmt

BOOK, CHAPTER = "Matthew", 1

# Matthew's own divisions, plus the title verse and the summary. The HUD
# names the section, so a viewer who joins mid-chapter knows which of the
# three fourteens they are in.
# The two verses that mean to show the whole sheet. Verse 1 is the chapter's
# title and verse 17 its summary, and both name people the width of the tree
# apart on purpose — so these are the only two allowed to rest below reading
# scale.
PANORAMA = (1, 17)

SECTIONS = [
    (1, 1, "The book of the genealogy"),
    (2, 6, "Abraham to David"),
    (7, 11, "David to the exile"),
    (12, 16, "The exile to the Christ"),
    (17, 17, "Fourteen generations"),
]


def section_of(v):
    for lo, hi, title in SECTIONS:
        if lo <= v <= hi:
            return title
    return SECTIONS[-1][2]


def _web_verses():
    return dict(load_chapter(BOOK, CHAPTER).verses)


# ---------------------------------------------------------------------------
# Bringing the exiles in
# ---------------------------------------------------------------------------

EXILE_X = 900       # px from a parent's centre before a name counts as thrown
SMALL = 24          # nodes: how much subtree may travel with one of them
SLOT_PAD = 18


def _fit_scale(nodes):
    box = None
    for n in nodes:
        b = node_box(n)
        box = b if box is None else _union(box, b)
    return _fit(_grow_min(box), pad=70)[0]


def _afford(lit):
    """-> (kept, dropped). Drop the worst outlier until the frame reads.

    A SAFETY NET THAT NO LONGER FIRES. Under the centred layout this was
    load-bearing: verse 2 could not hold Judah (2,435 px below Jacob, because
    his row is Israel's twelve sons) and verse 3 could not hold Zerah. The
    spine layout puts Judah directly under Jacob — he is the heir, his is the
    biggest of Israel's descents — and `_settle_kin` recovers Zerah, so as of
    2026-08-20 every one of the seventeen verses keeps every name it reads.

    It stays because the rule it encodes is still the right one if a verse
    ever does overflow: be GREEDY ON THE OUTLIER, not on the reading order.
    Trimming the front or the back of a recital was the obvious rule and it
    was wrong — verse 3 would have had to throw away Judah and Perez, the two
    names the sentence is actually about, to be rid of Zerah, who is neither
    first nor last.
    """
    keep, gone = list(lit), []
    while len(keep) > 1 and _fit_scale(keep) < READABLE:
        worst = max(keep, key=lambda n: _fit_scale(
            [m for m in keep if m is not n]))
        keep.remove(worst)
        gone.append(worst)
    return keep, gone


def _settle_kin(nodes, named):
    """Bring back the names the chart's own layout threw across the sheet.

    The chart centres a parent over the whole SPAN of its children's
    subtrees. That is right for a wall chart and ruinous for a camera: a
    small child standing beside a huge sibling gets pushed out past the far
    edge of that sibling's subtree, however close the two of them are in the
    text. Three of Matthew's five women went that way — Ruth was laid out
    3,569 px from Boaz, with Obed's subtree (the rest of the Bible) between
    them — and so did Zerah, who ended up 4,000 px from Perez, his own twin,
    because Perez's subtree is 298 nodes and his is ten.

    So: any name in Matthew's reading that is standing more than EXILE_X
    from its parent, and whose own subtree is small enough to carry, moves
    to the nearest free slot on the parent's child row. Everyone else stays
    exactly where the chart put them.

    The size test is what keeps this honest: a name is only moved when it
    is small enough that its position is an artefact of the layout rather
    than a fact about the tree. Under the spine layout it recovers Zerah,
    Shealtiel and the three wives, all of them to within 220 px of their
    parent. Judah needs no help — he is the heir of Israel's descent and so
    stands directly under Jacob, at dx 0.
    """
    def free(box, moving):
        x0, y0, x1, y1 = box
        return not any(x0 - SLOT_PAD < n.x + n.w and x1 + SLOT_PAD > n.x
                       and y0 - SLOT_PAD < n.y + n.h and y1 + SLOT_PAD > n.y
                       for n in nodes if n not in moving)

    moved = []
    for w in named:
        p = w.parent
        if p is None:
            continue
        if abs((w.x + w.w / 2) - (p.x + p.w / 2)) < EXILE_X:
            continue
        moving = set(walk(w))
        if len(moving) > SMALL:
            continue
        # The subtree travels as one piece, so the slot has to clear the
        # whole of it — testing only the node's own box put Zerah's ten
        # descendants down through Perez's.
        sx0 = min(n.x for n in moving)
        sy0 = min(n.y for n in moving)
        sx1 = max(n.x + n.w for n in moving)
        sy1 = max(n.y + n.h for n in moving)
        y = p.y + p.h + DROP
        # Step out from the parent's own centre, left first: the heir sits
        # under them, and a name recovered like this reads as standing
        # beside the family rather than in front of it.
        cx = p.x + p.w / 2
        best = None
        for k in range(1, 60):
            for sign in (-1, 1):
                x = cx + sign * (k * (w.w + SIB_GAP)) - w.w / 2
                dx, dy = x - w.x, y - w.y
                if free((sx0 + dx, sy0 + dy, sx1 + dx, sy1 + dy), moving):
                    best = (dx, dy)
                    break
            if best:
                break
        if best is None:
            continue
        for n in moving:
            n.x += best[0]
            n.y += best[1]
        moved.append(w)
    return moved


class MatthewWorld(World):
    """The Old Testament tree with Matthew's line resolved onto it.

    Subclasses `World` for `focus_box`, `context_nodes` and the layout
    contract the camera depends on; the whole of `World.__init__` is
    replaced, because Matthew's reading is a list, not a resolver.
    """

    def __init__(self):
        self.tree, self.at = MT.build()
        self.root = self.tree.root
        # THE SPINE LAYOUT, not the wall chart's (user, 2026-08-20). A
        # genealogy is a line of descent, and under the centred layout that
        # line drifts sideways at every generation by however much progeny
        # the last man happened to have — the camera spends its life
        # chasing a column that will not stand still. Here the heir is
        # directly under his father and the line is a straight vertical
        # run. See arrange_spine for what it costs (birth order) and why
        # the wall chart and 1 Chronicles still use the other one.
        arrange_spine(self.root, notes=False)
        place_spine(self.root, 0, 0)
        self.plan = None            # the spine layout returns no plan

        self.nodes = list(walk(self.root))
        self.line = MT.MatthewLine(self.tree, self.at)

        # Every person Matthew names, in reading order and deduped — the
        # candidates for `_settle_kin`, and the reason it runs before the
        # world box is measured.
        named, seen = [], set()
        for v, _names in MT.READING:
            for n in self.line.lit[v]:
                if n not in seen:
                    seen.add(n)
                    named.append(n)
        self.settled = _settle_kin(self.nodes, named)
        self.world_box = (min(n.x for n in self.nodes),
                          min(n.y for n in self.nodes),
                          max(n.x + n.w for n in self.nodes),
                          max(n.y + n.h for n in self.nodes))

        texts = _web_verses()
        self.order, self.arrivals, self.lit = [], {}, {}
        self.first_of, self.narr = {}, {}
        self.dropped = {}       # (ch, v) -> nodes the frame could not afford
        for v, _names in MT.READING:
            key = (CHAPTER, v)
            self.order.append((CHAPTER, v, {"title": section_of(v)}))
            self.lit[key] = self.line.lit[v]
            self.arrivals[key] = self.line.arrivals[v]
            for n in self.line.arrivals[v]:
                self.first_of[n] = key
            sec = _mp3_seconds(os.path.join(
                AUDIO_DIR, "Matthew_%d_%d.mp3" % (CHAPTER, v)))
            if sec is None:
                sec = 0.40 * len(texts.get(v, "").split()) + 0.7
            self.narr[key] = sec

    def focus_box(self, ch, v):
        """Every name in the verse — minus any the frame cannot afford.

        TWO departures from `World.focus_box`.

        It frames the whole LIT set rather than the arrivals. Chronicles
        frames what arrives because its verses are one father and a row of
        new sons, and the father only earns his place while the type
        survives. Matthew has no such hierarchy: a verse is a recital, every
        name in it is equally the point, and the one that happens to be new
        is usually the least interesting.

        And it will DROP a name rather than rest below reading scale — a
        rule that currently costs nothing, because under the spine layout
        every verse fits. It was load-bearing under the centred one, where
        verse 2 could not hold Judah and verse 3 could not hold Zerah; see
        `_afford`. If it ever fires again, nothing is lost by it: a verse
        that drops a name draws the CARD, and the card lists every person
        the verse names in reading order.
        """
        lit = self.lit.get((ch, v)) or []
        self.dropped[(ch, v)] = []
        if not lit:
            return None, "quiet"
        keep = lit
        if v not in PANORAMA:
            keep, gone = _afford(lit)
            self.dropped[(ch, v)] = gone
        saved_lit = self.lit[(ch, v)]
        saved_arr = self.arrivals.get((ch, v))
        self.lit[(ch, v)], self.arrivals[(ch, v)] = keep, []
        try:
            box, mode = World.focus_box(self, ch, v)
        finally:
            self.lit[(ch, v)] = saved_lit
            self.arrivals[(ch, v)] = saved_arr
        if self.dropped[(ch, v)]:
            # A legible rest AND the card — the card is now carrying names
            # that are off the frame, which is the whole point of keeping it.
            mode = "card"
        return box, mode

    def context_nodes(self):
        """Everything the Old Testament already carried.

        `World`'s version is "every node no verse names", which here would
        wrongly hold back Abraham and David — Matthew names them, but they
        were standing long before he did. The nodes that have to arrive are
        exactly the ones this chapter adds.
        """
        return [n for n in self.nodes if n not in self.line.new]


class MatthewFrame(VerseFrame):
    """One verse of Matthew 1:1-17."""

    PANORAMA = PANORAMA
    panorama = False
    family_lines = False        # the older elbow, until Matthew's own files
                                # are reviewed under the family lines
    card_wives_beside = False   # and the older card, with a wife standing
                                # among the children
    cap_pays_outside = False    # and the older node cap, over the world's
                                # boxes only

    def render(self, ch, v, scene, first):
        """Verses 1 and 17 get the whole tree, and a thinner veil.

        Both of them span Abraham to Christ on purpose — one as the
        chapter's title, one as its summary — so the camera goes out to a
        twentieth of reading scale, and at that scale the ordinary settings
        are wrong twice over. The 260-node budget, which exists so a wide
        Chronicles shot cannot balloon a file, culls four fifths of the tree
        and leaves the rings floating over a few scattered specks; and the
        veil, sized for dimming legible boxes, takes the rest down to black.
        A verse that is *about* the reach of the line has to be able to show
        the thing it reaches across.
        """
        pan = self.panorama = v in self.PANORAMA
        _focus, mode = self.world.focus_box(ch, v)
        if pan:
            self.max_nodes, self.veil_alpha = 1600, 0.26
        elif mode == "card" and not self.world.dropped.get((ch, v)):
            # A wide rest: the default budget scatters a few boxes over the
            # gap being crossed and the full-strength veil takes the rest to
            # black, so the shot says nothing about what it is spanning.
            # A verse that merely DROPPED a name rests tight and is not this
            # case — it draws the card over an ordinary close shot.
            self.max_nodes, self.veil_alpha = 700, 0.44
        else:
            self.max_nodes = VerseFrame.max_nodes
            self.veil_alpha = VerseFrame.veil_alpha
        return VerseFrame.render(self, ch, v, scene, first)

    def card_pos(self, cw, ch_, pad):
        """On a panorama the card goes to the bottom LEFT.

        Bottom-centre is right for a Chronicles wide shot, where the family
        being named is a row and the card sits under it. Matthew's two
        panoramas run their highlights down the middle of the sheet from
        Abraham to Christ, and a centred card sat on the last ring of the
        three it was naming.
        """
        if self.panorama:
            return 34, VIEW_BOT - ch_ - pad * 2 - 10
        # And on an ordinary wide verse it sits a little higher than
        # Chronicles puts it. Matthew's wide verses are a descent seen from
        # far off, so the LAST name in them lands near the bottom of the
        # frame — Judah's ring was half under the card that was naming him.
        return (W - cw) / 2, VIEW_BOT - ch_ - pad * 2 - 50

    def _thread(self, dur):
        """The whole line, Abraham to Christ, as one gold thread.

        At the scale verses 1 and 17 pull back to, a box is four pixels and
        a name is nothing; four gold rings on a grey haze say "here, here,
        here and here" but not "these are one line", which is the only thing
        either verse says. The thread is drawn down every node of the path —
        including the five Matthew passes over, because the line goes
        through them whether or not he counts them — and it draws itself
        from Abraham downward while the verse is read.
        """
        pts = []
        for n in self.world.line.path():
            pts.append((n.x + n.w / 2, n.y + n.h / 2))
        sub = SvgCanvas(W, H)
        sub.traced(pts, dim(HL, 0.9), 5.0, dur="%.2fs" % (dur * 0.85))
        return "".join(sub._els)

    def _extra_world_els(self, ch, v, dur, shown):
        """The gold arc of Matthew's claim about Zerubbabel's father.

        Verse 12 says Shealtiel; 1 Chronicles 3:19 says Pedaiah, Shealtiel's
        brother. The tree keeps Chronicles' father — that is whose tree it
        is — so without this the verse lights an uncle and a nephew with
        nothing between them and the sentence has no picture. The arc is the
        sentence: it springs from the name Matthew gives and lands on the
        man, and it draws itself while the verse is read.
        """
        w = self.world
        lit = set(w.lit.get((ch, v), []))
        out = []
        if v in self.PANORAMA:
            out.append(self._thread(dur))
        for a, b, _text in w.tree.links:
            if a not in lit or b not in lit:
                continue
            ax, ay = a.x + a.w / 2, a.y + a.h / 2
            bx, by = b.x + b.w / 2, b.y + b.h / 2
            mx, my = (ax + bx) / 2, (ay + by) / 2
            lift = min(240, max(90, abs(bx - ax) * 0.22 + abs(by - ay) * 0.18))
            sub = SvgCanvas(W, H)
            sub.path("M %s %s Q %s %s %s %s"
                     % (_fmt(ax), _fmt(ay), _fmt(mx), _fmt(my - lift),
                        _fmt(bx), _fmt(by)),
                     fill=None, stroke=dim(HL, 0.75), width=2.0)
            for px, py in ((ax, ay), (bx, by)):
                sub.circle(px, py, 4.0, fill=dim(HL, 0.9), stroke=None)
            out.append(_fade_group(sub._els, "%.2fs" % (dur * 0.45)))
        return out

    def _hud(self, c, ch, v, scene):
        hud = SvgLayer()
        hud.rectangle([0, 0, W, HUD_H], fill=BG + (236,))
        hud.text((28, 20), f"{scene['title']} — Matthew {ch}",
                 font=F_TITLE, fill=TEXT)
        c.raw(hud.elements())
        c.line((0, HUD_H), (W, HUD_H), dim(SAND_DIM, 0.6), 1.0)
