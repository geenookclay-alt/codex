from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class Segment:
    idx: int
    mode: str
    audio_text: str
    caption_text: str
    estimated_seconds: float
    timecodes: list[str] = field(default_factory=list)
    visual_note: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class StrategyEvaluation:
    hook_score: float = 0.0
    emotion_score: float = 0.0
    clarity_score: float = 0.0
    shorts_fit_score: float = 0.0
    overall_score: float = 0.0
    recommended: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Strategy:
    number: int
    title: str
    description: str
    reorder_text: str
    segments: list[Segment] = field(default_factory=list)
    strategy_type: str = "혼합형"
    hook_score: float = 0.0
    emotion_score: float = 0.0
    clarity_score: float = 0.0
    shorts_fit_score: float = 0.0
    overall_score: float = 0.0
    recommended: bool = False
    platform: str = "YouTube Shorts"
    generated_by_ai: bool = False

    def estimated_runtime(self) -> float:
        return round(sum(max(0.0, segment.estimated_seconds) for segment in self.segments), 2)

    def apply_evaluation(self, evaluation: StrategyEvaluation) -> None:
        self.hook_score = evaluation.hook_score
        self.emotion_score = evaluation.emotion_score
        self.clarity_score = evaluation.clarity_score
        self.shorts_fit_score = evaluation.shorts_fit_score
        self.overall_score = evaluation.overall_score
        self.recommended = evaluation.recommended

    def to_dict(self) -> dict[str, Any]:
        return {
            "number": self.number,
            "title": self.title,
            "description": self.description,
            "reorder_text": self.reorder_text,
            "segments": [segment.to_dict() for segment in self.segments],
            "strategy_type": self.strategy_type,
            "hook_score": self.hook_score,
            "emotion_score": self.emotion_score,
            "clarity_score": self.clarity_score,
            "shorts_fit_score": self.shorts_fit_score,
            "overall_score": self.overall_score,
            "recommended": self.recommended,
            "platform": self.platform,
            "generated_by_ai": self.generated_by_ai,
            "estimated_runtime": self.estimated_runtime(),
        }
