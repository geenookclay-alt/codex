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

app = FastAPI(title="Analytics Worker")

def handle_analytics_task(task: dict) -> None:
    print(f"[analytics-worker] handling {task}")
    time.sleep(0.2)

@app.on_event("startup")
def startup() -> None:
    start_background_worker("queue:analytics", handle_analytics_task)

@app.post("/aggregate")
def aggregate(payload: dict):
    return {"status": "aggregated", "payload": payload}
