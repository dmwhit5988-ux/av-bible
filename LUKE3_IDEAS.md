# Luke 3 genealogy — visual ideas to revisit

> **Status (2026-08-06):** idea #1 (roots) is implemented as the live design —
> `generate_luke3.py` + `generate_luke3_svg.py`. The straight-road tracking
> camera it replaced is preserved in `backups/luke3_road/`; the serpentine
> original remains in `backups/luke3_journey/`. The other ideas below are
> unbuilt candidates, with mocks in `mockups/luke3/`.

The genealogy (Luke 3:23-38) remains one of the hardest sections to sit through:
sixteen structurally identical verses, ~77 names, running BACKWARD from Jesus to
Adam ("the son of God"). Two versions exist so far, both "travel along a line":

1. **Serpentine journey path** (preserved in `backups/luke3_journey/`) — the whole
   winding road visible at once, a bright segment sweeps further each verse,
   verse names in a side panel.
2. **Tracking-camera dolly** (current: `generate_luke3.py` + `generate_luke3_svg.py`)
   — one long straight road, the camera dollies along it, marker stays centered,
   minimap + "generation N of M" counter.

The ideas below change the *geometry* or the *metaphor*, not just the rendering.
Static mocks (verse 31, the verse that reaches David) are in `mockups/luke3/`.

---

## 1. Roots — whole-chapter tree motif ★ front-runner

Mock: `mockups/luke3/mock1_roots.png`

John's preaching already supplies the imagery: "the **axe is laid at the root**
of the trees" (v9), "bear **fruits** worthy of repentance" (v8), "raise up
**children to Abraham** from these stones" (v8), then "you are my beloved
**Son**" (v22) — and the genealogy answers *whose son, exactly?* all the way down.

- A tree above ground = Jesus; the genealogy is the camera descending the
  taproot through soil strata.
- Each era is a distinct stratum (kings' layer, patriarchs' layer, pre-flood
  layer, bedrock at Adam, light — not soil — at "of God").
- Names are nodes on the root; era landmarks bold with era word.
- **Progress signal:** the soil color around you tells you what age you're in —
  no minimap needed.
- **Whole-chapter payoff:** vv.1-20 reuse the same tree (fruit on branches, axe
  at the trunk), v22 the dove descends onto it, v23 the camera goes below ground.
- Motion: same continuous-dolly mechanics as v2, rotated vertical.

## 2. Tree rings — whole list visible, zero travel

Mock: `mockups/luke3/mock2_rings.png`

Cross-section of a great tree: Jesus at the center, each generation one
concentric ring outward, God the outermost ring that encloses everything.

- Era rings brighter, labeled with a tick outside the disc.
- Each verse ignites the next band of rings; camera gently zooms out.
- **Progress signal:** lit radius vs. full disc — glanceable, no counter needed.
- Most "at-a-glance" of all options; 77 rings genuinely reads as deep time.
- Risk: individual names are hard to place on rings — current batch shown along
  a spoke; non-era names otherwise anonymous rings.

## 3. Abraham's stars — the constellation promise

Mock: `mockups/luke3/mock3_stars.png`

"Count the stars… so shall your offspring be." A fixed night sky of 77 stars.

- Each verse the next batch flares; a faint line threads them into one
  constellation from Jesus back to Adam.
- Era ancestors are first-magnitude stars, always named; ordinary names appear
  while their verse reads, then fade to a bright dot.
- The finished chapter leaves one complete constellation hanging in the sky.
- Inverts the mood: the list becomes the promise being counted out, not a slog.
- Fixed camera → very cheap SVG (opacity/flare animations only).

## 4. Receding line of fathers — perspective depth

Mock: `mockups/luke3/mock4_fathers.png`

Same linear structure as v2 but in one-point perspective: a queue of standing
silhouettes, each with a hand on the shoulder of the one before, vanishing
toward a glowing horizon (the source, "of God").

- Camera flies past figures as each verse reads; passed figures slip behind.
- 70+ figures shrinking to a vanishing point conveys the vertigo of the
  timespan in a way a flat sideways road can't.
- The hand-on-shoulder chain is "son of… son of…" made literal.
- Risk: hardest to render well in flat SVG; silhouettes must stay abstract.

## 5. Upstream to the source — the other whole-chapter option

Mock: `mockups/luke3/mock5_river.png`

The Jordan unifies the chapter: John preaches at the river, Jesus is baptized
in it, then the genealogy is the river traced *upstream* — against the current —
past named confluences, until the water narrows to a spring welling out of
light: "of God."

- Era ancestors are major forks; ordinary names are small tributaries.
- Shares v2's dolly mechanics (code thinking carries over) but replaces the
  abstract road with a metaphor the chapter itself sets up.
- "Against the current" is exactly what reading a genealogy backward feels like.
- Note: introduces water blues into the sand/gold palette (visible in mock).

## 6. Cross-cutting tricks (usable with any design, incl. current)

The core pain is sixteen interchangeable verses. Two cheap differentiators:

- **Palette drift** — warm dawn tones at Jesus cooling to deep night-blue at
  creation (or reverse, brightening toward "of God"). Every verse gets its own
  color temperature; the hue itself says where you are.
- **Time-depth counter** — "~28 generations before Christ" instead of
  "generation N of M". Stay with generation counts, not BC years (pre-Abraham
  dates are speculative).

---

## Recommendation

**#1 (roots)** is the bet to beat the current version — the boring section
becomes the payoff of imagery John introduces in the same chapter, and the
strata give per-verse variety for free. **#2 (tree rings)** is the strongest
pure-genealogy option if the John-the-Baptist verses stay as they are.
