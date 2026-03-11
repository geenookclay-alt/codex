from __future__ import annotations

from pathlib import Path

from models import Strategy


def write_edl(strategy: Strategy, output_path: Path) -> Path:
    body = [f"TITLE: {strategy.strategy_title}", "FCM: NON-DROP FRAME", ""]
    for i, seg in enumerate(strategy.segments or [{"line": "auto segment"}] * 3, start=1):
        body.append(f"{i:03d}  AX       V     C        00:00:00:00 00:00:03:00 00:00:00:00 00:00:03:00")
        body.append(f"* FROM CLIP NAME: {seg.get('line', 'segment')}")
    output_path.write_text("\n".join(body), encoding="utf-8")
    return output_path
