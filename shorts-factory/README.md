# Shorts Factory v7

Production-ready monorepo scaffold for collaborative YouTube Shorts production.

## Architecture
- **Frontend:** Next.js (TypeScript), Tailwind-ready, React Query
- **Service API:** NestJS (TypeScript)
- **Workers:** FastAPI + Redis queue consumers (AI, video, analytics)
- **Queue:** Redis
- **Database:** PostgreSQL
- **Video Tooling:** FFmpeg (`C:/ffmpeg/bin/ffmpeg.exe`)

## Monorepo Layout
```txt
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

## Quick Start
1. Start infrastructure:
   - `docker compose -f infra/postgres/docker-compose.yml up -d`
   - `docker compose -f infra/redis/docker-compose.yml up -d`
2. Install web/api deps at root: `npm install`
3. Run API: `npm run dev:api`
4. Run Web: `npm run dev:web`
5. Run workers:
   - `cd services/ai-worker && pip install -r requirements.txt && uvicorn app.main:app --reload --port 8101`
   - `cd services/video-worker && pip install -r requirements.txt && uvicorn app.main:app --reload --port 8102`
   - `cd services/analytics-worker && pip install -r requirements.txt && uvicorn app.main:app --reload --port 8103`

## Task Execution Flow
User action → API request → Task creation → Redis queue → Worker execution → Database update → UI refresh.

## FFmpeg Examples
- Preview render:
```bash
C:/ffmpeg/bin/ffmpeg.exe -y -i input.mp4 -vf scale=720:1280 -t 00:00:20 preview.mp4
```
- Burn-in subtitles:
```bash
C:/ffmpeg/bin/ffmpeg.exe -y -i input.mp4 -vf "subtitles=subtitles.srt" burnin.mp4
```
- Extract thumbnail frame:
```bash
C:/ffmpeg/bin/ffmpeg.exe -y -i input.mp4 -ss 00:00:01.000 -vframes 1 thumbnail.jpg
```

## Security
- JWT authentication (NestJS `auth` module scaffold)
- RBAC roles: `admin`, `planner`, `editor`, `operator`, `analyst`
