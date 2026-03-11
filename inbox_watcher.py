from __future__ import annotations

import threading
import time
from pathlib import Path
from typing import Callable

from asset_library import AssetLibrary


class InboxWatcher:
    def __init__(self, inbox_dir: Path, library: AssetLibrary, logger: Callable[[str], None], poll_sec: int = 5) -> None:
        self.inbox_dir = inbox_dir
        self.library = library
        self.logger = logger
        self.poll_sec = poll_sec
        self._alive = False
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        if self._alive:
            return
        self._alive = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._alive = False

    def _loop(self) -> None:
        while self._alive:
            try:
                for a in self.library.scan_inbox(self.inbox_dir):
                    self.logger(f"new asset registered={a.asset_id} {a.title} {a.duration_sec}s")
            except Exception as e:
                self.logger(f"inbox watcher error={e}")
            time.sleep(self.poll_sec)
