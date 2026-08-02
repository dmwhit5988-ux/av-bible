"""Guess an Anglicised IPA for a biblical proper noun from its spelling.

Scaling the verifier to the whole canon needs a reference pronunciation for
~1400 names that have none, and hand-authoring that many would be both slow and
the least trustworthy part of the pipeline. This generates them by the
conventions English uses for scripture names -- ch as /k/, -iah as /ˈaɪ.ə/,
hard g -- so that the guesses can at least be measured: run it over the names
that DO have a curated reference and the agreement says how far to trust it.
"""
import re

VOWELS = "aeiouy"

# Multi-letter graphemes, longest first. Values are (onset-consonant, nucleus).
DIGRAPH_C = {
    "sch": "sk", "tch": "tʃ", "sh": "ʃ", "ch": "k", "ph": "f", "th": "θ",
    "wh": "w", "kn": "n", "ps": "s", "gh": "ɡ", "qu": "kw", "ck": "k",
}
SINGLE_C = {
    "b": "b", "c": "k", "d": "d", "f": "f", "g": "ɡ", "h": "h", "j": "dʒ",
    "k": "k", "l": "l", "m": "m", "n": "n", "p": "p", "q": "k", "r": "r",
    "s": "s", "t": "t", "v": "v", "w": "w", "x": "ks", "z": "z",
}
# Vowel digraphs -> (long value, short value)
DIGRAPH_V = {
    "ai": "eɪ", "ay": "eɪ", "ea": "iː", "ee": "iː", "ei": "aɪ", "ey": "eɪ",
    "ie": "aɪ", "oa": "oʊ", "oe": "oʊ", "oo": "uː", "ou": "aʊ", "ow": "aʊ",
    "au": "ɔː", "aw": "ɔː", "eu": "juː", "ui": "uː", "oi": "ɔɪ", "oy": "ɔɪ",
}
OPEN_V = {"a": "eɪ", "e": "iː", "i": "aɪ", "o": "oʊ", "u": "juː", "y": "aɪ"}
SHUT_V = {"a": "æ", "e": "ɛ", "i": "ɪ", "o": "ɒ", "u": "ʌ", "y": "ɪ"}


def _split_syllables(word: str):
    """Crude syllabification: each vowel group is a nucleus, split consonants."""
    w = word.lower()
    units = []                       # (consonant-cluster, vowel-group)
    i = 0
    cluster = ""
    while i < len(w):
        if w[i] in VOWELS:
            v = w[i]
            i += 1
            # A vowel digraph only counts when it is a known pair.
            if i < len(w) and (v + w[i]) in DIGRAPH_V:
                v += w[i]
                i += 1
            else:
                while i < len(w) and w[i] in VOWELS and (v[-1] + w[i]) not in DIGRAPH_V:
                    # "ia", "eo" etc: separate nuclei, so stop and let the next
                    # loop pick it up.
                    break
            units.append([cluster, v, ""])
            cluster = ""
        else:
            cluster += w[i]
            i += 1
    if cluster:
        if units:
            units[-1][2] = cluster           # trailing coda
        else:
            units.append([cluster, "", ""])
    # Split each medial cluster: first consonant closes the syllable, rest opens
    # the next -- the usual English VC-CV rule that keeps "bil" short in Bileam.
    for k in range(len(units) - 1):
        nxt = units[k + 1][0]
        # Never split a digraph: "Ashan" divided as as|han turns /ʃ/ into /s/+/h/
        # and wrecks the whole word. Same for ph, th, ch.
        if len(nxt) >= 2 and nxt[:2].lower() not in DIGRAPH_C:
            units[k][2] = nxt[0]
            units[k + 1][0] = nxt[1:]
    return units


def _consonants(chunk: str):
    out, i = [], 0
    c = chunk.lower()
    while i < len(c):
        for n in (3, 2):
            if c[i:i + n] in DIGRAPH_C:
                out.append(DIGRAPH_C[c[i:i + n]])
                i += n
                break
        else:
            if c[i] == "c":
                nxt = c[i + 1] if i + 1 < len(c) else ""
                out.append("s" if nxt in "eiy" else "k")
            elif c[i] in SINGLE_C:
                out.append(SINGLE_C[c[i]])
            i += 1
    return "".join(out)


def _stress_index(units, word: str) -> int:
    """Which syllable carries primary stress."""
    n = len(units)
    if n <= 1:
        return 0
    low = word.lower()
    if low.endswith("iah") or low.endswith("iel") or low.endswith("iam"):
        return max(0, n - 2)        # Jere-MI-ah, Ez-E-kiel
    if n == 2:
        return 0
    return n - 3 if n >= 3 else 0   # antepenultimate for longer names


def guess(word: str) -> str:
    """Return an IPA guess like ``/dʒɛr.əˈmaɪ.ə/`` for ``word``."""
    word = re.sub(r"[^A-Za-z-]", "", word)
    if not word:
        return ""
    if "-" in word:                  # compound: do each half, join on the hyphen
        parts = [guess(p) for p in word.split("-") if p]
        return "/" + ".".join(p.strip("/") for p in parts) + "/"

    units = _split_syllables(word)
    if not units:
        return ""
    stress = _stress_index(units, word)
    low = word.lower()
    out = []
    for k, (onset, vowel, coda) in enumerate(units):
        on = _consonants(onset)
        cd = _consonants(coda)
        last = k == len(units) - 1
        if not vowel:
            out.append(("", on + cd))
            continue
        # A medial h after a vowel is not pronounced; it lengthens the vowel
        # instead (Ahlai is AH-lye, not AH-h-lye; Yahweh is YAH-way).
        if cd == "h" and not last:
            cd = ""
            coda = ""
        if on == "h" and k and units[k - 1][2] == "":
            pass                      # keep a real onset h (Ahio, Elihu)

        if vowel in DIGRAPH_V:
            nuc = DIGRAPH_V[vowel]
        elif vowel == "i" and not coda and not last:
            nuc = "i"                 # Jahdiel, Jahziel: i before a vowel
        elif last and low.endswith("ah"):
            nuc = "ə"
        elif last and vowel == "e" and coda == "":
            nuc = "iː"                       # Bethphage, Cyrene
        elif last and vowel in ("ai", "ay") :
            nuc = "aɪ"                       # Ahlai, Hushai, Zimri-type endings
        elif last and vowel == "u" and on.endswith("h"):
            nuc = "juː"                      # Elihu, Abihu
        elif k != stress:
            nuc = "ɪ" if vowel == "i" and coda else "ə"
        elif coda:                           # closed stressed syllable
            nuc = SHUT_V.get(vowel, "ə")
        else:                                # open stressed syllable
            nuc = OPEN_V.get(vowel, "ə")
        if low.endswith("iah") and k == len(units) - 1:
            nuc = "ə"
        out.append((("ˈ" if k == stress else "") + on + nuc + cd, ""))

    body = ".".join(p for p, _ in out if p) or "".join(x for _, x in out)
    body = body.replace(".ˈ", "ˈ") if body.startswith(".") else body
    # Put the stress mark before its syllable rather than inside the dot chain.
    body = re.sub(r"\.ˈ", "ˈ", body)
    return "/" + body + "/"


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    for w in ("Jeremiah", "Nebuchadnezzar", "Bileam", "Havilah", "Methuselah",
              "Zimri", "Chelubai", "Ephraim", "Gihon", "Melchizedek", "Sarah"):
        print(f"{w:<16} {guess(w)}")
