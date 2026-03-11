from __future__ import annotations

from pathlib import Path

from models import Strategy


def build_upload_package(strategy: Strategy, upload_dir: Path) -> None:
    upload_dir.mkdir(parents=True, exist_ok=True)
    (upload_dir / "final_title.txt").write_text(strategy.title_candidates[0] if strategy.title_candidates else strategy.strategy_title, encoding="utf-8")
    (upload_dir / "final_description.txt").write_text(strategy.description, encoding="utf-8")
    (upload_dir / "final_hashtags.txt").write_text("#shorts #youtube #trend", encoding="utf-8")
    (upload_dir / "final_thumbnail_copy.txt").write_text(
        strategy.thumbnail_copy_candidates[0] if strategy.thumbnail_copy_candidates else strategy.strategy_title,
        encoding="utf-8",
    )
    checklist = "\n".join([
        "preview 확인 완료",
        "burn-in 확인 완료",
        "제목 선택 필요",
        "설명 선택 필요",
        "해시태그 선택 필요",
    ])
    (upload_dir / "upload_checklist.txt").write_text(checklist, encoding="utf-8")
