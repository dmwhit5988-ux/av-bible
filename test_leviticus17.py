"""The Leviticus 1-7 offerings pictures (the workbench that files): every
verse is built, its cues are words the verses say, every table unit is lit in
a verse that cites it, only the nine ranges exist, the dock's slots are the
table's units, the motion budget holds over the whole book with no camera,
the seams hold by construction, and the modules import without writing
anything.

    .venv\\Scripts\\python.exe -m unittest test_leviticus17
"""

import importlib
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
MODULES = ["generate_leviticus17_svg", "leviticus17_spec", "leviticus17_bench",
           "leviticus17_parts", "leviticus17_dock", "leviticus17_art"] + \
          [f"leviticus17_wb_s{i}" for i in range(1, 8)]
# a file a section, the busiest of each, and the boundaries' first files
PROBES = [(1, 12), (2, 4), (3, 1), (3, 9), (4, 3), (4, 7), (5, 1), (5, 6), (6, 9), (6, 28),
          (7, 11), (7, 15), (7, 31)]


def setUpModule():
    global B, D, P
    import leviticus17_bench as B
    import leviticus17_dock as D
    import leviticus17_parts as P
    B.build_timeline()


class Files(unittest.TestCase):
    def test_every_verse_is_built(self):
        """Every verse 1:1-7:38 is in exactly one file, in canonical order;
        each file belongs to one section, no section is a stub, and every
        file has a word cued in it."""
        files = G.all_files()
        covered = [cv for fk in files for cv in G.file_verses(fk)]
        want = [(c, v) for c in SPEC.CHAPTERS for v in passages.verse_numbers(SPEC.BOOK, c)]
        self.assertEqual(covered, want)
        self.assertEqual(len(files), 163)
        sections = [B.section_of_file(fk) for fk in files]
        self.assertEqual(sections, sorted(sections))           # contiguous, in order
        self.assertEqual(sorted(set(sections)), [s[0] for s in B.SECTIONS])
        for sid, mod, _a, _b in B.SECTIONS:
            self.assertFalse(getattr(importlib.import_module(mod), "STUB", True), sid)
        # (a file of the formula "Yahweh spoke to Moses, saying" alone
        # only clears the bench)
        cued = {B.VERSE_FILE[cv] for _T, cv, *_r in B.CUES}
        formula = {fk for fk in files if all(G.verse_text(*cv).startswith("Yahweh spoke to Moses")
                                             for cv in G.file_verses(fk))}
        self.assertEqual([G.ref_str(fk) for fk in files if fk not in cued | formula], [])
        self.assertLessEqual(len(formula - cued), 2)

    def test_only_the_nine_ranges(self):
        self.assertEqual(sorted(SPEC.RANGES), NINE)
        self.assertEqual(sorted(fk for fk in G.all_files() if len(fk) == 3), NINE)

    def test_range_file_names(self):
        names = [G.file_name(fk) for fk in G.all_files() if len(fk) == 3]
        self.assertEqual(names, [f"Leviticus_{c}_{a}-{b}.svg" for c, a, b in NINE])
        self.assertEqual(G.file_name((1, 5)), "Leviticus_1_5.svg")

    def test_a_range_file_spans_its_verses(self):
        fk = (4, 1, 2)
        self.assertAlmostEqual(B.FILE_DUR[fk], G.narration(4, 1) + G.narration(4, 2), places=6)
        self.assertAlmostEqual(B.VERSE_T0[(4, 2)], B.FILE_T0[fk] + G.narration(4, 1), places=6)
        # a cue in a range's later verse waits RANGE_LAG more
        self.assertAlmostEqual(B.said_T(4, 2, "sins"),
                               B.VERSE_T0[(4, 2)] + G.said(4, 2, "sins") + B.RANGE_LAG, places=6)


class Cues(unittest.TestCase):
    def test_cue_words_are_said(self):
        self.assertGreater(len(B.CUES), 500)
        for T, (c, v), phrase, n, owner in B.CUES:
            self.assertGreater(len(G.occurrences(c, v, phrase)), n,
                               f"{owner}: Lev {c}:{v} doesn't say {phrase!r}")

    def test_a_misspelt_cue_fails(self):
        with self.assertRaises(KeyError):
            G.said(1, 5, "aroundd")
        n = len(B.CUES)
        with self.assertRaises(KeyError):
            B.cue(1, 5, "aroundd")
        with self.assertRaises(KeyError):
            B.cue(1, 5, "around", 5)                  # said once, not six times
        self.assertEqual(len(B.CUES), n)

    def test_a_cue_leads_its_word(self):
        T = B.cue(1, 5, "around")
        del B.CUES[-1]
        self.assertAlmostEqual(T, B.VERSE_T0[(1, 5)] + G.said(1, 5, "around") - B.SAY_LEAD,
                               places=6)

    def test_whole_words_only(self):
        text = G.verse_text(1, 3)
        hits = G.occurrences(1, 3, "he")
        self.assertEqual(len(hits), len(re.findall(r"\b[Hh]e\b", text)))
        self.assertTrue(all(not text[i - 1].isalpha() for i in hits if i))   # not "the"
        self.assertLess(len(G.occurrences(1, 3, "He")), len(hits))     # a capital is exact
        self.assertEqual(G.occurrences(1, 5, "Aaron's"), G.occurrences(1, 5, "Aaron’s"))
        self.assertTrue(G.occurrences(1, 5, "Aaron's"))


class Coverage(unittest.TestCase):
    def test_every_cited_unit_is_lit(self):
        """Every table unit is lit by 7:37, first in a verse that cites it
        (or its REACH), and every section leaves its boundary as the
        contract says."""
        probs, pending, _w, stubs = B.coverage()
        self.assertEqual((probs, pending, stubs), ([], [], []))
        self.assertEqual(sorted(G.table_units()), sorted(B.LIT))
        self.assertEqual(B.boundary_problems(), [])

    def test_the_coverage_rule_bites(self):
        saved = dict(B.LIT)
        try:
            B.LIT["trespass.by"] = B.at(6, 9, 1.0)          # a verse that doesn't cite it
            probs = B.coverage()[0]
            self.assertEqual(len(probs), 1)
            self.assertIn("trespass.by first lit at 6:9", probs[0])
            del B.LIT["meal.by"]
            self.assertIn("meal.by is never lit", B.coverage()[0])
        finally:
            B.LIT.clear()
            B.LIT.update(saved)

    def test_tables_name_real_units(self):
        units = G.table_units()
        reach, excused = B.reach_tables()
        for k in list(reach) + list(excused):
            self.assertIn(k[0] if isinstance(k, tuple) else k, units)


class Dock(unittest.TestCase):
    def test_every_dock_unit_is_a_table_unit(self):
        """The five columns' slots map 1:1 to the table's units (the WHEN
        cells excepted: they lift in 7:37's file view), and every slot sits
        inside the dock's column panel."""
        D._check_units()
        have = set()
        x0, y0, x1, y1 = D.D_X0, D.COL_Y, D.D_X0 + D.D_W, D.COL_BOT
        for off, (slots, _sk, bottom, _m) in D.LAYOUT.items():
            self.assertLessEqual(bottom, D.COL_BOT - 6, off)
            for k, s_ in slots.items():
                have.add(k.split("#")[0])
                b = s_.text_box() or s_.box
                self.assertTrue(x0 <= b[0] and b[2] <= x1 and y0 <= b[1] and b[3] <= y1,
                                f"{k} {tuple(round(q) for q in b)}")
        self.assertEqual(have, {k for k in G.table_units() if not k.endswith(".when")})

    def test_icons_clear_the_names_above(self):
        """BROUGHT's icon rows are far enough apart that no icon is drawn
        over the name of the thing above it."""
        for off, (slots, *_r) in D.LAYOUT.items():
            things = [s_ for s_ in slots.values() if s_.kind == "thing"]
            for a in things:
                top = a.icon[1] - a.icon[3]
                for b in things:
                    nb = b.text_box()
                    if b.y < a.y - 1 and abs(b.x - a.x) < 1:
                        self.assertGreaterEqual(top, nb[3] + D.ICON_GAP - 0.5, (off, a.key, b.key))

    def test_each_veil_holds_its_words(self):
        """The file view's table splits draw_offerings by unit: every unit's
        words are drawn inside its veil's box, so a change to draw_offerings
        can't leave the veils adrift."""
        _base, per_unit = D._table_parts()
        units = G.table_units()
        self.assertGreater(len(units), 60)
        for u in units.values():
            x0, y0, x1, y1 = u.box
            ax, ay = u.anchor
            self.assertTrue(x0 <= ax <= x1 and y0 <= ay <= y1, u.key)
            if ".icon" in u.key or u.key.endswith(".when"):
                continue
            words = [re.sub(r"<[^>]+>", "", t) for t in per_unit.get(u.key, ([], []))[1]]
            from html import unescape
            self.assertIn(u.text, [unescape(w) for w in words], u.key)

    def test_units_by_kind(self):
        units = G.table_units()
        for key in ("burnt.head", "burnt.by", "burnt.thing:bull",
                    "burnt.blood:around the altar", "sin.who:the anointed priest",
                    "sin.rank1", "sin.icon1:bull", "sin.blood:before the veil",
                    "sin.blood:before the veil/who", "trespass.when"):
            self.assertIn(key, units)
        self.assertEqual(sum(1 for k in units if k.startswith("sin.who:")), 7)
        self.assertEqual(sum(1 for k in units if re.match(r"sin\.rank\d$", k)), 5)
        self.assertEqual((R.OFF_X, R.OFF_Y), (2960, 1468))


class Motion(unittest.TestCase):
    """The owner's rules over the whole book (no rendering needed)."""

    def test_no_camera(self):
        """The frame never moves: the panels and the strip's plan have no
        events, and only chips, tokens, bench pieces and the file view's
        column ever travel."""
        for key in ("panels", "strip.art", "dock.panel"):
            self.assertEqual(B.ELS[key].events, [], key)
        for el in B.ELS.values():
            if el.region in ("base",):
                self.assertEqual(el.events, [], el.key)
            for e in el.events:
                if e["kind"] == "glide":
                    self.assertTrue(re.match(r"fv\d+\.glide$", el.key), el.key)
        self.assertEqual({t["kind"] for t in B.TRAVELS} - set(B.TRAVEL_KINDS), set())

    def test_motion_budget(self):
        """At most 3 chip flights and 1 file view a file, every travel at
        most 560 px (the filing glide aside) and 800 px/s at its peak, one
        thing travelling at a time and nothing lighting up during it."""
        bad = {}
        for fk in G.all_files():
            p = B.budget_problems(fk)
            if p:
                bad[G.ref_str(fk)] = p
        self.assertEqual(bad, {})
        for t in B.TRAVELS:
            if t["kind"] != "filing glide":
                self.assertLessEqual(t["px"], B.MAX_FLIGHT_PX + 0.5, t["what"])
            self.assertLessEqual(t["peak"], B.MAX_PEAK + 0.5, t["what"])
        per = {}
        for t in B.TRAVELS:
            if t["kind"] == "chip flight":
                per[t["file"]] = per.get(t["file"], 0) + 1
        self.assertLessEqual(max(per.values()), B.MAX_FLIGHTS)
        views = [B.file_of(T) for T, _o, _s in B.FILE_VIEWS]
        self.assertEqual(len(views), len(set(views)))
        self.assertEqual([o for _T, o, _s in B.FILE_VIEWS],
                         ["burnt", "meal", "peace", "sin", "trespass", "peace"])

    def test_timing_and_regions(self):
        """Nothing begins after the narration - 0.1 s, the last animation
        ends 0.35 s before the MP3 does, and at most one region begins an
        animation in any 0.3 s (one gesture's events share a group)."""
        bad = {}
        for fk in G.all_files():
            p = B.timing_problems(fk) + B.region_problems(fk)
            if p:
                bad[G.ref_str(fk)] = p
        self.assertEqual(bad, {})

    def test_seams_by_construction(self):
        """A file renders every element's state at its start, so it begins
        on the frame the file before ends on; what could break that is an
        animation still running at a file's end."""
        bad = {G.ref_str(fk): B.seam_problems(fk) for fk in G.all_files() if B.seam_problems(fk)}
        self.assertEqual(bad, {})
        # the state a file starts on is the state the file before ends on
        files = G.all_files()
        a, b = files[16], files[17]                          # 1:17 | 2:1
        self.assertEqual(B.file_end(a), B.FILE_T0[b])
        for el in B.ELS.values():
            self.assertEqual(el.state(B.file_end(a)), el.state(B.FILE_T0[b]), el.key)

    def test_section_boundaries_and_the_books_end(self):
        """Every section ends on the contract (bench.boundary_problems), and
        at the book's end nothing of the last section's workshop is on under
        the file view (no case outline, no chip)."""
        self.assertEqual(B.boundary_problems(), [])

    def test_glides_keep_their_words_clear(self):
        """A filing glide's words never touch the file view's keys at its
        quarter, half, three-quarter and nine-tenths points, and the filed
        column's own key waits for it to land."""
        for T, off, _o in B.FILE_VIEWS:
            fk = B.file_of(T)
            self.assertEqual(B.glide_text_problems(fk), [], G.ref_str(fk))
        for el in B.ELS.values():
            if el.key.endswith(".ownkey"):
                n = el.key.split(".")[0]
                land = next(e["T"] + e["dur"] for e in B.ELS[f"{n}.glide"].events
                            if e["kind"] == "glide")
                ins = [e["T"] for e in el.events if e["kind"] == "in"]
                self.assertEqual(len(ins), 1, el.key)
                self.assertAlmostEqual(ins[0], land, places=6)

    def test_a_trace_can_share_a_group(self):
        """3:17's not-mark over the blood is one gesture with the drop and
        NOT EATEN's unveil (one group: the region rule counts it once)."""
        fk = (3, 17)
        starts = B.region_starts(B.FILE_T0[fk], B.file_end(fk))
        groups = {g for _T, _reg, g, what in starts if what.startswith("s3.ban.blood.not")}
        self.assertEqual(groups, {"s3ban.blood"})


class Render(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out = {}
        for fk in PROBES:
            svg = B.render_file(fk)
            cls.out[fk] = (svg, B.qc_file(fk, svg))

    def test_probes_are_well_formed_xml(self):
        """An <img> parses a verse strictly: a doubled attribute (7:15-19's
        dashed divider once had two stroke-dasharrays) shows nothing."""
        import xml.etree.ElementTree as ET
        for fk, (svg, _rep) in self.out.items():
            ET.fromstring(svg)
        self.assertNotEqual(B.xml_problems('<svg a="1" a="2"/>'), [])
        self.assertEqual(B.xml_problems('<svg a="1"/>'), [])

    def test_a_traced_line_cannot_be_dashed(self):
        with self.assertRaises(ValueError):
            B.traced_svg([(0, 0), (10, 0)], (1, 2, 3), 2, extra=' stroke-dasharray="4 5"')

    def test_every_published_verse_parses(self):
        """Every Leviticus 1-7 file under web/visuals is well-formed XML."""
        import glob
        import xml.etree.ElementTree as ET
        from config import VISUALS_DIR
        files = []
        for c in range(1, 8):
            files += glob.glob(os.path.join(VISUALS_DIR, "Leviticus", str(c), "*.svg"))
        self.assertEqual(len(files), len(G.all_files()))
        for f in files:
            with self.subTest(os.path.basename(f)):
                ET.parse(f)

    def test_probes_pass_qc(self):
        for fk, (svg, rep) in self.out.items():
            self.assertEqual(rep["problems"], [], G.ref_str(fk))
            for bad in ("clip-path", "<mask", "<filter", "repeatCount"):
                self.assertNotIn(bad, svg, G.ref_str(fk))

    def test_text_floor(self):
        for fk, (_svg, rep) in self.out.items():
            self.assertGreaterEqual(rep["min_text"], B.MIN_TEXT, G.ref_str(fk))

    def test_probes_under_70_kb(self):
        for fk, (svg, _rep) in self.out.items():
            self.assertLess(len(svg.encode()), 70 * 1024, G.ref_str(fk))

    def test_file_views_under_the_cap(self):
        for fk in ((5, 13, 14), (6, 7, 8), (7, 37)):
            self.assertLess(len(B.render_file(fk).encode()), B.KB_MAX * 1024, G.ref_str(fk))

    def test_the_files_after_a_view_are_light(self):
        """5:15 opens in the workshop (5:13-14's view returns inside it), and
        7:38 leaves out what 7:37's table hides: both under the 70 KB aim."""
        for fk in ((5, 15), (7, 38)):
            self.assertLess(len(B.render_file(fk).encode()), B.KB_AIM * 1024, G.ref_str(fk))
        fk = (5, 13, 14)
        n = next(i for i, (T, _o, _s) in enumerate(B.FILE_VIEWS, 1) if B.file_of(T) == fk)
        self.assertFalse(B.ELS[f"fv{n}.table"].state(B.file_end(fk))[0])

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
        # a text's inherited font and default anchor are dropped, the root's kept
        from svg_surface import FONT_FAMILY
        root = f'<svg font-family="{FONT_FAMILY}"><text x="1" font-family="{FONT_FAMILY}" ' \
               f'text-anchor="start">a</text><text text-anchor="middle">b</text></svg>'
        c = G.compact(root)
        self.assertEqual(c.count("font-family"), 1)
        self.assertNotIn('text-anchor="start"', c)
        self.assertIn('text-anchor="middle"', c)


class ImportSafety(unittest.TestCase):
    def test_import_writes_nothing(self):
        with tempfile.TemporaryDirectory() as d:
            code = ("import sys; sys.path.insert(0, %r); " % ROOT
                    + "; ".join(f"import {m}" for m in MODULES)
                    + "; import leviticus17_bench as B; B.build_timeline()")
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
