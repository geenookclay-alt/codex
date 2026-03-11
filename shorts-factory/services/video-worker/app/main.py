import os
from fastapi import FastAPI
import redis

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
r = redis.Redis.from_url(REDIS_URL, decode_responses=True)
app = FastAPI(title="Video Worker")

FFMPEG_PATH = os.getenv('FFMPEG_PATH', r'C:/ffmpeg/bin/ffmpeg.exe')

@app.get('/health')
def health():
    return {'status': 'ok', 'service': 'video-worker', 'ffmpeg': FFMPEG_PATH}

@app.post('/build-preview')
def build_preview(payload: dict):
    return {'task': 'build_preview', 'ffmpeg_cmd': f"{FFMPEG_PATH} -y -i input.mp4 -vf scale=720:1280 -t 20 preview.mp4", 'payload': payload}

@app.post('/build-burnin')
def build_burnin(payload: dict):
    return {'task': 'build_burnin', 'ffmpeg_cmd': f"{FFMPEG_PATH} -y -i input.mp4 -vf subtitles=subtitles.srt burnin.mp4", 'payload': payload}

@app.post('/build-edl')
def build_edl(payload: dict):
    return {'task': 'build_edl', 'edl': [{'start': 0, 'end': 3, 'clip': 'intro.mp4'}], 'payload': payload}
