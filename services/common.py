from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import json
import logging

DEFAULT_FFMPEG_PATH = r"C:/ffmpeg/bin/ffmpeg.exe"

logger = logging.getLogger("sfv8")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

def atomic_write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)

@dataclass
class TaskEnvelope:
    task_type: str
    payload: dict[str, Any] = field(default_factory=dict)
