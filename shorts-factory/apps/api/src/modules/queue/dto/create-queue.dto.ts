import { IsIn, IsObject } from 'class-validator';

export class CreateQueueDto {
  @IsIn(['ai','video','analytics'])
  queue!: 'ai' | 'video' | 'analytics';

  @IsObject()
  payload!: Record<string, unknown>;
}
