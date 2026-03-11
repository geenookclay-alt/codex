from __future__ import annotations

from pathlib import Path

from base_parser import BaseStrategyParser
from html_parser import HTMLStrategyParser
from pdf_parser import PDFStrategyParser
from utils import detect_file_type


def create_parser(file_path: str, log) -> BaseStrategyParser:
    ftype = detect_file_type(Path(file_path))
    if ftype == "pdf":
        return PDFStrategyParser(log)
    if ftype == "html":
        return HTMLStrategyParser(log)
    raise ValueError("지원하지 않는 전략 파일 형식입니다. PDF/HTML만 지원합니다.")
