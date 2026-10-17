# Matthew 1 — the designs not built

> Split out of `docs/design/matthew-1.md` in the 2026-10 cleanup. The chapter shipped
> on the real Old Testament tree; these are the superseded fractal-tree status and
> the ideas that were considered and not built. Their concept stills are in
> `mockups/matthew1/` under the archive beside the repo (`config.ARCHIVE_DIR`).

## The fractal-tree design (2026-08-07, superseded)

> **Status (2026-08-07):** idea **A (one path through the tree)** is the live
> design — `generate_matthew1.py` (spec + geometry) and
> `generate_matthew1_svg.py` (drawing). The three-column list it replaced is
> preserved in `backups/matthew1_columns/`. Concept stills for every idea
> below are in `mockups/matthew1/`.
>
> Rebuilt same day after the first cut's Nativity half fell apart. Lessons
> that must survive any future rework:
> - **Interpolate the camera's VIEW (zoom + look-at), never its transforms.**
>   Tweening translate and scale independently swings the shot mid-move.
>   Zoom geometrically, look-at linearly, emit synchronized sampled value
>   lists (the Luke 3 dolly technique).
> - **Anything fastened to the tree lives IN the tree group** (the glow on
>   the bud, Mary's stem, the frail link) so camera moves carry it. Screen-
>   fixed overlays (beam, names) fade in only after the camera settles.
> - **The Nativity needs beats, not captions**: Mary's stem joins at v16/18,
>   Joseph's last link goes dashed through vv19-23, v20 pulls wide to relight
>   David→Joseph under "son of David", v24 redraws the link solid, v25 opens
>   the bud. The beam ends in a gradient tail, never a hard edge.

---

## B. The book of the genealogy

Still: `mockups/matthew1/mockB_book.png`

Verse 1 literally calls the chapter a *book* (βίβλος γενέσεως), so: a page
being written. Three scribal columns with tally brackets in the margin, the
women as glosses in brighter ink between the ruled lines, and at v16 the
formula visibly breaks — no "fathered", a mother's name, then the pen writes
THE name large. vv18-25 are the naming written out (v21 *Jesus*, v23
*Emmanuel*, v25 the naming completes the book's opening line).

- Most textually faithful of the three; pure names-and-numbers.
- In SVG the motion is **stroke-draw handwriting** — cheap and exactly right.
- **Pick this one if Matthew should look nothing like Luke.**

## C. Emmanuel — the stair ascends, the light descends

Still: `mockups/matthew1/mockC_emmanuel.png`

Two motions all chapter: the stair of generations climbs tread by tread
(dropping to a lower flight at Babylon) while a shaft of light descends. At
v16 they nearly touch; at vv18-25 they touch and the word is *God with us*.
The incarnation as geometry.

- Weakness: least specific to Matthew's own furniture — the fourteens and the
  women end up decorative — and the stair shares DNA with the throne profile.

---

## Earlier candidates (genealogy-only, no vv18-25 motif)

These were the first round, before the back half was considered. All have
stills in `mockups/matthew1/`.

### The throne profile

Stills: `mock1a_profile_kings.png`, `mock1b_profile_exile.png`,
`mock1c_profile_arrival.png`, plus the throne-line variants
`mock1d_no_throne_line.png`, `mock1e_throne_until_exile.png`,
`mock1f_throne_until_exile_kings.png`

An elevation chart: Abraham low, climbing to a crowned peak at David, a long
slide across the kings, a cliff at the deportation, a flat dark stretch, then
a rise at Jesus. **Shape and structure are the same thing** — set one is the
ascent, set two the plateau, set three the low road, so the terrain draws
v17's three fourteens without labelling them.

Resolved design problems, worth remembering if revisited:

- A labelled "the throne" rule spanning the chapter turns every height into a
  claim the data can't support (why is Manasseh above Jesse?). Two fixes were
  mocked: **drop the rule entirely** (terrain becomes shape, not scale), or
  **end the rule at the exile** and relabel it "David's throne" so it dies
  with the monarchy it marks. The latter was preferred.
- **Jesus must clear David.** The first cut had Jesus lower purely from an
  arithmetic slip (0.16 + 0.62 < 0.86). Matthew's case is "son of David"; the
  line should end at least as high as it peaked.

### Three turns of a spiral

Still: `mock2_spiral.png`

42 generations wound at fourteen per revolution, so the three sets are three
visually equal turns and the boundaries fall on one spoke. Proves its one idea
elegantly — but that is also its layout problem (the three most important
labels pile onto that spoke), and it tells you nothing about the story.

### The wall — built, broken, rebuilt

Still: `mock3_wall.png`

Each generation lays a stone; the wall rises, gains battlements through the
kings, shatters at the exile, is re-laid low, and Jesus is the cornerstone.
Strongest emotional beat at the exile, but as drawn it reads as graph paper
and wastes the frame. Would need real drawing craft to beat the alternatives.

### The five women as the spine

Still: `mock4_women.png`

Not a geometry — a re-weighting, layerable onto anything (and folded into A).
The fathers stay a uniform chain; the five women arrive from the side with a
tag: *Tamar. Rahab, of Jericho. Ruth, of Moab. The wife of Uriah. Mary.*
Too sparse to carry the chapter alone; free and valuable as a layer.

### Six sevens (a v17 treatment)

Still: `mock5_sevens.png`

Matthew's three fourteens are six sevens; the seventh opens at Christ. Almost
no drawing — counting made visible. **Use for verse 17 only**, which is
Matthew's own summary; it is not a chapter design.
