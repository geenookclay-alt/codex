import { Body, Controller, Get, Param, Post, UseGuards } from '@nestjs/common';
import { StrategiesService } from './strategies.service';
import { CreateStrategiesDto } from './dto/create-strategies.dto';
import { StrategiesEntity } from './entity/strategies.entity';
import { JwtGuard } from '../../common/jwt.guard';

@UseGuards(JwtGuard)
@Controller('strategies')
export class StrategiesController {
  constructor(private readonly service: StrategiesService) {}

  @Get()
  findAll(): Promise<StrategiesEntity[]> {
    return this.service.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string): Promise<StrategiesEntity | null> {
    return this.service.findOne(id);
  }

  @Post()
  create(@Body() dto: CreateStrategiesDto): Promise<StrategiesEntity> {
    return this.service.create(dto);
  }
}
