import { Body, Controller, Get, Param, Post } from '@nestjs/common';
import { StrategiesService } from './strategies.service';
import { CreateStrategiesDto } from './dto/create-strategies.dto';

@Controller('strategies')
export class StrategiesController {
  constructor(private readonly service: StrategiesService) {}

  @Get()
  list() {
    return this.service.list();
  }

  @Get(':id')
  get(@Param('id') id: string) {
    return this.service.get(id);
  }

  @Post()
  create(@Body() body: CreateStrategiesDto) {
    return this.service.create(body);
  }
}
