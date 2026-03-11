from __future__ import annotations
from typing import Any

STRATEGY_TYPES = ["result-first","emotional-spike","countdown","revenge/payoff","mystery","twist","info-driven","IF scenario","comparison","perspective-shift"]

def generate(asset_title: str, amount: int = 3) -> list[dict[str, Any]]:
    out = []
    for i in range(1, amount + 1):
        out.append({
            "strategy_number": i,
            "strategy_title": f"{i} {asset_title} payoff angle",
            "strategy_type": STRATEGY_TYPES[i % len(STRATEGY_TYPES)],
            "description": "AI-generated seed strategy.",
            "hook_candidates": ["Wait for the ending"],
            "title_candidates": [f"{asset_title} in 30 seconds"],
            "thumbnail_copy_candidates": ["You won't expect this"],
            "description_candidates": ["Fast short with clear payoff"],
            "hashtags": ["#shorts"],
            "estimated_runtime": 28,
            "generated_by_ai": True,
        })
    return out
