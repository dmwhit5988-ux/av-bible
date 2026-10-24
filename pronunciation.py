"""Pronunciation helper for the neural TTS.

The Edge neural voices (and the SAPI fallback) mispronounce many biblical
proper nouns. edge-tts XML-escapes all input, so SSML <phoneme> tags are read
literally and can't be used; the reliable, engine-agnostic fix is to respell
the name phonetically in the *text sent to the voice* while leaving the on-screen
text untouched. The same voice on Azure (azure_tts.py) does take SSML, so a name
can instead be spoken from its IPA there (``use_ipa``, ``ssml()``).

The master list lives in ``pronunciations.json`` as ``{_readme, names, verses}``.
``names`` is keyed by a name's exact spelling in the World English Bible (the
only text the app reads), each entry
``{say, ipa?, ipa_src?, ref, override, use_ipa?, status?, score?}``:

    say       the pronunciation, both shown to humans and (lowercased) fed to the
              voice when ``override`` is true. Tune this by ear -- whatever sounds
              right when spoken is what to store (e.g. "muh-HAL-uh-lel",
              "sheelah", "kaldeez").
    ipa       optional formal reference pronunciation.
    ipa_src   where ``ipa`` came from (isbe, cmudict, wiktionary, wikipedia,
              or generated), when that is recorded.
    ref       first place it appears (Book chapter:verse), for ordering.
    override  true = respell it before synthesis; false = speak it as spelled.
    use_ipa   true = on Azure, speak it from ``ipa`` (see azure_ipa), which wins
              over ``override`` there; Edge still respells or reads it plain.
              Absent means false.
    status    what checking the audio concluded -- see below. Absent means the
              name has never been checked.
    score     the agreement measured when it was last checked, 0-1.

``override`` and ``status`` answer different questions, which is why both exist.
``override`` is machinery: it alone decides whether ``respell`` substitutes.
``status`` is a record of what was found, so that "the voice already says this
correctly" is distinguishable from "nobody has ever listened" -- both of which
would otherwise look identical as ``override: false``:

    ok         checked; the plain spelling is read correctly, no override needed
    fixed      checked; an override (or, on Azure, the IPA) is in place and
               produces the right sound
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
lowercased ``say``. It's called from ``tts_engine.synthesize``, so every
narration benefits: the Studio's playback, the web app's pre-rendered MP3s and
Video Studio's renders. ``ssml(text)`` is its Azure counterpart: the same
respellings, plus a ``<phoneme>`` tag for every ``use_ipa`` name.

``verses`` is for a word that one verse needs said differently -- a heteronym
such as "Separate Barnabas" (the verb) in Acts 13:2, where respelling every
"separate" would break the adjective elsewhere. It is keyed by reference
("Acts 13:2"), each holding ``{words: say}``: ``words`` is the exact text of
the verse to replace, whole-word and case-sensitive, and ``say`` is spoken in
its place, as typed. ``for_verse(ref, text)`` applies them before ``respell``
or ``ssml``, so a name inside ``say`` is still respelled; ``tts_engine.route``
calls it when it is given the verse's ``ref``.

Edit the list with the GUI (``python pronunciation_tool.py``) -- it plays each
name back in the real voice and writes both this module's JSON and the readable
``PRONUNCIATIONS.md`` (a generated report, git-ignored).
``python pronunciation.py`` just rebuilds the markdown.
"""

import json
import os
import re
import sys
import threading
import time
import unicodedata
from typing import NamedTuple

import books

_HERE = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(_HERE, "pronunciations.json")
MD_PATH = os.path.join(_HERE, "PRONUNCIATIONS.md")

README = (
    "Master pronunciation list for Bible proper nouns, used to help the neural "
    "TTS. 'say' is tuned by ear -- whatever sounds right spoken is stored, and "
    "(lowercased) is what the voice is fed when 'override' is true; on-screen "
    "text is never changed. 'ipa' is an optional formal reference. Keys are WEB "
    "spellings: the exact form a name takes in the World English Bible, the only "
    "text the app reads. 'use_ipa' true means Azure renders speak the name from "
    "'ipa' instead (Edge renders still use 'say' or the plain spelling). "
    "'status' records what checking the audio concluded -- ok (reads correctly "
    "as spelled), fixed (override or IPA in place and working), suggested (a better "
    "spelling is known but unapplied, decide by ear), unfixed (wrong, nothing "
    "found yet), unsure (checked only against a generated reference, so it "
    "needs an ear); absent means never checked, which is NOT the same as ok. "
    "'score' is the agreement measured at that check, 0-1. 'verses' holds "
    "words that one verse needs said differently (a heteronym like 'Separate' "
    "the verb in Acts 13:2): {\"Book c:v\": {exact words in the verse: what "
    "to say, as typed}}. Edit with the GUI: "
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

    An override (or IPA in use) with no recorded status must have been set by
    hand at some point, so it reads as ``fixed`` rather than as unchecked.
    """
    info = info or {}
    s = info.get("status")
    if s and s in STATUS_LABELS:       # "" is a label too: absent must fall through
        return s
    return (STATUS_FIXED if info.get("override") or info.get("use_ipa")
            else STATUS_UNCHECKED)


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
_verses = {}           # dict: "Book c:v" -> {words in that verse: what to say}
# The Azure side, swapped in as one tuple so a reader never sees half a reload:
# (regex over override + use_ipa names with an optional possessive, or None;
#  {use_ipa name: its ipa}; {use_ipa name: why its ipa can't be sent}).
_ssml_state = (None, {}, {})
_mtime = None          # last-seen mtime of JSON_PATH, for auto-reload


def _current_mtime():
    try:
        return os.path.getmtime(JSON_PATH)
    except OSError:
        return None


def load(force: bool = False) -> dict:
    """Load and cache the master list. Missing/broken file -> empty (no-op).

    Auto-reloads when pronunciations.json changes on disk (its mtime moves), so
    a long-running process -- e.g. the Studio playing a passage -- picks up
    edits made by the separate Pronunciation Studio without a restart. This is
    what lets a changed pronunciation actually re-render: respell() then yields
    new text, whose hash misses the audio cache.
    """
    global _names, _pattern, _table, _ssml_state, _mtime, _verses
    mtime = _current_mtime()
    if _names is not None and not force and mtime == _mtime:
        return _names
    _mtime = mtime
    try:
        with open(JSON_PATH, encoding="utf-8") as f:
            data = json.load(f)
        _names = data.get("names", {})
        verses = data.get("verses", {})
        _verses = verses if isinstance(verses, dict) else {}
    except (OSError, ValueError, AttributeError):
        _names, _verses = {}, {}
    _table = {
        name: info["say"].lower()
        for name, info in _names.items()
        if info.get("override") and info.get("say")
    }
    _pattern = _names_regex(_table)
    ipa, problems = {}, {}
    for name, info in _names.items():
        if not info.get("use_ipa"):
            continue
        try:
            azure_ipa(info.get("ipa", ""))
            ipa[name] = info["ipa"]
        except ValueError as e:
            problems[name] = str(e)
    # The possessive is captured so it can go inside the <phoneme> tag: left
    # outside, Azure reads "Methuselah</phoneme>'s" as "Methuselah ess".
    _ssml_state = (_names_regex({**_table, **ipa}, possessive=True), ipa, problems)
    return _names


def _names_regex(keys, possessive=False):
    """A regex matching any of ``keys`` as a whole word, or None for no keys.

    Longest names first so a name that contains another matches whole.
    Lookarounds instead of \\b so a key may end in a non-word character (e.g.
    "fathers’" -- \\b after the apostrophe would never match).
    """
    if not keys:
        return None
    alts = "|".join(re.escape(k) for k in sorted(keys, key=len, reverse=True))
    tail = r"(['’‘]s)?" if possessive else ""
    return re.compile(r"(?<!\w)(" + alts + r")" + tail + r"(?!\w)")


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


def verse_words(ref: str) -> dict:
    """The words ``ref`` ("Acts 13:2") has said differently: {words: say}."""
    load()
    return dict(_verses.get(ref) or {})


def all_verse_words() -> dict:
    """Every verse's words: {"Book c:v": {words: say}}, a copy."""
    load()
    return {ref: dict(words) for ref, words in _verses.items()}


def apply_words(text: str, words: dict) -> str:
    """``text`` with each of ``words`` (whole-word, case-sensitive, longest
    first) replaced by its ``say``, as typed."""
    pattern = _names_regex({w for w, say in words.items() if w and say})
    if not pattern:
        return text
    return pattern.sub(lambda m: words[m.group(0)], text)


def for_verse(ref: str, text: str) -> str:
    """``text``, the verse ``ref``, with that verse's own words swapped in.
    Run it before ``respell`` or ``ssml``; a verse with none is unchanged."""
    return apply_words(text, verse_words(ref)) if ref else text


# --------------------------------------------------------------------------
# IPA for Azure (the <phoneme> path)
# --------------------------------------------------------------------------
# Azure speaks <phoneme alphabet="ipa" ph="…"> in its en-US phone set only
# (learn.microsoft.com, "SSML phonetic sets"). Two things about it were
# measured against the live service, en-US-AndrewNeural, on 2026-10-18:
#   * a symbol it doesn't know (parentheses, say) fails the whole request with
#     HTTP 400 -- so one bad name would cost a verse;
#   * a stress mark is honoured only when every syllable is separated by ".".
#     Otherwise the syllable *before* the mark takes the stress, so the list's
#     usual /mɪˈθuː.ʃeɪ.ɛl/ would be stressed on "mɪ".
# azure_ipa() therefore rewrites a stored reference into that phone set and
# splits it into syllables itself. The stored ``ipa`` is never changed.

# Azure's en-US phones. Vowels are syllable nuclei; ɚ and ɝ are the r-coloured
# schwa and "er" vowel. Note ASCII g (U+0067) and ɹ (U+0279), as the table has.
AZURE_VOWELS = frozenset(("i", "ɪ", "eɪ", "ɛ", "æ", "ɑ", "ɔ", "ʊ", "oʊ", "u",
                          "ʌ", "aɪ", "aʊ", "ɔɪ", "ə", "ɚ", "ɝ"))
AZURE_CONSONANTS = frozenset(("p", "b", "t", "d", "k", "g", "m", "n", "ŋ", "f",
                              "v", "θ", "ð", "s", "z", "ʃ", "ʒ", "h", "tʃ", "dʒ",
                              "l", "ɹ", "w", "j"))

# What the list's references use, mapped onto that set. The references mix
# British dictionary notation (ɒ, ɜː, ɛə, e, length marks) with American; the
# voice is American, so British vowels take their American values. A value
# ending "+ɹ" is a British centring diphthong, said with an r (ɛər -> ɛɹ, a
# bare ɛə too). One ending "+ɹ|ə" is either that or two vowels: /bɪər/ and
# /nɪə/ are "beer" and "near", but /ˈsæmjʊəl/ is "SAM-yoo-el" -- so it is the
# diphthong only before an r or at the end.
_IPA_UNITS = {
    # diphthongs and affricates, matched before their single letters (so the
    # ɪə inside "aɪə" is never taken for a centring diphthong)
    "aɪ": "aɪ", "aʊ": "aʊ", "eɪ": "eɪ", "oʊ": "oʊ", "ɔɪ": "ɔɪ", "əʊ": "oʊ",
    "ɑɪ": "aɪ", "ɑʊ": "aʊ", "tʃ": "tʃ", "dʒ": "dʒ",
    "ɛə": "ɛ+ɹ", "eə": "ɛ+ɹ", "ɪə": "ɪ+ɹ|ə", "ʊə": "ʊ+ɹ|ə",
    # eSpeak's long e and o, as the Verifier hears "say" and "go"
    "eː": "eɪ", "oː": "oʊ",
    # vowels
    "i": "i", "ɪ": "ɪ", "ɛ": "ɛ", "æ": "æ", "ɑ": "ɑ", "ɔ": "ɔ", "ʊ": "ʊ",
    "u": "u", "ʌ": "ʌ", "ə": "ə", "ɚ": "ɚ", "ɝ": "ɝ",
    "ɒ": "ɑ", "ɜ": "ɝ", "ɐ": "ə", "ɨ": "ɪ", "ᵻ": "ɪ", "ʉ": "u", "ɘ": "ə",
    "ɵ": "oʊ",
    "a": "æ", "e": "ɛ", "o": "oʊ",
    # consonants
    "p": "p", "b": "b", "t": "t", "d": "d", "k": "k", "g": "g", "ɡ": "g",
    "m": "m", "n": "n", "ŋ": "ŋ", "f": "f", "v": "v", "θ": "θ", "ð": "ð",
    "s": "s", "z": "z", "ʃ": "ʃ", "ʒ": "ʒ", "h": "h", "l": "l", "ɫ": "l",
    "r": "ɹ", "ɹ": "ɹ", "ɾ": "d", "w": "w", "ʍ": "w", "j": "j",
    "x": "k", "ħ": "h", "ʔ": "", "ʕ": "",
}
# Letters that NFD would split into a base and a diacritic, mapped first.
_PRECOMPOSED = {"ç": "h"}
_IPA_LONGEST = max(len(k) for k in _IPA_UNITS)
_STRESS = {"ˈ": 2, "ˌ": 1, "'": 2}          # ' is a common stand-in for ˈ
_BREAKS = set(". -‿|")                       # syllable (or word) boundaries
_SKIP = {"[", "]", "(", ")", "ː", "ˑ"}            # an optional (x) is kept
_SYLLABIC = "̩"                         # n̩ -> ən
_YOD_DROPPED = {"t", "d", "n", "s", "z", "θ", "l"}   # tju -> tu, as Americans say it

# Consonant clusters that may begin an English syllable, for splitting a run
# of consonants that has no "." in it (maximal onset).
_ONSETS = {(c,) for c in AZURE_CONSONANTS - {"ŋ"}} | {
    tuple(o) for o in (
        ("s", "p"), ("s", "t"), ("s", "k"), ("s", "m"), ("s", "n"), ("s", "l"),
        ("s", "w"), ("s", "f"),
        ("p", "l"), ("b", "l"), ("k", "l"), ("g", "l"), ("f", "l"),
        ("p", "ɹ"), ("b", "ɹ"), ("t", "ɹ"), ("d", "ɹ"), ("k", "ɹ"), ("g", "ɹ"),
        ("f", "ɹ"), ("θ", "ɹ"), ("ʃ", "ɹ"),
        ("t", "w"), ("d", "w"), ("k", "w"), ("g", "w"), ("θ", "w"),
        ("p", "j"), ("b", "j"), ("k", "j"), ("g", "j"), ("m", "j"), ("f", "j"),
        ("v", "j"), ("h", "j"),
        ("s", "p", "l"), ("s", "p", "ɹ"), ("s", "t", "ɹ"), ("s", "k", "ɹ"),
        ("s", "k", "w"), ("s", "k", "j"), ("s", "p", "j"))}


def _ipa_tokens(ipa: str) -> list:
    """Split a reference into ("V"|"C", phone), ("S", level) and ("B", ".")
    tokens in Azure's phone set. Raises ValueError on a symbol with no
    equivalent."""
    # A reference may hold alternatives ("/ˈæ.rən/, /ˈɛr.ən/", or the
    # Verifier's two readings "a / b"): the first is the one spoken.
    first = [part for part in re.split(r"[/,]", ipa or "") if part.strip()]
    s = first[0].strip() if first else ""
    for letter, phone in _PRECOMPOSED.items():
        s = s.replace(letter, phone)
    s = unicodedata.normalize("NFD", s)
    s = s.replace("\u0361", "").replace("\u035c", "")  # tie bars: d͡ʒ is dʒ
    raw = []                                   # (kind, value) before r-handling
    i = 0
    while i < len(s):
        ch = s[i]
        if ch in _SKIP:
            i += 1
            continue
        if ch in _STRESS:
            raw.append(("S", _STRESS[ch]))
            i += 1
            continue
        if ch in _BREAKS:
            raw.append(("B", "."))
            i += 1
            continue
        if ch == _SYLLABIC:                    # n̩: a schwa before the consonant
            if raw and raw[-1][0] == "C":
                raw.insert(len(raw) - 1, ("V", "ə"))
            i += 1
            continue
        if unicodedata.combining(ch):          # other diacritics carry nothing here
            i += 1
            continue
        for n in range(_IPA_LONGEST, 0, -1):
            unit = s[i:i + n]
            if unit in _IPA_UNITS:
                break
        else:
            raise ValueError(f"“{ch}” has no Azure en-US equivalent")
        i += len(unit)
        mapped = _IPA_UNITS[unit]
        if not mapped:                          # ʔ and friends: dropped
            continue
        if "+" in mapped:
            vowel, tail = mapped.split("+")
            raw.append(("V", vowel))
            raw.append(("R?", tail))            # resolved below, once the next phone is known
        else:
            raw.append(("V" if mapped in AZURE_VOWELS else "C", mapped))

    def next_phone(k):
        for kind, value in raw[k + 1:]:
            if kind in ("V", "C", "R?"):
                return kind, value
        return None, None

    out = []
    for k, (kind, value) in enumerate(raw):
        if kind == "R?":
            nxt = next_phone(k)
            if nxt[1] == "ɹ":
                continue                        # ɛər: the r is written already
            if value == "ɹ|ə" and nxt[0] is not None and not _carries_stress(raw, k - 1):
                out.append(("V", "ə"))          # ʊəl: two vowels, "yoo-el"
            else:
                out.append(("C", "ɹ"))          # nɪə, ɛə: the r the vowel stands for
            continue
        if kind == "C" and value == "ɹ" and out and out[-1] == ("V", "ɝ"):
            # ɜːr -> ɝ: the r is part of the vowel, unless a vowel follows it
            if next_phone(k)[0] != "V":
                continue
        if kind == "C" and value == "ɹ" and out and out[-1] == ("V", "ə"):
            if next_phone(k)[0] != "V":         # ər -> ɚ before a consonant or the end
                out[-1] = ("V", "ɚ")
                continue
        out.append((kind, value))
    return out


def _carries_stress(raw: list, k: int) -> bool:
    """Whether the vowel at ``raw[k]`` is stressed, or the only vowel: then a
    centring vowel there is one syllable even before a consonant (/bɪəd/ is
    "beard"), where an unstressed one is two (/ˈsæmjʊəl/)."""
    vowels = [kind for kind, _ in raw if kind == "V"]
    if len(vowels) == 1:
        return True
    for kind, _ in reversed(raw[:k]):
        if kind == "V":
            return False
        if kind == "S":
            return True
    return False


def _syllables(tokens: list) -> list:
    """Group tokens into [(stress, [phones])] syllables, one per vowel.

    Between two vowels the consonants split at a written "." if there is one;
    otherwise at a stress mark written before a consonant (dictionary style,
    /kəlˈdiːz/); otherwise by maximal onset, which also covers marks written
    just before the vowel (eSpeak style, /tˈaɪdəl/). A mark anywhere between
    two vowels stresses the second.
    """
    nuclei = [k for k, (kind, _) in enumerate(tokens) if kind == "V"]
    if not nuclei:
        raise ValueError("no vowel in it")

    def stress_in(span):
        return max((v for kind, v in span if kind == "S"), default=0)

    sylls = [[stress_in(tokens[:nuclei[0]]),
              [v for kind, v in tokens[:nuclei[0]] if kind == "C"]]]
    for a, b in zip(nuclei, nuclei[1:]):
        sylls[-1][1].append(tokens[a][1])
        gap = tokens[a + 1:b]
        cons = [v for kind, v in gap if kind == "C"]
        split = None
        seen = 0
        for kind, v in gap:                       # a written boundary wins
            if kind == "C":
                seen += 1
            elif kind == "B":
                split = seen
                break
        if split is None:
            seen = 0
            for kind, v in gap:                   # then a mark before a consonant
                if kind == "C":
                    seen += 1
                elif kind == "S" and seen < len(cons):
                    split = seen
                    break
        if split is None:                         # then maximal onset
            split = len(cons)
            while split > 0 and tuple(cons[split - 1:]) in _ONSETS:
                split -= 1
        sylls[-1][1].extend(cons[:split])
        sylls.append([stress_in(gap), cons[split:]])
    sylls[-1][1].append(tokens[nuclei[-1]][1])
    sylls[-1][1].extend(v for kind, v in tokens[nuclei[-1] + 1:] if kind == "C")
    return [(stress, phones) for stress, phones in sylls]


_SIBILANTS = {"s", "z", "ʃ", "ʒ", "tʃ", "dʒ"}
_VOICELESS = {"p", "t", "k", "f", "θ"}


def azure_ipa(ipa: str, possessive: bool = False) -> str:
    """``ipa`` rewritten for Azure: en-US phones, every syllable dotted, each
    stress mark at the start of its syllable. ``possessive`` adds the sound of
    a trailing 's. Raises ValueError (with a reason) when it can't be sent.

    >>> azure_ipa("/mɪˈθuː.ʃeɪ.ɛl/")
    'mɪ.ˈθu.ʃeɪ.ɛl'
    """
    sylls = _syllables(_ipa_tokens(ipa))
    for k, (stress, phones) in enumerate(sylls):
        # American yod-dropping: in a stressed or first syllable, British
        # /kəˈtjʊər.ə/ is "kuh-TOOR-uh" -- and Azure reads a kept tj as "ch".
        # Unstressed it stays ("value"), and so it does across a syllable
        # break: /ˈmæθ.juː/ is still "MATH-yoo".
        if ((stress or k == 0) and len(phones) > 2 and phones[0] in _YOD_DROPPED
                and phones[1] == "j" and phones[2] in ("u", "ʊ")):
            del phones[1]
        if stress and "ɚ" in phones:
            # Azure's table: ɝ is stressed "er" (fur), ɚ unstressed (supper)
            phones[phones.index("ɚ")] = "ɝ"
    if possessive:
        last = sylls[-1][1][-1]
        if last in _SIBILANTS:
            sylls.append((0, ["ɪ", "z"]))
        else:
            sylls[-1][1].append("s" if last in _VOICELESS else "z")
    marks = {0: "", 1: "ˌ", 2: "ˈ"}
    return ".".join(marks[stress] + "".join(phones) for stress, phones in sylls)


def ipa_problem(name: str) -> str:
    """Why a ``use_ipa`` name's IPA can't be sent to Azure, or "" if it can (or
    the name doesn't use IPA). Such a name falls back to its respelling, or to
    the plain spelling when it has none."""
    load()
    return _ssml_state[2].get(name, "")


def ipa_in_use(info: dict) -> bool:
    """Whether Azure renders really speak this entry from its IPA: ``use_ipa``
    is on and the IPA can be sent."""
    if not (info or {}).get("use_ipa"):
        return False
    try:
        azure_ipa(info.get("ipa", ""))
        return True
    except ValueError:
        return False


def xml_escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def phoneme(word: str, ipa: str, possessive: bool = False) -> str:
    """One ``<phoneme>`` element speaking ``word`` (shown text) as ``ipa``.
    Raises ValueError if the IPA can't be sent."""
    return (f'<phoneme alphabet="ipa" ph="{azure_ipa(ipa, possessive)}">'
            f"{xml_escape(word)}</phoneme>")


def uses_ipa(text: str) -> bool:
    """True if ``text`` names anyone whose ``use_ipa`` is on (with IPA Azure
    can take) -- i.e. whether Azure would say it differently from Edge."""
    load()
    pattern, ipa, _ = _ssml_state
    return bool(pattern) and any(m.group(1) in ipa for m in pattern.finditer(text))


def ssml(text: str) -> str:
    """``text`` as the body of an Azure ``<voice>`` element: XML-escaped, every
    ``use_ipa`` name as a ``<phoneme>`` tag (possessive inside it), every other
    override name respelled as ``respell`` would. Compact on purpose: Azure
    bills every character of it."""
    load()
    pattern, ipa, _ = _ssml_state
    table = _table or {}
    if not pattern:
        return xml_escape(text)
    out, pos = [], 0
    for m in pattern.finditer(text):
        name, poss = m.group(1), m.group(2) or ""
        out.append(xml_escape(text[pos:m.start()]))
        if name in ipa:
            out.append(phoneme(name + poss, ipa[name], possessive=bool(poss)))
        else:
            out.append(xml_escape(table.get(name, name) + poss))
        pos = m.end()
    out.append(xml_escape(text[pos:]))
    return "".join(out)


# --------------------------------------------------------------------------
# Saving (used by the GUI editor and the Verifier)
# --------------------------------------------------------------------------

_BOOK_INDEX = {name: i for i, name in enumerate(books.BOOK_NAMES)}


def _ref_key(ref: str):
    """Canonical sort key: book order, then chapter, verse. Unknown -> last."""
    m = re.match(r"^(.*?)\s+(\d+):(\d+)", ref or "")
    if not m:
        return (999, 999, 999)
    return (_BOOK_INDEX.get(m.group(1), 998), int(m.group(2)), int(m.group(3)))


_KEY_ORDER = ("say", "ipa", "ref", "override", "use_ipa", "status", "score")


def _tidy(info: dict) -> dict:
    """One entry with keys in a stable order, empty verdicts omitted and
    ``use_ipa`` written only when it is on."""
    out = {k: info[k] for k in _KEY_ORDER if k in info and info[k] not in ("", None)}
    out.setdefault("override", bool(info.get("override")))
    if not info.get("use_ipa"):
        out.pop("use_ipa", None)
    for k, v in info.items():          # keep anything unrecognised rather than drop it
        if k != "use_ipa":
            out.setdefault(k, v)
    return out


def _sorted_names(names: dict) -> dict:
    ordered = sorted(names.items(), key=lambda kv: (_ref_key(kv[1].get("ref", "")), kv[0]))
    return {k: _tidy(v) for k, v in ordered}


class SaveResult(NamedTuple):
    """What ``save_names`` wrote, and what the caller should be told about it."""
    names: dict    # the list as written: the merge, a fresh dict the caller may keep
    warning: str   # "" unless the file had changed on disk since the caller loaded it


_SAVE_LOCK = threading.Lock()


def _read_saved():
    """The names as they are on disk right now, bypassing the cache.

    None when the file is missing or unreadable -- which must not be mistaken
    for "every name was deleted elsewhere" by the merge.
    """
    try:
        with open(JSON_PATH, encoding="utf-8") as f:
            names = json.load(f).get("names")
    except (OSError, ValueError, AttributeError):
        return None
    return names if isinstance(names, dict) else None


def _canon(info):
    """An entry reduced to what it means, for telling a real edit from a re-save.

    Empty fields are dropped, ``override`` is a plain bool, ``use_ipa`` is kept
    only when on and the status is the effective one (``status_of``), so a tool
    that merely folds an untouched entry back -- adding ``"ipa": ""`` or
    spelling out the implied ``fixed`` -- has not edited it, and does not
    overwrite what another tool saved.
    """
    if info is None:
        return None
    out = {k: v for k, v in info.items() if v not in ("", None)}
    out["override"] = bool(info.get("override"))
    if not info.get("use_ipa"):
        out.pop("use_ipa", None)
    status = status_of(info)
    if status:
        out["status"] = status
    else:
        out.pop("status", None)
    return out


def _merge(names: dict, base: dict, saved: dict):
    """Three-way merge, per name: apply only what changed between ``base`` and
    ``names`` on top of ``saved``. Returns (merged, changed_elsewhere, clashes),
    where a clash is a name both sides changed differently (``names`` wins)."""
    merged = dict(saved)
    elsewhere, clashes = [], []
    for name in set(base) | set(names) | set(saved):
        mine = _canon(names.get(name))
        was = _canon(base.get(name))
        theirs = _canon(saved.get(name))
        if theirs != was:
            elsewhere.append(name)
        if mine == was:
            continue              # untouched here: what is on disk stands
        if theirs not in (was, mine):
            clashes.append(name)
        if name in names:
            merged[name] = names[name]
        else:
            merged.pop(name, None)
    return merged, elsewhere, sorted(clashes)


def _plural(n: int, word: str) -> str:
    return f"{n} {word}" + ("" if n == 1 else "s")


def _replace(tmp: str, path: str) -> None:
    """``os.replace``, retried briefly: on Windows it fails while another
    process has ``path`` open -- e.g. the main window re-reading the list."""
    for attempt in range(20):
        try:
            os.replace(tmp, path)
            return
        except PermissionError:
            if attempt == 19:
                raise
            time.sleep(0.05)


def save_names(names: dict, base: dict = None) -> SaveResult:
    """Write ``names`` to pronunciations.json (canonically ordered) + rebuild MD.

    Pronunciation Studio and the Verifier are separate processes, each editing
    its own copy of the list, so writing a copy back whole undoes whatever the
    other saved meanwhile. Pass ``base`` -- a deep copy of what the caller
    loaded -- and only the names that differ from it (added, changed, deleted)
    are applied, onto a fresh read of the file; every other name keeps what is
    on disk now. A name changed on both sides takes the caller's version, and
    the warning lists it.

    With no ``base`` the whole of ``names`` is written, as it always was, and
    the warning only notes (best effort) that the file's mtime moved since this
    process last loaded it.

    The file is written to a temp file and swapped in, so a reader never sees
    half of it. Returns ``SaveResult(names, warning)``: the list as written --
    the caller should adopt it, and a deep copy of it as its next ``base`` --
    and a warning, also printed, or "".
    """
    with _SAVE_LOCK:
        warning = ""
        merged = names
        if base is None:
            if _names is not None and _current_mtime() != _mtime:
                warning = ("pronunciations.json changed on disk since it was "
                           "loaded; this save replaced those changes.")
        else:
            saved = _read_saved()
            if saved is None:
                if base:
                    warning = ("pronunciations.json was missing or unreadable, "
                               "so this save wrote this window's whole list.")
            else:
                merged, elsewhere, clashes = _merge(names, base, saved)
                kept = len(elsewhere) - len(clashes)
                parts = []
                if kept:
                    parts.append(f"{_plural(kept, 'name')} saved by another "
                                 f"tool meanwhile {'was' if kept == 1 else 'were'} kept")
                if clashes:
                    shown = ", ".join(clashes[:8]) + ("…" if len(clashes) > 8 else "")
                    parts.append(f"{_plural(len(clashes), 'name')} changed in both "
                                 f"places took this window's version: {shown}")
                if parts:
                    warning = ("pronunciations.json had changed since this window "
                               "loaded it. " + "; ".join(parts) + ".")

        names_out = _sorted_names(merged)
        _write(names_out, _read_verses())
        write_markdown(names_out)
    if warning:
        print(warning, file=sys.stderr)
    return SaveResult(names_out, warning)


def save_verse(ref: str, words: dict) -> None:
    """Set the words ``ref`` has said differently to ``words`` ({words: say});
    empty removes the verse. Only that verse changes: the names and every
    other verse are written back as they are on disk now."""
    words = {w.strip(): say.strip() for w, say in words.items()
             if w.strip() and say.strip()}
    with _SAVE_LOCK:
        names = _read_saved()
        if names is None:
            raise OSError("pronunciations.json is missing or unreadable, so "
                          "the verse was not saved.")
        verses = _read_verses()
        if words:
            verses[ref] = words
        else:
            verses.pop(ref, None)
        _write(_sorted_names(names), verses)


def _read_verses() -> dict:
    """The ``verses`` section as it is on disk right now ({} if none)."""
    try:
        with open(JSON_PATH, encoding="utf-8") as f:
            verses = json.load(f).get("verses", {})
    except (OSError, ValueError, AttributeError):
        return {}
    return verses if isinstance(verses, dict) else {}


def _write(names: dict, verses: dict) -> None:
    """Write the whole file through a temp file, then reload the cache."""
    data = {"_readme": README, "names": names}
    if verses:
        data["verses"] = {ref: verses[ref] for ref in sorted(verses, key=_ref_key)}
    tmp = f"{JSON_PATH}.{os.getpid()}.tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        _replace(tmp, JSON_PATH)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)
    load(force=True)


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
        "  synthesis; IPA means Azure renders speak it from the IPA; blank means",
        "  the name is spoken exactly as spelled.",
        "- **Checked** — what listening to the real audio concluded. Blank means",
        "  nobody has checked it yet, which is not the same as it being right.",
        "",
        "| Name | Say it | IPA | First appears | TTS | Checked |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for name, info in rows:
        tts = " ".join(t for t, on in (("✅", info.get("override")),
                                        ("IPA", info.get("use_ipa"))) if on)
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
    n_ipa = sum(1 for _, i in rows if i.get("use_ipa"))
    n_both = sum(1 for _, i in rows if i.get("override") and i.get("use_ipa"))
    n_ref = sum(1 for _, i in rows if not (i.get("override") or i.get("use_ipa")))
    lines.append(
        f"_{len(rows)} names — {n_over} respelled for the voice, "
        f"{n_ipa} spoken from IPA on Azure ({n_both} of them respelled too), "
        f"{n_ref} reference-only._"
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
