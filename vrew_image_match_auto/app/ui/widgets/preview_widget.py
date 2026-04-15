from __future__ import annotations

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class PreviewWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.label = QLabel("Preview will appear here.")
        self.label.setWordWrap(True)
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)

    def set_preview_text(self, text: str) -> None:
        self.label.setText(text)
