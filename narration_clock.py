"""When a verse's MP3 says each part of its text: a clock read from the
pauses in the audio, matched to the text's punctuation.

The MP3s carry no word timings (Azure returns audio only, and the Edge
renderer keeps none), but the house voice pauses at commas, semicolons,
colons, full stops and parentheses. So the clock finds the pauses
(stretches QUIET_DB below the speech's loud end, at least MIN_PAUSE long)
and matches them, in order, to the punctuation; a pause with no
punctuation (a breath) or punctuation with no pause is passed over. Each
matched pause fixes the time of a point in the text, and a character
between two of them takes its time by its share of the clause's letters.
A town list, a name between every pair of commas, is where it is surest.

Checked on Joshua 13-19 (2026-10-29) against the Pronunciation Verifier's
phoneme model, 428 names in 148 verses: a name's time is 0.04 s off at the
median, 0.14 s at the 90th percentile and 0.30 s at most. The word's place
in the verse alone is 0.27 s off at the median and up to 1.55 s. Matching
clause by clause matters: matching each pause to when its mark is due over
the whole verse let a slowly said list drift a mark off, up to 1.5 s.

    clock = narration_clock.clock(text, mp3_path)   # None if there's no MP3
    clock(text.index("Hebron"))                      # seconds into the MP3

Decoding needs soundfile (with numpy), which reads MP3.
"""

import os
import re
from bisect import bisect_right

import numpy as np
import soundfile as sf

HOP = 0.01            # the loudness envelope's step, seconds
QUIET_DB = 35         # a pause is this far below the speech's 95th-percentile loudness
MIN_PAUSE = 0.12      # the shortest pause that counts, seconds
SKIP = 0.6            # the cost (seconds of misfit) of passing over a pause or a mark
# the marks the voice pauses at: , ; : . and a parenthesis ("the Jebusite
# (also called Jerusalem) southward")
BREAK = re.compile(r"[,;:.](?=\s|$)|\((?=\w)|(?<=\w)\)(?=\s)")
SILENT_DB = -60       # audio whose loud end is quieter than this holds no speech


def _envelope(path):
    """The audio's loudness in dB, one value a HOP, and its length."""
    data, sr = sf.read(path, dtype="float32", always_2d=True)
    a = data.mean(axis=1)
    hop = max(1, int(sr * HOP))
    n = len(a) // hop
    rms = np.sqrt((a[:n * hop].reshape(n, hop) ** 2).mean(axis=1) + 1e-12)
    return 20 * np.log10(rms), len(a) / sr


def pauses(path):
    """(speech start, speech end, [(pause start, pause end)]) in seconds:
    the pauses inside the speech, not the silence before or after it."""
    db, dur = _envelope(path)
    if not len(db) or np.percentile(db, 95) < SILENT_DB:
        return None
    quiet = db < np.percentile(db, 95) - QUIET_DB
    runs, i, n = [], 0, len(quiet)
    while i < n:
        if quiet[i]:
            j = i
            while j < n and quiet[j]:
                j += 1
            runs.append((i * HOP, j * HOP))
            i = j
        else:
            i += 1
    lead = runs[0][1] if runs and runs[0][0] == 0 else 0.0
    trail = runs[-1][0] if runs and runs[-1][1] >= n * HOP - 0.02 else dur
    if trail <= lead:
        return None
    return lead, trail, [(a, b) for a, b in runs
                         if a > lead and b < trail and b - a >= MIN_PAUSE]


def _letters(s):
    return len(s) - s.count(" ")


def _match(text, lead, trail, ps):
    """Pair pauses with punctuation marks, in order, so that each clause
    (from one paired pause to the next) lasts about as long as its letters
    take at the verse's mean rate, not counting the pauses passed over
    inside it. Scored clause by clause, so a list of short names, said
    slower than the verse's mean, can't drift the pairing a mark off.
    Passing over a pause (a breath) or a mark (no pause) costs SKIP."""
    marks = [m.start() for m in BREAK.finditer(text) if m.start() < len(text.rstrip()) - 1]
    P, B = len(ps), len(marks)
    before = [0]                                   # letters before each character
    for ch in text:
        before.append(before[-1] + (ch != " "))
    paused = [0.0]                                 # pause time before each pause
    for a, b in ps:
        paused.append(paused[-1] + b - a)
    rate = (trail - lead - paused[-1]) / max(1, before[-1])

    def first(j):                                  # a clause's first character, after mark j
        return 0 if j < 0 else marks[j] + 1

    def last(j):                                   # its end, at mark j
        return len(text) if j == B else marks[j]

    def ends(i):                                   # when pause i ends
        return lead if i < 0 else ps[i][1]

    def starts(i):
        return trail if i == P else ps[i][0]

    # best[(i, j)]: the least cost of pairing pause i with mark j, and the pair before
    best = {(-1, -1): (0.0, None)}
    for i2, j2 in [(i, j) for i in range(P) for j in range(B)] + [(P, B)]:
        cost, back = float("inf"), None
        for (i1, j1), (c1, _b) in best.items():
            if i1 >= i2 or j1 >= j2:
                continue
            spoken = starts(i2) - ends(i1) - (paused[i2] - paused[i1 + 1])
            c = (c1 + abs(spoken - rate * (before[last(j2)] - before[first(j1)]))
                 + SKIP * (i2 - i1 - 1 + j2 - j1 - 1))
            if c < cost:
                cost, back = c, (i1, j1)
        best[(i2, j2)] = (cost, back)
    pairs, node = [], best[(P, B)][1]
    while node != (-1, -1):
        pairs.append((ps[node[0]], marks[node[1]]))
        node = best[node][1]
    return pairs[::-1], B


class Clock:
    """Seconds into the MP3 at a character of the text. `matched` of the
    text's `marks` (its inner punctuation) were found as pauses."""

    def __init__(self, text, lead, trail, ps):
        pairs, self.marks = _match(text, lead, trail, ps)
        self.matched = len(pairs)
        # each clause: (first char, last char, start, end): a pause ends one
        # clause at its mark and starts the next just after it
        starts = [(0, lead)] + [(k + 1, b) for (_a, b), k in pairs]
        ends = [(k, a) for (a, _b), k in pairs] + [(len(text), trail)]
        self.text = text
        self.clauses = [(c0, c1, t0, t1) for (c0, t0), (c1, t1) in zip(starts, ends)]
        self._firsts = [c[0] for c in self.clauses]

    def __call__(self, pos):
        c0, c1, t0, t1 = self.clauses[max(0, bisect_right(self._firsts, pos) - 1)]
        pos = min(max(pos, c0), c1)
        span = max(1, _letters(self.text[c0:c1]))
        return t0 + (t1 - t0) * _letters(self.text[c0:pos]) / span


def clock(text, path):
    """The verse's clock, or None when it has no MP3 (or it holds no speech)."""
    if not os.path.exists(path):
        return None
    found = pauses(path)
    return Clock(text, *found) if found else None
