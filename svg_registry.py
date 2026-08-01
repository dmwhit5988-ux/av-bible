"""Registry of generator-owned SVG families (SVG_STUDIO_DESIGN.md section 4).

Every SVG the project ships today is produced by a generate_*_svg.py module;
re-running a generator rewrites its family's files from the Python spec,
silently discarding hand edits. The studio uses this registry to detect
"this verse's file is generator-owned" and route edits to the spec
(durable) rather than the XML (clobbered on regen) — detect and route,
never block.

Data lives in svg_generators.json so adding a family is a data edit, not a
code change. Matching is by (book, chapter), optionally narrowed by verse: a
family may carry a "verses": [lo, hi] range, which is how Genesis 11 is split
between Babel (1-9) and the Shem-to-Abram genealogy (10-32). Callers that know
the verse should pass it; ``owner_of`` without one falls back to the first
family listed for the chapter, which is ambiguous only for a split chapter.
"""

import json
import os
from dataclasses import dataclass

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
REGISTRY_PATH = os.path.join(REPO_ROOT, "svg_generators.json")


@dataclass(frozen=True)
class SpecPointer:
    file: str       # repo-relative path of the spec module to edit
    edit: str       # human-readable pointer to what inside it to edit


@dataclass(frozen=True)
class FamilyInfo:
    label: str
    book: str
    chapters: tuple
    generator: str  # repo-relative path of the generate_*_svg.py module
    spec: tuple     # tuple[SpecPointer]
    translation_suffixed: bool
    kind: str | None = None  # visual classification for the manifest
                             # (genealogy / map / diagram / ...)
    verses: tuple | None = None  # (lo, hi) when the family owns only part of
                                 # its chapter; None means the whole chapter

    def covers(self, verse: int | None) -> bool:
        """Whether this family owns `verse` of a chapter it already matches.
        An unranged family covers everything; a ranged one covers its range,
        and covers an unknown (None) verse so a verse-less lookup still
        resolves to something."""
        if self.verses is None or verse is None:
            return True
        return self.verses[0] <= verse <= self.verses[1]


def _load_families():
    with open(REGISTRY_PATH, encoding="utf-8") as f:
        data = json.load(f)
    families = []
    for fam in data["families"]:
        families.append(FamilyInfo(
            label=fam["label"],
            book=fam["book"],
            chapters=tuple(fam["chapters"]),
            generator=fam["generator"],
            spec=tuple(SpecPointer(p["file"], p["edit"]) for p in fam["spec"]),
            translation_suffixed=bool(fam.get("translation_suffixed")),
            kind=fam.get("kind"),
            verses=(tuple(fam["verses"]) if fam.get("verses") else None),
        ))
    return families


_families_cache = None


def families(force=False):
    global _families_cache
    if _families_cache is None or force:
        _families_cache = _load_families()
    return _families_cache


def owner_of(book: str, chapter: int,
             verse: int | None = None) -> FamilyInfo | None:
    """The family that generates this verse's SVG, or None if it is open for
    direct hand-authoring.

    Pass `verse` whenever it is known: a chapter can be split between two
    families (Genesis 11), and without the verse the first one listed wins.
    """
    for fam in families():
        if fam.book == book and chapter in fam.chapters and fam.covers(verse):
            return fam
    return None
