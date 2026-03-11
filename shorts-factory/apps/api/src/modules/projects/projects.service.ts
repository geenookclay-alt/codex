import { Injectable } from '@nestjs/common';
import { CreateProjectsDto } from './dto/create-projects.dto';
import { ProjectsEntity } from './entity/projects.entity';

@Injectable()
export class ProjectsService {
  async findAll(): Promise<ProjectsEntity[]> { return []; }
  async findOne(id: string): Promise<ProjectsEntity | null> { return { id, name: 'projects' } as ProjectsEntity; }
  async create(dto: CreateProjectsDto): Promise<ProjectsEntity> {
    return { id: crypto.randomUUID(), name: dto.name ?? 'projects' } as ProjectsEntity;
  }
}
