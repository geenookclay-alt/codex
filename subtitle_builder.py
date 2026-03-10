from __future__ import annotations

from models import Strategy
from utils import srt_timestamp


class SubtitleBuilder:
    def build_srt(self, strategy: Strategy, style: str = "rhythm") -> str:
        lines: list[str] = []
        t = 0.0
        for i, seg in enumerate(strategy.segments, start=1):
            start = t
            end = t + max(0.6, seg.estimated_seconds)
            t = end
            caption = self._style(seg.caption_text, style)
            lines.extend([
                str(i),
                f"{srt_timestamp(start)} --> {srt_timestamp(end)}",
                caption,
                "",
            ])
        return "\n".join(lines)

    def _style(self, text: str, style: str) -> str:
        if style == "movie":
            return f"♪ {text} ♪"
        return text.upper()
