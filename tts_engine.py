"""Text-to-speech synthesis.

Primary engine: Microsoft Edge neural voices via the free `edge-tts` service
(no API key, requires internet). One mp3 is generated per verse so playback
always knows exactly which verse is audible — the hook the visual layer uses.

Azure engine (azure_tts.py): the same voices through the Azure Speech service,
which accepts SSML, so names whose `use_ipa` is on are spoken from their IPA.
Azure is metered (the free tier is 500,000 characters a month), so it is only
used when a caller asks for it, by engine:
    ENGINE_EDGE   Edge for everything (respellings only) -- the default
    ENGINE_MIXED  Azure only for text naming someone spoken from IPA, Edge
                  for the rest -- the audio is the same, so only the verses
                  that need it spend characters
    ENGINE_AZURE  Azure for everything (e.g. while edge-tts is down)

Fallback engine: Windows built-in SAPI voices via PowerShell (offline, lower
quality) used automatically if edge-tts fails. Azure never falls back: a verse
that needed IPA mustn't quietly ship without it.

Generated audio is cached on disk keyed by voice, rate, and text hash, so a
chapter is only synthesized once. Plain text has one cache entry whichever
service spoke it; SSML with <phoneme> tags has its own.
"""

import asyncio
import hashlib
import os
import subprocess
import tempfile
import time
from typing import NamedTuple

import azure_tts
import pronunciation
from config import AUDIO_CACHE_DIR

# Curated Edge neural voices that read scripture well.
EDGE_VOICES = [
    "en-US-AndrewNeural",
    "en-US-BrianNeural",
    "en-US-ChristopherNeural",
    "en-US-GuyNeural",
    "en-US-AriaNeural",
    "en-US-JennyNeural",
    "en-US-MichelleNeural",
    "en-GB-RyanNeural",
    "en-GB-SoniaNeural",
    "en-AU-WilliamNeural",
]

# The house narration. Every tool renders with this voice and rate; only the
# Audio Renderer's advanced picker overrides the voice, for one render. The
# rate is a percent offset (edge-tts "+N%").
HOUSE_VOICE = "en-US-AndrewNeural"
HOUSE_RATE = 0

ENGINE_EDGE = "edge"
ENGINE_MIXED = "mixed"
ENGINE_AZURE = "azure"
ENGINES = (ENGINE_EDGE, ENGINE_MIXED, ENGINE_AZURE)
ENGINE_LABELS = {
    ENGINE_EDGE: "Edge (free): respellings only, no IPA",
    ENGINE_MIXED: "Azure for verses with IPA names, Edge for the rest",
    ENGINE_AZURE: "Azure for every verse",
}

# pronunciation.azure_ipa writes Azure's en-US phones, so only en-US voices
# speak names from IPA; any other voice override respells them as Edge does.
IPA_LOCALE = "en-US-"

SAPI_FALLBACK_NAME = "Windows built-in voice (offline fallback)"


class TTSError(Exception):
    pass


def _cache_file(voice: str, rate: int, text: str, ext: str, ssml: bool = False) -> str:
    key = f"{voice}|{rate}|ssml|{text}" if ssml else f"{voice}|{rate}|{text}"
    digest = hashlib.md5(key.encode("utf-8")).hexdigest()[:16]
    safe_voice = voice.replace("-", "")
    folder = os.path.join(AUDIO_CACHE_DIR, "tts")
    os.makedirs(folder, exist_ok=True)
    kind = "_ssml" if ssml else ""
    return os.path.join(folder, f"{safe_voice}_{rate:+d}{kind}_{digest}.{ext}")


def _cached(path: str) -> bool:
    return os.path.exists(path) and os.path.getsize(path) > 500


class Route(NamedTuple):
    """How ``synthesize`` would speak a text: by which service, sending what,
    cached where, and what Azure would bill if it isn't cached yet."""
    engine: str      # ENGINE_EDGE or ENGINE_AZURE: the service that speaks it
    payload: str     # the text for Edge, or the <voice> body for Azure
    path: str        # its mp3 in the cache
    chars: int       # Azure's billable characters; 0 for Edge

    @property
    def cached(self) -> bool:
        return _cached(self.path)


def route(text: str, voice: str, rate: int, engine: str = ENGINE_EDGE,
          apply_respell: bool = True) -> Route:
    """Decide how ``text`` is spoken under ``engine`` without speaking it --
    for estimating a render's Azure characters before it starts."""
    if (apply_respell and engine != ENGINE_EDGE and voice.startswith(IPA_LOCALE)
            and pronunciation.uses_ipa(text)):
        body = azure_tts.wrap_rate(pronunciation.ssml(text), rate)
        return Route(ENGINE_AZURE, body, _cache_file(voice, rate, body, "mp3", ssml=True),
                     azure_tts.billable(body))
    spoken = pronunciation.respell(text) if apply_respell else text
    path = _cache_file(voice, rate, spoken, "mp3")
    if engine == ENGINE_AZURE:
        body = azure_tts.wrap_rate(pronunciation.xml_escape(spoken), rate)
        return Route(ENGINE_AZURE, body, path, azure_tts.billable(body))
    return Route(ENGINE_EDGE, spoken, path, 0)


def _synthesize_edge(text: str, voice: str, rate: int, out_path: str) -> None:
    import edge_tts

    async def run():
        communicate = edge_tts.Communicate(text=text, voice=voice, rate=f"{rate:+d}%")
        await communicate.save(out_path)

    asyncio.run(run())
    if not os.path.exists(out_path) or os.path.getsize(out_path) < 500:
        raise TTSError("edge-tts produced no audio")


def _synthesize_sapi(text: str, rate: int, out_path: str) -> None:
    """Offline fallback: Windows SAPI via PowerShell, writes a wav file."""
    # SAPI rate is -10..10; map our -50..50 percent onto that range.
    sapi_rate = max(-10, min(10, round(rate / 5)))
    with tempfile.NamedTemporaryFile(
        "w", suffix=".txt", delete=False, encoding="utf-8-sig"
    ) as tf:
        tf.write(text)
        txt_path = tf.name
    script = (
        "Add-Type -AssemblyName System.Speech; "
        f"$t = [IO.File]::ReadAllText('{txt_path}'); "
        "$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
        f"$s.Rate = {sapi_rate}; "
        f"$s.SetOutputToWaveFile('{out_path}'); "
        "$s.Speak($t); $s.Dispose()"
    )
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", script],
            capture_output=True,
            timeout=120,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
    finally:
        try:
            os.remove(txt_path)
        except OSError:
            pass
    if result.returncode != 0 or not os.path.exists(out_path):
        raise TTSError("Windows SAPI synthesis failed: "
                       + result.stderr.decode(errors="replace")[:200])


def _drop(path: str) -> None:
    try:
        if os.path.exists(path):
            os.remove(path)
    except OSError:
        pass


# After an edge-tts failure (usually: offline), skip further edge attempts
# for this long so playback doesn't stall on a network timeout every verse.
_EDGE_RETRY_SECONDS = 120
_edge_down_until = 0.0


def synthesize(text: str, voice: str, rate: int, apply_respell: bool = True,
               engine: str = ENGINE_EDGE, label: str = "") -> str:
    """Return path to an audio file speaking `text`. Cached across runs.

    Cached neural mp3s are served forever. Cached SAPI wavs (made while
    offline) are only *fallbacks*: once edge-tts works again the verse is
    re-synthesized with the neural voice and the wav is deleted, so the
    lower-quality audio never becomes permanent.

    Proper nouns the voice mispronounces are phonetically respelled first (see
    pronunciation.py); this only changes what is *spoken*, and because the cache
    is keyed on the spoken text, updating the pronunciation list yields fresh
    audio automatically. `apply_respell=False` speaks `text` verbatim -- used by
    the pronunciation editor to preview an exact string.

    `engine` picks the service (see the module docstring). Whatever Azure
    speaks is Azure's or nothing: its failures raise azure_tts.AzureError.
    `label` names the request in the Azure usage log.
    """
    global _edge_down_until
    r = route(text, voice, rate, engine, apply_respell)
    if r.cached:
        return r.path
    if r.engine == ENGINE_AZURE:
        azure_tts.synthesize(r.payload, voice, r.path, label)
        _drop(r.path[:-4] + ".wav")   # an offline fallback for the same text
        return r.path
    text, mp3_path = r.payload, r.path
    wav_path = _cache_file(voice, rate, text, "wav")
    wav_cached = _cached(wav_path)

    if time.time() >= _edge_down_until:
        try:
            _synthesize_edge(text, voice, rate, mp3_path)
            if wav_cached:  # upgrade: replace the offline-fallback audio
                _drop(wav_path)
            return mp3_path
        except Exception:
            # Clean up any partial mp3, then back off from edge for a while.
            _drop(mp3_path)
            _edge_down_until = time.time() + _EDGE_RETRY_SECONDS

    if wav_cached:
        return wav_path
    _synthesize_sapi(text, rate, wav_path)
    return wav_path


def synthesize_ipa(word: str, ipa: str, voice: str, rate: int) -> str:
    """Azure speaking ``word`` from ``ipa`` alone -- the Pronunciation tool's
    preview. Cached like any SSML. Raises ValueError if the IPA can't be sent,
    azure_tts.AzureError if Azure fails."""
    body = azure_tts.wrap_rate(pronunciation.phoneme(word, ipa), rate)
    path = _cache_file(voice, rate, body, "mp3", ssml=True)
    if not _cached(path):
        azure_tts.synthesize(body, voice, path, f"preview {word}")
    return path
