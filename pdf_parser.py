from __future__ import annotations

import re

import pdfplumber

from base_parser import BaseStrategyParser
from models import Strategy
from utils import SEGMENT_START_PATTERN, is_strategy_header


class PDFStrategyParser(BaseStrategyParser):
    def parse(self, file_path: str) -> list[Strategy]:
        chunks: list[str] = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text() or ""
                if text.strip():
                    chunks.append(text)

        lines = [re.sub(r"\s+", " ", line).strip() for line in "\n".join(chunks).splitlines() if line.strip()]
        self.log("input file type=pdf")

        starts: list[tuple[int, int, str]] = []
        titles: list[str] = []
        for i, line in enumerate(lines):
            if SEGMENT_START_PATTERN.match(line):
                continue
            if not is_strategy_header(line):
                continue
            number = int(line.split()[0])
            title = re.sub(r"^\d{1,2}\s+", "", line).strip()
            starts.append((i, number, title))
            titles.append(f"{number}. {title}")

        self.log(f"detected strategy titles={titles}")

        strategies: list[Strategy] = []
        for idx, (start, number, title) in enumerate(starts):
            end = starts[idx + 1][0] if idx + 1 < len(starts) else len(lines)
            strategies.append(self.parse_strategy_content(number, title, lines[start + 1 : end]))
        return self.finalize(strategies)
