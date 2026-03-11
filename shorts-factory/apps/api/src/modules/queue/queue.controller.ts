import { Body, Controller, Get, Param, Post } from '@nestjs/common';
import { QueueService } from './queue.service';
import { CreateQueueDto } from './dto/create-queue.dto';

@Controller('queue')
export class QueueController {
  constructor(private readonly service: QueueService) {}

  @Get()
  list() {
    return this.service.list();
  }

  @Get(':id')
  get(@Param('id') id: string) {
    return this.service.get(id);
  }

  @Post()
  create(@Body() body: CreateQueueDto) {
    return this.service.create(body);
  }
}
