import { Body, Controller, Get, Param, Post } from '@nestjs/common';
import { UploadsService } from './uploads.service';
import { CreateUploadsDto } from './dto/create-uploads.dto';

@Controller('uploads')
export class UploadsController {
  constructor(private readonly service: UploadsService) {}

  @Get()
  list() {
    return this.service.list();
  }

  @Get(':id')
  get(@Param('id') id: string) {
    return this.service.get(id);
  }

  @Post()
  create(@Body() body: CreateUploadsDto) {
    return this.service.create(body);
  }
}
