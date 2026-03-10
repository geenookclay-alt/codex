from __future__ import annotations

from pathlib import Path

from bs4 import BeautifulSoup

from pdf_parser import PDFStrategyParser
from models import Segment, Strategy
from utils import SEGMENT_START_PATTERN, STRATEGY_HEADER_PATTERN, TIME_PATTERN, TIMECODE_PATTERN


class HTMLStrategyParser(PDFStrategyParser):
    def parse(self, file_path: str) -> list[Strategy]:
        self.log("bs4 import 성공 여부=True")
        html = Path(file_path).read_text(encoding="utf-8", errors="replace")
        soup = BeautifulSoup(html, "lxml")

        table_strategies = self._parse_from_table(soup)
        if table_strategies:
            self.log(f"input file type=html(table)")
            self.log(f"detected strategies={len(table_strategies)}")
            return table_strategies

        text = soup.get_text("\n", strip=True)
        lines = [ln.rstrip() for ln in text.splitlines() if ln.strip()]
        self.log("input file type=html(text fallback)")
        self.log(f"total lines or extracted text length={len(lines)} lines / {len(text)} chars")
        return self._parse_text_blocks(lines)

    def _parse_from_table(self, soup: BeautifulSoup) -> list[Strategy]:
        tables = soup.find_all("table")
        if not tables:
            return []

        strategies: dict[int, Strategy] = {}
        for table in tables:
            for tr in table.find_all("tr"):
                tds = tr.find_all(["td", "th"])
                cells = [td.get_text(" ", strip=True) for td in tds]
                if not cells:
                    continue

                header_match = STRATEGY_HEADER_PATTERN.match(cells[0])
                if header_match:
                    no = int(header_match.group(1))
                    title = header_match.group(2).strip()
                    strategies.setdefault(no, Strategy(no, title, "", "", []))
                    if len(cells) > 1:
                        strategies[no].description += ("\n" if strategies[no].description else "") + cells[1]
                    continue

                seg_match = SEGMENT_START_PATTERN.match(cells[0])
                if seg_match:
                    content = "\n".join(cells)
                    segment = self._parse_segment([content])
                    current_no = max(strategies.keys()) if strategies else 1
                    strategies.setdefault(current_no, Strategy(current_no, f"전략 {current_no}", "", "", []))
                    strategies[current_no].segments.append(segment)

        result = [strategies[k] for k in sorted(strategies.keys())]
        for s in result:
            self.log(f"strategy {s.number} segment block counts={len(s.segments)}")
        return result
