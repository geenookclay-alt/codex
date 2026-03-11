import crypto from 'node:crypto';
import { Injectable } from '@nestjs/common';
import { CreateTeamsDto } from './dto/create-teams.dto';

@Injectable()
export class TeamsService {
  list() {
    return [];
  }

  get(id: string) {
    return { id };
  }
  create(input: CreateTeamsDto) {
    return { id: crypto.randomUUID(), ...input };
  }
}
