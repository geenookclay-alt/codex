export class CreateUsersDto {
  name!: string;
  teamId?: string;
  projectId?: string;
  metadata?: Record<string, unknown>;
}
