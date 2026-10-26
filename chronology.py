"""The chronology layer: years for the family tree. See docs/design/ot-timeline.md.

The tree that `chronicles_tree` and `ot_grafts` weld together is structural —
it knows who begat whom, and nothing about when. This module knows when,
for the minority of people the text or the record can actually date, and it
knows the rules for guessing about everybody else in a way that is stated
on the sheet rather than hidden.

Three kinds of date, all kept in Anno Mundi (years from Adam) internally:

    life   (birth, death)       Genesis 5 and 11 give both for every link;
                                a handful of patriarchs and Moses besides.
    reign  (accession, end)     the kings, from Ussher's tables.
    at     (one year)           a person placed by an event the text ties
                                him to — Daniel carried to Babylon, Ezra's
                                journey, Jaddua meeting Alexander.

The Genesis 5/11 spine is COMPUTED from the begetting ages, not typed in.
Everything else is data with a warrant beside it.

The BC anchor is Ussher's, because those are the years that stood in the
margins of the Authorized Version for two centuries. The monarchy is
Ussher's too, for consistency; the modern synchronised dates (Thiele, on
the Assyrian eponym canon) run twenty to forty-five years later through
the divided kingdom and converge by the exile. `MODERN` carries the pairs
so a second rail can show the drift.

Run `python chronology.py` for the audit: what binds, what does not, and
how much of the tree is dated (about 7%).
"""

from collections import namedtuple

from chronicles_tree import walk

# ---------------------------------------------------------------------------
# The switches — see docs/design/ot-timeline.md §3.2. Each moves everything upstream of it.
# ---------------------------------------------------------------------------

CREATION_BC = 4004        # Ussher.  bc = CREATION_BC - am
ABRAM_BIRTH = 130         # Terah's age at Abram: 70 (Gen 11:26) | 130 (Acts 7:4)

# (name, age at begetting the next link, total years)  — Masoretic text
GEN5 = [("Adam", 130, 930), ("Seth", 105, 912), ("Enosh", 90, 905),
        ("Kenan", 70, 910), ("Mahalalel", 65, 895), ("Jared", 162, 962),
        ("Enoch", 65, 365), ("Methuselah", 187, 969), ("Lamech", 182, 777),
        ("Noah", 500, 950)]
GEN11 = [("Shem", 100, 600), ("Arpachshad", 35, 438), ("Shelah", 30, 433),
         ("Eber", 34, 464), ("Peleg", 30, 239), ("Reu", 32, 239),
         ("Serug", 30, 230), ("Nahor", 29, 148), ("Terah", 70, 205)]


def bc(am):
    return CREATION_BC - am


def am(bc_year):
    return CREATION_BC - bc_year


def spine():
    """-> ({name: (birth_am, death_am)}, flood_am). Genesis 5 and 11, added."""
    out, t = {}, 0
    for name, beget, total in GEN5:
        out[name] = (t, t + total)
        t += beget
    flood = out["Noah"][0] + 600                  # Gen 7:6
    t = flood + 2 - 100                           # Shem 100, two years after
    for name, beget, total in GEN11:
        out[name] = (t, t + total)
        t += beget
    abram = out["Terah"][0] + ABRAM_BIRTH
    out["Abram · Abraham"] = (abram, abram + 175)  # Gen 25:7
    return out, flood


SPINE, FLOOD = spine()
ABRAHAM = SPINE["Abram · Abraham"][0]

# ---------------------------------------------------------------------------
# Dates
# ---------------------------------------------------------------------------

Dated = namedtuple("Dated", "kind t0 t1 why soft")
# kind: life | reign | at.   t0/t1 in AM.   soft: an approximate placing.


def life(b, d, why, soft=False):
    return Dated("life", am(b), am(d), why, soft)


def reign(a, e, why, soft=False):
    return Dated("reign", am(a), am(e), why, soft)


def at_(y, why, soft=False):
    return Dated("at", am(y), am(y), why, soft)


def _lifeam(b, d, why):
    return Dated("life", b, d, why, False)


# A locator is a tuple of labels. Its head is resolved as: "root" -> Adam;
# a key of matthew_tree's `at` dict -> that node; otherwise a label that
# must be UNIQUE on the whole tree. Every later element is stepped to as a
# child of the previous one, and must match exactly one child. This is the
# same discipline matthew_tree uses, for the same reason: 205 labels on the
# tree are reused, and pre-order `find` picks whichever copy comes first.

def _chain(names):
    """Locators for a straight descent from Adam, one per name."""
    out, path = [], ["root"]
    for n in names:
        path = path + [n]
        out.append(tuple(path))
    return out


_G5 = [n for n, _, _ in GEN5][1:]                 # Seth … Noah (Adam is root)
_G11 = [n for n, _, _ in GEN11] + ["Abram · Abraham"]

BIND = []
BIND.append((("root",), _lifeam(*SPINE["Adam"], "Gen 5:3-5")))
for loc, name in zip(_chain(_G5 + _G11), _G5 + _G11):
    b, d = SPINE[name]
    ref = "Gen 5" if name in dict((n, 1) for n, _, _ in GEN5) else "Gen 11"
    BIND.append((loc, _lifeam(b, d, ref)))

JACOB = ("Jacob",)                                # matthew_tree's `at`
BIND += [
    # -- the patriarchs: the text gives ages, Ussher gives the years -------
    (("Abraham", "Ishmael"),   life(1910, 1773, "Gen 16:16, 25:17")),
    (("Isaac",),               life(1896, 1716, "Gen 21:5, 35:28")),
    (("Isaac", "Esau"),        life(1836, 1836, "Gen 25:26 — Jacob's twin", soft=True)),
    (("Jacob",),               life(1836, 1689, "Gen 25:26, 47:28")),
    (JACOB + ("Joseph",),      life(1745, 1635, "Gen 41:46, 50:26")),
    (JACOB + ("Levi", "Kohath", "Amram", "Moses"),
                               life(1571, 1451, "Ex 7:7, Deut 34:7")),
    (JACOB + ("Levi", "Kohath", "Amram", "Aaron"),
                               life(1574, 1452, "Ex 7:7, Num 33:39")),
    (JACOB + ("Joseph", "Ephraim", "Beriah", "Rephah", "Telah",
              "Tahan", "Ladan", "Ammihud", "Elishama", "Nun", "Joshua"),
                               life(1536, 1426, "Josh 24:29 — 110 years", soft=True)),
    (("Nahshon",),             at_(1491, "Num 1:7 — prince of Judah at the Exodus", soft=True)),

    # -- the united kingdom --------------------------------------------------
    (JACOB + ("Benjamin", "Jeiel, the father of Gibeon", "Ner", "Kish", "Saul"),
                               reign(1095, 1055, "Acts 13:21 — 40 years")),
    (("David",),               life(1085, 1015, "2 Sam 5:4 — 70 years")),
    (("Solomon",),             reign(1015, 975, "1 Kgs 11:42 — 40 years")),

    # -- Judah, from Ussher's tables ---------------------------------------
    (("Rehoboam",),    reign(975, 958, "1 Kgs 14:21 — 17 years")),
    (("Abijah",),      reign(958, 955, "1 Kgs 15:2 — 3 years")),
    (("Asa",),         reign(955, 914, "1 Kgs 15:10 — 41 years")),
    (("Jehoshaphat",), reign(914, 889, "1 Kgs 22:42 — 25 years")),
    (("Joram",),       reign(892, 885, "2 Kgs 8:17 — 8 years")),
    (("Ahaziah",),     reign(885, 884, "2 Kgs 8:26 — 1 year")),
    (("Joash",),       reign(878, 839, "2 Kgs 12:1 — 40 years")),
    (("Amaziah",),     reign(839, 810, "2 Kgs 14:2 — 29 years")),
    (("Uzziah",),      reign(810, 758, "2 Kgs 15:2 — 52 years")),
    (("Jotham",),      reign(758, 742, "2 Kgs 15:33 — 16 years")),
    (("Ahaz",),        reign(742, 726, "2 Kgs 16:2 — 16 years")),
    (("Hezekiah",),    reign(726, 698, "2 Kgs 18:2 — 29 years")),
    (("Manasseh",),    reign(698, 643, "2 Kgs 21:1 — 55 years")),
    (("Amon",),        reign(643, 641, "2 Kgs 21:19 — 2 years")),
    (("Josiah",),      reign(641, 610, "2 Kgs 22:1 — 31 years")),
    (("Josiah", "Shallum"),   reign(610, 610, "2 Kgs 23:31 — Jehoahaz, 3 months")),
    (("Jehoiakim",),   reign(610, 599, "2 Kgs 23:36 — 11 years")),
    (("Jechoniah",),   reign(599, 599, "2 Kgs 24:8 — 3 months")),
    (("Josiah", "Zedekiah"),  reign(599, 588, "2 Kgs 24:18 — 11 years; the city fell")),

    # -- Israel, from Ussher's tables --------------------------------------
    (JACOB + ("Joseph", "Ephraim", "Nebat", "Jeroboam"),
                               reign(975, 954, "1 Kgs 14:20 — 22 years")),
    (JACOB + ("Joseph", "Ephraim", "Nebat", "Jeroboam", "Nadab"),
                               reign(954, 953, "1 Kgs 15:25 — 2 years")),
    (JACOB + ("Issachar", "Ahijah", "Baasha"),
                               reign(953, 930, "1 Kgs 15:33 — 24 years")),
    (JACOB + ("Issachar", "Ahijah", "Baasha", "Elah"),
                               reign(930, 929, "1 Kgs 16:8 — 2 years")),
]
_NORTH = JACOB + ("the kings of Israel",)
BIND += [
    (_NORTH + ("Zimri",),                       reign(929, 929, "1 Kgs 16:15 — seven days")),
    (_NORTH + ("Omri",),                        reign(929, 918, "1 Kgs 16:23 — 12 years")),
    (_NORTH + ("Omri", "Ahab"),                 reign(918, 897, "1 Kgs 16:29 — 22 years")),
    (_NORTH + ("Omri", "Ahab", "Ahaziah"),      reign(897, 896, "1 Kgs 22:51 — 2 years")),
    (_NORTH + ("Omri", "Ahab", "Joram"),        reign(896, 884, "2 Kgs 3:1 — 12 years")),
    (_NORTH + ("Omri", "Ahab", "Athaliah"),     reign(884, 878, "2 Kgs 11:3 — six years over Judah")),
    (_NORTH + ("Jehu",),                        reign(884, 856, "2 Kgs 10:36 — 28 years")),
    (_NORTH + ("Jehu", "Jehoahaz"),             reign(856, 839, "2 Kgs 13:1 — 17 years")),
    (_NORTH + ("Jehu", "Jehoahaz", "Joash"),    reign(839, 825, "2 Kgs 13:10 — 16 years")),
    (_NORTH + ("Jehu", "Jehoahaz", "Joash", "Jeroboam"),
                                                reign(825, 784, "2 Kgs 14:23 — 41 years")),
    (_NORTH + ("Jehu", "Jehoahaz", "Joash", "Jeroboam", "Zechariah"),
                                                reign(773, 773, "2 Kgs 15:8 — six months")),
    (_NORTH + ("Jabesh", "Shallum"),            reign(772, 772, "2 Kgs 15:13 — one month")),
    (_NORTH + ("Gadi", "Menahem"),              reign(772, 761, "2 Kgs 15:17 — 10 years")),
    (_NORTH + ("Gadi", "Menahem", "Pekahiah"),  reign(761, 759, "2 Kgs 15:23 — 2 years")),
    (_NORTH + ("Remaliah", "Pekah"),            reign(759, 739, "2 Kgs 15:27 — 20 years")),
    (_NORTH + ("Elah", "Hoshea"),               reign(730, 721, "2 Kgs 17:1 — 9 years; Samaria fell")),

    # -- exile and return: placed by the event the text ties them to -------
    (("Zephaniah",),           at_(630, "Zeph 1:1 — in the days of Josiah", soft=True)),
    (("Abiathar", "Hilkiah", "Jeremiah"),
                               at_(627, "Jer 1:2 — Josiah's thirteenth year")),
    (("Judah", "of the royal offspring and of the nobles", "Daniel"),
                               at_(606, "Dan 1:1 — carried to Babylon")),
    # Dan 1:6 names the other three in the same deportation. Undated, they
    # would sit a generation below the house, centuries before Daniel.
    (("Judah", "of the royal offspring and of the nobles", "Hananiah"),
                               at_(606, "Dan 1:6 — carried to Babylon with Daniel")),
    (("Judah", "of the royal offspring and of the nobles", "Mishael"),
                               at_(606, "Dan 1:6 — carried to Babylon with Daniel")),
    (("Judah", "of the royal offspring and of the nobles", "Azariah"),
                               at_(606, "Dan 1:6 — carried to Babylon with Daniel")),
    (("Ezekiel",),             at_(593, "Ezek 1:2 — the fifth year of the captivity")),
    (("Zerubbabel",),          at_(536, "Ezra 2:2 — led the return")),
    (("Jehozadak", "Jeshua"),  at_(536, "Ezra 3:2 — built the altar")),
    (JACOB + ("Levi", "Iddo", "Berechiah", "Zechariah"),
                               at_(520, "Zech 1:1 — the second year of Darius")),
    (("Mordecai",),            at_(478, "Est 2:16 — Ahasuerus' seventh year", soft=True)),
    (("Hadassah · Esther",),
                               at_(478, "Est 2:16 — taken to the king", soft=True)),
    (("Ezra",),                at_(457, "Ezra 7:8 — Artaxerxes' seventh year")),
    (("Jehozadak", "Jeshua", "Joiakim", "Eliashib"),
                               at_(445, "Neh 3:1 — high priest when the wall was built")),
    (("Jehozadak", "Jeshua", "Joiakim", "Eliashib", "Joiada", "Jonathan", "Jaddua"),
                               at_(332, "Neh 12:22; Josephus Ant. 11.8 — met Alexander", soft=True)),
    (("Jesus",),               at_(4, "AM 4000 in Ussher; Herod died 4 BC — Luke's census is AD 6")),
]

# ---------------------------------------------------------------------------
# Landmarks — the lines drawn across the whole sheet
# ---------------------------------------------------------------------------

EVENTS = [                    # (year, label, strong)
    (bc(FLOOD),  "THE FLOOD",                       True),
    (1921,       "Abram called out of Haran",       False),
    (1706,       "Israel goes down into Egypt",     False),
    (1491,       "THE EXODUS",                      True),
    (1012,       "the Temple founded",              False),
    (975,        "THE KINGDOM DIVIDED",             True),
    (721,        "Samaria falls to Assyria",        False),
    (588,        "JERUSALEM FALLS",                 True),
    (536,        "the return under Cyrus",          False),
    (332,        "Alexander in Jerusalem",          False),
    (4,          "JESUS BORN",                      True),
]

ZONES = [                     # (from_bc, to_bc, title, what it means)
    (CREATION_BC, 1706, "THE TEXT COUNTS THE YEARS",
     "Genesis 5 and 11 give every man's age at his son's birth and at his "
     "death. Nothing here rests on any source but the verses."),
    (1706, 1095, "THE ELASTIC STRETCH",
     "430 years in Egypt or 215; 480 to the Temple or 440 or the sum of "
     "Judges. Drawn on Ussher's reading, but the ends are soft."),
    (1095, 588, "THE KINGS, YEAR BY YEAR",
     "Regnal years, summed. From about 850 BC the Assyrian eponym canon "
     "anchors them to the calendar — the right-hand rail shows where the "
     "two counts part company."),
    (588, 332, "EXILE AND RETURN",
     "Persian reigns are fixed by Babylonian astronomy; the biblical "
     "events float inside them."),
    (332, 4, "THE SILENCE",
     "From Jaddua to Joseph the genealogy is not recorded. Matthew's ten "
     "names and Luke's eighteen cross the gap, and share none."),
]

# Ussher's year -> the modern synchronised year, at the events where the
# two are both known. The drift is 44 years at the division and 2 at the
# fall, which is the story of what the Assyrian records did to the count.
MODERN = [
    (1015, 971, "Solomon"),
    (975,  931, "the kingdom divided"),
    (918,  874, "Ahab — Qarqar 853"),
    (884,  841, "Jehu — the Black Obelisk"),
    (726,  716, "Hezekiah"),
    (721,  722, "Samaria falls"),
    (588,  586, "Jerusalem falls"),
    (536,  538, "the return"),
    (4,    4,   "Herod dies"),
]

LUKE_TAIL = ["Rhesa", "Joanan", "Joda", "Josech", "Semein", "Mattathias",
             "Maath", "Naggai", "Esli", "Nahum", "Amos", "Mattathias",
             "Joseph", "Jannai", "Melchi", "Levi", "Matthat", "Heli"]

# ---------------------------------------------------------------------------
# Binding to the tree
# ---------------------------------------------------------------------------


class BindError(LookupError):
    pass


def locate(T, at, path):
    head, *rest = path
    if head == "root":
        cur = T.root
    elif head in at:
        cur = at[head]
    else:
        hits = [n for n in walk(T.root) if n.label == head]
        if len(hits) != 1:
            raise BindError(f"{path}: {head!r} has {len(hits)} matches on "
                            f"the tree; it must have one")
        cur = hits[0]
    for lab in rest:
        kids = [k for k in cur.kids if k.label == lab]
        if len(kids) != 1:
            raise BindError(f"{path}: {lab!r} under {cur.label!r} has "
                            f"{len(kids)} matches")
        cur = kids[0]
    return cur


def bind(T, at):
    """-> {node: Dated}. Raises on the first locator that does not resolve
    to exactly one node, because a silent miss is a date on the wrong man."""
    dated, errors = {}, []
    for path, d in BIND:
        try:
            n = locate(T, at, path)
        except BindError as e:
            errors.append(str(e))
            continue
        if n in dated:
            errors.append(f"{path}: {n.label!r} dated twice")
        dated[n] = d
    if errors:
        raise BindError("\n".join(errors))
    return dated


# ---------------------------------------------------------------------------
# Placing the undated
# ---------------------------------------------------------------------------

GEN_PRE = 100          # years per generation, extrapolating before the flood
GEN = 30               # … and after it
MIN_STEP = 8           # a child is never drawn less than this below a parent


def estimate(root, dated):
    """-> {node: year_am} for EVERY node.

    A dated node sits at its own year. An undated one sits between the
    nearest dated ancestor and the nearest dated descendant on its line,
    in proportion to the generations between; with no dated descendant it
    steps down from its parent by a generation. The masthead says so.
    """
    below = {}

    def down(n):
        best = None
        for k in n.kids:
            r = down(k)
            if k in dated:
                cand = (1, dated[k].t0)
            elif r:
                cand = (r[0] + 1, r[1])
            else:
                cand = None
            if cand and (best is None or cand[0] < best[0]):
                best = cand
        below[n] = best
        return best

    down(root)
    year = {}

    def top(n, anc_t, anc_d):
        if n in dated:
            t = dated[n].t0
            anc_t, anc_d = t, 0
        else:
            b = below[n]
            if b:
                t = anc_t + (b[1] - anc_t) * anc_d / (anc_d + b[0])
            else:
                t = anc_t + anc_d * (GEN_PRE if anc_t < FLOOD else GEN)
        # The tree's structure wins over the date for PLACEMENT: a son is
        # never drawn above his father, even where a dashed join is an
        # inference the date contradicts. The box still prints the true
        # year.
        if n.parent is not None:
            t = max(t, year[n.parent] + MIN_STEP)
        year[n] = t
        for k in n.kids:
            top(k, anc_t, anc_d + 1)

    top(root, dated[root].t0, 0)
    return year


# ---------------------------------------------------------------------------
# Audit
# ---------------------------------------------------------------------------

def audit(T, at, verbose=True):
    dated = bind(T, at)
    nodes = list(walk(T.root))
    bad = []
    for n, d in dated.items():
        p = n.parent
        while p is not None and p not in dated:
            p = p.parent
        if p is not None and dated[p].t0 > d.t0:
            bad.append(f"{p.label} ({bc(dated[p].t0)} BC) is dated after "
                       f"{n.label} ({bc(d.t0)} BC)")
    kinds = {}
    for d in dated.values():
        kinds[d.kind] = kinds.get(d.kind, 0) + 1
    people = sum(1 for n in nodes if n.kind != "house")
    if verbose:
        print(f"bound {len(dated)} dates onto {len(nodes)} nodes "
              f"({people} people): "
              + ", ".join(f"{v} {k}" for k, v in sorted(kinds.items())))
        print(f"coverage: {100 * len(dated) / people:.1f}% of people")
        for z0, z1, title, _ in ZONES:
            k = sum(1 for d in dated.values() if am(z0) <= d.t0 < am(z1))
            print(f"  {title:28s} {k:3d} dated")
        for line in bad:
            print("  placed by structure, not date:", line)
        print("flood AM", FLOOD, "=", bc(FLOOD), "BC;  Abraham born AM",
              ABRAHAM, "=", bc(ABRAHAM), "BC")
    return dated


if __name__ == "__main__":
    import matthew_tree
    T, at = matthew_tree.build()
    audit(T, at)
