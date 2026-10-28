# Reference charts

`web/visuals/reference/` holds the standalone wall charts. Nothing in them is tied to a verse.

Each chart is an SVG plus an `.html` viewer page. You can also open an `.svg` directly in a browser.

**The viewer.** The two generators write their viewer pages with `reference_viewer.page()`. Every page offers:
- one finger or the mouse to pan, two fingers to pinch, the wheel to zoom, and fit / + / − buttons that zoom about the middle of the screen;
- a name search. The search box is 16 px, because iOS zooms the whole page when a smaller field takes focus.

A chart whose generator also writes a **sidecar** (`<stem>.json`, today only the family tree's) gets more:
- **A tap on a box** opens its card. On a phone the card is a bottom sheet; from 700 px wide it is a side panel.
- **Search** lists the matches, each with its relation, so the nine Azariahs can be told apart. Whole names come first, then the start of a name, then anywhere in one, then a name found only in a box's note. A box's other names count as its names: "Jacob" finds Israel. ↑ ↓ step through the matches.
- **The card** gives the relation, the generation, the Ussher years where the chronology dates the person, the box's note and cross-references, the family, "Line to Adam", and the verses. The family is:
  - the parent, or both where the mother is on the wife line;
  - wives and children;
  - the men only joined under him (a dashed join, "as the text implies"), apart from his sons;
  - the family a reference chip stands in.
- **Line to Adam** outlines every box up the line and frames them. A wife hangs under her husband, so his line isn't hers. Hers runs from her reference chip in her father's family where she has one (Leah's through Laban), and otherwise the card offers none.
- **A verse chip** shows the verse, read from `/bibles/WEB/`. Inside the app, "Open in Theoria" posts `{type: "theoria:goto", book, chapter, verse}`, and the app closes the chart and goes to that verse without playing it.
- **The address** keeps the selection (`#id=<id>`), so ↗ opens and shares what is on screen. The app opens a chart at `#at=<Book>.<chapter>.<verse>`, and the page starts on the names that verse speaks.
- **Escape** closes the results, then the card, then (in the app) the chart.

Without a sidecar (the OT timeline), the search steps through the sheet's own text and zooms each hit to at least full size, where names are 15 px. The V6 and 1–2 Chronicles pages are older copies of the viewer, with no pinch and no zoom-to-hit, because nothing writes them.

## Status

- **Deployed.** All four charts deploy with the site at `https://theoria-bible.net/visuals/reference/<file>`. `web/` is served as it is, and Publish commits `web/visuals/`, so a change to a chart ships like any other visuals change.
- **Linked: the OT family tree only.** The app's **Reference** button, in the header beside ✦ Illustrated, lists the charts in `REFERENCES` in `web/js/app.js`. Today that list has just the OT family tree. A chart opens full screen over the app, in a frame under a bar with ← Back and ↗:
  - the frame keeps the passage, and any narration playing, as they were underneath;
  - the installed home-screen app has no Back button of its own, so the bar provides one;
  - ↗ opens the chart's page on its own, at the address you can share.
  The V6 heir-spine variant and the 1–2 Chronicles tree were experiments, and the OT timeline isn't in the list either. All three are unlinked, but anyone with the exact URL can open them.
- **Adding a chart to the list** is one entry in `REFERENCES` (title, one-line blurb, root-absolute `href`). It is web-app code, so it is committed by hand, and the chart's own files ship through Publish.
- **Not indexed.** `build_manifest.py` only indexes `web/visuals/<Book>/<chapter>/` and the flat `web/visuals/` root, so the charts never become manifest keys.
- **Cost.** The charts are 9 deploy files, the tree's sidecar among them. The Reference list itself costs none, because it is part of `app.js`.

| Chart | Files | Size | Built by |
|---|---|---|---|
| [The Old Testament family tree](#the-old-testament-family-tree) | `Old_Testament_family_tree.svg` / `.json` / `.html` | 26,946 × 16,736 px, about 1.3 MB, 1,254 boxes; the sidecar is about 215 KB | `generate_ot_family_tree_svg.py` |
| [V6 heir-spine variant](#the-v6-heir-spine-variant) | `Old_Testament_family_tree_V6_heir_spine.svg` / `.html` | 21,162 × 13,759 px, about 1.4 MB | no script writes it; its layout is in `tools/layout_lab.py` |
| [The 1–2 Chronicles family tree](#the-12-chronicles-family-tree) | `1-2_Chronicles_family_tree.svg` / `.html` | 19,777 × 13,754 px, about 1 MB | none: a frozen file |
| [The OT timeline](#the-ot-timeline) | `Old_Testament_timeline.svg` / `.html` | 65,030 × 12,230 px, about 1.4 MB, 1,269 boxes | `generate_ot_timeline_svg.py` |

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
