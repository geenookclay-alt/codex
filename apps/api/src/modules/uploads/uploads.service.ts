import { Injectable } from '@nestjs/common';

@Injectable()
export class UploadsService {
  list() { return { module: 'uploads', items: [] }; }
  upsert(dto: any) { return { module: 'uploads', ...dto }; }
}
