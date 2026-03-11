from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Callable

DEFAULT_FFMPEG_PATH = r"C:/ffmpeg/bin/ffmpeg.exe"

LogFn = Callable[[str], None]

TIME_PATTERN = re.compile(r"(\d+(?:\.\d+)?)초")
TIMECODE_PATTERN = re.compile(r"\b\d{2}:\d{2}(?:\.\d{1,3})?\b")
SEGMENT_START_PATTERN = re.compile(r"^(\d+)\s+\[([NA])\]\s*(.*)$")


def is_strategy_header(line: str) -> bool:
    text = re.sub(r"\s+", " ", line.strip())
    if not re.match(r"^\d{1,2}\s+.+", text):
        return False
    if re.match(r"^\d{1,2}\s+\[[NA]\]", text):
        return False

    number = int(text.split()[0])
    if number < 1 or number > 10:
        return False

    title = re.sub(r"^\d{1,2}\s+", "", text).strip()
    return len(title) >= 5


def safe_filename(name: str, max_len: int = 60) -> str:
    cleaned = re.sub(r'[\\/:*?"<>|]', "_", name)
    cleaned = re.sub(r"\s+", "_", cleaned).strip("._")
    return cleaned[:max_len] or "untitled"


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


def run_cmd(cmd: list[str], log: LogFn | None = None, cwd: Path | None = None) -> tuple[int, str, str]:
    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=str(cwd) if cwd else None,
    )
    if log and proc.returncode != 0:
        log(f"ffmpeg failed rc={proc.returncode}")
    return proc.returncode, proc.stdout, proc.stderr


def ffmpeg_exists(ffmpeg_path: str) -> bool:
    return Path(ffmpeg_path).exists() or shutil_which(ffmpeg_path) is not None


def shutil_which(binary: str) -> str | None:
    for folder in os.environ.get("PATH", "").split(os.pathsep):
        cand = Path(folder) / binary
        if cand.exists():
            return str(cand)
    return None


def format_python_debug() -> list[str]:
    return [
        f"sys.executable={sys.executable}",
        f"python version={sys.version.split()[0]}",
    ]


def srt_timestamp(seconds: float) -> str:
    milli = int(round(max(0.0, seconds) * 1000))
    h = milli // 3_600_000
    milli %= 3_600_000
    m = milli // 60_000
    milli %= 60_000
    s = milli // 1000
    ms = milli % 1000
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def tc_to_seconds(tc: str) -> float:
    mm, ss = tc.split(":")
    return int(mm) * 60 + float(ss)
