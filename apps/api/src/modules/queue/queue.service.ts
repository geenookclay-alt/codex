import { Injectable } from '@nestjs/common';

@Injectable()
export class QueueService {
  list() { return { module: 'queue', items: [] }; }
  upsert(dto: any) { return { module: 'queue', ...dto }; }
}
