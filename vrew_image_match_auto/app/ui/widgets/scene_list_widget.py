from __future__ import annotations

from PySide6.QtWidgets import QListWidget

from app.core.project_model import Scene


class SceneListWidget(QListWidget):
    def update_scenes(self, scenes: list[Scene]) -> None:
        self.clear()
        for scene in scenes:
            self.addItem(f"Scene {scene.index} ({len(scene.clip_ids)} clips)")
