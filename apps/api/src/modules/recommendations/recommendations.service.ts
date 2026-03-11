import { Injectable } from '@nestjs/common';

@Injectable()
export class RecommendationsService {
  list() { return { module: 'recommendations', items: [] }; }
  upsert(dto: any) { return { module: 'recommendations', ...dto }; }
}
