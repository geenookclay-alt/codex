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
class Strategy:
    number: int
    title: str
    description: str
    reorder_text: str
    segments: list[Segment] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "number": self.number,
            "title": self.title,
            "description": self.description,
            "reorder_text": self.reorder_text,
            "segments": [s.to_dict() for s in self.segments],
        }
