from __future__ import annotations

from pathlib import Path

from app.core.matcher import run_number_based_match
from app.core.project_model import MatchItem, ProjectData
from app.core.validators import ValidationResult, validate_text_items
from app.io.media_indexer import MediaIndexer
from app.io.text_parser import TextParser


class MatchService:
    def __init__(self) -> None:
        self.text_parser = TextParser()
        self.media_indexer = MediaIndexer()

    def load_text_items(self, path: Path) -> list[dict]:
        return self.text_parser.parse(path)

    def load_media_folder(self, path: Path) -> dict[int, Path]:
        return self.media_indexer.index_folder(path)

    def run_number_match(
        self,
        project: ProjectData,
        text_items: list[dict],
        media_map: dict[int, Path],
    ) -> tuple[list[MatchItem], ValidationResult]:
        validation = validate_text_items(text_items)
        matches = run_number_based_match(project, text_items, media_map)
        return matches, validation
