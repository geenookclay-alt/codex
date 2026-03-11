from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ExperimentPolicy:
    max_daily_generation: int = 15
    max_daily_upload_per_channel: int = 3
    shorts_fit_threshold: float = 70.0
    preview_limit: int = 3
    burn_in_enabled: bool = True
