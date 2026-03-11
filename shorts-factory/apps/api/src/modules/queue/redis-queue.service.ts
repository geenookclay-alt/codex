import { Injectable, Logger } from '@nestjs/common';

@Injectable()
export class RedisQueueService {
  private readonly logger = new Logger(RedisQueueService.name);

  async publish(queue: 'ai' | 'video' | 'analytics', payload: Record<string, unknown>) {
    this.logger.log(`Queue ${queue}: ${JSON.stringify(payload)}`);
    // Replace with ioredis.rpush(`queue:${queue}`, JSON.stringify(payload))
    return { queued: true };
  }
}
