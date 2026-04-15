from __future__ import annotations

from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout


class MotionDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Motion Settings")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("TODO: motion presets and per-clip controls."))
