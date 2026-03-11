import { Body, Controller, Get, Param, Post, UseGuards } from '@nestjs/common';
import { QueueService } from './queue.service';
import { CreateQueueDto } from './dto/create-queue.dto';
import { QueueEntity } from './entity/queue.entity';
import { JwtGuard } from '../../common/jwt.guard';

@UseGuards(JwtGuard)
@Controller('queue')
export class QueueController {
  constructor(private readonly service: QueueService) {}

  @Get()
  findAll(): Promise<QueueEntity[]> {
    return this.service.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string): Promise<QueueEntity | null> {
    return this.service.findOne(id);
  }

  @Post()
  create(@Body() dto: CreateQueueDto): Promise<QueueEntity> {
    return this.service.create(dto);
  }
}
