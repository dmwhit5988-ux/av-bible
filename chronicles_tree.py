"""ONE contiguous family tree for 1 & 2 Chronicles.

`generate_1chronicles.py` holds the names, but it holds them as ~50 separate
scenes, because that is what a per-verse camera needs: each chapter re-roots
its lists and the scenes never join up. This module does the other job — it
welds those scenes into a SINGLE tree whose root is Adam and in which every
person Chronicles can be connected to is reachable from that root, so the
whole thing can be read as one chart.

Three kinds of edge, and the distinction is the point of the chart:

    solid   father -> son, as the text states it.
    dashed  a join the text implies but does not spell out — a name that
            re-roots a list with no father given, an ascending "the son of,
            the son of" line hung on the ancestor it terminates in, a
            family placed under its tribe because the passage is headed by
            that tribe. Every dashed edge carries a note saying why.
    wife    a wife, or the mother the line is reckoned through (Tamar,
            Judah's daughter-in-law, 2:4). A daughter keeps the solid
            line, even one the next generation is reckoned through.

Nothing is silently merged. Where two passages give the same person a
different father (there are several — Chronicles is not tidy), both lines
are kept and the node carries the disagreement in its note. Where one man
goes by two names, one box carries both ("Hotham · Helem"); and where a
passage only retells a line already drawn (9:11's priests are 6:12-13's),
its rows are bound to those boxes (Tree.bind) instead of being drawn twice,
with the difference in a note.

Material that is not genealogy at all (the Levites' city allotments, the
gatekeepers' duty roster, Simeon's town list, the Hagrite war) is left out;
persons named inside those passages are kept.

Names and spellings are the WEB's, from the scene data, unmodified.

Built into the wall chart by generate_ot_family_tree_svg.py, and read verse
by verse as the 1 Chronicles 1-9 camera (svg_chronicles_world.py).
Run `python chronicles_tree.py` for a structural audit.
"""

import re

from generate_1chronicles import CHAPTERS, _node
from passages import load_chapter


# ---------------------------------------------------------------------------
# Node
# ---------------------------------------------------------------------------

class N:
    """One person (or, occasionally, one house) in the master tree."""

    __slots__ = ("label", "note", "kids", "kind", "ref", "icon", "link",
                 "parent", "depth", "key",
                 "xref", "src",
                 # filled by the layout pass
                 "x", "y", "w", "h", "tw", "sw", "sh", "rows", "xw", "lx")

    def __init__(self, label, note=None, kids=None, kind="person",
                 ref=None, icon=None, link="solid"):
        self.label = label
        self.note = note
        self.kids = list(kids or [])
        self.kind = kind          # person | woman | king | priest | house
        self.ref = ref            # "1 Chr 2:9" — shown as a small chip
        self.icon = icon          # svg_figures subject name
        self.link = link          # solid | dash | wife
        self.parent = None
        self.depth = 0
        self.key = None
        self.xref = []            # [(other node, why)] — gold cross-refs
        self.src = None           # (chapter, scene title, flatten index)
        self.x = self.y = self.w = self.h = 0.0
        # Distance from this node's own centre to the LEFT edge of its
        # subtree. Always sw/2 under the centred layout, and not under the
        # spine one — see arrange_spine in generate_ot_family_tree_svg.
        self.lx = 0.0
        self.sw = self.sh = 0.0
        self.tw, self.rows, self.xw = [], [], []

    def add(self, node):
        self.kids.append(node)
        return node

    def __repr__(self):
        return f"<N {self.label!r} x{len(self.kids)}>"


def walk(node):
    yield node
    for k in node.kids:
        yield from walk(k)


# ---------------------------------------------------------------------------
# Reading the scene data
# ---------------------------------------------------------------------------

def _scene(ch, title):
    for s in CHAPTERS[ch]:
        if s["title"] == title:
            return s
    raise KeyError(f"1 Chr {ch}: no scene {title!r}")


def _from_raw(raw):
    """Scene node shorthand -> N (headings kept; caller decides)."""
    label, note, kids = _node(raw)
    return N(label, note, [_from_raw(k) for k in kids])


def _nest(nodes):
    """Chain payload -> a single-child descent."""
    out = None
    for raw in reversed(nodes):
        n = _from_raw(raw)
        if out is not None:
            n.kids.append(out)
        out = n
    return out


# -- provenance -------------------------------------------------------------
#
# Every node lifted out of the scene data remembers which scene row it came
# from, as (chapter, scene title, flatten index). That is what lets the
# per-verse chapter renderer reuse `assign()` — the verse-matching engine
# below works in flatten indices, and this is the bridge from those indices
# to nodes in the welded tree. The stamping order has to match `flatten()`
# exactly; it does, because `_from_raw` and `_nest` both build structures
# whose pre-order is flatten's order (a chain link's own children come
# before the next link in both).

def _raw_count(raw):
    _label, _note, kids = _node(raw)
    return 1 + sum(_raw_count(k) for k in kids)


def _block_base(ch, title, col, i):
    """The flatten index of a block's first row."""
    k = 0
    for ci, blocks in enumerate(_scene(ch, title)["cols"]):
        for bi, (kind, payload) in enumerate(blocks):
            if (ci, bi) == (col, i):
                return k
            k += (_raw_count(payload) if kind == "T"
                  else sum(_raw_count(r) for r in payload))
    raise KeyError(f"{title}: no block [{col}][{i}]")


def _stamp(nodes, ch, title, base):
    """Assign consecutive flatten indices over a pre-order walk."""
    k = base
    for top in nodes:
        for n in walk(top):
            n.src = (ch, title, k)
            k += 1
    return k


def blk(ch, title, col, i):
    """The (col, i)-th block of a scene, as an N."""
    kind, payload = _scene(ch, title)["cols"][col][i]
    node = _from_raw(payload) if kind == "T" else _nest(payload)
    _stamp([node], ch, title, _block_base(ch, title, col, i))
    return node


def chain(ch, title, col, i):
    """A chain block as a flat list of Ns (the caller re-hangs them)."""
    kind, payload = _scene(ch, title)["cols"][col][i]
    assert kind == "C", f"{title} [{col}][{i}] is not a chain"
    nodes = [_from_raw(raw) for raw in payload]
    _stamp(nodes, ch, title, _block_base(ch, title, col, i))
    return nodes


def upward(ch, title, col, i, drop=0):
    """An ascending 'the son of, the son of …' chain, turned right way up.

    1 Chr 6 and 9 give several lines from the living man backwards to the
    patriarch. Reversed they descend, and — this is the whole reason the
    chart can be contiguous — they land on somebody already in the tree.
    `drop` trims that many ancestors off the (now) top, so the line can be
    hung under the node it duplicates instead of duplicating it.
    """
    nodes = chain(ch, title, col, i)[::-1][drop:]
    out = None
    for n in reversed(nodes):
        if out is not None:
            n.kids.append(out)
        out = n
    return out


def strip(node, keep=()):
    """Drop '~heading' children, promoting their own children in place."""
    out = []
    for k in node.kids:
        strip(k, keep)
        if k.label.startswith("~") and k.label not in keep:
            out.extend(k.kids)
        else:
            out.append(k)
    node.kids = out
    return node


def named(node, label, nth=1):
    """The nth node labelled `label` inside `node` (pre-order)."""
    hits = [n for n in walk(node) if n.label == label]
    if len(hits) < nth:
        raise KeyError(f"{label!r} #{nth} not found under {node.label!r}")
    return hits[nth - 1]


# ---------------------------------------------------------------------------
# The master tree
# ---------------------------------------------------------------------------

class Tree:
    def __init__(self, root):
        self.root = root
        self.links = []       # cross-references drawn as gold dotted arcs
        # Scene rows the tree retells or drops, and the node each one means:
        # (chapter, scene title, flatten index) -> node, or None for "this
        # row lights nothing". A node keeps the one `src` stamp of the row it
        # was lifted from; 4:1 recites a descent chapter 2 already built, and
        # 6:33-38 climbs back up the Kohathite line of 6:22-28, so their rows
        # have no node of their own. The verse camera reads this after a miss
        # on the stamp (svg_chronicles_world.World._resolve_verse). Fill it
        # from node handles held at graft time, never from a bare find().
        self.bind = {}

    # -- lookup ------------------------------------------------------------

    def find(self, label, nth=1, under=None):
        base = under if under is not None else self.root
        return named(base, label, nth)

    # -- grafting ----------------------------------------------------------

    def children(self, label, src, nth=1, under=None, ref=None, link=None,
                 note=None):
        """Append `src`'s children to the existing node of the same name.

        This is the ordinary case: chapter 2 says "the sons of Hezron", and
        Hezron is already in the tree as a son of Perez.
        """
        tgt = self.find(label, nth, under)
        assert src.label == label, \
            f"graft mismatch: {src.label!r} onto {label!r}"
        if ref and not tgt.ref:
            tgt.ref = ref
        if note:
            tgt.note = f"{tgt.note} · {note}" if tgt.note else note
        if src.note and not tgt.note:
            tgt.note = src.note
        for k in src.kids:
            if link:
                k.link = link
            tgt.kids.append(k)
        return tgt

    def child(self, label, src, nth=1, under=None, link="solid", ref=None):
        """Hang `src` (a whole subtree) under an existing node."""
        tgt = self.find(label, nth, under)
        src.link = link
        if ref:
            src.ref = ref
        tgt.kids.append(src)
        return src

    def descent(self, label, nodes, nth=1, under=None, link="solid",
                ref=None):
        """Continue an existing node with a further descent (list of Ns)."""
        tgt = self.find(label, nth, under)
        head = nodes[0]
        head.link = link
        if ref:
            head.ref = ref
        cur = tgt
        for n in nodes:
            cur.kids.append(n)
            cur = n
        return nodes[-1]

    def link(self, a, b, text):
        """A cross-reference between two nodes already in the tree.

        It is recorded on BOTH nodes as well as on the tree, because the
        chart writes the reference inside each box — a label floating in the
        space between boxes has nowhere safe to sit on a sheet this dense,
        and lands on somebody's name. The tree-level list is only used to
        draw the arc when the two happen to be near each other.
        """
        self.links.append((a, b, text))
        a.xref.append((b, text))
        b.xref.append((a, text))

    # -- finishing ---------------------------------------------------------

    def seal(self):
        """Wire parents/depth and give every node a stable id."""
        seen = {}
        def rec(n, parent, depth):
            n.parent, n.depth = parent, depth
            base = re.sub(r"[^A-Za-z0-9]+", "_", n.label).strip("_") or "n"
            i = seen.get(base, 0) + 1
            seen[base] = i
            n.key = f"{base}_{i}"
            for k in n.kids:
                rec(k, n, depth + 1)
        rec(self.root, None, 0)
        return self


# ===========================================================================
# I.  Adam to the nations                                    (1 Chr 1:1-27)
# ===========================================================================

def build(ot=True):
    """The tree. With `ot`, the rest of the Old Testament is grafted on too
    (ot_grafts.py) — everything the canon gives a join for."""
    root = blk(1, "From Adam to Noah", 0, 0)          # Adam … Noah + 3 sons
    root.ref = "1 Chr 1:1-4"
    root.icon = "man"
    T = Tree(root)

    noah = T.find("Noah")
    noah.icon = "boat"
    noah.note = "the flood — Genesis 6-9"

    T.children("Japheth", blk(1, "The sons of Japheth", 0, 0),
               ref="1:5-7")
    T.children("Ham", blk(1, "The sons of Ham", 0, 0), ref="1:8-16")
    T.children("Shem", blk(1, "The sons of Shem", 0, 0), ref="1:17-23")

    # 1:24-27 repeats Shem-Arpachshad-Shelah-Eber-Peleg, then goes on. Hang
    # the new half on the Peleg the tree already has, and the two lists are
    # one line instead of two.
    s2a = chain(1, "From Shem to Abraham", 0, 0)[5:]          # Reu … Abram
    s2a[-1].label = "Abram · Abraham"
    s2a[-1].note = "1:27 — Abram, that is, Abraham"
    s2a[-1].icon = "tent"
    T.descent("Peleg", s2a, ref="1:24-27")

    ab = "Abram · Abraham"
    T.children(ab, _relabel(blk(1, "The sons of Abraham", 0, 0), ab),
               ref="1:28-34")
    T.child(ab, blk(1, "The sons of Abraham", 1, 0), link="wife")  # Keturah
    T.find("Keturah").kind = "woman"

    esau = T.children("Esau", blk(1, "The sons of Esau", 0, 0),
                      ref="1:35-37")
    # 1:36 lists Timna among Eliphaz's sons; Genesis 36:12 makes her his
    # concubine, Amalek's mother. She takes the wife line beside the sons,
    # and Amalek stays in their row.
    tim1 = T.find("Timna", under=T.find("Eliphaz", under=esau))
    tim1.kind, tim1.link = "woman", "wife"

    # -- Edom: the Horites, the kings, the chiefs --------------------------
    #
    # Seir the Horite is not Esau's descendant. The chart still joins him to
    # the trunk by the marriage Genesis states: Esau's wife Oholibamah was
    # the daughter of Anah, the son of Zibeon the son of Seir (Gen 36:2, 14,
    # 20, 24-25). Timna, Lotan's sister (1:39), is probably the same Timna
    # that Genesis 36:12 gives Eliphaz as a concubine. One dashed edge, and
    # Edom is in.
    seir = blk(1, "The sons of Seir", 0, 0)
    seir.note = ("the Horite house of Seir — joined to Esau by marriage, "
                 "not descent")
    seir.link = "dash"
    seir.ref = "1:38-42"
    T.child("Esau", seir, under=esau, link="dash")
    # 1:39 "Timna was Lotan's sister" — Seir's daughter, beside Lotan.
    tim2 = named(seir, "Timna")
    tim2.kind = "woman"
    T.link(tim2, tim1,
           "Lotan's sister, reckoned with Eliphaz — Amalek's mother")

    # 1:43-50 is a succession, not a descent: each king "reigned in his
    # place", and four are given other fathers (in their notes). The kings
    # stand side by side; Mehetabel stays under the second Hadad.
    kings = N("the kings of Edom", "before any king reigned over Israel — "
              "each reigned in the place of the one before, not as his son",
              kind="house", link="dash", ref="1:43-50")
    kings.kids = chain(1, "The kings of Edom", 0, 1)
    for k in kings.kids:
        k.link, k.kind = "dash", "king"
    T.child("Esau", kings, under=esau, link="dash")
    meh = T.find("Mehetabel", under=kings)       # 1:50 "his wife's name"
    meh.kind, meh.link = "woman", "wife"

    # The chiefs are fresh boxes (clans, not the namesakes of 1:36), but
    # each keeps its row's src stamp, so 1:51-54 resolve by stamp and not
    # by guessing among three Timnas and four Kenazes.
    chiefs = N("the chiefs of Edom", "eleven chiefs, after Hadad died — "
               "clans, not a descent", kind="house", link="dash",
               ref="1:51-54")
    for k in (blk(1, "The chiefs of Edom", 0, 1).kids +
              blk(1, "The chiefs of Edom", 1, 0).kids):
        n = N(k.label, k.note, link="dash")
        n.src = k.src
        chiefs.kids.append(n)
    T.child("Esau", chiefs, under=esau, link="dash")

    # ===================================================================
    # II.  Israel and his twelve sons                          (1 Chr 2:1-2)
    # ===================================================================
    T.children("Israel", blk(2, "The sons of Israel", 0, 0), ref="2:1-2")
    isr = T.find("Israel")
    isr.icon = "altar"
    isr.note = "Jacob — 2:1 names him only as Israel"

    _judah(T)
    _david(T)
    _judah_more(T)
    _simeon(T)
    _reuben_gad_manasseh(T)
    _levi(T)
    _northern(T)
    _benjamin(T)
    _return(T)
    _second_chronicles(T)

    if ot:
        import ot_grafts
        ot_grafts.extend(T)
    return T.seal()


def _relabel(node, label):
    node.label = label
    return node


# ===========================================================================
# III.  Judah                                          (1 Chr 2:3-55, 4:1-23)
# ===========================================================================

def _judah(T):
    ju = T.children("Judah", blk(2, "The sons of Judah", 0, 0), ref="2:3-8")
    ju.icon = "lion"
    # 2:4 — Perez and Zerah are reckoned through her, so she takes the wife
    # line; the note keeps it from reading as a marriage to Judah.
    tam = T.find("Tamar", under=ju)
    tam.kind, tam.link = "woman", "wife"
    tam.note = "his daughter-in-law, Er's widow — Genesis 38"

    # 2:7 gives Achar a father (Carmi) but gives Carmi none. Joshua 7:1 puts
    # him under Zerah's son Zabdi — the Zimri of 2:6.
    carmi = blk(2, "The sons of Judah", 1, 0)
    carmi.note = "2:7 names no father; Joshua 7:1 makes him son of Zabdi"
    carmi.link = "dash"
    T.child("Zimri", carmi, link="dash")
    T.find("Achar").icon = "stone"
    T.find("Achar").note = "the troubler of Israel — Joshua 7"

    T.children("Hezron", blk(2, "From Hezron to David", 0, 0), ref="2:9-17")
    T.find("Chelubai").label = "Chelubai · Caleb"
    T.find("Chelubai · Caleb").note = "2:9 Chelubai, 2:18 Caleb — one man"

    # David's sisters (2:16) are Jesse's daughters.
    for i in (1, 2):
        w = blk(2, "From Hezron to David", 1, i)
        w.kind, w.link, w.ref = "woman", "solid", "2:16-17"
        w.note = "David's sister" + (f" — {w.note}" if w.note else "")
        T.child("Jesse", w)

    dav = T.find("David")
    dav.icon = "harp"
    dav.kind = "king"

    # -- Caleb ------------------------------------------------------------
    cal = "Chelubai · Caleb"
    caleb = T.children(cal, _relabel(blk(2, "Caleb and Hezron's later line",
                                         0, 0), cal), ref="2:18-20")
    # 2:18-19 — "Azubah his wife, and ... Jerioth", then "Caleb married
    # Ephrath": three wives, not daughters.
    for w in ("Azubah", "Jerioth", "Ephrath"):
        n = T.find(w, under=caleb)
        n.kind, n.link = "woman", "wife"
    T.find("Jerioth", under=caleb).note = (
        "2:18 — the Hebrew can also make her Azubah's daughter, or another "
        "name for Azubah")
    T.descent("Hur", chain(2, "Caleb and Hezron's later line", 1, 0)[1:],
              ref="2:19-20")
    bez = T.find("Bezalel")
    bez.note = "who built the tent of meeting — Exodus 31:2"
    bez.icon = "ark"

    # 2:21-23 — Hezron, at sixty, married Machir's daughter; their son Segub
    # fathered Jair. Machir is Manasseh's son, so this edge ties Judah to
    # Joseph's half of the nation; the cross-link is drawn once Manasseh is
    # built (see _northern).
    mach_dau = N("the daughter of Machir", "Hezron married her when he was "
                 "sixty — Machir was the father of Gilead", kind="woman",
                 link="wife", ref="2:21-23")
    seg = chain(2, "Caleb and Hezron's later line", 1, 2)[1:]     # Segub, Jair
    mach_dau.kids = [seg[0]]
    seg[0].kids = [seg[1]]
    seg[1].note = "twenty-three cities in Gilead; Geshur and Aram took them"
    T.child("Hezron", mach_dau, link="wife")
    # She has no row of her own, so she takes the heading that introduces
    # her ('~Hezron, at sixty, married the daughter of'), and 2:21 lights
    # her through it. The scene's "Machir" row there is her father's name
    # in her description, not Manasseh's son arriving: bound to her, 2:21
    # and 2:23 frame Hezron's house instead of resting on a card that
    # reaches across to Manasseh.
    mach_dau.src = (2, "Caleb and Hezron's later line", 11)
    T.bind[(2, "Caleb and Hezron's later line", 12)] = mach_dau

    abij = blk(2, "Caleb and Hezron's later line", 2, 2)          # Abijah
    abij.kind, abij.link = "woman", "wife"
    abij.note = "Hezron's wife, who bore him after he died in Caleb Ephrathah"
    T.child("Hezron", abij, link="wife")

    jerah = T.children("Jerahmeel", blk(2, "The sons of Jerahmeel", 0, 0),
                       ref="2:25-33")
    for w in ("Atarah", "Abihail"):             # 2:26, 2:29 — wives
        n = T.find(w, under=jerah)
        n.kind, n.link = "woman", "wife"

    # 2:34-41 — Sheshan had no sons; the line runs through his daughter and
    # her Egyptian husband, then thirteen generations to Elishama.
    T.children("Sheshan", blk(2, "The line of Sheshan", 0, 0), ref="2:34-35")
    T.find("Jarha").kind = "person"
    T.descent("Attai", chain(2, "The line of Sheshan", 1, 0)[1:],
              ref="2:36-41")

    # 2:42-49 — "the sons of Caleb the brother of Jerahmeel": the same Caleb.
    T.children(cal, _relabel(blk(2, "The descendants of Caleb", 0, 0), cal),
               ref="2:42-49")
    # 2:42 "Mareshah the father of Hebron"; 2:43 then lists Hebron's sons.
    T.child("Mareshah", blk(2, "The descendants of Caleb", 0, 1), ref="2:43")
    T.descent("Shema", chain(2, "The descendants of Caleb", 0, 2)[1:])
    T.descent("Rekem", chain(2, "The descendants of Caleb", 1, 0)[1:])
    for i, w in ((1, "Ephah"), (2, "Maacah")):
        blk_ = blk(2, "The descendants of Caleb", 1, 1) if w == "Ephah" \
            else blk(2, "The descendants of Caleb", 2, 1)
        blk_.kind, blk_.link = "woman", "wife"
        if w == "Ephah":
            # 2:46 "bore Haran, Moza, and Gazez; and Haran became the father
            # of Gazez": two men, Ephah's son and Haran's son, who bears his
            # uncle's name. strip() would make the second Gazez his own
            # uncle's brother, so his heading's children go under Haran
            # first. Both keep their stamps, so 2:46 lights both.
            hd = next(k for k in blk_.kids
                      if k.label.startswith("~and Haran"))
            for k in hd.kids:
                k.note = "2:46 — Haran's son, who shares his uncle's name"
            named(blk_, "Haran").kids.extend(hd.kids)
            blk_.kids.remove(hd)
        strip(blk_)
        T.child(cal, blk_, link="wife")
    jah = blk(2, "The descendants of Caleb", 2, 0)               # Jahdai
    jah.note = "2:47 gives him no father; the list stands among Caleb's"
    jah.link = "dash"
    T.child(cal, jah, link="dash")
    ach = blk(2, "The descendants of Caleb", 2, 2)               # Achsah
    ach.kind = "woman"
    T.child(cal, ach)

    # 2:50-55 — "the sons of Caleb the son of Hur": the chapter re-roots on
    # the Hur of 2:19, so his three sons join there.
    hur = T.children("Hur", blk(2, "The sons of Hur", 0, 2), ref="2:50-55")
    # 2:53 — "the families of Kiriath Jearim" are clans of the town Shobal
    # fathered, not his sons, and "from them came" the Zorathites and the
    # Eshtaolites: out of all four families, so they hang from the
    # families' house and not from the Mishraites, the last one named.
    sh = strip(blk(2, "The sons of Hur", 1, 0),
               keep=("~the families of Kiriath Jearim:", "~from them came"))
    fam = named(sh, "~the families of Kiriath Jearim:")
    fam.label = "the families of Kiriath Jearim"
    fam.kind, fam.link = "house", "dash"
    fam.note = "2:53 — clans of Kiriath Jearim, whose father was Shobal"
    came = named(fam, "~from them came")
    came.label, came.kind, came.link = "from them came", "house", "dash"
    came.note = "2:53 — out of the four families"
    T.children("Shobal", sh, under=hur)
    T.children("Salma", blk(2, "The sons of Hur", 2, 0), under=hur)
    # 2:55 — "the Tirathites, the Shimeathites, and the Sucathites. These
    # are the Kenites who came from Hammath, the father of the house of
    # Rechab". The Kenites are those three families, not a fourth beside
    # them, so the Kenites row becomes the house (keeping its stamp) and its
    # heading row goes; the families came from Hammath, so they hang under
    # him and not beside him. Hammath has his own row, the scene's last, so
    # 2:55 lights him too. Jeremiah 35's Rechab joins him in
    # ot_grafts._after.
    scribes = blk(2, "The sons of Hur", 2, 1)        # the heading, dropped
    ken = scribes.kids[3]
    assert ken.label == "Kenites", ken.label
    ham = named(ken, "Hammath")
    ken.label = "the Kenites — scribes at Jabez"
    ken.kind, ken.link = "house", "dash"
    ken.note = "2:55 follows Salma's sons; Kenites by origin (Judges 1:16)"
    ham.link = "dash"
    ham.note = "the father of the house of Rechab — 2:55"
    ham.kids[0:0] = scribes.kids[:3]   # Tirathites, Shimeathites, Sucathites
    T.child("Salma", ken, under=hur, link="dash")
    # 2:53-55 — clans and a place, not men: "the families of Kiriath
    # Jearim", "the families of scribes", "half of the Manahathites", and
    # Atroth Beth Joab among "the sons of Salma". The links stay as the
    # text gives them; only the box says it is a group.
    for lbl in ("Ithrites", "Puthites", "Shumathites", "Mishraites",
                "Zorathites", "Eshtaolites", "Netophathites", "Manahathites",
                "Zorites", "Tirathites", "Shimeathites", "Sucathites",
                "Atroth Beth Joab"):
        T.find(lbl, under=hur).kind = "house"


# ===========================================================================
# IV.  The house of David                                     (1 Chr 3:1-24)
# ===========================================================================

def _david(T):
    dv = blk(3, "The sons of David", 0, 0)
    born_heb = dv.kids[0]
    born_heb.label = "born to him in Hebron"
    born_heb.kind, born_heb.note = "house", "seven years and six months"
    born_jer = blk(3, "The sons of David", 1, 0)
    born_jer.label = "born to him in Jerusalem"
    born_jer.kind, born_jer.note = "house", "thirty-three years"
    tamar = blk(3, "The sons of David", 2, 2)
    tamar.kind, tamar.note = "woman", "their sister"

    T.children("David", N("David", kids=[born_heb, born_jer, tamar]),
               ref="3:1-9")
    T.find("Solomon").note = "of Bathshua — 3:5"

    # 3:10-16: son succeeding father, Solomon to the exile.
    kings = chain(3, "The kings of Judah", 0, 0)[1:]        # Rehoboam … Josiah
    for k in kings:
        k.kind = "king"
    T.descent("Solomon", kings, ref="3:10-14")
    T.find("Solomon").kind = "king"
    T.find("Solomon").icon = "house"
    T.find("Azariah", 1, under=T.find("Rehoboam")).label = "Azariah · Uzziah"

    T.children("Jeconiah", blk(3, "The line after the exile", 0, 0),
               ref="3:17-20")
    T.find("Shelomith").kind = "woman"
    T.find("Zerubbabel").icon = "house"
    T.find("Zerubbabel").note = ("who laid the second temple's foundation — "
                                 "Ezra 3:8")
    han = T.children("Hananiah", blk(3, "The line after the exile", 1, 0),
                     ref="3:21")
    # 3:21 "the sons of Rephaiah, the sons of Arnan, the sons of Obadiah, the
    # sons of Shecaniah": four families beside Hananiah's sons, with no
    # father named and no "his son" between them (the WEB, with the Hebrew;
    # the Greek reads a chain from Jeshaiah). Each hangs dashed on Hananiah.
    for n in chain(3, "The line after the exile", 1, 2):
        n.note = ("3:21 sets these four beside Hananiah's sons without "
                  "naming their father")
        T.child("Hananiah", n, under=han, link="dash", ref="3:21")
    # 3:22 — the chain row for Shemaiah already carries his five sons, so
    # this one graft brings them; they are not grafted a second time.
    shem = T.descent("Shecaniah",
                     chain(3, "The last generations recorded", 0, 0)[1:],
                     ref="3:22")
    assert shem.label == "Shemaiah", shem
    T.children("Neariah", blk(3, "The last generations recorded", 1, 0),
               under=shem, ref="3:23")
    T.children("Elioenai", blk(3, "The last generations recorded", 2, 0),
               ref="3:24")
    T.find("Anani").note = "the last name in the book's royal line"


# ===========================================================================
# V.  Judah's other families                                  (1 Chr 4:1-23)
# ===========================================================================

def _judah_more(T):
    # 4:1 is a descent, not a brotherhood — Perez, Hezron, Carmi, Hur and
    # Shobal are all already in the tree, so only Shobal's sons (4:2) are
    # added, and the verse's own rows are bound to the men chapter 2 built.
    # "Carmi" stands where Chelubai · Caleb does, between Hezron and Hur
    # (2:9, 2:18-19); the only Judahite Carmi, Zimri's (2:7), is off the line.
    judah = T.find("Judah")
    perez = T.find("Perez", under=judah)
    hezron = T.find("Hezron", under=perez)
    caleb = T.find("Chelubai · Caleb", under=hezron)
    hur = T.find("Hur", under=caleb)
    shobal = T.children("Shobal", strip(_only(blk(4, "Families of Judah",
                                                  0, 0), "Shobal")),
                        under=hur, ref="4:1-2")
    for k, n in enumerate((judah, perez, hezron, caleb, hur, shobal)):
        T.bind[(4, "Families of Judah", k)] = n
    # 2:52 Haroeh and 4:2 Reaiah: both "son of Shobal", and commonly read as
    # one man under two spellings. One box carries both names and Reaiah's
    # line; 4:2's Reaiah row finds it by the second half of the label (Jahath,
    # stamped, is its son, which settles it over the Reubenite Reaiah).
    hro = T.find("Haroeh", under=shobal)
    rea = T.find("Reaiah", under=shobal)
    hro.kids.extend(rea.kids)
    shobal.kids.remove(rea)
    hro.label = "Haroeh · Reaiah"
    hro.note = ((hro.note + " · ") if hro.note else "") + \
        "2:52 Haroeh, 4:2 Reaiah — commonly read as one man"

    # 4:3 "the sons of the father of Etam": their father is not named, and
    # Etam is a town (2 Chr 11:6), so the box is "the father of Etam". This
    # is the WEB's reading, with the Hebrew; the Greek, and NIV, ESV and
    # NRSV after it, read "the sons of Etam".
    etam = blk(4, "Families of Judah", 1, 0)
    etam.label = "the father of Etam"
    etam.note = "4:3 — among the sons of Hur (4:4)"
    etam.link = "dash"
    T.child("Hur", etam, link="dash", ref="4:3-4")
    T.find("Hazzelelponi").kind = "woman"
    for i in (2, 3):                                   # Penuel, Ezer
        n = blk(4, "Families of Judah", 1, i)
        n.note = "of the sons of Hur, the firstborn of Ephrathah — 4:4"
        T.child("Hur", n)

    ash = T.children("Ashhur", blk(4, "Families of Judah", 2, 0), ref="4:5-7")
    for w in ("Helah", "Naarah"):      # 4:5 "two wives, Helah and Naarah"
        n = T.find(w, under=ash)
        n.kind, n.link = "woman", "wife"
    hak = blk(4, "Families of Judah", 2, 1)
    hak.note = "4:8 gives no father"
    # 4:8 "the families of Aharhel the son of Harum": Aharhel's father is
    # Harum, and Hakkoz is the forebear of the families.
    har = named(hak, "Harum")
    har.link = "dash"
    har.note = ("4:8 — Hakkoz fathered 'the families of Aharhel the son of "
                "Harum'; how Harum joins Hakkoz is not said")
    T.child("Judah", hak, link="dash", ref="4:8")

    jab = blk(4, "The prayer of Jabez", 0, 0)
    jab.note = ("more honorable than his brothers — “Oh that you would bless "
                "me indeed, and enlarge my border!” · and God granted it")
    T.child("Judah", jab, link="dash", ref="4:9-10")

    chelub = blk(4, "Kenaz and Caleb's families", 0, 0)
    chelub.note = "4:11 — brother of Shuhah; no father given"
    T.child("Judah", chelub, link="dash", ref="4:11-12")

    # 4:13-15 — Kenaz, Othniel and Caleb son of Jephunneh. A DIFFERENT Caleb
    # from Hezron's son, and the chart says so rather than merging them.
    # 4:15 names his father; the father's own descent is not given.
    jeph = blk(4, "Kenaz and Caleb's families", 2, 0)
    jeph.note = ("4:15 — Caleb's father; the Kenizzite (Numbers 32:12); "
                 "Chronicles gives no further ancestry")
    calj = named(jeph, "Caleb")
    calj.note = ("the son of Jephunneh — the spy (Numbers 13:6), not the "
                 "Caleb son of Hezron")
    T.child("Judah", jeph, link="dash", ref="4:15")
    kenaz = blk(4, "Kenaz and Caleb's families", 1, 0)
    T.child("Judah", kenaz, link="dash", ref="4:13-14")
    oth = T.children("Othniel", blk(4, "Kenaz and Caleb's families", 1, 1))
    T.children("Seraiah", blk(4, "Kenaz and Caleb's families", 1, 2))
    oth.note = "Israel's first judge — Judges 3:9"
    oth.icon = "sword"
    # 4:13-14 "The sons of Othniel: Hathath. Meonothai became the father of
    # Ophrah": the WEB names no father for Meonothai. He stays under
    # Othniel, whose line 4:14 sets beside Seraiah's, on a dashed join.
    meo = T.find("Meonothai", under=oth)
    meo.link = "dash"
    meo.note = ("4:14 gives no father; some Greek copies and the Latin read "
                "“the sons of Othniel: Hathath and Meonothai”")
    T.link(T.find("Kenaz", 2), T.find("Kenaz", 3),
           "Caleb the Kenizzite and Othniel son of Kenaz — Joshua 15:17")

    for col, i, ref in ((0, 0, "4:16"), (0, 1, "4:17-18"),
                        (2, 1, "4:20"), (2, 2, "4:20")):
        n = blk(4, "More families of Judah", col, i)
        n.note = (n.note + " · " if n.note else "") + f"{ref} gives no father"
        T.child("Judah", n, link="dash", ref=ref)
    mer = T.children("Mered", blk(4, "More families of Judah", 1, 0),
                     ref="4:17-18")
    mer.note = "4:18 — he took Bithiah, Pharaoh's daughter"
    bith = T.find("Bithiah", under=mer)          # 4:18 "whom Mered took"
    bith.kind, bith.link = "woman", "wife"
    bith.note = "Pharaoh's daughter, whom Mered took"
    # 4:18 "His wife the Jewess bore Jered ..., Heber ... and Jekuthiel": a
    # wife, with her three sons under her. Her row says "the Jewess" so the
    # verse's text lights it; the box takes the verse's fuller wording.
    jew = T.find("the Jewess", under=mer)
    jew.label = "his wife the Jewess"
    jew.kind, jew.link, jew.note = "woman", "wife", "4:18"
    # 4:19 "the sons of the wife of Hodiah, the sister of Naham": in the WEB
    # Hodiah is the husband (the KJV reads it as her name), so he takes the
    # dashed join under Judah and she the wife line under him.
    hod = blk(4, "More families of Judah", 2, 0)
    assert hod.label == "Hodiah", hod
    hod.note = "4:19 gives no father"
    nah = named(hod, "the sister of Naham")
    nah.kind, nah.link, nah.note = "woman", "wife", "Hodiah's wife — 4:19"
    # 4:19 her sons "were the father of Keilah the Garmite, and Eshtemoa":
    # the son is unnamed, and Keilah is a town (Joshua 15:44).
    kei = named(nah, "Keilah")
    kei.label = "the father of Keilah"
    kei.note = "the Garmite"
    T.child("Judah", hod, link="dash", ref="4:19")

    she = T.children("Shelah", strip(blk(4, "The sons of Shelah", 0, 0)),
                     under=T.find("Judah"), ref="4:21-23")
    she.note = ("the potters, who lived at Netaim and Gederah with the "
                "king for his work")


def _only(node, label):
    """A block re-rooted on one of its children (4:1 lists a descent)."""
    return named(node, label)


# ===========================================================================
# VI.  Simeon                                                (1 Chr 4:24-43)
# ===========================================================================

def _simeon(T):
    T.children("Simeon", blk(4, "The sons of Simeon", 0, 0), ref="4:24-27")
    T.find("Shimei", 1, under=T.find("Simeon")).note = \
        "sixteen sons and six daughters — but the tribe did not multiply " \
        "like Judah"

    princes = blk(4, "The princes of Simeon", 0, 0)
    princes.label = "princes in their families"
    princes.kind, princes.link = "house", "dash"
    princes.note = "4:34-38 — heads of Simeon's houses, fathers not traced"
    T.child("Simeon", princes, link="dash", ref="4:34-38")
    # 4:37 climbs: "Ziza the son of Shiphi … the son of Shemaiah". Turned
    # right way up, Shemaiah heads the line and Ziza, the prince, is its foot.
    top = upward(4, "The princes of Simeon", 1, 1)
    top.note = "4:37 — Ziza's line read upward; Shemaiah's own father is " \
               "not given"
    top.link = "dash"
    princes.kids.append(top)

    ishi = blk(4, "The princes of Simeon", 2, 2)
    ishi.note = "his sons led five hundred to Mount Seir, and struck the " \
                "remnant of the Amalekites there — 4:42-43"
    ishi.link = "dash"
    T.child("Simeon", ishi, link="dash", ref="4:42-43")


# ===========================================================================
# VII.  Reuben, Gad and half-Manasseh beyond Jordan            (1 Chr 5:1-26)
# ===========================================================================

def _reuben_gad_manasseh(T):
    reu = T.children("Reuben", blk(5, "Reuben, the firstborn", 0, 3),
                     ref="5:1-3")
    reu.note = ("the firstborn, but he defiled his father's couch, and the "
                "birthright went to the sons of Joseph; the prince came "
                "from Judah")

    # 5:4-6, stamped: Joel > Shemaiah > … > Baal > Beerah, "his son" each.
    jc = chain(5, "Reuben, the firstborn", 1, 0)
    for a, b in zip(jc, jc[1:]):
        a.kids.append(b)
    joel, beerah = jc[0], jc[-1]
    joel.note = "5:4-6 — Joel's descent; his own father is not given"
    T.child("Reuben", joel, under=reu, link="dash", ref="5:4-6")
    beerah.note = ("prince of the Reubenites, whom Tilgath Pilneser "
                   "carried away")
    beerah.icon = "shackle"

    # 5:7 "His brothers" are Beerah's: Reubenite kinsmen whose father the
    # text doesn't give, so the house stays dashed under the tribe.
    bros = blk(5, "Reuben, the firstborn", 2, 0)
    bros.label = "Beerah's brothers by their families"
    bros.kind, bros.link, bros.note = "house", "dash", \
        "5:7-9 — kinsmen of Beerah; from Aroer to Nebo and Baal Meon"
    T.child("Reuben", bros, under=reu, link="dash", ref="5:7-9")

    # 5:11-17 is one register of Gadites in Bashan, listed in Jotham's and
    # Jeroboam's days — not Gad's own sons (those are Genesis 46:16, grafted
    # in ot_grafts). The chiefs of 5:12 and Ahi of 5:15 stand in one house;
    # the scene's "in Bashan to Salecah" note stays off Gad himself.
    gad = T.find("Gad", under=T.find("Israel"))
    sons = blk(5, "The sons of Gad", 0, 0)            # Gad + the four, stamped
    ahi = blk(5, "The sons of Gad", 2, 2)
    ahi.ref = "5:15"
    bashan = N("the Gadites in Bashan",
               "5:11-17 — in Bashan to Salecah; listed in the days of "
               "Jotham king of Judah and Jeroboam king of Israel",
               kids=sons.kids + [ahi], kind="house")
    T.child("Gad", bashan, under=gad, link="dash", ref="5:11-17")
    # 5:14 climbs from Abihail to Buz; turned right way up, Buz heads it.
    buz = upward(5, "The sons of Gad", 2, 1)
    buz.note = "5:14 read upward: Abihail's line climbs to Buz, whose own " \
               "descent from Gad is not given"
    T.child("Gad", buz, under=gad, link="dash", ref="5:14")
    # "These were the sons of Abihail" (5:14) — the seven of 5:13.
    abi = named(buz, "Abihail")
    abi.note = "5:13-14 — father of the seven, 'their brothers, of their " \
               "fathers' houses'"
    abi.kids.extend(blk(5, "The sons of Gad", 1, 0).kids)

    # half-Manasseh: the tribe is Joseph's, so it hangs on Manasseh, built
    # in _northern — deferred there.


# ===========================================================================
# VIII.  Levi                                                 (1 Chr 6:1-53)
# ===========================================================================

def _levi(T):
    lv = T.children("Levi", blk(6, "The line of the high priests", 0, 0),
                    ref="6:1")
    lv.icon = "lampstand"
    T.children("Kohath", blk(6, "The line of the high priests", 0, 1),
               ref="6:2")
    T.children("Amram", blk(6, "The line of the high priests", 0, 2),
               ref="6:3")
    T.find("Miriam").kind = "woman"
    T.find("Moses").icon = "scroll"
    koh = T.find("Kohath", under=lv)
    izhar = next(k for k in koh.kids if k.label == "Izhar")       # 6:2
    T.children("Aaron", blk(6, "The line of the high priests", 1, 0),
               ref="6:3-15")
    T.find("Aaron").kind = "priest"
    T.find("Aaron").icon = "priest"
    T.find("Jehozadak").note = ("went into captivity when Yahweh carried "
                                "Judah and Jerusalem away by Nebuchadnezzar")
    T.find("Jehozadak").icon = "shackle"
    T.find("Azariah", 1, under=T.find("Eleazar")).note = \
        "he executed the priest's office in the temple Solomon built — 6:10"

    # 6:16-19 re-lists the three houses; Gershon of 6:1 is Gershom here.
    T.find("Gershon").label = "Gershon · Gershom"
    T.children("Gershon · Gershom",
               _relabel(blk(6, "The families of Levi", 1, 0),
                        "Gershon · Gershom"), ref="6:17")
    T.children("Merari", blk(6, "The families of Levi", 2, 0), ref="6:19")

    # 6:20-30 — the three houses carried down.
    T.descent("Libni", chain(6, "The Levite lines", 0, 1)[2:], ref="6:20-21")
    # Korah's line, 6:22-28. The names repeat so freely here that the grafts
    # hold the nodes themselves rather than looking them up again.
    kch = chain(6, "The Levite lines", 1, 1)[1:]     # Amminadab … Shaul
    kch[0].note = "6:22 — 'Amminadab his son'; 6:18 has Izhar in this place"
    kch[0].link = "dash"
    T.descent("Kohath", kch, ref="6:22-24", link="dash")
    korah, elk1 = kch[1], kch[3]
    korah.note = "whose sons did not die — Numbers 26:11"
    for k in blk(6, "The Levite lines", 1, 2).kids:  # Amasai, Ahimoth
        elk1.kids.append(k)
    zoph = chain(6, "The Levite lines", 2, 0)[1:]    # Zophai … Elkanah
    zoph[0].note = "6:26 begins again from Elkanah without saying which"
    zoph[0].link = "dash"
    cur = elk1
    for n in zoph:
        cur.kids.append(n)
        cur = n
    sam = blk(6, "The Levite lines", 2, 1)           # Samuel + Joel, Abijah
    sam.note = "the seer, who with David ordained the gatekeepers in " \
               "their office of trust — 9:22"
    sam.icon = "scroll"
    sam.ref = "6:28"
    cur.kids.append(sam)
    T.descent("Mahli", chain(6, "The Levite lines", 2, 3)[2:], nth=1,
              under=T.find("Merari"), ref="6:29-30")

    # -- the three singers -------------------------------------------------
    #
    # 6:33-47 gives each singer's line UPWARD to Levi. Turned right way up
    # they land on men already here, which is what makes the Levite half of
    # the chart one tree: Heman continues Samuel's line, Asaph descends from
    # Gershom, Ethan from Merari's son Mushi.
    heman = blk(6, "The temple singers", 0, 2)
    heman.note = "the singer, in the midst — his line read upward to Israel"
    heman.icon = "harp"
    heman.ref = "6:33-38"
    T.child("Joel", heman, nth=1, under=T.find("Samuel"))

    # 6:33-38 climbs Heman's line back up to Israel through men 6:22-28
    # already built, so its rows are bound to them rather than lifted (a
    # lift would draw Samuel and Joel twice). The run Elkanah, Jeroham,
    # Eliel, Toah, Zuph matches 6:26-27 and 1 Samuel 1:1 (Elihu, Tohu,
    # Zuph): Eliel is Eliab, Toah Nahath, Zuph Zophai. Rows 10-16 (Elkanah,
    # Mahath, Amasai, Elkanah, Joel, Azariah, Zephaniah) have no right box
    # yet — the tree hangs Amasai under Assir's son Elkanah, above Tahath,
    # where 6:35-36 puts him below — so they light nothing rather than a
    # namesake.
    joel = next(k for k in sam.kids if k.label == "Joel")
    isr = T.find("Israel")
    assert lv in isr.kids
    assert [n.label for n in zoph] == ["Zophai", "Nahath", "Eliab",
                                       "Jeroham", "Elkanah"]
    assert [n.label for n in kch[1:7]] == ["Korah", "Assir", "Elkanah",
                                           "Ebiasaph", "Assir", "Tahath"]
    heman_line = {3: joel, 4: sam, 5: zoph[4], 6: zoph[3], 7: zoph[2],
                  8: zoph[1], 9: zoph[0],
                  17: kch[6], 18: kch[5], 19: kch[4], 20: kch[1],
                  21: izhar, 22: koh, 23: lv, 24: isr}
    for k in range(10, 17):
        heman_line[k] = None
    for k, n in heman_line.items():
        T.bind[(6, "The temple singers", k)] = n

    asaph = upward(6, "The temple singers", 1, 1, drop=2)   # after Levi,Gershom
    asaph.link = "dash"
    asaph.note = "6:39-43 read upward; 6:20 puts Libni, not Jahath, first " \
                 "under Gershom"
    T.child("Gershon · Gershom", asaph, link="dash", ref="6:39-43")
    asaph_leaf = named(asaph, "Berechiah")
    ap = blk(6, "The temple singers", 1, 0)
    ap.note = "his brother, who stood at his right hand"
    ap.icon = "harp"
    asaph_leaf.kids.append(ap)

    ethan = upward(6, "The temple singers", 2, 1, drop=3)  # after Levi,Merari,Mushi
    ethan.link = "dash"
    ethan.note = "6:44-47 read upward"
    T.child("Mushi", ethan, link="dash", ref="6:44-47")
    # The third singer is Ethan in 6:44 and 15:17-19 and Jeduthun in 16:41-42
    # and 25:1-6: one box with both names. 9:16's Jeduthun line hangs from it
    # (_return).
    et = blk(6, "The temple singers", 2, 0)
    et.label = "Ethan · Jeduthun"
    et.note = ("of the sons of Merari, on the left hand · Jeduthun in "
               "16:41 and 25:1, where 6:44 and 15:17 have Ethan")
    et.icon = "harp"
    named(ethan, "Kishi").kids.append(et)

    T.find("Levi").note = ("6:31-32 — David set these three over the song "
                           "in Yahweh's house after the ark came to rest")


# ===========================================================================
# IX.  Issachar, Naphtali, Manasseh, Ephraim, Asher            (1 Chr 7:1-40)
# ===========================================================================

def _northern(T):
    T.children("Issachar", blk(7, "The sons of Issachar", 0, 0), ref="7:1")
    T.children("Tola", blk(7, "The sons of Issachar", 1, 0), ref="7:2")
    T.children("Uzzi", blk(7, "The sons of Issachar", 2, 0), nth=1,
               under=T.find("Tola"), ref="7:3")
    T.children("Izrahiah", blk(7, "The sons of Issachar", 2, 1), ref="7:3")
    T.find("Issachar").note = "87,000 mighty men of valor in all — 7:5"

    T.children("Naphtali", blk(7, "The sons of Naphtali", 0, 0), ref="7:13")

    # -- Joseph: Manasseh and Ephraim --------------------------------------
    jos = T.find("Joseph")
    jos.note = "the birthright was his — 5:1-2"
    jos.kids = [N("Manasseh", link="solid", ref="7:14"),
                N("Ephraim", link="solid", ref="7:20")]
    # 7:14 gives Machir his son Gilead ("Machir the father of Gilead"), so
    # Gilead comes in from the scene, solid; Numbers 26 hangs its clan list
    # on this box (ot_grafts._numbers).
    man = T.children("Manasseh", blk(7, "The sons of Manasseh", 0, 0),
                     under=jos, ref="7:14")
    T.find("Asriel").note = "whom his Aramitess concubine bore"
    # 7:14 — the concubine who bore both sons. She stands beside them, as
    # Israel's and David's wives do, and has no children of her own on the
    # chart: Asriel and Machir stay under Manasseh, so Machir's house keeps
    # its generation. Her box is the scene's row, so 7:14 lights her.
    aram = man.kids[0]
    assert aram.label == "the Aramitess", aram
    aram.kind, aram.link, aram.ref = "woman", "wife", "7:14"
    aram.note = "his concubine — she bore Asriel and Machir — 7:14"
    mach = T.children("Machir", blk(7, "The sons of Manasseh", 0, 1),
                      ref="7:15-16")
    maa = T.find("Maacah", 1, under=mach)     # 7:16 "the wife of Machir"
    maa.kind, maa.link = "woman", "wife"
    T.children("Maacah", blk(7, "The sons of Manasseh", 1, 0), nth=1,
               under=T.find("Machir"))
    T.descent("Ulam", chain(7, "The sons of Manasseh", 1, 1)[1:], ref="7:17")
    for i in (0, 1):
        n = blk(7, "The sons of Manasseh", 2, i)
        n.link = "dash"
        n.note = (n.note + " · " if n.note else "") + \
            "7:18-19, among Gilead's house"
        T.child("Machir", n, link="dash", ref="7:18-19")
    T.find("Hammolecheth").kind = "woman"

    # The Judah/Joseph knot: Hezron's wife was Machir's daughter (2:21).
    T.link(T.find("the daughter of Machir"), T.find("Machir"),
           "Hezron of Judah married into Manasseh — 2:21")

    T.descent("Ephraim", chain(7, "The sons of Ephraim", 0, 1)[1:],
              ref="7:20-21")
    T.find("Ephraim").note = ("his sons Ezer and Elead were killed by the "
                              "men of Gath, and he mourned many days")
    # 7:21-22 — Ezer and Elead are Ephraim's own sons ("Ephraim their father
    # mourned"), so they stand after Shuthelah and before Beriah, who was
    # born after their deaths (7:23).
    for k in blk(7, "The sons of Ephraim", 0, 2).kids:
        k.note = "killed by the men of Gath when they came for the livestock"
        T.child("Ephraim", k, under=jos, ref="7:21")
    ber = blk(7, "The sons of Ephraim", 1, 0)
    ber.note = "“there was trouble with his house” — born to Ephraim after"
    T.child("Ephraim", ber, ref="7:23")
    # 7:24 "His daughter was Sheerah": "his" may be Beriah, just named, or
    # Ephraim, the subject of 7:22-23. She stays under Beriah, dashed.
    sheer = blk(7, "The sons of Ephraim", 1, 1)
    sheer.kind = "woman"
    sheer.note = ("his daughter (7:24 'his' — Beriah's or Ephraim's), who "
                  "built Lower and Upper Beth Horon")
    T.child("Beriah", sheer, under=ber, link="dash", ref="7:24")
    # 7:25 "Rephah was his son, and Resheph, and Telah his son": Resheph
    # alone has no "his son", so he is read as Rephah's brother (Keil &
    # Delitzsch), and the line runs on through Rephah to Telah and Joshua.
    line = chain(7, "The sons of Ephraim", 1, 3)     # Rephah, Resheph, Telah…
    reph, resh = line[0], line[1]
    assert (reph.label, resh.label) == ("Rephah", "Resheph"), line[:2]
    T.descent("Beriah", [reph] + line[2:], under=ber, ref="7:25-27",
              link="dash")
    reph.note = "7:25 continues the house without naming the join"
    resh.link, resh.ref = "dash", "7:25"
    resh.note = ('7:25 "Rephah was his son, and Resheph" — no "his son", '
                 "read as Rephah's brother")
    ber.kids.insert(ber.kids.index(reph) + 1, resh)
    josh = T.find("Joshua")
    josh.note = "who brought Israel into the land"
    josh.icon = "sword"

    # half-Manasseh beyond Jordan (5:23-26) hangs on Manasseh.
    half = blk(5, "The half-tribe of Manasseh", 0, 2)
    half.label = "heads of their fathers' houses in Bashan"
    half.kind, half.link = "house", "dash"
    half.note = ("mighty men of valor, from Bashan to Baal Hermon, Senir "
                 "and Mount Hermon — carried away by Tilgath Pilneser "
                 "with Reuben and Gad")
    T.child("Manasseh", half, under=jos, link="dash", ref="5:23-26")

    ash = T.children("Asher", blk(7, "The sons of Asher", 0, 0),
                     ref="7:30-32")
    for w in ("Shua", "Serah"):
        T.find(w).kind = "woman"
    T.find("Shomer").label = "Shomer · Shemer"
    T.children("Shomer · Shemer",
               _relabel(blk(7, "The sons of Asher", 1, 0), "Shomer · Shemer"),
               ref="7:34")
    # 7:32 lists Heber's sons as Japhlet, Shomer and Hotham; 7:33-35 takes
    # them in the same order as Japhlet, Shemer and "Helem his brother". As
    # with Shomer · Shemer, one man. The explicit note keeps T.children from
    # copying the scene row's bare "his brother" onto the merged box.
    heber = T.find("Heber", under=ash)
    T.find("Hotham", under=heber).label = "Hotham · Helem"
    T.children("Hotham · Helem",
               _relabel(blk(7, "The sons of Asher", 1, 1), "Hotham · Helem"),
               under=heber, note="7:32 Hotham, 7:35 Helem", ref="7:35-36")
    for i in (0, 1):
        n = blk(7, "The sons of Asher", 2, i)
        n.link = "dash"
        n.note = "7:38-39 gives no father"
        T.child("Asher", n, link="dash", ref="7:38-39")
    T.find("Asher").note = "26,000 men fit for war, chief of the princes"


# ===========================================================================
# X.  Benjamin and the house of Saul                           (1 Chr 7, 8)
# ===========================================================================

def _benjamin(T):
    # Two lists, seven chapters apart, and they do not agree. Both hang on
    # Benjamin, each labelled with the passage it comes from.
    b7 = blk(7, "The sons of Benjamin", 0, 0)
    b7.label = "the sons of Benjamin (7:6)"
    b7.kind, b7.note = "house", "Bela, Becher and Jediael — three"
    T.children("Benjamin", N("Benjamin", kids=[b7]), ref="7:6-12")
    also = blk(7, "The sons of Benjamin", 1, 0)
    also.label = "and also"
    also.kind, also.link, also.note = "house", "dash", \
        "7:12 — Shuppim and Huppim, the sons of Ir; Hushim, and the sons " \
        "of Aher"
    b7.kids.append(also)

    b8 = blk(8, "Benjamin: the sons of Bela", 0, 0)
    b8.label = "the sons of Benjamin (8:1)"
    b8.kind, b8.note = "house", \
        "Bela, Ashbel, Aharah, Nohah and Rapha — five, and a different list"
    T.child("Benjamin", b8, ref="8:1-2")
    T.children("Bela", blk(8, "Benjamin: the sons of Bela", 1, 0),
               under=b8, ref="8:3-5")
    ehud = blk(8, "Benjamin: the sons of Bela", 2, 2)
    ehud.link, ehud.note = "dash", \
        "8:6-7 — heads of the households of Geba, carried captive to Manahath"
    T.child("Benjamin", ehud, link="dash", ref="8:6-7")

    shah = blk(8, "Shaharaim in Moab", 0, 0)
    shah.link = "dash"
    shah.note = "in the field of Moab, after he had sent away Hushim and " \
                "Baara his wives — 8:8"
    # His three wives are rows of their own, so 8:8, 8:9 and 8:11 light
    # them; they stand in the order 8:8-9 names them.
    baara, hod = shah.kids
    assert (baara.label, hod.label) == ("Baara", "Hodesh"), shah.kids
    baara.kind, baara.link = "woman", "wife"
    baara.note = ("his wife, whom he sent away — 8:8; some identify her "
                  "with Hodesh (8:9)")
    hod.kind, hod.link = "woman", "wife"
    hod.note = "his wife, who bore him in the country of Moab"
    hush = blk(8, "Shaharaim in Moab", 1, 0)
    assert hush.label == "Hushim", hush
    hush.kind, hush.link = "woman", "wife"
    hush.note = "8:11 — of her he became the father of Abitub and Elpaal"
    shah.kids.insert(0, hush)
    T.child("Benjamin", shah, link="dash", ref="8:8-13")
    T.children("Elpaal", blk(8, "Shaharaim in Moab", 1, 1), ref="8:12-13")
    T.find("Shema", 1, under=T.find("Elpaal")).label = "Shema · Shimei"
    T.find("Shema · Shimei").note = "8:13 Shema, 8:21 Shimei — they drove " \
                                    "out the men of Gath"

    T.children("Beriah", _house(8, "Heads of households in Jerusalem", 0, 0,
                                "Beriah"),
               under=T.find("Elpaal"), ref="8:16")
    T.children("Elpaal", _house(8, "Heads of households in Jerusalem", 1, 0,
                                "Elpaal"), ref="8:18")
    T.children("Shema · Shimei",
               _house(8, "Heads of households in Jerusalem", 1, 1,
                      "Shema · Shimei"), ref="8:21")
    T.children("Shashak", _house(8, "Heads of households in Jerusalem", 2, 0,
                                 "Shashak"), ref="8:25")
    jer = _house(8, "Heads of households in Jerusalem", 2, 1, "Jeroham")
    jer.link = "dash"
    jer.note = "8:27 gives no father; these lived in Jerusalem"
    T.child("Benjamin", jer, link="dash", ref="8:26-28")

    # 8:29 leaves the father of Gibeon unnamed; 9:35 names him Jeiel. Ner is
    # among his sons in 9:36, which is how Saul joins the Benjamite tree.
    gib = blk(8, "The fathers of Gibeon", 0, 2)
    gib.label = "Jeiel, the father of Gibeon"
    gib.kind, gib.link = "person", "dash"
    gib.note = "8:29 leaves him unnamed; 9:35 gives the name — he lived " \
               "in Gibeon"
    maac = blk(8, "The fathers of Gibeon", 0, 1)
    maac.kind, maac.link, maac.note = "woman", "wife", "his wife"
    gib.kids.insert(0, maac)
    mik = N("Mikloth", "8:31 stops at Zecher, but 8:32 goes on with "
            "Mikloth; 9:37 lists him among the sons", link="dash",
            ref="8:32")
    mik.kids = chain(8, "The fathers of Gibeon", 1, 0)[1:]     # Shimeah
    mik.kids[0].label = "Shimeah · Shimeam"
    gib.kids.append(mik)
    gib.kids.append(N("Ner", "9:36 lists him among Jeiel's sons; 8:30 does "
                      "not", link="dash", ref="9:36"))
    T.child("Benjamin", gib, link="dash", ref="8:29-32")

    saul = blk(8, "The house of Saul", 0, 0)          # Ner -> Kish -> Saul …
    T.children("Ner", saul, ref="8:33-40")
    king = T.find("Saul", under=saul)
    king.kind = "king"
    king.icon = "sword"
    king.note = "the first king — 10:13-14 tells how he died"
    T.find("Jonathan", under=king).note =         "his son Merib Baal is the Mephibosheth of 2 Samuel 4:4"
    T.find("Azel").note = "9:44 repeats his six sons"
    # 9:35-44 tells this house a second time and spells four of it
    # differently. The doubled label is how the tree already carries one man
    # under two names, and it is what lets chapter 9's verses find him.
    for a, b in (("Zecher", "Zechariah"), ("Tarea", "Tahrea"),
                 ("Jehoaddah", "Jarah"), ("Raphah", "Rephaiah")):
        try:
            n = T.find(a, under=T.find("Benjamin"))
        except KeyError:
            continue
        n.label = f"{a} · {b}"
        n.note = f"9:35-44 spells him {b}"
    # 8:39 "the sons of Eshek his brother" follows "All these were the sons
    # of Azel" (8:38): Eshek is Azel's brother, a son of Eleasah (8:37).
    # Scoped to Saul's house — a bare "Eleasah" finds Sheshan's (2:39-40).
    esh = blk(8, "The house of Saul", 1, 0)
    esh.note = "Azel's brother — his son Ulam's sons were mighty men of " \
               "valor, archers, 150 sons and sons' sons"
    T.child("Eleasah", esh, under=king, ref="8:39-40")


def _house(ch, title, col, i, label):
    """A "the sons of X" block, re-labelled as the tree's X for grafting.

    Its row is X itself ("Shimei", for the man the tree calls Shema ·
    Shimei), so the verse that ends "the sons of X" lights him. Shashak's
    stays the heading '~the sons of Shashak:': his own row among Beriah's
    sons already lights him at 8:25.
    """
    n = blk(ch, title, col, i)
    n.label = label
    return n


# ===========================================================================
# XI.  Those who came back                                    (1 Chr 9:1-34)
# ===========================================================================

def _return(T):
    ret = N("the first to live again in their cities",
            "1 Chr 9:1-3 — after Judah was carried to Babylon for their "
            "disobedience; in Jerusalem lived children of Judah, Benjamin, "
            "Ephraim and Manasseh", kind="house", link="dash", ref="9:1-3")

    # Judah's returnees, each hung where the text puts them.
    uthai = upward(9, "Of Judah and Benjamin in Jerusalem", 0, 1)
    uthai.link, uthai.note = "dash", \
        "9:4 read upward, 'of the children of Perez' — the generations " \
        "between are not given"
    T.child("Perez", uthai, link="dash", ref="9:4")
    asa = blk(9, "Of Judah and Benjamin in Jerusalem", 0, 2)
    asa.link, asa.note = "dash", "the firstborn of the Shilonites — 9:5"
    T.child("Shelah", asa, under=T.find("Judah"), link="dash", ref="9:5")
    jeu = blk(9, "Of Judah and Benjamin in Jerusalem", 0, 3)
    jeu.link, jeu.note = "dash", "of the sons of Zerah — 690 brothers, 9:6"
    T.child("Zerah", jeu, nth=1, under=T.find("Tamar"), link="dash", ref="9:6")

    ben = N("of Benjamin, in Jerusalem", "9:7-9 — 956 brothers by their "
            "generations, all heads of fathers' households", kind="house",
            link="dash", ref="9:7-9")
    # In verse order: Sallu, Ibneiah (the son of Jeroham — not 8:27's
    # Jeroham, whose sons are others), Elah, Meshullam.
    for col, i in ((1, 1), (1, 2), (1, 3), (2, 0)):
        c = upward(9, "Of Judah and Benjamin in Jerusalem", col, i)
        c.link = "dash"
        ben.kids.append(c)
    T.child("Benjamin", ben, link="dash", ref="9:7-9")

    # The priests: 9:11 "Azariah the son of Hilkiah, the son of Meshullam, the
    # son of Zadok, the son of Meraioth, the son of Ahitub" is the high
    # priests' line of 6:12-13 told again. Ezra 7:1-2 (Shallum) and Neh
    # 11:11 (Meshullam) give the same pedigree, so Shallum is Meshullam. No
    # second line is drawn: the rows are bound to the 6:12-13 men, 9:11's
    # Azariah to Hilkiah's son as head of the house. Its Meraioth has no box
    # (a note on Zadok says so); bound to nothing, it cannot light the much
    # older Meraioth of 6:6-7, nine generations above this Ahitub.
    ele = T.find("Eleazar", under=T.find("Aaron"))
    zad2 = named(ele, "Zadok", 2)                          # 6:12
    ahit2 = next(n for n in walk(ele) if zad2 in n.kids)
    shm = next(k for k in zad2.kids if k.label == "Shallum")
    hil = next(k for k in shm.kids if k.label == "Hilkiah")
    az = next(k for k in hil.kids if k.label == "Azariah")
    assert ahit2.label == "Ahitub", ahit2
    shm.label = "Shallum · Meshullam"
    zad2.note = ((zad2.note + " · ") if zad2.note else "") + \
        "9:11 and Neh 11:11 put a Meraioth between him and Ahitub; 9:11 " \
        "calls Ahitub the ruler of God's house"
    for k, n in ((4, az), (5, hil), (6, shm), (7, zad2), (8, None),
                 (9, ahit2)):
        T.bind[(9, "The priests", k)] = n
    courses = N("of the priests' courses", "9:10, 12-13 — Jedaiah, Jehoiarib "
                "and Jachin head courses 2, 1 and 21 (24:7-17); 1,760 very "
                "able men for the work of the service of God's house",
                kind="house", link="dash", ref="9:10-13")
    for lbl in ("Jedaiah", "Jehoiarib", "Jachin"):
        courses.kids.append(N(lbl, link="dash"))
    for col, i, note in ((1, 0, "9:12 read upward — of Malchijah's course"),
                         (1, 1, "9:12 read upward — of Immer's course")):
        c = upward(9, "The priests", col, i)
        c.link, c.note = "dash", note
        courses.kids.append(c)
    T.child("Aaron", courses, link="dash", ref="9:10-13")

    # The Levites: two of these lines join singers already in the tree.
    mat = upward(9, "The Levites", 0, 3)                 # Asaph -> Mattaniah
    T.children("Asaph", mat, ref="9:15")
    # 9:16 "Obadiah the son of Shemaiah, the son of Galal, the son of
    # Jeduthun": Jeduthun is the singer Ethan (_levi), so the line hangs from
    # that box and his row lights it by the label's second half. Dashed,
    # because the line is shortened: Obadiah lived after the exile.
    oba = upward(9, "The Levites", 1, 0, drop=1)         # Galal -> Obadiah
    oba.link = "dash"
    oba.note = "9:16 read upward to Jeduthun — a shortened line: Obadiah " \
               "(Abda, Neh 11:17) lived after the exile"
    T.child("Ethan · Jeduthun", oba, link="dash", ref="9:16")
    shem = upward(9, "The Levites", 0, 1)                # Merari -> Shemaiah
    shem.link, shem.note = "dash", "9:14 read upward — of the sons of Merari"
    T.child("Merari", shem, link="dash", ref="9:14")
    ber = upward(9, "The Levites", 1, 1)
    ber.link, ber.note = "dash", \
        "9:16 read upward — he lived in the villages of the Netophathites"
    T.child("Levi", ber, link="dash", ref="9:16")
    misc = blk(9, "The Levites", 0, 2)
    misc.label = "and of the Levites"
    misc.kind, misc.link, misc.note = "house", "dash",         "9:15 names them without a father"
    for k in misc.kids:
        k.link = "dash"
    T.child("Levi", misc, link="dash", ref="9:15")

    # The gatekeepers: 9:19 read upward lands on Korah's son Ebiasaph.
    gate = upward(9, "The gatekeepers", 0, 3, drop=2)    # Kore > Shallum
    gate.link = "dash"
    gate.note = "9:17-19 — the chief of the gatekeepers, who with his " \
                "brothers kept the thresholds of the tent as their fathers " \
                "kept the entry of Yahweh's camp"
    shal = named(gate, "Shallum")
    # 9:21 "Zechariah the son of Meshelemiah"; 26:1-2 "Meshelemiah the son
    # of Kore … Zechariah the firstborn". Not Shallum under another name:
    # 9:31 gives Shallum a different firstborn.
    mesh = upward(9, "The gatekeepers", 1, 1)            # Meshelemiah > Zech.
    mesh.note = "the son of Kore — 26:1; Shelemiah, 26:14"
    named(mesh, "Zechariah").note = ("keeper of the door of the tent of "
                                     "meeting — 9:21; the firstborn, 26:2")
    gate.kids.append(mesh)
    T.child("Ebiasaph", gate, nth=1, link="dash", ref="9:17-21")
    # 9:17 "The gatekeepers: Shallum, Akkub, Talmon, Ahiman" gives the other
    # three no father, and gatekeepers came from Merari too (26:10), so they
    # stand in a group under Levi ("the four chief gatekeepers, who were
    # Levites", 9:26), not as Shallum's brothers. 9:17's Shallum is the man
    # of 9:19, so that row is bound to him.
    four = blk(9, "The gatekeepers", 0, 0)
    assert [k.label for k in four.kids] == \
        ["Shallum", "Akkub", "Talmon", "Ahiman"], four.kids
    keepers = N("the gatekeepers", "9:17 gives no father; the four chiefs "
                "were Levites, 9:26; 212 in all, 9:22", kind="house",
                link="dash", ref="9:17-26")
    for k in four.kids[1:]:
        k.link = "dash"
        keepers.kids.append(k)
    T.child("Levi", keepers, link="dash", ref="9:17-26")
    T.bind[(9, "The gatekeepers", 1)] = shal
    # 9:20 "Phinehas the son of Eleazar" is Aaron's grandson (6:4), not
    # Eli's son of Ithamar's house; the row has no node of its own.
    T.bind[(9, "The gatekeepers", 13)] = T.find("Phinehas", under=ele)
    # 9:31 "Mattithiah … the firstborn of Shallum the Korahite": the
    # gatekeeper of 9:17-19.
    mat2 = blk(9, "Duties of the temple service", 1, 0)   # Mattithiah
    mat2.note = ("the firstborn of Shallum the Korahite; over the things "
                 "baked in pans")
    T.child("Shallum", mat2, under=shal, link="solid", ref="9:31")

    # 9:2 names four classes, not four men: "Israel, the priests, the
    # Levites, and the temple servants" (Neh 11:3 lists the same). The lay
    # "Israel" is relabelled so the alias index doesn't find a second
    # Israel; the rows keep their stamps, so 9:2 lights the classes and not
    # the patriarch.
    grp = blk(9, "The first to return", 1, 0)
    notes = {"the temple servants": "a class, not one man — 9:2 · whom "
             "David and the princes had given for the service of the "
             "Levites, Ezra 8:20"}
    for k in grp.kids:
        k.kind, k.link = "house", "dash"
        k.note = notes.get(k.label, "a class, not one man — 9:2")
    assert grp.kids[0].label == "Israel", grp.kids[0].label
    grp.kids[0].label = "Israel (the people)"
    ret.kids = grp.kids
    T.child("Israel", ret, link="dash", ref="9:1-3")


# ===========================================================================
# XII.  What 2 Chronicles adds
# ===========================================================================
#
# 2 Chronicles is narrative, not genealogy — but it is the book that says how
# long each of David's heirs reigned, who their mothers were, and where the
# line was very nearly cut. Those facts belong on the same chart as the names
# 1 Chronicles 3 lists, so they are attached to the kings as notes and as a
# handful of extra people.

KINGS_2CH = {
    "Solomon":   ("40 years over all Israel; he built the house — "
                  "2 Chr 9:30", None),
    "Rehoboam":  ("41 when he began, 17 years", "Naamah the Ammonitess"),
    "Abijah":    ("3 years", "Micaiah the daughter of Uriel of Gibeah"),
    "Asa":       ("41 years — 2 Chr 16:13", None),
    "Jehoshaphat": ("35 when he began, 25 years",
                    "Azubah the daughter of Shilhi"),
    "Joram":     ("32 when he began, 8 years; his father gave the kingdom "
                  "to him, the firstborn, and to his brothers silver, gold "
                  "and fortified cities in Judah; he killed all his brothers "
                  "with the sword — 2 Chr 21:3-4. He departed without being "
                  "missed", None),
    "Ahaziah":   ("42 when he began, 1 year", "Athaliah the daughter of Omri"),
    "Joash":     ("7 when he began, 40 years; his own servants, Zabad the "
                  "son of Shimeath the Ammonitess and Jehozabad the son of "
                  "Shimrith the Moabitess, killed him on his bed for the "
                  "blood of Jehoiada's sons — 2 Chr 24:25-26",
                  "Zibiah, of Beersheba"),
    "Amaziah":   ("25 when he began, 29 years; they conspired against him "
                  "and killed him at Lachish", "Jehoaddan, of Jerusalem"),
    "Azariah · Uzziah": ("16 when he began, 52 years; a leper to the day of "
                         "his death, cut off from Yahweh's house",
                         "Jechiliah, of Jerusalem"),
    "Jotham":    ("25 when he began, 16 years",
                  "Jerushah the daughter of Zadok"),
    "Ahaz":      ("20 when he began, 16 years; they didn't bring him into "
                  "the tombs of the kings", None),
    "Hezekiah":  ("25 when he began, 29 years; buried in the ascent of the "
                  "tombs of the sons of David",
                  "Abijah, the daughter of Zechariah"),
    "Manasseh":  ("12 when he began, 55 years — the longest reign", None),
    "Amon":      ("22 when he began, 2 years; his servants conspired "
                  "against him", None),
    "Josiah":    ("8 when he began, 31 years; he died at Megiddo and all "
                  "Judah and Jerusalem mourned him", None),
    "Shallum":   ("Joahaz — 23 when he began, 3 months; Neco carried him "
                  "to Egypt — 2 Chr 36:1-4", None),
    "Jehoiakim": ("Eliakim, whose name the king of Egypt changed — 25 when "
                  "he began, 11 years", None),
    "Jeconiah":  ("Jehoiachin — 8 when he began, 3 months and 10 days; "
                  "Nebuchadnezzar brought him to Babylon", None),
}


def _second_chronicles(T):
    # Every royal lookup is scoped under David. Chronicles reuses these
    # names freely, and pre-order finds the LEVITE Asa, SAMUEL'S son
    # Abijah and SHELAH'S son Joash first — five kings' reigns spent a
    # while pinned on the wrong men because this function trusted bare
    # names.
    dav = T.find("David")
    for label, (reign, mother) in KINGS_2CH.items():
        try:
            n = T.find(label, under=dav)
        except KeyError:
            continue
        bits = [reign] + ([f"his mother: {mother}"] if mother else [])
        extra = " · ".join(b for b in bits if b)
        n.note = f"{n.note} · {extra}" if n.note else extra
        if n.kind == "person":
            n.kind = "king"

    # 2 Chr 11:18-23 — Rehoboam's two named wives. Mahalath is David's
    # granddaughter twice over, which ties the royal line back on itself.
    mah = N("Mahalath", "daughter of Jerimoth the son of David, and of "
            "Abihail the daughter of Eliab the son of Jesse — 2 Chr 11:18",
            kind="woman", link="wife", ref="2 Chr 11:18-19")
    for s in ("Jeush", "Shemariah", "Zaham"):
        mah.kids.append(N(s, link="solid"))
    # 2 Chr 11:20 "she bore him Abijah, Attai, Ziza, and Shelomith": her
    # Abijah is the king of 3:10, already Rehoboam's son on the line, so he
    # is not drawn a second time under her. A cross-reference ties them.
    maa = N("Maacah", "the daughter of Absalom, whom Rehoboam loved above "
            "all his wives — 18 wives, 60 concubines, 28 sons and 60 "
            "daughters", kind="woman", link="wife", ref="2 Chr 11:20-21")
    for s in ("Attai", "Ziza", "Shelomith"):
        maa.kids.append(N(s, link="solid"))
    reh = T.find("Rehoboam", under=dav)
    abij = next(k for k in reh.kids if k.label == "Abijah")
    abij.note = ((abij.note + " · ") if abij.note else "") + \
        "whom his father made chief, the prince among his brothers, " \
        "intending to make him king — 2 Chr 11:22"
    reh.kids[0:0] = [mah, maa]
    T.link(maa, T.find("Absalom"), "Rehoboam's queen was Absalom's daughter")
    T.link(maa, abij, "she bore him Abijah — 2 Chr 11:20-22; 13:2 calls his "
           "mother Micaiah the daughter of Uriel of Gibeah")
    T.link(mah, T.find("Eliab", under=T.find("Jesse")),
           "and Mahalath was Eliab's granddaughter")

    # 2 Chr 21:2-4 — Jehoshaphat's other sons, all killed by their brother.
    # "All these were the sons of Jehoshaphat": a stated sonship, so they
    # stand solid beside Joram, the firstborn, in his row. What their
    # father gave them, and what Joram did, is in Joram's note.
    jehs = T.find("Jehoshaphat", under=dav)
    for s in ("Azariah", "Jehiel", "Zechariah", "Azariah", "Michael",
              "Shephatiah"):
        jehs.kids.append(N(s, link="solid", ref="2 Chr 21:2"))

    # 2 Chr 21:17 - 23:11 — the line down to one child, and the priest's
    # wife who kept him alive. This is the hinge of the whole chart.
    jor = T.find("Joram", under=dav)
    ath = N("Athaliah", "the daughter of Omri, Jehoram's wife; when her son "
            "Ahaziah was dead she destroyed all the royal offspring of the "
            "house of Judah, and reigned six years — 2 Chr 22:10-12",
            kind="woman", link="wife", ref="2 Chr 21:6, 22:10-12")
    jor.kids.insert(0, ath)
    raid = N("his other sons", "the Philistines and Arabians carried away "
             "all that were found in the king's house, his sons and his "
             "wives, so that none was left him except the youngest — "
             "2 Chr 21:16-17", kind="house", link="solid", ref="2 Chr 21:17")
    jor.kids.append(raid)
    ahz = T.find("Ahaziah", under=dav)
    ahz.note = (ahz.note or "") + \
        " · made king because the band that came with the Arabians had " \
        "slain all the oldest — 2 Chr 22:1"

    jsh = N("Jehoshabeath", "the king's daughter, sister of Ahaziah and "
            "wife of Jehoiada the priest; she stole Joash from among the "
            "king's sons who were slain and hid him in God's house six "
            "years — 2 Chr 22:11", kind="woman", link="solid",
            ref="2 Chr 22:11")
    jor.kids.append(jsh)
    joash = T.find("Joash", under=dav)
    T.link(jsh, joash, "she hid him, and the line of David survived")

    T.find("Ahaz", under=dav).kids.append(
        N("Maaseiah", "the king's son, whom Zichri of Ephraim killed — "
          "2 Chr 28:7", link="solid", ref="2 Chr 28:7"))

    # 3:15 makes Zedekiah Josiah's third son; 3:16 lists a Zedekiah among
    # Jehoiakim's sons. Two men, as the WEB reads 3:16: the king is Josiah's
    # son (2 Kgs 24:17-18, Jer 37:1), so only he takes the crown, the
    # shackle and the reign. 2 Chr 36:10 calls the king Jehoiachin's
    # "brother", which his note records.
    jos_k = T.find("Josiah", under=dav)
    for zed in [n for n in jos_k.kids if n.label == "Zedekiah"]:
        zed.note = ("Mattaniah, whom the king of Babylon renamed — 2 Kgs "
                    "24:17; Josiah's son (Jer 37:1), Jehoiachin's uncle, "
                    "though 2 Chr 36:10 calls him his brother · 21 when he "
                    "began, 11 years — then the land kept Sabbath seventy "
                    "years")
        zed.icon = "shackle"
        zed.kind = "king"
    jhk = next(k for k in jos_k.kids if k.label == "Jehoiakim")
    z316 = next(k for k in jhk.kids if k.label == "Zedekiah")
    assert z316.kind == "person" and z316.icon is None, z316
    z316.note = ("3:16 — listed as a son of Jehoiakim; the king Zedekiah "
                 "was Josiah's son, Jehoiachin's uncle (2 Kgs 24:17-18; "
                 "Jer 37:1)")

    # The priests 2 Chronicles names. Hilkiah is secure — 1 Chr 6:13 puts
    # him one generation before Seraiah, and 2 Chr 34 has him find the book
    # in Josiah's day. The other two the chart will not pin to a generation
    # it cannot show, so they hang beside the line instead of on it.
    hil = T.find("Hilkiah", under=T.find("Shallum · Meshullam",
                                         under=T.find("Zadok", 2)))
    hil.note = ((hil.note + " · ") if hil.note else "") +         "who found the book of the law of Yahweh given by Moses, in "         "Josiah's eighteenth year — 2 Chr 34:14"
    hil.kind, hil.icon = "priest", "scroll"

    named_2ch = N("priests 2 Chronicles names",
                  "the book calls each of these chief priest without "
                  "placing him in chapter 6's descent", kind="house",
                  link="dash", ref="2 Chr 19:11, 26:17")
    named_2ch.kids = [
        N("Amariah", "the chief priest over you in all matters of Yahweh — "
          "2 Chr 19:11", kind="priest", link="dash"),
        N("Azariah", "who went in after Uzziah with eighty valiant priests "
          "and withstood him at the altar of incense — 2 Chr 26:17",
          kind="priest", link="dash"),
    ]
    T.child("Aaron", named_2ch, link="dash")

    jhd = N("Jehoiada", "the priest who hid Joash, made him king in the "
            "seventh year and ordered the house of Yahweh; he died at 130 "
            "and they buried him among the kings — 2 Chr 23-24",
            kind="priest", link="dash", ref="2 Chr 22:11-24:16", icon="priest")
    jhd.kids.append(N("Zechariah", "the son of Jehoiada, whom Joash "
                      "commanded to be stoned in the court of Yahweh's "
                      "house — 2 Chr 24:20-22", link="solid",
                      ref="2 Chr 24:20"))
    T.child("Aaron", jhd, link="dash")
    T.link(jhd, jsh, "the priest's house and the king's, joined by marriage")


# ---------------------------------------------------------------------------
# Audit
# ---------------------------------------------------------------------------

def audit(T):
    nodes = list(walk(T.root))
    people = [n for n in nodes if n.kind != "house"]
    by_link = {}
    for n in nodes:
        by_link[n.link] = by_link.get(n.link, 0) + 1
    depth = max(n.depth for n in nodes)
    labels = {}
    for n in nodes:
        labels.setdefault(n.label, []).append(n)
    dupes = {k: len(v) for k, v in labels.items() if len(v) > 1}
    print(f"nodes            {len(nodes)}")
    print(f"  people/houses  {len(people)} / {len(nodes) - len(people)}")
    print(f"  women          {sum(1 for n in nodes if n.kind == 'woman')}")
    print(f"  kings          {sum(1 for n in nodes if n.kind == 'king')}")
    print(f"edges            solid {by_link.get('solid', 0)}  "
          f"dashed {by_link.get('dash', 0)}  wife {by_link.get('wife', 0)}")
    print(f"cross-links      {len(T.links)}")
    print(f"deepest descent  {depth} generations "
          f"({' → '.join(_spine(max(nodes, key=lambda n: n.depth)))})")
    print(f"repeated names   {len(dupes)} "
          f"(most: {sorted(dupes.items(), key=lambda kv: -kv[1])[:6]})")
    _coverage(nodes)


def _spine(n):
    out = []
    while n:
        out.append(n.label)
        n = n.parent
    return out[::-1]


def _coverage(nodes):
    """How many of the proper names in 1 Chr 1-9 made it onto the chart."""
    have = set()
    for n in nodes:
        for part in n.label.split(" · "):
            have.add(part.strip())
    missing_by_ch = {}
    for ch in range(1, 10):
        verses = load_chapter("1 Chronicles", ch).verses
        caps = set()
        for _, text in verses:
            for m in re.finditer(r"(?<![.?!“] )\b([A-Z][a-z]{2,})\b", text):
                caps.add(m.group(1))
        missing_by_ch[ch] = sorted(caps - have - _STOP)
    tot = sum(len(v) for v in missing_by_ch.values())
    print(f"names in 1 Chr 1-9 not on the chart: {tot} "
          "(most are places, peoples and sentence-openers)")
    for ch, miss in missing_by_ch.items():
        if miss:
            print(f"   ch{ch}: {', '.join(miss[:18])}"
                  f"{' …' if len(miss) > 18 else ''}")


_STOP = {
    "The", "These", "They", "There", "This", "Their", "Then", "And", "But",
    "All", "Also", "His", "Her", "Now", "For", "When", "After", "Israel",
    "Judah", "Jerusalem", "Yahweh", "God", "Egypt", "Babylon", "Moab",
    "Assyria", "Gilead", "Bashan", "Jordan", "Levites", "Levite", "Sabbath",
    "Amalekites", "Hagrites", "Meunim", "Philistines", "Ammonitess",
    "Ephrathah", "Ephrathite", "Zorathites", "Netophathites", "Kenites",
    "Horites", "Edom", "Edomites", "Seir", "Aram", "Geshur", "Recah",
    "Hebron", "Bethlehem", "Beersheba", "Gibeon", "Gath", "Manahath",
    "Ono", "Lod", "Jabez", "Tekoa", "Ziph", "Gedor", "Soco", "Zanoah",
    "Eshtemoa", "Madmannah", "Machbena", "Gibea", "Kiriath", "Jearim",
    "Keilah", "Etam",
    "Behold", "Oh", "May",
}


if __name__ == "__main__":
    audit(build())
