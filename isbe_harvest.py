"""Harvest pronunciation respellings from the online ISBE (1915, public domain).

Phase 1: fetch the 26 per-letter index pages -> title/slug map.
Phase 2: match the project's guessed-IPA names against entry titles.
Phase 3: fetch each matched entry page, parse the leading respelling from the
         first paragraph (e.g. "a-da-li'-a (...)"), save raw harvest JSON.

Politeness: one request every 0.3 s, a real User-Agent, and nothing fetched
twice (responses cached on disk so a re-run is free).
"""
import html
import json
import os
import re
import string
import sys
import time
import unicodedata
import urllib.request

BASE = "https://www.internationalstandardbible.com"
OUT = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(OUT, "isbe_cache")
PRON_JSON = r"C:\Dev\AV Bible\pronunciations.json"
UA = {"User-Agent": "Mozilla/5.0 (pronunciation research; contact dmwhit5988@gmail.com)"}

os.makedirs(CACHE, exist_ok=True)


def fetch(path):
    """GET BASE/path with an on-disk cache; returns text or None on 404."""
    key = path.replace("/", "_")
    cpath = os.path.join(CACHE, key)
    if os.path.exists(cpath):
        with open(cpath, encoding="utf-8") as f:
            body = f.read()
        return None if body == "\x00404" else body
    req = urllib.request.Request(f"{BASE}/{path}", headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            with open(cpath, "w", encoding="utf-8") as f:
                f.write("\x00404")
            time.sleep(0.3)
            return None
        raise
    with open(cpath, "w", encoding="utf-8") as f:
        f.write(body)
    time.sleep(0.3)
    return body


# ---------------------------------------------------------------- phase 1
def build_index():
    entries = []  # (title, letter, slug)
    for letter in string.ascii_uppercase:
        body = fetch(f"{letter}/index.html")
        if body is None:
            print(f"  {letter}: no index!", flush=True)
            continue
        found = re.findall(r'<a href="([a-z0-9-]+\.html)">([^<]+)</a>', body)
        for slug, title in found:
            entries.append((html.unescape(title).strip(), letter, slug[:-5]))
        print(f"  {letter}: {len(found)} entries", flush=True)
    return entries


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.lower().strip()


def title_parts(title):
    """'Sabaco; Sabakon' -> ['sabaco','sabakon']; strip '(1)' qualifiers."""
    t = re.sub(r"\([^)]*\)", "", title)
    return [norm(p) for p in re.split(r"[;,]", t) if norm(p)]


# ---------------------------------------------------------------- phase 3
# A respelling token: syllables of letters joined by hyphens, with apostrophe
# stress marks, e.g. a-da-li'-a  or  shoo'-the-la.  Single-syllable ones
# (e.g. "kush") exist too but are indistinguishable from ordinary words, so we
# require either a hyphen or an apostrophe.
RESPELL = re.compile(r"^[a-zA-Z]+(?:['\u2019-][a-zA-Z']*)+")


def parse_entry(body):
    """Return (h1, [respellings]) from an entry page."""
    m = re.search(r"<h1>([^<]+)</h1>", body)
    h1 = html.unescape(m.group(1)).strip() if m else ""
    m = re.search(r'<p class="i0">(.*?)</p>', body, re.S)
    if not m:
        return h1, []
    text = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip()
    # Pronunciations come before the first '(' (which opens the transliteration)
    # or ':' — e.g. "a-da-li'-a ('adhalya', ...):" or "shoo'-the-la, ... :"
    head = re.split(r"[(:]", text, 1)[0]
    out = []
    for chunk in head.split(","):
        chunk = chunk.strip().replace("\u2019", "'")
        m2 = RESPELL.match(chunk)
        if m2:
            out.append(m2.group(0))
    return h1, out


def main():
    with open(PRON_JSON, encoding="utf-8") as f:
        names = json.load(f)["names"]
    targets = [k for k, v in names.items()
               if v.get("ipa_src") == "generated" or not v.get("ipa")]
    print(f"{len(targets)} target names", flush=True)

    print("Building ISBE index…", flush=True)
    entries = build_index()
    with open(os.path.join(OUT, "isbe_index.json"), "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=0)
    print(f"{len(entries)} total entries", flush=True)

    # part-of-title -> (letter, slug, part_index, n_parts, title)
    lookup = {}
    for title, letter, slug in entries:
        for i, p in enumerate(title_parts(title)):
            lookup.setdefault(p, (letter, slug, i, len(title_parts(title)), title))

    matched, unmatched = {}, []
    for name in targets:
        key = norm(name)
        hit = lookup.get(key)
        if hit is None and key.endswith("s"):        # Danites -> Danite
            hit = lookup.get(key[:-1])
        if hit is None and not key.endswith("s"):    # Ithrite -> Ithrites
            hit = lookup.get(key + "s")
        if hit is None:
            unmatched.append(name)
        else:
            matched[name] = hit
    print(f"matched {len(matched)}, unmatched {len(unmatched)}", flush=True)

    # Fetch the matched pages and parse.
    harvest, misses = {}, []
    slugs_done = {}
    for i, (name, (letter, slug, idx, nparts, title)) in enumerate(sorted(matched.items())):
        if slug not in slugs_done:
            body = fetch(f"{letter}/{slug}.html")
            slugs_done[slug] = parse_entry(body) if body else ("", [])
            if (i % 50) == 0:
                print(f"  [{i}/{len(matched)}] {name}", flush=True)
        h1, res = slugs_done[slug]
        if not res:
            misses.append(name)
            continue
        # If the entry lists as many respellings as headword parts, take the
        # matching one; otherwise fall back to the first.
        r = res[idx] if idx < len(res) and len(res) >= nparts else res[0]
        harvest[name] = {"respell": r, "title": title, "slug": f"{letter}/{slug}",
                         "all": res, "part": idx, "nparts": nparts}

    with open(os.path.join(OUT, "isbe_harvest.json"), "w", encoding="utf-8") as f:
        json.dump({"harvest": harvest, "unmatched": unmatched,
                   "no_respell": misses}, f, ensure_ascii=False, indent=1)
    print(f"harvested {len(harvest)}; no respelling on page for {len(misses)}; "
          f"no entry for {len(unmatched)}", flush=True)


if __name__ == "__main__":
    main()
