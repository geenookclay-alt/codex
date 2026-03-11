import { Injectable } from '@nestjs/common';
import { CreateAnalyticsDto } from './dto/create-analytics.dto';
import { AnalyticsEntity } from './entity/analytics.entity';

@Injectable()
export class AnalyticsService {
  async findAll(): Promise<AnalyticsEntity[]> { return []; }
  async findOne(id: string): Promise<AnalyticsEntity | null> { return { id, name: 'analytics' } as AnalyticsEntity; }
  async create(dto: CreateAnalyticsDto): Promise<AnalyticsEntity> {
    return { id: crypto.randomUUID(), name: dto.name ?? 'analytics' } as AnalyticsEntity;
  }
}
