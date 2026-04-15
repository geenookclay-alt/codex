from __future__ import annotations

from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout


class SettingsDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Settings")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("TODO: application settings and preferences."))
