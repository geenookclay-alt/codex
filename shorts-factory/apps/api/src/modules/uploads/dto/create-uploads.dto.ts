import { IsOptional, IsString } from 'class-validator';

export class CreateUploadsDto {
  @IsOptional()
  @IsString()
  name?: string;
}
