"""Import every root module, so a missing or untracked dependency fails here
instead of in the app (run.bat launches pythonw, which dies silently).

    .venv\\Scripts\\python.exe -m unittest test_imports -v
"""

import glob
import importlib
import os
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))

SKIP_PREFIXES = ("test_",)


def root_modules():
    names = []
    for path in sorted(glob.glob(os.path.join(HERE, "*.py"))):
        name = os.path.splitext(os.path.basename(path))[0]
        if not name.startswith(SKIP_PREFIXES):
            names.append(name)
    return names


class ImportEveryModule(unittest.TestCase):
    def test_root_modules_import(self):
        names = root_modules()
        self.assertGreater(len(names), 40, "found suspiciously few modules")
        for name in names:
            with self.subTest(module=name):
                importlib.import_module(name)


if __name__ == "__main__":
    unittest.main()
