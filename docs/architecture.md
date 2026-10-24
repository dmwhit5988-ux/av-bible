# Architecture

Theoria is a static website: the World English Bible (WEB) read aloud, with an animated SVG picture for each verse. Its content (the text, the pictures, the narration and their manifests) is made ahead of time on the PC by Python, mostly from Theoria Studio ([studio.md](studio.md)). The web app in `web/` is hand-written static HTML, JS and CSS, with no build step. Verses with no neural MP3 are read by the browser's own Web Speech. `web/` is also the site root: the content folders `web/bibles/`, `web/visuals/` and `web/audio/` are the site's `/bibles/`, `/visuals/` and `/audio/`. Publishing commits the content and pushes it to GitHub; the web app's code is committed by hand ([Deploy](#deploy)). Cloudflare then deploys `web/` as it stands in the pushed commit, as static assets of the `av-bible` Worker, served at <https://theoria-bible.net/>.

```
sources/eng-web.usfx.xml --import_translation.py--> web/bibles/WEB/<Book>_<ch>.json
        |                                                    |
        |            passages.load_chapter / verse_numbers   |
        v                                                    v
generate_*_svg.py (svg_generators.json)      tts_engine.synthesize (pronunciation.respell)
        |                                                    |
web/visuals/<Book>/<ch>/<Book>_<ch>_<v>.svg  web/audio/<Book>_<ch>_<v>.mp3
        | build_manifest.py                                  |
web/visuals/manifest.json (v2)               web/audio/manifest.json
        |                                                    |
        +---------- Publish: git add/commit/push of CONTENT_PATHS ----------+
                                                                            v
                  GitHub -> Cloudflare Workers Builds -> Worker "av-bible" serves web/
                                                                            |
                           web app (web/js): /bibles/WEB/, /visuals/, /audio/
```

## Text

- The source is `sources/eng-web.usfx.xml`, the eBible.org USFX file (`config.SOURCES_DIR`). Git ignores `sources/`.
- `import_translation.py` turns it into `web/bibles/WEB/<Book>_<ch>.json` (`config.BIBLES_DIR`): 1,189 files, one per chapter. Each holds `book`, `chapter`, `canonical` and `verses` (`[[number, text], ...]`). The files also carry `translation` and `notes` fields, which keep the re-import byte-identical; nothing reads them.
- In Python, `passages.load_chapter()` reads a chapter, and `passages.verse_numbers()` gives its verse numbers. That is the versification every picture follows: newer generators call `verse_numbers()`, and older ones carry their own verse tables that match it. Today the visual keys of all 73 illustrated chapters equal WEB's verses exactly.
- On the web, `web/js/bible.js` fetches `/bibles/WEB/<Book>_<ch>.json`.

## Visuals

1. **Generators.** Each `generate_*_svg.py` writes one family of pictures through `generate_tabernacle.out_path()`, as `web/visuals/<Book>/<ch>/<Book>_<ch>_<v>.svg` under `config.VISUALS_DIR` (1024×576, SMIL animation). The generator is the source of truth, so its output is never edited by hand. `svg_generators.json`, read by `svg_registry.py`, records which generator owns each chapter or verse range. `test_registry` checks that every published verse SVG has an owner. House rules for the pictures are in [visuals.md](visuals.md).
2. **Manifest.** `build_manifest.py` scans `web/visuals/` and writes `web/visuals/manifest.json`:

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
   - `web/visuals/reference/` holds the wall charts. They are not in the manifest: they deploy, but nothing links to them (D14; [reference-charts.md](reference-charts.md)).
3. **Web.**
   - `web/js/visuals.js` loads `/visuals/manifest.json` (revalidated with `cache: "no-cache"`). `findVisual()` looks up the verse key, then the chapter key.
   - The stage is an `<img>`. When the next verse shows the same file, the `<img>` is left alone, so the picture keeps playing or stays finished. Pressing Play on the verse already shown restarts it with a fresh `?r=` URL.
   - A verse with no picture shows a built-in "isn't illustrated yet" line pointing to the ✦ list of illustrated chapters.

## Narration

- **Respelling.** `pronunciation.respell()` swaps the names the voice gets wrong for spellings it says correctly. The list is `pronunciations.json` ([pronunciation.md](pronunciation.md)).
- **Synthesis.** `tts_engine.synthesize()` respells the text, then speaks it with edge-tts in the house voice (`tts_engine.HOUSE_VOICE` = `en-US-AndrewNeural`, `HOUSE_RATE` = 0).
  - Its `engine` can send text to Azure instead (`azure_tts.py`), which is the same voice, metered, and able to speak `use_ipa` names from their IPA. `edge` is the default. `mixed` sends Azure only the verses that name someone spoken from IPA. `azure` sends everything. `tts_engine.route()` says which service a text would go to, what it would send, and what it would bill ([pronunciation.md](pronunciation.md#ipa-through-azure)).
  - It caches the result as `cache/audio/tts/<voice without dashes>_<rate:+d>_<md5 of voice|rate|spoken text, 16 hex>.mp3` (`tts_engine._cache_file`). Plain text has one entry whichever service spoke it. SSML with `<phoneme>` tags is keyed `<voice>_<rate>_ssml_<md5>.mp3`.
  - When edge-tts is unreachable, it falls back to the offline Windows SAPI voice and writes a `.wav`. That audio is never published. Azure has no fallback: a verse it refuses is skipped.
- **Rendering.** The Audio tool (`audio_studio.py`) renders whole chapters through `generate_showcase_audio.generate_chapter()`.
  - Each verse becomes `web/audio/<Book>_<ch>_<v>.mp3`, registered in `web/audio/manifest.json` as `{"Genesis_1_1.WEB": "Genesis_1_1.mp3"}`. The `.WEB` suffix is a fixed part of the key format (D11).
  - Manifest writes re-read the file under a lock, merge, write a temp file and swap it in with `os.replace`. That way the Audio tool and Video Studio, both in the Studio's process, don't drop each other's entries.
  - Today 2,348 verses in 76 chapters are narrated.
- **Stale narration.** Changing a respelling changes the spoken text, so the next synthesis misses the cache. An MP3 already in `web/audio/` stays as it was until the chapter is re-rendered with "Overwrite existing files".
- **Audio-timed pictures.** The 1 Chronicles 1–9, Matthew 1, Numbers 34 and Acts 13–14 generators pace each verse's animation by the length of its MP3 in `web/audio/`. They fall back to an estimated pace when a file is missing. Re-run them after re-rendering those chapters.
- **Web.** `web/js/app.js` loads `audio/manifest.json` and plays a verse's MP3 when it has one. Otherwise `web/js/tts.js` reads the verse with Web Speech.

## Deploy

**Publish** in the Studio (`publish_studio.py`) is the only deploy path (D7). `web/` is served as it is, so there is nothing to build or copy, and Publish has two steps:

1. `build_manifest.py` rebuilds `web/visuals/manifest.json`. Publish then scans the content paths for changes (`git status`), and a confirm dialog shows the change summary, the commit message and the deploy's file count against the limit.
2. Git:
   - `git add -A` and `git commit` run on `publish_studio.CONTENT_PATHS` only: `web/audio`, `web/visuals`, `web/bibles` and `pronunciations.json`. The pronunciation list isn't deployed (it is outside `web/`), but the MP3s are rendered from it, so it is committed with them. Anything staged elsewhere stays staged and uncommitted.
   - `git push` follows. The push is the deploy.

Further rules:

- **Web-app code is committed by hand.** Publish never commits the web app's own files: everything in `web/` outside the three content folders, which is `index.html`, `js/`, `css/`, `icons/`, `manifest.webmanifest` and `.assetsignore` (`publish_studio.WEB_APP_PATHS`). It warns when they have uncommitted changes, because those changes stay unpublished until you commit them. Once committed, they ship on the next push as they are; there are no copies to refresh.
- **Dry run.** "Dry run (no commit / push)" runs step 1 and the change scan, logs what would be committed, and stops before `git add`, `git commit` and `git push`: nothing is staged, committed or pushed. Step 1 still rewrites the manifest.
- **Cloudflare side.**
  - GitHub triggers Cloudflare Workers Builds, which deploys the Worker `av-bible`.
  - `wrangler.toml` serves `web/` as static assets (`[assets] directory = "./web"`), so the app sits at `/`, with `/audio/`, `/bibles/WEB/` and `/visuals/` beside it.
  - `web/.assetsignore` (gitignore syntax) lists what wrangler leaves out of the upload: the file itself, `*.tmp`, `*.xml`, `.DS_Store`, `Thumbs.db` and `desktop.ini`. Everything else under `web/` is public, so nothing private or scratch belongs there.
  - The build settings live in Cloudflare, not in the repo: branch `main`; watch paths `web/*`, `wrangler.toml`, `package.json` and `package-lock.json` (a push of 3,000+ files or 20+ commits always builds); build command `npm clean-install --progress=false`; deploy command `npx wrangler deploy`; build variable `SKIP_DEPENDENCY_INSTALL=1`, so the build image doesn't also pip-install `requirements.txt`. Read them with `cf builds workers get <script tag>`.
- **No local deploys.** Local `wrangler` can't run on this Windows ARM64 PC, so deploys go only through GitHub.
- **Each content file is tracked once**, in the folder it is served from.

## File budget

On the Free plan, Cloudflare's Workers static assets take at most 20,000 files in one deployed version (`publish_studio.DEPLOY_FILE_LIMIT`). Files, not bytes, are the ceiling.

`publish_studio.count_deploy_files()` counts what a deploy ships: every file under `web/` that `web/.assetsignore` doesn't exclude. It reads that file, whose patterns are basename globs, and matches them with `fnmatch`. It counts the working tree, so content not yet published is included.

| Counted | Today |
|---|---|
| The web app's own files: `index.html`, `manifest.webmanifest`, `js/`, `css/`, `icons/` | 14 |
| `web/audio/`: the narration MP3s and `manifest.json` | 2,349 |
| `web/bibles/WEB/`: one JSON per chapter | 1,189 |
| `web/visuals/`: the verse SVGs, `manifest.json` and the 8 reference-chart files | 2,250 |
| **Total** | **5,802** |

- **Cost.** A fully produced verse costs about 2 files: 1 SVG and 1 MP3.
  - A range file costs one file for its whole run.
  - An identical copy still costs a file. The manifest points past it, but the copy stays on disk and deploys.
- **Where the number shows.**
  - The main window's meter, `Files n / 20,000`. It turns amber above 90% and red over the limit, and recounts at startup, when a tool window closes and when clicked.
  - Publish's meter.
  - The Audio Renderer's confirm dialog, which adds the new files a render would create.
  - Publish's confirm dialog, counted after step 1.
- **When it fills up.** The ways to make room are listed in [ROADMAP.md](../ROADMAP.md).

## Where state lives

| What | Where | Tracked |
|---|---|---|
| Studio settings: `last_book`, `last_chapter`, `last_verse`, `svg_preview_host`, `editor`, `render_engine` | `config.json`, written through `config.update(**changes)`; an unreadable file is first copied to `config.json.bak` | no |
| The Azure key and region | the environment variables `AZURE_SPEECH_KEY` and `AZURE_SPEECH_REGION`, never a file | no |
| The Azure usage meter: one line per billed request | `azure_usage.jsonl` (`config.AZURE_USAGE_PATH`) | no (ignored) |
| TTS cache; the Studio's error log | `cache/audio/tts/`; `cache/studio_error.log` | no |
| The Verifier's verdict store | `data/ipa_checks.json` (`config.IPA_CHECKS_PATH`) | yes |
| Pronunciation list; retired entries | `pronunciations.json`; `pronunciations_archive.json` | yes |
| Generated pronunciation reports | `PRONUNCIATIONS.md`, `PRONUNCIATION_TODO.md` | no (ignored) |
| Generator registry | `svg_generators.json` | yes |
| Content: text, pictures, narration and their manifests | `web/bibles/WEB/`, `web/visuals/`, `web/audio/` | yes |
| What the site serves | `web/` in the pushed commit, less what `web/.assetsignore` excludes | yes |
| The WEB source text | `sources/eng-web.usfx.xml` (`config.SOURCES_DIR`) | no (ignored) |
| Superseded designs, mockups, scratch work, the `pre-cleanup` bundle | `C:\Dev\Theoria-archive\` beside the repo (`config.ARCHIVE_DIR`): `backups/`, `mockups/`, `_scratch/`, `pre-cleanup.bundle` | no (outside the repo) |
| Video renders | `config.RENDERS_DIR` = `Theoria-archive\renders\` | no (outside the repo) |

The git tag `pre-cleanup` marks the repo as it was before the October 2026 cleanup (`docs/archive/CLEANUP_PLAN.md`).
