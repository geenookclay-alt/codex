from __future__ import annotations

from models import Strategy
from utils import srt_timestamp


class SubtitleBuilder:
    def build_srt(self, strategy: Strategy, style: str) -> str:
        cursor = 0.0
        rows: list[str] = []
        for order, segment in enumerate(strategy.segments, start=1):
            start = cursor
            end = cursor + max(0.6, segment.estimated_seconds)
            cursor = end
            rows.extend(
                [
                    str(order),
                    f"{srt_timestamp(start)} --> {srt_timestamp(end)}",
                    self._render_caption(segment.caption_text or segment.audio_text, style),
                    "",
                ]
            )
        return "\n".join(rows).strip() + "\n"

    def _render_caption(self, text: str, style: str) -> str:
        cleaned = " ".join(text.split())
        if style == "movie":
            return self._movie(cleaned)
        return self._rhythm(cleaned)

    def _rhythm(self, text: str) -> str:
        words = text.split()
        if len(words) <= 4:
            return text
        lines: list[str] = []
        chunk: list[str] = []
        for word in words:
            chunk.append(word)
            if len(" ".join(chunk)) >= 10:
                lines.append(" ".join(chunk))
                chunk = []
        if chunk:
            lines.append(" ".join(chunk))
        return "\n\n".join(lines[:3])

    def _movie(self, text: str) -> str:
        words = text.split()
        if len(words) <= 8:
            return text
        mid = len(words) // 2
        return " ".join(words[:mid]) + "\n" + " ".join(words[mid:])
