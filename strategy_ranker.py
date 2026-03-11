from __future__ import annotations

from pathlib import Path

from models import Strategy
from utils import save_json


class StrategyRanker:
    def rank(self, strategies: list[Strategy], ranking_path: Path | None = None) -> list[Strategy]:
        for s in strategies:
            s.hook_score = min(100, 60 + len(s.hook_candidates) * 8)
            s.emotion_score = 65 + (s.strategy_number % 5) * 6
            s.clarity_score = 68 + (s.strategy_number % 4) * 5
            s.shorts_fit_score = min(100, 70 + len(s.title_candidates) * 6)
            s.overall_score = round((s.hook_score + s.emotion_score + s.clarity_score + s.shorts_fit_score) / 4, 2)
        ordered = sorted(strategies, key=lambda x: x.overall_score, reverse=True)
        for idx, s in enumerate(ordered):
            s.recommended = idx < 3
        if ranking_path:
            save_json(ranking_path, [s.to_dict() for s in ordered])
        return ordered
