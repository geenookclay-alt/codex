# Shorts Factory v7 Architecture

## End-to-end flow
User action -> API request -> task record -> Redis queue -> worker execution -> PostgreSQL update -> UI refresh via polling/react-query.

## Services
- `apps/web`: Next.js collaboration and operations console.
- `apps/api`: NestJS API, authN/authZ, orchestration, and queue publishing.
- `services/ai-worker`: FastAPI inference + background worker for strategy/title/hook/recommendation jobs.
- `services/video-worker`: FastAPI + worker for subtitles/EDL/preview/burn-in rendering with FFmpeg.
- `services/analytics-worker`: FastAPI + worker for aggregation and recommendation refresh jobs.

## Scaling notes
- Stateless API and workers; scale horizontally behind a load balancer.
- Redis Streams can replace list queues for stronger guarantees.
- Use pgBouncer and read replicas for analytics heavy workloads.
