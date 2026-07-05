"""Audio playback via the Windows MCI interface (winmm.dll).

No third-party dependencies; plays mp3 and wav, supports pause/resume and
position queries (useful later for syncing graphics to long narration files).
"""

import ctypes
import os
import threading

_winmm = ctypes.windll.winmm

_MCI_TYPES = {".mp3": "type mpegvideo", ".wav": "type waveaudio"}


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


class AudioPlayer:
    """Plays one file at a time. Safe to call from a worker thread."""

    def __init__(self):
        self._alias = None
        self._counter = 0
        self._lock = threading.Lock()

    def load(self, path: str) -> None:
        with self._lock:
            self._close_locked()
            self._counter += 1
            alias = f"avbible{self._counter}"
            type_clause = _MCI_TYPES.get(os.path.splitext(path)[1].lower(), "")
            _mci(f'open "{path}" {type_clause} alias {alias}'.replace("  ", " "))
            self._alias = alias

    def play(self) -> None:
        with self._lock:
            if self._alias:
                _mci(f"play {self._alias}")

    def pause(self) -> None:
        with self._lock:
            if self._alias:
                _mci(f"pause {self._alias}")

    def resume(self) -> None:
        with self._lock:
            if self._alias:
                _mci(f"resume {self._alias}")

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

    def position_ms(self) -> int:
        with self._lock:
            if not self._alias:
                return 0
            try:
                return int(_mci(f"status {self._alias} position") or 0)
            except (PlayerError, ValueError):
                return 0

    def length_ms(self) -> int:
        with self._lock:
            if not self._alias:
                return 0
            try:
                return int(_mci(f"status {self._alias} length") or 0)
            except (PlayerError, ValueError):
                return 0

    def mode(self) -> str:
        """One of: playing, paused, stopped, (empty when nothing loaded)."""
        with self._lock:
            if not self._alias:
                return ""
            try:
                return _mci(f"status {self._alias} mode")
            except PlayerError:
                return ""
