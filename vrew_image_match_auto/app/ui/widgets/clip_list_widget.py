from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QListWidget

from app.core.project_model import Clip


class ClipListWidget(QListWidget):
    clip_selected = Signal(object)

    def __init__(self) -> None:
        super().__init__()
        self._clips: list[Clip] = []
        self.currentRowChanged.connect(self._on_row_changed)

    def update_clips(self, clips: list[Clip]) -> None:
        self.clear()
        self._clips = clips
        for clip in clips:
            self.addItem(f"#{clip.index:03d} [{clip.status}] {clip.text}")

    def _on_row_changed(self, row: int) -> None:
        clip = self._clips[row] if 0 <= row < len(self._clips) else None
        self.clip_selected.emit(clip)
