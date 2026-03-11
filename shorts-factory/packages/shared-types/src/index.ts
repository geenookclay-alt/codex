export type Role = 'admin' | 'planner' | 'editor' | 'operator' | 'analyst';

export type TaskType =
  | 'generate_strategies'
  | 'generate_titles'
  | 'generate_hooks'
  | 'build_subtitles'
  | 'build_edl'
  | 'build_preview'
  | 'build_burnin'
  | 'extract_thumbnail_frame'
  | 'update_performance_summary'
  | 'recalculate_recommendations';

export interface QueueTaskPayload {
  type: TaskType;
  projectId?: string;
  strategyId?: string;
  teamId?: string;
  metadata?: Record<string, unknown>;
}
