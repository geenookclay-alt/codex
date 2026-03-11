import { Injectable } from '@nestjs/common';
import { CreateStrategiesDto } from './dto/create-strategies.dto';
import { StrategiesEntity } from './entity/strategies.entity';

@Injectable()
export class StrategiesService {
  async findAll(): Promise<StrategiesEntity[]> { return []; }
  async findOne(id: string): Promise<StrategiesEntity | null> { return { id, name: 'strategies' } as StrategiesEntity; }
  async create(dto: CreateStrategiesDto): Promise<StrategiesEntity> {
    return { id: crypto.randomUUID(), name: dto.name ?? 'strategies' } as StrategiesEntity;
  }
}
