"""The Bible text: the World English Bible, bundled as one JSON per chapter.

WEB is the only translation Theoria reads. Chapters live under
bibles/WEB/<Book>_<chapter>.json, written by import_translation.py from the
eBible USFX source. Nothing here touches the network.

The JSON files also carry "translation" and "notes" fields (kept so the
re-importer round-trips byte-identically); the loader ignores them.
"""

import json
import os
from dataclasses import dataclass, field
from functools import lru_cache

from config import BIBLES_DIR

TRANSLATION = "WEB"
ATTRIBUTION = "World English Bible — public domain."


class PassageError(Exception):
    """User-presentable load failure."""


@dataclass
class Passage:
    book: str
    chapter: int
    canonical: str                              # e.g. "John 3"
    verses: list = field(default_factory=list)  # [(verse_number, text), ...]


def chapter_path(book: str, chapter: int) -> str:
    safe_book = book.replace(" ", "_")
    return os.path.join(BIBLES_DIR, TRANSLATION, f"{safe_book}_{chapter}.json")


def load_chapter(book: str, chapter: int) -> Passage:
    """Load one chapter of the bundled WEB text.

    Keys are picked explicitly rather than splatted into Passage, because the
    files carry fields (translation, notes) the dataclass no longer has.
    """
    path = chapter_path(book, chapter)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except OSError as e:
        raise PassageError(
            f"{book} {chapter} is not in the bundled World English Bible.") from e
    except ValueError as e:
        raise PassageError(
            f"The text file for {book} {chapter} is corrupt.") from e
    return Passage(book=data["book"], chapter=data["chapter"],
                   canonical=data["canonical"], verses=data["verses"])


@lru_cache(maxsize=None)
def verse_numbers(book: str, chapter: int) -> tuple:
    """WEB's verse numbers for a chapter, in order: the single source of
    versification for every generator (WEB's Romans 14 has 26 verses, its
    Romans 16 has 24, and it has no Acts 15:34)."""
    return tuple(int(num) for num, _ in load_chapter(book, chapter).verses)
