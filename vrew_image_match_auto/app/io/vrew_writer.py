from __future__ import annotations

import json
from pathlib import Path

from app.core.project_model import ProjectData


class VrewProjectWriter:
    """MVP writer that exports ProjectData as JSON."""

    def write(self, project: ProjectData, output_path: Path) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(project.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return output_path
