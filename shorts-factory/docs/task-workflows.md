# Task Workflow Map

## Supported Task Types
- generate_strategies
- generate_titles
- generate_hooks
- build_subtitles
- build_edl
- build_preview
- build_burnin
- extract_thumbnail_frame
- update_performance_summary
- recalculate_recommendations

## Flow
1. API receives user action.
2. API writes task metadata to `tasks` table.
3. API enqueues task to Redis queue (`shorts-factory-tasks`).
4. Responsible worker consumes and executes task.
5. Worker writes outputs to database tables.
6. Frontend refreshes data via React Query polling/invalidation.
