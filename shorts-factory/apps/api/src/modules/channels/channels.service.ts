import crypto from 'node:crypto';
import { Injectable } from '@nestjs/common';
import { CreateChannelsDto } from './dto/create-channels.dto';

@Injectable()
export class ChannelsService {
  list() {
    return [];
  }

  get(id: string) {
    return { id };
  }
  create(input: CreateChannelsDto) {
    return { id: crypto.randomUUID(), ...input };
  }
}
