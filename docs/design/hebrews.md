# Hebrews — visual design

> ## ✅ Built (2026-08-14) — all 13 chapters, 303 verses
>
> `generate_hebrews_svg.py` + `svg_priest.py`, registered in
> `svg_generators.json`, in the visuals manifest.
> Audit (`tools/audit_heb.py`): **0 off-canvas, 0 text overlaps, no
> identical run longer than 3** — including across 9:1–10:39, the 67-verse
> stretch in one room that was the stagnation risk.
>
> The frame is as designed: the column, per-chapter viewports with the margin
> gauge, the shadow/substance pair, the throne, the voice arcs, the BETTER
> thread and the 22 engraved phrases. **2:9** is its proof (the whole column
> at once, the descent running from the seat to the bottom edge); **8:5** is
> its thesis (the projection lines drawn between substance and shadow, so the
> page explains itself); **12:27** its resolution (the shadow simply not
> drawn); **13:13** its reversal.
>
> ### Seven things the build changed
>
> 1. **The shadow was a ziggurat.** Nested enclosures stacked by width put a
>    stepped pyramid on the page — the one silhouette this sanctuary must not
>    have, since Genesis 11 already owns it here. It is now a building in
>    section: a plinth for the camp, a court wall, the house with a gabled
>    roof, and the veil as a rule across it.
> 2. **The throne was a table.** As a slab it lost the single thing the frame
>    exists to say. It now has a back, legs and arms.
> 3. **Chapter 1 dropped the tent.** The chapter never mentions the
>    tabernacle, and the true tent standing mid-frame was crowding out the
>    catena of vv5–13, which *is* the chapter's structure.
> 4. **Engraved phrases land once and go.** They were re-drawn (and
>    re-pulsed) on every later verse, which left chapter 11 with three ringed
>    phrases and a weighing scale in one frame. A hinge phrase is a moment,
>    not furniture.
> 5. **Six chapters cut between sub-scenes rather than accumulating** — 6, 7,
>    9, 10, 12, 13. Chapter 6's four movements in one frame put the field on
>    top of the oath and the fall off the canvas; chapter 9 is five scenes and
>    chapter 10 is six, which is also what keeps that 67-verse stretch alive.
> 6. **The two weighings became a real balance.** 11:26 and 12:16 were two
>    beams with empty rectangles hung off them. `svg_figures.scales()` already
>    existed but only level, and a balance that cannot tip cannot say which
>    side won — so it gained a `tilt` (and `scales_pans()`, so a caller can
>    stand something *in* a pan rather than guess where the pans ended up).
>    Both verses now use one `balance()` helper with real objects in the pans:
>    Moses weighs a stack of coins against a cross and the cross goes down;
>    Esau weighs bread against a scroll and lets the bread go down. Same
>    instrument, same grammar, opposite verdict. The cross is the text's own
>    move, not the drawing's — 11:26 puts "the reproach of *Christ*" into
>    Moses' scale, and 12:2 equates that cross with its shame.
> 7. **Chapter 13 changes viewport at v9** (`VIEW_BY_VERSE`). 13:8 letters
>    "the same yesterday, today, and forever" beside the seat, which the low
>    viewport of the second half does not contain — so the chapter opens wide
>    on the whole column and then drops, which is what it says it is doing.
>
> ### Known soft spots, if it is ever revisited
>
> - **Chapter 5's commission ledger** is six rows of small italic and is the
>   most text-heavy frame in the book.
> - The **five warnings** are drawn in each chapter's own idiom rather than
>   sharing one mark. That was deliberate, but it means the thread is felt
>   rather than seen.

## The original design

> 13 chapters, **303 verses**. `CH_LEN` holds WEB's verse count for each
> chapter: 14, 18, 19, 16, 14, 20, 28, 13, 28, 39, 40, 29, 25.
>
> ⚠️ **Wording.** Quotations below are **WEB** (the project's only text,
> `passages.TRANSLATION`) or, like the engraved phrases of §4, a tight
> paraphrase of it: some are trimmed or re-ordered (*being dead, he still
> speaks*, 11:4; *a body you prepared for me*, 10:5), and several are
> lettered that way on the built graphic. The drawing is built on the WEB
> reading — most consequentially **"copy and shadow"** (8:5), **"collateral
> of a better covenant"** (7:22), **"sawn apart"** (11:37), **"festal
> gathering"** (12:23), and **"the Italians greet you"** (13:24). Check every
> phrase against `web/bibles/WEB/Hebrews_*.json` before lettering it.

---

## 1. Why this book needs its own frame

Romans argues and travels; its design followed a road. Hebrews does neither.
It is a book about **approach** — about how near a person may come, and to
what — and its own vocabulary is relentlessly spatial and vertical:

> *sat down* (1:3, 8:1, 10:12, 12:2) · *drift away* (2:1) · *enter into … rest*
> (11 verses across 3–4) · *passed through the heavens* (4:14) · *draw near*
> (4:16, 7:19, 7:25, 10:1, 10:22) · *within the veil* (6:19) · *the way into
> the Holy Place wasn't yet revealed* (9:8) · *a new and living way, through
> the veil* (10:20) · *outside of the camp* (13:13)

Two further facts shape everything below.

**Hebrews works by sectioning.** It cuts the tabernacle open and walks you
through its rooms (9:1–7); it cuts a man open to the dividing of joints and
marrow (4:12); it cuts open Abraham to show Levi still inside him (7:9–10).
The book's own method is the cross-section — which is exactly the drawing
this project already does well.

**Hebrews hands you a rendering instruction, three times.** The earthly things
are *a copy and shadow of the heavenly* (8:5), *representations of the true*
(9:24), *a shadow of the good to come, not the very image* (10:1). That is
not a metaphor to illustrate; it is a spec for how to draw the lower half of
the frame.

### Geometries considered and rejected as the spine

- **The "better than" ledger** — the catalog's suggestion, and the obvious
  one. Two columns accumulating: angels, Moses, Aaron, covenant, sanctuary,
  sacrifice. **Rejected.** This is precisely the failure the Romans rail
  post-mortem documented: a static table of contents holding for 300 verses,
  with motion that only counts. It summarises the book instead of reading it.
  The word survives as a thread (§3) and the comparisons survive as
  set-pieces; the frame goes elsewhere.
- **The five warnings as the spine** — 2:1–4, 3:7–4:13, 5:11–6:12, 10:26–39,
  12:25–29 interleave the exposition on a fixed rhythm. Too skeletal to carry
  a frame, too structural to waste. Kept as a thread.
- **The voice** — Hebrews quotes the Old Testament some thirty-five times and
  almost never says *it is written*; it says **he says**, *the Holy Spirit
  says*. Kept as a thread, with the Genesis 3 speaker-arc device reused.

---

## 2. The frame: one column, drawn twice

**A single vertical section, drawn once at 1:1 and held for the whole book.**
Bottom to top:

```
        ┌──────────────────────────────┐
        │   THE THRONE  ·  the seat    │  ← solid, lit, the light source
        │   the true tabernacle        │     "which the Lord pitched, not man"
        ├ ─ ─ ─ ─ the heavens ─ ─ ─ ─ ─┤  ← "passed through the heavens" 4:14
        │                              │
        ▓  holy of holies  ·  ark      ▓
        ▓ ══════ THE VEIL ══════       ▓  ← shadow: flat, soft-edged,
        ▓  holy place · lamp · table   ▓     monochrome, no depth
        ▓  the court · altar · laver   ▓
        ▓  the camp                    ▓
        └ ─ ─ ─ ─ outside the gate ─ ─ ┘  ← below the baseline; entered once
                                            (2:9) and finally (13:13)
```

The two halves are **one object and its shadow**. The light source is the
throne at the top of the frame, so the earthly structure below is literally
what the heavenly one casts. 8:5's *the pattern that was shown to you on the
mountain* is drawn as the projection lines running from the upper structure
to the lower — which is
how a shadow is constructed, so the frame explains itself the moment the text
names it.

**The camera's height on the column is the entire progress indicator.** No
bead track, no per-verse caption word, no verse counter — the Romans lesson.
An altitude tick on the margin, as in the Obadiah cliff design, and chapter +
verse small in the top-left corner as plain text.

### What the frame buys

| Verse | What the frame does |
|-------|--------------------|
| 2:9 | the only descent below the camp before ch. 13 — and it prefigures it |
| 6:19 | the veil is punctured at exactly one point by the anchor's line |
| 8:5 | the doubling is *named*, so the frame is justified on screen |
| 8:13 | *becoming old… near to vanishing* — the shadow's edges first fade |
| 10:20 | the puncture of 6:19 opens into a way |
| 12:27 | *the removing of those things that are shaken* — the shadow layer is shaken off and gone. The frame resolves in one verse. |
| 13:13 | the camera drops below the camp, because the altar moved |

That last move is the reason to choose this frame over any other. Twelve
chapters climb; the thirteenth deliberately goes back down and *outside*, and
13:14 gives the reason — *we don't have here an enduring city, but we seek
that which is to come*. The book ends walking, not arrived.

---

## 3. Threads

**The voice arcs.** Every Old Testament quotation draws an arc from a speaker
**above** the frame to a hearer within it — never from a scroll, because
Hebrews never says *it is written*. The chapter-1 catena is seven arcs; the
Jeremiah quotation at 8:8–12 is one long one. The thread has its own small arc:
1:1's *many times and in various ways* is many short fragmentary arcs at
scattered angles, collapsing at 1:2 into one; 5:11's *dull of hearing* is an
arc that greys out at its endpoint; 11:4's Abel *being dead, still speaks* is
an arc rising from a grave; and 12:24's *blood of sprinkling that speaks better
than Abel* answers it, thirteen chapters later, in the same frame. 12:25 —
*don't refuse him who speaks* — closes the thread with an arc turned away.

**The warnings.** Five, and at each one the floor under the camera's current
position gives way in a specific manner: a current that carries sideways (2:1),
a wilderness path that loops and never arrives (3:7–4:13), a field burned to
the root (6:8), a floor opened over fire (10:27–31), a shaking that takes
everything not fastened (12:25–29).

**BETTER.** Eleven verses carry the word — 1:4, 6:9, 7:19, 7:22, 8:6, 9:23,
10:34, 11:16, 11:35, 11:40, 12:24. Each cuts the word small into the
**substance** side of the frame. It is a content thread, not a counter (eleven
marks in 303 verses), but if the rendered book reads it as a tally, cut it.

**The four sittings.** 1:3, 8:1, 10:12, 12:2 — the seat is drawn at 1:3 and
then **never redrawn or altered for the remaining 300 verses**. That is what
makes 13:8 (*the same yesterday, today, and forever*) land: the one element in
the frame that has not changed. There is no seat anywhere in the lower
structure — the standing priests of 10:11 have nowhere to sit, and the drawing
should make that visible long before the text says it.

---

## 4. Text budget

Hebrews argues, so — as with Romans — a wordless canvas fights the text.
Same allowance: **short engraved phrases, 2–7 words, WEB wording or a tight
paraphrase, ALL-CAPS, carved into stone or set as a banner, at hinge verses
only.** Never sentences, never captions, never per-verse prose. Twenty-two
phrases across 303 verses — roughly one per fourteen.

| Verse | Engraved |
|-------|----------|
| 2:9 | BUT WE SEE HIM |
| 3:7 | TODAY, IF YOU WILL HEAR HIS VOICE |
| 4:9 | A SABBATH REST REMAINS |
| 4:12 | LIVING AND ACTIVE |
| 4:16 | LET US DRAW NEAR WITH BOLDNESS |
| 5:6 | A PRIEST FOREVER |
| 6:19 | SURE AND STEADFAST |
| 7:25 | TO THE UTTERMOST |
| 8:5 | A COPY AND SHADOW |
| 8:12 | I WILL REMEMBER THEIR SINS NO MORE |
| 9:12 | ONCE FOR ALL |
| 10:12 | HE SAT DOWN |
| 10:20 | A NEW AND LIVING WAY |
| 10:31 | THE HANDS OF THE LIVING GOD |
| 11:10 | THE CITY WHICH HAS THE FOUNDATIONS |
| 11:16 | A BETTER COUNTRY |
| 11:38 | OF WHOM THE WORLD WAS NOT WORTHY |
| 12:1 | THE RACE SET BEFORE US |
| 12:2 | LOOKING TO JESUS |
| 12:28 | A KINGDOM THAT CANNOT BE SHAKEN |
| 13:8 | THE SAME YESTERDAY, TODAY, AND FOREVER |
| 13:14 | NO ENDURING CITY HERE |

Two of these are deliberately *not* re-engraved on their return: 8:12's line
is already on the stone when the same text comes back at 10:17 (nothing new is
written — that is the point of the verse), and 12:24's better-speaking blood
answers 11:4's arc without a second phrase.

---

## 5. The thirteen chapters

### Hebrews 1 (14 vv.) · 💡 — *the throne, and the servants who have no seat*

Camera at the top of the column.

- **v. 1** — *at many times and in various ways*: many short voice arcs at
  scattered angles, arriving at scattered figures. Fragmentary by design.
- **v. 2** — they collapse into **one** arc. The worlds are drawn as it lands.
- **v. 3** — radiance, image, upholding; then *purified us of our sins* and
  **sat down**. The seat is taken. It is not touched again until 13:8.
- **v. 4** — the angel rank line is drawn across the frame; the seat is above
  it. First BETTER.
- **vv. 5–14** — the **catena**: seven quotations, seven arcs, each landing on
  the Son's side of the rank line or the angels'. v. 7 gives the angels their
  drawing — *winds*, *a flame of fire*: unfixed, moving, never seated. vv.
  10–12 roll the heavens up like a mantle, which should genuinely animate.
  v. 13 begins the footstool (finished at 10:13). v. 14 sends the serving
  spirits *out* of the frame, downward, toward the heirs.

### Hebrews 2 (18 vv.) · 💡 — *the descent below the line*

- **vv. 1–4** — **first warning.** *Drift away*: the things heard drawn as a
  moored point, the figure slipping past it sideways. Then two deliveries
  compared — the word spoken through angels (an arc via the rank line) against
  the word spoken by the Lord (direct), attested by hearers and then by four
  stacked witnesses: signs, wonders, works of power, gifts.
- **vv. 5–8** — Psalm 8 on the height line: *a little lower*, *crowned*, *all
  things under his feet*. Then v. 8 turns on itself — *we don't see all things
  subjected to him, yet* — and the subjection is drawn unfinished, greyed.
- **v. 9** — **the descent.** The figure leaves the seat and goes down the
  column, past the rank line, past the camp, to the frame's lower edge. The
  only downward move in the first twelve chapters, and it rehearses 13:13.
  Engraved: BUT WE SEE HIM.
- **v. 10** — the path drawn down and back, *perfect through sufferings*.
- **vv. 11–13** — three quotations, but the arcs now run **sideways** — Son to
  brothers, not heaven to earth. The speaker has changed position.
- **vv. 14–15** — a lifespan bar drawn shackled end to end (*all their lifetime
  subject to bondage*), then released.
- **vv. 16–18** — two hands offered, one taken (*not to angels, but to the
  offspring of Abraham*). HIGH PRIEST enters the book as an object — the
  garment and breastplate, drawn from **`svg_priest.py`**, which Exodus 28
  built (see its entry in the [content catalog](../content-catalog.md#exodus)).
  The vested figure, the ephod, the
  twelve-stone breastplate and the plate on the forehead are all reuse; what
  Hebrews adds is drawing them in the shadow key of §2.

### Hebrews 3 (19 vv.) · 🏛️ + 🔄 — *the house, and the road that never arrives*

- **vv. 1–6** — the column, read as a **house**. Moses drawn as a servant
  *inside a room*; the Son *over* it at the roofline. v. 3's *he who built the
  house has more honor than the house* puts a builder's hand at the scale of
  the whole structure. v. 6 — *whose house we are* — turns the courses into
  the readers.
- **vv. 7–19** — **second warning**, which does not end here: 3:7–4:13 is one
  continuous sub-world and should be built as such. The camera drops to a
  ground plane beside the column: a wilderness, and at the far end a gate
  marked REST. The generation's forty years are a path that loops and never
  reaches it; v. 17's *bodies fell in the wilderness* marks the loop with
  fallen figures; v. 11's oath bars the gate.
- **TODAY** (vv. 7, 13, 15) is drawn as a sun that does not move. Engraved at
  v. 7.
- **vv. 16–19** — the chapter's own rhetorical form is a ledger: three
  questions, each answered by the same group, and a conclusion. Four rows —
  *who rebelled?* / *with whom was he displeased forty years?* / *to whom did
  he swear?* / **unbelief**. Draw it as the ledger it already is.

### Hebrews 4 (16 vv.) · 🏛️ + 💡 — *the rest, the sword, the ascent*

Three movements, three sub-scenes.

- **vv. 1–11** — the rest. God's own seventh day drawn as a completed work
  (rhyme with the built Genesis 1 / Genesis 2 panels, which already own 2:1–3).
  v. 8 — *if Joshua had given them rest* — draws the conquest as an arrival
  that turns out not to be the gate; the gate stays ahead, still open. Engraved
  at v. 9: A SABBATH REST REMAINS.
- **vv. 12–13** — **the sword.** Not a weapon swung; a **section cut**. The
  figure opened to the dividing of soul and spirit, joints and marrow — *naked
  and laid open*. This is the book's own method applied to a person, and it
  should look like the same kind of drawing as the tabernacle section.
  Engraved: LIVING AND ACTIVE.
- **vv. 14–16** — **the ascent.** The camera lifts off the wilderness floor and
  climbs the column — *passed through the heavens* — arriving at the seat,
  which is relabelled: the throne of Majesty (1:3) is now the **throne of
  grace**. First arrival at the top from below. Engraved: LET US DRAW NEAR
  WITH BOLDNESS.

### Hebrews 5 (14 vv.) · 📊 — *the commission, and the two diets*

- **vv. 1–4** — the high priest's job spec as a **commission ledger**: taken
  from among men · appointed for men · offers gifts and sacrifices · deals
  gently, being himself surrounded with weakness · must offer for himself as
  well · does not take the honour on himself. Six rows, Aaron ticking each.
- **vv. 5–6** — the same ledger run against Christ, on two quotations. The
  row that Aaron cannot tick is **FOREVER** — left blank here, and paid off in
  chapter 7. Engraved at v. 6: A PRIEST FOREVER.
- **vv. 7–10** — *the days of his flesh*: prayers with strong crying and tears,
  obedience learned by suffering, made perfect, named. A descent-and-perfection
  arc that mirrors 2:9–10 at a smaller scale.
- **vv. 11–14** — **third warning opens.** *Dull of hearing* — the voice arc
  arrives and greys out at the ear. Then **milk and solid food**: a growth
  scale with a baby *not experienced in the word of righteousness* at one
  end and the full-grown, *senses exercised to discern good and evil*, at the
  other.

### Hebrews 6 (20 vv.) · 🏛️ + 💡 — *foundation, field, oath, anchor*

Already a vertical chapter; it maps onto the column with no forcing.

- **vv. 1–3** — six foundation stones laid in one course: repentance from dead
  works · faith toward God · teaching of baptisms · laying on of hands ·
  resurrection of the dead · eternal judgment. The point of the passage is
  that you do **not** lay them again — so the course is drawn once and the
  camera moves up off it. The house draw-once-then-hold rule, made literal.
- **vv. 4–6** — five things received (enlightened · tasted the heavenly gift ·
  partakers of the Holy Spirit · tasted the good word · tasted the powers of
  the age to come), drawn as five marks on a figure — then the figure falls
  below the course it was standing on.
- **vv. 7–8** — **the two fields.** One rain-arc splitting to two identical
  plots. One drinks and bears a crop and *receives blessing*; one bears thorns
  and thistles and is burned. No words required.
- **vv. 9–12** — the counter-ledger: *God is not unrighteous, so as to forget
  your work and the labour of love*. Entries that stay.
- **vv. 13–18** — **the oath.** God swore by himself *since he could swear by
  no one greater* — draw the oath as a hand raised toward a higher point that
  is not there, so the gesture curves back on itself. Then *two immutable
  things* as two pillars, and the refuge fled to between them.
- **vv. 19–20** — **the anchor.** Set-piece. The rope runs **upward**, and
  passes *within the veil* — the first thing in the book to cross it, and it
  crosses at exactly one point, which 10:20 will open. The forerunner is
  already inside. Engraved: SURE AND STEADFAST.

### Hebrews 7 (28 vv.) · 🌳 + 📊 — **break-away: the genealogy with the boxes missing**

Full frame leaves the column. This is a chart, and the strongest single
set-piece in the book.

- **vv. 1–3** — Melchizedek drawn as a standard house genealogy node — the
  vocabulary already exists in `generate_genealogy_svg.py` — but with **the
  parent sockets empty** and the lifespan bar running off both edges of the
  frame. *Without father, without mother, without genealogy, having neither
  beginning of days nor end of life.* Every other node in the frame has two
  parents and two ends. The name is glossed twice, by the text itself: *king
  of righteousness*, then *king of Salem*, which is *king of peace*.
- **vv. 4–8** — the tithe. A rank axis appears at v. 7 (*without any dispute
  the lesser is blessed by the greater*), and Melchizedek is above Abraham on
  it. v. 8 is two receipt columns: *here people who die receive tithes* —
  every entry closed by a death — *but there one receives tithes of whom it is
  testified that he lives* — one entry, open.
- **vv. 9–10** — **Levi in the body of his father.** Levi drawn as a small
  nested figure inside Abraham at the moment of the handover. The book's
  sectioning method again, and the chapter's best image.
- **vv. 11–19** — the change of priesthood forces a change of law. The twelve
  tribes as a row; only Levi's column carries an altar; the priest arrives out
  of **Judah**, *about which tribe Moses spoke nothing concerning priesthood*.
  v. 18 strikes the foregoing commandment out for *weakness and uselessness*;
  v. 19 — *the law made nothing perfect* — brings in a better hope, and the
  third *draw near*.
- **vv. 20–22** — two appointment documents: theirs unsealed (*made priests
  without an oath*), his sealed. WEB's *collateral of a better covenant* at
  v. 22 is a pledge lodged, not a person standing surety — draw it as a
  deposit.
- **vv. 23–25** — **the many priests.** A row of priest figures, each struck
  through, running off the frame edge — *hindered from continuing by death*.
  The text gives no number, so the drawing gives none; the row simply does not
  end on screen. Against it, one unstruck figure, *because he lives forever*.
  And *to the uttermost* is drawn as **reach**: the intercession line extends
  past the last struck figure in the row. Engraved: TO THE UTTERMOST.
- **vv. 26–28** — five fitnesses labelled — holy · guiltless · undefiled ·
  separated from sinners · *made higher than the heavens* — and that last one
  lifts the camera back onto the column for chapter 8. v. 27's *daily* against
  *once for all* is a small preview of 10:11–12; keep it small, the full
  treatment is three chapters away.

### Hebrews 8 (13 vv.) · 🏛️ — *the doubling declared*

The chapter that explains the frame.

- **v. 1** — *the main point*: the seat, drawn again at the top. Second sitting.
- **v. 2** — *the true tabernacle, which the Lord pitched, not man*.
- **vv. 3–5** — **the shadow.** The solid structure above; the light from the
  throne; the earthly tabernacle appearing on the ground below as its cast
  shadow, flat and soft-edged. v. 5's *pattern that was shown to you on the
  mountain* is drawn as the projection lines between them. Engraved: A COPY
  AND SHADOW.
- **vv. 6–12** — the new covenant: Jeremiah quoted at length as **one long
  voice arc**. Four provisions, each drawn: laws put into the mind and written
  on the heart (the Sinai tablet form dissolving into a heart outline) · *I
  will be their God, and they will be my people* · no one teaching his
  neighbour, *for all will know me, from their least to their greatest* · and
  the sins *remembered no more* — a record whose entries are not struck out
  but **absent**. Engraved at v. 12.
- **v. 13** — *becoming old and grows aged is near to vanishing away*. The
  shadow's edges soften for the first time. This is the seed of 12:27 and
  should be subtle enough that the payoff is a surprise.

### Hebrews 9 (28 vv.) · 🏛️ — *the tabernacle in section*

Maximum reuse: `generate_exodus2527_svg.py` and `generate_exodus26_svg.py`
already own this geometry, and the shadow layer *is* that drawing, flattened.

- **vv. 1–5** — the rooms furnished object by object, one per verse: lampstand,
  table, showbread · the second veil · golden altar of incense, the ark
  overlaid on all sides, the golden pot of manna, Aaron's rod that budded, the
  tablets · the cherubim of glory over the mercy seat. v. 5's *we can't speak
  now in detail* is a licence to stop labelling and let the drawing carry it.
- **vv. 6–7** — **the traffic diagram**, the chapter's best idea. The priests
  go into the first room *continually* — many paths, overlaid, worn into the
  floor. The high priest into the second **alone, once in the year, not
  without blood** — one thin path, dated. The frequency contrast is the whole
  argument and it is purely graphic.
- **vv. 8–10** — *the way into the Holy Place wasn't yet revealed while the
  first tabernacle was still standing*: the route is blocked **by the structure
  itself**. Counterintuitive and worth drawing exactly.
- **vv. 11–14** — the path relocates to the upper structure — *the greater and
  more perfect tabernacle, not made with hands* — and enters *once for all*.
  Two cleansing targets drawn, outer and inner: goats and bulls and heifer
  ashes reaching *the cleanness of the flesh*, blood of Christ reaching *your
  conscience*. Engraved at v. 12: ONCE FOR ALL.
- **vv. 15–22** — the **will and the testator**: an instrument that is *never
  in force while he who made it lives*. Then Moses' dedication — blood of
  calves and goats, with water, scarlet wool and hyssop, sprinkled on the book,
  the people, the tabernacle, the vessels. The sprinkling accumulates over
  four verses and then v. 22 states the rule the drawing has already made.
- **vv. 23–28** — the copies cleansed with these, *the heavenly things
  themselves with better sacrifices*. Then the closing parallel, which is a
  two-track diagram: *appointed for men to die once, and after this,
  judgment* / *Christ, offered once… will appear a second time*. The second
  track's return is drawn as a descent back down the column — the only one
  between 2:9 and 13:13, and it is a promise rather than a move.

### Hebrews 10 (39 vv.) · 📊 + 🏛️ — *the crossing*

Longest chapter but one; four sub-scenes.

- **vv. 1–4** — the shadow named a third time, and the repetition drawn: *the
  same sacrifices year by year, which they offer continually*. A cycle that
  never closes out — and v. 3's *yearly reminder of sins* means the ledger
  **accumulates** rather than clearing, which is the opposite of what a
  sacrifice is for.
- **vv. 5–10** — *a body you prepared for me*. v. 9 — *he takes away the
  first, that he may establish the second* — is drawn literally: the first
  arrangement lifted out of the frame, the second set into the gap.
- **vv. 11–14** — **the seated priest.** Set-piece, and the payoff of a
  frame-wide omission: *every priest indeed stands day by day*, a row of
  standing figures each repeating the same offering, in a structure that
  **has contained no seat since 1:3**. Then one who offered a single sacrifice
  and *sat down*. Third sitting. v. 13 places the footstool begun at 1:13.
  Engraved: HE SAT DOWN.
- **vv. 15–18** — the covenant quotation returns and **nothing new is
  engraved** — 8:12's line is already on the stone. Then v. 18: *where
  remission of these is, there is no more offering for sin* — and the altar in
  the lower structure goes out.
- **vv. 19–25** — **the crossing.** The single puncture of 6:19 opens: *a new
  and living way, through the veil, that is to say, his flesh*. Engraved.
  Then the three *let us* — draw near with a true heart, hold fast the
  confession, consider one another to provoke love and good works — drawn as
  **several** figures moving, not one, with the assembly of v. 25 forming and
  *the Day* appearing on the horizon.
- **vv. 26–31** — **fourth warning**, the severest. It lands because the altar
  is already out at v. 18: *there remains no more a sacrifice for sins*. The
  severity comparison of vv. 28–29 (Moses' law, on two or three witnesses,
  against *how much worse*), the three named offences, and then the floor
  opens. Engraved at v. 31: THE HANDS OF THE LIVING GOD.
- **vv. 32–39** — the recovery, as a ledger of what was lost against what is
  held: reproaches, oppressions, chains, *the plundering of your possessions*
  joyfully accepted — against *a better possession and an enduring one*. Then
  Habakkuk: *in a very little while, he who comes will come* — the horizon
  again — and two paths, *shrink back to destruction* and *faith to the saving
  of the soul*. The reader-figure takes the second, and walks straight into
  chapter 11.

### Hebrews 11 (40 vv.) · ⏳ + 🗺️ — *the road of pilgrims*

**Chapters 11 and 12 are one drawing.** The camera leaves the column for a
ground plane — but the city on the horizon is the top of that column, seen
from outside. Not a portrait gallery: a **road, walked**, by people who can
see where they are going and will not get there.

- **vv. 1–3** — faith as *assurance of things hoped for, proof of things not
  seen*: the city is drawn **solid** on the horizon while the road behind each
  figure fades. What is unseen is what is firm — the inversion is the point.
  v. 3's framing of the universe is a voice arc making ground.
- **vv. 4–7** — Abel's offering, and *being dead, he still speaks* — an arc
  rising from a grave, which 12:24 will answer. Enoch **leaves the road
  upward**, the only one who does. v. 6's principle interrupts the list and
  should interrupt the drawing. Noah's ship reuses the built Genesis 6–9
  geometry.
- **vv. 8–12** — Abraham *went out, not knowing where he went*; tents in a land
  not his own; and at v. 10 **the city is first drawn**, on the horizon, *which
  has the foundations, whose builder and maker is God*. Engraved. Then Sarah,
  and the stars and the sand of v. 12 — a deliberate rhyme with the Romans
  chapter-4 scene, which counted the same stars.
- **vv. 13–16** — **the hinge, and the reason for the whole design.** *These
  all died in faith, not having received the promises, but having seen them and
  embraced them from afar.* Draw the sightline from every figure to the city,
  long and unbroken. v. 15 draws the road **back** — the one they had time to
  take and didn't — unused. v. 16's *he has prepared a city for them* means the
  city is drawn **finished** while the road is still short. Engraved: A BETTER
  COUNTRY.
- **vv. 17–22** — Isaac offered and *figuratively* received back: a departure
  and a return on one line. Then three deathbed figures all facing forward down
  the road — Isaac blessing, Jacob *leaning on the top of his staff*, Joseph
  giving instructions concerning his bones. Joseph's bones are then **carried
  on** by the next figures, which is the road continuing itself.
- **vv. 23–29** — Moses. The scale at vv. 25–26 is the chapter's second-best
  image: *the treasures of Egypt* weighed against *the reproach of Christ*, and
  the reproach is heavier. He *looked to the reward* — the sightline to the
  city again. Then the Passover blood, and the Red Sea *passed through as on
  dry land*, where the Egyptians are the only figures on this road who do not
  come out.
- **vv. 30–31** — Jericho encircled seven days; Rahab, kept while the
  disobedient perish.
- **v. 32** — **the acceleration.** *The time would fail me* — six names in one
  breath, and the prophets. The road suddenly crowds and the drawing's pace
  visibly changes for one verse.
- **vv. 33–35a** — the victories, in the text's own order: kingdoms subdued,
  lions' mouths stopped, fire quenched, the sword escaped, *from weakness were
  made strong*, armies put to flight, the dead received back.
- **vv. 35b–38** — **the turn, and the passage most treatments skip.** *Others
  were tortured, not accepting their deliverance, that they might obtain a
  better resurrection* — then mocking, scourging, bonds, imprisonment, stoned,
  **sawn apart**, slain with the sword, in sheepskins and goatskins, destitute,
  afflicted, ill-treated. The road **goes below ground** here — *deserts,
  mountains, caves, and the holes of the earth* — while the city stays in
  sight above the horizon. And v. 38's parenthesis is drawn as an inversion:
  the world's line is put *below* the figures who are underground. Engraved:
  OF WHOM THE WORLD WAS NOT WORTHY.
- **vv. 39–40** — none of them received the promise. The road **stops short of
  the city**, and the gap is left visible on screen. *God having provided some
  better thing concerning us, so that apart from us they should not be made
  perfect* — the gap is not a failure, it is the place chapter 12 begins.

### Hebrews 12 (29 vv.) · 🏃 + 📊 — *the race, the mountain, the city*

Same drawing, continued.

- **v. 1** — the gap becomes the **track**. The pilgrims move to the verges and
  become *so great a cloud of witnesses*. Weights and *the sin which so easily
  entangles* are dropped on the line by the reader-figure. Engraved: THE RACE
  SET BEFORE US.
- **v. 2** — **the keystone of the whole design.** *Looking to Jesus* — the
  sightline every chapter-11 figure held toward the city now lands on a person;
  and he *has sat down at the right hand of the throne of God*, which is the
  seat drawn at 1:3, at the top of the column, unchanged. The road geometry
  and the column geometry fuse in one verse. Fourth and last sitting. Engraved:
  LOOKING TO JESUS.
- **vv. 3–11** — **discipline.** v. 4's *you have not yet resisted to blood* is
  a marker on the track showing how far the striving has gone against how far
  it could go — and chapter 11 has just drawn people who went the whole way.
  Then the two ledgers: *the fathers of our flesh*, who chastened *for a few
  days, as seemed good to them*, against *the Father of spirits*, *for our
  profit, that we may be partakers of his holiness*. v. 11 is a two-panel time
  strip: *for the present… not joyous but grievous* / *afterward… the peaceful
  fruit of righteousness*.
- **vv. 12–17** — the runners repaired and the track itself straightened —
  hands that hang down lifted, feeble knees, *straight paths for your feet, so
  what is lame may not be dislocated, but rather be healed*. Then the hazards
  beside it: falling short of grace, *a root of bitterness* drawn spreading
  **under** the track and defiling many, and **Esau**, who *sold his birthright
  for one meal* — drawn on the same scale that weighed Moses at 11:26, and
  weighed wrong. *He found no place for a change of mind though he sought it
  diligently with tears.*
- **vv. 18–24** — **the two mountains.** Full-frame set-piece, seven items a
  side, in the text's own order. Left, Sinai: *a mountain that might be
  touched* · burning with fire · blackness, darkness, storm · the sound of a
  trumpet · the voice of words the hearers *begged that not one more word
  should be spoken* · the animal that touches it stoned · Moses saying *I am
  terrified and trembling*. Right, Zion: Mount Zion, the city of the living
  God, the heavenly Jerusalem · innumerable multitudes of angels · the festal
  gathering and assembly of the firstborn enrolled in heaven · God the Judge of
  all · the spirits of just men made perfect · Jesus the mediator of a new
  covenant · *the blood of sprinkling that speaks better than that of Abel*.
  **The chapter-11 road arrives at the right-hand mountain** — this is the city
  those pilgrims were walking toward — and Abel's arc from 11:4 is answered
  here, thirteen chapters later, in the same frame. The voice thread closes.
- **vv. 25–29** — **fifth warning, and the frame resolves.** *See that you
  don't refuse him who speaks* — one last arc, and refusal drawn as an arc
  turned away. His voice shook the earth then; now, *not only the earth, but
  also the heavens*. And v. 27 — *the removing of those things that are shaken,
  as of things that have been made, that those things which are not shaken may
  remain* — **shakes the shadow layer off the bottom of the frame**. The copy,
  drawn as shadow since 8:5 and fading since 8:13, is gone. What remains is
  the solid structure and the city. Engraved at v. 28: A KINGDOM THAT CANNOT
  BE SHAKEN. And v. 29's *consuming fire* is the same fire that burned on the
  left-hand mountain at v. 18, now standing on the right.

### Hebrews 13 (25 vv.) · 💡 + 🗺️ — *outside of the gate*

The reversal. The frame is now single — no shadow — and the camera is at the
top. It spends the chapter coming down and going out.

- **vv. 1–6** — the practical charges as a small settled community at the foot
  of the structure: brotherly love continuing · hospitality to strangers, with
  an **unmarked angel drawn at the table** (*some have entertained angels
  without knowing it* — the drawing must not label it) · those in bonds
  remembered *as bound with them*, one chain across two figures · marriage held
  in honour · freedom from the love of money, with *I will in no way leave you,
  neither will I in any way forsake you* as a voice arc that simply **stays** —
  the only one in the book that does not resolve and vanish.
- **vv. 7–8** — the leaders remembered, *considering the results of their
  conduct* — the chapter-11 road returns as a short local stretch; these are
  the nearest pilgrims on it. Then **v. 8**, engraved: THE SAME YESTERDAY,
  TODAY, AND FOREVER — lettered beside the seat that has not been redrawn since
  1:3. The payoff only a per-verse book can earn.
- **vv. 9–14** — **the last move.** *We have an altar from which those who
  serve the holy tabernacle have no right to eat.* Then the ritual fact that
  drives it: the bodies of the sin offering are *burned outside of the camp*;
  therefore Jesus *suffered outside of the gate*; therefore *let us go out to
  him outside of the camp, bearing his reproach*. The camera drops below the
  camp line — the one region of the frame untouched since 2:9 — and the altar
  is drawn out there. v. 14 gives the reason and is engraved: NO ENDURING CITY
  HERE. *But we seek that which is to come* — the city is back on the horizon,
  and the road resumes. **The book ends walking, not arrived.**
- **vv. 15–19** — the sacrifices that remain, offered at the outside altar:
  praise, *the fruit of lips which proclaim allegiance to his name*, doing good
  and sharing. Then the leaders who *watch on behalf of your souls, as those
  who will give account* — an account drawn owing upward, back to the throne.
- **vv. 20–21** — the benediction. *The God of peace, who brought again from the
  dead the great shepherd of the sheep, with the blood of an eternal covenant.*
  The shepherd is the last figure drawn; the sheep are the readers; the way
  ahead is the road the pilgrims are on.
- **vv. 22–25** — the postscript stays small and plain: *I have written to you
  in few words* · Timothy freed · greetings to the leaders and the saints · *the
  Italians greet you* · grace. **Do not invent motion here.** The final mark is
  the road running off the frame edge.

---

## 6. Reuse, new work, and risks

**Reuse.** The shadow layer is `generate_exodus2527_svg.py` /
`generate_exodus26_svg.py` flattened — chapter 9 is close to free. The
priestly garments — 2:17 and the whole high-priest thread through chapter 10 —
come from **`svg_priest.py`**, written for Exodus 28 and factored out of it
for exactly this: `Form` places every garment on a body at any height, and
`ephod`, `breastplate_on`, `plate_on`, `turban` and `sash` are separately
callable, so Hebrews can vest a figure, half-vest it, or draw the pieces alone.
The genealogy node vocabulary in `generate_genealogy_svg.py` gives chapter 7
its Melchizedek chart. Noah's ship (11:7) comes from
`generate_genesis69_svg.py`; the seventh day (4:4) from the Genesis 1–2
panels; the speaker-arc device from `generate_genesis3_svg.py`; shared people
and objects from `svg_figures.py`, shared marks from `svg_vocab.py`.

**New work.** The projection-line construction that ties substance to shadow,
the two-mountain frame, and the pilgrim road. Also: `svg_priest.py` currently
draws in a single ink per garment, so the shadow key of §2 will want a muted
palette passed through it — the module takes its colours from the caller and
knows no palette, so this is a call-site change, not a rewrite.

**One thing Exodus 28 settled that Hebrews inherits.** The seated/standing
contrast of 10:11–12 depends on there being no seat anywhere in the earthly
sanctuary. Exodus 28's figure stands for all 43 verses and is never given
one — so the omission is already established in the built canon before
Hebrews spends it.

**Risks, in order of seriousness.**

1. **Chapters 9 and 10 sit in the same room for 67 verses.** The Romans
   post-mortem's stagnation finding applies directly. Mitigation is the
   sub-scene list above — 9 has four, 10 has six — but this is where the
   rendered review should look first.
2. **The shadow must stay legible in both themes.** A soft-edged monochrome
   mass under a lit structure is easy to lose on a dark ground. Decide the
   shadow's treatment against the palette before drawing anything else.
3. **The column is on screen for 303 verses.** It must not become the Romans
   rail. The defence is that it is not a table of contents — the camera moves
   within it, things are added to it, and it is destroyed at 12:27 — but the
   audit should confirm that no long run of verses leaves the drawing
   unchanged.
4. **Chapter 7 is a full break-away**, deliberately. Precedent: Acts 15–18
   steps aside from the map for five set-pieces. It should look like a
   different kind of drawing, and the return at 7:26 (*made higher than the
   heavens*) is what puts the camera back on the column.
5. **The BETTER thread could read as a tally.** Eleven marks, content-driven.
   If the rendered book reads it as a counter, cut it — the frame does not
   depend on it.

**Automated checks.** Same as Romans: a dev-only audit over all 303 generated
SVGs reporting overlapping text boxes, text wider than its box, text
off-canvas, and verses byte-identical to the previous verse. Target zero of
the first three; **no identical run longer than three verses**, watched
hardest across 9:1–10:39. (Built as `tools/audit_heb.py`, which checks
off-canvas text, overlaps and identical runs.)
