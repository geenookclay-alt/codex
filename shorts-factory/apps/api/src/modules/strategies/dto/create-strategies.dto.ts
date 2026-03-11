import { IsOptional, IsString } from 'class-validator';

export class CreateStrategiesDto {
  @IsOptional()
  @IsString()
  name?: string;
}
