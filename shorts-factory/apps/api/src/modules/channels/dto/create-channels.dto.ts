import { IsOptional, IsString } from 'class-validator';

export class CreateChannelsDto {
  @IsOptional()
  @IsString()
  name?: string;
}
