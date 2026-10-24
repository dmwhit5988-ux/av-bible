# Theoria Studio

The design of record for the PC app (`app.py`, launched by `run.bat`). For the data it moves and the deploy, see [architecture.md](architecture.md).

## The core idea

Everything that *produces* Theoria's assets is Python and can't run in a browser:
- `edge-tts` for the neural MP3s, and Azure (`azure_tts.py`) for names spoken from IPA;
- the `generate_*_svg.py` generators;
- `pronunciation.respell()`.

The website is a deliberately simple consumer. It reads `web/visuals/manifest.json` and `web/audio/manifest.json` and plays whatever is there. So authoring happens in the Studio, and the website is the product.

```
Studio  = author, render, check, publish   (tkinter on the PC)
Website = static, manifest-driven, no build step
Bridge  = web/visuals/, web/audio/, web/bibles/WEB/ and their manifests -> git push (web/ is the site)
```

Principles:
- **One house configuration:** WEB text, `en-US-AndrewNeural` at rate 0 (`tts_engine.HOUSE_VOICE`, `HOUSE_RATE`), SVG-only visuals. There are no per-user display toggles.
- **Generators are the source of truth for every picture.** The Studio sets up, runs, previews, checks and publishes, but it doesn't draw: drawing happens in Claude Code sessions, in generator code.
- **Deploying is one button,** Publish (D7).
- **Local tkinter plus WebView2** (through pywebview). No web framework, and no new native dependencies on this ARM64 machine.

## The main window

- **Passage bar.** Book, Chapter and Verse pickers, with ◀ ▶ to step a chapter. The Verse picker lists WEB's verse numbers (`passages.verse_numbers()`), and a verse is clamped to one the chapter has.
- **Tool bar.** One button per `TOOLS` entry, grouped as Plan, Author, Produce and Ship. The **Tools** menu repeats them and adds "Recount deploy files".
- **Deploy meter.** `Files n / 20,000` sits beside the tool bar. It turns amber above 90% and red over the limit. It recounts at startup, whenever a tool window closes, and when you click it.
- **Preview (interim).**
  - The chapter text is on the left; click a verse to play from it. The SVG stage is on the right, embedded WebView2 through `visual_stage.py` and `svg_stage.py`.
  - Play, Stop, Prev and Next drive `PlaybackSession`. It announces the chapter when it starts from the first verse, then reads each verse. The narration is synthesized live in the house voice through `tts_engine.synthesize()`, not taken from the published MP3s. It always uses Edge, so it never spends Azure characters, and names set to `use_ipa` are heard respelled or plain here; the published MP3s and ▶ IPA carry the IPA. At the end of a chapter it plays on into the next one, and it stops after Revelation.
  - While stopped, Prev and Next step one verse and roll across chapters.
  - This stage differs from the website in three ways:
    - it restarts the picture on every verse;
    - it doesn't look up range files;
    - it shows the book gradient where the website shows "isn't illustrated yet".

  The planned Preview pane (S4) replaces it.
- **Errors.** Tool, callback and worker-thread errors go to `cache/studio_error.log` and the status bar. `run.bat` starts the Studio with `pythonw`; if it can't even import, `run.bat` runs it with `python.exe` in the console instead.

## The tool registry

`app.TOOLS = {key: (label, group, factory, kind)}` drives the buttons and the menu.

- A factory imports its module only when called, so one broken tool can't stop the Studio starting. The failure is reported naming that tool.
- **Window tools** are a `tk.Toplevel` in the Studio's process. Each one's `App` implements the shared-passage contract below. All but Publish are built with the passage, as `App(top, book=…, chapter=…, verse=…)`.
- **Process tools** run as a separate process, one copy at a time (the Studio keeps the `Popen`). The Pronunciation Studio and the Verifier each hold the whole of `pronunciations.json`, so two copies would overwrite each other's edits. Between the two tools, a save merges per name with a fresh read of the file (`pronunciation.save_names`). Its lock works only within one process, so two saves within milliseconds of each other could still lose one edit.

| Key | Button (group) | Module | Kind |
|---|---|---|---|
| `coverage` | Coverage (Plan) | `coverage_studio.py` | window |
| `visuals` | Visuals (Author) | `svg_studio.py`: SVG Studio | window |
| `pronunciation` | Pronunciation (Author) | `pronunciation_tool.py` | process |
| `verifier` | Verifier (Author) | `pronunciation_check.py` | process |
| `audio` | Audio (Produce) | `audio_studio.py`: Audio Renderer | window |
| `video` | Video (Produce) | `video_studio.py`, engine `video_render.py` | window |
| `publish` | Publish (Ship) | `publish_studio.py` | window |

Each module also runs on its own as `python <module>.py`. SVG Studio, Pronunciation, Audio and Video also take `[Book] [chapter]`.

## The shared passage

Window tools implement two methods:

- `set_passage(book, chapter, verse=None, *, ask=False) -> bool` moves the tool to that passage. It returns False when the tool is busy, or when it has unsaved edits and `ask` is False. With `ask=True` it asks before discarding them.
- `can_close() -> bool` returns True when the window may close now. Otherwise it asks about unsaved edits or work in progress.

How the main window uses them:

- **A move the user makes stops playback first** (a picker, ◀ ▶, Prev/Next while stopped, Coverage's "Go to chapter"). Picking a verse inside the chapter that is playing is a jump instead, as on the website.
- **Then the move is announced** (`_passage_changed`):
  - The passage is saved (`config.update(last_book=…, last_chapter=…, last_verse=…)`).
  - `<<PassageChanged>>` fires once per real change. The verse ticking along during playback is not a change; the verse playback stopped on is.
- **Following.** Every open window tool follows with `ask=False`. One that refuses keeps its passage, and the status bar names it.
- **Re-click.** Clicking a tool's button while it is open raises it and calls `set_passage(..., ask=True)`, so SVG Studio asks before discarding unsaved edits.
- **Closing the main window** asks each open tool's `can_close()` in turn. One "no" keeps the Studio open.
  - Audio and Video renders finish the verse they are on.
  - Publish refuses while a publish runs.
  - The Pronunciation and Verifier processes are left running.
- **Process tools** get the passage only at launch (Pronunciation takes the book and chapter; the Verifier takes none). They don't follow later moves.

## The tools

### Coverage (`coverage_studio.py`)

The backlog. One tree over the canon (66 books, 1,189 chapters) shows, per chapter:
- **Verses:** the chapter length;
- **Visuals:** verses with a picture, and their kinds;
- **Audio:** verses narrated;
- **Unreviewed names:** proper nouns not yet in `pronunciations.json`;
- **Candidate:** the chapter's entry in the content catalog.

The Filter box offers: All chapters, Has content, Candidate gaps (no visuals), Unreviewed names. "Go to chapter" or a double-click sets the shared passage.

- **Reads:**
  - `web/bibles/WEB/`, `web/visuals/manifest.json`, `web/audio/manifest.json`;
  - `pronunciations.json` (`pronunciation.load`, with `scan_proper_nouns` over the WEB text);
  - [content-catalog.md](content-catalog.md). Coverage machine-reads it: it parses `### <Book>` headings and `- **<Book> <chapters>** — …` entries, and skips an entry with no chapter number.
- **Writes:** nothing.
- **Passage:** always follows, by selecting the row. `can_close()` is always True.

### Visuals: SVG Studio (`svg_studio.py`)

- **What it does:**
  - routes edits of a generator-owned verse to the generator's spec;
  - re-runs the generator;
  - previews the working SVG with its narration;
  - saves into `web/visuals/`.

  Design: [svg-studio.md](svg-studio.md).
- **Reads:** `web/visuals/<Book>/<ch>/<Book>_<ch>_<v>.svg`, `svg_generators.json`, the verse's MP3 in `web/audio/` (for the preview), and the `editor` and `svg_preview_host` settings.
- **Writes:**
  - the verse's SVG (Save);
  - `web/visuals/manifest.json`, by running `build_manifest.py` (Save + manifest);
  - every SVG of a family, by running its generator (Re-run generator);
  - the `svg_preview_host` setting.
- **Passage:**
  - When it follows the main window, it swaps the preview picture without narrating.
  - It stays put while a generator runs, or while the pane has unsaved edits.
  - On a re-click it asks before discarding them.
  - `can_close()` asks when a generator is running or edits are unsaved.

### Pronunciation (`pronunciation_tool.py`, a separate process)

- **What it does:** lists the proper nouns of a chapter. For each one you can:
  - hear the name as the voice says it (`tts_engine.synthesize(..., apply_respell=False)` in the house voice);
  - type and hear a "Say it" respelling;
  - edit the IPA and hear Azure say it (▶ IPA, `tts_engine.synthesize_ipa`), then tick **Use** to speak it from the IPA in Azure renders;
  - mark it Custom or "✓ Fine".

  Names are keyed by WEB spelling, so a fix applies everywhere the name occurs. ▶ IPA spends Azure characters, and the bottom line shows the meter.
- **Reads:** `web/bibles/WEB/`, `pronunciations.json`, `azure_usage.jsonl`.
- **Writes:**
  - `pronunciations.json`, via `pronunciation.save_names`, which merges per name with a fresh read;
  - the generated `PRONUNCIATIONS.md`;
  - the TTS cache;
  - `azure_usage.jsonl`, one line per ▶ IPA that reached Azure.

See [pronunciation.md](pronunciation.md).

### Verifier (`pronunciation_check.py`, a separate process)

- **What it does:**
  - synthesizes each name in carrier sentences in the house voice;
  - transcribes the audio back to IPA with `ipa_asr` (a wav2vec2 phoneme model);
  - scores the result against the stored `ipa`.

  It ranks suspicion; it doesn't issue verdicts. It needs the optional torch and transformers packages, and the model (about 1.2 GB) downloads on first run.
- **Reads:** `pronunciations.json`, `data/ipa_checks.json`.
- **Writes:** `data/ipa_checks.json` (the verdict store, tracked), and verdicts into `pronunciations.json` on Save.
- **Passage:** none. It works across the whole list.

### Audio: Audio Renderer (`audio_studio.py`)

- **What it does:** renders the narration MP3s for a book and chapter range, through `generate_showcase_audio.generate_chapter()`.
  - An existing file is skipped while it is current, and re-rendered once a pronunciation change has made it stale (`generate_showcase_audio.is_current`). The confirm dialog counts those re-renders. "Overwrite every existing file" re-renders all of them, which is for a voice or engine change.
  - "Voice override" is the one voice picker in the Studio. It applies to one render and is not saved.
  - "Engine" picks who speaks: Edge (free, respellings only), Azure for the verses with IPA names and Edge for the rest, or Azure for every verse ([pronunciation.md](pronunciation.md#ipa-through-azure)). The choice is remembered (`render_engine`). The Azure options are greyed out until `AZURE_SPEECH_KEY` and `AZURE_SPEECH_REGION` are set.
  - Before rendering, a confirm dialog shows the new-file count against the deploy budget. With an Azure engine it also shows the verses Azure will speak, their characters, how long the free tier's pace makes that take, and the last 31 days' use against 500,000. It warns when the render would go past that.
  - A verse is skipped when edge-tts is unreachable, so the offline voice never ships. A verse Azure refuses is skipped as "refused by Azure". A bad key, a used-up month or no network stops the render.
- **Reads:** `web/bibles/WEB/`, `pronunciations.json` (via `respell()` and `ssml()`), `web/audio/manifest.json`, `azure_usage.jsonl`.
- **Writes:**
  - `web/audio/<Book>_<ch>_<v>.mp3`;
  - `web/audio/manifest.json`, merged and saved after every chapter, so an interrupted render resumes;
  - the TTS cache;
  - `azure_usage.jsonl`, one line per verse Azure speaks.
- **Passage:**
  - A chapter already inside the From..To range leaves the range alone. Any other chapter becomes the range.
  - It refuses while a scan, its confirm dialog or a render is running.
  - `can_close()` asks during a render.

### Video: Video Studio (`video_studio.py`)

- **What it does:** renders a verse range to a 4K MP4 with captions, a description and a thumbnail. Design: [video-studio.md](video-studio.md).
- **Reads:** `web/audio/` MP3s (it synthesizes any that are missing), `web/visuals/`, `web/bibles/WEB/`, `svg_generators.json` (the `replay_identical` opt-out).
- **Writes:**
  - the MP4 and its sidecars, in `config.RENDERS_DIR` by default;
  - with "Also publish new narration to web/audio" ticked, newly synthesized MP3s, into `web/audio/` and its manifest.
- **Passage:**
  - The range starts at the passage and ends with its chapter.
  - A range you edited by hand is kept while the passage's chapter lies inside it.
  - It refuses while rendering, and `can_close()` asks during a render.

### Publish (`publish_studio.py`)

- **What it does:** rebuilds the visuals manifest, then makes a content-only commit and push. It has a "Dry run (no commit / push)" box. The steps, the content paths and the web-code warning are in [architecture.md](architecture.md#deploy).
- **Reads:** git status, the content folders.
- **Writes:** `web/visuals/manifest.json`, one commit of `CONTENT_PATHS`, and the push.
- **Passage:** `set_passage()` does nothing and returns True. `can_close()` refuses while a publish runs.

## The chapter workflow

What the Studio is built around, from catalog entry to published chapter. Steps marked *(planned)* don't exist yet.

1. **Pick a chapter.**
   - Today: Coverage with the "Candidate gaps (no visuals)" filter, and the chapter's catalog entry and design notes in `docs/design/`.
   - *(planned, S5)* a **Next up** queue of high-priority candidates, linked to their design records.
2. **Names.** Clear the chapter's unreviewed names in Pronunciation before rendering audio, because the audio depends on them.
3. **Audio.** Render the chapter in Audio. When a pronunciation changes later, render the chapter again: only the stale verses are re-rendered. *(planned, S3)* lint flags the stale verses.
4. **Visuals.**
   - Today:
     - the generator is written in a Claude Code session and registered in `svg_generators.json`;
     - then run it, or use SVG Studio's "Re-run generator";
     - then check each verse in SVG Studio's preview with its narration.
   - *(planned, S5)* **New visual family…** writes a generator from a template, plus its registry entry, and copies a ready-to-paste Claude prompt: the catalog entry, design notes, WEB text and house rules. The template iterates `verse_numbers()`.
   - *(planned, S5)* **Regenerate to scratch → compare → Accept.**
5. **Preview.**
   - Today: the main window's interim player, or the web app served locally from `web/` (`python -m http.server 8000 -d web`, the `web-static` entry in `.claude/launch.json`). It serves the working tree, so rebuild the manifest first when pictures changed.
   - *(planned, S4)* the Preview pane: the chapter end to end, exactly as the website shows it.
6. **Publish.** *(planned, S3)* lint runs first, and an optional separate commit of the sources follows the content commit.
7. **Video** (optional): a 4K MP4 in Video Studio.

## Generator CLI contract (planned, S5)

Every generator should accept the same three flags:
- `--only CH[:V]`: write one chapter or verse;
- `--out DIR`: write into a scratch folder instead of `web/visuals/`;
- `--dry`: report without writing.

A `cli` capability field in the registry says which generators support them, so SVG Studio and Regenerate-to-scratch know what they can ask for.

Today, of the 24 distinct registered generators:
- `generate_1chronicles_tree_svg.py` is the reference implementation. It has `--only N` (a chapter), `--out DIR` and `--dry`.
- `generate_matthew1_svg.py` has `--out` and `--dry`.
- The rest take no arguments and rewrite their whole family. SVG Studio's Re-run runs a generator with no arguments.

## Lint (planned, S3)

`lint.py`: pure checks with a CLI. Publish shows the report and refuses on blockers, keeping its dry-run box. The checks:

**Deploy and narration**
- The file budget against `DEPLOY_FILE_LIMIT`.
- **Partial-audio chapters:** some verses narrated but not all. This needs its own rule, because such a chapter may have no visuals.
- **Stale narration:** `generate_showcase_audio.is_current()` for every published verse, the check the Audio Renderer already makes per render. A fingerprint file can back it up in case the cache is cleared.
- **Audio-timed visuals** (1 Chronicles 1–9, Matthew 1) flagged when their MP3s change.

**Visual keys and files**
- Visual keys equal WEB's verses: no orphan keys, and no WEB verse missing a picture in a started chapter.
- A per-verse file inside a range file's run (warning; D17).
- Every visuals folder has a registry owner.
- Generator and spec files are tracked and clean.
- Every SVG parses.
- The manifest is newer than the newest SVG.
- No translation-suffixed or `.still.svg` files.

**SVG audit**
- Overlapping text, text wider than its box, text off-canvas. Promoted from `tools/audit_heb.py`; the method is in [design/romans.md](design/romans.md).

## Phases

| Phase | Status | Contents |
|---|---|---|
| **S1 Harden** | **Done** (WS5) | Toggles stripped; house voice; tool registry with lazy imports; close checks; single-instance process tools and merge-on-save; `config.update`; atomic audio-manifest writes; the shared passage; the MCI alias fix; rebrand |
| **S2 Consolidate** | planned | `studio_core.py`: verse keys and paths, WEB verse lists, the deploy budget, house size and palette without `generate_tabernacle`'s import side effects. `narration.py`: the audio naming and manifest helpers from `generate_showcase_audio`, made public. `ui_common.py`: picker, event pump, log pane. One visual resolver replacing `visual_stage.find_svg`, `video_render.resolve_svg` and `svg_preview.resolve_audio`. One `web_view.py` merging `svg_preview.py` and `svg_stage.py`. Each `App` takes a parent frame. SVG Studio's hand-authoring features retire (D12), leaving a read-only Source view |
| **S3 Lint + Publish** | planned | The lint above; Publish refuses on blockers; "commit sources" as a separate commit |
| **S4 Hub window** | planned | Coverage becomes the home pane, with the **Preview pane** beside it, the grouped tool bar and the budget meter in the header. Pronunciation Studio runs in-process; the Verifier stays a separate process |
| **S5 Workflow features** | planned | The generator CLI contract; regenerate to scratch → compare → Accept; New visual family… (with an option to write range files); the Next-up queue; a chapter contact sheet of settled end frames |
| **S6 Optional** | planned | Tabs instead of windows; `svg_palette.py` extracted (which also sets up colour themes); a browser for the `svg_figures` and `svg_vocab` figure vocabularies; a Video render queue and thumbnail composer |

**The Preview pane (S4).**
- **How it works.** A daemon `http.server` on 127.0.0.1 plus embedded WebView2, showing the real web app at `/?b=&c=&v=`. It uses the `--autoplay-policy=no-user-gesture-required` flag `svg_preview.py` already sets, with "Rebuild manifest" beside it.
- **Serving.** It must serve the production layout at `/`, because the web app fetches root-absolute paths (`/visuals/…`, `/bibles/WEB/…`). That layout is `web/` itself (`config.WEB_DIR`), so a plain `http.server` handler rooted there is enough.
- **Depends on** web deep links, which `web/js` doesn't have yet.
- **Before the old player goes,** a parity checklist runs on this PC:
  - deep links land on the verse;
  - MP3s autoplay;
  - a chapter without MP3s falls back to Web Speech;
  - the "isn't illustrated yet" pointer and the ✦ list work;
  - the end of a chapter rolls into the next;
  - a regenerated verse shows after "Rebuild manifest";
  - closing leaves no server or WebView2 process behind.

  Only after it passes are `PlaybackSession`, the transport code, `visual_stage.py` and `svg_stage.py` deleted.

**Shared visuals in the Studio (D17, planned).**
- SVG Studio labels a verse "shared with vv16-32" when its picture is a range file or an identical copy, and editing it says it affects the whole run. Today SVG Studio edits one `<Book>_<ch>_<v>.svg` per verse and doesn't know range files.
- The interim stage doesn't look range files up either. It is retired after S4, and the Preview runs the web app, which does.
- **Retiring:** Video Studio's "Also publish new narration" option; the Audio tool and the lint cover it.

## What not to build

- A vector editor or in-app drawing; an in-app code editor ("open in editor" is enough).
- Anything for more than one translation, including "just in case" hooks.
- A browser or Electron rewrite of the Studio.
- Loading the Verifier's torch model into the Studio's own process.
- A task tracker or database; the catalog plus measured state is the backlog.
- CI-driven content builds or automatic publishing.
- A video engine rework: `video_render.py` works, and it only gets re-hosted.
