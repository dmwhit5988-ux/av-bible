# AV Bible — "Studio" Plan

Turning the Windows desktop app into the content **studio** for the project,
while the web app stays the lean, static **distribution** target.

> Status 2026-07-09: **built.** All three features + the SVG Studio
> (design: `SVG_STUDIO_DESIGN.md`; build: commits 9a89129…2376560) are
> implemented. This document remains as the original plan of record.

## The core idea

Everything that *produces* assets is Python and cannot run in a browser:
`edge-tts` (neural MP3s), `svg_surface.py` + the `generate_*_svg.py` geometry,
Pillow, and the `pronunciation.respell()` layer. The web app is a deliberately
dumb consumer — it reads `visuals/manifest.json` and `web/audio/manifest.json`
and plays whatever is there.

So we concentrate **authoring** in the PC app and keep the web app as the
**publish** target. This doesn't fight the architecture; it completes it.

```
PC app  = STUDIO  (author + render + preview + stage for deploy)
Web app = CONSUMER (static, manifest-driven, no build step)
Bridge  = shared asset dirs + manifests, mirrored into deploy_bundle/
```

---

## Feature A — Pronunciation Studio as a built-in feature

**Effort: small. Most of it already exists.**

`pronunciation_tool.py` is already a complete standalone tkinter `App` that
shares the exact production path (`tts_engine.synthesize(..., apply_respell=
False)`, `pronunciation.scan_proper_nouns`, `save_names`). "Integrating" it is
just surfacing it from the main app.

**Plan**
- Add a "Pronunciation Studio" button/menu item in `app.py` that opens the
  existing UI as a `tk.Toplevel` — same pattern as `SettingsDialog` and
  `FullscreenStage`.
- Refactor `pronunciation_tool.App` to accept an optional parent instead of
  always creating its own `tk.Tk()` root. Keep `python pronunciation_tool.py`
  working as a standalone entry point.
- Hand-off nicety: open the tool pre-loaded on the book/chapter the reader is
  currently showing.

**Gotchas**
- The tool holds its own `AudioPlayer` and a working copy from
  `pronunciation.load(force=True)`. When both reader and tool are open, a Save
  in the tool should prompt the reader to reload the pronunciation list (live
  playback already picks up changes on the next synth because the cache is
  keyed on the respelled text).

**Model: Haiku 4.5** for the wiring/refactor → **Sonnet 5** if the reader↔tool
state sync gets fiddly.

---

## Feature B — Verse-by-verse SVG Studio (Option 3: verse-aware orchestrator)

**Effort: large. This is 80% of the project and has the important design fork
(now decided: Option 3).**

### Two hard facts from the code

1. **The desktop app cannot render SVG today.** `DefaultRenderer._find_image`
   (`visual_stage.py`) only knows `.gif/.webp/.png/.jpg/.txt/.rtf`. tkinter's
   canvas has no SVG — and no SMIL animation, which is the point of these
   visuals (traced routes, grow-in bars, pulses). **The preview must be a real
   browser engine.**
2. **Most SVGs are generated, not hand-drawn.** The genealogy/map/tabernacle
   families come out of Python generators reusing hand-tuned geometry. Editing
   the *output* XML directly would be clobbered on the next generator run.

### The Option 3 model: the studio orchestrates, it does not re-invent drawing

The studio owns the **verse-aware workflow, faithful animated preview, and
pipeline glue.** It delegates actual vector drawing to a text/XML pane and/or
Inkscape. We are **not** building "Illustrator for verses" — Inkscape already
exists and is free; what it can't give you is verse-awareness, SMIL preview
timed to narration, and pipeline integration.

**What the studio does**
- **Verse navigator.** Pick book / chapter / verse. Auto-loads the correct file
  honoring the translation-suffix chain (`.KJV.svg` → `.svg`) and shows which
  translation variants exist.
- **"Start from previous verse's final frame."** Maps cleanly onto how the
  generators already build: each verse's SVG is the prior verse's steady state
  *plus* one new reveal. Mechanically:
  1. Load verse N‑1's SVG.
  2. Freeze its SMIL animations to their end values (they already use
     `fill="freeze"`), demoting the whole thing to a static base `<g>`.
  3. Open a fresh animated overlay `<g>` for verse N's new element.
- **Faithful preview.** Render the working SVG into a small temp HTML and show
  it in an embedded webview (`pywebview`) or the system browser with live
  reload — this renders SMIL correctly **and** sidesteps `cairosvg`/native
  Cairo, which is exactly the kind of dependency that fights the Windows ARM64
  machine (same class of problem as the wrangler/GitHub-deploy constraint).
- **Preview with narration.** Play the verse's MP3 alongside the animation so
  you see motion timed to the read.
- **Save + publish glue.** On save: write the `.svg`, re-run `build_manifest.py`,
  and optionally stage into `deploy_bundle/` via `prepare-deploy.ps1`.

**Drawing itself** = hand-edit the XML pane and/or a "Open in Inkscape" button.

### For the generated families

Where a verse belongs to a generator family (genealogy, maps, tabernacle),
"edit" should route to the **Python spec**, not the XML — e.g. the per-verse
`CHAPTERS` dict, `LANDMARKS`, or name-variant tables — and re-run the generator
on save. The studio should detect "this file is generator-owned" (a small
registry mapping verse ranges → generator module) and steer you to the spec so
your edits actually stick. Pure hand-authored one-offs (Acts 13–14 style) edit
as raw SVG.

**Model: Opus 4.8** for the architecture + the preview/round-trip/"continue
from previous frame" design (get it right once) → **Sonnet 5** for the build →
escalate to **Opus/Fable 5** only if the webview integration gets stuck.

---

## Feature C — Chapter → MP3 batch renderer (any translation)

**Effort: easy-to-moderate.** `generate_showcase_audio.py` already does this for
a hardcoded `SHOWCASE_CHAPTERS` list. Generalize it to a GUI panel: pick book +
chapter range + translation + voice → render with a progress bar. Same
`tts_engine.synthesize` + `fetch_passage` calls the reader uses live.

**Two real caveats**
1. **The web player is WEB-only by design.** `resolveAudio` (web `tts.js`) swaps
   in an MP3 only when the visitor has WEB selected, because the audio manifest
   is a flat `Book_ch_v → file` map with no translation dimension. To ship other
   translations we must (a) key audio files/manifest by translation
   (`Book_ch_v.KJV.mp3`) and (b) teach the web `Player` to look up the current
   translation. This is a **web-side change**, planned as part of this feature.
2. **File-count ceiling.** Files (not bytes) are the Cloudflare Pages
   constraint (~20k). Every translation × chapter × verse multiplies fast
   (~31k verses per full translation). Keep the renderer **selective** — render
   the chapters that have visuals, in the translations you care about — and show
   a projected file-count-against-budget guardrail in the UI.

**Model: Sonnet 5** for the script generalization + GUI panel and the web
`Player`/manifest change; **Haiku 4.5** for the mechanical manifest/deploy glue.

---

## Build order

1. **Pronunciation feature** (Haiku/Sonnet) — small, high-confidence, ships the
   "studio" mindset immediately.
2. **Chapter→MP3 batch renderer, PC side only** (Sonnet) — keep WEB-only at
   first so nothing on the web breaks.
3. **Web multi-translation audio** (Sonnet) — unlock #2 for other translations
   once you actually want them.
4. **SVG Studio** (Opus design → Sonnet build) — last, biggest, and best
   started after re-immersing in the pipeline via 1–3.

## Model cheat-sheet

| Task | Model |
|---|---|
| Pronunciation integration | Haiku 4.5 → Sonnet 5 |
| Chapter→MP3 generalization + GUI | Sonnet 5 |
| Web multi-translation audio | Sonnet 5 |
| SVG Studio — architecture & preview/round-trip design | **Opus 4.8** |
| SVG Studio — bulk build | Sonnet 5 |
| SVG Studio — webview front-end polish | Sonnet 5 (escalate Opus/Fable 5) |
| Manifest/deploy glue, batch loops | Haiku 4.5 |

Rule of thumb: **Haiku for mechanical, Sonnet for features, Opus for the one
design decision everything hangs off of** (here: the SVG Studio edit model).

## Decisions for the SVG Studio (resolved 2026-07-08)

- **Preview host — embedded `pywebview` window.** Chosen for the self-contained
  feel (no external browser popping up), and it renders SMIL faithfully while
  avoiding `cairosvg`/native Cairo on ARM64. System-browser + live reload stays
  as the zero-dependency fallback if `pywebview` misbehaves.
- **Generator-owned files — detect and route, never block.** A generator-made
  SVG is a normal file and *can* be hand-edited; the catch is durability, not
  possibility — re-running its generator rewrites the file from the Python spec
  and silently discards any hand edits. The spec is the source of truth for
  those families. So the studio keeps a small registry (verse range → generator
  module) and, when you open a generator-owned verse, offers **"Edit spec
  (durable)"** as the primary action and **"Hand-edit this SVG anyway
  (one-off)"** as a clearly-labelled secondary. Hand-authored one-offs (Acts
  13–14 style) open straight into the editor with no warning, since nothing will
  overwrite them. This is also why "start from the previous verse's final frame"
  is the *generator's* job for those families (it already builds cumulatively)
  and a manual affordance only for hand-authored sequences.
- **Inkscape — optional, with a guided install prompt.** An "Open in Inkscape"
  button; if Inkscape isn't detected, a dialog explains what it is and links to
  the download. The tool always degrades to the built-in XML pane, so Inkscape
  is a convenience, never a requirement.
