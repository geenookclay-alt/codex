export class CreateTasksDto {
  name!: string;
  teamId?: string;
  projectId?: string;
  metadata?: Record<string, unknown>;
}
