from __future__ import annotations

from pathlib import Path

from settings import DEFAULT_FFMPEG_PATH
from utils import run_cmd


def make_preview(video_src: Path, out_path: Path, ffmpeg_path: str, logger) -> bool:
    cmd = [ffmpeg_path or DEFAULT_FFMPEG_PATH, "-y", "-i", str(video_src), "-t", "30", "-c:v", "libx264", str(out_path)]
    ok = run_cmd(cmd, logger)
    if ok:
        logger(f"generated output paths={out_path}")
    return ok


def make_burn_in(video_src: Path, srt_path: Path, out_path: Path, ffmpeg_path: str, logger) -> bool:
    if not srt_path.exists():
        logger("burn-in skipped reason=srt missing")
        return False
    if srt_path.stat().st_size == 0:
        logger("burn-in skipped reason=srt empty")
        return False
    subtitle_filter = 'subtitles=' + str(srt_path).replace('\\', '/')
    cmd = [ffmpeg_path or DEFAULT_FFMPEG_PATH, "-y", "-i", str(video_src), "-vf", subtitle_filter, "-c:v", "libx264", str(out_path)]
    ok = run_cmd(cmd, logger)
    if ok:
        logger(f"generated output paths={out_path}")
    return ok
