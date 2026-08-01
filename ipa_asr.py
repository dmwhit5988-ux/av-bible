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
    "ɹ": "r", "ɻ": "r", "ɾ": "r", "ʀ": "r", "ʁ": "r",
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
    """``text`` -> comparable coarse phone list."""
    return fold(phones(text))


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


# Below this many expected phones, hunting for a name inside a longer utterance
# stops being meaningful. Measured against decoy recordings that did *not*
# contain the name: at 4 phones or fewer the chance score equalled the real one
# every time (Ur /ɜːr/ scored 1.00 against audio of "Nebuchadnezzar"), while at
# 5+ phones every name tested beat its chance score by 0.17-0.80.
MIN_PHONES_FOR_LOCAL = 5


def can_locate(expected: str) -> bool:
    """True if ``expected`` is long enough to be found inside a carrier phrase."""
    return len(normalize(expected)) >= MIN_PHONES_FOR_LOCAL


def _fold_indexed(tokens):
    """Fold ``tokens``, remembering which original token each phone came from."""
    folded, origin = [], []
    for k, t in enumerate(tokens):
        for p in fold([t]):
            folded.append(p)
            origin.append(k)
    return folded, origin


def locate(expected: str, heard: str):
    """Find ``expected`` inside ``heard``. Returns ``(score, matched-span)``.

    Approximate substring alignment: gaps *before and after* the match are free,
    so when the name was spoken inside a carrier phrase the surrounding words
    cost nothing. The returned span is the slice of the original (unfolded)
    transcription that matched, which is what should be shown to a human -- the
    name as heard, without "he said … again" wrapped around it.

    Only meaningful when ``can_locate(expected)`` is true; on short names a
    chance match somewhere in the carrier is as likely as a real one.
    """
    a = normalize(expected)
    htoks = phones(heard)
    b, origin = _fold_indexed(htoks)
    if not a or not b:
        return 0.0, ""

    m, n = len(a), len(b)
    prev = [0] * (n + 1)            # row 0: a match may start anywhere, free
    pstart = list(range(n + 1))     # …and this is where it started
    for i in range(1, m + 1):
        cur, cstart = [i], [0]
        for j in range(1, n + 1):
            sub = prev[j - 1] + (a[i - 1] != b[j - 1])
            dele = prev[j] + 1      # expected phone absent from the audio
            ins = cur[j - 1] + 1    # extra phone in the audio
            best = min(sub, dele, ins)
            cur.append(best)
            cstart.append(pstart[j - 1] if best == sub else
                          pstart[j] if best == dele else cstart[j - 1])
        prev, pstart = cur, cstart

    end = min(range(1, n + 1), key=lambda j: prev[j])
    score = max(0.0, 1.0 - prev[end] / len(a))
    lo, hi = pstart[end], end
    span = "".join(htoks[origin[lo]:origin[hi - 1] + 1]) if lo < hi else ""
    return score, span


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
