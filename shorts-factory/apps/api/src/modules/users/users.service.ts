import { Injectable } from '@nestjs/common';
import { CreateUsersDto } from './dto/create-users.dto';
import { UsersEntity } from './entity/users.entity';

@Injectable()
export class UsersService {
  async findAll(): Promise<UsersEntity[]> { return []; }
  async findOne(id: string): Promise<UsersEntity | null> { return { id, name: 'users' } as UsersEntity; }
  async create(dto: CreateUsersDto): Promise<UsersEntity> {
    return { id: crypto.randomUUID(), name: dto.name ?? 'users' } as UsersEntity;
  }
}
