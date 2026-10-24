"""Pre-render neural-voice narration into web/audio/ for the web app.

The web app reads aloud via the browser's Web Speech API wherever it has no
MP3, and on most devices that sounds far more robotic than edge-tts's neural
voices (no key needed, but it's a Python library — a static site can't call
it directly). This module renders the MP3s instead. The Audio Renderer
(audio_studio.py) renders through generate_chapter(), and it and Video Studio
(video_render.py) both use the manifest helpers; run as a script, main()
renders the fixed SHOWCASE_CHAPTERS list.

For each verse it reuses tts_engine.synthesize() in the house voice (the
same call the Studio's player makes) and copies the resulting neural mp3
into web/audio/, then updates web/audio/manifest.json — a flat
{"Book_ch_v.WEB": "Book_ch_v.mp3"} map, one entry per verse. The ".WEB" on
the key is a fixed part of the format (the web player looks up
"<verse>.WEB"); the filename has no suffix. The web player falls back to
Web Speech for any verse with no MP3. The Audio Renderer and Video Studio
write the manifest too, so every write merges with what is on disk.

Resumable: skips verses whose mp3 already exists and is current
(is_current), so a re-render picks up exactly the verses a pronunciation
change has made stale -- a name's respelling or IPA, or a verse's own words
-- and nothing else. Only ships real neural
audio — if edge-tts is unreachable and tts_engine falls back to the lower
quality offline SAPI voice, that verse is skipped rather than shipping
degraded audio (rerun later once online). The engine (tts_engine.ENGINES)
decides which verses Azure speaks; a verse Azure refuses is skipped as
"failed", and a refusal that would repeat for every verse (bad key, quota
used up, offline) stops the render.

Usage:
    python generate_showcase_audio.py
"""

import filecmp
import json
import os
import shutil
import threading
import time

import azure_tts
import config
from passages import load_chapter, PassageError
import tts_engine

VOICE = tts_engine.HOUSE_VOICE
RATE = tts_engine.HOUSE_RATE
TRANSLATION = "WEB"  # suffix on every manifest key: Book_ch_v.WEB

# The fixed list main() renders. The Audio Renderer renders any chapter.
SHOWCASE_CHAPTERS = [
    ("Genesis", 1), ("Genesis", 5), ("Genesis", 11),
    ("Exodus", 25), ("Exodus", 26), ("Exodus", 27),
    ("Numbers", 32), ("Numbers", 34),
    ("Matthew", 1),
    ("Luke", 3),
    ("Acts", 13), ("Acts", 14),
]

AUDIO_DIR = config.WEB_AUDIO_DIR
MANIFEST_PATH = os.path.join(AUDIO_DIR, "manifest.json")

# Serialises the read-merge-write in _save_manifest across threads: the Audio
# Renderer and Video Studio both write the manifest from worker threads of the
# one Studio process.
_MANIFEST_LOCK = threading.Lock()


def _manifest_key(base: str) -> str:
    """'Genesis_1_1' -> 'Genesis_1_1.WEB'."""
    return f"{base}.{TRANSLATION}"


def _audio_filename(base: str) -> str:
    """'Genesis_1_1' -> 'Genesis_1_1.mp3'."""
    return f"{base}.mp3"


def is_current(text: str, ref: str, out_path: str, voice: str = VOICE,
               rate: int = RATE) -> bool:
    """True when the published mp3 at ``out_path`` is ``text`` (the verse
    ``ref``) as it would be spoken today.

    Each published mp3 is a byte copy of the TTS cache entry it was rendered
    from, and that entry is keyed on the text actually spoken, so a
    pronunciation change since -- a name's respelling or IPA, or the verse's
    own words -- leaves the mp3 matching no entry for today's text. Edge's
    route and Azure's IPA route both count, so switching engine alone doesn't
    make a verse stale; that, like a new voice, takes Overwrite. A cleared
    cache makes every verse look stale, which the Audio Renderer's confirm
    step shows before anything is synthesized.
    """
    for engine in (tts_engine.ENGINE_EDGE, tts_engine.ENGINE_MIXED):
        path = tts_engine.route(text, voice, rate, engine, ref=ref).path
        if os.path.exists(path) and filecmp.cmp(path, out_path, shallow=False):
            return True
    return False


# How many times a manifest read or write is tried, 50 ms apart, while
# Windows refuses it because another thread or process has the file open.
_ATTEMPTS = 20


def _load_manifest() -> dict:
    """web/audio/manifest.json as a dict; {} if it is missing or unreadable."""
    for attempt in range(_ATTEMPTS):
        try:
            with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, dict) else {}
        except PermissionError:          # mid-swap: try again
            if attempt == _ATTEMPTS - 1:
                return {}
            time.sleep(0.05)
        except (OSError, ValueError):
            return {}


def _save_manifest(manifest: dict) -> dict:
    """Merge ``manifest`` into web/audio/manifest.json; return what was written.

    Each writer holds the copy it loaded when its render began, so writing that
    copy back whole would drop every verse another render published since. The
    file is re-read under a lock and the caller's entries laid over it (entries
    are only ever added or re-pointed, never removed), then written to a temp
    file and swapped in with os.replace, so a reader never sees half a file.

    The temp name is unique to this process and thread, so two writers never
    share one. A swap refused because the file is open elsewhere
    (PermissionError), or a temp file or folder gone from under it
    (FileNotFoundError), is retried from the re-read, briefly; after that the
    error is raised. No temp file is ever left behind.
    """
    tmp = f"{MANIFEST_PATH}.{os.getpid()}.{threading.get_ident()}.tmp"
    with _MANIFEST_LOCK:
        for attempt in range(_ATTEMPTS):
            merged = _load_manifest()
            merged.update(manifest)
            try:
                os.makedirs(os.path.dirname(MANIFEST_PATH), exist_ok=True)
                with open(tmp, "w", encoding="utf-8") as f:
                    json.dump(merged, f, indent=2, sort_keys=True)
                os.replace(tmp, MANIFEST_PATH)
                return merged
            except (PermissionError, FileNotFoundError):
                if attempt == _ATTEMPTS - 1:
                    raise
                time.sleep(0.05)
            finally:
                if os.path.exists(tmp):    # web/audio ships whole: never leave it
                    try:
                        os.remove(tmp)
                    except OSError:
                        pass


def generate_chapter(book: str, chapter: int, manifest: dict, voice: str = VOICE,
                      rate: int = RATE, passage=None, on_verse=None,
                      should_stop=None, force: bool = False,
                      engine: str = tts_engine.ENGINE_EDGE) -> tuple:
    """Render one chapter's verses into web/audio/ and update `manifest`.

    Reused by both this CLI script and the Audio Renderer studio (audio_studio.py)
    so both go through the exact same synth/copy/manifest logic.

    `passage`, if given, skips the load (the studio loads each chapter during
    its file-count scan and reuses it here). `on_verse(num, status)` is called
    after each verse with status in {"written", "skipped", "degraded",
    "failed"} — lets a caller drive a progress bar. `should_stop()`, checked
    before each verse, lets a caller cancel between verses. Returns
    (written, skipped, degraded); a "failed" verse counts as degraded.

    `engine` is a tts_engine engine. A verse Azure refuses (usually an IPA
    symbol it doesn't know) is "failed" and skipped; an azure_tts.AzureError
    that is ``fatal`` is raised, ending the render.

    A verse whose MP3 already exists is skipped while it is current
    (is_current) and re-rendered once a pronunciation change has made it
    stale. `force=True` re-renders every verse whose MP3 already exists,
    overwriting the file in place (same filename, new bytes — the publish
    flow ships it as a modified file); that is for a voice or engine change.
    Either way interrupted renders stay resumable.
    """
    if passage is None:
        try:
            passage = load_chapter(book, chapter)
        except PassageError as e:
            print(f"  skip {book} {chapter}: {e}")
            return 0, 0, 0
    safe_book = book.replace(" ", "_")
    written = skipped = degraded = 0
    for num, text in passage.verses:
        if should_stop and should_stop():
            break
        base = f"{safe_book}_{chapter}_{num}"
        key = _manifest_key(base)
        filename = _audio_filename(base)
        out_path = os.path.join(AUDIO_DIR, filename)
        ref = f"{book} {chapter}:{num}"
        if (not force and key in manifest and os.path.exists(out_path)
                and is_current(text, ref, out_path, voice, rate)):
            skipped += 1
            if on_verse:
                on_verse(num, "skipped")
            continue
        try:
            src_path = tts_engine.synthesize(
                text, voice, rate, engine=engine, label=ref, ref=ref)
        except azure_tts.AzureError as e:
            if e.fatal:
                raise
            degraded += 1
            print(f"    {book} {chapter}:{num} — Azure refused it, skipped: {e}")
            if on_verse:
                on_verse(num, "failed")
            continue
        if not src_path.lower().endswith(".mp3"):
            # tts_engine fell back to the offline SAPI voice (edge-tts
            # unreachable) — don't ship degraded audio.
            degraded += 1
            print(f"    {book} {chapter}:{num} — edge-tts unavailable, "
                  f"skipped (rerun later)")
            if on_verse:
                on_verse(num, "degraded")
            continue
        os.makedirs(AUDIO_DIR, exist_ok=True)
        shutil.copyfile(src_path, out_path)
        manifest[key] = filename
        written += 1
        if on_verse:
            on_verse(num, "written")
    print(f"  {book} {chapter}: {written} written, {skipped} already present"
          + (f", {degraded} degraded/skipped" if degraded else ""))
    return written, skipped, degraded


def main() -> int:
    os.makedirs(AUDIO_DIR, exist_ok=True)
    manifest = _load_manifest()
    print(f"Generating showcase narration ({VOICE}) for "
          f"{len(SHOWCASE_CHAPTERS)} chapter(s)...")
    for book, chapter in SHOWCASE_CHAPTERS:
        generate_chapter(book, chapter, manifest)
        _save_manifest(manifest)  # save after each chapter, resumable
    total_bytes = sum(
        os.path.getsize(os.path.join(AUDIO_DIR, fn))
        for fn in manifest.values()
        if os.path.exists(os.path.join(AUDIO_DIR, fn))
    )
    print(f"\nDone: {len(manifest)} verse(s) narrated, "
          f"{total_bytes / 1_000_000:.1f} MB in {AUDIO_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
