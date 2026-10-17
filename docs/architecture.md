# Architecture

Theoria is a static website: the World English Bible (WEB) read aloud, with an animated SVG picture for each verse. Its content (the text, the pictures, the narration and their manifests) is made ahead of time on the PC by Python, mostly from Theoria Studio ([studio.md](studio.md)). The web app in `web/` is hand-written static HTML, JS and CSS, with no build step. Verses with no neural MP3 are read by the browser's own Web Speech. Publishing commits the content and pushes it to GitHub; the web app's code is committed by hand ([Deploy](#deploy)). Cloudflare then deploys the site as static assets of the `av-bible` Worker, served at <https://theoria-bible.net/>.

```
bibles/eng-web.usfx.xml --import_translation.py--> bibles/WEB/<Book>_<ch>.json
        |                                                    |
        |            passages.load_chapter / verse_numbers   |
        v                                                    v
generate_*_svg.py (svg_generators.json)      tts_engine.synthesize (pronunciation.respell)
        |                                                    |
visuals/<Book>/<ch>/<Book>_<ch>_<v>.svg      web/audio/<Book>_<ch>_<v>.mp3
        | build_manifest.py                                  |
visuals/manifest.json (v2)                   web/audio/manifest.json
        |                                                    |
        +---------- Publish: prepare-deploy.ps1 -> deploy_bundle/ -> git push ----------+
                                                                                       v
                         GitHub -> Cloudflare Workers Builds -> Worker "av-bible" (static assets)
                                                                                       |
                                    web app (web/js): /bibles/WEB/, /visuals/, /audio/
```

## Text

- The source is `bibles/eng-web.usfx.xml`, the eBible.org USFX file. Git ignores it.
- `import_translation.py` turns it into `bibles/WEB/<Book>_<ch>.json`: 1,189 files, one per chapter. Each holds `book`, `chapter`, `canonical` and `verses` (`[[number, text], ...]`). The files also carry `translation` and `notes` fields, which keep the re-import byte-identical; nothing reads them.
- In Python, `passages.load_chapter()` reads a chapter, and `passages.verse_numbers()` gives its verse numbers. That is the versification every picture follows: newer generators call `verse_numbers()`, and older ones carry their own verse tables that match it. Today the visual keys of all 73 illustrated chapters equal WEB's verses exactly.
- On the web, `web/js/bible.js` fetches `/bibles/WEB/<Book>_<ch>.json`.

## Visuals

1. **Generators.** Each `generate_*_svg.py` writes one family of pictures through `generate_tabernacle.out_path()`, as `visuals/<Book>/<ch>/<Book>_<ch>_<v>.svg` (1024×576, SMIL animation). The generator is the source of truth, so its output is never edited by hand. `svg_generators.json`, read by `svg_registry.py`, records which generator owns each chapter or verse range. `test_registry` checks that every published verse SVG has an owner. House rules for the pictures are in [visuals.md](visuals.md).
2. **Manifest.** `build_manifest.py` scans `visuals/` and writes `visuals/manifest.json`:

   ```json
   {"version": 2,
    "entries": {"Acts_13_1": [{"file": "Acts/13/Acts_13_1.svg", "kind": "map", "animated": true}]}}
   ```

   - `kind` comes from a `data-kind` attribute on the SVG root, else the owning family's `kind`, else `infographic`.
   - `animated` is true when the file contains a SMIL element.
   - One picture can serve several verses (D17), in two ways:
     - **Range file.** `Book_c_v1-v2.svg` supplies every WEB verse in its range that has no file of its own.
     - **Identical copy.** A verse whose SVG is byte-identical to the previous verse's points at the first file of that run, unless its family sets `"replay_identical": true`.
   - Today the manifest has 2,241 verse keys in 73 chapters of 11 books. They point at 2,116 distinct files: 125 verses share the previous verse's picture, and there are no range files yet.
   - `visuals/reference/` holds the wall charts. They are not in the manifest: they deploy, but nothing links to them (D14; [reference-charts.md](reference-charts.md)).
3. **Web.**
   - `web/js/visuals.js` loads `/visuals/manifest.json` (revalidated with `cache: "no-cache"`). `findVisual()` looks up the verse key, then the chapter key.
   - The stage is an `<img>`. When the next verse shows the same file, the `<img>` is left alone, so the picture keeps playing or stays finished. Pressing Play on the verse already shown restarts it with a fresh `?r=` URL.
   - A verse with no picture shows a built-in "isn't illustrated yet" line pointing to the ✦ list of illustrated chapters.

## Narration

- **Respelling.** `pronunciation.respell()` swaps the names the voice gets wrong for spellings it says correctly. The list is `pronunciations.json` ([pronunciation.md](pronunciation.md)).
- **Synthesis.** `tts_engine.synthesize()` respells the text, then speaks it with edge-tts in the house voice (`tts_engine.HOUSE_VOICE` = `en-US-AndrewNeural`, `HOUSE_RATE` = 0).
  - It caches the result as `cache/audio/tts/<voice without dashes>_<rate:+d>_<md5 of voice|rate|spoken text, 16 hex>.mp3` (`tts_engine._cache_file`).
  - When edge-tts is unreachable, it falls back to the offline Windows SAPI voice and writes a `.wav`. That audio is never published.
- **Rendering.** The Audio tool (`audio_studio.py`) renders whole chapters through `generate_showcase_audio.generate_chapter()`.
  - Each verse becomes `web/audio/<Book>_<ch>_<v>.mp3`, registered in `web/audio/manifest.json` as `{"Genesis_1_1.WEB": "Genesis_1_1.mp3"}`. The `.WEB` suffix is a fixed part of the key format (D11).
  - Manifest writes re-read the file under a lock, merge, write a temp file and swap it in with `os.replace`. That way the Audio tool and Video Studio, both in the Studio's process, don't drop each other's entries.
  - Today 2,348 verses in 76 chapters are narrated.
- **Stale narration.** Changing a respelling changes the spoken text, so the next synthesis misses the cache. An MP3 already in `web/audio/` stays as it was until the chapter is re-rendered with "Overwrite existing files".
- **Audio-timed pictures.** The 1 Chronicles 1–9 and Matthew 1 generators pace each verse's animation by the length of its MP3 in `web/audio/` (`svg_chronicles_world.AUDIO_DIR`). They fall back to an estimated pace when a file is missing. Re-run them after re-rendering those chapters.
- **Web.** `web/js/app.js` loads `audio/manifest.json` and plays a verse's MP3 when it has one. Otherwise `web/js/tts.js` reads the verse with Web Speech.

## Deploy

**Publish** in the Studio (`publish_studio.py`) is the only deploy path (D7):

1. `build_manifest.py` rebuilds `visuals/manifest.json`.
2. `prepare-deploy.ps1` rebuilds `deploy_bundle/`:
   - `web/*` goes to its root;
   - the `*.json` in each `bibles/` subfolder go to `bibles/<subfolder>/` (today only `bibles/WEB/`);
   - `visuals/` is copied without `*.xml` or `*.tmp`.

   A confirm dialog then shows the change summary, the commit message and the bundle's file count against the limit.
3. Git:
   - `git add -A` and `git commit` run on `publish_studio.CONTENT_PATHS` only: `web/audio`, `bibles`, `visuals` and their `deploy_bundle/` copies. Anything staged elsewhere stays staged and uncommitted.
   - `git push` follows. The push is the deploy.

Further rules:

- **Web-app code is committed by hand.** Publish never commits the web app's own files (`web/` except `web/audio`). It warns when they have uncommitted changes, because those changes, and their `deploy_bundle/` copies, stay unpublished until you commit them.
- **Dry run.** "Dry run (no commit / push)" runs steps 1 and 2, logs what would be committed and stops before git. Steps 1 and 2 still rewrite the manifest and `deploy_bundle/`.
- **Cloudflare side.**
  - GitHub triggers Cloudflare Workers Builds, which deploys the Worker `av-bible`.
  - `wrangler.toml` serves `deploy_bundle/` as static assets (`[assets] directory = "./deploy_bundle"`), so the app sits at `/`, with `/audio/`, `/bibles/WEB/` and `/visuals/` beside it.
  - The build settings live in the Cloudflare dashboard, not in the repo.
- **No local deploys.** Local `wrangler` can't run on this Windows ARM64 PC, so deploys go only through GitHub.
- **`deploy_bundle/` is tracked**, so each content file is in the repo twice. Serving `web/` directly and untracking the bundle is optional future work (D7(c), in [ROADMAP.md](../ROADMAP.md)).

## File budget

On the Free plan, Cloudflare's Workers static assets take at most 20,000 files in one deployed version (`publish_studio.DEPLOY_FILE_LIMIT`). Files, not bytes, are the ceiling.

`publish_studio.count_deploy_files()` counts what a deploy ships, from the source folders rather than `deploy_bundle/`:

| Counted | Today |
|---|---|
| Every file under `web/`, including the MP3s and manifest in `web/audio/` | 2,363 |
| The `*.json` in each `bibles/` subfolder (only `WEB`) | 1,189 |
| Every file under `visuals/` except `*.xml`: the verse SVGs, `manifest.json` and the 8 reference-chart files | 2,250 |
| **Total** | **5,802** |

- **Cost.** A fully produced verse costs about 2 files: 1 SVG and 1 MP3.
  - A range file costs one file for its whole run.
  - An identical copy still costs a file. The manifest points past it, but the copy stays on disk and deploys.
- **Where the number shows.**
  - The main window's meter, `Files n / 20,000`. It turns amber above 90% and red over the limit, and recounts at startup, when a tool window closes and when clicked.
  - Publish's meter.
  - The Audio Renderer's confirm dialog, which adds the new files a render would create.
  - Publish's confirm dialog counts the files actually in `deploy_bundle/` after step 2.
- **When it fills up.** The ways to make room are listed in [ROADMAP.md](../ROADMAP.md).

## Where state lives

| What | Where | Tracked |
|---|---|---|
| Studio settings: `last_book`, `last_chapter`, `last_verse`, `svg_preview_host`, `editor` | `config.json`, written through `config.update(**changes)`; an unreadable file is first copied to `config.json.bak` | no |
| TTS cache; the Studio's error log | `cache/audio/tts/`; `cache/studio_error.log` | no |
| The Verifier's verdict store | `data/ipa_checks.json` (`config.IPA_CHECKS_PATH`) | yes |
| Pronunciation list; retired entries | `pronunciations.json`; `pronunciations_archive.json` | yes |
| Generated pronunciation reports | `PRONUNCIATIONS.md`, `PRONUNCIATION_TODO.md` | no (ignored) |
| Generator registry | `svg_generators.json` | yes |
| Content: text, pictures, narration and their manifests | `bibles/WEB/`, `visuals/`, `web/audio/` | yes |
| The deployed copy | `deploy_bundle/` | yes |
| Superseded designs, mockups, scratch work, the `pre-cleanup` bundle | `C:\Dev\Theoria-archive\` beside the repo (`config.ARCHIVE_DIR`): `backups/`, `mockups/`, `_scratch/`, `pre-cleanup.bundle` | no (outside the repo) |
| Video renders | `config.RENDERS_DIR` = `Theoria-archive\renders\` | no (outside the repo) |

The git tag `pre-cleanup` marks the repo as it was before the October 2026 cleanup (`docs/archive/CLEANUP_PLAN.md`).
