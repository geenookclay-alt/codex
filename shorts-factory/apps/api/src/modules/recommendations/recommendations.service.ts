import crypto from 'node:crypto';
import { Injectable } from '@nestjs/common';
import { CreateRecommendationsDto } from './dto/create-recommendations.dto';

@Injectable()
export class RecommendationsService {
  list() {
    return [];
  }

  get(id: string) {
    return { id };
  }
  create(input: CreateRecommendationsDto) {
    return { id: crypto.randomUUID(), ...input };
  }
}
