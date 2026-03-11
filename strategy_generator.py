from __future__ import annotations

from models import Segment, Strategy
from prompt_templates import PLATFORM_HINTS, STRATEGY_TYPES, STYLE_HINTS


class StrategyGenerator:
    def __init__(self, log):
        self.log = log

    def generate(
        self,
        count: int,
        style: str,
        platform: str,
        source_hint: str,
        user_keywords: str,
        memo_text: str,
        start_number: int = 1,
    ) -> list[Strategy]:
        style_hint = STYLE_HINTS.get(style, STYLE_HINTS["혼합형"])
        platform_hint = PLATFORM_HINTS.get(platform, PLATFORM_HINTS["YouTube Shorts"])
        keywords = [word.strip() for word in user_keywords.split(",") if word.strip()]
        keyword_seed = keywords[0] if keywords else "핵심 사건"

        result: list[Strategy] = []
        for i in range(count):
            number = start_number + i
            strategy_type = STRATEGY_TYPES[i % len(STRATEGY_TYPES)]
            title = f"{keyword_seed} {strategy_type} 쇼츠 전략"
            if source_hint:
                title = f"{keyword_seed} | {strategy_type}"

            segments = [
                Segment(
                    idx=1,
                    mode="N",
                    audio_text=f"시작 3초 훅: {keyword_seed}의 결과부터 보여준다.",
                    caption_text=f"결과부터 공개: {keyword_seed}",
                    estimated_seconds=3.0,
                    timecodes=["00:00"],
                    visual_note="강한 표정/충격 컷",
                ),
                Segment(
                    idx=2,
                    mode="A",
                    audio_text=f"갈등 핵심과 감정 포인트를 2문장으로 전달. {style_hint}",
                    caption_text="갈등 포인트 압축",
                    estimated_seconds=6.0,
                    timecodes=["00:03"],
                    visual_note="중간 긴장감 장면",
                ),
                Segment(
                    idx=3,
                    mode="N",
                    audio_text=f"마무리 콜투액션: {platform_hint}",
                    caption_text="당신의 선택은?",
                    estimated_seconds=4.0,
                    timecodes=["00:09"],
                    visual_note="클라이맥스/엔딩",
                ),
            ]
            description = f"{style_hint}. {platform_hint}. 메모: {memo_text or '없음'}"
            strategy = Strategy(
                number=number,
                title=title,
                description=description,
                reorder_text="",
                segments=segments,
                strategy_type=strategy_type,
                platform=platform,
                generated_by_ai=True,
            )
            result.append(strategy)
        return result

    def augment_existing(
        self,
        strategies: list[Strategy],
        style: str,
        platform: str,
        user_keywords: str,
        memo_text: str,
    ) -> list[Strategy]:
        style_hint = STYLE_HINTS.get(style, STYLE_HINTS["혼합형"])
        platform_hint = PLATFORM_HINTS.get(platform, PLATFORM_HINTS["YouTube Shorts"])
        kw = user_keywords.strip() or "핵심 장면"
        for i, strategy in enumerate(strategies):
            strategy.strategy_type = strategy.strategy_type or STRATEGY_TYPES[i % len(STRATEGY_TYPES)]
            strategy.platform = platform
            strategy.generated_by_ai = False
            if not strategy.description:
                strategy.description = f"{style_hint} / {platform_hint}"
            strategy.description = f"{strategy.description}\n보강 메모: {memo_text or '없음'} / 키워드: {kw}"
        return strategies
