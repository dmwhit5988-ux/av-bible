"""Freeze a verse SVG's SMIL animations to their end state and demote it to
a static base group — the "start from previous verse's final frame" tool
(SVG_STUDIO_DESIGN.md section 3).

For hand-authored sequences only: each verse is the prior verse's steady
state plus one new reveal, so verse N starts as verse N-1 with its play-once
animations frozen at their final values, wrapped in a flat
<g class="frozen-base">, plus an empty overlay <g> for the new elements.
Generator families never come through here — they already build
cumulatively from their Python spec.

The normative case table (anything not listed: warn and preserve, never
invent):

  repeatCount="indefinite"              -> keep unchanged (steady-state
                                           ambience, e.g. the tabernacle
                                           pulse, IS part of the final frame)
  <animate>/<set> fill="freeze"         -> write final value onto the parent
                                           as a presentation attribute,
                                           remove the node
  <animate>/<set> without fill="freeze" -> the element snaps back to its
                                           base value at the end; remove the
                                           node, warn
  additive="sum" or by=-only            -> keep, warn (freezing would need
                                           the animated base value)
  animateTransform / animateMotion      -> keep, warn (no house generator
                                           emits these)

Special case: a frozen stroke-dashoffset of 0 deletes both stroke-dashoffset
and stroke-dasharray instead — a fully revealed traced line becomes a plain
polyline with no leftover dash plumbing.

Pure functions, no tkinter, no I/O: independently testable
(test_svg_freeze.py).
"""

import xml.etree.ElementTree as ET
from dataclasses import dataclass, field

SVGNS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVGNS)

_ANIM_TAGS = {"animate", "set", "animateTransform", "animateMotion"}


@dataclass
class FreezeResult:
    svg_text: str
    warnings: list = field(default_factory=list)


def _local(tag):
    return tag.rsplit("}", 1)[-1]


def _final_value(node):
    """Last `values` entry, else `to`, else None (malformed)."""
    values = node.get("values")
    if values:
        parts = [p.strip() for p in values.split(";") if p.strip()]
        if parts:
            return parts[-1]
    return node.get("to")


def _describe(node, parent):
    return (f'<{_local(node.tag)} attributeName='
            f'"{node.get("attributeName", "?")}"> on <{_local(parent.tag)}>')


def freeze_animations(root, warnings):
    """Apply the case table to every animation node under `root`, in
    document order (so a later animate on the same attribute wins, matching
    SMIL's sandwich model for our non-additive cases)."""
    # ET has no parent pointers; collect (parent, node) in document order
    # first — removing while iterating breaks .iter().
    targets = []
    for parent in root.iter():
        for node in list(parent):
            if _local(node.tag) in _ANIM_TAGS:
                targets.append((parent, node))

    for parent, node in targets:
        tag = _local(node.tag)
        if node.get("repeatCount") == "indefinite":
            continue  # perpetual: part of the final frame, keep
        if tag in ("animateTransform", "animateMotion"):
            warnings.append(f"{_describe(node, parent)} not frozen — "
                            f"element left animated")
            continue
        if node.get("additive") == "sum" or (
                node.get("by") is not None and _final_value(node) is None):
            warnings.append(f"{_describe(node, parent)} is additive — "
                            f"kept animated (freezing needs the animated "
                            f"base value)")
            continue
        if node.get("fill") != "freeze":
            warnings.append(f"{_describe(node, parent)} without "
                            f'fill="freeze" removed (reverts to base value)')
            parent.remove(node)
            continue
        attr = node.get("attributeName")
        value = _final_value(node)
        if not attr or value is None:
            warnings.append(f"{_describe(node, parent)} malformed — kept")
            continue
        try:
            is_zero = float(value) == 0.0
        except ValueError:
            is_zero = False
        if attr == "stroke-dashoffset" and is_zero:
            # Fully revealed traced line: drop the dash plumbing entirely.
            parent.attrib.pop("stroke-dashoffset", None)
            parent.attrib.pop("stroke-dasharray", None)
        else:
            parent.set(attr, value)
        parent.remove(node)


def freeze_to_base(svg_text: str, from_key: str,
                   new_verse: int | None = None) -> FreezeResult:
    """Turn verse N-1's SVG (`svg_text`, verse key `from_key` e.g.
    "Acts_13_4") into the starting document for verse N: animations frozen
    per the case table, everything but <defs> demoted into one flat
    <g class="frozen-base" data-from="…lineage…">, and an empty overlay
    <g id="vN"> appended for the new verse's elements."""
    warnings = []
    root = ET.fromstring(svg_text)

    freeze_animations(root, warnings)

    defs, content = [], []
    for child in list(root):
        (defs if _local(child.tag) == "defs" else content).append(child)
        root.remove(child)

    # Lineage: append from_key to a prior frozen base's data-from and hoist
    # its children — the base stays one flat group however long the chain.
    lineage = from_key
    flat = []
    def _is_empty_group(el):
        # A <g> whose children are only comments/PIs (e.g. the previous
        # verse's never-filled overlay) — drop it rather than carry husks
        # forward. Real overlay content keeps its <g> wrapper inside the
        # base; only frozen-base groups themselves are hoisted flat.
        return (_local(el.tag) == "g"
                and not [c for c in el if isinstance(c.tag, str)])

    for child in content:
        if (_local(child.tag) == "g"
                and child.get("class") == "frozen-base"):
            prior = child.get("data-from", "").strip()
            if prior:
                lineage = f"{prior} {from_key}"
            flat.extend(c for c in child if not _is_empty_group(c))
        elif not _is_empty_group(child):
            flat.append(child)

    base = ET.Element(f"{{{SVGNS}}}g",
                      {"class": "frozen-base", "data-from": lineage})
    base.extend(flat)

    if new_verse is None:
        try:
            new_verse = int(from_key.rsplit("_", 1)[-1]) + 1
        except ValueError:
            new_verse = 0
    overlay = ET.Element(f"{{{SVGNS}}}g", {"id": f"v{new_verse}"})
    overlay.append(ET.Comment(
        f" verse {new_verse}: add this verse's elements here; "
        f"prefix new ids with v{new_verse}- to avoid clashes with frozen "
        f"clip ids "))

    for d in defs:
        root.append(d)
    root.append(base)
    root.append(overlay)

    return FreezeResult(ET.tostring(root, encoding="unicode"), warnings)
