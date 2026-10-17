# Matthew 1 — visual ideas

> **Status (2026-08-20):** the live design is **the real Old Testament family
> tree**, not a made-up one — `matthew_tree.py` (grafts + the verse table),
> `svg_matthew_world.py` (camera over the tree, vv1-17),
> `svg_matthew_nativity.py` (figure stage, vv18-25), driven by
> `generate_matthew1_svg.py`. The fractal-tree design it replaced, and its
> 384 rendered files, are in `backups/matthew1_fractal_tree/`.
>
> **The finding that made it possible.** Abraham to Zerubbabel is ALREADY one
> unbroken parent-child chain on the welded tree that 1 Chronicles 1-9 is read
> against — thirty-six of Matthew's forty-two names, in Matthew's order, with
> Tamar and Ruth already standing as wives. Matthew adds fifteen nodes and not
> one of them is in the middle: Rahab, Bathsheba and Uriah at the side, and
> twelve in a tail hanging off Zerubbabel, which is to say off the end of the
> Old Testament.
>
> **What the real tree buys that a drawn one cannot.**
> - Verse 8 shows Ahaziah, Joash and Amaziah sitting UNLIT between Joram and
>   Uzziah, and verse 11 shows Jehoiakim between Josiah and Jechoniah. You
>   can see Matthew skipping, which is what his fourteens are made of.
> - Verses 13-16 run Matthew's tail down one column while Chronicles' own
>   post-exilic list (Hattush … Anani) runs down the next. The Old
>   Testament's line stops; this one keeps going.
> - Verse 12 draws the disagreement instead of hiding it: Zerubbabel keeps
>   Chronicles' father (Pedaiah) and a gold arc springs from Shealtiel, whom
>   Matthew, Ezra and Haggai give him.
> - No translation variants are needed any more. The boxes carry the Old
>   Testament's spellings with the chart's doubled label where they differ —
>   Jacob · Israel, Salma · Salmon, Jeconiah · Jechoniah, Azariah · Uzziah —
>   so one set of 25 files serves all eight translations (was 384 files).
>
> **What had to be fixed to make it read.**
> - The chart centres a parent over its children's whole span, which put Ruth
>   3,569 px from Boaz and Bathsheba 3,381 px from David. `_settle_wives`
>   nudges Matthew's women next to their husbands after layout.
> - The chart wraps a family too wide for one row, and rows after the first
>   hang below the whole HEIGHT of the row above — appending the tail put
>   Abiud a thousand pixels under Zerubbabel. It is inserted FIRST instead.
> - `focus_box` frames the arrivals in Chronicles; in Matthew every name in a
>   verse is equally the point, so it frames the whole lit set.
>
> **It uses the SPINE layout, not the wall chart's** (user, 2026-08-20, after
> the layout study in `_scratch/layout_lab.py`). `arrange_spine`/`place_spine`
> in `generate_ot_family_tree_svg.py` put the HEIR — the child carrying the
> widest descent — directly under its parent, instead of centring a parent
> over the whole span of its descendants. A line of descent is then a
> straight vertical column (median parent→child x-offset **0**, against 50).
> 1 Chronicles and the wall chart still use the centred layout; the spine
> costs BIRTH ORDER, since the heir goes first.
>
> What it bought Matthew 1:
>
> | | centred | spine |
> |---|---|---|
> | verses that must drop a name | 1 (Judah) | **0** |
> | v3 camera move | 1.61 oct / 3,224 px | **0.10 oct / 251 px** |
> | v2 camera move | 3.58 oct / 2,927 px | 2.76 oct / 1,475 px |
> | panorama rest scale | 0.080 | **0.141** |
> | total pan, vv2-16 | 10,698 px | **5,549 px** |
> | files | 1.4 MB | **0.8 MB** |
>
> Verse 17's panorama is the clearest gain: the gold thread is now a straight
> trunk with the tribes fanning off it, instead of a diagonal through a haze.
>
> **The two per-verse rules stay, and one of them no longer fires.**
> `_settle_kin` still recovers names the layout exiled — Zerah, Shealtiel and
> the three wives, all now within 220 px of their parent. `_afford` (drop the
> worst OUTLIER, never the front or back of the recital) is kept as a safety
> net but no verse needs it: Judah is the heir of Israel's descent, so under
> the spine he stands directly under Jacob at dx 0.
>
> **A mark draws itself once, on the verse it arrives.** `_appeared` /
> `_changed` read BEATS and nothing else (so a verse still renders alone).
> The bond is cut at verse 19 and verses 20-23 are all still severed — they
> were re-tracing the same two strokes across the stage four more times, and
> the prophet's quotation crossed twice.
>
> **Verse 25 is the manger, not a child.** `svg_figures.child()` is a child of
> seven and a newborn who can stand is not a newborn, so the birth is drawn as
> a manger with light coming out of it — `svg_figures.manger()`, new to the
> shared vocabulary. It is also the better picture: every other light in this
> chapter falls ON somebody from above, and this is the only thing on the
> stage that gives light instead of taking it. Note the manger itself comes
> from Luke 2:7 — Matthew 1:25 says only "her firstborn son".
>
> Concept stills for the older ideas below are in `mockups/matthew1/`.

---

## The chapter, and what makes it hard

Matthew 1 is the **opposite problem from Luke 3**. Luke was a 77-name slog in
one direction with no landmarks — it needed variety. Matthew has abundant
structure but the old design was **static**: three columns of fourteen, all 41
names on screen from verse 1, and a verse changed almost nothing. No journey,
barely any motion.

What the text itself supplies:

- Runs **forward** — Abraham to Jesus, the reverse of Luke.
- **v17 announces its own structure**: three sets of fourteen. (Fourteen is
  David's name in Hebrew — D-V-D, 4+6+4 — so the number is itself a claim.)
- The three sets are three **stations**: climbing to the throne, holding the
  throne, after the throne is gone.
- The **exile** is the hinge, named in both v11 and v12.
- **Five women**, four of them outsiders: Tamar, Rahab, Ruth, "the wife of
  Uriah" (Matthew pointedly will not name Bathsheba — he names the wronged
  husband), and Mary.
- The third set is historically **dark** — Abiud, Azor, Achim, Eliud and the
  rest appear nowhere else in scripture.
- **"and his brothers"** appears twice (v2 Judah, v11 Jechoniah) — the text
  itself points at the branches *not* taken.

### The back half, vv18-25 (previously unvisualised)

Coverage used to stop at v17. The Nativity half is where any whole-chapter
motif has to land, and it is richer than it looks:

- The angel opens with **"Joseph, son of David"** (v20) — the last private man
  in the list is addressed by the royal title the list just spent seventeen
  verses building. This is the hinge of the whole chapter.
- "conceived in her is **of the Holy Spirit**" (v18, v20) — the begetting chain
  breaks and the last link comes from above.
- "thou shalt **call his name Jesus**" (v21), **"Emmanuel — God with us"**
  (v23), and v25 Joseph performs the naming.
- The chapter's plot: **the begetting formula breaks at v16 and the naming
  repairs it.**

---

## A. One path through the tree ★ BUILT

Still: `mockups/matthew1/mockA_tree_path.png`

A deterministic fractal tree is the whole family of Abraham; one lit path
threading root-to-leaf is the line Matthew traces. The dim forks are literally
"and his brothers".

- The camera stays **wide** for the genealogy so the tree is always legible;
  the lit path advances a few forks per verse.
- **David** lands where the trunk first branches — the line rises straight
  through the patriarchs, and the dynasty begins to fork at the king.
- The **exile** is a break in the lit path: the line is cut, severed twigs
  fall, and what continues is a thinner shoot from the scar.
- The five **women** hang as short side-threads at their generation.
- **The transition:** the tree grew 41 generations by begetting, and then the
  final bud is opened by **light from above** — that beam is v18/v20's "of the
  Holy Spirit". The camera pushes in to the bud for vv18-25.
- **v20 pulls back out** so the whole David→Joseph stretch re-lights as the
  angel says "son of David", then v21 pushes back in. The camera move is the
  text's own move.
- Pairs with Luke 3: Luke **descends the root** of the same tree Matthew
  **climbs**. Deliberate diptych, same fractal family.

---

## Open decision: 41 names, 42 generations

Matthew claims three fourteens (42) but only **41 distinct names** appear —
Jechoniah has to be counted twice, closing the second set and opening the
third. The old three-column design handled this by putting 13 names in column
three. The built tree draws **41 nodes** with the break falling between
Jechoniah and Shealtiel, which sidesteps it visually; a six-sevens v17 frame
would show **42**, following Matthew's own stated count. Both are defensible —
they just must not contradict each other on screen.
