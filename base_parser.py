from __future__ import annotations

import re
from abc import ABC, abstractmethod

from models import Segment, Strategy
from utils import SEGMENT_START_PATTERN, TIME_PATTERN, TIMECODE_PATTERN


class BaseStrategyParser(ABC):
    def __init__(self, log):
        self.log = log

    @abstractmethod
    def parse(self, file_path: str) -> list[Strategy]:
        raise NotImplementedError

    def parse_strategy_content(self, number: int, title: str, lines: list[str]) -> Strategy:
        description_lines: list[str] = []
        segment_blocks: list[list[str]] = []
        current: list[str] = []

        for raw in lines:
            line = raw.strip()
            if not line:
                continue
            if SEGMENT_START_PATTERN.match(line):
                if current:
                    segment_blocks.append(current)
                current = [line]
            elif current:
                current.append(line)
            else:
                description_lines.append(line)

        if current:
            segment_blocks.append(current)

        segments = [self.parse_segment(block) for block in segment_blocks]
        desc = "\n".join(description_lines).strip()
        reorder_match = re.search(r"재배열|재배치|reorder", desc, re.IGNORECASE)
        reorder = desc[reorder_match.start() :].strip() if reorder_match else ""
        return Strategy(number=number, title=title, description=desc, reorder_text=reorder, segments=segments)

    def parse_segment(self, segment_block: list[str]) -> Segment:
        first = segment_block[0]
        match = SEGMENT_START_PATTERN.match(first)
        idx = int(match.group(1)) if match else 0
        mode = match.group(2) if match else "N"
        remain = (match.group(3) if match else first).strip()

        body_lines = [remain] + [line.strip() for line in segment_block[1:] if line.strip()]
        body = "\n".join([line for line in body_lines if line])
        estimated_match = TIME_PATTERN.search(body)
        estimated_seconds = float(estimated_match.group(1)) if estimated_match else 2.0
        timecodes = TIMECODE_PATTERN.findall(body)

        text_lines = [line for line in body_lines if line]
        audio_text = text_lines[0] if text_lines else ""
        caption_text = text_lines[1] if len(text_lines) > 1 else audio_text
        visual_note = " ".join(text_lines[2:]) if len(text_lines) > 2 else ""
        return Segment(
            idx=idx,
            mode=mode,
            audio_text=audio_text,
            caption_text=caption_text,
            estimated_seconds=estimated_seconds,
            timecodes=timecodes,
            visual_note=visual_note,
        )

    def finalize(self, strategies: list[Strategy]) -> list[Strategy]:
        deduped: dict[int, Strategy] = {}
        for strategy in strategies:
            if strategy.number not in range(1, 11):
                continue
            if strategy.number in deduped:
                continue
            if not strategy.segments:
                continue
            deduped[strategy.number] = strategy

        valid = [deduped[number] for number in sorted(deduped)]
        self.log(f"valid strategies count={len(valid)}")
        for strategy in valid:
            self.log(f"per-strategy segment count={strategy.number}:{len(strategy.segments)}")
        return valid
