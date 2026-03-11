import { Module } from '@nestjs/common';
import { QueueController } from './queue.controller';
import { QueueService } from './queue.service';
import { RedisQueueService } from './redis-queue.service';

@Module({
  controllers: [QueueController],
  providers: [QueueService, RedisQueueService],
  exports: [QueueService, RedisQueueService]
})
export class QueueModule {}
