import { Injectable } from '@nestjs/common';
import { CreateTasksDto } from './dto/create-tasks.dto';
import { TasksEntity } from './entity/tasks.entity';
import { RedisQueueService } from '../queue/redis-queue.service';

@Injectable()
export class TasksService {
  constructor(private readonly queue: RedisQueueService) {}

  async findAll(): Promise<TasksEntity[]> { return []; }
  async findOne(id: string): Promise<TasksEntity | null> { return { id, name: 'task', status: 'queued' } as TasksEntity; }
  async create(dto: CreateTasksDto): Promise<TasksEntity> {
    await this.queue.publish(dto.queue, { type: dto.type, projectId: dto.projectId });
    return { id: crypto.randomUUID(), name: dto.type, status: 'queued' } as TasksEntity;
  }
}
