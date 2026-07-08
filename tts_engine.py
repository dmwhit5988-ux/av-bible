"""Text-to-speech synthesis.

Primary engine: Microsoft Edge neural voices via the free `edge-tts` service
(no API key, requires internet). One mp3 is generated per verse so playback
always knows exactly which verse is audible — the hook the visual layer uses.

Fallback engine: Windows built-in SAPI voices via PowerShell (offline, lower
quality) used automatically if edge-tts fails.

Generated audio is cached on disk keyed by voice, rate, and text hash, so a
chapter is only synthesized once.
"""

import asyncio
import hashlib
import os
import subprocess
import tempfile
import time

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

SAPI_FALLBACK_NAME = "Windows built-in voice (offline fallback)"


class TTSError(Exception):
    pass


def _cache_file(voice: str, rate: int, text: str, ext: str) -> str:
    digest = hashlib.md5(f"{voice}|{rate}|{text}".encode("utf-8")).hexdigest()[:16]
    safe_voice = voice.replace("-", "")
    folder = os.path.join(AUDIO_CACHE_DIR, "tts")
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, f"{safe_voice}_{rate:+d}_{digest}.{ext}")


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


# After an edge-tts failure (usually: offline), skip further edge attempts
# for this long so playback doesn't stall on a network timeout every verse.
_EDGE_RETRY_SECONDS = 120
_edge_down_until = 0.0


def synthesize(text: str, voice: str, rate: int) -> str:
    """Return path to an audio file speaking `text`. Cached across runs.

    Cached neural mp3s are served forever. Cached SAPI wavs (made while
    offline) are only *fallbacks*: once edge-tts works again the verse is
    re-synthesized with the neural voice and the wav is deleted, so the
    lower-quality audio never becomes permanent.

    Proper nouns the voice mispronounces are phonetically respelled first (see
    pronunciation.py); this only changes what is *spoken*, and because the cache
    is keyed on the spoken text, updating the pronunciation list yields fresh
    audio automatically.
    """
    global _edge_down_until
    text = pronunciation.respell(text)
    mp3_path = _cache_file(voice, rate, text, "mp3")
    if os.path.exists(mp3_path) and os.path.getsize(mp3_path) > 500:
        return mp3_path
    wav_path = _cache_file(voice, rate, text, "wav")
    wav_cached = os.path.exists(wav_path) and os.path.getsize(wav_path) > 500

    if time.time() >= _edge_down_until:
        try:
            _synthesize_edge(text, voice, rate, mp3_path)
            if wav_cached:  # upgrade: replace the offline-fallback audio
                try:
                    os.remove(wav_path)
                except OSError:
                    pass
            return mp3_path
        except Exception:
            # Clean up any partial mp3, then back off from edge for a while.
            try:
                if os.path.exists(mp3_path):
                    os.remove(mp3_path)
            except OSError:
                pass
            _edge_down_until = time.time() + _EDGE_RETRY_SECONDS

    if wav_cached:
        return wav_path
    _synthesize_sapi(text, rate, wav_path)
    return wav_path
