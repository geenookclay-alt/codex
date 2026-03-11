export type Role = 'admin' | 'planner' | 'editor' | 'operator' | 'analyst';

export interface TaskPayload {
  type:
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
  projectId: string;
  metadata?: Record<string, unknown>;
}
