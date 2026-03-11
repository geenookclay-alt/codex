from __future__ import annotations

import re
from pathlib import Path
from typing import Callable

from bs4 import BeautifulSoup

from base_parser import BaseStrategyParser
from models import Strategy
from settings import STRATEGY_TYPES

HEADER_RE = re.compile(r"^(10|[1-9])\s+(?!\[[NA]\])(.*\S.*)$")
SEGMENT_RE = re.compile(r"^\d+\s+\[[NA]\]")


class HTMLStrategyParser(BaseStrategyParser):
    def __init__(self, logger: Callable[[str], None]) -> None:
        super().__init__(logger)

    def parse(self, file_path: Path) -> list[Strategy]:
        html = file_path.read_text(encoding="utf-8", errors="ignore")
        soup = BeautifulSoup(html, "lxml")
        lines: list[str] = []

        containers = soup.select("main, article, section, .content, .container")
        if containers:
            self.logger("html parse mode=container-first")
            for c in containers:
                lines.extend(self._extract_lines(c.get_text("\n")))
        tables = soup.select("table")
        if tables:
            self.logger("html parse mode=table parsing")
            for t in tables:
                lines.extend(self._extract_lines(t.get_text("\n")))
        if not lines:
            self.logger("html parse mode=text fallback")
            lines = self._extract_lines(soup.get_text("\n"))

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
            num = int(m.group(1))
            title = m.group(2).strip()
            if len(title) < 5 or num in strategies:
                continue
            current_no = num
            strategies[num] = Strategy(
                strategy_number=num,
                strategy_title=title,
                strategy_type=STRATEGY_TYPES[(num - 1) % len(STRATEGY_TYPES)],
                description=f"HTML 파싱 전략 {num}",
            )

        valid = [s for s in sorted(strategies.values(), key=lambda x: x.strategy_number) if len(s.segments) > 0]
        self.logger(f"detected strategy titles={[s.strategy_title for s in valid]}")
        self.logger(f"valid strategies count={len(valid)}")
        for s in valid:
            self.logger(f"per-strategy segment count={s.strategy_number}:{len(s.segments)}")
        return valid

    @staticmethod
    def _extract_lines(text: str) -> list[str]:
        return [ln.strip() for ln in text.splitlines() if ln.strip()]
