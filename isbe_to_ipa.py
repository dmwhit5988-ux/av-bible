"""Convert ISBE pronunciation respellings (diacritics lost) to reference IPA.

The online ISBE digitization keeps syllable breaks and the stress apostrophe
("a-da-li'-a") but drops the vowel macrons/breves of the print edition. So:
syllabification and stress are SOURCED; vowel quality is inferred from open/
closed syllable shape plus the digraphs that did survive (oo, ee, ai, aw...).
The scorer folds vowels onto a coarse alphabet anyway, so stress+consonants+
vowel class carry nearly all the signal.

convert("a-da-li'-a") -> "/əˌdəˈlaɪ.ə/" (roughly; see rules in code)
"""
import re

# consonant digraphs/letters -> IPA (respelling alphabet is already phonetic:
# soft g is written j, hard c as k, so bare letters map 1:1)
_CONS = [
    ("tch", "tʃ"), ("sh", "ʃ"), ("ch", "tʃ"), ("th", "θ"), ("zh", "ʒ"),
    ("ng", "ŋ"), ("hw", "w"), ("ph", "f"), ("wh", "w"), ("gh", "g"),
    ("b", "b"), ("d", "d"), ("f", "f"), ("g", "g"), ("h", "h"), ("j", "dʒ"),
    ("k", "k"), ("l", "l"), ("m", "m"), ("n", "n"), ("p", "p"), ("q", "k"),
    ("r", "r"), ("s", "s"), ("t", "t"), ("v", "v"), ("w", "w"), ("y", "j"),
    ("z", "z"), ("c", "k"), ("x", "ks"),
]

# vowel digraphs that survive digitization
_VOW2 = {
    "oo": "uː", "ee": "iː", "ai": "eɪ", "ay": "eɪ", "ea": "iː",
    "au": "ɔː", "aw": "ɔː", "oi": "ɔɪ", "oy": "ɔɪ", "ou": "aʊ", "ow": "aʊ",
    "ei": "eɪ", "eu": "juː", "ew": "juː", "ie": "iː", "oa": "oʊ", "ue": "uː",
    "igh": "aɪ",
}

_LONG = {"a": "eɪ", "e": "iː", "i": "aɪ", "o": "oʊ", "u": "juː"}
_SHORT = {"a": "æ", "e": "ɛ", "i": "ɪ", "o": "ɒ", "u": "ʌ"}
_R_COLORED = {"a": "ɑːr", "e": "ər", "i": "ɪr", "o": "ɔːr", "u": "ər"}
# Unstressed open syllables. The curated references in this project do not
# reduce as aggressively as general English: unstressed e/i stay /i/
# ("-i-el" -> i.ɛl, "be-e-" -> bi), matching their house style.
_REDUCED = {"a": "ə", "e": "i", "i": "i", "o": "oʊ", "u": "jʊ"}


def _syl_to_ipa(syl, stressed, is_final):
    """One respelling syllable -> IPA, using open/closed shape for quality."""
    s = syl.lower()
    out = []
    i = 0
    # tokenize into consonant / vowel units
    units = []
    while i < len(s):
        two = s[i:i + 2]
        three = s[i:i + 3]
        if three == "tch":
            units.append(("c", "tʃ")); i += 3; continue
        if three == "igh":
            units.append(("v", "aɪ")); i += 3; continue
        if two in _VOW2:
            units.append(("v", _VOW2[two])); i += 2; continue
        matched = False
        for lit, ipa in _CONS:
            if s.startswith(lit, i) and (len(lit) > 1 or s[i] not in "aeiou"):
                units.append(("c", ipa)); i += len(lit); matched = True
                break
        if matched:
            continue
        if s[i] in "aeiou":
            units.append(("v", s[i])); i += 1; continue
        i += 1  # unknown char: drop
    # resolve single-letter vowels by syllable shape
    for j, (kind, val) in enumerate(units):
        if kind == "v" and val in "aeiou":
            rest = units[j + 1:]
            followed_by_cons = any(k == "c" for k, _ in rest)
            next_is_r = rest and rest[0][1] == "r" and not any(
                k == "v" for k, _ in rest)
            # Final -i and -ite(s): traditionally the long /aɪ/ in Anglicised
            # biblical names (Guni, Amzi, Danites…) — the lost macron was ī.
            if is_final and val == "i" and all(
                    u[1] in ("t", "s", "") for u in rest) and (
                    not rest or rest[0][1] == "t" or not followed_by_cons):
                units[j] = ("v", "aɪ")
                continue
            if next_is_r:
                units[j] = ("v", _R_COLORED[val])
                # the r is inside the colored vowel; drop the standalone r
                units[j + 1] = ("c", "")
            elif not followed_by_cons:          # open syllable
                if stressed:
                    units[j] = ("v", _LONG[val])
                elif is_final and val == "a":
                    units[j] = ("v", "ə")
                else:
                    units[j] = ("v", _REDUCED[val])
            else:                               # closed syllable
                # keep the full short vowel even unstressed ("-am" -> æm,
                # "-el" -> ɛl) — the curated house style does not reduce these
                units[j] = ("v", _SHORT[val])
    return "".join(v for _, v in units)


def convert(respell: str) -> str:
    """ISBE respelling -> /IPA/ with stress and syllable dots."""
    r = respell.strip().lower().replace("`", "'")
    syls = [x for x in r.split("-") if x.strip("'")]
    # Trailing "-a-i" is the Hebrew -ai ending, /aɪ/ as one syllable
    if len(syls) >= 2 and syls[-1].strip("'") == "i" and syls[-2].strip("'") == "a":
        tail = "".join(x for x in syls[-2:] if "'" in x)
        syls = syls[:-2] + ["igh" + ("'" if tail else "")]  # placeholder: /aɪ/
    stressed_idx = None
    clean = []
    for idx, syl in enumerate(syls):
        if "'" in syl and stressed_idx is None:
            stressed_idx = idx
        clean.append(syl.replace("'", ""))
    if stressed_idx is None:
        stressed_idx = 0
    parts = []
    for idx, syl in enumerate(clean):
        ipa = _syl_to_ipa(syl, idx == stressed_idx, idx == len(clean) - 1)
        if not ipa:
            continue
        parts.append((idx == stressed_idx, ipa))
    # A syllable with no vowel is a syllabic consonant ("e'-d'-n"): merge it
    # into its neighbour, giving sonorants their schwa (-> iː.dən).
    _vowels = set("aeiouæɛɪɒʌəɔ")
    merged = []
    for stressed, ipa in parts:
        if merged and not (_vowels & set(ipa)):
            ps, pipa = merged[-1]
            if ipa and ipa[-1] in "nml":
                merged[-1] = (ps, pipa + ipa[:-1] + "ə" + ipa[-1])
            else:
                merged[-1] = (ps, pipa + ipa)
        else:
            merged.append((stressed, ipa))
    parts = merged
    out = ""
    for k, (stressed, ipa) in enumerate(parts):
        if stressed:
            out += "ˈ"
        elif k == 0 and len(parts) > 2:
            out += ""
        out += ipa
        if k < len(parts) - 1:
            out += "."
    return "/" + out + "/"


if __name__ == "__main__":
    for t in ["a-da-li'-a", "ar'-un", "shoo'-the-la", "kush", "me-shel-e-mi'-a",
              "je-di'-a-el", "a-hin'-o-am", "ba'-a-sha", "shoo-the'-la"]:
        print(t, "->", convert(t))
