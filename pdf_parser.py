from __future__ import annotations

import re
from pathlib import Path
from typing import Callable

import pdfplumber

from base_parser import BaseStrategyParser
from models import Strategy
from settings import STRATEGY_TYPES

HEADER_RE = re.compile(r"^(10|[1-9])\s+(?!\[[NA]\])(.*\S.*)$")
SEGMENT_RE = re.compile(r"^\d+\s+\[[NA]\]")


class PDFStrategyParser(BaseStrategyParser):
    def __init__(self, logger: Callable[[str], None]) -> None:
        super().__init__(logger)

    def parse(self, file_path: Path) -> list[Strategy]:
        self.logger("input file type=pdf")
        lines: list[str] = []
        with pdfplumber.open(str(file_path)) as pdf:
            for page in pdf.pages:
                text = page.extract_text() or ""
                lines.extend([ln.strip() for ln in text.splitlines() if ln.strip()])

        strategies: dict[int, Strategy] = {}
        current_no: int | None = None
        for line in lines:
            if SEGMENT_RE.match(line):
                if current_no in strategies:
                    strategies[current_no].segments.append({"line": line})
                continue
            m = HEADER_RE.match(line)
            if not m:
                continue
            no = int(m.group(1))
            title = m.group(2).strip()
            if no in strategies or len(title) < 5:
                continue
            current_no = no
            strategies[no] = Strategy(
                strategy_number=no,
                strategy_title=title,
                strategy_type=STRATEGY_TYPES[(no - 1) % len(STRATEGY_TYPES)],
                description=f"PDF 파싱 전략 {no}",
            )

        valid = [s for s in sorted(strategies.values(), key=lambda x: x.strategy_number) if s.segments]
        self.logger(f"detected strategy titles={[s.strategy_title for s in valid]}")
        self.logger(f"valid strategies count={len(valid)}")
        for s in valid:
            self.logger(f"per-strategy segment count={s.strategy_number}:{len(s.segments)}")
        return valid
