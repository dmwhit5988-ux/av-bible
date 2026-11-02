"""Genesis 1 and Numbers 1-2 import the garden's palette from generate_genesis2_svg, and svg_figures
is theirs as well as the garden's. Do they still regenerate byte-identical to what is published?

Slow, and by hand: after any change to svg_figures or to that palette, and not in the list before
committing. Nothing is written but a temp folder: out_path is patched in each importing module.

    .venv\\Scripts\\python.exe -m unittest test_garden_bytes -v

Genesis 1:14-1:19 are known drift, older than the garden: the published sun carries a
stroke-opacity the generator no longer writes. They stay listed until someone regenerates them.
"""

import os
import tempfile
import unittest
from unittest import mock

import config
import generate_genesis1_svg
import generate_numbers1_2_svg
import generate_tabernacle

KNOWN_DRIFT = {f"Genesis_1_{v}.svg" for v in range(14, 20)}


def regenerate(module, into):
    """Runs a generator's main with out_path in `into`. -> {name: (its bytes, the published's)}."""
    made = {}

    def out_path(book, chapter, name):
        made[name] = os.path.join(str(config.VISUALS_DIR), book, str(chapter), name)
        return os.path.join(into, name)

    def not_there(*_args):
        raise AssertionError("a module with its own out_path is writing")
    with (mock.patch.object(module, "out_path", out_path),
          mock.patch.object(generate_tabernacle, "out_path", not_there),
          mock.patch("builtins.print")):
        module.main()
    out = {}
    for name, published in made.items():
        with open(os.path.join(into, name), "rb") as a, open(published, "rb") as b:
            out[name] = (a.read(), b.read())
    return out


class Neighbours(unittest.TestCase):
    def differing(self, module):
        with tempfile.TemporaryDirectory() as into:
            files = regenerate(module, into)
        self.assertTrue(files)
        return {name for name, (ours, published) in files.items() if ours != published}

    def test_numbers_1_2(self):
        self.assertEqual(self.differing(generate_numbers1_2_svg), set())

    def test_genesis_1(self):
        self.assertLessEqual(self.differing(generate_genesis1_svg), KNOWN_DRIFT)


if __name__ == "__main__":
    unittest.main()
