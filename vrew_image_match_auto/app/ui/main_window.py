from __future__ import annotations

import logging
from collections import Counter
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from app.core.media_mapper import apply_matches_to_project
from app.core.project_model import MatchItem, ProjectData
from app.services.match_service import MatchService
from app.services.preview_service import PreviewService
from app.services.project_service import ProjectService
from app.ui.widgets.clip_list_widget import ClipListWidget
from app.ui.widgets.log_panel import LogPanel
from app.ui.widgets.preview_widget import PreviewWidget
from app.ui.widgets.project_info_widget import ProjectInfoWidget
from app.ui.widgets.result_table import ResultTableWidget
from app.ui.widgets.scene_list_widget import SceneListWidget


class MainWindow(QMainWindow):
    def __init__(self, logger: logging.Logger) -> None:
        super().__init__()
        self.setWindowTitle("Vrew Image Match Auto")
        self.resize(1300, 800)

        self.logger = logger
        self.project_service = ProjectService()
        self.match_service = MatchService()
        self.preview_service = PreviewService()

        self.project_data: ProjectData | None = None
        self.text_items: list[dict] = []
        self.media_map: dict[int, Path] = {}
        self.match_results: list[MatchItem] = []

        self._init_ui()

    def _init_ui(self) -> None:
        central = QWidget()
        main_layout = QVBoxLayout(central)

        top_bar = QHBoxLayout()
        self.btn_open_project = QPushButton("Open Project")
        self.btn_open_text = QPushButton("Open Text File")
        self.btn_open_media = QPushButton("Open Media Folder")
        self.btn_run_match = QPushButton("Run Match")
        self.btn_apply = QPushButton("Apply Matches")
        self.btn_save = QPushButton("Save Output")

        for btn in [
            self.btn_open_project,
            self.btn_open_text,
            self.btn_open_media,
            self.btn_run_match,
            self.btn_apply,
            self.btn_save,
        ]:
            top_bar.addWidget(btn)

        main_layout.addLayout(top_bar)

        splitter = QSplitter(Qt.Horizontal)

        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.addWidget(QLabel("Project Info"))
        self.project_info_widget = ProjectInfoWidget()
        left_layout.addWidget(self.project_info_widget)
        left_layout.addWidget(QLabel("Scenes"))
        self.scene_list_widget = SceneListWidget()
        left_layout.addWidget(self.scene_list_widget)
        left_layout.addWidget(QLabel("Clips"))
        self.clip_list_widget = ClipListWidget()
        left_layout.addWidget(self.clip_list_widget)

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.addWidget(QLabel("Match Results"))
        self.result_table_widget = ResultTableWidget()
        right_layout.addWidget(self.result_table_widget)
        right_layout.addWidget(QLabel("Preview"))
        self.preview_widget = PreviewWidget()
        right_layout.addWidget(self.preview_widget)

        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([450, 850])
        main_layout.addWidget(splitter)

        self.log_panel = LogPanel()
        main_layout.addWidget(QLabel("Logs"))
        main_layout.addWidget(self.log_panel, 1)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        main_layout.addWidget(self.progress_bar)

        self.setCentralWidget(central)
        self._wire_events()

    def _wire_events(self) -> None:
        self.btn_open_project.clicked.connect(self.on_open_project)
        self.btn_open_text.clicked.connect(self.on_open_text)
        self.btn_open_media.clicked.connect(self.on_open_media)
        self.btn_run_match.clicked.connect(self.on_run_match)
        self.btn_apply.clicked.connect(self.on_apply_matches)
        self.btn_save.clicked.connect(self.on_save_output)
        self.clip_list_widget.clip_selected.connect(self.on_clip_selected)

    def on_open_project(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Project File",
            "",
            "Project Files (*.json *.txt);;All Files (*)",
        )
        if not file_path:
            return
        try:
            self.project_data = self.project_service.load_project(Path(file_path))
            self.project_info_widget.update_project(self.project_data)
            self.scene_list_widget.update_scenes(self.project_data.scenes)
            self.clip_list_widget.update_clips(self.project_data.clips)
            self.logger.info(
                "Project loaded: %s (clips=%d, scenes=%d)",
                self.project_data.title,
                len(self.project_data.clips),
                len(self.project_data.scenes),
            )
        except Exception as exc:
            self._show_error(f"Failed to load project: {exc}")

    def on_open_text(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Text File",
            "",
            "Text Files (*.txt *.srt);;All Files (*)",
        )
        if not file_path:
            return
        try:
            self.text_items = self.match_service.load_text_items(Path(file_path))
            self.logger.info("Text items loaded: %d", len(self.text_items))
        except Exception as exc:
            self._show_error(f"Failed to load text file: {exc}")

    def on_open_media(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Open Media Folder", "")
        if not folder:
            return
        try:
            self.media_map = self.match_service.load_media_folder(Path(folder))
            self.logger.info("Media files indexed: %d", len(self.media_map))
        except Exception as exc:
            self._show_error(f"Failed to load media folder: {exc}")

    def on_run_match(self) -> None:
        if not self.project_data:
            self._show_error("Load a project first.")
            return

        self.progress_bar.setValue(20)
        matches, validation = self.match_service.run_number_match(
            self.project_data, self.text_items, self.media_map
        )
        self.match_results = matches
        self.result_table_widget.update_results(matches)
        self.progress_bar.setValue(80)

        counts = Counter(match.status for match in matches)
        self.logger.info(
            "Match completed. success=%d clip_not_found=%d media_not_found=%d invalid_item=%d",
            counts.get("success", 0),
            counts.get("clip_not_found", 0),
            counts.get("media_not_found", 0),
            counts.get("invalid_item", 0),
        )
        for warning in validation.warnings:
            self.logger.warning(warning)
        for error in validation.errors:
            self.logger.error(error)

        self.progress_bar.setValue(100)

    def on_apply_matches(self) -> None:
        if not self.project_data:
            self._show_error("Load a project first.")
            return

        applied = apply_matches_to_project(self.project_data, self.match_results)
        self.clip_list_widget.update_clips(self.project_data.clips)
        self.logger.info("Applied matches to clips: %d", applied)

    def on_save_output(self) -> None:
        if not self.project_data:
            self._show_error("Load a project first.")
            return

        suggested = f"{Path(self.project_data.file_path).stem}_matched.json"
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Output Project",
            suggested,
            "JSON Files (*.json);;All Files (*)",
        )

        requested_path = Path(file_path) if file_path else None
        try:
            out_path = self.project_service.save_project(self.project_data, requested_path)
            self.logger.info("Project saved: %s", out_path)
        except Exception as exc:
            self._show_error(f"Failed to save output: {exc}")

    def on_clip_selected(self, clip: object) -> None:
        preview = self.preview_service.get_preview_text(clip)
        self.preview_widget.set_preview_text(preview)

    def _show_error(self, message: str) -> None:
        self.logger.error(message)
        QMessageBox.critical(self, "Error", message)
