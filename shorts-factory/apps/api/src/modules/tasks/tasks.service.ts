import crypto from 'node:crypto';
import { Injectable } from '@nestjs/common';
import { CreateTasksDto } from './dto/create-tasks.dto';

@Injectable()
export class TasksService {
  list() {
    return [];
  }

  get(id: string) {
    return { id };
  }

  // enqueue workflow tasks into Redis for workers.
  create(input: CreateTasksDto) {
    return { id: crypto.randomUUID(), ...input };
  }
}
