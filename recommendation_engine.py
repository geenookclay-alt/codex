from __future__ import annotations

from collections import Counter

from models import PerformanceRecord


class RecommendationEngine:
    def recommend(self, records: list[PerformanceRecord]) -> dict:
        if not records:
            return {"top_strategies": [], "title_patterns": [], "hook_patterns": [], "thumbnail_patterns": []}
        ranked = sorted(records, key=lambda r: (r.views + r.likes * 3 + r.comments * 5), reverse=True)
        title_kw = Counter([r.title_used.split()[0] for r in records if r.title_used])
        hook_kw = Counter([r.hook_used.split()[0] for r in records if r.hook_used])
        thumb_kw = Counter([r.thumbnail_copy_used.split()[0] for r in records if r.thumbnail_copy_used])
        return {
            "top_strategies": [f"{r.project_id}:{r.strategy_number}" for r in ranked[:3]],
            "title_patterns": [k for k, _ in title_kw.most_common(5)],
            "hook_patterns": [k for k, _ in hook_kw.most_common(5)],
            "thumbnail_patterns": [k for k, _ in thumb_kw.most_common(5)],
        }
