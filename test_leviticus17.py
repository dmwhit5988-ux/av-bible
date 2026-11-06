"""The Leviticus 1-7 offerings pictures: the spec covers every verse, its
cues are words the verses say, only the nine ranges exist, the table's veils
sit on their words, and the modules import without writing anything.

    .venv\\Scripts\\python.exe -m unittest test_leviticus17
"""

import os
import re
import subprocess
import sys
import tempfile
import unittest

import passages
import leviticus17_spec as SPEC
import generate_leviticus17_svg as G
import generate_tabernacle_reference as R

ROOT = os.path.dirname(os.path.abspath(__file__))
NINE = [(4, 1, 2), (5, 13, 14), (5, 18, 19), (6, 7, 8), (6, 18, 19),
        (6, 23, 24), (7, 21, 22), (7, 27, 28), (7, 35, 36)]


class Coverage(unittest.TestCase):
    def test_every_verse_has_a_plan(self):
        """Every verse 1:1-7:38 is in exactly one file, the spec has every
        file in canonical order, and no plan is a stub."""
        files = G.all_files()
        covered = [cv for fk in files for cv in G.file_verses(fk)]
        want = [(c, v) for c in SPEC.CHAPTERS for v in passages.verse_numbers(SPEC.BOOK, c)]
        self.assertEqual(covered, want)
        self.assertEqual(list(SPEC.VERSES), files)
        stubs = [G.ref_str(fk) for fk in files if SPEC.VERSES[fk].stub]
        self.assertEqual(stubs, [])
        for fk in files:
            self.assertTrue(SPEC.VERSES[fk].stops, G.ref_str(fk))

    def test_every_cited_verse_lights_its_unit(self):
        """Every offerings.py row and thing ref in Lev 1-7 lights its unit,
        or is in EXCUSED (with a reason) or REACHED_OFFSCREEN; every unit is
        reached, in a verse that cites it, by 7:37."""
        verses, tables = G.load_verses()
        self.assertEqual(G.coverage_gaps(verses, tables), [])
        hist = G.History(verses, tables)
        bad, pending = G.qc_run(verses, tables, hist)
        self.assertEqual((bad, pending), ([], []))
        for key in G.table_units():
            self.assertIn(key, hist.first_lit, key)

    def test_the_coverage_rule_bites(self):
        verses, tables = G.load_verses()
        pair = ("trespass.by", (6, 2))
        self.assertIn(pair, tables["EXCUSED"])
        del tables["EXCUSED"][pair]
        gaps = G.coverage_gaps(verses, tables)
        self.assertEqual(len(gaps), 1)
        self.assertIn("trespass.by: its row cites 6:2", gaps[0])

    def test_only_the_nine_ranges(self):
        self.assertEqual(sorted(SPEC.RANGES), NINE)
        ranges = [k for k in SPEC.VERSES if len(k) == 3]
        self.assertEqual(sorted(ranges), NINE)
        singles_in_range = [k for k in SPEC.VERSES if len(k) == 2 and G.range_of(*k)]
        self.assertEqual(singles_in_range, [])
        self.assertEqual(len(G.all_files()), 163)

    def test_range_file_names(self):
        names = [G.file_name(fk) for fk in G.all_files() if len(fk) == 3]
        self.assertEqual(names, [f"Leviticus_{c}_{a}-{b}.svg" for c, a, b in NINE])
        self.assertEqual(G.file_name((1, 5)), "Leviticus_1_5.svg")


class Cues(unittest.TestCase):
    def test_cue_words_are_said(self):
        for fk, V in SPEC.VERSES.items():
            c, v = fk[0], fk[1]
            for stop in V.stops:
                G.shot_cam(stop.shot, V.beast)          # every shot resolves
                for beat in stop.beats:
                    cues = [beat[2]]
                    if len(beat) > 3 and "show" in beat[3]:
                        cues.append(beat[3]["show"])
                    for cue in cues:
                        cw = G.cue_word(cue)
                        if cw is None:
                            continue
                        w, n, _d = cw
                        hits = G.occurrences(c, v, w)
                        self.assertGreater(len(hits), n,
                                           f"Lev {c}:{v} doesn't say {w!r} ({beat})")

    def test_a_misspelt_cue_fails(self):
        with self.assertRaises(KeyError):
            G.said(1, 5, "aroundd")

    def test_whole_words_only(self):
        text = G.verse_text(1, 3)
        hits = G.occurrences(1, 3, "he")
        self.assertEqual(len(hits), len(re.findall(r"\b[Hh]e\b", text)))
        self.assertTrue(all(not text[i - 1].isalpha() for i in hits if i))   # not "the"
        self.assertLess(len(G.occurrences(1, 3, "He")), len(hits))     # a capital is exact
        self.assertEqual(G.occurrences(1, 5, "Aaron's"), G.occurrences(1, 5, "Aaron’s"))
        self.assertTrue(G.occurrences(1, 5, "Aaron's"))


class Veils(unittest.TestCase):
    def test_each_veil_holds_its_words(self):
        """Every unit's veil covers the table text it hides, so a change to
        draw_offerings can't leave the veils adrift."""
        _plan, table = G.ref_world()
        texts = []
        for el, box, is_text in table:
            if is_text:
                x, y = float(G._attr(el, "x")), float(G._attr(el, "y"))
                s = re.sub(r"<[^>]+>", "", el[el.find(">") + 1:])
                from html import unescape
                texts.append((unescape(s), x, y))
        units = G.table_units()
        self.assertGreater(len(units), 60)
        for u in units.values():
            x0, y0, x1, y1 = u.box
            ax, ay = u.anchor
            self.assertTrue(x0 <= ax <= x1 and y0 <= ay <= y1, u.key)
            if ".icon" in u.key:
                continue
            hit = [t for t in texts if t[0] == u.text
                   and x0 <= t[1] <= x1 and y0 <= t[2] <= y1]
            self.assertTrue(hit, f"{u.key}: no {u.text!r} inside its veil {u.box}")

    def test_units_by_kind(self):
        units = G.table_units()
        for key in ("burnt.head", "burnt.by", "burnt.thing:bull",
                    "burnt.blood:around the altar", "sin.who:the anointed priest",
                    "sin.rank1", "sin.icon1:bull", "sin.blood:before the veil",
                    "sin.blood:before the veil/who", "trespass.when"):
            self.assertIn(key, units)
        self.assertEqual(sum(1 for k in units if k.startswith("sin.who:")), 7)
        self.assertEqual(sum(1 for k in units if re.match(r"sin\.rank\d$", k)), 5)
        # the table is the reference's, where the design says
        self.assertEqual((R.OFF_X, R.OFF_Y), (2960, 1468))


class Render(unittest.TestCase):
    def test_probes_pass_qc(self):
        verses, tables = G.load_verses()
        hist = G.History(verses, tables)
        for fk in ((1, 5), (4, 7)):
            svg, rep = G.render(fk, verses, tables, hist)
            self.assertEqual(rep["problems"], [], G.ref_str(fk))
            self.assertNotIn("clip-path", svg)
            self.assertNotIn('repeatCount="indefinite"', svg)

    def test_state_is_derived(self):
        verses, tables = G.load_verses()
        hist = G.History(verses, tables)
        self.assertIn("burnt.head", hist.before[(1, 4)])
        self.assertNotIn("burnt.head", hist.before[(1, 3)])
        self.assertIn("A.fire", hist.before[(1, 8)])


class Fixes(unittest.TestCase):
    """The core's chapter 1 fixes: B scoped to the offering, one outline
    round an entry and its who-line, no label cut by the frame, size."""

    @classmethod
    def setUpClass(cls):
        cls.verses, cls.tables = G.load_verses()
        cls.hist = G.History(cls.verses, cls.tables)
        cls.out = {fk: G.render(fk, cls.verses, cls.tables, cls.hist)
                   for fk in ((1, 3), (1, 5), (1, 9), (3, 4), (4, 7))}

    def test_offering_of(self):
        import leviticus17_stations as ST
        self.assertEqual(ST.offering_of((1, 9)), "burnt")
        self.assertEqual(ST.offering_of((3, 4)), "peace")
        self.assertEqual(ST.offering_of((4, 9)), "sin")
        self.assertEqual(ST.offering_of((7, 4)), "trespass")
        self.assertEqual(ST.offering_of((7, 31)), "peace")
        self.assertEqual(ST.offering_of((7, 24)), "")

    def test_parts_board_is_the_offerings_own(self):
        """3:4 shows the peace law's parts only, none of the burnt
        offering's chips, and one word for the fat by the loins."""
        before = {k for k in self.hist.before[(3, 4)] if k.startswith("B.")}
        self.assertTrue(before and all("@burnt:" in k or "@peace:" in k for k in before), before)
        _svg, rep = self.out[(3, 4)]
        words = {k for k in rep["words"] if k.startswith("B.")}
        self.assertEqual(words, {"B.kidneys", "B.kidney_fat", "B.liver_cover",
                                 "B.fat_cover", "B.fat_on"})     # 3:3's and 3:4's
        self.assertIn("B.loins", rep["outlined"])          # its line still lights

    def test_each_law_keeps_its_own_altar_and_cast(self):
        """The burnt offering's stack isn't on the altar at the meal
        offering, nor its ram and goat beside the peace offering's ox."""
        import leviticus17_stations as ST
        self.assertEqual(ST.section_of((2, 2)), "meal:For the people")
        self.assertEqual(ST.section_of((6, 9)), "burnt:For the priests")
        self.assertEqual(ST.section_of((7, 23)), "")
        A = ST.registry()["A"]
        before = self.hist.before[(2, 2)]
        self.assertIn(A.pkey("A.slot.pieces", G.FileV(self.verses[(1, 8)], (1, 8))), before)
        self.assertNotIn(A.pkey("A.slot.pieces", G.FileV(self.verses[(2, 2)], (2, 2))), before)
        slots = self.hist.slots[(3, 1)]
        self.assertEqual(slots.get(("C", "mid@1:10")), "C.ram")
        self.assertFalse([k for k in slots if k[0] == "C" and k[1].endswith("@3:1")])
        self.assertEqual(self.hist.slots[(3, 2)].get(("C", "left@3:1")), "C.ox")

    def test_each_case_keeps_its_own_marks(self):
        """The bird's blood isn't on the altar's side at the meal offering,
        5:11's struck oil isn't struck at 6:20, the lamb of 3:6-11 isn't
        beside the goat of 3:12-16, and the ram's fat isn't on the wood when
        the bird is burned."""
        import leviticus17_stations as ST
        self.assertEqual(ST.case_of((1, 15)), "1:14")
        self.assertEqual(ST.case_of((6, 18, 19)), "6:14")
        reg = ST.registry()
        A, K = reg["A"], reg["K"]
        fv = lambda fk: G.FileV(self.verses[fk], fk)
        self.assertNotIn(A.pkey("A.side", fv((2, 9))), self.hist.before[(2, 9)])
        self.assertIn(A.pkey("A.side", fv((1, 16))), self.hist.before[(1, 16)])
        self.assertNotIn(A.pkey("A.slot.fat", fv((1, 15))), self.hist.before[(1, 15)])
        self.assertNotIn(K.pkey("K.not:oil", fv((6, 20))), self.hist.before[(6, 20)])
        cast = {v for k, v in self.hist.slots[(3, 13)].items() if k[0] == "C" and k[1].endswith("@3:12")}
        self.assertEqual(cast, set())          # 3:13 brings its goat in itself
        self.assertIn(("light", "C.goat", "@"), SPEC.VERSES[(3, 13)].stops[0].beats)

    def test_a_move_leaves_its_end_state(self):
        """7:31's fat at the altar and breast with the priests are still
        there at 7:32."""
        B = __import__("leviticus17_stations").registry()["B"]
        fv = G.FileV(self.verses[(7, 32)], (7, 32))
        before = self.hist.before[(7, 32)]
        self.assertIn(B.pkey("B.at:altar:fat", fv), before)
        self.assertIn(B.pkey("B.at:priests:breast", fv), before)

    def test_the_file_before_is_carried_in(self):
        """What 1:4 drew and 1:5 doesn't (the offerer's hand on the head)
        is in 1:5's first frame, its animations already played (begin < 0),
        and fades as the camera moves."""
        svg, rep = G.render((1, 5), self.verses, self.tables, self.hist)
        self.assertIn("C.hand", rep["carried"])
        self.assertIn('begin="-', svg)
        self.assertEqual(G.shift_times('<animate begin="2.00s" dur="0.50s"/>', 5.0),
                         '<animate begin="-0.49s" dur="0.50s"/>')

    def test_rests_are_whole_cards_at_the_lens(self):
        """Every stop rests on a home, a station's whole card or the whole
        table (7:37); a station's card, Sinai's too, is at STATION_S and a
        close-up name is refused. (This replaces the close-ups' head test:
        there are no close-ups to cut a head.)"""
        import leviticus17_stations as ST
        homes = set(SPEC.SHOTS)
        cards = {k for k, st in ST.registry().items() if not st.world}
        for fk, V in SPEC.VERSES.items():
            for stop in V.stops:
                self.assertIn(stop.shot, homes | cards | G.LENS_EXEMPT, G.ref_str(fk))
                s = G.shot_cam(stop.shot, V.beast)[0]
                if stop.shot not in G.LENS_EXEMPT:
                    self.assertEqual(s, SPEC.LENS, G.ref_str(fk))
        for k in cards:
            ox, oy = SPEC.STATIONS[k]
            self.assertEqual(G.shot_cam(k), (SPEC.STATION_S, ox + 512, oy + 288))
        for name in ("B.inner", "A.fire", "C.head"):
            with self.assertRaises(KeyError):
                G.shot_cam(name, "bull")

    def test_one_outline_round_entry_and_who_line(self):
        self.assertIn("burnt.burns:the whole/who", G.table_units())
        _svg, rep = self.out[(1, 9)]
        self.assertIn("burnt.burns:the whole", rep["outlined"])
        self.assertFalse([k for k in rep["outlined"] if k.endswith("/who")])

    def test_no_plan_label_cut_at_a_plan_shot(self):
        for name, cam in SPEC.SHOTS.items():
            self.assertEqual(G.plan_labels_cut(cam), [], name)
        # the rule bites: the core's old plan:door frame cut "lamp stand"
        self.assertIn("lamp stand", G.plan_labels_cut((1.9, 1470, 800)))

    def test_probes_under_70_kb(self):
        for fk, (svg, rep) in self.out.items():
            self.assertEqual(rep["problems"], [], G.ref_str(fk))
            self.assertLess(len(svg.encode()), 70 * 1024, G.ref_str(fk))

    def test_compaction_keeps_the_geometry(self):
        d = G.path_d("10.04,20 10.56,20.5 9.95,19.42", True)
        self.assertEqual(d, "M10 20l.6.5-.6-1.1z")
        svg = ('<g><polygon points="0,0 10,0 10,10" fill="rgb(255,0,0)"/>'
               '<polyline points="0,0 5,5" fill="none" stroke="rgb(1,2,3)">'
               '<animate attributeName="stroke-opacity" values="0;1" dur="1s"/></polyline>'
               '<polyline points="0,0 5,5" fill="none" stroke="rgb(1,2,3)" '
               'stroke-dasharray="7 28"><animate attributeName="x" values="0;1"/></polyline></g>')
        c = G.compact(svg)
        self.assertIn('<path d="M0 0l10 0 0 10z" fill="#f00"/>', c)
        self.assertIn("</path>", c)
        self.assertIn('stroke-dasharray="7 28"', c)
        self.assertEqual(c.count("<polyline"), c.count("</polyline>"))
        self.assertEqual(c.count("<path"), 2)

    def test_a_figure_drawn_twice_is_shared(self):
        import leviticus17_stations as ST
        import svg_figures as F
        ctx = ST.Ctx(None, (7, 31), None)
        once = ctx.resolve_figures(ctx.figure(F.priest(), 10, 20, 1.0))
        self.assertNotIn("<use", once)
        self.assertEqual(ctx.defs, {})
        two = ctx.resolve_figures(ctx.figure(F.priest(), 10, 20, 1.0)
                                  + ctx.figure(F.priest(), 60, 20, 1.0))
        self.assertEqual(two.count("<use"), 2)
        self.assertEqual(len(ctx.defs), 1)

    def test_a_hold_is_two_keyframes(self):
        cams = [(1.0, 100.0, 100.0)] * 50 + [(1.0 + i / 40, 100.0 + i, 100.0) for i in range(41)]
        keep = G.keyframes(cams)
        self.assertEqual(keep[:2], [0, 50])     # the hold runs to frame 50
        self.assertEqual(keep[-1], len(cams) - 1)


class Calm(unittest.TestCase):
    """The owner's "less whiplash" (the one lens): the whole run's camera
    within its budgets, and no file over the per-file ones."""

    def test_camera_is_calm(self):
        verses, _t = G.load_verses()
        P = G.plans(verses)
        legs = {fk: G.camera_legs(p) for fk, p in P.items()}
        every = [lg for ls in legs.values() for lg in ls]
        narr = sum(p.narr for p in P.values())
        self.assertLessEqual(len(every), 150)
        self.assertLessEqual(sum(lg["pan"] for lg in every), 200)
        self.assertLessEqual(sum(lg["zoom"] for lg in every), 2.5)
        self.assertLessEqual(sum(lg["arc"] for lg in every), 1.5)
        self.assertLessEqual(sum(lg["dur"] for lg in every), 0.26 * narr)
        # the still spans between one move's end and the next's start,
        # across the seams
        rests, still = [], None
        for p in P.values():
            t = 0.0
            for k, d in enumerate(p.D):
                if d <= 0:
                    continue
                if still is not None:
                    rests.append(round(still + p.starts[k] - t, 2))
                still, t = 0.0, p.starts[k] + d
            if still is not None:
                still += p.narr - t
        self.assertLessEqual(sum(1 for r in rests if r < 1.5), 20)
        for fk, ls in legs.items():
            ref = G.ref_str(fk)
            self.assertLessEqual(len(ls), G.MAX_LEGS, ref)
            self.assertLessEqual(sum(lg["pan"] for lg in ls), G.MAX_FILE_PAN, ref)
            self.assertLessEqual(sum(lg["zoom"] for lg in ls), G.MAX_FILE_ZOOM, ref)
            for lg in ls:
                self.assertLessEqual(lg["pan"], G.MAX_LEG_PAN, ref)
                self.assertLessEqual(round(lg["peak"]), G.MAX_PEAK_PX_S, ref)
                if lg["lens"]:
                    self.assertEqual(lg["kind"], "pan", ref)

    def test_a_pan_is_paced(self):
        """lev_duration keeps a long pan's eased peak at PAN_PEAK_PX_S, and
        caps it at PAN_MAX_D."""
        s = SPEC.LENS
        d = G.lev_duration((s, 0, 0), (s, 3000, 0))
        self.assertAlmostEqual(d, 3000 * s * G.EASE_PEAK / G.PAN_PEAK_PX_S, places=6)
        self.assertEqual(G.lev_duration((s, 0, 0), (s, 9000, 0)), G.PAN_MAX_D)
        self.assertEqual(G.lev_duration((s, 0, 0), (s, 0, 0)), 0.0)


class ImportSafety(unittest.TestCase):
    def test_import_writes_nothing(self):
        with tempfile.TemporaryDirectory() as d:
            code = ("import sys; sys.path.insert(0, %r); import generate_leviticus17_svg, "
                    "leviticus17_spec, leviticus17_stations; "
                    "leviticus17_stations.registry()" % ROOT)
            r = subprocess.run([sys.executable, "-c", code], cwd=d, capture_output=True,
                               text=True, timeout=300)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(os.listdir(d), [])
            self.assertEqual(r.stdout, "")

    def test_main_needs_a_destination(self):
        import contextlib
        import io
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
            G.main([])


if __name__ == "__main__":
    unittest.main()
