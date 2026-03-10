from __future__ import annotations

import re
from pathlib import Path

from bs4 import BeautifulSoup, Tag

from models import Strategy
from pdf_parser import PDFStrategyParser
from utils import SEGMENT_START_PATTERN


class HTMLStrategyParser(PDFStrategyParser):
    _HEADER_PREFIX_PATTERN = re.compile(r"^\s*(10|[1-9])(?:\s*[:\-\)\.]\s*|\s+)(.+)$")
    _SEGMENT_LIKE_HEADER_PATTERN = re.compile(r"^\s*(10|[1-9])\s+\[[NA]\]\b")
    _CONTEXT_KEYWORDS = (
        "[전략",
        "전략",
        "재배치",
        "재배열",
        "Content ID 회피",
        "바이럴",
    )

    def parse(self, file_path: str) -> list[Strategy]:
        self.log("bs4 import 성공 여부=True")
        html = Path(file_path).read_text(encoding="utf-8", errors="replace")
        soup = BeautifulSoup(html, "lxml")

        self.log("input file type=html")
        self.log("html parse mode=container-first+row-detection")

        container_strategies, container_count, raw_headers = self._parse_from_containers(soup)
        self.log(f"detected strategy containers={container_count}")
        self.log(f"raw detected strategy headers={raw_headers}")

        if container_strategies:
            return self._finalize_strategies(container_strategies)

        text = soup.get_text("\n", strip=True)
        lines = [ln.rstrip() for ln in text.splitlines() if ln.strip()]
        self.log("html parse mode=text-fallback")
        self.log(f"total lines or extracted text length={len(lines)} lines / {len(text)} chars")

        parsed, fallback_headers = self._parse_text_blocks_with_filter(lines)
        self.log(f"raw detected strategy headers={fallback_headers}")
        return self._finalize_strategies(parsed)

    def _parse_from_containers(self, soup: BeautifulSoup) -> tuple[list[Strategy], int, list[str]]:
        candidate_tags = ["h2", "h3", "h1", "p", "span", "div", "section", "article"]
        headers: list[tuple[Tag, int, str, str]] = []

        for tag_name in candidate_tags:
            for tag in soup.find_all(tag_name):
                if not isinstance(tag, Tag):
                    continue
                text = tag.get_text(" ", strip=True)
                header = self._extract_strategy_header(text)
                if not header:
                    continue
                no, title = header
                if not self._has_strategy_context(tag, text):
                    continue
                headers.append((tag, no, title, text))

        raw_headers = [h[3] for h in headers]
        dedup_by_no: dict[int, tuple[Tag, str]] = {}
        for tag, no, title, _ in headers:
            if no not in dedup_by_no:
                dedup_by_no[no] = (tag, title)

        strategies: list[Strategy] = []
        for no in sorted(dedup_by_no):
            if not (1 <= no <= 10):
                continue
            header_tag, title = dedup_by_no[no]
            container = self._find_strategy_container(header_tag)
            lines = self._extract_lines_from_container(container)
            strategy = self._parse_strategy_lines(no, title, lines)
            strategies.append(strategy)

        return strategies, len(strategies), raw_headers

    def _extract_strategy_header(self, line: str) -> tuple[int, str] | None:
        line = re.sub(r"\s+", " ", line).strip()
        if not line:
            return None
        if self._SEGMENT_LIKE_HEADER_PATTERN.match(line):
            return None

        m = self._HEADER_PREFIX_PATTERN.match(line)
        if not m:
            return None

        number = int(m.group(1))
        title = (m.group(2) or "").strip()
        title = re.sub(r"^\[[^\]]+\]\s*", "", title).strip()
        if not (1 <= number <= 10):
            return None
        if not title or len(title) < 5:
            return None
        if re.match(r"^\[[NA]\]", title):
            return None
        return number, title

    def _has_strategy_context(self, tag: Tag, line: str) -> bool:
        context = [line]
        prev = tag.previous_sibling
        nxt = tag.next_sibling
        if isinstance(prev, Tag):
            context.append(prev.get_text(" ", strip=True))
        if isinstance(nxt, Tag):
            context.append(nxt.get_text(" ", strip=True))
        parent = tag.parent
        if isinstance(parent, Tag):
            context.append(parent.get_text(" ", strip=True)[:500])
        merged = " ".join([c for c in context if c])
        return any(kw in merged for kw in self._CONTEXT_KEYWORDS)

    def _find_strategy_container(self, header_tag: Tag) -> Tag:
        for anc in header_tag.parents:
            if not isinstance(anc, Tag):
                continue
            if anc.name not in {"section", "article", "div", "table", "body"}:
                continue
            lines = self._extract_lines_from_container(anc)
            if any(SEGMENT_START_PATTERN.match(ln) for ln in lines):
                return anc
            if any(re.match(r"^\d+\s+\[[NA]\]", ln) for ln in lines):
                return anc
        return header_tag

    def _extract_lines_from_container(self, container: Tag) -> list[str]:
        lines: list[str] = []
        for tr in container.find_all("tr"):
            cells = [td.get_text(" ", strip=True) for td in tr.find_all(["td", "th"])]
            cells = [c for c in cells if c]
            if not cells:
                continue
            merged = " ".join(cells)
            lines.extend(self._split_line(merged))

        for tag in container.find_all(["div", "section", "article", "h1", "h2", "h3", "p", "span", "td"]):
            if not isinstance(tag, Tag):
                continue
            if tag.find("table"):
                continue
            txt = tag.get_text(" ", strip=True)
            if txt:
                lines.extend(self._split_line(txt))

        if not lines:
            text = container.get_text("\n", strip=True)
            for line in text.splitlines():
                lines.extend(self._split_line(line))

        seen: set[str] = set()
        uniq: list[str] = []
        for ln in lines:
            normalized = re.sub(r"\s+", " ", ln).strip()
            if normalized and normalized not in seen:
                seen.add(normalized)
                uniq.append(normalized)
        return uniq

    def _split_line(self, text: str) -> list[str]:
        parts = re.split(r"\s*(?:\n|\||/)\s*", text)
        return [p.strip() for p in parts if p.strip()]

    def _parse_strategy_lines(self, number: int, title: str, lines: list[str]) -> Strategy:
        segment_blocks: list[list[str]] = []
        current_segment: list[str] = []
        description_lines: list[str] = []

        for line in lines:
            if SEGMENT_START_PATTERN.match(line):
                if current_segment:
                    segment_blocks.append(current_segment)
                current_segment = [line]
                continue
            if current_segment:
                current_segment.append(line)
            else:
                description_lines.append(line)

        if current_segment:
            segment_blocks.append(current_segment)

        segments = [self._parse_segment(sb) for sb in segment_blocks]
        desc = "\n".join([ln for ln in description_lines if ln.strip() and ln.strip() != title]).strip()
        reorder_m = re.search(r"재배열|재배치|reorder", desc, re.IGNORECASE)
        reorder = desc[reorder_m.start() :].strip() if reorder_m else ""
        return Strategy(number=number, title=title, description=desc, reorder_text=reorder, segments=segments)

    def _parse_text_blocks_with_filter(self, lines: list[str]) -> tuple[list[Strategy], list[str]]:
        strategy_starts: list[tuple[int, int, str]] = []
        raw_headers: list[str] = []

        for i, line in enumerate(lines):
            header = self._extract_strategy_header_from_line(lines, i)
            if not header:
                continue
            no, title = header
            strategy_starts.append((i, no, title))
            raw_headers.append(line.strip())

        strategies: list[Strategy] = []
        for idx, (start, number, title) in enumerate(strategy_starts):
            end = strategy_starts[idx + 1][0] if idx + 1 < len(strategy_starts) else len(lines)
            block = lines[start:end]
            strategies.append(self._parse_strategy_block(number, title, block))

        return strategies, raw_headers

    def _extract_strategy_header_from_line(self, lines: list[str], i: int) -> tuple[int, str] | None:
        line = lines[i].strip()
        header = self._extract_strategy_header(line)
        if not header:
            return None

        if self._SEGMENT_LIKE_HEADER_PATTERN.match(line):
            return None

        number, title = header
        start = max(0, i - 2)
        end = min(len(lines), i + 3)
        context = " ".join(lines[start:end])
        if not any(kw in context for kw in self._CONTEXT_KEYWORDS):
            return None

        return number, title

    def _finalize_strategies(self, parsed: list[Strategy]) -> list[Strategy]:
        merged: dict[int, Strategy] = {}
        for st in parsed:
            if not (1 <= st.number <= 10):
                continue
            existing = merged.get(st.number)
            if existing is None:
                merged[st.number] = Strategy(st.number, st.title, st.description, st.reorder_text, list(st.segments))
                continue

            if existing.title.startswith("전략") and st.title:
                existing.title = st.title
            if st.description:
                existing.description = f"{existing.description}\n{st.description}".strip()
            if st.reorder_text and not existing.reorder_text:
                existing.reorder_text = st.reorder_text
            existing.segments.extend(st.segments)

        self.log(f"deduplicated strategy count={len(merged)}")
        for no in sorted(merged):
            self.log(f"strategy {no} segment count={len(merged[no].segments)}")

        valid = [merged[no] for no in sorted(merged) if len(merged[no].segments) >= 1]
        self.log(f"final valid strategies count={len(valid)}")
        return valid
