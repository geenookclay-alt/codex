import { IsOptional, IsString } from 'class-validator';

export class CreateAnalyticsDto {
  @IsOptional()
  @IsString()
  name?: string;
}
