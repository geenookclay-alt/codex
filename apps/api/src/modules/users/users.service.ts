import { Injectable } from '@nestjs/common';

@Injectable()
export class UsersService {
  list() { return { module: 'users', items: [] }; }
  upsert(dto: any) { return { module: 'users', ...dto }; }
}
