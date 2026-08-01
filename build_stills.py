#!/usr/bin/env python3
"""Generate reduced-motion still twins for every animated verse SVG.

For each visuals/**/<name>.svg containing SMIL animation, writes a sibling
<name>.still.svg — the finished frame as a plain static document
(svg_freeze.freeze_still). build_manifest.py attaches these to their base
file's manifest record as "still", and the web app swaps them in for
visitors with prefers-reduced-motion set.

Incremental: a still newer than its base SVG is left alone (pass
force=True / --force to rebuild everything). Stills whose base SVG is gone,
or whose base is no longer animated, are deleted — stills are derived
output, never authored.

Run before build_manifest.py so the manifest sees the fresh stills.

    python build_stills.py [--force]
"""

import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

from svg_freeze import freeze_still, svg_is_animated

VISUALS_DIR = Path(__file__).resolve().parent / "visuals"
STILL_TAIL = ".still.svg"


@dataclass
class StillStats:
    written: int = 0
    skipped: int = 0    # up to date
    removed: int = 0    # orphaned / base no longer animated
    static: int = 0     # base SVGs with no animation (no still needed)
    warnings: list = field(default_factory=list)  # (rel_path, message)

    def summary(self) -> str:
        return (f"{self.written} still(s) written, {self.skipped} up to "
                f"date, {self.removed} removed, {self.static} static "
                f"SVG(s) need none"
                + (f", {len(self.warnings)} warning(s)" if self.warnings
                   else ""))


def still_path_for(svg_path: Path) -> Path:
    return svg_path.with_name(svg_path.stem + STILL_TAIL)


def build_stills(force: bool = False,
                 on_progress=None) -> StillStats:
    """Walk visuals/ and (re)build still twins. on_progress, if given, is
    called with a short line per file written/removed (for GUI log panes)."""
    stats = StillStats()

    def note(line):
        if on_progress:
            on_progress(line)

    for svg_path in sorted(VISUALS_DIR.rglob("*.svg")):
        if svg_path.name.endswith(STILL_TAIL):
            continue
        rel = svg_path.relative_to(VISUALS_DIR).as_posix()
        try:
            text = svg_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as e:
            stats.warnings.append((rel, f"unreadable: {e}"))
            continue
        still = still_path_for(svg_path)

        if not svg_is_animated(text):
            stats.static += 1
            if still.exists():  # base was animated once; not anymore
                still.unlink()
                stats.removed += 1
                note(f"removed {still.name} (base is static now)")
            continue

        if (not force and still.exists()
                and still.stat().st_mtime >= svg_path.stat().st_mtime):
            stats.skipped += 1
            continue

        try:
            result = freeze_still(text)
        except Exception as e:  # malformed XML etc. — skip, don't abort run
            stats.warnings.append((rel, f"freeze failed: {e}"))
            continue
        for w in result.warnings:
            stats.warnings.append((rel, w))
        still.write_text(result.svg_text, encoding="utf-8")
        stats.written += 1
        note(f"wrote {still.relative_to(VISUALS_DIR).as_posix()}")

    # Orphans: stills whose base SVG no longer exists.
    for still in sorted(VISUALS_DIR.rglob(f"*{STILL_TAIL}")):
        base = still.with_name(
            still.name[: -len(STILL_TAIL)] + ".svg")
        if not base.exists():
            still.unlink()
            stats.removed += 1
            note(f"removed orphan {still.name}")

    return stats


if __name__ == "__main__":
    stats = build_stills(force="--force" in sys.argv[1:], on_progress=None)
    print(f"[OK] {stats.summary()}")
    for rel, msg in stats.warnings:
        print(f"  [WARN] {rel}: {msg}")
