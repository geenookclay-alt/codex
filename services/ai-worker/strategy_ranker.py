from __future__ import annotations

def score(strategy: dict, channel_fit: float = 0.7) -> dict:
    strategy.update({
      "hook_score": 0.7,
      "emotion_score": 0.7,
      "clarity_score": 0.8,
      "shorts_fit_score": 0.8,
      "novelty_score": 0.6,
      "channel_fit_score": channel_fit,
    })
    strategy["overall_score"] = round(sum(strategy[k] for k in ["hook_score","emotion_score","clarity_score","shorts_fit_score","novelty_score","channel_fit_score"]) / 6, 3)
    strategy["bucket"] = "top picks" if strategy["overall_score"] >= 0.78 else "safe picks" if strategy["overall_score"] >= 0.65 else "experiment picks"
    return strategy
