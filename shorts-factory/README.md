# Shorts Factory v7

Production-ready monorepo scaffold for collaborative YouTube Shorts planning, generation, rendering, scheduling, and analytics.

## Repository layout

```
shorts-factory/
  apps/
    web/
    api/
  services/
    ai-worker/
    video-worker/
    analytics-worker/
  packages/
    shared-types/
    shared-prompts/
  infra/
    postgres/
    redis/
  docs/
```

## Core capabilities implemented
- Team collaboration model (users/teams/roles/channels/projects).
- AI-assisted strategy/title/hook generation endpoints and queue workers.
- Video automation worker with FFmpeg path fixed to `C:/ffmpeg/bin/ffmpeg.exe`.
- Upload queue domain with scheduling status support.
- Performance analytics records and recommendation update pipeline.

## Run locally

1. Install dependencies (pnpm, Python 3.11+, Redis, PostgreSQL).
2. Apply DB schema:
   ```bash
   psql -U shorts -d shorts_factory -f infra/postgres/schema.sql
   ```
3. Start Redis and Postgres (see infra docs).
4. Start API and web:
   ```bash
   pnpm dev:api
   pnpm dev:web
   ```
5. Start workers:
   ```bash
   cd services/ai-worker && pip install -r requirements.txt && uvicorn app:app --port 8101
   cd services/video-worker && pip install -r requirements.txt && uvicorn app:app --port 8102
   cd services/analytics-worker && pip install -r requirements.txt && uvicorn app:app --port 8103
   ```

## Task execution flow
`User action -> API -> task row -> Redis queue -> worker -> DB update -> React Query refresh`

## Example FFmpeg commands

```bash
C:/ffmpeg/bin/ffmpeg.exe -i input.mp4 -vf "scale=720:1280" -t 00:00:15 preview.mp4
C:/ffmpeg/bin/ffmpeg.exe -i input.mp4 -vf "subtitles=subtitles.srt" -c:v libx264 burnin.mp4
```
