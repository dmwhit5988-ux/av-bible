"""Acoustic IPA transcription -- listen to an audio file, write down the phones.

This is the "ear" behind the Pronunciation Verifier (``pronunciation_check.py``).
It runs a wav2vec2 CTC model whose output vocabulary *is* the eSpeak IPA phoneme
set, so it reports the sounds actually present in the audio rather than guessing
at words. That distinction is the whole point: a word recognizer would hear
"Mahalalel" and helpfully report the spelling back, telling us nothing about how
the voice said it. This hears ``m ɐ h ˈa l ɐ l ɛ l`` and lets us judge.

    ipa = transcribe("cache/audio/tts/enUSAndrewNeural_+0_ab12.mp3")

Honest limits -- read these before trusting a number:

  * It is a *broad* transcription, not a narrow one. Expect roughly 10-25% phone
    error even on clean synthetic speech; vowel quality is the weak spot.
  * Its notation is eSpeak's, which is not the dictionary notation stored in
    ``pronunciations.json`` (``ɹ`` vs ``r``, ``ɐ`` vs ``ʌ``, r-coloured ``ɚ``…).
    ``fold()`` collapses both sides onto a coarser shared alphabet before any
    comparison, so scores measure real disagreement rather than notation drift.
  * Therefore ``similarity()`` is a triage signal -- good for "this name came out
    badly wrong", not for adjudicating a subtle stress or vowel argument.

Everything heavy (torch, transformers, the ~1.2 GB model) is imported lazily so
the rest of the studio still starts on a machine that hasn't installed them.
"""

import os
import re
import threading
import unicodedata

MODEL_ID = "facebook/wav2vec2-lv-60-espeak-cv-ft"
TARGET_SR = 16000

_model = None
_features = None       # Wav2Vec2FeatureExtractor: waveform -> normalized input
_tokenizer = None      # Wav2Vec2PhonemeCTCTokenizer: CTC ids -> IPA phones
_load_lock = threading.Lock()


# --------------------------------------------------------------------------
# Availability / model loading
# --------------------------------------------------------------------------

def available() -> tuple:
    """Return ``(ok, message)`` describing whether the deps are importable."""
    missing = []
    for mod, pkg in (("torch", "torch"), ("transformers", "transformers"),
                     ("soundfile", "soundfile"), ("scipy", "scipy")):
        try:
            __import__(mod)
        except ImportError:
            missing.append(pkg)
    if missing:
        return False, ("Missing: " + ", ".join(missing) +
                       "\n\npip install " + " ".join(missing))
    return True, "Ready."


def is_loaded() -> bool:
    return _model is not None


def load_model(status=None):
    """Load (and on first run download) the phoneme model. Thread-safe, cached.

    ``status`` is an optional ``callable(str)`` for progress messages.
    """
    global _model, _features, _tokenizer
    if _model is not None:
        return _model, _features, _tokenizer
    with _load_lock:
        if _model is not None:
            return _model, _features, _tokenizer
        if status:
            status(f"Loading {MODEL_ID} (first run downloads ~1.2 GB)…")
        import torch
        from transformers import (AutoModelForCTC, AutoTokenizer,
                                  Wav2Vec2FeatureExtractor)

        # The feature extractor and tokenizer are loaded separately rather than
        # through AutoProcessor for one specific reason: this tokenizer builds a
        # `phonemizer` backend in its constructor, which also wants a native
        # espeak-ng binary. That machinery is only used to turn *text* into
        # phonemes for training. We go the other way -- CTC ids to phones, which
        # needs nothing but the vocab file -- so do_phonemize=False skips it and
        # drops two awkward dependencies (one of them non-Python).
        tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, do_phonemize=False)
        features = Wav2Vec2FeatureExtractor.from_pretrained(MODEL_ID)
        model = AutoModelForCTC.from_pretrained(MODEL_ID)
        model.eval()
        # Inference only, and on CPU under x64 emulation -- grads would just be
        # wasted memory and time.
        torch.set_grad_enabled(False)
        _features, _tokenizer, _model = features, tokenizer, model
        if status:
            status("Model loaded.")
    return _model, _features, _tokenizer


# --------------------------------------------------------------------------
# Audio loading
# --------------------------------------------------------------------------

def read_audio(path: str):
    """Read any soundfile-supported file (mp3/wav/flac/ogg) as 16 kHz mono float32."""
    import numpy as np
    import soundfile as sf

    data, sr = sf.read(path, dtype="float32", always_2d=True)
    audio = data.mean(axis=1)  # downmix to mono
    if sr != TARGET_SR:
        from math import gcd
        from scipy.signal import resample_poly
        g = gcd(int(sr), TARGET_SR)
        # resample_poly low-passes as it decimates, so this doesn't alias the
        # way bare interpolation would going 24 kHz -> 16 kHz.
        audio = resample_poly(audio, TARGET_SR // g, int(sr) // g).astype("float32")
    return np.ascontiguousarray(audio)


# --------------------------------------------------------------------------
# Transcription
# --------------------------------------------------------------------------

def transcribe(path: str, status=None) -> str:
    """Return a space-separated IPA phone string for the audio at ``path``."""
    import torch

    model, features, tokenizer = load_model(status)
    audio = read_audio(path)
    if audio.size < TARGET_SR // 50:  # < 20 ms of audio; nothing to hear
        return ""
    inputs = features(audio, sampling_rate=TARGET_SR, return_tensors="pt")
    with torch.no_grad():
        logits = model(inputs.input_values).logits
    ids = torch.argmax(logits, dim=-1)
    # This model's vocabulary is the eSpeak phoneme set, so decoding already
    # yields space-separated IPA phones -- no tokenization needed here.
    return (tokenizer.batch_decode(ids)[0] or "").strip()


# --------------------------------------------------------------------------
# IPA normalization and comparison
# --------------------------------------------------------------------------

# Suprasegmentals and diacritics that carry no weight in a broad comparison.
_STRIP_CHARS = set("ˈˌːˑ.·|‖ ʰʷʲˠˤ̩̯͜͡ⁿ")

# Two-character units that must survive as one phone.
_DIGRAPHS = (
    "tʃ", "dʒ", "ts", "dz", "aɪ", "aʊ", "ɔɪ", "eɪ", "oʊ", "əʊ",
    "ɛə", "ɪə", "ʊə", "ɑɪ", "ɑʊ",
)

# Collapse eSpeak's notation and the dictionary's onto one coarse alphabet.
# Anything mapped to "" disappears entirely (e.g. eSpeak's inserted glottal stops).
_FOLD = {
    "ɡ": "g", "ɫ": "l", "ɭ": "l",
    "ɹ": "r", "ɻ": "r", "ʀ": "r", "ʁ": "r",
    # ɾ is the American flap, an allophone of /t/ and /d/ between vowels -- not
    # a rhotic. Folding it to "r" (as this table first did) penalised correct
    # speech: "Eden" comes back as [iː ɾ ɪ ŋ] and scored 0.25 against /ˈiː.dən/.
    "ɾ": "d",
    "ʍ": "w", "ʔ": "", "ʼ": "",
    # central / reduced vowels -- unstressed reduction is the noisiest signal
    # in the model's output, so they all become schwa.
    "ɐ": "ə", "ʌ": "ə", "ɜ": "ə", "ɘ": "ə", "ɵ": "ə",
    "ɚ": "ər", "ɝ": "ər",
    # eSpeak writes the TRAP vowel bare and the reduced high vowel as ᵻ; the
    # hand-written references use æ and ɪ for the same sounds.
    "a": "æ", "ɨ": "ɪ", "ᵻ": "ɪ",
    # cot/caught and father/bother are merged for most speakers; keeping them
    # apart only manufactures disagreement.
    "ɑ": "ɔ", "ɒ": "ɔ", "ɔː": "ɔ",
    "ʊ": "u",
    "o": "oʊ", "ɔʊ": "oʊ", "əʊ": "oʊ",
    "e": "eɪ",
    "ɑɪ": "aɪ", "ɑʊ": "aʊ",
    "ɛə": "ɛr", "ɪə": "ɪr", "ʊə": "ur",
    # The model's vocabulary carries r-coloured vowels as SINGLE tokens
    # (ɑːɹ, ɔːɹ, ɛɹ, ɪɹ, ʊɹ, aɪɚ), while the written references spell them as a
    # vowel followed by r. Without these they could never match: "Dara" came
    # back as [d ɑːɹ ɹ ɐ] and could not line up with /ˈdɛər.ə/. The ː is already
    # stripped by _clean, hence the keys here have none.
    "ɑɹ": "ɔr", "ɔɹ": "ɔr", "ɛɹ": "ɛr", "ɪɹ": "ɪr", "ʊɹ": "ur", "aɪɚ": "aɪər",
    "əl": "əl", "n̩": "n", "l̩": "l",
    "x": "k", "ç": "h",
}


def _clean(text: str) -> str:
    """Strip slashes, stress, length and syllable marks; decompose diacritics."""
    if not text:
        return ""
    text = text.strip().strip("/[]")
    text = unicodedata.normalize("NFD", text)
    out = []
    for ch in text:
        if ch in _STRIP_CHARS:
            continue
        if unicodedata.combining(ch):  # combining tilde, ring, etc.
            continue
        out.append(ch)
    return unicodedata.normalize("NFC", "".join(out))


def phones(text: str) -> list:
    """Split an IPA string into phone tokens.

    Model output arrives already space-separated, so that is honoured when
    present; the hand-written ``ipa`` values in pronunciations.json are one run
    of characters, so those are segmented with the digraph table.
    """
    if not text:
        return []
    if " " in text.strip():
        # Already segmented (model output) -- just clean each token.
        return [t for t in (_clean(t) for t in text.split()) if t]
    s = _clean(text)
    toks, i = [], 0
    while i < len(s):
        if i + 1 < len(s) and s[i:i + 2] in _DIGRAPHS:
            toks.append(s[i:i + 2])
            i += 2
        else:
            toks.append(s[i])
            i += 1
    return toks


def fold(tokens) -> list:
    """Map phone tokens onto the coarse shared alphabet (see ``_FOLD``)."""
    out = []
    for t in tokens:
        rep = _FOLD.get(t, t)
        if not rep:
            continue
        # A fold may expand to two phones (ɚ -> ə r); re-split those.
        if len(rep) > 1 and rep not in _DIGRAPHS:
            i = 0
            while i < len(rep):
                if i + 1 < len(rep) and rep[i:i + 2] in _DIGRAPHS:
                    out.append(rep[i:i + 2])
                    i += 2
                else:
                    out.append(rep[i])
                    i += 1
        else:
            out.append(rep)
    return out


def normalize(text: str) -> list:
    """``text`` -> comparable coarse phone list.

    Runs of the same phone collapse to one. English does not contrast length
    here, and doubling arises spuriously on both sides: a reference like
    /ˈdɛər.ə/ folds to d-ɛ-r-r-ə because "ɛə" already implies the rhotic that
    the written r repeats, and the model separately likes to emit [ɔːɹ ɹ].
    Without this, a correct match is penalised for an artefact of notation.
    """
    out = []
    for p in fold(phones(text)):
        if not out or out[-1] != p:
            out.append(p)
    return out


def _levenshtein(a, b) -> int:
    if not a:
        return len(b)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def similarity(expected: str, heard: str) -> float:
    """Return 0.0-1.0 agreement between two IPA strings after folding.

    1.0 means the coarse phone sequences are identical. Because both sides are
    folded first, this ignores notation differences and unstressed-vowel
    reduction, and reflects genuine disagreement about the sounds.
    """
    a, b = normalize(expected), normalize(heard)
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return 1.0 - _levenshtein(a, b) / max(len(a), len(b))


# A word spoken alone gets clipped by the voice ("Mahalalel" came back as
# "mahalla"), so names are recorded inside a fixed carrier and cut back out
# afterwards. The commas matter: without them a name's edge consonant merges
# into the neighbouring word ("He said Dara twice" lost Dara's /d/ into "said",
# leaving just "ɜː"). With them the anchors below transcribe identically every
# time, which is what makes the cut reliable.
# The tail word must not begin with a sound names commonly end in, or it eats
# one: with "twice", "Phut" transcribed as [f ʌ t w aɪ s] -- a single /t/ doing
# double duty -- and the strip returned "fʌ". "once" starts with /w/, which is
# effectively absent word-finally in these names, so nothing merges. It also
# stops the voice flapping a name's final /d/: "Eden" went from [iː ɾ ɪ ŋ]
# before "twice" to a clean [iː d ə n] before "once".
# Two carriers, because one measurement is not enough. The same name scores
# differently depending on what follows it -- "Salma" kept its /l/ before
# "yesterday" but dropped it before "once" -- so a single reading is a noisy
# basis for changing a pronunciation. Measuring in both and averaging cancels
# most of that context dependence.
CARRIERS = (
    ("He said, {}, once.",
     ("h", "i", "s", "ɛ", "d"), ("w", "ə", "n", "s")),
    ("He said, {}, yesterday.",
     ("h", "i", "s", "ɛ", "d"), ("j", "ɛ", "s", "t", "ə", "r", "d", "eɪ")),
)
CARRIER = CARRIERS[0][0]               # the primary, for single-shot callers
_HEAD = CARRIERS[0][1]
_TAIL = CARRIERS[0][2]


def _prefix_end(pattern, seq) -> int:
    """Index in ``seq`` where ``pattern`` best finishes, aligned from the start.

    Ties resolve to the earliest index, which is what we want: the real carrier
    word is the first thing in the utterance, so a chance match later in a name
    never wins.
    """
    n = len(seq)
    prev = list(range(n + 1))          # cost of skipping j tokens of seq
    for i in range(1, len(pattern) + 1):
        cur = [i]
        for j in range(1, n + 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1,
                           prev[j - 1] + (pattern[i - 1] != seq[j - 1])))
        prev = cur
    return min(range(n + 1), key=lambda j: prev[j])


def strip_carrier(heard: str, head=None, tail=None) -> str:
    """Cut the carrier words off a transcription, leaving just the name.

    Anchoring on known words beats searching for the name: an earlier version
    hunted for the expected phones anywhere in the utterance and would happily
    match them against "he sa[id]" instead of the name, silently scoring the
    wrong span. Here the boundaries come from text we control, so the result
    does not depend on the name being recognised correctly in the first place.

    Pass the ``head``/``tail`` of whichever entry in ``CARRIERS`` produced
    ``heard``; the defaults are the primary carrier's. Stripping with the wrong
    anchors leaves a carrier phone glued to the name rather than failing loudly.
    """
    head = head or _HEAD
    tail = tail or _TAIL
    toks = phones(heard)
    folded, origin = _fold_indexed(toks)
    if not folded:
        return ""
    start = _prefix_end(head, folded)
    # Search the tail from the end so a tie resolves to the real final word.
    end = len(folded) - _prefix_end(tuple(reversed(tail)), folded[::-1])
    if not 0 <= start < end <= len(folded):
        return "".join(toks)           # anchors implausible -- don't guess
    return "".join(toks[origin[start]:origin[end - 1] + 1])


def _fold_indexed(tokens):
    """Fold ``tokens``, remembering which original token each phone came from."""
    folded, origin = [], []
    for k, t in enumerate(tokens):
        for p in fold([t]):
            folded.append(p)
            origin.append(k)
    return folded, origin


def pretty(text: str) -> str:
    """Render a model phone string as conventional IPA for display.

    Only the inter-phone spaces are removed. Stress and length marks are *kept*
    -- they are noise for scoring (``phones`` drops them) but are exactly what
    makes the result useful as a written reference pronunciation.
    """
    return "".join((text or "").split())


# --------------------------------------------------------------------------
# CLI: transcribe files straight from the command line
# --------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    ok, msg = available()
    if not ok:
        print(msg)
        raise SystemExit(1)
    args = sys.argv[1:]
    if not args:
        print(__doc__.strip().splitlines()[0])
        print("\nusage: python ipa_asr.py <audio-file> [more…]")
        raise SystemExit(2)
    for path in args:
        if not os.path.exists(path):
            print(f"{path}: not found")
            continue
        print(f"{os.path.basename(path)}: {transcribe(path, status=lambda m: print('  ' + m))}")
