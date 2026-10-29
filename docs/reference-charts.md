# Reference charts

`web/visuals/reference/` holds the standalone reference charts. Nothing in them is tied to a verse.

Each chart is an SVG plus an `.html` viewer page. You can also open an `.svg` directly in a browser.

**The viewer.** The six generators write their viewer pages with `reference_viewer.page()`. Every page offers:
- one finger or the mouse to pan, two fingers to pinch, the wheel to zoom, and fit / + / − buttons that zoom about the middle of the screen;
- a name search. The search box is 16 px, because iOS zooms the whole page when a smaller field takes focus.

A chart whose generator also writes a **sidecar** (`<stem>.json`: the family tree's, the Tabernacle's, the atlas's, the kings' and Paul's journeys') gets more. The family tree's cards are people (below); the Tabernacle's are parts, the atlas's places, the kings page's reigns, prophets, nations and judges, and the journeys page's places, legs, lands and letters (`"card": "parts"`, see [The Tabernacle](#the-tabernacle), [The Land of Israel](#the-land-of-israel), [Kings and prophets](#kings-and-prophets) and [Paul's journeys](#pauls-journeys)). A card can also link to another reference page (`ln`: a king's box on the family tree), opened in the same frame, whose name the app's bar then shows:
- **A tap on a box** opens its card. On a phone the card is a bottom sheet; from 700 px wide it is a side panel.
- **Search** lists the matches, each with its relation, so the nine Azariahs can be told apart. Whole names come first, then the start of a name, then anywhere in one, then a name found only in a box's note. A box's other names count as its names: "Jacob" finds Israel. ↑ ↓ step through the matches.
- **The card** gives the relation, the generation, the Ussher years where the chronology dates the person, the box's note and cross-references, the family, "Line to Adam", and the verses. The family is:
  - the parent, or both where the mother is on the wife line;
  - wives and children;
  - the men only joined under him (a dashed join, "as the text implies"), apart from his sons;
  - the family a reference chip stands in.
- **Line to Adam** outlines every box up the line and frames them. A wife hangs under her husband, so his line isn't hers. Hers runs from her reference chip in her father's family where she has one (Leah's through Laban), and otherwise the card offers none.
- **A verse chip** shows the verse, read from `/bibles/WEB/`. Inside the app, "Open in Theoria" posts `{type: "theoria:goto", book, chapter, verse}`, and the app closes the chart and goes to that verse without playing it.
- **The address** keeps the selection (`#id=<id>`), so ↗ opens and shares what is on screen. The app opens a chart at `#at=<Book>.<chapter>.<verse>`, and the page starts on the names that verse speaks: the parts whose own verses include it, then the parts whose ranges cover it, and, on a sheet that sets `"chapter": true` (the atlas), the parts its chapter names.
- **Escape** closes the results, then the card, then (in the app) the chart.
- **Layers.** A sheet can mark groups `<g data-layer="...">` and list them in the sidecar's `layers`; chips in the bar show and hide them. A part on a hidden layer takes no tap, and a part found by search or named by `#at` shows its layer.
- **Hit areas.** The smallest box near the finger wins. A sheet of close-set small parts can ask (`"tap": "inside"`, the atlas) for a box the finger is inside to beat one it only grazes, so a neighbour's dot a few px off doesn't take the tap, unless the grazed box lies within the other (a box that holds parts is their background). A part can be tapped on `t` boxes in place of its own (an atlas place's dot and its name, not the gap a leader line spans), on more boxes (`hb`: the court and the tent, on their walls and labels, since other parts fill their insides), on `lo` boxes only where nothing else is under the finger (a river along its course, a lake, which the towns on them would otherwise lose taps to), or on none (`nohit`: the mercy seat lies on the ark). A duplicate card (`nos`: a part's drawing) is left out of search and `#at`.
- **Lines and steps.** A part drawn as a line (`pth`, a journey's leg, as x0,y0,x1,y1,…) glows along it when outlined, instead of getting a box. A part in a sequence (`st`: the parts before and after, a journey's legs) has buttons to both on its card, under the sidecar's `step` label.
- **Text by size.** A sheet can group its text by size (`<g data-fs="19">`). The page draws a group only while its text is at least 7.5 px on screen (`READ`), and with `data-fmax` only until it grows past that many px. A part carries its group's `fs` and `fx`, and while its name is hidden it takes no tap. When a part is outlined, selected or named by `#at`, at a zoom that hides its name, the name is written over the outline at reading size. Selecting a part zooms in far enough to read its name, and for a land not so far that its name fades.

Without a sidecar (the OT timeline), the search steps through the sheet's own text and zooms each hit to at least full size, where names are 15 px. The V6 and 1–2 Chronicles pages are older copies of the viewer, with no pinch and no zoom-to-hit, because nothing writes them.

## Status

- **Deployed.** All seven charts deploy with the site at `https://theoria-bible.net/visuals/reference/<file>`. `web/` is served as it is, and Publish commits `web/visuals/`, so a change to a chart ships like any other visuals change.
- **Linked: the OT family tree, the Tabernacle, the Land of Israel, Kings and prophets and Paul's journeys.** The app's **Reference** button, in the header beside ✦ Illustrated, lists the charts in `REFERENCES` in `web/js/app.js`. A chart opens full screen over the app, in a frame under a bar with ← Back and ↗:
  - the frame keeps the passage, and any narration playing, as they were underneath;
  - the installed home-screen app has no Back button of its own, so the bar provides one;
  - ↗ opens the chart's page on its own, at the address you can share.
  The V6 heir-spine variant and the 1–2 Chronicles tree were experiments, and the OT timeline isn't in the list either. All three are unlinked, but anyone with the exact URL can open them.
- **Adding a chart to the list** is one entry in `REFERENCES` (title, one-line blurb, root-absolute `href`). It is web-app code, so it is committed by hand, and the chart's own files ship through Publish.
- **Not indexed.** `build_manifest.py` only indexes `web/visuals/<Book>/<chapter>/` and the flat `web/visuals/` root, so the charts never become manifest keys.
- **Cost.** The charts are 21 deploy files, the five sidecars among them. The Reference list itself costs none, because it is part of `app.js`.

| Chart | Files | Size | Built by |
|---|---|---|---|
| [The Old Testament family tree](#the-old-testament-family-tree) | `Old_Testament_family_tree.svg` / `.json` / `.html` | 26,946 × 16,736 px, about 1.3 MB, 1,254 boxes; the sidecar is about 215 KB | `generate_ot_family_tree_svg.py` |
| [V6 heir-spine variant](#the-v6-heir-spine-variant) | `Old_Testament_family_tree_V6_heir_spine.svg` / `.html` | 21,162 × 13,759 px, about 1.4 MB | no script writes it; its layout is in `tools/layout_lab.py` |
| [The 1–2 Chronicles family tree](#the-12-chronicles-family-tree) | `1-2_Chronicles_family_tree.svg` / `.html` | 19,777 × 13,754 px, about 1 MB | none: a frozen file |
| [The OT timeline](#the-ot-timeline) | `Old_Testament_timeline.svg` / `.html` | 65,030 × 12,230 px, about 1.4 MB, 1,269 boxes | `generate_ot_timeline_svg.py` |
| [The Tabernacle](#the-tabernacle) | `Tabernacle.svg` / `.json` / `.html` | 2,860 × 2,906 px, about 100 KB, 34 cards | `generate_tabernacle_reference.py` |
| [The Land of Israel](#the-land-of-israel) | `Land_of_Israel.svg` / `.json` / `.html` | 6,103 × 7,680 px, about 115 KB, 224 places and 267 cards; the sidecar is about 237 KB | `generate_israel_atlas.py` |
| [Kings and prophets](#kings-and-prophets) | `Kings_and_prophets.svg` / `.json` / `.html` | 2,370 × 6,684 px, about 80 KB, 139 cards; the sidecar is about 96 KB | `generate_kings_reference.py` |
| [Paul's journeys](#pauls-journeys) | `Pauls_journeys.svg` / `.json` / `.html` | 7,336 × 3,978 px, about 320 KB, 64 places, 74 legs and 178 cards; the sidecar is about 145 KB | `generate_journeys_reference.py` |

## The Old Testament family tree

One contiguous family tree of the whole Old Testament, rooted at Adam.

**How it is built.**
- The data is `chronicles_tree.py`, which welds the 1 and 2 Chronicles genealogies into one tree, and `ot_grafts.py`, which grafts on every other person the Old Testament gives a join for.
- Names and spellings are the WEB's, unmodified.
- The 1 Chronicles 1–9 and Matthew 1:1–17 verse pictures are cameras over this same tree (`svg_chronicles_world.py`, `svg_matthew_world.py`). Matthew 1:18–25 is a figure stage instead (`svg_matthew_nativity.py`).
- The wall chart uses the centred layout (`generate_ot_family_tree_svg.arrange` and `place`). The Matthew camera lays the tree out with the heir under its parent (`arrange_spine` and `place_spine` in the same module), so his line of descent is a straight column.
- The 1 Chronicles camera uses a third layout, `layout_regions.py` (`svg_chronicles_world.LAYOUT = "regions"`). Adam to Israel's sons form one fan in strict generation rows, and each son's descendants stand in a titled panel under it, reached by a routed line; the routes share one trunk under the fan, so they draw as one thin branching line. A wife stands beside her husband, on the side away from his brothers where she can, and a house that gathers people is a small italic label on the line; so are the two houses that head panels, which keep Israel's sons' row to the twelve. In each verse's file a branch the reading has not reached yet is one faint block under its first person (`svg_silhouettes.py`). `generate_1chronicles_tree_svg.py --centred` and `--spine` re-run the camera under the other two layouts for comparison.

**Reading it.** The legend is on the sheet.

| Mark | Meaning |
|---|---|
| solid line | father to son, as the text states it |
| dashed line with an open bead | a join the text implies but does not state; the note on the box says what the inference is |
| doubled line | a wife, or the mother the line is reckoned through |
| gold line inside a box | a cross-reference: this person is named elsewhere on the sheet, and the line says how. The note is written in both boxes. Pairs close enough together are also tied by a gold arc, edge to edge. |
| small rose pill with a gold dot | a reference chip: a woman named in a second family. Her one full box is elsewhere, and its gold line points here (see below) |
| box outline | gold for a king (with a crown), jade for a priest or Levite, rose for a woman the text names, grey for a house or company |
| small number, bottom right | the generation from Adam, counted father to son; none on a wife's box, and none below a join whose length the text doesn't give |

**The generation number.** It is `N.gen`, which `chronicles_tree.Tree.seal` computes from Adam (1) down, and `generate_ot_family_tree_svg.printed_gen` decides where it prints. It is not the box's depth in the tree:
- A wife keeps her husband's number, so her sons are his sons' generation. Her own box prints none, because her generation is her own line's.
- A house box is never a generation. One that only gathers its parent's own children (`gap=0`, such as Absalom's "three sons") passes the parent's number down.
- A join marked `gap="?"` has no number, and neither does anything below it. That covers the companies the text gives no generations for (the kings and chiefs of Edom, the kings of Israel, the later houses of Benjamin, the 7:12 "and also" group, the priests' courses, the gatekeepers) and the men hung on their tribe or clan with no father named (1 Chronicles 4's families of Judah, Jephunneh and Hodiah among them, the fathers of the Numbers princes and spies, Eli, Ahithophel, Elimelech, Mordecai's Kish, Jahdai). Seir, joined to Esau by marriage, is marked too.
- The marks are set where each graft is made (`Tree.child(..., gap=...)`). `seal` raises if a house box would hand a number down without one.

So Abraham prints 20, Perez 24 and David 33, and Abraham to David is the fourteen of Matthew 1:17. The masthead's "the deepest line runs N generations" is computed from the same numbers (`deepest_line`).

**One box per woman.** A woman the canon names in two families has one full box and, where her other box would stand, a reference chip (`chronicles_tree.Tree.chip`): her name in a small pill with a gold dot, with no children, note, reference or number. The real box goes where her children are reckoned, and otherwise under her father:
- Leah and Rachel stand beside Israel as his wives; Laban keeps a chip for each.
- Milcah stands beside Nahor over her eight sons; Haran keeps a chip.
- Ruth stands beside Boaz, through whom Obed is reckoned (Matthew 1 finds her there); Mahlon keeps a chip on the marriage bar her box stood on.
- Michal had no child, so her one box is Saul's daughter, and David's wife list leaves her out. A cross-reference ties her to David, with no chip.

A chip keeps the link of the box it replaced, so the layouts place it the same way: a child in her father's row, or a wife beside her first husband. It stands a little lower than the names on its row so its middle is on their name line (`generate_ot_family_tree_svg.top_of`). The chip's cross-reference is written in the real box only; when the two are close, the gold arc ends on the chip's dot. Chips carry no `src` stamp and are left out of the verse cameras' name lookup, so a verse that names one of these women lights her real box. The wall chart, the timeline and both verse cameras draw chips through `draw_chip`, and none of them counts a chip as a person.

**Notes, cross-references and bands.** The words of notes and cross-references appear on the wall chart and the timeline only. The 1 Chronicles verse camera draws names, and the Matthew camera draws a cross-reference's arc, without its words, when a verse lights both ends (`svg_matthew_world`). A note says what the text says. Where it rests on an inference it says so ("some read", "probably"), and where two books disagree the disagreement is written on the box rather than resolved. A muster total, a count or a title the text gives a whole family, such as "heads of fathers' households", goes on the father or the family's mother, not on the last son listed. A note that names the group it covers can stay on the last son, as Shelah's "these three by Shua's daughter" (2:3) does. Notes on 1 Chronicles boxes start as the scene rows' notes in `generate_1chronicles.py`, and `chronicles_tree.py` adds to them or replaces them.

Pre-order `Tree.find` takes whichever namesake it reaches first. So where a name already repeats on the tree when a note, a cross-reference or a graft is placed, the box is held from where it was made, reached by a path down from a unique name (`Tree.at`, which raises unless each step is the only box of its name there), or looked up inside a subtree. `Tree.find` records every lookup whose name repeats, at that moment, in the scope it searched (`Tree.ambiguous`). The audit prints those with where each landed, and every cross-reference whose ends bear repeated names, so each can be checked. The bands behind the big subtrees are anchored the same way: where a band's name repeats, `REGION_AT` gives `region_node` a path for `Tree.at`. The timeline anchors its bands by `chronology.locate` paths (`generate_ot_timeline_svg.REGION_LOC`).

A cross-reference's gold arc runs from the edge of one box to the edge of the other, so its end dots sit on the box edges and never on the words (`link_route`). Of the arc between the two centres and curves leaving each box square to an edge, the chart takes the one that passes the fewest boxes bearing either end's name, then passes behind the fewest boxes, then keeps clearest of the rest, then is shortest (`_route_score`). A line behind a box reads as a line through that name, and past a namesake it would seem to point at the wrong man. The wall chart and the timeline route their arcs the same way, each on its own layout.

```
.venv/Scripts/python.exe generate_ot_family_tree_svg.py   # rebuild the .svg and .html
.venv/Scripts/python.exe chronicles_tree.py               # audit the tree without drawing it, with the lookups to check
```

**The sidecar.** `generate_ot_family_tree_svg.main` also writes `Old_Testament_family_tree.json` through `family_tree_data.sidecar`, so the page can say who a tapped box is. The SVG is unchanged by it. For each box it records:
- **an id**: when the box is new, the shortest run of names from it up towards Adam that no other box shares (`stable_ids`), such as `azariah.ahimaaz`. Brothers of one name take `~2`. After that it keeps the id it was issued: the generator reads the last sidecar back (`issued_ids`), so a namesake grafted later doesn't change a shared link, and an id once issued is never given to another box. `N.key` isn't used, because it numbers namesakes in pre-order and so changes when a graft adds one. A link to an id the sheet no longer has opens the search on its name;
- its box on the sheet, parent, children and reference chip;
- **a relation** that parts namesakes (`relations`), and further up the line ("son of Azariah, son of Johanan") or by order ("named second") where it has to. Examples:
  - "son of Ahimaaz", "wife of Boaz";
  - "among the kings of Edom", "one of the priests' courses";
  - "father of Hoshea, king of Israel" for a usurper's father hung in the kings' house.
  - Where the line alone would say it wrong, the tree's data gives the words (`N.rel`): Tamar hangs on Judah by the wife line because Perez and Zerah are reckoned through her, and she reads as "Judah's daughter-in-law";
- its generation (`printed_gen`), note, cross-references, and Ussher years from `chronology.bind`;
- **its verses**, which come from four places and never from matching names across the canon:
  - the box's own ref, read by `verse_refs.parse`, which checks every verse against WEB's versification and fails the build on one WEB doesn't have;
  - each verse of the 1 Chronicles 1–9 camera (`svg_chronicles_world.World.lit`);
  - Matthew 1:1–17's (`matthew_tree.MatthewLine.lit`);
  - Genesis 5 and 11:10–32: a person's own paragraph and his father's in `generate_genealogy`'s tables, kept only where the verse speaks the name.

World and `matthew_tree` build trees of their own, so `family_tree_data.pair` walks each down from Adam beside the chart's. Where `matthew_tree` joins a second name onto a box ("Jacob · Israel"), the chart's box gets it as another name (`a` in the sidecar). Boxes `matthew_tree` adds have no box on the chart (Matthew's line past Zerubbabel, Rahab, Uriah), except Bathsheba, whose cross-reference names the chart's own box for her. The generator prints the camera verses whose text doesn't speak the name they light: 12 today, all deliberate, such as 7:9's total lighting the sons it counts, and Matthew 1:6's "her who had been Uriah's wife".

A box's verses are only as wide as those four sources. David's, for instance, are 1 Chronicles 2:15 and 3:1–9 and Matthew 1. Samuel and Kings reach a box only through its own ref.

## The V6 heir-spine variant

The same tree under an alternative layout. It answers one question: since the sheet is also the world for two per-verse camera readings (1 Chronicles 1–9 and Matthew 1:1–17), would a different layout let the camera stay at reading scale?

**How V6 differs.** It puts the *heir* (the child carrying the biggest descent) directly under its parent, with the other children beside it. The wall chart's centred layout instead centres a parent over the whole span of its descendants. Under V6, a line of descent is a straight vertical column and the sheet is smaller.

**Why the wall chart doesn't use it.**
- It costs birth order: the heir is moved first among his brothers.
- On the measure that prompted it, it is a wash. `tools/layout_lab.py`, run on 2026-10-17, scores the share of verses that fit in one frame at reading scale:
  - 1 Chronicles 1–9: 287 of 324 under V6, against 288 for the centred layout;
  - Matthew 1:1–17: 12 of 17 under V6, against 11.

**Where heir-under-parent is live.** Only in the Matthew 1:1–17 camera, through the production generator's own `arrange_spine` and `place_spine`. That is not the lab's V6: drawn as a whole sheet it would come to 27,090 × 13,418 px, against V6's 21,162 × 13,759. `generate_1chronicles_tree_svg.py --spine` re-runs 1 Chronicles under it for comparison.

**Rebuilding it.** No script writes this file.
- `tools/layout_lab.py` holds the V6 layout and the measurements for all seven variants tried (V0–V6).
- The V6 layout is `arrange_v(root, …, pack=False, heir_first=True)` followed by `place_v(root, 0, 0, spine=True)`. This pair is a drop-in replacement for `generate_ot_family_tree_svg.arrange` and `place`.
- To draw the sheet again, run the wall chart's drawing code with those two swapped in.

```
.venv/Scripts/python.exe tools/layout_lab.py   # print the measurements
```

## The 1–2 Chronicles family tree

The family tree of 1 and 2 Chronicles alone, without the grafts from the rest of the Old Testament.

It is a **frozen file with no generator.** It has been deployed since 2026-08-14, and no script in the repo has ever written it: `generate_ot_family_tree_svg.py` writes only `Old_Testament_family_tree`. `chronicles_tree.build(ot=False)` builds the Chronicles-only data, but nothing draws it as a sheet.

## The OT timeline

The same tree laid on a year scale: every box sits at its year, and a rail down the left gives the year.

- **The scale.** The axis is one monotone, piecewise-linear map. It opens out where the tree is dense in time, such as the monarchy, and closes up where nothing is recorded. The tick spacing shows where.
- **What is dated.** 87 of 1,227 people are dated. Undated boxes sit between their nearest dated ancestor and descendant.
- **The year rails.** Ussher's years run throughout, with Thiele's on a right-hand rail.
- **The boxes** are drawn by the wall chart's `draw_node`, so they carry the same generation number. Matthew's line runs on to Jesus at 64.
- **Data.** `chronology.py` holds the dates and their binding to the tree. `matthew_tree.py` carries the line on past Zerubbabel to Jesus.
- **Design record.** [design/ot-timeline.md](design/ot-timeline.md).

```
.venv/Scripts/python.exe generate_ot_timeline_svg.py   # rebuild the .svg and .html
.venv/Scripts/python.exe chronology.py                 # the dating coverage report
```

## The Tabernacle

The court, the tent and its furnishings, drawn to scale (14 px a cubit) from `sanctuary.py`, the one Tabernacle model the Exodus 25–27 and Numbers 1–4 pictures also draw from. East is to the right, as in the Exodus plan.

**The sheet.**
- The plan: the court with its hangings, its sixty pillars and the gate's four colours; the tent, with the veil and the door screen in their colours; and the ark, the altar of incense, the table with its twelve loaves, the lamp stand, the basin and the altar of burnt offering, each labelled.
- **Measurements** (a layer, on): the court's 100 and 50, the gate's 20, and the tent's 30, 10, and 10 and 20 either side of the veil.
- **The camp** (a layer, off): the Levites on the four sides (Numbers 3:23–38) and the twelve tribes beyond them by their standards, with their counts (Numbers 2, from `generate_numbers1_2_svg.CAMPS` and `COUNT`). It is not to scale, and says so.
- **In detail** (a layer, on): the Exodus 25–27 drawings (`generate_tabernacle.INSETS`) of the ark, the table, the lamp stand, the altar, the veil, the door screen, the boards, the curtains, the coverings and the materials, each drawn whole, without a verse's highlight.

**The cards** come from `sanctuary.PARTS`:
- each measurement, marked **stated** (the text gives it), **derived** (it follows from what the text gives: the tent's 30 cubits from twenty boards a cubit and a half wide) or **not given** (the lamp stand and the basin have no size at all), with its verse;
- where the part stands, marked the same way. The text says which side a thing stands on, or what it stands between, but gives no distances inside the court, so the plan's spots are one common arrangement;
- what it was made of, and who carried it on the march (Numbers 4);
- its verses, grouped as commanded, made, set up and named elsewhere;
- links: a part to its drawing and back, and the ark and the mercy seat to each other.

Tapping a Levite or tribe card on the camp layer opens what they camped by and carried. Opened from a verse, the sheet starts on the parts that verse names: from Exodus 25:10, the ark.

**The model.** `sanctuary.py` keeps the plan in cubits (x east from the west hanging, y south from the north) with the Exodus plan's own literals. Making it the one model corrected three things in the published pictures:
- **The pillars.** There are now sixty, one every five cubits round the court with each corner counted once: 20, 20, 10, and on the east 3, 3 and 4 for the gate at 20–35 (Exodus 27:10–16). The Exodus 25–27 plan drew five uneven posts across the gate while its highlight ringed four others, and its per-side rings counted the corners twice.
- **The Numbers 1–4 courts.** Numbers 1–2 had the altar 12–17 cubits inside the gate, the basin at 27 and the tent 14 cubits from the west; Numbers 3–4 drew a court of the wrong shape with no altar, basin or veil. Both now draw the model.
- **WEB's wording** on the Exodus drawings: brass, lamp stand, sea cow hides, sockets, fillets.

```
.venv/Scripts/python.exe generate_tabernacle_reference.py   # rebuild the .svg, .json and .html
.venv/Scripts/python.exe -m unittest test_sanctuary          # the model's counts and verses
```

## The Land of Israel

An atlas of the land from Sidon to Kadesh Barnea and from the Great Sea to Bashan and Moab, with the places the WEB names, each at the site it is identified with. North is up, at 2,400 px a degree of latitude, about 21.6 px a km.

**The data is `gazetteer.py`, all point facts.** Each point of a line is one named place (a beach, cape, river mouth, bridge, spring, dam or tell) whose coordinate is a single fact from Wikidata (CC0) or Wikipedia. The comment beside it names the place and its Wikidata item, or marks it `~` as our own interpolation. The stretch north of Ras Naqoura is `acts_geography`'s, whose comments name the places without their Wikidata ids. No line is traced from OpenStreetMap, Google or an atlas; `test_gazetteer` checks the comments, and that no point copies a point of `generate_tribal_maps` or `generate_acts1518_svg`'s atlas-traced maps.
- **The coast** is today's: `acts_geography.MAIN_COAST` from south of Beirut to Ras Naqoura, then `COAST_SOUTH` to the mouth of the brook of Egypt.
- **The lakes** are at high water: the Salt Sea as it stood about 1900, its southern basin full, and Huleh before it was drained in the 1950s.
- **The rivers** run from source to mouth, and each mouth is a point of the coast, a lake or another river, so the lines meet: the Jordan and its three headstreams, the Yarmuk, the Jabbok, the Arnon, the Zered, the Kishon, Me Jarkon (the Yarkon) and the brook of Egypt.
- **224 places** (`SITES`). Each has its WEB name and other names, the tell, ruin or village it is identified with, its Wikidata item, its certainty, why, its tribe and Levite or refuge status from Joshua 13–21, its namesakes and its verses. Seven places in and against Jerusalem (`JERUSALEM`, among them the valleys of Hinnom and Rephaim) are kept for a city page and not drawn, and three north of the sheet (`BEYOND`: Gebal, Aphek, the entrance of Hamath) are for the Joshua 13–19 map. `UNPLACED` holds 67 notes on the places left off, with the reason: no agreed site, no point fact for the one proposed, or a name the WEB doesn't use.
- **Certainty** is `known` (the name survives, or inscriptions or excavation fix it), `probable` (most scholars agree) or `possible` (one proposal of several, and `why` names the others). On the sheet a known site is a filled dot, a probable one a thick ring, and a possible one a thin ring.
- **Verses.** A place's verses are every verse its names find in the WEB, less its `skip`: the verses where the word is a namesake, a person, a tribe, a lake named after the town, or a common word. The names find 3,797 verses across the 231 places (2,862 different verses); each was sorted, place by place, the sort was checked twice (2026-10-28; Joshua 13–19's new places were sorted and checked by script on 2026-10-29), and 865 are skipped. `refs` are the hand-checked ones a card lists when a place has many. A place's founder in a genealogy ("Ashhur the father of Tekoa") counts as the town.

**The sheet.**
- The base: the sea, the land, the lakes, the rivers, the lands' and the waters' names, and the places, labelled by a greedy placer that keeps every name clear of every other name and dot.
- **Text by size.** At the whole sheet the lands and the Great Sea show; on a phone the narrow lands (Sharon, Philistia, the Arabah, Zin) and the other waters come in at the first zoom. Then the 30 chief places (28 cities, and Mounts Hermon and Carmel) from about twice that; then the mountains and the towns with eight or more checked verses; and the rest from about six times. The lands' and the tribes' names fade as the towns come in.
- **The tribes** (a layer, off): each tribe's towns under one soft colour, its name at their middle, and rings for the Levite cities and the cities of refuge. No border is drawn: the text names towns and landmarks, not lines. A town in two lots (Beth Shemesh in Judah's and Dan's, Beersheba in Judah's and Simeon's) takes both colours.
- **In Jesus' day** (a layer, off): a ring round each place the Gospels or Acts name, and the names Judea, Phoenicia and the Decapolis.
- Huleh and the Yarmuk, which the Bible doesn't name, are drawn without a name; a tap on them opens their cards.

**The cards.** A place's card gives the site it is identified with, flagged known, probable or possible; why that site; how many verses name it; its other WEB names; its tribe in Joshua; its distance and direction from Jerusalem; its namesakes, which link to one another; what the dot marks and its Wikidata item; and its verses. A water's or a land's card gives its verses, the first in each book where there are many. A tribe's card names its towns and its chapter in Joshua. Opened from a verse, the sheet starts on the places that verse names, or failing those the places its chapter names: from Ruth 2:4, Bethlehem; from Ruth 1:3, which names none, the Bethlehem and Moab of Ruth 1. A chapter that names no place (Ruth 3) opens on the whole sheet.

```
.venv/Scripts/python.exe generate_israel_atlas.py      # rebuild the .svg, .json and .html
.venv/Scripts/python.exe -m unittest test_gazetteer     # the places, their verses and the lines
```

## Kings and prophets

The kings of Israel and Judah from Saul to the exile, with the prophets beside them, the foreign kings they dealt with and the judges before them. Time runs down the sheet.

**Two chronologies, never mixed.** The year line is Ussher's, the house count of the family tree and the timeline: its reigns are `chronology.BIND`'s, read by `kings.py` and checked against it by `test_kings`. Three reigns BIND doesn't hold have their own years with their sources (David's, Ish-bosheth's, and Tibni's, derived from 1 Kings 16:15–23). Thiele's years (The Mysterious Numbers of the Hebrew Kings, 1983) stand beside each reign in blue, in whole years as the Thiele column of Wikipedia's "Kings of Israel and Judah" gives them, with his coregencies on the cards. Thiele dates no reign before the division but Solomon's, so Saul and David have none.

**The sheet.**
- **The year line** stretches where reigns are short, so every bar carries its name: Zimri's seven days get the room of a year. The rail on the left gives the year, every fifty years ruled across.
- **The reigns:** the united kingdom across the middle, then Judah on the left and Israel on the right. A bar's colour is the text's verdict on the king: did right, right but, did evil, or none. A reign beside another stands in the half of its column (Jehoram beside Jehoshaphat, Tibni against Omri, Ish-bosheth in David's years at Hebron). Ussher's interregna in Israel are hatched.
- **The prophets** beside their kingdom: a writing prophet from the first to the last king his book's opening verse names, a narrative prophet over the reigns of the kings the histories set him beside. Where that overstates him, his span is the verses' own (Samuel died before David reigned; Jeremiah began in Josiah's 13th year; Amos's Uzziah and Jeroboam reigned together). Ezekiel, Daniel, Haggai and Zechariah stand at the years their verses give. Joel, Obadiah, Nahum, Habakkuk and Malachi name no king and are listed at the foot.
- **The nations** between the two kingdoms: each foreign king at the year the text dates him by, a filled mark for a regnal year, accession or death, a hollow one when the text gives no year and he stands in the reign. Judah's dealings are labelled on the left of the column and Israel's on the right, each crowded run spread up and down around its years. In Ussher's count an event is at its king's regnal year, or at Ussher's own year where he reckons otherwise (`kings.EVENT_USSHER`: Samaria's fall in 721, Jerusalem's in 588).
- **The judges** in a strip at the top, in order, with the years the text gives each and the enemy before them. They are not on the year line: their years, with the oppressions, add up to more than the 480 of 1 Kings 6:1.
- **Landmarks:** the kingdom divided, Samaria falls, Jerusalem falls, the return under Cyrus.

**The cards.**
- **A king** gives both counts' years; the text's length (and his age), the accession formula, his father and mother, the verdict, how the reign ended and where he was buried, each with its verse; where the texts disagree, both figures; his passages in Samuel or Kings and in Chronicles; the prophets and events beside him; and a link to his box on the OT family tree. Ish-bosheth, Athaliah and Tibni reigned outside the line each realm counts, so they take no number, and Saul, David and Solomon are the 1st, 2nd and 3rd.
- **A prophet** gives the verse that dates him and its words, the kings it names, his verses and, for a writing prophet, his book.
- **A foreign king's dealing** gives the dating words and verse, Ussher's year, and the modern date with its source, which stands for Thiele's count: his synchronisms don't all follow from a king's whole-year reign.
- **A judge** gives the years, the enemy before, the tribe and the story.

Opened from a verse, the sheet starts on what the verse names, then on the reigns and books whose passages include it: from 2 Kings 18:5, Hezekiah; from Isaiah 1:1, Isaiah; from Judges 4:4, Deborah.

```
.venv/Scripts/python.exe generate_kings_reference.py   # rebuild the .svg, .json and .html
.venv/Scripts/python.exe -m unittest test_kings          # BIND's years, the verses, the ties
```

## Paul's journeys

The four journeys of Acts on one sheet, from Rome to Damascus: the first (Acts 13:4–14:26), the second (15:36–18:22), the third (18:23–21:17) and the voyage to Rome (27:1–28:16).

**Point facts, no traces.** The coasts beyond the Levant are `mediterranean.py`'s: about 2,500 points, each a named place's own Wikidata coordinate (or marked `~`), gathered and checked against Wikidata by script on 2026-10-28. Southern Asia Minor, Syria and Cyprus are `acts_geography`'s, and the Levant `gazetteer`'s. The places, roads and sea courses are `journeys.py`'s: a place's point is its Wikidata item's (Lystra's is Zoldera's, since the item sits 13 km off), and a road's points are named stations on or by it. A course is our own `~` points: by sea, placed only where Acts says the ship passed (under the lee of Cyprus, opposite Chios) or where the sea leaves one way past a cape or island; by land, where the text doesn't give the way, only to keep the dotted line on land and through the one way a pass or isthmus leaves (Tempe, Thermopylae, the Isthmus). A course names no station the text doesn't, and its leg's card says the line is ours. `test_journeys` checks that no voyage, as drawn, crosses more than 6 km of land. The coasts are today's: Ephesus and Miletus stood on harbours that have since silted up, so their legs end inland.

**The sheet.**
- **The journeys**, a layer each and all on, in their own colours: a solid line by land, dashes by sea, dots where the text doesn't state the way or the stop (Paul went up and greeted the assembly, 18:22; the upper country, 19:1; the drift to Malta, 27:18–28:10). An arrow on each leg points on. Where journeys share a stretch their lines run side by side, meeting again at the stops; a tap takes the line nearest the finger. A stop the text names only as a land (Mysia, 16:7–8; Macedonia, 20:1) has no dot; the line runs to its name.
- **The places**, a dot each, filled where the site is known, a thick ring where it is probable, a thin ring where only possible, sized as chief cities, the journeys' stops and the rest; the roads under them, faint, including the common road from Antioch of Pisidia to Ephesus, which isn't drawn as Paul's (Colossians 2:1).
- **The lands** Acts and the letters name, and three waters: the sea off Cilicia and Pamphylia, the Adriatic Sea (in Paul's day the open sea between Crete and Sicily) and the Syrtis.
- **The seven assemblies** (a layer, off): Revelation's seven, numbered in the order of its letters, joined in that order, and Patmos.
- **The letters** (a layer, off): under each place, the letters addressed to it, and a square where 1 Corinthians says it was written (Ephesus, 16:8). Galatians and Titus stand under Galatia and Crete.

**The cards.**
- **A place** gives the site, its certainty and why, its other names, where it is, its letters, its stops on each journey and every New Testament verse that names it (two places of one name, the Antiochs, take only their checked verses), with chips to the legs that reach it.
- **A leg** gives the journey, its number, by land or sea, what Acts says (and Paul's own words, where a letter tells of it), the road it follows and how sure that is, or that the line is ours, its length as drawn, and buttons to the leg before and after. Its id is its journey and its two places (`journey2-troas-samothrace`), so a shared link survives a stop added before it.
- **A journey** (its line in the key) gives its legs, its length as drawn and its passage.
- **A letter** gives whom it is addressed to and where it was written, where the letter says.

Opened from a verse, the sheet starts on the places and legs the verse names (Acts 16:11: Troas, Samothrace, Neapolis and the two legs between), then on the legs, assemblies and letters whose passage it falls in (Romans 5:3: Romans; Revelation 2:10: Smyrna), then on what its chapter names.

```
.venv/Scripts/python.exe generate_journeys_reference.py   # rebuild the .svg, .json and .html
.venv/Scripts/python.exe -m unittest test_journeys          # the places, the legs, the coasts
```

