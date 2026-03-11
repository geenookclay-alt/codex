from __future__ import annotations

import tempfile
from pathlib import Path

from models import Strategy
from utils import LogFn, run_cmd, tc_to_seconds


class VideoBuilder:
    def __init__(self, ffmpeg_path: str, log: LogFn):
        self.ffmpeg_path = ffmpeg_path
        self.log = log

    def build_preview(self, input_video: Path, strategy: Strategy, output_video: Path) -> None:
        output_video.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="shorts_v4_") as temp_dir:
            temp = Path(temp_dir)
            parts: list[Path] = []
            for i, segment in enumerate(strategy.segments, start=1):
                if not segment.timecodes:
                    continue
                start_sec = tc_to_seconds(segment.timecodes[0])
                duration = max(0.2, segment.estimated_seconds)
                part = temp / f"part_{i:03}.mp4"
                cmd = [
                    self.ffmpeg_path,
                    "-y",
                    "-ss",
                    f"{start_sec:.3f}",
                    "-i",
                    str(input_video),
                    "-t",
                    f"{duration:.3f}",
                    "-c:v",
                    "libx264",
                    "-c:a",
                    "aac",
                    str(part),
                ]
                rc, _, _ = run_cmd(cmd, self.log)
                if rc == 0 and part.exists() and part.stat().st_size > 0:
                    parts.append(part)
            if not parts:
                raise RuntimeError("프리뷰 생성용 세그먼트 추출 실패")

            concat_file = temp / "concat.txt"
            concat_file.write_text("\n".join([f"file '{p.as_posix()}'" for p in parts]), encoding="utf-8")
            cmd_concat = [
                self.ffmpeg_path,
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat_file),
                "-c",
                "copy",
                str(output_video),
            ]
            rc, _, _ = run_cmd(cmd_concat, self.log)
            if rc != 0:
                raise RuntimeError("프리뷰 concat 실패")

    def maybe_burn_in_subtitle(self, input_video: Path, srt_path: Path, output_video: Path) -> tuple[bool, str]:
        if not srt_path.exists():
            return False, f"srt not found: {srt_path}"
        if srt_path.stat().st_size == 0:
            return False, f"srt empty: {srt_path}"

        output_video.parent.mkdir(parents=True, exist_ok=True)
        sub_path = srt_path.resolve().as_posix().replace(":", "\\:")
        cmd = [
            self.ffmpeg_path,
            "-y",
            "-i",
            str(input_video),
            "-vf",
            f"subtitles='{sub_path}'",
            "-c:v",
            "libx264",
            "-c:a",
            "aac",
            str(output_video),
        ]
        rc, _, _ = run_cmd(cmd, self.log)
        if rc != 0:
            return False, "ffmpeg burn-in command failed"
        return True, ""
