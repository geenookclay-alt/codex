import { Injectable } from '@nestjs/common';

@Injectable()
export class AnalyticsService {
  list() { return { module: 'analytics', items: [] }; }
  upsert(dto: any) { return { module: 'analytics', ...dto }; }
}
