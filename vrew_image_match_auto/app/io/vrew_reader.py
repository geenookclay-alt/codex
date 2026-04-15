from __future__ import annotations

import json
from pathlib import Path

from app.core.project_model import Clip, ProjectData, Scene


class VrewProjectReader:
    """MVP reader for mock Vrew project files.

    TODO: Replace parsing with real Vrew project schema support.
    """

    def read(self, path: Path) -> ProjectData:
        if not path.exists():
            raise FileNotFoundError(f"Project file not found: {path}")

        if path.suffix.lower() == ".json":
            return self._read_json(path)

        # Fallback: plain text file where each non-empty line becomes a clip.
        lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        clips = [
            Clip(
                id=f"clip_{idx:03d}",
                index=idx,
                scene_id="scene_001",
                text=line,
                start_time=None,
                end_time=None,
            )
            for idx, line in enumerate(lines, start=1)
        ]
        if not clips:
            clips = self._build_dummy_clips()

        scenes = [Scene(id="scene_001", index=1, clip_ids=[clip.id for clip in clips])]
        return ProjectData(file_path=str(path), title=path.stem, clips=clips, scenes=scenes, metadata={})

    def _read_json(self, path: Path) -> ProjectData:
        data = json.loads(path.read_text(encoding="utf-8"))
        raw_clips = data.get("clips", [])
        raw_scenes = data.get("scenes", [])

        clips = [
            Clip(
                id=str(c.get("id", f"clip_{i:03d}")),
                index=int(c.get("index", i)),
                scene_id=c.get("scene_id"),
                text=str(c.get("text", "")),
                start_time=c.get("start_time"),
                end_time=c.get("end_time"),
                media_type=c.get("media_type"),
                media_path=c.get("media_path"),
                motion_type=c.get("motion_type"),
                status=c.get("status", "pending"),
            )
            for i, c in enumerate(raw_clips, start=1)
        ]
        if not clips:
            clips = self._build_dummy_clips()

        scenes = [
            Scene(
                id=str(s.get("id", f"scene_{i:03d}")),
                index=int(s.get("index", i)),
                clip_ids=[str(cid) for cid in s.get("clip_ids", [])],
            )
            for i, s in enumerate(raw_scenes, start=1)
        ]
        if not scenes:
            scenes = [Scene(id="scene_001", index=1, clip_ids=[clip.id for clip in clips])]

        return ProjectData(
            file_path=str(path),
            title=str(data.get("title", path.stem)),
            clips=clips,
            scenes=scenes,
            metadata=dict(data.get("metadata", {})),
        )

    def _build_dummy_clips(self) -> list[Clip]:
        return [
            Clip(
                id=f"clip_{idx:03d}",
                index=idx,
                scene_id="scene_001",
                text=f"Dummy clip text {idx}",
                start_time=None,
                end_time=None,
            )
            for idx in range(1, 11)
        ]
