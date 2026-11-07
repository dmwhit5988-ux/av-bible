"""The family tree's Line to Jesus layer (gospel_lines.py and
generate_ot_family_tree_svg.place_gospel_lines): that it leaves the tree alone,
that both lines are the text's and land on the right boxes, that it stands clear
of everything already on the sheet, and that its verses say what it claims.

    .venv\\Scripts\\python.exe -m unittest test_gospel_lines
"""

import json
import os
import re
import unittest

import chronicles_tree as CT
import family_tree_data as FT
import generate_kings_reference as KR
import generate_luke3
import generate_ot_family_tree_svg as G
import gospel_lines as GL
import matthew_tree
import reference_viewer
import verse_refs
from books import BOOK_NAMES
from svg_surface import _fmt, _rgb

BUILT = None


def built():
    """The chart, built once: both lines' sheet, the sheet without them, and
    the sidecar with and without them."""
    global BUILT
    if BUILT is None:
        svg, W, H, T, (left, top), S = G.build_svg()
        plain = G.build_svg(lines=False)[0]
        path = os.path.join(G.OUT_DIR, G.STEM + ".json")
        with open(path, encoding="utf-8") as f:
            previous = json.load(f)
        data, misses = FT.sidecar(
            T, left, top, G.printed_gen, previous,
            extra=lambda items, index: GL.add_items(items, index, S, left, top))
        tree_only, _ = FT.sidecar(T, left, top, G.printed_gen, previous)
        BUILT = dict(svg=svg, W=W, H=H, T=T, left=left, top=top, S=S,
                     plain=plain, data=data, misses=misses, tree_only=tree_only,
                     previous=previous)
    return BUILT


OPENING = f'<g data-layer="{GL.LAYER}">\n'


def _group_end(svg, start):
    """Where the <g> opening at `start` closes, past its </g>."""
    depth = 1
    for m in re.compile(r"<g[ >]|</g>").finditer(svg, start + len(OPENING)):
        depth += -1 if m.group() == "</g>" else 1
        if depth == 0:
            return m.end()
    raise ValueError("an unclosed group")


def strip_layer(svg):
    """The sheet with the layer's <g data-layer="jesus"> groups taken out."""
    while OPENING in svg:
        start = svg.index(OPENING)
        svg = svg[:start] + svg[_group_end(svg, start) + 1:]
    return svg


def layer_groups(svg):
    """The text of the layer's groups, in order: its lines, then its boxes."""
    out, start = [], svg.find(OPENING)
    while start >= 0:
        end = _group_end(svg, start)
        out.append(svg[start:end])
        start = svg.find(OPENING, end)
    return out


def attrs(element):
    return dict(re.findall(r'([a-z0-9-]+)="([^"]*)"', element))


class TheTreeStaysAsItWas(unittest.TestCase):
    def test_the_sheet_less_the_layer_is_the_tree_byte_for_byte(self):
        b = built()
        self.assertEqual(b["svg"].count(f'<g data-layer="{GL.LAYER}">'), 2)
        self.assertEqual(strip_layer(b["svg"]), b["plain"])

    def test_the_sheet_keeps_its_size(self):
        b = built()
        self.assertEqual((round(b["W"]), round(b["H"])), (26946, 16736))

    def test_the_trees_items_come_first_and_unchanged(self):
        b = built()
        tree = b["tree_only"]["items"]
        for old, new in zip(tree, b["data"]["items"]):
            for field in ("id", "n", "s", "k", "b", "p", "c", "l", "x", "g"):
                self.assertEqual(old.get(field), new.get(field), old["id"])

    def test_nothing_is_grafted_on_the_tree(self):
        b = built()
        drawn = [n.label for n in CT.walk(b["T"].root)]
        self.assertEqual(drawn, [n.label for n in CT.walk(CT.build().root)])
        self.assertFalse({"Abiud", "Rhesa", "Heli", "Neri"} & set(drawn))

    def test_files_on_disk_are_what_the_generator_writes(self):
        b = built()
        with open(os.path.join(G.OUT_DIR, G.STEM + ".svg"), encoding="utf-8") as f:
            self.assertEqual(f.read(), b["svg"])
        self.assertEqual(b["previous"], json.loads(json.dumps(b["data"])))
        # the page is what reads the sidecar's new fields, so it moves with it
        with open(os.path.join(G.OUT_DIR, G.STEM + ".html"), encoding="utf-8") as f:
            self.assertEqual(f.read(), G.viewer_page(b["W"], b["H"]))

    def test_every_generated_page_is_the_current_viewer(self):
        # A push is a deploy: a viewer change must not reach one page of six.
        # V6 and 1-2 Chronicles are older copies that nothing writes.
        fixed = re.split(r"__(?:TITLE|PLACEHOLDER|W|H|DATA|STEM)__",
                         reference_viewer._PAGE)
        whole = re.compile(".*?".join(map(re.escape, fixed)), re.S)
        for stem in ("Old_Testament_family_tree", "Old_Testament_timeline",
                     "Tabernacle", "Land_of_Israel", "Kings_and_prophets",
                     "Pauls_journeys", "Temple", "Wilderness_journey",
                     "Sacred_year"):
            with open(os.path.join(G.OUT_DIR, stem + ".html"), encoding="utf-8") as f:
                self.assertTrue(whole.fullmatch(f.read()), stem)


class Ids(unittest.TestCase):
    def test_ids_are_unique_and_the_layers_literal(self):
        items = built()["data"]["items"]
        ids = [it["id"] for it in items]
        self.assertEqual(len(set(ids)), len(ids))
        layer = {it["id"] for it in items if it.get("ly")}
        for want in ("jesus", "joseph.mary", "mary.joseph", "jacob.matthew",
                     "abiud.matthew", "rhesa.luke-3-27", "heli.luke-3-23",
                     "mattatha.luke-3-31", "neri.luke-3-27",
                     "shealtiel.luke-3-27", "cainan.luke-3-36", "god.luke-3-38",
                     "stop.matthew-opens", "stop.part-david",
                     "stop.meet-shealtiel", "stop.part-zerubbabel",
                     "stop.meet-joseph"):
            self.assertIn(want, layer)
        self.assertEqual(len(layer), 57)
        self.assertNotIn("jacob", ids)      # a lost link opens the name search

    def test_a_second_generation_issues_the_same_ids(self):
        b = built()
        again = json.loads(json.dumps(b["data"]))
        nodes = list(CT.walk(b["T"].root))
        ids = FT.stable_ids(nodes, FT.issued_ids(again))
        for n, it in zip(nodes, b["data"]["items"]):
            self.assertEqual(ids[n], it["id"])

    def test_the_layer_issues_no_tree_id(self):
        self.assertFalse(set(FT.issued_ids(built()["data"]).values())
                         & {it["id"] for it in built()["data"]["items"]
                            if it.get("ly")})

    def test_no_kings_page_link_lands_on_the_layer(self):
        built()
        layer = {it["id"] for it in built()["data"]["items"] if it.get("ly")}
        tree = KR.tree_ids()
        self.assertFalse(set(tree.values()) & layer)
        self.assertEqual(tree["jehoiakim"], "jehoiakim")  # also called Eliakim


class TheLines(unittest.TestCase):
    def setUp(self):
        self.data = built()["data"]
        self.items = self.data["items"]
        self.matthew = self.data["lines"][0][1]
        self.luke = self.data["lines"][1][1]

    def is_named(self, name, i):
        """Whether item `i` is the box of a Gospel's `name`, by its label and
        the fixed table, never by an alias add_items may itself have written."""
        it = self.items[i]
        return it["n"] == (name if it.get("ly") else GL.SPELL.get(name, name))

    def test_matthew_is_the_reading_in_order(self):
        keys = []
        for v, names in matthew_tree.READING:
            if 2 <= v <= 16:
                keys += [k for k in names
                         if k not in GL.NOT_ON_LINE and k not in keys]
        want = [GL.tail_name(k) for k in keys]
        self.assertEqual(len(self.matthew), 41)
        self.assertEqual(len(want), 41)
        for name, i in zip(want, self.matthew):
            self.assertTrue(self.is_named(name, i), (name, self.items[i]["n"]))

    def test_matthew_skips_those_he_skips(self):
        names = {self.items[i]["n"] for i in self.matthew}
        self.assertFalse(names & {*matthew_tree.PASSED, "Tamar", "Mary"})

    def test_luke_is_the_text_position_by_position(self):
        slots, _ = generate_luke3.build_grid(generate_luke3.extract_line())
        self.assertEqual(len(self.luke), 77)
        self.assertEqual(len(slots), 77)
        for (name, v), i in zip(slots, self.luke):
            self.assertTrue(self.is_named(name, i), (name, v, self.items[i]["n"]))

    @staticmethod
    def above(box):
        out = []
        while box.parent is not None:
            box = box.parent
            out.append(box)
        return out

    def test_matthews_boxes_run_down_the_trees_own_line(self):
        L = built()["S"].lines
        boxes = [b for _k, b in L.matthew if b is not None]
        self.assertEqual(len(boxes), 30)
        for a, b in zip(boxes, boxes[1:]):
            if (a, b) == (L.shealtiel, L.zerubbabel):
                continue            # 1 Chronicles 3:19 hangs him under Pedaiah
            self.assertIn(a, self.above(b), (a.label, b.label))

    def test_lukes_boxes_run_up_the_trees_own_line(self):
        L = built()["S"].lines
        names = [s[0] for s in L.luke]
        boxes = [b for _n, _v, b in L.luke[names.index("David"):] if b is not None]
        self.assertEqual(len(boxes), 33)
        for a, b in zip(boxes, boxes[1:]):
            self.assertIn(b, self.above(a), (a.label, b.label))
        self.assertIn(L.david, self.above(L.nathan))
        self.assertEqual(L.nathan.parent, L.david)

    def test_each_tree_box_has_the_row_of_its_own_slot(self):
        # Kenan's alias Cainan is spoken in 3:36 too, so the names can't tell
        b = built()
        index = {n: i for i, n in enumerate(CT.walk(b["T"].root))}
        luke = self.data["books"].index("Luke")
        for nm, v, box in b["S"].lines.luke:
            if box is not None:
                self.assertIn([luke, 3, v, 0, 0], self.items[index[box]]["r"], (nm, v))

    def test_the_two_cainans(self):
        by_id = {it["id"]: i for i, it in enumerate(self.items)}
        self.assertEqual(self.luke[63], by_id["cainan.luke-3-36"])
        self.assertEqual(self.luke[72], by_id["kenan"])
        aliased = [it["id"] for it in self.items if "Cainan" in it.get("a", [])]
        self.assertEqual(aliased, ["kenan"])

    def test_only_the_same_men_are_shared(self):
        # So Matthan and Matthat, the Eliakims, the Jacobs and Luke's Josephs
        # can never read as a meeting.
        shared = {self.items[i]["id"] for i in set(self.matthew) & set(self.luke)}
        self.assertEqual(shared, {
            "abram-abraham", "isaac", "israel", "judah", "perez", "hezron.perez",
            "ram.hezron", "amminadab", "nahshon", "salma.nahshon", "boaz",
            "obed.boaz", "jesse", "david", "shealtiel", "zerubbabel",
            "joseph.mary", "jesus"})

    def test_no_name_from_the_timelines_list_gets_in(self):
        names = {it["n"] for it in self.items}
        self.assertFalse(names & {"Joda", "Josech"})

    def test_a_box_lists_each_line_it_is_on(self):
        for n, line in enumerate((self.matthew, self.luke)):
            for i in line:
                self.assertIn(n, self.items[i]["tl"], self.items[i]["id"])

    def test_no_card_makes_joseph_the_father_of_jesus(self):
        by_id = {it["id"]: it for it in self.items}
        at = {it["id"]: i for i, it in enumerate(self.items)}
        joseph, mary, jesus = (by_id[k] for k in ("joseph.mary", "mary.joseph", "jesus"))
        self.assertEqual(joseph["c"], [at["mary.joseph"]])
        self.assertNotIn("c", mary)     # the card would read "With Mary: Jesus"
        self.assertNotIn("p", jesus)
        self.assertEqual(mary["rows"], [["Son, Matthew 1:16", [at["jesus"]]]])
        for _label, chips in joseph["rows"]:
            self.assertNotIn(at["jesus"], chips)

    def test_jesus_date_is_ussher_alone(self):
        self.assertEqual(next(it for it in self.items if it["id"] == "jesus")["d"],
                         "4 BC (Ussher) · AM 4000")

    def test_the_counts_the_cards_state(self):
        S = built()["S"]
        L = S.lines
        keys = [k for k, _b in L.matthew]
        kings = keys.index("Shealtiel") - keys.index("David") - 1
        self.assertEqual(kings, 14)
        self.assertEqual(len(L.upper) + 1, 20)
        self.assertEqual(L.shealtiel.gen - L.david.gen - 1, 18)
        self.assertEqual(len(GL.TAIL), 9)
        self.assertEqual(len(L.lower), 18)
        self.assertEqual(2 + len(GL.TAIL) + kings, 25)
        self.assertEqual(2 + len(L.lower) + len(L.upper) + 1, 40)
        self.assertEqual(len(L.luke) - 1, 76)
        self.assertEqual(L.zerubbabel.gen + 9 + 2, 64)
        cards = json.dumps(self.items, ensure_ascii=False)
        for said in ("Matthew has 14 names, Luke 20 and this tree 18 generations",
                     "Matthew has 9 names on to Jacob, Luke 18 on to Heli",
                     "Matthew has 25 names, Luke 40",
                     "the 76th from Adam", "the 64th"):
            self.assertIn(said, cards)


class TheDrawing(unittest.TestCase):
    """What the sheet's two layer groups hold, not what the layout says."""

    def setUp(self):
        b = built()
        self.S, self.items = b["S"], b["data"]["items"]
        self.left, self.top = b["left"], b["top"]
        self.lines, self.boxes = layer_groups(b["svg"])

    def elements(self, group, tag):
        return [attrs(e) for e in re.findall(rf"<{tag} [^>]*/?>", group)]

    def test_every_item_on_the_layer_is_drawn_where_its_card_says(self):
        rects = {tuple(round(float(r[k]), 1) for k in ("x", "y", "width", "height"))
                 for r in self.elements(self.boxes, "rect")}
        for it in self.items:
            if it.get("ly"):
                x, y, w, h = it["b"]
                self.assertIn((round(x + self.left, 1), round(y + self.top, 1),
                               round(w, 1), round(h, 1)), rects, it["id"])

    def test_every_hop_is_painted_before_its_line(self):
        lines = self.elements(self.lines, "line")
        hops = [ln for ln in lines if ln["stroke"] == _rgb(G.BG) and ln["stroke-width"] == "6"]
        self.assertEqual(len(hops), len(self.S.hops))
        self.assertGreaterEqual(len(hops), 4)
        for x, y in self.S.hops:
            self.assertIn({"x1": _fmt(x), "y1": _fmt(y - 4), "x2": _fmt(x), "y2": _fmt(y + 4)},
                          [{k: ln[k] for k in ("x1", "y1", "x2", "y2")} for ln in hops])

    def test_joseph_to_jesus_is_dashed_and_only_dashed(self):
        S = self.S
        down = [ln for ln in self.elements(self.lines, "line")
                if ln["y1"] == _fmt(S.joseph.y + S.joseph.h) and ln["y2"] == _fmt(S.jesus.y)]
        self.assertEqual(len(down), 1)
        self.assertIn("stroke-dasharray", down[0])

    def test_mary_hangs_by_the_doubled_line_and_jesus_from_her(self):
        S = self.S
        lines = self.elements(self.lines, "line")
        to_mary = [ln for ln in lines if ln["y2"] == _fmt(S.mary.y)]
        self.assertEqual(len(to_mary), 2)
        self.assertEqual({ln["stroke"] for ln in to_mary}, {_rgb(G.FEMALE)})
        cx = _fmt(S.mary.x + S.mary.w / 2)
        self.assertTrue(any(ln["x1"] == cx and ln["y1"] == _fmt(S.mary.y + S.mary.h)
                            and ln["y2"] == _fmt(S.jesus.y)
                            and "stroke-dasharray" not in ln for ln in lines))

    def test_jesus_has_the_chi_rho_and_no_crown(self):
        S = self.S
        # draw_node crowns a king alone
        self.assertEqual((S.jesus.kind, S.jesus.icon), ("christ", "chi_rho"))
        self.assertEqual(G.accent(S.jesus), G.HL)

    def test_every_mark_and_label_is_written(self):
        S = self.S
        texts = re.findall(r"<text [^>]*>([^<]*)</text>", self.boxes)
        for _b, text in S.marks.values():
            self.assertIn(text, texts)
        for _x, _y, head, sub, _side in S.labels:
            self.assertIn(head, texts)
            self.assertIn(sub, texts)
        self.assertIn(S.supposed[2], texts)

    def test_both_strands_read_down_in_the_right_order(self):
        S = self.S
        L = S.lines
        for strand in (L.lower, L.upper):
            ys = [S.luke[slot[:2]].y for slot in reversed(strand)]
            self.assertEqual(ys, sorted(ys))
        self.assertLess(S.luke["Rhesa", 27].y, S.luke["Heli", 23].y)
        self.assertLess(S.luke["Mattatha", 31].y, S.luke["Neri", 27].y)
        tail = [S.tail[k].y for k in GL.TAIL]
        self.assertEqual(tail, sorted(tail))
        self.assertLess(S.luke["Heli", 23].y, S.joseph.y)
        self.assertLess(S.joseph.y, S.mary.y)
        self.assertLess(S.mary.y, S.jesus.y)


class Geometry(unittest.TestCase):
    CLEAR = 5

    def setUp(self):
        b = built()
        self.S, self.T = b["S"], b["T"]
        self.W, self.H, self.left, self.top = b["W"], b["H"], b["left"], b["top"]
        self.tree = [n for n in CT.walk(self.T.root)]
        self.lines = G.tree_lines(self.T.root)

    def rects(self):
        """(what, [x, y, w, h]) of everything the layer stands up, in layout
        coordinates."""
        S = self.S
        out = [(n.label, [n.x, n.y, n.w, n.h]) for n in S.boxes + [S.pill]]
        out += [("mark " + t, list(b)) for b, t in S.marks.values()]
        for x, y, head, sub, side in S.labels:
            w = max(G.F_NAME_B.getlength(head), G.F_LEGS.getlength(sub))
            out.append(("label " + head, [x - w if side == "r" else x, y - 10, w, 34]))
        x, y, text = S.supposed
        out.append(("supposed", [x, y - 8, G.F_LEGS.getlength(text), 16]))
        return out

    def test_every_box_stands_clear_of_the_trees(self):
        c = self.CLEAR
        for what, (x, y, w, h) in self.rects():
            for n in self.tree:
                self.assertFalse(
                    x - c < n.x + n.w and x + w + c > n.x
                    and y - c < n.y + n.h and y + h + c > n.y,
                    f"{what} is on {n.label}")

    def test_every_box_stands_inside_the_sheet(self):
        for what, (x, y, w, h) in self.rects():
            self.assertGreaterEqual(x - self.left, 0, what)
            self.assertGreaterEqual(y - self.top, 0, what)
            self.assertLessEqual(x + w - self.left, self.W, what)
            self.assertLessEqual(y + h - self.top, self.H, what)

    def test_no_box_stands_on_a_line_of_the_tree(self):
        for what, (x, y, w, h) in self.rects():
            for a, b in self.lines:
                self.assertFalse(
                    max(a[0], b[0]) >= x - 1 and min(a[0], b[0]) <= x + w + 1
                    and max(a[1], b[1]) >= y - 1 and min(a[1], b[1]) <= y + h + 1,
                    f"{what} is on a line {a} {b}")

    def test_no_box_stands_on_an_arc(self):
        arcs = [[G._bezier(cv, i / 400) for i in range(401)]
                for cv in G.link_routes(self.T)]
        for what, (x, y, w, h) in self.rects():
            for pts in arcs:
                self.assertFalse(any(x <= p[0] <= x + w and y <= p[1] <= y + h
                                     for p in pts), f"{what} is on an arc")

    def test_no_new_box_overlaps_another(self):
        rects = self.rects()
        for i, (w1, a) in enumerate(rects):
            for w2, b in rects[i + 1:]:
                self.assertFalse(a[0] < b[0] + b[2] and a[0] + a[2] > b[0]
                                 and a[1] < b[1] + b[3] and a[1] + a[3] > b[1],
                                 f"{w1} overlaps {w2}")

    def test_no_line_of_the_layer_passes_behind_a_tree_box(self):
        for run in self.S.runs:
            for a, b in zip(run, run[1:]):
                x0, x1 = min(a[0], b[0]), max(a[0], b[0])
                y0, y1 = min(a[1], b[1]), max(a[1], b[1])
                for n in self.tree:
                    self.assertFalse(x0 < n.x + n.w and x1 > n.x
                                     and y0 < n.y + n.h and y1 > n.y,
                                     f"{a}-{b} passes behind {n.label}")

    def test_a_crossing_of_the_trees_lines_is_always_a_hop(self):
        hops = set(self.S.hops)
        self.assertGreaterEqual(len(hops), 4)
        for run in self.S.runs:
            for a, b in zip(run, run[1:]):
                vertical = a[0] == b[0]
                for p, q in self.lines:
                    if vertical and p[1] == q[1] \
                            and min(a[1], b[1]) < p[1] < max(a[1], b[1]) \
                            and min(p[0], q[0]) < a[0] < max(p[0], q[0]):
                        self.assertIn((a[0], p[1]), hops)
                    if not vertical and p[0] == q[0] \
                            and min(a[0], b[0]) < p[0] < max(a[0], b[0]) \
                            and min(p[1], q[1]) < a[1] < max(p[1], q[1]):
                        self.fail(f"{a}-{b} crosses a drop at x {p[0]}")

    def test_the_arc_passes_behind_no_box(self):
        S = self.S
        grid = G._box_grid(self.tree + S.boxes + [S.pill])
        score = G._route_score(S.route, S.pill, S.lines.shealtiel, grid, None)
        self.assertEqual(score[:2], (0, 0))

    def test_each_column_stands_on_its_own_line_under_its_own_label(self):
        S = self.S
        luke_x, matthew_x = S.runs[1][-1][0], S.runs[2][0][0]
        for k in GL.TAIL:
            self.assertAlmostEqual(S.tail[k].x + S.tail[k].w / 2, matthew_x, msg=k)
        for slot in S.lines.lower:
            b = S.luke[slot[:2]]
            self.assertAlmostEqual(b.x + b.w / 2, luke_x, msg=slot[0])
        at = {head: x for x, _y, head, _sub, _side in S.labels}
        self.assertLess(at["MATTHEW 1:13-15"], matthew_x)
        self.assertGreater(at["LUKE 3:23-27"], luke_x)

    def test_both_columns_end_on_the_one_joseph(self):
        S = self.S
        j = S.joseph
        for x, y in (S.runs[1][-1], S.runs[2][-1]):
            self.assertEqual(y, j.y)
            self.assertTrue(j.x < x < j.x + j.w)

    def test_no_solid_line_joins_joseph_to_jesus(self):
        S = self.S
        joseph_end = S.joseph.y + S.joseph.h
        for run in S.runs:
            for a, b in zip(run, run[1:]):
                self.assertFalse(a[1] == joseph_end and b[1] == S.jesus.y)


class Verses(unittest.TestCase):
    def setUp(self):
        self.data = built()["data"]
        self.items = self.data["items"]
        self.books = self.data["books"]
        self.by_id = {it["id"]: it for it in self.items}

    def verses(self, row):
        book, c1, v1, c2, v2 = row
        book = self.books[book]
        if c2:
            self.fail(f"a row across chapters: {row}")
        for v in range(v1, (v2 or v1) + 1):
            yield book, c1, v

    def test_a_new_persons_verses_speak_the_name(self):
        for it in self.items:
            if not it.get("ly") or it.get("nos") or it.get("x") is not None:
                continue
            for row in it["r"]:
                for book, c, v in self.verses(row):
                    if (it["id"], book, v) == ("jesus", "Matthew", 17):
                        continue    # "to the Christ"
                    self.assertTrue(FT.speaks(it["n"], book, c, v),
                                    f"{it['id']}: {book} {c}:{v}")

    def test_a_tree_boxes_luke_verses_speak_one_of_its_names(self):
        luke = self.books.index("Luke")
        for it in self.items:
            if it.get("ly"):
                continue
            for row in it.get("r", []):
                if row[0] != luke:
                    continue
                said = [nm for nm in FT.names(it["n"]) + it.get("a", [])
                        if FT.speaks(nm, "Luke", 3, row[2])]
                self.assertTrue(said, f"{it['id']}: Luke 3:{row[2]}")

    def written(self):
        """Every sentence the layer adds to a card: its own items' words, and
        what it adds to the tree's boxes."""
        tree = built()["tree_only"]["items"]
        for i, it in enumerate(self.items):
            if it.get("ly"):
                yield it["id"], it.get("s", "")
                yield it["id"], it.get("note", "")
                for _label, text in it.get("tx", []):
                    yield it["id"], text
                continue
            old = tree[i]
            if it.get("note") != old.get("note"):
                yield it["id"], it["note"]
            for _o, why in it.get("xr", [])[len(old.get("xr", [])):]:
                yield it["id"], why

    def test_every_written_reference_parses_and_exists(self):
        # a bare "1:8" belongs to the book last named; Luke, where none is yet
        ref = re.compile(r"((?:\d )?[A-Z][a-z]+ )?(\d+:\d+(?:-\d+)?)")
        seen = 0
        for who, text in self.written():
            book = "Luke"
            for m in ref.finditer(text):
                book = (m.group(1) or book + " ").strip()
                if book not in BOOK_NAMES:
                    continue
                c, _, vs = m.group(2).partition(":")
                for v in vs.split("-"):     # both ends of a range
                    self.assertTrue(FT.verse_text(book, int(c), int(v)),
                                    f"{who}: {book} {c}:{v}")
                    seen += 1
                verse_refs.parse(f"{book} {m.group(2)}", book)
        self.assertGreater(seen, 100)

    def test_a_spelling_cited_to_a_verse_is_that_verses(self):
        # "Jechoniah in Matthew 1:12, Jeconiah in 1 Chronicles 3:17"
        cite = re.compile(r"\b([A-Z][a-z]+) in ((?:\d )?[A-Z][a-z]+) (\d+):(\d+)")
        seen = 0
        for who, text in self.written():
            for name, book, c, v in cite.findall(text):
                if book in BOOK_NAMES and name in ("Jechoniah", "Jeconiah"):
                    self.assertTrue(FT.speaks(name, book, int(c), int(v)),
                                    f"{who}: {name} in {book} {c}:{v}")
                    seen += 1
        self.assertGreaterEqual(seen, 2)

    def test_a_sentence_cites_the_verses_that_name_who_it_says(self):
        # Cainan's relation to Shelah spans two verses
        cainan = next(it for it in self.items if it["id"] == "cainan.luke-3-36")
        self.assertIn("Luke 3:35-36", cainan["note"])
        self.assertTrue(FT.speaks("Shelah", "Luke", 3, 35))
        self.assertTrue(FT.speaks("Cainan", "Luke", 3, 36))

    def test_every_quotation_is_in_its_verses(self):
        for it in self.items:
            if not it.get("pc"):
                continue
            for _label, text in it["tx"]:
                for quoted in re.findall(r"“([^”]+)”", text):
                    quoted = quoted.rstrip(".")
                    verses = [FT.verse_text(b, c, v)
                              for _g, rows in it["rg"] for row in rows
                              for b, c, v in self.verses(row)]
                    self.assertTrue(any(quoted in t for t in verses), quoted)

    def test_every_verse_of_both_genealogies_lands_on_a_name(self):
        for book, ch, verses in (("Matthew", 1, range(1, 18)),
                                 ("Luke", 3, range(23, 39))):
            b = self.books.index(book)
            for v in verses:
                hit = [it["n"] for it in self.items
                       if it.get("x") is None and not it.get("nos")
                       and any(r[0] == b and r[1] == ch and r[2] == v and not r[3]
                               for r in it.get("r", []))]
                self.assertTrue(hit, f"{book} {ch}:{v}")

    def test_the_audit_is_unchanged(self):
        self.assertEqual(len(built()["misses"]), 12)

    def test_stops_step_in_order(self):
        order = ["god.luke-3-38", "stop.matthew-opens", "stop.part-david",
                 "stop.meet-shealtiel", "stop.part-zerubbabel", "stop.meet-joseph"]
        at = {it["id"]: i for i, it in enumerate(self.items)}
        for n, sid in enumerate(order):
            before, after = self.by_id[sid]["st"]
            self.assertEqual(before, at[order[n - 1]] if n else None)
            self.assertEqual(after, at[order[n + 1]] if n + 1 < len(order) else None)

    def test_the_layer_is_off_when_the_sheet_opens(self):
        self.assertEqual(self.data["layers"][0]["id"], GL.LAYER)
        self.assertFalse(self.data["layers"][0]["on"])


if __name__ == "__main__":
    unittest.main()
