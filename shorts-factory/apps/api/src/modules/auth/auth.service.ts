import crypto from 'node:crypto';
import { Injectable } from '@nestjs/common';
import { CreateAuthDto } from './dto/create-auth.dto';

@Injectable()
export class AuthService {
  list() {
    return [];
  }

  get(id: string) {
    return { id };
  }
  create(input: CreateAuthDto) {
    return { id: crypto.randomUUID(), ...input };
  }
}
