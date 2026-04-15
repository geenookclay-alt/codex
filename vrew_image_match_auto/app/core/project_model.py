from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class Clip:
    id: str
    index: int
    scene_id: str | None
    text: str
    start_time: float | None
    end_time: float | None
    media_type: str | None = None
    media_path: str | None = None
    motion_type: str | None = None
    status: str = "pending"


@dataclass(slots=True)
class Scene:
    id: str
    index: int
    clip_ids: list[str] = field(default_factory=list)


@dataclass(slots=True)
class MatchItem:
    source_index: int
    source_text: str
    target_clip_index: int | None
    media_path: str | None
    media_type: str | None
    match_mode: str
    score: float
    status: str
    error_message: str | None = None


@dataclass(slots=True)
class ProjectData:
    file_path: str
    title: str
    clips: list[Clip] = field(default_factory=list)
    scenes: list[Scene] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "file_path": self.file_path,
            "title": self.title,
            "clips": [asdict(clip) for clip in self.clips],
            "scenes": [asdict(scene) for scene in self.scenes],
            "metadata": self.metadata,
        }
