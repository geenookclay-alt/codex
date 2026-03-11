import os
from fastapi import FastAPI
import redis

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
r = redis.Redis.from_url(REDIS_URL, decode_responses=True)
app = FastAPI(title="Analytics Worker")

@app.get('/health')
def health():
    return {'status': 'ok', 'service': 'analytics-worker'}

@app.post('/update-performance-summary')
def update_performance_summary(payload: dict):
    return {'task': 'update_performance_summary', 'summary': {'views': 1000, 'ctr': 0.12}, 'payload': payload}

@app.post('/recalculate-recommendations')
def recalculate_recommendations(payload: dict):
    return {'task': 'recalculate_recommendations', 'recommendations': ['Double down on hook format A', 'Post at 18:00 local'], 'payload': payload}
