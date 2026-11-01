"""Matthew's and Luke's lines to Jesus, on the OT family tree.

The family tree stops where the Old Testament does. Its reference page's
"Line to Jesus" layer runs it on: Matthew 1:2-16 from Abraham, Luke 3:23-38
from Jesus back to Adam and God, and the places the two meet and part. The
generator (generate_ot_family_tree_svg.py) places and draws the layer; this
module says who is on it and what their cards say.

- `build(T)` resolves both lines to the chart's boxes by position, never by
  searching a name, because the chart has men of those names who aren't these
  (two Josephs, a Levi, two Zadoks, two Eliezers), and Israel goes by Jacob.
  Matthew's come through
  `family_tree_data.pair` over `matthew_tree`. Luke's are read from the WEB
  text (`generate_luke3`), never from `chronology.LUKE_TAIL`, and walked up
  from David. Each step of both is checked against the box's label (`SPELL`
  holds where a Gospel and the chart spell a man differently).
- `add_items` appends the layer's items to the sidecar after the tree's, and
  adds to the tree's own boxes what the two lines say of them. The tree
  itself is never touched: a graft would move hundreds of boxes, and
  `matthew_tree` and the verse cameras build on the same tree.

Where the two lines disagree the cards say so and choose nothing. The one
choice the chart does make, that Luke's Shealtiel and Zerubbabel are
Matthew's, is stated on the card that makes it.
"""

import chronology
import family_tree_data as FT
import generate_luke3
import matthew_tree
import verse_refs
from books import BOOK_NAMES

LAYER = "jesus"
LAYER_LABEL = "Line to Jesus"

# Who Matthew 1:2-16 names beside the line, not on it.
NOT_ON_LINE = {"Zerah", "Tamar", "Rahab", "Ruth", "Bathsheba", "Uriah", "Mary"}

# Matthew's names past Zerubbabel that aren't Joseph or Jesus, as READING keys.
TAIL = ["Abiud", "Eliakim", "Azor", "Zadok", "Achim", "Eliud", "Eleazar",
        "Matthan", "Jacob (of Joseph)"]

# Where a Gospel's spelling isn't the box's label.
SPELL = {"Abraham": "Abram · Abraham", "Jacob": "Israel", "Salmon": "Salma",
         "Uzziah": "Azariah · Uzziah", "Jechoniah": "Jeconiah",
         "Aram": "Ram", "Arphaxad": "Arpachshad", "Enos": "Enosh",
         "Cainan": "Kenan", "Mahalaleel": "Mahalalel"}


def tail_name(key):
    """A READING key's name: "Jacob (of Joseph)" -> "Jacob"."""
    return key.split(" (")[0]


class Lines:
    """Both lines, resolved to the chart. `matthew` is [(READING key, box or
    None)], Abraham to Jesus; `luke` is [(name, verse, box or None)], Jesus
    to God, the text's own order. None is a man the chart has no box for.
    `lower` is Luke's slots from Heli to Rhesa and `upper` from Neri to
    Mattatha, in that order; a slot's (name, verse) is unique."""

    def __init__(self, matthew, luke, mt, at, david, solomon, nathan,
                 shealtiel, zerubbabel):
        self.matthew, self.luke = matthew, luke
        self.mt, self.at = mt, at
        self.david, self.solomon, self.nathan = david, solomon, nathan
        self.shealtiel, self.zerubbabel = shealtiel, zerubbabel
        names = [s[0] for s in luke]
        iz, ish, ina = (names.index(k) for k in
                        ("Zerubbabel", "Shealtiel", "Nathan"))
        self.lower = luke[2:iz]
        self.upper = luke[ish + 1:ina]

    def box(self, name, verse=None):
        """The chart's box for a slot of Luke's line."""
        return next(b for nm, v, b in self.luke
                    if nm == name and (verse is None or v == verse))


def build(T):
    """-> Lines, for the chart's tree `T`."""
    slots, _ranges = generate_luke3.build_grid(generate_luke3.extract_line())
    MT, at = matthew_tree.build()
    to_chart = FT.pair(MT.root, T.root)
    keys = []
    for v, names in matthew_tree.READING:
        if 2 <= v <= 16:
            keys += [k for k in names if k not in NOT_ON_LINE and k not in keys]
    matthew = [(k, to_chart.get(at[k])) for k in keys]
    for k, box in matthew:
        if box is not None and box.label != SPELL.get(k, k):
            raise ValueError(f"Matthew's {k} landed on the chart's {box.label}")

    david = to_chart[at["David"]]
    up, n = [], david
    while n is not None:
        if n.link != "wife":        # the line runs through Tamar's box
            up.append(n)
        n = n.parent
    names = [s[0] for s in slots]
    known = {"Zerubbabel": to_chart[at["Zerubbabel"]],
             "Shealtiel": to_chart[at["Shealtiel"]],
             "Nathan": FT._down(david, "Nathan")}
    luke, j = [], 0
    for sl, (name, v) in enumerate(slots):
        box = None
        if name in known and sl < names.index("David"):
            box = known[name]
        # Luke 3:36's Cainan has no box: Genesis 11:12 has no such man
        elif sl >= names.index("David") and name != "God" \
                and (name, v) != ("Cainan", 36):
            box = up[j]
            j += 1
            if box.label != SPELL.get(name, name):
                raise ValueError(f"Luke 3:{v} reads {name}; the chart's line "
                                 f"has {box.label} there")
        luke.append((name, v, box))
    if j != len(up):
        raise ValueError(f"Luke's line stops {len(up) - j} boxes short of Adam")
    return Lines(matthew, luke, MT, at, david, to_chart[at["Solomon"]],
                 known["Nathan"], known["Shealtiel"], known["Zerubbabel"])


def _rows(refs):
    """A sidecar's verse rows for a written list of references."""
    return FT._verse_rows(verse_refs.parse(refs, "Luke"))


def add_items(items, index, sheet, left, top):
    """Append the layer to the sidecar's `items` (at their canonical book
    indexes), and return its top-level additions (`lines`, `layers`, `step`).
    `index` is {tree box: item index} and `sheet` the layout
    (generate_ot_family_tree_svg.place_gospel_lines)."""
    L = sheet.lines

    def rect(b):
        return [round(b[0] - left, 1), round(b[1] - top, 1),
                round(b[2], 1), round(b[3], 1)]

    def box(n):
        return rect((n.x, n.y, n.w, n.h))

    def add(**kw):
        items.append({**kw, "ly": LAYER})
        return len(items) - 1

    def add_verse(i, row):
        items[i]["r"] = sorted(items[i].get("r", []) + [row])

    # -- the people ----------------------------------------------------------
    verses = {}
    for v, names in matthew_tree.READING:
        for k in names:
            if v > 1:
                verses.setdefault(k, []).append(v)
    tail = {}
    for k, father in zip(TAIL, ["Zerubbabel"] + TAIL):
        tail[k] = add(id=f"{tail_name(k).lower()}.matthew", n=tail_name(k),
                      s=f"son of {tail_name(father)}, Matthew 1:{verses[k][0]}",
                      k="person", b=box(sheet.tail[k]),
                      r=_rows("; ".join(f"Matthew 1:{v}" for v in verses[k])))
    joseph = add(id="joseph.mary", n="Joseph", s="the husband of Mary",
                 k="person", b=box(sheet.joseph),
                 note="Jacob's son in Matthew 1:16, Heli's in Luke 3:23. "
                      "Both lines are drawn.",
                 r=_rows("Matthew 1:16; Luke 3:23"))
    mary = add(id="mary.joseph", n="Mary", s="the wife of Joseph", k="woman",
               b=box(sheet.mary), l="wife", r=_rows("Matthew 1:16"))
    jesus = add(id="jesus", n="Jesus", s="who is called Christ", k="christ",
                b=box(sheet.jesus),
                # Ussher's year alone: the chronology's note on it goes on to
                # date a census the verses on this card don't mention
                d=FT.date_text(chronology.bind(L.mt, L.at)[L.at["Jesus"]]
                               ._replace(why="AM 4000")),
                r=_rows("Matthew 1:1; Matthew 1:16; Matthew 1:17; Luke 3:23"))

    # Luke's men by slot: Rhesa on to Heli, then Mattatha on to Neri
    slots = [(nm, v) for nm, v, _b in L.luke]
    luke = {}
    for nm, v, _b in [*reversed(L.lower), *reversed(L.upper)]:
        father, fv = slots[slots.index((nm, v)) + 1]
        cite = f"3:{v}" if fv == v else f"3:{v}-{fv}"
        luke[nm, v] = add(id=f"{nm.lower()}.luke-3-{v}", n=nm,
                          s=f"son of {father}, Luke {cite}", k="person",
                          b=box(sheet.luke[nm, v]), r=_rows(f"Luke 3:{v}"))
    arpachshad, shelah = L.box("Arphaxad"), L.box("Shelah")
    cainan = add(id="cainan.luke-3-36", n="Cainan", s="son of Arphaxad, Luke 3:36",
                 k="person", b=box(sheet.cainan), p=index[arpachshad],
                 c=[index[shelah]], r=_rows("Luke 3:36"),
                 note="Luke 3:35-36 stands him between Shelah and Arphaxad. "
                      "Genesis 11:12 and 1 Chronicles 1:18 and 1:24 make "
                      "Arpachshad Shelah's own father, so the tree's line "
                      "stays and he is drawn beside it.")
    neri, mattatha = luke[L.upper[0][:2]], luke[L.upper[-1][:2]]
    pill = add(id="shealtiel.luke-3-27", n="Shealtiel", s="son of Neri, Luke 3:27",
               k="person", b=box(sheet.pill), x=index[L.shealtiel], p=neri)

    # who hangs under whom, on the cards only
    zerubbabel = index[L.zerubbabel]
    chain = [tail[k] for k in TAIL]
    items[chain[0]]["p"] = zerubbabel
    for a, b in zip(chain, chain[1:]):
        items[b]["p"], items[a]["c"] = a, [b]
    items[chain[-1]]["c"] = [joseph]
    for slot, i in luke.items():
        up = luke.get(slots[slots.index(slot) + 1])
        if up is not None:
            items[i]["p"], items[up]["c"] = up, [i]
    rhesa, heli = luke[L.lower[-1][:2]], luke[L.lower[0][:2]]
    items[rhesa]["p"], items[heli]["c"] = zerubbabel, [joseph]
    items[mattatha]["p"], items[neri]["c"] = index[L.nathan], [pill]
    items[joseph]["c"], items[mary]["p"] = [mary], joseph

    # -- the places the lines meet and part ----------------------------------
    m_names = [k for k, _b in L.matthew]
    david_on = m_names.index("David")
    she_on = m_names.index("Shealtiel")
    m_kings = she_on - david_on - 1
    l_kings = len(L.upper) + 1                  # Nathan, Mattatha to Neri
    m_tail, l_tail = len(TAIL), len(L.lower)
    to_joseph = 2 + m_tail + m_kings, 2 + l_tail + l_kings
    tree_gens = L.shealtiel.gen - L.david.gen - 1
    # his number on this tree's count, had he a box of its own
    jesus_gen = L.zerubbabel.gen + m_tail + 2

    def stop(key, **kw):
        return add(b=rect(sheet.marks[key][0]), pc=True, nos=True, **kw)

    def frame(key):
        return rect(sheet.frames[key])

    stops = {}
    stops["god"] = stop(
        "god", id="god.luke-3-38", n="God", s="the end of Luke's line, 3:38",
        tx=[["Luke's line",
             "It ends “the son of Adam, the son of God.” Matthew's opens at "
             "Abraham, so from Adam to Terah only Luke runs."],
            ["Spellings",
             "Luke's Arphaxad, Mahalaleel, Cainan (3:37) and Enos are this "
             "tree's Arpachshad, Mahalalel, Kenan and Enosh. His other Cainan "
             "(3:36) isn't in Genesis 11, and is drawn beside the tree's line."]],
        see=[index[L.box("Adam")], index[L.box("Cainan", 37)], cainan],
        rg=[["Verses", _rows("Luke 3:34-38")]])
    stops["abraham"] = stop(
        "abraham", id="stop.matthew-opens", n="Matthew opens at Abraham",
        s="one line from here to David",
        tx=[["Abraham to David",
             "Matthew 1:2-6 and Luke 3:31-34 name the same fourteen men. "
             "Between the Gospels only Ram and Aram differ."],
            ["On this tree",
             "The line also passes through Tamar's box, between Judah and "
             "Perez. Matthew 1:3 names her; Luke names no women. Matthew "
             "1:5-6 also names Rahab and Uriah, who have no box here."]],
        see=[index[L.david]],
        rg=[["Verses", _rows("Matthew 1:2-6; Luke 3:31-34")]])
    stops["david"] = stop(
        "david", id="stop.part-david", n="The lines part at David",
        s="Solomon in Matthew, Nathan in Luke", fr=frame("david"),
        tx=[["Full brothers",
             "1 Chronicles 3:5 lists both among Bathshua's four sons."],
            ["How long",
             f"Between David and Shealtiel Matthew has {m_kings} names, Luke "
             f"{l_kings} and this tree {tree_gens} generations. No name is "
             f"shared."],
            ["Matthew passes over",
             "Ahaziah, Joash and Amaziah (1 Chronicles 3:11-12), between "
             "Joram and Uzziah in Matthew 1:8; and Jehoiakim (1 Chronicles "
             "3:15-16), between Josiah and Jechoniah in Matthew 1:11."]],
        see=[index[L.solomon], index[L.nathan], mattatha],
        rg=[["Verses", _rows("Matthew 1:6; Matthew 1:8; Matthew 1:11; Luke 3:31; "
                             "1 Chronicles 3:5; 1 Chronicles 3:11-12; "
                             "1 Chronicles 3:15-16")]])
    stops["shealtiel"] = stop(
        "shealtiel", id="stop.meet-shealtiel",
        n="The lines meet at Shealtiel and Zerubbabel",
        s="the same two names, in the same order", fr=frame("shealtiel"),
        tx=[["The chart's choice",
             "Neither Gospel says these are the other's men. The chart draws "
             "them as one pair, on the names and their order."],
            ["Shealtiel's father",
             "Jechoniah in Matthew 1:12, Jeconiah in 1 Chronicles 3:17. Neri "
             "in Luke 3:27."],
            ["Zerubbabel's father",
             "Shealtiel in Matthew 1:12, Luke 3:27, Ezra 3:2 and Haggai 1:1. "
             "Pedaiah in 1 Chronicles 3:19, where this tree hangs him."]],
        see=[index[L.shealtiel], zerubbabel, neri],
        rg=[["Verses", _rows("Matthew 1:12; Luke 3:27; 1 Chronicles 3:17; "
                             "1 Chronicles 3:19; Ezra 3:2; Haggai 1:1")]])
    stops["zerubbabel"] = stop(
        "zerubbabel", id="stop.part-zerubbabel",
        n="The lines part after Zerubbabel", s="Abiud in Matthew, Rhesa in Luke",
        fr=frame("zerubbabel"),
        tx=[["How long",
             f"Matthew has {m_tail} names on to Jacob, Luke {l_tail} on to "
             f"Heli. No name is shared."],
            ["Chronicles",
             "1 Chronicles 3:19-20 lists his children and names neither."]],
        see=[chain[0], rhesa],
        rg=[["Verses", _rows("Matthew 1:13; Luke 3:27; 1 Chronicles 3:19-20")]])
    stops["joseph"] = stop(
        "joseph", id="stop.meet-joseph", n="The lines meet at Joseph",
        s="and go on to Jesus", fr=frame("joseph"),
        tx=[["Joseph's father", "Jacob in Matthew 1:16. Heli in Luke 3:23."],
            ["How long",
             f"Between David and Joseph Matthew has {to_joseph[0]} names, "
             f"Luke {to_joseph[1]}."],
            ["The join",
             "Matthew 1:16: “Joseph, the husband of Mary, from whom was born "
             "Jesus.” Luke 3:23: “being the son (as was supposed) of Joseph.” "
             "Neither says Joseph became his father."]],
        see=[joseph, mary, jesus],
        rg=[["Verses", _rows("Matthew 1:16; Luke 3:23")]])
    order = ["god", "abraham", "david", "shealtiel", "zerubbabel", "joseph"]
    for n, key in enumerate(order):
        items[stops[key]]["st"] = [
            stops[order[n - 1]] if n else None,
            stops[order[n + 1]] if n + 1 < len(order) else None]

    # Mary's son by a row of her own, not as a child: under Joseph's wife that
    # would read "With Mary: Jesus", the one thing neither Gospel says
    items[mary]["rows"] = [["Son, Matthew 1:16", [jesus]]]
    items[jesus]["rows"] = [
        ["Mother, Matthew 1:16", [mary]],
        ["As was supposed, Luke 3:23", [joseph]],
        ["Where the lines meet and part", [stops[k] for k in order[1:]]]]
    items[jesus]["tx"] = [
        ["Matthew's fourteens",
         "Matthew 1:17 says fourteen three times. The names come to 14, 14 "
         "and 13; the last reaches 14 if Jechoniah counts again."],
        ["Generations",
         f"These boxes carry no number. Luke's list makes him the "
         f"{len(L.luke) - 1}th from Adam. On this tree's count Matthew's "
         f"line makes him the {jesus_gen}th, with the four kings he passes."]]
    items[joseph]["rows"] = [["Matthew's line", [chain[-1]]],
                             ["Luke's line", [heli]],
                             ["Where they meet", [stops["joseph"]]]]
    for b, keys in ((L.box("Abraham"), ["abraham"]), (L.david, ["david"]),
                    (L.shealtiel, ["shealtiel"]),
                    (L.zerubbabel, ["shealtiel", "zerubbabel"])):
        items[index[b]]["rows"] = [["Matthew and Luke",
                                    [stops[k] for k in keys]]]

    # -- the two lines -------------------------------------------------------
    named = {"Joseph": joseph, "Jesus": jesus, **tail}
    m_line = [index[b] if b is not None else named[k] for k, b in L.matthew]
    l_line = []
    for nm, v, b in L.luke:
        if b is not None:
            l_line.append(index[b])
        elif nm == "God":
            l_line.append(stops["god"])
        elif (nm, v) == ("Cainan", 36):
            l_line.append(cainan)
        else:
            l_line.append(luke.get((nm, v), named.get(nm)))
    for i in set(m_line) | set(l_line):
        items[i]["tl"] = [n for n, ln in enumerate((m_line, l_line)) if i in ln]

    # -- what the lines add to the tree's own boxes --------------------------
    luke_row = [BOOK_NAMES.index("Luke"), 3]
    for nm, v, b in L.luke:
        if b is not None:
            add_verse(index[b], luke_row + [v, 0, 0])

    # Where a Gospel spells a box's man otherwise, the box goes by that name
    # too and says where. Kenan alone goes by Cainan: 3:36's is the new box.
    spelled = {}
    for k, b in L.matthew:
        if b is not None and tail_name(k) not in FT.names(b.label):
            v = verses[k][0]
            spelled.setdefault(b, {}).setdefault(k, []).append(f"Matthew 1:{v}")
    for nm, v, b in L.luke:
        if b is not None and nm not in FT.names(b.label):
            spelled.setdefault(b, {}).setdefault(nm, []).append(f"Luke 3:{v}")
    for b, forms in spelled.items():
        it = items[index[b]]
        for nm, where in forms.items():
            if nm not in it.get("a", []):
                it["a"] = it.get("a", []) + [nm]
            verb = "reads" if len(where) == 1 else "read"
            said = f"{' and '.join(where)} {verb} {nm}."
            it["note"] = f"{it['note']} · {said}" if it.get("note") else said

    def also(b, other, why):
        items[index[b]].setdefault("xr", []).append([other, why])

    also(L.shealtiel, pill,
         "Luke 3:27 makes him the son of Neri; Matthew 1:12 the son of "
         "Jechoniah, and 1 Chronicles 3:17 of Jeconiah")
    also(L.zerubbabel, chain[0],
         "Matthew 1:13 goes on through Abiud; 1 Chronicles 3:19-20 doesn't "
         "name him")
    also(L.zerubbabel, rhesa,
         "Luke 3:27 goes on through Rhesa and calls Zerubbabel the son of "
         "Shealtiel; 1 Chronicles 3:19-20 doesn't name Rhesa")
    also(L.nathan, mattatha,
         "Luke 3:31 runs the line through Nathan, where Matthew 1:6 runs it "
         "through Solomon")
    boxes = dict(L.matthew)
    also(boxes["Joram"], index[boxes["Uzziah"]],
         "Matthew 1:8 goes straight to Uzziah; 1 Chronicles 3:11-12 has "
         "Ahaziah, Joash and Amaziah between")
    also(boxes["Josiah"], index[boxes["Jechoniah"]],
         "Matthew 1:11 goes straight to Jechoniah; 1 Chronicles 3:15-16 has "
         "Jehoiakim between")
    also(arpachshad, cainan,
         "Luke 3:35-36 stands Cainan between Shelah and him; Genesis 11:12 "
         "doesn't")

    return {"lines": [["Matthew's line, Abraham to Jesus", m_line],
                      ["Luke's line, Jesus to God", l_line]],
            "layers": [{"id": LAYER, "label": LAYER_LABEL, "on": False,
                        "fr": rect(sheet.frames["layer"])}],
            "step": "Along the two lines"}
