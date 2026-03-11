from __future__ import annotations
from pathlib import Path
from services.common import DEFAULT_FFMPEG_PATH, logger

def build_preview(source: Path, output: Path) -> Path:
    logger.info("ffmpeg path=%s", DEFAULT_FFMPEG_PATH)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(b"")
    return output

def build_burnin(preview: Path, srt: Path, output: Path) -> Path | None:
    if not srt.exists() or srt.stat().st_size == 0:
        logger.info("burn-in skipped: missing or empty srt")
        return None
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(b"")
    return output
