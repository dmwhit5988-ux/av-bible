"""Repair pass: remove letter-by-letter hyphen traps from this session's says.

The user confirmed by ear that a hyphenated bare-vowel or 2-letter segment
("ee-mim", "e-hi", "gal-e-ed") is read out as letters, and that the acoustic
scorer cannot hear the fault (a quick "E, E" transcribes as one long vowel).
So: for every fixed/suggested entry this session created (ipa_src == "isbe")
whose say still contains a risky segment, test merged alternatives and adopt
the best one that holds the score (within 0.05). The acoustic test guards
against a merge *changing* the pronunciation (e.g. "taira" turning into
TY-ruh); the merge itself removes the fault the test cannot hear.
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

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from isbe_sweep import (measure, merge_left, merge_right, candidates,  # noqa: E402
                        PURE_VOWEL, HARVEST, VOICE, CACHE_PATH)


def _risky(say):
    return any(PURE_VOWEL.match(seg) for seg in say.lower().split("-"))

TOL = 0.05


def main():
    names = pronunciation.load(force=True)
    try:
        with open(CACHE_PATH, encoding="utf-8") as f:
            cache = json.load(f)
    except (OSError, ValueError):
        cache = {}

    targets = []
    for name, info in names.items():
        say = info.get("say") or ""
        if (info.get("ipa_src") == "isbe"
                and info.get("status") in ("fixed", "suggested")
                and "-" in say and _risky(say)):
            targets.append(name)
    print(f"{len(targets)} risky says to repair", flush=True)
    ipa_asr.load_model(status=lambda m: print(m, flush=True))

    repaired = kept = 0
    for i, name in enumerate(sorted(targets), 1):
        info = names[name]
        say, expected = info["say"], info["ipa"]
        old_score = info.get("score") or 0.0
        segs = [s for s in say.lower().split("-") if s]
        cands = [merge_left(segs), merge_right(segs), "".join(segs)]
        if name in HARVEST:
            cands += candidates(name, HARVEST[name]["respell"])
        seen, todo = {name.lower(), say.lower()}, []
        for c in cands:
            if c and c.lower() not in seen and not _risky(c):
                seen.add(c.lower())
                todo.append(c)
        best_say, best_score, best_heard = None, -1.0, ""
        for cand in todo:
            s, h = measure(cand.lower(), expected)
            if s is not None and s > best_score:
                best_say, best_score, best_heard = cand, s, h
        # The old score is inflated by the very blind spot being repaired, so a
        # merged form that measures well on honest audio (>= 0.70, the sweep's
        # own adoption bar) wins even when it can't match the inflated number.
        if best_say and (best_score >= old_score - TOL or best_score >= 0.70):
            info["say"] = best_say
            info["override"] = True
            pronunciation.set_status(info, pronunciation.STATUS_FIXED,
                                     best_score)
            if info.get("override"):
                cache[name] = {"spoken": best_say.lower(), "voice": VOICE,
                               "mode": "carrier-avg", "heard": best_heard,
                               "score": round(best_score, 3)}
            repaired += 1
            tag = f"repaired -> {best_say} ({best_score:.2f}, was {say} {old_score:.2f})"
        else:
            # The say is known-misread (pure-vowel segment) and no repair held
            # the score: don't ship it as an override. Leave it as a suggestion
            # for the user's ear.
            if info.get("override"):
                info["override"] = False
                cache.pop(name, None)
            pronunciation.set_status(info, pronunciation.STATUS_SUGGESTED,
                                     old_score)
            kept += 1
            tag = (f"demoted to suggestion: {say} — no merge held the score "
                   f"(best {best_say} {best_score:.2f} vs {old_score:.2f})")
        print(f"[{i}/{len(targets)}] {name}: {tag}", flush=True)
        if i % 25 == 0:
            pronunciation.save_names(names)
            with open(CACHE_PATH, "w", encoding="utf-8") as f:
                json.dump(cache, f, indent=1, ensure_ascii=False)

    pronunciation.save_names(names)
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=1, ensure_ascii=False)
    print(f"DONE: {repaired} repaired, {kept} kept (flagged for the ear)", flush=True)


if __name__ == "__main__":
    main()
