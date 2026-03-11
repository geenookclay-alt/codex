from __future__ import annotations

from models import Strategy
from utils import tc_to_seconds


class EDLWriter:
    def build_edl(self, strategy: Strategy) -> str:
        rows = [f"TITLE: strategy_{strategy.number:02}", "FCM: NON-DROP FRAME"]
        rec_cursor = 0.0
        for idx, segment in enumerate(strategy.segments, start=1):
            source_in = tc_to_seconds(segment.timecodes[0]) if segment.timecodes else 0.0
            source_out = source_in + max(0.1, segment.estimated_seconds)
            rec_in = rec_cursor
            rec_out = rec_cursor + max(0.1, segment.estimated_seconds)
            rec_cursor = rec_out
            rows.append(
                f"{idx:03}  AX       V     C        "
                f"{self._tc(source_in)} {self._tc(source_out)} {self._tc(rec_in)} {self._tc(rec_out)}"
            )
            rows.append(f"* FROM CLIP NAME: SEG_{segment.idx:02}")
        return "\n".join(rows) + "\n"

    def _tc(self, seconds: float, fps: int = 30) -> str:
        total_frames = int(round(seconds * fps))
        hh = total_frames // (fps * 3600)
        total_frames %= fps * 3600
        mm = total_frames // (fps * 60)
        total_frames %= fps * 60
        ss = total_frames // fps
        ff = total_frames % fps
        return f"{hh:02}:{mm:02}:{ss:02}:{ff:02}"
