"""Unit tests for svg_freeze — one test per row of the normative case table
(SVG_STUDIO_DESIGN.md section 3) plus round-trips of real generator output.

    .venv\\Scripts\\python.exe -m unittest test_svg_freeze -v
"""

import os
import unittest
import xml.etree.ElementTree as ET

from svg_freeze import SVGNS, FreezeResult, freeze_to_base

HERE = os.path.dirname(os.path.abspath(__file__))


def wrap(inner):
    return (f'<svg xmlns="{SVGNS}" viewBox="0 0 1024 576" width="1024" '
            f'height="576">{inner}</svg>')


def parse(result: FreezeResult):
    return ET.fromstring(result.svg_text)


def find_all(root, local):
    return [e for e in root.iter() if e.tag == f"{{{SVGNS}}}{local}"]


def base_group(root):
    gs = [g for g in find_all(root, "g") if g.get("class") == "frozen-base"]
    assert len(gs) == 1, f"expected exactly one frozen-base, got {len(gs)}"
    return gs[0]


class FreezeCases(unittest.TestCase):
    def test_traced_polyline_dash_attrs_removed(self):
        # SvgCanvas.traced(): dash-reveal that freezes at offset 0 becomes a
        # plain polyline — both dash attributes deleted, animate gone.
        svg = wrap(
            '<polyline points="0,0 100,0" stroke="rgb(1,2,3)" fill="none" '
            'stroke-dasharray="100" stroke-dashoffset="100">'
            '<animate attributeName="stroke-dashoffset" values="100;0" '
            'dur="2.4s" begin="0s" fill="freeze"/></polyline>')
        root = parse(freeze_to_base(svg, "Acts_13_4"))
        (line,) = find_all(root, "polyline")
        self.assertIsNone(line.get("stroke-dasharray"))
        self.assertIsNone(line.get("stroke-dashoffset"))
        self.assertFalse(find_all(root, "animate"))

    def test_grown_polygon_freezes_final_opacity(self):
        # SvgCanvas.grown(): fill-opacity ends at the hi value.
        svg = wrap(
            '<polygon points="0,0 1,0 1,1" fill="rgb(1,2,3)" '
            'fill-opacity="0.235">'
            '<animate attributeName="fill-opacity" values="0.235;0.588" '
            'dur="2.6s" fill="freeze"/></polygon>')
        root = parse(freeze_to_base(svg, "Numbers_34_6"))
        (poly,) = find_all(root, "polygon")
        self.assertEqual(poly.get("fill-opacity"), "0.588")
        self.assertFalse(find_all(root, "animate"))

    def test_grow_rect_freezes_full_width(self):
        # SvgAnimLayer.grow_rect(): width wipes from start to full.
        svg = wrap(
            '<rect x="10" y="10" width="120" height="8" fill="rgb(1,2,3)">'
            '<animate attributeName="width" values="40;120" dur="2.4s" '
            'fill="freeze"/></rect>')
        root = parse(freeze_to_base(svg, "Genesis_5_7"))
        (rect,) = find_all(root, "rect")
        self.assertEqual(rect.get("width"), "120")

    def test_indefinite_pulse_kept(self):
        # group(pulse=...): the perpetual breathing glow is steady-state
        # ambience — part of the final frame, untouched.
        svg = wrap(
            '<g opacity="0.3"><animate attributeName="opacity" '
            'values="0.3;0.8;0.3" dur="3s" repeatCount="indefinite"/>'
            '<rect x="0" y="0" width="5" height="5"/></g>')
        result = freeze_to_base(svg, "Exodus_25_31")
        root = parse(result)
        (anim,) = find_all(root, "animate")
        self.assertEqual(anim.get("repeatCount"), "indefinite")
        self.assertEqual(result.warnings, [])

    def test_non_freeze_animate_removed_with_warning(self):
        svg = wrap(
            '<circle cx="1" cy="1" r="4" fill-opacity="0.2">'
            '<animate attributeName="fill-opacity" values="0.2;1" '
            'dur="1s"/></circle>')
        result = freeze_to_base(svg, "John_1_1")
        root = parse(result)
        (circle,) = find_all(root, "circle")
        self.assertEqual(circle.get("fill-opacity"), "0.2")  # base value
        self.assertFalse(find_all(root, "animate"))
        self.assertEqual(len(result.warnings), 1)
        self.assertIn('without fill="freeze"', result.warnings[0])

    def test_additive_kept_with_warning(self):
        svg = wrap(
            '<rect x="0" y="0" width="10" height="10">'
            '<animate attributeName="width" by="5" dur="1s" fill="freeze" '
            'additive="sum"/></rect>')
        result = freeze_to_base(svg, "John_1_1")
        root = parse(result)
        self.assertEqual(len(find_all(root, "animate")), 1)  # preserved
        (rect,) = find_all(root, "rect")
        self.assertEqual(rect.get("width"), "10")            # untouched
        self.assertIn("additive", result.warnings[0])

    def test_animate_transform_kept_with_warning(self):
        svg = wrap(
            '<rect x="0" y="0" width="10" height="10">'
            '<animateTransform attributeName="transform" type="rotate" '
            'from="0" to="90" dur="1s" fill="freeze"/></rect>')
        result = freeze_to_base(svg, "John_1_1")
        root = parse(result)
        self.assertEqual(len(find_all(root, "animateTransform")), 1)
        self.assertIn("not frozen", result.warnings[0])

    def test_set_applies_to_value(self):
        svg = wrap(
            '<text x="1" y="1" opacity="0">'
            '<set attributeName="opacity" to="1" begin="1s" '
            'fill="freeze"/></text>')
        root = parse(freeze_to_base(svg, "John_1_1"))
        (text,) = find_all(root, "text")
        self.assertEqual(text.get("opacity"), "1")
        self.assertFalse(find_all(root, "set"))

    def test_same_attribute_document_order_last_wins(self):
        svg = wrap(
            '<rect x="0" y="0" width="10" height="10" opacity="0">'
            '<animate attributeName="opacity" values="0;0.5" dur="1s" '
            'fill="freeze"/>'
            '<animate attributeName="opacity" values="0.5;1" dur="1s" '
            'begin="1s" fill="freeze"/></rect>')
        root = parse(freeze_to_base(svg, "John_1_1"))
        (rect,) = find_all(root, "rect")
        self.assertEqual(rect.get("opacity"), "1")

    def test_structure_defs_base_overlay(self):
        svg = wrap(
            '<defs><clipPath id="clip1"><rect width="5" height="5"/>'
            '</clipPath></defs>'
            '<rect x="0" y="0" width="10" height="10"/>'
            '<text x="1" y="1">hello</text>')
        root = parse(freeze_to_base(svg, "Acts_13_4"))
        self.assertEqual(root.get("viewBox"), "0 0 1024 576")
        kids = list(root)
        self.assertEqual([k.tag.rsplit('}', 1)[-1] for k in kids],
                         ["defs", "g", "g"])
        base = base_group(root)
        self.assertEqual(base.get("data-from"), "Acts_13_4")
        self.assertEqual(len(list(base)), 2)  # rect + text moved in
        overlay = kids[2]
        self.assertEqual(overlay.get("id"), "v5")

    def test_double_freeze_stays_flat_with_lineage(self):
        svg = wrap('<rect x="0" y="0" width="10" height="10"/>')
        first = freeze_to_base(svg, "Acts_13_3")
        second = freeze_to_base(first.svg_text, "Acts_13_4")
        root = parse(second)
        base = base_group(root)  # asserts exactly one — no nesting
        self.assertEqual(base.get("data-from"), "Acts_13_3 Acts_13_4")
        # the rect was hoisted, not wrapped in a second group
        self.assertEqual(
            [k.tag.rsplit('}', 1)[-1] for k in base], ["rect"])


class RealOutputRoundTrips(unittest.TestCase):
    """Freeze real generator output: afterwards no play-once animation
    remains, indefinite pulses survive, and no warnings fire (the house
    generators emit only table-covered cases)."""

    def _roundtrip(self, rel_path, from_key):
        path = os.path.join(HERE, "visuals", rel_path)
        with open(path, encoding="utf-8") as f:
            result = freeze_to_base(f.read(), from_key)
        self.assertEqual(result.warnings, [])
        root = parse(result)
        for anim in (find_all(root, "animate") + find_all(root, "set")):
            self.assertEqual(anim.get("repeatCount"), "indefinite",
                             "a play-once animation survived the freeze")
        return root

    def test_genealogy_verse(self):
        root = self._roundtrip(os.path.join("Genesis", "5",
                                            "Genesis_5_3.KJV.svg"),
                               "Genesis_5_3")
        base_group(root)

    def test_tribal_map_traced_verse(self):
        root = self._roundtrip(os.path.join("Numbers", "34",
                                            "Numbers_34_6.svg"),
                               "Numbers_34_6")
        # every traced border froze to "fully drawn": no dash-offset remains
        for el in root.iter():
            self.assertIsNone(el.get("stroke-dashoffset"))

    def test_tabernacle_pulse_survives(self):
        root = self._roundtrip(os.path.join("Exodus", "26",
                                            "Exodus_26_1.svg"),
                               "Exodus_26_1")
        pulses = [a for a in find_all(root, "animate")
                  if a.get("repeatCount") == "indefinite"]
        self.assertTrue(pulses, "the breathing glow should survive")


if __name__ == "__main__":
    unittest.main()
