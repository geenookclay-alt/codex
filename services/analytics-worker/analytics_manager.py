from __future__ import annotations
from pathlib import Path
import csv, json
from services.common import atomic_write_json

def import_performance(path: Path) -> list[dict]:
    if path.suffix.lower() == ".csv":
        with path.open("r", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    return json.loads(path.read_text(encoding="utf-8"))

def save_records(records: list[dict], out: Path) -> None:
    atomic_write_json(out, {"records": records})
