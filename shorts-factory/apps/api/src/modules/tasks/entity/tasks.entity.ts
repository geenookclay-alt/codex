export class TasksEntity {
  id!: string;
  name!: string;
  status!: 'queued' | 'running' | 'done' | 'failed';
}
