from __future__ import annotations

from pathlib import Path

from models import Project
from settings import PROJECTS_DIR
from utils import ensure_dir, load_json, save_json


class ProjectManager:
    def __init__(self, projects_dir: Path = PROJECTS_DIR) -> None:
        self.projects_dir = ensure_dir(projects_dir)

    def create_project(self, project: Project) -> Path:
        pdir = ensure_dir(self.projects_dir / project.project_id)
        ensure_dir(pdir / "outputs")
        ensure_dir(pdir / "analytics")
        ensure_dir(pdir / "logs")
        save_json(pdir / "project.json", project.to_dict())
        return pdir

    def list_projects(self) -> list[dict]:
        rows = []
        for p in sorted(self.projects_dir.glob("project_*")):
            rows.append(load_json(p / "project.json", {}))
        return [r for r in rows if r]
