import { Injectable } from '@nestjs/common';

@Injectable()
export class ChannelPoliciesService {
  list() { return { module: 'channel-policies', items: [] }; }
  upsert(dto: any) { return { module: 'channel-policies', ...dto }; }
}
