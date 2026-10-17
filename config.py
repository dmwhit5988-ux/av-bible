"""Load/save app settings to config.json beside the app."""

import json
import os
import sys
import threading
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
# Where load() copies a config.json it can't parse, before a write replaces it.
BACKUP_PATH = CONFIG_PATH + ".bak"
CACHE_DIR = os.path.join(BASE_DIR, "cache")
AUDIO_CACHE_DIR = os.path.join(CACHE_DIR, "audio")
VISUALS_DIR = os.path.join(BASE_DIR, "visuals")
# Read-only, ships with the app: the World English Bible, one JSON per
# chapter under bibles/WEB/ (kept out of CACHE_DIR so it is never cleared).
BIBLES_DIR = os.path.join(BASE_DIR, "bibles")
# The web app (served from deploy_bundle/, a copy of web/ + bibles/ + visuals/)
# and its pre-rendered narration.
WEB_DIR = os.path.join(BASE_DIR, "web")
WEB_AUDIO_DIR = os.path.join(WEB_DIR, "audio")
# Tracked data the tools keep: the Verifier's whole-canon verdict store, which
# would take a full ASR sweep to rebuild.
DATA_DIR = os.path.join(BASE_DIR, "data")
IPA_CHECKS_PATH = os.path.join(DATA_DIR, "ipa_checks.json")
# Outside the repo, beside it: superseded designs, mockups and scratch work
# kept for reference (backups/, mockups/, _scratch/), and finished video
# renders (renders/).
ARCHIVE_DIR = os.path.join(os.path.dirname(BASE_DIR), "Theoria-archive")
RENDERS_DIR = os.path.join(ARCHIVE_DIR, "renders")

DEFAULTS = {
    "last_book": "Genesis",
    "last_chapter": 1,
    "last_verse": 1,
    "svg_preview_host": "embedded",  # SVG Studio's preview: "embedded" or "browser"
    "editor": "",                    # external editor command; "" = system default
}

# Settings from earlier versions. Dropped on load so an old config.json can't
# resurrect them; the next write leaves them out. The voice and rate are now
# the house constants in tts_engine; the reader's toggles are gone.
OBSOLETE_KEYS = ("esv_api_key", "translation", "show_notes", "mode",
                 "voice", "rate", "show_reference")

_LOCK = threading.Lock()

# Where warnings go besides stderr. The Studio runs under pythonw, which has
# no stderr, so app.py points this at its error log.
warn_hook = None


def _warn(message: str) -> None:
    if warn_hook is not None:
        warn_hook(f"config: {message}")
    elif sys.stderr is not None:
        print(f"config: {message}", file=sys.stderr)


def _read_saved():
    """What config.json holds, as a dict: {} when there is none, or when it
    isn't a valid JSON object -- then it is first copied to config.json.bak,
    so the next write can replace it without losing it. None when it exists
    but can't be read (or backed up): nothing may overwrite it then."""
    for attempt in range(20):
        try:
            with open(CONFIG_PATH, "rb") as f:
                raw = f.read()
            break
        except FileNotFoundError:
            return {}
        except PermissionError as e:
            # Windows: briefly unopenable while another process swaps it in.
            if attempt == 19:
                _warn(f"could not read {CONFIG_PATH}: {e}")
                return None
            time.sleep(0.05)
        except OSError as e:
            _warn(f"could not read {CONFIG_PATH}: {e}")
            return None
    try:
        saved = json.loads(raw.decode("utf-8-sig"))
        problem = "" if isinstance(saved, dict) else "not a JSON object"
    except ValueError as e:              # bad JSON, or not UTF-8
        problem = str(e) or type(e).__name__
    if not problem:
        return saved
    try:
        with open(BACKUP_PATH, "wb") as f:
            f.write(raw)
    except OSError as e:
        _warn(f"{CONFIG_PATH} is unreadable ({problem}) and could not be "
              f"copied to {BACKUP_PATH} ({e}); using the defaults")
        return None
    _warn(f"{CONFIG_PATH} is unreadable ({problem}); using the defaults. "
          f"It was copied to {BACKUP_PATH}.")
    return {}


def _settings(saved) -> dict:
    cfg = dict(DEFAULTS)
    cfg.update(saved or {})
    for key in OBSOLETE_KEYS:
        cfg.pop(key, None)
    return cfg


def load() -> dict:
    """DEFAULTS overlaid with config.json, less OBSOLETE_KEYS. A config.json
    that won't parse is copied to config.json.bak (with a warning on stderr)
    before anything can overwrite it."""
    return _settings(_read_saved())


def _replace(tmp: str, path: str) -> None:
    """``os.replace``, retried briefly: on Windows it fails while another
    thread or process has ``path`` open for reading."""
    for attempt in range(20):
        try:
            os.replace(tmp, path)
            return
        except PermissionError:
            if attempt == 19:
                raise
            time.sleep(0.05)


def save(cfg: dict) -> bool:
    """Write the whole settings dict; True if it was written. It goes via a
    temp file swapped in, so a crash can't leave a half-written config.json.
    On failure the reason goes to stderr, config.json is left as it was and
    the temp file is removed. Prefer update(): a window that saves the dict
    it loaded at startup undoes every other window's changes since then."""
    tmp = f"{CONFIG_PATH}.{os.getpid()}.{threading.get_ident()}.tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)
        _replace(tmp, CONFIG_PATH)
        return True
    except OSError as e:
        _warn(f"could not save {CONFIG_PATH}: {e}")
        return False
    finally:
        if os.path.exists(tmp):
            try:
                os.remove(tmp)
            except OSError:
                pass


def update(**changes) -> dict:
    """Re-read config.json, apply `changes`, write it back and return the
    result. The main window and SVG Studio both write settings, so each
    changes only its own keys this way and neither undoes the other.

    If the write fails, or config.json exists but can't be read (writing
    then would replace settings this never saw), the file is left as it
    was and a warning naming the unsaved keys goes to stderr. The dict is
    returned either way -- it is what would have been written."""
    with _LOCK:
        saved = _read_saved()
        cfg = _settings(saved)
        cfg.update(changes)
        if saved is None or not save(cfg):
            _warn(f"settings not saved: {', '.join(sorted(changes))}")
        return cfg


def ensure_dirs() -> None:
    for d in (CACHE_DIR, AUDIO_CACHE_DIR, VISUALS_DIR):
        os.makedirs(d, exist_ok=True)
