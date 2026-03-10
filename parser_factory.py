from __future__ import annotations

from pathlib import Path

from base_parser import BaseStrategyParser
from html_parser import HTMLStrategyParser
from pdf_parser import PDFStrategyParser
from utils import LogFn, detect_file_type


def create_parser(file_path: str, log: LogFn) -> BaseStrategyParser:
    file_type = detect_file_type(Path(file_path))
    log(f"input file type={file_type}")

    if file_type == "pdf":
        parser: BaseStrategyParser = PDFStrategyParser(log)
    elif file_type == "html":
        parser = HTMLStrategyParser(log)
    else:
        raise ValueError(f"지원하지 않는 파일 형식: {file_path}")

    log(f"parser selected={parser.__class__.__name__}")
    return parser
