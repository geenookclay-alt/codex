from __future__ import annotations

import uuid
from pathlib import Path

from models import QueueItem
from settings import UPLOAD_QUEUE_PATH
from utils import load_json, save_json


class QueueManager:
    def __init__(self, queue_path: Path = UPLOAD_QUEUE_PATH) -> None:
        self.queue_path = queue_path

    def list_items(self) -> list[QueueItem]:
        return [QueueItem(**x) for x in load_json(self.queue_path, [])]

    def save_items(self, items: list[QueueItem]) -> None:
        save_json(self.queue_path, [x.to_dict() for x in items])

    def enqueue(self, project_id: str, strategy_number: int, scheduled_time: str) -> QueueItem:
        item = QueueItem(
            queue_id=f"q_{uuid.uuid4().hex[:8]}",
            project_id=project_id,
            strategy_number=strategy_number,
            scheduled_time=scheduled_time,
            upload_status="draft",
        )
        rows = self.list_items()
        rows.append(item)
        self.save_items(rows)
        return item

    def transition(self, queue_id: str, new_status: str) -> bool:
        valid = {
            "draft": {"render_ready", "failed"},
            "render_ready": {"review_ready", "failed"},
            "review_ready": {"upload_ready", "failed"},
            "upload_ready": {"scheduled", "failed"},
            "scheduled": {"uploaded", "failed"},
            "uploaded": set(),
            "failed": {"draft"},
        }
        items = self.list_items()
        for it in items:
            if it.queue_id == queue_id and new_status in valid.get(it.upload_status, set()):
                it.upload_status = new_status
                self.save_items(items)
                return True
        return False
