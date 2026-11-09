# Leviticus 1–7: the offerings table, filled on a workbench

The five offerings of Leviticus 1–7 as one comparison chart that fills in as
the law is read. The frame never pans or zooms: it is a still workshop in
three fixed regions. Each verse's thing is built on the bench on its word, a
chip lifts off it and glides to its slot in the dock's column of the
offerings table, and at the end of an offering's section the column is filed
into the Tabernacle reference page's own table (the file view), after which
the workshop comes back.

The 163 files (154 verses and the nine range files) are in
`web/visuals/Leviticus/1`–`7`, written by `generate_leviticus17_svg.py
--web`. QC refuses none of them, and the deploy count is 6,780 of 20,000.
The owner picked this concept ("the workbench that files") from three
prototypes of Lev 1. The prototypes, their reviews and the judge's brief are
in the archive's `mockups/lev17-display-2026-11-08`. The camera build it
replaced is in git.

## What it shows

- **The table is the spine.** Every unit of the offerings table (each entry,
  who-line, drawn thing, header and by-line) starts veiled as a placeholder
  bar in its offering's column. A unit is lit on the word of the verse that
  `offerings.py` cites for it, so the table is complete by 7:37, the verse
  that sums it up. 7:37 then lifts the WHEN cells in the order it names the
  offerings (burnt, meal, sin, trespass, consecration, peace).
- **The bench is where things happen.** It holds the pen and the altar set,
  and boards for what a cell can't hold: the labelled cutaway of the beast,
  the holy place's veil and altar of incense, the meal offering's supplies
  and cookware, 5:1–4's causes, the trespass value set, the bread rack, the
  day strip and the bans.
- **The strip is where it happens in the court.** The rings round the altar,
  the blood's path to the veil, the crop to the place of the ashes, and the
  bull and the ashes carried out through the gate to the clean place.
- **Nothing loops.** Everything plays once and holds. There is no prose on the
  graphic, only WEB names, numbers and labelled drawings.

## The frame

Three fixed regions on the 1024 × 576 frame (`leviticus17_bench.STRIP`,
`BENCH` and `DOCK`), and a top layer for the file view and 7:38:

| Region | Box | Holds |
|---|---|---|
| strip | 8, 8, 670 × 222 | the reference court plan, one window for the whole book (`leviticus17_parts`) |
| bench | 8, 238, 670 × 330 | the pen, the altar set and each verse's board (`leviticus17_parts`, the sections) |
| dock | 686, 8, 330 × 560 | five tabs over the active offering's column (`leviticus17_dock`) |
| top | the whole frame | the file view (`leviticus17_dock.file_view`) and 7:38's Sinai |

### The strip

`leviticus17_parts.strip_art` draws the reference's own `draw_court`,
`draw_tent` and `draw_furnishings`, words dropped, culled to one world window
(`StripCanvas`, no clipPath): from just west of the veil (`WX0`) to the gate,
centred on the altar's line, at `PS` 0.52 strip px a world px. Past the gate
a band holds the dashed camp edge and the clean place, pulled in, not to
scale. The court's walls are 50 cubits apart, about 360 px at this scale, so
they are off the strip.

The places (`parts.place`) come in once, each on its word, and stay for the
book: Tent of Meeting, veil, altar of incense, door, altar, north, place of
the ashes, gate, outside the camp and clean place. Named again, a place
pulses. The veil's and the altar of incense's chips sit under the tent, each
on a short leader up to what it names. There are no animal tokens on the
strip. A beast's place is a ring or a chip, with a link pulse on the bench's
beast. Priests and carried things (the carcass, the ashes) walk.

### The bench

The altar set (the altar inset, its wood and its fire, `parts.ALTAR_KEYS`)
comes in at 1:5 and 1:7 and is there at every section boundary. A board that
needs the whole bench hides it (`parts.altar_out`) and brings it back
(`altar_in`). That happens for 5:1–5 (the causes), 5:15–6:7 (the trespass
value set) and 7:12–28 (the bread rack, the day strip, the split and the
bans). The priests' shares
(7:8–10) stand left of the altar, which stays.

Beasts are `svg_figures` figures in the pen, and a beast opens into its
`beast_parts` cutaway (`parts.Beast`, `parts.cutaway`) on the word that
names its fat. Its parts pulse with their chips, and `parts.to_wood` glides
what is burned onto the wood as slabs of their kind (fat white). The
drawings more than one section shows are in `leviticus17_art.py`.

### The dock

Five tabs over one column panel. Each offering's column is laid out to its
own content from the reference's own words (`dock_layout`, through
`generate_leviticus17_svg.table_units` and `_entries_rows`): the header (the
WEB name, 18 px bold), then BROUGHT, ON THE ALTAR, THE BLOOD, WHO EATS and
NOT EATEN, with 11 px bold caps labels, 14 px entries and 12 px italic
who-lines. Every slot is one table unit, and an unlit unit is a placeholder
bar. The sin column, the fullest, fits by putting its ranks' icons in the
gutter.

- A tab is named the first time its offering is said, and `dock.switch`
  crossfades the column (0.6 s).
- `dock.light` lifts a unit in place with one pulse. `dock.fly` lifts a 14 px
  chip off the thing just built and glides it on a shallow arc to its slot,
  and the slot unveils as it lands.
- `dock.current` pulses a unit named again, and `dock.case_outline` keeps a
  steady outline round the current case's units in BROUGHT.
- `dock.forgiven` puts the "forgiven" chip at the sin and trespass headers
  on the nine verses that say it.

## Motion

- **One timeline.** Everything that changes is an element
  (`leviticus17_bench.El`) on one global timeline across the 163 files in
  canonical order. A file draws every element's state at its start and its
  events inside the file as SMIL, so each file begins on the frame the file
  before ends on. A range file's clock spans its verses. A cue in its later
  verse waits a further `RANGE_LAG` (0.15 s), since the app leaves the
  `<img>` running across a range.
- **Nothing before its word.** `bench.cue` is `SAY_LEAD` (0.1 s) before the
  verse says the phrase (`narration_clock`), and a phrase the verse doesn't
  say raises, so the build fails.
- **The vocabulary**, all SMIL, played once with `fill="freeze"`:
  - a fade, a lift or a grow for things and chips;
  - a trace for blood, cut lines, arrows, rings and paths (`traced_el`; a
    dashed line fades in instead, since a trace writes its own dashes);
  - one 0.9 s pulse for "first" or "named again", or a steady outline for the
    current case;
  - the not-mark drawn in one stroke (`parts.not_el`);
  - a travel, of four kinds: a chip flight (`dock.fly`), a bench move (a part
    to the wood, bread heaved, the breast waved), a token walk on the strip,
    and the filing glide.
- **The file view** (`dock.file_view`). The workshop crossfades (0.8 s) to the
  reference's own table (`draw_offerings` at `FV_S` 0.44). Units not yet lit
  are under bars. Readable keys sit over its column names (14 px) and row
  labels (11 px bold caps). The dock's column (a `<use>` of it) then glides
  into its slot. It takes the low road: it slides 30 px down and across to
  under the slot, shrinking to the slot's width, then rises into it, so it
  passes under the keys of the columns it crosses. The keys are drawn under
  the gliding column. The filed column's own key is veiled until the column
  lands, and it fades in with the landing crossfade. The view holds, then
  the workshop crossfades back.
- **The six file views**: burnt (1:17), meal (2:16), peace (4:1–2), sin
  (5:13–14: a 0.9 s glide, a 1.0 s hold and a 0.6 s return, so 5:15 opens
  in the workshop), trespass (6:7–8) and the whole table (7:37). 7:37 files
  the peace column after "burnt offering"'s WHEN has lifted, in 0.9 s, and
  each later WHEN lifts on its word or as the column lands, whichever is
  later.
- **7:38.** The table crossfades straight into a full-frame Sinai panel as
  "Moses" is said: Moses, then the mountain drawn in, then the wilderness. The
  book ends on the mountain.

## The sections

`bench.build_timeline` builds the furniture (`parts.setup`, `dock.setup`),
then each section in order, with `bench.OWNER` set to its id. The contract at
each section boundary is in `leviticus17_bench.py`'s docstring: the places
named so far, the altar set at rest, the boundary's tab active with every
unit lit so far, and no outline or chip of the section left on.

| Section | Module | Verses | Files its column |
|---|---|---|---|
| s1 | `leviticus17_wb_s1.py` | 1:1–17 | burnt, in 1:17 |
| s2 | `leviticus17_wb_s2.py` | 2:1–16 | meal, in 2:16 |
| s3 | `leviticus17_wb_s3.py` | 3:1–17, 4:1–2 | peace, in 4:1–2 |
| s4 | `leviticus17_wb_s4.py` | 4:3–35 | |
| s5 | `leviticus17_wb_s5.py` | 5:1–6:8 | sin, in 5:13–14; trespass, in 6:7–8 |
| s6 | `leviticus17_wb_s6.py` | 6:9–7:10 | |
| s7 | `leviticus17_wb_s7.py` | 7:11–38 | the whole table, in 7:37 |

Each module's docstring describes its bench verse by verse. `leviticus17_spec.py`
is data only: `RANGES`, `CASES` (where each case begins: its pieces clear
and the dock's case outline moves), `REACH` (where a unit is first lit, when
that isn't the first verse `offerings.py` cites for it) and `EXCUSED` (the
five WHEN cells, which lift together at 7:37). A section may lay its own
`REACH` and `EXCUSED` over them.

## QC and the budget

`bench.qc_file` refuses to write a file that:

- isn't well-formed XML (`xml_problems`). The app shows a verse in an
  `<img>`, which parses it strictly. An inline render forgives a doubled
  attribute, an `<img>` shows nothing;
- has an animation running across its end;
- has an animation beginning after the narration minus 0.1 s, or ending
  less than 0.35 s before its MP3 does (its last verse's, for a range),
  counted as the file writes them, to 0.01 s (`bench.fit` rounds down to
  fit);
- breaks the motion budget (`budget_problems`): no camera; at most 3 chip
  flights and 1 file view; a travel at most 560 px (the filing glide aside)
  and 800 px/s at its eased peak; one thing travelling at a time; nothing
  fading in, flaring, traced or pulsed elsewhere while it does (in the file
  view too, during its glide);
- has two regions beginning animations within 0.3 s, unless they share a
  group (one gesture);
- has text under 11 px in the workshop, text overlapping other text or
  leaving its region (at the file's start and end and after each event);
- lets the gliding column's words touch the file view's keys, at its
  quarter, half, three-quarter and nine-tenths points
  (`glide_text_problems`);
- is over 130 KB (it warns over 70).

`bench.run_report` adds the section boundaries (`boundary_problems`, the
book's end included) and coverage: every unit lit by 7:37, first in a verse
that cites it, or its `REACH`, or `EXCUSED`.

`bench.render_file` leaves out what an opaque full-frame element (the file
view's table) hides through the whole file, so 7:38 doesn't carry the
workshop under 7:37's table.

`test_leviticus17` checks the files and ranges, the cues, coverage, the dock's
units, the budget and timing over the whole book, the boundaries, the glides'
words, the seams by construction, well-formed XML (the probes and every
published file), the probes against QC and the size aims.
`test_svg_freeze` checks that every published SVG under `web/visuals` is
well-formed.

## As measured

Measured 2026-11-09, over the files written to the site:

- **Files.** 163, with the nine ranges, 6.39 MB in all.
- **Size.** Three files are over the 70 KB aim, and they are file views:
  6:7–8 (91.8 KB), 7:37 (91.4) and 5:13–14 (90.4). None is over 130 KB.
  5:15 is no longer over the aim, since it opens in the workshop, and neither
  is 7:38 (63.4 KB).
- **Motion.** 0 camera moves. 30 chip flights (at most 2 a file, the longest
  543 px, the fastest peak 790 px/s), 34 bench moves, 5 token walks, 6 file
  views with their filing glides, and 11 column switches. Travels take 76 s
  of the book's 1,509 s.
- **Stillness.** Sampled in Edge every 0.25 s, 63% of the steps change no
  pixel (3,854 of 6,121), and 34 steps change more than 30,000 px (file-view
  crossfades and whole-board set changes). Read from the timeline, nothing
  animates for 64.8% of the narration (every fade, trace, pulse and travel
  counted as motion).
- **Seams.** Edge, inline, paused: all 162 consecutive pairs differ by 0 px
  (the previous file's end and its frozen rest against the next file's first
  frame), and every end matches its frozen rest.
- **Loading.** All 163 files load in an `<img>` in Edge. Fourteen files
  played in real time in an Edge `<img>` (3:2, 4:19, 5:15, 6:30, 7:8, 7:11,
  7:12, 7:15–19, 7:37 and 7:38) end on their paused frame, and each first
  frame matches the file before's played end, at 0 px.
- **Not checked.** WebKit wasn't run on this build, and nothing has been seen
  on an iPad or with narration.

## Defaults that await the owner

- **The book's last frame** is 7:38's mountain over the finished table, not
  the table. Sinai could instead be an inset, or the table could stay dimmed
  behind the mountain.
- **The strip** keeps its window: from the veil to the gate at 0.52, with
  empty court between the altar and the gate, and the walls off it. Making
  the strip shorter would move the empty space into the bench, whose boards
  are laid out in absolute px in seven modules.
- **The filing glide's low road**: the column slides down and across,
  shrinking, then rises into its slot. 5:13–14's view is short (a 0.9 s glide,
  a 1.0 s hold and a 0.6 s return), so 5:15 opens in the workshop.
- **7:37**: the peace column is filed after "burnt offering"'s WHEN, and
  "meal offering"'s WHEN lifts as it lands, 0.15 s after its word.
- **The opened beasts.** The congregation's bull opens into its cutaway at
  4:19, as the priest's did at 4:8. The ruler's goat (4:26), the common
  person's goat (4:31) and lamb (4:35) still give a fat slab off the whole
  beast.
- **The bread rack** comes in with 7:12's "thanksgiving", as the altar set
  steps out. 7:11 is the peace tab only.
- **The shares** (7:8–10) stand left of the altar: the giver, an arrow, and
  the receiving priest at x 322 (the four sons at 7:10).
- **First-word cues**: "cakes" and "wafers" (2:4, 7:12) light on "unleavened",
  like "Tent of Meeting".
- **Small things the builders noted**: three cakes that read as six rolls
  (2:4), the bench's cupped hand with a squarely cut arm, 2:16's "all its
  frankincense" chip showing for about 1 s before the file view, the
  workshop resting empty for about 4 s in 4:1–2, and the sin column's pulse
  on "sins" there.

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
the horned sheep, so the table and the trespass board agree (decision 1).
With the wording fixes, that regenerates `reference/Tabernacle.svg`,
`.json` and `.html` deliberately. The diff must touch only the ram icons and
the corrected offering text and cards.

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

## Files

| Kind | Files |
|---|---|
| Generator | `generate_leviticus17_svg.py` (the clock, the files and ranges, the table's units, compaction, the CLI; import-safe) |
| Engine | `leviticus17_bench.py` (the timeline, rendering, QC), `leviticus17_parts.py` (the strip and the bench's shared parts), `leviticus17_dock.py` (the dock and the file view), `leviticus17_art.py` (the shared drawings) |
| Sections | `leviticus17_wb_s1.py` to `leviticus17_wb_s7.py` |
| Data | `leviticus17_spec.py` (`RANGES`, `CASES`, `REACH`, `EXCUSED`), `offerings.py`, `sanctuary.py` |
| Tests | `test_leviticus17.py` |
| Output | `web/visuals/Leviticus/1`–`7/`: 154 verse files and 9 range files, 163 in all |

The nine ranges pair a verse with a speech formula ("Yahweh spoke to Moses,
saying") or a pure restatement, so no range shows a later verse's words early
(D17 plays a range's motion from the start): 5:13–14, 5:18–19, 6:7–8,
6:18–19, 6:23–24, 7:21–22, 7:27–28 and 7:35–36 fold the formula or
restatement into the verse before it. 4:1–2 is the other way round: a 2.2 s
formula and then the first sin offering verse, which files the peace column
before "sin offering" is said at 4:3.

Build and check (the whole timeline is always computed, so seams are right):

    .venv\Scripts\python.exe generate_leviticus17_svg.py --out DIR [--only 2:1-2:16] [--report qc.json]
    .venv\Scripts\python.exe generate_leviticus17_svg.py --qc-only
    .venv\Scripts\python.exe generate_leviticus17_svg.py --web
