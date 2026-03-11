import { IsOptional, IsString } from 'class-validator';

export class CreateTeamsDto {
  @IsOptional()
  @IsString()
  name?: string;
}
