import crypto from 'node:crypto';
import { Injectable } from '@nestjs/common';
import { CreateProjectsDto } from './dto/create-projects.dto';

@Injectable()
export class ProjectsService {
  list() {
    return [];
  }

  get(id: string) {
    return { id };
  }
  create(input: CreateProjectsDto) {
    return { id: crypto.randomUUID(), ...input };
  }
}
