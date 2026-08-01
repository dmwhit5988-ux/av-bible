"""Scene specs + verse-matching engine for the 1 Chronicles 1-9 genealogies.

The nine genealogy chapters are broken into titled family-tree SCENES (a
scene serves a contiguous verse range). Every verse's SVG shows its whole
scene: names already read are solid, names still ahead are dim, and the
current verse's names glow with a once-through reveal — the same visual
language as the Genesis 5 / Matthew 1 genealogies.

Highlights are NOT hand-authored per verse. Each scene's rows are matched
against the actual WEB verse text (word-boundary, longest-label-first, one
row per label per verse, author order = text order), so a row lights up in
the verse that reads it. The rare ambiguous cases (recycled priest names in
the 1 Chr 6 chain, two Gazez in one verse) are pinned with a scene-level
`explicit` map: {verse: ["Label", "Label#2", ...]} — "#k" picks the k-th
row bearing that label; an explicit entry replaces text-matching for that
verse.

Data mini-language (kept terse — there are ~1,100 rows):
    node   := "Name" | (label, note) | (label, [kids]) | (label, note, [kids])
    block  := T(node)      a tree (root + indented children)
            | C(node, ...) a chain (top-to-bottom descent, one generation
                           per row; children only on the last link)
    scene  := sc(title, lo, hi, [col1_blocks, col2_blocks, ...], ...)
A label starting with "~" is a heading row: italic, dim, no dot, never
text-matched (highlightable only via `explicit`).

Spellings are the WEB's; the family ships translation-generic files
(translation_suffixed: false in svg_generators.json) — hand-building
variant tables for ~700 names across eight translations isn't worth it.

Rendered by generate_1chronicles_svg.py.
"""

import json
import os
import re

BOOK = "1 Chronicles"
REPO = os.path.dirname(os.path.abspath(__file__))


def web_verses(chapter):
    path = os.path.join(REPO, "bibles", "WEB",
                        f"1_Chronicles_{chapter}.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)["verses"]


# ---------------------------------------------------------------------------
# Data mini-language
# ---------------------------------------------------------------------------

def T(root):
    return ("T", root)


def C(*nodes):
    return ("C", list(nodes))


def CT(*nodes):
    """A linear descent as a nested single-child TREE node (for chains that
    hang under a tree parent, where a C block can't attach). The last entry
    may carry children of its own."""
    out = None
    for n in reversed(nodes):
        label, note, kids = _node(n)
        kids = list(kids) + ([out] if out is not None else [])
        out = (label, note, kids) if note else (label, kids)
    return out


def sc(title, lo, hi, cols, explicit=None, foot=None):
    return dict(title=title, verses=(lo, hi), cols=cols,
                explicit=explicit or {}, foot=foot)


def _node(n):
    """Normalise a node shorthand -> (label, note, kids)."""
    if isinstance(n, str):
        return n, None, []
    if len(n) == 2:
        label, second = n
        if isinstance(second, list):
            return label, None, second
        return label, second, []
    return n[0], n[1], list(n[2])


class Row:
    __slots__ = ("label", "note", "depth", "col", "heading",
                 "parent", "chainprev", "index")

    def __init__(self, label, note, depth, col, parent, chainprev):
        self.label, self.note = label, note
        self.depth, self.col = depth, col
        self.heading = label.startswith("~")
        self.parent, self.chainprev = parent, chainprev
        self.index = None


def flatten(scene):
    """Scene -> ordered Row list (author order == expected text order)."""
    rows = []

    def add(row):
        row.index = len(rows)
        rows.append(row)
        return row.index

    def tree(node, depth, col, parent):
        label, note, kids = _node(node)
        i = add(Row(label, note, depth, col, parent, None))
        # children of a heading row indent under it but draw no connector
        # (the engine checks whether the parent row is a heading)
        for kid in kids:
            tree(kid, depth + 1, col, i)

    for ci, blocks in enumerate(scene["cols"]):
        for kind, payload in blocks:
            if kind == "T":
                tree(payload, 0, ci, None)
            else:                                   # chain
                prev = None
                for j, n in enumerate(payload):
                    label, note, kids = _node(n)
                    i = add(Row(label, note, 0, ci, None, prev))
                    if kids:
                        assert j == len(payload) - 1, \
                            f"chain children only on last link: {label}"
                        for kid in kids:
                            tree(kid, 1, ci, i)
                    prev = i
    return rows


# ---------------------------------------------------------------------------
# Verse matching
# ---------------------------------------------------------------------------

def _explicit_rows(rows, refs, title):
    """Resolve ["Label", "Label#2", ...] -> row indices."""
    out = []
    for ref in refs:
        label, _, k = ref.partition("#")
        k = int(k) if k else 1
        matches = [r.index for r in rows if r.label == label]
        if len(matches) < k:
            raise KeyError(f"{title}: explicit ref {ref!r} not found")
        out.append(matches[k - 1])
    return out


def assign(scene, verse_texts):
    """Match scene rows to verses.

    Returns (first_read, highlights):
      first_read: row index -> verse it is first read in (rows never matched
                  are context — drawn as already-read from the scene start)
      highlights: verse -> [row indices] to glow in that verse
    """
    rows = flatten(scene)
    lo, hi = scene["verses"]
    by_label = {}
    for r in rows:
        if not r.heading:
            by_label.setdefault(r.label, []).append(r.index)
    labels_desc = sorted(by_label, key=len, reverse=True)

    first_read, highlights = {}, {}
    for v in range(lo, hi + 1):
        if v in scene["explicit"]:
            hl = _explicit_rows(rows, scene["explicit"][v], scene["title"])
            for i in hl:
                first_read.setdefault(i, v)
            highlights[v] = hl
            continue
        text = verse_texts.get(v, "")
        hl = []
        for label in labels_desc:
            pat = re.compile(rf"\b{re.escape(label)}\b")
            if not pat.search(text):
                continue
            text = pat.sub("\x00" * len(label), text)
            unread = [i for i in by_label[label] if i not in first_read]
            if unread:                       # one new row per label per verse
                first_read[unread[0]] = v
                hl.append(unread[0])
            elif len(by_label[label]) == 1:  # unambiguous re-mention
                hl.append(by_label[label][0])
        highlights[v] = sorted(hl)
    return rows, first_read, highlights


def coverage_check(chapter, scenes):
    verses = [v for v, _ in web_verses(chapter)]
    covered = []
    for s in scenes:
        lo, hi = s["verses"]
        covered.extend(range(lo, hi + 1))
    assert sorted(covered) == verses, \
        f"ch{chapter}: scene ranges {sorted(covered)[:5]}... != verses"


# ---------------------------------------------------------------------------
# Chapter 1 — Adam to Edom
# ---------------------------------------------------------------------------

CH1 = [
    sc("From Adam to Noah", 1, 4, [
        [C("Adam", "Seth", "Enosh", "Kenan", "Mahalalel", "Jared", "Enoch",
           "Methuselah", "Lamech",
           ("Noah", None, ["Shem", "Ham", "Japheth"]))],
    ]),
    sc("The sons of Japheth", 5, 7, [
        [T(("Japheth", [
            ("Gomer", ["Ashkenaz", "Diphath", "Togarmah"]),
            "Magog", "Madai",
            ("Javan", ["Elishah", "Tarshish", "Kittim", "Rodanim"]),
            "Tubal", "Meshech", "Tiras"]))],
    ]),
    sc("The sons of Ham", 8, 16, [
        [T(("Ham", [
            ("Cush", ["Seba", "Havilah", "Sabta",
                      ("Raama", ["Sheba", "Dedan"]),
                      "Sabteca",
                      ("Nimrod", "a mighty one in the earth")]),
            ("Mizraim", ["Ludim", "Anamim", "Lehabim", "Naphtuhim",
                         "Pathrusim",
                         ("Casluhim", "whence the Philistines"),
                         "Caphtorim"]),
            "Put",
            ("Canaan", [("Sidon", "his firstborn"), "Heth",
                        "Jebusite", "Amorite", "Girgashite",
                        "Hivite", "Arkite", "Sinite",
                        "Arvadite", "Zemarite", "Hamathite"])]))],
    ]),
    sc("The sons of Shem", 17, 23, [
        [T(("Shem", ["Elam", "Asshur",
                     ("Arpachshad", [("Shelah", [("Eber", [
                         ("Peleg", "in his days the earth was divided"),
                         ("Joktan", ["Almodad", "Sheleph", "Hazarmaveth",
                                     "Jerah", "Hadoram", "Uzal", "Diklah",
                                     "Ebal", "Abimael", "Sheba", "Ophir",
                                     "Havilah", "Jobab"])])])]),
                     "Lud", "Aram", "Uz", "Hul", "Gether", "Meshech"]))],
    ]),
    sc("From Shem to Abraham", 24, 27, [
        [C("Shem", "Arpachshad", "Shelah", "Eber", "Peleg", "Reu",
           "Serug", "Nahor", "Terah",
           ("Abram", "also called Abraham"))],
    ]),
    sc("The sons of Abraham", 28, 34, [
        [T(("Abraham", [("Isaac", ["Esau", "Israel"]),
                        ("Ishmael", [("Nebaioth", "the firstborn"),
                                     "Kedar", "Adbeel", "Mibsam", "Mishma",
                                     "Dumah", "Massa", "Hadad", "Tema",
                                     "Jetur", "Naphish", "Kedemah"])]))],
        [T(("Keturah", "Abraham’s concubine", [
            "Zimran",
            ("Jokshan", ["Sheba", "Dedan"]),
            "Medan",
            ("Midian", ["Ephah", "Epher", "Hanoch", "Abida", "Eldaah"]),
            "Ishbak", "Shuah"]))],
    ]),
    sc("The sons of Esau", 35, 37, [
        [T(("Esau", [
            ("Eliphaz", ["Teman", "Omar", "Zephi", "Gatam", "Kenaz",
                         "Timna", "Amalek"]),
            ("Reuel", ["Nahath", "Zerah", "Shammah", "Mizzah"]),
            "Jeush", "Jalam", "Korah"]))],
    ]),
    sc("The sons of Seir", 38, 42, [
        [T(("Seir", [
            ("Lotan", ["Hori", "Homam", ("Timna", "Lotan’s sister")]),
            ("Shobal", ["Alian", "Manahath", "Ebal", "Shephi", "Onam"]),
            ("Zibeon", ["Aiah",
                        ("Anah", [("Dishon", ["Hamran", "Eshban",
                                              "Ithran", "Cheran"])])]),
            "Anah", "Dishon",
            ("Ezer", ["Bilhan", "Zaavan", "Jaakan"]),
            ("Dishan", ["Uz", "Aran"])]))],
    ], explicit={
        38: ["Seir", "Lotan", "Shobal", "Zibeon", "Anah#2", "Dishon#2",
             "Ezer", "Dishan"],
    }),
    sc("The kings of Edom", 43, 50, [
        [T(("~kings in Edom before any king reigned over Israel:", [])),
         C(("Bela", "son of Beor · his city: Dinhabah"),
           ("Jobab", "son of Zerah of Bozrah"),
           ("Husham", "of the land of the Temanites"),
           ("Hadad", "son of Bedad, who struck Midian in Moab · Avith"),
           ("Samlah", "of Masrekah"),
           ("Shaul", "of Rehoboth by the River"),
           ("Baal Hanan", "son of Achbor"),
           ("Hadad", "his city: Pai", [
               ("Mehetabel", "his wife, daughter of Matred")]))],
    ], foot="each king reigned in the place of the one before"),
    sc("The chiefs of Edom", 51, 54, [
        [T(("~after Hadad died —", [])),
         T(("~the chiefs of Edom:", [
             "Timna", "Aliah", "Jetheth", "Oholibamah", "Elah", "Pinon"]))],
        [T(("~", [
            "Kenaz", "Teman", "Mibzar", "Magdiel", "Iram"]))],
    ], foot="eleven chiefs — the text lists them in order"),
]

# ---------------------------------------------------------------------------
# Chapter 2 — Israel to the families of Judah
# ---------------------------------------------------------------------------

CH2 = [
    sc("The sons of Israel", 1, 2, [
        [T(("Israel", ["Reuben", "Simeon", "Levi", "Judah", "Issachar",
                       "Zebulun", "Dan", "Joseph", "Benjamin", "Naphtali",
                       "Gad", "Asher"]))],
    ]),
    sc("The sons of Judah", 3, 8, [
        [T(("Judah", [("Er", "the firstborn — wicked in Yahweh’s sight"),
                      "Onan",
                      ("Shelah", "these three by Shua’s daughter"),
                      ("Tamar", "his daughter-in-law bore him:", [
                          ("Perez", ["Hezron", "Hamul"]),
                          ("Zerah", ["Zimri",
                                     ("Ethan", ["Azariah"]),
                                     "Heman", "Calcol", "Dara"])])]))],
        [T(("Carmi", [("Achar", "the troubler of Israel")]))],
    ]),
    sc("From Hezron to David", 9, 17, [
        [T(("Hezron", [
            "Jerahmeel",
            CT("Ram", "Amminadab",
               ("Nahshon", "prince of the children of Judah"),
               "Salma", "Boaz", "Obed",
               ("Jesse", [("Eliab", "the firstborn"),
                          ("Abinadab", "the second"),
                          ("Shimea", "the third"),
                          ("Nethanel", "the fourth"),
                          ("Raddai", "the fifth"),
                          ("Ozem", "the sixth"),
                          ("David", "the seventh")])),
            "Chelubai"]))],
        [T(("~their sisters:", [])),
         T(("Zeruiah", ["Abishai", "Joab", "Asahel"])),
         T(("Abigail", [("Amasa", "by Jether the Ishmaelite")]))],
    ]),
    sc("Caleb and Hezron's later line", 18, 24, [
        [T(("Caleb", "son of Hezron", [
            ("Azubah", "his wife", ["Jesher", "Shobab", "Ardon"]),
            "Jerioth",
            ("Ephrath", "married after Azubah died", ["Hur"])]))],
        [C("Hur", "Uri", "Bezalel"),
         T(("~Hezron, at sixty, married the daughter of", [])),
         C(("Machir", "the father of Gilead"),
           ("Segub", "her son by Hezron"),
           ("Jair", "who had twenty-three cities in Gilead"))],
        [T(("~Geshur and Aram took Jair’s towns — sixty cities", [])),
         T(("~after Hezron died in Caleb Ephrathah:", [])),
         T(("Abijah", "Hezron’s wife", [
             ("Ashhur", "the father of Tekoa")]))],
    ]),
    sc("The sons of Jerahmeel", 25, 33, [
        [T(("Jerahmeel", "the firstborn of Hezron", [
            ("Ram", "the firstborn", ["Maaz", "Jamin", "Eker"]),
            "Bunah", "Oren", "Ozem", "Ahijah",
            ("Atarah", "another wife", [
                ("Onam", "her son", [
                    ("Shammai", [
                        ("Nadab", [("Seled", "died without children"),
                                   CT("Appaim", "Ishi", "Sheshan",
                                      "Ahlai")]),
                        ("Abishur", [("Abihail", "his wife"),
                                     "Ahban", "Molid"])]),
                    ("Jada", [("Jether", "died without children"),
                              ("Jonathan", ["Peleth", "Zaza"])])])])]))],
    ], foot="these were the sons of Jerahmeel (v. 33)"),
    sc("The line of Sheshan", 34, 41, [
        [T(("Sheshan", "had no sons, but daughters", [
            ("Jarha", "his Egyptian servant — Sheshan gave him "
                      "his daughter", [("Attai", "her son")])]))],
        [C("Attai", "Nathan", "Zabad", "Ephlal", "Obed", "Jehu",
           "Azariah", "Helez", "Eleasah", "Sismai", "Shallum",
           "Jekamiah", "Elishama")],
    ]),
    sc("The descendants of Caleb", 42, 49, [
        [T(("Caleb", "the brother of Jerahmeel", [
            ("Mesha", "his firstborn, the father of Ziph"),
            ("Mareshah", "the father of Hebron")])),
         T(("Hebron", ["Korah", "Tappuah", "Rekem", "Shema"])),
         C("Shema", ("Raham", "the father of Jorkeam"))],
        [C("Rekem", "Shammai", "Maon", ("Beth Zur", "he was its father")),
         T(("Ephah", "Caleb’s concubine", [
             "Haran", "Moza", "Gazez",
             ("~and Haran became the father of", ["Gazez"])]))],
        [T(("Jahdai", ["Regem", "Jothan", "Geshan", "Pelet", "Ephah",
                       "Shaaph"])),
         T(("Maacah", "Caleb’s concubine", [
             "Sheber", "Tirhanah",
             ("Shaaph", "the father of Madmannah"),
             ("Sheva", "father of Machbena and Gibea")])),
         T(("Achsah", "Caleb’s daughter"))],
    ], explicit={
        46: ["Ephah", "Haran", "Moza", "Gazez", "Gazez#2"],
        49: ["Shaaph#2", "Sheva", "Achsah"],
    }),
    sc("The sons of Hur", 50, 55, [
        [T(("~the sons of Caleb, the son of Hur,", [])),
         T(("~the firstborn of Ephrathah:", [])),
         T(("Hur", [("Shobal", "father of Kiriath Jearim"),
                    ("Salma", "father of Bethlehem"),
                    ("Hareph", "father of Beth Gader")]))],
        [T(("Shobal", [("Haroeh", "half of the Menuhoth"),
                       ("~the families of Kiriath Jearim:", [
                           "Ithrites", "Puthites", "Shumathites",
                           "Mishraites",
                           ("~from them came", [
                               "Zorathites", "Eshtaolites"])])]))],
        [T(("Salma", ["Bethlehem", "Netophathites", "Atroth Beth Joab",
                      ("Manahathites", "half of them"), "Zorites"])),
         T(("~the scribes who lived at Jabez:", [
             "Tirathites", "Shimeathites", "Sucathites",
             ("Kenites", "from Hammath, of the house of Rechab")]))],
    ], explicit={
        51: ["Salma", "Hareph"],
    }),
]

# ---------------------------------------------------------------------------
# Chapter 3 — the house of David
# ---------------------------------------------------------------------------

CH3 = [
    sc("The sons of David", 1, 9, [
        [T(("David", [("~born to him in Hebron:", [
            ("Amnon", "the firstborn, of Ahinoam"),
            ("Daniel", "the second, of Abigail"),
            ("Absalom", "the third, of Maacah"),
            ("Adonijah", "the fourth, of Haggith"),
            ("Shephatiah", "the fifth, of Abital"),
            ("Ithream", "the sixth, by Eglah his wife")])]))],
        [T(("~born to him in Jerusalem:", [
            "Shimea", "Shobab", "Nathan",
            ("Solomon", "four of Bathshua"),
            "Ibhar", "Elishama", "Eliphelet", "Nogah", "Nepheg",
            "Japhia", "Elishama", "Eliada",
            ("Eliphelet", "nine in all")]))],
        [T(("~seven years and six months in Hebron,", [])),
         T(("~thirty-three years in Jerusalem", [])),
         T(("Tamar", "their sister")),
         T(("~besides the sons of the concubines", []))],
    ], explicit={
        4: ["~seven years and six months in Hebron,",
            "~thirty-three years in Jerusalem"],
    }),
    sc("The kings of Judah", 10, 16, [
        [C("Solomon", "Rehoboam", "Abijah", "Asa", "Jehoshaphat",
           "Joram", "Ahaziah", "Joash", "Amaziah", "Azariah", "Jotham",
           "Ahaz", "Hezekiah", "Manasseh", "Amon",
           ("Josiah", None, [
               ("Johanan", "the firstborn"),
               ("Jehoiakim", "the second", [("Jeconiah", "his son"),
                                            ("Zedekiah", "his son")]),
               ("Zedekiah", "the third"),
               ("Shallum", "the fourth")]))],
    ], explicit={
        15: ["Josiah", "Johanan", "Jehoiakim", "Zedekiah#2", "Shallum"],
        16: ["Jehoiakim", "Jeconiah", "Zedekiah#1"],
    }, foot="son succeeding father, Solomon to the exile"),
    sc("The line after the exile", 17, 21, [
        [T(("Jeconiah", "the captive", [
            "Shealtiel", "Malchiram",
            ("Pedaiah", [
                ("Zerubbabel", ["Meshullam", "Hananiah",
                                ("Shelomith", "their sister"),
                                "Hashubah", "Ohel", "Berechiah",
                                "Hasadiah", ("Jushab Hesed", "five")]),
                "Shimei"]),
            "Shenazzar", "Jekamiah", "Hoshama", "Nedabiah"]))],
        [T(("Hananiah", ["Pelatiah", "Jeshaiah"])),
         T(("~and the sons of, in descent:", [])),
         C("Rephaiah", "Arnan", "Obadiah", "Shecaniah")],
    ]),
    sc("The last generations recorded", 22, 24, [
        [C("Shecaniah",
           ("Shemaiah", None, ["Hattush", "Igal", "Bariah", "Neariah",
                               ("Shaphat", "six")]))],
        [T(("Neariah", ["Elioenai", "Hizkiah", ("Azrikam", "three")]))],
        [T(("Elioenai", ["Hodaviah", "Eliashib", "Pelaiah", "Akkub",
                         "Johanan", "Delaiah", ("Anani", "seven")]))],
    ]),
]

# ---------------------------------------------------------------------------
# Chapter 4 — Judah's other families; Simeon
# ---------------------------------------------------------------------------

CH4 = [
    sc("Families of Judah", 1, 8, [
        [T(("Judah", ["Perez", "Hezron", "Carmi", "Hur",
                      ("Shobal", [
                          ("Reaiah", [
                              ("Jahath", [
                                  "Ahumai",
                                  ("Lahad", "the families of the "
                                            "Zorathites")])])])]))],
        [T(("Etam", "the sons of his father:", [
            "Jezreel", "Ishma", "Idbash",
            ("Hazzelelponi", "their sister")])),
         T(("~the sons of Hur, the firstborn of Ephrathah:", [])),
         T(("Penuel", [("Gedor", "he was its father")])),
         T(("Ezer", [("Hushah", "he was its father")]))],
        [T(("Ashhur", "the father of Tekoa — two wives:", [
            ("Naarah", ["Ahuzzam", "Hepher", "Temeni", "Haahashtari"]),
            ("Helah", ["Zereth", "Izhar", "Ethnan"])])),
         T(("Hakkoz", ["Anub", "Zobebah",
                       ("Aharhel", "the son of Harum")]))],
    ]),
    sc("The prayer of Jabez", 9, 10, [
        [T(("Jabez", "more honorable than his brothers — his mother "
                     "said, “I bore him with sorrow”")),
         T(("~he called on the God of Israel:", [])),
         T(("~“Oh that you would bless me indeed,", [])),
         T(("~and enlarge my border!", [])),
         T(("~May your hand be with me, and may you", [])),
         T(("~keep me from evil, that I may not cause pain!”", [])),
         T(("~— and God granted him that which he requested", []))],
    ], explicit={
        9: ["Jabez"],
        10: ["~he called on the God of Israel:",
             "~“Oh that you would bless me indeed,",
             "~and enlarge my border!",
             "~May your hand be with me, and may you",
             "~keep me from evil, that I may not cause pain!”",
             "~— and God granted him that which he requested"],
    }),
    sc("Kenaz and Caleb's families", 11, 15, [
        [C(("Chelub", "the brother of Shuhah"),
           "Mehir",
           ("Eshton", None, [
               "Beth Rapha", "Paseah",
               ("Tehinnah", "the father of Ir Nahash")])),
         T(("~these are the men of Recah", []))],
        [T(("Kenaz", ["Othniel", "Seraiah"])),
         T(("Othniel", ["Hathath",
                        ("Meonothai", ["Ophrah"])])),
         T(("Seraiah", [("Joab", "father of Ge Harashim")]))],
        [T(("Caleb", "the son of Jephunneh", [
            "Iru", ("Elah", ["Kenaz"]), "Naam"]))],
    ], explicit={
        13: ["Kenaz", "Othniel", "Seraiah", "Othniel#2", "Hathath"],
    }),
    sc("More families of Judah", 16, 20, [
        [T(("Jehallelel", ["Ziph", "Ziphah", "Tiria", "Asarel"])),
         T(("Ezrah", ["Jether", "Mered", "Epher", "Jalon"]))],
        [T(("Mered", "married Pharaoh’s daughter:", [
            ("Bithiah", ["Miriam", "Shammai",
                         ("Ishbah", "father of Eshtemoa")]),
            ("~and his Jewish wife bore:", [
                ("Jered", "father of Gedor"),
                ("Heber", "father of Soco"),
                ("Jekuthiel", "father of Zanoah")])]))],
        [T(("~the sons of the wife of Hodiah,", [])),
         T(("~the sister of Naham:", [
             ("Keilah", "the Garmite — his father"),
             ("Eshtemoa", "the Maacathite")])),
         T(("Shimon", ["Amnon", "Rinnah", "Ben Hanan", "Tilon"])),
         T(("Ishi", ["Zoheth", "Ben Zoheth"]))],
    ]),
    sc("The sons of Shelah", 21, 23, [
        [T(("Shelah", "the son of Judah", [
            ("Er", "the father of Lecah"),
            ("Laadah", "the father of Mareshah"),
            ("~and the families of the linen workers", []),
            ("~of the house of Ashbea", []),
            "Jokim",
            ("~and the men of Cozeba", []),
            "Joash",
            ("Saraph", "who had dominion in Moab"),
            "Jashubilehem"]))],
        [T(("~(these records are ancient)", [])),
         T(("~they were the potters, and lived at", [])),
         T(("~Netaim and Gederah, with the king for his work", []))],
    ], explicit={
        23: ["~they were the potters, and lived at",
             "~Netaim and Gederah, with the king for his work"],
    }),
    sc("The sons of Simeon", 24, 27, [
        [T(("Simeon", ["Nemuel", "Jamin", "Jarib", "Zerah",
                       CT("Shaul", "Shallum", "Mibsam", "Mishma",
                          "Hammuel", "Zaccur",
                          ("Shimei", "sixteen sons, six daughters"))]))],
    ]),
    sc("Where Simeon settled", 28, 33, [
        [T(("~their cities until David’s reign:", [
            "Beersheba", "Moladah", "Hazarshual", "Bilhah", "Ezem",
            "Tolad", "Bethuel", "Hormah", "Ziklag"]))],
        [T(("~", ["Beth Marcaboth", "Hazar Susim", "Beth Biri",
                  "Shaaraim"])),
         T(("~their villages — five cities:", [
             "Etam", "Ain", "Rimmon", "Tochen", "Ashan"])),
         T(("~and all the villages around them, to Baal", []))],
    ], explicit={
        33: ["~and all the villages around them, to Baal"],
    }),
    sc("The princes of Simeon", 34, 43, [
        [T(("~princes in their families:", [
            "Meshobab", "Jamlech",
            ("Joshah", "the son of Amaziah"),
            "Joel",
            ("Jehu", "son of Joshibiah, son of Seraiah"),
            "Elioenai", "Jaakobah", "Jeshohaiah", "Asaiah", "Adiel",
            "Jesimiel", "Benaiah"]))],
        [T(("~and Ziza — his line, each the son of the next:", [])),
         C("Ziza", "Shiphi", "Allon", "Jedaiah", "Shimri", "Shemaiah"),
         T(("~their fathers’ houses increased greatly", []))],
        [T(("~they went to Gedor to seek pasture,", [])),
         T(("~and struck the Meunim in Hezekiah’s days", [])),
         T(("Ishi", "his sons led five hundred to Mount Seir:", [
             "Pelatiah", "Neariah", "Rephaiah", "Uzziel"])),
         T(("~they struck the remnant of the Amalekites,", [])),
         T(("~and have lived there to this day", []))],
    ], explicit={
        38: ["~their fathers’ houses increased greatly"],
        39: ["~they went to Gedor to seek pasture,"],
        40: ["~they went to Gedor to seek pasture,"],
        41: ["~and struck the Meunim in Hezekiah’s days"],
        43: ["~they struck the remnant of the Amalekites,",
             "~and have lived there to this day"],
    }),
]

# ---------------------------------------------------------------------------
# Chapter 5 — Reuben, Gad, half-Manasseh
# ---------------------------------------------------------------------------

CH5 = [
    sc("Reuben, the firstborn", 1, 10, [
        [T(("~Reuben was the firstborn, but he defiled", [])),
         T(("~his father’s couch — his birthright went to", [])),
         T(("~the sons of Joseph; from Judah came the prince", [])),
         T(("Reuben", ["Hanoch", "Pallu", "Hezron", "Carmi"]))],
        [C("Joel", "Shemaiah", "Gog", "Shimei", "Micah", "Reaiah", "Baal",
           ("Beerah", "prince of the Reubenites, exiled"))],
        [T(("~his brothers by their families:", [
            ("Jeiel", "the chief"), "Zechariah",
            ("Bela", "son of Azaz, son of Shema")])),
         T(("~they lived in Aroer, to Nebo and Baal Meon,", [])),
         T(("~eastward toward the Euphrates — and in Saul’s", [])),
         T(("~days they defeated the Hagrites in their tents", []))],
    ], explicit={
        1: ["~Reuben was the firstborn, but he defiled",
            "~his father’s couch — his birthright went to"],
        2: ["~the sons of Joseph; from Judah came the prince"],
        9: ["~eastward toward the Euphrates — and in Saul’s"],
        10: ["~days they defeated the Hagrites in their tents"],
    }),
    sc("The sons of Gad", 11, 17, [
        [T(("Gad", "over against them, in Bashan to Salecah:", [
            ("Joel", "the chief"),
            ("Shapham", "the second"),
            "Janai",
            ("Shaphat", "in Bashan")]))],
        [T(("~their brothers, of their fathers’ houses:", [
            "Michael", "Meshullam", "Sheba", "Jorai", "Jacan", "Zia",
            ("Eber", "seven")]))],
        [T(("~the sons of Abihail — his line:", [])),
         C("Abihail", "Huri", "Jaroah", "Gilead", "Michael",
           "Jeshishai", "Jahdo", "Buz"),
         T(("Ahi", "son of Abdiel, son of Guni")),
         T(("~listed in the days of Jotham of Judah", [])),
         T(("~and Jeroboam of Israel", []))],
    ], explicit={
        16: ["~listed in the days of Jotham of Judah"],
        17: ["~listed in the days of Jotham of Judah",
             "~and Jeroboam of Israel"],
    }),
    sc("The war with the Hagrites", 18, 22, [
        [T(("~Reuben, Gad, and half-Manasseh:", [])),
         T(("44,760 men", "able for war, skillful with bow and sword")),
         T(("~they made war with the Hagrites —", [
             "Jetur", "Naphish", "Nodab"]))],
        [T(("~they cried to God in the battle, and he", [])),
         T(("~answered, because they trusted in him", [])),
         T(("~they took away:", [
             ("50,000", "camels"),
             ("250,000", "sheep"),
             ("2,000", "donkeys"),
             ("100,000", "men")])),
         T(("~many fell slain, for the war was of God;", [])),
         T(("~they lived there until the captivity", []))],
    ], explicit={
        18: ["~Reuben, Gad, and half-Manasseh:", "44,760 men"],
        20: ["~they cried to God in the battle, and he",
             "~answered, because they trusted in him"],
        21: ["50,000", "250,000", "2,000", "100,000"],
        22: ["~many fell slain, for the war was of God;",
             "~they lived there until the captivity"],
    }),
    sc("The half-tribe of Manasseh", 23, 26, [
        [T(("~they increased from Bashan to Baal Hermon,", [])),
         T(("~Senir, and Mount Hermon", [])),
         T(("~the heads of their fathers’ houses:", [
             "Epher", "Ishi", "Eliel", "Azriel", "Jeremiah",
             "Hodaviah",
             ("Jahdiel", "mighty men of valor, famous men")]))],
        [T(("~but they played the prostitute after the gods", [])),
         T(("~of the peoples of the land — so God stirred up", [])),
         T(("Pul", "king of Assyria")),
         T(("Tilgath Pilneser", "king of Assyria — who carried them away:")),
         T(("~Reuben, Gad, and half-Manasseh, to", [
             "Halah", "Habor", "Hara",
             ("Gozan", "the river of — to this day")]))],
    ], explicit={
        23: ["~they increased from Bashan to Baal Hermon,",
             "~Senir, and Mount Hermon"],
        25: ["~but they played the prostitute after the gods",
             "~of the peoples of the land — so God stirred up"],
    }),
]

# ---------------------------------------------------------------------------
# Chapter 6 — Levi: priests, singers, cities
# ---------------------------------------------------------------------------

CH6 = [
    sc("The line of the high priests", 1, 15, [
        [T(("Levi", ["Gershon", "Kohath", "Merari"])),
         T(("Kohath", ["Amram", "Izhar", "Hebron", "Uzziel"])),
         T(("Amram", ["Aaron", "Moses", "Miriam"]))],
        [T(("Aaron", ["Nadab", "Abihu",
                      CT("Eleazar", "Phinehas", "Abishua", "Bukki", "Uzzi",
                         "Zerahiah", "Meraioth", "Amariah", "Ahitub",
                         "Zadok", "Ahimaaz", "Azariah", "Johanan",
                         ("Azariah", "priest in Solomon’s temple"),
                         "Amariah", "Ahitub", "Zadok", "Shallum",
                         "Hilkiah", "Azariah", "Seraiah",
                         ("Jehozadak", "went into captivity")),
                      "Ithamar"]))],
    ], explicit={
        3: ["Amram#2", "Aaron", "Moses", "Miriam", "Aaron#2",
            "Nadab", "Abihu", "Eleazar", "Ithamar"],
        8: ["Ahitub#1", "Zadok#1", "Ahimaaz"],
        11: ["Azariah#2", "Amariah#2", "Ahitub#2"],
        12: ["Ahitub#2", "Zadok#2", "Shallum"],
    }),
    sc("The families of Levi", 16, 19, [
        [T(("Levi", ["Gershom", "Kohath", "Merari"]))],
        [T(("Gershom", ["Libni", "Shimei"])),
         T(("Kohath", ["Amram", "Izhar", "Hebron", "Uzziel"]))],
        [T(("Merari", ["Mahli", "Mushi"])),
         T(("~the families of the Levites,", [])),
         T(("~according to their fathers’ households", []))],
    ], explicit={
        19: ["Merari#2", "Mahli", "Mushi",
             "~the families of the Levites,",
             "~according to their fathers’ households"],
    }),
    sc("The Levite lines", 20, 30, [
        [T(("~of Gershom:", [])),
         C("Gershom", "Libni", "Jahath", "Zimmah", "Joah", "Iddo",
           "Zerah", "Jeatherai")],
        [T(("~of Kohath:", [])),
         C("Kohath", "Amminadab", "Korah", "Assir", "Elkanah",
           "Ebiasaph", "Assir", "Tahath", "Uriel", "Uzziah", "Shaul"),
         T(("Elkanah", ["Amasai", "Ahimoth"]))],
        [C("Elkanah", "Zophai", "Nahath", "Eliab", "Jeroham", "Elkanah"),
         T(("Samuel", [("Joel", "the firstborn"),
                       ("Abijah", "the second")])),
         T(("~of Merari:", [])),
         C("Merari", "Mahli", "Libni", "Shimei", "Uzzah", "Shimea",
           "Haggiah", "Asaiah")],
    ]),
    sc("The temple singers", 31, 48, [
        [T(("~David set them over the song in Yahweh’s", [])),
         T(("~house, after the ark came to rest there", [])),
         T(("Heman", "the singer, a Kohathite — his line:")),
         C("Joel", "Samuel", "Elkanah", "Jeroham", "Eliel", "Toah",
           "Zuph", "Elkanah", "Mahath", "Amasai", "Elkanah", "Joel",
           "Azariah", "Zephaniah", "Tahath", "Assir", "Ebiasaph",
           "Korah", "Izhar", "Kohath", "Levi", "Israel")],
        [T(("Asaph", "his brother, at his right hand — his line:")),
         C("Berechiah", "Shimea", "Michael", "Baaseiah", "Malchijah",
           "Ethni", "Zerah", "Adaiah", "Ethan", "Zimmah", "Shimei",
           "Jahath", "Gershom", "Levi")],
        [T(("Ethan", "of Merari, on the left hand — his line:")),
         C("Kishi", "Abdi", "Malluch", "Hashabiah", "Amaziah",
           "Hilkiah", "Amzi", "Bani", "Shemer", "Mahli", "Mushi",
           "Merari", "Levi"),
         T(("~their brothers the Levites were appointed", [])),
         T(("~for all the service of God’s tabernacle", []))],
    ], explicit={
        31: ["~David set them over the song in Yahweh’s",
             "~house, after the ark came to rest there"],
        32: ["~David set them over the song in Yahweh’s",
             "~house, after the ark came to rest there"],
        44: ["Ethan#2", "Kishi", "Abdi", "Malluch"],
        48: ["~their brothers the Levites were appointed",
             "~for all the service of God’s tabernacle"],
    }, foot="each line reads downward: the son of, the son of …"),
    sc("The sons of Aaron and their charge", 49, 53, [
        [T(("~Aaron and his sons offered on the altar of", [])),
         T(("~burnt offering and the altar of incense,", [])),
         T(("~making atonement for Israel, according to", [])),
         T(("~all that Moses the servant of God commanded", []))],
        [T(("~the sons of Aaron, in descent:", [])),
         C("Aaron", "Eleazar", "Phinehas", "Abishua", "Bukki", "Uzzi",
           "Zerahiah", "Meraioth", "Amariah", "Ahitub", "Zadok",
           "Ahimaaz")],
    ], explicit={
        49: ["~Aaron and his sons offered on the altar of",
             "~burnt offering and the altar of incense,",
             "~making atonement for Israel, according to",
             "~all that Moses the servant of God commanded"],
        50: ["Aaron", "Eleazar", "Phinehas", "Abishua"],
    }),
    sc("Cities of the sons of Aaron", 54, 60, [
        [T(("~their dwelling places — theirs was the first lot:", [])),
         T(("Hebron", "in Judah — the fields went to Caleb")),
         T(("~cities of refuge and cities with suburbs:", [
             "Libnah", "Jattir", "Eshtemoa", "Hilen", "Debir",
             "Ashan", "Beth Shemesh"]))],
        [T(("~and out of the tribe of Benjamin:", [
            "Geba", "Allemeth", "Anathoth"])),
         T(("~thirteen cities in all,", [])),
         T(("~throughout their families", []))],
    ], explicit={
        54: ["~their dwelling places — theirs was the first lot:"],
        56: ["Hebron"],
        60: ["Geba", "Allemeth", "Anathoth", "~thirteen cities in all,",
             "~throughout their families"],
    }),
    sc("Cities allotted to the Levites", 61, 65, [
        [T(("~to the rest of the sons of Kohath, by lot:", [])),
         T(("ten cities", "out of the half-tribe of Manasseh")),
         T(("~to the sons of Gershom, by families:", [])),
         T(("thirteen cities", "from Issachar, Asher, Naphtali, Manasseh"))],
        [T(("~to the sons of Merari, by lot:", [])),
         T(("twelve cities", "out of Reuben, Gad, and Zebulun")),
         T(("~Israel gave the Levites these cities with", [])),
         T(("~their suburbs — by lot out of Judah,", [])),
         T(("~Simeon, and Benjamin", []))],
    ], explicit={
        61: ["~to the rest of the sons of Kohath, by lot:", "ten cities"],
        62: ["~to the sons of Gershom, by families:", "thirteen cities"],
        63: ["~to the sons of Merari, by lot:", "twelve cities"],
        64: ["~Israel gave the Levites these cities with",
             "~their suburbs — by lot out of Judah,"],
        65: ["~Simeon, and Benjamin"],
    }),
    sc("Kohath's cities in Ephraim", 66, 70, [
        [T(("~some Kohathite families had cities", [])),
         T(("~out of the tribe of Ephraim:", [])),
         T(("Shechem", "the city of refuge, in the hill country "
                       "of Ephraim")),
         T(("~with their suburbs:", [
             "Gezer", "Jokmeam", "Beth Horon"]))],
        [T(("~", ["Aijalon", "Gath Rimmon"])),
         T(("~and out of the half-tribe of Manasseh:", [
             "Aner", "Bileam"])),
         T(("~for the rest of the family of Kohath", []))],
    ], explicit={
        66: ["~some Kohathite families had cities",
             "~out of the tribe of Ephraim:"],
    }),
    sc("Gershom's cities", 71, 76, [
        [T(("~to the sons of Gershom —", [])),
         T(("~from the half-tribe of Manasseh:", [
             ("Golan", "in Bashan"), "Ashtaroth"])),
         T(("~from Issachar:", [
             "Kedesh", "Daberath", "Ramoth", "Anem"]))],
        [T(("~from Asher:", [
            "Mashal", "Abdon", "Hukok", "Rehob"])),
         T(("~from Naphtali:", [
             ("Kedesh", "in Galilee"), "Hammon", "Kiriathaim"]))],
    ], foot="every city with its suburbs"),
    sc("Merari's cities", 77, 81, [
        [T(("~to the rest of the Levites, the sons of Merari —", [])),
         T(("~from Zebulun:", ["Rimmono", "Tabor"])),
         T(("~from Reuben, beyond the Jordan at Jericho:", [
             ("Bezer", "in the wilderness"), "Jahzah",
             "Kedemoth", "Mephaath"]))],
        [T(("~from Gad:", [
            ("Ramoth", "in Gilead"), "Mahanaim", "Heshbon", "Jazer"]))],
    ], foot="every city with its suburbs"),
]

# ---------------------------------------------------------------------------
# Chapter 7 — Issachar, Benjamin, Naphtali, Manasseh, Ephraim, Asher
# ---------------------------------------------------------------------------

CH7 = [
    sc("The sons of Issachar", 1, 5, [
        [T(("Issachar", ["Tola", "Puah", "Jashub",
                         ("Shimron", "four")]))],
        [T(("Tola", ["Uzzi", "Rephaiah", "Jeriel", "Jahmai", "Ibsam",
                     ("Shemuel", "22,600 in David’s days")]))],
        [T(("Uzzi", ["Izrahiah"])),
         T(("Izrahiah", ["Michael", "Obadiah", "Joel",
                         ("Isshiah", "five; all of them chief men")])),
         T(("~bands of the army for war: 36,000", [])),
         T(("~all their families: 87,000 mighty men", []))],
    ], explicit={
        3: ["Uzzi#2", "Izrahiah", "Izrahiah#2", "Michael", "Obadiah",
            "Joel", "Isshiah"],
        4: ["~bands of the army for war: 36,000"],
        5: ["~all their families: 87,000 mighty men"],
    }),
    sc("The sons of Benjamin", 6, 12, [
        [T(("Benjamin", [
            ("Bela", ["Ezbon", "Uzzi", "Uzziel", "Jerimoth",
                      ("Iri", "22,034 mighty men")]),
            ("Becher", ["Zemirah", "Joash", "Eliezer", "Elioenai",
                        "Omri", "Jeremoth", "Abijah", "Anathoth",
                        ("Alemeth", "20,200 listed")]),
            ("Jediael", [
                ("Bilhan", ["Jeush", "Benjamin", "Ehud", "Chenaanah",
                            "Zethan", "Tarshish",
                            ("Ahishahar", "17,200 for war")])])]))],
        [T(("~also:", [("Shuppim", "and"), "Huppim",
                       ("Ir", "their sons —"),
                       ("Hushim", "the sons of Aher")]))],
    ], explicit={
        9: ["Becher", "Alemeth"],
        11: ["Jediael", "Ahishahar"],
    }),
    sc("The sons of Naphtali", 13, 13, [
        [T(("Naphtali", ["Jahziel", "Guni", "Jezer",
                         ("Shallum", "the sons of Bilhah")]))],
    ]),
    sc("The sons of Manasseh", 14, 19, [
        [T(("Manasseh", [
            ("Asriel", "whom his Aramitess concubine bore"),
            ("Machir", "the father of Gilead")])),
         T(("Machir", "took a wife of Huppim and Shuppim", [
             ("Maacah", "his wife"),
             ("Zelophehad", "the second — had daughters")]))],
        [T(("Maacah", "bore a son:", [
            "Peresh",
            ("Sheresh", "his brother", ["Ulam", "Rakem"])])),
         C("Ulam", "Bedan"),
         T(("~these were the sons of Gilead,", [])),
         T(("~the son of Machir, the son of Manasseh", []))],
        [T(("Hammolecheth", "his sister", [
            "Ishhod", "Abiezer", "Mahlah"])),
         T(("Shemida", ["Ahian", "Shechem", "Likhi", "Aniam"]))],
    ], explicit={
        17: ["Ulam#2", "Bedan", "~these were the sons of Gilead,",
             "~the son of Machir, the son of Manasseh"],
    }),
    sc("The sons of Ephraim", 20, 29, [
        [T(("~the sons of Ephraim, in descent:", [])),
         C("Ephraim", "Shuthelah", "Bered", "Tahath", "Eleadah",
           "Tahath", "Zabad", "Shuthelah"),
         T(("~also his sons Ezer and Elead, killed by the", [])),
         T(("~men of Gath when they came for the livestock;", [])),
         T(("~Ephraim their father mourned many days", []))],
        [T(("Beriah", "“there was trouble with his house”")),
         T(("Sheerah", "his daughter — built the Beth Horons")),
         T(("~then in descent:", [])),
         C("Rephah", "Resheph", "Telah", "Tahan", "Ladan", "Ammihud",
           "Elishama", "Nun", "Joshua")],
        [T(("~their possessions and settlements:", [
            "Bethel", ("Naaran", "eastward"), ("Gezer", "westward"),
            "Shechem", "Azzah"])),
         T(("~and by the borders of Manasseh:", [
             "Beth Shean", "Taanach", "Megiddo",
             ("Dor", "with their towns")]))],
    ], explicit={
        20: ["Ephraim", "Shuthelah", "Bered", "Tahath", "Eleadah",
             "Tahath#2"],
        21: ["Zabad", "Shuthelah#2",
             "~also his sons Ezer and Elead, killed by the",
             "~men of Gath when they came for the livestock;"],
        22: ["~Ephraim their father mourned many days"],
    }),
    sc("The sons of Asher", 30, 40, [
        [T(("Asher", ["Imnah", "Ishvah", "Ishvi",
                      ("Beriah", [
                          ("Heber", [
                              ("Japhlet", ["Pasach", "Bimhal", "Ashvath"]),
                              "Shomer", "Hotham",
                              ("Shua", "their sister")]),
                          ("Malchiel", "the father of Birzaith")]),
                      ("Serah", "their sister")]))],
        [T(("Shemer", ["Ahi", "Rohgah", "Jehubbah", "Aram"])),
         T(("Helem", "his brother", [
             ("Zophah", ["Suah", "Harnepher", "Shual", "Beri", "Imrah",
                         "Bezer", "Hod", "Shamma", "Shilshah", "Ithran",
                         "Beera"]),
             "Imna", "Shelesh", "Amal"]))],
        [T(("Jether", ["Jephunneh", "Pispa", "Ara"])),
         T(("Ulla", ["Arah", "Hanniel", "Rizia"])),
         T(("~26,000 men fit for war — heads of houses,", [])),
         T(("~choice and mighty men, chief of the princes", []))],
    ], explicit={
        40: ["~26,000 men fit for war — heads of houses,",
             "~choice and mighty men, chief of the princes"],
    }),
]

# ---------------------------------------------------------------------------
# Chapter 8 — Benjamin, to the house of Saul
# ---------------------------------------------------------------------------

CH8 = [
    sc("Benjamin: the sons of Bela", 1, 7, [
        [T(("Benjamin", [("Bela", "his firstborn"),
                         ("Ashbel", "the second"),
                         ("Aharah", "the third"),
                         ("Nohah", "the fourth"),
                         ("Rapha", "the fifth")]))],
        [T(("Bela", ["Addar", "Gera", "Abihud", "Abishua", "Naaman",
                     "Ahoah", "Gera", "Shephuphan", "Huram"]))],
        [T(("~heads of the households of Geba,", [])),
         T(("~carried captive to Manahath:", [])),
         T(("Ehud", ["Naaman", "Ahijah",
                     ("Gera", "who carried them captive", [
                         "Uzza", "Ahihud"])]))],
    ], explicit={
        6: ["Ehud", "~heads of the households of Geba,",
            "~carried captive to Manahath:"],
    }),
    sc("Shaharaim in Moab", 8, 13, [
        [T(("Shaharaim", "in Moab, after sending his wives away", [
            ("~by Hodesh his wife:", [
                "Jobab", "Zibia", "Mesha", "Malcam", "Jeuz", "Shachia",
                ("Mirmah", "heads of households")])]))],
        [T(("~by Hushim:", ["Abitub", "Elpaal"])),
         T(("Elpaal", ["Eber", "Misham",
                       ("Shemed", "who built Ono and Lod"),
                       "Beriah",
                       ("Shema", "they drove out the men of Gath")]))],
    ]),
    sc("Heads of households in Jerusalem", 14, 28, [
        [T(("~the sons of Beriah:", [
            "Ahio", "Shashak", "Jeremoth", "Zebadiah", "Arad", "Eder",
            "Michael", "Ishpah", "Joha"])),
         T(("~heads of households, chief men —", [])),
         T(("~these lived in Jerusalem", []))],
        [T(("~the sons of Elpaal:", [
            "Zebadiah", "Meshullam", "Hizki", "Heber", "Ishmerai",
            "Izliah", "Jobab"])),
         T(("~the sons of Shimei:", [
             "Jakim", "Zichri", "Zabdi", "Elienai", "Zillethai",
             "Eliel", "Adaiah", "Beraiah", "Shimrath"]))],
        [T(("~the sons of Shashak:", [
            "Ishpan", "Eber", "Eliel", "Abdon", "Zichri", "Hanan",
            "Hananiah", "Elam", "Anthothijah", "Iphdeiah", "Penuel"])),
         T(("~the sons of Jeroham:", [
             "Shamsherai", "Shehariah", "Athaliah", "Jaareshiah",
             "Elijah", "Zichri"]))],
    ], explicit={
        28: ["~heads of households, chief men —",
             "~these lived in Jerusalem"],
    }),
    sc("The fathers of Gibeon", 29, 32, [
        [T(("~the father of Gibeon lived in Gibeon —", [])),
         T(("Maacah", "his wife")),
         T(("~his sons:", [
             ("Abdon", "the firstborn"), "Zur", "Kish", "Baal",
             "Nadab", "Gedor", "Ahio", "Zecher"]))],
        [C("Mikloth", "Shimeah"),
         T(("~they too lived in Jerusalem,", [])),
         T(("~near their brothers", []))],
    ]),
    sc("The house of Saul", 33, 40, [
        [T(CT("Ner", "Kish",
              ("Saul", None, [
                  CT("Jonathan", "Merib Baal",
                     ("Micah", ["Pithon", "Melech", "Tarea",
                                ("Ahaz", [
                                    ("Jehoaddah", [
                                        "Alemeth", "Azmaveth",
                                        CT("Zimri", "Moza", "Binea",
                                           "Raphah", "Eleasah",
                                           ("Azel", "six sons:", [
                                               "Azrikam", "Bocheru",
                                               "Ishmael", "Sheariah",
                                               "Obadiah", "Hanan"]))])])])),
                  "Malchishua", "Abinadab", "Eshbaal"])))],
        [T(("Eshek", "his brother", [
             ("Ulam", "his firstborn"),
             ("Jeush", "the second"),
             ("Eliphelet", "the third")])),
         T(("~Ulam’s sons: mighty archers — 150 sons", [])),
         T(("~and sons’ sons, all of Benjamin", []))],
    ], explicit={
        40: ["~Ulam’s sons: mighty archers — 150 sons",
             "~and sons’ sons, all of Benjamin"],
    }),
]

# ---------------------------------------------------------------------------
# Chapter 9 — the returnees; Saul's house again
# ---------------------------------------------------------------------------

CH9 = [
    sc("The first to return", 1, 3, [
        [T(("~all Israel was listed by genealogies —", [])),
         T(("~written in the book of the kings of Israel;", [])),
         T(("~Judah was carried to Babylon", [])),
         T(("~for their disobedience", []))],
        [T(("~the first to live again in their cities:", [
            "Israel", "the priests", "the Levites",
            "the temple servants"])),
         T(("~and in Jerusalem lived children of Judah,", [])),
         T(("~Benjamin, Ephraim, and Manasseh", []))],
    ], explicit={
        1: ["~all Israel was listed by genealogies —",
            "~written in the book of the kings of Israel;",
            "~Judah was carried to Babylon", "~for their disobedience"],
        2: ["~the first to live again in their cities:",
            "Israel", "the priests", "the Levites",
            "the temple servants"],
        3: ["~and in Jerusalem lived children of Judah,",
            "~Benjamin, Ephraim, and Manasseh"],
    }),
    sc("Of Judah and Benjamin in Jerusalem", 4, 9, [
        [T(("~of Judah — of the children of Perez:", [])),
         C("Uthai", "Ammihud", "Omri", "Imri", "Bani"),
         T(("Asaiah", "the firstborn, of the Shilonites")),
         T(("Jeuel", "of the sons of Zerah — 690 brothers"))],
        [T(("~of Benjamin:", [])),
         C("Sallu", "Meshullam", "Hodaviah", "Hassenuah"),
         T(("Ibneiah", "the son of Jeroham")),
         C("Elah", "Uzzi", "Michri")],
        [C("Meshullam", "Shephatiah", "Reuel", "Ibnijah"),
         T(("~956 brothers by their generations —", [])),
         T(("~all heads of fathers’ households", []))],
    ], explicit={
        9: ["~956 brothers by their generations —",
            "~all heads of fathers’ households"],
    }, foot="each line reads downward: the son of, the son of …"),
    sc("The priests", 10, 13, [
        [T(("~of the priests:", [
            "Jedaiah", "Jehoiarib", "Jachin"])),
         C("Azariah", "Hilkiah", "Meshullam", "Zadok", "Meraioth",
           ("Ahitub", "the ruler of God’s house"))],
        [C("Adaiah", "Jeroham", "Pashhur", "Malchijah"),
         C("Maasai", "Adiel", "Jahzerah", "Meshullam", "Meshillemith",
           "Immer"),
         T(("~and their brothers: 1,760 very able men", [])),
         T(("~for the work of the service of God’s house", []))],
    ], explicit={
        13: ["~and their brothers: 1,760 very able men",
             "~for the work of the service of God’s house"],
    }, foot="each line reads downward: the son of, the son of …"),
    sc("The Levites", 14, 16, [
        [T(("~of the Levites:", [])),
         C("Shemaiah", "Hasshub", "Azrikam",
           ("Hashabiah", "of the sons of Merari")),
         T(("~", ["Bakbakkar", "Heresh", "Galal"])),
         C("Mattaniah", "Mica", "Zichri", "Asaph")],
        [C("Obadiah", "Shemaiah", "Galal", "Jeduthun"),
         C("Berechiah", "Asa",
           ("Elkanah", "who lived in the Netophathite villages"))],
    ], foot="each line reads downward: the son of, the son of …"),
    sc("The gatekeepers", 17, 27, [
        [T(("~the gatekeepers:", [
            ("Shallum", "the chief"), "Akkub", "Talmon", "Ahiman"])),
         T(("~who served in the king’s gate eastward,", [])),
         T(("~for the camp of the children of Levi", [])),
         C("Shallum", "Kore", "Ebiasaph", "Korah"),
         T(("~the Korahites kept the thresholds of the tent,", [])),
         T(("~as their fathers kept the entry of Yahweh’s camp", []))],
        [T(("Phinehas", "son of Eleazar — ruler in time past")),
         T(("Zechariah", "son of Meshelemiah — door keeper")),
         T(("~212 chosen gatekeepers, ordained in their", [])),
         T(("~office of trust by David and Samuel the seer", [])),
         T(("~they and their children kept the gates", [])),
         T(("~of Yahweh’s house by wards", []))],
        [T(("~gatekeepers on four sides:", [])),
         T(("~east, west, north, and south", [])),
         T(("~their brothers came from their villages", [])),
         T(("~for seven-day turns with them", [])),
         T(("~the four chief gatekeepers kept the rooms", [])),
         T(("~and the treasuries of God’s house,", [])),
         T(("~and opened it morning by morning", []))],
    ], explicit={
        18: ["~who served in the king’s gate eastward,",
             "~for the camp of the children of Levi"],
        19: ["Shallum#2", "Kore", "Ebiasaph", "Korah",
             "~the Korahites kept the thresholds of the tent,",
             "~as their fathers kept the entry of Yahweh’s camp"],
        22: ["~212 chosen gatekeepers, ordained in their",
             "~office of trust by David and Samuel the seer"],
        23: ["~they and their children kept the gates",
             "~of Yahweh’s house by wards"],
        24: ["~gatekeepers on four sides:",
             "~east, west, north, and south"],
        25: ["~their brothers came from their villages",
             "~for seven-day turns with them"],
        26: ["~the four chief gatekeepers kept the rooms",
             "~and the treasuries of God’s house,"],
        27: ["~and opened it morning by morning"],
    }),
    sc("Duties of the temple service", 28, 34, [
        [T(("~some kept the vessels of service,", [])),
         T(("~brought in and out by count", [])),
         T(("~some kept the furniture and the vessels of", [])),
         T(("~the sanctuary: the fine flour, the wine, the oil,", [])),
         T(("~the frankincense, and the spices", [])),
         T(("~sons of the priests mixed the spices", []))],
        [T(("Mattithiah", "over the things baked in pans")),
         T(("~Kohathites prepared the show bread", [])),
         T(("~every Sabbath", [])),
         T(("~the singers lived in the rooms, free from", [])),
         T(("~other service — employed day and night", [])),
         T(("~heads of Levite households; they lived", [])),
         T(("~at Jerusalem", []))],
    ], explicit={
        28: ["~some kept the vessels of service,",
             "~brought in and out by count"],
        29: ["~some kept the furniture and the vessels of",
             "~the sanctuary: the fine flour, the wine, the oil,",
             "~the frankincense, and the spices"],
        30: ["~sons of the priests mixed the spices"],
        32: ["~Kohathites prepared the show bread", "~every Sabbath"],
        33: ["~the singers lived in the rooms, free from",
             "~other service — employed day and night"],
        34: ["~heads of Levite households; they lived",
             "~at Jerusalem"],
    }),
    sc("The house of Saul, again", 35, 44, [
        [T(("Jeiel", "the father of Gibeon — he lived in Gibeon")),
         T(("Maacah", "his wife")),
         T(("~his sons:", [
             ("Abdon", "the firstborn"), "Zur", "Kish", "Baal", "Ner",
             "Nadab", "Gedor", "Ahio", "Zechariah", "Mikloth"])),
         C("Mikloth", "Shimeam")],
        [T(CT("Ner", "Kish",
              ("Saul", None, [
                  CT("Jonathan", "Merib Baal",
                     ("Micah", ["Pithon", "Melech", "Tahrea",
                                ("Ahaz", [
                                    ("Jarah", [
                                        "Alemeth", "Azmaveth",
                                        CT("Zimri", "Moza", "Binea",
                                           "Rephaiah", "Eleasah",
                                           ("Azel", "six sons:", [
                                               "Azrikam", "Bocheru",
                                               "Ishmael", "Sheariah",
                                               "Obadiah", "Hanan"]))])])])),
                  "Malchishua", "Abinadab", "Eshbaal"])))],
    ]),
]

CHAPTERS = {1: CH1, 2: CH2, 3: CH3, 4: CH4, 5: CH5,
            6: CH6, 7: CH7, 8: CH8, 9: CH9}
