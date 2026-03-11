from __future__ import annotations
from datetime import date
from pathlib import Path
from services.common import atomic_write_json

def build_daily_plan(assets: list[dict], max_assets: int = 5) -> dict:
    selected = sorted(assets, key=lambda a: a.get("duration", 0), reverse=True)[:max_assets]
    return {"date": str(date.today()), "selected_assets": selected}

def persist(plan: dict, project_dir: Path) -> None:
    atomic_write_json(project_dir / "daily_plan.json", plan)
