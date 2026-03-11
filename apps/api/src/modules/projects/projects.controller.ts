import { Body, Controller, Get, Post, UseGuards } from '@nestjs/common';
import { ProjectsService } from './projects.service';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';

@Controller('projects')
@UseGuards(JwtAuthGuard)
export class ProjectsController {
  constructor(private readonly service: ProjectsService) {}
  @Get()
  list() { return this.service.list(); }
  @Post()
  upsert(@Body() body: any) { return this.service.upsert(body); }
}
