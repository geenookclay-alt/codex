from __future__ import annotations

from pathlib import Path


class MediaIndexer:
    SUPPORTED_EXTENSIONS = {
        ".png",
        ".jpg",
        ".jpeg",
        ".webp",
        ".bmp",
        ".mp4",
        ".mov",
        ".avi",
        ".mkv",
    }

    def index_folder(self, path: Path) -> dict[int, Path]:
        if not path.exists() or not path.is_dir():
            raise FileNotFoundError(f"Media folder does not exist: {path}")

        media_map: dict[int, Path] = {}
        for file in sorted(path.iterdir()):
            if not file.is_file() or file.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
                continue
            if file.stem.isdigit():
                media_map[int(file.stem)] = file

        return media_map
