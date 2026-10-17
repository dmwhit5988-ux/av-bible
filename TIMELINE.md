# The chronology layer

A dated spine for the family tree — Adam to Jesus — that is rigorous where
the text supports rigour and openly empty where it does not.

It exists because the honest answer to "can we date the tree?" is *most of
it, no* — and the interesting chart is the one that shows exactly where the
dating stops.

## Status — built (2026-09-13)

| what | where |
|---|---|
| the data, the binding, the audit | `chronology.py` — run it for the coverage report |
| the sheet | `generate_ot_timeline_svg.py` → `visuals/reference/Old_Testament_timeline.svg` + `.html` |

84 of 1,258 people dated (6.7%): 29 lives, 41 reigns, 14 placed by an
event. Sheet is 65,000 × 11,500 px — a ribbon, because siblings cannot be
wrapped into rows on a time axis without saying brothers were born decades
apart; only runs of childless brothers are gridded, since nothing hangs
below a leaf.

Three things the build settled that the spec below did not:

* **Binding came free.** `matthew_tree.build()` already returns `at`, a
  chain-walked locator dict for every name from Abraham to Jesus. Section 4
  reduced to a `locate()` that walks a path of labels from `at`, from Adam,
  or from a label that must be unique — and 83 of 84 resolved first time.
* **Structure wins over date for placement.** Daniel is deported in 606 but
  hangs under Jeconiah (599) by the dashed "royal offspring" inference. The
  axis must stay monotone, so a son is never drawn above his father; the box
  prints the true year and the audit reports the case instead of failing.
* **The scale breaks itself.** One monotone map, `BASE` px per year,
  stretched wherever a parent would otherwise sit on its child — so the axis
  opens out in the monarchy and closes up where nothing is recorded, and
  the century ticks on the rail show exactly where. No hand-set zones.

What the sheet carries: BC/AM rail on the left; Ussher's years throughout,
with a right-hand rail showing Thiele's dates and the drift (−44 at the
division of the kingdom, −2 at the fall); five tinted zones with rotated
titles; eleven event lines from the Flood to the Nativity; a gutter of
lifespan and reign bars packed into lanes (Methuselah's ends on the flood
line; co-regencies overlap); date chips on every dated box; Luke's eighteen
names floating through the silence beside Matthew's ten.

The spec as written follows.

---

## 1. What this is

`generate_ot_family_tree_svg.py` draws 1,268 people in one contiguous
descent from Adam. It is a **structural** chart: the y axis is how far you
are from Adam in generations, not in years.

This layer adds a second reading of the same tree, where **y is time**. It
is a separate output, not a modification of the wall chart, for reasons
that section 2 makes unavoidable.

The deliverable is one poster and one claim:

> Of 1,268 people on the tree, about 70 can be given a date. Here they are,
> placed in time; here is everyone else, placed only by descent; and here
> are the four places where the chronology forks or fails.

The empty parts are the content. A chart that ran a confident unbroken line
from 4004 BC to Bethlehem would be lying, and it would be less interesting
than the truth.

---

## 2. Four findings from the existing code that constrain the design

These were measured, not assumed. They are the reason this is a new
generator rather than a ruler bolted onto the side of the old one.

### 2.1 Depth does not map to y — the "generation bands" are not bands

`generate_ot_family_tree_svg.py` opens by saying *"Every node at depth d
sits at the same y."* On the laid-out sheet that is false, and not
marginally:

    bands with y-spread > 0 :  50 of 65
    worst band spread       :  13,254 px
    depth 12                :  32 nodes spread over 581 px

`place()` sets a child's y from `top + n.h + DROP`, and the wrapped leaf
grids then push later rows down by `h + ROW_GAP` each. So y accumulates
through the parent's own box height and through however many rows the
siblings above wrapped into. Generation is *approximately* height, never
exactly.

**Consequence.** You cannot hang a year rail down the left of the existing
sheet. Nothing would line up with it. A chronology chart needs its own
placement pass in which y is computed from the date and nothing else — and
that pass will produce a completely different sheet shape, because time and
packing want opposite things.

*(Worth fixing the docstring either way — it describes an intention the code
does not implement.)*

### 2.2 Labels are not keys

    total nodes      : 1268
    distinct labels  :  925
    reused labels    :  205

Every group we want to date contains collisions:

| group | found | ambiguous |
|---|---|---|
| Genesis 5 | 10/10 | Enoch ×2, Lamech ×2, Noah ×2 |
| Genesis 11 | 10/10 | Shelah ×2, Eber ×4, Nahor ×2 |
| kings of Judah | 21/21 | Abijah ×6, Joash ×5, Ahaz ×2, Joram ×2, … |
| post-exilic | 9/10 | Jonathan ×3, Eliashib ×2 |

A table keyed `"Joash": 835` would bind to whichever Joash the walk reached
first. There are five.

### 2.3 `node.key` is stable per build but positional across edits

`Tree.seal()` gives every node a key (`Abijah_3`) from a pre-order counter.
That is stable for a given tree but **silently rebinds** the moment anyone
inserts a node earlier in the walk — the sixth Abijah becomes the third and
a date lands on the wrong man with no error.

This is the same hazard the project already met and solved once, with the
`src` flatten-index stamps in `chronicles_tree.py`. Solve it the same way:
bind explicitly, then assert.

### 2.4 The regnal data is already in the repo — as prose

`ot_grafts.py` carries every reign length, in `note` strings:

    N("Jeroboam", "Solomon's servant … — 22 years", kind="king", …)
    N("Nadab",    "2 years, whom Baasha struck at Gibbethon", …)
    N("Elah",     "2 years, whom Zimri his servant killed …", …)

The sourcing work is **done**. What is missing is structure. Do not
re-research these and do not regex them out of the notes either — promote
them to real fields and let the note keep saying it in words for the reader.

---

## 3. `chronology.py` — the data module

One new module, no dependency on any drawing code, runnable standalone for
audit exactly like `chronicles_tree.py`.

### 3.1 The Anno Mundi spine is computed, not typed

Genesis 5 and 11 are the only genealogies in Scripture that give both
age-at-begetting and total lifespan for every link. That makes them a
dataset. Type the two columns the text gives and derive everything else:

    # (name, age at begetting the next link, total years lived)
    GEN5 = [("Adam",130,930), ("Seth",105,912), ("Enosh",90,905),
            ("Kenan",70,910), ("Mahalalel",65,895), ("Jared",162,962),
            ("Enoch",65,365), ("Methuselah",187,969), ("Lamech",182,777),
            ("Noah",500,950)]
    GEN11 = [("Shem",100,600), ("Arpachshad",35,438), ("Shelah",30,433),
             ("Eber",34,464), ("Peleg",30,239), ("Reu",32,239),
             ("Serug",30,230), ("Nahor",29,148), ("Terah",70,205)]

Verified output:

    Noah born AM 1056      flood AM 1656
    Methuselah  AM  687-1656     <- dies the year of the flood, exactly
    alive at the flood: Methuselah, Noah, Shem
    Adam (AM 0-930) overlaps everyone through Lamech

Those overlaps are the single best thing on the chart and they fall out of
the arithmetic for free. Nobody has to be told Adam could have spoken to
Lamech; they can see the bars.

### 3.2 Forks are constants, not decisions baked into the data

Four switches. Each changes everything upstream of it, so each is a named
constant with the variant values beside it and a note saying who reads it
which way.

    TEXT        = "MT"      # MT | LXX | SAM   — Gen 5/11 begetting ages
    ABRAM_BIRTH = 130       # Terah's age: 70 (Gen 11:26 flat) | 130 (Acts 7:4)
    SOJOURN     = 430       # 430 in Egypt (AV/MT) | 215 (LXX/Sam, Gal 3:17)
    EXODUS_GAP  = 480       # 1 Kgs 6:1 | 440 (LXX) | ~450 judges (AV Acts 13:20)

Effect of just the second switch, computed:

    Terah  70  ->  Abram AM 1948, Isaac 2048, Jacob 2108, Egypt 2238
    Terah 130  ->  Abram AM 2008, Isaac 2108, Jacob 2168, Egypt 2298

The text tradition switch moves creation by roughly 1,400 years (MT ~4004
BC, LXX ~5500 BC). No archaeology arbitrates it.

### 3.3 The BC anchor

One constant converts the whole AM scale:

    CREATION_BC = 4004      # Ussher

`bc = CREATION_BC - am`. With `ABRAM_BIRTH = 130` this reproduces Ussher
exactly — flood 2348 BC, Abram born 1996 BC — which confirms Ussher took
Terah at 130, and gives a free regression test.

**Recommendation: adopt Ussher as the house chronology.** These dates were
printed in AV margins for over two centuries; for an *Authorized Version*
project that is restoration, not imposition. Carry modern synchronised dates
as a second muted scale from the monarchy down, where the two visibly part
company (fall of Jerusalem: Ussher 588, Thiele 586; division of the kingdom:
975 vs 931).

### 3.4 Real BC dates, entered as data

From roughly 850 BC the chronology stops being additive and becomes
anchored — the Bur-Sagale eclipse of 763 BC fixes the Assyrian eponym list;
Shalmaneser III puts Ahab at Qarqar in 853 and Jehu paying tribute in 841;
the Babylonian Chronicle dates the first fall of Jerusalem to a day, 16
March 597 BC. So:

    REIGNS = {                       # accession, end, and why we believe it
      "Solomon":  (971, 931, "1 Kgs 11:42 — 40 years"),
      "Ahab":     (874, 853, "Qarqar, Kurkh Monolith — hard anchor"),
      "Jehu":     (841, 814, "Black Obelisk tribute — hard anchor"),
      ...
    }

Two things the drawing must respect. **Reigns overlap** — Jehoshaphat
872-848 runs into Asa's 911-870 — because co-regency is how Thiele resolves
the numbers, and overlapping bars are the honest rendering, not a bug to
flatten. And **each entry carries its warrant**, so the chart can mark which
dates rest on a stone and which on a sum.

### 3.5 Uncertainty is a first-class record

    SPANS = [
      Span("egypt",  "Joseph", "Moses",
           lo=215, hi=430, why="Ex 12:40 vs LXX/Sam + Gal 3:17"),
      Span("judges", "Joshua", "Saul",
           lo=440, hi=480, why="1 Kgs 6:1 vs LXX vs the sum of Judges"),
      Span("silence","Jaddua", "Joseph",
           lo=None, hi=None, why="the genealogy is simply not recorded"),
    ]

A span with `lo is None` is not an error state. It is the most important
object in the module and it gets the most deliberate drawing on the sheet.

---

## 4. Binding dates to tree nodes

Never by label (2.2), never by raw `node.key` (2.3). Bind by explicit
locator, the way `ot_grafts.py` already grafts:

    BIND = [
        ("Joash",  dict(under="David"),            835, 796),
        ("Joash",  dict(under="Jehu"),             798, 782),   # the other one
        ("Abijah", dict(under="Rehoboam"),         913, 911),
    ]

`under=` resolves through the existing `Tree.find(label, nth, under=…)`, so
this reuses machinery that already works rather than inventing a second
lookup.

Then ship an `audit()` alongside it, in the style of
`chronicles_tree.audit()`:

- every `BIND` entry resolves to exactly one node — **assert, loudly**
- no node receives two conflicting dates
- no father is dated later than his son
- every dated node is reachable from Adam
- report coverage: dated / total, per era

That last line is the number that keeps the project honest. Expect roughly
**70 of 1,268 — about 5%.**

---

## 5. The chart

### 5.1 Axis

Vertical, matching the tree's own top-down descent. Ussher BC on the left
rail, AM on the right.

A linear axis is unusable: Genesis 5 would eat 1,600 years of sheet before
anyone interesting happens, and the monarchy — where nearly all the detail
lives — would compress to a sliver. **Break the scale explicitly**, with a
visible ruled break and the compression ratio printed at each one. A stated
break is honest; a silent log scale is not.

Four zones, four ratios, four different renderings:

| zone | span | rendering |
|---|---|---|
| **A. Adam → Joseph** | AM 0–2298 | full lifespan bars, exact both ends |
| **B. Egypt → Judges** | ~430 yrs ± | elastic band, both ends soft |
| **C. Saul → Zedekiah** | 1050–586 BC | reign bars, ±1 yr, overlaps drawn |
| **D. Exile → Jaddua** | 586–332 BC | Persian reigns firm, events floating |
| **E. Jaddua → Jesus** | 332–4 BC | **the dark gap** |

### 5.2 Zone A is the showpiece

Everyone in Genesis 5 and 11 gets a bar from birth to death, because the
text gives both. Overlaps are visible by construction: Adam's bar runs under
eight of his descendants; Methuselah's stops precisely on the flood line.
This zone needs no external source, no interpretive choice beyond `TEXT`,
and no apology.

### 5.3 Zone C is where genealogy and chronology lock

The kings of Judah are simultaneously on the family tree and on the absolute
calendar. This is the only stretch where a name has both a father and a
year, and it should be drawn to show that — reign bars in `ROYAL`, the
descent edges still running through them, and the stone-anchored reigns
(Ahab, Jehu) marked distinctly from the summed ones.

### 5.4 Zone E — how to draw the gap

This is the design problem and it deserves the best drawing on the sheet.

The tree ends at **Jaddua**, "the last high priest the Old Testament names"
(the note `ot_grafts._after()` already gives him), whom Josephus places at
Alexander's arrival, ~332 BC. Matthew's tail — Abiud, Eliakim, Azor, Zadok,
Achim, Eliud, Eleazar, Matthan, Jacob, Joseph — is the twelve nodes
`matthew_tree._tail()` adds, and every one of them is undated and
unattested anywhere outside that verse.

Draw it as **two parallel unpinned chains crossing an empty band**:

- Matthew's ~10 names across ~525 years — *~50 years per generation,
  biologically implausible*, and Matthew demonstrably compresses elsewhere
  (`matthew_tree.PASSED` already records the five he skips: Ahaziah, Joash,
  Amaziah, Jehoiakim, Pedaiah).
- Luke's ~18 names across the same span — ~29 years each, entirely normal.
- **Not one name in common.** The two lines part at David — Solomon's line
  versus Nathan's — and never rejoin until Joseph.

Neither chain touches either edge of the band. They float, deliberately, and
the band is labelled with what it is: *the genealogy is not recorded here.*

Then one closing note, because even the far edge is soft: Herod died in 4
BC, but Luke ties the census to Quirinius, whose Syrian legateship falls in
AD 6. The endpoint is ±10 years.

### 5.5 Undated nodes

The other ~1,200 people cannot go on a time axis and must not be faked onto
one. Two options, and the first is better:

1. **Dated spine only.** Adam → Noah → Abraham → Judah → David → the kings
   → Zerubbabel → Jesus, with tribal branches shown as *collapsed weights*
   — a labelled block reading "JUDAH · 214 descendants" hanging off Judah
   rather than 214 boxes. Readable at poster size, honest about what is
   known, and it makes the dated spine the subject.
2. Full tree with undated nodes hung by generation depth off their nearest
   dated ancestor — truthful only if those edges are visibly distinguished
   from real placement, and at 1,268 nodes it will fight the broken axis.

Build 1. Keep 2 as a maybe.

---

## 6. Build order

| # | step | output |
|---|---|---|
| 1 | `chronology.py` — AM spine, forks, BC anchor, reigns, spans | prints a dated table; no drawing |
| 2 | `audit()` — binding assertions + coverage report | the honest denominator |
| 3 | Promote reign lengths in `ot_grafts.py` to real fields | notes unchanged for the reader |
| 4 | Zone A standalone: the Genesis 5/11 lifespan chart | ships on its own; needs nothing else |
| 5 | Broken-axis machinery + zones C and D | |
| 6 | Zone E, the dark gap | the piece worth doing well |
| 7 | Assemble the poster | |

Step 4 is a complete, publishable graphic by itself and depends on nothing
after step 1. If this stalls anywhere, it stalls having already produced
something good.

---

## 7. What this will not do

Stated plainly so nobody has to rediscover it later:

- **It will not date most of the tree.** ~5% coverage. That is a fact about
  the sources, not a gap to be closed by more work.
- **It will not settle the forks.** MT/LXX, 430/215, 480/440 are switches,
  not conclusions. The chart shows the consequences of each; it does not
  adjudicate.
- **It will not bridge Jaddua to Joseph.** Nothing can, from the text. Some
  chronologies use Daniel's seventy weeks as a bridge; that is an
  interpretive move, and if it ever goes on the sheet it goes on labelled as
  one.
- **It will not give Jesus a birth year.** 6–4 BC, with the Quirinius
  problem drawn rather than hidden.
