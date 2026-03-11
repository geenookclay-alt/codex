import crypto from 'node:crypto';
import { Injectable } from '@nestjs/common';
import { CreateAnalyticsDto } from './dto/create-analytics.dto';

@Injectable()
export class AnalyticsService {
  list() {
    return [];
  }

  get(id: string) {
    return { id };
  }
  create(input: CreateAnalyticsDto) {
    return { id: crypto.randomUUID(), ...input };
  }
}
