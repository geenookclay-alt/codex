from __future__ import annotations

from PySide6.QtWidgets import QFormLayout, QLabel, QWidget

from app.core.project_model import ProjectData


class ProjectInfoWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.title_label = QLabel("-")
        self.file_label = QLabel("-")
        self.clip_count_label = QLabel("0")
        self.scene_count_label = QLabel("0")

        layout = QFormLayout(self)
        layout.addRow("Title:", self.title_label)
        layout.addRow("File:", self.file_label)
        layout.addRow("Clips:", self.clip_count_label)
        layout.addRow("Scenes:", self.scene_count_label)

    def update_project(self, project: ProjectData | None) -> None:
        if project is None:
            self.title_label.setText("-")
            self.file_label.setText("-")
            self.clip_count_label.setText("0")
            self.scene_count_label.setText("0")
            return

        self.title_label.setText(project.title)
        self.file_label.setText(project.file_path)
        self.clip_count_label.setText(str(len(project.clips)))
        self.scene_count_label.setText(str(len(project.scenes)))
