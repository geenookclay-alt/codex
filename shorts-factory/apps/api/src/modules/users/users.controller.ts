import { Body, Controller, Get, Param, Post, UseGuards } from '@nestjs/common';
import { UsersService } from './users.service';
import { CreateUsersDto } from './dto/create-users.dto';
import { UsersEntity } from './entity/users.entity';
import { JwtGuard } from '../../common/jwt.guard';

@UseGuards(JwtGuard)
@Controller('users')
export class UsersController {
  constructor(private readonly service: UsersService) {}

  @Get()
  findAll(): Promise<UsersEntity[]> {
    return this.service.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string): Promise<UsersEntity | null> {
    return this.service.findOne(id);
  }

  @Post()
  create(@Body() dto: CreateUsersDto): Promise<UsersEntity> {
    return this.service.create(dto);
  }
}
