import crypto from 'node:crypto';
import { Injectable } from '@nestjs/common';
import { CreateUsersDto } from './dto/create-users.dto';

@Injectable()
export class UsersService {
  list() {
    return [];
  }

  get(id: string) {
    return { id };
  }
  create(input: CreateUsersDto) {
    return { id: crypto.randomUUID(), ...input };
  }
}
