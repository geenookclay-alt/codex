from __future__ import annotations

from typing import Callable

from models import Strategy
from settings import STRATEGY_TYPES


class StrategyGenerator:
    def __init__(self, logger: Callable[[str], None]) -> None:
        self.logger = logger

    def generate(self, count: int, platform: str, keywords: str, memo: str) -> list[Strategy]:
        strategies: list[Strategy] = []
        kw = [k.strip() for k in keywords.split(",") if k.strip()] or ["핵심"]
        for i in range(1, min(10, count) + 1):
            base = kw[(i - 1) % len(kw)]
            strategies.append(
                Strategy(
                    strategy_number=i,
                    strategy_title=f"{i} {base} 중심 쇼츠 전략",
                    strategy_type=STRATEGY_TYPES[(i - 1) % len(STRATEGY_TYPES)],
                    description=f"{memo or '자동 생성'} 기반 전략",
                    hook_candidates=[f"{base} 이 장면 놓치면 손해", f"{base}의 진짜 결말", f"{base} 핵심만 20초 요약"],
                    title_candidates=[f"{base} 20초 정리", f"{base} 충격 포인트", f"{base} 바로 이해"],
                    thumbnail_copy_candidates=[f"{base} 실화?", f"{base} 핵심", f"{base} 반전"],
                    generated_by_ai=True,
                    platform=platform,
                )
            )
        self.logger(f"generated strategies={len(strategies)}")
        return strategies

    def augment_existing(self, strategies: list[Strategy]) -> list[Strategy]:
        for s in strategies:
            if len(s.hook_candidates) < 3:
                s.hook_candidates += [f"{s.strategy_title} 훅 {i}" for i in range(1, 4 - len(s.hook_candidates) + 1)]
            if len(s.title_candidates) < 3:
                s.title_candidates += [f"{s.strategy_title} 제목 {i}" for i in range(1, 4 - len(s.title_candidates) + 1)]
            if len(s.thumbnail_copy_candidates) < 3:
                s.thumbnail_copy_candidates += [f"{s.strategy_title} 썸네일 {i}" for i in range(1, 4 - len(s.thumbnail_copy_candidates) + 1)]
        self.logger("existing strategies augmented")
        return strategies
