from __future__ import annotations

from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout


class MatchDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Match Options")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("MVP: number-based matching only."))
