from __future__ import annotations

from pathlib import Path

from app.core.export_manager import build_output_path
from app.core.project_model import ProjectData
from app.io.vrew_reader import VrewProjectReader
from app.io.vrew_writer import VrewProjectWriter


class ProjectService:
    def __init__(self) -> None:
        self.reader = VrewProjectReader()
        self.writer = VrewProjectWriter()

    def load_project(self, path: Path) -> ProjectData:
        return self.reader.read(path)

    def save_project(self, project: ProjectData, requested_path: Path | None = None) -> Path:
        source_path = Path(project.file_path)
        output_path = requested_path or build_output_path(source_path)
        return self.writer.write(project, output_path)
