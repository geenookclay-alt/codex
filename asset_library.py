from __future__ import annotations

import uuid
from pathlib import Path

from models import Asset
from settings import ASSET_LIBRARY_PATH, VIDEO_EXTENSIONS
from utils import get_video_duration_sec, load_json, save_json


class AssetLibrary:
    def __init__(self, ffmpeg_path: str) -> None:
        self.ffmpeg_path = ffmpeg_path

    def load(self) -> list[Asset]:
        data = load_json(ASSET_LIBRARY_PATH, [])
        return [Asset(**x) for x in data]

    def save(self, assets: list[Asset]) -> None:
        save_json(ASSET_LIBRARY_PATH, [a.to_dict() for a in assets])

    def register_video(self, path: Path, source: str = "inbox") -> Asset:
        return Asset(
            asset_id=f"asset_{uuid.uuid4().hex[:8]}",
            file_path=str(path),
            title=path.stem.replace("_", " "),
            duration_sec=get_video_duration_sec(path, self.ffmpeg_path),
            source=source,
            tags=[],
            status="new",
        )

    def scan_inbox(self, inbox_dir: Path) -> list[Asset]:
        known = {a.file_path for a in self.load()}
        new_assets: list[Asset] = []
        for p in inbox_dir.iterdir() if inbox_dir.exists() else []:
            if p.suffix.lower() not in VIDEO_EXTENSIONS:
                continue
            if str(p) in known:
                continue
            new_assets.append(self.register_video(p))
        if new_assets:
            merged = self.load() + new_assets
            self.save(merged)
        return new_assets
