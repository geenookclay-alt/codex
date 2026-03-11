import crypto from 'node:crypto';
import { Injectable } from '@nestjs/common';
import { CreateUploadsDto } from './dto/create-uploads.dto';

@Injectable()
export class UploadsService {
  list() {
    return [];
  }

  get(id: string) {
    return { id };
  }

  // enqueue workflow tasks into Redis for workers.
  create(input: CreateUploadsDto) {
    return { id: crypto.randomUUID(), ...input };
  }
}
