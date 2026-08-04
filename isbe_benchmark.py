"""Measure ISBE-converted IPA against curated references before trusting it.

Yardstick from the project's own history: the rule generator scores 0.72
against curated references; the neural voice scores 0.77. If ISBE conversion
lands well above 0.72 it is a stronger reference than the guesses it replaces.

Samples curated-reference names, looks each up in the ISBE index, converts the
respelling, and scores it against the curated IPA with the same folded
similarity the verifier uses.
"""
import json
import os
import random
import sys

sys.path.insert(0, r"C:\Dev\AV Bible")
os.chdir(r"C:\Dev\AV Bible")
import ipa_asr        # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from isbe_to_ipa import convert                     # noqa: E402
from isbe_harvest import fetch, parse_entry, title_parts, norm  # noqa: E402

with open("pronunciations.json", encoding="utf-8") as f:
    names = json.load(f)["names"]
with open(os.path.join(HERE, "isbe_index.json"), encoding="utf-8") as f:
    entries = json.load(f)

lookup = {}
for title, letter, slug in entries:
    parts = title_parts(title)
    for i, p in enumerate(parts):
        lookup.setdefault(p, (letter, slug, i, len(parts)))

curated = [(k, v) for k, v in names.items()
           if v.get("ipa") and v.get("ipa_src") in (None, "", "curated")
           and "ipa_src" not in v or
           (v.get("ipa") and not v.get("ipa_src"))]
curated = [(k, v) for k, v in names.items()
           if v.get("ipa") and not v.get("ipa_src")]
random.seed(7)
random.shuffle(curated)

scores, misses = [], 0
worst = []
for name, info in curated:
    if len(scores) >= 150:
        break
    hit = lookup.get(norm(name))
    if not hit:
        misses += 1
        continue
    letter, slug, idx, nparts = hit
    body = fetch(f"{letter}/{slug}.html")
    if not body:
        misses += 1
        continue
    _, res = parse_entry(body)
    if not res:
        misses += 1
        continue
    r = res[idx] if idx < len(res) and len(res) >= nparts else res[0]
    ipa = convert(r)
    s = ipa_asr.similarity(info["ipa"], ipa)
    scores.append(s)
    worst.append((s, name, r, ipa, info["ipa"]))

worst.sort()
print(f"n={len(scores)}  mean={sum(scores)/len(scores):.3f}  "
      f"(generator baseline 0.72, voice 0.77)")
print("worst 12:")
for s, name, r, ipa, ref in worst[:12]:
    print(f"  {s:.2f} {name}: isbe {r} -> {ipa}  vs curated {ref}")
