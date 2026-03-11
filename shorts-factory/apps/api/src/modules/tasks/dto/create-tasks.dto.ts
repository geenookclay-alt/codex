import { IsIn, IsOptional, IsString, IsUUID } from 'class-validator';

export class CreateTasksDto {
  @IsString()
  type!: string;

  @IsIn(['ai','video','analytics'])
  queue!: 'ai' | 'video' | 'analytics';

  @IsOptional()
  @IsUUID()
  projectId?: string;
}
