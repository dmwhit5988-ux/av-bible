"""Load/save app settings to config.json beside the app."""

import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
CACHE_DIR = os.path.join(BASE_DIR, "cache")
AUDIO_CACHE_DIR = os.path.join(CACHE_DIR, "audio")
PASSAGE_CACHE_DIR = os.path.join(CACHE_DIR, "passages")
VISUALS_DIR = os.path.join(BASE_DIR, "visuals")
# Read-only, ships with the app: pre-converted local translations, one JSON
# per chapter (kept out of CACHE_DIR so it is never evicted or cleared).
BIBLES_DIR = os.path.join(BASE_DIR, "bibles")

DEFAULTS = {
    "esv_api_key": "",     # kept for when ESV support returns
    "translation": "WEB",
    "voice": "en-US-AndrewNeural",
    "rate": 0,             # speech rate offset in percent, -50..50
    "last_book": "John",
    "last_chapter": 3,
    "show_notes": True,    # show translator notes on the visual stage
    "show_reference": True,  # show the verse reference on the visual stage
}


def load() -> dict:
    cfg = dict(DEFAULTS)
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg.update(json.load(f))
    except (OSError, ValueError):
        pass
    return cfg


def save(cfg: dict) -> None:
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)
    except OSError:
        pass


def ensure_dirs() -> None:
    for d in (CACHE_DIR, AUDIO_CACHE_DIR, PASSAGE_CACHE_DIR, VISUALS_DIR):
        os.makedirs(d, exist_ok=True)
