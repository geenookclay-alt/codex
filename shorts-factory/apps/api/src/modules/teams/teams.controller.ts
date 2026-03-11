import { Body, Controller, Get, Param, Post, UseGuards } from '@nestjs/common';
import { TeamsService } from './teams.service';
import { CreateTeamsDto } from './dto/create-teams.dto';
import { TeamsEntity } from './entity/teams.entity';
import { JwtGuard } from '../../common/jwt.guard';

@UseGuards(JwtGuard)
@Controller('teams')
export class TeamsController {
  constructor(private readonly service: TeamsService) {}

  @Get()
  findAll(): Promise<TeamsEntity[]> {
    return this.service.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string): Promise<TeamsEntity | null> {
    return this.service.findOne(id);
  }

  @Post()
  create(@Body() dto: CreateTeamsDto): Promise<TeamsEntity> {
    return this.service.create(dto);
  }
}
