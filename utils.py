from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable

from settings import DEFAULT_FFMPEG_PATH


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def safe_title(text: str) -> str:
    blocked = '<>:"/\\|?*'
    cleaned = "".join("_" if ch in blocked else ch for ch in text.strip())
    return cleaned[:80] or "untitled"


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def save_json(path: Path, payload: Any) -> None:
    ensure_dir(path.parent)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def save_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    ensure_dir(path.parent)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def ffmpeg_exists(ffmpeg_path: str = DEFAULT_FFMPEG_PATH) -> bool:
    return Path(ffmpeg_path).exists()


def get_video_duration_sec(video_path: Path, ffmpeg_path: str = DEFAULT_FFMPEG_PATH) -> float:
    ffprobe = Path(ffmpeg_path).with_name("ffprobe.exe")
    if not ffprobe.exists() or not video_path.exists():
        return 0.0
    cmd = [
        str(ffprobe),
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(video_path),
    ]
    try:
        out = subprocess.check_output(cmd, text=True).strip()
        return round(float(out), 2)
    except Exception:
        return 0.0


def format_python_debug(ffmpeg_path: str) -> list[str]:
    return [
        f"sys.executable={sys.executable}",
        f"python version={sys.version.split()[0]}",
        f"ffmpeg path={ffmpeg_path}",
    ]


def run_cmd(cmd: list[str], logger: Callable[[str], None]) -> bool:
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        logger(f"command failed: {' '.join(cmd)}")
        logger(e.stderr.strip()[:300])
        return False
