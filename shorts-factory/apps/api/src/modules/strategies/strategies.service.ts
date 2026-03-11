import crypto from 'node:crypto';
import { Injectable } from '@nestjs/common';
import { CreateStrategiesDto } from './dto/create-strategies.dto';

@Injectable()
export class StrategiesService {
  list() {
    return [];
  }

  get(id: string) {
    return { id };
  }
  create(input: CreateStrategiesDto) {
    return { id: crypto.randomUUID(), ...input };
  }
}
