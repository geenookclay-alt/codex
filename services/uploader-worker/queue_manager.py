from __future__ import annotations
from pathlib import Path
import json
from services.common import atomic_write_json

QUEUE_PATH = Path("workspace/queue/upload_queue.json")

VALID = {"draft","render_ready","review_ready","upload_ready","scheduled","uploaded","failed"}

def load_queue() -> list[dict]:
    if not QUEUE_PATH.exists():
        return []
    try:
        return json.loads(QUEUE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []

def save_queue(items: list[dict]) -> None:
    atomic_write_json(QUEUE_PATH, items)

def insert(item: dict) -> None:
    if item.get("upload_status") not in VALID:
        raise ValueError("invalid queue status")
    q = load_queue()
    q.append(item)
    save_queue(q)
