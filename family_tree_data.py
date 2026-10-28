"""The OT family tree's reference data: who each box is, and where the Bible
names them.

The wall chart (generate_ot_family_tree_svg.py) draws the tree; its page in
the app's Reference list (reference_viewer.py) needs to know, for a tap on
the sheet, which box was hit and what to say about it. `sidecar()` writes
that as one JSON file beside the SVG, so the SVG itself stays as it is.

Each box gets:

- a **stable id**, so a shared link to a person keeps working. A new box's
  id is the shortest run of names from it up towards Adam that no other box
  shares ("azariah.ahimaaz"); after that the box keeps the id it was
  issued, read back from the last sidecar, even when a namesake grafted
  later would have made its run longer. `N.key` is not used: it numbers
  namesakes in pre-order, so it rebinds when a graft adds one;
- its **box** on the sheet, its parent and children, and the reference chip
  a woman's second family keeps (`N.chip`);
- a **relation** that tells namesakes apart ("son of Ahimaaz", "wife of
  Boaz"), lengthened up the line until the namesakes differ;
- its generation (`printed_gen`), note and cross-references, and its
  Ussher years where `chronology.bind` dates it;
- its **verses**, from four places and never from matching names across
  the canon:
    - the box's own ref (`N.ref`, read by verse_refs.parse);
    - the 1 Chronicles 1-9 camera's reading, verse by verse
      (`svg_chronicles_world.World.lit`);
    - Matthew 1:1-17's (`matthew_tree.MatthewLine.lit`);
    - Genesis 5 and 11:10-32, from `generate_genealogy`'s tables: each
      person's verses are their own paragraph and their father's, kept
      only where the verse speaks the name.

World and matthew_tree build trees of their own, so their boxes are matched
to the chart's by walking both trees down from Adam together (`pair`):
children match by label, or where matthew_tree has joined a second name
onto a label ("Jacob · Israel" for the chart's "Israel"), by one of its
names. Boxes matthew_tree adds that the chart doesn't have (Matthew's
line past Zerubbabel, Rahab, Uriah) have no box to light, except
Bathsheba, whose cross-reference names the chart's own box for her.

`audit()` reports every camera verse whose text doesn't speak the name it
lights, for review.
"""

import re

import chronology
import chronicles_tree as CT
import generate_genealogy as GG
import verse_refs
from books import BOOK_NAMES
from passages import load_chapter, verse_numbers

walk = CT.walk


# ---------------------------------------------------------------------------
# Who a box is
# ---------------------------------------------------------------------------

def names(label):
    """The names a box goes by: "Abram · Abraham" -> ["Abram", "Abraham"]."""
    return [p.strip() for p in label.split("·") if p.strip()]


def _slug(label):
    return re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-") or "n"


def _chains(labels, parents):
    """For boxes given by label and parent index, in pre-order: each box's
    run of slugged names from itself up to Adam, and a key for the whole run
    that brothers of one name tell apart by order ("...~2")."""
    chain = []
    for i, lab in enumerate(labels):
        up, j = [], i
        while j is not None:
            up.append(_slug(labels[j]))
            j = parents[j]
        chain.append(up)
    seen, keys = {}, []
    for up in chain:
        whole = ".".join(up)
        seen[whole] = seen.get(whole, 0) + 1
        keys.append(whole if seen[whole] == 1 else f"{whole}~{seen[whole]}")
    return chain, keys


def stable_ids(nodes, issued=None):
    """{node: id}. A box keeps the id it was issued before (`issued`, {whole
    run key: id}, read from the last sidecar), so a shared link to it still
    works after namesakes are grafted elsewhere. A new box's id is its own
    name, then its parent's, and so on up, as far as it takes for no other
    box to share it; brothers of one name, which no run of names can part,
    take "~2" by their order. An id once issued is never given to another
    box."""
    issued = issued or {}
    index = {n: i for i, n in enumerate(nodes)}
    chain, keys = _chains([n.label for n in nodes],
                          [index.get(n.parent) for n in nodes])
    by_depth = {}

    def sharing(i, d):
        """Every box whose first d names are box i's."""
        if d not in by_depth:
            groups = {}
            for j, up in enumerate(chain):
                groups.setdefault(tuple(up[:d]), []).append(j)
            by_depth[d] = groups
        return by_depth[d][tuple(chain[i][:d])]

    ids, taken = {}, set(issued.values())
    for i, n in enumerate(nodes):
        if keys[i] in issued:
            ids[n] = issued[keys[i]]
    for i, n in enumerate(nodes):
        if n in ids:
            continue
        for d in range(1, len(chain[i]) + 1):
            prefix = ".".join(chain[i][:d])
            sharers = sharing(i, d)
            if len(sharers) == 1 or len({id(nodes[j].parent) for j in sharers}) == 1:
                cand = prefix
                if len(sharers) > 1:
                    order = sharers.index(i)
                    cand = prefix if order == 0 else f"{prefix}~{order + 1}"
                if cand not in taken:
                    break
        k = 2
        while cand in taken:
            cand, k = f"{prefix}~{k}", k + 1
        ids[n] = cand
        taken.add(cand)
    assert len(set(ids.values())) == len(ids), "stable ids collide"
    return ids


def issued_ids(previous):
    """{whole run key: id} from a sidecar written before, or {}."""
    if not previous:
        return {}
    items = previous["items"]
    _chain, keys = _chains([it["n"] for it in items],
                           [it.get("p") for it in items])
    return {k: it["id"] for k, it in zip(keys, items)}


# House boxes whose label only joins two lists ("and also" in 1 Chr 7:12)
# and names no group: a box under one is placed by the box above it.
CONNECTIVE = {"and also", "from them came"}


def _above(house):
    """The box a house really hangs from, past any connective houses."""
    while house.kind == "house" and house.label in CONNECTIVE \
            and house.parent is not None:
        house = house.parent
    return house


def _member_of(house):
    """How a box under a house box stands to it: the house labels are the
    chart's own phrases ("the kings of Edom", "of the royal offspring and of
    the nobles", "Zorathites", "and of the Levites")."""
    if house.label in CONNECTIVE:
        return f"under {_above(house).label}"
    lab = re.sub(r"^and\s+", "", house.label)
    if lab.startswith("the "):
        return f"among {lab}"
    if lab.startswith("of "):
        return f"one {lab}"
    if lab.endswith("ites"):
        return f"among the {lab}"
    up = f", under {house.parent.label}" if house.parent is not None else ""
    return f"in “{lab}”{up}"


def _relation(n):
    p = n.parent
    if p is None:
        return ""
    if n.rel:
        return n.rel
    child = "daughter" if n.kind == "woman" else "son"
    if n.link == "wife":
        return f"wife of {p.label}"
    if n.kind == "house":
        return f"under {_above(p).label}"
    if p.kind == "house":
        # a house that only gathers its parent's own children ("three sons")
        # stands between a father and his sons
        if p.gap == 0 and p.parent is not None:
            return f"{child} of {p.parent.label}"
        # a usurper's father stands in the kings' house only to hold his son
        if p.label.startswith("the kings of ") and n.kind != "king":
            heir = next((k for k in n.kids if k.kind == "king"), None)
            if heir is not None:
                realm = p.label[len("the kings of "):]
                return f"father of {heir.label}, king of {realm}"
        return _member_of(p)
    if n.link == "dash":
        return f"joined under {p.label}"
    return f"{child} of {p.label}"


_ORDINAL = ["first", "second", "third", "fourth", "fifth"]


def relations(nodes):
    """{node: relation}. Namesakes whose relation is the same are told
    apart by the next relation up ("son of Azariah, son of Johanan"), and
    brothers of one name by their order ("son of Jehoshaphat, named
    second")."""
    out = {n: _relation(n) for n in nodes}
    by_name = {}
    for n in nodes:
        if n.chip is None:
            by_name.setdefault(n.label, []).append(n)
    for group in by_name.values():
        level = {n: n for n in group}
        for _ in range(4):
            seen = {}
            for n in group:
                seen.setdefault(out[n], []).append(n)
            clash = [g for g in seen.values() if len(g) > 1]
            if not clash:
                break
            for same in clash:
                if len({id(n.parent) for n in same}) == 1:
                    for i, n in enumerate(same):
                        out[n] += f", named {_ORDINAL[min(i, 4)]}"
                    continue
                for n in same:
                    up = level[n].parent
                    if up is None or up.parent is None:
                        continue
                    level[n] = up
                    out[n] = f"{out[n]}, {_relation(up)}"
    return out


# ---------------------------------------------------------------------------
# Matching another build of the tree to the chart's
# ---------------------------------------------------------------------------

def _same(other, chart):
    return other.label == chart.label or chart.label in names(other.label)


def pair(other_root, chart_root):
    """{other node: chart node}, walking both trees down from Adam together.
    A child matches the first chart child, in order, not already taken,
    whose label is its label or one of its names."""
    out = {other_root: chart_root}
    stack = [(other_root, chart_root)]
    while stack:
        o, c = stack.pop()
        free = list(c.kids)
        for ok in o.kids:
            hit = next((ck for ck in free if _same(ok, ck)), None)
            if hit is None:
                continue
            free.remove(hit)
            out[ok] = hit
            stack.append((ok, hit))
    return out


def _down(node, *labels):
    for lab in labels:
        kids = [k for k in node.kids if k.label == lab and k.chip is None]
        if len(kids) != 1:
            raise LookupError(f"{node.label!r} has {len(kids)} children "
                              f"{lab!r}")
        node = kids[0]
    return node


# ---------------------------------------------------------------------------
# Verses
# ---------------------------------------------------------------------------

_TEXT = {}


def verse_text(book, ch, v):
    if (book, ch) not in _TEXT:
        _TEXT[(book, ch)] = dict(load_chapter(book, ch).verses)
    return _TEXT[(book, ch)].get(str(v)) or _TEXT[(book, ch)].get(v, "")


def speaks(label, book, ch, v):
    """True when the verse's WEB text has one of the box's names in it."""
    text = verse_text(book, ch, v)
    return any(re.search(rf"\b{re.escape(nm)}\b", text) for nm in names(label))


def _paragraphs(line, first, last):
    """{key: [verses]} for a Genesis 5 or 11 table: a person's paragraph runs
    from the verse he fathers his son to the verse before the next one."""
    starts = [(row[0], row[-1]) for row in line if row[-1] is not None]
    out = {}
    for i, (key, v) in enumerate(starts):
        end = starts[i + 1][1] - 1 if i + 1 < len(starts) else last
        out[key] = list(range(first if i == 0 else v, end + 1))
    return out


def genesis_verses(T):
    """{chart node: [(book, ch, v)]} for Genesis 5 and 11:10-32. Each person
    is looked for in his own paragraph and his father's, and kept only in
    the verses that speak his name, so the two Nahors stay apart."""
    root = T.root
    g5 = _paragraphs(GG.G5_LINE, 1, verse_numbers("Genesis", 5)[-1])
    g11 = _paragraphs(GG.G11_LINE, 10, verse_numbers("Genesis", 11)[-1])
    nodes, cur = {"Adam": root}, root
    for key in [k for k, *_ in GG.G5_LINE][1:]:
        cur = _down(cur, key)
        nodes[key] = cur
    noah = nodes["Noah"]
    sons5 = {k: _down(noah, k) for k in ("Shem", "Ham", "Japheth")}
    cur, nodes11 = sons5["Shem"], {"Shem": sons5["Shem"]}
    for key in [k for k, *_ in GG.G11_LINE][1:]:
        cur = _down(cur, "Abram · Abraham" if key == "Abram" else key)
        nodes11[key] = cur
    terah = nodes11["Terah"]
    haran = _down(terah, "Haran")
    nahor = _down(terah, "Nahor")
    family = {"Nahor (son of Terah)": nahor, "Haran": haran,
              "Lot": _down(haran, "Lot"), "Iscah": _down(haran, "Iscah"),
              "Milcah": _down(nahor, "Milcah"),
              "Sarai": _down(nodes11["Abram"], "Sarai · Sarah")}

    found = {}

    def look(node, verses, ch):
        for v in verses:
            if speaks(node.label, "Genesis", ch, v):
                found.setdefault(node, []).append(("Genesis", ch, v))

    keys5 = [k for k, *_ in GG.G5_LINE]
    for i, key in enumerate(keys5):
        own = g5.get(key, [])
        father = g5.get(keys5[i - 1], []) if i else []
        look(nodes[key], sorted(set(own + father)), 5)
    for son in sons5.values():
        look(son, g5["Noah"], 5)
    keys11 = [k for k, *_ in GG.G11_LINE]
    for i, key in enumerate(keys11):
        own = g11.get(key, [])
        father = g11.get(keys11[i - 1], []) if i else []
        look(nodes11[key], sorted(set(own + father)), 11)
    # 11:32 is Terah's death "in Haran", the town; it names none of them
    for node in family.values():
        look(node, g11["Terah"][:-1], 11)
    return found


def camera_verses(T):
    """({chart node: [(book, ch, v)]} from the two verse cameras, the
    (source label, verse) pairs for audit(), {chart node: Dated} and
    {chart node: [other names]})."""
    from svg_chronicles_world import World
    import matthew_tree

    found, checks = {}, []
    world = World()
    to_chart = pair(world.root, T.root)
    for (ch, v), lit in world.lit.items():
        for n in lit:
            if n in to_chart:
                found.setdefault(to_chart[n], []).append(("1 Chronicles", ch, v))
                checks.append((n.label, "1 Chronicles", ch, v))
            else:
                checks.append((n.label + " [no box]", "1 Chronicles", ch, v))

    MT, at = matthew_tree.build()
    to_chart = pair(MT.root, T.root)
    # Where matthew_tree joins a second name onto a box ("Jacob · Israel"),
    # the chart's box goes by that name too, so a search for it finds him.
    aliases = {}
    for n, c in to_chart.items():
        extra = [nm for nm in names(n.label) if nm not in names(c.label)]
        if extra:
            aliases[c] = extra
    for n in list(walk(MT.root)):
        if n not in to_chart:
            # a box Matthew adds: it lights the chart's box only where its
            # own cross-reference names one (Bathsheba)
            for other, _why in n.xref:
                if other in to_chart:
                    to_chart[n] = to_chart[other]
    line = matthew_tree.MatthewLine(MT, at)
    for v, lit in line.lit.items():
        for n in lit:
            if n in to_chart:
                found.setdefault(to_chart[n], []).append(("Matthew", 1, v))
                checks.append((n.label, "Matthew", 1, v))
    dated = {to_chart[n]: d for n, d in chronology.bind(MT, at).items()
             if n in to_chart}
    return found, checks, dated, aliases


def audit(checks):
    """(label, book, ch, v) pairs whose verse doesn't speak the label."""
    return [(lab, b, c, v) for lab, b, c, v in checks
            if "[no box]" in lab or not speaks(lab, b, c, v)]


# ---------------------------------------------------------------------------
# The sidecar
# ---------------------------------------------------------------------------

def _year(am):
    bc = chronology.bc(am)
    return f"{bc} BC" if bc > 0 else f"AD {1 - bc}"


def date_text(d):
    """One line for the card: the years, by kind, with the warrant."""
    about = "about " if d.soft else ""
    span = (f"{about}{_year(d.t0)}" if d.t0 == d.t1 else
            f"{about}{_year(d.t0)} – {_year(d.t1)}")
    if d.kind == "reign":
        when = f"reigned {span}"
    elif d.kind == "life" and d.t0 == d.t1:
        when = f"born {span}"      # a birth placed with no death (Esau)
    else:
        when = span
    return f"{when} (Ussher) · {d.why}"


def _verse_rows(refs):
    """Sorted, de-duplicated [book index, c1, v1, c2, v2] rows (0 = none)."""
    rows = set()
    for r in refs:
        rows.add((BOOK_NAMES.index(r.book), r.c1, r.v1 or 0, r.c2 or 0,
                  r.v2 or 0))
    return [list(r) for r in sorted(rows)]


def sidecar(T, left, top, printed_gen, previous=None):
    """The page's data, as a dict ready for json.dump, and audit()'s list.
    `left`/`top` are the sheet's origin in layout space
    (generate_ot_family_tree_svg.build_svg), `printed_gen` the chart's own
    rule for the number a box shows, and `previous` the sidecar written
    last time, whose ids the boxes keep."""
    nodes = list(walk(T.root))
    index = {n: i for i, n in enumerate(nodes)}
    ids = stable_ids(nodes, issued_ids(previous))
    rel = relations(nodes)

    refs = {n: [] for n in nodes}
    for n in nodes:
        if n.ref:
            refs[n] += verse_refs.parse(n.ref, "1 Chronicles")
    found, checks, dated, aliases = camera_verses(T)
    for n, vs in list(found.items()) + list(genesis_verses(T).items()):
        refs[n] += [verse_refs.Ref(b, c, v) for b, c, v in vs]

    items = []
    for n in nodes:
        item = {
            "id": ids[n],
            "n": n.label,
            "s": rel[n],
            "k": n.kind,
            "b": [round(n.x - left, 1), round(n.y - top, 1),
                  round(n.w, 1), round(n.h, 1)],
        }
        if n.parent is not None:
            item["p"] = index[n.parent]
        if n.kids:
            item["c"] = [index[k] for k in n.kids]
        if n.link == "wife" and n.rel:
            # on the wife line for the reckoning, not as a wife (Tamar)
            item["l"] = "kin"
        elif n.link != "solid":
            item["l"] = n.link
        if n in aliases:
            item["a"] = aliases[n]
        if n.chip is not None:
            item["x"] = index[n.chip]
        g = printed_gen(n)
        if g is not None:
            item["g"] = g
        if n.note:
            item["note"] = n.note
        if n.xref:
            item["xr"] = [[index[o], why] for o, why in n.xref]
        if n in dated:
            item["d"] = date_text(dated[n])
        rows = _verse_rows(refs[n])
        if rows:
            item["r"] = rows
        items.append(item)
    used = sorted({row[0] for it in items for row in it.get("r", [])})
    remap = {b: i for i, b in enumerate(used)}
    for it in items:
        for row in it.get("r", []):
            row[0] = remap[row[0]]
    return {"version": 1, "books": [BOOK_NAMES[b] for b in used],
            "items": items}, audit(checks)
