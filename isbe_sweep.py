"""Headless verifier sweep + fix pass over the ISBE-referenced names.

For every name whose reference now comes from ISBE:
  1. measure the plain reading (what the pipeline would speak today) in both
     carriers, exactly as pronunciation_check.py does;
  2. if it clearly disagrees (< 0.55), acoustically test respelling candidates
     built from the ISBE syllables, and
       - adopt the winner as an override when it measures well (>= 0.70) and
         clearly beats the plain reading (+0.10),
       - otherwise record it as a suggestion if it merely beats plain,
       - otherwise leave the name marked still-wrong;
  3. record verdicts and the measurement cache like the GUI does.

Candidates deliberately follow the studio's hard-won respelling rules: no
bare-vowel hyphen segments, no trailing "-uh"; a single made-up word is
preferred, a consonant-anchored hyphenation is the fallback.
"""
import json
import os
import re
import sys
import time

sys.path.insert(0, r"C:\Dev\AV Bible")
os.chdir(r"C:\Dev\AV Bible")

import config           # noqa: E402
import ipa_asr          # noqa: E402
import pronunciation    # noqa: E402
import tts_engine       # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
VOICE = "en-US-AndrewNeural"
RATE = 0
CACHE_PATH = os.path.join(config.CACHE_DIR, "ipa_checks.json")
OK_AT, WARN_AT = 0.80, 0.55
ADOPT_AT, MARGIN = 0.70, 0.10

with open(os.path.join(HERE, "isbe_harvest.json"), encoding="utf-8") as f:
    HARVEST = json.load(f)["harvest"]


def spoken_for(name, info):
    if info.get("override") and info.get("say"):
        return info["say"].lower()
    return name


def measure(spoken, expected):
    """Two-carrier measurement; returns (score|None, 'span / span')."""
    scores, spans = [], []
    for text_fmt, head, tail in ipa_asr.CARRIERS:
        for attempt in range(3):
            try:
                path = tts_engine.synthesize(text_fmt.format(spoken), VOICE,
                                             RATE, apply_respell=False)
                heard = ipa_asr.transcribe(path)
                break
            except Exception as e:      # noqa: BLE001
                if attempt == 2:
                    return None, f"error: {e}"
                time.sleep(5)
        span = ipa_asr.strip_carrier(heard, head, tail)
        if span:
            spans.append(span)
            scores.append(ipa_asr.similarity(expected, span))
    if not scores:
        return None, ""
    return sum(scores) / len(scores), " / ".join(spans)


# ---------------------------------------------------------------- candidates
# ISBE syllable -> a spelling the voice tends to read as intended.
_SYL_MAP = [
    ("tch", "ch"), ("oo", "oo"), ("ee", "ee"), ("ai", "ay"), ("ay", "ay"),
    ("au", "aw"), ("aw", "aw"), ("oi", "oy"), ("oy", "oy"), ("ou", "ow"),
]


def _candidate_syls(respell):
    """ISBE respelling -> list of syllable spellings tuned for the voice."""
    syls = [s.replace("'", "") for s in respell.lower().split("-") if s.strip("'")]
    stress = None
    for i, s in enumerate(respell.lower().split("-")):
        if "'" in s:
            stress = i
            break
    out = []
    for i, s in enumerate(syls):
        v = s
        is_final = i == len(syls) - 1
        stressed = (i == stress) if stress is not None else i == 0
        # open-syllable single vowels: respell so the voice says the long form
        if re.fullmatch(r"[bcdfghjklmnpqrstvwxyz]*[aeiou]", v):
            head, vowel = v[:-1], v[-1]
            if vowel == "a":
                # long "ay" when stressed mid-word; final/unstressed -> "ah"
                # (never a trailing "-uh": the voice lengthens it to "oo")
                v = head + ("ay" if stressed and not is_final else "ah")
            elif vowel == "e":
                v = head + ("ee" if stressed else "eh")
            elif vowel == "i":
                # stressed open i is the long /aɪ/; "igh" reads reliably
                v = head + (("igh" if head else "eye") if stressed else "ih")
            elif vowel == "o":
                v = head + "oh"
            elif vowel == "u":
                v = head + "oo"
        out.append((v, stressed))
    return out


# A hyphenated segment that is ONLY vowels ("ee", "e", "a", "oo") is read out
# letter-by-letter by the neural voice (user-confirmed by ear: "ee-mim" is
# spoken "E, E, mim") even though the transcriber hears a clean long vowel --
# an acoustic blind spot. Consonant-bearing short segments ("ah", "jam") are
# fine, and hyphens are often load-bearing, so ONLY pure-vowel segments are
# dissolved -- into the previous or the next syllable (both get tested).
PURE_VOWEL = re.compile(r"^[aeiou]+$")


def merge_left(syls):
    """Dissolve pure-vowel segments into the preceding syllable."""
    parts = []
    for s in syls:
        if not s:
            continue
        if parts and (PURE_VOWEL.match(s) or PURE_VOWEL.match(parts[-1])):
            parts[-1] += s
        else:
            parts.append(s)
    return "-".join(parts)


def merge_right(syls):
    """Dissolve pure-vowel segments into the following syllable."""
    parts = []
    for s in reversed([x for x in syls if x]):
        if parts and (PURE_VOWEL.match(s) or PURE_VOWEL.match(parts[-1])):
            parts[-1] = s + parts[-1]
        else:
            parts.append(s)
    return "-".join(reversed(parts))


def candidates(name, respell):
    """Return ordered candidate 'say' strings to test."""
    tuned = [v for v, _ in _candidate_syls(respell)]
    raw = [s.replace("'", "") for s in respell.lower().split("-") if s.strip("'")]
    cands = [merge_left(tuned), merge_right(tuned), "".join(tuned),
             merge_left(raw), merge_right(raw), "".join(raw)]
    # never test the name itself, nor anything still carrying a pure-vowel seg
    seen, out = {name.lower()}, []
    for c in cands:
        if c and c.lower() not in seen and not any(
                PURE_VOWEL.match(seg) for seg in c.split("-")):
            seen.add(c.lower())
            out.append(c)
    return out


def main():
    names = pronunciation.load(force=True)
    try:
        with open(CACHE_PATH, encoding="utf-8") as f:
            cache = json.load(f)
    except (OSError, ValueError):
        cache = {}

    pass2 = "--pass2" in sys.argv
    targets = [n for n, v in names.items() if v.get("ipa_src") == "isbe"]
    if pass2:
        # second pass: only names still marked wrong; candidates get tried up
        # to the ok threshold, and the plain measurement is reused from cache
        targets = [t for t in targets
                   if names[t].get("status") == pronunciation.STATUS_UNFIXED]
    only = [a for a in sys.argv[1:] if not a.startswith("--")] or None
    if only:
        targets = [t for t in targets if t in only]
    print(f"{len(targets)} ISBE-referenced names to verify", flush=True)

    ipa_asr.load_model(status=lambda m: print(m, flush=True))

    fixed = suggested = ok = unfixed = unmeasured = 0
    t0 = time.time()
    for i, name in enumerate(sorted(targets), 1):
        info = names[name]
        expected = info["ipa"]
        spoken = spoken_for(name, info)
        c = cache.get(name)
        if (pass2 and c and c.get("mode") == "carrier-avg"
                and c.get("voice") == VOICE and c.get("spoken") == spoken
                and c.get("score") is not None):
            score, heard = c["score"], c["heard"]
        else:
            score, heard = measure(spoken, expected)
        if score is None:
            unmeasured += 1
            print(f"[{i}] {name}: unmeasured ({heard})", flush=True)
            continue
        cache[name] = {"spoken": spoken, "voice": VOICE, "mode": "carrier-avg",
                       "heard": heard, "score": round(score, 3)}
        best_say, best_score, best_heard = None, score, heard
        gate = OK_AT if pass2 else WARN_AT
        if score < gate and not info.get("override") and name in HARVEST:
            for cand in candidates(name, HARVEST[name]["respell"]):
                cscore, cheard = measure(cand.lower(), expected)
                if cscore is not None and cscore > best_score:
                    best_say, best_score, best_heard = cand, cscore, cheard
        if best_say and best_score >= ADOPT_AT and best_score >= score + MARGIN:
            info["say"] = best_say
            info["override"] = True
            pronunciation.set_status(info, pronunciation.STATUS_FIXED, best_score)
            cache[name] = {"spoken": best_say.lower(), "voice": VOICE,
                           "mode": "carrier-avg", "heard": best_heard,
                           "score": round(best_score, 3)}
            fixed += 1
            tag = f"FIXED -> {best_say} ({best_score:.2f}, was {score:.2f})"
        elif best_say and best_score >= score + MARGIN:
            info["say"] = best_say          # recorded, not applied
            pronunciation.set_status(info, pronunciation.STATUS_SUGGESTED, score)
            suggested += 1
            tag = f"suggested {best_say} ({best_score:.2f}, plain {score:.2f})"
        elif info.get("override"):
            pronunciation.set_status(info, pronunciation.STATUS_FIXED, score)
            tag = f"override kept ({score:.2f})"
        elif score >= OK_AT:
            pronunciation.set_status(info, pronunciation.STATUS_OK, score)
            ok += 1
            tag = f"ok ({score:.2f})"
        else:
            pronunciation.set_status(info, pronunciation.STATUS_UNFIXED, score)
            unfixed += 1
            tag = f"still wrong ({score:.2f})"
        print(f"[{i}/{len(targets)}] {name}: {tag}", flush=True)
        if i % 25 == 0:
            with open(CACHE_PATH, "w", encoding="utf-8") as f:
                json.dump(cache, f, indent=1, ensure_ascii=False)
            pronunciation.save_names(names)
            el = time.time() - t0
            print(f"  … saved. {el/60:.1f} min elapsed, "
                  f"{el/i*(len(targets)-i)/60:.0f} min left", flush=True)

    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=1, ensure_ascii=False)
    pronunciation.save_names(names)
    print(f"DONE: {ok} ok, {fixed} fixed, {suggested} suggested, "
          f"{unfixed} still wrong, {unmeasured} unmeasured", flush=True)


if __name__ == "__main__":
    main()
