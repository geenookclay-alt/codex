from __future__ import annotations

from pathlib import Path

DEFAULT_FFMPEG_PATH = r"C:/ffmpeg/bin/ffmpeg.exe"
WORKSPACE_DIR = Path("workspace")
INBOX_DIR = WORKSPACE_DIR / "inbox_videos"
PROJECTS_DIR = WORKSPACE_DIR / "projects"
QUEUE_DIR = WORKSPACE_DIR / "queue"
SETTINGS_DIR = WORKSPACE_DIR / "settings"
UPLOAD_QUEUE_PATH = QUEUE_DIR / "upload_queue.json"
CHANNEL_PROFILE_PATH = SETTINGS_DIR / "channel_profiles.json"
ASSET_LIBRARY_PATH = WORKSPACE_DIR / "asset_library.json"

VIDEO_EXTENSIONS = {".mp4", ".mov", ".mkv", ".avi", ".webm", ".m4v"}
DEFAULT_WINDOW_TITLE = "Shorts Auto Editor v7"
DEFAULT_WINDOW_SIZE = "1300x920"

STRATEGY_TYPES = [
    "결말 선공개형",
    "감정 폭발형",
    "카운트다운형",
    "참교육형",
    "미스터리형",
    "반전형",
    "정보형",
    "IF 가정형",
    "비교형",
    "시점 교차형",
]
