export class CreateAnalyticsDto {
  name!: string;
  teamId?: string;
  projectId?: string;
  metadata?: Record<string, unknown>;
}
