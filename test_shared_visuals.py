"""One picture across several verses (D17): range files and identical-copy
runs in build_manifest, and the shared clock in video_render.

    .venv\\Scripts\\python.exe -m unittest test_shared_visuals -v

The manifest tests build into a temporary visuals/ folder. Genesis 12 is used
because it has no visuals of its own and no registry owner; WEB gives it 20
verses.
"""

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import build_manifest
import svg_registry
import video_render
from video_render import Item, assign_clocks, MOTION_TAIL


def svg(width: int, animate: str = "") -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10">'
            f'<rect width="{width}" height="1">{animate}</rect></svg>')


def opted_out(*_args, **_kwargs):
    return svg_registry.FamilyInfo(
        label="test", book="Genesis", chapters=(12,), generator="x.py",
        spec=(), replay_identical=True)


class ManifestSharing(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        root = Path(self._tmp.name)
        self.chapter = root / "Genesis" / "12"
        self.chapter.mkdir(parents=True)
        self._saved = build_manifest.VISUALS_DIR, build_manifest.MANIFEST_PATH
        build_manifest.VISUALS_DIR = root
        build_manifest.MANIFEST_PATH = root / "manifest.json"

    def tearDown(self):
        build_manifest.VISUALS_DIR, build_manifest.MANIFEST_PATH = self._saved
        self._tmp.cleanup()

    def put(self, name: str, text: str):
        (self.chapter / name).write_text(text, encoding="utf-8")

    def build(self) -> dict:
        entries = build_manifest.build_manifest()
        return {key: records[0]["file"].split("/")[-1]
                for key, records in entries.items()}

    def test_range_file_supplies_each_verse(self):
        self.put("Genesis_12_1-3.svg", svg(1))
        files = self.build()
        self.assertEqual([files.get(f"Genesis_12_{v}") for v in (1, 2, 3)],
                         ["Genesis_12_1-3.svg"] * 3)
        self.assertNotIn("Genesis_12_4", files)

    def test_single_verse_range(self):
        self.put("Genesis_12_5-5.svg", svg(1))
        self.assertEqual(self.build().get("Genesis_12_5"), "Genesis_12_5-5.svg")

    def test_range_past_the_chapter_keeps_only_web_verses(self):
        self.put("Genesis_12_18-25.svg", svg(1))
        keys = sorted(k for k in self.build() if k.startswith("Genesis_12_"))
        self.assertEqual(keys, ["Genesis_12_18", "Genesis_12_19", "Genesis_12_20"])

    def test_own_file_wins_over_a_range(self):
        self.put("Genesis_12_1-3.svg", svg(1))
        self.put("Genesis_12_2.svg", svg(2))
        files = self.build()
        self.assertEqual(files["Genesis_12_2"], "Genesis_12_2.svg")
        self.assertEqual(files["Genesis_12_3"], "Genesis_12_1-3.svg")

    def test_overlapping_ranges_name_sorting_first_wins(self):
        self.put("Genesis_12_1-3.svg", svg(1))
        self.put("Genesis_12_2-5.svg", svg(2))
        files = self.build()
        self.assertEqual(files["Genesis_12_3"], "Genesis_12_1-3.svg")
        self.assertEqual(files["Genesis_12_4"], "Genesis_12_2-5.svg")

    def test_identical_copies_share_the_first_file(self):
        self.put("Genesis_12_7.svg", svg(1))
        self.put("Genesis_12_8.svg", svg(1))
        self.put("Genesis_12_9.svg", svg(2))
        files = self.build()
        self.assertEqual(files["Genesis_12_8"], "Genesis_12_7.svg")
        self.assertEqual(files["Genesis_12_9"], "Genesis_12_9.svg")

    def test_a_range_is_never_taken_over_by_an_identical_copy(self):
        self.put("Genesis_12_6.svg", svg(3))
        self.put("Genesis_12_7-9.svg", svg(3))
        files = self.build()
        self.assertEqual([files[f"Genesis_12_{v}"] for v in (7, 8, 9)],
                         ["Genesis_12_7-9.svg"] * 3)

    def test_replay_identical_opts_out(self):
        self.put("Genesis_12_7.svg", svg(1))
        self.put("Genesis_12_8.svg", svg(1))
        with mock.patch.object(build_manifest.svg_registry, "owner_of", opted_out):
            files = self.build()
        self.assertEqual(files["Genesis_12_8"], "Genesis_12_8.svg")

    def test_manifest_written(self):
        self.put("Genesis_12_1-2.svg", svg(1))
        self.build()
        data = json.loads(build_manifest.MANIFEST_PATH.read_text())
        self.assertEqual(data["version"], 2)
        self.assertEqual(set(data["entries"]), {"Genesis_12_1", "Genesis_12_2"})


ONCE = '<animate attributeName="width" from="0" to="1" dur="1s" fill="freeze"/>'
LOOP = '<animate attributeName="opacity" values="1;0.5;1" dur="2s" repeatCount="indefinite"/>'
FPS = 30


def verse(n, text, path, frames=60, chapter=12):
    return Item(kind="verse", ref=f"Genesis {chapter}:{n}", chapter=chapter,
                verse=n, svg_text=text, svg_path=path, frames=frames)


class VideoClock(unittest.TestCase):
    def test_a_shared_picture_continues_its_clock(self):
        title = Item(kind="title", ref="t", svg_text=svg(9, ONCE), frames=30)
        items = [title,
                 verse(1, svg(1, ONCE), "a.svg"),
                 verse(2, svg(1, ONCE), "b.svg"),     # identical copy
                 verse(3, svg(1, ONCE), "b.svg")]     # the very same file
        assign_clocks(items, FPS, "Genesis")
        self.assertEqual([i.clock_offset for i in items], [0.0, 0.0, 2.0, 4.0])
        self.assertAlmostEqual(items[1].motion_seconds, 1.0 + MOTION_TAIL)
        self.assertEqual([i.motion_frames for i in items[2:]], [0, 0])
        self.assertEqual([i.start_frame for i in items], [0, 30, 90, 150])

    def test_a_different_picture_starts_at_zero(self):
        items = [verse(1, svg(1, ONCE), "a.svg"), verse(2, svg(2, ONCE), "c.svg")]
        assign_clocks(items, FPS, "Genesis")
        self.assertEqual(items[1].clock_offset, 0.0)
        self.assertGreater(items[1].motion_frames, 0)

    def test_a_perpetual_animation_keeps_moving(self):
        items = [verse(1, svg(1, LOOP), "a.svg"), verse(2, svg(1, LOOP), "a.svg")]
        assign_clocks(items, FPS, "Genesis")
        self.assertEqual(items[1].clock_offset, 2.0)
        self.assertEqual(items[1].motion_frames, items[1].frames)

    def test_copies_restart_across_a_chapter_but_one_file_holds(self):
        copy = [verse(9, svg(1, ONCE), "a.svg", chapter=12),
                verse(1, svg(1, ONCE), "b.svg", chapter=13)]
        held = [verse(9, svg(1, ONCE), "a.svg", chapter=12),
                verse(1, svg(1, ONCE), "a.svg", chapter=13)]
        assign_clocks(copy, FPS, "Genesis")
        assign_clocks(held, FPS, "Genesis")
        self.assertEqual(copy[1].clock_offset, 0.0)
        self.assertEqual(held[1].clock_offset, 2.0)

    def test_replay_identical_opts_copies_out(self):
        items = [verse(1, svg(1, ONCE), "a.svg"), verse(2, svg(1, ONCE), "b.svg"),
                 verse(3, svg(1, ONCE), "b.svg")]
        with mock.patch.object(video_render.svg_registry, "owner_of", opted_out):
            assign_clocks(items, FPS, "Genesis")
        self.assertEqual(items[1].clock_offset, 0.0)   # a copy: replays
        self.assertEqual(items[2].clock_offset, 2.0)   # the same file: holds


if __name__ == "__main__":
    unittest.main()
