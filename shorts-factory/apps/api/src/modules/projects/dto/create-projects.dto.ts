import { IsOptional, IsString } from 'class-validator';

export class CreateProjectsDto {
  @IsOptional()
  @IsString()
  name?: string;
}
