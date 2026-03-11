from __future__ import annotations

def generate_recommendations(performance_records: list[dict]) -> dict:
    high = [r for r in performance_records if int(r.get("views", 0)) > 10000]
    return {
        "preferred_strategy_types": ["result-first", "mystery"] if high else ["info-driven"],
        "title_patterns": ["curiosity + payoff"],
        "queue_threshold": 0.72,
    }
