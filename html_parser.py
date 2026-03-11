from __future__ import annotations

import re
from pathlib import Path

from bs4 import BeautifulSoup, Tag

from base_parser import BaseStrategyParser
from models import Strategy
from utils import SEGMENT_START_PATTERN, is_strategy_header


class HTMLStrategyParser(BaseStrategyParser):
    CONTAINER_TAGS = ["section", "article", "div"]
    HEADING_TAGS = ["h1", "h2", "h3", "h4"]

    def parse(self, file_path: str) -> list[Strategy]:
        soup = BeautifulSoup(Path(file_path).read_text(encoding="utf-8", errors="replace"), "lxml")
        self.log("input file type=html")

        self.log("html parse mode=container-first")
        strategies, titles = self._parse_container_first(soup)
        if strategies:
            self.log(f"detected strategy titles={titles}")
            return self.finalize(strategies)

        self.log("html parse mode=table parsing")
        strategies, titles = self._parse_table(soup)
        if strategies:
            self.log(f"detected strategy titles={titles}")
            return self.finalize(strategies)

        self.log("html parse mode=text fallback")
        lines = self._normalized_lines(soup.get_text("\n", strip=True).splitlines())
        strategies, titles = self._parse_lines(lines)
        self.log(f"detected strategy titles={titles}")
        return self.finalize(strategies)

    def _parse_container_first(self, soup: BeautifulSoup) -> tuple[list[Strategy], list[str]]:
        found: list[tuple[int, str, Tag]] = []
        seen: set[int] = set()
        for heading in soup.find_all(self.HEADING_TAGS):
            if not isinstance(heading, Tag):
                continue
            text = self._line(heading.get_text(" ", strip=True))
            if not is_strategy_header(text):
                continue
            number = int(text.split()[0])
            if number in seen:
                continue
            title = re.sub(r"^\d{1,2}\s+", "", text).strip()
            found.append((number, title, heading.parent if isinstance(heading.parent, Tag) else heading))
            seen.add(number)

        for tag in soup.find_all(self.CONTAINER_TAGS):
            if not isinstance(tag, Tag):
                continue
            heading = tag.find(self.HEADING_TAGS)
            if not isinstance(heading, Tag):
                continue
            text = self._line(heading.get_text(" ", strip=True))
            if not is_strategy_header(text):
                continue
            number = int(text.split()[0])
            if number in seen:
                continue
            title = re.sub(r"^\d{1,2}\s+", "", text).strip()
            found.append((number, title, tag))
            seen.add(number)

        strategies: list[Strategy] = []
        titles: list[str] = []
        for number, title, tag in found:
            block = self._normalized_lines(tag.get_text("\n", strip=True).splitlines())
            block = [line for line in block if self._line(line) != self._line(f"{number} {title}")]
            strategies.append(self.parse_strategy_content(number, title, block))
            titles.append(f"{number}. {title}")
        return strategies, titles

    def _parse_table(self, soup: BeautifulSoup) -> tuple[list[Strategy], list[str]]:
        lines: list[str] = []
        for table in soup.find_all("table"):
            for row in table.find_all("tr"):
                cells = [self._line(col.get_text(" ", strip=True)) for col in row.find_all(["td", "th"])]
                lines.extend([cell for cell in cells if cell])
        return self._parse_lines(lines)

    def _parse_lines(self, lines: list[str]) -> tuple[list[Strategy], list[str]]:
        starts: list[tuple[int, int, str]] = []
        titles: list[str] = []
        seen: set[int] = set()
        for idx, line in enumerate(lines):
            if SEGMENT_START_PATTERN.match(line):
                continue
            if not is_strategy_header(line):
                continue
            number = int(line.split()[0])
            if number in seen:
                continue
            title = re.sub(r"^\d{1,2}\s+", "", line).strip()
            starts.append((idx, number, title))
            titles.append(f"{number}. {title}")
            seen.add(number)

        strategies: list[Strategy] = []
        for i, (start, number, title) in enumerate(starts):
            end = starts[i + 1][0] if i + 1 < len(starts) else len(lines)
            strategies.append(self.parse_strategy_content(number, title, lines[start + 1 : end]))
        return strategies, titles

    def _normalized_lines(self, lines: list[str]) -> list[str]:
        return [self._line(line) for line in lines if self._line(line)]

    def _line(self, value: str) -> str:
        return re.sub(r"\s+", " ", value).strip()
