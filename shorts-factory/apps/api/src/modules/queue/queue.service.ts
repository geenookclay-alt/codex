import { Injectable } from '@nestjs/common';
import { CreateQueueDto } from './dto/create-queue.dto';
import { QueueEntity } from './entity/queue.entity';
import { RedisQueueService } from './redis-queue.service';

@Injectable()
export class QueueService {
  constructor(private readonly redisQueue: RedisQueueService) {}

  async findAll(): Promise<QueueEntity[]> { return []; }
  async findOne(id: string): Promise<QueueEntity | null> { return { id, name: 'queue-event' } as QueueEntity; }
  async create(dto: CreateQueueDto): Promise<QueueEntity> {
    await this.redisQueue.publish(dto.queue, dto.payload);
    return { id: crypto.randomUUID(), name: dto.queue } as QueueEntity;
  }
}
