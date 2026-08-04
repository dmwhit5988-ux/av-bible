"""Apply the ISBE harvest to pronunciations.json.

Only entries whose reference is a rule-based guess (ipa_src == "generated") or
missing get a new IPA; sourced references (curated/cmudict/wiktionary/
wikipedia) are never overwritten -- the weaker source must not judge the
stronger. Status/score are cleared: the old verdict was measured against the
old reference and is stale. The verifier sweep re-measures next.
"""
import json
import os
import sys

sys.path.insert(0, r"C:\Dev\AV Bible")
os.chdir(r"C:\Dev\AV Bible")
import pronunciation  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from isbe_to_ipa import convert  # noqa: E402

with open(os.path.join(HERE, "isbe_harvest.json"), encoding="utf-8") as f:
    data = json.load(f)
harvest = data["harvest"]

names = pronunciation.load(force=True)
applied, skipped, agree = [], [], 0
for name, h in harvest.items():
    info = names.get(name)
    if info is None:
        continue
    src = info.get("ipa_src", "")
    if info.get("ipa") and src not in ("generated", ""):
        skipped.append(name)          # already has a sourced reference
        continue
    # Guard against a combined-headword parse picking up the wrong name's
    # respelling (e.g. "Simon Magus" supplying "ma'-gus" for Simon): the
    # respelling must at least start with the name's own first letter.
    if h["respell"].lstrip("'")[:1].lower() != name[:1].lower():
        skipped.append(name)
        continue
    ipa = convert(h["respell"])
    if len(ipa) <= 4:                 # conversion produced nothing usable
        skipped.append(name)
        continue
    old = info.get("ipa", "")
    import ipa_asr
    if old and ipa_asr.similarity(old, ipa) >= 0.999:
        agree += 1
    info["ipa"] = ipa
    info["ipa_src"] = "isbe"
    # verdict measured against the old guess is meaningless now
    pronunciation.set_status(info, pronunciation.STATUS_UNCHECKED)
    applied.append(name)

pronunciation.save_names(names)
print(f"applied {len(applied)} ISBE references "
      f"({agree} identical to the old guess after folding); "
      f"skipped {len(skipped)} already-sourced")
