"""Azure AI Speech text-to-speech, for names spoken from IPA.

edge-tts is free but escapes its input, so it can't carry SSML. The same voice
on Azure (the house en-US-AndrewNeural) takes SSML, including
``<phoneme alphabet="ipa">`` -- the way to say a name from its IPA instead of
respelling it until it sounds right (pronunciation.ssml). The two services give
the same audio: one sentence rendered by both on 2026-10-18 matched in length
to the sample, in leading and trailing silence, and in loudness (correlation
0.998), so a chapter can mix verses from each. tts_engine decides which verse
goes where.

The key and region come from the environment, never from a file:
    setx AZURE_SPEECH_KEY <key>
    setx AZURE_SPEECH_REGION <region, e.g. eastus>

The free tier (F0) allows 500,000 characters a month and 20 requests a minute.
Azure bills every character inside ``<voice>``, markup included (only
``<speak>`` and ``<voice>`` are free), so a ``<phoneme>`` tag costs about 40
characters plus its IPA. Azure has no API a Speech key can read usage from, so
every request Azure answers is logged locally (config.AZURE_USAGE_PATH, one
JSON line each) and ``usage()`` sums the last 31 days. Whether the free month
is a calendar month or a rolling 30 days isn't documented; a 31-day sum is
never lower than either. The portal's Metrics, "Synthesized Characters", is the
authority.
"""

import http.client
import json
import os
import threading
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

import config

KEY_ENV = "AZURE_SPEECH_KEY"
REGION_ENV = "AZURE_SPEECH_REGION"

# What edge-tts receives, so Azure and Edge verses are interchangeable.
OUTPUT_FORMAT = "audio-24khz-48kbitrate-mono-mp3"
USER_AGENT = "TheoriaStudio"

FREE_CHARS = 500_000          # F0: characters per month
WINDOW_DAYS = 31      # covers a calendar month and a rolling 30 days
# F0 allows 20 requests per 60 seconds; one every 3.1 s stays under it.
MIN_INTERVAL = 3.1
# Backoff for 429 (throttled) and 5xx, in seconds; then the request fails.
RETRY_WAITS = (5, 15, 30, 60)
# A request that never reached Azure (or lost its answer) is tried once more,
# after this long. Worst case for an unreachable Azure: two timeouts and this.
NETWORK_RETRY_WAIT = 5
TIMEOUT = 30          # one verse takes Azure 1-3 s


class AzureError(Exception):
    """A request Azure refused or that never reached it.

    ``fatal`` means every later request will fail the same way -- a bad key,
    the quota used up, no network -- so a render should stop rather than
    skip on to the next verse. A 400 (usually an IPA symbol Azure doesn't
    know) is not fatal: it is that one request's fault.
    """

    def __init__(self, message: str, status: int = None, fatal: bool = False):
        super().__init__(message)
        self.status = status
        self.fatal = fatal


def settings() -> tuple:
    """(key, region) from the environment; either may be "". The region is
    the endpoint's form: the portal's "East US" is "eastus"."""
    return (os.environ.get(KEY_ENV, "").strip(),
            os.environ.get(REGION_ENV, "").strip().lower().replace(" ", ""))


def available() -> tuple:
    """(ok, message): whether Azure can be called, and if not, why."""
    key, region = settings()
    missing = [n for n, v in ((KEY_ENV, key), (REGION_ENV, region)) if not v]
    if missing:
        return False, ("Azure is not set up: set " + " and ".join(missing)
                       + " (setx, then restart the Studio).")
    return True, f"Azure ({region})"


def billable(body: str) -> int:
    """Characters Azure bills for a request whose <voice> element holds
    ``body``: all of it, markup included."""
    return len(body)


def wrap_rate(body: str, rate: int) -> str:
    """``body`` at ``rate`` percent off normal speed, as edge-tts's "+N%".
    Rate 0 adds nothing: the markup would be billed for no change."""
    return f'<prosody rate="{rate:+d}%">{body}</prosody>' if rate else body


def document(body: str, voice: str) -> str:
    """The SSML document for ``body`` spoken by ``voice``."""
    lang = "-".join(voice.split("-")[:2]) or "en-US"
    return (f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" '
            f'xml:lang="{lang}"><voice name="{voice}">{body}</voice></speak>')


# ----- the local usage ledger -------------------------------------------------

_LEDGER_LOCK = threading.Lock()


def record(chars: int, label: str = "") -> None:
    """Log one billed request. An append of one short line, so the Studio and
    the Pronunciation tool (separate processes) can both write it."""
    line = json.dumps({"t": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                       "chars": int(chars), "what": label}, ensure_ascii=False)
    with _LEDGER_LOCK:
        try:
            with open(config.AZURE_USAGE_PATH, "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except OSError:
            pass               # the meter is advisory; never fail a render on it


def usage(days: int = WINDOW_DAYS) -> int:
    """Characters logged in the last ``days`` days."""
    since = datetime.now(timezone.utc) - timedelta(days=days)
    total = 0
    try:
        with open(config.AZURE_USAGE_PATH, encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    if datetime.fromisoformat(entry["t"]) >= since:
                        total += int(entry["chars"])
                except (ValueError, KeyError, TypeError):
                    continue
    except OSError:
        pass
    return total


def usage_text() -> str:
    """One line for a status bar: the 30-day meter against the free tier."""
    return (f"Azure, last {WINDOW_DAYS} days: {usage():,} of {FREE_CHARS:,} "
            f"free characters")


# ----- requests ----------------------------------------------------------------

_PACE_LOCK = threading.Lock()
_last_request = 0.0


def _pace() -> None:
    """Hold this thread until MIN_INTERVAL has passed since the last request
    this process made."""
    global _last_request
    with _PACE_LOCK:
        wait = _last_request + MIN_INTERVAL - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        _last_request = time.monotonic()


def _post(ssml: str, key: str, region: str, billed) -> bytes:
    """The audio for ``ssml``. ``billed()`` is called as soon as Azure answers
    200: it has charged the request then, even if the body never arrives."""
    req = urllib.request.Request(
        f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1",
        data=ssml.encode("utf-8"), method="POST",
        headers={"Ocp-Apim-Subscription-Key": key,
                 "Content-Type": "application/ssml+xml",
                 "X-Microsoft-OutputFormat": OUTPUT_FORMAT,
                 "User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        billed()
        return resp.read()


def synthesize(body: str, voice: str, out_path: str, label: str = "") -> int:
    """Speak ``body`` (the inside of <voice>: text, <phoneme> tags) with
    ``voice`` into the mp3 ``out_path``. Returns the characters billed.

    Paced to the free tier's rate; a 429 or 5xx is retried with backoff, a
    network failure once. Every request Azure answers 200 is logged, as it
    is billed then. Raises AzureError -- see its ``fatal``. The file appears
    only complete: it is written beside ``out_path`` and swapped in.
    """
    key, region = settings()
    ok, why = available()
    if not ok:
        raise AzureError(why, fatal=True)
    ssml = document(body, voice)
    chars = billable(body)
    waits = list(RETRY_WAITS)
    network_retries = 1
    while True:
        _pace()
        try:
            audio = _post(ssml, key, region, lambda: record(chars, label))
            break
        except urllib.error.HTTPError as e:
            detail = ""
            try:
                detail = e.read(300).decode("utf-8", "replace").strip()
            except OSError:
                pass
            if e.code in (429, 500, 502, 503, 504) and waits:
                time.sleep(waits.pop(0))
                continue
            raise _http_error(e.code, detail) from None
        except (urllib.error.URLError, http.client.HTTPException, OSError) as e:
            # Unreachable, timed out, or the answer was cut off midway
            # (IncompleteRead); a malformed region lands here too.
            if network_retries:
                network_retries -= 1
                time.sleep(NETWORK_RETRY_WAIT)
                continue
            raise AzureError(f"Couldn't reach Azure ({region}): {e}",
                             fatal=True) from None
    if len(audio) < 500:
        # A voice that ignores <phoneme> has been seen to answer with silence.
        raise AzureError(f"Azure returned no audio ({len(audio)} bytes).")
    tmp = f"{out_path}.{os.getpid()}.{threading.get_ident()}.tmp"
    try:
        with open(tmp, "wb") as f:
            f.write(audio)
        _replace(tmp, out_path)
    except OSError as e:
        raise AzureError(f"Couldn't save Azure's audio: {e}") from None
    finally:
        if os.path.exists(tmp):
            try:
                os.remove(tmp)
            except OSError:
                pass
    return chars


def _replace(tmp: str, path: str) -> None:
    """``os.replace``, retried for a few seconds: on Windows it fails while
    another thread has ``path`` open -- edge-tts writing the same plain-text
    cache file for the Studio's playback, say."""
    for attempt in range(60):
        try:
            os.replace(tmp, path)
            return
        except PermissionError:
            if attempt == 59:
                raise
            time.sleep(0.1)


def _http_error(status: int, detail: str) -> AzureError:
    tail = f" ({detail})" if detail else ""
    if status == 400:
        return AzureError("Azure rejected the request (400). Usually an IPA "
                          "symbol it doesn't know" + tail, status)
    if status == 401:
        return AzureError(f"Azure refused the key (401). Check {KEY_ENV} and "
                          f"{REGION_ENV}" + tail, status, fatal=True)
    if status == 403:
        return AzureError("Azure refused the request (403): the key, or the "
                          "free tier's characters for this month are used up"
                          + tail, status, fatal=True)
    if status == 429:
        return AzureError("Azure is still throttling (429) after retries: the "
                          "free tier allows 20 requests a minute, and refuses "
                          "everything once the month's characters are used up"
                          + tail, status, fatal=True)
    return AzureError(f"Azure failed with HTTP {status}" + tail, status,
                      fatal=status >= 500)
