from __future__ import annotations

from pathlib import Path
from typing import Callable

from base_parser import BaseStrategyParser
from html_parser import HTMLStrategyParser
from pdf_parser import PDFStrategyParser


def create_parser(file_path: str | Path, logger: Callable[[str], None]) -> BaseStrategyParser:
    path = Path(file_path)
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return PDFStrategyParser(logger)
    if suffix in {".html", ".htm"}:
        logger("input file type=html")
        return HTMLStrategyParser(logger)
    raise ValueError(f"지원하지 않는 파일 형식: {suffix}")
