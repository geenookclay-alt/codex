from __future__ import annotations

from pathlib import Path

from utils import LogFn, run_cmd


class VideoBuilder:
    def __init__(self, ffmpeg_path: str, log: LogFn):
        self.ffmpeg_path = ffmpeg_path
        self.log = log

    def build_preview(self, input_video: Path, output_video: Path) -> None:
        output_video.parent.mkdir(parents=True, exist_ok=True)
        cmd = [self.ffmpeg_path, "-y", "-i", str(input_video), "-t", "30", "-c:v", "libx264", "-c:a", "aac", str(output_video)]
        rc, _, _ = run_cmd(cmd, self.log)
        if rc != 0:
            raise RuntimeError("프리뷰 영상 생성 실패")

    def burn_in_subtitle(self, input_video: Path, srt_path: Path, output_video: Path) -> None:
        ok, reason = self.maybe_burn_in_subtitle(input_video, srt_path, output_video)
        if not ok:
            raise RuntimeError(f"burn-in 영상 생성 실패: {reason}")

    def maybe_burn_in_subtitle(self, input_video: Path, srt_path: Path, output_video: Path) -> tuple[bool, str | None]:
        srt_file = Path(srt_path)
        if not srt_file.exists():
            return False, f"SRT 파일 없음: {srt_path}"
        if srt_file.stat().st_size == 0:
            return False, f"SRT 파일 비어 있음: {srt_path}"

        output_video.parent.mkdir(parents=True, exist_ok=True)
        srt_escaped = str(srt_file).replace("\\", "/").replace(":", "\\:")
        cmd = [
            self.ffmpeg_path,
            "-y",
            "-i",
            str(input_video),
            "-vf",
            f"subtitles='{srt_escaped}'",
            "-c:v",
            "libx264",
            "-c:a",
            "aac",
            str(output_video),
        ]
        rc, _, _ = run_cmd(cmd, self.log)
        if rc != 0:
            return False, "ffmpeg 실행 실패"
        return True, None
