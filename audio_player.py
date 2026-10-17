"""Audio playback via the Windows MCI interface (winmm.dll).

No third-party dependencies; plays mp3 and wav one file at a time.
"""

import ctypes
import os
import threading

_winmm = ctypes.windll.winmm

_MCI_TYPES = {".mp3": "type mpegvideo", ".wav": "type waveaudio"}

# MCI aliases are shared by the whole process, so they are numbered here, not
# per player: two players that each counted from 1 would open the same alias,
# and the second open fails or one player stops the other's file.
_alias_count = 0
_alias_lock = threading.Lock()


class PlayerError(Exception):
    pass


def _mci(command: str) -> str:
    buf = ctypes.create_unicode_buffer(256)
    err = _winmm.mciSendStringW(command, buf, 254, 0)
    if err:
        err_buf = ctypes.create_unicode_buffer(256)
        _winmm.mciGetErrorStringW(err, err_buf, 254)
        raise PlayerError(f"MCI error {err}: {err_buf.value} (cmd: {command})")
    return buf.value


def _new_alias() -> str:
    global _alias_count
    with _alias_lock:
        _alias_count += 1
        return f"theoria{_alias_count}"


class AudioPlayer:
    """Plays one file at a time. Safe to call from a worker thread."""

    def __init__(self):
        self._alias = None
        self._lock = threading.Lock()

    def load(self, path: str) -> None:
        with self._lock:
            self._close_locked()
            alias = _new_alias()
            type_clause = _MCI_TYPES.get(os.path.splitext(path)[1].lower(), "")
            _mci(f'open "{path}" {type_clause} alias {alias}'.replace("  ", " "))
            self._alias = alias

    def play(self) -> None:
        with self._lock:
            if self._alias:
                _mci(f"play {self._alias}")

    def stop(self) -> None:
        with self._lock:
            if self._alias:
                try:
                    _mci(f"stop {self._alias}")
                except PlayerError:
                    pass

    def close(self) -> None:
        with self._lock:
            self._close_locked()

    def _close_locked(self) -> None:
        if self._alias:
            try:
                _mci(f"close {self._alias}")
            except PlayerError:
                pass
            self._alias = None

    def mode(self) -> str:
        """MCI's mode, e.g. playing or stopped ("" when nothing is loaded)."""
        with self._lock:
            if not self._alias:
                return ""
            try:
                return _mci(f"status {self._alias} mode")
            except PlayerError:
                return ""
