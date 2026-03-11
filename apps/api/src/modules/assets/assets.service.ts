import { Injectable } from '@nestjs/common';

@Injectable()
export class AssetsService {
  list() { return { module: 'assets', items: [] }; }
  upsert(dto: any) { return { module: 'assets', ...dto }; }
}
