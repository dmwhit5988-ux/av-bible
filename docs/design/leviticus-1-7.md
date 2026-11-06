# Leviticus 1–7: the offerings table and its stations

The five offerings of Leviticus 1–7 as one comparison chart that fills in as
the law is read. Every verse is a camera over one sheet. That sheet holds the
Tabernacle reference page's court plan and five-column offerings table, both
drawn by the reference's own functions, and eleven screen-sized stations
around them for what a table cell can't hold: the altar, the parts of the
animal, the veil, the kitchen and the rest.

## Status: built (2026-11-06), the owner's review to come

The 163 files are in `web/visuals/Leviticus/1`–`7`, written by
`generate_leviticus17_svg.py --web`. QC refuses none of them, a fresh run
reproduces them byte for byte, and the deploy count is 6,774 of 20,000. The
build departs from the plan below in the ways listed under [As built](#as-built).

After the first build the owner found the camera moved too much ("it
constantly shifts around the graphic"). The camera was rebuilt around one
lens, described under [Camera and motion](#camera-and-motion): every rest is
at the same scale, so a move is a slide, not a zoom.
Where the two differ, the spec (`leviticus17_spec.py`) is right and the verse
plan tables are the design's draft.

A design panel drafted this: three verse inventories (1–3, 4–5, 6–7) and a
map of the code to reuse, then three independent designs (chart-first,
place-first, lean) and a critic who scored them and merged one. Chart-first
won (7.5), rebuilt on the lean design's chassis (7), with the place-first
design's paths and marks grafted on (6). The critic's claims about the code
were checked by hand: the sin column's five rank groups (`ranks()`), the
insets' Exodus captions (`panel()`), the begin-at-0 pulses
(`svg_surface._pulse_anim`), and every helper named below.

The owner answered the design's twelve questions on
2026-11-06 (see [Owner's decisions](#owners-decisions)). They chose one pass
for all seven chapters, a mountain for Sinai, no "without defect" chip, and
the `offerings.py` wording fixes in this build. The rest took the defaults.

## What it shows

- **The table is the spine.** The sheet starts with every unit of the
  offerings table under a veil: each entry, who-line, drawn thing, header and
  by-line. A unit unveils on the word of the verse that `offerings.py` cites
  for it, so the chart is complete by 7:37, the verse that sums it up. 7:37
  then lights the columns in the order it names them (burnt, meal, sin,
  trespass, consecration, peace).
- **The court plan is where things happen.** Tokens walk from the gate to the
  door (1:3) and to the north side of the altar (1:11). Blood is traced round
  the altar (1:5). The crop goes to the place of the ashes (1:16). The bull and
  the ashes are carried out through the gate to the clean place (4:12, 21;
  6:11).
- **The stations hold the detail**, each drawn on its word:
  - fire and wood laid in order on the altar;
  - fat taken from a labelled cutaway of the animal;
  - seven numbered drops before the veil;
  - blood on the horns and down the side;
  - the oven, griddle and pan;
  - the added fifth;
  - the peace offering's three days.
- **Nothing loops.** Everything plays once and holds. There is no prose on the
  graphic, only WEB names, numbers and labelled drawings.

## The sheet

All seven chapters share one world sheet, in world px, where 1 world px is
1 screen px at s=1.

### The plan

This is the reference's own court, tent and furnishings, drawn by
`generate_tabernacle_reference.draw_court`, `draw_tent` and
`draw_furnishings` at the reference's own coordinates (`sanctuary.Plan(730,
440, 14)`): court x 730–2130, y 440–1140, with east to the right. `draw_dims`
and `draw_camp` are not drawn. The Leviticus layer above it has:

- a dashed camp edge, not to scale;
- the **north side** strip of the altar, with the chip "north";
- the **place of the ashes** east of the altar: a `mound()` with the chip
  "place of the ashes";
- the **clean place** off the plan, past the camp edge: a mound, wood bars and
  a flame, with the chips "outside the camp" and "clean place";
- the blood ring round the altar; the blood path from the door to the veil
  line; the out path (altar, gate, clean place);
- beast and priest tokens as `<use>` at about 42 px; and Moses (`man()`)
  outside the gate for 1:1.

### The table

This is `generate_tabernacle_reference.draw_offerings`, unchanged, at its own
coordinates: x 2960–4910, y 1548–2824, five 360-px columns (burnt, meal,
peace, sin, trespass), with the rows BROUGHT, ON THE ALTAR, THE BLOOD, WHO
EATS, NOT EATEN and WHEN.

Each unit's veil is a PANEL rect at opacity 0.72 that fades to 0 on its cue.
The Leviticus generator computes the veils' boxes from the reference's own
`entries()`, `ranks()`, `OFF_ROWS`, `offer_columns()` and layout constants,
so the reference isn't refactored. The sin column's BROUGHT has five rank
groups (`ranks()` merges the anointed priest with the whole congregation, and
the common person with "one guilty of 5:1–4"), with seven who-lines. A
Leviticus-only "consecration" chip beside the trespass header comes in at
7:37.

### The stations

Each station is a 1024 × 576 PANEL card with no title, laid out at screen
size. The camera rests on a whole card at the lens (s 0.829), so the card
fills most of the screen with a margin round it. A station is written into a
file only if one of that file's rest cameras sees it.

The "Where" column below is the design's. As built, the cards sit in
`leviticus17_spec.STATIONS`: H and A under the plan, M and B under them, C,
D, G, S, T and K in two columns beside the table, and L far to the west.

| Station | Where | What it holds | Mainly for |
|---|---|---|---|
| **A** altar | under the plan's altar | `inset_altar` ×1.4 with overlays: fire, wood in two courses, a stack (pieces, head, fat, memorial, bird), blood on the two visible horns, a run down the side, a pool at the base, the ash heap. A bird bay (neck wrung, crop, wing tear), a day strip, the priest in linen (`svg_priest`) | 1:5–17; 4:7, 18, 25, 30, 34; 6:9–13 |
| **B** parts board | under A | one `beast_parts(kind)` cutaway (bull, sheep, ram or goat), chips on leaders in the margins; a sidebar with the altar and two priests for the shares | 1:6–13; 3:3–4, 9–10, 14–15; 4:8–11; 7:3–4, 30–34 |
| **C** cast | left of B | the verse's animal (`draw_thing`), the offerer with his hand on its head, `priest()` for Aaron's sons, the elders, the chips "male", "female", "young bull" | 1:2–4; 3:1–2; 4:3–4, 13–15, 22–24, 27–29 |
| **H** holy place | under the tent | the veil inset and `inset_incense` ×1.3: seven numbered drops before the veil, blood on the incense altar's horns | 4:5–7, 16–18 |
| **G** meal | under the burnt and meal columns | flour, oil poured, frankincense, the handful; a split bar ("memorial" / "Aaron and his sons"); first fruits parched and bruised; the "most holy" bracket; "every male" | 2:1–3, 8–10, 14–16; 6:14–18 |
| **K** kitchen | under the peace and sin columns | `cookware` oven, griddle and pan with cakes and wafers; a rules strip (yeast and honey with `not_mark`, salt with "covenant" lighting all five names at 2:13); a ten-part measure bar with the tenth split "morning" / "evening"; the earthen and bronze pots | 2:4–7, 11–13; 5:11; 6:20–23, 28 |
| **M** causes | above the table | a 2×2 of 5:1–4: witness, carcasses, uncleanness of man, oath ("evil", "good"); a "confess" arrow | 5:1–6 |
| **T** trespass | above the table, right | the horned ram; coins and scales with "shekel of the sanctuary"; the fifth bar; the six wrongs of 6:2–3 with return arrows | 5:14–19; 6:1–7 |
| **D** peace law | right of M | a bread shelf (four kinds) heaved to the priest; day 1, 2, 3; clean / unclean, "cut off" | 7:11–21 |
| **S** shares and bans | right of T | the priest's shares (the skin, the baked, "mixed with oil" / "dry"); the bans on fat and blood, "died of itself", "torn", "dwellings", "cut off" | 7:8–10, 22–27 |
| **L** Sinai | far outside the camp | a `mountain()` drawn in, "Mount Sinai", "wilderness of Sinai", and Moses | 7:38 |

The grid keeps the busiest chains next to each other: the plan's altar above
A, A above B, the tent above H, and the meal column above G and K.

A heads-up display (HUD) sits outside the camera. A title plate shows
"Leviticus <c>" until an offering is named, then the offering's WEB name
(`offerings.OFFERING[k].name`), and "the law" at 7:37–38. A "forgiven" chip
under it fades in on the word in the nine verses that say it (4:20, 26, 31,
35; 5:10, 13, 16, 18; 6:7).

## Camera and motion

- **One flight**: `svg_map_camera.Flight`, chained from 1:1 to 7:38. Each
  file starts where the last one ended, and all files are built in one run
  in canonical order. Each file lands at least 0.35 s before its MP3 ends
  (`svg_chronicles_world._mp3_seconds`). A verse under 5 s has one stop, up to
  10 s two, and three only above 10 s.
- **One lens.** Every rest is at `LENS` (s 0.829), except 7:37's whole
  table at 0.45. A move between two rests at the lens is a plain eased pan,
  so the zoom-out-and-swoop of a van Wijk flight happens only into and out
  of 7:37. The rests are named homes in `SHOTS`:
  - `P`, the court plan with the whole tent, and `O`, outside the gate;
  - the table's six homes, `TL1`–`TL3` (the row labels, burnt, meal and
    peace) and `TR1`–`TR3` (peace, sin and trespass), each a band of rows;
  - each station's whole card, named by its letter. Close-ups are retired:
    `shot_cam` refuses `<St>.<name>`.
- **Pace.** `lev_duration` times each leg from `cam_duration`, lengthened
  until the pan's eased peak is at most `PAN_PEAK_PX_S` (1300 px/s on
  screen), up to `PAN_MAX_D` (3.8 s). A zoom is held under `ZOOM_PEAK_PX_S`.
  A stop rests at least `DWELL` (1.3 s), and a file's last stop rests
  `LAST_REST` (1.5 s) counting the next file's hold. A short verse may
  squeeze a leg to `MIN_LEG_SQUEEZE`, but never so it peaks above
  `SQUEEZE_PEAK_PX_S`.
- **The movement budget.** QC refuses a rest off the lens (other than
  `LENS_EXEMPT`), a zoom between two lens rests, and a file over
  `MAX_LEGS` (3), `MAX_FILE_PAN` (5.5 screen widths) or `MAX_FILE_ZOOM`
  (1.2 octaves), or a leg over `MAX_LEG_PAN` (3 widths) or `MAX_PEAK_PX_S`
  (1800 px/s). It warns above 1300 px/s. `test_camera_is_calm` holds the
  book's totals: at most 150 legs, 200 widths of pan, 2.5 octaves of zoom
  and 26% of the narration spent moving.
- **As measured** (the first build in brackets): 148 legs (178), 25% of the
  narration moving (33%), 181 screen widths of pan (327.5), 1.8 octaves of
  zoom (87.2), 51 files that don't move (28), and 5.3 widths in the busiest
  file (9.0).
- **Cues**: a `lev_say`/`cue` pair copied from `garden_stage.say`/`cue`
  (which is bound to `BOOK = "Genesis"`), timed by `narration_clock` with
  the words-per-second estimate as fallback. A misspelt cue word fails the
  build.
- **The motion vocabulary**, all SMIL, played once with `fill="freeze"` and
  an explicit begin:
  1. *Reach*: a unit's veil fades 0.72 → 0 over 0.5 s. Later files leave the
     veil out.
  2. *First*: a new `pulse_at(points, begin)`, once, on the verse a thing
     becomes current. It's new because `SvgCanvas`'s pulses begin at 0 s.
  3. *Current again*: a steady outline faded in, with no pulse.
  4. *Draw-in*: `traced_el` for blood, cut lines, arrows, the pour and the
     brackets; `lift_in` or a fade for chips and figures; `grow_rect` for the
     fifth, the day bars and the tenth.
  5. *Tokens*: `animateTransform` for a beast to the door or the north side,
     the crop to the ashes, the bull and the ashes out of the camp, a handful
     to the fire, bread heaved, the breast waved once and the thigh lifted
     once.
  6. *Not*: `not_mark` traced over a forbidden thing.
- **State persists**: reached stays reached, drawn stays drawn. Where a cited
  verse can't afford the flight to its cell (6:11 ashes, 7:5 trespass fat,
  7:9 meal priest, 7:13 leavened bread, 7:31 breast), the unit is reached off
  camera, listed in `REACHED_OFFSCREEN`, and shown at full strength the next
  time a camera rests there.
- **Nothing is shown before it is said.** Reach overrides cover units whose
  first citing verse comes before the words: "burnt offering" at 1:3 (not
  1:2), "sin offering" at 4:3, the female goat or lamb at 4:32, salt at 2:13,
  the fifth at 5:16, "everyone who is clean" at 7:19, and the right thigh at
  7:33 (its row also cites 7:14, which is the cakes). The five WHEN cells are
  summaries, so they unveil together at 7:37.

## What is new

### Figures (in `svg_figures.py`, defaults byte-identical)

- `sheep(ram=False)`: `ram=True` adds curled horns and a heavier neck. The
  default returns today's ewe exactly, so Genesis, Hebrews, Zephaniah and the
  reference page don't change.
- `beast_parts(kind)` for a bull, sheep, ram or goat: a diagrammatic side
  view over the figure's dimmed silhouette. It is a diagram, not anatomy, and
  must stay clear and not gory. Its keyed parts can be pulsed, moved or
  outlined alone: skin, head, legs, the body, the pieces (cut lines), innards,
  the fat that covers the innards, the fat on them, the two kidneys and the
  fat by the loins, the liver and the cover on it, the backbone, the fat tail
  (sheep and ram), breast, right thigh, and the dung (bull). Each part has an
  anchor for its chip's leader. This is the largest new drawing.
- `cookware(kind)`: oven, griddle, pan and pot. The pot is drawn in clay for
  "earthen" and in bronze for "bronze" (6:28).
- `mountain()`: a plain labelled mountain for Sinai at 7:38, drawn in the
  house material style. There's no shared mountain yet (the garden's and
  Shiloh's hills are their own), and Exodus 19 on the backlog will want the
  same figure.
- `svg_vocab.not_mark()`: the one mark for what is forbidden or not eaten (a
  ring with one bar).

Existing stand-ins carry the rest: `basket` for fine flour, `cup` for
frankincense and salt, `bread()` for cakes, wafers and leavened bread,
`grass()` for first fruits, one `dove` for turtledove and pigeon, and `mound()`
for the ash heaps.

### Data

`PARTS`, `THINGS` and `THING_KEYS` are untouched, and the new tables are
additive. `OFFERINGS` changes only where its wording is corrected (below).

- **`sanctuary.PLACES`**, a table kept outside `PARTS` (the reference sidecar
  loops over `PARTS`):
  - `ash_place` east of the altar (1:16; "east" is stated, the distance isn't,
    so the point is DERIVED; 6:10's "beside the altar" is DERIVED);
  - `north_side` of the altar (1:11 STATED for the flock; DERIVED for "where
    they kill the burnt offering" in 4:24, 29, 33; 6:25; 7:2);
  - `clean_place` outside the camp, off the plan, direction NOT_GIVEN (4:12,
    21; 6:11).
- **`offerings.CUTS`**: the parts in WEB wording, keyed to `beast_parts`, each
  with its verses and the beasts it applies to.
- **`offerings.RITES`**: who lays a hand on the head, where it's killed and
  who acts, each with its ref and flag (1:4–7, 11, 15; 3:2, 8, 13; 4:4, 15, 24,
  29, 33; 5:8; 6:25; 7:2).
- **Small boards**: `CAUSES` (5:1–4), `WRONGS` (6:2–3), `BREADS` (7:12–13),
  `DAYS` (7:15–18), `VESSELS` (2:4–7; 6:21, 28; 7:9), `FORGIVEN`,
  `MOST_HOLY`, `ONE_LAW` (7:7), `PENALTIES` ("cut off", 7:20–27),
  `LAW_ORDER` (7:37) and `SINAI` (7:38).

### Wording fixes in `offerings.py`

The verse inventories checked every row against the WEB. These fixes go in
first, because the table shows them on both the verse pictures and the
reference page (the owner's decision 8):

- **The sin offering's ranks**: "the poor" and "the poorest" become "can't
  afford a lamb" (5:7) and "can't afford two birds" (5:11), the text's own
  terms.
- **The burnt offering's WHO EATS**: "no one" is flagged DERIVED. The text
  says the priest burns "all of it" (1:9, 13), not that no one eats it.
- **The meal offering's ON THE ALTAR**: the handful with all its frankincense
  cites 2:2 and 6:15. 2:9 is cited only for the baked kinds' "memorial",
  since it names no handful and no frankincense.
- **The sin offering's blood at 4:18**: "the altar which is before Yahweh,
  that is in the Tent of Meeting" gets its own entry, flagged DERIVED. Only
  4:7 names the altar of sweet incense.
- **"which is by the loins"**: the fat by the loins is added where the text
  says it, in the peace offering (3:4, 10, 15), the sin offering's bull (4:9)
  and the trespass offering (7:4). So is 3:9's "close to the backbone".
- **The same pass** also fixes these:
  - the sin offering's WHEN: "made known to him" cites 4:14, 23 and 28, not
    4:2;
  - the burnt bird's crop goes "in the place of the ashes" (1:16);
  - 2:11's yeast and honey are worded as the text has them: no meal offering
    is made with yeast, and no yeast or honey is burned;
  - the priests' own meal offering is "in a griddle" and "in the day when he
    is anointed" (6:20–21);
  - the trespass offering's silver is flagged DERIVED;
  - the module docstring's peace offering range agrees with `law_ref`.

`test_sanctuary`'s pins on `OFFERINGS` are updated to match. Omissions the
inventories found (the parts, the places of killing, the vessels, 5:1–4's
causes, 6:2–3's wrongs, 6:27–28, 7:12's third bread, the "cut off"
penalties) go in the new tables, not in the rows.

### The reference changes

`generate_tabernacle_reference.thing_parts` maps "ram" and "male sheep" to
the horned sheep, so the table and the trespass station agree (decision 1).
With the wording fixes, that regenerates `reference/Tabernacle.svg`,
`.json` and `.html` deliberately. The diff must touch only the ram icons and
the corrected offering text and cards.

## Files

| Kind | Files |
|---|---|
| New | `generate_leviticus17_svg.py` (the sheet, the stations, the flight, QC; import-safe), `leviticus17_spec.py` (shots, stations, all 172 verses, ranges, reach overrides, `EXCUSED`, `REACHED_OFFSCREEN`; data only), `test_leviticus17.py` (added to the CLAUDE.md test list) |
| Edited | `svg_figures.py`, `svg_vocab.py`, `offerings.py`, `sanctuary.py`, `test_sanctuary.py`, `generate_tabernacle_reference.py` (`thing_parts` only), `svg_generators.json` (one Leviticus 1–7 family) |
| Regenerated | `web/visuals/reference/Tabernacle.svg`, `.json`, `.html` (the ram icons and the corrected wording) |
| Output | `web/visuals/Leviticus/1`–`7/`: 154 verse files and 9 range files, 163 in all |

The nine ranges pair a verse with a speech formula ("Yahweh spoke to Moses,
saying") or a pure restatement, so no range shows a later verse's words early
(D17 plays a range's motion from the start): 5:13–14, 5:18–19, 6:7–8,
6:18–19, 6:23–24, 7:21–22, 7:27–28 and 7:35–36 fold the formula or
restatement into the verse before it. 4:1–2 is the other way round: a 2.2 s
formula and then the first sin offering verse, which lights nothing until
"sin offering" is said at 4:3, so that file carries a camera move only. The deploy goes from 6,611 files today
(`count_deploy_files()`, with the Leviticus audio and the unpublished Acts 6–7
in the tree) to about 6,774 of 20,000.

## Checks

The generator refuses to write a file that fails any of these:

- it lands at least 0.35 s before its MP3 ends;
- no text overlaps, overflows or leaves the canvas, at rest or mid-flight;
- at most about 1,050 rects and 268 texts, with figures in `<defs>`/`<use>`;
- no clip, mask or filter inside the camera group;
- every `offerings.py` row and thing ref in Lev 1–7 lights its unit, or is in
  `EXCUSED` or `REACHED_OFFSCREEN` with a reason;
- every unit is reached by 7:37;
- every verse 1:1–7:38 has a spec entry.

`test_leviticus17` checks:

- every verse is covered;
- every cue word occurs whole in its WEB verse;
- only the nine ranges exist;
- each veil box contains its unit's text anchor, so a change to
  `draw_offerings` can't leave the veils adrift;
- the module imports safely.

`test_sanctuary` gains checks that every new ref parses and lies in Lev 1–7,
that `PLACES` keys aren't `PARTS` keys, that every `CUTS` key is a
`beast_parts` anchor for each beast it names, and that labels are four words
at most.

The inset drawers carry their own Exodus titles ("THE BRONZE ALTAR / acacia
wood overlaid with brass"). On a Leviticus verse those would be caption
lines, so a `FilteredLayer(SvgLayer)` drops `panel()`'s frame and its two
texts and leaves `generate_tabernacle` untouched. Both elevations draw only
two horns, so blood goes on the two visible horns. Only the plan's four horn
dots show all four.

## Risks

- **Short verses.** 4:1 and 6:1 are 2.2 s; 1:6, 4:19 and 7:1 are 3.7 s;
  3:12 and 6:29 are 4.0 s. Their flights must be short. The fallback is to
  hold the last shot.
- **Long flights.** M, T, D and S sit top right and A, B, H and C bottom
  left. 5:1, 5:15, 7:8 and 7:38 cross the sheet and need a mid-flight
  readability and size check.
- **The plan's own labels** are about 9–13 px at the court shot (s 0.7). They
  read at the door and altar shots. The Leviticus chips use inverse font with
  `em_tick`.
- **Byte-identity.** `sheep()`, `dove()` and the `generate_tabernacle` insets
  must not change. Check Exodus 25–27 against `render_verse_svg`, and check
  the reference `build_svg()` differs only in the ram icons and the corrected
  wording.
- **The reference table's layout.** The corrected wording changes some cell
  heights (the rank labels, the "by the loins" lines), and so the table's
  row heights. The veils are computed from the same constants, so they follow.
  The reference page's own layout needs a look once it's regenerated.
- **Weight.** The heaviest frames are B with A, and the sin BROUGHT cell
  (five groups, seven figures). Culling with `visible_world`, `<use>` and the
  caps are required. The target is 30–70 KB a file.
- **Timing.** `narration_clock` times words inside a long clause by letter
  share (3:4, 3:9, 4:35, 7:4, 7:12), so a part may light a few tenths early
  or late.
- **WebKit in `<img>`.** Em offsets under an animated font size need
  `em_tick`, and tspans need explicit baselines. Test the way the app plays
  them, in Playwright WebKit outside the repo.
- **Scale.** The owner chose one pass for all seven chapters, eleven stations
  and all the tables. `beast_parts` is the piece most likely to need a second
  look, so it is rendered for the owner in step 2, before the generator
  depends on it.
- **`svg_figures.py` has uncommitted edits** from the Acts 6–8 work in this
  checkout. The figure step waits until that lands.

## Owner's decisions

Taken 2026-11-06.

| # | Question | Decision |
|---|---|---|
| 1 | Horned ram on the reference page too? | **Yes, both.** The table and the verse pictures match. |
| 2 | Cutaway labels up to four WEB words ("fat that covers", "by the loins", "cover on the liver", "right thigh")? | **Yes, up to four words.** |
| 3 | Where is "outside the camp" (4:12, 21; 6:11)? | **East, past the gate**, beyond a dashed camp edge that isn't to scale. |
| 4 | A mark for Yahweh speaking at 1:1? | **No mark.** Moses and the labelled tent only. |
| 5 | A "forgiven" chip on the nine verses that say it? | **Yes, the chip.** |
| 6 | 4:15's elders, whose number isn't given? | **Two figures and an "elders" chip.** |
| 7 | Stand-in icons or about six new ones? | **Keep the stand-ins.** |
| 8 | Fix the `offerings.py` wording now or later? | **In this build** (see [Wording fixes](#wording-fixes-in-offeringspy)). |
| 9 | Nine range files, or one file for every verse? | **Nine ranges, 163 files.** |
| 10 | 7:37–38: chips only, or a mountain too? | **A mountain too.** The consecration stays a name chip. Sinai gets `mountain()` with its chips and Moses. |
| 11 | A "without defect" chip wherever a verse says it? | **No chip.** The narration carries it, and the verse plan has none. |
| 12 | One pass, chapters 1–5 first, or trimmed? | **All of 1–7 in one pass.** |

## Build order

1. **Data.** The `offerings.py` wording fixes, with `test_sanctuary`'s pins
   updated; `sanctuary.PLACES`; `offerings.CUTS`, `RITES` and the boards; the
   new `test_sanctuary` checks. Run the CLAUDE.md test list and confirm
   `THINGS` and `PARTS` are untouched.
2. **Figures.** `sheep(ram=)`, `beast_parts`, `cookware`, `mountain`,
   `not_mark`. In the scratchpad, assert `sheep()` and `sheep(lamb=True)`
   match HEAD, and render the new drawings for the owner to see.
3. **The reference page.** Map the ram, then diff `build_svg()` in memory
   against the published sheet. Only the ram icons and the corrected wording
   may differ. Check the table's layout, then regenerate.
4. **The generator skeleton**, writing to the scratchpad only: the sheet, the
   places layer, the stations and filtered insets, the veils, the shots,
   cues, `pulse_at`, the flight, culling, the HUD and QC. Render four probes:
   1:5, 3:4, 4:7 and 7:37.
5. **WebKit** on the probes, played in real time in an `<img>`.
6. **The spec** for all 172 verses, the reach overrides, `EXCUSED` and
   `REACHED_OFFSCREEN`, and `test_leviticus17` passing.
7. **Generate** the 163 files in order, add the `svg_generators.json` family,
   run `build_manifest.py`, and check `count_deploy_files()`.
8. **One review**: the QC report, then WebKit on the tight verses (1:6, 4:19,
   7:1) and the long flights (5:15, 7:8, 7:38).
9. **Docs and commit**: this record, a Leviticus 1–7 section in
   `docs/visuals.md`, and the content-catalog entry marked Built. Run the
   tests, commit locally, and ask before pushing.

## As built

- **Modules.** The stations are split across four modules: `leviticus17_stations.py` (the Station API, and A, B, C and H), `leviticus17_st_meal.py` (G and K), `leviticus17_st_law.py` (M and T) and `leviticus17_st_peace.py` (D, S and L). The generator holds the sheet, the flight, the carry, the size passes and QC.
- **Veils.** The veils are opaque, with placeholder bars where the text will be, not a 0.72 PANEL. A veil that stays for a whole file is drawn as three shapes.
- **Cases.** `CASES` in the spec marks each new beast or bringing (1:3 herd, 1:10 flock, 1:14 birds, and so on). The altar's stack, bird bay, blood, priest and day strip, the cast's slots and K's struck marks belong to their case, so one offering's marks don't carry into the next.
- **Board B** is scoped to its offering and beast: `offering_of`, and `pkey` is given the file's ref. A part keeps the words of the verse that first named it (`CUT_WORDS`: "fat on the inwards" for 3:9, "the fat tail" for 7:3).
- **The carry.** What the previous file drew and this one doesn't (a pulse still running, a part B moved, D's meat) is drawn into the first frame and fades as the camera first moves. Parts that B moved stay where they were moved (`B.at:`, `B.up:`).
- **The carry of drawn pieces.** A station's standing pieces (`Station.base_pieces()`, such as A's bay dove) are pieces, not the card's base, so the carry holds them across a seam.
- **The opening hold.** A file holds its opening camera until the previous file's last stop has rested `LAST_REST` (1.5 s), where the verse can afford it.
- **Merged stops.** 1:17 and 6:5 had two stops on the same card at the lens; each is one stop, with the beats at their old times.
- **Table stops dropped.** Where the verse can't afford the table stop, the unit is reached off camera (`REACHED_OFFSCREEN`): 1:5, 1:15, 2:4, 3:9, 4:10, 4:25, 5:9 and 7:30. 2:3 and 2:14 are reordered instead. 1:10 goes to C first (the ram on "sheep", the goat on "goats"), then to the cell on "male".
- **Walks dropped** because the verse is too short for them: the ox at 4:14, the goat at 4:24 and the thigh carried at 7:33.
- **Shots.** The `table` shot is 158 px right of the design's, so that 7:37's "consecration" chip fits right of the trespass header. The homes' bands are placed so that no table word is cut by the frame or sits under the title plate.
- **At the lens.** The plan's tokens carry chips at world size 14 with a halo ("male", "crop", "meal offering"), so they read at the lens. "place of the ashes" sits east of the heap, clear of the altar and the north box.
- **Table headings.** `ref_world()` leaves out the table's "THE OFFERINGS" and "Leviticus 1–7" on the verse pictures.
- **The HUD.** The title plate changes to "burnt offering" at 1:3 and "trespass offering" at 6:6. The old title fades out before the new one fades in.
- **Wording on the verse pictures.** `ref_world()` drops the WHEN cells' source flags. 2:13's names are one chip, "all your offerings".
- **QC beyond the design's checks.** The generator also refuses a file if:
  - text is cut by the frame at rest, including the reference plan's own labels (`plan_labels_cut`);
  - an animation begins after the narration.

  It also holds the movement budget (see [Camera and motion](#camera-and-motion)).
- **Size.** The size passes are `compact`, `CamOut` keyframes, `cull_card` and shared figures in `<defs>`. Files run 7–124 KB, 43 KB on average and 7.17 MB in all. Twenty are over 70 KB, because the wider lens shows more of the table at each rest. The heaviest, 7:37 and 7:38, are mostly the reference table's own drawings.
- **Left as it is.**
  - 7:37 rests on the whole table at s 0.45, which is small on a phone.
  - At the lens, the table's text is about 11.6 px on a 1024-wide screen and the plan's own labels 10.8 px; the altar on the plan is about 60 px wide.
  - At the TR homes the row labels are off screen, so a lit sin or trespass cell has no row name in frame.
  - Six verses end on a table cell lit on arrival and the next verse flies straight back (7:8, 7:10, 7:18, 4:7, 5:12, 5:13–14). They are the fastest legs, up to 1,750 px/s.
  - T's top band is cut by the frame at 6:1–5 (drawings only, no words).
  - Text on a moving token isn't measured by QC.
  - These targets weren't built: the 4:20 "=" bracket, plan hand-marks, the 6:14 basket, the 7:34 arrows, the 3:11 tail slab, and chips for "anointed priest" (6:22) and "peace offerings" (4:10, 4:26).
- **Checked.**
  - Edge rest-frame contact sheets of all 163 files (211 rests), and the seams between them: 0 of 162 pairs over 100 px.
  - Playwright WebKit, played in an `<img>`, on the squeezed, merged and P files: every rest matches its paused frame.
  - `test_leviticus17`: 29 tests, including `test_camera_is_calm` and `test_a_pan_is_paced`.

## Verse plan

The design's plan. The spec is the build; see [As built](#as-built).

Each row is one file. "Shot" is where the camera rests (→ marks a flight
between stops). "Lights" is what comes in, and on which word.

### Leviticus 1

| Verse | Shot | Lights | Motion |
|---|---|---|---|
| 1:1 | plan:court → plan:tent | The tent outline pulses on 'Tent of Meeting'. The 'Moses' token fades in by the gate on 'Moses'. HUD 'Leviticus 1'. | The opening zoom from the whole court into the tent, landing 0.35 s before the end of a 4.5 s verse. |
| 1:2 | col(burnt) → C | burnt by-line 'anyone' unveiled on 'anyone'. On C, ox fades in on 'herd'; male sheep and goat on 'flock'. The burnt header stays veiled: not yet named. | Down to the table, then across to the cast station. |
| 1:3 | cell(burnt,brought) → plan:door | Header 'burnt offering' unveiled on 'burnt offering'. 'herd, a male' and the bull icon unveiled on 'herd'/'male'. On the plan, the ox token walks gate→door on 'door', with the token chip 'male'. | Two stops; the token translates along a traced path. |
| 1:4 | C.head | The offerer fades in. hand('rest') settles on the ox's head on 'hand', and the head outline pulses once. | Close-up at s 1.8. |
| 1:5 | plan:altar → cell(burnt,blood) | 'Aaron's sons' priest tokens fade in on their name. The blood ring is traced side by side round the altar on 'around'. 'around the altar' unveiled on landing. | Two stops. |
| 1:6 | B (bull) | The skin outline pulses with the chip 'skin' on 'flay'. Cut lines are traced and the chip 'pieces' appears on 'pieces'. | One quick leg (3.7 s verse). |
| 1:7 | A | Flames grow on the hearth on 'fire'. Wood bars lift in course by course on 'wood'. Chips 'fire' and 'wood'. | One stop. |
| 1:8 | A.fire | Slabs 'pieces', 'head' and 'fat' are laid on the wood, each on its word. | Push in to the hearth. |
| 1:9 | B (bull) → A.fire → col(burnt) lower rows | Innards and legs pulse on their words, and water lines are traced on 'water'. The fire flares on 'burn'. On landing, 'the whole' (burns) and 'no one' (eaten) are unveiled. | Three stops (11.5 s). |
| 1:10 | C → cell(burnt,brought) | Horned male sheep on 'sheep' and male goat on 'goats'. Chip 'male'. 'flock, a male' and the two icons are unveiled on landing. | Two stops. |
| 1:11 | plan:altar | The north strip pulses with the chip 'north' on 'north'. The sheep token moves to it. The blood ring is current (steady) on 'around'. | One stop. |
| 1:12 | B (sheep) → A.fire | Cut lines are traced on 'pieces'; head and fat pulse. Slabs are laid on the wood on 'in order'. | Two stops. |
| 1:13 | B (sheep) → A.fire | Innards and legs, with water traced on 'water'. The chip 'the whole' appears on 'whole' and the fire flares on 'burn'. | Two stops. |
| 1:14 | cell(burnt,brought) | Turtledove and pigeon icons and 'turtledoves or young pigeons' unveiled on their words. | One stop. |
| 1:15 | A.bird → cell(burnt,blood) | The neck mark is traced on 'wring' (head off). The bird goes onto the fire on 'burn'. A red run is traced down the altar's side on 'side'. 'the altar's side' unveiled on landing. | Two stops; the A.bird frame shows the altar's right face. |
| 1:16 | plan:altar | The 'crop' token moves east from the altar on 'east'. The ash-place mound and the chip 'place of the ashes' fade in on 'ashes'. | One stop. |
| 1:17 | A.bird → A.fire → cell(burnt,burns) | The wing tear line is traced on 'wings', with the chip 'not divided'. The bird goes onto the wood and the fire flares on 'burn'. 'the whole bird' unveiled on landing. | Three stops (13.4 s). |

### Leviticus 2

| Verse | Shot | Lights | Motion |
|---|---|---|---|
| 2:1 | col(meal) | Header 'meal offering' and 'anyone' unveiled on their words. Icons: fine flour on 'fine flour', oil on 'oil', frankincense on 'frankincense'. The entry 'flour, oil, frankincense' is unveiled. HUD 'meal offering'. | Pan one column. |
| 2:2 | G → A.fire → cell(meal,burns) | Basket, jar and cup are present. hand('cup') closes on 'handful'. The split bar's 'memorial' end lights on 'memorial'. The handful token lands on the fire on 'burn'. 'a handful' unveiled on landing. | Three stops (15.9 s). |
| 2:3 | G → cell(meal,eaten) | The rest of the split bar grows as 'Aaron and his sons' on "Aaron's". A 'most holy' bracket stub with 'meal offering' on 'most holy'. 'the priests' unveiled on landing. | Two stops. |
| 2:4 | K.cook → cell(meal,brought) | The oven is drawn in on 'oven'. Bread chips 'unleavened cakes' and 'unleavened wafers' on their words. 'cakes or wafers' and the cakes and wafers icons are unveiled on landing. | Two stops. |
| 2:5 | K.cook → cell(meal,brought) | The griddle with a flat round on 'griddle'; chip 'mixed with oil'. 'from the griddle' unveiled on landing. | Two stops (6.9 s). |
| 2:6 | K.cook (griddle close) | Cut lines across the round on 'pieces'; oil traced on 'oil'. | One stop (4.2 s). |
| 2:7 | K.cook → cell(meal,brought) | The pan is drawn in on 'pan'. 'from the pan' unveiled on landing. | Two stops; QC holds the landing. |
| 2:8 | plan:door | A bread token passes from the offerer to a priest token on 'priest'. The priest walks to the altar on 'altar'. | One stop; tokens translate. |
| 2:9 | A.fire | The 'memorial' slab lands on the fire on 'memorial', and the fire flares on 'burn'. | One stop. |
| 2:10 | G → cell(meal,eaten) | 'Aaron and his sons' on the split bar is current. 'the priests' is current. | Two stops. |
| 2:11 | K.rules | Chips 'yeast' on 'yeast' and 'honey' on 'honey'. not_mark traced over both on 'burn no'. | One stop. |
| 2:12 | K.rules | The chip 'first fruits' on 'first fruits', with arrows traced from yeast and honey. The struck arrow to the altar stays. | Hold with a small pan. |
| 2:13 | K.rules → cell(meal,brought) | The cup 'salt' on 'salt'; the chip 'covenant' on 'covenant'. The five offering names light in turn on 'all your offerings'. The salt icon and 'salt, no yeast' are unveiled on landing. | Two stops. |
| 2:14 | G.fruits → cell(meal,brought) | Ears with 'first fruits'. A flame under them on 'parched'; the chip 'bruised' on 'bruised'. 'parched grain' and the first-fruits icon are unveiled on landing. | Two stops. |
| 2:15 | G.fruits | Oil traced on 'oil'; the frankincense cup on 'frankincense'. | One stop. |
| 2:16 | G.fruits → A.fire → cell(meal,burns) | A 'part' token splits off on 'part', with the chip 'all its frankincense'. It lands on the fire on 'burn'. 'part of it' unveiled on landing. | Three stops (10.4 s). |

### Leviticus 3

| Verse | Shot | Lights | Motion |
|---|---|---|---|
| 3:1 | col(peace) → C | Header 'sacrifice of peace offerings' on 'peace offerings'. 'anyone', the herd icon and 'male or female' unveiled on 'herd'/'male'. On C, the ox with the chips 'male' and 'female' on their words. HUD title changes. | Two stops. |
| 3:2 | C.head → plan:door | Hand on the ox's head on 'hand'. The ox token at the door on 'door'. The blood ring is current on 'around'. | Two stops. peace.blood is unveiled at 3:8. |
| 3:3 | B (bull) | fat_cover pulses with its chip on 'covers', then fat_on on 'all the fat'. | One stop. |
| 3:4 | B.inner | 'two kidneys' with the numeral 2 on 'kidneys'. 'by the loins' on 'loins'. 'cover on the liver' on 'liver'. | Push in to s 1.7. |
| 3:5 | A.fire → cell(peace,burns) | The 'burnt offering' slab is current on 'burnt offering'. Fat slabs are laid on top on 'burn', over wood and fire. 'the fat' unveiled on landing. | Two stops. |
| 3:6 | C | Lamb and goat on 'flock'; chips 'male' and 'female'. | One stop. |
| 3:7 | cell(peace,brought) | The lamb icon and 'a lamb' unveiled on 'lamb'. | One stop (4.5 s). |
| 3:8 | C.head → cell(peace,blood) | Hand on the lamb's head on 'hand'. peace 'around the altar' unveiled on 'around'. | Two stops. |
| 3:9 | B.tail (sheep) → cell(peace,burns) | tail_fat pulses on 'tail fat'. The cut line is traced at 'backbone'. fat_cover and fat_on light on 'inwards'. 'the fat, the tail' unveiled on landing. | Two stops (14.4 s). |
| 3:10 | B.inner | Kidneys, 'by the loins' and 'cover on the liver' in turn. | One stop. |
| 3:11 | A.fire | Fat slabs, the tail among them, on the fire on 'burn'; the chip 'food' on 'food'. | One stop. |
| 3:12 | cell(peace,brought) | The goat icon and 'a goat' unveiled on 'goat'. | One stop (4.0 s). |
| 3:13 | C.head → plan:door | Hand on the goat's head on 'hand'. The goat token before the tent on 'Tent of Meeting'. The ring is current on 'around'. | Two stops. |
| 3:14 | B (goat) | fat_cover, then fat_on, on their words. | One stop. |
| 3:15 | B.inner | Kidneys, 'by the loins' and 'cover on the liver'. | One stop. |
| 3:16 | A.fire | Fat on the fire on 'burn'. The chips 'all the fat' and "Yahweh's" on their words. | One stop. |
| 3:17 | S.bans → cell(peace,not_eaten) | Rows 'fat' and 'blood' drawn in, and not_mark on 'neither'. The tent icon 'dwellings' on 'dwellings'. 'the fat, the blood' unveiled on landing. | Two stops. |

### Leviticus 4

| Verse | Shot | Lights | Motion |
|---|---|---|---|
| 4:1–2 | col(sin) | Nothing unveiled ('sin offering' is first said at 4:3). The column frame outline pulses once on arrival. HUD 'Leviticus 4'. | One short flight inside 4:1's 2.2 s, then hold through 4:2. |
| 4:3 | cell(sin,brought) group 1 | 'the anointed priest' unveiled on 'anointed priest'. 'a young bull' and the bull icon on 'bull'. Header 'sin offering' on 'sin offering'. HUD 'sin offering'. | One stop at s 1.4 framing the header and group 1. |
| 4:4 | plan:door → C.head | The bull token walks gate→door on 'door'. Hand on its head on 'hand'. | Two stops. |
| 4:5 | plan:tent | The blood path is traced from the door through the screen into the holy place on 'Tent of Meeting'. | One stop. |
| 4:6 | H.veil | Seven drops numbered 1-7 at 0.3 s steps from 'seven times', before the veil. | One stop. |
| 4:7 | H.incense → A → cell(sin,blood) | Blood on the incense altar's two visible horns on 'horns'. The pour traced at the bronze altar's base on 'base'. 'before the veil' unveiled on landing. | Three stops (14.5 s). |
| 4:8 | B (bull) | fat_cover and fat_on are current on their words. | One stop. |
| 4:9 | B.inner | Kidneys, loins and liver cover are current on their words. | One stop. |
| 4:10 | A.fire → cell(sin,burns) | The chip 'peace offerings' on its word. Fat slabs on the fire on 'burn'. 'the fat' (a bull) unveiled on landing. | Two stops. |
| 4:11 | B (bull) | skin, meat (body), head, legs, innards and dung pulse with chips in turn on their words. | One stop. |
| 4:12 | plan:camp → cell(sin,not_eaten) | The whole-bull token is carried out of the gate to the clean place on 'outside of the camp'. Mound with 'ashes' on 'ashes'. Wood bars and flames on 'wood'/'fire'. 'the bull: outside the camp' unveiled on landing. | Pull out, then down to the table. |
| 4:13 | cell(sin,brought) group 1 | 'the whole congregation' unveiled on 'congregation'. | One stop. |
| 4:14 | cell(sin,brought) → plan:door | The bull icon is current on 'bull'. The bull token at the door on 'Tent of Meeting'. | Two stops. |
| 4:15 | C.head | An 'elders' group fades in on 'elders' (count not given, owner question). Hands settle on the bull's head on 'hands'. | One stop. |
| 4:16 | plan:tent | The blood path is current (steady) on 'Tent of Meeting'. | One stop (4.4 s). |
| 4:17 | H.veil | Drops 1-7 relight in turn from 'seven'. | One stop. |
| 4:18 | H.incense → A | The incense horns are current on 'horns'. The base pool is current on 'base'. | Two stops. |
| 4:19 | A.fire | The chip 'all its fat' lands on the fire on 'burn'. | One stop (3.7 s). |
| 4:20 | cell(sin,brought) group 1 | An '=' bracket is traced joining the two who-lines on 'as he did'. HUD 'forgiven' on 'forgiven'. | One stop. |
| 4:21 | plan:camp | The bull token rides the 4:12 path out on 'outside the camp'. The clean place is current. | One stop. |
| 4:22 | cell(sin,brought) group 2 | 'a ruler' unveiled on 'ruler'. | One stop. |
| 4:23 | cell(sin,brought) group 2 | 'a male goat' and the male goat icon unveiled on 'goat'. | Hold. |
| 4:24 | C.head → plan:altar | Hand on the goat's head on 'hand'. The goat token to the north strip, which is current on 'burnt offering' (DERIVED from 1:11). | Two stops. |
| 4:25 | A → cell(sin,blood) | Blood on the bronze altar's two visible horns on 'horns'. The base pour on 'base'. "on the altar's horns" unveiled on landing. | Two stops. |
| 4:26 | A.fire → cell(sin,burns) | Fat on the fire on 'fat'; the chip 'peace offerings'. 'the fat' (a goat or a lamb) unveiled. HUD 'forgiven' on 'forgiven'. | Two stops. |
| 4:27 | cell(sin,brought) group 3 | 'one of the common people' unveiled on 'common people'. | One stop. |
| 4:28 | cell(sin,brought) group 3 | The female goat icon unveiled on 'female'. The entry text, which says 'or lamb', waits for 4:32. | Hold. |
| 4:29 | plan:altar | The female goat token to the north strip, with a hand mark pulse on 'hand'. The north strip is current on 'burnt offering'. | One stop (6.2 s). |
| 4:30 | A | Horns, then base, are current on their words. | One stop. |
| 4:31 | A.fire | Fat on the fire on 'burn'; the chip 'pleasant aroma'. HUD 'forgiven' on 'forgiven'. | One stop. |
| 4:32 | cell(sin,brought) group 3 | The lamb icon and 'a female goat or lamb' unveiled on 'lamb'. | One stop. |
| 4:33 | plan:altar | The lamb token to the north strip on 'burnt offering'; hand mark on 'hand'. | One stop. |
| 4:34 | A | Horns and base are current. | One stop. |
| 4:35 | B (sheep) → A.fire | tail_fat, kidneys and liver cover pulse together on 'fat' (the tail is DERIVED from 3:9). They land on the fire on 'burn'. HUD 'forgiven'. | Two stops (17.1 s). |

### Leviticus 5

| Verse | Shot | Lights | Motion |
|---|---|---|---|
| 5:1 | M | Cell 1: man() 'witness' on 'witness'; chips 'seen' and 'known'. | A long flight to the causes card. |
| 5:2 | M | Cell 2: three dim figures under 'carcass' with chips 'unclean animal', 'unclean livestock' and 'creeping things' on their words. | Pan within the card. |
| 5:3 | M | Cell 3: man() with the chip 'uncleanness of man'. | Pan. |
| 5:4 | M | Cell 4: 'oath', 'evil' and 'good' on their words. | Pan. |
| 5:5 | M | The four cells pulse together on 'one of these'. The 'confess' arrow is traced on 'confess'. | Pull out to the whole card. |
| 5:6 | cell(sin,brought) group 3 | The who-line 'one guilty of 5:1–4' unveiled on 'female'. The female goat and lamb icons are current. | One stop. |
| 5:7 | cell(sin,brought) group 4 → A.bird | 'the poor', 'two turtledoves or young pigeons' and the dove icons unveiled on their words. On A, two doves with chips 'sin offering' on 'one' and 'burnt offering' on 'other'. | Two stops. |
| 5:8 | A.bird | Bird 1 pulses on 'first'. The neck mark is traced on 'wring', with the chip 'not severed'. | One stop. |
| 5:9 | A → cell(sin,blood) | Sprinkle marks on the side on 'side'; a drain at the base on 'base'. "the altar's side" (sin) unveiled on landing. | Two stops. |
| 5:10 | A.fire | The second bird onto the fire on 'burnt offering'. HUD 'forgiven' on 'forgiven'. | One stop. |
| 5:11 | cell(sin,brought) group 5 → K.measure | 'the poorest', 'a tenth of an ephah' and the flour icon unveiled on 'tenth'. On K, the 1/10 segment lights; a basket. not_mark on the jar on 'no oil' and on the cup on 'frankincense'. | Two stops (16.7 s). |
| 5:12 | G → A.fire → cell(sin,burns) | hand('cup') 'handful' on 'handful'; the chip 'memorial portion'. It lands on the fire on 'burn'. 'a handful' (sin) unveiled on landing. | Three stops (10.7 s). |
| 5:13–14 | G → cell(sin,eaten) | HUD 'forgiven' on 'forgiven'. The rest of the flour slides to priest() with the chip "the priest's" on "priest's". 'the remaining flour' unveiled on landing. | Plays within 5:13, then holds through the formula 5:14. |
| 5:15 | col(trespass) → T | Header 'trespass offering', 'anyone' and the ram icon unveiled on their words. On T, the horned ram on 'ram'; coins and scales on 'silver'; the chip 'shekel of the sanctuary' on 'shekel'. HUD 'trespass offering'. | Two stops (18.3 s). |
| 5:16 | T.bar → cell(trespass,brought) | The bar grows as 'restitution' on 'restitution'; the sixth part '1/5' grows on 'fifth part'; an arrow to the priest on 'priest'. HUD 'forgiven'. 'a ram, a fifth' and the silver icon unveiled on landing. | Two stops. |
| 5:17 | T | man() with chips "didn't know" on 'know' and 'guilty' on 'guilty'. | One stop. |
| 5:18–19 | T → cell(trespass,brought) | The ram is current on 'ram'; the chip 'estimation'; an arrow to the priest on 'priest'. HUD 'forgiven'. 'a ram' (a sin he didn't know) unveiled on landing. | Plays within 5:18, then holds through 5:19, which only restates. |

### Leviticus 6

| Verse | Shot | Lights | Motion |
|---|---|---|---|
| 6:1 | T.wrongs | Nothing new. | One short glide in 2.2 s. |
| 6:2 | T.wrongs | The man and 'neighbor' on 'neighbor'. Chips 'deposit', 'bargain', 'robbery' and 'oppressed' on their words. | One stop. |
| 6:3 | T.wrongs | Chips 'lost thing' and 'sworn to a lie'. | Hold. |
| 6:4 | T.wrongs | Return arrows traced from the man to the neighbor, one per item on its word: robbery, oppression, deposit, lost thing. | Slight pull out. |
| 6:5 | T.bar | The 'sworn' arrow on 'sworn'. The bar is current with the chip 'in full' on 'in full'. '1/5' current on 'fifth'. An arrow to 'owner' on 'belongs'; the chip 'in the day'. | One stop. |
| 6:6 | T → cell(trespass,brought) | The ram and 'estimation' are current; an arrow to the priest on 'priest'. 'a fifth, a ram' (a wrong against his neighbor) unveiled on landing. | Two stops. |
| 6:7–8 | plan:altar | A priest token at the altar on 'before Yahweh'. HUD 'forgiven' on 'forgiven'. | Plays within 6:7, then holds through the formula 6:8. |
| 6:9 | A → A.days | HUD 'burnt offering' on 'burnt offering'. The burnt-offering slab on the hearth. The fire is current. The day strip moon→sun is traced on 'all night', with the 'morning' tick on 'morning'. | Two stops. The 'fire' Row has no short, so no cell lights. |
| 6:10 | A → plan:altar | The priest in linen with chips 'linen garment' and 'linen breeches' on their words. The ash heap lifts from the hearth on 'ashes'. The ash token reaches the ash place on 'beside the altar' (DERIVED from 1:16). | Two stops. |
| 6:11 | plan:camp | A token chip 'other garments' on 'other garments'. The ash token rides out to the clean place on 'outside the camp'. 'the ashes: outside the camp' is unveiled off-camera (REACHED_OFFSCREEN; first seen at 7:8). | One stop (6.6 s). |
| 6:12 | A.fire | Wood bars laid on 'wood', with a sun tick 'every morning'. The 'burnt offering' slab on 'burnt offering'. Fat slabs and the chip 'peace offerings' on 'fat'. | One stop. |
| 6:13 | A.days | Three day/night ticks traced on 'continually'. The fire holds. | One stop (4.5 s). |
| 6:14 | plan:altar | HUD 'meal offering'. Priest tokens with a basket by the altar on 'before the altar'; the chip 'sons of Aaron'. | One stop. |
| 6:15 | G → A.fire | The handful (hand cup) is current on 'handful'; frankincense is current. It lands on the fire on 'burn', with the chip 'memorial'. | Two stops. |
| 6:16 | plan:court → cell(meal,eaten) | The chip 'without yeast' on 'yeast'. The court outline pulses on 'court'. 'the priests' (meal) is current. | Two stops. |
| 6:17 | G | The 'most holy' bracket is traced. 'sin offering' and 'trespass offering' names fade in under it on their words. | One stop. |
| 6:18–19 | G | A row of four priest() figures on 'every male'; the chip 'forever'. A hand touch with the chip 'holy' on 'touches'. | Plays within 6:18, then holds through the formula 6:19. |
| 6:20 | K.measure → cell(meal,brought) | The tenth lights on 'tenth' and splits into 'morning' (sun) and 'evening' (moon) on their words. 'tenth of an ephah' unveiled on landing. | Two stops. |
| 6:21 | K.cook | The griddle is current; oil traced on 'oil'. The chip 'soaked' on 'soaked'. Cut lines with 'baked pieces' on 'pieces'. | One stop. |
| 6:22 | A.fire → cell(meal,burns) | The chip 'anointed priest' on its word. The whole tenth onto the fire on 'burned'. 'all of it' unveiled on landing. | Two stops. |
| 6:23–24 | cell(meal,not_eaten) | "a priest's own" unveiled on 'not be eaten'. | Plays within 6:23, then holds through the formula 6:24. |
| 6:25 | plan:altar → G | HUD 'sin offering'. The north strip is current on 'burnt offering is killed'. On G, 'sin offering' under 'most holy' is current on 'most holy'. | Two stops. |
| 6:26 | cell(sin,eaten) → plan:court | 'the priests' (sin) unveiled on 'eat'. The court outline pulses on 'court'. | Two stops. |
| 6:27 | K.vessels | The chip 'holy' on 'touch'. The coat with a blood mark on 'blood'. Water traced on 'wash'; the chip 'holy place'. | One stop. |
| 6:28 | K.vessels | Earthen pot: a crack traced and its halves part once on 'broken'. Bronze pot: scour strokes on 'scoured', water on 'rinsed'. | Pan. |
| 6:29 | G | The 'every male' row is current; 'most holy' is current. | One stop (4.0 s; adjacent). |
| 6:30 | plan:tent → cell(sin,not_eaten) | The blood path is current on 'Tent of Meeting'. 'blood in the Tent: burned' unveiled on landing. | Two stops. |

### Leviticus 7

| Verse | Shot | Lights | Motion |
|---|---|---|---|
| 7:1 | col(trespass) | HUD 'trespass offering'. The header and ram icon are current on 'trespass offering'. | One stop (3.7 s). |
| 7:2 | plan:altar → cell(trespass,blood) | The north strip is current on 'burnt offering'. The ram token; the ring is current on 'around'. 'around the altar' (trespass) unveiled on landing. | Two stops. |
| 7:3 | B (ram) | tail_fat, then fat_cover, pulse on their words. | One stop. |
| 7:4 | B.inner | Kidneys, 'by the loins' and 'cover on the liver'. | One stop. |
| 7:5 | A.fire | The parts land on the fire on 'burn'. 'the fat' (trespass) is unveiled off-camera (REACHED_OFFSCREEN; seen at 7:6). | One stop. |
| 7:6 | cell(trespass,eaten) | 'the priests' (every male among the priests) unveiled on 'every male'. | One stop; the frame includes ON THE ALTAR. |
| 7:7 | G | An '=' traced between 'sin offering' and 'trespass offering' on 'one law'. An arrow to priest() on 'priest'. | One stop. |
| 7:8 | S.shares → cell(burnt,not_eaten) | Row 1: 'skin' with an ox outline and an arrow to 'the priest who offers it' on 'skin'. HUD 'burnt offering'. "the skin: the priest's" unveiled on landing. | Two stops. |
| 7:9 | S.shares | Row 2: oven, pan and griddle <use> on their words; an arrow to the priest. HUD 'meal offering'. meal 'the priest' is unveiled off-camera (seen at 7:10). | One stop. |
| 7:10 | S.shares → cell(meal,eaten) | Row 3: 'mixed with oil' and 'dry' with an arrow to 'all the sons of Aaron'. 'the priests' (all the sons of Aaron) unveiled on landing. | Two stops. |
| 7:11 | D.breads | HUD 'sacrifice of peace offerings' on 'peace offerings'. The shelf frame. | One stop. |
| 7:12 | D.breads → cell(peace,brought) | The chip 'thanksgiving' on 'thanksgiving'. Breads 'unleavened cakes', 'unleavened wafers' and 'cakes mixed with oil' on their words. 'cakes and wafers' and the peace cakes and wafers icons unveiled on landing. | Two stops. |
| 7:13 | D.breads | The fourth bread, 'leavened bread', on 'leavened bread'. Its table icon is unveiled off-camera (seen at 7:29). | Hold. |
| 7:14 | D.breads | One of each lifts on 'one out of each'. The chip 'heave offering' on 'heave'. They move to priest() with the chip 'sprinkles the blood' on 'sprinkles'. The 'right thigh' entry is not lit (EXCUSED). | One stop; translate. |
| 7:15 | D.days | The day 1 bar grows as 'thanksgiving' on 'day'. The 'morning' tick on 'morning'. | One stop. |
| 7:16 | D.days | Bars 'vow' and 'freewill' grow to day 2 on 'next day'. | Hold; grow_rect from the drawn width. |
| 7:17 | D.days | A flame in the day 3 column on 'third day'. | Hold (5.0 s). |
| 7:18 | D.days → cell(peace,not_eaten) | not_mark on day 3's eat mark on 'eaten'. Chips 'not accepted' and 'abomination' on their words. "third day's meat" unveiled on landing. | Two stops. |
| 7:19 | D.split → cell(peace,eaten) | The meat token to the flame on 'unclean' and 'burned', or to the group on 'clean'. 'unclean meat' and 'the offerer' (everyone who is clean) unveiled on landing. | Two stops; the frame shows WHO EATS and NOT EATEN. |
| 7:20 | D.split | One figure slides apart once on 'cut off'; the chip 'cut off'. | Hold. |
| 7:21–22 | D.split | Chips 'uncleanness of man' and 'unclean animal' on their words. 'cut off' is current on 'cut off'. | Plays within 7:21, then holds through the formula 7:22. |
| 7:23 | S.bans | Ox, sheep and goat on 'bull', 'sheep' and 'goat'. not_mark on the 'fat' row on 'fat'. | One stop. |
| 7:24 | S.bans | Chips 'dies of itself' and 'torn' on their words. An arrow to 'other service' on 'service'. not_mark on 'eat'. | Pan. |
| 7:25 | S.bans | 'cut off' by the fat row on 'cut off'. | Hold. |
| 7:26 | S.bans | A dove on 'bird' and a goat on 'animal', with not_mark on the 'blood' row. 'dwellings' is current. | Pan. |
| 7:27–28 | S.bans | 'cut off' by the blood row on 'cut off'. | Plays within 7:27, then holds through the formula 7:28. |
| 7:29 | C → cell(peace,brought) | The offerer with the ox on 'offers'. The herd, lamb and goat icons are current, and the leavened bread icon is seen. | Two stops. |
| 7:30 | B.breast → cell(peace,brought) | Hands under the breast on 'own hands'. Fat and breast pulse on 'fat' and 'breast'. The breast sways once on 'waved'; the chip 'wave offering'. 'with his own hands' unveiled on landing. | Two stops. |
| 7:31 | B | The fat token to the sidebar's altar icon on 'burn'. The breast to the priests with 'Aaron and his sons' on "Aaron's". 'the breast' is unveiled off-camera (seen at 7:33). | Pull out to the whole board (5.4 s). |
| 7:32 | B | right_thigh pulses on 'right thigh' and lifts once on 'heave'; the chip 'heave offering'. | One stop. |
| 7:33 | B → cell(peace,eaten) | The thigh moves to one priest with the chip 'offers the blood' on 'blood'. 'the right thigh' unveiled on landing. | Two stops. |
| 7:34 | B | A sideways arrow (breast) on 'waved breast' and an up arrow (thigh) on 'heaved thigh', from the chip 'children of Israel' to 'Aaron and his sons'; the chip 'forever'. | One stop. |
| 7:35–36 | B | An 'anointing portion' bracket traced round the breast and thigh chips on 'anointing portion'. | Plays within 7:35, then holds through 7:36, which only restates. |
| 7:37 | table:all | HUD 'the law'. Column frames pulse in the verse's order on their words: burnt, meal, sin, trespass, then the 'consecration' chip fades in on 'consecration', then peace. The WHEN row's five veils lift on landing (EXCUSED until now). | Pull back to the whole table at s 0.45. |
| 7:38 | table:all → L | Moses on 'Moses'. The mountain drawn in, with the chip 'Mount Sinai', on 'Mount Sinai'. 'wilderness of Sinai' on its words. | A van Wijk flight out and over to the Sinai card. It lands 0.35 s before the end and holds: the last frame. |
