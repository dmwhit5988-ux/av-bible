"""Consistency checks for svg_generators.json, the registry SVG Studio uses to
route "edit this verse" to the generator that owns it.

    .venv\\Scripts\\python.exe -m unittest test_registry -v

- every generator and spec file it names exists (and imports, for .py);
- no two families claim the same verse;
- every published verse SVG under visuals/<Book>/<ch>/ has an owner. This
  is the check that would have caught 2 Peter and Zephaniah shipping with no
  family at all;
- no visual carries a translation code (WEB is the only translation).
"""

import importlib
import os
import re
import unittest

import svg_registry

HERE = os.path.dirname(os.path.abspath(__file__))
VISUALS = os.path.join(HERE, "visuals")

# <Book>_<ch>_<v>.svg (the .still.svg reduced-motion twins don't match)
VERSE_SVG = re.compile(r"^(?P<book>.+)_(?P<ch>\d+)_(?P<v>\d+)\.svg$")

# WEB is the only translation (D9), so no visual may carry a translation code.
SUFFIXED = re.compile(r"\.(KJV|ASV|BBE|BSB|DARBY|DRA|YLT|OEB|WEB)\.")


def _overlap(a, b):
    """Whether two families of the same chapter could both own a verse."""
    if a.verses is None or b.verses is None:
        return True
    return a.verses[0] <= b.verses[1] and b.verses[0] <= a.verses[1]


class RegistryPaths(unittest.TestCase):
    def test_generator_and_spec_files_exist_and_import(self):
        for fam in svg_registry.families(force=True):
            for rel in [fam.generator] + [p.file for p in fam.spec]:
                with self.subTest(family=fam.label, file=rel):
                    self.assertTrue(os.path.isfile(os.path.join(HERE, rel)),
                                    f"{rel} does not exist")
                    if rel.endswith(".py"):
                        importlib.import_module(rel[:-3])


class RegistryOwnership(unittest.TestCase):
    def test_no_two_families_claim_a_verse(self):
        fams = svg_registry.families(force=True)
        for i, a in enumerate(fams):
            for b in fams[i + 1:]:
                shared = set(a.chapters) & set(b.chapters)
                if a.book == b.book and shared:
                    with self.subTest(a=a.label, b=b.label):
                        self.assertFalse(
                            _overlap(a, b),
                            f"both claim {a.book} {sorted(shared)}")

    def test_every_published_verse_svg_has_an_owner(self):
        orphans = []
        for book_dir in sorted(os.listdir(VISUALS)):
            book_path = os.path.join(VISUALS, book_dir)
            if not os.path.isdir(book_path):
                continue
            for ch_dir in sorted(os.listdir(book_path)):
                ch_path = os.path.join(book_path, ch_dir)
                if not (ch_dir.isdigit() and os.path.isdir(ch_path)):
                    continue
                for name in sorted(os.listdir(ch_path)):
                    if name.endswith(".still.svg"):
                        continue
                    m = VERSE_SVG.match(name)
                    if not m:
                        continue
                    book = m["book"].replace("_", " ")
                    if svg_registry.owner_of(book, int(m["ch"]),
                                             int(m["v"])) is None:
                        orphans.append(name)
        self.assertEqual(orphans, [],
                         f"{len(orphans)} verse SVG(s) with no registry owner")

    def test_no_translation_suffixed_visuals(self):
        suffixed = [name for _, _, files in os.walk(VISUALS)
                    for name in files if SUFFIXED.search(name)]
        self.assertEqual(suffixed, [],
                         f"{len(suffixed)} translation-suffixed file(s), "
                         f"e.g. {suffixed[:3]}")


if __name__ == "__main__":
    unittest.main()
