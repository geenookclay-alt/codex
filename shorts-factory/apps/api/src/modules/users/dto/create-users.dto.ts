import { IsOptional, IsString } from 'class-validator';

export class CreateUsersDto {
  @IsOptional()
  @IsString()
  name?: string;
}
