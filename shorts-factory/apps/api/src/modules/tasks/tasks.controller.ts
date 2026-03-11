import { Body, Controller, Get, Param, Post, UseGuards } from '@nestjs/common';
import { TasksService } from './tasks.service';
import { CreateTasksDto } from './dto/create-tasks.dto';
import { TasksEntity } from './entity/tasks.entity';
import { JwtGuard } from '../../common/jwt.guard';

@UseGuards(JwtGuard)
@Controller('tasks')
export class TasksController {
  constructor(private readonly service: TasksService) {}

  @Get()
  findAll(): Promise<TasksEntity[]> {
    return this.service.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string): Promise<TasksEntity | null> {
    return this.service.findOne(id);
  }

  @Post()
  create(@Body() dto: CreateTasksDto): Promise<TasksEntity> {
    return this.service.create(dto);
  }
}
