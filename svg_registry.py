"""Registry of generator-owned SVG families (SVG_STUDIO_DESIGN.md section 4).

Every SVG the project ships today is produced by a generate_*_svg.py module;
re-running a generator rewrites its family's files from the Python spec,
silently discarding hand edits. The studio uses this registry to detect
"this verse's file is generator-owned" and route edits to the spec
(durable) rather than the XML (clobbered on regen) — detect and route,
never block.

Data lives in svg_generators.json so adding a family is a data edit, not a
code change. Matching is by (book, chapter); no family owns a partial
chapter today. If that ever changes, add an optional "verses": [lo, hi]
field to the JSON entry — owner_of already returns the first match.
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
        ))
    return families


_families_cache = None


def families(force=False):
    global _families_cache
    if _families_cache is None or force:
        _families_cache = _load_families()
    return _families_cache


def owner_of(book: str, chapter: int) -> FamilyInfo | None:
    """The family that generates this chapter's SVGs, or None if the
    chapter is open for direct hand-authoring."""
    for fam in families():
        if fam.book == book and chapter in fam.chapters:
            return fam
    return None
