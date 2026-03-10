from __future__ import annotations

from models import Strategy


class EDLWriter:
    def build_edl(self, strategy: Strategy) -> str:
        lines = ["TITLE: Shorts Auto Editor", "FCM: NON-DROP FRAME"]
        start_tc = 0
        for i, seg in enumerate(strategy.segments, start=1):
            dur_frames = int(seg.estimated_seconds * 30)
            in_f = start_tc
            out_f = start_tc + dur_frames
            start_tc = out_f
            lines.append(
                f"{i:03}  AX       V     C        {self._tc(in_f)} {self._tc(out_f)} {self._tc(in_f)} {self._tc(out_f)}"
            )
            lines.append(f"* FROM CLIP NAME: SEG_{seg.idx:02}")
        return "\n".join(lines) + "\n"

    def _tc(self, frames: int, fps: int = 30) -> str:
        h = frames // (fps * 3600)
        frames %= fps * 3600
        m = frames // (fps * 60)
        frames %= fps * 60
        s = frames // fps
        f = frames % fps
        return f"{h:02}:{m:02}:{s:02}:{f:02}"
