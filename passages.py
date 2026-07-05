"""Fetch Bible passages.

Primary source: Crossway's official ESV API (https://api.esv.org) — free key
required for personal, non-commercial use.

Fallback source: bible-api.com serving the public-domain World English Bible
(WEB), used only so the app works before an ESV key has been entered.

A small on-disk cache keeps repeat chapter loads instant. To respect the ESV
API's condition that no more than 500 verses be stored locally, the ESV cache
is capped and oldest chapters are evicted first.
"""

import json
import os
import re
import time
from dataclasses import dataclass, field

import requests

from config import PASSAGE_CACHE_DIR, AUDIO_CACHE_DIR, BIBLES_DIR
from books import chapters_in

ESV_TEXT_URL = "https://api.esv.org/v3/passage/text/"
ESV_AUDIO_URL = "https://api.esv.org/v3/passage/audio/"
BIBLE_API_URL = "https://bible-api.com/{query}?translation={translation}"

ESV_CACHE_VERSE_LIMIT = 450  # stay under the 500-verse local storage limit

# code, dropdown label, bible-api.com id, attribution, source
#   source "api"   -> fetched live from bible-api.com (api_id used)
#   source "local" -> read from bibles/<CODE>/ JSON bundled with the app
#                     (api_id is None)
# (ESV via Crossway's API is temporarily removed from this list for the
#  proof of concept; fetch_esv/fetch_esv_audio below remain for its return.)
TRANSLATIONS = [
    ("KJV", "KJV — King James", "kjv",
     "King James Version — public domain.", "api"),
    ("WEB", "WEB — World English", "web",
     "World English Bible — public domain.", "api"),
    ("ASV", "ASV — American Standard", "asv",
     "American Standard Version (1901) — public domain.", "api"),
    ("BBE", "BBE — Basic English", "bbe",
     "Bible in Basic English — public domain.", "api"),
    ("DARBY", "Darby Translation", "darby",
     "Darby Translation — public domain.", "api"),
    ("DRA", "Douay-Rheims 1899", "dra",
     "Douay-Rheims 1899 American Edition — public domain.", "api"),
    ("BSB", "BSB — Berean Standard", None,
     "Berean Standard Bible — public domain.", "local"),
    ("YLT", "YLT — Young's Literal", None,
     "Young's Literal Translation — public domain.", "local"),
    ("OEB", "OEB — Open English (partial)", None,
     "Open English Bible — public domain (CC0). Not all books complete.",
     "local"),
]

TRANSLATION_LABELS = {code: label for code, label, *_ in TRANSLATIONS}
TRANSLATION_IDS = {code: api_id for code, _, api_id, *_ in TRANSLATIONS}
TRANSLATION_ATTRIBUTION = {code: attr for code, _, _, attr, _ in TRANSLATIONS}
TRANSLATION_SOURCES = {code: source for code, _, _, _, source in TRANSLATIONS}


class PassageError(Exception):
    """User-presentable fetch failure."""


@dataclass
class Passage:
    book: str
    chapter: int
    canonical: str                      # e.g. "John 3"
    translation: str                    # e.g. "KJV", "WEB"
    verses: list = field(default_factory=list)  # [(verse_number, text), ...]
    # Per-verse translator notes, aligned with `verses` by index. For
    # bible-api.com texts these are the bracketed words the translators
    # supplied for clarity (ASV and Darby carry them; the API has no
    # separate footnote field). Kept generic so richer sources (e.g. the
    # ESV API's real footnotes) can fill the same slot later.
    notes: list = field(default_factory=list)   # [[note, ...], ...]


# ---------------------------------------------------------------------------
# Disk cache
# ---------------------------------------------------------------------------

def _cache_path(translation: str, book: str, chapter: int) -> str:
    safe_book = book.replace(" ", "_")
    # ".v2" marks the format that includes per-verse notes; older cache
    # files are simply ignored.
    return os.path.join(PASSAGE_CACHE_DIR,
                        f"{translation}_{safe_book}_{chapter}.v2.json")


def _cache_get(translation: str, book: str, chapter: int):
    path = _cache_path(translation, book, chapter)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return Passage(**data)
    except (OSError, ValueError, TypeError):
        return None


def _cache_put(passage: Passage) -> None:
    path = _cache_path(passage.translation, passage.book, passage.chapter)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(passage.__dict__, f)
    except OSError:
        return
    if passage.translation == "ESV":
        _evict_esv_cache()


def _evict_esv_cache() -> None:
    """Keep total ESV verses cached on disk under the license limit."""
    entries = []
    try:
        names = os.listdir(PASSAGE_CACHE_DIR)
    except OSError:
        return
    for name in names:
        if not name.startswith("ESV_"):
            continue
        path = os.path.join(PASSAGE_CACHE_DIR, name)
        try:
            with open(path, "r", encoding="utf-8") as f:
                count = len(json.load(f).get("verses", []))
            entries.append((os.path.getmtime(path), path, count))
        except (OSError, ValueError):
            continue
    entries.sort(reverse=True)  # newest first
    total = 0
    for _, path, count in entries:
        total += count
        if total > ESV_CACHE_VERSE_LIMIT:
            try:
                os.remove(path)
            except OSError:
                pass


# ---------------------------------------------------------------------------
# ESV API
# ---------------------------------------------------------------------------

_VERSE_SPLIT = re.compile(r"\[(\d+)\]")


def _parse_esv_text(raw: str) -> list:
    """Split ESV plain text on bracketed verse numbers into (num, text) pairs."""
    parts = _VERSE_SPLIT.split(raw)
    verses = []
    # parts = [prefix, num, text, num, text, ...]
    for i in range(1, len(parts) - 1, 2):
        num = int(parts[i])
        text = re.sub(r"\s+", " ", parts[i + 1]).strip()
        if text:
            verses.append((num, text))
    return verses


def fetch_esv(api_key: str, book: str, chapter: int) -> Passage:
    cached = _cache_get("ESV", book, chapter)
    if cached:
        return cached
    params = {
        "q": f"{book} {chapter}",
        "include-passage-references": "false",
        "include-verse-numbers": "true",
        "include-first-verse-numbers": "true",
        "include-footnotes": "false",
        "include-headings": "false",
        "include-short-copyright": "false",
        "include-selahs": "true",
        "indent-poetry": "false",
        "indent-paragraphs": "0",
        "include-passage-horizontal-lines": "false",
        "include-heading-horizontal-lines": "false",
    }
    try:
        resp = requests.get(
            ESV_TEXT_URL,
            params=params,
            headers={"Authorization": f"Token {api_key}"},
            timeout=20,
        )
    except requests.RequestException as e:
        raise PassageError(f"Could not reach the ESV API: {e}") from e
    if resp.status_code == 401:
        raise PassageError("The ESV API rejected your key. Check it in Settings.")
    if resp.status_code == 429:
        raise PassageError("ESV API daily request limit reached. Try again later.")
    if resp.status_code != 200:
        raise PassageError(f"ESV API error (HTTP {resp.status_code}).")
    data = resp.json()
    passages = data.get("passages") or []
    if not passages or not passages[0].strip():
        raise PassageError(f"The ESV API returned no text for {book} {chapter}.")
    verses = _parse_esv_text(passages[0])
    if not verses:
        raise PassageError(f"Could not parse verses for {book} {chapter}.")
    passage = Passage(
        book=book,
        chapter=chapter,
        canonical=data.get("canonical") or f"{book} {chapter}",
        translation="ESV",
        verses=verses,
    )
    _cache_put(passage)
    return passage


def fetch_esv_audio(api_key: str, book: str, chapter: int) -> str:
    """Download the official ESV narration mp3 for a chapter. Returns file path."""
    safe_book = book.replace(" ", "_")
    out_path = os.path.join(AUDIO_CACHE_DIR, f"esv_narration_{safe_book}_{chapter}.mp3")
    if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
        return out_path
    try:
        resp = requests.get(
            ESV_AUDIO_URL,
            params={"q": f"{book} {chapter}"},
            headers={"Authorization": f"Token {api_key}"},
            timeout=120,
        )
    except requests.RequestException as e:
        raise PassageError(f"Could not download ESV audio: {e}") from e
    if resp.status_code == 401:
        raise PassageError("The ESV API rejected your key. Check it in Settings.")
    if resp.status_code != 200 or len(resp.content) < 1000:
        raise PassageError(f"ESV audio unavailable for {book} {chapter} "
                           f"(HTTP {resp.status_code}).")
    tmp = out_path + ".part"
    with open(tmp, "wb") as f:
        f.write(resp.content)
    os.replace(tmp, out_path)
    return out_path


# ---------------------------------------------------------------------------
# Public-domain translations (bible-api.com, no key needed)
# ---------------------------------------------------------------------------

# BBE/Darby embed editorial headers like "<A Psalm. Of David.>" or
# "{A Psalm of David.}" in verse text — remove so TTS doesn't read them.
_ANNOTATION = re.compile(r"<[^<>]*>|\{[^{}]*\}")

# ASV/Darby mark translator-supplied words in [brackets], e.g.
# "Commit [thyself] unto Jehovah". The words stay in the spoken/printed
# text; the bracketed fragments are also collected as per-verse notes.
_SUPPLIED = re.compile(r"\[([^\[\]]+)\]")

# Single-chapter books: bible-api.com parses "Jude 1" as Jude *verse* 1 (not
# the whole book), so a plain chapter query silently returns only verse 1. We
# must request an explicit verse range "Jude 1:1-N". N varies slightly by
# translation (e.g. 3 John has 14 or 15 verses), so we try a safe upper bound
# and step down until the range resolves. Values are the largest count seen
# across the public-domain translations.
_SINGLE_CHAPTER_MAX = {
    "Obadiah": 21, "Philemon": 25, "2 John": 13, "3 John": 15, "Jude": 25,
}


def _query_candidates(book: str, chapter: int) -> list:
    """Reference strings to try in order (first that resolves wins)."""
    if chapters_in(book) == 1:
        top = _SINGLE_CHAPTER_MAX.get(book, 40)
        return [f"{book} 1:1-{n}" for n in range(top, max(top - 4, 0), -1)]
    return [f"{book} {chapter}"]


def fetch_public(code: str, book: str, chapter: int) -> Passage:
    api_id = TRANSLATION_IDS.get(code)
    if not api_id:
        raise PassageError(f"Unknown translation: {code}")
    cached = _cache_get(code, book, chapter)
    if cached:
        return cached
    data = None
    for candidate in _query_candidates(book, chapter):
        query = candidate.replace(" ", "+")
        try:
            resp = requests.get(
                BIBLE_API_URL.format(query=query, translation=api_id), timeout=20)
        except requests.RequestException as e:
            raise PassageError(f"Could not reach bible-api.com: {e}") from e
        if resp.status_code == 429:
            raise PassageError("bible-api.com rate limit reached — wait about "
                               "30 seconds and press Play again.")
        if resp.status_code == 404:
            continue  # verse range past the book's end — try a smaller one
        if resp.status_code != 200:
            raise PassageError(f"bible-api.com error (HTTP {resp.status_code}).")
        data = resp.json()
        break
    if data is None:
        raise PassageError(f"{book} {chapter} is not available in "
                           f"{TRANSLATION_LABELS.get(code, code)}.")
    verses = []
    notes = []
    for v in data.get("verses", []):
        raw = _ANNOTATION.sub("", v.get("text", ""))
        verse_notes = [re.sub(r"\s+", " ", m).strip()
                       for m in _SUPPLIED.findall(raw)]
        text = _SUPPLIED.sub(r"\1", raw)  # keep the words, drop the brackets
        text = re.sub(r"\s+", " ", text).strip()
        if text:
            verses.append((v["verse"], text))
            notes.append([n for n in verse_notes if n])
    if not verses:
        raise PassageError(f"No verses returned for {book} {chapter}.")
    passage = Passage(
        book=book,
        chapter=chapter,
        canonical=f"{book} {chapter}",
        translation=code,
        verses=verses,
        notes=notes,
    )
    _cache_put(passage)
    return passage


# ---------------------------------------------------------------------------
# Local (bundled) translations
# ---------------------------------------------------------------------------

def _local_path(code: str, book: str, chapter: int) -> str:
    safe_book = book.replace(" ", "_")
    return os.path.join(BIBLES_DIR, code, f"{safe_book}_{chapter}.json")


def load_local(code: str, book: str, chapter: int) -> Passage:
    """Load a chapter from a bundled translation under bibles/<CODE>/.

    These files ship with the app (produced by import_translation.py) and use
    the same on-disk shape as the passage cache, so they deserialize straight
    into a Passage. No network needed — this is the offline path.
    """
    path = _local_path(code, book, chapter)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except OSError as e:
        raise PassageError(
            f"{book} {chapter} is not available in "
            f"{TRANSLATION_LABELS.get(code, code)}.") from e
    except ValueError as e:
        raise PassageError(
            f"The local file for {book} {chapter} "
            f"({TRANSLATION_LABELS.get(code, code)}) is corrupt.") from e
    return Passage(**data)


def fetch_passage(api_key: str, book: str, chapter: int,
                  translation: str = "WEB") -> Passage:
    """Fetch the requested translation.

    Routing: a bundled local copy under bibles/<CODE>/ wins for ANY
    translation when present (offline, no rate limit) — this is how the
    public-domain API translations become permanent local copies once
    prefetched. Translations declared "local" have no API fallback. ESV
    needs the user's free key (currently not offered in the UI, falls back
    to WEB); everything else comes from bible-api.com.
    """
    if os.path.exists(_local_path(translation, book, chapter)):
        return load_local(translation, book, chapter)
    if TRANSLATION_SOURCES.get(translation) == "local":
        return load_local(translation, book, chapter)  # raises friendly error
    if translation == "ESV":
        if api_key.strip():
            return fetch_esv(api_key.strip(), book, chapter)
        return fetch_public("WEB", book, chapter)
    return fetch_public(translation, book, chapter)


_last_fetch = 0.0


def polite_throttle(min_interval: float = 0.4) -> None:
    """Tiny courtesy delay between API hits when batch-fetching."""
    global _last_fetch
    now = time.time()
    wait = _last_fetch + min_interval - now
    if wait > 0:
        time.sleep(wait)
    _last_fetch = time.time()
