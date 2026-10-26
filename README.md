# Theoria

Theoria is a visual Bible. It reads the World English Bible (WEB, public domain)
aloud verse by verse and shows an animated SVG picture for each verse. The website
is a static web app. This repo also holds **Theoria Studio**, the Windows app that
authors the content and publishes it.

## Live site

**<https://theoria-bible.net/>**, served by the `av-bible` Cloudflare Worker.

As of 2026-10-17 it has 2,241 illustrated verses in 73 chapters across 11 books
(Genesis, Exodus, Numbers, 1 Chronicles, Matthew, Luke, Acts, Romans, Hebrews,
2 Peter, Zephaniah), drawn from 2,116 picture files. Neural narration covers 2,348
verses in 76 chapters, and the browser's Web Speech voice reads the rest. Coverage
in the Studio shows the current numbers.

On a verse without a picture, the stage says the verse or chapter "isn't illustrated
yet" and offers a button that opens the ✦ list of illustrated chapters. When
consecutive verses share a picture, it keeps playing and doesn't restart.

## How it's made

1. **Text.** `web/bibles/WEB/<Book>_<chapter>.json` holds one file per chapter
   (1,189). `import_translation.py` rebuilds them from the eBible.org USFX file
   `sources/eng-web.usfx.xml`. The `sources/` folder is gitignored.
2. **Pictures.** The generator scripts registered in `svg_generators.json` draw the
   per-verse SVGs, animated with SMIL, into `web/visuals/<Book>/<chapter>/`. Each
   script draws one or more families, and the registry records which generator owns
   which chapters. The generators are the source of truth, and generated SVGs are
   never edited by hand. `build_manifest.py` indexes the SVGs into
   `web/visuals/manifest.json`. Two other scripts, `generate_ot_family_tree_svg.py`
   and `generate_ot_timeline_svg.py`, draw wall charts into `web/visuals/reference/`.
3. **Narration.** The Studio's Audio Renderer synthesizes one MP3 per verse into
   `web/audio/`, listed in `web/audio/manifest.json`. It uses the house voice
   `en-US-AndrewNeural` through edge-tts, with proper nouns respelled from
   `pronunciations.json`. Optionally, the same voice on Azure speaks chosen names
   from their IPA ([docs/pronunciation.md](docs/pronunciation.md#ipa-through-azure)).
4. **Publish.** The Studio's Publish tool rebuilds the visuals manifest, then
   commits the content and pushes it. The push is the deploy: Cloudflare Workers
   Builds deploys `web/` from the pushed commit as the av-bible Worker's static
   assets (`wrangler.toml`). Nothing is copied or built first.

The web app in `web/` is plain JavaScript with no build step and no framework.
`web/` is also the site root, so the content folders inside it are the site's
`/bibles/`, `/visuals/` and `/audio/`. The app fetches the chapter JSON and both
manifests, then plays each verse's MP3, falling back to Web Speech where there is
none.
[docs/architecture.md](docs/architecture.md) covers the whole flow.

## Quick start

**Use the site:** open it in a browser.

**Run the Studio** on Windows, from the repo root:

```bat
py -3.14 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
run.bat
```

`run.bat` also sets everything up by itself. It creates `.venv` if it is missing,
reinstalls the requirements whenever `requirements.txt` changes, and starts the Studio
with `pythonw`. If the Studio can't load, `run.bat` runs it in the console so the
traceback stays on screen. After the Studio starts, its errors go to
`cache/studio_error.log`.

**Optional: Azure, for names spoken from IPA.** Create an Azure Speech resource
(the free F0 tier gives 500,000 characters a month), then set its key and region
and restart the Studio. Nothing else needs it.

```bat
setx AZURE_SPEECH_KEY <your key>
setx AZURE_SPEECH_REGION eastus
```

**Run the web app locally:** serve `web/` at the site root. From the repo root, run
`python -m http.server 8000 -d web` (any Python works, `.venv\Scripts\python.exe`
included), then open `http://localhost:8000/`. The `web-static` entry in
`.claude/launch.json` runs the same server. It shows the working tree as it is, so
after changing pictures, rebuild the manifest with `build_manifest.py` or SVG
Studio's **Save + manifest** before you look.

## Repo map

| Path | What it holds |
|---|---|
| `web/` | The site root, which Cloudflare serves as it is. It holds the web app (`index.html`, `js/`, `css/`, `icons/`, `manifest.webmanifest`) and the three content folders below. `web/.assetsignore` lists the files the upload leaves out. |
| `web/audio/` | The narration MP3s and their manifest. |
| `web/bibles/WEB/` | The WEB text, one JSON file per chapter. |
| `web/visuals/` | Per-verse SVGs in `web/visuals/<Book>/<chapter>/`, `manifest.json`, and `reference/`, which holds the wall charts. The charts are deployed but nothing on the site links to them ([docs/reference-charts.md](docs/reference-charts.md)). |
| `sources/` | Ignored: `eng-web.usfx.xml`, the source text that `import_translation.py` turns into `web/bibles/WEB/`. |
| `docs/` | Design docs. See [Docs](#docs). |
| `data/` | `ipa_checks.json`, the Verifier's verdict store. |
| `tools/` | Reference scripts: `audit_heb.py` (a text-overlap audit of the Hebrews SVGs) and `layout_lab.py` (a family-tree layout study). |
| `branding/` | Logo sources, and `theoria_studio.ico`, the Studio's desktop-shortcut icon. |
| `cache/` | Ignored: the TTS cache and the Studio's error log. |
| Root files | The Python modules (below), `run.bat`, `requirements.txt`, `svg_generators.json` (the generator registry), `pronunciations.json`, `pronunciations_archive.json` and `isbe_harvest.json` (pronunciation data), and the deploy files `wrangler.toml`, `package.json` and `package-lock.json`. |

Superseded designs, old renders and scratch work live outside the repo in
`C:\Dev\Theoria-archive` (`config.ARCHIVE_DIR`). Video renders go to
`config.RENDERS_DIR`, its `renders/` folder.

**The web app** (`web/`, plain ES modules that `index.html` loads with no build step):

- `web/index.html` and `web/css/style.css`: the page, with the Book, Chapter and Verse
  pickers, the stage, the player controls and the ✦ dialog.
- `web/js/app.js`: the UI and playback, the ✦ list, the "isn't illustrated yet" pointer,
  the screen Wake Lock, and loading `web/audio/manifest.json`.
- `web/js/bible.js`: fetches the chapter JSON from `/bibles/WEB/`.
- `web/js/data.js`: the book list and chapter counts, ported from `books.py`.
- `web/js/tts.js`: the per-verse player, which plays the verse's MP3 where there is one
  and uses Web Speech otherwise.
- `web/js/visuals.js`: looks pictures up in `/visuals/manifest.json`, lists the
  illustrated chapters, and picks each book's background gradient.
- `web/manifest.webmanifest` and `web/icons/`: the web app manifest and icons.

**The Studio** (`app.py`, tkinter). The main window holds the shared passage (Book,
Chapter, Verse), a preview player (the WEB text, read in the house voice beside the
SVG stage), the deploy file-budget meter, and the tool buttons. The buttons come
from the `TOOLS` registry in `app.py`:

| Group | Tool | Module | Runs as |
|---|---|---|---|
| Plan | Coverage: per-chapter visuals, audio, unreviewed names and catalog candidates | `coverage_studio.py` | window |
| Author | Visuals (SVG Studio): each verse's SVG and its owner, a live preview, Re-run generator, manifest rebuild | `svg_studio.py`, `svg_preview.py` | window |
| Author | Pronunciation: review and tune proper-noun respellings, hear and set the IPA Azure speaks, or respell a word in one verse only | `pronunciation_tool.py` | separate process |
| Author | Verifier: transcribes the rendered audio and scores it against the list | `pronunciation_check.py`, `ipa_asr.py` | separate process |
| Produce | Audio: renders chapter narration MP3s, through Edge, Azure or both | `audio_studio.py` | window |
| Produce | Video: renders a verse range to an MP4 (4K by default) | `video_studio.py`, `video_render.py` | window |
| Ship | Publish: manifest, commit, push | `publish_studio.py` | window |

The modules the Studio and its tools share:

- `config.py` handles settings (`config.json`, ignored) and the paths: `WEB_DIR`
  (the site root), `VISUALS_DIR`, `BIBLES_DIR`, `WEB_AUDIO_DIR` and `SOURCES_DIR`.
  The other modules take their paths from it.
- `passages.py` loads the WEB text and provides `verse_numbers()`. `books.py` holds
  the canon.
- `tts_engine.py` does speech synthesis (`HOUSE_VOICE`, `HOUSE_RATE`) and picks the
  service for each text (`ENGINES`, `route()`).
- `azure_tts.py` calls Azure's text-to-speech and keeps the free-tier meter.
- `pronunciation.py` provides `respell()`, the Azure SSML (`ssml()`, `azure_ipa()`),
  and reads and writes `pronunciations.json`.
- `generate_showcase_audio.py` holds the narration file and audio-manifest helpers.
- `audio_player.py` plays audio through Windows MCI.
- `visual_stage.py` and `svg_stage.py` draw the main window's SVG stage in WebView2.
- `build_manifest.py`, `svg_registry.py` (which reads `svg_generators.json`) and
  `svg_freeze.py` support the visuals pipeline.
- `isbe_sweep.py` and `regen_pronunciation_todo.py` maintain the pronunciation list.

**Generator families.** `svg_generators.json` registers 25 families from 24 scripts.
Nearly every generator also uses `svg_surface.py` and `generate_tabernacle.py`, and
most use `svg_figures.py`. The table lists each family's other dependencies:

| Passage | Generator | Builds on |
|---|---|---|
| Genesis 1–4, 6–9, 10, 11:1–9 | `generate_genesis{1,2,3,4,69,10,11}_svg.py` | `generate_tribal_maps.py`: `MapFrame` for Genesis 10 and 11, and water colours for Genesis 1, 2 and 6–9. Genesis 1 and 3 reuse Genesis 2's palette. Genesis 11 reuses Genesis 10's map. |
| Genesis 5, 11:10–32 | `generate_genealogy_svg.py` | `generate_genealogy.py` |
| Exodus 25, 27 and Exodus 26 | `generate_exodus2527_svg.py`, `generate_exodus26_svg.py` | `generate_tabernacle.py`, which holds the Exodus 25–27 spec. The Exodus 25, 27 family also reuses Exodus 26. |
| Exodus 28 | `generate_exodus28_svg.py` | `svg_priest.py`, `svg_vocab.py` |
| Numbers 1–2, 3–4 | `generate_numbers1_2_svg.py`, `generate_numbers3_4_svg.py` | Numbers 1–2 takes colours from `generate_tribal_maps.py` and `generate_genesis2_svg.py`. |
| Numbers 32, 34 | `generate_numbers32_svg.py`, `generate_numbers34_svg.py` | `generate_tribal_maps.py`, which holds the shared geometry. Numbers 34 is a camera tour on `svg_map_camera.py`. |
| 1 Chronicles 1–9 | `generate_1chronicles_tree_svg.py` | `generate_1chronicles.py`, `chronicles_tree.py`, `ot_grafts.py`, `svg_chronicles_world.py`, `svg_family_lines.py`, which draws the lines that join each family, and `layout_regions.py`, which lays the tree out in a fan with a titled panel for each son of Israel |
| Matthew 1 | `generate_matthew1_svg.py` | `matthew_tree.py`, `svg_matthew_world.py`, `svg_matthew_nativity.py`, `svg_chronicles_world.py` |
| Luke 3 | `generate_luke3_svg.py` | `generate_luke3.py`, which takes its frame timing from `generate_genealogy.py` |
| Acts 13–14 | `generate_acts1314_svg.py` | `acts_geography.py`, which holds the map; `acts1314_synagogue.py`, `acts1314_jerusalem.py` and `acts1314_lystra.py`, the three scenes; `svg_map_camera.py` and `svg_scene_card.py` for the camera tour and its scene cards |
| Acts 15–18 | `generate_acts1518_svg.py` | `generate_tribal_maps.py` (`MapFrame`) |
| Romans 1–16 | `generate_romans_svg.py` | |
| Hebrews 1–13 | `generate_hebrews_svg.py` | `svg_priest.py`, `svg_vocab.py` |
| 2 Peter, Zephaniah | `generate_2peter_svg.py`, `generate_zephaniah_svg.py` | `svg_vocab.py` |

The libraries most generators share:

- `svg_surface.py` provides `SvgCanvas`, the SVG drawing surface, along with its SMIL
  helpers.
- `generate_tabernacle.py` holds the house palette, output paths and fonts, and also
  the Exodus 25–27 spec.
- `svg_figures.py` is the shared figure vocabulary: people, creatures and objects.
- `svg_vocab.py` holds small drawing helpers.
- `generate_tribal_maps.py` holds the map projection and shared map data.
- `svg_map_camera.py` is the camera-tour engine for maps (Numbers 34, Acts 13–14): the
  camera, names that hold their size and are placed by a clash test, the plates,
  the overview inset and the QC checks. It takes its camera arc and audio timing
  from `svg_chronicles_world.py`.
- `svg_scene_card.py` hangs a side-view scene (a town, its people) in a camera
  tour's world, so the camera can dive into it from the town's dot. Its cast
  carry their state from one verse's file to the next.
- `generate_ot_family_tree_svg.py` draws the Old Testament family-tree wall chart.
  It also provides the tree layout that 1 Chronicles and Matthew 1 use.
- `generate_ot_timeline_svg.py` draws the OT timeline chart, using `chronology.py`.

## Requirements

- Windows, with Python 3.14 in `.venv`. On this ARM64 PC the venv Python is an
  emulated x64 build. `platform.machine()` reports `ARM64`, so check
  `sysconfig.get_platform()` instead, which reports `win-amd64`. x64 wheels install
  normally.
- `requirements.txt`: edge-tts (narration) and aiohttp (edge-tts's networking, and
  Video Studio's browser control), Pillow (used by the generators), and pywebview
  with the Microsoft Edge WebView2 Runtime, which shows every visual in the Studio.
  WebView2 is built into Windows 11.
- Optional, for the tools that use `ipa_asr.py` (the Verifier and `isbe_sweep.py`):
  `pip install torch transformers soundfile scipy`. That is about 1.5 GB installed,
  and the model downloads about 1.2 GB on first run. Nothing else imports them.
- Video Studio needs ffmpeg (`winget install BtbN.FFmpeg.GPL`, or `ffmpeg.exe` and
  `ffprobe.exe` in `tools/ffmpeg/bin/`) and Google Chrome or Microsoft Edge, which
  draws the frames.
- Windows PowerShell, which provides the offline SAPI fallback voice.
- Inkscape is optional, for SVG Studio's "Open in Inkscape".

## Deploy

**A push to `main` deploys.** The GitHub repo is connected to Cloudflare Workers
Builds, which deploys the Worker `av-bible`. `wrangler.toml` serves `./web` from the
pushed commit as static assets: the web app at `/`, and `/audio/`, `/bibles/WEB/`
and `/visuals/` beside it. `web/.assetsignore` lists what wrangler leaves out of the
upload: `*.tmp`, `*.xml`, `.DS_Store`, `Thumbs.db`, `desktop.ini` and the file
itself. Everything else under `web/` goes public. Local wrangler can't run on
Windows ARM64, because it needs `workerd`, which has no build for that platform. So
every deploy goes through GitHub. `package.json` pins wrangler 4.107.0, and the build
installs it from `package-lock.json`.

**Build settings** (in Cloudflare, not in the repo). Cloudflare builds only for pushes that touch `web/`, `wrangler.toml`, `package.json` or `package-lock.json` (its build watch paths). A push of 3,000 or more files, or of 20 or more commits, always builds. The build
runs `npm clean-install` from the lockfile, then `npx wrangler deploy`. The build
variable `SKIP_DEPENDENCY_INSTALL=1` stops Cloudflare also pip-installing
`requirements.txt`, which the site doesn't need.

**Publish** is the deploy button. Open it with the Publish button in the Studio's
Ship group, or run `publish_studio.py`. It has two steps:

1. `build_manifest.py` rebuilds `web/visuals/manifest.json`. Publish then scans the
   content paths for changes (`git status`), and a confirm dialog shows the change
   summary and the file budget.
2. It runs `git add`, `git commit` and `git push` on the content paths only, which
   are `publish_studio.CONTENT_PATHS`: `web/audio`, `web/visuals`, `web/bibles` and
   `pronunciations.json`. The pronunciation list isn't deployed, but the MP3s are
   rendered from it, so it is committed with them.
   The commit message reads `Publish: …`. If there are no content changes, nothing
   is committed or pushed.

Tick **Dry run (no commit / push)** to run step 1 and the change scan, and log what
would be committed. It stops before `git add`, `git commit` and `git push`. A dry run
still rewrites the manifest.

**File budget.** Cloudflare Workers static assets allow about 20,000 files per
deployed version (`publish_studio.DEPLOY_FILE_LIMIT`). The ceiling is a file count,
not bytes. `count_deploy_files()` counts what a deploy ships: every file under `web/`
that `web/.assetsignore` doesn't exclude, 5,802 files as of 2026-10-17. Each fully
produced verse adds about two files, one SVG and one MP3. The Studio's toolbar and
Publish show the count, and the Audio Renderer projects it before a render.

**Web-app code** means everything in `web/` outside the three content folders:
`index.html`, `js/`, `css/`, `icons/`, `manifest.webmanifest` and `.assetsignore`
(`publish_studio.WEB_APP_PATHS`). Publish never commits it, and it warns while any of
it is uncommitted. To ship a change to it, commit the changed files by hand (for
example `git add web/js/app.js`, then `git commit`) and run `git push`. Because
`web/` is served as it is, the push deploys the change, and there are no copies to
refresh. Publish's own `git push` also pushes any local commits like this one.

Python, docs and other code are committed by hand the same way. A push of only
those doesn't trigger a build, because only `web/` is served.

**Rollback.** Either `git revert` the bad commit and push, which redeploys the
previous content, or roll the Worker back to an earlier version from its deployments
list in the Cloudflare dashboard. A dashboard rollback doesn't touch git, so the next
build deploys `main` as it stands.

## Tests

```bat
.venv\Scripts\python.exe -m unittest test_imports test_registry test_svg_freeze test_shared_visuals test_azure_tts
```

There are 65 tests in five modules:

- `test_imports`: every root module imports.
- `test_registry`: `svg_generators.json` is consistent, every published verse SVG has
  an owner, and no retired variant files are present.
- `test_svg_freeze`: `svg_freeze`, with one test for each row of its case table.
- `test_shared_visuals`: range files, identical-copy sharing and Video Studio's shared
  clock.
- `test_azure_tts`: the Azure path, offline: IPA conversion (every stored `ipa`
  must convert), the SSML a verse becomes, engine routing, the usage meter and how
  `use_ipa` is saved.

## Docs

- [ROADMAP.md](ROADMAP.md): what's next for content, the web app, the Studio and
  infrastructure.
- [CREDITS.md](CREDITS.md): the text, the voice, the pronunciation sources and the
  libraries.
- [CLAUDE.md](CLAUDE.md): rules for AI coding sessions in this repo.
- [docs/architecture.md](docs/architecture.md): data flow, the audio pipeline, deploy
  and the file budget.
- [docs/studio.md](docs/studio.md): Theoria Studio, covering every tool, what it
  reads and writes, and the chapter workflow.
- [docs/svg-studio.md](docs/svg-studio.md): the SVG Studio design.
- [docs/video-studio.md](docs/video-studio.md): Video Studio.
- [docs/visuals.md](docs/visuals.md): visual conventions, covering SVG and SMIL, file
  naming, manifest v2, the registry and the house rules.
- [docs/pronunciation.md](docs/pronunciation.md): `respell()`, the Verifier, and how
  the list is maintained.
- [docs/content-catalog.md](docs/content-catalog.md): candidate visuals for the whole
  canon. Coverage parses this file, so keep its format.
- [docs/reference-charts.md](docs/reference-charts.md): the wall charts in
  `web/visuals/reference/`.
- Design records:
  - [Hebrews](docs/design/hebrews.md)
  - [Romans](docs/design/romans.md)
  - [Matthew 1](docs/design/matthew-1.md)
  - [Short books](docs/design/short-books.md)
  - [OT timeline](docs/design/ot-timeline.md)
- [docs/archive/](docs/archive/README.md): superseded plans and records.
