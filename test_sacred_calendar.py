"""sacred_calendar.py and the Sacred year page: every ref is a WEB verse,
every card's words are WEB's own, the months and feasts are dated as their
verses date them, and the files on disk are what the generator writes.

    .venv\\Scripts\\python.exe -m unittest test_sacred_calendar
"""

import glob
import json
import os
import re
import unittest

import generate_sacred_year_reference as G
import reference_viewer
import sacred_calendar as SC
import verse_refs
from config import BIBLES_DIR

TEXT = {}
for _p in glob.glob(os.path.join(BIBLES_DIR, "WEB", "*.json")):
    _d = json.load(open(_p, encoding="utf-8"))
    for _n, _t in _d["verses"]:
        TEXT[(_d["book"], _d["chapter"], int(_n))] = _t


def words(*refs):
    return " ".join(TEXT[v] for ref in refs for r in verse_refs.parse(ref, None)
                    for v in r.verses())


def norm(t):
    t = t.replace("’", "'").replace("‘", "'").replace("“", '"') \
        .replace("”", '"')
    return re.sub(r"\s+", " ", t).lower()


ORD = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth",
       "tenth", "eleventh", "twelfth", "thirteenth", "fourteenth", "fifteenth", "sixteenth",
       "seventeenth", "eighteenth", "nineteenth", "twentieth", "twenty-first", "twenty-second",
       "twenty-third", "twenty-fourth", "twenty-fifth", "twenty-sixth", "twenty-seventh"]
NUM = {13: "thirteen", 12: "twelve", 11: "eleven", 10: "ten", 9: "nine", 8: "eight",
       7: "seven", 1: "one"}


def all_refs():
    """(where, ref string) for every ref in the module."""
    out = []

    def note(w, n):
        if n:
            out.extend((w, r) for r in n.refs)

    def card(w, c):
        out.extend((w, r) for r in c.refs)
    for m in SC.MONTHS:
        for nm in m.names:
            out.extend((nm.name, r) for r in nm.refs + nm.numbered_by)
            note(nm.name, nm.note)
    for f in SC.FEASTS + (SC.DAILY,):
        out.extend((f.key, r) for r in f.refs + f.nt_refs + f.offerings_by_day_refs)
        out.extend((f.key, r) for _n, r in f.aka_refs)
        for n in (f.rest, f.farming, f.offerings_note, f.date_note, f.pilgrim_note, f.name_note):
            note(f.key, n)
        card(f.key, f.card)
    for f in SC.FARMING:
        out.extend((f.key, r) for r in f.refs)
        note(f.key, f.basis_note)
        card(f.key, f.card)
    for e in SC.DATED_EVENTS:
        out.extend((e.key, r) for r in (e.ref,) + e.also)
        card(e.key, e.card)
    for j in SC.JOHN + SC.ACTS:
        out.append((j.label, j.ref))
    for y in SC.YEARS:
        out.extend((y.key, r) for r in y.refs)
        out.extend((y.key, r) for _n, r in y.aka_refs)
        for rule in y.rules:
            out.extend((rule.label, r) for r in rule.refs)
        card(y.key, y.card)
        if y.trumpet:
            out.append((y.key, y.trumpet[2]))
            card(y.key, y.trumpet[3])
    for k, n in SC.NOTES.items():
        note(k, n)
    out.extend((k, r) for k, (r, _w) in SC.DEFINED.items())
    out.extend((name, r) for _m, name, r in SC.DIVISIONS)
    out.extend(("three times", r) for r in SC.THREE_TIMES.refs + SC.THREE_TIMES_CARD.refs)
    return out


def cards():
    out = [(f.key, f.card) for f in SC.FEASTS + (SC.DAILY,)]
    out += [(f.key, f.card) for f in SC.FARMING]
    out += [(e.key, e.card) for e in SC.DATED_EVENTS]
    out += [(y.key, y.card) for y in SC.YEARS]
    out += [("trumpet", SC.YEAR["jubilee"].trumpet[3]), ("three", SC.THREE_TIMES_CARD)]
    return out


_BUILT = {}


def built():
    if not _BUILT:
        svg, boxes = G.build_svg()
        _BUILT.update(svg=svg, data=json.loads(json.dumps(G.sidecar(boxes), ensure_ascii=False)))
    return _BUILT


class Verses(unittest.TestCase):
    def test_every_ref_is_a_web_verse(self):
        refs = all_refs()
        self.assertGreater(len(refs), 400)
        for where, ref in refs:
            with self.subTest(where=where, ref=ref):
                self.assertTrue(verse_refs.parse(ref, None))

    def test_cards_are_webs_words(self):
        """Each fragment of a card is found, word for word, in its verses."""
        for key, c in cards():
            text = norm(words(*c.refs))
            for w in c.words:
                with self.subTest(key=key, words=w[:40]):
                    self.assertIn(norm(w).strip(" .;,"), text)

    def test_john_and_acts_quote_their_verse(self):
        for j in SC.JOHN + SC.ACTS:
            text = norm(words(j.ref))
            for w in j.card.split(" … "):
                with self.subTest(j.ref):
                    self.assertIn(norm(w).strip(" .;,!“”\""), text)
            if j.feast:
                self.assertIn(j.feast, SC.FEAST)


class Months(unittest.TestCase):
    def test_twelve_from_abib(self):
        self.assertEqual([m.n for m in SC.MONTHS], list(range(1, 13)))
        self.assertEqual(SC.month_names(1), "Abib · Nisan")
        self.assertEqual(SC.month_names(4), "")
        self.assertEqual(SC.month_names(5), "")

    def test_names_are_spelled_as_web_spells_them(self):
        """Every verse a name lists has the name as a whole word, and every
        verse that numbers it has the name and the month's number."""
        for m in SC.MONTHS:
            for nm in m.names:
                for ref in nm.refs:
                    with self.subTest(name=nm.name, ref=ref):
                        self.assertRegex(words(ref), r"\b%s\b" % nm.name)
                if nm.name == "Abib":
                    continue
                for ref in nm.numbered_by:
                    with self.subTest(name=nm.name, numbered_by=ref):
                        t = words(ref)
                        self.assertRegex(t, r"\b%s\b" % nm.name)
                        self.assertIn(f"{ORD[m.n - 1]} month", t.lower())

    def test_abib_is_the_first_month(self):
        self.assertIn("first month of the year", words("Exod 12:2"))
        self.assertIn("month Abib", words("Exod 13:4"))

    def test_elul_is_never_numbered(self):
        elul = [nm for m in SC.MONTHS for nm in m.names if nm.name == "Elul"][0]
        self.assertEqual(elul.numbered_by, ())
        self.assertIsNotNone(elul.note)

    def test_davids_captains(self):
        self.assertEqual([d[0] for d in SC.DIVISIONS], list(range(1, 13)))
        for m, name, ref in SC.DIVISIONS:
            with self.subTest(ref):
                t = words(ref)
                self.assertIn(name, t)
                self.assertIn(f"{ORD[m - 1]} month", t)


class Feasts(unittest.TestCase):
    def test_names_are_webs(self):
        for f in SC.FEASTS:
            text = norm(words(*f.refs + f.nt_refs))
            for name in (f.name,) + f.aka:
                with self.subTest(feast=f.key, name=name):
                    self.assertIn(norm(name), text)
            for name, ref in f.aka_refs:
                with self.subTest(feast=f.key, aka=name):
                    self.assertIn(norm(name), norm(words(ref)))

    def test_days_are_the_verses_days(self):
        """The words that set each feast are in its defining verse, and the
        month and day on FEASTS are those words'."""
        for key, (ref, ws) in SC.DEFINED.items():
            t = norm(words(ref))
            for w in ws:
                with self.subTest(key=key, words=w):
                    self.assertIn(norm(w), t)
            f = SC.FEAST[key]
            # the day by its ordinal (the eighth day is the feast's own count,
            # the new moon "the beginnings of your months")
            if f.day and key not in ("eighth_day", "new_moon"):
                self.assertRegex(t, rf"\b{ORD[f.day - 1]} (?:and [a-z]+ )?days?\b", key)
            # the month where the verse numbers it (the rest say "the same
            # month", "this seventh month" or "Adar", or give none)
            if key in ("passover", "trumpets", "second_passover"):
                self.assertIn(ORD[f.month - 1] + " month", t, key)
            if key in ("tents", "atonement"):
                self.assertIn("this " + ORD[f.month - 1] + " month", t, key)
        self.assertEqual((SC.FEAST["passover"].month, SC.FEAST["passover"].day), (1, 14))
        self.assertEqual((SC.FEAST["unleavened_bread"].day, SC.FEAST["unleavened_bread"].days),
                         (15, 7))
        self.assertEqual((SC.FEAST["trumpets"].month, SC.FEAST["trumpets"].day), (7, 1))
        self.assertEqual((SC.FEAST["atonement"].month, SC.FEAST["atonement"].day), (7, 10))
        self.assertEqual((SC.FEAST["tents"].month, SC.FEAST["tents"].day,
                          SC.FEAST["tents"].days), (7, 15, 7))
        self.assertEqual(SC.FEAST["eighth_day"].day, 15 + 7)
        self.assertEqual((SC.FEAST["second_passover"].month, SC.FEAST["second_passover"].day),
                         (2, 14))
        self.assertTrue(SC.FEAST["weeks"].counted)
        self.assertIsNone(SC.FEAST["weeks"].day)

    def test_three_pilgrim_feasts(self):
        self.assertEqual({f.key for f in SC.FEASTS if f.pilgrim},
                         {"unleavened_bread", "weeks", "tents"})
        t = words("Deut 16:16")
        for name in ("feast of unleavened bread", "feast of weeks", "feast of tents"):
            self.assertIn(name, t)

    def test_tents_bulls_run_thirteen_to_seven_then_one(self):
        f = SC.FEAST["tents"]
        self.assertEqual([o.bulls for o in f.offerings_by_day], [13, 12, 11, 10, 9, 8, 7, 1])
        self.assertEqual({(o.rams, o.lambs, o.goats) for o in f.offerings_by_day[:7]},
                         {(2, 14, 1)})
        for o, ref in zip(f.offerings_by_day, f.offerings_by_day_refs):
            with self.subTest(ref):
                t = words(ref).lower()
                self.assertTrue(f"{NUM[o.bulls]} young bull" in t or
                                f"{NUM[o.bulls]} bull" in t, ref)
        self.assertEqual(SC.FEAST["eighth_day"].offerings, f.offerings_by_day[7])
        self.assertEqual(f.offerings.row(), "Bulls 13, rams 2, lambs 14, goat 1")

    def test_weeks_offerings_as_each_book_gives_them(self):
        f = SC.FEAST["weeks"]
        self.assertEqual((f.offerings.bulls, f.offerings.rams), (2, 1))
        self.assertIn("two young bulls, one ram", words("Num 28:27"))
        self.assertEqual((f.offerings_lev23.bulls, f.offerings_lev23.rams), (1, 2))
        self.assertIn("one young bull, and two rams", words("Lev 23:18"))

    def test_tents_is_webs_name(self):
        self.assertEqual(SC.FEAST["tents"].name, "feast of tents")
        self.assertIn(("Feast of Booths", "John 7:2"), SC.FEAST["tents"].aka_refs)
        self.assertIn(("feast of harvest", "Exod 23:16"), SC.FEAST["weeks"].aka_refs)


class Farming(unittest.TestCase):
    def test_drawn_spans(self):
        for f in SC.FARMING:
            with self.subTest(f.key):
                self.assertIn(f.basis, ("stated", "derived", "season"))
                for m0, d0, m1, d1, basis in f.drawn:
                    self.assertIn(basis, ("stated", "derived", "convention"))
                    # a month joined from several verses is never "stated"
                    if f.basis == "derived":
                        self.assertNotEqual(basis, "stated")
                    self.assertTrue(1 <= m0 <= 12 and 1 <= m1 <= 12 and 1 <= d0 <= 30 and
                                    1 <= d1 <= 30)
                    # the text never dates a season-only entry
                    if f.basis == "season":
                        self.assertEqual(basis, "convention")


class Events(unittest.TestCase):
    def test_months_and_days_are_the_cards(self):
        """Where a card names a month or a day, one of them is the event's."""
        for e in SC.DATED_EVENTS:
            t = norm(" ".join(e.card.words))
            months = {ORD.index(w) + 1 for w in re.findall(r"\b([a-z-]+) month\b", t)
                      if w in ORD}
            with self.subTest(e.key):
                if months and e.month and not e.months:
                    self.assertIn(e.month, months | ({e.month_end} if e.month_end else set()))
                # "the fourteenth and fifteenth days" names both
                days = {ORD.index(w) + 1 for w in
                        re.findall(r"\b([a-z-]+)(?= (?:and [a-z-]+ )?days?\b)", t) if w in ORD}
                if days and e.day:
                    self.assertIn(e.day, days | ({e.day_end} if e.day_end else set()))

    def test_keys_and_stories(self):
        keys = [e.key for e in SC.DATED_EVENTS]
        self.assertEqual(len(set(keys)), len(keys))
        for e in SC.DATED_EVENTS:
            self.assertIn(e.story, SC.STORIES)
        # a day with no month: Ezekiel 26:1 and 32:17, and 40:1's "beginning
        # of the year"
        self.assertEqual({e.key for e in SC.DATED_EVENTS if e.month is None},
                         {"ezekiel_26", "ezekiel_32_17", "ezekiel_40"})
        self.assertIn("in the beginning of the year", words("Ezek 40:1"))

    def test_a_month_is_its_own_verses_or_marked(self):
        """An event's own verse numbers its month or names it, unless
        `month_from` says the month is carried from elsewhere."""
        # a name counts where WEB numbers it (so not Elul)
        names = {nm.name: m.n for m in SC.MONTHS for nm in m.names if nm.numbered_by}
        for e in SC.DATED_EVENTS:
            if e.month is None:
                continue
            self.assertIn(e.month_from, ("", "context", "calendar"), e.key)
            t = words(e.ref)
            if e.months:
                # "the fasts of the fourth, fifth, seventh, and tenth months"
                given = all(re.search(r"\b%s\b" % ORD[m - 1], t) for m in e.months)
            else:
                given = (f"{ORD[e.month - 1]} month" in t.lower() or
                         any(names[n] == e.month and re.search(r"\b%s\b" % n, t)
                             for n in names))
            with self.subTest(e.key):
                if e.key == "law_studied":
                    # Neh 8:14's "the feast of the seventh month" names the
                    # feast; the day of 8:13 ("On the second day") has none
                    self.assertEqual(e.month_from, "context")
                elif e.month_from:
                    self.assertFalse(given, "marked carried, but the verse gives its month")
                else:
                    self.assertTrue(given, "the verse doesn't give its month")

    def test_hezekiah_the_first_day_is_the_sanctifying(self):
        e = SC.EVENT["hezekiah_begins"]
        self.assertEqual((e.month, e.day), (1, 1))
        self.assertIn("began on the first day of the first month to sanctify", words(e.ref))
        self.assertNotIn("first day", words("2 Chr 29:3"))

    def test_kings_and_jeremiah_differ(self):
        self.assertEqual((SC.EVENT["temple_burned"].day, SC.EVENT["temple_burned"].day_alt),
                         (7, 10))
        self.assertIn("seventh day", words("2 Kgs 25:8"))
        self.assertIn("tenth day", words("Jer 52:12"))


class Years(unittest.TestCase):
    def test_jubilee_on_the_day_of_atonement(self):
        j = SC.YEAR["jubilee"]
        self.assertEqual(j.every, 50)
        m, d, ref, _card = j.trumpet
        self.assertEqual((m, d), (SC.FEAST["atonement"].month, SC.FEAST["atonement"].day))
        self.assertIn("Day of Atonement", words(ref))
        self.assertEqual(SC.YEAR["sabbath_year"].every, 7)


class Page(unittest.TestCase):
    def test_files_on_disk_are_what_the_generator_writes(self):
        b = built()
        with open(os.path.join(G.OUT_DIR, G.STEM + ".svg"), encoding="utf-8") as f:
            self.assertEqual(f.read(), b["svg"])
        with open(os.path.join(G.OUT_DIR, G.STEM + ".json"), encoding="utf-8") as f:
            self.assertEqual(json.load(f), b["data"])
        with open(os.path.join(G.OUT_DIR, G.STEM + ".html"), encoding="utf-8") as f:
            self.assertEqual(f.read(), G.viewer_page())

    def test_the_page_is_the_current_viewer(self):
        fixed = re.split(r"__(?:TITLE|PLACEHOLDER|W|H|DATA|STEM)__", reference_viewer._PAGE)
        whole = re.compile(".*?".join(map(re.escape, fixed)), re.S)
        with open(os.path.join(G.OUT_DIR, G.STEM + ".html"), encoding="utf-8") as f:
            self.assertTrue(whole.fullmatch(f.read()))

    def test_three_files(self):
        files = glob.glob(os.path.join(G.OUT_DIR, G.STEM + ".*"))
        self.assertEqual(sorted(os.path.basename(p) for p in files),
                         ["Sacred_year.html", "Sacred_year.json", "Sacred_year.svg"])

    def test_sidecar(self):
        d = built()["data"]
        items = d["items"]
        ids = [it["id"] for it in items]
        self.assertEqual(len(set(ids)), len(ids))
        layers = {l["id"] for l in d["layers"]}
        self.assertEqual(layers, {"feasts", "farming", "events", "john"})
        for it in items:
            with self.subTest(it["id"]):
                self.assertEqual(len(it["b"]), 4)
                if it.get("ly"):
                    self.assertIn(it["ly"], layers)
                for j in it.get("see", []):
                    self.assertLess(j, len(items))
        for t in d["tours"]:
            self.assertTrue(t["stops"])
            for s in t["stops"]:
                self.assertLess(s["i"], len(items))
        self.assertEqual([v["id"] for v in d["views"]], ["year", "jubilee"])
        # every feast, month, farming entry, dated day (but David's
        # divisions, on the month cards) and John's mark has a card
        for want in (["month-%d" % n for n in range(1, 13)] +
                     [f.key.replace("_", "-") for f in SC.FEASTS] +
                     ["farm-" + f.key.replace("_", "-") for f in SC.FARMING] +
                     ["day-" + e.key.replace("_", "-") for e in SC.DATED_EVENTS
                      if e.key != "davids_divisions"] +
                     ["john-2-13", "john-5-1", "john-6-4", "john-7-2", "john-10-22-23",
                      "john-11-55", "jubilee", "sabbath-year", "jubilee-trumpet"]):
            self.assertIn(want, ids)

    def test_dated_flag_is_the_months(self):
        """A card says 'stated' only where its own verse gives the month and
        the day; a month carried from elsewhere is 'derived'."""
        d = built()["data"]
        by_id = {it["id"]: it for it in d["items"]}
        for e in SC.DATED_EVENTS:
            it = by_id.get("day-" + e.key.replace("_", "-"))
            if not it:
                continue
            flag = it["dims"][0][2]
            with self.subTest(e.key):
                if e.month is None:
                    self.assertEqual(flag, "not given")
                elif e.month_from:
                    self.assertEqual(flag, "derived")
                elif e.day:
                    self.assertEqual(flag, "stated")

    def test_rim_dots_of_two_kinds_never_stack(self):
        """Month-only dots stand clear of the dated days, so no leader for a
        dated day ends on a month-only stack."""
        dots = G.event_dots()
        filled = [a for a, _k, f, _l in dots if f]
        for a, key, f, _l in dots:
            if not f:
                with self.subTest(key):
                    self.assertGreaterEqual(min(abs(a - x) for x in filled), G.CLEAR)
        level, top = G.stacks(dots)
        for i, (a, _k, f, _l) in enumerate(dots):
            mates = [j for j, (b, _k2, f2, _l2) in enumerate(dots) if abs(a - b) < G.NEAR]
            self.assertTrue(all(dots[j][2] == f for j in mates))
            self.assertEqual(top[i], max(level[j] for j in mates))
        # one dot per event and month: the other book's day is in the label
        self.assertEqual(sum(1 for d in dots if d[1] == "temple_burned"), 1)
        self.assertIn("7 or 10 · temple burned", built()["svg"])

    def test_frames_stay_on_the_sheet(self):
        d = built()["data"]
        for it in d["items"]:
            if "fr" in it:
                x, y, w, h = it["fr"]
                with self.subTest(it["id"]):
                    self.assertTrue(x >= 0 and y >= 0 and x + w <= G.W + 0.1 and
                                    y + h <= G.H + 0.1)

    def test_at_finds_what_a_verse_names(self):
        """#at opens on what the verse names: the viewer's own rule, a
        single verse first, then a range."""
        d = built()["data"]
        items, books = d["items"], d["books"]

        def at(book, c, v):
            b = books.index(book)

            def inr(r):
                _b, c1, v1, c2, v2 = r
                ce = c2 or c1
                if not v1:
                    return c1 <= c <= ce
                if c < c1 or c > ce or (c == c1 and v < v1):
                    return False
                ve = v2 or (10 ** 9 if c2 else v1)
                return not (c == ce and v > ve)

            def single(r):
                return r[2] and not r[3] and not r[4]

            def named(test):
                return {it["id"] for it in items if not it.get("nos") and
                        any(r[0] == b and test(r) for r in it["r"])}
            return named(lambda r: single(r) and inr(r)) or named(lambda r: not single(r) and inr(r))
        self.assertEqual(at("Leviticus", 23, 5), {"passover"})
        self.assertIn("weeks", at("Leviticus", 23, 16))
        self.assertEqual(at("Leviticus", 23, 27), {"atonement"})
        self.assertEqual(at("Numbers", 29, 20), {"tents"})
        self.assertEqual(at("Numbers", 29, 36), {"eighth-day"})
        self.assertIn("passover-egypt".replace("passover-egypt", "day-passover-egypt"),
                      at("Exodus", 12, 6))
        self.assertIn("purim", at("Esther", 9, 21))
        self.assertIn("jubilee-trumpet", at("Leviticus", 25, 9))
        self.assertEqual(at("Haggai", 2, 10), {"day-from-today-bless"})


if __name__ == "__main__":
    unittest.main()
