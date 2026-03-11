import { Injectable } from '@nestjs/common';

@Injectable()
export class TeamsService {
  list() { return { module: 'teams', items: [] }; }
  upsert(dto: any) { return { module: 'teams', ...dto }; }
}
