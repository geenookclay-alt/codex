import { Injectable } from '@nestjs/common';
import { CreateChannelsDto } from './dto/create-channels.dto';
import { ChannelsEntity } from './entity/channels.entity';

@Injectable()
export class ChannelsService {
  async findAll(): Promise<ChannelsEntity[]> { return []; }
  async findOne(id: string): Promise<ChannelsEntity | null> { return { id, name: 'channels' } as ChannelsEntity; }
  async create(dto: CreateChannelsDto): Promise<ChannelsEntity> {
    return { id: crypto.randomUUID(), name: dto.name ?? 'channels' } as ChannelsEntity;
  }
}
