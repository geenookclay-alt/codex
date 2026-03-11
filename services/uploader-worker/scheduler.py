from __future__ import annotations
from datetime import datetime

def schedule(item: dict, when: str) -> dict:
    datetime.fromisoformat(when)
    item["scheduled_time"] = when
    item["upload_status"] = "scheduled"
    return item
