import crypto from 'node:crypto';
import { Injectable } from '@nestjs/common';
import { CreateQueueDto } from './dto/create-queue.dto';

@Injectable()
export class QueueService {
  list() {
    return [];
  }

  get(id: string) {
    return { id };
  }

  // enqueue workflow tasks into Redis for workers.
  create(input: CreateQueueDto) {
    return { id: crypto.randomUUID(), ...input };
  }
}
