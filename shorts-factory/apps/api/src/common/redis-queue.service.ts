import { Injectable } from '@nestjs/common';
import { Queue } from 'bullmq';

@Injectable()
export class RedisQueueService {
  private queue = new Queue('shorts-factory-tasks', {
    connection: { host: process.env.REDIS_HOST ?? 'localhost', port: 6379 },
  });

  async enqueue(name: string, payload: Record<string, unknown>) {
    return this.queue.add(name, payload, { removeOnComplete: true });
  }
}
