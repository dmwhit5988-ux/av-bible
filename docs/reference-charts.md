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
| [The Old Testament family tree](#the-old-testament-family-tree) | `Old_Testament_family_tree.svg` / `.html` | 26,935 × 15,847 px, about 1.4 MB, 1,266 boxes | `generate_ot_family_tree_svg.py` |
| [V6 heir-spine variant](#the-v6-heir-spine-variant) | `Old_Testament_family_tree_V6_heir_spine.svg` / `.html` | 21,162 × 13,759 px, about 1.4 MB | no script writes it; its layout is in `tools/layout_lab.py` |
| [The 1–2 Chronicles family tree](#the-12-chronicles-family-tree) | `1-2_Chronicles_family_tree.svg` / `.html` | 19,777 × 13,754 px, about 1 MB | none: a frozen file |
| [The OT timeline](#the-ot-timeline) | `Old_Testament_timeline.svg` / `.html` | 64,880 × 11,943 px, about 1.5 MB, 1,281 boxes | `generate_ot_timeline_svg.py` |

## The Old Testament family tree

One contiguous family tree of the whole Old Testament, rooted at Adam.

**How it is built.**
- The data is `chronicles_tree.py`, which welds the 1 and 2 Chronicles genealogies into one tree, and `ot_grafts.py`, which grafts on every other person the Old Testament gives a join for.
- Names and spellings are the WEB's, unmodified.
- The 1 Chronicles 1–9 and Matthew 1:1–17 verse pictures are cameras over this same tree (`svg_chronicles_world.py`, `svg_matthew_world.py`). Matthew 1:18–25 is a figure stage instead (`svg_matthew_nativity.py`).
- The wall chart and the 1 Chronicles camera use the centred layout (`generate_ot_family_tree_svg.arrange` and `place`). The Matthew camera lays the tree out with the heir under its parent (`arrange_spine` and `place_spine` in the same module), so his line of descent is a straight column.

**Reading it.** The legend is on the sheet.

| Mark | Meaning |
|---|---|
| solid line | father to son, as the text states it |
| dashed line with an open bead | a join the text implies but does not state; the note on the box says what the inference is |
| doubled line | a wife, or the mother the line is reckoned through |
| gold line inside a box | a cross-reference: this person is named elsewhere on the sheet, and the line says how. The note is written in both boxes. Pairs close enough together are also tied by a gold arc. |
| box outline | gold for a king (with a crown), jade for a priest or Levite, rose for a woman the text names, grey for a house or company |
| small number, bottom right | the generation from Adam |

```
.venv/Scripts/python.exe generate_ot_family_tree_svg.py   # rebuild the .svg and .html
.venv/Scripts/python.exe chronicles_tree.py               # audit the tree without drawing it
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
- **What is dated.** 87 of 1,255 people are dated. Undated boxes sit between their nearest dated ancestor and descendant.
- **The year rails.** Ussher's years run throughout, with Thiele's on a right-hand rail.
- **Data.** `chronology.py` holds the dates and their binding to the tree. `matthew_tree.py` carries the line on past Zerubbabel to Jesus.
- **Design record.** [design/ot-timeline.md](design/ot-timeline.md).

```
.venv/Scripts/python.exe generate_ot_timeline_svg.py   # rebuild the .svg and .html
.venv/Scripts/python.exe chronology.py                 # the dating coverage report
```
