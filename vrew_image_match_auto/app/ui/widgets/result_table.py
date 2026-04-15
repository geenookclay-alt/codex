from __future__ import annotations

from PySide6.QtWidgets import QTableWidget, QTableWidgetItem

from app.core.project_model import MatchItem


class ResultTableWidget(QTableWidget):
    HEADERS = [
        "Source Index",
        "Source Text",
        "Target Clip",
        "Media Path",
        "Media Type",
        "Mode",
        "Score",
        "Status",
        "Error",
    ]

    def __init__(self) -> None:
        super().__init__(0, len(self.HEADERS))
        self.setHorizontalHeaderLabels(self.HEADERS)

    def update_results(self, matches: list[MatchItem]) -> None:
        self.setRowCount(len(matches))
        for row, match in enumerate(matches):
            values = [
                str(match.source_index),
                match.source_text,
                "" if match.target_clip_index is None else str(match.target_clip_index),
                match.media_path or "",
                match.media_type or "",
                match.match_mode,
                f"{match.score:.2f}",
                match.status,
                match.error_message or "",
            ]
            for col, value in enumerate(values):
                self.setItem(row, col, QTableWidgetItem(value))

        self.resizeColumnsToContents()
