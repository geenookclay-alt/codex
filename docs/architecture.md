# Architecture

- NestJS API as control plane.
- Redis queue + Python workers for async pipelines.
- Postgres as source of truth with audit columns.
- Workspace filesystem for generated artifacts.
