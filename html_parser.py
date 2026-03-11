from __future__ import annotations

import re
from pathlib import Path

from bs4 import BeautifulSoup, Tag

from models import Strategy
from pdf_parser import PDFStrategyParser

SEGMENT_LINE_PATTERN = re.compile(r"^(\d+)\s+\[([NA])\]\s*(.*)$")


def is_strategy_header(line: str) -> bool:
    line = line.strip()

    if not re.match(r"^\d{1,2}\s+.+", line):
        return False

    if re.match(r"^\d{1,2}\s+\[[NA]\]", line):
        return False

    num = int(line.split()[0])
    if num < 1 or num > 10:
        return False

    title = re.sub(r"^\d{1,2}\s+", "", line)

    if len(title) < 5:
        return False

    return True


class HTMLStrategyParser(PDFStrategyParser):
    _CONTAINER_TAGS = ["section", "article", "div", "h1", "h2", "h3"]

    def parse(self, file_path: str) -> list[Strategy]:
        html = Path(file_path).read_text(encoding="utf-8", errors="replace")
        soup = BeautifulSoup(html, "lxml")

        self.log("input file type=html")

        self.log("html parse mode=container-first")
        container_strategies, container_headers = self._parse_container_first(soup)
        if container_strategies:
            self.log(f"detected strategy headers={container_headers}")
            return self._finalize_strategies(container_strategies)

        self.log("html parse mode=table parsing")
        table_strategies, table_headers = self._parse_table_first(soup)
        if table_strategies:
            self.log(f"detected strategy headers={table_headers}")
            return self._finalize_strategies(table_strategies)

        self.log("html parse mode=text fallback")
        text = soup.get_text("\n", strip=True)
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        text_strategies, text_headers = self._parse_text_fallback(lines)
        self.log(f"detected strategy headers={text_headers}")
        return self._finalize_strategies(text_strategies)

    def _parse_container_first(self, soup: BeautifulSoup) -> tuple[list[Strategy], list[str]]:
        header_tags: list[tuple[Tag, int, str, str]] = []

        for tag in soup.find_all(self._CONTAINER_TAGS):
            if not isinstance(tag, Tag):
                continue
            line = re.sub(r"\s+", " ", tag.get_text(" ", strip=True)).strip()
            if not line or not is_strategy_header(line):
                continue
            number, title = self._extract_header_parts(line)
            header_tags.append((tag, number, title, line))

        strategies: list[Strategy] = []
        detected_headers = [row[3] for row in header_tags]
        seen_numbers: set[int] = set()

        for tag, number, title, _ in header_tags:
            if number in seen_numbers:
                continue
            seen_numbers.add(number)
            block_lines = self._extract_container_block(tag)
            strategy = self._parse_strategy_content(number, title, block_lines)
            strategies.append(strategy)

        return strategies, detected_headers

    def _parse_table_first(self, soup: BeautifulSoup) -> tuple[list[Strategy], list[str]]:
        lines: list[str] = []
        for tr in soup.find_all("tr"):
            if not isinstance(tr, Tag):
                continue
            cells = [cell.get_text(" ", strip=True) for cell in tr.find_all(["th", "td"])]
            for cell in cells:
                normalized = re.sub(r"\s+", " ", cell).strip()
                if normalized:
                    lines.append(normalized)
        return self._parse_text_fallback(lines)

    def _parse_text_fallback(self, lines: list[str]) -> tuple[list[Strategy], list[str]]:
        starts: list[tuple[int, int, str]] = []
        detected_headers: list[str] = []

        for idx, line in enumerate(lines):
            if not is_strategy_header(line):
                continue
            number, title = self._extract_header_parts(line)
            starts.append((idx, number, title))
            detected_headers.append(line.strip())

        strategies: list[Strategy] = []
        seen_numbers: set[int] = set()
        for i, (start_idx, number, title) in enumerate(starts):
            if number in seen_numbers:
                continue
            seen_numbers.add(number)
            end_idx = starts[i + 1][0] if i + 1 < len(starts) else len(lines)
            block = lines[start_idx + 1 : end_idx]
            strategies.append(self._parse_strategy_content(number, title, block))

        return strategies, detected_headers

    def _extract_header_parts(self, line: str) -> tuple[int, str]:
        number = int(line.split()[0])
        title = re.sub(r"^\d{1,2}\s+", "", line).strip()
        return number, title

    def _extract_container_block(self, header_tag: Tag) -> list[str]:
        container = self._find_container(header_tag)
        raw_lines = container.get_text("\n", strip=True).splitlines()
        lines = [re.sub(r"\s+", " ", ln).strip() for ln in raw_lines if ln.strip()]

        header_text = re.sub(r"\s+", " ", header_tag.get_text(" ", strip=True)).strip()
        start_index = 0
        for i, line in enumerate(lines):
            if line == header_text:
                start_index = i + 1
                break
        return lines[start_index:]

    def _find_container(self, tag: Tag) -> Tag:
        for parent in tag.parents:
            if isinstance(parent, Tag) and parent.name in {"section", "article", "div"}:
                return parent
        return tag

    def _parse_strategy_content(self, number: int, title: str, lines: list[str]) -> Strategy:
        segment_blocks: list[list[str]] = []
        current_block: list[str] = []
        description_lines: list[str] = []

        for line in lines:
            if SEGMENT_LINE_PATTERN.match(line):
                if current_block:
                    segment_blocks.append(current_block)
                current_block = [line]
            elif current_block:
                current_block.append(line)
            else:
                description_lines.append(line)

        if current_block:
            segment_blocks.append(current_block)

        segments = [self._parse_segment(block) for block in segment_blocks]
        description = "\n".join(description_lines).strip()
        reorder_match = re.search(r"재배열|재배치|reorder", description, re.IGNORECASE)
        reorder_text = description[reorder_match.start() :].strip() if reorder_match else ""
        return Strategy(number=number, title=title, description=description, reorder_text=reorder_text, segments=segments)

    def _finalize_strategies(self, strategies: list[Strategy]) -> list[Strategy]:
        unique_strategies: dict[int, Strategy] = {}
        for strategy in strategies:
            if strategy.number < 1 or strategy.number > 10:
                continue
            if strategy.number not in unique_strategies:
                unique_strategies[strategy.number] = strategy

        ordered = [unique_strategies[num] for num in sorted(unique_strategies)]
        valid_strategies = [s for s in ordered if len(s.segments) > 0]

        self.log(f"valid strategies count={len(valid_strategies)}")
        for strategy in valid_strategies:
            self.log(f"strategy segment count={strategy.number}:{len(strategy.segments)}")

        return valid_strategies
