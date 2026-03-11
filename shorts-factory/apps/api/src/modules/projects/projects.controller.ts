import { Body, Controller, Get, Param, Post, UseGuards } from '@nestjs/common';
import { ProjectsService } from './projects.service';
import { CreateProjectsDto } from './dto/create-projects.dto';
import { ProjectsEntity } from './entity/projects.entity';
import { JwtGuard } from '../../common/jwt.guard';

@UseGuards(JwtGuard)
@Controller('projects')
export class ProjectsController {
  constructor(private readonly service: ProjectsService) {}

  @Get()
  findAll(): Promise<ProjectsEntity[]> {
    return this.service.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string): Promise<ProjectsEntity | null> {
    return this.service.findOne(id);
  }

  @Post()
  create(@Body() dto: CreateProjectsDto): Promise<ProjectsEntity> {
    return this.service.create(dto);
  }
}
