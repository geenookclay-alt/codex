import { Injectable } from '@nestjs/common';
import { CreateTeamsDto } from './dto/create-teams.dto';
import { TeamsEntity } from './entity/teams.entity';

@Injectable()
export class TeamsService {
  async findAll(): Promise<TeamsEntity[]> { return []; }
  async findOne(id: string): Promise<TeamsEntity | null> { return { id, name: 'teams' } as TeamsEntity; }
  async create(dto: CreateTeamsDto): Promise<TeamsEntity> {
    return { id: crypto.randomUUID(), name: dto.name ?? 'teams' } as TeamsEntity;
  }
}
