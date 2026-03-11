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

FFMPEG_PATH = r"C:/ffmpeg/bin/ffmpeg.exe"
app = FastAPI(title="Video Worker")

def handle_video_task(task: dict) -> None:
    print(f"[video-worker] handling {task}")
    time.sleep(0.3)

@app.on_event("startup")
def startup() -> None:
    start_background_worker("queue:video", handle_video_task)

@app.get("/ffmpeg-examples")
def ffmpeg_examples():
    return {
        "preview": f'{FFMPEG_PATH} -i input.mp4 -vf "scale=720:1280" -t 00:00:15 preview.mp4',
        "burnin": f'{FFMPEG_PATH} -i input.mp4 -vf "subtitles=subtitles.srt" -c:v libx264 burnin.mp4'
    }
