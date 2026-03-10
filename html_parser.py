from __future__ import annotations

import re
from pathlib import Path

from bs4 import BeautifulSoup, Tag

from pdf_parser import PDFStrategyParser
from models import Strategy
from utils import SEGMENT_START_PATTERN


class HTMLStrategyParser(PDFStrategyParser):
    _HEADER_WITH_LABEL = re.compile(r"^\s*(?:전략|strategy)\s*(10|[1-9])\s*[:\-\)\.]?\s*(.*)$", re.IGNORECASE)
    _HEADER_NUMBERED = re.compile(r"^\s*(10|[1-9])\s*[\)\].:\-]+\s+(.+)$")

    def parse(self, file_path: str) -> list[Strategy]:
        self.log("bs4 import 성공 여부=True")
        html = Path(file_path).read_text(encoding="utf-8", errors="replace")
        soup = BeautifulSoup(html, "lxml")

        self.log("input file type=html")
        table_strategies, container_count = self._parse_from_table(soup)
        self.log("html parse mode=table-first")
        self.log(f"detected strategy containers={container_count}")

        if table_strategies:
            final = self._finalize_strategies(table_strategies)
            return final

        text = soup.get_text("\n", strip=True)
        lines = [ln.rstrip() for ln in text.splitlines() if ln.strip()]
        self.log("html parse mode=text-fallback")
        self.log(f"total lines or extracted text length={len(lines)} lines / {len(text)} chars")
        parsed = self._parse_text_blocks(lines)
        final = self._finalize_strategies(parsed)
        return final

    def _parse_from_table(self, soup: BeautifulSoup) -> tuple[list[Strategy], int]:
        tables = soup.find_all("table")
        if not tables:
            return [], 0

        strategies: dict[int, Strategy] = {}
        detected_containers = 0

        for table in tables:
            if not isinstance(table, Tag):
                continue

            current_no: int | None = None
            touched_this_table = False

            for tr in table.find_all("tr"):
                cells = [td.get_text(" ", strip=True) for td in tr.find_all(["td", "th"])]
                cells = [c for c in cells if c]
                if not cells:
                    continue

                header = self._extract_header_from_cells(cells)
                if header:
                    no, title = header
                    current_no = no
                    touched_this_table = True
                    strategy = strategies.setdefault(no, Strategy(no, title or f"전략 {no}", "", "", []))
                    if title and strategy.title.startswith("전략 "):
                        strategy.title = title
                    continue

                segment = self._extract_segment_from_cells(cells)
                if segment:
                    if current_no is None:
                        continue
                    strategies.setdefault(current_no, Strategy(current_no, f"전략 {current_no}", "", "", [])).segments.append(segment)
                    touched_this_table = True
                    continue

                if current_no is not None:
                    desc = " | ".join(cells)
                    if desc and len(desc) < 300:
                        st = strategies[current_no]
                        st.description = f"{st.description}\n{desc}".strip()

            if touched_this_table:
                detected_containers += 1

        return [strategies[k] for k in sorted(strategies.keys())], detected_containers

    def _extract_header_from_cells(self, cells: list[str]) -> tuple[int, str] | None:
        candidates = [cells[0]]
        if len(cells) >= 2:
            candidates.append(f"{cells[0]} {cells[1]}")

        for raw in candidates:
            text = re.sub(r"\s+", " ", raw).strip()
            if SEGMENT_START_PATTERN.match(text):
                continue

            m = self._HEADER_WITH_LABEL.match(text)
            if m:
                no = int(m.group(1))
                if 1 <= no <= 10:
                    title = (m.group(2) or "").strip()
                    return no, title

            m = self._HEADER_NUMBERED.match(text)
            if m:
                no = int(m.group(1))
                if 1 <= no <= 10:
                    title = m.group(2).strip()
                    if "[N]" in text or "[A]" in text:
                        continue
                    return no, title
        return None

    def _extract_segment_from_cells(self, cells: list[str]):
        for i, cell in enumerate(cells):
            if SEGMENT_START_PATTERN.match(cell):
                merged = "\n".join(cells[i:])
                return self._parse_segment([merged])
        return None

    def _finalize_strategies(self, parsed: list[Strategy]) -> list[Strategy]:
        merged: dict[int, Strategy] = {}
        for st in parsed:
            if not (1 <= st.number <= 10):
                continue
            existing = merged.get(st.number)
            if not existing:
                merged[st.number] = st
                continue
            if existing.title.startswith("전략 ") and st.title:
                existing.title = st.title
            if st.description:
                existing.description = f"{existing.description}\n{st.description}".strip()
            existing.segments.extend(st.segments)

        if len(merged) > 10:
            self.log("경고: 전략 개수가 비정상적으로 많습니다. HTML 헤더 탐지를 재검토하세요.")

        for no in sorted(merged.keys()):
            self.log(f"strategy {no} segment count={len(merged[no].segments)}")

        valid = [merged[no] for no in sorted(merged.keys()) if merged[no].segments]
        self.log(f"final valid strategies count={len(valid)}")
        return valid
