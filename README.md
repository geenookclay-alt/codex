# Shorts Factory v8

Monorepo for an AI-assisted YouTube Shorts operating system with human approvals, queue-first execution, and analytics feedback.

## Structure

- `apps/web`: Next.js + Tailwind + React Query UI
- `apps/api`: NestJS API (JWT + RBAC + domain modules)
- `services/*`: Python workers (FastAPI + queue processors)
- `packages/*`: shared TypeScript contracts, prompts, and policy helpers
- `infra/*`: local postgres/redis/storage bootstrap
- `docs`: architecture and operations docs

## Quick start

```bash
npm install
npm run dev:web
npm run dev:api
python services/planner-worker/planner_worker.py --help
```

## FFmpeg

Workers use a fixed default path:

```python
DEFAULT_FFMPEG_PATH = r"C:/ffmpeg/bin/ffmpeg.exe"
```
