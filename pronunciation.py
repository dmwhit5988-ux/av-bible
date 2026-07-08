"""Pronunciation helper for the neural TTS.

The Edge neural voices (and the SAPI fallback) mispronounce many biblical
proper nouns -- obscure genealogy names especially (Mahalalel, Arpachshad,
Reu...). edge-tts XML-escapes all input, so SSML <phoneme> tags are read
literally and can't be used. The reliable, engine-agnostic fix is to respell
the name phonetically in the *text sent to the voice* while leaving the text
shown on screen untouched.

The master list of names + pronunciations lives in ``pronunciations.json``.
``respell(text)`` swaps every whole-word occurrence of an ``override`` name for
a lowercased form of its ``say`` respelling. It is called from
``tts_engine.synthesize`` so both the desktop live playback and the pre-render
of the web showcase MP3s benefit.

Run ``python pronunciation.py`` to (re)generate ``PRONUNCIATIONS.md`` -- a
readable table built from the JSON so the two never drift.
"""

import json
import os
import re

_HERE = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(_HERE, "pronunciations.json")
MD_PATH = os.path.join(_HERE, "PRONUNCIATIONS.md")

_names = None          # dict: name -> {say, ipa, ref, override}
_pattern = None        # compiled regex over the override names, or None
_table = None          # dict: matched name -> lowercased respelling


def load(force: bool = False) -> dict:
    """Load and cache the master list. Missing/broken file -> empty (no-op)."""
    global _names, _pattern, _table
    if _names is not None and not force:
        return _names
    try:
        with open(JSON_PATH, encoding="utf-8") as f:
            _names = json.load(f).get("names", {})
    except (OSError, ValueError):
        _names = {}
    # What we feed the voice: the explicit `tts` spelling if given, else a
    # lowercased `say`. `tts` exists because the human-readable respelling
    # (hyphenated, stressed) is sometimes read letter-by-letter by the engine;
    # a single made-up word is spoken more reliably.
    _table = {
        name: (info.get("tts") or info.get("say", "")).lower()
        for name, info in _names.items()
        if info.get("override") and (info.get("tts") or info.get("say"))
    }
    if _table:
        # Longest names first so a name that contains another matches whole.
        keys = sorted(_table, key=len, reverse=True)
        _pattern = re.compile(r"\b(" + "|".join(re.escape(k) for k in keys) + r")\b")
    else:
        _pattern = None
    return _names


def respell(text: str) -> str:
    """Return ``text`` with override proper nouns swapped for phonetic spellings.

    Whole-word, case-sensitive (names are capitalized in scripture, so common
    lowercase words are never touched; ``\\bHam\\b`` won't hit "Hamath", etc.).
    A trailing possessive like "Methuselah's" still matches the bare name.
    """
    load()
    if not _pattern:
        return text
    return _pattern.sub(lambda m: _table[m.group(0)], text)


def _ref_sort_key(ref: str):
    """Sort by book order (as first seen), then chapter, then verse."""
    m = re.match(r"^(.*?)\s+(\d+):(\d+)", ref or "")
    if not m:
        return (ref or "", 0, 0)
    return (m.group(1), int(m.group(2)), int(m.group(3)))


def write_markdown() -> str:
    """Regenerate PRONUNCIATIONS.md from the JSON. Returns the path written."""
    names = load(force=True)
    rows = sorted(names.items(), key=lambda kv: _ref_sort_key(kv[1].get("ref", "")))
    lines = [
        "# Bible proper-noun pronunciation guide",
        "",
        "Master list used to help the neural text-to-speech read scripture names",
        "correctly. Generated from `pronunciations.json` -- **edit the JSON, then run",
        "`python pronunciation.py` to rebuild this file** (do not hand-edit here).",
        "",
        "- **Say** — phonetic respelling; CAPITALS mark the stressed syllable.",
        "- **TTS** — ✅ means the audio pipeline substitutes this spelling before",
        "  synthesis; blank means the voice already says it correctly (reference only).",
        "",
        "| Name | Say it | IPA | First appears | TTS |",
        "| --- | --- | --- | --- | --- |",
    ]
    for name, info in rows:
        tts = "✅" if info.get("override") else ""
        lines.append(
            f"| {name} | {info.get('say', '')} | {info.get('ipa', '')} "
            f"| {info.get('ref', '')} | {tts} |"
        )
    lines.append("")
    n_over = sum(1 for _, i in rows if i.get("override"))
    lines.append(
        f"_{len(rows)} names — {n_over} respelled for the voice, "
        f"{len(rows) - n_over} reference-only._"
    )
    lines.append("")
    with open(MD_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return MD_PATH


if __name__ == "__main__":
    path = write_markdown()
    n = len(load())
    print(f"Wrote {path} ({n} names)")
