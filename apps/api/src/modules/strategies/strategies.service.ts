import { Injectable } from '@nestjs/common';

@Injectable()
export class StrategiesService {
  list() { return { module: 'strategies', items: [] }; }
  upsert(dto: any) { return { module: 'strategies', ...dto }; }
}
