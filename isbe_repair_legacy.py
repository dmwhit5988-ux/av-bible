"""Repair the hand-tuned overrides that still carry a letter-by-letter trap.

These 15 predate the ISBE work and were written by ear, so `isbe_repair.py`
(which only touches this session's machine-made spellings) left them alone.
Each carries a pure-vowel hyphen segment -- "BAY-a-ruh", "EE-fron" -- which the
voice reads out as a letter while the transcriber hears a clean vowel, so no
score can clear them (see the acoustic blind spot in pronunciation_check.py).

Two things are being fixed at once, because the transcriptions show both:

  * the pure-vowel segment ("-a-" -> "-uh-", "EE-" -> "ee" joined on), and
  * a trailing "-uh", which the voice lengthens to "oo": "BAY-a-ruh" comes
    back as [b eI @ r u]. That fault the scorer CAN see, so fixing it should
    raise the score rather than merely hold it.

Candidates are hand-written per name rather than generated: there are 15 of
them, they are irregular, and a generator has no way to know that "kyooz" is
losing its /j/ or that "i-" is being read "eye". Every candidate is measured
in both carriers against the entry's curated IPA, and one is adopted only if
it holds the current reading (within 0.03) -- the test cannot see the fault
being fixed, so its only job is to catch a rewrite that changes the word.
"""
import json
import os
import sys

import config
import ipa_asr
import pronunciation
import tts_engine

VOICE = "en-US-AndrewNeural"
RATE = 0
CACHE_PATH = os.path.join(config.CACHE_DIR, "ipa_checks.json")
TOL = 0.03

# name -> candidate spellings, best-guess first. Rules applied:
#   "-a-"    -> "-uh-"   (consonant-anchored, so not read as a letter)
#   "-uh"    -> "-ah"    (trailing -uh lengthens to "oo")
#   "EE-"    -> joined   (a leading bare vowel is spelled out)
#   "i-"     -> "ih-"    (bare i is read "eye")
CANDIDATES = {
    "Achaia":       ["uh-KAY-ah", "uh-KAY-uh", "ah-KAY-ah"],
    "Amariah":      ["am-uh-REYE-ah", "am-uh-REYE-uh", "ammuh-REYE-ah"],
    "Baara":        ["BAY-uh-rah", "BAY-uh-ruh", "BAYuh-rah"],
    "Beracah":      ["BEHR-uh-kah", "BEHR-uh-kuh", "BEHRuh-kah"],
    "Berachah":     ["BEHR-uh-kah", "BEHR-uh-kuh", "BEHRuh-kah"],
    "Bethsaida":    ["behth-SAY-ih-dah", "behth-SAY-ih-duh", "behthSAY-ih-dah"],
    "Cenchreae":    ["sehn-KREE-yee", "sehn-KREEee", "sehnKREE-yee"],
    "Eliel":        ["EElee-ehll", "eelee-ehll", "EElee-ell"],
    "Eliphelehu":   ["ih-lihf-uh-LEE-hoo", "ihlihf-uh-LEE-hoo",
                     "ih-lihf-uh-LEEhoo"],
    "Ephron":       ["EEfron", "eefron", "EEfron"],
    "Jaalam":       ["JAY-uh-lam", "JAYuh-lam", "jay-uh-lam"],
    "Jehoshabeath": ["jee-hoh-SHAB-yee-athh", "jee-hoh-SHABee-athh",
                     "jeehoh-SHAB-yee-athh"],
    "Maachah":      ["MAY-uh-kah", "MAY-uh-kuh", "MAYuh-kah"],
    "Naarah":       ["NAY-uh-rah", "NAY-uh-ruh", "NAYuh-rah"],
    "Syracuse":     ["SIHR-uh-kewz", "SIHR-uh-kyooz", "SIHRuh-kewz"],
}

# Round two, for the names round one could not settle. What round one taught:
# a lone "uh" is not always safe either (MAY-uh-kah came back [meI aU k A] --
# read as the "ow" diphthong), so the schwa is better carried by a glide the
# name already implies: "MAY-yuh-" for /eI.@/, "-mmuh-" doubling the anchor
# consonant. A leading "ee" cannot be hyphenated off and cannot be dropped
# either, so it is joined and the FOLLOWING syllable is re-spelled to stop the
# join changing it ("eefrawn" not "eefron").
ROUND2 = {
    "Amariah":     ["ammuh-REYE-uh", "am-muh-REYE-uh", "amuh-REYE-uh"],
    "Cenchreae":   ["sehn-kree-yee", "sen-KREE-yee", "sehnkree-yee"],
    "Eliel":       ["eelee-ehl", "eeleeehll", "eelee-yehll"],
    "Eliphelehu":  ["illihf-uh-LEE-hoo", "ihllihf-uh-LEE-hoo",
                    "ilihf-uh-LEE-hoo"],
    "Ephron":      ["eefrawn", "eefrahn", "eefrohn"],
    "Maachah":     ["MAY-yuh-kuh", "MAY-yuh-kah", "mayuh-kuh"],
    "Naarah":      ["NAY-yuh-ruh", "NAY-yuh-rah", "nayuh-ruh"],
}

# Round three. The cleanest escape from a respelling trap is to stop
# respelling: the name itself can never be read out as letters. So the bare
# spelling is tested here alongside the remaining ideas, and where it wins the
# override is dropped rather than replaced (this is what `override:false`
# is for -- see the Methuselah note in the pronunciation memory: the voice's
# own lexicon beats a respelling more often than the respelling deserves).
ROUND3 = {
    "Cenchreae":  ["Cenchreae", "sehn-kreeyee", "sehn-KREE-yeh"],
    "Eliel":      ["Eliel", "eelee-yehl", "eeliyehll"],
    "Eliphelehu": ["Eliphelehu", "ilif-uh-LEE-hoo", "ihlif-uh-LEE-hoo"],
    "Maachah":    ["Maachah", "MAY-ah-kuh", "MAY-ah-kah"],
    "Naarah":     ["Naarah", "NAY-ah-ruh", "NAY-ah-rah"],
}

# Round four: Bethsaida only. Round one's replacement cleared the trap at an
# unchanged 0.69 but introduced a spurious affricate, so the syllable boundary
# is being cut in the wrong place. These move it.
ROUND4 = {
    "Bethsaida": ["behth-SAY-yih-duh", "behth-SAY-yih-dah", "beth-SAY-ih-duh",
                  "behthsay-ih-duh", "behth-SIGH-duh"],
}

# Round five: the two names ending in an unstressed /@/ that nothing has
# fixed. Bethsaida was solved by a "y" glide carrying the weak syllable, so
# that shape is retried here against a bare final "-a" and "-er", since both
# "-uh" (lengthens to "oo") and "-ah" (opens to /A/) are already known wrong.
ROUND5 = {
    "Maachah": ["MAY-yuh-ka", "MAY-yuh-kuh", "may-yuh-ka", "MAY-yuh-ker"],
    "Naarah":  ["NAY-yuh-ra", "NAY-yuh-ruh", "nay-yuh-ra", "NAY-yuh-rer"],
}


def measure(spoken, expected):
    scores, spans = [], []
    for text_fmt, head, tail in ipa_asr.CARRIERS:
        path = tts_engine.synthesize(text_fmt.format(spoken), VOICE, RATE,
                                     apply_respell=False)
        span = ipa_asr.strip_carrier(ipa_asr.transcribe(path), head, tail)
        if span:
            spans.append(span)
            scores.append(ipa_asr.similarity(expected, span))
    if not scores:
        return None, ""
    return sum(scores) / len(scores), " / ".join(spans)


def main():
    names = pronunciation.load(force=True)
    try:
        with open(CACHE_PATH, encoding="utf-8") as f:
            cache = json.load(f)
    except (OSError, ValueError):
        cache = {}

    ipa_asr.load_model(status=lambda m: print(m, flush=True))
    table = (ROUND5 if "--round5" in sys.argv else
             ROUND4 if "--round4" in sys.argv else
             ROUND3 if "--round3" in sys.argv else
             ROUND2 if "--round2" in sys.argv else CANDIDATES)
    changed = kept = 0
    for name, cands in sorted(table.items()):
        info = names.get(name)
        if info is None:
            print(f"{name}: not in list", flush=True)
            continue
        expected, old_say = info["ipa"], info["say"]
        base, base_heard = measure(old_say.lower(), expected)
        print(f"\n{name}  ref {expected}\n  current  {old_say:24} "
              f"{base if base is None else round(base, 3)}  {base_heard}",
              flush=True)
        best = None
        for cand in cands:
            s, h = measure(cand.lower(), expected)
            print(f"  cand     {cand:24} "
                  f"{s if s is None else round(s, 3)}  {h}", flush=True)
            if s is not None and (best is None or s > best[1]):
                best = (cand, s, h)
        if best and base is not None and best[1] >= base - TOL:
            info["say"] = best[0]
            if best[0].lower() == name.lower():
                # The plain spelling reads as well as the respelling: drop the
                # override entirely. No spelling, no trap.
                info["override"] = False
                pronunciation.set_status(info, pronunciation.STATUS_OK,
                                         best[1])
                verdict = "DROPPED override — reads correctly as spelled"
            else:
                pronunciation.set_status(info, pronunciation.STATUS_FIXED,
                                         best[1])
                verdict = f"ADOPTED {best[0]}"
            cache[name] = {"spoken": best[0].lower(), "voice": VOICE,
                           "mode": "carrier-avg", "heard": best[2],
                           "score": round(best[1], 3)}
            changed += 1
            print(f"  -> {verdict} ({best[1]:.2f} vs {base:.2f})", flush=True)
        else:
            kept += 1
            print(f"  -> kept {old_say} (no candidate held the reading)",
                  flush=True)

    pronunciation.save_names(names)
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=1, ensure_ascii=False)
    print(f"\nDONE: {changed} respelled, {kept} kept", flush=True)


if __name__ == "__main__":
    main()
