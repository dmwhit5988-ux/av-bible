"""Regenerate PRONUNCIATION_TODO.md from pronunciations.json + the check cache.

Run after a verifier sweep changes verdicts:
    .venv/Scripts/python.exe regen_pronunciation_todo.py
"""
import json
import os

import config
import pronunciation

CACHE_PATH = os.path.join(config.CACHE_DIR, "ipa_checks.json")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "PRONUNCIATION_TODO.md")

SRC_LABEL = {
    "": "curated", None: "curated", "cmudict": "CMUdict", "isbe": "ISBE (1915)",
    "wiktionary": "Wiktionary", "wikipedia": "Wikipedia",
    "generated": "generated guess",
}


def main():
    names = pronunciation.load(force=True)
    try:
        with open(CACHE_PATH, encoding="utf-8") as f:
            cache = json.load(f)
    except (OSError, ValueError):
        cache = {}

    by_status = {}
    for name, info in names.items():
        by_status.setdefault(pronunciation.status_of(info), []).append(name)

    def heard(name):
        r = cache.get(name)
        return (r or {}).get("heard", "")

    def rows(status, limit):
        got = sorted(by_status.get(status, []),
                     key=lambda n: names[n].get("score") or 0)
        out = []
        for n in got[:limit]:
            i = names[n]
            out.append(f"| **{n}** | {i.get('ipa','')} | "
                       f"{SRC_LABEL.get(i.get('ipa_src'), i.get('ipa_src'))} | "
                       f"`{heard(n)}` | {i.get('score') or 0:.2f} |")
        return out, len(got)

    src_counts = {}
    for info in names.values():
        k = SRC_LABEL.get(info.get("ipa_src"), info.get("ipa_src"))
        src_counts[k] = src_counts.get(k, 0) + 1

    lines = [
        "# Pronunciation to-do — whole canon",
        "",
        f"Every proper noun in the WEB text has been checked against real "
        f"audio. The list holds {len(names)} names; this file is what "
        f"checking could **not** settle.",
        "",
        "| Verdict | Names |",
        "| --- | --- |",
    ]
    for st in pronunciation.STATUS_ORDER:
        lines.append(f"| {pronunciation.STATUS_LABELS[st]} | "
                     f"{len(by_status.get(st, []))} |")
    lines += [
        "",
        "## Where the references come from",
        "",
        "| Reference | Names |",
        "| --- | --- |",
    ]
    for k in ("curated", "ISBE (1915)", "CMUdict", "Wiktionary", "Wikipedia",
              "generated guess"):
        if k in src_counts:
            lines.append(f"| {k} | {src_counts[k]} |")
    lines += [
        "",
        "The ISBE references were harvested from the International Standard "
        "Bible Encyclopedia (1915, public domain) — headword respellings like "
        "`a-da-li'-a`, converted to IPA (`isbe_harvest.py` → `isbe_to_ipa.py` "
        "→ `isbe_apply.py`). Measured against 150 curated references the "
        "conversion agrees 0.91 — well above the 0.72 rule-generator it "
        "replaced, so these are real references, judged accordingly "
        "(ok / still wrong, not unsure).",
        "",
        "**Known acoustic blind spot:** a hyphenated pure-vowel segment in a "
        "respelling (`ee-mim`, `el-a-sar`) is read out letter-by-letter but "
        "transcribes as a clean long vowel, so a score alone cannot clear "
        "such a spelling. `isbe_sweep.py`/`isbe_repair.py` refuse to emit "
        "them; older hand-tuned overrides that still carry one are listed at "
        "the bottom for the ear.",
        "",
        "## Still wrong — worth acting on",
        "",
        "Judged against a sourced reference; no tested respelling fixed them.",
        "",
        "| Name | Reference | Source | Voice says | Score |",
        "| --- | --- | --- | --- | --- |",
    ]
    r, total = rows(pronunciation.STATUS_UNFIXED, 200)
    lines += r
    if total > 200:
        lines.append(f"\n_…and {total - 200} more; filter to \"Still wrong\" "
                     f"in the Pronunciation Studio for the full set._")
    lines += [
        "",
        "## Suggestions waiting",
        "",
        "A better spelling is recorded in `say` but not applied "
        "(`override:false`) — it beat the plain reading without clearing the "
        "adoption bar, or a repair could not hold its score. These want an "
        "ear in the Studio.",
        "",
        "| Name | Reference | Source | Voice says | Score |",
        "| --- | --- | --- | --- | --- |",
    ]
    r, total = rows(pronunciation.STATUS_SUGGESTED, 200)
    lines += r
    if total > 200:
        lines.append(f"\n_…and {total - 200} more._")

    # Old overrides that still carry the letter-by-letter trap
    import re
    pv = re.compile(r"^[aeiou]+$")
    risky = [(n, i.get("say")) for n, i in names.items()
             if i.get("override") and any(
                 pv.match(s) for s in (i.get("say") or "").lower().split("-"))]
    if risky:
        lines += [
            "",
            "## Overrides that still carry a pure-vowel hyphen segment",
            "",
            "Pre-existing hand-tuned spellings the automated repair did not "
            "touch. The scorer cannot judge these — only the ear can.",
            "",
            "| Name | Say |",
            "| --- | --- |",
        ]
        for n, s in sorted(risky):
            lines.append(f"| {n} | `{s}` |")

    unsure = len(by_status.get(pronunciation.STATUS_UNSURE, []))
    lines += [
        "",
        f"## Unsure — {unsure} names still on a generated guess",
        "",
        "No entry in ISBE, CMUdict, Wiktionary or Wikipedia. A low score here "
        "is as likely to mean the guess is wrong as the voice. Closing these "
        "means listening.",
        "",
        "---",
        "",
        "_Generated by `regen_pronunciation_todo.py` from a whole-canon "
        "verifier sweep of the WEB text (1189 chapters, voice "
        "en-US-AndrewNeural). Scores are two-carrier averages._",
    ]
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
