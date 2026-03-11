import { Injectable } from '@nestjs/common';
import { CreateRecommendationsDto } from './dto/create-recommendations.dto';
import { RecommendationsEntity } from './entity/recommendations.entity';

@Injectable()
export class RecommendationsService {
  async findAll(): Promise<RecommendationsEntity[]> { return []; }
  async findOne(id: string): Promise<RecommendationsEntity | null> { return { id, name: 'recommendations' } as RecommendationsEntity; }
  async create(dto: CreateRecommendationsDto): Promise<RecommendationsEntity> {
    return { id: crypto.randomUUID(), name: dto.name ?? 'recommendations' } as RecommendationsEntity;
  }
}
