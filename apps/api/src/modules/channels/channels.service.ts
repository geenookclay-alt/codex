import { Injectable } from '@nestjs/common';

@Injectable()
export class ChannelsService {
  list() { return { module: 'channels', items: [] }; }
  upsert(dto: any) { return { module: 'channels', ...dto }; }
}
