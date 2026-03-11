from __future__ import annotations

from pathlib import Path

from models import Strategy
from utils import save_json


def package_ai(strategy: Strategy, ai_dir: Path) -> None:
    ai_dir.mkdir(parents=True, exist_ok=True)
    p = f"strategy_{strategy.strategy_number:02d}"
    (ai_dir / f"{p}_hook.txt").write_text("\n".join(strategy.hook_candidates), encoding="utf-8")
    (ai_dir / f"{p}_title_candidates.txt").write_text("\n".join(strategy.title_candidates), encoding="utf-8")
    (ai_dir / f"{p}_thumbnail_copy.txt").write_text("\n".join(strategy.thumbnail_copy_candidates), encoding="utf-8")
    (ai_dir / f"{p}_description.txt").write_text(strategy.description, encoding="utf-8")
    (ai_dir / f"{p}_hashtags.txt").write_text("#shorts #youtube #viral", encoding="utf-8")
    save_json(ai_dir / f"{p}_metadata.json", strategy.to_dict())
    (ai_dir / "codex_prompt.txt").write_text("Shorts Auto Editor v7 prompt", encoding="utf-8")
