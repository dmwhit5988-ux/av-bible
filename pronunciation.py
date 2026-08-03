"""Pronunciation helper for the neural TTS.

The Edge neural voices (and the SAPI fallback) mispronounce many biblical
proper nouns. edge-tts XML-escapes all input, so SSML <phoneme> tags are read
literally and can't be used; the reliable, engine-agnostic fix is to respell
the name phonetically in the *text sent to the voice* while leaving the on-screen
text untouched.

The master list lives in ``pronunciations.json`` -- a dict keyed by the exact
spelling as it appears in scripture, each entry
``{say, ipa?, ref, override, status?, score?}``:

    say       the pronunciation, both shown to humans and (lowercased) fed to the
              voice when ``override`` is true. Tune this by ear -- whatever sounds
              right when spoken is what to store (e.g. "muh-HAL-uh-lel",
              "sheelah", "kaldeez").
    ipa       optional formal reference pronunciation.
    ref       first place it appears (Book chapter:verse), for ordering.
    override  true = respell it before synthesis; false = speak it as spelled.
    status    what checking the audio concluded -- see below. Absent means the
              name has never been checked.
    score     the agreement measured when it was last checked, 0-1.

``override`` and ``status`` answer different questions, which is why both exist.
``override`` is machinery: it alone decides whether ``respell`` substitutes.
``status`` is a record of what was found, so that "the voice already says this
correctly" is distinguishable from "nobody has ever listened" -- both of which
would otherwise look identical as ``override: false``:

    ok         checked; the plain spelling is read correctly, no override needed
    fixed      checked; an override is in place and produces the right sound
    suggested  checked; a better spelling is known but was not applied, because
               the plain reading was close enough that the disagreement may be
               the transcriber's error rather than the voice's -- decide by ear
    unfixed    checked; the plain spelling is wrong and no respelling has worked
    unsure     checked, but only against a GENERATED reference (ipa_src), so a
               disagreement may equally be the reference's fault. Measured, the
               generator agrees with curated references 0.72 of the time while
               the voice itself manages 0.77 -- it is the weaker of the two, so
               it cannot convict the voice. Needs an ear, not another sweep.

``respell(text)`` swaps every whole-word occurrence of an ``override`` name for a
lowercased ``say``. It's called from ``tts_engine.synthesize`` so desktop
playback and the pre-rendered web showcase audio both benefit.

Edit the list with the GUI (``python pronunciation_tool.py``) -- it plays each
name back in the real voice and writes both this module's JSON and the readable
``PRONUNCIATIONS.md``. ``python pronunciation.py`` just rebuilds the markdown.
"""

import json
import os
import re

import books

_HERE = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(_HERE, "pronunciations.json")
MD_PATH = os.path.join(_HERE, "PRONUNCIATIONS.md")

README = (
    "Master pronunciation list for Bible proper nouns, used to help the neural "
    "TTS. 'say' is tuned by ear -- whatever sounds right spoken is stored, and "
    "(lowercased) is what the voice is fed when 'override' is true; on-screen "
    "text is never changed. 'ipa' is an optional formal reference. Keys are the "
    "exact spelling as it appears in the World English Bible (WEB); add "
    "translation-specific spellings (e.g. KJV 'Mahalaleel') as extra keys. "
    "'status' records what checking the audio concluded -- ok (reads correctly "
    "as spelled), fixed (override in place and working), suggested (a better "
    "spelling is known but unapplied, decide by ear), unfixed (wrong, nothing "
    "found yet); absent means never checked, which is NOT the same as ok. "
    "'score' is the agreement measured at that check, 0-1. Edit with the GUI: "
    "python pronunciation_tool.py (it plays names back and rewrites this file + "
    "PRONUNCIATIONS.md); check against real audio with python "
    "pronunciation_check.py."
)

# Verification verdicts. The empty string is "never checked" and is stored by
# omitting the key entirely, so the file stays clean for untouched entries.
STATUS_UNCHECKED = ""
STATUS_OK = "ok"
STATUS_FIXED = "fixed"
STATUS_SUGGESTED = "suggested"
STATUS_UNFIXED = "unfixed"
STATUS_UNSURE = "unsure"

STATUS_ORDER = (STATUS_UNCHECKED, STATUS_OK, STATUS_FIXED, STATUS_SUGGESTED,
                STATUS_UNFIXED, STATUS_UNSURE)
STATUS_LABELS = {
    STATUS_UNCHECKED: "unchecked",
    STATUS_OK: "fine as spelled",
    STATUS_FIXED: "overridden",
    STATUS_SUGGESTED: "suggestion waiting",
    STATUS_UNFIXED: "still wrong",
    STATUS_UNSURE: "unsure (guessed IPA)",
}


def status_of(info: dict) -> str:
    """The verdict for one entry, falling back for entries predating the field.

    An override with no recorded status must have been tuned by hand at some
    point, so it reads as ``fixed`` rather than as unchecked.
    """
    info = info or {}
    s = info.get("status", "")
    if s in STATUS_LABELS:
        return s
    return STATUS_FIXED if info.get("override") else STATUS_UNCHECKED


def set_status(info: dict, status: str, score=None) -> dict:
    """Record a verdict on ``info`` in place; ``STATUS_UNCHECKED`` clears it."""
    if status == STATUS_UNCHECKED:
        info.pop("status", None)
        info.pop("score", None)
    else:
        info["status"] = status
        if score is None:
            info.pop("score", None)
        else:
            info["score"] = round(float(score), 3)
    return info

_names = None          # dict: name -> {say, ipa?, ref, override}
_pattern = None        # compiled regex over the override names, or None
_table = None          # dict: matched name -> lowercased spoken form
_mtime = None          # last-seen mtime of JSON_PATH, for auto-reload


def _current_mtime():
    try:
        return os.path.getmtime(JSON_PATH)
    except OSError:
        return None


def load(force: bool = False) -> dict:
    """Load and cache the master list. Missing/broken file -> empty (no-op).

    Auto-reloads when pronunciations.json changes on disk (its mtime moves), so
    a long-running process -- e.g. the desktop app playing audio -- picks up
    edits made by the separate Pronunciation Studio without a restart. This is
    what lets a changed pronunciation actually re-render: respell() then yields
    new text, whose hash misses the audio cache.
    """
    global _names, _pattern, _table, _mtime
    mtime = _current_mtime()
    if _names is not None and not force and mtime == _mtime:
        return _names
    _mtime = mtime
    try:
        with open(JSON_PATH, encoding="utf-8") as f:
            _names = json.load(f).get("names", {})
    except (OSError, ValueError):
        _names = {}
    _table = {
        name: info["say"].lower()
        for name, info in _names.items()
        if info.get("override") and info.get("say")
    }
    if _table:
        # Longest names first so a name that contains another matches whole.
        # Lookarounds instead of \b so a key may end in a non-word character
        # (e.g. "fathers’" -- \b after the apostrophe would never match).
        keys = sorted(_table, key=len, reverse=True)
        _pattern = re.compile(
            r"(?<!\w)(" + "|".join(re.escape(k) for k in keys) + r")(?!\w)"
        )
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
    pattern, table = _pattern, _table  # snapshot: load() may reload on a thread
    if not pattern:
        return text
    # .get fallback: if a mid-reload leaves pattern/table momentarily out of
    # step, leave the word unchanged rather than raising (self-corrects next call).
    return pattern.sub(lambda m: table.get(m.group(0), m.group(0)), text)


# --------------------------------------------------------------------------
# Saving (used by the GUI editor)
# --------------------------------------------------------------------------

_BOOK_INDEX = {name: i for i, name in enumerate(books.BOOK_NAMES)}


def _ref_key(ref: str):
    """Canonical sort key: book order, then chapter, verse. Unknown -> last."""
    m = re.match(r"^(.*?)\s+(\d+):(\d+)", ref or "")
    if not m:
        return (999, 999, 999)
    return (_BOOK_INDEX.get(m.group(1), 998), int(m.group(2)), int(m.group(3)))


_KEY_ORDER = ("say", "ipa", "ref", "override", "status", "score")


def _tidy(info: dict) -> dict:
    """One entry with keys in a stable order and empty verdicts omitted."""
    out = {k: info[k] for k in _KEY_ORDER if k in info and info[k] not in ("", None)}
    out.setdefault("override", bool(info.get("override")))
    for k, v in info.items():          # keep anything unrecognised rather than drop it
        out.setdefault(k, v)
    return out


def _sorted_names(names: dict) -> dict:
    ordered = sorted(names.items(), key=lambda kv: (_ref_key(kv[1].get("ref", "")), kv[0]))
    return {k: _tidy(v) for k, v in ordered}


def save_names(names: dict) -> None:
    """Write ``names`` to pronunciations.json (canonically ordered) + rebuild MD."""
    data = {"_readme": README, "names": _sorted_names(names)}
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    load(force=True)
    write_markdown(names)


def write_markdown(names: dict = None) -> str:
    """Regenerate PRONUNCIATIONS.md. Returns the path written."""
    if names is None:
        names = load(force=True)
    rows = sorted(names.items(), key=lambda kv: (_ref_key(kv[1].get("ref", "")), kv[0]))
    lines = [
        "# Bible proper-noun pronunciation guide",
        "",
        "Master list used to help the neural text-to-speech read scripture names",
        "correctly. Generated from `pronunciations.json` -- edit with the GUI",
        "(`python pronunciation_tool.py`) or the JSON, then rebuild with",
        "`python pronunciation.py`. Do not hand-edit this file.",
        "",
        "- **Say it** — the pronunciation fed to the voice (tuned by ear).",
        "- **TTS** — ✅ means the audio pipeline substitutes this spelling before",
        "  synthesis; blank means the name is spoken exactly as spelled.",
        "- **Checked** — what listening to the real audio concluded. Blank means",
        "  nobody has checked it yet, which is not the same as it being right.",
        "",
        "| Name | Say it | IPA | First appears | TTS | Checked |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for name, info in rows:
        tts = "✅" if info.get("override") else ""
        st = status_of(info)
        checked = STATUS_LABELS[st] if st else ""
        if info.get("score") is not None and st:
            checked += f" ({info['score']:.2f})"
        lines.append(
            f"| {name} | {info.get('say', '')} | {info.get('ipa', '')} "
            f"| {info.get('ref', '')} | {tts} | {checked} |"
        )
    lines.append("")
    counts = {}
    for _, i in rows:
        counts[status_of(i)] = counts.get(status_of(i), 0) + 1
    lines.append("**Checked:** " + ", ".join(
        f"{counts.get(s, 0)} {STATUS_LABELS[s]}" for s in STATUS_ORDER) + ".")
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


# --------------------------------------------------------------------------
# Proper-noun detection (used by the GUI editor)
# --------------------------------------------------------------------------

_TOKEN_RE = re.compile(r"[A-Z][A-Za-z’'\-]*")
_SENT_END = set(".!?:;")
# Chars that, immediately before a word, mark it as starting a clause (so a
# capital there is ambiguous, not automatically a proper noun).
_CLAUSE_START = set("“”‘’\"'([—–")

# Common capitalized words that are not names needing pronunciation help.
_STOPWORDS = {
    "The", "A", "An", "And", "But", "Or", "Nor", "So", "Then", "Now", "Thus",
    "Therefore", "For", "Yet", "As", "At", "By", "In", "Into", "Of", "On",
    "Onto", "Out", "Over", "To", "Unto", "Up", "Upon", "With", "Without",
    "Within", "From", "Before", "After", "When", "While", "Where", "Whom",
    "Who", "Whose", "Which", "What", "Why", "How", "If", "Because", "Behold",
    "Come", "Let", "Lo", "See", "Go", "Make", "This", "That", "These", "Those",
    "There", "Here", "He", "She", "It", "They", "We", "You", "I", "His", "Her",
    "Their", "Its", "Our", "Your", "My", "Him", "Them", "Us", "Also", "All",
    "Every", "Each", "No", "Not", "One", "Two", "Truly", "Indeed", "Surely",
    "O", "Oh", "God", "Lord", "GOD", "LORD", "Amen", "Selah", "Yes",
}


def _normalize(tok: str) -> str:
    """Strip a trailing possessive and stray hyphens from a captured token."""
    for suf in ("’s", "'s", "’", "'"):
        if tok.endswith(suf):
            tok = tok[: -len(suf)]
            break
    return tok.strip("-")


def _is_clause_start(text: str, idx: int) -> bool:
    j = idx - 1
    while j >= 0 and text[j] in " \t\n\r":
        j -= 1
    if j < 0:
        return True
    return text[j] in _SENT_END or text[j] in _CLAUSE_START


def scan_proper_nouns(verses, known=None):
    """Detect likely proper nouns in ``verses`` (list of ``(num, text)``).

    Returns ``[(name, [verse_nums]), ...]`` in order of first appearance. A
    capital word mid-sentence is almost always a proper noun; one that starts a
    clause counts only if it's a known name or also appears mid-sentence.
    """
    known = set(known or ())
    midsentence = set()
    for _, text in verses:
        for m in _TOKEN_RE.finditer(text):
            norm = _normalize(m.group(0))
            if norm and norm != "I" and not _is_clause_start(text, m.start()):
                midsentence.add(norm)

    order, occ = [], {}
    for num, text in verses:
        for m in _TOKEN_RE.finditer(text):
            norm = _normalize(m.group(0))
            if not norm or norm == "I" or norm in _STOPWORDS:
                continue
            is_name = (
                norm in known
                or norm in midsentence
                or not _is_clause_start(text, m.start())
            )
            if not is_name:
                continue
            if norm not in occ:
                occ[norm] = []
                order.append(norm)
            if not occ[norm] or occ[norm][-1] != num:
                occ[norm].append(num)
    return [(n, occ[n]) for n in order]


if __name__ == "__main__":
    path = write_markdown()
    print(f"Wrote {path} ({len(load())} names)")
