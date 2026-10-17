"""Matthew's genealogy, read against the whole Old Testament family tree.

Matthew 1:1-17 is not a new list. Thirty-six of its forty-two names are
already standing on the welded tree that `chronicles_tree.build(ot=True)`
produces for 1 Chronicles 1-9 — Abraham to Zerubbabel is ONE unbroken
parent-child chain there, running from y=1291 to y=6422 on the laid-out
sheet. So the right drawing for Matthew 1 is not another tree: it is the
Old Testament tree with a line lit down it, and the reader watching the
line arrive at somewhere the Old Testament never went.

What this module adds to that tree, and nothing more:

  * FOUR NAMES the Old Testament has but Matthew reads differently, given
    the doubled label the tree already uses for Abram/Abraham and
    Azariah/Uzziah — Jacob · Israel, Salma · Salmon, Jeconiah · Jechoniah,
    Azariah · Uzziah (already doubled).
  * TWO WOMEN and ONE HUSBAND Matthew names that the tree had no join for:
    Rahab (Salmon's wife), Bathsheba as David's wife rather than only as
    Eliam's daughter, and Uriah beside her.
  * THE TAIL: Abiud, Eliakim, Azor, Zadok, Achim, Eliud, Eleazar, Matthan,
    Jacob, Joseph, Mary, Jesus. Twelve nodes, all of them past the last
    verse of the Old Testament, which is exactly where the genealogy stops
    being a quotation and starts being news.

Two disagreements are drawn rather than resolved, per the chart's rule:

  * ZERUBBABEL'S FATHER. Matthew (and Ezra 3:2, and Haggai) says Shealtiel;
    1 Chronicles 3:19 says Pedaiah, Shealtiel's brother. Zerubbabel stays
    where Chronicles put him and a gold cross-reference runs to Shealtiel.
  * FIVE GENERATIONS MATTHEW PASSES OVER. Ahaziah, Joash and Amaziah sit
    between Joram and Uzziah on the tree, Jehoiakim between Josiah and
    Jechoniah, and Pedaiah between Jechoniah and Zerubbabel. The camera
    walks straight over them and they stay unlit, which is the honest way
    to draw a genealogy that skips — and Matthew's fourteens depend on the
    skipping.

`MatthewLine` carries the verse-by-verse reading. It is the same job
`generate_1chronicles.assign()` does for Chronicles, done by hand here
because Matthew is twenty-five verses and the names are unambiguous once
they are anchored to the chain.
"""

import chronicles_tree as CT
from chronicles_tree import N, walk


# ---------------------------------------------------------------------------
# The line, verse by verse
# ---------------------------------------------------------------------------
#
# Each entry is (verse, [name, ...]) in the order the verse reads them. The
# names are the keys used below to reach a node; a name that is not on the
# Old Testament tree is created by `_tail` or `_women`.

READING = [
    (1,  ["Jesus", "David", "Abraham"]),
    (2,  ["Abraham", "Isaac", "Jacob", "Judah"]),
    (3,  ["Judah", "Perez", "Zerah", "Tamar", "Hezron", "Ram"]),
    (4,  ["Ram", "Amminadab", "Nahshon", "Salmon"]),
    (5,  ["Salmon", "Boaz", "Rahab", "Obed", "Ruth", "Jesse"]),
    (6,  ["Jesse", "David", "Solomon", "Bathsheba", "Uriah"]),
    (7,  ["Solomon", "Rehoboam", "Abijah", "Asa"]),
    (8,  ["Asa", "Jehoshaphat", "Joram", "Uzziah"]),
    (9,  ["Uzziah", "Jotham", "Ahaz", "Hezekiah"]),
    (10, ["Hezekiah", "Manasseh", "Amon", "Josiah"]),
    (11, ["Josiah", "Jechoniah"]),
    (12, ["Jechoniah", "Shealtiel", "Zerubbabel"]),
    (13, ["Zerubbabel", "Abiud", "Eliakim", "Azor"]),
    (14, ["Azor", "Zadok", "Achim", "Eliud"]),
    (15, ["Eliud", "Eleazar", "Matthan", "Jacob (of Joseph)"]),
    (16, ["Jacob (of Joseph)", "Joseph", "Mary", "Jesus"]),
    (17, ["Abraham", "David", "Jechoniah", "Jesus"]),
]

# The generations the tree carries and Matthew reads straight past. They are
# drawn, never lit, and the camera's path goes over them.
PASSED = ["Ahaziah", "Joash", "Amaziah", "Jehoiakim", "Pedaiah"]

# Matthew's three fourteens, for verse 17. The middle name of each pair is
# the hinge the verse names.
SETS = [("Abraham", "David"), ("David", "Jechoniah"), ("Jechoniah", "Jesus")]


# ---------------------------------------------------------------------------
# Grafting
# ---------------------------------------------------------------------------

def _relabel(T, old, new, note=None):
    n = T.find(old)
    n.label = new
    if note:
        n.note = f"{n.note} · {note}" if n.note else note
    return n


def _women(T, at):
    """The three women Matthew names that the tree had no join for.

    Ruth and Tamar were already here — Ruth as Boaz's wife out of the book
    of Ruth, Tamar as Judah's in 1 Chronicles 2:4 — which is half of why
    this design works at all.
    """
    salma = at["Salmon"]
    rahab = N("Rahab", "of Jericho — Matthew 1:5; Joshua 2, 6:25",
              kind="woman", link="wife", ref="Matthew 1:5")
    salma.kids.insert(0, rahab)
    at["Rahab"] = rahab

    # Matthew does not name Bathsheba; he names her first husband, and the
    # tree had her only as Eliam's daughter, a long way from Solomon. She
    # goes in beside David, where the verse puts her, and the cross-
    # reference keeps the sheet honest about her being one person.
    david = at["David"]
    bath = N("Bathsheba", "“her who had been Uriah's wife” — Matthew 1:6; "
             "2 Samuel 11-12", kind="woman", link="wife", ref="Matthew 1:6")
    uriah = N("Uriah", "the Hittite, one of David's mighty men — "
              "2 Samuel 11:3, 23:39", link="wife", ref="Matthew 1:6")
    bath.kids.append(uriah)
    david.kids.insert(0, bath)
    at["Bathsheba"], at["Uriah"] = bath, uriah
    T.link(bath, T.find("Bathsheba · Bathshua"),
           "the same woman — 1 Chronicles 3:5 reckons her by her father")


def _tail(T, at):
    """Abiud to Jesus: the twelve names past the end of the Old Testament.

    They hang under Zerubbabel, where Matthew hangs them. Jesus is not
    Joseph's child on this sheet — he is Mary's, with Joseph married in,
    which is the shape of verse 16's own sentence ("Joseph, the husband of
    Mary, from whom was born Jesus").
    """
    tail = ["Abiud", "Eliakim", "Azor", "Zadok", "Achim", "Eliud",
            "Eleazar", "Matthan"]
    nodes = []
    for i, label in enumerate(tail):
        n = N(label, ref="Matthew 1:13-15" if i == 0 else None)
        nodes.append(n)
    jacob = N("Jacob", "the father of Joseph — not the patriarch",
              ref="Matthew 1:15")
    nodes.append(jacob)
    joseph = N("Joseph", "the husband of Mary, a carpenter of Nazareth",
               ref="Matthew 1:16", icon="man")
    nodes.append(joseph)

    # FIRST of Zerubbabel's children, not last. The chart wraps a family
    # whose children are too wide to sit in one row, and rows after the
    # first hang below the whole HEIGHT of the row above — so appending put
    # Abiud a thousand pixels under his father, with Chronicles' own post-
    # exilic list in between, and the line appeared to restart rather than
    # continue. At the head of the row he descends from Zerubbabel exactly
    # as any other son does, and Matthew's line and Chronicles' run down
    # side by side, which is the truth of the matter.
    nodes[0].ref = "Matthew 1:13 — past the end of the Old Testament"
    at["Zerubbabel"].kids.insert(0, nodes[0])
    for a, b in zip(nodes, nodes[1:]):
        a.kids.append(b)

    mary = N("Mary", "of whom was born Jesus", kind="woman", link="wife",
             ref="Matthew 1:16")
    joseph.kids.append(mary)
    jesus = N("Jesus", "who is called Christ", kind="king",
              ref="Matthew 1:16", icon="star")
    mary.kids.append(jesus)

    for label, n in zip(tail, nodes):
        at[label] = n
    at["Jacob (of Joseph)"] = jacob
    at["Joseph"], at["Mary"], at["Jesus"] = joseph, mary, jesus


def build():
    """-> (Tree, {matthew name: node}).

    The Old Testament tree, with Matthew's readings and Matthew's tail.
    """
    T = CT.build(ot=True)

    # The doubled labels. The tree already reads Abram · Abraham and
    # Azariah · Uzziah this way; these three are the same case, and without
    # them a reader following the narration hears "Jacob" and "Salmon" and
    # finds no such box on the sheet.
    _relabel(T, "Israel", "Jacob · Israel")
    _relabel(T, "Salma", "Salma · Salmon", "Matthew 1:4-5 reads Salmon")
    _relabel(T, "Jeconiah", "Jeconiah · Jechoniah")

    david = T.find("David")
    at = {
        "Abraham": T.find("Abram · Abraham"),
        "Isaac": T.find("Isaac"),
        "Jacob": T.find("Jacob · Israel"),
        "David": david,
    }
    # Almost every name from Judah down is ambiguous across the canon —
    # Reuben's son Hezron stands before Perez's in pre-order, there is a
    # Levite Amminadab, a second Ram in Jerahmeel's house, two Obeds. Names
    # are no way to reach them. Walk the chain instead, which cannot pick
    # the wrong man: each of these is the child of the one above it.
    at["Judah"] = _kid(at["Jacob"], "Judah")
    at.update(_walk_down(at["Judah"], [
        "Tamar", "Perez", "Hezron", "Ram", "Amminadab", "Nahshon",
        "Salma · Salmon", "Boaz", "Obed", "Jesse"]))
    at["Salmon"] = at.pop("Salma · Salmon")
    at["Zerah"] = _kid(at["Tamar"], "Zerah")
    at["Ruth"] = _kid(at["Boaz"], "Ruth")

    # The kings are walked for the same reason, and more urgently: scoping a
    # bare `find` under David is not enough on its own — Rehoboam's house
    # holds a second Abijah, and pre-order reaches him first. (This is the
    # ordinal trap that put a crowned Joash in Shelah's branch when the OT
    # chart was built.) The crown descends one child at a time.
    at.update(_walk_down(david, [
        "born to him in Jerusalem", "Solomon", "Rehoboam", "Abijah", "Asa",
        "Jehoshaphat", "Joram", "Ahaziah", "Joash", "Amaziah",
        "Azariah · Uzziah", "Jotham", "Ahaz", "Hezekiah", "Manasseh",
        "Amon", "Josiah", "Jehoiakim", "Jeconiah · Jechoniah", "Pedaiah",
        "Zerubbabel"]))
    at["Uzziah"] = at.pop("Azariah · Uzziah")
    at["Jechoniah"] = at.pop("Jeconiah · Jechoniah")
    at["Shealtiel"] = _kid(at["Jechoniah"], "Shealtiel")

    _women(T, at)
    _tail(T, at)

    # Chronicles hangs Zerubbabel on Pedaiah; Matthew, Ezra and Haggai hang
    # him on Shealtiel. Both are drawn — he keeps his Chronicles father and
    # the gold arc carries Matthew's claim across to his uncle.
    T.link(at["Shealtiel"], at["Zerubbabel"],
           "Matthew 1:12, Ezra 3:2 — “Shealtiel's son”; "
           "1 Chronicles 3:19 says Pedaiah")

    T.seal()
    return T, at


def _kid(node, label):
    return next(k for k in node.kids if k.label == label)


def _walk_down(node, labels):
    """Follow a single-child descent by name, one step at a time.

    `T.find` walks pre-order from the root, so a common name finds whichever
    copy the traversal reaches first. Every name here is the only child of
    the one above it, so stepping down the chain cannot pick the wrong man.
    """
    out, cur = {}, node
    for label in labels:
        cur = next(k for k in cur.kids if k.label == label)
        out[label] = cur
    return out


# ---------------------------------------------------------------------------
# The reading
# ---------------------------------------------------------------------------

class MatthewLine:
    """Verses 1-17 resolved onto the tree.

    `lit[v]` is every node the verse names, in reading order. `arrivals[v]`
    is the subset the sheet has not shown before — for Matthew that is only
    ever the tail, because the Old Testament is already standing when the
    New Testament opens. That difference is the whole point of the design:
    the reader watches a line they know run out past the last thing they
    know.
    """

    def __init__(self, tree, at):
        self.tree, self.at = tree, at
        self.lit, self.arrivals, self.first_of = {}, {}, {}
        # Everything Matthew adds arrives; everything the Old Testament
        # already carried is context, standing from the first frame.
        new = {at[k] for k in ("Rahab", "Bathsheba", "Uriah", "Abiud",
                               "Eliakim", "Azor", "Zadok", "Achim", "Eliud",
                               "Eleazar", "Matthan", "Jacob (of Joseph)",
                               "Joseph", "Mary", "Jesus")}
        for v, names in READING:
            nodes = [at[n] for n in names]
            self.lit[v] = nodes
            arriving = []
            for n in nodes:
                if n in new and n not in self.first_of:
                    self.first_of[n] = v
                    arriving.append(n)
            self.arrivals[v] = arriving
        self.new = new
        self.passed = [at[label] for label in PASSED]

    def path(self):
        """Abraham to Jesus down the tree, every node on the way — the ones
        Matthew names and the four he passes over."""
        out, n = [], self.at["Jesus"]
        stop = self.at["Abraham"]
        while n is not None:
            out.append(n)
            if n is stop:
                break
            n = n.parent
        out.reverse()
        return out
