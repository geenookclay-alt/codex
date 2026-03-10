from __future__ import annotations

import re
from pathlib import Path

import pdfplumber

from base_parser import BaseStrategyParser
from models import Segment, Strategy
from utils import (
    SEGMENT_START_PATTERN,
    STRATEGY_HEADER_PATTERN,
    TIME_PATTERN,
    TIMECODE_PATTERN,
)


class PDFStrategyParser(BaseStrategyParser):
    def parse(self, file_path: str) -> list[Strategy]:
        self.log(f"pdfplumber.__file__={getattr(pdfplumber, '__file__', 'N/A')}")
        text_chunks: list[str] = []
        with pdfplumber.open(file_path) as pdf:
            for i, page in enumerate(pdf.pages, start=1):
                page_text = page.extract_text() or ""
                self.log(f"[PDF] page={i}, chars={len(page_text)}")
                if page_text:
                    text_chunks.append(page_text)

        full_text = "\n".join(text_chunks)
        lines = [ln.rstrip() for ln in full_text.splitlines()]
        self.log(f"input file type=pdf")
        self.log(f"total lines or extracted text length={len(lines)} lines / {len(full_text)} chars")
        return self._parse_text_blocks(lines)

    def _parse_text_blocks(self, lines: list[str]) -> list[Strategy]:
        strategy_starts: list[tuple[int, int, str]] = []
        for i, line in enumerate(lines):
            m = STRATEGY_HEADER_PATTERN.match(line)
            if m:
                strategy_starts.append((i, int(m.group(1)), m.group(2).strip()))

        strategies: list[Strategy] = []
        for idx, (start, number, title) in enumerate(strategy_starts):
            end = strategy_starts[idx + 1][0] if idx + 1 < len(strategy_starts) else len(lines)
            block = lines[start:end]
            strategy = self._parse_strategy_block(number, title, block)
            strategies.append(strategy)

        self.log(f"detected strategies={len(strategies)}")
        return strategies

    def _parse_strategy_block(self, number: int, title: str, block: list[str]) -> Strategy:
        description_lines: list[str] = []
        segment_blocks: list[list[str]] = []
        current_segment: list[str] = []

        for line in block[1:]:
            if SEGMENT_START_PATTERN.match(line):
                if current_segment:
                    segment_blocks.append(current_segment)
                current_segment = [line]
            else:
                if current_segment:
                    current_segment.append(line)
                else:
                    description_lines.append(line)
        if current_segment:
            segment_blocks.append(current_segment)

        segments = [self._parse_segment(sb) for sb in segment_blocks]
        self.log(f"strategy {number} segment block counts={len(segment_blocks)}")

        desc = "\n".join([x for x in description_lines if x.strip()]).strip()
        reorder_m = re.search(r"재배열|reorder", desc, re.IGNORECASE)
        reorder = desc[reorder_m.start():].strip() if reorder_m else ""
        return Strategy(number=number, title=title, description=desc, reorder_text=reorder, segments=segments)

    def _parse_segment(self, segment_block: list[str]) -> Segment:
        first = segment_block[0]
        m = SEGMENT_START_PATTERN.match(first)
        idx = int(m.group(1)) if m else 0
        mode = m.group(2) if m else "N"
        remain = (m.group(3) or "").strip() if m else first
        body = "\n".join([remain] + segment_block[1:]).strip()

        sec_m = TIME_PATTERN.search(body)
        estimated_seconds = float(sec_m.group(1)) if sec_m else 2.0
        timecodes = TIMECODE_PATTERN.findall(body)

        lines = [ln.strip() for ln in body.splitlines() if ln.strip()]
        audio_text = lines[0] if lines else body
        caption_text = lines[1] if len(lines) > 1 else audio_text
        visual_note = " ".join(lines[2:]) if len(lines) > 2 else ""

        return Segment(
            idx=idx,
            mode=mode,
            audio_text=audio_text,
            caption_text=caption_text,
            estimated_seconds=estimated_seconds,
            timecodes=timecodes,
            visual_note=visual_note,
        )
