from __future__ import annotations

from pathlib import Path

from models import Strategy


def build_srt(strategy: Strategy, output_path: Path, style: str = "rhythm") -> Path:
    lines: list[str] = []
    chunks = strategy.hook_candidates[:3] or [strategy.strategy_title]
    for i, text in enumerate(chunks, start=1):
        start = (i - 1) * 4
        end = start + 3
        lines += [
            str(i),
            f"00:00:{start:02d},000 --> 00:00:{end:02d},000",
            text if style == "rhythm" else f"[{style}] {text}",
            "",
        ]
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path
