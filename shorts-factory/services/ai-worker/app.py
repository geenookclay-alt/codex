import json
import os
import threading
import time
from dataclasses import dataclass
from typing import Callable

import redis
from fastapi import FastAPI

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

@dataclass
class Worker:
    queue_name: str
    handler: Callable[[dict], None]

    def run(self) -> None:
        while True:
            _, raw = redis_client.blpop(self.queue_name)
            payload = json.loads(raw)
            self.handler(payload)

def start_background_worker(queue_name: str, handler: Callable[[dict], None]) -> None:
    thread = threading.Thread(target=Worker(queue_name, handler).run, daemon=True)
    thread.start()

app = FastAPI(title="AI Worker")

def handle_ai_task(task: dict) -> None:
    print(f"[ai-worker] handling {task}")
    time.sleep(0.2)

@app.on_event("startup")
def startup() -> None:
    start_background_worker("queue:ai", handle_ai_task)

@app.post("/generate-strategies")
def generate_strategies(payload: dict):
    return {"strategies": [{"title": "5 editing tricks", "hook": "Stop scrolling"}], "input": payload}

@app.post("/generate-titles")
def generate_titles(payload: dict):
    return {"titles": ["3 Secrets for Viral Shorts", "Edit Faster in 30s"], "input": payload}

@app.post("/rank-strategies")
def rank_strategies(payload: dict):
    strategies = payload.get("strategies", [])
    ranked = sorted(strategies, key=lambda x: x.get("score", 0), reverse=True)
    return {"ranked": ranked}
