from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class Asset:
    asset_id: str
    file_path: str
    title: str
    duration_sec: float
    source: str = "inbox"
    tags: list[str] = field(default_factory=list)
    status: str = "new"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Project:
    project_id: str
    channel_name: str
    series_name: str
    project_title: str
    platform: str
    language: str
    status: str
    source_video_path: str
    strategy_file_path: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Strategy:
    strategy_number: int
    strategy_title: str
    strategy_type: str
    description: str
    hook_candidates: list[str] = field(default_factory=list)
    title_candidates: list[str] = field(default_factory=list)
    thumbnail_copy_candidates: list[str] = field(default_factory=list)
    estimated_runtime: float = 25.0
    segments: list[dict[str, Any]] = field(default_factory=list)
    hook_score: float = 0.0
    emotion_score: float = 0.0
    clarity_score: float = 0.0
    shorts_fit_score: float = 0.0
    overall_score: float = 0.0
    recommended: bool = False
    platform: str = "YouTube Shorts"
    generated_by_ai: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class QueueItem:
    queue_id: str
    project_id: str
    strategy_number: int
    scheduled_time: str
    upload_status: str = "draft"
    selected_title: str = ""
    selected_hook: str = ""
    selected_thumbnail_copy: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class PerformanceRecord:
    project_id: str
    strategy_number: int
    upload_date: str
    views: int
    likes: int
    comments: int
    title_used: str
    hook_used: str
    thumbnail_copy_used: str
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ChannelProfile:
    channel_name: str
    upload_slots: list[str] = field(default_factory=lambda: ["09:00", "13:00", "20:00"])
    title_tone: str = "casual"
    subtitle_style: str = "rhythm"
    preferred_strategy_types: list[str] = field(default_factory=list)


@dataclass
class SystemLog:
    created_at: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))
    level: str = "INFO"
    message: str = ""
