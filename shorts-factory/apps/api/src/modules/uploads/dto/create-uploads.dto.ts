export class CreateUploadsDto {
  name!: string;
  teamId?: string;
  projectId?: string;
  metadata?: Record<string, unknown>;
}
