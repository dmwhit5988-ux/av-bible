"""The wilderness journey: the camps are Numbers 33's, in its order and
spelling, each verse exists in the WEB, a camp with no site has no point,
the coasts are point facts that meet where they should and copy no
atlas-traced or schematic map, the route keeps to the land but for the
crossing, every verse of the journey's chapters opens on something, and
the page on disk is what the generator writes.

    .venv\\Scripts\\python.exe -m unittest test_wilderness
"""

import functools
import inspect
import json
import math
import os
import re
import unittest

import acts_geography as AG
import gazetteer as GZ
import generate_israel_atlas as A
import generate_wilderness_reference as R
import mediterranean as M
import near_east as NE
import reference_viewer
import sinai as S
import verse_refs
import wilderness as WD
from passages import verse_numbers
from test_gazetteer import _traced_points

POINT = r"^\s+\([\d.]+, [\d.]+\),\s+# (~( .+)?|.+\((Q\d+|[a-z]{2}:[^)]+)\))$"


@functools.lru_cache(maxsize=None)
def built():
    return R.build()


def refs_of_everything():
    """(where, ref string) for every ref the data modules hold."""
    out = []
    for s in WD.STATIONS + list(WD.ENDS.values()):
        for f in ("num33", "refs", "story"):
            if getattr(s, f):
                out.append((f"{s.key}.{f}", getattr(s, f)))
        out += [(f"{s.key}.more", r) for _l, r in s.more]
    cr = WD.CROSSING
    out += [("crossing.num33", cr.num33), ("crossing.refs", cr.refs),
            ("crossing.story", cr.story)]
    out += [(f"event {e.key}", e.refs) for e in WD.EVENTS]
    for d in WD.DATES:
        out.append((f"date {d.ref}", d.ref))
        if d.also:
            out.append((f"date {d.ref} also", d.also))
    for sp in WD.SPANS:
        out.append((f"span {sp.label}", sp.ref))
        if sp.also:
            out.append((f"span {sp.label} also", sp.also))
    out += [(f"variant {v.key}", v.ref) for v in WD.VARIANTS]
    out += [(f"leg {a}-{b}", r) for (a, b), r in WD.LEG_REFS.items()]
    out += [(f"years {k}", r) for k, (r, _t) in WD.YEARS.items()]
    return out


class Data(unittest.TestCase):
    def test_every_ref_parses(self):
        """verse_refs.parse raises on a verse the WEB doesn't have."""
        for where, ref in refs_of_everything():
            with self.subTest(where=where, ref=ref):
                self.assertTrue(verse_refs.parse(ref, "Numbers"))

    def test_forty_two_camps_in_numbers_33s_order(self):
        """Each camp's Numbers 33 verses start where the last camp's end:
        the verse that leaves one camp encamps in the next."""
        self.assertEqual(len(WD.STATIONS), 42)
        self.assertEqual(WD.STATIONS[0].key, "rameses")
        self.assertEqual(WD.STATIONS[-1].key, "plains_of_moab")
        for a, b in zip(WD.STATIONS, WD.STATIONS[1:]):
            with self.subTest(a=a.key, b=b.key):
                self.assertEqual(WD.num33_verses(a)[-1], WD.num33_verses(b)[0])
        self.assertEqual(len({s.key for s in WD.STATIONS}), 42)

    def test_names_are_spelled_as_numbers_33_spells_them(self):
        self.assertEqual(WD.misspelled(), [])
        for s in WD.STATIONS:
            first = WD.num33_verses(s)[0] if s.key != "rameses" else 3
            with self.subTest(s.key):
                self.assertIn(s.name, A.TEXT_WEB[("Numbers", 33, first)])

    def test_each_ref_names_its_camp(self):
        for s in WD.STATIONS + list(WD.ENDS.values()):
            pat = re.compile(A.names_pattern([s.name] + list(s.aka)))
            for v in A.verses(s.refs):
                with self.subTest(camp=s.key, verse=v):
                    self.assertRegex(A.TEXT_WEB[v], pat)

    def test_sites(self):
        for s in WD.STATIONS + list(WD.ENDS.values()):
            with self.subTest(s.key):
                if s.site is None:
                    # a camp that is not identified has no point to be drawn at
                    self.assertIsNone(R.site_point(s.key) if s.key in WD.STATION
                                      and not s.ends else None)
                    continue
                self.assertIn(s.site.certainty, WD.CERTAINTIES)
                self.assertTrue(s.site.qid or s.site.wiki)
                if s.site.qid:
                    self.assertRegex(s.site.qid, r"^Q\d+$")
                self.assertTrue(R.LAT_BOT < s.site.lat < R.LAT_TOP)
                self.assertTrue(R.LON_L < s.site.lon < R.LON_R)
                if s.site.certainty == WD.TRADITIONAL:
                    self.assertTrue(s.site.since, "a traditional site says since when")

    def test_no_camp_without_a_site_has_a_point(self):
        unplaced = [s for s in WD.STATIONS if s.site is None and not s.ends]
        self.assertEqual(len(unplaced), 27)
        for s in unplaced:
            with self.subTest(s.key):
                self.assertIsNone(R.site_point(s.key))
                card = next(it for it in built()["data"]["items"]
                            if it["id"] == s.key.replace("_", "-"))
                self.assertNotIn("dims", card)
                where = dict(card["tx"])["Where"]
                self.assertTrue(where.startswith("Not identified; drawn in its order between"))

    def test_gazetteer_camps_take_gazetteers_point(self):
        for s in WD.STATIONS + list(WD.ENDS.values()):
            if s.site and s.site.gazetteer:
                g = GZ.SITES[s.site.gazetteer]
                with self.subTest(s.key):
                    self.assertEqual((s.site.lat, s.site.lon, s.site.qid, s.site.certainty),
                                     (g.lat, g.lon, g.qid, g.certainty))
        self.assertEqual(WD.STATION["kadesh"].site.gazetteer, "kadesh_barnea")
        self.assertEqual(WD.STATION["dibon_gad"].site.gazetteer, "dibon")

    def test_card_text_is_for_readers(self):
        """Working notes (keys, Wikidata ids, coordinates) stay out of the
        text a card shows."""
        for s in WD.STATIONS + list(WD.ENDS.values()):
            fields = [s.card, s.proposed, s.namesakes, s.differs]
            if s.site:
                fields += [s.site.name, s.site.why, s.site.since]
            for t in fields:
                with self.subTest(camp=s.key, text=t[:40]):
                    self.assertNotRegex(t, r"\b[a-z]+_[a-z_]+\b|\bQ\d+|P625|\d+\.\d{3}")
        for e in WD.EVENTS:
            with self.subTest(event=e.key):
                self.assertLessEqual(len(e.label.split()), 4)
                self.assertNotRegex(e.note, r"\b[a-z]+_[a-z_]+\b")
        for d in WD.DATES:
            for t in (d.card, d.inferred):
                self.assertNotRegex(t, r"\b[a-z]+_[a-z_]+\b|this file", d.ref)

    def test_events_dates_and_spans_point_at_camps(self):
        keys = set(WD.STATION) | {"crossing"}
        for e in WD.EVENTS:
            with self.subTest(e.key):
                at = e.at if isinstance(e.at, tuple) else (e.at,)
                self.assertTrue(set(at) <= keys)
        for d in WD.DATES:
            self.assertIn(d.station, set(WD.STATION) | {"gilgal"}, d.ref)
        for sp in WD.SPANS:
            self.assertTrue(sp.station is None or sp.station in WD.STATION, sp.ref)

    def test_dates_are_in_order_and_whole(self):
        for d in WD.DATES:
            with self.subTest(d.ref):
                self.assertIn(d.year, (1, 2, 40, 41))
                self.assertTrue(d.month is None or 1 <= d.month <= 12)
                self.assertTrue(d.day is None or 1 <= d.day <= 30)
                self.assertEqual(not d.stated, bool(d.inferred))
        keys = [(d.year, d.month or 99, d.day or 0) for d in WD.DATES]
        self.assertEqual(keys, sorted(keys))


class Lines(unittest.TestCase):
    LISTS = ["SUEZ_WEST_SHORE", "SINAI_WEST_SHORE", "SINAI_EAST_SHORE", "ARABIA_EAST_SHORE",
             "TIMSAH", "GREAT_BITTER", "LITTLE_BITTER", "BARDAWIL", "TIRAN", "NILE"]

    def test_every_point_is_a_point_fact(self):
        src = inspect.getsource(S)
        n = 0
        for name in self.LISTS:
            body = re.search(r"\n%s = \[\n(.*?)\n\]" % name, src, re.S).group(1)
            for ln in body.split("\n"):
                if ln.strip().startswith("("):
                    n += 1
                    with self.subTest(list=name, line=ln.strip()):
                        self.assertRegex(ln, POINT)
        self.assertEqual(n, sum(len(getattr(S, k)) for k in self.LISTS))
        wsrc = inspect.getsource(WD)
        for name in ("ROUTE_VIA", "CROSSING_SPAN"):
            body = re.search(r"\n%s = [\[{]\n(.*?)\n[\]}]" % name, wsrc, re.S).group(1)
            for ln in body.split("\n"):
                if re.match(r"\s+\(\d", ln):
                    with self.subTest(list=name, line=ln.strip()):
                        self.assertRegex(ln, POINT)

    def test_points_are_in_a_sane_box(self):
        for name in self.LISTS:
            for lat, lon in getattr(S, name):
                with self.subTest(list=name, point=(lat, lon)):
                    self.assertTrue(26.0 < lat < 32.0 and 30.5 < lon < 36.5)

    def test_no_point_copies_a_traced_or_schematic_map(self):
        banned = _traced_points()
        for n in ("AEGEAN_SHORE", "LIBYA_SHORE", "PELOPONNESE"):
            banned |= {(round(a, 3), round(b, 3)) for a, b in getattr(AG, n)}
        for line in AG.FAR_ISLANDS:
            banned |= {(round(a, 3), round(b, 3)) for a, b in line}
        banned |= {(round(a, 3), round(b, 3)) for a, b in AG.SERMON_SITES.values()}
        banned |= {(round(a, 3), round(b, 3)) for a, b in AG.EDOM_WAY}
        ours = [getattr(S, k) for k in self.LISTS] + list(WD.ROUTE_VIA.values()) + \
            [WD.CROSSING_SPAN]
        ours.append([(s.site.lat, s.site.lon) for s in WD.STATIONS if s.site])
        for p in (q for line in ours for q in line):
            with self.subTest(point=p):
                self.assertNotIn((round(p[0], 3), round(p[1], 3)), banned)

    def test_the_shores_meet(self):
        self.assertEqual(S.SUEZ_WEST_SHORE[-1], S.SINAI_WEST_SHORE[0])        # Port Tawfiq
        self.assertEqual(S.SINAI_WEST_SHORE[-1], S.SINAI_EAST_SHORE[0])       # Ras Muhammad
        self.assertIn(S.SINAI_WEST_SHORE[-1], NE.RED_SEA_EAST)
        self.assertEqual(S.SINAI_EAST_SHORE[-1], S.ARABIA_EAST_SHORE[0])      # Aqaba
        self.assertEqual(S.NILE[-1], (31.5269, 31.8447))
        self.assertIn(S.NILE[-1], M.AFRICA)                                  # Damietta mouth
        self.assertTrue(set(S.BARDAWIL[:6]) <= set(M.AFRICA))
        self.assertEqual(M.AFRICA[0], GZ.COAST[-1])

    def test_the_shores_run_off_the_sheet(self):
        self.assertLess(S.SUEZ_WEST_SHORE[0][0], R.LAT_BOT)
        self.assertLess(S.ARABIA_EAST_SHORE[-1][0], R.LAT_BOT)
        self.assertLess(S.NILE[0][1], R.LON_L)


class Route(unittest.TestCase):
    def setUp(self):
        self.land = R.PROJ.PS(R.land_ring())
        self.water = [R.PROJ.PS(r) for r in R.LAKES]

    def on_land(self, x, y):
        return A.inside(x, y, self.land) and not any(A.inside(x, y, w) for w in self.water)

    def test_the_route_keeps_to_the_land(self):
        """The drawn line, both its parts, runs on land and off the lakes
        and the Salt Sea: the sea is crossed only by the crossing."""
        route = built()["map"].route
        for i, part in enumerate(route.parts):
            for x, y in part["dense"]:
                # the crossing's ends are shore points
                if min(math.dist((x, y), e) for e in route.span) < 12:
                    continue
                with self.subTest(part=i, at=(round(x), round(y))):
                    self.assertTrue(self.on_land(x, y))

    def test_the_crossing_spans_the_sea(self):
        """Its ends are shore points, and the line between is water."""
        self.assertIn(WD.CROSSING_SPAN[0], S.SUEZ_WEST_SHORE)
        self.assertIn(WD.CROSSING_SPAN[-1], S.SINAI_WEST_SHORE)
        (x0, y0), (x1, y1) = built()["map"].route.span
        inner = [(x0 + (x1 - x0) * t / 50, y0 + (y1 - y0) * t / 50) for t in range(3, 48)]
        self.assertFalse(any(self.on_land(x, y) for x, y in inner))

    def test_every_camp_is_on_the_line(self):
        route = built()["map"].route
        for s in WD.STATIONS:
            with self.subTest(s.key):
                part, arc, (x, y) = route.at[s.key]
                if s.site:
                    self.assertLess(math.dist((x, y), R.P(s.site.lat, s.site.lon)), 0.5)
        # in Numbers 33's order along each part
        for i in range(2):
            arcs = [route.at[s.key][1] for s in WD.STATIONS if route.at[s.key][0] == i]
            self.assertEqual(arcs, sorted(arcs))

    def test_beads_are_evenly_spaced(self):
        """A camp with no site stands evenly between the camps either side."""
        route = built()["map"].route
        for s in WD.STATIONS:
            if s.site or s.ends:
                continue
            keys = R.nodes()
            i = keys.index(s.key)
            a = next(k for k in reversed(keys[:i]) if R.site_point(k))
            b = next(k for k in keys[i + 1:] if R.site_point(k))
            inner = keys[keys.index(a) + 1:keys.index(b)]
            sa, sb = route.at[a][1], route.at[b][1]
            if (a, b) in WD.ROUTE_BREAKS:
                # spaced between the camp before and the point the text puts
                # them before
                vi, last = WD.ROUTE_BREAKS[(a, b)]
                inner = inner[:inner.index(last) + 1]
                pt = R.P(*WD.ROUTE_VIA[(a, b)][vi])
                part = route.parts[route.at[a][0]]
                sb = min(zip(part["dense"], part["arc"]),
                         key=lambda q: math.dist(q[0], pt))[1]
            j = inner.index(s.key) + 1
            with self.subTest(s.key):
                self.assertAlmostEqual(route.at[s.key][1], sa + (sb - sa) * j / (len(inner) + 1),
                                       places=6)


def opens(items, books, book, c, v, chapter=True):
    """The items reference_viewer's #at finds for a verse."""
    b = books.index(book)

    def single(r):
        return r[2] and not r[3] and not r[4]

    def in_range(r):
        _b, c1, v1, c2, v2 = r
        ce = c2 or c1
        if not v1:
            return c1 <= c <= ce
        if c < c1 or c > ce or (c == c1 and v < v1):
            return False
        ve = v2 or (math.inf if c2 else v1)
        return not (c == ce and v > ve)

    def named(test):
        return [i for i, it in enumerate(items) if it.get("x") is None and not it.get("nos")
                and any(r[0] == b and test(r) for r in it.get("r", []))]
    hit = named(lambda r: single(r) and in_range(r))
    if not hit:
        hit = named(lambda r: not single(r) and in_range(r))
    if not hit and chapter:
        hit = named(lambda r: r[1] <= c <= (r[3] or r[1]))
    return hit


class Sheet(unittest.TestCase):
    def test_files_on_disk_are_what_the_generator_writes(self):
        b = built()
        out = os.path.join(R.OUT_DIR, R.STEM)
        with open(out + ".svg", encoding="utf-8") as f:
            self.assertEqual(f.read(), b["svg"])
        with open(out + ".json", encoding="utf-8") as f:
            self.assertEqual(json.load(f), json.loads(json.dumps(b["data"])))
        with open(out + ".html", encoding="utf-8") as f:
            self.assertEqual(f.read(), b["html"])

    def test_the_page_is_the_current_viewer(self):
        fixed = re.split(r"__(?:TITLE|PLACEHOLDER|W|H|DATA|STEM)__", reference_viewer._PAGE)
        whole = re.compile(".*?".join(map(re.escape, fixed)), re.S)
        with open(os.path.join(R.OUT_DIR, R.STEM + ".html"), encoding="utf-8") as f:
            self.assertTrue(whole.fullmatch(f.read()))

    def test_three_files_at_most(self):
        files = [f for f in os.listdir(R.OUT_DIR) if f.startswith(R.STEM)]
        self.assertEqual(sorted(files), [R.STEM + e for e in (".html", ".json", ".svg")])

    def test_ids_are_unique_and_links_hold(self):
        items = built()["data"]["items"]
        ids = [it["id"] for it in items]
        self.assertEqual(len(ids), len(set(ids)))
        n = len(items)
        for it in items:
            for j in it.get("see", []) + [j for j in it.get("st", []) if j is not None]:
                self.assertTrue(0 <= j < n, it["id"])
            for _label, href in it.get("ln", []):
                stem, _, part = href.rpartition("#id=")
                with open(os.path.join(R.OUT_DIR, os.path.basename(stem)),
                          encoding="utf-8"):
                    pass
                other = json.load(open(os.path.join(R.OUT_DIR, os.path.basename(stem)
                                                    .replace(".html", ".json")),
                                       encoding="utf-8"))
                self.assertIn(part, {x["id"] for x in other["items"]}, it["id"])

    def test_every_station_has_a_card_and_every_leg_steps(self):
        d = built()["data"]
        items = d["items"]
        by_id = {it["id"]: i for i, it in enumerate(items)}
        for s in WD.STATIONS:
            self.assertIn(s.key.replace("_", "-"), by_id)
        legs = [i for i, it in enumerate(items) if it["id"].startswith("leg-")]
        self.assertEqual(len(legs), 41)
        self.assertEqual(items[legs[0]]["st"][0], None)
        self.assertEqual(items[legs[-1]]["st"][1], None)
        for a, b in zip(legs, legs[1:]):
            self.assertEqual(items[a]["st"][1], b)
            self.assertEqual(items[b]["st"][0], a)
        for i in legs:
            self.assertGreaterEqual(len(items[i]["pth"]), 4)

    def test_every_span_and_date_is_on_the_sheet(self):
        d = built()["data"]
        ns = {it["n"].lower() for it in d["items"]}
        for sp in WD.SPANS:
            on_card = sp.years == 40 and sp.ref not in R.LONG
            with self.subTest(sp.label):
                self.assertTrue(sp.label.lower() in ns or on_card)
        dates = [it for it in d["items"] if it["id"].startswith("date-")]
        self.assertEqual(len(dates), len(WD.DATES))

    def test_every_verse_of_the_journey_opens_on_something(self):
        """A verse of Exodus 12-19, Numbers 10-36 or Deuteronomy 1-3 opens on
        the camps it names, or the passage it falls in."""
        d = built()["data"]
        for book, chapters in (("Exodus", range(12, 20)), ("Numbers", range(10, 37)),
                               ("Deuteronomy", range(1, 4))):
            for c in chapters:
                for v in verse_numbers(book, c):
                    with self.subTest(verse=f"{book} {c}:{v}"):
                        self.assertTrue(opens(d["items"], d["books"], book, c, v,
                                              chapter=False))

    def test_a_numbers_33_verse_opens_on_its_camps(self):
        d = built()["data"]
        items = d["items"]
        for s in WD.STATIONS:
            i = next(j for j, it in enumerate(items) if it["id"] == s.key.replace("_", "-"))
            for v in WD.num33_verses(s):
                if s.name in A.TEXT_WEB[("Numbers", 33, v)]:
                    with self.subTest(camp=s.key, verse=v):
                        self.assertIn(i, opens(items, d["books"], "Numbers", 33, v))

    def test_tours_and_views(self):
        d = built()["data"]
        self.assertEqual([v["label"] for v in d["views"]], ["Map", "Years 1–2", "Years 3–41"])
        self.assertEqual({t["label"] for t in d["tours"]},
                         {"Egypt to Sinai", "Sinai to Kadesh", "Kadesh to the Jordan"})
        for t in d["tours"]:
            for st in t["stops"]:
                self.assertLess(st["i"], len(d["items"]))
                for r in st["r"]:
                    self.assertLess(r[0], len(d["books"]))
        self.assertEqual([l["id"] for l in d["layers"]], ["events", "variants"])
        svg = built()["svg"]
        for l in d["layers"]:
            self.assertIn(f'data-layer="{l["id"]}"', svg)


class Drawing(unittest.TestCase):
    def test_date_diamonds_dont_touch(self):
        marks = [m for m in built()["marks"] if m["d"].month and m["d"].day]
        for a in marks:
            for b in marks:
                if a is b or a["col"] != b["col"]:
                    continue
                with self.subTest(a=a["d"].ref, b=b["d"].ref):
                    self.assertTrue(abs(a["x"] - b["x"]) >= 18 or abs(a["y"] - b["y"]) >= 18)

    def test_frames_lie_on_the_sheet(self):
        d = built()["data"]
        for it in d["items"] + d["views"]:
            if "fr" in it:
                x, y, w, h = it["fr"]
                with self.subTest(it["id"]):
                    self.assertTrue(x >= 0 and y >= 0 and x + w <= R.W and y + h <= R.H)

    def test_a_wildernesss_name_comes_in_whole(self):
        """Both lines of "Wilderness of Sin" are in one size group, so "SIN"
        never shows alone."""
        svg = built()["svg"]
        for key, r in WD.REGIONS.items():
            if not r.name.startswith("Wilderness of "):
                continue
            main = r.name[len("Wilderness of "):].upper()
            with self.subTest(key):
                m = re.search(r'<g data-fs="[\d.]+" data-fmax="[\d.]+">((?:(?!</g>).)*>%s</text>'
                              r'(?:(?!</g>).)*)</g>' % re.escape(main), svg, re.S)
                self.assertTrue(m and ">WILDERNESS OF</text>" in m.group(1))

    def test_card_rows_dont_repeat(self):
        for it in built()["data"]["items"]:
            for label, rs in it.get("rg", []):
                with self.subTest(item=it["id"], group=label):
                    self.assertEqual(len(rs), len({tuple(r) for r in rs}))


if __name__ == "__main__":
    unittest.main()
