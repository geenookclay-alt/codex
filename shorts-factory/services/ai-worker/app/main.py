import os
from fastapi import FastAPI
import redis

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
r = redis.Redis.from_url(REDIS_URL, decode_responses=True)
app = FastAPI(title="AI Worker")

@app.get('/health')
def health():
    return {'status': 'ok', 'service': 'ai-worker'}

@app.post('/generate-strategies')
def generate_strategies(payload: dict):
    return {'strategies': [{'title': '3 hooks to stop the scroll', 'score': 0.87}], 'input': payload}

@app.post('/generate-titles')
def generate_titles(payload: dict):
    topic = payload.get('topic', 'Shorts')
    return {'titles': [f'{topic}: Do this before posting', f'{topic}: 5 mistakes to avoid']}

@app.post('/rank-strategies')
def rank_strategies(payload: dict):
    strategies = payload.get('strategies', [])
    ranked = sorted(strategies, key=lambda s: s.get('score', 0), reverse=True)
    return {'ranked': ranked}
