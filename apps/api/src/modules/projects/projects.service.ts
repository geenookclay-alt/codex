import { Injectable } from '@nestjs/common';

@Injectable()
export class ProjectsService {
  list() { return { module: 'projects', items: [] }; }
  upsert(dto: any) { return { module: 'projects', ...dto }; }
}
