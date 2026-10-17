"""Load/save app settings to config.json beside the app."""

import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
CACHE_DIR = os.path.join(BASE_DIR, "cache")
AUDIO_CACHE_DIR = os.path.join(CACHE_DIR, "audio")
VISUALS_DIR = os.path.join(BASE_DIR, "visuals")
# Read-only, ships with the app: the World English Bible, one JSON per
# chapter under bibles/WEB/ (kept out of CACHE_DIR so it is never cleared).
BIBLES_DIR = os.path.join(BASE_DIR, "bibles")

DEFAULTS = {
    "voice": "en-US-AndrewNeural",
    "rate": 0,             # speech rate offset in percent, -50..50
    "last_book": "John",
    "last_chapter": 3,
    "show_reference": True,  # show the verse reference on the visual stage
}

# Settings from the multi-translation / ESV era. Dropped on load so an old
# config.json can't resurrect them; the next save writes the file without.
OBSOLETE_KEYS = ("esv_api_key", "translation", "show_notes", "mode")


def load() -> dict:
    cfg = dict(DEFAULTS)
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg.update(json.load(f))
    except (OSError, ValueError):
        pass
    for key in OBSOLETE_KEYS:
        cfg.pop(key, None)
    return cfg


def save(cfg: dict) -> None:
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)
    except OSError:
        pass


def ensure_dirs() -> None:
    for d in (CACHE_DIR, AUDIO_CACHE_DIR, VISUALS_DIR):
        os.makedirs(d, exist_ok=True)
