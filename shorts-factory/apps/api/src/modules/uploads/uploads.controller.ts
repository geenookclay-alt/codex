import { Body, Controller, Get, Param, Post, UseGuards } from '@nestjs/common';
import { UploadsService } from './uploads.service';
import { CreateUploadsDto } from './dto/create-uploads.dto';
import { UploadsEntity } from './entity/uploads.entity';
import { JwtGuard } from '../../common/jwt.guard';

@UseGuards(JwtGuard)
@Controller('uploads')
export class UploadsController {
  constructor(private readonly service: UploadsService) {}

  @Get()
  findAll(): Promise<UploadsEntity[]> {
    return this.service.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string): Promise<UploadsEntity | null> {
    return this.service.findOne(id);
  }

  @Post()
  create(@Body() dto: CreateUploadsDto): Promise<UploadsEntity> {
    return this.service.create(dto);
  }
}
