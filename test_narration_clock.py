"""The narration clock (narration_clock.py) on made-up audio: tones for
speech, silence for pauses, so the times it should give are known.

    .venv\\Scripts\\python.exe -m unittest test_narration_clock
"""

import os
import tempfile
import unittest

import numpy as np
import soundfile as sf

import narration_clock as NC

SR = 16000


def audio(*parts):
    """('s', seconds) of speech (a tone) and ('p', seconds) of silence."""
    out = []
    for kind, sec in parts:
        n = int(round(sec * SR))
        t = np.arange(n) / SR
        out.append(0.3 * np.sin(2 * np.pi * 220 * t) if kind == "s" else np.zeros(n))
    return np.concatenate(out).astype("float32")


class Clock(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.dir.cleanup()

    def clock(self, text, *parts):
        path = os.path.join(self.dir.name, "verse.wav")
        sf.write(path, audio(*parts), SR)
        return NC.clock(text, path)

    def test_each_clause_starts_after_its_pause(self):
        text = "Alpha, Beta, Gamma."
        clk = self.clock(text, ("p", 0.2), ("s", 1.0), ("p", 0.3), ("s", 1.0), ("p", 0.3),
                         ("s", 1.0), ("p", 0.4))
        self.assertEqual((clk.matched, clk.marks), (2, 2))
        self.assertAlmostEqual(clk(text.index("Alpha")), 0.2, delta=0.02)
        self.assertAlmostEqual(clk(text.index("Beta")), 1.5, delta=0.02)
        self.assertAlmostEqual(clk(text.index("Gamma")), 2.8, delta=0.02)

    def test_a_breath_is_passed_over(self):
        """A pause with no punctuation doesn't take the comma's place."""
        text = "Alpha, Beta Gamma."
        clk = self.clock(text, ("s", 1.0), ("p", 0.3), ("s", 0.5), ("p", 0.15), ("s", 0.5))
        self.assertEqual((clk.matched, clk.marks), (1, 1))
        self.assertAlmostEqual(clk(text.index("Beta")), 1.3, delta=0.02)

    def test_a_list_said_slowly_keeps_its_pairing(self):
        """Joshua 15:32's pauses as measured in its MP3: short names said
        slower than the verse's mean rate don't pull the pairing a mark off."""
        text = "Lebaoth, Shilhim, Ain, and Rimmon. All the cities are twenty-nine, with their villages."
        clk = self.clock(text, ("p", 0.14), ("s", 0.59), ("p", 0.30), ("s", 0.55), ("p", 0.34),
                         ("s", 0.38), ("p", 0.16), ("s", 0.44), ("p", 0.40), ("s", 1.54),
                         ("p", 0.25), ("s", 0.86), ("p", 0.35))
        self.assertEqual((clk.matched, clk.marks), (5, 5))
        self.assertAlmostEqual(clk(text.index("Shilhim")), 1.03, delta=0.02)
        self.assertAlmostEqual(clk(text.index("Ain")), 1.92, delta=0.02)

    def test_the_voice_pauses_at_a_parenthesis(self):
        text = "Zelah, the Jebusite (also called Jerusalem), Gibeath."
        clk = self.clock(text, ("s", 0.6), ("p", 0.3), ("s", 0.8), ("p", 0.3), ("s", 1.0),
                         ("p", 0.3), ("s", 0.6))
        self.assertEqual((clk.matched, clk.marks), (3, 3))      # "Zelah," "(" "Jerusalem),"
        self.assertAlmostEqual(clk(text.index("also")), 2.0, delta=0.02)
        self.assertAlmostEqual(clk(text.index("Gibeath")), 3.3, delta=0.02)

    def test_silence_is_no_clock(self):
        path = os.path.join(self.dir.name, "silent.wav")
        sf.write(path, np.zeros(SR * 2, dtype="float32"), SR)
        self.assertIsNone(NC.clock("Alpha, Beta.", path))

    def test_times_run_forward(self):
        text = "One, two; three: four, five."
        clk = self.clock(text, ("s", 0.6), ("p", 0.2), ("s", 0.6), ("p", 0.25), ("s", 0.7),
                         ("p", 0.2), ("s", 0.5), ("p", 0.2), ("s", 0.6))
        ts = [clk(i) for i in range(len(text))]
        self.assertEqual(ts, sorted(ts))

    def test_no_mp3_no_clock(self):
        self.assertIsNone(NC.clock("Alpha.", os.path.join(self.dir.name, "none.mp3")))


if __name__ == "__main__":
    unittest.main()
