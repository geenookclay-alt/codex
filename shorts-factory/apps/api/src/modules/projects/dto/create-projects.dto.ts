export class CreateProjectsDto {
  name!: string;
  teamId?: string;
  projectId?: string;
  metadata?: Record<string, unknown>;
}
