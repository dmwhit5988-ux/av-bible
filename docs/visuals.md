# Visuals

Every illustrated verse shows one animated SVG picture on the stage while the verse is narrated. Each picture is written by a Python generator (`generate_*.py`), indexed by `build_manifest.py` into `web/visuals/manifest.json`, and looked up by the web app (`web/js/visuals.js`), which fetches it as `/visuals/manifest.json`.

As of 2026-10-17: 2,241 illustrated verses in 73 chapters of 11 books, shown by 2,116 distinct pictures, from 25 registered generator families. Every illustrated chapter is complete.

## Format

- **SVG only, animated with SMIL** (`<animate>`, `<animateTransform>` and so on). There is no script, no CSS animation and no raster image. The web stage shows a picture in an `<img>`, so each file must be self-contained: no external files and no web fonts. Text uses the Georgia stack (`svg_surface.FONT_FAMILY`).
- **Canvas 1024 × 576** (`generate_tabernacle.W, H`). Every verse SVG has `viewBox="0 0 1024 576"`, and the stage letterboxes it.
- **Motion plays once and holds.** The exceptions loop forever: the Exodus 25–27 pulse and the Genesis 3:24 sword (99 files).
- There are no still or reduced-motion variants (D4).
- `build_manifest.py` still accepts `.webp`, `.gif`, `.png` and `.jpg`, but none exist and none should be added.

## Files and names

| What | Path |
|---|---|
| One verse | `web/visuals/<Book>/<chapter>/<Book>_<chapter>_<verse>.svg`, with underscores for the spaces in a book name, e.g. `web/visuals/1_Chronicles/2/1_Chronicles_2_5.svg` |
| A verse range | `web/visuals/<Book>/<chapter>/<Book>_<chapter>_<v1>-<v2>.svg`, e.g. `Numbers_32_16-32.svg`. It is one picture for every verse in the range that has no file of its own. None exist yet. |
| A whole chapter | `web/visuals/<Book>/<chapter>/<Book>_<chapter>.svg`, the key `Book_c`, used for any verse with no key of its own. None exist. |

- Generators build the path with `generate_tabernacle.out_path(book, chapter, filename)`, under `config.VISUALS_DIR`.
- The site serves the folder at `/visuals/`, so a file's URL is its path without `web/`.
- Verse numbers come from `passages.verse_numbers(book, chapter)`, the WEB versification. A generator iterates those numbers rather than a hard-coded chapter length.
- A file name never carries a translation suffix or `.still`. `build_manifest.py` and `test_registry` flag either as a retired leftover.

## The manifest

Run `.venv/Scripts/python.exe build_manifest.py`. Publish runs it as step 1, and SVG Studio's **Save + manifest** runs it too. It writes schema v2:

```json
{
  "version": 2,
  "entries": {
    "Acts_13_1": [
      {"file": "Acts/13/Acts_13_1.svg", "kind": "map", "animated": true}
    ]
  }
}
```

| Field | Meaning |
|---|---|
| key | `Book_c_v` (a verse) or `Book_c` (a chapter), book name with underscores |
| `file` | Path relative to `web/visuals/`, forward slashes |
| `kind` | `data-kind="…"` on the SVG root if present, else the owning family's `kind` in `svg_generators.json`, else `infographic`. Today: diagram, genealogy, map, chart. |
| `animated` | Whether the SVG contains a SMIL element (`svg_freeze.svg_is_animated`) |

**What it reads.** Image files in `web/visuals/<Book>/<chapter>/`, and in the flat `web/visuals/` root.

**What it skips.**
- Anything that isn't an image: `manifest.json`, and the chart viewers' `.html`.
- Dot-folders.
- `web/visuals/reference/`: it has no chapter folders, so its charts never become keys. See [reference-charts.md](reference-charts.md).
- Any `.still.svg`.
- A range file whose range runs backwards, or whose chapter WEB doesn't have.

**How it fills a range.**
- A range file supplies each WEB verse in its range. Verses WEB doesn't have are left out, with a warning.
- A verse's own file beats the range, with a warning.
- Where two ranges overlap, the name that sorts first wins, with a warning. `video_render.resolve_svg` picks the same file.

**How it shares identical copies.**
- Walking each chapter in verse order, a verse whose SVG is byte-identical to the previous verse's is pointed at the first file of that run. The copies stay on disk.
- This is recomputed on every build, so a run splits by itself once a generator makes two verses differ.
- A range file is never re-pointed at a copy.
- A family with `"replay_identical": true` in the registry opts out. None does today.
- Today 125 verses share the previous verse's picture. Numbers 32:16-32 is one picture.

**What it reports.**
- `[WARN]` lines for each range problem above.
- `[OK]` with the number of verses that share a picture.
- `[WARN]` listing any retired variant files (translation-suffixed or `.still.svg`) under `web/visuals/`.
- Finally the key count and the number of animated records.

## How the web app uses it

- `VisualStage.findVisual` looks up the verse key, then the chapter key, and prefers an `.svg` record.
- `VisualStage.illustratedChapters` marks every chapter with at least one key. Those chapters get the ✦ in the pickers and in the ✦ Illustrated list.
- **A verse with no picture** shows the book gradient, the reference and one line, with a **✦ See illustrated chapters** button that opens the list (`showNotIllustrated` in `web/js/app.js`). The line reads "Genesis 12 isn't illustrated yet." for a chapter with no pictures, and "This verse isn't illustrated yet." inside an illustrated chapter. It is built into the page, so it costs no deploy file.
- The manifest is fetched with `cache: "no-cache"`, so returning visitors see a new deploy at once.

## Playback rule: the same picture keeps playing (D17)

- When the next verse shows the same file as the one before (a range file or a shared identical copy), the stage leaves the `<img>` alone. A running animation keeps running, and a finished one stays finished. Nothing is downloaded again.
- The picture restarts only when it changes.
- Starting playback on the verse already shown (Play from stopped, or a tap on that verse) restarts its picture, so it stays in step with the narration. The stage does this by loading the file with a fresh `?r=` query.
- Coming back from idle or from an un-illustrated verse loads the picture fresh, and it plays once.
- **Video Studio follows the same rule.** A verse that shows the previous item's picture carries on that picture's clock, and the `replay_identical` opt-out applies there too ([video-studio.md](video-studio.md)).
- **Two Studio views don't follow it yet.** SVG Studio doesn't know range files. The Studio's interim player stage (`visual_stage.py`) finds files on disk, doesn't look up range files, and restarts the picture on every verse. Both are on the [roadmap](../ROADMAP.md).

## Generators and the registry

- **Generators are the source of truth.** Re-running one rewrites its whole family from the Python spec, so **never hand-edit a generated SVG**: the next run throws the edit away. To change a picture, edit the generator, re-run it, rebuild the manifest, check it, then Publish.
- **`svg_generators.json`** lists every family. Each entry has `label`, `book`, `chapters`, optionally `verses: [lo, hi]` when the family owns only part of a chapter (Genesis 11 is split between two families), `generator`, `spec` (the files and what in them to edit), `kind`, and optionally `replay_identical`.
- **`svg_registry.py`** loads it. `owner_of(book, chapter, verse)` returns the owning family. Always pass the verse when you know it.
- **Who reads the registry:**
  - SVG Studio routes "edit this verse" to the spec and offers **Re-run generator** ([svg-studio.md](svg-studio.md));
  - `build_manifest.py` takes `kind` and `replay_identical` from it;
  - `video_render.py` reads `replay_identical`.
- **`test_registry`** checks four things: every generator and spec file exists (and imports), no two families claim a verse, every verse SVG under `web/visuals/<Book>/<chapter>/` has an owner, and no retired variant file is back.
- **A new family** needs its generator and a registry entry in the same change.

## House rules

**Less is more.** The verse is narrated, so the picture never restates it.
- No caption line, no prose block, no explanatory footer or notes panel, and no verse counter or bead track.
- Use names, numbers, shapes and one- or two-word labels on the drawn parts.
- Reveal a detail only on the element the current verse is about.
- Spend the space this frees on bigger type and breathing room, not on more content.
- The one widening is in the argued letters (Romans): short engraved phrases of 2–7 words, in WEB wording, at hinge verses only, roughly one per 10–15 verses. Never sentences ([design/romans.md](design/romans.md)).

**The drawing rules.**
- **Draw once, then hold.** A thing animates only on the verse it first appears. This applies to growth too: when a road gains a stretch, only the new stretch draws itself in.
- **Highlight by pulsing the outline, never by redrawing it.**
  - Use `SvgCanvas.pulse_outline`, `pulse_rect` or `pulse_ellipse` (in `svg_surface.py`).
  - Pass `first=` true only on the verse the element becomes current.
  - Keep `traced()` for reveals where the drawing-on is the point, such as rivers, routes and borders.
- **Measure every box.** `svg_vocab.text_w()` reads real Georgia advance widths through PIL, so rings, chips and labels are cut to fit their text.
- **WEB wording** (or a tight paraphrase) for any phrase on the canvas.
- **No empty boxes on a tree camera.** In the 1 Chronicles 1–9 and Matthew 1:1–17 tree flights, a drawn box carries its name whenever it is on screen at camera scale `NAME_MIN_SCALE` (0.12) or closer at any moment of the flight or the rest it lands on. Below that scale a box is a speck under 10 px and stays bare. `svg_chronicles_world._flight_seen` measures this from the keyframes `_camera_group` actually writes, and `_seen_scale` turns it into the names. There is no separate name budget: the per-verse node cap (`MAX_NODES`, 260) bounds boxes and names together, and the cull gives the cap first to what the flight shows largest.
- **Tree-camera lines keep a floor.** Box edges and static connectors take their stroke width from one group per nominal width (`svg_chronicles_world._stroke_group`). Each group's width is animated on the camera's own schedule, so below scale `STROKE_HOLD_SCALE` (0.68) a stroke stops thinning, and it never drops under `STROKE_MIN_PX` (1 screen px). On a wide pull-back the shape of the tree stays visible.
- **Past the cap, outlines.** `MAX_NODES` limits the boxes that can carry names. Every other box the flight puts on screen at any scale is still drawn, as an outline with its connector and no name, so a wide pull-back shows the whole tree. The busiest verse (1 Chronicles 2:2) draws about 1,050 boxes; that plays smoothly on the owner's iPad.

**The audit targets.** For every family:
- Zero overlapping text boxes.
- Zero text wider than its box.
- Zero text off the canvas.

In the argued letters (Romans and Hebrews) there is a fourth target: no run of identical verses longer than three. There, where each verse moves the argument, a hold of two or three is draw-once-then-hold working, and a longer one is stagnation ([design/romans.md](design/romans.md), [design/hebrews.md](design/hebrews.md)). Elsewhere a long hold can be deliberate: a range file, or identical copies shared under D17, such as the 17 verses of Numbers 32:16–32 on one picture.

`tools/audit_heb.py` checks the Hebrews set for off-canvas text, overlaps and identical runs. A Studio lint that runs the overlap, overflow and off-canvas checks for every family is on the [roadmap](../ROADMAP.md).

## The figure vocabulary: `svg_figures.py`

People, creatures, growing things and made things are drawn once, in `svg_figures.py`, and new work takes them from there. The module docstring sets the conventions:

- **Geometry is tagged by material and knows nothing about colour.**
  - `palette(ink, page)` builds the paint table from a book's own two colours.
  - `draw(c, parts, x, gy, s, ink, page, …)` paints a figure onto an `SvgCanvas`.
  - `style=` passes a whole table instead, usually a `palette()` with a few materials changed (`garden_paint()` in `generate_genesis2_svg.py`).
- **One unit.** One unit is 1/100 of an adult man's height. The `UNIT` table states each subject's real size against a man, so two figures at the same scale are at true relative size.
- **Feet on zero.** Local y runs up from the figure's own ground line. `place()` drops it on the canvas at any size, facing either way.
- **Real coordinates.** `place()` returns points, not a transform. Stroke weights don't scale with the figure, and a figure can be drawn in with `traced()` or `pulse_outline()` like any other mark.
- Bodies go through `smooth()` (a Catmull-Rom curve) and limbs through `taper()`. Boards and masonry are raw point lists, because the curve fitter turns a beam into a bolster.

`svg_vocab.py` holds the smaller shared marks (arrows, struck labels, tally rows) and `text_w()`. `git grep -l svg_figures` lists the generators that use the vocabulary.

## Reference charts

`web/visuals/reference/` holds the wall charts: the OT family tree, its V6 heir-spine variant, the 1–2 Chronicles tree and the OT timeline. They deploy with the site, but nothing links to them. See [reference-charts.md](reference-charts.md).
