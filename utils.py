from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Callable

LogFn = Callable[[str], None]

TIME_PATTERN = re.compile(r"(\d+(?:\.\d+)?)초")
TIMECODE_PATTERN = re.compile(r"\b\d{2}:\d{2}(?:\.\d{1,3})?\b")
STRATEGY_HEADER_PATTERN = re.compile(r"^\s*(10|[1-9])[\)\].:\-\s]+(.+)$")
SEGMENT_START_PATTERN = re.compile(r"^\s*(\d+)\s+\[([NA])\]\s*(.*)$")


def safe_filename(name: str, max_len: int = 80) -> str:
    sanitized = re.sub(r'[\\/:*?"<>|]', "_", name).strip()
    sanitized = re.sub(r"\s+", "_", sanitized)
    return (sanitized[:max_len] or "untitled").strip("._")


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def detect_file_type(path: Path) -> str:
    ext = path.suffix.lower()
    if ext == ".pdf":
        return "pdf"
    if ext in {".html", ".htm"}:
        return "html"
    return "unknown"


def run_cmd(cmd: list[str], log: LogFn, cwd: Path | None = None) -> tuple[int, str, str]:
    log(f"[CMD] {' '.join(cmd)}")
    p = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(cwd) if cwd else None,
        encoding="utf-8",
        errors="replace",
    )
    if p.stdout.strip():
        log(f"[STDOUT] {p.stdout.strip()}")
    if p.stderr.strip():
        log(f"[STDERR] {p.stderr.strip()}")
    return p.returncode, p.stdout, p.stderr


def format_python_debug() -> str:
    return f"sys.executable={sys.executable}\npython_version={sys.version}"


def srt_timestamp(seconds: float) -> str:
    ms = int(round(seconds * 1000))
    h = ms // 3600000
    ms %= 3600000
    m = ms // 60000
    ms %= 60000
    s = ms // 1000
    ms %= 1000
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def sec_to_ffmpeg(seconds: float) -> str:
    return f"{max(0.0, seconds):.3f}"


def ffmpeg_exists(ffmpeg_path: str) -> bool:
    fp = Path(ffmpeg_path)
    if fp.exists():
        return True
    return any((Path(p) / ffmpeg_path).exists() for p in os.environ.get("PATH", "").split(os.pathsep))
