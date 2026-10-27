# Reference charts

`web/visuals/reference/` holds the standalone wall charts. Nothing in them is tied to a verse.

Each chart is an SVG plus an `.html` viewer page. The viewer adds drag-to-pan, wheel zoom, fit / + / − buttons, and a name search that steps through the hits (↑ ↓). All four viewers are the same page; the two generators write theirs from `generate_ot_family_tree_svg.VIEWER`. You can also open an `.svg` directly in a browser.

## Status (D14)

- **Deployed.** All four charts deploy with the site at `https://theoria-bible.net/visuals/reference/<file>`. `web/` is served as it is, and Publish commits `web/visuals/`, so a change to a chart ships like any other visuals change.
- **Not linked.** Nothing in the web app links to them, because which family-tree version belongs in the app hasn't been chosen. Anyone with the exact URL can open one.
- **Not indexed.** `build_manifest.py` only indexes `web/visuals/<Book>/<chapter>/` and the flat `web/visuals/` root, so the charts never become manifest keys.
- **None is archived.** The V6 heir-spine variant stays until the choice is made.
- **Cost.** The charts are 8 deploy files.
- **Later.** A Charts entry in the app is on the [roadmap](../ROADMAP.md), once the version is chosen.

| Chart | Files | Size | Built by |
|---|---|---|---|
| [The Old Testament family tree](#the-old-testament-family-tree) | `Old_Testament_family_tree.svg` / `.html` | 26,946 × 16,736 px, about 1.3 MB, 1,254 boxes | `generate_ot_family_tree_svg.py` |
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
- The 1 Chronicles camera uses a third layout, `layout_regions.py` (`svg_chronicles_world.LAYOUT = "regions"`). Adam to Israel's sons form one fan in strict generation rows, and each son's descendants stand in a titled panel under it, reached by a routed line; the routes share one trunk under the fan, so they draw as one thin branching line. A wife stands beside her husband, on the side away from his brothers where she can, and a house that gathers people is a small italic label on the line; so are the two houses that head panels, which keep Israel's sons' row to the twelve. `generate_1chronicles_tree_svg.py --centred` and `--spine` re-run the camera under the other two layouts for comparison.

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
