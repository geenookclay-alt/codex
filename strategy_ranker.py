from __future__ import annotations

from models import Strategy, StrategyEvaluation


class StrategyRanker:
    def evaluate(self, strategy: Strategy) -> StrategyEvaluation:
        title_len = len(strategy.title)
        seg_count = len(strategy.segments)
        runtime = strategy.estimated_runtime()

        hook_score = min(10.0, 4.0 + (title_len / 18.0) + (1.5 if seg_count >= 3 else 0.5))
        emotion_score = min(10.0, 3.5 + seg_count * 1.1)
        clarity_score = min(10.0, 4.0 + (2.0 if strategy.description else 0.0) + min(seg_count, 4) * 0.8)
        shorts_fit_score = min(10.0, 10.0 - abs(35.0 - runtime) / 6.0)

        overall = round((hook_score + emotion_score + clarity_score + shorts_fit_score) / 4.0, 2)
        recommended = overall >= 7.2
        return StrategyEvaluation(
            hook_score=round(hook_score, 2),
            emotion_score=round(emotion_score, 2),
            clarity_score=round(clarity_score, 2),
            shorts_fit_score=round(max(0.0, shorts_fit_score), 2),
            overall_score=overall,
            recommended=recommended,
        )

    def rank(self, strategies: list[Strategy]) -> list[Strategy]:
        for strategy in strategies:
            strategy.apply_evaluation(self.evaluate(strategy))
        return sorted(strategies, key=lambda item: item.overall_score, reverse=True)
