# AV Bible

A Windows desktop app that reads the Bible aloud (ESV) with a visual stage
that displays graphics for the verse currently being spoken.

## Quick start

1. Double-click **run.bat** (first launch sets up the environment automatically).
2. Pick a book, chapter, and version, press **▶ Play**.

## Available Bible versions

All versions are public domain, served by bible-api.com — no keys, no setup:

| Version | Translator notes? |
|---------|-------------------|
| **KJV** — King James Version | — |
| **WEB** — World English Bible | — |
| **ASV** — American Standard Version (1901) | Yes |
| **BBE** — Bible in Basic English | — |
| **Darby** Translation | Yes |
| **Douay-Rheims** 1899 | — |

(bible-api.com allows roughly 15 requests per 30 seconds — plenty for normal
listening, and chapters are cached on disk after the first fetch.)

Audio is Microsoft Edge neural text-to-speech (free, no key): one clip is
generated per verse, so the app always knows exactly which verse is being
spoken — that drives the verse highlight and the visual stage.

Other controls: voice picker, speed slider, pause/resume, prev/next verse,
click any verse in the text panel to jump to it, and **Auto-continue** to keep
reading into the next chapter (and next book) automatically.

## Translator notes on the display

bible-api.com has no true footnote data (there is no footnote field in its
API), but the **ASV** and **Darby** texts mark *translator-supplied words* —
words added for clarity that are not in the original Hebrew/Greek, e.g.
"Commit *[thyself]* unto Jehovah" (ASV, Psalm 22:8).

With **"Show translator notes on display"** checked, those notes appear on
the visual stage while the verse that contains them is being read. The same
display slot is generic: a future source with real footnotes (e.g. the ESV
API) can feed it without further UI changes.

## About the ESV (temporarily removed)

ESV support is disabled in this proof-of-concept build to keep everything
key-free. The Crossway ESV API code paths (`fetch_esv`, `fetch_esv_audio`,
the narration mode, and the Settings dialog for the key) remain in the source,
dormant — restoring the ESV entry in `passages.TRANSLATIONS` and the Settings
button in `app.py` brings it back. The ESV API also supplies real footnotes,
which would plug directly into the translator-notes display.

## The visual stage — where your custom graphics go

The right-hand panel (and the **🖥 Display window** fullscreen mode, handy for
a second monitor or projector) is driven by verse-change events. Two ways to
customize it:

### 1. No code: drop images into `visuals/<Book>/<chapter>/`

Visuals are organized one folder per book, one subfolder per chapter, and
the renderer picks the most specific file first:

```
visuals/John/3/John_3_16.png   ← exact verse (book_chapter_verse, spaces → _)
visuals/John/3/John_3.png      ← whole chapter
visuals/John/John.png          ← whole book
visuals/default.png            ← fallback for everything
```

(Files placed flat in `visuals/` still work as a fallback, but the folder
layout is preferred — see `visuals/README.txt` for the full conventions.)

Supported formats: **PNG / JPG** (static — scaled to fill, center-cropped)
and **animated WebP / GIF** (letterboxed to fit, never cropped, so diagrams
and maps stay whole; loops continuously while the verse is read). For the
same name, an animated file wins over a static one. Prefer animated WebP
over GIF — far smaller files and full color (`Genesis_1_2.webp` is the
built-in example). Animations are capped at 100 frames and ~96 MB decoded;
oversized ones are automatically scaled down.

**Translation-specific visuals:** insert the translation code before the
extension (`Genesis_5_3.KJV.webp`) and that file is preferred when that
version is being read, falling back to the generic file otherwise. The
bundled Genesis 5 / 11 genealogy visuals use this — each translation's
name spellings (Enos/Enosh/Henoch…) appear as that translation is read.

Bundled demo visuals: Genesis 1 (photo stills), Genesis 5 and 11:10–32
(animated lifespan timelines, `generate_genealogy.py`), Exodus 25–27
(animated tabernacle diagrams, `generate_tabernacle.py`), and Matthew
1:1–17 (the genealogy of Jesus in three columns of fourteen,
`generate_matthew1.py`).

The verse reference (and translator notes, when enabled) is drawn over the
image. Sized around 1920×1080 works well for stills.

### 2. Code: write a custom renderer

Every time the spoken verse changes, the stage receives a `VerseContext`
(book, chapter, verse number, verse text, reference, position in chapter,
translation). To take over the drawing completely, subclass `Renderer` in
`visual_stage.py`:

```python
class MyRenderer(Renderer):
    def render(self, canvas, ctx, width, height):
        # ctx.book, ctx.chapter, ctx.verse, ctx.text, ctx.reference ...
        canvas.create_rectangle(0, 0, width, height, fill="navy")
        canvas.create_text(width/2, height/2, text=ctx.text, fill="white")
```

and activate it in `app.py` with `self.stage.set_renderer(MyRenderer())`.
Everything else (playback, sync, fullscreen mirroring) keeps working
unchanged.

## Project layout

| File | Purpose |
|------|---------|
| `app.py` | Main window, playback session thread, event wiring |
| `passages.py` | ESV API + WEB fallback fetching, disk cache |
| `tts_engine.py` | edge-tts synthesis (per-verse mp3s) + offline SAPI fallback |
| `audio_player.py` | mp3/wav playback via Windows MCI (no dependencies) |
| `visual_stage.py` | VerseContext, renderers, stage controller, fullscreen window |
| `books.py` | 66-book canon with chapter counts |
| `config.py` | Settings persistence (`config.json`) |

Caches live in `cache/` (synthesized audio, downloaded narration, and passage
text — the ESV text cache is capped under 500 verses per Crossway's license
terms). Safe to delete anytime.

## Copyright notes

- Scripture quotations marked "ESV" are from The Holy Bible, English Standard
  Version®, © 2001 by Crossway. Used by permission. All rights reserved.
- The ESV API's free tier is for personal, non-commercial use. If you later
  distribute this app or use it publicly (e.g. church projection), review
  Crossway's licensing at <https://api.esv.org/#conditions>.
- The World English Bible fallback is public domain.
