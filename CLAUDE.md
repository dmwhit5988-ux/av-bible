# CLAUDE.md

These are the rules for AI coding sessions in this repo. [README.md](README.md)
explains the project, and `docs/` has the detail.

## Machine

- The PC runs Windows 11 ARM64, but the venv Python (3.14) is an emulated x64 build.
  `platform.machine()` reports `ARM64`. Check `sysconfig.get_platform()` instead,
  which reports `win-amd64`, before ruling out a package. x64 wheels such as torch
  install fine.
- Node is native ARM64, so npm packages that are only built for x64 fail. Wrangler's
  `workerd` is one of them. Don't add native dependencies the Studio doesn't already
  have.
- Use `.venv\Scripts\python.exe` and install packages into `.venv`.
- Search with `git grep` or the Grep tool. Never run `grep -r` over the tree, because
  `.venv/` and `cache/` are huge.

## Git and deploy

- **A push to `main` is a deploy.** Cloudflare Workers Builds deploys the Worker
  `av-bible` from `deploy_bundle/`. Never push without asking the user first.
- Commit locally first, then ask before pushing. Publish's own `git push` sends any
  local commits too.
- Deploy only through GitHub. Local wrangler can't run on this PC, so don't try to
  work around that.
- To confirm that a push deployed, check the "Workers Builds: av-bible" check run on
  the commit:
  `curl -s https://api.github.com/repos/dmwhit5988-ux/av-bible/commits/<sha>/check-runs`.
  The repo is public, so no auth is needed. `gh` isn't installed.
- For the user, deploying stays one button: Publish in the Studio. Any change to the
  deploy layout must update Publish (`publish_studio.py`, `prepare-deploy.ps1`) in the
  same commit, and must be checked with a Publish dry run.
- Publish commits only `publish_studio.CONTENT_PATHS`. Commit code and docs by hand.
  When you change web-app files, refresh their `deploy_bundle/` copies with a Publish
  dry run or `prepare-deploy.ps1`, then commit the copies too.
- Mind the file budget. A deploy can hold about 20,000 files
  (`publish_studio.DEPLOY_FILE_LIMIT`, counted by `count_deploy_files()`), and the
  ceiling is files, not bytes. Every file added under `web/`, `bibles/` or `visuals/`
  counts.

## Scope

- WEB is the only translation. Never add translation pickers, translation variants,
  or hooks for other translations.
- Don't add or propose still images, reduced-motion support, a speed control or a
  notes toggle. These were decided against (D4–D6).

## Web app

- `web/` is static vanilla JS with no build step, no framework and no bundler.
- The page fetches root-absolute paths (`/visuals/…`, `/bibles/WEB/…`), so test it
  served at a site root, for example `deploy_bundle/`.

## Studio

- The Studio is tkinter. A window tool is a `tk.Toplevel` registered in the `TOOLS`
  registry in `app.py`. Its `App` implements
  `set_passage(book, chapter, verse=None, *, ask=False) -> bool` and
  `can_close() -> bool`. A process tool runs as a separate process, one copy at a
  time.
- Write settings with `config.update(**changes)`. Never `config.save()` a dict you
  loaded earlier, because that undoes other windows' changes.
- Narration always uses `tts_engine.HOUSE_VOICE` and `tts_engine.HOUSE_RATE`.
- Write `pronunciations.json` through `pronunciation.save_names()`, which merges
  concurrent saves. `PRONUNCIATIONS.md` and `PRONUNCIATION_TODO.md` are generated and
  ignored, so never edit them.
- Never load the Verifier's torch model into the Studio's own process.

## Visuals

- Generators (`generate_*_svg.py` and the spec modules named in
  `svg_generators.json`) are the source of truth. Never hand-edit a generated SVG.
  Change the spec and regenerate instead. Every published verse SVG needs an owner in
  `svg_generators.json`. The wall charts in `visuals/reference/` are exempt: they
  stay deployed and unlinked, and the 1–2 Chronicles chart is a frozen file with no
  generator ([docs/reference-charts.md](docs/reference-charts.md)).
- Take verse numbers from `passages.verse_numbers()`. Never hard-code chapter
  lengths.
- Animate with SMIL, and keep the motion.
- Put no caption lines and no prose on a graphic, because the verse is narrated.
  Use names, numbers and labelled drawings only.
- Draw people, creatures and objects with `svg_figures.py`, the shared vocabulary.
- To show one picture across consecutive verses, write a range file
  `Book_c_v1-v2.svg`. Don't write a copy for each verse, because every copy costs a
  deploy file.
- After changing visuals, run `build_manifest.py`.

## Housekeeping

- Put superseded designs, backups, renders and scratch work in
  `C:\Dev\Theoria-archive` (`config.ARCHIVE_DIR`), never in the repo.
- Before committing, run
  `.venv\Scripts\python.exe -m unittest test_imports test_registry test_svg_freeze test_shared_visuals`.
- In living docs, describe what is, and cite file and function names, not line
  numbers. History belongs in git and `docs/archive/`, and the archive is not
  updated.
- Where docs live:
  - `README.md`: overview and deploy.
  - `ROADMAP.md`: plans.
  - `CREDITS.md`: credits.
  - `docs/architecture.md`, `docs/studio.md`, `docs/visuals.md` and
    `docs/pronunciation.md`: how things work.
  - `docs/content-catalog.md`: the backlog. Coverage parses it, so keep the
    `### <Book>` headings and the `- **<Book> <chapters>** — …` entries.
  - `docs/design/`: build records.
