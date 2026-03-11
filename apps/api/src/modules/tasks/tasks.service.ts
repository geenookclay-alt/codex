import { Injectable } from '@nestjs/common';

@Injectable()
export class TasksService {
  list() { return { module: 'tasks', items: [] }; }
  upsert(dto: any) { return { module: 'tasks', ...dto }; }
}
