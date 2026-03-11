from __future__ import annotations

from pathlib import Path

from models import PerformanceRecord
from utils import load_json, save_json


class AnalyticsManager:
    def __init__(self, analytics_path: Path) -> None:
        self.analytics_path = analytics_path

    def list_records(self) -> list[PerformanceRecord]:
        return [PerformanceRecord(**x) for x in load_json(self.analytics_path, [])]

    def append(self, record: PerformanceRecord) -> None:
        rows = self.list_records()
        rows.append(record)
        save_json(self.analytics_path, [r.to_dict() for r in rows])
